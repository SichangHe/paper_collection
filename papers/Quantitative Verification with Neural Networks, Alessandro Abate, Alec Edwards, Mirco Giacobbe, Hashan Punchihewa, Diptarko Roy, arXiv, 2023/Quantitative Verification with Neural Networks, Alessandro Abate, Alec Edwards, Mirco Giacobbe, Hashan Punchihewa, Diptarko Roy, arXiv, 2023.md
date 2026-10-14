Logical Methods in Computer Science
Volume 22, Issue 2, 2026, pp. 4:1–4:26                                                           Submitted       Mar. 21, 2024
https://lmcs.episciences.org/                                                                    Published       Apr. 15, 2026




         QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS

                               a                                                       b
 ALESSANDRO ABATE                  , ALEC EDWARDS , MIRCO GIACOBBE                         , HASHAN PUNCHIHEWA,
                                           AND DIPTARKO ROY b
   a
        Department of Computer Science, University of Oxford, UK
        e-mail address: alessandro.abate@cs.ox.ac.uk
    b
        School of Computer Science, University of Birmingham, UK
        e-mail address: m.giacobbe@bham.ac.uk, d.s.roy@bham.ac.uk


           Abstract. We present a data-driven approach to the quantitative verification of proba-
           bilistic programs and stochastic dynamical models. Our approach leverages neural networks
           to compute tight and sound bounds for the probability that a stochastic process hits
           a target condition within finite time. This problem subsumes a variety of quantitative
           verification questions, from the reachability and safety analysis of discrete-time stochastic
           dynamical models, to the study of assertion-violation and termination analysis of proba-
           bilistic programs. We rely on neural networks to represent supermartingale certificates that
           yield such probability bounds, which we compute using a counterexample-guided inductive
           synthesis loop: we train the neural certificate while tightening the probability bound over
           samples of the state space using stochastic optimisation, and then we formally check the
           certificate’s validity over every possible state using satisfiability modulo theories; if we
           receive a counterexample, we add it to our set of samples and repeat the loop until validity
           is confirmed. We demonstrate on a diverse set of benchmarks that, thanks to the expressive
           power of neural networks, our method yields smaller or comparable probability bounds
           than existing symbolic methods in all cases, and that our approach succeeds on models
           that are entirely beyond the reach of such alternative techniques.




                                                   1. Introduction
Probabilistic programs extend imperative programs with the ability to sample from proba-
bility distributions [DS20, GHNR14, Koz81, MM05], which provides an expressive language
to describe randomized algorithms, cryptographic protocols, and Bayesian inference schemes.
Discrete-time stochastic dynamical models, characterised by stochastic difference equations,
are a natural framework to describe auto-regressive time series, as well as sequential decision
and planning problems in unknown environments. A fundamental quantitative verification
problem for probabilistic programs and stochastic dynamical models is the quantitative
   Key words and phrases: Data-driven Verification, Quantitative Verification, Probabilistic Programs,
Stochastic Dynamical Models, Counterexample-guided Inductive Synthesis, Neural Networks.
 ∗
   The conference version of this manuscript appeared at CONCUR 2023 [AEG+ 23].
   This work was supported in part by Innovate UK under the HICLASS project, EPSRC Centre for Doctoral
Training in Autonomous Intelligent Machines and Systems (EP/S024050/1) and EPSRC Doctoral Training
Partnership, Google DeepMind Scholarship, Advanded Research and Invention Agency under the Safeguarded
AI programme.



l       LOGICAL METHODS
        IN COMPUTER SCIENCE         DOI:10.46298/LMCS-22(2:4)2026
                                                                    © A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy
                                                                    ⃝
                                                                    CC Creative Commons
4:2            A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy            Vol. 22:2




reachability question, which amounts to finding the probability with which the system
reaches a given target condition within a finite number of steps. Reachability is at the
core of a variety of other important quantitative verification questions as, by selecting
appropriate target conditions on the state space, we can express the probability that a
probabilistic program terminates or that it violates an assertion, as well as the probability
that a stochastic dynamical model satisfies an invariant or remains within a set of safe
configurations.
     Quantitative reachability verification has been studied extensively using theories and
algorithms built upon symbolic reasoning techniques, such as quantitative calculi [MM02,
MMS96], probabilistic model checking algorithms [KNP05, FKN+ 11], discrete abstrac-
tions of stochastic dynamical models [AKM11, TMKA17, SA12], and the synthesis of
supermartingale-like certificates [CS13, CFG16, CNv17, CFNH18, LSAZ22]. Among the
latter class, a method to provide a sound upper bound for the reachability probability of
a system is to synthesise a supermartingale function that maps every reachable state to a
non-negative real, whose value is never smaller than 1 inside the target condition, and such
that it never increases in expectation as the system evolves outside of the target. This is
referred to as a non-negative repulsing supermartingale or stochastic invariant indicator in
the literature [TOUH21, CGMv22, CNv17], and its output over a given state provides an
upper bound for the probability that the system reaches the target condition from that state.
Symbolic methods for the synthesis of such certificates assume that the supermartingale
function, as well as its post-expectation, which depends on the model constraints and
distributions, are both in linear or polynomial form. This poses syntactic restrictions to
their applicability.
     Data-driven and counterexample-guided inductive synthesis (CEGIS) procedures, com-
bined with machine learning approaches that leverage neural networks to represent certificates,
have shown great promise in mitigating the aforementioned limitation [CRG19, AAGP21,
GKP22, PAA21, MCL23, AGR21, LvCH22, vLHC23, vLV+ 23, GKPT24, NMTZ24, NGL25].
In particular, neural-based CEGIS decouples the task of guessing a certificate from that of
checking its validity, delegating the guessing task to efficient machine learning algorithms
that leverage the expressive power of neural networks, while confining symbolic reasoning to
the checking part of the task, which is computationally easier to solve in isolation than the
entire synthesis problem. CEGIS has been applied to the synthesis of neural supermartingales
for the almost-sure termination analysis of probabilistic programs [AGR21], as well as their
counterpart for stochastic dynamical models with applications to qualitative queries such as
almost-sure safety and stability [MCL23, LvCH22].
     In this paper, we present theory, methods, and an extensive experimental evaluation
to demonstrate the efficacy and flexibility of neural supermartingales to solve quantitative
verification questions for probabilistic programs and stochastic dynamical models, using
machine learning combined with satisfiability modulo theories (SMT) technologies.

Theory: We use the theory of non-negative repulsing supermartingales [TOUH21, Section
    4] to leverage neural networks as representations of supermartingale functions for
    quantitative verification, while exploiting SMT solving to guarantee soundness.
Methods: We present a CEGIS-based approach to train neural supermartingale functions
    that minimise an upper bound for the reachability probability over sample points from
    the state space, and check their validity over every possible state using SMT solving.
    We present a program-agnostic approach that relies on state samples in the training
Vol. 22:2             QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                          4:3




     v ∈ Vars                                                                   (variables)
    N ∈R                                                                       (numerals)
     E ::= v | N | -E | E + E | E − E | E ∗ E | . . .             (arithmetic expressions)
     P ::= Bernoulli( E ) | Gaussian( E, E ) | . . .            (probability distributions)
     B ::= true | !B | B && B | B||B | E == E | E < E | . . .       (Boolean expressions)
     C ::= skip                                                       (update commands)
            | v=E                                               (deterministic assignment)
            |v ∼ P                                              (probabilistic assignment)
            |C ;C                                                 (sequential composition)
            | if B then C else C fi                             (conditional composition)

       Figure 1: Grammar for update commands, Boolean and arithmetic expressions.

    phase, and also a novel program-aware approach that embeds model information in
    the loss function to enhance the effectiveness of stochastic optimisation.
Experiments: We build a prototype implementation and compare the efficacy of our
    method with the state of the art in synthesis of linear supermartingales using symbolic
    reasoning [TOUH21]. We show that our program-aware approach computes tighter
    or comparable probability bounds than symbolic reasoning on existing benchmarks,
    while our program-agnostic approach matches it in over half of the instances. We
    additionally demonstrate that both our approaches can handle models beyond reach
    of purely symbolic methods.


            2. Probabilistic Programs and Stochastic Dynamical Models
Probabilistic programs are computer programs whose execution is determined by random
variables, and stochastic dynamical models describe discrete-time dynamical systems with
probabilistic behaviour. The earlier enjoy the flexibility of imperative programming con-
structs and are used to describe randomised algorithms, and the latter are expressed as
stochastic difference equations and are used to describe probabilistic systems that evolve
over infinite time. The semantics of both can be described in terms of stochastic processes
and, for this reason, verification questions for both can be solved with similar techniques.
    The syntax of our modeling framework uses imperative constructs from probabilistic
programs and defines executions over infinite time as dynamical systems. Specifically, we
consider programs that operate over an ordered set of n real-valued variables, denoted
by Vars, and update their values through the repeated execution of a command C whose
grammar is described in Figure 1. Under this definition, a state of the system is an n-
dimensional vector s ∈ Rn that assigns a value to each variable symbol. The update command
C defines an update function f : Rn × [0, 1]m → Rn , where m is the number of syntactic
probabilistic assignment statements occurring in C, which maps the current state and m
random variables uniformly distributed in [0, 1] into the next state. Conceptually, within f ,
each random variable is mapped into its respective distribution by applying the appropriate
inverse transformation. Altogether, our probabilistic program defines a stochastic process,
4:4             A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy             Vol. 22:2




whose behaviour is determined by the following stochastic difference equation:
                                  st+1 = f (st , rt ),   rt ∼ Um ,                          (2.1)
where rt is an m-dimensional random input sampled at time t from the uniform distribution
Um over the m-dimensional hypercube [0, 1]m . The initial state s0 is either given as a
deterministic assignment to constant values, or is non-deterministically chosen from a
set of initial conditions S0 characterized by a Boolean expression. This setting can be
seen as an assertion about the initial conditions followed by the probabilistic program
while true do C od. As we show in Section 3, this allows us to characterise verification
questions such as termination, non-termination, invariance and assertion-violation for while
loops with general guards, as well as reachability and safety verification questions for
dynamical models with general stochastic disturbances.
    The semantics of our model is defined as a stochastic process induced by the Markov
chain over the probability space of infinite words of random samples. This is defined by the
probability space triple (Ω, F, P) [BS96, HLL96], where
• Ω is the set of infinite sequences ([0, 1]m )ω of m-dimensional tuples of values in [0, 1],
• F is the extension of the Borel σ-algebra over the unit interval B([0, 1]) to Ω,
• P is the extension of the Lebesgue measure on [0, 1] to Ω.
     Every initialisation of the system on state s ∈ Rn induces a stochastic process {Xts }t∈N
