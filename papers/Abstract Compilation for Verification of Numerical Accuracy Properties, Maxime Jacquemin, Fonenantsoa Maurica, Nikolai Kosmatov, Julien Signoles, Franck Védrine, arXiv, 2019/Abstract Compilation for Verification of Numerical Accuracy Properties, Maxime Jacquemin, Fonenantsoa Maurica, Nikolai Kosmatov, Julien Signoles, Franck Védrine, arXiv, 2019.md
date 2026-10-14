                                                   Abstract Compilation for Verification of
                                                      Numerical Accuracy Properties

                                                 Maxime Jacquemin1 , Fonenantsoa Maurica1,3 , Nikolai Kosmatov1,2 ,
                                                             Julien Signoles1 , and Franck Védrine1
                                             1
                                                 CEA, LIST, Software Security and Reliability Laboratory, Palaiseau, France
arXiv:1911.10930v1 [cs.SE] 25 Nov 2019




                                                                       firstname.lastname@cea.fr
                                                           2
                                                             Thales Research & Technology, Palaiseau, France
                                                                       nikolaikosmatov@gmail.com
                                                                    3
                                                                      Billee, Neuilly-sur-Seine, France
                                                                    firstname.lastname@billee.fr

                                                  Abstract. Verification of numerical accuracy properties in modern soft-
                                                  ware remains an important and challenging task. This paper describes an
                                                  original framework combining different solutions for numerical accuracy.
                                                  First, we extend an existing runtime assertion checker called E-ACSL with
                                                  rational numbers to monitor accuracy properties at runtime. Second, we
                                                  present an abstract compiler, FLDCompiler, that performs a source-to-
                                                  source transformation such that the execution of the resulting program,
                                                  called an abstract execution, is an abstract interpretation of the initial
                                                  program. Third, we propose an instrumentation library FLDLib that for-
                                                  mally propagates accuracy properties along an abstract execution. While
                                                  each of these solutions has its own interest, we emphasize the benefits
                                                  of their combination for an industrial setting. Initial experiments show
                                                  that the proposed technique can efficiently and soundly analyze numer-
                                                  ical accuracy for industrial programs on thin numerical scenarios.


                                         1   Introduction
                                         Floating-point numbers are widely used in many areas such as digital signal pro-
                                         cessing, localization applications, neural networks, and high performance com-
                                         puting. However, the results of floating-point operations are rounded, which
                                         approximates them w.r.t. ideal computations on real numbers. An accumulation
                                         of rounding errors may lead to inaccurate computations that are sometimes at
                                         the origin of disastrous bugs123 . Therefore, it is of the utmost importance to
                                         verify the accuracy of such numerical computations in critical systems.
                                             Verification of accuracy properties remains a challenging research topic since
                                         many years [1]. Testing-based techniques are too optimistic: they do not detect
                                         many numerical misbehaviors because they cannot represent real numbers pre-
                                         cisely. A contrario, static analysis techniques, for instance, based on abstract
                                         interpretation [2], are too pessimistic: they compute over-approximations of the
                                         1
                                           http://www-users.math.umn.edu/~arnold/disasters/patriot.html
                                         2
                                           https://en.wikipedia.org/wiki/Vancouver_Stock_Exchange
                                         3
                                           http://www-users.math.umn.edu/~arnold/disasters/sleipner.html
floating-point operations that lead to false alarms, signaling potential errors that
cannot happen on any concrete execution.
    In this paper, we propose the new concept of abstract compilation as an in-
termediate technique between testing and abstract interpretation. An abstract
compiler embeds an abstract interpretation engine for floating-point computa-
tions into the generated code in order to soundly verify the properties of interest
during its execution, called an abstract execution. To that end, the abstract com-
piler converts each floating-point value of the concrete execution to an abstract
value that is interpreted at runtime by a dedicated library.
    The main difficulty of this technique consists in handling unstable tests in a
sound way. Indeed, an unstable test happens when the guard of a conditional
depends on a floating-point expression e and can be evaluated to a boolean value
different from the one relying on real arithmetic. In such a case, the program’s
concrete execution flow differs from the theoretical one since the conditional
branch that is executed is not the same. To solve this issue, each unstable test is
enclosed in a loop in order to soundly iterate over all possible execution paths.
    Compared to abstract interpretation, abstract compilation remains precise
even if the execution context is not statically known (e.g. in presence of commu-
nication channels), since the generated code embedding the abstract engine is
executed on concrete inputs. Compared to testing techniques, it remains sound.
It is also possible to test programs while taking into account uncertainty of their
inputs (e.g. coming from sensors), providing better insights on its robustness.
    Last but not least, when the numerical accuracy properties of interest are
actually properties over rational numbers (in Q), the generated code evaluates
them in an exact manner, without relying on abstract values. Therefore, no
approximations are introduced in such cases.
    For evaluating this approach in practice, we have implemented a prototype
abstract compiler from C code annotated with formal numerical accuracy prop-
erties into C++ code. It relies on three main components: the runtime assertion
checker E-ACSL [3] to convert the formal properties into C code, FLDCompiler
that deals with instability and generates the resulting C++ code, and the C++
library FLDLib 4 that interprets abstract numerical values at runtime. This
toolchain has been evaluated on our own motivating examples, on small-size
examples coming from other sources, and on large-size industrial case studies
(mostly synchronous reactive systems of several dozens of thousands lines of
code). Each component of the toolchain has its own interest and has been de-
veloped independently from abstract compilation. Hence, it is possible to use
them separately, or to replace one of these components by a different one in a
particular setting. For instance, it is possible to replace FLDLib by Cadna [4] to
obtain an accuracy verification by stochastic propagation.
    To sum-up, the contributions of the paper include:
 – an extension of the runtime assertion checker E-ACSL that supports opera-
   tions over rational numbers in an exact manner. As far as we know, that is
   the first support of rational numbers in such a tool;
4
    https://github.com/fvedrine/fldlib
 – a description of the abstract compiler FLDCompiler that deals with unstable
   tests while generating code for the abstract interpretation engine;
 – an instrumentation library, FLDLib, that formally propagates accuracy prop-
   erties along the abstract execution of the test program;
 – a presentation of a new verification technique named abstract compilation
   that embeds an abstract interpretation engine at runtime, as well as a pro-
   totype toolchain that combines the three aforementioned components;
 – an evaluation of this toolchain over a set of representative programs.

Outline. The rest of the paper is organized as follows. Section 2 presents an
overview of abstract compilation through a motivating example. Section 3 pro-
vides the necessary background in order to understand the technical parts of the
paper. Section 4 details the three components of our abstract compiler toolchain.
Section 5 shows our experimental results. Section 6 introduces the related work
before concluding and introducing perspectives in Section 7.


2   Overview and Motivating Example
Abstract compilation is an intermediate verification technique for numerical ac-
curacy between testing and abstract interpretation [2]. Testing tools, e.g. FpDe-
bug [5], are likely to deliver too optimistic results since they have no confidence
interval, whereas abstract interpreters, e.g. Fluctuat [6], are likely to deliver too
pessimistic results (false alarms) that come from over-approximations.
    Consider for instance the C function of Fig. 1. It implements an interpola-
