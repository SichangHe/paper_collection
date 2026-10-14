                                                   Learning Nonlinear Loop Invariants with Gated
                                                   Continuous Logic Networks (Extended Version)
                                                             Jianan Yao∗                                           Gabriel Ryan∗                              Justin Wong∗
                                                    Columbia University, USA                                Columbia University, USA                    Columbia University, USA
                                                     jianan@cs.columbia.edu                                  gabe@cs.columbia.edu                      justin.wong@columbia.edu

                                                                                         Suman Jana                                     Ronghui Gu
                                                                                Columbia University, USA                      Columbia University, CertiK, USA
                                                                                suman@cs.columbia.edu                              rgu@cs.columbia.edu
arXiv:2003.07959v4 [cs.SE] 25 Jun 2020




                                         Abstract                                                                             nonlinear loop invariants and show it solves 26 out of 27
                                         Verifying real-world programs often requires inferring loop                          problems, 3 more than prior work, with an average runtime
                                         invariants with nonlinear constraints. This is especially true                       of 53.3 seconds. We further demonstrate the generic learning
                                         in programs that perform many numerical operations, such                             ability of G-CLNs by solving all 124 problems in the linear
                                         as control systems for avionics or industrial plants. Recently,                      Code2Inv benchmark. We also perform a quantitative stabil-
                                         data-driven methods for loop invariant inference have shown                          ity evaluation and show G-CLNs have a convergence rate
                                         promise, especially on linear loop invariants. However, ap-                          of 97.5% on quadratic problems, a 39.2% improvement over
                                         plying data-driven inference to nonlinear loop invariants is                         CLN models.
                                         challenging due to the large numbers of and large magni-
                                         tudes of high-order terms, the potential for overfitting on                          CCS Concepts: • Software and its engineering → Soft-
                                         a small number of samples, and the large space of possible                           ware verification; • Computing methodologies → Neu-
                                         nonlinear inequality bounds.                                                         ral networks.
                                            In this paper, we introduce a new neural architecture for
                                         general SMT learning, the Gated Continuous Logic Network                             Keywords: Loop Invariant Inference, Program Verification,
                                         (G-CLN), and apply it to nonlinear loop invariant learning.                          Continuous Logic Networks
                                         G-CLNs extend the Continuous Logic Network (CLN) archi-
                                         tecture with gating units and dropout, which allow the model                         ACM Reference Format:
                                         to robustly learn general invariants over large numbers of                           Jianan Yao, Gabriel Ryan, Justin Wong, Suman Jana, and Ronghui
                                         terms. To address overfitting that arises from finite program                        Gu. 2020. Learning Nonlinear Loop Invariants with Gated Continu-
                                                                                                                              ous Logic Networks (Extended Version). In Proceedings of the 41st
                                         sampling, we introduce fractional sampling—a sound relax-
                                                                                                                              ACM SIGPLAN International Conference on Programming Language
                                         ation of loop semantics to continuous functions that facili-
                                                                                                                              Design and Implementation (PLDI ’20), June 15–20, 2020, London,
                                         tates unbounded sampling on the real domain. We addition-                            UK. ACM, New York, NY, USA, 16 pages. https://doi.org/10.1145/
                                         ally design a new CLN activation function, the Piecewise                             3385412.3385986
                                         Biased Quadratic Unit (PBQU), for naturally learning tight
                                         inequality bounds.
                                            We incorporate these methods into a nonlinear loop in-
                                         variant inference system that can learn general nonlinear                            1   Introduction
                                         loop invariants. We evaluate our system on a benchmark of                            Formal verification provides techniques for proving the cor-
                                         ∗ Equal contribution                                                                 rectness of programs, thereby eliminating entire classes of
                                                                                                                              critical bugs. While many operations can be verified auto-
                                         Permission to make digital or hard copies of all or part of this work for            matically, verifying programs with loops usually requires
                                         personal or classroom use is granted without fee provided that copies                inferring a sufficiently strong loop invariant, which is unde-
                                         are not made or distributed for profit or commercial advantage and that
                                         copies bear this notice and the full citation on the first page. Copyrights          cidable in general [5, 10, 15]. Invariant inference systems are
                                         for components of this work owned by others than the author(s) must                  therefore based on heuristics that work well for loops that ap-
                                         be honored. Abstracting with credit is permitted. To copy otherwise, or              pear in practice. Data-driven loop invariant inference is one
                                         republish, to post on servers or to redistribute to lists, requires prior specific   approach that has shown significant promise, especially for
                                         permission and/or a fee. Request permissions from permissions@acm.org.               learning linear invariants [30, 35, 39]. Data-driven inference
                                         PLDI ’20, June 15–20, 2020, London, UK
                                                                                                                              operates by sampling program state across many executions
                                         © 2020 Copyright held by the owner/author(s). Publication rights licensed
                                         to ACM.                                                                              of a program and trying to identify an Satisfiability Modulo
                                         ACM ISBN 978-1-4503-7613-6/20/06. . . $15.00                                         Theories (SMT) formula that is satisfied by all the sampled
                                         https://doi.org/10.1145/3385412.3385986                                              data points.
PLDI ’20, June 15–20, 2020, London, UK                                                           J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu


    However, verifying real-world programs often requires           This allows CLNs to learn SMT formulas with gradient de-
loop invariants with nonlinear constraints. This is espe-           scent, but a template that defines the logical structure of the
cially true in programs that perform many numerical op-             formula has to be manually provided.
erations, such as control systems for avionics or industrial           We base our approach on three developments that ad-
plants [6, 20]. Data-driven nonlinear invariant inference is        dress the challenges inherent in nonlinear loop invariant
fundamentally difficult because the space of possible non-          inference: First, we introduce a new neural architecture, the
linear invariants is large, but sufficient invariants for veri-     Gated Continuous Logic Network (G-CLN), a more robust CLN
fication must be inferred from a finite number of samples.          architecture that is not dependent on formula templates. Sec-
In practice, this leads to three distinct challenges when per-      ond, we introduce Fractional Sampling, a principled program
forming nonlinear data-driven invariant inference: (i) Large        relaxation for dense sampling. Third, we derive the Piece-
search space with high magnitude terms. Learning nonlinear          wise Biased Quadratic Unit (PBQU), a new CLN activation
terms causes the space of possible invariants to grow quickly       function for inequality learning. We provide an overview of
(i.e. polynomial expansion of terms grows exponentially in          these methods below.
the degree of terms). Moreover, large terms such as x 2 or          Gated Continuous Logic Networks. G-CLNs improve the
x y dominate the process and prevent meaningful invariants          CLN architecture by making it more robust and general.
from being learned. (ii) Limited samples. Bounds on the num-        Unlike CLNs, G-CLNs are not dependent on formula tem-
ber of loop iterations in programs with integer variables           plates for logical structure. We adapt three different methods
limit the number of possible samples, leading to overfitting        from deep learning to make G-CLN training more stable
when learning nonlinear invariants. (iii) Distinguishing suffi-     and combat overfitting: gating, dropout, and batch normal-
cient inequalities. For any given finite set of samples, there      ization [2, 13, 16, 37]. To force the model to learn a varied
are potentially infinite valid inequality bounds on the data.       combination of constraints, we apply Term Dropout, which
However, verification usually requires specific bounds that         operates similarly to dropout in feedforward neural networks
constrain the loop behavior as tightly as possible.                 by zeroing out a random subset of terms in each clause. Gat-
    Figure 1a and 1b illustrate the challenges posed by loops       ing makes the CLN architecture robust by allowing it to ig-
with many higher-order terms as well as nonlinear inequality        nore subclauses that cannot learn satisfying coefficients for
bounds. The loop in Figure 1a computes a cubic power and            their inputs, due to poor weight initialization or dropout. To
requires the invariant (x = n3 ) ∧ (y = 3n2 + 3n + 1) ∧             stabilize training in the presence of high magnitude nonlin-
(z = 6n + 6) to verify its postcondition (x = a 3 ). To infer       ear terms, we apply normalization to the input and weights
this invariant, a typical data-driven inference system must         similar to batch normalization.
consider 35 possible terms, ranging from n to x 3 , only seven         By combining dropout with gating, G-CLNs are able to
of which are contained in the invariant. Moreover, the higher-      learn complex constraints for loops with many higher-order
order terms in the program will dominate any error measure          terms. For the loop in Figure 1a, the G-CLN will set the n2
in fitting an invariant, so any data-driven model will tend to      or n 3 terms to zero in several subclauses during dropout,
only learn the constraint (x = n 3 ). Figure 1b shows a loop for    forcing the model to learn a conjunction of all three equality
computing integer square root where the required invariant          constraints. Clauses that cannot learn a satisfying set of
is (n ≥ a 2 ) to verify its postcondition. However, a data-driven   coefficients due to dropout, i.e. a clause with only x and n
model must identify this invariant from potentially infinite        but no n3 term, will be ignored by a model with gating.
other valid but loosely fit inequality invariants.                  Fractional Sampling. When the samples from the program
    Most existing methods for nonlinear loop invariant infer-       trace are insufficient to learn the correct invariant due to
ence address these challenges by limiting either the structure      bounds on program behavior, we perform a principled relax-
of invariants they can learn or the complexity of invariants        ation of the program semantics to continuous functions. This
they can scale to. Polynomial equation solving methods such         allows us to perform Fractional Sampling, which generates
as Numinv and Guess-And-Check are able to learn equal-              samples of the loop behavior at intermediate points between
ity constraints but cannot learn nonlinear inequality invari-       integers. To preserve soundness, we define the relaxation
ants [21, 33]. In contrast, template enumeration methods            such that operations retain their discrete semantics relative
such as PIE can potentially learn arbitrary invariants but          to their inputs but operate on the real domain, and any in-
struggle to scale to loops with nonlinear invariants because        variant for the continuous relaxation of the program must
space of possible invariants grows too quickly [26].                be an invariant for the discrete program. This allows us to
    In this paper, we introduce an approach that can learn          take potentially unbounded samples even in cases where the
general nonlinear loop invariants. Our approach is based            program constraints prevent sufficient sampling to learn a
on Continuous Logic Networks (CLNs), a recently proposed            correct invariant.
neural architecture that can learn SMT formulas directly            Piecewise Biased Quadratic Units. For inequality learn-
from program traces [30]. CLNs use a parameterized relax-           ing, we design a PBQU activation, which penalizes loose fits
ation that relaxes SMT formulas to differentiable functions.        and converges to tight constraints on data. We prove this
Learning Nonlinear Loop Invariants with G-CLNs                                                              PLDI ’20, June 15–20, 2020, London, UK




   // pre : ( a >= 0)                                                          // pre : ( n >= 0)          18
                                   4k       x samples
   n =0; x =0;                                                                 a =0; s =1; t =1;           16
                                            y samples
   y =1; z =6;                              z samples                          // compute sqrt :
                                                                                                           14
   // compute cube :               3k       invariants                         while ( s <= n ) {
   while ( n != a ) {                                                                                      12
                                                                                  a += 1;
       n += 1;                                                                                             10

                             xyz
                                                                                  t += 2;
                                   2k




                                                                                                       a
       x += y ;                                                                   s += t ;                  8
       y += z ;                                                                }                            6
       z += 6;                     1k                                          return a ;
                                                                                                            4                   loose invariant
   }                                                                           // post : a ^2 <= n                              tight invariant
   return x ;                                                                                               2
                                                                               // and n < ( a +1) ^2                            sample
                                   0
   // post : x == a ^3                                                                                      0
                                        0       5            10   15                                            0     100         200         300
                                                         n                                                                  n
