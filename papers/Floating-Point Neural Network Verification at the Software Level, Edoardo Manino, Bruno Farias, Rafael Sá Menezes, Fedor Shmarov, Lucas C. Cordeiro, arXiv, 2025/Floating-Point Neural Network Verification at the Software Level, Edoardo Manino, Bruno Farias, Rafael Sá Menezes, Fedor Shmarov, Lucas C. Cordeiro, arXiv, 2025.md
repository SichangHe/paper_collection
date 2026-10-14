                                         Floating-Point Neural Network Verification at the
                                                          Software Level

                                                Edoardo Manino1*, Bruno Farias1 , Rafael Sá Menezes1 ,
                                                        Fedor Shmarov2 , Lucas C. Cordeiro1,3
                                           1*
                                              Department of Computer Science, The University of Manchester,
                                                         Oxford Road, Manchester, M13 9PL, UK.
                                              2
                                                School of Computing, Newcastle University, 1 Science Square,
                                                           Newcastle upon Tyne, NE4 5TG, UK.
                                         3
                                           Faculty of Electrical and Computer Engineering, Universidade Federal
                                            do Amazonas, Avenida Rodrigo Otávio, Manaus, 69080-900, Brazil.
arXiv:2510.23389v2 [cs.SE] 10 Aug 2026




                                                          *Corresponding author(s). E-mail(s):
                                                           edoardo.manino@manchester.ac.uk;
                                                  Contributing authors: bruno.farias@manchester.ac.uk;
                                          rafael.menezes-2@manchester.ac.uk; fedor.shmarov@newcastle.ac.uk;
                                                            lucas.cordeiro@manchester.ac.uk;


                                                                                Abstract
                                           The software implementation of neural networks must be proven correct before
                                           deployment in safety-critical systems. To this end, software verification may
                                           seem an attractive solution, as automated verification tools can reason about the
                                           behaviour of floating-point arithmetic and other typical low-level implementation
                                           details of neural network code. In this paper, we conduct the first rigorous eval-
                                           uation of eight state-of-the-art automated software verifiers on neural network
                                           code. In doing so, we construct NeuroCodeBench 2.0, a benchmark comprising
                                           912 neural network verification examples that cover activation functions, com-
                                           mon layers, and full neural networks of up to 170K parameters. We demonstrate
                                           that the obtained results are rather underwhelming: existing verifiers often return
                                           incorrect results, cannot reliably check more than a single neural layer at a time,
                                           and do not fully support the standard math library. To compensate for the lat-
                                           ter, we supply the verifiers with explicit implementations of required functions
                                           (e.g. TanH), which leads to no visible improvements. Overall, our study demon-
                                           strates that the existing state-of-the-art software verifiers are not ready to handle




                                                                                    1
     verification of neural networks at software level. However, a historical analy-
     sis of the progress of verifiers over the years show non-monotonic but constant
     improvements.

     Keywords: AI Safety, Software Verification, Neural Networks, Floating Point




1 Introduction
In the past years, there have been growing concerns on the reliability of AI systems
and the associated risks [1]. Indeed, AI systems are known to perform exceptionally
well on existing benchmarks while still producing an unacceptable rate of incorrect and
unsafe predictions in real-world settings [2, 3]. Moreover, targeted adversarial attacks
are known to arbitrarily degrade the performance of AI systems at inference time [4].
While inventing better techniques to benchmark, test [5], and improve the reliability of
AI systems is an active area of research, an overarching solution is still missing [6–8].
    In this regard, neural network verification is emerging as one of the most principled
approaches to assess the AI systems’ reliability, as it can provide formal guarantees
on the behaviour of neural networks [9]. In a nutshell, the verification approach takes
a neural network model f , a safety property P in a suitable formal language, and
automatically verifies whether f satisfies P for all possible inputs. For some especially
desirable properties, such as robustness to adversarial perturbations of the input [4],
state-of-the-art verifiers can scale to neural networks with more than 1M neurons [10].
Furthermore, research on extending these verification tools to hyper-properties [11, 12],
language models [13, 14], and cyber-physical systems [15, 16] is well under way.
    At the same time, idealised neural networks models and common neural exchange
formats hide most of the implementation details of the final AI system, including
floating-point types and numerical optimisations [17]. Such a level of abstraction is not
acceptable in safety-critical applications (CPS, IoT), where guarantees of the imple-
mentation’s correctness are needed [18]. Indeed, type conversion errors in software
implementation have caused real-world accidents in the past, ranging from the loss of
a $370 million US dollar space rocket in flight [19] to the death of military personnel
due to a faulty air-defence missile [20].
    A simple example of the numerical issues that may arise in floating-point com-
putation is presented in Figure 1. There, we can see that the SoftSign activation, a
common replacement for more computationally expensive sigmoid functions, ceases
to be a non-decreasing function once it is implemented in 32-bit IEEE 754 floating
point. Establishing whether small numerical errors can cascade into larger vulner-
abilities requires reasoning about the software implementation of the entire neural
network [21]. In contrast, existing real-valued verification workflows will hide the issue
until a numerically-aware adversary exploits it [22, 23].
    In principle, software verification can ensure a system’s safety at the implemen-
tation level. In fact, verification tools are routinely employed to identify bugs in
industrial-scale code or prove their absence [24, 25]. Unfortunately, existing attempts
to employ software verifiers on neural network code have yielded mixed results. On the


                                             2
                   1          x
                        y = 1+|x|

                 0.5                                      0.93750012

                                                          0.93750006
                   0



            y
                                                          0.93750000
                −0.5
                                                          0.93749994




                                                                   14.99998

                                                                              14.99999

                                                                                         15.00000

                                                                                                    15.00001

                                                                                                               15.00002
                 −1
                  −16 −12 −8   −4   0   4   8   12   16
                                    x

Fig. 1: The SoftSign activation is a non-decreasing function in infinite precision (left)
but not when implemented in 32-bit IEEE 754 floating-point arithmetic (right).


one hand, software verifiers do not scale well to large neural network instances, forcing
practitioners to switch to unsound infinite-precision models [26] or abandoning verifi-
cation in favour of pure testing approaches [27]. On the other hand, software verifiers
appear to produce a high rate of incorrect results in some settings [28], casting doubt
on their role as a safety oracle. Although the latter is a known phenomenon in gen-
eral software verification tasks [29–31], more work is needed to establish the current
capabilities of software verifiers for neural network code and to steer the verification
community towards a clear path for improvement.
    In this paper, we present the first rigorous study on the verification of floating-point
neural network code with automated software verification tools. Our main goal is to
validate the claim that these tools support the verification of floating-point code [32],
and reproduce earlier works that suggest that this claim does not extend to neural
network implementations [27, 28]. To this end, we make the following contributions to
the state of the art:
• We construct the NeuroCodeBench 2.0 benchmark to be a common ground for com-
  parison across tools. NeuroCodeBench 2.0 contains 912 snippets of code of varying
  size: from individual activation functions and neural layers to whole end-to-end
  neural networks. Furthermore, we augment each benchmark instance with safety
  specifications in the form of reachability properties; we make sure that the expected
  verdicts (safe or unsafe) are known in advance via a combination of techniques (e.g.,
  by construction, exhaustive testing). NeuroCodeBench 2.0 is a substantial improve-
  ment over our previous short report [28], we list all the differences in Appendix
  B.
• We make NeuroCodeBench 2.0 compatible with most verification tools by produc-
  ing fully contained C files that include the model implementation, safety property,
  required libraries, and system dependencies. In this way, we can rely on the
  same infrastructure as the International Competition on Software Verification (SV-
  COMP)        [32] and guarantee a highly reliable, reproducible workflow via the
  BenchExec framework [33]. Furthermore, our efforts led to NeuroCodeBench 2.0
  becoming part of the official benchmark set of SV-COMP since the 2026 edition.
• We compare the performance of eight state-of-the-art automated software verifica-
  tion tools from the perspective of an expert user. Accordingly, we take great care


                                                     3
  to run the tools with the same settings their authors chose for the 2024 edition of
  SV-COMP. Overall, we demonstrate that the tools exhibit a large variance across
  the NeuroCodeBench 2.0 benchmark, with an average of 11% correct and 3% incor-
  rect verdicts. When we try to improve their behaviour by providing operational
  models of the C mathematical library in a separate experiment, we show that the
  performance improvements are minor.
• We show how the release of NeuroCodeBench 1.0, an earlier version of our bench-
  mark, has had a dramatically positive impact on the performance of most tools
  between 2023 and 2024. At the same time, the introduction of NeuroCodeBench 2.0
  in late 2025 demonstrated a more moderate effect on the state-of-the-art software
  verifiers. Moreover, we investigate the historical progress of the field by compar-
  ing earlier versions of one of the tools (i.e., ESBMC) since 2018; our experiments
  demonstrate a non-monotonic pattern in its performance over the years.
    In more detail, this paper is structured as follows. In Section 2, we introduce neu-
ral network verification more formally and list the subtle differences introduced by
software implementations, floating-point types, and mathematical libraries. In Section
3, we present every step of our benchmark design, from initial requirements to the
construction of each of its nine benchmark categories. In Section 4, we discuss our pro-
cess to make NeuroCodeBench 2.0 compatible with the SV-COMP infrastructure. In
Section 5, we present the results of our experiments, which include running all verifi-
cation tools on the plain NeuroCodeBench 2.0 benchmark and adding the operational
models of the math.h library, and evaluating the historical progress of the tools. In
Section 6, we draw our conclusions and propose a few suggestions on how to improve
the effectiveness of automated software verifiers for the analysis of neural network
code.

2 Background
2.1 Neural Networks
In machine learning, a neural network is defined as a function f : Rn0 → RnL between
two real vector spaces of dimensions n0 and nL respectively [34]. Crucially, mod-
ern neural network architectures construct f by composing together a sequence of L
simpler functions ℓi : Rni−1 → Rni , called layers:

                              f = ℓ1 ◦ ℓ2 ◦ · · · ◦ ℓL−1 ◦ ℓL                        (1)

Common layers include affine transformations
                                                such as ℓi (x) = Ax + b or element-wise
activation functions such as ℓi (x) j = tanh xj . We give a more comprehensive list of
neural network layers and activation functions in Sections 3.3 and 3.4.
    Typically, we optimise the values of layer parameters against a large training set of
input-output pairs, until the network reaches the desired accuracy. In some cases, the
choice of layer types, layer dimensions ni , and activation functions themselves is the
result of an automated process called neural architecture search [35]. These optimisa-
tion processes are governed by a complex set of heuristics, whose hyper-parameters are


                                            4
tuned by trial-and-error to maximise the efficiency of training [36]. In this paper, we
assume that training has already finished and we look at the behaviour of the trained
neural network f .

2.2 Neural Network Verification
While the machine learning process is undoubtedly effective, with state-of-the-art neu-
ral networks achieving better than human accuracy in many tasks, it offers no formal
guarantees on the correctness of the resulting behaviour. Neural network verification
aims to rectify the problem by reasoning over a trained network to prove whether
it satisfies certain functional properties [9]. More specifically, safety properties over
neural networks are usually defined in the following form:

                               x ∈ Din =⇒ f (x) ∈ Dout                                (2)

where x ∈ Din is the pre-condition and f (x) ∈ Dout is the post-condition in computer
programming parlance. Perhaps the most famous example of safety property is adver-
sarial robustness [4], which requires a neural network to compute the same output
class for all possible perturbations of magnitude ϵ around a given input c:
                                                        
                 ||x − c|| ≤ ϵ =⇒ arg max f (x) = arg max f (c)                       (3)

where the arg max operator selects the highest scoring out of nL output classes. In
NeuroCodeBench , all safety properties are in the form of Equation 2.
    Given a neural network f and a safety property P , it remains to check whether
P holds for f . Unfortunately, this decision problem is quite hard to solve. For the
most popular networks architectures f and safety properties P , complete decision
procedures fall into the NP-complete complexity class [9]. Furthermore, the worst-
case theoretical complexity depends on the number of non-linearities in the network
f , which correlates with the dimension of the activation layers. In practice, scaling to
neural networks containing more than a few million neurons remains a challenge [10].
    State-of-the-art verification tools use several strategies to solve the aforementioned
decision problem. They include convex relaxations of the associated satisfiability prob-
lem [37], custom SMT solvers [38], and over-approximation via abstract domains [39].
Currently, the most effective approaches combine branch and bound search with opti-
misable linear abstraction bounds [40, 41]. Since 2020, the international Verification
of Neural Networks Competition (VNN-COMP) provides a forum for tool authors
to compare progress [10]. NeuroCodeBench contains two categories derived from
VNN-COMP benchmarks (see Section 3.9).

2.3 Floating-Point Arithmetic
Although most of the machine learning literature defines neural networks as func-
tions over real vector spaces f : Rn0 → RnL , the actual computation is run on
digital hardware, which can only support finite-precision arithmetic. In this respect,



                                            5
the default numerical type of mainstream machine learning libraries such as Pytorch1
and Tensorflow2 is typically the 32-bit IEEE 754 floating-point format [42]. Further-
more, specialised hardware accelerators may favour even shorter types ranging from
Google’s 16-bit BFloat16 [43] to Nvidia’s, ARM’s and Intel’s 8-bit FP8 format [44].
    Compared to real-valued arithmetic, floating-point types introduce a small amount
of rounding error after each operation. As a direct consequence, basic arithmetic oper-
ations in floating point are not associative [45], i.e., we have that (a + b)+ c ̸= a +(b + c).
When executing computationally intensive algorithms, such as convolutions via the
Winograd [46] or Fast Fourier Transforms [47], the floating-point deviations com-
pound and lead to different outputs depending on the specific numerical optimisations
used [17]. In neural networks, these numerical discrepancies are large enough to inval-
idate many of the safety proofs produced by the neural network verifiers we mention
in Section 2.2 [22, 23].
    As a result, there have been calls to verify neural networks at the implementa-
tion level [21]. That way, we can ensure that the required safety properties hold for
the digital artefact fˆ : Fn0 → FnL that is executed, rather than its real-valued coun-
terpart f : Rn0 → RnL . Unfortunately, neural network exchange formats such as
ONNX3 do not contain enough implementation details to aid verification at this level
of abstraction [48]. Instead, the few existing studies attempt to specify the details of
the neural network implementation at the software level, usually in the C program-
ming language [26–28]. This process essentially turns neural network verification into
a software verification problem.

2.4 Software Verification
From a high-level perspective, software verification (SV) solves a problem similar to
that of neural network verification (VNN) described in Section 2.2. That is, given a
program S and a safety property P , a software verifier tries to decide whether P holds
for all inputs to S (i.e., S is safe with respect to P ) or not.4 If the latter is the case,
then the verifier provides a counter-example: a series of input values and assignments
that lead to a bug (i.e., safety property violation) in the given program S . However,
there are two crucial differences between SV and VNN:
• Software verifiers need to reason over finite domains (i.e., float’s, int’s, etc.),
  and therefore, must adhere to the semantics of arithmetic operations over the
  corresponding domains.
• Software verifiers need to make necessary assumptions about the underlying memory
  model (i.e., how the memory is allocated, accessed, and freed) and computational
  models of external libraries (e.g., implementations of stdlib.h, math.h, etc.).
   In verifying C programs, safety properties are often encoded as assertions. Figure 2
contains a code listing with an implementation of the SoftSign function and the
monotonicity property ∀x1 , x2 : x2 ≥ x1 ⇒ Sof tSign(x2 ) ≥ Sof tSign(x1 ). As

  1
    https://pytorch.org
  2
    https://www.tensorflow.org
  3
    https://onnx.ai/
  4
    Note that software verification is undecidable in general [49]. However, we ensure that our benchmarks
are always decidable.


                                                    6
    float softsign(float x) { return x / (fabsf(x) + 1.0f); } // SoftSign implementation

    int main()
    {
        float x1, x2; // some arbitrary float values
        if(!isnan(x1) && !isnan(x2) && !isinf(x1) && !isinf(x2)) { //avoid special values
            if(x2 >= x1) assert(softsign(x2) >= softsign(x1)); // monotonicity property
        }
        return 0;
    }


Fig. 2: Example implementation of SoftSign function from Figure 1 together with the
monotonicity property that should hold for all values of x1 and x2 within the numerical
limits of the float type. The code is adapted from the file ”softsign 2 unsafe.c”
of NeuroCodeBench 2.0.


Figure 1 illustrates, the property holds for all x1 , x2 ∈ R but not when x1 , x2 ∈ F.
As a consequence, verification of this program will result in an assertion violation.
A possible counter-example is x1 = 15.0f and x2 = 15.00000286102294921875f,
since softsign(15.0f) = 0.9375 and softsign(15.00000286102294921875f) =
0.937499940395355224609375.
    There are a myriad of different software verification techniques. Brain et. al. [50]
identify six main paradigms: static analysis, abstract interpretation, testing & sym-
bolic execution, model checking, deductive verification, and functional verification.
Many state-of-the-art automated software verifiers (e.g., CBMC [51], ESBMC [52],
CPAChecker [53], KLEE [54]), cleverly combine different verification techniques across
these paradigms. Dozens of such tools participate in SV-COMP [32] – the largest
annual software verification competition – where they compete in finding bugs (i.e.,
user-specified assertion violations, buffer overflows, arithmetic overflows, pointer bugs,
etc.) in tens of thousands of C programs ranging from simple unit tests to device
drivers.
    For neural network verification, working at the software level introduces addi-
tional scalability issues. The comparison between neural network verifiers and software
verifiers in [26] clearly shows a higher timeout rate for the latter. Moreover, the
authors of [27] observe that software verifiers cannot prove the equivalence of differ-
ent matrix multiplication algorithms beyond three-dimensional input tensors of size
10 × 10 × 10. Our results in Section 5.4 confirm that software verifiers struggle with
larger benchmark instances.

2.5 Correctly-Rounded Mathematical Libraries
While software verifiers allow us to reason about floating-point programs, they still
rely on assumptions about the semantics of external libraries. In this respect, neural
networks often depend on elementary mathematical functions in their implementation
of activation functions and network layers, as we show in Sections 3.2 and 3.3. For C
programs, the function definitions are provided by the standard library math.h, but



                                             7
their behaviour is implementation dependent (see Appendix A). This lack of portabil-
ity can become an issue for software verifiers, as they typically need a non-ambiguous
specification to correctly reason about the program safety [55].
    A principled solution to the ambiguity in floating-point semantics is to provide a
