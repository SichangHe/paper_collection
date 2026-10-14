                                                Towards platform-independent verification
                                                 of the standard mathematical functions:
                                                         the square root function?

                                         Nikolay V. Shilov1 , Igor S. Anureev2 , Mikhail Berdyshev1 , Dmitry Kondratev2 ,
                                                                       Aleksey V. Promsky2
arXiv:1801.00969v2 [cs.LO] 25 Jan 2018




                                                                 1
                                                                  Innopolis University, Innopolis, Russia
                                                           shiloviis@mail.ru, m.berdyshev@innopolis.ru
                                                2
                                                  A.P. Ershov Institute of Informatics Systems RAS, Novosibirsk, Russia
                                                    anureev@iis.nsk.su, apple-66@mail.ru, promsky@iis.nsk.su



                                                 Abstract. The paper presents (human-oriented) specification and (pen-
                                                 and-paper) verification of the square root function. The function imple-
                                                 ments Newton method and uses a look-up table for initial approxima-
                                                 tions. Specification is done in terms of total correctness assertions with
                                                                                                                √
                                                 use of precise arithmetic and the mathematical square root . . ., algo-
                                                 rithms are presented in pseudo-code with explicit distinction between
                                                 precise and machine arithmetic, verification is done in Floyd-Hoare style
                                                 and adjustment (matching) of runs of algorithms with precise arithmetics
                                                 and with machine arithmetics. The primary purpose of the paper is to
                                                 make explicit properties of the machine arithmetic that are sufficient to
                                                 make verification presented in the paper. Computer-aided implementa-
                                                 tion and validation of the proofs (using some proof-assistant) is the topic
                                                 for further studies.
                                                 Keywords: machine arithmetic, exact functions, formal verification, to-
                                                 tal and partial correctness, Floyd-Hoare method, square root, Newton
                                                 method, look-up table, fix-point representation, floating-point represen-
                                                 tation


                                         1     Introduction
                                         1.1     Motivation
                                         Let us start with a quotation from the abstract of the paper [18], because it
                                         correlates with the purpose of our paper very well:
                                               Current critical systems commonly use a lot of floating-point compu-
                                               tations, and thus the testing or static analysis of programs containing
                                               floating-point operators has become a priority. However, correctly defin-
                                               ing the semantics of common implementations of floating-point is tricky,
                                         ?
                                             This research is supported by Russian Basic Research Foundation grant no. 17-
                                             01-00789 Platform-independent approach to formal specification and verification of
                                             standard mathematical functions.
    because semantics may change with many factors beyond source-code
    level, such as choices made by compilers.
The major difference between [18] and the present paper is the concern: the
cited paper addresses problems with the floating-point value representation and
arithmetics, while the present paper addresses the standard mathematical func-
tion platform-independent formal specification and formal verification by study
in full details the square root function.
    In our approach the platform-independence means that we specify properties
of the functions and prove these properties for for approximate algorithms with-
out building (some-how comprehensive) formal model of a particular processor
architecture (like, for example, Intel’s processors in [8,9,11] or Oracles processors
in [13]) or fix/floating-point formats (like, for example, in [2,7,18]) but carry out
a proofs with several explicit simple assumptions how machine arithmetic relates
to the precise arithmetic. Thus these explicit simple assumptions are sufficient
conditions to validate on a particular processor with particular formats of nu-
meric data in order to guarantee that a mathematical functions verified with
these assumptions (square root function in this paper) meet their formal spec-
ification. We believe that our assumptions about machine arithmetic are valid
for many platforms and are easy to check/validate.
    Before we move to a literature survey on topics related to our study let
us advocate importance of the formal verification of the software. Although
our paper addresses verification in small (i.e. verification of small stay-alone
programs), we would appeal in the next paragraph to importance of verification
in large i.e. verification of complex cyber-physical systems. (Please refer slides
8-11 of [13] for justification of a need of verification in small, floating-point
arithmetic, and the standard mathematical functions in particular.)
    December 12, 2017, Roskosmos [28] has published the official results of in-
vestigation of the accident on November 28, 2017, which has led to loss of the
Meteor-M satellite (altogether with another 18 satellites). Risks at start have
been insured for the sum of 2,6 billion Russian rubles. Results of the investigation
read [28] (translation by N.V. Shilov):
    It has revealed the hidden problem in an algorithm which wasn’t shown
    for decades of successful launches of Sojuz carrier-rocket with the upper-
    stage accelerating block Fregate. ... There was a combination of pa-
    rameters of a launching-pad of the spaceport, azimuths of flight of the
    carrier-rocket and the accelerating block which hadn’t been met earlier.
    Respectively, it hasn’t been revealed at the carried-out on-land testing
    and simulation of a ballistic trajectory according to the standard adopted
    techniques.
The formal verification (in large as well as in small) is aimed to reveal “hidden
problem in an algorithm which wasn’t shown for decades”, a rare “combination
of parameters” that can’t be revealed “according to the standard adopted tech-
niques”. We believe that a formal verification is a demand of the day and one of
a few grad challenges for Computer Science research [12].
1.2     Literature survey

A need for better specification and validation of the standard functions is rec-
ognized (in principle) by industrial and academic professional community, as
well as the problem of a conformance of their implementation with the specifica-
tion. We would like to point out just on two papers [16,17] that address formal
complex specification and testing of standard mathematical functions. Hear we
use adjunctive complex because these papers don’t restrict function properties
by accuracy but take into consideration, for example, that sin and cos are odd
and even functions respectively, they match pythagorean normalization equality
sin2 x + cos2 x = 1 for all real x ∈ R. An educational value and issues of bet-
ter documentation and specification of the standard functions are discussed in
papers [22,23].
    Several studies have been published on platform-dependant formal verifica-
tion of mathematical functions, including division [4,9], square root [20,9,21,4],
trigonometric [8], exponential [10], and gamma [24] functions. Also several stud-
ies have been published on axiomatization of machine arithmetic (mostly binary
floating-point arithmetic for the IEEE-754 standard [26]) to prove basic mathe-
matical properties and consequently prove correctness of mathematical functions
[2,7,3,1].
    First let us remark that even platform-independent verification of the integer
square root function is not a trivial exercise. Please refer, for example, paper [21]
where some standard mathematical integer functions (including the square root)
are specified and verified in PVS.
    Paper [2] formalizes machine arithmetic using Z-notation and present an
implementation of the specification written in Occam. It presents a formal de-
scription of several mathematical functions over floating-point numbers, namely:
rounding, addition, multiplication, square root, type-casting to integer, compar-
isons, etc. Besides it, the paper specifies five classes of floating-point numbers:
NaN, Inf, zero, normal and denormal numbers. Then four modes of rounding
and error conditions are presented. The implementation includes representations
of floating-point numbers, its rounding and packing/unpacking and basic finite
mathematical procedures. The main algorithm pattern for a binary operation
with floating-point values (according to [2]) is as follows:

 1. unpack both operands into their sign, exponent and mantissa fields;
 2. denormalise both by shifting in the leading bit of the mantissa if necessary;
 3. perform the operation with denormalized arguments;
 4. pack the result and then round the packed result.

    Next paper [7] presents an approach to verification in HOL Light of sev-
eral floating-point operations of a new (at time of publication) Intel computer
architecture IA-64:

      Correctness of the mathematical software starts from the assumption that
      the underlying hardware floating point operations behave according to the
    IEEE standard 754 for binary floating point arithmetic. Actually, IEEE-
    754 doesn’t explicitly address floating-point machine arithmetic opera-
    tions, and it leaves underspecified certain significant questions, e.g. NaN
    propagation and underflow detection. Thus, we not only need to specify
    the key IEEE concepts but also some details specific to IA-64.

