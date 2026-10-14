                                                 Computer-Assisted Verification of Four Interval Arithmetic Operators

                                                                                           Daisuke Ishiia , Tomohito Yabua
                                                          a Department of Information Science, University of Fukui. 3-9-1 Bunkyo, Fukui-shi, Fukui, 910-8507, Japan




                                        Abstract
                                            Interval arithmetic libraries provide the four elementary arithmetic operators for operand intervals bounded by
arXiv:2003.10623v2 [cs.LO] 8 Apr 2020




                                        floating-point numbers. Actual implementations need to make a large case analysis that considers, e.g., magnitude
                                        relations between all pairs of argument bounds, positional relations between the arguments and zero, and handling of
                                        the special values, ±∞ and NaN. Their correctness is not obvious as they are implemented by human hands, which
                                        comes to be critical for the reliability. This work provides a mechanically-verified interval arithmetic library. For this
                                        purpose, we utilize the Why3 platform equipped with a specification language for annotated programs and back-end
                                        theorem provers. We conduct several proof tasks for each of three properties of the target code: validity, soundness,
                                        and tightness; zero division exception handling is also verified for the division code. To accomplish the proof, we
                                        propose several techniques for specification/verification. First, we specify additional lemmas that support deductions
                                        made by back-end SMT solvers, which enable to discharge proof obligations in floating-point arithmetic containing
                                        nonlinear terms. Second, we examine the annotation of tightness, which requires to assume that a computation may
                                        result in NaN; we propose specific extremum operators for this purpose. In the experiments, applying the techniques
                                        in conjunction with the Alt-Ergo SMT solver and the Coq proof assistant proved the entire code.
                                        Keywords: Interval Arithmetic, Floating-Point Numbers, Program Verification, SMT Solvers, Proof Assistants



                                        1. Introduction

                                            Interval arithmetic [1, 2] is a reliable method for numerical computation that deals with reals. It handles (machine-
                                        representable) intervals instead of numerical values, typically floating-point (FP) numbers, and evaluates arithmetic
                                        expressions via computing their interval enclosures with careful control of rounding modes and interval widening.
                                        The four elementary arithmetic operators on intervals can be implemented in an efficient way that only considers the
                                        bounds of the given argument intervals. However, actual implementations need to make a large case analysis that
                                        considers, e.g., magnitude relations between all pairs of argument bounds, positional relations between the arguments
                                        and zero, and handling of the special values, ±∞ and NaN. For instance, the implementation of the multiplication in
                                        the kv library [3] comprises 13 branches. As existing code bases are implemented by human hands, their correctness
                                        is not obvious, which comes to be critical for the reliability.
                                            In this work, we use Why3 to prove the correctness of the code. Why3 [4, 5] has been developed as a program
                                        verification platform, which integrates automated theorem provers (e.g. SMT solvers) and interactive proof assistants
                                        (e.g. Coq). Why3 provides a specification language WhyML to describe a target program and to annotate the program
                                        with meta-level properties. Given a specification, Why3 generates verification conditions (VCs) that ensure the cor-
                                        rectness when they are all validated. Users can then apply the back-end provers in succession to discharge all of the
                                        VCs. Targets of Why3 include numerical programs and several applications have been reported (e.g. [6]), as support
                                        for the numerical domain has been developed both in the platform and its back-end provers.
                                            This study aims for the verification of the four interval arithmetic operations, i.e., addition, subtraction, multi-
                                        plication and division. For this purpose, we translate an implementation into WhyML and properly annotate the pre-
                                        conditions and postconditions. For the generated VCs, we experiment with discharging them via utilizing back-end


                                            Email address: dsksh@acm.org (Daisuke Ishii)

                                        Preprint submitted to Journal of Computational and Applied Mathematics                                                        March 18, 2020
                                        c 2020. This manuscript version is made available under the CC-BY-NC-ND 4.0 license
                                        http://creativecommons.org/licenses/by-nc-nd/4.0/
provers, Alt-Ergo [7] and Coq. Although the control structure of the implementation is simple, which only consists
of branching statements, proof obligation becomes complicated due to combinations of FP number expressions and
the axioms that realize the system of FP numbers/intervals in Why3. Several VCs thus remain unproved after a basic
usage of Why3. Therefore, we examine the target annotated code and propose techniques to complete the verification.
Finally, we show that the entire annotated code is verified and present experimental measures such as timings.

1.1. Contribution
    This contribution is a mechanical proof of an implementation of the four operators, which verifies mainly three
properties: validity (“the results conform to the definition of intervals”), soundness (“the results enclose every possible
real values”) and tightness (“the resulting enclosures are optimal/tightest”). Our verification result indicates that the
operators, which compute with the bounds of operand intervals and return the hull of computed results, satisfy the
three properties.
    To complete the proof, we propose several techniques to specify/verify the target interval operations and their
properties. First, through an examination of each unproved VC, we find that specifying an additional lemma will help
the Alt-Ergo SMT solver to discharge the VC. For instance, for a VC on FP numbers, a lemma on reals involving the
same expression as the VC may help to discharge it. We identify 19 lemmas needed for the complete verification.
Second, we propose a specification of the tightness property of an interval computation such that the code annotated
with the property is verified by SMT solvers. In this specification, it is essential to reformulate the interval hull
operation with a consideration of NaN.
    We note that the target of above techniques is not limited to interval arithmetic operations but applicable to various
proof tasks in the numerical domain, e.g., verification of other interval functions and application programs.

1.2. Outline
    Section 2 introduces basic notions and concepts of interval arithmetic. Section 3 explains the main tools for veri-
fication: Why3 and Alt-Ergo. The following sections describe the main verification process for an interval arithmetic
code. First, Section 4 gives an overview of the process. Second, Section 5 explains the specification of the target
code. Next, Section 6 and Section 7 describe the processes of annotating the pre- and postconditions to the code and
discharging the generated proof obligations. Section 8 reports the complete results of the verification experiment.

2. Interval Arithmetic

     Interval arithmetic [1, 2, 8] is a method for reliable numerical computations, which replaces the FP numbers that
are usually used in numerical computation with intervals that enclose values in R; the result should contain all the
solutions calculated for every real in the given input interval.
     Before introducing intervals, we consider sets of machine-representable numbers that conform to IEEE-754 stan-