over the state space Rn . Let ω = r0 r1 r2 . . . be an infinite sequence of random samples in
[0, 1]m , then the stochastic process is defined by the sequence of random variables
                           s
                          Xt+1 (ω) = f (Xts (ω), rt ),       X0s (ω) = s.                   (2.2)
This defines the natural filtration {Ft }t∈N , which is the smallest filtration to which the
stochastic process Xts is adapted. In other words [Kal06], this can be seen as another Markov
chain with state space Rn and transition kernel
                         T (s, S ′ ) = Leb r ∈ [0, 1]m | f (s, r) ∈ S ′ ,
                                                                       
                                                                                         (2.3)
where S ′ is a Borel measurable subset of Rn and Leb refers to the Lebesgue measure of a
measurable subset of [0, 1]m . In other words, kernel T denotes the probability to transition
from state s into a set of states S ′ . The transition kernel also defines the post-expectation
operator X, also known as the next-time operator [TOUH21, Definition 2.16]. X can be
applied to an arbitrary Borel-measurable function h : Rn → R defining the post-expectation
of h, denoted by X[h] and defined as the following function over states:
                                             Z
                                 X[h](s) = h(s′ ) T (s, ds′ ).                             (2.4)

This represents the expected value of h evaluated at the next state, given the current state
being s. Computing the symbolic representation of a post-expectation for probabilistic
programs and stochastic dynamical models is a core problem in probabilistic verifica-
tion [GMV16, GSV20]. Indeed, our theoretical framework builds upon the post-expectation
(cf. Eq. (5.1b)), and our verification procedure uses a symbolic representation of the post-
expectation (cf. Section 6.2) as well as our program-aware learning procedure, while our
program-agnostic learning procedure approximates it statistically (cf. Section 6.1).
     We remark that our model encompasses general probabilistic program loops as well as
stochastic dynamical systems with general disturbances. For example, a probabilistic loop
Vol. 22:2             QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                            4:5




with guard condition B and body C in the form
                                       while B do C od                                       (2.5)
can be expressed as a loop with guard true and body if B then C else skip fi. This
expresses the fact that, after termination, the program will stay on the terminal state
indefinitely. Also, discrete-time stochastic difference equations with a nonlinear vector field
g and time-invariant input disturbance with an arbitrary distribution W in the form
                                  st+1 = g(st , wt ),   wt ∼ W,                              (2.6)
comply with our model. It is sufficient to derive wt with an appropriate inverse transformation
from the uniform distribution and embed it in the update function f (Eq. (2.1)), to simulate
a function g that accepts random inputs wt distributed according to distribution W. Note
that this is without loss of generality; we do not require f to be continuous and we do
not require it to be differentiable, and therefore we can represent any distribution using
the inverse CDF method, as is standard in stochastic simulation [AG07, Chapter 2, p.36].
Our model is even more general, as it encompasses state-dependent distributions, whose
parameters depend on the state and may depend on other distributions and thus define joint,
multi-variate and hierarchically-structured distributions. Notably, our model comprises both
continuous and discrete probability distributions and is able to model discrete-time stochastic
hybrid systems [LSAZ22]. Our model also subsumes probabilistic models and programs over
finite state spaces, where each state can be represented as a point of the Euclidean space Rn .
Note that this encoding of a finite state space ensures Borel-measurability of the update
function, as the σ-algebra of this finite state space (i.e., its powerset) is a subset of the Borel
σ-algebra.



       3. Quantitative Reachability Verification of Probabilistic Models
Quantitative verification treats the question of providing a quantity (probability) with which
a system satisfies a property, as opposed to providing a definite (positive or negative) answer.
In fact, it is sometimes too conservative or inappropriate to demand a definite outcome
to a formal verification question. For instance, a system whose behaviour is probabilistic
may violate a specification on rare corner cases and yet satisfy it with a probability that is
deemed acceptable for the application domain. We address the quantitative verification of
probabilistic systems, which is the problem of computing the probability for which a system
satisfies a specification [Kwi07, vBW01, BHHK10, BdAFK18].
     We consider the quantitative reachability verification question, which as we show below,
is at the core of a variety of quantitative verification problems for probabilistic programs
and stochastic dynamical models. Henceforth, we use 1S to denote the indicator function
of set S, i.e., 1S (s) = 1 if s ∈ S and 1S (s) = 0 if s ̸∈ S; we also use λx.M to denote the
anonymous function that takes an argument x and evaluates the expression M to produce
its result.
     We now provide a recursive characterisation for the probability that a stochastic process
reaches a Borel measurable target set in exactly time t (Lemma 3.1), and in at most time t
(Lemma 3.2). Finally, in Lemma 3.3 we employ these results to show that the probability
of reaching a target set in any finite time is the limit of the time-bounded reachability
probability as the time bound goes to infinity.
4:6             A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy                                                   Vol. 22:2




Lemma 3.1. Let the event that a stochastic process {Xts }t∈N over state space Rn initialised
in state s ∈ Rn reaches a target set A ∈ B(Rn ) in exactly time t ∈ N be
             Reachst (A) = ω ∈ Ω | X0s (ω) ̸∈ A, . . . , Xt−1
                                                          s
                                                              (ω) ̸∈ A, Xts (ω) ∈ A ,
                           
                                                                                       (3.1)
with Reachs0 (A) = Ω if s ∈ A, and Reachs0 (A) = ∅ if s ∈
                                                        / A. Then, Reachst (A) is measurable
and its probability measure can be expressed as follows:
                                                                                                ′
                      P[Reachst+1 (A)] = 1Rn \A (s) · X[λs′ . P[Reachst (A)]](s),                                               (3.2a)
                         P[Reachs0 (A)] = 1A (s).                                                                               (3.2b)

Proof. For every i we have that the pre-image of any measurable set R ∈ B(Rn ) under
Xis : (Ω, F) → (Rn , B(Rn )), denoted (Xis )−1 [R], is measurable since Xis is a measurable
function [MTG09, Section 3.4]. It follows that Reachst (A) is measurable because it can be
expressed as the following finite intersection:
              Reachst (A) = ∩{(Xis )−1 [Rn \ A] : i = 0, . . . , t − 1} ∩ (Xts )−1 [A].
It is a standard result (see [MTG09, Theorem 3.4.1] and [Rev75, Theorem 2.8]) that the
probability measure of the event Reachst 0 (A) with t > 0 can be expressed as an integral with
respect to the transition kernel of the Markov chain:
                                                      Z                     Z              Z          t
                                                                                                      Y
         P[Reachst 0 (A)] = 1Rn \A (s0 )                              ···                                    T (si−1 , dsi )
                                                          s1 ∈Rn \A          st−1 ∈Rn \A   st ∈A i=1
                                                                    t−1                            t
                                   Z                  Z                               !
                                                                    Y                             Y
                              =                 ···                        1Rn \A (si ) 1A (st )             T (si−1 , dsi )
                                       s1 ∈Rn         st ∈Rn        i=0                                i=1

As a consequence, we can express the probability measure of Reachst+1
                                                                   0
                                                                      (A) as follows:
                                          Z
  P[Reachst+1
           0
              (A)] = 1Rn \A (s0 )
                                            s1 ∈Rn
                                                  t                                            t+1
                Z                  Z                                        !                                         !
                                                  Y                                            Y
                             ···                           1Rn \A (si ) 1A (st+1 )                   T (si−1 , dsi ) T (s0 , ds1 )
                    s2 ∈Rn         st+1 ∈Rn       i=1                                          i=2
                |                                                     {z                                               }
                                                                       s
                                                                P[Reacht 1 (A)]

Then, after substituting s0 with s and s1 with s′ , we derive Eq. (3.2a) as follows:
                                        Z
                                                    ′
                 s
         P[Reacht+1 (A)] = 1Rn \A (s) ·   P[Reachst (A)] T (s, ds′ )
                                                           Rn
                                                                                  ′
                               = 1Rn \A (s) · X[λs′ . P[Reachst (A)]](s)                                          by (2.4)

Finally, Eq. (3.2b), which states that P[Reachs0 (A)] = 1A (s) directly follows from the
definition of Reachs0 (A), as Reachs0 (A) = Ω when s ∈ A and Reachs0 (A) = ∅ when s ̸∈ A.
Lemma 3.2. Let the event that a stochastic process {Xts }t∈N over state space Rn initialised
in state s ∈ Rn reaches a target set A ∈ B(Rn ) in at most time t ∈ N be
                               Reachs≤t (A) = ∪{ Reachsi (A) : 0 ≤ i ≤ t }.                                                       (3.3)
Vol. 22:2              QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                                             4:7




Then, Reachs≤t (A) is measurable and its probability measure can be expressed as follows:
                                                                                        ′
                P[Reachs≤t+1 (A)] = 1A (s) + 1Rn \A (s) · X[λs′ . P[Reachs≤t (A)]](s),                      (3.4a)
                  P[Reachs≤0 (A)] = 1A (s).                                                                 (3.4b)
Proof. Since the sets in the family {Reachst (A) : t ∈ N} are disjoint, we note that the union
in (3.3) that defines Reachs≤t (A) is a union of disjoint sets. It follows that, by countable
additivity of measure and disjointness of the union in (3.3), its probability measure is
given by
                                               Xt
                             P[Reachs≤t (A)] =      P[Reachst (A)].                       (3.5)
                                                         i=0
Consequently and thanks to Lemma 3.1, we have
                                              t+1
                                              X
   P[Reachs≤t+1 (A)] = P[Reachs0 (A)] +             P[Reachsi (A)]                                     by (3.5)
                                              i=1
                                    t+1
                                    X
                       = 1A (s) +         P[Reachsi (A)]                                              by (3.2b)
                                    i=1
                                    t
                                    X
                       = 1A (s) +         P[Reachsi+1 (A)]
                                    i=0
                                     t
                                                                             ′
                                    X
                       = 1A (s) +         1Rn \A (s) · X[λs′ . P[Reachsi (A)]](s)                     by (3.2a)
                                    i=0
                                  t              Z                                            
                                                                          ′
                                  X
                       = 1A (s) +    1Rn \A (s) ·                P[Reachsi (A)] T (s, ds′ )            by (2.4)
                                    i=0                    Rn
                                                           t
                                                 Z                                  !
                                                                          ′
                                                           X
                       = 1A (s) + 1Rn \A (s) ·                   P[Reachsi (A)]         T (s, ds′ )
                                                    Rn     i=0
                                                 Z
                                                                     ′
                       = 1A (s) + 1Rn \A (s) ·           P[Reachs≤t (A)] T (s, ds′ )                   by (3.5)
                                                    Rn
                                                                         ′
                       = 1A (s) + 1Rn \A (s) · X[λs′ . P[Reachs≤t (A)]](s)                            by (2.4).
Furthermore, we also have that
            P[Reachs≤0
                     0
                       (A)] = P[Reachs00 (A)] = 1A (s0 )                         by (3.5) and (3.2b).