This paper starts with a theory of floating point arithmetic, which is non specific
to any format and afterwards specifies IA-64 formats in details. Floating-point
numbers in [7] are presented in highly generic way (as ±k × 2E−N ) but have a
canonical representation and normalized form. The paper argues also that the
concept of the unit in the last place (ulp) has several different definitions but
all have some counterintuitive properties; due to this reason the paper adopts
a modified definition from [19]. Four types of rounding (to-Nearest, Down, Up,
to-Zero) are defined in [7]; in contrast to the IEEE standard rounding is defined
for numbers with an unbounded exponent range, but all overflows are handled
during operations execution.
    Paper [3] describes syntax and semantics of floating-point arithmetic theory.
Besides being general, the formalization seriously rely upon Satisfiability Modulo
Theories (SMT) approach. The paper has 2 certain contributions: mathemati-
cal structures for floating-point model, a signature for a theory of floating-point
arithmetic and an interpretation of its operators in terms of the mathematical
structures defined earlier. Thus, it is designed to be a formal reference for auto-
matic theorem provers providing built-in support for reasoning about floating-
point arithmetic.
    It is important to prove correctness of mathematical functions widely used
in different architectures and libraries. The square root function is required (by
IEEE-754) to be exact (please refer the next section 2 for the definition). Hence,
correctness of this function (as well as other exact functions) should be consid-
ered with a special attention.
    Approach to verification of the square root function suggested in paper [4]
is based on a concept of a digit serial method (DSM) for a number: DSM for
a real number x ∈ R is an algorithm that determines the digits of x serially,
starting with the leading digit. The main contribution of the paper is a generic
DSM analysis method for determining bounds on the magnitudes of the digits,
as well as bounds on the error associated with the estimates. (We believe that
the approach may be related to interval techniques [14].)
    In the papers [5,20] authors prove correctness of the square root algorithm
used in Power4 processor. The algorithm uses Chebyshev polynomials. Despite
of the fact that the algorithm has more steps comparing to the Newton (also
known as Newton-Raphson) method used in [11], only one iteration is enough to
get necessary accuracy; also, because less instructions are reliant on the earlier
ones in the polynomial algorithm, the algorithm is better for parallelization.
The verification in [5,20] is divided by two parts: proof of Taylors theorem and
proof of properties of the square root function using Taylors theorem. One of the
biggest challenges in the study in [20] was to approximate error size of Chebyshev
polynomial with Taylors series as the former has a better approximation. To
escape this problem hundreds of Taylors series were evaluated. The proof has
been carried-out using non-standard analysis book (library) in ACL2.


1.3   Paper structure

In the next section 2 we present specification of the square root function accord-
ing to the C programming language standard, sketch Newton method to compute
approximations for the square root, formalize it as SQR algorithm (with until-
loop) and specify it in Floyd-Hoare style by a total correctness assertion [6]
assuming the precise arithmetic (i.e. for mathematical reals).
    In section 3 we give a pen-and-paper verification of the algorithm SQR from
the previous section 2 using Floyd-Hoare approach [6] and assuming the precise
arithmetic: partial correctness is considered in the subsection 3.1 and termination
— in the subsection 3.2.
    Section 4 presents two modifications of the square root algorithm SQR: the
first algorithm ISQR differs from SQR by use of an auxiliary function to “com-
pute” good initial approximations (see subsection 4.1), the second algorithm
F SQR (see subsection 4.2) is a for-loop-based algorithm that uses the same
auxiliary function but (in contrast to ISQR) estimates the number of suffi-
cient iterations to achieve the required accuracy of the approximations. Both
algorithms in this section are specified and verified under assumption that the
arithmetic is precise.
    The following-up section 5 starts with the subsection 5.1 where we formu-
late assumptions about fix-point values and arithmetic, and then presents and
specifies the fix-point algorithm f ixSQR in the subsection 5.2.
    The algorithm f ixSQR is verified (manually) in the section 6 by comparison
with runs of algorithm F SQR on the same input data. In the same section 5
we specialise the algorithm f ixSQR into better algorithm mixSQR which is
correct because of correctness of the algorithm f ixSQR.
    Section 7 presents our assumptions about floating-point arithmetic, the al-
gorithm f ltSQR that computes approximations for the square root function in
floating-point arithmetic, its specification and pen-and-paper verification. The
algorithm is based on square root extraction from mantissa (using the fix-point
algorithm mixSQR) and integer division to compute the exponent.
    In the last section 8 we summarise the content and contribution of the present
paper and discuss the topics for further research.


2     What is the standard function sqrt?

The C reference portal at en.cppreference.com/w/c specifics the the square
root function sqrt [25] as it represented in the Appendix A. It is easy
                                                                    √ to see an
