Logical Methods in Computer Science
Vol. 7 (2:17) 2011, pp. 1–33                                                         Submitted    Jun. 15, 2010
www.lmcs-online.org                                                                  Published    Jun. 21, 2011




    AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC

                                            ROBERT ATKEY

     University of Strathclyde, UK
     e-mail address: Robert.Atkey@cis.strath.ac.uk


         Abstract. Type-based amortised resource analysis following Hofmann and Jost—where
         resources are associated with individual elements of data structures and doled out to the
         programmer under a linear typing discipline—have been successful in providing concrete
         resource bounds for functional programs, with good support for inference. In this work
         we translate the idea of amortised resource analysis to imperative pointer-manipulating
         languages by embedding a logic of resources, based on the affine intuitionistic Logic of
         Bunched Implications, within Separation Logic. The Separation Logic component allows
         us to assert the presence and shape of mutable data structures on the heap, while the
         resource component allows us to state the consumable resources associated with each
         member of the structure.
            We present the logic on a small imperative language, based on Java bytecode, with
         procedures and mutable heap. We have formalised the logic and its soundness property
         within the Coq proof assistant and extracted a certified verification condition generator.
         We also describe an proof search procedure that allows generated verification conditions to
         be discharged while using linear programming to infer consumable resource annotations.
            We demonstrate the logic on some examples, including proving the termination of in-
         place list reversal on lists with cyclic tails.




                                           1. Introduction
Tarjan, in his paper introducing the concept of amortised complexity analysis [25], noted
that the statement and proof of complexity bounds for operations on some data structures
can be simplified if we think of the data structure as being able to store “credits” that
are used up by later operations. By setting aside credit inside a data structure to be
used by later operations, the cost of a sequence of operations can be amortised over time.
In this paper, we propose a way to merge amortised complexity analysis with Separation
Logic [19, 24] to formalise some of these arguments and to simplify the specification and
verification of resource-consuming pointer-manipulating programs.
     Separation Logic is built upon a notion of resources and their separation. The assertion
A  B holds for some resource if it can be split into two separate resources that make A
true and B true respectively. Resource separation enables local reasoning about mutation
of resources; if the program mutates the resource associated with A, then we know that B
   1998 ACM Subject Classification: D.2.4, F.3.1.
   Key words and phrases: resource bounded computing, amortised analysis, separation logic, java bytecode,
program logic, resource models.



l    LOGICAL METHODS
     IN COMPUTER SCIENCE                      DOI:10.2168/LMCS-7 (2:17) 2011
                                                                                             c
                                                                                             CC
                                                                                                  R. Atkey
                                                                                                  Creative Commons
2                                             R. ATKEY




is still true on its separate resource. Usually Separation Logic uses mutable heaps as its
notion of resource. In this paper, we combine heaps with consumable resources to reason
about resource consumption as well as resource mutation.
     To see how Separation Logic-style reasoning about consumable resources is beneficial,
consider the standard inductively defined list segment predicate from Separation Logic,
augmented with an additional proposition R denoting the presence of a consumable resource
for every element of the list:
                lsegpR, x, y q     x  y ^ emp
                                   _ Dd, z. rx data
                                                ÞÑ ds  rx next
                                                           ÞÑ zs  R  lsegpz, yq
We will introduce the assertion logic properly in Section 4 below. We can represent a heap
H and a consumable resource r that satisfy this predicate graphically:
                         H    a           b        c        d
                                                                    null

                         r    R           R       R         R
So we have r, H |ù lsegpR, x, null q, assuming x contains the address of the head of the list.
Here r  R  R  R  R—we assume that consumable resources form a commutative monoid—
and r represents the resource that is available for the program to use in the future. We can
split H and r to separate out the head of the list with its associated resource:
                        H1    a      H2            c
                                          b                  d
                                                                    null

                         r1   R      r2 R         R         R
This heap and resource satisfy r1  r2 , H1 Z H2 |ù rx ÞÑ as  rx ÞÑ y s  R  lsegpR, y, null q,
                                                          data       next

where H1 Z H2  H, r1  r2  r and we assume that y contains the address of the b element.
Now that we have separated out the head of the list and its associated consumable resource,
we are free to mutate the heap H1 and consume the resource r1 without affecting the tail
of the list. So the program can move to a new state where the head of the list has been
mutated to A and the associated resource has been consumed:
                        H1        H2            c
                            A           b                d
                                                                 null

                                     r2 R         R         R
We do not need to do anything special to reason that the tail of the list and its associated
consumable resource are unaffected.
    The combined assertion about heap and consumable resource describes the current
shape and contents of the heap and also the available resource that the program may
consume in the future. By ensuring that, for every state in the program’s execution, the
resource consumed plus the resource available for consumption in the future is less than or
equal to a predefined bound, we can ensure that the entire execution is resource bounded.
This is the main assertion of soundness for our program logic in Section 3.5. We also treat
a variant program logic that allows dynamic but fallible resource acquisition in Section 3.6.
    By intermixing resource assertions with Separation Logic assertions about the shapes
of data structures, as we have done with the resource carrying lseg predicate above, we can
                 AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                           3




specify amounts of resource that depend on the shape of data structures in memory. By the
definition of lseg, we know that the amount of resource available to the program is linearly
proportional to the length of the list, without having to do any arithmetic reasoning about
lengths of lists. In Section 4.2 we describe some useful inductively defined predicates that
maintain a close connection between shape and resources.
    The association of resources with parts of a data structure is exactly the banker’s
approach to amortised complexity analysis proposed by Tarjan.
    Our original inspiration for this work came from the work of Hofmann and Jost [15] on
the automatic heap-space analysis of functional programs. Their analysis associates with
every element of a data structure a permission to use a piece of resource (in their case, heap
space). This resource is made available to the program when the data structure is decom-
posed using pattern matching. When constructing part of a data structure, the required
resources must be available. A linear type system is used to ensure that data structures
carrying resources are not duplicated since this would entail duplication of consumable re-
source. This scheme was later extended to imperative object-oriented languages [16, 17],
but still using a type-based analysis.

1.1. Contributions. We summarise the content and contributions of this work:
  In Section 3, we define a program logic that allows mixing of assertions about heap shapes
  and assertions about future consumable resources. Tying these together allows us to easily
  state resource properties in terms of the shapes of heap-based data structures, rather than
  in terms of extensional properties such as their size or contents. We have formalised the
  soundness proof of our program logic in the Coq proof assistant.
  In Section 4 we present a syntax for our assertion logic, based on a combination of Boolean
  Bunched Implications extended with pointer assertion primitives, as is usual for Separa-
  tion Logic, and affine intuitionistic Bunched Implications to declaratively state properties
  of the consumable resource available to a program. We also discuss several useful induc-
  tively defined predicates for this logic that demonstrate tight connections between heap
  shapes and resources. We also discuss the advantages and disadvantages of this tight
  connection.
  In Section 5, we define a restricted subset of the assertion logic that allows us to perform
  effective proof search to discharge verification conditions, while inferring resource anno-
  tations. A particular feature of the proof search procedure we describe is that, given loop
  invariants that specify only the the shape of data structures, we can infer the necessary
  consumable resource annotations.
  In Section 2 and Section 6, we demonstrate the logic on some examples, showing how
  a mixture of amortised resource analysis and Separation Logic can be used to simplify
  resource-aware specifications, deal with relatively complex pointer manipulation and to
  prove termination in the presence of cyclic structures in the heap.

1.2. Differences to previously published versions. This paper is a revised and ex-
panded version of the ESOP 2010 conference version [5]. Additional explanation has been
provided and Section 3.6 has been added on a variant program logic accounting for dynamic
resource acquisition. Section 4 has been expanded with more examples of inductively de-
fined predicates tightly integrating shape and resource properties, and a discussion of the
disadvantages of this integration. Section 5 on automated verification and proof search has
4                                          R. ATKEY




been refined for clarity and to better match the implementation. We have also included the
merge-sort example in Section 2.2 from an invited TGC 2010 paper [2].

                                 2. Motivating Examples
The example we gave in the introduction, where a program iterates through a list consuming
resources as it proceeds, only demonstrates an extremely simple, albeit common, pattern.
In this section, we give two more complex examples that serve to highlight the advantages of
the amortised approach to specifying and verifying resource bounds. The first example, in
Section 2.1, demonstrates how the integrated description of available consumable resources
and heap structure helps with specification. The second example, in Section 2.2, shows
how the amortised approach simplifies the problem of verifying the resource consumption
of a pointer manipulating program. This example also shows a weakness of maintaining a
tight connection between heap shape and consumable resources, which we discuss further
in Section 4.3.
    In each case we attempt to demonstrate how amortised reasoning is easier than the
traditional approach of keeping a global counter for consumed resources as a “ghost” variable
in the logic.

2.1. Functional Queues. We consider so-called functional queues [18, 8], where a queue
is represented by a pair of lists. This example is a standard one for introducing amortised
complexity analysis [21]. We verify an imperative implementation that performs mutations
in-place on the underlying lists. The point of this example is to see how the amortised
technique simplifies the specifications of the procedures operating on this data structure.
                              a         b        c       d
                                                                  null
                                   e        f

     The top list represents the head of the queue, while the bottom list represents the tail of
the queue in reverse. This structure represents the queue ra, b, c, d, f, es. When we enqueue
a new element, we add it to the head of the bottom list. To dequeue an element, we remove
it from the head of the top list. If the top list is empty, then we reverse the bottom list
and change the top pointer to point to it, changing the bottom pointer to point to null ,
representing the empty list.
     When determining the complexity of these operations, it is obvious that the enqueue
operation is constant time, but the dequeue operation either takes constant time if the top
list is empty, or takes time linear in the size of the bottom list in order to perform the
reversal. If we were to account for resource usage by maintaining a global counter then
we would have to expose the lengths of the two lists in specification of the enqueue and
dequeue instructions. So we would need a predicate queuepx, h, tq to state that x points to
a queue with a head and tail lists of lengths h and t respectively. The operations would
have the specifications (written as Hoare triples):
    r 1 .   tqueuepx, h, tq ^ rc  r1 u enqueue tqueuepx, h, t 1q ^ rc  r1 Ru
    r1.     tqueuepx, 0, tq ^ rc  r1 u dequeue tqueuepx, t  1, 0q ^ rc  r1 p1 tqRu
    r1. tqueuepx, h 1, tq ^ rc  r1 u dequeue tqueuepx, h, tq ^ rc  r1 Ru
                  AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                               5




where rc is a ghost variable counting the total amount of resource consumed by the program,
and R is the amount of resource required to perform a single list node manipulation. The
dotted minus t  1 denotes the predecessor operation on natural numbers. Note that we
have had to give two specifications for dequeue for the cases when the head list is empty
and when the head list has an element. The accounting for the sizes of the internals of the
queue data structure is of no interest to clients of this data structure. These specifications
complicate clients’ reasoning when using these queues.
     Using amortised analysis, this specification can be drastically simplified. We associate
a single piece of resource with each element of the tail list so that when we come to reverse
the list we have the necessary resource available to reverse each list element. The queue
predicate is therefore:
           queuepxq  Dy, z. rx ÞÑ y s  rx ÞÑ z s  lsegpe, y, null q  lsegpR, z, null q
                                  head         tail