(a) Loop for computing cubes that requires the invariant (x =              (b) Loop for computing integer approximation to square root. The
n 3 )∧(y = 3n 2 +3n+1)∧(z = 6n+6) to infer its postcondition (x = a 3 ).   graph shows three valid inequality invariants, but only the tight
A data-driven model must simultaneously learn a cubic constraint           quadratic inequality invariant (n ≥ a 2 ) is sufficient to verify that
that changes by 1000s and a linear constraint that increments by 6.        the final value of a is between ⌊sqrt(n)⌋ and ⌈sqrt(n)⌉.

                Figure 1. Example problems demonstrating the challenges of nonlinear loop invariant learning.

function will learn a tight bound on at least one point and                differentiable logic, and the CLN neural architecture for SMT
demonstrate empirically that it learns precise bounds invari-              learning. Subsequently, we introduce the high-level work-
ant bounds, such as the (n ≥ a 2 ) bound shown in Figure 1b.               flow of our method in §3. Next, in §4, we formally define
   We use G-CLNs with Fractional Sampling and PBQUs                        the gated CLN construction, relaxation for fractional sam-
to develop a unified approach for general nonlinear loop                   pling, and PBQU for inequality learning, and provide sound-
invariant inference. We evaluate our approach on a set of                  ness guarantees for gating and convergence guarantees for
loop programs with nonlinear invariants, and show it can                   bounds learning. We then provide a detailed description of
learn invariants for 26 out of 27 problems, 3 more than prior              our approach for nonlinear invariant learning with CLNs
work, with an average runtime of 53.3 seconds. We also                     in §5. Finally we show evaluation results in §6 and discuss
perform a quantitative stability evaluation and show G-CLNs                related work in §7 before concluding in §8.
have a convergence rate of 97.5% on quadratic problems, a
39.2% improvement over CLN models. We also test the G-                     2     Background
CLN architecture on the linear Code2Inv benchmark [35]                     In this section, we provide a brief review of the loop invariant
and show it can solve all 124 problems.                                    inference problem and then define the differentiable logic
   In summary, this paper makes the following contributions:               operators and the Continuous Logic Network architecture
    • We develop a new general and robust neural architec-                 used in our approach.
      ture, the Gated Continuous Logic Network (G-CLN),
      to learn general SMT formulas without relying on for-                2.1    Loop Invariant Inference
      mula templates for logical structure.                                Loop invariants encapsulate properties of the loop which
    • We introduce Fractional Sampling, a method that fa-                  are independent of the iterations and enable verification to
      cilitates sampling on the real domain by applying a                  be performed over loops. For an invariant to be sufficient for
      principled relaxation of program loop semantics to                   verification, it must simultaneously be weak enough to be
      continuous functions while preserving soundness of                   derived from the precondition and strong enough to conclude
      the learned invariants.                                              the post-condition. Formally, the loop invariant inference
    • We design PBQUs, a new activation function for learn-                problem is, given a loop “while(LC) C,” a precondition P,
      ing tight bounds inequalities, and provide convergence               and a post-condition Q, we are asked to find an inductive
      guarantees for learning a valid bound.                               invariant I that satisfies the following three conditions:
    • We integrate our methods in a general loop invariant
      inference system and show it solves 26 out 27 problems                     P =⇒ I          {I ∧ LC} C {I }        I ∧ ¬LC =⇒ Q
      in a nonlinear loop invariant benchmark, 3 more than                 where the inductive condition is defined using a Hoare triple.
      prior work. Our system can also infer loop invariants                   Loop invariants can be encoded in SMT, which facilitates
      for all 124 problems in the linear Code2Inv benchmark.               efficient checking of the conditions with solvers such as Z3 [4,
  The rest of the paper is organized as follows: In §2, we                 7]. As such, our work focuses on inferring likely candidate
provide background on the loop invariant inference problem,                invariant as validating a candidate can be done efficiently.
PLDI ’20, June 15–20, 2020, London, UK                                                                 J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu


Data-driven Methods. Data-driven loop invariant infer-                   optimization while also preserving the semantics of boolean
ence methods use program traces recording the state of each              logic, it must fulfill three conditions:
variable in the program on every iteration of the loop to                   1. It must preserve the meaning of the logic, such that
guide the invariant generation process. Since an invariant                     the continuous truth values of a valid assignment are
must hold for any valid execution, the collected traces can be                 always greater than the value of an invalid assignment:
used to rule out many potential invariants. Formally, given
a set of program traces X , data-driven invariant inference                       (F (x) = T rue ∧ F (x ′) = False)
finds SMT formulas F such that:                                                                    =⇒ (S(F )(x) > S(F )(x ′))
                       ∀x ∈ X , F (x) = T rue
                                                                            2. It must be must be continuous and smooth (i.e. differ-
2.2    Basic Fuzzy Logic                                                       entiable almost everywhere) to facilitate training.
                                                                            3. It must be strictly increasing as an unsatisfying assign-
Our approach to SMT formula learning is based on a form of
                                                                               ment of terms approach satisfying the mapped formula,
differentiable logic called Basic Fuzzy Logic (BL). BL is a re-
                                                                               and strictly decreasing as a satisfying assignment of
laxation of first-order logic that operates on continuous truth
                                                                               terms approach violating the formula.
values on the interval [0, 1] instead of on boolean values. BL
uses a class of functions called t-norms (⊗), which preserves            S is constructed as follows to satisfy these requirements. The
the semantics of boolean conjunctions on continuous truth                logical relations {∧, ∨, ¬} are mapped to their continuous
values. T-norms are required to be consistent with boolean               equivalents in BL:
logic, monotonic on their domain, commutative, and asso-
ciative [14]. Formally, a t-norm is defined ⊗ : [0, 1]2 → [0, 1]               Conjunction:         S(F 1 ∧ F 2 ) ≜ S(F 1 ) ⊗ S(F 2 )
such that:                                                                     Disjunction:         S(F 1 ∨ F 2 ) ≜ S(F 1 ) ⊕ S(F 2 )
      • ⊗ is consistent for any t ∈ [0, 1]:                                    Negation:                 S(¬F ) ≜ 1 − S(F )
                t ⊗1=t                       t ⊗0=0
                                                                         where any F is an SMT formula. S defines SMT predicates {=
      • ⊗ is commutative and associative for any t ∈ [0, 1]:             , ,, <, ≤, >, ≥} with functions that map to continuous truth
                                                                         values. This mapping is defined for {>, ≥} using sigmoids
       t1 ⊗ t2 = t2 ⊗ t1       t 1 ⊗ (t 2 ⊗ t 3 ) = (t 1 ⊗ t 2 ) ⊗ t 3
                                                                         with a shift parameter ϵ and smoothing parameter B:
      • ⊗ is monotonic (nondecreasing) for any t ∈ [0, 1]:
                                                                                                                             1
                                                                            Greater Than:            S(x 1 > x 2 ) ≜
                  t 1 ≤ t 2 =⇒ t 1 ⊗ t 3 ≤ t 2 ⊗ t 3                                                                 1 + e −B(x 1 −x 2 −ϵ )
                                                                                                                             1
BL additionally requires that t-norms be continuous. T-conorms              Greater or Equal to:     S(x 1 ≥ x 2 ) ≜
(⊕) are derived from t-norms via DeMorgan’s law and oper-                                                            1 + e −B(x 1 −x 2 +ϵ )
ate as disjunctions on continuous truth values, while nega-              where x 1 , x 2 ∈ R. Mappings for other predicates are derived
tions are defined ¬t := 1 − t.                                           from their logical relations to {>, ≥}:
   In this paper, we keep t-norms abstract in our formula-
tions to make the framework general. Prior work [30] found                Less Than:          S(x 1 < x 2 ) = S(¬(x 1 ≥ x 2 ))
product t-norm x ⊗ y = x · y perform better in Continu-                   Less or Equal to: S(x 1 ≤ x 2 ) = S(¬(x 1 > x 2 ))
ous Logic Networks. For this reason, we use product t-norm                Equality:           S(x 1 = x 2 ) = S((x 1 ≥ x 2 ) ∧ (x 1 ≤ x 2 ))
in our final implementation, although other t-norms (e.g.,
Godel) can also be used.                                                  Inequality:         S(x 1 , x 2 ) = S(¬(x 1 = x 2 ))

                                                                         Using these definitions the parametric relaxation S satisfies
2.3    Continuous Logic Networks
                                                                         all three conditions for sufficiently large B and sufficiently
We perform SMT formula learning with Continuous Logic                    small ϵ. Based on this parametric relaxation S(F ), we build a
Networks (CLNs), a neural architecture introduced in [30]                Continuous Logic Network model M, which is a computa-
that are able to learn SMT formulas directly from data. These            tional graph of S(F )(x) with learnable parameters W . When
can be used to learn loop invariants from the observed be-               training a CLN, loss terms are applied to penalize small B,
havior of the program.                                                   ensuring that as the loss approaches 0 the CLN will learn
   CLNs are based on a parametric relaxation of SMT formu-               a precise formula. Under these conditions, the following
las that maps the SMT formulation from boolean first-order               relationship holds between a trained CLN model M with
logic to BL. The model defines the operator S. Given an                  coefficients W and its associated formula F for a given set of
quantifier-free SMT formula F : X → {T rue, False}, S maps               data points, X :
it to a continuous function S(F ) : X → [0, 1]. In order for
the continuous model to be both usable in gradient-guided                        ∀x ∈ X , M(x;W ) = 1 ⇐⇒ F (x;W ) = True
Learning Nonlinear Loop Invariants with G-CLNs                                                                                   PLDI ’20, June 15–20, 2020, London, UK


                                                                                                      Given a program loop, we modify it to record variables
                    1         F(x)                                                                for each iteration and then execute the program to gener-
      Truth Value


                              (F)(x)
                                                                                                  ate samples. Figure 4a illustrates this process for the sqrt
                                                                                                  program from Figure 1b. The program has the input n with
                    0                                                                             precondition (n ≥ 0), so we execute with values n = 0, 1, 2, ...
                              0         1           2               3       4          5          for inputs in a set range. Then we expand the samples to
                                                        x                                         all candidate terms for the loop invariant. By default, we
