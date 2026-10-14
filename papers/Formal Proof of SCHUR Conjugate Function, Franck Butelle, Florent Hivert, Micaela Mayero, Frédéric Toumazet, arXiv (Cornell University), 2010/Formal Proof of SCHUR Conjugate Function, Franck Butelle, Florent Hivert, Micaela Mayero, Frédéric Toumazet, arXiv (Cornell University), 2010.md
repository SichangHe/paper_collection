                                        Formal Proof of SCHUR Conjugate Function? ??

                                         Franck Butelle1 , Florent Hivert2 , Micaela Mayero1,3 , and Frédéric Toumazet4
                                                       1
                                                     LIPN UMR 7030, Université Paris 13, Villetaneuse, F-93430
                                               2
                                               LITIS EA 4108, Université de Rouen, Saint-Etienne-du-Rouvray, F-76801
                                        3
                                          LIP, INRIA Grenoble – Rhône-Alpes, UMR 5668, UCBL, ENS Lyon, Lyon, F-69364
                                          4
                                            LIGM UMR 8049, Université de Marne-la-Vallée, Champs sur Marne, F-77454
arXiv:1004.5034v1 [cs.LO] 28 Apr 2010




                                                   Abstract. The main goal of our work is to formally prove the cor-
                                                   rectness of the key commands of the SCHUR software, an interactive
                                                   program for calculating with characters of Lie groups and symmetric
                                                   functions. The core of the computations relies on enumeration and ma-
                                                   nipulation of combinatorial structures. As a first ”proof of concept”, we
                                                   present a formal proof of the conjugate function, written in C. This
                                                   function computes the conjugate of an integer partition. To formally
                                                   prove this program, we use the Frama-C software. It allows us to an-
                                                   notate C functions and to generate proof obligations, which are proved
                                                   using several automated theorem provers. In this paper, we also draw on
                                                   methodology, discussing on how to formally prove this kind of program.


                                        1      Introduction
                                        SCHUR [1] is an interactive software for calculating properties of Lie groups
                                        and symmetric functions [2]. It is used in research by combinatorists, physicists,
                                        theoretical chemists [3] as well as for educational purpose as a learning tool for
                                        students in algebraic combinatorics. One of its main uses is to state conjectures
                                        on combinatorial objects. For such use, it is important to have some confidence
                                        in the results produced by SCHUR.
                                            Until now, the method used to get some confidence in the results has mostly
                                        been based on just one example for each command.
                                            The computation of other examples is complex due to the well known combi-
                                        natorial explosion, especially when using algorithms associated to the symmetric
                                        group, see section 2.1. Unfortunately, the combinatorial explosion as well as com-
                                        puting time forbid test generation or verification techniques (model checking).
                                        Therefore, in this paper, we focus on formal proof of the existing program.
                                            With the aim of verifying the whole software, we start with proving the
                                        correctness of its fundamentals bricks. The main combinatorial object used in
                                        SCHUR is integer partition. The first non-trivial operation on integer partitions
                                        is the conjugate. Moreover, conjugate function is necessary for more than half of
                                        the 240 interactive commands of SCHUR. From this point of view, we can say
                                        that conjugate is a critical function of SCHUR.
                                        ?
                                             This research is supported by the PEPS-CNRS project CerBISS.
                                        ??
                                             The final publication of this paper is available at www.springerlink.com
    The very first work consists in isolating (see 4.3) the code of this function
from the program. Next, we chose to use the most popular tool of program proof
community’s Frama-C [4] successor of Caduceus. Frama-C is a plug-in system.
In order to prove programs, we used Jessie [5], the deductive verification plug-in
of C programs annotated with ACSL [6]. The generated verification conditions
can be submitted to external automatic provers, and for more complex situations,
to interactive theorem provers as well (see section 2.2).
    After a short presentation of software tools and theoretical concepts, we will
present the formal proof of a program. Finally, after discussing difficulties and
mistakes encountered along the way, we will propose a methodology to prove
such a software, and finally discuss future work.


