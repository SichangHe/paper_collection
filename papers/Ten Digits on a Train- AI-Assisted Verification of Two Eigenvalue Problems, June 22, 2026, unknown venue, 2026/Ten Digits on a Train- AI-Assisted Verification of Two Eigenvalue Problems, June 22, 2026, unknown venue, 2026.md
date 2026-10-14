                                                           TEN DIGITS ON A TRAIN:
                                           AI-ASSISTED VERIFICATION OF TWO EIGENVALUE PROBLEMS
                                                                               MATTHEW J. COLBROOK∗

                                                                                   June 22, 2026
                                                                  Dedicated to Marco Marletta on his 60th birthday.
                                               Abstract. Accurate numerical eigenvalues are often difficult to certify, especially in singular or
                                           non-normal settings. This article reports a human–AI collaboration on two such computations. For
                                           a singular self-adjoint Schrödinger operator, a verified zero count and Dirichlet–Neumann bracketing
arXiv:2606.23821v1 [math.NA] 22 Jun 2026




                                           certify the complete negative spectrum to ten decimal places. For a delicate non-normal atom–
                                           molecule benchmark, a previously unresolved resonance pair is separated, with each member enclosed
                                           to ten digits. The second result is achieved not by increasing the precision of one-way shooting, but by
                                           reformulating the problem as a global matching system for projective solution lines. The infinite tail is
                                           encoded as uncertainty in the terminal projective data, and a componentwise, tail-robust Krawczyk–
                                           Brouwer inclusion supplies the certificate. This gives a reusable architecture for analytic boundary-
                                           value systems with ill-conditioned propagation and uncertain asymptotic data. The collaboration
                                           also exposes the strengths and limits of AI assistance. AI rapidly produced accurate candidates
                                           and plausible proof strategies, but several failed, including one apparently complete tail argument
                                           that omitted the componentwise check required by a nonuniform polydisc. Validated computation
                                           is a stringent test of AI-assisted mathematics: the output is not merely a number, but a number
                                           with a proof. These examples show why the proof object matters, and why human mathematical
                                           judgment remained decisive. More broadly, as AI makes code, exposition, and plausible numerical
                                           claims inexpensive, standards for verification, attribution, peer review, and training must adapt. The
                                           implications are unsettling; the opportunity is extraordinary.

                                               Key words. validated computation, spectral theory, eigenvalue enclosure, singular Sturm–
                                           Liouville problems, resonance, Krawczyk method, interval arithmetic, artificial intelligence

                                               AMS subject classifications. 65L15, 65G20, 68T99, 34L15, 34L16, 81Q12


                                               1. Ten digits on a train. Over the past few months, something has changed.
                                           Almost everywhere I visit, people are talking about the mathematical ability of AI
                                           systems. Sometimes the discussion is explicit; more often it sits just offstage. Which
                                           problems have become easier? Which parts of our work are being automated? How
                                           much of a serious computational project can now be initiated by a few prompts?
                                           This has become an elephant in the room for computational mathematics, and for
                                           mathematics more broadly. We talk about it in corridors, in offices, and over coffee,
                                           but not yet, I think, with the directness that the subject deserves.
                                               The experiment reported here grew out of that atmosphere, but it began with a
                                           birthday-conference question. I asked Marco Marletta for a favorite eigenvalue, and
                                           then for a non-normal analog. The exchange was fun and fixed the mathematical
                                           starting point: a self-adjoint singular Coulomb problem and a resonance pair that he
                                           remembered as exceptionally difficult. Here are the four messages that set the scene.

                                               Matthew to Marco
                                              Hi Marco,
                                              I hope that all is well! Quick question - what is your favourite eigenvalue?
                                              Best, Matt



                                              ∗ Department of Applied Mathematics and Theoretical Physics, University of Cambridge, Cam-

                                           bridge, CB3 0WA. (mjc249@cam.ac.uk)
                                                                                              1
2                                     M. J. COLBROOK


    Marco to Matthew
    Hi Matt,
    It is probably the ground state of hydrogen, so the bottom of the spectrum of the 1D
    Schroedinger operator with potential V(r) = 2/rˆ2 - 1/r. I believe its value is -0.0625,
    or -1/16, and I seem to remember my first computed approximation was -0.0621, before
    we had implemented the algorithm for doing better boundary conditions and meshing.
    It was the first eigenvalue I ever computed numerically for a singular problem.
    Many years later I was in Oxford visiting Nick Trefethen around the time he had just
    published Chebfun. He wanted to show me how good it was and asked me for a problem
    to test it. I gave him this problem, Chebfun promptly fell over, and Nick complained
    that it was not fair! Goodness, I had a lot to learn about social skills.
    All the best, Marco

    Matthew to Marco
    That is a wonderful story! Do you also have a favourite non-normal version of this?

    Marco to Matthew
    I would choose one particular resonance pair from my 2014 many-author paper
    https://orca.cardiff.ac.uk/id/eprint/64130/8/OA-20142015-45.pdf
    It’s the one at the bottom of page 15. It was an utter beast to compute. Never mind
    a 100 digit challenge, just getting 4 digits would have been nice!

    The first message leads to the ℓ = 1 sector of the radial Coulomb operator, with
potential
                           VC (r) = 2/r2 − 1/r,      r > 0,
whose ground state is −1/16 = −0.0625. Marco’s recollection of an early numerical
approximation near −0.0621, and of a later Chebfun [11] anecdote, made it a good
control problem. The second message points to the resonance pair at the bottom of
page 15 of Bögli, Brown, Marletta, Tretter, and Wagenhofer [6], originally associated
with Abramov, Aslanyan, and Davies [1]. Resonances encode oscillation and decay
rates for open systems in quantum, wave, and scattering problems [29, 12].
     I was on the train from Cambridge to Leeds when I decided to turn the above
exchange into a test. Could an AI assistant be driven, by repeated mathematical
questioning, to rigorous proof objects certifying ten digits of these eigenvalues? By
the end of the journey, I had a provisional answer. By the end of the day, I had
what appeared to be a complete certificate. The AI system used in the computational
exchanges was ChatGPT 5.5 (with Codex), with the intelligence setting “Extra High”,
in May 2026. I allowed it to search, write code, propose methods, make mistakes, and
try to diagnose them. I did not allow a final claim to rest on the chat. Validated
computation is a useful stress test for this reason. It asks the assistant not merely for
a value, a program, or an explanation, but for a mathematically checkable object.
     This paper reports that case study: not as a benchmark of an AI system in
isolation, but as an account of a human–AI mathematical exchange in which numerical
suggestions were repeatedly pushed toward independently checkable certificates. The
examples should be read in that spirit. I analyze only the methods used by the large
language model and the mathematical work needed to interpret, repair, or replace
them. I do not claim that these are the best-conditioned, most economical, or most
elegant validation strategies one could design from a blank page.
     The paper sits at the intersection of two literatures. The first is the established
                                    TEN DIGITS ON A TRAIN                                          3

         AI-assisted exploration

                                response            candidate                 author
             prompt           code/method           or failure              assessment
                                       new prompt

                                    if checkable
                                                            mathematical certification

                        finite              theorem or           mathematical
                      certificate         validation test           claim

     Fig. 1.1. The workflow used in the two examples. The assistant operates in an exploration
loop, where prompts lead to proposed methods, code, numerical candidates, and useful failures. A
computed spectral claim enters the paper only after passing through a separate certification layer.

tradition of validated computation: interval analysis, a posteriori estimates, Taylor
models, and fixed-point tests have long turned numerical work into mathematical
proof [18, 22, 28, 15]. The second literature is new and moving quickly: AI-assisted
mathematics, including program-search discovery, human–AI proof search, and proof-
assistant workflows whose statements and outputs must themselves be audited [21,
10, 14]. The aim here is to examine their intersection in concrete validated spectral
computations, with broader consequences for numerical mathematics.
     The sharpest mathematical contribution is the resonance certificate. The calcu-
lation moves from the earlier two-decimal enclosure, which did not separate the two
parity resonances, to two 17-digit certified enclosures. The key step is not extra pre-
cision. It is a change of proof object. Rather than validate a long non-normal shoot
or a scalar determinant obtained from one-way propagation, the method projectivizes
the solution line at each mesh point, treats all node coordinates as simultaneous un-
knowns, and verifies the resulting sparse global matching system by a Krawczyk inclu-
sion.1 The tail estimate is then inserted as a set-valued final-row perturbation, and
a robust Krawczyk–Brouwer inclusion gives the corresponding half-line resonance.2
This gives a reusable validation framework for analytic boundary-value systems with
ill-conditioned propagation and uncertain terminal data.
     Throughout, I show a working style for interacting with an AI assistant summa-
rized in Figure 1.1. The assistant operates in the exploration loop, where prompts pro-
duce methods, code, candidates, and failures. The mathematical claims pass through
a separate certification layer. In the resonance problem, this separation was essential:
failed approaches led to the global projective formulation, and a draft certificate that
looked finished failed an audit because it controlled global maxima where the proof
required nodewise inclusion in a polydisc. AI can and does make mistakes. The lesson
is not to dismiss AI-assisted work, but to make every claim checkable.
     The prompt and response3 boxes below record this exchange. The explanations
in the paper reconstruct and correct the intervening work from the assistant’s files—
scripts, notes, output tables, and certificates—and assess which mathematical claims
they support. I have checked all of the code for the certificates line by line.
   1 The Krawczyk method [16, 19] combines a Newton-like correction with Jacobian interval bounds.
   2 This should be distinguished from the validation in [6], where interval arithmetic and the argu-

ment principle are applied to a finite-interval determinant.
   3 I also record the response time to roughly indicate the relative difficulty of each stage. These

timings are machine-, server load-, and internet-speed-dependent (UK train Wi-Fi is notoriously bad)
and are longer than the run times of the final interval-arithmetic certificate codes.
4                                         M. J. COLBROOK

                                              Table 1.1
     Numerical certificates verified to ten digits. The displayed values are rounded to ten decimal
places. The resonance validation below has an error radius less than 7 × 10−19 . The self-adjoint
operator considered is a modification of the exactly solvable Coulomb operator.

certified object                                  displayed value            verification method
modified self-adjoint ground state                −0.0531967615              Temple certificate

modified self-adjoint negative spectrum       11 intervals in Table 3.1      Sturm verifier

odd/Dirichlet resonance                    0.9180018174 − 17.0006882497 i    projective Krawczyk

even/Neumann resonance                     0.9178768454 − 17.0006448370 i    projective Krawczyk



     Table 1.1 summarizes the numerical outcomes. The article is also intended as a
