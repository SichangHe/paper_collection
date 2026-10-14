                                                        Towards platform-independent
                                                         specification and verification
                                                   of the standard trigonometry functions?

                                         Nikolay V. Shilov1 , Boris L. Faifel2 , Svetlana O. Shilova3 , Aleksey V. Promsky4
                                                       1
                                                       Innopolis University, Innopolis, Russia, shiloviis@mail.ru,
arXiv:1901.03414v1 [cs.LO] 10 Jan 2019




                                          2
                                              Yu. Gagarin State Technical University of Saratov, Russia, catstail@yandex.ru,
                                                           3
                                                             retired, Novosibirsk, Russia shilov61@inbox.ru,
                                                   4
                                                     A.P. Ershov Institute of Informatics Systems, Novosibirsk, Russia
                                                                          promsky@iis.nsk.su




                                                  Abstract. Research project “Platform-independent approach to for-
                                                  mal specification and verification of standard mathematical functions” is
                                                  aimed onto a development of an incremental combined approach to the
                                                  specification and verification of the standard mathematical functions like
                                                  sqrt, cos, sin, etc. Platform-independence means that we attempt to
                                                  design a relatively simple axiomatization of the computer arithmetic in
                                                  terms of real, rational, and integer arithmetic (i.e. the fields R and Q of
                                                  real and rational numbers, the ring Z of integers) but dont specify neither
                                                  base of the computer arithmetic, nor a format of numbers representation.
                                                  Incrementality means that we start with the most straightforward spec-
                                                  ification of the simplest easy to verify algorithm in real numbers and
                                                  finish with a realistic specification and a verification of an algorithm in
                                                  computer arithmetic. We call our approach combined because we start
                                                  with a manual (pen-and-paper) verification of some selected algorithm
                                                  in real numbers, then use these algorithm and verification as a draft and
                                                  proof-outlines for the algorithm in computer arithmetic and its manual
                                                  verification, and finish with a computer-aided validation of our manual
                                                  proofs with some proof-assistant system (to avoid appeals to “obvious-
                                                  ness” that are very common in human-carried proofs). In the paper we
                                                  present first steps towards a platform-independent incremental combined
                                                  approach to specification and verification of the standard functions cos
                                                  and sin that implement mathematical trigonometric functions cos and
                                                  sin.
                                                  Keywords: fix-point numbers, floating-point numbers, computer/mach-
                                                  ine arithmetic, formal verification, partial and total correctness, Hoare
                                                  triples, Floyd verification method of inductive assertions, irrational num-
                                                  bers, periodic real functions, Taylor expansion/series, Chebychev polyno-
                                                  mials

                                         ?
                                              This research is supported by Russian Basic Research Foundation grant no. 17-
                                              01-00789 Platform-independent approach to formal specification and verification of
                                              standard mathematical functions.
1   Introduction

One who has a look at verification research and practice may observe that
there exist verification in large (scale) and verification in small (scale): ver-
ification in large deals (usually) behavioral properties of large-scale complex
critical systems like the Curiosity Mars mission [11], while verification in small
addresses (usually) functional properties of small programs like computing the
standard trigonometry functions [9]. Verification of behavioral properties of a
safety/mission/avalability-critical system doesn’t guaranty safety/liveness/fair-
ness of the system but may detect some bugs that may cause a very expensive
and/or fatal system failure (like launch failure from launch-site “Vostochny”
November 28, 2017, [16]). At the same time verification in small also is of the
high importance: a tiny bug/mistake/error in a small but frequently/massively
used function/program may cause a huge money losses; it is true in particular
for the standard computer functions (available in the standard libraries) [8]. Of
course this division of the verification research onto two streams — in large and
in small scale — is just a split not a break because all verification research work
altogether towards incorporation of the formal verification into the software de-
velopment cycle — at compilation/linking stages maybe [10].
    Our paper deals with verification in small, in particular, it looks like that it
is about the same topic as [9] i.e. formal verification of two standard computer
functions cos and sin that implement well-known trigonometry mathematical
real functions cos, sin : R → R. But there are serious differences between [9] and
our paper. Firstly, the cited paper is platform-dependent (IntelrIA-64 architec-
ture), its approach is neither incremental nor combined; next it provides neither
definition of the both cos and sin functions, nor specification of their computer
partners cos and sin; finally, because of use of HOL-light, all algorithms in
the cited paper are functional but not imperative. In contrast, in our paper
we present platform-independent and incremental approach, based on provided
formal definition for mathematical functions, discuss several variants of formal
specifications for their computer partners, use Hoare total correctness asser-
tions [1,7] for logical specification of imperative algorithms that implements the
computer functions, and finish with manual (pen-and-paper) verification (using
Floyd-Hoare approach [1,7]) of the computer functions for argument value in the
rage [−1, 1] (in radian measure). (Thus we postpone computer-aide validation
of our proof for the future while the paper [9] have done computer-aided formal
verification.)
    Our present paper is a next one in a series of our papers devoted to the
development of a platform-independent incremental combined approach to spec-
ification and verification of the standard mathematical functions [17,18,19,20].
Position papers [17,18] have stated our concern regarding a need of

 – better specification and incremental combined platform-independent verifi-
   cation of standard functions,
 – introduction and standardization of a certification process for the standard
   functions,
 – inclusion of an incremental combined platform-independent verification into
   this certification.
    A work-in-progress electronic preprint [19] has presented a human-oriented
specification and pen-and-paper verification of a computer square root func-
tion that implements Newton-Raphson method by non-adaptive for-loop (with
a pre-computed number of iterations) and uses a look-up table for initial ap-
proximations. The specification in [19] has been presented as a total correctness
                                                                            √
assertion with use of precise arithmetic and the mathematical square root . . .,
algorithms has been presented by imperative pseudo-code with explicit distinc-
tion between precise and machine arithmetic, manual verification has been done
in Floyd-Hoare style and adjustment (matching) of runs of algorithms with pre-
cise arithmetics and with machine arithmetics. It is possible to say that the
primary contribution of the paper [19] was an axiomatisation of properties of
a machine (fix-point as well as floating-point) arithmetic that are sufficient to
carry out the verification.
    A journal (Russian) paper [20] is based on an improved axiomatization from
