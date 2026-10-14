                                                                            On Sound Compilation of Reals

                                                                     Eva Darulova                                                          Viktor Kuncak
                                                                         EPFL                                                                   EPFL
                                                                  eva.darulova@epfl.ch                                                  viktor.kuncak@epfl.ch




                                        Abstract                                                                         In this paper we advocate a natural but ambitious alternative:
                                        Writing accurate numerical software is hard because of many                  source code programs should be expressed in terms of ideal, math-
arXiv:1309.2511v1 [cs.PL] 10 Sep 2013




                                        sources of unavoidable uncertainties, including finite numerical             ematical real numbers. In our system, the programmer writes a pro-
                                        precision of implementations. We present a programming model                 gram using a Real data type and states the desired postconditions,
                                        where the user writes a program in a real-valued implementation              then specifies uncertainties explicitly in pre- and postconditions as
                                        and specification language that explicitly includes different types          well as the desired target precision on the return values. It is then
                                        of uncertainties. We then present a compilation algorithm that gen-          up to our trustworthy compiler to check, taking into account all un-
                                        erates a conventional implementation that is guaranteed to meet              certainties and their propagation, that the desired precision can be
                                        the desired precision with respect to real numbers. Our verification         soundly realized in a finite precision implemenation. If so, the com-
                                        step generates verification conditions that treat different uncertain-       piler chooses and emits one such finite-precision implementation.
                                        ties in a unified way and encode reasoning about floating-point                  Following this model, we derive verification conditions that en-
                                        roundoff errors into reasoning about real numbers. Such verifica-            code reasoning about floating-point roundoff errors into reason-
                                        tion conditions can be used as a standardized format for verifying           ing about real numbers. Our verification conditions explicitly sep-
                                        the precision and the correctness of numerical programs. Due to              arate the ideal program without external uncertainties and round-
                                        their often non-linear nature, precise reasoning about such verifica-        offs from the actual program, which is actually executed in finite
                                        tion conditions remains difficult. We show that current state-of-the         precision with possibly noisy inputs. Additionally, our constraints
                                        art SMT solvers do not scale well to solving such verification con-          are fully parametric in the floating-point precision and can thus be
                                        ditions. We propose a new procedure that combines exact SMT                  used with different floating-point hardware configurations, as well
                                        solving over reals with approximate and sound affine and interval            as used for determining the minimum precision needed.
                                        arithmetic. We show that this approach overcomes scalability lim-                To summarize, the view of source code as functions over real
                                        itations of SMT solvers while providing improved precision over              numbers has several advantages:
                                        affine and interval arithmetic. Using our initial implementation we           • Programmers can, for the most part, reason in real arithmetic
                                        show the usefullness and effectiveness of our approach on several
                                                                                                                        and not floating-point arithmetic. We thus achieve separation of
                                        examples, including those containing non-linear computation.
                                                                                                                        the design of algorithms (which may still be approximate) from
                                                                                                                        their realization using finite precision computations.
                                                                                                                      • We can verify the ideal meaning of programs using techniques
                                        1.   Introduction                                                               developed to reason over real numbers, which are more scalable
                                        Writing numerical programs is difficult, in part because the pro-               than techniques that directly deal with floating point arithmetic.
                                        grammer needs to deal not only with the correctness of the al-                • The approach allows us to quantify the deviation of implemen-
                                        gorithm but also with unavoidable uncertainties. Program inputs                 tation outputs from ideal ones, instead of merely proving e.g.
                                        may not be exactly known because they come from physical exper-                 range bounds of floating-point variables which is used in sim-
                                        iments or were measured by an embedded sensor. The computa-                     pler static analyses.
                                        tion itself suffers from roundoff errors at each step, because of the
                                        use of finite-precision arithmetic. In addition, resources like energy        • The compiler for reals is free to do optimizations as long as they
                                        may be scarce so that only a certain number of bits are available               preserve the precision requirements. This allows the compiler
                                        for the numerical datatype. At the same time, the computed results              to apply, for example, associativity of arithmetic, or even select
                                        can have far-reaching consequences if used to control, for example,             different approximation schemes for transcendental functions.
                                        a vehicle or a nuclear power plant. It is therefore of great impor-           • In addition to roundoff errors, the approach also allows the
                                        tance to improve confidence in numerical code [34]. One of the first            developer to quantify program behavior in the face of external
                                        challenges in doing this is that most of our automated reasoning                uncertainties such as input measurement errors.
                                        tools work with real arithmetic, whereas the code is implemented in
                                        finite-precision (typically, floating point) arithmetic. Many current            Using our verification condition generation approach, the cor-
                                        approaches to verifying numerical programs start with the floating-          rectness and the precision of compilation for small programs can
                                        point implementation and then try to verify the absense of (runtime)         be directly verified using an SMT solver such as Z3 [16] (see Sec-
                                        errors. However, the absence of errors by itself does not guarantee          tion 5.3); this capability will likely continue to improve as the
                                        that program behavior matches the desired specification expressed            solvers advance. However, the complexity of the generated veri-
                                        using real numbers. Fundamentally, the source code semantics is              fication conditions for larger programs is still out of reach of such
                                        expressed in terms of data types such as floating points. This is            solvers and we believe that specialized techniques are and will con-
                                        further problematic for compiler optimizations, because, e.g., the           tinue to be necessary for this task. This paper presents two special-
                                        associativity law is unsound with respect to such source code se-            ized techniques that improve the feasibility of the verification task.
                                        mantics.                                                                     The first technique performs local approximation and is effective


                                                                                                                 1                                                               2018/10/30
even in benchmarks containing nonlinear arithmetic; the second               different selection of numerical algorithms. To support program-
technique specifically handles conditional expressions.                      ming of larger code fragments our system also supports a modu-
                                                                             lar verification technique, which handles functions through inlining
1.1   Solving Non-Linear Constraints                                         function bodies or using their postconditions. We thus expect that
Nonlinear arithmetic poses a significant challenge for verification          our technique is applicable to larger code bases as well, possibly
because it cannot directly be handled using Simplex-like algorithms          through refactoring code into multiple smaller and annotated func-
embedded inside SMT solvers. Although interesting relevant frag-             tions. Even on the benchmarks that we release, we are aware of no
ments are decidable and are supported by solvers, their complex-             other available system that would provide the same guarantees with
ity is much higher. Unfortunately, non-linear arithmetic is ubiq-            our level of automation.
uitous in numerical software. Furthermore, our verification condi-
tions add roundoff errors to arithmetic expressions, so the resulting        1.4     Summary of Contributions
constraints grow further in complexity, often becoming out of reach          Our overall contribution is an approach for sound compilation of
of solvers. An alternative to encoding into SMT solver input is to           real numbers. Specifically:
use a sound and overapproximating arithmetic model such as in-                • We present a real-valued implementation and specification lan-
terval or affine arithmetic [15]. However, when used by itself on
                                                                                   guage for numerical programs with uncertainties; we define its
non-linear code, these approaches yield too pessimistic results to
                                                                                   semantics in terms of verification constraints that they induce.
be useful.
                                                                                   We believe that such verification conditions can be used as a
    We show that we can combine range arithmetic computation
                                                                                   standardized format for verifying the precision and the correct-
with SMT solving to overcome the limitations of each of the indi-
                                                                                   ness of numerical programs.
vidual techniques when applied to non-linear arithmetic. We obtain
a sound, precise, and somewhat more scalable procedure. During                • We develop an approximation procedure for computing precise
range computation, our technique also checks for common prob-                      range and error bounds for nonlinear expressions which com-
lems such as overflow, division by zero or square root of a negative               bines SMT solving with interval arithmetic. We show that such
number, emitting the corresponding warnings. Additionally, be-                     an approach significantly improves computed range and error
cause the procedure is a forward computation, it is suitable for auto-             bounds compared to standard interval arithmetic, and scales
matically generating function summaries containing output ranges                   better than SMT solving alone. Our procedure can also be used
and errors of a function. From the point of view of the logical                    independently as a more precise alternative to interval arith-
encoding of the problem, range arithmetic becomes a specialized                    metic, and thus can perform forward computation without hav-
method to perform approximate quantifier elimination of bounded                    ing the desired postconditions.
variables that describe the uncertainty.                                      • We describe an approach for soundly computing error bounds
                                                                                   in the presence of branches and uncertainties, which ensures
1.2   Sound Compilation of Conditional Branches
                                                                                   soundness of compilation in case the function defined by a
In the presence of uncertainties, conditional braches become an-                   program is not known to be continuous.
other verification challenge. The challenge is that the ideal execu-          • We have implemented our framework and report our experience
tion may follow one branch, but, because of input or roundoff er-
                                                                                   on a set of diverse benchmarks, including benchmarks from
rors, the actual execution follows another. This behaviour may be
                                                                                   physics, biology, chemistry, and control systems. The results
acceptable, however, if we can show that the error on the output
                                                                                   show that our technique is effective and that it achieves a syn-
remains within required bounds. Therefore, our approach would
                                                                                   ergy of the techniques on which it relies.
directly benefit from automated analysis of continuity, which was
advocated previously [48]. For such continuous functions, our anal-
ysis can be done separately for each program path. In the absence            2.     Example
of knowledge of continuity, we present a new method to check that            We demonstrate some aspects of our system on the example in Fig-
different paths taken by real-valued and floating point versions of          ure 1. The methods triangle and triangleSorted compute the area of
the program still preserves the desired precision specification. Our         a triangle with side lengths a, b and c. The notation a.in(1.0, 9.0)
check does not require continuity (which becomes difficult to prove          is short for 1.0 < a && a < 9.0. We consider a particular applica-
for non-linear code). Instead, it directly checks that the difference        tion where the user may have two side lengths given, and may
between the two values on different branches meets the required              vary the third. She has two functions available to do the compu-
precision. This technique extends our method for handling non-               tation and wants to determine whether either or both satisfy the
linear arithmetic, so it benefits from the combination of range arith-       precision requirement of 1e-11 on line 9. Our tool determines that
metic and SMT solving.                                                       such requirement needs at least double floating point precision; the
                                                                             challenge then is to establish that this precision is sufficient to en-