ambiguity in the specification: it first says that sqrt(2) must be 2, but then
(in the Notes) that the error of sqrt(2) must be less than 0.5 of ulp — the unit
in the least precision (that is type and platform dependable. Of course, we have
                                               √
to rule out the first option (that sqrt() is ) as non-realistic; instead we have
and examine in details the second one.
     The standards mentioned in the specification are IEEE 754-2008 Standard for
Floating-Point Arithmetic and the international standard ISO/IEC 60559:2011
[27] (that is identical to IEEE 754-2008). Section 9 of the standard recommends
fifty operations that language standards should define (but all these operations
are optional, not required in order to conform the standard). Some of these
operations (including sqrt() as a special case of the function ( )1/n for n = 2),
if being implemented, must be (according to the standard’ terminology) exact
i.e. to round correctly (i.e. with an error less than 0.5ulp). Due to this use of the
term exact for computer functions and operation, let us fix another term precise
when we speak about mathematical functions and operations with mathematical
real numbers R.
     The first problem with the standard is type and platform dependence of
the concept of the exact function: the accuracy upper bound 0.5ulp depends on
numeric type (float vs. double) as well as on implementation of the types (i.e.
memory size reserved for the types). Another very critical problem with the spec-
ification and ISO/IEC/IEEE standards above is the absence (in the specification
and standards) of a description of any validation procedure to check/prove that
an implementation conforms the specification/standard.
     Instead of requiring that sqrt computes the exact values for square roots in
type- and/or platform-dependent way, it makes sense to specify another “stan-
dard” generic function (say SQR( , )) for generic numeric data types with two
parameters: the first parameter is for passing the argument value Y ≥ 0 and the
second
√        — for passing the accuracy value Eps > 0; the function is for computing
   Y with the accuracy Eps.
     The accuracy of this function SQR (i.e. the most wanted property and the
only property specified in the standard) can be formally specified by any (or
both) of the following two assertions:
                                                                           √
  – for all type-legal values y ≥ 0 and ε > 0, SQR(y, ε) differs from y by no
                         √
      more than ε, i.e. | y − SQR(y, ε)| ≤ ε;
                                                             2
  – for all type-legal values y ≥ 0 and ε > 0, SQR(y, ε) differs from y by no
                                        2
      more than ε, i.e. y − (SQR(y, ε)      ≤ ε.
   It makes sense to fix the first formal specification for better compatibility
with the concept of the exact standard function, since in this case we can define
the standard function sqrt via SQR as follows:
     float sqrt(float Y)
     {return((float)SQR(Y, default(float)/2.0);}
where default is another new type- and platform-dependent feature (similar to
sizeof) that returns the value of the unit in the least precision for a numeric
type.
    One may select any reasonable and feasible computation method to approxi-
      √
mate . For example, it can be a very intuitive, easy-to-implement and popular
in education (e.g. [19,15]) Newton Method:
float ab(float X)
{if (X<0) return(-X); else return(X);}

float SQR(float Y, float Eps)
{float X, D;
       X=Y;
       do {D=(Y/X-X)/2; X+=D;} while (ab(D)>=Eps/2);
return X;}


     Fig. 1. A floating-point function to compute a square root approximation


 1. input the number (to compute the square root) and guess an initial approx-
    imation for the root;
 2. compute the arithmetic mean between the guess and the number divided by
    the guess; let this mean be a new guess;
 3. repeat step 2 while the difference between the new and the previous guesses
    isn’t small enough (i.e. doesn’t feet the use-defined accuracy).
(Please refer to Fig. 1 for a sample implementation of the function for the data
type float.)
    Both floating-point functions in Fig. 1 are easy to specify formally in a Hoare
style [6]:
            
             [X is f loat] ab(X) [returned value = |X|],
               [Y ≥ 0 and Eps > 0 are f loats]            √                     (1)
                      SQR(Y, Eps)[|returned value − Y | ≤ Eps].
            

(Remark that the specification is incomplete since it doesn’t specify the program
behavior and output if input values are Y < 0 and/or Eps ≤ 0.)
   For a generic square root function with a generic numeric data type for input
and output values, the specification (1) should be modified:
    [T Y P Y is a numeric type, Y ≥ 0 : T Y P E, and Eps >√0 : T Y P E]
                                                                                (2)
                         SQR(Y, Eps) [|returned value − Y | ≤ Eps].
If these specifications are proved, then SQR may be a good alternative to the
standard function sqrt.
    Unfortunately, it is not easy to prove these specifications automatically and
formally because of several reasons. The major one is a problem that we already
discussed in the literature survey in the introduction section 1 — an axiom-
atization of the computer-dependent floating-point arithmetic. Even a manual
pen-and-paper verification of the algorithm SQR (assuming precise arithmetic
for real numbers R) is not a trivial exercise that we solve in the next section.

3   Pen-and-paper verification of SQR
Fig. 2 shows a flowchart of the algorithm (a little bit modified) of the function
from Fig. 1. Let us refer to the algorithm as SQR in the sequel. Having specified
                     Fig. 2. A flowchart of the algorithm SQR


the algorithm in the same way as the function, we need to prove the following
“relaxation” of the second triple in (2):
                                                      √
           [Y, Eps ∈ R & Y ≥ 0 & Eps > 0] SQR [|X − Y | ≤ Eps]            (3)

To prove this assertion, let us consider three disjoint cases for the range of the
initial value of the variable Y : 0 ≤ Y < 1, Y = 1 and Y > 1:
                                                           √
           [Y, E ∈ R & 0 ≤ Y < 1 & Eps > 0] SQR [|X − Y | ≤ Eps],              (4)
                                                         √
             [Y, E ∈ R & Y = 1 & Eps > 0] SQR [|X − Y | ≤ Eps],                (5)
                                                         √
             [Y, E ∈ R & Y > 1 & Eps > 0] SQR [|X − Y | ≤ Eps].                (6)
   The second case (5) is trivial. Two other cases (4) and (6) are “ideologically”
very similar, so we prove below in this section the assertion (6) only. Due to this
reason we assume below in the subsections 3.1 and 3.2 that the initial (input)
variable values meet the precondition Y, E ∈ R & Y > 1 & Eps > 0 and that all
operation used in the algorithm are precise mathematical operations with reals.

3.1   Partial Correctness
Let us employ the Floyd method [6] for a pen-and-paper proof of partial cor-
rectness. Let us select the control points 1, 2, and 3 as depicted in Fig. 2 to cut
the flowchart into three loop-free paths:
path (1..2) from the starting point 1 to point 2;
path (2+3) from point 2 to the final point 3 via the positive branch;
path (2–2) from point 2 to the same point 2 via the negative branch.
Let us consider all these paths one by one using the following annotations for
the control points:
 1. Y > 1 & Eps > 0 (i.e. the pre-condition);
                      √
2. Y > 1√& Eps > 0 & Y ≤ X ≤ Y (the loop invariant);
3. |X − Y | ≤ Eps (i.e. the post-condition).
   The first path (1..2) is easy to verify:
                                                                         √
                (Y > 1 & Eps > 0) → (Y > 1 & Eps > 0 &                       Y ≤ Y ≤ Y)
                                                                              √            .
             {Y > 1 & Eps > 0} X := Y {Y > 1 & Eps > 0 &                        Y ≤ X ≤ Y}


    The second path (2+3) is not so easy. Let us introduce a test program con-
struct φ? as a short-hand for if φ then stop else abort. Then verification of the
path (after some simplification) is as follows:
                                √                         2                            √
      (Y > 1 & Eps > 0 &            Y ≤ X ≤ Y & | Y −X
                                                    2X | < Eps/2) → |X −                   Y | < Eps


                       √                              2                                    √
  {Y > 1 & Eps > 0 &       Y ≤ X ≤ Y } D := Y −X
                                              2X          {|D| < Eps/2 → |X −               Y | < Eps/2}   (7)


                           √                              2                                √
   {Y > 1 & Eps > 0 &          Y ≤ X ≤ Y } D := Y −X
                                                  2X              ; |D| < Eps/2? {|X −      Y | < Eps}

The premise
                        √                          Y − X2                  √
(Y > 1 & Eps > 0 &             Y ≤X≤Y &|                  | < Eps/2) → |X − Y | < Eps
                                                     2X
is valid since in this case we have
       √        |X − √Y | (X + √Y )   2X  Eps     2
 |X − Y | =                           ×    √ ≤    ×    √ < Eps.
                          2X            X+ Y   2    1+ Y                                            X

   The proof (also after some simplification) of the third path (2–2) is as follows:

                                √                         2
       (Y > 1 & Eps > 0 &           Y ≤ X ≤ Y & | Y −X
                                                    2X | ≥ Eps/2) →              √              2
                                                 → (Y > 1 & Eps > 0 &                Y ≤ Y +X
                                                                                           2X       ≤ Y)


                                √
       {Y > 1 & Eps > 0 &           Y ≤ X ≤ Y}
                                                              2
                                           D := Y −X
                                                  2X            √
                                                                                                           (8)
                               {|D| ≥ Eps/2 → (Y > 1 & Eps > 0 & Y ≤ X + D ≤ Y )}


                                √
       {Y > 1 & Eps > 0 &           Y ≤ X ≤ Y}
                                         2
                           D := Y −X
                                  2X         ; |D| ≥ Eps/2? ; X := X + D   √
                                                         {Y > 1 & Eps > 0 & Y ≤ X ≤ Y }

A hint to prove the premise of this derivation:
              √                        √        +X 2
– (Y > 1 & Y ≤ X) → (Y > 1 & Y ≤ Y 2X                )
                    √
   since (Y > 1 & Y ≤ X) implies X > 1 and, hence, both sides of the
                        √            2
   AM-GM inequality X Y ≤ Y +X         may be divided by X;
              √                   2
                                              +X 2
– (Y > 1 & Y ≤ X ≤ Y ) → (Y > 1 & Y 2X             <Y)
                    √                         Y −X 2        +X 2
   since (Y > 1 & Y ≤ X ≤ Y ) implies 2X ≤ 0 and, hence, Y 2X     =
             2            2
          −X           −X
   X + Y 2X    ≤ Y + Y 2X    ≤ Y.
3.2    Termination
                                                                              √
Let us prove below that the loop invariant Y > 1 & Eps > 0 & Y ≤ X ≤ Y
implies that every loop iteration reduces the absolute value of D twice at least.
    For it let us fix some y > 1 as the initial value of the variable Y , ε > 0 as
the initial value of the variable Eps, let x1 , x2 , . . . xn , x(n+1) , . . . be the values
of the variable X immediately before 1st , 2nd , . . . n-th, (n + 1)-th, etc., iteration
of the loop for this fixed initial value y of Y , and let d1 , d2 , . . . dn , d(n+1) , . . . be
the values of the variable D immediately after 1st , 2nd , . . . n-th, (n + 1)-th, etc.,
iteration of the loop (also for the same fixed initial value y of Y ). In particular,
                    y−x2
x1 = y and dn = 2xnn , x(n+1) = xn + dn for all n > 0.
    Let us express d(n+1) in terms of dn :
                                              y+x2
         y−x2(n+1)               2 y−( 2xnn )2
d(n+1) = 2x(n+1)   = y−(x n +dn )
                      2(xn +dn ) =    y+x2
                                               =
                                     2 2xnn
                                                         (y−x2 )2 xn       d2 x
                                                                           n n           d2
                                                     = − 4x2 (y+x
                                                              n
                                                                  2 ) = − y+x2 = − 2x
                                                                                      n
                                                                                     (n+1)
                                                                                           .
                                                            n     n               n


Note that all values d1 , d2 , . . . dn , d(n+1) , . . . are negative due to the loop
invariant. Hence
                 |d(n+1) |   d(n+1)      dn     1 x2 − y  1
                           =        =−         = × n2    < .
                   |dn |       dn      2x(n+1)  2 xn + y  2
                           √
                         y− y
It implies |d(n+1) | <    2n , i.e. the algorithm terminates after at most
                                                    √
                                                 y− y
                                      1 + log2
                                                   ε
iterations of the loop.


4     Towards machine-oriented square root algorithm
4.1    Improved square root algorithms based on until-loop
In spite being very efficient (due to a logarithmic complexity) the algorithm
may be improved (optimized). Firstly,     √ since we study case when 1 < Y and
know (from the loop invariant) that Y ≤ X ≤ Y , it makes sense to compute
                                        2
                                          −Y                                       −X 2
directly the absolute value AD := X2X        of D instead of computing D := Y 2X
and then |D| in the loop condition. Next, we may use a fast hash function
SU P : (1, ∞) → (1, ∞) to compute good initial upper approximations instead
of a very rough initial upper approximation used in the algorithm SQR. (For
example, it may be rounded-up square roots.) While the first optimization just
saves on each loop iteration on calls of the function computing the absolute value,
the second one reduces the number of loop iterations. Fig. 3 shows a flowchart
of the improved algorithm that we refer as the algorithm ISQR in the sequel.
    For example if the function SU P returns the rounded-up square roots, y > 1
is the initial (input) value of the variable Y , and ε > 0 is the initial (input) value
         Fig. 3. A flowchart of the improved (optimized) algorithm ISQR

                                                 √
of variable Eps (accuracy) then 0 ≤ SU P (y) − y < 1 and, hence, an upper
bound for the number of the loop iterations in the algorithm ISQR is
                                                       √
                                           SU P (y) − y
                     1 − log2 ε ≥ 1 + log2
                                                  ε
instead of an upper bound
                                                       √
                                                    y− y
                     1 + log2 y − log2 ε ≥ 1 + log2
                                                      ε
for the number of the loop iterations in the non-optimized algorithm SQR.
    To prove the following total correctness assertion
                                      √
[Y > 1 & Eps > 0 & ∀y ∈ (1, +∞) : y ≤ SU P (y) ≤ y)]
                                                                   √
                                                       ISQR [|X − Y | < Eps]
we need to prove the partial correctness only since the termination are proved
already by providing an upper bound for the number of the loop iterations.
    For proving the partial correctness we may use the same control points 1, 2,
and 3 to cut the flowchart into three loop-free paths (1..2), (2+3), (2–2), and
the same annotations for the control points 2 (the loop invariant) and 3 (the
post-condition) as for the algorithm SQR, but need to extend the precondition
(Y > 1 & Eps > 0) of the SQR by specification of the function SU P :
                                       √
                       ∀y ∈ (1, +∞) : y ≤ SU P (y) ≤ y.
The above proof (7) of the path (2+3) and the proof (8) of the path (2–2)
remains valid. The first path (1..2) is easy to verify:

                                        √
       (Y > 1 & Eps > 0 & ∀y ∈ (1, +∞) : y ≤ SU P (y) ≤ y) →√
                                     → (Y > 1 & Eps > 0 & Y ≤ SU P (Y ) ≤ Y )
                                                                                 (9)
                                       √
       {Y > 1 & Eps > 0 & ∀y ∈ (1, +∞) : y ≤ SU P (y) ≤ y)}       √
                                 X := SU P (Y ) {Y > 1 & Eps > 0 & Y ≤ X ≤ Y }
      Fig. 4. A flowchart of the non-adaptive for-loop-based algorithm F SQR


4.2   For-loop-based square root algorithms
      (when more means better )
As we already proved, for every initial value y > 1 of the variable Y and every
initial value ε > 0 of the variable Eps termination of the√ improved square root al-
                                                 SU P (y)− y
gorithm is guaranteed after (at most) 1+dlog2          ε     e loop iterations, where
d. . .e is integer round-up function. Hence is possible to compute approximations
for the square root by a non-adaptive for-loop-based algorithm F SQR which
flowchart depicted in Fig. 4. The algorithm uses a non-deterministic assignment
                                                           √
                                                      X− Y
                       N := any integer ≥ 1 + log2                               (10)
                                                         Eps

(where d. . .e stays for integer rounding up). The corresponding correctness as-
sertion is
                                         √
   [Y > 1 & Eps > 0 & ∀y ∈ (1, +∞) : y ≤ SU P (y) ≤ y)] √
                                                                            (11)
                                                F SQR [|X − Y | < Eps2 ].

    Termination of the algorithm F SQR is guaranteed by design since it is for-