[19]. In the cited paper an adaptive imperative algorithm implementing the same
Newton-Raphson method for a square root function has been specified by total
correctness assertions and verified manually using Floyd-Hoare approach in both
fix-point and floating-point arithmetics; the post-condition of the total correct-
ness assertion states that the final overall error is not greater that 2ulp where
ulp is Unit in the Last Place — the unit of the last meaningful digit. The paper
[20] has reported two steps towards computer-aided validation and verification
of the used adaptive algorithm:
 – an implementation of a fix-point data type according to the axiomatization
   can be found at https://bitbucket.org/ainoneko/lib_verify/src/,
 – ACL2 proofs of
     • the consistency of the computer arithmetics axiomatization,
                                                                       √
     • the existence of a look-up table with initial approximations for . . .
   can be found at https://github.com/apple2-66/c-light/tree/master/
   experiments/square-root.
    The paper is organized as follows. In the next section 2 we discuss and re-
call definitions and properties of the constant π and two trigonometric functions
cos ≡ λx ∈ R. (cos x) and sin ≡ λx ∈ R. (sin x). Then in the section 3 we discuss
how to compute, specify, and verify approximations of π in the real arithmetics;
this section serves as a bridge to the section 4 where we discuss computation,
specification, and verification of approximations for values the trigonometric
functions cos and sin in the real arithmetics. (Also in future research we will
need a verified algorithm to compute approximations of π.) In the section 5 we
present some shocking experiments with direct implementation on conventional
computers (that use floating-point arithmetic) of algorithms presented and ver-
ified (for the real arithmetic) in the previous section 4: it turns out that the
trigonometric functions cos and sin can get values out of the range [−1, 1] even
for moderate argument values! Due to these shocking experiments we turn to
                  Fig. 1. Geometric definition of cos α and sin α


fix-point arithmetic (and axiomatize it), design, specify and verify (manually)
algorithms to compute approximations of the trigonometric functions cos and sin
working in fix-point arithmetic with small argument values in the range [−1, 1]
(i.e. that approximate functions λx ∈ [−1, 1]. (cos x) and λx ∈ [−1, 1]. (sin x)).
Thus we postpone study of computation, specification, and verification of ap-
proximations in floating-point arithmetic of the functions cos and sin for the
future; we discuss in brief this research topic and other future research topics in
the last concluding section 7.


2   What are trigonometric functions cos and sin
Let us refer Fig.1 to give a geometric definition for the trigonometry func-
tions cos, sin : R → R and some other related definitions. By definition [14],
Archimedes’ constant π is the ratio of a circle’s circumference to its diame-
ter. Also by definition [15], radian measure of the angle between rays defined by
                −→       −−→                                             a
                                    L
radius-vectors OA and OB is α = R      where L is the length of the arc AB. Finally,
by definition [21], cosine cos α and sine sin α of the angle between two radius-
        −→         −−→
vectors OA and OB with radian measure α is defined as follows: cos α = X     R and
sin α = YR ; the following basic equalities immediately follow from definitions and
geometric arguments (Pythagorean theorem and triangle equalities):
           2          2
 – (cos α) + (sin α) = 1 (or shortly cos2 α + sin2 α = 1);
 – cos α = cos(−α) and
                      sin(−α)  =−  sin α;
 – cos α = sin π2 + α =  sin π
                             2 − α  ;
 – sin α = − cos π2 + α = cos π2 − α ;
                       
 – cos α = − cos(α + π) = cos(α + 2π);
 – sin(α) = − sin(α + π) = sin(α + 2π).
   More complicated are the following trigonometric addition formulas [23]:
 – cos(α + β) = cos α · cos β − sin α · sin β,
 – cos(α − β) = cos α · cos β + sin α · sin β,
 – sin(α + β) = cos α · sin β + sin α · cos β,
 – sin(α − β) = cos α · sin β − sin α · cos β,
where α and β are radian measures of two angles. These formulas imply the
following double-angle [24] and half-angle [25] formulas
 – cos 2α = cos2 α − sin2 α,
 – sin 2α = 2 cos α · sinqα,
                b α+π c
 – cos α2 = (−1) 2π         1+cos α
                               2    ,
                  α
                      q
                b c
 – sin α2 = (−1) 2π       1−cos α
                             2    ,

where α is the radian measures of an angle and (λ x. bxc) : R → Z is the floor
function that truncates each real number to the largest integer that isn’t greater
than the number.
    Since cos α and sin α are defined for every radian measure α ∈ R, one
can define two functions cos, sin : R → [−1, 1] as cos = (λα ∈ R. cos α) and
sin = (λα ∈ R. sin α); remark that in Calculus and Real Analysis the bound
variable of the function is usually denoted by x, y, z instead of α [21]. Since
our paper is about specification and verification of computations of approximate
values of these two trigonometric functions cos and sin we will refer them in this
paper as the trigonometric functions (while in more general context the list of
trigonometric functions [21] includes also other functions that can be derived
from cos and sin ).
    It immediately follows from the above basic equalities that these functions
satisfy the Pythagorean equality

                                  cos2 x + sin2 x = 1                         (1)

for all x ∈ R. It also immediately follows from the same basic equalities, that
both functions are periodic with 2π as the smallest period, i.e.:
                        cos (x + 2π) = − cos (x + π) = cos x,
                                                                              (2)
                        sin (x + 2π) = sin (x + π) = sin x
for all x ∈ R. It follows from the trigonometric addition formulas that
                       cos(x + y) = cos x · cos y − sin x · sin y,
                                                                              (3)
                       sin(x + y) = cos x · sin y + sin x · cos y
for all x, y ∈ R; also, it follows from the double-angle formulas that
               cos 2x = cos2 x − sin2 x = 2 cos2 x − 1 = 1 − 2 sin2 x,
                                                                              (4)
               sin 2x = 2 cos x · sin x
