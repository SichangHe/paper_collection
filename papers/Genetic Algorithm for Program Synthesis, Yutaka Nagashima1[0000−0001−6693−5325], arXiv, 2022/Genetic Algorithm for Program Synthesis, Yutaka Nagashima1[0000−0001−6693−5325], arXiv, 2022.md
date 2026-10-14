                                                Genetic Algorithm for Program Synthesis

                                                              Yutaka Nagashima1[0000−0001−6693−5325]

                                                                  Independent, Cambridge, the UK
arXiv:2211.11937v2 [cs.NE] 19 Jan 2023




                                               Abstract. A deductive program synthesis tool takes a specification as
                                               input and derives a program that satisfies the specification. The draw-
                                               back of this approach is that search spaces for such correct programs tend
                                               to be enormous, making it difficult to derive correct programs within a
                                               realistic timeout. To speed up such program derivation, we improve the
                                               search strategy of a deductive program synthesis tool, SuSLik, using evo-
                                               lutionary computation. Our cross-validation shows that the improvement
                                               brought by evolutionary computation generalises to unforeseen problems.


                                         1   Introduction

                                         A far-fetched goal of artificial intelligence research is to build a system that
                                         writes computer programs for humans. To achieve this goal, researchers take
                                         two distinct approaches: deductive program synthesis and inductive program
                                         synthesis. Both approaches attempt to produce programs requested by human
                                         users. The difference lies how they produce programs: deductive synthesis tries
                                         to deduce programs that satisfy specifications, while inductive program synthesis
                                         tries to induce programs from examples.
                                             While such inductive synthesis alleviates the burden of implementation by
                                         guessing programs from given input-output examples, in inductive synthesis re-
                                         sulting programs are not trustworthy. Deductive synthesis overcomes this lim-
                                         itation with formal specifications: it allows users to formalise what they want
                                         as specifications, whereas inductive synthesis tools guess how programs should
                                         behave from examples provided by users. Thus, in deductive synthesis providing
                                         formal specifications remains as users’ responsibility. The upside of deductive
                                         synthesis is, however, users can obtain correct programs upon success.
                                             SuSLik [19], for example, is one of such deductive synthesis tools. It takes a
                                         specification provided by humans and attempts to produce heap-manipulating
                                         programs satisfying the specification in a language that resembles the C lan-
                                         guage. Internally, this derivation process is formulated as proof search: SuSLik
                                         composes a heap-manipulating program by conducting a best-first search for
                                         a proof goal presented as specification. The drawback is that the search algo-
                                         rithm often fails to find a proof within a realistic timeout. That is, even we
                                         pass a specification to SuSLik, SuSLik may not produce a program satisfying
                                         the specification. According to Itzhaky et al. [5], different synthesis tasks benefit
                                         from different search parameters, and that we might need a mechanism to tune
                                         SuSLik ’s search strategy for a given synthesis task.
2        Y. Nagashima

2    SuSLik’s Search Strategy

SuSLik synthesises a program by searching for a corresponding proof. We can
see SuSLik’s proof search as an exploration of an OR-tree, nodes of the tree
represent (intermediate) synthesis goals, while edges of the tree represent rule
applications. The shape of such search tree is not known in advance, and the
task of SuSLik is to identify a solved node, in which a proof is complete.
    Since such OR-trees can
be too large to find proofs current generation                                              training
within a realistic timeout, champion other winners                     losers               dataset

SuSLik narrows the search               A        B      C    D       E        F       G
                                             A    B                   E        F        G
space using a proof strategy.                                                                  H


Essentially, proof strategy in       next generation                                       validation
SuSLik is a function that                        mutated
                                                           other winners
                                                                               mutated      dataset
                                   champion
                                                champion                        winners
takes a synthesis goal and re-
turns an ordered list of rules          A
                                          A  A    A’
                                                 A’    A’’   B       CC       B’
                                                                              B’      C’C’