where lseg is the resource-carrying list predicate given above and e is the unit of the con-
sumable resource monoid, representing no resource. The list holding the head of the queue
has no resource associated with every element, while the list holding the tail of the queue
does have a resource associated with every element, waiting to pay for the list reversal when
it occurs. Diagrammatically, a queue with associated resources looks like this:
                             a         b        c        d
                                                                      null
                                    e         f

                                    R         R
    The specifications of the operations now becomes straightforward:
      tqueuepxq  R  Ruenqueuetqueuepxqu                tqueuepxq  Rudequeuetqueuepxqu
To enqueue an element, we require two elements of resource: one to add the new element
to the tail list, and one to “store” in the list so that we may use it for a future reversal
operation. To dequeue an element, we require a single element of resource to remove an
element from a list. If a list reversal is required then it is paid for by the resources previously
required by enqueue.
    Once we have set the specification of queues to store one element of resource for every
node in the tail list, we can use the resource annotation inference procedure presented in
Section 5 to generate the resource parts of the enqueue and dequeue specifications.

2.2. Merge-sort Inner Loop. We now describe a more complicated list manipulating
program that shows the benefits of the amortised approach for verification. This example
demonstrates the combination of reasonably complex pointer manipulation with resource
reasoning. Most of the technical details arise from dealing with the heap-shape behaviour
of the program; the resource bounds simply drop out thanks to the inference of resource
annotations.
     Consider the Java method declaration mergeInner shown in Figure 1 that describes
the inner loop of an in-place merge sort algorithm for linked lists1. The method takes two
arguments: list, a reference to the head node of a linked list; and k, an integer. The
integer argument dictates the sizes of the sublists that the method will be merging in this
  1Adapted from C code: http://www.chiark.greenend.org.uk/ sgtatham/algorithms/listsort.html.
                                                               ~
6                                     R. ATKEY




public static Node mergeInner (Node list, int k) {
     Node p      = list;
     Node tail   = null;

     list = null;

     while (p != null) {
          Node q = p;
          for (int i = 0; i < k; i++) {
               q = q.next;
               if (q == null) break;
          }

         Node pstop = q;
         int qsize = k;
         while (p != pstop || (qsize > 0 && q != null)) {
              Node e;
              if (p == pstop) {
                   e = q;
                   q = q.next;
                   qsize--;
              } else if (qsize == 0 || q == null) {
                   e = p;
                   p = p.next;
              } else if (p.data <= q.data) {
                   e = p;
                   p = p.next;
              } else {
                   e = q;        // perform swap
                   q = q.next;
                   qsize--;
              }

               if (tail != null)      tail.next = e;
               else                   list = e;

               tail = e;
         }

         p = q;
     }

     if (tail == null) return null; else tail.next = null;
     return list;
}

              Figure 1: Inner loop of an in-place linked-list merge sort
                   AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                                 7




pass. The method steps through the list 2*k elements at a time, merging the two sublists
of length k each time. The outer loop does the 2*k stepping, and the inner loop does the
merging. To accomplish a full merge sort, mergeInner would be called log2 n times with
doubling k, where n is the length of the list.
     Assume that we wish to account for the number of swapping operations performed by
this method, i.e. the number of times that the fourth branch of the if statement in the
inner loop is executed. We accomplish this in our implementation by inserting a special
consume instruction at this point.
     The pre- and post-conditions of the method are as follows:
                 PrepmergeInnerq : list  null ^ plsegpx, list, null q  Ry q
                PostpmergeInnerq : lsegp0, retval, null q
     The precondition states that the first argument points to a list segment ending with
null, with x amount of resource associated with every element of the list, and y amount
of additional resource that may be used. The actual values of x and y will be inferred by a
linear program solver. The condition list  null is a safety condition required to prevent
a null pointer exception.
     The outer loop in the method needs a disjunctive invariant corresponding to whether
this is the first iteration or a later iteration.
           plsegpo1 , list, tailq  rtail next
                                          ÞÑ ?s  rtail data
                                                         ÞÑ ?s  lsegpo2 , p, null q  Ro q
                                                                                          3

         _ pplist  null ^ tail  null q  lsegpo4 , p, null q  Ro q 5


      The first disjunct is used on normal iterations of loop: the variable list points to the
list that has been processed so far, ending at tail; and p points to the remainder of the list
that is to be processed. We have annotated these lists with the resource variables o1 and
o2 that will contain the resources associated with each element of these lists. The second
disjunct covers the case of the first iteration, when list and tail are null and p points
to the complete list to be processed. The resource annotation o4 will be filled in with the
amount of resource that is required for every element of the list to be processed. As one
might expect, this will be equal to the value of x, the amount of resource required by the
precondition of the method.
      Moving on, we consider the first inner loop that advances the pointer q by k elements
forward, thus splitting the list ahead of p into a k-element segment and the rest of the list.
The next loop will merge the first k-element segment with the k-element prefix of the second
segment. It is convenient for our implementation to split out this inner loop into another
method2, with the following signature:
public static Node advance (Node l, int k)
      The argument l points to a linked list, and the method will advance k elements through
the list (or until the end) and return a pointer to the split point. The specification of this
method is:
                 Prepadvanceq : lsegpa0 , l, null q
                Postpadvanceq : lsegpa0 , l, retvalq  lsegpa0 , retval, null q
  2This is because our implementation works on unstructured JVM-like bytecode, and so cannot easily
apply Separation Logic’s frame rule to modularly reason about the loop. Using a separate method allows
application of the frame rule. See Remark 3.2.
8                                           R. ATKEY




     Again, we have left the resource annotation on the elements of the list as a variable a0 ,
to be filled in by the linear solver. The appearance of the same variable in the pre- and
post-condition implies that we expect this resource to be preserved by the method. The
fact that we have had to explicitly mention the resources that must be preserved points to
a limitation of the amortised method as we present it here. We discuss this issue further in
Section 4.3.
     Proceeding though our main method, the invariant of the inner loop is as follows, again
as two disjuncts according to whether it is the first or later iteration of the outer loop:
          plsegpi1 , list, tailq  rtail next
                                           ÞÑ ?s  rtail data
                                                          ÞÑ ?s
                               lsegpi2 , p, pstopq  lsegpi3 , q, null q  Ri q
                                                                           4

        _ pplist  null ^ tail  null q  lsegpi5 , p, pstopq  lsegpi6 , q, null q  Ri q
                                                                                       7


The first part of each disjunct is as before, stating that list to tail contains the part of list
that has been processed. Since we have now split the remainder of the list into two pieces
we have two separate list segments referenced by p and q pointing to the parts of the list
that are to be merged. The resource meta-variable i1 will indicate the amount of resource
associated with the list that has been processed; i2 and i5 are the amount of resource
associated with the “left-hand” pending list; and i3 and i4 are the resource associated with
the “right-hand” pending list.
     At the end of the method, we null terminate the list and return. A superfluous null
check on this is required for our tool to prove memory safety. The fact that this is non-
null relies on the execution of the inner loop at least once, which requires that k ¡ 0. This
fact is not expressible in the logic of the implementation described in Section 5.
     Running this example through our implementation produces the solution x  1, y  0
for the precondition’s resource annotations. This indicates that the input list needs to
contain one element of resource for every list element. For the outer loop’s invariant, we
obtain o2  o4  1 and all the others are 0. This indicates that the list we have processed has
had all its resources consumed, while the list remaining to be processed still has associated
resources. This is as expected for a loop iterating through a list. The specification of
advance is completed by inferring a0  1, indicating that advance preserves the resources
associated with the list. Finally the inner loop’s invariant has i2  i3  i5  i6  1 and
all others 0, indicating that the two list segments that are remaining to be processed have
associated resources, while the processed segments do not.

2.2.1. Comparisons to other techniques. Though we have had to work to supply the loop
invariants for our implementation, we note that these invariants may be inferred by other
tools, for example [6], and the resource variables automatically inserted using the procedure
outlined in Section 5. The key to the amortised approach is the tight connection between
shape invariants, which is a complex but well-studied problem, and resource consumption.
     Most other techniques for resource usage analysis that handle data structures do so by
considering the sizes of the structures. The SPEED system of Gulwani et al. [13] can infer
resource bounds for programs manipulating heap-based data structures, but only when these
data structures are manipulated through abstract interfaces. The specifications for these
abstract interfaces record the effect of the operations on the size of the data structure. Thus,
the technique is unable to cope with the kind of program that we have presented above that
uses direct pointer manipulation. Nevertheless, Gulwani et al. report impressive results on
real-world Microsoft product code.
                 AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                           9




     The COSTA system [1] can deal with some uses of direct pointer manipulation, but
accounts for the sizes of heap-based data structures by counting the length of the longest
path from a given reference. Thus, it cannot deal with programs that demonstrate sharing
on the heap; the Java method described above has, in its inner loop, three pointers all
pointing to the same list.
     One might also use Separation Logic to deal with sharing on the heap, and add informa-
tion on the sizes of heap-based data structures to account for resource usage. So one would
have a predicate lsegn px, y q that describes a list segment of length n from x to y, along
with a ghost variable to track resource consumption as discussed in Section 2.1. We argue
that the amortised approach described here is simpler due to the differences in reasoning
between the global property of the length of a whole list, and the local property of each
list element having an associated amount of resource to be used. For example, consider the
specification of the advance method using sized structures:
    Prepadvanceq : lsegn pl, null q
   Postpadvanceq : Dn1 , n2 . n1 n2  n ^ plsegn1 pl, retvalq  lsegn2 pretval, null qq
We have had to introduce two existential variables indicating the sizes of the lists returned
by the method. These additional values have to then be related back to the length of the
original list by the calling method, and thence to the resource consumption, requiring non-
straightforward arithmetic reasoning. The amortised approach exploits the shape-reasoning
already present in Separation Logic to account for resources.

                   3. A Program Logic for Heap and Resources
We now describe a simple programming language and a consumable-resource-aware logic for
it. We define a “shallow” program logic where we treat pre- and post-conditions and pro-
gram assertions as arbitrary predicates over heaps and consumable resources. In Section 4,
we will layer on top of this a “deep” assertion logic where predicates are actually Separation
Logic formulae augmented with atomic resource propositions.
    At the end of this section, we consider a variant system that allows dynamic but fallible
resource acquisition as well as resource consumption.
    The development in this section has been formalised within the Coq proof assistant; thus
the shallow embedding makes use of Coq’s own logic as the assertion logic. We also make
minor use of Coq’s dependent types. Lemma 3.1 and Theorem 3.3 establishing the sound-
ness of the program logic have been mechanically verified within Coq, as have Lemma 3.5
and Theorem 3.6 establishing soundness for the dynamic resource acquisition variant.

3.1. Semantic Domains. Assume an infinite set A of memory addresses. We model heaps
as finite partial maps H  pA  Fq áfin V, where F ranges over field names and V  AK Z
represents the values that programs can directly manipulate: possibly null addresses and
integers. We write dom pH q for the domain of a heap and H1 #H2 for heaps with disjoint
domains; H1 Z H2 denotes union of heaps with disjoint domains.
     Consumable resources are represented as elements of an ordered monoid pR, , , eq,
where e is the least element. Example consumable resources include pN, ¤, , 0q or pQ¥0 , ¤
, , 0q for representing a single resource that is consumed (e.g. time or space), or multisets
for representing multiple named resources that may be consumed independently. The or-
dering on consumable resources is used to allow weakening in our assertion logic: we allow
10                                        R. ATKEY




the asserter to assert that more resources are required by the program than are actually
needed.
     As is standard in the semantics of substructural logics [23], we make use of a ternary