guided exposition of validated numerics: the certificates are introduced through the
questions they answer, rather than as a catalog of interval algorithms. The three
certificates become progressively more complicated: a variational Temple certificate
for the ground state, a global Sturm and bracketing certificate for the full negative
spectrum, and a non-variational projective Krawczyk certificate for the resonance
pair. I learned some interesting mathematics during the exchange, which I hope the
reader will enjoy as well.
     Where does this leave us? Wider implications are discussed in Sections 5 and 6,
but the numerical analysis community should not treat this as a curiosity at the edge
of the field. The point is not to argue against AI: the opportunities are extraordinary,
and the exchange below let me explore methods, failures, and reformulations at a
speed that would have been hard to imagine only recently. Precisely because the
opportunity is real, the standards matter. AI changes the cost of trying ideas, the
apparent difficulty of examples, and the ease with which plausible numerical claims
can be produced. If our standards for validation, credit, and research training do not
adapt, polished but weakly checked claims may travel faster than understanding.
     The structure of the paper is as follows. Sections 2 and 3 treat the self-adjoint
problems: first, a control example, and then a harder certificate problem. Section 4
gives the non-normal resonance problem, the failed validation routes, and the global
projective Krawczyk certificate. Section 5 discusses lessons from the certificates, in-
cluding the social consequences of AI-assisted computational mathematics. We con-
clude in Section 6.

    2. A control problem: Marletta’s Coulomb eigenvalue. The first problem
Marletta gave was the reduced radial problem on (0, ∞):
                             
              ′′       2    1
(2.1)      −u (r) +       −     u(r) = λu(r),    u(r) = O(r2 ) (r ↓ 0).
                       r2   r
This is the ℓ = 1 Coulomb problem. The Coulomb spectrum of hydrogen was one
of the proving grounds of quantum mechanics. Balmer’s empirical formula and Ryd-
berg’s generalization organized the observed lines into integer-labeled series [4, 23];
Bohr’s model explained the same pattern by quantized orbits [7]; and Schrödinger
recast hydrogen as an eigenvalue problem and recovered the spectrum from a wave
equation [24]. After separation of variables, the angular momentum ℓ = 1 case has
centrifugal term ℓ(ℓ + 1)/r2 = 2/r2 , giving exactly (2.1) in the present units.
     The essential spectrum of this operator is [0, ∞) [27, Thm. 10.9]. To find the
negative eigenvalues, let λ = −κ2 , with κ > 0, and set x = 2κr. If u(r) = r2 e−κr y(x),
                                   TEN DIGITS ON A TRAIN                                        5

then the differential equation becomes
                                                           
                              ′′            ′          1
                           xy + (4 − x)y +               − 2 y = 0.
                                                      2κ
This is Kummer’s equation [20, Sec. 13.2(i)]. The solution regular at r = 0 is square
integrable at infinity only when the hypergeometric series terminates, that is when
                             1
                               − 2 = m,           m = 0, 1, 2, . . . .
                            2κ
                                                        (3)
Then y is a generalized Laguerre polynomial Lm (x). Setting n = m + 1 ∈ N gives
infinitely many negative eigenvalues accumulating at the bottom of the essential spec-
trum:
                                         1
                     λn = −κ2 = −              ,   n = 1, 2, . . . .
                                     4(n + 1)2
Since x = 2κr = r/(n + 1), the corresponding eigenfunctions are, up to normalization,

                                          (3)
(2.2)         un (r) = r2 e−r/(2(n+1)) Ln−1 (r/(n + 1)),             n = 1, 2, . . . .
Thus the smallest eigenvalue is −1/16, with eigenfunction proportional to r2 e−r/4 .
    A short, earlier AI exchange, not reproduced here, recovered this answer quickly,
but not by merely printing a remembered formula. I asked for a certified numerical
computation. For a positive
                       ′′     2
                                 chosen trial function v, the assistant found that the
pointwise quotient −v +(2/r v
                                −1/r)v
                                       was identically −1/16. When I next asked for
enclosures of the ten lowest eigenvalues, the attempted numerical validation exposed
the terminating Laguerre structure. This relegated the Coulomb problem to a useful
control case. Once the right ansatz is found, the proof reduces to polynomial identities.
The more revealing test was to modify the problem in a new conversation that did
not contain this derivation.
    3. A modified self-adjoint problem.
    3.1. The lowest eigenvalue. To remove the exact Laguerre structure while
keeping the same singular half-line setting, I sent the following prompt.

                                       Prompt 1: modifying Marletta’s eigenvalue

               Below, I will paste an email exchange with Marco Marletta. He describes
           his favourite eigenvalue. Let’s change the potential to r22 − r(1+r/200)
                                                                              1
                                                                                   2 . I want

           you to investigate whether this has a negative eigenvalue. If so, I want you
           to come up with a way to compute its smallest eigenvalue. You will need to
           rigorously prove error bounds on the eigenvalue and fully describe your com-
           putational procedure. You will find Python installed in the current directory.
           You can probably build a rational computation verification in Python, or you
           may need to look at interval arithmetic implementations.

    For self-adjoint operators, and here in particular, a good approximate eigenvector
can often be turned into a rigorous eigenvalue bound by combining residual estimates,
comparison theorems, and variational principles (see Theorem 3.1 below).
    The modified operator in this prompt is
                          d2                              2          1
                 H=−          + V (r),          V (r) =      −
                          dr2                             r2   r(1 + r/200)2
6                                       M. J. COLBROOK


on L2 (0, ∞). The modification preserves the singular radial character of Marletta’s
problem, but it removes the exact Laguerre solution. Near 0, the dominant equation
remains −u′′ + r22 u = 0, whose power-law solutions are r2 and r−1 . The admissible
branch therefore satisfies u(r) = O(r2 ), while the r−1 branch is excluded. As for
the Coulomb operator, the essential spectrum of H is [0, ∞) [27, Thm. 10.9]. If a
trial function has Rayleigh quotient below 0, then the min–max principle implies the
existence of a discrete negative eigenvalue.
    AI response, worked for 10m 54s

       Yes. The modified potential still has a negative ground-state eigenvalue.
    I produced a rigorous certificate in EIGENVALUE.md and the verifier script
    verify_temple.py. Certified enclosure:
           −0.05319676154302054294 ≤ λ1 ≤ −0.05319676154233948813.
    The proof uses a five-term hydrogenic Ritz vector, computes its Rayleigh
    quotient and residual with rational interval arithmetic, then applies Temple’s
    inequality. The spectral gap needed for Temple comes from comparing the
    new potential with Marco’s Coulomb potential, whose second l = 1 level is
    −1/36. I also ran the verifier successfully with the local Python.


    At this stage these were claims made by the assistant, not yet certified results. I
have audited the proposed argument and verifier, and this is the same pattern used
throughout. Here, the assistant first used a finite-difference discretization and then
formed a five-dimensional Ritz approximation that found a candidate near −0.0532.
It then proposed a certificate: round the Ritz vector to rational data, compute a
Rayleigh quotient and residual bound, use the Coulomb operator as a comparison,
and apply Temple’s inequality with an explicit gap.
    The certificate is small enough to describe explicitly. It uses the trial vector
                                               4
                                               X
(3.1)                     u(r) = r2 e−r/4 +          cj r2 e−r/4 (r/10)j .
                                               j=1

The transcript does not establish why this form was selected. Mathematically, it is a
natural polynomial–exponential enrichment of the first Coulomb eigenfunction u1 in
(2.2). The rational coefficients were obtained by rounding an exploratory Ritz vector:
                 911357530019777039                      3464720637087477951
     c1   =                              ,     c2 =                              ,
              50000000000000000000000                   500000000000000000000
                  653458902923720157                      1159101098623161979
    c3 = −                                ,    c4 =                                 .
                2500000000000000000000                  50000000000000000000000
The displayed rational coefficients define the trial function exactly; they need not
enclose the floating-point Ritz coefficients. The exploratory calculation is used only
to select a good trial function. The floating-point Ritz calculation has no further role.
     For the normalized vector v = u/∥u∥, the verifier computes enclosures for the
Rayleigh quotient ρ = ⟨Hv, v⟩ and squared residual δ 2 = ∥(H − ρ)v∥2 . The functions
in the expansion (3.1) are products of powers of r and e−r/4 . After integration by
parts and the substitution t = r + 200, the only non-elementary quantity needed is
the single scalar

                                                     Z ∞
                                  100                        e−s
                            C=e         E1 (100) =                 ds.
                                                      0    100 + s
                                  TEN DIGITS ON A TRAIN                                7

For example, the inner products involve
        Z ∞ −r/2 3                  Z ∞                                  
               e     r          100        −t/2            120000 8000000
    K=                   dr = e          e       t − 600 +       −          dt.
         0    (r + 200)2             200                      t      t2
The nonnegative powers of t are evaluated by repeated integration by parts, while
                 Z ∞ −t/2                    Z ∞ −t/2
                      e                           e          1     C
            e100           dt = C,      e100         2
                                                       dt =     − .
                  200   t                     200   t       200    2
Thus, K = −40796+4120000 C. Similarly, the verifier represents each required integral
as a + bC, with a, b ∈ Q. The scalar C is enclosed by the finite identity
                                     N −1
                                X (−1)k sk
                         1                     (−1)N sN
                              =            +                .
                      100 + s      100k+1    100N (100 + s)
                                     k=0
                         −s
After multiplying by e        and integrating, this gives
                    N −1
                    X      (−1)k k!                                 N!
               C=                   + RN ,       0 ≤ (−1)N RN ≤           .
                           100k+1                                 100N +1
                    k=0

This is a rigorously bounded asymptotic expansion: the terms initially decrease, but
factorial growth eventually dominates as N → ∞. Nevertheless, with N = 60, the
verifier obtains an interval of width less than 8.33 × 10−41 , which proves that
               C = 0.009901942286733018406405931819804200422 . . . .
For example, K = −40796 + 4120000 C = 0.0022213 . . . with large cancellation, which
illustrates why exact rational endpoints are preferable here.
     The reduction to one constant is a useful example of certificate design. It is
more transparent, smaller, and easier to check than asking an interval quadrature
routine to integrate each required integral independently. The variational structure
then provides a global enclosure.
    Certificate 3.1 (Ground-state enclosure). For the modified Coulomb operator
H, the lowest eigenvalue λ1 satisfies
           −0.05319676154302054294 ≤ λ1 ≤ −0.05319676154233948813.
    Proof. The verifier rigorously gives δ 2 ≤ 1.7311721 × 10−14 and
          ρ ∈ [−0.0531967615423394881331, −0.0531967615423394881330].