to apply next. Itzhaky et al.
developed the default strat-                Fig. 1: Mutation and Elitist Selection
egy by manually encoding hu-
man expertise. For example, the default strategy precludes the application of a
rule called CALL when another rule CLOSE has been applied before reaching the
current node. This way, the SuSLik rules are grouped into 10 ordered lists, and
the order of these rules in the lists define how SuSLik explores the corresponding
OR-tree.
    Another decision SuSLik has to make for an effective search is to select the
next node to expand. The current version of SuSLik make this decision using a
cost function, manually developed and tuned by Itzhaky et al. [5].
    Both the weights of the cost function and orders of derivation rules are manu-
ally tuned for the benchmark used in their evaluation [5]; however, as we show in
Section 4, our evolutionary framework finds better strategies through evolution.


3    Evolutionary Computation for SuSLik

The aim of our evolutionary computation is to optimise the order of each group of
derivation rules and the weights of the cost function, which is used to implement
best-first search.
    Algorithm 1 summarises the genetic algorithm we used in our framework
to improve the search strategy of SuSLik. Firstly, the algorithm takes a set
of training problems an inputs, using which we evolve SuSLik instances over 40
generations. Line 1 defines the initial population. Each individual in a population
is evaluated according to the fitness function described in Section 3.
    For each generation, we copy individuals from the previous iteration (Line 6),
mutate them (Line 7), evaluate individuals (Line 8). Then, we sort all individuals
in the current generation based on their performance (Line 9 - 10). And we
continue to the next generation using the best 20 individuals from the current
                                   Genetic Algorithm for Program Synthesis         3

pool. In the following, we explain the mutation algorithm, the fitness function,
and our selection algorithm.

Mutation. As we explained in Section 2, by default a search strategy of SuSLik
is defined by two factors: the order of rule application and weights of each node
in the search tree. To determine an effective way to apply genetic algorithms
to program synthesis in SuSLik, we implemented the following three different
mutation algorithms:

 – Order-only mutation changes only the order of rule application for each node.
 – General rule-weight mutation changes the weights of each node based on
   what rules have been applied to reach that node.
 – Goal-specific rule-weight mutation allows SuSLik to choose a weight for each
   rule based on properties of a node during a search.

Fitness. The fitness function mea-
sures the performance of SuSLik in-       Algorithm 1 Evolutionary Computa-
stances. More specifically, it measures   tion for SuSLik
how many derivation problems each
                                          Input: synthesis problems for SuSLik
SuSLik instance solves within the         Output: a SuSLik search strategy
timeout of 2.5 seconds for each prob-
lem. When multiple SuSLik instances        1: Let old_pop be the initial population.
solve the same number of derivation        2: fitness(old_pop)
problems, the fitness function uses        3: generation ← 1
the numbers of rules fired by the in-      4: while generation ≤ 40 do
stances as a tie-breaker: it considers     5:    generation ← generation + 1
that the instance that solves a certain    6:    new_pop ← old_pop
number of problems with a smaller          7:    mutate(new_pop)
                                           8:    fitness(new_pop)
number of rule applications is bet-
                                           9:    whole_pop ← old_pop + new_pop
ter than another instance that solves     10:    sort (whole_pop)
the same number of problems with a        11:    old_pop ← take (whole_pop, 20)
larger number of rule applications.       12: end while

Selection. We adopt a version of elitist
selection as our selection method: we pass individuals from the current genera-
tion to the next generation. by copying them and mutating them if they show
better performance in the current generation. Figure 1 provides the schematic
view of our elitist selection. Unlike the standard elitist selection algorithm, ours
prioritizes the best individual in each generation to speed up the evolution: the
best individual in each generation, called champion, is entitled with three chil-
dren, one original copy without mutation and two mutated children, whereas
each of other 19 winners has one original copy and only one mutated child in
the next generation.

 Note that each individual has two kinds of properties to mutate: the order of
derivation rules, and weights used in the cost function. While we represent the
4       Y. Nagashima

