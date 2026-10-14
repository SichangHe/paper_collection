                                         Verifying Numerical Methods with Isabelle/HOL

                                             Dustin Bryant1 , Jonathan Julian Huerta y Munive2 , and Simon Foster3
                                                                         1
                                                                             Independent, USA
                                                           2
                                                               University of Aalborg, Copenhagen, Denmark
                                                                        3
                                                                          University of York, UK
arXiv:2511.20550v4 [cs.LO] 22 Sep 2026




                                               Abstract. Modern machine learning pipelines and ODE solvers are
                                               built on numerical algorithms. Reliable numerical methods are thus a
                                               prerequisite for trustworthy machine learning and cyber-physical sys-
                                               tems. We evaluate a framework designed for verifying imperative pro-
                                               grams and the Isabelle proof assistant as tools for proving the total cor-
                                               rectness of four numerical algorithms: the bisection method, the fixed-
                                               point method, the perceptron, and the gradient descent algorithm. Our
                                               verifications required subtle extensions and generalisations to Isabelle’s
                                               version of Taylor’s theorem and higher-order derivatives. Finally, we re-
                                               flect on the framework’s automation, friendly syntax, and on further
                                               requirements to turn it into a verification tool for numerical methods.


                                         1   Introduction
                                         Numerical methods are an important class of algorithms that iteratively ap-
                                         proximate solutions to mathematical problems. They often employ concepts
                                         from linear algebra and analysis, and are foundational to machine learning. For
                                         instance, stochastic gradient descent, the backbone of modern neural network
                                         training, minimises cost functions by approximating their gradients and updat-
                                         ing the network’s weights accordingly. While such algorithms have well-known
                                         mathematical foundations, work on their formal verification is still in its infancy.
                                             Verification of numerical algorithms is challenging for several reasons. Firstly,
                                         their formalisation requires mature libraries of diverse mathematical concepts,
                                         such as matrices, transcendental functions, and their derivatives. Secondly, de-
                                         spite the existence of various methods for verifying iterative methods [19,26,15],
                                         their implementations still require expertise in functional programming and in
                                         the idiosyncrasies of the verification tools employed. Finally, proof automation
                                         has remained a bottleneck for the adoption of these tools. We therefore in-
                                         vestigate whether verifying numerical methods with an interface closer to the
                                         best-known imperative programming paradigm, and that also alleviates specific
                                         prover knowledge with automation, is feasible.
                                             If possible, this would contribute to enabling a wider audience to verify nu-
                                         merical methods by lowering the barrier to using these high-assurance tools. Two
                                         developments make the evaluation of this question more achievable: the growth of
                                         formalised libraries of Analysis and Ordinary Differential Equations [11,13,16,31],
                                         and the creation of frameworks for imperative program verification on top of
these [8,9,12]. Considering this, we contribute a qualitative assessment of one of
these imperative programming frameworks by using it to verify the total cor-
rectness of four numerical algorithms.
    We choose the Isabelle/ITrees framework [9] that provides user-friendly pro-
gramming syntax together with understandable Hoare logic specifications and
automation for verification condition generation (VCG). Discharging the re-
sulting VCs only requires application and development of foundational theo-
rems from multivariate analysis, many of which are provided by Isabelle’s HOL-
Analysis package. Isabelle’s Sledgehammer tool largely aids in the proving process,
and substantially automates the verification. Moreover, the use of ITrees means
we can execute the algorithms in Isabelle and generate code that intrinsically
has a high degree of assurance in its correctness.
    We extend Isabelle/ITrees to support real valued vectors and matrices (Sec-
tion 2) and use it to prove the total correctness of four numerical algorithms:
the bisection method (Section 3), the fixed-point method (FPM - Section 4),
the perceptron (Section 5), and the gradient descent algorithm (Section 6). To
achieve this, we substantially extend Isabelle’s Analysis libraries with generali-
sations of higher-order derivatives and Taylor’s formula with a Peano remainder.
Our experience is generally positive, requiring the following steps for each nu-
merical method: (1) model the algorithm in Isabelle/ITrees, (2) experiment with
the algorithm by executing it, (3) write its correctness specifications, (4) pose
a suitable set of invariants and variants, (5) use the VCG automation to pro-
duce proof obligations, (6) if required, prove theorems from Analysis to aid in
discharging the proof goals and (7) repeat from step 4 until the postcondition
is proved. We conclude our paper by discussing related (Section 8) and future
work (Section 9). To our knowledge, this is the first application of an imperative
verification framework to a diverse set of numerical algorithms.
    While this paper focuses on a version of these algorithms using arbitrary
precision, we have also explored a generative AI-based autoformalisation ap-
proach [6] to adapt our manual verifications to floating-point arithmetic. We
believe that the formalisation of these algorithms (and others omitted due to
space constraints) via Isabelle/ITrees and the Isabelle/HOL libraries cements
these tools as a foundation for verifying numerical algorithms. Our formalisa-
tions are available via GitHub and links to them appear throughout.


2   Isabelle/ITrees

We describe relevant features of the Isabelle/ITrees library [9] and showcase the
extensions that we implemented to enable its support for numerical methods.
    Isabelle/ITrees is part of the Isabelle/UTP semantics and verification ecosys-
tem [8]. The library provides an abstract imperative programming notation,
mechanisms for total-correctness specifications, (in)variant annotations, and a
verification-condition generator. The programs are assigned a formal semantics
in terms of Interaction Trees (ITrees), which unify denotational and operational
semantics. In particular, ITrees, as coinductively defined data structures, are ex-
  ecutable in nature, and the library leverages Isabelle’s code generator for this.
  We extend the existing tool to support real number variables by using the HOL-
  Analysis library and providing implementations of vector and matrix operations
  to the code generator, enabling the execution of numerical algorithms.
      Consider a program for scalar-vector multiplication in Isabelle/ITrees:

1 alphabet (’n :: finite ) st = i::nat vc::"real vec[’n]"
2
3 program vec_scale "(c :: real , X ::real vec[’n])" =
4 "vc := X; i := 0;
5 while i < CARD(’n) do vc[i] := c * X(i); i := i + 1 od"

  Here, the alphabet command declares the program’s state space, consisting of
  two variables: the natural number i, and the (real) vector vc. The state type st
  is parametric over type ’n, which is the vector’s dimension of finite cardinality.
      We define program vec scale using the program keyword. The program
  takes as input the (real) scalar c, and a vector X of dimension ’n. Having ini-
  tialised vc and i to X and 0 respectively, the program iterates through each ele-
  ment of vc, performing a point-wise multiplication. The notation CARD(’n) gives
  the dimension of the vector as a natural number. The operation X(i) retrieves
  the ith element of X. We can run the program using the execute keyword:

1 execute " vec_scale (3, Vector [1 ,2 ,3 ,4])"

  The Vector notation builds a vector of the inferred dimension (4). The execute
  command compiles the vec scale program to an ITree, generates SML code,
  and then executes the code. Isabelle reports that the program terminates with
  state i = 4, vc = Vector[3, 6, 9, 12]. Execution is feasible only when the
  real number inputs are rational, and so supported by multi-precision arithmetic.
      We can verify such a numerical algorithm using Hoare logic. The Hoare triple
  below states a total correctness claim that the program terminates and, in the
  final state, vc is the result of a scalar multiplication, denoted in Isabelle via ∗R .

1 lemma "H[True] vec_scale (c, X) [vc = c ∗R X]"

  Isabelle/ITrees includes the vcg proof method, which applies Hoare logic laws
  to produce verification conditions. This often requires annotating the program
  with loop (in)variants [8,9,12]. Below, we add to vec scale both,

1 while i < CARD(’n)
2   invariant i ≤ CARD(’n) ∧ (∀k<i. vc k = c * X k)
3   variant CARD(’n) - i do ... od

  where the dots (...) abbreviate the above body of the while-loop. The vcg
  method yields the extensionality principle for vectors as a proof obligation.
  Namely, if each element of the vector vc is c times the corresponding element of
  X, then vc is the scalar multiple c ∗R X. This VC can be discharged automati-
  cally by application of Isabelle’s Sledgehammer tool.
 3    Bisection Method
 We begin assessing Isabelle/ITrees’ suitability for verifying numerical algorithms
 with the bisection method—a classic, derivative-free root-finding algorithm. We
 choose it because it is an accessible entry point to the field. We describe its
 implementation, justify the correctness specification and loop invariants, and
 discuss the challenges in the corresponding proof.
     Recall from Bolzano’s Theorem that a real-valued function f , continuous on
 a closed interval [a, b] ⊆ R, and such that f (a) and f (b) have opposite signs,
 has a root inside the open interval (a, b). The bisection method iterates this
 aforementioned fact (see Listing 1.1): at each step n, it defines the current bracket
 as an interval, [ln , un ], that halves the previous bracket (where [l0 , u0 ] = [a, b]).
 The bisection method evaluates f at the bracket’s midpoint mn = (ln + un )/2,
 and retains the bracket’s half on which the sign change persists. It repeats this
 process until the bracket’s length falls below a given threshold. This halving
 process explains the term bisection. The algorithm is formalised below:

1 program bisection "( f::real⇒real , a::real , b::real , tol::real )"
2   over state = "iter:= 0; fa:= f(a); fb:= f(b); l:= a; u:= b;
3   xmid:= l; ymid:= f(xmid);
4     while u-l>tol do
5       iter:= iter +1; xmid:= (l+u)/2; ymid:= f(xmid);
6       if fa*ymid >0 then l:= xmid; fa:= ymid
7       else u:= xmid; fb:= ymid fi od"
                       Listing 1.1. Bisection method in Isabelle

     We initialise the bracket [l, u] to [a, b], while fa and fb denote the value of
 the input function f at the bracket’s left and right limits. The while loop checks
 that the bracket’s size is strictly larger than the input tolerance (u-l>tol), while
 the loop’s body computes the current bracket’s midpoint xmid:=(l+u)/2 and
 the value of f at that midpoint, ymid. The chosen half of the bracket depends
 on the sign agreement of f at the left endpoint and midpoint (fa*ymid > 0).
     Having discussed the intuition for the algorithm’s behaviour, we state the
 bisection method’s total correctness below and explain our assumptions.

1 theorem bisection_error_bound:
2   assumes "0 < tol" "tol < b-a"
3     "f(a)*f(b) < 0" " continuous_on {a..b} f"
4   shows "H[True] bisection (f,a,b,tol) [
5     ∃c. f(c) = 0 ∧ c ∈ {a<..<b} ∧ u-l ≤ tol
6     ∧ ¦c - xmid¦ ≤ (b-a)/2^ iter
7     ∧ ¦c - xmid¦ ≤ tol ∧ iter = ⌈log 2 (b-a)/tol⌉]"
                Listing 1.2. Total correctness of the bisection method

 The theorem in Listing 1.2 asserts that bisection terminates, returning xmid
 as an approximation to a root
                             of f. That
                                       is, xmid is at most a distance of tol
 to a root c after precisely log2 b−a
                                  tol    iterations, provided f is continuous on
    [a, b]. We assume continuity on [a, b] and f(a)*f(b)<0 so that we may apply
    Bolzano’s theorem. The assumptions tol<b-a and 0<tol guarantee a nonempty
    initial domain and the possibility of termination. Notably, our implementation
    of the method does not terminate if f(xmid)=0.
        Finding the right variant was crucial (and challenging) to prove the termi-
    nation of the bisection method. The program’s loop (in)variants are below.

1       invariant fa = f(l) ∧ fb = f(u) ∧ (l = xmid ∨ u = xmid)
2       ∧ a ≤ l ∧ u ≤ b ∧ l < u ∧ fa*fb ≤ 0
3       ∧ u-l = (b-a)/2^ iter ∧ 2*(u-l) > tol
4       variant nat(⌈log 2 (b-a)/tol⌉) - iter

    The conjuncts fa=f(l) and fb=f(u) state that the cached values fa and fb
    agree with those of the function at the bracket’s endpoints l and u. The dis-
    junction l = xmid ∨ u = xmid declares that each iteration replaces one of the
    interval’s endpoints by the midpoint xmid, corresponding to either the then or
    else branch in Listing 1.1. The bounds a ≤ l, l < u, and u ≤ b state that the
    bracket remains a nonempty subinterval of [a, b]. The sign condition fa*fb ≤ 0
    preserves applicability of Bolzano’s theorem; again we note that since possi-
    bly f(xmid)=0 it could be the case that fa*fb=0. Bolzano is only applicable
    if fa*fb < 0, but fortunately vcg handles these cases separately. Finally, the
    invariant u-l=(b-a)/2iter captures the bracket’s halving at each iteration.
        From the above invariants,    one
                                         can prove that the program’s iterations iter
    are bounded below by log2 b−a
                             
                                    tol   . To derive the exact value for iter (to derive
    the variant), we observe that the while loop’s condition is always respected in
    the predecessor step and the bracket’s size is always halved: tol < ui−1 − li−1 =
    2 · (ui − li ), which remains true when iter=0 by the assumptions 0<tol<b-a.
    From this observation, the violation of the loop’s condition at   the last 
                                                                                 iteration
    and the second-to-last invariant, the number of iterations is log2 b−a  tol    .
        With the aforementioned loop (in)variants, Isabelle/ITrees’ vcg method gen-
    erates 15 goals in total, 13 of which can be proven directly with Isabelle’s Sledge-
    hammer. The remaining two proof obligations are symmetrical and related to the
    last invariant. With algebraic manipulations, one can discharge them.
        Overall, the formalisation and verification of the bisection method required
    195 lines of Isabelle code under the counting convention of Section 7. Notably,
    Isabelle/ITrees enables the straightforward formalisation of the algorithm, its
    correctness specification, and loop (in)variants. Furthermore, the framework’s
    automation reduces the bisection method’s proof of correctness to a single goal,
    up to symmetry, proven by application of Bolzano’s Theorem and some algebra.
    Thus, the verification process for this program is highly automated.


    4    Fixed-Point Method
    We now focus on a numerical method with stronger mathematical prerequisites,
    the fixed-point method (FPM). As before, we discuss the algorithm’s formalisa-
    tion, its correctness specification, and the challenges and intuitions in proving it.
 In particular, our analysis of the conditions under which the FPM is applicable
 requires expanding the libraries of formalised mathematics in Isabelle with an
 implementation of higher-order differentiability and Taylor’s theorem.
      As the name hints, the FPM approximates a fixed point of its input function
 f . These are points r such that f (r) = r. It is also a root-finding method since
 f (r) = r is equivalent to f (r) − r = 0. The FPM starts from an initial guess x0
 and repeatedly applies f , generating a sequence xn+1 = f (xn ) converging to r.
 Informally, its convergence relies on assuming that the input function f reduces
 the distance between points in a neighbourhood S of x0 after each application.
 Formally, it relies on f satisfying the conditions of the Banach fixed-point the-
 orem, that is, S should be a contractive neighbourhood of the initial point x0
 under f (namely, |f (x) − f (y)| ≤ c · |x − y| for all x, y ∈ S, where c < 1). As
 before, the program’s formalisation is straightforward in the framework:

1 program fpm "( f::real⇒real , x0::real , tol::real )" over st
2   ="x := x0; x_new := f x; iter := 0;
3   while (¦x_new - x¦ ≥ tol) do
4     x := x_new; x_new := f x; iter := iter + 1 od"
                    Listing 1.3. Fixed-point method in Isabelle

 In Listing 1.3, the variables x :: R and x new :: R correspond to xn and xn+1
 respectively, where n is the number of iterations iter :: N. The distance test
 |x new − x| ≥ tol controls the loop’s termination. Irrespective of this test, the
 loop’s body executes the assignments x := x new, x new:= f x, and iter:=
 iter + 1. The loop exits when the latest distance falls below the tolerance. A
 first, total correctness theorem for the fixed point method appears below.

1 lemma fpm_iter_bnd_local_leq:
2   assumes "0 ≤ c" "c < 1" "0 < tol" "0 < δ" "f r = r"
3     and "¦x0 - r¦ ≤ δ"
4     and "∀s t. ¦s - r¦ ≤ δ ∧ ¦t - r¦ ≤ δ
5       −→ ¦f s - f t¦ ≤ c*¦s - t¦"
6   shows "H[True] fpm(f, x0 , tol)[
7   ¦x-r¦≤c ^ iter * ¦x0 -r¦ ∧ ¦x_new -x¦<tol
8   ∧ iter ≤ Suc (nat⌈ln (max 1 (¦f x0 - x0¦/tol))/ln (1/c)⌉)]"
      Listing 1.4. Total correctness of the FPM in a contractive neighbourhood

    The first two assumptions in Listing 1.4 specify the contraction constant,
 while the last assumption characterises contractivity. We choose an interval of
 radius δ > 0 as the contractive neighbourhood of the initial guess and assume
 that a fixed point of f exists in this interval. We also proved a version of the
 aforementioned lemma that replaces ≤ in the assumption | x0 − r |≤ δ with <,
 and similarly replacing it in the antecedent of the final assumption. Below, we
 write our loop invariants and variant for the FPM:

1 invariant x = (f^^ iter) x0 ∧ x_new = f x
2   ∧ ¦x_new -x¦ ≤ (c^iter)*¦f x0 -x0¦
3     ∧ iter ≤ Suc nat⌈ln(max 1 (¦f x0 - x0¦/tol))/ln (1/c)⌉)
4    variant Suc(nat⌈ln(max 1 (¦f x0 - x0¦/tol))/ln (1/c)⌉) - iter

    The first invariant x = fiter x0 specifies that, at iteration iter, the variable x
    holds the iter-th application of f to the initial guess, and x new = f x relates
    each iteration to the next one. Also, contractivity implies that the step sizes
    decay geometrically, thus |xk+1 − xk | ≤ c k |f (x0 ) − x0 |. To prove termination
    without an explicit max iter, we derive a closed-form iteration bound from the
    loop guard and apply induction on k. Notice that c is missing from the program.
    We can reason about it from the (in)variants with a renaming aid where we
    define fpm aux(f, x0, tol,c) (which receives the ghost variable c), and prove
    it equivalent to the original: fpm aux(f, x0, tol,c) = fpm(f, x0, tol).
          After applying vcg, four proof obligations emerge: one discharged by Sledge-
    hammer, one requiring an induction, and the remaining needing straightforward
    algebraic manipulations with intermediate steps discharged by Sledgehammer.
          As stated above, the total correctness theorem requires its users to identify
    the contraction constant c for f on a neighbourhood around the fixed point. To
    alleviate these burdens, we use the rest of the Section to formalise two results
    that establish conditions under which a contractive neighbourhood exists. For
    this, we closely follow Solomon’s presentation [29].
          Firstly, we consider a continuously differentiable function f ∈ C 1 (U ) such
    that |f ′ (r)| < 1. We can find an ε > 0, such that 1 − |f ′ (r)| − ε > 0. Then by
    continuity of f ′ , there is also a δ > 0 such that, if |x − r| < δ, then 1 − ε −
    |f ′ (r)| > |f ′ (x) − f ′ (r)|. By the triangle inequality, |f ′ (x)| < 1 − ε holds in a
    neighbourhood of radius δ around the fixed point r. Then, by the mean value
    theorem |f (x) − f (r)| = |f ′ (θ)||x − r| for some θ if x ∈ [r − δ, r + δ]. Hence,
    |f (x) − f (r)| < (1 − ε)|x − r|. Thus, users only need to provide a C 1 function
    and an initial guess x0 close to the fixed point. The formal statement appears
    below, and as before, we may replace the ≤ in the goal’s antecedent with <.