2     Presentation of the Software Used

2.1   The SCHUR Software

SCHUR is an interactive software for calculating properties of Lie groups and
symmetric functions. A Symmetric Function is a function which is symmetric,
or invariant, under any permutation of its variables. For example f (x1 , x2 , x3 ) =
x1 + x2 + x3 is a symmetric function.
    SCHUR has originally written by Prof. Brian G. Wybourne in Pascal lan-
guage. Then it was translated into C by an automatic program making it quite
difficult to read. There are almost no comments in the code, the code is more
than 50,000 lines long with many global variables. Local variables have names
such as W 52 and so on.
    After the death of Prof. Wybourne in November 2003, some people felt that
his program should be maintained, and if possible enhanced, with a view to
making it freely available to the mathematics and physics research community.
    Nowadays, it is open source under the GPL license and includes more than
240 commands. The code still includes very few comments. Some mistakes have
been corrected but some interactive commands are so intricate that it is difficult
to have more than a few examples to check them against and most people do
not even know if the result is correct or not.
    This is why we started to work on this code. Firstly some of the commands in
SCHUR are very well implemented (for example, plethysm is computed faster by
SCHUR than by many other combinatorial toolboxes). Formally proving some
key functions inside would also be a major advance for its research community.


2.2   The Frama-C Software

Frama-C [4] is an open source extensible platform dedicated to source code analy-
sis of C software. It is co-developed by two French public institutions: CEA–LIST
(Software Reliability Laboratory) and INRIA-Saclay (ProVal project).
    Frama-C is a plug-in system. In order to prove programs, we use Jessie [5],
the deductive verification plug-in of C programs annotated with ACSL [6]. It

                                         2
uses internally the languages and tools of the Why platform [7]. The Jessie
plug-in uses Hoare-style [8] weakest precondition computations to formally prove
ACSL properties. The generated verification conditions (VC) can be submitted
to external automatic provers such as Simplify [9], Alt-Ergo [10], Z3 [11], CVC3
[12].
     These automatic provers belong to SMT (Satisfiability Modulo Theories)
solvers. The SMT problem is a decision problem for logical formulas with re-
spect to combinations of background theories expressed in classical first-order
logic with equality. First-order logic is undecidable. Due to this high computa-
tional difficulty, it is not possible to build a procedure that can solve arbitrary
SMT problems. Therefore, most procedures focus on the more realistic goal of
efficiently solving problems that occur in practice.
     For more complex situations, interactive theorem provers can be used to
establish the validity of VCs, like Coq [13], PVS [14], Isabelle/HOL [15], etc. For
our purpose, we used Coq (see section 4.2) since it is the one best known to the
authors.


3     The Conjugate Function
In this section, the basics of algebraic combinatorics are given so that the reader
can understand what is actually proved. Interestingly in this field, though the
interpretation of what is actually computed can be of a very abstract algebraic
level, the computation itself boils down most of the time to possibly intricate
but rather elementary manipulations.

3.1   Combinatorial and Algebraic Background: Integer Partitions
A partition of a positive integer n is a way of writing n as a sum of a non-
increasing sequence of integers. For example λ = (4, 2, 2, 1) and µ = (2, 1) are
partitions of n = 9 and n0 = 3 respectively. We write |λ| = n and |µ| = n0 [16].
    The Ferrers diagram F λ associated to a partition λ = (λ1 , λ2 , ..., λp )
consists of |λ| = n boxes, arranged in l(λ) = p left-justified rows of lengths
λ1 , λ2 , ..., λp . Rows in F λ are oriented downwards (or upwards for some au-
thors). F λ is called the shape of λ.
Definition 1. The conjugate of an integer partition is the partition associated
to the diagonal symmetric of its shape.
For example, for λ = (3, 2, 1, 1, 1), here is the Ferrers diagram F λ and the Ferrers
diagram of the conjugate partition:




                                         3
    So the conjugate partition of (3, 2, 1, 1, 1) is (5, 2, 1).
    A semi-standard Young tableau of shape λ is a numbering of the boxes