weights as floating point numbers, we adopt permutation encoding for the orders
of derivation rules.
    For each permutation encoding, each individual has the probability of 0.1 to
be moved, while we change weights by multiplying a random number between 0.8
and 1.2. In our framework, we do not apply crossover to permutation encoding:
since our sequences denoting rule orders tend to be short, we are not sure if
crossovers would result in a better performance of evolution.
    Our evolutionary computation for program synthesis differs from genetic pro-
gramming [9] or evolutionary programming [1]: we did not directly apply simu-
lated evolution to programs, but our framework improves the search mechanism
for deriving correct programs through evolution. We take this approach to take
the best of both worlds: the correctness of resulting programs guaranteed by the
deductive synthesis and its certification tool, and the search heuristics enhanced
through evolutionary computation.


4    Evaluation

We conducted cross-validations to evaluate what improvements our evolutionary
computation framework brought to SuSLik. We measured how many synthesis
problems SuSLik failed to solve with in 2.5 seconds of timeout. For this eval-
uation, we used a consumer laptop running Ubuntu 20.04.3 LTS on a machine
with 16 CPUs of AMD Ryzen 7 4,800H with Radeon Graphics and 15,854MB
of main memory.
    As SuSLik is a new tool, we have only 65 problems available in our bench-
mark: problems from a preceding work on SuSLik [5] and new problems prepared
for this project. These problems include tasks on various data-structures such as
integers, singly linked lists, sorted lists, doubly linked lists, lists of lists, binary
trees, and packed trees.
    Firstly, we randomly split our benchmarks into two groups: the validation
dataset and training dataset. Then, using the training dataset we apply our
evolutionary computation described in Algorithm 1 to evolve SuSLik’s search
strategy. As explained in Section 3, the output of our evolutionary computa-
tion is just one search strategy produced after 40 generations. However, in this
experiment we conducted cross-validations using the best individual from the
training set for each generation to see how our framework produces transferable
improvement over generations.
    To reduce the influence from a specific random split, we conducted this exper-
iment four times, and the result of each experiment is illustrated from Figure 2
to Figure 5. In these figures, the horizontal axes represent the number of genera-
tions, while the vertical axes represent the number of synthesis problems SuSLik
did not solve within the timeout.
    These figures show that when adopting the general rule-weight mutation,
our evolutionary framework managed to improve SuSLik’s capability to find
solutions in validation sets, even though evolution is based on training sets.
That is, somewhat contrarily to the prediction by Itzhaky introduced in Section
                                                                     Genetic Algorithm for Program Synthesis                                            5



Unsolved problems out of 33.




                                                                               Unsolved problems out of 24.
                                                         order-only                                           18
                               22
                                                    general rule-weight
                                                  goal-specific rule-weight
                               20
                                                                                                              16

                               18
                                                                                                                              order-only
                                                                                                              14         general rule-weight
                               16                                                                                      goal-specific rule-weight
                                    0        10       20       30         40                                       0        10      20       30    40
                                                   Generation.                                                                   Generation.

                                    Fig. 2: Cross-validation 1                                                     Fig. 3: Cross-validation 2

                               22

                                                                               Unsolved problems out of 34.
Unsolved problems out of 34.




                                                                                                              24

                               20                                                                             22

                               18                                                                             20

                                                                                                              18
                               16
                                               order-only                                                                     order-only
                                          general rule-weight                                                 16         general rule-weight
                               14       goal-specific rule-weight                                                      goal-specific rule-weight
                                                                                                              14
                                    0        10       20       30         40                                       0        10      20       30    40
                                                   Generation.                                                                   Generation.

                                    Fig. 4: Cross-validation 3                                                     Fig. 5: Cross-validation 4


1, we found that there are strategies that tend to perform better for unforeseen
problems, and we can find such strategies using evolutionary computation.
    On the other hand, the order-only mutation and goal-specific rule-weight