loop-based. Informally speaking the partial correctness of the algorithm follows
                                                                 2
                                                                   −Y
from the partial correctness of the algorithm ISQR: while X2X          ≥ Eps values
of X in both algorithms are equal in each iteration, and then √     F SQR   exercises
several more iterations that move value of X closer to Y . Nevertheless we
would like to make this argument more formal and in Floyd-Hoare style [6].
    Let us select the control points 1, 2, and 3 as depicted in Fig. 4 and annotate
them as follows:
                                           √
 1. Y > 1 & Eps > 0 & ∀y ∈ (1, +∞) : y ≤ SU P (y) ≤ y);              √
                           √
 2. Y > 1 & Eps > 0 & Y ≤ X ≤ Y & N ≥ 1 + log2 SU P (Y         Eps
                                                                  )− Y
                                                                         &
                                                                √                 √
                                                                        SU P (Y )− Y
                                         &0≤K≤N &X− Y ≤                              ;
          √                                                                2 N −K

 3. |X − Y | ≤ Eps  2  (i.e. the post-condition).
    Proof of the√
                   path (1..2) is trivial since at the end of this path N ≥ 1 +
      SU P (Y )− Y
dlog2      Eps     e, N − K = 0 and X = SU P (Y ).
    Proof of the path (2–2) just follows the proof of the similar path for the
algorithm SQR with the following addendum: 0 ≤ K ≤ N before the loop
implies 0 ≤ K ≤ N after the loop because of the loop condition K > 0 that
holds on this path before the assignment K := K − 1.
    Proof of the path (2+3) is more complicated: at the end of the path

1. K
   √ = 0 (due to the invariant at start of the path and the loop condition);
2. Y ≤ X (due to the invariant
                          p        at start
                                         √ of the path);
3. according to (2) |X − (Y )| = X − Y ;
                                                                  √
4. according to (1), (3) and the invariant |X − (Y )| ≤ SU P (Y )− Y
                                                p
                                                              2N
                                                                     ;
              √                  √                        √
5. SU P (Y
         2N
           )− Y
                ≤      SU P (Y )− Y
                                      √
                            SU P (Y )− Y
                                           = SUSU
                                                P (Y )− Y
                                                         √
                                                  P (Y )− Y
                                                            = Eps
                                                               2
                     1+log2
                                 Eps     2×
                    2                 √             Eps
                            SU P (Y )− Y
      (because N ≥ 1 + log2      Eps √ );
6. according to (4) and (5) |X −           Y | ≤ Eps
                                                  2 .

   We have proved a stronger assertion for F SQR than for SQR and ISQR.
Moreover, the proof implies that more iterations means better accuracy of com-
putations (in the precise arithmetic, of course).


5     Square root algorithm for fix-point arithmetics

5.1     Fix-point machine arithmetics

