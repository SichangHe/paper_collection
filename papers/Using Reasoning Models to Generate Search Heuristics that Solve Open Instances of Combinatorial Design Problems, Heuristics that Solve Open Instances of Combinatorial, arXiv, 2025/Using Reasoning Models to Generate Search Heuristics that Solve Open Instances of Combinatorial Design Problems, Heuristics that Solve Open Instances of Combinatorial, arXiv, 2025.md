                                             Using Reasoning Models to Generate Search
                                         Heuristics that Solve Open Instances of Combinatorial
                                                            Design Problems


                                                                                 Christopher D. Rosin
                                                                               https://constructive.codes
arXiv:2505.23881v1 [cs.AI] 29 May 2025




                                                                             christopher.rosin@gmail.com



                                                                                       Abstract

                                                  Large Language Models (LLMs) with reasoning are trained to iteratively generate
                                                  and refine their answers before finalizing them, which can help with applications
                                                  to mathematics and code generation. We apply code generation with reasoning
                                                  LLMs to a specific task in the mathematical field of combinatorial design. This
                                                  field studies diverse types of combinatorial designs, many of which have lists of
                                                  open instances for which existence has not yet been determined. The Constructive
                                                  Protocol CPro1 uses LLMs to generate search heuristics that have the potential
                                                  to construct solutions to small open instances. Starting with a textual definition
                                                  and a validity verifier for a particular type of design, CPro1 guides LLMs to select
                                                  and implement strategies, while providing automated hyperparameter tuning and
                                                  execution feedback. CPro1 with reasoning LLMs successfully solves long-standing
                                                  open instances for 7 of 16 combinatorial design problems selected from the 2006
                                                  Handbook of Combinatorial Designs, including new solved instances for 3 of
                                                  these (Bhaskar Rao Designs, Symmetric Weighing Matrices, Balanced Ternary
                                                  Designs) that were unsolved by CPro1 with non-reasoning LLMs. It also solves
                                                  open instances for several problems from recent (2025) literature, generating new
                                                  Covering Sequences, Johnson Clique Covers, Deletion Codes, and a Uniform
                                                  Nested Steiner Quadruple System.


                                         1   Introduction
                                         We apply code generation via reasoning Large Language Models (LLMs) to a specific task in the
                                         mathematical field of combinatorial design. Combinatorial designs are systems of finite sets that
                                         satisfy specified constraints. The particular finite sets and constraints involved define the type of
                                         combinatorial design (e.g. Balanced Incomplete Block Design, Packing Array). The existence
                                         problem (or combinatorial design problem) for a particular type of combinatorial design has a small
                                         number of input parameters (e.g. size), and asks whether it is possible to construct a design that
                                         satisfies the constraints for these parameters. An instance of the existence problem specifies particular
                                         numerical values for the parameters. The existence problem is often addressed by systematic
                                         mathematical constructions that are proven correct and show existence for large classes of instances,
                                         and by mathematical proofs of impossibility that show certain instances cannot exist. But these may
                                         leave behind parameters for which existence remains unknown; these remain as open instances.
                                         As an example, a Symmetric Weighing Matrix is an n × n matrix W with entries in the set {0, 1, −1},
                                         satisfying W W T = wI and W = W T . For w = 16, a Symmetric Weighing Matrix exists for
                                         n = 16, n = 18, and all n ≥ 20 with the possible exception of n ∈ {22, 23, 25, 27, 29} for which
                                         existence was unknown [7] as of 2006. A 2023 result showed that w = 16 n = 23 exists [13]. This
                                         paper’s results include construction of a w = 16 n = 22 Symmetric Weighing Matrix, resolving this
                                         open instance and leaving n ∈ {25, 27, 29} as the remaining open instances for w = 16.
One standard approach to small open instances is heuristic computational search (Handbook of
Combinatorial Designs [7], chapter VII.6). This paper builds on earlier work which developed
a Constructive Protocol CPro1 that automates an experimental process to identify and optimize
heuristic strategies [40]. Starting from a textual definition for a combinatorial design problem and a
validity verifier for proposed solutions, CPro1 guides LLMs to select and implement strategies in C
code, while providing automated hyperparameter tuning and execution feedback using the verifier
(Algorithm 1). In this paper, we use CPro1 with reasoning LLMs that are trained with a reinforcement
learning process to develop their answers in a lengthy textual process that allows space for iteration
and revision before finalizing the answer [19].
We assess the ability of CPro1, with a reasoning LLM, to solve open instances of combinatorial design
problems. CPro1 successfully solves long-standing open instances for 7 of 16 combinatorial design
problems selected from the 2006 Handbook of Combinatorial Designs; 3 of these 7 with new open
instances solved compared to CPro1 using non-reasoning models [40]. We also find CPro1 solves
open instances for 3 out of 4 problems from recent (February 2025) combinatorial design literature.
CPro1 also improves upon an April 2025 results that used the FunSearch LLM-based protocol
to create novel Deletion Codes [51]. Positive results are shown in Table 1. While we don’t see
success with combinatorial design problems that have already seen sustained iterative development
of computational methods by the research community (e.g. Covering Arrays [47, 49, 42]), we do see
strong results in design types that have seen less attention on computational methods.


Algorithm 1 Protocol CPro. Note prompt(x) returns LLM result when prompted with x.
  Input: Definition (of the problem), Dev & Open (instance parameter lists), Verifier (Python code)
  Output: Verified designs for the Open instances (if found)
  // Generate 1000 diverse candidate search heuristics, using the C programming language
  for 50 reps do
     Strategies = prompt(Definition + "Please suggest " + N(=20) + " different approaches...")
     for S in Strategies do
        Details = prompt(Definition + "We have selected..." + S + "...Describe the elements...")
        Code,Hyperparm_ranges = prompt("Now implement...") //Continued chat; Details in context
        append Code,Hyperparm_ranges to Candidates
     end for
  end for // We now have R*N=1000 candidates
  // Execute each candidate (up to 50 sec.), tune hyperparameters, use Verifier to score results
  for C in Candidates do
     Set C’s Hyper_settings,Score = hypertune(C,Hyperparm_ranges) // Execute on Dev instances
     // Grid-based hyperparm tuning (linear in middle, logarithmic/fine-grained out to the endpoints).
     // Up to 1000 grid points run for 0.5 seconds; top 100 for 5 sec.; top 10 for 50 sec.; return best 1.
  end for
  truncate Candidates to the top 5 according to their Score
  // Optimize the execution speed of the top 5 candidates
  for C in Candidates do
     for 5 optimization rounds do
        O = [prompt("...improve the performance..." + C + "...") * 50 times]
        if highest-scoring result from O is much better than C: replace C by it, else: break
     end for
  end for
  // Execute top 5 candidates for a full 2 hours on Dev instances and verify results
  for C in Candidates do: score C with 2-hour runs on Dev instances
  truncate Candidates to the top 2 according to their 2-hour score
  // Execute top 2 candidates for 48 hours on Open instances and output verified solutions
  for C in Candidates do
     Run C for 48 hours on Open instances, and output each result that passes Verifier check.
  end for




                                                   2
 Packing Array (PA): an N × k array with entries in the set {0, 1, . . . v − 1}, such that every N × 2
 subarray contains every ordered pair of symbols at most once.
  (N,k,v):      (24,7,6)    (18,8,6) (28,10,8) (24,11,8) (32,11,9) (28,12,9)
  (21,14,9) (19,15,9)
 Symmetric Weighing Matrix (SymmW): an n × n matrix W with entries in the set {0, 1, −1},
 satisfying W W T = wI and W = W T .
  (n,w): (19,9)† (21,9)† (22,16)
 Skew Weighing Matrix (SkewW): an n × n matrix W with entries in the set {0, 1, −1}, satisfying
 W W T = wI and W T = −W .
  (n,w): (18,9)
 Bhaskar Rao Design (BRD): a v × b array with entries in the set {−1, 0, 1}. Each row contains r
 nonzero entries and each column contains k nonzero entries. For any pair of distinct rows, the
 pairwise element products contain −1 and +1 each L/2 times.
  (v,b,r,k,L): (15,42,14,5,4) (15,126,42,5,12) (16,48,15,5,4)
 Balanced Ternary Design (BTD): an arrangement of V elements into B multisets, or blocks,
 each of cardinality K ≤ V , satisfying: 1. Each element appears R = p1 + 2 ∗ p2 times, with
 multiplicity one in p1 blocks and multiplicity two in p2 blocks. 2. Every pair of distinct elements
 appears L times.
  (V,B;p1,p2,R;K,L):       (17,17;8,2,12;12,8) (14,21;6,3,12;8,6) (12,16;4,4,12;9,8)
  (16,16;7,3,13;13,10) (12,21;4,5,14;8,8)          (16,22;9,1,11;8,5) (21,21;12,1,14;14,9)
 Equidistant Permutation Array (EPA): m rows, each a permutation of {0, 1, . . . n − 1}. Each pair
 of distinct rows must differ in exactly d positions.
  (n,d,m): (12,8,21)†
 Florentine Rectangle (FR): r rows, each a permutation of S = {0, 1, . . . n − 1}. For distinct
 a, b ∈ S and m ∈ {1, 2, ..., n − 1}, at most one row has b positioned m steps to the right of a.
  (r,n): (7,20) (7,24) (7,25) (7,26) (7,27)
