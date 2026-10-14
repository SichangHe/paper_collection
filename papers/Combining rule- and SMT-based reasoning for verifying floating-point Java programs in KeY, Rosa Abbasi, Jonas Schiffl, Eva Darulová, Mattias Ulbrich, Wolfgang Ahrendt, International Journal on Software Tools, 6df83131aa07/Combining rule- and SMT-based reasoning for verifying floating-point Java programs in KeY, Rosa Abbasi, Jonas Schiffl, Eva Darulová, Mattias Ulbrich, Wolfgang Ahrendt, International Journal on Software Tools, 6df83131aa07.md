International Journal on Software Tools for Technology Transfer (2023) 25:185–204
https://doi.org/10.1007/s10009-022-00691-x

    GENERAL

    Special Issue: TACAS 2021



Combining rule- and SMT-based reasoning for verifying floating-point
Java programs in KeY
Rosa Abbasi1          · Jonas Schiﬄ2       · Eva Darulova1,3         · Mattias Ulbrich2      · Wolfgang Ahrendt4

Accepted: 7 November 2022 / Published online: 8 March 2023
© The Author(s) 2023


Abstract
Deductive verification has been successful in verifying interesting properties of real-world programs. One notable gap is
the limited support for floating-point reasoning. This is unfortunate, as floating-point arithmetic is particularly unintuitive
to reason about due to rounding as well as the presence of the special values infinity and ‘Not a Number’ (NaN). In this
article, we present the first floating-point support in a deductive verification tool for the Java programming language. Our
support in the KeY verifier handles floating-point arithmetics, transcendental functions, and potentially rounding-type casts.
We achieve this with a combination of delegation to external SMT solvers on the one hand, and KeY-internal, rule-based
reasoning on the other hand, exploiting the complementary strengths of both worlds. We evaluate this integration on new
benchmarks and show that this approach is powerful enough to prove the absence of floating-point special values—often a
prerequisite for correct programs—as well as functional properties, for realistic benchmarks.

Keywords Deductive verification · Floating-point arithmetic · Transcendental functions


1 Introduction                                                               postconditions, from which verification conditions (VCs)
                                                                             are automatically generated. These are then either proven
Deductive verification has been successful in providing                      directly by the verifier itself, or discharged with exter-
functional verification for programs written in popular pro-                 nal tools such as automated Satisfiability Modulo Theories
gramming languages such as Java [2,21,40,48], Python [27],                   (SMT) solvers or interactive proof assistants.
Rust [4], C [23,53], and Ada [17,49]. Deductive verifiers                        While deductive verifiers fully implement many sophisti-
allow a user to annotate methods in a program with pre- and                  cated data representations (including heap data structures,
                                                                             objects, and ownership), support for floating-point num-
                                                                             bers remains rather limited—solely Frama-C and SPARK
B Rosa Abbasi
      rosaabbasi@mpi-sws.org                                                 offer automated support for floating-point arithmetic in C
                                                                             and Ada [30]. This state of affairs is at least partially a
      Jonas Schiffl
      jonas.schiffl@kit.edu                                                  result of previous limitations in floating-point support in
                                                                             SMT solvers. Consequently, deductive verification has been
      Eva Darulova
      eva@mpi-sws.org                                                        used for floating-point programs only by experts with con-
                                                                             siderable manual effort [13,30]. This is unfortunate as it
      Mattias Ulbrich
      ulbrich@kit.edu                                                        makes deductive verification unavailable for a large num-
                                                                             ber of programs across many domains including embedded
      Wolfgang Ahrendt
      ahrendt@chalmers.se                                                    systems, machine learning, and scientific computing. With
                                                                             the increasing need for parallelization in code, scientific
1     MPI-SWS, Kaiserslautern and Saarbrücken, Saarbrücken,                  computing specifically has recently experienced algorithmic
      Germany                                                                challenges for which formal methods may contribute to a
2     Karlsruhe Institute of Technology, Karlsruhe, Germany                  solution [8,56].
3     Uppsala University, Uppsala , Sweden                                       One of the main challenges of floating-point arithmetic is
4     Chalmers University of Technology, Gothenburg, Sweden                  its unintuitive behavior and the special values that the IEEE


                                                                                                                                123
186                                                                                                                     R. Abbasi et al.


754 standard [38] introduces. For instance, an overflow or a          We exploit both KeY’s symbolic execution and exter-
division by zero results in the special value (positive or neg-    nal SMT support. On the one hand, we handle arithmetic
ative) infinity, and not a runtime exception. Similarly, invalid   operations by relying on a combination of KeY’s symbolic
operations like sqrt(-1.0) result in a Not a Number (NaN)          execution to handle the heap and SMT-based decision pro-
value. These special values are problematic as seemingly           cedures to handle the floating-point part of the VCs. On the
straightforward identities do not hold (x == x or x * 0.0 ==       other hand, we support transcendental functions via axiom-
0.0). In addition, every operation on floating-point numbers       atization in the KeY prover itself.
potentially involves rounding, which compromises familiar             Transcendental functions such as sine are a common fea-
rules like associativity and distributivity. Hence, reasoning      ture in engineering applications, but are not supported by
support for writing correct floating-point programs is indis-      floating-point decision procedures. We explore two ways of
pensable.                                                          supporting them soundly but approximately, by encoding
    Abstract interpretation-based tools can prove the absence      them as axiomatized uninterpreted function symbols once
of runtime errors and special values [18,42] and bound             directly in the SMT queries, and once in additional calcu-
roundoff errors due to floating-point’s finite precision [9,       lus rules in KeY. Our evaluation shows that even though
19,24,35,58]. SMT decision procedures [15] or SAT-based            such reasoning is approximate, it is nonetheless sufficient
model-checking [22,56], on the other hand, can prove intri-        to prove the absence of special values in many interesting
cate properties requiring bit-precise reasoning. However,          programs.
these techniques and tools largely support only purely                We evaluate KeY’s floating-point support on a num-
floating-point programs or program snippets, or analyze pro-       ber of real-world floating-point Java programs, verifying
grams only up to a predefined depth of the call stack. Gen-        the absence of special values as well as functional cor-
eral reasoning about real-world object-oriented programs,          rectness, including programs with loops (with the help of
however, requires support for more than floating-point arith-      loop invariants). Our benchmark set allows us to evaluate
metic. Many realistic programs mix floating-point types            recent progress in SMT floating-point support in Z3 [26],
with other primitive types, like integers, including (implicit)    CVC4 [6] and MathSAT [20] on yet unseen benchmarks. For
type casts and moreover use object-oriented concepts, like         instance, we observe that quantifiers are challenging even if
the (unbounded) object heap. This necessitates different           they do not affect satisfiability of SMT queries. Our bench-
analyses which need to be integrated with floating-point rea-      marks are openly available, and we expect our insights to be
soning.                                                            useful for further solver development.
    Handling floating-points in a deductive verifier has unique    Contributions In summary, we make the following contribu-
advantages. First, the deductive verification approach already     tions:
comes with the infrastructure for reasoning about complex
control and data structures (like exception handling and               – we implement and evaluate the first automated deductive
heaps). Second, it allows one to flexibly combine the ver-               verification of floating-point Java programs by combin-
ifier’s symbolic execution reasoning with external decision              ing the strength of rule-based and SMT-based deduction;
procedures. Third, depending on the theory support, the ver-           – we develop novel automated support for reasoning about
ifier or external solver may also generate counterexamples               transcendental functions in a deductive verifier;
of a property and thus help program debugging—something                – we add support for reasoning about (potentially round-
an abstract interpretation-based approach fundamentally                  ing) type conversions;
cannot provide.                                                        – we collect a new set of challenging real-world floating-
    We report on adding floating-point support to the KeY                point benchmarks in Java;1
deductive verifier, providing the first automated deductive            – we compare different SMT solvers for discharging floating-
floating-point support for the Java programming language.                point VCs on this new set of benchmarks.
Among others, we verify the absence of the special val-
ues infinity and NaN. While those are helpful in particular            This article extends a previous conference paper [1]
circumstances (like carefully designed implementations of          by more floating-point arithmetic background, the presen-
numeric analysis algorithms), for most applications they           tation of all rules for transcendental functions and sqrt,
indicate an error. Hence, showing their absence is a pre-          new rules—and accordingly experiments—for (potentially
requisite for further (functional) reasoning. Moreover, our        rounding) casts between integers and floats, new experi-
extension allows to express and discharge functional prop-         ments on the verification of floating-point loop invariants,
erties relating pre- and poststates, including bounds on           new experiments on the sensitivity of SMT solvers to numer-
roundoff errors and bounds on differences between two sim-
ilar floating-point programs, which we also demonstrate.
                                                                   1   Available at https://zenodo.org/record/6572961#%23.Yot0hJNBy3I


123
Combining rule- and SMT-based reasoning . . .                                                                                187


ous problem modifications, and extended reporting of the             In addition to the application of taclets, KeY also sup-
experiments presented in [1].                                     ports the translation of open goals into the common SMT
                                                                  input format SMT-LIB [7] and the calling of an external
                                                                  SMT solver. For specific theories, SMT solvers can be much
2 Background                                                      more efficient than KeY’s own, rule-based reasoning, while
                                                                  other goals are more effectively dealt with by KeY rather
2.1 Introduction to KeY                                           than SMT solvers. KeY therefore allows to discharge some
                                                                  goals with SMT solvers, and others with KeY’s own, rule-
KeY [2] is a platform for deductive verification of Java pro-     based proof engine.
grams, working at a source code level. The input is a Java
program annotated in the Java Modeling Language (JML)             2.2 Floating-point arithmetic in Java
[44], encouraging a Design by Contract ([45,50]) approach
to software development. The user specifies the expected          Among the primitive (i.e., non-reference) types of Java,
behavior of Java classes with class invariants that the pro-      there are two which represent floating-point numbers, namely
gram has to maintain at critical points. Methods are specified    float and double. They are associated with the 32-bit
with method contracts, consisting mainly of pre- and post-        and 64-bit format, respectively, as specified in the IEEE
conditions, with the understanding that if the precondition       754 Standard for Floating-Point Arithmetic. More precisely,
holds when the method is called, the postcondition has to         Java implements a subset of that standard. In the following,
hold after the method returns.                                    we summarize some central characteristics of Java floating-
   After loading an annotated program, KeY translates it to a     point numbers, loosely following Muller et.al. [52]. Most
formula in Java Dynamic Logic [2] (JavaDL), an instance of        of this is not specific to Java, but more generally applies to
Dynamic Logic [36] which enables logical reasoning about          IEEE 754. Note that the Java Virtual Machine (JVM) only
Java programs. Logical rules are provided for the translation     supports floating-point numbers with base 2, even if the Java
of programs into first-order logic, and for closing the result-   language syntax supports base 10 as well, in such a way that
ing goals, or proof obligations. KeY is semi-interactive in       parsing and input/output routines translate back and forth
that it allows manual rule application, while also offering       between the bases.
powerful built-in automation and macros.                              Each (base 2) floating-point number x (except the special
   The rules are written in KeY as taclets,                       values +∞, −∞, and NaN, see below) with precision p can
   calculus rule schemata, implementing rewrite rules. One        be represented as a triplet (s, m, e), such that x = (−1)s ∗