of F λ with entries from {1, 2, ..., n}, weakly increasing across rows and strictly
increasing down columns. A tableau is standard if and only if each entry appears
only once. Here is an example of shape (4, 2, 2, 1) tableau:

                                           1 2 2 5
                                           2 4
                                           3 6
                                           5

    A symmetric function of a set of variables {x1 , x2 , . . .} is a function
f (x1 , x2 , . . .) of those variables which is invariant under any permutation of those
variables (that is for example f (x1 , x2 , . . .) = f (x2 , x1 , . . .)). This definition is
usually restricted to polynomial functions. The most important linear basis of
symmetric function’s algebra is called the Schur functions and they are com-
binatorially defined as follows: for a given semi-standard Young tableau T of
shape λ, write xT the product of the xi for all i appearing in the tableau. Then
                                                     X
                                    sλ (x) =               xT .                             (1)
                                               T ∈Tab(λ)

where Tab(λ) is the set of all tableaux of shape λ. We will note sλ (x), sλ . For
example, consider the tableaux of shape (2, 1) using just three variables x1 , x2 , x3 :

         1 1       1 1        2 2        1 2         1 3          1 2      1 3        2 3
         2         3          3          3           2            2        3          3

The associated Schur function is therefore:

    s(21) (x1 , x2 , x3 ) = x21 x2 + x21 x3 + x22 x3 + 2x1 x2 x3 + x1 x22 + x1 x23 + x2 x23 (2)

thus:
                 s(21) = s(21) (x1 , x2 , x3 ) + s(21) (x1 , x2 , x3 , x4 ) + . . .
Note that, with this combinatorial definition, the symmetry of s(21) (x1 , x2 , x3 )
is not exactly obvious.
    We need to recall some well-known results in symmetric function theory:
though Schur functions have historically been defined by Jacobi [17], they were
named in the honor of Schur who discovered their crucial role in the representa-
tion theory of the symmetric group and the general linear group. Namely, after
the discovery by Frobenius that the irreducible representation of the symmetric
groups are indexed by integer partitions, Schur showed that those functions can
be interpreted as characters of those irreducible representation, and by Schur-
Weyl duality characters of Lie groups and Lie algebras. Notably we obtain the
representation of the general linear groups (GLn ) and unitary groups (Un ) [18]
from the symmetric group representations. In this setting, the conjugate of the


                                                 4
partition essentially encodes the tensor product of a representation by the sign
representation.
    Further work by Schur-Littlewood involve infinite sum of Schur functions
associated to partitions [19], whose conjugates have a particular form. In partic-
ular, these series are used to obtain symplectic (Sp2n ) and orthogonal character
groups (On ) (symmetric and orthogonal Schur functions) from standard Schur
functions [20].
    One particularly important and difficult computational problem here is
plethysm (see SCHUR reference manual [1] and [2]). It is the analogue in sym-
metric functions of the substitution of polynomial inside another polynomial
f (x) 7→ f (g(x)). It is called plethysm because by some combinatorial explosion,
it involves very quickly a lot (a plethora) of terms, making it something very
difficult to compute efficiently. For example, s(21) (s(21) ), the first example with
non trivial partitions in the input is already very hard to compute by hand. First
we can regard s(21) as a function in as many monomial as in (2):

s(21) (s(21) )(x1 , x2 , x3 ) = s(21) (x21 x2 , x21 x3 , x22 x3 , x1 x2 x3 , x1 x2 x3 , x1 x22 , x1 x23 , x2 x23 )
it can be shown that the following holds:
      s(21) (s(21) ) = s(22221) + s(321111) + 2s(32211) + s(3222) + s(33111) +
                        3s(3321) + 2s(42111) + 3s(4221) + 3s(4311) + 3s(432) +
                        s(441) + s(51111) + 2s(5211) + s(522) + 2s(531) + s(54) + s(621)

