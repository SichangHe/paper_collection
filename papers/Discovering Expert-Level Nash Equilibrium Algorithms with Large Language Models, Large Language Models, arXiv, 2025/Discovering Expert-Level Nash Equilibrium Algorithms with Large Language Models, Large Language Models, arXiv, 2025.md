                                        Discovering Expert-Level Nash Equilibrium Algorithms with
                                                         Large Language Models

                                                               Hanyu Li* 1 , Dongchen Li*2 , and Xiaotie Deng*1
                                                 1 CFCS, School of Computer Science, Peking University, Beijing, China
                                           2 School of Computing and Data Science, The University of Hong Kong, Pokfulam,
arXiv:2508.11874v2 [cs.GT] 8 Jun 2026




                                                                                    Hong Kong


                                                                                    June 9, 2026



                                                                                       Abstract
                                                 Designing polynomial-time algorithms for approximate Nash equilibria (ANE) with prov-
                                             able worst-case guarantees is a fundamental open problem in algorithmic game theory. While
                                             large language models (LLMs) can generate candidate algorithms at scale, certifying worst-
                                             case guarantees requires formal analysis over all game instances—a task for which no auto-
                                             mated system previously existed. Here, we present LegoNE, a framework encoding expert
                                             proof strategies into a symbolic language that automatically compiles any candidate algorithm
                                             into a ﬁnite optimization problem certifying its worst-case guarantee. Integrating LegoNE
                                             with a reasoning LLM, we rediscovered an algorithm matching the best polynomial-time
                                             guarantee for two-player games, and discovered a three-player algorithm improving the best
                                             guarantee from 0.6 + δ to 0.5 + δ—provably beyond the reach of the extension technique, the
                                             only previously known multi-player ANE design paradigm. These results show that encoding
                                             domain-speciﬁc proof strategies into a machine-tractable language can support LLM-driven
                                             discovery of algorithms outside known human design paradigms.


                                        Introduction
                                        The Nash equilibrium (NE), introduced by Nash in 1951 [1], is a foundational solution concept in
                                        game theory. Computing an NE, however, has proven to be a persistent computational challenge:
                                        all known algorithms, such as the classic Lemke–Howson method [2], require exponential time,
                                        and the celebrated PPAD-completeness results [3, 4] conﬁrmed that this difﬁculty is inherent.
                                        The study of approximate Nash equilibria (ANE) emerged in response: Lipton, Markakis, and
                                        Mehta [5] showed that ϵ-ANE can be computed in quasi-polynomial time for any constant ϵ,
                                        providing the ﬁrst sub-exponential algorithm; this line was further advanced by Babichenko,
                                        Barman, and Peretz [6], who reduced the dependence on the number of players from polynomial
                                        to logarithmic.
                                          * Corresponding authors: lhydave@pku.edu.cn, dongchen.li@connect.hku.hk, xiaotie@pku.edu.cn




                                                                                           1
    Determining the best ϵ achievable in strictly polynomial time—a canonical pursuit in the
theory of approximation algorithms [7, 8]—has been one of the fundamental open questions
in algorithmic game theory [9]. Rubinstein [10] proved that no polynomial-time algorithm can
achieve ϵ-ANE for a sufﬁciently small constant ϵ (ruling out a PTAS), though the hardness con-
stant remains unspeciﬁed and is believed to be very small [11]. For two-player games with
payoffs in [0, 1], a sequence of polynomial-time algorithms improved the worst-case guarantee
from 0.75 [12] to 0.5 [13] to 0.3393 + δ [14]—and then progress stalled for 15 years, until Deligkas,
Fasoulakis, and Markakis [9] achieved 1/3 + δ. Throughout the paper, δ > 0 denotes an arbi-
trarily small constant used in approximation guarantees; guarantees hold for any ﬁxed δ with
running time polynomial in 1/δ. The precise polynomial-time threshold remains unknown, with
a large gap between the best algorithm and the known hardness bound.
    For games with more than two players, progress has been even more limited. The only
known polynomial-time approach is the extension technique [15, 16], which recursively lifts an
r-player algorithm to (r +1) players with guarantee degrading from ϵr to 1/(2 − ϵr ). Applied to
the best two-player result, this yields 0.6 + δ for three-player games and approximately 0.71 + δ
for four-player games, with guarantees approaching 1 as the number of players grows.
    Large language models (LLMs) offer a route to accelerating algorithmic exploration: they can
generate large numbers of candidate algorithms beyond the pace of human researchers. In re-
cent years, combining LLMs with automated evaluators has produced advances across scientiﬁc
domains, from geometry theorem proving [17, 18] to algorithm discovery for matrix multiplica-
tion [19] and combinatorial optimization [20]. Applying this paradigm to ANE algorithm design,
however, requires an automated evaluator that can certify worst-case performance guarantees—
that is, prove that a candidate algorithm produces a valid approximate equilibrium for every
possible game instance. Such automated evaluation requires domain-speciﬁc formal tools: for
Euclidean geometry, mechanized deductive systems have been available for decades [21, 22]; for
ANE algorithm analysis, no comparable automated system previously existed, and proofs have
relied on ad-hoc, paper-by-paper mathematical arguments.
    Here, we present LegoNE, a domain-speciﬁc framework that makes such certiﬁcation auto-
matic for ANE algorithms. LegoNE provides a symbolic language that translates expert proof
strategies from two decades of ANE research into composable building blocks, and an automated
analyzer that compiles any candidate algorithm written in this language into a ﬁnite optimization
problem whose optimal value certiﬁes the algorithm’s worst-case guarantee. The compilation
rests on two principles—instantiation (reducing universal quantiﬁers to a ﬁnite set of concrete con-
straints) and forgetting (abstracting payoff functions into symbolic real variables)—which together
reduce an inﬁnite-dimensional proof obligation to a ﬁxed-size mathematical program solved by
an off-the-shelf solver. Coupled with a reasoning LLM, LegoNE enables an automated discov-
ery loop: the LLM proposes candidate algorithms by composing building blocks, the analyzer
computes a provably correct approximation guarantee and returns it as quantitative feedback,
and the LLM iterates toward better designs. The two components are complementary: the LLM
provides large-scale exploration, and LegoNE provides rigorous, quantitative evaluation.
    Using this framework, we demonstrate two main results. First, the LLM–LegoNE system
rediscovered within two iterations a polynomial-time algorithm matching the best known guar-
antee of 1/3 + δ for two-player games—a result that took human experts 15 years to achieve
from the previous best. Second, the system discovered a three-player algorithm achieving 0.5 + δ,
improving upon the previous best of 0.6 + δ.


                                                 2
    The signiﬁcance of the three-player result extends beyond a numerical improvement. The
extension technique—the only previously known paradigm for multi-player ANE—satisﬁes ϵ3 =
1/(2 − ϵ2 ) [15, 16], where ϵ2 is the two-player guarantee. Achieving ϵ3 ≤ 0.5 via extension would
require ϵ2 = 0—an exact Nash equilibrium, which is PPAD-hard. The discovered algorithm
therefore achieves a guarantee that is provably beyond what the extension technique can deliver
in polynomial time, establishing, to our knowledge, that effective multi-player ANE algorithms
exist outside the extension paradigm.
    These results illustrate how encoding a domain’s proof strategies into a machine-tractable
formal language can support LLM-driven algorithmic discovery. The high-level approach—an
LLM proposes candidates while an automated evaluator provides feedback—is shared with prior
AI-for-science systems [17, 20, 19]; our contribution is the evaluator itself, a formal system for
automated worst-case analysis that did not previously exist for this domain. While LegoNE is
currently speciﬁc to ANE, preliminary extensions to vertex cover approximation and polymatrix
games (see the appendix) suggest that the underlying compilation technique may apply to other
algorithm analysis problems where universal guarantees can be reduced to ﬁnite systems of
algebraic inequalities.


Results
LegoNE Framework
LegoNE is a framework for specifying and automatically certifying algorithms for ϵ-approximate
Nash equilibria (ANE) [23]. An ϵ-ANE is a near-stable strategy proﬁle in which no player has
more than ϵ regret, i.e., none can improve their payoff by more than ϵ via unilateral deviation.
The smaller the worst-case ϵ guaranteed by an algorithm, the better its performance guarantee.
LegoNE provides (i) a specialized symbolic language for composing ANE algorithms from high-
level building blocks, and (ii) an automated analyzer that compiles any such program into a ﬁnite
optimization problem whose solution certiﬁes the algorithm’s performance guarantee.

Language for Algorithm Design. The LegoNE language is a specialized Python-like language
designed to specify ANE algorithms for ﬁxed-number-of-players games. It is based on a compact
set of predeﬁned building blocks derived from established game-theoretic research over the past
two decades. These blocks represent high-level strategic concepts, such as calculating an optimal
counter-move (BestResponse) or mixing existing strategies (UniformMixing).
    This modular approach simpliﬁes algorithm design. For example, the Daskalakis-Mehta-
Papadimitriou (DMP) algorithm [13] can be expressed in just a few lines by composing these
blocks (Figure 1).
    The LegoNE language is highly expressive within its domain, capable of describing a wide
array of building blocks from the literature, ranging from solving linear programming to gradient
descent. Moreover, it supports expressing complex algorithms through arbitrary compositions
of these blocks, allowing for the creation of additional algorithms. This abstraction creates a
structured design space through a programming language. Within the context, an LLM can
learn to explore algorithms by combining these established concepts, rather than reasoning from
scratch.



                                                3
              num_players = 2


              def Random1() -> p1:
                   description = "Random strategy x1 for p1"
                   constraints = []
                   return x1


              def BestResponse1(s2: p2) -> p1:
                   description = "Best response x1 for p1 against s2 of p2"
                   constraints = [
                         forall(s1).(U1(s1,s2)<=U1(x1,s2))
                   ]
                   return x1

              def BestResponse2(s1: p1) -> p2:
                   ...



              def UniformMix1(s1: p1, s2: p1) -> p1:
                  ...


              def algo():
                  i: p1 = Random1()
                  j: p2 = BestResponse2(i)
                  k: p1 = BestResponse1(j)
                   r1: p1 = UniformMix1(i, k)
                   return r1, j


Figure 1: The LegoNE code of the DMP algorithm. The language uses simple, high-level
building blocks encapsulating core game-theoretic concepts. Here we deﬁne building blocks
BestResponse1, which computes the best response x1 of player 1 (p1) against strategy s2 of
player 2 (p2), Random1, which randomly produces a strategy for player 1 (p1), and so on. Then we
deﬁne the DMP algorithm, which combines these blocks and ﬁnally returns the strategy proﬁle
r1, r2 for both players.




                                               4
Automated Analyzer: From Code to Proof. A key component of LegoNE is its automated an-
alyzer, which transforms algorithm analysis into a systematic machine-driven process. For any
algorithm expressed in the LegoNE language, the analyzer computes its best possible approxi-
mation guarantee, ϵ, and simultaneously generates a computer proof of this guarantee. This is
achieved through a two-step abstraction that reduces the original inﬁnite-dimensional problem
which states a guarantee for all possible games to a ﬁnite, solvable math program. An overview
of this process is illustrated in Figure 2.
    The process begins by translating the procedural code of an algorithm into a set of declarative
logical properties based on Floyd-Hoare semantics [24, 25]. During the process, each line of the
code is encoded as a mathematical statement. For instance, the instruction

                                        k = BestResponse1(j)

becomes a universal assertion: “Given that player 2 plays strategy j, for all possible strategies
player 1 could choose, none yields a higher payoff than strategy k.” More formally, this can be
expressed as a logical statement as follows:

                                        ∀s1 , u1 (s1 , j) ≤ u1 (k, j),                             (1)

where u1 (s1 , j) is the payoff for player 1 when playing strategy s1 against player 2’s strategy j.
This statement asserts that for all possible strategies s1 available to player 1, none yields a higher
payoff than strategy k when player 2 plays strategy j. Aggregating these properties for all lines
of code creates a complete series of logical properties of the algorithm.
    Because this speciﬁcation ranges over inﬁnite-dimensional spaces (the set of all strategies and
payoff functions), direct computation is intractable; the core difﬁculty is universal quantiﬁcation
(e.g., ∀s1 over all strategies). LegoNE addresses this via a two-step process: instantiation and
forgetting.

   1. Instantiation: From Inﬁnite to Finite. The analyzer instantiates the logical properties only
      for the ﬁnite set of strategies explicitly constructed within the algorithm. This is based on
      the insight from human proofs that an algorithm’s properties need only be veriﬁed for the
      strategies it generates. For example, to analyze the line

                                           k = BestResponse1(j),

     which corresponds to the property ∀s1 , u1 (s1 , j) ≤ u1 (k, j), the analyzer instantiates the
     universal quantiﬁer ∀s1 with exactly the strategies for player 1 used in the DMP algorithm
     (Figure 1): i, k, and r1. This substitution yields a ﬁnite set of inequalities involving only
     the strategies that the algorithm actually constructs:

        • u1 (i, j) ≤ u1 (k, j)
        • u1 (k, j) ≤ u1 (k, j) (which is trivially true)
        • u1 (r1 , j) ≤ u1 (k, j)

     This step reduces the inﬁnite set of quantiﬁers to a ﬁnite number of instantiated constraints.




                                                      5
                         !" #$ !%&

                           Random1                     def BestResponse1(s2: p2) -> p1:
                                                           constraints = [
                        BestResponse1
                                                           ]
                                                           return y1
                         UniformMix1


                        BestResponse2


       !$' "( #  #                           ! !$ #" #$&

        def algo():
             i: p1 = Random1()
             j: p2 = BestResponse2(i)
             k: p1 = BestResponse1(j)
             r1: p1 = UniformMix1(i, k)
             return r1, j




     " #&#  #                                           # ('$ #$




                                         

                                 $ &!) #$  * #