example taclet that rewrites any expression matching x + 0        m ∗ 2e , where s ∈ {0, 1} is the sign, m (called significand) is
to x is shown below:                                              a binary fixed-point number with one digit before the radix
                                                                  point and p − 1 digits after the radix point (note that 0 ≤
find    x +0                                                      m < 2), and e (exponent) is an integer such that emin ≤ e ≤
replace x                                                         emax . Java supports two floating-point formats (both in base
                                                                  2): float with p = 24, emin = −126, emax = 127 and
                                                                  double with p = 53, emin = −1022, emax = 1023.
   In general, taclets have the following form:
                                                                      Whenever the result of a computation cannot be exactly
                                                                  represented with the given precision, it is rounded. IEEE 754
find    tfind
                                                                  defines various rounding modes, of which Java only sup-
replace treplace
                                                                  ports round to nearest, ties to even. Rounding is exact, as if
add     ϕadd
                                                                  one would first compute the ideal real number, and round
show    ϕshow
                                                                  afterwards. Note that rounding may even occur when the
                                                                  exact mathematical result of a computation corresponds to
    It consists of a schematic find term tfind which has to       an integer number. The single precision type float has a
match an expression or formula in the current goal, and a         significand of 24 bits and can therefore not exactly represent
term treplace which replaces the matched expression or for-       all integers of the 32-bit type int. However, integers whose
mula. New formulas may be introduced as new assumptions           absolute value is smaller than 224 can be represented in an
onto the proof goal using add. If the rule has a side condition   exact way in the type float.
ϕshow that needs to be established, it can be optionally spec-        A number x could potentially be represented by differ-
ified using show that will open a new proof goal for ϕshow .      ent (s, m, e) triples. However, it has many computational
One of the clauses for add and replace may be empty or            advantages to restrict the floating-point numbers to a normal
omitted. The taclet language supports typed meta-variables        form. Therefore, m is always chosen such that 1 ≤ m < 2
and heuristics for KeY’s automation.                              wherever possible (these are called the normal numbers) and


                                                                                                                      123
188                                                                                                                            R. Abbasi et al.


0 ≤ m < 1 only were necessary (these are called the subnor-                  3 Floating-point support in KeY
mal numbers). Note that, for subnormal numbers, e = emin .
Also note that, for subnormal numbers, the relative round-                   3.1 Arithmetics
ing error can be much worse than for normal numbers. On
the other hand, the existence of subnormals guarantees the                   In order to be able to specify and verify programs con-
following equivalence: (x > y) ↔ (x − y > 0). With-                          taining floating-point numbers, we made several extensions
out subnormals, this would not hold, because the difference                  to the KeY tool. We added the float and double types
between two normal floating-point numbers can be smaller                     to the KeY type system, introduced functions and predi-
than any normal floating-point number.                                       cate symbols to formalize arithmetic operations (+, *, . . . ),
    The triple representation gives us two zeros, +0 and                     and comparisons (<, ==, . . . ) on floating-point expressions,
−0, represented by (0, 0, 0) and (1, 0, 0), respectively.2 The               and added cast operations among floating-point and integer
Boolean expressions +0.0==−0.0 and −0.0==+0.0 both                           types ((double), (float), (int)). The translation supports
return true. If the absolute value of the ideal result of a                  both code with and without the strictfp modifier. How-
computation is too small to be representable as a floating-                  ever, since the actual precision of non-strictfp operations
point number of the given format, the resulting floating point               is not known, the function symbols remain uninterpreted.
number is +0 or −0. In addition, there are three special val-                We assume that the strictfp modifier is set for all our
ues, +∞, −∞, and NaN (Not a Number). If the absolute                         benchmarks. We extended KeY’s parser to correctly handle
value of the ideal result of a computation is too big to be                  programs and annotations containing floating-point numbers
representable as a floating-point number of the given for-                   and added logic rules for translating floating-point expres-
mat, the result is +∞ or −∞. Also, division by zero will                     sions from Java or JML to JavaDL.
give an infinite result (e.g., 7.3/ + 0 = +∞).3 Comput-                         As an example, Listing 1 shows a JML specification of
ing further with infinity may give an infinite result (e.g.,                 our Rectangle benchmark that contains floating-point liter-
+∞ + +∞ = +∞), but may also result in the additional                         als and makes use of the fp_nan and fp_nice predicates.
‘error value’ NaN (e.g., +∞−+∞ = NaN). The predicates                        fp_nan states that a floating-point expression is NaN and
==, <, >, <=, >= return false as soon as one operand eval-                   fp_nice, states that a floating-point expression is neither
uates to NaN. The predicate != returns true as soon as one                   NaN nor infinity. The scale method contains two contracts
operand evaluates to NaN. In particular, NaN==NaN returns                    that are checked separately, ensuring that the class fields of
false, and NaN!=NaN returns true. Due to the presence of                     a scaled rectangle object are not NaN, considering different
infinities and NaN, floating-point operations do not throw                   preconditions. For the first contract, the SMT solver pro-
Java exceptions.4                                                            duces a counterexample. In the second, we bound inputs by
    By default, the Java virtual machine is allowed to make                  concrete ranges that we picked arbitrarily and get the valid
use of higher-precision formats provided by the hardware.                    result. In practice, such ranges would come from the context,
This can make computation more accurate, but it also leads                   e.g., from the kind of rectangles that appear in an applica-
to platform-dependent behavior. This can be avoided by                       tion, or from known ranges of sensor values.
using the strictfp modifier, ensuring that floating-point                       Concerning discharging the resulting proof obligations,
computations inside methods or classes with the strictfp                     there were two main ways to consider. One is to create
modifier comply to the precision defined in the IEEE                         a floating-point theory within KeY by adding axioms and
754 Standard, even for intermediate results. This modifier                   deduction rules, so that the desired properties can be proven
ensures portability. Additionally, one can set the Assume                    in KeY’s calculus. The other way is to translate the proof
strictfp option in KeY, meaning that all computations are                    obligations from JavaDL to SMT-LIB and call an external
assumed to be within the scope of a strictfp modifier, even                  SMT solver. While the KeY approach traditionally favors
if strictfp is not explicit in the code.                                     conducting proofs with KeY’s own, rule-based reasoning
                                                                             engine, we partially deviated from this way in order to har-
                                                                             ness the greater efficiency of SMT solvers when it comes to
2 More precisely, the second element of these tuples has one zero            the combinatorically heavy reasoning about floating-point
before the radix point, and p − 1 zeros after the radix point.               arithmetic. Our approach attempts to get the best of both
3 Note that 7.3/ + 0 and 7.3/ − 0 give different results, +∞ and −∞,         worlds by distinguishing between basic floating-point arith-
respectively, even if +0.0==−0.0 returns true.                               metic, i. e., elementary operations and comparisons, and
4  The notion of exceptions in the IEEE 754 Standard is not to be con-       more complex functions which do not have an SMT-LIB
fused with Java exceptions. IEEE 754 exceptions are rather ‘sticky           equivalent (e. g., the transcendental functions), or where
flags’ for overflow, underflow, and other problematic situations. They
                                                                             rule-based reasoning is more effective than SMT solvers
do not change the control flow and certainly are not objects. In this con-
text, we can also mention that IEEE 754 exceptions are not supported         currently are (see Sect. 3.2.2).
by Java.


123
Combining rule- and SMT-based reasoning . . .                                                                                189


                                                                  3.2 Transcendental functions
Listing 1 The Rectangle.scale benchmark
/*@ public normal_behavior
  @ requires \fp_nice(arg0.x) && \fp_nice(arg0.y)
                                                                  Floating-point decision procedures in SMT solvers success-
  @    && \fp_nice(arg1) && \fp_nice(arg2);                       fully handle programs consisting of arithmetic and square-
    @   ensures !\fp_nan(\result.x) && !\fp_nan(\result.y) &&     root operations. Many numerical real-world programs, how-
    @    !\fp_nan(\result.width) && !\fp_nan(\result.height);
                                                                  ever, include transcendental functions such as sin and cos.
    @ also
    @ public normal_behavior
                                                                  In Java programs, these functions are implemented as static
    @   requires -5.53 <= arg0.x && arg0.x <= -3.38 &&            library functions in the class java.lang.Math.
    @     -5.53 <= arg0.y && arg0.y <= -3.38 &&                      Unlike arithmetic operations, transcendental functions
    @      3.1 < arg0.width && arg0.width <= 3.7332 &&
                                                                  are much more loosely specified by the IEEE 754 Standard—
    @     3.0000001 < arg0.height && arg0.height <=4.0004 &&
    @     3.0003001 < arg1 && arg1 <= 4.0024 &&
                                                                  only an upper bound on the roundoff error is given. Libraries
    @     -6.4000003 < arg2 && arg2 <= 3.0001;                    are thus free to provide different implementations, and even
    @   ensures !\fp_nan(\result.x) && !\fp_nan(\result.y)&&      tighter error bounds. Exact reasoning in the same spirit as
    @     !\fp_nan(\result.width) &&!\fp_nan(\result.height);
                                                                  floating-point arithmetic would thus have to encode a spe-
  @*/
public Rectangle scale(Rectangle arg0,double arg1,double arg2){
                                                                  cific implementation. Given that these implementations are
    Area v1 = new Area(arg0);                                     highly optimized, this approach would be arguably com-
    AffineTransform v2 =                                          plex. We observe, however, that such exact reasoning about
        AffineTransform.getScaleInstance(arg1, arg2);
                                                                  transcendental functions is often not necessary and a sound
    Area v3 = v1.createTransformedArea(v2);
    Rectangle v4 = v3.getRectangle2D();
                                                                  approximate approach is sufficient and efficient.
    return v4;                                                       In this section, we introduce an axiomatic approach for
}                                                                 reasoning about programs containing transcendental func-
                                                                  tions. We observe that with the flexibility of deductive
                                                                  verification and KeY itself, we can instantiate it in two
                                                                  different ways. We encode transcendental functions as unin-
   Elementary operations and comparisons get translated           terpreted functions and axiomatize them in the SMT queries.
to the corresponding SMT-LIB functions. In SMT-LIB, all           Alternatively, we encode these axioms in KeY as logical
floating-point computations conform to the IEEE 754 Stan-         inference rules. In the following, we explain each of these
dard. Therefore, only Java programs with the strictfp             solutions in more detail and later we will evaluate them on a
modifier can be directly translated to SMT-LIB without loss       set of benchmarks.
of correctness.
   We developed a translation from KeY’s floating-point the-      3.2.1 Axiomatization in SMT
ory to SMT-LIB. In order to integrate it into KeY, we also
overhauled the existing translation from JavaDL to SMT-           We encode library functions as uninterpreted functions and
LIB to create a new, more modular framework, which now            include a set of axioms in the SMT-LIB translation for each
supports all the features of the original translation, e. g.,     method that is called in a benchmark. That is, we extended
heaps and integer arithmetic, but also floating-point expres-     KeY such that when a transcendental function appears in the
sions at the same time.                                           proof obligation, its declaration alongside all the axioms for
   Floating-point intricacies sometimes require extra cau-        that function is added to the translation.