Lemma 3.3. Let the event that a stochastic process {Xts }t∈N over state space Rn initialised
in state s ∈ Rn reaches a target set A ∈ B(Rn ) in finite time be
              Reachsfin (A) = ∪ {Reachst (A) : t ∈ N} = ∪ Reachs≤t (A) : t ∈ N .
                                                         
                                                                                       (3.6)
Then, Reachsfin (A) is measurable and its probability measure (i.e. the reachability probability
of the target set) may be expressed as follows:
                              P[Reachsfin (A)] = lim P[Reachs≤t (A)].                                        (3.7)
                                                      t→∞

Proof. We recall from Eq. (3.3) that Reachs≤t (A) = ∪ {Reachsi (A) : 0 ≤ i ≤ t}, and we note
that this implies that Reachs≤t (A) ⊆ Reachs≤t+1 (A). Then, we recall from Eq. (3.6) that
4:8             A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy               Vol. 22:2




Reachsfin (A) = ∪ Reachs≤t (A) : t ∈ N . Finally, we apply a standard result in measure
                   

theory regarding the measure of an increasing union [Axl19, Theorem 2.59] to conclude
P[Reachsfin (A)] = limt→∞ P[Reachs≤t (A)].
    The recursive characterisation of the time-bounded reachability probability (Lemma 3.2)
and the limit characterisation of the probability of reaching the target set in any finite time
(Lemma 3.3) provides the foundation for a fixpoint characterisation for the reachability
probability (Section 4), in turn justifying the conditions that a supermartingale certificate
must satisfy (Section 5) for it to provide a sound upper bound on the reachability probability.
    Our method leverages neural networks to compute an upper bound for the reachability
probability with respect to a given target set (cf. Section 5). Notice that an appropriate
choice of target set allows us to express a variety of other quantitative verification questions,
for which our method can provide an upper or lower bound. Next, by providing a suitable
choice for the target set, we show how important quantitative verification questions for
probabilistic programs and stochastic dynamical models can be characterised as instances of
quantitative reachability.
Termination Analysis: Let G ∈ B(Rn ) be the guard set of a probabilistic while loop as in
      Eq. (2.5), i.e., the set of states for which that guard condition evaluates to true. The
      event that the loop terminates from initial state s0 is Reachsfin   0
                                                                            (Rn \ G). Our method
      computes an upper bound for the probability that the loop terminates or, dually, it
      computes a lower bound for the probability of non-termination. Notably, when this
      lower bound is greater than 0, then almost-sure termination is refuted.
Assertion-violation Analysis: Let G ∈ B(Rn ) be the guard set of a probabilistic while
      loop and A ∈ B(Rn ) be the satisfying set of an assertion placed at the beginning of the
      loop body. Given initial state s0 , the event that the assertion is eventually violated is
      Reachsfin
              0
                (G \ A). Our method computes an upper bound for the probability of assertion
      violation or, dually, a lower bound for its satisfaction. Note that assertions in other
      positions of the body can be modelled similarly by using additional Boolean variables.
Safety Verification: Let B ∈ B(Rn ) be a set of undesirable states in a stochastic dynamical
      model. The event that the system is safe when initialised in s0 , i.e., it never reaches an
      undesirable state, is given by Ω \ Reachsfin  0
                                                      (B). Our method computes a lower bound
      for the probability that the system is safe, which is 1 − P[Reachsfin    0
                                                                                 (B)].
                                            n
Invariant Verification: Let I ∈ B(R ) be a candidate invariant set. The event that
      I is invariant when the system is initialised in s0 is Ω \ Reachsfin         0
                                                                                     (Rn \ I). Our
      method computes a lower bound for the probability that set I is invariant, which is
      1 − P[Reachsfin0
                       (Rn \ I)]. Note that if s0 ∈
                                                  / I, this definition yields a trivial lower bound
      of zero for the probability of invariance.


           4. Fixpoint Characterisation of Quantitative Reachability
Our supermartingale certificate proof-rule (Theorem 5.1) relies on the order-theoretic char-
acterisation of reachability probabilities in probabilistic programs [TOUH18]. This previous
seminal work considered a more general setting allowing for both non-determinism and
arbitrary program invariants. For clarity and self-containment, and to build intuition about
order-theoretic reasoning in our context, we present a streamlined analysis that mirrors the
soundness proof for non-negative supermartingales [TOUH18, Proposition 4.2] in a setting
without non-determinism or invariants.
Vol. 22:2            QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                        4:9




   We define the space of candidate certificates as the set of (B(Rn ), B(Rn≥0 ∪ {∞}))-
measurable functions V ⊂ Rn → R≥0 ∪ {∞}. Furthermore, we define the ordering relation
≤ between two functions U, V ∈ V pointwise as follows:
                              U ≤ V ⇔ ∀s ∈ Rn . U (s) ≤ V (s).                          (4.1)
The set of functions V under the ordering ≤ defines a pointed complete partially ordered set
(pointed CPO) [DP02, Definition 8.1] with the constant zero function as its bottom element;
we overload the symbol 0 ∈ V to denote the constant zero function.
Lemma 4.1. (V, ≤) is a pointed CPO with bottom element 0, and with each countable
increasing chain {Vi }i∈N having least upper bound:
                  (sup {Vi : i ∈ N})(s) = sup {Vi (s) : i ∈ N} = lim Vi (s).            (4.2)
                                                                    i→∞

Proof. The fact that the pointwise relation ≤ on functions is reflexive, transitive and anti-
symmetric follows from the properties of the natural ordering relation ≤ on the set R≥0 ∪{∞}.
This shows that (V, ≤) is a partial order. The constant function 0 is the bottom element of
the partial order because V contains only non-negative functions.
     To show that the partial order is also complete, we need to show that the least upper
bound of every countable increasing chain {Vi }i∈N in (V, ≤) is also in V; in other words,
that the least upper bound is (B(Rn ), B(R≥0 ∪ {∞}))-measurable. To this end, we note that
for all s ∈ Rn we have (sup {Vi : i ∈ N})(s) = sup {Vi (s) : i ∈ N} owing to a standard result
[DP02, Lemma 8.5(ii), p.177], and that the pointwise supremum of a countable family of
measurable functions is also measurable [Pol01, Example 8, p.23].
     Finally, since for any s ∈ Rn we have {Vi (s)}i∈N is a non-decreasing sequence in
the extended non-negative reals (namely, the set R≥0 ∪ {∞}), we have by the monotone
convergence property of non-decreasing real sequences [RF10, Theorem 15, p.21] that
                               lim Vi (s) = sup {Vi (s) : i ∈ N}.
                              i→∞

    The exact reachability probability is a measurable function from states to non-negative
reals, and is thus an element of the pointed CPO V. By Lemma 3.2 we have a recursive
characterisation of increasingly tight approximations to this probability in terms of the
higher-order endofunction Φ : V → V defined as
                           Φ(V )(s) = 1A (s) + 1Rn \A (s) · X[V ](s).                   (4.3)
Furthermore, Lemma 3.3 states that the exact reachability probability is the limit of its
approximations. We formalise this argument by an application of Kleene’s Fixpoint Theorem
(see [DP02, Section 8.15, p.183] and [Win93, Theorem 5.11]) over the pointed CPO (V, ≤)
over the space of certificates. A technical requirement of Kleene’s Fixpoint Theorem is that
Φ is ω-continuous [Win93, Definition p.71]. A function is ω-continuous if it is monotonic and
preserves least upper bounds of countable increasing chains. To show that the higher-order
function Φ is ω-continuous, we first show that the post-expectation operator X (which is in
turn a higher-order function in V) is ω-continuous.
Lemma 4.2. X is ω-continuous.
Proof. Recalling the definition of ω-continuity for an endofunction on a pointed CPO [Win93,
Definition p.71], we show that X satisfies the following two properties:
4:10                A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy            Vol. 22:2




• X is monotonic. Suppose U, V ∈ V with U ≤ V . Then for all s ∈ Rn :
                           Z
                X[U ](s) =     U (s′ ) T (s, ds′ )
                             n
                           ZR
                         ≤     V (s′ ) T (s, ds′ )          by U ≤ V
                                   Rn
                               = X[V ](s).
• X preserves least upper bounds of countable increasing chains. Let V0 ≤ V1 ≤ . . . be a
  countable increasing chain in V. As X is monotone, X[V0 ] ≤ X[V1 ] ≤ . . . is also a countable
  increasing chain. We note that since X is an integral, it satisfies the Monotone Convergence
  Theorem (MCT) [Pol01, Theorem 12], which can be invoked in the following since {Vi }i∈N
  is a sequence of non-negative measurable functions that converge monotonically to the
  function sup {Vi : i ∈ N}. Thus, for all s ∈ Rn , we have that
       (sup {X[Vi ] : i ∈ N})(s) = lim X[Vi ](s)                            by (4.2), Lemma 4.1
                                   i→∞
                                       Z
                                 = lim     Vi (s′ ) T (s, ds′ )                         by (2.4)
                                   i→∞ Rn
                                   Z
                                 =    (sup {Vi : i ∈ N})(s′ ) T (s, ds′ )          (4.2) & MCT
                                     Rn
                                 = X[sup {Vi : i ∈ N}](s)
Lemma 4.3. Φ is ω-continuous.
Proof. We show that Φ satisfies the following two properties.
• Φ is monotonic. Let s ∈ Rn be arbitrary and assume U ≤ V . Then
          Φ(U )(s) = 1A (s) + 1Rn \A (s) · X[U ](s)
                   ≤ 1A (s) + 1Rn \A (s) · X[V ](s)        by monotonicity of X, Lemma 4.2
                   = Φ(V )(s),
  therefore Φ(U ) ≤ Φ(V ).
• Φ preserves least upper bounds of countable increasing chains. Suppose {Vi : i ∈ N} is a
  countable increasing chain in (V, ≤). Let s ∈ Rn be arbitrary. Then
       Φ(sup {Vi : i ∈ N})(s) = 1A (s) + 1Rn \A (s) · X[sup {Vi : i ∈ N}](s)            by (4.3)
                               = 1A (s) + 1Rn \A (s) · (sup {X[Vi ] : i ∈ N})(s)   by Lemma 4.2
                               = 1A (s) + 1Rn \A (s) · (sup {X[Vi ](s) : i ∈ N})        by (4.2)
                               = sup {(1A (s) + 1Rn \A (s) · X[Vi ](s)) : i ∈ N}
                               = sup {Φ[Vi ](s) : i ∈ N}                                by (4.3)
                               = (sup {Φ(Vi ) : i ∈ N}) (s)                            by (4.2);
  we note that the steps above relying on Eq. (4.2) use the property that suprema in the
  pointed CPO (V, ⊑) are defined pointwise. Finally, the derivation above establishes that
  Φ(sup {Vi : i ∈ N}) = sup {Φ(Vi ) : i ∈ N}.
    To demonstrate that the exact reachability probability is the least fixpoint of the