(a) Open instances from 2006 Handbook, that were solved and found to exist by CPro1. (†: in prototyping set)

 Covering Sequence (CS): A cyclic sequence x0 , x1 , . . . xL−1 of length L over the binary
 alphabet, such that for any length-n binary word there exists a j such that subsequence
 xj , x(j+1) mod L , x(j+2) mod L , . . . x(j+n−1) mod L is Hamming distance at most R from the word.
   (n,R,L):           (9,1,71)       (10,1,138)        (11,1,224)     (11,2,64)      (12,2,127)
   (12,3,36)          (13,2,276)     (13,3,61)         (14,3,122)     (15,3,230)     (16,3,426)
   (17,2,3938)        (17,3,795)     (18,1,52390)      (18,2,7605)    (18,3,1481) (19,1,104498)
   (19,2,14797) (19,3,2734) (20,1,207000) (20,2,28901) (20,3,5102)
 Johnson Clique Cover (JCC): The Johnson Graph J(N, k) has a vertex for each k-element subset
 of {1, 2, . . . N }. Two subsets A, B are connected by an edge if |A∩B| = k −1. A size-C Johnson
 Clique Cover has C cliques in J(N, k) such that their union includes all vertices in J(N, k).
   (N,k,C): (13,4,105) (13,6,248) (14,4,138) (14,6,410) (15,4,177)
 Uniform Nested Steiner Quadruple System (UNSQS): A Steiner Quadruple System (SQS) is a set
 of blocks, each a size-4 subset of V = {0, 1, ..., v − 1}, such that each subset of 3 elements of V
 is contained in exactly one block. A Uniform Nested SQS splits each block into two ND-pairs of 2
 elements each, such that each distinct ND-pair appears the same number of times. Let p denote
 the number of distinct ND-pairs that appear among the blocks.
   (v,p): (14,91)
     (b) Open instances from Feb. 2025 articles [5, 25, 4], that were solved and found to exist by CPro1.

 Deletion Code (DC): a set of m binary words of length n. Given word x, D(x) is the length-(n−s)
 words obtained by deleting s distinct bits. For any two distinct words x, y: |D(x) ∩ D(y)| = 0.
  (n,s,m):    (12,2,36) (13,2,55) (14,2,85) (15,2,132) (16,2,208)
  (13,3,16) (14,3,21) (15,3,29) (16,3,42)
(c) Deletion Codes found to exist by CPro1, improving on results from Apr. 2025 article using FunSearch [51].
Table 1: Main Results. Combinatorial design problems by source, each with brief definition and
a list of the open instances solved (bold italic indicates newly solved instances using CPro1 with a
reasoning model; plain italic previously solved with CPro1 and non-reasoning models [40]). For each
of these open instances, the code generated by CPro1 constructed a verified solution. The Appendix
includes sample solutions (Figs. 2 to 8) and full definitions as used by CPro1 (Tables 5 to 8).


                                                      3
2     Related Work

Code generation is one of the primary applications of LLMs [22, 24, 34]. LLM code generation
has been used to develop heuristics for combinatorial optimization problems [28, 1, 45], including
generating search operators for genetic algorithms [54]. In this paper, we use LLMs to propose and
implement heuristic strategies in an open-ended way, and successful strategies that emerge include
genetic algorithms [33], simulated annealing [26], and tabu search [15].
Efforts to apply LLMs to mathematics have focused on exercises and benchmarks with known
solutions [21, 20, 14, 29, 30] and generation of step-by-step proofs that could be verified with
systems like Lean [53, 44]. LLMs have difficulty generating valid lengthy step-by-step proofs [38].
Here, we focus on problems that can be resolved by constructing a combinatorial object that can
be easily verified, rather than requiring a step-by-step proof. This has the potential to resolve open
questions in mathematics without the difficulty of generating lengthy step-by-step proofs.
This paper builds on earlier work which developed Constructive Protocol CPro1 [40] for combinatorial
design problems using non-reasoning LLMs. Here, we focus on the use of reasoning LLMs that are
generally more effective than non-reasoning LLMs for mathematics and code generation [19, 37, 52,
31, 14, 11].
Deep learning has emerging applications to constructions in research-level mathematics [50, 32, 2,
46, 3, 36]. FunSearch [39] uses code-generating LLMs in an evolutionary algorithm to search for
greedy functions. It succeeded on a recognized open question by constructing a size-512 Cap Set for
n = 8, and was recently used to obtain novel Deletion Codes [51]. Compared to FunSearch, CPro1
generates fewer candidates, allows open-ended strategies rather than just greedy functions, and is
simpler without FunSearch’s iterative evolution. We test CPro1 with a reasoning model on Cap Sets
and Deletion Codes.


3     Method

Terminology: A Large Language Model (LLM) takes a textual prompt and returns a textual response,
which may include natural language and/or programming language code. LLMs are trained via
machine learning, but we use off-the-shelf pretrained LLMs. For reasoning LLMs, the pretraining
includes reinforcement learning of a textual process that iteratively develops and refines the answer;
this textual reasoning trace is not part of the final result. We use protocol to refer to an algorithm
which includes calls to an LLM, and scaffolding consists of protocol elements other than the LLM.


    Selected combinatorial designs from     Handbook        Combinatorial designs
    the Handbook                            Chapter         from Feb. 2025               Source
    Balanced Incomplete Block Design        II.1            Covering Sequence            [5]
    Packing Array (PA)                      III.3           Johnson Clique Cover         [25]
    Orthogonal Array                        III.6           Uniform Nested Steiner
                                                                                         [4]
    Symmetric Weighing Matrix (SymmW)       V.2             Quadruple System
    Skew Weighing Matrix (SkewW)            V.2             Covering Array               [42]
    Bhaskar Rao Design (BRD)                V.4
    Balanced Ternary Design (BTD)           VI.2            FunSearch Problems           Source
    Costas Array                            VI.9            Cap Sets                     [39]
    Covering Design                         VI.11           Deletion Codes               [51]
    Difference Triangle Set                 VI.19
    Perfect Mendelsohn Design               VI.35         Table 2: Problem Selection: Combina-
    Equidistant Permutation Array (EPA)     VI.44         torial designs with long-standing open in-
    Florentine Rectangle (FR)               VI.62         stances from the 2006 Handbook of Com-
    Circular Florentine Rectangle           VI.62         binatorial Designs [7]; recent problems
    Tuscan-2 Square                         VI.62         from Feb. 2025 combinatorial design liter-
    Supersimple Design                      VI.57         ature; 2 problems addressed by FunSearch.




                                                  4
3.1   Selection of Combinatorial Designs (see Table 2)

We start with the same 16 types of combinatorial designs from the 2006 Handbook of Combinatorial
Designs [7] (henceforth Handbook) that were used with CPro1 and non-reasoning models [40]. Each
of these has clearly defined open instances in the Handbook with relatively small parameters that
might be amenable to heuristic search. Instances which have already been solved in the literature are
omitted [43, 35, 17, 13, 8, 16, 18, 9], focusing on remaining instances that are still open.
In addition, we also sample much more recent open questions. From the Journal of Combinatorial
Design and arXiv’s math.CO combinatorics category, we survey all articles that first appeared in
Feb. 2025, and select those which describe combinatorial design problems and include a table of
specific open instances. Out of 6 J. Combinatorial Design articles, we select 2, and out of 447 arXiv
combinatorics articles (the great majority of which do not address combinatorial designs), we select
2. Note this gives a rough idea of the scope of applicability of the method.
We also include Cap Sets from the original FunSearch paper [39] and Deletion Codes from an April
2025 FunSearch paper [51], to see if CPro1 could replicate FunSearch’s results and go beyond them.
For each selected problem, we provide:

Textual Definition of the problem, mandating a specific solution representation as an integer array.
Verifier in Python Determines whether a proposed solution in this representation is correct.
Open Instances Instance parameters for which existence is not yet known. The ultimate goal is to
construct designs with these parameters.
Development Instances (Dev Instances) Instances known to exist, including some of the smallest,
as well as ones just slightly smaller than the Open Instances. Candidates are executed on these, with
results checked by the Verifier, to identify the most promising approaches.

3.2   Protocol

Algorithm 1 summarizes the Constructive Protocol CPro1 (see [40] for more details). During initial
testing, 1000 candidate programs are generated and undergo hyperparameter tuning, and each are
scored on the basis of 50 seconds of execution using the tuned hyperparameters. The 5 top-scoring
candidates proceed to optimization (also 50 seconds). For final testing on development instances, the
same 5 candidates (after optimization) are given 2 hours. The 2 top-scoring candidates from this then
run for 48 hours on the open instances.