tion table y composed of n measures to compute a linear approximation of a
continuous function on a point in ∈ [0, n − 1]. We would like to verify that, at
every call site, the round-off error of the result can increase the imprecision of
the input by at most twice the biggest measure of the table. We would also like
to check that the function is robust enough: not only this property is satisfied
for all concrete input values, but also for any value near them [7].
    For instance, in the ACSL specification language [8], the desired accuracy and
robustness properties can be expressed by the following assertion:
/* @ assert
       \ let ( err_min , err_max ) = accuracy_get_ferr ( in );
       \ let cst = max_distance (& y [0] , n );
       accuracy_assert_ferr ( out ,
          -2.0 * cst * min ( err_min , - err_max ) ,
          +2.0 * cst * max ( - err_min , err_max )); */
Function max distance (omitted here) computes the maximal distance between
two successive elements of y, that is, maxi=0,...,n−2 |y[i + 1] − y[i]|. Functions
accuracy get ferr and accuracy assert ferr are built-ins that extend the
original ACSL language. The first one gives access to the error bounds of its pa-
rameter while the second one asserts an accuracy property, here that the resulting
round-off error for out is bounded by −2.0 × cst × min(err min, −err max)
and 2.0 × cst × max(−err min, err max).
1   double interpolate ( double in , double *y , i n t n ) {
2     double out ;
3     i n t index = ( i n t ) in ;
4     i f ( index < 0 || index >= n -1)
5         out = ( index < 0) ? y [0] : y [n -1];
6     else
7         out = y [ index ] + ( in - index ) * ( y [ index +1] - y [ index ]);
8     return out ;
9   }
                   Fig. 1: Motivating example: an interpolation table.


        It is worth noting that the robustness property is actually broken for this
    example since for two close values −1 and −1 + ε of in (with a small ε > 0),
    we have index equal, resp., to -1 and 0, and out equal, resp., to y[0] and
    2y[0] − y[1], with an obvious discontinuity. Therefore, an alarm shall be raised
    if (and, optimally, only if) such a context is encountered.
        Testing-based techniques cannot check the desired properties for all values,
    while abstract interpreters have a hard time to verify them in a precise manner
    because they include three verification challenges:
     1. keeping precise relationships between variables index and in after the ini-
        tialization of the former through the latter at line 3;
     2. analyzing the unstable test issued from line 3 that may lead to execute one
        branch of the conditional or another depending on the guard is computed
        over floating-point or real numbers;
     3. expressing the desired accuracy and robustness properties in a formal way.
    In addition to these technical challenges, a practical abstract interpreter usually
    requires to stub input-output (I/O) functions such as communications with the
    environment and the initialization machinery. To circumvent these issues, our
    approach embeds into the code an abstract interpretation engine that only man-
    ages floating-point computations. Concrete code execution solves the practical
    issues of a static abstract interpreter. It also solves point (1) since the relations
    are implicitly kept by the execution flow, while the abstract compiler automati-
    cally replaces the concrete floating-point values and operators by their abstract
    counterparts that soundly take into account round-off errors. The abstract com-
    piler also takes care of point (2) by enclosing each potential unstable test in a
    loop, so ensuring a complete coverage of all possible executions as explained in
    Section 4.2. Finally, point (3) is addressed by relying on a formal specification
    language, e.g. ACSL [8], that can express powerful numerical properties.

    3   Background
    This section introduces the necessary background for understanding the technical
    parts of the paper: Ieee-754 floating-point numbers in Section 3.1, and the
    minimal required specification language based on ACSL in Section 3.2.
             0 0.1    ...      10 11    ...      100 110    ...    990

                     δ = 0.1           δ=1               δ = 10

Fig. 2: Schematic representation of positive values of a floating-point type with
β = 10, p = 2, emin = 0 and emax = 2. The difference between two consecutive
floats, denoted by δ, is different for different intervals of values.


3.1   IEEE-754 Floating-Point Numbers

A floating-point number is a rounded representation of a real number. Simply
                                                s
put, a real number x, denoted as x = (−1) mβ e in scientific notation, is approx-
                                                              s
imated by the floating-point number f = ◦(x) = (−1) m̂β e where s ∈ {0, 1},
                                                    +
β ∈ N, β ≥ 2, e ∈ {emin , . . . , emax } ⊂ Z, m ∈ R , and m̂ is an approximation of
m on p ≥ 2 digits. The quantities β, p, emin and emax parameterize the considered
floating-point type. The function ◦ is called the rounding function.
    Floating-point numbers are standardized by the Ieee-754 norm. Among oth-
ers, it defines several standard types — several assignments for β, p, emin and
emax — such as the float and double types of the C programming language.
Ieee-754 defines several rounding functions, but the rest of the paper assumes
that ◦ rounds x to the nearest floating-point number. A Ieee-754 compliant
implementation also requires floating-point arithmetic operations to be correctly
rounded : given a real arithmetic operation ?, its floating-point equivalent ?
must satisfy f1 ? f2 = ◦(f1 ? f2 ) where f1 , f2 are floating-point numbers.
    To illustrate all this, consider the floating-point type represented in Fig. 2 and
parameterized by β = 10, p = 2, emin = 0 and emax = 2. In this type, the real x =
             0                                                    0
10π = (−1) 3.14 · · · 101 is approximated by f = o(x) = (−1) 3.1 · 101 = 31 while
computing 1/3 gives us 1 / 3 = ◦(1/3) = ◦(0.3 · · · ) = 0.3. In both examples, the
rounding introduces a difference between the behavior of the real numbers and
the floating-point numbers. This difference, called the absolute error, is normally
quite small with standard floating-point type. Its counterpart, the relative error,
is defined as the absolute error divided by the expected result in real numbers.
Since these errors are accumulated at each floating-point operation of a program,
they may lead to huge differences between the observed and expected behaviors.
    The interested reader may refer to [9] or [10] for additional details.


3.2   Specification Language

The purpose of this work is to target accuracy properties of C programs. For
expressing them, we rely on the E-ACSL specification language [11], derived from
the ACSL specification language [8]. The differences between both languages [12]
are of no importance for our work, so we only present here an overview of a
small common fragment. Its formal syntax is shown in Fig. 3. Most constructs
have already been illustrated in Section 2.
          assert ::= /*@ assert pred; */                             assertion
            pred ::= pred rel pred                       rel ∈ {∧, ∨, =⇒ }
                 |   ¬pred                                           negation
                 |   term cmp term                   cmp ∈ {<, ≤, ≡, >, ≥}
                 |   let x = term; pred                       local binding
                 |   p(term, . . . , term)                   p ∈ P builtins
            term ::= x                                         logic binder
                 |   lv                                          left-values
                 |   zcst                                            zcst ∈ Z
                 |   qcst                                      qcst ∈ Q \ Z
                 |   term op term                         op ∈ {+, −, ×, /}

                     Fig. 3: Syntax of the specification language.

                     Built-in name                 : type
                     accuracy enlarge [f,d]val err: F × Q4 → bool
                     accuracy assert [f,d][rel]err : F × Q2 → bool
                     accuracy get [f,d][rel]err    : F → Q2
                     accuracy get [f,d]real        : F → Q2
                     [f,d]print                    : F → bool

Fig. 4: Built-in predicates extending ACSL. Their counterparts exist in FLDLib.


    Logic statements are assertions enclosed in special comments /*@ ...*/ that