higher-order function Φ, we leverage Kleene’s Fixpoint Theorem which states that since Φ is
Vol. 22:2              QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                              4:11




ω-continuous, its least fixpoint is given by
                                          sup {Φt (0) : t ∈ N}                                    (4.4)
where we let Φt denote the t-fold application of Φ to its argument. To relate this to quantita-
tive reachability, we show in Lemma 4.4 that for any t ∈ N, the function λs. P[Reachs≤t (A)]
is equal to Φt+1 (0) (which is simply a re-statement of Lemma 3.2). In combination with
Eq. (3.7), this yields the following result.
Lemma 4.4. λs. P[Reachsfin (A)] is the least fixpoint of Φ.
Proof. We need to prove
                           λs.P[Reachsfin (A)] = (sup {Φt (0) : t ∈ N}).                          (4.5)
To prove Eq. (4.5) we first show that for all t ∈ N and s ∈ Rn , we have
                                    P[Reachs≤t (A)] = Φt+1 (0)(s).                                (4.6)
We proceed by induction on t ∈ N, that is, we show
• λs. P[Reachs≤0 (A)] = Φ1 (0), and
• λs. P[Reachs≤t (A)] = Φt+1 (0) implies λs. P[Reachs≤t+1 (A)] = Φt+2 (0).
For the base case, we let s ∈ Rn and have
            P[Reachs≤0 (A)] = 1A (s)                                               by (3.4b)
                            = 1A (s) + 1Rn \A (s) · X[0](s)                because X[0] = 0
                                1
                            = Φ (0)(s)                                             by (4.3).
For the inductive case, we let s ∈ Rn and leverage Lemma 3.2 as follows:
                                                                     ′
        P[Reachs≤t+1 (A)] = 1A (s) + 1Rn \A (s) · X[λs′ .P[Reachs≤t (A)]](s)          by (3.4a)
                                    ′      ′
                          = Φ(λs .P[Reachs≤t (A)])(s)                                  by (4.3)
                               t+1
                          = Φ(Φ         (0))(s)                                          by IH
                          = Φt+2 (0)(s)
    Next, we show that (4.5) is a consequence of Lemma 4.1, noting that {Φt (0)}t∈N is a
countable increasing chain in (V, ≤):
            P[Reachsfin (A)] = lim P[Reachs≤t (A)]                                  by (3.7)
                              t→∞
                           = lim Φt+1 (0)(s)                                        by (4.6)
                              t→∞
                           = lim Φt (0)(s)
                              t→∞
                           = (sup {Φt (0) : t ∈ N})(s)                   by (4.2), Lemma 4.1

    In summary, Lemma 4.4 characterises the exact reachability probability as the least
fixpoint of a ω-continuous endofunction Φ on the set V. We use this fixpoint characterisation
in Section 5 to show how a supermartingale certificate establishes an upper bound on the
probability of reaching a target state in any number of steps.
4:12               A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy                Vol. 22:2




             5. Neural Supermartingales for Quantitative Verification
Supermartingale certificates provide a flexible and powerful theoretical framework for the
formal verification of probabilistic models with infinite state spaces (see [Dur10, Section
5.2], [CS13, Definition 9 and Theorem 4]). Not only have supermartingales been applied
to qualitative questions, such as almost-sure termination analysis of probabilistic programs
and almost-sure stability analysis of stochastic dynamical models, but also to quantitative
reachability verification, as in this work. Specifically, this is enabled by the theory of
non-negative repulsing supermartingales and of stochastic invariants [TOUH21, CGMv22,
CNv17].
     Our method builds upon the theory of non-negative repulsing supermartingales and
stochastic invariant indicators and applies it to take advantage of the expressive power of
neural networks and the flexibility of machine learning and counterexample-guided inductive
synthesis algorithms. We refer to a function V that is non-increasing in expectation outside of
the target set as a supermartingale. This is because V (Xts ) defines a supermartingale process
[Dur10, Section 5.2], where Xts is the stochastic process corresponding to the semantics of
the probabilistic model, c.f. Eq. (2.2). Our method hinges on the following theorem.
Theorem 5.1. Let A ∈ B(Rn ) be a target set, and let V : Rn → R≥0 ∪{∞} be a non-negative
function that satisfies the following two conditions:
(indicating condition)                     ∀s ∈ A : V (s) ≥ 1,                                   (5.1a)
(non-increasing condition)                 ∀s ̸∈ A : X[V ](s) ≤ V (s),                           (5.1b)
Then for all s ∈ Rn we have V (s) ≥ P[Reachsfin (A)].
Proof. Suppose that V ∈ V is a function that satisfies (5.1a) and (5.1b). We show that V is
a pre-fixpoint of Φ (defined in Eq. 4.3), namely, that Φ(V ) ≤ V . We proceed by cases:
       Case s ∈ A: Φ(V )(s) = 1A (s) + 1Rn \A (s) · X[V ](s) = 1 ≤ V (s)                by (5.1a),
       Case s ∈
              / A: Φ(V )(s) = 1A (s) + 1Rn \A (s) · X[V ](s) = X[V ](s) ≤ V (s)         by (5.1b).
This establishes that V is a pre-fixpoint of Φ.
     Next, we recall the standard result [DP02, Section 8.20, p.186] that (if it exists) the
least fixpoint of a monotone endofunction is equal to its least pre-fixpoint (and therefore, the
least fixpoint is less than or equal to any pre-fixpoint). In our case, since the endofunction
Φ : V → V is ω-continuous, its least fixpoint exists and is equal (by Lemma 4.4) to the exact
reachability probability, λs. P[Reachsfin (A)]. Thus, as V is a pre-fixpoint of Φ, we have that
λs. P[Reachsfin (A)] ≤ V holds true, which corresponds to the statement of Theorem 5.1.
     As we show in detail in Section 6, we compute a supermartingale that satisfies the two
criteria (5.1a) and (5.1b), while also minimising its output over the initial state s0 . When
the initial state is chosen nondeterministically from a set S0 , we instead minimise the output
over all states in the set. As a consequence of Theorem 5.1, the maximum of V over S0 is a
sound upper bound for the reachability probability.
     In this work, we template V as a neural network with n input neurons, l hidden layers
with respectively h1 , . . . hl neurons in each hidden layer, and 1 output neuron. We guarantee
a-priori that the function’s output will be non-negative over the entire domain using the
following architecture:
                                                       T                             T
 V (x) = sum (σl ◦ · · · ◦ σ1 (x)) ,   σi (z) = (ReLU(wi,1 z + bi,1 ), . . . , ReLU(wi,h i
                                                                                           z + bi,hi )),
                                                                                                   (5.2)
Vol. 22:2            QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                          4:13




      while x > 0 do
          assert ( x <= 10) ;                             1
          p ~ Bernoulli (0.5) ;




                                                     Probability
          if p == 1 then
               x -= 2                                                 V lin
          else                                                        V3neur
                                                                        neur
                                                                      V12
               x += 1
                                                                               Preach
          fi
      od                                         −2−1              1 2 3 4 5 6 7 8 9 10 11
                                                                      Initial value of x

Figure 2: Comparison between linear and neural supermartingale functions in tightness of
          bounds for the assertion violation probability of the program repulse, shown on the
          left. On the right, the function V lin indicates the tightest linear supermartingale
          (under the restriction that x is greater than −2). The functions V3neur and V12   neur

          indicate single-layer neural supermartingales with 3 and 12 neurons respectively.
          The piecewise constant function Preach is the true probability of assertion violation,
          and indicates the ideal lower bound for the value of any supermartingale function.


where sum(zl,1 , . . . , zl,hl ) = hk=1                                   T ∈ Qhi−1 (defining
                                  P l
                                        zl,k , ReLU (z) = max{0, z}, and wi,j
h0 = n, the number of input neurons) and bi,j ∈ Q are respectively the weight vector and
the bias parameter for the inputs to neuron j at layer i. Then, our method trains the neural
network to satisfy the two criteria (5.1a) and (5.1b), while also minimising its output on the
initial condition.
     Using neural networks as templates of supermartingale functions introduces non-trivial
advantages with respect to symbolic methods for the synthesis of supermartingales. Firstly,
neural supermartingales are able to better approximate the true probability of reachability
and thus attain tighter upper bounds on it. Secondly, symbolic methods require deterministic
invariants that overapproximate the set of reachable states, and to suitably restrict the
domain of the template. Figure 2 illustrates using an example the advantages of neural
certificates with respect to linear supermartingales synthesised using Farkas’ lemma. This
example shows that increasing the number of neurons provides greater flexibility and
allows the certificate to more tightly approximate the true probability. Moreover, this
example shows that linear supermartingales require their domain to be restricted with an
appropriate deterministic invariant (to enforce non-negativity). Notably, symbolic methods
for the synthesis of polynomial supermartingales based on Putinar’s Positivstellensatz also
require compact deterministic invariants to be provided [CGMv22]. By contrast, neural
supermartingales (whose output is always non-negative) achieve the same result while
relaxing the requirement of providing an invariant beforehand.


              6. Data-driven Synthesis of Neural Supermartingales
Our approach to synthesising neural supermartingales for quantitative verification utilises a
counterexample-guided inductive synthesis (CEGIS) procedure [Sol08, STB+ 06] (cf. Fig. 3).
This procedure consists of two components, a learner and a verifier, that work in opposition
to each other. On the one hand, the learner seeks to synthesise a candidate supermartingale
4:14            A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy             Vol. 22:2




                                          Candidate V
                                                                    V, p
                                     Learner           Verifier
                        f , S0 , A
                                               dcex

Figure 3: Overview of the counterexample-guided inductive synthesis procedure used to
          synthesise neural supermartingales for quantitative reachability verification. Inputs
          to the procedure are a probabilistic program f , a set of initial states S0 , and a
          target set A. The procedure outputs a valid neural supermartingale V and a
          probability bound p.

that meets the desired specification (cf. Eq. (5.1)) over a finite set of samples from the
state space, while simultaneously optimising the tightness of the probability bound. On
the other hand, the verifier seeks to disprove the validity of this candidate by searching
for counterexamples, i.e., instances where the desired specification is invalidated, over the
entire state space. If the verifier shows that no such counterexample exists, then the desired
specification is met by the supermartingale and the procedure provides a sound probability
bound for the reachability probability of interest, together with a neural supermartingale to
certify it.