3.3   Prototyping Set

CPro1 was developed with the aid of a small prototyping set of combinatorial design problems for
which a manual effort found solvable open instances [40]. This was based on manual development and
tuning of local search methods for 5 of of the 16 selected combinatorial designs from the Handbook:
Bhaskar Rao Designs (BRD), Difference Triangle Sets, Equidistant Permutation Arrays (EPA),
Supersimple Designs, and Symmetric Weighing Matrices (SymmW). The local search methods
selected changes which minimize a cost function, while sometimes accepting worsening moves to
escape local optima. Local search succeeded in solving 1 open instance for EPA and 2 for SymmW
(marked with † in Table 1(a)); EPA and SymmW formed the Prototyping Set.
Table 3 shows CPro1’s Prototyping Set results with the non-reasoning GPT-4o model used originally,
as well as with two reasoning models: the OpenAI o3-mini [37] set to “high” reasoning, and the
open-weights model DeepSeek R1 [19]. o3-mini-high is especially successful and solves 4 instances
from the prototyping set (including SymmW instance n = 22 w = 16 that both hand-coded local
search and CPro1 with GPT-4o failed on), so we use o3-mini-high for reasoning model experiments
here.

3.4   Experiments

For each of the 16 types of combinatorial design from the Handbook, each of the four Feb. 2025
problems, and both of the FunSearch problems, we run CPro1 with the reasoning model o3-mini-high.
We also include and compare prior results with obtained with CPro1 using non-reasoning model


                                                 5
            LLM                            Ver. Date        SymmW open solved   EPA open solved
            GPT-4o [23]                    2024-05-13             2                   1
            o3-mini-high [37]              2025-01-31             3                   1
            DeepSeek R1 [19]               2025-01-20             2                   1
Table 3: Prototyping Set Results. For each LLM and total number of candidate programs: the
number of distinct open instances that are solved by CPro1 on each Prototyping Set problem. GPT-4o
is a non-reasoning model previously used with CPro1 [40]; o3-mini-high and DeepSeek R1 are
reasoning models newly tested here.



GPT-4o [40] on the Handbook problems. We also test ablated and scaled-down versions of the
protocol, using the same candidate programs generated by the original runs.
When we succeed in solving open instances of a combinatorial design problem, we extend by testing
the generated code on adjacent open instances (e.g. next size larger).
Each experiment runs on a Linux machine with AMD Ryzen 9 7950X3D CPU and 128GB of memory,
with the machine fully dedicated to one run at a time. A full run of CPro1 on one type of combinatorial
design takes approximately 6-10 days, the majority of which is used running candidate programs on
development instances and open instances. Runs with o3-mini-high tend to take longer than runs
with GPT-4o, because with o3-mini-high there are fewer candidate programs which immediately fail.

4         Results
Table 1 shows the main results. CPro1 solves open instances for 7 types of combinatorial designs
of the 16 selected from the Handbook. This includes open instances that were only solved with
CPro1 using the reasoning model o3-mini-high (and not using GPT-4o) for 3 of these 7. Positive
results using the reasoning model include Bhaskar Rao Designs, for which our hand-coded local
search failed. CPro1 with o3-mini-high solves a superset of instances solved with GPT-4o (Table 4).
For other Handbook combinatorial designs from Table 2, code generated by CPro1 solves many
development instances, but no open instances.
CPro1 using o3-mini-high solves open instances for 3 of the 4 selected problems from Feb. 2025
combinatorial design literature. It creates problem-specific local search algorithms for Covering
Sequence and Johnson Clique Cover, obtaining significant progress on open instances compared to
the computational methods used in the original publications [5, 25]. These are more recent types of
combinatorial designs that do not appear in the Handbook, and have thus far received less attention.
For the Deletion Codes problem, FunSearch was reported in April 2025 to improve on state-of-the-art
codes for 3 sets of parameters [51]. CPro1 implements a tabu search which replicates these results
and also finds further improvement (larger sets of codewords meeting the constraints) for all 3, plus 6
other sets of parameters, substantially improving on the state of the art for small Deletion Codes.
Note Table 1 only shows independent solved instances. For example, the EPA with n=12 d=8 m=21
implies the existence of n=13 d=8 m=21 (add a constant column), and the PA with N=32 k=11 v=9
trivially implies the existence of N=31 k=11 v=9 (remove a row), but we don’t list these.
All of the open instance solutions, and the code that constructed them, are available on github. 1

4.1        Ablation

Table 4 shows that all considered elements of the protocol are needed to obtain the full results on
the 7 successful Handbook problems, though CPro1 runs with o3-mini-high are less degraded by
ablation.

4.2        Scaled-Down Runs

Figure 1 has results from repeated scaled-down runs for 4 of the Handbook problems, each using
only 40 candidate programs. These candidates come from the original pool of candidates, giving
      1
          https://github.com/Constructive-Codes/CPro1


                                                        6
                              PA        SymmW     SkewW     BTD       FR       EPA         BRD
    o3-mini-high              Tabu      DFS       DFS       Tabu      GRASP    cSA         cSA,2p
    - Reduce runtime          Tabu      DFS       DFS       Tabu               cSA         cSA,2p
    - No final dev test       Tabu      DFS       DFS       Tabu                           cSA,2p
    - No optimization         Tabu      DFS       DFS       Tabu                           2p
    - No hyper tuning         Tabu      DFS       DFS       Tabu,RG                        2p
    GPT-4o                    cSA       rSA       cSA       GA        DFS      cSA
    - Reduce runtime          cSA       rSA       cSA       GA        DFS
    - No final dev test       cSA       rSA       cSA       GA        DFS
    - No optimization         cSA       SA        cSA       GA
    - No hyper tuning         rSA       GA
Table 4: Problem-Specific Results and Ablation. Each row is an experiment, each column a type
of combinatorial design from the Handbook. Colored cells show where the experiment solved at
least one open instance: green indicates the experiment solved all the open instances that the initial
run did, and yellow indicates an ablation experiment solved only a subset. The first set of rows use
o3-mini-high, and the “-” rows stack up successive ablations: Reduce runtime reduces from 48 hours
to 2 for open instances, No final dev test eliminates final 2 hour testing on development instances
(instead using original 50-second test results), No optimization eliminates the code optimization
step, and No hyper tuning eliminates hyperparameter tuning (instead using defaults given by the
LLM). The second set of rows use GPT-4o (from [40]). Each cell shows the strategies that obtained
success: DFS: backtracking depth-first search, GA: genetic algorithm, SA: simulated annealing with
slow cooling schedule, rSA: simulated annealing with periodic resets, cSA: constant-temperature
simulated annealing, Tabu: Tabu search [15], RG: randomized greedy (randomized DFS within row,
restart if any row fails), 2-phase for BRD: find binary incidence matrix, then add signs, GRASP:
Greedy randomized adaptive search procedure [12].


                1                                                 Figure 1: Results from scaled-
                                                                  down 40-candidate runs. With re-
               0.8
                                                                  duced runtime (2 hours) on open
Success rate




               0.6                                                instances, no final dev test, and
                                                                  no optimization. Each bar shows
               0.4                                                the rate of successfully solving at
                                                                  least one open instance, across 25
               0.2                                                repeated runs, with 95% Clopper-
                0                                                 Pearson confidence interval. Each
                                                                  problem’s difference between o3-
                      PA       SymmW          SkewW       BTD
                                                                  mini-high and GPT-4o is significant
                               o3-mini-high     GPT-4o            (p<0.0001, Z-test).



1000/40 = 25 scaled-down runs. Each bar shows the fraction of these 25 runs that solved at least
one open instance. These are ablated runs: using reduced runtime of 2 hours on open instances, no
final dev test, and no optimization step (but retaining hyperparameter tuning). We see that success
rates remain high for the o3-mini-high reasoning model, whereas GPT-4o performs relatively poorly.


4.3             Strategies Implemented by Generated Code

Most of the positive results in Table 4 use simulated annealing, genetic algorithms, tabu search, or
depth-first search. Each full run includes 1000 candidates, generated from 50 lists of 20 proposed
strategies each. Simulated annealing, genetic algorithms, tabu search, greedy algorithms, and depth-
first search are usually each proposed dozens of times during a run. This gives adequate room to
explore alternatives within each method (e.g. for cost function, neighborhood).
All of the successful strategies are randomized, and most appear well-optimized. Successful programs
are 120-270 lines of C code for GPT-4o, and up to 540 lines for o3-mini-high.


                                                      7
