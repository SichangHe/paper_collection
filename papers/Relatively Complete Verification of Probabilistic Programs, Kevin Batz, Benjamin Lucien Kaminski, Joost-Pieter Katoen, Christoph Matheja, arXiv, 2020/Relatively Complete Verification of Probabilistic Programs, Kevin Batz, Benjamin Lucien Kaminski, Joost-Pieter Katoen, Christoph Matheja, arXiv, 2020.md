                                         Relatively Complete Verification of Probabilistic Programs
                                         An Expressive Language for Expectation-based Reasoning

                                         KEVIN BATZ∗ , RWTH Aachen University, Germany, Germany
                                         BENJAMIN LUCIEN KAMINSKI, University College London, United Kingdom, United Kingdom
arXiv:2010.14548v2 [cs.LO] 28 Jan 2022




                                         JOOST-PIETER KATOEN∗ , RWTH Aachen University, Germany, Germany
                                         CHRISTOPH MATHEJA, ETH Zürich, Switzerland, Switzerland
                                         We study a syntax for specifying quantitative “assertions”—functions mapping program states to numbers—for
                                         probabilistic program verification. We prove that our syntax is expressive in the following sense: Given any
                                         probabilistic program 𝐶, if a function 𝑓 is expressible in our syntax, then the function mapping each initial
                                         state 𝜎 to the expected value of 𝑓 evaluated in the final states reached after termination of 𝐶 on 𝜎 (also called
                                         the weakest preexpectation wpJ𝐶K (𝑓 )) is also expressible in our syntax.
                                            As a consequence, we obtain a relatively complete verification system for reasoning about expected values
                                         and probabilities in the sense of Cook: Apart from proving a single inequality between two functions given by
                                         syntactic expressions in our language, given 𝑓 , 𝑔, and 𝐶, we can check whether 𝑔 ⪯ wpJ𝐶K (𝑓 ).

                                         February 1, 2022: This is a revised version, correcting technical issues in the proofs of Theorem 8.4 and 9.4.


                                         1   INTRODUCTION
                                         Probabilistic programs are ordinary programs whose execution may depend on the outcome of
                                         random experiments, such as sampling from primitive probability distributions or branching on
                                         the outcome of a coin flip. Consequently, running a probabilistic program (repeatedly) on a single
                                         input generally gives not a single output but a probability distribution over outputs.
                                            Introducing randomization into computations is an important tool for the design and analysis of
                                         efficient algorithms [Motwani and Raghavan 1999]. However, increasing efficiency by randomization
                                         often comes at the price of introducing a non-zero probability of producing incorrect outputs.
                                         Furthermore, even though a program may be efficient in expectation, individual executions may
                                         exhibit a long—even infinite—run time [Bournez and Garnier 2005; Kaminski et al. 2018].
                                            Reasoning about these probabilistic phenomena is hard. For instance, deciding termination
                                         of probabilistic programs has been shown to be strictly more complex than for ordinary pro-
                                         grams [Kaminski and Katoen 2015; Kaminski et al. 2019]. Nonetheless, probabilistic program
                                         verification is an active research area. After seminal work on probabilistic program semantics by
                                         Kozen [1979, 1981], many different techniques have been developed, see [Hart et al. 1982] for an early
                                         example. Modern approaches include, amongst others, martingale-based techniques [Chakarov
                                         and Sankaranarayanan 2013; Chatterjee et al. 2016a,b, 2017; Fu and Chatterjee 2019; Huang et al.
                                         2018] and weakest-precondition-style calculi [Batz et al. 2019; Kaminski 2019; Kaminski et al. 2018;
                                         McIver and Morgan 2005; Ngo et al. 2018]. The former can be phrased in terms of the latter, and
                                         all of the aforementioned techniques can be understood as instances or extensions of Kozen’s
                                         probabilistic propositional dynamic logic (PPDL) [Kozen 1983, 1985].

                                         ∗ Batz and Katoen are supported by the ERC AdG 787914 FRAPPANT.




                                         Authors’ addresses: Kevin Batz, RWTH Aachen University, Germany, Germany, kevin.batz@cs.rwth-aachen.de; Benjamin
                                         Lucien Kaminski, University College London, United Kingdom, United Kingdom, b.kaminski@ucl.ac.uk; Joost-Pieter Katoen,
                                         RWTH Aachen University, Germany, Germany, katoen@cs.rwth-aachen.de; Christoph Matheja, ETH Zürich, Switzerland,
                                         Switzerland, cmatheja@inf.ethz.ch.


                                                                           Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
2                                                                                 Batz, Kaminski, Katoen, and Matheja


   Probabilistic program verification, extensionally. There are two perspectives for reasoning about
programs: the extensional and the intensional. Whereas intensional approaches provide a syntax, i.e.,
a formal language, for assertions, extensional approaches admit arbitrary assertions and dispense
with considerations about syntax altogether—they treat assertions as purely mathematical entities.
   A standard technique for probabilistic program verification that takes the extensional approach
is the weakest preexpectation (wp) calculus of McIver and Morgan [2005]—itself an instance of
Kozen’s PPDL [Kozen 1983, 1985]. Given a probabilistic program 𝐶 and some function 𝑓 (called
the postexpectation), mapping (final) states to numbers, the weakest preexpectation wpJ𝐶K (𝑓 ) is a
mapping from (initial) states to numbers, such that

                                      Expected value of 𝑓 , measured in final states reached
               wpJ𝐶K (𝑓 ) (𝜎) =
                                      after termination of 𝐶 on initial state 𝜎 .
For probabilistic programs with discrete probabilistic choices, the wp calculus can be defined for
arbitrary real-valued postexpectations 𝑓 [Kaminski 2019; McIver and Morgan 2005].
   Probabilistic program verification, intensionally. While the extensional approach often yields
elegant formalisms, it is unsuitable for developing practical verification tools, which ultimately rely
on some syntax for assertions. In particular, we cannot—in general—rely on the property, implicitly
assumed in the extensional approach, that there is no distinction between assertions representing
                                                                         Í∞
the same mathematical entity: a tool may not realize that 4 · 0.5 and 𝑖=     0 /2 represent the same
                                                                               1 𝑖
mathematical entity (the number 2).
   An example of intensional probabilistic program verification is the verifier of Ngo et al. [2018]
which specifies a simple syntax which is extensible by user-specified base and rewrite functions.
  Main contribution. Given a calculus for program verification and an assertion language, two
fundamental questions immediately arise:
     (1) Soundness: Are only true assertions derivable in the calculus?
     (2) Completeness: Can every true assertion be derived and is it expressible in the assertion language?
While soundness is typically a must for any verification system, completeness is—as noted by Apt
and Olderog [2019] in their recent survey of 50 years of Hoare logic—a “subtle matter and requires
careful analysis”.
   In fact, to the best of our knowledge, existing probabilistic program verification techniques
(including all of the above references amongst many other works) either take the extensional
approach or do not aim for completeness. In this paper, we take the intensional path and make the
following contribution to formal reasoning about probabilistic programs:

    We provide a simple formal language of functions for probabilistic program verification such that:
              If 𝑓 is syntactically expressible, then wpJ𝐶K (𝑓 ) is syntactically expressible.

A language from which we can draw functions 𝑓 with the above property is called expressive. Having
an expressive language renders the wp calculus relatively complete [Cook 1978]: Given functions 𝑓
and 𝑔 in our language and a probabilistic program 𝐶, suppose we want to verify 𝑔 ⪯ wpJ𝐶K (𝑓 ),
where ⪯ denotes the point-wise order of functions mapping states to numbers. Due to expressive-
ness, we can effectively construct in our language a function ℎ representing wpJ𝐶K (𝑓 ). Hence,
verification is complete modulo checking whether the inequality 𝑔 ⪯ ℎ between two functions
in our language holds. Indeed, Hoare logic is also only complete modulo deciding an implication
between two formulae in the language of first-order arithmetic [Apt and Olderog 2019].

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                            3


   Challenges and usefulness. Notice that providing some expressive language is rather easy: A single-
ton language that can only represent the null-function is trivially expressive since, for any program
𝐶, the expected value of 0 is 0. That is, wpJ𝐶K (0) = 0. The challenge in a quest for an expressive
language for probabilistic program verification is hence to find a language that (i) is closed under
taking weakest preexpectations and (ii) can express interesting (quantitative) properties.
   Indeed, our language can: For instance, it is capable of expressing termination probabilities
(via wpJ𝐶K (1)—the expected value of the constant function 1). These can be irrational numbers
like the reciprocal of the golden ratio 1/𝜑 [Olmedo et al. 2016]. In general, termination probabilities
carry a high internal degree of complexity [Kaminski et al. 2019]. Our language can also express
probabilities√over program variables on termination of a program and that can be expressed in
terms of 𝜋, 3 and so forth. These can e.g., be generated by Buffon machines, i.e., probabilistic
programs that only use Bernoulli experiments [Flajolet et al. 2011].
   Termination probabilities already hint at one of the technical challenges we face: Even starting
from a constant function like 1, our language has to be able to express mappings from states to
highly complex real numbers. Another challenge we face is that when constructing wpJ𝐶K (𝑓 ), due
to probabilistic branching in combination with loops, considering single execution traces is not
enough: We have to collect all terminating traces and average over the values of 𝑓 in terminal states.
We attack these challenges via Gödel numbers for rational sequences and encodings of Dedekind
cuts.
   Aside from termination probabilities, our language is capable of expressing a wide range of
practically relevant functions, like polynomials or Harmonic numbers. Polynomials are a common
subclass of ranking functions1 for automated probabilistic termination analysis; harmonic numbers
are ubiquitous in expected runtime analysis. We present more scenarios covered by our syntax and
avenues for future work in Sections 12 and 13.
   Overall, we believe that an expressive syntax for probabilistic program verification is what really
expedites a search for tractable fragments of both programs and “assertion” language in the first
place. Studying such fragments may also yield additional insights: For example, Kozen [2000] and
Kozen and Tiuryn [2001] studied the propositional fragment of Hoare logic and showed that it is
subsumed by an extension of KAT—Kleene algebra with tests.
  Further related work. Relative completeness of Hoare logic was shown by Cook [1978]. Winskel
[1993] and Loeckx et al. [1984] proved expressiveness of first-order arithmetic for Dijkstra’s
weakest precondition calculus. For separation logic [Reynolds 2002]—a very successful logic for
compositional reasoning about pointer programs—expressiveness was shown by Tatsuta et al. [2009,
2019], almost a decade later than the logic was originally developed and started to be used.
  Perhaps most directly related to this paper is the work by den Hartog and de Vink [2002] on a
Hoare-like logic for verifying probabilistic programs. They prove relative completeness (also in the
sense of Cook [1978]) of their logic for loop-free probabilistic programs and restricted postconditions;
they leave expressiveness for loops as an open problem: “It is not clear whether the probabilistic
predicates are sufficiently expressive [. . . ] for a given while loop.”
Organization of the paper. We give an introduction to syntax, extensional semantics, and verification
systems for probabilistic programs, in particular the weakest preexpectation calculus, in Section 2.
We formulate the expressiveness problem in Section 3. We define the syntax and semantics of our
expressive language of expectations in Section 4. We prove expressiveness of our language for loop-free
probabilistic programs in Section 5. We then move to proving expressiveness of our language
for loops. We outline the expressiveness proof for loops in Section 6 and do the full technical proof
1 In probabilistic program analysis terminology: ranking supermartingales.



                                   Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
4                                                                                    Batz, Kaminski, Katoen, and Matheja


throughout Sections 7 – 10. In Section 11 and Section 12, we discuss extensions and a few scenarios
in which our language could be useful; we conclude in Section 13.

2     PROBABILISTIC PROGRAMS — THE EXTENSIONAL PERSPECTIVE
We briefly recap classical reasoning about probabilistic programs á la Kozen [1985], which is
agnostic of any particular syntax for expressions or formulae—it takes an extensional approach.

2.1     The Probabilistic Guarded Command Language
We consider the imperative probabilistic programming language pGCL featuring discrete proba-
bilistic choices—branching on outcomes of coin flips—as well as standard control-flow instructions.
2.1.1   Syntax. Formally, a program 𝐶 in pGCL adheres to the grammar
                   𝐶        −→          skip                                                      (effectless program)
                                            |   𝑥 := 𝑎                                                     (assignment)
                                            | 𝐶;𝐶                                           (sequential composition)
                                            |   {𝐶 } [ 𝑝 ] {𝐶 }                                  (probabilistic choice)
                                            |   if ( 𝜑 ) { 𝐶 } else { 𝐶 }                         (conditional choice)
                                            |   while ( 𝜑 ) { 𝐶 } ,                                         (while loop)
where 𝑥 is taken from a countably infinite set of variables Vars, 𝑎 is an arithmetic expression over
variables, 𝑝 ∈ [0, 1] ∩ Q is a rational probability, and 𝜑 is a Boolean expression (also called guard)
over variables. For an overview of metavariables 𝐶, 𝑥, 𝑎, 𝜑, . . . , used throughout this paper, see
Table 1 at the end of this section.
   For the moment, we assume that both arithmetic and Boolean expressions are standard expres-
sions without bothering to provide them with a concrete syntax. However, we will require them to
adhere to a concrete syntax which we provide in Sections 4.1 and 4.2.
2.1.2 Program States. A program state 𝜎 maps each variable in Vars to its value—a positive rational
number in Q ≥0 .2 To ensure that the set of program states is countable,3 we restrict ourselves to
states in which at most finitely many variables—intuitively those that appear in a given program—
are assigned non-zero values; every state can thus be understood as a finite mapping that only
keeps track of assignments to non-zero values. Formally, the set Σ of program states is
                   Σ = 𝜎 : Vars → Q ≥0 { 𝑥 ∈ Vars | 𝜎 (𝑥) ≠ 0 } is finite .
                         

We use metavariables 𝜎, 𝜏, . . . , for program states, see also Table 1. We denote by 𝜎 J𝑒K the evaluation
of (arithmetic or Boolean) expression 𝑒 in 𝜎, i.e., the value obtained from evaluating 𝑒 after replacing
every variable 𝑥 in 𝑒 by 𝜎 (𝑥). We define the semantics of expressions more formally in Section 4.4.
2.1.3 Forward Semantics. One of the earliest ways to give semantics to a probabilistic program 𝐶
is by means of forward-moving measure transformers [Kozen 1979, 1981]. These transform an
initial state 𝜎 into a probability distribution 𝜇𝐶𝜎 over final states (i.e., a measure on Σ). We consider
Kozen’s semantics the reference forward semantics. More operational semantics are provided in
the form of probabilistic transition systems [Gretz et al. 2014; Kaminski 2019], where programs
describe potentially infinite Markov chains whose state spaces comprise of program states, or trace
2 To keep the presentation simple, we consider only unsigned variables; we discuss this design choice and an extension to

signed variables, which can also evaluate to negative rationals, in Section 11.
3 Working with probabilistic programs over a countable set of states avoids technical issues related to measurability.



Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                               5


semantics [Cousot and Monerau 2012; Di Pierro and Wiklicky 2016; Kaminski et al. 2019], where
the traces are sequences of program states and each trace is assigned a certain probability.
   In any of these semantics, the probabilistic choice { 𝐶 1 } [ 𝑝 ] { 𝐶 2 } flips a coin with bias 𝑝
towards heads. If the coin yields heads, 𝐶 1 is executed (with probability 𝑝); otherwise, 𝐶 2 . Moreover,
skip does nothing. 𝑥 := 𝑎 assigns the value of expression 𝑎 (evaluated in the current program
state) to 𝑥. The sequential composition 𝐶 1 ; 𝐶 2 first executes 𝐶 1 and then 𝐶 2 . The conditional choice
if ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 } executes 𝐶 1 if the guard 𝜑 is satisfied; otherwise, it executes 𝐶 2 . Finally,
the loop while ( 𝜑 ) { 𝐶 } keeps executing the loop body 𝐶 as long as 𝜑 evaluates to true.

2.2   Weakest Preexpectations
Dually to the forward semantics, probabilistic programs can also be provided with semantics in the
form of backward-moving random variable transformers, originally due to Kozen [1983, 1985]. This
paper is set within this dual view, which is a standard setting for probabilistic program verification.
2.2.1 Expectations. Floyd-Hoare logic [Floyd 1967; Hoare 1969] as well as the weakest precondition
calculus of Dijkstra [1976] employ first-order predicates for reasoning about program correctness.
For probabilistic programs, Kozen [1983, 1985] was the first to generalize from predicates to
measurable functions (or random variables). Later, McIver and Morgan [2005] coined the term
expectation—not to be confused with expected value—for such functions. In reference to Dijkstra’s
weakest precondition calculus, their verification system is called the weakest preexpectation calculus.
   Formally, the set E of semantic expectations is defined as
                                    E = 𝑋 𝑋 : Σ → R∞
                                           
                                                            ≥0   ,
i.e., functions 𝑋 that associate a non-negative quantity (or infinity) to each program state. We use
metavariables 𝑋 , 𝑌 , 𝑍 for semantic expectations.
   Expectations form the assertion “language” of the weakest preexpectation calculus. However, we
note that—so far—expectations are in no way defined syntactically: They are just the whole set of
functions from Σ to R∞  ≥ 0 . It is hence borderline to speak of a language. The goal of this paper is to
provide a syntactically defined subclass of E—i.e., an actual language—such that formal reasoning
about probabilistic programs can take place completely within this class.
   We furthermore note that we work with more general expectations than McIver and Morgan
[2005], who only allow bounded expectations, i.e., expectations 𝑋 for which there is a bound 𝛼 ∈ R ≥0
such that ∀𝜎 : 𝑋 (𝜎) ≤ 𝛼. In contrast to McIver and Morgan, our structure (E, ⪯) of unbounded
expectations forms a complete lattice with least element 0 and greatest element ∞, where ⪯ lifts
the standard ordering ≤ on the (extended) reals to expectations by pointwise application. That is,
                               𝑋 ⪯ 𝑌          iff         ∀𝜎 ∈ Σ :      𝑋 (𝜎) ≤ 𝑌 (𝜎) .
Examples of (bounded) expectations include, for instance, Iverson [1962] brackets [𝜑], which
associate to a Boolean expression 𝜑 its indicator function:4
                                             (
                                               1, if 𝜎 J𝜑K = true
                                [𝜑] = 𝜆𝜎 .
                                               0, if 𝜎 J𝜑K = false .
Iverson brackets embed Boolean predicates into the set of expectations, rendering McIver and
Morgan’s calculus a conservative extension of Dijkstra’s calculus.
  Examples of unbounded expectations are arithmetic expressions over variables, like
                                            𝑥 + 𝑦 = 𝜆𝜎 . 𝜎 (𝑥) + 𝜎 (𝑦) ,
4 We use 𝜆-expressions to denote functions; function 𝜆𝑥   . 𝑓 applied to 𝑎 evaluates to 𝑓 in which 𝑥 is replaced by 𝑎.

                                   Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
6                                                                                           Batz, Kaminski, Katoen, and Matheja


                                       𝝈                                                           𝝈′
        wpJ𝐶K (𝑋 )                                                    wpJ𝐶K (𝑋 )

                                  •        𝐶
                                                                                                    •
                                                                                                          𝐶

                h •            •              •                             h •           •
                                                         ..       i                                                ..       i
             Exp 𝑋 (𝜏1 )     𝑋 (𝜏2 )        𝑋 (𝜏3 )           .          Exp 𝑋 (𝜏 ′ )   𝑋 (𝜏2′ )          •             .
                                                                                 1
                                                                                                        𝑋 (𝜏3′ )


Fig. 1. The weakest preexpectation wpJ𝐶K (𝑋 ) maps every initial state 𝜎 to the expected value of 𝑋 , measured
with respect to the final distribution over states reached after termination of program 𝐶 on input 𝜎. wpJ𝐶K is
backward-moving in the sense that it transforms an 𝑋 : Σ → R∞         ≥ 0 , evaluated in final states after termination
of 𝐶, into wpJ𝐶K (𝑋 ) : Σ → R∞   ≥ 0 , evaluated in initial states before execution of 𝐶.


where we point-wise lifted common operators on the reals, such as +, to operators on expectations.
Strictly speaking, McIver and Morgan’s calculus cannot handle expectations like 𝑥 + 𝑦 off-the-shelf.
   We denote by 𝑋 [𝑥/𝑎] the “substitution” of variable 𝑥 by expression 𝑎 in expectation 𝑋 , i.e.,
                                                                            (
                                                                          𝑟,      if 𝑦 = 𝑥,
     𝑋 [𝑥/𝑎] = 𝜆𝜎 . 𝑋 𝜎 𝑥 ↦→ J𝑎K ,
                                𝜎
                                             where       𝜎 [𝑥 ↦→ 𝑟 ] = 𝜆𝑦 .
                                                                              𝜎 (𝑦), else.
2.2.2 Backward Semantics: The Weakest Preexpectation Calculus. Suppose we are interested in the
expected value of the quantity (expectation) 𝑋 after termination of 𝐶. In analogy to Dijkstra, 𝑋 is
called the postexpectation and the sought-after expected value is called the weakest preexpectation
of 𝐶 with respect to postexpectation 𝑋 , denoted wpJ𝐶K (𝑋 ) [McIver and Morgan 2005]. As the
expected value of 𝑋 generally depends on the initial state 𝜎 on which 𝐶 is executed, the weakest
preexpectation wpJ𝐶K (𝑋 ) is itself also a map of type E, mapping an initial program state 𝜎 to the
expected value of 𝑋 (measured in the final states) after successful termination of 𝐶 on 𝜎, see Figure 1.
The weakest preexpectation calculus is a backward semantics in the sense that it transforms a
postexpectation 𝑋 ∈ E, evaluated in final states after termination of 𝐶, into a preexpectation
wpJ𝐶K (𝑋 ) ∈ E, evaluated in initial states before execution of 𝐶.
   Between forward-moving measure transformers and backward-moving expectation transformers,
there exists the following duality established by Kozen:
  Theorem 2.1 (Kozen Duality [1983; 1985]). If 𝜇𝐶𝜎 is the distribution over final states obtained by
running 𝐶 on initial state 𝜎, then for any postexpectation 𝑋 ,
                                 ∑︁
                                     𝜇𝐶𝜎 (𝜏) · 𝑋 (𝜏) = wpJ𝐶K (𝑋 ) (𝜎) .
                                           𝜏 ∈Σ

In particular, if 𝑋 = [𝜑], then wpJ𝐶K (𝑋 ) (𝜎) is the probability that running 𝐶 on 𝜎 terminates in a
final state satisfying 𝜑—thus generalizing Dijkstra’s weakest preconditions.
   As with standard weakest preconditions, weakest preexpectations are not determined monolithi-
cally for the whole program 𝐶 as characterized above. Rather, they are determined compositionally
using a backward-moving expectation transformer
                                                      wp : pGCL → (E → E)
which is defined recursively on the structure of 𝐶 according to the rules in Figure 2. Most of
these rules are standard: wpJskipK is the identity as skip does not modify the program state.
For the assignment 𝑥 := 𝑎, wpJ𝑥 := 𝑎K (𝑋 ) substitutes in 𝑋 the assignment’s left-hand side 𝑥 by
its right-hand side 𝑎. For sequential composition, wpJ𝐶 1 ; 𝐶 2 K (𝑋 ) first determines the weakest

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                            7


                  𝑪                                     wp J𝑪K (𝑿 )
                  skip                                  𝑋
                  𝑥 := 𝑎                                𝑋 [𝑥/𝑎]
                                                        wpJ𝐶 1 K wpJ𝐶 2 K (𝑋 )
                                                                                  
                 𝐶1 ; 𝐶2
                  { 𝐶1 } [ 𝑝 ] { 𝐶2 }                   𝑝 · wpJ𝐶 1 K (𝑋 ) + (1 − 𝑝) · wpJ𝐶 2 K (𝑋 )
                  if ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }         [𝜑] · wpJ𝐶 1 K (𝑋 ) + [¬𝜑] · wpJ𝐶 2 K (𝑋 )
                  while ( 𝜑 ) { 𝐶 ′ }                   lfp 𝑌 . [¬𝜑] · 𝑋 + [𝜑] · wpJ𝐶 ′K (𝑌 )

     Fig. 2. Rules defining the weakest preexpectation of program 𝐶 with respect to postexpectation 𝑋 .


preexpectation wpJ𝐶 2 K (𝑋 ) which is then fed into wpJ𝐶 1 K as a postexpectation. For both the
probabilistic choice { 𝐶 1 } [ 𝑝 ] { 𝐶 2 } and the conditional choice if ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }, the
weakest preexpectation with respect to 𝑋 yields a convex sum 𝑝 · wpJ𝐶 1 K (𝑋 ) + (1 − 𝑝) · wpJ𝐶 2 K (𝑋 ).
In the former case, the weights are given by the probability 𝑝. In the latter case, they are determined
by the guard 𝜑, i.e., we have 𝑝 = [𝜑] and 1 − [𝜑] = [¬𝜑].
   The weakest preexpectation of a loop is given by the least fixed point of its unrollings, i.e.,
                                  wpJwhile ( 𝜑 ) { 𝐶 ′ }K (𝑋 ) = lfp 𝑌 . Φ𝑋 (𝑌 ) ,
where the characteristic function Φ𝑋 of while ( 𝜑 ) { 𝐶 ′ } with respect to 𝑋 ∈ E is defined as
                           Φ𝑋 :     E → E,      𝑌 ↦→ [¬𝜑] · 𝑋 + [𝜑] · wpJ𝐶 ′K (𝑌 ) .
Since (E, ≤) is a complete lattice and Φ𝑋 is monotone, fixed points exist due to the Knaster-Tarski
fixed point theorem; we take the least fixed point because we reason about total correctness.
   Throughout this paper, we exploit that Φ𝑋 is, in fact, Scott-continuous (cf. [Olmedo et al. 2016]).
Kleene’s theorem then allows us to approximate the least fixed point iteratively:
    Lemma 2.2 (Kleene et al. [1952]). We have
                       wpJwhile ( 𝜑 ) { 𝐶 ′ }K (𝑋 ) = lfp 𝑌 . Φ𝑋 (𝑌 ) = sup Φ𝑛𝑋 (0) ,
                                                                                  𝑛 ∈N
where 0 = 𝜆𝜎 . 0 is the constant-zero expectation and Φ𝑛𝑋 (𝑌 ) denotes the 𝑛-fold application of Φ𝑋 to 𝑌 .