dard [9], i.e., floating-point (FP) numbers. In the following, F denotes a set of finite FP numbers including the signed
zeros (−0 and +0; we also denote +0 by 0). Additionally, special FP data, i.e., −∞, +∞, NaN, are considered ac-
cording to the context. In the following, we assume IEEE-754’s comparison operators {<, >, ≤, ≥, =} for FP numbers
in F ∪ {±∞, NaN}; for example, +0 = −0 holds and NaN ≤ x does not hold for x ∈ F ∪ {±∞, NaN}. Given a
real x̃ ∈ R, ▽( x̃) and △( x̃) denote the downward and upward rounded values in F ∪ {−∞, +∞} and are defined by
▽( x̃) := max{x ∈ F ∪ {−∞} : x ≤ x̃} and △( x̃) := min{x ∈ F ∪ {+∞} : x ≥ x̃}. Additionally, we assume the four
operators for FP numbers ⊙ ∈ {+, −, ×, ÷}. For x, y ∈ F ∪ {±∞}, ▽(x ⊙ y) and △(x ⊙ y) denote the downward and
upward rounded values of the operation ⊙. Special cases are handled according to IEEE-754 and the semantics in
[10]: Infinity arithmetic, e.g., 0 − +∞ = −∞; invalid operations, e.g., +∞ − +∞ = NaN; and overflows, e.g., positive
overflow of ▽(x ⊙ y) evaluates to max F; we also assume that underflows result in correctly rounded values.
     An interval x = [x, x] is defined as a closed connected set { x̃ ∈ R : x ≤ x̃ ≤ x}, where x ≤ x. In an actual
implementation, the lower and upper bounds x and x are restricted to FP numbers in F. We also consider the entire
interval [−∞, +∞] := R and half-bounded intervals [x, +∞] := { x̃ ∈ R : x ≤ x̃} and [−∞, x] := { x̃ ∈ R : x̃ ≤ x}, where
x, x ∈ F. IF denotes the set of intervals, which contains the entire interval and the closed/half-bounded intervals
bounded by FP numbers in F ∪ {±∞}. Intervals are considered as overapproximations of (non-empty) sets S ⊆ R of
interest; when the extrema of a set are not representable in IF, we consider an interval whose lower/upper bounds are

                                                            2
rounded downwards/upwards. Given a set S ⊆ R, An optimal (tightest) overapproximation is obtained by the hull
operation hull(S ) := [▽(inf S ), △(sup S )].
    Recently, interval arithmetic has been standardized [8]. The standard is layered into four levels as in IEEE-
754 and it is parameterized with the notions such as flavors and decorations to be adapted to various models and
implementations. The interval arithmetic in this paper deals with a variant of the set-based flavor. It is different in
that we consider neither empty intervals nor division by an interval containing zero. The set-based flavor represents
the empty set as empty intervals, e.g. [x, x] where x > x and [−∞, −∞], but our IF does not contain them. In the
set-based flavor, x ÷ [0, 0] is computed as an empty interval, and other divisions by intervals containing zero can be
done with the two-output division scheme, whereas our division operator throws an exception. Otherwise, our interval
arithmetic is “classical” [8], which is based on the “simple model” [11]. In this paper, we intend to make the interval
arithmetic code simple without missing the essential verification process. We consider the process will be applied to
other extensions in a future work.
    Now, we introduce a definition of the four arithmetic operations on intervals.

Definition 1 (Four interval arithmetic operators) For x, y ∈ IF and ⊙ ∈ {+, −, ×, ÷},
                      x ⊙ y := hull({x ⊙ y : x ∈ x, y ∈ y})     (We assume 0 < y when ⊙ = ÷).
    The following theorem gives the basic principle for the tight implementation of the interval operators, namely to
take the hull of the values computed with the bounds of operand intervals.

Theorem 1 For x, y ∈ IF and ⊙ ∈ {+, −, ×, ÷} (we assume 0 < y when ⊙ = ÷),
                                                                                                   
       x ⊙ y ⊇ min ▽(x ⊙ y), ▽(x ⊙ y), ▽(x ⊙ y), ▽(x ⊙ y) , max △(x ⊙ y), △(x ⊙ y), △(x ⊙ y), △(x ⊙ y) ,           (1)
where for S ⊆ F ∪ {±∞, NaN},
                                                                       
                   min(S − {NaN}) if S , {NaN},
                   
                                                                       max(S − {NaN}) if S , {NaN},
                                                                        
                                                                        
        min S :=                                              max S :=                                           (2)
                   0
                                  if S = {NaN},                        0
                                                                                       if S = {NaN}.
    See Appendix A for the proof. Because the above theorem serves as a basis for the tightness specification in
the following sections, we only consider the one-way inclusion ⊇ in (1). In the theorem, we use modified extremum
operators min and max with an unusual handling of NaN, which occurs in some FP computations, e.g., +∞ − +∞
and 0 × +∞. They evaluate to zero when all the arguments are NaN (with the second cases), whereas the operators of
IEEE-754 evaluate to NaN. The min and max operators in the right-hand sides of (2) select the extrema based on the
ordinary comparison between FP numbers, e.g., min{0, +∞} = 0. For example, a subtraction and a multiplication are
performed as:
                                                                                       
                     [0, +∞] − [0, +∞] ⊇ min 0, −∞, +∞, NaN , max 0, −∞, +∞, NaN
                                                                              
                                        = min{0, −∞, +∞}, max{0, −∞, +∞} = [−∞, +∞],
                                                                
                     [0, 0] × [−∞, +∞] ⊇ min NaN}, max {NaN} = [0, 0].
In our context, the second cases of (2) only happen in the multiplications of [0, 0] and [−∞, +∞].
    Several libraries that implement the interval four operators have been developed, e.g., PROFIL/BIAS,1 filib++,2
Boost Interval Arithmetic Library,3 gaol,4 libieeep1788,5 INTLAB,6 GNU Octave interval package,7 and kv [3]. In the
actual code base, the multiplication and division operators are implemented as nested branching statements based on
a careful case analysis. The number of branches increases further due to other factors such as optimizations to reduce
the number of rounding mode controls [12], data-level parallelization [13] and multi-precision FP computation [3].

  1 http://www.ti3.tuhh.de/keil/profil/index_e.html
  2 http://www2.math.uni-wuppertal.de/wrswt/software/filib.html
  3 https://www.boost.org/doc/libs/1_72_0/libs/numeric/interval/doc/interval.htm
  4 http://frederic.goualard.net/#research-software
  5 https://github.com/nadezhin/libieeep1788
  6 http://www.ti3.tu-harburg.de/rump/intlab/
  7 https://octave.sourceforge.io/interval/index.html


                                                          3
3. Why3 Platform and Alt-Ergo SMT Solver

   The main tools used in this work are Why3 and Alt-Ergo.

3.1. Overview of the Tools
    Why3 (version 1.1.0) [4, 5] is a platform for deductive program verification, which provides: (i) a specification lan-
guage WhyML to describe programs and specifications; (ii) a verification condition (VC) generator that applies weakest
precondition calculus to the annotated programs; and (iii) a proof intermediate interface that facilitates discharging
the VCs using the back-end automated/interactive theorem provers. Why3’s back-end theorem provers include SMT
solvers, e.g., Alt-Ergo [7], CVC4 and Z3,8 and theorem proof assistants, e.g., Coq.9 The possible results of applying
an automated prover to discharge a VC are valid, invalid, timeout (within a configured time limit), or unknown. Why3
provides a GUI to allow users to browse a list of generated VCs. Users assign a back-end prover to each VC to validate
it. When provers cannot validate a VC, users are able to modify the VC (e.g., split one VC into several VCs) and
investigate a prover’s input/output though the GUI.
    WhyML is an OCaml-like language to describe functional programs and to annotate programs with first-order pred-