Given a self-adjoint operator L that is bounded below, let λ1 (L) ≤ λ2 (L) ≤ · · · denote
its discrete eigenvalues below the essential spectrum. If there are a finite number N
of these, set λN +j (L) to be the bottom of the essential spectrum for j ∈ N. These
are the min–max levels of L. Since −1/(r(1 + r/200)2 ) ≥ −1/r, comparison with the
ℓ = 1 Coulomb operator HC in Section 2 implies that λ2 (H) ≥ λ2 (HC ) = −1/36.
Rayleigh–Ritz gives λ1 (H) ≤ ρ < −1/36. Therefore H has exactly one eigenvalue
below −1/36 and Temple’s inequality [26, Thm. 1] gives
                                        δ2
                                ρ−             ≤ λ1 (H) ≤ ρ.
                                     −1/36 − ρ
Substituting the outward-rounded intervals gives the displayed enclosure.
    In the above proof, the condition ρ < λ2 (HC ) ≤ λ2 (H) lets a single trial vector
certify the bottom eigenvalue, rather than merely locating a nearby spectral point.
8                                      M. J. COLBROOK


    3.2. Finite or infinite negative spectrum? At this stage, I was very excited
that this could all be achieved at the push of a button. (It took me significantly
longer to write the above explanation of the certificate and to check it.) In the usual
mathematical way, I immediately wanted more.

                                     Prompt 2: finite or infinite negative spectrum

                 Wonderful! Are there infinitely many negative eigenvalues or finitely
             many? If there are finitely many, say N , compute the first min(10, N ) negative
             eigenvalues to 10 digits. If there are infinitely many, compute the smallest 10
             to 10 digits. Again, everything has to be rigorously justified.


    AI response, worked for 21m 56s

        It is finite: there are exactly 11 negative eigenvalues. I wrote the justifi-
    cation in SPECTRUM.md, with the shooting generator spectrum_shooting.py.
    The first ten, ordered from most negative upward, are: −0.0531967615,
    −0.0193674097,         −0.0082420874,      −0.0036685443,       −0.0016120468,
    −0.0006697369, −0.0002515677, −0.0000804935, −0.0000198995, and
    −0.0000031084. √The proof structure is: the potential is nonnegative for
    r ≥ 9800 + 4000 6, so there can only be finitely many negative eigenvalues;
    the zero-energy regular solution has exactly 11 zeros, giving N = 11 by Sturm
    oscillation; Dirichlet–Neumann bracketing then encloses the first ten half-line
    eigenvalues in intervals of radius 5 × 10−12 .

                                                                                     √
     The assistant’s first observation was that V (r) ≥ 0 for r ≥ r+ = 9800 + 4000 6.
In fact, since limr→∞ r2 V (r) = 2 > −1/4, there is a Kneser-type half-line criterion [5,
Cor. 3.6(ii)] that rules out an infinite sequence of negative eigenvalues accumulating at
0. Hence, there are only finitely many negative eigenvalues. The second observation
involves u0 , the regular solution of the zero-energy equation
                                             
                          2           1
(3.2)       −u′′0 (r) +      −                  u0 (r) = 0,     u0 (r) ∼ r2 (r ↓ 0).
                          r2   r(1 + r/200)2
Sturm oscillation identifies the number of negative eigenvalues of H with the number
of zeros of u0 , provided that zero is not itself an eigenvalue [13, Thm. 2.1, Cor. 2.4,
and the discussion following Thm. 7.4].
     However, I should highlight a warning. The initial response overclaimed since the
produced code spectrum_shooting.py used floating-point arithmetic. In preparing
this paper, I separated the exploratory computation from the proof step. The certified
claims below use the later Arb [15] verifier selfadjoint_interval_verify.py, which
checks the zero crossings, the tail signs, and the Dirichlet–Neumann endpoint signs
by interval arithmetic. It proves one zero in each of the following intervals:
         1   :   [10.681579, 10.683579],     2         :     [26.241254, 26.243254],
         3   :   [49.959273, 49.961273],     4         :     [85.068026, 85.070026],
         5   :   [137.168771, 137.170771],   6         :    [216.494771, 216.496771],
         7   :   [343.195032, 343.197032],   8         :    [561.492538, 561.494538],
         9   :   [985.487724, 985.489724],   10        :   [1999.515565, 1999.517565],
        11   :   [5906.061779, 5906.063779].
This is a validated shooting calculation. The verifier starts at ε = 10−2 from a regular
                                 TEN DIGITS ON A TRAIN                                        9

Frobenius expansion with an explicit bound on the omitted tail, and a coefficient
bound shows that there is no zero on (0, ε). The verifier then propagates the interval
enclosure for (u0 , u′0 ) by Taylor steps for u′′0 = V u0 , bounding each remainder by a
Cauchy–Picard majorant. A detailed description is delayed until Subsection 3.4.
    The verifier first proves a sign change across each of the 11 displayed intervals.
Independently, it covers [ε, T ] by certified Taylor steps. On each step, either the
range enclosure of u0 excludes zero, or the endpoint signs are opposite and the range
enclosure of u′0 excludes zero. The scan therefore finds exactly 11 zeros and no others.
Since the displayed boxes are disjoint and each contains a zero, each contains exactly
one zero. It is verified that u0 (T ) < 0 and u′0 (T ) < 0. Since V (r) ≥ 0 for r ≥ T
and u′′0 = V u0 ≤ 0 for u0 < 0, this sign information rules out further zeros on
[T, ∞). Figure 3.1 (right) illustrates this behavior. This also proves that zero is not
an eigenvalue: limr→∞ u0 (r) = −∞ so u0 cannot be square integrable.

     3.3. Analytic form and zero counting missed by the AI. The zero-energy
solution u0 has a closed form and analytic argument for its 11 zeros, which the assist-
ant did not notice. This does not invalidate the interval certificate above; rather, it
is a useful reminder that, just like a human, an AI-assisted route can find a checkable
proof without finding the simplest analytic
                                          √ description that often helps a proof.
     Set r = 200 tan2 (θ/2) and u0 (r) = r y(θ) for 0 < θ < π. A direct calculation
transforms the zero-energy equation into
                        1 d                        9
(3.3)                 −        (sin θ y ′ (θ)) +        y(θ) = 200 y(θ).
                      sin θ dθ                   sin2 θ
This is the associated Legendre equation of order 3 and degree
                              √
                        ν = ( 801 − 1)/2,           ν(ν + 1) = 200
[20, Secs. 14.2–14.3]. The solution with the required behavior u0 (r) ∼ r2 as r ↓ 0 is
                                           √
                                                           
                                                    200 − r
                        u0 (r) = 6 × 2003/2 r P−3
                                               ν              ,
                                                    200 + r
where P−3ν denotes the Ferrers function on (−1, 1).
     This transformation also gives an analytic zero count. The Sturm–Liouville op-
erator on the left-hand side of (3.3) has eigenvalues n(n + 1), n = 3, 4, 5, . . .. Since
13 × 14 = 182 < 200 < 210 = 14 × 15, Sturm oscillation shows that the solution
regular at θ = 0 has exactly 11 zeros in (0, π). Because r = 200 tan2 (θ/2) maps (0, π)
bijectively onto (0, ∞), the zero-energy solution u0 has exactly 11 positive zeros.
     Figure 3.1 shows this solution and its derivative. The left panel plots u0 , with a
magnified panel near the eleventh zero. The right panel plots u′0 and marks the onset
of the nonnegative tail. For√r > 0, since u′′0 = V u0 , the zeros of u0 , together with
the zeros r± = 9800 ± 4000 6 of the potential, are the critical points of u′0 . At the
certified point T > r+ , the verified signs of u0 and u′0 give the non-oscillatory tail
used above.

    3.4. Enclosures for all negative eigenvalues. Before giving the final argu-
ment for the eigenvalue enclosures, I will record my final prompt for this problem—
there was only one sensible thing left to do.4


   4 The reader may find the tone of some prompts amusing. I often find (and am often told) that

AI assistants work better when encouraged.
10                                                                M. J. COLBROOK

                                                                                  2
         100
                                                                                  1
           0
u0 (r)




                                                                        u00 (r)
                          #10-4    11th zero                                      0
                     1
         -100
                     0
                                                                                  -1                      monotone tail
                     -1                                                                            u00 and u0 decreasing
         -200
                     5906.061              5906.063
                                                                                  -2
                 0                     1
            10                    10                  102   103       104          100    101      102        103          104   105
                                                      r                                                  r
     Fig. 3.1. The regular solution of (3.2). Left: u0 , with the verified interval for the eleventh zero
shaded in the inset. Right: u′0 , with the beginning of the monotone tail indicated. The zeros of u0
are shown as red dots in the left panel and crosses in the right panel.


                                                                             Prompt 3: the eleventh eigenvalue

                             Wow! Great job. Since there are 11, we may as well compute the 11th as
                          well. Please can you do this. Rigorously argue why your computations are
                          correct, explicitly describe the method and any computations you have done.


         AI response, worked for 5m 29s

            Done. The eleventh eigenvalue is certified in the interval
                             [−1.6240198497433 × 10−7 , −1.6239198497433 × 10−7 ].
         I updated the spectrum note with all eleven eigenvalues in SPECTRUM.md. This
         includes the finiteness argument, Sturm oscillation count, Dirichlet/Neumann
         bracketing, Frobenius initialization, and interval-shooting certification.


     As in the preceding response, this was an overclaim at the time: spectrum_
shooting.py supplied a plausible candidate interval, but the certification was estab-
lished only by the later Arb verifier selfadjoint_interval_verify.py.
     The task is to enclose eigenvalues of H between the finite-interval Neumann and
Dirichlet eigenvalues [27, Sec. 2.3 and Sec. 4.4]. Let HLD and HLN be the finite-interval
realizations on (0, L), with the same u(r) = O(r2 ) condition at 0 and with Dirichlet
and Neumann conditions respectively at L.5 Let HL,∞      D           N
                                                              and HL,∞   denote the tail
realizations on (L, ∞). The corresponding quadratic-form domains satisfy Q(HLD ⊕
   D
HL,∞  ) ⊂ Q(H) ⊂ Q(HLN ⊕ HL,∞    N
                                    ), and the forms agree on their common domains.
Consequently, HL ⊕ HL,∞ ≤ H ≤ HLD ⊕ HL,∞
                  N     N                     D
                                                   in the form sense. Since V (r) ≥ 0 for
r ≥ L, both tail operators are nonnegative. The min–max principle therefore gives
(3.4)                                         λj (HLN ) ≤ λj (H) ≤ λj (HLD ),            j = 1, . . . , 11.
          The verifier uses a Frobenius expansion to construct rigorous initial balls for


    5 The floating-point locator spectrum_shooting.py used the larger truncation point 25000 to find

candidate intervals. The rigorous interval-arithmetic script selfadjoint_interval_verify.py
                                                                                         √     then