reference implementation of the functions in math.h. In this regard, there is a long his-
tory of designing explicit approximation algorithms for elementary functions, including
CORDIC [56], BKM [57], and the onion peeling strategy [58]. Over the years, these
algorithms have been integrated in the standard mathematical library in conjunction
with dedicated hardware primitives for efficiency reasons.5 In this paper, we consider
the following two state-of-the-art implementations of math.h:
• MUSL. This mathematical library is based on the well-established numerical algo-
  rithms of FDLIBM [59]. While the functions it provides are not always correctly
  rounded, the documentation6 states that sqrtf is guaranteed to give correctly
  rounded results and that “other functions should have small ulp error in nearest
  rounding mode and the sign of zero should be correct”. Furthermore, the MUSL
  library is already used by the software verifier ESBMC for some of its math.h
  operational models [52].
• CORE-MATH. This mathematical library is an evolution of CR-LIBM [60], a long-
  standing effort to provide correctly rounded functions [61]. Crucially, the numerical
  algorithms it uses have been formally verified [62, 63]. Unfortunately, the library
  does not provide a square root function, and some trigonometric functions (cosf,
  sinf) use 128-bit arithmetic, which most software verifiers do not support.7
In Section 5.3, we include the MUSL and CORE-MATH numerical algorithms in
our benchmark instances, and measure their impact on the performance of existing
software verifiers.

3 Benchmark Design
In this section, we present NeuroCodeBench 2.0, our benchmark of neural network
code for software verification. First, we list the design requirements that guided our
benchmark-building process. Then we provide details on how we built each benchmark
category. Table 1 provides an overview of the structure of NeuroCodeBench 2.0.

3.1 Design Requirements
We design NeuroCodeBench with two broad goals in mind: to create a rigorous mea-
surement tool and to stimulate further research on the topic. On the one hand, previous
research shows that software verifiers struggle to reason on neural network code [27]
and sometimes produce incorrect results [28]. As such, having access to an exten-
sive benchmark of neural network code allows a fair assessment of the performance
of state-of-the-art software verification tools. On the other hand, there exist a consid-
erable scalability gap between bit-precise software verification and infinite-precision

 5
     For an example, see NewLib at https://sourceware.org/newlib/
 6
     https://wiki.musl-libc.org/mathematical-library.html
 7
     See code at https://core-math.gitlabpages.inria.fr/



                                                   8
             Table 1: Overview of NeuroCodeBench 2.0. The “Unsafe” column
             comprises all properties for which a counterexample exists. The
             “Ground Truth” column reports the source of our verdicts. We
             highlight differences with NeuroCodeBench 1.0 as new for new
             categories, and more for expanded ones.
               Benchmark Category                   Safe   Unsafe   Ground Truth

               Maths Functions more                 42     16       Brute Force
               Activation Functions more            44     13       Brute Force
               Neural Layers new                    43     43       By Construction
               Hopfield Networks                    46     34       By Construction
               SAT ReLU Networks new                48     48       By Construction
               Polynomial Approximation             48     48       Brute Force
               Lipschitz-Bounded Networks new       54     54       By Construction
               Probability Density                  22     13       Counterexamples
               Reinforcement Learning               103    193      Counterexamples

               Total                                450    462



neural network verifiers [26]. While there are indications that the latter might be solv-
ing a fundamentally easier computational problem [64], further research on reducing
the empirical gap between the two requires practical means to measure progress.
    Against this background, we design NeuroCodeBench with the following three
features in mind:
• Ground Truth. Software verification benchmarks contain assertions over program
  variables (see Section 2.4). In NeuroCodeBench , we know a priori which assertions
  hold and which do not, thus making the program safe and unsafe, respectively.
  Furthermore, we maintain a balance between safe and unsafe verdicts to discourage
  guessing the answer. As a result, our benchmark can serve as a rigorous measurement
  tool for the correctness of existing software verifiers. In the remainder of Section
  3, we give details on the specific techniques we use to establish the ground-truth
  verdicts.
• Complexity Range. The scalability of software verifiers is significantly worse than
  their infinite-precision counterparts [26]. To stimulate further research, we include
  a wide range of program instances in NeuroCodeBench , ranging from very simple
  mathematical functions to full neural networks. In this way, any improvement in
  software verification techniques, however small, has a chance to solve a noticeable
  number of additional instances. We have already seen the positive effects of this
  incremental reward structure during the 2023 edition of SV-COMP, see Section 5.5
  for details.
• Programming Language. Mainstream machine learning libraries such as PyTorch8
  and Tensorflow9 exhibit inconsistent behaviour across computing platforms [17]. To

 8
     https://pytorch.org/
 9
     https://www.tensorflow.org




                                                9
                     Table 2: Safety properties of mathematical func-
                     tions. Only 42 out of 58 instances hold.




                                                                 expm1f new



                                                                                     log1pf new



                                                                                                         sqrtf
                                           cosf

                                                  erff

                                                          expf



                                                                              logf



                                                                                                  sinf
                       Properties

                       Domain              -      -        -          -        1          1       -       1
                       Linear Bound        2      2        2          2        1          1       2       2
                       Monotonicity        -      1        1          1        1          1       -       1
                       Periodicity         1      -        -          -        -          -       1       -
                       Finite Difference   2      2        2          2        2          2       2       2
                       Inverse Function    2      -        2          2        2          2       2       2
                       Symmetry            1      1        -          -        -          -       1       -

                       Total               8      6        7          7        7          7       8       8



  avoid the issue, we adopt two microcontroller libraries which convert high-level neu-
  ral network specifications to standalone artifacts in plain C: onnx2c10 and keras2c11 .
  Producing benchmarks in plain C has the additional benefit of being compatible
  with a large number of existing software verifiers [32]. Furthermore, microcontroller
  platforms are the natural target for a wide range of TinyML and IoT applications,
  where small neural network models are the norm [65, 66].

3.2 Maths Library
Typically, neural network code relies on 32-bit floating-point arithmetic (see Section
2.3). In many cases, the code invokes the standard library math.h to perform specific
mathematical operations. In particular, this is true for a majority of the activation
functions used in neural networks (see Section 3.3), which are defined in terms of expo-
nential, logarithm, and hyperbolic tangent. Similarly, computing Euclidean distances
and vector normalisation require taking the square root [34]. Furthermore, the posi-
tional encodings used in some sequence models [67] and convolution algorithms based
on the Fourier transform [47] depend on the correct implementation of the sine and
cosine functions.
    In this light, we provide 58 benchmark instances that check whether a software
verifier can reason over the mathematical functions in Table 2. In addition to the
functions listed there, our benchmark relies on the following ancillary functions: acosf,
asinf, atanhf, fabsf, fmaxf, isgreater, isgreaterequal, isless, islessequal.
Furthermore, we include the function tanhf under the category of activation functions
(see Section 3.3). We defer a discussion on the inherent ambiguity of writing bit-precise
specifications over math.h functions to Section 2.5.

 10
      https://github.com/kraiskil/onnx2c
 11
      https://github.com/PlasmaControl/keras2c




                                                         10
      1                                          4        ELU
                                                         GELU
                                                       GLU/Swish
                                                 2       ReLU
      0                          Gaussian               SoftPlus
                                 Logistic
                                 Softsign
                                                 0
                                  Step
     −1                           TanH
       −4      −2        0       2          4    −4      −2        0      2       4

            (a) Bounded activations                   (b) Unbounded activations

             Fig. 3: Visual comparison of popular activation functions.


   Overall, our benchmark checks whether the floating-point implementations of
the functions in Table 2 satisfy the fundamental properties of their corresponding
mathematical functions. More specifically, we check for the following properties:
• Domain. Logarithms and square root return NaN for negative inputs.
• Linear Bound. All functions satisfy some linear bounds in the form ±f (x) ≤ ax + b.
  For instance, cos(x) ≤ 1 and exp(x) ≥ x + 1.
• Monotonicity. Most functions are monotonically non-decreasing.
• Periodicity. Sine and cosine have a period of 2π .
• Finite Difference. All functions satisfy some invariants on their derivatives f ′ (x).
                              √
  For instance, erf ′ (x) ≤ 2/ π and exp′ (x) = exp(x).
• Inverse Function. Most functions have a closed-form inverse. For instance,
  arccos(cos(x)) = x and log(exp(x)) = x.
• Symmetry. The error function, sine, and cosine are symmetric around zero. For
  instance, erf(x) = − erf(−x) and cos(x) = cos(−x).
Due to the non-idealities of floating-point representation, many of the mathematical
properties listed above do not always hold (e.g., see Figure 1). For our benchmark, we
derived the ground-truth verdicts in Table 1 by checking each safety property against
all possible 32-bit floating-point inputs.

3.3 Activation Functions
The vast majority of neural network architectures include several activation layers,
where the output of each neuron is passed through a so-called activation function (see
Section 2.1). These functions are highly non-linear and allow modern neural networks
to fit arbitrary datasets [34]. We can classify all activation functions based on the
range of their co-domain: bounded or unbounded (see Figure 3). In our benchmark,
we include the following popular activation functions [68, 69]:
• ELU(x) = {exp(x) − 1 if x < 0, x otherwise}.
• Gaussian(x) = exp(−x2 ). √ 
• GELU(x) = x · 21 1 + erf(x/ 2) .


                                            11
                Table 3: Safety properties of common activation functions.
                Only 44 of our 57 instances hold.




                                            Gaussian new



                                                                       GLU new




                                                                                                                         Step new
                                                                                                   SoftPlus

                                                                                                              SoftSign
                                                                                 Logistic
                                                           GELU




                                                                                            ReLU




                                                                                                                                    TanH
                                      ELU
                  Properties

                  Linear Bound        2            2       3               2        2       2       3            2           2      2
                  Monotonicity        1            -       1               2        1       1       1            1           1      1
                  Finite Difference   2            2       2               -        2       -       2            2           -      2
                  Inverse Function    -            -       -               -        2       -       -            -           -      2
                  Symmetry            -            1       -               2        1       -       -            1           1      1

                  Total               5            5       6               6        8       3       6            6           4      8



• GLU(x, y ) = x·Logistic(y ). Also called Swish when x = y .
                                                  −1
• Logistic(x) = 21 1 + tanh(x/2) = 1 + exp(−x)
                                  
                                                      . Also called Sigmoid.
• ReLU(x) = {0 if x < 0, x otherwise} = max(0, x).
• SoftPlus(x) = log(1 + exp(x)).
• SoftSign(x) = x · (1 + |x|)−1 .
• Step(x) = {0 if x < 0, 1 otherwise}.
                                            −1
• TanH(x) = exp(2x) − 1 · exp(2x) + 1
                            
                                                .
    Overall, we write 57 safety properties of activation functions. In a similar fashion to
the mathematical library (see Section 3.2), we exploit several fundamental properties
to construct our benchmark. We list them in Table 3. Note that, differently from the
properties in Table 2, none of the activation functions we consider is periodic or has
a limited input domain.

3.4 Neural Layers
One of the design requirements of NeuroCodeBench is that it should contain instances
of progressively increasing difficulty (see Section 3.1). In this respect, previous work
shows that software verifiers struggle to reason about the implementation of simple
linear algebra primitives as soon as their dimension exceeds toy examples [27]. As
neural networks make a heavy use of such primitives, it is worth including them in
our benchmark.
    More specifically, we focus on the basic constituent layers of most neural net-
works [34]. Typically, they fall into the following four subcategories:
• Affine Layers. One of the most computationally intensive operations in neural
  networks are affine transformations, i.e., they map an input tensor x to an out-
  put y = Ax + b [70]. Here, we include a so-called Linear layer,12 where Ax is a

 12
      https://pytorch.org/docs/stable/generated/torch.nn.Linear.html



                                                                  12
                       Table 4: Safety properties of basic neural layers.
                       Only 43 out of 86 instances hold.




                                                         BatchNorm new




                                                                                           LayerNorm new




                                                                                                                        MaxPool new
                                           AvgPool new




                                                                              Conv1D new




                                                                                                           Linear new




                                                                                                                                      SoftMax
                         Properties

                         Linear Bound      11                   -                   -             -              -      11             6
                         Monotonicity       3                   4                   -             8              -       3             4
                         Symmetry           -                   8                   4             -              4       -             -
                         Identity           -                   -                   4             -              8       -             -
                         Output Norm        -                   -                   -             4              -       -             4

                         Total             14            12                         8      12              12           14            14



  dense matrix-vector multiplication, and a simplified version of a one-dimensional
  convolutional layer,13 where A is sparse.
• Normalisation Layers. The learning dynamics of gradient descent can be greatly
  improved by normalising the tensors in the hidden layers of a neural network [71].
  Batch normalisation [72] achieves this by rescaling all tensors in a training batch to
  have zero mean and unitary standard deviation. Layer normalisation [73] achieves
  the same result by computing the mean and standard deviation across an individual
  tensor, rather than a whole batch. Both normalisation layers rely on computing a
  square root.
• Pooling Layers. Mostly used in convolutional neural networks, pooling layers down-
  sample an input tensor to a lower-dimensional one [74]. The downsampling is
  controlled by setting a window size w and stride s. For one-dimensional tensors, pool-
  ing is defined as yi = Pool(x(i−1)s , . . . , x(i−1)s+w−1 ), where MaxPool and AvgPool
  return the maximum and average value, respectively.
• SoftMax Layer. Defined as SoftMax(x) = exp(x)/ di exp(xi ),14 it takes an arbi-
                                                            P
  trary input vector x ∈ Fd and maps it to a valid probability distribution [34]. The
  presence of element-wise exponentials makes it challenging for software verifiers.
   As Table 4 shows, we write 86 safety properties across the seven neural layers. We
keep the layer size small (d ∈ [2, 10]) to provide a moderate increase in verification
complexity with respect to the individual functions in Sections 3.2 and 3.3. In contrast
with the categories therein, we take advantage of the additional properties of identity
(Ax = x when A = I is the identity matrix) and of the fact that the outputs of
LayerNorm and SoftMax should have norm one.

 13
      https://pytorch.org/docs/stable/generated/torch.nn.Conv1d.html
 14
      For simplicity, we omit the temperature τ from our implementation.




                                                                         13
3.5 Hopfield Networks
Hopfield networks are known for their use as error-correcting decoders [75]. From a
practical perspective, the Hopfield neural architecture takes an input vector of d sign
bits x ∈ {±1}d , and produces an output y ∈ {±1}d of the same type and size. Modern
variants of Hopfield networks can memorise a large number of vectors during training,
and correct any entries in the input vector that had their sign flipped [76]. We give a
visual example of the computation required to do so in Figure 4.
    For NeuroCodeBench , we adopt a simplified Hopfield architecture based on Heb-
bian weights, which does not require training [75]. Specifically, we construct our models
to reconstruct the individual input vector x∗ = 1, whose entries are all unitary.
Furthermore, we encode our Hopfield networks in the following recurrent form:

                                  yt+1 = σ (U yt + V xt + b)                                 (4)

where the input matrix is the identity V = I , the kernel (state) matrix has all unitary
entries U = 11T , the bias is b = 0, the initial state is y0 = 0 and the input is non-
zero at the initial step only xt≥1 = 0. Traditionally, Hopfield networks use the Step
activation function σ . For compatibility with keras2c [77], we replace it with either the
SoftSign or the TanH activation instead. Overall, we construct 40 different Hopfield
network by varying the activation function σ ∈ {SoftSign,TanH}, the input vector size
d ∈ {4, 8, 16, 32, 64} and the number of timesteps t ∈ {1, 2, 3, 4}, as shown in Table 5.
     Finally, we write 80 safety properties by exploiting the fact that the network in
Equation 4 can always reconstruct y = x∗ , given enough timesteps, when at least
d/2 + 1 of the input entries are correct. As such, we always set the first d/2 − 1
entries of x0 to non-deterministic floating-point numbers in [−1, 1]. Thanks to the
monotonicity of the Hopfield model, it is possible to check its worst and best-case
behaviour by testing the two concrete inputs x−                                              +
                                                     0 = (−1, . . . , −1, 1, . . . , 1) and x0 =
(1, . . . , 1) respectively. An example of such analysis for d = 4, t = 4 and σ = SoftSign is
shown in Figure 4. With the technique of propagating x−               +
                                                              0 and x0 through the network
f , we are able to establish provably-correct post-conditions in the form yt ≥ f (x−           0)
and yt ≤ f (x+    0 ).

3.6 SAT ReLU Networks
A classic result on the theoretical complexity of neural network verification states
that it is as hard as solving a 3-SAT problem [9]. In deriving their proof, the authors
introduce several gadgets to embed 3-SAT formulae into ReLU neural networks. Here,
we exploit and extend their theoretical construction to turn arbitrary SAT formulae
into neural network verification benchmarks.
    First, let us establish the following gadgets, which allow us to declare Boolean
variables over the binary set {0, 1} and define the semantics of the operators ¬, ∨,
and ∧:




                                               14
               −1             −0.5             0.5              0.6            0.72              1



                1              0.5             0.5              0.6            0.72              1



                1              0.5             0.5              0.6            0.72              1



                1              0.5             0.5              0.6            0.72              1


Fig. 4: An (unrolled) Hopfield network with SoftSign activations and t = 4 recurrent
steps. The network is able to recover the correct (positive) sign for all output entries,
when a strict majority of the input entries are correct. We omit the final classification
layer (dashed) from our benchmarks.


• Binarisation. Given x ∈ [0, 1], we have x ∈ {0, 1} iff x−ReLU(2x − 1) = 0.15
• Negation. Given x, y ∈ {0, 1}, we have y = ¬x iff y = 1 − x.
• Disjunction. Given xi ∈ {0, 1}, we have y = x1 ∨ · · · ∨ xn iff y = 1 − ReLU(1 −
  Pn
    i=1 xi ).
• Conjunction. Given xi ∈ {0, 1}, we have y = x1 ∧ · · · ∨ xn iff y = ReLU(1 − n +
  Pn
    i=1 xi ).

    Next, we show how to encode an arbitrary SAT formula P in the form of a neural
network (see Figure 5 on the left). Without                     W assume that P is in
                                              V loss of generality,
conjunctive normal form (CNF), i.e., P = i ci where ci = j tj and tj ∈ {xk , ¬xk }.
Additionally, assume for now that xk ∈ {0, 1} for all k . We encode the negation of each
disjunctive clause ci in a separate neuron c̄i of a fully-connected ReLU layer as follows:
                                            
                                            −1 if xk ∈ ci
                                                                                                        X
c̄ = σ (W x + b)         where         Wik = +1 if ¬xk ∈ ci                      and        bi = 1 −             1
                                                                                                       ¬xk ∈ci
                                            
                                              0 otherwise
                                            
                                                                                     (5)
where σ is the ReLU activation function and xk ∈ ci (respectively ¬xk ∈ ci ) if variable
xk (or its negation) appears as a term of clause ci . Given c̄ in Equation 5, we encode
the conjunction of their negated value as y1 = 1 − 1T c̄, where 1T is a row vector with
unitary entries. Note that we omit the ReLU activation from the conjunction gadget
for now.
    Similarly, we can extend our neural network encoding to include the binarisation