1 lemma fpm_known_iter_bnd_C1_leq:
2 assumes "f r = r" "r ∈ U" " C_k_on 1 f U"
3   and "¦deriv f r¦ < 1" "0 < tol"
4 shows "∃ δ > 0. ∃ ε > 0. (∀(x0 :: real). ¦r - x0¦ ≤ δ
5   −→ H[True] fpm(f, x0 , tol) [¦x - r¦ ≤ (1 - ε)^iter*¦x0 - r¦
6     ∧ ¦x_new - x¦ < tol ∧
7     iter ≤ Suc(nat⌈ln(max 1 (¦f x0 - x0¦/tol))/ ln (1/(1 -ε))⌉)])"
                 Listing 1.5. Convergence when f ∈ C 1 (U ) and | f ′ (r) |< 1


       The second case that we consider requires the first derivative of f at the fixed
    point to be 0 (f ′ (r) = 0), and the second derivative f ′′ (r) to exist. Since f is
    twice differentiable, by Taylor’s theorem in its Peano remainder form, there is a
    function h, tending to 0 at xn , such that

                                                  f ′′ (r)               h(xn )
         f (xn ) = f (r) + f ′ (r) · (xn − r) +            · (xn − r)2 +        · (xn − r)2 .
                                                      2                    2
 We can replace h(xn ) by an appropriate ε > 0 and use the triangle inequality to
 derive the following bound on an iterate of the FPM:
                                                   1 ′′
                |xn+1 − r| = |f (xn ) − f (r)| ≤     |f (r) + ε| · (xn − r)2 .
                                                   2
 That is, the distance between the next iteration and the desired fixed point re-
 duces quadratically. This is often highlighted to indicate that under the above-
 stated conditions, the FPM converges faster (quadratically). We have also for-
 malised this result and proven it using features of the Isabelle/ITrees framework.


1 lemma fpm_iter_quadratic_convergence:
2   assumes "f(r) = r" "r ∈ U" " C_k_on 1 f U"
3     and "deriv f r = 0" "0 < tol" "f twice_differentiable_at r"
4   shows "∃(δ :: real) >0. ∃(ε :: real) >0. (∀x0. ¦r - x0¦ < δ
5     −→ H[True] fpm(f, x0 , tol) [¦x_new - x¦ < tol ∧ ¦x-r¦
6     ≤ (((¦deriv(deriv f) r¦ + ε)/2) ^(2^ iter -1))*¦x0 -r¦^(2^ iter)
7 ∧ iter ≤ Suc(nat⌈ln(max 1 (¦f x0 - x0¦/tol)) / ln (1/(1 -ε))⌉)])"
     Listing 1.6. Quadratic conv. when f ∈ C 1 (U ), f twice diff. at r, and f ′ (r) = 0

     Unlike the bisection method, the formalisation and verification of these re-
 sults are not straightforward. Concretely, the goals that emerged from the vcg
 method on the specification in Listing 1.4 are not automatically discharged with
 Sledgehammer. Yet, their proofs are still relatively simple, requiring simple in-
 ductions with intermediate steps that Sledgehammer can prove. However, our
 formalisation and verification of the specifications in Listings 1.4, 1.5, and
 1.6 require several, long ε − δ arguments, making the fixed-point development
 span 1111 lines of Isabelle code under the counting convention of Section 7.
 This number does not account for the extensions to the libraries of formalised
 mathematics in Isabelle that we needed to state our correctness specifications.
 Namely, to assert the conditions related to the higher-order differentiability of
 the input function f and the possibility of approximating f via a Taylor expan-
 sion, the existing libraries were insufficient. In particular, to our knowledge, we
 contribute (1) the most general definition of higher-order differentiability in any
 Isabelle library (all other concepts in the AFP either imply ours or are instances
 of ours) and (2) the only formalisation of Taylor’s theorem in its Peano form.
 These contributions, along with further concepts from vector calculus, span 4754
 lines of Isabelle code under the same convention.


 5    Perceptron

 The perceptron is a supervised learning algorithm for binary classification, which
 seeks parameters theta ∈ Rn and bias ∈ R such that sgn(xi ·theta+bias) = yi
 for each labelled example (xi , yi ) in a dataset D, where yi ∈ {−1, +1} is the label
 of xi ∈ Rn . The algorithm is a semi-decision procedure for linear separability: it
 terminates after finitely many iterations with a pair (theta, bias) that correctly
 classifies all examples if and only if the data is linearly separable. Geometrically,
 H (θ, b) = {x | x · θ + b = 0} defines a hyperplane with θ as a normal vector and
 the objective is to find (theta, bias) such that H (theta, bias) strictly divides
 the two classes with a positive margin γ > 0. Below, we present the algorithm
 in two stages: pass through, which “learns” from the data, and perceptron,
 which repeatedly iterates pass through until no misclassifications are detected.

1 program pass_through "D :: (( real vec[’n]) × real) list"
2   over "(’n :: finite ) state"
3   =" changed: = False; i:= 0;
4   while i < length D do x_i:= fst (D!i); y_i:= snd (D!i);
5      if y_i*(x_i•theta+bias)≤0 then theta: = theta+y_i* R x_i; bias:
      = bias+y_i;
6      updates: = updates +1; changed: = True fi; i:= i+1 od"
       Listing 1.7. One pass (epoch) of the perceptron over the training data.


1 program perceptron "D :: (( real vec[’n]) × real) list"
2 over "(’n :: finite ) state"
3 = " theta: = 0; bias:= 0; changed: = True; updates: = 0;
4 while changed do pass_through D od"
 Listing 1.8. The classic perceptron as repeated passes until an epoch makes no
 updates.


     The variable updates::nat counts the number of changes to the ordered
 pair (theta, bias), while changed::bool records if pass through updated the
 pair at least once. In such a case, the perceptron will call pass through again.
 The updates are assignments theta := theta + yi ∗ xi and bias := bias + yi
 and occur only when the sign of yi and xi · theta + bias do not match. That is,
 when xi is on the wrong side of H (theta, bias).
     The perceptron convergence theorem (PCT) says that if the data are linearly
 separable with margin γ > 0, and all the datapoints (xi , yi ) are inside the circle
 of radius R > 0 (∥xi ∥2 + 1 ≤ R2 ), then the perceptron makes at most (R/γ)2
 updates before it finds parameters (theta, bias) that correctly classify all points
 in D. We formalise the PCT as:

1 theorem perceptron_convergence_theorem:
2   assumes V"γ > 0" "∥θ∥2 + b2 = 1"
3     and " t. t < length D =⇒
4     ∥fst(D!t)∥2 + 1 ≤ R 2 ∧ snd(D!t)∈{-1, 1} ∧ snd(D!t)*(fst(D!t)
      •θ+b) ≥ γ"