relation to describe the combination of separate entities. In our case, the entities are pairs
of heaps and consumable resources:
                Rxyz  H1 #H2 ^ H1 Z H2  H3 ^ r1  r2  r3
                        where x  pH1 , r1 q, y  pH2 , r2 q, z  pH3 , r3 q
We extend the order on resources to pairs of heaps and resources by pH1 , r1 q  pH2 , r2 q iff
H1  H2 and r1  r2 .

3.2. A Little Virtual Machine. The programming language we treat is a simple stack-
based virtual machine, similar to Java bytecode. We have removed the class-based object
system and virtual methods, but retained mutable heap and procedures. There are two
types: int and ref, corresponding to the two kinds of values in V. We assume a set P Q pname
of procedure names, where a procedure’s name also determines its list of argument types
and its return type. Programs are organised into a finite set of procedures, indexed by their
name and individually consisting of lists of instructions from the following collection:
      ι :: iconst z | ibinop op | pop | load n | store n | aconst null
            | binarycmp cmp offset | unarycmp cmp offset | ifnull offset | goto offset
            | new desc | getfield fnm | putfield fnm | free desc | consume r
            | return | call pname
These instructions—apart from consume—are standard, so we only briefly explain them.
Inside each activation frame, the virtual machine maintains an operand stack and a collec-
tion of local variables, both of which contain values from the semantic domain V. Local
variables are indexed by natural numbers. The instructions in the first two lines of the
list perform the standard operations with the operand stack, local variables and program
counter. The third line includes instructions that allocate, free and manipulate structures
stored in the heap. The instruction consume r consumes the resource r. The desc argument
to new and free describes the structure to be created on the heap by the fields and their
types. The fourth line contains the procedure call and return instructions that manipulate
the stack of activation frames.
     Individual activation frames are tuples xcode, S, L, pc y P Frm consisting of the list of
instructions from the procedure being executed, the operand stack and local variables, and
the program counter. The first two lines of instructions that we gave above only operate
within a single activation frame and have no effect on the heap or consumable resources, so
we give their semantics as a small-step relation between frames: ÝÑ  Frm  Frm defined
                                                                    frm

in Figure 2. The rules make use of semantic interpretations JopK and JcmpK of binary
operations and binary relations on integers.
     The third line of instructions contains those that manipulate the heap and consume
resources. Their small-step operational semantics is modelled by a relation ÝÑ  Frm 
                                                                                mut

H  Frm  H  R, which relates the before and after activation frames and heaps, and
states the consumable resource consumed by this step. The rules defining this relation are
given in Figure 3. The rules for the instructions new and free take a parameter desc. This
parameter describes the fields and their types for the object to be allocated or deallocated.
                   AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                                          11




For a description desc  xfnm 1 : τ1 , ..., fnm n : τn y, we have written H ra ÞÑ desc s to denote a
heap updated with pa, fnm i q ÞÑ default pτi q, where default pintq  0 and default pref q  null .
For the free instruction, H zxa, desc y denotes the removal of all elements with keys pa, fnm i q
in H.


                                           code rpc s  iconst z
                              xcode, S, L, pc y ÝÑ
                                                frm
                                                    xcode, z :: S, L, pc       1y

                                          code rpc s  ibinop op
                xcode, z1 :: z2 :: S, L, pc y ÝÑ
                                              frm
                                                  xcode, pJopK z1 z2 q :: S, L, pc          1y

                code rpc s  pop                                  code rpc s  load n        Lrns  v
 xcode, z :: S, L, pc y ÝÑ xcode, S, L, pc
                       frm
                                                 1y         xcode, S, L, pc y ÝÑ xcode, v :: S, L, pc
                                                                             frm
                                                                                                             1y

                                            code rpc s  store n
                       xcode, v :: S, L, pc y ÝÑ
                                              frm
                                                  xcode, S, Lrn ÞÑ vs, pc            1y

                                          code rpc s  aconst null
                             xcode, S, L, pc y ÝÑ
                                               frm
                                                   xcode, null :: S, L, pc      1y

                        code rpc s  binarycmp cmp offset              z1 JcmpK z2
                         xcode, z1 :: z2 :: S, L, pc y ÝÑ
                                                       frm
                                                           xcode, S, L, offset y
                     code rpc s  binarycmp cmp offset           pz1 JcmpK z2 q
                        xcode, z1 :: z2 :: S, L, pc y ÝÑ xcode, S, L, pc 1y
                                                        frm



                         code rpc s  unarycmp cmp offset               z JcmpK 0
                               xcode, z :: S, L, pc y ÝÑ xcode, S, L, offset y
                                                      frm



                       code rpc s  unarycmp cmp offset              pz JcmpK 0q
                              xcode, z :: S, L, pc y ÝÑ
                                                     frm
                                                         xcode, S, L, pc 1y
    code rpc s  ifnull offset        a  null                 code rpc s  ifnull offset        a  null
 xcode, a :: S, L, pc y ÝÑ xcode, S, L, offset y
                       frm
                                                            xcode, a :: S, L, pc y ÝÑ xcode, S, L, pc
                                                                                    frm
                                                                                                             1y

                                          code rpc s  goto offset
                                 xcode, S, L, pc y ÝÑ
                                                   frm
                                                       xcode, S, L, offset y
                      Figure 2: Intra-frame Operational Semantics Rules
12                                                        R. ATKEY




                                code rpc s  new desc    pfnm. pa, fnm q R H q
                      xcode, S, L, pc y, H ÝÑ xcode, a :: S, L, pc 1y, H ra ÞÑ desc s, e
                                                mut



                                     code rpc s  getfield fnm           H ra, fnm s  v
                           xcode, a :: S, L, pc y, H ÝÑ xcode, v :: S, L, pc
                                                          mut
                                                                                            1y, H, e

                                                code rpc s  putfield fnm
                 xcode, a :: v :: S, L, pc y, H ÝÑ
                                                mut
                                                    xcode, S, L, pc              1y, H rpa, fnm q ÞÑ v s, e

                                                  code rpc s  free desc
                       xcode, a :: S, L, pc y, H ÝÑ
                                                 mut
                                                     xcode, S, L, pc              1y, H zxa, desc y, e

                                                 code rpc s  consume r
                                xcode, S, L, pc y, H ÝÑ
                                                     mut
                                                         xcode, S, L, pc              1y, H, r

                Figure 3: Heap and Resource Mutating Operational Semantics Rules



                            f ÝÑ f 1                                           f, H ÝÑ f 1 , H 1 , rc
                               frm                                                    mut


            xr, H, f :: fs y ÝÑ
                             prg
                                 xr, H, f 1 :: fs y                xr, H, f :: fs y ÝÑ
                                                                                    prg
                                                                                        xr  rc , H 1 , f 1 :: fs y
                                                      code rpc s  return
     xr, H, xcode , v :: S, L, pc y :: xcode 1 , S 1, L1 , pc 1 y :: fs y ÝÑ
                                                                          prg
                                                                              xr, H, xcode 1 , v :: S 1, L1 , pc 1 y :: fs y
                                code rpc s  call pname              prg rpname s  code 1
 xr, H, xcode , args          S, L, pc y :: fs y ÝÑ xr, H, xcode 1 , rs, xargs y, 0y :: xcode, S, L, pc            1y :: fs y
                                                  prg



                             Figure 4: Small-step Operational Semantics Rules

     Note that all the rules in the ÝÑ relation apart from the consume instruction consume
                                                mut

no resources: e is the identity element of our resource monoid.
     A state of the full virtual machine is a tuple xr, H, fs y P State, where r is the resource
consumed to this point, h is the current heap, and fs is a list of activation frames. The small-
step operational semantics of the full machine for some program prg is given by a relation
ÝÑ
 prg
       State  State which incorporates the ÝÑfrm
                                                    and ÝÑ relations and also describes how
                                                         mut

the call and return instructions manipulate the stack of activation frames. The rules defining
this relation are presented in Figure 4. In the rule for the instruction call, the operation
denotes list concatenation, rs denotes the empty list and xy denotes the translation of a
list to a finite map from natural numbers in the obvious way.
     Finally, we use the predicate s Ó H, r, v to indicate when a return instruction is to be
executed and there is only one activation frame on the stack. In this case execution of the
                  AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                             13




program terminates. The H, r and v are the final heap, the total consumed resources and
the return value of the program respectively.

3.3. Assertions. Every procedure pname in the program is annotated with a precondi-
tion and a post-condition. To allow for variables that are universally quantified over both
the pre- and post-condition we make use of Coq’s dependent types to augment procedure
specifications with a specific “environment” type. A procedure specification is a dependent
triple:
                  xE : Type, P  E  V  H  R, Q  E  V  H  R  Vy
     Preconditions P are predicates over E  V  H  R: environments, lists of arguments to
the procedure and the heap and available resource at the start of the procedure’s execution.
Post-conditions are predicates over E  V  H  R  V: environments, argument lists and
the heap, remaining consumable resource and return value.
     Intermediate assertions in our program logic are predicates over E  V  H  R  V 
pN á Vq: environments, argument lists, the heap, remaining consumable resource and the
current operand stack and local variable store. Intermediate assertions are the assertions
that are attached to every instruction in the body of a procedure by our program logic and
specify a sufficient precondition for safely executing that instruction and all of its successors.
     Note that each of the three different types of assertions talks about the remaining
consumable resources available to the program, not the resources that have already been
consumed.

3.4. Program Logic. A proof that a given procedure’s implementation code matches its
specification xE, P, Qy consists of a map C from instruction offsets in code to assertions such
that:
(1) Every instruction’s assertion is suitable for that instruction: for every instruction offset
    i in code, there exists an assertion A such that C $Q tAu ñ i:code ris, and C ris implies
    A. Figure 5 gives the definition of the judgement C $Q tAu ñ i:ι for a selected subset
    of the instructions ι. The post-condition Q is used for the case of the return instruction.
    We explain the definition of this judgement in more detail below.
(2) The precondition implies the assertion for the first instruction: for all environments
    env P E, arguments args, heaps H and consumable resources r, we have
                       P pe, args , H, r q ñ C r0spenv , args, H, r, rs, xargs yq
     where rs denotes the empty operand stack, and xy maps lists of values to finite maps
     from naturals to values, as in the operational semantics in Figure 4.
When condition 1 holds, we write this as C $ code : Q, indicating that the procedure
implementation code has a valid proof C for the post-condition Q.
     The rules in Figure 5 are an illustrative subset of the rules of the program logic. The