gadgets for the input vector x (see Figure 5 on the right). To do so, we introduce the
following fully-connected ReLU layer:
                                                                      
                                                 I                       0
            b = σ (V x + u)    where     V =              and      u=                (6)
                                                2I                      −1

  15
     The authors of [9] propose the alternative condition ReLU(ϵ−x)+ReLU(x−1+ϵ) ≤ ϵ for any arbitrarily
small ϵ (see Appendix I therein). Since said condition is always satisfied for x ∈ [0, 1], it does not ensure that
x ∈ [0, ϵ] ∪ [1 − ϵ, 1] as the authors claim. Our binarisation condition x−ReLU(2x − 1) = 0 solves the issue.



                                                       15
                                        x1 , . . . , x n
              CNF formula                                                   Binarisation

                Negation/Disjunction     Identity                  Double Increase

                        ReLU               ReLU                         ReLU

                     Conjunction                           Difference

                            y1                                y2

         Fig. 5: Details of the SAT ReLU network architecture (a sketch).


where σ is the ReLU activation function, I is the identity matrix and 0, 1 are column
vectors with zero-valued and unitary entries, respectively. Note that the presence of
the ReLU activation is only necessary for half of the binarisation gadget, but we keep
it for the whole layer for reason of simplicity. Given b in Equation 6, we encode the
result of the binarisation gadget as y2 = [1T − 1T ]b.
    Finally, we can express the SAT problem associated to any arbitrary CNF formula
P as a safety property over its equivalent ReLU neural network. Specifically, P is
satisfiable if and only if there exists some x ∈ [0, 1]n such that y1 = 1 and y2 = 0. The
former post-condition (y1 = 1) takes the place of the ReLU activation function in the
conjunction gadget, as any input x ∈ {0, 1}n that does not satisfy P will cause y1 ≤ 0.
The latter condition (y2 = 0) ensures that the inputs have been binarised correctly.
    In total, we generate 96 SAT ReLU benchmarks from boolean formulae of different
sizes. We vary the number of input variables in n ∈ {5, 8, 13, 21, 34, 55, 89, 144} and
the number of clauses in |c| = nr with the multiplier r ∈ {1, 2, 3, 4, 5, 6}. On the
one hand, we generate satisfiable formulae by choosing a satisfying assignment, and
then creating |c| random clauses that do not contradict it. On the other hand, we
generate unsatisfiable formulae iteratively: we begin with the contradiction x1 ∧ ¬x1 ,
then we pick an existing clause ci at random and replace it with the two clauses
ci ∨ xk and ci ∨ ¬xk , where xk ̸∈ ci . The size of the corresponding neural network is
n × (|c| + 2n) × 2, where |c| hidden neurons are needed for the disjunction gadgets and
2n for the binarisation ones (see Figure 5).

3.7 Polynomial Approximation Networks
In contrast to the classification problems presented in Sections 3.5 and 3.6, neural
networks are also routinely employed to approximate the behaviour of several physi-
cal and electrical processes by solving the corresponding regression problem (see for
instance [78, 79]). In such applications, we assume that there is an unknown function
g that we wish to approximate with a neural network f , given a limited set of samples
{(x, g (x))i }. Ideally, we would like the approximation f to be as close to the unknown
function g as possible.
    Here, we emulate this process for an arbitrary oscillating polynomial g (x) =
0.125x4 − 0.25x3 − 0.75x2 + x + 0.5 (see Figure 6), from which we extract 100 points by


                                            16
                                                                training data
                                                     1         16×16 network

             −0.5




                                         output y
                            +ϵ
                                                     0
                            −ϵ
              −1

                                                    −1
                −2.2   −2   −1.8 −1.6

                                                         −2        −1   0       1   2   3
                                                                         input x

Fig. 6: Comparison between one of our polynomial approximation networks and its
training data (right). The safety property requires that the output error of the network
does not exceed ϵ in a small input interval (left).


linearly sampling the interval x ∈ [−2, 3]. Then, we train several multilayer perceptrons
f , whose architecture comprises L layers of the following form:

                                        xℓ = σℓ (Wℓ xℓ−1 + bℓ )                             (7)

where ℓ is the layer index, x0 is the network input, xL is the network output, Wℓ is the
weight matrix, bℓ is the bias vector, σℓ is the ReLU activation function when ℓ < L
and the identity function for the last (output) layer. In total, we train 16 multilayer
perceptrons with different number of layers L ∈ {2, 3, 4, 5}, as shown in Table 5.
For each network, we keep the number of neurons d equal for all its hidden layers
ℓ ∈ [1, L − 1], such that xℓ ∈ Fd . We vary d ∈ {4, 8, 16, 32, 64, 128, 256, 512, 1024}, as
long as the total number of neurons does not exceed 256 when L > 2. Figure 6 shows
the behaviour of the L = 3, d = 16 network after training.
    We define our safety properties as follows. First, we formally evaluate the quality of
the approximation f (g ) ≈ g (x) by scanning every possible 32-bit floating-point value
in the training interval x ∈ [−2, 3] ⊂ F. For each network f , we identify the input that
causes the largest difference x∗ = arg maxx |f (x) − g (x)|, and set our pre-condition to
be a small interval around x∗ of size 0.1 (see Figure 6 on the left). Second, we compute
the maximum difference ϵ∗ = max |f (x)−ĝ (x)| against an affine approximation ĝ of the
polynomial g in the small interval around x∗ that satisfies the pre-condition. We use
this information to generate six different post-conditions in the form |f (x) − ĝ (x)| ≤ ϵ
(see Figure 6 on the left): three of them set ϵ < ϵ∗ thus yielding a counterexample,
three of them set ϵ > ϵ∗ thus yielding safe instances. We choose the six values of the
threshold ϵ ∈ {ϵ1 , . . . , ϵ6 } in small increments such that ϵi = 2ϵi−1 . Values of ϵi further
away from the satisfiability threshold ϵ∗ usually yield benchmark instances that are
easier to solve [80]. In Section 5.4.3, we show that the latter is not true for software
verifiers.




                                                              17
                                                                                  1
                                                                                          training data
                                                                                         16×16 network
             1
                                                                                 0.8




                                                                      output y
output y     0
                                                                                 0.6
                                                             2
           −1                                          0
                 −2
                            0                    −2                              0.4
                                           2                                      −1.7    −1.6        −1.5      −1.4   −1.3
                                                           input x2
                      input x1                                                                   inputs x1 ≡ x2

  (a) Training data with two input dimensions                         (b) Lipschitz bounds on the x1 ≡ x2 line

                        Fig. 7: Safety properties of Lipschitz-bounded networks.


3.8 Lipschitz-Bounded Networks
Given the relative fragility of neural networks to small input perturbations [81], the
machine learning community has dedicated considerable effort to quantifying and con-
trolling their effects [82, 83]. One popular approach relies on controlling the Lipschitz
constant c of the whole network f , such that ∥f (x) − f (x′ )∥p ≤ c∥x − x′ ∥p for any
pair of arbitrary inputs x, x′ in some norm p [84, 85]. In this way, any small input
perturbation x′ = x + ϵ cannot cause a large change in the network output.
    Here, we adopt the Lipschitz-bounded network architecture in [85]. It is composed
by residual layers ℓ with the following form:

                                       xℓ = xℓ−1 − 2WℓT D−1 σ (Wℓ xℓ−1 + bℓ )                                           (8)
                                                           Pd
where σ is the ReLU activation function, and D = diag( j=1 |Wℓ WℓT |ij qj /qi ) with a
vector q of additional trainable parameters. Note that residual layers like the one in
Equation 8 require the inputs xℓ−1 ∈ Fd and outputs xℓ ∈ Fd to have the same dimen-
sion d. We can increase d by introducing an additional zero-padding layer and decrease
d by introducing a (normalised) linear projection.16 By construction, Equation 8 has
a Lipschitz constant of c = 1 in Euclidean norm (p = 2) [85].
    To construct our benchmark, we train 18 different Lipschitz-bounded neural
networks with k ∈ {2, 3, 4} inputs and two residual layers of dimension d ∈
{4, 8, 12, 16, 20, 24}. We construct our training set by extracting 65536 samples from
the following oscillating function:
                           k
                           Y
                      y=         g (xi )       where          g (x) = 0.75 cos (0.75x) − 0.5 sin(x)                     (9)
                           i=1

where the inputs are taken uniformly at random from the multi-dimensional interval
x ∈ [−π, π ]k . In Figure 7a, we show a visual representation of Equation 9 for k = 2.

    16
           See the code at https://github.com/araujoalexandre/Lipschitz-SLL-Networks/tree/main/core/models



                                                                 18
    Thanks to the property of Lipschitz-boundedness, we can define safety properties
over the behaviour of each f without the need of the same computationally-expensive
procedure from Section 3.7. More specifically, we restrict our pre-conditions to the
input interval x ∈ [−1.6, −1.4]k , which is centered around a region of maximum slope.
Then, we compute the output of the network at the centroid xc = (−1.5, . . . , −1.5)
which automatically yields the conical-shaped output bounds shown in Figure                √        7. In
fact,
    √  knowing  that   c = 1 for p = 2, we can conclude that f ( x ) ∈ [ f ( x c ) − 0 . 1   k, f ( x c )+
0.1 k ] where 0.1 is the maximum perturbation around the√input xc . With this, we
write three post-conditions in the form f (x) ≤ f (xc ) + 0.1 ks with s ∈ {1, 2, 4} for
each network f .
    To complete our Lipschitz-bounded benchmark, we add a set of violated properties.
We construct these by testing 10M random inputs and establishing a lower bound
on the maximum possible output ŷ ≤ maxx f (x) in the pre-condition interval x ∈
[−1.6, −1.4]k . Then, we write a further three post-conditions in the form f (x) ≤
f (xc ) + (ŷ − f (xc ))/s with s ∈ {1, 2, 4} for each network f . In total, the Lipschitz-
bounded benchmark contains 108 safety properties (see Table 1).

3.9 VNN-COMP Networks
The International Verification of Neural Network Competition (VNN-COMP) provides
an extensive corpus of benchmarks dating back to its inception in 2020 [86]. These
benchmarks use the Open Neural Network eXchange (ONNX) format17 to specify a
neural network’s parameters and architecture. While most VNN-COMP benchmarks
use 32-bit floating point constants, the ONNX format does not necessarily mandate
the specific order of arithmetic operations. As a result, executing the same ONNX
neural network on different software and hardware platforms may yield inconsistent
results [17]. Indeed, the verifiers that compete in VNN-COMP are supposed to reason
on the real-valued behaviour of such neural networks, thus side-stepping the non-
idealities of floating-point arithmetic.
    Here, we propose a straightforward methodology for translating any VNN-COMP
benchmark to a lower-level abstraction defined by C code. We do so in two steps.
First, we provide a reference implementation of an ONNX neural network by running
it through the onnx2c tool.18 Second, we convert the corresponding safety properties
from the original VNN-LIB format19 to a minimal main() function with explicit pre-
and post-conditions on the inputs and outputs of the neural network.
    More concretely, we apply our translation methodology to the two specific cat-
egories listed below, which first appeared in the 2022 edition of VNN-COMP. As
opposed to the majority of the benchmarks therein, the two categories below involve
neural networks of comparable size to the ones in NeuroCodeBench (see Table 5):
• Probability Density. This is a corpus of three neural networks that estimate the
  probability density of the evolution trajectories in various state system [87]: ground
  collision avoidance systems for F-16 aircrafts (GCAS), ground robot navigation

  17
     https://onnx.ai/
  18
     https://github.com/kraiskil/onnx2c
  19
     https://www.vnnlib.org/



                                                   19
      Table 5: Architecture and size of the neural networks in NeuroCodeBench 2.0.
 Subcategory                         Arch.     In        Out     Depth     Width       Act. Fun.    Convert

                                                                                       TanH/
 Hopfield Networks                   Recur.    4–64      4–64    1         4–64                     keras2c
                                                                                       SoftSign
 SAT ReLU Networks new               FC        5–144     2       1         15–1152     ReLU         onnx2c
 Polynomial Approximation            FC        1         1       1–4       4–1024      ReLU         keras2c
 Lipschitz-Bounded Nets new          Resid.    2–4       1       2         4–24        ReLU         onnx2c
 Probability Density                 FC        3–14      3–14    2–3       32–64       ReLU         onnx2c
 Reinforcement Learning              FC        4–8       2–8     2         64–256      ReLU         onnx2c



  (Robot), Van der Pol oscillators (VDP). The corpus is associated with 37 safety
  properties in total, which are derived via reachability techniques.
• Reinforcement Learning. This is a corpus of three neural networks trained to solve
  some reinforcement learning tasks with safety constraints [88]: the cart-pole toy
  control problem, Dubins rejoin manoeuvre in aircraft formation flight, space docking
  manoeuvre for a lunar lander. The corpus is associated with 296 safety properties
  corresponding to the safety constraints the neural networks are trained to satisfy.
    A major downside of our translation methodology is that we lose any soundness
guarantee on the verdict associated to the safety properties. Indeed, by considering
the bit-precise behaviour of a very specific C implementation in 32-bit floating point,
we might be introducing or removing vulnerabilities with respect to the real-valued
version of the benchmark. While we have no option but to trust the safety verdicts
of the real-valued VNN-COMP verifiers, we can at least recover the soundness of the
benchmarks on which they produced a counterexample trace.
    We do so by checking whether each counterexample trace is still causing a violation
on the translated C implementation of the neural network. Throughout this process,
we eliminate 2 out of 208 benchmarks with unsafe verdict. Specifically, we can not
reproduce any of the five counterexamples for property 5 of the Robot subcategory,
and the six counterexamples for property 6 of the VDP subcategory. As such, the
reach prob density category in NeuroCodeBench contains only 35 benchmarks out
of the original 37.

4 Benchmark Format
In this section, we describe how to make a benchmark like NeuroCodeBench 2.0 com-
patible with most existing software verifiers. This is a crucial step of our methodology
because verifiers are highly specialised tools and, as such, can be complex to config-
ure and use correctly without understanding their internal implementation details.
Fortunately, the international software verification competition (SV-COMP) [32] has
already established a common format and verification workflow over the past decade.
Our goal is to match it.20

   20
      An early version of our benchmark, NeuroCodeBench 1.0, is already part of the official benchmark set
of SV-COMP (see Section 5.5 for details).


                                                    20
      float relu(float x) {
        return fmaxf(x, 0.0f); // relu implementation
      }

      int main() {
        float x = __VERIFIER_nondet_float(); // returns a non-deterministic float input
        __VERIFIER_assume(islessequal(x, 0.0f)); // pre-condition (domain restriction)
        float y = relu(x); // computes the output value
        if(y != 0.0); // post-condition (should be zero)
          reach_error(); // error state
        return 0;
      }


Fig. 8: Example of ReachSafety harness. The property requires that applying ReLU
over a non-positive input must return zero.


    In SV-COMP, tools verify C programs against a specification. The specification can
range from memory management to the absence of overflows or simply ensuring that a
specific statement is not reachable.21 The latter category is called ReachSafety in SV-
COMP parlance and includes a large set of verification instances whose goal is to check
that a custom error function (i.e. reach error) is never invoked. A neural network
verification benchmark like NeuroCodeBench 2.0, with its explicit pre-condition and
post-condition structure (see Equation 2), falls into this category.
    Figure 8 contains an example of an SV-COMP harness (a C program with a
property) in the ReachSafety format. Note that the harness includes two auxiliary
intrinsic functions: VERIFIER nondet float() and VERIFIER assume( Bool). The
first constructs a non-deterministic float variable22 , while the second adds a pre-
condition on its value. We explain the role of such intrinsic functions in Section
4.1.1.
    The ReachSafety format we show in Figure 8 has a few advantages over the plain C
format from our introductory example of Figure 2. First, it provides an explicit mech-
anism for specifying pre- and post-conditions via intrinsic functions, thereby removing
semantic ambiguity. Second, it allows us to apply the same evaluation methodol-
ogy used in SV-COMP, including a highly reproducible benchmarking workflow via
the BenchExec framework [33]. Third, it lets us import the verifier settings that the
tool authors have already optimised for competition purposes, thus ensuring a fair
comparison among them.
    The rest of the section lists the requirements of the SV-COMP format (Section
4.1), presents our workflow to convert the benchmark files (Section 4.2), and covers
additional requirements to make NeuroCodeBench 2.0 compatible with BenchExec
(Section 4.3).

 21
      The competition rules are available at https://sv-comp.sosy-lab.org/2025/rules.php.
 22
      In this context, nondeterministic means that it can assume any value representable by the float type.




                                                     21
4.1 SV-COMP Requirements
The verification benchmarks used in SV-COMP must satisfy the following require-
ments:
• No Undefined Behaviour. The benchmarks must not rely on any undefined behaviour
  of the C standard. For example, all variables must be initialized and read and write
  operations must not contain buffer overflows. Furthermore, all functions need to be
  declared and defined, unless they are part of the C standard itself. The only way to
  introduce undefined behaviour is via explicit intrinsic functions (see Section 4.1.1).
• Self-Contained File. In real-world C programs, it is common to split the imple-
  mentation among multiple files and libraries. For SV-COMP purposes, the entire
  program must fit into a single source file. Additionally, only standard C headers are
  allowed for inclusion (e.g. stdlib.h, math.h).
• Explicit Host Configuration. In the C standard, certain implementation details are
  left to the specific system architecture the program is compiled on. In contrast, a
  SV-COMP benchmark should not rely on any implementation of the standard (X86
  vs ARM, Windows vs Linux). If a specific behaviour is required, it needs to be
  explicitly defined in the benchmark.
Among these requirements, the first requires manual inspection, the second can be
automatically checked with a compiler, and the third usually involves running a com-
piler preprocessor in the host system to generate the source file with all the required
characteristics. We present our approach to satisfy them in Section 4.2.

4.1.1 Intrinsic Functions
Some verification benchmarks are designed to reason on the consequences of unde-
fined behaviour. For example, a benchmark might want to use an undefined variable
to simulate an input from the user or a read from a sensor. In order to model these sit-
uations, SV-COMP introduces a number of intrinsic functions. In general, they can be
thought of as extensions to libc that allow us to control the thread scheduling, spec-
ify pre-conditions, and set nondeterministic values, among others. Here, we describe
the ones that are relevant to our work:
• Nondeterministic Values. The function VERIFIER nondet X(void) returns a non-
  deterministic value of type X, where X is any C primitive type, such as int or float.
  In this context, nondeterministic means any value that the type can be assigned to.