mutation resulted in less promising results. In particular, the goal-specific rule-
weight mutation over-fitted to training data in Figure 2 and Figure 5, probably
due to its capability to fine tune the strategy for our small dataset.


5                              Discussion

The limited size of available dataset is the main challenge we faced in this project.
This problem is partially unavoidable since program synthesis itself is still an
emerging field in Computer Science. Other AI projects for interactive theorem
provers take advantage of large existing proof corpora for training. For example,
Nagashima built a tactic prediction tool, PaMpeR [16], for Isabelle/HOL by ex-
tracting 425,334 data points [13] from the Archive of Formal Proofs (AFP) [8]. Li
6       Y. Nagashima

et al. also mined the AFP and produced 820K training examples for conjectur-
ing. For Coq, Yang et al. constructed a dataset containing 71K proofs from 123
projects [21], whereas Huang et al. [4] extracted a dataset consisting of 1,602 lem-
mas from the Feit-Thompson formalization. For HOL Light [3], The HOLStep [6]
used 1,013,046 training examples and 196,030 testing examples extracted from
11,400 proofs, while the HOList project presented a benchmark based on 2,199
definitions and 29,462 theorems and lemmas. These projects managed to gather
large data sets since their underlying theorem provers, Isabelle/HOL, Coq, and
HOL Light, have a larger user base than SuSLik [19] does.
    For the moment, our framework improves static parameters for SuSLik. That
is, the resulting weights and rule orders are fixed for all intermediate synthe-
sis problems. Our evaluation has shown that our static parameter optimisation
(general rule-weight mutation) using evolutionary computation generalises well:
a SuSLik instance that performs well for a training dataset tends to perform
well for an evaluation dataset. We expected that we could achieve even better
performance by producing dynamic parameters (goal-specific rule-weight) for
SuSLik: functions that inspect a node at hand and decide on a promising rule
order and weights for that node. Our efforts in this direction are, unfortunately,
unsuccessful so far. We hope that a larger training dataset would allow for such
optimisation in the future.


6   Related Work

Despite the current trend of applying deep learning to theorem proving, we
consciously avoided deep learning in this project, as we have a limited number
of synthesis problems at hand.
     Even though there was an attempt to use reinforcement learning [20] for a
connection-style proof search [7]; we mindfully chose evolutionary computation
over reinforcement learning: since we do not have a changing environment in our
setting, it is unclear if we gain any benefits from having two metrics, reward func-
tion for the long term goal and value function for the short term benefit. Instead,
we improved SuSLik’s default search strategy for randomly chosen fixed training
problem sets and measured how the improvement generalizes to validation sets.
     When implementing our framework for evolutionary computation, we took
the advantage of a Python framework for evolutionary computation called DEAP
[2], even though SuSLik itself is implemented in Scala.
     Previously, we attempted to improve proof strategies [17] for Isabelle/HOL
using evolutionary computing [11]. However, the focus of that project shifted to
the prediction of induction arguments [14,15] using meta-languages [10,12].
     Nawaz et al. used a genetic algorithm to evolve random proof sequences to
target proofs. The drawback of their approach is that the fitness function used
in the genetic algorithm relies on the existence of a proof for a given problem.
Therefore, this framework is not applicable to open conjectures without existing
proofs [18].
                                    Genetic Algorithm for Program Synthesis          7

Acknowledgment
We would like to thank Andreea Costea for preparing additional SuSLik prob-
lems for cross-validations.