for all x ∈ R; finally, it follows from the double-angle formulas that
                                                   q
                                           b x+π c
                             cos x2 = (−1) 2π        1+cos x
                                                        2    ,
                                                 x
                                               b c
                                                    q                                 (5)
                             sin sin x2 = (−1) 2π      1−cos x
                                                          2

for all x ∈ R.


3   Computing π in Reals

Definition for the constant π provided in the previous section aren’t convenient
to compute their values because of a geometric nature of these definitions. So
we need better ways to compute this constant.
   The following fabulous story is a quotation from the paper [17] that was a
position paper motivating a need for better specification and verification of the
standard mathematical function.

     The mathematical irrational number π is the ratio of a circle’s circum-
    ference to its diameter D; it is also a well-known mathematical fact that
    the area of the circle is (π × D2 )/4, i.e. it is π/4 of the area of the square
    built on the circle’s diameter. This observation leads to the Monte Carlo
    method for computing an approximation of π as follows (Fig. 2-left):
    draw a segment of a circle in the first quadrant and the square around
    it, then randomly place dots in the square; the ratio of the number of
    dots inside the circle to the total number of dots should be approximately
    equal to π/4...
     The C-program depicted in Fig. 2-right implements the above Monte
    Carlo method to compute an approximation for π. It prescribes to ex-
    ercise 10 series of 1,000,000 trials each. This code was developed by a
    Computer Science instructor to teach first-year students C-loops by an
    example of a very intuitive algorithm. There were 25 students in the class
    that used either Code::Blocks 12.11 or Eclipse Kepler IDEs for C/C++
    with MinGW environment...
     Imagine the embarrassment of the instructor when each of 25 students
    in the class got 10 times the value 4.000000 as an approximation for π!

   Please refer papers [17,18] for detailed discussion what was wrong with the
described 25 computational experiments and for a human “proof” that π is
4.000000 indeed. But we have to rule the idea to compute π using Monte Carlo
methods because of impossibility to generate random numbers (but pseudo-
random only) that are used in the method.
   Instead one can compute approximations for π using series — for example,
a Leibnitz’ series [14]

        π      1 1 1                1            X         1
          = 1 − + − + . . . (−1)n        + ... =   (−1)n        .                     (6)
        4      3 5 7              2n + 1                 2n + 1
                                                           n≥0
 Fig. 2. Idea (left) and C-code (right) to compute Monte Carlo approximation for π


This series representation for π results from series representation of the arctan-
gent function
                                      X          x2n+1
                           arctan x =      (−1)n
                                                 2n + 1
                                      n≥0

that is valid for all for arguments x ∈ [−1, 1]. The series 6 converges according
to Leibnitz criterion for the alternating series [26] but slowly: for every n ∈ N
its convergence rate is
                                                    
            π           1 1 1              n     1              1
              − 1 − + − + . . . (−1)                    ≤              ;       (7)
            4           3 5 7                2n + 1       2(n + 1) + 1
for example, if we would like to get accuracy 0.001 for π we should compute and
summarise (almost) 2,000 terms of the series!
    Nevertheless Leibnitz’ series gives a way to define π and compute its valid
approximations using exact real arithmetics:
 – an algorithm P iCodeInReals in Fig. 3 “inputs” accuracy ε > 0, uses vari-
   ables capable to store (exactly) real numbers and exercise (exactly) the stan-
   dard real operations, and “outputs” an approximation π with (at least) this
   accuracy ε;
 – total correctness assertion that specifies the algorithm is

                       [ε > 0] P iCodeInReals [|π − pi| ≤ ε]                    (8)

    where π is defined by (6).
   It is easy to verify manually the total correctness assertion (8):
 – if ε > 0, then the algorithm terminates after d 2ε − 32 e iteration of the loop
   (2 + 2), where (λ x. dxe) : R → Z is the ceiling function that rounds up each
   real number to the least integer that isn’t smaller than the number;
                                                  qp := 1 ; n := 1 ; sign := −1 ;
                                                  while 4ε < 2n+1
                                                               1
                                                                   do
                                                                             1
                                                         qp := qp + sign × 2n+1  ;
                                                         n := n + 1 sign := −sign od
                                                  pi := 4 × qp



Fig. 3. A flowchart (left) and the pseudo-code (right) of the algorithm P iCodeInReals


 – partial correctness of the algorithm with respect to the same pre-condition
   and the postcondition can be proved by Floyd-Hoare method [1,7] with
                                                                      
                                                 m=(n−1)
                                                    X             1 
         precondition & sign = (−1)n & qp =             (−1)m
                                                   m=0
                                                               2m  +1

    as the invariant of the control point 2 and using (7) to prove the exit path
    (2 − 3).


4    Computing the trigonometric functions in Reals

As for the constant π, the definitions for the functions cos and sin provided in
the section 2 aren’t convenient to compute their values because of a geometric
nature of these definitions. So we need better ways to compute these functions.
   Both functions are smoothness and can be represented by Taylor series [21]:
                     2         4                2n
                                                                    n x2n
       cos x = 1 − x2! + x4! + . . . (−1)n (2n)!
                                            x
                                                             P
                                                 + ... =    n≥0 (−1) (2n)! ,
                     3     5
                                            x2n+1                        x2n+1
                                                                                         (9)
       sin x = x − x3! + x5! + . . . (−1)n (2n+1)! + . . . = n≥0 (−1)n (2n+1)!
                                                            P
                                                                               .