5   shows "H[True] perceptron (D) [real updates ≤ (R/γ) 2
6     ∧ (∀i < length D. sgn(fst(D!i) • theta + bias) = snd(D!i))]"
                  Listing 1.9. The perceptron convergence theorem
     The assumption about separability is an existential assertion of a hyperplane
 H (θ, b). To address this, we define the program perceptron aux (D, θ, b, γ, R)
 (with its respective pass-through) that receives as inputs the ghost variables
 R, γ, θ, and b, but that is otherwise indistinguishable from the original per-
 ceptron program. In our formalisation, we perform the invariant reasoning on
 this auxiliary program and show that introducing these new variables does not
 change the semantics: perceptron aux (D, θ, b, γ, R) = perceptron (D). The
 loop variants and invariants of pass through aux and perceptron aux are
 shown below.

1 invariant updates*γ ≤ (θ•theta)+( b*bias ) ∧ ∥theta∥2 + bias 2 ≤
      updates*R 2
2 ∧ ( changed −→ old[ updates ]< updates ) ∧ (¬changed −→ updates =
      old[ updates ])
3 ∧ (¬ changed −→ (∀j < i. (snd(D!j))*(( fst(D!j)) • theta + bias
      ) > 0))
4 variant length D-i
                Listing 1.10. Loop (in)variants of pass through aux


1 invariant updates*γ ≤ (θ•theta)+( b*bias ) ∧ ∥theta∥2 + bias 2 ≤
      updates*R 2
2 ∧ (¬ changed −→(∀j < length D. (snd(D!j))*(( fst (D!j)) • theta
      +bias) > 0))
3 ∧ updates ≤ nat ⌈(R/γ) 2 ⌉
4 variant (nat ⌈(R/γ) 2 ⌉ - updates + (if changed then 1 else 0))
                 Listing 1.11. Loop (in)variants of perceptron aux

     The first two invariants characterise the perceptron’s standard proof of con-
 vergence [22]. Namely, one must inductively show that the angle between the
 hyperplanes H (theta, bias) and H (θ, b) is bounded from below by the updates
 times the margin, and that the norm of the updated normal vector never grows
 larger than the radius R. From these, one deduces the maximum number of
 updates (R/γ)2 required for convergence of the perceptron (which is itself an
 invariant). Additionally, the Isabelle/ITrees framework includes an operator old
 enabling us to describe the state of a variable before its most recent assign-
 ment. Thanks to this helpful feature, the remaining invariants denote the above-
 described behaviour of updates and H (theta, bias) relative to the changed
 variable. The separation of the programs enables us to carry only the necessary
 invariants from the inner loop to the outer one. For the variants, the first one
 says that each iteration in a pass through the data decreases the number of data
 points to visit. The second one coincides with the main invariant, except for the
 fact that one has to consider that the program requires an extra pass through
 the data to certify that everything has been classified correctly. Thus, in the fi-
 nal iteration, there are no errors and the program terminates, but since updates
 does not change, the variants should still be decreased, which is expressed with
 the term (if changed then 1 else 0).
 6   Gradient Descent

 The gradient descent algorithm stands out among multidimensional optimisation
 methods for its simplicity and prominence in modern machine-learning practice.
 The method is so-named as it updates a vector approximation x :: R vec[’i]
 to a minimiser x min (a point x ∗ such that f (x ∗ ) ≤ f (x) for all x), by moving in
 the direction opposite to the steepest ascent. That is, it moves opposite to the
 gradient grad(x) of f at x, a distance of α(x)>0 at each step. The method exits
 its while-loop when the first-order optimality condition grad(x) • grad(x) ≤ ε2
 is satisfied. We showcase the formalisation of the method below.

1 program gradient_descent "(grad :: R vec[’i] ⇒ R vec[’i], x0 ::
       R vec[’i], α :: R vec[’i] ⇒ R, ε :: R)"
2   over " ’i::finite st" = "x:= x0; iter:= 0;
3   while (grad(x) • grad(x) > ε2 ) do x:= x-(α x)* R grad(x); iter:
      = iter +1 od"
                      Listing 1.12. Gradient descent algorithm


 The choice of step length α(x) in general depends on x, and on the optimisation
 problem. However, there is no general-purpose method for specifying its value,
 and in general, the method may not converge [24].
      We verified three versions of gradient descent, all sharing the program of
 Listing 1.12 and differing only in their assumptions on f , their convergence rate,
 and the resulting iteration bound. Ordered from the weakest to the strongest
 hypotheses, these are: (i) a general, possibly nonconvex, L-smooth objective, for
 which the method reaches an ε-stationary point in O L (f (x0 ) − f (x ∗ ))/ε2 steps;
 (ii) an L-smooth objective satisfying the Polyak-Łojasiewicz (PL) inequality with
 the constant step 1/L, which converges linearly; and (iii) a strongly convex
 quadratic f (x) = 21 x ⊤ Qx − b⊤ x minimised by exact line search, which converges
                                   2
 at the Kantorovich rate A−a  A+a     , where 0 < a ≤ A bound the eigenvalues of
 Q. As in the fixed-point method, each result is discharged for the imperative
 program by the vcg method, with the problem data (L, µ, the minimiser, and the
 eigenvalue bounds) supplied to the proof through an auxiliary program proven
 equal to gradient descent.
      The first regime assumes no convexity and only an L-Lipschitz gradient. The
 descent lemma then guarantees a fixed energy decrease per step while ∥∇f (x)∥ >
 ε, and telescoping this decrease bounds the number of iterations needed to reach
 an ε-stationary point.

1 theorem gradient_descent_general_convergence:
                             V
2   assumes
          V "0 < ε" "0 < L" " x.
                               V α x = 1 / L"
3    and " x. f x_min ≤ f x" " x. (f has_derivative (λh. grad x
      • h)) (at x)"       V
4    and grad_Lipschitz: " x y. ∥grad x - grad y∥ ≤ L*∥x - y∥"
5   shows "H[True] gradient_descent (grad , x0 , α, ε)
6     [∥grad x∥ ≤ ε ∧ iter ≤ nat ⌈2*L*(f x0 - f x_min)/ε2 ⌉]"
       Listing 1.13. Convergence to an ε-stationary point under L-smoothness alone

    The second regime keeps the constant step α(x)= 1/L and the L-Lipschitz gra-
    dient, and additionally assumes that f satisfies the Polyak-Łojasiewicz property:

                   1
                     ∥∇f (x)∥2 ≥ µ ·(f (x) − f (x ∗ )),   for all x.   (PL)
                   2

    Intuitively this indicates that “if f (x) is far from f (x ∗ ), then x is not at a flat
    plateau because the gradient squared ∥∇f (x)∥2 must be greater”. Moreover, if
    ∇f (x) = 0 then f (x) = f (x ∗ ). Under these conditions, starting from x0, the f
    converges linearly to f(x min) (i.e. f (x ∗ )):

1 theorem gradient_descent_linear_convergence:V
2   assumes
          V "0 < ε" "0 < L" "0 V
                               < µ" "µ < L" " x. α x = 1 / L"