tion. For example, there are two different notions of equal-         For the axiomatization of transcendentals, we did not add
ity for floats: bitwise equality and IEEE754 equality. Our        rules that expand to a definition or allow a repeated approx-
implementation ensures these are distinguished correctly          imation of the function value (like expansion into a Taylor
and that the specification language remains intuitive for a       series). Instead, we added a number of lemmata encoding
developer to use.                                                 interesting properties related to special values. For instance,
   Using the translation to SMT-LIB, we can specify and           the following axiom states that if the input to the sin func-
prove two classes of properties in KeY, the absence of spe-       tion is not a NaN or infinity, then the returned value of sin
cial values and functional properties. The absence of special     is between −1.0 and 1.0:
values is specified using the fp_nan and fp_infinite pred-
icates (or the fp_nice equivalent). Furthermore, one can
specify functional properties (including loop invariants) that
are expressible in floating-point arithmetic, e.g., one can
compare the result of a computation against the result of a
different program which is known to produce a good result
or a reference value.


                                                                                                                      123
190                                                                                                                        R. Abbasi et al.


(assert (forall ((a Float64)) (=>
  (and (not (fp.isNaN a)) (not (fp.isInfinite a)))
  (and (fp.leq (sinDouble a)
               (fp #b0 #b01111111111#b0000...000000))
       (fp.geq (sinDouble a)
               (fp #b1 #b01111111111#b0000...000000))))))


    Note that this implies that the result is not a NaN or infin-
ity. The other axioms are similar in spirit, so we do not list
them.
    These axioms are expressed as quantified floating-point
formulas and capture high-level properties of library func-
tions complying with the specifications in the IEEE 754
Standard. Clearly, since we do not have the actual imple-
mentations of these functions, we are not able to prove
arbitrary properties. However, such an axiomatization is            Fig. 1 List of added axioms to KeY for transcendental functions
often sufficient to check for (the absence of) special values,
i.e., NaN and infinity, as our experiments in Sect. 4.4 show.
                                                                    proof obligation can either be closed, i.e., proven, by KeY
                                                                    automatically, or be given to the SMT solver as before for
3.2.2 Taclets in KeY
                                                                    final solving. Currently, the set of axioms (in the SMT-
                                                                    LIB translation and as taclets in KeY) only contains axioms
Reasoning about quantified formulas in SMT is a long-
                                                                    for the transcendental functions occurring in our bench-
lasting challenge [32]. We have also observed in our exper-
                                                                    marks, namely sin, cos, and atan functions. So far we have
iments with only arithmetic operations (Sect. 4.3) that
                                                                    10 axioms; however, adding more axioms (also for further
SMT solvers struggle with quantifiers in combination with
                                                                    transcendentals like exponentiation or logarithm) is straight-
floating-point numbers. We have therefore implemented an
                                                                    forward.
alternative approach encoding the axioms not in the SMT
                                                                       The full set of axioms is listed in Fig. 1 (stated in natural
queries, but instead as deductive inference rules (called
                                                                    language for presentation purposes).
‘taclets’) in KeY.
   The rules encode the same logical information as the uni-
versally quantified assertions that we add in SMT-LIB (and          3.3 Interaction of floats with other primitive types
where we leave the choice of instantiations entirely to the
SMT/SAT solver). With our taclet approach, we instantiate           For the formal verification of Java programs with floats,
a quantifier (only) to one’s needs. For instance, the taclet that   there are often not only floating-point numbers that have to
corresponds to the SMT axiom mentioned in Sect. 3.2.1 is            be taken into consideration, but also heap data structures,
captured by the following taclet:                                   arrays, and primitive values of other data types than float
                                                                    or double. Our SMT translation in KeY does not only tar-
                                                                    get the floating-point theory, but encodes other aspects of
find sin(x)
                                                                    proof obligations into theories like linear integer arithmetic
add ¬fp_nan(x) ∧ ¬fp_infinite(x)
                                                                    for integers, or arrays representing heap data structures.
     → −1.0 ≤ sin(x) ≤ +1.0 ⇒
                                                                    In the evaluation, the state-of-the-art SMT solvers show
                                                                    their ability to reason about these theories when they occur
   We note that this is an incomplete treatment of the formal-      simultaneously within the same proof obligation. As long
ized operations. Considering only some and not all possible         as the different theories act on disjoint domains, this com-
quantifier instantiations buys us more closed proofs and            bined integrated translation works nicely in most cases. For
shorter running times in some cases. However, it may also           instance, programs using float arrays or class attributes of
lead to spurious counterexamples (false positives) reported         type double can be handled as long as floating-point values
by the SMT solver in other cases.                                   and other types are not arithmetically combined within an
   A heuristic strategy applies the rules automatically using       expression.
the occurrences of transcendentals as instantiation triggers.          However, there are relevant cases in which arithmetic
However, instantiating the axioms too eagerly consider-             expressions in Java programs have to contain both integer
ably increases the number of open goals, which is why we            and floating-point variables, their domains thus becoming
assume that the user selects the axioms to apply manually           entangled. It is, for instance, a legal Java expression to add
(and did so in the experiments). After the application, the         an integer value to a float value, yielding a float value.


123
Combining rule- and SMT-based reasoning . . .                                                                                        191


Such cases of intersecting value domains require special                 after floating-point addition ( f 1 +float f 2 = rnd(R( f 1 ) +R
attention.                                                               R( f 2 )) for floats f 1 , f 2 ) and when converting integers to
    We call float-representable those 32-bit int values which            floats ((float)i = rnd(R(i)) for an integer i).
can be represented in float without loss of precision. In                   With a, b as required by the theorem, we have
particular, all integers between −224 and 224 are float-                 R(rnd(R(a))) = R(a), R(rnd(b)) = R(b) and R(a +int
representable.5 According to the Java Language Specifica-                b) = R(a) +R R(b). Hence,
tion (JLS) [33], an implicit widening cast called numeric
promotion is applied when different primitive types are com-
bined in an arithmetic operation. The addition iv + fv of an                (float)(a +int b)
integer variable iv and a float variable fv is hence equiva-             = rnd(R(a +int b)) = rnd(R(a) +R R(b))
lent to the expression (float)iv + fv in which the numeric               = rnd(R(r nd(R(a)) +R R(r nd(R(b))))
promotion has been made explicit.
                                                                         = (float)a +float (float)b
    The cast operator connects the domains of the two prim-
itive types and maps integer values to floats by applying
the same rounding operation which is applied to the result                  Note that Theorem 1 does not require a + b to be float-
of arithmetic operations within floats. Since this family of             representable. Indeed, a + b may need to be rounded when
cast operators on primitive types is translated from JML into            casted to float on the left of the equation. At the same time,
JavaDL as uninterpreted functions, we can build a bridge                 the float addition on the right side of the equation may also
between the integer and floating-point domains by adding                 require rounding. The insight from the proof above is that
theorems/axioms about the numeric promotion to KeY in                    the IEEE standard and the JLS force the rounding on both
form of taclets.                                                         sides to be the same!
    In KeY, we can add knowledge about the casting operator                 Theorem 1 can also be formulated for subtraction and
in form of taclet rules to the verification engine: The new              multiplication (with essentially the same correctness argu-
taclets are implemented as conditional rewriting taclet rules            ments) instead of addition. A taclet that implements this
introducing new constraints on the cast operator ‘(float)’.              theorem for the float-representable numbers in the afore-
    A central property of float-representable integers is that           mentioned range is the following:
the cast operation can be inverted, captured by the following
taclet
                                                                         find    (float)(a + b)
find    (int)(float)i                                                    replace (float)a + (float)b
replace i                                                                show    −224 ≤ a ≤ 224 ∧ − 224 ≤ b ≤ 224
show    −224 ≤ i ≤ 224

 in KeY, formalising that casting an integer expression i first           Note that the taclet does not cover all float-representable
to a float and then back to an int is the identity if i stays            integers but only the interval in which all integers are float-
within the range of float-representable values.                          representable. In this range, the sum a + b cannot overflow.
    Since the JLS prescribes the same rounding mode for                  The taclet can also be formulated for subtraction. The taclet
float operations and numeric promotion, it does not matter,              for the case of multiplication must take this into considera-
for float-representable values, if they are first added and then         tion:
cast or the way around:
                                                                         find    (float)(a ∗ b)
Theorem 1 Let a, b be float-representable integer values
                                                                         replace (float)a ∗ (float)b
such that a + b does not int-overflow. Then, (float)(a +
b) = (float)a + (float)b.                                                show       − 224 ≤ a ≤ 224 ∧ − 224 ≤ b ≤ 224
                                                                                     ∧ − 231 ≤ a ∗ b < 231
Proof e introduce an auxiliary injection function R : float∪
int → R canonically mapping float and integer values to
their real-valued counterparts. The function rnd : R →                    Note that KeY internally operates on mathematical integers
float is the rounding function mapping real values to floats.            (instead of 32-bit integers) such that the overflow check can
According to the JLS, the same rounding function is used                 be implemented in this fashion.
                                                                            Another important rule for the cast operator is the con-
5                                                                        version of literals: any expression (float)c where c is a
  This interval is indeed the largest in which all integers are float-
representable. The value 224 + 1 requires a 25-bit significand to be     numerical integer literal can be rewritten to the correspond-
precisely represented, but float only has a precision of 24 bits.        ing numerical literal on the float side, like


                                                                                                                              123
192                                                                                                                  R. Abbasi et al.


                                                                  sqrt in this list, as we have observed that exact support
Listing 2 Adding up the values in an array of floats.
                                                                  can be expensive, so it may be advantageous to handle sqrt
/*@ public normal_behaviour
  @ requires (\forall int i; 0 <= i <a.length;
                                                                  axiomatically. We include benchmarks with loops and loop
    @                 1.f <= a[i] && a[i]<= 2.f);                 invariants used for the evaluation of the tool Pine [39], repre-
    @   requires a.length < 16 777 216; //== 224                  sented as Pine.*. Benchmarks Rectangle, Circuit, Matrix3,
    @   ensures (float)a.length <= \result &&                     Rotation and Pine.pendulum-approx are partially shown in
    @                \result <= (float)a.length* 2.f;
                                                                  Listings 1, 6, 3, 4 and 5 respectively.
  @*/
float sum(float[] a) {                                               Each benchmark also includes a JML contract that is to
        float sum = 0.0f;                                         be checked. For some methods, we specify two contracts
        int i = 0;                                                (marked by “(2)” in the first column of Table 1), each serv-
        /*@ loop_invariant 0 <= i && i <= a.length &&
                                                                  ing as an independent benchmark. The contracts for some
          @     (float)i <= sum && sum <= (float)i * 2.f;
          @ decreases a.length - i;                               of these benchmarks check that the methods do not return
          @ assignable \nothing;                                  a special value, i.e., infinity and/or NaN, the preconditions
          @*/                                                     being that the variables are not themselves special values
         while(i < a.length) {
                                                                  and possibly are bounded in a given range. For the Matrix,
              sum += a[i];
              i++;                                                FPLoop, Rotate and Pine.* benchmarks, we check a func-
         }                                                        tional property (see Sect. 4.3). The Pine.* benchmarks and
         return sum;                                              FPLoop, which has three contracts, additionally show how to
}
                                                                  specify floating-point loop behavior using loop invariants.

                                                                  4.2 Proof obligation generation
find    (float)0
replace 0.0 f                      .                              To reason about the contract of a selected benchmark, we
                                                                  apply KeY, which generates proof obligations or ‘goals’.
                                                                  Some of these goals (heap-related) are closed by KeY auto-
   Similar theorems and rules can be formulated for other         matically. The remaining open goals are closed by either
combinations of primitive types, in particular involving          SMT solvers with floating-point support directly (Sects. 3.1
double and long.
                                                                  and 3.2.1), or with a combination of transcendental KeY
   An example program, which makes use of numeric pro-            taclets and floating-point SMT solving (Sect. 3.2.2).
motion in Java, is shown in Listing 2, where the loop                 Columns 6 and 7 in Table 1 show the number of proof
invariant and the postcondition contain a numeric promotion       obligations closed by KeY directly and to be discharged by
(made explicit in the listing). In order to prove that the loop   external solvers, respectively. The next two columns show
invariant is inductive, one has to show that (float)(i +1) =      the number of taclet rules that KeY applied in order to close
(float)i + 1. f , which can be proven using the newly intro-      its goals, and the time this takes. For benchmarks with two
duced taclet mentioned above.                                     contracts, we show the respective values separated by ‘/’.
                                                                      We run our experiments on a server with 1.5 TB memory
                                                                  and 4x12 CPU cores at 3 GHz. However, KeY runs single-
4 Evaluation
                                                                  threadedly and does not use more than 8GB of memory.
4.1 Benchmark programs                                                For our set of benchmarks, the symbolic execution pro-
                                                                  cess is fully automated. Note that the machinery can deal
    We collected a set of existing floating-point Java pro-       with loop invariants, if they are provided. Automated loop
grams representing real-world applications in order to eval-      invariant generation is, however, particularly challenging for
uate the feasibility and performance of KeY’s floating-point      floating-points due to roundoff errors [25,39], and a research
support.                                                          topic in itself.
    The left half of Table 1 provides an overview of our
benchmarks. Each benchmark consists of one method, which          4.3 Evaluation of SMT floating-point support
is composed of arithmetic operations and method calls
to potentially other classes. The invocations of methods          Previous work [30] reported that SMT support for float-
from java.lang.Math (e.g., Math.abs) are marked by “+1”           ing-point arithmetic is rather limited. However, with recent
in Table 1; these are resolved by inlining the method imple-      advances [15], we evaluate the situation again. Most bench-
mentation. For benchmarks that contain calls to transcen-         marks used to evaluate SMT solvers’ decision procedures [55]
dental functions and square root, the called functions are        aim to check (individual) specialized (corner case) prop-
listed; these are handled by our axiomatization. We include       erties of floating-point arithmetic. The proof obligations


123
Combining rule- and SMT-based reasoning . . .                                                                                         193


Table 1 Benchmark details and KeY automode statistics, time is measured in seconds
Benchmark                    Benchmark details                                        Automode statistics
                             # Classes     # Method   # Arith.      Library           # Goals       # Goals      # Rules       Automode
                                           calls      ops           functions         closed        to be        applied       time (s)
                                                                                      by KeY        closed
                                                                                                    externally

Complex.add (2)              1             0          2             –                 3/3           1/4          185 / 286     0.7 / 0.2
Complex.divide (2)           1             0          11            –                 10 / 8        2/8          483 / 625     0.7 / 0.8
Complex.compare              1             0          2             –                 3             2            216           0.2
Complex.reciprocal (2)       1             1          6             –                 1/1           2/2          402 / 406     0.4 / 0.5
Circuit.impedance            2             1          3             –                 1             4            360           0.5
Circuit.current (2)          2             3          14            –                 11 / 11       4/1          1267 / 1238   4.0 / 4.1
Matrix2.transposedEq         1             3          3             –                 3             1            735           0.9
Matrix3.transposedEq         1             4          34            –                 3             1            1786          5.1
Matrix3.transposedEqV2       1             4          34            –                 3             1            1796          5.4
Rectangle.scale (2)          3+1           23         22            –                 32 / 32       32 / 16      5990 / 5617   18.4 / 14.5
Rotate.computeError          1+1           6          26            –                 108           8            3693          74.2
Rotate.computeRelErr         1+1           6          28            –                 120           8            3898          79.6
FPLoop.fploop                1             0          1             –                 2             4            99            0.1
FPLoop.fploop2               1             0          1             –                 2             4            99            0.1
FPLoop.fploop3               1             0          1             –                 2             4            99            0.1
Pine.ex2                     1             1          9             –                 2             12           320           1.3
Pine.ex2-reset               1             1          9             –                 2             16           394           1.8
Pine.ex3-reset-leadlag       1             1          6             –                 2             15           240           0.5
Pine.ex7-dampened            1             1          5             –                 2             10           203           0.6
Pine.filter-goubault         1             1          3             –                 2             8            183           0.5
Pine.filter-mine1            1             1          4             –                 2             10           211           0.6
Pine.filter-mine2            1             1          3             –                 2             8            172           0.6
Pine.filter-mine2-nondet     1             1          4             –                 2             8            193           0.5
Pine.harmonic                1             1          5             –                 2             9            199           0.4
Pine.pendulum-approx         1             1          17            –                 2             10           299           0.9
Pine.pendulum-small          1             1          7             –                 2             10           224           0.7
Pine.symplectic              1             1          6             –                 2             9            195           0.7
Cartesian.toPolar            2+1           3          6             sqrt, atan        1             4            438           0.5
Cartesian.distanceTo         1+1           1          5             sqrt              2             1            191           0.1
Polar.toCartesian            2+1           3          4             cos, sin          1             2            364           0.5
Circuit.instantCurrent       2+1           14         23            sqrt, atan, cos   17            2            1686          14.1
Circuit.instantVoltage       1+1           1          4             cos               0             2            138           0.1



generated from our set of benchmarks are complementary                    proof obligations in parallel, for our experiments, we do so
in that they are more arithmetic heavy, while nonetheless                 sequentially to maintain comparability.
relying on accurate reasoning about special values and func-                 KeY’s default translation to SMT introduces axioms
tional properties.                                                        which include quantifiers. These quantifications are not
   For each open goal not automatically closed, KeY gen-                  related to floating-point arithmetic, but are used to logically
erates one SMT-LIB file that is fed to the solvers for                    encode important properties of the Java memory model, like
validation. We compare the performance of the three major                 the type hierarchy and the absence of dangling references
SMT solvers with floating-point support CVC4 [6] (version                 on any valid Java heap. If we reason about floating-point
1.8, with the SymFPU library [15] enabled), Z3 (4.8.9) [26]               problems in isolation, they are not needed, but if we want to
and MathSAT (5.6.3) [20]. For this, we set a timeout of 300s              consider Java verification more holistically with questions
for each proof obligation. While KeY is able to discharge                 combining aspects of heap and floating point reasoning,


                                                                                                                               123
194                                                                                                                            R. Abbasi et al.


Table 2 Summary of valid / invalid goals correctly decided and average running times of each solver for the SMT translations with and without
quantified axioms
Details   Experiment           Quantified axioms     # Goals    CVC4                     Z3                          MathSAT
                                                                # Goals decided   Avg.   # Goals decided    Avg.     # Goals decided     Avg.

Table 3   Valid                ✓                     80         79                5.4    25                 25       –                   –
Table 4   contracts            ✗                     80         79                5.3    52                 63.7     80                  10.1
Table 5   Invalid              ✓                     9          0                 7.6    0                  2.6      –                   –
          contracts            ✗                     9          8                 12.8   7                  60.4     9                   2.0
Table 8   Axioms in SMT        ✓                     10         9                 17.3   4                  65.0     –                   –
          Axioms as taclets    ✓                     10         10                28.0   2                  164.0    –                   –
          Axioms as taclets    ✗                     10         10                28.1   5                  84.3     8                   1.5
Table 9   fp.sqrt              ✗                     7          7                 40.4   1                  23.5     5                   1.2
          Axiomatized sqrt     ✗                     7          5                 2.1    5                  86.4     5                   3.9
Table 6   Loop invariants      ✗                     113        113               6.5    112                13.5     113                 5.0




Fig. 2 Runtimes for valid goals with SMT translations with quantifiers   Fig. 3 Runtimes for valid goals with SMT translations without quan-
                                                                         tifiers



they become essential. We manually inspected that the proof
obligations without our axiomatized treatment of transcen-               axiomatizations of transcendental functions and square root,
dental functions do not depend on these properties and                   and loop invariants, respectively.
investigate the quantifier support by including or removing                 Figures 2 and 3 show a more detailed view of the solvers’
them from the SMT translations. We do not report results                 running time for the valid benchmarks. The x-axis shows
with quantifiers for MathSAT, since it does not support                  the number of open goals that are discharged by the SMT
them.                                                                    solvers, sorted by running time for each solver individually.
    Table 2 summarizes the results of our experiments; the               The k-th point of one graph shows the minimum running
first column lists the corresponding table with detailed                 time needed by the solver to close each of the k fastest goals.
results. Column 4 shows the number of expected valid or                  Note that each solver may have different goals which are its
invalid goals for all benchmarks. For each solver, we show               k fastest. The y-axis shows the time on a logarithmic scale,
the number of goals that each solver can validate or inval-              and the maximum value of 300 indicates the timeout.
idate, together with the average time (in seconds) needed.                  We conclude that in the presence of quantified axioms
The goals resulting in timeout were excluded from the com-               and floating-point arithmetic solvers’ performance deterio-
putation of the average time. Column 3 shows whether the                 rate for both valid and invalid goals. In particular, none of the
SMT queries include quantifiers or not. The rows summa-                  solvers is able to find counterexamples for any of the invalid
rize our experiments with valid contracts, invalid contracts,            goals. However, when the quantified axioms are removed


123
Combining rule- and SMT-based reasoning . . .                                                                                        195


                                                                        from the SMT translations, their performance improves. For
Listing 3 The Matrix3 benchmark
                                                                        valid contracts, CVC4 and MathSAT perform better than
public class Matrix3 {
                                                                        Z3, in terms of both number of goals validated and the run-
    //The matrix: [[a b c],[d e f],[g h i]]                             ning time per goal. In particular, MathSAT is able to prove
    double a, b, c, d, e, f, g, h, i;                                   all goals. However, the running time performance of CVC4
    double det;
                                                                        is better than MathSAT’s. For invalid contracts, solvers are
    // method transpose not shown
                                                                        able to produce the expected counterexamples at least par-
    double determinant() {                                              tially. Particularly, MathSAT has a better performance than
        return (a * e * i + b * f * g + c * d * h) -                    CVC4 and Z3 in terms of both running time and the number
        (c * e * g + b * d * i + a * f * h);
                                                                        of proof obligations for which it can produce counterexam-
    }
                                                                        ples.
    double determinantNew() {
        return (a * (e * i) + (g * (b * f) + c * (d * h))) -
        (e * (c * g) + (i * (b * d) + a * (f * h)));                    Proving functional properties Listings 3 and 4 show exam-
    }
                                                                        ples of functional properties that are concerned with floating-
    /*@ ensures \fp_normal(\result) ==> (\result == det); @*/           point computation. The verification results are included
    double transposedEq() {                                             in Table 3 and Table 4.
        det = determinant();
        return transpose().determinant();
    }


    /*@ ensures \fp_normal(\result) ==> (\result == det); @*/
    double transposedEqV2() {
        det = determinantNew();
        return transpose().determinantNew();
    }
}




Table 3 Summary of valid goals proved and running times of each solver for the SMT translations with quantified axioms
Benchmark                         # Goals        CVC4                                              Z3
                                                 # Goals proven         Avg.         Max.          # Goals proven        Avg.       Max.

Complex.add(1)                    1              1                      0.6          0.6           1                     1.6        1.6
Complex.divide(1)                 2              2                      1.7          1.9           2                     1.8        2.3
Complex.divide(2)                 8              8                      3.4          11.5          4                     3.2        TO
Complex.compare                   2              2                      0.5          0.6           2                     1.5        1.5
Complex.reciprocal(1)             2              2                      1.0          1.7           0                     –          TO
Complex.reciprocal(2)             2              2                      1.8          2.4           2                     2.7        4.0
Circuit.impedance                 4              4                      0.8          0.9           3                     87.5       TO
Circuit.current(1)                4              4                      6.3          13.2          0                     –          TO
Circuit.current(2)                1              1                      5.5          5.5           0                     –          TO
Matrix2.transposedEq              1              1                      0.5          0.5           0                     –          TO
Matrix3.transposedEqV2            1              1                      1.3          1.3           0                     –          TO
Rectangle.scale(1)                32             31                     2.2          TO            7                     46.6       TO
Rotate.computeError               8              8                      9.8          13.9          0                     –          TO
Rotate.computeRelErr              8              8                      25.3         45.6          0                     –          TO
FPLoop.fploop                     4              4                      0.5          1.0           4                         2.3    8.1
Summary                           80             79                     5.4          TO            25                    25         TO




                                                                                                                                   123
196                                                                                                                                            R. Abbasi et al.


Table 4 Summary of valid goals proved and running times of each solver for the SMT translations without quantified axioms
Benchmark                   # Goals       CVC4                                  Z3                                         MathSAT
                                          # Goals proven    Avg.       Max.     # Goals proven   Avg.         Max.         # Goals proven      Avg.     Max.

Complex.add(1)              1             1                 0.5        0.5      1                1.3          1.3          1                   0.2      0.2
Complex.divide(1)           2             2                 1.6        1.9      2                2.1          2.7          2                   1.5      1.9
Complex.divide(2)           8             8                 3.4        11.4     4                2.5          TO           8                   29.0     209.5
Complex.compare             2             2                 0.5        0.6      2                1.1          1.3          2                   0.2      0.2
Complex.reciprocal(1)       2             2                 0.9        1.5      1                198.5        TO           2                   2.2      2.4
Complex.reciprocal(2)       2             2                 1.7        2.3      2                2.8          3.4          2                   1.5      1.9
Circuit.impedance           4             4                 0.7        0.7      4                9.5          17.1         4                   0.4      0.5
Circuit.current(1)          4             4                 6.3        13.0     0                –            TO           4                   13.3     36.2
Circuit.current(2)          1             1                 5.2        5.2      0                –            TO           1                   26.3     26.3
Matrix2.transposedEq        1             1                 0.5        0.5      0                –            TO           1                   0.6      0.6
Matrix3.transposedEqV2      1             1                 1.1        1.1      0                –            TO           1                   3.9      3.9
Rectangle.scale(1)          32            31                2.1        TO       32               95.1         251.8        32                  2.4      4.2
Rotate.computeError         8             8                 9.7        13.5     0                –            TO           8                   22.7     35.7
Rotate.computeRelErr        8             8                 25.0       45.0     0                –            TO           8                   27.5     46.4
FPLoop.fploop               4             4                 0.5        1.1      4                2.0          7.2          4                   0.4      1.0
Summary                     80            79                5.3        TO       52               63.7         TO           80                  10.1     209.5


Table 5 Summary of invalid goals proved and running times of each solver for the SMT translations with and without quantified axioms
Benchmark                   # Goals              CVC4                                 Z3                                       MathSAT
                                                 # Goals           Avg.       Max.    # Goals          Avg.         Max.       # Goals          Avg.    Max.
                            Valid     Invalid    Valid Invalid                        Valid Invalid                            Valid Invalid

With quantified axioms
Matrix3.transposedEq        0         1          0      0          –          TO      0     0          –            TO         –     –          –        –
Rectangle.scale(2)          12        4          12     0          12.2       TO      8     0          4.6          TO         –     –          –       –
Complex.add(2)              2         2          2      0          0.6        0.7     2     0          1.4          TO         –     –          –        –
FPLoop.fploop2              3         1          3      0          0.9        1.7     3     0          0.5          TO         –     –          –        –
FPLoop.fploop3              3         1          3      0          0.4        1.7     3     0          0.3          TO         –     –          –        –
Summary                     20        9          20     0          7.6        TO      16    0          2.6          TO         –     –          –        –
Without quantified axioms
Matrix3.transposedEq        0         1          0      1          170.2      170.2   0     0          –            TO         0     1          16.2     16.2
Rectangle.scale(2)          12        4          12     3          12.2       TO      12    3          108.2        TO         12    4          2.4      9.5
Complex.add(2)              2         2          2      2          0.5        0.5     2     2          0.7          1.0        2     2          0.2      0.2
FPLoop.fploop2              3         1          3      1          0.4        0.6     3     1          0.9          1.7        3     1          0.3      0.5
FPLoop.fploop3              3         1          3      1          0.3        0.6     3     1          0.6          1.7        3     1          0.2      0.4
Summary                     20        9          20     8          12.8       TO      20    7          60.4         TO         20    9          2.0      16.2



    For Matrix, we check that the determinants of a matrix                      method) to KeY, CVC4 validates the contract in 1.1s, Math-
and its transpose are equal. Note that this property holds                      SAT in 3.9s and Z3 times out again. One thing worth noting
trivially under real arithmetic, but not necessarily under                      is that the way programs are written can greatly influence
floating-points. After feeding transposedEq (which uses the                     the computational complexity needed to reject or verify the
determinant method) and its contract to KeY, increasing                         contract. This is evident from the fact that slightly modify-
the default timeout sufficiently and discharging the created                    ing the order of operations (using determinantNew instead)
goal, CVC4 generates a counterexample in 170.2s seconds                         substantially reduces verification time and changes the veri-
and MathSAT in 16.2s. Z3 times out after 30 minutes.                            fication result for MathSAT and CVC4.
By feeding transposedEqV2 (which uses the determinantNew


123
Combining rule- and SMT-based reasoning . . .                                                                               197


                                                                  is able to prove that all but one of the considered invariants
Listing 4 The Rotation benchmark
                                                                  are in fact inductive. We used the timeout of two hours for
public class Rotation {
    final static double cos90 = 6.123233995736766E-17;
                                                                  this experiment and observed that MathSAT performs better
    final static double sin90 = 1.0;                              than the other solvers in proving the invariants.
                                                                     Note that not all invariants generated by Pine are neces-
    // rotates a 2D vector by 90 degrees
                                                                  sarily verifiable by KeY (e.g., Ex2 in Table 6), because the
    public static double[] rotate(double[] vec) {
        double x = vec[0] * cos90 - vec[1] * sin90;
                                                                  semantics of Pine and KeY differ subtly. In Pine, the gener-
        double y = vec[0] * sin90 + vec[1] * cos90;               ated invariant and bounds are considered to be real-valued,
        return new double[]{x, y};                                whereas in KeY they are evaluated under a floating-point
    }
                                                                  semantics.
    /*@ requires (\forall int i; 0 <= i && i < vec.length;
      @ \fp_nice(vec[i]) && vec[i] > 1.0 && vec[i] < 2.0) &&
                                                                  Sensitivity to contract variations We conducted an exper-
        @   vec.length == 2;                                      iment on our Rectangle.scale benchmark to assess the
        @ ensures   \result[0] < 1.0E-15 &&                       solver’s sensitivity to various changes, applied to the bench-
        @ \result[1] < 1.0E-15;
                                                                  mark’s contract or its implementation.
      @*/
    public static double[] computeError(double[] vec) {
                                                                     Specifically, we considered the following versions of the
        double[] temp = rotate(rotate(rotate(rotate(vec))));      benchmark:
        return new double[]{Math.abs(temp[0] - vec[0]),
         Math.abs(temp[1] - vec[1])};
    }
                                                                   • v0: is the original version of the benchmark (Listing 1
}                                                                    using the second contract) and our baseline;
                                                                   • v1: reduces the number of classes involved to two, while
                                                                     keeping the same functionality;
                                                                   • v2: reduces the number of classes involved to one, while
   For Rotate, we check that the difference between an orig-         keeping the same functionality;
inal vector and the one that is rotated four times by 90           • v3: modifies v2 such that variable bounds in the precon-
degrees must not be larger than 1.0E-15. We also verified            dition become more “complicated” in terms of longer
the same bound for the relative difference (by exploiting            fractional parts (e.g., the bounds for arg2 become
another method and contract) for this benchmark. The con-            [3.0000001, -6.4000000003] instead of [3.0001, -6.4000
stant cos90 in Listing 4 is not precisely 0.0 to account for         003]);
rounding effects in the computation of the cosine. FPLoop          • v4: simplifies the mathematical expression of v2 (less
includes three loops, for which the contracts check that the         arithmetic operations)
return value is bigger than a given constant.                      • v5: modifies v3 such that arg2 has a tighter bound, i.e.,
   Furthermore, we have investigated KeY’s capability in             the interval width is smaller
proving floating-point loop invariants in more details in the      • v6: modifies v2 such that arg2 has a larger bound, i.e.,
next experiment.                                                     the interval width is larger
   Though not always very fast, these examples show that           • v7: modifies v2 such that only arg2 has a “complicated”
verification of functional floating-point properties is viable.      bound
                                                                   • v8: modifies v0 such that arg2 has a tighter bound
Proving loop invariants We conducted an experiment to
assess KeY in proving floating-point loop invariants for a           Table 7 summarizes the results for this experiment. With
set of benchmarks. As part of this experiment, we verified        the quantified formulas included in the SMT translation,
some of the floating-point loop invariants generated by the       both CVC4 and Z3 are able to prove more goals when the
Pine tool [39] (represented as Pine.* in Table 1). Listing 5      number of classes is reduced, and also when the number
shows the nonlinear Pine.pendulum-approx benchmark and            of arithmetic operations is reduced. Z3 further seems to be
the loop invariant that Pine has generated. This benchmark        sensitive to whether variable bounds are “complicated” or
simulates a simple pendulum and uses a Taylor approxima-          not, whereas CVC4 is not. We obtain a somewhat surprising
tion of the sine function. The condition of the while loop is a   result when arg2 has a tighter bound. While Z3’s perfor-
placeholder for any condition, meaning that we are proving        mance improves, CVC4 validates two goals less. On the
the loop invariant regardless of how many iterations the loop     other hand, increasing the bounds on arg2 does not seem
takes. We thus specify diverges true, which means that the        to make a difference.
method is (unconditionally) allowed to not terminate.                It seems that arg2 is the bottleneck for this benchmark;
   Row 10 in Table 2 summarizes the results of this experi-       when only arg2 has a “complicated” input interval, CVC4
ment, and Table 6 shows the detailed results. As shown, KeY       proves less goals. Finally, constraining arg2 in the original


                                                                                                                     123
198                                                                                                                                    R. Abbasi et al.


Table 6 Summary of goals proved and running times of each solver for benchmarks with floating-point loop invariants without quantified axioms
Benchmark                # Goals       CVC4                                  Z3                                       MathSAT
                                       # Goals proven   Avg.      Max.       # Goals proven     Avg.    Max.          # Goals proven   Avg.     Max.

Ex2                      12            9(CE)            5.2       34.4       9(CE)              27.6    TO            9(CE)            3.4      22.7
Ex2-reset                16            16               0.8       4.2        16                 19.3    162.8         16               0.9      2.9
Ex3-reset-leadlag        15            15               0.7       5.7        15                 0.4     496.8         15               0.9      8.5
Ex7-dampened             10            10               1.5       10.2       10                 1.9     3081.0        10               3.9      34.2
Filter-goubault          8             8                2.1       13.2       8                  8.7     360.4         8                3.3      21.8
Filter-mine1             10            10               1.2       4.6        10                 1.3     522.2         10               1.9      8.1
Filter-mine2             8             8                8.4       63.0       8                  0.3     997.5         8                21.0     163.1
Filter-mine2-nondet      8             8                0.9       2.7        8                  14.1    707.7         8                0.8      3.6
Harmonic                 9             9                2.9       20.1       9                  28.5    2643.0        9                2.7      20.2
Pendulum-approx          10            10               47.2      223.7      9                  4.9     TO            10               16.8     421.2
Pendulum-small           10            10               1.9       14.5       10                 7.5     2412.5        10               1.8      14.6
Symplectic               9             9                1.7       9.2        9                  32.9    1989.1        9                3.4      21.5
Summary                  113           113              6.5       223.7      112                13.5    TO            113              5.0      421.2


Table 7 SMT solvers summary statistics for various versions of the Rectangle benchmark with quantified axioms in the SMT translations
version      Applied change                             # Goals         CVC4                                     Z3
                                                                        # Goals validated     Avg.     Max.      # Goals validated     Avg.     Max.

v0           None (original)                            32              31                    2.3      TO        7                     46.2      TO
v1           Fewer classes (2) in v0                    32              32                    2.5      4.8       9                     42.7      TO
v2           Fewer classes (1) in v0                    32              32                    2.4      4.2       7                     85.2      TO
v3           Complicated intervals for all vars in v2   32              32                    2.5      5.5       6                     59.3      TO
v4           Simpler math in v2                         16              16                    1.0      1.3       12                    35.3      TO
v5           Shorter interval for arg2 in v3            32              30                    2.3      TO        9                     95.1     TO
v6           Longer interval for arg2 in v2             32              32                    2.6      7.4       7                     14.8     TO
v7           Complicated interval for arg2 in v2        32              31                    2.4      TO        7                     23.9      TO
v8           Shorter interval for arg2 in v0            32              32                    2.5      4.2       7                     46.5      TO


benchmark more tightly allows CVC4 to validate all goals                         are included in Table 8. Note that both approaches are fully
but Z3’s performance remains unaffected.                                         automated.
   With the SMT-LIB translation that does not introduce                             We conclude that the SMT solvers perform better when
quantified axioms, we can see that CVC4’s results, in terms                      the axiomatization is applied at the KeY level. When axioms
of number of goals validated, are the same as before, while                      for transcendental functions are added to the SMT-LIB
Z3 performs much better than before. MathSAT is able to                          translation directly Z3 validates 4 out of 10 goals. With the
validate all goals of all versions.                                              axiomatization at the KeY level, solvers are able to vali-
   In summary, the solvers’ performance seems to be sensi-                       date more goals (with quantified formulas removed from the
tive to slight innocuous looking changes such as the number                      SMT translations), e.g., Z3 is able to validate 5 goals and
of classes involved and variable bounds. For example, con-                       CVC4 can validate all. Therefore, it is preferable to apply
straining arg2 in the original benchmark more tightly allows                     them on the KeY side via taclet rules.
CVC4 to validate all goals (1 more). This behavior could be                         All the solvers we have used in this work comply with the
potentially exploited by, e.g., relaxing a variable’s bounds.                    IEEE 754 standard and therefore have bit-precise support for
                                                                                 the square-root function. They provide bit-precise reasoning
                                                                                 by effectively encoding the behavior of floating-point cir-
4.4 Transcendental functions in KeY                                              cuits over bitvectors (which is naturally expensive), together
                                                                                 with different heuristics and abstractions to speed up solv-
  We evaluated the two approaches from Sect. 3.2.1 on                            ing time. However, depending on the property, we do not
our set of benchmarks; rows 5, 6, and 7 in Table 2 sum-                          always need bit-precise reasoning, so we propose handling
marize the results. The detailed results of these experiments


123
Combining rule- and SMT-based reasoning . . .                                                                                                    199


Table 8 Summary statistics with axioms in SMT-LIB translations and as taclet rules in KeY
Benchmark                 # Goals   CVC4                                     Z3                                   MathSAT
                                    # Goals validated        Avg.    Max.    # Goals validated    Avg.    Max.    # Goals validated   Avg.   Max.

Axioms in SMT-LIB translation
Cartesian.toPolar         4         4                        7.1     9.2     1                    16.8    TO      –                   –      –
Polar.toCartesian         2         2                        0.9     0.9     2                    69.7    95.7    –                   –      –
Circuit.instantCurrent    2         1                        123.6   TO      0                    –       TO      –                   –      –
Circuit.instantVoltage    2         2                        1.1     1.1     1                    103.8   TO      –                   –      –
Summary                   10        9                        17.3    TO      4                    65.0    TO      –                   –      –
Axioms as taclet rules in KeY with quantified formulas
Cartesian.toPolar         4         4                        6.8     7.7     1                    40.0    TO      –                   –      –
Polar.toCartesian         2         2                        1.4     1.9     1                    288.0   TO      –                   –      –
Circuit.instantCurrent    2         2                        123.8   128.3   0                    –       TO      –                   –      –
Circuit.instantVoltage    2         2                        1.3     1.3     0                    –       TO      –                   –      –
Summary                   10        10                       28.0    128.3   2                    164.0   TO      –                   –      –
Axioms as taclet rules in KeY without quantified formulas
Cartesian.toPolar         4         4                        6.9     7.5     1                    23.5    TO      4                   1.2    1.7
Polar.toCartesian         2         2                        1.5     2.3     2                    52.6    81.2    2                   0.6    0.8
Circuit.instantCurrent    2         2                        123.5   127.5   0                    –       TO      0                   –      TO
Circuit.instantVoltage    2         2                        1.5     1.7     2                    146.4   160.7   2                   0.8    0.8
Summary                   10        10                       28.1    127.5   5                    84.3    TO      8                   1.5    TO



                                                                                  • If arg is NaN or less than zero, then sqrt(arg) is NaN.
Listing 5 The pendulum-approx benchmark
                                                                                  • If arg is positive infinity, then sqrt(arg) is positive infin-
/*@ public normal_behavior
                                                                                    ity.
  @ requires 0.0f <= u && u <= 0.0f && 2.0f <= v && v <= 3.0f;                    • If arg is positive zero or negative zero, then sqrt(arg) is
    @ diverges true;                                                                the same as arg.
    @*/
                                                                                  • If arg is not NaN and greater than or equal to zero, then
    public float pendulum-approx(float u, float v) {
                                                                                    sqrt(arg) is not NaN.
      /*@ loop_invariant -1.1f <= u && u <= 1.2f        &&                        • If arg is not infinity and is greater than one then
        @ -3.2f <= v && v <= 3.1f &&                                                sqrt(arg) < arg.
        @   (-0.11f*u) + (0.01f*v) + (1.0f*u*u) + (0.03f*u*v)
        @   + (0.12f*v*v) <= 1.15f;
        @*/
        while (true) {
         u = u + 0.01f * v;
                                                                                    Rows 8 and 9 in Table 2 summarize the results for this
         v = v + 0.01f * (-0.5f * v - 9.81f *
            (u - (u * u * u) / 6.0f +                                            experiment; the detailed results are included in Table 9.
            (u * u * u * u * u) / 120.0f));                                         We observed that for two out of the three benchmarks,
        }                                                                        the average running time of all solvers decreases using
        return u;
                                                                                 the axiomatized square root. Furthermore, Z3 is able to
}
                                                                                 reason about more proof obligations with the axiomatized
                                                                                 version. However, the success of this approach depends
the square-root function with the same taclet-based axioma-                      on the axioms added to KeY and may not always work
tization as introduced in Sect. 3.2.2.                                           if we do not have suitable axioms. For example, for the
   To this end, we conducted an experiment on the bench-                         Circuit.instantCurrent benchmark which computes the
marks containing sqrt, comparing the approach from                               instantanious current of an RL circuit (Listing 6), using the
Sect. 3.2.2 (adding the necessary axioms, resp. taclet rules)                    axiomatized square root, CVC4 is not able to validate the
to using the square root implemented in SMT solvers                              contract, but with fp.sqrt the contract is validated. The rea-
(fp.sqrt). We chose to include only axioms specified in                          son our approach is unsuccessful on this benchmark is that
or inferred from the IEEE 754 standard. The set of used                          the square-root function appears early in the computation
axioms are as follows:                                                           followed by atan and cos afterwards, resulting in complex


                                                                                                                                          123
200                                                                                                                            R. Abbasi et al.

Table 9 Summary statistics for benchmarks containing the square-root function, with quantified formulas removed from the SMT-LIB
translation
Benchmark                # Goals   CVC4                                Z3                                  MathSAT
                                   # Goals validated   Avg.    Max.    # Goals validated   Avg.    Max.    # Goals validated   Avg.     Max.

fp.sqrt
Cartesian.toPolar        4         4                   6.9     7.5     1                   23.5    TO      4                   1.2       1.7
Cartesian.distanceTo     1         1                   8.2     8.2     0                   –       TO      1                   1.0       1.0
Circuit.instantCurrent   2         2                   123.5   127.5   0                   –       TO      0                   –         TO
Summary                  7         7                   40.4    127.5   1                   23.5    TO      5                   1.2       TO
Axiomatized sqrt
Cartesian.toPolar        4         4                   2.0     2.9     4                   49.81   163.0   4                   1.0      1.6
Cartesian.distanceTo     1         1                   2.7     2.7     1                   233.0   233.0   1                   1.0       1.0
Circuit.instantCurrent   2         0                   –       TO      0                   –       TO      0 (2 CE)            11.1     13.8
Summary                  7         5                   2.1     TO      5                   86.4    TO      5                   3.9       13.8


Listing 6 The Circuit.instantCurrent benchmark
public class Circuit {
    double maxVoltage, frequency, resistance, inductance;
    // ...


/*@ public normal_behavior
  @ requires 1.0 < this.maxVoltage && this.maxVoltage < 12.0 && 1.0 < this.frequency && this.frequency < 100.0 &&
    @   1.0 < this.resistance && this.resistance < 50.0 && 0.001 < this.inductance && this.inductance < 0.004 &&
    @  0.0 < time && time < 300.0;
    @ ensures !\fp_nan(\result) && !\fp_infinite(\result);
  @*/
public double instantCurrent(double time) {
    Complex curr = computeCurrent();
    double maxCurrent = Math.sqrt(curr.getRealPart() * curr.getRealPart() + curr.getImaginaryPart() * curr.getImaginaryPart());
    double theta = Math.atan(curr.getImaginaryPart() / curr.getRealPart());
    return maxCurrent * Math.cos((2.0 * Math.PI * frequency * time) + theta);
}
}




expressions. In order to prove the corresponding proof obli-               of variable input ranges. From our experiment with pro-
gations, in this case stronger axioms are needed.                          grams containing loops, we observed that KeY is able to
                                                                           prove the provided invariants and solvers are mostly able to
   In summary, treating sqrt axiomatically can result in
                                                                           prove the generated goals. Finally, based on our results, we
shorter solving times than performing bit-precise reasoning,
                                                                           can confirm that the support for floating-point theory seams
but the approach may not always succeed when the axioms
                                                                           promising in all the solvers we examined. However, in terms
are not sufficient to prove a particular property.
                                                                           of scalability and the size and type of problems they can han-
                                                                           dle, there is still room for improvement.
4.5 Discussion and insights                                                   From our experiments with programs containing tran-
                                                                           scendental functions (and sqrt), we observed that handling
In our set of experiments, we used benchmarks taken from                   these functions as uninterpreted with an appropriate axiom-
real code to examine the feasibility of our approach and                   atization at the SMT-LIB or the taclet level is a viable
the solver’s support for the floating-point theory. We can                 approach, with an interesting trade-off between the verifier
conclude that, for our set of benchmarks, generally all the                performance and the properties that can be proven. Clearly,
solvers perform better with an SMT translation that does                   properties that require exact semantics for transcendental
not introduce quantified formulas. Especially if the contract              functions will not be proven with our approach, but our
of the benchmark is invalid, the solvers are not able to pro-              experiments show that reasoning about the absence of spe-
duce counterexamples when quantifiers are present. Another                 cial values is indeed possible. We further observe that both
observation is that solvers’ performance is affected by the                our approaches for adding axioms to the SMT queries or as
number of heap operations performed and the complexity


123
Combining rule- and SMT-based reasoning . . .                                                                              201


taclet rules work to some extent, however, applying axioms       5 Related work
as taclets in KeY directly has several advantages. Using
taclets avoids quantified axioms in the SMT query, which         Our implementation uses the floating-point SMT-LIB the-
in turn improves the performance. While the additional           ory [16], which, however, does not handle transcendental
assertions do not compromise the theoretical decidability        functions, as their semantics is (library) implementation
of the theory (since the quantified domains are finite), they    dependent. Some real-valued automated solvers do handle
add considerably to the complexity of the encoding for the       transcendental functions [3,31], but to the best of our knowl-
bit-blasting SAT-based decision procedures such that run-        edge, the combination of floating-points and reals in SMT
ning times may increase exponentially. The experiments           solvers is still severely limited.
have thus exposed a weakness of the SAT-based verification          None of the existing deductive verifiers support floating-
approach: if symbols outside the canonical arithmetic oper-      point transcendental functions automatically. The Why3
ations with fixed semantics are used within a program or         deductive verification framework [28] has support for floating-
specification, providing semantics for these symbols within      point arithmetic, with front-ends for the C and Ada program-
the SMT-LIB translation is not efficient.                        ming languages through Frama-C [23] and SPARK [17,30],
   Concretely, applying the axiomatization as taclets (and       respectively. Why3 has back-end support for different SMT
removing other quantifiers from the SMT translation) allows      solvers, as well as interactive proof assistants like Coq.
us to use MathSAT as the solver. Furthermore, we have also       Until recently, Why3 would discharge still many interest-
observed that quantifiers in the SMT queries result in poor      ing floating-point problems with the help of Coq, relying on
performance (unknown results or timeouts) when a query is        significant user interaction. In later work [30] (in the context
invalid. Applying axioms as taclets lets us avoid this issue.    with floating-point verification for Ada programs), Why3
The rule-based sequent calculus, on which the KeY reason-        can achieve a higher degree of automation. Note, however,
ing engine is based, deals with universally quantified symbol    that the user is still required to add code assertions as well
axiomatizations very successfully in many domains. The           as ‘ghost code’ to a significant extent.
taclet mechanism and the implemented automatic strategy             The Boogie intermediate verification language [46] also
allow one to control the treatment of the symbol depend-         supports floating-point expressions and targets Z3 for dis-
ing on a variety of side conditions, e.g., applying a lemma      charging proof obligations. In the Boogie community, it
only if another relevant formula is also present in the proof    was observed that writing a specification in Boogie leads
obligation. Furthermore, taclets can also be applied manu-       to decreases in SMT solver performance when compared to
ally, which allows the verifying user to control the calculus    writing the goal in SMT-LIB directly, probably due to an
in a very fined-grained manner. Another advantage of hav-        inherent mixing of theories when using Boogie [57]. This
ing taclet rules is that we can create taclets with different    matches our own experiences, and separation of theories
formats for a single axiom and by doing so can sometimes         should be considered an important task for the further devel-
even reduce the size of the proof obligation. This is the case   opment of floating-point verification.
when, instead of adding an axiom to the proof obligation,           Other deductive verifiers for Java have only rudimentary
we replace a term with another one and thus avoid enlarg-        support for floating-points. Verifast [40] treats floating-point
ing the proof obligation. That said, an axiomatization at the    operations as if they were real values, and OpenJML [21]
KeY level may result in spurious counterexamples if a rule       parses programs with floating-point operations, but essen-
application for an uninterpreted symbol, which would make        tially treats float and double as uninterpreted sorts.
the sequent valid, has not been applied yet. However, such a        The Java category of verification competition SV-COMP
spurious counterexample can be straightforwardly identified      [10] contains a number of benchmarks that make use of
by simply executing the method in question on it.                floating-point variables. However, the focus of these bench-
   To summarize, the experiments show that highly auto-          marks is usually not on arithmetical properties of expres-
mated floating point program verification is viable for          sions, but on the completeness of the Java language support.
relevant properties (handling of special values and some         Amongst the participants of SV-COMP 2020, Symbolic
functional properties), up to a certain level of complexity      (Java) Pathfinder (SPF) [54] (and various extensions) and
(given by the SMT solvers). The choices of which parts of        the Java Bounded Model Checker (JBMC) [22] support
a proof obligation are delegated to SMT, and how they are        floating-point arithmetic. Besides being limited to exploring
translated to SMT are crucial for achieving effective and        the state space up to a bounded depth, their constraint lan-
efficient program verification. Arithmetic operations proved     guages do not support quantifiers and abstracting of method
to be more efficiently dealt with by delegation to SMT,          calls—which are features that we have used in this work.
whereas for transcendental functions, axiomatization and            Floating-point arithmetic has also been formalized in sev-
rule-based treatment in the theorem prover, outside the SMT      eral interactive theorem provers [14,29,41]. While one can
solver, perform clearly better.                                  prove intricate properties about floating-point programs [12,


                                                                                                                    123
202                                                                                                                       R. Abbasi et al.


13,37], proofs using interactive provers are to a large part     scendental functions, as well as programs with loops. We
manual and require significant expertise.                        observe that the MathSAT and CVC4 solver’s floating-point
    Abstract interpretation-based techniques can show the        support scales sufficiently for our benchmarks, as long as the
absence of special values in floating-point code fully auto-     queries do not include any quantifiers. On the other hand,
matically, and several abstract domains which are sound          our axiomatized approach for transcendental functions is
with respect to floating-point arithmetic exist [18,42]. While   best realized using calculus rules in KeY’s internal reason-
the analysis itself is fully automated, applying it success-     ing engine, rather than in SMT solvers. We also presented
fully to real-world programs in general requires adaptation      rules for handling potentially rounding casts from integers
to each program analyzed by end-users, e.g., the selection of    to floating-point types.
suitable abstract domains or widening thresholds [11].              While our work is implemented within the KeY verifier,
   Besides showing the absence of special values, recent         we expect the insights from this work to be portable to other
research has developed static analyses to bound floating-        verifiers.
point roundoff errors [24,34,47,51,58]. These analyses cur-
                                                                 Acknowledgements This research was partially funded by the Deutsche
rently work only for small arithmetic kernels and the tools
                                                                 Forschungsgemeinschaft (DFG, German Research Foundation) project
in particular do not accept programs with objects.               387674182. The authors would like to thank Daniel Eddeland, who
   Dynamic analyses generally scale well on real-world           together with co-author W. Ahrendt performed prestudies which
programs, but can only identify bugs (when given failure-        impacted the current work.
triggering input), rather than proving correctness for all
                                                                 Funding Open Access funding enabled and organized by Projekt
possible inputs. Executing a floating-point program together     DEAL.
with a higher-precision one allows one to find inputs which
cause large roundoff errors [9,19,43]. Ariadne [5] uses a        Open Access This article is licensed under a Creative Commons
                                                                 Attribution 4.0 International License, which permits use, sharing, adap-
combination of symbolic execution, real-valued SMT solv-         tation, distribution and reproduction in any medium or format, as
ing and testing to find inputs that trigger floating-point       long as you give appropriate credit to the original author(s) and the
exceptions, including overflow and invalid operations. Our       source, provide a link to the Creative Commons licence, and indicate
work subsumes this approach as the SMT solvers that we           if changes were made. The images or other third party material in this
                                                                 article are included in the article’s Creative Commons licence, unless
use can directly generate counterexamples, but more impor-       indicated otherwise in a credit line to the material. If material is not
tantly, KeY is able to prove the absence of such exceptions.     included in the article’s Creative Commons licence and your intended
                                                                 use is not permitted by statutory regulation or exceeds the permitted
                                                                 use, you will need to obtain permission directly from the copy-
                                                                 right holder. To view a copy of this licence, visit http://creativecomm
6 Conclusion                                                     ons.org/licenses/by/4.0/.


In this work, we set out to enable efficient verification of     References
programs which feature floating-point computations in com-
bination with the other features of a fully fledged, widely       1. Abbasi, R., Schiffl, J., Darulova, E., Ulbrich, M., Ahrendt, W.:
used programming language, here Java. This is a differ-              Deductive verification of floating-point java programs in key. In:
                                                                     Tools and Algorithms for the Construction and Analysis of Sys-
ent problem from verifying floating-point computations in
                                                                     tems (TACAS) (2021)
isolation. To achieve that, we extend the verification tool       2. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H.,
KeY, which prior to this work supported full sequential Java         Ulbrich, M. (eds.): Deductive Software Verification - The KeY
except floating-point types. The core of KeY is a prover             Book - From Theory to Practice, LNCS, vol. 10001. Springer
                                                                     (2016)
applying proof rules capturing an axiomatic semantics of          3. Akbarpour, B., Paulson, L.C.: MetiTarski: An Automatic Theo-
the target language (Java), with the option to export proof          rem Prover for Real-Valued Special Functions. J. Autom. Reason.
goals to SMT solver plug-ins. This gave us the freedom               44(3) (2010)
to decide which features, and under which circumstances,          4. Astrauskas, V., Müller, P., Poli, F., Summers, A.J.: Leveraging
                                                                     rust types for modular specification and verification. In: Object-
should be dealt with by proof rules within the KeY prover,           Oriented Programming Systems, Languages, and Applications
or by exporting goals to an SMT solver, respectively.                (OOPSLA) (2019)
    By joining the complementary strengths of SAT-based           5. Barr, E.T., Vo, T., Le, V., Su, Z.: Automatic detection of
SMT solving and rule-based deduction, we presented the               floating-point exceptions. In: Principles of Programming Lan-
                                                                     guages (POPL) (2013)
first working floating-point support in a deductive verifica-     6. Barrett, C., Conway, C.L., Deters, M., Hadarean, L., Jovanovi’c,
tion tool for Java. At the same time, we close a remaining           D., King, T., Reynolds, A., Tinelli, C.: CVC4. In: Computer Aided
gap in KeY to now support full sequential Java. Our eval-            Verification (CAV) (2011). Snowbird, Utah
uation shows that for specifications dealing with absence         7. Barrett, C., Stump, A., Tinelli, C., et al.: The SMT-LIB standard:
                                                                     version 2.0. In: Proceedings of the 8th International Workshop on
of NaN and infinity, as well as with value ranges, our               Satisfiability Modulo Theories (2010)
approach can verify realistic programs automatically within
a reasonable time frame. This includes programs using tran-
123
Combining rule- and SMT-based reasoning . . .                                                                                                      203


 8. Beckert, B., Nestler, B., Kiefer, M., Selzer, M., Ulbrich, M.:            30. Fumex, C., Marché, C., Moy, Y.: Automating the verification of
    Experience report: Formal methods in material science. CoRR                   floating-point programs. In: Verified Software: Theories, Tools,
    arXiv:1802.02374 (2018)                                                       and Experiments (VSTTE) (2017)
 9. Benz, F., Hildebrandt, A., Hack, S.: A dynamic program analysis           31. Gao, S., Kong, S., Clarke, E.M.: dReal: An SMT solver for non-
    to find floating-point accuracy problems. In: Programming Lan-                linear theories over the reals. In: International Conference on
    guage Design and Implementation (PLDI) (2012)                                 Automated Deduction (CADE-24) (2013)
10. Beyer, D.: Advances in automatic software verification: SV-               32. Ge, Y., de Moura, L.: Complete instantiation for quantified for-
    COMP 2020. In: Tools and Algorithms for the Construction and                  mulas in satisfiabiliby modulo theories. In: Computer Aided
    Analysis of Systems (TACAS) (2020)                                            Verification (CAV) (2009)
11. Blanchet, B., Cousot, P., Cousot, R., Feret, J., Mauborgne, L.,           33. Gosling, J., Joy, B., Steele, G., Bracha, G.: Java Language Specifi-
    Miné, A., Monniaux, D., Rival, X.: A static analyzer for large                cation, Second Edition: The Java Series, 2nd edn. Addison-Wesley
    safety-critical software. In: Programming Language Design and                 (2000)
    Implementation (PLDI) (2003)                                              34. Goubault, E., Putot, S.: Static analysis of finite precision compu-
12. Boldo, S., Clément, F., Filliâtre, J.C., Mayero, M., Melquiond, G.,           tations. In: Verification, Model Checking, and Abstract Interpreta-
    Weis, P.: Wave equation numerical resolution: A comprehensive                 tion (VMCAI) (2011)
    mechanized proof of a C program. J. Autom. Reason. 50(4) (2013)           35. Goubault, E., Putot, S.: Robustness analysis of finite precision
13. Boldo, S., Filliâtre, J.C., Melquiond, G.: Combining Coq and                  implementations. In: Asian Symposium on Programming Lan-
    Gappa for certifying floating-point programs. In: Intelligent Com-            guages and Systems (APLAS) (2013)
    puter Mathematics (2009)                                                  36. Harel, D., Kozen, D., Tiuryn, J.: Dynamic logic. In: Handbook of
14. Boldo, S., Melquiond, G.: Flocq: A unified library for proving                Philosophical Logic, pp. 99–217. Springer (2001)
    floating-point algorithms in Coq. In: IEEE Symposium on Com-              37. Harrison, J.: Floating point verification in HOL light: the expo-
    puter Arithmetic (ARITH) (2011)                                               nential function. Formal Methods Syst. Des. 16(3) (2000)
15. Brain, M., Schanda, F., Sun, Y.: Building better bit-blasting for         38. IEEE, C.S.: IEEE standard for floating-point arithmetic. IEEE Std
    floating-point problems. In: Tools and Algorithms for the Con-                754-2008 (2008)
    struction and Analysis of Systems (TACAS) (2019)                          39. Izycheva, A., Darulova, E., Seidl, H.: Counterexample and
16. Brain, M., Tinelli, C., Rümmer, P., Wahl, T.: An automatable for-             simulation-guided floating-point loop invariant synthesis. In:
    mal semantics for IEEE-754 floating-point arithmetic. In: IEEE                Static Analysis Symposium (SAS) (2020)
    Symposium on Computer Arithmetic (ARITH) (2015)                           40. Jacobs, B., Smans, J., Philippaerts, P., Vogels, F., Penninckx, W.,
17. Chapman, R., Schanda, F.: Are we there yet? 20 years of industrial            Piessens, F.: VeriFast: A powerful, sound, predictable, fast verifier
    theorem proving with SPARK. In: Interactive Theorem Proving                   for C and java. In: NASA Formal Methods (NFM) (2011)
    (ITP) (2014)                                                              41. Jacobsen, C., Solovyev, A., Gopalakrishnan, G.: A parameterized
18. Chen, L., Miné, A., Cousot, P.: A sound floating-point polyhedra              floating-point formalizaton in HOL Light. Electron. Notes Theo-
    abstract domain. In: Asian Symposium on Programming Lan-                      ret. Comput. Sci. 317 (2015)
    guages and Systems (APLAS) (2008)                                         42. Jeannet, B., Miné, A.: Apron: a library of numerical abstract
19. Chiang, W.F., Gopalakrishnan, G., Rakamaric, Z., Solovyev, A.:                domains for static analysis. In: Computer Aided Verification
    Efficient search for inputs causing high floating-point errors. In:           (CAV) (2009)
    Principles and Practice of Parallel Programming (PPoPP) (2014)            43. Lam, M.O., Hollingsworth, J.K., Stewart, G.W.: dynamic floating-
20. Cimatti, A., Griggio, A., Schaafsma, B., Sebastiani, R.: The Math-            point cancellation detection. Parallel Comput. 39(3) (2013)
    SAT5 SMT solver. In: Tools and Algorithms for the Construction            44. Leavens, G.T., Baker, A.L., Ruby, C.: Preliminary design of JML:
    and Analysis of Systems (TACAS) (2013)                                        A behavioral interface specification language for java. ACM SIG-
21. Cok, D.R.: OpenJML: JML for Java 7 by extending OpenJDK. In:                  SOFT Software Engineering Notes 31(3) (2006)
    NASA Formal Methods (NFM) (2011)                                          45. Leavens, G.T., Cheon, Y.: Design by contract with JML (2006).
22. Cordeiro, L.C., Kesseli, P., Kroening, D., Schrammel, P., Trtík, M.:          http://www.jmlspecs.org/jmldbc.pdf
    JBMC: A bounded model checking tool for verifying java byte-              46. Leino, K.R.M.: This is Boogie 2 (2008). https://www.microsoft.
    code. In: Computer Aided Verification (CAV) (2018)                            com/en-us/research/publication/this-is-boogie-2-2/
23. Cuoq, P., Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J.,         47. Magron, V., Constantinides, G., Donaldson, A.: Certified roundoff
    Yakobowski, B.: Frama-C. In: Software Engineering and Formal                  error bounds using semidefinite programming. ACM Trans. Math.
    Methods (SEFM) (2012)                                                         Softw. 43(4) (2017)
24. Darulova, E., Izycheva, A., Nasir, F., Ritter, F., Becker, H., Bastian,   48. Marché, C., Paulin-Mohring, C., Urbain, X.: The KRAKATOA
    R.: Daisy - framework for analysis and optimization of numeri-                tool for certification of Java/JavaCard programs annotated in JML.
    cal programs. In: Tools and Algorithms for the Construction and               J. Logic Algebraic Programm. 58(1) (2004)
    Analysis of Systems (TACAS) (2018)                                        49. McCormick, J.W., Chapin, P.C.: Building high integrity appli-
25. Darulova, E., Kuncak, V.: Towards a compiler for reals. ACM                   cations with SPARK. Cambridge University Press, Cambridge
    Trans. Program. Lang. Syst. (TOPLAS) 39(2) (2017)                             (2015)
26. De Moura, L., Bjørner, N.: Z3: An efficient SMT solver. In: Tools         50. Meyer, B.: Applying “Design by Contract”. Computer 25(10)
    and Algorithms for the Construction and Analysis of Systems                   (1992)
    (TACAS) (2008)                                                            51. Moscato, M., Titolo, L., Dutle, A., Muñoz, C.: Automatic estima-
27. Eilers, M., Müller, P.: Nagini: A static verifier for python. In: Com-        tion of verified floating-point round-off errors via static analysis.
    puter Aided Verification (CAV) (2018)                                         In: SAFECOMP (2017)
28. Filliâtre, J.C., Paskevich, A.: Why3—where programs meet                  52. Muller, J., Brisebarre, N., de Dinechin, F., Jeannerod, C., Lefèvre,
    provers. In: European Symposium on Programming (ESOP)                         V., Melquiond, G., Revol, N., Stehlé, D., Torres, S.: Handbook of
    (2013)                                                                        Floating-Point Arithmetic. Birkhäuser (2010)
29. Fox, A., Harrison, J., Akbarpour, B.: A formal model                      53. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: a verification
    of IEEE floating point arithmetic. HOL4 Theorem Prover                        infrastructure for permission-based reasoning. In: Verification,
    Library (2017). https://github.com/HOL-Theorem-Prover/HOL/                    Model Checking, and Abstract Interpretation (VMCAI) (2016)
    tree/master/src/floating-point


                                                                                                                                          123
204                                                                                                                             R. Abbasi et al.


54. Pasareanu, C.S., Mehlitz, P.C., Bushnell, D.H., Gundy-Burlet, K.,   58. Solovyev, A., Jacobsen, C., Rakamaric, Z., Gopalakrishnan, G.:
    Lowry, M.R., Person, S., Pape, M.: Combining unit-level symbolic        rigorous estimation of floating-point round-off errors with sym-
    execution and system-level concrete execution for testing NASA          bolic taylor expansions. In: Formal Methods (FM) (2015)
    software. In: International Symposium on Software Testing and
    Analysis (ISSTA) (2008)
55. QF_FP SMT benchmarks. https://clc-gitlab.cs.uiowa.edu:2443/
                                                                        Publisher’s Note Springer Nature remains neutral with regard to juris-
    SMT-LIB-benchmarks/QF_FP (2019)
                                                                        dictional claims in published maps and institutional affiliations.
56. Siegel, S.F., Mironova, A., Avrunin, G.S., Clarke, L.A.: Using
    model checking with symbolic execution to verify parallel numer-
    ical programs. In: International Symposium on Software Testing
    and Analysis (ISSTA) (2006)
57. Slow verification of programs combining multiple floating point
    values (Github issue) (2019 (accessed May 11, 2020)). https://
    github.com/boogie-org/boogie/issues/109




123