3.2     Computation in Algebraic Combinatorics
Basically, the architecture of a software for computing in algebraic combinatorics
is composed of two parts:
  – a computer algebra kernel dealing with the bookkeeping of expressions and
    linear combinations (parsing, printing, collecting, Gaussian and Groebner
    elimination algorithm. . . );
  – a very large bunch of small combinatorial functions which enumerate and
    manipulate the combinatorial data structures.
In algebraic combinatorics software, for each basic combinatorial structure such
as permutations or partitions, there are typically 50-200 different functions. Con-
jugating a partition is a very good example of what those many functions do,
that is surgery on lists of integers or lists of lists of integers or more advanced
recursive structures like trees. . . In a basic computation, most of the time is
spent mapping or iterating those functions on some sets of objects. But due to
combinatorial explosion those sets can be very large so these functions must be
very well optimized.

3.3     Properties
The definition of conjugate (diagonal symmetric of its partition shape) is easy to
understand but may conduct to naive implementations that may be inefficient.


                                                       5
    Let us suppose that we represent an integer partition by an integer array
starting from 1. For example λ = (3, 2, 1, 1, 1) gives t[1] = 3, t[2] = 2,... t[l(λ)] =
1. Recall that t[i] is non-increasing, that is t[i + 1] ≤ t[i].
    One way to compute the conjugate is to count boxes: in our previous example
the first column of λ had 4 boxes, the second had 3 etc. Therefore, to compute the
number of boxes in a column j we need to know how many lines are longer than
j. As a consequence, if tc is the array representing the conjugate, the following
formula gives the value of the entries of the conjugate:

                          tc [j] = |{i | 1 ≤ i ≤ l(λ) ∧ t[i] ≥ j}| .

Note that tc [j] = 0 if j > t[1], so the previous expression must be computed only
from j = 1 to j = t[1]. This last property will be one of our predicates used to
check the correctness of loop invariants.

3.4     SCHUR Implementation
Here follows the code of the conjugate function extracted from the SCHUR
software. We expanded type definitions (C “structs” and “typedefs”) from the
original code just to simplify the work of Frama-C and to make this part of code
independent from the rest of the SCHUR software (getting rid of global variables
and so on).

                 #define MAX 100

                 void conjgte (int A[MAX], int B[MAX]) {
                   int i, partc = 1, edge = 0;

                     while (A[partc] != 0) {
                        edge = A[partc];
                        do
                             partc = partc + 1;
                        while (A[partc] == edge);
                        for (i = A[partc] + 1; i <= edge; i++)
                             B[i] = partc - 1;
                     }
                 }

   Note that this implementation is not naive (and not so easy to understand)
but its time complexity is optimal (linear in the length of the partition).
   The algorithm is based on looking for the set of descents of the partition5 .
The do–while loop follows a “flat” portion of the partition (t[i] = t[i − 1]) until a
descent is found. Next the for–loop assigns the values of the B array according to
the flat portion. The following figure clarifies this: we have denoted partc1 the
value of partc at the entrance of while loop. partc2 is the value of partc after
5
    A descent is such that t[i] < t[i − 1]


                                              6
the do–while loop. For clarity’s sake we supposed A[partc2 ]+1 to be different
from A[partc1 ]. If we count boxes column by column to construct array B, it is
clear that B[i]=partc2 -1 for all A[partc2 ]+1 ≤ i ≤ A[partc1 ]=edge.




                                               A[partc2 ]+1
                                               A[partc2 ]



                                                                    A[partc1 ]

                                                                                       A[1]
                                         ...                  ...                ...




                                    1
                                    ↓           ↓ ↓                  ↓                 ↓
                             1→          ...                  ...                ...
                             ..     ..          ..     ..              ..
                              .      .           .      .               .
                        partc1 →         ...                  ...
                              ..    ..          ..     ..              ..
                               .     .           .      .               .
                     partc1 +n →         ...                  ...
                        partc2 →         ...
                               ..   ..          ..
                                .    .           .