Figure 2: The LegoNE analyzer process. a, The analyzer reads all building blocks, which de-
scribe their mathematical properties. b, The analyzer then reads the algorithm code, which is
composed of these building blocks. c, The analyzer translates the algorithm code into logical
encodings of the algorithm’s properties and the proof goal for approximation analysis. d, The
analyzer instantiates the logical properties for the ﬁnite set of strategies constructed by the al-
gorithm. e, The analyzer then “forgets” the underlying structure of the payoff functions and
encodes the properties as a ﬁnite set of algebraic inequalities over real variables a1 , a2 , a3 , . . . . f,
Finally, the analyzer formulates a constrained optimization problem to ﬁnd the tightest possible
ϵ subject to these inequalities and solves it using an external solver, like Mathematica.


                                                      6
   2. Forgetting: From Functions to Variables. Although the number of constraints is now
      ﬁnite, terms like u1 (i, j) still depend on unknown payoff functions from arbitrary games.
      To address this second source of inﬁnitude, the analyzer treats each payoff value, such
      as u1 (i, j), as a single symbolic real variable, denoted v1,ij . This forgets the underlying
      structure of the function u1 . The inequality u1 (i, j) ≤ u1 (k, j) is thus transformed into a
      simple algebraic relationship between two variables: v1,i,j ≤ v1,k,j .
    Through this two-step process, the initial assertion over inﬁnite-dimensional functions is con-
verted into a ﬁnite system of algebraic inequalities over a set of real variables. This system is then
formulated as a constrained optimization problem: ﬁnd the minimum possible ϵ — an expres-
sion also formulated using these new variables — subject to the derived system of inequalities.
The optimal value, found by an external solver, is the tightest possible worst-case approximation
guarantee, ϵ. The solution to this optimization problem constitutes a constructive proof of the
algorithm’s performance guarantee. Within the LegoNE framework, computing the guarantee is
equivalent to proving it.

Empirical Validation. To verify the correctness of the LegoNE analyzer, we implemented all
known polynomial-time ANE algorithms for ﬁxed-number-of-players games from the literature
in LegoNE language. This includes a series of works published over more than two decades.
The literature on ANE algorithms has focused almost exclusively on two-player games. For
games with more than two players, the only established design paradigm is to extend two-player
algorithms. We also implemented the three-player algorithm derived from this paradigm.
    The result is shown in Table 1. For each algorithm, the LegoNE analyzer managed to com-
pute the approximation guarantee matching the results from the original papers up to a 10−5
precision. The original proofs for these algorithms required from a few to over a dozen pages of
mathematical arguments. In LegoNE, each algorithm was expressed within 60 lines of code. The
automated computation of the approximation guarantee for each was completed within 80 sec-
onds for all algorithms, a task that had previously required years of cumulative human research.
These results conﬁrmed the correctness of the framework and showed its potential to accelerate
theoretical research by efﬁciently identifying correct approximation guarantees. See Table 2 for
the detailed experimental results.

Extending the Framework. The framework’s core principles, instantiation and forgetting, ex-
tend beyond the analysis of ﬁxed-number-of-players games. We have applied the framework to
analyze algorithms for two broader classes of problems, demonstrating its generality. See the
appendix for details.
    First, we analyzed algorithms for approximate Nash equilibrium in polymatrix games [28].
Unlike standard games with a ﬁxed number of players, polymatrix games model interactions in
large networks where each player’s payoff is determined only by their neighbors in a given graph.
The challenge is to reason about an arbitrary number of players. We applied our framework to
the only known polynomial-time ANE algorithm for polymatrix games from the literature. Our
framework handles the analysis by using the forgetting principle to abstract away player-speciﬁc
indices, allowing for a uniﬁed analysis that automatically proves the algorithm’s approximation
guarantee.
    Second, we extended the framework to analyze a broad class of approximation algorithms
based on linear programming (LP) relaxation and rounding [8]. As a classic example of this

                                                  7
                                           Guarantee proved in      Guarantee proved
               Author initials, year
                                             original paper           by LegoNE
                 KPS [12], 2006                     0.75                   0.75000
                DMP [13], 2006                      0.5                    0.50000
                DMP [26], 2006                 0.38197 + δ†              0.38197 + δ
               BBM-1 [15], 2007                   0.38197                  0.38197
               CDFFJS [27], 2016                  0.38197                  0.38197
               BBM-2 [15], 2007                   0.36392                  0.36392
                 TS [14], 2007                 0.33933 + δ               0.33933 + δ
                 DFM [9], 2022                    1/3 + δ                0.33333 + δ
            DFM+extension (3-player)
                                                  0.6 + δ                0.60000 + δ
                [9, 15, 16], 2022

Table 1: Benchmark of LegoNE on existing algorithms. The table summarizes the approxima-
tion guarantees proved by LegoNE for each algorithm, compared to the guarantees proven in the
original papers. The results match exactly, demonstrating the framework’s correctness and effec-
tiveness in automating algorithm analysis. † Throughout the paper, δ > 0 denotes an arbitrarily
small constant used in approximation guarantees; guarantees hold for any ﬁxed δ with running
time polynomial in 1/δ.




                                       Guarantee proved
          Author initials, year                             Code lines     Running time (s)
                                         by LegoNE
            KPS [12], 2006                  0.75000            27                22.55
           DMP [13], 2006                   0.50000            42                 4.31
           DMP [26], 2006                 0.38197 + δ          38                31.13
          BBM-1 [15], 2007                  0.38197            46                11.81
          CDFFJS [27], 2016                 0.38197            48                65.87
          BBM-2 [15], 2007                  0.36392            —                  1.38
            TS [14], 2007                 0.33933 + δ          31                13.90
            DFM [9], 2022                 0.33333 + δ          52                79.63
       DFM+extension (3-player)
                                          0.60000 + δ          50                8.34
           [9, 15, 16], 2022

Table 2: Detailed benchmark of LegoNE on existing algorithms. This table shows the lines of
code and running time for each algorithm. The code lines include deﬁning all used building
blocks, inherent constraints, and the algorithm deﬁnition. The guarantees computed by LegoNE
are also listed for reference.




                                                 8
                                                                                   LegoNE analyzer




                                                                    feedback
                                                        
                                          ( ✗ invalid syntax at ... )

                            building blocks

                                                                                                  algorithm




         human experts                                                                        algorithm
                                                      controller
                               guidance

                                                            
                                              ( ✗ invalid syntax at ... )

                                                                        feedback            LLM

Figure 3: The human-machine collaborative loop for algorithm discovery. Human experts
provide high-level building blocks and design guidance. The LLM then proposes a candidate
algorithm by combining these blocks. The LegoNE analyzer automatically computes a proven
approximation guarantee and returns it as feedback; if the algorithm has a syntax error, the
analyzer will output the speciﬁc error message to the LLM. The loop iterates, allowing the LLM
to reﬁne its designs based on rigorous theoretical feedback.


method, we analyzed an algorithm for the vertex cover problem, a fundamental challenge in
computer science. The analysis involves translating the algorithm — which solves a relaxed
version of the problem and rounds the solution — into our framework. The analyzer then auto-
matically proves the algorithm’s approximation ratio of 2, matching the known result from the
literature. These applications show that the framework can potentially serve as a general tool for
automated algorithm analysis across a broader range of computational problems.

LLM-Powered Algorithmic Discovery
We further integrate LegoNE with an LLM to automate algorithmic discovery (Figure 3).
    In this paradigm, human experts and LLMs have different roles based on their complemen-
tary strengths. The human expert provides the fundamental components for algorithm design,
translating domain-speciﬁc knowledge and high-level proof strategies into the building blocks of
the LegoNE language. This task requires a level of conceptual understanding not yet achievable
by LLMs. The LLM, in turn, navigates the vast combinatorial space of how these blocks can be
assembled, exploring potential algorithms at a scale and speed difﬁcult for human researchers
alone.
    The learning process in this framework is useful for two reasons. First, the building blocks
provide a high-level speciﬁcation of the design space, making it tractable for the LLM. Second,


                                                            9
the LegoNE analyzer provides rapid, rigorous feedback by computing a provably correct approxi-
mation guarantee for any proposed algorithm. This iterative process of proposing, verifying, and
reﬁning allows for efﬁcient exploration of the algorithm design space. An interaction controller
manages this process, using carefully designed prompts from human experts’ design experience
and insights to guide the LLM toward promising areas of the design space while still encourag-
ing the generation of diverse solutions. Importantly, this feedback is not evaluated on particular
game instances: the analyzer returns an approximation guarantee that holds for all game in-
stances.

Reproducing Best Polynomial-Time Worst-Case Guarantees. To validate the framework, we
ﬁrst tasked it with rediscovering a known result in ANE research. In an experiment conﬁgured
for two-player games, a reasoning LLM [29] was provided only with the building blocks avail-
able in the literature prior to 2007, when the best polynomial-time worst-case guarantee at the
time [14] was obtained. After 2 rounds of interaction with the LegoNE analyzer, the LLM con-
structed an algorithm. Although structurally different from the 2022 reﬁnement achieving the
current best polynomial-time worst-case guarantee [9], LegoNE proved it achieved the same ap-
proximation guarantee. This result, which required 15 years of cumulative research by human
experts, indicates the framework’s potential to accelerate the process of generating and validating
theoretical ideas.

Discovering Multi-Player Algorithms. We applied the framework to three-player games, a set-
ting where human-designed methods have seen limited progress. Prior work typically relies on
an extension technique that adapts two-player algorithms [15, 16]; this approach is restrictive
and often yields weaker guarantees. Figure 4 illustrates the three-player polynomial-time base-
line that, prior to our work, achieved the best polynomial-time worst-case guarantee, constructed
using the extension technique over the DFM algorithm [9].
    Using the LLM-LegoNE system, we discovered in 11 rounds a fundamentally different algo-
rithm (Figure 5) whose LegoNE analysis proves an approximation guarantee of 0.5 + δ, improv-
ing on the previously best 0.6 + δ polynomial-time worst-case guarantee.
    The central building block in Figure 5 is StationaryPoint3. Intuitively, it ﬁxes player 3’s
mixed strategy z and performs a gradient descent procedure using linear programming to ﬁnd a
stationary point ( xs , ys ) that locally minimizes the maximum regrets of players 1 and 2, associated
with dual strategies (w, zdual ).
    Beyond this numerical improvement, the discovery represents a departure from the only
previously known design paradigm for multi-player ANE. The extension technique satisﬁes ϵ3 =
1/(2 − ϵ2 ) [15, 16]; achieving ϵ3 ≤ 0.5 via extension would require ϵ2 = 0—an exact Nash
equilibrium, which is PPAD-hard. The discovered algorithm therefore achieves a guarantee that
no extension-based construction can deliver in polynomial time. Structurally, while extension-
technique constructions use a best-response-then-mix approach as the ﬁnal step, the discovered
algorithm uses a different composition of building blocks, combining BestResponse, EqMix, and
OptimalMixing.
    Across 12 rounds, the LLM produced 7 distinct algorithms; only the ﬁrst relied on the exten-
sion technique, while the remaining 6 explored alternative non-extension structures that nonethe-
less achieved nontrivial guarantees. The expert knowledge provided to the LLM consists of the
building blocks themselves (standard game-theoretic operations drawn from the ANE literature,


                                                 10
     def algo():
         z: p3 = Random3()
         x: p1, y: p2 = DFM(z)
         z_br: p3 = BestResponse3(x, y)
              z_mix: p3 = 0.6 * z + 0.4 * z_br
              return x, y, z_mix

Figure 4: An extension-technique three-player ANE algorithm (baseline). This construction
treats the best two-player polynomial-time NE algorithm as a black-box component and extends it
to three-player games, yielding the previously best 0.6 + δ polynomial-time worst-case guarantee.




def algo():
      z = Random3()
      xs, ys, w, z_dual = StationaryPoint3(z)
      x_mix = EqMix1(xs, w)
      y_mix = EqMix2(ys, z_dual)
      z_br = BestResponse3(x_mix, y_mix)
      z_mix = EqMix3(z, z_br)
      o1, o2, o3 = OptimalMixing(xs, w, x_mix, ys, z_dual, y_mix, z,
                                             z_br, z_mix)
      return o1, o2, o3

Figure 5: A three-player ANE algorithm discovered by the LLM. This algorithm combines build-
ing blocks such as StationaryPoint3 and OptimalMixing in a distinctive structure. The LegoNE
framework proves an approximation guarantee of 0.5 + δ, improving upon the previously best
0.6 + δ polynomial-time worst-case guarantee.




                                               11
such as BestResponse, StationaryPoint, and OptimalMixing) and prompt-level constraints that
deﬁne the search space—but not the algorithmic structure, composition order, or mixing coef-
ﬁcients. In these runs, the extension technique was available as a possible component, yet the
LLM generated non-extension approaches. The structure of the ﬁnal 0.5 + δ algorithm was not
anticipated by the human experts who designed the building blocks. A detailed inventory of the
expert inputs is provided in the Methods (Section B.1).


Discussion
This work presents LegoNE, a domain-speciﬁc formal system that automates the analysis of
approximate Nash equilibrium algorithms, and demonstrates its integration with an LLM to form
an automated discovery loop. The LegoNE analyzer—built on the instantiation and forgetting
principles—compiles any candidate algorithm expressed in the LegoNE language into a ﬁnite
optimization problem whose solution certiﬁes the algorithm’s worst-case guarantee. Coupled
with a reasoning LLM, this loop reproduced the best polynomial-time worst-case guarantee for
two-player games within two iterations and discovered a three-player algorithm that improves
upon the previous best guarantee from 0.6 + δ to 0.5 + δ.
    The three-player result has implications beyond the speciﬁc approximation constant. The
extension technique [15, 16]—previously the only known paradigm for designing multi-player
ANE algorithms—satisﬁes ϵ3 = 1/(2 − ϵ2 ); achieving ϵ3 ≤ 0.5 via extension would require
an exact Nash equilibrium algorithm, a PPAD-hard task. The discovered algorithm therefore
establishes, to our knowledge, that effective polynomial-time multi-player ANE algorithms exist
outside the extension paradigm. This opens a design space for multi-player algorithms and
contributes to narrowing the gap between the best known polynomial-time guarantees and the
hardness lower bounds—a gap that remains large and largely uncharacterized for both two-
player and multi-player settings.
    Our progress should be read as both a positive result and a boundary marker. LegoNE
currently depends on human-curated building blocks that encode proof strategies from the ex-
isting literature; it cannot discover fundamentally different proof techniques. The framework’s
scope is limited to algorithm analysis problems where the instantiation and forgetting princi-
ples apply—settings where universal guarantees can be reduced to ﬁnite systems of algebraic
inequalities. Our preliminary extensions to vertex cover approximation and polymatrix games
(see the appendix) suggest this class is nontrivial, but its exact boundaries remain to be charac-
terized. Looking ahead, we hope to develop more expressive languages that allow algorithms to
be analyzed from ﬁrst principles, reducing the dependence on hand-curated building blocks and
broadening the range of problems amenable to automated analysis.




                                               12