icate logic statements. The language has a type system, which provides the type real for real numbers, types for FP
numbers, user-defined record types, etc. WhyML also has a module system that encapsulates specification as a module;
basic modules are supplied in the standard library. There are two implementations of 64-bit FP numbers: the type t
provided by the ieee_float.Float64 module and the type double of the floating_point.DoubleFull module.
Running examples in this paper uses the former, which has been introduced in a recent version of Why3; it is compat-
ible with the FloatingPoint theory of SMT-LIB and processed by dedicated solvers when the VCs are discharged
with SMT solvers. The latter realizes a theory of FP numbers based on the theory of reals and the generated VCs are
encoded with the predicates on reals. The two modules provide arithmetic operators (with rounding mode control)
and comparison operators that conform to IEEE-754. FP numbers are related to real numbers using the rounding
functions and translation functions provided by either module.
    Alt-Ergo (version 2.2.0) [7] is an SMT solver, which shares various features with Why3. For example, Alt-Ergo
has a trigger mechanism that allows users to guide the solver towards the proof, using a user-defined lemma. In WhyML,
auxiliary lemmas can be specified with triggers and they are utilized by Alt-Ergo. In our experiments, with the help
of several user-defined lemmas, Alt-Ergo discharged the most VCs.

3.2. Program Verification Process Using Why3
     A user of Why3 verifies a program through performing the following tasks.
     Specification of the target code, properties and lemmas. The user implements the target code in the WhyML lan-
guage and annotates the properties to the code as preconditions and postconditions. Here, requirements for the code
should be better represented as simple and generic properties; however, such properties tend to require more efforts to
verify. In our work, we investigate an intuitive yet provable representation of the tightness property (cf. Theorem 1).
Also, the user is able to annotate properties about intermediate states by inserting assert formulas in the middle
of the code, and specify lemmas related to the properties besides the code. These auxiliary annotations will help
automated deductions performed by provers like Alt-Ergo.
     Generation of VCs and proving with back-end provers. Once an annotated WhyML program is fed to the Why3 tool,
a set of VCs are generated; discharging them all entails the correctness of the annotated program. The user is able
to modify the VCs by applying logical transformations; for example, s/he can split a VC into several VCs which are
easier to prove. Then, s/he applies a prover to each VC to check its validity. In this work, we first apply SMT solvers,
i.e., Alt-Ergo and Z3, and then invoke the Coq tool for manual proving.
     Analysis on unprovable VCs and modification of the specification. When VCs are not provable, the user returns
to the specification task to modify either the target code or the annotations. Since the automated proving processes
of VCs are incomplete in general, they may fail to prove VCs even for a correct specification. In such cases, the user
should make an effort in finding a specification that results in provable VCs. Here, an interactive proof task with Coq


  8 Alt-Ergo: https://alt-ergo.ocamlpro.com/; CVC4: https://cvc4.github.io/; Z3: https://github.com/Z3Prover/z3
  9 https://coq.inria.fr/


                                                            4
may help to understand the proof context and to identify an additional lemma that is useful to discharge the proof goal.
In this work, we actually make such analyses; as a result, we insert assertions within the code and specify lemmas to
help Alt-Ergo’s proof process.

4. Towards a Verified Interval Arithmetic Library

    The goal of this study is to verify the correctness of an implementation of the four interval arithmetic operators.
The implementation code is first cloned from the kv library [3] and then modified to conform to Theorem 1 (see
Section 5.3 for details). To achieve this goal, we apply the verification process described in Section 3.2 to the operator
code. This section describes the properties we aim at verifying.
    When interval operators are implemented in a programming language (e.g. WhyML), without loss of generality, we
can assume that intervals are represented as pairs of FP numbers such as x = (x, x) where x and x can be arbitrary FP
numbers in F ∪ {±∞, NaN}; we denote the set of such pairs by IF∗ in this section. In the following, we denote that a
pair x ∈ IF∗ is a valid interval by x ∈ IF. Accordingly, interval operations ⊙ ∈ {+, −, ×, ÷} will be implemented as
procedures f⊙ : IF∗ × IF∗ → IF∗ .
    The properties are specified as one precondition and four postconditions, i.e., first-order conditions in R, F, IF
and IF∗ . Here, we present a high-level specification of the pre- and postconditions.

Definition 2 (Pre- and postconditions) Let x, y, r ∈ IF∗ be pairs of FP numbers, ⊙ ∈ {+, −, ×, ÷} be an operation,
and f⊙ be an implementation of the interval operation, which is interpreted as a function IF∗ × IF∗ → IF∗ . Then, the
precondition PV and the postconditions QV , QS , QT and QZ of computation r := f⊙ (x, y) are specified as follows:

                (Validity precondition)              PV :≡ x ∈ IF ∧ y ∈ IF,
               (Validity postcondition)              QV :≡ r ∈ IF,
            (Soundness postcondition)                QS :≡ ∀ x̃ ∈ x, ∀ỹ ∈ y, x̃ ⊙ ỹ ∈ r,
                                                                       
             (Tightness postcondition)               QT :≡ r = min ▽(x ⊙ y), ▽(x ⊙ y), ▽(x ⊙ y), ▽(x ⊙ y) ,
                                                                                                              
                                                                    max △(x ⊙ y), △(x ⊙ y), △(x ⊙ y), △(x ⊙ y) ,
          (Exceptional postcondition)                QZ :≡ 0 ∈ y.

    Note that, in the right-hand sides, each appearance of the operator ⊙ acts as that for reals or FP numbers. In
the definition, first, the precondition PV states that the operand pairs of FP numbers are valid intervals, i.e., their
lower (resp. upper) bounds are in F ∪ {−∞} (resp. F ∪ {+∞}) and the magnitude relation holds between the lower
and upper bounds. Second, similar to PV , the postcondition QV states the validity of the computation result. Third,
the postcondition QS states the soundness: “The result contains every possible real operation results.” Fourth, the
postcondition QT states the tightness: “The result is an optimal/tightest overapproximation of the four computations
with the argument FP numbers.” Finally, QZ is the postcondition for the case where the computation of f÷ throws the
zero division exception.
    If the target code is executed, it will perform an operation and either terminate normally or throw an exception