One of the problems with the improved and for-loop-based algorithms is how to
implement an efficient function SU P . A hint is use of a numeric data type T
with a (huge maybe) finite set of values V alT ⊂ R instead of an infinite set R.
Then the function SU P may be implemented in two steps:

 – define an efficient rounding up function round : V alT → V alT ,
 – pre-compute and memorize a look-up table root with good upper approxi-
   mations for the roots for each of the rounded values.

Further details and steps depend on selected numeric data type. In this and
the next sections we study fix-point numeric data and algorithms with fix-point
arithmetic. (We study of f loating−point data and algorithms later in the section
7.)
    We understand fix-point numeric data type T as follows:

 – the set of values V alT is a finite subset of mathematical reals R such that
     • it comprises all reals in some finite range [− inf T , supT ], where inf T > 2,
       supT > 2, with some fixed step 12 > δT > 0,
     • and includes all integer numbers IntT in this range [− inf T , supT ];
 – legal binary arithmetic operations are
  Fig. 5. A flowchart of the square root algorithm f ixSQR for fix-point arithmetic


     • addition and subtraction; if not the range overflow exception then these
       operations are precise: they equal to the standard mathematical opera-
       tions assuming their mathematical results fall in the range [− inf T , supT ]
       (and due to this reason are denoted as + and −);
     • multiplication ⊗ and division ; these operations are approximate but
       correctly rounded in the following sense: for all x, y ∈ V alT
         ∗ if x × y ∈ V alT then x ⊗ y = x × y;
         ∗ if x/y ∈ V alT then x y = x/y;
         ∗ if x × y ∈ [− inf T , supT ] then |x ⊗ y − x × y| < δT /2;
         ∗ if x/y ∈ [− inf T , supT ] then |x y − x/y| < δT /2.
 – legal binary relations are equality and all standard inequalities; these rela-
   tions are precise, i.e. they equal to the standard mathematical relations (and
   due to this reason are denoted as =, 6=, ≤, ≥, <, >).
      Due to the assumptions about the set of values
             V alT = {n × δT : n ∈ Z and − infT ≤ n × δT ≤ supT };
according the assumptions about integer values IntT within the range of V alT
                                                1
                           [−2..2] ⊆ V alT and     ∈ N.
                                                δT
    In case when multiplication is guaranteed to be precise (the mathemati-
cal product is in V alT ) then let us use the standard notation × instead of ⊗;
similarly in case when division is guaranteed to be precise (the mathematical
dividend is in V alT ) then let us use the standard notation / instead of .

5.2     Fix-point variant of the square root: algorithm and specification
A non-adaptive algorithm F SQR (Fig. 4) that uses mathematical operations
transforms into algorithm f ixSQR (Fig. 5) that uses machine fix-point opera-
tions. This algorithm also (as F SQR) uses a non-deterministic assignment op-
erator
                                                      Stp
                    N := some n ∈ IntT that 2n−1 ≥                       (12)
                                                     Eps
that differs from the assignment (10) by use of some instead of any: this differ-
ence means that later we select the value instead of use an arbitrary one.
    In the new algorithm we use an additional variable Stp for a positive value
in V alT , an array root, and a function round that have the following properties:
STEP: value of Stp is a multiple of the accuracy Eps, divides supT and is used
  to define the set ArgStp = {n × Stp : n ∈ N, and 1 < n × stp ≤ supT };
ROOT: root is a √pre-computed look-up table indexed by ArgStp such that
  root[v] − δT < v ≤ root[v] for each index v ∈ ArgStp ;
ROUND: the function round : V alT → ArgStp is a rounding-up such that
  round(u) − step < u ≤ round(u) for each u ∈ V alT , u > 1.
Comment on the STEP property: we consider as a very natural the as-
sumption that
 – Stp is a multiple of the accuracy Eps since in the “limit” case Eps = δT and
   this Eps divides any Stp ∈ V alT ;
 – Stp divides the “extreme” value supT because this value should be provided
   with a pre-computed square root upper approximation.
   We are ready to specify correctness of the square root algorithm f ixSQR
with fix-point arithmetic:
    [Y ∈ V alT & Y > 1 & Eps ∈ V alT & Eps > 0 &
                    & STEP & ROOT & ROUND]√                                      (13)
                            f ixSQR [|X − Y | < Eps
                                                            
                                                 2  + N × δT ].

6    Pen-and-paper verification of f ixSQR
     (more may be worse)
Termination of the algorithm f ixSQR is straightforward since it is a for-loop-
based algorithm. So we need to prove partial correctness only. We do this proof
below by adjustment (or comparison) of runs of algorithm f ixSQR with fix-point
arithmetics and algorithm F SQR with precise arithmetics.
    Let us select and fix hereafter initial values x, y, s, ε for the variables X, Y ,
Stp, and Eps, and a look-up table root and a function round such that meet
the precondition in (13). Let SU P : (1, ∞) → (1, ∞) be the function defined as
follows:
                  
                    root[v], if u ∈ (1, supT ], v ∈ ArgStp and u ∈ (v − s, v];
      SU P (u) =
                    u otherwise.
Then this function and the initial values of X, Y , and Eps meet the precondition
in (11).
    Let nn be a particular value assigned to N by the non-deterministic assign-
                                                                          √
ment operator (12) in the algorithm f ixSQR. Remark that SU P (y) − y ≤ s
due to the following arguments:
                        2                   √           √
                SU P (y) ≤ y + s ≤ y + 2s y + s2 = ( y + s)2 ;
hence this value nn is also a legal value of the non-deterministic expression
                                                         √
                                               SU P (y) − y 
                    any integer ≥ 1 + log2
                                                     ε
that is the right-hand expression in the assignment (10). It implies that both
algorithms F SQR and f ixSQR have legal runs with the initial values x, y, ε
for the variables X, Y , and Eps where both have exactly nn iterations of their
loops.
     Let x00 , . . . x0nn and x000 , . . . x00nn values of the variable X in these runs after
0-iterations, . . . nn-iterations of the corresponding loop. (In particular, x = x00 =
x000 is the initial value of X and x0nn and x00nn are the final values of the variable
upon termination.)
     Let us prove by induction on k ∈ [0..nn] that

                                         |x0k − x00k | ≤ kδT .                          (14)

Basis: x = x00 = x000 .
Assumption: |x0k − x00k | ≤ kδT for all k ∈ [0..n], where n < nn.
Step: Let ∆ = x0n − x00n ; (|∆| ≤ nδT due to the assumption.)
                 x0
    1. x0n+1 = 2n + 2xy0 ;
                          n
                                         x00
    2. x00n+1 = x00n 2 + y (2x00n ) = 2n + δa + 2xy00 + δb where |δa |, |δb | ≤ δ2T ;
                                                              
                                                        n
                            x00 −x0
    3. |x00n+1 − x0n+1 | = | n 2 n + y2 x100 − x10 + (δa + δb )| ≤
                                                  
                                                 n       n
                        |x00 −x0 |
                   ≤ n 2 n + y2 x100 − x10 + |δa + δb | ≤ |∆|    y 1
                                                             2 + 2 x00 − x10 + δT ;
                                    n     n                         n      n
     4. (Taylor’ expansion) x100 = x0 1+∆ = x10 − (x∆
                                                    0 )2 + θ,
                                     n       n           n       n
                   where θ is a converging alternating series, |θ − (x∆            ∆
                                                                      0 )2 | ≤ | (x0 )2 |;
                                                                             n         n

     5. (from 4) y2 x100 − x10       = y2 θ − (x∆
                                                0 )2 ≤ y2 × (x|∆|     y  |∆|
                                                               0 )2 ≤ 2 × y  = |∆|
                                                                                2 ;
                       n       n                     n               n

      6. (from 3 and 5) |x00n+1 − x0n+1 | ≤ |∆|  y 1
                                             2 + 2 x00  − x10 + δT ≤ |∆|  |∆|
                                                                      2 + 2 + δT ;
                                                     n      n
      7. (from 6) |x00n+1 − x0n+1 | ≤ |∆| + δT ≤ nδT + δT = (n + 1)δT .
                                                                          √
     According to the the proven total correctness assertion (11) |x0nn − y| ≤ 2ε ;
                                                       00    √     ε