References
 1. Fogel, L., Owens, A.J., Walsh, M.J.: Artificial intelligence through simulated evo-
    lution (1966)
 2. Fortin, F.A., De Rainville, F.M., Gardner, M.A., Parizeau, M., Gagné, C.: DEAP:
    Evolutionary algorithms made easy. Journal of Machine Learning Research 13,
    2171–2175 (jul 2012)
 3. Harrison, J.: HOL Light: A tutorial introduction. In: Srivas, M.K., Camilleri, A.J.
    (eds.) Formal Methods in Computer-Aided Design, First International Conference,
    FMCAD ’96, Palo Alto, California, USA, November 6-8, 1996, Proceedings. Lecture
    Notes in Computer Science, vol. 1166, pp. 265–269. Springer (1996). https://doi.
    org/10.1007/BFb0031814, https://doi.org/10.1007/BFb0031814
 4. Huang, D., Dhariwal, P., Song, D., Sutskever, I.: Gamepad: A learning environ-
    ment for theorem proving. In: 7th International Conference on Learning Repre-
    sentations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019. OpenReview.net
    (2019), https://openreview.net/forum?id=r1xwKoR9Y7
 5. Itzhaky, S., Peleg, H., Polikarpova, N., Rowe, R.N.S., Sergey, I.: Deductive syn-
    thesis of programs with pointers: Techniques, challenges, opportunities - (in-
    vited paper). In: Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification
    - 33rd International Conference, CAV 2021, Virtual Event, July 20-23, 2021,
    Proceedings, Part I. Lecture Notes in Computer Science, vol. 12759, pp. 110–
    134. Springer (2021). https://doi.org/10.1007/978-3-030-81685-8_5, https:
    //doi.org/10.1007/978-3-030-81685-8_5
 6. Kaliszyk, C., Chollet, F., Szegedy, C.: Holstep: A machine learning dataset for
    higher-order logic theorem proving. In: 5th International Conference on Learn-
    ing Representations, ICLR 2017, Toulon, France, April 24-26, 2017, Conference
    Track Proceedings. OpenReview.net (2017), https://openreview.net/forum?id=
    ryuxYmvel
 7. Kaliszyk, C., Urban, J., Michalewski, H., Olsák, M.: Reinforcement learn-
    ing of theorem proving. In: Bengio, S., Wallach, H.M., Larochelle, H.,
    Grauman, K., Cesa-Bianchi, N., Garnett, R. (eds.) Advances in Neural In-
    formation Processing Systems 31: Annual Conference on Neural Informa-
    tion Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montréal,
    Canada. pp. 8836–8847 (2018), https://proceedings.neurips.cc/paper/2018/
    hash/55acf8539596d25624059980986aaa78-Abstract.html
 8. Klein, G., Nipkow, T., Paulson, L., Thiemann, R.: The Archive of Formal Proofs
    (2004), https://www.isa-afp.org/
 9. Koza, J.R.: Genetic programming - on the programming of computers by means
    of natural selection. Complex adaptive systems, MIT Press (1993)
10. Nagashima, Y.: LiFtEr: Language to encode induction heuristics for Isabelle/HOL.
    In: Lin, A.W. (ed.) Programming Languages and Systems - 17th Asian Sympo-
    sium, APLAS 2019, Nusa Dua, Bali, Indonesia, December 1-4, 2019, Proceedings.
    Lecture Notes in Computer Science, vol. 11893, pp. 266–287. Springer (2019).
    https://doi.org/10.1007/978-3-030-34175-6_14, https://doi.org/10.1007/
    978-3-030-34175-6_14
8       Y. Nagashima

11. Nagashima, Y.: Towards evolutionary theorem proving for Isabelle/HOL. In:
    López-Ibáñez, M., Auger, A., Stützle, T. (eds.) Proceedings of the Genetic and
    Evolutionary Computation Conference Companion, GECCO 2019, Prague, Czech
    Republic, July 13-17, 2019. pp. 419–420. ACM (2019). https://doi.org/10.1145/
    3319619.3321921, https://doi.org/10.1145/3319619.3321921
12. Nagashima, Y.: Definitional quantifiers realise semantic reasoning for proof by
    induction. CoRR abs/2010.10296 (2020), https://arxiv.org/abs/2010.10296