For the Uniform Nested Steiner Quadruple System problem, CPro1’s approach succeeds by addressing
different constraints in two phases: first create a Steiner Quadruple System using Knuth’s Algorithm
X [27], then perform tabu search for nested pairs. A two-phase approach also arises for Bhaskar Rao
Designs: first find a 0/1 matrix that meets incidence constraints, then add +1/-1 signs. These two-
phase approaches seem somewhat surprising; one might have anticipated that constraint interaction
would prevent success. Prior two-phase approaches for the Covering Array combinatorial design
problem [48, 49] have both phases addressing the same constraints.

5       Limitations
In general, the application of simulated annealing, tabu search, and genetic algorithms to combinatorial
designs is well established (Handbook chapter VII.6). The positive results reported here arise from
automation of computational experimentation that could have been done manually. The research
community has only undertaken limited effort on such experimentation for the designs with positive
results here; this may have left low-hanging fruit for CPro1. Some of the designs with no positive
results here have received much greater attention from the research community. For example, CPro1
was unsuccessful on Covering Arrays. This included failure to replicate mathematical constructions
from the Feb. 2025 paper, as well as earlier results from specialized search heuristics [47, 48] that
were noted in the Feb. 2025 paper. Covering Arrays have received substantial attention, leading
to development of progressively better computational techniques and mathematical constructions
[47, 49]; CPro1 is less likely to contribute here.
CPro1 can only show existence by constructing a solution. For some of the open instances included
here, there may exist no solution, but non-existence proofs are outside the scope of CPro1.
We perform only one full-scale run of CPro1 with each included LLM on each type of combinatorial
design, and the LLMs are inherently nondeterministic in their responses; repeat runs could yield
different results.
After our experiments were completed, a new publication reported use of FPGAs to solve some of
the open Difference Triangle Set instances that CPro1 failed to solve [41].
CPro1 fails to replicate FunSearch’s 512-size Cap Set solution for n = 8. One issue may be a vast
difference in scale: while CPro1’s run generated only 1000 candidate programs, FunSearch’s 512
result was found in 4 of 140 runs, each of which generated 2.5 million candidate programs [39].
Other attempts to replicate FunSearch’s 512 result with LLM-generated code have also failed [6, 10].
CPro1’s solutions are built by randomized heuristics, and usually show little structure. FunSearch’s
greedy functions are more likely to yield structure that aids mathematical understanding [39].

6       Conclusion
The protocol CPro1 uses LLMs to generate search heuristics, and using a reasoning LLM it success-
fully solves open instances of the existence problem for 7 types of combinatorial designs from the
Handbook of Combinatorial Designs (including open instances for 3 of them that were unsolved
by CPro1 with non-reasoning LLMs), 3 more from the Feb. 2025 combinatorial design literature,
and also yields state of the art results for the Deletion Codes problem that was previously addressed
by FunSearch. The code for CPro1 is available,2 and the protocol can be run on additional types of
combinatorial designs by supplying a textual definition, a Python verifier, and small collections of
parameters for development instances and open instances.




    2
        https://github.com/Constructive-Codes/CPro1


                                                      8
References
 [1] T. Bömer, N. Koltermann, M. Disselnmeyer, L. Dörr, and A. Meyer. Leveraging Large Language
     Models to develop heuristics for emerging optimization problems, 2025. arXiv:2503.03350.
 [2] F. Charton, J. S. Ellenberg, A. Z. Wagner, and G. Williamson. PatternBoost: Constructions in
     mathematics with a little help from AI, 2024. arXiv:2411.00566.
 [3] H. Chau, H. Jenne, D. Brown, J. He, M. Raugas, S. Billey, and H. Kvinge. Machine learning
     meets algebraic combinatorics: A suite of datasets capturing research-level conjecturing ability
     in pure mathematics, 2025. arXiv:2503.06366.
 [4] Y. M. Chee, S. H. Dau, T. Etzion, H. M. Kiah, and W. Zhang. Pairs in nested Steiner quadruple
     systems. Journal of Combinatorial Designs, 33(5):177–187, 2025.
 [5] Y. M. Chee, T. Etzion, H. Ta, and V. K. Vu. Constructions of covering sequences and arrays,
     2025. arXiv:2502.08424.
 [6] Z. Chen, Z. Zhou, Y. Lu, R. Xu, L. Pan, and Z. Lan. UBER: Uncertainty-based evolution with
     large language models for automatic heuristic design, 2024. arXiv:2412.20694.
 [7] C. J. Colbourn and J. H. Dinitz. Handbook of combinatorial designs. Taylor & Francis, 2006.
 [8] J. Dinitz. New results in Part V, 2018. https://site.uvm.edu/jdinitz/?page_id=404.
 [9] J. Dinitz. New results in Part VI, 2018. https://site.uvm.edu/jdinitz/?page_id=413.
[10] J. S. Ellenberg, C. S. Fraser-Taliente, T. R. Harvey, K. Srivastava, and A. V. Sutherland.
     Generative modeling for mathematical discovery, 2025. arXiv:2503.11061.
[11] EpochAI. AI benchmarking hub – FrontierMath, 2025. https://epoch.ai/data/ai-benchmarking-
     dashboard.
[12] T. A. Feo and M. G. Resende. Greedy randomized adaptive search procedures. Journal of
     global optimization, 6:109–133, 1995.
[13] S. D. Georgiou, S. Stylianou, and H. Alrweili. On symmetric weighing matrices. Mathematics,
     11:2076, 2023.
[14] E. Glazer, E. Erdil, T. Besiroglu, D. Chicharro, E. Chen, A. Gunning, C. F. Olsson, J.-S. Denain,
     A. Ho, E. d. O. Santos, et al. FrontierMath: A benchmark for evaluating advanced mathematical
     reasoning in AI, 2024. arXiv:2411.04872.
[15] F. Glover and M. Laguna. Tabu search. Springer, 1997.
[16] D.      Gordon.              La      Jolla        Covering   Repository       Tables,      2025.
     https://ljcr.dmgordon.org/cover/table.html.
[17] M. Greig. Constructions using balanced n-ary designs. In Designs, pages 227–274. Springer,
     2002.
[18] T. S. Griggs and A. R. Kozlik. The last two perfect Mendelsohn designs with block size 5.
     Journal of Combinatorial Designs, 28(12):865–868, 2020.
[19] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
     DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning, 2025.
     arXiv:2501.12948.
[20] C. He, R. Luo, Y. Bai, S. Hu, Z. L. Thai, J. Shen, J. Hu, X. Han, Y. Huang, Y. Zhang, J. Liu,
     L. Qi, Z. Liu, and M. Sun. OlympiadBench: A challenging benchmark for promoting AGI with
     Olympiad-level bilingual multimodal scientific problems, 2024. arXiv:2402.14008.
[21] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt.
     Measuring mathematical problem solving with the MATH dataset. NeurIPS, 2021.


                                                   9
[22] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy, and H. Wang.
     Large language models for software engineering: A systematic literature review. ACM Trans.
     Softw. Eng. Methodol., 33(8), 2024. doi: 10.1145/3695988.
[23] A. Hurst, A. Lerer, et al. GPT-4o system card, 2024. arXiv:2410.21276.
[24] J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim. A survey on large language models for code
     generation, 2024. arXiv:2406.00515.
[25] S. F. Jørgensen. On the clique covering numbers of Johnson graphs, 2025. arXiv:2502.15019.
[26] S. Kirkpatrick, C. D. Gelatt Jr, and M. P. Vecchi. Optimization by simulated annealing. Science,
     220(4598):671–680, 1983.
[27] D. E. Knuth. Dancing links, 2000. arXiv:cs/0011047.
[28] F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, and Q. Zhang. Evolution of heuristics:
     towards efficient automatic algorithm design using large language model. In Proceedings of the
     41st International Conference on Machine Learning, ICML’24, 2024.
[29] J. Liu, X. Lin, J. Bayer, Y. Dillies, W. Jiang, X. Liang, R. Soletskyi, H. Wang, Y. Xie,
     B. Xiong, et al. Generating streamlining constraints with Large Language Models, 2024.
     arXiv:2408.10268.
[30] J. Liu, X. Lin, J. Bayer, Y. Dillies, W. Jiang, X. Liang, R. Soletskyi, H. Wang, Y. Xie, B. Xiong,
     et al. CombiBench: Benchmarking LLM capability for combinatorial mathematics, 2025.
     arXiv:2505.03171.
[31] LiveBench. LiveBench leaderboard, 2025. https://livebench.ai.
[32] A. Mehrabian, A. Anand, H. Kim, N. Sonnerat, M. Balog, G. Comanici, T. Berariu, A. Lee,
     A. Ruoss, A. Bulanova, et al. Finding increasingly large extremal graphs with AlphaZero and
     tabu search. In NeurIPS, 2024.
[33] M. Mitchell. An introduction to genetic algorithms. MIT Press, 1998.
[34] M. Nejjar, L. Zacharias, F. Stiehle, and I. Weber. LLMs for science: Usage for code generation
     and data analysis. Journal of Software: Evolution and Process, 37(1):e2723, 2025.