6.1. Training of Neural Supermartingales from Samples. Our neural supermartingale
for quantitative reachability verification consists of a neural network with ReLU activation
functions, with an arbitrary number of hidden layers (cf. Section 5). We train this neural
network using gradient descent over a finite set D = {d(1) , . . . , d(m) } ⊆ Rn of states d(i)
sampled over the state space Rn . Initially, we sample uniformly within a bounded hyper-
rectangle of Rn , a technique that scales effectively to high dimensional state spaces and
efficiently populates the initial dataset of state samples. Then, we construct a loss function
that guides gradient descent to optimise the parameters (weight and biases) of the neural
network V to satisfy the specification set out in Eq. (5.1) while also minimising the probability
bound. We define a loss function L(D) that consists of three terms:
                      L(D) = β1 Lind (D) + β2 Lnon-inc (D) + β3 Lmin (D).                   (6.1)
Components Lind and Lnon-inc are responsible for encouraging satisfaction of the conditions in
Eq. (5.1), while the component Lmin is responsible for tightening the probability bound. The
parameters of this optimisation problem are the parameters of the neural network, which are
initialised randomly. The dataset consists of the state samples, initially sampled randomly,
and generated from counterexamples in subsequent CEGIS iterations (cf. Section 6.2). The
coefficients β1 , β2 and β3 denote scale factors for each term, which we choose according to
the priority that we want to assign to each condition (cf. Section 7).
     First, consider the condition in Eq. (5.1a), which we refer to as the indicating condition.
For this, we use the following loss function:
                                          1     X
(indicating loss)          Lind (D) =                 ReLU (1 − V (d))                    (6.2)
                                      |D ∩ A|
                                               d∈D∩A
This adds a penalty for states d ∈ D lying inside the target condition A, at which V fails to
satisfy the indicating condition, whilst ignoring any states where V satisfies it. We average
Vol. 22:2            QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                         4:15




this per-state penalty across all states in D ∩ A (where |D ∩ A| denotes the number of
elements in this set).
     We next consider the non-increasing condition in Eq. (5.1b), for which we use the
following loss term:
                                           1    X
(non-increasing loss)    Lnon-inc (D) =             ReLU(X[V ](d) − V (d)).       (6.3)
                                        |D \ A|
                                                 d∈D\A

This penalises states d ∈ D lying outside of the target set A, at which V fails to satisfy the
non-increasing condition. Notably, this component is defined in terms of the post-expectation
X[V ] of our supermartingale. To embed this expression in our loss function we consider two
alternative approaches, which we call program-aware and program-agnostic.
Program-aware Approach: The program-aware approach uses the source code of the
      program to generate a symbolic expression for the post-expectation of V . For this
      purpose, we exploit the symbolic inference algorithm introduced by the tool PSI
      [GMV16, GSV20], along with a symbolic representation of V . We construct a proba-
      bilistic program which represents the evaluation of V on the state resulting after the
      execution of the update function f . The expected value of this program’s result is
      precisely X[V ]. This results in a symbolic expression that is a function of the program
      state and parameters of V . In the non-increasing loss, states are instantiated to
      elements of D \ A, while the parameters are left as free-variables that the gradient
      descent engine differentiates with respect to.
Program-agnostic Approach: The program-agnostic approach provides an alternative
      formulation of the non-increasing loss term that does not require symbolic reasoning.
      Instead of directly leveraging the program’s source code, it assumes that for any state
      we can draw independent samples from its distribution over successor states, i.e., we
      assume access to a generative model [MMLG10, KMN99, JS21]. We therefore utilise
      a Monte Carlo scheme to estimate the post-expectation. For each state d in our
      dataset D, to obtain an estimate of X[V ](d) we sample a number m′ of successor states
      D′ = {d′ (k) : 1 ≤ k ≤ m′ }. Each successor state d′ (k) is sampled by executing the
      program’s update P function f (cf. Eq. (2.1)) at state d. Then X[V ](d) is estimated as
      X[V ](d) ≈ |D1′ | d′ ∈D′ V (d′ ), namely the average of V over D′ . Even though this is an
      approximation, we emphasise that this does not affect the soundness of our scheme,
      which is ensured by the verifier.
     Finally, we introduce a tightness criterion that minimises the probability upper bound:
                                                     1       X
(minimisation loss)                   Lmin (D) =                  V (d).                   (6.4)
                                                  |D ∩ S0 |
                                                         d∈D∩S0

This term encourages V to take smaller values over the set of initial states S0 . Recall that
the smaller the probability upper bound, the closer it is to the true value.
     The loss function is provided to the gradient descent optimiser, whose performance
benefits from a smooth objective. For this reason, to improve the performance of our learner
we replace every ReLU activation within the neural network V with a smooth approximation,
Softplus, which takes the form Softplus(s) = log(1 + exp(s)), whereas the occurrences of
ReLU applied to the output of V in Eqs. (6.2), (6.3) and (6.3) are retained. Additionally,
we improve the approximation of Softplus to ReLU at small values over the interval [0, 1] by
re-scaling V . This means that we modify the indicating condition to require that V (x) ≥ α
4:16               A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy             Vol. 22:2




over the target set A,
                     Pfor some large α > 1. In other words, we modify the indicating loss
                 1
to Lind (V ) = |D∩A|   d∈D∩A ReLU(α − V (d)). We remark that while Softplus is used as
the activation function in the learning stage, for the verification stage we instead employ
ReLU activation functions, ensuring soundness of the generated neural supermartingale.
We remark that this has no effect on the soundness of our approach, which is ultimately
guaranteed by the verifier.

6.2. Verification of Neural Supermartingales Using SMT Solvers. The purpose of
the verification stage is to check that the neural supermartingale meets the requirements
of Eq. (5.1) over the entire state space Rn , and if that is determined to be the case to
furthermore obtain a sound upper bound on the reachability probability. We achieve this by
constructing a suitable formula in first-order logic, Eq. (6.5), and use SMT solving to decide
its validity, or equivalently, to decide the satisfiability of its negation, Eq. (6.6).
     The conditions pertaining to the validity of the neural supermartingale, given in (5.1a)
and (5.1b), are encoded by the formulas φind and φnon-inc . We also note that for a constant
p ∈ [0, 1] to be a sound upper bound on the reachability probability, it is sufficient to require
that p is an upper bound on the neural supermartingale’s value over the set of initial states
S0 (cf. Theorem 5.1), which is expressed by the formula φbound . A suitable choice for the
bound p is determined by a binary search over the interval [0, 1].
  ∀s ∈ Rn : (s ∈ A → V (s) ≥ 1) ∧ (s ∈
                                     / A → X[V ](s) ≤ V (s)) ∧ (s ∈ S0 → V (s) < p) . (6.5)
            |       {z        } |            {z            } |          {z        }
                        φind                      φnon-inc                    φbound

Here, V (s) is a symbolic encoding of the candidate neural supermartingale proposed by
the learner (Section 6.1), and S0 and A are defined by Boolean predicates over program
variables, all of which (in our setting of networks composed from ReLU activations) are
expressible using expressions and constraints in non-linear real arithmetic. For this reason,
we use Z3 as our SMT solver [dMB08].
    The SMT solver is provided with the negation of Eq. (6.5), namely
       ∃s ∈ Rn : (s ∈ A ∧ V (s) < 1) ∨ (s ∈
                                          / A ∧ X[V ](s) > V (s)) ∨ (s ∈ S0 ∧ V (s) ≥ p),      (6.6)
                 |       {z        } |            {z            } |          {z        }
                        ¬φind                    ¬φnon-inc                  ¬φbound

and decides its satisfiability, seeking an assignment dcex of s that is a counterexample to the
neural supermartingale’s validity, for which any of ¬φind , ¬φnon-inc and ¬φbound are satisfied.
If no counterexample is found, this certifies the validity of the neural supermartingale.
Alternatively, if a counterexample dcex is found, it is added to the data set D, for the
synthesis to incrementally resume.


                                 7. Experimental Evaluation
The previous section has presented a new method for synthesising neural supermartingales.
This section presents an empirical evaluation of the method, by testing it against a series of
benchmarks. Each benchmark is run ten times. A test is successful if a valid supermartingale
is synthesised, and the proportion of successful tests is recorded. Further, the average bound
from the valid supermartingales is also recorded, along with the average time taken by
the learning and verification steps, respectively. This procedure is applied separately for
program-aware and program-agnostic synthesis. We use values β1 = 10, β2 = 105 , β3 = 1
in Eq. (6.1) to define the priority ordering of the three terms in the loss function, which
Vol. 22:2            QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                                 4:17




Table 1: Results comparing neural supermartingales with Farkas Lemma for different bench-
         marks. Here, p is the average probability bound generated by the certificate;
         success ratio is the number of successful experiments, out of 10 repeats, generated
         by CEGIS with neural supermartingale; ‘-’ means no result was obtained. We also
         denote the architecture of the network: (h1 , h2 ) denotes a network with 2 hidden
         layers consisting of h1 and h2 neurons respectively.
    Benchmark            Farkas’           Quantitative Neural Certificates               Network
                         Lemma        Program-Agnostic            Program-Aware            Arch.
                                       p       Success Ratio      p       Success Ratio
    persist 2d              -       ≤ 0.1026        0.9        ≤ 0.1175        0.9         (3, 1)
    faulty marbles          -       ≤ 0.0739        0.9        ≤ 0.0649        0.8           3
    faulty unreliable       -       ≤ 0.0553        0.9        ≤ 0.0536        1.0           3
    faulty regions          -       ≤ 0.0473        0.9        ≤ 0.0411        0.9         (3, 1)
    cliff crossing       ≤ 0.4546   ≤ 0.0553        0.9        ≤ 0.0591        0.8           4
    repulse100           ≤ 0.0991   ≤ 0.0288        1.0        ≤ 0.0268        1.0           3
    repulse100 uniform   ≤ 0.0991   ≤ 0.0344        1.0            -            -            2
    repulse100 2d        ≤ 0.0991   ≤ 0.0568        1.0        ≤ 0.0541        1.0           3
    faulty varying       ≤ 0.1819   ≤ 0.0864        1.0        ≤ 0.0865        1.0           2
    faulty concave       ≤ 0.1819   ≤ 0.1399        1.0        ≤ 0.1356        0.9         (3, 1)
    fixed loop           ≤ 0.0091   ≤ 0.0095        1.0        ≤ 0.0094        1.0           1
    faulty loop          ≤ 0.0181   ≤ 0.0195        1.0        ≤ 0.0184        1.0           1
    faulty uniform       ≤ 0.0181   ≤ 0.0233        1.0        ≤ 0.0221        1.0           1
    faulty rare          ≤ 0.0019   ≤ 0.0022        1.0        ≤ 0.0022        1.0           1
    faulty easy1         ≤ 0.0801   ≤ 0.1007        1.0        ≤ 0.0865        1.0           1
    faulty ndecr         ≤ 0.0561   ≤ 0.0723        1.0        ≤ 0.0630        1.0           1
    faulty walk          ≤ 0.0121   ≤ 0.0173        1.0        ≤ 0.0166        1.0           1