Figure 2. Plot of the formula F (x) ≜ (x = 1)∨(x ≥ 5)∨(x ≥                                        enumerate all the monomials over program variables up to
2 ∧ x ≤ 3) and its associated CLN M(x).                                                           a given degree maxDeд, as shown in Figure 4b. Our system
                                                                                                  can be configured to consider other non-linear terms like x y .
                                                                                                      We then construct and train a G-CLN model using the col-
                                                                                                  lected trace data. We use the model architecture described
              Source                                                             Candidate        in §5.2.1, with PBQUs for bounds learning using the pro-
               code                                                               Invariant
                                                                                                  cedure in §5.2.2. After training the model, the SMT for-
                                                                                                  mula for the invariant is extracted by recursively descend-
                                                                                                  ing through the model and extracting clauses whose gat-
         Execution
          Traces                                                                      Z3          ing parameters are above 0.5, as outlined in Algorithm 1.
                                                                                                  On the sqrt program, the model will learn the invariant
    Trace Collection                    Invariant Generation                 Invariant Checking
                                                                                                   a 2 ≤ n ∧ (t = 2a + 1) ∧ su = (a + 1)2 .
                                                                                                      Finally, if z3 returns a counterexample, we will incorporate
                                         Counterexamples
                                                                                                  it into the training data, and rerun the three stages with more
Figure 3. Overview of method consisting of 3 phases: trace                                        generated samples. Our system repeats until a valid invariant
generation from source code file, G-CLN training, and in-                                         is learned or times out.
variant extraction followed by checking with Z3.
                                                                                                  4     Theory
          // pre : ( n >= 0)                                                                      In this section, we first present our gating construction for
          a =0; s =1; t =1;                     1           a   t       ... as   t2        st     CLNs and prove gated CLNs are sound with regard to their
          while (s <= n ) {                                                                       underlying discrete logic. We then describe Piecewise Biased
                                                1           0   1           0     1         1
             log (a ,s ,t , n ) ;                                                                 Quadratic Units, a specific activation function construction
             a += 1;                            1           1   3           4     9         12
                                                                                                  for learning tight bounds on inequalities, and provide theo-
             t += 2;                            1           2   5          18    25         45
             s += t ;                                                                             retical guarantees. Finally we present a technique to relax
                                                1           3   7          48    49        112
          }                                                                                       loop semantics and generate more samples when needed.
          log (a ,s ,t , n ) ;
         (a) Program instru-    (b) Sample data points generated
         mented to log samples. with maximum degree of 2.
                                                                                                  4.1   Gated t-norms and t-conorms
                                                                                                  In the original CLNs [30], a formula template is required
Figure 4. Training data generation for the program shown                                          to learn the invariant. For example, to learn the invariant
in Figure 1b.                                                                                     (x + y = 0) ∨ (x − y = 0), we have to provide the template
                                                                                                  (w 1x + w 2y + b1 = 0) ∨ (w 3x + w 4y + b2 = 0), which can be
                                                                                                  constructed as a CLN model to learn the coefficients. So, we
Figure 2 shows an example CLN for the formula on a single                                         have to know in advance whether the correct invariant is an
variable x:                                                                                       atomic clause, a conjunction, a disjunction, or a more com-
                                                                                                  plex logical formula. To tackle this problem, we introduce
                        F (x) = (x = 1) ∨ (x ≥ 5) ∨ (x ≥ 2 ∧ x ≤ 3)                               gated t-norms and gated t-conorms.
                                                                                                     Given a classic t-norm T (x, y) = x ⊗ y, we define its asso-
                                                                                                  ciated gated t-norm as
3      Workflow
Figure 3 illustrates our overall workflow for loop invariant
inference. Our approach has three stages: (i) We first instru-                                          TG (x, y; д1 , д2 ) = (1 + д1 (x − 1)) ⊗ (1 + д2 (y − 1))
ment the program and execute to generate trace data. (ii) We
then construct and train a G-CLN model to fit the trace data.
(iii) We extract a candidate loop invariant from the model                                        Here д1 , д2 ∈ [0, 1] are gate parameters indicating if x and
and check it against a specification.                                                             y are activated, respectively. The following equation shows
PLDI ’20, June 15–20, 2020, London, UK                                                                   J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu


the intuition behind gated t-norms.                                    Algorithm 1 Formula Extraction Algorithm.
                               x ⊗y        д1 = 1, д2 = 1             Input: A gated CLN model M, with input nodes
                                                                       X = {x 1 , x 2 , ..., x n } and output node p.
                              
                               x           д1 = 1, д2 = 0
                              
                              
        TG (x, y; д1 , д2 ) =
                              
                               y           д1 = 0, д2 = 1             Output: An SMT formula F
                                            д1 = 0, д2 = 0             Procedure ExtractFormula(M)
                              
                               1
                              
                                                                         1: if p = TG (M 1 , ..., Mn ; д1 , ..., дn ) then
                              
   Informally speaking when д1 = 1, the input x is activated             2:    F := True
and behaves as in the classic t-norm. When д1 = 0, x is                  3:    for i := 1 to n do
deactivated and discarded. When 0 < д1 < 1, the value of                 4:       if дi > 0.5 then
д1 indicates how much information we should take from x.                 5:           F := F ∧ ExtractFormula(Mi )
This pattern also applies for д2 and y.                                  6: else if p = TG′ (M 1 , ..., Mn ; д1 , ..., дn ) then
   We can prove that ∀д1 , д2 ∈ [0, 1], the gated t-norm is              7:    F := False
continuous and monotonically increasing with regard to x                 8:    for i := 1 to n do
and y, thus being well suited for training.                              9:       if дi > 0.5 then
   Like the original t-norm, the gated t-norm can be easily             10:           F := F ∨ ExtractFormula(Mi )
extended to more than two operands. In the case of three                11: else if p = 1 − M 1 then
operands, we have the following:                                        12:    F := ¬ExtractFormula(M1 )
   TG (x, y, z; д1 , д2 , д3 ) = (1 + д1 (x − 1)) ⊗ (1 + д2 (y − 1))    13: else
                                                                        14:    F := BuildAtomicFormula(M)
                             ⊗ (1 + д3 (z − 1))
  Using De Morgan’s laws x ⊕ y = 1 − (1 − x) ⊗ (1 − y), we
define gated t-conorm as                                               possible denominator. We check if each rounded invariant
                                                                       fits all the training data and discard the invalid ones.
          TG′ (x, y; д1 , д2 ) = 1 − (1 − д1x) ⊗ (1 − д2y)                In Theorem 4.1, we will show that the extracted SMT
                                                                       formula is equivalent to the gated CLN model under some
Similar to gated t-norms, gated t-conorms have the following
property.
                                                                                          Gate             T-norm
                              
                               x ⊕y        д1 = 1, д2 = 1
                               x           д1 = 1, д2 = 0
                              
                              
        TG (x, y; д1 , д2 ) =
         ′
                              
                               y           д1 = 0, д2 = 1                                        Gate               T-norm

                                            д1 = 0, д2 = 0
                              
                               0
                              
                              
   Now we replace the original t-norms and t-conorms in                                                     Gate

CLN with our gated alternatives, which we diagram in Fig-
ure 5. Figure 6 demonstrates a gated CLN for representing
an SMT formula. With the gated architecture, the gating pa-
rameters д1 , д2 for each gated t-norm or gated t-conorm are
made learnable during model training, such that the model              Figure 5. Example of gated t-norm with three operands
can decide which input should be adopted and which should              constructed from binary t-norms. The gated t-conorm is
be discarded from the training data. This improves model               done similarly.
flexibility and does not require a specified templates.
   Now, we formally state the procedure to retrieve the SMT
formula from a gated CLN model recursively in Algorithm 1.                                                   +
Abusing notation for brevity, Mi in line 1 represent the
                                                                                                                         +
output node of model Mi rather than the model itself, and                                                    +
the same applies for line 8 and line 15. BuildAtomicFormula                                                  -
in line 18 is a subroutine to extract the formula for a model                                                            +
with no logical connectives (e.g., retrieving x + y + z = 0
in Figure 6). The linear weights which have been learned                                                     +
serve as the coefficients for the terms in the equality or
inequality depending on the associated activation function.            Figure 6. An instance of gated CLN. “+” means
Finally, we need to round the learned coefficients to integers.        activated (g=1) and “-” means deactivated (g=0).
We first scale the coefficients so that the maximum is 1 and           The SMT formula learned is (3y − 3z − 2 = 0) ∧
then round to the nearest rational number using a maximum              ((x − 3z = 0) ∨ (x + y + z = 0)).
Learning Nonlinear Loop Invariants with G-CLNs                                                                    PLDI ’20, June 15–20, 2020, London, UK


constraints. We first introduce a property of t-norms that is                     x ∈ X , then from Theorem 4.1 the recovered formula F is
defined in the original CLNs [30].                                                guaranteed to hold true for all the training samples. That is,
                                                                                  ∀x ∈ X , F (x) = T rue.
Property 1. ∀t u, (t > 0) ∧ (u > 0) =⇒ (t ⊗ u > 0).
  The product t-norm x ⊗ y = x · y, which is used in our                          4.2   Parametric Relaxation for Inequalities
implementation, has this property.                                                For learned inequality constraints to be useful in verification,
  Note that the hyperparameters c 1 , c 2 , ϵ, σ in Theorem 4.1                   they usually need to constrain the loop behavior as tightly as
will be formally introduced in §4.2 and are unimportant here.                     possible. In this section, we define a CLN activation function,
One can simply see                                                                the bounds learning activation, which naturally learns tight
                                                                                  bounds during training while maintaining the soundness
                        lim         M(x; c 1 , c 2 , σ , ϵ)
                    c 1 →0,c 2 →∞                                                 guarantees of the CLN mapping to SMT.
                     σ →0,ϵ →0
                                                                                                                     c2
                                                                                                               (t −u)12 +c 2 t < u
                                                                                                              
as the model output M(x).                                                                                     
                                                                                                 S(t ≥ u) ≜
                                                                                                              
                                                                                                                     c2
                                                                                                                           1                   (3)
Theorem 4.1. For a gated CLN model M with input nodes                                                          (t −u)22 +c 2 t ≥ u
                                                                                                              
                                                                                                                           2
{x 1 , x 2 , ..., x n } and output node p, if all gating parameters {дi }
                                                                                                              
                                                                                  Here c 1 and c 2 are two constants. The following limit prop-
are either 0 or 1, then using the formula extraction algorithm,                   erty holds.
the recovered SMT formula F is equivalent to the gated CLN
                                                                                                                         0 t <u
                                                                                                                     
model M. That is, ∀x ∈ R n ,                                                                        lim S(t ≥ u) =
                                                                                                   c 1 →0                1 t ≥u
    F (x) = T rue ⇐⇒                lim       M(x; c 1 , c 2 , σ , ϵ) = 1   (1)                    c 2 →∞
                              c 1 →0,c 2 →∞
                               σ →0,ϵ →0                                          Intuitively speaking, when c 1 approaches 0 and c 2 approaches
   F (x) = False ⇐⇒                 lim       M(x; c 1 , c 2 , σ , ϵ) = 0   (2)   infinity, S(x ≥ 0) will approach the original semantic of pred-
                              c 1 →0,c 2 →∞
                               σ →0,ϵ →0                                          icate ≥. Figure 7b provides an illustration of our parametric
                                                                                  relaxation for ≥.