[35] H. Noritake, M. Banbara, T. Soh, N. Tamura, and K. Inoue. Constraint modeling and SAT
     encoding of the packing array problem. Computer Software, 31:1_116–1_130, 2014.
[36] A. Novikov, N. Vu, M. Eisenberger, E. Dupont, et al. AlphaEvolve: A coding agent for scientific
     and algorithmic discovery, 2025. DeepMind.
[37] OpenAI. OpenAI o3-mini system card, 2025. https://cdn.openai.com/o3-mini-system-card-
     feb10.pdf.
[38] I. Petrov, J. Dekoninck, L. Baltadzhiev, M. Drencheva, K. Minchev, M. Balunović, N. Jovanović,
     and M. Vechev. Proof or bluff? Evaluating LLMs on 2025 USA Math Olympiad, 2025.
     arXiv:2503.21934.
[39] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. Ruiz,
     J. S. Ellenberg, P. Wang, O. Fawzi, et al. Mathematical discoveries from program search with
     large language models. Nature, 625(7995):468–475, 2024.
[40] C. D. Rosin. Using code generation to solve open instances of combinatorial design problems,
     2025. arXiv:2501.17725.
[41] M. Shehadeh, W. Kingsford, and F. R. Kschischang. New difference triangle sets by an
     FPGA-based search technique, 2025. arXiv:2502.19517.
[42] K. Shokri and L. Moura. New families of strength-3 covering arrays using linear feedback shift
     register sequences. Journal of Combinatorial Designs, 2025.


                                                 10
[43] J. Stardom. Metaheuristics and the search for covering and packing arrays. Master’s thesis,
     Simon Fraser University, 2001.
[44] B. Stroebl, S. Kapoor, and A. Narayanan. Inference Scaling fLaws: The limits of LLM
     resampling with imperfect verifiers, 2024. arXiv:2411.17501.
[45] W. Sun, S. Feng, S. Li, and Y. Yang. CO-Bench: Benchmarking language model agents in
     algorithm search for combinatorial optimization, 2025. arXiv:2504.04310.
[46] G. Swirszcz, A. Z. Wagner, G. Williamson, S. Blackwell, B. Georgiev, A. Davies, A. Eslami,
     S. Racaniere, T. Weber, and P. Kohli. Advancing geometry with AI: Multi-agent generation of
     polytopes, 2025. arXiv:2502.05199.
[47] J. Torres-Jimenez and E. Rodriguez-Tello. New bounds for binary covering arrays using
     simulated annealing. Information Sciences, 185(1):137–152, 2012.
[48] J. Torres-Jimenez, H. Avila-George, and I. Izquierdo-Marquez. A two-stage algorithm for
     combinatorial testing. Optimization Letters, 11(3):457–469, 2017.
[49] J. Torres-Jimenez, I. Izquierdo-Marquez, and H. Avila-George. Methods to construct uniform
     covering arrays. IEEE Access, 7:42774–42797, 2019.
[50] A. Z. Wagner. Constructions in combinatorics via neural networks, 2021. arXiv:2104.14516.
[51] F. Weindel and R. Heckel.       LLM-guided search for deletion-correcting codes, 2025.
     arXiv:2504.00613.
[52] C. White, S. Dooley, M. Roberts, et al. LiveBench: A challenging, contamination-limited LLM
     benchmark. In ICLR, 2025.
[53] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, and
     A. Anandkumar. LeanDojo: Theorem proving with retrieval-augmented language models.
     NeurIPS, 2024.
[54] H. Ye, J. Wang, Z. Cao, F. Berto, C. Hua, H. Kim, J. Park, and G. Song. ReEvo: Large language
     models as hyper-heuristics with reflective evolution. In NeurIPS, 2024.




                                               11
A   Appendix: Definitions Used for Prompting




                                   12
 A "Balanced Incomplete Block Design" BIBD(v,b,r,k,L) is a pair (V,B) where V is a v-set and
 B is a collection of b k-subsets of V (blocks) such that each element of V is contained in exactly r
 blocks and any 2-subset of V is contained in exactly L blocks.
 The BIBD is represented by a v by b incidence matrix (v rows and b columns) with elements in
 0,1. The matrix element m_{ij} in the i’th row and j’th column is 1 iff element i is contained in
 block j. The sum of each row is r, and the sum of each column is k. For each pair of distinct
 elements y and z, sum_{j=1}^{b} m_{yj} m_{zj} = L.
 Given (v,b,r,k,L) we want to find the incidence matrix for a valid BIBD(v,b,r,k,L).
 A "Packing Array" PA(N,k,v) is an N x k array (N rows and k columns), with each entry from
 the v-set 0,1,...v-1, so that every N x 2 subarray contains every ordered pair of symbols at most
 once. Given (N,k,v), we want to construct PA(N,k,v).
 An "Orthogonal Array" OA(N,k,s) of size N, degree k, and order s, is a k x N array (k rows
 and N columns) with entries from the s-set {0,1,...,s-1} having the property that in every 2 x N
 submatrix, every 2 x 1 column vector appears the same number (lambda) of times. lambda is
 called the index of the OA, and lambda = N/s^2. Given (N,k,s,lambda), we want to construct an
 OA(N,k,s) with index lambda.
 A "weighing matrix" W(n,w) with parameters (n,w) is an n by n square matrix (n rows and n
 columns) with entries in {0,1,-1} that satisfies W W^T = wI. That is, W times its transpose is equal
 to the constant w times the identity matrix I. The weighing matrix will have w nonzero entries in
 each row and each column. And each pair of distinct rows is orthogonal (dot product zero). Given
 (n,w), we want to construct "SymmW", a symmetric weighing matrix W(n,w) that satisfies these
 properties and is also a symmetric matrix.
 A "weighing matrix" W(n,w) with parameters (n,w) is an n by n square matrix (n rows and n
 columns) with entries in {0,1,-1} that satisfies W W^T = wI. That is, W times its transpose is equal
 to the constant w times the identity matrix I. The weighing matrix will have w nonzero entries
 in each row and each column. And each pair of distinct rows is orthogonal (dot product zero).
 Given (n,w), we want to construct "SkewW", a skew weighing matrix W(n,w) that satisfies these
 properties and is also a skew matrix: that is, W^T = -W.
 A "Bhaskar Rao Design" BRD(v,b,r,k,L) is represented by a v by b array (v rows and b columns)
 with elements a_{ij} in {-1,0,1}. Each row contains exactly r nonzero elements, and each column
 contains exactly k nonzero elements. For any pair of distinct rows, the list of pairwise element
 products must contain -1 L/2 times, and must contain +1 L/2 times. That is, for distinct rows f and
 g, the set of pairwise element products {a_{fj}*a_{gj}} contains -1 L/2 times, +1 L/2 times, and 0
 b-L times.
 Given (v,b,r,k,L) we want to find a valid BRD(v,b,r,k,L).
 A "Balanced Ternary Design" BTD(V,B;p1,p2,R;K,L) is an arrangement of V elements into B
 multisets, or blocks, each of cardinality K (K<=V) satisfying:
 1. Each element appears R=p1 + 2*p2 times altogether, with multiplicity one in exactly p1 blocks
 and multiplicity two in exactly p2 blocks.
 2. Every pair of distinct elements appears L times; that is, if m_{vb} is the multiplicity of the
 v’th element in the b’th block, then for every pair of distinct elements v and w, sum_{b=1}^{B}
 m_{vb} m_{wb} = L.
 The BTD is represented by a V by B incidence matrix with elements in 0,1,2. The matrix element
 m_{vb} in the v’th row and b’th column is the multiplicity of the v’th element in the b’th block.
 The sum of each row is R, and the sum of each column is K.
 Given (V,B,p1,p2,R,K,L) we want to find BTD(V,B;p1,p2,R;K,L).
 A "Costas Array" of order n is an n by n array of dots and blanks that satisfies:
 (1) There are n dots and n(n-1) blanks, with exactly one dot in each row and each column.
 (2) All the segments between pairs of dots differ in length or slope.
 We will represent the Costas Array by a one-dimensional list "CA" of length n, that contains a
 permutation of {0,1,...,n-1}. CA[i] identifies the row for the dot that is in column i of the grid.
 Condition (1) is automatically satisfied by this representation. Condition (2) is satisfied if the
 tuples (j-i,CA[j]-CA[i]) are unique across all j>i with 0<=i,j<n.
 Given n, we want to construct the one-dimensional list CA that represents a valid Costas Array of
 order n.