Both series are alternating absolutely converging series for all x ∈ R, and —
moreover — according to Leibnitz criterion for the alternating series [26], for
every n ∈ N, if |x| ≤ 2n then
                           2    4
                                                       
                                                  x2n       x2n+2
             cos x − 1 − x2! + x4! + . . . (−1)n (2n)!   ≤ (2n+2)! ,
                                                                                      (10)
                                  3     5
                                                         x2n+1             x2n+3
              sin x −       x − x3! + x5! + . . . (−1)n (2n+1)!       ≤   (2n+3)!   .

   Very similar to the way to compute π approximations, the series (10 give a
way to define functions cos and sin and compute their approximate values using
exact real arithmetics.

Cosine:
                                                cs := 1 ; n := 1 ; sign := −1 ;
                                                        2
                                                tc := x2 ;
                                                while ε < tc do
                                                        cs := cs + sign × tc ;
                                                        n := n + 1 ; sign := −sign ;
                                                                      x2
                                                        tc := tc × 2n(2n−1) od



Fig. 4. A flowchart     (left)   and   the   pseudo-code   (right)   of   the   algorithm
CosCodeInReals


     – an algorithm CosCodeInReals in Fig. 4 “inputs” argument value x and
       accuracy ε > 0, uses variables capable to store (exactly) real numbers
       and exercise (exactly) the standard real operations, and “outputs” an
       approximation for cos x with (at least) this accuracy ε;
     – total correctness assertion that specifies the algorithm is

                     [0 < ε < 1] CosCodeInReals [|cs − cos x| ≤ ε]                  (11)

       where cos x is defined by (10).
Sine:
     – an algorithm SinCodeInReals in Fig. 5 “inputs” argument value x and
       accuracy ε > 0, uses variables capable to store (exactly) real numbers
       and exercise (exactly) the standard real operations, and “outputs” an
       approximation for sin x with (at least) this accuracy ε;
     – total correctness assertion that specifies the algorithm is

                      [0 < ε < 1] SinCodeInReals [|cs − sin x| ≤ ε]                 (12)

        where sin x is defined by (10).
   Manual verification of the total correctness assertions (11) and 12) is very
similar to each other and similar (a little bit more complicated) to the verification



                                                sn := x ; n := 1 ; sign := −1 ;
                                                        3
                                                ts := x6 ;
                                                while ε < ts do
                                                       sn := sn + sign × ts ;
                                                       n := n + 1 ; sign := −sign ;
                                                                     x2
                                                       ts := ts × 2n(2n+1) od



Fig. 5. A flowchart (left) and the pseudo-code (right) of the algorithm SinCodeInReals
of total correctness assertion 8) presented at the end of the previous section. Due
to this reason let us discuss below verification of the condition (11) only because
of a similarity of verification of (11) and 12).
    First let us prove partial correctness of the algorithm CosCodeInReals with
respect to the same pre-condition and the postcondition as in the total cor-
rectness assertion (11) using Floyd-Hoare method [1,7]. For it let us adopt the
following conjunction
                           
                             0<ε<1
                            sign = (−1)n
                           
                           
                                    x2n
                              tc = (2n)!                                        (13)
                           
                           
                                      m=(n−1)          2m
                                              (−1)m x
                           
                            cs =  P
                                     m=0              (2m)!

as the invariant of the control point 2. Pathes (1..2) and (2 + 2) are easy to
prove. Proof of the exit path (2 − 3) follows from the convergence rate (10) for
cos-function, but we should take care about the applicability condition of the
convergence rate: |x| ≤ 2n; this condition holds on this path since 1 > ε ≥ tc =
 x2n                    |x|         |x|                                           |x|
(2n)! implies that 1 > 2m or 1 > 2m−1 for some m ∈ [1..n] and, hence, 1 > 2n .
    Next let us prove termination. Let us fix “input” (i.e. initial) values x and ε >
                                      x2m
0. Let m = min n. (2n > |x|), p = (2m)!    , and let k = d log2 p−log
                                                                  2
                                                                      2ε
                                                                         e. According
                                                                             2n
                                                                       x
to the invariant (13), at the n-th iteration (n > 0) of the loop tc = (2n)! ; hence
at the (m + k)-th iteration of the loop
       2m                 2k
      x                 x
tc = (2m)! × Qi=k ((2m+(2i−1))(2m+2i))  =
              i=1
                                      2
                                                                  1 2
                      Qi=k          x
                                                Qi=k                
              = p × i=1 (2m+(2i−1))(2m+2i) < p × i=1              2    =
                                                                       2k
                                                              = p × 21     ≤ p × pε = ε,

i.e. after this iteration the algorithm terminates.


5   Computing the trigonometric functions on conventional
    computers

The previous section ends on a major note: Taylor series definition of the math-
ematical functions cos and sin is easy to

 – implement for approximate computations of values of these functions;
 – use in the specification and verification of these implementations.

But there are some objections against being too optimistic:

 – “easy implementation” assumes ability of store and manipulate (using the
   standard arithmetic operations) real numbers;
 – “easy verification” is based on a preliminary knowledge from Real Analysis
   and relay upon human logic reasoning skills.
 float CosCodeInC(float x, float eps) int TestCosInC(float min,
 { float cs,stc,doubn;                 float max, float step, float eps)
   cs=stc=dn=1;                       { float x,c;
   while (fabs(stc) > eps)              for (x=min; x<=max; x=x+step)
   { sigtc=-sigtc*x*x/(dn*(dn+1));      { c=CosCodeInC(x,eps);
     cs=cs+stc; dn+=2; }                  printf("%e %e \n",x,c); }
   return cs; }                         return 0; }

Fig. 6. C-function CosCodeInC (left) implements the algorithm CosCodeInReals; C-
function TestCosInC (right) tests the function CosCodeInC



    The most common machine approaches to represent some finite subset of
real numbers using fix-point and/or floating-point formats. Both concepts can
be defined as follows.

Fixed-point format has a fixed number (e.g. 4) for the sign and digits in the
   integer part (i.e. before the radix/decimal point) and a fix number (e.g. 2) of
   digits in the fractional part (i.e. after the radix point) of some fixed implicit
   (e.g. binary, decimal, etc.) positional notation; for example, in the specified
   fix-point format +003.14 is an approximation of π.
Floating-point format has a fixed number (e.g. 4) for the sign and digits of
   the significant/mantissa (usually integer) and a fixed number (e.g. 2) for the
   sign and digits of the exponent/magnitude (usually integer) represented in
   some fix-point formats (different maybe) and some fixed implicit base (also
   usually integer) of the exponent; usually the significant doesn’t have leading
   zeros; for example, +314 × 10−2 may be floating-point representation of an
   approximation of π with the significant +314, the exponent −02, and 10 as
   an implicit exponent base.