that signals zero division when ⊙ = ÷. For the case where the code terminates normally, we first verify that a result r
is an interval that overapproximates the true results in { x̃ ⊙ ỹ : x̃ ∈ x, ỹ ∈ y} (QV and QS ). Secondly, we verify that
r is an optimal overapproximation as described in Theorem 1 (QT ). Here, we take into account the overflow cases as
they are specified in the Why3’s module. Finally, for the exceptional case, we verify that the code correctly detects
the zero division (QZ ). Our result contains a proof of a variant of Theorem 1: Soundness of the right-hand side of (1).
    The representation of the tightness in QT is rather restrictive as it assumes the monotonicity of the operations.
More generic representation (e.g. ∀r̃ ∈ r, ∃ x̃ ∈ x, ∃ỹ ∈ y, r̃ ∈ (hull( x̃) ⊙ hull(ỹ))) is preferable but it will certainly make
the verification process less automated and more difficult, which involves many interactive proof tasks. In this work,
we aim at making the proof process automated and simple with a restrictive annotation.




                                                                5
1    module Interval
2      use real.Real
3      use ieee_float.Float64
4      use Float64Ex
5

6     type interval = { inf: Float64.t; sup: Float64.t }
7

8     predicate real_in (a: real) (x: interval) =
9       ((t’isFinite x.inf /\ t’real x.inf <= a) \/ is_minus_infinity x.inf) /\
10      ((t’isFinite x.sup /\ t’real x.sup >= a) \/ is_plus_infinity x.sup)
11

12    val constant zeroI : interval
13      ensures{ is_zero result.inf /\ is_zero result.sup }
14

15    lemma zeroR_in_zeroI: real_in 0. zeroI
16

17    predicate valid (x: interval) =
18      (t’isFinite x.inf \/ is_minus_infinity x.inf) /\
19      (t’isFinite x.sup \/ is_plus_infinity x.sup) /\ x.inf .<= x.sup
20

21     lemma valid_not_nan: forall x. valid x -> is_not_nan x.inf /\ is_not_nan x.sup
22     lemma valid_zeroI: valid zeroI
23   end


                                          Figure 1: Specification of the interval module.


                                Table 1: Some vocabularies for FP numbers (x, y ∈ F ∪ {±∞, NaN}).
          Expression        Interpretation                      Expression                      Interpretation
          is_zero x         ⇔ x = −0 or x = +0                  t’isFinite x                    ⇔ x∈F
          zeroF             = +0                                is_plus_infinity x              ⇔ x = +∞
          x .<= y           ⇔ x ≤ y (cf. IEEE-754)              is_infinite x                   ⇔ x = −∞ or x = +∞
          mul_down x y      = ▽ (x × y)                         is_not_nan x                    ⇔ x is not NaN


 5. Target Code: Interval Multiplication Procedure

    In the following sections, we consider interval multiplication as a running example. This section explains how we
 specify intervals (Section 5.1) and an interval procedure (Section 5.2) with the WhyML language. Also, Section 5.3
 explains a difference between our code and the original code. Additional notes on specifying other operators are
 described in Appendix B.

 5.1. Specification of Intervals
     We consider interval operations as procedures that handle data of the interval type, which is specified in a
 dedicated Why3 module (Figure 1) named Interval; related constants, predicates and lemmas are also specified
 in this module. In Figure 1, first, the modules for real numbers and FP numbers are imported at Lines 2–4; these
 modules provide type real, type Float64.t (double-precision FP number), and related types, constants, operators
 and predicates (some of them are summarized in Table 1). Most of them are specified by a set of WhyML axioms, e.g.,
 the operator .<= is specified as follows.
     forall x y. x .<= y -> ( (is_finite x /\ is_finite y) \/
       (is_minus_infinity x /\ is_not_nan y) \/ (is_not_nan x /\ is_plus_infinity y) )
 The Float64Ex module imported at Line 4 is our own module that provides auxiliary vocabularies for FP numbers
 (some are shown in Table 1). Second, the type interval is defined at Line 6 as a record combining the lower (inf)
                                                                6
1    module IntervalMul
2      use real.Real
3      use ieee_float.Float64
4      use Float64Ex
5      use Interval
6

7      let multiply (x y: interval) : interval
8        (* pre- and postconditions are specified here *)
9      = if x.inf .>= zeroF then
10         if x.sup .= zeroF then
11           zeroI
12         else
13           if y.inf .>= zeroF then
14             if y.sup .= zeroF then
15               zeroI
16             else
17               { inf = mul_down x.inf y.inf; sup = mul_up x.sup y.sup }
18           else if y.sup .<= zeroF then
19             { inf = mul_down x.sup y.inf; sup = mul_up x.inf y.sup }
20           else
21             { inf = mul_down x.sup y.inf; sup = mul_up x.sup y.sup }
22       (* other 8 branches are omitted *)
23   end


                                  Figure 2: Code snippet for multiplication of intervals: Case x ≥ 0.



 and upper (sup) bounds of type Float64.t. Third, the predicate real_in is defined at Lines 8–10 to state a ∈ x
 where a ∈ R and x ∈ IF. Fourth, the module specifies a constant interval zeroI, i.e., a point-wise interval containing
 0. It is specified using the is_zero predicate instead of specifying a concrete interval to represent either of intervals
 whose bounds are −0 or +0. At Line 15, there is a lemma characterizing zeroI, which may be used in an automated
 proof process. In the rest of the specification (Lines 17–22), the predicate valid x to state the validity of the value x
 of type interval is specified. For instance, it is used in the precondition PV to state that x ∈ IF. Then, two lemmas
 using valid are specified; valid_not_nan states that the bounds of valid intervals are not NaN; valid_zeroI states
 the validity of the constant specified above. Lemmas in a WhyML module are proved by Why3’s back-end provers. The
 three lemmas specified so far are proved using Alt-Ergo, where each proof takes less than 0.2s.

 5.2. Specification of Multiplication Procedure
     Interval multiplication code written as a WhyML function multiply is shown in Figure 2; only five branches are
 shown due to space limitations, but the full specification consists of 13 branches. At Lines 2–5, necessary modules
 are imported. Multiplication is defined by the WhyML function multiply at Lines 7–22. The procedure is specified as
 a nested if-then statement and the expressions inside are specified with predefined vocabularies for FP numbers and
 intervals.

 5.3. Modification of the Target Code
     In this work, one major modification was made against the codebase of the kv library (version 0.4.38). In the
 modification, Lines 11 and 15 of the code in Figure 2 were simplified; Line 11 of the original code was implemented
 as follows.
             if y.inf .= minus_inf || y.sup .= plus_inf then entireI else zeroI
 Line 11 corresponds to the case where x = [0, 0] and the modified code results in [0, 0], whereas the original code
 checks whether a y’s bound is ±∞ and returns either [−∞, +∞] or [0, 0]. Line 15 is likewise for switched x and y.
 Thus, the code comprises 17 branches. Our verification result suggests that the original code of kv unnecessarily

                                                                  7