we find beneficial across our set of benchmarks. To compare our method against existing
work, we perform template-based synthesis of linear supermartingales using Farkas’ Lemma.
This requires deterministic invariants to overapproximate the reachable set of states, which
may either be generated by abstract interpretation, or provided manually [TOUH21]. In our
experiments involving the Farkas’ Lemma, we provide a suitable invariant manually based
on the guard of the loop, in some cases strengthening them with additional constraints by
an educated guess.
     It should be noted that our method is inherently stochastic. One reason is the random
initialisation of the neural template’s parameters in the learning phase. In program-agnostic
synthesis, an additional source of randomness is the sampling of successor states. So that the
results accurately reflect the performance of our method, the random seed for these sources
of randomness is selected differently for each test. An additional source of non-determinism
arises from the SMT solver Z3 as it generates counterexamples: this cannot be controlled
externally. Benchmarks are run on a machine with an Nvidia A40 GPU, and involve the
assertion-violation analysis of programs created using the following two patterns:
Unreliable Hardware: These are programs that execute on unreliable hardware. The
    goal is to upper bound the probability that the program fails to terminate due to a
    hardware fault. A simple example is faulty loop, whose source code is presented
4:18            A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy         Vol. 22:2




                                            100




                     Probability bound p
                       Farkas’ Lemma
                                           10−1



                                           10−2

                                                            Farkas Fails
                                                            Farkas Succeeds
                                           10−3
                                              10−3    10−2      10−1      100
                                                    Probability bound p
                                           Program-Agnostic Neural Supermartingale

Figure 4: Probability bounds generated using program-agnostic neural supermartingales
          and using Farkas’ Lemma. The reference line y = x allows one to see which
          approach outperforms the other and by how much: above the line means that
          neural supermartingales outperform Farkas’ Lemma, below the line the opposite.
          Neural supermartingales can significantly outperform linear templates when a
          better bound exists, but otherwise achieve similar results. Our approach with
          program-aware neural supermartingales provides even better outcomes, compared
          with Farkas’ Lemma.


    in Listing 1, and which consists of a loop which may violate an assertion with small
    probability, modelling a hardware fault.
Robot Motion: These programs model an agent (e.g., a robot) that moves within a
    physical environment. In these benchmarks, the uncertainty in control and sensing is
    modelled probabilistically. The environment contains a target region and a hazardous
    region. The goal is to upper bound the probability that the robot enters the hazardous
    region. We provide the program repulse100 as an example (listing 2), which is a
    variant of repulse (Fig. 2) containing a modified assertion and initial state. The
    program models the motion of a robot in a one-dimensional environment, starting at
    x = 10. The target region is where x < 0, and hazardous region is where x > 100. As
    with repulse, in each iteration there is an equal probability of x being decremented
    by 2, and x being incremented by 1.
Several of the programs are based on benchmarks used in prior work focusing on other types
of supermartingales [ADFG10, CS13]. Additionally, there are several benchmarks that are
entirely new.
     The results are reported in Table 1. The table is divided into three sections. The first
section shows the benchmarks where Farkas’ Lemma cannot be applied, and where only our
method is capable of producing a bound. The second section shows examples where both
methods are able to produce a bound, but our method produces a notably better bound.
The third section shows benchmarks where both methods produce comparable bounds.
Vol. 22:2           QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                      4:19




Table 2: Results showing the time taken in seconds to synthesise supermartingales by our
         method and Farkas’ Lemma. For our method, we show the time taken during
         learning and verification.
        Benchmark            Farkas’          Quantitative Neural Certificates
                             Lemma        Program-Agnostic         Program-Aware
                                       Learn Time Verify Time Learn Time Verify Time
        persist 2d              -        169.14      85.31       44.96       74.90
        faulty marbles          -        114.24      29.23       15.86       28.68
        faulty unreliable       -        123.85      45.48       18.34       33.97
        faulty regions          -         17.92      35.85       17.55       32.38
        cliff crossing        0.11       134.61      19.02       21.27       29.07
        repulse100            0.19        16.65       5.00        6.49        3.74
        repulse100 uniform    0.19        21.28      14.18          -           -
        repulse100 2d         0.12       122.92      64.54       15.75       47.70
        faulty varying        0.36        21.74       5.06        4.71        3.28
        faulty concave        0.39        49.12      13.37       13.49        7.82
        fixed loop            0.15        14.16       3.14        3.34           2.43
        faulty loop           0.16        25.52       3.81        3.73           2.66
        faulty uniform        0.34        20.20       1.91        6.75           1.33
        faulty rare           0.27        25.52       4.27        3.71           2.96
        faulty easy1          0.31       104.20      12.78        4.95           7.51
        faulty ndecr          0.33       104.89       9.06        5.37           4.66
        faulty walk           0.32        15.08       4.00        6.97           3.33



    Dashes in the table indicate experiments where a valid supermartingale could not be
obtained. In the case of Farkas’ Lemma, there are several cases where there is no linear
supermartingale for the benchmark. By contrast, program-agnostic and program-aware syn-
thesis could be applied to almost all benchmarks. The one exception is repulse100 uniform
where only program-aware synthesis was unsuccessful: this is due to indicator functions in
the post-expectation, which are not smooth and posed a problem for the optimiser. This
benchmark underscores the value of program-agnostic synthesis, since it does not require
embedding the explicit post-expectation in the loss function.
    The first section of the benchmarks in Table 1 demonstrates that our method produces
useful results on programs that are out-of-scope for existing techniques. Furthermore, the
success ratio of our method is high on all the benchmarks, which indicates its robustness.
For the second and third sections (which consist of benchmarks to which Farkas’ Lemma is
applicable), the success ratio of our method is broadly maximal, which is to be expected,
since these programs can also be solved by Farkas’ Lemma.
    In the second section of Table 1, we find more complex benchmarks where our method
was able to significantly improve the bound from Farkas’ Lemma. The smallest improvement
was about 0.04, and the largest improvement was over 0.39. The intuition here is that neural
templates allow more sophisticated supermartingales to be learnt, that can approximate
how the reachability probability varies across the state space better than linear templates,
and thereby yield tighter probability bounds.
    The third section of Table 1 consists of relatively simple benchmarks, where our method
produces results that are marginally less tight in comparison to Farkas’ Lemma. This is
4:20             A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy             Vol. 22:2




not surprising since our method uses neural networks consisting of a single neuron for these
examples, owing to their simplicity. The expressive power of these networks is therefore
similar to linear templates.
      In summary, the results show that our method does significantly better on more complex
examples, and marginally worse on very simple examples. This is highlighted in Figure 4.
Each point represents a benchmark. The position on the x-axis shows the probability
bound obtained by our program-agnostic method, and the y-axis shows the probability
bound obtained by Farkas’ Lemma. Points above the line indicate benchmarks where neural
supermartingales outperform Farkas’ Lemma, and vice versa. The scale is logarithmic to
emphasise order-of-magnitude differences.
      Notice that in Table 1 the program-aware algorithm usually yields better bounds than
the program-agnostic algorithm, but the improvement is mostly marginal. This is in fact a
strength of our method: our data-driven approach performs almost as well as one dependent
on symbolic representations, which is promising in light of questions of scalability to more
complex programs. We also include a breakdown of computation time (Table 2) which
allows distinguishing between learning and verification overheads. Notably, Farkas’ Lemma
is significantly faster than our method, given that it relies on solving a convex optimisation
problem via linear programming, whereas the synthesis of neural supermartingales is a
non-convex optimisation problem that is addressed using gradient descent.
      Having presented the experimental results, we shall further comment on some specific
benchmarks. The repulse100 program (listing 2) is a variation of repulse presented in
Fig. 2, but with the assertion changed to assert(x <= 100). While this is a small program,
our method is still able to produce a significantly better result than Farkas’ lemma, using a
neural supermartingale with a single hidden layer consisting of three ReLU components that
are summed together, which allows a convex piecewise linear function to be learnt.
      The cliff crossing program (listing 3) is a further benchmark for which our method
is capable of producing a significantly better bound. cliff crossing (listing 3) models a
robot moving along a road (defined by the region (x, y) ∈ [0, 50] × [0, 10]) that is adjacent to
a cliff (defined by the region with y > 10). This is a 2 dimensional benchmark, for which we
use a neural supermartingale that consists of two input neurons and four ReLU components,
leading to a clear improvement compared to the linear supermartingale in the tightness of
the probability bounds generated, as illustrated by Fig. 5.
      Both repulse100 and cliff crossing are benchmarks that use neural supermartingales
with a single hidden layer. An example that uses two hidden layers is faulty concave
(listing 4), which simulates a program executing on unreliable hardware, where the probability
of a fault varies across the state space. This results in two distinct regions of the state space,
one of which has a significantly higher probability of assertion violation than the other. We
find that neither a linear template nor a single-layer neural supermartingale is able to exploit
this conditional behaviour, each of which yield an overly conservative certificate, but that
a neural supermartingale with two hidden layers is able to more tightly approximate the
reachability probability in each of the two regions.


                                      8. Related Work
The formal verification of probabilistic programs using supermartingales is a well-studied
topic. Early approaches to introduce this technique applied them to almost-sure termination
analysis of probabilistic programs [CS13], which allowed several extensions to polynomial
Vol. 22:2           QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                      4:21




         Listing 1: faulty loop                         Listing 2: repulse100
  error = 0;                                  x = 10;
  i = 0;                                      while x >= 0 do
  while i < 10 do                                 assert ( x <= 100) ;
      assert ( error == 0) ;                      p ~ Bernoulli (0.5) ;
      p ~ Bernoulli (0.999) ;                     if p == 1 then
      if p == 1 then                                   x -= 2
           q ~ Bernoulli (0.5) ;                  else
           if q == 1 then                              x += 1
                 i += 1                           fi
           fi                                 od
      else
           error = 1
      fi
  od

        Listing 3: cliff crossing                   Listing 4: faulty concave
  x = 0;                                      i = 1;
  y = 0;                                      error = 0;
  while x <= 50 do                            while i < 10 do
      assert ( y <= 10) ;                         assert ( error == 0) ;
      p ~ Bernoulli (0.9) ;                       if i < 4 then
      x += 1;                                          p ~ Bernoulli (0.999)
      if p == 0 then                              else
           y += 1                                      p ~ Bernoulli (0.99)
      else                                        fi ;
            if y >= 1 then                        if p == 1 then
                  y -= 1                               q ~ Bernoulli (0.5) ;
            fi                                          if q == 1 then
      fi                                                      i += 1
  od                                                    fi
                                                  else
                                                        error = 1
                                                  fi
                                              od