Fix-point format is quite common in assembly-level programming languages
but is rarely used in high-level programming languages; instead variants of the
floating-point formats are popular in high-level programming languages (e.g.
float, double, and long double in C-language [4]).
    Since series (10) for cos and sin are very similar as well as the algorithms
Fig. 4 and 5 that are based on these series, and different floating-point types in
different programming languages have similar problems with representation of
real values, let us consider and discuss below only a series-based implementation
of cos function in C-language with use of float data type. Then algorithm
CosCodeInReals (Fig. 4) can be implemented as function CosCodeInC presented
in the left part of the Fig. 6; in this function the variable stc is used for signed
tc (and assumed to be equal to −sign × tc), and the variable dn — for doubled
n (and assumed to be equal to 2n).
    Table 1 presents some test data for CosCodeInC with aid of the testing func-
tion TestCosInC (presented in the right part of the Fig. 6) for argument values in
the range [0, 30] (radians) with some fixed step (0.05) and accuracy (10−6 ). One
can remark a shocking results in the table 1: computed values of CosCodeInC
 x          CosCodeInC    x          CosCodeInC      x        CosCodeInC
 0.000e+000 1.000000e+000 1.850e+001 1.144768e+000 2.900e+001 1.315880e+004
 5.000e-002 9.987502e-001 1.900e+001 9.913036e-001 2.950e+001 3.822034e+003
 1.000e-001 9.950042e-001 1.950e+001 6.106047e-001 3.000e+001 -2.368533e+003
                    Table 1. Some tests data for CosCodeInC



(that are expected to be values of cos) are 1.144768 for 1.85 radians and even
13158.8 for 29 radians (that can’t be true)!
    The main reason of this non-tolerable inaccuracy with computing trigonomet-
ric functions using floating-point data formats are well-known [6]: while n ≤ x
                       n
the values of terms xn! in the series (10) are so big that later addition of small
         m
values xm! with x << m “vanish” because of normalization of floating point
values prior to addition.
    There are several ways to overcome the problem with computing values of
the trigonometric functions cos and sin in floating-point arithmetic [6]:
 – use series (10) to compute values of cos and sin for small argument values;
 – use
    • either periodicity (2) to reduce big argument values to the small ones,
    • or (for example) Chebychev polynomials
         ∗ to compute trigonometric functions for positive integer argument
           values (i.e. cos n and sin n for n ∈ N)
         ∗ and trigonometric addition formulas (3) to compute trigonometric
           functions for argument values comprising the integer and fractional
           parts (the later is in the range [0, 1)).
    Since in any cases there is a need to compute reliable approximations for the
values of the trigonometric functions for small argument values we concentrate in
this paper on computation, specification, and (manual) verification in machine
arithmetic for small argument values — namely for x ∈ [−1, 1] — and postpone
the study for big argument values for the future. Also, since all values are small,
in this paper we use not a floating-point but a fix-point format to represent the
real numbers in the range of [−1, 1].
    We would like to conclude this section with a remark that a move from
small argument values to big ones isn’t trivial: we strongly agree with Wikipedia
[22] that the computation of trigonometric functions is a complicated subject,
which can today be avoided by most people because of the widespread availability
of computers and scientific calculators but strongly disagree that modern tools
provide built-in trigonometric functions for any angle [22]. Indeed, in the C
reference [2] functions cos [3] and sin [5] return values are specified as follows.
cos: If no errors occur, the cosine of arg (cos(arg)) in the range [−1, 1], is
   returned. The result may have little or no significance if the magnitude of
   arg is large. (until C++11)
sin: If no errors occur, the sine of arg (sin(arg)) in the range [−1, 1], is returned.
   The result may have little or no significance if the magnitude of arg is large.
   (until C99)
These specifications are too much vague since they don’t explain neither what
are cos(arg) and sin(arg) (in particular when these values are irrational), no
what is significance, nor what is large magnitude.


6     The trigonometric functions in Fix-point Arithmetic
6.1     Fix-point Arithmetic
First we axiomatized a platform-independent fix-point arithmetic in the elec-
tronic preprint [19] and then improved the initial axiomatization in the journal
paper [20]. In the present paper we follow the later version, but explicitly admit
that there may be several different fix-point data types simultaneously.
   A fix-point data-type (with Gaussian rounding) D satisfies the following ax-
ioms.
 – The set of values V alD is a finite set of rational numbers Q (and reals R)
   such that
     • it contains the least inf D < 0 and the largest supD > 0 elements,
     • altogether with
         ∗ all rational numbers in [inf D , supD ] with a step δD > 0,
         ∗ all integers IntD in the range [− inf D , supD ].
 – Admissible operations include machine addition ⊕, subtraction , multipli-
   cation ⊗, division , integer rounding up d e and down b c.
   Machine addition and subtraction. If the exact result of the standard
       mathematical addition (subtraction) of two fix-point values falls within
       the interval [inf D , supD ], then machine addition (subtraction respective-
       ly) of these arguments equals to the result of the mathematical operation
       (and notation + and − is used in this case).
   Machine multiplication and division. These operations return values
       that are nearest in V alD to the exact result of the corresponding standard
       mathematical operation: for any x, y ∈ V alD
         • if x × y ∈ V alD then x ⊗ y = x × y;
         • if x/y ∈ V alD then x y = x/y;
         • if x × y ∈ [inf D , supD ] then |x ⊗ y − x × y| ≤ δD /2;
         • if x/y ∈ [inf D , supD ] then |x y − x/y| ≤ δD /2;
   Integer rounding up and down are defined for all values in V alD .
 – Admissible binary relations include all standard equalities and inequalities
   (within [inf D , supD ]) denoted in the standard way =, 6=, ≤, ≥, <, >.