enlarges some results from [0, 0] to [−∞, +∞], which is not correct regarding our tightness property. The original
code is correct in terms of the cset model [11] but it is not clear whether this design choice was made or not (cf. the
code does not support divisions by an interval containing zero). Based on our interval arithmetic flavor (Section 2),
our code is simplified and results in tighter intervals yet it is verified to be correct.

6. Validity and Soundness of Multiplication

   This section describes the verification process for the validity QV and soundness QS of the interval multiplication,
in which we annotate the target code with the properties (Section 6.1) and discharge the resulting VCs using the
Why3’s back-end provers (Section 6.2).

6.1. Specification of the Pre- and Postconditions
    We annotate the multiply function in Figure 2 with the properties in Section 4. The following pre- and postcon-
ditions, which encode PV , QV and QS of Definition 2, respectively, are inserted at Line 8 of the code. 10
      requires { valid x /\ valid y } (* P_V *)
      ensures { valid result } (* Q_V *)
      ensures { forall u v. real_in u x /\ real_in v y ->
        real_in (u * v) result } (* Q_S *)

6.2. Proof
     Next, we generate a proof obligation (i.e., a set of VCs) for the function multiply using the Why3 tool and try
to discharge (i.e., prove the validity of) the VCs using one of the back-end SMT solvers. This process can be easily
performed through the Why3 GUI. Here, two VCs for the postconditions are generated. However, for these VCs,
neither proof process of Alt-Ergo and Z3 does terminate after 10min. For that case, we can split the VC into 26
partial VCs (again through Why3’s GUI), each of which corresponds to one of the 13 branches and one of the two
postconditions; discharging them all entails the validity of the original VC. We apply Alt-Ergo to prove the split VCs;
it discharges 13 of them and leaves 13 VCs unproved.
     To prove the remaining VCs, we try to prove them interactively using the Coq proof assistant. An interactive
proof is pessimistic due to complication of the VCs involving intervals and FP numbers, which requires a number
of rewritings to accomplish the proof.11 The proof of such VCs are performed by SMT solvers more efficiently by
automating the rewritings when their search strategies are sufficient. However, this interaction is useful to identify an
auxiliary lemma that is helpful for SMT solvers. Indeed, for the VCs under consideration, we find that the following
lemma is useful for the proof with Alt-Ergo.
      lemma Rmult_le_compat: forall r1 r2 r3 r4 : real.
        0. <= r1 <= r2 /\ 0. <= r3 <= r4 -> r1 * r3 <= r2 * r4
By adding this lemma within the same module, two of the unproved VCs12 are discharged using Alt-Ergo. The above
lemma assumes the branching condition in Figure 2 (in reals) and describes a magnitude relation between the products
of the pairs of reals. The same lemma is considered in the proof in [14]. The lemma will be regarded as a relation
between the branching condition and the resulting state, when the variables are converted to the Float64.t type. The
lemma is difficult to prove with SMT solvers because of the nonlinear terms but it is proved with Coq.13 In this way,
a proof task involving nonlinear term is done manually. Likewise, all of the unproved VCs are discharged with four
additional lemmas and finally the soundness of multiply is proved. Overall, Alt-Ergo takes 243s to discharge the 26
VCs. Z3 is able to discharge four of them.

  10 The variable result is a built-in variable that represents the resulting value r (Definition 2) of the function under verification.
  11 In a Coq proof context, FP numbers are formalized by real numbers with additional data; vocabularies for intervals and FP numbers are defined

and characterized based on reals and integers. For instance, rewriting a context by applying a lemma on real numbers requires to unfold the
definitions of the vocabularies used in the context, which additionally requires a number of rewritings.
  12 Each unproved VC corresponds to the third branch shown in Figure 2 and either Q or Q , respectively.
                                                                                        V      S
  13 It is simply proved by the tactic “auto with real.”


                                                                           8
1     function min2 (x y: Float64.t) : Float64.t
2     = if x .< y then x else if is_not_nan y then y else x
3

4     function min4 (w x y z: Float64.t) : Float64.t = min2 w (min2 x (min2 y z))
5

6     lemma min4_feq: forall w x y z [min4 w x y z].
7       is_not_nan w \/ is_not_nan x \/ is_not_nan y \/ is_not_nan z ->
8         min4 x y z w .= w \/ min4 x y z w .= x \/ min4 x y z w .= y \/ min4 x y z w .= z
9

10    lemma min4_fle: forall w x y z [min4 w x y z].
11      (is_not_nan w -> min4 w x y z .<= w) /\ (is_not_nan x -> min4 w x y z .<= x) /\
12      (is_not_nan y -> min4 w x y z .<= y) /\ (is_not_nan z -> min4 w x y z .<= z)
13

14    lemma min4_feq_w: forall w x y z [min4 w x y z].
15      is_not_nan w /\ (w .<= x \/ is_nan x) /\ (w .<= y \/ is_nan y) /\ (w .<= z \/ is_nan z) ->
16        min4 w x y z .= w
17

18    (* lemmas min4_feq_(x|y|z) are omitted *)


                                      Figure 3: Specification of the min2 and min4 functions.


 7. Tightness of Multiplication

     As a second round of the verification, we verify the tightness QT of the multiply function. The postcondition
 states that results are the hull of the candidate bounds, i.e., rounded values of x × y, x × y, x × y and x × y. However,
 annotation of QT is not straightforward due to the complicated comparison of FP numbers that can be the special
 value NaN. This section describes comparison functions for our purpose (Section 7.1), how we annotate QT into the
 code in Figure 2 (Section 7.2) and a proof process (Section 7.3).

 7.1. Comparison of Four FP Numbers
     To specify the postcondition QT , we introduce the functions min4 and max4, which correspond to (the first cases
 of) the min and max operations in Theorem 1; these functions take the four candidate bounds and evaluate to the
 minimum/maximum of them while ignoring NaN; they evaluate to NaN when all the arguments are NaN. Specification
 of min4 is shown in Figure 3, which is actually described in the Float64Ex module; max4 is specified in the same
 way. First, the min2 function that compares two FP numbers is specified (Lines 1–2). min2 ignores NaN given as
 an argument so that the expression min2 x y evaluates to x when y evaluates to NaN. Second, the min4 function
 is simply specified with min2 (Line 4). To support deductions when min4 is used, we also specify six lemmas
 including min4_feq (Lines 6–8), min4_fle (Lines 10–12) and min4_feq_w (Lines 14–16) in Figure 3. The first
 two lemmas state the relations between the value of min4 and the arguments that are not NaN; they are respectively
 proved by Alt-Ergo in 7s and 0.5s. The last four lemmas state possible resulting values of min4 expressions, which
 are equivalent to one of the arguments w, x, y and z; these four lemmas are respectively proved by Alt-Ergo in 0.4s.
 The descriptions “[min4 w x y z]” specify the trigger of a lemma, which enforces to assume the lemma when a
 min4 predicate becomes true.

 7.2. Specification of Tightness
     Before annotating QT , we specify the conditions for the second cases of Equation (2) in Theorem 1, which hold
 when the four candidate bounds become NaN; these cases only happen in multiplication. The condition for min
 is specified as a predicate in the IntervalMul module as follows (the condition for max is specified likewise as
 mul_nan_case_sup).
      predicate mul_nan_case_inf (x y: interval) =
        is_nan (mul_down x.inf y.inf) /\ is_nan (mul_down x.inf y.sup) /\
        is_nan (mul_down x.sup y.inf) /\ is_nan (mul_down x.sup y.sup)
                                                                9
   Then, the pre- and postconditions PV and QT are specified as follows.
     requires { valid x /\ valid y } (* P_V *)
     ensures { not mul_nan_case_inf x y ->
       result.inf .= min4
         (mul_down x.inf y.inf) (mul_down x.inf y.sup)
         (mul_down x.sup y.inf) (mul_down x.sup y.sup)} (* Q_T lb *)
     ensures { not mul_nan_case_sup x y ->
       result.sup .= max4
         (mul_up x.inf y.inf) (mul_up x.inf y.sup)
         (mul_up x.sup y.inf) (mul_up x.sup y.sup) } (* Q_T ub *)
     ensures { mul_nan_case_inf x y /\ mul_nan_case_sup x y ->
       is_zero result.inf /\ is_zero result.sup } (* Q_T NaN case *)