Methods

The LegoNE Framework in Detail
Background: Approximate Nash Equilibrium (ANE)
In a normal-form game, multiple players select actions from their respective action spaces. Play-
ers can choose mixed strategies, which are probability distributions over their available actions,
and they subsequently receive expected payoffs. Suppose there are r players, with r ﬁxed. A
strategy proﬁle, denoted by x = ( x1 , . . . , xr ), is a collection of all players’ strategies. Each player i
has a payoff function, ui ( x), which represents their expected utility under a given strategy proﬁle
x. Following the standard convention for approximation guarantees, these payoffs are normal-
ized to the range [0, 1] [12]. A central concept in game theory is the Nash equilibrium (NE), a
strategy proﬁle where no single player can gain a better payoff by unilaterally changing their
strategy. The existence of at least one NE is guaranteed in any ﬁnite game [1, 30].
    While the concept of NE is fundamental, the focus of modern algorithmic game theory often
shifts to the notion of an approximate Nash equilibrium (ANE) [23], which relaxes the strict optimal-
ity condition of an NE. The regret for player i under a strategy proﬁle x, denoted f i ( x), measures
the maximum payoff increase they could achieve by deviating to a different strategy. Formally,
this regret is deﬁned as:
                                    f i ( x) := max ui ( x̃i , x−i ) − ui ( x).                            (2)
                                              x̃i ∈∆ni

Here, x−i represents the strategies of all players except player i. For any non-negative value ϵ,
a strategy proﬁle x is termed an ϵ-approximate Nash equilibrium (ϵ-NE) if the maximum regret
among all players does not exceed ϵ; that is, if f ( x) := maxi∈[r] f i ( x) ≤ ϵ. A perfect Nash
equilibrium corresponds to the case where ϵ = 0.
    When we say an algorithm has an approximation guarantee of b, we mean that it produces
a strategy proﬁle x such that f ( x) ≤ b for any game instance. Consequently, the objective for
designing an ANE algorithm is to create a polynomial-time process whose resulting strategy
proﬁle x consistently ensures a small f ( x) value for any game instance. We focus on algorithms
for a ﬁxed number r of players.

The LegoNE Language
The LegoNE framework introduces a domain-speciﬁc programming language that shifts the
paradigm from describing an algorithm’s execution steps (its operational semantics [31]) to specify-
ing its mathematical properties (its axiomatic semantics [24, 25]). This methodology is inspired by
Floyd-Hoare logic [24, 25], and facilitates a human-machine collaboration where human design-
ers encode their insights about algorithmic components into logical formulas, which machines
then use as axioms for further analysis.
    An algorithm is constructed by ﬁrst deﬁning fundamental building blocks and then compos-
ing them in sequence. Consider the Daskalakis-Mehta-Papadimitriou (DMP) algorithm [13] for
2-player games. Its building blocks include operations like BestResponse, which ﬁnds an opti-
mal strategy against an opponent (e.g., j = BestResponse(i )), and UniformMixing, which creates
an equal-probability mixture of two strategies (e.g., r1 = UniformMixing (i, k)). Although these
examples are simple, the LegoNE language is highly expressive within its domain, capable of

                                                         13
describing a wide array of building blocks from the literature, ranging from solving linear pro-
gramming to gradient descent.
    The core of LegoNE is that each such building block is encoded by a logic formula that
captures its guaranteed properties. For instance, the BestResponse operation j = BestResponse(i )
for player 2 is not described by how to compute it, but by the logical assertion that it produces a
payoff at least as high as any other possible strategy y:

                                               ∀y(u2 (i, y) ≤ u2 (i, j)).                                         (3)

Similarly, the UniformMixing block is encoded with formulas specifying its linear behavior on
payoffs, such as ∀y(u1 (r1 , y) = u1 (i, y)/2 + u1 (k, y)/2).
    The logical encoding for an entire algorithm, ϕ[Γ], is the conjunction of the formulas for each
of its steps, along with a set of predeﬁned inherent formulas, ϕ0 . These inherent formulas state
fundamental truths, such as the deﬁnition of regret and the fact that all payoffs are bounded
within [0, 1]. The objective of proving that algorithm Γ has an approximation guarantee of ϵ is
then stated as a single, comprehensive logical implication:

                             (∀u1 , . . . , ur )(∀s11 , . . . )(ϕ[Γ] → f (s1 , . . . , sr ) ≤ ϵ).                 (4)

This formula asserts that for any valid game, if the properties guaranteed by the algorithm’s steps
hold, then its output’s f value is necessarily bounded by ϵ; thus, the approximation guarantee of
this algorithm is ϵ.

The LegoNE Analyzer
The central challenge in formally analyzing an ANE algorithm lies in handling objects of un-
bounded dimensionality. An algorithm’s approximation guarantee must hold true for any game.
This implies it must be valid for payoff matrices of any arbitrary size and for an inﬁnite contin-
uum of possible mixed strategies within the corresponding simplexes. This universal-quantiﬁcation
nature of the proof goal makes direct computational veriﬁcation intractable.
    To overcome this fundamental obstacle, the LegoNE analyzer introduces a two-step proce-
dure that systematically translates the abstract, inﬁnite-dimensional proof task into a concrete,
ﬁxed-size constrained optimization problem. This procedure is inspired by how human experts
construct proofs: by separating the properties of the algorithm from the general properties of
real arithmetic. The core of our automated analysis rests on two principles: instantiation and
forgetting.

The Instantiation Principle: From Inﬁnite Quantiﬁers to Finite Constraints. LegoNE’s ﬁrst
key tactic, instantiation, translates the universally quantiﬁed properties of an algorithm into
a ﬁnite set of concrete algebraic inequalities. A human proof does not reason about all in-
ﬁnitely many strategies; instead, it cleverly selects a few crucial instances to build its argu-
ment. For example, a building block like xk = BestResponse( x j ) is deﬁned by the property
∀ x(u1 ( x, x j ) ≤ u1 ( xk , x j )). The analyzer automates the human-like instantiation process by sys-
tematically substituting the universally quantiﬁed variable (here, ∀ x) with all other speciﬁc strat-
egy variables that appear in the algorithm’s code.
    Furthermore, it instantiates universally quantiﬁed variables using a strategy that maximizes
the payoff. For example, from ∀ x(u1 ( x, x j ) ≤ u1 ( xk , x j )) we can derive maxx u1 ( x, x j ) ≤ u1 ( xk , x j ).

                                                             14
This allows it to derive a crucial identity, for instance, maxx u1 ( x, x j ) = u1 ( xk , x j ), by combining
the derived inequality maxx u1 ( x, x j ) ≤ u1 ( xk , x j ) with the inherent property from the deﬁnition
of the maximum operator, maxx u1 ( x, x j ) ≥ u1 ( xk , x j ). By applying this instantiation procedure
to every logical formula describing the algorithm, LegoNE transforms the problem from one of
inﬁnite logical deduction to one of satisfying a ﬁnite system of inequalities involving a limited
number of strategy-dependent terms.

The Forgetting Principle: From Function Spaces to Real Variables. After instantiation, the
problem is reduced to a system of inequalities involving terms like u1 ( xi , x j ), u1 ( xk , x j ), and
maxx u1 ( x, x j ). These terms are still, in principle, complex, high-dimensional payoff functions.
The second key tactic, forgetting, is based on the insight that a formal proof only uses the arith-
metic relationships between these terms, not their underlying functional structure.
    Therefore, the analyzer forgets their origin. It treats each unique term, such as u1 ( xi , x j ),
as a single, abstract real-valued variable, for example, a1 . The term u1 ( xk , x j ) becomes a2 ,
maxx u1 ( x, x j ) becomes a3 , and so on for all terms present in the instantiated formula. The origi-
nal system of inequalities is thus rewritten purely in terms of these new real variables. This cru-
cial step maps the problem from an intractable function space into a standard, ﬁnite-dimensional
real vector space, where only the core arithmetic properties that are essential for the proof are
preserved.

The End Product: A Constrained Optimization Problem. The culmination of the instantiation
and forgetting principles is the automatic compilation of any algorithm written in LegoNE into
the following form:
                          ∀ a1 , a2 , . . . ( ϕ 0 ( a1 , a2 , . . . ) → g ( a1 , a2 , . . . ) ≤ ϵ ), (5)
where ϕ0 ( a1 , a2 , . . . ) is a set of inequalities derived from the algorithm’s properties, and function
g( a1 , a2 , . . . ) represents the original function f ( x), now expressed in terms of the abstract vari-
ables a1 , a2 , . . . . The goal is to ﬁnd the minimum value of ϵ such that the implication holds for
all possible values of the abstract variables. This is equivalent to ﬁnding the maximum value of
g( a1 , a2 , . . . ) subject to the constraints ϕ0 ( a1 , a2 , . . . ). The formulation is as follows:

                                        maximize        g ( a1 , a2 , . . . )
                                          a1 ,a2 ,...
                                                                                                          (6)
                                        subject to      ϕ 0 ( a1 , a2 , . . . ).

The optimal value of this ﬁxed-size optimization problem is precisely the best approximation
guarantee for the given algorithm that can be derived via this proof tactic. Crucially, the number
of variables and constraints of this optimization problem is ﬁxed once the tactic is ﬁxed and does
not scale with the size of the game instance. This ﬁnal problem is a ﬁxed-size program that can
be solved by off-the-shelf numerical solvers, such as Gurobi [32] or Mathematica [33].

Benchmarking LegoNE on Existing Human-Designed Algorithms
To validate the correctness and analytical power of the LegoNE framework, we benchmarked it
against the existing human-designed ANE algorithms from the literature. The framework’s com-
piler was implemented in C++ using the lexer Flex [34] and parser Bison [35], with Mathematica
serving as the external optimization solver. The version of Wolfram Engine inside Mathematica

                                                        15
is 14.2. We set the Mathematica parameters as follows: AccuracyGoal to 10, WorkingPrecision
to 20, and MaxIterations to 2000. We use the default method (auto) as the optimization method.
To ensure a reproducible result, we rerun the same optimization on a MacBook and a Windows
PC. For testing the running time, we used a MacBook Pro 14 (M4 chip, 10-core CPU/10-core
GPU, 16GB RAM). Each optimization was executed 5 times under identical conditions.
    Most existing polynomial-time ANE algorithms have been designed for two-player games.
We encoded all major algorithms from the literature in the LegoNE language, including com-
plex ones like the Tsaknakis-Spirakis algorithm. This process demonstrated LegoNE’s ability to
express sophisticated algorithmic components, such as branching operations, mixing strategies
with payoff-dependent coefﬁcients, and the intricate StationaryPoint building block.
    For computational efﬁciency and due to current limitations of the LegoNE compiler, we
set special parameters for some algorithms. The LegoNE compiler does not currently support
branching operations; however, due to symmetry of the algorithm, it is sufﬁcient to encode one
branch. For BBM-1 [15] with 0.36 approximation guarantee, the LegoNE compiler does not
currently support square root operations, so we manually compute the compiler output. For
KPS [12] with 0.75 approximation guarantee and DMP [26] with 0.38 approximation guarantee,
we manually provide the diagonal logic encoding (see the appendix remark on optimal mixing
for two-player games) for the optimal mixing operation to follow the original proof.
    As summarized in Tables 1 and 2, the approximation guarantees computed and proven by
LegoNE for each algorithm are identical (up to 10−5 precision) to the guarantees proven in the
original papers.
    To further demonstrate the framework’s expressive power, we modeled the only established
paradigm for designing three-player ANE algorithms in the literature: the extension technique [15,
16]. This method takes an existing algorithm Γ that computes an α-NE for two-player games and
extends it to create an algorithm for three-player games. Prior to our work, the best human-
designed polynomial-time worst-case guarantee for three-player games was obtained by extend-
ing the (1/3 + δ)-NE two-player algorithm [9], which yields a (0.6 + δ)-NE. We modeled this in
LegoNE by treating the two-player algorithm Γ as a single, black-box building block whose encod-
ing is its proven guarantee (e.g., f ( x1o , x2o ) ≤ 0.6 + δ). When analyzing the complete three-player
algorithm, LegoNE correctly computed the approximation guarantee to be (0.6 + δ), matching
the result proven in the literature.


Experimental Details for Automated Algorithmic Discovery
Human-Machine Interaction Loop and Engineering Considerations
Our automated discovery process is centered on an iterative interaction loop between a Large
Language Model (LLM) and the LegoNE framework. This approach is founded on a human-
machine collaboration paradigm where humans establish the high-level theoretical framework,
and the machine explores the vast algorithmic design space within it. The process separates
the deﬁnition of foundational building blocks from the task of combining them into a complete
algorithm. Deﬁning additional building blocks requires deep domain expertise and complex
mathematical derivations, a role reserved for human experts. In contrast, the task of combining
these predeﬁned blocks is a more structured, mechanical process that is well-suited for automa-
tion by an LLM. This automation is feasible due to two key factors: the design space is signiﬁ-


                                                  16
cantly condensed by using complex, pre-deﬁned blocks that encapsulate human insights, and the
LegoNE compiler provides immediate feedback by automatically computing the approximation
guarantee for any valid combination.
   To make this exploration process efﬁcient and robust, we implemented several engineering
choices:

Auto-return with Optimal Mixing In the literature of ANE algorithms, a particularly complex
step is determining the appropriate coefﬁcients for mixing constructed strategies to achieve a
small approximation guarantee. This task is challenging for LLMs. To simplify the task, we
modiﬁed the LegoNE compiler to automatically apply optimal mixing operations as the ﬁnal step
of any given algorithm fragment. This enhancement allows the LLM to focus on constructing
effective strategies, while the compiler handles the optimal mixing.