3    TOWARDS AN EXPRESSIVE LANGUAGE FOR EXPECTATIONS
As long as we take the extensional approach to program verification, i.e., we admit all expectations
in E, reasoning about expected values of pGCL programs is complete: For every program 𝐶 and
postexpectation 𝑋 , it is, in principle, possible to find an expectation wpJ𝐶K (𝑋 ) ∈ E which—by the
above soundness property—coincides with the expected value of 𝑋 after termination of 𝐶.
   The main goal of this paper is to enable (relatively) complete verification of probabilistic programs
by taking an intensional approach. That is, we use the same verification technique described in
Section 2 (i.e., the weakest preexpectation calculus) but
                                fix a set Exp of syntactic expectations 𝑓 .
We use metavariables 𝑓 , 𝑔, ℎ, . . . , for syntactic expectations, as opposed to 𝑋 , 𝑌 , 𝑍 , . . . , for semantic
expectations in E, see also Table 1. While 𝑓 itself is merely a syntactic entity to begin with, we
denote by J𝑓 K the corresponding semantic expectation in E. Having a syntactic set of expectations
at hand immediately raises the question of expressiveness:

                                   Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
8                                                                                 Batz, Kaminski, Katoen, and Matheja


                               Table 1. Metavariables used throughout this paper.


          Entities                            Metavariables                Domain           Defined in
          Natural numbers                     𝑛, 𝑖, 𝑗, 𝑘                   N
          Positive rationals                  𝑟, 𝑠, 𝑡                      Q ≥0
          Positive extended reals             𝛼, 𝛽, 𝛾                      R∞
                                                                            ≥0
          Rational probabilities              𝑝, 𝑞                         [0, 1] ∩ Q

          Variables                           𝑥, 𝑦, 𝑧, 𝑣, 𝑤, 𝑢, 𝑛𝑢𝑚        Vars             Section 2.1
          Arithmetic expressions              𝑎, 𝑏                         AExpr            Section 4.1
          Boolean expressions                 𝜑, 𝜓, 𝜉                      Bool             Section 4.2

          Syntactic expectations              𝑓 , 𝑔, ℎ                     Exp              Section 4.3
          Semantic expectations               𝑋, 𝑌 , 𝑍                     E                Section 2.2.1

          Programs                            𝐶                            pGCL             Section 2.1
          Program states                      𝜎, 𝜏                         Σ                Section 2.1.2


            For 𝑓 ∈ E, is the weakest preexpectation wpJ𝐶K (J𝑓 K) again expressible in E?
    Definition 3.1 (Expressiveness of Expectations). The set Exp of syntactic expectations is expressive
iff for all programs 𝐶 and all 𝑓 ∈ Exp there exists a syntactic expectation 𝑔 ∈ Exp, such that
                                                  wpJ𝐶K (J𝑓 K) = J𝑔K .                                             △
Notice that constructing some expressive set of syntactic expectations is straightforward. For
example, the set Exp = {0}, which consists of a single expectation 0—interpreted as the constant
expectation J0K = 𝜆𝜎 . 0—is expressive: wpJ𝐶K (J0K) = J0K holds for every 𝐶 by strictness of wp.5
    The main challenge is thus to find a syntactic set Exp that (i) can be proven expressive and
(ii) covers interesting properties—at the very least, it should cover all Boolean expressions 𝜑 (to
reason about probabilities) and all arithmetic expressions 𝑎 (to reason about expected values).

4     SYNTACTIC EXPECTATIONS
We now describe the syntax and semantics for a set Exp of syntactic expectations which we will
(in the subsequent sections) prove to be expressive and which can be used to express interesting
properties such as, amongst others, the expected value of a variable 𝑥, the probability to terminate,
the probability to terminate in a set described by a first-order arithmetic predicate 𝜑, etc.

4.1    Syntax of Arithmetic Expressions
We first describe a syntax for arithmetic expressions, which form precisely the right-hand-sides of
assignments that we allow in pGCL programs. Naturally, the syntax of arithmetical expressions will
reoccur in our syntax of expectations. Formally, the set AExpr of arithmetic expressions is given by
                   𝑎       −→          𝑟 ∈ Q ≥0                                         (non-negative rationals)
                                          |    𝑥 ∈ Vars                                   (Q ≥0 -valued variables)
                                          |    𝑎 +𝑎                                                       (addition)
5 wp being strict means that wpJ𝐶K (0) = 0 for every 𝐶, see [Kaminski 2019].



Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                               9


                                              |        𝑎 ·𝑎,                                             (multiplication)
                                              |        𝑎 −¤ 𝑎 ,                   (subtraction truncated at 0 (“monus”))

where Vars is a countable set of Q ≥0 -valued variables. We use metavariables 𝑟, 𝑠, 𝑡 for non-negative
rationals, 𝑥, 𝑦, 𝑧, 𝑣, 𝑤, 𝑢 for variables, and 𝑎, 𝑏, 𝑐 for arithmetic expressions, see also Table 1.

4.2   Syntax of Boolean Expressions
We next describe a syntax for Boolean expressions over AExpr, which form precisely the guards that
we allow in pGCL programs (for conditional choices and while loops). Again, the syntax of Boolean
expressions will also naturally reoccur in our syntax of expectations. Formally, the set Bool of
Boolean expressions is given by

                     𝜑      −→            𝑎<𝑎                                (strict inequality of arithmetic expressions)
                                                  |    𝜑 ∧𝜑                                                (conjunction)
                                                  |     ¬𝜑 .                                                   (negation)

We use metavariables 𝜑, 𝜓, 𝜉 for Boolean expressions, see also Table 1.
 The following expressions are syntactic sugar with their standard interpretation and semantics:

             false ,       true ,         𝜑 ∨𝜓 ,                  𝜑 −→ 𝜓 ,        𝑎 =𝑏,       and      𝑎 ≤𝑏.

4.3   Syntax of Expectations
We now describe the syntax of a set of expressive expectations which can be used as both pre- and
postexpectations for the verification of probabilistic programs. Formally, the set Exp of syntactic
expectations is given by

                 𝑓        −→          𝑎                                                         (arithmetic expressions)
                                          |           [𝜑] · 𝑓 | 𝑓 · [𝜑]                                        (guarding)
                                          |           𝑓 +𝑓                                                     (addition)
                                          |           𝑎 · 𝑓 | 𝑓 ·𝑎                   (scaling by arithmetic expressions)
                                          |           S𝑥 : 𝑓                                          (supremum over 𝑥)
                                          |           J 𝑥: 𝑓 .                                          (infimum over 𝑥)

As mentioned before, we use metavariables 𝑓 , 𝑔, ℎ for syntactic expectations, see also Table 1. Let
us go over the different possibilities of syntactic expectations according to the above grammar.

   Arithmetic expressions. These form the base case and it is immediate that they are needed for an
expressive language. Assume, for instance, that we want to know the “expected” (in fact: certain)
value of variable 𝑥—itself an arithmetic expression by definition—after executing 𝑥 := 𝑎. Then this is
given by wpJ𝑥 := 𝑎K (𝑥) = 𝑎—again an arithmetic expression. As 𝑎 could have been any arithmetic
expression, we at least need all arithmetic expressions in an expressive expectation language.

   Guarding and addition. Both guarding—multiplication with a predicate—and addition are used
for expressing weakest preexpectations of conditional choices and loops. As we have, for instance,

           wpJif ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }K (𝑓 ) = [𝜑] · wpJ𝐶 1 K (𝑓 ) + [¬𝜑] · wpJ𝐶 1 K (𝑓 ) ,

it is evident that guarding and addition is convenient, if not necessary, for being expressive.

                                    Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