verifies the required endpoint signs at L = T = 19597.9589711328 > r+ = 9800 + 4000 6, which
already lies in the nonnegative tail of the potential.
                                   TEN DIGITS ON A TRAIN                                             11

u(ε, λ) and u′ (ε, λ), where ε = 10−2 . Near r = 0,
                                       ∞
                            1         X   (−1)m (m + 1) m−1
                                    =                  r    .
                      r(1 + r/200)2   m=0
                                              200m
                     P∞
Writing u(r, λ) = r2 n=0 an (λ)rn with a0 = 1 and comparing the coefficient of rn
in the eigenvalue equation gives
                                 X (−1)m (m + 1)
                n(n + 3)an +                       aj + λan−2 = 0,
                              m+j=n−1
                                          200m

with the convention that ak = 0 for k < 0. For every spectral endpoint used below,
|λ| < 0.054. The verifier initializes the regular solution at ε = 10−2 by retaining the
coefficients a0 (λ), . . . , a80 (λ). The recurrence above implies, by induction, that
                                n−1
                |λ|       1     X m+1       40000/39601 + 0.06
 |an (λ)| ≤           +                 m
                                          ≤                    < 1,                             n ≥ 1.
              n(n + 3) n(n + 3) m=0 200             4
Consequently, the omitted tails beginning with a81 satisfy
            80                                          80
            X                     ε83                   X                             83ε82 − 82ε83
 u(ε, λ)−         an (λ)εn+2 ≤        ,   u′ (ε, λ)−          (n + 2)an (λ)εn+1 ≤                   .
            n=0
                                 1−ε                    n=0
                                                                                        (1 − ε)2
The verifier evaluates the two finite sums in Arb ball arithmetic, adds these symmetric
tail bounds, and uses the resulting balls as the initial data at r = ε.
     The verifier then propagates the solution by validated local Taylor expansions.
At a point x, let
                                            ∞
                                            X                                   ∞
                                                                                X
            q(x + t, λ) = V (x + t) − λ =         qk tk ,       u(x + t, λ) =         bn tn .
                                            k=0                                 n=0
                   ′′
The equation u = qu gives the recurrence
                                                   n
                                     1        X
                        bn+2 =                  qk bn−k ,              n ≥ 0.
                               (n + 1)(n + 2)
                                                  k=0

To bound the omitted Taylor tail over the interval 0 ≤ t ≤ h, choose ρ > h such that
the disk |z − x| ≤ ρ avoids the singularity at 0, and set
                                2                40000
                        Q=           2
                                       +                       + |λ|.
                             (x − ρ)     (x − ρ)(x + 200 − ρ)2
If Qρ2 /2 < 1, the integral equation and a Picard majorant give
                                                             U + ρU1
                                 sup |u(z)| ≤ M :=                     ,
                             |z−x|≤ρ                        1 − Qρ2 /2
where U and U1 are rigorous upper bounds for |u(x)| and |u′ (x)|. Cauchy’s estimate
then yields, with τ = h/ρ,
            ∞                         ∞                                  
           X
                    n      τ d+1     X
                                               n−1     M τ d d + 1 − dτ
                bn h ≤ M         ,        nbn h      ≤                     .
                           1−τ                         ρ       (1 − τ )2
         n=d+1                              n=d+1

The verifier therefore obtains rigorous enclosures of the endpoint values and of the
ranges of u and u′ throughout every step.
12                                                                              M. J. COLBROOK

                        Finite-interval PrB
                                          ufer count                                                                            Finite-interval PrB
                                                                                                                                                  ufer radius
            12
                     3(T; 6)=:
                     certi-ed eigenvalue intervals                                                                      8
            10       Dirichlet levels
                     Neumann levels




                                                                                                   10−3 log10 R(T, λ)
             8                                                                                                          6
3(T; 6)=:




                                                               eleventh certi-ed interval
             6                                       11
                                                                                                                        4
                                                    10.9
                                                    10.8
             4                                3=:
                                                    10.7
                                                    10.6                                                                2
             2                                      10.5
                                                      6.7894          6.78942        6.78944
                                                                     ! log10 (!6)

             0                                                                                                          0
                 0          2                   4                         6                    8                            0      2         4          6       8
                                      ! log10 (!6)                                                                                      ! log10 (!6)
     Fig. 3.2.      Floating-point illustration of the finite-interval Prüfer calculation at T =
19597.9589711328. Left: θ(T, λ)/π as a function of − log10 (−λ). Integer levels correspond to Dirich-
let conditions u(T, λ) = 0, and half-integer levels correspond to Neumann conditions u′ (T, λ) = 0.
The blue bands are the certified common bracketing intervals mj ± 5 × 10−12 ; their endpoints are not
the crossing locations. The inset magnifies the eleventh interval and marks the approximate Dirich-
let and Neumann crossings obtained from the floating-point Prüfer data. Right: 10−3 log10 R(T, λ),
where R2 = u(T, λ)2 + u′ (T, λ)2 . Its broad growth is expected: for λ = −κ2 < 0, the tail equation
is approximately u′′ = κ2 u, so a generic terminal solution grows like eκT . The figure is illustrative
only; the certificate uses interval endpoint signs and Sturm oscillation.



     The finite-interval Dirichlet and Neumann eigenvalues are the zeros of u(L, λ) and
u′ (L, λ), respectively. To count them, define the Prüfer radius and angle by
                          u(r, λ) = R(r, λ) sin θ(r, λ),                                                       u′ (r, λ) = R(r, λ) cos θ(r, λ),
with θ(r, λ) → 0 as r ↓ 0. A Wronskian calculation gives
                                        RL
                         ∂θ              0
                                           u(r, λ)2 dr
                            (L, λ) =                       > 0.
                         ∂λ          u(L, λ)2 + u′ (L, λ)2
Moreover, θ(L, λ) → 0 as λ → −∞. Since u0 (T ) < 0 and u′0 (T ) < 0 for L = T =
19597.9589711328, and u0 has 11 positive zeros,
                                                                        11π < θ(T, 0) < 23π/2.
Hence, the conditions θ(T, λ) ∈ πZ give exactly 11 negative Dirichlet eigenvalues, and
the conditions θ(T, λ) ∈ π/2 + πZ give exactly 11 negative Neumann eigenvalues. Fig-
ure 3.2 illustrates the Sturm count: θ(r, λ) records the endpoint boundary conditions,
while R(r, λ) records the exponential growth of a generic terminal solution.
     The code spectrum_shooting.py supplied approximate roots from which the
candidate intervals were selected. The Arb verifier selfadjoint_interval_verify.
py repeats the shooting calculation with interval Taylor arithmetic. For each interval
mj ± 5 × 10−12 , it propagates the regular solution at both λ-endpoints to evaluate
u(T, λ) and u′ (T, λ). Opposite signs of u(T, λ) at the two endpoints imply a Dirichlet
finite-interval eigenvalue in the interval, and opposite signs of u′ (T, λ) imply a Neu-
mann one. Since the verifier finds an eigenvalue in each of 11 pairwise disjoint negative
intervals, every interval contains exactly one Dirichlet and one Neumann eigenvalue.
The inequality (3.4) then encloses λj (H). The end result is the following certificate.
     Certificate 3.2 (Negative spectrum). The modified half-line operator has ex-
actly eleven negative eigenvalues contained in the intervals in Table 3.1.
                                     TEN DIGITS ON A TRAIN                                       13
                                           Table 3.1
     All negative eigenvalues of H. The Arb verifier certifies the Sturm count and the Dirichlet–
Neumann endpoint signs for the intervals mj ± 5 × 10−12 , with row j corresponding to λj . The first
eigenvalue also has the independent Temple certificate in Theorem 3.1.

            j     midpoint of certified interval   radius      value to 10 decimal places
            1     −5.3196761542354 × 10−2          5 × 10−12   −0.0531967615
            2     −1.9367409728912 × 10−2          5 × 10−12   −0.0193674097
            3     −8.2420874282006 × 10−3          5 × 10−12   −0.0082420874
            4     −3.6685443298679 × 10−3          5 × 10−12   −0.0036685443
            5     −1.6120468156717 × 10−3          5 × 10−12   −0.0016120468
            6     −6.6973685120550 × 10−4          5 × 10−12   −0.0006697369
            7     −2.5156770074481 × 10−4          5 × 10−12   −0.0002515677
            8     −8.0493482670423 × 10−5          5 × 10−12   −0.0000804935
            9     −1.9899482902437 × 10−5          5 × 10−12   −0.0000198995
           10     −3.1084439935000 × 10−6          5 × 10−12   −0.0000031084
           11     −1.6239698497433 × 10−7          5 × 10−12   −0.0000001624




    4. The non-normal resonance pair. The second problem was deliberately less
forgiving. The target is the resonance pair λ̂±
                                              2 from [6, Table 6]. That work already
proved the existence of one resonance in each parity sector, but computed both to
two digits and did not separate them. Our aim is to replace that common enclosure
by two disjoint enclosures determining both components to ten decimal places.
    Here, the feedback loop in Figure 1.1 became even more important: high-precision
candidates appeared quickly, but the failed certificates forced changes in the proof
strategy. The result is a general and reusable method: a global projective multiple-
shooting certificate that turns a non-normal complex-scaled resonance calculation
from an unstable shooting problem into a verified finite-dimensional existence theo-
rem.



    4.1. Background. The underlying operator is the Schrödinger operator
                  d2
             −       + Q(x),         Q(x) = (x2 − 1.6) exp(−x2 /10),           x ∈ R.
                 dx2
However, the numbers in [6, Table 6] are not L2 eigenvalues, but resonances.
     Because Q is an even function, the full-line problem decomposes into two half-
line problems: odd states satisfy the Dirichlet condition
                                                  √         u(0) = 0, while √ even states