Prompt Engineering We designed a multi-stage prompting strategy to guide the LLM.

   • Initial Prompt: The ﬁrst prompt provides a clear and constrained starting point for the
     LLM. It includes: (1) a clear description of the task, with the primary goal of minimizing
     the approximation guarantee ϵ; (2) strict design constraints, such as the mandatory use of
     static single assignments (SSA), type annotations, a no-return statement requirement, and
     the compulsory inclusion of at least one StationaryPoint building block due to its proven
     effectiveness from human experts’ experience; and (3) concrete examples of both valid and
     invalid code snippets to help the LLM understand the expected format and constraints.

   • Iterative Feedback Prompts: Subsequent prompts are dynamically adjusted based on the
     LLM’s previous output. If the previous algorithm was invalid, the new prompt includes de-
     tailed compiler error messages, highlighting speciﬁc issues like type mismatches, incorrect
     usage of building blocks, or violations of SSA rules. The LLM is then instructed to carefully
     review and correct these errors. If the algorithm was valid, the prompt focuses on optimiza-
     tion. It provides the current best approximation guarantee ϵ and encourages the LLM to
     achieve a smaller value. Speciﬁcally, the prompt guides the LLM to: leverage more com-
     plex building blocks; break symmetry by applying different blocks to each player; explore
     alternative combinations to avoid local optima; and adhere to Occam’s Razor by preferring
     simpler strategies that achieve comparable or better results.

Expert Knowledge Inventory To enable assessment of whether the expert-provided knowledge
may have biased the LLM toward the discovered solutions, we provide a detailed accounting of
all expert inputs.
    The building blocks provided to the LLM encode standard game-theoretic operations drawn
from the ANE literature:

   • BestResponse: computes an optimal response to an opponent’s strategy (basic game-theoretic
     concept);

   • Random: generates an arbitrary strategy (trivial);

   • StationaryPoint: computes an approximate stationary point of the maximum-regret func-
     tion and its dual, returning four strategies [14];

                                                17
   • ZeroSumNE: computes an exact Nash equilibrium of a zero-sum game via linear program-
     ming (textbook);
   • EqMix: equal-probability mixture of two strategies (trivial);
   • MaxPayoff: maximizes a given payoff function (trivial).
These building blocks deﬁne what operations are available, but do not prescribe how to combine
them—the composition is entirely determined by the LLM.
   The prompt-level constraints fall into three categories:
  1. Structural constraints (limiting the search space): at most 3 strategies per player (enforced
     at runtime), static single assignment (SSA), type annotations required.
  2. Heuristic guidance (non-restrictive): Occam’s Razor (fewer strategies preferred), encour-
     agement to break symmetry between players, penalization of duplicate algorithms.
  3. Domain-speciﬁc constraint: the LLM must include at least one StationaryPoint building
     block. This constraint reﬂects the domain knowledge that all competitive polynomial-time
     ANE algorithms since Tsaknakis and Spirakis [14] rely on stationary-point computation;
     algorithms without it (e.g., KPS [12], DMP [13]) achieve at best ϵ = 0.5. This constraint
     excludes known-suboptimal directions but does not specify how the strategies returned by
     StationaryPoint should be combined—the latter is the creative part that the LLM must
     determine.
   Critically, the expert inputs do not include:
   • any suggestion of the overall algorithmic structure or composition order;
   • any hint to use or avoid the extension technique;
   • any speciﬁcation of mixing coefﬁcients or payoff-dependent weights;
   • any target ϵ value;
   • any few-shot examples of algorithm designs (the provided code examples illustrate only
     the expected format, not algorithmic strategies).
    The results provide empirical evidence that the expert inputs did not bias the LLM toward the
discovered solutions: of the 7 distinct three-player algorithms produced across 12 rounds, only
the ﬁrst used the extension technique; the remaining 6 independently explored non-extension
structures. The ﬁnal 0.5 + δ algorithm combines BestResponse, EqMix, and OptimalMixing in a
pattern that was not anticipated by the human experts who designed the building blocks.

Process Management for Robust Exploration To prevent redundant exploration, we maintain
a record of all previously generated algorithms. If the LLM proposes a duplicate, it is informed
and shown the record of past attempts. If duplicates persist up to a certain threshold, the interac-
tion is restarted to encourage new lines of inquiry. Similarly, to prevent the LLM from forgetting
instructions in a long conversation history, we restart the interaction when the chat history ex-
ceeds a certain length. Finally, to ensure timely analysis by LegoNE, we set limits on the number
of code lines and constructed strategies, prompting the LLM to simplify any overly complex
algorithms it generates.

                                                   18
Experimental Setup and Main Results
For our experiments, we employed DeepSeek-R1-250120 (abbreviated as R1) [29], a reasoning
LLM. We set the temperature to 0.8, allowing for some variation in the LLM’s responses. We
provide the LLM with a set of building blocks derived from existing human-designed algorithms.
    For the LegoNE analyzer, we use the same environment as in the benchmarking subsection
above. For two-player cases, we set the Mathematica parameters as follows: AccuracyGoal to 6,
and MaxIterations to 5000. For three-player cases, since the computation is more difﬁcult, we
set AccuracyGoal to 40, WorkingPrecision to 60, and MaxIterations to 2000. For both cases, we
use the default method (auto) as the optimization method. As a reproducibility check, we run
the full process on a Windows personal computer (PC) and then manually verify the LegoNE
analyzer output on the MacBook.

Two-Player Game Experiments In the two-player game setting, R1 replicated the best polynomial-
time worst-case guarantee in 2 rounds, but with a different algorithm than the literature. This
provides a concrete comparison with the 15 years between the previous guarantee and the current
one in the human-designed literature.
    We also tested with the DeepSeek-V3-241226 (abbreviated as V3) model [36]. Again, we set
the temperature to 0.8 and used the same building-block requirements. In a more extensive
test of 100 rounds, V3 did not surpass the best polynomial-time worst-case guarantee but did
discover several combinations not found in the literature.

Three-Player Game Experiments In the more challenging three-player game domain, R1 dis-
covered an algorithm with a provable approximation guarantee of (0.5 + δ) in 11 rounds. This
improves upon the previously best human-designed polynomial-time worst-case guarantee of
0.6 + δ. Furthermore, R1 discovered six additional algorithms with guarantees ranging from
0.5 + δ to 0.8 + δ within 12 rounds.
    All but the ﬁrst of these discovered algorithms do not use the extension technique shown
in Figure 4, which was previously the only known approach for human experts to design a
three-player ANE algorithm with a nontrivial guarantee better than 1. These structurally distinct
algorithms show that the automated process can explore parts of the design space outside the
extension paradigm. The best-performing discovered algorithm is presented in Figure 5. The
extension-technique constructions terminate with a best-response-then-mix step; in contrast, the
discovered algorithm relies on a substantially more intricate composition of building blocks,
interleaving BestResponse, EqMix, and OptimalMixing in a nontrivial manner.


Related Work
The Computational Complexity of Nash Equilibria. The Nash equilibrium [1, 30] is the central
solution concept in non-cooperative game theory. Nash’s existence theorem is purely existential;
the ﬁrst algorithmic approach, the Lemke–Howson algorithm [2], requires exponential time in
the worst case, and for decades no polynomial-time algorithm was found, though no hardness
proof was known either. In this setting, Lipton, Markakis, and Mehta [5] initiated the study of
approximate Nash equilibria by proving that ϵ-ANE can be computed in quasi-polynomial time
for any constant ϵ, via a structural result showing that Nash equilibria can be well approximated


                                               19
by strategies with logarithmic support—the ﬁrst sub-exponential algorithm for the problem. The
subsequent PPAD-completeness results of Daskalakis, Goldberg, and Papadimitriou [3] (for three
or more players) and Chen and Deng [4] (for two players) conﬁrmed that computing an exact
Nash equilibrium is intractable, providing theoretical justiﬁcation for the pursuit of approxima-
tion.
    Following PPAD-completeness, polynomial-time approximation algorithms advanced rapidly:
Kontogiannis, Panagopoulou, and Spirakis [12] achieved ϵ = 0.75; Daskalakis, Mehta, and Pa-
padimitriou [13, 26] improved this to 0.5 and 0.382; Bosse, Byrka, and Markakis [15] reached
0.364; and Tsaknakis and Spirakis [14] attained 0.3393 + δ. Progress then stalled for 15 years.
In the quasi-polynomial regime, Babichenko, Barman, and Peretz [6] substantially improved the
support-size bounds for multi-player games, reducing the dependence on the number of play-
ers from polynomial to logarithmic. Rubinstein [10] proved that no PTAS exists (assuming the
Exponential Time Hypothesis for PPAD), ruling out polynomial-time algorithms for arbitrarily
small ϵ; however, the corresponding hardness constant is not explicit and is believed to be very
small [11]. Deligkas, Fasoulakis, and Markakis [9] ﬁnally broke the 15-year barrier with a 1/3 + δ
guarantee.
    For multi-player games, the extension technique [15, 16] lifts an r-player algorithm to (r +1)
players with guarantee degrading from ϵr to 1/(2 − ϵr ). Applied to the best two-player result, this
yields 0.6 + δ for three-player games, with guarantees approaching 1 as the number of players
grows. No alternative design paradigm for polynomial-time multi-player ANE algorithms was
known prior to this work.

Explore-and-Evaluate Pipelines for Algorithmic Discovery. A broad thread of work auto-
mates algorithm development by exploring a hypothesis space and evaluating candidates with a
machine-computable objective, including program synthesis [37] and automated algorithm con-
ﬁguration [38]. Recent systems use learned heuristics to navigate large spaces of low-level al-
gorithms, e.g., reinforcement-learning agents that discover faster sorting routines [39] and new
matrix multiplication decompositions [19], as well as self-learning synthesis for structured do-
mains such as integer-sequence programs [40]. These efforts typically evaluate candidates by
empirical metrics (runtime, operation counts, benchmark accuracy) or by correctness for ﬁxed
input sizes, whereas LegoNE targets theorem-style worst-case approximation guarantees over an
inﬁnite family of games.

Relationship to AI-for-Science Systems. LegoNE combined with an LLM shares the high-
level explore-and-evaluate architecture with recent AI-for-science systems such as AlphaGeome-
try [17, 18], FunSearch [20], and AlphaEvolve [41]. Within this shared paradigm, three technical
differences are worth noting. First, the evaluators in prior systems are either pre-existing (Al-
phaGeometry’s deductive engine DDAR dates to the work of Chou, Gao, and Zhang in the
1990s [42]) or straightforward to construct (FunSearch evaluates programs by executing them
on speciﬁc instances); the LegoNE analyzer—based on the instantiation and forgetting compila-
tion principles—is a formal system constructed in this work. Second, while AlphaGeometry’s
evaluator provides binary feedback (proof found or not), the LegoNE analyzer returns a quantita-
tive worst-case guarantee ϵ, enabling gradient-style optimization in the LLM search loop. Third,
AlphaGeometry veriﬁes static geometric propositions, whereas LegoNE veriﬁes universal per-
formance guarantees of procedural algorithms, requiring Floyd–Hoare-style program reasoning


                                                20
combined with the instantiation and forgetting compilation.

Sample-Based Guarantees for Strategic Properties. There is a growing literature that evaluates
algorithms or strategic properties from samples, providing distribution-dependent guarantees
rather than worst-case ones. For example, generalization results quantify how much data suf-
ﬁces to learn or tune high-performing algorithms under an unknown instance distribution [43],
and related techniques estimate approximate incentive compatibility or distance from equilib-
rium in auctions from sampled types or play trajectories [44, 45]. These tools are well-suited to
settings where a reference distribution is meaningful and data are available, and they comple-
ment classical worst-case analyses that seek instance-independent approximation guarantees.

LLMs for Game Solving and Strategy/Policy Generation. Recent work studies LLMs as gener-
ators of strategies and policies, including self-play with code-generating models to reﬁne game
strategies [46], guiding language generation with game-theoretic equilibrium solvers [47], trans-
lating natural-language game descriptions into extensive-form representations [48], and code-
space response oracles for interpretable multi-agent policies [49]. These lines primarily target
empirical behavior in particular games or interaction domains, whereas our focus is synthesizing
polynomial-time algorithms for normal-form games together with machine-checkable worst-case
guarantees.


Data Availability
All data generated in this study—including the discovered ANE algorithms expressed in the
LegoNE language, the benchmark approximation guarantees computed by the analyzer (Ta-
bles 1, 2), the LLM prompts (src/auto_design/prompts.py), and the running-time measurements—
are publicly available at the Zenodo repository [50]; reuse of these materials is governed by the
license described in the Code Availability statement below.


Code Availability
The source code of the LegoNE compiler and analyzer, the building-block library, and the LLM-
driven discovery pipeline used in this study is deposited in the Zenodo repository [50]. The code
includes implementations sufﬁcient to reproduce all experiments reported in this paper. The
repository is released under copyright “All rights reserved” by the authors, owing to ongoing
patent-related plans. Non-commercial academic use—including reproduction, veriﬁcation, and
extension of the results reported in this paper—is permitted free of charge upon written request
to the corresponding author Hanyu Li (lhydave@pku.edu.cn); requests are typically answered
within two weeks. The repository will remain available indeﬁnitely. Other uses require a separate
licensing agreement with the authors.


Acknowledgements
The authors would like to thank Ruyi Ji, Yuhao Li, and Paul Spirakis for helpful discussions.
The authors would also like to thank the anonymous reviewers for their valuable comments and

                                               21
suggestions.


Funding
This work is supported by the Natural Science Foundation of China (Grant No. 62572010 and
Grant No. 6212290003).


Author Contributions
H.L. and D.L. conceived the project and designed the LegoNE framework. H.L. implemented
the LLM-powered discovery loop and the LegoNE building-block library, and carried out the
computational experiments. D.L. contributed to experimental analysis and validation. H.L. and
D.L. jointly developed the formal analyses and proofs. H.L. wrote the original draft; H.L. and
D.L. contributed to the writing and led the revision responses. X.D. supervised the project.


Competing Interests
The authors declare no competing interests.




                                              22