10                                                                                     Batz, Kaminski, Katoen, and Matheja


                                 𝝈                                                          𝝈
         𝒂                           J𝒂K                                        𝝋               J𝝋K = true     iff
                                                                                            𝜎
        𝑟    (∈ Q ≥0 )          𝑟                                               𝑎 <𝑏            J𝑎K < 𝜎 J𝑏K
                                                                                            𝜎
        𝑥      (∈ Vars)         𝜎 (𝑥)                                           𝜓 ∧𝜉            J𝜓 K = true = 𝜎 J𝜉K
                                 𝜎
        𝑏 +𝑐                         J𝑏K + 𝜎 J𝑐K                                ¬𝜓          𝜎
                                                                                                J𝜓 K = false
                                 𝜎         𝜎
        𝑏 ·𝑐                         J𝑏K · J𝑐K
                                (
                                     𝜎
                                      J𝑏K − 𝜎 J𝑐K ,       if 𝜎 J𝑏K ≥ 𝜎 J𝑐K
        𝑏 −¤ 𝑐
                                     0,                   else
                 Table 2. The semantics of arithmetic expressions 𝑎 and Boolean expressions 𝜑.



   Scaling by arithmetic expressions. One could ask why we restrict to multiplications of arithmetic
expressions and expectations and do not simply allow for multiplication of two arbitrary expec-
tations 𝑓 · 𝑔. We will defer this discussion to Section 4.6. For now, it suffices to say that we can
express all multiplications we need without running into trouble with quantifiers which would
happen otherwise.
    Suprema and infima. The supremum and infimum constructs S𝑥 : 𝑓 and J 𝑥 : 𝑓 take over the role
of the ∃ and ∀ quantifiers of first-order logic. We use them to bind variables 𝑥. The S and J quan-
tifiers are necessary to make our expectation language expressive in the same was as, for instance,
at least the ∃ quantifier is necessary to make first-order logic expressive for weakest preconditions
of non-probabilistic programs.
   As is standard, we additionally admit parentheses for clarifying the order of precedence in
syntactic expectations. To keep the amount of parentheses to a minimum, we assume that · has
precedence over + and that the quantifiers Sand J have the least precedence.
   The set of free variables FV (𝑓 ) ⊆ Vars is the set of all variables that occur syntactically in 𝑓 and
that are not in the scope of some Sor J quantifier. We write 𝑓 (𝑥 1, . . . , 𝑥𝑛 ) to indicate that at most
the variables 𝑥 1, . . . , 𝑥𝑛 occur freely in 𝑓 .
   Given a syntactic expectation 𝑓 , a variable 𝑥 ∈ FV (𝑓 ), and an arithmetic expression 𝑎, we
denote by 𝑓 [𝑥/𝑎] the syntactic replacement of every occurrence of 𝑥 in 𝑓 by 𝑎. Given a syntactic
expectation of the form 𝑓 (. . . , 𝑥𝑖 , . . .), we often write 𝑓 (. . . , 𝑎, . . .) instead of the more cumbersome
𝑓 (. . . , 𝑥𝑖 , . . .) [𝑥𝑖 /𝑎].

4.4 Semantics of Expressions and Expectations
The semantics of arithmetic and Boolean expressions is standard—see Table 2. For a program state 𝜎,
we define
                                                 (
                                                  𝑟,       if 𝑦 = 𝑥
                             𝜎 [𝑥 ↦→ 𝑟 ] ≜ 𝜆𝑦 .
                                                  𝜎 (𝑦), otherwise.
The semantics 𝜎 J𝑓 K of an expectation 𝑓 under state 𝜎 is an extended positive real (i.e., a positive
real number or ∞) defined inductively as follows:
                                                      𝜎            𝜎
                                                          J𝑎K ≜     J𝑎K 6
                                                                   (
                                                                     𝜎
                       𝜎                       𝜎                       J𝑓 K ,   if 𝜎 J𝜑K = true
                           J[𝜑] · 𝑓 K      ≜       J𝑓 · [𝜑]K ≜
                                                                     0,         else

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                              11

                                                    𝜎                𝜎
                                                        J𝑓 + 𝑔K ≜        J𝑓 K + 𝜎 J𝑔K
                             𝜎                      𝜎                𝜎
                                 J𝑎 · 𝑓 K   ≜           J𝑓 · 𝑎K ≜        J𝑎K · 𝜎 J𝑓 K
                                                                             n                               o
                                                𝜎                                𝜎 [𝑥↦→𝑟 ]
                                                    JS𝑥 : 𝑓 K ≜ sup                          J𝑓 K 𝑟 ∈ Q ≥0
                                                                            n                                o
                                                𝜎 J                              𝜎 [𝑥↦→𝑟 ]
                                                    J 𝑥 : 𝑓 K ≜ inf                          J𝑓 K 𝑟 ∈ Q ≥0
We assume that 0 · ∞ = ∞ · 0 = 0. Most of the above are self-explanatory. The most involved
definitions are the ones for quantifiers. The interpretation of the S𝑥 : 𝑓 quantification interprets 𝑓
under all possible values of the bounded variable 𝑥 and then returns the supremum of all these
values. Analogously, J 𝑥 : 𝑓 returns the infimum. Notice that—even though all variables evaluate to
rationals—both the supremum and the infimum are taken over a set of reals. Hence, an expectation
𝑓 involving S or J possibly evaluates to an irrational number. For example, the expectation
                                                𝑓 = S𝑥 : [𝑥 · 𝑥 < 2] · 𝑥 ,
               √
evaluates to 2 ∉ Q ≥0 under every state 𝜎.
  The supremum of ∅ is 0. Dually, the infimum of ∅ is ∞. The supremum of an unbounded set is ∞.
We also note that our semantics can generate ∞ only by using a S quantifier.
  As a shorthand for turning syntactic expectations into semantic ones, we define
                                                        J𝑓 K ≜ 𝜆𝜎 . 𝜎 J𝑓 K .

4.5    Equivalence and Ordering of Expectations
For two expectations 𝑓 and 𝑔, we write 𝑓 = 𝑔 only if they are syntactically equal. On the other hand,
we say that two expectations 𝑓 and 𝑔 are semantically equivalent, denoted 𝑓 ≡ 𝑔, if their semantics
under every state is equal, i.e.,
                                            𝑓 ≡ 𝑔             iff       J𝑓 K = J𝑔K .
Similarly to the partial order ⪯ on semantical expectations in E, we define a (semantical) partial
order ⪯ on syntactic expectations in Exp by
                                            𝑓 ⪯ 𝑔             iff       J𝑓 K ⪯ J𝑔K .

4.6    A Note on Forbidding 𝒇 · 𝒈 in our Syntax
Analogously to classical logic, a syntactic expectation 𝑓 is in prenex normal form, if it is of the form
                                                    𝑓 = Q 1𝑥 1 . . . Q 𝑘 𝑥𝑘 : 𝑔 ,
where Q 𝑖 ∈ {S, J } and where 𝑔 is quantifier-free. Being able to transform any syntactic expectation
into prenex normal form while preserving its semantics will be essential to our expressiveness proof.
In particular, we require that there is an algorithm that brings arbitrary syntactic expectations into
prenex normal form, without inspecting their semantics.
   The problem with allowing 𝑓 · 𝑔 arises in the context of the 0 · ∞ = 0 phenomenon. Suppose for
the moment that we allow for 𝑓 · 𝑔 syntactically and define
                                                𝜎                   𝜎
                                                    J𝑓 · 𝑔K     ≜       J𝑓 K · 𝜎 J𝑔K
semantically, where 0 · ∞ = ∞ · 0 = 0. Because of commutativity of multiplication, the above is an
absolutely natural definition. This also immediately gives us that 𝜎 J𝑓 · 𝑔K = 𝜎 J𝑔 · 𝑓 K .
6 Here, on the left-hand-side 𝜎 J · K denotes the semantics of expectations, whereas on the right-hand-side 𝜎 J · K denotes

the semantics of arithmetic expressions.


                                      Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
12                                                                                 Batz, Kaminski, Katoen, and Matheja


  We now show that we encounter a problem when trying to transform expectations into prenex
normal form. For that, consider the two expectations
                                               1
                                  𝑓 = J 𝑥:                and          𝑔 = S𝑦 : 𝑦 .
                                             𝑥 +1
Notice that we slightly abuse notation since, strictly speaking, 𝑥+11 is not allowed by our syntax.
We can however express it as S𝑧 : [𝑧 · (𝑥 + 1) = 1] · 𝑧. Clearly, we have 𝜎 J𝑓 K = 0 and 𝜎 J𝑔K = ∞
for all 𝜎, i.e., both 𝑓 and 𝑔 are constant expectations.
   Let us now consider the product of 𝑓 and 𝑔. For all 𝜎, its semantics is given by
            𝜎               𝜎
                J𝑓 · 𝑔K =       J𝑓 K · 𝜎 J𝑔K = 0 · ∞ = 0 = ∞ · 0 =          𝜎
                                                                                J𝑔K · 𝜎 J𝑓 K =   𝜎
                                                                                                     J𝑔 · 𝑓 K .
Now consider the following:
                  𝜎 s                        {
                              1
                       J 𝑥:
     𝜎                                       
       J𝑓 · 𝑔K =                    · S𝑦 : 𝑦
                            𝑥 +1
                  𝜎s                       {
                                  1
               =     J 𝑥 : S𝑦 :         ·𝑦                                                              (by prenexing)
                                𝑥 +1
                                                        
                                1
               = inf sup             · 𝑠 𝑠 ∈ Q ≥0 𝑟 ∈ Q ≥0
                              𝑟 +1
               = inf { ∞ | 𝑟 ∈ Q ≥0 }
                    = ∞
                    ≠ 0
                    = sup { 0 | 𝑠 ∈ Q ≥0 }
                                                                 
                                        1
                    = sup inf                · 𝑠 𝑟 ∈ Q ≥0 𝑠 ∈ Q ≥0
                                      𝑟 +1
                                                                 
                                            1
                    = sup inf 𝑠 ·                 𝑟 ∈ Q ≥0 𝑠 ∈ Q ≥0                (by commutativity of · in R∞
                                                                                                              ≥0 )
                                          𝑟 +1
                      𝜎 s                          {
                                               1
                    =            J
                          S𝑦 : 𝑥 : 𝑦 ·
                                            𝑥 +1
                      𝜎 s                            {
                                                  1
                                          J
                                    
                    =      S𝑦 : 𝑦 · 𝑥 :                                                          (by un-prenexing)
                                                𝑥 +1
                    = 𝜎 J𝑔 · 𝑓 K

We see that S𝑦 : J 𝑥 : 𝑥+11 · 𝑦 is a sound prenex normal form of 𝑔 · 𝑓 whereas J 𝑥 : S𝑦 : 𝑥+11 · 𝑦
apparently is not a sound prenex normal form of 𝑓 · 𝑔. A fact that seems even more off-putting is
that—even though 𝑓 ≡ 0—the above argument would not have worked for 𝑓 = 0.
  To summarize, we deem the above considerations enough grounds to forbid 𝑓 · 𝑔 altogether, in
particular since the rescaling 𝑎 · 𝑓 suffices in order for our syntactic expectations to be expressive.
We also note that we will later provide a syntactic, but much more complicated, way to write down
arbitrary products between syntactic expectations, see Theorem 9.4.

5    EXPRESSIVENESS FOR LOOP-FREE PROGRAMS
Before we deal with loops, we now show that our set Exp of syntactic expectations is expressive for
all loop-free pGCL programs. Proving expressiveness for loops is way more involved and will be
addressed separately in the remaining sections.

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                           13


  Lemma 5.1. Exp is expressive (see Definition 3.1) for all loop-free pGCL programs 𝐶, i.e., for all
𝑓 ∈ Exp there exists a syntactic expectation 𝑔 ∈ Exp, such that
                                                   wpJ𝐶K (J𝑓 K) = J𝑔K .
For proving this expressiveness lemma (and also for the case of loops), we need the following
technical lemma about substitution of variables by values in our semantics:
   Lemma 5.2. For all 𝜎, 𝑓 , and 𝑎,
           𝜎                   𝜎 [𝑥↦→ 𝜎 J𝑎 K ]
               J𝑓 [𝑥/𝑎]K =                       J𝑓 K   or equivalently        J𝑓 [𝑥/𝑎]K = J𝑓 K [𝑥/𝑎]
   Proof. By induction on the structure of 𝑓 .                                                                        □
Intuitively, Lemma 5.2 states that syntactically replacing variable 𝑥 by an arithmetical expression 𝑎
in expectation 𝑓 amounts to interpreting 𝑓 in states where the variable 𝑥 has been substituted by
the evaluation of 𝑎 under that state.
   Proof of Lemma 5.1. Let 𝑓 ∈ Exp be arbitrary. The proof goes by induction on the structure
of loop-free programs 𝐶. It is somewhat standard, but it demonstrates nicely that our syntactic
constructs are actually needed, so we provide it here. We start with the atomic programs:
   The effectless program skip. We have wpJskipK (J𝑓 K) = J𝑓 K and 𝑓 ∈ Exp by assumption.
   The assignment 𝑥 := 𝑎. We have
                                           wpJ𝑥 := 𝑎K (J𝑓 K) = J𝑓 K [𝑥/𝑎]
                                                                = J𝑓 [𝑥/𝑎]K                          (by Lemma 5.2)
and 𝑓 [𝑥/𝑎] ∈ Exp since 𝑓 [𝑥/𝑎] is obtained from 𝑓 by a syntactical replacement.
  Induction Hypothesis. For arbitrary loop-free 𝐶 1 and 𝐶 2 , there exist syntactic expectations 𝑔1, 𝑔2 ∈
Exp, such that
                      wpJ𝐶 1 K (J𝑓 K) = J𝑔1 K             and      wpJ𝐶 2 K (J𝑓 K) = J𝑔2 K .
We then proceed with the compound loop-free programs:
   The probabilistic choice { 𝐶 1 } [ 𝑝 ] { 𝐶 2 }. We have
                   wpJ{ 𝐶 1 } [ 𝑝 ] { 𝐶 2 }K (J𝑓 K)
                    = 𝑝 · wpJ𝐶 1 K (J𝑓 K) + (1 − 𝑝) · wpJ𝐶 2 K (J𝑓 K)                         (by definition of wp)
                    = 𝑝 · J𝑔1 K + (1 − 𝑝) · J𝑔2 K                                           (by I.H. on 𝐶 1 and 𝐶 2 )
                    = J𝑝 · 𝑔1 + (1 − 𝑝) · 𝑔2 K                         (pointwise addition and multiplication)
and 𝑝 · 𝑔1 + (1 − 𝑝) · 𝑔2 ∈ Exp, see Section 4.3.
   The conditional choice if ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }. We have
                   wpJif ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }K (J𝑓 K)
                    = [𝜑] · wpJ𝐶 1 K (J𝑓 K) + [¬𝜑] · wpJ𝐶 2 K (J𝑓 K)                          (by definition of wp)
                    = [𝜑] · J𝑔1 K + [¬𝜑] · J𝑔2 K                                            (by I.H. on 𝐶 1 and 𝐶 2 )
                    = J[𝜑] · 𝑔1 + [¬𝜑] · 𝑔2 K                          (pointwise addition and multiplication)
and [𝜑] · 𝑔1 + [¬𝜑] · 𝑔2 ∈ Exp, see Section 4.3.
   Hence, Exp is expressive for loop-free programs.                                                                   □

                                   Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
14                                                                                Batz, Kaminski, Katoen, and Matheja


6     EXPRESSIVENESS FOR LOOPY PROGRAMS — OVERVIEW
Before we get to the proof itself, we outline the main challenges—and the steps we took to address
them—of proving expressiveness of our syntactic expectations Exp for pGCL programs including
loops; the technical details of the involved encodings and auxiliary results are considered throughout
Sections 7 – 10. This section is intended to support navigation through the individual components
of the expressiveness proof; as such, we provide various references to follow-up sections.

6.1    Setup
As in the loop-free case considered in Section 5, we prove expressiveness of Exp for all pGCL
programs (including loopy ones) by induction on the program structure; all cases except loops are
completely analogous to the proof of Lemma 5.1. Our remaining proof obligation thus boils down
to proving that, for every loop 𝐶 = while ( 𝜑 ) { 𝐶 ′ },
                     ∀ 𝑓 ∈ Exp ∃ 𝑔 ∈ Exp :         wpJ while ( 𝜑 ) { 𝐶 ′ }K (J𝑓 K) = J𝑔K ,                       (†)
where we already know by the I.H. that the same property holds for the loop body 𝐶 ′, i.e.,
                            ∀ 𝑓 ′ ∈ Exp ∃ 𝑔 ′ ∈ Exp :       wpJ𝐶 ′K (J𝑓 ′K) = J𝑔 ′K .                            (1)
   Remark (A Simplification for this Overview). Just for this overview section, we assume that the set
Vars of all variables is finite instead of countable. This is a convenient simplification to avoid a few
purely technical details such that we can focus on the actual ideas of the proof. We do not make this
assumption in follow-up sections. Rather, our construction will ensure that only the finite set of
“relevant” variables—those that appear in the program or the postcondition under consideration—is
taken into account.                                                                                    △

6.2    Basic Idea: Exploiting the Kozen Duality
We first move to an alternative characterization of the weakest preexpectation of loops whose
components are simpler to capture with syntactic expectations. In particular, we will be able to
apply our induction hypothesis (1) to some of these components.
  Recall the Kozen duality between forward moving measure transformers and backward moving
expectation transformers (see Theorem 2.1 and Figure 1 in Section 2):
                                                 ∑︁
                             wpJ𝐶K (𝑋 ) = 𝜆𝜎0 .      𝑋 (𝜏) · 𝜇𝐶𝜎0 (𝜏) ,
                                                             𝜏 ∈Σ

where 𝜇𝐶𝜎0 is the probability distribution over final states obtained by running 𝐶 on initial state 𝜎0 .
Adapting the above equality to our concrete case in which 𝐶 is a loop and 𝑋 = J𝑓 K, we obtain
                                                  ∑︁
          wpJ while ( 𝜑 ) { 𝐶 ′ }K (J𝑓 K) = 𝜆𝜎0 .                       𝜎0
                                                     J[¬𝜑] · 𝑓 K (𝜏) · 𝜇while( 𝜑 ) { 𝐶′ }
                                                                                          (𝜏) ,
                                                            𝜏 ∈Σ

where we strengthened the postexpectation 𝑓 to [¬𝜑] · 𝑓 to account for the fact that the loop guard
𝜑 is violated in every final state, see [Kaminski 2019, Corollary 4.6, p. 85]. The main idea is—instead
                                        𝜎0
of viewing the whole distribution 𝜇while(   𝜑 ) { 𝐶′ }
                                                       in a single “big step”—to take a more operational
“small-step” view: we consider the intermediate states reached after each guarded loop iteration,
which corresponds to executing the program
                                    𝐶 iter = if ( 𝜑 ) { 𝐶 ′ } else { skip } .
We then sum over all terminating execution paths—finite sequences of states 𝜎0, . . . 𝜎𝑘−1 with initial
state 𝜎0 and final state 𝜎𝑘−1 = 𝜏—instead of a single final state 𝜏. The probability of an execution

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                               15


path is then given by the product of the probability 𝜇𝐶𝜎𝑖iter (𝜎𝑖+1 ) of each intermediate step, i.e., the
probability of reaching the state 𝜎𝑖+1 from the previous state 𝜎𝑖 :

                                                                    ∑︁                                  𝑘−2
                                                                                                        Ö
      wpJ while ( 𝜑 ) { 𝐶 ′ }K (J𝑓 K) = 𝜆𝜎0 . sup                               J[¬𝜑] · 𝑓 K (𝜎𝑘−1 ) ·           𝜇𝐶𝜎𝑖iter (𝜎𝑖+1 ) .   (2)
                                                        𝑘 ∈N 𝜎 ,...,𝜎
                                                                0      𝑘−1 ∈Σ                           𝑖=0

Notice that the above sum (without the sup) considers all execution paths of a fixed length 𝑘; we
take the supremum over all natural numbers 𝑘 to account for all terminating execution paths.
   Next, we aim to apply the induction hypothesis (1) to the probability 𝜇𝐶𝜎𝑖iter (𝜎𝑖+1 ) of each step such
that we can write it as a syntactic expectation. To this end, we need to characterize 𝜇𝐶𝜎𝑖iter (𝜎𝑖+1 ) in
terms of weakest preexpectations. We employ a syntactic expectation [𝜎] —called the characteristic
assertion [Winskel 1993] of state 𝜎—that captures the values assigned to variables by state 𝜎:7
                                             "                #
                                               Û
                                     [𝜎] =          𝑥 = 𝜎 (𝑥) .
                                                          𝑥 ∈Vars

By Kozen duality (Theorem 2.1), the probability of reaching state 𝜎𝑖+1 from 𝜎𝑖 in one guarded loop
iteration 𝐶 iter is then given by

                                     𝜇𝐶𝜎𝑖iter (𝜎𝑖+1 ) = wpJ𝐶 iter K (J[𝜎𝑖+1 ] K) (𝜎𝑖 ) .

By the same reasoning as for conditional choices in Lemma 5.1 and the induction hypothesis (1),
there exists a syntactic expectation 𝑔𝐶𝜎𝑖+iter1 ∈ Exp such that
                                                                         r         z
                     𝜇𝐶𝜎𝑖iter (𝜎𝑖+1 ) = wpJ𝐶 iter K (J[𝜎𝑖+1 ] K) (𝜎𝑖 ) = 𝑔𝐶𝜎𝑖+iter1 (𝜎𝑖 ) .

Plugging the above equality into our “small-step” characterization of loops (2) then yields the
following characterization of J𝑔K in (†):

                                                                  ∑︁         r           z          𝑘−2 r
                                                                                                    Ö               z
  wpJ while ( 𝜑 ) { 𝐶 ′ }K (J𝑓 K) = 𝜆𝜎0 . sup                                    [¬𝜑] · 𝑓 (𝜎𝑘−1 ) ·       𝑔𝐶𝜎𝑖+iter1 (𝜎𝑖 )
                                                    𝑘 ∈N 𝜎 ,...,𝜎
                                                                    𝑘−1 ∈Σ                          𝑖=0
                                                            0
                                                                                 | {z }                   |{z}
                                                                                   ∈Exp                               ∈Exp
                                                                                                            |          {z            }
                                                                                                 non-constant product expressible in Exp?
                                                                             |                         {z                            }
                                                                                      simple product expressible in Exp?
                                                          |                                   {z                                     }
                                                                non-constant sum over paths of length 𝑘 expressible in Exp?
                                                    |                                      {z                                        }
                                                                                      S 𝑘 : ... ∈Exp
                                                                                                                                     (3)

A formal proof of the above characterization is provided alongside Theorem 10.1.

6.3    Encoding Loops as Syntactic Expectations
Let us now revisit the individual components of the expectation (3) above and discuss how to
encode them as syntactic expectations in Exp, moving through the braces from bottom to top:

7 Recall from our remark on simplification that Vars is finite.



                                    Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
16                                                                                Batz, Kaminski, Katoen, and Matheja


6.3.1 The supremum sup𝑘 ∈N . The supremum ensures that terminating execution paths of arbitrary
length are accounted for; it is supported in Exp by the S quantifier. If we already know a syntactic
expectation 𝑔sum (𝑘) ∈ Exp for the entire sum that follows, we hence obtain an encoding of the
whole expectation, namely
                                            S𝑘 : 𝑔sum (𝑘, . . .) ∈ Exp .
                                     Í
6.3.2 The non-constant sum 𝜎0,...,𝜎𝑘−1 ∈Σ . This sum cannot directly be written as a syntactic
expectation: First, it sums over execution paths whereas all variables and constants in syntactic
expectations are evaluated to rational numbers. Second, its number of summands depends on the
length 𝑘 of execution paths whereas Exp only supports sums with a constant number of summands.
   To deal with the first issue, there is a standard solution in proofs of expressiveness (cf. [Loeckx
and Sieber 1987; Tatsuta et al. 2009, 2019; Winskel 1993]): We employ Gödelization to encode both
program states and finite sequences of program states as natural numbers in syntactic expectations.
The details are found in Section 7. In particular:
      • We show that Exp subsumes first-order arithmetic over the natural numbers.
      • We adapt the approach of Gödel [1931] to encode sequences of both natural numbers and
        non-negative rationals as Gödel numbers in our language Exp.
      • We define a predicate (in Exp) StateSequence (𝑢, 𝑣) that is satisfied iff 𝑢 is the Gödel number
        of a sequence of states of length 𝑣 − 1.
To deal with the second issue (the sum having a variable number of summands), we also rely on the
ability to encode sequences as Gödel numbers in Exp—the details are found in Section 9. Roughly
speaking, we encode the sum as follows:
      • We define a syntactic expectation ℎ(𝑣 sum, . . .) that serves as a map from 𝑣 sum to individual
        summands, i.e., ℎ [𝑣 sum /𝑖] yields the 𝑖-th summand.
      • We construct a syntactic expectation Sum [𝑣 sum, ℎ, 𝑣] for partial sums, summing up the first
        𝑣 summands defined by the syntactic expectation ℎ—see Theorem 9.2 for details.
6.3.3 The product J[¬𝜑] · 𝑓 K · . . .. This product is not directly expressible in Exp as arbitrary
products between syntactic expectations are not allowed. They are, however, expressible in our
language. We define a product operation ℎ 1 ⊙ ℎ 2 and prove its correctness in Corollary 9.5.
                                 Î 2 r 𝜎𝑖+1 z
6.3.4 The non-constant product 𝑘−   𝑖=0 𝑔𝐶 iter (𝜎𝑖 ). This product consists of 𝑘 − 1 factors; its encod-
ing requires
          a similar approach as for non-constant sums. That is, we define a syntactic expectation
Product 𝑣 prod, ℎ, 𝑣 that multiplies the first 𝑣 factors defined by the syntactic expectation ℎ(𝑣 prod ).
Details are provided in Theorem 9.4.
                                         r       z
6.3.5 The expectations J[¬𝜑] · 𝑓 K and 𝑔𝐶𝜎𝑖+iter1 . Both are syntactic expectations by construction.

6.4    The Expressiveness Proof
It remains to glue together the constructions for the individual components of the expectation (3),
which characterizes the weakest preexpectation of loops. We present the full construction, a proof
of its correctness, and an example of the resulting syntactic expectation in Section 10.

7     GÖDELIZATION FOR SYNTACTIC EXPECTATIONS
We embed the (standard model of) first-order arithmetic over both the rational and the natural num-
bers in our language Exp—thereby addressing the first issue raised in Section 6.3.1. Consequently,
Exp conservatively extends the standard assertion language of Floyd-Hoare logic (cf. [Cook 1978;

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                              17


            𝑃               𝑃 Q≥0
                                                                                          𝑃          [𝑃]
            𝜑              𝜑 ∧ 𝑁 (𝑥 1 ) ∧ . . . ∧ 𝑁 (𝑥𝑛 )
                                                                                          𝜑          [𝜑]
            ∃𝑥 : 𝑃 ′        ∃𝑥 : 𝑃Q′ ≥0
                                                                                          ∃𝑣 : 𝑃 ′   S𝑣 : [𝑃 ′]
            ∀𝑥 : 𝑃 ′       ∀𝑥 : 𝑁 (𝑥) −→ 𝑃 Q′ ≥0
                                                                                          ∀𝑣 : 𝑃 ′   J 𝑣 : [𝑃 ′]

   Fig. 3. Rules defining the formula formula 𝑃Q≥0 ∈
                                                                            Fig. 4. Rules for transforming a formula
   AQ≥0 for a Boolean expression 𝜑 and FV (𝑃) =
                                                                            𝑃 ∈ AQ≥0 into an expectation [𝑃] ∈ Exp.
   {𝑥 1, . . . , 𝑥𝑛 }.

Loeckx et al. 1984; Winskel 1993]), enabling us to encode finite sequences of both rationals and
naturals in Exp by means of Gödelization [Gödel 1931].
   Recall from Table 1 that we use, e.g., metavariables 𝜑, 𝜓 for Boolean expressions, 𝜎 for program
states, and so on and we will omit providing the types in order to unclutter the presentation.

7.1    Embedding First-Order Arithmetic in Exp
We denote by AQ≥0 the set of formulas 𝑃 in first-order arithmetic over Q ≥0 , i.e., the extension of
Boolean expressions 𝜑 (see Section 4.2) by an existential quantifier ∃𝑥 : 𝑃 and a universal quantifier
∀𝑥 : 𝑃 with the usual semantics, e.g., 𝜎 J∀𝑥 : 𝑃K = true iff for all 𝑟 ∈ Q ≥0 , 𝜎 [𝑥↦→𝑟 ] J𝑃K = true. The set
AN of formulas 𝑃 in first-order arithmetic over N is defined analogously by restricting ourselves to
(1) states8 𝜎 : Vars → N and (2) constants in N rather than Q ≥0 .
   For simplicity, we assume without loss of generality that all formulas 𝑃 are in prenex normalform, i.e.,
𝑃 is a Boolean expression comprising of a block of quantifiers followed by a quantifier-free formula.
Recall that program states originally evaluate variables to rationals. Since our expressiveness proof
requires encoding sequences of naturals, it is crucial that we can assert that a variable evaluates to
a natural. To this end, we adapt a result by Robinson [1949]:
   Lemma 7.1. N is definable in AQ≥0 , i.e. there exists a formula 𝑁 (𝑥) ∈ AQ≥0 , such that for all 𝜎,
                                      𝜎
                                          J𝑁 (𝑥)K = true           iff       𝜎 (𝑥) ∈ N .
We use the above assertion 𝑁 to first embed AN in AQ≥0 . Thereafter, we embed AQ≥0 in Exp.
Embedding a formula 𝑃 ∈ AN in AQ≥0 amounts to (1) asserting 𝑁 (𝑥) for every 𝑥 ∈ FV (𝑃) and (2)
guarding every quantified variable 𝑥 in 𝑃 with 𝑁 (𝑥), i.e., whenever we attempt to evaluate the
embedding-formula for non-naturals, we default to false—see Figure 3 for a formal definition.
   Theorem 7.2. Let 𝑃Q≥0 ∈ AN be the embedding of 𝑃 ∈ AN as defined in Figure 3. Then, for all 𝜎,
                                  (
                     𝜎
                                     𝜎
                                       J𝑃K , if 𝜎 (𝑥) ∈ N for all 𝑥 ∈ FV (𝑃) ,
                       J𝑃 Q≥0 K =
                                    false, otherwise .
Embedding a formula 𝑃 ∈ AQ≥0 into Exp amounts to (1) taking its Iverson bracket for every Boolean
expression and (2) substituting the quantifiers ∃/∀ by their quantitative analogs S/J , see Figure 4.
   Theorem 7.3. Let [𝑃] ∈ Exp be the embedding of 𝑃 ∈ AQ≥0 as defined in Figure 4. Then, for all 𝜎,
                                          (
                               𝜎            1, if 𝜎 J𝑃K = true
                                 J[𝑃]K =
                                            0, if 𝜎 J𝑃K = false .
Given 𝑃 (𝑣 1, . . . , 𝑣𝑛 ) ∈ AQ≥0 , we often write [𝑃 (𝑣 1, . . . , 𝑣𝑛 )] instead of [𝑃] (𝑣 1, . . . , 𝑣𝑛 ).
8 Program states serve here the role of interpretations in classical first-order logic.



                                      Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
18                                                                                    Batz, Kaminski, Katoen, and Matheja


7.2     Encoding Sequences of Natural Numbers
The embedding of AN in our language Exp of syntactic expectations gives us access to a classical
result by Gödel [1931] for encoding finite sequences of naturals in a single natural.
  Lemma 7.4 (Gödel [1931]). There is a formula Elem (𝑣 1, 𝑣 2, 𝑣 3 ) ∈ AN (with quantifiers) satisfying:
For every finite sequence of natural numbers 𝑛 0, . . . , 𝑛𝑘−1 , there is a (Gödel) number 𝑛𝑢𝑚 ∈ N that
encodes it, i.e., for all 𝑖 ∈ {0, . . . , 𝑘 − 1} and all 𝑚 ∈ N, it holds that
                              Elem (𝑛𝑢𝑚, 𝑖, 𝑚) ≡ true               iff          𝑚 = 𝑛𝑖 .
By Theorem 7.3, we also have an expectation [Elem (𝑣 1, 𝑣 2, 𝑣 3 )] expressing Elem in Exp.
     Example 7.5 (Factorials via Gödel). The syntactic expectation below evaluates to the factorial 𝑥!:
      Fac (𝑥) = S𝑣 : S𝑛𝑢𝑚 : 𝑣 · Elem (𝑛𝑢𝑚, 0, 1) ∧ Elem (𝑛𝑢𝑚, 𝑥, 𝑣)
                                   

                     ∧ ∀𝑢 : ∀𝑤 : 𝑢 < 𝑥 ∧ Elem (𝑛𝑢𝑚, 𝑢, 𝑤) −→ Elem (𝑛𝑢𝑚, 𝑢 + 1, 𝑤 · (𝑢 + 1)) .
                                                                                              

For every state 𝜎, the quantifier S𝑛𝑢𝑚 selects a sequence 𝑛 0, 𝑛 1 . . . satisfying 𝑛𝜎 (𝑥) = 𝜎 (𝑥)!. The
quantifier S𝑣 then binds 𝑣 to the value 𝑛𝜎 (𝑥) = 𝜎 (𝑥)!. Finally, by multiplying the {0, 1}-valued
expectation specifying the sequence by 𝑣, we get that 𝜎 JFac (𝑥)K = 𝜎 (𝑥)!.                            △
To assign a unique Gödel number 𝑛𝑢𝑚 to a sequence 𝑛 0, . . . , 𝑛𝑘−1 of length 𝑘 we employ minimal-
ization, i.e., we take the least suitable Gödel number. Formally, we define the formula
            Sequence (𝑛𝑢𝑚, 𝑣)
              ≜    (∀𝑢 : 𝑢 < 𝑣 −→ ∃𝑤 : Elem (𝑛𝑢𝑚, 𝑢, 𝑤))
                     ∧ ∀𝑛𝑢𝑚 ′ : ∀𝑢 : 𝑢 < 𝑣 −→ ∃𝑤 : Elem (𝑛𝑢𝑚, 𝑢, 𝑤) ∧ Elem (𝑛𝑢𝑚 ′, 𝑢, 𝑤)
                                                                                                             

                         −→ 𝑛𝑢𝑚 ′ ≥ 𝑛𝑢𝑚 .
                                          

For every 𝑘 and every sequence 𝑛 0, . . . , 𝑛𝑘−1 of length 𝑘, we then define the Gödel number encoding
the sequence 𝑛 0, . . . , 𝑛𝑘−1 as the unique natural number ⟨𝑛 0, . . . , 𝑛𝑘−1 ⟩ satisfying
                                                            Û1
                                                            𝑘−
                    Sequence (⟨𝑛 0, . . . , 𝑛𝑘−1 ⟩, 𝑘) ∧           Elem (⟨𝑛 0, . . . , 𝑛𝑘−1 ⟩, 𝑖, 𝑛𝑖 ) .
                                                             𝑖=0

7.3     Encoding Sequences of Non-negative Rationals
Recall that program states in pGCL map variables to values in Q ≥0 . To encode sequences of program
states, we thus first lift Gödel’s encoding Elem (𝑛𝑢𝑚, 𝑖, 𝑛) to uniquely encode sequences over Q ≥0 .
The main idea is to represent such a sequence by pairing two sequences over N.
  Lemma 7.6 (Pairing Functions [Cantor 1878]). There is a formula Pair(𝑣 1, 𝑣 2, 𝑣 3 ) ∈ AN satisfying:
For every pair of natural numbers (𝑛 1, 𝑛 2 ), there is exactly one natural number 𝑛 such that
                                             Pair(𝑛, 𝑛 1, 𝑛 2 ) ≡ true .
    Theorem 7.7. There is a formula RElem (𝑣 1, 𝑣 2, 𝑣 3 ) ∈ AQ≥0 satisfying: For every finite sequence
𝑟 0, . . . , 𝑟𝑘−1 ⊂ Q ≥0 there is a Gödel number 𝑛𝑢𝑚, such that for all 𝑖 ∈ {0, . . . , 𝑘 − 1} and 𝑠 ∈ Q ≥0 ,
                                   RElem (𝑛𝑢𝑚, 𝑖, 𝑠) ≡ true               iff 𝑠 = 𝑟𝑖 .
  Example 7.8 (Harmonic Numbers). For every 𝜎 with 𝜎 (𝑥) = 𝑘 ∈ N, the expectation Harmonic (𝑥) ∈
Exp below evaluates to the 𝑘-th harmonic number H (𝑘) = 𝑘𝑖=1 1𝑖 .
                                                            Í

      Harmonic (𝑥) = S𝑣 : S𝑛𝑢𝑚 : 𝑣 · RElem (𝑛𝑢𝑚, 0, 0) ∧ RElem (𝑛𝑢𝑚, 𝑥, 𝑣)
                                       

                                  ∧ ∀𝑢 : ∀𝑤 : (𝑢 < 𝑥 ∧ RElem (𝑛𝑢𝑚, 𝑢, 𝑤))

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                            19


                                        −→ ∃𝑤 ′ : 𝑤 ′ · (𝑢 + 1) = 1 ∧ RElem (𝑛𝑢𝑚, 𝑢 + 1, 𝑤 + 𝑤 ′)
                                                                                                                  

Notice that the above Iverson bracket evaluates to 1 on state 𝜎 iff 𝜎 (𝑛𝑢𝑚) encodes a sequence
𝑟 0, 𝑟 1, . . . , 𝑟 𝜎 (𝑥) such that 𝜎 (𝑣) = 𝑟 𝜎 (𝑥) and
                             1             1                            1
                               + 𝑟 0, 𝑟 2 = + 𝑟 1 , . . . , 𝑟 𝜎 (𝑥) =
                   𝑟0 = 0 , 𝑟1 =                                            + 𝑟 𝜎 (𝑥)−1 .
                             1             2                          𝜎 (𝑥)
By Theorem 7.2, we do not need to require that 𝜎 (𝑢) ∈ N as RElem (𝑛𝑢𝑚, 𝑖, 𝑤) is false if 𝜎 (𝑢) ∉ N.
△
Analogously to the previous section, we define a predicate RSequence (𝑛𝑢𝑚, 𝑣) that uses minimaliza-
tion to a unique Gödel number 𝑛𝑢𝑚 for every sequence 𝑟 0, . . . , 𝑟𝑘−1 of length 𝑘; the only difference
between RSequence (𝑛𝑢𝑚, 𝑣) and Sequence (𝑛𝑢𝑚, 𝑣) is that every occurrence of Elem (., ., .) is re-
placed by RElem (., ., .). Moreover, for every 𝑘 and every sequence 𝑟 0, . . . , 𝑟𝑘−1 , we define the Gödel
number encoding the sequence 𝑟 0, . . . , 𝑟𝑘−1 as the unique natural number ⟨𝑟 0, . . . , 𝑟𝑘−1 ⟩ satisfying
                                                               Û1
                                                               𝑘−
                    RSequence (⟨𝑟 0, . . . , 𝑟𝑘−1 ⟩, 𝑘) ∧             RElem (⟨𝑟 0, . . . , 𝑟𝑘−1 ⟩, 𝑖, 𝑟𝑖 ) .
                                                                𝑖=0

7.4 Encoding Sequences of Program States
To encode sequences of program states, we first fix a finite set x = {𝑥 0, . . . , 𝑥𝑘−1 } of relevant
variables. Intuitively, x consists of all variables that appear in a given program or a postexpectation.
We define an equivalence relation ∼x on states by
                                𝜎 1 ∼x 𝜎 2       iff         ∀𝑥 ∈ x : 𝜎1 (𝑥) = 𝜎2 (𝑥) .
  Every 𝑛𝑢𝑚 satisfying Sequence (𝑛𝑢𝑚, 𝑘) encodes exactly one state 𝜎 (modulo ∼x ). The Gödel
number encoding 𝜎 (w.r.t. x), which we denote by ⟨𝜎⟩x , is then the unique number satisfying
                                                             Û1
                                                             𝑘−
                            RSequence (⟨𝜎⟩x, 𝑘) ∧                   RElem (⟨𝜎⟩x, 𝑖, 𝜎 (𝑥𝑖 )) .
                                                              𝑖=0
Notice that we implictly fixed an ordering of the variables in x to identify each value stored in 𝜎
for a variable in x. The formula
                                                                 Û1
                                                                 𝑘−
             EncodesStatex (𝑛𝑢𝑚) ≜ RSequence (𝑛𝑢𝑚, 𝑘) ∧              RElem (𝑛𝑢𝑚, 𝑖, 𝑥𝑖 )
                                                                                     𝑖=0
evaluates to true on state 𝜎 iff 𝜎 (𝑛𝑢𝑚) is the Gödel number of a state 𝜎 ′ with 𝜎 ∼x 𝜎 ′. Now, let
𝜎0, . . . , 𝜎𝑛−1 be a sequence of states of length 𝑛. The Gödel number encoding 𝜎0, . . . , 𝜎𝑛−1 (w.r.t. x),
which we denote by ⟨(𝜎0, . . . , 𝜎𝑛−1 )⟩x , is then the unique number satisfying
                                                             Û1
                                                             𝑛−
               Sequence (⟨(𝜎0, . . . , 𝜎𝑛−1 )⟩x, 𝑛) ∧               Elem (⟨(𝜎0, . . . , 𝜎𝑛−1 )⟩x, 𝑖, ⟨𝜎𝑖 ⟩x ) .
                                                              𝑖=0
We are now in a position to encode sequences of states. The formula
                     StateSequencex (𝑛𝑢𝑚, 𝑣)
                  = Sequence (𝑛𝑢𝑚, 𝑣) ∧ (∃𝑣 ′ : Elem (𝑛𝑢𝑚, 0, 𝑣 ′) ∧ EncodesStatex (𝑣 ′))
                      ∧ ∀𝑢 : ∀𝑣 ′ : ((𝑢 < 𝑣 ∧ Elem (𝑛𝑢𝑚, 𝑢, 𝑣 ′)) −→ RSequence (𝑣 ′, 𝑘))
evaluates to true on state 𝜎 iff (1) 𝑛𝑢𝑚 is the Gödel number of some sequence 𝜎0, . . . , 𝜎𝜎 (𝑣−1) ∈ Σ
of states of length 𝜎 (𝑣) and where (2) 𝜎 and 𝜎0 coincide on all variables in x, i.e., 𝜎 ∼x 𝜎0 . Notice
that, for every sequence 𝜎0, . . . , 𝜎𝑛−1 of states of length 𝑛, there is exactly one 𝑛𝑢𝑚 satisfying

                                  Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
20                                                                                Batz, Kaminski, Katoen, and Matheja


StateSequencex (𝑛𝑢𝑚, 𝑛). If clear from the context, we often omit the subscript x and simply write
⟨𝜎⟩ (resp. ⟨(𝜎0, . . . , 𝜎𝑛−1 )⟩) instead of ⟨𝜎⟩x (resp. ⟨(𝜎0, . . . , 𝜎𝑛−1 )⟩x ).

8     THE DEDEKIND NORMAL FORM
Before we encode sums and products of non-constant size in Exp—as required to deal with the
challenges in Sections 6.3.2 to 6.3.4—we introduce a normal form that gives a convenient handle to
encode real numbers as syntactic expectations.
   As a first step, we transform syntactic expectations into prenex normal form, i.e., we rewrite
every 𝑓 ∈ Exp into an equivalent syntactic expectation of the form Q 1𝑣 1 . . . Q 𝑘 𝑣𝑘 : 𝑓 ′, where
Q 𝑖 ∈ {S, J } and 𝑓 ′ is “quantifier”–free, i.e., contains neither S nor J . The following lemma
justifies that any expectation can indeed be transformed into an equivalent one in prenex normal
form by iteratively pulling out quantifiers. In case the quantified logical variable already appears in
the expectation the quantifier is pulled over, we rename it by a fresh one first.
  Lemma 8.1 (Prenex Transformation Rules). For all 𝑓 , 𝑓1 , 𝑓2 ∈ Exp, terms 𝑎, and Boolean
expressions 𝜑, quantifiers Q ∈ {S, J }, and fresh logical variables 𝑣 ′, the following equivalences hold:
  (1) ( Q𝑣 : 𝑓1 ) + 𝑓2 ≡ Q𝑣 ′ : 𝑓1 [𝑣/𝑣 ′] + 𝑓2 ,
  (2) 𝑓1 + ( Q𝑣 : 𝑓2 ) ≡ Q𝑣 ′ : 𝑓1 + 𝑓2 [𝑣/𝑣 ′],
  (3) 𝑎 · Q𝑣 : 𝑓       ≡ Q𝑣 ′ : 𝑎 · 𝑓 [𝑣/𝑣 ′] and ( Q𝑣 : 𝑓 ) · 𝑎 ≡ Q𝑣 ′ : (𝑓 [𝑣/𝑣 ′] · 𝑎),
  (4) [𝜑] · Q𝑣 : 𝑓 ≡ Q𝑣 ′ : [𝜑] · 𝑓 [𝑣/𝑣 ′] and ( Q𝑣 : 𝑓 ) · [𝜑] ≡ Q𝑣 ′ : (𝑓 [𝑣/𝑣 ′] · [𝜑]).
The Dedekind normal form is motivated by the notion of Dedekind cuts [Bertrand 1849]. We denote
by Cut (𝛼) the Dedekind cut of a real number, i.e., the set of all rationals strictly smaller than 𝛼. In
the realm of all reals, it is required that a Dedekind cut is neither the empty set nor the whole set
of rationals Q. However, since we operate in the realm of non-negative reals with infinity R∞    ≥0 , we
do allow for both empty cuts and Q ≥0 . More formally, we define:
                              ≥ 0 . The Dedekind cut Cut (𝛼) ⊆ Q ≥0 of 𝛼 is defined as
     Definition 8.2. Let 𝛼 ∈ R∞
                                      Cut (𝛼)      ≜ { 𝑟 ∈ Q ≥0 | 𝑟 < 𝛼 } .
Furthermore, we define Cut (𝛼) ≜ Cut (𝛼) ∪ {0}.
Dedekind cuts are relevant for our technical development as they allow to describe every real
number 𝛼 as a supremum over a set of rational numbers. In particular, the Dedekind cut Cut (0)
of 0 is the empty set with supremum 0, and the Dedekind cut Cut (∞) of ∞ is the set Q ≥0 with
supremum ∞. Formally:
                               ≥0 , we have 𝛼 = sup Cut (𝛼).
     Lemma 8.3. For every 𝛼 ∈ R∞
     Theorem 8.4. For every 𝑓 ∈ Exp, there is a syntactic expectation in prenex normal form
                                      Dedekind[𝑣 Cut, 𝑓 ] = Prefix : [𝜑] ,
where Prefix is the quantifier prefix, 𝜑 is an effectively constructible Boolean expression, and the free
variable 𝑣 Cut is fresh; we call Dedekind[𝑣 Cut, 𝑓 ] the Dedekind normal form of 𝑓 .
  Moreover, for all program states 𝜎, we have
                                                        (
                           𝜎                              1, if 𝜎 (𝑣 Cut ) < 𝜎 J𝑓 K
                             JDedekind[𝑣 Cut, 𝑓 ]K =
                                                          0, otherwise .
     The Dedekind normal form Dedekind[𝑣 Cut, 𝑓 ] defines the Dedekind cut of every 𝜎 J𝑓 K , i.e.,
          for all 𝜎 : Cut 𝜎 J𝑓 K = 𝑟 ∈ Q ≥0 𝑟 = 𝜎 (𝑣 Cut ), 𝜎 JDedekind[𝑣 Cut, 𝑓 ]K = 1 .
                                  

Hence, we can recover 𝑓 from Dedekind[𝑣 Cut, 𝑓 ]:

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                                  21


        Lemma 8.5. Let Dedekind[𝑣 Cut, 𝑓 ] be in Dedekind normal form. Then
                                                 𝑓 ≡ S𝑣 Cut : Dedekind[𝑣 Cut, 𝑓 ] · 𝑣 Cut .

9        SUMS, PRODUCTS, AND INFINITE SERIES OF SYNTACTIC EXPECTATIONS
This section deals with the syntactic Sum and Product expectations as described in Section 6.3.2.
Since a syntactic expectation 𝑓 evaluates to a non-negative extended real, we rely on a reduction
from sums over reals to suprema of sums over rationals:
        Lemma 9.1. For all 𝛼 0, . . . , 𝛼𝑛 ∈ R∞
                                              ≥ 0 , we have
                            𝑛
                                              (    𝑛
                                                                                              )
                          ∑︁                     ∑︁
                                𝛼 𝑗 = sup            𝑟 𝑗 ∀𝑖 ∈ {0, . . . , 𝑛} : 𝑟𝑖 ∈ Cut (𝛼𝑖 )
                                   𝑗=0                      𝑗=0

  Theorem 9.2. For every 𝑓 ∈ Exp with free variable 𝑣 sum , there is an effectively constructible
expectation Sum [𝑣 sum, 𝑓 , 𝑣] ∈ Exp such that for all states 𝜎 with 𝜎 (𝑣) ∈ N, we have
                                           (𝑣)
                                         𝜎∑︁                                                                         ∞
                                                                                                                    ∑︁
    𝜎
        JSum [𝑣 sum, 𝑓 , 𝑣]K =                   𝜎
                                                     J𝑓 [𝑣 sum /𝑗]K and 𝜎 JS𝑣 : Sum [𝑣 sum, 𝑓 , 𝑣]K =                     𝜎
                                                                                                                              J𝑓 [𝑣 sum /𝑗]K .
                                          𝑗=0                                                                       𝑗=0

   Proof. We sketch the construction of Sum [𝑣 sum, 𝑓 , 𝑣]. Lemma 9.1 and the Dedekind normal
form Dedekind[𝑣 Cut, 𝑓 ] of 𝑓 (cf. Theorem 8.4) give us
                         (𝑣)
                       𝜎∑︁
                               𝜎
                                   J𝑓 [𝑣 sum /𝑗]K
                        𝑗=0
                               ( 𝜎 (𝑣)                                                                          )
                                 ∑︁
                                          𝑟 𝑗 ∀𝑗 ∈ {0, . . . , 𝜎 (𝑣)} : 𝑟 𝑗 ∈ Cut      𝜎                    
                   = sup                                                                   J𝑓 [𝑣 sum /𝑗]K
                                    𝑗=0
                               ( 𝜎 (𝑣)                                                                                        )
                                 ∑︁
                                                                          𝜎
                   = sup                  𝑟 𝑗 ∀𝑗 ∈ {0, . . . , 𝜎 (𝑣)} :       JDedekind[𝑓 , 𝑟 𝑗 ]K = 1 or 𝑟 𝑗 = 0                 .        (4)
                                    𝑗=0

Writing Dedekind[𝑣 Cut, 𝑓 ] = Prefix : [𝜑] (cf. Theorem 8.4) and denoting by Prefix the quantifier
prefix obtained from Prefix by flipping all quantifiers, we then construct a syntactic expectation 𝑔
with free variables 𝑣 and 𝑛𝑢𝑚 by
                       S𝑣 ′ : 𝑣 ′ · J 𝑢 : J 𝑧 : S𝑣 Cut : Prefix :
                       [RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣)
                           ∧ (𝑢 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑢, 𝑧) ∧ ( [𝜑] 𝑣 prod 𝑢 ∨ 𝑣 Cut = 0))
                                                                          

                               −→ RElem (𝑛𝑢𝑚, 𝑢 + 1, 𝑧 + 𝑣 Cut ) ] .
                                                                

For every state 𝜎 where 𝜎 (𝑛𝑢𝑚) is a Gödel number encoding some sequence
                            1, 1 · 𝑟 1, 1 + 𝑟 1 + 𝑟 2, . . . , 1 + 𝑟 1 + . . . + 𝑟 𝜎 (𝑣)
with 𝑟 𝑗 ∈ Cut 𝜎 J𝑓 [𝑣 sum /𝑗]K for all 0 ≤ 𝑗 ≤ 𝜎 (𝑣), expectation 𝑔 evaluates to the last element
                               
of the above sequence, i.e., an element of the set from Equation (4). Hence, by Lemma 9.1, the
supremum over these sequences, i.e, all Gödel numbers, gives us
                                                        Sum [𝑣 sum, 𝑓 , 𝑣] = S𝑛𝑢𝑚 : 𝑔 .
See Appendix C.1 for a detailed proof.                                                                                                       □

                                                Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
22                                                                                          Batz, Kaminski, Katoen, and Matheja


For an arithmetic expression 𝑎, we write Sum [𝑣 sum, 𝑓 , 𝑎] instead of Sum [𝑣 sum, 𝑓 , 𝑣] [𝑣/𝑎].
   Example 9.3. Sum provides us with a much more convenient way to construct Harmonic (𝑥)
from Example 7.8. Let 𝑓 = 1/𝑣sum where 1/𝑣sum is a shorthand for S𝑤 : 𝑤 · [𝑤 · 𝑣 sum = 1]. Then, by
Theorem 9.2, we have for every 𝜎 ∈ Σ
                                                     (𝑥)
                                                   𝜎∑︁                                (𝑥)
                                                                                    𝜎∑︁
                  𝜎                                        𝜎                                1
                      JSum [𝑣 sum, 𝑓 , 𝑥]K =                   J𝑓 [𝑣 sum /𝑗]K =               = H (𝜎 (𝑥)) .
                                                   𝑗=0                                  𝑗=1
                                                                                            𝑗

     The construction of the syntactic Product expectation is completely analogous:
  Theorem 9.4. For every 𝑓 ∈ Exp with free variable 𝑣 prod , there is an effectively constructible
expectation Product 𝑣 prod, 𝑓 , 𝑣 ∈ Exp such that for every state 𝜎 with 𝜎 (𝑣) ∈ N, we have
                                                               (𝑣)
                                                              𝜎Ö
                                   Product 𝑣 prod, 𝑓 , 𝑣
                              𝜎q                        y        𝜎q        y
                                                            =        𝑓 𝑣 prod 𝑗   .
                                                                          𝑗=0

   For an arithmetic expression 𝑎, we write Product 𝑣 prod, 𝑓 , 𝑎 instead of Product 𝑣 prod, 𝑓 , 𝑣 [𝑣/𝑎].
                                                                                               

   An immediate, yet important, consequence of Theorem 9.4 is that, even though syntactically
forbidden, arbitrary products of syntactic expectations are expressible in Exp. Let 𝑓 , 𝑔 ∈ Exp, and
let 𝑣 prod be a fresh variable. We define the (unrestricted) product 𝑓 ⊙ 𝑔 of 𝑓 and 𝑔 by
                     𝑓 ⊙ 𝑔 ≜ Product 𝑣 prod, 𝑣 prod = 0 · 𝑓 + 𝑣 prod = 1 · 𝑔, 1 .
                                                                             

     Corollary 9.5. Let 𝑓 , 𝑔 ∈ Exp. For all states 𝜎, we have
                                             𝜎                     𝜎
                                                 J𝑓 ⊙ 𝑔K =             J𝑓 K · 𝜎 J𝑔K .

10 EXPRESSIVENESS OF OUR LANGUAGE
With the results from the preceding sections at hand, we give a constructive expressiveness proof
for our language Exp. Fix a set of variables x = {𝑥 0, . . . , 𝑥𝑛−1 }. We assume a fixed set Σx ⊆ Σ that
contains exactly one state from each equivalence class of ∼x (cf. Section 7.4). Given a state 𝜎 ∈ Σ,
we define the characteristic expectation [𝜎] x of 𝜎 (w.r.t. x) as
                               [𝜎] x     ≜   [𝑥 0 = 𝜎 (𝑥 0 ) ∧ . . . ∧ 𝑥𝑛−1 = 𝜎 (𝑥𝑛−1 )] .
The expectation [𝜎] x evaluates to 1 on state 𝜎 ′ if 𝜎 ∼x 𝜎 ′, and to 0 otherwise. Finally, we denote
by Vars(𝐶) the set of all variables that appear in the pGCL program 𝐶.
  Let us now formalize the characterization of wpJwhile ( 𝜑 ) { 𝐶 ′ }K (J𝑓 K) from Section 6.2:
   Theorem 10.1. Let 𝐶 = while ( 𝜑 ) { 𝐶 ′ } be a loop and let 𝑓 ∈ Exp. Furthermore, let x be a finite
set of variables with Vars(𝐶) ∪ FV (𝑓 ) ⊆ x. We have
             wpJwhile ( 𝜑 ) { 𝐶 ′ }K (J𝑓 K)
                        ∑︁
           = 𝜆𝜎 . sup              [𝜎0 ] x (𝜎) · ( [¬𝜑] · J𝑓 K) (𝜎𝑘−1 )
                   𝑘 ∈N 𝜎 ,...,𝜎
                          0    𝑘−1 ∈Σx

                                                  𝑘−2
                                                  Ö
                                              ·         wpJif ( 𝜑 ) { 𝐶 ′ } else { skip }K ( [𝜎𝑖+1 ] x ) (𝜎𝑖 ) .
                                                  𝑖=0

     Proof. See Appendix D.                                                                                                  □
     We are finally in a position to prove expressiveness (cf. Definition 3.1).
     Theorem 10.2. The language Exp of syntactic expectations is expressive.

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                             23


   Proof. By induction on the structure of 𝐶. All cases except loops are completely analogous
to the proof of Lemma 5.1. Let us thus consider the case 𝐶 = while ( 𝜑 ) { 𝐶 1 }. We employ the
syntactic Sum- and Product expectations from Theorems 9.2 and 9.4 to construct the series from
Theorem 10.1 in Exp, thus expressing wpJwhile ( 𝜑 ) { 𝐶 1 }K J𝑓 K .
   The products ocurring in Theorem 10.1 are expressed by an effectively constructible syntactic
expectation Path [𝑓 ] (𝑣 1, 𝑣 2 ) (where 𝑣 1 and 𝑣 2 are fresh variables) satisfying:
   (1) If 𝜎 (𝑣 1 ) ∈ N with 𝜎 (𝑣 1 ) > 0 and 𝜎 (𝑣 2 ) = ⟨(𝜎0, . . . , 𝜎𝜎 (𝑣1 )−1 )⟩x , then
              𝜎
                  JPath [𝑓 ] (𝑣 1, 𝑣 2 )K
                                             𝜎 (𝑣
                                                Ö 1 )−2

          = ( [¬𝜑] · J𝑓 K) (𝜎𝜎 (𝑣1 )−1 ) ·                wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] x ) (𝜎𝑖 )      (5)
                                                𝑖=0

   (2) If 𝜎 (𝑣 1 ) ∉ N or 𝜎 (𝑣 1 ) = 0, then 𝜎 JPath [𝑓 ] (𝑣 1, 𝑣 2 )K = 0.
Then, for the syntactic expectation
             ℎ = JS𝑙𝑒𝑛𝑔𝑡ℎ : S𝑛𝑢𝑚𝑠 : Sum 𝑣 sum, StateSequencex (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ)
                                                                            

                                                                    ⊙ Path [𝑓 ] (𝑙𝑒𝑛𝑔𝑡ℎ, 𝑣 sum ) , 𝑛𝑢𝑚𝑠 K ,
                                                                                                       

we have wpJwhile ( 𝜑 ) { 𝐶 1 }K J𝑓 K = JℎK.
                                     
   Here, the quantifier S𝑙𝑒𝑛𝑔𝑡ℎ in ℎ corresponds to the sup 𝑘 from Theorem 10.1. The subsequent
Sum expectation expresses the sum from Theorem 10.1: Summing over sequences of states of length
𝑙𝑒𝑛𝑔𝑡ℎ is realized by summing over all Gödel numbers 𝑛𝑢𝑚 satisfying StateSequence (𝑛𝑢𝑚, 𝑙𝑒𝑛𝑔𝑡ℎ).
See D.1 for a detailed correctness proof.                                                     □

10.1 Example
We conclude this section by sketching the construction of a syntactic expectation for a concrete
loop. Consider the program 𝐶 given by
                                            while ( 𝑐 = 1 ) {
                                               { 𝑐 := 0 } [ 1/2 ] { 𝑐 := 1 } ;
                                              𝑥 := 𝑥 + 1 }
where we denote the loop body by 𝐶 ′. Morever, let 𝑓 ≜ 𝑥 ∈ Exp. Then the syntactic expectation ℎ
expressing wpJwhile ( 𝑐 = 1 ) { 𝐶 ′ }K J𝑥K as sketched in the proof of Theorem 10.2 is
                                           

           ℎ = JS𝑙𝑒𝑛𝑔𝑡ℎ : S𝑛𝑢𝑚𝑠 : Sum 𝑣 sum, StateSequencex (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ)
                                                                                  

                                                    ⊙ Path [𝑓 ] (𝑙𝑒𝑛𝑔𝑡ℎ, 𝑣 sum ) , 𝑛𝑢𝑚𝑠 K ,
                                                                                       

where the syntactic expectation Path [𝑓 ] (𝑙𝑒𝑛𝑔𝑡ℎ, 𝑣 2 ) is defined as follows:
      [𝑙𝑒𝑛𝑔𝑡ℎ < 2] · ( S𝑛𝑢𝑚 : [Elem (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ − 1, 𝑛𝑢𝑚)] ⊙ Substx [([¬(𝑐 = 1)] · 𝑥), 𝑛𝑢𝑚])
    + [𝑙𝑒𝑛𝑔𝑡ℎ ≥ 2] · ( S𝑛𝑢𝑚 : [Elem (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ − 1, 𝑛𝑢𝑚)] ⊙ Substx [( [¬(𝑐 = 1)] · 𝑥), 𝑛𝑢𝑚])
         ⊙ Product S𝑛𝑢𝑚 1 : S𝑛𝑢𝑚 2 : Elem 𝑣 sum, 𝑣 prod, 𝑛𝑢𝑚 1 ∧ Elem 𝑣 sum, 𝑣 prod + 1, 𝑛𝑢𝑚 2
                                                                                             

             ⊙ Substx [Substx′ [𝑔, 𝑛𝑢𝑚 2 ] , 𝑛𝑢𝑚 1 ] , 𝑙𝑒𝑛𝑔𝑡ℎ − 2
                                                                  

and where
                     1
𝑔 = [𝑐 = 1] ·          · ( [0 = 𝑐 ′ ∧ 𝑥 + 1 = 𝑥 ′] + [1 = 𝑐 ′ ∧ 𝑥 + 1 = 𝑥 ′]) + [¬(𝑐 = 1)] · [𝑐 = 𝑐 ′ ∧ 𝑥 = 𝑥 ′] .
                     2

                                     Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
24                                                                                Batz, Kaminski, Katoen, and Matheja


We omit unfolding ℎ further. Although our general construction yields  rather complex syntactic
preexpectations, notice we can express wpJwhile ( 𝑐 = 1 ) { 𝐶 ′ }K J𝑥K much more concisely as
                                          𝑥 + [𝑐 = 1] · 2        ∈     Exp .

11     ON NEGATIVE NUMBERS
Throughout the paper, we have evaded supporting negative numbers in two aspects:
   (1) In our verification system—the weakest preexpectation calculus—we allow expectations, both
       syntactic and semantic, to map program states to non-negative values in R∞      ≥0 only.
   (2) In our programming language, we allow variables to assume non-negative values in Q ≥0 only.
While the former restriction is fairly standard in the literature on probabilistic programs (cf. [McIver
and Morgan 2005]), considering only unsigned program variables is less common. An attentive
reader may thus ask whether our completeness results rely on the above restrictions. In this section,
we briefly comment on our reasons for considering only non-negative numbers. Moreover, we
discuss how one could incorporate support for negative numbers in both of the above aspects.

11.1    Signed Expectations
There exist approaches that support signed expectations, which allow arbitrary reals in their
codomain. However, as working with signed expectations may lead to integrability issues, these
approaches require a significant technical overhead (cf. [Kaminski and Katoen 2017] for details).
Moreover, proof rules for loops become much more involved. Calculi like Kozen’s PPDL in principle
allow signed expectations off-the-shelf, but PPDL’s induction rule for loops is restricted to non-
negative expectations as well [Kozen 1983]. We thus opted for the more common approach of
considering only unsigned expectations. An alternative is to perform a Jordan decomposition on
the expectation (i.e., decomposing it into positive and negative parts) and then reason individually
about the positive and the negative part. As outlined below, such a decomposition can already be
performed on program level without changing the verification system.

11.2    Signed Program Variables
Omitting negative numbers does not affect our results because they can easily be encoded in
our (Turing complete) programming language: we can emulate signed variables, for instance, by
splitting each variable 𝑥 into two variables |𝑥 | and 𝑥 sgn , representing the absolute value of 𝑥 and
its sign (𝑥 sgn = 1 if 𝑥 negative, and 𝑥 sgn = 0 otherwise), respectively. With this convention, the
program below emulates the subtraction assignment 𝑧 := 𝑥 − 𝑦 using only addition and monus:
                                           
                         if 𝑥 sgn = 𝑦sgn {                          // calculuate magnitude of 𝑧
                                                             
                             |𝑧| := |𝑥 | −¤ |𝑦| + |𝑦| −¤ |𝑥 |
                          } else {
                                |𝑧| := |𝑥 | + |𝑦|
                          };
                          if ( |𝑥 | > |𝑦| ) {                                           // calculuate sign of 𝑧
                                𝑧 sgn := 𝑥 sgn
                          } else {
                                if ( |𝑥 | = |𝑦| ) {
                                      𝑧 sgn := 0
                                } else {

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                            25


                                       𝑧 sgn := 1 −¤ 𝑦sgn
                                }
                          }
Similar emulations can be performed for addition, multiplication, etc. For the purpose of proving
relative completeness, signed variables are thus syntactic sugar; we omit them for simplicity.
   Our main reason for disallowing negative numbers as values of program variables is that we
want 𝑥 to be a valid (unsigned) expectation. If 𝑥 was signed, it would not be a valid expectation as
it does not map only to non-negative values. In order to fix this problem to some extent, one would
have to “make 𝑥 non-negative”, e.g., by instead using the expectation [𝑥 ≥ 0] · 𝑥 (𝑥 truncated at
0) or the expectation |𝑥 | (absolute value of 𝑥; not supported (but can be encoded) in our current
syntax). However, neither of the above expectations actually represents “the value of 𝑥”.

12     DISCUSSION
We now discuss a few aspects in which our expressive language Exp of expectations could be useful.

12.1    Relative Completeness of Probabilistic Program Verification
An immediate consequence of Theorem 10.2 is that, for all pGCL programs 𝐶 and all syntactic
expectations 𝑓 , 𝑔 ∈ Exp, verifying the bounds
                           J𝑔K ⪯ wpJ𝐶K (J𝑓 K)                or     wpJ𝐶K (J𝑓 K) ⪯ J𝑔K
reduces to checking a single inequality between two syntactic expectations in Exp, namely 𝑔 and
the effectively constructible expectation for wpJ𝐶K (J𝑓 K). In that sense, the wp calculus together with
Exp form a relatively complete (cf. [Cook 1978]) system for probabilistic program verification. Given
an oracle for discharging inequalities between syntactic expectations, every correct inequality of
the above form can be derived.

12.2    Termination Probabilities
For each probabilistic program 𝐶, the weakest preexpectation
                                                      wpJ𝐶K (1)
is a mapping from initial state 𝜎 to the probability that 𝐶 terminates on 𝜎. Since 1 ∈ Exp, termination
probabilities of any pGCL program on any input are expressible in our syntax.
   This demonstrates that our syntax is capable of capturing mappings from states to numbers
that are far from trivial as termination probabilities in general carry a high degree of internal
complexity [Kaminski and Katoen 2015; Kaminski et al. 2019]. More concretely, given 𝐶, 𝜎, and 𝛼,
deciding whether 𝐶 terminates on 𝜎 at least with probability 𝛼 is Σ01 –complete in the arithmetical
hierarchy. Deciding whether 𝐶 terminates on 𝜎 at most with probability 𝛼 is even Π 02 –complete,
thus strictly harder than, e.g., the universal termination problem for non-probabilistic programs.

12.3   Probability to Terminate in Some Postcondition
For a probabilistic program 𝐶 and a first-order predicate [𝜑], the weakest preexpectation
                                                     wpJ𝐶K ( [𝜑])
is a mapping from initial state 𝜎 to the probability that 𝐶 terminates on 𝜎 in a state 𝜏 |= 𝜑. Since
[𝜑] is expressible in Exp, we have that wpJ𝐶K ( [𝜑]) is also expressible in Exp by expressivity of
Exp. We can thus embed and generalize Dijkstra’s weakest preconditions completely in our system.

                                    Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
26                                                                                Batz, Kaminski, Katoen, and Matheja


12.4    Distribution over Final States
Let 𝐶 be a probabilistic program in which only the variables 𝑥 1, . . . , 𝑥𝑘 occur. Moreover, let 𝜇𝐶𝜎
be the final distribution obtained by executing 𝐶 on input 𝜎, cf. Section 2.1.3. Then, by the Kozen
duality (cf. Theorem 2.1), we can express the probability 𝜇𝐶𝜎 (𝜏) of 𝐶 terminating in final state 𝜏 on
initial state 𝜎, where 𝜏 (𝑥𝑖 ) = 𝑥𝑖′, by
                           𝜇𝐶𝜎 (𝜏) = wpJ𝐶K 𝑥 1 = 𝑥 1′ ∧ · · · ∧ 𝑥𝑘 = 𝑥𝑘′ (𝜎) .
                                                                       

Intuitively, we can write the initial values of 𝑥 1, . . . , 𝑥𝑘 into 𝜎 (𝑥 1 ), . . . , 𝜎 (𝑥𝑘 ) and the final values
into 𝜎 (𝑥 1′ ), . . . , 𝜎 (𝑥𝑘′ ).
                                                                                                        
   Since 𝑥 1 = 𝑥 1′ ∧ · · · ∧ 𝑥𝑘 = 𝑥𝑘′ ∈ Exp, we have that wpJ𝐶K 𝑥 1 = 𝑥 1′ ∧ · · · ∧ 𝑥𝑘 = 𝑥𝑘′ is ex-
                                     

pressible in Exp as well. Hence, we can express Kozen’s measure transformers in our syntax.

12.5    Ranking Functions / Supermartingales
There is a plethora of methods for proving termination of probabilistic programs based on ranking
supermartingales [Chakarov and Sankaranarayanan 2013; Chatterjee et al. 2016b, 2017; Fioriti and
Hermanns 2015; Fu and Chatterjee 2019; Huang et al. 2018, 2019]. Ranking supermartingales are
similar to ranking functions, but one requires that the value decreases in expectation. Weakest
preexpectations are the natural formalism to reason about this.
   For algorithmic solutions, ranking supermartingales are often assumed to be, for instance,
linear [Chatterjee et al. 2018] or polynomial [Chatterjee et al. 2016a; Ngo et al. 2018; Schreuder and
Ong 2019]. This also applies to the allowed shape of templates for loop invariants in works [Feng
et al. 2017; Katoen et al. 2010] on the automated synthesis of probabilistic loop invariants. Functions
linear or polynomial in the program variables are obviously subsumed by our syntax. However, our
syntax now enables searching for wider tractable classes.

12.6    Harmonic Numbers
Harmonic numbers are ubiquitous in reasoning about expected values or expected runtimes of
randomized algorithms. They appear, for instance, as the expected runtime of Hoare’s randomized
quicksort or the coupon collector problem, or as ranking functions for proving almost-sure ter-
mination [Kaminski 2019; Kaminski et al. 2018; McIver et al. 2018; Olmedo et al. 2016]. Harmonic
numbers are syntactically expressible in our language as in Example 7.8, or more conveniently as
                   r     h            iz
            𝐻𝑥 = Sum 𝑣 sum, 𝑣sum 1
                                   ,𝑥     ,             1
                                                where 𝑣sum  = S𝑧 : [𝑧 · 𝑣 sum = 1] · 𝑧 .

We note that, in termination proofs, the Harmonic numbers do not occur as termination probabilities,
but rather in ranking functions whose expected values after one loop iteration need to be determined.
Our syntax is capable of handling such ranking functions and we could safely add 𝐻𝑥 to our syntax.

13     CONCLUSION AND FUTURE WORK
We have presented a language of syntactic expectations that is expressive for weakest preexpectations
of probabilistic programs á la Kozen [1985] and McIver and Morgan [2005]. As a consequence, veri-
fication of bounds on expected values of functions (expressible in our language) after probabilistic
program execution is relative complete in the sense of Cook [1978].
   We have discussed various scenarios covered by our language, such as reasoning about termina-
tion probabilities, thus demonstrating the language’s usefulness.
Future Work. We currently do not support probabilistic programs with (binary) non-deterministic
choices, as do McIver and Morgan [2005], and it is not obvious how to incorporate it, given our

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                    27


current encoding. What seems even more out of reach is handling unbounded non-determinism,
which would be needed, for instance, to come up with an expressive expectation language for
quantitative separation logic (QSL)—an (extensional) verification system for compositional reasoning
about probabilistic pointer programs with access to a heap [Batz et al. 2019; Matheja 2020].
   For non-probabilistic heap-manipulating programs, a topic considered by Tatsuta et al. [2019]
are inductive definitions of predicates in classical separation logic (SL) and proving that SL is
expressive in this context. QSL also features inductive definitions and it would be interesting to
consider expressiveness in this setting.
   Despite its similarity to the wp calculus, we did not consider the expected runtime calculus (ert) by
Kaminski et al. [2018]. We strongly conjecture that Exp is expressive for expected runtimes as well.
   Finally, the conditional weakest preexpectation calculus (cwp) [Kaminski 2019; Olmedo et al.
2018] for probabilistic programs with conditioning needs weakest liberal preexpectations, which
generalize Dijkstra’s weakest liberal preconditions. It currently remains open, whether wlpJ𝐶K (𝑓 )
is expressible in Exp. There is the duality wlpJ𝐶K (𝑓 ) = 1 − wpJ𝐶K (1−𝑓 ), originally due to Kozen
[1983], but it is not immediate how to express 1−𝑓 in Exp, if 𝑓 is not a plain arithmetic expression.

Acknowledgements. We thank David N. Jansen for his feedback on an older version of this paper.

REFERENCES
Krzysztof R. Apt and Ernst-Rüdiger Olderog. 2019. Fifty years of Hoare’s logic. Formal Asp. Comput. 31, 6 (2019), 751–807.
   https://doi.org/10.1007/s00165-019-00501-3
Kevin Batz, Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Thomas Noll. 2019. Quantitative
   separation logic: a logic for reasoning about probabilistic pointer programs. Proc. ACM Program. Lang. 3, POPL (2019),
   34:1–34:29.
Joseph Bertrand. 1849. Traité d’Arithmétique. Libraire de L. Hachette et Cie.
Olivier Bournez and Florent Garnier. 2005. Proving Positive Almost-Sure Termination. In Term Rewriting and Applications,
   16th International Conference, RTA 2005, Nara, Japan, April 19-21, 2005, Proceedings (Lecture Notes in Computer Science,
   Vol. 3467), Jürgen Giesl (Ed.). Springer, 323–337. https://doi.org/10.1007/978-3-540-32033-3_24
Georg Cantor. 1878. Ein Beitrag zur Mannigfaltigkeitslehre. Journal für die reine und angewandte Mathematik 1878, 84
   (1878), 242–258.
Aleksandar Chakarov and Sriram Sankaranarayanan. 2013. Probabilistic Program Analysis with Martingales. In Computer
   Aided Verification - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013. Proceedings (Lecture
   Notes in Computer Science, Vol. 8044), Natasha Sharygina and Helmut Veith (Eds.). Springer, 511–526.
Krishnendu Chatterjee, Hongfei Fu, and Amir Kafshdar Goharshady. 2016a. Termination Analysis of Probabilistic Programs
   Through Positivstellensatz’s. In Computer Aided Verification - 28th International Conference, CAV 2016, Toronto, ON,
   Canada, July 17-23, 2016, Proceedings, Part I (Lecture Notes in Computer Science, Vol. 9779), Swarat Chaudhuri and Azadeh
   Farzan (Eds.). Springer, 3–22.
Krishnendu Chatterjee, Hongfei Fu, Petr Novotný, and Rouzbeh Hasheminezhad. 2016b. Algorithmic analysis of qualitative
   and quantitative termination problems for affine probabilistic programs. In Proceedings of the 43rd Annual ACM SIGPLAN-
   SIGACT Symposium on Principles of Programming Languages, POPL 2016, St. Petersburg, FL, USA, January 20 - 22, 2016,
   Rastislav Bodík and Rupak Majumdar (Eds.). ACM, 327–342.
Krishnendu Chatterjee, Hongfei Fu, Petr Novotný, and Rouzbeh Hasheminezhad. 2018. Algorithmic Analysis of Qualitative
   and Quantitative Termination Problems for Affine Probabilistic Programs. ACM Trans. Program. Lang. Syst. 40, 2 (2018),
   7:1–7:45.
Krishnendu Chatterjee, Petr Novotný, and Dorde Zikelic. 2017. Stochastic invariants for probabilistic termination. In
   Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages, POPL 2017, Paris, France,
   January 18-20, 2017, Giuseppe Castagna and Andrew D. Gordon (Eds.). ACM, 145–160.
Stephen A. Cook. 1978. Soundness and Completeness of an Axiom System for Program Verification. SIAM J. Comput. 7
   (1978), 70–90.
Patrick Cousot and Michael Monerau. 2012. Probabilistic Abstract Interpretation. In Programming Languages and Systems
   - 21st European Symposium on Programming, ESOP 2012, Held as Part of the European Joint Conferences on Theory and
   Practice of Software, ETAPS 2012, Tallinn, Estonia, March 24 - April 1, 2012. Proceedings (Lecture Notes in Computer Science,
   Vol. 7211), Helmut Seidl (Ed.). Springer, 169–193.


                                     Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
28                                                                                    Batz, Kaminski, Katoen, and Matheja


Jerry den Hartog and Erik P. de Vink. 2002. Verifying Probabilistic Programs Using a Hoare Like Logic. Int. J. Found. Comput.
   Sci. 13, 3 (2002), 315–340.
Alessandra Di Pierro and Herbert Wiklicky. 2016. Probabilistic Abstract Interpretation: From Trace Semantics to DTMC’s
   and Linear Regression. In Semantics, Logics, and Calculi - Essays Dedicated to Hanne Riis Nielson and Flemming Nielson on
   the Occasion of Their 60th Birthdays (Lecture Notes in Computer Science, Vol. 9560), Christian W. Probst, Chris Hankin, and
   René Rydhof Hansen (Eds.). Springer, 111–139.
Edsger W. Dijkstra. 1976. A Discipline of Programming. Prentice-Hall. http://www.worldcat.org/oclc/01958445
Yijun Feng, Lijun Zhang, David N. Jansen, Naijun Zhan, and Bican Xia. 2017. Finding Polynomial Loop Invariants for
   Probabilistic Programs. In Automated Technology for Verification and Analysis - 15th International Symposium, ATVA 2017,
   Pune, India, October 3-6, 2017, Proceedings (Lecture Notes in Computer Science, Vol. 10482), Deepak D’Souza and K. Narayan
   Kumar (Eds.). Springer, 400–416. https://doi.org/10.1007/978-3-319-68167-2_26
Luis María Ferrer Fioriti and Holger Hermanns. 2015. Probabilistic Termination: Soundness, Completeness, and Composi-
   tionality. In Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
   POPL 2015, Mumbai, India, January 15-17, 2015, Sriram K. Rajamani and David Walker (Eds.). ACM, 489–501.
Philippe Flajolet, Maryse Pelletier, and Michèle Soria. 2011. On Buffon Machines and Numbers. In Proceedings of the
   Twenty-Second Annual ACM-SIAM Symposium on Discrete Algorithms, SODA 2011, San Francisco, California, USA, January
   23-25, 2011, Dana Randall (Ed.). SIAM, 172–183. https://doi.org/10.1137/1.9781611973082.15
Robert W Floyd. 1967. Assigning Meanings to Programs. In Mathematical Aspects of Computer Science, J.T. Schwarz (Ed.),
   Vol. 19. American Mathematical Society, 19–32.
Hongfei Fu and Krishnendu Chatterjee. 2019. Termination of Nondeterministic Probabilistic Programs. In Verification, Model
   Checking, and Abstract Interpretation - 20th International Conference, VMCAI 2019, Cascais, Portugal, January 13-15, 2019,
   Proceedings (Lecture Notes in Computer Science, Vol. 11388), Constantin Enea and Ruzica Piskac (Eds.). Springer, 468–490.
Kurt Gödel. 1931. Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. Monatshefte für
   Mathematik und Physik 38, 1 (1931), 173–198.
Friedrich Gretz, Joost-Pieter Katoen, and Annabelle McIver. 2014. Operational versus weakest pre-expectation semantics for
   the probabilistic guarded command language. Perform. Evaluation 73 (2014), 110–132. https://doi.org/10.1016/j.peva.
   2013.11.004
Sergiu Hart, Micha Sharir, and Amir Pnueli. 1982. Termination of Probabilistic Concurrent Programs. In Conference Record
   of the Ninth Annual ACM Symposium on Principles of Programming Languages, Albuquerque, New Mexico, USA, January
   1982, Richard A. DeMillo (Ed.). ACM Press, 1–6.
C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. Commun. ACM 12, 10 (1969), 576–580.
Mingzhang Huang, Hongfei Fu, and Krishnendu Chatterjee. 2018. New Approaches for Almost-Sure Termination of
   Probabilistic Programs. In Programming Languages and Systems - 16th Asian Symposium, APLAS 2018, Wellington, New
   Zealand, December 2-6, 2018, Proceedings (Lecture Notes in Computer Science, Vol. 11275), Sukyoung Ryu (Ed.). Springer,
   181–201.
Mingzhang Huang, Hongfei Fu, Krishnendu Chatterjee, and Amir Kafshdar Goharshady. 2019. Modular verification for
   almost-sure termination of probabilistic programs. Proc. ACM Program. Lang. 3, OOPSLA (2019), 129:1–129:29.
Kenneth E. Iverson. 1962. A Programming Language. John Wiley & Sons, Inc., USA.
Benjamin Lucien Kaminski. 2019. Advanced weakest precondition calculi for probabilistic programs. Ph.D. Dissertation.
   RWTH Aachen University, Germany. http://publications.rwth-aachen.de/record/755408
Benjamin Lucien Kaminski and Joost-Pieter Katoen. 2015. On the Hardness of Almost-Sure Termination. In Mathematical
   Foundations of Computer Science 2015 - 40th International Symposium, MFCS 2015, Milan, Italy, August 24-28, 2015,
   Proceedings, Part I (Lecture Notes in Computer Science, Vol. 9234), Giuseppe F. Italiano, Giovanni Pighizzini, and Donald
   Sannella (Eds.). Springer, 307–318.
Benjamin Lucien Kaminski and Joost-Pieter Katoen. 2017. A weakest pre-expectation semantics for mixed-sign expectations.
   In 32nd Annual ACM/IEEE Symposium on Logic in Computer Science, LICS 2017, Reykjavik, Iceland, June 20-23, 2017. IEEE
   Computer Society, 1–12.
Benjamin Lucien Kaminski, Joost-Pieter Katoen, and Christoph Matheja. 2019. On the hardness of analyzing probabilistic
   programs. Acta Informatica 56, 3 (2019), 255–285.
Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Federico Olmedo. 2018. Weakest Precondition
   Reasoning for Expected Runtimes of Randomized Algorithms. J. ACM 65, 5 (2018), 30:1–30:68.
Joost-Pieter Katoen, Annabelle McIver, Larissa Meinicke, and Carroll C. Morgan. 2010. Linear-Invariant Generation for
   Probabilistic Programs: - Automated Support for Proof-Based Methods. In SAS (Lecture Notes in Computer Science,
   Vol. 6337). Springer, 390–406.
Stephen Cole Kleene, NG De Bruijn, J de Groot, and Adriaan Cornelis Zaanen. 1952. Introduction to Metamathematics.
   Vol. 483. van Nostrand New York.



Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                 29


Dexter Kozen. 1979. Semantics of Probabilistic Programs. In 20th Annual Symposium on Foundations of Computer Science,
    San Juan, Puerto Rico, 29-31 October 1979. IEEE Computer Society, 101–114.
Dexter Kozen. 1981. Semantics of Probabilistic Programs. J. Comput. Syst. Sci. 22, 3 (1981), 328–350. https://doi.org/10.1016/
    0022-0000(81)90036-2
Dexter Kozen. 1983. A Probabilistic PDL. In Proceedings of the 15th Annual ACM Symposium on Theory of Computing, 25-27
    April, 1983, Boston, Massachusetts, USA. ACM, 291–297. https://doi.org/10.1145/800061.808758
Dexter Kozen. 1985. A Probabilistic PDL. J. Comput. Syst. Sci. 30, 2 (1985), 162–178. https://doi.org/10.1016/0022-
    0000(85)90012-1
Dexter Kozen. 2000. On Hoare logic and Kleene algebra with tests. ACM Trans. Comput. Log. 1, 1 (2000), 60–76.
Dexter Kozen and Jerzy Tiuryn. 2001. On the completeness of propositional Hoare logic. Inf. Sci. 139, 3-4 (2001), 187–195.
Jacques Loeckx and Kurt Sieber. 1987. The Foundations of Program Verification, 2nd ed. Wiley-Teubner.
J. Loeckx, K. Sieber, and R.D. Stansifer. 1984. The Foundations of Program Verification. John Wiley. https://books.google.de/
    books?id=wagmAAAAMAAJ
Christoph Matheja. 2020. Automated Reasoning and Randomization in Separation Logic. Ph.D. Dissertation. RWTH Aachen
    University, Aachen. https://doi.org/10.18154/RWTH-2020-00940
Annabelle McIver and Carroll Morgan. 2005. Abstraction, Refinement and Proof for Probabilistic Systems. Springer. https:
    //doi.org/10.1007/b138392
Annabelle McIver, Carroll Morgan, Benjamin Lucien Kaminski, and Joost-Pieter Katoen. 2018. A new proof rule for
    almost-sure termination. Proc. ACM Program. Lang. 2, POPL (2018), 33:1–33:28.
Rajeev Motwani and Prabhakar Raghavan. 1999. Randomized Algorithms. In Algorithms and Theory of Computation
    Handbook, Mikhail J. Atallah (Ed.). CRC Press. https://doi.org/10.1201/9781420049503-c16
Van Chan Ngo, Quentin Carbonneaux, and Jan Hoffmann. 2018. Bounded expectations: resource analysis for probabilistic
    programs. In Proceedings of the 39th ACM SIGPLAN Conference on Programming Language Design and Implementation,
    PLDI 2018, Philadelphia, PA, USA, June 18-22, 2018, Jeffrey S. Foster and Dan Grossman (Eds.). ACM, 496–512.
Federico Olmedo, Friedrich Gretz, Nils Jansen, Benjamin Lucien Kaminski, Joost-Pieter Katoen, and Annabelle McIver. 2018.
    Conditioning in Probabilistic Programming. ACM Trans. Program. Lang. Syst. 40, 1 (2018), 4:1–4:50.
Federico Olmedo, Benjamin Lucien Kaminski, Joost-Pieter Katoen, and Christoph Matheja. 2016. Reasoning about Recursive
    Probabilistic Programs. In Proceedings of the 31st Annual ACM/IEEE Symposium on Logic in Computer Science, LICS ’16,
    New York, NY, USA, July 5-8, 2016, Martin Grohe, Eric Koskinen, and Natarajan Shankar (Eds.). ACM, 672–681.
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In 17th IEEE Symposium on Logic in
    Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings. IEEE Computer Society, 55–74.
Julia Robinson. 1949. Definability and Decision Problems in Arithmetic. J. Symb. Log. 14, 2 (1949), 98–114.
Anne Schreuder and C.-H. Luke Ong. 2019. Polynomial Probabilistic Invariants and the Optional Stopping Theorem. CoRR
    abs/1910.12634 (2019).
Makoto Tatsuta, Wei-Ngan Chin, and Mahmudul Faisal Al Ameen. 2009. Completeness of Pointer Program Verification by
    Separation Logic. In Software Engineering and Formal Methods. IEEE Computer Society, 179–188.
Makoto Tatsuta, Wei-Ngan Chin, and Mahmudul Faisal Al Ameen. 2019. Completeness and expressiveness of pointer
    program verification by separation logic. Inf. Comput. 267 (2019), 1–27.
Glynn Winskel. 1993. The Formal Semantics of Programming Languages: An Introduction. MIT Press, Cambridge, MA, USA.




                                    Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
30                                                                                      Batz, Kaminski, Katoen, and Matheja


A     APPENDIX TO SECTION 8 (THE DEDEKIND NORMAL FORM)
A.1     Proof of Lemma 8.1
     Lemma A.1. Let 𝛼 ∈ R ≥0 and 𝐴, 𝐵 ⊆ R∞
                                         ≥0 . Then, we have:
     (1)       𝛼 · sup 𝐴           = sup{𝛼 · 𝑎 | 𝑎 ∈ 𝐴},
     (2)        𝛼 · inf 𝐴          = inf {𝛼 · 𝑎 | 𝑎 ∈ 𝐴},
     (3) (sup 𝐴) + (sup 𝐵) = sup{𝛽 + 𝛾 | 𝛽 ∈ 𝐴, 𝛾 ∈ 𝐵},
     (4) (inf 𝐴) + (inf 𝐵) = inf {𝛽 + 𝛾 | 𝛽 ∈ 𝐴, 𝛾 ∈ 𝐵}, and
     (5) if 𝐴 is a singleton, i.e., 𝐴 = {𝛽}, then sup 𝐴 = inf 𝐴 = 𝛽,
where we define 0 · ∞ = 0.
     Proof of Lemma 8.1. By definition of equivalence between expectations, we have
                                       𝑓1 ≡ 𝑓2    iff for all 𝜎 : 𝜎 J𝑓1 K =     𝜎
                                                                                    J𝑓2 K .
Let us fix an arbitrary state 𝜎.
  To prove Lemma 8.1 (1) for Q = S, we proceed as follows:
                    𝜎
                   J( S𝑣 : 𝑓1 ) + 𝑓2 K
                       n                        o
                = sup 𝜎 [𝑣↦→𝑟 ] J𝑓1 K 𝑟 ∈ Q ≥0 + 𝜎 J𝑓2 K                                      (Semantics of expecations)
                       n                        o           n        o
                = sup 𝜎 [𝑣↦→𝑟 ] J𝑓1 K 𝑟 ∈ Q ≥0 + sup 𝜎 [𝑣↦→𝑟 ] J𝑓2 K                                     (Lemma A.1 (5))
                       n     ′
                                                                 o
                = sup 𝜎 [𝑣 ↦→𝑟 ] J𝑓1 [𝑣/𝑣 ′]K + 𝜎 J𝑓2 K 𝑟 ∈ Q ≥0                                (Lemma A.1 (3), 𝑣 ′ fresh)
                =   𝜎
                        JS𝑣 ′ : 𝑓1 [𝑣/𝑣 ′] + 𝑓2 K .                                           (Semantics of expectation)
The proofs for Q = J as well as the proof of Lemma 8.1 (2) are completely analogous.
  To prove Lemma 8.1 (3) for Q = J , we proceed as follows:
                         J𝑎 · J 𝑣 : 𝑓 K
                           𝜎
                                    n                      o
                     = 𝜎 J𝑎K · inf 𝜎 [𝑣↦→𝑟 ] J𝑓 K 𝑟 ∈ Q ≥0                                    (Semantics of expectations)
                           n                                o
                     = inf 𝜎 J𝑎K · 𝜎 [𝑣↦→𝑟 ] J𝑓 K 𝑟 ∈ Q ≥0                                               (Lemma A.1 (2))
                           n            ′
                                                                   o
                     = inf 𝜎 J𝑎K · 𝜎 [𝑣 ↦→𝑟 ] J𝑓 [𝑣/𝑣 ′]K 𝑟 ∈ Q ≥0                                              (𝑣 ′ fresh)
                     =     𝜎 J
                               J 𝑣 ′ : 𝑎 · 𝑓 [𝑣/𝑣 ′]K .                                       (Semantics of expectations)
The proofs for Q = S as well as the proof of Lemma 8.1 (4) are completely analogous.

A.2     Proof of Theorem 8.4
First, we prove that every 𝑓 ∈ Exp is equivalent to some expectation in summation normal form.
For that, we employ an auxiliary result:
  Lemma A.2. Let 𝑓 ∈ Exp be quantifier-free. Then there exist (1) a natural number 𝑛 ≥ 1, (2) Boolean
expressions 𝜑 1, . . . , 𝜑𝑛 , and (3) terms 𝑎 1, . . . , 𝑎𝑛 such that 𝑓 is equivalent to an expectation 𝑓 ′ given by
                                                            𝑛
                                                           ∑︁
                                                    𝑓′ =         [𝜑𝑖 ] · 𝑎𝑖 ,
                                                           𝑖=1

where the above sum is a shorthand for [𝜑 1 ] · 𝑎 1 + . . . + [𝜑𝑛 ] · 𝑎𝑛 .

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                             31


   Proof. By induction on the structure of quantifier-free syntactic expectations.

Base case 𝑓 = 𝑎. The expectation 𝑓 is obviously equivalent to
                                                          1
                                                         ∑︁
                                                 𝑓′ =          [true] · 𝑎 .
                                                         𝑖=1

As the induction hypothesis now assume that for some arbitrary, but fixed, quantifier-free syntactic
expectations 𝑓1 and 𝑓2 there are expectations 𝑓1′ and 𝑓2′ equivalent to 𝑓1 and 𝑓2 , respectively, given
by
                                                         𝑛
                                                        ∑︁
                                                𝑓1′ =         [𝜑𝑖 ] · 𝑎𝑖 , and
                                                        𝑖=1
                                                         𝑚
                                                        ∑︁
                                                𝑓2′ =
                                                               ′ ′
                                                               𝜑 𝑖 · 𝑎𝑖 .
                                                        𝑖=1

The case 𝑓 = 𝑎 · 𝑓1 . We have
                     𝑎 · 𝑓1
                          𝑛
                         ∑︁
                   ≡ 𝑎·     [𝜑𝑖 ] · 𝑎𝑖                                                                         (by I.H.)
                             𝑖=1
                         𝑛
                        ∑︁
                   ≡          [𝜑𝑖 ] · 𝑎 · 𝑎𝑖                  (· distributes over + in the quantifier-free setting)
                        𝑖=1
                         𝑛
                        ∑︁
                   ≡          [𝜑𝑖 ] · 𝑢𝑖 .                                                              (let 𝑢𝑖 = 𝑎 · 𝑎𝑖 )
                        𝑖=1

The case 𝑓 = 𝑓1 · 𝑎 is completely analogous.

The case 𝑓 = [𝜑] · 𝑓1 . We have
                    [𝜑] · 𝑓1
                           𝑛
                          ∑︁
                  ≡ [𝜑] ·    [𝜑𝑖 ] · 𝑎𝑖                                                                        (by I.H.)
                               𝑖=1
                        𝑛
                       ∑︁
                  ≡          [𝜑] · [𝜑𝑖 ] · 𝑎𝑖                 (· distributes over + in the quantifier-free setting)
                       𝑖=1
                        𝑛
                       ∑︁
                  ≡          [𝐺𝑖 ] · 𝑎𝑖 .                                                             (let 𝐺𝑖 = 𝜑 ∧ 𝜑𝑖 )
                       𝑖=1

The case 𝑓 = 𝑓1 · [𝜑] is completely analogous.

The case 𝑓 = 𝑓1 + 𝑓2 . This case is trivial since
                                                  𝑓1 + 𝑓2 ≡ 𝑓1′ + 𝑓2′ ,                                        (by I.H.)
where 𝑓1′ + 𝑓2′ is of the desired form. This completes the proof.                                                       □


                                     Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
32                                                                                            Batz, Kaminski, Katoen, and Matheja


  Theorem A.3 (Summation Normal Form). Every syntactic expectation 𝑓 is equivalent to an
expectation 𝑓 ′ in summation normal form, i.e. 𝑓 ′ is of the form
                                                            𝑛
                                                           ∑︁
                               𝑓 ′ = Q 1𝑣 1 . . . Q 𝑘 𝑣𝑘 :    [𝜑𝑖 ] · 𝑎𝑖 .
                                                                              𝑖=1

     Proof. By Lemma 8.1, 𝑓 is equivalent to an expectation in prenex normal form, i.e.,
                                                   𝑓 ≡ Q 1𝑣 1 . . . Q 𝑘 𝑣𝑘 : 𝑔 ,
where 𝑔 is quantifier-free. By Lemma A.2, 𝑔 is then equivalent to an expectation of the form
                                           𝑛
                                          ∑︁
                                               [𝜑𝑖 ] · 𝑎𝑖 .
                                                           𝑖=1
Hence, 𝑓 is equivalent to the following expectation in summation normal form:
                                                             𝑛
                                                            ∑︁
                                𝑓 ′ = Q 1𝑣 1 . . . Q 𝑘 𝑣𝑘 :    [𝜑𝑖 ] · 𝑎𝑖 .
                                                                              𝑖=1
                                                                                                                                   □
  Towards the construction of the Dedekind normal form of an expectation, we first show that the
Dedekind cut of an expectation 𝑓 is definable in AQ≥0 .
     Definition A.4. Let 𝑓 ∈ Exp be in summation normal form, say
                                                             𝑛
                                                            ∑︁
                                  𝑓 = Q 1𝑣 1 . . . Q 𝑘 𝑣𝑘 :    [𝜑𝑖 ] · 𝑎𝑖 .
                                                                             𝑖=1
Now let 𝑣 Cut be a fresh variable. We construct a formula 𝐷 [𝑣 Cut, 𝑓 ] inductively on 𝑘 as follows:
                        Í𝑛
  (1) If 𝑘 = 0 and 𝑓 =     [𝜑𝑖 ] · 𝑎𝑖 , then
                              𝑖=1
                                                         Û                            𝑛
                                                                                     Û                     𝑛
                                                                                                           ∑︁   
               𝐷 [𝑣 Cut, 𝑓 ] =                                                             𝐵𝑖 −→ 𝑣 Cut <      𝑇𝑖 .
                                                   >𝑛                              𝑖=1                       𝑖=1
                                    (𝐵𝑖 ,𝑇𝑖 ) 1≤𝑖 ≤𝑛 ∈   𝑖=1    (𝜑𝑖 ,𝑎𝑖 ),(¬𝜑𝑖 ,0)

     (2) If 𝑘 > 0 and 𝑓 = S𝑣 : 𝑓 ′, then
                                            𝐷 [𝑣 Cut, 𝑓 ] = ∃𝑣 : 𝐷 [𝑣 Cut, 𝑓 ′] .
     (3) If 𝑘 > 0 and 𝑓 = J 𝑣 : 𝑓 ′, let 𝑣 ′ be a fresh variable and define
                        𝐷 [𝑣 Cut, 𝑓 ] = ∃𝑣 ′ : 𝑣 ′ > 𝑣 Cut ∧ ∀𝑣 : 𝐷 [𝑣 Cut, 𝑓 ′] [𝑣 Cut /𝑣 ′] .
                                                                𝑛
                                                                Í
     Lemma A.5. For every 𝑓 = Q 1𝑣 1 . . . Q 𝑘 𝑣𝑘 :                   [𝜑𝑖 ] ·𝑎𝑖 in summation normal form and all states 𝜎,
                                                                𝑖=1

                                                                              𝜎 (𝑣 Cut ) ∈ Cut
                         𝜎                                                                        𝜎       
                             J𝐷 [𝑣 Cut, 𝑓 ]K = true                 iff                               J𝑓 K .
     Proof. By induction on 𝑘. We fix an arbitrary state 𝜎.
                                                                                      >𝑛
Base case 𝑘 = 0. There is exactly one ((𝐵 1′ ,𝑇1′), . . . , (𝐵𝑛′ ,𝑇𝑛′)) ∈                  𝑖=1 {(𝜑𝑖 , 𝑎𝑖 ), (¬𝜑𝑖 , 0)} such that
                                        𝜎t 𝑛           |
                                              Û
                                                     ′
                                                  𝐵𝑖         = true .
                                                          𝑖=1

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                                        33


Hence, we have
                                                    𝜎
                                                        J𝑓 K
                                                    𝜎t 𝑛                         |
                                                          ∑︁
                                             =                     [𝜑𝑖 ] · 𝑎𝑖                                                      (by definition)
                                                          𝑖=1
                                                    𝜎t 𝑛                 |
                                                          ∑︁
                                                                   𝑇𝑖′
                                                                                                                    𝜎 q     y
                                             =                               .                             (since      𝜑𝑗         = 0 if 𝐵 𝑗 = ¬𝜑 𝑗 )
                                                          𝑖=1

This gives us
         𝜎
             J𝐷 [𝑣 Cut, 𝑓 ]K = true
         𝜎u                                                                                                     }
                                             Û                                       𝑛
                                                                                     Û                    𝑛
                                                                                                         ∑︁   
  iff        v                                                                             𝐵𝑖 −→ 𝑣 Cut <    𝑇𝑖 ~ = true (by definition)
                                                 >𝑛
                 ( (𝐵 1 ,𝑇1 ),...,(𝐵𝑛 ,𝑇𝑛 )) ∈     𝑖=1 { (𝜑𝑖 ,𝑎𝑖 ),(¬𝜑𝑖 ,0) }
                                                                                     𝑖=1                 𝑖=1
         𝜎t 𝑛                                       𝑛
                                                               |
           Û                                       ∑︁
  iff                 𝐵𝑖′ −→ 𝑣 Cut <                     𝑇𝑖′         = true                                                (by above reasoning)
              𝑖=1                                  𝑖=1
         𝜎t                  𝑛
                                         |
                            ∑︁
  iff         𝑣 Cut <              𝑇𝑖′        = true                                       (left-hand side of implication evaluates to true)
                            𝑖=1
                              𝜎t 𝑛                 |
                                    ∑︁
  iff 𝜎 (𝑣 Cut ) <                           𝑇𝑖′                                                                                   (by definition)
                                     𝑖=1
                               𝜎
  iff 𝜎 (𝑣 Cut ) <                 J𝑓 K .                                                                                  (by above reasoning)


  As the induction hypothesis now assume that for some arbitrary, but fixed expectation 𝑓 ′ in
summation normal form and all states 𝜎, we have
                    J𝐷 [𝑣 Cut, 𝑓 ′]K = true       𝜎 (𝑣 Cut ) ∈ Cut 𝜎 J𝑓 ′K .
                  𝜎                                                       
                                             iff
Induction step for 𝑓 = S𝑣 : 𝑓 ′. We have
         𝜎
             J𝐷 [𝑣 Cut, 𝑓 ]K = true
   iff   𝜎
             J∃𝑣 : 𝐷 [𝑣 Cut, 𝑓 ′]K = true                                                                                          (by definition)
                                                       𝜎 [𝑣↦→𝑟 ]                     ′
   iff   there is 𝑟 ∈ Q ≥0 with      J𝐷 [𝑣 Cut, 𝑓 ]K = true                                                                        (by definition)
                                                                        
   iff there is 𝑟 ∈ Q ≥0 with 𝜎 [𝑣 ↦→ 𝑟 ] (𝑣 Cut ) ∈ Cut 𝜎 [𝑣↦→𝑟 ] J𝑓 ′K                                                                   (by I.H.)

   iff there is 𝑟 ∈ Q ≥0 with 𝜎 (𝑣 Cut ) < 𝜎 [𝑣↦→𝑟 ] J𝑓 ′K                                    (by definition and 𝑣 ≠ 𝑣 Cut by construction)
   iff 𝜎 (𝑣 Cut ) < sup 𝜎 [𝑣↦→𝑟 ] J𝑓 ′K | 𝑟 ∈ Q ≥0
                       
                                                                                                                                       (see below)
                               𝜎               ′         𝜎
   iff 𝜎 (𝑣 Cut ) < JS𝑣 : 𝑓 K = J𝑓 K .                                                                                             (by definition)


We justify the last but one step as follows. The “only if”-direction holds since the supremum
evaluates at least to 𝜎 [𝑣↦→𝑟 ] J𝑓 ′K . For the if -direction, assume for a contradiction that
                                  𝜎 (𝑣 Cut ) < sup 𝜎 [𝑣↦→𝑟 ] J𝑓 ′K | 𝑟 ∈ Q ≥0
                                                    
                                                                                               (6)

                                                   Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
34                                                                                        Batz, Kaminski, Katoen, and Matheja


and

                                    for all 𝑟 ∈ Q ≥0 it holds that 𝜎 (𝑣 Cut ) ≥ 𝜎 [𝑣↦→𝑟 ] J𝑓 ′K .                        (7)

Inequality (7) implies that 𝜎 (𝑣 Cut ) is an upper bound on 𝜎 [𝑣↦→𝑟 ] J𝑓 ′K | 𝑟 ∈ Q ≥0 . Hence, 𝜎 (𝑣 Cut )
                                                           

is greater than or equal to the least upper bound of this set. This contradicts inequality (6).

Induction step for 𝑓 = J 𝑣 : 𝑓 ′. We have
           𝜎
               J𝐷 [𝑣 Cut, 𝑓 ]K = true
     iff   𝜎
               J∃𝑣 ′ : 𝑣 ′ > 𝑣 Cut ∧ ∀𝑣 : 𝐷 [𝑣 Cut, 𝑓 ′] [𝑣 Cut /𝑣 ′]K = true                               (by definition)
     iff   there is 𝑠 ∈ Q ≥0 with 𝑠 > 𝜎 (𝑣 Cut ) such that for all 𝑟 ∈ Q ≥0 ,
                   𝜎 [𝑣′ ↦→𝑠 ] [𝑣↦→𝑟 ]
                                         J𝐷 [𝑣 Cut, 𝑓 ′] [𝑣 Cut /𝑣 ′]K = true                               (by definition)
     iff   there is 𝑠 ∈ Q ≥0 with 𝑠 > 𝜎 (𝑣 Cut ) such that for all 𝑟 ∈ Q ≥0 ,
                                                   ′                       
                𝜎 [𝑣 ′ ↦→ 𝑠] [𝑣 ↦→ 𝑟 ] (𝑣 ′) ∈ Cut 𝜎 [𝑣 ↦→𝑠 ] [𝑣↦→𝑟 ] J𝑓 ′K                                        (by I.H.)

     iff there is 𝑠 ∈ Q ≥0 with 𝑠 > 𝜎 (𝑣 Cut ) such that for all 𝑟 ∈ Q ≥0 , 𝑠 < [𝑣↦→𝑟 ] J𝑓 ′K
                                                                                       (𝑣 ′ and 𝑣 Cut are fresh)
     iff there is 𝑠 ∈ Q ≥0 with 𝑠 > 𝜎 (𝑣 Cut ) such that 𝑠 ≤ inf [𝑣↦→𝑟 ] J𝑓 ′K | 𝑟 ∈ Q ≥0 } (†, see below)
                                                                  

     iff 𝜎 (𝑣 Cut ) < inf [𝑣↦→𝑟 ] J𝑓 ′K | 𝑟 ∈ Q ≥0 }
                          
                                                      (“only if”: by tranisitivity, “if”: choose 𝑠 = inf . . .)
                       𝜎 J    ′        𝜎
     iff 𝜎 (𝑣 Cut ) < J 𝑣 : 𝑓 K = J𝑓 K .

We justify the step marked with † as follows. For the “only if”-direction, observe that if 𝑠 is a
strict lower bound on 𝜎 [𝑣↦→𝑟 ] J𝑓 K | 𝑟 ∈ Q ≥0 }, then 𝑠 is at least the greatest lower bound, i.e., the
                        