6.2     Computing cos in Fix-point Arithmetic
Since we study the trigonometric functions for argument values in the range
[−1, 1], the algorithm CosCodeInReals presented in the Fig. 4 can be modified
as presented in the left part of the Fig. 7; the corresponding specification (11)
should be modified as follows:

      [(0 < ε < 1) & (−1 ≤ x ≤ 1)] CosCodeInZerOne [|cs − cos x| ≤ ε]         (14)
Fig. 7. Flowcharts     of   the    algorithms    CosCodeInZerOne        (left)   and
CosCodeInF ixP oint (right)


where cos x is defined by (10).
    Correctness of the specification (14) is easy to prove very similar to the proof
of the specification (11), but we need to modify the invariant (13) as follows:
                          
                          
                           0<ε<1
                          
                          
                           −1 ≤ x ≤ 1
                           sign = (−1)n
                          
                          
                            ep = (−1)n × (2n)! × ε        ;                     (15)
                                    2n
                          
                                 x
                           tc = (2n)!
                          
                          
                          
                           cs = Pm=(n−1) (−1)m x2m
                          
                                   m=0             (2m)!

this modified invariant can be used in the proof of the path (2 − 3) as follows:
           |ep| ≥ 1
       
       
        −1 ≤ x ≤ 1
       
                                             |ep|      1      x2n
           ep =  (−1) n
                        × (2n)! × ε ⇒ ε=          ≥        ≥       = tc;
       
                  2n
                                            (2n)!    (2n)!   (2n)!
                 x
           tc = (2n)!
       

since tc ≥ |cs − cos x|, it implies that |cs − cos x| ≤ ε.
    The above algorithm CosCodeInZerOne presented in the left part of the Fig.
4 can be converted into algorithm CosCodeInF ixP oint (with fix-point arith-
metic) presented in the right part of the Fig. 7; the corresponding specification
(11) should be modified as follows:
                                        
      δD < 1 &
     0 < ε < 1 & ε ∈ V alD &            
                                        
     ∃N ∈ IntD : ((2N )! × ε ≥ 1) & 
      −1 ≤ x ≤ 1 & x ∈ V alD                                                 (16)
                              CosCodeInF
                                       "    ixP oint               #
                                                               3nδD
                                       |csf p − cos x| ≤ ε + 2(1−δ D)
                                                                      &
                                       n = min {N : ((2N )! × ε ≥ 1)}
where (as usual in this paper) cos x is defined by (10). Please refer Appendix A
for a proof idea & sketch for the correctness of this assertion.
Fig. 8. Flowcharts     of   the     algorithms    SinCodeInZerOne        (left)   and
SinCodeInF ixP oint (right)


6.3     Computing sin in Fix-point Arithmetic
Like in the above subsection, the algorithm SinCodeInReals presented in the
Fig. 5 can be modified for argument values in the range [−1, 1] as presented in
the left part of the Fig. 8; the corresponding specification (12) should be modified
also:

      [(0 < ε < 1) & (−1 ≤ x ≤ 1)] SinCodeInZerOne [|sn − sin x| ≤ ε]             (17)

where cos x is defined by (10). Correctness of the above specification (17) can
be proved very similar to the proof of the specification (14).
   Again, similarly to the previous subsection, the above algorithm SinCodeIn-
ZerOne presented in the left part of the Fig. 5 can be converted into algorithm
SinCodeInF ixP oint (with fix-point arithmetic) presented in the right part of
the Fig. 8; the corresponding specification (12) should be modified as follows:
                                          
      δD < 1 &
     0 < ε < 1 & ε ∈ V alD &              
                                          
     ∃N ∈ IntD : ((2N + 1)! × ε ≥ 1) & 
      −1 ≤ x ≤ 1 & x ∈ V alD                                                 (18)
                            SinCodeInF
                                 "        ixP oint                   #
                                                             3nδD
                                     |snf p − sin x| ≤ ε + 2(1−δ D)
                                                                    &
                                     n = min {N : ((2N + 1)! × ε ≥ 1)}

where (as usual in this paper) sin x is defined by (10). A proof of this specification
should be similar to the proof of the specification (16).


7     Conclusion
In this paper we concentrate on design, specification and (a preliminary manual)
verification of two trigonometric functions cos and sin in platform-independent
fix-point arithmetic for small argument values in the range [−1, 1] and use Taylor
expansions as the definitions of the functions. Let us enumerate below some
problems that need further theoretical and experimental research.
(defun my-cos (x &optional (eps 1E-8))
  (let ((a 1) (s 1) (k 0))
    (loop
      (when (<= (abs a) eps) (return s))
      (setq a (- (/ (* a x x) (+ k 1) (+ k 2)))
                s (+ s a)
                k (+ k 2)))))


Fig. 9. Lisp-function to compute approximations for cos in unbounded rational arith-
metic with accuracy 10−8



   First, we should try to implement our verified algorithms on the virtual
computer (for our fix-point arithmetic) available at https://bitbucket.org/
ainoneko/lib_verify/src/ and then test these implementations against

 – selected algebraic values for these functions (for example, sin π6 = 21 , sin π4 =
             √             √
   cos π4 = 22 , cos π6 = 23 , etc.) in lines with test approach suggested and
   explained in [12,13];
 – automatically generated test data computed using Taylor expansions in any
   language that supports unbounded integer arithmetic; for example, a Lisp-
   function in Fig. 9 computes approximations for cos in unbounded rational
   arithmetics with accuracy 10−8 .

    Next we should complete the section 6 by a pen-and-paper proof of the
specification (16) (instead of the sketch presented in the appendix A) and by a
proof of the specification (18). Then we should validate/implement both proofs
using some proof-assistance since manual proofs accompanied by computer-aided
proofs is the core idea of the combined approach to verification. Currently in our
studies of the square-root function [19,20]) we are using proof-assistance ACL2
for proof-validation/implementation, but may change our choice later.
    Finally we should move from computation, specification and verification of