Table 5: Definitions for use in prompting: Handbook combinatorial design problems part 1. Note
the definitions use ASCII symbols for the sake of prompting.



                                                 13
 A "Covering" Cov(t,v,k,n) is a pair (X,B), where X is a v-set of elements and B is a collection
 of k-subsets of X, such that every t-subset of X occurs in at least one block in B. B has n blocks,
 and it is required that t<k. We represent the Covering by an n by v incidence matrix (n rows and
 v columns) with elements in {0,1}; a 1 in row i column j indicates that block i contains the j’th
 element. There are k 1’s per row. Given (t,v,k,n) we want to construct a Cov(t,v,k,n) and provide
 the incidence matrix.
 A "Difference Triangle Set" (n,k)-DTS is a set X={X_1,...,X_n} where for 1<=i<=n,
 X_i={a_{i0}, a_{i1},..., a_{ik}} with a_{ij} an integer and with 0 = a_{i0} < a_{i1} <a_{i2} < ...
 < a_{ik}. The differences a_{il}-a_{ij} for 1<=i<=n, 0<=j!=l<=k are all distinct and nonzero. The
 "scope" of a DTS is the max of all a_{ij} in the DTS.
 Given (n,k) and s, we want to construct an (n,k)-DTS with scope s. The (n,k)-DTS should be
 represented by an n by k+1 array (n rows and k+1 columns) of elements a_{ij} with 1<=i<=n and
 0<=j<=k.
 Given a k-tuple (x_0, x_1, x_2, ..., x_{k-1}), elements x_i, x_{i+t} are t-apart in the k-tuple,
 where i+t is taken modulo k.
 A "Perfect Mendelsohn Design" with parameters v and k is denoted as a (v,k)-PMD. It is a set
 V={0,1,...,v-1} of size v together with a collection B of blocks of ordered k-tuples of distinct
 elements from V, such that for every i=1,2,3,...,k-1 each ordered pair (x,y) of distinct elements
 from V is i-apart in exactly one block. Note since there are v*(v-1) pairs of distinct elements that
 must be 1-apart in exactly one block, and each block has k pairs that are 1-apart, the design will
 contain b=v*(v-1)/k blocks. We will use b to denote the number of blocks.
 Given (v,k,b), we want to construct a (v,k)-PMD with b blocks. We will represent the PMD with a
 b by k array (b rows and k columns), with each element of the array chosen from {0,1,...,v-1}.
 An "equidistant permutation array" (EPA) with parameters (n,d,m) can be represented as an m
 by n matrix (m rows and n columns), where each row is the permutation of the numbers 0 to n-1.
 Each pair of distinct rows must differ in exactly d positions. Given (n,d,m), we want to construct
 an equidistant permutation array (EPA) with these parameters.
 A "Florentine Rectangle" FR(r,n) is an r x n array (r rows and n columns), with each row having
 a permutation of the set of symbols S={0,1,2,...,n-1}, such that for any two distinct symbols a and
 b in S and each m in {1,2,3,...,n-1} there is at most one row in which b appears in the position
 which is m steps to the right of a. A single row will have n-m pairs of symbols a,b with b being m
 steps to the right of a; so n-1 pairs with b directly to the right of a, n-2 with b 2 steps to the right of
 a, and only 1 pair with b n-1 steps to the right of a. Given (r,n) we want to construct a FR(r,n).
 A "Circular Florentine Rectangle" CFR(r,n) is an r x n array (r rows and n columns), with each
 row having a permutation of the set of symbols S={0,1,2,...,n-1}, such that for any two distinct
 symbols a and b in S and each m in {1,2,3,...,n-1} there is at most one row in which b appears in
 the position which is m steps to the right of a. "Steps to the right" is taken circularly - so if a is at
 position i then b is at position (i+m) mod n. Given (r,n) we want to construct a CFR(r,n).
 A "Tuscan-2 Square" T2(n) of size n is an n x n array (n rows and n columns), with each row
 having a permutation of the set of symbols S={0,1,2,...,n-1}, such that any two distinct symbols a
 and b in S have exactly one row in which b appears in the position directly to the right of a, and at
 most one row in which b appears two positions to the right of a (with one symbol between). Given
 n, we want to construct a T2(n).
 A "Supersimple Balanced Incomplete Block Design" SBIBD(v,b,r,k,L) is a pair (V,B) where
 V is a v-set and B is a collection of b k-subsets of V (blocks) such that each element of V is
 contained in exactly r blocks, any 2-subset of V is contained in exactly L blocks, and any two
 distinct blocks have at most two elements in common.
 The SBIBD is represented by a v by b incidence matrix (v rows and b columns) with elements in
 {0,1}. The matrix element m_{ij} in the i’th row and j’th column is 1 iff element i is contained
 in block j. The sum of each row is r, and the sum of each column is k. For each pair of distinct
 elements y and z, sum_{j=1}^{b} m_{yj} m_{zj} = L. For each pair of distinct blocks g and h,
 sum_{i=1}^{v} m_{ig} m_{ih} <= 2.
 Given (v,b,r,k,L) we want to find the incidence matrix for a valid SBIBD(v,b,r,k,L).
Table 6: Definitions for use in prompting: Handbook combinatorial design problems part 2. Note
the definitions use ASCII symbols for the sake of prompting.




                                                     14
 An "(n,R)-Covering Sequence" (abbreviated "(n,R)-CS") of length L is a cyclic sequence
 x_0,x_1,...,x_{L-1} of length L, over the binary alphabet (x_i is in {0,1} for all j) such that for any
 length-n binary word y_0,y_1,...,y_{n-1} there exists a j such that subsequence x_j,x_{(j+1) mod
 L},x_{(j+2) mod L}...,x_{(j+n-1) mod L} of length n is Hamming distance at most R away from
 the word. That is, y_0,...,y_{n-1} and x_j,...,x_{(j+n-1) mod L} differ in at most R positions. For
 our purposes, n <= 16 and R <= 3 and L <= 1200. Given (n,R,L) we want to construct a (n,R)-CS
 of length at most L. Output (n,R)-CS as a list of values in {0,1} separated by spaces, all on one
 line.
 The Johnson Graph J(N,k) with k<=N/2 is the graph whose vertices are k-element subsets of
 [N]={1,2,...,N}, with two subsets connected by an edge if their intersection has size exactly k-1.
 A "Johnson Clique Cover" JCC(N,k,C) of size C is a set of C cliques in J(N,k), such that the
 union of these cliques includes all vertices in J(N,k). Note the cliques in the clique cover do not
 need to be disjoint; they may share vertices. For our purposes, N<=15 and C<800. Given (N,k,C)
 we want to construct a JCC(N,k,C). It is a theorem that it suffices to consider clique covers that
 consist only of maximal cliques, and that all maximal cliques of J(N,k) are either type 0 or type
 1, defined as follows. A type 0 clique specifies a k-1 element subset S of [N], and consists of all
 vertices corresponding to the subset S plus x, for each x that is an element of [N] that is not in S.
 A type 1 clique specifies k+1 elements in [N], and consists of all vertices corresponding to the
 subset S excluding x, for each x that is an element of S. Specify a clique as a space-separated
 list of integers where the first integer is the type (0 or 1) and the remaining integers specify the
 elements of S. For example in J(5,2) the type 0 clique "0 1" consists of vertices for the subsets
 1,2, 1,3, 1,4, and 1,5; and the type 1 clique "1 3 4 5" consists of vertices for the subsets {4,5},
 {3,4}, and {3,5}. Output the clique cover as C lines, with one clique per line, where each line is a
 space-separated list of integers starting with the type (0 or 1).
 A "Steiner Quadruple System" (or SQS) of order v consists of a set of blocks, with each block
 containing 4 elements of the set V={0,1,...,v-1}, such that each subset of 3 elements of V is
 contained in exactly one block. There are v*(v-1)*(v-2)/6 subsets of 3 elements of V, and each
 block covers 4 of these subsets, so the SQS will have v*(v-1)*(v-2)/24 blocks. A "Uniform
 Nested Steiner Quadruple System" of order v splits each block into two "ND-pairs" of two
 elements each, such that each distinct ND-pair appears the same number of times. Set p denote
 the number of distinct ND-pairs that appear among the blocks; it may be that each of the v*(v-1)/2
 subsets of 2 elements from V appears as an ND-pair so that p = v*(v-1)/2, or it may be that some
 subsets of 2 elements from V don’t appear as an ND-pair and then we have p < v*(v-1)/2. There
 are v*(v-1)*(v-2)/12 ND-pairs, so each of the p distinct ND-pairs appears v*(v-1)*(v-2)/(12*p)
 times. We call such a design a UNSQS(v,p). Given (v,p) we want to construct a UNSQS(v,p).
 For our purposes, 8<=v<=58 and 28<=p<=1260. Output the UNSQS(v,p) as v*(v-1)*(v-2)/24
 lines, one block per line, with each line having a space-separated list of 4 numbers identifying the
 elements of V in the block. The first ND-pair in a block should be the first two elements listed for
 the block, and the second ND-pair is the last two elements listed. Order does not matter within an
 ND-pair.
 A "Covering Array of Strength 3" CA3(N,k,v) is an N x k array (N rows and k columns), with
 each entry from the v-set of symbols {0,1,...v-1}, so that every N x 3 subarray contains every
 ordered triple of symbols at least once. Given (N,k,v), we want to construct CA3(N,k,v). For our
 purposes, N<1000, k<1000, and v<6. Output the CA3(N,k,v) as N lines with one row per line,
 with each line a space-separated list of k columns where each column is an integer in {0,1,...,v-1}.