rule for iconst merely states that the precondition for executing this instruction is the
precondition of the next instruction with the specified integer pushed on to the stack. The
rules for most of the other intra-frame, non-mutating instructions are similar. Slightly
different are the rules for the conditional instructions, for example ifnull; these make use of
logical conjunction to make sure that both possible outcomes of the conditional have their
preconditions satisfied.
14                                                  R. ATKEY




     C $Q tλpenv , args, r, H, S, Lq. C ri          1spenv , args, r, H, z :: S, Lqu ñ i:iconst z
            $                                                                        ,
            '
            '     p
              λ env , args, r, H, S, L . q                                /
                                                                          /
            &               1          1
                      a, S .S  a :: S ñ                                 .
     C $Q                                                                   ñ i:ifnull n
            '
            '           pa  null ñ C ri 1spenv , args, r, H, S 1 , Lqq^ /
                                                                          /
            %
                        pa  null ñ C rnspenv , args, r, H, S 1 , Lqq     -

            $                                                                    ,
            '     p
            ' λ env , args, r, H, S, L .     q                                   /
                                                                                 /
                 a, v, S 1 .
                      
            '
            '                                                                    /
                                                                                 /
            &                                                                    .
     C $Q                 S  a :: v :: S 1 ^                                    ñ i:putfield fnm
            '
            '
            '
            '             pa, fnm q P H ^                                      /
                                                                               /
                                                                               /
                                                                               /
                          C ri 1spenv , args, r, H rpa, fnm q ÞÑ v s, S 1 , Lq
            %                                                                  -

            "                                                                    *
                λpenv , args, r, H, S, Lq.
     C $Q                                                                            ñ i:consume rc
                  Dr1 . rc  r1  r ^ C ri       1spenv , args, r 1 , H, S, Lq
            $                                                                            ,
            '
            '     p
              λ env , args, r, H, S, L .     q                                           /
                                                                                         /
                 args 1 S 1 .S args 1 S 1
                                                  ñ
            '
            '                                                                            /
                                                                                         /
            '
            '                                                                            /
                                                                                         /
                   env 1 Ep , H1 , r1 , H2 , r2 .
                          D       P p                 qp         q
            '
            '                                                                            /
                                                                                         /
            '
            '                                                                            /
                                                                                         /
            '
            '
            &                  p          qp
                      R H1 , r1 H2 , r2 H, r          qp q^                              /
                                                                                         /
                                                                                         .
     C $Q                     Pp penv 1 , args 1 , H1 , r1 q^                          ñ i:call p
            '
            '
            '
            '                 v, pH11 , r11 q.                                      /
                                                                                     /
                                                                                     /
                                                                                     /
                                H11 #H2 ñ
            '
            '                                                                        /
                                                                                     /
            '
            '                                                                        /
                                                                                     /
            '
            '
            '
                                            1       1    1   1
                                Qp penv , args , H1 , r1 , v q ñ
                                                                                     /
                                                                                     /
                                                                                     /
            '                                              1   1   1           1     /
            %
                                C ri 1spenv , args , r1  r2 , H1 Z H2 , v :: S , Lq -

     C $Q tλpenv , args, r, H, S, Lq.v, S 1 . S  v :: S 1 ñ Qpenv , args, r, H, v qu ñ i:return

                                  Figure 5: Program Logic Rules (Extract)

     The rules for putfield and consume demonstrate heap and consumable resource con-
sumption respectively. For putfield, the heap is judged to be satisfactory if it contains the
address and field that are to be mutated. For resource consumption, we must “subtract”
the consumed resource from the current resource that has been supplied. If the desired
resource is not present then this instruction’s precondition will not hold.
     The rule for the call instruction demonstrates how the heap and the consumable re-
sources are dealt with similarly for the purposes of a frame rule. The current heap and
consumable resources are split into two parts pH1 , r1 q and pH2 , r2 q, with the first part be-
ing handed off to the callee for it to be mutated. Finally, the precondition of the return
instruction is directly derived from the post-condition of the current procedure.

3.5. Soundness. Soundness for the program logic is stated as the preservation of a safety
invariant by every step of the virtual machine. We define safety for activation frames, frame
stacks and whole machine states, each building on the last.
                    AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                                   15




     We say that an activation frame is safe if there is a proof for the code being executed
in the frame such that the requirements of the next instruction to be executed are satisfied.
Formally, a frame f  xcode, S, L, pc y is safe for environment env P E, arguments args, heap
H, resource r and post-condition Q, written safeFrame penv , f, H, r, args , Qq if3:
(1) There exists a certificate C such that C $ code : Q;
(2) C rpc s exists and C rpc spenv , args, r, H, S, Lq holds.
Safety of activation frames is preserved by steps in the virtual machine:
Lemma 3.1 (Intra-frame safety preservation).
(1) If
    (a) safeFrame penv , f, H, r, args , Qq
    (b) f ÝÑ f 1
           frm

    then safeFrame penv , f 1 , H, r, args , Qq.
(2) If
    (a) safeFrame penv , f, H1 , r, args , Qq
    (b) H1 #H2 and H1 Z H2  H
    (c) f, H ÝÑ f 1 , H 1 , rc
                mut

    then there exists H11 and r 1 such that
    (a) H11 #H2 and H11 Z H2  H 1
    (b) rc  r 1  r
    (c) safeFrame penv , f 1 , H11 , r 1 , args, Qq.
The second part of this lemma states that if we take a step that mutates the heap or
consumes some resource, and the activation frame has been certified as safe for a sub-part
of the heap, then the rest of the heap—H2 —is unaffected by a single step of execution in
this activation frame, and the new state of the activation frame is safe for the mutated heap
and new amount of consumable resources.
Remark 3.2. We pause for a moment to consider the relationship between our program
logic and traditional Separation Logic. The second part of the previous lemma effectively
states that execution steps for mutating instructions are local: for any other piece of heap
that is present but not mentioned in its precondition, the execution of a mutating instruction
will not affect it. This is usually expressed in Separation Logic by the frame rule that states
if we know that tP uC tQu holds, then tP  RuC tQ  Ru holds for any other resource assertion
R. We do not have an explicit frame rule in our program logic; application of the rule is
implicit in the rule for the call instruction (so, conflatingly, the frame rule is applied for
new activation frames). We do not have access to the frame rule in order to modularly
reason about the internals of each procedure, e.g. local reasoning about individual loops.
This is partially a consequence of the unstructured nature of the bytecode that we are
working with. It has not been a hindrance in small examples that we have verified so far,
but may well become so in larger procedures with multiple loops that need invariants—see
Section 2.2 for an example. In such cases it may be useful to layer a hierarchical structure,
matching the loops or other sub-program structure, on top of the unstructured bytecode in
order to apply frame rules and facilitate local reasoning inside procedures.
   3In this definition, and all the later ones in this section, we have omitted necessary assertions about
well-typedness of the stack, local variables and the heap because they would only clutter our presentation.
16                                                R. ATKEY




      We have now handled all the instructions except the call and return instructions that
create and destroy activation frames. To state soundness of our program logic for these we
need to define what it means for a stack of activation frames to be safe. Intuitively, a stack of
activation frames is a bridge between the overall arguments args top and post-condition Qtop
for the program and the arguments args cur and post-condition Qcur for the current activa-
tion frame, with respect to the current heap H and available consumable resources r, such
that, when the current activation frame finishes, its calling frame on the top of the stack is
safe. We write this as safeStack Ecur ,Etop pfs, H, r, env cur , args cur , Qcur , env top , args top , Qtop q.
The types Ecur and Etop refer to the environment types for the current and top-level pro-
cedures respectively, and env cur P Ecur , env top P Etop are the specific elements being used.
      Accordingly, we say that the empty frame stack is safe when r  e, H  emp, env cur 
env top , args cur  args top and Qcur  Qtop . A non-empty frame stack fs  xcode, S, L, pc y ::
fs 1 is safe when there exist pH1 , r1 q, pH2 , r2 q, env , args, Q and C, A such that:
(1) RpH1 , r1 qpH2 , r2 qpH, r q;
(2) The code is certified: C $ code : Q;
(3) The next instruction to be executed has precondition A: C rpc s  A;
(4) When the callee returns, the instruction’s precondition will be satisfied: for all v P
      V, H21 , r21 such that H21 #H1 and Qcur penv cur , args cur , H21 , r21 , v q holds, Apenv , args, r21 
      r1 , H21 Z H1 , v :: S, Lq holds as well.
(5) The rest of the frame stack fs will be safe when this activation frame returns:
      safeStack pfs, H2 , r2 , env , args, Q, env top , args top , Qtop q.
Note how the safeStack predicate divides up the heap and consumable resource between the
activation frames on the call stack; each frame hands a piece of its heap and consumable
resource off to its callees to use. This mirrors the formulation of the rule for call in the
program logic in Figure 5.
      Finally, we say that a state s  xrc , H, fs y is safe for environment env , arguments args,
post-condition Q and maximum resource rmax , written safeState ps, env , args, Q, rmax q, if:
(1) there exists an rfuture such that rc  rfuture  rmax ; and also
(2) rfuture and H split into pH1 , r1 q and pH2 , r2 q, i.e. RpH1 , r1 qpH2 , r2 qpH, rfuture q;
(3) there exists at least one activation frame: fs  f :: fs 1 and environment env cur , argu-
      ments args cur and post-condition Qcur ; such that
(4) safeFrame pf, H1 , r1 , env cur , args cur , Qcur q; and
(5) safeStack pfs, H2 , r2 , env cur , args cur , Qcur , env , args, Qq.
The key point in the definition of safeState is that the assertions of the program logic talk
about the resources that will be consumed in the future of the program’s execution. Safety
for a state says that when we combine the future resource requirements rfuture with resources
that have been consumed in the past, rc , then the total is less than the total resources rmax
that are allowed for the execution.
Theorem 3.3 (Soundness). Assume that all the procedures in prg match their specifications.
(1) If
    (a) safeState ps, env , args, Q, rmax q; and
    (b) s ÝÑ s1
           prg

    then safeState ps1 , env , args, Q, rmax q.
(2) If safeState ps, env , args, Q, rmax q and s Ó H, r, v, then there exists an r 1 such that
    Qpenv , args, H, r 1 , v q and r  r 1  rmax .
                 AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                          17




In the halting case in this theorem, the existentially quantified resource r 1 indicates the
resources that the program still had available at the end of its execution. We are also
guaranteed that when the program halts, the total resource that it has consumed will be
less than the fixed maximum rmax that we have set, and moreover, by item 1 of the theorem,
this bound has been observed at every step of the computation.
Remark 3.4. Though we assumed it above, the proof of soundness of the program logic does
not require that the monoid of resources is commutative. This opens the way to considering
non-commutative notions of resource, such as traces. However, constructing a usable proof-
theory for a mixed commutative/non-commutative notion of resource (i.e. heaps and a
putative non-commutative consumable resource) is hard. Also, the resource acquisition
variant of the program logic that we describe in the next section requires commutativity.


3.6. Allowing for Resource Acquisition. The operational semantics and program logic
described above assume a fixed total amount of resource that may be consumed by the
program. The precondition of the main procedure of the program specifies the amount of
resource that will be required for the entire run. In this section we consider the changes
necessary to support dynamic but fallible acquisition of resources via a special acquire
instruction. We provide an example use of this additional capability in Section 3.7.
     We assume that there is a capricious environment that entertains requests for additional
resources from programs. Requests may be granted or denied. A program may request an
additional resource using a special acquire instruction. To make things interesting, and
to allow for the example in the next section, we make the resource requested by acquire
dynamic and correspondingly modify consume, removing its static argument:
                                 ι :: ... | consume | acquire
For both instructions, we assume that the resource being consumed or requested is indicated
by an integer value on the stack. For the acquire instruction the intended semantics is that
if the request is granted then a 1 is pushed on to the operand stack, otherwise a 0 is pushed.
     For the operational semantics, we modify the relation ÝÑ to have an additional “ac-
                                                              mut

quired resources” component:
                              f, H ÝÑ f, H, rconsumed , racquired
                                   mut

For each of the existing heap mutating instructions except consume, the acquired resource
is equal to the unit of the resource monoid, e. The operational semantics of consume is
replaced by the following rule to reflect the dynamic resource identification:
                                    code rpc s  consume
               xcode, z :: S, L, pc y, H ÝÑ
                                         mut
                                             xcode, S, L, pc 1y, H, respzq, e