infimum, of this set. For the “if”-direction, first observe that 𝑠 ≠ 0 since 𝜎 (𝑣 Cut ) ≥ 0. Since Q ≥0 is
dense, there is an 𝑠 ′ with 𝜎 (𝑣 Cut ) < 𝑠 ′ < 𝑠. Hence, we have

                                𝑠 > 𝜎 (𝑣 Cut ) and 𝑠 ≤ inf [𝑣↦→𝑟 ] J𝑓 ′K | 𝑟 ∈ Q ≥0 }
                                                           

                              implies 𝑠 > 𝜎 (𝑣 Cut ) and for all 𝑟 ∈ Q ≥0 , 𝑠 ≤ [𝑣↦→𝑟 ] J𝑓 ′K
                              implies 𝑠 ′ > 𝜎 (𝑣 Cut ) and for all 𝑟 ∈ Q ≥0 , 𝑠 ′ < [𝑣↦→𝑟 ] J𝑓 ′K ,

which is what we had to show.
                                                                                                                           □

  Definition A.6 (Dedekind Normal Form). Let 𝑓 be an expectation in summation normal form. The
Dedekind normal form Dedekind[𝑣 Cut, 𝑓 ] of 𝑓 w.r.t. the fresh variable 𝑣 Cut is given by:

                                                Dedekind[𝑣 Cut, 𝑓 ] = [𝐷 [𝑣 Cut, 𝑓 ]] ,