1.3   Implementation and Evaluation                                          sure these bounds, given that errors in floating code accumulate and
We have implemented our compilation and verification procedure,              grow without an a priori bound.
including the verification condition generation, analysis of possi-              Our tool verifies fully automatically that the method triangleSorted
bly non-linear expressions, and the handling of conditionals. Our            indeed satisfies the postcondition and generates the source code
system is implemented as an extension of a verifier for functional           with the Double datatype which also includes a more precise and
Scala programs. The implementation relies on a range arithmetic              complete postcondition:
implementation for Scala as well as on the Z3 SMT solver.
                                                                                   0.01955760939159717 ≤ res ∧ res ≤ 12.519984025578283 ∧
   We have evaluated the system on a number of diverse bench-                        res +/− 8.578997409317759e−12
marks, obtaining promising results. We are releasing our bench-
marks (and making them available as supplementary material for                   To achieve this result, our tool first checks that the precondition
reviewers). We hope that the benchmarks can be used to com-                  of the function call is satisfied using the Z3 solver. Then, it inlines
pare future tools for error quantification, help the development of          the body of the function triangleSorted and computes a sound bound
nonlinear solvers, and also present challenges for more aggressive           on the result’s uncertainty with our approximation procedure and
compilation schemes, with different number representations and               uses it to show that the postcondition is satisfied. The error compu-


                                                                         2                                                                2018/10/30
   def mainFunction(a: Real, b: Real, c: Real): Real = {
                                                                                  and the user annotates them with pre- and postconditions that ex-
 2     require(4.500005 <= a && a <= 6.5)                                         plicitly talk about uncertainties. Real represents ideal real num-
                                                                                  bers without any uncertainty. We allow arithmetic expressions over
                                                                                                                                               √
 4       val b = 4.0                                                              Reals with the standard arithmetic operators {+, −, ∗, /, }, and
         val c = 8.5                                                              together with conditionals and function calls they form the body
 6       val area = triangleSorted(a, b, c)                                       of methods. Our tool also supports immutable variable declarations
         //val area = triangleUnstable(a, b, c)                                   as val x = .... This language allows the user to define a computation
 8       area                                                                     over real numbers. Note that this specification language is not exe-
       } ensuring(res => res +/− 1e−11)
                                                                                  cutable.
10
       def triangle(a: Real, b: Real, c: Real): Real = {                              The precondition allows the user to provide a specification of
12       require(a.in(1.0, 9.0) && b.in(1.0, 9.0) && c.in(1.0, 9.0) &&            the environment. A complete environment specification consists of
            a + b > c + 1e−6 && a + c > b + 1e−6 && b + c > a + 1e−6)             lower and upper bounds for all method parameters and an upper
14                                                                                bound on the uncertainty or noise. Range bounds are expressed
           val s = (a + b + c)/2.0                                                with regular comparison operators. Uncertainty is expressed with
16         sqrt(s ∗ (s − a) ∗ (s − b) ∗ (s − c))                                  the predicate such as x +/− 1e−6, which denotes that the variable
       }                                                                          x is only known up to 1e − 6. Alternatively, the programmer can
18
                                                                                  specify the relative error as x +/− 1e−7 ∗ x. If no noise except for
       def triangleSorted(a: Real, b: Real, c: Real): Real = {
                                                                                  roundoff is present, roundoff errors are automatically added to
20       require(a.in(1.0, 9.0) && b.in(1.0, 9.0) && c.in(1.0, 9.0) &&
            a + b > c + 1e−6 && a + c > b + 1e−6 && b + c > a + 1e−6 &&           input variables.
22          a < c && b < c)                                                           The postcondition can specify the range and the maximum un-
                                                                                  certainty accepted on the output. In addition to the language al-
24         if (a < b) {                                                           lowed in the precondition, the postcondition may reference the er-
              sqrt((c+(b+a)) ∗ (a−(c−b)) ∗ (a+(c−b)) ∗ (c+(b−a)))/4.0             rors on inputs directly in the following way: res +/− 3.5 ∗ !x, which
26         } else {                                                               says that the maximum acceptable error on the output variable res
              sqrt((c+(a+b)) ∗ (b−(c−a)) ∗ (b+(c−a)) ∗ (c+(a−b))) / 4.0           is bounded from above by 3.5 times the initial error on x. Whereas
28         }                                                                      the precondition may only talk about the ideal values, the postcon-
       }
                                                                                  dition can also reference the actual value directly via ∼x. This al-
                                                                                  lows us to assert that runtime values will not exceed a certain range,
                   Figure 1. Computing the area of a triangle.
                                                                                  for instance.
                                                                                  Floating-point arithmetic Our tool and technique support in the
     tation takes into account in a sound way the input uncertainty (here         generated target code any floating-point precision and in partic-
     an initial roundoff error on the inputs), its propagation and roundoff       ular, single and double floating-point precision as defined by the
     errors commited at each arithmetic operation. Additionally, due to           IEEE 754 floating-point standard [46]. It is also straightforward to
     the initial roundoff error the comparison on line 24 is not exact, so        combine it with techniques to generate fixed-point arithmetic [13],
     that some floating-point computations will take a different branch           which similarly relies on knowing ranges of variables. We assume
     than their corresponding real-valued computation. More precisely,            rounding-to-nearest rounding mode and that basic arithmetic oper-
     the total error when computing the condition is 7.22e − 16, as                                   √
                                                                                  ations {+, −, ∗, /, } are rounded correctly, which means that the
     computed by our tool. That is, floating-point values that satisfy            result from any such operation must be the closest representable
     a < b + 7.22e − 16 may take the else branch, even though the                 floating-point number. Hence, provided there is no overflow, the
     corresponding real values would follow the then branch, and simi-            result of a binary operation ◦F satisfies
     larly in the opposite direction. Our tool verifies that the difference
     in the computed result in two branches, due to this divergence be-                x ◦F y = (x ◦R y)(1 + δ), |δ| ≤ M , ◦ ∈ {+, −, ∗, /}        (1)
     tween real arithmetic and floating point arithmetic code, remains            where ◦R is the ideal operation in real numbers and M is the
     within the precision requirement.                                            machine epsilon that determines the upper bound on the relative
         Finally, our tool uses our novel range computation procedure             error. This model provides a basis for our roundoff error estimates.
     to also compute a more precise output range than we could have
     obtained in interval arithmetic. It then includes this more com-
     plete postcondition in the generated floating-point code. In fact, in-
                                                                                  4.     Compiling Reals to Finite Precision
     terval arithmetic alone computes the ranges [0.0138, 16.163] and             Given a specification or program over reals and a possible target
     [0.0169, 14.457] for using the methods triangle and triangleSorted           floating-point precision, our tool generates code over floating-point
     respectively, seemingly suggesting that two methods perform en-              numbers that satisfy the given pre- and postconditions. Figure 2
     tirely different computations. With our technique, the tool com-             presents a high-level view of our compilation algorithm. Our tool
     putes the same range [0.0195, 12.52] for both methods, but shows a           first analyses the entire specification and generates one verification
     difference in the absolute error of the computation. For the method          condition for each postcondition to be proven. To obtain a modular
     triangle, the verification fails, as desired, because the computed er-       algorithm, the tool also generates verification conditions that check
     ror (2.3e − 11) exceeds the required precision bound. This result            that at each function call the precondition of the called function
     is expected—the textbook formula for triangles is known to suffer            is satisfied. The methods are then sorted by occuring function
     from imprecision for flat triangles [31], which is somewhat rectified        calls. This allows us to re-use already computed postconditions
     in the method triangleSorted.                                                of function calls in a modular analysis. If the user specified a
                                                                                  target precision, the remaining part of the compilation process is
                                                                                  perfomed with respect to this precision, if not or in the case the
     3.     Programs with Reals                                                   user specified several possible precisions, our tool will iteratively
     Each program to be compiled consists of one top-level object with            select the next more precise precision and attempt to compile the
     methods written in a functional subset of the Scala programming              entire program. If compilation fails due to unsatisfied assertions,
     language [41]. All methods are functions over the Real datatype              the next precision is selected. Thus, one task of our algorithm is to


                                                                              3                                                               2018/10/30
Input: spec: specification over Reals, prec: candidate precisions              a <= x && x <= b    x ∈ [a, b]
for fnc ← spec.fncs                                                            x +/− k             x◦ = x + errx ∧ errx ∈ [−k, k]
  fnc.vcs = generateVCs(fnc)                                                   x +/− m ∗ x         x◦ = x + errx ∧ errx ∈ [−|mx|, |mx|]
                                                                               ∼x                  x◦
spec.fncs.sortBy((f1, f2) => f1 ⊆ f2.fncCalls)
                                                                               !x                  errx