approximations of the trigonometric functions for small argument values in fix-
point arithmetic to relatively big argument values in floating-point arithmetics.
As we have mentioned in the section 5, computing of the values of the trigono-
metric functions for big argument values may be reduced to small argument
values either using periodicity (2), or (for example) Chebychev polynomials,
the trigonometric addition 3, the double-angle 4, and the half-angle 5 formulas.
(Remark that in the first case we need to compute approximate values of the
constant π with high precision.)
    We would like to finish the paper with a remark that the test-based approach
from [12,13] may be used for argument range larger than [−1, 1]; automated test-
ing against valid approximations computed using unbounded rational arithmetic
also may help; for example table 2 presents rational approximation of cos 50 com-
puted as (my-cos 50) using unbounded rational arithmetic (this rational value
is “equal” to a float-point value 0.9649660286).
  nominator                             denominator
  24370613165454113267560338608221954 25255410493873184332225648114958816
  98255428138520309455467035800407203 94660898821193613023561185556763590
  92481216493267961919792183534114282 78896631844387898015300688850221053
  43256901695353743984506265611950655 37104695728469968259460206109490815
  23779221083103374016633819981723287 73617550435820266050926650594970281
  8060581913569126766599                3572299506856327202849
                 Table 2. Result of evaluation of (my-cos 50)




References

1. Apt K.R., de Boer F.S., Olderog E.-R. Verification of Sequential and Concurrent
   Programs. Springer-Verlag, 2009.
2. C reference. https://en.cppreference.com/w/c. (Visited December 27, 2018.)
3. C reference: cos, cosf, cosl. https://en.cppreference.com/w/c/numeric/math/cos.
   (Visited December 27, 2018.)
4. C reference: Fundamental types. https://en.cppreference.com/w/cpp/language/
   types. (Visited December 27, 2018.)
5. C reference: sin, sinf, sinl. https://en.cppreference.com/w/c/numeric/math/sin.
   (Visited December 27, 2018.)
6. Dorn W.S., McCracken D.D. Numerical Methods with Fortran IV Case Studies.
   John Wiley & Sons, 1972.
7. Gries D. The Science of Programming. Springer-Verlag, 1981.
8. Grohoski G. Verifying Oracle’s SPARC Processors with ACL2. Slides of the In-
   vited talk for 14th International Workshop on the ACL2 Theorem Prover and
   Its Applications. http://www.cs.utexas.edu/users/moore/acl2/workshop-2017/
   slides-accepted/grohoski-ACL2_talk.pdf. (Visited December 27, 2018.)
9. Harrison J. Formal Verification of Floating Point Trigonometric Functions. Lecture
   Notes in Computer Science. 2000. Vol. 1954. P.217–233.
10. Hoare C.A.R. The Verifying Compiler: A Grand Challenge for Computing Re-
   search. Lecture Notes in Computer Science. 2003. Vol. 2890. P. 1–12.
11. Holzmann G.J. Mars Code. Commun. ACM, 2014, Vol. 57(2), p. 64–73.
12. Kuliamin V. Standardization and Testing of Mathematical Functions. Program-
   ming and Computer Software. 2007. Vol. 33(3). P. 154–173.
13. Kuliamin V.V. Standardization and Testing of Mathematical Functions in floating
   point numbers. Lecture Notes in Computer Science. 2010. Vol. 5947. P. 257–268.
14. Pi(number). Encyclopedia of Mathematics. http://www.encyclopediaofmath.
   org/index.php?title=Pi(number)&oldid=43586. (Visited December 27, 2018.)
15. Radian. Encyclopedia of Mathematics. http://www.encyclopediaofmath.org/
   index.php?title=Radian&oldid=31576. (Visited December 27, 2018.)
16. “Roskosmos” nazval prichinu neudachnogo zapuska s kosmodroma Vostochnyy
   (Roskosmos named the cause of the launch failure from launch-site “Vostochny”).
   https://www.rbc.ru/politics/12/12/2017/5a2ebcd59a79479d29667115.               (In
   Russian. Visited December 27, 2018.)
17. Shilov N.V. On the need to specify and verify standard functions. The Bulletin
   of the Novosibirsk Computing Center (Series: Computer Science), 2015, Vol. 38, p.
   105–119.
18. Shilov N.V., Promsky A.V. On specification andd verification of standard math-
   ematical functions. Humanities and Science University Journal, 2016, Vol. 19, p.
   57–68.
19. Shilov N.V. Anureev I.S. Berdyshev M., Kondratyev D., Promsky A.V. To-
   wards platform-independent verification of the standard mathematical functions: the
   square root function. https://arxiv.org/abs/1801.00969 [arXiv:abs/1801.00969].
   (Visited December 27, 2018.)
20. Shilov N. V., Kondratyev D. A., Anureev I. S., Bodin E. V, Promsky A. V.
   Platform-independent Specification and Verification of the Standard Mathemati-
   cal Square Root Function. Modeling and Analysis of Information Systems, 2018,
   Vol. 25(6), p. 637–666.
21. Trigonometric functions. V.I. Bityutskov (originator), Encyclopedia of Mathe-
   matics. http://www.encyclopediaofmath.org/index.php?title=Trigonometric_
   functions&oldid=14919. (Visited December 27, 2018.)
22. Trigonometric functions: Computation. From Wikipedia, the free encyclopedia.
   https://en.wikipedia.org/wiki/Trigonometric_functions#Computation. (Vis-
   ited December 27, 2018.)
23. Weisstein E. W. Trigonometric Addition Formulas. From MathWorld–A Wolfram
   Web Resource. http://mathworld.wolfram.com/Double-AngleFormulas.html.
24. Weisstein E. W. Double-Angle Formulas. From MathWorld–A Wolfram Web Re-
   source. http://mathworld.wolfram.com/TrigonometricAdditionFormulas.html.
25. Weisstein E. W. Half-Angle Formulas. From MathWorld–A Wolfram Web Re-
   source. http://mathworld.wolfram.com/Half-AngleFormulas.html.
26. Weisstein E. W. Leibniz Criterion. From MathWorld–A Wolfram Web Resource.
   http://mathworld.wolfram.com/LeibnizCriterion.html.