4     The Formal Proof of the Conjugate Function

4.1   Annotations

In the following paragraphs we present the annotations added to the code. Note
that this is the only additions made to it. First we have to specify the model of
integers we want to deal with:

#pragma JessieIntegerModel(strict)

    This means that int types are modeled by integers with appropriate bounds,
and for each arithmetic operation, it is mandatory to show that no overflow
occurs.
    Next, we have to express in first-order logic what an integer partition (stored
in an array) is:

#define MAX 100
/*@ predicate is_partition{L}(int t[]) =
     (\forall integer i; 1 <= i < MAX ==> 0 <= t[i] < (MAX-1)) &&
     (\forall integer i,j; 1 <= i <=j < MAX ==> t[j] <= t[i]) &&
     t[MAX-1]==0;
  */

   Note that annotations are coded in the C comments, starting with a @. The
{L} term is the context (pre, post, etc.), we won’t detail it here, see [5, 6] for
details.


                                           7
    The data structure (array of integers) comes from the way the SCHUR soft-
ware represents integer partitions. 0 is used as a mark of end of array, just like
character strings in C. The MAX value comes from the original source code as
well. The first line of the predicate is_partition expresses that we are able to
compute the conjugate (if at least one element is greater than or equal to MAX-
1, the conjugate will no be able to be stored in an array of size MAX-1 with
the last element fixed to 0). From the source code it is expressed by an external
simple test on t[1], but expressing it like that simplifies automatic provers job.
The second line of the predicate defines the non-increasing order.
    The following predicate is needed to express how we count blocs to compute
the conjugate. It may be read as z equals the number of elements of partition
t, whose indexes are included in {1, .., j − 1} and whose values are greater than
or equal to k. It is theoretically possible to express it as an axiomatic theory, a
kind of function, but automatic provers we use make a better use of predicates.
Note that we need to explicit the z = 0 case, in order to be able to prove the
global post-condition is_conjugate(A,B).

/*@ predicate countIfSup{L}(int t[],integer j,integer k,integer z)=
    is_partition{L}(t) &&
    1<= j <= MAX &&
    1<= k < MAX &&
    ((1<=z<j && \forall integer i ; 1<=i<=z ==> t[i]>= k)
     || (z==0 && \forall integer i ; 1<=i<j ==> t[i]<k)) ;
 */

   Here is what we want to obtain at the end of the computation, t2 is a con-
jugate of t1 if the following holds:

/*@ predicate is_conjugate{L}(int t1[], int t2[]) =
    \forall integer k ; 1<=k<MAX ==> countIfSup(t1,MAX,k,t2[k]);
 */

    Finally, here is the function. First we have to give precise requirements on the
inputs. For example, (\valid(A+ (1..(MAX-1))) means that memory has been
allocated so array indexes from 1 to MAX-1 are allowed). From the original code,
the B array is supposed to be initialized with zeros before calling the function.
This is translated into a requires directive. Next, we specify which memory
elements are modified by the function (assigns). This is used for safety proofs.
In the end, the output is correct if the post-condition (ensures) is met.

/*@ requires \valid(A+ (1..(MAX-1)));
    requires \valid(B+ (1..(MAX-1)));
    requires is_partition(A);
    requires \forall integer k; 1<=k<MAX ==> B[k]== 0;
    assigns B[1..A[1]];
    ensures is_conjugate(A,B);
    */


                                         8