References
 [1] Nash, J. Non-Cooperative Games. Annals of Mathematics 54, 286–295 (1951). Available at
     http://www.jstor.org/stable/1969529. 1969529.

 [2] Lemke, C. E. & Howson, J. T., Jr. Equilibrium Points of Bimatrix Games. Journal of the Society
     for Industrial and Applied Mathematics 12, 413–423 (1964). Available at http://epubs.siam.
     org/doi/10.1137/0112033.

 [3] Daskalakis, C., Goldberg, P. W. & Papadimitriou, C. H. The complexity of computing a
     Nash equilibrium. In Kleinberg, J. M. (ed.) Proceedings of the 38th Annual ACM Symposium
     on Theory of Computing, 2006, May 21-23, 71–78 (ACM, Seattle, WA, USA, 2006). Available at
     https://doi.org/10.1145/1132516.1132527.

 [4] Chen, X., Deng, X. & Teng, S.-H. Settling the complexity of computing two-player Nash
     equilibria. J. ACM 56, 14:1–14:57 (2009). Available at https://doi.org/10.1145/1516512.
     1516516.

 [5] Lipton, R. J., Markakis, E. & Mehta, A. Playing large games using simple strategies. In
     Proceedings of the 4th ACM Conference on Electronic Commerce (EC 2003), 36–41 (ACM, San
     Diego, CA, USA, 2003). Available at https://doi.org/10.1145/779928.779933.

 [6] Babichenko, Y., Barman, S. & Peretz, R. Simple approximate equilibria in large games.
     In Proceedings of the ﬁfteenth ACM conference on Economics and computation, 753–770 (ACM,
     Palo Alto California USA, 2014). Available at https://dl.acm.org/doi/10.1145/2600057.
     2602873.

 [7] Williamson, D. P. & Shmoys, D. B. The Design of Approximation Algorithms (Cambridge Uni-
     versity Press, Cambridge, 2011). Available at https://www.cambridge.org/core/books/
     design-of-approximation-algorithms/88E0AEAEFF2382681A103EEA572B83C6.

 [8] Vazirani, V. V. Approximation algorithms (Springer, Berlin Heidelberg, 2003), corrected second
     printing edn.

 [9] Deligkas, A., Fasoulakis, M. & Markakis, E. A polynomial-time algorithm for 1/2-well-
     supported nash equilibria in bimatrix games. SIAM Journal on Computing 52, 1083–1096
     (2023). Available at https://doi.org/10.1137/23m1549237.

[10] Rubinstein, A. Settling the Complexity of Computing Approximate Two-Player Nash Equi-
     libria. In 2016 IEEE 57th Annual Symposium on Foundations of Computer Science (FOCS), 258–
     265 (2016). Available at https://ieeexplore.ieee.org/document/7782938.

[11] Deligkas, A., Fearnley, J., Hollender, A. & Melissourgos, T. Pure-Circuit: Tight Inapproxima-
     bility for PPAD. J. ACM 71, 31:1–31:48 (2024). Available at https://dl.acm.org/doi/10.
     1145/3678166.

[12] Kontogiannis, S. C., Panagopoulou, P. N. & Spirakis, P. G. Polynomial Algorithms for Ap-
     proximating Nash Equilibria of Bimatrix Games. In Spirakis, P. G., Mavronicolas, M. & Kon-
     togiannis, S. C. (eds.) Internet and Network Economics, Second International Workshop, WINE


                                                23
    2006, December 15-17, Proceedings, vol. 4286 of Lecture Notes in Computer Science, 286–296
    (Springer, Patras, Greece, 2006). Available at https://doi.org/10.1007/11944874_26.

[13] Daskalakis, C., Mehta, A. & Papadimitriou, C. H. A Note on Approximate Nash Equilib-
     ria. In Spirakis, P. G., Mavronicolas, M. & Kontogiannis, S. C. (eds.) Internet and Network
     Economics, Second International Workshop, WINE 2006, December 15-17, Proceedings, vol. 4286
     of Lecture Notes in Computer Science, 297–306 (Springer, Patras, Greece, 2006). Available at
     https://doi.org/10.1007/11944874_27.

[14] Tsaknakis, H. & Spirakis, P. G. An Optimization Approach for Approximate Nash Equilib-
     ria. In Deng, X. & Graham, F. C. (eds.) Internet and Network Economics, Third International
     Workshop, WINE 2007, December 12-14, Proceedings, vol. 4858 of Lecture Notes in Computer Sci-
     ence, 42–56 (Springer, San Diego, CA, USA, 2007). Available at https://doi.org/10.1007/
     978-3-540-77105-0_8.

[15] Bosse, H., Byrka, J. & Markakis, E. New algorithms for approximate Nash equilibria in
     bimatrix games. Theoretical Computer Science 411, 164–173 (2010). Available at https://www.
     sciencedirect.com/science/article/pii/S0304397509006719.

[16] Hémon, S., De Rougemont, M. & Santha, M. Approximate Nash Equilibria for Multi-player
     Games. In Monien, B. & Schroeder, U.-P. (eds.) Proceedings of the 1st International Sympo-
     sium on Algorithmic Game Theory (SAGT 2008), vol. 4997 of Lecture Notes in Computer Sci-
     ence, 267–278 (Springer, Berlin, Heidelberg, 2008). Available at https://doi.org/10.1007/
     978-3-540-79309-0_24.

[17] Trinh, T. H., Wu, Y., Le, Q. V., He, H. & Luong, T. Solving olympiad geometry without
     human demonstrations. Nature 625, 476–482 (2024). Available at https://www.nature.com/
     articles/s41586-023-06747-5.

[18] Chervonyi, Y. et al. Gold-medalist Performance in Solving Olympiad Geometry with Al-
     phaGeometry2. Journal of Machine Learning Research 26, 1–39 (2025). Available at https:
     //jmlr.org/papers/v26/25-1654.html.

[19] Fawzi, A. et al. Discovering faster matrix multiplication algorithms with reinforcement
     learning. Nature 610, 47–53 (2022). Available at https://www.nature.com/articles/
     s41586-022-05172-4.

[20] Romera-Paredes, B. et al. Mathematical discoveries from program search with large lan-
     guage models. Nature 625, 468–475 (2024). Available at https://www.nature.com/articles/
     s41586-023-06924-6.

[21] Tarski, A. & McKinsey, J. C. C. A Decision Method for Elementary Algebra and Geome-
     try (University of California Press, 1951), dgo - digital original, 1 edn. Available at
     https://www.jstor.org/stable/jj.8501420. jj.8501420.

[22] Wu, W.-t. Mechanical Theorem Proving in Geometries. Texts and Monographs in Symbolic
     Computation (Springer, Vienna, 1994). Available at http://link.springer.com/10.1007/
     978-3-7091-6639-0.



                                               24
[23] Everett, H. Recursive Games. In Contributions to the Theory of Games (AM-39), Volume III,
     47–78 (Princeton University Press, 1957). Available at http://www.jstor.org/stable/j.
     ctt1b9x26z.6. j.ctt1b9x26z.6.

[24] Floyd, R. W. Assigning Meanings to Programs. In Colburn, T. R., Fetzer, J. H. & Rankin, T. L.
     (eds.) Program Veriﬁcation: Fundamental Issues in Computer Science, 65–81 (Springer Nether-
     lands, Dordrecht, 1993). Available at https://doi.org/10.1007/978-94-011-1793-7_4.

[25] Hoare, C. A. R. An axiomatic basis for computer programming. Communications of the ACM
     12, 576–580 (1969). Available at https://dl.acm.org/doi/10.1145/363235.363259.

[26] Daskalakis, C., Mehta, A. & Papadimitriou, C. Progress in approximate Nash equilibria.
     In Proceedings of the 8th ACM conference on Electronic commerce, 355–358 (ACM, San Diego
     California USA, 2007). Available at https://dl.acm.org/doi/10.1145/1250910.1250962.

[27] Czumaj, A. et al. Distributed Methods for Computing Approximate Equilibria. In Cai, Y. &
     Vetta, A. (eds.) Web and Internet Economics - 12th International Conference, WINE 2016, December
     11-14, Proceedings, vol. 10123 of Lecture Notes in Computer Science, 15–28 (Springer, Montreal,
     Canada, 2016). Available at https://doi.org/10.1007/978-3-662-54110-4_2.

[28] Deligkas, A., Fearnley, J., Savani, R. & Spirakis, P. Computing Approximate Nash Equilibria
     in Polymatrix Games. Algorithmica 77, 487–514 (2017). Available at https://doi.org/10.
     1007/s00453-015-0078-7.

[29] Guo, D. et al. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement
     learning. Nature 645, 633–638 (2025). Available at https://www.nature.com/articles/
     s41586-025-09422-z.

[30] Nash, J. F. Equilibrium points in n-person games. Proceedings of the National Academy of
     Sciences 36, 48–49 (1950). Available at https://www.pnas.org/doi/10.1073/pnas.36.1.48.

[31] Mailloux, B. J., Peck, J. E. L., Koster, C. H. A. & van Wijngaarden, A. Report on the Al-
     gorithmic Language ALGOL 68. In Mailloux, B. J., Peck, J. E. L., Koster, C. H. A. & van
     Wijngaarden, A. (eds.) Report on the Algorithmic Language ALGOL 68, 80–218 (Springer, Berlin,
     Heidelberg, 1969). Available at https://doi.org/10.1007/978-3-662-39502-8_1.

[32] Gurobi Optimization. https://www.gurobi.com/. Available at https://www.gurobi.com/.
     (accessed 2024-11-13).

[33] Wolfram Mathematica: Modern Technical Computing.        https://www.wolfram.com/
     mathematica/. Available at https://www.wolfram.com/mathematica/. (accessed 2024-11-
     13).

[34] Paxson, V. Flex - a scanner generator. https://www.cs.princeton.edu/~appel/modern/c/
     software/flex/flex.html. Available at https://www.cs.princeton.edu/~appel/modern/
     c/software/flex/flex.html. (accessed 2024-11-16).

[35] Free Software Foundation. Bison - GNU Project. https://www.gnu.org/software/bison/.
     Available at https://www.gnu.org/software/bison/. (accessed 2024-11-16).


                                                 25
[36] DeepSeek-AI et al. DeepSeek-V3 Technical Report (2024). Available at http://arxiv.org/
     abs/2412.19437. 2412.19437.

[37] Jacindha, S., Abishek, G. & Vasuki, P. Program Synthesis - A Survey. In Kumar, A., Zu-
     rada, J. M., Gunjan, V. K. & Balasubramanian, R. (eds.) Computational Intelligence in Ma-
     chine Learning, vol. 834, 409–421 (Springer Nature Singapore, Singapore, 2022). Available at
     https://link.springer.com/10.1007/978-981-16-8484-5_39.

[38] Stützle, T. & López-Ibáñez, M. Automated algorithm conﬁguration and design. In Proceed-
     ings of the Genetic and Evolutionary Computation Conference Companion, 959–982 (ACM, Lille
     France, 2021). Available at https://dl.acm.org/doi/10.1145/3449726.3461404.

[39] Mankowitz, D. J. et al. Faster sorting algorithms discovered using deep reinforcement
     learning. Nature 618, 257–263 (2023). Available at https://www.nature.com/articles/
     s41586-023-06004-9.

[40] Gauthier, T., Olšák, M. & Urban, J. Improvements in Program Synthesis for Integer Se-
     quences. In 8th Conference on Artiﬁcial Intelligence and Theorem Proving (AITP 2023) (Aus-
     sois, France, 2023). Available at http://aitp-conference.org/2023/abstract/AITP_2023_
     paper_8.pdf.

[41] Novikov, A. et al. AlphaEvolve: A coding agent for scientiﬁc and algorithmic discovery.
     arXiv preprint arXiv:2506.13131 (2025). Available at https://arxiv.org/abs/2506.13131.
     2506.13131.

[42] Chou, S.-C., Gao, X.-S. & Zhang, J.-Z. Machine Proofs in Geometry, vol. Volume 6 of
     Series on Applied Mathematics (WORLD SCIENTIFIC, 1994). Available at https://www.
     worldscientific.com/doi/10.1142/2196.

[43] Balcan, M.-F. et al. How Much Data Is Sufﬁcient to Learn High-Performing Algorithms?
     Journal of the ACM 71, 32:1–32:58 (2024). Available at https://dl.acm.org/doi/10.1145/
     3676278.

[44] Balcan, M.-F., Sandholm, T. & Vitercik, E. Estimating Approximate Incentive Compatibility.
     In Proceedings of the 2019 ACM Conference on Economics and Computation (EC 2019), 867 (ACM,
     Phoenix, AZ, USA, 2019). Available at https://doi.org/10.1145/3328526.3329628.

[45] Pieroth, F. R. & Sandholm, T. Verifying Approximate Equilibrium in Auctions. arXiv preprint
     arXiv:2408.11445 (2024). Available at https://arxiv.org/abs/2408.11445. 2408.11445.

[46] Bachrach, Y. et al. Combining Code Generating Large Language Models and Self-Play to It-
     eratively Reﬁne Strategies in Games. In Proceedings of the 34th International Joint Conference on
     Artiﬁcial Intelligence (IJCAI 2025), 10999–11003 (ijcai.org, Montreal, Canada, 2025). Available
     at https://doi.org/10.24963/ijcai.2025/1249.

[47] Gemp, I. et al. States as Strings as Strategies: Steering Language Models with Game-
     Theoretic Solvers. arXiv preprint arXiv:2402.01704 (2024). Available at https://arxiv.org/
     abs/2402.01704. 2402.01704.



                                                 26
[48] Deng, S., Wang, Y. & Savani, R. From Natural Language to Extensive-Form Game Rep-
     resentations. In Proceedings of the 24th International Conference on Autonomous Agents and
     Multiagent Systems (AAMAS 2025), 593–601 (IFAAMAS, Detroit, MI, USA, 2025). Available
     at https://dl.acm.org/doi/10.5555/3709347.3743575.

[49] Hennes, D., Li, Z., Schultz, J. & Lanctot, M. Code-Space Response Oracles: Generating
     Interpretable Multi-Agent Policies with Large Language Models. https://arxiv.org/abs/
     2603.10098v1 (2026). Available at https://arxiv.org/abs/2603.10098v1. (accessed 2026-
     04-01).

[50] Li, H., Li, D. & Deng, X. lego-ne: Source code and data for “Discovering Expert-Level Nash
     Equilibrium Algorithms with Large Language Models”. Zenodo, https://doi.org/10.
     5281/zenodo.20158034 (2026). Available at https://doi.org/10.5281/zenodo.20158034.

[51] Van Dalen, D. Logic and Structure. Universitext (Springer, London, 2013). Available at
     https://link.springer.com/10.1007/978-1-4471-4558-5.