where is [𝐷 [𝑣 Cut, 𝑓 ]] constructed according to Figure 4, and where we call 𝑣 Cut the cut variable of
Dedekind[𝑣 Cut, 𝑓 ].

  Soundness of the Dedekind normal form immediately follows from Theorem 7.3 and Lemma A.5.
Notice that, by Theorems 7.3 and A.3, Dedekind[𝑣 Cut, 𝑓 ] is equivalent to an expectation of the form
Prefix : [𝜑] for some quantifier prefix Prefix and some Boolean expression 𝜑. We thus often write
Dedekind[𝑣 Cut, 𝑓 ] = Prefix : [𝜑].

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                            35


A.3    Proof of Lemma 8.5
    Proof. Let 𝜎 be a state. We have
                     JS𝑣 Cut : Dedekind[𝑣 Cut, 𝑓 ] · 𝑣 Cut K
                      𝜎
                       n                                                      o
                  = sup 𝜎 [𝑣Cut ↦→𝑟 ] JDedekind[𝑣 Cut, 𝑓 ] · 𝑣 Cut K 𝑟 ∈ Q ≥0                          (by definition)
                       n                                       o
                  = sup 𝜎 [𝑣Cut ↦→𝑟 ] J𝑣 Cut K 𝑟 ∈ Cut 𝜎 J𝑓 K
                                                (since 𝜎 [𝑣Cut ↦→𝑟 ] JDedekind[𝑣 Cut, 𝑓 ]K = 0 if 𝑟 ∉ Cut 𝜎 J𝑓 K )
                                                                                                                 

                                           𝑟 ∈ Cut 𝜎 J𝑓 K
                                                         
                  = sup 𝑟 ∈ Q ≥0                                                                    (by definition)
                      𝜎
                  =       J𝑓 K .                                                                       (by definition)
                                                                                                                       □