void conjgte (int A[MAX], int B[MAX])
{
  int i, partc=1, edge = 0 ;

    Now we have to define the loop variant and invariant for each loop (to prove
properties). The “loop variant” must decrease, while remaining non negative, to
be able to prove termination. We also use a “ghost variable” to store the state
of a variable before any modification.

    /*@ loop variant MAX-partc;
         loop invariant 1<=partc<MAX;
         loop assigns B[1..A[1]];
         loop invariant \forall integer k;
            A[partc]+1 <=k <= A[1] ==> countIfSup(A,MAX,k,B[k]);
      */
    while (A[partc] != 0) {
       edge = A[partc];

        /*@ ghost int old_partc = partc; */

        /*@ loop variant MAX-partc;
            loop invariant old_partc<=partc ;
            loop invariant \forall integer k;
                old_partc<= k <= partc ==> A[k]==edge;
            loop invariant partc<MAX-1;
         */
         do
             partc = partc + 1;
         while (A[partc] == edge);

   We also use the assert directive to have a verification point of a property
that may help automatic provers for the next properties or global ones.

        /*@ assert countIfSup(A,partc,edge,partc-1);*/

        /*@ loop variant edge-i;
             loop invariant i >= A[partc]+1 && edge+1>=i ;
             loop invariant \forall integer k;
                 A[partc]+1 <=k <i ==> countIfSup(A,MAX,k,B[k]);
             loop assigns B[ (A[partc]+1)..edge];
          */
        for (i = A[partc] + 1; i <= edge; i++)
             B[i] = partc - 1;
    }
}


                                       9
                   Fig. 1. Graphical Interface: default behavior


4.2   Proofs

The figures 1 to 3 are snapshots of gWhy (Frama-c graphical interface when
using plugin Jessie). We applied this tool on the previous annotated code.
    The Verification Conditions (VC, also called proof obligations) that have to
be proved one by one (line by line) appear to the left of each of the following
snapshots. In the upper right part of the window, we can check at a glance what
hypotheses are known and what is to be proved at the bottom of it (under the
line). No circularity paradox is possible here, since the proof of a VC can only
rely on other VC higher in the control-flow graph of the function.
    In the lower right part of the window, the corresponding part of the annota-
tion is highlighted in the source code with some lines before and after it.
    We will now focus on the VC part, to the left. We can see (green) dots
meaning that this property has been proved by this prover. There is also (blue)
rhombus with a question mark inside (see assertion 13), indicating that this
prover will not be able to to prove this property. Actually, this does not mean
that this VC is wrong, remember that these provers use heuristics. Sometimes,
you may see scissors meaning that the maximum execution time has been reached
without proving the VC. Again, this does not mean that the corresponding VC
is wrong. Finally, at the top of a column a (green) check or (red, with a white
cross inside) point is shown. The first one means that all properties have been
proved by that prover. In fig.1, The (blue) arrow at the top of the CVC3 column
means that it is still computing some unshown VC (greater than number 16).
    The last figure is the final part. The provers have worked on the safety of the
code, that is to say, integer bounds (overflow problems), pointer referencing and
termination.


                                        10
                       Fig. 2. Graphical Interface continued


    As seen in section 4.1, the B array has to be initialized with ze-
ros before calling the function. This requirement has been enlightened
thanks to the annotations and tools, in particular because without the
line requires \forall integer k;1<=k<MAX ==> B[k]==0, the postcondition
which states that B is a conjugate of A cannot be proved.
    We have also used Coq proof assistant. However, it not being essential to our
present point, we chose to live aside the detail of this procedure (see section 4.3).


4.3   Problems, Mistakes

As usual when using formal proof tools, there are several ways to formalize or
to annotate programs. Choices made during at this stage are very important for
future proofs. For example, declaring a function as an axiomatic theory or as
a predicate will suppose corresponding proofs to be different. We can make a
similar remark with data-types used in programs.
    For these reasons, using “good” annotations which allows automatic provers
to prove verification conditions (VC) successfully is a clever way to go about it.
    When we deal with 40,000 lines of undocumented code, another critical part
of the work consists in “correctly” isolating the piece of code that we want to
prove. The code can use global variables, initializations made by other functions,
or use intricate data-types and so on.
    In the following paragraphs, these problems and associated mistakes are dis-
cussed.


Isolating a Part of Program. Generally speaking, the analyzed function must
be free of external calls. More precisely if a function is called from it, it has to
be incorporated in the code (like macro expansion) or, at least, independently
proved.


                                         11
                        Fig. 3. Graphical Interface: Safety



    Next, data types must be simplified. Even if Frama-C can cope with simple