Here, QT is specified in three parts. The first and second parts describe the first cases of Equation (2) using the min4
and max4 functions, each of which specifies the lower or upper bound portion of QT . The third part describes the
second cases of Equation (2) in conjunction because they only happen at the same time.

7.3. Proof
    The first and second postconditions are transformed into 26 VCs (with three split operations) and Alt-Ergo dis-
charges 22 of them; 4 VCs are left unproved after 10min. The third postcondition is transformed into a VC and
discharged by Alt-Ergo in 0.5s.
    After investigation of the remaining VCs, we have found that the following lemma helps Alt-Ergo to prove the
VCs generated from the first postcondition.
     lemma mul_down_positive_finite: forall x y [mul_down x y].
       is_positive (mul_down x y) /\ t’isFinite (mul_down x y) ->
         round RTN (t’real zeroF) <= round RTN (t’real x * t’real y)
The lemma details the relation between the lower bound of the result and zero. The premise extracts the unproved
two branches, each of which corresponds to a remaining VC; for example, one of the VCs corresponds to the third
branch in Figure 2, where x.inf ≥ 0 and y.inf ≥ 0 hold and the lower bound of the result is computed as
mul_down x.inf y.inf. We presume that applying round explicitly on both sides of the consequent inequality
facilitates unifying it with expressions specified in the ieee_float module and thus further deductions are invoked.
Another lemma mul_up_negative_finite is specified likewise for the second postcondition. In our experiment
with Alt-Ergo, the two lemmas are proved in 0.2s and the 26 VCs generated from the target code are proved in 308s.

8. Implementation and Experiments

    This section summarizes how the four operators have been specified (Section 8.1) and reports the verification result
(Section 8.2). Section 8.3 describes how we extracted an executable code from the specification. The file containing
the specifications and the extracted code is available at https://dsksh.github.io/vint-jcam2020.zip.

8.1. Specification
    Each operator was implemented as a WhyML function (see Appendix B for some details). The number of branches
in each function is shown in the second column of Table 2. Each function was annotated with the conditions PV ,
QV , QS and QT (the code for division was also annotated with QZ ). Since the “NaN case” described in Section 7.2
only happened in multiplication, QT was translated as two postconditions (“Q_T lb” and “Q_T ub” without precon-
ditioning) for the other three operators. In the experiment, we identified that additional lemmas were necessary for
the verification (the numbers of such lemmas are shown in the third column of Table 2). First, two variations of the
lemma in Section 7.3 were needed to verify QT for each operator code. Second, the subtraction code was annotated
with an assert formula to detail a property of the resulting value. Third, the multiplication and division codes were
                                                          10
                                                Table 2: Experimental results.
                                                  No split              Split full       Split optimal
                   Op.    # Br’s    # Lm’s    # VCs     Time         # VCs      Time    # VCs Time
                    +        1         2        3       36.4s          8        25.0s      6      24.7s
                    −        1         2        3       63.0s          10       47.2s      8      47.0s
                    ×       13       2+4        3        140s         100       508s       3       140s
                    ÷        7       6+7        7     TO (1)           33     TO (4)      15       578s


also annotated with four and seven lemmas, respectively, which were the variations of the lemma in Section 6.2; here,
the seven lemmas for division include the four lemmas for multiplication. There were 19 lemmas specified in total.
Other than the operator code, two WhyML modules, Float64Ex and Interval were prepared, which contained 30
and three lemmas about FP numbers and intervals, respectively.

8.2. Statistical Data
    We performed an experiment to verify the implementation of four operators and all of them were successfully
verified. The experiments (including the running examples) were operated using a 2.2GHz Intel Xeon E5-2650v4
processor with 128GB of RAM. The following tools were used: Why3 1.1.0, Alt-Ergo 2.2.0, Coq 8.8.0 and Z3 4.7.1.
The memory used was limited to 4GB and the time to 10min for each VC proof.
    Why3’s split strategy allows splitting VCs in several degrees. Therefore, the verification was performed with three
settings: Without using the split strategy (“No split”); with splitting VCs as many times as possible (“Split full”); with
an optimal number of splittings that requires minimum CPU time (“Split optimal”). Note that splitting a VC does not
always result in VCs that are discharged by SMT solvers more efficiently than the original.
    Herein, we present the experimental results in Table 2. The first three columns represent the target operator