B     APPENDIX TO SECTION 7 (GÖDELIZATION FOR SYNTACTIC EXPECTATIONS)
B.1    Proof of Lemma 7.1
    Proof. We employ a result by Robinson [Robinson 1949, Section 3]: For 𝑎, 𝑏, 𝑘 ∈ Q, let
                   Φ(𝑎, 𝑏, 𝑘) ≜ ∃𝑥, 𝑦, 𝑧 ∈ Q : 2 + 𝑎𝑏𝑘 2 + 𝑏𝑧 2 = 𝑥 2 + 𝑎𝑦 2
                      𝐵(𝑎, 𝑏) ≜ Φ(𝑎, 𝑏, 0) ∧ ∀𝑚 ∈ Q : (Φ(𝑎, 𝑏, 𝑚) −→ Φ(𝑎, 𝑏, 𝑚 + 1))
                           𝐴(𝑘) ≜ ∀𝑎, 𝑏 ∈ Q : 𝐵(𝑎, 𝑏) −→ Φ(𝑎, 𝑏, 𝑘) .
Then 𝑘 ∈ Q is an integer if and only if 𝐴(𝑘) holds. Denote by 𝐴 ′ (resp. Φ′, 𝐵 ′) the formula obtained
from 𝐴 (resp. Φ, 𝐵) by replacing every occurrence of Q by Q ≥0 , i.e. we restrict to quantification over
Q ≥0 . Note that Φ(𝑎 ′, 𝑏 ′, 𝑘 ′) iff Φ′ (𝑎 ′, 𝑏 ′, 𝑘 ′) for all 𝑎 ′, 𝑏 ′, 𝑘 ′ ∈ Q ≥0 since all occurrences of 𝑥, 𝑦, 𝑧 in
𝐵 are squared.
   Since 𝐴 ′ (𝑘 ′) is expressible in AQ≥0 , we prove the lemma by showing that for every 𝑘 ′ ∈ Q ≥0 ,
                                     𝑘′ ∈ N         if and only if       𝐴 ′ (𝑘 ′) .
The “only if” direction is straightforward since
                           Φ′ (𝑎, 𝑏, 0) ∧ ∀𝑚 ∈ Q ≥0 : (Φ′ (𝑎, 𝑏, 𝑚) −→ Φ′ (𝑎, 𝑏, 𝑚 + 1))
implies Φ(𝑎, 𝑏, 𝑘 ′) for all 𝑘 ′ ∈ N. Hence, if 𝑎, 𝑏 ∈ Q ≥0 and 𝐵 ′ (𝑎, 𝑏) holds, then Φ′ (𝑎, 𝑏, 𝑘 ′) holds,
which implies 𝐴 ′ (𝑘 ′).

The “if” direction is less obvious. We proceed by recapping the crucial parts of Robinson’s proof
that 𝐴(𝑘) implies 𝑘 ∈ Z for all 𝑘 ∈ Q on a sufficient level of abstraction. We then show how to
employ the same proof to show that 𝐴 ′ (𝑘 ′) implies 𝑘 ′ ∈ N for all 𝑘 ′ ∈ Q ≥0 .
  Robinson shows that it suffices to derive the following two facts from assumption 𝐴(𝑘):
                              Φ(1, 𝑝, 𝑘) holds for all primes 𝑝 ∈ 𝑃1                                                 (8)
                              Φ(𝑞, 𝑝, 𝑘) holds for all primes 𝑝 ∈ 𝑃2 and all 𝑞 ∈ 𝑄 ,                                 (9)
where 𝑃1, 𝑃2, 𝑄 ⊆ N are some non-empty sets of primes. We do not give these sets explicitly here
since they are not relevant for this proof. (8) and (9) in conjunction imply 𝑘 ∈ Z. Now, since
Φ(𝑎 ′, 𝑏 ′, 𝑘 ′) and Φ′ (𝑎 ′, 𝑏 ′, 𝑘 ′) are equivalent for all 𝑎 ′, 𝑏 ′, 𝑘 ′ ∈ Q ≥0 , our proof obligation is to show
that for every 𝑘 ′ ∈ Q ≥0 , 𝐴 ′ (𝑘 ′) implies:
                             Φ′ (1, 𝑝, 𝑘 ′) holds for all primes 𝑝 ∈ 𝑃 1 , and                                      (10)
                             Φ (𝑞, 𝑝, 𝑘 ) holds for all primes 𝑝 ∈ 𝑃2 and all 𝑞 ∈ 𝑄 .
                               ′       ′
                                                                                                                    (11)

                                   Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
36                                                                                       Batz, Kaminski, Katoen, and Matheja


We may then invoke Robinson’s result from above to conclude that 𝑘 ′ ∈ N.
    To prove (8), Robinson shows that 𝐵(1, 𝑝) holds for every 𝑝 ∈ 𝑃1 . Since 𝐵(1, 𝑝) implies 𝐵 ′ (1, 𝑝)
for all 𝑝 ∈ 𝑃1 (recall that 𝑝 is a natural number), we also get 𝐵 ′ (1, 𝑝). Now, assumption 𝐴(𝑘) and the
fact that 𝐵(1, 𝑝) holds imply Φ(1, 𝑝, 𝑘). We apply the same reasoning for Φ′ (1, 𝑝, 𝑘): Assumption
𝐴 ′ (𝑘) and the fact that 𝐵 ′ (1, 𝑝) holds imply Φ′ (1, 𝑝, 𝑘 ′), which proves (10).
    The proof of (11) is completely analogous.
                                                                                                       □

B.2     Proof of Theorem 7.2
     Proof. By induction on the structure of 𝑃 and by using Lemma 7.1.

Base case 𝑃 = 𝜑. If there is 𝑣 ∈ FV (𝑃) with 𝜎 (𝑣) ∉ N, then 𝜎 J𝑁 (𝑣)K = false and thus 𝜎 J𝑃Q≥0 K = false.
Conversely, if for all 𝑣 ∈ FV (𝑃) it holds that 𝜎 (𝑣) ∈ N, then 𝜎 is an interpretation for 𝑃 and obvi-
ously 𝜎 J𝑃Q≥0 K = 𝜎 J𝑃K since 𝜎 J𝑁 (𝑣)K = true.

As the induction hypothesis (I.H.) now assume that the theorem holds for some arbitrary, but fixed,
𝑃 ′ ∈ AN .

The case 𝑃 = ∃𝑣 : 𝑃 ′. First notice rthat FV z (𝑃) = FV (𝑃 ) \ {𝑣 }. Hence, if there is 𝑣 ∈ FV (𝑃)
                                                            ′                             ′
                                    𝜎
with 𝜎 (𝑣 ′) ∉ N, then 𝜎 J𝑃Q≥0 K =    𝑃 Q′ ≥0 = false by I.H. Now assume that for all 𝑣 ′ ∈ FV (𝑃) it
holds that 𝜎 (𝑣 ′) ∈ N, rendering 𝜎 an interpretation for 𝑃. We have
                                𝜎
                                    J𝑃 Q≥0 K = true
                                𝜎r              z
                      iff            ∃𝑣 : 𝑃Q′ ≥0    = true                                          (by definition)
                                                        𝜎 [𝑣↦→𝑟 ] r      z
                      iff      there is 𝑟 ∈ Q ≥0 with              𝑃Q′ ≥0 = true                    (by definition)
                                                     𝜎 [𝑣↦→𝑛] r        z
                      iff      there is 𝑛 ∈ N with              𝑃Q′ ≥0 = true
                                                                   𝜎 [𝑣↦→𝑟 ] r       z
                                         (If 𝑣 ∈ FV (𝑃 ′), then               𝑃 Q′ ≥0 = true only if 𝑟 ∈ N by I.H.)

                      iff      there is 𝑛 ∈ N with 𝜎 [𝑣↦→𝑛] J𝑃 ′K = true                                          (by I.H.)
                                𝜎            ′
                      iff           J∃𝑣 : 𝑃 K = true                                                       (by definition)
                                𝜎
                      iff           J𝑃K = true .                                                           (by definition)
The case 𝑃 = ∀𝑣 : 𝑃 ′. First notice that FV (𝑃) = FV (𝑃 ′) \ {𝑣 }. Hence, if there is 𝑣 ′ ∈ FV (𝑃) with
𝜎 (𝑣 ′) ∉ N, then
                      𝜎
                          J𝑃Q≥0 K
                      𝜎r                       z
                  =        ∀𝑣 : 𝑃Q′ ≥0 ∨ ¬𝑁 (𝑣)                                                            (by definition)
                                                              𝜎 [𝑣↦→𝑟 ] r        z
                  =   𝜎
                          J∀𝑣 : ¬𝑁 (𝑣)K .                 (             𝑃Q′ ≥0       = false for all 𝑟 ∈ Q ≥0 \ N by I.H.)
                  = false .                                                            (there is an 𝑟 ∈ Q ≥0 with 𝑟 ∉ N)
Now assume that for all 𝑣 ′ ∈ FV (𝑃) it holds that 𝜎 (𝑣 ′) ∈ N, rendering 𝜎 an interpretation for 𝑃.
We have
                                    𝜎
                                        J𝑃Q≥0 K = true

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                  37

                                     𝜎r                     z
                         iff            ∀𝑣 : 𝑃Q′ ≥0 ∨ ¬𝑁 (𝑣)       = true                        (by definition)
                                                               𝜎 [𝑣↦→𝑟 ] r               z
                         iff         for all 𝑟 ∈ Q ≥0 we have             𝑃Q′ ≥0 ∨ ¬𝑁 (𝑣) = true
                                                            𝜎 [𝑣↦→𝑛] r        z
                         iff         for all 𝑛 ∈ N we have             𝑃Q′ ≥0 = true
                                                                         ( 𝜎 [𝑣↦→𝑟 ] J¬𝑁 (𝑣)K = true for all 𝑟 ∈ Q ≥0 \ N)
                         iff         for all 𝑛 ∈ N we have 𝜎 [𝑣↦→𝑛] J𝑃 ′K = true                                    (by I.H.)
                                     𝜎           ′
                         iff             J∀𝑣 : 𝑃 K = true                                                    (by definition)
                                     𝜎
                         iff             J𝑃K = true .                                                        (by definition)

                                                                                                                             □

B.3   Proof of Theorem 7.3
   Proof. First notice that 𝜎 J[𝑃]K ∈ {0, 1} for all 𝑃 ∈ AQ≥0 . We now proceed by induction on the
structure of 𝑃.

Base case 𝑃 = 𝜑. This case follows immediately from the definition of 𝜎 J𝜑K .

As the induction hypothesis now assume that the theorem holds for some arbitrary, but fixed,
𝑃 ′ ∈ AQ ≥ 0 .

The case 𝑃 = ∃𝑣 : 𝑃 ′. We have
                             𝜎
                                 J[𝑃]K = 1
                   iff     JS𝑣 : [𝑃 ′]K = 1
                             𝜎
                                                                                                             (by definition)
                              n                         o
                   iff    sup 𝜎 [𝑣↦→𝑟 ] J[𝑃 ′]K 𝑟 ∈ Q ≥0 = 1                                                 (by definition)

                   iff    there is 𝑟 ∈ Q ≥0 with 𝜎 [𝑣↦→𝑟 ] J[𝑃 ′]K = 1                            ( 𝜎 [𝑣↦→𝑟 ] J[𝑃 ′]K ∈ {0, 1})
                   iff    there is 𝑟 ∈ Q ≥0 with 𝜎 [𝑣↦→𝑟 ] J𝑃 ′K = true                                             (by I.H.)
                             𝜎            ′
                   iff           J∃𝑣 : 𝑃 K = true .                                                          (by definition)

The case 𝑃 = ∀𝑣 : 𝑃 ′. We have
                         𝜎
                             J[𝑃]K = 1
                  iff     J 𝑣 : [𝑃 ′]K = 1
                         𝜎 J
                                                                                                             (by definition)
                             n                           o
                               𝜎 [𝑣↦→𝑟 ]
                  iff    inf             J[𝑃 ′]K 𝑟 ∈ Q ≥0 = 1

                  iff    for all 𝑟 ∈ Q ≥0 we have 𝜎 [𝑣↦→𝑟 ] J[𝑃 ′]K = 1                           ( 𝜎 [𝑣↦→𝑟 ] J[𝑃 ′]K ∈ {0, 1})
                  iff    for all 𝑟 ∈ Q ≥0 we have 𝜎 [𝑣↦→𝑟 ] J𝑃 ′K = true                                            (by I.H.)
                         𝜎            ′
                  iff        J∀𝑣 : 𝑃 K = true                                                                (by definition)
                         𝜎
                  iff        J𝑃K = true .                                                                    (by definition)

                                                                                                                             □

                                          Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
38                                                                                  Batz, Kaminski, Katoen, and Matheja


B.4      Proof of Theorem 7.7
      Proof. We define RElem by
         RElem (𝑣 1, 𝑣 2, 𝑣 3 )
      = ∃𝑛, 𝑛 1, 𝑛 2 : Pair(𝑛, 𝑛 1, 𝑛 2 ) ∧ Elem (𝑣 1, 𝑣 2, 𝑛) ∧ 𝑛 2 · 𝑣 3 = 𝑛 1 ∧ (𝑛 1 ⊥𝑛 2 ∨ (𝑛 1 = 0 ∧ 𝑛 2 = 1)) ,
                                                                                                       𝑛