3    and " x. f x_min ≤ f x" " x. (f has_derivative (λh. grad x
      • h)) (at x)"       V
4                             V ∥grad x - grad y∥ ≤ L*∥x - y∥"
     and grad_Lipschitz: " x y.
5    and Polyak_Lojasiewicz: " x. 2*µ*(f x - f x_min) ≤ grad x •
      grad x"
6   shows "H[True] gradient_descent (grad , x0 , α, ε)
7   [∥grad x∥≤ε ∧ iter ≤ nat ⌈ln ((2 *L*(f x0 - f x_min))/ε2 )/ln
      (1/(1 - µ/L))⌉]"
    Listing 1.14. Linear conv. bound for gradient descent under L-smoothness and PL

        Polyak proved the original statement of the above formalisation in 1963 [27],
    but our formalisation follows Theorem 1 of Karimi et al [18]. However, we em-
    phasise the bound on the number of iterations. Critical to this development in
    Isabelle, we showed that ∇f being L−Lipschitz implies a well-known inequality
    in optimisation theory, namely,

                                                            L
                       f (y) ≤ f (x) + ∇f (x) • (y − x) +     ∥y − x∥2 ,
                                                            2

    which in turn implies ∥∇f (x)∥2 ≤ 2L (f (x) − f (x ∗ )). To assist in this verification,
    we demonstrated 4 corollaries about the Lebesgue integral defined in the file
    Interval Integral.thy [2]. As customary, we present the invariants for proving
    the convergence of this method.

1 invariant f(x)-f(x_min) ≤ (f(x0)-f(x_min))*(1-(α x0)*µ)^iter
2   ∧ iter ≤ nat⌈ln ((2 *L*(f x0 - f x_min))/ε2 )/ln (1/(1 - α(x)*µ))⌉
3   ∧ (∥grad(x)∥ > ε −→
4   iter +1 ≤ nat⌈ln ((2 *L*(f x0 - f x_min))/ε2 )/ln (1/(1 -α(x)*µ))⌉)
5 variant nat⌈ln ((2 *L*(f x0 - f x_min))/ε2 )/ln (1/(1 -α(x)*µ))⌉-iter
    Listing 1.15. Loop invariant and variant for total correctness of gradient descent
    under L-smoothness and the PL inequality
      The invariant f(x)−f(xmin ) ≤ (f(x0 )−f(xmin ))·(1−( α x0 ) µ )iter is precisely
  the convergence rate of Theorem 1 by Karimi et al. [18] provided α(x0 ) = 1/L.
  The variant and the second invariant match the postcondition in the total
  correctness triple, similar to the third invariant that also emphasises that if
  ∥grad(x)∥ > ε then the current iterate cannot be equal to the upper bound.
  Again we use an auxiliary program to supply L and µ for the proofs.
      The third and strongest regime specialises f to a strongly convex quadratic,
  f (x) = 12 x ⊤ Qx − b⊤ x with Q symmetric positive-definite, and replaces the con-
                                              ∇f (x) • ∇f (x)
  stant step by exact line search, α(x) =                       . Writing 0 < a ≤ A
                                            ∇f (x) • (Q ∇f (x))
  for bounds on the eigenvalues of Q (obtained from an orthogonal diagonalisation
  Q = U ⊤ D U ), the classical Kantorovich inequality yields the geometric per-step
              2
  rate A−a
         A+a     , from which we again derive a closed-form iteration bound.

1 theorem gradient_descent_quadratic:
2    assumesV "0 < ε" "0 < a" "a < A"
3     and " V x. α x = (grad x • grad x) / (grad x • (Q *v grad x))"
4     and " V x. f x = (1/2) * (x • (Q *v x)) - b • x"
5     and " x. (f has_derivative (λh. grad x • h)) (at x)"
6     and "Q = transpose U ** D ** U" " orthogonal_matrix U" "
       diagonal_mat
            V            D"
7     and " i. a ≤ D $ i $ i ∧ D $ i $ i ≤ A" "D ** Dinv = mat 1"
       "grad x_star = 0"
8    shows "H[True] gradient_descent (grad , x0 , α, ε)
9    [∥grad x∥ ≤ ε ∧ iter ≤ nat ⌈ln (A*((x0 - x_star ) • (Q *v (x0 -
        x_star )))/ε2 )/ln ((A+a) 2 /(A-a) 2 )⌉]"
  Listing 1.16. Convergence at the Kantorovich rate for a strongly convex quadratic
  with exact line search

      Together, these three regimes already illustrate the spectrum of convergence
  criteria the method admits [18]; a fuller exploration is beyond the scope of this
  evaluation of the Isabelle/ITrees framework. We report proof effort for the linear
  regime as representative: proving linear convergence of gradient descent with
  vcg produces 12 goals, 9 of which can be discharged by Sledgehammer. The
  remaining 3 require using our optimisation inequality from Lipschitz continuity
  and specifying various algebraic manipulations. Besides this, the results from
  this section rely on several auxiliary facts from elementary real analysis and
                                            Rb
  integration. These include the evaluation a t, dt = (b2 −a 2 )/2, the monotonicity
                                                        Rb          Rb
  of the integral, namely that f ≤ g on [a, b] implies a f , dt ≤ a g, dt, a chain-
  rule lemma for composing a function with the line segment t 7→ x + t · d, and a
  specialised form of the Fundamental Theorem of Calculus on [0, 1].

  7   Evaluation
  Here, we track automation of proof obligations generated by vcg as a proxy
  for proof effort with the Isabelle/ITrees framework on the formalised numeri-
Table 1. Verification statistics for the current Isabelle sources. The VCG counts were
checked in Isabelle2025 against the built Numerical Methods session.
     Algorithm                         VCs             Auto.         LOC
     Bisection                           15          13 (87%)         195
     FPM (local/quad.)                  4/4      1 (25%)/2 (50%)     1111
     Perceptron                          11           8 (73%)         208
     Gradient descent (gen./PL/quad.) 8/12/8 6 (75%)/9 (75%)/4 (50%) 1085


cal methods (assuming the library dependencies are available). We record the
number of verification conditions, the percentage of those discharged by direct
automation, and the lines of code (LOC) needed for each method in Table 1.
The automation column counts VCs closed by a direct prover call, such as a
Sledgehammer-suggested by metis, by smt, or a one-line simplification. It does
not count obligations that need a structured Isar argument, even when that
argument contains automated intermediate steps. LOC counts non-comment,
non-blank Isabelle lines, excluding text, section, and subsection commands.
    The automation rates should be read together with the structure of the gen-
