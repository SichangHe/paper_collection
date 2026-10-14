                                              Satisfiability Modulo Transcendental Functions via
                                                           Incremental Linearization?

                                                          Alessandro Cimatti1 , Alberto Griggio1 , Ahmed Irfan1,2 ,
                                                                 Marco Roveri1 , and Roberto Sebastiani2
                                                                        1
                                                                         Fondazione Bruno Kessler, Italy,
                                                                            [lastname]@fbk.eu,
                                                                       2
                                                                         DISI, University of Trento, Italy,
                                                                     [firstname].[lastname]@unitn.it
arXiv:1801.08723v1 [cs.LO] 26 Jan 2018




                                                 Abstract. In this paper we present an abstraction-refinement approach to Satisfi-
                                                 ability Modulo the theory of transcendental functions, such as exponentiation and
                                                 trigonometric functions. The transcendental functions are represented as uninter-
                                                 preted in the abstract space, which is described in terms of the combined theory
                                                 of linear arithmetic on the rationals with uninterpreted functions, and are incre-
                                                 mentally axiomatized by means of upper- and lower-bounding piecewise-linear
                                                 functions. Suitable numerical techniques are used to ensure that the abstractions
                                                 of the transcendental functions are sound even in presence of irrationals. Our ex-
                                                 perimental evaluation on benchmarks from verification and mathematics demon-
                                                 strates the potential of our approach, showing that it compares favorably with
                                                 delta-satisfiability/interval propagation and methods based on theorem proving.


                                         1    Introduction
                                         Many applications require dealing with transcendental functions (e.g., exponential, log-
                                         arithm, sine, cosine). Nevertheless, the problem of Satisfiability Modulo the theory of
                                         transcendental functions comes with many difficulties. First, the problem is in general
                                         undecidable [22]. Second, we may be forced to deal with irrational numbers - in fact,
                                         differently from polynomial, transcendental functions most often have irrational values
                                         for rational arguments. (See, for example, Hermite’s proof that exp(x) is irrational for
                                         rational non-zero x.)
                                             In this paper, we describe a novel approach to Satisfiability Modulo the quantifier-
                                         free theory of (nonlinear arithmetic with) transcendental functions over the re-
                                         als - SMT(NTA). The approach is based on an abstraction-refinement loop, using
                                         SMT(UFLRA) as abstract space, UFLRA being the combined theory of linear arith-
                                         metic on the rationals with uninterpreted functions. The Uninterpreted Functions are
                                         used to model nonlinear and transcendental functions. Then, we iteratively incre-
                                         mentally axiomatize the transcendental functions with a lemma-on-demand approach.
                                         Specifically, we eliminate spurious interpretations in SMT(UFLRA) by tightening the
                                         piecewise-linear envelope around the (uninterpreted counterpart of) the transcendental
                                         functions.
                                         ?
                                             This work was funded in part by the H2020-FETOPEN-2016-2017-CSA project SC2
                                             (712689). We thank James Davenport and Erika Abraham for useful discussions.
     A key challenge is to compute provably correct approximations, also in presence
of irrational numbers. We use Taylor series to exactly compute suitable accurate ratio-
nal coefficients. We remark that nonlinear polynomials are only used to numerically
compute the coefficients –i.e., no SMT solving in the theory of nonlinear arithmetic
(SMT(NRA)) is needed– whereas the refinement is based on the addition, in the abstract
space, of piecewise-linear axiom instantiations, which upper- and lower-bound the can-
didate solutions, ruling out spurious interpretations. To compute such piecewise-linear
bounding functions, the concavity of the curve is taken into account. In order to deal
with trigonometric functions, we take into account the periodicity, so that the axiom-
atization is only done in the interval between −π and π. Interestingly, not only this is
helpful for efficiency, but also it is required to ensure correctness.
     Another distinguishing feature of our approach is a logical method to conclude
the existence of a solution without explicitly constructing it. We use a sufficient cri-
terion that consists in checking whether the formula is satisfiable under all possible in-
terpretations of the uninterpreted functions (representing the transcendental functions)
that are consistent with some rational interval bounds within which the correct values
for the transcendental functions are guaranteed to exist. We encode the problem as a
SMT(UFLRA) satisfiability check, such that an unsatisfiable result implies the satisfia-
bility of the original SMT(NTA) formula.
     We implemented the approach on top of the M ATH SAT SMT solver [7], using
the P Y SMT library [14]. We experimented with benchmarks from SMT-based veri-
fication queries over nonlinear transition systems, including Bounded Model Check-
ing of hybrid automata, as well as from several mathematical properties from the
M ETI TARSKI [1] suite and from other competitor solver distributions. We contrasted
our approach with state-of-the-art approaches based on interval propagation (iSAT3
and D R EAL), and with the deductive approach in M ETI TARSKI. The results show that
our solver compares favourably with the other solvers, being able to decide the highest
number of benchmarks.
     This paper is organized as follows. In §2 we describe some background. In §3 we
overview the approach, defining the foundation for safe linear approximations. In §4 we
describe the specific axiomatization for transcendental functions. In §5 we discuss the
related literature, and in §6 we present the experimental evaluation. In §7 we draw some
conclusions and outline directions for future work.


2   Background

We assume the standard first-order quantifier-free logical setting and standard notions
of theory, satisfiability, and logical consequence. As usual in SMT, we denote with LRA
the theory of linear real arithmetic, with NRA that of non-linear real arithmetic, with
UF the theory of equality (with uninterpreted functions), and with UFLRA the com-
bined theory of UF and LRA. Unless otherwise specified, we use the terms variable and
free constant interchangeably. We denote formulas with ϕ, ψ, terms with t, variables
with x, y, a, b, functions with f, tf , ftf , each possibly with subscripts. If x and y are
two variables, we denote with ϕ{x 7→ y} the formula obtained by replacing all the oc-
currences of x in ϕ with y. We extend this notation to ordered sequences of variables in
the natural way. If µ is a model and x is a variable, we write µ[x] to denote the value of
x in µ, and we extend V  this notation to terms and formulas in the usual way. If Γ is a set
of formulas, we write Γ to denote the formula obtained by taking the conjunction of
all its elements. We write t1 < t2 < t3 for t1 < t2 ∧ t2 < t3 .
     A transcendental function is an analytic function that does not satisfy a polynomial
equation (in contrast to an algebraic function [15, 26]). Within this paper we consider
univariate exponential, logarithmic, and trigonometric functions. We denote with NTA
the theory of (non-linear) real arithmetic extended with these transcendental functions.
     A tangent line to a univariate function f (x) at a point of interest x = a is a straight