(“Op.”), the number of branches (“# Br’s”) and the number of additional lemmas (“# Lm’s”). The data “m+n” indicates
that m lemmas were discharged with SMT solvers and n lemmas were proved with Coq (only the VCs generated from
the former are taken into account in the following columns). The following columns are separated for each of the
settings described above; for each section, the number of generated VCs (“# VCs”) and the total execution time by
Alt-Ergo (“Time”) are shown. “TO (n)” (for “Time Out”) means that the proofs for n VCs did not finish within 10min.
Note that the verification of the division code succeeded only with the “Split optimal” setting.
    Additionally, 33 lemmas in the Float64Ex and Interval modules were discharged by Alt-Ergo in 32.6s in total.
We also tried to discharge the “Split full” VCs with Z3, which was less efficient in our experiment; for each operator,
1/8, 1/10, 48/100 and 2/33 VCs were proved, respectively, and the rest resulted in timeout.

8.3. Extraction of Executable Code
    Why3 provides an extract function that generates an executable code from a WhyML code. Using this function,
we extracted an OCaml code that implements the interval type and the four operators. The extraction of numerical
programs with Why3 required additional implementations. First, we prepared an OCaml module for FP arithmetic
operations with rounding mode control. We implemented the rounding operators in C, which were then interfaced
with OCaml functions of the dedicated Round module. Second, we extended Why3’s extract function to support
the Float64.t type and related constants/functions. For this purpose, we prepared a driver file that defines various
translation rules.

9. Related Work

    Ayad and Marché [14] reported a case study on verifying an interval multiplication code. They used Frama-C,
which is a verification platform like Why3 equipped with SMT solvers, and verified the soundness QS of a variant of
our code. In this paper, we go further by considering the tightness QT .
    For generic FP computation, a number of verified programs have been reported. A notable implementation is
CRlibm [15], which aims at replacing the mathematical library of C. Elementary functions of CRlibm were formally
verified yet preserve the efficiency of the computation. The correctness was proved by analyzing the bounds of
                                                             11
numerical errors by hand or using the Gappa tool [16]. CRlibm differs from our verified code in two aspects: First, the
properties and the target programs are different; in CRlibm, it is verified that computation results are rounded values
in the prescribed direction for the elementary functions such as logarithm functions. Second, CRlibm is implemented
in C and executable but our code is not; instead, we extract an executable OCaml code (Section 8.3).
    Verification results for other numerical programs/algorithms have been reported [17, 6, 18], which used tools in-
cluding Frama-C, SMT solvers, Gappa and Coq (with Flocq [19]). They targeted computations of certain expressions
in reals, which differed from our subject: operations on FP intervals. In the verification, they aimed at certifying
rounding error bounds of numerical computations, as in the verification of CRlibm. On the other hand, our target code
outputs intervals that should enclose possible errors; then, we verify the correctness of the code. The verification tool
Frama-C is able to target C++ programs (with the C++ plugin). Verification of our target program with Frama-C will
be a future work as different tools might require different efforts to accomplish a verification.
    Gappa [16] is a theorem prover for (specific forms of) VCs about real numbers which may involve rounding
operators. It has been shown practical for proving rounding error bounds as mentioned above [15, 17, 6]. Gappa can
be applied to our VCs but how to encode them in a way solvable with Gappa is not straightforward; for example, it is
unclear how to handle user-defined types (e.g. interval) and the special FP values ±∞ and NaN since Gappa does
not support them natively.

10. Conclusion and Future Work

    A code for four interval operations, verified with Why3, has been presented. We implemented the target code with
WhyML and annotated with properties validity, soundness and tightness; then, we proved the correctness by discharging
all of the generated VCs by Alt-Ergo and Coq. The tightness was specified in an indirect way with the min4/max4
functions; we verified that each bound of a result coincides either of the extremum computed with the bounds of
the inputs, or zero. We believe interval arithmetic code is an appealing application for program verification as its
correctness matters and as the provers of this domain are developed actively.
    In the verification, several strategies were utilized, e.g., specification of auxiliary lemmas that help Alt-Ergo, and
delegation of reasoning on nonlinear terms to the interactive proof with Coq. Some lemmas are not specific to interval
arithmetic; so, they can be reused by automated provers in other applications. Many of the VCs were proved in a
combined automated and interactive manner. This approach is powerful as VCs tend to become complicated, while
often involving nonlinear terms. In principle, it can handle arbitrary VCs on background theories of the tools.
    As a future work, we plan to verify other interval computations, such as other arithmetic implementations, elemen-
tary functions, and application programs. We aim to schematize useful strategies for the verification of this domain.
Another line of work is to design and integrate a set of axioms for interval analysis into a prover like Alt-Ergo [20]
for reasoning about statements on interval arithmetic.


Acknowledgements

   The authors thank Masahide Kashiwagi who developed the kv library and the developers of the verification tools
we utilized. We also thank Guillaume Melquiond for suggesting us the use of lemmas on reals in the early stage.
We are grateful for the many valuable comments of the peer reviewers. This work was partially funded by JSPS
(KAKENHI 18K11240 and 18H03223).

References
 [1] R. E. Moore, Interval Analysis, Prentice-Hall, 1966.
 [2] A. Neumaier, Interval Methods for Systems of Equations, Cambridge University Press, 1990.
 [3] M. Kashiwagi, The kv Interval Arithmetic Library (version 0.4.43) (2017).
     URL http://verifiedby.me/kv/index-e.html
 [4] F. Bobot, J.-C. Filliâtre, C. Marché, G. Melquiond, A. Paskevich, The Why3 Platform (version 1.1.0) (2017).
     URL http://why3.lri.fr/
 [5] F. Bobot, J.-C. Filliâtre, C. Marché, A. Paskevich, Why3 : Shepherd Your Herd of Provers, in: International Workshop on Intermediate
     Verification Languages (BOOGIE), 2011, pp. 53–64.


                                                                   12
 [6] S. Boldo, F. Clément, J.-C. Filliâtre, M. Mayero, G. Melquiond, P. Weis, Wave Equation Numerical Resolution : a Comprehensive Mechanized
     Proof of a C Program, Journal of Automated Reasoning 50 (4) (2013) 423–456.
 [7] F. Bobot, S. Conchon, E. Contejean, M. Iguernelala, S. Lescuyer, A. Mebsout, The Alt-Ergo Theorem Prover (version 2.2.0) (2017).
     URL https://alt-ergo.ocamlpro.com/
 [8] IEEE, 1788-2015 – IEEE Standard for Interval Arithmetic, 2015. doi:10.1109/IEEESTD.2015.7140721.
 [9] IEEE, 754-2008 – IEEE Standard for Floating-Point Arithmetic, 2008.
[10] M. Brain, C. Tinelli, P. Ruemmer, T. Wahl, An Automatable Formal Semantics for IEEE-754 Floating-Point Arithmetic, in: IEEE Symposium
     on Computer Arithmetic (ARITH), 2015, pp. 160–167. doi:10.1109/ARITH.2015.26 .
[11] J. D. Pryce, G. F. Corliss, Interval arithmetic with containment sets, Computing 78 (3) (2006) 251–276.
     doi:10.1007/s00607-006-0180-4.
[12] S. M. Rump, T. Ogita, Y. Morikura, S. Oishi, Interval arithmetic with fixed rounding mode, Nonlinear Theory and Its Applications, IEICE
     7 (3) (2016) 362–373. doi:10.1587/nolta.7.362.
     URL https://www.jstage.jst.go.jp/article/nolta/7/3/7_362/_article
[13] F. Goualard, Fast and Correct SIMD Algorithms for Interval Arithmetic, in: 9th International Workshop on State-of-the-Art in Scientific and
     Parallel Computing (PARA), 2008, pp. 6126–6127.
[14] A. Ayad, C. Marché, Multi-prover verification of floating-point programs, in: IJCAR, LNAI 6173, 2010, pp. 127–141.
[15] C. Daramy-Loirat, D. Defour, F. De Dinechin, M. Gallet, N. Gast, C. Quirin Lauter, J.-M. Muller, CRlibm – A library of correctly rounded
     elementary functions in double-precision (version 1.0beta4) (2016).
[16] M. Daumas, G. Melquiond, Certification of bounds on expressions involving rounded operators, ACM Transactions on Mathematical Soft-
     ware 37 (1) (2010) 1–20. arXiv:0701186, doi:10.1145/1644001.1644003.
     URL http://gappa.gforge.inria.fr/
[17] S. Boldo, C. Marché, Formal Verification of Numerical Programs: From C Annotated Programs to Mechanical Proofs, Mathematics in
     Computer Science 5 (4) (2011) 377–393. doi:10.1007/s11786-011-0099-9.
[18] P. Roux, Formal Proofs of Rounding Error Bounds, Journal of Automated Reasoning 57 (2) (2016) 135–156.
[19] S. Boldo, G. Melquiond, Flocq: A unified library for proving floating-point algorithms in Coq, in: IEEE Symposium on Computer Arithmetic
     (ARITH), 2011, pp. 243–252. doi:10.1109/ARITH.2011.40.
     URL http://flocq.gforge.inria.fr/
[20] S. Conchon, M. Iguernlala, K. Ji, G. Melquiond, A. Fumex, A Three-tier Strategy for Reasoning about Floating-Point Numbers in SMT, in:
     CAV, LNCS 10427, 2017, pp. 419–435.
[21] M. Kashiwagi, “Tanten ni mugendai wo motsu kukan enzan matome” (A summary of interval arithmetic with infinity bounds, in Japanese)
     (2015).
     URL http://verifiedby.me/kv/interval/table3.pdf


Appendix A. Proof of Theorem 1

    We check the tightness of the right-hand side (rhs) for the following two cases: (i) Except when all of the computa-
tions with the interval bounds become NaN, the tightness is obvious since the bounds of the rhs are the rounded values
of the operation results, i.e., the hull of some theoretical values. (ii) For the case when all boundary computations
result in NaN, which is evaluated to 0 with the second case of (2), we confirm that it only happens in the multiplication
and it results in a correct interval:
   +) The extremum bounds are always computed as [▽(x + y), △(x + y)]. Here, additions ±∞ + ∓∞ that result in NaN
      never happen; so, the second cases of (2) do not apply.
   −) The rhs is always computed as [▽(x − y), △(x − y)]. Neither subtractions ±∞ − ±∞ that result in NaN nor the
      second cases of (2) happen.
   ×) The computation results of the rhs are classified as follows:

                                          y < 0, y ≤ 0                y < 0, y > 0               y ≥ 0, y > 0           y=y=0
                   x < 0, x ≤ 0       [▽(x × y), △(x × y)]       [▽(x × y), △(x × y)]       [▽(x × y), △(x × y)]        [0, 0] (**)
                   x < 0, x > 0       [▽(x × y), △(x × y)]               (*)                [▽(x × y), △(x × y)]        [0, 0] (**)
                   x ≥ 0, x > 0       [▽(x × y), △(x × y)]       [▽(x × y), △(x × y)]       [▽(x × y), △(x × y)]        [0, 0] (**)
                    x=x=0                 [0, 0] (**)                [0, 0] (**)                [0, 0] (**)               [0, 0]

       The cell (*) is computed as [min{▽(x × y), ▽(x × y)}, max{△(x × y), △(x × y)}]. Note that the multiplications of
       0 and ±∞ result in NaN. These combinations never happen in the cells not marked with (**). For the cells
       marked with (**), we compute [0, 0] as ∀r ∈ R, 0 × r = 0. When multiplying [0, 0] and half-bounded intervals,
       [0, 0] is computed with the first cases of (2). When multiplying [0, 0] and [−∞, +∞], [0, 0] is computed with
       the second cases.

                                                                      13
  ÷) The computation results of the rhs are classified as follows:

                                                         y<0                    y>0
                                     x<0          [▽(x ÷ y), △(x ÷ y)]   [▽(x ÷ y), △(x ÷ y)]
                                  x ≤ 0, x ≥ 0    [▽(x ÷ y), △(x ÷ y)]   [▽(x ÷ y), △(x ÷ y)]
                                     x>0          [▽(x ÷ y), △(x ÷ y)]   [▽(x ÷ y), △(x ÷ y)]

      The divisions ±∞ ÷ ±∞ that result in NaN never happen in all the cells; so, the second cases do not apply.
   Almost identical analysis to the above is described in [21], in which the cells (**) of the multiplication table are