where 𝑛 1 ⊥𝑛 2 denotes relative primality of 𝑛 1 and 𝑛 2 , which is definable in AN . Let 𝑟 0 = 𝑛00,,21 , . . . , 𝑟𝑘−1 =
𝑛𝑘−1,1
𝑛𝑘−1,2 such that each 𝑛𝑖,𝑗 is a natural number satisfying: If 𝑟 𝑖 = 0, then 𝑛𝑖,1 = 0 and 𝑛𝑖,2 = 1. If 𝑟 𝑖 ≠ 0,
then 𝑛𝑖,1 and 𝑛𝑖,2 are relatively prime. Notice that these conditions imply that the pairs 𝑛𝑖,0, 𝑛𝑖,1 are
unique.
  Furthermore, by Lemma 7.6, there is a unique sequence of natural numbers 𝑛 0, . . . , 𝑛𝑘−1 with
                              Pair(𝑛𝑖 , 𝑛𝑖,1, 𝑛𝑖,2 ) ≡ true   for all 𝑖 ∈ {0, . . . , 𝑘 − 1} .
Finally, by Lemma 7.4, there is a natural number 𝑎 encoding the sequence 𝑛 0, . . . , 𝑛𝑘−1 . This gives
us
       RElem (𝑎, 𝑖, 𝑟 ) ≡ true
iff    ∃𝑛, 𝑛 1, 𝑛 2 : Pair(𝑛, 𝑛 1, 𝑛 2 ) ∧ Elem (𝑎, 𝑖, 𝑛) ∧ 𝑛 2 · 𝑟 = 𝑛 1 ∧ (𝑛 1 ⊥𝑛 2 ∨ (𝑛 1 = 0 ∧ 𝑛 2 = 1)) ≡ true
                                                                                                      (by definition)
iff    Pair(𝑛𝑖 , 𝑛𝑖,1, 𝑛𝑖,2 ) ∧ Elem (𝑎, 𝑖, 𝑛𝑖 ) ∧ 𝑛𝑖,2 · 𝑟 = 𝑛𝑖,1 ≡ true
                                    (by above reasoning and uniqueness of the 𝑛s and the pairs 𝑛𝑖,1, 𝑛𝑖,2 )
iff 𝑟 = 𝑟𝑖 ,                                                                                       (by construction)
which completes the proof.                                                                                              □

C      APPENDIX TO SECTION 9 (SUMS, PRODUCTS, AND INFINITE SERIES OF
       SYNTACTIC EXPECTATIONS)
C.1      Proof of Theorem 9.2
      Proof. Write
                                     Dedekind[𝑣 Cut, 𝑓 ] = Prefix (𝑓 ) : [𝜑] ,

with cut variable 𝑣 Cut and where Prefix (𝑓 ) = Q 1𝑣 1 : . . . : Q 𝑛 𝑣𝑛 . Furthermore, assume that 𝑣, 𝑣 ′, 𝑛𝑢𝑚, 𝑢, 𝑧
are fresh logical variables not occurring in Dedekind[𝑣 Cut, 𝑓 ]. Now define
        Sum [𝑣 sum, 𝑓 , 𝑣]    ≜ S𝑣 ′ : S𝑛𝑢𝑚 : 𝑣 ′ · J 𝑢 : J 𝑧 : S𝑣 Cut : Prefix (𝑓 ) :
                                  [RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣)
                                     ∧ (𝑢 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑢, 𝑧) ∧ ( [𝜑] 𝑣 prod 𝑢 ∨ 𝑣 Cut = 0))
                                                                                    

                                         −→ RElem (𝑛𝑢𝑚, 𝑢 + 1, 𝑧 + 𝑣 Cut ) ] .
                                                                          

The reasoning is now analagous         to the proof of Theorem 9.4 using Lemma 9.1. The equality
 𝜎
   JS𝑣 : Sum [𝑣 sum, 𝑓 , 𝑣]K = ∞    𝜎
                              Í
                                𝑗=0   J𝑓 K holds since an infinite series evaluates to the supremum of
its partial sums.
                                                                                                    □

C.2      Proof of Theorem 9.4
We employ the following auxiliary result.

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                                                39


      Lemma C.1. For all 𝛼 0, . . . , 𝛼𝑛 ∈ R∞
                                            ≥ 0 , we have
                       𝑛
                       Ö
                              𝛼 𝑗 = sup 𝑟 ∈ Q ≥0 𝑟 = 𝑟 0 · . . . · 𝑟𝑛 , ∀0 ≤ 𝑖 ≤ 𝑛 : 𝑟𝑖 ∈ Cut (𝛼𝑖 )
                                       
                                                                                                                                  .
                        𝑗=0

      Proof. By induction on 𝑛.                                                                                                                           □
      We now prove Theorem 9.4.
      Proof. Write
                                                    Dedekind[𝑣 Cut, 𝑓 ] = Prefix : [𝜑]
and assume that 𝑣, 𝑣 ′, 𝑛𝑢𝑚, 𝑢, 𝑧 are fresh variables not occurring in Dedekind[𝑣 Cut, 𝑓 ]. Furthermore,
denote by Prefix the quantifier prefix obtained from Prefix by flipping all quantifiers, i.e., by
replacing every occurrence of S by J and vice versa. Now define
   Product 𝑣 prod, 𝑓 , 𝑣   ≜ S𝑣 ′ : S𝑛𝑢𝑚 : 𝑣 ′ · J 𝑢 : J 𝑧 : S𝑣 Cut : Prefix :
                        

                                                [RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣 ′)
                                                   ∧ (𝑢 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑢, 𝑧) ∧ ( [𝜑] 𝑣 prod 𝑢 ∨ 𝑣 Cut = 0))
                                                                                                  

                                                       −→ RElem (𝑛𝑢𝑚, 𝑢 + 1, 𝑧 · 𝑣 Cut ) ] .
                                                                                        

The crux of the proof is to show that the {0, 1}-valued expectation right after 𝑣 ′ · . . . evaluates
to 1 on state 𝜎 iff 𝜎 (𝑛𝑢𝑚) encodes a sequence 1, 1 · 𝑟 0, 1 · 𝑟 0 · 𝑟 1, . . . , 1 · 𝑟 0 · . . . · 𝑟 𝜎 (𝑣) where
           q        y                                            𝜎Î(𝑣)
𝑟 𝑗 ∈ Cut
           𝜎
             𝑓 𝑣 prod 𝑗     for all 0 ≤ 𝑗 ≤ 𝜎 (𝑣) and where 𝜎 (𝑣 ′) =        𝑟 𝑗 . This implies
                                                                                                                 𝑗=0

             Product 𝑣 prod, 𝑓 , 𝑣
        𝜎q                        y

 =      𝜎
            JS𝑣 ′ : S𝑛𝑢𝑚 : 𝑣 ′ · . . .K                                                                                           (by definition)
                                                                                                           (𝑣)
                       (                                                                                  𝜎Ö
                                                                                                                                                                         )
                                                                                                                                                                    
                                                                                                                                           𝜎 [ 𝑣prod ↦→ 𝑗 ]
 = sup sup                                ′
                               𝑟 𝑟 encodes 1, . . . , 1 · 𝑟 0 · . . . · 𝑟 𝜎 (𝑣) and 𝑟 =                          𝑟 𝑗 where 𝑟 𝑗 ∈ Cut                          J𝑓 K
        𝑟 ∈Q≥0 𝑟 ′ ∈Q≥0                                                                                   𝑗=0
                                                                                                                          (claim proven below)
                                    (𝑣)
                  (                𝜎Ö
                                                                                                  )
                                                                                             
                                                                    𝜎 [ 𝑣prod ↦→ 𝑗 ]
 = sup                𝑟 𝑟=                𝑟 𝑗 where 𝑟 𝑗 ∈ Cut                          J𝑓 K           .
        𝑟 ∈Q≥0                      𝑗=0
         (𝑣)
        𝜎Ö
                𝜎 [ 𝑣prod ↦→ 𝑗 ]
 =                                 J𝑓 K .                                                                                       (by Lemma C.1)
        𝑗=0

We have
        𝜎
            JJ 𝑢 : J 𝑧 : S𝑣 Cut : Prefix :
        [RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣 ′)
              ∧ (𝑢 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑢, 𝑧) ∧ ( [𝜑] 𝑣 prod 𝑢 ∨ 𝑣 Cut = 0))
                                                             

                  −→ RElem (𝑛𝑢𝑚, 𝑢 + 1, 𝑧 · 𝑣 Cut ) ]K = 1
                                                   
                                                                    𝜎
iff     for all 𝑟, 𝑠 ∈ Q ≥0 there is 𝑡 ∈ Q ≥0 with JPrefix :
        [RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣 ′)
              ∧ (𝑟 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑟, 𝑠) ∧ ( [𝜑] 𝑣 prod 𝑟 [𝑣 Cut /𝑡] ∨ 𝑡 = 0))
                                                             


                                                Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
40                                                                                     Batz, Kaminski, Katoen, and Matheja


                  −→ RElem (𝑛𝑢𝑚, 𝑟 + 1, 𝑠 · 𝑡) ]K = 1
                                              
                                                                                            (expectation is {0,1}-valued)
iff     𝜎
            J[RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣 )]K = 1 and for all 𝑟, 𝑠 ∈ Q ≥0
                                                                ′

                                   𝜎
        there is 𝑡 ∈ Q ≥0 with JPrefix :
        [ (𝑟 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑟, 𝑠) ∧ ( [𝜑] 𝑣 prod 𝑟 [𝑣 Cut /𝑡] ∨ 𝑡 = 0))
                                                       

                −→ RElem (𝑛𝑢𝑚, 𝑟 + 1, 𝑠 · 𝑡) ]K = 1
                                              
                  (quantitative quantifiers correspond to qualitative quantifiers, standard prenexing)
iff     𝜎
          J[RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣 ′)]K = 1 and for all 𝑟, 𝑠 ∈ Q ≥0 there is 𝑡 ∈ Q ≥0 with
          J[𝑟 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑟, 𝑠)K = 1 and Prefix : [𝜑] 𝑣 prod 𝑟 [𝑣 Cut /𝑡] ∨ 𝑡 = 0 = 1
        𝜎                                          𝜎q                                        y

            implies 𝜎 JRElem (𝑛𝑢𝑚, 𝑟 + 1, 𝑠 · 𝑡)K = 1
                      (standard prenexing into antecedent of implication, expectation is {0, 1}-valued)
iff     𝜎
          J[RElem (𝑛𝑢𝑚, 0, 1) ∧ RElem (𝑛𝑢𝑚, 𝑣 + 1, 𝑣)]K = 1 and for all 𝑟, 𝑠 ∈ Q ≥0 there is 𝑡 ∈ Q ≥0 with
                                                                              
        𝜎
          J[𝑟 < 𝑣 + 1 ∧ RElem (𝑛𝑢𝑚, 𝑟, 𝑠)K = 1 and 𝑡 ∈ Cut 𝜎 [ 𝑣prod ↦→𝑟 ] J𝑓 K ∪ {0}
            implies 𝜎 JRElem (𝑛𝑢𝑚, 𝑟 + 1, 𝑠 · 𝑡)K = 1                                                  (by Theorem 8.4)
iff 𝜎 (𝑛𝑢𝑚) encodes sequence 1, 1 · 𝑟 0, 1 · 𝑟 0 · 𝑟 1, . . . , 1 · 𝑟 0 · . . . · 𝑟 𝜎 (𝑣)
                                       
    with 𝑟 𝑗 ∈ Cut 𝜎 [ 𝑣prod ↦→ 𝑗 ] J𝑓 K for all 0 ≤ 𝑗 ≤ 𝜎 (𝑣)
                                 (𝑣)
                                𝜎Ö
                         ′
        and where 𝜎 (𝑣 ) =             𝑟𝑗 .
                                 𝑗=0

                                                                                                                         □

D      APPENDIX TO SECTION 10 (EXPRESSIVENESS OF OUR LANGUAGE)
Given an expectation 𝑋 ∈ E, we denote by

               Vars(𝑋 ) = { 𝑥 ∈ Vars | ∃𝜎 ∈ Σ : ∃𝑛, 𝑛 ′ ∈ N : 𝑋 (𝜎 [𝑥 ↦→ 𝑛]) ≠ 𝑋 (𝜎 [𝑥 ↦→ 𝑛 ′]) }

the set of all “relevant” variables in 𝑋 . We restrict to expectations 𝑋 with |Vars(𝑋 )| < ∞, since
|Vars(J𝑓 K)| < ∞ holds for every syntactic expectation 𝑓 . Theorem 10.1 is a consequence of the
while-case of the following theorem.

  Theorem D.1. Let 𝐶 be a program and 𝑋 be an expectation. Furthermore, let x be a finite set of
program variables with Vars(𝐶) ∪ Vars(𝑋 ) ⊆ x. We have
                                           ∑︁
                      wpJ𝐶K (𝑋 ) = 𝜆𝜎0 .       wpJ𝐶K ( [𝜎] x ) (𝜎0 ) · 𝑋 (𝜎) .
                                                        𝜎 ∈Σx

      Proof. By induction on the structure of 𝐶. For a state 𝜎 ′, we often abbreviate [𝜎 ′] x by [𝜎 ′] .

The case 𝐶 = skip. We have

                                wpJskipK (𝑋 ) (𝜎0 )
                             = 𝑋 (𝜎0 )                                                                    (by definition)
                             = [𝜎0 ] (𝜎0 ) · 𝑋 (𝜎0 )                                                      ([𝜎0 ] (𝜎0 ) = 1)
                             = wpJskipK ( [𝜎0 ] ) (𝜎0 ) · 𝑋 (𝜎0 )                             (wpJskipK ( [𝜎0 ] ) = [𝜎0 ] )

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                      41

                                       ∑︁
                            =                 wpJskipK ( [𝜎] ) (𝜎0 ) · 𝑋 (𝜎) .
                                      𝜎 ∈Σx
        (there is exactly one 𝜎 ∈ Σx with wpJskipK ( [𝜎] ) (𝜎0 ) = 1 and for this 𝜎 we have 𝜎 ∼x 𝜎0 )

The case 𝑥 := 𝑎. We have

          wpJ𝑥 := 𝑎K (𝑋 ) (𝜎0 )
                           
        = 𝑋 (𝜎0 𝑥 ↦→ 𝜎0 J𝑎K )                                                                       (by definition)
                  𝜎0                   𝜎0                         𝜎0      
        = 𝜎0 𝑥 ↦→ J𝑎K (𝜎0 𝑥 ↦→ J𝑎K ) · 𝑋 (𝜎0 𝑥 ↦→ J𝑎K )
                                                                                                             
                                                               ( 𝜎0 𝑥 ↦→ 𝜎0 J𝑎K (𝜎0 𝑥 ↦→ 𝜎0 J𝑎K ) = 1)
                                        
        = wpJ𝑥 := 𝑎K 𝜎0 𝑥 ↦→ 𝜎0 J𝑎K
                                                                                
                                               (𝜎0 ) · 𝑋 (𝜎0 𝑥 ↦→ 𝜎0 J𝑎K )                          (by definition)
                                                           there is exactly one 𝜎 ∈ Σx with wpJ𝑥 :=
                                                                                                   𝑎 K ( [𝜎 ] ) (𝜎
                                                                                                                   0 ) = 1)
           ∑︁
        =      wpJ𝑥 := 𝑎K ( [𝜎] ) (𝜎0 ) · 𝑋 (𝜎) .        (         and for this 𝜎 we have 𝜎 ∼x 𝜎0 𝑥 ↦→ 𝜎0 J𝑎 K
              𝜎 ∈Σx

As the induction hypothesis now assume that the theorem holds for some arbitrary, but fixed
programs 𝐶 1, 𝐶 2 and all postexpectations 𝑋 .

The case 𝐶 = 𝐶 1 ; 𝐶 2 . We have

                      wpJ𝐶 1 ; 𝐶 2 K (𝑋 ) (𝜎0 )
                  = wpJ𝐶 1 K wpJ𝐶 2 K (𝑋 ) (𝜎0 )
                                           
                                                                                                                 (by definition)
                     ∑︁
                  =     wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) · wpJ𝐶 2 K (𝑋 ) (𝜎)                                                  (I.H. on 𝐶 1 )
                        𝜎 ∈Σx
                        ∑︁                                       ∑︁
                  =                  wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) ·             wpJ𝐶 2 K ( [𝜎 ′] ) (𝜎) · 𝑋 (𝜎 ′)          (I.H. on 𝐶 2 )
                        𝜎 ∈Σx                                   𝜎 ′ ∈Σx
                        ∑︁ ∑︁
                  =                        wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) · wpJ𝐶 2 K ( [𝜎 ′] ) (𝜎) · 𝑋 (𝜎 ′)                    (algebra)
                        𝜎 ∈Σx 𝜎 ′ ∈Σx
                         ∑︁ ∑︁
                  =                        wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) · wpJ𝐶 2 K ( [𝜎 ′] ) (𝜎) · 𝑋 (𝜎 ′)                    (algebra)
                        𝜎 ′ ∈Σ   x 𝜎 ∈Σx
                         ∑︁
                                     wpJ𝐶 1 K wpJ𝐶 2 K ( [𝜎 ′] ) (𝜎0 ) · 𝑋 (𝜎 ′)
                                                                
                  =                                                                                                 (I.H. on 𝐶 1 )
                        𝜎 ′ ∈Σx
                         ∑︁
                  =                  wpJ𝐶 1 ; 𝐶 2 K ( [𝜎 ′] ) (𝜎0 ) · 𝑋 (𝜎 ′) .                                  (by definition)
                        𝜎 ′ ∈Σ   x


The case 𝐶 = if ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }. We distinguish the cases [𝜑] (𝜎0 ) = 1 and [¬𝜑] (𝜎0 ) = 1.
For [𝜑] (𝜎0 ) = 1, we have

               wpJif ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }K (𝑋 ) (𝜎0 )
          = [𝜑] (𝜎0 ) · wpJ𝐶 1 K (𝑋 ) (𝜎0 ) + [¬𝜑] (𝜎0 ) · wpJ𝐶 2 K (𝑋 ) (𝜎0 )                                   (by definition)
          = [𝜑] (𝜎0 ) · wpJ𝐶 1 K (𝑋 ) (𝜎0 )                                                       ([¬𝜑] (𝜎0 ) = 0 by assumption)
                         ∑︁
          = [𝜑] (𝜎0 ) ·      wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 ) · 𝑋 (𝜎1 )                                                     (I.H. on 𝐶 1 )
                                 𝜎1 ∈Σx
                 ∑︁
          =             [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 ) · 𝑋 (𝜎1 )                                                  (algebra)
               𝜎1 ∈Σx


                                              Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
42                                                                                             Batz, Kaminski, Katoen, and Matheja

                    ∑︁
                                 [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 ) + [¬𝜑] (𝜎0 ) · wpJ𝐶 2 K ( [𝜎1 ] ) (𝜎0 ) · 𝑋 (𝜎1 )
                                                                                                             
          =
                  𝜎1 ∈Σx
                                                                                              ([¬𝜑] (𝜎0 ) = 0 by assumption)
                    ∑︁
          =                  wpJif ( 𝜑 ) { 𝐶 1 } else { 𝐶 2 }K (𝜎1 ) (𝜎0 ) · 𝑋 (𝜎1 ) .                           (by definition)
                  𝜎1 ∈Σx

The case [¬𝜑] (𝜎0 ) = 1 is completely analogous.

The case 𝐶 = while ( 𝜑 ) { 𝐶 1 }. This case is more involved. First observe that for every 𝜎1 ∈ Σ,

                    sup Φ𝑘[𝜎1 ] (0) (𝜎0 ) = wpJwhile ( 𝜑 ) { 𝐶 1 }K ( [𝜎1 ] ) (𝜎0 ) .                           (by Lemma 2.2)
                    𝑘 ∈N

We proceed by induction on 𝑘 to show that

              Φ𝑘𝑋 (0) (𝜎0 )
                      ∑︁                                        𝑘−2
                                                                Ö
         =                             ( [¬𝜑] · 𝑋 ) (𝜎𝑘−1 ) ·         wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
                 𝜎0 ,...,𝜎𝑘−1 ∈Σx                               𝑖=0
                  ∑︁
         =                  Φ𝑘[𝜎1 ] (0) (𝜎0 ) · 𝑋 (𝜎1 ) .                                                                    (12)
                 𝜎1 ∈Σx

This implies the claim, since
                  wpJwhile ( 𝜑 ) { 𝐶 1 }K (𝑋 ) (𝜎0 )
             = sup Φ𝑘𝑋 (0) (𝜎0 )                                                                                (by Lemma 2.2)
               𝑘 ∈N
                    ∑︁
             = sup       Φ𝑘[𝜎1 ] (0) (𝜎0 ) · 𝑋 (𝜎1 )                                                          (by Equation 12)
                   𝑘 ∈N 𝜎 ∈Σ
                             1     x

                                   𝑘′
                                   ∑︁
             = sup sup                   Φ𝑘[enum(𝑖) ] (0) (𝜎0 ) · 𝑋 (enum(𝑖))
                   𝑘 ∈N 𝑘 ′ ∈N 𝑖=0
     (choose some bijection enum : N → Σx , value of infinite series is supremum of partial sums)
                                   𝑘′
                                   ∑︁
             = sup sup                   Φ𝑘[enum(𝑖) ] (0) (𝜎0 ) · 𝑋 (enum(𝑖))                                  (swap suprema)
                   𝑘 ′ ∈N 𝑘 ∈N 𝑖=0
                            𝑘′
                            ∑︁
             = sup                 sup Φ𝑘[enum(𝑖) ] (0) (𝜎0 ) · 𝑋 (enum(𝑖))                             (algebra, sum is finite)
                   𝑘 ′ ∈N   𝑖=0 𝑘 ∈N
                            𝑘′
                            ∑︁
             = sup                 wpJwhile ( 𝜑 ) { 𝐶 1 }K ( [enum(𝑖)] ) (𝜎0 ) · 𝑋 (enum(𝑖))                    (by Lemma 2.2)
                   𝑘 ′ ∈N 𝑖=0
                    ∑︁
             =                wpJwhile ( 𝜑 ) { 𝐶 1 }K ( [𝜎1 ] ) (𝜎0 ) · 𝑋 (𝜎1 ) .
                   𝜎1 ∈Σx
                                                                      (value of infinite series is supremum of partial sums)

Base case 𝑛 = 0. For Φ𝑋0 (0) (𝜎0 ), we have

             Φ𝑋0 (0) (𝜎0 )
        = 0

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                         43


                       ∑︁                                      𝑘−2
                                                               Ö
          =                          ( [¬𝜑] · 𝑋 ) (𝜎𝑘−1 ) ·           wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) .
                  𝜎0 ,...,𝜎𝑘−1 ∈Σx                              𝑖=0
                                                                                                       (empty sum evaluates to 0)

        𝜎1 ∈Σx Φ [𝜎1 ] (0)(𝜎0 ) · 𝑋 (𝜎1 ), we have
      Í         0
For
                                                              ∑︁
                                                                      Φ0[𝜎1 ] (0)(𝜎0 ) · 𝑋 (𝜎1 )
                                                            𝜎1 ∈Σx
                                                              ∑︁
                                                      =               0 · 𝑋 (𝜎1 )
                                                            𝜎1 ∈Σx
                                                      = 0.

As the induction hypothesis now assume that Equation (12) holds for some arbitrary, but fixed,
𝑘 ∈ N.

Induction Step. For Φ𝑘+ 1
                     𝑋 (0) (𝜎0 ), we have

      Φ𝑘+ 1
       𝑋 (0) (𝜎0 )
               
    = Φ𝑘 Φ𝑘𝑋 (0) (𝜎0 )                                                                                               (by definition)
                                                 
    = [𝜑] (𝜎0 ) · wpJ𝐶 1 K Φ𝑘𝑋 (0) (𝜎0 ) + [¬𝜑] (𝜎0 ) · 𝑋 (𝜎0 )                                                      (by definition)
    = [𝜑] (𝜎0 )
                                                                                    𝑘−2
                                                                                                                                             !
                                              ∑︁                                    Ö
              · wpJ𝐶 1 K 𝜆𝜎0 .                             ( [¬𝜑] · 𝑋 ) (𝜎𝑘−1 ) ·          wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) (𝜎
                                        𝜎0 ,...,𝜎𝑘−1 ∈Σx                             𝑖=0
        + [¬𝜑] (𝜎0 ) · 𝑋 (𝜎0 )                                                                                            (I.H. on 𝑘)
                  ∑︁
    = [𝜑] (𝜎0 ) ·     wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 )
                          𝜎1 ∈Σx
                                                                          𝑘−2
                                                                                                                                     !
                                 ∑︁                                       Ö
              · 𝜆𝜎0 .                         ( [¬𝜑] · 𝑋 ) (𝜎𝑘−1 ) ·            wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) (𝜎1 )
                           𝜎0 ,...,𝜎𝑘−1 ∈Σx                               𝑖=0
        + [¬𝜑] (𝜎0 ) · 𝑋 (𝜎0 )                                                                                          (I.H. on 𝐶 1 )
                  ∑︁
    = [𝜑] (𝜎0 ) ·     wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 )
                          𝜎1 ∈Σx
                                                            𝑘−1
                                                                                                                           !
                        ∑︁                                  Ö
              ·                     ([¬𝜑] · 𝑋 ) (𝜎𝑘 ) ·            wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
                   𝜎1 ,...,𝜎𝑘 ∈Σx                            𝑖=1
            + [¬𝜑] (𝜎0 ) · 𝑋 (𝜎0 )                                                                   (applying 𝜎1 and index shift)
           ∑︁
    =          [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 )
          𝜎1 ∈Σx
                                                            𝑘−1
                                                                                                                           !
                        ∑︁                                  Ö
              ·                     ([¬𝜑] · 𝑋 ) (𝜎𝑘 ) ·            wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
                   𝜎1 ,...,𝜎𝑘 ∈Σx                            𝑖=1
              + [¬𝜑] (𝜎0 ) · 𝑋 (𝜎0 )                                                                                       (algebra)

                                              Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
44                                                                                                    Batz, Kaminski, Katoen, and Matheja


               ∑︁                                  𝑘−1
                                                   Ö
     =                     ([¬𝜑] · 𝑋 ) (𝜎𝑘 ) ·           wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) . (see below)
          𝜎0 ,...,𝜎𝑘 ∈Σx                           𝑖=0