may be written before any C instruction. Assertions are typed predicates which
include logical relations and comparison operators over terms, local bindings à
la ML, as well as applications of built-in predicates shown in Fig. 4, in which F
denotes either type float (if f) or double (if d). These predicates have their
counterparts supported by the FLDLib library (cf. Section 4.3). The pair of built-
ins starting with accuracy enlarge enlarge the values and the absolute errors
to the two pairs of bounds provided as arguments. accuracy assert built-ins
check whether the absolute or (if rel is indicated) the relative error is included
within the given bounds. accuracy get built-ins return the lower and upper
bounds of the absolute or relative error, or those of the real-number domain.
The last built-ins print information about the internal FLDLib representation.
    Terms are logic binders x, C left-values lv (variables, pointer derefences, array
and struct accesses, etc), mathematical constants (either integers or rationals),
or numerical operators. Terms are typed. The typing rules are left implicit here,
but are straightforward. A numerical operation is an integer one if both argu-
ments are integers; otherwise it is an operation over rational numbers (and the
integer argument, if any, is automatically promoted to the corresponding ratio-
nal number). It is worth noting that all constants and numerical operators are
over mathematical numbers (either integers in Z, or rationals in Q depending on
 annotated C code                     C++ code with unstable tests
                                               r
                   E-A
                      CS                  pile                FLD
                                                                  Lib
                        L             C om                 or
                                  FLD                         Cad
                                                                  na
                    instrumented C code                            instrumented binary
                     Fig. 5: The abstract compilation toolchain.


the context). C integers and floating-point values are implicitely coerced to their
mathematical counterparts. For the sake of simplicity, we assume no NaN nor
±∞ values, as well as no runtime errors when evaluating C left-values (see [12]
for a discussion about them).


4     Abstract Compilation Toolchain
Our toolchain, shown in Fig. 5, consists of three components, respectively intro-
duced in Sections 4.1, 4.2, and 4.3. The first two steps, E-ACSL and FLDCompiler,
perform code generation, while the last step is linking with FLDLib library (that
can be replaced at no cost by Cadna [4]). Steps 2, 3 are further detailed in Fig. 10.



4.1    E-ACSL Runtime Assertion Checker
E-ACSL [3] is the runtime assertion checker of Frama-C [13], an analysis frame-
work for C code. It converts a C program annotated with ACSL formal speci-
fications to another C program that behaves at runtime as the original one if
every annotation is satisfied, otherwise it fails on the first invalid annotation.
Therefore, it may be seen as a compiler from ACSL+C code to C code. While
this tool has been being developed since a few years, it has been extended here
to support numerical properties over rational numbers5 . In addition, a special
extension to support the numerical built-ins presented in Fig. 4 has also been
designed for our abstract compiler. It generates FLDLib-compatible code.
    As explained in Section 3.2, the specification language relies on mathemati-
cal integers and rational numbers. Therefore, the generated code cannot soundly
use standard C operators over integral or floating-point types. Instead, E-ACSL
generates special code relying on GMP library6 to soundly represent mathemati-
cal integers and rationals. Built-in predicates of Fig. 4 are directly compiled into
their FLDLib counterparts.
    However, the generated GMP code is inefficient compared to machine in-
structions. To reduce the need for GMP code without loss of soundness, we have
designed a dedicated type system in order to rely on machine representations as
much as possible, and generate GMP code only when necessary. The type sys-
tem relies on integer intervals and a custom notion of kind. E-ACSL infers such
5
    This part of the work will be included in the next open source version of Frama-C.
6
    https://gmplib.org/
a kind for each term, and uses it to decide whether the machine types and oper-
ations can be sufficient to perform the required operations or not. Our technical
presentation of E-ACSL focuses on this type system. In practice, thanks to this
solution, very few pieces of GMP code are generated for integers. Some compar-
isons of floating-point values without operators (e.g. f == 0.) do not require
GMP’s rational operations either (as in the example in the end of the section).
    We assume the existence of a type system, where Σ(t) denotes the type of
a term t and the primitive isinteger(t) (resp. isfloat(t)) is true if and only if
Σ(t) is a subtype of Z (resp. a floating-point type). 4τ is the subtyping relation
(expressing that all values of one type are also values of the other).

Integer intervals. We consider integer intervals with partial order 4I . Let T(I)
be the smallest C integral type containing interval I, or Z otherwise, and I(t) be
an interval that contains all the possible values of the term t. In practice, E-ACSL
relies on a simple syntactic type-based inference system to compute I(t)7 .

Kinds. A kind is either an integer interval, or a floating-point type, or a rational.
More formally, let (K, 4) be the (sup-)semi-lattice of kinds defined as follows:
                                                       Z I1 4 Z I2 ⇐⇒ I1 4I I2
     K ::= Z I        integer interval I
                                                      F τ1 4 F τ2 ⇐⇒ τ1 4τ τ2
       |   F τ    floating-point type τ
                                                        Z I 4 F τ ⇐⇒ T(I) 4τ τ
       |   Q                     rational
                                                        K 4 Q (for all K ∈ K)
    Let ∪ denote the union over kinds induced by their lattice structure. The kind
of a term t, denoted κ(t), and the type of a kind k, denoted θ(k), are defined as
follows:
     κ(t) = Z I(t) if isinteger(t)                       θ(Z I) = T(I)
      κ(t) = F Σ(t)        if isfloat(t)                      θ(F τ ) = τ
      κ(t) = Q           if ¬ isfloat(t)                        θ(Q) = Q

Type system. Fig. 6 presents the type system. A type judgement, written Γ `
t : τ1    τ2 for terms (resp. Γ `p p : τ1       τ2 for predicates), means “in the
typing environment Γ , the C expression generated for t (resp. p) may soundly
have type τ1 , but, in the case of an operator (resp. a comparison), it must be
computed over type τ2 .”. τ2 is omitted when irrelevant. Predicates return an
int. For instance, assuming a large integer constant c and variables x and y
of type int, the term x/(y + c) requires GMP code because y + c does not fit
into any C type. However, its result fits into a int, so it may safely be compared
to 0 with the usual C equality. Therefore, its type is int         Z. Fig 7 details
the derivation tree of x/(y + c) ≡ 0. To improve precision, typing of operators
computes the kind of its operands and its result, merges them (to get the most
precise interval containing all of their possible values) and converts the result
into the corresponding C type. The last two rules for terms are coercion rules.
7
    This inference system is omitted here, but has already been presented in French [14].
                        Γ ` cst : Σ(cst)               Γ ` lv : Σ(lv)              Γ ` x : Γ (x)
                     τ = θ(κ(t1 ) ∪ κ(t2 ) ∪ κ(t1 op t2 )) Γ ` t1 : τ                      Γ ` t2 : τ
                                         Γ ` t1 op t2 : τ   τ
                 Γ ` t : τ 0 τ 0 4τ τ                Γ ` t : τ0       τ 0 τ ≺ τ 0 θ(κ(t)) 4τ τ
                      Γ `t:τ                                          Γ `t:τ     τ0


      Γ `p p1 : int `p p2 : int                     Γ `p p : int             Γ ` t1 : τ1 · · · Γ ` tn : τn
        Γ `p p1 rel p2 : int                       Γ `p ¬p : int                Γ `p p(t1 , . . . , tn ) : int
       τ = θ(κ(t1 ) ∪ κ(t2 )) Γ ` t1 : τ Γ ` t2 : τ                            Γ ` t : τ Γ, x : τ `p p : int
                Γ `p t1 cmp t2 : int    τ                                        Γ `p let x = t; p : int

                                         Fig. 6: E-ACSL type system.

                    ` y : int         `c:Z
 ` x : int                `y+c:Z
            ` x/y + c : Z           Z                    int ≺ Z           θ(κ(x/(y + c))) 4 int
                                        ` x/y + c : int          Z                                                ` 0 : int
                                               `p x/(y + c) ≡ 0 : int

                               Fig. 7: Derivation tree for x/(y + c) ≡ 0.