[52] Deng, X., Li, D. & Li, H. On the optimal mixing problem of approximate Nash equilibria
     in bimatrix games. Theoretical Computer Science 1031, 115072 (2025). Available at https:
     //www.sciencedirect.com/science/article/pii/S0304397525000106.

[53] Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C. Introduction to algorithms (MIT Press,
     Cambridge, Mass, 2009), 3rd ed edn.




                                                 27
A      A Formal and Complete Treatment of LegoNE
In this part, we provide a formal and complete treatment of LegoNE. We ﬁrst deﬁne the syntax
of logic encodings of building blocks, algorithms, and the proof goal. Then, we describe the
instantiation and forgetting tactics. Finally, we show how to convert the LegoNE code into a
constrained optimization problem to ﬁnd the approximation guarantee.

A.1     Syntax of Logic Encodings
We ﬁrst deﬁne the syntax of logic encodings of building blocks.

Symbols.        We use the following symbols in the logic encodings:

    • payoff functions: u1 , u2 , . . . , ur ,

    • loss functions: f 1 , f 2 , . . . , f r , f ,

    • strategy variables: x1 , x2 , . . . , xr , y1 , y2 , . . . , yr , . . . ,

    • payoff variables: U1 , U2 , . . . ,

    • real variables: ρ1 , ρ2 , . . . ,

    • real constants: 1, −1, 0.5, . . . ,

    • arithmetic operators: +, −, ×, ÷, ≤, ≥, =, min, max,

    • logic connectives: ∧, ∨,

    • quantiﬁers: ∀, ∃.

    • other symbols: (, ), :, ,.

Terms. We can only use the following terms in the logic encodings:

    • payoff terms: U ( xi , y−i ), where U is among payoff functions u1 , u2 , . . . , ur and payoff vari-
      ables U1 , U2 , . . . ,

    • loss terms: f i ( xi , y−i ),

    • maximum of payoff terms: maxxi U ( xi , y−i ),

    • real variables: ρi ,

    • real constants: 1, −1, 0.5, . . . .




                                                                    28
Arithmetic expressions.      The set L A of arithmetic expressions can be inductively deﬁned as
follows:

   • Terms are in L A .

   • If α, β ∈ L A , then (α + β), (α − β), (α × β), (α ÷ β), min{α, β}, max{α, β} ∈ L A .

Remark A.1. Note that we set the maximum of payoff terms as a term, rather than an expression.
This is because the maximum operation here ranges over xi , which is not a ﬁnite set. Thus,
the arithmetic properties of such maximum operations are not straightforward, compared to
the maximum of two real numbers. Humans need to provide the properties of such maximum
operations in the logic encodings.
   Similarly, while we know that payoff functions are multi-linear, it could be difﬁcult for ma-
chines to ﬂexibly utilize multi-linearity. Thus, we only treat payoff functions as terms, rather
than expressions. Multi-linearity is then provided by humans as logic encodings, which are
much easier for machines to utilize.

Comparison expressions. A comparison expression is a formula in the form of α COMP β,
where α, β ∈ L A and COMP ∈ {≤, ≥, =}.

Basic types. We use a : A to denote that a is of type A. We have the following basic types and
their elements used to deﬁne the input and output of building blocks:

   • None type None: no element,

   • Real type Real: arithmetic expressions in L A ,

   • Payoff type Payoﬀ: payoff functions u1 , u2 , . . . , ur and their linear combinations with coefﬁ-
     cients in Real,

   • Comparison type Comp: comparison expressions,

   • Player i’s strategy type Strategyi : the element in Strategyi can be inductively constructed as
     follows. If xi , yi : Strategyi , then αxi + (1 − α)yi is in Strategyi for any α : Real with α ∈ [0, 1].

Building blocks.     A building block is a function with inputs and outputs. The type of building
blocks is
                             Ti1 × Ti2 × · · · × Tik → To1 × To2 × · · · × Tom ,                         (7)
where Tij ’s are input types and Tok ’s are output types. The input types can be any of the basic
types above, and the output types can be any of them except the comparison type. For example,
when r = 3, BestResponse2 is a building block with type Strategy1 × Strategy3 → Strategy2 .

Logic encodings of building blocks. We use ϕ to denote the mapping from a building block
to a logic encoding. A building block can be encoded as a formula from the following set L E ,
inductively constructed as follows:




                                                     29
   • All atomic properties α’s belong to L E , where each α has the following form:

                                          (∃ρ1 . . . , ρs )(∀ x11 , . . . , xrmr )(∀U1 , U2 , . . . )γ.                  (8)

      The meaning of each symbol is as follows:

          – ρi is a real variable.
          – xit is the t-th strategy variable of player i.
          – Ui is a payoff variable.
          – γ is a comparison expression.

   • If α, β ∈ L E , then (α ∧ β) ∈ L E .

   • If α, β ∈ L E , then (α ∨ β) ∈ L E .

   Logic encodings are used to describe the properties of building blocks. For example, in two-
player games, the building block y1 = BestResponse1( x2 ) can be encoded as

                                               ∀z1 (u1 (z1 , x2 ) ≤ u1 (y1 , x2 )).                                      (9)

This encoding only have an atomic property.
    We can have more complicated properties by using conjunctions and disjunctions of such
atomic properties. The conjunction can be understood as “this building block has all these
properties”, while the disjunction can be understood as “this building block has at least one
of these properties”. Finally, the existential quantiﬁers can be understood as “this building block
constructs some internal variables to achieve these properties”. For example, the encoding of
building block StationaryPoint has an existential quantiﬁer ∃ρ. (See Section B)
    Apart from the building blocks, the deﬁnitions of payoff function ui and regret f i themselves
also imply a group of inherent formulas:

   • For i ∈ [r ], ∀ x(0 ≤ ui ( x) ≤ 1 ∧ 0 ≤ f i ( x) ≤ 1).

   • For i ∈ [r ], ∀ xi , ∀ x−i ( f i ( xi , x−i ) = maxx̃i ui ( x̃i , x−i ) − ui ( xi , x−i )).

   • For i ∈ [r ], ∀ xi , ∀ x−i (maxx̃i ui ( x̃i , x−i ) ≥ ui ( xi , x−i )).

   • For i ∈ [r ], ∀ x−i (maxx̃i ui ( x̃i , x−i ) ≤ 1).

We denote the conjunction of these formulas for all i’s as ϕ0 .

Algorithms. In the LegoNE framework, each algorithm is a sequence of assignment statements.
One assignment uses a deﬁned building block with existing variables as inputs and new variables
as outputs.
    Formally, suppose we have deﬁned a set F of building blocks. Then, an algorithm is a ﬁnite
sequence of assignments s1 , . . . , s p . For each assignment si , we maintain a corresponding variable
set Vi . V0 is the input of the algorithm. si must be in one of the following forms:

   1. v10 , . . . , v0m = f i (v1 , . . . , vn ), where v10 , . . . , v0m are new variables not in Vi−1 , v1 , . . . , vn are
      existing variables in Vi−1 or constants, and f i is a building block in F .

                                                                  30
   2. return v1 , . . . , vr , where v1 , . . . , vr are existing variables in Vi−1 and variable vi has type
      Strategyi .
If form 1 is used, then update Vi = Vi−1 ∪ {v10 , . . . , v0m }; otherwise Vi = Vi−1 .
    A more intuitive way to write an algorithm is given as follows:

Algorithm 1 Algorithm Γ
Input: Payoff functions u1 , u2 , . . . , ur
  1: s11 , s12 , . . . , s1m1 = B1
  2: s21 , s22 , . . . , s2m2 = B2
            ...
  k: sk1 , sk2 , . . . , skmk = Bk
  k + 1: return s1 , s2 , . . . , sr


   Here, sij is a strategy as the j-th output of building block Bi using only variables suv with
u < i, v ≤ mu , and si is player i’s strategy, being one among s11 , . . . , skmk .

Encoding of algorithms. The encoding of algorithm Γ is

                                      ϕ[Γ] : ϕ0 ∧ ϕ[line 1] ∧ · · · ∧ ϕ[line k ].                             (10)

Proof goal.     To show that algorithm Γ has an approximation guarantee of b, the proof goal is

                      (∀u1 , u2 , . . . , ur )(∀s11 , . . . , skmk )(ϕ[Γ] → f (s1 , s2 , . . . , sr ) ≤ b).   (11)

A.2    Instantiation and Forgetting
In this part, we formally give the instantiation and forgetting tactics in LegoNE. These tactics are
essential for rewriting the proof goal into a form that is amenable to optimization.
    Here, we propose Algorithm 2 to instantiate the universal quantiﬁers in any property in the
form of (8).
    Note that Algorithm 2 only instantiates the atomic properties (8) in the logic encoding. The
instantiation of the whole logic encoding is given by simply instantiating all atomic properties in
the encoding.
    Suppose we do the instantiation for the proof goal (11) of algorithm Γ. We denote the result
as ψ0 . Now we describe the forgetting tactic.
    For the forgetting tactic, it is essentially a renaming process. Since we have formally deﬁned
what a term is, we can directly rename all terms using new names such that different terms have
different names. We present it in Algorithm 3.
    Using the instantiation and forgetting tactics, we can rewrite the proof goal into a form that
is ready for optimization. We will discuss this in the next section.

A.3    Converting LegoNE Code into an Optimization Problem
In this part, we show how to convert the LegoNE code into a constrained optimization problem
to ﬁnd the approximation guarantee.

                                                              31
Algorithm 2 Instantiation Algorithm
Input: A logic formula ψ in the form of (8), a series of payoff functions u1 , u2 , . . . , ur , and a series
    of strategies s11 , s12 , . . . , srmr .
Output: A series of inequalities derived from ψ.
 1: For each payoff quantiﬁer ∀Ui , replace it with uk for all k ∈ [r ] and all newly constructed
    payoff functions. // This will eliminate all payoff quantifiers.
 2: Do the following two procedures, respectively.


 3: Procedure 1: Instantiation using existing strategies.
 4:      For each strategy quantiﬁer ∀ xit , replace all occurrence of xit with sik for all k ∈ [mi ] and
         remove the quantiﬁer ∀ xit . // This will eliminate all strategy quantifiers.
 5:      The remaining formulas are all universal-quantiﬁer-free. Let C1 be the conjunction of
         these formulas.

 6: end Procedure 1


 7: Procedure 2: Instantiation using the max operator.
 8: for strategy quantiﬁer ∀ xit do
 9:    if xit occurs more than once in ψ then
10:        continue       // The maximum of two different terms involving xit may not be
           obtained at the same xit .
11:    end if
12:    Use Procedure 1 to instantiate all but one strategy quantiﬁer xit and obtain C1 . This will
       eliminate all but one strategy quantiﬁer.
13:    For every term ui ( xit , ·) in C1 , replace it with maxxi ui ( xit , ·). The result is C2 ( xit ).
                                                                  t
14: end for
15: Let C2 be the conjunction of C2 ( xit ) for all xit (if any).
16: end Procedure 2


17: return C1 ∧ C2 .


    We still focus on the general Algorithm Γ in Section A.1. This time, we do not know the
approximation guarantee of the algorithm. Instead, we set an unknown approximation guarantee
b, but the proof goal (11) remains the same. For convenience, we here write down the proof goal
again:
                   (∀u1 , u2 , . . . , ur )(∀s11 , . . . , skmk )(ϕ[Γ] → f (s1 , s2 , . . . , sr ) ≤ b). (12)
We need to ﬁnd a real number b as small as possible such that the above formula is valid.
   Similarly, we can rewrite the proof goal into
                   ∀ a1 , . . . , ∀b1 , . . . , ∀c1 , . . . (ϕ0 [Γ] → g( a1 , . . . , b1 , . . . , c1 , . . . ) ≤ b),   (13)
    Here, ϕ0 [Γ] contains no universal quantiﬁers on payoffs or strategies. However, in the gen-
eral case, ϕ0 [Γ] still contains existential quantiﬁers on real variables. We need to handle these
existential quantiﬁers.
    The existential quantiﬁer can be handled by the following standard result in predicate logic
(see. e.g., Theorem 3.5.11 on page 74 and Example 1 on page 73 in textbook [51]).

                                                                  32
Algorithm 3 Forgetting Algorithm
Input: A logic formula ψ0 after instantiation of the proof goal (11).
 1: Collect all terms in ψ0 . Let T be the set of all terms.
 2: For each term t ∈ T, deﬁne a new symbol θ ( t ) that does not appear in ψ0 .
 3: Replace each term t in ψ0 with θ ( t ).
 4: Remove all quantiﬁers in outermost of ψ0 and replace them with ∀ θ ( t ) for all t ∈ T.
 5: return ψ0 .



Lemma A.2. Suppose x occurs free in formula A( x ) and does not occur free in formula B. Then

   • (∃ xA( x )) → B is logically equivalent to ∀ x ( A( x ) → B).

   • (∃ xA( x )) ∧ B is logically equivalent to ∃ x ( A( x ) ∧ B).

   • (∃ xA( x )) ∨ B is logically equivalent to ∃ x ( A( x ) ∨ B).

    Using the second and the third properties, we can rewrite the proof goal (13) as

                ∀ a1 , . . . , ∀b1 , . . . , ∀c1 , . . . , ∀ρ1 . . . (ϕ00 [Γ] → g( a1 , . . . , b1 , . . . , c1 , . . . ) ≤ b),   (14)

where ϕ00 [Γ] is quantiﬁer-free.
    To ﬁnd the smallest b such that (14) is valid, we can instead ﬁnd the largest g over all possible
values of a1 , . . . , b1 , . . . , c1 , . . . , ρ1 , . . . and set b to be this largest value. Thus, we can write down
the following constrained optimization problem:

                                            maximize                      g( a1 , . . . , b1 , . . . , c1 , . . . )
                                        a1 ,...,b1 ,...,c1 ,...,ρ1 ,...
                                                                                                                                  (15)
                                                  subject to              ϕ00 [Γ].

     Then we show how to solve this optimization problem.
     First, since constraint ϕ00 [Γ] is quantiﬁer-free, we can write the premise into disjunctive normal
form (DNF). This step can also be performed by machines [51]. An exemplary form of DNF for
ϕ00 [Γ] is ( a1 ≤ a2 ∧ a5 ≥ a6 ) ∨ (b1 = b2 ∧ b3 ≥ b4 ) ∨ (c1 ≥ c2 ).
     Second, (15) can be split into three optimization problems: to maximize g subject to a1 ≤