satisfy the Neumann condition u′ (0) = 0. With −λ chosen  √    so  that Re    −λ > 0, the
condition at infinity is exponential decay, u(x) ∼ exp(− −λx), which gives the usual
L2 eigenvalue problem. Resonances arise as poles of the meromorphic continuation
across the continuous spectrum λ ∈ [0, ∞), equivalently as discrete eigenvalues of
a complex-scaled operator discussed below. After continuation, the same outgoing
solution need not lie in L2 ; in the examples below, it grows exponentially on the real
axis. This is the complex-scaling interpretation used in [6, Sec. 2, eqs. (2.1)–(2.5)]; see
also the classical references [2, 25] and the book [12]. The complex-scaled boundary-
value problems that we use below are highly non-normal, so even plausible numerical
roots computed with high precision can be treacherous.
14                                        M. J. COLBROOK


                                    Prompt 4: from Marco’s desired four digits to ten

                  Wonderful, now let’s do a different problem. Marco sent me the message
              pasted below. I want us to push the boat out. Figure out a way to compute
              this resonance to 10 digits of accuracy (not just the 4 digits that Marco would
              like). It has to be fully rigorous and accurate. We may need to come up with
              new ideas to do this.


     AI response, worked for 1h 15m 12s

         I’ve identified the target and obtained high-precision candidate values.
     The pair is the Abramov pair λ̂−         +
                                        2 , λ̂2 in Table 6, at the bottom of page 15
     of Bögli–Brown–Marletta–Tretter–Wagenhofer. Using the paper’s stretched
     scaling (R, θ, X) = (10, 0.76, 10), I get:

     (4.1)         λ̂−
                     2 ≈ 0.9180018173874698 − 17.00068824973865 i,

     (4.2)         λ̂+
                     2 ≈ 0.9178768454495876 − 17.00064483695551 i.

     These are high-precision candidates, not yet a rigorous certificate. The route I
     think will get us the rigorous 10 digits is: work in the z-plane,
                                                              √        shoot backwards
     from X = 10 with the outgoing condition y ′ (X) = − −z, form the Dirichlet
     and Neumann determinants, propagate the ODE and variational equation
     with interval Taylor arithmetic, apply an interval Newton/Krawczyk test on
     small boxes in z, use the paper’s truncation bound αX,θ,R ≤ 1.77 × 10−17 , so
     that the tail error is far below the requested ten-digit scale. The next step is
     to turn the Taylor shooting into an interval certificate.


     Here, λ̂−       +
             2 and λ̂2 correspond to the Dirichlet and Neumann half-line problems,
respectively. The assistant identified both resonances and suggested the following
possible validation route. Ordinary complex scaling sends λ to z = e2iθ λ. For this
difficult pair, one instead chooses R > 0 and follows the complex ray ξ = Reiθ x
for x ≥ 0, with y(x) = u(ξ). Multiplying the transformed equation by R2 e2iθ and
truncating the domain gives
                       −y ′′ (x) + qθ,R (x)y(x) = z y(x),        0 ≤ x ≤ X,
where
                                                    R2 e2iθ x2
                                                              
                      2 2iθ    2 2iθ 2
                                                                              z = R2 e2iθ λ.
                                              
         qθ,R (x) = R e       R e     x − 1.6 exp −                   and
                                                       10
We use the same  √parameters as [6]: X = 10, θ = 0.76 rad, and R = 10.
    Let k(z) = −z, with Re k(z) > 0. The outgoing free solution in the absence of
a potential is the decaying exponential exp(−k(z) x). Thus, we impose the following
boundary condition at the truncation point X:
(4.3)                                  y ′ (X) + k(z)y(X) = 0.
For each z, integrating the outgoing solution backwards from X to 0 yields FD (z) =
y(0; z) and FN (z) = y ′ (0; z). Zeros of FD and FN give the odd and even finite-
interval resonances, respectively. Figure 4.1 shows the corresponding solutions at the
numerical candidate resonances. A tail bound can then be used to account for the
contribution of the tail of qθ,R on [X, ∞) to the true outgoing solution.
     In exact arithmetic, this is a clean analytic formulation. For computation, this
                                                TEN DIGITS ON A TRAIN                                                        15

                              Odd/Dirichlet Solution                                         Even/Neumann Solution
             105                                                            105




                                                               jyN (x)j
jyD (x)j



             100                                                            100
                          0   1     2       3          4   5                             0   1        2       3      4        5




                                                                 sin(arg(yN (x)))
  sin(arg(yD (x)))




                     1                                                              1

                     0                                                              0

                     -1                                                             -1
                          0   1     2       3          4   5                             0   1        2       3      4        5
                                        x                                                                 x
     Fig. 4.1. Finite-interval resonance solutions for the stretched complex-scaled problem. The
solutions are normalized by yD (10) = 1 and yN (10) = 1, and only the interval 0 < x ≤ 5 is shown
to make the oscillation and growth visible. The upper panels plot |y(x)| on a logarithmic scale; the
lower panels plot sin(arg y(x)). This figure is illustrative only: the rigorous resonance enclosure is
supplied by the global projective Krawczyk certificate.

                                             Table 4.1
     Diagnostic routes to the resonance certificate. Each failed route identified which object should
not be certified or an obstacle to overcome, and so narrowed the form of the final proof.

route                                    obstruction                                         lesson
amplitude shooting         enclosures grew rapidly in the                                    raw amplitudes are poor variables
                           unstable solution component                                       for long validated propagation
variation-of-constants and free growth and some wrapping                                     better local coordinates did not
amplitude Lohner forms     were reduced, but one-way                                         cure the long composition
                           amplification remained
midpoint or Wronskian      the enclosure of the matching                                     this characteristic formulation
matching                   determinant remained too wide                                     was still too ill-conditioned
Riccati/projective         amplitude growth disappeared, but                                 solution lines are the appropriate
shooting                   a chart denominator could no                                      variables, but the long one-way
                           longer be certified to exclude zero                               composition remained unsuitable
centered projective Lohner local projective remainders initially                             the node lines should be treated
forms                      stayed small but later widened                                    as simultaneous unknowns
more precision             roundoff shrank while the principal                               the tested formulation was not
                           widths and failure point persisted                                roundoff limited
global projective multiple               short validated maps coupled by                     a componentwise Krawczyk
shooting                                 projective matching equations                       inclusion succeeded



is an unstable one-way shooting: terminal and local interval errors are propagated
through the non-normal dynamics to x = 0.

     4.2. Useful failures. The final certificate did not appear at once. Several fail-
ures are summarized in Table 4.1. Each failed attempt found an obstruction and
changed the next question (Figure 1.1). They also had a clear logic. Amplitudes were
too unstable. Changes of basis and midpoint matching improved the scaling, but still
left a boundary determinant built from long propagation. Projective coordinates re-
vealed the right variable (the solution line), but not the right proof. The final method
in Subsection 4.3 kept the projective variable and replaced one-way shooting with a
global multiple-shooting interval Newton system.
     The AI assistant repeatedly predicted that the next modification would complete
the proof. The subsequent failures show why such predictions were overly optimistic.
16                                      M. J. COLBROOK


                                              Prompt 5: asking for interval arithmetic

                 This is excellent work! Now let’s push for a fully rigorous verification. Will
              you need to do interval arithmetic in Python?


     AI response, instant response

         Yes, I think we do need interval arithmetic in Python, or something equiv-
     alent. For this problem, ordinary high-precision floating point is only enough
     to locate the candidates. To make a 10-digit claim rigorous, we need certi-
     fied enclosures for: the ODE propagation, the determinant values F± (z), the
     derivative with respect to z, the interval Newton or Krawczyk inclusion test,
     and the truncation/scaling error from replacing the half-line problem by the
     X = 10 boundary problem.
         The good news is that the problem is low-dimensional enough that we
     probably do not need a huge interval package. I’d build a small complex-
     interval Taylor solver in Python using rational/decimal
                                                           √ endpoints where safe,
     with our own interval complex square-root branch for −z. The key validation
     would be: N (B) = z0 −F ′ (B)−1 F (z0 ) or a Krawczyk variant, showing N (B) ⊂
     B for each small box B around the two candidate roots.

    On each short interval, the Taylor coefficients give a finite, checkable enclosure of
the transfer map and its derivative. The first issue was whether these local enclosures
could be composed across [0, X] without losing the boundary condition.

                                           Prompt 6: committing to the interval route

                 Wonderful, let’s do it!


     AI response, worked for 1h 27m 14s

         Yes, and I’ve started the rigorous verification machinery. I installed
     python-flint and built several Arb-based verifier prototypes in the workspace.
         Important: I do not yet have a completed rigorous 10-digit certificate.
     The naive interval methods fail: direct amplitude propagation creates huge
     wrapping/unstable-direction enclosures, even though the floating point deter-
     minant is tiny. The projective Riccati version is the promising route, but its
     current chart switching still needs a sharper Lohner/Taylor-model style en-
     closure; otherwise Arb refuses reciprocal chart switches when the interval still
     contains zero. That is a genuine rigor issue, not a coding nuisance.
         So the next step is clear: replace the current absolute interval Riccati
     propagation by a centered projective Taylor model. In practice, propagate a
     high-precision midpoint line plus a small rigorous error ball in a locally chosen
     Möbius chart, updating the chart center along the computed trajectory. That
     should remove the zero-containing chart-switch problem and give a usable
     Krawczyk proof.


    The first attempts used direct interval shooting, propagating the solution in com-
plex balls using interval Taylor methods with rigorous remainder estimates at each
step. The difficulty was that these local errors compounded: they were fed into
transverse directions amplified by the non-normal shooting dynamics. The resulting
                                TEN DIGITS ON A TRAIN                                    17

enclosures, therefore, measured not only uncertainty in the resonance but also the
instability of the proof architecture itself: small Taylor and interval errors carried
through an unstable one-way propagation.
    Variation of constants removed much of the free evolution, while interior matching
shortened the shooting intervals. Both improved the scaling, but the argument still
ended with a scalar matching determinant built from interval-dependent data, whose
enclosure was too wide to certify the zero.
    Projective coordinates removed the irrelevant amplitude and followed the line
spanned by (y, y ′ ), the object on which the boundary conditions depend. However, in
the one-way Riccati and projective attempts, the intervals became too wide to prove
that the denominators in maps induced by the transfer matrices stay away from zero.
    At this stage, it was natural to ask whether more precision could solve the issue.

                               Prompt 7: extended precision as a possible cure?

              OK, would it help to use extended precision floats? Can we do it by just
           using way more precision? If not, try this other method you discussed.


   AI response, worked for 40m 21s

       Extended precision alone won’t help. I tested exactly that on the centered-
  projective verifier: same failure point at 360 bits and 900 bits. The rounding
  part shrank dramatically, but the actual enclosing ball did not. At the failure
  point: (a) 360 bits; projective coordinate radius about 21.1635544598, denom-
  inator radius about 85.0013815165 (b) 900 bits; projective coordinate radius
  still about 21.1635544598, denominator radius still about 85.0013815165. So
  precision improved the tiny Arb roundoff decorations from around 10−105 to
  10−267 , but the useful interval width stayed unchanged. That means the ob-
  struction is interval dependency/wrapping, not floating point precision.
       I tried the other method and added a new verifier that: builds midpoint
  frames along the left and right solution lines; converts each rigorous Taylor
  step into a local projective Möbius transfer map; propagates only the centered
  projective coordinate and its z-derivative; tries a Krawczyk certificate on the
  z-box. This is the right structural method, but the current implementation
  still does not certify the root. The new failure is much more informative: the
  centered scalar projective interval still wraps and grows before the matching
  point, even though the true midpoint coordinate should remain near zero.
       So the next step is a Taylor-model/Lohner split for the projective coor-
  dinate, e.g., propagate w(z) = w0 + w1 (z − z0 ) + E with a separate rigorous
  remainder E, rather than propagating w as one undifferentiated complex ball.
  So: no certificate yet, but we have narrowed the obstruction.


    The answer was no. Comparing 360-bit and 900-bit runs made the point plain:
roundoff terms shrank, but the relevant enclosing balls did not. Increased precision
removed the much smaller rounding contribution, but the dominant widths came from
propagating interval enclosures through unstable transverse directions.

                                                   Prompt 8: the full-force request

              OK, please go full force and do this to get the verification.
18                                       M. J. COLBROOK


     AI response, worked for 2h 30m 12s

         I pushed this hard, and I do not yet have a rigorous 10-digit certificate I can
     honestly stand behind. What I did get is useful: one-way verified shooting is
     the wrong architecture for this resonance. I built and tested Arb complex ball
     interval Taylor shooting, amplitude Lohner splitting, centered projective prop-
     agation, projective Lohner splitting, and smoother/propagated frame variants.
     They all fail for the same structural reason: tiny local proof defects are am-
     plified through an unstable transverse projective direction. More precision
     postpones the failure but does not remove it.
         The next certificate should be a global sparse multiple-shooting Krawczyk
     or argument-principle/VNODE-style validation, not one-way shooting. The
     finite-interval root is numerically nailed; the missing piece is a global verified
     eigenvalue enclosure around the tiny boxes.


     By separating a center trajectory from the enclosing remainder, the Lohner-style
variants [17] substantially reduced some forms of wrapping—the artificial enlargement
caused by repeatedly replacing a thin correlated set by boxes or balls. They did
not, however, make the one-way validation succeed. A centered-projective run with
h = 0.001, Taylor order 180, and 600-bit precision kept the projective radius small
for about 500 steps, but later could no longer prove that a denominator was nonzero.
     Better local control had not removed the global amplification of transverse un-
certainty. The next formulation had to put all mesh nodes in the unknown vector
and validate the boundary-value problem at once. In validated-computation terms,
this is the analog of replacing an unstable shooting method by a multiple-shooting or
collocation formulation.

    4.3. Success: A global projective certificate. The above diagnosis pointed
to the successful route explained in this section. The construction has three steps.
First, replace solution vectors by solution lines, so that exponential growth in the
amplitude is divided out. Second, introduce one projective unknown at each mesh
point, so that the local transfer maps are short and the boundary conditions are im-
posed simultaneously. Third, apply a Krawczyk inclusion test to this global matching
system, with a tail estimate included in the final boundary equation.

      4.3.1. Setting up the finite-interval system. To set up this system, let
                         xj = jh,       h = 0.0025,        j = 0, . . . , 4000.
Recall that z is the stretched spectral parameter in
(4.4)               −y ′′ (x) + qθ,R (x)y(x) = z y(x),        0 ≤ x ≤ X = 10,
               −2 −2iθ
and λ = R e          z. For each candidate spectral parameter z0 , let Y (x; z0 ) denote
the solution propagated from the left boundary line: Y (0; z0 ) = 0, Y ′ (0; z0 ) = 1
in the Dirichlet case, and Y (0; z0 ) = 1, Y ′ (0; z0 ) = 0 in the Neumann case. Set
Yj = Y (xj ; z0 ) and Yj′ = Y ′ (xj ; z0 ), and choose the unitary frame (ordered basis)

                                                          Yj −Yj′
                                                                 
                                             1
                           Pj =                                     ,
                                  (|Yj |2 + |Yj′ |2 )1/2 Yj′ Yj
whose columns provide local coordinates for the Cauchy data (y, y ′ )T . A nearby solu-
tion line at xj , provided its first coordinate in the Pj -frame is nonzero, is represented
by the line spanned by Pj (1, wj )T . The verifier first computes high-precision point
                                TEN DIGITS ON A TRAIN                                     19

approximations to the center trajectory and uses them to construct fixed, numeri-
cally near-unitary frames. These frames are coordinate choices rather than certified
approximations to the exact center line; their inverses and all subsequent transfer
maps are enclosed rigorously in Arb. The coordinate wj = 0 therefore denotes the
numerical center line used to define the chart. Projective coordinates help because
the scale of the solution, which may grow or decay violently, is discarded, while the
line on which the boundary condition depends is retained.
     If U = (y, y ′ )T , then (4.4) is equivalent to the first-order system
                                                                           
                     ′                                            0       1
                U (x) = A(x, z)U (x),          A(x, z) =                      .
                                                            qθ,R (x) − z 0
For xj ≤ x ≤ xj+1 , let Φj (x, z) be the 2-by-2 solution matrix of this first-order system,
normalized by Φj (xj , z) = I. Thus Φj (x, z) maps Cauchy data at xj to Cauchy data
at x. The transfer matrix is Tj (z) = Φj (xj+1 , z) and maps Cauchy data at xj to
Cauchy data at xj+1 :                                         
                                y(xj+1 )               y(xj )
                                            = Tj (z)               .
                               y ′ (xj+1 )             y ′ (xj )
Equivalently, the two columns of Tj (z) are obtained by solving the ODE across the
short interval with initial data (1, 0)T and (0, 1)T . In the moving frames, let
                                           
                              aj (z) bj (z)       −1
                                              = Pj+1  Tj (z)Pj .
                              cj (z) dj (z)
Hence, the local transfer map on the projective coordinate is the Möbius map
                                                 cj (z) + dj (z)wj
                          wj+1 = fj (z, wj ) =                     .
                                                 aj (z) + bj (z)wj
The variables wj are scalar projective coordinates, not Cauchy data themselves. In
the frame Pj , the value wj represents the line
                                               
                                                  1
                             Lj (wj ) = span Pj        .
                                                 wj
Thus wleft (z) and wright (z) are the scalar coordinates whose associated lines are
the left boundary line and the outgoing line at X, respectively. The left line is
LD                   T                                     N                 T
  left = span{(0, 1) } for the odd/Dirichlet problem, and Lleft = span{(1, 0) } for the
even/Neumann problem. The right outgoing line is Lout (z) = span{(1, −k(z))T }.
      The finite-interval resonance condition becomes
       w0 = wleft (z),   wj+1 = fj (z, wj ), j = 0, . . . , 3999,   w4000 = wright (z).
Thus, the verifier constructs a map F : C4001 × C → C4002 . For W = (w0 , . . . , w4000 ),
the global system F (W, z) = 0 for the finite interval [0, X] has the form
                                F0 (W, z) = w0 − wleft (z),
                 Fj+1 (W, z) = wj+1 − fj (z, wj ),         j = 0, . . . , 3999,
                            F4001 (W, z) = w4000 − wright (z).
On each subinterval [xj , xj+1 ], the local transfer matrices and their z-derivatives are
enclosed by Taylor integration with Arb complex ball arithmetic. The verifier checks
a Picard majorant condition on each local Taylor disk and uses Cauchy estimates to
bound the omitted tails. Thus the short maps Tj (z), rather than one long propagated
solution, enter the global residual with rigorous local error bounds.
20                                         M. J. COLBROOK


    4.3.2. Structured inverse of the Jacobian. The interval Newton test is ap-
plied on a polydisc
      B = (w0 , . . . , w4000 , z) : |wj | ≤ rj , j = 0, . . . , 4000, |z − z0 | ≤ 10−12 .
          

This is a simultaneous neighborhood of all projective node variables and of the spectral
parameter. At the center (W0 , z0 ) = (0, . . . , 0, z0 ) of the polydisc B, let
                                                                 ′                      ′
     αj = ∂w fj (z0 , 0),       βj = ∂z fj (z0 , 0),       γ0 = wleft (z0 ),      γX = wright (z0 ).
Given a right-hand side r, the linear system F ′ (W0 , z0 )(∆W, ∆z) = r has the form
                                           ∆w0 − γ0 ∆z = r0 ,
                   ∆wj+1 − αj ∆wj − βj ∆z = rj+1 ,                 j = 0, . . . , 3999,
                                        ∆w4000 − γX ∆z = r4001 .
Thus, applying the inverse of the midpoint Jacobian does not require solving a large,
dense linear system. For a fixed ∆z, the first 4001 equations can be solved by the
forward recurrence
                  ∆w0 = r0 + γ0 ∆z,            ∆wj+1 = rj+1 + αj ∆wj + βj ∆z.
Let ∆wj = pj + sj ∆z, then the recurrence propagates the two scalar sequences
           p0 = r0 ,        s0 = γ0 ,      pj+1 = rj+1 + αj pj ,          sj+1 = βj + αj sj .
The final boundary equation then gives ∆z = (r4001 − p4000 )/(s4000 − γX ). The certifi-
cate files prove a rigorous lower bound greater than 5.11 for |s4000 −γX | in both parity
cases, so this structured inverse is safely defined on the relevant interval data. Let
A0 be an approximation to the above Jacobian obtained by taking rigorous derivative
enclosures. Let Υ = A−1  0 be the corresponding structured inverse preconditioner.

    4.3.3. A tail-corrected Krawczyk-type inclusion. Conceptually, the verifier
applies Newton’s method. The difference is that the computation is performed on the
whole polydisc B, not only at the center (W0 , z0 ), and must take into account the
truncation tail. For the finite-interval system F (W, z) = 0, the Krawczyk inclusion
            (W0 , z0 ) − ΥF (W0 , z0 ) + I − ΥF ′ (B) (B − (W0 , z0 )) ⊂ int B
                                                     

gives existence and uniqueness in the polydisc [28, Ch. 6] [19, 18, 22].
    However, the truncation at X is not, by itself, the half-line resonance problem.
We imposed (4.3), but the true outgoing solution sees the tail of qθ,R on [X, ∞). If
                     Z ∞
            αX,θ,R =     |qθ,R (x)| dx < 1 and ε = αX,θ,R /(1 − αX,θ,R ),
                            X

then the terminal data for the true outgoing solution satisfies [8, Thm. 3.3]
               y(X) = 1 + η0 ,           y ′ (X) = −k(z)(1 + η1 ),         |η0 |, |η1 | ≤ ε.
                                                                      ′
Hence, for the true terminal projective coordinate τ = y (X)/y(X),6
                                                       η0 − η 1   2ε|k(z)|
(4.5)                        |τ + k(z)| ≤ |k(z)|                ≤          .
                                                       1 + η0      1−ε
    6 Step B of [6, Sec. 3] uses a similar (but amplitude) tail estimate, but then counts zeros of