together with the proven property (14) it implies |xnn − y| ≤ 2 +nn×δ ; since
x00nn and nn are the values of the variables X and N in the algorithm f ixSQR,
it finishes the proof of the assertion (13).
     One can remark that correctness of the assertion (13) implies that more
iterations of the loop may be worse in accuracy (due to the addend N × δT in
the postcondition).
     Our proof of the assertion (13) implies correctness of the following assertion

   [Y ∈ V alT & Y > 1 & Eps ∈ V alT & Eps > 0 &
                          Stp
   & EP S ≥ 2δT (2 + log2 Eps )&
                                                                                        (15)
                     & STEP & ROOT & ROUND]        √
                                       mixSQR [|X − Y | < Eps].

where mixSQR is algorithm depicted on Fig. 6. The assertion is valid due to
    Fig. 6. A flowchart of the square root algorithm mixSQR for fix-point arithmetic


the arguments represented in the next paragraph.
   The algorithm mixSQR is a specialization of the algorithm f ixSQR with
deterministic assignment
                                                               Stp
                   N := the minimal n ∈ IntT that 2n−1 ≥
                                                               Eps
instead of the nondeterministic assignment (12). The precondition in (15) ex-
                                                                    Stp
pands the precondition in (13) by the addend EP S ≥ 2δT (2 + log2 Eps   ) that
                                        Stp
means that the interval [(1 + log2 Eps      ), Eps
                                               2δT ] has length ≥ 1, i.e. contains an
integer. Let y, ε, s be initial values of Y , Eps, and Stp that satisfy the precon-
dition in (15) (and hence the precondition in (13)), and let nn be the minimal
                         Stp
n ∈ IntT that 2n−1 ≥ Eps     (i.e. the value assigned to the variable N ). Since y, ε,
s satisfy the precondition in (13), the algorithm mixSQR stops on these initial
data with final values of the
                             variables that satisfy the postcondition in (13), i.e.
      √
|x0 − y| < 2ε + nn × δT , where x0 is the final value of X; since the value of N
                                                                             √
is nn then nn × δT < 2δεT × δT = 2ε ; put it altogether we get that |x0 − y| < ε,
i.e. the postcondition in (15) is true.

7      Square root algorithm for floating-point arithmetic
In contrast to the fix-point numeric data type in the subsection 5.1, we aren’t
going to specify properties of floating-point arithmetic operations (since we don’t
need them to compute square root function) but just the properties of the set of
floating-point values and couple of type-casting operations (that convert floating-
point values into fix-point values and back).
    Let T be a fix-point numeric data type that satisfies the properties specified
in the subsection 5.1. We understand floating-point numeric data type F as
follows:
 – the set of values V alF is a finite subset of mathematical reals R that com-
   prises some reals in some finite range [− inf F , supF ], where inf F , supF > 2
   and {0, inf F , supF } ⊆ V alF ;
Fig. 7. A flowchart of the square root algorithm f ltSQR for floating-point arithmetic


 – there are two unary operations M an : V alF → V alT (called mantissa),
   Exp : V alF → IntT (called exponent), and an integer constant βT ∈ IntF
   (called exponent base or just base) such that for all positive x ∈ V alF
     • 1 < M an(x) < supβF ;
                          T


     • if infT is odd then −infT < Exp(x) else −infT ≤ Exp(x);
                        Exp(x)
     • x = M an(x) × βF        .
    Firstly remark that according to our definition of mantissa, it ranges in
(1, sup
     βF ) while the most common definition says that the mantissa ranges in
        T


[0.1, 1). We adopt the above definition as a variation and of the standard one
due to the following reasons: the right end of the range ( sup
                                                             βF ) is parameterised
                                                               T


by parameters that characterise numeric types T and F and hence is more gen-
eral than any fixed right end; the left end 1 of the range is excluded because we
want to use a verified algorithm mixSQR to compute in fix-point arithmetic an
approximation of the square root form the mantissa.
                                                              Exp(x)
    Next remark that in the property x = M an(x) × βF                we use × for
the precise mathematical multiplication and assume that the right-hand side
product is exactly computable on computer. This assumption is based on a
conventional representation of a floating-point value in the computer memory
as a pair consisting of mantissa and exponent with opportunity to extract the
mantissa and the exponent separately and precisely (we use operations M an
and Exp) and then reconstruct the value back (and save it in the memory) by
coupling the mantissa and the exponent (we represent it by using mathematical
multiplication ×).
    The algorithm f ltSQR to compute floating-point approximations of the
square root function for floating-point argument is presented in Fig. 7. In this
algorithm
 – mixSQR is the algorithm from Fig. 6,
 – an “input” variable A and the “output” variable B are of the floating-point
   type F ,
 – another “input” variable Eps has the fix-point type T ,
 – a variable Z is of the fix-point type T (but range within integers IntT ),
 – a machine operation ⊗ is the fix-point multiplication (specified in the sub-
   section 5.1),
 – and, finally, a constant βF is the exponent base (i.e. a fixed integer of type
   T ).

Recall that the algorithm mixSQR uses (within its scope) its own “local” vari-
ables and a constant:

 – the “output” and “input” variables X and Y are of the fix-point type T ,
 – the variables K and N are also of the fix-point type T (but range within
   integers IntT ),
 – the variable Stp of the fix-point type T is the step of indexes of the look-up
   table root;
 – the look-up table root is an array of the fix-point type T contains pre-
   computed upper approximations for square root for indexes;
 – and a constant δT is the step of the fix-point type T (i.e. a fixed real value
   of type T that is the minimal positive value of this type).

   Specification of the algorithm f ltSQR follows below:

   [A ∈ V alF & Y > 0 & Eps ∈ V alT & Eps > 0 &
                            Stp
     & EP S ≥ 2δT (2 + log2 Eps )&
                     & STEP & ROOT & ROUND]                                  (16)
                                   √                      Exp(A)
                      f ltSQR [|B − A| < Eps + 2√δTβ × β b 2 c ],
                                                     
                                                           F


where b. . .c is integer round-down function.
    The assertion is easy to verify since the algorithm mixSQR is verified already
and the algorithm f ltSQR has loop-free flowchart (since the only loop is hidden
inside mixSQR in this chart). The only thing we need are annotations for control
points on the chart:

1. the precondition from (16);
2. the precondition from (15) extended by the following two conjuncts:
   (a) Y = if odd(Exp(A)) then M an(A) ⊗ βF else M an(A);
   (b) Z = if odd(Exp(A)) then (Exp(A) − 1) else Exp(A);
3. the postcondition from (15) extended by the same two conjuncts 2a and 2b;
4. the postcondition from (16).

   Proof of the paths (1+2) and (1–2) are straightforward.
   Let us proof the path (2..3). For it let us assume that the condition assigned
to the control point 2 is true. It implies that before exercise of mixSQR the
precondition in (15) is true; due to the correctness of the assertion (15), the
algorithm mixSQR terminates and upon its termination the postcondition in
(15) is true also. Remark also that conjuncts 2a and 2b remains true since
mixSQR doesn’t change neither Y nor A. Hence the condition assigned to the
control point 3 is true. It finishes the proof of the path (2..3).
   For proving the last path (3..4) firstly let us prove that the condition in the
control point (3) implies the next two properties:
                                Z    Exp(A)
                                  =b        c,                                (17)
                                2      2
             p
      |X −       if odd(Exp(A)) then M an(A) × βF else M an(A)| < 
                                                                              (18)
                                                     < Eps + 2√δTβ .
                                                                        F