erated goals. Bisection is the most direct example: 13 of the 15 VCs close auto-
matically, and the remaining two are symmetric root-extraction obligations that
call the shared Bolzano helper. The perceptron is similar once the Novikoff in-
variants are supplied. Of its 11 VCs, 8 close directly; the remaining goals invoke
the shared margin, norm-growth, and mistake-bound lemmas. In both cases, the
difficult part is not low-level proof search but finding invariants and variants
that expose the textbook argument in a form the VCG can use.
    The FPM shows the other extreme. In the local contraction theorem, only one
of four VCs closes directly. The other obligations are the convergence argument:
geometric decay of the step size, the contradiction proof for the logarithmic iter-
ation bound, and the error decay towards the fixed point. The quadratic theorem
again generates four VCs, two of which are routine bound/variant obligations.
The others use the Taylor–Peano expansion and the local contraction reason-
ing. This explains why the FPM LOC count is high: the imperative program
is small, but the proof depends on substantial analysis infrastructure, including
the separate higher-order differentiability developments not in the table.
    Gradient descent lies between the two. The general smooth and PL-linear
theorems both have 75% direct automation: the guard-contradiction and exit-
condition VCs are routine, while the remaining obligations apply the descent
lemma, the PL contraction, or the iteration-bound lemmas. The quadratic exact-
line-search proof has lower direct automation because the proof explicitly applies
the Kantorovich contraction. Overall, vcg is effective at separating program rea-
soning from mathematical reasoning: it removes routine Hoare-logic bookkeep-
ing, but the analytic content still has to be packaged as reusable Isabelle lemmas.
    In general, proof effort tracks the mathematical content of the convergence
theorem more closely than the size of the imperative program. Across the seven
VCG invocations in Table 1, 43 of 62 obligations close directly, an aggregate
rate of 69%. The remaining goals correspond to recognisable textbook steps:
root extraction, Novikoff estimates, local-contraction bounds, descent lemmas,
and Kantorovich contraction. This supports the observation that Isabelle/ITrees
gives an accessible front end for numerical programs, while scalability depends
on reusable analysis and optimisation lemmas.


8   Related Work

The literature on verification of numerical methods is abundant. In PVS, for
instance, there has been work towards building libraries for reasoning about
real numbers since at least the mid-2000s [7,10,23,21]. However, those works
have focused on interval arithmetic and/or Taylor models as abstractions for
reasoning about polynomial and real arithmetic inequalities. In contrast, we
leverage the recent development of analysis libraries and directly reason about
Taylor polynomials, rather than models.
    The Rocq community has produced vast work. From the formalisation of
foundational theorems [30] to the verification of specific numerical methods us-
ing similar methods of interval arithmetic, Taylor models and linear algebra [26]
or complex combinations of Frama-C, automated provers and manual proofs [3].
These approaches have converged into an actively developed framework for veri-
fying numerical methods and producing reliable C programs [19,1]. Just like our
work, those projects leverage the libraries of a long-standing prover. For instance,
it relies on the Taylor Lagrange theorem from the Coquelicot library [4]. The
framework is exhaustive, with a complete pipeline that accounts for numeric sta-
bility and rounding errors, including sound examples on finding the solutions to
initial value problems of harmonic oscillators. In contrast, we have only focused
on adapting an imperative programming framework into a method for verifying
numerical methods. The execute command only performs arbitrary precision
operations. We consider the refinement of the Isabelle/ITrees framework to sup-
port numeric stability and rounding errors a worthwhile endeavour for future
work. Another, younger method in Rocq uses Taylor models and defines higher-
order differentiation for approximating solutions to initial value problems for
non-linear polynomial ordinary differential equations (ODEs) [25]. It arbitrarily
approximates the solution to the ODE by using more terms of its Taylor model.
    In Isabelle/HOL itself, there have been verifications for specific algorithms,
but not a framework per se. For instance, some Runge-Kutta methods over deep
embeddings of arithmetic expressions or set-based Euler methods have been ver-
ified [13,14]. We have generalised the higher-order differentiability of the Smooth
Manifolds AFP entry [17] with our derivative definitions and shown their rela-
tionships. Furthermore, as the name suggests, the focus there is on formalising
smooth manifolds instead of verifying numerical algorithms. The Isabelle/ITrees
framework also has much in common with Lammich’s Imperative HOL frame-
work [20]. However, we have endeavoured to avoid Isabelle idiosyncrasies in the
program notation and VCG methods. We believe that such a choice lowers the
barrier to using the Isabelle/ITrees framework, and means it can be applied
without extensive knowledge of Isabelle. More recently, the pioneering work from
Brucker and Stell [5] demonstrated the feasibility of verifying neural networks in
Isabelle/HOL. The results presented here are complementary in that our work
could pave the way for verifying the training algorithms, rather than the neural
networks themselves.
   Finally, in Lean, the rapid growth of the MathLib library [31] has caught up
with older provers like Rocq and Isabelle in terms of formalisation of higher-order
derivatives, Taylor series and continuously differentiable functions. So much so
that there is already work on constructing arbitrary stochastic computation
graphs, and a proof of correctness for an executable stochastic backpropagation
function [28]. Yet, as far as we know, a verification framework for numerical
algorithms is still nonexistent there.


9   Conclusion

We have evaluated Isabelle/ITrees, an imperative verification framework em-
bedded in Isabelle/HOL, as a method for proving total correctness of numerical
algorithms. The bisection method, fixed-point method, perceptron, and gradient
descent all admit readable imperative programs, Hoare-style specifications, and
loop annotations close to the textbook arguments. In each case, vcg reduces the
proof to mathematical verification conditions; after suitable invariants and vari-
ants are supplied, many of these obligations are discharged by Isabelle’s existing
automation.
    The case studies also make clear that the main cost is not programming
the algorithms, but supplying the surrounding analysis. Bisection and the per-
ceptron need little beyond their classical proof principles. Fixed-point iteration,
by contrast, required higher-order differentiability and Taylor’s theorem with
Peano remainder to obtain sharp local and quadratic convergence statements,
and gradient descent required reusable optimisation and integration lemmas. The
accompanying Isabelle theories now also contain floating-point variants and Re-
finement Framework counterparts, which strengthens the evidence that the ap-
proach is not limited to idealised real-arithmetic models. Overall, Isabelle/ITrees
provides a usable front end for verified numerical methods, while the scalability
of the approach depends on continuing to package the analytic, optimisation,
and floating-point facts that such methods routinely assume.

Funding statement: A Horizon MSCA 2022 Postdoctoral Fellowship (project
acronym DeepIsaHOL and number 101102608) supported the second author
during the development of this article. The third author is partly funded by
Horizon EU project RoboSAPIENS (grant agreement 101133807).