where we assume the existence of a function res : Z Ñ R that names certain consumable
resources in R by integers. We do not assume that res is a monoid homomorphism. Two
new operational semantics rules are added for the acquire instruction, for the two possible
18                                            R. ATKEY




outcomes of requesting more resource:
                                         code rpc s  acquire
                xcode, z :: S, L, pc y, H ÝÑ
                                          mut
                                              xcode, 1 :: S, L, pc   1y, H, e, respz q

                                         code rpc s  acquire
                  xcode, z :: S, L, pc y, H ÝÑ
                                            mut
                                                xcode, 0 :: S, L, pc 1y, H, e, e
States of the virtual machine are modified to be four-tuples xrcon , rtot , H, f sy of consumed
resources, total allowed resources, current heap and current activation frame stack. The
invariant that is now to be maintained is that the rcon is always less than or equal to rtot .
The only rule from Figure 4 that is modified (apart from threading through the unchanged
rtot ) is the rule incorporating ÝÑ into the relation:
                                 mut


                                       f, H ÝÑ f 1 , H 1 , rc , ra
                                             mut


                     xr, rtot , H, f :: fs y ÝÑ
                                             prg
                                                 xr  rc , rtot  ra , H 1 , f 1 :: fs y
The halting predicate is extended to a five-place relation s Ó H, rcon , rtot , v, where rcon is
the total consumed resource of the execution and rtot is the total acquired resource.
     Perhaps surprisingly, the assertions (pre- and post-conditions and instruction level as-
sertions) are left unchanged, as are the rules of the logic from Figure 5 for the original set
of instructions. We modify the rule for resource consumption to take into account the new
dynamic nature:
              $                                                              ,
                   p
              & λ env , args, r, H, S, L .    q                              .
       C $Q            z, S 1 . S  z :: S 1 ñ Dr1.                           ñ i:consume
              %                     1                           1      1
                         respz q  r  r ^ C ri 1spenv , args, r , H, S , Lq
                                                                             -

and we add a new rule for resource acquisition:
      $                                                                                  ,
      &                         z, S 1 . S  z :: S 1 ñ                            .
C $Q λpenv , args, r, H, S, Lq.   C ri 1spenv , args, r  respz q, H, 1 :: S 1 , Lq   ñ i:acquire
    %                                                                 1
                                  ^ C ri 1spenv , args, r, H, 0 :: S , Lq           -

This exactly mirrors the pair of operational semantics rules. An acquire instruction is safe to
run if it is safe the execute the next instruction either with additional available consumable
resource and a 1 on the stack, or with no additional consumable resource and a 0 on the
stack.
    The definition of safe frame remains unchanged from above, and the statement of the
second item of Lemma 3.1 is adjusted to account for the possibility of additional resources
being acquired:
Lemma 3.5 (Intra-frame safety preservation (Resource Acquisition Variant)).
(2) If
    (a) safeFrame penv , f, H1 , r, args , Qq
    (b) H1 #H2 and H1 Z H2  H
    (c) f, H ÝÑ f 1 , H 1 , rc , ra
                mut

    then there exists H11 and r 1 such that
    (a) H11 #H2 and H11 Z H2  H 1
    (b) rc  r 1  r  ra
    (c) safeFrame penv , f 1 , H11 , r 1 , args, Qq.
                   AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                            19




The definition of the safeStack predicate remains the same as before, and the safeState
predicate is modified to be of the form safeState ps, env , args, Qq: the original rmax argument
is taken to be the rtot from the state. The key safety property, as before, is that the consumed
resources, plus the future resources, is less than or equal to the total allowed resources. But
now the total resources allowed may be increased during execution.
     The new version of Theorem 3.3 is as follows:
Theorem 3.6 (Soundness (Resource Acquisition Variant)). Assume that all the procedures
in prg match their specifications.
(1) If
    (a) safeState ps, env , args, Qq; and
    (b) s ÝÑ s1
           prg

    then safeState ps1 , env , args, Qq.
(2) If safeState ps, env , args, Qq and s Ó H, rcon , rtot , v, then there exists an r 1 such that
    Qpenv , args, H, r 1 , v q and rcon  r 1  rtot .
This theorem gives a comparable guarantee to Theorem 3.3, in that the (now dynamic)
resource bound is respected at every step of the computation and at the end of execution.
By inspection of the operational semantics, we can see that the resource bound may only
be increased by successful execution of an acquire instruction.

3.7. Resource Acquisition Example. To illustrate the utility of the language and logic
extended with resource acquisition, we take the example of block booking as presented by
Aspinall, Maier and Stark [4]. The scenario is that an application running on a mobile
device has a list of telephone numbers that it wants to send SMS messages to. Permission
must be sought from the user to send these messages, since sending incurs a monetary
cost. It is not necessarily convenient to request permission from the user when the message
is to be sent, so permission is requested in advance. We use the program logic extended
with resource acquisition to bridge the gap between the acquisition of permission and its
consumption, ensuring that no attempt is made to perform an operation that has not been
authorised. In this scenario, the acquire instruction is implemented by actually requesting
permission from the user.
     Figure 6 shows the code for a method, requestPermissions, that loops through a list
of telephone numbers, requesting permission for each one. We assume that the calls to the
method acquire are compiled to instances of the acquire instruction. We have taken the
liberty of assuming a value type of telephone numbers rather than re-using the int type.
The result of the resource acquisition attempt is stored in the permission field of the record
for that telephone number.
     The specification of the precondition of requestPermissions is simply that there is a
proper linked list on the heap, using the following inductively defined predicate:
 lsegpx, y q  px  y ^ empq _ pDn, p, z. rx     ÞÑ ns  rx permission
                                                               ÞÑ ps  rx next
                                                                          ÞÑ zs  lsegpz, yqq
                                               number

In the post-condition, we make use of another inductively defined predicate that states the
resources available, dependent on the value of the permission field:
  lsegsend px, y q    px  y ^ empq
                       _ pDn, z. rx number          ÞÑ 1s  Rsendpnq  rx next
                                      ÞÑ ns  rx permission               ÞÑ zs  lsegpz, yqq
                       _ pDn, z. rx ÞÑ ns  rx ÞÑ 0s  rx ÞÑ zs  lsegpz, yqq
                                    number       permission   next
20                                          R. ATKEY




class PhoneNumberNode {
     public PhoneNumber     number;
     public boolean         permission;
     public PhoneNumberNode next;
}

...

public static void requestPermissions (PhoneNumberNode phoneNumber) {
     while (phoneNumber != null) {
          phoneNumber.permission = acquire (phoneNumber.number);
          phoneNumber = phoneNumber.next;
     }
}

                           Figure 6: Resource Acquisition Example

Thus when the permission field has the value 1, the list node is associated with the
permission to send to that telephone number; and when the permission field has the value
0, no such associated permission is available. We revisit this kind of conditionally-resource-
carrying predicate in Section 4.2.
    Re-interpreting the consume instruction as sending an SMS message, a loop that sends
messages to all telephone numbers that the user has approved now looks much like the
simple list iteration example from the introduction, augmented with a dynamic check to
ensure that permission has been sought and received.

                                  4. Deep Assertion Logic
In the previous section we described a program logic but remained agnostic as to the exact
form of the assertions save that they must be predicates over certain domains. This shallow
approach makes the statement and soundness proof easier, but inhibits discussion of actual
specifications and proofs in the logic. In this section we show how a combination of two
variants of the logic of Bunched Implications (BI) [20, 22] can be used to provide a syntax
for assertions in our program logic. We combine boolean BI with affine intuitionistic BI,
for describing heaps and consumable resources respectively.

4.1. Syntax and Semantics. We made use of three different types of assertion for the
program logic: procedure pre- and post-conditions, and intermediate assertions within pro-
cedures. These all operate on heaps and consumable resources and the arguments to the
current procedure, but differ in whether they talk about return values or the operand stack
and local variables. To deal with these differences we assume that we have a set of terms in
our logic, ranged over by t, t1 , t2 , ..., that at least includes logical variables and a constant
null for representing the null reference, and also variables for representing the current proce-
dure arguments, the return value and the operand stack and local variables as appropriate.
                   AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                                  21




            η, x |ù J          iff always
            η, x |ù t1 ' t2    iff Jt1 Kη ' Jt2 Kη
            η, x |ù emp        iff x  pH, r q and H  tu
            η, x |ù rt1 ÞÑ t2 s iff x  pH, r q and H  tpJt1 Kη , f q ÞÑ Jt2 Kη u
                         f

            η, x |ù Rri         iff x  pH, r q and ri  r and H  tu
            η, x |ù φ1 ^ φ2 iff η, x |ù φ1 and η, x |ù φ2
            η, x |ù φ1 _ φ2 iff η, x |ù φ1 or η, x |ù φ2
            η, x |ù φ1  φ2 iff exists y, z. st. Ryzx and η, y |ù φ1 and η, z |ù φ2
            η, x |ù φ1 Ñ φ2 iff for all y. if x  y and η, y |ù φ1 then η, y |ù φ2
            η, x |ù φ1 — φ2 iff for all y, z. if Rxyz and η, y |ù φ1 then η, z |ù φ2
            η, x |ù v.φ        iff for all a, η rv ÞÑ as, x |ù φ
            η, x |ù Dv.φ        iff exists a, η rv ÞÑ as, x |ù φ

                                 Figure 7: Semantics of assertions

    Formulae are built from at least the following constructors:
  φ ::   J | t1 ' t2 | φ1 ^ φ2 | φ1 _ φ2 | φ1 Ñ φ2 | emp | φ1  φ2 | φ1 — φ2 | x.φ | Dx.φ
          | rt1 ÞÑf t2s | Rr | . . .
Where ' P t, u. We can also add inductively defined predicates as needed, see Section 4.2
below. The only non-standard formula with respect to Separation Logic is Rr which rep-
resents the presence of some consumable resource r. The semantics of the assertion logic
is given in Figure 7 as a relation |ù between environments and heap/consumable resource
pairs and formulae. We assume a sensible semantics JKη for terms in a given environment.
     As a consequence of having an ordering on consumable resources, and our chosen seman-
tics of emp,  and —, our logic contains affine intuitionistic BI as a sub-logic for reasoning
purely about consumable resources.
Proposition 4.1. If φ is a propositional BI formula with only Rr as atoms, then r |ùbi φ
iff η, pr, hq |ù φ.


4.2. Inductively Defined Shape and Resource Predicates. We now present some
inductively defined predicates that demonstrate how heap-resident data structures may have
resources associated with their nodes. We have introduced the resource-aware lseg predicate
that describes a segment of a list with a resource associated to every element:
        lsegpr, x, y q  px  y ^ empq _ pDd, z. rx ÞÑ ds  rx ÞÑ z s  Rr  lsegpr, z, y qq
                                                       data          next

An alternative that we made use of in the block booking example in Section 3.7 is to only
demand resources when the element data satisfies some predicate, for example when the
integer stored in the node is not equal to zero:
lseg0 pr, x, y q  px  y ^ empq _ pDd, z. rx ÞÑ ds  rx ÞÑ z s  pd  0 Ñ Rr q  lseg0 pr, z, y qq
                                                data          next

This kind of specification allows the conditional resource property to be specified locally
within the list structure. If we were attempting explicit resource accounting using sized
22                                             R. ATKEY




