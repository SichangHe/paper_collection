                                                                     Learning to Solve and Optimize by Evolving Code

                                                            Veronika Semmelrock∗1 , Benedetta Strizzolo∗2 , Francesco Zuccato∗1 ,
                                                             Gerhard Friedrich∗1 , Patrick Rodler∗1 and Konstantin Schekotihin∗1
                                                                                1
                                                                                  University of Klagenfurt, Austria
                                                                                    2
                                                                                      University of Udine, Italy
                                                                 {firstname.lastname}@aau.at, strizzolo.benedetta@spes.uniud.it

                                                                     Abstract                                     often requires redesigning problem specifications [Dodaro
arXiv:2605.31049v1 [cs.LG] 29 May 2026




                                                                                                                  et al., 2024], crafting problem-specific heuristics [Comploi-
                                              Combinatorial and optimization problems are fun-                    Taupe et al., 2023], decomposing the problem into manage-
                                              damental to many industrial AI applications. Solv-                  able subproblems [El-Kholany et al., 2025], or implementing
                                              ing large-scale real-world instances of such prob-                  tailored local-search procedures [Sanghikian et al., 2026].
                                              lems typically requires careful problem formal-                        To address these challenges, we build on recent advances
                                              ization, specialized solvers, and expert-designed                   in program generation via code evolution [Novikov et al.,
                                              heuristics. Thus, experts need to specify not only                  2025]. Our approach integrates a new C HECK M ATE com-
                                              what solutions are, but also how they are derived.                  ponent into the OpenEvolve [Sharma, 2025] controller loop.
                                              By introducing the tool C HECK M ATE, we show                       Given a natural-language description and a formal specifica-
                                              that algorithm generation via code evolution rep-                   tion of what solutions are, along with a training set of rep-
                                              resents a paradigm shift by eliminating the need                    resentative instances, OpenEvolve+C HECK M ATE automati-
                                              to formulate the how. C HECK M ATE solely relies                    cally synthesizes a problem-specific solver—implemented as
                                              on the what. Specifically, a formal specification                   a Python program—without requiring any formulation of how
                                              ensures solutions’ correctness and enables system-                  to solve the problem.
                                              atic performance evaluation of the generated pro-                      We investigate the following research questions:
                                              grams, while a natural language description guides                      RQ1 Can OpenEvolve+C HECK M ATE solve hard real-
                                              the evolutionary process.                                                     world (a) combinatorial and (b) optimization prob-
                                              The effectiveness of our method is demonstrated                               lems, such as configuration and scheduling?
                                              on selected problems from two industrial domains:                       RQ2 How does the performance of the generated pro-
                                              configuration and scheduling. In all cases, the                               grams compare to state-of-the-art solvers?
                                              evolved algorithms consistently outperform state-                       RQ3 How well do these evolved programs scale?
                                              of-the-art solvers. This underscores the potential of                  Our evaluation targets configuration problems from auto-
                                              formal methods in guiding code evolution for auto-                  mated engineering and an industrial scheduling problem. We
                                              matically solving complex real-world problems.                      analyze two configuration tasks from Siemens that capture
                                                                                                                  pivotal real-world challenges: one stresses solver scalabil-
                                                                                                                  ity with respect to solution size [Semmelrock and Friedrich,
                                         1    Introduction                                                        2025], and the other examines solver behavior when several
                                         Combinatorial and optimization problems are central to many              difficult problems are combined [Gebser et al., 2015]. In
                                         industrial AI applications, including the automated engi-                addition, we evaluate a real-world scheduling problem from
                                         neering of technical systems (e.g., configuring and planning             metalworking at voestalpine [Zuccato et al., 2025].
                                         the composition of large electronic systems) [Falkner et al.,               Across all tasks, OpenEvolve+C HECK M ATE generated
                                         2016] and the automation of process planning and scheduling              problem-specific code that outperformed the respective state-
                                         [Da Col and Teppan, 2022]. A long-standing vision in AI is               of-the-art solvers by orders of magnitude on large or hard
                                         that domain experts should specify what constitutes a correct            instances. Thus, our approach extends to solving problems
                                         solution, while the computer should determine how to obtain              where leading solvers cannot deliver solutions.
                                         it efficiently [Freuder, 2018].
                                            In practice, however, applying state-of-the-art solvers from          2   Preliminaries
                                         constraint [Laborie et al., 2018], logic [Kaufmann et al.,
                                                                                                                  Since our contribution integrates with OpenEvolve [Sharma,
                                         2016], or mathematical programming [Perron et al., 2023] to
                                                                                                                  2025], an open-source implementation of AlphaEvolve
                                         large real-world problem instances still demands substantial             [Novikov et al., 2025], we provide a brief overview of
                                         expert intervention beyond the what. Effective deployment
                                                                                                                  this framework. OpenEvolve is a code optimization frame-
                                            ∗                                                                     work that automatically generates programs capable of solv-
                                              The first three authors contributed equally and are listed in al-
                                         phabetical order. The same holds for the last three authors.             ing specified problems by leveraging evolutionary computa-
tion and the capabilities of Large Language Models (LLMs)             3.1      Program Execution and Evaluation
in program synthesis. This framework operates through                 In each training iteration j ≤ N , in order to evaluate the
an asynchronous pipeline consisting of four core modules:             generated program pj , C HECK M ATE:
(i) a prompt sampler that generates prompts using previously           (1) Executes pj on a training instance i ∈ I: if pj fails, go to
evolved programs and their evaluation scores, (ii) an LLM                  (4) and forward ⟨incorrect, feedback ⟩, where the feed-
ensemble, i.e., a set of LLMs that process prompts and pro-                back details the failure reason, e.g., an error stack trace;
duce full code rewrites or targeted edits, (iii) an evaluator              otherwise, go to (2) and forward candidate solution cji ;
pool that scores and ranks generated programs, and (iv) a pro-         (2) Syntactically checks cji : if the check fails, go to (4) and
gram database that stores these programs and their scores in               forward ⟨incorrect, feedback ⟩, where the feedback in-
a structured grid [Mouret and Clune, 2015], organizing them                cludes, e.g., syntactic errors in cji ; else, go to (3) and
according to diverse user-defined criteria, such as code com-              forward cji parsed into the verifier-specific format;
plexity and correctness. Note that the evaluator pool, at its          (3) Checks the correctness of cji using the verifier V :
core, is an evaluation function that the user must implement.              if the check returns positively, go to (4) and for-
An island-based genetic algorithm [Tanese, 1989] manages                   ward ⟨correct, ∅⟩; else, go to (4) and forward
selection, migration, and evolution across iterations.                     ⟨incorrect, feedback ⟩, where feedback includes, e.g., vi-
   Adopting OpenEvolve’s terminology, we denote an arti-                   olated constraints in F ;