while prec 6= ∅ and notProven(spec.fncs)                                       xy                 (x  y) ∧ (x◦  y◦ )(1 + δ1 )
  precision = prec.nextPrecise                                                 sqrt(x)             sqrt(x) ∧ sqrt(x◦ )(1 + δ2 )
  for fnc ← spec.fncs
    for vc ← fnc.vcs                                                           val z = x           z = x ∧ z◦ = x◦
       while vc.hasNextApproximation ∧ notProven(vc)                           if (c(x)) e1(x)     ((c(x) ∧ e1(x)) ∨ (¬c(x) ∧ e2(x)))∧
         approx = getNextApproximation(vc, precision)                          else e2(x)          ((c◦ (x◦ ) ∧ e1◦ (x◦ )) ∨ (¬c◦ (x◦ ) ∧ e2◦ (x◦ )))
         vc.status = checkWithZ3(approx)
  generateSpec(fnc)                                                            g(x)                g(x) ∧ g◦ (x◦ )
generateCode(spec)                                                                                       ∈ {+, −, ∗, /}
                                                                                               −m ≤ δi ∧ δi ≤ m , all δ are fresh
Output: floating−point code with generated postconditions
                                                                                  cond◦ and e◦ denote functions with roundoff errors at each step
                 Figure 2. Compilation algorithm.
                                                                                      Table 1. Semantics of our specification language.

automatically determine the necessary least floating-point precision
to ensure the specification is met. Currently, each precision iteration       where ~ x, res,
                                                                                          ~ ~ y denote the input, output and local variables respec-
is computed separately, which is not a big issue due to a small               tively.
number alternative floating-point targets. We did identify certain                Table 1 summarizes how verification constraints are generated
shared computations between iterations; we can exploit them in the            from our specification language. Each variable x in the specification
future for more efficient compilation. In order for the compilation           corresponds to two real-valued variables x, x◦ , the ideal one in the
process to succeed, the specification has to be met with respect              absence of uncertainties and roundoff errors and the actual one,
to a given floating-point precision, thus the principal part of our           computed by the compiled program. Note that the ideal and actual
algorithm is spent in verification, which we describe in Section 5.           variables are related only through the error bounds in the pre- and
    We envision that in the future the compilation task will also             postconditions, which allows for the ideal and actual executions to
include automatic precision-preserving code optimizations, but in             take different paths.
this paper we concentrate on the challenging groundwork of veri-                  In the method body we have to take into account roundoff
fying the precision of code.                                                  errors from arithmetic operations and the propagation of existing
                                                                                                                                                √
    Our tool currently generates Scala code over single, dou-                 errors. Our system currently supports operations {+, −, ∗, /, },
ble, double-double and quad-double floating-point arithmetic. For             but these can be in principle extended to elementary functions, for
double-double and quad-double precision, which were imple-                    instance by encoding them via Taylor expansions [37].
mented in software by [3], we provide a Scala interface with the                  Note that the resulting verification conditions are parametric in
generated code. In case the verification part of compilation fails,           the machine epsilon.
we nonetheless generate code (together with a failure report) with
the best postconditions our tool was able to compute. The user can            5.2   Specification Generation
then use the generated specifications to gain insight why and where           In order to give feedback to developers and to facilitate automatic
her program does not satify requirements.                                     modular analysis, our tool also provides automatic specification
    Our techniques are not restricted to these floating-point preci-          generation. By this we mean that the programmer still needs to
sions, however, and will work for any precision that follows the              provide the environment specification in form of preconditions, but
abstraction given in Equation (1). Furthermore, while we have im-             our tool automatically computes a precise postcondition.
plemented our tool to accept specifications in a domain specific lan-            Formally, we can rewrite the constraint (*) as
guage embedded in Scala and generate code in Scala, all our tech-
niques apply equally to all programming languages and hardware                      ∀~
                                                                                     x, res. (∃~      x) ∧ body(~
                                                                                               y . P (~            y , res)) → Q(~
                                                                                                                x, ~             x, res)
that follow the floating-point abstraction we assume (Equation 1).
                                                                              where Q is now unknown. We obtain the most precise post-
                                                                              condition Q by applying quantifier elimination (QE) to P (~     x) ∧
5.    Verifying Real Programs                                                 body(~x, ~
                                                                                       y , res) and eliminate ~
                                                                                                              y . The theory of arithmetic over re-
                                                                              als admits QE so it is theoretically possible to use this approach.
We will now describe the verification part of our compilation al-
                                                                              We do not currently use a full QE procedure for specification gen-
gorithm. In the following we will call the ideal computation the
                                                                              eration, as it is expensive and it is not clear whether the returned
computation in the absence of any uncertainties and implemented
                                                                              expressions would be of a suitable format. Instead, we use our ap-
in a real arithmetic, and the actual computation the computation
                                                                              proximation approach which computes ranges and maximum errors
that will finally be executed in finite-precision and with potentially
                                                                              in a forward fashion and allows us to compute an (over) approxi-
uncertain inputs.
                                                                              mation of a postcondition of the form res ∈ [a, b] ∧ res ± u.
5.1   Verification Conditions for Loop-Free Programs
                                                                              5.3   Difficulty of Simple Encoding into SMT solvers