a2 ∧ a5 ≥ a6 , to maximize g subject to b1 = b2 ∧ b3 ≥ b4 , and to maximize g subject to c1 ≥ c2 . Each
of these is a ﬁxed-size constrained optimization problem, and thus can be solved by numerical
solvers (like Mathematica [33] or Gurobi [32]). Suppose the optimal values of these problems are
v1 , v2 , v3 . Then, we actually prove that

   • if b1 = b2 ∧ b3 ≥ b4 , then g(. . . ) ≤ v1 ;

   • if a1 ≤ a2 ∧ a5 ≥ a6 , then g(. . . ) ≤ v2 ;

   • if c1 ≥ c2 , then g(. . . ) ≤ v3 .

Finally, combining these results, we show that under constraint ϕ00 [Γ], g(. . . ) ≤ max{v1 , v2 , v3 }.
Thus, we can set b = max{v1 , v2 , v3 } as the ﬁnal approximation guarantee.



                                                                             33
B     Building blocks and their logic encodings
In this part, we show the building blocks in the literature and their logic encodings. For an
accessible presentation, we will use mathematical symbols rather than the LegoNE code. It is not
hard to see the equivalence between the mathematical symbols and the LegoNE code.

B.1    Inherent constraints
The deﬁnitions of payoff functions and regret functions themselves provide constraints. Here, we
list the inherent constraints for the payoff functions and regret functions.

    • For given i ∈ [r ], ∀ x(0 ≤ ui ( x) ≤ 1).
                                                                              0
    • For given i ∈ [r ], ∀ xi , ∀ x−i ( f i ( xi , x−i ) = maxxi0 ui ( xi , x−i ) − ui ( xi , x−i )).
                                                                0
    • For given i ∈ [r ], ∀ xi , ∀ x−i (maxxi0 ui ( xi , x−i ) ≥ ui ( xi , x−i )).
                                                        0
    • For given i ∈ [r ], ∀ x−i (maxxi0 ui ( xi , x−i ) ≤ 1).

B.2    Building blocks in the literature
We can collect most basic (polynomial-time computable) operations from the literature. Although
most of them are designed for two-player games, we can easily generalize them under the setting
of r-player games.

    • Random strategy: xi = Randomi().
       Description: Sample a random strategy xi for player i.
       Logic encoding: None.

    • Best response (ﬁrst occurred in [13]): xi = BestResponse( x−i ).
       Description: For a player i, given a strategy proﬁle x−i of the other players, ﬁnd the best
       response strategy xi = arg maxxi ∈∆n ui ( xi , x−i ).
                                                            i

       Logic encoding:
                                                        0                         0
                                                   ∀ xi (ui ( xi , x−i ) ≥ ui ( xi , x−i )).             (16)


       Remark B.1. The operation described in mathematical symbols is a “template” for the real
       code. In the LegoNE code, we need to instruct which i is used in the operation. Thus, the
       real code should be BestResponsei for player i.

    • Zero-sum NE (ﬁrst occurred in [15]): xi , x j = ZeroSumNE( x−i,j , u).
       Description: For a given linear combination u of payoffs u1 , . . . , ur and a strategy proﬁle x−i,j
       of the other players, ﬁnd the NE ( xi , x j ) of zero-sum two-player game u(·, ·, x−i,j ).
       Logic encoding:
                                               0            0
                                           ∀ xi (u( xi , x j , x−i,j ) ≥ u( xi , x j , x−i,j )) ∧
                                                    0               0                                    (17)
                                             ∀ x j (u( xi , x j , x−i,j ) ≤ u( xi , x j , x−i,j )).

                                                                        34
• Stationary point (ﬁrst occurred in [14]): xi , x j , yi , y j = StationaryPoint( x−i,j ).
  Description: Given a strategy proﬁle x−i,j of the other players, hold it ﬁxed and consider
  the two-variable objective max{ f i ( xi , x j , x−i,j ), f j ( xi , x j , x−i,j )} over players i and j’s mixed
  strategies. The building block returns a pair ( xi , x j ) that is a stationary point of this objective
  using linear programming, associated with two dual solutions yi and y j .
  Remark B.2. In the main text, StationaryPoint3 is used for three-player games. It is simply
  the above StationaryPoint instantiated with players (i, j) = (1, 2) and x−1,2 = z, where z is
  player 3’s current mixed strategy; it outputs ( xs , ys , w, zdual ) corresponding to ( x1 , x2 , y1 , y2 ).

  Logic encoding:

                                                     f i ( xi , x j , x−i,j ) = f j ( xi , x j , x−i,j ) ∧
                                                 0                                        0
                                             ∀ xi (ui (yi , x j , x−i,j ) ≥ ui ( xi , x j , x−i,j )) ∧
                                                 0                                                0
                                             ∀ x j (u j ( xi , y j , x−i,j ) ≥ u j ( xi , x j , x−i,j )) ∧
                                                                                      0       0
                                                              ∃ρ ∈ [0, 1], ∀ xi , ∀ x j ,
                                           0                     0                             0
                                                                                                                                    
   f i ( xi , x j , x−i,j ) ≤ ρ ui (yi , x j , x−i,j ) − ui ( xi , x j , x−i,j ) − ui ( xi , x j , x−i,j ) + ui ( xi , x j , x−i,j ) +
                               0                        0                                0
                                                                                                                               
              (1 − ρ) u j ( xi , y j , x−i,j ) − u j ( xi , x j , x−i,j ) − u j ( xi , x j , x−i,j ) + u j ( xi , x j , x−i,j ) .
                                                                                                                                      (18)
  Note that the quantiﬁer ∃ρ ∈ [0, 1] is treated as a parameter in the LegoNE code.

• Uniform mixing (ﬁrst occurred in [12]): xi = UniformMixing ( x1i , . . . , xis )
  Description: For a player i, given strategies x1i , . . . , xis , output the strategy xi = 1s ∑sk=1 xik .
  Logic encoding:
                                                                                                                  !
                                                              −i                  1 s
                                 ∀u ∈ Payoff, ∀ x                    u ( x , x ) = ∑ u ( xik , x −i )
                                                                           i   −i
                                                                                                                      ∧
                                                                                  s k =1
                                                                                  !                                                 (19)
                                         s
                                 −i         1
                            ∀x         ∑ s f j ( xik , x −i ) ≥ f j ( xi , x −i )                 for all j ∈ [r ], j 6= i.
                                       k =1

  The second part of the formula is the Jensen’s inequality over the convex function f j .

• Branching: IfThenElse( a, b, branch 1, branch 2)
  Description: Given certain values a, b, go to branch 1 if a ≥ b, and go to branch 2 otherwise.
  Logic encoding:

                [( a ≥ b) ∧ constraints in branch 1] ∨ [( a < b) ∧ constraints in branch 2].                                        (20)
  Note that operations max and min can be expressed by branch.

• Optimal mixing (occurred in every paper on ANE algorithms, ﬁrst formalized in [52]):

                      (s1∗ , . . . , sr∗ ) = OptimalMixing (s11 , . . . , s1t1 , . . . , s1r , . . . , srtr , u1 , . . . , ur ).    (21)


                                                                        35
      Description: Given a set of strategies s11 , . . . , s1t1 ∈ ∆n1 , . . . , s1r , . . . , srtr ∈ ∆nr , and payoff func-
      tions u1 , . . . , ur , the optimal mixing operation OptimalMixing outputs the strategy proﬁle
      (s1∗ , . . . , sr∗ ) that minimizes the function f on M, the set of all convex combinations of the
      strategies, i.e.,
                      (                                                                                              )
                                                                 tk                                     tk
          M=       ( s , . . . , s ) ∈ ∆ n1 × · · · × ∆ nr : s = ∑
                      1       r                            k
                                                                       αik sik ; αkj ≥ 0, j ∈ [tk ];   ∑ αik = 1, k ∈ [r]   .
                                                                i =1                                   i =1
                                                                                                                            (22)
      Logic encoding: It is very complicated and non-trivial to write down the logic encoding of
      the optimal mixing operation. We defer it to Section B.3.
    These operations are the basic building blocks for writing polynomial-time ANE algorithms.

B.3    Encoding of Optimal Mixing
The optimal mixing operation is the solution to a continuous optimization problem, which is not
directly expressible in logic formulas. Instead, we provide a formula that is implied by the optimal
mixing operation, namely, a necessary condition of the optimal mixing operation. Formally, we
have the following theorem.
Theorem B.3. For any ﬁxed r and t1 , . . . , tr , if x1o , . . . , xro are the output of the optimal mixing operation
given the input strategies sik , then there is a term L∗ such that
                                                                             
                 ϕ ( x1o , . . . , xro ) = OptimalMixing (s11 , . . . , srtr ) 7→ [ f ( x1o , . . . , xro ) ≤ L∗ ] (23)

and L∗ is expressed by f i values on the input strategies sik with arithmetic operations +, −, ×, ÷, <, >,
max, min operations over ﬁnite elements, and branch operations.
    Below we ﬁrst give a sketch of the proof of Theorem B.3. An overall tactic is to gradually
relax f ( x1o , . . . , xro ) to obtain the upper bound in the theorem.
   • First, we restrict the domain from M to the edges of M, which produces the ﬁrst upper
     bound.

   • Then, along each edge, replace f i with a linear upper bound li . The minimum of f on an
     edge is bounded by the minimum of max{l1 , . . . , lr }, which can be explicitly expressed by
     the f i values on the vertices of the edge.

   • Finally, the vertices of M are exactly the strategy proﬁle constructed by the input. Thus,
     we can ﬁnd an upper bound that is expressed by f i values on the constructed strategies.
    Now we provide the detailed proof of Theorem B.3. To simplify the notations, we below
assume that the number of input strategies for each player is the same, i.e., t1 = · · · = tr = t, and
the action sets are of the same size, i.e., n1 = · · · = nr = n. One can easily see that the general
case follows the same procedure.
    To further simplify the notations, we will use coefﬁcients rather than strategies to represent
the elements in M. Note that each element in M can be represented by its coefﬁcients (αik )k,i . The
coefﬁcients form a set A = ∆rt . The correspondence between the coefﬁcients and the strategies is
given by the following diagram:

                                                           36
                       αk = (α1k , . . . , αkt ) ∈ ∆t                      ∑it=1 αik sik ∈ ∆n
                                                                                                                       (24)
                                                                                                     
                        α = ( α1 , . . . , αr ) ∈ A             ∑it=1 α1i s1i , . . . , ∑it=1 αri sri ∈ M

    Then, we naturally deﬁne f i (α) and f (α) by its corresponding strategy proﬁles. Now, we can
give the detailed logic encoding of the optimal mixing operation.
    First, A is a polytope, whose vertices are in form of (α1 , . . . , αr ), where αk ∈ {e1 , . . . , et }. The
vertices correspond to the strategy proﬁles constructed by the inputs skj . The edges of A are in
form of       n                                                                                                      o
                (ei1 , . . . , eik−1 , λeik + (1 − λ)eik0 , eik+1 , . . . , eir ) : λ ∈ [0, 1], i1 , . . . , ir ∈ [t] . (25)

   Intuitively, an edge is the segment between two adjacent vertices, with only one αk varying.
To simplify the discussion, when we refer to a speciﬁc edge E, we will use the above form to
represent it. Denote the union of all edges as E . Then, we clearly have the following lemma.
Lemma B.4. E ⊆ A. Thus,

                                 min f (α) ≤ min f (α) =                min           min f (α).                       (26)
                                 α∈A              α∈E              E is an edge of A α∈ E

    By this lemma, if we can ﬁnd an upper bound of minα∈E f (α) for each edge E, then we can
ﬁnd an upper bound of minα∈A f (α).
    An important observation of f i is that along each edge E, only one αk = λeik + (1 − λ)eik0