The first property (17) directly follows from the condition (2b). The prove of
the second one follows below:
Exp(a) is even: The radicand and the variable Y (in algorithm mixSQR) both
   equal M an(A); hence
         p
   |X − if odd(Exp(A))√ then M an(A) ⊗ βF else M an(A)| =
              = |X − Y | < (because assertion (15) is correct)<
                                                   < Eps < Eps + 2√δTβ .
                                                                         
                                                                                  F


Exp(a) is odd: The radicand equals M an(A) × βF and the variable Y equals
   M an(A) ⊗ βF ; hence
         p
   |X − ifpodd(Exp(A)) then M an(A) × βF else M an(A)| =
   = |X − M   pan(A) × βF | <        p                    p
     < |X − M an(A) ⊗ βF | + | M an(A) ⊗ βF − M an(A) × βF | <
                    (due to correctness pof the assertion (15))
                                                             p
                            < Eps + | M an(A) ⊗ βF − M an(A) × βF | <
       (because of properties of the fix-point arithmetic, where |∆| < δ2T )
                                   p                         p
                       < Eps + | M an(A) √      × βF + ∆ − √ M an(A) × βF | <
                                                                  ∆
        (because of Taylor expansion of t + ∆ as a series t + √    t
                                                                     + . . .)
                   p                          ∆
                                                             p
        < Eps + | M an(A) × βF + √                    + ... − M an(A) × βF | <
                                          M an(A)×βF
                                                                    ∆
                                                  < Eps + | √              + ...| <
                                                                M an(A)×βF
                                            √
         (because the Taylor expansion of       t + ∆ is an alternating series)
                                                      < Eps + | √ δT            |<
                                                                 2   M an(A)×βF
                                       <(because 1 < M an(A))< Eps + 2√δTβ .
                                                                                      F


As soon as it is proved that the properties (17) and (18) are valid in the control
point (3), the proof of the path (3..4) become trivial.
   It finishes pen-and-paper verification of specified algorithm computing ap-
proximations for the square root with floating-point arithmetic.


8   Conclusion
Let us summarise the content of the paper.
   Firstly we take a very standard Newton method to compute square root,
present is as an iterative algorithm SQR, specify it by Hoare total correctness
assertion, and prove its validity in the case when input argument is greater
than 1, accuracy is positive, and “computer” is precise (i.e. all computations are
done in mathematical real numbers); the upper bound of loop iterations of the
algorithm SQR is logarithmic.
    Next we improve the algorithm SQR by using an auxiliary function to com-
pute better initial approximations for square roots (it results in the algorithm
ISQR) and then suggest a for-loop-based algorithm F SQR that uses the same
auxiliary function, computes a lower bound for the number of iterations that is
sufficient to achieve the specified accuracy; both algorithms ISQR and F SQR
work with precise arithmetic, but we prove that F SQR achieves better accuracy
than ISQR, and can achieves better accuracy if to increase the number of the
loop iterations.
    Then we convert for-loop-based algorithm with precise arithmetic F SQR
into algorithm f ixSQR with fix-point arithmetic, specify it by total correctness
assertion and prove its validity by adjustment of its runs with runs of F SQR
with the same input data. Another specifics of the algorithm f ixSQR is use a
look-up table (arrange as an array) for upper approximations of square roots
and rounding-up function.
    Use of a machine fix-point arithmetic instead of the precise arithmetic results
in situation that more iterations of the loop doesn’t always improve accuracy in
contrast to F SQR. Due to this reason we suggest an other algorithm mixSQR
that is a specialised version of the algorithm f ixSQR.
    Finally we use the algorithm mixSQR as a subroutine in algorithm f ltSQR
that computes approximations of the square root function in floating-point arith-
metic. For this we assume that each floating-point number is represented as its
mantissa and exponent, and both — the mantissa and exponent — are fix-point
numbers. We specify the algorithm by a total correctness assertion and prove its
correctness (basing on the correctness of the algorithm mixSQR).
    All proofs in this paper are human-driven and oriented pen-and-paper proofs.
So the next topic of our project is to validate all these proofs with aid of some
automated proof-assistant. We are going to use ACL2 due to industrial strength
of this proof-assistant [13] for platform-specific verification of the standard math-
ematical functions (but don’t rule out alternatives to this assistant).
    Nevertheless remark that we attempt and present in this paper an approach
that we call platform-independent. Also remark that we don’t attempt to build
an axiomatization of an “abstract” machine (fix-point or floating-point) arith-
metics. Instead we just make several explicit assumptions about machine arith-
metic (and how it relates to the precise arithmetic) that are sufficient to validate
specifications and algorithms with machine arithmetic by using its relations with
specifications and algorithms with precise arithmetics. We believe that our as-
sumptions about machine arithmetic are valid for many platforms and they are
easy to check. Remark that if a platform’s machine arithmetic meets these as-
sumptions then properties of the algorithms mixSQR and f ltSQR exercised on
this platform are specified by total correctness assertions (15) and (16) respec-
tively.
   Let us group together and list in one place our assumptions about fix-point
and floating-point machine arithmetic that we introduce in the subsection 5.1
and the section 7) and use in this paper:

Fix-point arithmetic: We understand fix-point numeric data type T as fol-
   lows:
     – the set of values V alT is a finite subset of mathematical reals R such
       that
         • it comprises all reals in some finite range [− inf T , supT ], where inf T >
            2, supT > 2, with some fixed step 21 > δT > 0,
         • and includes all integer numbers IntT in this range [− inf T , supT ];
     – legal binary arithmetic operations are
         • addition and subtraction; if not the range overflow exception then
            these operations are precise: they equal to the standard mathemati-
            cal operations assuming their mathematical results fall in the range
            [− inf T , supT ] (and due to this reason are denoted as + and −);
         • multiplication ⊗ and division ; these operations are approximate
            but correctly rounded in the following sense: for all x, y ∈ V alT
              ∗ if x × y ∈ V alT then x ⊗ y = x × y;
              ∗ if x/y ∈ V alT then x y = x/y;
              ∗ if x × y ∈ [− inf T , supT ] then |x ⊗ y − x × y| < δT /2;
              ∗ if x/y ∈ [− inf T , supT ] then |x y − x/y| < δT /2.
     – legal binary relations are equality and all standard inequalities; these re-
       lations are precise, i.e. they equal to the standard mathematical relations
       (and due to this reason are denoted as =, 6=, ≤, ≥, <, >).
Floating-point arithmetic We understand floating-point numeric data type
   F as follows:
     – the set of values V alF is a finite subset of mathematical reals R that com-
       prises some reals in some finite range [− inf F , supF ], where inf F , supF >
       2 and {0, inf F , supF } ⊆ V alF ;
     – there are two unary operations M an : V alF → V alT (called mantissa),
       Exp : V alF → IntT (called exponent), and an integer constant βT ∈
       IntF (called exponent base or just base) such that for all positive x ∈
       V alF
         • 1 < M an(x) < sup    βF ;
                                  T


         • if infT is odd then −infT < Exp(x) else −infT ≤ Exp(x);
                                Exp(x)
         • x = M an(x) × βF            .

    Let us remark that our fix-point and floating-point numeric types are internal
or instant types in the following sense:

 – a program language provides numeric user-types integer, real, etc. (they
   may be int and/or long int, float and/or double in C, or integer and
   real in Pascal, etc.) with type-, implementation-, and platform-dependent
   the unit of least precision (or unit in the last place) ulpτ ∈ R, where τ is a
   “complex parameter” (type, implementation, platform);
 – our fix-point type T and floating-point type F are types for microprograms
   to implement algorithms mixSQR and f ltSQR in such a way that there
   exist values ε > 0 and s > 0 for variables Eps and Stp that guaranty exact
   accuracy of the implemented mixSQR and f ltSQR, (i.e. ulp     2
                                                                   τ
                                                                     > ε in the
                                                  ulpτ         δ
   case of integer and algorithm mixSQR, and 2 > ε + 2√Tβ in the case
                                                                   F
   of real and algorithm f ltSQR).

    Finally let us mention one more research topic — to find an “optimal bal-