programs, programs with non-determinism, lexicographic and modular termination argu-
ments, and persistence properties [ACN18, CFG16, CFNH18, CNv17, FC19, HFCG19]. All
these methods relied on symbolic reasoning algorithms for synthesising supermartingales,
that leveraged theories based on Farkas’ lemma for the synthesis of linear certificates, and
Putinar’s Positivestellensatz and sum-of-square methods for the synthesis of polynomial
certificates [CGG+ 25]. While these methods are the state-of-the-art for many existing
problem instances in literature, to achieve the strong guarantees that they provide (such as
4:22              A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy               Vol. 22:2




   1                                                  1


                                           10                                                  10
   0                                                  0
   0                                  5               0                                  5
             20                                                 20
                        40      0                                         40     0
            Linear supermartingale.                            Neural supermartingale.

Figure 5: Supermartingale functions for the cliff crossing benchmark as generated using
          Farkas’ Lemma (on the left) and using neural supermartingales (on the right).
          The right hand figure illustrates the tighter bounds obtainable through the use of
          neural templates.


completeness for the specific class of programs they target), they must necessarily introduce
restrictions on the class of programs to which they are applicable, and the form of certificates
that they derive. Moreover, symbolic methods need externally provided invariants that are
stronger than Rn to enforce non-negativity in the case of linear certificates, as we illustrate in
Fig. 2. Also, symbolic methods for the synthesis of polynomial certificates require compact
deterministic invariants to operate.
     The use of neural networks to represent certificates has allowed many of these restrictions
to be lifted. In the context of the analysis of probabilistic programs, neural networks were
first applied to certify positive almost-sure termination [AGR21]. This approach lent itself
to a wider range of formal verification questions for stochastic dynamical models, from
stability and safety analysis to controller synthesis [LSAZ22, LvCH22, CHLv23, MCL23,
NMTZ24, NGL25]. These data-driven inductive synthesis techniques for supermartingales
have also been extended to machine learning techniques other then deep learning, such
as piecewise linear regression and decision tree learning [BCJ+ 23, BTP+ 22]. Data-driven
techniques for formal verification have also been applied to the construction of system
abstractions, reducing the verification of the original system to a simpler yet equivalent
verification task [AGS24, AEG22, AGMS25, MVF+ 25].
     The present work focuses on verifying the system under analysis through the construction
of proof certificates. In particular, our work extends the data-driven synthesis of neural
supermartingale certificates to quantitative verification questions. The correctness of our
approach builds upon the theory of non-negative repulsing supermartingales [TOUH21], as
formulated in Theorem 5.1. Our experiments have demonstrated that neural certificates
attain comparable results on programs that are amenable to symbolic analysis (such as
those in the third section of Table 1), while surpassing symbolic methods on more complex
programs that are either out-of-scope or yield overly conservative bounds when existing
techniques are applied (such as those in the first and second section of Table 1).
Vol. 22:2              QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                               4:23




                                          9. Conclusion
We have presented a data-driven framework for the quantitative verification of probabilis-
tic models that leverage neural networks to represent supermartingale certificates. Our
experiments have shown that neural certificates are applicable to a wider range of prob-
abilistic models than was previously possible using purely symbolic techniques. We also
illustrate that on existing models our method yields certificates of better or comparable
quality than those produced by symbolic techniques for the synthesis of linear super-
martingales. This builds upon the ability of neural networks to approximate non-linear
functions, while satisfying the constraints imposed by Theorem 5.1 without the need for
supporting deterministic invariants to be provided externally. Our method applies to quan-
titative termination and assertion-violation analysis for probabilistic programs, as well as
safety and invariant verification for stochastic dynamic models. We imagine extensions
to further quantitative verification questions, such as temporal properties beyond reacha-
bility [BK08, AGR24, GKPT24, AGR25, GKPT25], and bounding expected accrued costs
[NCH18, WFG+ 19, WHR21]. While neural networks of no greater than two layers suffice
for our examples, it also remains open to investigate whether deeper network architectures
are beneficial for quantitative verification, as well as their effect on the tightness of bounds
obtained and scalability of the approach.



                                            References
[AAGP21]  Alessandro Abate, Daniele Ahmed, Mirco Giacobbe, and Andrea Peruffo. Formal synthesis of
          Lyapunov Neural Networks. IEEE Control. Syst. Lett., 5(3):773–778, 2021.
[ACN18]   Sheshansh Agrawal, Krishnendu Chatterjee, and Petr Novotný. Lexicographic ranking super-
          martingales: an efficient approach to termination of probabilistic programs. Proc. ACM Program.
          Lang., 2(POPL):34:1–34:32, 2018.
[ADFG10] Christophe Alias, Alain Darte, Paul Feautrier, and Laure Gonnord. Multi-dimensional rankings,
          program termination, and complexity bounds of flowchart programs. In SAS, volume 6337 of
          Lecture Notes in Computer Science, pages 117–133. Springer, 2010.
[AEG22]   Alessandro Abate, Alec Edwards, and Mirco Giacobbe. Neural abstractions. In NeurIPS, 2022.
[AEG+ 23] Alessandro Abate, Alec Edwards, Mirco Giacobbe, Hashan Punchihewa, and Diptarko Roy.
          Quantitative verification with neural networks. In CONCUR, volume 279 of LIPIcs, pages
          22:1–22:18. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2023.
[AG07]    S. Asmussen and P.W. Glynn. Stochastic Simulation: Algorithms and Analysis. Stochastic
          Modelling and Applied Probability. Springer New York, 2007. URL: https://books.google.
          com.sg/books?id=vMI2MdxchU0C.
[AGMS25] Alessandro Abate, Mirco Giacobbe, Christian Micheletti, and Yannik Schnitzer. Branching
          bisimulation learning. In CAV (4), volume 15934 of Lecture Notes in Computer Science, pages
          161–184. Springer, 2025.
[AGR21]   Alessandro Abate, Mirco Giacobbe, and Diptarko Roy. Learning probabilistic termination proofs.
          In CAV (2), volume 12760 of Lecture Notes in Computer Science, pages 3–26. Springer, 2021.
[AGR24]   Alessandro Abate, Mirco Giacobbe, and Diptarko Roy. Stochastic omega-regular verification
          and control with supermartingales. In CAV (3), volume 14683 of Lecture Notes in Computer
          Science, pages 395–419. Springer, 2024.
[AGR25]   Alessandro Abate, Mirco Giacobbe, and Diptarko Roy. Quantitative supermartingale certificates.
          In CAV (2), volume 15932 of Lecture Notes in Computer Science, pages 3–28. Springer, 2025.
[AGS24]   Alessandro Abate, Mirco Giacobbe, and Yannik Schnitzer. Bisimulation learning. In CAV (3),
          volume 14683 of Lecture Notes in Computer Science, pages 161–183. Springer, 2024.
[AKM11]   Alessandro Abate, Joost-Pieter Katoen, and Alexandru Mereacre. Quantitative automata model
          checking of autonomous stochastic hybrid systems. In HSCC, pages 83–92. ACM, 2011.
4:24              A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy                       Vol. 22:2




[Axl19]   S. Axler. Measure, Integration & Real Analysis. Graduate Texts in Mathematics. Springer
          International Publishing, 2019.
[BCJ+ 23] Kevin Batz, Mingshuai Chen, Sebastian Junges, Benjamin Lucien Kaminski, Joost-Pieter Katoen,
          and Christoph Matheja. Probabilistic program verification via inductive synthesis of inductive
          invariants. In TACAS (2), volume 13994 of Lecture Notes in Computer Science, pages 410–429.
          Springer, 2023.
[BdAFK18] Christel Baier, Luca de Alfaro, Vojtech Forejt, and Marta Kwiatkowska. Model checking
          probabilistic systems. In Handbook of Model Checking, pages 963–999. Springer, 2018.
[BHHK10] Christel Baier, Boudewijn R. Haverkort, Holger Hermanns, and Joost-Pieter Katoen. Performance
          evaluation and model checking join forces. Commun. ACM, 53(9):76–85, 2010.
[BK08]    Christel Baier and Joost-Pieter Katoen. Principles of model checking. MIT Press, 2008.
[BS96]    D. P. Bertsekas and S. E. Shreve. Stochastic optimal control: The discrete-time case. Athena
          Scientific, 1996.
[BTP+ 22] Jialu Bao, Nitesh Trivedi, Drashti Pathak, Justin Hsu, and Subhajit Roy. Data-driven invariant
          learning for probabilistic programs. In CAV (1), volume 13371 of Lecture Notes in Computer
          Science, pages 33–54. Springer, 2022.
[CFG16]   Krishnendu Chatterjee, Hongfei Fu, and Amir Kafshdar Goharshady. Termination analysis of
          probabilistic programs through positivstellensatz’s. In CAV (1), volume 9779 of Lecture Notes
          in Computer Science, pages 3–22. Springer, 2016.
[CFNH18] Krishnendu Chatterjee, Hongfei Fu, Petr Novotný, and Rouzbeh Hasheminezhad. Algorithmic
          analysis of qualitative and quantitative termination problems for affine probabilistic programs.
          ACM Trans. Program. Lang. Syst., 40(2):7:1–7:45, 2018.
[CGG+ 25] Krishnendu Chatterjee, Amir Kafshdar Goharshady, Ehsan Kafshdar Goharshady, Mehrdad
          Karrabi, Milad Saadat, Maximilian Seeliger, and Dorde Zikelic. Polyqent: A polynomial quantified
          entailment solver. In ATVA, volume 16145 of Lecture Notes in Computer Science, pages 411–424.
          Springer, 2025.
[CGMv22] Krishnendu Chatterjee, Amir Kafshdar Goharshady, Tobias Meggendorfer, and D̄ord̄e Žikelić.
          Sound and complete certificates for quantitative termination analysis of probabilistic programs.
          In CAV (1), volume 13371 of Lecture Notes in Computer Science, pages 55–78. Springer, 2022.
[CHLv23] Krishnendu Chatterjee, Thomas A. Henzinger, Mathias Lechner, and D̄ord̄e Žikelić. A learner-
          verifier framework for neural network controllers and certificates of stochastic systems. In TACAS
          (1), volume 13993 of Lecture Notes in Computer Science, pages 3–25. Springer, 2023.
[CNv17]   Krishnendu Chatterjee, Petr Novotný, and D̄ord̄e Žikelić. Stochastic invariants for probabilistic
          termination. In POPL, pages 145–160. ACM, 2017.
[CRG19]   Ya-Chien Chang, Nima Roohi, and Sicun Gao. Neural Lyapunov Control. In NeurIPS, pages
          3240–3249, 2019.
[CS13]    Aleksandar Chakarov and Sriram Sankaranarayanan. Probabilistic program analysis with mar-
          tingales. In CAV, volume 8044 of Lecture Notes in Computer Science, pages 511–526. Springer,
          2013.
[dMB08]   Leonardo Mendonça de Moura and Nikolaj S. Bjørner. Z3: an efficient SMT solver. In TACAS,
          volume 4963 of Lecture Notes in Computer Science, pages 337–340. Springer, 2008.