a finite-interval determinant by interval arithmetic and the argument principle. Marletta tells me
that the exploratory Fortran code behind the earlier computations also rescaled the solution during
propagation, which is morally a projective-line device; the present proof replaces this by a 4000-node
global projective matching system certified by a Krawczyk inclusion test.
                               TEN DIGITS ON A TRAIN                                   21

The true half-line equation has the form F (W, z) + e∗ (z) = 0, where the final-row
correction e∗ (z) is analytic on the chosen z-neighborhood and satisfies e∗ (z) ∈ E.
Here, E denotes an enclosure of the image, under the final projective chart, of the
disk in (4.5) relative to the free outgoing coordinate.
    The code verifies the robust inclusion
            (W0 , z0 ) − ΥF (W0 , z0 ) − ΥE + I − ΥF ′ (B) (B − (W0 , z0 )) ⊂ int B
                                                          
(4.6)
and uses a Brouwer argument. Define
                                                                 
                          T (W, z) = (W, z) − Υ F (W, z) + e∗ (z) .
The term I − ΥF ′ (B) (B − (W0 , z0 )) controls the nonlinear variation of F over the
                          

whole polydisc, while −ΥE controls the tail uncertainty. The inclusion (4.6) proves
that T maps the compact convex polydisc B into its interior. Brouwer’s fixed-point
theorem gives (W∗ , z∗ ) ∈ B with T (W∗ , z∗ ) = (W∗ , z∗ ), and since Υ is invertible,
F (W∗ , z∗ ) + e∗ (z∗ ) = 0. Thus the finite-interval Krawczyk test gives uniqueness for
the truncated problem, while the tail-corrected inclusion gives existence for the half-
line resonance problem in the same certified polydisc.
    4.3.4. The final prompt and certificate. Here is my final prompt:

                                                    Prompt 9: the step to victory

              OK, please try this next step. Take as long as needed.


   AI response, worked for 2h 36m 9s

      Done. This time, the global verification worked. I implemented a
  global projective multiple-shooting Krawczyk verifier in resonance_global_
  projective_verify.py. It verifies all node transfer equations and both
  boundary conditions at once, avoiding the unstable one-way shooting obstruc-
  tion. Certified values:
          λ̂−
            2 = 0.91800181738746978598 − 17.00068824973864792716 i

          λ̂+
            2 = 0.91787684544958761758 − 17.00064483695551276997 i.

  The finite-interval Arb complex ball Krawczyk certificates succeeded for both
  parities: Dirichlet/minus z radius: 6.4680503619 × 10−17 Neumann/plus z
  radius: 6.4639342899 × 10−17 Corresponding finite-interval λ radii: < 6.47 ×
  10−19 Using the 2014 paper’s tail bound αX,θ,R ≤ 1.77 × 10−17 conservatively
  in the z-plane gives total λ uncertainty below 8.3 × 10−19 .


    At this stage, I should highlight another warning. The response above records
the exchange with AI, not the final audit of the proof objects. The finite-interval
certificates were sound, but the first separate tail checker did not prove the passage
from the truncated problem to the half-line resonance.
    Specifically, the finite-interval system is F (W, z) = 0, whereas the half-line prob-
lem requires F (W, z) + e∗ (z) = 0. The checker had bounded the tail correction and
then compared a worst-case required node radius with a worst-case allowed node ra-
dius. That is not enough for a nonuniform polydisc: the proof needs, for every node j,
the required radius in wj to be smaller than the allowed radius rj . I therefore corrected
resonance_global_projective_verify.py and reran the global projective verifier
with the tail interval E inserted directly into the final boundary row. This slightly
22                                  M. J. COLBROOK


changed the radii from those in the AI response. Here is the corrected procedure.

     Tail-robust global projective verifier

  1. Choose the parity, centre z0 , mesh xj = jh, and frames Pj along the midpoint
     solution line, so that this line has coordinate wj = 0 at every node.
  2. Use Arb complex ball Taylor integration to enclose the local transfer matrices
     Tj (z) and their z-derivatives on the prescribed z-neighborhood.
                                                                     c (z)+d (z)w
  3. Convert the transfer matrices to the Möbius maps fj (z, w) = ajj (z)+bjj (z)w and
     verify that the denominators stay away from zero on the relevant boxes.
  4. Form the global residual F (W, z), consisting of the left boundary equation, the
     4000 local matching equations, and the right projective boundary equation.
  5. Apply the structured inverse Υ by the forward recurrence.
  6. Insert the tail interval E into the final boundary row and verify the robust
     inclusion (4.6) component by component in the nonuniform polydisc B.

     Certificate 4.1 (Resonance pair). Let
       cD = 0.9180018173874697859784363 − 17.0006882497386479271609736 i,
       cN = 0.9178768454495876175818796 − 17.0006448369555127699716473 i.

Then |λ̂−
        2 − cD | < 6.50 × 10
                            −19
                                and |λ̂+
                                       2 − cN | < 6.50 × 10
                                                           −19
                                                               . In particular,
  λ̂−
    2 = 0.9180018174 − 17.0006882497 i,         λ̂+
                                                  2 = 0.9178768454 − 17.0006448370 i

to ten decimal places.
    The two certified centers are separated by |λ̂−      +
                                                   2 − λ̂2 | > 1.32 × 10
                                                                        −4
                                                                           , which is much
larger than the certified radii, so the two parity resonances are distinct.
     Proof. Let zσ denote the computed stretched resonance, with σ = D for the
odd/Dirichlet problem and σ = N for the even/Neumann problem. The tail-included
verifier resonance_global_projective_verify.py uses the bound αX,θ,R ≤ 1.77 ×
10−17 from [6, p. 15] to enclose the tail correction in the final projective boundary
row. It then checks the robust inclusion (4.6) in the same nonuniform polydisc B,
component by component. The largest node-radius fractions are 0.6474 and 0.6469,
so the inclusions are strict.
     Thus the Brouwer argument above gives a solution of the half-line resonance
equation in B. Since any fixed point lies in the image set on the left-hand side of
(4.6), the verified z-radii are the smaller image radii, not the input radius 10−12 . The
certificate files certificate_D_global_projective_tail.json and certificate_
N_global_projective_tail.json give |z − zD | < 6.4982 × 10−17 and |z − zN | <
6.4954 × 10−17 . Since λ = R−2 e−2iθ z with R = 10, the certified z-radii give λ-radii
below 6.50 × 10−19 , even after rounding the certificate centres to the displayed cσ .

     5. Lessons from the certificates.

     5.1. Three certificates, two proof cultures. The preceding sections provide
three certificates but reflect two proof cultures. In the self-adjoint problems, stability
is supplied by the operator. For the ground state, Temple’s inequality turns a trial
vector into an eigenvalue enclosure once the residual and comparison gap are known.
For the full negative spectrum, Sturm oscillation counts the levels, Dirichlet–Neumann
bracketing traps them, and the nonnegative tail rules out spectrum beyond the cutoff.
                               TEN DIGITS ON A TRAIN                                  23

Variational order, comparison, and oscillation carry the proof.
    The resonance problem lacks this protection. The complex-scaled operator is
non-self-adjoint: its eigenvalues have no variational ordering, and without condition-
ing information, a small residual need not locate a nearby genuine eigenvalue. The
certificate therefore validates a different object: not a long shoot from one endpoint to
the other, but a global matching system for projective solution lines. The Krawczyk
inclusion proves a zero of this finite nonlinear system, and the tail-robust inclusion
transfers the result to the half-line resonance problem.
    This is the mathematical hinge of the case study. The AI assistant could produce
plausible candidates in both settings, but the certificate had to match the problem’s
stability structure. The digits look similar in a table; the proof objects do not.
     5.2. Reusable certificate-seeking principles. The workflow in Figure 1.1
separates exploration from certification. The upper lane records proposed methods,
code, candidate values, and failures. The lower lane begins only once there is a
finite object to check against a theorem, inequality, or validation criterion. Thus, a
Ritz calculation supplies a trial vector, not an eigenvalue enclosure; a floating-point
shooting code supplies candidate intervals, not a Sturm count; and a high-precision
resonance determinant supplies a candidate zero, not a resonance enclosure. In each
case, the mathematical status changes only after the relevant certificate has been
checked.
     This separation was not cosmetic. The slow part was deciding what the artifacts
proved: repairing gaps, supplying missing arguments and references, and writing the
mathematics carefully. Reproducibility alone is therefore too weak a standard; one
must also know whether the reproduced object is a locator, a diagnostic, or a cer-
tificate. AI-generated prose can blur these distinctions. Failures also belong in the
record. In the resonance problem, failed one-way validations showed that neither a
propagated amplitude nor a single projective trajectory was the right object to certify.
In the self-adjoint problem, the floating-point spectrum calculation became useful only
after it was separated from a later interval verifier that carried the proof.
     5.3. Social implications. AI makes plausible numerical output cheap. Digits,
explanations, and code may now appear before anyone has decided what the compu-
tation shows/proves. This is not a reason to dismiss such output; it is a reason to
read it differently. The question is not only whether a number is plausible, but what
mathematical object makes it checkable and trustworthy. In this paper, the transcript
records the search; the certificates carry the claims.
     The same change raises questions about credit and attribution. Visible manual
labor is an especially poor proxy for mathematical contribution in an AI-assisted work-
flow. Greater weight falls on the intellectual and technical decisions: what question
was posed, what representation and normalization were chosen, what theorem was ap-
plicable, what obstruction was correctly diagnosed, how the verifier was implemented
and audited, and which certificate ultimately survived scrutiny. Some problems will
also become routine. If the main difficulty is assembling standard code or finding the
right formula, the problem may no longer carry the same training value or credit. That
is not a loss to hide from; it redirects attention to formulation, stability, validation,
counterexamples, and interpretation.
     There is a pedagogical opportunity here, and a danger. Validated computation
can look forbidding when introduced as a catalog of interval methods, Taylor models,
and fixed-point theorems. In an AI-assisted workflow, the need for validation arises
naturally: the assistant proposes numbers, and the mathematician asks what would
24                                   M. J. COLBROOK


make them checkable. But many tasks by which students learn, and are assessed,
are precisely the tasks for which an AI assistant is now useful: writing code, testing
examples, finding references, and drafting arguments. Students should use powerful
tools, but the standard must rise with the tool. They must be trained to find the gap
in a fluent but false argument, and to know what a computation is meant to support.
      There is an institutional lesson too. AI is no reason to weaken mathematical
training; it is a reason to deepen it. Powerful tools demand skilled operators. Univer-
sities, professional societies, and funding agencies should invest in the expertise and
infrastructure needed to evaluate AI-assisted mathematical work. Without such train-
ing, users risk becoming dependent on fluent output without developing the ability
to judge what is meaningful, what assumptions are missing, and what, if anything, a
computation has shown. There is also an equity issue. If the advantage shifts to those
with the training, colleagues, time, and institutional resources to turn output into re-
liable mathematics, then broad access to advanced mathematical and computational
education becomes more important, not less.
      The community is beginning to say this explicitly. The Leiden Declaration on Ar-