ance” between size of the array root with initial upper approximations for square
roots for selected arguments, number of iterations of the loop in the algorithm
f inSQR, and accuracy of the square root approximation: if ε and s are values of
the variables Eps and Stp then the array size is sup T
                                                       , number of iterations may
                                                √ s
be any n ≥ 1 + dlog2 ε e , and accuracy |X − Y | is less than 2sn + n × δT .
                       s
                                                                               



References

1. Ayad A., Marché C. Multi-prover verification of floating-point programs // Lecture
   Notes in Artificial Intelligence. 2010. Vol. 6173. P.127–141.
2. Barret G. 1989. Formal Methods Applied to a Floating-Point Number System //
   IEEE Trans. Softw. Eng. 1989. Vol. 15(5). P.611–621.
3. Brain M., Tinelli C., Ruemmer Ph., and Wahl T. An Automatable Formal Semantics
   for IEEE-754 Floating-Point Arithmetic // Proceedings of the 2015 IEEE 22nd
   Symposium on Computer Arithmetic (ARITH ’15). IEEE Computer Society. 2015.
   P160–167.
4. Ferguson W.E. (Jr), Bingham J., Erkok L., Harrison J.R., Leslie-Hurd J. Digit
   serial methods with applications to division and square root (with mechanically
   checked correctness proofs) // 2017. Eprint arXiv:1708.00140. https://arxiv.org/
   abs/1708.00140. (Visited December 19, 2017.)
5. Gamboa R.A. Square Roots in Acl2: a Study in Sonata Form // Technical Report.
   University of Texas at Austin, USA. 1997.
6. Gries D. The Science of Programming. Springer-Verlag, 1981.
7. Harrison J. A Machine-Checked Theory of Floating Point Arithmetic // Lecture
   Notes in Computer Science. 1999. Vol. 1690. P. 113–130.
8. Harrison J. Formal Verification of Floating Point Trigonometric Functions // Lec-
   ture Notes in Computer Science. 2000. Vol. 1954. P.217-233.
9. Harrison J. Formal Verification of IA-64 Division Algorithms // Lecture Notes in
   Computer Science. 2000. Vol. 1869. P. 233–251.
10. Harrison J. Floating Point Verification in HOL Light: The Exponential Function
   // Formal Methods System Design. 2000. Vol. 16(3). P. 271–305.
11. Harrison J. Formal Verification of Square Root Algorithms // Formal Methods in
   System Design. 2003. Vol. 22(2). P.143–153.
12. Hoare C.A.R. The Verifying Compiler: A Grand Challenge for Computing Research
   // Lecture Notes in Computer Science. 2003. Vol. 2890. P. 1–12.
13. Grohoski G. Verifying Oracle’s SPARC Processors with ACL2. Slides of the In-
   vited talk for 14th International Workshop on the ACL2 Theorem Prover and
   Its Applications. http://www.cs.utexas.edu/users/moore/acl2/workshop-2017/
   slides-accepted/grohoski-ACL2_talk.pdf. (Visited December 19, 2017.)
14. Gutowski M.W. Power and beauty of interval methods. arXiv:physics/0302034
   [physics.data-an]. http://arxiv.org/pdf/physics/0302034.pdf. (Visited Decem-
   ber 19, 2017.)
15. Kochan S.G. Programming in C: A Complete Introduction to the C Program-
   ming Language. Functions Calling Functions at p.131. Sam’s Publishing, 2005 (3rd
   Edition).
16. Kuliamin V. Standardization and Testing of Mathematical Functions // Program-
   ming and Computer Software. 2007. Vol. 33, n. 3. P. 154–173.
17. Kuliamin V.V. Standardization and Testing of Mathematical Functions in floating
   point numbers // Lecture Notes in Computer Science. 2010. Vol. 5947. P. 257–268.
18. Monniaux D. The pitfalls of verifying floating-point computations // ACM Trans-
   actions on Programming Languages and Systems. 2008. Vol. 30, n. 3. P.1–41.
19. Muller J.-M. Elementary Functions: Algorithms and Implementation. Birkhauser,
   2005.
20. Sawada J., Gamboa R. Mechanical Verification of a Square Root Algorithm Using
   Taylor’s Theorem // Lecture Notes in Computer Science. 2002. Vol. 2517. P. 274–
   291.
21. Shelihov V.I. Verification and synthesis of efficient programs for standard functions
   flor, isqrt and ilog2 using predicate programming technology // Proceedings of
   12 Int. Conf. on Control and modelling of complex systems. Samara: Samara Science
   Center of Russian Academy of Science. 2010. P.622-630. (In Russian.)
22. Shilov N.V. On the need to specify and verify standard functions // The Bulletin
   of the Novosibirsk Computing Center (Series: Computer Science). 2015. n.38, p.105–
   119.
23. Shilov N.V., Promsky A.V. On specification andd verification of standard mathe-
   matical functions // Humanities and Science University Journal. 2016. n.19, p.57–
   68.
24. Siddique U., Hasan O. On the Formalization of Gamma Function in HOL // 2014.
   J. Autom. Reason. Vol. 53(4). P. 407–429.
25. C refernce. Sqrt, sqrtf, sqrtl. http://en.cppreference.com/w/c/numeric/math/
   sqrt. (Visited December 19, 2017.)
26. IEEE 754-2008. http://ieeexplore.ieee.org/document/4610935. (Visited De-
   cember 19, 2017.)
27. ISO/IEC/IEEE 60559:2011. Information technology -- Microprocessor Systems --
   Floating-Point arithmetic http://www.iso.org/iso/iso_catalogue/catalogue_
   tc/catalogue_detail.htm?csnumber=57469. (Visited December 19, 2017. In Rus-
   sian.)
28. Roskosmos called the reason of unsuccessful start from the East spaceport https:
   //news.mail.ru/politics/31931345/. (Visited December 19, 2017.)
A    Specification of the sqrt function

The C reference portal at en.cppreference.com/w/c specifics the the square
root function sqrt [25] as it represented below.


    C Numerics Common mathematical functions
    sqrt, sqrtf, sqrtl
    Defined in header <math.h>
    float sqrtf( float arg ); (1) (since C99)
    double sqrt( double arg ); (2)
    long double sqrtl( long double arg ); (3) (since C99)
    Defined in header <tgmath.h>
    ]define sqrt( arg ) (4) (since C99)
    1-3) Computes square root of arg.
    4) Type-generic macro: If arg has type long double, sqrtl is called.
    Otherwise, if arg has integer type or the type double, sqrt is called.
    Otherwise, sqrtf is called. If arg is complex or imaginary,
    then the macro invokes the corresponding complex function
    (csqrtf, csqrt, csqrtl).
    Parameters
    arg - floating point value
    Return value
                                              √
    If no errors occur, square root of arg ( arg), is returned.
    If a domain error occurs, an implementation-defined value is returned
    (NaN where supported).
    If a range error occurs due to underflow, the correct result (after rounding)
    is returned.
    Error handling
    Errors are reported as specified in math errhandling.
    Domain error occurs if arg is less than zero.
    If the implementation supports IEEE floating-point arithmetic (IEC 60559),
    • If the argument is less than −0, FE INVALID is raised and NaN is returned.
    • If the argument is +∞ or ±0, it is returned, unmodified.
    • If the argument is NaN, NaN is returned
    Notes
    sqrt is required by the IEEE standard be exact.
    The only other operations required to be exact are the arithmetic operators
    and the function fma. After rounding to the return type
    (using default rounding mode),
    the result of sqrt is indistinguishable from the infinitely precise result.
    In other words, the error is less than 0.5 ulp.
    Other functions, including pow, are not so constrained.