Each method with its precondition P and postcondition Q implies
the following verification condition:                                         For small functions we can already prove interesting properties by
                                                                              using the exact encoding of the problem just described and dis-
        ∀~x, res,
              ~ ~        x) ∧ body(~
                  y . P (~         x, ~    ~ → Q(~
                                      y , res)   x, res)
                                                     ~             (*)        charging the verification constraints with Z3. Consider the follow-


                                                                          4                                                               2018/10/30
                                                                                  approximation pipeline. We support inlining of both user-provided
      def getNextApproximation(vc, precision):
                                                                                  postconditions and postconditions computed by our own specifi-
                                                                                  cation generation procedure. If this still is not precise enough, we
                                                            getRange!
                                   getPathError!          evalWithError!          inline the entire function body.
      inlining postcondition                                                          Postcondition inlining is implemented by replacing the function
                                    path-wise             approx. error
      inlining full function                                                      call with a fresh variable and constraining it with the postcondi-
                                     merging          approx. error & range       tion. Thus, if verification suceeds with inlining the postcondition,
           functions                  paths               arithmetic              we avoid having to consider each path of the inlined function sep-
                                                                                  arately and can perform modular verification avoiding a potential
                                first approximation
                                                                                  path explosion problem. Such modular verification is not feasible
                                                                                  when postconditions are too imprecise and we plan to explore the
                       Figure 3. Approximation pipeline.                          generation of more precise postconditions in the future. One step
                                                                                  in this direction is to allow postconditions that are parametric in
ing code a programmer may write to implement the third B-spline                   the initial errors, for example with the operator !x introduced in
basic function which is commonly used in signal processing [29].                  Section 3. While our tool currently supports postcondition inlining
                                                                                  with such postconditions, we do not yet generate these automati-
  def bspline3(u: Real): Real = {                                                 cally.
    require(0 ≤ u && u ≤ 1 && u ± 1e−13)
    −u∗u∗u / 6.0                                                                  Arithmetic The arithmetic part of the verification constraints gen-
  } ensuring (res ≥ −0.17 ≤ res && res ≤ 0.05 && res ± 1e−11)                     erated by Table 1 can be essentially divided into the ideal part and
                                                                                  the actual part, which includes roundoff errors at each computation
Functions and the correspoding verification conditions of this com-               step. The ideal part determines whether the ideal range constraints
plexity are already within the possibilities of the nonlinear solver              in the postcondition are satisfied and the actual part determines
within Z3. For more complex functions however, Z3 does not                        whether the uncertainty part of the postcondition is satisfied. We
(yet) provide an answer in a reasonable time, or returns unknown.                 can use our procedure presented in Section 6 to compute a sound
Whether alternative techniques in SMT solvers can help in such                    approximation of both the result’s range as well as its uncertainty.
cases remains to be seen [7, 30]. We here provide an approach                     Based on this, our tool constructs two approximations. For the first,
based on step-wise approximation that addresses the difficulty of                 the ideal part of the constraint is left untouched and the actual part
general-purpose constraint solving.                                               is replaced by the computed uncertainty bound. This effectively re-
5.4    Verification with Approximations                                           moves a large number of variables and many times suffiently sim-
                                                                                  plifies the constraint for Z3 to succeed. If this fails, our tool addi-
In order to nontheless verify interesting programs, we have de-                   tionally replaces the ideal part by the computed range constraint.
veloped an approximation procedure that computes a sound over-                    Note that the second approximation may not have enough informa-
approximation of the range of an expression and of the uncertainty                tion to prove a more complex postconditions, as correlation infor-
on the output. This procedure is a forward computation and we                     mation is lost. We note that the computation of ranges and errors
also use it to generate specifications automatically. We describe the             is the same for both approximations and thus trying both does not
approximation procedure in detail in Section 6, for now we will as-               affect efficiency significantly.
sume that it exists and, given a precondition P and an expression
expr, computes a sound bound on the output range and its associ-                  Paths In the case of several paths through the program, we have
ated uncertainty:                                                                 the option to consider each path separately or to merge results at
                                                                                  each join in the control flow graph. This introduces a tradeoff be-
([a, b], err) = evalWithError(P, expr) ⇔                                          tween efficiency and precision, since on one hand, considering each
∀~                       x, x~◦ ) ∧ res = expr(~
  x, x~◦ , res, res◦ .P (~                     x) ∧ res◦ = expr◦ (x~◦ )           path separately leads to an exponential number of paths to consider.
                                                                                  On the other hand, merging at each join looses correlation informa-
→ ¬(res < a ∨ b < res) ∧ |res − res◦ | < err
                                                                                  tion between variables which may be necessary to prove certain
    We have identified three possibiities for approximation: nonlin-              properties. Our approximation pipeline chooses merging first, be-
ear arithmetic, function calls, and paths and each can be approxi-                fore resorting to a path-by-path verification in case of failure. We
mated at different levels. We have observed in our experiments, that              believe that other techniques for exploring the path space could also
“one size does not fit all” and a combination of different approxi-               be integrated into our tool [9, 32]. Another possible improvement
mations is most successful in proving the verification conditions we              are heuristics that select a different order of approximations de-
encountered. For each verification condition we thus construct ap-                pending on particular characteristics of the verification condition.
proximations until Z3 is able to prove one, or until we run out of ap-
proximations where we report the verification as failed. We can thus              Example We illustrate the verification algorithm on the exam-
view verification as a stream of approximations to be proven. We il-              ple in Figure 4. The functions sineTaylor and sineOrder3 are veri-
lustrate the pipeline that computes the different approximations in               fied first since they do not contain function calls. Verification with
Figure 3. The routines getPathError, getRange and evalWithError are               the full verification constraint fails. Next, our tool computes the er-
described in the following sections in more detail.                               rors on the output and Z3 suceeds to prove the resulting constraint
    The first approximation (indicated by the long arrow in Fig-                  with the ideal part untouched. From this approximation our tool
ure 3) is to use Z3 alone on the entire constraint constructed by the             directly computes a new, more precise postcondition, in particular
rules in Table 1. This is indeed an approximation, as all function                it can narrow the resulting error to 1.63e-15. Next, our tool con-
calls are treated as uninterpreted functions in this case. As noted               siders the comparison function. Inlining only the postcondition is
before, this approach only works in very simple cases or when no                  not enough in this case, but computing the error approximation on
uncertainties and no functions are present.                                       the inlined functions suceeds in verifying the postcondition. Z3 is
                                                                                  again able to verify the real-valued portion independently. Finally,
Function calls If the verification constraint contains function                   the tool verifies that the preconditions of the function calls are satis-
calls and the first approximation failed, our tool will attempt to in-            fied by using Z3 alone. Verification of the function comparisonInvalid
line postconditions and pass on the resulting constraint down the                 fails with all approximations so that our tool reports unknown. It also


                                                                              5                                                                  2018/10/30
                                                                               sents possible values of variables as affine forms
def comparisonValid(x: Real): Real = {                                                                               n
                                                                                                                     X
  require(−2.0 < x && x < 2.0)                                                                           x̂ = x0 +         xi i
  val z1 = sineTaylor(x)                                                                                             i=1
  val z2 = sineOrder3(x)
  z1 − z2                                                                      where x0 denotes the central value (of the represented interval) and
} ensuring(res => ∼res <= 0.1)                                                 each noise symbol i is a formal variable denoting a deviation from
                                                                               the central value, intended to range over [−1, 1]. The maximum
def comparisonInvalid(x: Real): Real = {                                       magnitude of each noise term is given by the corresponding xi .
  require(−2.0 < x && x < 2.0)                                                 Note that the sign of xi does not matter in isolation, it does, how-
  val z1 = sineTaylor(x)                                                       ever, reflect the relative dependence between values. For example,
  val z2 = sineOrder3(x)                                                       take x = x0 + x1 1 , then
  z1 − z2
} ensuring(res => ∼res <= 0.01) // counterexample: 1.0                                         x − x = x0 + x1 1 − (x0 + x1 1 )
                                                                                                      = x0 − x0 + x1 1 − x1 1 = 0
def sineTaylor(x: Real): Real = {
  require(−2.0 < x && x < 2.0)                                                 If we subtracted x = x0 −x1 1 instead, the resulting interval would
  x − (x∗x∗x)/6.0 + (x∗x∗x∗x∗x)/120.0 − (x∗x∗x∗x∗x∗x∗x)/5040.0                 have width 2 ∗ x1 and not zero.
} ensuring(res => −1.0 < res && res < 1.0 && res +/− 1e−14)                        The range represented by an affine form is computed as
                                                                                                                                                n
def sineOrder3(x: Real): Real = {                                                                                                               X
  require(−2.0 < x && x < 2.0)                                                       [x̂] = [x0 − rad(x̂), x0 + rad(x̂)],           rad(x̂) =         |xi |
  0.954929658551372 ∗ x − 0.12900613773279798∗(x∗x∗x)                                                                                           i=1
} ensuring(res => −1.0 < res && res < 1.0 && res +/− 1e−14)
                                                                               A general affine operation αx̂ + β ŷ + ζ consists of addition, sub-
                                                                               traction, addition of a constant (ζ) or multiplication by a constant
      Figure 4. Different polynomial approximations of sine.
                                                                               (α, β). Expanding the affine forms x̂ and ŷ we get
                                                                                                                                   n
                                                                                                                                   X
                                                                                      αx̂ + β ŷ + ζ = (αx0 + βy0 + ζ) +             (αxi + βyi )i
provides the counterexample it obtains from Z3 (x = 1.0), which                                                                    i=1
in this case is a valid counterexample.
                                                                               An additional motivation for using affine arithmetic is that differ-
                                                                               ent contributions to the range it represents remain, at least partly,
5.5   Soundness
                                                                               separated. This information can be used for instance to help iden-
Our procedure is sound because our constraints overapproximate                 tify the major contributor of a result’s uncertainty or to separate
the actual errors. Furthemore, even in the full constraint as gener-           contributions from external uncertainties from roundoff errors.
ated from Table 1, roundoff errors are overapproximated since we
assume the worst-case error bound at each step. While this ensures             6.1     Range Computation
soundness, it also introduces incompleteness, as we may fail to val-           The goal of this procedure is to perform a forward-computation to
idate a specification because our overapproximation is too large.              determine the real-valued range of a nonlinear arithmetic expres-
This implies that counterexamples reported by Z3 are in general                sion given ranges for its inputs. Two common possibilities are in-
only valid, if they disprove the ideal real-valued part of the verifica-       terval and affine arithmetic, but they tend to overapproximate the
tion constraint. In general, this is easy to distinguish from the case         resulting range, especially if the input intervals are not sufficiently
where verification fails due to too large error bounds, as Z3 prefers          small (order 1). Affine arithmetic improves over interval arithmetic
simpler counterexamples over complex ones and thus chooses all                 somewhat by tracking linear correlations, but in the case of non-
error variables to be zero if the ideal part is being violated.                linear expressions the results can become actually worse than for
                                                                               interval arithmetic.
6.    Solving Nonlinear Constraints                                            Observation: A nonlinear theorem prover such as the one that
Having given an overview of the approximation pipeline, we now                 comes with Z3 can decide with relatively good precision whether
describe the computation of the approximation for nonlinear arith-             a given bound is sound or not. That is we can check with a prover
metic, which corresponds to the last box in Figure 3. For complete-            whether for an expression e the range [a, b] is a sound interval en-
ness of presentation, we first review interval and affine arithmetic           closure. This observation is the basis of our range computation.
which are common choices for performing sound arithmetic com-
putations and which we also use as part of our technique. We then                  The input to our algorithm is a nonlinear expression expr and a
present our novel procedure for computing the output range of a                precondition P on its inputs, which specifies, among possibly other
nonlinear expression given ranges for its inputs that can be a more            constraints, ranges on all input variables ~
                                                                                                                          x. The output is an interval
precise substitute for interval or affine arithmetic. Finally, we con-         [a, b] which satisfies the following:
tinue with a procedure that computes a sound overapproximation                  [a, b] = getRange(P, expr) ⇔
of the uncertainty on the result of a nonlinear expression.
    One possibility to perform guaranteed computations is to use                      ∀~         x) ∧ res = expr(~
                                                                                       x, res.P (~               x) → ¬(res < a ∨ b < res)
standard interval arithmetic [39]. Interval arithmetic computes a              The algorithm for computing the lower bound of a range is given
bounding interval for each basic operation as                                  in Figure 5. The computation for the upper bound is symmetric. For
      x ◦ y = [min(x ◦ y), max(x ◦ y)]          ◦ ∈ {+, −, ∗, /}               each range to be computed, our tool first computes an initial sound
                                                                               estimate of the range with interval arithmetic. It then performs an
and analogously for square root. Affine arithmetic was originally              initial quick check to test whether the computed first approximation
introduced in [15] and addresses the difficulty of interval arithmetic         bounds are already tight. If not, it uses the first approximation as the
in handling correlations between variables. Affine arithmetic repre-           starting point and then narrows down the lower and upper bounds


                                                                           6                                                                     2018/10/30
                                                                               other additional constraints on the ideal variables. The uncertainty
def getRange(expr, precondition, precision, maxIterations):
                                                                               specification is necessary, as it related the ideal and actual variables.
  z3.assertConstraint(precondition)
                                                                                   The idea of our procedure is to “execute” a computation while
  [aInit, bInit] = evalInterval(expr, precondition.ranges);
                                                                               keeping track of the output range of the current expression and
                                                                               its associated errors. At each arithmetic operation, we propagate
  //lower bound
                                                                               existing errors, compute an upper bound on the roundoff error
  if z3.checkSat(expr a + precision) == UNSAT
                                                                               and add it to the overall errors. Since the roundoff error depends
     a = aInit
                                                                               proportionally on the range of values, we also need to keep track of
     b = bInit
                                                                               the ranges as precisely as possible.
     numIterations = 0
                                                                                   Our procedure is build on the abstraction that a computation is
     while (b−a) < precision ∧ numIterations < maxIterations
                                                                               an ideal computation plus or minus some uncertainty. The abstrac-
       mid = a + (b − a) / 2
                                                                               tion of floating-point roundoff errors that we chose also follows this
       numIterations++
                                                                               separation:
       z3.checkSat(expr mid) match
         case SAT ⇒ b = mid                                                             f l(x  y) = (x  y)(1 + δ) = (x  y) + (x  y)δ
         case UNSAT ⇒ a = mid
                                                                               for δ ∈ [−m , m ] and  ∈ {+, −, ∗, /}. This allows us to treat all
         case Unknown ⇒ break
                                                                               uncertainties in a unified manner.
     aNew = a
                                                                                   Our procedure builds on the idea of the SmartFloat datatype [12],
  else
                                                                               which uses affine arithmetic to track both the range and the errors.
     aNew = aInit
                                                                               For nonlinear operations, however, the so computed ranges become
                                                                               very pessimistic quickly and the error computation may also suffer
  bNew = ... //upper bound symmetrically
                                                                               from this imprecision. We observed that since the errors tend to be
  return: [aNew, bNew]
                                                                               relatively small, this imprecision does not affect the error propaga-
                                                                               tion itself to such an extent. If the initial errors are small (less than
 Figure 5. Algorithm for computing the range of an expression.
                                                                               one), multiplied nonlinear terms tend to be even smaller, whereas
                                                                               if the affine terms are larger than one, the nonlinear terms grow. We
                                                                               thus concentrate on improving the ideal range of values and use our
using a binary search. At each step of the binary search our tool              novel range computation procedure for this part and leave the error
uses Z3 to confirm or reject the newly proposed bound.                         propagation with affine arithmetic as in [12].
    The search stops when either Z3 fails, i.e. returns unknown for                In our adaptation, we represent every variable and intermediate
a query or cannot answer within a given timeout, the difference                computation result as a datatype with the following components:
between subsequent bounds is smaller than a precision threshold,
or the maximum number of iterations is reached. This stopping                             x : (range : Interval, err
                                                                                                                  ˆ : Af f ineF orm)
criterion can be set dynamically.                                              where range is the range of this variable, computed as described in
Additional constraints In addition to the input ranges, the pre-               Section 6.1 and errˆ is the affine form representing the errors. The
condition may also contain further constraints on the variables. For           (overapproximation) of the actual range including all uncertainties
example consider again the method triangle in Figure 1. The pre-               is then given by totalRange = range + [err], ˆ where err ˆ denotes
condition bounds the inputs as a, b, c ∈ [1, 9], but the formula is            the interval represented by the affine form.
useful only for valid triangles, i.e. when every two sides together            Roundoff error computation         Roundoff errors are computed at
are longer than the third. If not, we will get an error at the lat-            each computation step as
est when we try to take the square root of a negative number. In
interval-based approaches we can only consider input intervals that                              ρ = δ ∗ maxAbs(totalRange)
satisfy this constraint for all values, and thus have to check sev-            where δ is the machine epsilon, and added to errˆ as a fresh noise
eral (and possibly many) cases. In our approach, since we are using            term. Note that this roundoff error computation makes our error
Z3 to check the soundness of bounds, we can assert the additional              computation parametric in the floating-point precision.
constraints up-front and then all subsequent checks are performed
with respect to all additional and initial contraints. This allows us to       Error propagation For affine operations addition, subtraction,
avoid interval subdivisions due to imprecisions or problem specific            and multiplication by a constant factor the propagated errors are
constraints such as those in the triangle example. This becomes es-            computed term-wise and thus as for standard affine arithmetic. We
pecially valuable in the presence of multiple variables, where we              refer the reader to [12, 15] for further details and describe here
may need an exponential number of subdivisions.                                only the propagation for nonlinear arithmetic. For multiplication,
                                                                               division and square root, the magnitude of errors also depends
6.2   Error Approximation                                                      on the ranges of variables. Since our ranges are not affine terms
                                                                               themselves, propagation has to be adjusted. In the following, we
We now describe our approximation procedure which, for a given
                                                                               denote the range of a variable x by [x] and its associated error by
expression expr and a precondition P on the inputs, computes
                                                                               the affine form errˆ x . When we write [x] ∗ err
                                                                                                                             ˆ y we mean that the
the range and error on the output. More formally, our procedure
                                                                               interval [x] is converted into an affine form and the multiplication
satisfies the following:
                                                                               is performed in affine arithmetic.
([a, b], err) = evalWithError(P, expr) ⇔                                           Multiplication is computed as
∀~                       x, x~◦ ) ∧ res = expr(~
  x, x~◦ , res, res◦ .P (~                     x) ∧ res◦ = expr◦ (x~◦ )         x ∗ y = ([x] + err
                                                                                                ˆ x )([y] + err
                                                                                                             ˆ y)
→ ¬(res < a ∨ b < res) ∧ |res − res◦ | < err                                           = [x] ∗ [y] + [x] ∗ err
                                                                                                            ˆ y + [y] ∗ err     ˆ x ∗ err
                                                                                                                         ˆ x + err     ˆy +ρ
where expr◦ represents the expression evaluated in floating-point              where ρ is the new roundoff error. Thus the first term contributes
arithmetic and ~x, x~◦ are the ideal and actual variables. The precon-         to the ideal range and the remaining three to the error affine form.
dition specifies the ranges and uncertainties of initial variables and         The larger the factors [x] and [y] are, the larger the finally computed


                                                                           7                                                                  2018/10/30
errors will be. In order to keep the overapproximation as small as
                                                                               def getPathError:
possible, we evaluate [x] and [y] with our new range computation.
                                                                             2 Input: pre (x ∈ [a, b] ∧ x ± n)
    Division is computed as
                                                                                      program (if (cond(x) < 0) f1(x) else f2(x))
   x         1                                                               4   val pathError1 = computePathError(pre, cond, f1, f2)
     = x ∗ = ([x] + err    ˆ x )([1/y] + errˆ1/y )
   y        y                                                                    val pathError2 = computePathError(pre, ¬ cond, f2, f1)
               1                    1                                        6   return max (pathError1, pathError2)
     = [x] ∗ [ ] + [x] ∗ errˆ 1 + [ ] ∗ err
                                          ˆ x + errˆ x ∗ err
                                                           ˆ1 +ρ
               y              y     y                        y
                                                                             8  def computePathError(pre, c, f1, f2):
For square root, we first compute an affine approximation of square               ([c], errc ) = evalWithError(pre, c)
root as in [12]                                                                   ([f2]f loat , errf loat ) =
                        √                                                    10
                           x=α∗x+ζ +θ                                                evalWithError(pre ∧ c(x) ∈ [0, errc ], f2)
and then perform the affine multiplication term wise.                        12   [f1]real =
                                                                                     getRange(pre ∧ c(x) ∈ [−errc , 0], f1)
Overflows and NaN Our procedure allows us to detect potential                14   return: max |[f1]real − ([f2]f loat + errf loat )|
overflows, division by zero and square root of a negative value, as
our tool computes ranges of all intermediate values. We currently                        Figure 6. Computing error due to diverging paths.
report these issues as warnings to the user.

6.3   Limitations                                                                conditional of the form c(x) == 0 would yield different results
The limitation of this approach is clearly the ability of Z3 to check            for the ideal and actual computation for nearly any input, so we do
our constraints. We found its capabilities satisfactory, although we             not allow it in our specification language.
expect the performance to still significantly improve. To emphasize                  The actual computation commits a certain error when comput-
the difference to the constraints that are defined by Table 1, the               ing the condition of the branch and it is this error that causes some
constraints we use here do not add errors at each step and thus                  executions to follow a different branch than the corresponding ideal
the number of variables is reduced significantly. We also found                  one would. Consider the case where the ideal computation evalu-
several transformations helpful, such as rewriting powers (e.g. x ∗              ates f1, but the actual one evaluates f2. Algorithm 6 gives the com-
x ∗ x to x3 ), multiplying out products and avoiding non-strict                  putation of the path error in this case. The idea is to compute the
comparisons in the precondition, although the benefits were not                  ranges of f1 and f2, but only for the inputs that could be diverg-
entirely consistent. Note that at each step of our error computation,            ing. The final error is then the maximum difference of these value.
our tool computes the current range. Thus, even if Z3 fails to tighten           The algorithm extends naturally to several variables. In the case of
the bound for some expressions, we still compute more precise                    several paths through the program, this error has to be, in princi-
bounds than interval arithmetic overall in most cases, as the ranges             ple, computed for each combination of paths. We use Z3 to rule out
of the remaining subexpressions have already been computed more                  infeasible paths up front so that the path error computation is only
precisely.                                                                       performed for those paths that are actually feasible.
                                                                                     We have currently implemented this approach in our tool for
                                                                                 the case when we use merging to handle paths in order to avoid
7.    Conditional Statements                                                     having to consider an exponential number of path combinations.
In this Section we consider the difference between the ideal and                 We also use a higher default precision and number of iterations
actual computation due to uncertainties on computing branch con-                 threshold during the binary search in the range computation as this
ditions and the resulting different paths taken. We note that the                computation requires in general very tight intervals for each path.
full constraint constructed according to Section 3 automatically in-                 We identify two challenges for performing this computation:
cludes this error. Recall that the ideal and actual computations are             1. As soon as the program has multiple variables, the inputs for the
independent except for the initial conditions, so that it is possible               different branches are not two-dimensional intervals anymore,
that they follow different paths through the program.                               which makes an accurate evaluation of the individual paths
    In the case of approximation, however, we compute the error                     difficult in standard interval arithmetic.
on individual paths and have to consider the error due to diverging
paths separately. If a method encodes a continous function in the                2. The inputs for the two branches are inter-dependent. Thus,
usual mathematical sense then we note that we only need to quan-                    simply evaluating the two branches with inputs that are in the
tify errors for each path separately. Thus, if have a method [9] to                 correct ranges, but are not correlated, yields pessimistic results
determine whether a function with conditional statements is con-                    when computing the final difference (line 16).
tinuous, then our approach described so far is sufficient to provide                 We overcome the first challenge with our range computation
sound error bounds. For the case where such a procedure does not                 which takes into account additional constraints. For the second
exist or fails to provide an answer, for example due to nonlinear-               challenge, we use our range computation as well, however unfortu-
ity, or the function simply is not continuous, we propose the fol-               nately Z3 fails to tighten the final range to a satisfactory precision
lowing algorithm to explicitly compute the difference between the                due to timeouts. We still obtain much better error estimates than
ideal and the actual computation across paths. Note that we do not               with interval arithmetic alone, as the ranges of values for the indi-
assume continuity, i.e. the algorithm allows us to compute error                 vidual paths are already computed much more precisely. We report
bounds even in the case on non-continous functions.                              in Section 8 on the type of programs whose verification is already
    For simplicity, we present here the algorithm for the case of one            in our reach today.
conditional statement:
                    if (c(x) < 0) f1(x)                                          8.   Experiments
                    else f2(x)
                                                                                 The examples in Figure 1 and 4 and Section 5.3 provide an idea
It generalizes readily to more complex expressions. W.l.o.g. we                  of the type of programs our tool is currently able to verify fully
assume that the condition is of the form c(x) < 0. Indeed, any                   automatically. The B-spline example from Section 5.3 is the largest


                                                                         8                                                                   2018/10/30
 Benchmark                 Our error (IA only)      Simulated error           variables in preconditions and path conditions. Table 2 compares
 doppler1*                 2.36e-6                      5.97e-7               results of our range computation procedure described in Section 6
                                                                              against ranges obtained with standard interval arithmetic. Interval
 doppler1                  4.92e-13 (4.95e-13)         7.11e-14               arithmetic is one of the methods used for step-wise range estima-
 doppler2*                 6.21e-5                      1.85-5                tion; an alternative being affine arithmetic. We have also experi-
 doppler2                  1.29e-12                    1.14e-13               mented with an affine arithmetic implementation [12]. However, we
                                                                              found that affine arithmetic gives more pessimistic results for com-
 doppler3*                 1.23e-4                      5.96e-5               puting ranges for non-linear benchmarks. We believe that this is
 doppler3                  2.03e-13 (2.05e-13)         4.27e-14               due to imprecision in computing nonlinear operations. Note, how-
 rigidBody1*               9.21e-7                      8.24e-7               ever, that we still use affine arithmetic to estimate errors given the
                                                                              computed ranges.
 rigidBody1                5.08e-13                    2.28e-13                   We set the default precision threshold to 1e−10 and maximum
 rigidBody2*               1.51e-4                      1.25e-4               number of iterations for the binary search to 50. To obtain an
 rigidBody2                6.48e-11                    2.19e-11               idea about the ranges of our functions, we have also computed
 jetEngine*                0.15       (-)              3.58e-5                a lower bound on the range using simulations with 107 random
                                                                              inputs and with exact rational arithmetic evaluation of expressions.
 jetEngine                 1.62e-8 (-)                 5.46e-12               We observe that our range computation can significantly improve
 turbine1*                 4.86e-6                      3.71e-7               over standard interval bounds. The jetEngine benchmark is a notable
 turbine1                  1.25e-13 (1.38e-13)         1.07e-14               example, where interval arithmetic yields the bound [−∞, ∞],
                                                                              but our procedure can still provide bounds that are quite close to
 turbine2*                 8.05e-6                      7.66e-7               the true range. Running times are below 7 seconds for the most
 turbine2                  1.76e-13 (1.96e-13)         1.43e-14               complex benchmarks, except for jetEngine which runs in about 1
 turbine3*                 3.35e-6                      1.04e-6               minute due to timeouts from Z3 for some intermediate ranges.
 turbine3                  8.50e-14 (9.47e-14)         5.33e-15
 verhulst*                 2.82e-4                      2.40e-4
 verhulst                  6.82e-16                    2.23e-16               Error computation Table 3 compares uncertainties computed by
 predatorPrey*             9.22e-5                      8.61e-5               our tool against maximum uncertainties obtained through exten-
 predatorPrey              2.94e-16 (2.96e-16)         1.12e-16               sive simulation with 107 random inputs. We ran the simulation in
                                                                              parallel with rational and their corresponding floating-point value
 carbonGas*                2114297.84                 168874.70
                                                                              and obtained the error by taking the difference in the result. Bench-
 carbonGas                 4.64e-8 (5.04e-8)            3.73e-9               marks marked with (*) have added initial uncertainties. Unless oth-
 Sine (single)             1.03e-6 (1.57e-6)            1.79e-7               erwise indicated, we used double floating-point precision. To our
 Sine                      9.57e-16 (1.46e-15)         4.45e-16               knowledge this is the first quantitative comparison of an error com-
                                                                              putation precision with (an approximation) of the true errors on
 Sqrt (single)             9.03e-7 (9.52e-7)            2.45e-7               such benchmarks. Except for the benchmarks jetEngine∗ our com-
 Sqrt                      8.41e-16 (8.87e-16)         4.45e-16               puted uncertainties are within an order and many times even closer
 Sine, order 3 (single)    1.19e-6 (1.55e-6)            2.12e-7               to the underapproximation of the true errors provided by simula-
                                                                              tion. In the case of the jetEngine∗ benchmark, we believe that the
 Sine, order 3             1.11e-15 (1.44e-15)         3.34e-16               imprecision is mainly due to its complexity and subsequent failures
Table 3. Comparison of errors computed with our procedure                     of Z3. The values in parentheses in the second column indicate er-
                                                                              rors computed if ranges at each arithmetic operation are computed
against simulated errors. Simulations were performed with 107 ran-
                                                                              using interval arithmetic alone. While we have not attempted to im-
dom inputs. (*) indicates that inputs have external uncertainties as-
                                                                              prove the affine arithmetic-based error computation from [12], we
sociated.
                                                                              can see that in some cases a more precise range computation can
                                                                              gain us improvements. The full effect of the imprecision of stan-
meaningful example we were able to find that Z3 alone could verify            dard range computation appears when, due to this imprecision, we
in the presence of uncertainties. For all other cases, it was necessary       obtain possible errors such as division-by-zero or square root of a
to use our approximation methods.                                             negative number errors. The first case happens in the case of the
                                                                              non-linear jetEngine benchmark, so with interval arithmetic alone
8.1   Evaluating Effectiveness on Nonlinear Expressions                       we would therefore not obtain any meaningful result. Similarly, for
To evaluate our range and error computation technique we have                 the triangle example from Section 2, without being able to con-
chosen several nonlinear expressions commonly used in physics,                strain the inputs to form valid triangles, we cannot compute any
biology and chemistry [40, 43, 49] as benchmark functions, as well            error bound, because the radicand becomes possibly negative.
as benchmarks used in control systems [1] and suitable benchmarks                 Table 4 presents another relevant experiment, evaluating the
from [18].Experiments were performed on a desktop computer                    ability to use additional constraints during our range computation.
running Ubuntu 12.04.1 with a 3.5GHz i7 processor and 16GB of                 We use the triangle example from Section 2 with additional con-
RAM. Running times highly depend on the timeout used for Z3.                  straints allowing increasingly flat triangles by setting the threshold
Our default setting is 1 second; we did not find much improvement             on line 13 (a + b > c + 1e−6) to the different values given in the first
in the success rate above this threshold.                                     column. As the triangles become flatter, we observe an expected in-
                                                                              crease in uncertainty on the input since the formula becomes more
Range computation Stepwise estimation of errors crucially de-                 prone to roundoff errors. At threshold 1e−10 our range computation
pends on the estimate of the ranges of variables. The strength of             fails to provide the necessary precision and the radicand becomes
using a constraint solver such as Z3 is that it can perform such esti-        possibly negative. (We used double precision in this example as
mation while taking into account the precise dependencies between             well.)


                                                                          9                                                                 2018/10/30
                   Benchmark                          Our range             interval arithmetic               Simulated range
                   doppler1                  [-137.639, -0.033951]       [-158.720, -0.029442]           [-136.346, -0.035273]
                   doppler2                  [-230.991, -0.022729]       [-276.077, -0.019017]            [-227.841,-0.023235]
                   doppler3                    [-83.066, -0.50744]         [-96.295, -0.43773]             [-82.624, -0.51570]
                   rigidBody1                      [-705.0, 705.0]             [-705.0, 705.0]             [-697.132, 694.508]
                   rigidBody2                  [-56010.1, 58740.0]        [-58740.0, 58740.0]          [-54997.635, 57938.052]
                   jetEngine                 [-1987.022, 5099.243]                [−∞, ∞]                [-1779.551, 4813.564]
                   turbine1                     [-18.526, -1.9916]          [-58.330, -1.5505]              [-18.284, -1.9946]
                   turbine2                      [-28.555, 3.8223]           [-29.437, 80.993]               [-28.528, 3.8107]
                   turbine3                     [0.57172, 11.428]           [0.46610, 40.376]               [0.61170, 11.380]
                   verhulst                     [0.31489, 1.1009]           [0.31489, 1.1009]               [0.36685,0.94492]
                   predatorPrey               [0.039677, 0.33550]         [0.037277, 0.35711]              [0.039669,0.33558]
                   carbonGas                 [4.3032 e6, 1.6740 e7]      [2.0974 e6, 3.4344 e7]         [4.1508 e6, 1.69074 e7]
                   Sine                          [-1.0093, 1.0093]           [-2.3012, 2.3012]               [-1.0093, 1.0093]
                   Sqrt                             [1.0, 1.3985]           [0.83593, 1.5625]                  [1.0, 1.3985]
                   Sine (order 3 approx.)        [-1.0001, 1.0001]           [-2.9420, 2.9420]                   [-1.0, 1.0]

Table 2. Comparison of ranges computed with out procedure against interval arithmetic and simulation. Simulations were performed with
107 random inputs. Ranges are rounded outwards.


       Benchmark                Range             Max. abs. error              def cav10(x: Real): Real = {
     triangle1 (0.1)      [0.29432, 35.0741]        2.72e-11                 2   require(x.in(0, 10))
                                                                                 if (x∗x − x >= 0)
    triangle2 (1e-2)     [0.099375, 35.0741]        8.04e-11                 4      x/10
    triangle3 (1e-3)    [3.16031e-2, 35.0741]       2.53e-10                     else
                                                                             6      x∗x + 2
    triangle4 (1e-4)     [9.9993e-3, 35.0741]       7.99e-10
                                                                               } ensuring(res => 0 <= res && res <= 3.0 && res +/− 3.0)
    triangle5 (1e-5)     [3.1622e-3, 35.0741]        2.53e-9                 8

    triangle6 (1e-6)     [9.9988e-4, 35.0741]        7.99e-9                def squareRoot3(x: Real): Real = {
                                                                         10   require( x.in(0,10) && x +/− 1e−10 )
    triangle7 (1e-7)     [3.1567e-4, 35.0741]        2.54e-8                  if (x < 1e−5)
    triangle8 (1e-8)     [9.8888e-5, 35.0741]        8.08e-8             12      1 + 0.5 ∗ x
                                                                              else
    triangle9 (1e-9)     [3.0517e-5, 35.0741]        2.62e-7             14      sqrt(1 + x)
  triangle10 (1e-10)              -                     -                   } ensuring( res => res +/− 1e−10)
                                                                         16

Table 4. Ranges and errors for increasingly flat triangles. All val-             def smartRoot(a: Real, b: Real, c: Real): Real = {
ues are rounded outwards. Interval arithmetic alone fails to provide     18        require(3 <= a && a <= 3 && 3.5 <= b && b <= 3.5 &&
any result.                                                                         c.in(−2, 2) && b∗b − a ∗ c ∗ 4.0 > 0.1)
                                                                         20
                                                                              val discr = b∗b − a ∗ c ∗ 4.0
                                                                         22   if(b∗b − a∗c > 10.0) {
                                                                                 if(b > 0.0) c ∗ 2.0 /(−b − sqrt(discr))
8.2   Evaluating Errors across Program Paths
                                                                         24      else if(b < 0.0) (−b + sqrt(discr))/(a ∗ 2.0)
Figure 7 presents several examples to evaluate our error compu-                  else (−b + sqrt(discr))/(a ∗ 2.0)
tation procedure across different paths from Section 7. The first        26   }
method cav10 [22] has been used before as a benchmark function                else {
for computing the output range. Our tool can verify the given post-      28      (−b + sqrt(discr))/(a ∗ 2.0)
                                                                              }
condition immediately. Note that the error on the result is actually
                                                                         30 } ensuring (res => res +/− 6e−15)
as large as the result itself, since the method is non-continuous,
an aspect that has been ignored in previous work, but that our                              Figure 7. Path error computation examples.
tool detects automatically. The method squareRoot3 is also an non-
continous function that computes the square root of 1 + x using an
approximation for small values and the regular library method oth-               method from [23]. We are currently not aware of an automatic tool
erwise. Note the additional uncertainty on the input, which could                to prove programs continuous in the presence of nonlinear arith-
occur for instance if this method is used in an embedded controller.             metic, so that we need to compute the error across different paths
Our tool can verify the given spefication. If we change the condition            as well. Our tool succeeds in verifying the postcondition in about
on line 10 to x < 1e−4 however, verification fails. In this fashion,             25s. The rather long running time is due to the complexity of the
we can use our tool to determine the appropriate branch condition                conditions when computing the error across paths, and thus Z3’s
to meet the precision requirement. The above examples verify all                 longer response time, and a number of Z3 timeouts (Z3 timeout
in under 5 seconds. Finally, the smartRoot method computes one                   here means merely that some ranges have not been tightend to the
root of a quadratic equation using the well-known more precise                   best precision). In the future, we envision that optimizations that


                                                                        10                                                                 2018/10/30
select alternative approximations can be performed automatically               arithmetic [30] will make many more verification problems feasible
by a trustworthy compiler.                                                     with our techniques. An alternative to this approach is using linear
                                                                               approximations to solve polynomial constraints [7]. We believe that
9.   Related work                                                              such advances are largely orthogonal to our use of range arithmetic
                                                                               and complement each other.
Current approaches for verifying floating-point code include ab-
stract interpretation, interactive theorem proving and decision pro-           Testing Symbolic execution is a well-known technique for gener-
cedures, which we survey in this section. We are not aware of work             ating test inputs. [6] use a combination of meta-heuristic search and
that would automatically integrate reasoning about uncertainties.              interval constraint solving to solve the floating-point constraints
                                                                               that arise, whereas [33] combine random search and evolutionary
Abstract interpretation (AI) Abstract domains that are sound                   techniques. [47] test numerical code for precision by perturbing
with respect to floating-point computations can prove bounds on                low-order bits of values and rewriting expressions. The idea is to
the ranges of variables [5, 11, 20, 28, 38]. The only work in this area        exagerate initial errors and thus make imprecisions more visible.
that can also quantify roundoff errors is the tool Fluctuat[17, 24].           Probabilistic arithmetic [45] is a similar approach but it does the
These techniques use interval or affine arithmetic and together with           perturbation by using different rounding modes. [4] also propose
the required join and meet operations may yield too pessimistic                a testing produce to detect accuracy problems by instrumentring
results. [42] improves the precision of Fluctuat by refining the in-           code to perform a higher-precision computation side by side with
put domains with a constraint solver. Our approach can be viewed               the regular computations. While these approaches are sound with
as approaching the problem from a different end, starting with an              respect to floating-point arithmetic, they only generate or can check
exact constraint and then using approximation until the solver suc-            individual inputs and are thus not able to verify or compute output
ceeds. Unlike AI tools in general, our system currently handles                ranges or their roundoff errors.
only functional code, in particular it does not handle loops. If the
user can provide inductive postconditions, then we can still prove             Robustness analysis [27] combines abstract interpretation with
the code correct, but we do not in general discover these ourselves.           model checking to check programs for stability by tracking the evo-
Our focus lies on proving precise bounds on the ranges in the pres-            lution of the width of the interval representing a single input. [36]
ence of nonlinear computations and the quantification of roundoff              use concolic execution to find inputs which, given maximum devi-
errors and other uncertainties.                                                ations on inputs, maximize the deviation on the outputs. These two
                                                                               works however, use a testing approach and cannot provide sound
Theorem proving The Gappa tool [14, 35] generates a proof                      guarantees. [9] presents a framework for continuity analysis of pro-
checkable by the interactive theorem prover Coq from source code               grams along the mathematical −δ definition of continuity and [10]
with specifications. It can reason about properties that can be re-            builds on this work and presents a sound robustness analysis. This
duced to reasoning about ranges and errors, but targets, very precise          framework provides a syntactic proof of robustness for programs
properties of specialized functions, such as software implementa-              over reals and thus does not consider floating-points. Our approach
tions of elementary functions. The specification itself requires ex-           describes a quantitative measure of robustness for nonlinear pro-
pertize and the proofs human intervention. A similar approach is               grams with floating-point numbers and other uncertainties, and we
taken by [2] which generate verification conditions that are dis-              believe that it can complement the cited framework.
charged by various theorem provers. Harisson has also done signif-
icant work on proving floating-point programs in the HOL Light
theorem prover [26].                                                           10.    Conclusion
    Our approach makes a different compromise on the precision                 We have presented a programming model for numerical programs
vs. automation tradeoff, by being less precise, but automatic. The             that decouples the mathematical problem description from its re-
Gappa approach can be used complementary to ours, in that if we                alization in finite precision. The model uses a Real data type that
detect that more precision is needed, Gappa is employed by an                  corresponds to mathematical real numbers. The developer specifies
expert user on selected methods, and the results are then used by              the program using reals and indicates the target precision; the com-
our tool instead of automatically computed specifications.                     piler chooses a floating point representation while checking that the
                                                                               desired precision targets are met. We have described the soundness
Range computation The Gappa tool and most constraint solvers
                                                                               criteria by translating programs with precision requirements into
internally use interval arithmetic for sound range computations,
                                                                               verification conditions over mathematical reals. The resulting veri-
whose limitations are well-known. [19] describes an arithmetic
                                                                               fication conditions, while a natural description of the problem being
based on function enclosures and [37] use an arithmetic based
                                                                               solved, are difficult to solve using a state-of-the art SMT solver Z3.
on taylor series as an alternative. This approach is useful when
                                                                               We therefore developed an algorithm that combines SMT solving
checking a constraint, but is not suitable for a forward computation
                                                                               with range computation. Our notion of soundness incorporates full
of ranges and errors.
                                                                               input/output behavior of functions, taking into account that, due to
Decision procedures An alternative approach to verification via                conditionals, small differences in values can lead to different paths
range computation are floating-point decision procedures. Bit-                 being taken in the program. For such cases our approach estimates
precise constraints, however, become very large quickly. [8] ad-               a sound upper bound on the total error of the computation.
dresses this problem by using a combination of over- and underap-                  We have evaluated our techniques on a number of benchmarks
proximations. [25] present an alternative approach in combining                from the literature, including benchmarks from physics, biology,
interval constraint solving with a CDCL algorithm and [21] is a                chemistry, and control systems. We have found that invocation of
decision procedure for nonlinear real arithmetic combining inter-              SMT solver alone is not sufficient to handle these benchmarks due
val constraint solving with an SMT solver for linear arithmetic.[44]           to scalability issues, whereas the use of range arithmetic by itself
formalizes the floating-points for the SMT-LIB format. While these             is not precise enough. By combining these two techniques we were
approach can check ranges on numeric variables, they do not handle             able to show that a floating point version of the code conforms to
roundoff errors or other uncertainties and cannot compute specifi-             the real-valued version with reasonable precision requirements.
cations automatically.                                                             We believe that our results indicate that it is reasonable to in-
    Our techniques rely on the performance of Z3. We hope that                 troduce Reals as a data type, following a list of previously intro-
an integration of the recent new improved solver for nonlinear                 duced mathematical abstractions in programming languages, such


                                                                          11                                                               2018/10/30
as unbounded integers, rationals, and algebraic data types. The fea-                [24] E. Goubault, S. Putot, and F. Védrine. Modular static analysis with
sibility of verified compilation of our benchmarks suggests that it                      zonotopes. In SAS, 2012.
is realistic to decouple the verification of executable mathematical                [25] L. Haller, A. Griggio, M. Brain, and D. Kroening. Deciding floating-
models over reals from their sound compilation. We therefore ex-                         point logic with systematic abstraction. In FMCAD, 2012.
pect that this methodology will help advance rigorous formal veri-                  [26] J. Harrison. Floating-Point Verification using Theorem Proving. In
fication of numerical software and enable us to focus more on high-                      Formal Methods for Hardware Verification, 6th International School
level correctness properties as opposed to run-time errors alone.                        on Formal Methods for the Design of Computer, Communication, and
                                                                                         Software Systems, SFM, 2006.
References                                                                          [27] F. Ivancic, M. Ganai, S. Sankaranarayanan, and A. Gupta. Numerical
                                                                                         stability analysis of floating-point computations using software model
 [1] A. Anta and P. Tabuada. To Sample or not to Sample: Self-Triggered                  checking. In MEMOCODE, 2010.
     Control for Nonlinear Systems. IEEE Transactions on Automatic
     Control, 55(9), 2010.                                                          [28] B. Jeannet and A. Miné. Apron: A Library of Numerical Abstract
                                                                                         Domains for Static Analysis. In CAV, 2009.
 [2] A. Ayad and C. Marché. Multi-prover verification of floating-point
     programs. In IJCAR, 2010.                                                      [29] J. Jiang, W. Luk, and D. Rueckert. FPGA-Based Computation of Free-
                                                                                         Form Deformations. In Field-Programmable Logic and Applications,
 [3] D. H. Bailey, Y. Hida, X. S. Li, and B. Thompson. C++/Fortran-                      2003.
     90 double-double and quad-double package.                   http://crd-
     legacy.lbl.gov/˜dhbailey/mpdist/, 2013.                                        [30] D. Jovanović and L. de Moura. Solving Non-linear Arithmetic. In
                                                                                         IJCAR 2012, 2012.
 [4] F. Benz, A. Hildebrandt, and S. Hack. A dynamic program analysis to
     find floating-point accuracy problems. In PLDI, 2012.                          [31] W. Kahan. Miscalculating Area and Angles of a Needle-like Triangle.
                                                                                         Technical report, University of California Berkeley, 2000.
 [5] B. Blanchet, P. Cousot, R. Cousot, J. Feret, L. Mauborgne, A. Miné,
     D. Monniaux, and X. Rival. A static analyzer for large safety-critical         [32] V. Kuznetsov, J. Kinder, S. Bucur, and G. Candea. Efficient State
     software. In PLDI, pages 196–207, 2003.                                             Merging in Symbolic Execution. In PLDI, 2012.
 [6] M. Borges, M. d’Amorim, S. Anand, D. Bushnell, and C. S. Pasareanu.            [33] K. Lakhotia, N. Tillmann, M. Harman, and J. de Halleux. FloPSy -
     Symbolic Execution with Interval Solving and Meta-heuristic Search.                 Search-Based Floating Point Constraint Solving for Symbolic Execu-
     In ICST, 2012.                                                                      tion. In Testing Software and Systems. Springer Berlin / Heidelberg,
                                                                                         2010.
 [7] C. Borralleras, S. Lucas, A. Oliveras, E. Rodrı́guez-Carbonell, and
     A. Rubio. Sat modulo linear arithmetic for solving polynomial con-             [34] X. Leroy. Verified squared: does critical software deserve verified
     straints. J. Automated Reasoning, 48(1), 2012.                                      tools? In POPL, 2011.
 [8] A. Brillout, D. Kroening, and T. Wahl. Mixed abstractions for floating-        [35] M. D. Linderman, M. Ho, D. L. Dill, T. H. Meng, and G. P. Nolan. To-
     point arithmetic. In FMCAD, pages 69–76, 2009.                                      wards program optimization through automated analysis of numerical
                                                                                         precision. In CGO, 2010.
 [9] S. Chaudhuri, S. Gulwani, and R. Lublinerman. Continuity analysis
     of programs. In POPL, 2010.                                                    [36] R. Majumdar, I. Saha, and Z. Wang. Systematic Testing for Control
                                                                                         Applications. In MEMOCODE, 2010.
[10] S. Chaudhuri, S. Gulwani, R. Lublinerman, and S. Navidpour. Proving
     Programs Robust. In ESEC/FSE, 2011.                                            [37] K. Makino and M. Berz. Taylor Models and Other Validated Func-
                                                                                         tional Inclusion Methods. International Journal of Pure and Applied
[11] L. Chen, A. Miné, J. Wang, and P. Cousot. Interval Polyhedra: An
                                                                                         Mathematics, 4, 2003.
     Abstract Domain to Infer Interval Linear Relationships. In SAS, 2009.
                                                                                    [38] A. Miné. Relational Abstract Domains for the Detection of Floating-
[12] E. Darulova and V. Kuncak. Trustworthy numerical computation in
                                                                                         Point Run-Time Errors. In ESOP, 2004.
     Scala. In OOPSLA, 2011.
                                                                                    [39] R. Moore. Interval Analysis. Prentice-Hall, 1966.
[13] E. Darulova, V. Kuncak, R. Majumdar, and I. Saha. Synthesis of fixed-
     point arithmetic code. In EMSOFT, 2013.                                        [40] J. D. Murray. Mathematical Biology, I. An Introduction. Springer,
                                                                                         2002.
[14] F. de Dinechin, C. Lauter, and G. Melquiond. Certifying the Floating-
     Point Implementation of an Elementary Function Using Gappa. IEEE               [41] M. Odersky, L. Spoon, and B. Venners. Programming in Scala: A
     Trans. Comput., 2011.                                                               Comprehensive Step-by-step Guide. Artima Incorporation, 2008.
[15] L. H. de Figueiredo and J. Stolfi. Self-Validated Numerical Methods            [42] O. Ponsini, C. Michel, and M. Rueher. Refining Abstract Interpreta-
     and Applications. IMPA/CNPq, Brazil, 1997.                                          tion Based Value Analysis with Constraint Programming Techniques.
                                                                                         In CP, 2012.
[16] L. De Moura and N. Bjørner. Z3: an efficient SMT solver. In TACAS,
     2008.                                                                          [43] A. Quarteroni, F. Saleri, and P. Gervasio. Scientific Computing with
                                                                                         MATLAB and Octave. Springer, 3rd edition, 2010.
[17] D. Delmas, E. Goubault, S. Putot, J. Souyris, K. Tekkal, and
     F. Vedrine. Towards an industrial use of FLUCTUAT on safety-critical           [44] P. Rümmer and T. Wahl. An SMT-LIB Theory of Binary Floating-
     avionics software. In FMICS, 2009.                                                  Point Arithmetic. In Informal proceedings of 8th International Work-
                                                                                         shop on Satisfiability Modulo Theories (SMT) at FLoC, 2010.
[18] V. D’Silva, L. Haller, D. Kroening, and M. Tautschnig. Numeric
     Bounds Analysis with Conflict-driven Learning. In TACAS, 2012.                 [45] N. Scott, F. Jézéquel, C. Denis, and J.-M. Chesneaux. Numerical
                                                                                         ‘health check’ for scientific codes: the CADNA approach. Computer
[19] J. A. Duracz and M. Konecny. Polynomial function enclosures and
                                                                                         Physics Communications, 2007.
     floating point software verification. Constraints in Formal Verifica-
     tion/IJCAR, 2008.                                                              [46] I. C. Society. IEEE Standard for Floating-Point Arithmetic. IEEE Std
                                                                                         754-2008, 2008.
[20] J. Feret. Static Analysis of Digital Filters. In the 13th European
     Symposium on Programming - ESOP, 2004.                                         [47] E. Tang, E. Barr, X. Li, and Z. Su. Perturbing numerical calculations
                                                                                         for statistical analysis of floating-point program (in)stability. In ISSTA,
[21] S. Gao, M. Ganai, F. Ivancic, A. Gupta, S. Sankaranarayanan, and
                                                                                         2010.
     E. Clarke. Integrating ICP and LRA solvers for deciding nonlinear
     real arithmetic problems. In FMCAD, 2010.                                      [48] E. M. Westbrook and S. Chaudhuri. A Semantics for Approximate
                                                                                         Program Transformations. CoRR, 2013.
[22] K. Ghorbal, E. Goubault, and S. Putot. A Logical Product Approach
     to Zonotope Intersection. In CAV, 2010.                                        [49] C. Woodford and C. Phillips. Numerical Methods with Worked Exam-
[23] D. Goldberg. What every computer scientist should know about                        ples, volume 2nd. Springer, 2012.
     floating-point arithmetic. ACM Comput. Surv., 23(1), 1991.


                                                                               12                                                                        2018/10/30