varies, and thus f i is a function in λ. By scrutinizing the deﬁnition of f i , we have the following
lemma.
Lemma B.5. For each edge E and each i ∈ [r ], f i is a convex function on E.
Proof. Then, by the deﬁnition of f i , f i (α) = g(λ), where g has the form

                  1 ( λeik + (1 − λ ) eik0 ), . . . , an ( λeik + (1 − λ ) eik0 )} − b ( λeik + (1 − λ ) eik0 ).
            max{ aT                                    T                              T
                                                                                                                       (27)

Since max is a convex function and the addition/composition of convex function with a linear
function is still convex, g is convex. Thus, f i is convex on E.

   By Lemma B.5, using Jensen’s inequality, we have the following lemma, which actually gives
an upper bound of f i on each edge.
Lemma B.6. For each edge E and each i ∈ [r ], let αk = λeik + (1 − λ)eik0 be the varying coefﬁcient on E.
Then, f i (α) ≤ λ f i (ei1 , . . . , eik , . . . , eir ) + (1 − λ) f i (ei1 , . . . , eik0 , . . . , eir ).
    Now, the upper bound given by (26) becomes:
                                                       n                                                          o
         min f (α) ≤       min          min max λ f i (. . . , eik , . . . ) + (1 − λ) f i (. . . , eik0 , . . . ) .   (28)
         α∈A         E is an edge of A λ∈[0,1] i ∈[r ]
                                       |                                 {z                                       }
                                                                                 TE

   Finally, to prove Theorem B.3, we need to show that TE can be explicitly expressed by f i
values on the vertices of E. The explicit expression of TE can be given by the following lemma.

                                                              37
Lemma B.7. For each edge E, suppose ai = f i (. . . , eik , . . . ) and bi = f i (. . . , eik0 , . . . ) for i ∈ [r ]. Let
li (λ) = ai (1 − λ) + bi λ, i ∈ [r ]. Then

    TE = min{ max{ a1 , . . . , ar },
                    max{b1 , . . . , br },
                                   
                                   maxk∈[r] lk (( ai − a j )/( ai + b j − a j − bi )),
                                                                                              if ai > a j and bi < b j ,
                                                                                                                               (29)
                   for all i 6= j, maxk∈[r] lk (( ai − a j )/( ai + b j − a j − bi )),         if ai < a j and bi > b j ,
                                   
                                   
                                      1,                                                       otherwise.
                 }.

Proof. Essentially, TE is the maximum of r linear functions l1 , . . . , lr in λ. Thus, its minimum on
[0, 1] must be one of the following points:
    • the endpoint λ = 0 with the minimum value max{l1 (0), . . . , lr (0)},

    • the endpoint λ = 1 with the minimum value max{l1 (1), . . . , lr (1)}, or

    • the points where li intersects with l j for some i 6= j at λ∗ , with the minimum value
      max{l1 (λ∗ ), . . . , lr (λ∗ )}.

     For the last case, li and l j intersect if and only if at the li , l j values have intersection on λ ∈ [0, 1],
i.e., ai > a j and bi < b j , or, ai < a j and bi > b j . Then, under this condition, li (λ∗ ) = l j (λ∗ ) implies
that λ∗ = ( ai − a j )/( ai + b j − a j − bi ). Note that ai = f i (. . . , eik , . . . ) and bi = f i (. . . , eik0 , . . . ). Since
all expressions are given by ai and bi , TE can be expressed by f i values on the vertices of E as in
the lemma.

    Finally, we prove Theorem B.3.

Proof of Theorem B.3. By Lemma B.7, TE can be expressed by f i values on the vertices of E. Then,
since there are only a ﬁxed number of vertices (and hence edges) in A, by Lemma B.4, we have
that the upper bound
                                         min      TE = L∗                                    (30)
                                                   E is an edge of A

can be expressed by f i values on the vertices of A, which completes the proof.

Remark B.8. For two-player games, there is an alternative logic encoding for the optimal mixing
operation, which is implicitly used in [26] and [12]. The main idea as follows.

    • First, we restrict the domain not to the edges of M, but to the diagonal of M. That is, for
      strategy proﬁle ( x1 , x2 ) and (y1 , y2 ), we restrict the domain to {(λx1 + (1 − λ)y1 , λx2 + (1 −
      λ)y2 ) : λ ∈ [0, 1]}.

    • Then, instead of using linear upper bounds for the whole f i on the diagonal, we only relax
      the maximum term max( x1 )0 u1 (( x1 )0 , x2 ) or max( x2 )0 u2 ( x1 , ( x2 )0 ) to a linear function. By
      doing so, f i is relaxed to a quadratic function qi , and f is relaxed to max{q1 , q2 }.

    • The minimum of max{q1 , q2 } on the diagonal can be explicitly expressed by f i values on
      the vertices of M, which gives a different upper bound of the optimal mixing operation.

                                                                38
However, this encoding requires much more time to compute the ﬁnal approximation guarantee
than what we have shown in the main body. Thus, we do not use this encoding in the current
LegoNE.




                                           39
C     Extensions of LegoNE
In this part, we show that the LegoNE framework can be extended to handle more general
algorithmic problems.

C.1   Example 1: ANE Algorithms in Polymatrix Games
In the ﬁrst example, we extend the LegoNE framework from r-player games to polymatrix games.
     Polymatrix games are a special kind of ﬁnite normal-form and graphical games. In a polyma-
trix game, the strategic interactions between players are captured by a graph G = (V, E), where
the nodes V correspond to players, and edges E indicate direct dependencies between players’
utilities. Then, for any strategy proﬁle x = ( xi )i∈V of all players, the payoff function ui of player
i is only determined by the strategies of its neighbors N (i ) in the graph:
                                            u i ( x ) = ( x i )T     ∑ Aij x j ,                              (31)
                                                                   j ∈ N (i )

where x j is the strategy of player j, and Aij is the payoff matrix between players i and j. Besides,
for the simplicity, in this part, for any two strategy proﬁles x and x̃, we use the notation ( x; x̃) to
denote the strategy proﬁle ( xi , x̃−i ) for all players i.
    Since polymatrix games are also ﬁnite normal-form games, we can directly use the same loss-
function representation as in r-player games. That is, for any strategy proﬁle x, we deﬁne the
loss function for each player i as
                                          f i ( x) = max ui ( x̃; x) − ui ( x),                               (32)
                                                        x̃

and the approximation function f ( x) = maxi f i ( x).
    The only known ANE algorithm for polymatrix games [28] has an approximation guarantee
of (1/2 + δ). We now show how to extend the LegoNE framework to prove this result. Following
the LegoNE framework, we ﬁrst give the Floyd-Hoare semantics of the ANE algorithm. Then, we
use the instantiation and forgetting tactics to decide its validity in ﬁrst-order logic over the reals
(FOL-R), denoted FOLR .
    For the ﬁrst step, we need to encode an ANE algorithm into a logic formula. We consider
the algorithm given by [28]. This algorithm uses a similar gradient-descent approach proposed
in [14] to compute and output the stationary point x∗ of f . The encoding of the stationary point
comes from equation (11) and deﬁnition (5) in [28]:
             ∀ x0 [ f ( x∗ ) ≤ max D f iδ ( x∗ ; x0 ) + δ
                               i
                                                                                                              (33)
                  ∧ ∀i ( D f i ( x ; x ) ≤ max ui (y; x0 ) − ui ( x∗ ; x0 ) − ui ( x0 ; x∗ ) + ui ( x∗ ))].
                              δ ∗ 0
                                            y

Here, δ is some ﬁxed real constant.
     Note that now the universal quantiﬁer ∀i is ranging over all players, instead of a ﬁxed number
r of players.
     For the second step, we show how to do the instantiation and forgetting. The key idea
is, although there are unboundedly many players, we only use a ﬁnite number of approaches to
handle them. The forgetting actually already occurs when we denote ( xi , x̃−i ) by ( x; x̃), where we
use a uniﬁed notation for all players i. We further do the forgetting to eliminate other occurrences
of i in the encoding:

                                                             40
   • Denote functions maxi D f iδ by v and ui by u. By doing so, in notations D f iδ and ui , the
     distinctions between different players vanish.

   • After eliminating the occurrences of i, the derived upper bound of D f iδ ( x∗ ; x0 ) will hold for
     any i. Thus, it also holds for maxi D f iδ ( x∗ ; x0 ), and we can replace it by v( x∗ ; x0 ).

    Thus, after eliminating the occurrences of i by forgetting, the encoding can be rewritten in
the following form:

                   ∀ x0 [ f ( x∗ ) ≤ v( x∗ ; x0 ) + δ
                          ∧ v( x∗ ; x0 ) ≤ max u(y; x0 ) − u( x∗ ; x0 ) − u( x0 ; x∗ ) + u( x∗ )].     (34)
                                               y

    Next, we instantiate x0 . The choice of x0 is similar to that in LegoNE: x∗ , the stationary point,
and x, the best response of all players against x∗ (i.e., xi = arg maxxi ui ( xi , ( x∗ )−i )). Moreover, by
the deﬁnition of best response, we have maxy u(y; x∗ ) = u( x; x∗ ).
    Thus, the instantiation of x0 leads to the following formula:

                           f ( x∗ ) ≤ v( x∗ ; x) + δ
                        ∧ v( x∗ ; x∗ ) ≤ max u(y; x∗ ) − u( x∗ ) − u( x∗ ) + u( x∗ )
                                               y

                        ∧ v( x ; x) ≤ max u(y; x) − u( x∗ ; x) − u( x; x∗ ) + u( x∗ )
                                 ∗                                                                     (35)
                                           y

                        ∧ max u(y; x∗ ) = u( x; x∗ ).
                             y

Here we use u( x∗ ; x∗ ) = u( x∗ ) by deﬁnition.
   To be clearer, we can write it by substituting same terms by the same real variables to get a
ﬁrst-order real arithmetic formula:
                                         a ≤ b+δ∧a ≤ c+δ
                                      ∧ b ≤ d−e∧c ≤ d− f −g+e                                          (36)
                                      ∧ d = g.

    Using this formula and the inherent formulas (i.e., all variables are in [0, 1]), we can again
use cylindrical algebraic decomposition (CAD) to prove that the approximation guarantee of this
algorithm is (1/2 + δ), which can also be checked by humans.
    The above use of instantiation and forgetting is not dependent on any particular property of
polymatrix games. Thus, it can actually be used for other kinds of graphical games (provided
we have a proper programming language like LegoNE). Besides, the derivation above is easier
than [28], which instantiates the formula with ( x + x)/2 instead, without justifying the choice
of the coefﬁcient 1/2. However, under our framework, the choice of 1/2 is also justiﬁed by the
proof.
    Finally, from a higher-level view, this example shows that by recursively applying forgetting
and instantiation tactics, we can handle unboundedly many encodings that have a ﬁnite repre-
sentation using indices.




                                                         41
C.2   Example 2: Linear Programming Relaxations with Rounding Techniques
In the second example, we show that LegoNE-style framework can be extended beyond ANE
algorithms. Speciﬁcally, we consider the approximation analysis of algorithms designed using
linear programming (LP) relaxations with rounding techniques.
    LP relaxations with rounding techniques are widely used to design polynomial-time approxi-
mation algorithms for combinatorial optimization problems [8]. The key idea is to ﬁrst represent
the problem as an integer linear program (ILP), then relax it to a linear program (LP), and ﬁnally
round the solution of the LP to an integer solution [8]. As a concrete example, we consider
the vertex cover problem to illustrate how machines can prove the approximation ratios for its
algorithm.
    Given a graph G = (V, E), a vertex cover is a subset V 0 ⊆ V such that each edge in E has
at least one endpoint in V 0 . The optimization problem is to ﬁnd a minimum-size vertex cover.
However, the decision version of vertex cover is NP-complete [53]. Thus, we have to resort to
polynomial-time approximation algorithms.
    To state such an algorithm, we ﬁrst formulate the vertex cover problem as an integer linear
program (ILP), denoted as ILP(V, E), formulated as follows:
                                minimize      ∑ xv
                                              v ∈V
                                subject to   xu + xv ≥ 1, ∀(u, v) ∈ E,                              (37)
                                             xv ∈ {0, 1}, ∀v ∈ V.
The optimal solution is a binary vector x ∗ ∈ {0, 1}V , corresponding to a vertex cover, where
xv∗ = 1 if and only if v is in the cover.
    Then we present the desired algorithm Γ with two steps as follows:
   1. x = sol(LP(V, E)): We relax the ILP to a linear program (LP) by relaxing the constraints
      xv ∈ {0, 1} to 0 ≤ xv ≤ 1. The LP is denoted as LP(V, E). Solve LP(V, E) and we can get a
      fractional solution x.
   2. x 0 = Round( x ): We then round x to an integer solution x 0 by setting xv0 = 1 if xv ≥ 1/2, and
      = 0 otherwise. Output x 0 as the solution.
    It was shown that the output x 0 of this algorithm is indeed a vertex cover and the approxima-
tion ratio of algorithm Γ is 2 [8], i.e., the size of the output is at most twice the size of the optimal
solution. Now, let us see how the LegoNE framework can be extended for the approximation
analysis of this algorithm. Here, we do not consider how to prove the correctness (i.e., Algorithm
Γ is indeed a polynomial-time vertex-cover algorithm) by machines. Again, we need to 1. give the
Floyd-Hoare semantics of the algorithm; 2. use the instantiation and forgetting tactics to decide
its validity in FOLR .
    For the ﬁrst step, just like ANE algorithms, algorithm Γ can be seen as a combination of two
building blocks: LP and Round, and we can encode them as follows:
   • Since we relax the constraints, the optimal objective value ∑v∈V xv of LP(V, E) is no more
     than the optimal objective value of ILP(V, E). Denote the optimal solution to ILP(V, E) as
     x ∗ , the encoding of x = sol(LP(V, E)) is:
                                                          !
                                               ∑ xv ≤ ∑ xv∗      .                                  (38)
                                              v ∈V        v ∈V


                                                     42
   • By simple reasoning, the encoding of x 0 = Round( x ) is:
                                                   ∀v( xv0 ≤ 2xv ).                            (39)

   • We also have an inherent encoding of x ∗ as the optimal solution of ILP(V, E):
                                                          !
                                           ∀y       ∑ xv∗ ≤ ∑ yv               ,               (40)
                                                   v ∈V              v ∈V

     where the domain of y is all feasible solutions of ILP(V, E).
    For the second step, we encounter a problem that resembles those in Section C.1: We have
unboundedly many variables and constraints, but they are ﬁnitely represented using indices.
Our solution is similar. Facing notation xv , we forget the information given by subscript v and
treat xv equally for all v’s.
    Bearing this idea, we can present the instantiation tactics on ∀y and ∀v:
   • For y, its value can only be either x 0 or x ∗ . Other choices are unlikely to produce.
   • For v, to eliminate the quantiﬁer ∀v, we have a different approach from Section C.1. Here,
     by the characteristic of the sum operator, we can handle it by summing up over all v’s, i.e.,
     from premise ∀v( f (v) ≤ g(v)) to derive a conclusion ∑v f (v) ≤ ∑v g(v). In this way, the
     quantiﬁer ∀v is eliminated.
   Following the above elimination deductions, we can derive

                                    ∑ xv0 ≤ ∑ (2xv ) = 2 ∑ xv                                  (41)
                                    v ∈V          v ∈V                  v ∈V

from ∀v( xv0 ≤ 2xv ), and
                                  ∑ xv∗ ≤ ∑ xv0 ∧ ∑ xv∗ ≤ ∑ xv∗                                (42)
                                 v ∈V       v ∈V              v ∈V          v ∈V

from ∀y(∑v xv∗ ≤ ∑v yv ). We also know from the encoding of x = sol(LP(V, E)) that

                                            ∑ xv ≤ ∑ xv∗ .                                     (43)
                                           v ∈V               v ∈V

The goal of the proof is to show that

                                           ∑ xv0 ≤ 2 ∑ xv∗ .                                   (44)
                                           v ∈V               v ∈V

    Again, we can use the forgetting tactic. We can treat sum terms as whole notations. By doing
so, all derived inequalities and the proof goal only involves real-valued terms, and need to show:
                            ( a ≤ 2b ∧ c ≤ a ∧ c ≤ c ∧ b ≤ c) → a ≤ 2c.                        (45)
This problem also reduces to deciding the validity of a formula in FOLR . We can again use CAD
to solve this problem.
    Importantly, the above instantiation and forgetting procedure does not depend on the speciﬁc
structure of the vertex cover problem. It only concerns the form of ILP and our treatment on
indices. Thus, the above procedure can be applied to other linear programming relaxations with
rounding techniques.

                                                         43