fact as a textual error-feedback provided to the LLM, and the          (4) Stores feedback and evaluates pj ’s performance on in-
combined score zj ∈ [0, 1] as a numerical score assigned to                stance i using the scoring functions S, based on the ver-
program pj . Intuitively, the higher the combined score, the               dict (correct/incorrect) as well as statistics such as run-
higher the likelihood for the program to be selected by the                time, consumed memory, and resulting objective values.
prompt sampler and to guide further evolution.
                                                                      This process is repeated for all training instances i ∈ I,
                                                                      or until the early stopping is triggered due to k consecutive
3   Approach                                                          incorrect verdicts.1
Extending OpenEvolve’s pipeline (Sec. 2), our approach                   Finally, C HECK M ATE (i) aggregates the instance-level
C HECK M ATE provides a general, problem-independent im-              scores from Step (4) to determine zj , the combined score
plementation of the evaluator pool that employs state-of-the-         of pj , and (ii) returns zj with the stored feedback for all in-
art solvers as verifiers to check the correctness of programs’        stances (i.e., artifacts) to OpenEvolve’s main controller loop.
produced problem solutions. Fig. 1 illustrates the integrated
framework, with our contributions highlighted in the dashed           3.2      Textual Feedback
blue box. OpenEvolve+C HECK M ATE expects the following
                                                                      The artifacts (cf. Sec. 2) are used to provide textual feedback
inputs: (i) a natural language description D of the problem
                                                                      directly to the LLM. They depend on the underlying failure
(prompt), (ii) a formal specification F defining valid prob-
                                                                      type, of which we distinguish five kinds: (i) execution ex-
lem solutions, (iii) a solution verifier V , (iv) a set of training
                                                                      ceptions, such as compilation or runtime errors, (ii) inten-
problem instances I (for which valid problem solutions are
                                                                      tional exceptions, raised by the evolved program itself due to
assumed to exist), (v) a set S of scoring functions for pro-
                                                                      a precondition or invariant violation, (iii) exceeded resource
gram evaluation, (vi) a (possibly empty) initial program p0 ,
                                                                      errors, whenever (user-defined) time or memory limits are
and (vii) a set of evolution and LLM hyperparameters Λ.
                                                                      reached, (iv) syntactic errors, e.g., an incomplete candidate
   Given the inputs, OpenEvolve+C HECK M ATE, denoted as
                                                                      solution, and (v) semantic errors, if the verdict of V for cji
the function generator g, produces a program p∗ . Formally:
                                                                      equals incorrect.
                 g : (D, F , V , I , S , p0 , Λ) 7→ p∗                   Each artifact comprises the failed instance, the failure type,
The generation of p∗ involves N training iterations, with N           and a suggestion for repairing the failure. The suggestion
defined in Λ. At each iteration 1 ≤ j ≤ N , the LLM ensem-            proposes an improvement to the program in natural language,
ble non-deterministically generates an intermediate program           depending on the failure type. It can include the stack trace,
pj , aiming to improve the programs p0 , . . . , pj−1 . C HECK -      the error message, the position of syntactic errors, or the set
M ATE evaluates pj by producing the combined score zj . Af-           of violated constraints or logical sentences. The artifact is
ter N iterations, the pj achieving the highest zj will then cor-      stored alongside program pj and is injected into the prompt
respond to the final best program p∗ .                                whenever pj is selected in subsequent iterations.
   At the core of C HECK M ATE, the solution verifier V is
used to check the correctness of program outputs. Specifi-            Failure Protocol: Self-refined feedback on program-level.
cally, given a program pj , which (possibly) generates a can-         To support the evolution process when programs do not pro-
didate solution cji for a problem instance i, V outputs (i) a         duce candidate solutions, we introduce the Failure Protocol
verdict ∈ {correct, incorrect} indicating whether cji is an           as part of the textual feedback mechanism. By instructing the
(in)correct solution for i , and, (b) in case of incorrect, some      LLM via the prompt to implement this protocol, we enable
feedback detailing which parts of the formal specification F          a program-level self-refinement loop. Whenever the program
are violated by cji . Formally:                                       expects that the ongoing candidate solution generation will
                                                                      fail, it should raise one of the following exceptions, indicat-
     pj : i 7→ cji     V : (F, i, cji ) 7→ ⟨verdict, feedback ⟩       ing that it believes (i) the instance has no correct solution,
C HECK M ATE’s overall program evaluation process, employ-
                                                                         1
ing V , is detailed next.                                                    On early stopping, unevaluated instances are deemed incorrect.
                                                                                     scoring                    formal                  solution
                                                        training set
                                                                                    functions                specification              verifier




              empty initial         OpenEvolve
               program             Controller Loop
                                                            Cascading Evaluator                                         Checker
                                                                                                YES: solution
                                            program                execution                    with objective           syntactic
                                 Prompt                                                             values
                                 Sampler
                 natural                                                                                                parsed solution

                language                                               successful
                                                                       execution?                    NO:
                 prompt            LLMs
                                                                                                  feedback
                                                                                                                             correct?
                                 Ensemble                                                                                                          best program
                                                                   NO: stacktrace                                     YES: parsed solution

                                 Program
                                            score and                                             correct or
                                 Database
                                            feedback
                                                                  evaluation                    incorrect with          semantic
               parameters                                                                         feedback

                                                                                                                                CheckMate




                                     Figure 1: System overview of the proposed evolution framework


(ii) the instance has a correct solution but the implemented                             quality-efficiency zjqe trade-off scores. The correctness score
search strategy will not find it, or (iii) it cannot recover from                        builds upon the number of training instances i ∈ I solved,
wrong decisions.                                                                         while the quality-efficiency score combines the quality score
   Exceptions raised in accordance with the Failure Protocol                             zjq and the efficiency score zje . The quality score reflects the