structures, it is better to have a first pass on them (unions suppression, typedef
expansion and so on).


How to Make Good Annotations? As previously explained, ACLS is a
language which is used to annotate C programs. Annotating an existing program
consists in choosing properties (comportment, results,...) that the user wants to
be “confirmed”, such as preconditions, loop invariants, post conditions. In our
case, for example, one of the most relevant properties we proved is that the result
B is the conjugate of the partition A. This property is stated as a postcondition.
    As usual, there are several ways to formalize annotations. Particularly when
using external provers, a good method is to know how provers work. Here, we
have to remember that the automatic provers are SMT solvers (see section 2.2).
    As an example, we can give the definition of countIfSup. In a first formal-
ization we wrote it as an “axiomatization”. But due to another problem that we
will describe in the next paragraph, we needed to make some proofs in Coq which
used countIfSup. Then, to make it easier for Coq, we decided to try to define
it inductively. Thanks to this other definition, some conditions were automati-
cally proved by SMT solvers. This example shows how important formalization
choices can be.
    In the next paragraph, we will explain and illustrate how Coq allowed us to
correct some errors in our annotations.


                                        12
Why Coq? Once annotations are completed, the method consists in using
automatic provers (using gWhy for example). As previously explained, if all
proof obligations are proved by at least one prover, the work can be considered
as finished. But, if one or more proof obligations is/are still unproved, several
approaches are possible: the first one consists in verifying that annotations are
“sufficient”, that is to say a precondition or a loop invariant is not missing.
Another approach, when the user suppose that his annotations are correct, is to
use an external non automatic prover to try to prove proof obligations that have
not been verified previously.
    In our case, we used the interactive theorem prover Coq twice. The first time
was because a postcondition had not been proved by SMT provers. When we be-
gan Coq proof, we discovered that the definition of countIfSup was incomplete:
the second part of the “||” (logical or) was missing.
    The second time we used Coq was to prove a loop invariant. Similarly, we
detected another incompleteness in countIfSup definition (j < M AX instead
of j ≤ M AX). Proof assistants are well adapted to detect this kind of problems.
Indeed, building formal proofs manually, a user can easily see which hypotheses
are necessary.
    After having corrected and replaced the “axiomatization” of countIfSup by
a predicate, all proof obligations have been proved by at least one automatic
prover.
    Note that the new definition allowed us to remove from the annotations one
additional lemma which, at first, appeared necessary.