• Preconditions. The function VERIFIER assume( Bool) is used to define a path pre-
  condition. It only allows the execution to continue if the condition holds. Otherwise,
  it causes the path of execution to be unreachable (and vacuously correct).
• Violation Functions. For the ReachSafety category, the intrinsic function
  reach error(void) specifies that the path contains an error. If a program can reach
  this statement, it implies that the property has been violated.
We give an example of the use of these intrinsic functions in Figure 8.




                                          22
          Main Harness    Numerical Libraries
                                                join files                       gcc -E
                                                             Almagamation (.c)            Benchmark Instance (.i)

         Neural Network   Intrinsic Functions



                          Fig. 9: Benchmark conversion workflow.


4.2 Benchmark Conversion Workflow
With all the requirements defined in Section 4.1.1, we can describe our workflow to
automatically convert our benchmarks to the SV-COMP format (see Figure 9). To
minimise duplication, the NeuroCodeBench repository23 divides the source code of
each benchmark instance into the following components:
• Main Harnesses. These files are the entry point of the C program. All of them
  provide a main() function with pre- and post-conditions, as shown in Figure 8. We
  make sure that all instances of undefined behaviour are specified via calls to the
  SV-COMP intrinsic functions (see Section 4.1.1).
• Neural Networks. NeuroCodeBench 2.0 categories that involve whole neural net-
  works (see Table 5) tend to reuse the same neural network code for multiple safety
  properties. For this reason, we keep the neural network implementation in a separate
  file.
• Numerical Libraries. All benchmarks generated with the help of keras2c (see Table
  5) require an additional library that provide the implementation of Keras layers.
  Furthermore, experiments that involve the use of explicit operational models for
  math.h rely on linking with either the MUSL or CORE-MATH libraries (see Section
  2.5).
• Intrinsic Functions. These files contain the headers with the intrinsic function
  declarations (see Section 4.1.1).
    As a first step, we need to merge each harness with all its dependencies and produce
a single self-contained file (see Section 4.1). We do so via a so-called amalgamation
stage. The term is inspired by the SQLite project [89], where an amalgamation is
a single C source file that contains everything needed to compile the library. For
NeuroCodeBench 2.0, we automate this process with CMake.24 We show an example
of the result in Figure 10.
    As a second step, we need to make explicit the host configuration of the self-