The first one is a standard subsumption rule [15], while the second one soundly
downcasts a term to a smaller type than its own type if its infered kind fits in.

Code generation. Generating code from the information computed by the type
system is quite straightforward. For instance, the code generated for the assertion
/*@ assert x/(y + c) ≡ 0 ∧ f − 0.1 ≤ g; */ with the first operand of ≡ of type
int    Z, and f and g of type double would be as follows.
/* compute x /( y + c ) with GMP i n t e g e r s */
mpz_t _x , _y , _c , _add , _div ; int _div2 , _and ;
m pz _i n it _s et _ si ( _x , x ); mp z _i ni t _s et _s i ( _y , y );
m p z _ i n i t _ s e t _ s t r ( _c , " 7 9 2 2 8 1 6 2 5 1 4 2 6 4 3 3 7 5 9 3 5 4 3 9 5 0 3 3 5 " ,10); /* some large value */
mpz_init ( _add ); mpz_add ( _add , _y , _c );
mpz_init ( _div ); mpz_tdiv_q ( _div , _x , _add );
/* safely d o w n c a s t the result of the d i v i s i o n from GMP to int for testing it */
_div2 = mpz_get_si ( _div );
i f ( _div2 == 0) {
    /* compute f -0.1 <= g with GMP r a t i o n a l s */
    mpq_t _f , _cst , _g , _sub ; int _le ;
    mpq_init ( _cst ); mpq_set_str ( _cst , " 01/10 " ,10);
    mpq_init ( _f ); mpq_set_d ( _f , f );
    mpq_init ( _sub ); mpq_sub ( _sub , _f , _cst );
    mpq_init ( _g ); mpq_set_d ( _g , g );
    /* getting the result of the p r e d i c a t e as an int */
    _le = mpq_cmp ( _sub , _g );
    _and = _le <= 0;
    /* de - a l l o c a t e the a l l o c a t e d GMP v a r i a b l e s for r a t i o n a l s */
    mpq_clear ( _cst ); mpq_clear ( _f ); mpq_clear ( _sub ); mpq_clear ( _g );
} else
_and = 0;
/* runtime check the c o n j u n c t i o n */
assert ( _and );
/* de - a l l o c a t e the a l l o c a t e d GMP v a r i a b l e s for i n t e g e r s */
mpz_clear ( _x ); mpz_clear ( _y ); mpz_clear ( _c ); mpz_clear ( _add );
mpz_clear ( _div );




4.2     FLDCompiler Abstract Compiler
As said previously, in order to be sound, the embedding of an abstract interpre-
tation engine inside the program encloses each unstable test t within a loop that
must consider all possible evaluations of t. The toolchain provides two directives
to delimit those loops: split marks the start of a block of code B that must
be run multiple times to analyze all possible executions, while merge marks the
point of convergence where all memory states after the executions of B must
be joined into a unique state. Such a block B enclosed between these directives
is called a split-merge section. They are inserted into the code by FLDCompiler
while their instrumentation is provided by FLDLib. In the general case, split is
parameterized by the variables that must be reset before a new execution in or-
der to ensure that the memory state is the same at each loop iteration (i.e. each
execution of the section runs from the same state), while merge is parameterized
by the variables to be joined after different executions.
    Consider again the example of Fig 1. FLDCompiler inserts a split directive
with no argument before the cast at line 3, while a merge directive parameterized
by out is inserted before line 8. Indeed, a cast from a floating-point value to an
integer is actually a form of an unstable test since the real value can be cast to
a different integer than the floating-point one. The merge directive cannot be
placed earlier in the function because out would not be computed yet.
    FLDCompiler is a source-to-source program transformation that automati-
cally annotates a program with the needed split and merge directives together
with their parameters. For the sake of performance and precision, a generated
split-merge section should be minimal, i.e. its block of code is as small as pos-
sible, split only resets what is needed, and merge only joins variables that are
modified by the block of code and used afterward. It is worth noting that com-
puting these parameters statically is undecidable, so over-approximations may
actually be performed. Positioning the split-merge sections is done by a greedy
algorithm that expands them through the code until three criteria, presented
below, are satisfied. These criteria are illustrated on the example of Fig. 8 that
contains the unstable test if (2 * x + 3 < 0).

Criterion 1 A split must strictly dominate its associated merge. Conversely,
a merge must strictly post-dominate its associated split.

   Dominance and post-dominance relations [16] used in this criterion state
that all paths that go through split must go through its associated merge
and, conversely, all paths that go through merge must have gone through its
associated split. This criterion ensures that the memory allocations performed
by split are eventually freed by merge. The other way round, the memory
    Fig. 8: Example of the transformation steps performed by FLDCompiler.

      int f ( f l o a t x ) {   int f ( f l o a t x ) {   int f ( f l o a t x ) {
        { code1 ;                 { code1 ;                 ... do ...
          i f ( x < 0)              ... do ...              { code1 ;
              { code2 ; }           i f ( x < 0)              i f ( x < 0)
        }                               { code2 ; }               { code2 ; }
        return 0 ;                }                         }
      }                           ... while ...             ... while ...
                                  return 0 ;                return 0 ;
                                }                         }
Fig. 9: (a) Original code, (b) invalid and (c) valid examples of instrumentation.


freed by merge must have been initially allocated by split. In our example, the
if statement is post-dominated by the while, which is dominated by the if.
Therefore, a split (resp. merge) directive is added before the if (resp. while).

Criterion 2 A split-merge section must start and end in the same block.

    A split-merge section is enclosed in a do ... while loop. Its do part is
generated by split, whereas the while part is generated by merge. Generating
them in distinct blocks would lead to syntactically invalid C code. In our example
and most of the time, that is not an issue, but enforcing it on nested blocks as
in Fig. 9a is trickier. Here, Criterion 1 states that split must be inserted before
if, while merge must be inserted before return. Inserting them naively as in
Fig. 9b leads to an invalid code. FLDCompiler inserts them as in Fig. 9c.

Criterion 3 Non floating-point variables must be kept unchanged in every mem-
ory state generated by a split and joined by its associated merge.

    This criterion is mandatory because the libraries linked to the generated