predicates, we would be forced to reflect the whole list into the logic and state the resource
requirement in terms of the number of non-zero elements:
                            lsegpl, x, y q ^ r  lengthpfilterpλx.x  0, lqq
Reasoning with such global list properties is obviously much harder than locally reasoning
about each individual node as it is processed by the program.
    The amortised approach is not limited to reasoning purely about singly-linked lists, the
standard doubly-linked list and tree predicates of Separation Logic can be easily augmented
with local resource annotations (we have omitted the data components of these predicates
to save space):
     dlsegpr, p, x, y q  px  y ^ empq _ pDz. rx ÞÑ z s  rx ÞÑ ps  Rr  dlsegpr, x, z, y qq
                                                      next        prev


             treepr, xq     px  null ^ empq
                             _ pDy, z. rx left
                                          ÞÑ ys  rx right
                                                      ÞÑ zs  Rr  treepyq  treepzqq
These predicates all describe resources that are linear in proportion to the sizes of the data
structures. Using the clever technique of Hoffmann and Hofmann [14], we can also present
lists with associated resources that are polynomially proportional to the length of the list,
by exploiting the presentation of polynomials using binomial coefficients. In their system,
lists are annotated with resources that are lists of rational numbers
                                                          °k      
                                                                        xp1, ..., pn y. The idea
                                                                n
is that a list of length n annotated with such a list has i1 i pi associated resource. We
can give such lists as an inductively defined predicate in our logic:
           lsegpÝ
                Ñp , x, zq  px  z ^ empq _ pDy. rx ÞÑ ys  Rp1  lsegp⊳pÑ
                                                                          Ýp q, y, zqq
                                                          next

where ⊳pÝ Ñp q  pp1 p2, p2 p3, ..., pk1 , pk q is the additive shift of a resource annotation
as defined by Hoffmann and Hofmann.

4.3. Heap and Resource Separation. In the logic of Section 4.1, we only made use of
one kind of separating conjunction, φ1  φ2 , that separates both heaps and consumable
resources. This allows the tight integration of the heap shapes of various data structures
and consumable resources as shown in the previous section. Evidently, there are two other
possible combinations that allow sharing of heap or resources. For example, separation of
resources, but sharing of heap:
               η, x |ù φ1  φ2 iff x  pH, r q and exists r1 , r2 . st.
                            R

                                     r1  r2  r
                                     and η, pH, r1 q |ù φ1 and η, pH, r2 q |ù φ2
This definition looks like it might be useful to specify that we have a single data structure
on the heap, but two resource views on it. A need for this kind of situation arose in the
merge-sort example in Section 2.2. There, the auxiliary procedure advance, that advances
a pointer a certain number of elements through a list, was given the specification:
                 Prepadvanceq : lsegpa0 , l, null q
                Postpadvanceq : lsegpa0 , l, retvalq  lsegpa0 , retval, null q
where a0 was an amount of resource associated with every element of the list that was to be
preserved. Note that advance does not modify the list in any way and does not consume
any resources. Evidently, this specification is satisfied for any a0 . In the spirit of Separation
Logic, we would like to be able to state the specification of advance without mentioning
                 AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                           23




resources—because it does not consume or release any—and combine the specification later
on with the fact that the list has some associated resources. So, we would like to give
advance the specification:
                 Prepadvanceq : lsegp0, l, null q
                Postpadvanceq : lsegp0, l, retvalq  lsegp0, retval, null q
since it does not require or yield any consumable resource, and then apply a putative
resource-frame rule:
                                       tP u C tQu
                                     tP R Ru C tQ R Ru
Where R would record that every element of the unmodified list has a0 associated resource.
As with the normal frame rule of Separation Logic, this turns what would be a second-order
universally quantified assertion into an unquantified assertion. This simplification is crucial
for developing automated procedures for discharging verification conditions as in Section 5.
For the present example, we can use linear programming to infer the instantiation of a0 ,
but for general complex composite resources, or for examples that require polymorphic
recursion, this problem could become much harder.
      Unfortunately, in order for this rule to be sound we must ensure that C does not modify
the heap in any way that would violate the resource associations. There is currently no
way to enforce this within the logic. In the example, this manifests itself as the inability to
guarantee that the list in the post-condition of advance has exactly the same shape as the
list in the precondition, which would be required to assign a resource to every element.

                               5. Automated Verification
In this section we describe a verification condition (VC) generation and proof search proce-
dure for automated verification of programs against specifications in the program logic, as
long as procedures have been annotated with loop invariants. The restricted subset of Sep-
aration Logic that we use in this section is similar to the subset used by Berdine et al. [6],
though instead of performing a forwards analysis of the program, we generate verification
conditions by backwards analysis and then attempt to solve them using proof search. We
develop our own proof search procedure rather than re-use an existing Separation Logic-
inspired tool in order to incorporate a key feature of Hofmann and Jost’s amortised system:
the use of linear programming to infer resource annotations [15]. In the system we present
here, the proof search procedure generates linear constraints that can be solved by linear
programming to infer resource annotations. A limitation of the VC-generate and solve tech-
nique we use here is the potential for exponential blow-up of the verification conditions in
the size of program. The forward symbolic execution approach deals with this by attempt-
ing to prune unreachable paths as soon as possible and merging similar feasible paths using
heuristics.

5.1. Restricted Assertion Logic. Following Berdine et al., we make use of a highly re-
stricted assertion logic that forbids arbitrary nesting of the additive and separating conjunc-
tions and disallows negative occurrences of implications. This makes proof search practical.
For the purposes of resource annotation inference, consumable resources are represented in
24                                            R. ATKEY




the restricted syntax as linear expressions over a collection of globally existentially quanti-
fied meta-variables. We use y1 , y2 , and so on for resource variables to be inferred, and x1 , x2 ,
etc. for logical variables. Resource variables cannot be quantified over inside formulae.
     The basic assertion of the proof search logic is of the form
                                        ª
                                             Dx. Πi | Σi | Θi
                                         i
where we use the meta-variable S to stand for such assertions. They consist of a finite
disjunction of clauses, each with a collection of existentially quantified variables and three
collections of assertions. The first portion, Π, contains assertions about pure (non-heap and
non-consumable resource) data, which are equalities and disequalities of the form:
                                      P :: t1  t2 | t1  t2
The terms that we allow in the data and heap assertions are either variables, or the constant
null. A collection Π  P1 , ..., Pn is interpreted by translation into the logic of Section 4 as
the additive conjunction of the Pi . The second portion, Σ, contains assertions about the
heap, which are of the form:
                                 X :: rt1 ÞÑ t2 s | lsegpΘ, t1 , t2 q
                                              f

Here we have made use of the inductively defined list segment predicate from Section 4.2.
A collection Σ  X1 , ..., Xn is interpreted as the separating (or multiplicative) conjunction
of the Xi . The final portion Θ is a linear expression indicating an amount of consumable
resource. It is easily possible to generalise this to multiple resources by considering multiple
named linear expressions. Given a valuation of the resource meta-variables yi , extended to
an interpretation JΘK this is interpreted in the logic of Section 4 as the formula RJΘKr for
some fixed resource r. A whole composite Π | Σ | Θ is interpreted as Π ^ pΣ  RJΘKr q.
    Finally, we have the set of goal formulae that the verification condition generator will
produce and the proof search will solve.
                G :: S  G | S — G | S | G1 ^ G2 | P Ñ G | x.G | Dx.G
Note that we only allow implications (Ñ and —) to appear in positive positions. This
means that we can interpret them in our proof search as adding extra information to the
context.

5.2. Verification Condition Generation. Verification condition generation is performed
for each procedure individually by computing weakest liberal preconditions for each instruc-
tion, working backwards from the last instruction in the method. To resolve loops, we
require that the targets of all backwards jumps have been annotated with loop invariants
S that are of the special form in the previous section. This assumes that the instructions
have been sorted into reverse post-order so we can scan the instructions in reverse order
to collect the verification conditions. We omit the rules that we use for weakest liberal
precondition generation since they are very similar to the rules for the shallowly embedded
logic in Figure 5. The verification condition generator will always produce a VC for the
entailment of the computed weakest liberal precondition of the first instruction from the
procedure’s precondition, plus a VC for each annotated instruction, being the entailment
between the annotation and the computed weakest liberal precondition. All VCs will have
a formula of the form S as the antecedent and a goal formula G as the conclusion.
                  AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                            25




    The verification condition generation procedure has been formalised within the Coq
proof assistant and proved sound with respect to the program logic in Section 3. By using
Coq’s module system [12] we have abstracted the verification condition generator over the
particular deep assertion logic used. We used Coq’s program extraction capabilities to
extract the verification condition generator and instantiated it with the proof search logic
described in this section.

5.3. Proof Search. The output of the verification condition generation phase is a collection
of problems of the form S $ G, which can each be reduced to a finite collection of sequents
of the form Π | Σ | Θ $ G. To discharge these proof obligations, we make use of the
I/O interpretation of proof search as defined for intuitionistic linear logic by Cervesato,
Hodas and Pfenning [9], along with heuristic rules for unfolding the inductive list segment
predicate. We augment the I/O model of resource accounting with an additional part
that collects linear constraints that may be fed into a integer linear program solver, to
automatically infer resource annotations.
     We use the following judgement form for proof search goals that collect linear con-
straints. Here C is a set of linear constraints over the resource meta-variables yi :
                                       Π | Σ | Θ $ GzC
The proof search procedure is defined by the rules shown in Figure 8, Figure 9, Figure 10
and Figure 11. These rules make use of several auxiliary judgements:
                 Π | Σ | Θ $ Σgoal z Σout , Θout , C Heap assertion matching
                         Θ $ Θgoal z Θout , C          Resource matching
                                 Π$K                   Contradiction spotting
                                 Π$Π   1               Data assertion entailment
The backslash notation used in these judgements follows Cervesato et al., where in the
judgement Θ $ Θgoal z Θout , C, the proof context Θ denotes the facts used as input and
Θout denotes the facts that are left over (the output) from proving Θgoal . The C component
collects the linear constraints that must hold for the judgement to give a valid separation
logic entailment. A similar interpretation is used for the heap assertion matching judgement.
We do not define the data entailment or contradiction spotting judgement explicitly here;
we intend that these judgements satisfy the basic axioms of equalities and disequalities.
     The rules in Figure 8 are the goal driven search rules. There is an individual rule
for each possible kind of goal formula. The first two rules are matching rules that match
a formula S against the context, altering the context to remove the heap and resource
assertions that S requires, as dictated by the semantics of the assertion logic. We must
search for a disjunct i that is satisfied by the current context. There may be multiple such
i, and in this case the search may have to backtrack. When the goal is a formula S, then
we ask that the left-over heap is empty, in order to detect memory leaks. Note that the
logical variables x1 , x2 , ... may not occur in the constraint sets, so we do not need to handle
universally quantified constraints.
     The matching rules make use of the heap and resource matching judgements defined