are referred to as intentional exceptions. They include addi-                            optimization of the objective values, whereas the efficiency
tional information that the program considers useful feedback                            score combines the runtime and memory consumption.
for evolution. During execution, C HECK M ATE intercepts in-                                In particular, C HECK M ATE (i) normalizes the raw statis-
tentional exceptions and parses them into artifacts, including                           tics into scores in [0, 1];2 (ii) aggregates the instance-level
the suggestion that the error indeed lies within the program,                            scores into the overall correctness zjc , quality zjq , and effi-
because all instances are assumed to be satisfiable.                                     ciency zje scores; (iii) combines the quality and efficiency
                                                                                         scores into the composite quality-efficiency tradeoff score
3.3   Inputs                                                                             zjqe ; and (iv) combines zjc , zjqe into the combined score zj .
In this section, we present the inputs to the code evolution                             To address these tasks, we employed an exponential decay
framework that are either novel or central to our approach.                              function for Step (i), the arithmetic mean for (ii), and combi-
Formal specification and solution verifier. The formal                                   nations of harmonic mean, product, and Prioritized Ordered
specification F is used by the verifier V to check if a can-                             Weighted Average (POWA) [Yager, 2009] for (iii) and (iv).
didate solution cij yielded by the program pj is correct for
                                                                                         Training set. The training set should include representa-
the problem instance i. It can be provided, e.g., in the form
                                                                                         tive instances of various difficulty levels. Since the initial
of constraints or logical sentences depending on the selected
                                                                                         program p0 is empty, including sufficiently easy instances is
V , such as clingo [Gebser et al., 2019], or CP Optimizer [La-
                                                                                         highly recommended to enable the evolutionary process to
borie et al., 2018]. Since F is used solely to check, there is
                                                                                         get started. In early iterations, the main challenge is to solve
no need to tune it for solving, e.g., by employing guessing or
                                                                                         at least some instances. Once this occurs, the scoring func-
symmetry-breaking techniques.
                                                                                         tion becomes informative, yielding non-zero correctness val-
Prompt. The natural language description D is a solver-                                  ues and therefore a useful combined score, enabling the pro-
agnostic specification designed to be independent from the                               gram to evolve effectively. As training progresses, it appears
format of the solution verifier. It is structured as a domain-                           that instances of moderate difficulty promote generalization,
specific prompt which contains: (i) the LLM identity, (ii) the                           while hard ones support scaling and efficiency improvements.
task to be performed, (iii) the problem description including
context, core entities, and constraints that must be satisfied,
and (iv) instructions on expected input/output formats and al-                           4      Case Studies
gorithm requirements. This structured approach provides the                              In this work, we demonstrate the effectiveness of our ap-
LLM with the necessary context for generating programs.                                  proach on the three case studies motivated in Sec. 1. This
Scoring functions. The scoring functions constitute one of                               section provides a high-level overview of these case studies.
the most fundamental components of the learning process, as
they affect how programs are ranked, selected, and evolved                                   2
                                                                                               Normalization must ensure the maximization of each score. For
across iterations. As introduced in Sec. 3.1, they are em-                               decision problems, we assign a trivial quality score of 1 to any cor-
ployed to derive zj , the combined score of each program                                 rect solution, whereas for optimization problems, we require lower
pj . Specifically, zj is built upon the correctness zjc and the                          and upper bounds for each objective of every instance for scoring.
4.1       House Configuration Problem                             5.1   Datasets
The technology-independent House Configuration Problem            For each case study, we use separate training and test sets, all
(HCP) [Fleischanderl et al., 1998; Friedrich et al., 2011]        comprising easy, moderate, and hard instances.
was introduced by Siemens and abstracts electronic modules,          For the CCP, we reuse the dataset of Gebser et al. (2015),
frames, and racks into things, cabinets, and rooms. Specif-       which comprises 99 instances: 30 easy, 33 moderate, and 36
ically, persons own multiple things, whereas each thing be-       hard, which, for brevity, we will denote by 30/33/36. For the
longs to exactly one person. The task is to assign things         training set, we select 20 instances, split as 3/7/10, as such a
to cabinets and cabinets to rooms while satisfying capacity,      split was employed to define the CCP’s competition instances
ownership, and ordering constraints (the latter introduced in     for the 6th ASP Competition [Gebser et al., 2017]. More-
[Semmelrock and Friedrich, 2025]).                                over, we generate and include 5 more very easy instances (cf.
                                                                  Sec. 3.3) by reducing the number of components in the easy
4.2       Combined Configuration Problem                          ones. Hence, the CCP’s training set includes 25 instances
                                                                  (8/7/10), while the test set comprises the 79 remaining ASP
The Combined Configuration Problem (CCP) [Gebser et al.,          competition instances (27/26/26).
2015] is a combinatorial benchmark motivated by industrial           For the HCP and the E-DFJSP, we generate both training
product configuration tasks at Siemens, such as the configu-      and test sets, ensuring that all instances are satisfiable by de-
ration of railway control and safety systems [Falkner et al.,     sign. The training sets are composed of 15 instances, split
2016]. The problem is defined via a directed acyclic graph        as 5/5/5. For the HCP, the easy instances consist of up to
with vertices, paths, bins, colors, areas, and border elements.   5 persons (∼50 things), the moderate instances of up to 50
The CCP integrates multiple interacting subproblems that          persons (∼500 things), and the hard instances of up to 500
must be solved simultaneously: (P1) vertex coloring, (P2) bin     persons (∼5 000 things). The hardness assessments reflect
packing, (P3) partitioning into disjoint paths, (P4) matching     the results of [Semmelrock and Friedrich, 2025] on clingo’s
border elements to areas, and (P5) ensuring the connected-        performance. Likewise, for the E-DFJSP, the easy instances
ness of color-induced subgraphs. The combination of these         involve up to 10 jobs (∼60 operations), the moderate up to 50
subproblems makes the CCP very challenging for solvers.           jobs (∼300 operations), and the hard up to 500 jobs (∼3 000
                                                                  operations). This is in accordance with [Schlenkrich and Par-
4.3       Energy-Aware Double-Flexible Job-Shop                   ragh, 2022] where scheduling problems were classified as
                                                                  large-scale if they comprise at least 1 000 operations.