AI disclosure: The structure of descent lemma from Lipschitz gradient
was inspired from the output of ChatGPT 5.2 extended thinking. Claude Code
with Opus 4.8 was used to generate the programs and proofs for the Lammich
paradigm and floating point proofs. No other Isabelle code in the contributions
of this article has been produced with generative AI.
References

 1. Appel, A.W., Kellison, A.: VCFloat2: Floating-point error analysis in Coq. In:
    CPP 2024. pp. 14–29. ACM (2024)
 2. Avigad, J., Hölzl, J., Serafin, L.: Theory Interval Integral. In Isabelle/HOL (HOL-
    Analysis session), theory file HOL/Analysis/Interval Integral.thy
 3. Boldo, S., Clément, F., Filliâtre, J.C., Mayero, M., Melquiond, G., Weis, P.: Wave
    equation numerical resolution: a comprehensive mechanized proof of a C program.
    Journal of Automated Reasoning 50(4), 423–456 (2013)
 4. Boldo, S., Lelay, C., Melquiond, G.: Coquelicot: A user-friendly library of real
    analysis for Coq. Mathematics in Computer Science 9, 41–62 (2015)
 5. Brucker, A.D., Stell, A.: Verifying feedforward neural networks for classification
    in Isabelle/HOL. In: Formal Methods (FM 2023). LNCS, vol. 14000, pp. 427–444.
    Springer (2023)
 6. Bryant, D., Huerta y Munive, J.J., Kaliszyk, C., Urban, J.: Munkres’ general topol-
    ogy autoformalized in Isabelle/HOL (2026), https://arxiv.org/abs/2604.07455
 7. Daumas, M., Lester, D., Muñoz, C.: Verified real number calculations: A library for
    interval arithmetic. IEEE Transactions on Computers 58(2), 226–237 (February
    2009)
 8. Foster, S., Baxter, J., Cavalcanti, A., Woodcock, J., Zeyda, F.: Unifying semantic
    foundations for automated verification tools in Isabelle/UTP. Science of Computer
    Programming 197 (October 2020)
 9. Foster, S., Hur, C.K., Woodcock, J.: Unifying model execution and deductive ver-
    ification with Interaction Trees in Isabelle/HOL. ACM Trans. on Software Engi-
    neering Methodology (TOSEM) (2024)
10. Gottliebsen, H., Hardy, R., Lightfoot, O., Martin, U.: Applications of real number
    theorem proving in PVS. Formal Aspects Comput. 25(6), 993–1016 (2013)
11. Hölzl, J., Immler, F., Huffman, B.: Type classes and filters for mathematical anal-
    ysis in Isabelle/HOL. In: ITP. LNCS, vol. 7998, pp. 279–294. Springer (2013)
12. Huerta y Munive, J.J., Foster, S., Gleirscher, M., Struth, G., Pardillo Laursen,
    C., Hickman, T.: IsaVODEs: Interactive verification of cyber-physical systems at
    scale. Journal of Automated Reasoning 68(4), 21 (2024)
13. Immler, F.: Formally verified computation of enclosures of solutions of ordinary
    differential equations. In: NFM 2014. LNCS, vol. 8430, pp. 113–127. Springer (2014)
14. Immler, F.: A verified ODE solver and the Lorenz attractor. J. Autom. Reason.
    61(1-4), 73–111 (2018)
15. Immler, F., Hölzl, J.: Numerical analysis of ordinary differential equations in Is-
    abelle/HOL. In: ITP. LNCS, vol. 7406, pp. 377–392. Springer (2012)
16. Immler, F., Traut, C.: The flow of ODEs: Formalization of variational equation
    and Poincaré map. In: ITP 2016. LNCS, vol. 9807, pp. 184–199. Springer (2016)
17. Immler, F., Zhan, B.: Smooth manifolds and types to sets for linear algebra in
    Isabelle/HOL. In: CPP 2019. pp. 65–77. ACM (2019)
18. Karimi, H., Nutini, J., Schmidt, M.: Linear convergence of gradient and proximal-
    gradient methods under the Polyak-Łojasiewicz condition. In: Machine Learning
    and Knowledge Discovery in Databases (ECML PKDD 2016). LNCS, vol. 9851,
    pp. 795–811. Springer (2016)
19. Kellison, A.E., Appel, A.W.: Verified numerical methods for ordinary differen-
    tial equations. In: FoMLAS 2022, and NSV 2022. LNCS, vol. 13466, pp. 147–163.
    Springer (2022)
20. Lammich, P.: Refinement to imperative HOL. Journal of Automated Reasoning
    62(4), 481–503 (2019)
21. Muñoz, C., Lester, D.: Real number calculations and theorem proving. In: Hurd,
    J., Melham, T. (eds.) Theorem Proving in Higher Order Logics (TPHOLs 2005).
    LNCS, vol. 3603, pp. 195–210. Springer-Verlag (2005)
22. Murphy, C., Gray, P., Stewart, G.: Verified perceptron convergence theorem. In:
    MAPL 2017. pp. 43–50. Association for Computing Machinery (2017)
23. Narkawicz, A., Muñoz, C.: A formally verified generic branching algorithm for
    global optimization. In: Cohen, E., Rybalchenko, A. (eds.) Verified Software: The-
    ories, Tools, and Experiments (VSTTE 2013). LNCS, vol. 8164, pp. 326–343.
    Springer (May 2014)
24. Nocedal, J., Wright, S.: Numerical Optimization. Springer series in operations re-
    search and financial engineering, Springer, 2nd edn. (2006)
25. Park, S., Thies, H.: A Coq formalization of Taylor models and power series for
    solving ordinary differential equations. In: ITP 2024. LIPIcs, vol. 309, pp. 30:1–
    30:19. Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2024)
26. Pasca, I.: Formal Verification for Numerical Methods. (Vérification formelle pour
    les méthodes numériques). Ph.D. thesis, University of Nice Sophia Antipolis, France
    (2010)
27. Polyak, B.T.: Gradient methods for the minimisation of functionals. USSR Com-
    putational Mathematics and Mathematical Physics 3(4), 864–878 (1963)
28. Selsam, D., Liang, P., Dill, D.L.: Developing bug-free machine learning sys-
    tems with formal mathematics. In: International Conference on Machine Learning
    (ICML 2017). p. 3047–3056. JMLR.org (2017)
29. Solomon, J.: Numerical Algorithms: Methods for Computer Vision, Machine Learn-
    ing, and Graphics. A K Peters/CRC Press, 1st edn. (July 2015)
30. Tekriwal, M., Duraisamy, K., Jeannin, J.B.: A formal proof of the Lax equivalence
    theorem for finite difference schemes. In: NFM 2021. p. 322–339. Springer-Verlag
    (2021)
31. The Mathlib Community: The Lean mathematical library. In: CPP 2020. p.
    367–381. Association for Computing Machinery (2020)