To see that the last step is sound, distinguish the cases [𝜑] (𝜎0 ) = 1 and [𝜑] (𝜎0 ) = 0. If [𝜑] (𝜎0 ) = 1,
then wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎1 ] ) (𝜎0 ) = wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 ). Conversely, if [𝜑] (𝜎0 ) =
0, then there is exactly one sequence of states 𝜎0, . . . , 𝜎𝑘 = 𝜎0, . . . , 𝜎0 such that
                                    𝑘−1
                                    Ö
                                           wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
                                     𝑖=0

evaluates to 1. For all other sequences, the above product evaluates to 0. This gives us
                      ∑︁                                    𝑘−1
                                                            Ö
                                  ( [¬𝜑] · 𝑋 ) (𝜎𝑘−1 ) ·           wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
                 𝜎0 ,...,𝜎𝑘 ∈Σx                              𝑖=0
                                            𝑘−1
                                            Ö
              = ( [¬𝜑] · 𝑋 ) (𝜎0 ) ·              wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎0 ] ) (𝜎0 )
                                            𝑖=0
              = ( [¬𝜑] · 𝑋 ) (𝜎0 ) ,
which completes this case.

         𝜎1 ∈Σx Φ [𝜎1 ] (0) (𝜎0 ) · 𝑋 (𝜎1 ), we have
For
      Í          𝑘+1

         ∑︁
               Φ𝑘+ 1
                [𝜎1 ] (0) (𝜎0 ) · 𝑋 (𝜎1 )
      𝜎1 ∈Σx
         ∑︁
 =             Φ [𝜎1 ] (Φ𝑘[𝜎1 ] (0)) (𝜎0 ) · 𝑋 (𝜎1 )                                                                    (by definition)
      𝜎1 ∈Σx
         ∑︁                                                                  
 =               [𝜑] (𝜎0 ) · wpJ𝐶 1 K Φ𝑘[𝜎1 ] (0) (𝜎0 ) + ( [¬𝜑] · [𝜎1 ] ) (𝜎0 ) · 𝑋 (𝜎1 )                              (by definition)
      𝜎1 ∈Σx
         ∑︁                                    
 =              [𝜑] (𝜎0 ) · wpJ𝐶 1 K Φ𝑘[𝜎1 ] (0) (𝜎0 ) · 𝑋 (𝜎1 )
      𝜎1 ∈Σx
      + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                          (([¬𝜑] · [𝜎1 ] ) (𝜎0 ) ≠ 0 only if 𝜎0 ∼x 𝜎1 )
                                                                                     !
         ∑︁                       ∑︁
 =              [𝜑] (𝜎0 ) ·               wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) · Φ𝑘[𝜎1 ] (0) (𝜎) · 𝑋 (𝜎1 )
      𝜎1 ∈Σx                      𝜎 ∈Σx
   + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                                                                    (I.H. on 𝐶 1 )
    ∑︁ ∑︁
 =            [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) · Φ𝑘[𝜎1 ] (0) (𝜎) · 𝑋 (𝜎1 )
      𝜎1 ∈Σx 𝜎 ∈Σx
   + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                                                                       (algebra)
   ∑︁ ∑︁
 =            [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) · Φ𝑘[𝜎1 ] (0) (𝜎) · 𝑋 (𝜎1 )
      𝜎 ∈Σx 𝜎1 ∈Σx
      + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                                                                (swap sums)
                                                                                                  !
         ∑︁                                                   ∑︁
 =             [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎] ) (𝜎0 ) ·                   Φ𝑘[𝜎1 ] (0) (𝜎) · 𝑋 (𝜎1 )
      𝜎 ∈Σx                                                  𝜎1 ∈Σx
      + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                                                                    (algebra)

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                      45

      ∑︁
 =            [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎] ) (𝜎0 )
      𝜎 ∈Σx
                                                                   𝑘−2
                                                                                                                               !
                            ∑︁                                     Ö
         · 𝜆𝜎0 .                          ( [¬𝜑] · 𝑋 ) (𝜎𝑘−1 ) ·         wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) (𝜎)
                       𝜎0 ,...,𝜎𝑘−1 ∈Σx                            𝑖=0
   + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                                                                (I.H. on 𝑘)
    ∑︁
 =       [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 )
      𝜎1 ∈Σx
                                                                   𝑘−2
                                                                                                                               !
                            ∑︁                                     Ö
         · 𝜆𝜎0 .                          ( [¬𝜑] · 𝑋 ) (𝜎𝑘−1 ) ·         wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) (𝜎1 )
                       𝜎0 ,...,𝜎𝑘−1 ∈Σx                            𝑖=0
      + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                                                  (rename 𝜎 by 𝜎1 )

       ∑︁
 =             [𝜑] (𝜎0 ) · wpJ𝐶 1 K ( [𝜎1 ] ) (𝜎0 )
      𝜎1 ∈Σx
                                                      𝑘−1
                                                                                                                   !
                  ∑︁                                  Ö
         ·                     ( [¬𝜑] · 𝑋 ) (𝜎𝑘 ) ·         wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
              𝜎1 ,...,𝜎𝑘 ∈Σx                          𝑖=1
      + ( [¬𝜑] · 𝑋 ) (𝜎0 )                                                                     (applying 𝜎1 and index shift)
          ∑︁                                   𝑘−1
                                               Ö
 =                     ( [¬𝜑] · 𝑋 ) (𝜎𝑘 ) ·          wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) .
      𝜎0 ,...,𝜎𝑘 ∈Σx                           𝑖=0
                                                                                          (see reasoning for previous case)
This completes the proof.                                                                                                       □

D.1     Proof of Theorem 10.2
We employ an auxiliary result.
   Lemma D.2. Let 𝐶 ∈ pGCL. Then, for every 𝜎 ∈ Σ, we have
     wpJ𝐶K ( [𝜎] x ) = wpJ𝐶K 𝑥 0 = 𝑥 0′ ∧ . . . ∧ 𝑥𝑛−1 = 𝑥𝑛−
                                                          ′
                                                                ′                      ′
                                                                                                         
                                                             1     𝑥 0 /𝜎 (𝑥 0 ), . . . , 𝑥𝑛−1 /𝜎 (𝑥𝑛−1 ) .

   Proof. By induction on 𝐶.                                                                                                    □

   Since we encode program states 𝜎 as Gödel numbers ⟨𝜎⟩, we define for every 𝑓 ∈ Exp a syn-
tactic expectation Substx [𝑓 , 𝑣] such that Substx [𝑓 , ⟨𝜎⟩] is equivalent to the syntactic expectation
obtained from substituting every 𝑥 ∈ x by 𝜎 (𝑥) in 𝑓 . For that, let 𝑣 0, . . . , 𝑣𝑛−1 be fresh variables not
occurring in 𝑓 . Now define
       Substx [𝑓 , 𝑣]
  ≜ S𝑣 0 : . . . : S𝑣𝑛−1 : [RElem (𝑣, 0, 𝑣 0 ) ∧ . . . ∧ RElem (𝑣, 𝑛 − 1, 𝑣𝑛−1 )] ⊙ 𝑓 [𝑥 0 /𝑣 0, . . . , 𝑥𝑛−1 /𝑣𝑛−1 ] .
   Lemma D.3. For every 𝜎 ∈ Σ and 𝑛𝑢𝑚 = ⟨𝜎⟩, we have
                                     𝑓 [𝑥 0 /𝜎 (𝑥 0 ), . . . , 𝑥𝑛 /𝜎 (𝑥𝑛 )] ≡ Substx [𝑓 , 𝑛𝑢𝑚] .
   Proof. See Appendix D.2.                                                                                                     □

   If FV (𝑓 ) ⊆ x, then substituting every 𝑥 ∈ x by 𝜎 ′ (𝑥) in 𝑓 corresponds to evaluating J𝑓 K in 𝜎 ′:

                                            Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
46                                                                                          Batz, Kaminski, Katoen, and Matheja


     Lemma D.4. If FV (𝑓 ) ⊆ x, then , for all states 𝜎, 𝜎 ′ and every 𝑛𝑢𝑚 = ⟨𝜎 ′⟩, we have
                                                𝜎
                                                    JSubstx [𝑓 , 𝑛𝑢𝑚]K = J𝑓 K (𝜎 ′) .

     Proof. See Appendix D.3.                                                                                                □

  In particular, 𝜎 JSubstx [ℎ, 𝑣]K is independent of 𝜎 since Substx [ℎ, 𝑣] does not contain free pro-
gram variables.

Proof of of Theorem 10.2.
  We prove that


                     wpJwhile ( 𝜑 ) { 𝐶 1 }K J𝑓 K (𝜎)
                                                  

                   = JS𝑙𝑒𝑛𝑔𝑡ℎ : S𝑛𝑢𝑚𝑠 : Sum 𝑣 sum, StateSequencex (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ)
                     𝜎                                                          

                                                                     ⊙ Path [𝑓 ] (𝑙𝑒𝑛𝑔𝑡ℎ, 𝑣 sum ) , 𝑛𝑢𝑚𝑠 K .
                                                                                                        


Assuming that Path satisfies Equations (1) and (2), we have

          JS𝑙𝑒𝑛𝑔𝑡ℎ : S𝑛𝑢𝑚𝑠 : Sum 𝑣 sum, StateSequencex (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ)
      𝜎                                                              

                                         ⊙ Path [𝑓 ] (𝑙𝑒𝑛𝑔𝑡ℎ, 𝑣 sum ) , 𝑛𝑢𝑚𝑠 K
                                                                            
        𝜎 [𝑙𝑒𝑛𝑔𝑡ℎ↦→𝑟 ]
                        JS𝑛𝑢𝑚𝑠 : Sum 𝑣 sum, StateSequencex (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ)
                                                                            
 = sup
                                         ⊙ Path [𝑓 ] (𝑙𝑒𝑛𝑔𝑡ℎ, 𝑣 sum ) , 𝑛𝑢𝑚𝑠 K | 𝑟 ∈ Q ≥0
                                                                            

                                                                                        (by definition)
              S𝑛𝑢𝑚𝑠 : Sum 𝑣 sum, StateSequencex (𝑣 sum, 𝑟 ) ⊙ Path [𝑓 ] (𝑟, 𝑣 sum ) , 𝑛𝑢𝑚𝑠
          𝜎q                                                                             y
 = sup
       𝑟 ∈Q≥0
                                                                                                       (rewrite supremum)
                 ∞
                     𝜎 [𝑣sum ↦→ 𝑗 ] q
                ∑︁
                                         StateSequencex (𝑣 sum, 𝑟 ) ⊙ Path [𝑓 ] (𝑟, 𝑣 sum )
                                                                                           y
 = sup                                                                                                     (by Theorem 9.2)
       𝑟 ∈Q≥0 𝑗=0
                 ∞
                ∑︁
                          StateSequencex ( 𝑗, 𝑟 ) ⊙ Path [𝑓 ] (𝑟, 𝑗)
                   𝜎 q                                             y
 = sup                                                                                                          (Lemma 5.2)
       𝑟 ∈Q≥0 𝑗=0
              ∞
             ∑︁
                        StateSequencex ( 𝑗, 𝑟 ) ⊙ Path [𝑓 ] (𝑘, 𝑗)
                𝜎 q                                              y
 = sup
       𝑘 ∈N 𝑗=0
                                                                           (Path [𝑓 ] (𝑟, 𝑗) = 0, if 𝑟 ∉ N, replace 𝑟 by 𝑘)
                   ∑︁
                                 𝜎
 = sup                               JPath [𝑓 ] (𝑘, 𝑗)K
       𝑘 ∈N 𝑗=⟨𝜎 ,...,𝜎
                  0      𝑘−1 ⟩
            𝜎0 ,...,𝜎𝑘−1 ∈Σx
                 𝜎 0 ∼x 𝜎
                 (for every sequence 𝜎0, . . . , 𝜎𝑘−1 ∈ Σx there is exactly one Gödel number and 𝜎0 ∼x 𝜎)
                   ∑︁                                                     𝑘−2
                                                                          Ö
 = sup                           [𝜎0 ] x (𝜎) · ( [¬𝜑] · J𝑓 K) (𝜎𝑘−1 ) ·         wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
       𝑘 ∈N 𝑗=⟨𝜎 ,...,𝜎                                                   𝑖=0
                  0     𝑘−1 ⟩
            𝜎0 ,...,𝜎𝑘−1 ∈Σx
                                                                      (by Equation (1) and [𝜎0 ] x (𝜎) = 1 iff 𝜎0 ∼x 𝜎)

Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                                      47


                    ∑︁                                                      𝑘−2
                                                                            Ö
 = sup                        [𝜎0 ] x (𝜎) · ( [¬𝜑] · J𝑓 K) (𝜎𝑘−1 ) ·              wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 )
     𝑘 ∈N 𝜎 ,...,𝜎
            0       𝑘−1 ∈Σx                                                 𝑖=0
                                                                                               (product does not depend on 𝑗)
 = wpJwhile ( 𝜑 ) { 𝐶 1 }K J𝑓 K (𝜎) .
                                             
                                                                                                                 (by Theorem 10.1)
It remains to give Path [𝑓 ] (𝑣 1, 𝑣 2 ). By I.H., there is a 𝑔 ∈ Exp with
              wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K 𝑥 0 = 𝑥 0′ ∧ . . . ∧ 𝑥𝑛 = 𝑥𝑛′
                                                                              
                                                                                  = J𝑔K .
Hence, by Lemma D.2, we have for every 𝜎 ∈ Σ:
                wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎] x ) =
                                                                                  q  ′
                                                                                   𝑔 𝑥 0 /𝜎 (𝑥 0 ), . . . , 𝑥𝑛′ /𝜎 (𝑥𝑛 )
                                                                                                                         y
                                                                                                                              (13)
Now define
            Path [𝑓 ] (𝑣 1, 𝑣 2 )
       ≜       [𝑣 1 < 2] · ( S𝑛𝑢𝑚 : [Elem (𝑣 2, 𝑣 1 − 1, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚])
           + [𝑣 1 ≥ 2] · ( S𝑛𝑢𝑚 : [Elem (𝑣 2, 𝑣 1 − 1, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚])
                 ⊙ Product S𝑛𝑢𝑚 1 : S𝑛𝑢𝑚 2 : Elem 𝑣 2, 𝑣 prod, 𝑛𝑢𝑚 1 ∧ Elem 𝑣 2, 𝑣 prod + 1, 𝑛𝑢𝑚 2
                                                                                                 

                     ⊙ Substx [Substx′ [𝑔, 𝑛𝑢𝑚 2 ] , 𝑛𝑢𝑚 1 ] , 𝑣 1 − 2
                                                                       

Here S𝑛𝑢𝑚 : [Elem (𝑣 2, 𝑣 1 − 1, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚] is a shorthand for
            S𝑛𝑢𝑚 : S𝑣 : [𝑣 + 1 = 𝑣 1 ] · [Elem (𝑣 2, 𝑣, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚] .
Similarily, Product 𝑣 prod, . . . , 𝑣 1 − 2 is shorthand for
                                          

                                S𝑣 : [𝑣 + 2 = 𝑣 1 ] · Product 𝑣 prod, . . . , 𝑣 .
                                                                              

We now show that Path [𝑓 ] (𝑣 1, 𝑣 2 ) indeed satisfies the specification from (1) and (2). We distinguish
the following cases:

The case 𝜎 (𝑣 1 ) ∉ N. By Theorem 7.2, we have
                     𝜎
                         JS𝑛𝑢𝑚 : [Elem (𝑣 2, 𝑣 1 − 1, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚]K = 0
                𝜎
and hence JPath [𝑓 ] (𝑣 1, 𝑣 2 )K = 0.

The case 𝜎 (𝑣 1 ) = 0. In this case, we have
                                                      𝜎 [𝑣↦→𝑟 ]
                                                                  J[𝑣 + 1 = 𝑣 1 ]K = 0
                                   𝜎
for all 𝑟 ∈ Q ≥0 and thus JPath [𝑓 ] (𝑣 1, 𝑣 2 )K = 0.

The case 𝜎 (𝑣 1 ) = 1 and 𝜎 (𝑣 2 ) = ⟨(𝜎0 )⟩. We have
           𝜎
               JPath [𝑓 ] (1, ⟨(𝜎0 )⟩)K
      =    𝜎
               JS𝑛𝑢𝑚 : [Elem (⟨(𝜎0 )⟩, 0, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚]K
                                                               ( 𝜎 J[𝑣 1 ≥ 2]K = 0 and 𝜎 J[𝑣 1 < 2]K = 1)
           𝜎
      =        JSubstx [( [¬𝑏] · 𝑓 ), ⟨𝜎0 ⟩]K               ( 𝜎 J[Elem (⟨(𝜎0 )⟩, 0, 𝑛𝑢𝑚)]K = 1 only for 𝜎 (𝑛𝑢𝑚) = ⟨𝜎0 ⟩)
      = J[¬𝑏] · 𝑓 K (𝜎0 )                                                                                           (by Lemma D.4)
                                       𝜎 (𝑣
                                          Ö 1 )−2

      = ( [¬𝑏] · J𝑓 K) (𝜎0 ) ·                      wpJif ( 𝑏 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] ) (𝜎𝑖 ) .
                                         𝑖=0
                                                                                                       (empty product equals 1)

                                         Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
48                                                                                    Batz, Kaminski, Katoen, and Matheja


The case 𝜎 (𝑣 1 ) = 𝑘 ∈ N with 𝑘 ≥ 2 and 𝜎 (𝑣 2 ) = ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩. We have
     𝜎
         JPath [𝑓 ] (𝑘, ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩)K
 = 𝜎 J( S𝑛𝑢𝑚 : [Elem (⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑘 − 1, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚])
       ⊙ Product S𝑛𝑢𝑚 1 : S𝑛𝑢𝑚 2 : [Elem ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑣 prod, 𝑛𝑢𝑚 1
                                                                              

           ∧ Elem ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑣 prod + 1, 𝑛𝑢𝑚 2 ] ⊙ Substx [Substx′ [𝑔, 𝑛𝑢𝑚 2 ] , 𝑛𝑢𝑚 1 ] , 𝑘 − 2 K
                                                                                                           
                                                                 𝜎                      𝜎
                                                                ( J[𝑣 1 ≥ 2]K = 1 and J[𝑣 1 < 2]K = 0)
 = 𝜎 J( S𝑛𝑢𝑚 : [Elem (⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑘 − 1, 𝑛𝑢𝑚)] ⊙ Substx [( [¬𝑏] · 𝑓 ), 𝑛𝑢𝑚]) K
         𝜎                                                                     
       · JProduct S𝑛𝑢𝑚 1 : S𝑛𝑢𝑚 2 : [Elem ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑣 prod, 𝑛𝑢𝑚 1
           ∧ Elem ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑣 prod + 1, 𝑛𝑢𝑚 2 ] ⊙ Substx [Substx′ [𝑔, 𝑛𝑢𝑚 2 ] , 𝑛𝑢𝑚 1 ] , 𝑘 − 2 K
                                                                                                           
                                                                                       (by Theorem 9.5)
 = J[¬𝑏] · 𝑓 K (𝜎𝑘−1 )
           𝜎                                                                       
          · JProduct S𝑛𝑢𝑚 1 : S𝑛𝑢𝑚 2 : [Elem ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑣 prod, 𝑛𝑢𝑚 1
              ∧ Elem ⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑣 prod + 1, 𝑛𝑢𝑚 2 ] ⊙ Substx [Substx′ [𝑔, 𝑛𝑢𝑚 2 ] , 𝑛𝑢𝑚 1 ] , 𝑘 − 2 K
                                                                                                              
                                                                          (see reasoning for previous case)
 = J[¬𝑏] · 𝑓 K (𝜎𝑘−1 )
              𝑘−2
              Ö
                    𝜎
          ·             JS𝑛𝑢𝑚 1 : S𝑛𝑢𝑚 2 : [Elem (⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑖, 𝑛𝑢𝑚 1 )
              𝑖=0
                            ∧ Elem (⟨(𝜎0, . . . , 𝜎𝑘−1 )⟩, 𝑖 + 1, 𝑛𝑢𝑚 2 )] ⊙ Substx [Substx′ [𝑔, 𝑛𝑢𝑚 2 ] , 𝑛𝑢𝑚 1 ]K
                                                                          (by Theorem 9.4 and 𝑘 ≥ 2 by assumption)
 = J[¬𝑏] · 𝑓 K (𝜎𝑘−1 )
              𝑘−2
              Ö
                    𝜎
          ·             JSubstx [Substx′ [𝑔, ⟨𝜎𝑖+1 ⟩] , ⟨𝜎𝑖 ⟩]K
              𝑖=0
                                                 (S quantifiers enforce 𝜎 (𝑛𝑢𝑚 1 ) = ⟨𝜎𝑖 ⟩ and 𝜎 (𝑛𝑢𝑚 2 ) = ⟨𝜎𝑖+1 ⟩)
 = J[¬𝑏] · 𝑓 K (𝜎𝑘−1 )
              𝑘−2
              Ö
                    Substx 𝑔 𝑥 0′ /𝜎𝑖+1 (𝑥 0 ), . . . , 𝑥𝑛′ /𝜎𝑖+1 (𝑥𝑛 ) , ⟨𝜎𝑖 ⟩
                  𝜎q                                                         y
          ·                                                                                           (by Lemma D.3)
              𝑖=0
 = J[¬𝑏] · 𝑓 K (𝜎𝑘−1 )
              𝑘−2
              Ö   q  ′
                   𝑔 𝑥 0 /𝜎𝑖+1 (𝑥 0 ), . . . , 𝑥𝑛′ /𝜎𝑖+1 (𝑥𝑛 ) (𝜎𝑖 )
                                                              y
          ·                                                                                           (by Lemma D.4)
              𝑖=0
 = J[¬𝑏] · 𝑓 K (𝜎𝑘−1 )
              𝑘−2
              Ö
          ·         wpJif ( 𝜑 ) { 𝐶 1 } else { skip }K ( [𝜎𝑖+1 ] x ) (𝜎𝑖 ) ,                         (by Equation 13)
              𝑖=0
which is what we had to show. Hence, we finally obtain
               wpJwhile ( 𝜑 ) { 𝐶 1 }K J𝑓 K
                                            

            = JS𝑙𝑒𝑛𝑔𝑡ℎ : S𝑛𝑢𝑚𝑠 : Sum 𝑣 sum, StateSequencex (𝑣 sum, 𝑙𝑒𝑛𝑔𝑡ℎ)
                                                                         

                                                                   ⊙ Path [𝑓 ] (𝑙𝑒𝑛𝑔𝑡ℎ, 𝑣 sum ) , 𝑛𝑢𝑚𝑠 K .
                                                                                                      


Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
Relatively Complete Verification of Probabilistic Programs                                                             49


This completes the proof.

D.2       Proof of Lemma D.3
   Proof. We have
      Substx′ [𝑓 , 𝑛𝑢𝑚]
 ≡ S𝑣 0 : . . . : S𝑣𝑛−1 : [RElem (𝑛𝑢𝑚, 0, 𝑣 0 ) ∧ . . . ∧ RElem (𝑛𝑢𝑚, 𝑛 − 1, 𝑣𝑛−1 )] ⊙ 𝑓 𝑥 0′ /𝑣 0, . . . , 𝑥𝑛−
                                                                                                             ′
                                                                                                                        
                                                                                                                1 /𝑣 𝑛−1
                                                                                                (by definition)
 ≡ [RElem (𝑛𝑢𝑚, 0, 𝜎 (𝑥 0 )) ∧ . . . ∧ RElem (𝑛𝑢𝑚, 𝑛 − 1, 𝜎 (𝑥𝑛−1 ))] ⊙ 𝑓 𝑥 0 /𝜎 (𝑥 0 ), . . . , 𝑥𝑛−
                                                                                   ′               ′
                                                                                                                   
                                                                                                      1 /𝜎 (𝑥𝑛−1 )
                                              (for 0 ≤ 𝑗 ≤ 𝑛 − 1, RElem (𝑛𝑢𝑚, 𝑗, 𝑚) ≡ 1 only for 𝑚 = 𝜎 (𝑥 𝑗 ))
      ′                     ′
                                            
 ≡ 𝑓 𝑥 0 /𝜎 (𝑥 0 ), . . . , 𝑥𝑛− 1 /𝜎 (𝑥𝑛−1 ) .
                                        ([RElem (𝑛𝑢𝑚, 0, 𝜎 (𝑥 0 )) ∧ . . . ∧ RElem (𝑛𝑢𝑚, 𝑛 − 1, 𝜎 (𝑥𝑛−1 ))] ≡ 1)
                                                                                                               □

D.3       Proof of Lemma D.4
   Proof. We have
      𝜎
          JSubstx [𝑓 , 𝑛𝑢𝑚]K
 =    𝜎
          JS𝑣 0 : . . . : S𝑣𝑛−1 : [RElem (𝑛𝑢𝑚, 0, 𝑣 0 ) ∧ . . . ∧ RElem (𝑛𝑢𝑚, 𝑛 − 1, 𝑣𝑛−1 )] ⊙ 𝑓 [𝑥 0 /𝑣 0, . . . , 𝑥𝑛−1 /𝑣𝑛−1 ]K
                                                                                                (by definition)
 =    𝜎
          J[RElem (𝑛𝑢𝑚, 0, 𝜎 ′ (𝑥 0 )) ∧ . . .q∧ RElem (𝑛𝑢𝑚, 𝑛 −y1, 𝜎 ′ (𝑥𝑛−1 ))] ⊙ 𝑓 [𝑥 0 /𝜎 ′ (𝑥 0 ), . . . , 𝑥𝑛−1 /𝜎 ′ (𝑥𝑛−1 )]K
                   (for 0 ≤ 𝑗 ≤ 𝑛 − 1, RElem 𝑛𝑢𝑚, 𝑗, 𝑣 𝑗 = 1 only for 𝜎 (𝑣 𝑗 ) = 𝜎 ′ (𝑥 𝑗 ), Lemma 5.2)
                                            𝜎                  

 =    𝜎
          J𝑓 [𝑥 0 /𝜎 ′ (𝑥 0 ), . . . , 𝑥𝑛−1 /𝜎 ′ (𝑥𝑛−1 )]K
                                           ([RElem (𝑛𝑢𝑚, 0, 𝜎 ′ (𝑥 0 )) ∧ . . . ∧ RElem (𝑛𝑢𝑚, 𝑛 − 1, 𝜎 ′ (𝑥𝑛−1 ))] ≡ 1)
 = J𝑓 K (𝜎 ′) .                                                       (Vars( J𝑓 K) ⊆ FV (𝑓 ) ⊆ x and Lemma 5.2)
                                                                                                                        □




                                     Proc. ACM Program. Lang., Vol. 1, No. POPL, Article . Publication date: October 2020.