The Energy-Aware Double-Flexible Job Shop Problem (E-                We designed the test sets to contain an overproportional
DFJSP) scheduling problem [Gong et al., 2018] exemplifies         number of hard instances ranging from large to very large
a real-world production process at voestalpine3 , where jobs      size, in accordance with research question RQ3, i.e., inves-
consist of multiple metal-cutting operations. Each cut opera-     tigating the scalability of the evolved code. Specifically, we
tion requires selecting an eligible machine and its correspond-   used a split of 6/6/24, where the 24 hard cases comprise up
ing parameters, from a k × k grid. Between cuts, workers          to 3 000 persons (∼30 000 things) for the HCP and up to 1 000
perform setup and transport operations on the machines. A         jobs (∼6 000 operations) for the E-DFJSP, thus going signifi-
correct schedule assigns the operations to the corresponding      cantly beyond what is commonly already considered hard.
machines and workers while satisfying all constraints, such
as preventing resource overlaps. Schedules are evaluated ac-      5.2   Experiments
cording to lexicographically prioritized objectives to be min-
imized: (1) job tardiness Tard , (2) total energy consumption     Each experiment was conducted on a machine equipped with
TEC —including auxiliary, idle, and processing energy—,           an AMD EPYC 7H12 64-core Processor, with RAM usage re-
and (3) makespan Cmax . Note that, as the machine parame-         stricted to 32 GB. Timeouts for evolved programs and solvers
ters influence both processing time and energy consumption,       to find a solution for any problem were set to 600 s.
optimizing such a problem is a highly complex task.               Training. Since OpenEvolve+C HECK M ATE is inherently
   We map the objective values to the quality score zjq as fol-   non-deterministic, each evolutionary training run can produce
lows. First, Tard , TEC , and Cmax are normalized into [0, 1]     a different best program p∗ . To account for this variability, we
using the corresponding theoretical lower and upper bounds.       performed four independent training runs for each case study
Next, an exponential decay function is applied to compute         (Sec. 4), yielding four corresponding best programs p∗ .
the scores zjTard , zjTEC , and zjCmax , which are subsequently      Each problem has a specific prompt D and formal specifi-
                                                                  cation F . Exclusively for CCP, due to its hardness, (i) D in-
combined into zjq = POWA(zjTard , zjTEC , zjCmax ).               cludes the Failure Protocol (Sec. 3.2), and (ii) F is exploited
                                                                  to pinpoint violated constraints returned by the verifier when-
5       Evaluation                                                ever its verdict for a candidate solution equals incorrect.
                                                                     While most parameters were kept at OpenEvolve’s de-
In this section, we evaluate the proposed approach exper-         fault values, the following problem-specific settings were
imentally. [Semmelrock et al., 2026] provides datasets,           used: (i) the number of evolutionary iterations (50 for HCP,
evolved programs, and results.                                    75 for CCP, 100 for E-DFJSP, or, for brevity 50/75/100),
                                                                  (ii) the number of islands (3/5/5), and (iii) the migration
    3
        https://www.voestalpine.com/                              interval (10/10/15) to promote greater diversity between
evolved programs. C HECK M ATE’s early stopping parameter             Problem          HCP         CCP                    E-DFJSP
k (Sec. 3.1) was set to 3. For all case studies, program eval-                     p∗L p∗H SOL p∗L p∗H SOL             p∗L p∗H SOL
uation criteria include built-in measures of code complexity
and diversity, quantifying program length and (textual) differ-       Easy     100 100         100   63    93   100 100 100        100
ences. In addition, HCP’s and CCP’s criteria set contains the         Moderate 100 100          67   88    85    88 100 100        100
correctness, runtime, and memory usage scores. In contrast,           Hard     100 100           0   96    88     4 100 100         42
E-DFJSP contains the quality and tardiness scores to guide            Overall 100 100           28   82    89    65 100 100         61
the evolution more prominently towards programs that yield
high-quality solutions. To balance performance, efficiency,          Table 1: Percentage of test instances solved by the evolved programs
and cost [Novikov et al., 2025], we used as LLMs GPT-5 for           with the lowest and highest overall percentage (p∗L and p∗H ) and by
                                                                     the state-of-the-art solver (SOL).
60% of queries and GPT-5-mini for the remaining 40%.
Testing. Each training run outputs a best program p∗ ,
which was evaluated using C HECK M ATE (standalone; with-            are ordered using the Earliest Due Date (EDD) heuristic to
out OpenEvolve) on the described test set (Sec. 5.1). To illus-      reduce total tardiness, and operations are scheduled respect-
trate the performance variability across the four training runs,     ing precedence constraints. Per task, all feasible machine-
we focus on p∗L and p∗H . Here, p∗L (p∗H ) denotes the evolved       worker-mode combinations are evaluated to minimize total
program that attains the lowest (highest) combined score on          completion time, processing energy, and resulting machine
the test set, largely driven by the overall solving percentage.      makespan. The program maintains sorted calendars for ma-
Comparison with the baseline solvers and verifiers. To               chines, considering the interval from load start to unload com-
compare our evolved programs against state-of-the-art ap-            pletion, and for workers, who are required only during setup
proaches, we executed top-performing solvers as standalone           operations. Finally, it outputs a correct schedule together with
solving engines for each problem. For HCP and CCP,                   the corresponding objective values.
we employed clingo with the original formal specifications
                                                                     5.4   Results and Discussion
(HCP [Semmelrock and Friedrich, 2025]; CCP [Gebser et al.,
2017]), as it demonstrated strong solving performance in tests       Tab. 1 summarizes the overall and difficulty-wise solving per-
compared to a leading CP solver OR-Tools [Perron et al.,             centage for p∗L , p∗H , and the corresponding state-of-the-art
2023]. For E-DFJSP, we used CP-Optimizer, following the              solver (SOL) across the three selected case studies. For HCP
results reported in [Da Col and Teppan, 2022], together with         and E-DFJSP, both p∗L and p∗H solve all instances, whereas
a formal specification extending that of Zuccato et al. (2025)       for CCP they solve 82% and 89%, respectively. In contrast,
in terms of a more general energy consumption formulation.           SOLs perform well on easy instances but degrade substan-
                                                                     tially on the moderate and hard ones, achieving 28%, 65%,