Table 7: Definitions for use in prompting: Feb. 2025 combinatorial design problems. Note the
definitions use ASCII symbols for the sake of prompting.




                                                   15
 A "Cap Set" CS(n,s) is a subset S of Z_3^{n}, such that S has at least s distinct points, and
 no three points {x,y,z} in S satisfy x+y+z=0 (vector addition over Z_3^{n}, so addition is taken
 modulo 3). We represent the cap set by an array with at least s rows, and n columns in each row.
 Elements of the array are from Z_3={0,1,2}, and each row represents a point in Z_3^{n} which is
 an element of S. Given (n,s) we want to construct a Cap Set CS(n,s).
 A "Deletion Code" DC(n,s,m) with parameters (n,s,m) is a set m binary words of length n, such
 that any two distinct words from the set do not share any any length n-s word obtained by deleting
 s bits from each of the two words. Given a length n word x, let D(x) be the set of length n-s words
 obtained from x by deleting two distinct bits (at positions which need not be adjacent). Note
 D(x) has (n choose s) members. Our requirement is that, for any two distinct words x and y in
 DC(n,s,m), D(x) and D(y) have the empty intersection. Given (n,s,m) we want to construct a
 DC(n,s,m). For our purposes, 7<=n<=16, s is 2 or 3, and m<250. Output the DC(n,s,m) as an m
 by n array, where each row is a space-separated list of n bits in {0,1} representing one word in the
 Deletion Code.
Table 8: Definitions for use in prompting: FunSearch problems. Note the definitions use ASCII
symbols for the sake of prompting.




                                                 16
B Appendix: Solutions to Open Instances of Combinatorial Design Problems
Figures 2 to 8 show verified designs that resolve open instances of combinatorial design problems
as noted in Table 1. Each of these was constructed by code that was generated by protocol CPro1,
and that code is available in the github repository 3 . One example is provided here for each type of
combinatorial design – remaining solutions are in the repository.


   0 0 0 −1 0 1 −1 0 −1 1 −1 −1 −1 1 1 −1 0 1 1 −1 1 1
   0 0 0 1 0 −1 0 1 1 1 1 −1 0 −1 −1 −1 −1 1 −1 −1 1 1
   0 0 −1 −1 0 0 0 1 −1 −1 1 1 −1 1 −1 −1 0 −1 −1 −1 −1 1
  −1 1 −1 0 −1 0 −1 0 −1 −1 −1 −1 −1 −1 −1 1 0 1 −1 1 0 0
   0 0 0 −1 −1 −1 1 0 −1 −1 1 1 0 −1 1 1 −1 1 1 −1 1 0
   1 −1 0 0 −1 −1 −1 0 −1 1 −1 1 0 −1 −1 −1 −1 −1 1 1 0 0
  −1 0 0 −1 1 −1 −1 0 1 1 1 1 −1 1 −1 1 0 1 1 1 0 0
   0 1 1 0 0 0 0 −1 1 −1 −1 1 0 −1 −1 −1 1 1 1 −1 −1 1
  −1 1 −1 −1 −1 −1 1 1 0 1 0 −1 1 0 0 −1 1 0 1 0 −1 −1
   1 1 −1 −1 −1 1 1 −1 1 0 0 0 1 1 −1 0 −1 0 0 1 1 1
  −1 1 1 −1 1 −1 1 −1 0 0 −1 0 −1 0 0 −1 −1 −1 −1 0 1 −1
  −1 −1 1 −1 1 1 1 1 −1 0 0 0 1 −1 −1 0 1 0 0 1 1 1
  −1 0 −1 −1 0 0 −1 0 1 1 −1 1 1 −1 1 1 0 −1 −1 −1 0 1
   1 −1 1 −1 −1 −1 1 −1 0 1 0 −1 −1 0 0 1 1 0 −1 0 −1 1
   1 −1 −1 −1 1 −1 −1 −1 0 −1 0 −1 1 0 −1 0 1 0 0 −1 1 −1
  −1 −1 −1 1 1 −1 1 −1 −1 0 −1 0 1 1 0 0 −1 1 0 0 −1 1
   0 −1 0 0 −1 −1 0 1 1 −1 −1 1 0 1 1 −1 1 1 −1 1 1 0
   1 1 −1 1 1 −1 1 1 0 0 −1 0 −1 0 0 1 1 −1 1 0 1 1
   1 −1 −1 −1 1 1 1 1 1 0 −1 0 −1 −1 0 0 −1 1 0 0 −1 −1
  −1 −1 −1 1 −1 1 1 −1 0 1 0 1 −1 0 −1 0 1 0 0 −1 1 −1
   1 1 −1 0 1 0 0 −1 −1 1 1 1 0 −1 1 −1 1 1 −1 1 0 0
   1 1 1 0 0 0 0 1 −1 1 −1 1 1 1 −1 1 0 1 −1 −1 0 −1

                         Figure 2: Symmetric Weighing Matrix with n=22 w=16




   3
       https://github.com/Constructive-Codes/CPro1


                                                     17
     1     0    0     1    0    −1    1     0    0     0    0     0    1     0    0
     1     0    0     0    1     0    0     1    0     0    0     0   −1     0   −1
     0     0    0     0    0     0    0     1   −1     1   −1     0    1     0    0
     0     0   −1     0    0     0    0     0    1     0    1     0    0    −1    1
     0     0    0     0    1     1    0     0    0     1    0     0    1    −1    0
     0    −1    0    −1    0    −1    0     1    0     0    0     0    0     1    0
     0    −1    0     0   −1     0    0     0    0     0    1     0    1     0   −1
     0     1   −1     1    0     0    0     0    0     0    1     0    1     0    0
     0     0   −1    −1    0     1    0     0    0     0    0     1    0     0   −1
     0     0    0     0    0     0    1     1    0     0    1     1    0     1    0
     0     0    0     1   −1     0    0     0    1     1   −1     0    0     0    0
     0     1    0     0    0    −1   −1    −1    0     0    0     0    0     0   −1
     1     0    0     0    0     0    1     0    1     0    0     0   −1     1    0
     0     0   −1     0    0     0    0     0    0     0    0    −1   −1    −1   −1
     1    −1    0     1    0     0    0     0    0    −1    0     0    0    −1    0
     1     1    0     0    1     0    0     0    0    −1    0     1    0     0    0
     0     0    0     0    0     1    0     0    1    −1    0    −1    0     0    1
     0    −1   −1     0    0    −1    0     0    1     1    0     0    0     0    0
     1     0    0     0    0     1    0     0    1     0   −1     1    0     0    0
    −1     0    1     0    1     0    0     0    1     0    0     0    0    −1    0
     1     0    0     0    0     0   −1     0    0     1    1     0    0     0    1
     0     0    0     1    0     0    1     0   −1     0    0    −1   −1     0    0
     1     0    0     0   −1     1   −1     0    0     0    0     0    0     0   −1
     0     1    0    −1   −1     0    0     0   −1     0    0     0    0     0    1
     0     0    1     0    0     0    1    −1    0    −1    0     0    1     0    0
     0     0    1     0   −1    −1    0     0    0     0    0     0   −1    −1    0
     1     0    1    −1    0     0    0    −1    0     1    0     0    0     0    0
     0     0    0     1    0     0    0     0    0     1    0     1   −1     0    1
     0     0    0     0    1    −1    0    −1    0     0   −1     1    0     0    0
     0     0    0    −1    0     0    0     1    0     0   −1     0    0    −1    1
     0     0   −1     0    0    −1   −1     0    0    −1   −1     0    0     0    0
    −1    −1   −1     0    0     0    0    −1    0     0    0     1    0     0    0
     0    −1    0     0    0     1    0    −1   −1     0    0     0   −1     0    0
    −1     0    1     0    0     0    0     1    1     0    0     0    0     0   −1
     0     0    0     1    1     0   −1     1   −1     0    0     0    0     0    0
     0     0   −1    −1    1     0    1     0    0     0    0    −1    0     0    0
     0     1   −1     0   −1     0    1     0    0     0   −1     0    0     0    0
     0     1    0     0    0     0    1     0    0     1    0     0    0    −1   −1
     1     0    0    −1    0    −1    0     0    0     0    1     0    0    −1    0
     0    −1    0     0    0     0    1     0   −1     0    0     1    0    −1    0
     1    −1    0     0    0     0    0     0    0     0   −1    −1    1     0    0
     0     0    0     0   −1     0    0     1    0    −1    0     1    0    −1    0