code, e.g. FLDLib, have no abstraction for non floating-point variables: merging
them would result in a runtime crash. For example, the middle part of Fig. 8
presents a first positioning attempt for the split-merge section that actually vio-
lates Criterion 3. Indeed, because the value of the integer variable n is modified
in the if and is needed after the merge, its values must be joined. To fix this,
merge is delayed as shown on the right side of Fig. 8.
Arguments of split and merge. As said previously, split and merge take pa-
rameters that specify, resp., the variables to reset before a new execution of
the section, and the ones to be eventually merged after them. To minimize the
analysis cost, only necessary parameters should be generated. For example, if
a variable is never modified, resetting its value is useless. These parameters for
split and merge are respectively computed by a save-list and a merge-list whose
computation is explained below. They are based on a dedicated data dependency
analysis inspired from [17]. More precisely, for each statement p, this analysis
gathers four sets, informally defined as follows:
mustdef(p) : a set of variables necessarily modified in p (that is, all executions
   modify them). For instance, variable n of Fig. 8 is in the mustdef set of if.
maydef(p) : a set of pairs (x, s) where s is a sub-statement of p that may
   modify the variable x. In Fig. 8, the maydef set of while contains x and the
   loop body b since executing b modifies x. However, x does not belong to the
   mustdef set of while because, if n = 0, then x is left unchanged.
mayref(p) : a set of pairs (x, s) where s is a statement of p that may read the
   variable x. In Fig. 8, x belongs to the mayref set of if because it is read by
   its condition. For sequence of statements S, this set does not contain vari-
   ables that are read after being assigned in S. For instance, x (paired to any
   statement) does not belong to mayref of sequence S = x = 2; y = x + 3;.
data(p) : a set of tuples (s1 , s2 , x) in which s1 writes a variable x that is later
   read by s2 (without intermediate writings). Its computations uses the three
   previous sets. For the example of sequence S above, variable x is modified by
   x = 2; and then read by y = x + 3, so (x = 2, y = x + 3, x) ∈ data(S).
The save-list and merge-list of a split-merge section are computed as follows:
   save-list(p) = {x | ∃(s1 , s2 ), (x, s1 ) ∈ maydef(p) ∧ (x, s2 ) ∈ mayref(p)},
  merge-list(p) = {x | ∃(s1 , s2 ), (x, s1 ) ∈ maydef(p) ∧ (s1 , s2 ) ∈ data(F(p)) ∧ s2 6∈ p},
                  where F(p) is the body of the function containing p.

It means that a variable x is added to the save-list of a section p if there is
a statement inside p that may modify x and another statement that may read
x. Said another way, if a new execution may depend on the value of a variable
that could have been modified in another execution, then we need to reset it
before each execution. Dualy, a variable x is added to the merge-list of a section
p if there is a statement in p that may modify x and there is another statement
outside the section that may read x.
    FLDCompiler is implemented as a Frama-C plugin and relies on its kernel to
pretty-print the generated code. It visits the whole source code and generates the
split-merge sections based on the declared type of variables. The basic version has
no notion of alias, so if a pointer iterates on the cells of a floating-point array,
it does not add them to the save-list and the merge-list, which may produce
unsound results. To get around this problem, FLDCompiler relies on Eva [18],
the value analysis of Frama-C (as shown below in Fig. 10), in order to know all
possible targets of pointers to be added to the save-list and the merge-list. It is
                     Source code

                                                           split          path selection
       Frama-C/Eva

                     FLDCompiler
                                                                            constraint
                                     Fluctuat          index=(int)in;
         FLDLib                                                            propagation

                    Compiler:
                  g++, clang++
                                                          out=...         domain computation

                  Executable code
                   with analysis

                                                           merge              union
                   Robustness &
                  accuracy verdict



       Fig. 10: Tool architecture.              Fig. 11: Handling a split-merge section.


worth noting that it may add unnecessary variables to the lists since the analysis
by abstract interpretation is conservative. Finally, FLDCompiler issues a warning
if it tries to add to the lists something that is dynamically allocated and thus
that does not exist at compile-time.

4.3   FLDLib Numercical Analysis Library
FLDLib is an open-source instrumentation library that infers accuracy proper-
ties based on zonotopes [19] over a C or C++ code. It relies on a static analysis
dedicated to verification of numerical scenarios [6] that is originally implemented
in the close-source tool Fluctuat. FLDLib only deals with detecting numerical er-
rors and computing domains of numerical variables. Discrete values (pointers in-
cluded) are only enumerated. In particular, it has no pointer analysis. Therefore,
it is better used on thin scenarios that encompass concrete test cases in small
intervals. In such scenarios, pointers have only one or two possible value(s). This
way, it is possible to get exploitable results for accuracy and robustness proper-
ties of numerical pieces of code, even if integrated in a larger development.
    Starting from a source code instrumented by E-ACSL, Fig. 10 shows how
FLDLib is integrated within a verification workflow together with FLDCompiler,
and compared to Fluctuat. Figure 11 shows how FLDLib handles a split-merge
section generated by FLDCompiler: this section now focuses on explaining its
main parts, that are path exploration, constraint propagation and domain com-
putation. Even if not detailed here, FLDLib also supports the built-ins of Fig. 4
(after their translation by E-ACSL into their FLDLib counterparts).

Domain computation. FLDLib domains combine intervals and zonotopes [19].
Zonotopes allow to maintain linear relationships between program variables V
that share the same perturbations (noise symbols) by mapping V to affine forms.
Sharing noise symbols between variables helps at keeping precise information
since it means that the source of uncertainty is the same. We do not detail the
Fig. 12: Function x2 abstracted (a) with intervals (yellow) and affine forms (or-
ange) shown separately, and (b) the resulting intersection. The same abstractions
with a subdivision, (c) shown separately, and (d) the resulting intersection.


zonotope domain here for lack of space, but only illustrate by examples (see
Fig. 12) the benefits of combining zonotopes and intervals, in particular, with
a domain subdivision. For instance, if x ∈ [0, 1], an interval is more precise
than a zonotope for representing x2 (providing an interval x2 ∈ [0, 1] instead of
[−0.25, 1], cf. the projection of abstractions onto the x × x axis in Fig. 12a), but
less precise for representing x−x2 ([−1, 1] instead of [0, 0.25], cf. the distance from
the diagonal in Fig. 12a). The intersection of both abstractions provides more
precise results (Fig. 12b). A subdivision of the input interval into two intervals
significantly improves the results (Fig. 12c,d). The union operation mentioned
in Fig. 11 does not try to keep linear relationships coming from zonotopes but
ensures the preservation of intervals.
    The main principle of FLDLib consists in redefining double and float types
by a structure containing four fields representing the abstraction: (1) the floating
point domain float as an interval, (2) the real-number domain real as a zonotope,
(3) the error domain err as a zonotope, and (4) the relative error defined by an
interval. Like Cadna [4], FLDLib uses C++ operator overloading to propagate
these four domains over the program execution by redefining comparisons and
casts from floating-point types to integral types. Operator overloading is partic-
ularly interesting here since it limits necessary source-to-source transformation.
A similar approach could be applied to C programs with no operator overload-
ing capabilities, where such a transformation can be automatically done by the
Clang compiler. We have done promising initial experiments on Ada programs
that also support operator overloading through the libadalang library.