5.3   Synopsis of the Best Evolved Programs                          and 61% overall on HCP, CCP, and E-DFJSP, respectively.
The synopses of the best evolved programs were produced              This indicates that both p∗L and p∗H are competitive and con-
through a manual analysis conducted by the authors.                  sistently outperform traditional solvers on harder instances,
HCP. HCP’s p∗H begins by verifying available capacities              underscoring the scalability of our approach.
by computing the minimum number of cabinets and rooms                   The cactus plots depicted in Figs. 2, 3, and 4 compare
required under the ownership and capacity constraints and            correctness, memory usage (top panel), and runtime (bottom
checks whether they exist. It proceeds greedily and deter-           panel) between p∗H and SOL for each problem. Instances are
ministically, sorting things, cabinets and rooms and grouping        ordered by increasing memory usage of SOL.
them by owner, which enforces the ordering constraint. The           HCP. Fig. 2 shows a clear performance gap on HCP. While
program produces a correct configuration whenever sufficient         both approaches handle the easy instances, clingo’s mem-
resources exist, without exploring alternative assignments.          ory usage increases sharply at instance 11 and remains near
CCP. CCP’s p∗H combines heuristic-guided search with                 saturation, leading to repeated timeouts (13 times), out-of-
constraint-aware pruning and bounded backtracking to con-            memory events (8 times), and internal errors (5 times) on
struct correct configurations over a state space of partial color,   all harder instances. In contrast, p∗H maintains negligible
bin, and area assignments. Instead of exhaustively enumer-           memory (average: 281 MB) and runtime (average: 0.08 s)
ating possibilities, the program incrementally builds a com-         throughout and produces no incorrect solutions. Overall, p∗H
plete assignment while discarding infeasible branches early          solves all instances with orders-of-magnitude lower resource
based on capacity, path, and area constraints, and apply-            usage, indicating superior scalability.
ing deterministic ordering for repeatability. The procedure          CCP. As can be seen from Fig. 3, p∗H manifests consistently
is not purely greedy—rejected assignments may be revisited           negligible runtimes while clingo exhibits three different run-
through limited backtracking—yet it avoids full search by            time behaviors. More specifically, clingo solves 28 instances
steering decisions via deterministic heuristics.                     within 10 s and 23 instances between 10 s and the 10 min time
E-DFJSP. E-DFJSP’s p∗H consists of a greedy scheduler                limit, while 28 instances remain unsolved. In contrast, p∗H
that first determines the set of eligible workers for each ma-       solves 89% of the instances with consistently low memory
chine and, for every cut-machine pair, selects the best ma-          and runtime, 546 MB and 0.12 s on average. Given this high
chine parameters by choosing the one with minimum process-           performance, which applies to all four best programs, even
ing time and, in case of ties, lower energy consumption. Jobs        a parallel portfolio solver combining all of them is practical
Runtime [s] Memory [GB]   32
                                                                                                                    Resource pH        Resource clingo        Resource Limit
                          16                                                                                        Timeout/OOM        Internal Error
                        0
                      600
                      300
                           0
                                0                  5                      10               15                  20                 25              30                 35

Figure 2: HCP: Comparison between the evolved program (p∗H ) and clingo wrt. memory [GB ] (above) and runtime [s] (below). Symbols
×, + depict the reason why clingo did not find a correct solution (OOM stands for out-of-memory). p∗H is always correct.

                      2.50
Runtime [s] Memory [GB]




                                    Resource pH        Resource clingo         Resource Limit
                      1.25          Timeout/OOM        Failure Protocol        Incorrect Solution

                      0.00
                       600
                          300
                           0
                                0                 10               20                30                 40             50              60                70               80

Figure 3: CCP: Comparison between the evolved program (p∗H ) and clingo wrt. memory [GB ] (above) and runtime [s] (below). Symbol
× depicts the reason why clingo did not find a correct solution (OOM stands for out-of-memory). The other symbols refer to p∗H .


and achieves a 100% solving rate across all training and test                                       age and, respectively, worst-case costs for checking the cor-
instances. This yields two key findings: (i) the best program                                       rectness of outputs of best evolved programs p∗H amounted
p∗H solves more instances and exhibits a much lower resource                                        to 3.01 s / 0.11 s / 1.93 s and 18.28 s / 0.32 s / 5.13 s per test
usage than the state-of-the-art solver, and (ii) a portfolio of all                                 instance for HCP / CCP / E-DFJSP.
four evolved programs can, to the best of our knowledge, for
the first time, successfully solve all CCP instances from [Geb-                                     6        Related Work
ser et al., 2015].
                                                                                                    Combinatorial and optimization problems. Modern
E-DFJSP. Fig. 4 compares p∗H against CP Optimizer (CPO)
                                                                                                    symbolic AI methods utilize declarative formalisms, such
for E-DFJSP. With regard to the solving rate, p∗H is success-
                                                                                                    as Answer Set Programming [Gebser et al., 2012], Con-
ful 100 % of the time on the test instances, whereas CPO fails
                                                                                                    straint Programming [Rossi et al., 2008], or Mixed Integer
to produce any solution on 14 of the 18 hardest ones due to
                                                                                                    Programming [Wolsey, 2020], to address complex com-
6 timeouts and 8 memory exhaustions. Regarding memory
                                                                                                    binatorial and optimization problems. These approaches
consumption, the two approaches exhibit comparable behav-
                                                                                                    decouple problem specification from search algorithms,
ior on the easy and moderate instances; for the hard ones,
                                                                                                    enabling domain-independent solvers to find optimal or
however, CPO’s space requirements escalate. In terms of run-
                                                                                                    near-optimal solutions using advanced techniques like
time, p∗H requires an average of 1.26 s across all instances
                                                                                                    conflict-driven clause learning and constraint propagation.
to find a solution, whereas CPO either fails to produce any
                                                                                                    However, large industrial problem instances significantly
solution or achieves, if at all, only marginally better qual-
                                                                                                    reduce solver performance in practice [Falkner et al., 2018;
ity scores despite using the entire time budget. In fact, CPO
                                                                                                    Schlenkrich and Parragh, 2022]. To improve performance,
finds the optimum only for the easiest instance (10 jobs, 1
                                                                                                    research has focused on three directions [Kotary et al., 2021]:
machine). Notably, for all instances with 200 jobs or more,
                                                                                                    (i) developing domain-specific heuristics, (ii) improving
p∗H outperforms CPO on tardiness—the objective of highest
                                                                                                    problem encodings, and (iii) configuring existing or learning
priority—by 49% on average. Furthermore, the state-of-the-
                                                                                                    new problem-specific algorithms. While designing any of
art solver cannot solve most instances with at least 500 jobs
                                                                                                    these approaches requires significant domain expertise and
within 10 min, while p∗H always succeeds in less than 4 s.
                                                                                                    manual effort, it has been observed that machine learning