as long as the t-norm in M satisfies Property 1.
                                                                                     Compared with the sigmoid construction in the original
Proof. We prove this by induction over the formula structure                      CLNs (Figure 7a), our parametric relaxation penalizes very
considering four cases: atomic, negation, T-norm, and T-                          large x, where x ≥ 0 is absolutely correct but not very in-
conorm. For brevity, we sketch the T-norm case here and                           formative because the bound is too weak. In general, our
provide the full proof in Appendix A.                                             piecewise mapping punishes data points farther away from
                                                                                  the boundary, thus encouraging to learn a tight bound of the
T-norm Case. If p = TG (M1 , ..., Mn ; д1 , ..., дn ), which means
                                                                                  samples. On the contrary, the sigmoid construction encour-
the final operation in M is a gated t-norm, we know that
                                                                                  ages samples to be far from the boundary, resulting in loose
for each submodel M1 , ..., Mn the gating parameters are all
                                                                                  bounds which are not useful for verification.
either 0 or 1. By the induction hypothesis, for each Mi , using
Algorithm 1, we can extract an equivalent SMT formula Fi
satisfying Eq. (1)(2). Then we can prove the full model M
and the extracted formula F also satisfy Eq. (1)(2), using the
induction hypothesis and the properties and t-norms.            □
   The requirement of all gating parameters being either 0 or
1 indicates that no gate is partially activated (e.g., д1 = 0.6).
Gating parameters between 0 and 1 are acceptable during
                                                                                  (a) Plot of S(x ≥ 0) with the      (b) Plot of S(x ≥ 0) with our
model fitting but should be eliminated when the model con-                        CLNs’ sigmoid construction.        piecewise construction.
verges. In practice this is achieved by gate regularization
                                                                                  Figure 7. Comparison of the mapping S on ≥. The hyper-
which will be discussed in §5.2.1.
                                                                                  parameters are B = 5, ϵ = 0.5, c 1 = 0.5, and c 2 = 5.
   Theorem 4.1 guarantees the soundness of the gating method-
ology with regard to discrete logic. Since the CLN architec-                         Since the samples represent only a subset of reachable
ture is composed of operations that are sound with regard to                      states from the program, encouraging a tighter bound may
discrete logic, this property is preserved when gated t-norms                     potentially lead to overfitting. However, we ensure sound-
and t-conorms are used in the network.                                            ness by later checking learned invariants via a solver. If an
   Now the learnable parameters of our gated CLN include                          initial bound is too tight, we can incorporate counterexam-
both linear weights W as in typical neural networks, and                          ples to the training data. Our empirical results show this
the gating parameters {дi }, so the model can represent a                         approach works well in practice.
large family of SMT formulas. Given a training set X , when                          Given a set of n k-dimensional samples {[x 11 , ..., x 1k ], ...,
the gated CLN model M is trained to M(x) = 1 for all                              [x n1 , ..., x nk ]}, where x i j denotes the value of variable x j in
PLDI ’20, June 15–20, 2020, London, UK                                                               J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu


the i-th sample, we want to learn an inequality w 1x 1 + ... +          // pre : x = y = 0               x     y y2            y3      y4
w k x k + b ≥ 0 for these samples. The desirable properties of          //        /\ k >= 0
such an inequality is that it should be valid for all points,           while ( y < k ) {                 0    0         0     0       0
and have as tight as a fit as possible. Formally, we define a              y ++;                          1    1         1     1       1
“desired” inequality as:
                                                                           x += y * y * y ;               9    2         4     8       16
                                                                        }                                36    3        9     27      81
           ∀i ∈ {1, ..., n}, w 1x i1 + ... + w k x ik + b ≥ 0           // post : 4 x == k ^2
                                                                                                         100   4        16    64      256
                                                              (4)       //       * ( k + 1) ^2
           ∃j ∈ {1, ..., n}, w 1x j1 + ... + w k x jk + b = 0                                            225   5        25    125     625
   Our parametric relaxation for ≥ shown in Eq. 3 can always            (a) The ps4 program          (b) Training data generated
learn an inequality which is very close to a “desired” one              in the benchmark.            without Fractional Sampling.
with proper c 1 and c 2 . Theorem 4.2 put this formally.
Theorem 4.2. Given a set of n k-dimensional samples √ with              x       y    y2      y3     y4    x0       y0        y02      y03    y04
the maximum L2-norm l, if c 1 ≤ 2l and c 1 · c 2 ≥ 8 nl 2 , and
                                                                        -1 -0.6 0.36 -0.22 0.13           -1   -0.6      0.36       -0.22   0.13
the weights are constrained as ki=1 w i2 = 1, then when the
                                 Í
                                                                      -0.9 0.4 0.16 0.06 0.03             -1   -0.6      0.36       -0.22   0.13
model√ converges, the learned inequality has distance at most          1.8 1.4 1.96 2.74 3.84             -1   -0.6      0.36       -0.22   0.13
c 1 / 3 from a “desired” inequality.                                     0 -1.2 1.44 -1.73 2.07            0   -1.2      1.44       -1.73   2.07
                                                                         0 -0.2 0.04 -0.01 0.00            0   -1.2      1.44       -1.73   2.07
Proof. See Appendix B.                                          □
                                                                       0.5 0.8 0.64 0.52 0.41              0   -1.2      1.44       -1.73   2.07
                                                      √
   Recall that c 1 is a small constant, so c 1 / 3 can be con-
                                                                            (c) Training data generated with fractional sampling.
sidered as the error bound of inequality learning. Although
we only proved the theoretical guarantee when learning a
                                                                            Figure 8. An example of Fractional Sampling.
single inequality, our parametric relaxation for inequalities
can be connected with other inequalities and equalities with
conjunctions and disjunctions under a single CLN model.             where V0 7→∗ V means starting from initial values V0 and
   Based on our parametric relaxation for ≥, other inequality       executing the loop for 0 or more iterations ends with values
predicates can be defined accordingly.                              V for the variables.
                                 c2                                   Now we relax the initial values X 0 and see them as input
                            (t −u)22 +c 2 t < u
                           
                                                                    variables VI , which may carry arbitrary values. The new loop
                           
              S(t ≤ u) ≜
                           
                                        2
                                 c2
                            (t −u)12 +c 2 t ≥ u
                                                                   program will have variables V ∪ VI . Suppose we can learn
                                        1
                                                                    an invariant predicate I ′ for this new program, i.e.,
                           
  S(t > u) ≜ S(t ≥ (u + ϵ))         S(t < u) ≜ S(t ≤ (u − ϵ))                       ∀VI V , VI 7→∗ V =⇒ I ′(VI ∪ V )                          (6)
where ϵ is a set small constant.
                                                                    Then let VI = V0 , Eq. (6) will become
   For our parametric relaxation, some axioms in classic logic
just approximately rather than strictly hold (e.g., t ≤ u =                           ∀V , V0 7→∗ V =⇒ I ′(V0 ∪ V )                           (7)
¬(t > u)). They will strictly hold when c 1 → 0 and c 2 → ∞.
                                                                    Now V0 is a constant, and I ′(V0 ∪ V ) satisfies Eq. (5) thus
   We reuse the Gaussian function as the parametric relax-
                                                                    being a valid invariant for the original program. In fact, if we
ation for equalities [30]. Given a small constant σ ,
                                                                    learn predicate I ′ successfully then we have a more general
                                         (t − u)2                   loop invariant that can apply for any given initial values.
                   S(t = u) ≜ exp (−              )
                                            2σ 2                       Figure 8 shows how Fractional Sampling can generate
                                                                    more fine-grained samples with different initial values, mak-
4.3   Fractional Sampling
                                                                    ing model fitting much easier in our data-driven learning
In some cases, the samples generated from the original pro-         system. The correct loop invariant for the program in Figure
gram are insufficient to learn the correct invariant due to         8a is
dominating growth of some terms (higher-order terms in                              (4x = y 4 + 2y 3 + y 2 ) ∧ (y ≤ k)
particular) or limited number of loop iterations. To generate
more fine-grained yet valid samples, we perform Fractional          To learn the equality part (4x = y 4 + 2y 3 + y 2 ), if we choose
Sampling to relax the program semantics to continuous func-         maxDeд = 4 and apply normal sampling, then six terms
tions without violating the loop invariants by varying the          {1, y, y 2 , y 3 , y 4 , x } will remain after the heuristic filters in
initial value of program variables. The intuition is as follows.    §5.1.3. Figure 8b shows a subset of training samples without
   Any numerical loop invariant I can be viewed as a predi-         Fractional Sampling (the column of term 1 is omitted).
cate over program variables V initialized with V0 such that           When y becomes larger, the low order terms 1, y, and y 2
                                                                    become increasingly negligible because they are significantly
                    ∀V , V0 7→∗ V =⇒ I (V )                  (5)    smaller than the dominant terms y 4 and x. In practice we
Learning Nonlinear Loop Invariants with G-CLNs                                                              PLDI ’20, June 15–20, 2020, London, UK


observe that the coefficients for x 4 and y can be learned                 w 2t 2 + ... +w k tk = 0 (note that ti can be a higher-order term),
accurately but not for 1, y, y 2 . To tackle this issue, we hope           so does the normalized sample and vice versa. The same
to generate more samples around y = 1 where all terms are                  argument applies to inequalities.
on the same level. Such samples can be easily generated by
                                                                           5.1.2 Weight Regularization. For both equality invari-
feeding more initial values around y = 1 using Fractional
                                                                           ant w 1x 1 + ... + wm xm + b = 0 and inequality invariant
Sampling. Table 8c shows some generated samples from
                                                                           w 1x 1 + ... + wm xm + b ≥ 0, w 1 = ... = wm = b = 0 is a true
x 0 = −1, y0 = −0.6 and x 0 = 0, y0 = −1.2.
                                                                           solution. To avoid learning this trivial solution, we require
    Now we have more samples where terms are on the same
                                                                           at least one of {w 1 , ..., wm } is non-zero. A more elegant way
level, making the model easier to converge to the accurate
                                                                           is to constrain the Lp -norm of the weight vector to constant
solution. Our gated CLN model can correctly learn the re-
                                                                           1. In practice we choose L2-norm as we did in Theorem 4.2.
laxed invariant 4x − y 4 − 2y 3 − y 2 − 4x 0 + y04 + 2y03 + y02 = 0.
                                                                           The weights are constrained to satisfy
Finally we return to the exact initial values x 0 = 0, y0 = 0,
and the correct invariant for the original program will appear                                      w 12 + ... + wm
                                                                                                                  2
                                                                                                                    =1
4x − y 4 − 2y 3 − y 2 = 0.
                                                                           5.1.3 Term Dropout. Given a program with three vari-
    Note that for convenience, in Eq. (5)(6)(7), we assume all
                                                                           ables {x, y, z} and maxDeд = 2, we will have ten candidate
variables are initialized in the original program and all are
                                                                           terms {1, x, y, z, x 2 , y 2 , z 2 , xy, xz, yz}. The large number of
relaxed in the new program. However, the framework can
                                                                           terms poses difficulty for invariant learning, and the loop