Constraint propagation. Comparison operators and casts from floating-point val-
ues to integer values are likely to introduce constraints on noise symbols i . Con-
sider for instance a conditional whose guard is x ≥ 0 for some variable x whose
abstraction is real = 0 , err = 10−7 1 , and float = [−1, 1]. It may lead to six
execution flows depending on the evaluation of the guard as a float (denoted
cf ) or as a real (denoted cr ): two if cf and cr are evaluated to the same truth
value, and four if these values diverge and the execution after the conditional is
interpreted either as a floating-point or a real number (2 + 2 × 2 = 6). Choosing
an execution flow among these six ones is called a local decision.
 1:                                                                       . Start of Split
 2: stack ← push(stack, current-path-explorer, end-explore) . save outer section context
 3: current-path-explorer ←
         new path explorer from mode(current-path-explorer, id) . create a new one
 4: end-explore ← end-explore id       . define label to explore next path of section id
 5: MΣ ← ∅                                     . merged memory MΣ is initially empty
 6: Msaved ← create local memory for(M, save-list) . save cur. memory for save-list
 7: do                                                    . iterate over execution paths
 8:     M ← restore memory(Msaved , save-list, M) . restore Msaved to M for save-list
 9:                                                                        . End of Split
10:      instructions of the section      . intrumented to ensure exploration of paths
11:                                                                     . Start of Merge
12:     M ← merge unstable(current-path-explorer, merge-list, M) . merge path data
13: end-explore id :                              . jump here to explore the next path
14:     MΣ ← merge(MΣ , merge-list, M)         . merge domains for merge-list into MΣ
15: while next path(current-path-explorer)       . choose next path if any, or exit loop
16: M ← MΣ                            . set current memory M to merged memory MΣ
17: current-path-explorer, end-explore ← pop(stack) . get the outer section’s context
18: if MΣ = ∅ then                                   . if no feasible path in the section
19:     goto end-explore                  . then explore next path in the outer section
20:                                                                      . End of Merge
                 Fig. 13: Instrumentation of a split-merge section.


   On our example, if xfloat and xreal are both positive, then 0 ∈ [0, 1]. There-
                                         def
fore, it defines a new noise symbol d = 20 −1 (so 0 = 0.5d +0.5) , constrained
to be in the interval [−1, 1]. Every affine form containing the shared symbol 0 is
then notified. If the replacement of 0 by 0.5+0.5d would improve the amplitude
of the affine form by 5%, this replacement becomes effective even if it may lose
some relationships with other variables. This rate of 5% is proved to be good in
practice. In this particular example, x becomes real = 0.5 + 0.5d , err = 10−7 1 ,
float = [0, 1]. Similarly, the unstable flow xfloat ≥ 0, xreal < 0, 0 < xerr requires
1 ∈ [0, 10−7 ], 0 ∈ [−10−7 , 0], since float = real + 10−7 1 ≥ 0. After replace-
ment, x becomes real = −5 × 10−8 + 5 × 10−8 d0 , err = 5 × 10−8 + 5 × 10−8 d1 ,
float = [0, 10−7 ].

Path exploration within split-merge sections. FLDLib instruments the constructs
split(id, save-list) and merge(id, merge-list) generated by FLDCompiler, where
id is a unique identifier for each section. As we outlined by Fig. 11, they en-
compass the instructions of the section. We detail this in Fig. 13. Split-merge
sections can be nested. As explained in Section 4.2, the current memory state
M is saved (for the variables of save-list) in Msaved and restored back into M
to start every new execution of the section from the same state (cf. lines 6, 8 in
Fig. 13).
    The outer section context is saved in a stack at line 2 and retrieved at line
17. The label end-explore defines a label where the execution jumps to explore a
next path if an inner split-merge section found no feasible path, or if an infeasible
path is encountered in the current section while exploring the instructions at line
10. The jump at line 19 shows the first usage. If feasible paths are found, the
execution continues with a merged state (line 16) after retrieving the context
(line 17).
    Another stack, current-path-explorer, ensures the storage and exploration of
paths. The call to next path at line 15 chooses the next path to be executed,
if any, and stores it in current-path-explorer, or exits the loop otherwise. The
exploration is performed in a depth-first search and relies on an instrumentation
of comparison operations and float-to-interger casts encountered in the section.
The instrumentation is realized by overloading comparison and cast operations
in C++.
    In practice, in addition to the split/merge directives, FLDLib adds at the
beginning of each source file a new header float_diagnosis.h. This header
replaces the definition of double and float types by the representation of their
abstract domains (as explained earlier in this section). The implementation of
goto end-explore benefits from the C++ exception mechanism. The main func-
tion is augmented with a header and a footer in order to initialize and clean up
the analysis state.
    Last but not least, FLDLib prevents merge-list from containing int variables
in order to keep precise relationships between discrete and continuous variables.
These constraints may move forward some merge constructions until the int
variables become useless.


5   Experimental Results
The toolchain presented in this paper has been evaluated on a benchmark of
small-size C examples and experimented on two industrial case studies.

Benchmarks. We use the benchmarks from [7]. It contains several small-size C
examples that may be categorized as follows.
 Simple examples show basic computations that focus on accuracy properties.
 Unstable branches are robustness tests for unstable branch handling.
 Interpolation tables contain various ways to compute an interpolation table.
   They also focus on testing robustness of unstable branches.
 Maths models functions of math.h for error estimation.
 Miscellaneous contain various other examples. File filter.c is a second or-
   der linear filter that focuses accuracy File patriot.c is an historical example
   that contains a sum of 0.1 whose error shifts over time. File complex LU.c
   finds a vector X such that M (X) = (Y ) for a square matrix M with a Low-
   er/Upper decomposition. File complex intersect.c shows iterative com-
   putations. File scanf.c show how to manage external library functions not
   related to floating-point operations.
   Each example have been annotated with ACSL assertions modeling the ex-
pected properties in order to use our toolchain. All of them have also been run
file/variable           Our toolchain        Fluctuat             Precisa           FpDebug
Simple examples:
absorption.c/z          1e-8                 1e-8                 5.96e-8           1e-8
associativity.c/u       6.67e-16             1.55e-15             4.21e-15          -2.22e-16
division.c/z2           1.805e-16            5.55e-16             5.55e-16          -1.57e-17
exp.c/y                 4.47e-13             5.61e-13             4.45e-12          ko
polynome.c/t            3.576e-06            2.57e-06             9.67e-06          2.15e-07
relative.c/z            2.32e-12             2.32e-12             6.59e-12          1.82e-13
triangle.c/A            1.44e-04             1.73e-04             8.09e-04          0.0
Unstable branches:
comp abs.c/z            3.58e-07             2 (false alarm)      4 (false alarm)   -2.85e-08
comp cont.c/z           5.03e-05             9.03e-05             3 (false alarm)   -2.25e-08
comp cont nested.c/z    1.0e-18              1.0e-18              n/t               -1.0e-18
comp cont mult.c/res    3.40e-05             105 (false alarm)    192               ko (unstable)
comp disc nested.c/z    0.1 (true alarm)     0.1                  n/t               ko
comp disc.c/z           0.5 (true alarm)     1.0                  2                 ko
comp model err.c/S      0.023 (true alarm)   3.82e-01             ko                ko
Interpolation tables:
inter cond.c/res        1.33e-05             105 (false alarm)    191               4.77e-07
inter loop.c/res        1.45e-06             4.05e-06             33                -4.60e-07
inter tbl cast.c/out1   4e-06                77.1 (false alarm)   time out          -1.04e-15
inter tbl loop.c/res    4e-08                ko                   n/t               -1.04e-15
motiv example.c/out1    1.19e-07             77.1 (false alarm)   time out          -1.04e-08
motiv example.c/out2    4 (true alarm)       95.1                 time out          ko
Maths:
sin model error.c/res   2.57e-16             2.57e-16             n/t               8.79e-18
sqrt unroll.c/t.v       7.10e-15             7.81e-14             n/t               -4.81e-15
sqrt fixpoint.c/res     3.15e-15             1.39e-14             n/t               3.51e-16
Miscellaneous:
filter.c/S              1.56e-14             1.65e-14             time out          1.44e-16
patriot.c/t             1.91e-04             1.91e-04             time out          1.91e-04
complex LU.c/det        7.14e-15             ko                   ko                7.14e-15
complex intersect.c/x   5.32e-01             0.2                  ko                ko
scanf.c/res             5.96e-07             ko                   ko                ko


                Fig. 14: Tool comparison over small-size C examples.