line that “just touches” the function at the point, and represents the instantaneous rate
of change of the function f at that one point. The tangent line Tf,a (x) to the function f
at point a is the straight line defined as follows:

                                       def                d
                          Tf,a (x) = f (a) +                f (a) ∗ (x − a)
                                                         dx
        d
where dx  f is the first-order derivative of f wrt. x.
    A secant line to a univariate function f (x) is a straight line that connects two points
on the function plot. The secant line Sf,a,b (x) to a function f between points a and b is
defined as follows:
                                 def    f (a) − f (b)
                      Sf,a,b (x) =                    ∗ (x − a) + f (a).
                                            a−b
    For a function f that is twice differentiable at point c, the concavity of f at c is
the sign of its second derivative evaluated at c. We denote open and closed intervals
between two real numbers l and u as ]l, u[ and [l, u] respectively. Given a univariate
function f over the reals, the graph of f is the set of pairs {hx, f (x)i | x ∈ R}. We
might sometimes refer to an element hx, f (x)i of the graph as a point.

Taylor Series and Taylor’s Theorem. Given a function f (x) that has n + 1 continuous
derivatives at x = a, the Taylor series of degree n centered around a is the polynomial:
                                                   n
                                             def
                                                   X f (i) (a)
                          Pn,f (a) (x) =                         ∗ (x − a)i
                                                   i=0
                                                           i!

where f (i) (a) is the evaluation of i-th derivative of f (x) at point x = a. The Taylor
series centered around 0 is also called Maclaurin series.
    According to Taylor’s theorem, any continuous function f (x) that is n + 1 differen-
tiable can be written as the sum of the Taylor series and the remainder term:

                           f (x) = Pn,f (a) (x) + Rn+1,f (a) (x)

where Rn+1,f (a) (x) is basically the Lagrange form of the remainder, and for some point
b between x and a it is given by:

                                             def   f (n+1) (b)
                       Rn+1,f (a) (x) =                        ∗ (x − a)n+1 .
                                                    (n + 1)!
                         bool SMT-NTA-check-abstract (ϕ):
                         1. ϕ b = initial-abstraction(ϕ)
                         2. Γ = ∅
                         3. precision := initial-precision ()
                         4. while true:
                         5.      if budget-exhausted ():
                         6.           abort                             V
                         7.      hres, µ bi = SMT-UFLRA-check (ϕ    b ∧ Γ)
                         8.      if not res:
                         9.           return false
                         10.     hsat, Γ 0 i := check-refine (ϕ, µb, precision)
                         11.     if sat:
                         12.          return true
                         13.     else:
                         14.          precision := maybe-increase-precision ()
                         15.          Γ 00 := refine-extra (ϕ, µ
                                                               b)
                         16.          Γ := Γ ∪ Γ 0 ∪ Γ 00

                Fig. 1. Solving SMT(NTA) via abstraction to SMT(UFLRA).


The value of the point b is not known, but the upper bound on the size of the remainder
          u
Rn+1,f (a) (x) at a point x can be estimated by:

                     u        def                                               |(x − a)n+1 |
         Rn+1,f (a) (x) =                   max             (|f (n+1) (c)|) ∗                 .
                                    c∈[min(a,x),max(a,x)]                         (n + 1)!

This allows to obtain two polynomials that are above and below the function at a given
                                                 u                                 u
point x, by considering Pn,f (a) (x) + Rn+1,f (a) (x) and Pn,f (a) (x) − Rn+1,f (a) (x)
respectively.


3   Overview of the approach

Our procedure, which extends to SMT(NTA) and pushes further the approach presented
in [5] for SMT(NRA), works by overapproximating the input formula with a formula
over the combined theory of linear arithmetic and uninterpreted functions. The main
algorithm is shown in Fig. 1. The solving procedure follows a classic abstraction-
refinement loop, in which at each iteration, the current safe approximation ϕ        b of the
input SMT(NTA) formula ϕ is refined by adding new constraints Γ that rule out one (or
possibly more) spurious solutions, until one of the following conditions occurs: (i)Vthe
resource budget (e.g. time, memory, number of iterations) is exhausted; or (ii) ϕ    b∧ Γ
becomesVunsatisfiable in SMT(UFLRA); or (iii) the SMT(UFLRA) satisfiability result
    b ∧ Γ can be lifted to a satisfiability result for the original formula ϕ. An initial
for ϕ
current precision is set (calling the function initial-precision), and this value is possibly
increased at each iteration (calling maybe-increase-precision) according to the result of
check-refine and some heuristic.
    In Fig. 1 we distinguish between two different refinement procedures:
1) check-refine, which is described below; 2) refine-extra, which is described in §4,
                 hbool, axiom-seti check-refine (ϕ, µ  b, precision):
                  1. Γ := check-refine-NRA (ϕ, µ    b) # NRA refinement of [5]
                  2.  := 10−precision
                  3. for all tf (x) ∈ ϕ:
                  4.      c := µb[x]
                  5.      hPl (x), Pu (x)i := poly-approx (tf (x), c, )
                  6.         b[ftf (x)] ≤ Pl (c) or µ
                          if µ                      b[ftf (x)] ≥ Pu (c):
                  7.           Γ := Γ ∪ get-lemmas-point (tf (x), µ   b, Pl (x), Pu (x))
                  8. if Γ = ∅:
                  9.      if check-model (ϕ, µ b):
                  10.          return htrue, ∅i
                  11.     else:
                  12.          return check-refine (ϕ, µ b, precision+1)
                  13. else:
                  14.     return hfalse, Γ i

                             Fig. 2. The main refinement procedure.


where we provide further details on the treatment of each specific transcendental func-
tion that we currently support.

Initial Abstraction. The function initial-abstraction takes in input an SMT(NTA) for-
mula ϕ and returns a SMT(UFLRA) safe approximation ϕ          b of it. First, we flatten each
transcendental function application tf (t) in ϕ in which t is not a variable by replac-
ing t with a fresh variable y, and by conjoining y = t to ϕ. Then, we replace each
transcendental function tf (x) in ϕ with a corresponding uninterpreted function ftf (x),
producing thus an SMT(UFLRA) formula ϕ.        b Finally, we add to ϕ  b some simple initial
axioms for the different transcendental functions, expressing general, simple mathemat-
ical properties about them. We shall describe such axioms in §4.
    If ϕ contains also non-linear polynomials, we handle them as described in [5]:
we replace each non-linear product t1 ∗ t2 with an uninterpreted function application
f mul(t1 , t2 ), and add to the input formula some initial axioms expressing general, sim-
ple mathematical properties of multiplications. (We refer the reader to [5] for details.)