13. Nagashima, Y.: Simple dataset for proof method recommendation in isabelle/hol.
    In: Benzmüller, C., Miller, B.R. (eds.) Intelligent Computer Mathematics - 13th
    International Conference, CICM 2020, Bertinoro, Italy, July 26-31, 2020, Proceed-
    ings. Lecture Notes in Computer Science, vol. 12236, pp. 297–302. Springer (2020).
    https://doi.org/10.1007/978-3-030-53518-6_21, https://doi.org/10.1007/
    978-3-030-53518-6_21
14. Nagashima, Y.: Smart induction for Isabelle/HOL (tool paper). In: 2020
    Formal Methods in Computer Aided Design, FMCAD 2020, Haifa, Is-
    rael, September 21-24, 2020. pp. 245–254. IEEE (2020). https://doi.
    org/10.34727/2020/isbn.978-3-85448-042-6_32, https://doi.org/10.34727/
    2020/isbn.978-3-85448-042-6_32
15. Nagashima, Y.: Faster smarter proof by induction in Isabelle/HOL. In: Zhou, Z.
    (ed.) Proceedings of the Thirtieth International Joint Conference on Artificial In-
    telligence, IJCAI 2021, Virtual Event / Montreal, Canada, 19-27 August 2021. pp.
    1981–1988. ijcai.org (2021). https://doi.org/10.24963/ijcai.2021/273, https:
    //doi.org/10.24963/ijcai.2021/273
16. Nagashima, Y., He, Y.: PaMpeR: proof method recommendation system for Is-
    abelle/HOL. In: Huchard, M., Kästner, C., Fraser, G. (eds.) Proceedings of
    the 33rd ACM/IEEE International Conference on Automated Software Engi-
    neering, ASE 2018, Montpellier, France, September 3-7, 2018. pp. 362–372.
    ACM (2018). https://doi.org/10.1145/3238147.3238210, https://doi.org/
    10.1145/3238147.3238210
17. Nagashima, Y., Kumar, R.: A proof strategy language and proof script generation
    for Isabelle/HOL. In: de Moura, L. (ed.) Automated Deduction - CADE 26 - 26th
    International Conference on Automated Deduction, Gothenburg, Sweden, August
    6-11, 2017, Proceedings. Lecture Notes in Computer Science, vol. 10395, pp. 528–
    545. Springer (2017). https://doi.org/10.1007/978-3-319-63046-5_32, https:
    //doi.org/10.1007/978-3-319-63046-5_32
18. Nawaz, M.Z., Hasan, O., Nawaz, M.S., Fournier-Viger, P., Sun, M.: Proof search-
    ing in HOL4 with genetic algorithm. In: Hung, C., Cerný, T., Shin, D., Bechini,
    A. (eds.) SAC ’20: The 35th ACM/SIGAPP Symposium on Applied Comput-
    ing, online event, [Brno, Czech Republic], March 30 - April 3, 2020. pp. 513–
    520. ACM (2020). https://doi.org/10.1145/3341105.3373917, https://doi.
    org/10.1145/3341105.3373917
19. Polikarpova, N., Sergey, I.: Structuring the synthesis of heap-manipulating pro-
    grams. Proc. ACM Program. Lang. 3(POPL), 72:1–72:30 (2019). https://doi.
    org/10.1145/3290385, https://doi.org/10.1145/3290385
20. Sutton, R.S., Barto, A.G.: Reinforcement learning: An introduction. IEEE Trans.
    Neural Networks 9(5), 1054–1054 (1998). https://doi.org/10.1109/TNN.1998.
    712192, https://doi.org/10.1109/TNN.1998.712192
21. Yang, K., Deng, J.: Learning to prove theorems via interacting with proof assis-
    tants. In: Chaudhuri, K., Salakhutdinov, R. (eds.) Proceedings of the 36th In-
    ternational Conference on Machine Learning, ICML 2019, 9-15 June 2019, Long
                              Genetic Algorithm for Program Synthesis       9

Beach, California, USA. Proceedings of Machine Learning Research, vol. 97, pp.
6984–6994. PMLR (2019), http://proceedings.mlr.press/v97/yang19a.html