with Fluctuat [6], Precisa [20] and FpDebug [5]. Figure 14 presents the results of
our evaluation. ko identifies a case where the tool is not pertinent (scalability,
unmanaged unstable branch) or when a reasonable bound for accuracy is not
verified. n/t means “not translated” into PVS for Precisa. A number reports the
accuracy that the tool infers. If written in bold, that is the best accuracy for a
particular example. Therefore, the table clearly shows that our toolchain has
almost always the best accuracy.
   Since FLDLib uses the same reasoning as Fluctuat except on the constraint
management, many results are merely the same. However, Fluctuat has only a
minor support of unstable branches. FpDebug also lacks of support of unstable
branches. That explains why our toolchain is often better than these tools. The
comparison with Precisa is somehow biased since SMT optimization with FPRock
was not activated. We do not know if it would have scaled better with this
optimization. Nevertheless our toolchain aims to provide guaranteed accuracy
analysis with unstable branches on existing C code containing loops and several
thousands of lines of source code, while Precisa is more concerned with robustness
proofs of smaller algorithms.


Industrial case studies. We also experimented our toolchain on two (non public)
industrial case studies (synchronous reactive systems of several dozens of thou-
sands of lines of code). The C code of the first one was automatically generated,
whereas the code of the second one was written by hand in C++. The first one
contains computations that represent physical models, with many components
like interpolation tables. One component (convergent linear filters) deals with
memory management and not only with numerical computations. The second use
cases contains solving algorithms and uses external libraries base on templates.
    FLDCompiler was used to identify the location of the split-merge annota-
tions and the list of variables that must be saved and merged. Even if we only
used its syntactic version that is not based on the Eva plug-in of Frama-C (re-
sulting in a loss of precision), the results were pretty good and useful. However,
these case studies shown that FLDCompiler need to be extended to provide bet-
ter results on some linear algebra algorithms and some discontinuous unstable
branches. For example, the determinant computation is a continuous formula but
it often internally uses a LU (Lower/Upper) matrix decomposition that contains
many unstable branches due to the choice of the best pivoting number. Delaying
the merging point as done by FLDCompiler results in that case in a combinatorial
explosion. In practice, we choose only one particular matrix decomposition to
go on: by default it is the one that has been created by the last execution path
between the split and the merge.
    FLDLib scales better that Fluctuat on these case studies since it does not care
about pointers. Nevertheless, FLDLib’ scalability is directly related to the trade-
off between precise results and analysis’ times: if the number of noise symbols in
zonotopes is not bounded, the analysis may be quadratic. In practice, an option
sets a bound to limit the number of noise symbols introduced in an affine form.
    On the first generated industrial C code, our toolchain succeeds in keep-
ing a reasonable error for a thin scenario and such avoiding excessive over-
approximations. On the second industrial C++ code, the guaranteed numerical
error delivered by FLDLib increases at every loop cycle and false alarms appear
because more and more unstable branches are detected. That leads to a combi-
natorial explosions in solving algorithms of FLDCompiler (when the merge point
is far from the split point in terms of instructions). In such a case FLDLib has
rather been used to identify the tricky numerical parts of a big code.
    All in all, these industrial use cases demonstrate that our toolchain scales
on thin scenarios up to several dozens of thousands of lines of code. At worst, a
few split-merge points have to be manually set and FLDLib provides an helpful
support for this task. It is also worth noting that FLDLib can be replaced by
Cadna to obtain a stochastic analysis that scales better, even if the results are
non-necessarily sound but close to the expected ones. We have also experimented
the exact part of FLDLib that roughly works like FpDebug, but at source code
level. With this component we obtain under-approximated results.
     Last but not least, our toolchain may be easily integrated within a continuous
integration setting. For that purpose, it only requires to instrument the unit test
files. Any other file (including library file) can remain unchanged.


6     Related Work

Verification of accuracy properties remains a challenging research topic. During
the last fifteen years, many tools and academic prototypes have been developed
to tackle this problem. They can be classified in two categories: testing tools and
static analysis tools.
    Let us consider testing tools first. FpDebug [5] and Herbgrind [21] are two
tools based on Valgrind [22] that are designed to avoid false positive reports.
FpDebug relies on MPFR 8 to associate a highly-precise value to each floating-
point value of the tested program. If the difference between both values is too
large, an error is reported. It guarantees that no reported problem is a false pos-
itive, but it can miss problems that need better precision. Herbgrind evaluates
rounding errors in a similar way but, in addition, it uses symbolic execution to
detect important accuracy loss and track the root causes of those losses. Unlike
our toolchain, FpDebug and Herbgrind avoid false positive reports and scale up
on bigger programs. However, our toolchain can guarantee that there is no error
in the program. Verrou [23], Cadna [4], and Verificarlo [24] are other examples of
testing tools that aim at reporting possible instances of errors. They use stochas-
tic protocols to give error estimations. The core idea consists in randomly (with
a selected probability) changing the rounding mode used for each floating-point
operation encountered during the program execution. For each execution, the
obtained floating-point values differ, and with enough executions, an estima-
tion can be made. Note that Cadna infers three different executions during one
analysis. The stochastic process allows to obtain a good confidence in such an
estimation, even if it cannot provide any guarantee. Like our toolchain, those
three tools do not avoid false positive reports because of the stochastic process.
However, unlike us, they cannot guarantee the absence of errors for the same
reason.
    For static analysis tools, different trade-offs exist between scalability and
tightness of over-approximations. Precisa [20] and Fluctuat [6] are based on ab-
stract interpretation and favor scalability. Both of them handle unstable tests;
Precisa manage them more rigourously, but Fluctuat scales reasonably for pro-
grams of a few thousand lines of code. Precisa uses interval arithmetic combined
with branch-and-bound optimization and symbolic error computations, while
Fluctuat relies on the zonotope abstract domain [19] to represent both the val-
ues and the errors along the analyzed program. Compared to Precisa and Fluc-
tuat, our toolchain scales better and can handle I/O and memory manipulations
without the need of stubs. Another tool is FPTaylor [25]. It favors tightness. For
that purpose, it formulates the problem of bounding errors as an optimization
8
    https://www.mpfr.org