[DP02]    B. A. Davey and H. A. Priestley. Introduction to Lattices and Order. Cambridge University
          Press, 2 edition, 2002. doi:10.1017/CBO9780511809088.
[DS20]    Fredrik Dahlqvist and Alexandra Silva. Semantics of probabilistic programming: A gentle
          introduction. In Gilles Barthe, Joost-Pieter Katoen, and Alexandra Silva, editors, Foundations
          of Probabilistic Programming, pages 1–42. Cambridge University Press, 2020.
[Dur10]   Rick Durrett. Probability: Theory and Examples, 4th Edition. Cambridge University Press, 2010.
[FC19]    Hongfei Fu and Krishnendu Chatterjee. Termination of nondeterministic probabilistic programs.
          In VMCAI, volume 11388 of LNCS, pages 468–490. Springer, 2019.
[FKN+ 11] Vojtech Forejt, Marta Z. Kwiatkowska, Gethin Norman, David Parker, and Hongyang Qu.
          Quantitative multi-objective verification for probabilistic systems. In TACAS, volume 6605 of
          Lecture Notes in Computer Science, pages 112–127. Springer, 2011.
[GHNR14] Andrew D. Gordon, Thomas A. Henzinger, Aditya V. Nori, and Sriram K. Rajamani. Probabilistic
          programming. In FOSE, pages 167–181. ACM, 2014.
Vol. 22:2              QUANTITATIVE VERIFICATION WITH NEURAL NETWORKS                              4:25




[GKP22]   Mirco Giacobbe, Daniel Kroening, and Julian Parsert. Neural termination analysis. In ES-
          EC/SIGSOFT FSE, pages 633–645. ACM, 2022.
[GKPT24] Mirco Giacobbe, Daniel Kroening, Abhinandan Pal, and Michael Tautschnig. Neural model
          checking. In NeurIPS, 2024.
[GKPT25] Mirco Giacobbe, Daniel Kroening, Abhinandan Pal, and Michael Tautschnig. Let a neural
          network be your invariant. In NeurIPS, 2025.
[GMV16]   Timon Gehr, Sasa Misailovic, and Martin T. Vechev. PSI: exact symbolic inference for proba-
          bilistic programs. In CAV (1), volume 9779 of Lecture Notes in Computer Science, pages 62–83.
          Springer, 2016.
[GSV20]   Timon Gehr, Samuel Steffen, and Martin T. Vechev. λPSI: exact inference for higher-order
          probabilistic programs. In PLDI, pages 883–897. ACM, 2020.
[HFCG19] Mingzhang Huang, Hongfei Fu, Krishnendu Chatterjee, and Amir Kafshdar Goharshady. Modular
          verification for almost-sure termination of probabilistic programs. Proc. ACM Program. Lang.,
          3(OOPSLA):129:1–129:29, 2019.
[HLL96]   O. Hernández-Lerma and J. B. Lasserre. Discrete-time Markov control processes, volume 30 of
          Applications of Mathematics. Springer-Verlag, 1996.
[JS21]    Yujia Jin and Aaron Sidford. Towards tight bounds on the sample complexity of average-reward
          mdps. In ICML, volume 139 of Proceedings of Machine Learning Research, pages 5055–5064.
          PMLR, 2021.
[Kal06]   O. Kallenberg. Foundations of modern probability. Springer Science & Business Media, 2006.
[KMN99]   Michael J. Kearns, Yishay Mansour, and Andrew Y. Ng. A sparse sampling algorithm for
          near-optimal planning in large markov decision processes. In IJCAI, pages 1324–1231. Morgan
          Kaufmann, 1999.
[KNP05]   Marta Z. Kwiatkowska, Gethin Norman, and David Parker. Quantitative analysis with the
          probabilistic model checker PRISM. In QAPL, volume 153 of Electronic Notes in Theoretical
          Computer Science, pages 5–31. Elsevier, 2005.
[Koz81]   Dexter Kozen. Semantics of probabilistic programs. J. Comput. Syst. Sci., 22(3):328–350, 1981.
[Kwi07]   Marta Z. Kwiatkowska. Quantitative verification: models techniques and tools. In ESEC/SIG-
          SOFT FSE, pages 449–458. ACM, 2007.
[LSAZ22] A. Lavaei, S. Soudjani, A. Abate, and M. Zamani. Automated verification and synthesis of
          stochastic hybrid systems: A survey. Automatica, 146(12), 2022.
[LvCH22] Mathias Lechner, D̄ord̄e Žikelić, Krishnendu Chatterjee, and Thomas A. Henzinger. Stability
          verification in stochastic control systems via neural network supermartingales. In AAAI, pages
          7326–7336. AAAI Press, 2022.
[MCL23]   Frederik Baymler Mathiesen, Simeon Craig Calvert, and Luca Laurenti. Safety certification for
          stochastic systems via neural barrier functions. IEEE Control. Syst. Lett., 7:973–978, 2023.
[MM02]    Annabelle McIver and Carroll Morgan. Games, probability and the quantitative µ-calculus qmµ.
          In LPAR, volume 2514 of Lecture Notes in Computer Science, pages 292–310. Springer, 2002.
[MM05]    Annabelle McIver and Carroll Morgan. Abstraction, Refinement and Proof for Probabilistic
          Systems. Monographs in Computer Science. Springer, 2005.
[MMLG10] Odalric-Ambrym Maillard, Rémi Munos, Alessandro Lazaric, and Mohammad Ghavamzadeh.
          Finite-sample analysis of bellman residual minimization. In ACML, volume 13 of JMLR Pro-
          ceedings, pages 299–314. JMLR.org, 2010.
[MMS96]   Carroll Morgan, Annabelle McIver, and Karen Seidel. Probabilistic predicate transformers. ACM
          Trans. Program. Lang. Syst., 18(3):325–353, 1996.
[MTG09]   Sean Meyn, Richard L. Tweedie, and Peter W. Glynn. Markov Chains and Stochastic Stability.
          Cambridge Mathematical Library. Cambridge University Press, 2 edition, 2009.
[MVF+ 25] Frederik Baymler Mathiesen, Nikolaus Vertovec, Francesco Fabiano, Luca Laurenti, and Alessan-
          dro Abate. Certified neural approximations of nonlinear dynamics. CoRR, abs/2505.15497,
          2025.
[NCH18]   Van Chan Ngo, Quentin Carbonneaux, and Jan Hoffmann. Bounded expectations: resource
          analysis for probabilistic programs. In PLDI, pages 496–512. ACM, 2018.
[NGL25]   Grigory Neustroev, Mirco Giacobbe, and Anna Lukina. Neural continuous-time supermartingale
          certificates. In AAAI, pages 27538–27546. AAAI Press, 2025.
4:26              A. Abate, A. Edwards, M. Giacobbe, H. Punchihewa, and D. Roy                                             Vol. 22:2




[NMTZ24] Alireza Nadali, Vishnu Murali, Ashutosh Trivedi, and Majid Zamani. Neural closure certificates.
          In AAAI, pages 21446–21453. AAAI Press, 2024.
[PAA21]   Andrea Peruffo, Daniele Ahmed, and Alessandro Abate. Automated and formal synthesis of
          neural barrier certificates for dynamical models. In TACAS (1), volume 12651 of Lecture Notes
          in Computer Science, pages 370–388. Springer, 2021.
[Pol01]   David Pollard. A User’s Guide to Measure Theoretic Probability. Cambridge Series in Statistical
          and Probabilistic Mathematics. Cambridge University Press, 2001.
[Rev75]   D. Revuz. Markov Chains. Mathematical Studies. North-Holland Publishing Company, 1975.
[RF10]    H.L. Royden and P. Fitzpatrick. Real Analysis. Prentice Hall, 4 edition, 2010.
[SA12]    S. Esmaeil Zadeh Soudjani and A. Abate. Adaptive and sequential gridding for abstraction and
          verification of stochastic processes. SIAM Journal on Applied Dynamical Systems, 12(2):921–956,
          2012.
[Sol08]   Armando Solar-Lezama. Program Synthesis by Sketching. PhD thesis, University of California at
          Berkeley, USA, 2008.
[STB+ 06] Armando Solar-Lezama, Liviu Tancau, Rastislav Bodı́k, Sanjit A. Seshia, and Vijay A. Saraswat.
          Combinatorial sketching for finite programs. In ASPLOS, pages 404–415. ACM, 2006.
[TMKA17] Ilya Tkachev, Alexandru Mereacre, Joost-Pieter Katoen, and Alessandro Abate. Quantitative
          model-checking of controlled discrete-time markov processes. Inf. Comput., 253:1–35, 2017.
[TOUH18] Toru Takisaka, Yuichiro Oyabu, Natsuki Urabe, and Ichiro Hasuo. Ranking and repulsing
          supermartingales for reachability in probabilistic programs. In ATVA, volume 11138 of Lecture
          Notes in Computer Science, pages 476–493. Springer, 2018.
[TOUH21] Toru Takisaka, Yuichiro Oyabu, Natsuki Urabe, and Ichiro Hasuo. Ranking and repulsing
          supermartingales for reachability in randomized programs. ACM Trans. Program. Lang. Syst.,
          43(2):5:1–5:46, 2021.
[vBW01]   Franck van Breugel and James Worrell. Towards quantitative verification of probabilistic transi-
          tion systems. In ICALP, volume 2076 of Lecture Notes in Computer Science, pages 421–432.
          Springer, 2001.
[vLHC23] D̄ord̄e Žikelić, Mathias Lechner, Thomas A. Henzinger, and Krishnendu Chatterjee. Learning
          control policies for stochastic systems with reach-avoid guarantees. In AAAI, pages 11926–11935.
          AAAI Press, 2023.
[vLV+ 23] D̄ord̄e Žikelić, Mathias Lechner, Abhinav Verma, Krishnendu Chatterjee, and Thomas A.
          Henzinger. Compositional policy learning in stochastic control systems with formal guarantees.
          In NeurIPS, 2023.
[WFG+ 19] Peixin Wang, Hongfei Fu, Amir Kafshdar Goharshady, Krishnendu Chatterjee, Xudong Qin, and
          Wenjun Shi. Cost analysis of nondeterministic probabilistic programs. In PLDI, pages 204–220.
          ACM, 2019.
[WHR21] Di Wang, Jan Hoffmann, and Thomas W. Reps. Central moment analysis for cost accumulators
          in probabilistic programs. In PLDI, pages 559–573. ACM, 2021.
[Win93]   Glynn Winskel. The formal semantics of programming languages - an introduction. Foundation
          of computing series. MIT Press, 1993.




                                            This work is licensed under the Creative Commons Attribution License. To view a copy of this
                                            license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                            Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse 2,
                                            10777 Berlin, Germany