A    Proof Sketch for the Correctness Assertion 16
Let us remark that a conjunct

                           ∃N ∈ IntD : ((2N )! × ε ≥ 1)

in the precondition of (16) implies that
 – the algorithm CosCodeInF ixP oint terminates, the final value of the vari-
   able n is min {N : ((2N )! × ε ≥ 1)} indeed, it is equal to the number of
   iterations of the algorithm CosCodeInF ixP oint and to number of itera-
   tions of the algorithm CosCodeInZerOne;
 – in all assignments in CosCodeInF ixP oint but the following two

                                 tcf p := −(x ⊗ x) 2
                                                                                 (19)
                     tcf p := − (tcf p ⊗ (x (m 1))) ⊗ (x         m)

   all the floating-point operations are equal to the corresponding exact real
   arithmetic operations (e.g. epf p := m ⊗ ((m 1) ⊗ epf p) can be replaced
   by epf p := m × (m − 1) × epf p);
 – more over, in the second of these assignments (19) the floating-point sub-
   traction is equal to the exact real arithmetic subtraction, i.e. this assignment
   can be replaced by tcf p := − (tcf p ⊗ (x (m − 1))) ⊗ (x m).
    Due to the above observations (remarks) we can exercise both algorithms
CosCodeInZerOne and CosCodeInF ixP oint synchronously in iterations. For
all integer k ∈ [1.. min {N : ((2N )! × ε ≥ 1)}] let tcf pk and scf pk be instant
values of the corresponding variables before k-th check of the (equal) conditions
|ep| < 1 and |epf p| < 1 in the algorithms CosCodeInZerOne and CosCodeIn-
F ixP oint respectively; let also ∆k = tcf pk − tck . In particular,

                                                              x2
                      ∆1 = tcf p1 − tc1 = −(x ⊗ x)       2+      ;                 (20)
                                                              2
the absolute value of ∆1 may be evaluated a follows:
                                2
                                            0
                                                 2
  |∆1 | = −(x ⊗ x) 2 + x2 = − x⊗x     2  + δ2 + x2 =
                                                               (21)
                            00
                                    
                      x2 + δ      0    2       0 00  0 00
               = − 2 2 + δ2 + x2 = δ2 − δ4 ≤ δ2 + δ4 = 43 δD ,

where |δ 0 |, |δ 00 | ≤ δD .
   Let k be any integer in the range [1.. min {N : ((2N )! × ε ≥ 1)}). As we
                             x2k                           x2(k+1)
know (13), tck = (−1)k × (2k)!   and tck+1 = (−1)k+1 × (2(k+1))!   = −tck ×
     x2
(2k+1)(2k+2) . For technical convenience let us introduce auxiliary values

                                                 x
                                  tck+ = tck × 2k+1 ,
                          tcf pk+ = tcf pk ⊗ (x (2k + 1)) ,                        (22)
                                ∆k+ = tcf pk+ − tck+ ;

then
                                                  x
                                tck+1 = −tck+ × 2k+2 ,
                        tcf pk+1 = −tcf pk+1 ⊗ (x (2k + 2)) ,                      (23)
                               ∆k+1 = tcf pk+1 − tck+1 .
We have:
                                                                 0
                                                                    
                                                        x
tcf pk+ = tcf pk ⊗ (x     (2k + 1)) = (tck + ∆k ) ⊗ 2k+1      + δ2 =
                                                  0
                                                          00
                                            x
                         = (tck + ∆k ) × 2k+1 + δ2 + δ2 =
                                                         0
                                                                             0
                                                                                 00
                                               x2k
                                     = tck+ + (2k)!  × δ2 + ∆k × 2k+1   x
                                                                          + δ2 + δ2

where |δ 0 |, |δ 00 | ≤ δD ; since |x| ≤ 1 we can evaluate |∆k+ | in terms of |∆k | and
δD as follows:

                x2k       δ0                      δ0     δ 00
                                                    
                                           x                    1 + δD        3
  |∆k+ | =             × + ∆k ×                 +      +      ≤        |∆k | + δD . (24)
               (2k)!       2             2k + 1   2       2        2          4

Due to similarity between (22) and (23) we can evaluate |∆k+1 | in terms of |∆k+ |
and δD as follows:
                                   1 + δD         3
                         |∆k+1 | ≤        |∆k+ | + δD .                       (25)
                                      2           4
Combining (22) and (23) we get
                                      2                             
                              1 + δD                         1 + δD      3
              |∆k+1 | ≤                     × |∆k | +               + 1 × δD .                     (26)
                                 2                              2        4

Inequalities (21) and (26) together imply that
                       2k            P                
                                         i=2k−1 1+δD i
     |∆k+1 | ≤ 1+δ 2
                     D
                           × |∆1 | +     i=0      2        × 34 δD ≤
                                                      1+δD 2k+1
                                                          
                        P
                            i=2k 1+δD i
                                                                −1
                                             3
                                                                    × 34 δD =
                                                        2
                     ≤      i=0     2      ×   δ
                                             4 D =       1+δD                                      (27)
                                                                             −1
                                                                  2k+12
                                                            1+δD
                                                   1−
                                                                                          δD
                                                                            × 32 δD ≤ 23 1−δ
                                                              2
                                               =            1−δD                             D
                                                                                               .

    Using (21) and (27) we can prove the first property from the postcondition
of the specification (16):
                   Pk=n−1            P                         
                                       k=n−1       Pk=n−1
|csf p − cos x| =     k=1   tcf pk −   k=1   tck −    k=1   tck   − cos x ≤
               Pk=n−1             Pk=n−1        Pk=n−1
           ≤      k=1   tcf pk − k=1 tck +        k=1   tck − cos x ≤
                       Pk=n−1                           Pk=n−1
                    ≤ k=1 |tcf pk tck | + ε = |∆1 |+ ≤ k=2 |tcf pk tck | + ε ≤
                                            3                  3 δD        3nδD
                                            4 δD + (n − 2) × 2 1−δD ≤ 2(1−δD ) .