Spuriousness check and abstraction refinement. The core of our procedure is the
check-refine function, shown in Fig. 2.
    First, if the formula contains also some non-linear polynomials, check-refine per-
forms the refinement of non-linear multiplications as described in [5]. In Fig. 2, this is
represented by the call to the function check-refine-NRA at line 1, which may return
some axioms to further constrain f mul terms. If no non-linear polynomials occur in ϕ,
then Γ is initialized as the empty set.
    Then, the function iterates over all the transcendental function applications tf (x) in
ϕ (lines 3–7), and checks whether the SMT(UFLRA)-model µ        b is consistent with their
semantics.
    Intuitively, in principle, this amounts to check that tf (b
                                                              µ[x]) is equal to µ
                                                                                b[ftf (x)].
In practice, however, the check cannot be exact, since transcendental functions at ratio-
nal points typically have irrational values (see e.g. [21]), which cannot be represented
           axiom-set get-lemmas-point (tf (x), µ   b, Pl (x), Pu (x)):
            1. c := µ
                    b[x]
            2. v := µb[ftf (x)]
            3. conc := get-concavity (tf (x), c)
            4. if (v ≤ Pl (c) and conc ≥ 0) or (v ≥ Pu (c) and conc ≤ 0):
                # tangent refinement
            5.      P := (v ≤ Pl (c)) ? (Pl ) : (Pu )
                                       d
            6.      T (x) := P (c) + dx   P (c) · (x − c) # tangent of P at c
                                                                d
            7.      hl, ui := get-tangent-bounds (tf (x), c, dx    P (c))
            8.      ψ := (conc < 0) ? (ftf (x) ≤ T (x)) : (ftf (x) ≥ T (x))
            9.      return {((x ≥ l) ∧ (x ≤ u)) → ψ}
            10. else: # (v ≤ Pl (c) ∧ conc < 0) ∨ (v ≥ Pu (c) ∧ conc > 0)
                 # secant refinement
            11.     prev := get-previous-secant-points (tf (x))
            12.     l := max{p ∈ prev | p < c}
            13.     u := min{p ∈ prev | p > c}
            14.     P := (v ≤ Pl (c)) ? (Pl ) : (Pu )
                               P (l) − P (c)
            15.     Sl (x) :=                · (x − l) + P (l) # secant of P between l and c
                                   l−c
                                P (u) − P (c)
            16.     Su (x) :=                  · (x − u) + P (u)
                                    u−c
            17.     ψl := (conc < 0) ? (ftf (x) ≥ Sl (x)) : (ftf (x) ≤ Sl (x))
            18.     ψu := (conc < 0) ? (ftf (x) ≥ Su (x)) : (ftf (x) ≤ Su (x))
            19.     φl := (x ≥ l) ∧ (x ≤ c)
            20.     φu := (x ≥ c) ∧ (x ≤ u)
            21.     store-secant-point (tf (x), c)
            22.     return {(φl → ψl ), (φu → ψu )}


      Fig. 3. Piecewise-linear refinement for the transcendental function tf (x) at point c.