tificial Intelligence and Mathematics, published on June 2, 2026, and endorsed by the
International Mathematical Union, emphasizes verification, attribution, disclosure, re-
search autonomy, funding, and unequal access [3]. Publication policy is moving in the
same direction. In SIAM News,7 Kolda frames AI use in SIAM journal submissions
as a contract of trust among authors, editors, referees, and readers. That is the right
institutional tone: not prohibition, but responsibility, disclosure, and consequences
when work breaks the trust on which mathematical publication depends.
      This is not only a question about certified eigenvalues. Numerical analysis is
not, and should not become, a field in which every computation is forced into an
interval certificate. Much of the subject is exploratory: modeling, discretization,
asymptotics, conditioning, complexity, software, and simulation. In such settings, the
standard is not proof of every digit, but clarity about the evidence being offered.
Depending on the problem, that evidence may be a convergence study, a conditioning
analysis, an uncertainty estimate, a comparison with experiment, or an independent
implementation. AI makes this distinction sharper. Exploration should be presented
as exploration; a numerical statement presented as a theorem or certified value carries
a different burden.
     6. Conclusion. This article has proved that a singular self-adjoint Schrödinger
operator has exactly eleven negative eigenvalues and has enclosed all of them to ten
decimal places. It has also replaced a common two-digit enclosure of a notoriously
difficult odd–even resonance pair by two disjoint enclosures determining both real and
imaginary parts to seventeen decimal places.
     The self-adjoint certificates use Temple’s inequality, Sturm oscillation, and Dirich-
let–Neumann bracketing. The resonance certificate instead uses a global projective
multiple-shooting system, a componentwise Krawczyk inclusion, and a robust Brouwer
inclusion for the infinite tail; more generally, it gives a reusable validation route for
ill-conditioned complex-scaled boundary-value problems: certify short transfer maps,
introduce projective node variables, and verify the global matching equations.
     For roughly a decade, I have studied spectral computations: how to perform them,
when to trust them, and what can be achieved for difficult operator problems [9].

    7 T. G. Kolda, “A Contract of Trust: Artificial Intelligence Usage for SIAM Journal Sub-

missions,” SIAM News, May 1, 2026, https://www.siam.org/publications/siam-news/articles/
a-contract-of-trust-artificial-intelligence-usage-for-siam-journal-submissions/.
                                   TEN DIGITS ON A TRAIN                                         25

Calculations such as the resonance enclosure have traditionally required substantial
effort. It is natural to ask whether the above should worry me. What remains of such
expertise when an AI-assisted exchange can produce high-precision candidates and
plausible proof strategies so rapidly?
     The answer is that the expertise does not disappear; it changes role. Without that
background, I would not have known what to ask, which answers to distrust, which
failures called for a change of formulation, or what finite certificate could support the
claim. The assistant greatly accelerated exploration, but it did not remove the need
for mathematical judgment. Instead, the bottleneck shifted from producing plausible
numerical evidence to deciding what mathematical claim that evidence can support.
     Nor was the exchange a sequence of uninterrupted successes. For the eleven self-
adjoint eigenvalues, the initial response found the correct qualitative picture and useful
candidates, but its shooting code was only a floating-point locator. In the resonance
problem, several candidate validation routes failed while revealing why the problem
was difficult. The most important error came after apparent success: a separate tail
checker failed to verify the half-line problem. The nonuniform polydisc required a
later componentwise inclusion at every node. The recorded exchange also did not
produce the associated-Legendre representation of the zero-energy solution u0 , which
later supplied a shorter analytic zero count.
     This paper is not an argument against AI-assisted mathematics. I expect to use
these tools, and I expect many mathematicians to use them fruitfully. However, the
standard will have to rise with the tool. AI tools can range across a vast mathematical
landscape, suggest methods we might not have tried, sharpen our techniques, and
remove routine work. We should welcome that. The danger is that weak claims
can look polished. The response is not to pretend that nothing has changed, but
to make explicit what is being trusted. The appropriate evidence depends on the
problem: it may be an interval certificate, a convergence study, a conditioning or
uncertainty analysis, comparison with experiment, or an independent implementation.
The point applies well beyond the eigenvalue and resonance certificates studied here.
As generation becomes cheaper, verification, interpretation, responsible attribution,
and human judgment become more, not less, central to numerical analysis.

    AI Declaration and Code Availability. ChatGPT 5.5 with Codex was used
in May 2026 as an exploratory research assistant as described in the text. The
use of AI in the paper is limited to the displayed response boxes and some of the
code in the repository. All code is available at https://github.com/MColbrook/
ai-assisted-eigenvalue-certificates. I have tested the code independently, and checked
and corrected it line by line. I assume responsibility for all content.

                                         REFERENCES

 [1] A. A. Abramov, A. Aslanyan, and E. B. Davies. Bounds on complex eigenvalues and resonances.
          Journal of Physics A: Mathematical and General, 34(1):57–72, 2001.
 [2] J. Aguilar and J.-M. Combes. A class of analytic perturbations for one-body Schrödinger
          Hamiltonians. Communications in Mathematical Physics, 22(4):269–279, 1971.
 [3] J. Alper, M. Barany, A. Chavarri Villarello, S. Dahmen, W. Dean, K. Ganapathy, M. Harris,
          D. Holmes, M. Jamnik, S. Kelk, B. Kra, U. Martin, B. Naskrecki, R. Ochigame, J. Portegies,
          and J. Schmitt. Leiden declaration on artificial intelligence and mathematics, 2026.
 [4] J. J. Balmer. Notiz über die Spectrallinien des Wasserstoffs. Annalen der Physik und Chemie,
          261(5):80–87, 1885.
 [5] J. Behrndt, P. Schmitz, G. Teschl, and C. Trunk. Relative oscillation theory and essential
          spectra of Sturm–Liouville operators. Journal of Mathematical Analysis and Applications,
          518(1):126673, 2023.
26                                      M. J. COLBROOK


 [6] S. Bögli, B. M. Brown, M. Marletta, C. Tretter, and M. Wagenhofer. Guaranteed resonance
         enclosures and exclosures for atoms and molecules. Proceedings of the Royal Society A:
         Mathematical, Physical and Engineering Sciences, 470(2171):20140488, 2014.
 [7] N. Bohr. I. On the constitution of atoms and molecules. The London, Edinburgh, and Dublin
         Philosophical Magazine and Journal of Science, 26(151):1–25, 1913.
 [8] B. M. Brown, M. Langer, M. Marletta, C. Tretter, and M. Wagenhofer. Eigenvalue bounds
         for the singular Sturm–Liouville problem with a complex potential. Journal of Physics A:
         Mathematical and General, 36(13):3773–3787, 2003.
 [9] M. J. Colbrook. Infinite-Dimensional Spectral Computations: Foundations, Algorithms, and
         Modern Applications. Cambridge University Press, Cambridge, 2026.
[10] K. M. Collins, A. Q. Jiang, S. Frieder, L. Wong, M. Zilka, U. Bhatt, T. Lukasiewicz, Y. Wu,
         J. B. Tenenbaum, W. Hart, et al. Evaluating language models for mathematics through
         interactions. Proceedings of the National Academy of Sciences, 121(24):e2318124121, 2024.
[11] T. A. Driscoll, N. Hale, and L. N. Trefethen. Chebfun Guide. Pafnuty Publications, Oxford,
         2014.
[12] S. Dyatlov and M. Zworski. Mathematical Theory of Scattering Resonances, volume 200 of
         Graduate Studies in Mathematics. American Mathematical Society, 2019.
[13] F. Gesztesy, B. Simon, and G. Teschl. Zeros of the Wronskian and renormalized oscillation
         theory. American Journal of Mathematics, 118(3):571–594, 1996.
[14] T. Hubert, R. Mehta, L. Sartran, M. Z. Horváth, G. Žužić, E. Wieser, A. Huang, J. Schrit-
         twieser, Y. Schroecker, H. Masoom, et al. Olympiad-level formal mathematical reasoning
         with reinforcement learning. Nature, pages 1–3, 2025.
[15] F. Johansson. Arb: Efficient arbitrary-precision midpoint-radius interval arithmetic. IEEE
         Transactions on Computers, 66(8):1281–1292, 2017.
[16] R. Krawczyk. Newton-Algorithmen zur Bestimmung von Nullstellen mit Fehlerschranken. Com-
         puting, 4(3):187–201, 1969.
[17] R. J. Lohner. Enclosing the solutions of ordinary initial and boundary value problems. In Com-
         puter Arithmetic: Scientific Computation and Programming Languages. B. G. Teubner,
         Stuttgart, 1987.
[18] R. E. Moore, R. B. Kearfott, and M. J. Cloud. Introduction to Interval Analysis. SIAM,
         Philadelphia, 2009.
[19] A. Neumaier. Interval Methods for Systems of Equations. Cambridge University Press, Cam-
         bridge, 1990.
[20] F. W. J. Olver, D. W. Lozier, R. F. Boisvert, and C. W. Clark, editors. NIST Handbook of
         Mathematical Functions. Cambridge University Press, 2010.
[21] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J.
         Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi, et al. Mathematical discoveries from program
         search with large language models. Nature, 625(7995):468–475, 2024.
[22] S. M. Rump. Verification methods: Rigorous results using floating-point arithmetic. Acta
         Numerica, 19:287–449, 2010.
[23] J. R. Rydberg. Recherches sur la constitution des spectres d’émission des éléments chimiques.
         Kungliga Vetenskapsakademiens handlingar, 23(11):1–155, 1890.
[24] E. Schrödinger. Quantisierung als Eigenwertproblem. Annalen der Physik, 384(4):361–376,
         1926.
[25] B. Simon. Resonances and complex scaling: A rigorous overview. International Journal of
         Quantum Chemistry, 14(4):529–542, 1978.
[26] G. Temple. The theory of Rayleigh’s principle as applied to continuous systems. Proceedings
         of the Royal Society of London, 119(782):276–293, 1928.
[27] G. Teschl. Mathematical Methods in Quantum Mechanics: With Applications to Schrödinger
         Operators, volume 157 of Graduate Studies in Mathematics. American Mathematical So-
         ciety, Providence, RI, 2 edition, 2014.
[28] W. Tucker. Validated Numerics: A Short Introduction to Rigorous Computations. Princeton
         University Press, Princeton, NJ, 2011.
[29] M. Zworski. Mathematical study of scattering resonances. Bulletin of Mathematical Sciences,
         7(1):1–85, 2017.