in Figure 9. The heap matching judgements take a data, heap and resource context and
attempt to match a list of heap assertions against them, returning the left over heap,
resources and computed constraints. The first three rules are straightforward: the empty
heap assertion is always matchable, points-to relations are looked up in the context directly
and pairs of heap assertions are split, threading the contexts through. For the list segment
26                                                  R. ATKEY




                            exists i, t.   Π | Σ | Θ $ Σi rt{xs z Σ1 , Θ1 , CH
                   Π $ Πi rt{xs      Θ $ Θi rt{xs z Θ2 , CR
                                         1                     Π | Σ 1 | Θ 2 $ G z CG
                                      
                                       ª
                          Π|Σ|Θ$              Dx. Πi | Σi | Θi  G z CH Y CR Y CG
                                         i

         exists i, t.     Π | Σ | Θ $ Σi rt{xs z emp, Θ1 , CH         Π $ Πi      Θ 1 $ Θ i z Θ 2 , CR
                                               ª
                                 Π|Σ|Θ$             Dx. Πi | Σi | Θi z CH Y CR
                                                i

           forall i, x.     Π, Πi | Σ, Σi | Θ       Θi $ G z C
                           
                            ª                                              Π, P | Σ | Θ $ G z C
            Π|Σ|Θ$               Dx. Πi | Σi | Θi     — G z C
                             i                                            Π | Σ | Θ $ P Ñ GzC

     Π | Σ | Θ $ G1 z C1    Π | Σ | Θ $ G2 z C2                Π | Σ | Θ $ GzC       x R fv pΠq Y fv pΣq
            Π | Σ | Θ $ G1 ^ G2 z C1 Y C2                                Π | Σ | Θ $ x.G z C

                                             Π | Σ | Θ $ Grt{xs z C
                                             Π | Σ | Θ $ Dx.G z C

                                  Figure 8: Goal Driven Search Rules

rules, there are three cases. Either the two pointers involved in the list are equal, in which
case we are immediately done; or we have a single list cell in the context that matches the
start pointer of the predicate we are trying to satisfy, and we have the required resources
for an element of this list, so we can reduce the goal by one step; or we have a whole list
segment in the context and we can reduce the goal accordingly. The resource matching
rule is where linear constraints are actually generated; to match a resource we subtract the
desired resource from the available resources and add a constraint to ensure that there was
enough resource to do this. Note that this rule always succeeds during proof search, but
may generate unsatisfiable constraints. Thus back-tracking may still be required.
     The final two sets of rules operate on the proof search context. The first set, shown
in Figure 10, describe how information flows from the heap part of the context to the data
part. If we know that two variables both have a points-to relation involving a field f, then
we know that these locations must not be equal. Similarly, if we know that a variable does
point to something, then it cannot be null. If any contradictions are found using these rules,
then the proof search can terminate immediately for the current goal. This is provided for
by the first rule in Figure 10.
     The final set of rules performs heuristic unfolding of the inductive lseg predicate. These
rules are shown in Figure 11. These rules take information from the data context and use
it to unfold lseg predicates that occur in the heap context. The first rule is triggered when
the proof search learns that there is a list segment where the head pointer of the list is
not equal to null. In this case, two proof search goals are produced, one for the case that
                 AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                                        27




                                         Heap Matching Rules:
                                                             Π $ t1  t11        Π $ t2  t12
        Π | Σ | Θ $ emp z Σ, Θ, tu                    Π | Σ, rt1 ÞÑ t2 s | Θ $ rt11 ÞÑ t12 s z Σ, Θ, tu
                                                                  f                   f



                 Π | Σ | Θ $ Σ 1 z Σ 1 , Θ 1 , C1 Π | Σ 1 | Θ 1 $ Σ 2 z Σ 2 , Θ 2 , C2
                            Π | Σ | Θ $ Σ 1  Σ 2 z Σ 2 , Θ 2 , C1 Y C2

                                              Π $ t1  t2
                                   Π | Σ | Θ $ lsegpΘl , t1 , t2 q z Σ, Θ, tu

        Π $ t1  t11      Θ $ Θ l z Θ 1 , CR            Π | Σ | Θ1 $ lsegpΘl , tn , t2 q z Σ1 , Θ2 , CH
             Π | Σ, rt1 ÞÑ tn s, rt1 ÞÑ td s | Θ $ lsegpΘl , t11 , t2 q z Σ1 , Θ2 , CR Y CH
                        next               data



                    Π $ t11  t1      Π | Σ | Θ $ lsegpΘl , t2 , t3 q z Σ1 , Θ1 , C
                    Π | Σ, lsegpΘl , t1 , t2 q | Θ $ lsegpΘl , t11 , t3 q z Σ1 , Θ1 , C

                                      Resource Matching Rule:

                                         Θ $ Θ1 zpΘ  Θ1 q, tΘ ¥ Θ1 u

                                         Figure 9: Matching Rules


                                                      Π$K
                                                 Π | Σ | Θ $ G ztu


                   Σ  rt1 ÞÑ ts, rt2 ÞÑ t1 s, Σ1  Π, t1  t2 | Σ | Θ $ G z C
                               f             f

                                        Π | Σ | Θ $ GzC

                        Σ  rt ÞÑ t1 s, Σ1    Π, t  null | Σ | Θ $ G z C
                                     f

                                         Π | Σ | Θ $ GzC

                                   Figure 10: Contradiction Flushing

the list segment is empty and one for when it is not. The other rules are similar; taking
information from the data context and using it to refine the heap context.
     The proof search strategy that we employ works by first saturating the context by
repeatedly applying the rules in Figure 10 and Figure 11 to move information from the data
context into the heap context and vice versa. This process terminates because there are a
finite number of points-to relations and list segment predicates to generate rule applications,
and when new predicates are introduced via list segment unfolding they either do not trigger
any new inequalities or are over fresh variables about which nothing is yet known. Once
28                                              R. ATKEY




                                           Π $ t1  null
     Π, t1  t2 | Σ | Θ $ G z C1     Π | Σ, rt1 ÞÑ xs, rt1 ÞÑ y s, lsegpR, x, t2 q | Θ, R $ G z C2
                                                 next          data

                              Π | Σ, lsegpR, t1 , t2 q | Θ $ G z C1 Y C2

     Π $ t1  null      Π, t2  null | Σ | Θ $ G z C             Π $ t1  t2       Π | Σ | Θ $ GzC
            Π | Σ, lsegpR, t1 , t2 q | Θ $ G z C                  Π | Σ, lsegpR, t1 , t2 q | Θ $ G z C

             Π $ t1  t2     Π | Σ, rt1 ÞÑ xs, rt1 ÞÑ y s, lsegpR, x, t2 q | Θ, R $ G z C
                                         next           data

                                 Π | Σ, lsegpR, t1 , t2 q | Θ $ G z C

                                 Figure 11: List Unfolding Rules

the context is fully saturated, the proof search reduces the goal by using the goal-driven
search rules and the process begins again.
    Given a collection of verification conditions and a successful proof search over them
that has generated a set of linear constraints, we input these into a linear solver, along with
the constraint that every variable is positive and an objective function that attempts to
minimise variables appearing in the precondition.
Theorem 5.1. The proof search procedure is terminating. Moreover, it is sound: if Π | Σ |
Θ $ G z C and there is an valuation of the y that satisfies C, then Π ^pΣ  RJΘKr q $ G under
this valuation using the translation of the proof search logic into the logic of Section 4 as
defined in Section 5.1.


                         6. Examples of Automated Verification

6.1. Small Examples. We have tested the automated resource inference procedure de-
scribed in the previous section on several small examples, including the simple loop itera-
tion example from the introduction and the examples from Section 2. We summarise these
examples in the following table. Note that the proof search procedure also verifies the mem-
ory safety of these examples. For timings, these tests were performed on an PC running
64-bit Ubuntu Linux 10.10 on an 8-core Intel Core i7 860 at 2.80GHz. Times were measured
using the GNU time utility. Our implementation only makes use of a single core.
                  AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                            29




     Name                    Property Inferred                                    Time (s)
     iterate list            Number of iterations is length of input list         0.010
     iterate recursive       Number of calls is length of input list              0.010
     copy list               Number of allocations is length of input list        0.013
     reverse                 Number of iterations is length of input list         0.012
     queue                   Resource annotations on enqueue and deqeueue         0.019
     frying pan              Number of times each element is visited              0.018
     mergesort               Number of comparisons is length of input list        0.037
     tree traverse           Number of calls is size of input tree                0.012
     tree copy               Number of allocations is size of input tree          0.014
     tree mirror             Number of calls is size of input tree                0.012
     In each of these examples, we seeded the program with loop invariants describing the
shape of heap data structures, but left our implementation to infer the resource bounds. The
last three examples involving trees make use of the inductive tree predicate from Section 4.2.
The proof search procedure was augmented with heuristic rules for matching and unfolding
instances of the tree predicate, following those for lists. The tree examples are all recursive
procedures.
     As can be seen from the table, the time taken for each of the examples is trivial. It
remains to be seen how well this technique scales to real-world code. It seems evident
that the VC-generate and solve process is not scalable in general due to the potential for
exponential blow-up in the size of the generated formulae. A more realistic implementation
of the program logic described in this paper would likely use the forward symbolic execution
approach, as described by Berdine et al. [6].

6.2. Frying Pan List Reversal. As a larger example, we demonstrate the use of the proof
search procedure coupled with linear constraint generation on the standard imperative in-
place list reversal algorithm on lists with cyclic tails (also known as “frying pan” lists). This
example was used by Brotherston, Bornat and Calcagno [7] to illustrate the use of cyclic
proofs to prove program termination. Here we show how our amortised resource logic can
be used to infer bounds on the time complexity of this procedure.
                                                           f
                               a         b         c           e

                                                         d

The “handle” of the structure consists of the nodes a, b, c and the “pan” consists of the
nodes d, e and f. When the in-place list-reversal procedure is run upon a structure of this
shape, it will proceed up the handle, reversing it, around the pan, reversing it, and then
back down the handle, restoring it to its original order. For the purposes of this example, we
assume that it takes one element of resource to handle the reversal of one node. Following
Brotherston, Bornat and Calcagno, we can specify a cyclic list in Separation Logic by the
following formula, where v0 points to the head of the list and v1 points to the join between
30                                                 R. ATKEY




the handle and the pan4.
                        Dk.lsegpx1 , v0 , v1 q  rv1 next
                                                     ÞÑ ks  lsegpx2 , k, v1 q  Rx   3


We have annotated the list segments involved with resource annotation variables x1 and x2
that we will instantiate using linear programming. The predicate Rx3 denotes any extra
resource we may require. Similarly, we have annotated the required loop invariant (adapted
from Brotherston et al.):
           pDk. lsegpa1 , l0 , v1 q  lsegpa2, l1 , null q  rv1 next
                                                                  ÞÑ ks  lsegpa3 , k, v1 q  Ra q
                                                                                               4


           _ pDk. lsegpb1 , k, null q  rj ÞÑ ks  lsegpb2, l0 , v1 q  lsegpb3 , l1 , j q  Rb q
                                             next                                              4


           _ pDk. lsegpc1 , l0 , null q  lsegpc2 , l1 , v1 q  rv1 next
                                                                    ÞÑ ks  lsegpc3 , k, v1 q  Rc q
                                                                                                   4


Each disjunct of the loop invariant corresponds to a different phase of the procedure’s
progress. Brotherston et al. note that it is possible to infer the shape part of this loop
invariant using current Separation Logic tools. Here, we have added the ability to infer
resource annotations, and hence bounds on the time consumption of the procedure. Running
our tool on this example produces the following instantiation of the variables:
      Precondition               x1  2 x2  1 x3  2
      Loop invariant, phase 1 a1  2 a2  1 a3  1 a4  2
      Loop invariant, phase 2 b1  1 b2  1 b3  0 b4  1
      Loop invariant, phase 3 c1  1 c2  0 c3  0 c4  0
      Post-condition             x11  0 x12  0 x13  0
Pictorially, the inference has associated the following amount of resource with each part of
the input structure:
                                                        f
                                    a          b          c      1       e

                                    2          2          2      d       1
                                                                 1
Each node of the handle has 2 associated elements of resource, to handle the two passes
of the handle that the procedure takes, while the pan has one element of resource for each
node. The inferred annotations for the loop invariant track how the resources on each node
are consumed by the procedure, gradually all reducing to zero. Since we have added a
consume instruction to be executed every time the procedure starts a loop, the resource
inference process has also verified the termination of this procedure, and given us a bound
on the number of times the loop will execute in terms of the shape of the input.

                                            7. Conclusions
We have presented a program logic that extends the resource reasoning capabilities of Sep-
aration Logic from reasoning about mutable resources such as the heap to consumable
resources such as time. We have demonstrated how doing so allows tight connections be-
tween the shape of data structures and the resources required to process them to be stated,
   4Note that the data part of the list node has been omitted in this formula and in the loop invariants to
reduce clutter.
                  AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                                31




and so expanding the reach of Separation Logic’s local reasoning principle to consumable
resources.
     We have presented an automated proof procedure that takes programs annotated with
shape invariants and infers consumable resource annotations. The main limitation of this
automated proof search procedure is that it only supports the statement and inference of
bounds that are linear in the size of lists that are mentioned in a procedure’s precondition.
This is a limitation shared with the original work of Hofmann and Jost [15]. We note that
this is not a limitation of the program logic that we have presented, only of the automated
verification procedure that we have layered on top. In Section 4.2 we presented a Separation
Logic version of the polynomial potential lists of Hoffmann and Hofmann [14], which opens
the way to inference of polynomial bounds for pointer manipulating list programs. Initial
experiments with extending our implementation in this direction have been promising.
     We have demonstrated that the use of mixed shape and resource assertions can sim-
plify the complexity of specifications that talk about resources, and this should extend to
extensions of the proof search procedure, or to interactive systems based on this program
logic. The resource aware program logic of Aspinall et al. [3] also uses the same layering:
a general program logic for resources (which is proved complete in their case) is used as a
base for a specialised logic for reasoning about the output of the Hofmann-Jost system.
     A possible direction for future work is to consider different assertion logics and their
expressiveness in terms of the magnitude of resources they can express. We conjecture that
the deep assertion logic we have presented here, extended with the lseg predicate can express
resources linear in the size of the heap. It would be interesting to consider more expressive
logics and evaluate them from the point of view of implicit computational complexity; the
amount of resource that one can express in an assertion dictates the amount of resource
that is available for the future execution of the program.
     Additional future work is to consider the proof theory of the combined Boolean BI and
affine intuitionistic BI that have used in this paper.
     Other resource inference procedures that are able to deal with non-linear bounds include
those of Chin et al. [10, 11], Albert et al. [1] and Gulwani et al. [13]. When dealing
with heap-based data structures, all of these techniques use a method of attaching size
information to assertions about data structures. As we demonstrated in Section 2.1, this can
lead to unwanted additional complexity in specifications. However, all of these techniques
deal with numerically bounded loops, which our current prototype automated procedure
cannot. We are currently investigating how to extend our approach to deal with non-linear
and numerically-driven resource bounds.
Acknowledgements I would like to thank Kenneth MacKenzie and Brian Campbell for
discussion and comments on this work. The ESOP 2010 and LMCS anonymous reviewers
also provided helpful suggestions. This work was funded by EPSRC Follow-on Fund grant
EP/G006032/1 “Resource Static Analysis” and EPSRC grant EP/G068917/1 “Categorical
Foundations for Indexed Programming”.

                                          References
[1] Elvira Albert, Puri Arenas, Samir Genaim, German Puebla, and Damiano Zanardini. COSTA: Design
    and Implementation of a Cost and Termination Analyzer for Java Bytecode. In Frank S. de Boer, Mar-
    cello M. Bonsangue, Susanne Graf, and Willem P. de Roever, editors, Formal Methods for Components
    and Objects, 6th International Symposium, FMCO 2007, Amsterdam, The Netherlands, October 24-26,
32                                              R. ATKEY




     2007, Revised Lectures, volume 5382 of Lecture Notes in Computer Science, pages 113–132. Springer,
     2007.
 [2] David Aspinall, Robert Atkey, Kenneth MacKenzie, and Donald Sannella. Symbolic and Analytic
     Techniques for Resource Analysis of Java Bytecode. In Martin Wirsing, Martin Hofmann, and Axel
     Rauschmayer, editors, Proceedings of 5th International Symposium on Trustworthy Global Computing
     (TGC 2010), volume 6084 of Lecture Notes in Computer Science, pages 1–22. Springer, 2010.
 [3] David Aspinall, Lennart Beringer, Martin Hofmann, Hans-Wolfgang Loidl, and Alberto Momigliano. A
     program logic for resources. Theor. Comput. Sci., 389(3):411–445, 2007.
 [4] David Aspinall, Patrick Maier, and Ian Stark. Safety guarantees from explicit resource management.
     In Frank S. de Boer, Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever, editors, Formal
     Methods for Components and Objects, 6th International Symposium, FMCO 2007, Amsterdam, The
     Netherlands, October 24-26, 2007, Revised Lectures, volume 5382 of Lecture Notes in Computer Science,
     pages 52–71. Springer, 2007.
 [5] Robert Atkey. Amortised Resource Analysis with Separation Logic. In Andrew Gordon, editor, ESOP
     2010: Proceedings of the 19th European Symposium on Programming Languages and Systems, volume
     6012 of Lecture Notes in Computer Science, pages 85–103. Springer, 2010.
 [6] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Symbolic execution with separation logic. In
     Kwangkeun Yi, editor, Programming Languages and Systems, Third Asian Symposium, APLAS 2005,
     Tsukuba, Japan, November 2-5, 2005, Proceedings, volume 3780 of Lecture Notes in Computer Science,
     pages 52–68. Springer, 2005.
 [7] James Brotherston, Richard Bornat, and Cristiano Calcagno. Cyclic proofs of program termination
     in separation logic. In George C. Necula and Philip Wadler, editors, Proceedings of the 35th ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2008, San Francisco,
     California, USA, January 7-12, 2008, pages 101–112. ACM, 2008.
 [8] F. Warren Burton. An efficient functional implementation of FIFO queues. Information Processing
     Letters, 14(5):205–206, 1982.
 [9] Iliano Cervesato, Joshua S. Hodas, and Frank Pfenning. Efficient resource management for linear logic
     proof search. Theor. Comput. Sci., 232(1-2):133–163, 2000.
[10] Wei-Ngan Chin, Huu Hai Nguyen, Corneliu Popeea, and Shengchao Qin. Analysing memory resource
     bounds for low-level programs. In Richard Jones and Stephen M. Blackburn, editors, Proceedings of
     the 7th International Symposium on Memory Management, ISMM 2008, Tucson, AZ, USA, June 7-8,
     2008, pages 151–160. ACM, 2008.
[11] Wei-Ngan Chin, Huu Hai Nguyen, Shengchao Qin, and Martin C. Rinard. Memory usage verification for
     oo programs. In Chris Hankin and Igor Siveroni, editors, Static Analysis, 12th International Symposium,
     SAS 2005, London, UK, September 7-9, 2005, Proceedings, volume 3672 of Lecture Notes in Computer
     Science, pages 70–86. Springer, 2005.
[12] Jacek Chrzaszcz. Implementing Modules in the Coq System. In David A. Basin and Burkhart Wolff,
     editors, Theorem Proving in Higher Order Logics, 16th International Conference, TPHOLs 2003, Rom,
     Italy, September 8-12, 2003, Proceedings, volume 2758 of Lecture Notes in Computer Science, pages
     270–286. Springer, 2003.
[13] Sumit Gulwani, Krishna K. Mehra, and Trishul M. Chilimbi. Speed: precise and efficient static estima-
     tion of program computational complexity. In Zhong Shao and Benjamin C. Pierce, editors, Proceedings
     of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL
     2009, Savannah, GA, USA, January 21-23, 2009, pages 127–139. ACM, 2009.
[14] Jan Hoffmann and Martin Hofmann. Amortized Resource Analysis with Polynomial Potential. In An-
     drew Gordon, editor, ESOP 2010: Proceedings of the 19th European Symposium on Programming Lan-
     guages and Systems, volume 6012 of Lecture Notes in Computer Science, pages 287–306. Springer, 2010.
[15] Martin Hofmann and Steffen Jost. Static prediction of heap space usage for first-order functional pro-
     grams. In Proceedings of the 30th ACM SIGPLAN-SIGACT symposium on Principles of Programming
     Languages, POPL ’03, pages 185–197, New York, NY, USA, 2003. ACM.
[16] Martin Hofmann and Steffen Jost. Type-Based Amortised Heap-Space Analysis. In Peter Sestoft, editor,
     Programming Languages and Systems, 15th European Symposium on Programming, ESOP 2006, Held
     as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2006, Vienna,
     Austria, March 27-28, 2006, Proceedings, volume 3924 of Lecture Notes in Computer Science, pages
     22–37. Springer, 2006.
                   AMORTISED RESOURCE ANALYSIS WITH SEPARATION LOGIC                                                            33




[17] Martin Hofmann and Dulma Rodriguez. Efficient Type-Checking for Amortised Heap-Space Analysis. In
     Erich Grädel and Reinhard Kahle, editors, Computer Science Logic, 23rd international Workshop, CSL
     2009, 18th Annual Conference of the EACSL, Coimbra, Portugal, September 7-11, 2009. Proceedings,
     volume 5771 of Lecture Notes in Computer Science, pages 317–331. Springer, 2009.
[18] Robert Hood and Robert Melville. Real-Time Queue Operations in Pure LISP. Information Processing
     Letters, 13(2):50–53, 1981.
[19] Samin S. Ishtiaq and Peter W. O’Hearn. Bi as an assertion language for mutable data structures. In
     Proceedings of the 28th ACM SIGPLAN-SIGACT symposium on Principles of Programming Languages,
     POPL ’01, pages 14–26, New York, NY, USA, 2001. ACM.
[20] P. O’Hearn and D. Pym. The logic of bunched implications. Bulletin of Symbolic Logic, 5(2):215–243,
     1999.
[21] Chris Okasaki. Purely Functional Data Stuctures. Cambridge University Press, 1998.
[22] D. J. Pym. The Semantics and Proof Theory of the Logic of Bunched Implications, volume 26 of Applied
     Logic Series. Kluwer Academic Publishers, 2002.
[23] Greg Restall. An Introduction to Substructural Logics. Routledge, 2000.
[24] John C. Reynolds. Separation Logic: A Logic for Shared Mutable Data Structures. In 17th IEEE Sympo-
     sium on Logic in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings,
     pages 55–74. IEEE Computer Society, 2002.
[25] Robert Endre Tarjan. Amortized computational complexity. SIAM Journal on Algebraic and Discrete
     Methods, 6(2):306–318, 1985.




                                             This work is licensed under the Creative Commons Attribution-NoDerivs License. To view
                                             a copy of this license, visit http://creativecommons.org/licenses/by-nd/2.0/ or send a
                                             letter to Creative Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or
                                             Eisenacher Strasse 2, 10777 Berlin, Germany