in SMT(UFLRA). Therefore, for each tf (x) in ϕ, we instead compute two polyno-
mials, Pl (x) and Pu (x), with the property that tf (b      µ[x]) belongs to the open interval
]Pl (b
     µ[x]), Pu (bµ[x])[. The polynomials are computed using Taylor series, according to
the given current precision, by the function poly-approx, which shall be described in §4.
     If the model value µ b[ftf (x)] for tf (x) is outside the above interval, then the function
get-lemmas-point is used to generate some linear lemmas that will remove the spurious
point hb µ[x], µ
               b[ftf (x)]i from the graph of the current abstraction of tf (x) (line 7).
     If at least one point was refined in the loop of lines 3–7, the current set of lemmas
Γ is returned (line 10). If instead none of the points was determined to be spurious, the
function check-model is called (line 9). This function tries to determine whether the
abstract model µ  b does indeed imply the existence of a model for the original formula ϕ
(more details are given below). If the check fails, we repeat the check-refine call with
an increased precision (line 12).

Refining a spurious point with secant and tangent lines. Given a transcendental
function application tf (x), the get-lemmas-point function generates a set of lemmas for
refining the interpretation of ftf (x) by constructing a piecewise-linear approximation of
tf (x) around the point µb[x], using one of the polynomials Pl (x) and Pu (x) computed in
check-refine. The kind of lemmas generated, and which of the two polynomials is used,
                        1.2
                                          p1                                tf(x)
                          1                                                Pl(x)
                                                                           Pu(x)
                        0.8                                                 T(x)
                                                                    Sl(x), Su(x)
                        0.6                              p2

                        0.4

                        0.2
                                   lx                                        ux
                          0

                        -0.2
                               0    0.5        1   1.5    2   2.5        3          3.5   4


                           Fig. 4. Piecewise-linear refinement illustration.



depend on (i) the position of the spurious value µ    b[ftf (x)] relative to the correct value
tf (b
    µ[x]), and (ii) the concavity of tf around the point µ  b[x]. If the concavity is positive
(resp. negative) or equal to zero, and the point lies below (resp. above) the function,
then the linear approximation is given by a tangent to the lower (resp. upper) bound
polynomial Pl (resp. Pu ) at µ   b[x] (lines 4–9 of Fig. 3); otherwise, i.e. the concavity is
negative (resp. positive) and the point is below (resp. above) the function, the linear
approximation is given by a pair of secants to the lower (resp. upper) bound polynomial
Pl (resp. Pu ) around µ b[x] (lines 10–22 of Fig. 3). The two situations are illustrated in
Fig. 4.
     In the case of tangent refinement, the function get-tangent-bounds (line 7) returns
an interval [l, u] such that the tangent line is guaranteed not to cross the transcendental
function tf . In practice, this interval can be (under)approximated quickly by exploiting
known properties of the specific function tf under consideration. For example, for the
exponential function get-tangent-bounds always returns [−∞, +∞]; for other func-
tions, the computation can be based e.g. on an analysis of the (known, precomputed)
                                                                                d
inflection points of tf around the point of interest µ   b[x] and the slope dx     P (c) of the
tangent line.
     In the case of secant refinement, a second value, different from µ    b[x], is required to
draw a secant line. The function get-previous-secant-points returns the set of all the
points at which a secant refinement was performed in the past for tf (x). From this set,
we take the two points closest to µ  b[x], such that l < µb[x] < u and that l, u do not cross
any inflection point, 3 and use those points to generate two secant lines and their validity
intervals. Before returning the set of the two corresponding lemmas, we also store the
new secant refinement point µ    b[x] by calling store-secant-point.



                             V The function check-model tries to determine whether
Detecting satisfiable formulas.
the UFLRA-model µ         b ∧ Γ implies the satisfiability of the original formula ϕ.
                    b for ϕ

 3
     For simplicity, we assume that this is always possible. If needed, this can be implemented e.g.
     by generating the two points at random while ensuring that l < µ  b[x] < u and that l, u do not
     cross any inflection point.
If, for all tf (x) in ϕ, tf has a rational value at the rational point µb[x],4 and µb[ftf (x)] is
equal to tf (b µ[x]), then µ
                           b can be directly lifted to a model µ for ϕ.
     In the general case, we exploit this simple observation: we can still conclude that ϕ
is satisfiable if we are able to show that ϕb is satisfiable under all possible interpretations
of ftf that are guaranteed to include also tf .
     Using the model µ     b, we compute safe lower and upper bounds tf (b          µ[x]) l and
          u
tf (b
    µ[x]) for the function tf at point µ b[x] with the poly-approx function (see above).
Let F T F be the set of all ftf (x) terms occurring in ϕ.b Let V be the set of variables x
for ftf (x) ∈ F T F , and F be the set of all the function symbols in F T F . Intuitively, if
we can prove the validity of the following formula:
                                                                        
                           ^                                         u
      ∀ ftf ∈ F.                         µ[x]) ≤ ftf (b
                                      tf (b            µ[x]) ≤ tf (b
                                                                   µ[x])  → ϕ{V
                                                                             b   7→ µ
                                                                                    b[V ]}
                                              l
                      ftf (x)∈F T F

then the original formula ϕ is satisfiable.
     In order to be able to use a quantifier-free SMT(UFLRA)-solver, we reduce the
problem to the validity check of a pure UFLRA formula. Let CT be the set of all terms
ftf (b
     µ[x]) occurring in ϕ{V
                        b    7→ µb[V ]}. We replace each occurrence of ftf (bµ[x]) in CT
with a corresponding fresh variable yftf (bµ[x]) from a set Y . We then check the validity
of the formula:
                                                                                   
     def
                    ^                                           u
ϕsat
 b = ∀Y.
 µ
                                  µ[x]) ≤ ftf (b
                                tf (b            µ[x]) ≤ tf (b
                                                             µ[x])  → ϕ{V
                                                                       b   7→ µ
                                                                              b[V ]} {CT 7→ Y }.
                                        l
                ftf (x)∈F T F

   If ¬ϕsat
         b is unsatisfiable, we conclude that ϕ is satisfiable. Clearly, this can be
         µ
checked with a quantifier-free SMT(UFLRA)-solver, since ¬∀x.φ is equivalent to
∃x.¬φ, and x can then be removed by Skolemization.


4    Abstraction Refinement for Transcendental Functions

In this section, we describe the implementation of the poly-approx and refine-extra for
the transcendental functions that we currently support, namely exp and sin.5
    The poly-approx(tf (x), c, ) function uses the Maclaurin series of the corresponding
transcendental function and Taylor’s theorem to find the lower and upper polynomials.
Essentially, this is done by expanding the series (and the remainder approximation)
up to a certain n, until the desired precision  (i.e. the difference between the upper
and lower polynomials evaluated at c) is achieved. Notice that, since we can precisely
evaluate the derivative of any order at 0 for both exp and sin,6 the computation of both
the Maclaurin series and the remainder polynomial is always exact.
 4
   Although, as mentioned above, this is not the case in general (see e.g. [21]), it is true for some
   special values, e.g. exp(0) = 1, sin(0) = 0.
 5
   We remark that our tool (see §6) can handle also log, cos, tan, arcsin, arccos, arctan by
   means of rewriting. We leave as future work the possibility of handling such functions natively.
 6
   Because (i) exp(0) = 1, sin(0) = 0, cos(0) = 1, (ii) exp(i) (x) = exp(x) for all i, and
   (iii) | sin(i) (x)| is | cos(x)| if i is odd and | sin(x)| otherwise.
Exponential Function

Piecewise-Linear Refinement. The polynomial Pn,exp(0) (x) given by the Maclaurin
series behaves differently depending on the sign of x. For that reason, poly-approx
distinguishes three cases for finding the polynomials Pl (x) and Pu (x):

Case x = 0: since exp(0) = 1, we have Pl (0) = Pu (0) = 1;
Case x < 0: we have that Pn,exp(0) (x) < exp(x) if n is odd, and Pn,exp(0) (x) >
                                               Pn     i
   exp(x) if n is even (where Pn,exp(0) (x) = i=0 xi! ); we therefore set Pl (x) =
   Pn,exp(0) (x) and Pu (x) = Pn+1,exp(0) (x) for a suitable n so that the required
   precision  is met;
                                                                          xn+1 −1
Case x > 0: we have that Pn,exp(0) (x) < exp(x) and Pn,exp(0) (x) ∗ (1 − (n+1)! ) >
                         n+1
                     x
    exp(x) when (1− (n+1)! ) > 0, therefore we set Pl (x) = Pn,exp(0) (x) and Pu (x) =
                           n+1
                          x
    Pn,exp(0) (x) ∗ (1 − (n+1)! )−1 for a suitable n.

    Since the concavity of exp is always positive, the tangent refinement will always
give lower bounds for exp(x), and the secant refinement will give upper bounds. More-
over, as exp has no inflection points, get-tangent-bounds always returns [−∞, +∞].

Extra Refinement. The exponential function is monotonically increasing with a non-
linear order. We check this property between two fexp(x) and fexp(y) terms in ϕ:  b if
µ
b[x] < µ          b[fexp(x)] 6< µ
        b[y], but µ             b[fexp(y)], then we add the following extra refinement
lemma:
                             x < y ↔ fexp(x) < fexp(y)

Initial Axioms. We add the following initial axioms to ϕ.
                                                       b

           Lower Bound: fexp(x) > 0
                    Zero: (x = 0 ↔ fexp(x) = 1) ∧ (x < 0 ↔ fexp(x) < 1)∧
                           (x > 0 ↔ fexp(x) > 1)
      Zero Tangent Line: x = 0 ∨ fexp(x) > x + 1


Sin Function

Piecewise-Linear Refinement. The correctness of our refinement procedure relies cru-
cially on being able to compute the concavity of the transcendental function tf at a
given point c. This is needed in order to know whether a computed tangent or secant
line constitutes a valid upper or lower bound for tf around c (see Fig. 3). In the case of
the sin function, computing the concavity at an arbitrary point c is problematic, since
this essentially amounts to computing the remainder of c and π, which, being π a tran-
scendental number, cannot be exactly computed.
    In order to solve this problem, we exploit another property of sin, namely its peri-
odicity (with period 2π). More precisely, we split the reasoning about sin depending on
two kinds of periods: base period and extended period. A period is a base period for
the sin function if it is from −π to π, otherwise it is an extended period. In order to
reason about periods, we first introduce a symbolic variable π b, and add the constraint
lπ < πb < uπ to ϕ,b where lπ and uπ are valid rational lower and upper bounds for the ac-
tual value of π (in our current implementation, we have lπ = 333             355
                                                               106 and uπ = 113 ). Then,
we introduce for each fsin(x) term an “artificial” sin function application fsin(yx )
(where yx is a fresh variable), whose domain is the base period. This is done by adding
the following constraints:

             π ≤ yx ≤ π
           (−b        b) ∧ ((−b
                              π≤x≤π
                                  b) → yx = x) ∧ fsin(x) = fsin(yx ).

We call these fresh variables base variables. Notice that the second and the third con-
straint are saying that fsin(x) is the same as fsin(yy ) in the base period.
    Let Fsinbase be the set of fsin(yx ) terms that have base variables as arguments,
                                                        def
Fsin be the set of all fsin(x) terms, and Fsinext = Fsin − Fsinbase . The tangent
and secant refinement is performed for the terms in Fsinbase , while we add a linear
shift lemma (described below) as refinement for the terms in Fsinext . Using this trans-
formation, we can easily compute the concavity of sin at µ    b[yx ] by just looking at the
sign of µb[yx ], provided that −lπ ≤ µ  b[yx ] ≤ lπ , where lπ is the current lower bound
    b.7 In the case in which −uπ < µ
for π                                  b[yx ] < −lπ or lπ < µ b[yx ] < uπ , we do not per-
form the tangent/secant refinement, but instead we refine the precision of π   b. For each
fsin(yx ) ∈ F Sinbase , poly-approx tries to find the lower and upper polynomial using
Taylor’s theorem, which ensures that:
                                       u                                                        u
     Pn,sin(0) (yx ) − Rn+1,sin(0) (yx ) ≤ sin(yx ) ≤ Pn,sin(0) (yx ) + Rn+1,sin(0) (yx )
                              Pn       (−1)k ∗yx
                                               2k+1                     u            y 2(n+1)
where Pn,sin(0) (yx ) =          k=0     (2k+1)!      and Rn+1,sin(0) (yx ) = (2(n+1))!
                                                                                x
                                                                                        . There-
                                                               u
fore, we can set Pl (x) = Pn,sin(0) (x) − Rn+1,sin(0) (x) and Pu (x) = Pn,sin(0) (x) +
            u
Rn+1,sin(0) (x).

Extra Refinement. For each fsin(x) ∈ Fsinext with the corresponding base variable
yx , we check whether the value µ b[x] after shifting to the base period is equal to the value
of µ
   b[yx ]. We calculate the shift s of x as the rounding towards zero of (b   µ[x] + µ
                                                                                     b[bπ ])/(2 ·
µ
b[b
  π ]), and we then compare µ  b[yx ] with µb[x] − 2s · µb[b
                                                           π ]. If the values are different, we
add the following shift lemma for relating x with yx in the extended period s:

                    π ∗ (2s − 1) ≤ x ≤ π
                   (b                  b ∗ (2s + 1)) → yx = x − 2s ∗ π
                                                                     b.

In this way, we do not need the tangent and secant refinement for the extended period
and we can reuse the refinements done in the base period. Note that even if the calcu-
lated shift value is wrong (due to the imprecision of µ
                                                      b[b
                                                        π ] with respect to the real value
π), we may generate something useless but never wrong.
    We also check the monotonicity property of sin, which can be described for the base
period as: (i) the sin is monotonically increasing in the interval − π2 to π2 ; (ii) the sin
is monotonically decreasing in the intervals −π to − π2 and π2 to π. We add one of the
 7
     In the interval [−π, π], the concavity of sin(c) is the opposite of the sign of c.
constraints below if it is in conflict according to the current abstract model for some
fsin(yx1 ), fsin(yx2 ) ∈ Fsinbase .

                    π               π
                       ≤ yx1 < yx2 ≤ ) → f sin(yx1 ) < f sin(yx2 )
                    b               b
                  (−
                    2               2
                                    π
                  π ≤ yx1 < yx2 ≤ − ) → f sin(yx1 ) > f sin(yx2 )
                                    b
                (−b
                                    2
                    π
                   ( ≤ yx1 < yx2 ≤ πb) → f sin(yx1 ) > f sin(yx2 )
                    b
                     2

Initial Axioms. For each fsin(z) ∈ Fsin, we add the generic lower and upper bounds:
−1 ≤ fsin(z) ≤ 1. For each fsin(yx ) ∈ Fsinbase , we add the following axioms.

        Symmetry: fsin(yx ) = − fsin(−yx )
                             b ↔ fsin(yx ) > 0) ∧ (−b
            Phase: (0 < yx < π                      π < yx < 0 ↔ fsin(yx ) < 0)
    Zero Tangent: (yx > 0 → fsin(yx ) < yx ) ∧ (yx < 0 → fsin(yx ) > yx )
                         b → fsin(yx ) < −yx + π
        π Tangent: (yx < π                     b)∧
                    (yx > −b
                           π → fsin(yx ) > −yx − π
                                                 b)
Significant Values: (fsin(yx ) = 0 ↔ (yx = 0 ∨ yx = π
                                                    b ∨ yx = −b π ))∧
                                          π                           π
                    (fsin(yx ) = 1 ↔ yx = ) ∧ (fsin(yx ) = −1 ↔ yx = − )∧
                                          b                           b
                                          2                           2
                                 1          π         5∗π
                    (fsin(yx ) = ↔ (yx = ∨ yx =
                                            b            b
                                                           ))∧
                                 2          6          6
                                   1            π          5∗π
                    (fsin(yx ) = − ↔ (yx = − ∨ yx = −
                                                b              b
                                                                 ))
                                   2            6            6

Optimization
We use infinite-precision to represent rational numbers. In our (model-driven) approach,
we may have to deal with numbers with very large numerators and/or denominators. It
may happen that we get such rational numbers from the bad model µ      b for the variables
appearing as arguments of transcendental functions. As a result of the piecewise-linear
refinement, we will feed to the SMT(UFLRA) solver numbers that have even (expo-
nentially) larger numerators and/or denominators (due to the fact that poly-approx uses
power series). This might significantly slow-down the performance of the solver. We
address this issue by approximating “bad” values µ b[x] with too large numerators and/or
denominators by using continued fractions [20]. The precision of the rational approx-
imation is increased periodically over the number of iterations. Thus we delay the use
numbers with larger numerator and/or denominator, and eventually find those numbers
if they are really needed.


5   Related work
The approach proposed in this paper is an extension of the approach adopted in [5] for
checking the invariants of transition systems over the theory of polynomial Nonlinear
Real Arithmetic. In this paper we extend the approach to transcendental functions, with
the critical issue of irrational valuations. Furthermore, we propose a way to prove SAT
without being forced to construct the model.
    In the following, we compare with related approaches found in the literature.

Interval propagation and D ELTA S AT. The first approach to SMT(NTA) was pio-
neered by iSAT3 [11], that carries out interval propagation for nonlinear and transcen-
dental functions. iSAT3 is both an SMT solver and bounded model checker for tran-
sition systems. A subsequent but very closely related approach is the D R EAL solver,
proposed in [12]. D R EAL relies on the notion of delta-satisfiability [12], which basi-
cally guarantees that there exists a variant (within a user-specified δ “radius”) of the
original problem such that it is satisfiable. The approach cannot guarantee that the orig-
inal problem is satisfiable, since it relies on numerical approximation techniques that
only compute safe overapproximations of the solution space.
     There are a few key insights that differentiate our approach. First, it is based on
linearization, it relies on solvers for SMT(UFLRA), and it proceeds by incrementally
axiomatizing transcendental functions. Compared to interval propagation, we avoid nu-
merical approximation (even if within the bounds from D ELTA S AT). In a sense, the
precision of the approximation is selectively detected at run time, while in iSAT3 and
D R EAL this is a user defined threshold that is uniformly adopted in the computations.
Second, our method relies on piecewise linear approximations, which can provide sub-
stantial advantages when approximating a slope – intuitively, interval propagation ends
up computing a piecewise-constant approximation. Third, a distinguishing feature of
our approach is the ability to (sometimes) prove the existence of a solution even if the
actual values are irrationals, by reduction to an SMT-based validity check.

Deductive Methods. The M ETI TARSKI [1] theorem prover relies on resolution and on
a decision procedure for NRA to prove quantified inequalities involving transcendental
functions. It works by replacing transcendental functions with upper- or lower-bound
functions specified by means of axioms (corresponding to either truncated Taylor series
or rational functions derived from continued fraction approximations), and then using
an external decision procedure for NRA for solving the resulting formulas. Differently
from our approach, M ETI TARSKI cannot prove the existence nor compute a satisfying
assignment, while we are able to (sometimes) prove the existence of a solution even if
the actual values are irrationals. Finally, we note that M ETI TARSKI may require the user
to manually write axioms if the ones automatically selected from a predefined library
are not enough. Our approach is much simpler, and it is completely automatic.
    The approach presented in [10], where the NTA theory is referred to as NLA, is
similar in spirit to M ETI TARSKI in that it combines the SPASS theorem prover [27]
with the iSAT3 SMT solver. The approach relies on the SUP(NLA) calculus that com-
bines superposition-based first-order logic reasoning with SMT(NTA). Similarly to our
work, the authors also use a UFLRA approximation of the original problem. This is
however done only as a first check before calling iSAT3. In contrast, we rely on solvers
for SMT(UFLRA), and we proceed by incrementally axiomatizing transcendental func-
tions instead of calling directly an NTA solver. Another similarity with our work is the
possibility of finding solutions in some cases. This is done by post-processing an in-
conclusive iSAT3 answer, trying to compute a certificate for a (point) solution for the
narrow intervals returned by the solver, using an iterative analysis of the formula and of
the computed intervals. Although similar in spirit, our technique for detecting satisfiable
instances is completely different, being based on a logical encoding of the existence of
a solution as an SMT(UFLRA) problem.


Combination of interval propagation and theorem proving. G APPA [9,18] is a stan-
dalone tool and a tactic for the C OQ proof assistant, that can be used to prove properties
about numeric programs (C-like) dealing with floating-point or fixed-point arithmetic.
Another related C OQ tactic is C OQ .I NTERVAL [19]. Both G APPA and C OQ .I NTERVAL
combine interval propagation and Taylor approximations for handling transcendental
functions. A similar approach is followed also in [25], where a tool written in H OL -
L IGHT to handle conjunctions of non-linear equalities with transcendental functions is
presented. The work uses Taylor polynomials up to degree two. NLC ERTIFY [17] is
another related tool which uses interval propagation for handling transcendental func-
tions. It approximates polynomials with sums of squares and transcendental functions
with lower and upper bounds using some quadratic polynomials [2]. Internally, all these
tools/tactics rely on multi-precision floating point libraries for computing the interval
bounds.
    A similarity between these approaches and our approach is the use of the Taylor
polynomials. However, one distinguishing feature is that we use them to find lower
and upper linear constraints by computing tangent and secant lines. Moreover, we do
not rely on any floating point arithmetic library, and unlike the mentioned approaches,
we can also prove the existence of a solution. On the other hand, some of the above
tools employ more sophisticated/specialised approximations for transcendental func-
tions, which might allow them to succeed in proving unsatisfiability of formulas for
which our technique is not sufficiently precise.
    Finally, since we are in the context of SMT, our approach also has the benefits
of being: (i) fully automatic, unlike some of the above which are meant to be used
within interactive theorem provers; (ii) able to deal with formulas with an arbitrary
Boolean structure, and not just conjunctions of inequalities; and (iii) capable of handling
combinations of theories (including uninterpreted functions, bit-vectors, arrays), which
are beyond what the above, more specialised tools, can handle.


6   Experimental Analysis

Implementation. The approach has been implemented on top of the M ATH SAT SMT
solver [7], using the P Y SMT library [14]. We use the GMP infinite-precision arithmetic
library to deal with rational numbers. Our implementation and benchmarks are available
at https://es.fbk.eu/people/irfan/papers/cade17-smt-nta.tar.gz.


Setup. We have run our experiments on a cluster equipped with 2.6GHz Intel Xeon
X5650 machines, using a time limit of 1000 seconds and a memory limit of 6 Gb.
    We have run M ATH SAT in two configurations: with and without universal check
for proving SAT (resp. called M ATH SAT and M ATH SAT- NO U NI SAT).
    The other systems used in the experimental evaluation are D R EAL [13], iSAT3 [24],
and M ETI TARSKI [1], in their default configurations (unless otherwise specified). Both
iSAT3 and D R EAL were also run with higher precision than the default one. The dif-
ference between the two configurations is rather modest and, when run with higher
precision, they decrease the number of M AYBE S AT answers. M ETI TARSKI can prove
the validity of quantified formulae, answering either valid or unknown. As such, it is
unfair to run it on satisfiable benchmarks. In general, we interpret the results of the
comparison taking into account the features of the tools.


Benchmarks. We consider three classes of benchmarks. First, the bounded model
checking (BMC) benchmarks are the results of unrolling transition systems with non-
linear and transcendental transition relations, obtained from the discretization of hybrid
automata. We took benchmarks from the distributions of iSAT3, from the discretization
(by way of H Y C OMP [6] and NU X MV [4]) of benchmarks from [8] and from the hybrid
model checkers H Y ST [3] and H ARE [23]. Second, the Mathematical benchmarks are
taken from the M ETI TARSKI distribution. These are benchmarks containing quantified
formulae over transcendental functions, and are all valid, most of them corresponding
to known mathematical theorems. We selected the M ETI TARSKI benchmarks without
quantifier alternation and we translated them into quantifier-free SMT(NTA) problems.
The third class of benchmarks consists of 944 instances from the D R EAL distribution
that contain transcendental functions.
    Both the mathematical and the D R EAL benchmarks contain several transcendental
functions (log, cos, ...) that are not supported natively by our prototype. We have there-
fore applied a preprocessing step that rewrites those functions in terms of exp and sin.8
iSAT3 requires bounds on the variables and it is unable to deal with the benchmarks
above (that either do not specify any bound or specify too wide bounds for the used
variables). Thus, we scaled down the benchmarks so that the variables are constrained
in the [−300, 300] interval since for higher bounds iSAT3 raises an exception due to
reaching the machine precision limit. Finally, for the BMC benchmarks, we run iSAT3
in BMC mode, in order to ensure that its optimized unrolling is activated.


BMC and Mathematical Results. In Table 1, we present the results. The benchmarks
are classified as either S AT or U NSAT when at least one of the solvers has been able to
return a definite answer. If only M AYBE S AT answers are returned, then the benchmark
is classified as U NKNOWN. For each tool, we report the number of answers produced
within the used resource limits. For the M AYBE S AT benchmarks, the numbers in paren-
theses indicate the instances which have been classified as S AT/U NSAT by at least one
other tool. For example, an entry “87 (32/7)” means that the tool returned M AYBE S AT
for 87 instances, of which 32 were classified as S AT and 7 U NSAT by some other tool.9
 8
   Sometimes we used a relational encoding: e.g. if ϕ contains arcsin(x), we rewrite it as
   ϕ{arcsin(x) 7→ asx } ∧ sin(asx ) = x ∧ − πb2 ≤ asx ≤ πb2 , where asx is a fresh variable.
 9
   There was no case in which two tools reported S AT and U NSAT for the same benchmark.
Benchmarks                Bounded Model Checking (887)       Mathematical (681)
Result                SAT UNSAT         MaybeSAT          SAT UNSAT MaybeSAT
M ETI TARSKI          N.A. N.A.            N.A.           N.A.   530      N.A.
M ATH SAT              72    553           N.A.            0     210      N.A.
M ATH SAT- NO U NI SAT 44    554           N.A.            0     221      N.A.
iSAT3                 N.A. N.A.            N.A.           N.A. N.A.       N.A.
D R EAL               N.A.   392        281 (67/23)       N.A.   285   316 (0/253)
Benchmarks            Scaled Bounded Model Checking (887) Scaled Mathematical (681)
Result                SAT UNSAT         MaybeSAT          SAT UNSAT MaybeSAT
M ATH SAT              84    556           N.A.            0     215      N.A.
M ATH SAT- NO U NI SAT 48    556           N.A.            0     229      N.A.
iSAT3                  35    470         87 (32/7)         0     212   137 (0/115)
D R EAL               N.A.   403        251 (77/23)       N.A.   302   245 (0/195)
                   Table 1. Results on the BMC and Metitarski benchmarks.



     First, we notice that the universal SAT technique directly results in 72 benchmarks
proved to be satisfiable by M ATH SAT, without substantial degrade on the U NSAT
benchmarks. Second, we notice that M ETI TARSKI is very strong to deal with its own
mathematical benchmarks, but is unable to deal with the BMC ones, which contain fea-
tures that are beyond what it can handle (Boolean variables and tens of real variables).10
     In the lower part of Table 1, we present the results on the scaled-down benchmarks,
so that iSAT3 can be run. The results for D R EAL and M ATH SAT are consistent with
the ones obtained on the original benchmarks – the benchmarks are slightly simplified
for M ATH SAT, that solves 12 more S AT instances and 2 more U NSAT ones, and for
D R EAL , that solves 11 more U NSAT instances. The performance of iSAT3 is quite good,
halfway between D R EAL and M ATH SAT on the bounded model checking benchmarks,
and slightly lower than M ATH SAT on the mathematical ones. In the BMC benchmarks,
iSAT3 is able to solve 35 S AT and 470 U NSAT instances, 102 more than D R EAL and
135 less than M ATH SAT.
     The M AYBE S AT results need further analysis. We notice that both iSAT3 and
D R EAL often return M AYBE S AT on unsatisfiable benchmarks (e.g. all the mathematical
ones are U NSAT). There are many cases where D R EAL returns a D ELTA S AT result, but
at the same time it prints an error message stating that the numerical precision limit has
been reached. Thus, it is unlikely that the result is actually D ELTA S AT, but it should
rather be interpreted as M AYBE S AT in these cases.11


D R EAL Benchmarks Results. The D R EAL benchmarks turn out to be very hard. The
results are reported in Table 2, where we show the performance of D R EAL both on the
original benchmarks and on the ones resulting from the removal via pre-processing of
10
   According to the documentation of M ETI TARSKI, the tool is ineffective for problems with
   more than 10 real variables. Our experiments on a subset of the instances confirmed this.
11
   We contacted the authors of D R EAL and they reported that this issue is currently under inves-
   tigation.
    Benchmarks           D R EAL (all) (944)     Benchmarks D R EAL (exp/sin only) (96)
    Status          SAT UNSAT MaybeSAT Status                  SAT UNSAT MaybeSAT
    D R EAL (orig.) N . A .  102     524(3/4) D R EAL (orig.) N . A . 17    37 (3/3)
    M ATH SAT         3       68        N.A.     M ATH SAT      3     39      N.A.
    D R EAL         N.A.      44      57(3/4)
                            Table 2. Results on the Dreal benchmarks.



the transcendental functions not directly supported by M ATH SAT. The results shows
that in the original format D R EAL solves many more instances, and this suggests that
dealing with other transcendental functions in a native manner may lead to substantial
improvement in M ATH SAT too. Interestingly, if we focus on the subset of 96 bench-
marks that only contain exp and sin (and are dealt by M ATH SAT without the need of
preprocessing), we see that M ATH SAT is significantly more effective than D R EAL in
proving unsatisfiability, solving more than twice the number of instances (right part of
Table 2).
    We conclude by noticing that overall M ATH SAT solves 906 benchmarks out of
2512, 127 more than D R EAL, the best among the other systems. A deeper analysis of the
results (not reported here for lack of space) shows that the performance of the solvers is
complementary: the “virtual-best system” solves 1353 benchmarks. This suggests that
the integration of interval propagation may yield further improvements.


7   Conclusion
We present a novel approach to Satisfiability Modulo the theory of transcendental func-
tions. The approach is based on an abstraction-refinement loop, where transcendental
functions are represented as uninterpreted ones in the abstract space SMT(UFLRA), and
are incrementally axiomatized by means of piecewise-linear functions. We experimen-
tally evaluated the approach on a large and heterogeneous benchmark set: the results
demonstrates the potential of our approach, showing that it compares favorably with
both delta-satisfiabily and interval propagation and with methods based on theorem
proving.
     In the future we plan to exploit the solver for the verification of infinite-state tran-
sition systems and hybrid automata with nonlinear dynamics, and for the analysis of
resource consumption in temporal planning. Finally we would like to define a unifying
framework to compare linearization and interval propagation, and to exploit the poten-
tial synergies.


References
 1. Akbarpour, B., Paulson, L.C.: Metitarski: An automatic theorem prover for real-valued spe-
    cial functions. JAR 44(3), 175–205 (2010)
 2. Allamigeon, X., Gaubert, S., Magron, V., Werner, B.: Certification of inequalities involving
    transcendental functions: combining sdp and max-plus approximation. In: Control Confer-
    ence (ECC), 2013 European. pp. 2244–2250. IEEE (2013)
 3. Bak, S., Bogomolov, S., Johnson, T.T.: HYST: a source transformation and translation tool
    for hybrid automaton models. In: Proceedings of the 18th International Conference on Hy-
    brid Systems: Computation and Control. pp. 128–133. ACM (2015)
 4. Cavada, R., Cimatti, A., Dorigatti, M., Griggio, A., Mariotti, A., Micheli, A., Mover, S.,
    Roveri, M., Tonetta, S.: The nuXmv symbolic model checker. In: CAV. Springer (2014)
 5. Cimatti, A., Griggio, A., Irfan, A., Roveri, M., Sebastiani, R.: Invariant checking of NRA
    transition systems via incremental reduction to LRA with EUF. In: Legay and Margaria [16],
    pp. 58–75, also available at https://es-static.fbk.eu/people/griggio/papers/
    tacas17.pdf
 6. Cimatti, A., Griggio, A., Mover, S., Tonetta, S.: HyComp: An SMT-based model checker for
    hybrid systems. In: TACAS. pp. 52–67. Springer (2015)
 7. Cimatti, A., Griggio, A., Schaafsma, B.J., Sebastiani, R.: The MathSAT5 SMT solver. In:
    TACAS. LNCS, vol. 7795, pp. 93–107. Springer (2013)
 8. Cimatti, A., Mover, S., Sessa, M.: From electrical switched networks to hybrid automata. In:
    FM. pp. 164–181. Springer (2016)
 9. de Dinechin, F., Lauter, C., Melquiond, G.: Certifying the floating-point implementation of
    an elementary function using gappa. IEEE Trans. Comput. 60(2), 242–253 (Feb 2011)
10. Eggers, A., Kruglov, E., Kupferschmid, S., Scheibler, K., Teige, T., Weidenbach, C.: Super-
    position modulo non-linear arithmetic. In: FroCoS. LNCS, vol. 6989, pp. 119–134. Springer
    (2011)
11. Fränzle, M., Herde, C., Teige, T., Ratschan, S., Schubert, T.: Efficient solving of large non-
    linear arithmetic constraint systems with complex boolean structure. JSAT 1(3-4), 209–236
    (2007)
12. Gao, S., Avigad, J., Clarke, E.M.: δ-complete decision procedures for satisfiability over the
    reals. In: IJCAR. pp. 286–300. Springer (2012)
13. Gao, S., Kong, S., Clarke, E.M.: dReal: An SMT solver for nonlinear theories over the reals.
    In: CADE. pp. 208–214. Springer (2013)
14. Gario, M., Micheli, A.: PySMT: a solver-agnostic library for fast prototyping of SMT-based
    algorithms. In: SMT. pp. 373–384 (2015)
15. Hazewinkel, M.: Encyclopaedia of Mathematics: Stochastic Approximation Zygmund
    Class of Functions. Encyclopaedia of Mathematics, Springer Netherlands (1993), https:
    //books.google.it/books?id=1ttmCRCerVUC
16. Legay, A., Margaria, T. (eds.): Tools and Algorithms for the Construction and Analysis of
    Systems - 23rd International Conference, TACAS 2017, Held as Part of ETAPS 2017, Up-
    psala, Sweden, April 22-29, 2017, Proceedings, Part I, Lecture Notes in Computer Science,
    vol. 10205 (2017)
17. Magron, V.: Nlcertify: A tool for formal nonlinear optimization. In: International Congress
    on Mathematical Software. pp. 315–320. Springer (2014)
18. Martin-Dorel, É., Melquiond, G.: Proving tight bounds on univariate expressions with ele-
    mentary functions in coq. Journal of Automated Reasoning 57(3), 187–217 (2016)
19. Melquiond, G.: Coq-interval (2011)
20. Nemhauser, G.L., Wolsey, L.A.: Integer and Combinatorial Optimization. Wiley-
    Interscience, New York, NY, USA (1988)
21. Nieven, I.: Numbers: rational and irrational. Mathematical Association of America (1961)
22. Ratschan, S.: Efficient solving of quantified inequality constraints over the real numbers.
    TOCL 7(4), 723–748 (2006)
23. Roohi, N., Prabhakar, P., Viswanathan, M.: HARE: A hybrid abstraction refinement engine
    for verifying non-linear hybrid automata. In: Legay and Margaria [16], pp. 573–588
24. Scheibler, K., Kupferschmid, S., Becker, B.: Recent Improvements in the SMT Solver iSAT.
    MBMV 13, 231–241 (2013)
25. Solovyev, A., Hales, T.C.: Formal verification of nonlinear inequalities with taylor interval
    approximations. In: NASA Formal Methods Symposium. pp. 383–397. Springer (2013)
26. Townsend, E.: Functions of a Complex Variable. Read Books (2007)
27. Weidenbach, C., Dimova, D., Fietzke, A., Kumar, R., Suda, M., Wischnewski, P.: SPASS
    version 3.5. In: CADE. LNCS, vol. 5663, pp. 140–145. Springer (2009)