easily extends to programs with uninitialized variables, or
                                                                           invariant in a real-world program is unlikely to contain all
we just want to relax a subset of initialized variables. Details
                                                                           these terms. We use two methods to select terms. First the
on how fractional sampling is incorporated in our system
                                                                           growth-rate-based heuristic in [33] is adopted to filter out
are provided in §5.4.
                                                                           unnecessary terms. Second we apply a random dropout to
                                                                           discard terms before training.
5     Nonlinear Invariant Learning                                            Dropout is a common practice in neural networks to avoid
In this section, we describe our overall approach for nonlin-              overfitting and improve performance. Our dropout is ran-
ear loop invariant inference. We first describe our methods                domly predetermined before the training, which is different
for stable CLN training on nonlinear data. We then give an                 from the typical weight dropout in deep learning [37]. Sup-
overview of our model architecture and how we incorporate                  pose after the growth-rate-based filter, seven terms {1, x,
our inequality activation function to learn inequalities. Fi-              y, z, x 2 , y 2 , xy} remain. Before the training, each input term
nally, we show how we extend our approach to also learn                    to a neuron may be discarded with probability p.
invariants that contain external functions.                                   The importance of dropout is twofold. First it further re-
                                                                           duces the number of terms in each neuron. Second it en-
5.1   Stable CLN Training on Nonlinear Data                                courages G-CLN to learn more simple invariants. For exam-
Nonlinear data causes instability in CLN training due to the               ple, if the desired invariant is (x − y − 1 = 0) ∧ (x 2 − z =
large number of terms and widely varying magnitudes it in-                 0), then a neuron may learn their linear combination (e.g.,
troduces. We address this by modifying the CLN architecture                2x − 2y − 2 + x 2 − z = 0) which is correct but not human-
to normalize both inputs and weights on a forward execution.               friendly. If the term x is discarded in one neuron then that
We then describe how we implement term dropout, which                      neuron may learn x 2 −z = 0 rather than 2x −2y−2+x 2 −z = 0.
helps the model learn precise SMT coefficients.                            Similarly, if the terms x 2 and xy are discarded in another
                                                                           neuron, then that neuron may learn x − y − 1 = 0. Together,
5.1.1 Data Normalization. Exceedingly large inputs cause
                                                                           the entire network consisting of both neurons will learn the
instability and prevent the CLN model from converging to
                                                                           precise invariant.
precise SMT formulas that fit the data. We therefore modify
                                                                              Since the term dropout is random, a neuron may end up
the CLN architecture such that it rescales its inputs so the
                                                                           having no valid invariant to learn (e.g., both x and x 2 are
L2-norm equals a set value l. In our implementation, we used
l = 10.
    We take the program in Figure 1b as an example. The raw                Table 1. Training data after normalization for the program
samples before normalization is shown in Figure 4b. The                    in Figure 1b, which computes the integer square root.
monomial terms span in a too wide range, posing difficulty
for network training. With data normalization, each sample                             1      a        t     ...   as      t2     st
(i.e., each row) is proportionally rescaled to L2-norm 10. The
                                                                                     0.70      0     0.70            0    0.70   0.70
normalized samples are shown in Table 1.
                                                                                     0.27    0.27    0.81          1.08   2.42   3.23
    Now the samples occupy a more regular range. Note that
                                                                                     0.13    0.25    0.63          2.29   3.17   5.71
data normalization does not violate model correctness. If
                                                                                     0.06    0.19    0.45          3.10   3.16   7.23
the original sample (t 1 , t 2 , ...tk ) satisfies the equality w 1t 1 +
PLDI ’20, June 15–20, 2020, London, UK                                                                        J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu




              Dropout       Gaussian                                 Output



                                                         Gated
                                                       Conjunction
                                                         Layer
   Input                                   Gated
                                         Disjunction
                                            Layer
                                                                                  (a) Learned inequality         (b) Learned inequality
              Dropout       PBQ Unit                                              bounds.                        bounds on sqrt.

                                                                                 Figure 10. Examples of 2 dimensional bound fitting.
Figure 9. Diagram of G-CLN model. Additional disjunction
and conjunction layers may be added to learn more complex
SMT formulas.                                                                 the following loss function with regard to the linear weights
                                                                              W and gating parameters G,
                                                                                                     Õ
                                                                                       L(X ;W , G) =    (1 − M(x;W , G))
discarded in the example above). But when gating (§4.1)
                                                                                                    x ∈X
is adopted, this neuron will be deactivated and remaining                                                    Õ                          Õ
neurons may still be able to learn the desired invariant. More                                       + λ1            (1 − дi ) + λ 2             дi
details on gated model training will be provided in §5.2.1.                                                 дi ∈TG                     дi ∈TG′

                                                                              By training the G-CLN with this loss formulation, the model
5.2    Gated CLN Invariant Learning                                           tends to learn a formula F satisfying each training sample
Here we describe the Gated CLN architecture and how we                        (recall F (x) = T rue ⇔ M(x) = 1 in §4.1). Together, gating
incorporate the bounds learning activation function to learn                  and regularization prunes off poorly learned clauses, while
general nonlinear loop invariants.                                            preventing the network from pruning off too aggressively.
                                                                              When the training converges, all the gating parameters will
5.2.1 Gated CLN Architecture. Architecture. In §3.1,
                                                                              be very close to either 1 or 0, indicating the participation of
we introduce gated t-norm and gated t-conorm, and illustrate
                                                                              the clause in the formula. The invariant is recovered using
how they can be integrated in CLN architecture. Theoreti-
                                                                              Algorithm 1.
cally, the gates can cascade to many layers, while in practice,
we use a gated t-conorm layer representing logical OR fol-                    5.2.2 Inequality Learning. Inequality learning largely
lowed by a gated t-norm layer representing logical AND, as                    follows the same procedure as equality learning with two
shown in Figure 9. The SMT formula extracted from such a                      differences. First, we use the PBQU activation (i.e., the para-
gated CLN architecture will be in conjunctive normal form                     metric relaxation for ≥) introduced in §4.2, instead of the
(CNF). In other words, G-CLN is parameterized by m and n,                     Gaussian activation function (i.e., the parametric relaxation
where the underlying formula can be a conjunction of up                       for =). This difference is shown in Figure 9. As discussed in
to m clauses, where each clause is a disjunction of n atomic                  §4.2, the PBQU activation will learn tight inequalities rather
clauses. In the experiments we set m=10, n=2.                                 than loose ones.
Gated CLN Training. For the sake of discussion, consider                         Second, we structure the dropout on inequality constraints
a gated t-norm with two inputs. We note that the gating                       to consider all possible combinations of variables up to a set
parameters д1 and д2 have an intrinsic tendency to become                     number of terms and maximum degree (up to 3 terms and 2nd
0 in our construction. When д1 = д2 = 0, TG (x, y; д1 , д2 ) = 1              degree in our evaluation). We then train the model following
regardless of the truth value of the inputs x and y. So when                  the same optimization used in equality learning, and remove
training the gated CLN model, we apply regularization on                      constraints that do not fit the data based on their PBQU
д1 , д2 to penalize small values. Similarly, for a gated t-conorm,            activations after the model has finished training.
the gating parameters д1 , д2 have an intrinsic tendency to                      When extracting a formula from the model we remove
become 1 because x ⊕ y has a greater value than x and y.                      poorly fit learned bounds that have PBQU activations be-
To resolve this we apply regularization pressure on д1 , д2 to                low a set threshold. As discussed in §4.2, PBQU activations
penalize close-to-1 values.                                                   penalizes points that are farther from its bound. The tight
    In the general case, given training set X and gate regular-               fitting bounds in Figures 10a and 10b with solid red lines
ization parameters λ 1 , λ 2 , the model will learn to minimize               have PBQU activations close to 1, while loose fitting bounds
Learning Nonlinear Loop Invariants with G-CLNs                                                    PLDI ’20, June 15–20, 2020, London, UK


with dashed lines have PBQU activations close to 0. After          an Intel XeonE5-2623 v4 2.60GHz CPU, 256Gb of memory,
selecting the best fitting bounds, we check against the loop       and an Nvidia GTX 1080Ti GPU.
specification and remove any remaining constraints that are
                                                                   System Configuration. We implement our method with
unsound. If the resulting invariant is insufficient to prove the
                                                                   the PyTorch Framework and use the Z3 SMT solver to vali-
postcondition, the model is retrained using the counterex-
                                                                   date the correctness of the inferred loop invariants. For the
amples generated during the specification check.
                                                                   four programs involving greatest common divisors, we man-
                                                                   ually check the validity of the learned invariant since gcd is
5.3   External Function Calls                                      not supported by z3. We use a G-CLN model with the CNF
In realistic applications, loops are not entirely whitebox and     architecture described in §5.2.1, with a conjunction of ten
may contain calls to external functions for which the sig-         clauses, each with up to two literals. We use adaptive regular-
nature is provided but not the code body. In these cases,          ization on the CLN gates. λ 1 is set to (1.0, 0.999, 0.1), which
external functions may also appear in the loop invariant. To       means that λ 1 is initialized as 1.0, and is multiplied by 0.999
address these cases, when an external function is present, we      after each epoch until it reaches the threshold 0.1. Similarly,
sample it during loop execution. To sample the function, we        λ 2 is set to (0.001, 1.001, 0.1). We try three maximum denom-
execute it with all combinations of variables in scope during      inators, (10, 15, 30), for coefficient extraction in §4.1. For the
sampling that match its call signature.                            parametric relaxation in §4.2, we set σ = 0.1, c 1 = 1, c 2 = 50.
   For example, the function дcd : Z × Z → Z, for great-           The default dropout rate in §5.1.3 is 0.3, and will decrease
est common divisor, is required in the invariant for four of       by 0.1 after each failed attempt until it reaches 0. We use the
the evaluation problems that compute either greatest com-          Adam optimizer with learning rate 0.01, decay 0.9996, and
mon divisor or least common multiple: (egcd2, egcd3, lcm1,         max epoch 5000.
and lcm2). In practice, we constrain our system to binary
functions, but it is not difficult to utilize static-analysis to   6.1   Polynomial Invariant Dataset
extend the support to more complex external function calls.        We evaluate our method on a dataset of programs that require
This procedure of constructing terms containing external           nonlinear polynomial invariants [22]. The problems in this
function calls is orthogonal to our training framework.            dataset represent various numerical algorithms ranging from
                                                                   modular division and greatest common denominator (дcd)
5.4   Fractional Sampling Implementation                           to computing geometric and power series. These algorithms
We apply fractional sampling on a per-program basis when           involve up to triply nested loops and sequential loops, which
we observe the model is unable to learn the correct polyno-        we handle by predicting all the requisite invariants using
mial from the initial samples. We first sample on 0.5 intervals,   the model before checking their validity. We sample within
then 0.25, etc. until the model learns a correct invariant. We     input space of the whole program just as we do with single
do not apply fractional sampling to variables involved in          loop problems and annotate the loop that a recorded state
predicates and external function calls, such as gcd. In princi-    is associated with. The invariants involve up to 6th order
ple, predicate constraints can be relaxed to facilitate more       polynomial and up to thirteen variables.
general sampling. We will investigate this in future work.         Performance Comparison. Our method is able to solve
   Among all the programs in our evaluation, only two of           26 of the 27 problems as shown in Table 2, while NumInv