Training and Checking Costs                                                                         (ML) methods can simplify this challenge in many industrial
The cost in API fees was at most C 20 per training run and                                          cases where problem instances share similar patterns.
below C 200 overall. Times per training run ranged from 1                                              For the first direction, various ML techniques have been
to 16 hours, depending on the number of iterations and the                                          proposed to learn effective heuristics from, e.g., problem in-
efficiency of the generated programs. C HECK M ATE’s aver-                                          stances or solving traces, using supervised or reinforcement
Runtime [s] Memory [GB]   32
                                   Resource pH          Resource CPO
                                   Timeout/OOM          Resource Limit
                          16
                     0
                   600




                                                                                                                                          QualityScore
                                   QualityScore(pH ) QualityScore(CPO)
                   300                                                                                                                1
                                                                                                                                      0
                                                                                                                                          1
                          0
                               0                 5               10      15       20            25             30             35

Figure 4: E-DFJSP: Comparison between the evolved program (p∗H ) and CP Optimizer (CPO) wrt. memory [GB ] (above), runtime [s]
(below, primary y-axis), and the difference on their quality score (below, secondary y-axis, gray background). If the difference is positive
then p∗H is better than CPO (when CPO does not find a solution, its quality score is 0). Symbol × depicts the instances where CPO did not
find a correct solution (OOM stands for out-of-memory). p∗H is always correct.


learning methods [Bengio et al., 2021; Lodi and Zarpellon,                    the authors of [Georgiev et al., 2025] applied AlphaEvolve
2017]. Injected into a solver, learned heuristics can signifi-                to 67 mathematical problems, and, in a few cases, verified
cantly enhance its performance in the target domain. In the                   the program-generated solutions using AlphaProof [Hubert et
second direction, ML has been used to generate or optimize                    al., 2026] and Lean [de Moura et al., 2015]. Notably, SAT-
problem encodings, e.g., by adding symmetry-breaking or                       LUTION [Yu et al., 2025] evolves entire code repositories to
implied constraints [Tarzariol et al., 2023; Taupe et al., 2020],             produce variants of SAT solvers, which operate at the propo-
or finding problem decompositions [Cappart et al., 2025]. In                  sitional level. Differently, C HECK M ATE employs first-order
the third direction, ML approaches were first used to develop                 specifications to verify the correctness of candidate solutions
portfolio solvers capable of automatically configuring exist-                 for the given problem instances. Therefore, C HECK M ATE
ing solvers for specific problem instances [Kotthoff, 2016].                  addresses an open point in prior work by providing an au-
More recently, deep learning methods have been proposed to                    tomated declarative verification approach that guarantees the
solve combinatorial problems in an end-to-end fashion [Ko-                    correctness of returned solutions.
tary et al., 2021], learning to predict (approximate) solutions
directly without invoking solvers at inference time.                          7   Conclusions
   Our approach can roughly be classified in the third direc-
tion, as we aim to automatically generate problem-specific                    The OpenEvolve+C HECK M ATE framework showed the great
solving algorithms. Unlike prior work that relies on deep                     potential to automatically synthesize problem-solving algo-
learning models, we employ evolutionary computation com-                      rithms implemented in Python. The system needs no infor-
bined with LLMs to synthesize code. This enables us to gen-                   mation on how to construct solutions. It relies only on what
erate interpretable and verifiable algorithms, rendering our                  defines a correct (optimal) solution and a set of representa-
approach more flexible without compromising performance                       tive instances. The obtained programs can efficiently tackle
across different combinatorial and optimization problems.                     large and challenging instances from the practical use cases
                                                                              of Siemens and voestalpine that are currently out of reach
Code generation for combinatorial optimization. Code                          for state-of-the-art solvers. Our analysis demonstrates that
evolution with LLMs has recently emerged as a particu-                        the generated algorithms can successfully solve difficult real-
larly relevant research topic in combinatorial optimization.                  world (a) combinatorial and (b) optimization problems such
Early frameworks, such as FunSearch [Romera-Paredes et                        as configuration and scheduling, thereby addressing RQ1.
al., 2024], focused on evolving heuristics for Cap Set and                    The evolved programs significantly outperform state-of-the-
Bin Packing problems. Subsequent works, such as Evolu-                        art solvers on hard instances, addressing RQ2. Finally, the
tion of Heuristics [Liu et al., 2024], expanded the scope to                  results highlight strong scalability: both in terms of increas-
a wider range of problems, such as online bin-packing, trav-                  ing problem size, as tested on the HCP and E-DFJSP, and in
eling salesman, and flow shop scheduling. Furthermore, Al-                    terms of increasing problem hardness, as examined with re-
phaEvolve [Novikov et al., 2025] and its open-source imple-                   gard to the CCP. This addresses RQ3 and confirms the prac-
mentations, such as OpenEvolve [Sharma, 2025], ShinkaE-                       tical viability of our approach.
volve [Lange et al., 2025], DeepEvolve [Liu et al., 2025],                       Future research should explore several promising direc-
and CodeEvolve [Assumpção et al., 2025], have applied code                  tions to further evaluate the approach and enhance its appli-
evolution to a variety of domains, focusing on the previously                 cability and robustness. For example, by using C HECK M ATE
mentioned problems, as well as matrix multiplication, the                     to verify the outputs of synthesized programs, we ensure so-
minimum overlap problem, and kissing numbers in 11 di-                        lution correctness per instance, while establishing their over-
mensions. The aforementioned approaches neither explic-                       all correctness remains important future work. Moreover, we
itly mention formal verification nor utilize software testing,                will conduct systematic ablation studies to quantify the con-
but rely on handcrafted solution checkers. More recently,                     tribution of every C HECK M ATE component.
Acknowledgments                                                [Fleischanderl et al., 1998] Gerhard Fleischanderl, Gerhard
                                                                  Friedrich, Alois Haselböck, Herwig Schreiner, and
This research was funded in whole or in part by the Austrian      Markus Stumptner. Configuring large systems using gen-
Science Fund (FWF) 10.55776/COE12 and the Austrian Re-            erative constraint satisfaction. IEEE Intell. Syst., 13(4):59–
search Promotion Agency (FFG) FO999910235 (SAELING)               68, 1998.
and 930480ATRIA (ATRIA).
                                                               [Freuder, 2018] Eugene C. Freuder. Progress towards the
                                                                  holy grail. Constraints, 23(2):158–171, 2018.
References                                                     [Friedrich et al., 2011] Gerhard Friedrich, Anna Ryabokon,
[Assumpção et al., 2025] Henrique S. Assumpção, Diego         Andreas A. Falkner, Alois Haselböck, Gottfried Schenner,
  Ferreira, Leandro Lacerda Campos, and Fabricio Mu-              and Herwig Schreiner. (re)configuration based on model
  rai. Codeevolve: An open source evolutionary coding             generation. In Second Workshop on Logics for Component
  agent for algorithm discovery and optimization. CoRR,           Configuration, volume 65 of EPTCS, pages 26–35, 2011.
  abs/2510.14150, 2025.                                        [Gebser et al., 2012] Martin Gebser, Roland Kaminski, Ben-