Figure 3: Bhaskar Rao Design with parameters (15,42,14,5,4). Note the transpose is shown.




                                           18
     0   0   2   0   0   1   0   1   0   1   1    0   1   1   0   0   1   0   0   0   1   1
     2   1   1   1   0   1   0   0   0   0   0    1   1   0   0   1   0   0   1   0   0   1
     1   0   1   0   0   1   2   1   1   0   1    0   0   0   0   1   0   1   0   1   0   0
     1   0   0   0   1   0   0   0   1   0   2    1   1   1   1   0   0   0   0   1   0   1
     0   1   0   0   1   2   1   0   0   1   0    1   1   1   1   0   0   1   0   0   0   0
     0   1   0   0   0   1   0   1   1   0   0    1   1   0   0   0   1   0   1   2   1   0
     1   0   0   0   1   0   1   2   0   1   0    1   0   0   1   0   1   0   1   0   0   1
     0   0   1   1   0   0   1   0   0   0   0    1   0   2   1   1   1   0   1   1   0   0
     1   1   1   0   1   0   0   0   2   1   0    0   0   1   0   0   1   1   1   0   0   0
     0   0   1   1   2   0   1   0   0   0   0    0   1   0   0   0   0   1   1   1   1   1
     1   1   0   1   0   0   1   0   0   0   1    0   1   0   1   0   2   1   0   0   1   0
     0   0   0   1   0   1   0   0   1   1   0    0   0   0   1   1   1   1   0   1   0   2
     0   0   0   1   0   0   1   0   1   2   1    1   1   0   0   1   0   0   1   0   1   0
     0   1   0   0   0   0   0   1   0   0   1    1   0   1   0   1   0   2   1   0   1   1
     0   2   1   1   1   0   0   1   0   1   1    0   0   0   1   1   0   0   0   1   0   0
     1   0   0   1   1   1   0   1   1   0   0    0   0   1   1   1   0   0   0   0   2   0

         Figure 4: Balanced Ternary Design with parameters (16,22;9,1,11;8,5)




01011101010011100001000000110110011001101101000101011000111101111110010

                     Figure 5: Covering Sequence with n=9 R=1 L=71




                                             19
                                                   0   1    9   11
0    2    3     4                                  0   3    8    9
1    1    3     4    9   13                        0   8   10   12
0    3    9    12                                  0   1    7   10
0    1    2     3                                  0   1    5    9
1    1    3     5    6   11                        1   2    3    5    9   10
0    5    7    10                                  0   3    5   13
0    2    8     9                                  0   3   10   12
0    2    5    12                                  0   2   10   13
0    6    7     8                                  0   1   12   13
0    3    6    13                                  0   7   10   11
0    2    6     9                                  0   4   12   13
0    2    9    13                                  1   2    3    6    8    9
0    1   11    13                                  1   5    6    8    9   10
0    1    6     8                                  1   4    5    8   11   13
0    9   10    11                                  0   1    5   10
0    1    4     6                                  0   2    6   12
1    5    9    10   12   13                        0   2    4   11
0    3    6    10                                  0   4    9   10
1    1    2     6   10   11                        1   3    4    7    8   10
0    3   10    13                                  1   2    4    5    7    8
1    1    6     7    9   13                        0   3    6    9
1    6    8     9   12   13                        1   3    4    5    6    7
1    4    5     6   11   12                        0   7    9   10
1    3    7     9   11   13                        0   2    8   13
0    6    7    11                                  1   1    7    8    9   12
0    2    8    12                                  1   4    8    9   11   12
0    1    2     7                                  0   6   10   12
1    3    5     7   11   12                        1   1    5    7    8   13
0    4    5     9                                  0   2    3    7
0    4    7    12                                  0   8    9   13
0    3    8    13                                  1   1    3    4    5   12
0    6    8    11                                  0   3    8   12
0    5    7     9                                  0   5    9   11
0    2    8    10                                  0   1   11   12
0    6    9    12                                  0   1    4    8
0    1    4    10                                  0   1    9   10
0    6   10    13                                  1   4    6    9   11   13
1    2    5     7   11   13                        0   3    4   11
0    4    7     9                                  0   2    3   11
0    2    5     6                                  0   4    6    8
1    1    5     6    7   12                        1   1    2    5    8   11
0   11   12    13                                  1   2    3    9   12   13
0    7   12    13                                  0   3    6   12
1    1    3     8   10   11                        0   4   10   11
1    1    2     4    9   12                        0   5   10   11
0    2    6    13                                  0   4    5   10
0    7    8    11                                  1   1    4    5    7   11
0    8   10    13                                  0   5    8   12
0    4    7    13                                  1   1    2    4    5   13
1    2    7     9   11   12                        1   2    4    6    7   10
0    1    3     7                                  0   5    6   13
0    3    5     8
0    2   10    12
              Figure 6: Johnson Clique Cover with N=13 k=4 C=105




                                     20
                                                2   13    3    4
0    1    2    3                                2    8    3    5
0    4    1    5                                2   11    3    6
0    6    1    7                                2    3    7   12
0    9    1    8                                2   10    3    9
0   10    1   11                                2    4    5   10
0    1   12   13                                2    4    8    9
0    4    2    6                                2   11    4   12
0    7    2    5                                2    5    9   11
0   10    2    8                                2   12    5   13
0    2    9   12                                2    9    6    7
0    2   11   13                                2    6    8   12
0    8    3    4                                2   10    6   13
0    5    3    9                                2   13    7    8
0    3    6   10                                2    7   10   11
0    3    7   13                                3   11    4    5
0   11    3   12                                3   12    4    6
0   11    4    7                                3    7    4    9
0   13    4    9                                3   13    5    6
0   12    4   10                                3    5    7   10
0    5    6   12                                3    7    6    8
0    8    5   11                                3    8    9   12
0   13    5   10                                3    8   10   11
0    6    8   13                                3   11    9   13
0    9    6   11                                3   10   12   13
0   12    7    8                                4    6    5    7
0    7    9   10                                4    5    8   13
1    4    2    7                                4   12    5    9
1    2    5    6                                4    8    6   11
1    2    8   11                                4   10    6    9
1   13    2    9                                4    7    8   10
1   10    2   12                                4   13    7   12
1    4    3   10                                4   11   10   13
1    3    5   12                                5    8    6    9
1    9    3    6                                5   11    6   10
1    3    7   11                                5    9    7   13
1    8    3   13                                5    7   11   12
1    6    4   13                                5   12    8   10
1   12    4    8                                6    7   10   12
1    9    4   11                                6   13    7   11
1    7    5    8                                6   12    9   13
1    5    9   10                                7    9    8   11
1   11    5   13                                8    9   10   13
1   10    6    8                                8   12   11   13
1    6   11   12                                9   11   10   12
1   12    7    9
1   13    7   10
Figure 7: Uniform Nested Steiner Quadruple System with v=14 p=91




                              21
 0   1   1   1   1   1    1   0   0   0   0   1
 1   1   0   0   0   0    0   0   1   1   1   1
 0   1   1   0   1   1    1   1   1   1   0   1
 1   1   1   0   1   1    0   0   0   1   0   0
 1   1   1   1   1   1    1   1   1   1   1   1
 1   1   1   1   0   1    0   1   0   1   0   1
 0   0   0   0   0   1    1   1   1   1   1   1
 0   0   0   1   1   1    1   0   0   0   0   0
 1   1   0   0   0   1    0   0   0   0   0   0
 1   0   0   1   1   1    0   1   1   1   1   1
 1   1   1   1   1   1    1   1   1   0   0   0
 0   0   1   1   0   0    0   0   0   0   1   0
 1   1   1   0   1   1    0   0   1   1   1   1
 1   1   1   1   0   0    0   0   0   0   0   1
 0   0   0   0   0   0    0   0   0   0   0   0
 0   0   0   1   1   0    0   1   1   1   1   0
 1   1   1   1   0   0    0   0   1   1   1   0
 1   0   0   1   1   0    0   1   1   0   0   0
 0   1   0   0   1   1    1   0   1   0   1   0
 1   0   0   0   0   1    0   0   0   1   1   0
 1   0   0   0   0   1    1   1   1   1   0   0
 0   0   0   1   0   1    1   1   0   0   1   1
 0   1   1   1   0   0    1   0   0   0   1   1
 0   0   0   0   0   0    1   1   1   0   0   0
 0   0   1   1   1   1    0   1   1   1   0   0
 0   0   0   0   0   0    0   0   0   1   1   1
 1   0   1   0   1   0    0   0   0   1   0   1
 1   1   1   0   0   1    1   1   1   0   0   1
 0   0   1   0   1   0    1   0   0   1   0   0
 1   1   0   0   0   1    1   0   1   0   1   1
 0   0   1   1   1   0    0   0   1   1   0   1
 0   1   0   0   0   1    1   0   0   0   0   1
 0   1   1   0   0   0    1   0   1   1   0   0
 0   1   0   1   0   1    0   1   0   1   1   1
 0   0   0   0   0   1    0   1   0   1   0   1
 1   0   1   1   1   1    1   0   0   1   1   0

Figure 8: Deletion Code with n=12 s=2 m=36




                     22