them, ps5 and ps6, require fractional sampling. For both           solves 23 of 27. Our average execution time was 53.3 seconds,
of them sampling on 0.5 intervals is sufficient to learn the       which is a minor improvement to NumInv who reported 69.9
correct invariant, although more fine grained sampling helps       seconds. We also evaluate LoopInvGen (PIE) on a subset of
the model learn a correct invariant more quickly. The cost         the simpler problems which are available in a compatible
associated with fractional sampling is small (< 5s).               format1 . It was not able to solve any of these problems be-
                                                                   fore hitting a 1 hour timeout. In Table 2, we indicate solved
6     Evaluation                                                   problems with ✓, unsolved problems with ✗, and problems
                                                                   that were not attempted with −.
We evaluate our approach on NLA, a benchmark of common
                                                                      The single problem we do not solve, knuth, is the most
numerical algorithms with nonlinear invariants. We first per-
                                                                   difficult problem from a learning perspective. The invariant
form a comparison with two prior works, Numinv and PIE,
                                                                   for the problem, (d 2 ∗q − 4 ∗r ∗d + 4 ∗k ∗d − 2 ∗q ∗d + 8 ∗r ==
that use polynomial equation solving and template learning
                                                                   8 ∗ n) ∧ (mod(d, 2) == 1), is one of the most complex in the
respectively. We then perform an ablation of the methods
                                                                   benchmark. Without considering the external function call
we introduce in this paper. Finally, we evaluate the stability
                                                                   to mod (modular division), there are already 165 potential
of our approach against a baseline CLN model.
Evaluation Environment. The experiments described in               1 LoopInvGen uses the SyGuS competition format, which is an extended

this section were conducted on an Ubuntu 18.04 server with         version of smtlib2.
PLDI ’20, June 15–20, 2020, London, UK                                                          J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu


Table 2. Table of problems requiring nonlinear polynomial          Table 3. Table with ablation of various components in the
invariant from NLA dataset. We additionally tested Code2Inv        G-CLN model. Each column reports which problems can be
on the same problems as PIE and it fails to solve any within       solved with G-CLN when that feature ablated.
1 hour. Numinv results are based on Table 1 in [21]. G-CLN
solves 26 of 27 problems with an average execution time of               Problem Data  Weight Drop- Frac.    Full
53.3 seconds.                                                                    Norm. Reg.   out   Sampling Method
                                                                         divbin   ✗       ✗       ✓          ✓             ✓
  Problem       Degree      # Vars       PIE   NumInv G-CLN              cohendiv ✗       ✗       ✗          ✓             ✓
  divbin        2           5            -     ✓      ✓                  mannadiv ✗       ✗       ✓          ✓             ✓
  cohendiv      2           6            -     ✓      ✓                  hard     ✗       ✗       ✓          ✓             ✓
  mannadiv      2           5            ✗     ✓      ✓                  sqrt1    ✗       ✗       ✗          ✓             ✓
  hard          2           6            -     ✓      ✓                  dijkstra ✗       ✗       ✓          ✓             ✓
  sqrt1         2           4            -     ✓      ✓                  cohencu ✗        ✗       ✓          ✓             ✓
  dijkstra      2           5            -     ✓      ✓                  egcd     ✗       ✓       ✗          ✓             ✓
  cohencu       3           5            -     ✓      ✓                  egcd2    ✗       ✓       ✗          ✓             ✓
  egcd          2           8            -     ✓      ✓                  egcd3    ✗       ✓       ✗          ✓             ✓
  egcd2         2           11           -     ✗      ✓                  prodbin ✗        ✓       ✓          ✓             ✓
  egcd3         2           13           -     ✗      ✓                  prod4br ✗        ✓       ✓          ✓             ✓
  prodbin       2           5            -     ✓      ✓                  fermat1 ✗        ✓       ✓          ✓             ✓
  prod4br       3           6            ✗     ✓      ✓                  fermat2 ✗        ✓       ✓          ✓             ✓
  fermat1       2           5            -     ✓      ✓                  freire1  ✗       ✓       ✓          ✓             ✓
  fermat2       2           5            -     ✓      ✓                  freire2  ✗       ✓       ✗          ✓             ✓
  freire1       2           3            -     ✗      ✓                  knuth    ✗       ✗       ✗          ✗             ✗
  freire2       3           4            -     ✗      ✓                  lcm1     ✗       ✓       ✓          ✓             ✓
  knuth         3           8            -     ✓      ✗                  lcm2     ✗       ✓       ✓          ✓             ✓
  lcm1          2           6            -     ✓      ✓                  geo1     ✗       ✓       ✓          ✓             ✓
  lcm2          2           6            ✗     ✓      ✓                  geo2     ✗       ✓       ✓          ✓             ✓
  geo1          2           5            ✗     ✓      ✓                  geo3     ✗       ✓       ✓          ✓             ✓
  geo2          2           5            ✗     ✓      ✓                  ps2      ✓       ✗       ✓          ✓             ✓
  geo3          3           6            ✗     ✓      ✓                  ps3      ✗       ✗       ✓          ✓             ✓
  ps2           2           4            ✗     ✓      ✓                  ps4      ✗       ✗       ✓          ✓             ✓
  ps3           3           4            ✗     ✓      ✓                  ps5      ✗       ✗       ✓          ✗             ✓
  ps4           4           4            ✗     ✓      ✓                  ps6      ✗       ✗       ✓          ✗             ✓
  ps5           5           4            -     ✓      ✓
  ps6           6           4            -     ✓      ✓

                                                                   term dropouts as well as fractional sampling. Table 3 notes
terms of degree at most 3, nearly twice as many as next most       that data normalization is crucial for nearly all the problems,
complex problem in the benchmark, making it difficult to           especially for preventing high order terms from dominat-
learn a precise invariant with gradient based optimization.        ing the training process. Without weight regularization, the
We plan to explore better initialization and training strategies   problems which involve inequalities over multiple variables
to scale to complex loops like knuth in future work.               cannot be solved; 7 of the 27 problems cannot be solved with-
   Numinv is able to find the equality constraint in this in-      out dropouts, which help avoid the degenerate case where
variant because its approach is specialized for equality con-      the network learns repetitions of the same atomic clause.
straint solving. However, we note that NumInv only infers          Fractional sampling helps to solve high degree (5th and 6th
octahedral inequality constraints and does not in fact infer       order) polynomials as the distance between points grow fast.
the nonlinear and 3 variable inequalities in the benchmark.
   We handle the mod binary function successfully in fermat1       6.3    Stability
and fermat2 indicting the success of our model in support-         We compare the stability of the gated CLNs with standard
ing external function calls. Additionally, for four problems       CLNs as proposed in [30]. Table 4 shows the result. We ran
(egcd2, egcd3, lcm1, and lcm2), we incorporate the дcd ex-         the two CLN methods without automatic restart 20 times
ternal function call as well.                                      per problem and compared the probability of arriving at
                                                                   a solution. We tested on the example problems described
6.2   Ablation Study                                               in [30] with disjunction and conjunction of equalities, two
We conduct an ablation study to demonstrate the benefits           problems from Code2Inv, as well as ps2 and ps3 from NLA.
gained by the normalization/regularization techniques and          As we expected, our regularization and gated t-norms vastly
Learning Nonlinear Loop Invariants with G-CLNs                                                  PLDI ’20, June 15–20, 2020, London, UK


                                                                    Neural Networks for Invariant Inference. Recently, neu-
Table 4. Table comparing the stability of CLN2INV with our          ral networks have been applied to loop invariant inference.
method. The statistics reported are over 20 runs per problem        Code2Inv combines graph and recurrent neural networks
with randomized initialization.                                     to model the program graph and learn from counterexam-
                                                                    ples [35]. In contrast, CLN2INV uses CLNs to learn SMT
       Problem      Convergence Rate       Convergence Rate         formulas for invariants directly from program data [30]. We
                        of CLN                of G-CLN              also use CLNs but incorporate gating and other improve-
        Conj Eq             75%                   95%               ments to be able to learn general nonlinear loop invariants.
        Disj Eq             50%                  100%               Polynomial Invariants. There have been efforts to uti-
      Code2Inv 1            55%                   90%               lize abstract interpretation to discover polynomial invari-
      Code2Inv 11           70%                  100%               ants [28, 29]. More recently, Compositional Recurrance Anal-
          ps2               70%                  100%
                                                                    ysis (CRA) performs analysis on abstract domain of transition
          ps3               30%                  100%
                                                                    formulas, but relies on over approximations that prevent it
                                                                    from learning sufficient invariants [9, 18, 19]. Data-driven
improves the stability of the model as clauses with poorly
                                                                    methods based on linear algebra such as Guess-and-Check
initialized weights can be ignored by the network. We saw
                                                                    are able to learn polynomial equality invariants accurately
improvements across all the six problems, with the baseline
                                                                    [33]. Guess-and-check learns equality invariants by using
CLN model having an average convergence rate of 58.3%,
                                                                    the polynomial kernel, but it cannot learn disjunctions and
and the G-CLN converging 97.5% of the time on average.
                                                                    inequalities, which our framework supports natively.
6.4     Linear Invariant Dataset                                       NumInv [21, 23, 24] uses the polynomial kernel but also
                                                                    learns octahedral inequalities. NumInv sacrifices soundness
We evaluate our system on the Code2Inv benchmark [35]               for performance by replacing Z3 with KLEE, a symbolic
of 133 linear loop invariant inference problems with source         executor, and in particular, treats invariants which lead to
code and SMT loop invariant checks. We hold out 9 problems          KLEE timeouts as valid. Our method instead is sound and
shown to be theoretically unsolvable in [30]. Our system            learns more general inequalities than NumInv.
finds correct invariants for all remaining 124 theoretically
solvable problems in the benchmark in under 30s.                    8   Conclusion
                                                                    We introduce G-CLNs, a new gated neural architecture that
7      Related Work                                                 can learn general nonlinear loop invariants. We addition-
Numerical Relaxations. Inductive logic programming (ILP)            ally introduce Fractional Sampling, a method that soundly
has been used to learn a logical formula consistent with a set      relaxes program semantics to perform dense sampling, and
of given data points. More recently, efforts have focused on        PBQU activations, which naturally learn tight inequality
differentiable relaxations of ILP for learning [8, 17, 27, 38] or   bounds for verification. We evaluate our approach on a set of
program synthesis [36]. Other recent efforts have used formu-       27 polynomial loop invariant inference problems and solve
las as input to graph and recurrent nerual networks to solve        26 of them, 3 more than prior work, as well as improving
Circuit SAT problems and identify Unsat Cores [1, 31, 32].          convergence rate to 97.5% on quadratic problems, a 39.2%
FastSMT also uses a neural network select optimal SMT               improvement over CLN models.
solver strategies [3]. In contrast, our work relaxes the seman-
tics of the SMT formulas allowing us to learn SMT formulas.
Counterexample-Driven Invariant Inference. There is                 Acknowledgements
a long line of work to learn loop invariants based on coun-         The authors are grateful to our shepherd, Aditya Kanade,
terexamples. ICE-DT uses decision tree learning and lever-          and the anonymous reviewers for valuable feedbacks that
ages counterexamples which violate the inductive verifica-          improved this paper significantly. This work is sponsored in
tion condition [11, 12, 39]. Combinations of linear classifiers     part by NSF grants CNS-18-42456, CNS-18-01426, CNS-16-
have been applied to learning CHC clauses [39].                     17670, CCF-1918400; ONR grant N00014-17-1-2010; an ARL
   A state-of-the-art method, LoopInvGen (PIE) learns the           Young Investigator (YIP) award; an NSF CAREER award; a