contained source file (see Section 4.1). On the one hand, we include all relevant library
headers and preprocess the resulting file with the GCC compiler.25 On the other hand,
we need to remove any system-specific or compiler-specific intrinsics. For the latter,
we notice that GCC tends to introduce a number of function attributes to mark them
 23
    https://github.com/emanino/plain c nn benchmark
 24
    https://cmake.org/
 25
    https://gcc.gnu.org/onlinedocs/gcc/Function-Attributes.html




                                                        23
      #include <verifier_functions.h>                   # include <verifier_functions.h>
      void network(const float in[1][21],               void network(const float in[1][21],
        float out[1][2]);                                  float out[1][2]);
      int main() {                                      int main() {
        float t1[1][21];                                   // ...
        float t2[1][2];                                 }
        t1[0][0] = __VERIFIER_nondet_float();           # include <float.h>
        // ...                                          # include <math.h>
        __VERIFIER_assume(t1[0][0] >= 0.0f              // ...
          && t1[0][0] <= 1.0f);                         static const float weights[168][21] = {
        // ...                                             {-1.0000000000000000000f, ... },
        network(t1, t2);                                   // ...
        // ...                                          }
        __VERIFIER_assert(!(t2[0][0] >= 1.0f            void network(const float in[1][21],
          && t2[0][1] <= 0.0f));                           float out[1][2]) {
        return 0;                                                 // ...
      }                                                 }


Fig. 10: Example of amalgamation from prop bool v21 c126 safe.c. The main har-
ness (left) is combined with the neural network implementation, numerical libraries
and intrinsic functions (right). For reason of space, the code shown here has been
greatly simplified.


as allocations. Since attributes are not standard across compilers, we use the Clang
compiler26 to identify them before removal.
   As a final sanity check step, we make sure that we are still able to compile the
benchmarks with GCC. During this check, we use mock-up implementations of the
SV-COMP intrinsic functions to avoid linking errors.

4.3 BenchExec Setup
In addition to the .i sources containing the C program and ReachSafety specification,
a well-formed SV-COMP benchmark provides additional files in four different formats.
These files are consumed by the BenchExec framework [33] when running the software
verifiers, and allow us to automate the whole evaluation process. More specifically, the
four file formats specify the following information:
• Tool Definition. An .xml file for each software verifier. The files specify the resource
  limits and options used by the respective tool. Additionally, they list which run-sets
  should be used for the analysis. We use the same files submitted by tool authors
  to the ReachSafety category of SV-COMP and replace the run-sets with those of
  NeuroCodeBench 2.0.
• Run-Set. A .set file that lists all benchmark instances in a given category. The file
  contains a regex that matches all relevant source code files.
• Specification. A .yml file for each benchmark instance. Each file lists the source
  code (see Section 4.2), the word size (32 or 64 bits), the property definition, and the
  expected verdict (safe or unsafe). We produce these files in a programmatic way.

 26
      https://clang.llvm.org/docs/AttributeReference.html


                                                   24
• Property. A .prp file with the definition of the safety property to be verified in LTL
  format. For this work, we use the same specification as the SV-COMP ReachSafety
  category:
                 CHECK( init(main()), LTL(G ! call(reach error())) )                 (10)
  which states that, when starting the program execution from the main function, the
  function reach error should never be invoked.
    With this setup, we can run BenchExec on NeuroCodeBench 2.0 and evaluate all
software verifiers that participate in SV-COMP. We do so in Section 5.

5 Experiments
After designing NeuroCodeBench (Section 3), and building it in a format compatible
with existing automated software verifiers (Section 4), we can now run our experimen-
tal study on the verification of floating-point neural networks at the software level.
To do so, we take the perspective of an expert user, who knows how to install, run,
and analyse the results of automated verification tools. As such, we assume that we
can only apply minimal to no configuration changes to existing verification tools. This
is in direct contrast to tool authors, who have deep knowledge about the configura-
tion options (e.g. command-line flags) and can potentially introduce sizable changes
to improve the performance of their tool.27
    In this light, we want to answer the following experimental questions using
NeuroCodeBench:
• Tool Correctness. Can we trust the verdicts produced by automated software ver-
  ifiers? Thanks to the presence of ground-truth labels for each NeuroCodeBench
  instance, we can check whether verifiers return the correct verdict. That gives us an
  indication of whether these tools can be used as a safety oracle for the floating-point
  implementations of neural networks. The results are given in Section 5.2.
• Maths Library Support. Does the presence of calls to math.h affect automated soft-
  ware verifiers? A large proportion of NeuroCodeBench instances contains functions
  calls to math.h, which the verifiers might not support. This gives us an opportunity
  to test whether it is possible to provide external definitions (operational models) of
  these functions to the verifiers. The results are given in Section 5.3.
• Scalability. How large of a problem can existing automated verification tools solve?
  By design, NeuroCodeBench contains instances in a wide range of complexity, from
  individual layers and activations to full neural networks. With it, we can estimate the
  scalability of verification tools, which informs the potential applications for which
  they can be employed. The results are given in Section 5.4.
• Historical Progress. Has the performance of automated software verifiers improved
  in the past few years? Since NeuroCodeBench is a new benchmark, it can be
  used to retroactively investigate the evolution of verification tools and establish

  27
     Note the all authors of this paper are involved with the development of ESBMC [52]. However, we
explicitly avoided making changes to ESBMC for the purposes of the present paper, treating it as an external
tool instead (see Section 5.1.1).




                                                    25
  whether general improvements in software verification readily translate to floating-
  point neural network code. We do so by going as far back as 2018. The results are
  given in Section 5.5.
   Before covering the results of the reproducibility study, we discuss the details of
our experimental setup in Section 5.1.

5.1 Experimental Setup
Our experimental setup is designed to replicate the conditions of SV-COMP as much
as possible, as they constitute one of the highest standards for scientific reproducibility
in the community [32, 33], as detailed in Section 4. For reference, we provide a public
stand-alone copy of NeuroCodeBench 2.0 and the results of the verifier runs.28

5.1.1 Software Verifiers.
For our experiments, we compare eight state-of-the-art software verifiers: 2LS [90],
CBMC [51], CPAChecker [53], DIVINE [91], ESBMC [52], PeSCo [92], Pinaka [93],
UAutomizer [94]. These eight tools have been taking part in SV-COMP for several
years, are actively maintained by their respective research groups, and support C
programs with floating-point computation. Other software verification tools exist [32],
but we exclude them from our experiments due to a range of factors outside of our
control spanning licensing restrictions, limited support for floating-point C programs,
and local configuration issues. For reproducibility reasons, we use the versions available
on the SV-COMP website29 without modifications, and run them on NeuroCodeBench
using a local instance of BenchExec 3.23 [33]. When not otherwise specified, we use
the SV-COMP’24 version of the tools. In the historical comparison of Section 5.5, we
refer to the archived versions of ESBMC on the SV-COMP website from 2018 to 2025
(current year).

5.1.2 Hardware Platform.
We run all experiments on an Ubuntu 20.04 machine with Kernel 5.4.0-177-generic.
The hardware is a 64-bit 32-core Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz with
170GiB of RAM. We allow the verifiers to use 15GB of RAM, 900s of CPU time,
and four cores per each benchmark instance. The bulk of our experiments took place
in three main phases that spanned from July 2024 to June 2025, followed by a few
minor updates in June 2026. In total, we estimate that reproducing the experiments
in this paper would take approximately 3163 CPU hours: 2312 CPU hours for the
results in Sections 5.2, 5.3, 5.4, and 851 CPU hours for the historical results of ESBMC
(excluding 2024, since it is already included in the previous count) in Section 5.5.

5.1.3 Implementation of math.h
We bundle with NeuroCodeBench 2.0 the plain C implementations of math.h provided
by the MUSL and CORE-MATH libraries (see Sections 2.5 and 4.2). Specifically,

 28
      https://zenodo.org/records/21873894
 29
      https://sv-comp.sosy-lab.org/



                                            26
we extract all relevant 32-bit floating-point functions listed in Section 3.2.30 In the
case of CORE-MATH, we omit the sqrtf function, which is not provided, and the
sinf and cosf functions. The latter two functions rely on 128-bit float arithmetic,
which is not supported by the majority of existing software verifiers. Furthermore, we
reduce the external dependencies of the MUSL library to the minimum necessary for
successful compilation, and replace the bit manipulation primitives in CORE-MATH
with plain C implementations. We also address minor issues with type casting and
macro definitions.

5.2 Tool Correctness
Table 6 provides a high-level overview of the output of the verifiers. After analysing
each instance in NeuroCodeBench 2.0 for 900 seconds, the verifiers return inconclu-
sive verdicts for the majority of the benchmark. More worryingly, a non-insignificant
percentage of the verdicts are incorrect (3% in total).



Table 6: Breakdown of all verdicts returned by the verifiers for NeuroCodeBench 2.0
benchmarks (912 overall).
                        Correct       Incorrect                       Inconclusive
      Verifier
                  Safe     Unsafe   Safe   Unsafe      Timeout   Out of Memory       Unknown   Error

    2LS            12         2      -        -           4             -              894      -
   CBMC            66        305     -      121           -            80               -      340
 CPAChecker        18         19     -        -          292          265               -      318
  DIVINE           6          3      -        -          390          152              361      -
  ESBMC            76         86     -        -          539          211               -       -
   PeSCo           24         25    10        -          482           58               -      313
   Pinaka          44         71     -       82          243          292               -      180
 UAutomizer        9         27      -       12          754            1              106      3




    The only tool that produces the most definitive verdicts (i.e., safe or unsafe) is
CBMC, with 492 definitive against 440 inconclusive verdicts. However, nearly a quarter
of them are incorrect. Similarly, more than a third of all definitive verdicts produced
by Pinaka and exactly a quarter of all definitive verdicts reported by UAutomizer are
incorrect. In all three cases, these are incorrect unsafe verdicts, i.e. the tools report
the presence of a spurious bug. In contrast, the only tool that returns around 17% of
incorrect safe verdicts is PeSCo.
    Although the other verifiers appear to produce only correct verdicts, we cannot
exclude the possibility that some of them might be “lucky guesses”. Indeed, given the
balanced number of safe and unsafe instances in NeuroCodeBench 2.0 (see Table 1), a
hypothetical verifier that produces random verdicts would be correct 50% of the time
on average. The SV-COMP rules [32] discourage guessing by penalising verdicts that

 30
      See https://github.com/emanino/plain c nn benchmark/tree/main/extern/math op models



                                                  27
                 Table 7: Definite verdicts (both correct and incor-
                 rect) on the subset of NeuroCodeBench 2.0 with calls
                 to math.h (180 instances).




                                                CPAChecker




                                                                                               UAutomizer
                                                             DIVINE

                                                                      ESBMC
                                         CBMC




                                                                                      Pinaka
                                                                              PeSCo
                                   2LS
                  Op. Models



                  None             2     169     -            -       66      3       127      13
                  MUSL             -      57    27            -       54      37       58       -
                  CORE-MATH        2     120    4             -       35      7       67        -



are not supported by a valid proof. Unfortunately, this process of witness validation
relies on running an ensemble of specialised software verifiers to check the proof, which
could still return a wrong result in our setting. For this reason, we choose to only
evaluate the verifiers against our ground-truth verdicts.
    With that caveat in mind, CBMC, ESBMC, and Pinaka are the three tools that
correctly solve the largest number of instances: 371, 162, and 115 respectively. Among
them, ESBMC is the only one that does not return incorrect verdicts. For this reason,
we focus on ESBMC in our later analysis of scalability and historical progress (see
Sections 5.4 and 5.5).
    On a different note, all inconclusive verdicts in Table 6 can be broadly placed
into one of two subcategories: exhaustion of computational resources or defence mech-
anisms against unsupported features. For the former, the tools typically report a
timeout or out of memory message. Occasionally, some of them return an error code
instead. For example, CBMC produces a specific error code instead of a timeout. For
the latter, many tools resort to outputting an unknown or error verdict when they
encounter a mathematical function that is not currently supported. We give a detailed
analysis of log outputs and time distributions in Appendices C and D.

5.3 Maths Library Support
One of the difficulties of verifying software that features calls to external libraries comes
from the fact that a verifier will struggle to reason on them if the implementations
of these libraries are not provided. Although most verifiers support the core features
of the C language, including many standard libraries, the mathematical functions in
math.h are often overlooked. Here, we measure how verifiers perform on benchmark
instances that contain calls to these functions and we evaluate whether introducing
explicit C implementations of math.h improves the verification outcomes.
    To do so, we isolate the 180 instances that contain calls to math.h by filtering
NeuroCodeBench 2.0 against the list of mathematical functions in Table E3. Then,
we concatenate the MUSL or CORE-MATH operational models to each benchmark
instance as detailed in Section 4.2. Table 7 and Figure 11 compare the performance
of software verifiers with and without math.h operational models.



                                                28
 180                                                                              180
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH
                                                                                                                                             97
 90                                                                               90
                                                                                                        58         51                                 45
                                                                                             23   24          32
       2         2                                                                      14                                                        2
            0          0     0    0       0   0    0        0    0    0                                                    0   0    0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                                 (a) 2LS                                                                     (b) CBMC

 180                                                                              180
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH

 90                                                                               90

            3    1          10    3                              14
       0               0                  0   0    0        0         0                 0    0    0     0     0    0       0   0    0        0    0    0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                      (c) CPAChecker                                                                         (d) DIVINE

 180                                                                              180
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH

 90                                                                               90
       27              39   33
            18   14               21                                                                          12               8                 14
                                          0   0    0        0    3    0                 0    3    1     3          6       0        0        0         0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                            (e) ESBMC                                                                        (f) PeSCo

 180                                                                              180
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH

 90                                                         73                    90
                       40   33    28
       14   20   24                                                   15
                                          0   0    0             5                      3    0    0     9     0    0       0   0    0        1    0    0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                            (g) Pinaka                                                                 (h) UAutomizer

Fig. 11: Verifier performance on the 180 benchmark instances of NeuroCodeBench
2.0 that contain math.h functions.


    Overall, the introduction of operational models has opposite effects on different
software verifiers, as Table 7 shows. On the one hand, verifiers like CBMC, ESBMC,
Pinaka, and UAutomizer see a reduction in the number of solved instances. We believe
this is a consequence of the additional complexity of reasoning on the implementation
of mathematical functions, i.e., there is more C code to verify when the libraries are
provided. On the other hand, tools like CPAChecker and PeSCo greatly benefit from
the presence of operational models. In their case, we believe that MUSL yields better
results than CORE-MATH because the latter implementations often rely on double-
precision arithmetic followed by truncation, instead of performing the computation in
single-precision directly.
    At the same time, our goal is not just to increase the total number of solved
instances, but rather the number of correct ones. In this respect, Figure 11 shows a
more detailed picture. Specifically, the majority of verdicts produced by CPAChecker
and PeSCo with the MUSL operational models turns out to be incorrect. For PeSCo,



                                                                             29
the increase includes incorrect unsafe verdicts, which the tool never produces on the
plain benchmark (see Table 6).
    In contrast, the introduction of operational models benefits CBMC and Pinaka the
most. Indeed, these two tools see a significant reduction in the number of incorrect
verdicts, with almost no impact on the total number of correct ones. In fact, MUSL
demonstrates the most striking effect by almost completely eliminating all incorrect
verdicts. Regarding ESBMC, the introduction of operational models resulted in a
moderate reduction in performance.
    For completeness, we also report the results on the 732 benchmark instances that
do not contain relevant calls to math.h in Figure C2, together with the full result
matrix in Table C1. As that figure shows, the verifier performance is largely unaffected
by the addition of (unused) operational models. This is not surprising, since most
software verifiers employ slicing techniques to ignore the portions of code that do not
have any effect on the verification conditions.

5.4 Scalability
One of our design requirements for NeuroCodeBench 2.0 was to provide benchmark
instances in a wide range of complexity (see Section 3.1). With them, we can mea-
sure the scalability of software verifiers as the reasoning tasks become computationally
harder. Table 8 compares the performance of the verifiers between different subcat-
egories, without operational models of math.h functions. There, we highlight the
number of both correct and incorrect definitive verdicts (safe or unsafe) returned by
each verifier. Also, we score the complexity of each category by computing a solution
rate, which represents the average proportion of benchmarks solved by the verifiers.



Table 8: Number of correct (incorrect) verdicts returned by the verifiers for each category of
NeuroCodeBench 2.0. We sort the categories by their average solution rate, i.e. the percentage
of instances solved correctly (incorrectly) by the average verifier.




                                                                                                                         Solution Rate
                                                    CPAChecker




                                                                                                        UAutomizer
                                                                 DIVINE

                                                                          ESBMC
                                            CBMC




                                                                                             Pinaka
                                                                                   PeSCo
                                    2LS




 Benchmark Category



 Neural Layers (n = 86)              -     69 (7)   27           5        72      36       59 (13)    23 (8)         42% (4%)
 Activation Functions (n = 57)      12    23 (33)   10           4        27      11       19 (36)    8 (4)          25% (16%)
 Maths Functions (n = 58)           2     22 (33)    -           -        25       -       22 (33)      5            16% (14%)

 Lipschitz-Bounded Nets (n = 108)   -       55       -            -       16        -        14          -              9.8%
 SAT ReLU Networks (n = 96)         -     41 (24)    -            -       16      (10)        1          -           7.6% (4.4%)
 Polynomial Approx. (n = 96)        -       45       -            -        6        -         -          -              6.6%
 Hopfield Networks (n = 80)         -     36 (24)    -            -        -        2         -          -           5.9% (3.8%)

 Reinforcement Learning (n = 296)   -       80       -            -       -        -          -          -               3%
 Probability Density (n = 35)       -        -       -            -       -        -          -          -               0%




                                              30
    As expected, the three easiest categories to solve are those that contain individual
components of a neural network: neural layers, activation functions, and mathematical
functions. Among them, neural layers involves the lowest number of calls to math.h,
with only 44% of instances, compared to 77% and 100% for the other two cate-
gories, respectively. As a consequence, the number of incorrect verdicts in neural layers
remains relatively small.
    As we move onto benchmark instances that contain whole neural networks, the
solution rate drops into the single digits, and many state-of-the-art software verifiers
cease to return useful output. Still, we can see a difference between synthetically-
generated benchmarks and real-world ones. Indeed, we constructed the former
four categories (i.e., Lipschitz-Bounded Networks, SAT ReLU Networks, Polynomial
Approximation, Hopfield Networks) to include a few small instances (see Section 3),
which the verifiers can solve successfully. In contrast, we converted the latter two cat-
egories (i.e. Reinforcement Learning and Probability Density) from the VNN-COMP
competition format (see Section 3.9), and their relatively larger neural network size
(64 to 512 neurons) is at the upper limit of what state-of-the-art software verifiers can
handle.
    In the remainder of the section, we identify the exact scalability limit of soft-
ware verifiers by looking at the individual results of each benchmark instance. More
specifically, we focus on the three subcategories containing synthetic networks (i.e.,
Lipschitz-Bounded Networks, SAT ReLU Networks, Polynomial Approximation Net-
works), and we report how much CPU time and memory the verifiers use. We mainly
base our analysis on ESBMC, as it is the tool with the highest number of correctly
solved benchmarks that produces no incorrect verdicts.

5.4.1 Lipschitz-Bounded Networks
As we explain in Section 3.8, two complexity factors are at play in this subcategory.
First, the network architecture itself varies in the number of inputs i and the width
of the hidden layers w, while the number of outputs o = 1 and hidden layers d = 2
remains the same. Due to the specific Lipschitz-bounded architecture we chose, the
number of network parameters is (2d− 1)w2 +(i + o + d)w + o, which scales quadratically
in the network width w. Second, each network is associated with six different safety
properties (cases). These differ in their decidability threshold: three are safe and three
are unsafe. Cases 2, 3 are the closest to the threshold and thus the most difficult to
solve, at least in theory.
    Figure 12 shows that ESBMC solves 16 out of 108 benchmark instances. Most of
them (10 out of 16) are the smallest networks with layer width w = 4. As the layer
width increases, ESBMC begins experiencing a higher rate of timeouts. Interestingly,
all solved instances beyond w > 4 are unsafe, i.e. ESBMC needs only to find one
counterexample. Moreover, there is only one instance of cases 2, 3 that ESBMC is able
to solve, thus confirming that being closer to the decision threshold makes for more
challenging instances regardless of network size. In terms of memory consumption,
ESBMC demonstrates a steady increase in memory consumption as the size of each
layer in the networks increases.



                                           31
            1,000

                        800




  CPU Time (s)
                        600
                        400
                        200
                    0
  Memory (GB)    10.0

                        7.5

                        5.0

                        2.5

                          0
                                     Correct
                        103        Inconclusive
 Net. Params




                        102


    Cases 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5
    Verdict Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe
    Width 4       4     4     4     4     4     8     8     8     8     8     8 12 12 12 12 12 12 16 16 16 16 16 16 20 20 20 20 20 20 24 24 24 24 24 24
    Inputs 2      2     3     3     4     4     2     2     3     3     4     4     2     2     3     3     4     4     2     2     3     3     4     4     2     2     3     3     4     4     2     2     3     3     4     4


                 Fig. 12: Performance of ESBMC on the Lipschitz-Bounded Networks category.


                   1,000

                         800
         CPU Time (s)




                         600
                         400
                         200
                           0
                         7.5
         Memory (GB)




                         5.0


                         2.5


                              0
                         105          Correct
                                    Inconclusive
       Net. Params




                              4
                         10

                         103

                         102
                                   5 Uns.

                                  10 Uns.

                                  15 Uns.
                                  18 Uns.


                                   8 Uns.
                                  24 Uns.

                                  27 Uns.

                                  16 Uns.

                                  24 Uns.


                                  32 Uns.

                                  40 Uns.

                                  13 Uns.
                                  46 Uns.


                                  26 Uns.

                                  39 Uns.

                                  52 Uns.

                                  65 Uns.

                                  21 Uns.

                                  78 Uns.

                                  42 Uns.
                                  62 Uns.


                                  84 Uns.

                                  105 Uns.

                                  34 Uns.

                                  126 Uns.

                                   68 Uns.

                                  102 Uns.

                                  136 Uns.

                                  170 Uns.

                                   55 Uns.

                                  204 Uns.

                                  110 Uns.

                                  165 Uns.

                                  220 Uns.

                                  275 Uns.

                                   89 Uns.

                                  330 Uns.
                                  178 Uns.


                                  267 Uns.

                                  356 Uns.

                                  445 Uns.

                                  144 Uns.

                                  534 Uns.

                                  288 Uns.

                                  432 Uns.

                                  576 Uns.

                                  720 Uns.

                                  864 Uns.
                                   5 Safe

                                  10 Safe

                                  15 Safe


                                  20 Safe
                                   8 Safe


                                  25 Safe

                                  30 Safe

                                  16 Safe

                                  24 Safe
                                  32 Safe

                                  40 Safe

                                  13 Safe


                                  48 Safe
                                  26 Safe

                                  39 Safe

                                  52 Safe

                                  65 Safe

                                  21 Safe

                                  78 Safe

                                  42 Safe


                                  63 Safe
                                  84 Safe

                                  105 Safe

                                  34 Safe

                                  126 Safe

                                   68 Safe

                                  102 Safe

                                  136 Safe

                                  170 Safe

                                   55 Safe

                                  204 Safe

                                  110 Safe

                                  165 Safe

                                  220 Safe

                                  275 Safe

                                   89 Safe

                                  330 Safe


                                  178 Safe
                                  267 Safe

                                  356 Safe

                                  445 Safe

                                  144 Safe

                                  534 Safe

                                  288 Safe

                                  432 Safe

                                  576 Safe

                                  720 Safe

                                  864 Safe
        Verdict
        Clauses                   144
                                  144


                                  144
                                  144
                                  144
                                  144
                                  144
                                  144
                                  144
                                  144
                                  144
                                  144
        Inputs
                                   13
                                   13


                                   13
                                   13
                                   13
                                   13
                                   13
                                   13
                                   13
                                   13
                                   21
                                   21
                                   13
                                   13
                                   21
                                   21
                                   21
                                   21
                                   21
                                   21
                                   21
                                   21
                                   34
                                   34
                                   21
                                   21
                                   34
                                   34
                                   34
                                   34
                                   34
                                   34
                                   34
                                   34
                                   55
                                   55
                                   34
                                   34
                                   55
                                   55
                                   55
                                   55
                                   55
                                   55
                                   55
                                   55
                                   89
                                   89
                                   55
                                   55
                                   89
                                   89
                                   89
                                   89
                                   89
                                   89
                                   89
                                   89


                                   89
                                   89
                                   5
                                   5
                                   5
                                   5
                                   5
                                   5
                                   5
                                   5
                                   8
                                   8
                                   5
                                   5
                                   5
                                   5
                                   8
                                   8
                                   8
                                   8
                                   8
                                   8
                                   8
                                   8


                                   8
                                   8




                                  Fig. 13: Performance of ESBMC on the SAT ReLU Networks category.


5.4.2 SAT ReLU Networks
As we explain in Section 3.6, the size of the networks in this category is directly
correlated with the number of input variables v and clauses c in the original CN F
formula. More specifically, the number of parameters in the network is given by (2v +
c)(v + 3) + 2, which scales quadratically in the number of input variables. We also
expect unsafe instances to be easier to solve than safe ones, as finding a counterexample
suffices.
    Figure 12 shows that ESBMC solves 16 out of 96 instances. They include all net-
works with only v = 5 variables and four networks with v = 8 variables. As expected,
safe instances take considerably longer to solve and are the first to time out as the


                                                                                                              32
        1,000

                800


 CPU Time (s)
                600
                400
                200
                   0
                12.5
 Memory (GB)




                10.0
                 7.5
                 5.0
                 2.5
                  0
                         Correct
                104
                       Inconclusive
 Net. Params




                103


                102

  Cases 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5 0 1 2 3 4 5
  Verdict Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns. Safe Uns.
  Depth 4       4     3     3     4     4     1     1     2     2     1     1     3     3     4     4     1     1     2     2     1     1     3     3     4     4     2     2     3     3     2     2
  Width 4       4     8     8     8     8 128 128 16 16 256 256 16 16 16 16 512 512 32 32 1024 1024 32 32 32 32 64 64 64 64 128 128


                 Fig. 14: Performance of ESBMC on the Polynomial Approximation category.


network size grows larger. As per the memory, we begin to observe a clear phe-
nomenon: while the memory consumption initially increases with the complexity of
the instances, it drops to zero again for instances with more than 6K network param-
eters. We believe this phenomenon can be attributed to the bounded model checking
nature of ESBMC, where the verification process consists of iterating between sym-
bolic execution and SMT solving. Thus, reaching the timeout at different stages will
result in different memory consumption profiles (e.g., symbolic execution is typically
less memory intensive than SMT solving).

5.4.3 Polynomial Approximation Networks
As we explain in Section 3.7, the complexity of the present category is driven by two
main factors. First, the number of network parameters can be computed as (d − 1) ∗
w2 + (d + 2)w + 1, where d is the number of hidden layers and w is their width. As
such, the network size scales quadratically in the layer width w. Second, there are six
safety properties (cases) for each network, three safe and three unsafe. The middle
cases (i.e. 2, 3) are the closest to the decision threshold. Similar to Section 5.4.1, we
expect them to be more difficult to solve than the others.
    Figure 14 shows that ESBMC solves only the 6 simplest benchmark instances,
with the rest reaching timeout. Among these, we do not observe the expected peak of
complexity around cases 2, 3. Instead, all unsafe instances appear easier to solve. In
terms of memory consumption, ESBMC exhibits the same sudden drops as the SAT
ReLU category (see Section 5.4.2).




                                                                                                 33
5.5 Historical Progress
One of the main inspirations behind our work were anecdotal observations of incorrect
verdicts from software verifiers. Early development of NeuroCodeBench allowed us to
confirm our observations, measure their frequency, and begin the process of engaging
with the software verification community. This section examines the recent progress
in the field.

5.5.1 Impact on Tool Development
We first introduced NeuroCodeBench 1.0, an earlier version of our benchmark, into the
SV-COMP benchmark suite in time for its 2024 edition [32]. This was a crucial step
in attracting the attention of the community to the problem of verifying C programs
with extensive use of floating-point arithmetic and mathematical functions. Given the
rules of SV-COMP, tool authors had a chance to look at the benchmark and patch
their software verifiers before the competition.


                Correct        Incorrect                                                                                     Correct
 400                                                                      383                               400             Incorrect


                                                    255
                                                                    224
                                                                                                                       204
 200                                                      177                                               200
           111
                    76                     69                                                                                   78
                                                                                                                                                               50
                                     30                                                                                                                                        11
                                                                                         7        6                                              7    0              0                   0              6        0
      0                                                                                                           0
               CBMC           CPAChecker            ESBMC            PeSCo          UAutomizer                             CBMC           CPAChecker           ESBMC           PeSCo               UAutomizer


                                     (a) August 2023.                                                                                      (b) December 2023.

Fig. 15: Verifier performance on NeuroCodeBench 1.0 before and after its introduction
into the SV-COMP benchmark suite.




500                                                                                                         500
           Correct       Incorrect                                                                                     Correct       Incorrect
400                  371                                                                                    400
                                                                                                                                 353

300                                                                                                         300


200                                                       162                                               200
                            121                                               115                                                       122                         130                      127
100                                                                                 82                      100                                                                                    82       67
                                                                    49                                                                           42                           57
                                      37                                                     36
          14    0                          0    9   0           0        10                       12                  14    0                         0   12   0          0         10                           0
  0                                                                                                           0
           2LS        CBMC CPAChecker DIVINE              ESBMC     PeSCo       Pinaka UAutomizer                      2LS        CBMC CPAChecker DIVINE            ESBMC     PeSCo          Pinaka UAutomizer



                                          (a) June 2025.                                                                                      (b) January 2026.

Fig. 16: Verifier performance on NeuroCodeBench 2.0 before and after its introduction
into the SV-COMP benchmark suite.


    For this reason, the difference in tool performance before and after the introduction
of NeuroCodeBench 1.0 is stark, as shown in Figure 15. Note that the results in Figure


                                                                                                       34
                                              Correct Safe




                                                                                     v1.0 release




                                                                                                           v2.0 release
                               300           Correct Unsafe




            Solved Instances
                                             Incorrect Safe
                                            Incorrect Unsafe
                               200


                               100


                                 0
                                     2018   2019     2020      2021    2022   2023   2024           2025   2026
                                                                       Year

Fig. 17: NeuroCodeBench 2.0 performance of different versions of ESBMC between
2018 and 2026.


15a are our own, as detailed our preliminary technical report [28]. In contrast, the
results in Figure 15b come from the official SV-COMP 2024 runs, which we filtered
to show the NeuroCodeBench 1.0 instances only. Informal communication with tool
authors confirmed that a large portion of incorrect results was fixed in the run up to
the competition in direct response to the release of our benchmark.
    The newest version of our benchmark introduces significantly more instances and
fixes some known issues, as detailed in Appendix B. As such, it may reveal further
incorrect behaviour in existing verifiers and drive further development of these tools.
    It is important to note that all of the experiments in this paper were conducted
before NeuroCodeBench 2.0 was included into the most recent addition of SV-COMP
2026. Since then some verifiers demonstrated some improvements (see Figure 16b).
Although, the overall effect was not as noticeable as when NeuroCodeBench 1.0 was
first introduced into SV-COMP 2024.

5.5.2 Performance Trends since 2018
NeuroCodeBench 2.0 can also be used as a measuring tool to gauge the progress of soft-
ware verifiers on floating-point reasoning over the years. In this section, we recover the
executables and setups of older software verification tools from the historical records
of SV-COMP. We cover the nine years spanning between the 2018 and 2026 editions
of the competition. For simplicity, we study the performance of ESBMC only. We
choose this specific tool because it has the best performance among those that do not
produce any incorrect verdicts (see Table 6).
    The results in Figure 17 show a sharp increase in the number of safe verdicts around
2022 and 2023, including a large portion of incorrect ones. An internal investigation
within our research group revealed that the increase was due to an erroneous imple-
mentation of an unrelated verification algorithm in ESBMC (i.e., k -induction), which
remained undiscovered until the release of NeuroCodeBench 1.0. The latter also caused
a significant shift in development focus towards ensuring the verifier correctness on
floating-point benchmarks in 2024. Indeed, after the release of NeuroCodeBench 1.0
the number of incorrect verdicts drops from 295 to zero.



                                                                      35
    Additionally, there is a gradual improvement in the number of instances correctly
solved by ESBMC, if we ignore the 2022-2023 spike. The trend continues in 2025, when
ESBMC has yet again increased the number of correct instances from 162 to 231, albeit
at the price of introducing ten incorrect outcomes. We provide a full breakdown of the
results in Appendix E (see Table E2). At he same time, the most recent results from
2026 demonstrated a performance drop with ESBMC correctly solving 114 instances
(compared to 162 and 231 in the two years before) and producing no incorrect verdicts.

6 Conclusions and Future Work
In this paper, we show how to model the floating-point details of neural networks by
extracting their low-level implementation in plain C code. This step is necessary in
ensuring the safety and reliability of neural network models, since the numerical details
of performing finite-precision inference may affect the output of the computation and
produce unwanted outcomes. Unfortunately, state-of-the-art neural network verifiers
discard these computational details and thus are unable to guarantee the absence of
vulnerabilities in the worst case.
    For this reason, we perform a rigorous evaluation of the performance of another
class of verification tools, i.e. software verifiers, which are able to reason on the
exact behaviour of floating-point arithmetic. To do so, we significantly expand on
NeuroCodeBench , our existing benchmark for neural network code verification. Our
benchmark design satisfies two main requirements: the verdict of every verification
query must be known in advance, and the set of verification queries must feature a
gradual increase in complexity. Together, the two requirements allow us to test both
the correctness and scalability of existing software verifiers.
    In summary, our work reveals a number of crucial pieces of information. First,
neural network verification at the software level is conceptually feasible, but the exist-
ing tools are not yet ready to cope with the scale of the problem. Indeed, 50% of
the software verifiers we test return a non-insignificant number of incorrect verdicts.
Furthermore, even the most successful of them fail to solve a large majority of our
benchmark. Second, we have evidence to show that the release of NeuroCodeBench
has had a very beneficial impact on the community. In fact, the presence of our bench-
mark has led to a drastic reduction, if not complete elimination, of incorrect verdicts in
most state-of-the-art software verification tools. By maintaining and expanding Neu-
roCodeBench over time, we commit to further encourage tool authors to improve
their verifiers on floating-point tasks.
    At the same time, we believe that the path towards certifying the whole imple-
mentation of a neural network against worst-case numerical deviations is still long.
In particular, software verifiers need native support for mathematical libraries such
as math.h and custom decision procedures for neural network code. In both cases,
we plan to take inspiration from the algorithms employed by high-level neural net-
work verifiers (branch and bound, linear abstractions) and adapt them to work on
floating-point arithmetic.




                                           36
Acknowledgements. This work is partially funded by the EPSRC grant
EP/T026995/1 entitled “EnnCore: End-to-End Conceptual Guarding of Neural Archi-
tectures” under Security for all in an AI enabled society, the ARIA Opportunity Seed
entitled “Hardware-Level AI Safety Verification” under Mathematics for Safe AI, and
the the EPSRC grant EP/V000497/1 entitled “SCorCH: Secure Code for Capability
Hardware”.

Appendix A              Adoption of the IEEE 754 Standard in
                        the C Language
In Section 3, we present several instances of our benchmark where we rely on functions
from the standard library math.h. There, we make the assumption that all functions in
math.h have correctly-rounded implementations and existing software verifiers reason
over correctly-rounded implementations. Crucially, if this assumption were not to hold,
some of our ground-truth verdict may become incorrect. Here, we explain why this
is not always the case because of some conflicts between the IEEE 754 floating-point
and the C language semantics (see Sections A.1 and A.2). Note that the conflicts can
be resolved by providing explicit operational models of the mathematical functions,
as we propose in Section 2.5.

A.1     The IEEE 754 Standard
According to the IEEE 754 standard [42], every floating-point operation should be
correctly rounded. More specifically, Section 4.3 of the standard states the following:
  Except where stated otherwise, every operation shall be performed as if it first produced
  an intermediate result correct to infinite precision and with unbounded range, and then
  rounded that result according to one of the attributes in this clause.

At the same time, any programming language that conforms to the IEEE 754 stan-
dard is required to implement only a small subset of arithmetic operations. More
specifically, Sections 5.4.1 and 5.5.1 of the standard lists the following mandatory oper-
ations: addition, subtraction, multiplication, division, square root, fused multiply-add,
negation and absolute value. All other mathematical operations are labeled as “recom-
mended”, including transcendental, hyperbolic and trigonometric functions (see Table
9.1 therein). That is, an IEEE 754 conformant programming language may not include
functions such as the exponential or sine functions.
    In summary, the IEEE 754 standard does not mandate the implementation of
most functions we find the mathematical library math.h. However, if a programming
language implements any of the recommended functions, then such an implementation
must be correctly rounded. Indeed, Section 9.2 of the standard states that:
  A conforming operation shall return results correctly rounded for the applicable rounding
  direction for all operands in its domain.
Unfortunately, the IEEE 754 standard is not enforceable, and requires effort from
programming language developers and users to maintain compliance. Section 11 of
the standard recognises the potential danger of non-compliant languages to
reproducibility, and states that:


                                            37
  Reproducible results require cooperation from language standards, language processors, and
  users. A language standard should support reproducible programming.

Next, we show how the C language does not comply with the IEEE 754 standard.

A.2      The C99 Standard
The semantics of floating-point arithmetic have remained stable through the years.
Here, we refer to the C99 standard [95] as an example. Specifically, Section 5.2.4.2.2
of the standard states the following about the characteristics of floating point types
in float.h (Point 5 therein):
  The accuracy of the floating-point operations (+, -, *, /) and of the library functions in
  <math.h> and <complex.h> that return floating-point results is implementation defined.
which is in direct constrast to the correctly-rounded requirement of the IEEE 754
standard (see Section A.1). Indeed, the only mention of correct rounding behaviour
regards the fused multiply-add operator.31 Specifically, Section 7.12.13.1 of the C99
standard states that:
  The fma functions compute (x × y) + z, rounded as one ternary operation: they compute
  the value (as if ) to infinite precision and round once to the result format, according to the
  rounding mode characterized by the value of FLT ROUNDS. A range error may occur.

In summary, the C99 standard provides an ambiguous specification of the semantics of
floating-point arithmetic in the C language.32 This fact severely hinders the testing and
verification of numerical software, which requires a clear and non-ambiguous specifica-
tion [55, 96]. Indeed, existing verification tools cope with the inherent ambiguity in the
C language by introducing various degrees of non-determinism and numerical approx-
imation in their operational models of math.h functions. We show the consequences
of this choice in the experimental results of Section 5.3.

Appendix B                  Differences between NeuroCodeBench
                            1.0 and NeuroCodeBench 2.0
In this appendix, we list all differences between the earliest release of NeuroCodeBench
1.0 as described in our technical report [28] and the current release of NeuroCodeBench
2.0.

Bug Fixes.
During benchmark preparation for the 2024 edition of SV-COMP, the community
discovered a few minor bugs in NeuroCodeBench 1.0. We list them here, with the
corresponding patches:

  31
     Contrary to popular belief, the C99 standard does not explicitly mandate correctly-rounded behaviour
for the square root function (see Section 7.12.7.5 therein).
  32
     The newest C23 standard makes an effort to make math.h fully compliant with IEEE 754, see https:
//www.open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf.




                                                   38
• lunarlander 26 unsafe.c and lunarlander 90 safe.c contained wrong pre-
  conditions due to a missing exponential notation in the constant bounds.33 We
  reintroduced the exponential notation, thus making the pre-condition non-empty.
• cos 7 safe.c, erf 5 safe.c, logistic 7 unsafe.c, softsign 5 safe.c and
  tanh 7 safe.c contained calls to the isgreaterequal macro with an integer argu-
  ment.34 We replaced the arguments with a floating-point constant to match the
  macro type.
• logistic 1 safe.c and tanh 1 safe.c contained post-conditions with the wrong
  inequality sign.35 We replaced the erroneous call to isgreaterequal with
  islessequal, which solved the issue.
Furthermore, we independently discovered the following additional bug, which was
patched in time for SV-COMP 2024:
• tanh w8 r4 case 1 safe.c in the Hopfield network subcategory had the wrong ver-
  dict due to the output converging to 1, but not quite reaching it for all inputs. We
  renamed it to tanh w8 r4 case 1 unsafe.c accordingly.

New Instances.
Version 2.0 of our benchmark introduces 305 new verification queries, which we have
clearly marked with the tag new throughout the main body of the paper. For ease
of reference, we list them here as well:
• Maths Functions. We introduce 14 new instances, covering properties of the expm1f
  and log1pf functions.
• Activation Functions. We introduce 15 new instances, covering the Gaussian, GLU,
  and Step activations.
• Neural Layers. The 86 instances in this category are almost entirely new, with the
  exception of the 14 properties of the SoftMax layer. The latter were originally part
  of the activation function category in NeuroCodeBench 1.0.
• SAT ReLU Networks. This category is entirely new, for a total of 96 instances.
• Lipschitz-Bounded Networks. This category is entirely new, for a total of 108
  instances.

Operational Models.
Version 2.0 of our benchmark can be augmented with operational models of math.h
functions. We discuss their role in depth throughout the paper (see Sections 5.1.3, 2.5
and 4.2). Here, we list the single-precision floating-point functions they provide:
• MUSL. Provides acosf, asinf, atanhf, cosf, erff, expf, expm1f, fabsf, fmaxf,
  log1pf, logf, sinf, and tanhf. The addition of sqrtf is optional.
• CORE-MATH. Provides acosf, asinf, atanhf, cosf, erff, expf, expm1f, log1pf,
  logf, sinf, and tanhf.

 33
      https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks/-/merge requests/1490
 34
      https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks/-/merge requests/1456
 35
      https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks/-/issues/1394




                                                 39
            1,000

                 800




  CPU Time (s)
                 600
                 400
                 200
                   0

  Memory (GB)    2.0


                 1.0


                   0
                 105       Correct
                          Incorrect
 Net. Params




                 104    Inconclusive


                 103

                 102
                        5 Uns.

                       10 Uns.

                       15 Uns.
                       18 Uns.


                        8 Uns.
                       24 Uns.

                       27 Uns.

                       16 Uns.

                       24 Uns.


                       32 Uns.

                       40 Uns.

                       13 Uns.
                       46 Uns.


                       26 Uns.

                       39 Uns.

                       52 Uns.

                       65 Uns.

                       21 Uns.

                       78 Uns.

                       42 Uns.
                       62 Uns.


                       84 Uns.

                       105 Uns.

                       34 Uns.

                       126 Uns.

                        68 Uns.

                       102 Uns.

                       136 Uns.

                       170 Uns.

                        55 Uns.

                       204 Uns.

                       110 Uns.

                       165 Uns.

                       220 Uns.

                       275 Uns.

                        89 Uns.

                       330 Uns.
                       178 Uns.


                       267 Uns.

                       356 Uns.

                       445 Uns.

                       144 Uns.

                       534 Uns.

                       288 Uns.

                       432 Uns.

                       576 Uns.

                       720 Uns.

                       864 Uns.
                        5 Safe

                       10 Safe

                       15 Safe


                       20 Safe
                        8 Safe


                       25 Safe

                       30 Safe

                       16 Safe

                       24 Safe
                       32 Safe

                       40 Safe

                       13 Safe


                       48 Safe
                       26 Safe

                       39 Safe

                       52 Safe

                       65 Safe

                       21 Safe

                       78 Safe

                       42 Safe


                       63 Safe
                       84 Safe

                       105 Safe

                       34 Safe

                       126 Safe

                        68 Safe

                       102 Safe

                       136 Safe

                       170 Safe

                        55 Safe

                       204 Safe

                       110 Safe

                       165 Safe

                       220 Safe

                       275 Safe

                        89 Safe

                       330 Safe


                       178 Safe
                       267 Safe

                       356 Safe

                       445 Safe

                       144 Safe

                       534 Safe

                       288 Safe

                       432 Safe

                       576 Safe

                       720 Safe

                       864 Safe
  Verdict
  Clauses




                       144
                       144


                       144
                       144
                       144
                       144
                       144
                       144
                       144
                       144
                       144
                       144
  Inputs
                        13
                        13


                        13
                        13
                        13
                        13
                        13
                        13
                        13
                        13
                        21
                        21
                        13
                        13
                        21
                        21
                        21
                        21
                        21
                        21
                        21
                        21
                        34
                        34
                        21
                        21
                        34
                        34
                        34
                        34
                        34
                        34
                        34
                        34
                        55
                        55
                        34
                        34
                        55
                        55
                        55
                        55
                        55
                        55
                        55
                        55
                        89
                        89
                        55
                        55
                        89
                        89
                        89
                        89
                        89
                        89
                        89
                        89


                        89
                        89
                        5
                        5
                        5
                        5
                        5
                        5
                        5
                        5
                        8
                        8
                        5
                        5
                        5
                        5
                        8
                        8
                        8
                        8
                        8
                        8
                        8
                        8


                        8
                        8




                       Fig. C1: Performance of CBMC on the SAT ReLU Networks category.


Appendix C                             Observations on the Behaviour of
                                       Verifiers on NeuroCodeBench 2.0
In this appendix, we report our detailed observation on the behaviour of the software
verifiers we tested in Section 5. As we take the perspective of expert users in the course
of our experiments, the content of this appendix should not be seen as an attempt to
discover the root causes of the behaviour we observe. Instead, we report them here to
provide additional context around our experimental results.
• 2LS. This verifier clearly applies an explicit heuristic to detect maths functions.
  The heuristic quickly causes 2LS to return “unknown” as verdict. The output logs
  reveal the specific list of functions:
                  2ls-binary: preprocessing util.cpp:701:
                  void twols parse optionst::assert no unsupported function calls(goto modelt&):
                  Assertion ‘NOT MATH FUN(name, "cos") && NOT MATH FUN(name, "acos")
                  && NOT MATH FUN(name, "sin") && NOT MATH FUN(name, "asin") &&
                  NOT MATH FUN(name, "tan") && NOT MATH FUN(name, "atan") &&
                  NOT MATH FUN(name, "atan2") && NOT MATH FUN(name, "cosh") &&
                  NOT MATH FUN(name, "acosh") && NOT MATH FUN(name, "sinh") &&
                  NOT MATH FUN(name, "asinh") && NOT MATH FUN(name, "tanh") &&
                  NOT MATH FUN(name, "atanh") && NOT MATH FUN(name, "exp") &&
                  NOT MATH FUN(name, "exp2") && NOT MATH FUN(name, "expm1") &&
                  NOT MATH FUN(name, "log") && NOT MATH FUN(name, "log10") &&
                  NOT MATH FUN(name, "log2") && NOT MATH FUN(name, "log1p") &&
                  NOT MATH FUN(name, "erf")’ failed.
• CBMC. This verifier returns 121 incorrect unsafe results on NeuroCodeBench 2.0 as
  shown in Table 6. In contrast to all other verifiers except ESBMC, the tool produces
  a full counterexample trace for each unsafe verdict. By manual inspection, these
  traces tend to include zero and NaN values as inputs. Moreover, a large majority


                                                     40
  of incorrect results seems to be due to under-specified maths functions: the return
  value of most calls to math.h is a non-deterministic float, sometime restricted to
  a reasonable range (e.g. the output of cosf is restricted to [−1, 1]). At the same
  time, CBMC also returns incorrect unsafe verdicts for benchmarks that do not
  contain calls to math.h, as shown in Figure C1. Reproducing the corresponding
  counterexample traces yield output values that do not violate the network post-
  condition, thus confirming that they are spurious.
• CPAChecker. This verifier reports an error when processing some functions from
  the C standard. For instance, verification queries that contain calls to memset
  trigger the following log message:
    Error: line 11207: Unrecognized C code (Memory assignment
    function called but their handling is disabled. Set
    cpa.predicate.enableMemoryAssignmentFunctions=true
    to enable.): memset(C, 0, (outrows * outcols) * 4UL)
    (CExpressionVisitorWithPointerAliasing.visit, SEVERE)
  Similar error messages are returned for most maths functions, even when MUSL or
  CORE-MATH operational models are provided. For example, benchmark
  instances that rely on tanhf cause the following error:
    Error: line 2154: Unsupported feature (arithmetic function):
    tanhf(x) (line was originally float y = tanhf(x);)
    (ExpressionToFormulaVisitor.visit, SEVERE)
• DIVINE. Unfortunately, this verifier provides no information in the log files.
• ESBMC. This verifier internally uses a subset of the MUSL operational models [52],
  as we mention in Section 2.5. Interestingly, explicitly including the MUSL models
  as part of the benchmark causes 3 incorrect unsafe verdicts to appear (see Figure
  11e). Note that instances that do not contain maths functions do not cause this
  issue, as shown in Figure C2e. Since ESBMC produces full counterexample traces
  for its unsafe verdicts, we can run the three benchmark instances with the given
  concrete inputs. Doing so leads to outputs that do not violate the assertion, thus
  showing that the counterexamples are indeed spurious.
• PeSCo. This verifier throws the same errors as CPAChecker, except for the memset
  ones. For example, the below is a snippet taken verbatim from the output logs:
    Error: line 1129: Unsupported feature (arithmetic function):
    tanhf(x1) (line was originally float y1 = tanhf(x1);)
    (ExpressionToFormulaVisitor.visit, SEVERE)
• Pinaka. This verifier returns 82 incorrect unsafe results (see Table 6), but does not
  provide counterexample traces that we can inspect. Furthermore, the logs do not
  contain errors or warnings regarding the absence maths function support.
• UAutomizer. This verifier appears to process each benchmark instance in two
  stages: default analysis and bit-precise analysis. The first stage often fails due to
  the presence of basic floating point operations such as fabs, fmax, isnan and
  round. The following is an example from the output logs:
    ExceptionOrErrorResult: UnsupportedOperationException: floating point
    operation not supported in non-bitprecise translation: fabs



                                          41
 270                                                                              270                  247 247 248
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH
 180                                                                              180

 90                                                                               90    52   52   52
       10        9                                                                                                                           24   23   24
            0          2     0    2       0   0    0        0    0    0                                                    0   0    0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                                 (a) 2LS                                                                     (b) CBMC

 270                                                                              270
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH
 180                                                                              180

 90                                                                               90
       18   15   17    19   18    18      0   0    0        0    3    0                 6    0    0     3     0    0       0   0    0        0    0    0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                      (c) CPAChecker                                                                         (d) DIVINE

 270                                                                              270
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH
 180                                                                              180

 90    49   49   49    47   47    47                                              90
                                                                                        24   16   20    22    15   21     10   19   10
                                          0   0    0        0    0    0                                                                      0    4    0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                            (e) ESBMC                                                                        (f) PeSCo

 270                                                                              270
                                       None   MUSL       CORE-MATH                                                      None   MUSL       CORE-MATH
 180                                                                              180

 90                                                                               90
       30   39   29    31   31    31
                                          0   0    0        9    0    9                 6    0    0     18    0    0       0   0    0        11   0    0
   0                                                                                0
       Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe              Correct Safe   Correct Unsafe    Incorrect Safe    Incorrect Unsafe


                            (g) Pinaka                                                                 (h) UAutomizer

Fig. C2: Verifier performance on the 732 benchmark instances of NeuroCodeBench
2.0 without math.h functions.


  Then, the verifier tries again in bit-precise mode. From the phrasing of the log
  messages, we can infer that this mode must still involve some form of
  over-approximation. For example, a benchmark instance containing calls to tanhf
  may cause the following message:
        Unable to prove that a call to reach error is unreachable. Reason:
        overapproximation of tanhf at line 1129.

  When adding MUSL or CORE-MATH operational models, the analysis reaches
  the bit-precise stage but fails due to unsupported functions. This happens even
  for benchmarks where all mathematical operations could be sliced away, e.g. those
  containing only ReLU activation functions.
       For completeness, we report a full breakdown of the verifiers behaviour in Table
C1.




                                                                             42
Table C1: Detailed comparison of the verdicts returned by the verifiers on NeuroCodeBench 2.0
using 3 different operational model settings: None, MUSL, and CORE-MATH.
                                  Correct          Incorrect                   Inconclusive
   Verifier      Op. Models
                               True   False    True     False   Timeout   Out of Memory       Unknown   Error

                  None          12      2          -       -       4            -               894       -
     2LS         MUSL            -      -          -       -       -            -               912       -
               CORE-MATH        11      2          -       -       5            -               894       -

                  None          66     305         -     121       -           80                -      340
   CBMC          MUSL           75     279         -      25       -           90               30      413
               CORE-MATH        76     299         -      69       -           97               11      360

                  None          18      19         -       -      292          265               -      318
 CPAChecker      MUSL           18      28         -      17      392          264               -      193
               CORE-MATH        18      21         -       -      335          265               -      273

                  None           6      3          -       -      390          152              361       -
   DIVINE        MUSL            -      -          -       -       -            -               912       -
               CORE-MATH         -      -          -       -       -            -               912       -

                  None          76      86         -      -       539          211               -        -
   ESBMC         MUSL           67      80         -      3       551          211               -        -
               CORE-MATH        63      68         -      -       570          211               -        -

                  None          24      25         10      -      482          58                -      313
    PeSCo        MUSL           19      27         27     18      598          54                -      169
               CORE-MATH        21      27         10      -      541          60                -      253

                  None          44      71         -      82      243          292               -      180
    Pinaka       MUSL           59      64         -      5       305          293               -      186
               CORE-MATH        53      59         -      24      302          292               -      182

                  None           9      27         -      12      754           1               106      3
 UAutomizer      MUSL            -       -         -       -       -            -               912      -
               CORE-MATH         -       -         -       -       -            -               912      -



Appendix D              Time Distribution Graphs
In Figure D3, we report the cumulative distribution of the time it takes the verifiers to
produce a verdict. Specifically, we compare the distributions of correct, incorrect, and
inconclusive verdicts. The results show that almost the entirety of incorrect verdicts
(either safe or unsafe) are returned in the first few seconds of computation. In contrast,
correct verdicts are more uniformly spread across the 900 seconds of computation time.
As expected, more than half of the inconclusive verdicts are due to timeout, i.e. they
are close to the 900 second threshold. Still, almost a third happen in the first seconds
of computation, thus reinforcing our conclusion that many verifiers simply “reject” a
large number of benchmark instances (see also Appendix C).




                                              43
                           15%

                                                                         10.9%
                           10%




            Correct
                            5%



                            5%
                            4%
            Incorrect       3%                                           3.1%

                            2%
                            1%

                           100%
                                                                         86.0%
                           75%
            Inconclusive




                           50%

                           25%

                            0%
                                  0         300                  600   900
                                                  CPU Time (s)

Fig. D3: Cumulative distribution of the time taken by all verifiers to solve the Neu-
roCodeBench 2.0 benchmark. On the right, we report the overall percentage of correct,
incorrect, and inconclusive verdicts.


Appendix E                            Additional Information
This Appendix contains additional information that would not fit the main text of the
present paper:
• Historical Progress. Table E2 lists the data behind the historical comparison of
  different ESBMC versions in Figure 17
• Math Library Support. Table 5.3 reports the full list of functions from math.h that
  we use when filtering the relevant subset of NeuroCodeBench 2.0 in Section 5.3.
  Note that the table is conservative, i.e. it contains functions that NeuroCodeBench
  2.0 instances may not call, at least directly.


References
 [1] Bengio, Y., Mindermann, S., Privitera, D., Besiroglu, T., Bommasani, R., Casper,
     S., Choi, Y., Fox, P., Garfinkel, B., Goldfarb, D., et al.: International ai safety
     report. arXiv preprint arXiv:2501.17805 (2025)

 [2] Raji, I.D., Kumar, I.E., Horowitz, A., Selbst, A.: The fallacy of ai functional-
     ity. In: Proceedings of the 2022 ACM Conference on Fairness, Accountability,



                                                     44
   Table E2: Detailed comparison of different versions of ESBMC on Neu-
   roCodeBench 2.0, spanning the years 2018 to 2025.
               Correct        Incorrect                        Inconclusive
    Year
            True    False    True   False     Timeout    Out of Memory        Unknown   Error

    2018     83         27   10      73         301            342              76        -
    2019     113        57   34      89         393            226               -        -
    2020     114        52   34      89         394            227               2        -
    2021     119        92   34      81         359            227               -        -
    2022     350        71   234     81         159             17               -        -
    2023     345        91   210     85         69              16              96        -
    2024     76         86    -       -         539            211               -        -
    2025     134        97   10       -         459            212               -        -
    2026     59         55    -       -         798              -               -        -




Table E3: Full list of functions that we use to filter the 180 instances of NeuroCodeBench 2.0 in
Section 5.3.
                                            exp,expf,expl,exp2,exp2f,exp2l,expm1,expm1f,expm1l,
 Exponential functions
                                            log,logf,logl,log10,log10f,log10l,log2,log2f,log2l,log1p,log1pf,log1pl

 Power functions                            pow,powf,powl, sqrt,sqrtf,sqrtl, cbrt,cbrtf,cbrtl,hypot,hypotf,hypotl

                                            sin,sinf,sinl,cos,cosf,cosl,tan,tanf,tanl,
 Trigonometric functions
                                            asin,asinf,asinl,acos,acosf,acosl,atan,atanf,atanl,atan2,atan2f,atan2l

                                            sinh,sinhf,sinhl,cosh,coshf,coshl,tanh,tanhf,tanhl,
 Hyperbolic functions
                                            asinh,asinhf,asinhl,acosh,acoshf,acoshl,atanh,atanhf,atanhl

 Error functions                            erf,erff,erfl,erfc,erfcf,erfcl

 Gamma functions                            tgamma,tgammaf,tgammal,lgamma,lgammaf,lgammal

                                            frexp,frexpf,frexpl,ldexp,ldexpf,ldexpl,
 Floating-point manipulation functions      scalbn,scalbnf,scalbnl,scalbln,scalblnf,scalblnl,
                                            ilogb,ilogbf,ilogbl,logb,logbf,logbl



    and Transparency. FAccT ’22, pp. 959–972. Association for Computing Machin-
    ery, New York, NY, USA (2022). https://doi.org/10.1145/3531146.3533158 .
    https://doi.org/10.1145/3531146.3533158

 [3] Martı́nez, E.: Re-evaluating gpt-4’s bar exam performance. Artificial intelligence
     and law, 1–24 (2024) https://doi.org/10.1007/s10506-024-09396-9

 [4] Szegedy, C., Zaremba, W., Sutskever, I., Bruna, J., Erhan, D., Goodfellow, I.,
     Fergus, R.: Intriguing Properties of Neural Networks. In: 2nd International Con-
     ference on Learning Representations, ICLR 2014 ; Conference Date: 14-04-2014


                                                 45
    Through 16-04-2014 (2014). https://arxiv.org/pdf/1312.6199

 [5] Casper, S., Bu, T., Li, Y., Li, J., Zhang, K., Hariharan, K., Hadfield-
     Menell, D.: Red teaming deep neural networks with feature synthesis
     tools. In: Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt,
     M., Levine, S. (eds.) Advances in Neural Information Processing Sys-
     tems, vol. 36, pp. 80470–80516. Curran Associates, Inc., ??? (2023).
     https://proceedings.neurips.cc/paper files/paper/2023/file/febe5c5c6973f713cc43bf0f7c90edbe-
     Paper-Conference.pdf

 [6] Huang, X., Kroening, D., Ruan, W., Sharp, J., Sun, Y., Thamo, E., Wu, M., Yi,
     X.: A survey of safety and trustworthiness of deep neural networks: Verification,
     testing, adversarial attack and defence, and interpretability. Computer Science
     Review 37, 100270 (2020) https://doi.org/10.1016/j.cosrev.2020.100270

 [7] Yang, J., Zhou, K., Li, Y., Liu, Z.: Generalized out-of-distribution detection:
     A survey. International Journal of Computer Vision 132(12), 5635–5662 (2024)
     https://doi.org/10.1007/s11263-024-02117-4

 [8] Perez-Cerrolaza, J., Abella, J., Borg, M., Donzella, C., Cerquides, J., Cazorla,
     F.J., Englund, C., Tauber, M., Nikolakopoulos, G., Flores, J.L.: Artificial intel-
     ligence for safety-critical systems in industrial and transportation domains: A
     survey. ACM Comput. Surv. 56(7) (2024) https://doi.org/10.1145/3626314

 [9] Katz, G., Barrett, C., Dill, D.L., Julian, K., Kochenderfer, M.J.: Reluplex: An
     Efficient SMT Solver for Verifying Deep Neural Networks. In: Majumdar, R.,
     Kunčak, V. (eds.) Computer Aided Verification, pp. 97–117. Springer, Cham
     (2017). https://doi.org/10.1007/978-3-319-63387-9 5

[10] Brix, C., Bak, S., Johnson, T.T., Wu, H.: The Fifth International Verification of
     Neural Networks Competition (VNN-COMP 2024): Summary and Results (2024).
     https://arxiv.org/abs/2412.19985

[11] Teuber, S., Büning, M.K., Kern, P., Sinz, C.: Geometric path enumeration for
     equivalence verification of neural networks. In: 2021 IEEE 33rd International
     Conference on Tools with Artificial Intelligence (ICTAI), pp. 200–208 (2021).
     https://doi.org/10.1109/ICTAI52525.2021.00035

[12] Athavale, A., Bartocci, E., Christakis, M., Maffei, M., Nickovic, D., Weis-
     senbacher, G.: Verifying global two-safety properties in neural networks with
     confidence. In: Gurfinkel, A., Ganesh, V. (eds.) Computer Aided Verification, pp.
     329–351. Springer, Cham (2024). https://doi.org/10.1007/978-3-031-65630-9 17

[13] Shi, Z., Zhang, H., Chang, K.-W., Huang, M., Hsieh, C.-J.: Robustness verifica-
     tion for transformers. In: International Conference on Learning Representations
     (2020). https://openreview.net/forum?id=BJxwPJHFwS



                                          46
[14] Casadio, M., Dinkar, T., Komendantskaya, E., Arnaboldi, L., Daggitt, M.L., Isac,
     O., Katz, G., Rieser, V., Lemon, O.: Nlp verification: towards a general method-
     ology for certifying robustness. European Journal of Applied Mathematics, 1–58
     (2025) https://doi.org/10.1017/S0956792525000099

[15] Ivanov, R., Carpenter, T., Weimer, J., Alur, R., Pappas, G., Lee, I.: Verisig 2.0:
     Verification of neural network controllers using taylor model preconditioning.
     In: Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification, pp. 249–262.
     Springer, Cham (2021). https://doi.org/10.1007/978-3-030-81685-8 11

[16] Huang, C., Fan, J., Chen, X., Li, W., Zhu, Q.: Polar: A polynomial arithmetic
     framework for verifying neural-network controlled systems. In: Bouajjani, A.,
     Holı́k, L., Wu, Z. (eds.) Automated Technology for Verification and Analysis, pp.
     414–430. Springer, Cham (2022). https://doi.org/10.1007/978-3-031-19992-9 27

[17] Schlögl, A., Hofer, N., Böhme, R.: Causes and effects of unantici-
     pated numerical deviations in neural network inference frameworks.
     In: Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt, M.,
     Levine, S. (eds.) Advances in Neural Information Processing Sys-
     tems, vol. 36, pp. 56095–56107. Curran Associates, Inc., ??? (2023).
     https://proceedings.neurips.cc/paper files/paper/2023/file/af076c3bdbf935b81d808e37c5ede463-
     Paper-Conference.pdf

[18] Abate, A., Bessa, I., Cattaruzza, D., Cordeiro, L., David, C., Kesseli, P., Kroen-
     ing, D., Polgreen, E.: Automated formal synthesis of digital controllers for
     state-space physical plants. In: Majumdar, R., Kunčak, V. (eds.) Computer
     Aided Verification, pp. 462–482. Springer, Cham (2017). https://doi.org/10.1007/
     978-3-319-63387-9 23

[19] Lions, J.-L., et al.: ARIANE 5: Flight 501 failure. Report by the Inquiry Board
     190 (1996)

[20] Office, U.G.A.: Patriot missile defense: Software problem led to system failure at
     dhahran, saudi arabia (GAO/IMTEC-92-26) (1992)

[21] Cordeiro, L., Daggitt, M., Girard-Satabin, J., Isac, O., Johnson, T., Katz, G.,
     Komendantskaya, E., Lemesle, A., Manino, E., Šinkarovs, A., Wu, H.: Neural net-
     work verification is a programming language challenge. In: 34th European Sym-
     posium on Programming (2025). https://doi.org/10.1007/978-3-031-91118-7 9

[22] Jia, K., Rinard, M.: Exploiting verified neural networks via floating point numer-
     ical error. In: Drăgoi, C., Mukherjee, S., Namjoshi, K. (eds.) Static Analysis,
     pp. 191–205. Springer, Cham (2021). https://dl.acm.org/doi/10.1007/978-3-030-
     88806-0 9

[23] Szász, A., Bánhelyi, B., Jelasity, M.: No soundness in the real world:
     On the challenges of the verification of deployed neural networks. In:


                                          47
    Forty-second International Conference on             Machine     Learning    (2025).
    https://openreview.net/forum?id=c16m2kUTLZ

[24] Chudnov, A., Collins, N., Cook, B., Dodds, J., Huffman, B., MacCárthaigh,
     C., Magill, S., Mertens, E., Mullen, E., Tasiran, S., Tomb, A., Westbrook, E.:
     Continuous formal verification of amazon s2n. In: Chockler, H., Weissenbacher,
     G. (eds.) Computer Aided Verification, pp. 430–446. Springer, Cham (2018).
     https://doi.org/10.1007/978-3-319-96142-2 26

[25] Fox, A.C.J., Stockwell, G., Xiong, S., Becker, H., Mulligan, D.P., Petri, G., Chong,
     N.: A verification methodology for the arm® confidential computing architecture:
     From a secure specification to safe implementations. Proc. ACM Program. Lang.
     7(OOPSLA1) (2023) https://doi.org/10.1145/3586040

[26] Matos, J.B.P., Lima Filho, E.B., Bessa, I., Manino, E., Song, X., Cordeiro, L.C.:
     Counterexample guided neural network quantization refinement. IEEE Trans-
     actions on Computer-Aided Design of Integrated Circuits and Systems 43(4),
     1121–1134 (2024) https://doi.org/10.1109/TCAD.2023.3335313

[27] Magalhães, J.W.d.S., Woodruff, J., Polgreen, E., O’Boyle, M.F.P.: C2taco:
     Lifting tensor code to taco. In: Proceedings of the 22nd ACM SIG-
     PLAN International Conference on Generative Programming: Concepts and
     Experiences. GPCE 2023, pp. 42–56. Association for Computing Machin-
     ery, New York, NY, USA (2023). https://doi.org/10.1145/3624007.3624053 .
     https://doi.org/10.1145/3624007.3624053

[28] Manino, E., Menezes, R.S., Shmarov, F., Cordeiro, L.C.: NeuroCodeBench:
     a Plain C Neural Network Benchmark for Software Verification. In: Work-
     shop on Automated Formal Reasoning for Trustworthy AI Systems (2023).
     https://arxiv.org/pdf/2309.03617

[29] Cadar, C., Donaldson, A.F.: Analysing the program analyser. In: Pro-
     ceedings of the 38th International Conference on Software Engineering
     Companion. ICSE ’16, pp. 765–768. Association for Computing Machin-
     ery, New York, NY, USA (2016). https://doi.org/10.1145/2889160.2889206 .
     https://doi.org/10.1145/2889160.2889206

[30] Zhang, C., Su, T., Yan, Y., Zhang, F., Pu, G., Su, Z.: Finding and understanding
     bugs in software model checkers. In: Proceedings of the 2019 27th ACM Joint
     Meeting on European Software Engineering Conference and Symposium on the
     Foundations of Software Engineering. ESEC/FSE 2019, pp. 763–773. Association
     for Computing Machinery, New York, NY, USA (2019). https://doi.org/10.1145/
     3338906.3338932 . https://doi.org/10.1145/3338906.3338932

[31] Dyck, F., Richter, C., Wehrheim, H.: Robustness testing of software verifiers. In:
     Ferreira, C., Willemse, T.A.C. (eds.) Software Engineering and Formal Methods,
     pp. 66–84. Springer, Cham (2023). https://doi.org/10.1007/978-3-031-47115-5 5


                                           48
[32] Beyer, D.: State of the art in software verification and witness validation: Sv-comp
     2024. In: International Conference on Tools and Algorithms for the Construc-
     tion and Analysis of Systems, pp. 299–329 (2024). https://doi.org/10.1007/
     978-3-031-57256-2 15 . Springer

[33] Beyer, D., Löwe, S., Wendler, P.: Reliable benchmarking: requirements and solu-
     tions. International Journal on Software Tools for Technology Transfer 21(1),
     1–29 (2019) https://doi.org/10.1007/s10009-017-0469-y

[34] Bishop, C.M., Nasrabadi, N.M.: Pattern Recognition and Machine Learning vol.
     4. Springer, ??? (2006). https://link.springer.com/book/9780387310732

[35] Elsken, T., Metzen, J.H., Hutter, F.: Neural architecture search: A survey. Journal
     of Machine Learning Research 20(55), 1–21 (2019)

[36] Bardenet, R., Brendel, M., Kégl, B., Sebag, M.: Collaborative hyperparame-
     ter tuning. In: Dasgupta, S., McAllester, D. (eds.) Proceedings of the 30th
     International Conference on Machine Learning. Proceedings of Machine Learn-
     ing Research, vol. 28, pp. 199–207. PMLR, Atlanta, Georgia, USA (2013).
     https://proceedings.mlr.press/v28/bardenet13.html

[37] Singh, G., Gehr, T., Püschel, M., Vechev, M.: Robustness certification with
     refinement. In: International Conference on Learning Representations (2019).
     https://openreview.net/forum?id=HJgeEh09KQ

[38] Wu, H., Isac, O., Zeljić, A., Tagomori, T., Daggitt, M., Kokke, W., Refaeli, I.,
     Amir, G., Julian, K., Bassan, S., et al.: Marabou 2.0: a versatile formal analyzer
     of neural networks. In: International Conference on Computer Aided Verification,
     pp. 249–264 (2024). https://doi.org/10.1007/978-3-031-65630-9 13 . Springer

[39] Bak, S.: nnenum: Verification of relu neural networks with optimized abstraction
     refinement. In: NASA Formal Methods Symposium, pp. 19–36 (2021). https://
     doi.org/10.1007/978-3-030-76384-8 2 . Springer

[40] Xu, K., Shi, Z., Zhang, H., Wang, Y., Chang, K.-W., Huang, M., Kailkhura,
     B., Lin, X., Hsieh, C.-J.: Automatic perturbation analysis for scalable certified
     robustness and beyond. Advances in Neural Information Processing Systems 33,
     1129–1141 (2020)

[41] Xu, K., Zhang, H., Wang, S., Wang, Y., Jana, S., Lin, X., Hsieh, C.-J.: Fast
     and complete: Enabling complete neural network verification with rapid and
     massively parallel incomplete verifiers. In: International Conference on Learning
     Representations (2021). https://openreview.net/forum?id=nVZtXBI6LNn

[42] IEEE: Ieee standard for floating-point arithmetic. IEEE Std 754-2019 (Revision of
     IEEE 754-2008), 1–84 (2019) https://doi.org/10.1109/IEEESTD.2019.8766229



                                           49
[43] Google: Improve your model’s performance with bfloat16. Retrieved 2025-02-08.
     https://cloud.google.com/tpu/docs/bfloat16 Accessed 2025-02-08

[44] Micikevicius, P., Stosic, D., Burgess, N., Cornea, M., Dubey, P., Grisenthwaite,
     R., Ha, S., Heinecke, A., Judd, P., Kamalu, J., Mellempudi, N., Oberman, S.,
     Shoeybi, M., Siu, M., Wu, H.: FP8 Formats for Deep Learning (2022). https:
     //arxiv.org/abs/2209.05433

[45] Shanmugavelu, S., Taillefumier, M., Culver, C., Hernandez, O., Coletti, M.,
     Sedova, A.: Impacts of floating-point non-associativity on reproducibility for hpc
     and deep learning applications. In: SC24-W: Workshops of the International Con-
     ference for High Performance Computing, Networking, Storage and Analysis, pp.
     170–179 (2024). https://doi.org/10.1109/SCW63240.2024.00028

[46] Lavin, A., Gray, S.: Fast algorithms for convolutional neural networks. In: Pro-
     ceedings of the IEEE Conference on Computer Vision and Pattern Recognition
     (CVPR) (2016). https://doi.org/10.1109/CVPR.2016.435

[47] Pratt, H., Williams, B., Coenen, F., Zheng, Y.: Fcnn: Fourier convolutional neural
     networks. In: Ceci, M., Hollmén, J., Todorovski, L., Vens, C., Džeroski, S. (eds.)
     Machine Learning and Knowledge Discovery in Databases, pp. 786–798. Springer,
     Cham (2017). https://doi.org/10.1007/978-3-319-71249-9 47

[48] Jajal, P., Jiang, W., Tewari, A., Kocinare, E., Woo, J., Sarraf, A., Lu, Y.-
     H., Thiruvathukal, G.K., Davis, J.C.: Interoperability in deep learning: A
     user survey and failure analysis of onnx model converters. In: Proceedings
     of the 33rd ACM SIGSOFT International Symposium on Software Testing
     and Analysis. ISSTA 2024, pp. 1466–1478. Association for Computing Machin-
     ery, New York, NY, USA (2024). https://doi.org/10.1145/3650212.3680374 .
     https://doi.org/10.1145/3650212.3680374

[49] Rice, H.G.: Classes of recursively enumerable sets and their decision problems.
     Transactions of the American Mathematical society 74(2), 358–366 (1953)

[50] Brain, M., Polgreen, E.: A pyramid of (formal) software verification. In: Platzer,
     A., Rozier, K.Y., Pradella, M., Rossi, M. (eds.) Formal Methods, pp. 393–419.
     Springer, Cham (2025). https://doi.org/10.1007/978-3-031-71177-0 24

[51] Kroening, D., Tautschnig, M.: Cbmc – c bounded model checker. In: Ábrahám,
     E., Havelund, K. (eds.) Tools and Algorithms for the Construction and Analysis
     of Systems, pp. 389–391. Springer, Berlin, Heidelberg (2014). https://doi.org/10.
     1007/978-3-642-54862-8 26

[52] Menezes, R.S., Aldughaim, M., Farias, B., Li, X., Manino, E., Shmarov, F., Song,
     K., Brauße, F., Gadelha, M.R., Tihanyi, N., Korovin, K., Cordeiro, L.C.: Esbmc
     v7.4: Harnessing the power of intervals. In: Finkbeiner, B., Kovács, L. (eds.)
     Tools and Algorithms for the Construction and Analysis of Systems, pp. 376–380.


                                           50
    Springer, Cham (2024). https://doi.org/10.1007/978-3-031-57256-2 24

[53] Baier, D., Beyer, D., Chien, P.-C., Jankola, M., Kettl, M., Lee, N.-Z., Lemberger,
     T., Lingsch-Rosenfeld, M., Spiessl, M., Wachowitz, H., Wendler, P.: Cpachecker
     2.3 with strategy selection. In: Finkbeiner, B., Kovács, L. (eds.) Tools and Algo-
     rithms for the Construction and Analysis of Systems, pp. 359–364. Springer,
     Cham (2024). https://doi.org/10.1007/978-3-031-57256-2 21

[54] Cadar, C., Dunbar, D., Engler, D.: Klee: unassisted and automatic gen-
     eration of high-coverage tests for complex systems programs. In: Proceed-
     ings of the 8th USENIX Conference on Operating Systems Design and
     Implementation. OSDI’08, pp. 209–224. USENIX Association, USA (2008).
     https://dl.acm.org/doi/10.5555/1855741.1855756

[55] Brisebarre, N., Hanrot, G., Muller, J.-M., Zimmermann, P.: Correctly-rounded
     evaluation of a function: why, how, and at what cost? (2024). https://hal.science/
     hal-04474530/document

[56] Volder, J.E.: The cordic trigonometric computing technique. IRE Transactions on
     Electronic Computers EC-8(3), 330–334 (1959) https://doi.org/10.1109/TEC.
     1959.5222693

[57] Bajard, J.-C., Kla, S., Muller, J.-M.: Bkm: a new hardware algorithm for complex
     elementary functions. IEEE Transactions on Computers 43(8), 955–963 (1994)
     https://doi.org/10.1109/12.295857

[58] Ziv, A.: Fast evaluation of elementary mathematical functions with correctly
     rounded last bit. ACM Trans. Math. Softw. 17(3), 410–423 (1991) https://doi.
     org/10.1145/114697.116813

[59] Beebe, N.H.F.: Improving upon the Cody/Waite algorithms, pp. 823–
     828. Springer, Cham (2017). https://doi.org/10.1007/978-3-319-64110-2 25 .
     https://doi.org/10.1007/978-3-319-64110-2 25

[60] Daramy-Loirat, C., Defour, D., Dinechin, F., Gallet, M., Gast, N., Muller, J.-
     M.: CR-LIBM: A library of correctly rounded elementary functions in double-
     precision. Research Report LIP (2006). https://hal-ens-lyon.archives-ouvertes.fr/
     ensl-01529804

[61] Sibidanov, A., Zimmermann, P., Glondu, S.: The core-math project. In: 2022
     IEEE 29th Symposium on Computer Arithmetic (ARITH), pp. 26–34 (2022).
     https://doi.org/10.1109/ARITH54963.2022.00014

[62] Dinechin, F., Lauter, C., Melquiond, G.: Certifying the floating-point implemen-
     tation of an elementary function using gappa. IEEE Transactions on Computers
     60(2), 242–253 (2011) https://doi.org/10.1109/TC.2010.128



                                          51
[63] Martin-Dorel, É., Hanrot, G., Mayero, M., Théry, L.: Formally verified certificate
     checkers for hardest-to-round computation. Journal of Automated Reasoning 54,
     1–29 (2015) https://doi.org/10.1007/s10817-014-9312-2

[64] Henzinger, T.A., Lechner, M., Žikelić, D.o.e.: Scalable verification of quantized
     neural networks. Proceedings of the AAAI Conference on Artificial Intelligence
     35(5), 3787–3795 (2021) https://doi.org/10.1609/aaai.v35i5.16496

[65] Banbury, C., Zhou, C., Fedorov, I., Matas, R., Thakker, U., Gope,
     D., Janapa Reddi, V., Mattina, M., Whatmough, P.: Micronets: Neu-
     ral network architectures for deploying tinyml applications on commodity
     microcontrollers. In: Smola, A., Dimakis, A., Stoica, I. (eds.) Proceed-
     ings of Machine Learning and Systems, vol. 3, pp. 517–532 (2021).
     https://proceedings.mlsys.org/paper files/paper/2021/file/c4d41d9619462c534b7b61d1f772385e-
     Paper.pdf

[66] Saha, S.S., Sandha, S.S., Srivastava, M.: Machine learning for microcontroller-
     class hardware: A review. IEEE Sensors Journal 22(22), 21362–21390 (2022)
     https://doi.org/10.1109/JSEN.2022.3210773

[67] Likhomanenko, T., Xu, Q., Synnaeve, G., Collobert, R., Rogozhnikov,
     A.: Cape: Encoding relative positions with continuous augmented posi-
     tional embeddings. In: Ranzato, M., Beygelzimer, A., Dauphin, Y., Liang,
     P.S., Vaughan, J.W. (eds.) Advances in Neural Information Processing
     Systems, vol. 34, pp. 16079–16092. Curran Associates, Inc., ??? (2021).
     https://proceedings.neurips.cc/paper files/paper/2021/file/865bf46435bd84fa5d89f64cf3ba7347-
     Paper.pdf

[68] Nwankpa, C.E., Ijomah, W., Gachagan, A., Marshall, S.: Activation functions :
     comparison of trends in practice and research for deep learning. In: 2nd Interna-
     tional Conference on Computational Sciences and Technology, PAK, pp. 124–133
     (2021). https://strathprints.strath.ac.uk/75897/

[69] Hendrycks, D., Gimpel, K.: Gaussian Error Linear Units (GELUs) (2023). https:
     //arxiv.org/abs/1606.08415

[70] Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M.W., Keutzer, K.: A
     survey of quantization methods for efficient neural network inference. In: Low-
     power Computer Vision, pp. 291–326. Chapman and Hall/CRC, ??? (2022).
     https://www.taylorfrancis.com/chapters/edit/10.1201/9781003162810-13/survey-
     quantization-methods-efficient-neural-network-inference-amir-gholami-sehoon-kim-
     zhen-dong-zhewei-yao-michael-mahoney-kurt-keutzer

[71] Santurkar, S., Tsipras, D., Ilyas, A., Madry, A.: How does batch nor-
     malization help optimization? In: Bengio, S., Wallach, H., Larochelle, H.,
     Grauman, K., Cesa-Bianchi, N., Garnett, R. (eds.) Advances in Neural Infor-
     mation Processing Systems, vol. 31. Curran Associates, Inc., ??? (2018).


                                           52
    https://proceedings.neurips.cc/paper files/paper/2018/file/905056c1ac1dad141560467e0a99e1cf-
    Paper.pdf

[72] Ioffe, S., Szegedy, C.: Batch normalization: Accelerating deep network training
     by reducing internal covariate shift. In: Bach, F., Blei, D. (eds.) Proceedings
     of the 32nd International Conference on Machine Learning. Proceedings of
     Machine Learning Research, vol. 37, pp. 448–456. PMLR, Lille, France (2015).
     https://proceedings.mlr.press/v37/ioffe15.html

[73] Ba, J.L., Kiros, J.R., Hinton, G.E.: Layer normalization. arXiv preprint
     arXiv:1607.06450 (2016)

[74] Scherer, D., Müller, A., Behnke, S.: Evaluation of pooling operations in convolu-
     tional architectures for object recognition. In: Diamantaras, K., Duch, W., Iliadis,
     L.S. (eds.) Artificial Neural Networks – ICANN 2010, pp. 92–101. Springer, Berlin,
     Heidelberg (2010). https://doi.org/10.1007/978-3-642-15825-4 10

[75] Abu-Mostafa, Y., St. Jacques, J.: Information capacity of the hopfield model.
     IEEE Transactions on Information Theory 31(4), 461–464 (1985) https://doi.
     org/10.1109/TIT.1985.1057069

[76] Chaudhuri, R., Fiete, I.: Bipartite expander hopfield networks as self-decoding
     high-capacity error correcting codes. In: Wallach, H., Larochelle, H., Beygelz-
     imer, A., Alché-Buc, F., Fox, E., Garnett, R. (eds.) Advances in Neural
     Information Processing Systems, vol. 32. Curran Associates, Inc., ??? (2019).
     https://proceedings.neurips.cc/paper files/paper/2019/file/97008ea27052082be055447be9e85612-
     Paper.pdf

[77] Conlin, R., Erickson, K., Abbate, J., Kolemen, E.: Keras2c: A library for con-
     verting keras neural networks to real-time compatible c. Engineering Applications
     of Artificial Intelligence 100, 104182 (2021) https://doi.org/10.1016/j.engappai.
     2021.104182

[78] Xu, J., Yagoub, M.C.E., Ding, R., Zhang, Q.-J.: Neural-based dynamic model-
     ing of nonlinear microwave circuits. IEEE Transactions on Microwave Theory
     and Techniques 50(12), 2769–2780 (2002) https://doi.org/10.1109/TMTT.2002.
     805192

[79] Massi, O., Mezza, A.I., Giampiccolo, R., Bernardini, A.: Deep learning-based
     wave digital modeling of rate-dependent hysteretic nonlinearities for virtual ana-
     log applications. EURASIP Journal on Audio, Speech, and Music Processing
     2023(1), 12 (2023) https://doi.org/10.1186/s13636-023-00277-8

[80] Huang, P., Wu, H., Yang, Y., Daukantas, I., Wu, M., Zhang, Y., Barrett, C.:
     Towards efficient verification of quantized neural networks. In: Proceedings of
     the AAAI Conference on Artificial Intelligence, vol. 38, pp. 21152–21160 (2024).
     https://dl.acm.org/doi/10.1609/aaai.v38i19.30108


                                           53
[81] Biggio, B., Corona, I., Maiorca, D., Nelson, B., Šrndić, N., Laskov, P., Giacinto,
     G., Roli, F.: Evasion attacks against machine learning at test time. In: Blockeel,
     H., Kersting, K., Nijssen, S., Železný, F. (eds.) Machine Learning and Knowledge
     Discovery in Databases, pp. 387–402. Springer, Berlin, Heidelberg (2013). https:
     //doi.org/10.1007/978-3-642-40994-3 25

[82] Tsuzuku, Y., Sato, I., Sugiyama, M.: Lipschitz-margin training:
     Scalable certification of perturbation invariance for deep neural net-
     works. In: Bengio, S., Wallach, H., Larochelle, H., Grauman, K.,
     Cesa-Bianchi, N., Garnett, R. (eds.) Advances in Neural Informa-
     tion Processing Systems, vol. 31. Curran Associates, Inc., ??? (2018).
     https://proceedings.neurips.cc/paper files/paper/2018/file/485843481a7edacbfce101ecb1e4d2a8-
     Paper.pdf

[83] Cohen, J., Rosenfeld, E., Kolter, Z.: Certified adversarial robustness via ran-
     domized smoothing. In: Chaudhuri, K., Salakhutdinov, R. (eds.) Proceed-
     ings of the 36th International Conference on Machine Learning. Proceedings
     of Machine Learning Research, vol. 97, pp. 1310–1320. PMLR, ??? (2019).
     https://proceedings.mlr.press/v97/cohen19c.html

[84] Zhang, B., Jiang, D., He, D., Wang, L.: Rethinking lipschitz neural networks and
     certified robustness: A boolean function perspective. In: Koyejo, S., Mohamed, S.,
     Agarwal, A., Belgrave, D., Cho, K., Oh, A. (eds.) Advances in Neural Information
     Processing Systems, vol. 35, pp. 19398–19413. Curran Associates, Inc., ??? (2022).
     https://proceedings.neurips.cc/paper files/paper/2022/file/7b04ec5f2b89d7f601382c422dfe07af-
     Paper-Conference.pdf

[85] Araujo, A., Havens, A.J., Delattre, B., Allauzen, A., Hu, B.: A
     unified algebraic perspective on lipschitz neural networks. In: The
     Eleventh International Conference on Learning Representations (2023).
     https://openreview.net/forum?id=k71IGLC8cfc

[86] Müller, M.N., Brix, C., Bak, S., Liu, C., Johnson, T.T.: The Third International
     Verification of Neural Networks Competition (VNN-COMP 2022): Summary and
     Results (2023). https://arxiv.org/abs/2212.10376

[87] Meng, Y., Sun, D., Qiu, Z., Waez, M.T.B., Fan, C.: Learning density distri-
     bution of reachable states for autonomous systems. In: Faust, A., Hsu, D.,
     Neumann, G. (eds.) Proceedings of the 5th Conference on Robot Learning. Pro-
     ceedings of Machine Learning Research, vol. 164, pp. 124–136. PMLR, ??? (2022).
     https://proceedings.mlr.press/v164/meng22a.html

[88] Ravaioli, U.J., Cunningham, J., McCarroll, J., Gangal, V., Dunlap, K., Hobbs,
     K.L.: Safe reinforcement learning benchmark environments for aerospace control
     systems. In: 2022 IEEE Aerospace Conference (AERO), pp. 1–20 (2022). https:
     //doi.org/10.1109/AERO53065.2022.9843750



                                           54
[89] SQLite: The SQLite Amalgamation — sqlite.org. Retrieved 2025-06-27. https:
     //sqlite.org/amalgamation.html Accessed 2025-06-27

[90] Malı́k, V., Martiček, Š., Schrammel, P., Srivas, M., Vojnar, T., Wahlang, J.: 2ls:
     Memory safety and non-termination. In: Beyer, D., Huisman, M. (eds.) Tools and
     Algorithms for the Construction and Analysis of Systems, pp. 417–421. Springer,
     Cham (2018). https://doi.org/10.1007/978-3-319-89963-3 24

[91] Baranová, Z., Barnat, J., Kejstová, K., Kučera, T., Lauko, H., Mrázek, J., Ročkai,
     P., Štill, V.: Model checking of c and c++ with divine 4. In: D’Souza, D.,
     Narayan Kumar, K. (eds.) Automated Technology for Verification and Analysis,
     pp. 201–207. Springer, Cham (2017). https://doi.org/10.1007/978-3-319-68167-2
     14

[92] Richter, C., Wehrheim, H.: Pesco: Predicting sequential combinations of verifiers.
     In: Beyer, D., Huisman, M., Kordon, F., Steffen, B. (eds.) Tools and Algorithms
     for the Construction and Analysis of Systems, pp. 229–233. Springer, Cham
     (2019). https://doi.org/10.1007/978-3-030-17502-3 19

[93] Chaudhary, E., Joshi, S.: Pinaka: Symbolic execution meets incremental solving.
     In: Beyer, D., Huisman, M., Kordon, F., Steffen, B. (eds.) Tools and Algorithms
     for the Construction and Analysis of Systems, pp. 234–238. Springer, Cham
     (2019). https://doi.org/10.1007/978-3-030-17502-3 20

[94] Heizmann, M., Christ, J., Dietsch, D., Ermis, E., Hoenicke, J., Lindenmann, M.,
     Nutz, A., Schilling, C., Podelski, A.: Ultimate automizer with smtinterpol. In:
     Piterman, N., Smolka, S.A. (eds.) Tools and Algorithms for the Construction
     and Analysis of Systems, pp. 641–643. Springer, Berlin, Heidelberg (2013). https:
     //doi.org/10.1007/978-3-642-36742-7 53

[95] ISO: Iso c standard 1999. Technical report, ISO (1999). ISO/IEC 9899:1999 draft.
     http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf

[96] Cody, W.J.: Implementation and testing of function software. In: Messina,
     P.C., Murli, A. (eds.) Problems and Methodologies in Mathematical
     Software Production, pp. 24–47. Springer, Berlin, Heidelberg (1982).
     https://dl.acm.org/doi/10.5555/648091.747640




                                            55