problem that is soundly solved by using first-order Taylor approximations of
arithmetic expressions. Bounds are found on the transformed expressions by us-
ing expensive optimization procedures. However, they allow FPTaylor to provide
tight over-approximations of absolute and relative errors. FPTaylor generally pro-
vides tighter approximations than our toolchain. However, unlike our toolchain,
it cannot analyze large programs and handles neither loops, nor I/O operations,
nor unstable tests. Finally, Gappa [26] presents a third possible trade-off. Indeed,
Gappa is intended to help verifying and formally proving properties on numer-
ical programs. It is based on interval arithmetic and several rewriting rules for
floating-point rounding errors expressions. It can generate proof certificates that
can be verified using the Coq proof assistant and is also used as a backend prover
for the Why3 software verification platform. The interest of our toolchain lies in
its ability to relatively scale and in its management of I/O and memory manip-
ulations without the need of stubs. However, the goal of those tools is to prove
numerical properties for large input domains, while our toolchain is limited to
thin scenarios.


7   Conclusion and Perspectives

Assessment of numerical accuracy in critical programs is crucial to prevent ac-
cumulation of rounding errors that can provoke dangerous bugs. In this work,
we presented the design and implementation of a new toolchain for evaluation
of numerical accuracy properties in C programs. It is based on abstract com-
pilation, embedding an accuracy analysis engine into the compiled code whose
execution allows accuracy property assessment. This work relies on several in-
dependent original contributions: an extension of the runtime verification tool
E-ACSL to precisely support rational numbers, the design of the abstract com-
piler FLDCompiler and an instrumentation library, FLDLib, for reasoning about
numerical properties.
    The proposed approach combines the precision of testing-based techniques
with the capacity of static analysis to analyze several executions at the same
time. Initial experiments confirm the interest of the proposed technique, in par-
ticular, for industrial software. Future work includes a proof of soundness for
the whole toolchain, a large evaluation on real-life programs and an extension of
the toolchain to support all features of the C programming language, as well as
specific ACSL built-ins (e.g. \exact, \round error) capable to express powerful
properties over floating-point and real numbers.

Acknowledgement. The authors thank Romain Soulat and Thales Research &
Technology for providing case studies and participation in the evaluation. We
are also very grateful to Jean Gassino, Gregory de la Grange and IRSN for their
support and evaluation on additional case studies.
References
 1. Monniaux, D.: The pitfalls of verifying floating-point computations. Transactions
    on Programming Languages and Systems (TOPLAS) 30(3) (may 2008)
 2. Cousot, P., Cousot, R.: Abstract interpretation: a unified lattice model for static
    analysis of programs by construction or approximation of fixpoints. In: Symposium
    on Principles of Programming Languages (POPL). (1977)
 3. Signoles, J., Kosmatov, N., Vorobyov, K.: E-ACSL, a Runtime Verification Tool
    for Safety and Security of C Programs. Tool Paper. In: International Workshop on
    Competitions, Usability, Benchmarks, Evaluation, and Standardisation for Run-
    time Verification Tools (RV-CuBES). (September 2017)
 4. Jézéquel, F., Chesneaux, J.M.: CADNA: a library for estimating round-off error
    propagation. Computer Physics Communications 178(12) (2008) 933–955
 5. Benz, F., Hildebrandt, A., Hack, S.: A dynamic program analysis to find floating-
    point accuracy problems. In: Conference on Programming Language Design and
    Implementation (PLDI). (June 2012)
 6. Goubault, E., Putot, S.: Static analysis of finite precision computations. In: Inter-
    national Conference on Verification, Model Checking, and Abstract Interpretation
    (VMCAI). (January 2011)
 7. Goubault, E., Putot, S.: Robustness analysis of finite precision implementations.
    In: Asian Symposium on Programming Languages and Systems (APLAS). (De-
    cember 2013)
 8. Baudin, P., Filliâtre, J.C., Marché, C., Monate, B., Moy, Y., Prevosto, V.: ACSL:
    ANSI/ISO C Specification Language. http://frama-c.com/acsl.html.
 9. Goldberg, D.: What Every Computer Scientist Should Know About Floating-Point
    Arithmetic. ACM Computing Surveys 23(3) (March 1991)
10. Muller, J., Brisebarre, N., de Dinechin, F., Jeannerod, C., Lefèvre, V., Melquiond,
    G., Revol, N., Stehlé, D., Torres, S.: Handbook of Floating-Point Arithmetic.
    Birkhäuser (2010)
11. Signoles, J.: E-ACSL: Executable ANSI/ISO C Specification Language. http:
    //frama-c.com/download/e-acsl/e-acsl.pdf.
12. Delahaye, M., Kosmatov, N., Signoles, J.: Common specification language for
    static and dynamic analysis of C programs. In: Symposium on Applied Computing
    (SAC). (March 2013)
13. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-C:
    A Software Analysis Perspective. Formal Aspects of Computing (January 2015)
14. Jakobsson, A., Kosmatov, N., Signoles, J.: Rester statique pour devenir plus rapide,
    plus précis et plus mince. In: Journées Francophones des Langages Applicatifs
    (JFLA). (January 2015) In French.
15. Pierce, B.: Types and Programming Languages. MIT Press (2002)
16. Prosser, R.T.: Applications of Boolean Matrices to the Analysis of Flow Diagrams.
    In: Eastern Joint IRE-AIEE-ACM Computer Conference. (December 1959)
17. Léchenet, J., Kosmatov, N., Le Gall, P.: Cut branches before looking for bugs:
    certifiably sound verification on relaxed slices. Formal Aspects of Computing 30(1)
    (2018) 107–131
18. Blazy, S., Bühler, D., Yakobowski, B.: Structuring abstract interpreters through
    state and value abstractions. In: International Conference on Verification, Model
    Checking, and Abstract Interpretation (VMCAI). (January 2017)
19. Ghorbal, K., Goubault, E., Putot, S.: The Zonotope Abstract Domain Taylor1+.
    In: International Conference on Computer Aided Verification (CAV). (July 2009)
20. Titolo, L., Muñoz, C.A., Feliú, M.A., Moscato, M.M.: Eliminating unstable tests in
    floating-point programs. In: Logic-Based Program Synthesis and Transformation
    (LOPTSR). (September 2018)
21. Sanchez-Stern, A., Panchekha, P., Lerner, S., Tatlock, Z.: Finding root causes of
    floating point error with herbgrind. CoRR abs/1705.10416 (2017)
22. Nethercote, N., Seward, J.: Valgrind: A Framework for Heavyweight Dynamic
    Binary Instrumentation. In: Conference on Programming Language Design and
    Implementation (PLDI’07). (June 2007)
23. Févotte, F., Lathuilière, B.: Studying the numerical quality of an industrial com-
    puting code: A case study on code aster. In: Numerical Software Verification
    (NSV). (July 2017)
24. Denis, C., de Oliveira Castro, P., Petit, E.: Verificarlo: Checking floating point
    accuracy through monte carlo arithmetic. In: Symposium on Computer Arithmetic
    (ARITH). (July 2016)
25. Solovyev, A., Baranowski, M.S., Briggs, I., Jacobsen, C., Rakamaric, Z., Gopalakr-
    ishnan, G.: Rigorous estimation of floating-point round-off errors with symbolic
    taylor expansions. Transactions on Programming Languages and Systems 41(1)
    (2019)
26. Daumas, M., Melquiond, G.: Certification of bounds on expressions involving
    rounded operators. Transactions on Mathematical Software 37(1) (2010)