[Bengio et al., 2021] Yoshua Bengio, Andrea Lodi, and An-         jamin Kaufmann, and Torsten Schaub. Answer Set Solving
  toine Prouvost. Machine learning for combinatorial op-          in Practice. Synthesis Lectures on Artificial Intelligence
  timization: a methodological tour d’horizon. EJOR,              and Machine Learning. Morgan & Claypool, 2012.
  290(2):405–421, 2021.                                        [Gebser et al., 2015] Martin Gebser, Anna Ryabokon, and
[Cappart et al., 2025] Quentin Cappart, Tias Guns, Michele        Gottfried Schenner. Solving combined configuration prob-
  Lombardi, Gilles Pesant, and Dimos Tsouros. Combin-             lems: a heuristic approach. In 17th Int’l Configuration
  ing constraint programming and machine learning: From           Workshop, CEUR Workshop Proceedings, pages 55–59.
  current progress to future opportunities. JAIR, 84, 2025.       CEUR-WS.org, 2015.
                                                               [Gebser et al., 2017] Martin Gebser, Marco Maratea, and
[Comploi-Taupe et al., 2023] Richard Comploi-Taupe, Ger-
                                                                  Francesco Ricca. The sixth answer set programming com-
  hard Friedrich, Konstantin Schekotihin, and Antonius            petition. JAIR, 60:41–95, 2017.
  Weinzierl. Domain-specific heuristics in answer set pro-
  gramming: A declarative non-monotonic approach. JAIR,        [Gebser et al., 2019] Martin Gebser, Roland Kaminski, Ben-
  76:59–114, 2023.                                                jamin Kaufmann, Marius Lindauer, Max Ostrowski, Javier
                                                                  Romero, Torsten Schaub, Sven Thiele, and Philipp Wanko.
[Da Col and Teppan, 2022] Giacomo Da Col and Erich C              Potassco guide version 2.2.0, 2019. Retrieved from https:
  Teppan. Industrial-size job shop scheduling with con-           //github.com/potassco/guide/releases/tag/v2.2.0.
  straint programming. Oper. Res. Perspect., 9:100249,
                                                               [Georgiev et al., 2025] Bogdan Georgiev, Javier Gómez-
  2022.
                                                                  Serrano, Terence Tao, and Adam Zsolt Wagner. Math-
[de Moura et al., 2015] Leonardo Mendonça de Moura,              ematical exploration and discovery at scale. CoRR,
   Soonho Kong, Jeremy Avigad, Floris van Doorn, and              abs/2511.02864, 2025.
   Jakob von Raumer. The Lean theorem prover (system de-       [Gong et al., 2018] Guiliang Gong, Qianwang Deng, Xuran
   scription). In 25th Int’l Conf. on Automated Deduction         Gong, Wei Liu, and Qinghua Ren. A new double flexible
   (CADE), Lecture Notes in Computer Science, pages 378–          job-shop scheduling problem integrating processing time,
   388. Springer, 2015.                                           green production, and human factor indicators. J. Clean.
[Dodaro et al., 2024] Carmine Dodaro, Giuseppe Galatà,           Prod., 174:560–576, 2018.
  Martin Gebser, Marco Maratea, Cinzia Marte, Marco            [Hubert et al., 2026] Thomas Hubert, Rishi Mehta, Laurent
  Mochi, and Marco Scanu. Operating room scheduling via           Sartran, Miklós Z. Horváth, Goran Žužić, Eric Wieser, Aja
  answer set programming: Improved encoding and test on           Huang, Julian Schrittwieser, Yannick Schroecker, Hussain
  real data. JLC, 34(8):1556–1579, 2024.                          Masoom, Ottavia Bertolli, Tom Zahavy, Amol Mandhane,
[El-Kholany et al., 2025] Mohammed M. S. El-Kholany,              Jessica Yung, Iuliya Beloshapka, Borja Ibarz, Vivek Vee-
   Martin Gebser, and Konstantin Schekotihin. Decompo-            riah, Lei Yu, Oliver Nash, Paul Lezeau, Salvatore Mercuri,
   sition strategies and multi-shot ASP solving for job-shop      Calle Sönne, Bhavik Mehta, Alex Davies, Daniel Zheng,
   scheduling. LMCS, 21(3), 2025.                                 Fabian Pedregosa, Yin Li, Ingrid von Glehn, Mark Row-
                                                                  land, Samuel Albanie, Ameya Velingker, Simon Schmitt,
[Falkner et al., 2016] Andreas A. Falkner,        Gerhard         Edward Lockhart, Edward Hughes, Henryk Michalewski,
   Friedrich, Alois Haselböck, Gottfried Schenner, and           Nicolas Sonnerat, Demis Hassabis, Pushmeet Kohli, and
   Herwig Schreiner. Twenty-five years of successful appli-       David Silver. Olympiad-level formal mathematical reason-
   cation of constraint technologies at Siemens. AI Mag.,         ing with reinforcement learning. Nature, 651(8106):607–
   37(4), 2016.                                                   613, 2026.
[Falkner et al., 2018] Andreas A. Falkner,       Gerhard       [Kaufmann et al., 2016] Benjamin Kaufmann,                 Nicola
   Friedrich, Konstantin Schekotihin, Richard Taupe,              Leone, Simona Perri, and Torsten Schaub. Grounding
   and Erich Christian Teppan. Industrial applications of         and solving in answer set programming.               AI Mag.,
   answer set programming. KI, 32(2-3):165–176, 2018.             37(3):25–32, 2016.
[Kotary et al., 2021] James Kotary, Ferdinando Fioretto,          [Rossi et al., 2008] Francesca Rossi, Peter van Beek, and
   Pascal Van Hentenryck, and Bryan Wilder. End-to-end               Toby Walsh. Constraint programming. In Handb. Knowl.
   constrained optimization learning: A survey. In 30th Int’l        Represent., volume 3 of Foundations of Artificial Intelli-
   Joint Conf. on Artificial Intelligence, pages 4475–4482. ij-      gence, pages 181–211. Elsevier, 2008.
   cai.org, 2021.                                                 [Sanghikian et al., 2026] Nathalie Sanghikian,          Rafael