analyzed differently.

Appendix B. Specification of Subtraction and Division

     The verification processes for other operations are similar to that for the multiplication. Some notable annotations
made to the subtraction and division operators are described below.
     Specification of the subtraction operator is shown in Figure B.4. In the specification of QT , the precondition
mul_nan_case is omitted since it is not necessary; if the precondition was violated, the result would be [NaN, NaN],
which is an invalid interval; it is verified with the postcondition QV that it will not happen. At Lines 12–13, two
properties on the lower bound of the result and the argument intervals are annotated; the properties are introduced
as premises in the VCs for the postconditions; they accelerated the proof process of Alt-Ergo in our experiment. As
a side note, similar assertions were not annotated to the addition operator, since it was verified automatically and
efficiently without them.
     Specification of the division operator is shown in Figure B.5. Line 9 raises the Division_by_zero exception and
it is verified with the postcondition QZ at Line 3 that it is raised properly.




                                                           14
1    let subtraction (x y: interval) : interval
2      requires { valid x /\ valid y }
3      ensures { valid result }
4      ensures { forall u v. real_in u x /\ real_in v y -> real_in (u - v) result }
5      ensures { result.inf .= min4
6          (sub_down x.inf y.inf) (sub_down x.inf y.sup)
7          (sub_down x.sup y.inf) (sub_down x.sup y.sup) }
8      ensures { result.sup .= max4
9          (sub_up x.inf y.inf) (sub_up x.inf y.sup)
10         (sub_up x.sup y.inf) (sub_up x.sup y.sup) }
11   = let r = { inf = sub_down x.inf y.sup; sup = sub_up x.sup y.inf } in
12     assert { r.inf .<= sub_down x.inf y.inf \/ is_nan (sub_down x.inf y.inf) };
13     assert { r.inf .<= sub_down x.sup y.sup \/ is_nan (sub_down x.sup y.sup) };
14     r


                                      Figure B.4: Code for subtraction of intervals.


1    let division (x y: interval) : interval
2      (* pre- and postconditions are omitted *)
3      raises { Division_by_zero -> real_in 0. y }
4    = if y.inf .> zeroF then
5        (* three branches are omitted *)
6      else if y.sup .< zeroF then
7        (* three branches are omitted *)
8      else
9        raise Division_by_zero


                           Figure B.5: Code snippet for division of intervals: Exceptional case.




                                                           15