Other Vicissitudes. Among the main encountered difficulties, we can mention
the confidence in the provers we used. In our case, one of the versions of CVC3
was faulty and proved all VC correct, even when they were false. For this reason
we decided to consider that a proof obligation was proved when at least two
automatic provers succeed on proving it. It is the case for all our obligations
except one (VC # 23 is only proved by Simplify). The proof of VC # 23 is in
progress using Coq.


5   Conclusion and Future Work
We have isolated and formally proved one of the key commands of the SCHUR
software. This work reinforced us in the idea of formally proving chosen parts of
software of the same kind, composed of 40,000 lines of undocumented code.
    Thanks to this approach, we have focused on critical points (such as par-
ticular initializations of arrays and appropriate bounds) from the original code
and by extension, we have understood the progression axis of the methodology.
In particular, it is better to know how SMT automatic provers work to try to
make a “good” annotation so that obligation proofs will be more easily proved
by them. In the methodology, non automatic external provers like Coq may be
used to refine annotations, and to prove obligations when no automatic provers
succeed.

                                       13
    The conjugate function is a basic brick of combinatorics. This give us perspec-
tive to prove other functions. Therefore, as a future work, the second step is to
prove algorithms relying on exhaustive enumeration algorithm, such as compu-
tation of Littlewood-Richardson coefficients, Koskas numbers, Koskas matrices,
representation multiplicity in tensor product decompositions, etc.
    The final objective will be to build proved libraries usable for scientific com-
munity.

References
 1. Butelle, F., King, R., Toumazet, F.: SCHUR, an interactive program for calculating
    properties of Lie groups and symmetric functions, http://schur.sourceforge.net.
    Release 6.06.
 2. MacDonald, I.G.: Symmetric Functions and Hall Polynomials. Clarendon Press,
    Oxford University Press (New York) (1979) 2nd edition in 1998.
 3. King, R.C., Bylicki, M., Karwowski, J., eds.: Symmetry, Spectroscopy and SCHUR.
    Nicolaus Copernicus University Press (2006)
 4. Correnson, L., Cuoq, P., Puccetti, A., Signoles, J.: Frama-C User Manual, Beryl-
    lium release, http://frama-c.cea.fr
 5. Marché, C., Moy, Y.:           Jessie Tutorial, http://frama-c.cea.fr/jessie/jessie-
    tutorial.pdf. Release 2.21.
 6. Baudin, P., Cuoq, P., Filliâtre, J.C., Marché, C., Monate, B., Moy, Y., Prevosto, V.:
    ACSL: ANSI/ISO C Specification Language, http://frama-c.cea.fr/download/acsl-
    implementation-Beryllium-20090902.pdf
 7. Filliâtre, J.C., Marché, C., Moy, Y., Hubert, T., Rousset, N.: Why is a software
    verification platform, http://why.lri.fr. Release 2.21.
 8. Hoare, C.A.R.: An axiomatic basis for computer programming. Communications
    of the ACM 12(10) (1969) 576–580 and 583
 9. Detlefs, D., Nelson, G., Saxe, J.B.: Simplify: a theorem prover for program check-
    ing. J. ACM 52(3) (2005) 365–473 Release 1.5.4.
10. Conchon, S., Contejean, E., Bobot, F., Lescuyer, S.: Alt-Ergo is an automatic
    theorem prover dedicated to program verification, http://ergo.lri.fr. Release 0.9.
11. Microsoft        Research:               Z3      An     Efficient     SMT      Solver,
    http://research.microsoft.com/en-us/um/redmond/projects/z3. Release 2.4.
12. Barrett, C., Tinelli, C.: CVC3. In Damm, W., Hermanns, H., eds.: Proceedings
    of the 19th International Conference on Computer Aided Verification (CAV ’07).
    Volume 4590 of Lecture Notes in Computer Science., Springer-Verlag (July 2007)
    298–302 http://cs.nyu.edu/acsys/cvc3 Release 20091011.
13. Bertot, Y., Castéran, P.: Interactive Theorem Proving and Program Development:
    Coq’Art: The Calculus of Inductive Constructions. EATCS, Texts in Theoretical
    Computer Science. Springer Verlag (2004)
14. Shankar, N., Owre, S., Rushby, J.M., Stringer-Calvert, D.W.J.: PVS prover guide,
    http://pvs.csl.sri.com/doc/pvs-prover-guide.pdf
15. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL — A Proof Assistant for
    Higher-Order Logic. Volume 2283 of LNCS. Springer (2002)
16. Andrews, G.E.: The theory of partitions. Cambridge University Press (1984)
17. Jacobi, C.G.J.: De functionibus alternantibus earumque divisione per productum
    e differentiis elementorum conflatum. Journal für die reine und angewandte Math-
    ematik (Crelles Journal) 22 (1841) 360–371 Reprinted in Gesammelten Werke III,
    G. Reimer, Berlin, 1884.


                                            14
18. Littlewood, D.E.: The Theory of Group Characters. Oxford University Press
    (1950) second edition.
19. Lascoux, A., Pragacz, P.: S-function series. J. Phys. A: Math. Gen. 21 (1988)
    4105–4118
20. Newell, M.J.: On the representations of the orthogonal and symplectic groups. In:
    Proc. Roy. Irish Acad., Section A: Mathematical and Physical Sciences. Volume 54.
    (1951) 143–152




                                         15