[Kotthoff, 2016] Lars Kotthoff. Algorithm selection for              Meirelles, Anand Subramanian, and Rafael Martinelli.
   combinatorial search problems: A survey. In Data Min-             A heuristic algorithm based on beam search and iterated
   ing and Constraint Programming, volume 10101 of LNCS,             local search for the maritime inventory routing problem.
   pages 149–190. Springer, 2016.                                    Comput. Oper. Res., 188:107347, 2026.
[Laborie et al., 2018] Philippe Laborie, Jerome Rogerie,          [Schlenkrich and Parragh, 2022] Manuel Schlenkrich and
   Paul Shaw, and Petr Vilı́m. IBM ILOG CP Optimizer for             Sophie N. Parragh. Solving large scale industrial pro-
   scheduling - 20+ years of scheduling with constraints at          duction scheduling problems with complex constraints: an
   IBM/ILOG. Constraints, 23(2):210–250, 2018.                       overview of the state-of-the-art. In 4th Int’l Conf. on In-
[Lange et al., 2025] Robert Tjarko Lange, Yuki Imajuku,              dustry 4.0 and Smart Manufacturing, Procedia Computer
   and Edoardo Cetin.         Shinkaevolve: Towards open-            Science, pages 1028–1037. Elsevier, 2022.
   ended and sample-efficient program evolution. CoRR,            [Semmelrock and Friedrich, 2025] Veronika Semmelrock
   abs/2509.19349, 2025.                                             and Gerhard Friedrich. Investigating the grounding bot-
[Liu et al., 2024] Fei Liu, Xialiang Tong, Mingxuan Yuan,            tleneck for a large-scale configuration problem: Existing
   Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu              tools and constraint-aware guessing. In 41st Int’l Conf.
   Zhang. Evolution of heuristics: towards efficient au-             on Logic Programming, EPTCS, pages 482–495, January
   tomatic algorithm design using large language model.              2025.
   In 41st Int’l Conf. on Machine Learning, ICML’24.              [Semmelrock et al., 2026] Veronika Semmelrock, Benedetta
   JMLR.org, 2024.                                                   Strizzolo, Francesco Zuccato, Gerhard Friedrich, Patrick
[Liu et al., 2025] Gang Liu, Yihan Zhu, Jie Chen, and Meng           Rodler, and Konstantin Schekotihin. Checkmate project.
   Jiang. Scientific algorithm discovery by augmenting al-           https://git-ainf.aau.at/checkmate/ijcai26, 2026.
   phaevolve with deep research. CoRR, abs/2510.06056,            [Sharma, 2025] Asankhaya Sharma.            Openevolve: an
   2025.                                                             open-source evolutionary coding agent. https://github.
[Lodi and Zarpellon, 2017] Andrea Lodi and Giulia Zarpel-            com/algorithmicsuperintelligence/openevolve, 2025. Ac-
   lon. On learning and branching: a survey. TOP: An Official        cessed: 23 September 2025.
   Journal of the Spanish Society of Statistics and Operations    [Tanese, 1989] Reiko Tanese. Distributed genetic algorithms
   Research, 25(2):207–236, 2017.                                    for function optimization. PhD thesis, University of Michi-
[Mouret and Clune, 2015] Jean-Baptiste Mouret and Jeff               gan, USA, 1989.
   Clune. Illuminating search spaces by mapping elites.           [Tarzariol et al., 2023] Alice Tarzariol, Martin Gebser, Kon-
   CoRR, abs/1504.04909, 2015.                                       stantin Schekotihin, and Mark Law. Learning to break
[Novikov et al., 2025] Alexander Novikov, Ngân Vu, Mar-             symmetries for efficient optimization in answer set pro-
   vin Eisenberger, Emilien Dupont, Po-Sen Huang,                    gramming. In AAAI, pages 6541–6549. AAAI Press, 2023.
   Adam Zsolt Wagner, Sergey Shirobokov, Borislav Ko-             [Taupe et al., 2020] Richard Taupe, Antonius Weinzierl, and
   zlovskii, Francisco J. R. Ruiz, Abbas Mehrabian,                  Gerhard Friedrich. Conflict generalisation in ASP: learn-
   M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George             ing correct and effective non-ground constraints. Theory
   Holland, Alex Davies, Sebastian Nowozin, Pushmeet                 Pract. Log. Program., 20(5):799–814, 2020.
   Kohli, and Matej Balog.           Alphaevolve: A coding        [Wolsey, 2020] Laurence A Wolsey. Integer programming.
   agent for scientific and algorithmic discovery. CoRR,             John Wiley & Sons, 2020.
   abs/2506.13131, 2025.                                          [Yager, 2009] Ronald R. Yager. Prioritized OWA aggrega-
[Perron et al., 2023] Laurent Perron, Frédéric Didier, and         tion. Fuzzy Optim. Decis. Mak., 8(3):245–262, 2009.
   Steven Gay. The CP-SAT-LP solver (invited talk). In            [Yu et al., 2025] Cunxi Yu, Rongjian Liang, Chia-Tung Ho,
   29th Int’l Conf. on Principles and Practice of Constraint
                                                                     and Haoxing Ren. Autonomous code evolution meets np-
   Programming, CP 2023, Toronto, Canada, August 27-31,
                                                                     completeness. CoRR, abs/2509.07367, 2025.
   2023, LIPIcs, pages 3:1–3:2. Schloss Dagstuhl - Leibniz-
   Zentrum für Informatik, 2023.                                 [Zuccato et al., 2025] Francesco Zuccato, Patrick Rodler,
[Romera-Paredes et al., 2024] Bernardino Romera-Paredes,             Gerhard Friedrich, Konstantin Schekotihin, and Richard
                                                                     Comploi-Taupe. Energy-aware double-flexible job shop
   Mohammadamin Barekatain, Alexander Novikov, Matej
                                                                     scheduling with machine modes and setup times: A real-
   Balog, M. Pawan Kumar, Emilien Dupont, Francisco J. R.
                                                                     world industrial case study using constraint programming.
   Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi,
                                                                     In ECAI Workshop on AI-based Planning for Complex
   Pushmeet Kohli, and Alhussein Fawzi. Mathematical dis-
                                                                     Real-World Applications (CAIPI 2025), CEUR Workshop
   coveries from program search with large language models.
                                                                     Proceedings, pages 84–99. CEUR-WS.org, 2025.
   Nature, 625(7995):468–475, 2024.