loop invariant using enumerative synthesis to repeatedly            Google Faculty Fellowship; a Capital One Research Grant;
add data consistent clauses to strengthen the post-condition        a J.P. Morgan Faculty Award; a Columbia-IBM Center Seed
until it becomes inductive [25, 26, 34]. For the strengthening      Grant Award; and a Qtum Foundation Research Gift. Any
procedure, LoopInvGen uses PAC learning, a form of boolean          opinions, findings, conclusions, or recommendations that
formula learning, to learn which combination of candidate           are expressed herein are those of the authors, and do not
atomic clauses is consistent with the observed data. In con-        necessarily reflect those of the US Government, ONR, ARL,
trast, our system learn invariants from trace data.                 NSF, Google, Capital One J.P. Morgan, IBM, or Qtum.
PLDI ’20, June 15–20, 2020, London, UK                                                                               J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu


References                                                                           of Software Engineering. ACM, 605–615.
 [1] Saeed Amizadeh, Sergiy Matusevych, and Markus Weimer. 2019.                [22] ThanhVu Nguyen, Deepak Kapur, Westley Weimer, and Stephanie
     Learning To Solve Circuit-SAT: An Unsupervised Differentiable Ap-               Forrest. 2012. Using dynamic analysis to discover polynomial and
     proach. In International Conference on Learning Representations. https:         array invariants. In Proceedings of the 34th International Conference on
     //openreview.net/forum?id=BJxgz2R9t7                                            Software Engineering. IEEE Press, 683–693.
 [2] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. 2014. Neural           [23] ThanhVu Nguyen, Deepak Kapur, Westley Weimer, and Stephanie
     machine translation by jointly learning to align and translate. arXiv           Forrest. 2012. Using dynamic analysis to discover polynomial and
     preprint arXiv:1409.0473 (2014).                                                array invariants. In Proceedings of the 34th International Conference on
 [3] Mislav Balunovic, Pavol Bielik, and Martin Vechev. 2018. Learning               Software Engineering. IEEE Press, 683–693.
     to solve SMT formulas. In Advances in Neural Information Processing        [24] Thanhvu Nguyen, Deepak Kapur, Westley Weimer, and Stephanie
     Systems. 10317–10328.                                                           Forrest. 2014. DIG: a dynamic invariant generator for polynomial
 [4] A. Biere, H. van Maaren, and T. Walsh. 2009. Handbook of Satisfiability:        and array invariants. ACM Transactions on Software Engineering and
     Volume 185 Frontiers in Artificial Intelligence and Applications. IOS           Methodology (TOSEM) 23, 4 (2014), 30.
     Press, Amsterdam, The Netherlands, The Netherlands.                        [25] Saswat Padhi and Todd D. Millstein. 2017. Data-Driven Loop Invariant
 [5] Andreas Blass and Yuri Gurevich. 2001. Inadequacy of computable                 Inference with Automatic Feature Synthesis. CoRR abs/1707.02029
     loop invariants. ACM Transactions on Computational Logic (TOCL) 2,              (2017). arXiv:1707.02029 http://arxiv.org/abs/1707.02029
     1 (2001), 1–11.                                                            [26] Saswat Padhi, Rahul Sharma, and Todd Millstein. 2016. Data-driven
 [6] Werner Damm, Guilherme Pinto, and Stefan Ratschan. 2005. Guaran-                precondition inference with learned features. ACM SIGPLAN Notices
     teed termination in the verification of LTL properties of non-linear            51, 6 (2016), 42–56.
     robust discrete time hybrid systems. In International Symposium on         [27] Ali Payani and Faramarz Fekri. 2019. Inductive Logic Program-
     Automated Technology for Verification and Analysis. Springer, 99–113.           ming via Differentiable Deep Neural Logic Networks. arXiv preprint
 [7] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT               arXiv:1906.03523 (2019).
     solver. In International conference on Tools and Algorithms for the Con-   [28] Enric Rodríguez-Carbonell and Deepak Kapur. 2004. Automatic gen-
     struction and Analysis of Systems. Springer, 337–340.                           eration of polynomial loop invariants: Algebraic foundations. In Pro-
 [8] Richard Evans and Edward Grefenstette. 2018. Learning explanatory               ceedings of the 2004 international symposium on Symbolic and algebraic
     rules from noisy data. Journal of Artificial Intelligence Research 61           computation. ACM, 266–273.
     (2018), 1–64.                                                              [29] Enric Rodríguez-Carbonell and Deepak Kapur. 2007. Generating all
 [9] Azadeh Farzan and Zachary Kincaid. 2015. Compositional recurrence               polynomial invariants in simple loops. Journal of Symbolic Computa-
     analysis. In 2015 Formal Methods in Computer-Aided Design (FMCAD).              tion 42, 4 (2007), 443–476.
     IEEE, 57–64.                                                               [30] Gabriel Ryan, Justin Wong, Jianan Yao, Ronghui Gu, and Suman Jana.
[10] Carlo A Furia, Bertrand Meyer, and Sergey Velder. 2014. Loop invari-            2020. CLN2INV: Learning Loop Invariants with Continuous Logic
     ants: Analysis, classification, and examples. ACM Computing Surveys             Networks. In International Conference on Learning Representations.
     (CSUR) 46, 3 (2014), 34.                                                        https://openreview.net/forum?id=HJlfuTEtvB
[11] Pranav Garg, Christof Löding, P Madhusudan, and Daniel Neider.             [31] Daniel Selsam and Nikolaj Bjørner. 2019. Guiding high-performance
     2014. ICE: A robust framework for learning invariants. In International         SAT solvers with unsat-core predictions. In International Conference
     Conference on Computer Aided Verification. Springer, 69–87.                     on Theory and Applications of Satisfiability Testing. Springer, 336–353.
[12] Pranav Garg, Daniel Neider, Parthasarathy Madhusudan, and Dan              [32] Daniel Selsam, Matthew Lamm, Benedikt Bünz, Percy Liang, Leonardo
     Roth. 2016. Learning invariants using decision trees and implication            de Moura, and David L. Dill. 2019. Learning a SAT Solver from Single-
     counterexamples. In ACM Sigplan Notices, Vol. 51. ACM, 499–512.                 Bit Supervision. In International Conference on Learning Representations.
[13] Felix A Gers, Jürgen Schmidhuber, and Fred Cummins. 1999. Learning              https://openreview.net/forum?id=HJMC_iA5tm
     to forget: Continual prediction with LSTM. (1999).                         [33] Rahul Sharma, Saurabh Gupta, Bharath Hariharan, Alex Aiken, Percy
[14] Petr Hájek. 2013. Metamathematics of fuzzy logic. Vol. 4. Springer              Liang, and Aditya V Nori. 2013. A data driven approach for algebraic
     Science & Business Media.                                                       loop invariants. In European Symposium on Programming. Springer,
[15] Charles Antony Richard Hoare. 1969. An axiomatic basis for computer             574–592.
     programming. Commun. ACM 12, 10 (1969), 576–580.                           [34] Rahul Sharma, Saurabh Gupta, Bharath Hariharan, Alex Aiken, and
[16] Sergey Ioffe and Christian Szegedy. 2015. Batch normalization: Ac-              Aditya V Nori. 2013. Verification as learning geometric concepts. In
     celerating deep network training by reducing internal covariate shift.          International Static Analysis Symposium. Springer, 388–411.
     arXiv preprint arXiv:1502.03167 (2015).                                    [35] Xujie Si, Hanjun Dai, Mukund Raghothaman, Mayur Naik, and Le Song.
[17] Angelika Kimmig, Stephen Bach, Matthias Broecheler, Bert Huang,                 2018. Learning loop invariants for program verification. In Advances
     and Lise Getoor. 2012. A short introduction to probabilistic soft logic.        in Neural Information Processing Systems. 7751–7762.
     In Proceedings of the NIPS Workshop on Probabilistic Programming:          [36] Xujie Si, Mukund Raghothaman, Kihong Heo, and Mayur Naik. 2019.
     Foundations and Applications. 1–4.                                              Synthesizing datalog programs using numerical relaxation. In Proceed-
[18] Zachary Kincaid, Jason Breck, Ashkan Forouhi Boroujeni, and Thomas              ings of the 28th International Joint Conference on Artificial Intelligence.
     Reps. 2017. Compositional recurrence analysis revisited. ACM SIG-               AAAI Press, 6117–6124.
     PLAN Notices 52, 6 (2017), 248–262.                                        [37] Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever,
[19] Zachary Kincaid, John Cyphert, Jason Breck, and Thomas Reps. 2017.              and Ruslan Salakhutdinov. 2014. Dropout: a simple way to prevent
     Non-linear reasoning for invariant synthesis. Proceedings of the ACM            neural networks from overfitting. The journal of machine learning
     on Programming Languages 2, POPL (2017), 1–33.                                  research 15, 1 (2014), 1929–1958.
[20] Hai Lin, Panos J Antsaklis, et al. 2014. Hybrid dynamical systems: An      [38] Fan Yang, Zhilin Yang, and William W Cohen. 2017. Differentiable
     introduction to control and verification. Foundations and Trends® in            learning of logical rules for knowledge base reasoning. In Advances in
     Systems and Control 1, 1 (2014), 1–172.                                         Neural Information Processing Systems. 2319–2328.
[21] ThanhVu Nguyen, Timos Antonopoulos, Andrew Ruef, and Michael               [39] He Zhu, Stephen Magill, and Suresh Jagannathan. 2018. A data-driven
     Hicks. 2017. Counterexample-guided approach to finding numerical                CHC solver. In ACM SIGPLAN Notices, Vol. 53. ACM, 707–721.
     invariants. In Proceedings of the 2017 11th Joint Meeting on Foundations
Learning Nonlinear Loop Invariants with G-CLNs                                                                PLDI ’20, June 15–20, 2020, London, UK


A     Proof for Theorem 3.1                                                    equivalent SMT formula Fi using Algorithm 1 according to
Property 1. ∀t u, (t > 0) ∧ (u > 0) =⇒ (t ⊗ u > 0).                            the induction hypothesis. Again we just prove the full model
Theorem 3.1. For a gated CLN model M with input nodes                          M and the extracted formula F satisfy Eq. (8).
{x 1 , x 2 , ..., x n } and output node p, if all gating parameters               From line 7-10 in Algorithm 1, we know that the extracted
{дi } are either 0 or 1, then using the formula extraction                     formula F is the disjunction of a subset of formulas Fi if the
algorithm, the recovered SMT formula F is equivalent to the                    Fi is activated (дi > 0.5). Because in our setting all gating
gated CLN model M. That is, ∀x ∈ R n ,                                         parameters are either 0 or 1, then a logical equivalent form
                                                                               of F can be derived.
     F (x) = T rue ⇐⇒         lim         M(x; c 1 , c 2 , σ , ϵ) = 1    (8)
                          c 1 →0,c 2 →∞
                           σ →0,ϵ →0
                                                                                                F (x) = ∨ni=1 ((дi = 1) ∧ Fi (x))              (13)
    F (x) = False ⇐⇒          lim         M(x; c 1 , c 2 , σ , ϵ) = 0    (9)       Under the t-conorm case, we have
                          c 1 →0,c 2 →∞
                           σ →0,ϵ →0                                                     M(x) = TG′ (M1 (x), ..., Mn (x); д1 , ..., дn ) =
as long as the t-norm in M satisfies Property 1.                                         1 − (1 − д1 M1 (x)) ⊗ ... ⊗ (1 − дn Mn (x))
Proof. We prove this by induction.                                             Using Property 1 we can prove that
T-norm Case. If p = TG (M1 , ..., Mn ; д1 , ..., дn ) which means                     M(x) = 1 ⇐⇒ ∃i ∈ {1, ..., n}, 1 − дi Mi (x) = 0
the final operation in M is a gated t-norm, we know that
for each submodel M1 , ..., Mn the gating parameters are all                   Because the gating parameter дi is either 0 or 1, we further
either 0 or 1. According to the induction hypothesis, for each                 have
Mi , using Algorithm 1, we can extract an equivalent SMT                            M(x) = 1 ⇐⇒ ∃i ∈ {1, ..., n}, дi = 1 ∧ Mi = 1              (14)
formula Fi satisfying Eq. (8)(9). Now we prove the full model                      Combining Eq. (10)(13)(14), we will finally have
M and the extracted formula F satisfy Eq. (8). The proof for
Eq. (9) is similar and omitted for brevity. For simplicity we                  F (x) = T rue ⇐⇒ ∃i ∈ {1, ..., n}, (дi = 1) ∧ Fi (x) = T rue
use M(x) to denote lim σ →0,ϵ →0 M(x; c 1 , c 2 , σ , ϵ).                          ⇐⇒ ∃i ∈ {1, ..., n}, (дi = 1) ∧ Mi (x) = 1
                           c 1 →0,c 2 →∞
   Now the proof goal becomes F (x) = T rue ⇐⇒ M(x) =                              ⇐⇒ M(x) = 1
1, and the induction hypothesis is                                             Negation Case. If p = 1 − M1 which means the final oper-
      ∀i ∈ {1, ..., n}, Fi (x) = T rue ⇐⇒ Mi (x) = 1                    (10)   ation is a negation, from the induction hypothesis we know
                                                                               that using Algorithm 1 we can extract an SMT formula F 1
   From line 2-5 in Algorithm 1, we know that the extracted                    from submodel M1 satisfying Eq. (8)(9). From line 11-12 in
formula F is the conjunction of a subset of formulas Fi if the                 Algorithm 1 we know that the extracted formula for M is
Fi is activated (дi > 0.5). Because in our setting all gating                  F = ¬F 1 . Now we show such an F satisfy Eq. (8)(9).
parameters are either 0 or 1, then a logical equivalent form
of F can be derived.                                                                 F (x) = T rue ⇐⇒ F 1 (x) = False ⇐⇒ M 1 (x) = 0

                 F (x) = ∧ni=1 ((дi = 0) ∨ Fi (x))                      (11)          ⇐⇒ M(x) = 1
                                                                                     F (x) = False ⇐⇒ F 1 (x) = T rue ⇐⇒ M 1 (x) = 1
    Recall we are considering the t-norm case where
                                                                                      ⇐⇒ M(x) = 0
       M(x) = TG (M1 (x), ..., Mn (x); д1 , ..., дn ) =
                                                                               Atomic Case. In this case, the model M consists of only
       (1 + д1 (M1 (x) − 1)) ⊗ ... ⊗ (1 + дn (Mn (x) − 1))
                                                                               a linear layer and an activation function, with no logical
Using the properties of a t-norm in §2.2 we can prove that                     connectiveness. This degenerates to the atomic case for the
 M(x) = 1 ⇐⇒ ∀i ∈ {1, ..., n}, (1 + дi (Mi (x) − 1)) = 1                       ungated CLN in [30] where the proof can simply be reused.
                                                                                                                                         □
Because the gating parameter дi is either 0 or 1, we further
have                                                                           B     Proof for Theorem 3.2
    M(x) = 1 ⇐⇒ ∀i ∈ {1, ..., n}, дi = 0 ∨ Mi = 1                       (12)   Recall our continuous mapping for inequalities.
                                                                                                                c2
    Combining Eq. (10)(11)(12), we will finally have                                                       (t −u)12 +c 2 t < u
                                                                                                          
                                                                                                          
                                                                                              S(t ≥ u) ≜
                                                                                                          
                                                                                                                       1                   (15)
F (x) = T rue ⇐⇒ ∀i ∈ {1, ..., n}, (дi = 0) ∨ Fi (x) = T rue                                                    c2
                                                                                                           (t −u)22 +c 2 t ≥ u
                                                                                                          
  ⇐⇒ ∀i ∈ {1, ..., n}, (дi = 0) ∨ Mi (x) = 1                                                                           2
                                                                                                          
                                                                               Theorem 3.2. Given a set of n k-dimensional samples    √ with
  ⇐⇒ M(x) = 1                                                                  the maximum L2-norm l, if c 1 ≤ 2l and c 1 · c 2 ≥ 8 nl 2 , and
T-conorm Case. If p = TG′ (M1 , ..., Mn ; д1 , ..., дn ) which                 the weights are constrained as w 12 + ... + w k2 = 1, then when
means the final operation in M is a gated t-conorm, similar                    the model √ converges, the learned inequality has distance at
to the t-norm case, for each submodel Mi we can extract its                    most c 1 / 3 from a ’desired’ inequality.
PLDI ’20, June 15–20, 2020, London, UK                                                                                      J. Yao, G. Ryan, J. Wong, S. Jana, R. Gu

                                                                                                                                  √
Proof. The model maximize the overall continuous truth                           since f ′(x) is strictly increasing in (∞, −c 1 / 3), we can ob-
value, so the reward function is                                                 tain a stronger lower bound
                              n
                              Õ                                                     f ′(w 1x 11 + ... + w k x 1k + b) ≥ f ′(−l − l) = f ′(−2l)                 (22)
      R(w 1 , ..., w k , b) =   f (w 1x i1 + ... + w k x ik + b)
                                 i=1
                                                                                 Put it altogether, we have
where f (x) = S(x ≥ 0). We first want to prove that, if                                  ∂R
                                                                                             = f ′(w 1x 11 + ... + w k x 1k + b)+
there exists a √point that breaks the inequality with distance                           ∂b
                                                                                          n
more than c 1 / 3, then ∂R    ∂b > 0, indicating the model will not
                                                                                         Õ
                                                                                             f ′(w 1x i1 + ... + w k x ik + b)
converge here. Without loss of generality, we assume the                                 i=2
first point {x 11 , ...x 1k } breaks the inequality, i.e.,                               ≥ f ′(−2l) + (n − 1)f ′(2l) > f ′(−2l) + n f ′(2l)
                                                √
             w 1x i1 + ... + w k x ik + b + C1/ 3 < 0          (16)                                           4l                         64nl 4
                                                                                         >                                      · (1 −            )
We will consider the following two cases.
                                                                                                          2             2
                                                                                             c 12 (1 + 4lc 2 )2 (1 + 4lc 2 )2            c 12c 22
                                                                                                         1              2
 (i) All the points breaks the inequality, i.e.                                  Some intermediate steps are omitted. Because we know
                                                                                           √
             ∀i ∈ {1, ..., n}, w 1x i1 + ... + w k x ik + b < 0                  c 1c 2 ≥ 8 nl 2 , finally we have ∂R
                                                                                                                   ∂b > 0.
                                                                                     Now we have proved that   √  no point can break the learned
From Eq. (15), it is easy to see that
                                                                                 inequality more than c 1 / 3. We need to prove at least one
                        f (x) > 0 x < 0
                      ′
                                                                                 point is on or beyond the boundary. We prove this by con-
                                                                          (17)
                        f ′(x) < 0 x > 0                                         tradiction. Suppose all points satisfy
Then we have                                                                                          w 1x i1 + ... + w k x ik + b > 0
           n                                      n                              Then we have
     ∂R Õ ′                                      Õ
        =     f (w 1x i1 + ... + w k x ik + b) >     0=0                              ∂R Õ ′
                                                                                            n                                      n
     ∂b
                                                                                                                                  Õ
          i=1                                    i=1                                     =     f (w 1x i1 + ... + w k x ik + b) <     0=0
                                                                                      ∂b
  (ii) At least one point, say, {x j1 , ..., x jk }, satisfies the in-                     i=1                                    i=1

equality.                                                                        So the model does not converge, which concludes the proof.
                                                                                                                                        □
                      w 1x j1 + ... + w k x jk + b ≥ 0                    (18)
From CauchyâĂŞSchwarz inequality, ∀i ∈ {1, ..., n} we have
     (w 1x i1 + ... + w k x ik )2 ≤ (w 12 + ... + w k2 )(x i1
                                                           2
                                                              + ... + x ik
                                                                        2
                                                                           )
     = 1 · (x i1
              2
                 + ... + x ik
                           2
                              ) ≤ l2
So
            ∀i ∈ {1, ..., n}, −l ≤ w 1x i1 + ... + w k x ik ≤ l           (19)
Combining Eq. (16)(18)(19), a lower bound and an upper
bound of b can be obtained
                                     √
                   −l ≤ b < l − c 1 / 3            (20)

                            √ can show√that f (x) is strictly in-
Using basic calculus we                            ′

creasing in (−∞,√    −c 1 / 3)√ and (c 2 / 3, +∞), and strictly de-
creasing in (−c 1 / 3, c 2 / 3). Combining Eq. (17)(19)(20), we
have
 f ′(w 1x i1 + ... + w k x ik + b) ≥ f ′(|w 1x i1 + ... + w k x ik + b|)
 ≥ f ′(|w 1x i1 + ... + w k x ik | + |b |) ≥ f ′(l + l) = f ′(2l)
                                                                          (21)
                                                            √
The deduction of Eq. (21) requires 2l ≤ C2/ 3, which can
          √ from the two known conditions c 1 ≤ 2l and
be obtained
c 1c 2 ≥ 8 nl 2 .
    Eq. (21) provides a lower bound of the derivative for any
point. For the point that breaks the inequality in Eq. (16),
