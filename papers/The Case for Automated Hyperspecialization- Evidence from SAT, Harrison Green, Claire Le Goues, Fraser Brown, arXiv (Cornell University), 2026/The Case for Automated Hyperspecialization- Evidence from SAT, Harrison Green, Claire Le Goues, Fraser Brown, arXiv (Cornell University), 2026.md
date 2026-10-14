                                                   The Case for Automated Hyperspecialization:
                                                                Evidence from SAT
                                                     Harrison Green                            Claire Le Goues                                                  Fraser Brown
                                                 Carnegie Mellon University                Carnegie Mellon University                              Carnegie Mellon University
                                                    Pittsburgh, PA, USA                       Pittsburgh, PA, USA                                     Pittsburgh, PA, USA
                                                    harrisog@cmu.edu                          clegoues@cmu.edu                                         fraserb@cmu.edu

                                         Abstract                                                          SAT formulas span structurally diverse families
                                         The software status quo is to use one system to process
                                                                                                               cryptography-simon                                            rooks
                                         many different kinds of inputs. In contrast, we propose hy-           71 formulas                                                   30 formulas

                                         perspecialization: creating new software that is optimized
arXiv:2609.14836v1 [cs.SE] 13 Sep 2026




                                                                                                                                                                                          circuit-minimization
                                         for a single class of inputs. Hyperspecializing manually is                                                                                      50 formulas

                                         anywhere from expensive to impossible. We conjecture that
                                         coding agents make automated hyperspecialization cheap, ef-
                                         fective, and safe for problems with measurable performance
                                         and checkable output. This paper explores one such problem,
                                         SAT solving, by synthesizing hundreds of workload-specific
                                         SAT solvers at an average cost of $37 each. Our special-
                                         ists outperform their competition-winning, general-purpose
                                         cousins by 5× on average, and by over 10× on a quarter of
                                         benchmark families. A general-purpose solver constructed
                                         from over a hundred of our prototype hyperspecialists won                                                                                               antibandwidth
                                                                                                                                                                                                 187 formulas
                                         the SAT track at the 2026 SAT Competition.
                                                                                                             hamiltonian
                                                                                                             1.1k formulas                                                           pigeonhole principle
                                                                                                                                                                                     55 formulas

                                         1   Introduction
                                         Different sub-fields of computer science have staged their                                              random-planted-solution
                                                                                                                                                 328 formulas
                                         own rebellions against generality. The architecture [42, 44],
                                                                                                               Industrial (58 families)   Crafted (113 families)   Random (15 families)       Mixed (3 families)
                                         databases [100, 101], networking [11, 21], and operating sys-
                                         tems [30, 31, 73] communities have repeatedly discovered
                                                                                                          Figure 1. Each point represents a SAT formula from 189
                                         that domain-specific software or hardware outperforms its
                                                                                                          benchmark families in this paper, projected using t-SNE over
                                         generalist alternative. “Exterminate all operating system ab-
                                                                                                          56 structural features. Colors indicate broad benchmark ori-
                                         stractions” [30]! The OS should not offer applications founda-
                                                                                                          gin, with shades distinguishing families. Seven family clus-
                                         tional primitives like virtual memory, since doing so requires
                                                                                                          ters are highlighted and labeled.
                                         making decisions about, for example, page table design—
                                         and “any tradeoff penalizes applications that were not an-
                                         ticipated...by the OS designer” [30]. Instead, the OS should
                                         expose almost bare hardware resources, and the application
                                         should use (or avoid) the relevant ones. As a result of the
                                         specialist OS, the application enjoys significant speedups.      those GPUs in the first place [68]. More recently, following
                                            Despite these generality rebellions, not every specialist     a similar cost-benefit analysis, there has been an explosion
                                         has made it from the academic world to reality; Linux has        of interest in (and startups about) custom chips for LLM
                                         not been re-written as a library OS. This is not because the     inference [16, 57, 84].
                                         general- vs. special-purpose performance gap is overstated,         Compared to hardware, custom software can justify a
                                         but because building specialized software and hardware is not    smaller benefit because it’s cheaper to produce—and the cost
                                         free. Specialists get deployed when the performance benefit      is now nosediving towards zero. What once required assem-
                                         of specialization outweighs the cost of specializing.            bling a team of highly paid programmers now requires only
                                            There are domains where the high cost of specialization       a credit card and a horde of Claudes. The Claudes’ results
                                         is worth it [25]. It’s extremely expensive to tape out a new     and the programmers’ results are not necessarily the same,
                                         chip [60]—much more expensive than it is to create new           though; while it’s possible that agents could build specialized
                                         software—yet the performance benefit of GPUs, amortized          operating systems, such a task involves huge codebases, in-
                                         across all graphics problems, justifies the cost of creating     formal specifications, and complex evaluations—and there is
                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


no way to check if the resulting specialist is correct.1 Thus                    formally verified checker can validate independently. Thus,
the animating question of this paper: “are there meaningful                      we need never trust the LLM-generated SAT solver, and need
domains in which (1) specialization improves performance                         only check its results.
and (2) specialization is plausibly automatable?”                                   This paper implements automated hyperspecialization for
   We believe that there may be several such domains (§6),                       SAT. Our first contribution is presenting hyperspecialization,
but this paper presents an existence proof for one: Boolean                      a form of program optimization that synthesizes a fresh pro-
Satisfiability (SAT) solving. A SAT solver takes a formula of                    gram for a given workload, and describing the applications
Boolean variables, their negations, and the operators AND                        for which automated hyperspecialization is tractable (§3).
and OR, and decides whether any assignment of true and                           Such problems must handle diverse workloads (so there’s
false to the variables makes the formula itself true. SAT was                    something to specialize for), have measurable objectives (so
the first problem shown to be NP-complete [24], meaning                          there’s something to optimize towards), and have checkable
that any problem in NP can be efficiently reduced to SAT, and                    results (so there’s no call to trust the LLM author).
that there is no efficient algorithm for solving SAT unless P =                     Our second contribution is a framework for SAT hyper-
NP. Donald Knuth describes SAT as a “killer app” because it                      specialization: we develop specialist SAT solvers for the 189
can be used to solve so many (hard!) important problems [62].                    “families”—i.e., formulas sharing an origin—in the Global
Software verification, circuit equivalence checking, package                     Benchmark Database (GBD) [52], the SAT community’s bench-
dependency resolution, combinatorial math problems, and                          mark corpus built from over twenty years of competition
more all reduce in whole or part to SAT. These domains                           submissions. For each family in the database, we randomly
have not typically created their own SAT solvers. Instead,                       select a training set of instances, and provide this set to a
since SAT is a hard problem, they rely on existing tools that                    coding agent. The agent is prompted to implement (and re-
have implemented sixty years of optimizations, including a                       peatedly evaluate when necessary) a specialized solver from
long tail of tricks that have been sharpened annually since                      scratch for the entire family. Many solvers do not use tradi-
the inaugural 2002 SAT Competition [53]. Rolling your own                        tional SAT algorithms. Instead, they recover structure that
solver was (usually) not worth it.                                               was lost in the encoding, and use a different algorithm to
   We argue that rolling your own solver is now worth it.                        solve the structured problem. For example, one specialist
First, the SAT community already recognizes SAT as a do-                         recognizes a family of rook-placement formulas and proves
main in which specialization improves performance. SAT                           that they’re unsatisfiable: the solver knows about rooks and
problems of different origins have very different structure [4]                  chessboards, so it can say that satisfying the constraints
(Figure 1), and SAT solvers “may dramatically change their                       would require more rooks than the board’s rows fit.
performance depending on the class of...instances they are                          Our third contribution is an evaluation of specialist solvers’
trying to solve” [4]. There are even theoretical differences be-                 performance (§4) that shows the specialists perform better
tween solving strategies. For example, most modern solvers                       than their general-purpose cousins, for low cost. A prototype
use conflict-driven clause learning (CDCL), which can require                    of our hyperspecialization approach won the SAT track at
exponentially large refutations of XOR constraints [107].                        the 2026 SAT Competition. Specialists match or beat the per-
Gauss-Jordan elimination can solve the same constraints in                       family virtual best solver, drawn from four past competition-
polynomial time but cannot solve other kinds of constraints,                     winning solvers, on 64% of families, with a geometric mean
since it only reasons about systems of linear equations [43].                    12× improvement (without checking) and 5× (with check-
Empirically, too, no single solver is best on all workloads:                     ing); specialists are ≥ 100× faster for 27% of families (without
the “virtual best solver” (i.e., an oracle that runs the fastest                 checking) and 14% of families (with checking) (§4.2). A spe-
available solver on a given formula) would outperform the                        cialist costs on average $37 and takes one and a half hours
winning solver in every competition to date.                                     to produce; the fastest arrives in twenty-eight minutes for
   Second, SAT solvers are well-suited to being written by                       $11 and a 1.7× improvement (§4.3).
machines. They have a simple, well-specified interface, are                         Finally, we discuss the implications of SAT hyperspecial-
straightforward to evaluate, and are grounded in a vast public                   ization for downstream consumers, and broader opportuni-
literature that spans algorithms, theory, systems, and formal                    ties for hyperspecialization (§6)—from SMT solving to com-
methods, along with codebases, system descriptions, bench-                       pression to compilation and, perhaps, beyond.
marks, and competition results; the LLMs have been consum-
ing this literature for years. Most importantly, though, SAT
solvers produce a checkable result. A “satisfying assignment”                    2    Related work
to the formula can be (efficiently) checked by plugging it in;                   In this section, we position our work with respect to prior
an “unsatisfiable” answer comes with a proof that a small,                       literature on software synthesis for optimization. We first
                                                                                 discuss approaches that bound the space of candidate pro-
1 In fairness to the machines, all of these facts make OSes hard for people to   grams so that correctness follows by search space construc-
write, too.                                                                      tion (§2.1). We then discuss recent LLM-based approaches,
The Case for Automated Hyperspecialization:
Evidence from SAT

which search a much broader space of program alternatives          execution code per SQL template [66], handling off-nominal
but with relaxed correctness guarantees (§2.2). Finally, we        inputs by falling back to a general-purpose engine.
discuss prior work on SAT optimization in particular (§2.3).          Most LLM-driven optimization work is considerably more
                                                                   constrained (see [70]). One line of work generates an im-
2.1   Optimizing to a reference                                    proved component of a human-written outer algorithm, such
                                                                   as a scoring function, priority rule, or penalty term [69, 81,
Traditional synthesis techniques. Program synthesis writ           94, 116]; another gives the model an existing implementation
large (see [40]) has a multi-decade research lineage. Our          and asks for a faster equivalent [86]. SuperCoder [110] uses
work is closest in spirit to inductive techniques, which syn-      an LLM as a superoptimizer, asking for assembly that runs
thesize programs against partial specifications like input-        faster than a compiled reference while preserving behavior.
output pairs [39, 89]. Oracle-guided variants query an ora-           These searches check success against a provided test suite.
cle that returns counterexamples to constrain the next can-        Tests are only partial correctness specifications, so an agent
didate [3, 54, 55, 98, 106]. Our setting shares the iterative      can satisfy the tests without actually solving the problem.
structure: an agent proposes a candidate, observes how it          Agents exploit evaluation harnesses [65], fail the tests they
performs, and revises.                                             were rewarded for passing [110], and replace complete search
   More closely related is superoptimization, which searches       with approximations that return schema-valid wrong an-
for a fast program equivalent to a given input program, rank-      swers [108].
ing by a cost function. Equivalence is established by proof or        This prior work establishes that LLMs can effectively
by testing depending on the technique. Underlying search           search a large space of implementations heuristically. We
techniques include, e.g., enumeration [75], deductive proof        also use LLMs to search for programs, but limit our search
search over an axiomatized machine [56], or candidate gen-         to applications where it’s easy to check programs’ results
eration checked against an oracle [9]. STOKE [95] takes the        for correctness.
last approach and comes closest to ours in spirit, sampling
whole candidate programs. It treats correctness as a term
in a cost function, with a symbolic validator checking the
candidates that survive. The reference need not be an ex-
isting program; generative libraries search over equivalent        2.3   Optimization for SAT solvers
decompositions [90] or schedules [19, 51, 91] against a fixed      While SAT is an NP-complete problem—and random SAT
mathematical specification.                                        instances are very hard to solve [20]—formulas derived from
Workload specialization. Specializing programs to work-            real-world problems tend to have much faster than average-
loads is longstanding practice across computer science. Ar-        case runtime [5]. Modern SAT solvers can solve instances
chitects design domain-specific processors [25, 42, 44, 57, 68],   with millions of clauses and variables, and the SAT Competi-
while database researchers argue for engines specialized by        tion shows huge performance improvements over the years.
                                                                   The first solver optimizations were two foundational algo-
workload [100, 101].
                                                                   rithms, Davis-Putnam-Logemann-Loveland (DPLL) [26] and
   Automating specialist construction has historically meant
autotuning, searching a space of implementations laid out          conflict-driven clause learning (CDCL) [74, 78]. Improve-
in advance (e.g., for linear algebra kernels [113], or signal      ments since have broadly focused on engineering [13] or
transforms [90]). FFTW [33] defers the search to runtime.          solver heuristics [67]. LLMs are a recent addition to the
   Across these systems, the search or design space is con-        solver optimization literature: both SATLUTION [117] and
                                                                   AE-Kissat-MAB [28], which won the 2025 SAT Competi-
structed to be semantics-preserving, whether via program
                                                                   tion [23], use LLMs to optimize existing solver codebases.
equivalence, specification refinement, or parameterization
of an existing implementation. The tradeoff is that a general         No prior work builds a fresh solver from scratch for every
correctness requirement constrains the search: requiring gen-      workload, but some specialize in a limited way, or manually.
erated SAT solvers to operate correctly on all formulas rules      SATenstein [61], which only solves SAT instances, synthe-
out, for example, solvers that can only solve rook placement       sizes new solvers for a given workload by combining pieces
                                                                   of existing solvers. AutoSAT [103] and AutoModSAT [102]
problems (fast!).
                                                                   use LLMs to optimize for several specific families. They start
                                                                   from a simplified solver codebase, and only allow the LLM to
2.2   Optimizing and synthesizing with LLMs                        modify a maximum of nine heuristics within the CDCL im-
Recent LLM-based optimization approaches relax correct-            plementation. Prior work also manually specializes solvers
ness requirements to search a much larger space of alterna-        to a specific workload (e.g., cryptanalysis [79, 99]), or au-
tives. LLMs have been used to generate whole-system data-          tomatically specializes by tuning parameters [47, 48, 72] or
base implementations customized to a workload. They have           choosing the anticipated best from a portfolio of solvers for
synthesized query engines for a workload contract [109] or         a given instance [58, 59, 114, 115].
                                                                                     Harrison Green, Claire Le Goues, and Fraser Brown


3     Automated hyperspecialization                                3.2   SAT can be hyperspecialized
The software status quo is general-purpose: a single imple-        The task of solving SAT formulas satisfies all of our desider-
mentation processes many different workloads. But these            ata: the workload is heterogeneous, because solvers need to
workloads may favor different algorithms, representations,         solve formulas encoding very diverse problems; faster run-
and heuristics, creating opportunities to take advantage of        time is the obvious objective; and we can efficiently check a
a workload’s particular structure. The goal of automated           SAT solver’s results. We discuss SAT and SAT solvers next,
hyperspecialization is to realize these opportunities by auto-     then expand on each criterion in more detail.
matically synthesizing specialist implementations tailored
to each target workload.                                           3.2.1 SAT. Boolean Satisfiability (SAT) asks whether a for-
   In contrast to optimization, the defining feature of hyper-     mula over Boolean variables and operators ∧, ∨, and ¬ is true
specialization is that it considers workload-specific imple-       under some assignment to the variables. Given the space of
mentations, not general-purpose ones. It synthesizes imple-        inputs X (formulas) and outputs Y (assignments or proofs),
mentations designed to handle, for example, only SAT prob-         a SAT solver (𝜎 : X ⇀ Y ∪ unknown) is a potentially non-
lems generated by the Kani [27] verifier, or only encodings        deterministic procedure which, upon receiving input 𝑥 ∈ X
of register allocation problems. A particular implementation       either produces an output 𝑦 (i.e., a satisfying assignment
need only perform well—or perform at all!—on its target            or UNSAT proof), runs indefinitely, or returns unknown.
workload. Our intuition is that restricting workloads allows       R ⊆ X × Y is the set of correct outputs.
implementations to exploit assumptions about the types of          3.2.2 Heterogeneous workloads in SAT. We use I to
inputs they will encounter. For example, a specialist for regis-   refer to a workload, a finite set of input instances. Our im-
ter allocation instances can assume that the problem is graph      plementation of hyperspecialization specializes by family—a
coloring, and quickly refute with a counting argument.             set of SAT formulas drawn from the same task or generator.
   The next section describes the qualities that make a soft-      Family 𝑘 has representative workload I𝑘 . During hyperspe-
ware task amenable to hyperspecialization (§3.1): if a task        cialization, we split this workload into separate training and
has heterogeneous workloads, measurable objectives, and a          validation splits, denoted I𝑘train and I𝑘val .
checkable result, it can be iteratively and safely hyperspecial-
ized by agents. This paper focuses on hyperspecialization for      3.2.3 Measuring solver performance. We care about
SAT since SAT solvers are critical pieces of software across       SAT solvers being fast. We can measure a particular SAT
a huge range of domains, from mathematics to software              solver’s performance by running it on an input in a fixed
verification to circuit design. We describe why SAT is hyper-      environment with a timeout. Running 𝜎 on input 𝑥 with
specializable (§3.2), including details about workloads, the       timeout 𝑇 yields an output 𝑦 and runtime measurement 𝑡
specific measurable objective, and how to check the correct-                            (𝑦, 𝑡) ∼ Run𝑇 (𝜎, 𝑥)
ness of SAT solver results. Finally, we discuss our realization
of hyperspecialization as a whole-codebase synthesis task,         where 𝑦 ∈ Y ∪unknown is the observed output and 𝑡 ∈ [0,𝑇 ]
where agents iteratively produce and measure a SAT solver          is the (right-censored) observed runtime. Crashes and out-
implementation tailored to a given workload (§3.3).                of-memory (OOM) errors are treated as (unknown,𝑇 ).
                                                                   PAR-2 scores. Following the SAT Competition’s example [34],
                                                                   we convert runtime measurements into a PAR-2 score in or-
3.1    What kind of software can be hyperspecialized?              der to encourage both (1) solving instances faster and (2)
There are three qualities that make a task amenable to auto-       solving more instances correctly within the timeout:
mated hyperspecialization. The task must have:                                                  (
                                                                                                 𝑡   if (𝑥, 𝑦) ∈ R,
                                                                              PAR-2(𝑥, 𝑦, 𝑡) :=
                                                                                                  2𝑇 otherwise.
      1. Heterogeneous workloads: the task should operate
         on more than one type of workload so that there is        A solver’s score on a given input 𝑥 for which it produces 𝑦
         plausibly a benefit from building workload-tailored       in time 𝑡 is 𝑡 if the solver returned a valid solution within
         specialists.                                              the time budget, and twice the timeout otherwise.
      2. Measurable objective(s): it should be possible to            To compute performance of a solver 𝜎 on a workload I,
         compare one implementation to another implemen-           denoted 𝑃 (𝜎, I), we run the solver once on each formula:
         tation for a given measurable property (e.g., speed,
         memory use, etc.).                                                 (𝑦𝑥 , 𝑡𝑥 ) ∼ Run𝑇 (𝜎, 𝑥)     for each 𝑥 ∈ I
      3. Efficiently checkable results: to safely automate         and compute the average PAR-2 score:
         software construction—and, as a result, deploy un-
                                                                                          1 ∑︁
         trusted code—implementations’ results must be check-                𝑃 (𝜎, I) :=       PAR-2(𝑥, 𝑦𝑥 , 𝑡𝑥 )
         able.                                                                           |I|
                                                                                                𝑥∈I
The Case for Automated Hyperspecialization:
Evidence from SAT

3.2.4 Checking solver results. Satisfying assignments                           Edit σ¹                  Edit σ²                  Edit σ³                 …
                                                                   Agent
are conceptually easy to check by plugging in the values
                                                                   1 core                    paused                   paused                 paused
and evaluating the formula. We use the formally verified
gratchk checker in SAT mode [64].                                  Cloud
   Checking UNSAT answers, on the other hand, requires             10 CPUs

augmenting the solver to emit a proof [38, 118]. Our syn-                                  Evaluate σ¹              Evaluate σ²             Evaluate σ³

thesized solvers emit proofs in either DRAT [112], DPR [45],         Agent active         Training (80%)       Validation (20%)

or VeriPB [37] format. We validate these proofs using the
GRAT [64], DPR [104], and VeriPB [15] proof-checking tool-         Figure 2. Our bimodal optimization framework alternates
chains (as described for the SAT Competition 2025), respec-        between (a) using a coding agent to construct and optimize
tively. Each of these toolchains consists of an elaborator         candidate solvers and (b) evaluating these solvers on paral-
which fills in details omitted in the original proof and emits     lelized cloud compute (shown here with 10 CPUs).
an elaborated certificate which is checked by a formally ver-
ified checker.
                                                                   container in “bypass approval” mode using the default Codex
   The choice of proof format and toolchain affects both the
                                                                   harness. We run all agents with broad internet access dis-
reasoning that can be expressed directly and the cost of gen-
                                                                   abled. While web search could be beneficial in some cases,
erating and verifying certificates. For both SAT and UNSAT
                                                                   we found it too difficult to enable web search without po-
results, checking takes polynomial time in the (combined)
                                                                   tentially leaking validation formula data (see §I for more).
size of the formula and the solver’s output.
                                                                   Each agent run is allocated two hours of active time—time
3.3   Agent-based hyperspecialization for SAT                      spent synthesizing and testing code, not external evaluation
                                                                   time—and a maximum of ten external evaluations.
We treat the problem of SAT solver hyperspecialization as a
whole-codebase synthesis task. Given a target workload I𝑘 ,        3.4      When does hyperspecialization pay off?
we task a coding agent (GPT-5.6 Sol in Codex) with produc-
                                                                   Hyperspecialization makes sense when the benefits out-
ing a specialized solver 𝜎𝑘 that minimizes 𝑃 (𝜎𝑘 , I𝑘 ) (smaller
                                                                   weigh the costs. In our agent-based framework (§3.3), hy-
PAR-2 is better). To ensure that agents do not simply memo-
                                                                   perspecialization incurs two costs: money (i.e., LLM token
rize solutions, we provide the agent 80% of the instances as
                                                                   spend) and time (i.e., waiting for the agent to run). The po-
training data I𝑘train , and evaluate performance of submitted
                                                                   tential benefit is that a faster solver will save time in the
solvers on the withheld 20% validation data I𝑘val .                future.
   Agents may submit candidate solvers for evaluation. An             If we synthesize a specialist that is faster than the general-
external evaluation server runs the candidate solver on both       purpose baseline, and run that specialist on sufficiently many
the training and validation splits, but only returns training      instances, we will eventually gain back our upfront special-
results to the agent as feedback. We capture the sequence of       ization time. Running the cost-benefit analysis for monetary
submissions and their respective cumulative costs as a trace:      cost is less straightforward, since it requires assigning mon-
                                                                   etary value to a speedup. How much would you pay for a
                            D                 E𝑛
                      T := (𝜎𝑘(𝑖 ) , 𝐶 (𝑖 ) )
                                              𝑖=1                  2× faster solver for your workload? For some workloads and
Where 𝜎𝑘(𝑖 ) is the 𝑖-th candidate solver and 𝐶 (𝑖 ) is the cu-    companies, the answer is perhaps “a lot!”
mulative cost (in time and money) to produce and evaluate             Our evaluation (§4) analyzes this cost-benefit tradeoff in
                                                                   two regimes. In the time-insensitive regime, specialists are
𝜎𝑘(𝑖 ) .
                                                                   built once and run over an infinite future workload. The
    SAT solver development naturally yields a bimodal work-
                                                                   specialization time is fully amortized, so we only care about
load: the agent spends some time writing, editing, and debug-
                                                                   speedups compared to monetary cost. In the time-sensitive
ging code (low CPU usage, inference-bound, largely sequen-
                                                                   regime, specialists will run over a finite future workload, and
tial) and some time running SAT solver evaluations (high
                                                                   our goal is to minimize the total runtime over that workload:
CPU usage, compute-bound, parallelizable). To use compute
                                                                   is it faster to hyperspecialize or run an off-the-shelf solver?
efficiently, we design our hyperspecialization framework
around this division (Figure 2). We run agents on dedicated        3.4.1 Cost in the time-sensitive regime. To reason about
machines with bounded compute (i.e., a single core and lim-        tradeoffs in the time-sensitive regime, consider a machine
ited memory), and instruct them to submit candidate solvers        whose goal is to solve as many instances as possible, and
to an external evaluation server that runs parallel evaluations    which has compute to devote to either hyperspecialization
in the cloud.                                                      or solving (with a generated specialist or an off-the-shelf
    For all experiments, we use GPT-5.6 Sol [83] in Codex with     general-purpose solver). This machine has 𝐶 identical cores
extra-high reasoning (see §G for details on this choice, and       and an ordered workload W := ⟨𝑥 1, 𝑥 2, . . . , 𝑥 𝑁 ⟩ where all 𝑁
§A for the prompt). The agent runs in an isolated Docker           instances are available at time zero. A deployment policy 𝜋
                                                                                          Harrison Green, Claire Le Goues, and Fraser Brown


specifies which computations to run, when to run them, and        Table 1. Overall winner from the previous four years of the
how to schedule them on the available cores. For example,         SAT Competition, and percentage of time it appears in the
a fixed policy runs the same solver on the next queued in-        VBS.
stance whenever a core becomes available. Other policies
may race multiple solvers or allocate cores to domain-specific            Year     Solver                          Baseline wins
hyperspecialization.
   For each policy, we measure its makespan 𝑀𝜋 (W, 𝐶), the                2023     SBVA-CaDiCaL [41]                         16.9%
elapsed time until all scheduled tasks have terminated, and its           2024     Kissat-sc2024 [14]                        32.0%
verified solve count 𝑄 𝜋 (W, 𝐶), the total number of correct              2025     AE-Kissat-MAB [28]                        30.5%
solutions. Choosing between several policies is inherently                2026     satsuma-iter+kissat3                      20.6%
a multi-objective problem: we want to both minimize the
makespan and maximize the number of solved formulas. The
space of policies, therefore, defines a Pareto frontier, where    4.1.1 Dataset. We draw formula families from the GBD [52],
two policies on this frontier are not directly comparable: one    which consists of2 31,809 CNF formulas split across 189 dif-
is better in one metric and worse in the other.                   ferent families. These formulas have accumulated over 20
   For our evaluation of the time-sensitive regime (§4.3), we     years of SAT competitions, and vary in size from 2 to 9,842
make the simplifying observation that the shape of this prob-     instances.
lem is analogous to that of comparing individual solver per-      4.1.2 Baseline solvers. We compare against the overall
formance. The best solver should run faster and solve more        winner of each of the previous four SAT Competitions (Ta-
formulas within the timeout. Therefore, we lift PAR-2 score       ble 1), which represents each year’s strongest sequential
to the policy level:                                              solver across a range of formulas. To make the comparison
                                                                  stronger, we also report a per-family virtual best solver. For
       𝑃𝜋 (W, 𝐶) = 𝑀𝜋 (W, 𝐶) + 2𝑇 (𝑁 − 𝑄 𝜋 (W, 𝐶))
                                                                  each family 𝑘, we pick the baseline with the lowest training
A policy’s score is the time it took to run (including hyper-     PAR-2 and evaluate that choice on the validation set. Given
specialization time, when applicable) plus a timeout penalty      baselines Σ = {𝜎 (1) , . . . , 𝜎 (𝑛) },
for every instance it failed to solve. We discuss a Pareto                  𝑃 (𝜎 VBS, I𝑘val ) := 𝑃 (argmin 𝑃 (𝜎, I𝑘train ), I𝑘val )
frontier-based treatment of optimality in §C.                                                         𝜎 ∈Σ

                                                                  Across the 189 families in our dataset, each of the four base-
4     Evaluation                                                  line solvers wins (and is thus selected in the VBS) between
We address the following broad research questions:                16.9% and 32.0% of the time (Table 1).
                                                                     §B extends our comparison to recent LLM-based SAT
RQ1: How much does hyperspecialization improve perfor-
                                                                  solver improvement frameworks: AutoSAT [103], Auto-
     mance compared to a general-purpose baseline?
                                                                  ModSAT [102], and SolSearch [96]. We do not compare to
RQ2: When is hyperspecialization economically viable?
                                                                  closed-source SATLUTION [117].
   We deploy domain-specific hyperspecialization at scale:
we create solvers for the 189 families in the GBD across three    4.1.3 Environment. We keep the environment consistent
different proof formats. We evaluate the solvers’ cost and        across all experiments. Solver evaluations use a timeout of
performance relative to a portfolio of four state-of-the-art      600 seconds, a memory budget of 8 GB, and a verifier timeout
general-purpose solvers. Cumulatively, our evaluation con-        of 6,000 seconds. They run in Google Cloud Batch using pre-
sumed approximately $25k worth of LLM tokens (at API              emptable spot instances (n2-highmem-2 with Intel Ice Lake,
pricing) and over 5 CPU-years of solver evaluation. We syn-       to match the SAT Competition 2026 evaluation environment).
thesized over 5,700 unique solvers and ran over 1.8 million       Each task is allocated 1 vCPU and 8 GB RAM, with two tasks
solver invocations.                                               per instance; this is uniform across all solvers. Coding agents
   Next, we describe our evaluation setup (§4.1), and the an-     run on an AMD EPYC 9454P processor with 256 GB of RAM.
swers to RQ1 (§4.2) and RQ2 (§4.3); §5 answers more informal      4.1.4 Task alignment. Agents deployed at scale can score
questions about hyperspecialization.                              well without faithfully solving the task. We refined the task
                                                                  description and environment beforehand using Docent [76]
4.1   Evaluation setup                                            to surface avenues for cheating in pilot runs (§I.2). Afterward,
We describe our dataset (§4.1.1), baseline solvers (§4.1.2),      we audited every agent transcript and generated solver for
the system environment (§4.1.3), and how we ensured task          compliance (§I.3), found seven invalid runs, and reran them;
alignment (§4.1.4); §3.2.4 already described the three proof
formats we use, with one independent agent per proof for-         2 At evaluation time.

mat.                                                              3 Proceedings of SAT Competition 2026 not yet available.
The Case for Automated Hyperspecialization:
Evidence from SAT

a second audit of those seven found no further violations.         many other families on which specialists perform well con-
All results in this paper refer to valid runs.                     tain shuffled variants. When the shuffled instance is removed
                                                                   from the coloring-clique validation set, the specialist out-
4.2   RQ1: How much does hyperspecialization                       performs the baseline (14×, 2× accounting for verification
      improve performance?                                         time).
For every family in the dataset, we select the best special-       Evaluating performance transfer. Specialist performance
ized solver (across all three proof systems) by evaluating         on a family should still transfer to unseen instances drawn
performance on the training set. We compute the baseline-          from the same family. To measure this, we plot the correla-
to-specialist PAR-2 ratio, defined below, on the validation set,   tion between solvers’ PAR-2 scores on the training set and
comparing each specialist with the per-family virtual-best         validation set. Highly correlated scores indicate that special-
of the four baseline solvers. Figure 3 shows this ratio both       ist performance transfers, while higher PAR-2 scores (i.e.,
excluding and including verification time.                         worse performance) on the validation set (vs. the training
PAR-2 ratio. We compare the performance of two solvers             set) imply overfitting to the training set.
𝜎𝑎 and 𝜎𝑏 using the log PAR-2 ratio:                                  Figure 4 shows baseline solver training/validation correla-
                                                                   tion in the left panel (A) as a reference; note that the baseline
                                            𝑃 (𝜎𝑏 , I)             solvers, unlike the specialists, were not actually trained. We
                Δ𝑃 (𝜎𝑎 , 𝜎𝑏 , I) := log10
                                            𝑃 (𝜎𝑎 , I)             plot a point at

We use a ratio because we care about improvements relative                            (𝑃 (𝜎, I𝑘train ), 𝑃 (𝜎, I𝑘val ))
to 𝜎𝑏 ’s score, rather than absolute improvement in PAR-2.         for every baseline solver 𝜎 ∈ Σ and family 𝑘. In the right
The logarithmic scale makes improvements and regressions           panel (B), we plot the performance of every specialized solver
symmetric around zero: a positive value Δ𝑃 > 0 indicates           synthesized throughout all of the agent runs. We plot
that 𝜎𝑎 has a better (smaller) PAR-2 score, and a negative
                                                                                   (𝑃 (𝜎𝑘(𝑖 ) , I𝑘train ), 𝑃 (𝜎𝑘(𝑖 ) , I𝑘val ))
value Δ𝑃 < 0 indicates that 𝜎𝑏 has a better (smaller) PAR-2
score.                                                             for every family 𝑘 and every candidate solver 𝜎𝑘(𝑖 ) produced
Speedups. Agents constructed hyperspecialized solvers that         during domain-specific hyperspecialization for family 𝑘. Train-
yielded significant speedups over the baseline solvers. Ex-        ing and validation PAR-2 were highly rank-correlated both
cluding verification time, specialization produced a faster        for specialists (Spearman 𝜌 = 0.83) and baselines (𝜌 = 0.88).
solver in 121/189 families (64.0%), and produced a solver that        While specialists were more varied in performance than
had more than a 1,000× reduction in PAR-2 score for 32/189         baselines (median absolute deviation of 1.27× vs. 1.16×), they
families (16.9%). The geometric mean ratio was a 12.0× re-         were only slightly more biased towards training performance.
duction in PAR-2 score.                                            The median ratio of validation PAR-2 to training PAR-2 was
   Including verification time in both baseline and specialist     1.01 for specialists (compared to 1.00 for baselines). 6.0% of
scores reduces the geometric mean ratio to 5.03×. The spe-         submissions had a validation/training ratio above 10, com-
cialist still outperforms the baseline on 121/189 families: nine   pared to 4.6% of submissions with validation/training ratio
families gain an advantage and nine lose it. The effect varies     below 0.1. The near-symmetry of these measures suggests
substantially by family. For binary-tree-parity, for exam-         variance within a family as opposed to overfitting.
ple, the ratio remains approximately 323,000×. For purdom-
                                                                   4.3   RQ2: When is hyperspecialization economically
instances, it falls from 917× to 0.278×. In this case, the spe-
                                                                         viable?
cialist found a cheap way to generate an expensive-to-check
proof.                                                             We evaluate specialization in both the time-insensitive regime
                                                                   (§4.3.1) and the time-sensitive regime (§4.3.2).
Failure cases. When agents were not able to discover opti-
mized specialists, their performance still almost always ap-       4.3.1 Time-insensitive regime. We consider the case
proached baseline performance. Specialists had worse than          where a specialized solver will be reused many times—or
a 10× increase in PAR-2 score on only two families. The            infinitely!—making money the driving cost. In Figure 5, we
worst such family is coloring-clique, where the specialist         compare how the improved performance of a candidate spe-
is 104 × worse. The GBD includes one shuffled formula—i.e.,        cialized solver relates to its cumulative construction cost.
an instance with renamed variables and reordered clauses—          For every submission index 𝑖, we plot the average PAR-2
in this family, alongside ten structurally distinct coloring-      validation ratio over the baselines (same as RQ1) and the cu-
clique instances. The shuffled formula was randomly allo-          mulative cost (LLM usage + cloud compute) of the candidate
cated to the validation set with no counterpart in training;       solver 𝜎𝑘(𝑖 ) .
the agent never observed it, and thus could not build a solver        Hyperspecialization potential was predominantly influ-
that accounted for shuffling. Shuffling itself is not the issue:   enced by family, not cumulative specialization effort. On
                                                                                                                                                        Harrison Green, Claire Le Goues, and Fraser Brown


                        Specialists achieve large speedups in a majority of families                                                        Excl. verification   Incl. verification       DPR     VeriPB         GRAT
                                                                                                                                                                                                 binary-tree-parity
                                                                                                                                                                                                      742k× → 323k×
                                       106×


                                       104×
                   PAR-2 ratio




                                                                                 software-verification
                                       102×
                                                                                    0.95× → 1.71×


                                         1×
                                                                                                                                                                                                  rooks
                                                                                                                                                                                                  11.0k× → 7.43×
                                  10−2×                                                                                                                          purdom-instances
                                                   coloring-clique                                                                                                   917× → 0.28×
                                                   7,398× → 1,268× worse
                                  10−4×
                                               1                      25                   50                    75             100                     125                   150                      175             189

                                                                                                                      Families (ranked)




Figure 3. Held-out validation score ratios (baseline / specialist) against the per-family virtual-best of four baseline solvers.
Gray stems and open circles exclude verification; colored markers add verification time to both solvers while retaining PAR-2
penalties. Both solvers are selected using training PAR-2. Families are ranked by the ratio excluding verification; values above
1× favor specialization. Color and marker shape identify the specialist’s proof system. Callouts show speedup excluding →
including verification time.

                                                                                                                               Specialist performance increases with cumulative cost
                        Baselines and specialists generalize to held-out instances
                                                                                                                               PAR-2 ratio on validation set              Proof system          DPR    VeriPB    GRAT
                                        A Baselines                              B Specialists
                                                                                                                                                                                                 Checkpoint means (±1 SD)
                                        Spearman ρ = 0.88 · n = 748              Spearman ρ = 0.83 · n = 4,725

                                 1k                                                                                           10³× better
 Validation PAR-2 (s)




                                                                                                                              10²× better
                                 10
                                                                                                                              10¹× better

                                 0.1
                                                                                                                                    Equal


                  0.001                                                                                                       10¹× worse

                                       0.001        0.1         10         1k   0.001        0.1         10      1k                         $0          $20         $40             $60         $80             $100
                                                                      Training PAR-2 (s)                                                                           Cumulative cost (USD)



Figure 4. Training and validation PAR-2 for baseline solvers                                                                Figure 5. Validation speedup of specialized solvers relative to
(A) and all generated specialists (B), with pooled Spearman                                                                 cumulative construction cost. Each point shows the average
correlations.                                                                                                               performance of the 𝑖th submitted solver across all agent runs
                                                                                                                            (separately for each evaluated proof format).

average, even the agents’ first solver submissions (𝜎𝑘(1) ) were
faster than baselines. The average time to the first submis-                                                                performant solver submissions than with GRAT at a slightly
sion was just 28.1 minutes at a total cost of $10.63, yielding                                                              cheaper average cost. On the other hand, DPR runs were on
a 1.71× improvement over baseline. Full runs (limited to 2                                                                  average more expensive than both GRAT and VeriPB runs
hours of active time and 10 evaluations) took on average 1.5                                                                for unknown reasons.
hours at a cost of $37, yielding a 4.40× improvement.4
   The agent accounted for a majority of the total cost (91.4%),                                                            4.3.2 Time-sensitive regime. When there does not yet
yet a minority of the overall runtime (26.9%). Additionally, we                                                             exist a specialized solver for a particular workload, we must
observed that among the three proof formats, agents had the                                                                 decide whether to attempt hyperspecialization or just run
most success with VeriPB, on average yielding slightly more                                                                 an existing general-purpose solver. Here, there is an explicit
                                                                                                                            tradeoff between the amount of compute and time allocated
4 This includes submissions from all three proof formats (not just the best                                                 for specialization vs. solving. We evaluate eleven different
one) thus is lower than the average speedup in RQ1.                                                                         scenarios.
The Case for Automated Hyperspecialization:
Evidence from SAT

                    Hyperspecialization becomes optimal for most families as workloads grow
                                             C=1                     C=2                          C=4                 C=8                 C=16                         C=32                         C=64
                                    1
                                    2
                                    4
                                    8
   Workload size N (Instances)




                                   16
                                  32
                                  64
                                 128
                                 256
                                 512
                                   1k
                                  2k
                                  5k
                                 10k
                                 20k
                                 40k
                                 80k
                                   …          ···                      ···                          ···                 ···                ···                             ···                       ···
                                  1M
                                        0      50      100 0           50             100 0         50    100 0         50        100 0    50            100 0             50       100 0            50    100
                                                                                                            Share of families won (%)

                                                             Fixed baseline                                          Race                                        Specialization

                                            SBVA '23   Kissat '24     AE-Kissat '25       Satsuma '26             Four-solver race          Wait · DPR            Wait · VeriPB     Wait · GRAT
                                                                                                                                            Hybrid · DPR          Hybrid · VeriPB   Hybrid · GRAT




Figure 6. Share of optimal on-demand policies across simulated workloads. Each horizontal bar specifies a simulated machine
with 𝐶 cores and a workload size of 𝑁 . The bar is colored to represent the share of families for which a given on-demand
                                 ∗
policy 𝜋 was the optimal policy 𝜋𝐶,𝑁    .
                                     ,𝑘


Fixed baseline policy (4 instances). A fixed baseline policy                                                            simulate each policy 𝜋 on each of these representative work-
runs the same solver on the next workload instance when-                                                                loads and compute the optimal policy for family 𝑘 in config-
ever a core is available. We evaluate a fixed policy separately                                                         uration (𝐶, 𝑁 ) as the policy with the lowest total score:
for each of the four baseline solvers.                                                                                                                   𝑟
                                                                                                                                                        ∑︁
Four-solver race policy (1 instance). We evaluate a four-
                                                                                                                                       ∗
                                                                                                                                     𝜋𝐶,𝑁  ,𝑘 := argmin    𝑃𝜋 (W𝑘(𝑖 ) , 𝐶)
                                                                                                                                                         𝜋 ∈Π        𝑖=1
solver race where each of the fixed baselines is deployed in
parallel for a single workload instance whenever four cores                                                               We visualize results in Figure 6. Each horizontal bar de-
are free (which requires 𝐶 ≥ 4). All instances terminate                                                                notes a particular number of cores 𝐶 (x-axis) and a particular
whenever the first solver returns a verified solution.                                                                  workload size 𝑁 (y-axis). The bar is colored based on what
                                                                                                                        share of families a given policy 𝜋 is the optimal policy for the
Specialization policy (6 instances). We evaluate two hy-                                                                configuration (𝐶, 𝑁 ). This visualization allows us to see how
perspecialization deployment policies for each of the three                                                             the distribution of optimal strategies changes as we change
proof formats. In wait, all cores are used for hyperspecializa-                                                         the machine size (𝐶) and the workload size (𝑁 ).
tion. We replay the agent and evaluation compute workload
based on the available parallelism. Once hyperspecializa-                                                               Results. For small workloads, running fixed baseline solvers
tion completes, the best checkpoint is served on all cores.                                                             directly is most frequently the optimal strategy as these
In hybrid, hyperspecialization runs until the first solver                                                              solvers incur no upfront cost. In regimes where the work-
is submitted. Then, half the cores immediately serve that                                                               load undersaturates the available compute (i.e. 𝑁 < 𝐶), the
solver, while the remaining cores continue hyperspecializa-                                                             four-solver race is frequently dominant, as it provides a mech-
tion. When a new, better solver is produced, the serving                                                                anism to use this “free” compute.
cores switch to it. Once specialization completes, all cores                                                               Across all machine sizes, as the workload size increases,
serve the best solver.                                                                                                  hyperspecialization increases in viability. On average, GRAT
   We performed a discrete-event simulation of each of these                                                            specialists fare better than both VeriPB and DPR. Within
runtime policies. For every core count 𝐶 ∈ {1, 2, 4, 8, 16, 32, 64},                                                    each format, the hybrid form of the strategy (where available
workload size 𝑁 ∈ {1, 2, 4, . . . , 80 𝑘, 1 𝑀 }, and family 𝑘, we                                                       specialists are immediately deployed) is optimal on more
sample 𝑟 random workloads of size 𝑁 (with replacement)                                                                  families than the wait form. Once the workload size exceeds
from the validation set I𝑘val , producing W𝑘(1) , . . . , W𝑘(𝑟 ) . We                                                   𝑁 = 2, 000, some form of hyperspecialization is the optimal
                                                                                                                        strategy on a majority of families across all machine sizes.

                                                                                                                        5       Case studies
                                                                                                                        This section describes four case studies: classifying the strate-
                                                                                                                        gies used by generated solvers, deploying specialists in real
                                                                                                     Harrison Green, Claire Le Goues, and Fraser Brown


systems that use solvers, measuring how specialists for one        Case-study performance                                               Without verification   With verification

                                                                   Train / Val.: isolated formulas   Original / New: native workflows
family perform on another, and exploring how sensitive spe-
                                                                                                       Train
cialists are to cardinality encodings (described later).                                                Val.
                                                                   OpenTitan
                                                                                                     Original
5.1   Solver taxonomy                                                                                   New
                                                                                                        Train
                                                                                                         Val.
We surveyed the entire set of 567 training-selected special-       ORFS
                                                                                                     Original
ists across the 189 families, using LLM-based techniques to                                             New
analyze and classify the nearly 500,000 lines of generated                                              Train
                                                                                                         Val.
solver code. This section gives broad insights into specialists’   CBMC
                                                                                                     Original
strategies, while §K describes our method and its limitations;                                          New
                                                                                                        Train
in §J, we provide concise, LLM-generated descriptions of                                                 Val.
                                                                   Kani
every family and solver.                                                                             Original
                                                                                                        New
Results. Specialists did not compete with generalists by                                                Train
                                                                                                         Val.
developing new algorithms; rather, they sampled from the                                             Original
                                                                   Conda           (pycosat)
vast SAT and algorithms literature to solve the problem at                                              New

hand, and implemented their solutions with systems-level                                             Original
                                                                                   (libmamba)
                                                                                                        New
optimizations.                                                                                                      0.1×          1×            10×                     100×
   Generated solvers were remarkably varied and family-                                      Baseline / specialist ratio (>1 favors specialist)

specific. Our audit found at least forty unique solver strate-
gies: CDCL, the backbone of almost all modern solvers, was         Figure 7. Specialists’ redeployment performance across five
the second most common strategy (57.5%), after constructing        real-world systems. Formulas were extracted from a target
witnesses or deriving proofs directly from problem structure       and used to develop a specialist; Train/Val. show specialist
(60.7%). Only 16.2% of solvers deployed CDCL on its own,           speedup over baselines in isolation on these representative
and 81.1% of solvers used more than one strategy (Figure 13).      formulas. We then redeploy the specialist in the real-world
   Specialists frequently recovered high-level structure from      system and measure end-to-end performance compared to
input formulas (Figure 14)—for example, graphs (41.3%), Bool-      the native tool on the original target for which formulas were
ean circuits (38.6%), and cardinality constraints (27.9%)—and      extracted (original) and a new target (new). For Conda, we
97.2% of specialists included some check excluding formulas        evaluate two different native modes: pycosat and libmamba.
that did not fit the expected structure (Figure 16). Recov-
ered structure also informed orchestration for multi-strategy
solvers: 93.3% of solvers selected solving procedures based
on structure, and 60.1% ran distinct methods sequentially          even when accounting for proof verification time—something
(Figure 18).                                                       native solutions did not even attempt.
   Specialists used a wide range of known heuristics and              Deploying specialists was challenging for several non-
techniques (e.g., XOR reasoning). They also optimized be-          obvious reasons, though: (1) real-world systems often implic-
yond just algorithmic and search speedups, using an array          itly trust solvers and run them without proof-logging, while
of low-level systems techniques like memory preallocation          our specialists always spend time producing proofs; (2) some
(96.5%), specialized parsing (66.0%), buffered proof logging       systems (e.g., CBMC and Kani) optimize by running native
(45.1%), going so far as to add branch-prediction hints (1.1%)     solvers in incremental mode, a mode our specialists do not
and SIMD-accelerated code (1.8%) (Figure 19).                      yet (but could!) support; (3) some systems (e.g., Conda) use
                                                                   custom, higher-level (and thus faster) solvers as alternatives
5.2   End-to-end deployment                                        to SAT. One potential direction for future work is synthesiz-
We ask whether applying hyperspecialization to real-world          ing solvers for a given family and a given application (e.g., a
systems results in solvers competitive with native perfor-         verification-specific, incremental solver for Kani).
mance. We isolated SAT formulas from five real systems,
synthesized a specialist, and then evaluated the specialist in     5.3      Cross-family sensitivity and performance
a simulated deployment on new targets. Figure 7 presents           §4.2 measures solvers only on their target validation set.
the results compared to native baselines for circuit equiva-       Here, we run the top per-family selected specialist on the
lence checking (OpenTitan [85] and ORFS [105]), verification       validation set of every other family (Figure 20).
(CBMC [22] and Kani [27]), and package dependency resolu-          Results. Most specialists were very selective, refusing to
tion (Conda [93]); see §E for details.                             run (i.e. quickly returning UNKNOWN) on families outside of
Results. For two of our five systems (OpenTitan and ORFS),         the target domain: only 27 solvers attempted to run on more
specialists outperformed native solutions on novel targets         than 50% of other families. Targeted specialists were also
The Case for Automated Hyperspecialization:
Evidence from SAT

often the best solver for their family: in 134 of the 189 cases                How cardinality encoding affects performance
                                                                               Validation PAR-2 (s)       SBVA '23   Kissat '24   AE-Kissat '25   Satsuma '26    Specialist
(70.9%), the targeted specialist won its own family.
                                                                                        GPHP                     LDPC decoding                    Vertex cover
   Specialists were also robust. Only seven source/target com-                  1.2k
                                                                                                  1/20
binations resulted in solutions rejected by the verifier. Six re-                       17/20            3/20
                                                                                  10
jections (all on multiplier-verification) were false posi-
tives, caused by a bug in the DPR elaborator dpr-trim5 that                       0.1

mishandled clauses with repeated literals. We have reported                    0.001
this bug with a patch. Only one rejection was legitimate. The




                                                                                        KM ot
                                                                                               t




                                                                                                                KM t
                                                                                                                       t




                                                                                                                                                         t

                                                                                                                                                         t
                                                                                            ive
                                                                                             q.

                                                                                         Ca .
                                                                                            rd.

                                                                                         M- .




                                                                                                                     q.
                                                                                                                     rt.
                                                                                                                    rd.

                                                                                                                      t.




                                                                                                                                                       q.

                                                                                                                                                      rd.

                                                                                                                                                        t.
                                                                                             rt


                                                                                              t

                                                                                           -To




                                                                                                                    To
                                                                                                                   -To




                                                                                                                                                      To

                                                                                                                                                     -To
                                                                                           To




                                                                                                                   To




                                                                                                                                                     To
fpga-routing solver read clause lines into a fixed 64 KiB




                                                                                            T
                                                                                          Se




                                                                                                                  Se




                                                                                                                                                    Se
                                                                                          So




                                                                                                                  So
                                                                                                                 Ca




                                                                                                                                                   Ca
                                                                                         Na




                                                                                                                 M-




                                                                                                                                                   M-
                                                                                                                                                  KM
buffer with fgets. It correctly preserved unfinished clauses
across multiple reads, but not unfinished literals: it dropped                Figure 8. Average validation PAR-2 of baselines and special-
minus signs that fell at a buffer boundary, converting nega-                  ists for various cardinality encodings.
tive literals into positive ones. Triggering this bug required a
clause line exceeding 64 KiB with a negative literal precisely
at the boundary.                                                              Hyperspecialization and SAT. Hyperspecialization (we
                                                                              hope!) makes it easier for SAT research to have practical
5.4    Cardinality constraint encodings                                       impact. In the past, a technique benefiting a small set of
                                                                              formulas was difficult to justify maintaining in a mainline
Many high-level problems define cardinality constraints,                      solver. Now, if the technique is useful for a specific workload,
or bounds related to counting (e.g., “exactly two of these                    an agent can discover and implement it in a specialist.
variables must be true”). These constraints can be encoded                       Hyperspecialization may also open up new research av-
into Boolean logic in a variety of ways. For general-purpose                  enues. For example, a CDCL solver’s reasoning maps cleanly
solvers, the specific choice of encoding is an active area of                 to DRAT proofs; it doesn’t need the richness of formats like
research [6–8, 10, 32, 77, 82, 92, 97], because it plays a signif-            VeriPB. Specialist solvers can take advantage of more expres-
icant role in solve time. Fewer clauses and/or variables, for                 sive reasoning, though—so the bottleneck becomes proof
example, often correlate with faster solve times. Here, we                    verification time. Can we design formats that speed up veri-
test if the same is true under hyperspecialization. We evalu-                 fication with specialist-authored hints? What does a proof
ated baseline and specialist performance across three crafted                 format designed for hyperspecialists look like?
benchmarks—chosen because they used many cardinality                             Finally, we may consider the SAT solver within the context
constraints and covered both SAT and UNSAT—and up to                          of the embedding application. §5.2 describes how synthe-
seven cardinality encoding methods; see §H for more.                          sizing a specialist from workload examples alone may not
Results. Figure 8 shows the performance of baselines and                      be enough to beat native speeds. The synthesis step could
specialists.6 Unlike general-purpose solvers,7 specialists do                 improve performance by accounting for information about
not benefit from more compact encodings; in fact, for one of                  the embedding application.
the benchmarks, the naive (pairwise) cardinality encoding                     Hyperspecialization beyond SAT. The most obvious hy-
yielded the fastest specialist (yet the worst baseline perfor-                perspecialization domains beyond SAT are its close rela-
mance). We hypothesize that it is more important for a for-                   tives that also support verification: SMT [29], MaxSAT [12],
mula to be encoded in a conceptually clear way for the hyper-                 pseudo-Boolean optimization [63], finite-domain constraint
specialist, as opposed to a compact—but perhaps convoluted—                   solving [36], QBF [80], certified model counting [17], and
way. Compactness helps general-purpose solvers because it                     more. Hyperspecialization should work more generally, though:
plays nicely with those solvers’ fixed internal heuristics. In                we claim that it applies to any problem with a given shape
contrast, the specialist chooses its own internal heuristics—in               (§3.1). We now provide three possibilities in rough order of
many cases extracting and reasoning about cardinality con-                    audacity.
straints at a high level. An optimized encoding can stymie the                   A lossless compressor sees many types of inputs (e.g.,
specialist who’s trying to reconstruct a higher-level problem.                text or audio), and produces a small archive that decom-
                                                                              presses back to the original. There already exist special-
6     Discussion                                                              ized compressors that use domain knowledge to achieve
This section considers the ramifications of hyperspecializa-                  better compression ratios than general-purpose compres-
tion for SAT and beyond.                                                      sors [2, 18, 46, 87, 111]. Automated hyperspecialization may
                                                                              allow us to tailor compressors to other workloads—or even
5 The elaborator runs before the formally verified part of the checker.
                                                                              individual inputs! The correctness check is simply decom-
6 All using GRAT, so specialists must construct resolution-based proofs and   pressing the output and comparing the result with the input.
cannot simply map the cardinality constraints into algebraic proofs.             Compilers compile many types of programs, and under-
7 The general-purpose encoding benefit is more visible in §H.                 standing program semantics often improves performance
                                                                                                        Harrison Green, Claire Le Goues, and Fraser Brown


of the generated binary. Could we build hyperspecialized                            [7] Roberto Asín, Robert Nieuwenhuis, Albert Oliveras, and Enric
compilers for certain classes of programs, using transla-                               Rodríguez-Carbonell. 2011. Cardinality networks: a theoretical
tion validation [71, 88] to check output? What about web                                and empirical study. Constraints 16, 2 (2011), 195–221. https:
                                                                                        //doi.org/10.1007/s10601-010-9105-0
browsers? They serve many different web pages, and today,                           [8] Olivier Bailleux and Yacine Boufkhad. 2003. Efficient CNF Encoding
behemoth applications wring new drips of performance out                                of Boolean Cardinality Constraints. In Principles and Practice of Con-
of JavaScript engines and renderers with each new release.                              straint Programming – CP 2003 (Lecture Notes in Computer Science,
What would per-workload browsers look like, and how might                               Vol. 2833), Francesca Rossi (Ed.). Springer Berlin Heidelberg, Berlin,
we check them? More broadly, in a world where untrusted                                 Heidelberg, 108–122. https://doi.org/10.1007/978-3-540-45193-8_8
                                                                                    [9] Sorav Bansal and Alex Aiken. 2006. Automatic generation of peephole
authors can specialize (or “specialize”) anything, how might                            superoptimizers. ACM SIGOPS Operating Systems Review 40, 5 (Oct.
we re-imagine checking?                                                                 2006), 394–403. https://doi.org/10.1145/1168917.1168906
                                                                                   [10] Kenneth E. Batcher. 1968. Sorting networks and their applications.
                                                                                        In Proceedings of the April 30–May 2, 1968, spring joint computer
Generative AI disclosure                                                                conference. Association for Computing Machinery, New York, New
We used generative AI to assist with various aspects of this                            York, USA, 307–314. https://doi.org/10.1145/1468075.1468121
research. We used coding agents (primarily GPT-5.6 Sol in                          [11] Adam Belay, George Prekas, Ana Klimovic, Samuel Grossman, Chris-
Codex, but also other models in Cursor and Claude Code) to                              tos Kozyrakis, and Edouard Bugnion. 2014. IX: A Protected Data-
                                                                                        plane Operating System for High Throughput and Low Latency. In
help with the development of the SAT hyperspecialization                                11th USENIX Symposium on Operating Systems Design and Imple-
framework, evaluation pipelines, and case studies. Our core                             mentation (OSDI 14). USENIX Association, Broomfield, CO, USA, 49–
experiment tests how well coding agents can synthesize                                  65. https://www.usenix.org/conference/osdi14/technical-sessions/
SAT solvers and thus naturally uses generative AI. During                               presentation/belay
evaluation, we used LLMs (GPT-6 Astra and GPT-5.6 Luna)                            [12] Jeremias Berg, Bart Bogaerts, Jakob Nordström, Andy Oertel, and
                                                                                        Dieter Vandesande. 2023. Certified Core-Guided MaxSAT Solving. In
to build taxonomies of solver behavior (detailed in §K). In                             Automated Deduction – CADE 29 (Lecture Notes in Computer Science,
the preparation of this manuscript, we used coding agents                               Vol. 14132). Springer, 1–22. https://doi.org/10.1007/978-3-031-38499-
(GPT-5.6 Sol / GPT-6 Astra) to help create graphs and figures.                          8_1
Except for three clearly labeled sections in the appendix (§J,                     [13] Armin Biere, Tobias Faller, Katalin Fazekas, Mathias Fleury, Nils
§K.3, and §E.1), the words in this paper were written by                                Froleyks, and Florian Pollitt. 2024. CaDiCaL 2.0. In Computer
                                                                                        Aided Verification (Lecture Notes in Computer Science, Vol. 14681),
humans.                                                                                 Arie Gurfinkel and Vijay Ganesh (Eds.). Springer, Cham, 133–152.
                                                                                        https://doi.org/10.1007/978-3-031-65627-9_7
References                                                                         [14] Armin Biere, Tobias Faller, Katalin Fazekas, Mathias Fleury, Nils
                                                                                        Froleyks, and Florian Pollitt. 2024. CaDiCaL, Gimsatul, IsaSAT and
  [1] Ignasi Abío, Robert Nieuwenhuis, Albert Oliveras, and Enric                       Kissat Entering the SAT Competition 2024. In Proceedings of SAT
      Rodríguez-Carbonell. 2013. A Parametric Approach for Smaller and                  Competition 2024: Solver, Benchmark and Proof Checker Descriptions
      Better Encodings of Cardinality Constraints. In Principles and Prac-              (Department of Computer Science Report Series B, Vol. B-2024-1), Marijn
      tice of Constraint Programming (Lecture Notes in Computer Science,                J. H. Heule, Markus Iser, Matti Järvisalo, and Martin Suda (Eds.).
      Vol. 8124), Christian Schulte (Ed.). Springer Berlin Heidelberg, Berlin,          Department of Computer Science, University of Helsinki, Helsinki,
      Heidelberg, 80–96. https://doi.org/10.1007/978-3-642-40627-0_9                    Finland, 8–10. https://hdl.handle.net/10138/584822
  [2] Azim Afroozeh, Leonardo X. Kuffo, and Peter Boncz. 2023. ALP:                [15] Bart Bogaerts, Ciaran McCreesh, Magnus O. Myreen, Jakob Nord-
      Adaptive Lossless Floating-Point Compression. Proceedings of the
                                                                                        ström, Andy Oertel, and Yong Kiam Tan. 2023. VeriPB and CakePB
      ACM on Management of Data 1, 4, Article 230 (2023), 26 pages. https:              in the SAT Competition 2023. In Proceedings of SAT Competition
      //doi.org/10.1145/3626717                                                         2023: Solver, Benchmark and Proof Checker Descriptions (Department
  [3] Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo M. K. Martin,                  of Computer Science Series of Publications B, Vol. B-2023-1). University
      Mukund Raghothaman, Sanjit A. Seshia, Rishabh Singh, Armando                      of Helsinki, Helsinki, Finland, 86–88. https://hdl.handle.net/10138/
      Solar-Lezama, Emina Torlak, and Abhishek Udupa. 2013. Syntax-                     563824
      guided synthesis. In 2013 Formal Methods in Computer-Aided Design.           [16] Russell Brandom. 2026.          OpenAI’s Jalapeño Chip Is Built
      IEEE, Piscataway, NJ, USA, 1–8. https://doi.org/10.1109/fmcad.2013.               for Fast Inference at Scale, Benchmarks Show. TechCrunch.
      6679385                                                                           https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-
  [4] Carlos Ansótegui, Maria Luisa Bonet, Jesús Giráldez-Cru, and Jordi                for-fast-inference-at-scale-benchmarks-show/
      Levy. 2017. Structure features for SAT instances classification. Journal     [17] Randal E. Bryant, Wojciech Nawrocki, Jeremy Avigad, and Mar-
      of Applied Logic 23 (2017), 27–39. https://doi.org/10.1016/j.jal.2016.            ijn J. H. Heule. 2023. Certified Knowledge Compilation with Ap-
      11.004                                                                            plication to Verified Model Counting. In 26th International Confer-
  [5] Carlos Ansótegui, Maria Luisa Bonet, Jesús Giráldez-Cru, Jordi Levy,              ence on Theory and Applications of Satisfiability Testing (SAT 2023)
      and Laurent Simon. 2019. Community structure in industrial SAT                    (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 271).
      instances. Journal of Artificial Intelligence Research 66 (2019), 443–472.        Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 6:1–6:20. https:
      https://doi.org/10.1613/jair.1.11741                                              //doi.org/10.4230/LIPIcs.SAT.2023.6
  [6] Roberto Asín, Robert Nieuwenhuis, Albert Oliveras, and Enric                 [18] Shubham Chandak, Kedar Tatwawadi, Idoia Ochoa, Mikel Hernaez,
      Rodríguez-Carbonell. 2009. Cardinality networks and their applica-                and Tsachy Weissman. 2019. SPRING: A Next-Generation Com-
      tions. In Theory and Applications of Satisfiability Testing - SAT 2009            pressor for FASTQ Data. Bioinformatics 35, 15 (2019), 2674–2676.
      (Lecture Notes in Computer Science, Vol. 5584). Springer Berlin Hei-              https://doi.org/10.1093/bioinformatics/bty1015
      delberg, Berlin, Heidelberg, 167–180. https://doi.org/10.1007/978-3-
      642-02777-2_18
The Case for Automated Hyperspecialization:
Evidence from SAT

 [19] Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie         [33] M. Frigo and S. G. Johnson. 2005. The Design and Implementation
      Yan, Meghan Cowan, Haichen Shen, Leyuan Wang, Yuwei Hu, Luis                 of FFTW3. Proc. IEEE 93, 2 (2005), 216–231. https://doi.org/10.1109/
      Ceze, Carlos Guestrin, and Arvind Krishnamurthy. 2018. TVM: An               jproc.2004.840301
      Automated End-to-End Optimizing Compiler for Deep Learning. In          [34] Nils Froleyks, Marijn Heule, Ashlin Iser, Matti Järvisalo, and Martin
      13th USENIX Symposium on Operating Systems Design and Implemen-              Suda. 2021. SAT Competition 2020. Artificial Intelligence 301 (2021),
      tation (OSDI 18) (Carlsbad, CA, USA) (OSDI’18). USENIX Association,          103572. https://doi.org/10.1016/j.artint.2021.103572
      Carlsbad, CA, USA, 579–594. https://www.usenix.org/conference/          [35] Robert Gallager. 1962. Low-density parity-check codes. IRE Trans-
      osdi18/presentation/chen                                                     actions on Information Theory 8, 1 (1962), 21–28. https://doi.org/10.
 [20] Vašek Chvátal and Endre Szemerédi. 1988. Many hard examples for              1109/tit.1962.1057683
      resolution. J. ACM 35, 4 (1988), 759–768. https://doi.org/10.1145/      [36] Stephan Gocht, Ciaran McCreesh, and Jakob Nordström. 2022. An
      48014.48016                                                                  Auditable Constraint Programming Solver. In 28th International Con-
 [21] David D. Clark and David L. Tennenhouse. 1990. Architectural Con-            ference on Principles and Practice of Constraint Programming (CP 2022)
      siderations for a New Generation of Protocols. In Proceedings of the         (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 235).
      ACM Symposium on Communications Architectures and Protocols. As-             Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 25:1–25:18.
      sociation for Computing Machinery, New York, NY, USA, 200–208.               https://doi.org/10.4230/LIPIcs.CP.2022.25
      https://doi.org/10.1145/99508.99553                                     [37] Stephan Gocht and Jakob Nordström. 2021. Certifying Parity Rea-
 [22] Edmund Clarke, Daniel Kroening, and Flavio Lerda. 2004. A Tool               soning Efficiently Using Pseudo-Boolean Proofs. Proceedings of the
      for Checking ANSI-C Programs. In Tools and Algorithms for the                AAAI Conference on Artificial Intelligence 35, 5 (2021), 3768–3777.
      Construction and Analysis of Systems (Lecture Notes in Computer              https://doi.org/10.1609/aaai.v35i5.16494
      Science, Vol. 2988). Springer, Berlin, Heidelberg, 168–176. https:      [38] Evgueni Goldberg and Yakov Novikov. 2003. Verification of proofs
      //doi.org/10.1007/978-3-540-24730-2_15                                       of unsatisfiability for CNF formulas. In 2003 Design, Automation and
 [23] Cayden Codel, Katalin Fazekas, Marijn J. H. Heule, and Markus Iser.          Test in Europe Conference and Exhibition. IEEE Computer Society,
      2025. The Results of SAT Competition 2025. SAT 2025 conference pre-          Los Alamitos, CA, USA, 886–891. https://doi.org/10.1109/date.2003.
      sentation. https://satcompetition.github.io/2025/satcomp25slides.            1253718
      pdf                                                                     [39] Sumit Gulwani. 2011. Automating string processing in spreadsheets
 [24] Stephen A. Cook. 1971. The complexity of theorem-proving pro-                using input-output examples. ACM SIGPLAN Notices 46, 1 (2011),
      cedures. In Proceedings of the Third Annual ACM Symposium on                 317–330. https://doi.org/10.1145/1925844.1926423
      Theory of Computing (Shaker Heights, Ohio, USA) (STOC ’71). As-         [40] Sumit Gulwani, Oleksandr Polozov, and Rishabh Singh. 2017. Pro-
      sociation for Computing Machinery, New York, NY, USA, 151–158.               gram synthesis. Foundations and Trends in Programming Languages
      https://doi.org/10.1145/800157.805047                                        4, 1–2 (2017), 1–119. https://doi.org/10.1561/2500000010
 [25] William J. Dally, Yatish Turakhia, and Song Han. 2020. Domain-          [41] Andrew Haberlandt and Harrison Green. 2023. SBVA-CaDiCaL and
      specific hardware accelerators. Commun. ACM 63, 7 (2020), 48–57.             SBVA-Kissat: Structured Bounded Variable Addition. In Proceedings
      https://doi.org/10.1145/3361682                                              of SAT Competition 2023: Solver, Benchmark and Proof Checker Descrip-
 [26] Martin Davis, George Logemann, and Donald Loveland. 1962. A                  tions (Department of Computer Science Series of Publications B, Vol. B-
      machine program for theorem-proving. Commun. ACM 5, 7 (July                  2023-1). Department of Computer Science, University of Helsinki,
      1962), 394–397. https://doi.org/10.1145/368273.368557                        Helsinki, Finland, 18. https://hdl.handle.net/10138/563824
 [27] Rémi Delmas, Zyad Hassan, Qinheping Hu, Rahul Kumar, Felipe R.          [42] Rehan Hameed, Wajahat Qadeer, Megan Wachs, Omid Azizi, Alex
      Monteiro, Thanh Nguyen, Adrián Palacios, Celina Val, Michael                 Solomatnikov, Benjamin C. Lee, Stephen Richardson, Christos
      Tautschnig, Justus Adam, Daniel Schwartz-Narbonne, and Carolyn               Kozyrakis, and Mark Horowitz. 2010. Understanding sources of
      Zech. 2026. Kani: A Model Checker for Rust. arXiv:2607.01504 [cs.SE]         inefficiency in general-purpose chips. In Proceedings of the 37th
      https://arxiv.org/abs/2607.01504                                             annual international symposium on Computer architecture. Associa-
 [28] Hang Ding, Mao Luo, Chu-Min Li, Shunwei Li, Runyao Chen, Cai-                tion for Computing Machinery, New York, NY, USA, 37–47. https:
      quan Xiong, and Xinyun Wu. 2025. A Self-Optimizing Framework                 //doi.org/10.1145/1815961.1815968
      for SAT Solvers via Population Evolution and Large Language Model       [43] Cheng-Shen Han and Jie-Hong Roland Jiang. 2012. When Boolean
      Collaboration. In Proceedings of SAT Competition 2025: Solver and            satisfiability meets Gaussian elimination in a simplex way. In Com-
      Benchmark Descriptions (Proceedings of SAT Competitions), Cayden             puter Aided Verification (Lecture Notes in Computer Science, Vol. 7358).
      Codel, Katalin Fazekas, Marijn J. H. Heule, and Markus Iser (Eds.).          Springer Berlin Heidelberg, Berlin, Heidelberg, 410–426. https:
      TU Wien, Vienna, Austria, 15–17. https://doi.org/10.34726/10379              //doi.org/10.1007/978-3-642-31424-7_31
 [29] Burak Ekici, Alain Mebsout, Cesare Tinelli, Chantal Keller, Guy Katz,   [44] John L. Hennessy and David A. Patterson. 2019. A new golden
      Andrew Reynolds, and Clark Barrett. 2017. SMTCoq: A Plug-In for              age for computer architecture. Commun. ACM 62, 2 (2019), 48–60.
      Integrating SMT Solvers into Coq. In Computer Aided Verification             https://doi.org/10.1145/3282307
      (CAV 2017), Part II (Lecture Notes in Computer Science, Vol. 10427).    [45] Marijn J. H. Heule, Benjamin Kiesl, and Armin Biere. 2020. Strong
      Springer, 126–133. https://doi.org/10.1007/978-3-319-63390-9_7               Extension-Free Proof Systems. Journal of Automated Reasoning 64, 3
 [30] Dawson R. Engler and M. Frans Kaashoek. 1995. Exterminate all                (2020), 533–554. https://doi.org/10.1007/s10817-019-09516-0
      operating system abstractions. In Proceedings 5th Workshop on Hot       [46] Daniel Reiter Horn, Ken Elkabany, Chris Lesniewski-Laas, and Keith
      Topics in Operating Systems (HotOS-V). IEEE Computer Society, Los            Winstein. 2017. The Design, Implementation, and Deployment of a
      Alamitos, CA, USA, 78–83. https://doi.org/10.1109/hotos.1995.513459          System to Transparently Compress Hundreds of Petabytes of Image
 [31] Dawson R. Engler, M. Frans Kaashoek, and James O’Toole, Jr. 1995.            Files for a File-Storage Service. In 14th USENIX Symposium on Net-
      Exokernel: An operating system architecture for application-level            worked Systems Design and Implementation (NSDI 2017). USENIX
      resource management. ACM SIGOPS Operating Systems Review 29, 5               Association, Boston, MA, USA, 1–15. https://www.usenix.org/
      (1995), 251–266. https://doi.org/10.1145/224057.224076                       conference/nsdi17/technical-sessions/presentation/horn
 [32] Niklas Eén and Niklas Sörensson. 2006. Translating Pseudo-Boolean
      Constraints into SAT. Journal on Satisfiability, Boolean Modeling and
      Computation 2, 1–4 (2006), 1–26. https://doi.org/10.3233/sat190014
                                                                                                        Harrison Green, Claire Le Goues, and Fraser Brown


[47] Frank Hutter, Holger H. Hoos, and Kevin Leyton-Brown. 2011. Se-                    Richard Walter, Walter Wang, Eric Wilcox, and Doe Hyun Yoon. 2017.
     quential Model-Based Optimization for General Algorithm Configu-                   In-datacenter performance analysis of a tensor processing unit. In
     ration. In Learning and Intelligent Optimization (Lecture Notes in Com-            Proceedings of the 44th annual international symposium on computer
     puter Science, Vol. 6683), Carlos A. Coello Coello (Ed.). Springer, Berlin,        architecture. Association for Computing Machinery, New York, NY,
     Heidelberg, 507–523. https://doi.org/10.1007/978-3-642-25566-3_40                  USA, 1–12. https://doi.org/10.1145/3079856.3080246
[48] Frank Hutter, Holger H. Hoos, Kevin Leyton-Brown, and Thomas                  [58] Serdar Kadioglu, Yuri Malitsky, Ashish Sabharwal, Horst Samulowitz,
     Stützle. 2009. ParamILS: an Automatic Algorithm Configuration                      and Meinolf Sellmann. 2011. Algorithm Selection and Scheduling. In
     Framework. Journal of Artificial Intelligence Research 36 (2009), 267–             Principles and Practice of Constraint Programming – CP 2011 (Lecture
     306. https://doi.org/10.1613/jair.2861                                             Notes in Computer Science, Vol. 6876), Jimmy Lee (Ed.). Springer Berlin
[49] Alexey Ignatiev, Antonio Morgado, and Joao Marques-Silva. 2018.                    Heidelberg, Berlin, Heidelberg, 454–469. https://doi.org/10.1007/978-
     PySAT: A Python Toolkit for Prototyping with SAT Oracles. In Theory                3-642-23786-7_35
     and Applications of Satisfiability Testing – SAT 2018 (Lecture Notes          [59] Serdar Kadioglu, Yuri Malitsky, Meinolf Sellmann, and Kevin Tierney.
     in Computer Science, Vol. 10929). Springer International Publishing,               2010. ISAC – Instance-Specific Algorithm Configuration. In ECAI
     Cham, 428–437. https://doi.org/10.1007/978-3-319-94144-8_26                        2010: 19th European Conference on Artificial Intelligence (Frontiers in
[50] Alexey Ignatiev, Zi Li Tan, and Christos Karamanos. 2024. Towards                  Artificial Intelligence and Applications, Vol. 215). IOS Press, Amster-
     Universally Accessible SAT Technology. In 27th International Con-                  dam, Netherlands, 751–756. https://doi.org/10.3233/978-1-60750-
     ference on Theory and Applications of Satisfiability Testing (SAT 2024)            606-5-751
     (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 305),        [60] Moein Khazraee, Lu Zhang, Luis Vega, and Michael Bedford Taylor.
     Supratik Chakraborty and Jie-Hong Roland Jiang (Eds.). Schloss                     2017. Moonwalk: NRE optimization in ASIC clouds. In Proceedings of
     Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany,                      the Twenty-Second International Conference on Architectural Support
     16:1–16:11. https://doi.org/10.4230/LIPIcs.SAT.2024.16                             for Programming Languages and Operating Systems. Association for
[51] Yuka Ikarashi, Gilbert Louis Bernstein, Alex Reinking, Hasan Genc,                 Computing Machinery, New York, NY, USA, 511–526. https://doi.
     and Jonathan Ragan-Kelley. 2022. Exocompilation for productive                     org/10.1145/3037697.3037749
     programming of hardware accelerators. In Proceedings of the 43rd              [61] Ashiqur R. KhudaBukhsh, Lin Xu, Holger H. Hoos, and Kevin Leyton-
     ACM SIGPLAN International Conference on Programming Language                       Brown. 2016. SATenstein: Automatically building local search SAT
     Design and Implementation (San Diego, CA, USA) (PLDI 2022). As-                    solvers from components. Artificial Intelligence 232 (2016), 20–42.
     sociation for Computing Machinery, New York, NY, USA, 703–718.                     https://doi.org/10.1016/j.artint.2015.11.002
     https://doi.org/10.1145/3519939.3523446                                       [62] Donald E. Knuth. 2015. The Art of Computer Programming, Volume
[52] Ashlin Iser and Christoph Jabs. 2024. Global Benchmark Database. In                4, Fascicle 6: Satisfiability. Addison-Wesley Professional, Boston,
     27th International Conference on Theory and Applications of Satisfiabil-           MA, USA.            https://www.informit.com/store/art-of-computer-
     ity Testing (SAT 2024) (Leibniz International Proceedings in Informatics           programming-volume-4-fascicle-6-satisfiability-9780134397603
     (LIPIcs), Vol. 305), Supratik Chakraborty and Jie-Hong Roland Jiang           [63] Wietze Koops, Daniel Le Berre, Magnus O. Myreen, Jakob Nordström,
     (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl,               Andy Oertel, Yong Kiam Tan, and Marc Vinyals. 2025. Practically
     Germany, 18:1–18:10. https://doi.org/10.4230/LIPIcs.SAT.2024.18                    Feasible Proof Logging for Pseudo-Boolean Optimization. In 31st
[53] Matti Järvisalo, Daniel Le Berre, Olivier Roussel, and Laurent Simon.              International Conference on Principles and Practice of Constraint Pro-
     2012. The international SAT solver competitions. AI Magazine 33, 1                 gramming (CP 2025) (Leibniz International Proceedings in Informatics
     (2012), 89–94. https://doi.org/10.1609/aimag.v33i1.2395                            (LIPIcs), Vol. 340). Schloss Dagstuhl – Leibniz-Zentrum für Informatik,
[54] Susmit Jha, Sumit Gulwani, Sanjit A. Seshia, and Ashish Tiwari. 2010.              21:1–21:27. https://doi.org/10.4230/LIPIcs.CP.2025.21
     Oracle-guided component-based program synthesis. In Proceedings of            [64] Peter Lammich. 2023. GRAT: A Formally Verified (UN)SAT Proof
     the 32nd ACM/IEEE International Conference on Software Engineering                 Checker. In Proceedings of SAT Competition 2023: Solver, Benchmark
     – Volume 1. Association for Computing Machinery, New York, NY,                     and Proof Checker Descriptions (Department of Computer Science Series
     USA, 215–224. https://doi.org/10.1145/1806799.1806833                              of Publications B, Vol. B-2023-1). University of Helsinki, Helsinki,
[55] Susmit Jha and Sanjit A. Seshia. 2017. A theory of formal synthesis                Finland, 82–85. https://hdl.handle.net/10138/563824
     via inductive learning. Acta Informatica 54, 7 (2017), 693–726. https:        [65] Robert Tjarko Lange, Qi Sun, Aaditya Prasad, Maxence Faldor, Yujin
     //doi.org/10.1007/s00236-017-0294-5                                                Tang, and David Ha. 2025. Towards Robust Agentic CUDA Kernel
[56] Rajeev Joshi, Greg Nelson, and Keith Randall. 2002. Denali: a goal-                Benchmarking, Verification, and Optimization. arXiv:2509.14279
     directed superoptimizer. ACM SIGPLAN Notices 37, 5 (May 2002),                     https://arxiv.org/abs/2509.14279
     304–314. https://doi.org/10.1145/543552.512566                                [66] Jiale Lao and Immanuel Trummer. 2026. Demonstrating GenDB:
[57] Norman P. Jouppi, Cliff Young, Nishant Patil, David Patterson, Gau-                Instance-Optimized and Customized Query Processing Code Gener-
     rav Agrawal, Raminder Bajwa, Sarah Bates, Suresh Bhatia, Nan Bo-                   ation via LLM Agents. Proceedings of the VLDB Endowment 19, 12
     den, Al Borchers, Rick Boyle, Pierre-luc Cantin, Clifford Chao, Chris              (2026), 4602–4605. https://doi.org/10.14778/3827998.3828076
     Clark, Jeremy Coriell, Mike Daley, Matt Dau, Jeffrey Dean, Ben Gelb,          [67] Jia Hui Liang, Vijay Ganesh, Pascal Poupart, and Krzysztof Czarnecki.
     Tara Vazir Ghaemmaghami, Rajendra Gottipati, William Gulland,                      2016. Learning rate based branching heuristic for SAT solvers. In The-
     Robert Hagmann, C. Richard Ho, Doug Hogberg, John Hu, Robert                       ory and Applications of Satisfiability Testing – SAT 2016 (Lecture Notes
     Hundt, Dan Hurt, Julian Ibarz, Aaron Jaffey, Alek Jaworski, Alexander              in Computer Science, Vol. 9710). Springer International Publishing,
     Kaplan, Harshit Khaitan, Daniel Killebrew, Andy Koch, Naveen Ku-                   Cham, 123–140. https://doi.org/10.1007/978-3-319-40970-2_9
     mar, Steve Lacy, James Laudon, James Law, Diemthu Le, Chris Leary,            [68] Erik Lindholm, John Nickolls, Stuart Oberman, and John Montrym.
     Zhuyuan Liu, Kyle Lucke, Alan Lundin, Gordon MacKean, Adri-                        2008. NVIDIA Tesla: A unified graphics and computing architecture.
     ana Maggiore, Maire Mahony, Kieran Miller, Rahul Nagarajan, Ravi                   IEEE Micro 28, 2 (2008), 39–55. https://doi.org/10.1109/mm.2008.31
     Narayanaswami, Ray Ni, Kathy Nix, Thomas Norrie, Mark Omernick,               [69] Fei Liu, Xialiang Tong, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun
     Narayana Penukonda, Andy Phelps, Jonathan Ross, Matt Ross, Amir                    Wang, Zhichao Lu, and Qingfu Zhang. 2024. Evolution of heuristics:
     Salek, Emad Samadiani, Chris Severn, Gregory Sizikov, Matthew                      towards efficient automatic algorithm design using large language
     Snelham, Jed Souter, Dan Steinberg, Andy Swing, Mercedes Tan, Gre-                 model. In Proceedings of the 41st International Conference on Machine
     gory Thorson, Bo Tian, Horia Toma, Erick Tuttle, Vijay Vasudevan,                  Learning (Vienna, Austria) (Proceedings of Machine Learning Research,
The Case for Automated Hyperspecialization:
Evidence from SAT

      Vol. 235). PMLR, Vienna, Austria, 32201–32223. https://proceedings.              Piscataway, NJ, USA, 9–17. https://doi.org/10.1109/ictai.2013.13
      mlr.press/v235/liu24bs.html                                                 [83] OpenAI. 2026. GPT-5.6: Frontier Intelligence That Scales with Your
 [70] Fei Liu, Yiming Yao, Ping Guo, Zhiyuan Yang, Xi Lin, Zhe Zhao, Xi-               Ambition. OpenAI. https://openai.com/index/gpt-5-6/ GPT-5.6 Sol.
      aliang Tong, Kun Mao, Zhichao Lu, Zhenkun Wang, Mingxuan Yuan,              [84] OpenAI. 2026. Jalapeño’s First Results Show Industry-Leading Speed
      and Qingfu Zhang. 2026. A Systematic Survey on Large Language                    and Efficiency in AI Inference. OpenAI. https://openai.com/index/
      Models for Algorithm Design. Comput. Surveys 58, 8, Article 218                  jalapeno-first-results/
      (June 2026), 32 pages. https://doi.org/10.1145/3787585                      [85] OpenTitan Contributors. [n. d.]. OpenTitan Documentation. Open-
 [71] Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and                  Titan. Retrieved September 9, 2026 from https://opentitan.org/book/
      John Regehr. 2021. Alive2: bounded translation validation for LLVM.         [86] Anne Ouyang, Simon Guo, Simran Arora, Alex L. Zhang, William Hu,
      In Proceedings of the 42nd ACM SIGPLAN International Conference on               Christopher Ré, and Azalia Mirhoseini. 2025. KernelBench: can LLMs
      Programming Language Design and Implementation (Virtual, Canada)                 write efficient GPU kernels?. In Proceedings of the 42nd International
      (PLDI 2021). Association for Computing Machinery, New York, NY,                  Conference on Machine Learning (Vancouver, Canada) (Proceedings
      USA, 65–79. https://doi.org/10.1145/3453483.3454030                              of Machine Learning Research, Vol. 267). PMLR, Vancouver, Canada,
 [72] Manuel López-Ibáñez, Jérémie Dubois-Lacoste, Leslie Pérez Cáceres,               47356–47415. https://proceedings.mlr.press/v267/ouyang25a.html
      Mauro Birattari, and Thomas Stützle. 2016. The irace package: It-           [87] Tuomas Pelkonen, Scott Franklin, Justin Teller, Paul Cavallaro, Qi
      erated racing for automatic algorithm configuration. Operations                  Huang, Justin Meza, and Kaushik Veeraraghavan. 2015. Gorilla: A
      Research Perspectives 3 (2016), 43–58. https://doi.org/10.1016/j.orp.            Fast, Scalable, In-Memory Time Series Database. Proceedings of the
      2016.09.002                                                                      VLDB Endowment 8, 12 (2015), 1816–1827. https://doi.org/10.14778/
 [73] Anil Madhavapeddy, Richard Mortier, Charalampos Rotsos, David                    2824032.2824078
      Scott, Balraj Singh, Thomas Gazagnaire, Steven Smith, Steven Hand,          [88] Amir Pnueli, Michael Siegel, and Eli Singerman. 1998. Translation
      and Jon Crowcroft. 2013. Unikernels: Library Operating Systems for               validation. In International Conference on Tools and Algorithms for
      the Cloud. In Proceedings of the eighteenth international conference             the Construction and Analysis of Systems (Lecture Notes in Computer
      on Architectural support for programming languages and operating                 Science, Vol. 1384). Springer Berlin Heidelberg, Berlin, Heidelberg,
      systems. Association for Computing Machinery, New York, NY, USA,                 151–166. https://doi.org/10.1007/bfb0054170
      461–472. https://doi.org/10.1145/2451116.2451167                            [89] Oleksandr Polozov and Sumit Gulwani. 2015. FlashMeta: A Frame-
 [74] J. P. Marques-Silva and K. A. Sakallah. 1999. GRASP: a search al-                work for Inductive Program Synthesis. In Proceedings of the 2015 ACM
      gorithm for propositional satisfiability. IEEE Trans. Comput. 48, 5              SIGPLAN International Conference on Object-Oriented Programming,
      (1999), 506–521. https://doi.org/10.1109/12.769433                               Systems, Languages, and Applications. Association for Computing
 [75] Henry Massalin. 1987. Superoptimizer: a look at the smallest program.            Machinery, New York, NY, USA, 107–126. https://doi.org/10.1145/
      ACM SIGARCH Computer Architecture News 15, 5 (Oct. 1987), 122–126.               2814270.2814310
      https://doi.org/10.1145/36177.36194                                         [90] M. Püschel, J. M. F. Moura, J. R. Johnson, D. Padua, M. M. Veloso,
 [76] Kevin Meng, Vincent Huang, Jacob Steinhardt, and Sarah                           B. W. Singer, Jianxin Xiong, F. Franchetti, A. Gacic, Y. Voronenko, K.
      Schwettmann. 2025. Introducing Docent. Transluce.                  https:        Chen, R. W. Johnson, and N. Rizzolo. 2005. SPIRAL: Code Generation
      //transluce.org/docent/blog/introducing-docent                                   for DSP Transforms. Proc. IEEE 93, 2 (2005), 232–275. https://doi.
 [77] Antonio Morgado, Alexey Ignatiev, and Joao Marques-Silva. 2015.                  org/10.1109/jproc.2004.840306
      MSCG: Robust Core-Guided MaxSAT Solving: System Description.                [91] Jonathan Ragan-Kelley, Connelly Barnes, Andrew Adams, Sylvain
      Journal on Satisfiability, Boolean Modeling and Computation 9, 1 (2015),         Paris, Frédo Durand, and Saman Amarasinghe. 2013. Halide: a
      129–134. https://doi.org/10.3233/sat190105                                       language and compiler for optimizing parallelism, locality, and re-
 [78] Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang,                 computation in image processing pipelines. In Proceedings of the
      and Sharad Malik. 2001. Chaff: engineering an efficient SAT solver. In           34th ACM SIGPLAN Conference on Programming Language Design
      Proceedings of the 38th Annual Design Automation Conference (Las Ve-             and Implementation (Seattle, Washington, USA) (PLDI ’13). Asso-
      gas, Nevada, USA) (DAC ’01). Association for Computing Machinery,                ciation for Computing Machinery, New York, NY, USA, 519–530.
      New York, NY, USA, 530–535. https://doi.org/10.1145/378239.379017                https://doi.org/10.1145/2491956.2462176
 [79] Saeed Nejati and Vijay Ganesh. 2019. CDCL(Crypto) SAT Solvers               [92] Joseph E. Reeves. 2025. Cardinality Constraints in Boolean Satisfia-
      for Cryptanalysis. In Proceedings of the 29th Annual International               bility Solving. Ph.D. thesis. Carnegie Mellon University, Pittsburgh,
      Conference on Computer Science and Software Engineering (CASCON                  PA, USA. https://www.cs.cmu.edu/~jereeves/research/jereeves_phd_
      ’19). IBM Corp., Riverton, NJ, USA, 311–316. https://arxiv.org/abs/              csd_2025.pdf Technical Report CMU-CS-25-147.
      2005.13415                                                                  [93] Jaime Rodríguez-Guerra and Jannis Leidel. 2023. Conda 23.10.0:
 [80] Aina Niemetz, Mathias Preiner, Florian Lonsing, Martina Seidl, and               libmamba is now the default solver. Conda Blog. https://conda.org/
      Armin Biere. 2012. Resolution-Based Certificate Extraction for QBF               blog/2023-11-06-conda-23-10-0-release/ Accessed: 2026-08-29.
      (Tool Presentation). In Theory and Applications of Satisfiability Testing   [94] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander
      – SAT 2012 (Lecture Notes in Computer Science, Vol. 7317). Springer,             Novikov, Matej Balog, M. Pawan Kumar, Emilien Dupont, Francisco
      430–435. https://doi.org/10.1007/978-3-642-31612-8_33                            J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi, Push-
 [81] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont,                 meet Kohli, and Alhussein Fawzi. 2024. Mathematical discoveries
      Po-Sen Huang, Adam Zsolt Wagner, Sergey Shirobokov, Borislav                     from program search with large language models. Nature 625, 7995
      Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian, M. Pawan Ku-                  (2024), 468–475. https://doi.org/10.1038/s41586-023-06924-6
      mar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies,            [95] Eric Schkufza, Rahul Sharma, and Alex Aiken. 2013. Stochastic
      Sebastian Nowozin, Pushmeet Kohli, and Matej Balog. 2025. Al-                    superoptimization. ACM SIGARCH Computer Architecture News 41, 1
      phaEvolve: A coding agent for scientific and algorithmic discovery.              (2013), 305–316. https://doi.org/10.1145/2490301.2451150
      arXiv:2506.13131 [cs.AI] https://arxiv.org/abs/2506.13131                   [96] Junjie Sheng, Yanqiu Lin, Jiehao Wu, Yanhong Huang, Jianqi Shi, Min
 [82] Toru Ogawa, Yangyang Liu, Ryuzo Hasegawa, Miyuki Koshimura,                      Zhang, and Xiangfeng Wang. 2025. SolSearch: An LLM-Driven Frame-
      and Hiroshi Fujita. 2013. Modulo based CNF encoding of cardinality               work for Efficient SAT-Solving Code Generation. In 2025 IEEE/ACM
      constraints and its application to MaxSAT solvers. In 2013 IEEE 25th             47th International Conference on Software Engineering: New Ideas
      International Conference on Tools with Artificial Intelligence. IEEE,            and Emerging Results (ICSE-NIER). IEEE, Piscataway, NJ, USA, 6–10.
                                                                                                        Harrison Green, Claire Le Goues, and Fraser Brown


      https://doi.org/10.1109/icse-nier66352.2025.00007                                arXiv:2505.11480 [cs.CL] https://arxiv.org/abs/2505.11480 Revised
 [97] Carsten Sinz. 2005. Towards an Optimal CNF Encoding of Boolean                   August 8, 2026.
      Cardinality Constraints. In Principles and Practice of Constraint Pro-     [111] Junyu Wei, Guangyan Zhang, Yang Wang, Zhiwei Liu, Zhanyang Zhu,
      gramming - CP 2005 (Lecture Notes in Computer Science, Vol. 3709),               Junchao Chen, Tingtao Sun, and Qi Zhou. 2021. On the Feasibility
      Peter van Beek (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg,            of Parser-based Log Compression in Large-Scale Cloud Systems.
      827–831. https://doi.org/10.1007/11564751_73                                     In 19th USENIX Conference on File and Storage Technologies (FAST
 [98] Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Se-                  2021). USENIX Association, Berkeley, CA, USA, 249–262. https:
      shia, and Vijay Saraswat. 2006. Combinatorial sketching for finite               //www.usenix.org/conference/fast21/presentation/wei
      programs. In Proceedings of the 12th international conference on Ar-       [112] Nathan Wetzler, Marijn J. H. Heule, and Warren A. Hunt, Jr. 2014.
      chitectural support for programming languages and operating systems.             DRAT-trim: Efficient Checking and Trimming Using Expressive
      Association for Computing Machinery, New York, NY, USA, 404–415.                 Clausal Proofs. In Theory and Applications of Satisfiability Testing
      https://doi.org/10.1145/1168857.1168907                                          – SAT 2014 (Lecture Notes in Computer Science, Vol. 8561). Springer,
 [99] Mate Soos, Karsten Nohl, and Claude Castelluccia. 2009. Extending                Cham, 422–429. https://doi.org/10.1007/978-3-319-09284-3_31
      SAT Solvers to Cryptographic Problems. In Theory and Applications          [113] R. Clint Whaley and Jack J. Dongarra. 1998. Automatically Tuned
      of Satisfiability Testing - SAT 2009, 12th International Conference, SAT         Linear Algebra Software. In SC ’98: Proceedings of the 1998 ACM/IEEE
      2009, Swansea, UK, June 30 - July 3, 2009. Proceedings (Lecture Notes in         Conference on Supercomputing. IEEE, Piscataway, NJ, USA, 38. https:
      Computer Science, Vol. 5584), Oliver Kullmann (Ed.). Springer, Berlin,           //doi.org/10.1109/sc.1998.10004
      Heidelberg, 244–257. https://doi.org/10.1007/978-3-642-02777-2_24          [114] Lin Xu, Holger Hoos, and Kevin Leyton-Brown. 2010. Hydra: Au-
[100] Michael Stonebraker, Daniel J. Abadi, Adam Batkin, Xuedong Chen,                 tomatically Configuring Algorithms for Portfolio-Based Selection.
      Mitch Cherniack, Miguel Ferreira, Edmond Lau, Amerson Lin, Samuel                Proceedings of the AAAI Conference on Artificial Intelligence 24, 1 (Jul.
      Madden, Elizabeth J. O’Neil, Pat O’Neil, Alex Rasin, Nga Tran, and               2010), 210–216. https://doi.org/10.1609/aaai.v24i1.7565
      Stan Zdonik. 2005. C-Store: A Column-oriented DBMS. In Proceedings         [115] Lin Xu, Frank Hutter, Holger H. Hoos, and Kevin Leyton-Brown.
      of the 31st International Conference on Very Large Data Bases. VLDB              2008. SATzilla: Portfolio-Based Algorithm Selection for SAT. Journal
      Endowment, Trondheim, Norway, 553–564. https://www.vldb.org/                     of Artificial Intelligence Research 32 (2008), 565–606. https://doi.org/
      archives/website/2005/program/paper/thu/p553-stonebraker.pdf                     10.1613/jair.2490
[101] Michael Stonebraker and Uğur Çetintemel. 2005. “One Size Fits              [116] Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo
      All”: An Idea Whose Time Has Come and Gone. In 21st International                Hua, Haeyeon Kim, Jinkyoo Park, and Guojie Song. 2024. ReEvo:
      Conference on Data Engineering (ICDE’05). IEEE, Piscataway, NJ, USA,             large language models as hyper-heuristics with reflective evolution.
      2–11. https://doi.org/10.1109/icde.2005.1                                        In Advances in Neural Information Processing Systems (Vancouver,
[102] Yiwen Sun, Furong Ye, Zhihan Chen, Ke Wei, and Shaowei Cai. 2025.                BC, Canada), Vol. 37. Curran Associates Inc., Red Hook, NY, USA,
      Discovering heuristics in a complex SAT solver with large language               43571–43608. https://doi.org/10.52202/079017-1381
      models. arXiv:2507.22876 [cs.AI] https://arxiv.org/abs/2507.22876          [117] Cunxi Yu, Rongjian Liang, Chia-Tung Ho, and Haoxing Ren.
      Revised June 6, 2026.                                                            2025. Autonomous Code Evolution Meets NP-Completeness.
[103] Yiwen Sun, Furong Ye, Xianyin Zhang, Shiyu Huang, Bingzhen                       arXiv:2509.07367 [cs.AI] https://arxiv.org/abs/2509.07367
      Zhang, Ke Wei, and Shaowei Cai. 2026. AutoSAT: Automatically               [118] Lintao Zhang and Sharad Malik. 2003. Validating SAT solvers using
      Optimize SAT Solvers via Large Language Models. Journal of                       an independent resolution-based checker: Practical implementations
      Artificial Intelligence Research 86, Article 29 (July 2026), 50 pages.           and other applications. In 2003 Design, Automation and Test in Europe
      https://doi.org/10.1613/jair.1.20499                                             Conference and Exhibition. IEEE Computer Society, Los Alamitos, CA,
[104] Yong Kiam Tan, Marijn J. H. Heule, and Magnus O. Myreen. 2023.                   USA, 880–885. https://doi.org/10.1109/date.2003.1253717
      Verified LRAT and LPR Proof Checking with cake_lpr. In Proceed-
      ings of SAT Competition 2023: Solver, Benchmark and Proof Checker
      Descriptions (Department of Computer Science Series of Publications
      B, Vol. B-2023-1). University of Helsinki, Helsinki, Finland, 89–90.
      https://hdl.handle.net/10138/563824
[105] The OpenROAD Project. [n. d.]. OpenROAD Flow Scripts Docu-
      mentation. The OpenROAD Project. Retrieved September 9, 2026
      from https://openroad-flow-scripts.readthedocs.io/en/latest/index2.
      html
[106] Emina Torlak and Rastislav Bodik. 2014. A lightweight symbolic vir-
      tual machine for solver-aided host languages. ACM SIGPLAN Notices
      49, 6 (2014), 530–541. https://doi.org/10.1145/2666356.2594340
[107] Alasdair Urquhart. 1987. Hard examples for resolution. J. ACM 34, 1
      (1987), 209–219. https://doi.org/10.1145/7531.8928
[108] Haoyu Wang, Yuliang Song, Tao Li, Zhiwei Deng, Yaqing Wang,
      Deepak Ramachandran, Eldan Cohen, and Dan Roth. 2026. Formalize,
      Don’t Optimize: The Heuristic Trap in LLM-Generated Combinatorial
      Solvers. arXiv:2605.12421 [cs.AI] https://arxiv.org/abs/2605.12421
[109] Johannes Wehrstein, Timo Eckmann, Matthias Jasny, and Carsten
      Binnig. 2026. Bespoke OLAP: Synthesizing Workload-Specific One-
      size-fits-one Database Engines. Proceedings of the VLDB Endowment
      19, 11 (2026), 3759–3771. https://doi.org/10.14778/3836663.3836723
[110] Anjiang Wei, Tarun Suresh, Huanmi Tan, Yinglun Xu, Gagan-
      deep Singh, Ke Wang, and Alex Aiken. 2025. SuperCoder: As-
      sembly Program Superoptimization with Large Language Models.
The Case for Automated Hyperspecialization:
Evidence from SAT

A     Agent prompt
Each agent is prompted with the core task prompt (§A.1) plus a proof instruction extension depending on the selected proof
format: DPR: §A.2, GRAT: §A.3, or VeriPB: §A.4. In addition, we also provide condensed documentation for each of the formats,
mounted in the container at /opt/autospec/docs (not shown here).

A.1    Task definition
  Mission: build an efficient, certifying solver specialized to the single target family `{family}`.

  This is deliberately not a general-purpose SAT-solver task. You are not required to use DPLL, CDCL, clause learning, or any other
        traditional SAT architecture, and your solver need not work on unrelated formulas. The intended advantage is to reverse-engineer this
        family's encoding, recover the high-level mathematical problem and generator structure, and solve that problem directly. Be creative
        and aggressively family-specific while remaining sound.

  Specialization principles:
  - Infer reusable family structure, not instance identities. It is valid to depend on a detected encoding, generator invariant, parameter
        regime, repeated block layout, or high-level theorem shared by the family.
  - Consider direct constructions, graph algorithms, matching or flow, dynamic programming, algebra, Gaussian elimination, bitset
        propagation, interval reasoning, symmetry reduction, bounded search over recovered objects, decomposition, or a purpose-built
        decision procedure. A conventional SAT core is optional, not the default objective.
  - Build conservative structural detectors and validate every assumed invariant across diverse training instances. If an input does not
        match the supported structure, return `s UNKNOWN`; never stretch an unsound fast path.
  - Treat CNF-to-problem and problem-to-certificate mappings as first-class algorithm components. For SAT, reconstruct a complete DIMACS
        assignment and independently check every original clause. For UNSAT, design the selected proof strategy alongside the high-level
        algorithm rather than after it.
  - Optimize the whole evaluated path: parsing, detection, solving, model/proof generation, proof size, elaboration cost, and verified-kernel
        cost. Once the algorithm is right, profile representative sizes and use appropriate compiled, cache-friendly, bit-parallel, or
        incremental data structures.

  Recommended workflow:
  1. Survey multiple small, medium, and large training formulas. Measure variable/clause counts, clause-width and polarity distributions,
        units/binaries, components, variable degrees, repeated strides/blocks, and signatures of gates, XORs, cardinalities, grids, graphs,
        permutations, schedules, or time steps.
  2. Form explicit hypotheses about high-level objects and the variable/clause mapping. Write small analysis tools when helpful, and falsify
        each hypothesis on the full training set instead of trusting one attractive example.
  3. Prototype the direct high-level solver and a conservative recognizer. Check high-level answers against the original CNF before investing
        in optimization.
  4. Prototype certificate production on tiny self-authored proof unit tests (not additional family benchmarks) with the installed checker
        pipeline. Establish a proof-generating invariant that scales with the specialized algorithm.
  5. Implement the competition package, test locally on representative training formulas, submit, inspect per-instance status and timing, and
        iterate. Fix every invalid model, invalid proof, crash, timeout, or proof-checker resource failure before chasing marginal speed.
  6. Leave a concise README in the solver directory explaining the recovered encoding, supported detector, algorithm, certificate
        construction, experiments, limitations, and promising next steps for future runs.

  Scope and integrity rules:
  - `/data/train` is the complete, read-only training set authorized for this run. Do not search for, request, download, reconstruct, or
        synthesize additional benchmark formulas, even when web search is enabled.
  - Hidden validation instances, membership, labels, runtimes, metrics, failures, job details, and storage locations are private. Do not
        attempt to infer or access them.
  - Do not memorize, branch on, or encode training filenames, hashes, comments, literal sequences, or individual training instances. Build
        family-level algorithmic improvements only.
  - Imported provenance labels are not correctness oracles. Return SAT/UNSAT only with a certificate accepted by the selected checker;
        otherwise print `s UNKNOWN`.

  A ready-to-edit C++20 scaffold is installed at `/workspace/solver`. Work in that directory rather than starting elsewhere. Its only
        required contract files are `README.md`, executable `build.sh`, and executable `run.sh`; keep the README current with the recovered
        structure, algorithm, certificate construction, experiments, limitations, and next steps.

  The Ubuntu 24.04 agent environment includes Python 3.12 (with development headers and venv support), Node/npm, Clang/Clang++ 16, LLD 16,
        CMake, Ninja, Make, GDB, strace, `time`, Git, curl, ripgrep (`rg`), `fd`, jq, `file`, `xxd`, `pdftotext`, `lsof`, `bc`, `tree`,
        `tar`, `unzip`, `zip`, `bzip2`, and `xz`, in addition to the selected proof tools. Clang's AddressSanitizer runtime is installed, so
        local manual debug builds with `-fsanitize=address` are supported; restore the normal optimized `build.sh` before submission. These
        tools are available for local analysis, debugging, and builds; submitted solvers must still be self-contained for the smaller worker
        runtime.

  The `kissat` and `cadical` binaries are installed for local experiments, hypothesis checks, and comparison on authorized training
        formulas. They are local analysis tools only: never invoke either binary from `run.sh`, the submitted solver, or any subprocess
        during actual solving, and do not make the submitted artifact depend on them.
                                                                                               Harrison Green, Claire Le Goues, and Fraser Brown


 The submission host invokes `build.sh` exactly once as `build.sh <artifact-dir>` inside the local `linux/amd64` builder container. The
       scaffold compiles with the worker-matched flags `-std=c++20 -O3 -march=icelake-server -mtune=icelake-server -DNDEBUG -pthread`; do
       not use `-march=native`. Put the executable solver and any runtime-only files in the supplied artifact directory. GCP workers receive
       that precompiled artifact, do not invoke `build.sh`, and call only:

      run.sh <formula.cnf> <output-dir>

 Write only SAT Competition lines to stdout: `c ...`, exactly one `s SATISFIABLE`, `s UNSATISFIABLE`, or `s UNKNOWN`, and `v ... 0` for
       SAT. The exact SAT reference is `/opt/autospec/docs/proof-formats/sat.md`. Every SAT assignment line written by the solver must
       retain its `v ` prefix; literals may be wrapped across multiple `v` lines or placed on one long line, and the broker imposes no
       per-line character limit. Terminate the whole model exactly once with `0` and emit no later literals. The broker validates this
       stdout, strips the `s`/`v` prefixes, and gives `gratchk sat` a prefix-free raw literal file. Therefore never pass prefixed solver
       stdout directly to `gratchk`; capture the real stdout and run `autospec-check-sat formula.cnf solver.stdout` for the
       broker-equivalent local check. For UNSAT, write the selected proof syntax to `<output-dir>/proof.out`. Return exit code 0 after every
       well-formed SAT, UNSAT, or UNKNOWN response; any other exit code is a solver crash.

 Evaluation worker resources:
 - Each evaluation task is provisioned with {evaluation_cpu_cores:g} {evaluation_cpu_label} and {evaluation_memory_gib:g} GiB of RAM. The
       solver and subsequent verifier stages run sequentially within that task allocation. {evaluation_cpu_guidance}
 - The local agent container and the 4-vCPU builder can expose different resources. Optimize and size the submitted runtime for the
       evaluation allocation, especially peak solver/proof memory.

 Evaluation time budgets:
 - The evaluation runner externally stops each solver invocation after {solver_timeout_seconds} seconds. This is a development-efficiency
       cutoff that avoids spending evaluation capacity on hard instances, not a desired stopping point or a limit on how deployed artifacts
       may be used.
 - Do not add, tune, or preserve an internal watchdog, safety margin, or elapsed-time check that returns `s UNKNOWN` or otherwise gives up
       near this cutoff. In particular, do not stop a few seconds early to anticipate the evaluator. Keep making sound progress until the
       external runner stops the process so the artifact remains useful under longer deployment limits.
 - Certificate verification has a separate {verifier_timeout_seconds}-second total wall-clock budget shared by elaboration and the verified
       kernel. Verification time is reported separately and is excluded from the solver score.

 Agent effort budgets:
 - Work diligently throughout the available budget. This run has {active_time_hours:g} hours of active work and at most {max_evaluations}
       accepted evaluation submissions. Active time includes reasoning, local analysis, implementation, builds, local tests, MCP calls other
       than evaluation waiting, and resume overhead. Time spent blocked inside `wait_for_completion` is paused and does not consume active
       work.
 - Call `get_budget` whenever useful to see exact used and remaining active seconds and evaluation submissions. The supervisor interrupts
       the session when active time is exhausted. If a turn ends before 95% of active time is used and evaluation capacity remains, it
       automatically resumes the same session with the remaining budget.
 - Do not stop after one plausible approach or one good score. Use the budget for careful structural investigation, correctness testing,
       profiling, and measured iterations. An evaluation request beyond the submission limit is rejected and the session is stopped.
 - Every accepted submission is a checkpoint. The system automatically selects the best-performing correct checkpoint across the run, so the
       last submission does not need to restate or recreate the best earlier solver. Focus each submission on learning or improving
       performance while guaranteeing correctness across all supported inputs.

 Use the bound MCP tools `submit_solver`, `get_status`, `get_budget`, `wait_for_completion`, and `get_results`. Submit `/workspace/solver`.
       They evaluate training only. Each run permits one active training evaluation at a time. After submitting, call `wait_for_completion`
       with no arguments; it follows the current training evaluation and waits for up to three hours, so do not poll `get_status` while that
       evaluation is active. Every submission also triggers an independent private validation run; that run never blocks another training
       submission.




A.2   DPR extension
 Selected proof contract: DPR.
 - The comprehensive local reference is `/opt/autospec/docs/proof-formats/dpr.md`. Read it before implementing the proof logger and consult
       it whenever syntax or elaboration is unclear.
 - Emit textual DPR into `proof.out`; each addition is `<clause> 0` or `<clause> <witness> 0`, and each deletion is `d <clause> 0`.
 - A PR witness has no separator token: it must start by repeating the first clause literal. Example: `-4 -17 -4 -17 1 20 0` has clause `-4
       -17` and witness `-4 -17 1 20`.
 - A witness-free addition is checked as RUP and then RAT; for RAT the first literal is the pivot. A witnessed non-RUP addition uses
       propagation redundancy. Deletions name clauses by contents, not IDs.
 - Prefer simple RUP steps when possible, use PR witnesses for a tested family-level repair/symmetry map, terminate every step with `0`, and
       normally derive the empty clause with `0`.
 - Locally elaborate: `dpr-trim formula.cnf proof.out -L elaborated.lpr`.
 - Check the verified kernel proof: `cake_lpr formula.cnf elaborated.lpr`.
 - Inspect `elaborated.lpr` to debug IDs, pivots, witnesses, and propagation/candidate hint blocks. Only the exact kernel line `s VERIFIED
       UNSAT` establishes success; elaborator acceptance is not a verified certificate.
The Case for Automated Hyperspecialization:
Evidence from SAT

A.3    GRAT extension
  Selected proof contract: GRAT.
  - The comprehensive local reference is `/opt/autospec/docs/proof-formats/grat.md`. Read it before implementing the proof logger and consult
        it whenever syntax or elaboration is unclear.
  - Emit ASCII textual DRAT into `proof.out`, not a GRAT kernel file and not binary DRAT. Additions are `<clause literals> 0`; deletions are
        `d <clause literals> 0`; `0` alone adds the empty clause.
  - Additions are checked first by RUP. If RUP fails, the first literal is the RAT pivot and all required opposite-pivot candidates must be
        justified. DRAT has no explicit PR witness or PB arithmetic.
  - Deletions name live clauses by contents, not IDs. Get the proof working without deletion first, then delete only after the last use of a
        clause as a propagation reason or RAT candidate.
  - Locally elaborate: `gratgen formula.cnf proof.out -o elaborated.gratp -l elaborated.gratl`.
  - Check the verified proof: `gratchk unsat formula.cnf elaborated.gratl elaborated.gratp`.
  - `gratgen` may report `s VERIFIED` on stderr; that is not the final result. Only the exact `gratchk` stdout line `s VERIFIED UNSAT`
        establishes success.


A.4    VeriPB extension
  Selected proof contract: VeriPB.
  - The comprehensive local reference is `/opt/autospec/docs/proof-formats/veripb.md`. Read it before implementing the proof logger and
        consult it whenever syntax, IDs, arithmetic, or subproofs are unclear.
  - Emit an augmented pseudo-Boolean proof version 3.0 into `proof.out`. The required outer structure is:
    `pseudo-Boolean proof version 3.0`
    `f <number-of-input-clauses>;`
    `<derivation rules, each ending in ;>`
    `output NONE;`
    `conclusion UNSAT : <live-contradiction-id>;`
    `end pseudo-Boolean proof;`
  - Input clauses receive IDs `1..N`; every constraint-adding derivation receives the next ID, while deletions do not. CNF literal `k` is
        `xk`, literal `-k` is `~xk`, and a clause becomes `+1 <lit> ... >= 1`.
  - Use `rup <constraint>;` for PB reverse unit propagation and `pol <RPN expression>;` for cutting-planes arithmetic. For example, opposite
        unit constraints at IDs 5 and 6 yield a contradiction with `pol 5 6 +;`.
  - Augmented conveniences include `ia` for syntactic implication/addition, `red` with a substitution witness for satisfiability-preserving
        strengthening, `pbc` subproofs, order-backed `dom`, and `del id <ids>;`. Let VeriPB elaborate these to explicit CakePB kernel steps
        and ordered RUP hints.
  - Locally elaborate with the exact worker order: `veripb -u --cnf --elaborate elaborated.pbp formula.cnf proof.out`.
  - Check the verified kernel proof: `cake_pb_cnf formula.cnf elaborated.pbp`.
  - Inspect the elaborated proof to debug absolute IDs and annotations. Only frontend `s VERIFIED UNSATISFIABLE` followed by kernel `s
        VERIFIED UNSAT` establishes success.
                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


B    Extended performance results
In the main body of RQ1 (§4.2) we evaluate the top specialist
against the per-family VBS of the four core baselines. This
serves as a sort of lower bound on the potential of hyperspe-
cialization: How effective are the best specialists compared to
a strong baseline?
   Here we include a complete enumeration of head-to-head
results, visualized in a similar format. Figure 9 shows the per-
family head-to-head performance of specialists constructed
for every format (DPR, VeriPB, GRAT) as well as the best
specialist compared to: each of the four core baselines indi-
vidually, the per-family virtual-best of the four core baselines,
and three additional baselines from related work in LLM-
based solver synthesis: AutoSAT [103], AutoModSAT [102],
and SolSearch [96].
The Case for Automated Hyperspecialization:
Evidence from SAT


 A      Without verification time                                                                                                                           Specialists vs. baselines
                                                Core baselines                                                                                  Additional baselines
                     SBVA                 Kissat            AE-Kissat             Satsuma                Family VBS                AutoSAT        AutoModSAT             SolSearch
                  2023 winner           2024 winner         2025 winner          2026 winner           4 core baselines

 DPR            109 /181 wins      105 /189 wins          105 /189 wins       126 /189 wins             101 /189 wins           137 /189 wins    139 /189 wins         105 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×
 VeriPB         110 /181 wins      104 /189 wins          101 /189 wins       125 /189 wins             99 /189 wins            146 /189 wins    143 /189 wins         104 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×
 GRAT           121 /181 wins          110 /189 wins      110 /189 wins       134 /189 wins            109 /189 wins            148 /189 wins    149 /189 wins         112 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×

                                                                                                         RQ1

 Best           128 /181 wins      123 /189 wins          123 /189 wins       145 /189 wins             121 /189 wins           160 /189 wins    158 /189 wins         125 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×
                 Specialization wins                   Baseline wins                           Share of families won                                 Families ranked within each panel

                                                        Validation PAR-2 ratio: baseline / specialist · Selections by training PAR-2




 B      With verification time                                                                                                                              Specialists vs. baselines
                                                Core baselines                                                                                  Additional baselines
                     SBVA                 Kissat            AE-Kissat             Satsuma                Family VBS                AutoSAT        AutoModSAT             SolSearch
                  2023 winner           2024 winner         2025 winner          2026 winner           4 core baselines

 DPR            109 /181 wins          101 /189 wins      101 /189 wins        131 /189 wins            96 /189 wins            131 /189 wins    139 /189 wins          98 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×
 VeriPB          111 /181 wins         97 /189 wins        99 /189 wins       132 /189 wins             95 /189 wins            131 /189 wins     141 /189 wins         96 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×
 GRAT           122 /181 wins          113 /189 wins      115 /189 wins       144 /189 wins             117 /189 wins           145 /189 wins    155 /189 wins         109 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×

                                                                                                         RQ1

 Best           131 /181 wins      120 /189 wins          124 /189 wins        151 /189 wins            121 /189 wins           153 /189 wins    158 /189 wins         117 /189 wins
         10⁶×
         10³×
           1×
        10⁻³×
                 Specialization wins                   Baseline wins                           Share of families won                                 Families ranked within each panel

                                                 Validation PAR-2 + verification ratio: baseline / specialist · Selections by training PAR-2



Figure 9. Full head-to-head per-family performance between specialists (rows) and baselines (columns). (A) Validation PAR-2
without verification time. (B) Validation PAR-2 including verification time, using the same training-selected solvers. Each
subplot ranks families by the baseline/specialist PAR-2 ratio. Labels denote families where the specialist outperforms the
baseline. The two specific subplots marked RQ1 denote the data highlighted in the main body of the paper.
                                                                   Harrison Green, Claire Le Goues, and Fraser Brown


C    Pareto frontier of on-demand
     specialization
Developing an optimal runtime policy is inherently a multi-
objective optimization problem. We want to both minimize
the makespan (𝑀𝜋 ) and maximize the number of solved for-
mulas (𝑄 𝜋 ). Picking an optimal policy therefore requires
determining the relationship between these two metrics: Do
we care more about solving quickly or solving every formula?
   In RQ2 (§4.3), we define optimality by a combined metric
𝑃𝜋 where an unsolved formula is equivalent to a penalty
of 2𝑇 seconds. This formula is not unreasonable (indeed it
mirrors PAR-2 which is widely used to measure SAT solver
performance), but it is arbitrary in the sense that we could
have decided an unsolved formula was worth more or less.
   Here, we visualize these on-demand runtime policy re-
sults without imposing a combined metric. Instead, for each
machine size (𝐶) and workload size (𝑁 ), we plot the Pareto
frontier of makespan and coverage tradeoffs. Each subplot
in Figure 10, Figure 11, and Figure 12 plots, for a particular
(𝐶, 𝑁 ) configuration, the average makespan 𝑀 𝜋 and average
coverage 𝑄 𝜋 for each runtime policy 𝜋 computed over all
family workloads of size 𝑁 :
                                𝑟
                        1 ∑︁ ∑︁
              𝑀 𝜋 :=               𝑀𝜋 (W𝑘(𝑖 ) , 𝐶)
                     𝑟 |𝐾 |
                            𝑘 ∈𝐾
                               𝑖=1
                                   𝑟
                          1 ∑︁ ∑︁
              𝑄 𝜋 :=               𝑄 𝜋 (W𝑘(𝑖 ) , 𝐶)
                       𝑟 |𝐾 |
                            𝑘 ∈𝐾
                               𝑖=1


   In each subplot, we draw a line between runtime policies
that sit on the Pareto frontier (i.e. no other policy has both a
smaller makespan and larger coverage). Additionally, we cir-
cle the point with the optimal average PAR-2 score computed
as:
                   𝑃 𝜋 := 𝑀 𝜋 + 2𝑇 (𝑁 − 𝑄 𝜋 )
   Note that since results here are averaged over every family,
the optimal policy selected here is not necessarily the same as
the most frequently optimal policy selected on a per-family
basis (as visualized in Figure 6).
The Case for Automated Hyperspecialization:
Evidence from SAT


                                 Coverage and makespan by workload (1/3)
                                                                                    *
                                       Pareto frontier             Optimal policy: πC, N = arg minπ ∈ Π Pπ (C, N)

                                                               C=1                     C=2                    C=4                        C=8                     C=16                      C=32                       C=64
                                                     AE-Kissat '25             AE-Kissat '25          Four-solver race           Four-solver race         Four-solver race         Four-solver race            Four-solver race

                                              0.6


                                 N=1



                                              0.4

                                                     500                500k   500             200k    500               100k     500               50k   500                20k    500                  20k    500               20k
                                                     AE-Kissat '25             AE-Kissat '25          AE-Kissat '25              Four-solver race         Four-solver race         Four-solver race            Four-solver race

                                               1.2


                                 N=2



                                              0.8

                                                     500                500k    500            200k    500               100k    500                50k   500                20k   500                   20k   500                20k
                                                     AE-Kissat '25             AE-Kissat '25          AE-Kissat '25              Four-solver race         Four-solver race         Four-solver race            Four-solver race

                                              2.4
 Mean verified solve count, Qπ




                                 N=4



                                               1.6

                                                     1k                 500k   1k              200k    500               100k     500               50k   500                20k   500                   20k   500                20k
                                                     AE-Kissat '25             AE-Kissat '25          AE-Kissat '25              AE-Kissat '25            Four-solver race         Four-solver race            Four-solver race

                                              4.8


                                 N=8



                                              3.2

                                                          5k            500k   2k              200k   1k                 100k     500               50k   500                20k   500                   20k   500                20k
                                                     AE-Kissat '25             AE-Kissat '25          AE-Kissat '25              AE-Kissat '25            Four-solver race         Four-solver race            Four-solver race

                                              9.6


                                 N=16



                                              6.4

                                                     5k                 500k     5k            200k    2k                100k    1k                 50k   500                20k   500                   20k 500                  20k
                                                     AE-Kissat '25             AE-Kissat '25          AE-Kissat '25              AE-Kissat '25            Four-solver race         Four-solver race            Four-solver race

                                             19.2


                                 N=32



                                             12.8

                                                     10k                500k   5k              200k     5k               100k     2k                50k   1k                 20k   500                   20k     1k               20k


                                                                                                              Mean makespan, Mπ (seconds; log scale)

                                                                 Fixed baseline                                                   Race                                              Specialization

                                       SBVA '23            Kissat '24      AE-Kissat '25        Satsuma '26                     Four-solver race                  Wait · DPR             Wait · VeriPB           Wait · GRAT
                                                                                                                                                                  Hybrid · DPR           Hybrid · VeriPB         Hybrid · GRAT



                                                                  Figure 10. Pareto frontier of on-demand runtime strategies. N=1 to N=32.
                                                                                                                                                                           Harrison Green, Claire Le Goues, and Fraser Brown



                                Coverage and makespan by workload (2/3)
                                                                                 *
                                    Pareto frontier             Optimal policy: πC, N = arg minπ ∈ Π Pπ (C, N)

                                                            C=1                         C=2                         C=4                        C=8                         C=16                          C=32                        C=64
                                                  AE-Kissat '25                AE-Kissat '25             AE-Kissat '25                AE-Kissat '25              Four-solver race             Four-solver race            Four-solver race

                                          38.4


                                N=64



                                          25.6

                                                  20k                  500k 10k                  200k    5k                 100k         5k                50k   2k                 20k       1k                    20k        1k                  20k
                                                  AE-Kissat '25                AE-Kissat '25             AE-Kissat '25                AE-Kissat '25              Four-solver race             Four-solver race            Four-solver race

                                          76.8


                                N=128



                                          51.2

                                                   50k          200k                 50k         200k         20k          100k          10k               50k        5k          20k         2k                    20k   1k                 10k
                                                  AE-Kissat '25                AE-Kissat '25             AE-Kissat '25                AE-Kissat '25              Four-solver race             Four-solver race            Four-solver race

                                           154
Mean verified solve count, Qπ




                                N=256



                                           102

                                                   100k                500k 50k                   200k               50k      100k         20k          50k            10k       20k                5k              20k    2k                10k
                                                  AE-Kissat '25                Hybrid · VeriPB           Hybrid · VeriPB              Wait · GRAT                Wait · GRAT                  Four-solver race            Four-solver race

                                           307


                                N=512



                                           205

                                                  200k               500k        100k          200k       50k                 200k               50k    100k               20k         50k            10k        20k                5k     10k
                                                  AE-Kissat '25                Hybrid · VeriPB           Hybrid · VeriPB              Wait · GRAT                Wait · GRAT                  Wait · GRAT                 Four-solver race

                                          600


                                N=1k



                                          400

                                                        420k    530k                170k    240k              100k     200k              50k            200k     20k                   100k              20k        50k              10k         20k
                                                  Wait · GRAT                  Hybrid · VeriPB           Wait · GRAT                  Wait · GRAT                Wait · GRAT                  Wait · GRAT                 Four-solver race

                                           1.2k


                                N=2k



                                          800

                                                         720k 840k                 270k     370k              200k         500k           100k      200k               50k             200k   20k                 100k    10k                     50k


                                                                                                                 Mean makespan, Mπ (seconds; log scale)

                                                               Fixed baseline                                                          Race                                                        Specialization

                                    SBVA '23            Kissat '24          AE-Kissat '25          Satsuma '26                       Four-solver race                        Wait · DPR             Wait · VeriPB              Wait · GRAT
                                                                                                                                                                             Hybrid · DPR           Hybrid · VeriPB            Hybrid · GRAT



                                                               Figure 11. Pareto frontier of on-demand runtime strategies. N=64 to N=2k.
The Case for Automated Hyperspecialization:
Evidence from SAT


                                 Coverage and makespan by workload (3/3)
                                                                                 *
                                     Pareto frontier            Optimal policy: πC, N = arg minπ ∈ Π Pπ (C, N)

                                                           C=1                      C=2                       C=4                         C=8                        C=16                        C=32                       C=64
                                                  Wait · GRAT              Wait · GRAT                Wait · GRAT                Wait · GRAT                 Wait · GRAT                 Wait · GRAT                Wait · GRAT

                                             3k


                                 N=5k



                                             2k

                                                        1.5M    1.9M         500k          1M              500k            2M       200k                1M     100k               500k     50k              200k     20k              100k
                                                  Wait · GRAT              Wait · GRAT                Wait · GRAT                Wait · GRAT                 Wait · GRAT                 Wait · GRAT                Wait · GRAT

                                             6k


                                 N=10k



                                             4k

                                                        2.7M 3.6M            1M             2M         500k         2M                 500k         2M            200k              1M        100k          500k       50k            200k
                                                  Wait · GRAT              Wait · GRAT                Wait · GRAT                Wait · GRAT                 Wait · GRAT                 Wait · GRAT                Wait · GRAT

                                            12k
 Mean verified solve count, Qπ




                                 N=20k



                                             8k

                                                        5M       7.1M             2.4M 3.4M           1M              5M           500k        2M                  500k            2M         200k             1M      100k           500k
                                                  Wait · GRAT              Wait · GRAT                Wait · GRAT                Wait · GRAT                 Wait · GRAT                 Wait · GRAT                Wait · GRAT

                                            24k


                                 N=40k



                                            16k

                                                       9.8M      14M            4.7M     6.9M         2M              10M        1M                5M         500k           2M                 500k          2M       200k            1M
                                                  Wait · GRAT              Wait · GRAT                Wait · GRAT                Wait · GRAT                 Wait · GRAT                 Wait · GRAT                Wait · GRAT

                                            48k


                                 N=80k



                                            32k

                                                        19M      28M              9.4M   14M            5M           20M         2M             10M          1M                5M         500k         2M           200k               2M
                                                  Wait · GRAT              Wait · GRAT                Wait · GRAT                Wait · GRAT                 Wait · GRAT                 Wait · GRAT                Wait · GRAT

                                          600k


                                 N=1M



                                          400k

                                                       240M 340M            100M           200M        50M          200M         20M               200M      10M                100M     5M                   50M          5M         20M


                                                                                                              Mean makespan, Mπ (seconds; log scale)

                                                               Fixed baseline                                                     Race                                                    Specialization

                                     SBVA '23          Kissat '24       AE-Kissat '25           Satsuma '26                     Four-solver race                         Wait · DPR           Wait · VeriPB           Wait · GRAT
                                                                                                                                                                         Hybrid · DPR         Hybrid · VeriPB         Hybrid · GRAT



                                                              Figure 12. Pareto frontier of on-demand runtime strategies. N=5k to N=1M.
                                                                                                                                               Harrison Green, Claire Le Goues, and Fraser Brown


Solving strategies                                                                     Only this strategy      Structure recovered from CNF
     Systematic                 Local / stochastic       Algebraic / structural                                  Logical       Combinatorial      Domain
     Direct / construction      Inference / relaxation   Other / opaque
                                                                                                                  Semantic components / cones                                                        43.2%
    Structural construction / theorem                                                               60.7%                        Problem graphs                                                      41.3%
                                 CDCL                                                               57.5%               Gates / Boolean circuits                                                     38.6%
                  Greedy construction                                                               22.0%               Finite-domain variables                                                      31.4%
              Exhaustive enumeration                                                                21.0%            Cardinality / PB constraints                                                    27.9%
          Native-domain local search                                                                 17.5%                Permutations / orders                                                      24.0%
              Constraint backtracking                                                               16.9%         Arithmetic / modular structure                                                     22.0%
      Circuit / equivalence reasoning                                                               15.7%             Other recovered structure                                                      21.9%
            Cardinality / PB reasoning                                                              15.2%              Equivalence / implication                                                     21.2%
                 WalkSAT-style search                                                               14.3%                Matching / assignment                                                       20.6%
               Other graph algorithms                                                               13.6%                XOR / parity equations                                                      20.5%
            DPLL (no clause learning)                                                                 8.6%          Symmetry / group structure                                                       14.5%
                Weighted local search                                                                 8.6%             State-transition systems                                                       9.7%
          Arithmetic / number theory                                                                  8.5%                  Geometry / packing                                                        8.5%
             Propagation-only solving                                                                 7.8%                     Statistical models                                                     4.9%
                 ProbSAT-style search                                                                  7.1%                                                 0        25          50       75   100
               Tabu search / TabuSAT                                                                   7.1%
                                                                                                                                                                            Solvers (%)
               XOR / GF(2) elimination                                                                6.3%
                   State-space search                                                                 6.0%
                       Matching / flow                                                               4.4%
               Resolution / elimination                                                              4.4%      Figure 14. What representations do specialists recover?
          Meet-in-the-middle search                                                                   3.9%
                Dynamic programming                                                                   3.7%
                  Simulated annealing                                                                 3.5%     Preprocessing and inprocessing
     Stored witness / proof / answer                                                                 3.4%        Before only      Before + during      During only
                    Branch and bound                                                                  2.1%
         Large-neighborhood search                                                                    2.1%                 Root unit simplification                                                  62.4%
                       Other algorithm                                                                2.1%                          Clause cleanup                                                   33.5%
              Look-ahead SAT search                                                                   1.9%                  Cone / core reduction                                                     17.8%
          Belief / survey propagation                                                                 1.9%                Structural strengthening                                                    15.7%
            Input-feature answer rule                                                                 1.8%                    Other preprocessing                                                     14.1%
              GSAT-style greedy flips                                                                 1.8%                  Resolution elimination                                                   13.8%
       Independent random sampling                                                                    1.8%             Self-subsuming resolution                                                     13.6%
          2-SAT / implication solving                                                                 1.8%                 Gate / circuit reduction                                                    13.1%
           Horn / tractable fragments                                                                 1.2%                         Domain filtering                                                    9.2%
                  Novelty-style search                                                                1.2%                    Failed-literal probing                                                   8.6%
           Local search (unspecified)                                                                  1.1%             Cardinality / PB reduction                                                     8.3%
             Population / evolutionary                                                                0.9%              XOR / algebraic reduction                                                       7.8%
     Decision diagrams / compilation                                                                  0.7%                      Literal substitution                                                    7.2%
              Continuous optimization                                                                 0.5%                Problem decomposition                                                          7.1%
      Configuration-checking search                                                                  0.4%                     Variable compaction                                                      6.9%
                                                                                                                               Symmetry breaking                                                       5.8%
                                                0          25           50        75          100
                                                                                                                            Pure-literal elimination                                                   4.2%
                                                                  Solvers (%)                                                 Clause subsumption                                                       2.8%
                                                                                                                                Clause vivification                                                      1.1%
Strategy labels per solver                                                                                             Blocked-clause elimination                                                      0.5%

                                                                                                     81.1%                                                  0        25          50       75   100
                             2+ labels (460)
                                1 label (106)                                                       18.7%                                                                   Solvers (%)

                                 0 labels (1)                                                        0.2%
                                                0          25           50        75          100             Figure 15. What kinds of preprocessing and inprocessing
                                                                  Solvers (%)                                 do specialists do?

          Figure 13. What algorithms do specialists use?                                                       Encoding assumptions and safeguards
                                                                                                                 Encoding assumptions          Recognition / scope   Answer safeguards


D       Extended: Methods and techniques                                                                             Unsupported-case rejection
                                                                                                                        Structural validity guards
                                                                                                                                                                                                     97.2%
                                                                                                                                                                                                     96.3%
                                                                                                                            Relational recognition                                                   94.4%
                                                                                                                     Exact templates / signatures                                                    90.8%
                                                                                                                      Original-CNF model checks                                                      86.4%
                                                                                                                       Multiple encoding variants                                                    65.4%
                                                                                                                     Variable-ID / layout reliance                                                   64.4%
                                                                                                                            Model reconstruction                                                     61.6%
                                                                                                                       Canonicalized recognition                                                     57.7%
                                                                                                                     Rejected-candidate fallback                                                     47.6%
                                                                                                                        Domain / reduced checks                                                      45.9%
                                                                                                                            Clause-order reliance                                                    44.6%
                                                                                                                    Sampled / fingerprint checks                                                      12.7%
                                                                                                                       Stored candidates / proofs                                                      6.2%
                                                                                                                         Certificate / RUP checks                                                      3.7%
                                                                                                                                                            0        25          50       75   100
                                                                                                                                                                            Solvers (%)



                                                                                                              Figure 16. How do specialists decide whether to run or not?
The Case for Automated Hyperspecialization:
Evidence from SAT

 Search tuning                                                                                           Systems-level optimizations
   Branch / phase         Learning / restarts       Local search   Search control                          Input / output   CPU   Memory / state

       Static / occurrence ordering                                                             71.3%                    Compiler / ISA flags                                     99.5%
                 Scheduled restarts                                                            69.3%                    Preallocation / reuse                                     96.5%
      Input-dependent parameters                                                               66.3%             Incremental state updates                                        79.4%
             Bounded search effort                                                             61.2%                  Flat / compact storage                                      75.5%
           Biased / seeded phases                                                               59.1%            Watched / blocking literals                                      68.6%
        Conflict-activity branching                                                            56.4%                     Specialized parsing                                      66.0%
                       Phase saving                                                            51.3%                 Scalar word parallelism                                      59.4%
          Domain-aware branching                                                               46.4%                    Lazy / deferred work                                      51.5%
          Learned-clause retention                                                             45.9%                   Buffered proof output                                       45.1%
               Diverse search starts                                                           44.4%              Bit-count / scan intrinsics                                     39.2%
      Learned-clause minimization                                                              36.5%            Reduced proof-output work                                         38.6%
      Random branch / tie choices                                                              31.2%                   Specialized hot loops                                      32.8%
               Make / break scoring                                                            30.2%                           Lookup tables                                      31.9%
               Noisy move selection                                                            27.0%                 Memory-mapped input                                          25.7%
                  LBD / glue quality                                                           23.3%                     Branchless updates                                        10.1%
       Look-ahead branch scoring                                                               19.4%                        OS memory hints                                         6.9%
                  Stagnation control                                                            15.7%              Compact proof encoding                                           3.7%
                Tabu / recency rules                                                             9.9%           Alignment / cache blocking                                          1.8%
       Adaptive constraint weights                                                               8.6%                           Explicit SIMD                                       1.8%
       Temperature / noise control                                                               8.3%               Branch-prediction hints                                          1.1%
                   Adaptive restarts                                                             6.2%                CPU software prefetch                                         0.2%
                                                0            25         50          75   100                                                    0   25       50        75   100
                                                                   Solvers (%)                                                                           Solvers (%)



      Figure 17. How do specialists tune their search?                                                  Figure 19. What kinds of systems-level optimizations do
                                                                                                        specialists implement?
 Combining solving methods
   Selection / fallback       Composition       Information transfer

               Structural dispatch                                                             93.3%
              Sequential methods                                                               60.1%
       Candidate / phase transfer                                                              39.2%
       Constraint / bound transfer                                                             38.8%
     Separate SAT / UNSAT routes                                                               38.1%
           Size / feature dispatch                                                             37.9%
             General SAT fallback                                                              34.2%
         Repeated configurations                                                               33.0%
                Budgeted handoff                                                               32.8%
          Residual subsolver calls                                                              26.1%
      Unlogged / certifying stages                                                             20.6%
                  Refinement loop                                                              10.2%
         Adaptive effort allocation                                                             4.9%
                                                0            25         50          75   100
                                                                   Solvers (%)



Figure 18. How do specialists combine multiple methods?
                                                                                      Harrison Green, Claire Le Goues, and Fraser Brown


E     Extended: End-to-end deployment                             finite-field multiplier, a 64-bit substitution and permutation
In this section we present full details of the end-to-end de-     block, and 32-input sum and maximum trees, each under
ployment case studies. We study circuit equivalence checking      four rewrites (Table 2). Native is ABC’s cec procedure, which
on OpenTitan [85] and ORFS [105] designs, C verification          combines circuit reasoning with internal SAT solving. Our
with CBMC [22], Rust verification with Kani [27], and depen-      path builds the comparison CNF from the same prepared pair,
dency resolution with Conda [93]. For each case, we train a       runs the specialist, and optionally checks its answer. This
specialist on extracted formulas and select its checkpoint by     measures the equivalence stage, not the whole OpenTitan
validation PAR-2. We then evaluate the generated specialist       verification flow. The limit is 600 seconds per stage, with a
on a new workload and compare it to native performance.           630-second outer guard for native CEC. Ratios are 1.64/1.15
   Specialists were synthesized and evaluated internally in       on all 292 original pairs and 3.47/2.17 on eight of the 16 new
the same mixed infrastructure described previously (§4.1.3).      pairs. The specialist returns unsupported on the eight sum-
All of the redeployment evaluations were measured by run-         tree and maximum-tree cases; native finishes all 16. Thus
ning systems in Docker with one assigned CPU on an AMD            the new-workload gain applies only to the supported half of
EPYC 9454P with networking disabled. We include scripts           the set.
necessary to reproduce these results in our artifact package.
   Native runs use one assigned CPU, three repetitions per
                                                                  Table 2. OpenTitan workload provenance. Counts describe
mode, and 32 GiB of memory, except that Conda uses one
                                                                  the full input sets.
repetition and Kani runs (being more memory-intensive)
use 16 GiB. Shared compilation and circuit preparation are
excluded from timing; encoding, solver interaction, and re-       Input      Source                                               Size
quested checks are included. Note also that in the five case      Formulas   Cryptographic, Ibex, and error-correction      292 CNFs
studies we test, native tools (by default) do not perform inde-              blocks
pendent SAT certificate checking. We evaluate our specialist      Original   Same retained circuit pairs                     292 pairs
both with and without verification.                               New        Multiplier, substitution/permutation, sum        16 pairs
                                                                             and maximum trees
E.1    Case studies
    Æ The rest of this section was generated with
    GPT-6 Astra (xhigh) and provides purely factual
                                                                  E.1.2 ORFS circuit equivalence. System and export.
    details about experimental setup based on the code.
                                                                  OpenROAD-flow-scripts (ORFS) provides scripts and exam-
    It has been completely vetted for correctness by
                                                                  ple designs for hardware implementation. We use its de-
    the human authors.
                                                                  signs for a second circuit-equivalence study. We apply eight
                                                                  synthesis-mapping flows to nine circuit tops from AES, JPEG,
E.1.1 OpenTitan circuit equivalence. System and ex-               and Ethernet designs. Yosys produces reference and revised
port. OpenTitan is an open-source hardware security project.      logic graphs; AIGER’s aigmiter and aigtocnf tools con-
Here we check whether two versions of one of its circuits         struct and export the comparison formulas. Registers are
produce the same outputs (i.e. combinational equivalence          treated as corresponding inputs and outputs, so these are
checking). Our sources are Ascon, Keccak, PRESENT, and            combinational comparisons rather than proofs over arbitrar-
PRINCE cryptographic blocks, the vendored Ibex arithmetic         ily many clock cycles. All 72 distinct formulas are UNSAT,
unit and instruction decoder, and error-correction encoders       with 57 used for training and 15 for validation. The training
and decoders. We use Yosys/Slang to convert their hard-           and validation score ratios are 50.64/28.64 and 72.12/40.42.
ware descriptions into logic graphs and then we apply four
                                                                  Deployment. We use the 72 original circuit pairs and a
ABC rewrite recipes and compare each result with its ref-         new set comprising GCD, FIFO, RISC-V arithmetic-unit, and
erence graph. ABC exports a CNF that asks whether any             UART designs under the same eight mapping flows (Table 3).
input makes the two graphs disagree. These are explicit com-      Native is the Yosys-bundled ABC cec procedure. Our path
parison formulas, rather than copies of ABC’s internal SAT        rebuilds the comparison and CNF, then solves and optionally
queries. We also include deliberate legal configuration mis-
                                                                  checks the answer. Shared synthesis is excluded; the timed
matches. The 296 planned comparisons yield 292 distinct for-
                                                                  task is equivalence checking, not placement, routing, or the
mulas: 272 UNSAT and 20 SAT, split into 233 training and 59       full ORFS flow. Limits match the OpenTitan experiment.
validation formulas. The specialist’s training and validation     All 72 original and 32 new cases finish in both specialist
score ratios are 14.28/11.21 and 13.27/10.38, respectively.       modes. Native-time ratios are 2.16/0.61 on the original set
Deployment. The original workload contains the 292 re-            and 2.81/1.21 on the new set. Checking removes the original-
tained circuit pairs. The new workload contains a 32-bit          workload gain, but the new-workload gain remains.
The Case for Automated Hyperspecialization:
Evidence from SAT

Table 3. ORFS workload provenance. Each source top re-              E.1.4 Rust verification with Kani. System and export.
ceives eight mappings.                                              Kani checks Rust properties by compiling verification har-
                                                                    nesses into CBMC’s program representation. One harness
Input       Source                                         Size     can issue several SAT queries. We use Kani 0.67.0 on all 112
                                                                    harnesses in the s2n-quic CI matrix, covering its codec, core
Formulas    Nine AES, JPEG, and Ethernet tops          72 CNFs
Original    Same mapped circuit pairs                  72 pairs     protocol, and platform crates. A copying wrapper around
New         GCD, FIFO, RISC-V ALU, and UART            32 pairs     external Kissat records each live per-property formula. This
                                                                    produces 302 distinct formulas, split into 241 training and
                                                                    61 validation formulas. Of these, 237 are SAT and 65 are
E.1.3 C verification with CBMC. System and export.                  UNSAT; a SAT query does not by itself mean the overall har-
CBMC checks C code by turning bounded program execu-                ness found a bug. The external interface can encode queries
tions and safety properties into logical constraints. We use        differently from native incremental solving. Training and
AWS C Common’s verification harnesses, which are small              validation score ratios are 1.43/1.74 and 10.54/6.48.
drivers that supply inputs and state the properties to check.
                                                                    Deployment. We rerun the 112 s2n-quic harnesses and test
They cover utilities such as buffers, arrays, hash tables, and
                                                                    14 new harnesses from Hifitime, a Rust time library (Ta-
priority queues. We build all 173 harnesses with CBMC 6.4.0
                                                                    ble 5). Native is Kani’s default CaDiCaL workflow. Our path
and preserve their upstream options. A wrapper copies each
                                                                    uses the external specialist with optional model or GRAT
live CNF at CBMC’s external SAT interface before Kissat an-
                                                                    checks. Each timed invocation checks one harness after its
swers it. A separate export supplies variable names; it does
                                                                    own untimed code-generation warmup. Hifitime uses its
not replace the live query. Six harnesses make no SAT call.
                                                                    required contract and stubbing options and a library build-
The remaining 167 yield distinct UNSAT formulas, split into
                                                                    configuration adjustment; harness bodies are unchanged.
133 training and 34 validation formulas. The training and
                                                                    Original runs have 3600 seconds and 32 GiB; new runs have
validation score ratios are 0.41/0.79 and 1.53/1.93.
                                                                    300 seconds and 16 GiB.
Deployment. The original workload contains the 167 formula-            Ratios are 0.86/0.62 on 109 shared original targets; two
producing AWS proofs, and the new workload contains all             specialist targets time out and another fails during checking.
15 coreJSON proofs (Table 4). We time fresh CBMC runs               Seven Hifitime harnesses make no SAT call and are excluded
from prepared program representations, including symbolic           from solver comparisons. Among the seven that do, native
execution and Boolean encoding. The specialist replaces the         finishes all seven, while the specialist finishes four without
external SAT callback; checked UNSAT answers must pass              checking and three with checking. Three inputs are unsup-
DPR-trim and CakeLPR. Native AWS runs use CBMC 6.4.0                ported, and the checked epoch-equality harness times out.
with MiniSat. Native coreJSON runs follow upstream CI:              Ratios on the three shared targets are 0.76/0.59. Native re-
CBMC 6.3.1, its required contract instrumentation and patch,        mains faster despite the isolated-formula gains. Matching
and per-proof MiniSat, CaDiCaL, or Kissat choices. Original         source harnesses can also produce different later SAT queries
runs have 3600 seconds; new runs have 300 seconds.                  after changing the solver.
   On the 159 original targets shared by both specialist modes,
the ratio is 1.18/0.32. Eight checked targets exhaust CakeLPR’s     Table 5. Kani workload provenance. Seven new harnesses
separate 4-GiB heap. The unchecked specialist finishes all          invoke SAT.
167, but its ratio on that full set is 0.69, so the shared-subset
point does not establish an overall gain. On new targets, na-       Input      Source                                        Size
tive finishes 15, the unchecked specialist 14, and the checked
specialist 13. Ratios on the 13 shared targets are 0.38/0.11;       Formulas   s2n-quic codec, core, and platform       302 CNFs
                                                                               crates
the other specialist runs time out. The validation-formula im-
                                                                    Original   Complete s2n-quic CI matrix          112 harnesses
provement therefore does not carry through to faster native
                                                                    New        Hifitime timescale, general, and      14 harnesses
verification.                                                                  epoch harnesses
Table 4. CBMC workload provenance. Six AWS harnesses
produce no SAT query.
                                                                    E.1.5 Dependency resolution with Conda. System and
Input       Source                                         Size     export. Conda chooses compatible package versions for a
                                                                    software environment. Its classic backend repeatedly calls py-
Formulas    AWS C Common verification harnesses       167 CNFs      cosat while constructing and improving a package plan. We
Original    Same formula-producing AWS proofs        167 proofs
                                                                    run Conda 26.5.3 with pycosat on the EO-datascience and
New         All upstream coreJSON proof targets       15 proofs
                                                                    xESMF environment specifications, using a frozen conda-
                                                                    forge index. We copy the current clauses at every classic
                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


SAT callback, then let the unchanged pycosat path answer.
The 154 calls yield 151 distinct formulas: 105 SAT and 46
UNSAT, split into 120 training and 31 validation formulas.
These include intermediate optimization queries. Training
and validation score ratios are 10.39/3.91 and 11.76/4.83.
Deployment. The original workload reuses those two envi-
ronments. The new workload uses three XROMS CI speci-
fications for Python 3.11–3.13 and Xskillscore’s minimum-
tests specification (Table 6). We time offline environment
planning with conda env create –dry-run, excluding in-
stallation and copying the frozen index. Native baselines
are classic/pycosat and libmamba 2.5.0, a different depen-
dency resolver built on libsolv. The specialist replaces every
SAT callback inside classic Conda; it is not inserted inside
libmamba. Checked answers use model checks or VeriPB/-
CakePB. Original plans have 3600 seconds and new plans
600 seconds.
   Against pycosat, ratios are 1.67/0.84 on both original plans
and 1.20/0.89 on one shared new plan. Against libmamba,
ratios are 0.054/0.027 on both original plans and 0.053/0.040
on two shared new plans. On the four new plans, pycosat fin-
ishes three, libmamba four, and the specialist three without
checking and two with checking. One checked plan takes
599.38 seconds, close to the limit, with only one repetition.
The specialist helps classic Conda without checking on the
shared cases, but libmamba remains much faster. Different
SAT assignments and the omission of pycosat’s propagation-
limit shortcut can change later queries and final package
choices. New environments also share a small initialization
formula with the original corpus.

Table 6. Conda workload provenance. Counts refer to plan-
ning, not installation.

Input      Source                                         Size
Formulas   EO-datascience and xESMF environments     151 CNFs
Original   Same environment specifications             2 plans
New        Three XROMS specifications and              4 plans
           Xskillscore minimum-tests
The Case for Automated Hyperspecialization:
Evidence from SAT

F    Extended: Cross-family sensitivity and
     performance
In Figure 20 we plot cross-family performance of every top
training-selected specialist on every other family (capped at
100 instances).
   Most specialists implement some sort of early detection to
decide whether they are capable of running on a given for-
mula. A family is not attempted only if the specialist returns
UNKNOWN within one second on every sampled instance. Oth-
erwise, it is attempted; the matrix distinguishes attempted
families with no verified solves from those with at least one
verified solve. Incomplete evaluations are excluded from the
coverage counts.
                                                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown



             Cross-family solver performance
                               Relative performance                                     Matrix cells
                               PAR-2 / best for target
                                                                                                                                                                        Transfer
                                                                                           No attempt            Solved; not best                                       coverage
                                                                                           Attempted; no solve   Best (all ties)                                        ≥1 solve
                               1×                   10²×             10⁴×   ≥10⁶×
                               Darker squares indicate lower PAR-2                         Rejected result                                                              0 solves
                           1




                         25




                         50




                         75
  Source solver (rank)




                         100




                         125




                         150




                         175




                         189
                               1                      25               50       75                100               125               150             175     189   0       100      188

                                                                                     Target family (rank)                                                                Families
                                                                                                                                                                        attempted
                                                                                                                                                                    Excludes own family




Figure 20. Cross-family performance of each top solver on up to 100 validation instances from every other family. Each cell
shows the performance of a given specialist solver (y-axis) on a target family. The diagonal shows solver performance on its
own target family. The right panel shows the solver’s transfer coverage: which other families it attempted and had at least one
solve.
The Case for Automated Hyperspecialization:
Evidence from SAT

G     Choice of agent                                                         Encoding                       Year
We conducted a small pilot evaluation (in May 2026) to decide                 Naive (direct)                  —
which base model and harness to use for our experiments.                      Totalizer [8]                  2003
We found that both GPT-5.5 (in Codex) and Claude Opus                         Sequential counter [97]        2005
4.8 (in Claude Code) were able to successfully and consis-                    Sorting network [10, 32]       2006
tently synthesize working specialized solvers, while smaller                  Cardinality network [6, 7]     2009
proprietary models and frontier open-weight models took                       Modulo totalizer [82]          2013
longer and failed more frequently. After GPT-5.6 Sol was re-                  𝑘-modulo totalizer [77]        2015
leased (which has the same pricing as GPT-5.5), we switched
evaluations to use that model.
   Due to the costs associated with running so many agents        Table 7. Cardinality constraint encoding formats tested.
at scale, we limit our evaluation in this paper to a single
representative frontier model. The point of the paper is to
demonstrate an existence proof of the utility of hyperspe-
cialization with frontier models available today. We expect             Í error pattern must contain exactly 𝑘 flipped bits:
                                                                      • The
                                                                         𝑖 𝑒𝑖 = 𝑘.
that future models will continue to improve at both the abil-
                                                                    We sample instances with 105 error bits, 52 parity checks,
ity to write performant solver code and in cost-efficiency,
                                                                 and 𝑘 = 12. Each parity check involves 13 bits. The cardinal-
both axes would continue to make hyperspecialization more
                                                                 ity encoding applies to the single exact-weight constraint;
economically viable. We leave exploration of comprehensive
                                                                 the CNF encoding of the parity checks is fixed across encod-
multi-agent benchmarking to future work.
                                                                 ing methods. All instances are SAT by construction: we plant
                                                                 an error pattern of weight 12 and compute its syndrome.
H      Extended: Cardinality constraint
       encodings                                                 H.1.3 Vertex cover. Vertex cover problems ask whether a
                                                                 graph admits a set of at most 𝑘 vertices containing at least one
Here we present complete details of our cardinality con-
                                                                 endpoint of every edge. A Boolean variable 𝑥 𝑣 represents
straint encoding case study.
                                                                 selecting vertex 𝑣 for the cover. The formula defines the
                                                                 following constraints:
H.1     Benchmark problems
                                                                      • Every edge (𝑢, 𝑣) must have at least one selected
We evaluated hyperspecialization on three crafted bench-
                                                                        endpoint: 𝑥𝑢 ∨ 𝑥 𝑣 .
marks covering both SAT and UNSAT cases and a variety of                                                              Í
                                                                      • The cover must contain at most 𝑘 vertices: 𝑣 𝑥 𝑣 ≤ 𝑘.
formula size ranges.
                                                                    We sample instances with 2,100 vertices, 3,570 edges, and
H.1.1 GPHP. Generalized, capacitated pigeonhole princi-          𝑘 = 1, 330. The cardinality encoding applies to the single
ple problems ask if it is possible to assign pigeons to holes.   global cover-size constraint; each edge contributes one bi-
Unlike the standard framing, holes in the generalized case       nary clause. We construct the graphs by reducing degree-
can accommodate multiple pigeons up to a fixed capacity. A       three Tseitin parity formulas to 3-CNF and then to vertex
Boolean variable 𝑥 𝑝,ℎ represents assigning pigeon 𝑝 to an al-   cover. Even- and odd-charge source instances yield 50 SAT
lowed hole ℎ. The formula defines the following constraints:     and 50 UNSAT instances, respectively.
                                                  Í
    • A pigeon must occupy exactly one hole: ℎ 𝑥 𝑝,ℎ = 1         H.2   Benchmark construction
                                             Í
    • Each hole has at-most-𝑐ℎ capacity: 𝑝 𝑥 𝑝,ℎ ≤ 𝑐ℎ
                                                                 For each benchmark, we sampled 100 formulas, calibrated
  We sample instances with between 17 and 25 pigeons, 6–9        to be hard for baseline solvers, and then encoded these 100
holes, and capacities of 2–4. All instances are UNSAT by         formulas separately with a variety of cardinality encodings
construction: there is always one more pigeon than available     implemented in PySAT [49, 50], listed in Table 7.
capacity.                                                           We split each group of 100 formulas into 80 training in-
                                                                 stances and 20 validation instances (using the same seed) and
H.1.2 LDPC decoding. Low-density parity-check [35] de-           independently synthesize specialists for each benchmark/en-
coding problems ask whether an error pattern can explain an      coding pair (using only GRAT-based specialists for parity
observed parity-check syndrome. A Boolean variable 𝑒𝑖 indi-      with baselines).
cates whether bit 𝑖 was flipped during transmission. Given a
binary parity-check matrix 𝐻 and syndrome 𝑠, the formula         H.3   Results
defines the following constraints:
                                                                 In Figure 8, we present average validation PAR-2 values for
      • The error pattern must satisfy the observed parity       each benchmark/encoding pair, for both baseline solvers and
        checks: 𝐻𝑒 = 𝑠 (mod 2).                                  generated specialists. Here, we examine how these results
                                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


relate to formula size. Figure 21 shows baseline performance,         Formula size and baseline performance
                                                                      Validation PAR-2 (s)                                              SBVA '23            Kissat '24      AE-Kissat '25           Satsuma '26
while Figure 22 shows specialist performance. The x-axis of
                                                                              GPHP                                           LDPC decoding                                  Vertex cover
each subplot is the mean number of variables (top row) or
                                                                              Naive     KM-Tot           Tot.        Sort.   KM-Tot        Tot.            Card.           KM-Tot            Tot.            Seq.
clauses (bottom row).                                                                 Seq.       M-Tot          Card.             M-Tot            Seq.            Sort.            M-Tot            Card.

    Encoding choices substantially affect formula sizes. For           1.2k

the baseline solvers (Figure 21), we see some correlation              600
with performance. Solvers generally perform worse as the               400

number of clauses or variables grows for both GPHP and                        100                            1k                       2k                     6k             10k                                 1m
                                                                                      Mean variables                               Mean variables                                 Mean variables
vertex cover. Indeed this is not surprising. It has been                       Seq.      M-Tot           Tot.        Naive   KM-Tot        Seq.            Sort.           KM-Tot           Card.             Tot.

observed before that encoding size plays a role in solver                         KM-Tot         Card.          Sort.             M-Tot            Card.           Tot.             M-Tot            Seq.

                                                                       1.2k
performance, although it is not the sole factor [1].
    Interestingly, we observe no such clear trend for the spe-         600
cialists (Figure 22). In some cases, the trend is almost reversed.     400
                                                                                 1k                               10k              6k                        15k           100k                              2m
The sequential encoding for GPHP performs the best among                               Mean clauses                                   Mean clauses                                  Mean clauses
all of the baseline solvers but is one of the worst for the spe-
cialist. Conversely, the largest and simplest encoding (naive        Figure 21. Baseline validation PAR-2 versus mean whole-
encoding) is one of the worst for the baselines but yields the       CNF variable count (top row) and clause count (bottom row),
best specialist.                                                     across cardinality encodings. Columns show benchmark
    For LDPC decoding, the 𝑘-modulo totalizer is decisively          groups. Both axes are logarithmic, with a shared time range.
worse than all other formats for the specialists despite being
the newest of the encodings and producing the smallest
formulas in both variables and clauses. Yet for vertex cover,         Formula size and specialist performance
                                                                      Validation PAR-2 (s)
it flips and yields the best specialist.
                                                                              GPHP                                              LDPC decoding                                     Vertex cover
    One potential hypothesis is that there are two competing                                  Tot.                                                                                       M-Tot
                                                                                                                                       KM-Tot
                                                                       1.2k           Seq.                                                                                   3
factors that influence specialist performance: 1. Formulas                                                   Card.       0.01
                                                                                                                                                                                             Tot.

                                                                        30                                                                  Tot.     Sort.                                              Seq.
should be described succinctly in an easily parseable way                             KM-Tot                                                                                0.3
                                                                          1                            Sort.            0.003                                                            KM-Tot
(fancier encodings create more complex structures and aux-                            Naive
                                                                                                                                      M-Tot                Card.                             Card.
                                                                      0.03               M-Tot                          0.001                      Seq.                    0.03
iliary variables which may be harder or slower to parse
                                                                              100                     1k                              2k                    6k                    10k                           1m
consistently). 2. At a certain point, raw formula size does be-                  Mean variables                                    Mean variables                                    Mean variables
come important. For example, vertex cover problems are                        Card.
                                                                                                                                        KM-Tot
                                                                                                                                                                             3
                                                                                                                                                                                            M-Tot
                                                                       1.2k
roughly two orders of magnitude bigger (in bytes) than both                                   Tot.                                                                                                       Tot.
                                                                                                                         0.01
                                                                        30        Seq.                                                               Tot.
the other benchmarks. Here, encodings that save parsing                                                                         M-Tot Card.                                 0.3                     Card.

                                                                          1
                                                                                       KM-Tot
                                                                                                     Sort.              0.003
                                                                                                                                                                                                       Seq.
time (even if more complex) may be worthwhile.                                                        Naive
                                                                                                                                            Sort.                                        KM-Tot
                                                                      0.03 M-Tot                                        0.001     Seq.                                     0.03
    Subsequent exploration is out of scope for this paper, but
                                                                                1k                       10k                          6k                   15k                    100k                       2m
interesting future work could be to develop an understanding                      Mean clauses                                        Mean clauses                                    Mean clauses
of optimal encodings for hyperspecialization (which may be
separate from encodings for general-purpose solvers).                Figure 22. Validation PAR-2 of training-selected specialists
                                                                     versus mean whole-CNF variable count (top row) and clause
I     Extended: Ensuring and evaluating task                         count (bottom row). Filled squares indicate that all 20 valida-
      alignment                                                      tion instances were solved; open squares indicate at least one
                                                                     failure. Both axes are logarithmic; time ranges differ across
Here we describe in detail the objectives of restricted internet
                                                                     benchmark groups.
access (§I.1), how we iteratively improved the agent prompt
and harness before the full evaluation (§I.2) and how we
analyzed runs after the evaluation to ensure compliance              agent from inadvertently leaking information about the with-
(§I.3).                                                              held validation set (since the Global Benchmark Database is
                                                                     a public resource), and thus contaminating the evaluation.
I.1   Agent internet access                                          Therefore, we chose to run all agents with restricted internet
During initial pilot experiments, we experimented with al-           access.
lowing agents to access the internet, with the intuition that           True network isolation would be bulletproof, but would
such a resource would be useful to learn about specialized           also prevent agents from installing runtime packages or other
techniques and (potentially) research information about the          dependencies (which we did want to allow). Therefore, we
specific high-level problem if applicable. While these agents        attempted to enforce the restricted internet access by both
did perform well, we found it near impossible to prevent the         disabling the web_search tools in Codex and by explicitly
The Case for Automated Hyperspecialization:
Evidence from SAT

prompting the agent not to use the internet. We validated         Integrity audit: round 1
that these measures were effective after the fact (§I.3) and
                                                                  Cohort                                                    567 runs
reran any runs which violated these rules (in practice, only
7).                                                                                                                         No lead 339
                                                                  Screens
                                                                                                                            Any lead 228
    In retrospect, however, none of the agents attempted to
                                                                  Trace                                                     Clear 563
install any runtime packages or other dependencies, thus          (Luna)                                                    Candidate 4
this restriction was unnecessary. A more robust solution          Code                                                      Clear 563
would be to properly enforce full network isolation at the        (Luna)                                                    Candidate 4

sandbox level.                                                                                                              Clear 560
                                                                  Cumulative
                                                                                                                            Confirmed 7

                                                                                                                            Clear 560
I.2   Iterative harness and environment development               Final
                                                                                                                            Confirmed 7
                                                                              Initial screen combinations
Our initial agent configuration was intentionally minimal.          None (339)      Code (3)                All three (1)
We started with a simple prompt and Docker environment.             Regex (221)     Regex + trace (3)

We iteratively ran pilot experiments and used Docent [76] to
analyze agent behaviors. Docent is a tool for using language                Figure 23. First round of the integrity audit.
models to scan, summarize, and cluster findings and proved
useful for quickly identifying failure modes and avenues for
                                                                 access. We supplemented this analysis with a deterministic
cheating. We found it very useful for quickly iterating on
                                                                 Python script that searched over the agent-authored com-
framework design and prompt engineering.
                                                                 mands for network-related keywords, including curl/wget,
   As an example, our initial prompt resulted in agents more
                                                                 remote Git operations, HTTP libraries, and package manager
frequently attempting to build general-purpose solvers, so
                                                                 commands. Matching excerpts were provided as evidence
we added language to enforce the task of hyperspecialization.
                                                                 leads to GPT-5.6 Luna (high) during the transcript analysis
We also found that agents would frequently attempt to use
                                                                 on Docent.
certain common command-line tools (jq,ripgrep, time, xz,
gdb, etc...) which were not available in our restricted envi-    B: LLM-based code analysis. We provided GPT-5.6 Luna
ronment, so we updated the environment to include all of         (high) with the full solver source, including build and run
these tools by default.                                          scripts for each run and tasked it with identifying if there
   Initially, our prompt language describing the timeout (that   was evidence of bundling an external solver.
we would run solvers for 10 minutes) was not clear enough,       Cumulative decision. For runs flagged by either the tran-
causing many agents to mistakenly implement their own            script or solver analysis, we gathered the supporting evi-
timeout logic inside their generated solvers, needlessly ter-    dence and prompted GPT-5.6 Sol (high) to determine whether
minating them just before 10 minutes if no solution had          a legitimate violation occurred. All runs labeled as cheating
been found. We were able to use Docent to detect and fix         were manually reviewed and we also spot-checked several
this issue before the full evaluation. Docent also helped us     non-flagged runs.
discover several environment configuration failures, such
as memory-induced crashes in part of the evaluator that          I.3.1 Results. We performed two rounds of analysis. In
pre-checked SAT models (replaced with gratchk), and file         the first round (Figure 23), we analyzed the 567 initial eval-
permission issues when mounting the evaluation dataset in        uation runs (189 families × 3 proof formats). Of these, four
Docker.                                                          candidates were flagged in the trace analysis and another
                                                                 four (with one overlap) in the code analysis. All of these
I.3   Cheating analysis pipeline                                 were marked as confirmed by the aggregator (and human
                                                                 review).
After the full evaluation, we performed a comprehensive
                                                                    After rerunning these seven invalidated runs, we per-
analysis of generated artifacts (transcripts and solver code)
                                                                 formed a second audit on the new seven runs. None of these
to ensure compliance with the intended task. In particular,
                                                                 runs were flagged in either the trace or code analysis. Only
we wanted to ensure that no agent accessed the internet (thus
                                                                 the non-cheating runs were used for data results in this pa-
could not leak information about the withheld validation set)
                                                                 per.
or bundled external solvers as part of the submitted code.
While manually reviewing all transcripts and solver code is
infeasible at scale, we deployed a comprehensive two-part
analysis.
A: LLM-based trace analysis. We uploaded transcripts
to Docent and provided GPT-5.6 Luna (high) a detailed
prompt, tasking it with identifying any evidence of network
                                                            Harrison Green, Claire Le Goues, and Fraser Brown


Integrity audit: round 2
Cohort                                         7 runs

                                               No lead 4
Screens
                                               Any lead 3

Trace
                                               Clear 7
(Luna)

Code
                                               Clear 7
(Luna)

Cumulative                                     Clear 7


Final                                          Clear 7


Initial screen combinations
  None (4)       Regex (3)




         Figure 24. Second round of the integrity audit.
The Case for Automated Hyperspecialization:
Evidence from SAT

J     Complete specialist gallery                                            2d-strip-packing                                                         002
                                                                             46 GBD instances · 10 validation · baseline 10/10
This gallery contains a short description for each of the 189 families
we evaluate on and the three train-selected specialists for each.            2D strip-packing asks whether rectangles can be placed in a strip so no
                                                                             pair overlaps on both axes while encoded capacity and geometry
                                                                             conditions hold. CNF represents axis-overlap relations,
    Æ Note that the content generated in this section was
                                                                             rectangle-to-column incidence, and auxiliary gates enforcing the
    generated by tasking GPT-5.6 Luna (high) with summa-                     required structural constraints.
    rizing both families and solvers. We found no inaccu-
                                                                             Proof format                             No verif.         + verif.    Solved
    racies when spot-checking but it is possible that some                   GRAT                                     0.210 ×          0.424 ×        9/10
    descriptions are slightly inaccurate (although unlikely                  Activity-based watched-literal CDCL branches with a bonus for
    to be egregiously so).                                                   overlap variables, then uses 1-UIP learning, restarts, and clause
                                                                             reduction for general fallback search. It handles only the recognized
Reading the numbers. No verif. is baseline PAR-2 divided by                  encoding schema: SAT assignments are checked clause by clause,
specialist PAR-2; + verif. adds all recorded verification time to both       while UNSAT traces are written as textual DRAT for external
scores before taking the ratio. Values above 1× favor the specialist         elaboration and checking; other inputs return UNKNOWN.
(green); values below 1× favor the baseline (rust); ratios rounding to       DPR                                      0.208 ×          0.424 ×        9/10
1.00× are gray. Bold marks the largest unrounded ratio among the             Overlap-first branching biases watched-literal CDCL toward recovered
three specialists in that family, separately for each timing column          pair-overlap variables before auxiliary variables, with first-UIP
                                                                             learning and standard heuristic fallback. Recognition is limited to the
(including ties). Solved counts verified validation results; failures
                                                                             bounded normalized schema; SAT assignments are checked, while
retain the PAR-2 penalty, so speedups can also reflect differences           UNSAT searches are replayed when needed before emitting textual
in coverage.                                                                 DPR learned-clause and deletion lines; unsupported inputs or proof
                                                                             failures return UNKNOWN.
01-integer-programming                                                001    VeriPB                                   0.616 ×          0.805 ×       10/10
6 GBD instances · 2 validation · baseline 2/2                                Structural-prefix branching prioritizes overlap and incidence variables,
Find a vector of zero-one values that satisfies a system of integer linear   leaving gate variables to propagation and falling back to an unset
equations. The benchmark encodes the equations as CNF using                  suffix variable when needed. 1-UIP learning supports the search; SAT
Boolean circuits, with auxiliary variables representing intermediate         models are checked, while UNSAT emits VeriPB RUP steps and a
computation.                                                                 conclusion, with trimming only in small cases; unsupported inputs or
Proof format                             No verif.     + verif.    Solved
                                                                             model/proof failures return UNKNOWN.
GRAT                                       137 ×      76.8 ×          2/2
Circuit reconstruction extracts XOR rows and recovers the binary             agile                                                                    003
linear system from a prescribed prefix and bounded-input sequential          2,597 GBD instances · 520 validation · baseline 499/520
layout. Meet-in-the-middle handles smaller cases, while wider                The benchmark asks whether a bit-blasted Boolean or bit-vector
bounded searches use projection and local heuristics before CDCL             circuit has an assignment satisfying its CNF encoding. The clauses
fallback. Checked complete assignments yield SAT; unsupported or             express wire aliases, XOR relations, gate definitions, and residual
exhausted searches return UNKNOWN, with no UNSAT certificate                 circuit assertions.
path.
                                                                             Proof format                             No verif.         + verif.    Solved
DPR                                       0.664 ×    0.694 ×          2/2    GRAT                                     0.120 ×          0.125 ×     166/520
Weighted union-find recovers integer rows from a prescribed                  Failed-literal probing, binary-implication congruence, and exact XOR
equivalence-linked circuit layout; exact elimination and bounded             recovery drive shallow split refutations on smaller instances, with a
nullspace search then seek Boolean models. Bit-parallel and                  narrow CDCL fallback. Larger instances receive bounded model trials
lattice-guided searches supplement it, with CDCL after heuristic             and may return UNKNOWN; SAT outputs checked assignments, while
failure. Fallback learning logs witness-free DPR additions; direct SAT       supported UNSAT paths emit DRAT clauses ending in the empty
emits no proof output, and unsupported or internal failures return           clause for external checking.
UNKNOWN, not UNSAT.
                                                                             DPR                                      0.208 ×          0.213 ×     341/520
VeriPB                                     106 ×       10.9 ×         2/2
                                                                             A randomized constructive pass recovers aliases, XORs, and forward
Ordered Boolean-function reconstruction and parity-chain packing             gates to build models, then falls back to bounded elimination, probing,
reduce the recognized CNF to an integer system of common                     and CDCL. Checked SAT models may return before proof content is
bounded-width rows. Modular RREF derives pivots, with direct                 added; UNSAT writes witness-free DPR additions for external
enumeration for small nullity and meet-in-the-middle for larger              checking, while failed checks yield UNKNOWN.
supported nullities. Forward evaluation and clause checking validate
SAT candidates; unsupported shapes or failed searches return                 VeriPB                                   0.100 ×          0.105 ×     98/520
UNKNOWN, with no UNSAT certificate path.                                     A 64-lane bit-parallel circuit simulation samples circuit inputs,
                                                                             enumerating some patterns and assigning deterministic
                                                                             pseudorandom words to others; surviving assignments are expanded
                                                                             and checked. Failure to find a witness is not UNSAT, while eligible
                                                                             residuals use signed-alias quotienting, gate congruence, and CDCL
                                                                             with RUP PB proof output, and other cases return UNKNOWN.
                                                                                                   Harrison Green, Claire Le Goues, and Fraser Brown


algebra                                                               004   alloy-vpn-models                                                    006
8 GBD instances · 2 validation · baseline 0/2                               15 GBD instances · 3 validation · baseline 3/3
The benchmark asks whether two nontrivial binary coefficient vectors        These benchmarks ask whether a Boolean assignment satisfies a
have a product equal to the identity in a table-indexed algebra. CNF        circuit-shaped CNF encoding a relational model, including auxiliary
encodings use pairwise AND variables and XOR constraints requiring          gate variables and one asserted condition. The instances use structured
odd parity in the identity class and even parity in every other product     binary implications and longer gate clauses rather than arbitrary CNF.
class.                                                                      Proof format                             No verif.    + verif.    Solved
Proof format                             No verif.    + verif.     Solved   GRAT                                     0.220 ×     0.222 ×         2/3
GRAT                                       1.00 ×     1.00 ×          0/2   Signed-AND circuit recognition contracts parity-equivalent variables
After recognizing the prescribed CNF layout, it enumerates                  and propagates assignments through a gate DAG, then tries restricted
weight-three supports for one coefficient vector and solves the             searches before a circuit-aware CDCL fallback. SAT assignments are
resulting product constraints for the other with packed GF(2) Gaussian      expanded and checked against the original CNF; a level-0 fallback
elimination. A validated witness yields a complete checked SAT              conflict can emit a DRAT trace for external elaboration, while
assignment; unsupported inputs or failure to find this restricted           unsupported shapes or failed searches return UNKNOWN.
witness return UNKNOWN, with no UNSAT certificate path.                     DPR                                      0.445 ×     0.435 ×         3/3
DPR                                        1.00 ×     1.00 ×          0/2   It reconstructs signed-AND gates with parity union-find, then searches
After recognition, it searches coefficient bits with row and column         leaf representatives using DAG propagation and circuit-aware CDCL.
bitsets, greedy parity-improving flips, restarts, and occasional            A fallback can emit unit and learned clause additions as a DRAT trace
boundary-basis choices. If that incomplete search fails,                    for external elaboration and checking; unsupported encodings or
coefficient-decision CDCL can produce a checked model or record             failed searches return UNKNOWN, while SAT assignments are
DPR additions on a successful UNSAT path; recognition, model                expanded and CNF-checked.
completion, or certification failure returns UNKNOWN.                       VeriPB                                   0.802 ×     0.766 ×         3/3
VeriPB                                    2.00 ×      2.00 ×          1/2   On selected accepted shapes, support-pair gate normalization reorders
Strict structural decoding evaluates a fixed 21-word two-generator          clauses before watched-literal CDCL; other accepted shapes use the
construction over represented inverse pairs and compares its product        generic watched-literal path. SAT assignments are printed as complete
parities with the decoded right-hand side. It reconstructs and checks all   models, but UNSAT has no active certificate path: lower-scope results
auxiliaries before emitting a complete assignment; failed recognition       lack certification and the largest hard-coded scope returns
or construction returns UNKNOWN, with no UNSAT certificate path.            UNKNOWN.

algorithm-equivalence-checking                                       005    antibandwidth                                                       007
36 GBD instances · 8 validation · baseline 4/8                              187 GBD instances · 38 validation · baseline 27/38

The benchmark asks whether a Boolean circuit has an input on which          Antibandwidth asks whether graph vertices can occupy distinct
two represented computations produce different outputs. Tseitin-style       positions so adjacent vertices are far apart by at least w. CNF uses
CNF introduces variables for gate values and asserts an OR of XOR           vertex-position variables, coverage constraints, and clauses forbidding
output differences, so UNSAT corresponds to equivalence for the             edge endpoints from being too close.
encoded pair.                                                               Proof format                             No verif.    + verif.    Solved
Proof format                             No verif.    + verif.     Solved   GRAT                                     0.894 ×     0.931 ×      20/38
GRAT                                      0.619 ×    0.673 ×          1/8   Release-time permutations and focused tabu swaps seek a labeling that
Miter-shape recognition validates the restricted circuit structure, then    separates every edge, guiding exchanges by conflicts and distance
bounded variable elimination simplifies it before watched-literal CDCL      deficits. It validates and emits a completed SAT assignment, but rejects
with first-UIP learning and restarts. Recognition does not establish        other structures as UNKNOWN, has no UNSAT certificate path, and
sorting semantics and unsupported shapes return UNKNOWN;                    may continue without resolving a failed search.
validated SAT assignments are printed, while UNSAT produces a               DPR                                       1.54 ×      1.52 ×      27/38
DRAT-style clause stream.                                                   Capacity-constrained graph coloring, layered ordering, and local
DPR                                      0.689 ×     0.755 ×          2/8   swaps first seek an antibandwidth order; otherwise watched-literal
A narrow gate recognizer accepts only the prescribed gate grammar           CDCL completes the recognized formula. A validated completion
and XOR/OR miter tail, then bounded variable elimination feeds              supplies the SAT certificate; UNSAT uses witness-free direct or learned
watched-literal CDCL. Elimination resolvents and learned clauses are        additions plus an empty clause, while unsupported structures return
emitted as witness-free additions with deletions; contradiction yields      UNKNOWN.
UNSAT, but satisfying results or unsupported inputs return                  VeriPB                                   0.919 ×     0.937 ×      20/38
UNKNOWN.                                                                    Maximum-linear-arrangement seeding and stochastic swap search
VeriPB                                   0.614 ×     0.679 ×          1/8   build a vertex permutation, using min-conflicts and penalty objectives
Exact miter recognition admits only the supported topological               to improve edge separation. It emits a validated SAT assignment; the
XOR/OR shape, then bounded elimination and self-subsuming                   checked recognizer accepts only this structure, bounded search returns
resolution preprocess the CNF before watched-literal CDCL with              UNKNOWN without an ordering, and no UNSAT certificate path is
first-UIP learning. UNSAT paths emit VeriPB resolution and RUP steps;       implemented.
SAT paths print checked assignments, while unsupported shapes or
internal failures return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

argumentation                                                        008   auto-correlation                                                     010
217 GBD instances · 40 validation · baseline 9/40                          51 GBD instances · 11 validation · baseline 2/11
The benchmark asks whether a directed argumentation instance               The benchmark asks whether a binary sequence has bounded aperiodic
admits a conflict-free, defended, or stable set of arguments, or a         autocorrelation or whether two cyclic subsets have constant combined
complete labeling. CNF encodings use status variables and clauses          intersection counts at every nonzero shift. CNF encodings use primary
expressing attacks, defense, coverage, and sometimes exactly-one           variables and auxiliary gates or counters to express these constraints.
choices, though supported layouts are only restricted patterns.            Proof format                             No verif.    + verif.     Solved
Proof format                             No verif.    + verif.   Solved    GRAT                                       1.60 ×     1.60 ×        5/11
GRAT                                     0.970 ×     0.978 ×      7/40     Structural recognition drives multiplier-orbit enumeration and cyclic
Exact recognition of the expected two-label clause layout drives           intersection matching for cyclic subset instances, while tabu bit flips
projection onto in variables, then bounded graph search and                search recognized aperiodic sequence layouts. Smaller cyclic cases use
randomized maximal conflict-free-set repair precede watched-literal        randomized annealing; larger or unsupported cases, low-goal
CDCL. SAT assignments are checked against the original CNF; only           aperiodic cases, and exhausted searches return UNKNOWN, while
this recognized projection can emit an UNSAT certificate, while other      residual WalkSAT completion can produce SAT assignments without
branches seek SAT and failed proof reruns return UNKNOWN.                  an UNSAT certificate path.
DPR                                      0.866 ×     0.872 ×      3/40     DPR                                      0.871 ×     0.871 ×        0/11
Structural recognition of strict two-block and three-block layouts         It searches recognized cyclic subset layouts by enumerating bounded
drives projection onto in variables, followed by bounded graph search      multiplicative-orbit unions and matching cyclic difference signatures,
and randomized maximal conflict-free-set repair before watched-literal     including complementary, swapped, and rotated variants. After fixing
CDCL. SAT assignments are checked against the original CNF; only           primary bits, watched-literal propagation plus an internal full clause
the two-block rerun emits UNSAT, while other layouts or failed             check validate complete SAT assignments; failed recognition or
searches return UNKNOWN, without internally checking that stream.          construction returns UNKNOWN, with no UNSAT or DPR certificate
VeriPB                                   0.936 ×     0.943 ×      6/40     path.
Repeated-block status recovery exposes an attack graph for grounded        VeriPB                                    1.91 ×     1.91 ×         6/11
fixed-point propagation, randomized kernel repair, and compressed          It dispatches recognized aperiodic layouts to correlation-maintaining
CDCL over IN variables. SAT witnesses are checked on the original          simulated annealing with restarts, and cyclic layouts to bounded
CNF; failure to find a stable kernel can return UNKNOWN on weaker          multiplicative-orbit enumeration with hashed meet-in-the-middle
encodings, while only conservative recognized cases emit an UNSAT          autocorrelation matching. Propagation, uniform fills, and residual
proof.                                                                     WalkSAT completion precede full clause verification; unsupported,
                                                                           exhausted, and low-bound aperiodic cases return UNKNOWN, with no
                                                                           general SAT fallback or UNSAT/VeriPB certificate path.
at-least-two-sol                                                     009
18 GBD instances · 4 validation · baseline 2/4
The benchmark asks whether a Boolean CNF formula has at least two          automata-synchronization                                             011
satisfying assignments, rather than merely one. A common encoding          12 GBD instances · 3 validation · baseline 3/3
places two copies of the formula in one CNF, links corresponding           Does a bounded-length word send every state of a complete two-letter
variables with equality indicators, and requires at least one pair to      deterministic automaton to one state? Its time-expanded CNF tracks
differ.                                                                    reachable states and letter choices, propagates transitions, and requires
Proof format                             No verif.    + verif.   Solved    at most one final reachable state.
GRAT                                     0.599 ×     0.688 ×         0/4   Proof format                             No verif.    + verif.     Solved
A bounded 2-CNF implication/SCC search and a permutation-CSP               GRAT                                       21.1 ×     2.21 ×         3/3
search first seek two models after exact layout recognition. Fallback      For recognized inputs, structural Cerny recognition first yields a
watched-literal CDCL uses a blocking clause for the second model;          closed-form word; otherwise bit-packed image-set beams and
unsupported layouts or failure to find that model return UNKNOWN           reverse-BFS pair merging seek a bounded reset word. Candidate words
rather than UNSAT, while only fallback UNSAT paths emit textual            become checked assignments; failed searches invoke bounded
DRAT for external elaboration.                                             small-subset or antichain image-exclusion clauses for external DRAT
DPR                                      0.785 ×     0.883 ×         1/4   elaboration, while unsupported or out-of-bound cases return
An active 2-CNF-plus-wide-clause search and a permutation-CSP              UNKNOWN.
search first seek two models after exact layout recognition. Fallback      DPR                                      0.101 ×     0.134 ×         1/3
watched-literal CDCL uses a blocking clause for another model;             After recognizing the fixed two-letter image-set schema, it tries Cerny
unsupported layouts or failed second-model validation return               detection, image-set beams, greedy pair merging, then watched-literal
UNKNOWN, while UNSAT paths emit witness-free textual DPR clause            CDCL. Direct words become checked assignments; CDCL emits
additions ending in the empty clause, to be elaborated and checked         learned and pair-distance clause additions, reporting UNSAT only after
externally.                                                                a level-zero contradiction. Missing transition clauses disable
VeriPB                                   0.599 ×     0.688 ×         0/4   pair-distance preprocessing, and unsupported or uncertified cases
An AIG structural-hashing shortcut and bounded Davis-Putnam                return UNKNOWN.
elimination target selected UNSAT cases, retaining information for         VeriPB                                     489 ×     26.7 ×          3/3
RUP replay and model extension. Fallback component-wise                    After recognizing the reachable-subset encoding, it uses Cerny
watched-literal CDCL finds one model, blocks it, and seeks a second;       threshold dispatch and exact-encoding interval reasoning, then falls
checked witnesses are accepted, while failed recognition or                back to duplicate-eliminating bit-parallel beams. If searches find no
second-model search returns UNKNOWN and UNSAT paths close                  word, bounded pair/triple-distance reasoning emits VeriPB proofs; SAT
with VeriPB RUP certificates.                                              assignments are clause-checked, but the solver does not validate proof
                                                                           files and unsupported or unproved cases return UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


baseball-lineup                                                     012    belpyramid-puzzle                                                   014
40 GBD instances · 8 validation · baseline 7/8                             57 GBD instances · 12 validation · baseline 6/12
The benchmark asks whether exactly K items can be selected so that         These instances ask whether two Boolean networks with shared inputs
every binary attribute receives at least its required coverage. Its CNF    differ on some output. CNF clauses encode AND gates and output
encodes the selection, item-attribute incidence, and cardinality or        comparisons; a required mismatch makes SAT witness inequivalence
coverage counts with auxiliary variables and sequential counters.          and UNSAT indicate equivalence; this is not every possible encoding.
Proof format                             No verif.    + verif.    Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                      1.98 ×      1.94 ×        7/8    GRAT                                      0.638 ×    0.795 ×        1/12
After recognizing the row-mask-counter schema, weighted                    RUP-checked simulation lemmas drive solving on normalized AIG
randomized greedy selection with targeted min-conflicts swaps drives       miters, with multiword signatures proposing equivalences before a
the primary search. It falls back to a bounded DPLL tree; availability     monolithic watched-literal CDCL fallback. First-UIP learning and
conflicts emit RUP-style units and an empty clause, while unresolved       reason minimization support fallback search; SAT models are checked,
cases return UNKNOWN. SAT assignments reconstruct auxiliaries and          the pyramid branch returns UNKNOWN, and UNSAT emits textual
are checked against all input clauses.                                     DRUP-style additions for external checking.
DPR                                        1.98 ×     1.65 ×        7/8    DPR                                      0.698 ×     0.870 ×        2/12
Strict row-mask-counter recognition precedes deficit-weighted greedy       Signature-guided equivalence sweeping drives incremental
selection with restarts and swap-delta improvement. Failure triggers       assumption-based CDCL on a recognized AND-miter layout.
exact row conflict search only for small K; larger unresolved cases        Multiword signatures propose equivalent or complementary variables,
return UNKNOWN. UNSAT uses sparse-column units or conflict                 with a complementary-input prepass; bounded queries retain learned
refutations, may add witness-free clauses, and is not internally           clauses and final conflicts emit proof clauses, while failed searches or
verified; SAT models are clause-checked.                                   unsupported layouts return UNKNOWN without a SAT witness.
VeriPB                                   0.992 ×     0.993 ×        6/8    VeriPB                                   0.690 ×     0.825 ×       2/12
Scarcity-weighted greedy search with breakout swaps follows strict         Comparator-cone probing leads the compact-miter search: assumed
incidence-counter recovery. Failure falls back to a bounded                output mismatches are tested with restricted watched-literal CDCL,
primary-variable tree, then weighted PB separation with lifted-counter     then the full miter receives unrestricted CDCL. Learned clauses
proof logging; bounded or unsupported cases return UNKNOWN. SAT            remain global and UNSAT is logged with VeriPB RUP records, but
candidates are clause-checked; UNSAT emits RUP or PB derivations,          rejected finite-domain layouts and all non-UNSAT outcomes return
including deficient-support contradictions.                                UNKNOWN without a SAT witness.

battleship                                                          013    binary-pigeon-hole                                                  015
45 GBD instances · 9 validation · baseline 8/9                             5 GBD instances · 1 validation · baseline 0/1

The benchmark asks whether selected cyclic modular lines cover every       Binary pigeon-hole CNFs ask whether p pigeons can be assigned
point of an n-by-n toroidal board. It encodes line choices with Boolean    distinct holes using binary codes. A direct encoding gives each pigeon
variables, coverage clauses for every point, and within-block              a bit block, excludes unused codes, and forbids two pigeons from
at-most-one clauses.                                                       sharing a valid code.
Proof format                             No verif.    + verif.    Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                       421 ×      35.4 ×        9/9    GRAT                                      4,340 ×     1.40 ×         1/1
A direct square proof handles complete square instances, while             Exact structural recognition replaces general SAT search. For
bounded prime-power construction and weighted min-conflicts seek           recognized formulas, it translates codes into unary membership and
checked SAT assignments elsewhere. If these searches fail,                 capacity constraints, repeatedly reduces pigeon-hole instances with
affine-symmetry lifting or watched-literal CDCL can emit DRAT traces       fresh bridge variables, and emits an empty clause in a DRAT-style
for applicable cases; unsupported or unresolved inputs return              stream for external elaboration and checking. Recognition or
UNKNOWN, and UNSAT requires successful proof generation.                   proof-writing failure returns UNKNOWN.
DPR                                      0.414 ×     0.420 ×        6/9    DPR                                       3,170 ×    0.620 ×         1/1
Compressed-word min-conflicts tracks line coverage with exact deltas       Exact recognition of the complete direct encoding drives a specialized
and restarts, trying one permitted omitted pair with both rows forced      path without general search. SAT assigns pigeon i code i and rechecks
before one-row search unless its negative-case guard applies. After        the clauses; UNSAT adds exact-code indicators and unary pigeon-hole
heuristic failure, bounded unit propagation emits a DPR-style stream       constraints, then uses witness-free clause additions and
with witness-free additions; limits or unsupported layouts return          propagation-redundancy symmetry steps to reach an empty clause;
UNKNOWN.                                                                   unsupported cases return UNKNOWN.
VeriPB                               2.49·104 ×      4,470 ×        9/9    VeriPB                               3.51·104 ×       264 ×          1/1
A direct cutting-planes contradiction handles complete square              Exact canonical-encoding recognition, including an order-independent
instances, while a prime-field two-affine-pencil construction supplies     retry, and a binary-code assignment shortcut replace general SAT
checked SAT assignments on qualifying complete instances.                  search. SAT assigns pigeon i code i and checks clauses; UNSAT emits a
Otherwise grouped set-cover min-conflicts uses coverage counts, tabu       VeriPB certificate with exact-code indicators, per-hole pseudo-Boolean
moves, and bounded restarts before selected CDCL fallbacks;                capacity derivations, and per-pigeon binary resolution trees;
specialized proof routes certify limited UNSAT cases, while unresolved     unsupported inputs or proof-generation failures return UNKNOWN.
recognized inputs return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

binary-tree-parity                                                    016    bitvector                                                             018
2 GBD instances · 1 validation · baseline 0/1                                594 GBD instances · 119 validation · baseline 49/119
These instances ask whether a Boolean assignment satisfies                   The benchmark asks whether a Boolean assignment can satisfy a CNF
three-variable parity equations whose supports form two full binary          encoding of quantifier-free bit-vector constraints, with variables
trees, possibly in different variable orderings. In CNF, each equation is    representing bit values and circuit intermediates. Clauses enforce
represented by clauses forbidding the four assignments of one parity,        translated operations and asserted constraints.
with some instances allowing a shortened block.                              Proof format                             No verif.       + verif.   Solved
Proof format                             No verif.       + verif.   Solved   GRAT                                     0.739 ×        0.855 ×     20/119
GRAT                                  7.42·105 ×     3.23·105 ×       1/1    It recognizes local gate blocks and, when coverage is sufficient, tries
Packed GF(2) Gaussian elimination solves recognized parity groups,           bit-parallel functional-block search; otherwise it uses watched-literal
with bounded affine-space enumeration and direct checking of                 CDCL with activity branching, 1-UIP learning, restarts, and clause
candidates against the CNF. It falls back to order-independent               reduction. SAT models are rechecked, while UNSAT is represented by
matching for shortened gates; SAT emits a checked assignment, while          textual DRAT additions for external elaboration; failures can return
unsupported or unsuccessful cases return UNKNOWN because no                  UNKNOWN.
UNSAT certificate path is implemented.                                       DPR                                      0.737 ×        0.846 ×     21/119
DPR                                   3.21·105 ×     6.25·104 ×       1/1    Local gate-pattern detection supplies only a heap tie-break, not
Exact recognition of the gate order and orientation precedes packed          bit-vector or XOR reasoning; the solver otherwise runs generic
GF(2) Gaussian elimination and bounded Gray-code enumeration of              watched-literal first-UIP CDCL with phase saving and restarts. Its
affine solutions, with SAT candidates checked against clauses. It retries    addition-only proof records learned clauses and the empty clause at
weakened gates by fixing the omitted-clause assignment and attempts          root conflict, while SAT models are checked and printed separately,
Davis-Putnam refutation only for small no-model cases; unsupported           not in the proof.
or uncertified outcomes return UNKNOWN.                                      VeriPB                                   0.756 ×        0.852 ×     23/119
VeriPB                                3.17·105 ×     6.39·104 ×       1/1    Root failed-literal probing and bounded proof-logged variable
Affine reduction through the recognized first tree produces a packed         elimination precede generic watched-literal first-UIP CDCL; no
GF(2) system for the second. It also enumerates bounded                      bit-vector semantics are used. SAT assignments are independently
shortened-gate branches and checks candidates against the CNF.               checked, while UNSAT emits VeriPB RUP steps, deletions, and a final
Failed-literal propagation yields UNSAT only on a RUP contradiction;         empty clause, with parsing, checking, or proof-writing failures
failed or unsupported cases return UNKNOWN, while SAT emits a                yielding UNKNOWN.
checked assignment.
                                                                             bounded-model-checking                                                019
bioinformatics                                                        017    31 GBD instances · 7 validation · baseline 7/7
61 GBD instances · 13 validation · baseline 10/13                            These benchmarks ask whether a Boolean assignment satisfies a
The benchmark asks whether Boolean variables satisfy a structured set        Tseitin-encoded circuit check. Variables represent circuit or state
of constraints; some instances organize them as one-of-many choices          signals, and CNF clauses impose local gate and checking constraints.
at positions with compatibility or circuit conditions. CNF uses one-hot      Proof format                             No verif.       + verif.   Solved
clauses and auxiliary Tseitin variables, but these recognized shapes do      GRAT                                    0.0612 ×       0.0605 ×        7/7
not define every possible encoding.                                          It recognizes dense Tseitin-like AND/OR and XOR/XNOR structure,
Proof format                             No verif.       + verif.   Solved   then applies bounded elimination to gate outputs; unsupported shapes
GRAT                                      0.461 ×       0.691 ×      6/13    return UNKNOWN rather than invoking general search. CDCL with
Conservative XITS recognition enables canonical partition branching          first-UIP learning is the fallback, emitting DRAT additions for external
in small-class cases; other inputs use activity-ordered first-UIP CDCL,      elaboration on UNSAT and checking reconstructed SAT models
with failed-literal probing and bounded elimination only on the              against the original clauses.
generic path. Checked SAT models are printed, while reported UNSAT           DPR                                     0.0549 ×       0.0390 ×        7/7
is accompanied by textual DRAT ending in an empty clause;                    It starts with reverse-order bounded variable elimination, retaining
unresolved search or reconstruction failure returns UNKNOWN.                 non-tautological resolvents and recording eliminated values for
DPR                                       0.362 ×       0.532 ×      4/13    reconstruction; watched-literal CDCL with first-UIP learning is the
Bounded Davis-Putnam elimination protects the one-hot and counter            fallback when no contradiction appears. UNSAT uses addition-only
prefix; Xits cases also bias state choices and probe same-state pairs        RUP-style clause additions, while reconstructed SAT assignments are
before CDCL fallback. SAT assignments are reconstructed and                  checked against original clauses; failed reconstruction or validation
checked; internal UNSAT is logged with preprocessing and learned             returns UNKNOWN, and proof logging is configurable.
clauses plus an empty clause for external DPR elaboration, while             VeriPB                                  0.0471 ×       0.0168 ×        7/7
unrecognized inputs or failed checks return UNKNOWN.                         It begins with parity-DSU substitution and conservative gate hashing,
VeriPB                                   0.485 ×        0.436 ×      6/13    adding bounded elimination only for a recognized signature;
Detected Xits shapes activate positive phases on choice blocks,              unrecognized or malformed inputs return UNKNOWN. CDCL with
Xits-gated minimization, and learned-clause reduction; other inputs          first-UIP learning is the fallback, with UNSAT logged as augmented
use activity-based first-UIP CDCL with phase saving and Luby restarts.       VeriPB RUP additions and reconstructed SAT assignments checked
Checked SAT assignments are printed, while UNSAT requires written            against the original CNF.
VeriPB RUP records ending in an empty record; parse, check, or
proof-write failure returns UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


brent-equations                                                     020    cellular-automata                                                    022
20 GBD instances · 4 validation · baseline 3/4                             52 GBD instances · 11 validation · baseline 8/11
These benchmarks ask whether the 3 by 3 matrix-multiplication tensor       These benchmarks ask whether a cyclic binary row has a predecessor
over GF(2) has a rank-r decomposition into binary factor vectors. A        trajectory under a local cellular-automaton rule for T steps ending in
Tseitin-style CNF represents products and XOR accumulation, yielding       prescribed values. CNF represents cell states by time layer, links local
729 parity equations that describe the tensor.                             neighborhoods with transition clauses, and fixes terminal values with
Proof format                             No verif.    + verif.    Solved   unit clauses.
GRAT                                       1.06 ×     1.06 ×         3/4   Proof format                             No verif.    + verif.     Solved
A 26-term Strassen-style construction drives recognized unfixed            GRAT                                      1.29 ×      1.44 ×        9/11
high-rank cases, while fixed cases use DSU component decomposition,        Backward traversal of recognized layered gates biases search from the
bounded multi-choice search, and bipartite matching after                  fixed terminal row, while a shallow clause-width SPG heuristic tries
gate-network recognition. Incremental residual local search handles        sequential phase passes before the generic watched-literal CDCL
eligible high-rank failures; clause-checked SAT assignments are            fallback. SAT assignments are checked; UNSAT results use textual
emitted, but no UNSAT certificate path exists and unsuccessful cases       DRAT additions, with recognized-path clauses replayed
return UNKNOWN.                                                            chronologically, while an exhausted SPG budget returns UNKNOWN.
DPR                                       1.06 ×      1.06 ×         3/4   DPR                                      0.455 ×     0.520 ×        2/11
XOR-root monomial flattening and bipartite matching first construct a      Structural clause-width dispatch selects bounded and deterministic
primary assignment for recognized high-rank encodings. When direct         phase passes for non-ECA layouts, then falls back to watched-literal
construction fails, an open-ended weighted WalkSAT search may              CDCL with first-UIP learning; recognized ECA layouts return
precede watched-literal CDCL; SAT assignments are checked and              UNKNOWN unless ECA_CDCL enables ordinary CDCL, with no
emitted, while unsupported, low-rank, or UNSAT cases return                specialized reverse-search path. SAT assignments are checked, while
UNKNOWN and no UNSAT certificate path is implemented.                      UNSAT learning is emitted as witness-free DPR additions, including
VeriPB                                     1.06 ×     1.06 ×        3/4    the empty clause.
Direct reconstruction of the fixed generator schedule drives sparse        VeriPB                                   0.692 ×     0.698 ×        6/11
rank-one completion; substituted dense cases use bit-parallel tabu         Recognized Rule-110 layouts first try a cyclic-predecessor check, then
search with incremental deltas and repair. Watched-literal CDCL            use backward row-biased CDCL; population signatures may activate
follows failed direct searches; clause-checked SAT assignments are         bounded elimination, while unrecognized inputs return UNKNOWN.
emitted, but low-rank, contradictory, or failed searches return            Tracked UNSAT replay emits VeriPB RUP dependencies and an empty
UNKNOWN and no UNSAT certificate path exists.                              conclusion, while direct predecessor derivations are limited to targets
                                                                           without a cyclic one-step predecessor; SAT assignments are checked.
cardinality-constraints                                             021
17 GBD instances · 4 validation · baseline 4/4                             circuit-equialence-checking                                          023
The benchmark asks whether at most K lattice points can hit every          19 GBD instances · 4 validation · baseline 0/4
specified geometric object, such as a square or triangle. CNF uses         The benchmark asks whether two Boolean circuits compute the same
Boolean variables for point selections, clauses requiring each object to   function. A CNF miter combines their outputs with an XOR and forces
be hit, and auxiliary clauses encoding the at-most-K bound.                it true, so SAT gives a distinguishing input while UNSAT establishes
Proof format                             No verif.    + verif.    Solved   equivalence for the gate encoding.
GRAT                                     0.506 ×     0.779 ×         3/4   Proof format                             No verif.    + verif.     Solved
Incidence recognition drives a canonical hitting-set witness for aligned   GRAT                                      1.00 ×      1.00 ×         0/4
squares, with min-conflicts as a SAT fallback; propagation completes       Strict LUT/miter recognition drives bit-parallel simulation of small
the model before checking it. For arbitrary squares and aligned            root supports, checking any distinguishing assignment against the
triangles, mapped templates or DRAT-producing 1-UIP CDCL handle            original clauses. Watched-literal DPLL handles larger supported roots
UNSAT; aligned squares lack a CDCL fallback, and unsupported or            and logs learned or cube-blocking clauses as textual DRAT additions,
failed paths return UNKNOWN.                                               ending UNSAT with an empty clause; unsupported layouts or
DPR                                      0.301 ×     0.633 ×         2/4   excessive support return UNKNOWN.
Bounded geometric regeneration and weighted min-conflicts construct        DPR                                       1.00 ×      1.00 ×         0/4
a capped hitting set; propagation then completes and checks the            Semantic sweeping groups equal or complemented signals using
original CNF for SAT. On failure, bounded resolution elimination feeds     bit-parallel truth-table simulation, then tests candidate implications by
GenericCDCL, whose resolution and learned-clause additions support         propagation and RUP. Common-cut lemmas and bounded CDCL add
an UNSAT certificate; unsupported or altered inputs, or failure of that    witness-free clause additions, ending proved UNSAT with an empty
path, return UNKNOWN.                                                      clause; bounded failure returns UNKNOWN, and SAT models are
VeriPB                                   0.302 ×     0.633 ×        2/4    checked.
Fixed-cardinality simulated annealing searches recognized exact            VeriPB                                    1.00 ×     1.00 ×          0/4
geometric layouts while maintaining unhit objects; unit propagation        Packed signatures find equal or complemented candidate
and small recursive DPLL then complete the assignment and check            correspondences, certified first by bounded parity-DSU exact cuts with
every original clause. No UNSAT certificate path is active: recognition,   bit-parallel evaluation. Relevant-cone CDCL falls back when cuts fail,
construction, or completion failure returns UNKNOWN.                       reusing proved pairs and logging RUP or polynomial-resolution steps;
                                                                           internal SAT only rejects candidates, no SAT assignment is emitted,
                                                                           and unsupported or unproved roots return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

circuit-equivalence-checking                                       024    circuit-multiplier                                                  026
20 GBD instances · 4 validation · baseline 1/4                            20 GBD instances · 4 validation · baseline 2/4
The benchmark asks whether two Boolean circuit signals agree on           The benchmark asks whether two nontrivial positive binary numbers,
every shared input assignment. Gate relations are encoded in CNF and      represented little-endian, can multiply to the fixed target encoded by
a difference (XOR) output is asserted, so SAT supplies a                  the instance. CNF clauses constrain operand bits and auxiliary
counterexample and UNSAT establishes equivalence.                         multiplier, adder, and carry wires so an assignment realizes that
Proof format                             No verif.    + verif.   Solved   product.
GRAT                                      3.01 ×     3.07 ×        3/4    Proof format                             No verif.    + verif.    Solved
Bit-parallel SAT sweeping leads the search: signatures on a recognized    GRAT                                     0.789 ×     0.789 ×         1/4
acyclic LUT network propose equal or complemented signals, and            Watched-literal CDCL is the active engine, with first-UIP learning,
CDCL assumptions test them against counterexamples. Bounded               restarts, rephasing, and clause reduction after a syntactic two-block
functional search covers exceptional inputs; fallback CDCL logs           check. SAT models are checked against the original CNF; closed
textual DRAT for external checks on UNSAT, while unsupported              non-SAT searches return UNKNOWN because no retained DRAT
inputs return UNKNOWN and SAT yields a checked model.                     proof is produced.
DPR                                        1.52 ×     1.56 ×       2/4    DPR                                      0.620 ×     0.620 ×         0/4
Assumption-based relation queries lead the search: incremental            Structural recognition admits only the documented operand blocks
watched-literal CDCL tests candidate signal equalities from a bounded     and circuit layout; malformed or unmatched inputs return
signature sweep, with counterexamples refining the signatures before      UNKNOWN without generic SAT fallback. ProbSAT-style local search
final fanin queries. Failed candidates are discarded; unsupported or      tracks unsatisfied clauses and break counts, then falls back to
uncertifiable encodings return UNKNOWN, SAT gives a checked               watched-literal CDCL for checked SAT models and witness-free DPR
model, and only the final UNSAT path emits a dependency-tracked           additions plus a root-contradiction marker on UNSAT.
RUP proof core.                                                           VeriPB                                   0.757 ×     0.757 ×        1/4
VeriPB                                   0.763 ×     0.782 ×       0/4    Bounded variable elimination follows strict recognition, removes only
Bit-parallel simulation leads: replayed lanes can produce                 internal variables while protecting operand words, and retains
clause-checked SAT models; otherwise bounded gate elimination feeds       reverse-reconstruction records; unmatched inputs return UNKNOWN.
embedded CDCL, whose UNSAT path logs a VeriPB proof with RUP              Residual watched-literal CDCL uses first-UIP learning and restarts;
constraints and an empty clause, while fallback SAT is not checked        reconstructed SAT models are checked against the original CNF, while
against the original formula and nonmatching encodings return             internal UNSAT returns UNKNOWN without a VeriPB refutation.
UNKNOWN.
                                                                          clique-coloring                                                     027
circuit-minimization                                               025    15 GBD instances · 3 validation · baseline 3/3
50 GBD instances · 10 validation · baseline 0/10                          The CNF asks whether some edge assignment contains k distinct
Structured circuit-minimization encodings ask whether exactly a           selected vertices forming a clique and assigns every vertex a color so
prescribed number of Boolean candidates can cover every                   adjacent vertices differ. Edge, selection, and color variables encode
requirement; selector clauses express coverage, and Tseitin               these conditions with exactly-one, distinctness, and incompatibility
population-count clauses enforce the exact cardinality.                   clauses.
Proof format                             No verif.    + verif.   Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                       9.95 ×    9.95 ×       9/10    GRAT                                      31.1 ×      2.30 ×         3/3
Structural recognition and population-counter probing recover             Exact schema recognition and closed-form model construction are the
candidate phases and the exact cover size, with a per-bit fallback.       active techniques. Its SAT branch checks a complete assignment; when
Weighted greedy cover search uses focused exchanges and changing          k>c, it emits a DRAT proof with fresh variables and a Hall-style
target weights; counter propagation completes SAT models, whose           pigeonhole refutation, while unrecognized or unsupported cases
original clauses are checked, while unsupported or unsuccessful cases     return UNKNOWN instead of using generic search.
return UNKNOWN without an UNSAT certificate path.                         DPR                                        10.7 ×    0.330 ×         3/3
DPR                                       9.97 ×      9.92 ×      9/10    Exact schema recognition gates both branches. When k>c,
Phase normalization identifies candidate inputs and cover constraints,    fresh-variable, witness-free clause additions and a subset-Hall
while bounded cardinality probing recovers the target size in two         refutation provide the UNSAT certificate; in the constructive regime, it
exact layouts. A randomized weighted add/remove search seeks the          constructs and checks a closed-form clique-coloring assignment.
fixed-cardinality cover, then bounded propagation/DPLL completes          Unrecognized or unsupported cases return UNKNOWN rather than
variables; checked SAT assignments are emitted, but failed or             invoking generic search.
unsupported cases return UNKNOWN because no UNSAT certificate             VeriPB                                     26.4 ×    0.513 ×        3/3
path exists.                                                              Streaming recognition and direct model checking lead the solver. It
VeriPB                                     9.94 ×     9.88 ×      9/10    constructs a checked SAT assignment when k<=n and c>=k;
Recognition of two exact signatures recovers selector phases, cover       otherwise it emits bounded pseudo-Boolean proofs for n<k or k>c
rows, and target cardinality from the population-count core, with         using position-pigeonhole reasoning or vertex symmetry, RUP, and
repair for a shortened-gate variant. Weighted fixed-cardinality search    cutting planes, while recognition or guard failures return UNKNOWN
focuses on uncovered rows and scores swaps with tabu diversification;     without general search.
clause-checked candidates yield SAT models, while failed or
unsupported cases return UNKNOWN without an UNSAT path.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


clique-formulas                                                     028    clustered-random                                                     030
4 GBD instances · 1 validation · baseline 1/1                              43 GBD instances · 9 validation · baseline 8/9
The benchmark asks whether k ordered positions can choose vertices         The benchmark asks whether a Boolean assignment satisfies every
from different parts of a complete multipartite graph. Its CNF has one     clause in a uniform 3- or 4-CNF formula whose clauses are arranged in
positive choice clause per position and binary clauses forbidding two      overlapping clusters on limited variable supports. It represents a
choices in one position or the same part.                                  restricted clustered random SAT structure, not every possible
Proof format                             No verif.   + verif.     Solved   encoding.
GRAT                                        447 ×    47.9 ×          1/1   Proof format                             No verif.      + verif.   Solved
Cross-row forbidden-neighbor signatures reconstruct rows and parts,        GRAT                                     0.379 ×       0.498 ×        6/9
followed by an exact conflict audit for the balanced encoding. It checks   Focused local search with occurrence counters and bounded Hamming
a complete SAT assignment when positions fit the parts; otherwise, for     repair comes first, followed by watched-literal CDCL when no verified
at most 16 parts, it writes a DRAT certificate for external elaboration    assignment is found. SAT returns a checked complete assignment;
and checking using OR definitions and subset-Hall clauses, while           only the fallback logs learned clauses and an empty clause as a DRAT
unsupported cases return UNKNOWN.                                          trace for external elaboration, while unsupported input or
DPR                                        820 ×     17.9 ×          1/1   reconstruction failure returns UNKNOWN.
DSU recognition recovers selector positions and parts, requiring the       DPR                                      0.481 ×       0.616 ×        7/9
balanced clone encoding and full incompatibility set rather than           Factor-local exhaustive repair and stochastic local search with
general search. It checks a SAT assignment when positions fit              belief-propagation decimation for width-4 cases precede
recovered parts; otherwise it emits a DPR refutation with                  factor-resolution clauses, bounded Davis-Putnam elimination, and
clone-collapse additions and a pigeonhole sequence, while                  watched-literal CDCL fallback. SAT exits return checked assignments,
unsupported inputs or failed checks return UNKNOWN.                        whereas only the fallback emits witness-free RUP-style clause
VeriPB                                     735 ×     9.00 ×         1/1    additions toward an UNSAT derivation; unsupported inputs return
Twin-variable representative reduction and whole-part symmetry             UNKNOWN.
breaking compress the recognized balanced, auxiliary-free encoding         VeriPB                                   0.470 ×       0.336 ×        7/9
instead of general clique search. It checks a SAT assignment when          Focused probSAT-style walking leads the search, with
positions fit the parts; otherwise it writes a VeriPB proof ending in a    consensus-derived clauses on width-4 instances; failure triggers
RUP contradiction without verifying that proof; unsupported inputs or      first-UIP CDCL with same-support consensus, bounded elimination,
failures in model checks or proof output return UNKNOWN.                   and a selective failed-literal pass. SAT returns a checked assignment,
                                                                           while UNSAT is certified through sliced VeriPB RUP steps;
                                                                           unsupported inputs or internal errors return UNKNOWN.
clique-width                                                        029
27 GBD instances · 6 validation · baseline 1/6
The benchmark asks whether a recovered graph can be built through n        coloring                                                             031
stages using at most k temporary labels, with each stage recording         594 GBD instances · 119 validation · baseline 58/119
component relations, label choices, and graph constraints. These           The benchmark asks whether each graph vertex can receive a color
construction choices are represented by CNF variables and clauses.         while respecting every encoded incompatibility between endpoint
Proof format                             No verif.   + verif.     Solved   choices. These constraints are translated into CNF using compact
GRAT                                      1.00 ×     1.00 ×          1/6   Boolean codes or one-hot choices in the recognized instances, rather
                                                                           than one universal coloring encoding.
A partition-state merge search tries forest-postorder,
linear-neighborhood, and beam-bounded general constructions,               Proof format                             No verif.      + verif.   Solved
pruning merges by outside-neighborhood signatures and implication          GRAT                                     0.776 ×       0.784 ×     38/119
conflicts; reused-label enumeration is an active fallback. The narrow      Strict recognizers send compact cases through bit-mask forward
recognized layout is required; structural assignments receive              checking, with small-domain branching and impact-based state
SCC-based 2-SAT completion and full clause checking, while search or       ordering; one-hot cases use CDCL directly. SAT assignments are
checking failure returns UNKNOWN and no UNSAT certificate is               checked against the CNF; failed bounded searches use CDCL or
emitted.                                                                   elimination, emitting DRAT clause additions for UNSAT, while
DPR                                        1.00 ×    1.00 ×          1/6   unresolved cases return UNKNOWN.
A capped linear-order DFS seeks a graph ordering; success adds             DPR                                      0.845 ×       0.854 ×     44/119
relation literals, while failure or cap exhaustion sends a binary normal   Incidence-signature recognition reduces supported compact encodings
form with representatives and Sinz-style counters to watched-literal       to finite-domain masks and binary support tables, followed by arc
CDCL. Only a narrow normalized layout is recognized; 32-bit masks          consistency and tabu/min-conflicts search. Validated assignments
limit support, and failed or unsupported cases return UNKNOWN              provide SAT witnesses; eligible failures fall back to watched-literal
without an UNSAT or DPR certificate.                                       CDCL, emitting DRAT additions including an empty clause for UNSAT,
VeriPB                                     1.00 ×    1.00 ×         1/6    while larger failed compact cases return UNKNOWN by default.
Graph recovery and a bounded component-hierarchy trial provide the         VeriPB                                   0.879 ×       0.888 ×     47/119
active heuristic, after which failure falls back to unrestricted           Recognized encodings become finite-domain CSPs: min-conflicts
watched-literal CDCL rather than implying UNSAT. The exact                 repair is followed by propagation and bounded DSATUR-style search.
generator-specific layout is required; SAT assignments are checked         SAT assignments are checked against the original CNF; exact rope
internally, while UNSAT emits a PB RUP proof, and malformed or             signatures may use triangle-cycle dynamic programming, while CDCL
unsupported inputs return UNKNOWN without external checking.               or rope DP emit VeriPB proof steps, including RUP steps, for UNSAT;
                                                                           inconclusive one-hot or dense-choice searches return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

coloring-clique                                                        032    core-based-generator                                                  034
11 GBD instances · 3 validation · baseline 3/3                                20 GBD instances · 4 validation · baseline 3/4
The benchmark asks whether an existentially chosen graph can                  The benchmark asks whether a Boolean CNF is satisfiable when a
contain a k-vertex clique while admitting a proper coloring with c            residual core is surrounded by repeated three-row gadgets over signed
colors. The CNF uses edge, clique-position, and color variables for           variables. Each gadget encodes all but one sign pattern with chain
graph choices, vertex selection, distinctness, and coloring conflicts.        auxiliaries and links the omitted pattern to the core.
Proof format                             No verif.        + verif.   Solved   Proof format                             No verif.     + verif.     Solved
GRAT                                 1.35·10 −4 × 7.88·10−4 ×          2/3    GRAT                                      35.9 ×      61.6 ×          4/4
Exact structural recognition accepts only the expected numbering and          Missing-sign decoding fixes gadget variables and reduces recognized
complete clause set; malformed or unrecognized formulas return                inputs to output units plus a residual core for watched-literal CDCL
UNKNOWN. Recognized instances receive a clause-checked SAT                    with first-UIP learning. SAT assignments are checked; UNSAT emits a
assignment when k <= c; when k > c, the solver introduces                     textual DRAT trace with gadget clauses, learned residual clauses, and a
position-color variables and emits a textual DRAT pigeonhole                  final contradiction, while rejected structures or failures return
refutation, with generation failures returning UNKNOWN.                       UNKNOWN.
DPR                                 1.35·10−4 ×      7.88·10 −4 ×      2/3    DPR                                        1.05 ×      1.01 ×         3/4
Exact clause-set recognition accepts only the recovered k = c+1               Strict structural extraction and preprocessing remove recognized
encoding; equivalent encodings return UNKNOWN. For matches, it                padding, pure variables, and low-product occurrence pairs while
skips SAT search, adds selected-color and derived-color clauses,              recording resolvents, leaving a reduced core for watched-literal CDCL.
reduces the contradiction to pigeonhole, and emits a DPR certificate          SAT models are reconstructed and checked; UNSAT writes a textual
ending in the empty clause; proof failures return UNKNOWN.                    DPR trace that can include witness-free clause additions, while
VeriPB                               1.35·10 −4 ×    7.87·10 −4 ×      2/3    unsupported structures or proof failures return UNKNOWN.
Symmetry-based paired vertex swaps canonicalize selected vertices             VeriPB                                     1.05 ×      3.22 ×         3/4
after accepting the exact contiguous layout and complete templates;           Local search first attacks the bounded, structurally extracted core; if it
alternate layouts or unsupported formulas return UNKNOWN. For c               fails, its best phase seeds watched-literal CDCL. SAT models are
>= k, it checks a SAT assignment; for c < k, RUP exclusions and               extended through the gadgets and checked; UNSAT emits VeriPB
cutting planes derive a VeriPB pigeonhole contradiction, with                 cutting-planes and RUP derivations, while unsupported structures or
generation failures returning UNKNOWN.                                        internal failures return UNKNOWN.

                                                                              cover                                                                 035
coloring-mycielski-graph                                               033
                                                                              18 GBD instances · 4 validation · baseline 1/4
19 GBD instances · 4 validation · baseline 0/4
                                                                              The benchmark asks whether an n-point Steiner triple system has a
The benchmark asks whether a recursively constructed Mycielski
                                                                              cap of at least k points with no complete triple. CNF uses point
graph has a proper coloring with one fewer color than its level. CNF
                                                                              variables, triple clauses forbidding all three selected, and auxiliary
encodings use vertex-color variables, exactly-one constraints, and edge
                                                                              counters for the size threshold.
clauses forbidding equal colors, with supported compact and permuted
variants.                                                                     Proof format                             No verif.     + verif.     Solved
                                                                              GRAT                                       1.00 ×      1.00 ×         1/4
Proof format                             No verif.        + verif.   Solved
GRAT                                       1.33 ×        0.786 ×       1/4    Recognized layouts first use randomized cap search with maximal-cap
                                                                              growth, local exchanges, tabu or annealing moves, and a special
One-hot recognition drives an extension-variable recoloring proof that
                                                                              projective quotient search. Selected targets use watched-literal CDCL;
repeatedly reduces a Mycielski coloring instance to fewer colors.
                                                                              checked SAT models are printed, while UNSAT emits learned clauses
Shadow copies handle hinted levels, bit encodings first define color
                                                                              and the empty clause as DRAT. Unrecognized inputs or noncertifying
indicators, and an opt-in CDCL fallback can verify SAT assignments;
                                                                              failures return UNKNOWN.
without it, unsupported inputs return UNKNOWN, while refutations
are emitted as DRAT text for external elaboration.                            DPR                                       1.00 ×      1.00 ×          1/4
DPR                                   1.01·104 ×           120 ×       4/4    Recognized Steiner/BDD layouts use quasigroup cap search:
                                                                              completion conflicts trigger endpoint removal, refill, and periodic
It recognizes supported compact, permuted, and canonical layouts,
                                                                              ruin-and-recreate. Selected cases use a propagation tree or
reconstructing graph, color, and hint structure rather than running
                                                                              watched-literal CDCL, emitting clause additions, some witness-free,
general SAT search. Complete hints drive RUP shadow-edge
                                                                              that end in the empty clause; unsupported layouts and proof failures
derivations and a PHP refutation; incomplete hints use fresh-variable
                                                                              return UNKNOWN, while remaining regimes lack an UNSAT path.
one-hot recursion only at bounded ranks, while rejected inputs return
UNKNOWN and no SAT-witness path exists.                                       VeriPB                                     1.00 ×      1.00 ×         1/4
VeriPB                               2.94·104 ×            271 ×       4/4
                                                                              Embedded affine and product cap constructions lead, with bit-mask
                                                                              branch-and-bound and selected tabu-style repair on recognized
It recognizes canonical and recovered bit, one-hot, and XOR layouts,
                                                                              layouts. Selected cases then use proof-logging CDCL or a tree proof;
then uses color symmetry to fix the newest root and recursively derive
                                                                              direct SAT models are checked and printed, but CDCL SAT results are
a coloring instance with one fewer color. Proof-only indicators and
                                                                              not printed as models, and unsupported or noncertifying cases return
recoloring steps support the induction to a final contradiction; failed
                                                                              UNKNOWN.
recognition or certificate generation returns UNKNOWN, with no
SAT-witness path.
                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


crafted-cec                                                          036     cryptography                                                          038
20 GBD instances · 4 validation · baseline 4/4                               860 GBD instances · 172 validation · baseline 84/172
The benchmark asks whether a primary-input assignment can make               These benchmarks ask whether a chosen Boolean input block can
an asserted output of a signed AND circuit true. Each topologically          make a one-block cryptographic hash or compression circuit meet
ordered gate is represented by one wide clause plus binary clauses,          specified output constraints. The circuit becomes CNF with variables
and the final output is asserted by a unit clause.                           for input bits and intermediate values, plus clauses fixing constants,
Proof format                             No verif.    + verif.     Solved    selected inputs, and outputs.
GRAT                                      23.7 ×      23.5 ×           4/4   Proof format                             No verif.      + verif.    Solved
Packed genetic search simulates the recognized circuit in bit lanes,         GRAT                                     0.961 ×       0.961 ×     74/172
mutating assignments to seek a 12-input model and rechecking                 Recognized hash layouts enumerate a bounded free message prefix,
clauses. The SAT path has no UNSAT route; a narrow two-input                 evaluate the hash, and use CDCL to complete auxiliary variables; other
branch uses equivalence checks and RUP case proofs with CDCL                 formulas use watched-literal CDCL with 1-UIP learning and restarts.
fallback, emitting a proof stream on closure, while unsupported              Models are checked and returned; direct search lacks an UNSAT
layouts or unfinished proofs return UNKNOWN.                                 certificate and reports UNKNOWN on exhaustion or completion
DPR                                        21.1 ×     18.7 ×           4/4   failure, while fallback logging supplies DRAT for elaboration.
Packed bit-parallel evaluation combines an incumbent with one-bit            DPR                                       1.01 ×       1.01 ×      80/172
neighbors; coordinate ascent and sparse mutations seek the asserted          Exact structural recognition drives free-message enumeration and
root, with large inputs falling back to random assignments. After            native hash evaluation, followed by CDCL completion of auxiliary
validation it emits a SAT model but no DPR certificate; heuristic failure    variables; unrecognized inputs use watched-literal CDCL with 1-UIP
has no UNSAT or timeout result, while binary-root and unrecognized           learning and restarts. Verified SAT assignments are returned, while
layouts return UNKNOWN.                                                      only the fallback can log learned DPR/RUP-style additions and a final
VeriPB                                     9.89 ×     9.44 ×         4/4     empty clause; direct-search failure or unavailable logging yields
Weighted breakout search scores packed assignments and one-bit               UNKNOWN.
neighbors, raises weights on false root targets, and uses random moves       VeriPB                                   0.896 ×       0.896 ×     66/172
to seek a satisfying 12-way output without handling a negative root. It      Functional recovery of ordered gate blocks and 64-way bit-sliced input
reconstructs gates and checks clauses before emitting the model; no          search drives the specialized path, filtering derived values against fixed
UNSAT certificate path is active, and unsupported shapes or other            clauses. SAT assignments are checked against original clauses; only
roots return UNKNOWN.                                                        compact CDCL emits a VeriPB RUP proof for UNSAT, while
                                                                             unsupported structures, fast-path exhaustion, and non-SAT sampled
cril-misc                                                            037     cases return UNKNOWN.
62 GBD instances · 13 validation · baseline 4/13
The benchmark asks whether Boolean signal and gate-output variables          cryptography-ascon                                                    039
can satisfy a CNF encoding of a circuit or netlist. Clauses encode local     26 GBD instances · 6 validation · baseline 5/6
gate relations, which may include parity-like constraints, gate              These formulas ask whether two unknown message bytes can make a
definitions, or equivalences.                                                fixed Ascon-Hash v1.2 digest through a bit-blasted Boolean circuit.
Proof format                             No verif.    + verif.     Solved    The benchmark uses a specific optimized, topologically ordered CNF
GRAT                                     0.848 ×      1.04 ×        1/13     encoding with auxiliary variables and fixed constraints, rather than
                                                                             arbitrary cryptographic formulas.
Structural recognition limits this solver to a large, clause-dense
circuit-CNF envelope; parity-like blocks remain ordinary clauses, not        Proof format                             No verif.      + verif.    Solved
GF(2)-eliminated. Watched-literal first-UIP CDCL handles recognized          GRAT                                     1,010 ×       1.55 ×         6/6
inputs; unsupported or unresolved cases return UNKNOWN, SAT                  Bit-parallel enumeration evaluates all 16-bit source assignments
assignments are checked, and UNSAT learned clauses are emitted as            through the recognized circuit and intersects the target constraints. A
raw DRAT additions for external elaboration.                                 surviving assignment is completed and checked clause by clause;
DPR                                      0.799 ×     0.977 ×        0/13     exhaustion emits textual DRAT additions for external elaboration,
It recognizes ordered ternary parity blocks and NAND definitions,            including generated shortcuts and a resolution tree, while
then uses bipartite matching to orient parity equations before               unsupported shapes or failed checks return UNKNOWN.
branching with structure-informed preferences in watched-literal             DPR                                        747 ×        1.50 ×        6/6
CDCL. Unsupported or unmatched cases return UNKNOWN; SAT                     Bit-sliced truth-table evaluation exhaustively tests 16-bit source
models are checked, while UNSAT emits witness-free DPR clause                assignments, using small gates and frontier summaries to filter target
additions, including an empty clause, but the source does not establish      constraints. A surviving input is completed and checked against every
proof correctness.                                                           clause; otherwise the solver emits witness-free assignment-blocking
VeriPB                                   0.799 ×     0.977 ×        0/13     clauses and a resolution sequence for a DPR certificate, with
Order-sensitive XOR/NAND template recognition selects probe                  recognition or certificate failures returning UNKNOWN.
variables, followed by hidden-unit extraction and failed-literal probing     VeriPB                                     1.17 ×      0.400 ×        4/6
before watched-literal first-UIP CDCL. UNSAT traces use RUP steps            Incidence decomposition and bit-parallel compiled-gate evaluation
and a VeriPB conclusion, SAT models are fully assigned and rechecked,        enumerate the 16-bit source assignments while separating four small
and input or post-check failures return UNKNOWN.                             side components. A surviving lane is reconstructed with recursive
                                                                             DPLL and fully clause-checked; with none, the solver emits
                                                                             assignment-blocking RUP leaves and a balanced VeriPB
                                                                             polynomial-elimination tree, while unsupported structures or proof
                                                                             failures return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

cryptography-cbmc                                                   040    design-debugging                                                    042
13 GBD instances · 3 validation · baseline 3/3                             119 GBD instances · 24 validation · baseline 24/24
These benchmarks ask whether Boolean constraints from a bounded            These benchmarks ask whether fixed stimuli and, when present, state
cryptographic circuit check, typically a CBMC AES encoding, have a         or observed values are consistent with a combinational or unrolled
satisfying assignment. Circuit inputs and intermediate values become       sequential circuit. Tseitin-style CNF clauses constrain Boolean signals,
Boolean variables, while gate equations, bookkeeping conditions, and       while unit clauses fix selected values; SAT means a completion exists
an assertion or miter obligation become CNF clauses.                       and UNSAT means inconsistency.
Proof format                             No verif.    + verif.    Solved   Proof format                             No verif.     + verif.   Solved
GRAT                                      2.72 ×      8.95 ×         3/3   GRAT                                      3.04 ×      1.93 ×      24/24
Root propagation, binary-equivalence substitution, bounded variable        Uniform-phase completion precedes search, assigning DIMACS
elimination, and failed-literal probing simplify recognized CNFs before    variables in fixed order and accepting SAT only after checking every
activity-guided CDCL with restarts and clause reduction. It checks SAT     original clause. Failed trials invoke first-UIP CDCL with activity-based
assignments against the original clauses and logs preprocessing and        branching and phase saving, logging learned clauses as a DRAT
search additions for externally checked UNSAT proofs; unsupported          refutation; SAT paths return checked models, and malformed or
inputs and some cases after elimination return UNKNOWN.                    inconclusive cases return UNKNOWN.
DPR                                      0.419 ×      1.36 ×         3/3   DPR                                 4.43·10 −3 ×     0.0379 ×     22/24
Signature filtering identifies Tseitin-like inputs, after which root       Gate-pattern congruence closure recovers supported AND, XOR, and
simplification, implication-SCC substitution, bounded elimination, and     ITE relations and merges them with a DSU quotient after propagation
failed-literal probing precede focused output-assumption search for a      and phase trials. Failed-literal probing can emit clauses toward a DPR
unique width-16, 56, or 184 candidate, with generic CDCL as fallback.      contradiction, but unsupported residual encodings or inconclusive
Logged witness-free clause additions and empty-clause exits support        search return UNKNOWN; no general DPLL or CDCL fallback exists.
UNSAT, while SAT assignments are reported; unsupported inputs or           VeriPB                              8.85·10 −3 ×     0.0704 ×     23/24
unresolved post-elimination searches return UNKNOWN.                       Occurrence-counter propagation scans CSR literal occurrences to
VeriPB                                   0.159 ×     0.654 ×        2/3    decrement residual counts, with CDCL fallback using 1-UIP learning,
Lookup-map congruence, signed AND/NAND matching, and                       phase saving, and restarts. UNSAT produces a VeriPB RUP proof, or a
binary-implication equivalences drive clause rewriting, bounded            conditional compact pol chain for qualifying root conflicts; SAT
elimination, and failed-literal probing before watched-literal CDCL        assignments are clause-checked, while malformed or unresolved cases
with 1-UIP learning. UNSAT receives VeriPB RUP records ending in an        return UNKNOWN.
empty constraint; SAT is reported only when no variables were
eliminated, while malformed inputs, setup failures, or post-elimination    diagnosis                                                           043
SAT cases return UNKNOWN.                                                  130 GBD instances · 26 validation · baseline 19/26
                                                                           The benchmark asks whether a finite-domain diagnosis model has a
cryptography-simon                                                  041    consistent assignment, with each object selecting one of six states
71 GBD instances · 15 validation · baseline 5/15                           across repeated scenarios. Observations and transition or relation
These instances ask whether a 32-bit key maps fixed plaintext to           constraints are compiled into CNF using one-hot choices and auxiliary
ciphertext through Simon-style Feistel rounds, with a related key          variables.
obtained by bit permutation. The CNF bit-blasts keys, round states,        Proof format                             No verif.     + verif.   Solved
and gate intermediates, and fixes both endpoint words.                     GRAT                                     0.586 ×      1.40 ×      12/26
Proof format                             No verif.    + verif.    Solved   It recognizes the six-state exact-one structure, performs
GRAT                                     1,110 ×     1,100 ×      15/15    binary-implication SCC substitution and bounded variable elimination,
Structured Hamming-weight-ordered enumeration exploits the                 then solves accepted formulas with watched-literal CDCL and first-UIP
related-key bit permutation after exact canonical recognition, with        learning. Unsupported inputs return UNKNOWN; SAT outputs are
SIMD batches and an exhaustive key-search fallback. A found key is         checked assignments, while UNSAT uses textual DRAT for external
reconstructed and checked against every input clause before a SAT          elaboration; preprocessing conflicts can lack a final empty clause.
assignment is emitted; unsupported, exhausted, or failed-validation        DPR                                      0.520 ×       1.22 ×     10/26
cases return UNKNOWN, with no UNSAT certificate path.                      It dispatches on recognized disjoint six-state exact-one groups and
DPR                                        624 ×      596 ×       15/15    uses watched-literal CDCL with first-UIP learning, implication-graph
AVX-512 exhaustive enumeration of the first key, with a last-round         minimization, activity branching, and restarts. SAT returns a checked
inverse filter, follows fixed-key probes and exact clause-multiset         assignment; UNSAT uses logged additions and deletions ending in an
recognition. Each found key is expanded and checked against every          empty clause, with recovery after the serialization guard, while
clause before a SAT assignment is emitted; unsupported,                    unsupported or certificate failures return UNKNOWN.
failed-validation, or exhausted cases return UNKNOWN because no            VeriPB                                   0.661 ×       1.39 ×     14/26
UNSAT certificate path is implemented.                                     It uses binary-clause parity union-find to quotient variables and
VeriPB                                     716 ×      679 ×       15/15    validate a SAT model from the reduced instance; otherwise inputs use
Strict ordered-template recognition is followed by word-level endpoint     watched-literal CDCL with first-UIP learning. Unsupported or
screening and exhaustive vectorized key enumeration, including a           unresolved cases return UNKNOWN; UNSAT emits VeriPB RUP
copied-half test before the final nonlinear round. Each surviving key is   additions with hints, deletions, and an empty-clause conclusion, but
expanded and clauses are validated before a SAT assignment is              shortcut paths have no UNSAT certificate.
emitted; rejected templates or keyless instances return UNKNOWN,
with no UNSAT certificate path.
                                                                                                   Harrison Green, Claire Le Goues, and Fraser Brown


dimacs-sorter                                                        044    discrete-logarithm                                                  046
32 GBD instances · 7 validation · baseline 7/7                              20 GBD instances · 4 validation · baseline 1/4
These benchmarks ask whether one option can be selected from each           The benchmark asks whether a bounded exponent x satisfies a^x mod
finite-domain block, with auxiliary Boolean choices, so that all            n = r. CNF encodings represent exponent bits and staged accumulator,
remaining constraints are satisfied. In CNF, each block uses an             conditional-product, and modular-reduction words, with clauses fixing
at-least-one clause and pairwise at-most-one clauses, followed by           the final residue; implementations recognize particular layouts.
residual circuit or row constraints.                                        Proof format                             No verif.    + verif.    Solved
Proof format                             No verif.     + verif.    Solved   GRAT                                  2.85·104 ×     7,850 ×         4/4
GRAT                                    0.0591 ×     0.0591 ×        3/7    Prefix CDCL probes recover intermediate residues; GCD-based
Ordered one-hot and gate-DAG recognition is the distinguishing              reconstruction recovers the modulus before baby-step/giant-step
technique: recognized circuits are evaluated over domain choices and        search finds an exponent. That exponent and the circuit state are
Boolean controls, while shuffled inputs receive only one-hot                assigned as roots, and occurrence-indexed propagation completes and
recognition. After an initial population pass, watched-literal CDCL         checks clauses; unsupported or ambiguous recovery, search or
supplies the fallback; failed search or checking returns UNKNOWN,           completion failures return UNKNOWN, with no UNSAT certificate
with no UNSAT certificate path.                                             path implemented.
DPR                                        1.31 ×      1.31 ×        7/7    DPR                                  4.09·104 ×      1,070 ×         4/4
Bit-parallel local search is the distinguishing technique: after            Baby-step/giant-step search directly recovers a bounded exponent
recovering signed one-hot blocks and functional gates, it evaluates         after structural recognition, then pins exponent, accumulator, and
many candidate states at once and applies tabu reassignment with            product words to reduce circuit completion to propagation. A
randomized restarts. Recognition is bounded; search is incomplete.          watched-literal pass is followed by an active CDCL fallback and clause
SAT models are printed, while failures return UNKNOWN; no UNSAT             checking; unsupported layouts, noninvertible giant steps, and search
or DPR certificate is emitted.                                              or completion failures return UNKNOWN, with no UNSAT or DPR
VeriPB                                    2.50 ×      2.49 ×         7/7    certificate path.
Row abstraction and propagation distinguish this solver: recognized         VeriPB                                3.55·104 ×      885 ×          4/4
sorter rows become source-count constraints, narrowed by fixpoint           Extended baby-step/giant-step search peels gcd factors and uses
intervals and bounded affine checks before branching on the row with        GCD-based modulus recovery to solve the bounded logarithm. Stage
fewest patterns. Leaves reconstruct gates and validate every clause;        residues and quotient hints pin exponent and state bits; alternating
unsupported layouts or exhausted search return UNKNOWN, with no             forward and reverse propagation completes auxiliaries and checks
VeriPB UNSAT certificate path.                                              clauses, while unsupported layouts or search/completion failures
                                                                            return UNKNOWN, with no general SAT fallback or UNSAT/VeriPB
dining-philosophers                                                  045
                                                                            certificate path implemented.
37 GBD instances · 8 validation · baseline 8/8
These benchmarks ask whether a bounded dining-philosophers
transition system can reach a deadlocked ring at some time frame.
CNF encodes Boolean state and action signals, transition circuitry, and
deadlock indicators, with a clause requiring one indicator to be true.
Proof format                             No verif.     + verif.    Solved
GRAT                                     0.573 ×     0.595 ×         8/8
After recognizing its gate/XOR structure, the solver orders branches
on deadlock outputs by AND-cone size; a size heuristic changes only
that order. It then uses watched-literal CDCL, checks SAT assignments,
and logs UNSAT clauses as textual DRAT additions for external
checking; unsupported inputs return UNKNOWN.
DPR                                      0.255 ×      0.177 ×        8/8
It recovers paths from Tseitin structure, prioritizes temporal goals, and
for the exact UNSAT shape adds action-coverage clauses before
bounded Davis-Putnam elimination, followed by CDCL. Non-special
recognized inputs use CDCL; SAT models are checked, while UNSAT
logging uses witness-free DPR additions with preludes outside live
RUP checks, and unrecognized inputs or search/check failures return
UNKNOWN.
VeriPB                                   0.115 ×     0.0576 ×        7/8
Bounded Davis-Putnam elimination first shrinks recognized formulas
while recording data for reverse model reconstruction, then
watched-literal CDCL handles the reduced instance. SAT assignments
are reconstructed and checked against all original clauses; UNSAT
preprocessing and learned clauses are logged as VeriPB RUP
constraints with an empty constraint; unsupported inputs,
reconstruction failures, or validation failures return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

edge-matching                                                       047    ensemble-computation                                               049
97 GBD instances · 20 validation · baseline 8/20                           13 GBD instances · 3 validation · baseline 3/3
The benchmark asks whether a square grid can be filled using each tile     These benchmarks ask whether a bounded collection of set-union
once while colors on shared edges agree between neighbors. CNF uses        operations can generate required target subsets from basic elements.
one-hot placement and internal-edge groups, with clauses enforcing         They encode operation choices and resulting memberships as
legal local orientations; recognized layouts are specific encodings, not   structured Boolean circuits, often expressed as CNF with auxiliary
the whole edge-matching family.                                            gate variables.
Proof format                             No verif.   + verif.     Solved   Proof format                             No verif.    + verif.   Solved
GRAT                                      2.17 ×     2.16 ×       14/20    GRAT                                     0.152 ×     0.271 ×       1/3
Structural recognition targets compact and unshuffled historical           Template recognition identifies bounded direct or complement layouts
layouts, using grid embedding, arc consistency, and depth-first edge       and encodes candidate subsets as integer masks. Randomized
synchronization, with watched propagation and false-first completion       disjoint-union and min-conflicts searches propose programs;
on the historical path. SAT models undergo full clause checking; only      assumptions on result bits are propagated and clause-checked, while
a root-level propagation conflict emits a one-step RUP/DRAT                unsupported inputs or failed search return UNKNOWN and no active
empty-clause addition, while unrecognized layouts and other failures       UNSAT or DRAT emission path exists.
return UNKNOWN.                                                            DPR                                      0.101 ×     0.181 ×       0/3
DPR                                        1.10 ×    1.10 ×        8/20    Bounded structural recognition filters for the six-row, k-column
Compact tile-major recognition and local orientation enumeration           indicator layout and uses the recovered block to seed branching
drive a min-conflict constructor, followed by connected-frontier           phases and order. Watched-literal CDCL with first-UIP learning
backtracking with edge propagation, MRV choices, capacity checks,          searches the CNF; SAT models are completed and checked, while
and symmetry breaking. The fallback forcing and watched-literal            unsupported inputs or unproved UNSAT outcomes return UNKNOWN
search prints SAT only after complete clause validation; unsupported,      because proof logging is disabled.
unsatisfiable, or exhausted cases return UNKNOWN because no                VeriPB                                   0.152 ×     0.271 ×       1/3
UNSAT certificate path is implemented.                                     Acyclic XOR/AND recognition groups rows into masks and extracts
VeriPB                                     1.64 ×    1.61 ×       12/20    targets. A construction handles one-one cases; randomized
Generalized exact-cover search uses colored secondary edge columns,        common-subexpression elimination and OR closure repair handle
bounded local edge tuples, and minimum-active-row branching after          others, with CDCL fallback on an abstract subset closure. Checked
recognizing the compact placement-and-color structure. An alternate        SAT witnesses are emitted; failures or unsupported cases return
path requires a recovered contiguous square gate layout, forces            UNKNOWN, with no UNSAT or VeriPB certificate path.
identity placement, and uses watched-literal propagation; complete
models are clause-checked, while failures return UNKNOWN because
                                                                           equivalence-chain                                                  050
no UNSAT certificate path is implemented.
                                                                           19 GBD instances · 4 validation · baseline 0/4
                                                                           This benchmark asks whether a Boolean assignment satisfies a
edit-distance                                                       048    structured CNF. Groups of four ternary clauses encode parity relations
20 GBD instances · 4 validation · baseline 0/4                             over three variables, while binary and other ternary clauses impose
The benchmark asks whether a signed complete graph can be                  residual constraints, sometimes using auxiliary variables.
partitioned into clusters so that disagreements with target edge signs     Proof format                             No verif.    + verif.   Solved
stay within an encoded edit budget. Pair-equality variables represent      GRAT                                      1.00 ×      1.00 ×       0/4
co-membership, transitivity clauses enforce consistent clusters, and
                                                                           Affine parity extraction and bounded-weight meet-in-the-middle
additional bounded-width clauses constrain the allowed edit count.
                                                                           decoding drive this solver: it recognizes four-clause ternary parity
Proof format                             No verif.   + verif.     Solved   groups, eliminates them over GF(2), and searches for a low-weight
GRAT                                       2.00 ×    2.00 ×          2/4   parity-check solution. It propagates candidates through residual
The solver first uses partition local search with singleton, all-in-one,   constraints and checks SAT assignments; without general fallback or
and graph-derived starts, then vertex relocations and cluster merges. It   UNSAT certification, structural, decoding, or completion failure
fixes pair variables, uses watched-literal CDCL to complete and            returns UNKNOWN.
validate a SAT model, and returns UNKNOWN on missed partitions,            DPR                                       1.00 ×      1.00 ×       0/4
unsupported encodings, or failed completion; no UNSAT certificate          Bounded-weight syndrome decoding is its core: it reduces recognized
path is implemented.                                                       XOR structure to a system and uses meet-in-the-middle search for
DPR                                        2.00 ×    2.00 ×          2/4   support of weight at most seven. It reconstructs variables and applies
Positive-gain agglomeration, single-vertex descent, and                    DPLL to residuals; checked SAT assignments succeed, while
correlation-clustering restarts generate fixed pair assignments, then      unsupported structure or failed decoding/completion returns
watched-literal CDCL completes and checks a SAT model. On failure,         UNKNOWN without an UNSAT path.
induced-P3 packing and bounded minimum-fill Davis-Putnam                   VeriPB                                    1.00 ×      1.00 ×       0/4
elimination feed residual CDCL and emit proof records for external         Affine propagation and randomized conflict-core learning drive its
checking; recognition mismatches return UNKNOWN, while UNSAT               search: Gaussian elimination expresses variables as affine forms, then
requires empty-clause or conflict evidence, not heuristic failure.         residual-clause decisions yield dependency-based affine nogoods. It
VeriPB                                    2.00 ×     2.00 ×         2/4    checks reconstructed SAT assignments; unsupported structures or
Multi-start cluster-editing search uses graph-based and random             failed search return UNKNOWN, with no UNSAT refutation
partitions, greedy vertex moves, merges, exchanges, and perturbations      implemented.
to find a budget-feasible partition. It fixes pair variables and runs
watched-literal CDCL only on the budget suffix, checks every original
clause, and returns UNKNOWN on unsupported encodings or failed
search/completion; no UNSAT certificate path is implemented.
                                                                                                 Harrison Green, Claire Le Goues, and Fraser Brown


equivalence-chain-principle                                         051   erdos-discrepancy                                                        053
4 GBD instances · 1 validation · baseline 0/1                             21 GBD instances · 5 validation · baseline 1/5
These CNFs ask whether a chain of Boolean tables can satisfy fixed        The benchmark asks whether a finite sequence of positive or negative
endpoint assignments while auxiliary matching choices transport           ones can keep every prefix sum along each homogeneous progression
truth values between adjacent tables. In the benchmark encoding, CNF      d, 2d, and so on within absolute value three. Its CNF uses sign
clauses express exact-one matching choices and guarded implications       variables plus auxiliary state variables to encode these bounded-prefix
between corresponding entries.                                            conditions.
Proof format                             No verif.   + verif.    Solved   Proof format                             No verif.         + verif.    Solved
GRAT                                      1.00 ×     1.00 ×         0/1   GRAT                                       1.01 ×          1.01 ×         1/5
Bounded structural recognition activates a fiber-independence             Primary-boundary recognition guides activity and phase initialization
invariant, propagating selector-controlled equivalences across the        for the restricted three-state encoding, after which watched-literal
chain and using a backward dependency pass from a contradictory           CDCL performs the active search with learning, restarts, and clause
endpoint fiber. For recognized instances, it emits a textual DRAT         reduction. SAT assignments receive full clause verification; rejected
clause-addition stream ending in the empty clause for external            inputs, search or verification failure, and an UNSAT result return
elaboration; unsupported, malformed, or proof-generation failures         UNKNOWN, with no UNSAT certificate path.
return UNKNOWN, with no general SAT fallback.                             DPR                                        905 ×          80.2 ×          5/5
DPR                                       1.00 ×     1.00 ×         0/1   Mod-3 phase seeding, with ladder reconstruction for shuffled
Bounded recognition handles k=3 patterns by recursively transporting      instances, targets recognized encodings before watched-literal CDCL
guarded existential-row clauses and branching on one matching             completes or repairs assignments through learning and restarts. It
coordinate; it does not require every pairwise-negative exact-one         verifies clauses for SAT; unsupported inputs, recognition failure,
clause. Recognized k=4 patterns invoke watched-literal CDCL with          search failure, and an UNSAT result all return UNKNOWN, with no
1-UIP learning and log UNSAT clause additions; checked SAT                DPR proof path for UNSAT.
assignments are supported, while unsupported cases or solver failures     VeriPB                                   0.815 ×          0.815 ×         0/5
return UNKNOWN.                                                           A conditional family-specific phase warm start seeds sequence
VeriPB                                    1.00 ×     1.00 ×         0/1   variables from a generated instance, then watched-literal CDCL
Structural recognition dispatches accepted chains to either a             searches recognized inputs with learning and restarts; only phases, not
pseudo-Boolean equivalence proof, using matching-tree cardinality         learned state, are carried over. It rebuilds states and rechecks clauses
inequalities that telescope across layers, or a guarded implication       before SAT; recognition, reconstruction, or search failure and root
proof that propagates nonempty fibers through an n-ary path tree. It      contradiction return UNKNOWN, with no UNSAT certificate path.
emits a VeriPB proof rather than performing SAT search; inputs
outside the reconstructed layout, proof-generation failures, and output
                                                                          fdmus                                                                     054
failures return UNKNOWN.
                                                                          1,000 GBD instances · 200 validation · baseline 200/200
                                                                          Given a Boolean circuit, the benchmark asks whether some input
equivalence-checking                                                052
                                                                          makes its output 1 and makes it 0 after either of two coordinate flips.
28 GBD instances · 6 validation · baseline 0/6
                                                                          CNF uses three circuit copies, sharing inputs except at those flips, with
These benchmarks ask whether two acyclic Boolean networks produce         gate and output constraints.
the same output for every primary-input assignment. A Tseitin CNF
                                                                          Proof format                             No verif.         + verif.    Solved
introduces variables for internal signals and asserts a final mismatch
                                                                          GRAT                                       3.22 ×         2.08 ×      200/200
output, so a satisfying assignment supplies a distinguishing input and
unsatisfiability establishes equivalence.                                 Transitive-fanout equivalences collapse unaffected gates onto
                                                                          first-copy representatives and restrict decisions to changed inputs and
Proof format                             No verif.   + verif.    Solved   affected cones. Watched-literal CDCL handles the reduced instance
GRAT                                      1.00 ×     1.00 ×         0/6   and SAT returns a complete assignment; exact-layout rejection or
Bit-parallel simulation proposes equal or complementary signals,          solver/proof failures return UNKNOWN, while UNSAT retains a
which the solver verifies while decomposing negated mismatch goals        textual DRAT/RUP-style certificate.
through recognized gate polarities. An incremental watched-literal
                                                                          DPR                                        3.03 ×         0.794 ×     200/200
CDCL fallback handles unresolved goals and logs learned clauses plus
an empty clause for external UNSAT checking; unsupported or               Congruence propagation equates gates across copies; quotienting and
incomplete searches return UNKNOWN, and no SAT-model output               bounded elimination simplify affected cones. Residual watched-literal
path is implemented.                                                      CDCL searches the remainder and emits textual DPR additions for
                                                                          preprocessing and learning, with an empty clause on UNSAT. SAT
DPR                                       1.00 ×     1.00 ×         0/6   reconstruction checks the full original assignment; unsupported
Recursive OR decomposition and LUT shortcuts try to force                 layouts or solver, proof, or reconstruction failures return UNKNOWN.
final-miter literals false before cone-local watched-literal CDCL
                                                                          VeriPB                                    3.51 ×          0.352 ×     200/200
handles the remainder. Its three-input four-clause check is generic
rather than mux-specific; on UNSAT, local clauses are mapped back         Structural hashing in lockstep with disjoint-set equalities derives gate
and logged with an empty clause for external checking, while SAT          congruences across the three copies, followed by root-level unit
completion is checked and failures return UNKNOWN.                        propagation. A two-watched-literal CDCL fallback handles remaining
                                                                          cases and logs equivalences and learned clauses as VeriPB RUP steps;
VeriPB                                    1.00 ×     1.00 ×         0/6   SAT returns a checked full assignment, while unsupported layouts or
Hash-consed complemented-edge DAG reconstruction turns                    solver/proof-writing failures return UNKNOWN.
recognized Tseitin gates into simplified Boolean structure, while
simulation signatures only nominate candidate equivalences and
constants. Watched-literal RUP checks and bounded branching
elaborate these claims; targeted CDCL emits RUP proof steps for
closed UNSAT cases, but unresolved residues return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

fermat                                                                  055    fixed-shape-random                                                   057
8 GBD instances · 2 validation · baseline 2/2                                  30 GBD instances · 6 validation · baseline 2/6
This family asks whether two bounded, equal-width integers p and q             This benchmark asks whether shared Boolean base variables can
satisfy p squared minus q squared equals N, usually with ordering and          satisfy all components of a bounded, fixed-shape CNF encoding. Each
range conditions. A CNF encodes the squaring and subtraction circuits          component uses center or root auxiliaries and selectors to express
with auxiliary variables.                                                      compatible local supports, and the question becomes whether one
Proof format                             No verif.       + verif.    Solved    assignment satisfies every original clause.
GRAT                                  6.07·104 ×     1.48·104 ×         2/2    Proof format                             No verif.    + verif.    Solved
Template recognition recovers the odd target N rather than searching           GRAT                                      4.64 ×     4.64 ×           5/6
arbitrary CNF. It factors N, selects a balanced divisor pair for p and q,      On recognized inputs, noisy minimum-break local search works on the
propagates through the circuit, and checks every clause before                 sparse CNF and checks candidates before reporting SAT. A failed walk
emitting a SAT assignment; unsupported or unsuccessful cases return            does not imply UNSAT; watched-literal first-UIP CDCL is the fallback,
UNKNOWN, with no UNSAT certificate path.                                       logging learned clauses and a final empty clause as textual DRAT for
DPR                                   4.25·104 ×        1,430 ×         2/2    external GRAT elaboration, while unsupported inputs return
Strict recognition of 8-65-bit primary vectors and a ripple-subtractor         UNKNOWN.
layout extracts the odd target N. Pollard-rho factorization and divisor        DPR                                        4.55 ×     4.55 ×          5/6
splits construct p and q, after which ordered propagation and full             Recognized inputs use focused probSAT on compact CNF, then
clause checks validate a SAT assignment; unsupported or failed cases           support-level min-conflicts over shared bases. Base models get
return UNKNOWN, with no UNSAT or DPR path.                                     exhaustive auxiliary completion; if these searches fail, watched-literal
VeriPB                                4.79·104 ×        1,300 ×         2/2    CDCL logs learned clauses and the empty clause as witness-free DPR
                                                                               additions, and heuristic failure is not UNSAT. Unsupported shapes
Parity and carry-chain recognition extracts an odd target from the
                                                                               return UNKNOWN; no elaboration or kernel validation is supplied.
narrow CNF layout rather than solving arbitrary formulas. It factors
the target, selects a closest nontrivial factor pair, builds a full model by   VeriPB                                     4.62 ×     4.62 ×         5/6
forward propagation, and checks every clause; failures return                  Plan projection first reduces each recognized gadget to minimal
UNKNOWN, with no UNSAT or VeriPB proof path.                                   signed-primary supports, then weighted min-conflicts flips all false
                                                                               literals of selected plans while updating affected gadgets incrementally.
                                                                               Exhaustive auxiliary reconstruction and full CNF checking certify
finite-state-machines                                                   056
                                                                               SAT; no UNSAT or VeriPB certificate path exists, so unsupported
12 GBD instances · 3 validation · baseline 3/3
                                                                               inputs return UNKNOWN and unsatisfiable inputs may continue until
These benchmarks ask whether a bounded, unrolled finite-state                  externally stopped.
transition system has an assignment satisfying its transition
constraints and a stated property condition. State, signal, and auxiliary
gate equations are converted to CNF, typically through Tseitin clauses.        floodit-puzzle                                                       058
                                                                               40 GBD instances · 8 validation · baseline 8/8
Proof format                             No verif.       + verif.    Solved
                                                                               These instances ask whether a fixed-source Flood-It board can be
GRAT                                      0.822 ×        1.62 ×         3/3
                                                                               completely flooded within at most m moves by choosing colors that
Bounded variable elimination resolves pivots only when pair, width,
                                                                               absorb adjacent monochromatic regions. The CNF uses one-hot color
and growth limits permit, retaining resolvents for reconstruction and
                                                                               choices and time-indexed flooded-state variables.
logging. It then uses watched-literal CDCL with 1-UIP learning; SAT
reverses elimination and checks a model, unsupported layouts return            Proof format                             No verif.    + verif.    Solved
UNKNOWN, and UNSAT is written as DRAT additions for external                   GRAT                                       745 ×     61.2 ×           8/8
elaboration and checking.                                                      Disjoint-set contraction and bitset state tracking support
DPR                                       0.478 ×       0.971 ×         3/3    multi-heuristic greedy construction, with seeded noisy trials providing
                                                                               a fallback for finding a plan within the move bound. It recognizes only
It recognizes only TIP/PICO layouts; TIP prioritizes frames containing
                                                                               ten-color square grids; found plans are expanded into move and state
bad-state goals. On PICO, bounded Davis-Putnam elimination uses
                                                                               variables and clause-checked before SAT, while construction failure
gate definitions and capped pairwise resolution before residual CDCL;
                                                                               returns UNKNOWN and no UNSAT certificate path exists.
SAT reverses elimination and checks a model, unsupported or
setup-failing cases return UNKNOWN, while UNSAT ends with                      DPR                                        328 ×      5.71 ×          8/8
witness-free clause additions and an empty clause.                             Monochromatic-region contraction supports greedy region-graph
VeriPB                                    1.24 ×        0.318 ×         3/3    color selection with randomized trials as a fallback for finding a
                                                                               bounded move sequence. It reconstructs and clause-checks the full
Binary-implication SCC preprocessing merges equivalent literals,
                                                                               assignment before SAT; this narrow recognized encoding has no
selecting bounded elimination regimes before a watched-literal CDCL
                                                                               UNSAT certificate path, so recognition, search, or checking failure
fallback. SAT restores eliminated variables and checks a model;
                                                                               returns UNKNOWN.
UNSAT logs preprocessing and learned clauses as VeriPB RUP
constraints, ending with an empty RUP and UNSAT command, while                 VeriPB                                     582 ×      6.51 ×         8/8
malformed or failed cases return UNKNOWN.                                      Randomized greedy rollouts on a contracted region graph lead into
                                                                               bounded beam search over flooded-component states. It recognizes
                                                                               only a ten-color layout, expands a found plan into all action and
                                                                               auxiliary variables, and rechecks every CNF clause before SAT; missed
                                                                               plans or failures return UNKNOWN, with no UNSAT certificate path.
                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


fpga-routing                                                          059    genurq                                                               061
97 GBD instances · 20 validation · baseline 16/20                            12 GBD instances · 3 validation · baseline 3/3

These CNFs ask whether each route or vertex can select one of k              Instances use small clause blocks with graph-like variable sharing; one
channels so conflicting pairs receive different channels. They encode        form encodes parity constraints, while another combines positive
choices with group clauses and matched binary conflicts, with some           binary clauses with an exact sequential encoding of an at-most-k
instances using equality-expanded or binary representations.                 constraint. The task is to determine whether all clauses can be satisfied
                                                                             for these restricted encodings.
Proof format                             No verif.     + verif.     Solved
GRAT                                      1.29 ×       1.04 ×       17/20    Proof format                             No verif.    + verif.     Solved
The active strategy reconstructs conflict graphs, uses bit-parallel clique   GRAT                                       64.9 ×     41.2 ×         3/3
search, and tries chordal or tabu coloring before finite-domain search       Recognizes bounded-width parity blocks as XOR equations, solves
and CDCL fallback. SAT assignments are checked against the CNF;              their incidence graph by spanning forests, and enumerates one
UNSAT proof output supplies learned clauses or finite-domain                 possible exceptional block. It verifies resulting assignments against the
nogoods for external DRAT elaboration, while unsupported or                  CNF before SAT, but has no UNSAT certificate path; unsupported or
unfinished cases return UNKNOWN.                                             unresolved inputs return UNKNOWN instead of using general SAT
                                                                             search.
DPR                                       4.07 ×       4.05 ×       19/20
The active strategy finds bitset (k+1)-cliques, then tries bounded           DPR                                        56.4 ×     18.1 ×         3/3
coloring, binary equality chains, and tabu search before CDCL fallback.      Combines XOR block recognition and incidence-graph parity solving
SAT assignments are checked against input clauses; UNSAT uses                with a fallback for positive binary clauses and a sequential at-most-k
PR/PHP clique proofs or proof-logged CDCL with normalized/original           counter. The base branch emits a checked SAT assignment; only
fallback and witness-free additions. Unsupported inputs or unresolved        bounded line-graph reconstruction can produce an UNSAT DPR proof,
searches return UNKNOWN; verification is external.                           reducing the matching contradiction to PHP with PR swaps, while
                                                                             failed searches and unsupported shapes return UNKNOWN.
VeriPB                                    4.09 ×      4.08 ×        19/20
The active strategy reconstructs route-conflict graphs and searches for      VeriPB                                    72.7 ×      17.6 ×         3/3
bounded oversized cliques, using cutting-planes pigeonhole proofs            Recognizes bounded XOR/table blocks, enumerates exceptional
when a clique is found; dense bit encodings can use one-hot                  assignments, and solves incidence components by spanning trees.
extensions. Otherwise watched-literal CDCL supplies RUP logging,             Compact SAT models are checked, while supported contradictions use
while SAT models are checked against original clauses and                    VeriPB red/rup proofs or, after bounded line-graph reconstruction, pol
unsupported or failed cases return UNKNOWN.                                  proofs using a sequential counter; the debug route has no SAT branch
                                                                             and failures return UNKNOWN.
generic-csp                                                           060
83 GBD instances · 17 validation · baseline 8/17                             glassy-gen                                                           062
                                                                             140 GBD instances · 28 validation · baseline 9/28
Each instance asks whether a ternary constraint problem has one of
four values for every variable while satisfying all relations. Its CNF       The benchmark asks whether a Boolean assignment satisfies every
encoding uses four-literal domain clauses and three-literal clauses          clause in a sparse near-14-regular CNF formula. It uses mostly
forbidding disallowed value triples; the recognized subset has unique        three-literal clauses, at most one two-literal clause, and variables
extension of any two values.                                                 occurring 13 or 14 times, defining a structural envelope rather than the
                                                                             whole family.
Proof format                             No verif.     + verif.     Solved
                                                                             Proof format                             No verif.    + verif.     Solved
GRAT                                     0.702 ×      0.793 ×        3/17
                                                                             GRAT                                     1,340 ×     1,330 ×       28/28
Bounded MAC first applies tuple-mask arc consistency, then the active
CDCL search adds domain and functional clauses and uses conflict             Bit-packed GF(2) elimination treats the three-literal clauses as favored
learning to seek a checked SAT assignment. UNSAT emits DRAT proof            odd-parity equations, then recursive implication-closure repair tests
text for external elaboration and checking; unrecognized formulas or         the candidate; failure falls back to replica-exchange Metropolis search
proof-output failure return UNKNOWN, and the local-search path is            with local CNF repair and reseeding. Only clause-checked SAT
inactive.                                                                    assignments are emitted; unsupported inputs return UNKNOWN and
                                                                             no active UNSAT certificate path exists.
DPR                                      0.892 ×     0.928 ×         6/17
                                                                             DPR                                        4.35 ×     4.35 ×       24/28
Unique-extension propagation builds bootstrap seeds, then four-way
DFS seeks checked SAT assignments and records rejected cubes.                Ordered planted-prefix reconstruction leads the search, followed by
UNSAT is limited to at most 11 seeds and a complete bounded search           GF(2) parity elimination that tests both a solution and its complement;
with an externally checked clause/deletion log; otherwise unbounded          failures fall back to watched-literal 1-UIP CDCL and then open-ended
local search is used, while unrecognized inputs return UNKNOWN.              probSAT repair. Only verified SAT assignments are emitted, while
                                                                             unsupported or unverified cases have no UNSAT/DPR path and return
VeriPB                                   0.820 ×     0.678 ×         6/17    UNKNOWN.
Support filtering and bounded CSP search branch on domains, then
                                                                             VeriPB                                     60.0 ×     60.0 ×       28/28
fall back to watched-literal CDCL with learned clauses when that
search fails; SAT assignments are checked against the original CNF.          Ordered selector reconstruction is tried first, with candidate
UNSAT uses VeriPB text with red witnesses and RUP steps for external         enumeration and CNF verification, followed by packed GF(2)
checking; recognition or proof setup/finalization failure returns            elimination of odd-parity equations; remaining recognized cases use
UNKNOWN.                                                                     XOR annealing and focused probSAT-style search with Hamming-ball
                                                                             repair. Only verified SAT models are emitted; unsupported or
                                                                             unsuccessful searches return UNKNOWN, with no UNSAT/VeriPB
                                                                             certificate path exists.
The Case for Automated Hyperspecialization:
Evidence from SAT

graceful-production                                                   063    graph-isomorphism                                                   065
20 GBD instances · 4 validation · baseline 4/4                               92 GBD instances · 19 validation · baseline 14/19
The benchmark asks whether a structured CNF encoding of                      The benchmark asks whether two colored graphs have a vertex
finite-domain order and equality constraints is satisfiable. Boolean         bijection that preserves the relevant adjacency relations. In the
variables represent semantic choices and auxiliary comparison,               supported CNF form, long clauses require candidate mapping choices,
arithmetic, cardinality, or gate relations, while clauses enforce            while binary clauses forbid incompatible choices.
consistency in a restricted ordered construction.                            Proof format                             No verif.    + verif.    Solved
Proof format                             No verif.       + verif.   Solved   GRAT                                      1.79 ×     1.71 ×       17/19
GRAT                                      6.44 ×         2.08 ×        4/4   After recognizing the restricted candidate-mapping grammar, it tries a
Two-watched-literal propagation drives a positive, increasing-variable       bounded grid-factor shortcut with graph-isomorphism search, then
completion after root units, avoiding branching or backtracking. It          falls back to CDCL with binary-conflict propagation and clause
recognizes only a narrow normalized DIMACS signature; an                     learning. SAT assignments are checked against the original CNF;
independent clause scan verifies the selected-literal SAT witness, while     UNSAT is emitted as textual DRAT for external elaboration, while
root conflicts alone emit a minimal proof artifact and completion            unsupported inputs or failed checks return UNKNOWN.
conflicts or unsupported inputs return UNKNOWN.                              DPR                                      0.476 ×     0.721 ×       0/19
DPR                                     0.0179 ×       0.0418 ×        2/4   It reconstructs recognized graphs, using paired color refinement and
Positive increasing-index construction, driven by watched-literal            individualization search, while a bounded CFI branch solves induced
propagation, is the active technique rather than general SAT search or       GF(2) constraints and falls back on this search. SAT mappings are
a graph-level decoder. It independently checks every original clause         CNF-checked; narrow UNSAT proof search uses Hall/pigeonhole
and emits a clause-covering SAT witness; conflicts, unsupported              branching and RUP/PR only for full instances without phase flips or
inputs, or oversized outputs return UNKNOWN, and no UNSAT or                 repair cells, while other nonisomorphic cases return UNKNOWN.
DPR certificate path is implemented.                                         VeriPB                                   0.476 ×     0.721 ×       0/19
VeriPB                                  0.0179 ×       0.0410 ×        2/4   It solves the recognized incidence structure as an
Parameterized opening-signature recognition selects the supported            independent-transversal problem, using bitset arc consistency and
ordered CNF subset, followed by unit propagation and increasing              minimum-domain DFS with conflict-based support checks. After
positive assignment without DPLL or fallback search. A verified              checking complete assignments against the CNF, it emits SAT models;
essential-variable witness is emitted for SAT; structurally different,       unrecognized shapes and failed searches return UNKNOWN, with no
conflicting, or oversized inputs return UNKNOWN, with no UNSAT or            active UNSAT certificate path.
VeriPB certificate path.
                                                                             gray_codes                                                          066
grandtour-puzzle                                                       064   35 GBD instances · 7 validation · baseline 6/7
20 GBD instances · 4 validation · baseline 4/4                               This benchmark asks whether a cycle of w distinct binary words of
The benchmark asks whether choices can cover every required source           width b exists, with each pair of cyclically adjacent words differing in
while each destination is used at most once. CNF encodings use               exactly one bit. The CNF uses a binary matrix and auxiliary variables
coverage clauses and binary incompatibility clauses; supported               for shifted tracks, XOR relations, and one-bit transitions.
instances have one more source than destination, producing a                 Proof format                             No verif.    + verif.    Solved
pigeonhole contradiction.                                                    GRAT                                     0.683 ×     0.866 ×         5/7
Proof format                             No verif.       + verif.   Solved   A bounded 64-bit exact-cover search over cyclic translates is the SAT
GRAT                                  2.50·104 ×        3,200 ×        4/4   technique, constructing a shifted-track cycle and checking the
Bounded dual-rail recovery and line-graph inversion reconstruct a            resulting assignment against all clauses. If construction fails,
bipartite incidence graph, accepting only a checked connected                watched-literal CDCL is used; unsupported cases may return
component with one more source than destination. A                           UNKNOWN, and UNSAT certificates are emitted as DRAT streams
swap-and-remove reduction then emits ordered DRAT additions,                 ending in empty clause.
including extensions, to the empty clause; recognition, parsing, or          DPR                                      0.673 ×     0.849 ×         5/7
proof-output failure returns UNKNOWN, with no SAT search.                    A bounded residue construction is the primary SAT technique: it
DPR                                   1.17·104 ×         2.99 ×        4/4   chooses periodic transition representatives and track offsets, then
Signed union-find normalization, propagation, and clique checks              checks the assignment against every clause. If construction fails,
recognize a one-over-capacity pigeonhole core, while matching                CDCL is the fallback; unsupported cases return UNKNOWN, and
exposes a Hall circuit. For accepted cores, it adds fresh variables and      root-conflict UNSAT logging records only witness-free learned-clause
emits deletion and witness-free clause additions completing a                additions, ending in empty clause without PR witnesses.
polynomial pigeonhole proof. It does not run SAT search, and                 VeriPB                                   1,540 ×      100 ×         7/7
unsupported or failed cases return UNKNOWN.                                  Bounded canonical cyclic-factor search is the active SAT technique: it
VeriPB                               3.17·104 ×      1.56·104 ×        4/4   enumerates derivative choices and shift lifts, builds words, and checks
Parity union-find collapses equality and complement classes, then            adjacency, uniqueness, and all clauses. Failure invokes no CDCL;
line-graph reconstruction recovers endpoint cliques and the one-unit         counting and parity arguments can emit VeriPB proofs in eligible
source surplus. The solver emits RUP clauses and incremental                 nondivisible or odd-quotient cases, while other recognized cases
pseudo-Boolean at-most-one derivations for a counting proof, but             return UNKNOWN.
performs no SAT search or external proof check; unsupported or failed
cases return UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


greentao                                                            067    hamiltonian                                                              069
12 GBD instances · 3 validation · baseline 0/3                             1,100 GBD instances · 220 validation · baseline 206/220
Green-Tao-style instances ask whether prime arithmetic-progression         The benchmark asks whether a structured monotone CNF has a
edges can be two-colored so every positive edge contains color 1 and       selection of Boolean variables that selects exactly one variable in each
every negative edge contains color 0. In CNF, these two requirements       positive constraint. Pairwise negative clauses forbid selecting variables
are monotone positive and negative clauses.                                that co-occur, reducing the decision question to a restricted
Proof format                             No verif.   + verif.     Solved   exact-cover search.
GRAT                                      1.00 ×     1.00 ×          0/3   Proof format                             No verif.         + verif.    Solved
Stochastic incremental local search repairs violated clauses with          GRAT                                     0.248 ×          0.256 ×     141/220
occurrence-local satisfaction counts, weighted break/make scores,          Focused Metropolis flips and at-most-one-preserving packing searches
restarts, and noisy flips, followed by a longer fallback. Checked          provide SAT attempts, followed by exactly-one CDCL probes. SAT
assignments are certificates and produce SAT output; the inactive          assignments are checked; if no model is found, an unbounded logged
exact proof path leaves failed searches as UNKNOWN, with no UNSAT          CDCL run emits learned clauses and an empty clause as DRAT text for
certificate.                                                               external elaboration and checking, while unsupported, exhausted, or
DPR                                       1.00 ×     1.00 ×          0/3   failed paths return UNKNOWN.
Min-conflicts search leads with negative-edge covers, balanced starts,     DPR                                      0.473 ×          0.483 ×     185/220
and focused flips; failure guides an exact fallback using blocker          Reversible exact-cover search branches on the least-available
reduction, counter propagation, watched clauses, and gain branching.       constraint with reversible bitset buckets; bounded probes precede an
No cutoff applies; it emits witness-free clause additions and an           unbounded pass. Watched-literal CDCL follows a no-model search;
empty-clause UNSAT certificate. SAT has no proof file; unsupported         SAT assignments are checked, while UNSAT runs emit learned clauses
inputs return UNKNOWN.                                                     and an empty clause as witness-free DPR additions for external
VeriPB                                    1.00 ×     1.00 ×         0/3    checking; unsupported layouts or proof failures return UNKNOWN.
With shorter positive clauses, asymmetric greedy hitting-set               VeriPB                                   0.443 ×          0.423 ×     182/220
initialization covers negative edges while avoiding complete positive      CDCL-first search operates only after strict port-layout recognition,
edges; stalled cases use Novelty+ local search with make-break scores,     then falls back after a non-root conflict to Algorithm X with singleton
restarts, and incumbent retention. Checked assignments are printed as      propagation, reversible state, and minimum-row branching. SAT
SAT certificates; no UNSAT or VeriPB certificate path exists, so           models are checked against the CNF; UNSAT reruns emit
unsupported and unsatisfiable inputs return UNKNOWN.                       pseudo-Boolean RUP steps and tree nogoods, while unsupported
                                                                           layouts, some large cases, or proof-output failures return UNKNOWN.
grs-fp-comm                                                         068
64 GBD instances · 13 validation · baseline 1/13                           hamiltonian-cycle                                                        070
The benchmark asks whether a bit-blasted Boolean circuit for               24 GBD instances · 5 validation · baseline 4/5
floating-point commutativity has a satisfying assignment, representing     The benchmark asks whether a sparse graph contains a single cycle
a counterexample. Its CNF uses unit constraints and ordered local          visiting every vertex once. In the recognized CNF layouts, paired
clauses for two- or three-input gates; recognized layouts are restricted   directed-edge selectors enforce one chosen incoming and outgoing arc
and do not independently verify arithmetic semantics.                      per vertex, with auxiliary finite-state counter constraints.
Proof format                             No verif.   + verif.     Solved   Proof format                             No verif.         + verif.    Solved
GRAT                                     0.955 ×     1.12 ×        0/13    GRAT                                       251 ×           233 ×          5/5
Gate-aware root propagation and bounded variable elimination, with         Graph CDCL drives the search with degree-two constraints, DSU
defined outputs avoided as decisions, simplify accepted streams before     component checks, and incremental subtour cuts. Blossom 2-factor
watched-literal first-UIP CDCL on the residual formula. For UNSAT, it      seeds and randomized DFS provide fallbacks; a found cycle is oriented,
emits plain clause additions; unsupported inputs or a conflict-free        completed by watched-literal propagation, and clause-checked, while
completion are reported as UNKNOWN rather than producing a SAT             unsupported or exhausted searches return UNKNOWN rather than an
witness.                                                                   UNSAT certificate.
DPR                                      0.955 ×     1.12 ×        0/13    DPR                                        1.43 ×          1.43 ×         4/5
Repeated failed-literal probing, root shortening, binary-implication       Structural recognition reconstructs the graph, then rollback degree-2
SCC processing, and bounded Davis-Putnam elimination reduce the            search uses subtour propagation and frontier memoization on detected
recognized circuit formula before 1-UIP CDCL on the remainder. Its         narrow strips. A Tutte-style degree-2 factor and bounded exchanges,
UNSAT path buffers derived clause additions, including probe, SCC,         followed by full-CNF CDCL, provide fallbacks; verified assignments
elimination, learned, and contradiction clauses; unsupported inputs or     are emitted, while unsupported layouts or failed SAT-side searches
a satisfying search result are reported as UNKNOWN.                        return UNKNOWN because no UNSAT/DPR certificate path exists.
VeriPB                                   0.955 ×     1.12 ×        0/13    VeriPB                                     1.42 ×          1.41 ×         4/5
Dynamic-cost elimination over gate outputs and binary-implication          Certifying CDCL with VeriPB RUP replay supplies UNSAT
SCC substitution drive preprocessing; fixed-seed local search seeds        certification after a graph-guided probe using blossom matching, Posa
phases for one-UIP CDCL with minimization and restarts. For UNSAT,         rotations, and bounded rollback. Only the supported layouts are
it emits derived and trimmed learned clauses as unhinted RUP steps,        recognized; SAT candidates are completed and clause-checked with
then an empty RUP constraint and conclusion; unsupported layouts or        full assignments, while unsupported inputs or replay divergence yield
SAT exhaustion return UNKNOWN.                                             UNKNOWN and the counter-divisibility helpers remain unused.
The Case for Automated Hyperspecialization:
Evidence from SAT

hanoi                                                                  071    hardware-model-checking                                                073
6 GBD instances · 2 validation · baseline 2/2                                 76 GBD instances · 15 validation · baseline 8/15
The benchmark asks whether a Boolean assignment describes a legal             The benchmark asks whether Boolean signals in a bounded hardware
shortest Towers-of-Hanoi transfer between three pegs. A CNF uses              check can receive values satisfying every constraint. Gate relations,
move, disk, support, and state variables, with clauses enforcing one          initial conditions, and checked outputs become CNF clauses, often in a
move per step, legal support changes, and the initial and goal                structured Tseitin netlist, though encodings may be less regular.
configurations.                                                               Proof format                             No verif.       + verif.    Solved
Proof format                             No verif.        + verif.   Solved   GRAT                                     0.567 ×        0.674 ×        1/15
GRAT                                       159 ×          64.7 ×       2/2    Exact AND/XOR recognition, equivalence probing, and bounded
Structural recognition recovers conditional-frame tracks, transition          variable elimination simplify smaller gate-heavy instances before
order, and endpoint towers for bounded Hanoi signatures. It                   search. Watched-literal CDCL handles larger or unreduced formulas;
recursively constructs the canonical plan, maps moves to action               SAT models are reconstructed and checked, while UNSAT clauses are
variables, propagates units before checking every clause; it has no SAT       logged for external elaboration and malformed or failed internal paths
fallback, and structural, propagation, or verification failure returns        return UNKNOWN.
UNKNOWN, with no UNSAT certificate path.                                      DPR                                      0.794 ×        0.964 ×        5/15
DPR                                  4.57·10 −4 ×    4.63·10 −4 ×      0/2    Conservative gate recognition and canonicalization recover Boolean
Structural recognition accepts only a fixed six-disk, 63-transition           operations, then test structural candidates under negation before
structure, reconstructs its persistent tracks, and synthesizes the            adding RUP-style proof clauses. Within certifying size limits,
canonical plan. It reduces residual clauses to 2-SAT by propagation           watched-literal CDCL handles fallback cases; larger formulas with
and SCC fallback, checks complete assignments against all clauses, and        structural tasks use quotient discovery, while checked SAT
emits SAT only; failures return UNKNOWN, with no UNSAT                        assignments are accepted and proofless UNSAT or failed discovery
certificate path.                                                             return UNKNOWN.
VeriPB                               4.57·10 −4 ×    4.63·10 −4 ×      0/2    VeriPB                                   0.586 ×        0.730 ×        1/15
Recognition recovers the six-disk path and persistent move tracks,            Complemented-edge structural hashing canonicalizes recognized
then forces each moved disk to the canonical optimal sequence.                topologically numbered Tseitin gates, folds simplifications, and checks
Occurrence-based unit completion handles larger frontends, while the          the resulting quotient by propagation. After structural admission,
base residual falls back to learned-clause CDCL. SAT assignments are          internal watched-literal CDCL searches the quotient; without
clause-checked; unsupported or non-SAT cases return UNKNOWN,                  admission or a structural contradiction, the solver returns
and no UNSAT certificate is emitted.                                          UNKNOWN, while SAT assignments are clause-checked and UNSAT
                                                                              ends with a VeriPB RUP certificate.
hardware-bmc                                                           072
49 GBD instances · 10 validation · baseline 6/10                              hardware-verification                                                  074
                                                                              779 GBD instances · 156 validation · baseline 129/156
This benchmark asks whether bounded hardware execution can reach
a bad state while obeying initial and transition constraints. The             The benchmark asks whether Boolean signals in a circuit or
time-unrolled circuit, state, and gate constraints become CNF clauses,        hardware-oriented encoding can satisfy all required constraints. CNF
so SAT gives a witness execution and UNSAT rules out the bound.               typically expresses gate relations together with output, property, or
Proof format                             No verif.        + verif.   Solved
                                                                              state conditions, though the runtime accepts arbitrary DIMACS
                                                                              formulas.
GRAT                                     0.868 ×          1.13 ×      5/10
Structural gate-pattern recognition admits a narrow hardware-CNF              Proof format                             No verif.       + verif.    Solved
subfamily, then bounded variable elimination simplifies it before             GRAT                                     0.637 ×        0.965 ×     106/156
watched-literal CDCL search. SAT assignments are reconstructed and            A bounded AIG sweep recognizes signed-AND gate patterns, simulates
checked against the original CNF; UNSAT runs emit DRAT-style                  assignments in parallel, and may reconstruct a model or add
clause additions, deletions, and an empty clause for external checking,       equivalence clauses after RUP checks. Otherwise it falls back to CDCL.
while rejected inputs, proof-output failure, or failed checks return          SAT models are checked; UNSAT logging records learned additions
UNKNOWN.                                                                      and a root empty clause as DRAT for external checking. Malformed
DPR                                       0.829 ×         1.09 ×      5/10    input returns UNKNOWN.
Wide-gate recognition and incremental assumptions over bad frames             DPR                                      0.460 ×        0.685 ×      83/156
drive search, with propagation and bounded elimination feeding                A size-band portfolio starts with baseline CDCL, then reparses selected
watched-literal CDCL. Rejected frames become complement units;                inputs into a fresh solver with recursive reason minimization. It
SAT models are checked after reverse extension, while UNSAT may               otherwise uses first-UIP learning, watched propagation, activity
log witness-free clause additions, deletions, and an empty clause for         branching, and restarts. SAT assignments are not independently
checking; unrecognized inputs, proof-output failure, or failed                clause-checked; UNSAT output records learned and empty-clause
reconstruction return UNKNOWN.                                                additions without original-clause copies, and malformed input or
VeriPB                                   0.797 ×         0.786 ×      5/10    replay/proof failures return UNKNOWN.
Signed equivalence closure and gate-congruence recognition enable             VeriPB                                   0.526 ×        0.688 ×     97/156
proof-logged substitutions and bounded variable elimination before            A circuit sweep recovers gates, uses bit-parallel signatures and
watched-literal CDCL search. SAT models are reconstructed and                 bounded implication queries, and falls back to CDCL when
checked against the original CNF; supported UNSAT runs emit VeriPB            unproductive. The fallback uses first-UIP learning and Luby restarts;
RUP steps through contradiction, whereas UNSAT outside supported              SAT assignments are clause-checked, while UNSAT output records
certificate profiles or on unrecognized inputs returns UNKNOWN.               learned clauses as VeriPB RUP constraints, an empty contradiction,
                                                                              and an explicit conclusion. Malformed input or certificate failures
                                                                              return UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


hashtable-safety                                                    075    heule-nol                                                           077
21 GBD instances · 5 validation · baseline 1/5                             11 GBD instances · 3 validation · baseline 2/3
These instances are CNF satisfiability queries with numbered Boolean       The benchmark asks whether an L-shaped board can use three colors
variables and clauses. The available solver artifacts do not establish     without a monochromatic equal-arm L, with some cells pinned. The
which hashtable-level property the queries encode.                         CNF gives each cell three color variables, an at-least-one clause, and
Proof format                             No verif.   + verif.     Solved   negative clauses forbidding monochromatic colors on each L.
GRAT                                     0.815 ×     1.10 ×          0/5   Proof format                             No verif.    + verif.    Solved
Packed binary implications are used for propagation in a narrow            GRAT                                       37.4 ×     37.4 ×         3/3
variable-count range, with ordinary watched literals as the fallback. It   Weighted breakout descent uses incidence-local recoloring scores, tabu
runs first-UIP CDCL with activity-based branching, phase saving, and       moves, and restarts to escape local minima. The narrow
restarts, checks SAT assignments, and emits learned clauses as DRAT        canonical-board recognizer validates a found coloring and emits it as
for external elaboration; input, proof, or exception failures return       the SAT witness; unsupported inputs return UNKNOWN, while
UNKNOWN.                                                                   unresolved recognized cases can remain in the restart loop because no
DPR                                      0.815 ×     1.10 ×          0/5   UNSAT certificate path is implemented.
A strict CNF profile gate admits only very large, mostly short-clause      DPR                                        13.4 ×     13.4 ×         3/3
formulas with many units; accepted inputs use two-watch CDCL with          Incremental breakout local search combines weighted incident scores,
1-UIP learning. Checked SAT models are reported, while UNSAT               smoothing, and deterministic restart salts. The exact 22 by 22, n=11
output uses witness-free DPR clause additions, a final empty clause,       recognizer searches one-hot colorings although its raw clauses lack
and only the first parsed original unit; unsupported or output failures    at-most-one constraints; it emits checked SAT assignments, proves
return UNKNOWN.                                                            only a directly forced monochromatic L by an empty clause, and
VeriPB                                   0.815 ×     1.09 ×         0/5    unresolved cases can remain in the restart loop.
A fixed signature gate accepts only a narrow normalized bit-blasted        VeriPB                                     194 ×      191 ×          3/3
CNF pattern; accepted inputs use watched-literal CDCL with 1-UIP           Incremental weighted min-conflicts local search evaluates six
learning and activity-based branching. UNSAT conflicts are logged as       recolorings around a violated corner, using noise, breakout weights,
VeriPB RUP constraints with hints and a final empty RUP, while SAT         and deterministic restarts. After exact recognition for n <= 64,
returns a checked assignment; unsupported or malformed inputs              unsupported inputs return UNKNOWN; VeriPB pol or RUP certificates
return UNKNOWN.                                                            cover only two restricted UNSAT triggers, while checked SAT
                                                                           assignments are emitted and other unresolved cases may continue
heule-folkman                                                       076    indefinitely.
11 GBD instances · 3 validation · baseline 3/3
The benchmark asks whether the edges of a K4-free graph can receive        hgen                                                                078
two colors so every triangle is non-monochromatic. A CNF                   336 GBD instances · 68 validation · baseline 36/68
representation uses one variable per edge and an                           These benchmarks ask whether a Boolean assignment satisfies a
all-positive/all-negative clause pair per triangle, requiring its three    DIMACS CNF, usually with bounded-width clauses and regular
values not to be all equal.                                                occurrence, density, and polarity patterns. Some encodings use disjoint
Proof format                             No verif.   + verif.     Solved   four-literal choice clauses and signed binary exclusions whose hole
GRAT                                       429 ×      419 ×          3/3   components are one fewer than choice groups.
Focused local search attacks monochromatic triangles with weighted         Proof format                             No verif.    + verif.    Solved
break-score flips and updates, then falls back to watched-literal CDCL     GRAT                                       1.32 ×     1.30 ×      42/68
when bounded search fails. SAT assignments are checked before              Configuration-checking and ProbSAT-style local search maintains
emission; CDCL UNSAT logs textual DRAT and emits the empty                 true-literal counts and a false-clause set, then uses unbounded focused
clause after a root conflict for external elaboration, while unsupported   restarts when attempts find no model. An elimination route uses
inputs return UNKNOWN.                                                     watched-literal CDCL with first-UIP learning and writes learned
DPR                                        1.83 ×    1.83 ×          3/3   clauses as textual DRAT additions for external elaboration; the
NAE local search uses focused bad-triangle walks and                       local-search route has no UNSAT result path.
breakout/probSAT choices, then tries vertex cut-switching, bounded         DPR                                       1.64 ×      1.53 ×      47/68
repair, elimination, and CDCL. SAT candidates are checked on the           A structural sparse-pigeonhole detector first constructs a
original; reduced UNSAT is rerun untouched, logging additions that         RUP/PR/RAT-style certificate with deletions and witness-free clause
may be witness-free and emitting the empty clause only after a root        additions; the writer is not internally checked. Otherwise focused
conflict for external checking; unsupported inputs return UNKNOWN.         stochastic local search uses break counts, weighted choices, restarts,
VeriPB                                     104 ×     98.2 ×         3/3    and an active WalkSAT-style mode. Regular recognized formulas have
NAE WalkSAT first maintains monochromatic triangles incrementally          no UNSAT certificate route; failed assignments are reported
across noise restarts and an alternate sampler, then falls back to         UNKNOWN.
watched-literal CDCL seeded with its best phase and a color-symmetry       VeriPB                                     1.61 ×    1.63 ×       47/68
fixing. A complete assignment is expanded and checked against the          A direct pigeonhole detector emits a VeriPB-style proof by deriving
original clauses; unrecognized or exhausted cases return UNKNOWN           hole at-most-one constraints and summing them with four-choice
because no UNSAT certificate path is implemented.                          clauses. Other CNFs use inverse-power local search with spectral
                                                                           restarts, then CDCL with RUP logging; only the exact pigeonhole
                                                                           structure has a direct proof path, while failed paths can return
                                                                           UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

hidoku                                                             079    independent-set                                                    081
34 GBD instances · 7 validation · baseline 7/7                            30 GBD instances · 6 validation · baseline 2/6
The benchmark asks whether an n by n grid can place 1 through n^2         The benchmark asks whether exactly K of N=2^d binary-word vertices
exactly once, respect fixed clues, and put consecutive values in          can be selected without selecting both ends of a graph edge. CNF uses
king-adjacent cells. CNF encodings use cell-value variables, exact-one    one selection variable per vertex, clauses forbidding both endpoints of
constraints, clue units, and adjacency implications, sometimes with       each edge, and auxiliary one-hot running-count variables enforcing
auxiliary variables.                                                      the exact total.
Proof format                             No verif.    + verif.   Solved   Proof format                             No verif.   + verif.    Solved
GRAT                                    0.0818 ×     0.202 ×        0/7   GRAT                                       1.17 ×    1.29 ×         2/6
It enumerates a bounded set of row-wise Hamiltonian snake                 Weighted-syndrome construction is tried first for Z-channel graphs,
assignments under board symmetries, fixing the primary cell-value         followed by specialized exact or bit-parallel complement-clique search
variables before searching auxiliary variables. Watched-literal DPLL      and bounded local search on remaining recognized cases. Candidates
completes and independently checks the CNF before emitting a total        are given counter values and fully rechecked before SAT output; failed
SAT assignment; unrecognized or unsuccessful cases return                 or unsupported inputs return UNKNOWN, with no UNSAT or DRAT
UNKNOWN, and no UNSAT certificate path is implemented.                    certificate path.
DPR                                        163 ×     0.278 ×        7/7   DPR                                        1.17 ×    1.29 ×         2/6
It tries row-boustrophedon snakes on presumed primary variables,          Layered complement-graph clique search drives construction, using
then uses propagation and recursive DPLL to complete and check the        Hamming-weight layers and bit-parallel branch-and-bound for
CNF before emitting a SAT assignment. A specialized recognizer            transposition graphs, while deterministic local search handles other
constructs a clause/deletion trace for a diagonal crossing and reports    recognized cases. After assigning the running-count auxiliaries, it
UNSAT only on contradiction, but covers only narrowly recognized          rechecks every clause before emitting a SAT assignment; failed or
6x6 and 7x7 encodings; other failures return UNKNOWN.                     unsupported cases return UNKNOWN, and no UNSAT or DPR
VeriPB                                   8,980 ×     2,620 ×       7/7    certificate path is implemented.
It recognizes a nested-AMO and king-neighbor encoding and, for a          VeriPB                                    4.63 ×     3.62 ×        5/6
geometric clue obstruction, emits a VeriPB certificate using PB and       Component decomposition and complement-clique search solve
RUP derivations. Otherwise it tries symmetric row snakes, then            suitable cases exactly, while residual-degree greedy and exchange
clue-aware Hamiltonian-path search with distance and connectivity         search cover larger graphs. A found SAT assignment reconstructs the
pruning; SAT models are checked before emission, while failed or          automaton and is checked against every clause; only narrow
unrecognized cases return UNKNOWN.                                        component-tree, transposition, and Z-channel branches emit VeriPB
                                                                          UNSAT proofs, while other failures or unsupported cases return
                                                                          UNKNOWN.
hypertree-decomposition                                            080
56 GBD instances · 12 validation · baseline 8/12
                                                                          independent-set-reconfiguration                                    082
The benchmark asks whether a hypergraph has an elimination order
                                                                          20 GBD instances · 4 validation · baseline 0/4
whose resulting bags satisfy the hypertree-width bound, with each bag
covered by at most k hyperedges and special conditions. A CNF             Given a graph and two same-size independent sets, the task asks
records order, completion relations, bag selections, and bound            whether one can reach the other through a specified-length sequence
constraints. Recognizers may support restricted encodings.                of distinct independent sets, replacing one vertex at each step. CNF
                                                                          encodings represent graph edges, configurations, transitions, and
Proof format                             No verif.    + verif.   Solved
                                                                          endpoint constraints.
GRAT                                       1.23 ×     1.23 ×      7/12
Recognizes a fixed CNF layout, constructs a primal elimination order      Proof format                             No verif.   + verif.    Solved
with dual min-fill trials, then searches bag hyperedge covers, using      GRAT                                       2.00 ×    2.00 ×         2/4
bounded branching only for smaller widths. Rollback Horn                  Target-directed bitset exploration builds the token-jumping
propagation completes remaining variables, after which every clause is    component, then randomized shortest-path-guided trials seek a simple
checked before SAT output; unsupported layouts, width rejection, or       path of the prescribed length. A completed path is propagated and
failed construction/search return UNKNOWN, with no UNSAT                  checked against the CNF for SAT; bounded component, parity, and
certificate path.                                                         small-clique routines write DRAT-style UNSAT certificates, while
                                                                          unrecognized or unresolved cases return UNKNOWN.
DPR                                       1.23 ×      1.16 ×      7/12
Recognizes degree-two incidence and an exact dual-line-graph primal       DPR                                       3.95 ×     3.90 ×         3/4
graph, then fixes a primal order by greedy dual minimum-fill              Guarded structural routines emit PHP/RUP-style derivations,
completion. A watched-literal backtracking search solves remaining        including witness-free clause additions, for a few UNSAT cases;
guard, special-condition, and counter variables, with limited seed        otherwise bidirectional BFS with bounded randomized walks and ear
retries; structural rejection or unsolved residual returns UNKNOWN,       insertion seeks a simple path of the required length. Propagation and
and no DPR derivation or UNSAT certificate path is implemented.           clause rescanning complete SAT models; unsupported layouts or
                                                                          unresolved searches return UNKNOWN, with no general UNSAT path.
VeriPB                                   0.517 ×     0.522 ×      0/12
Uses randomized local search over orders, with bitset branching for       VeriPB                                     2.00 ×    1.99 ×        2/4
bounded bag covers and restarts. After an order is found, it fixes arcs   Specialized pseudo-Boolean proof generators run first, while bit-mask
and selectors, uses Horn propagation for remaining variables, and         token-jump generation and component enumeration support
checks every clause before SAT output; unsupported layouts or failed      distance-pruned exact-length DFS or seeded restarts. SAT paths are
search/completion return UNKNOWN, with no VeriPB or UNSAT                 propagated and rescanned against the CNF; no generic CDCL proof
certificate path.                                                         fallback is enabled, so unrecognized or unresolved cases return
                                                                          UNKNOWN.
                                                                                                   Harrison Green, Claire Le Goues, and Fraser Brown


influence-maximization                                               083    karatsuba-multiplication                                              085
20 GBD instances · 4 validation · baseline 0/4                              3 GBD instances · 1 validation · baseline 1/1
The benchmark asks whether at most K seed nodes in a directed graph         These CNFs ask whether two odd, nontrivial binary factors satisfy a
can activate at least T nodes within ten synchronous threshold rounds,      bit-blasted Karatsuba encoding of a fixed odd product. Factor bits and
with seeds remaining active. A CNF represents seed choices, activity        auxiliary circuit variables are linked by clauses, making the
states, threshold propagation, and cardinality limits.                      benchmark a Boolean satisfiability question.
Proof format                             No verif.    + verif.    Solved    Proof format                             No verif.    + verif.    Solved
GRAT                                       1.33 ×     1.33 ×         1/4    GRAT                                     0.115 ×     0.115 ×          0/1
Greedy seed construction and simulated-annealing swaps guide                Composite odd-prefix probing guides modular-inverse recovery and
threshold diffusion on the recognized encoding. A watched-literal           watched-literal recursive DFS, prioritizing factor bits before auxiliary
CDCL fallback handles unsuccessful searches without an internal stop        variables; clause learning, available prime tries, and factor-order
condition; unresolved cases can return UNKNOWN. SAT checks a                symmetry prune the search. Only a checked satisfying assignment is
total assignment; UNSAT logs learned clauses and an empty clause as         emitted; no UNSAT certificate is implemented, so unsupported layouts,
DRAT additions for external elaboration.                                    contradictions, and exhausted searches return UNKNOWN.
DPR                                       1.33 ×      1.33 ×         1/4    DPR                                      0.115 ×     0.115 ×          0/1
Bit-parallel diffusion simulation drives greedy and annealed                Low-column residue decoding with modular-inverse propagation
fixed-cardinality seed search on recognized layouts. If it fails, a         drives watched-literal recursive DFS, prioritizing factor bits before
watchdog-free CDCL fallback adds reduction, elimination, and                branching on remaining variables; prime and exact-width checks
learning clauses; unresolved or rejected models return UNKNOWN.             prune completed candidates. It emits a checked satisfying assignment
SAT requires a total satisfying assignment; UNSAT requires potentially      but has no UNSAT certificate or generic fallback, so unsupported
witness-free RUP additions to derive the empty clause.                      layouts, contradictions, and failed searches return UNKNOWN.
VeriPB                                     1.33 ×     1.33 ×         1/4    VeriPB                                   0.115 ×     0.115 ×          0/1
Bitset threshold simulation scores greedy additions and annealed            Adaptive modular-residue recovery guides discrepancy-ordered factor
fixed-cardinality swaps on the recognized ten-layer layout.                 search on recognized layouts, while bounded CDCL completes
Activity-guided CDCL is conflict-bounded, so failed heuristic search or     auxiliary variables and a general CDCL loop handles backdoor failure.
unfinished fallback returns UNKNOWN. SAT requires a checked                 Every reported assignment is checked against the original clauses; no
assignment; UNSAT is reported only after level-zero closure with            UNSAT certificate path exists, so heuristic failure, contradictions, or
VeriPB RUP constraints and deletions.                                       unsuccessful completion return UNKNOWN.

interval-matching                                                    084    knights-problem                                                       086
23 GBD instances · 5 validation · baseline 0/5                              21 GBD instances · 5 validation · baseline 2/5
The benchmark asks whether each group can choose one option                 The benchmark asks whether an even square board has a closed
without using a resource clique twice. Its CNF expresses choices with       knight tour, a cycle of legal knight moves that visits every square
at-least-one clauses and conflicts with binary clauses, reducing the        exactly once. CNF encodings select these moves, with auxiliary
question to a matching that covers every group.                             variables enforcing one-to-one incidence or position conditions.
Proof format                             No verif.    + verif.    Solved    Proof format                             No verif.    + verif.    Solved
GRAT                                  2.97·104 ×      17.9 ×         5/5    GRAT                                       3.34 ×     3.49 ×          4/5
Parity-DSU polarity recovery normalizes recognized clauses into rows        Structural graph recovery is the distinguishing technique: recognized
and conflict cliques; augmenting-path matching constructs and checks        CNFs are matched to an even-board knight graph before a randomized
a full assignment against every original clause. After a Hall deficiency,   Warnsdorff-style search selects a closed tour. Propagation and
alternating reachability feeds a fresh-variable pigeonhole reduction        bounded completion fill the remaining variables and check all clauses,
emitting definition, row, conflict, and empty clauses for UNSAT;            but failed recognition or search yields UNKNOWN; no general fallback
unsupported structure or proof failure returns UNKNOWN.                     or UNSAT certificate path is implemented.
DPR                                   1.26·105 ×       208 ×         5/5    DPR                                       3.34 ×      3.48 ×          4/5
Augmenting-path matching builds a complete assignment, checked              Structural encoding recognition recovers the knight graph and move
against every original clause before SAT is reported. For a deficient       groups, then randomized Warnsdorff search proposes a tour;
matching, Hall validation and bitset-guided swap planning must              propagation and bounded residual DPLL complete the assignment. For
succeed; the PR-style writer emits swap records, unit clauses, and an       unary and binary formulas, SCC reasoning can certify UNSAT with
empty clause for UNSAT, while recognition, model-check, planning, or        contradictory unit clauses and an empty clause; unsupported
proof-output failures return UNKNOWN.                                       encodings or failed search return UNKNOWN.
VeriPB                               1.50·105 ×      4,220 ×         5/5    VeriPB                                     1.67 ×     1.74 ×          3/5
Augmenting-path matching on recognized signed group/resource                Stable-color refinement and constrained backtracking recover
structure yields a complete assignment checked against every original       knight-graph structure only for validated layouts, after which a
clause before SAT is reported. For a deficient matching, alternating        Warnsdorff-style search selects a closed tour. Watched-literal
reachability supplies a Hall witness for a pseudo-Boolean derivation        propagation and bounded residual completion check the full clauses,
combining group clauses and clique bounds to derive an empty clause;        but unsupported layouts or failed construction return UNKNOWN; no
recognition, model-check, or certificate failures return UNKNOWN.           UNSAT certificate path is implemented.
The Case for Automated Hyperspecialization:
Evidence from SAT

ktf                                                                087    linvrinv                                                              089
20 GBD instances · 4 validation · baseline 2/4                            12 GBD instances · 3 validation · baseline 1/3
KTF instances ask whether a team can be selected from conflict groups     The benchmark asks whether n by n Boolean matrices over GF(2) can
so each skill is covered at least a required number of times within a     satisfy AB = I but not BA = I, testing one-sided inversion. The CNF
weight budget. The CNF uses agent variables, skill counts, conflict       uses matrix variables and AND/XOR auxiliaries, with a clause
cliques, and a budget constraint.                                         requiring BA to differ from I.
Proof format                             No verif.    + verif.   Solved   Proof format                             No verif.       + verif.   Solved
GRAT                                     0.511 ×     0.511 ×        0/4   GRAT                                       1.00 ×        1.00 ×       1/3
Bounded auxiliary-only elimination is followed by watched-literal         A narrow structural signature drives watched-literal CDCL, preferring
CDCL, with learned clauses and positive-first branching. SAT              variables with the expected gate-occurrence pattern and otherwise
reconstructs eliminated variables and checks the CNF; UNSAT at level      using activity-based decisions. First-UIP learning, restarts, phase
zero is logged with clause additions and an empty clause for external     saving, and clause reduction guide search; UNSAT emits textual DRAT
DRAT elaboration, while unsupported input or internal failure returns     for external elaboration, while SAT returns a checked assignment and
UNKNOWN.                                                                  malformed, unsupported, or proof-file failures return UNKNOWN.
DPR                                        1.02 ×     1.02 ×        2/4   DPR                                       1.00 ×         1.00 ×       1/3
It recognizes a narrow nested clique-and-skill encoding, compresses       XOR/AND flattening turns recognized networks up to four into parity
each clique to a level, and tries rarity-weighted greedy constructions.   clauses before two-watch CDCL, retaining the original CNF if
It completes auxiliaries and checks every clause for SAT; only demand     flattening fails. First-UIP learning produces a textual DPR trace with
two enables watched-literal CDCL with witness-free clause additions       parity, learned-clause, deletion, and empty-clause records on UNSAT;
for UNSAT, while other failures or unrecognized layouts return            SAT returns a checked assignment, while malformed, unsupported, or
UNKNOWN.                                                                  larger inputs return UNKNOWN.
VeriPB                                   1,440 ×      62.6 ×       4/4    VeriPB                                     1.00 ×        1.00 ×       1/3
An integer-dual search tests whether skill lower bounds exceed the        Algebraic decoding reconstructs matrices and, at orders four and five,
decoded budget, emitting a pseudo-Boolean proof on success.               enumerates vectors for an injection-surjection VeriPB certificate.
Otherwise, randomized cost-aware construction and fail-first              Other cases below six, or decoder failures, use watched-literal CDCL
branching seek SAT models, complete auxiliaries by propagation, and       with First-UIP learning and RUP logging; malformed or unsupported
check clauses; unsupported structures or exhausted search return          inputs and orders six or larger return UNKNOWN, and SAT returns a
UNKNOWN, with no general UNSAT fallback.                                  checked assignment.

lam-discrete-geometry                                              088    long-learned-clauses                                                  090
20 GBD instances · 4 validation · baseline 3/4                            16 GBD instances · 4 validation · baseline 0/4
These CNFs ask whether a partially fixed incidence structure can be       This benchmark asks whether a Boolean assignment satisfies every
completed by selecting incidence variables so required sets are hit       clause in a structured CNF formula. The clauses encode local relations
while incompatible pairs and small forbidden patterns are avoided.        and, in some instances, larger counting or graph-linked layouts.
They use restricted row-based encodings, sometimes with auxiliary         Proof format                             No verif.       + verif.   Solved
intersection variables.                                                   GRAT                                       4.00 ×        3.96 ×       3/4
Proof format                             No verif.    + verif.   Solved   Small XOR truth-table blocks are grouped into incidence components;
GRAT                                     0.401 ×     0.619 ×        0/4   an odd-RHS, zero-incidence component triggers fresh XOR gates,
The supported pure 111-stride path uses a perfect-matching                resolution projections, and balanced-tree rotations for a refutation.
configuration lift, grouping incidence variables into row                 The refutation is written as DRAT for external elaboration and
configurations and searching an exact-cover problem with bitset           checking; otherwise bounded randomized search checks models, and
incompatibility masks and minimum-options branching. It has no            unsupported or failed cases return UNKNOWN.
generic fallback: unsupported structures return UNKNOWN, while            DPR                                        4.00 ×        3.95 ×       3/4
UNSAT explanations are emitted as textual DRAT additions for              Small clauses become 2-4-variable parity relations; sparse XOR
external elaboration and checking.                                        expressions and greedy overlap cancellation refute the odd-aggregate,
DPR                                      0.401 ×     0.619 ×        0/4   two-occurrence case with witness-free DPR additions for external
A domain-level search enumerates legal row domains for the compact        elaboration and checking. Otherwise, bipartite flow handles a relaxed
stride-111 layout, propagating compatibility with bit masks and           exact-two four-variable pattern with one binary relation and builds a
chronological branching. If the specialized path does not establish       clause-checked model; unsupported cases return UNKNOWN.
UNSAT, watched-literal CDCL with learned clauses and restarts is          VeriPB                               1.59·105 ×      1.20·104 ×       4/4
used; unsupported signatures return UNKNOWN, and UNSAT output             Sequential-counter and clique-covered graph layouts are recognized
is a witness-free clause-addition stream for external elaboration and     first, yielding a non-branching pseudo-Boolean proof of contradiction.
checking.                                                                 Compact groups use parity tests or fewest-mask branching for a
VeriPB                                   0.401 ×     0.619 ×       0/4    clause-checked model; structural proofs use only recognized clauses. A
Semantic failed-literal probing and incidence-specific preprocessing      bounded TreeRup fallback can emit a RUP proof, and unrecognized or
prepare accepted instances for two-watched-literal CDCL, using            uncertified paths return UNKNOWN.
first-UIP minimization, semantic phases, and Luby restarts. The
bounded detector has no generic fallback: rejected inputs return
UNKNOWN, while UNSAT attempts produce a VeriPB-style RUP
proof for external checking and proof-creation failure also returns
UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


matrix-multiplication                                               091    maxsat-optimum                                                       093
53 GBD instances · 11 validation · baseline 7/11                           60 GBD instances · 12 validation · baseline 9/12
These benchmarks ask whether a matrix-multiplication tensor over           The benchmark asks whether a Boolean assignment satisfies hard
GF(2) can be expressed as a bounded sum of rank-one tensors. CNF           clauses while using no more than a specified number of soft-constraint
variables encode factor coefficients and auxiliary products, while         relaxations. CNF encodings may express this bound with counters or
parity constraints require the resulting tensor entries to match.          structured choice, conflict, coverage, or selector gadgets, so recognized
Proof format                             No verif.     + verif.   Solved   forms are restricted rather than universal.
GRAT                                     0.978 ×     0.987 ×       7/11    Proof format                             No verif.     + verif.    Solved
Structural recognizers recover tensor factors from AND/parity              GRAT                                     0.348 ×      0.373 ×       0/12
connectivity and try rank-six proof bridges or the embedded rank-23        Structured order-counter and selector recognition activates
construction, completing auxiliary variables by propagation before         destroy/rebuild, crossover, and weighted neighborhood search, with a
falling back to watched-literal CDCL. SAT models are clause-checked;       fresh SAT solve validating each extended candidate. Unrecognized
UNSAT proof output is textual DRAT, with rank-six branches                 inputs use watched-literal CDCL with textual DRAT-style logging;
remapping bundled binary proof assets.                                     specialized branches emit SAT models but lack an UNSAT certificate
DPR                                      0.373 ×      0.382 ×      0/11    and may return UNKNOWN or continue indefinitely.
An exact recognizer for the checked rank-23 Brent structure                DPR                                      0.348 ×      0.373 ×       0/12
canonicalizes the GF(2) tensor, searches the embedded Laderman orbit,      Exact-schema recognition activates least-model Horn closure and
and propagates auxiliaries. Only nine compact signatures reach             support-counted local search over choices, emitting checked SAT
watched-literal CDCL; SAT assignments are checked, compact UNSAT           models. If that path fails or is inapplicable, watched-literal CDCL
logs witness-free DPR additions and an empty clause, while                 solves the original CNF and logs learned clauses as witness-free DPR
unsupported inputs or proof failures return UNKNOWN.                       additions. It tests only K, not a global optimum; exhaustion may return
VeriPB                                   0.937 ×      0.957 ×      7/11    UNKNOWN, and immediate-conflict UNSAT lacks proof logging.
Exact structural recognizers recover the 3x3 rank-23 Laderman              VeriPB                                   0.407 ×     0.436 ×        2/12
structure or a rank-10 parity chain, using GF(2) elimination for           Focused clause-weighted local search handles synthesis-shaped CNFs
residuals and a basis model for rank 10. Eligible cases use                by flipping variables from false clauses and increasing weights on
watched-literal CDCL with RUP logging; direct SAT returns checked          trapped clauses, returning only checked SAT models and no UNSAT
assignments, while hard-listed or oversized cases return UNKNOWN           proof path. Other recognized forms undergo subsumption, bounded
without an UNSAT certificate.                                              variable elimination, and watched-literal CDCL with reconstructed
                                                                           assignments and VeriPB/RUP UNSAT logging; unsupported inputs or
maximum-constraint-partition                                        092    configured limits can yield UNKNOWN.
10 GBD instances · 2 validation · baseline 2/2
The benchmark asks whether 100 of 200 weighted items can be chosen         md5-equivalence-checking                                             094
so their total equals that of the remaining 100. Its CNF uses selector     20 GBD instances · 4 validation · baseline 4/4
variables plus auxiliary cardinality and binary-sum circuitry, with        The benchmark asks whether a structured Boolean computation can
equality outputs enforcing matching totals.                                be assigned values that satisfy its circuit constraints and a terminal
Proof format                             No verif.     + verif.   Solved   comparison. CNF uses circuit and state variables with gate and control
GRAT                                    0.0797 ×     0.0798 ×        1/2   clauses, but recognized instances follow exact layouts rather than
Bit-parallel evaluation of singleton scenarios recovers weights and        arbitrary encodings.
total from the recognized 200-selector circuit, then dispatches by         Proof format                             No verif.     + verif.    Solved
parity. Odd totals use least-significant-bit Davis-Putnam elimination      GRAT                                     0.113 ×     0.218 ×         3/4
and can emit DRAT additions for elaboration and checking; even totals      Occurrence-based unit propagation drives a DIMACS-order
use cardinality-grouped meet-in-the-middle search, but have no             lucky-model construction, setting remaining encountered literals false
UNSAT path; unsupported layouts or failures return UNKNOWN.                and retrying with reversed order and phase choices within the
DPR                                       1,060 ×     74.5 ×         2/2   bounded affine family. It checks every retained clause before emitting
Bit-parallel singleton evaluation recovers weights and total from the      a complete satisfying assignment; malformed, unsupported, or failed
recognized circuit, then dispatches by parity. Odd totals use a            attempts return UNKNOWN, and no UNSAT path is implemented.
least-significant-bit slice with minimum-occurrence-product                DPR                                     0.0382 ×     0.0739 ×        1/4
Davis-Putnam elimination and witness-free clause additions for             Fixed-point construction leads: occurrence-list propagation builds a
UNSAT; even totals use cardinality-grouped meet-in-the-middle              base assignment, reuses its stable state across middle stages, and
search for checked models, while unsupported layouts or failures           watched-literal DPLL searches the two terminal stages as fallback. It
return UNKNOWN.                                                            checks shifted clauses and terminal gates before emitting a complete
VeriPB                                   1,610 ×       70.9 ×       2/2    assignment; failed or unsupported cases return UNKNOWN, with no
Scenario evaluation recovers weights and complementary sums from           UNSAT certificate path.
the recognized circuit, then dispatches by parity. Odd totals use affine   VeriPB                                  0.0381 ×     0.0737 ×        1/4
GF(2) cone analysis to emit a pseudo-Boolean proof with RUP                Exact structural recognition recovers equality cones and variable
contradiction; even totals use greedy balancing and bounded                relationships, then a fixed-point loop flips a target or free leaf while
exchanges for checked models but have no UNSAT path, while                 streaming gate evaluation. It handles only the default bounded
unsupported structures or failures return UNKNOWN.                         recognized layout and checks every original clause before emitting a
                                                                           complete assignment; failures return UNKNOWN, with no UNSAT
                                                                           certificate path.
The Case for Automated Hyperspecialization:
Evidence from SAT

mechanical-master-key                                                 095    minimal-superpermutation                                           097
20 GBD instances · 4 validation · baseline 0/4                               46 GBD instances · 10 validation · baseline 7/10
The benchmark asks whether keys can receive bounded-jump                     The benchmark asks whether a fixed-length word over n symbols
cut-depth words so every lock separates each unauthorized key from           contains each required permutation as a contiguous substring. CNF
its authorized keys at some position, with CNF using one-hot                 encodes symbols at positions and links possible windows to
key-depth variables, lock-depth variables, and separation witnesses.         occurrence, coverage, and cardinality constraints through auxiliary
Proof format                             No verif.       + verif.   Solved   variables.
GRAT                                      5.27 ×         5.25 ×       4/4    Proof format                             No verif.   + verif.   Solved
Weighted local search assigns legal bounded-jump words to keys,              GRAT                                  2.54·104 ×     57.1 ×      10/10
scoring unauthorized pairs by authorized-depth counts and using              Hard-coded construction dispatch seeds candidate words, then
whole-word moves, breakout weighting, and restarts. It accepts only          whole-formula propagation and clause checking produce SAT
the D=4, P=8 layout, checks the reconstructed SAT assignment, and            assignments for supported layouts. If this fails on the recognized n=4
returns UNKNOWN when recognition, search, or checking fails; no              forbidden-canonical signature, occurrence-placement DFS emits
UNSAT certificate path is implemented.                                       RUP-style context clauses through a replayed recipe or semantic
DPR                                        3.59 ×        3.48 ×       3/4    fallback; other or unverified cases return UNKNOWN.
Enumerated legal bounded-jump paths feed weighted local search,              DPR                                  5.20·104 ×      54.8 ×      10/10
tracking authorization counts and violated pairs with whole-word             Fixed-witness seeding and indexed unit propagation test hard-coded
moves and breakout weighting. It accepts only the exact CNF layout,          n=4 and n=5 constructions, with bounded residual enumeration and a
checks reconstructed SAT assignments, and returns UNKNOWN for                complete clause check before SAT output. Six exact n=4 variable-count
unsupported inputs or search failure; its proof fallback is disabled, so     and clause-structure cases use occurrence-window DPLL with copied
no UNSAT result is implemented.                                              or regenerated DPR occurrence-cover templates for UNSAT
VeriPB                                     1.71 ×        1.69 ×       2/4    certificates; unsupported inputs or failed residual completion return
Exact recognition gates sparse counterexample-repair, moving                 UNKNOWN.
violating keys toward absent depths or unique authorized users with          VeriPB                                     520 ×     80.8 ×      10/10
per-lock masks and counts. Other cases use legal words, whole-word           Coverage-first branching drives watched-literal completion after
RUP additions, and key-space CDCL with auxiliary elimination; SAT            pinning shape-recognized formulas to canonical constructions, with
models are clause-checked, root conflicts yield UNSAT, while failures        chronological backtracking and full clause checks before SAT output.
or unsupported inputs yield UNKNOWN.                                         If completion fails, only n=4 cases enter proof-logging CDCL on
                                                                             uncovered permutation blocks, with VeriPB chains for UNSAT; n=5
                                                                             failures and unrecognized or unresolved searches return UNKNOWN.
minimal-disagreement-parity                                           096
29 GBD instances · 6 validation · baseline 1/6
The benchmark asks whether shared Boolean variables produce parity           minimum-disagreement-parity                                        098
outputs that disagree with observations within a bounded limit. Its          30 GBD instances · 6 validation · baseline 0/6
CNF uses XOR or equality auxiliaries, a counter for the disagreement         The benchmark asks whether a binary source assignment induces
bound, and can include ordinary residual clauses.                            affine parity outputs with at most K disagreement bits. It encodes the
Proof format                             No verif.       + verif.   Solved   parity relations and Hamming-weight bound in CNF using auxiliary
GRAT                                 2.65·105 ×      1.02·105 ×       6/6    variables, while concrete encodings may vary.
Affine decoding through a weighted union-find and bit-parallel               Proof format                             No verif.   + verif.   Solved
Gaussian elimination is the main strategy. It enumerates bounded             GRAT                                      5.39 ×     4.45 ×        5/6
error patterns, then completes auxiliary and weakened-chain variables        Dual-syndrome meet-in-the-middle decoding uses GF(2) elimination to
with watched-literal search, verifies the full CNF, and prints SAT only      enumerate bounded supports and recover a checked assignment for
then; unsupported recognition or failed decoding returns UNKNOWN,            the recognized canonical XOR-and-counter layout. If it fails, CDCL
with no UNSAT certificate path.                                              adds proof-only XOR consequences, emits DRAT for external
DPR                                        53.2 ×        53.1 ×       6/6    checking, and reports UNSAT only after a root conflict; unsupported
GF(2) elimination, min-fill factor decomposition, and                        or inconclusive cases return UNKNOWN.
separator/syndrome joins are the central search strategy. Junction-tree      DPR                                        3.00 ×    3.00 ×        4/6
messages aid bounded reconstruction, and recovered assignments are           Affine reconstruction recovers the map, then Gray-code
back-substituted and checked against every input clause before SAT is        meet-in-the-middle search indexes partial outputs and tests bounded
printed; unsupported or failed paths return UNKNOWN with no                  Hamming neighborhoods for a source assignment. The candidate is
UNSAT certificate path.                                                      propagated and checked against every clause before SAT output;
VeriPB                                2.96·104 ×     2.54·104 ×       6/6    restricted layouts, capacity limits, failed search, or no model yield
Affine-mask propagation and Gaussian-elimination syndrome                    UNKNOWN, with no UNSAT certificate path implemented.
decoding drive the active search on recognized fixed-shape encodings.        VeriPB                                     3.00 ×    3.00 ×        4/6
It enumerates bounded errors, checks decoded witnesses against the           Lee-Brickell information-set decoding samples syndrome positions,
CNF, uses DPLL for a narrow weakened branch, and returns                     solves binary systems, and tests low-error candidates with packed
UNKNOWN for unsupported or failed cases; its VeriPB proof routine            parity operations to recover a source assignment in the recognized
is not invoked for UNSAT.                                                    affine-XOR/cardinality encoding. After validation, eligible small
                                                                             lower-bound cases use watched-literal CDCL with VeriPB RUP logging
                                                                             for UNSAT; bounded decoding failure or unsupported cases return
                                                                             UNKNOWN.
                                                                                                   Harrison Green, Claire Le Goues, and Fraser Brown


misc-satex                                                           099    modcircuits                                                          101
19 GBD instances · 4 validation · baseline 3/4                              20 GBD instances · 4 validation · baseline 1/4
The benchmark asks whether a Boolean assignment satisfies every             These benchmarks ask whether a bounded acyclic Boolean circuit with
clause of a CNF formula. Some instances encode one allowed choice           two-input gates can realize a modular Boolean function, possibly with
per object with binary incompatibilities, while others encode Boolean       encoded input or output residues. CNF encodings represent gate
gate relationships; these structures describe recognized subfamilies,       sources, gate truth tables, row values, and outputs, with clauses
not all CNF inputs.                                                         enforcing consistency and the target behavior.
Proof format                             No verif.      + verif.   Solved   Proof format                             No verif.    + verif.     Solved
GRAT                                       8.83 ×       8.82 ×        4/4   GRAT                                      1.00 ×      1.00 ×           1/4
Graph-color recognition drives bounded TabuCol, while pure 3-CNF            Hard-coded recognizers install bit-parallel phase hints for selected
uses bounded ProbSAT with break counts; accepted models are                 MOD4, MOD5, and restricted MOD3 layouts, while otherwise
checked against the original clauses. Fallback uses canonicalization,       retaining generic watched-literal CDCL search with exactly-one
bounded elimination, and watched-literal CDCL, logging resolvents           source-choice branching where applicable. SAT assignments are
and learned clauses as DRAT for external elaboration; failed search or      checked against the original clauses; UNSAT search logs learned
reconstruction yields UNKNOWN rather than UNSAT.                            clause additions and a terminal empty clause for external DRAT
DPR                                       11.6 ×        11.4 ×        4/4   elaboration, and failed checks return UNKNOWN.
Structural matching recovers shared color labels in recognized              DPR                                      0.750 ×     0.750 ×           0/4
correspondence-coloring CNF, followed by bounded randomized                 Structural decoders derive hard-coded phase assignments for selected
TabuCol search and full-model checking. The narrow twoall shape             MOD4, MOD5, and restricted MOD3 layouts, then test constructions
instead uses bounded elimination and watched-literal CDCL with              under temporary assumptions before CDCL fallback. Fallback uses
logged clauses for UNSAT; circuit and generic paths lack an UNSAT           implication-SCC substitution and bounded variable elimination, while
certificate path and may return UNKNOWN after failed search.                first-UIP learning logs clause additions, including witness-free
VeriPB                                   0.781 ×       0.780 ×        3/4   additions; checked SAT models return, but unsupported shapes or
Invariant-based recognition recovers list-coloring structure for            failed completion yield UNKNOWN.
TabuCol, while other admitted shapes use ProbSAT, min-break, or             VeriPB                                   0.750 ×     0.750 ×           0/4
weighted-breakout search. Recognized AIG and completion cases may           Embedded recipe matching decodes one-hot layouts and uses 64-bit
use bounded elimination with reverse extension, and heuristic failures      truth-table simulation to assign gates, outputs, and row variables for
fall to watched-literal CDCL with RUP logging; checked SAT                  selected parameter shapes. A polarity-shuffled ten-gate layout can
assignments are accepted, but unmatched inputs return UNKNOWN.              trigger signed topology recovery with CDCL completion after
                                                                            construction fails; checked assignments are returned, while
miter                                                                100
                                                                            unsupported shapes or failed search yield UNKNOWN and no UNSAT
524 GBD instances · 105 validation · baseline 74/105
                                                                            certificate is implemented.
A Boolean miter CNF asks whether two Boolean circuits can produce
different outputs on some input. Circuit wires and auxiliary variables      mosoi-289                                                            102
are constrained by gate clauses, with clauses expressing the required       36 GBD instances · 8 validation · baseline 4/8
output difference.                                                          Assign one of four colors to each grid cell so that no color occupies all
Proof format                             No verif.      + verif.   Solved   four corners formed by two rows and two columns. A CNF uses four
GRAT                                     0.569 ×       0.632 ×     46/105   variables per cell, clauses restricting allowed colors, and four-literal
Signed-literal congruence is its main preprocessing: implication SCCs       negative clauses forbidding monochromatic rectangles.
and recognized AND, XOR, or mux structures merge equivalent                 Proof format                             No verif.    + verif.     Solved
signals before bounded elimination. Failed-literal probing and CDCL         GRAT                                       1.00 ×     1.00 ×           4/8
search the residual; checked SAT models are reconstructed, while            Collision-scored min-conflicts search uses row-pair/color counts with
UNSAT is logged as textual DRAT for external elaboration and failures       legal recoloring and restarts. It checks candidate assignments against
return UNKNOWN.                                                             every parsed clause; bounded search failure returns UNKNOWN.
DPR                                      0.379 ×       0.424 ×     15/105   Counting obstructions trigger a DRAT proof using a pigeonhole
Exact AND/XOR Tseitin recognition uses topological signed hashing           reduction from a usable 6x31 core; failed or unsupported cases return
and equivalence lemmas, with an all-AND unit-root path as a second          UNKNOWN.
recognizer. Residual cases use bounded elimination, profile-gated           DPR                                        1.00 ×     1.00 ×           4/8
CDCL, or tree DPLL; checked SAT assignments are printed, while              A specialized 6x30/30x6 matching construction is tried first; otherwise
unsupported or exhausted cases return UNKNOWN and UNSAT uses                pseudorandom annealing minimizes monochromatic rectangles, with
witness-free RUP/DRUP-style additions.                                      balanced column swaps preserving color counts in tight cases.
VeriPB                                   0.509 ×       0.567 ×     39/105   Checked SAT assignments are emitted, while a generated 6x31 core
Parity union-find and bottom-up AND-cone hashing recover                    can produce a DPR pigeonhole proof with fresh collision variables;
duplicate-wire equivalences, followed by bounded Davis-Putnam               unsupported sequential-counter/K4 cases return UNKNOWN.
elimination, even though the input miter structure is not validated.        VeriPB                               2.52·104 ×       788 ×            8/8
Watched-literal CDCL handles the remainder with RUP-logged clauses;         Incremental min-conflicts search on a recognized ordered or
checked SAT models have no VeriPB SAT certificate, and proof,               signed/permuted grid scores row-pair/color collisions and applies
resource, or model failures return UNKNOWN.                                 random perturbations. It verifies every input clause for each candidate
                                                                            before emitting a SAT assignment; resource-count contradictions
                                                                            produce a VeriPB proof, while the MIS fallback emits only a proof and
                                                                            unsupported inputs return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

multiplier-circuits                                                  103    multiplier-verification                                               105
18 GBD instances · 4 validation · baseline 4/4                              27 GBD instances · 6 validation · baseline 2/6
These benchmarks ask whether two bounded unsigned binary integers           Determine whether values for the free input variables can satisfy a
multiply to a fixed target. The target is encoded by unit clauses on        structured acyclic Boolean mux network, a fixed-true terminal, and a
product outputs, while Boolean gate clauses connect operand bits to a       final disjunction. The CNF defines each mux with six clauses and
multiplier circuit and auxiliary variables.                                 includes the network constraints plus the final clause.
Proof format                             No verif.    + verif.    Solved    Proof format                             No verif.       + verif.   Solved
GRAT                                       547 ×      217 ×          4/4    GRAT                                       1.05 ×        1.05 ×       2/6
Structural multiplier recognition recovers operand widths and the           64-bit signature sweeping proposes RUP-validated unit and binary
fixed product, then small-divisor and Pollard-Brent factorization finds     lemmas over the ordered ITE DAG. CDCL searches, tries final-literal
width-fitting operands. The factors drive watched-literal propagation       assumptions, then falls back to whole-miter search; it emits
and a full clause scan for SAT; only a root-level unit-propagation          DRAT-style clause additions and an empty clause for external
conflict emits an empty-clause certificate, while recognition, factoring,   elaboration, returns UNKNOWN on unsupported or incomplete cases,
or other unsatisfiable cases return UNKNOWN.                                and has no SAT assignment output.
DPR                                        713 ×      33.1 ×         4/4    DPR                                      0.702 ×        0.707 ×       0/6
Rigid-layout recognition and bit-parallel signature simulation recover      Gate-aware propagation stores each ITE as a six-clause object,
a target from ordered encoding, then drive width-bounded divisor            rescanning affected gates while CDCL branches only on primary
search with Pollard-Brent factoring. Candidate factors are checked          inputs. First-UIP learning with watched clauses supports UNSAT
against all original clauses before a SAT assignment is emitted;            certification through witness-free learned clause additions and an
ambiguous signatures, unsupported layouts, or failed searches return        empty clause; unsupported structure, duplicate final literals, or proof
UNKNOWN, with no UNSAT certificate path.                                    failures return UNKNOWN, while SAT prints an assignment.
VeriPB                                     853 ×      33.3 ×         4/4    VeriPB                                    1.05 ×        0.833 ×       2/6
Structural recognition reads product units and replaces SAT search          Mux-derived phase initialization guides watched-literal CDCL with
with width-bounded factor search, using trial division, with                first-UIP learning. It logs learned clauses with RUP and dependency
Pollard-Brent available only up to 128 bits. It checks factors through      hints and a final empty constraint for UNSAT; the SAT path checks
the circuit and clauses before emitting a SAT model; unsupported or         and prints a model but emits no completed VeriPB certificate, while
unfactored targets return UNKNOWN, with no UNSAT or VeriPB                  unsupported inputs or proof failures return UNKNOWN.
certificate path.
                                                                            mutilated-chessboard                                                  106
multiplier-equivalence-checking                                      104    22 GBD instances · 5 validation · baseline 2/5
20 GBD instances · 4 validation · baseline 0/4                              The task asks whether dominoes can cover every remaining square
The benchmark asks whether two circuit implementations, commonly            after removing two same-color opposite corners from a checkerboard,
16-bit multipliers over two 16-bit operands, produce different outputs      without overlap. CNF encodings use placement variables, coverage
for some input. The CNF encodes the circuits and a final disagreement       clauses, and constraints preventing a square from being used twice.
miter, so SAT gives a counterexample and UNSAT rules out                    Proof format                             No verif.       + verif.   Solved
disagreement for that encoding.                                             GRAT                                       1.53 ×        1.16 ×       3/5
Proof format                             No verif.    + verif.    Solved    Checkerboard matching recovery drives anti-diagonal frontier DP,
GRAT                                      1.00 ×     1.00 ×          0/4    using occupancy bit masks and a subset trie to reuse failed states.
XOR/XNOR detection and bounded parity substitution strengthen               Preparation checks destination conflicts with binary propagation and
recognized instances before watched-literal CDCL search with                emits bottom-up dependency lemmas, deletions, and an empty root
activity-based branching and clause learning. SAT is reported only          clause for UNSAT; without a SAT witness path, satisfiable or
with an assignment checked against the CNF; rejected patterns return        unsupported cases return UNKNOWN.
UNKNOWN, while exhausted UNSAT search logs learned and                      DPR                                      0.783 ×        0.812 ×       1/5
strengthening clauses plus deletions and a final empty clause for           A strict structural recognizer accepts only validated direct-incidence or
external checking.                                                          sparse-matrix pigeonhole layouts and returns UNKNOWN otherwise.
DPR                                       1.00 ×     1.00 ×          0/4    Bounded Davis-Putnam elimination and watched-literal CDCL use
Primary-input conflict projection uses an independent watched-literal       first-UIP learning; the clause/deletion trace records resolvents, learned
RUP oracle to minimize learned clauses, driving asserting backjumps         clauses, deletions, and an empty clause on a level-zero conflict, while
in watched-literal CDCL search. SAT models are reconstructed and            non-UNSAT outcomes return UNKNOWN without model
checked; unsupported or failed cases return UNKNOWN, while                  reconstruction.
UNSAT emits witness-free DPR additions, including learned                   VeriPB                               3.56·105 ×      1.33·104 ×       5/5
operand-blocking clauses and a final empty clause for external              Matching recognition converts compact or sparse layouts into
elaboration and checking.                                                   degree-2-to-4 counting constraints over mutexes, replacing general
VeriPB                                    1.00 ×     1.00 ×          0/4    search. Unit propagation may justify missing mutexes in the sparse
Proof-first pseudo-Boolean generation recovers partial products and         fallback; a VeriPB contradiction then combines coverage clauses with
width-three compressor relations from a restricted Tseitin DAG, emits       clique inequalities. Unsupported inputs or failed proof preconditions
a refutation, and leaves proof checking external. If generation fails,      return UNKNOWN; no SAT witness path is implemented.
bit-parallel evaluation searches for a counterexample and reports SAT
only after clause checking; otherwise it returns UNKNOWN and has
no UNSAT certificate path.
                                                                                                 Harrison Green, Claire Le Goues, and Fraser Brown


oddball-weighing                                                   107    ordering-principle                                                   109
40 GBD instances · 8 validation · baseline 8/8                            36 GBD instances · 8 validation · baseline 8/8
The benchmark asks whether each object can receive a nonzero              The benchmark asks whether a directed relation on n objects can give
ternary signature and orientation across non-adaptive weighings so        every object a predecessor while obeying antisymmetry and
every weighing has equal positive and negative counts. CNF                transitivity. A CNF encoding uses variables for directed edges,
encodings represent signature choices and directed matching edges         predecessor clauses, binary clauses forbidding opposite edges, and
pairing opposite outcomes.                                                ternary clauses expressing transitivity.
Proof format                             No verif.    + verif.   Solved   Proof format                             No verif.    + verif.     Solved
GRAT                                       413 ×      36.9 ×        8/8   GRAT                                       142 ×      11.7 ×         8/8
It recognizes a narrow matching-and-signature CNF pattern, then           A bounded search for cycles among omitted transitivity clauses
searches fixed canonical assignments with randomized-prefix               supplies checked SAT models when successful; a single missing
meet-in-the-middle and free ordered subsets with                          predecessor or antisymmetry axiom also permits direct model
codeword/orientation annealing. Successful constructions undergo          construction. Otherwise, vertex elimination emits a textual DRAT
streamed propagation and clause checks; an odd-row obstruction can        clause sequence toward UNSAT; unsupported shapes or failed
produce textual DRAT for external elaboration, while other heuristic      construction return UNKNOWN without general SAT search.
failures return UNKNOWN rather than UNSAT.                                DPR                                        138 ×      4.31 ×         8/8
DPR                                        359 ×      3.77 ×        8/8   Structural recognition recovers vertices, directed edges, and polarities,
On narrow canonical block/domain inputs, an odd-coordinate                then validates the supported transitivity pattern. It either greedily
matching obstruction adds core clauses and an empty clause for            eliminates vertices with witness-free RUP additions to derive UNSAT,
UNSAT certification. Otherwise, exact dynamic programming gives           or constructs and checks a model for narrowly supported
way to annealing or distinct-tuple search; the SAT path lifts tuple and   missing-axiom or cycle cases; unsupported inputs and failed checks
matching variables, propagates the CNF, and greedily completes            return UNKNOWN without general SAT search.
clauses, while failures return UNKNOWN.                                   VeriPB                                     120 ×      3.99 ×         8/8
VeriPB                                   0.692 ×      1.04 ×       7/8    Safe object elimination removes an object only when omitted
On its recognized layouts, seeded annealing balances coordinate sums      transitivity clauses cannot obstruct it, then emits a VeriPB RUP proof
by changing orientations and, for free layouts, selected signature        of UNSAT. If elimination fails, it checks models only for a
classes. Only fixed layouts with an odd support coordinate use the        missing-transitivity cycle or one missing predecessor or asymmetry
pseudo-Boolean matching proof path; other cases seek a model by           clause; unsupported or failed cases return UNKNOWN without
streaming propagation after pairing opposite sides, with failures or      general SAT search.
oversized inputs returning UNKNOWN.
                                                                          ordering-principle-xor                                               110
or_randxor                                                         108    6 GBD instances · 2 validation · baseline 2/2
10 GBD instances · 2 validation · baseline 2/2                            Given n vertices, can a transitive, antisymmetric relation give every
The benchmark asks whether ternary Boolean XOR equations can be           vertex at least one of three prescribed predecessors? The supplied
satisfied when each logical value is represented by the OR of a           encodings represent each relation variable by an XOR pair and expand
consecutive pair of variables. Each equation is converted to CNF by       the resulting width-two and width-three clauses into CNF.
distributing over those pair expressions, producing the encoded           Proof format                             No verif.    + verif.     Solved
instance.                                                                 GRAT                                      2,670 ×     15.8 ×         2/2
Proof format                             No verif.    + verif.   Solved   Candidate-state scanning applies the finite-order minimal-element
GRAT                                     0.281 ×     0.354 ×        2/2   contradiction, replacing a current candidate exactly when a relation
Bit-packed GF(2) Gaussian elimination solves recognized systems and       holds. It bridges selected XOR definitions to logical clauses and emits a
reconstructs a checked SAT assignment. Inconsistent cases use             DRAT clause-addition refutation ending in the empty clause;
pair-symmetry reduction, bounded Davis-Putnam elimination, and            unrecognized or output-failing cases return UNKNOWN rather than
watched-literal CDCL to build a textual DRAT refutation for external      using general SAT search.
checking; only exact canonical OR-pair expansions are handled, and        DPR                                      8,640 ×      44.4 ×         2/2
failures return UNKNOWN.                                                  Minimum-fill elimination orders the predecessor graph and
DPR                                      0.434 ×     0.129 ×        2/2   gauge-fixes only XOR atoms needed by that plan. It emits witness-free
Bit-packed GF(2) elimination first solves recognized equations and        DPR additions for bypass and reduced predecessor clauses, reporting
produces a clause-checked SAT assignment. For inconsistency, the          UNSAT only after an empty clause is written; there is no SAT fallback,
solver peels a 2-core, applies pair-symmetry reduction and bounded        and unsupported or failed cases return UNKNOWN.
Davis-Putnam elimination with witness-free clause additions, then         VeriPB                                    2,710 ×     33.8 ×         2/2
uses CDCL to complete the refutation; only exact canonical OR-pair        Redundancy-based XOR symmetry breaking fixes each even physical
expansions are recognized, and failures return UNKNOWN.                   bit before deterministic vertex elimination. It emits RUP predecessor
VeriPB                                   0.194 ×     0.275 ×       2/2    clauses as candidate sets are unioned, then completes a VeriPB proof
Dependency-carrying GF(2) elimination solves recognized systems           with a final NONE marker and UNSAT conclusion; failed recognition
and yields a clause-checked SAT assignment. For inconsistency, the        or proof generation returns UNKNOWN, and no SAT search is used.
solver peels and normalizes a 2-core, then uses watched-literal CDCL
with RUP logging to emit a VeriPB proof; only the exact OR-pair
encoding is supported, and unsupported inputs or failed proof
construction return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

p-center                                                           111    pebbling                                                              113
21 GBD instances · 5 validation · baseline 5/5                            55 GBD instances · 11 validation · baseline 11/11
The benchmark asks whether at most p candidate facilities can cover       These instances ask whether a Boolean assignment can satisfy a DAG’s
every demand point, with each demand represented by a positive            pebbling dependencies while forcing its sink false. CNF encodings use
facility clause. In CNF, auxiliary variables enforce the cardinality      signed literal blocks, source clauses, Cartesian transition families, and
bound, while equivalent encodings may represent the same p-center         sink units; some variants use a specific NAE gadget.
question.                                                                 Proof format                             No verif.       + verif.   Solved
Proof format                             No verif.    + verif.   Solved   GRAT                                       13.9 ×       0.292 ×     11/11
GRAT                                      3.03 ×     2.14 ×         5/5   A clause-sharing recognizer factors transition families into Cartesian
Failed-literal probing is the active strategy: root propagation tests     predecessor blocks and reconstructs the pebbling graph, with an
variables and turns a conflicting polarity into an opposite unit until    UNSAT-only fallback for exact parity-gadget shapes. Staged resolution
conflict or closure. It handles only a restricted layout with unit        and RUP checks handle complete transitions and limited missing-cell
coverage clauses; no SAT path exists, so unclosed or SAT cases return     repairs. CDCL can return a checked SAT assignment or DRAT trace;
UNKNOWN, while closed refutations record units and an empty               unsupported cases return UNKNOWN.
clause.                                                                   DPR                                        109 ×         25.3 ×     11/11
DPR                                        2.72 ×    0.416 ×        5/5   Occurrence signatures and Cartesian-tail factorization recover a
Facility-aware DPLL is the active strategy: watched propagation           disjoint DAG, with a validated three-variable NEQ route using a fixed
branches on a facility from the shortest uncovered cover clause,          resolution template. Topological traversal emits resolution proofs,
favoring frequent facilities, then uses auxiliary fallback decisions to   including repairs, while SAT construction handles only one recognized
complete the counter extension. It checks SAT assignments and emits       source, transition, or sink defect and checks its model. Unrecognized
postorder, witness-free RUP blockers for UNSAT; other encodings or        or failed constructions return UNKNOWN.
failed checks return UNKNOWN.                                             VeriPB                                     30.0 ×        12.4 ×     11/11
VeriPB                                     2.06 ×    0.663 ×       5/5    NAE3 dispatch eliminates exact gadgets by local resolution; incidence
Specialized neighborhood branching is central: watched propagation        recovery otherwise builds a Horn quotient from signed blocks.
selects a candidate from the tightest uncovered neighborhood, while       Forward chaining finds a conflict for proof or lifts a checked SAT
counter clauses enforce capacity. Root propagation may produce an         model; only one-deletion OR cases are accepted. Unit-containing
empty-RUP result; otherwise a CDCL fallback learns RUP clauses,           CDCL covers small recognized-width formulas; NAE SAT cases and
while checked SAT assignments are emitted and unsupported layouts         unresolved inputs return UNKNOWN.
or failed checks return UNKNOWN.
                                                                          perfect-matching                                                      114
parity-games                                                       112    17 GBD instances · 4 validation · baseline 0/4
28 GBD instances · 6 validation · baseline 5/6
                                                                          Given a bipartite graph, can each of n+1 left vertices choose an
The benchmark uses structured CNF encodings of bounded sequences          incident right vertex without choosing any right vertex twice? The
of parity-game strategies and their transitions. Satisfiability asks      CNF requires one choice per left vertex and at-most-one use per right
whether Boolean variables can realize a consistent encoded                vertex, often exposing an unbalanced matching or pigeonhole core.
construction, using relation variables, transition clauses, and
definitional witnesses.                                                   Proof format                             No verif.       + verif.   Solved
                                                                          GRAT                                 5.53·105 ×         3,080 ×       4/4
Proof format                             No verif.    + verif.   Solved
                                                                          Structural recognition identifies an unbalanced graph-pigeonhole core
GRAT                                      1.05 ×     1.05 ×         5/6
                                                                          by recovering consecutive row blocks and column exclusions from
Strict structural recognition gates two-watched-literal CDCL with         binary implication paths. It recursively eliminates rows and holes with
1-UIP learning, clause minimization, activity-based branching, and        fresh variables, using RAT definitions and RUP child rows to derive the
LBD retention. SAT models are checked; a non-SAT pass is rerun with       empty clause; unsupported encodings, proof failures, and SAT cases
logging, and only a logged UNSAT yields UNSAT, while nonmatching          return UNKNOWN.
inputs or a failed rerun yield UNKNOWN. The proof path emits
textual DRAT clauses.                                                     DPR                                   2.82·105 ×        1,840 ×       4/4
                                                                          Hall-deficit recognition reconstructs the unbalanced matrix and checks
DPR                                      0.673 ×     0.673 ×        4/6
                                                                          binary implication reachability for column conflicts. It recursively
Binary-implication SCC compression, failed-literal probing, and           removes a row and column, adding Tseitin definitions and witness-free
bounded resolution elimination simplify recognized instances before       conflict clauses, with RUP bridges when needed, until an empty clause;
CDCL; vivification is inactive. SAT assignments are reconstructed and     unsupported shapes, proof failures, and SAT inputs return
checked against the original CNF, while UNSAT deductions are              UNKNOWN without SAT search or assignment output.
streamed as witness-free textual DPR additions; malformed or
nonmatching inputs return UNKNOWN.                                        VeriPB                                3.26·105 ×     6.18·104 ×       4/4
                                                                          Pigeonhole counting recognizes a row-major unbalanced core,
VeriPB                                   0.673 ×     0.672 ×       4/6
                                                                          recovering column at-most-one constraints from pairwise, sequential,
Binary-implication SCC compression and bounded variable                   grouped, or implication-based encodings. It writes a VeriPB proof
elimination precede CDCL with first-UIP learning. In SAT-first mode,      using inequality chains or RUP-added conflicts followed by
it searches without proof retention and reruns only UNSAT results for     cutting-planes induction; full-CNF propagation is a fallback, while
version 3.0 pseudo-Boolean proof emission. SAT models are                 unrecognized or satisfiable inputs return UNKNOWN without general
reconstructed and checked; no verifier is included, and parsing,          SAT search.
checking, or proof-writing failures return UNKNOWN.
                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


petrinet-concurrency                                                  115    phnf                                                                117
54 GBD instances · 11 validation · baseline 6/11                             27 GBD instances · 6 validation · baseline 2/6
These benchmarks ask whether a graph’s vertices can be assigned one          The task is to choose exactly one value from each disjoint group while
of k colors so adjacent vertices differ. The accepted CNF uses               avoiding forbidden pairs between groups. In CNF, group clauses
vertex-color variables, per-vertex at-least-one clauses, and same-color      require a choice, complete within-group binary exclusions enforce
edge exclusions, with a restricted symmetry-broken layout.                   uniqueness, and cross-group binary clauses forbid incompatible value
Proof format                             No verif.     + verif.     Solved   pairs.
GRAT                                       530 ×      12.8 ×        11/11    Proof format                             No verif.    + verif.    Solved
DSATUR coloring is the primary search, with colors renamed by first          GRAT                                     0.875 ×     1.39 ×          1/6
occurrence to respect the triangular symmetry breaking. If it fails,         Rectangle compression is active: repeated row and column masks
bounded bit-parallel clique search seeks a checked (k+1)-clique for a        become Boolean features before CDCL searches the model. The
pigeonhole-style UNSAT proof; bounded TabuCol may find a SAT                 bounded recognizer has no generic fallback, so rejected inputs and
assignment and independently verify it; unresolved cases return              failed SAT checks return UNKNOWN. UNSAT logging records feature,
UNKNOWN. It handles only this recognized layout.                             rectangle, and learned clauses for external elaboration, but an
DPR                                        5.77 ×     0.640 ×       10/11    initial-unit conflict may lack an empty clause.
DSATUR coloring drives the SAT search on the strictly recognized             DPR                                      0.747 ×      1.37 ×         0/6
layout, using dense bitsets; success emits a complete assignment. If it      Parity factoring leads the active search: union-find links
fails, greedy and exact clique search seek a (k+1)-clique for a              complementary binary relations, CDCL searches the latent CNF, and
pigeonhole-style UNSAT proof, but failure to find the clique or write        finite-domain search verifies assignments before path-consistency and
the proof returns UNKNOWN; no explicit empty-clause derivation is            finite-domain CDCL fallbacks. Unsupported structures return
written.                                                                     UNKNOWN; verified SAT assignments are emitted, while UNSAT uses
VeriPB                                     5.77 ×      5.18 ×       10/11    a witness-free DPR log for external elaboration, with replay failure
Clique-anchored coloring and DSATUR drive SAT search on the                  also returning UNKNOWN.
recognized layout, with randomized list-coloring, MRV backtracking,          VeriPB                                   0.747 ×      1.37 ×         0/6
and tabu/min-conflicts fallbacks. A bounded exact clique search can          Dominance substitution and failed-assumption probing lead the
emit an UNSAT cutting-planes proof for a (k+1)-clique within the             default search, followed by path-consistency implications and bit-mask
kernel guard; SAT models are clause-checked, but no external proof           propagation in CDCL. The recognizer accepts only bounded complete
checker is invoked, and failure returns UNKNOWN.                             choice blocks and returns UNKNOWN otherwise; SAT assignments
                                                                             are reparsed and checked, while UNSAT records dominance and RUP
philips                                                               116
                                                                             steps with a final contradiction, reporting UNKNOWN if proof
4 GBD instances · 1 validation · baseline 1/1                                finalization fails.
These CNFs encode a miter comparing two combinational multiplier
circuits driven by the same binary inputs. Gate variables and local          pigeon-hole                                                         118
                                                                             154 GBD instances · 31 validation · baseline 23/31
circuit relations are expressed as CNF constraints, so satisfiability asks
whether the two outputs can differ.                                          The benchmark asks whether pigeons can be assigned to holes without
Proof format                             No verif.     + verif.     Solved
                                                                             exceeding the allowed hole capacity. CNF encodings use placement
GRAT                                       91.1 ×     0.425 ×         1/1
                                                                             variables, clauses requiring each pigeon to choose a hole, and clauses
                                                                             preventing forbidden collisions; variants may add capacities or guards.
Packed 64-bit truth-table enumeration over a recognized acyclic netlist
is the active technique. A clause-checked candidate yields SAT;              Proof format                             No verif.    + verif.    Solved
recognition or proof failures yield UNKNOWN, with no general SAT             GRAT                                     0.982 ×      1.57 ×      22/31
fallback. The no-candidate path uses RUP equivalences and a recursive        Exact grid recognition regenerates the expected clause set before
Shannon-style refutation with deletions, blocking clauses, and a final       accepting a layout and constructs a checked assignment for recognized
empty clause for external checking.                                          SAT cases. Specialized UNSAT branches use subset-counting,
DPR                                        1.61 ×     1.06 ×          1/1    occupancy-state, implication, finite-path, or relativized reasoning and
                                                                             emit DRAT streams; bounded CDCL handles limited cases, while
Gray-code enumeration of one recovered 10-bit operand drives the
                                                                             unsupported or unfinished paths return UNKNOWN.
search. Each fixed case uses fresh CDCL with minimized learned
clauses; a SAT case returns a checked model. Refuted cases write lifted      DPR                                        8.82 ×     2.47 ×      30/31
learned clauses and resolve blocking clauses to the empty clause for         Incidence reconstruction identifies pigeon rows, holes, and guarded
external DPR elaboration; unsupported cases return UNKNOWN.                  collision structure, directing recognized instances to specialized paths
VeriPB                                     438 ×     0.811 ×          1/1    rather than a general CNF solver. Only the standard branch constructs
                                                                             and checks SAT assignments; other recognized variants use clause
Fixed-shape fingerprinting dispatches on twenty high-fanout inputs.
                                                                             additions, deletions, PR-style induction, RUP checks, or
The active path emits a complete binary tree with RUP blocking leaves
                                                                             clique-restricted CDCL proofs, while failed recognition or unfinished
and cutting-planes joins to a contradiction for external VeriPB
                                                                             paths return UNKNOWN.
checking. It does not internally validate the proof or provide a SAT
fallback; recognition or generation failures return UNKNOWN.                 VeriPB                                    8.84 ×     14.0 ×       30/31
                                                                             Structural recognition reconstructs matrix placement columns and
                                                                             collision edges, enabling a direct SAT assignment only on the matrix
                                                                             path. Recognized UNSAT variants use aggregate PB/RUP derivations,
                                                                             while a fixed MIS-wrapper signature alone enables CDCL with
                                                                             RUP-logged learned clauses; unsupported layouts or failed certificate
                                                                             generation return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

planning                                                             119    popularity-similarity                                                 121
667 GBD instances · 134 validation · baseline 81/134                        42 GBD instances · 9 validation · baseline 3/9
These benchmarks ask whether a Boolean assignment satisfies every           These instances are 3-CNF formulas, with three literals per clause. The
clause in a CNF encoding of a planning decision problem. Variables          available solver artifacts establish their clause structure but do not
and clauses can represent actions, states, auxiliary choices, or            recover the generating popularity-similarity model.
occupancy constraints, while inputs use DIMACS rather than                  Proof format                             No verif.    + verif.     Solved
recovered planning semantics.                                               GRAT                                       1.07 ×     1.12 ×          3/9
Proof format                             No verif.      + verif.   Solved   Bounded variable elimination limits resolvent growth, records
GRAT                                     0.719 ×       0.850 ×     57/134   eliminated variables, and passes the residual to watched-literal CDCL
Short-clause occurrence weighting guides bounded DIMACS CDCL,               with degree-seeded EVSIDS. It accepts only the recognized fixed
with a dense-instance binary-implication path but no planning-specific      3-CNF degree profile, returns UNKNOWN on other inputs, checks
reconstruction. Malformed inputs return UNKNOWN; oversized                  reconstructed SAT assignments, and may print UNSAT after failed
inputs receive only a two-pass model attempt and otherwise return           reconstruction without a final empty-clause certificate.
UNKNOWN. Validated SAT assignments are emitted, while UNSAT                 DPR                                       1.09 ×     0.988 ×          3/9
retains learned clauses as ASCII additions followed by the empty            Focused local search uses break-score weighting on variables from
clause.                                                                     unsatisfied clauses, then falls back to bounded Davis-Putnam
DPR                                      0.762 ×       0.889 ×     62/134   elimination and a 1-UIP CDCL cube search. It handles the recognized
A narrow multi-robot path-planning reconstruction searches                  3-CNF shape, returns UNKNOWN otherwise, checks SAT assignments,
space-time paths with vertex and swap avoidance, then injects a             and logs witness-free clause additions for external DPR elaboration
candidate branch. A failed candidate falls back to CDCL rather than         when cube closure reports UNSAT.
proving UNSAT; clause-checked SAT models are emitted, while                 VeriPB                                     1.03 ×    0.898 ×          3/9
UNSAT uses a learned-clause journal as DPR additions plus the empty         Popularity ordering and damped loopy-BP seed decisions and phases;
clause, and malformed or unsupported inputs return UNKNOWN.                 watched-literal CDCL then uses first-UIP learning and restarts. It
VeriPB                                   0.759 ×       0.790 ×     62/134   accepts only the recognized 3-CNF profile, returns UNKNOWN on
Conservative layout-gated root probing can force learned root units         unsupported inputs or conflict limits, and checks SAT assignments.
before first-UIP CDCL; it is structural rather than planner-semantic.       Enabled proof logging emits learned clauses and level-zero conflicts as
SAT assignments are reread and clause-checked, while UNSAT                  VeriPB RUP steps.
translates learned clauses into VeriPB RUP constraints with deletions
and an empty constraint; malformed, oversized, or output failures
                                                                            prime-factoring                                                       122
return UNKNOWN.
                                                                            185 GBD instances · 37 validation · baseline 27/37
                                                                            These CNFs ask whether two bounded binary factors multiply to a
polynomial-multiplication                                            120
                                                                            fixed target integer. Variables encode factor bits, partial products,
60 GBD instances · 12 validation · baseline 5/12
                                                                            carries, and output wires, while gate clauses and fixed bits constrain
The benchmark asks whether length-n polynomial multiplication over          the multiplication circuit.
GF(2) can be expressed as a sum of T products of three binary factor
                                                                            Proof format                             No verif.    + verif.     Solved
vectors. Its CNF encodes factor coefficients, conjunctions, and XOR
                                                                            GRAT                                     0.845 ×     0.843 ×        24/37
chains enforcing each convolution output.
                                                                            Structural multiplier recognition recovers operand positions, polarities,
Proof format                             No verif.      + verif.   Solved   and a bounded factor split, then checks the resulting assignment
GRAT                                      7.57 ×        5.32 ×      11/12   against every original clause. Specialized failures fall back to first-UIP
Recognizing compact GF(2) layouts, it constructs a symmetric rank           CDCL; SAT yields a checked assignment, root-conflict UNSAT is
decomposition, evaluates product and XOR variables, and                     logged as textual DRAT for external elaboration, and unresolved cases
independently checks every clause before emitting a SAT assignment.         return UNKNOWN.
For recognized UNSAT cases, including ordered GF(3) layouts, it
                                                                            DPR                                      0.596 ×     0.604 ×        17/37
content-checks and remaps bundled DRAT cores; unsupported layouts
or failed checks return UNKNOWN.                                            Structural probing on recognized multipliers uses packed all-zero and
                                                                            singleton-pair tests to recover input polarity and bit order, then
DPR                                       7.57 ×        6.24 ×      11/12   searches bounded factors. A restricted CDCL fallback checks SAT
Recognizing regular layouts with sufficient rank, it constructs SAT         assignments. Only the special 8-by-8 EZFact no-factor case emits
assignments from GF(2) bilinear decompositions, with ordered                witness-free blocking clauses followed by a resolution tree; other
propagation and full-CNF validation; the alternate layout has no SAT        no-factor results and CDCL UNSAT return UNKNOWN.
path. For UNSAT, it recovers limited permutations by incidence
                                                                            VeriPB                                    1.03 ×     0.973 ×        27/37
structure and maps checked embedded DRAT templates for bounded
recognized cases; failures or unsupported cases return UNKNOWN.             Polarity-aware structural decoding reconstructs shuffled multiplier
                                                                            bits and tests arithmetic candidates, with a narrower multiplier
VeriPB                                    1.52 ×        1.53 ×       7/12   recognizer as a second direct path. These direct paths provide checked
It recognizes the tensor header equations and constructs GF(2)              SAT assignments but no UNSAT certificate. If they fail, CDCL logs
decompositions from diagonal and pair products, using a special             level-zero UNSAT as VeriPB RUP traces with deletions; unsupported or
reduced-product basis and elimination for n=5. It evaluates all             resource-limited cases return UNKNOWN.
auxiliary variables and clauses before SAT output; it has no general
search or UNSAT certification, so failed or unsupported cases return
UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


prime-testing                                                       123    profitable-robust-production                                        125
58 GBD instances · 12 validation · baseline 7/12                           20 GBD instances · 4 validation · baseline 2/4
These benchmarks ask whether structured Boolean arithmetic                 The benchmark asks whether binary production decisions and
constructions have satisfying assignments, including fixed-product         auxiliary Boolean variables can satisfy constraints linking production
factors, modular square roots, or repeated gate predicates. CNF            and profit across scenarios. These constraints encode comparisons,
encodings use Tseitin-style gate clauses, unit constraints, and            arithmetic, and robust minima or related aggregates in CNF, often
equivalences over circuit and word variables.                              with order/comparator and Tseitin variables.
Proof format                             No verif.    + verif.    Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                       1.27 ×     1.29 ×       8/12    GRAT                                      23.7 ×      17.6 ×         4/4
Arithmetic witness construction drives the main search: factorization      For recognized inputs, support-row canonicalization fixes selected
or modular-root solving fixes word inputs, and unit propagation            auxiliary rows and installs stride-based assignments, then
completes assignments followed by full clause checks; repeated blocks      watched-literal CDCL searches decomposed components with reused
use watched-literal DPLL with offset translation. Supported failures       phases, learning, and restarts. These restrictions may exclude
may use bounded input-tree search, reporting UNSAT only with               satisfying assignments; SAT models are checked against the original
textual DRAT refutations; unsupported cases return UNKNOWN.                clauses, while contradictory or exhausted searches return UNKNOWN
DPR                                       1.56 ×     1.37 ×        9/12    and no UNSAT certificate is produced.
Bit-parallel exhaustive search handles recognized repeated circuits,       DPR                                      0.823 ×     0.825 ×         2/4
while arithmetic decoding uses factorization or modular roots              Binary-implication SCC substitution and bounded elimination remove
followed by propagation and clause checks. Selected fallbacks use          equivalent or redundant comparator variables before watched-literal
restricted CDCL, emitting clauses and an empty clause as DPR               CDCL. On SAT, it reconstructs eliminated variables and checks every
additions; unsupported cases return UNKNOWN, while proof-output            original clause before printing a model; no DPR proof is emitted, and
failure can return SAT without an UNSAT certificate.                       rejected inputs, contradictions, or failed searches return UNKNOWN
VeriPB                                     1.27 ×     1.29 ×       8/12    rather than UNSAT.
Bit-parallel evaluation is the primary search for repeated circuits,       VeriPB                                   0.804 ×     0.805 ×         2/4
while product and quadratic layouts recover arithmetic witnesses           False-first phase heuristics with occurrence-signature exceptions
using factorization or modular-root methods, then complete                 initialize watched-literal CDCL, while recognition of the expected
assignments by propagation and validate every original clause. The         ripple-gate prefix only selects the specialized input path. After a SAT
solver has no general SAT search or UNSAT or VeriPB certification          result, the solver reparses and checks every original clause before
path; unrecognized or failed constructions return UNKNOWN.                 outputting the assignment; it has no VeriPB derivation or UNSAT path,
                                                                           so search exhaustion and internal failure return UNKNOWN.
product-configuration                                               124
23 GBD instances · 5 validation · baseline 5/5                             purdom-instances                                                    126
                                                                           19 GBD instances · 4 validation · baseline 4/4
These benchmarks ask whether a Boolean assignment can select
product or configuration choices while satisfying requested features,      The family asks whether two binary operand vectors multiply to a
exclusions, implications, and support conditions. The instances use        fixed integer. CNF encodings represent factor bits, partial products,
flattened CNF with unit, binary, and wider clauses representing these      and an AND/XOR carry network, with unit clauses fixing output bits;
constraints, without requiring recovery of named product domains.          some encodings may shuffle variables or polarities.
Proof format                             No verif.    + verif.    Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                       3.88 ×    3.31 ×          5/5   GRAT                                     0.878 ×     0.388 ×         4/4
Failed-literal probing builds root units in short-clause activity order,   Partial-product graph recovery identifies a shuffled, polarity-flipped
followed by watched-literal propagation and activity-guided CDCL           multiplication circuit, then factors the fixed target and evaluates
with first-UIP learning and restarts. Rejected inputs or proof-output      compatible operands for a clause-checked model. If no compatible pair
failures return UNKNOWN; SAT returns a checked model, while                is found, modular prefix lemmas guide a least-significant-bit-first RUP
UNSAT records learned clauses and, on root conflict, the empty clause      tree, which writes the UNSAT proof only if it completes; unsupported
as textual DRAT additions.                                                 inputs return UNKNOWN.
DPR                                       6.63 ×     0.502 ×         5/5   DPR                                        917 ×     0.278 ×         4/4
An exclusion-heavy recognizer selects a specialized path, combining        Gate recognition reconstructs a single-writer network, including a
root-unit and watched-literal propagation with activity-weighted,          clean AND/XOR multiplier. It recovers an odd target, factors it, and
negative-first CDCL, first-UIP learning, and restarts. Unsupported         checks a model; direct UNSAT cases emit a blocker-tree clause
structure or internal or proof-output failure returns UNKNOWN; SAT         sequence, while augmented cases may use bounded factor search or
yields a checked model, while UNSAT appends learned clauses and, on        unlogged CDCL for SAT, returning UNKNOWN on recognition or
root contradiction, an empty clause to textual DPR output.                 search failure.
VeriPB                                     4.24 ×     1.09 ×        5/5    VeriPB                                   0.134 ×     0.189 ×         3/4
Shortest-open-clause branching follows failed-literal closure, guiding     Carry-weight and bipartite-graph recovery reconstructs factor-bit
search; conflicts use first-UIP learning, nonchronological backtracking,   order, after which factoring the target enables fixed-point AND/XOR
and a conservative whole-decision nogood fallback. Unsupported             evaluation and independent clause checking for composite cases. For
structure or checking or writing failure returns UNKNOWN; SAT              prime targets, first-UIP CDCL supplies RUP-style proof logging;
yields a checked assignment, while UNSAT writes learned clauses and        unsupported structures, factoring failures, or an incomplete proof
an empty clause as a VeriPB RUP certificate.                               return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

puzzle                                                                127    quantum-kochen-specker                                              129
21 GBD instances · 5 validation · baseline 5/5                               11 GBD instances · 3 validation · baseline 2/3
The benchmark asks whether fixed-orientation polyomino                       The benchmark asks whether an n-vertex graph can meet a specified
components can cover every cell of a rectangular board without               Kochen-Specker obstruction: Boolean edge variables choose
overlap. A structured CNF encodes board-cell labels, one-label-per-cell      adjacencies, triangle variables represent conjunctions of three edges,
constraints, piece-placement limits, adjacency, and forbidden                and CNF clauses enforce square-freeness and rule out the intended
translations.                                                                zero-one coloring, sometimes with symmetry breakers.
Proof format                             No verif.       + verif.   Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                    0.0927 ×      0.0866 ×        4/5    GRAT                                     0.588 ×     0.695 ×         1/3
It searches recognized fixed, translation-only shapes with bit-parallel      The solver first tries a hard-coded 17-vertex graph witness, propagates
exact-cover DFS, constrained-cell branching, and failed-state                triangle auxiliaries, and verifies complete SAT assignments against the
memoization. Found tilings are expanded and checked before SAT               original clauses. Other recognized inputs use edge-biased CDCL with
output. When search fails, mapped-placement CDCL attempts UNSAT              elimination and failed-literal probing; first-UIP clauses support
and emits DRAT additions; unsupported cases or failed proof                  external DRAT elaboration, while only an empty clause yields UNSAT
generation return UNKNOWN without external verification.                     and unsupported or unfinished cases return UNKNOWN.
DPR                                     0.0546 ×       0.0790 ×       2/5    DPR                                      0.654 ×     0.759 ×         1/3
It searches recognized fixed, translation-only shapes by bit-parallel        A hard-coded 17-vertex construction solves residual constraints,
exact-cover backtracking with constrained-cell branching and                 propagates triangle auxiliaries, and verifies its assignment against the
failed-state memoization. Found tilings are expanded and checked             original CNF. Other recognized cases use edge-prioritized CDCL with
before SAT output. When search fails on eligible small boards,               selected layer removal and first-UIP learning; witness-free DPR
auxiliary CDCL logs DRAT additions, including witness-free clauses;          additions support UNSAT certification, while unsupported or
unsupported cases or an inconclusive fallback return UNKNOWN                 unfinished cases return UNKNOWN and the shortcut lacks UNSAT
without external verification.                                               certification.
VeriPB                                   0.164 ×       0.0752 ×       4/5    VeriPB                                   0.469 ×     0.595 ×        0/3
It extracts placement masks from bidirectional implications and solves       Edge-prioritized CDCL drives the accepted n=17 minimum-degree
exact cover by minimum-domain branching, grouped translations, and           regime, with watched literals, activity-based branching, phase saving,
failed-state memoization. SAT assignments are checked; UNSAT                 deletion, and restarts. It checks SAT assignments against the original
reruns a DFS emitting VeriPB symmetry breakers and RUP nogoods               CNF and reports UNSAT only after serializing its trace as RUP steps
ending in contradiction. No general-SAT fallback is active, so rejected      for external checking, ending in an empty clause; unsupported inputs
inputs or proof failures return UNKNOWN.                                     or trace failures return UNKNOWN.

pythagorean-triples                                                   128    quasigroup-completion                                               130
21 GBD instances · 5 validation · baseline 2/5                               261 GBD instances · 53 validation · baseline 47/53

Given a collection of Pythagorean triples, assign each represented           The benchmark asks whether a partially filled quasigroup or
integer one of two colors so that no triple is monochromatic. In CNF,        Latin-square table can be completed so each cell receives one value
each triple is represented by complementary monotone clauses, while          and each value occurs once in every row and column. CNF uses
binary clauses capture constraints left after a vertex is fixed or           cell-value choices with one-hot groups and pairwise conflicts, but
removed.                                                                     encodings vary.
Proof format                             No verif.       + verif.   Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                 4.05·104 ×      2.98·104 ×       5/5    GRAT                                     0.578 ×     0.697 ×      41/53
Core reconstruction is the active technique: the solver regenerates a        A strict polarity/parity recognizer recovers three exact-cover
bounded Pythagorean 2-core, refines incidence signatures to map the          dimensions, then tries DSATUR-guided min-conflicts and bounded
input, and applies an embedded two-coloring. It completes residual           smallest-column search. Failed recognition or search falls back to
variables with non-monochromatic propagation and failed-literal DFS;         CDCL; SAT models are checked, while UNSAT emits textual DRAT for
the restricted recognizer does not validate numeric identities, and          external elaboration and checking, and proof, verification, or parse
recognition or search failure returns UNKNOWN without an UNSAT               failures can yield UNKNOWN.
certificate path.                                                            DPR                                      0.618 ×     0.702 ×      41/53
DPR                                        1.45 ×        1.45 ×       4/5    A phase-shuffled exact-cover detector recovers three dimensions and
Stochastic local search leads the default path, combining break-based        tries bounded min-conflicts followed by a local walk. Failures use
moves, clause weighting, and elite-agreement freezing. If it fails,          CDCL or, for larger recognized instances, exhaustive Algorithm X with
high-degree decimation is followed by watched-literal CDCL repair on         state-clause additions for its proof search; SAT reports checked models,
expanding neighborhoods and then the full formula; checked SAT               and parse, verification, or proof failures can yield UNKNOWN.
assignments are emitted, while failed or internally unsatisfiable            VeriPB                                   0.448 ×     0.531 ×      37/53
searches return UNKNOWN because no UNSAT certificate path is                 Watched-literal CDCL drives search, with proof-logged variable
implemented.                                                                 elimination, first-UIP learning, and structural recognition used only
VeriPB                                   0.936 ×        0.936 ×       2/5    for phases and preprocessing. UNSAT emits VeriPB-style RUP
Weighted breakout local search is the active first stage, using the best     constraints and a final empty RUP; SAT reconstructs and checks a
coloring as a phase guide before expanding-neighborhood CDCL                 model but creates no final proof artifact, while malformed input or
repairs and a full CDCL fallback with elimination and reconstruction.        output setup failure yields UNKNOWN.
The recognizer accepts only this non-monochromatic structure;
checked SAT assignments are output, while CDCL UNSAT invokes
VeriPB logging and proof failure yields UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


railway-safety                                                       131   ramsey-numbers                                                      133
9 GBD instances · 2 validation · baseline 0/2                              6 GBD instances · 2 validation · baseline 0/2
These benchmarks ask whether a bounded railway interlocking or             The benchmark asks whether the edges of a complete graph can be
transition-system scenario has a Boolean assignment satisfying its         colored with two colors while avoiding a monochromatic K_s in one
gate, state, and transition constraints together with a selected safety    color and K_t in the other. CNF uses one variable per edge and clauses
obligation. The encoding uses Tseitin-style CNF clauses over those         for every forbidden clique.
variables.                                                                 Proof format                             No verif.    + verif.    Solved
Proof format                             No verif.    + verif.    Solved   GRAT                                      1.98 ×     1.07 ×          1/2
GRAT                                      1.00 ×     1.00 ×          0/2   Specialized comparator networks reduce selected (4,4,n) and (3,6,n)
Preprocessing combines bounded Davis-Putnam elimination and                cases to guarded core cases, using ordering and branch exclusions for
binary-implication SCC reduction with watched-literal CDCL; very           the former and selection/profile sorting before CDCL for the latter. It
wide terminal clauses trigger failed-literal decomposition, while          handles dispatched instances through an induced 18-vertex core, emits
smaller cases use residual CDCL. Outside structural recognition it         proof clauses and comments for GRAT checking, and otherwise
returns UNKNOWN; SAT models are checked against the original               returns UNKNOWN.
CNF, and UNSAT steps are logged as textual DRAT for external               DPR                                        1.00 ×     1.00 ×         0/2
elaboration and checking.                                                  An edge-indexed CDCL engine uses watched literals, clause learning,
DPR                                       1.00 ×     1.00 ×          0/2   and restarts; selected recognized cases search an induced core. It
Failed-literal probing ranks literals in a syntactically wide clause;      accepts only the canonical encoding and supported range, serializes
first-UIP CDCL searches branches under their negations and otherwise       learned clauses and deletions for DPR elaboration and checking, and
falls back to ordinary CDCL. Malformed input returns UNKNOWN;              returns UNKNOWN when unsupported or failing; SAT from a core
SAT models are checked against original clauses, while UNSAT               need not model the full input.
logging records learned clauses and failed-literal units, can include      VeriPB                                     1.00 ×     1.00 ×         0/2
witness-free clause additions, and closes with an empty clause.            An extrema-degree PB route targets (3,6;19), using symmetry and
VeriPB                                    1.00 ×     1.00 ×          0/2   CDCL to establish units before summing degree bounds into a PB
A final wide, all-negative clause activates assumption-based               contradiction. If it does not finish, symmetry-guided CDCL is the
decomposition: watched-literal first-UIP CDCL tries each tail literal,     fallback; PB/RUP records are logged, SAT models are checked, only
retains learned consequences, and uses ordinary CDCL otherwise.            exhaustive encodings are accepted, and unsupported or unresolved
Outside recognition it returns UNKNOWN; SAT models are checked             cases return UNKNOWN.
against original clauses, while UNSAT learned clauses are emitted as
VeriPB RUP records followed by an UNSAT conclusion.                        ramseycube                                                          134
                                                                           10 GBD instances · 2 validation · baseline 2/2
ramsey                                                               132   These CNFs ask whether the edges of a complete graph can be colored
6 GBD instances · 2 validation · baseline 1/2                              with two colors while avoiding monochromatic subgraphs. Variables
These benchmarks ask whether the edges of a complete graph can be          represent graph edges, and signed clauses encode forbidden 3-cubes,
colored so that specified forbidden subgraphs are not monochromatic.       with some encodings also constraining a specified color on four-cycles.
Boolean CNF encodes the edge colors and may add auxiliary variables        Proof format                             No verif.    + verif.    Solved
and clauses for local color constraints.                                   GRAT                                       1.04 ×     1.29 ×         2/2
Proof format                             No verif.    + verif.    Solved   Structural Q3/C4 recognition uses prescribed n=8-20 patterns and
GRAT                                      0.998 ×    0.988 ×         1/2   fixed-coloring witnesses for small SAT cases, verifying every clause
Line-graph reconstruction drives the K32 four-color path, which            before SAT. Asymmetric instances use a complete K9 core with 1-UIP
applies an F2^4 edge coloring; a direct K18 path instead uses              CDCL, emitting learned clauses and an empty clause for external
symmetry-breaking sorting and a CDCL tail. SAT assignments are             DRAT elaboration; unsupported inputs and symmetric K13 return
checked against the clauses; UNSAT paths emit textual DRAT traces          UNKNOWN.
for external elaboration, while generic Ramsey-shaped inputs use           DPR                                        3.06 ×    0.738 ×         2/2
CDCL and rejected inputs return UNKNOWN.                                   Embedded colorings answer small SAT cases by mapping supported
DPR                                      4,220 ×      91.0 ×         2/2   lexicographic K_n edge layouts to fixed assignments and checking
Structural recognition drives Ramsey-specific paths: four-color cases      every clause. Asymmetric inputs with an induced K9 core use 1-UIP
use bounded min-conflicts search on a recovered 3-uniform                  CDCL and log learned clauses plus an empty clause; unsupported
hypergraph, with a paired two-color fallback. SAT candidates are           layouts, failed checks, and symmetric n=13 return UNKNOWN.
checked against the input CNF; exact recognized layouts alone receive      VeriPB                                     230 ×     30.8 ×          2/2
UNSAT certificates from bundled DPR templates, while failed bounded        Threshold-core detection searches for K13 or K9 complete cores,
search or other cases return UNKNOWN.                                      deletes clauses outside the core, and adds permutation-witnessed
VeriPB                                    1,990 ×     184 ×          2/2   symmetry breaking before watched-literal CDCL. Only core UNSAT
Min-conflicts recoloring handles recognized four-color layouts,            receives RUP-logged VeriPB output; direct-formula UNSAT and
propagating gate variables after a candidate is found; a separate          unsupported or unmatched inputs return UNKNOWN, while checked
R(4,4;18) path reconstructs edge structure, adds symmetry reductions,      SAT models are returned.
and runs CDCL. Clause-checked SAT candidates are accepted; the
R(4,4;18) path emits VeriPB red and RUP steps for UNSAT, while
R(4,5;25) inputs and failed bounded searches return UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

random                                                               135    random-clustered                                                   137
872 GBD instances · 175 validation · baseline 86/175                        36 GBD instances · 8 validation · baseline 4/8
This family asks whether a Boolean assignment can satisfy every             The benchmark asks whether a Boolean assignment can make every
clause in a random-style CNF formula, or whether no such assignment         clause in a sparse 3-CNF formula true. Inputs use three-literal clauses
exists. Instances encode clauses as sets of signed literals, often with a   and are intended to exhibit clustered variable co-occurrence, although
broadly uniform short width.                                                recognizer filters describe only supported encodings, not the entire
Proof format                             No verif.     + verif.    Solved   family.
GRAT                                       1.44 ×      1.43 ×     114/175   Proof format                             No verif.   + verif.    Solved
ProbSAT-style local search leads, using false-clause sampling,              GRAT                                       1.00 ×    1.00 ×         4/8
break/make counts, and restarts; its finite budget is not an UNSAT          Break-weighted stochastic local search drives accepted 3-CNF
conclusion before watched-literal CDCL takes over. Verified SAT             instances, choosing variables from unsatisfied clauses and updating
assignments are emitted; UNSAT requires a textual DRAT stream               clause counts, occurrence lists, and unsatisfied-clause state
ending in the empty clause for external elaboration, while                  incrementally. A found assignment is independently checked before
nonmatching or failed cases return UNKNOWN.                                 SAT output; rejected inputs return UNKNOWN, while unsuccessful
DPR                                        1.13 ×      1.12 ×      96/175   accepted searches continue restarting without an UNSAT proof path.
Incremental probSAT-style local search samples false clauses and uses       DPR                                       1.00 ×     1.00 ×         4/8
break/make scoring with random restarts, but is gated off for some          Structural recognition selects supported clustered 3-CNF instances,
narrow-width, dense, or high-ratio cases. Watched-literal CDCL then         then randomized break-weighted local search flips variables from
supplies a checked SAT assignment or, after a level-zero conflict, an       unsatisfied clauses while maintaining clause counts and occurrence
UNSAT result with clause-addition proof; rejected inputs and proof or       data incrementally. It independently checks and emits complete SAT
reconstruction failures yield UNKNOWN.                                      assignments; unsupported inputs return UNKNOWN, while
VeriPB                                    1.50 ×       1.50 ×     117/175   unsuccessful accepted searches restart without an UNSAT or DPR
Focused ProbSAT/WalkSAT local search leads, sampling variables              certificate path.
from false clauses with break-weighted and occasional make-aware            VeriPB                                     1.00 ×    1.00 ×        4/8
moves; default routing can give some recognized shapes an                   Bounded ProbSAT searches recognized instances with break-weighted
unbounded search, so they may not reach the exact fallback. The exact       flips from unsatisfied clauses, then falls back to watched-literal CDCL
CDCL fallback verifies SAT assignments and emits VeriPB RUP                 with clause learning when it fails. SAT assignments are checked
constraints for UNSAT; solver or proof-file failures yield UNKNOWN.         against clauses; CDCL UNSAT paths serialize a RUP-based proof for
                                                                            external VeriPB checking, while unsupported inputs return
                                                                            UNKNOWN and local-search failure alone does not establish UNSAT.
random-circuits                                                      136
21 GBD instances · 5 validation · baseline 4/5
                                                                            random-csp                                                         138
The task is to choose Boolean primary inputs so an acyclic fixed-width
                                                                            24 GBD instances · 5 validation · baseline 3/5
lookup circuit produces a prescribed pattern on its final output bits.
CNF uses truth-table clauses for the gates and unit clauses to fix the      These instances ask whether each object in a finite binary CSP can
target outputs.                                                             take one value while avoiding forbidden unary and pairwise
                                                                            combinations. CNF encodings often use exactly-one selector blocks or
Proof format                             No verif.     + verif.    Solved
                                                                            compact bit blocks defining legal states, with cross-object clauses
GRAT                                      78.0 ×       61.0 ×         5/5
                                                                            forbidding state pairs.
AVX-512 batched truth-table enumeration first tests compatible
primary-input assignments, pruning gates outside the target cone. A         Proof format                             No verif.   + verif.    Solved
CDCL fallback propagates table rows and learns first-UIP clauses            GRAT                                       13.7 ×    13.6 ×         5/5
when enumeration is unavailable or finds no model; verified SAT             State-level CDCL over the recovered finite-domain CSP leads the
assignments are emitted, while unsupported inputs or failed search          search, followed by arc-consistency backtracking and local repair or
return UNKNOWN, with no UNSAT certificate path.                             min-conflicts methods. Reconstructed assignments are checked against
                                                                            the original clauses before SAT output; failed finite phases may enter
DPR                                        1.24 ×      1.24 ×         4/5
                                                                            restart cycles until externally stopped, and no UNSAT certificate path
Target-cone reduction replaces each relevant forbidden truth-table          is implemented.
block with compact implications before a watched-literal CDCL search.
The search uses a topological order portfolio, retrying with another        DPR                                        540 ×     534 ×          5/5
order after a bounded attempt; verified SAT models are emitted, while       Structure recovery compiles recognized one-hot or compact-state CNF
unsupported layouts or failed search return UNKNOWN and no                  into domains with unary costs and forbidden pairs, then uses belief
UNSAT certificate is produced.                                              propagation, tabu or min-conflicts search, and consistency repairs.
                                                                            Feasible assignments are mapped back and checked against clauses
VeriPB                                     9.80 ×      7.53 ×         5/5
                                                                            before SAT output; unsupported or unsuccessful cases return
Batched truth-table enumeration with root bitset filtering first tests      UNKNOWN, with no UNSAT certificate path.
eligible recognized circuits. The fallback searches backward from fixed
outputs, choosing a gate with the smallest compatible preimage set          VeriPB                                     19.4 ×    19.3 ×        5/5
and propagating bitset domains; verified SAT assignments are emitted,       Damped belief propagation seeds weighted breakout and tabu search
while unsupported layouts, contradictions, or exhaustion return             on recovered CSPs; arc-consistency masks and dom/wdeg
UNKNOWN, with no UNSAT certificate path.                                    backtracking provide fallback. Original clauses are checked for SAT
                                                                            assignments; the unbounded WalkSAT route has no complete fallback,
                                                                            while unsupported or failed searches return UNKNOWN and no
                                                                            VeriPB logger provides an UNSAT certificate.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


random-hiddenmodel                                                  139    random-mus                                                            141
117 GBD instances · 24 validation · baseline 16/24                         14 GBD instances · 3 validation · baseline 0/3
The benchmark asks whether a Boolean assignment satisfies every            This family asks whether one Boolean assignment satisfies every
clause of a structured CNF formula whose clauses contain two or three      disjunction of signed literals in a CNF formula. The recognized inputs
distinct variables. A recurring subpattern translates to odd-parity XOR    use a restricted mix of two- and three-literal clauses; the label does not
equations, but it is only a special subfamily, not the definition of the   establish provenance or minimal unsatisfiability.
benchmark.                                                                 Proof format                             No verif.     + verif.     Solved
Proof format                             No verif.    + verif.    Solved   GRAT                                      1.00 ×      1.00 ×          0/3
GRAT                                      1.16 ×      1.16 ×      17/24    ProbSAT local search with break-weighted flips is the active first stage,
Parity shortcuts and spectral-seeded NAE or focused local search first     and verified models terminate the search. Failure triggers bounded
seek checked satisfying assignments, followed by watched-literal           elimination, vivification, and watched-literal first-UIP CDCL; SAT
CDCL when those searches fail. The parity and heuristic paths have no      assignments are checked, while UNSAT logs derived clauses and an
UNSAT certificate; the fallback logs learned clauses and a root conflict   empty clause in a DRAT trace intended for external elaboration, with
as DRAT additions for external elaboration, while unresolved or            unsupported inputs returning UNKNOWN.
unsupported cases return UNKNOWN.                                          DPR                                       1.00 ×      1.00 ×          0/3
DPR                                       1.01 ×      1.01 ×      16/24    WalkSAT with break-count choices leads the search before fallback. If
Validated structure sends odd 3-XOR blocks to packed GF(2)                 no verified model is found, bounded elimination and watched-literal
elimination; other recognized formulas use bounded focused search,         CDCL emit a textual DPR/RUP-style trace; unsupported inputs and
width-2 inputs go directly to CDCL, and nonmatching inputs return          some failures return UNKNOWN, and optional lookahead is inactive
UNKNOWN. Checked SAT models certify satisfiability; the fallback           by default. External elaboration and checking are outside the solver;
logs witness-free DPR RUP additions for learned clauses and an empty       no certificate validation is claimed.
clause, requiring external elaboration and checking.                       VeriPB                                    1.00 ×      1.00 ×          0/3
VeriPB                                    1.28 ×      1.23 ×      18/24    On recognized inputs, break-only probSAT with weighted flips leads
Packed GF(2) elimination handles the recognized odd-XOR signature,         the search, and every candidate model is checked against the input.
then majority/minority seeds and focused ProbSAT search seek a             After local search fails, bounded variable elimination and
checked model before watched-literal CDCL takes over. The fallback         watched-literal 1-UIP CDCL continue until SAT or UNSAT; the fallback
logs learned clauses and the root conflict as VeriPB RUP constraints,      logs VeriPB RUP constraints, while probSAT failure alone produces no
including deletions and a final UNSAT conclusion for external              UNSAT certificate and unsupported inputs return UNKNOWN.
verification; malformed or unresolved inputs return UNKNOWN.
                                                                           random-planted-solution                                               142
random-modularity                                                   140    328 GBD instances · 66 validation · baseline 60/66
59 GBD instances · 12 validation · baseline 11/12                          The task is to find a Boolean assignment satisfying every clause of a
The benchmark asks whether a Boolean assignment satisfies every            random planted-solution CNF. Recognized inputs have three literals
clause in a CNF formula, or whether no such assignment exists.             over distinct variables per clause, with selected density ranges.
Variables are grouped into communities, with many short clauses local      Proof format                             No verif.     + verif.     Solved
to one community and fewer clauses linking communities.                    GRAT                                      3.37 ×      3.37 ×        64/66
Proof format                             No verif.    + verif.    Solved   Triple-parity belief propagation seeds the exact 4.41-density branch,
GRAT                                     0.203 ×     0.204 ×       4/12    while other recognized densities use signed-pair spectral power
Community decomposition leads on recognized fixed-size layouts:            iteration; both feed focused local search with break-score and polarity
local DPLL handles contiguous blocks, followed by damped                   restarts. A verified full assignment is emitted on success, but
belief-propagation decimation for cross-block search and a bounded         malformed or out-of-band inputs return UNKNOWN, and recognized
elimination followed by CDCL fallback. UNSAT proofs are emitted as         failures continue through unbounded restarts without an UNSAT
textual DRAT for external elaboration; SAT models are checked, and         certificate path.
unrecognized or unresolved inputs return UNKNOWN.                          DPR                                      0.796 ×      0.796 ×       57/66
DPR                                      0.229 ×     0.228 ×       5/12    Signed spectral seeding and degree-normalized power iteration
Contiguous-community decomposition leads the search on recognized          initialize break-weighted local search, with belief propagation and
fixed-size layouts: deterministic DPLL handles sufficiently dense          survey decimation added only in the exact 4.41-density branch. It
community blocks, followed by weighted coordinate repair and CDCL          verifies any complete satisfying assignment, but unsupported inputs
fallbacks for bridge clauses. Local contradictions and global CDCL         return UNKNOWN and failed recognized searches can remain in
refutations are recorded as DPR additions; checked SAT models are          unbounded random restarts; no UNSAT certificate path is
output, while unsupported or unresolved cases return UNKNOWN.              implemented.
VeriPB                                   0.331 ×     0.333 ×       7/12    VeriPB                                   0.655 ×     0.655 ×        54/66
Incremental ProbSAT-style search leads on recognized layouts,              Planted-likelihood belief propagation with confidence-guided
followed by community-product block search with projected DPLL             decimation supplies seeds, followed by bounded Hamming and
repairs and an unbounded CDCL fallback. SAT assignments are                make-break repair and, on some paths, learned-clause CDCL
checked; a completed CDCL refutation is written as VeriPB RUP steps,       completion. The solver independently checks a full satisfying
while formulas outside the recognized structure or unfinished              assignment; unsupported or unsuccessful runs return UNKNOWN, no
refutations return UNKNOWN.                                                UNSAT certificate is produced, and a middle-density branch can
                                                                           remain in unbounded decimation and repair.
The Case for Automated Hyperspecialization:
Evidence from SAT

rbsat                                                              143    register-allocation                                                 145
116 GBD instances · 24 validation · baseline 4/24                         20 GBD instances · 4 validation · baseline 4/4
The benchmark asks whether each finite-domain object can take             The benchmark asks whether an interference graph can assign one of
exactly one value while avoiding listed forbidden value pairs between     k registers to each vertex so adjacent vertices differ. CNF uses x[v,c]:
objects. Its recognized CNF uses one signed choice block per object,      positive vertex clauses require registers, while negative edge clauses
one at-least-one clause, pairwise at-most-one clauses, and binary         forbid adjacent vertices from sharing a register.
clauses forbidding cross-object pairs.                                    Proof format                             No verif.    + verif.    Solved
Proof format                             No verif.    + verif.   Solved   GRAT                                       13.4 ×     1.75 ×         4/4
GRAT                                      2.37 ×      2.37 ×     17/24    Maximum Cardinality Search drives chordal coloring for the exact
Structure-aware finite-domain search leads with weighted                  direct encoding (3 <= k <= 20, at most 5000 vertices). Checked
min-conflicts, arc-consistent repair, and belief-propagation decimation   colorings provide SAT assignments; if they fail, DSATUR seeks a
before falling back to watched-literal CDCL with clause learning. SAT     model or a bounded clique search can emit a pigeonhole DRAT proof,
assignments are checked against the CNF; UNSAT is certified by a          with unresolved or unsupported cases returning UNKNOWN.
separate CDCL rerun that writes DRAT additions for external               DPR                                       15.4 ×      1.34 ×         4/4
elaboration and checking, while recognition or certifying failure can     Bitset clique search leads the direct-coloring workflow, restricted to
return UNKNOWN.                                                           complete consecutive-block encodings with 1 <= k <= 63 and at most
DPR                                       2.80 ×     2.80 ×      17/24    8192 vertices; reverse-MCS and greedy coloring seek a checked SAT
Signed one-hot recognition and bit-mask arc consistency drive the         assignment. A rechecked (k+1)-clique yields a deletion-based
exact search after a bounded randomized min-conflicts pass, using         pigeonhole DPR proof; otherwise exponential DSATUR emits rejection
dom/wdeg variable selection and least-damaging values. SAT                blocks, and unresolved cases return UNKNOWN.
assignments are checked; after failed searches, a separate                VeriPB                                     13.6 ×    14.8 ×         4/4
unit-propagation DFS emits a tree-style proof of UNSAT with decision      Bitset clique search and maximum-cardinality analysis guide the
nogoods and an empty clause, without independent verification;            restricted contiguous-block recognizer for k >= 3; other inputs return
unrecognized encodings return UNKNOWN.                                    UNKNOWN. Greedy coloring seeks a checked SAT assignment, while
VeriPB                                    2.68 ×      2.68 ×     17/24    exact component-wise DSATUR handles unresolved cases. A
Structural one-hot recovery drives randomized constructive search,        rechecked clique yields VeriPB pseudo-Boolean proofs, and exact
tabu or message-passing repair, weighted local search, and bounded        search emits RUP nogoods; model checks or proof-output failures
MAC before a CSP-directed CDCL scout. A SAT assignment is                 return UNKNOWN.
clause-checked; only a scout UNSAT result enables a logged CDCL
rerun with VeriPB RUP constraints for UNSAT certification, while          relational-dependencies                                             146
failure enters unbounded diversified search rather than UNKNOWN.          20 GBD instances · 4 validation · baseline 4/4
                                                                          The benchmark asks whether variables can satisfy Horn dependencies
reg-n                                                              144
                                                                          while limiting false primary variables and true auxiliary variables. Its
60 GBD instances · 12 validation · baseline 8/12
                                                                          CNF encoding uses clauses for a and b imply c plus complete subset
These structured formulas assign Boolean color choices to objects         blocks that impose the two cardinality limits.
arranged by a hierarchy. Positive clauses require a choice for each
                                                                          Proof format                             No verif.    + verif.    Solved
object; tree or product-based exclusions, sometimes expanded into
                                                                          GRAT                                       26.0 ×    2.74 ×          4/4
ternary and longer clauses, constrain which choices can coexist.
                                                                          A Horn-closure shortcut sets the first block true and second block
Proof format                             No verif.    + verif.   Solved
                                                                          false; if it fails, watched-literal CDCL uses implicit cardinality
GRAT                                      1.00 ×      1.01 ×      8/12    propagation and branches only on the first block. SAT assignments are
Parity-based canonicalization and rank-indexed checking recover tree      checked against the input, while UNSAT paths emit textual DRAT;
coordinates and verify every required clause family exactly once. For     unrecognized formulas or unresolved failures return UNKNOWN.
supported fixed regimes, the solver remaps variables in a packed
                                                                          DPR                                        33.1 ×     1.69 ×         4/4
regime-specific DRAT template and reports UNSATISFIABLE only
after replay succeeds; it has no general SAT search, and unsupported      A closure-pruned primary-variable search uses Horn forward chaining,
or malformed structures or missing proof data return UNKNOWN.             cardinality cutoffs, and lookahead branch selection; a SAT survey may
                                                                          supply a model or reusable tree. SAT models receive a raw clause
DPR                                       1.00 ×     0.287 ×      8/12    check; on recognized instances, UNSAT searches serialize search trees
Product-run detection and polarity-specific OR extensions compact         as witness-free DPR additions, while construction or writing failure
recognized contiguous Cartesian-product layouts before a                  returns UNKNOWN.
watched-literal first-UIP CDCL search. UNSAT results are logged as a
                                                                          VeriPB                                    35.4 ×     0.504 ×        4/4
textual DPR-style stream with RAT-style definitions, deletions, and
CDCL lemmas, while SAT assignments are checked against the original       Certifying primary-variable search forward-chains Horn rules with
CNF; failed recognition or internal failure returns UNKNOWN.              bitmask closure and causal conflict clauses; it first tries a bounded
                                                                          natural-order search, then an unbounded degree-scored fallback. SAT
VeriPB                                    1.01 ×     1.01 ×       8/12    leaves receive structural checks, while UNSAT traversals write RUP
Canonical variable recovery and exact, order-sensitive clause             and cutting-planes resolution steps in VeriPB; unsupported inputs or
validation identify the hierarchical coloring structure without a SAT     failed checks or proof failures return UNKNOWN.
search. It introduces event, z, and a variables with red constraints,
aggregates occurrences into macro conflicts, and emits RUP
tree-resolution steps in a VeriPB text proof; recognition or output
failures return UNKNOWN, and the source includes no verifier.
                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


relativized-pigeon-hole                                                147   risc-instruction-removal-subrv                                       149
55 GBD instances · 11 validation · baseline 8/11                             21 GBD instances · 5 validation · baseline 0/5
The benchmark asks whether p first-layer pigeons can choose distinct         The benchmark asks whether an acyclic Boolean netlist has an
objects, while each chosen object chooses a distinct one of only p-1         assignment satisfying its gate constraints and three terminal unit
final holes. A CNF uses choice, activation, and object-to-hole variables,    clauses. In CNF, each later variable is constrained as a Boolean
with existence, implication, and collision clauses encoding these two        function of up to three earlier variables.
injective assignments.                                                       Proof format                             No verif.    + verif.     Solved
Proof format                             No verif.    + verif.    Solved     GRAT                                      1.00 ×      1.00 ×         0/5
GRAT                                       1.51 ×     3.36 ×        9/11     It uses bounded-cone MiniCDCL and parity union-find to discover
Extension-variable composition and a sequential at-most-one counter          endpoint relations, then applies truth-table closure with local clause
reduce complete recognized encodings to an ordinary pigeonhole               proving. It reports UNSAT only when closure derives a contradiction,
contradiction. The UNSAT branch writes DRAT records containing               emitting textual DRAT additions for external elaboration and
extension clauses, derived clauses, deletions, and an empty clause; one      checking; unsupported inputs or failed closure return UNKNOWN,
omitted color-collision case instead gets a checked SAT model, while         and no SAT-witness path is implemented.
unsupported, over-limit, or proof/model failures return UNKNOWN.             DPR                                       1.00 ×      1.00 ×         0/5
DPR                                        1.51 ×    0.720 ×        9/11     It uses template-based gate propagation in CDCL, initially deciding on
Structural recognition drives a square-case matching proof and a             non-output variables and falling back to all variables when that queue
rectangular-case witness-backed repair with case splits that derive          empties. It reports UNSAT after a root conflict and logs learned clauses
canonical selector units before an inner pigeonhole proof. Clause            with a terminal empty clause, but has no SAT-witness path;
additions may be witness-free; one-clause-short forms receive only a         unsupported, oversized, or completed satisfiable cases return
checked SAT construction, limited to supported missing-tuple cases,          UNKNOWN.
and unsupported inputs or failures return UNKNOWN.                           VeriPB                                    1.00 ×     1.00 ×          0/5
VeriPB                               2.94·104 ×       335 ×        11/11     It uses formula-seeded, 64-lane bit-parallel evaluation of recognized
Pseudo-Boolean clique counting is central: lower bounds force at least       functional gates, filtering lanes by the unit clauses and selecting a
p active objects, while per-hole demand and clique capacities cap them       surviving assignment for direct clause checking. It emits a checked
at p-1, yielding a streamed UNSAT proof. One omitted second-layer            SAT assignment when one survives, but has no UNSAT or VeriPB
collision instead uses a constructed and checked SAT model with no           certificate path; unsupported inputs or no surviving lane return
UNSAT certificate path; unsupported forms or failures return                 UNKNOWN.
UNKNOWN.
                                                                             rooks                                                                150
risc-instruction-removal-golcrest                                      148   30 GBD instances · 6 validation · baseline 0/6
9 GBD instances · 2 validation · baseline 1/2                                The benchmark asks whether n+1 squares can be selected on an n by n
These benchmarks encode relational checks on a processor circuit.            board while no row contains more than one selected square. CNF uses
Primary inputs and ordered auxiliary variables represent Boolean             cell variables, row-conflict clauses, and an exact-cardinality constraint
signals, while Tseitin gate clauses and fixed endpoint conditions ask        represented by a BDD.
whether the encoded circuit admits a consistent assignment.                  Proof format                             No verif.    + verif.     Solved
Proof format                             No verif.    + verif.    Solved     GRAT                                 1.10·104 ×       7.43 ×         6/6
GRAT                                     0.667 ×     1.55 ×            0/2   Layered ordered-BDD recognition drives a frontier-state proof:
Packed truth-pattern simulation groups equal or complemented                 sequential row-prefix variables track occupied rows, and minimal
variable signatures to propose units and equivalences, then checks           fixed-cardinality masks are propagated from deep BDD layers upward
each candidate by watched-literal RUP. Bounded propagation-only              to emit the certificate. It is UNSAT-only for the recognized row-based
closure emits accepted RUP clauses and an empty clause on                    encoding; unsupported structure, resource limits, or proof-generation
contradiction; unsupported encodings or no contradiction return              failure yield UNKNOWN rather than invoking general SAT search.
UNKNOWN, and no SAT assignment path is implemented.                          DPR                                   1.05·104 ×      5.30 ×         6/6
DPR                                      0.667 ×     1.55 ×            0/2   BDD recovery and frontier-limited dynamic programming drive the
Reduced ordered BDD construction uses interleaved primary-input              proof: occupancy variables and bitmask states summarize filled rows,
ordering and unique-node/apply caching to evaluate the recognized            while threshold-based minimal occupied subsets prune recursive BDD
circuit directly. It reports UNSAT only for a terminal-true target,          traversal; a cofactor fallback handles canonical ITE cases. It is
emitting witness-free DPR additions for the derivation and final empty       UNSAT-only for the narrow recovered row-capacity encoding;
clause; strict width-8 and input-count checks, resource limits, and          recognition or generation failure returns UNKNOWN without general
other outcomes return UNKNOWN, with no SAT witness path.                     SAT search.
VeriPB                                   0.667 ×     1.55 ×            0/2   VeriPB                                     584 ×     14.9 ×          6/6
Bounded Davis-Putnam elimination preprocesses the CNF by                     Pseudo-Boolean cutting planes drive an UNSAT certificate: row
removing low-occurrence variables within resolvent bounds, then              at-most-one inequalities provide an upper bound of n, while
watched-literal CDCL solves the reduced instance. It logs BVE                proof-only one-unit flow through the ordered BDD and a
resolvents, learned clauses, and terminal conflicts as VeriPB steps,         rank-weighted potential derive the lower bound n+1. The solver
checks SAT assignments against the original clauses, and returns             accepts only the recognized square, row-based BDD structure;
UNKNOWN when eliminated variables cannot be reconstructed.                   recognition or proof-emission failure returns UNKNOWN, with no
                                                                             SAT/model path.
The Case for Automated Hyperspecialization:
Evidence from SAT

rubikcube                                                            151    satcoin                                                             153
20 GBD instances · 4 validation · baseline 0/4                              20 GBD instances · 4 validation · baseline 0/4
Bounded Rubik’s Cube reachability asks whether legal face turns can         The supported satcoin instances ask whether a 32-bit nonce in a
transform an initial cube state into the solved state within a fixed move   specified range makes a Bitcoin-genesis header satisfy a
horizon. A CNF encoding represents move choices and intermediate            double-SHA-256 difficulty target. The CNF bit-blasts the hashing
states, constraining transitions and the final solved configuration.        circuit and the constraints selecting candidate nonces.
Proof format                             No verif.    + verif.     Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                      1.00 ×      1.00 ×         0/4    GRAT                                      1.00 ×     0.557 ×         0/4
Watched-literal CDCL with activity branching, learning, restarts, and       Bit-parallel unit propagation tests up to 64 interval candidates at once
clause reduction is the main search, using recovered move-variable          after a bounded two-equality recognizer identifies the 32-bit range.
preferences only for a canonical cube layout. An optional two-phase         When every lane is refuted, an MSB-first interval tree emits
search precedes it and falls back to CDCL; checked SAT assignments          propagation-checked DRAT additions and deletions for external
are accepted, while UNSAT uses DRAT-style traces for external               elaboration; a surviving lane, recognition failure, or proof-generation
certification and proof or certification failures return UNKNOWN.           failure returns UNKNOWN.
DPR                                       1.00 ×      1.00 ×         0/4    DPR                                       1.00 ×      1.00 ×         0/4
Recovered cube permutations drive two-phase cubie search with BFS           64-lane bit-parallel propagation scans recognized interval candidates,
pruning and move-word restrictions, but only on the recognized              with scalar clause propagation as a fallback for unresolved groups. An
canonical layout and bounded horizon. A path gets auxiliary                 all-clause-satisfying candidate yields a checked complete assignment.
completion and full original-CNF checking; failed search or validation      When all candidates are refuted, it adds blocking clauses for covered
returns UNKNOWN, while optional proof writers emit DRAT-style               cubes, including witness-free batch additions, and uses a high-bit-first
traces for external DPR elaboration and checking.                           closing tree; unresolved, recognition, or resource-limit failures return
VeriPB                                    1.00 ×     1.00 ×          0/4    UNKNOWN.
Generator-numbered gadget validation, coordinate pruning tables, and        VeriPB                                    1.00 ×      1.00 ×        0/4
depth-fixed two-phase DFS search only the recognized layout and             Double-SHA-256 evaluation of extracted nonces drives the search after
phase schedule. On failure, ProofCDCL probes scoped suffixes for SAT,       recognizing a restricted CNF layout and interval. A hash hit returns
then runs watched-literal CDCL with RUP lemmas and PBC subproofs;           UNKNOWN because no CNF model is reconstructed; otherwise a
checked models are accepted, while UNSAT requires a level-zero              prefix tree emits VeriPB blockers and RUP parent steps for UNSAT,
conflict and otherwise returns UNKNOWN.                                     with structural leaf checks and UNKNOWN on recognition or
                                                                            proof-writing failure.
sat-x                                                                152
20 GBD instances · 4 validation · baseline 1/4                              scheduling                                                          154
The benchmark asks whether fixed-width integer words satisfy a              435 GBD instances · 87 validation · baseline 52/87
cube-sum equation, typically X^3 - Y^3 - Z^3 = 3, with optional             These scheduling CNFs ask whether games or jobs can be assigned to
bounds or range restrictions. CNF represents the arithmetic with bit        rounds, dates, venues, or workers while respecting one-assignment,
vectors and Tseitin auxiliary variables, plus clauses enforcing             conflict, home/away, break, and exclusion constraints. Variables
constants, targets, comparisons, and exact-width arithmetic.                represent assignments and auxiliary conditions, and clauses enforce
Proof format                             No verif.    + verif.     Solved   the allowed choices and incompatibilities.
GRAT                                      1.01 ×      1.02 ×         1/4    Proof format                             No verif.    + verif.    Solved
Bounded signed cube identities and 2-adic cube-root lifting generate        GRAT                                     0.645 ×     0.687 ×      25/87
candidate words; propagation and residual DPLL complete and                 Circle-method one-factorization and layered orientation dynamic
validate each candidate before SAT output. Failures return                  programming construct recognized double-round-robin schedules
UNKNOWN, and the cube path has no UNSAT certificate; only a                 while tracking venue alternation and rejecting forbidden break runs.
narrow 16-bit Brocard branch uses CDCL and logs learned clauses plus        Watched-literal propagation completes auxiliary variables and
a contradiction for external DRAT elaboration.                              validates SAT assignments; bounded MiniCdcl or Hall and matching
DPR                                      0.758 ×     0.764 ×         0/4    refutations cover selected cases, while failed or unsupported cases
An embedded arithmetic witness fixes the inputs of recognized cubic         return UNKNOWN and UNSAT paths log DRAT additions.
layouts; flat propagation and residual watched-literal DPLL complete        DPR                                      0.572 ×     0.609 ×      17/87
the assignment and rescan all clauses before SAT output. Failed             Structural fingerprints dispatch narrow encodings; circle factorization
searches return UNKNOWN; the cubic path has no UNSAT certificate,           fixes Break schedules and derives home/break variables, followed by
while a narrow Brocard fallback uses CDCL and logs learned clauses          unit propagation and residual auxiliary-only DPLL. SAT valuations are
for external DPR elaboration and checking.                                  clause-scanned, but one CDCL path can leave entries unassigned and
VeriPB                                   0.758 ×     0.764 ×         0/4    validate them as true; selected UNSAT cases emit tree or learned-clause
For recognized cubic layouts, an embedded witness fixes the cubic           additions, while unsupported or failed cases return UNKNOWN.
inputs; occurrence-indexed propagation and false-first residual             VeriPB                                   0.830 ×     0.881 ×      39/87
backtracking complete the assignment and validate clauses before SAT        Symmetry-preserving red and RUP derivations exploit recognized
output. A small Brocard fallback uses watched-literal CDCL and emits        round-robin structure, while matching uses augmenting paths and
VeriPB RUP steps for UNSAT; failures return UNKNOWN, with no                Hall-style deficiencies. A bounded monotone-choice search, with
generic UNSAT certificate or in-process proof check.                        stochastic construction only outside break encodings, precedes
                                                                            watched-literal first-UIP CDCL; SAT assignments are checked,
                                                                            specialized UNSAT derivations require proof output, and unresolved
                                                                            cases can return UNKNOWN.
                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


school-timetabling                                                    155    sgen                                                                157
60 GBD instances · 8 validation · baseline 6/8                               128 GBD instances · 26 validation · baseline 4/26

The task asks whether courses with weekly loads can be assigned time         The benchmark asks whether a Boolean assignment satisfies every
slots and eligible teachers or resources while respecting daily blocks,      signed CNF clause. Its instances use structured encodings of
occupied-day limits, availability, and non-overlap constraints. CNF          exact-cover, counting, matching, or counter constraints, represented
encodings use course-period, day-use, resource-choice, and auxiliary         by unit, binary, and wider clauses.
cardinality or conflict variables.                                           Proof format                             No verif.    + verif.    Solved
Proof format                             No verif.     + verif.     Solved   GRAT                                       1.46 ×     1.47 ×      11/26
GRAT                                     0.945 ×      0.945 ×         5/8    Signed five-variable exact-cover recognition leads to Algorithm
A narrow translated-layout recognizer extracts durations, daily limits,      X/DLX, followed by potentially unbounded stochastic repair, while
educator choices, and availability, then schedules contiguous blocks         separate partition-gap and counter-gap patterns use watched-literal
with legal day allocations and bit masks. Min-conflicts with tabu repair     CDCL. Checked SAT assignments are printed; CDCL UNSAT logs
and random restarts seeks a model; watched-literal completion and            learned clauses, deletions, and an empty clause as textual DRAT for
full clause checks precede SAT output. Unsupported layouts return            external elaboration and checking, whereas unsupported or
UNKNOWN, while scheduling failures retry without an UNSAT                    unresolved cases return UNKNOWN.
certificate path.                                                            DPR                                        1.57 ×     1.58 ×      12/26
DPR                                       1.42 ×      1.42 ×          6/8    Signed exact-cover reconstruction drives fixed-seed min-conflicts with
A structural recognizer extracts the timetable grid, resource choices,       tabu moves, followed by smallest-constraint Algorithm X; compact or
and cardinality constraints, then uses a weighted Hall/max-flow gate         all-ternary cases can fall back to watched-literal CDCL. Verified SAT
followed by randomized min-conflicts repair and bit-mask interval            assignments are printed, while CDCL UNSAT runs log learned clauses,
placement. Propagation and full clause checking precede SAT output;          deletions, and an empty clause for external elaboration; failed searches
failed construction or checking returns UNKNOWN, and no UNSAT                and unresolved larger cases return UNKNOWN.
certificate path is implemented.                                             VeriPB                                   3,900 ×      261 ×       26/26
VeriPB                                   0.793 ×     0.790 ×          5/8    Pseudo-Boolean counting, binary-clique, and sequential-counter
An encoding detector identifies grid, loads, options, and intervals, then    recognition handle structured UNSAT cases first, while SAT search
uses Horn/implication closure, min-conflicts repair, and                     uses augmenting-path matching or bit-parallel exact-cover DFS.
source-sensitive moves. Small residual neighborhoods use                     UNSAT certificates come from counting or counter derivations, or
watched-literal CDCL completion with full clause checks before SAT           from restricted exact-cover refutation with inequalities and RUP
output. Parse or detection failures return UNKNOWN; search may               nogoods; checked SAT models are printed, and unsupported, failed, or
restart indefinitely without an UNSAT certificate path.                      uncertified paths return UNKNOWN.


set-covering                                                          156    sgen-balanced                                                       158
40 GBD instances · 8 validation · baseline 7/8                               4 GBD instances · 1 validation · baseline 1/1
Choose a subset of columns that hits every positive requirement while        The benchmark asks whether a Boolean assignment satisfies a
never choosing both endpoints of a declared conflict. In CNF,                structured 3-CNF formula. Each clause has three distinct variables,
requirements are positive clauses and conflicts are distinct binary          while occurrences are distributed nearly evenly across variables and
negative clauses, yielding an independent hitting-set decision problem.      polarities, often through ordered rounds or layers; the recognizers
                                                                             accept only particular such layouts.
Proof format                             No verif.     + verif.     Solved
GRAT                                       71.5 ×     58.9 ×          8/8    Proof format                             No verif.    + verif.    Solved
A conflict-aware local search first builds an independent hitting set        GRAT                                      9.27 ×     24.6 ×          1/1
through randomized restarts and replacement moves that evict                 On recognized formulas, shallow decisions use clause-pressure scores
conflicting selections. It then falls back to uncovered-row CDCL with        and choose polarity toward lower pressure; deeper search falls back to
learned clauses; checked SAT assignments are reported, while UNSAT           activity-based CDCL with first-UIP learning, restarts, and
is logged in textual DRAT for external checking, and unsupported or          learned-clause reduction. SAT models are checked before printing,
failed cases return UNKNOWN.                                                 while UNSAT runs emit learned-clause additions, deletions, and final
                                                                             empty clause for external elaboration; unsupported formulas or
DPR                                       81.8 ×       52.0 ×         8/8
                                                                             proof-file failure return UNKNOWN.
A bounded focused local search scores flips by coverage and conflict
effects, then falls back to complete fail-first search when it misses a      DPR                                        1.09 ×     2.61 ×         1/1
model. The exact path tracks row coverage and forbidden                      Exact ordered ten-layer inputs, optionally with a partial layer, are
neighborhoods, checks SAT assignments, and emits witness-free RUP            recognized; others return UNKNOWN. Dense pivots trigger
clauses in textual DPR for UNSAT; unsupported forms return                   independent-set elimination with resolvents and reconstruction; CDCL
UNKNOWN.                                                                     is the fallback. SAT checks precede assignment output; UNSAT records
                                                                             learned clauses, resolvents, deletions, and an empty clause;
VeriPB                                     1.73 ×      1.77 ×         7/8
                                                                             reconstruction failure aborts and model-check failure returns
An independence-preserving min-conflicts pass first seeks a cover by
                                                                             UNKNOWN.
evicting conflicting selections, then falls back to exact bitset search on
the smallest compatible domain. It uses conflict-directed backjumping        VeriPB                                   0.998 ×      2.72 ×         1/1
and sibling exclusions, checks SAT assignments, and emits VeriPB RUP         After balanced-shape recognition, it first runs bounded probSAT local
no-goods for external UNSAT checking; unsupported input or                   search with break-count weighting, then independently falls back to
proof-file failure returns UNKNOWN.                                          watched-literal CDCL with phase saving and first-UIP learning.
                                                                             Verified SAT models are printed; UNSAT runs emit parent-logged
                                                                             clauses and a final empty-clause RUP for external checking.
                                                                             Unsupported inputs, proof-file failure, or failed model checks return
                                                                             UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

sliding-puzzle                                                     159    software-bmc                                                         161
62 GBD instances · 13 validation · baseline 0/13                          18 GBD instances · 4 validation · baseline 4/4
The benchmark asks whether a 5x5 board with one blank and 24              The benchmark asks whether a bounded execution of software can
numbered tiles can reach the ordered goal arrangement within a            satisfy its Boolean transition and assertion constraints. Bit-blasting
bounded number of moves. Its CNF encodes initial states, move             program and state bits, with Tseitin variables for intermediate gates,
transitions, and goal checks for this reachability question.              turns this question into CNF whose satisfiability represents a possible
Proof format                             No verif.   + verif.    Solved   execution.
GRAT                                       1.86 ×    1.86 ×       6/13    Proof format                             No verif.    + verif.    Solved
IDA* search combines Manhattan distance with immediate-reversal           GRAT                                      2.94 ×     2.96 ×          4/4
and parity pruning, then a linear-conflict bound, after recognizing the   Watched-literal CDCL with 1-UIP minimization and topology-biased
fixed CNF layout. A found path fixes the encoded state variables, and     decisions drives accepted instances; binary implication specialization
residual DPLL completes and checks the SAT assignment; no UNSAT           serves large bounded-width cases, while local repair is inactive.
certificate path exists, so unsupported or unsolved cases return          Checked SAT models are printed, while root-level UNSAT emits
UNKNOWN.                                                                  learned clauses and the empty clause as textual DRAT for validation;
DPR                                        1.86 ×    1.86 ×       6/13    unsupported inputs or failed checks return UNKNOWN.
IDA* search updates Manhattan distance, suppresses immediate              DPR                                        1.58 ×     1.54 ×         4/4
reversals, and advances bounds by two on the fixed 5x5 layout. Found      Bounded variable elimination with non-tautological resolvents
paths yield checked SAT assignments; after failure, a                     precedes watched-literal CDCL and first-UIP learning on selected
boundary-crossing construction with PHP-style symmetry clauses            formulas; guarded cases use CDCL alone. The aggregate-only
may emit DPR proof through horizon 31, reporting UNSAT only on            recognizer sends unrecognized or resource-failing cases to
success; other cases return UNKNOWN.                                      UNKNOWN rather than falling back, while SAT reconstructs
VeriPB                                    1.86 ×     1.86 ×       6/13    assignments and UNSAT logs clause additions for external DPR
Bounded depth-first A* search combines Manhattan and linear-conflict      elaboration and checking.
bounds with immediate-reversal pruning, child ordering, and a             VeriPB                                     1.09 ×    0.649 ×         4/4
failed-state table. For a found path it tries direction mappings, fixes   Polarity-biased watched-literal CDCL drives recognized inputs, using
selector bits, propagates and checks a complete SAT assignment; no        first-UIP learning, phase saving, and geometric restarts; oversized
UNSAT certificate path exists, so unsupported or no-path cases return     instances are rejected. SAT assignments are checked against original
UNKNOWN.                                                                  clauses, while UNSAT emits learned clauses as VeriPB RUP steps plus
                                                                          an empty RUP and UNSAT conclusion; malformed, unrecognized, or
social-golfer                                                      160    storage-failing cases return UNKNOWN.
39 GBD instances · 8 validation · baseline 3/8
The task arranges players into G groups of P each week for W weeks,       software-verification                                                162
using every player once weekly and preventing any pair from meeting       277 GBD instances · 56 validation · baseline 36/56
twice. CNF clauses encode these group and pair constraints,               These CNFs encode bit-blasted software-verification conditions.
sometimes with auxiliary variables.                                       Boolean variables represent circuit or state signals, while clauses
Proof format                             No verif.   + verif.    Solved   express gate relations, fixed values, and other verification constraints.
GRAT                                       1.27 ×    1.27 ×         4/8   Proof format                             No verif.    + verif.    Solved
Conflict-directed coloring first extracts matching structure from the     GRAT                                     0.950 ×     1.71 ×        35/56
Table encoding, then falls back to Context or classic reconstructions     A bounded reverse-circuit probe evaluates grouped gate definitions in
with specialized schedules, watched propagation, and 1-UIP CDCL. A        parallel with 64-bit lanes and checks candidate assignments against
full SAT assignment is checked against every original clause;             the original CNF. On probe failure, watched-literal CDCL with
unsupported inputs, failed construction, and exhausted search return      first-UIP learning and restarts provides the fallback, logging textual
UNKNOWN, with no UNSAT certificate path implemented.                      DRAT clauses; the probe cannot establish UNSAT, and unrecognized
DPR                                       2.55 ×     2.55 ×         6/8   or oversized inputs return UNKNOWN.
Structural CNF recognition drives schedule reconstruction: table,         DPR                                      0.708 ×      1.25 ×       24/56
context, and classic layouts are decoded by incidence components, pair    Two bounded low-variable probes with opposite phases try SAT or
fingerprints, and supported schedule constructions. The resulting         UNSAT before unbounded CDCL; exhausted probes are discarded. The
assignment is checked against every original clause, but unsupported      fallback uses watched-literal CDCL with VSIDS and first-UIP learning,
or failed cases return UNKNOWN and no UNSAT result or DPR trace           checking SAT models and logging proof-minimized clauses that may
is produced.                                                              be witness-free, including the empty clause for a root conflict. Parse,
VeriPB                                     2.55 ×    2.54 ×        6/8    model-check, and resource failures return UNKNOWN.
Strict Table and Context recognition seeds embedded or finite-field       VeriPB                                   0.638 ×      1.01 ×       20/56
affine schedules, with symmetry alignment and recursive clique-factor     A pre-conflict bias toward low variable IDs exploits the expected
search as bounded construction fallbacks. Unit propagation and            primary-before-derived allocation. The sole search engine is
false-phase completion fill the assignment before every original clause   watched-literal CDCL with VSIDS, phase saving, first-UIP learning,
is checked; unsupported or unsuccessful constructions return              geometric restarts, and RUP logging. Checked SAT assignments are
UNKNOWN, and no UNSAT certificate path is implemented.                    emitted; UNSAT produces an empty RUP contradiction and VeriPB
                                                                          conclusion, while malformed, oversized, proof-output, or model-check
                                                                          failures return UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


sorting-networks                                                    163    st-connectivity-principle                                                 165
23 GBD instances · 5 validation · baseline 1/5                             2 GBD instances · 1 validation · baseline 0/1
These instances ask whether a bounded-depth comparator network             The benchmark asks whether two edge-selected path systems on
can be chosen to sort every encoded Boolean input on its channels.         identical rectangular grids can connect alternating terminal pairs
CNF variables select disjoint comparator pairs in each layer, while        without sharing a vertex. Boolean edge variables and CNF clauses
auxiliary simulation variables and clauses enforce channel use and         enforce local degree or parity rules, plus cross-color clauses forbidding
sorted outputs.                                                            selected edges from meeting at one vertex.
Proof format                             No verif.    + verif.    Solved   Proof format                             No verif.        + verif.      Solved
GRAT                                       1.00 ×     1.00 ×        1/5    GRAT                                       1.00 ×         1.00 ×           0/1
Canonical comparator-block recognition only supplies phase and             Min-fill bucket elimination is the active refutation strategy, using
activity hints for selected layouts, while watched-literal CDCL            literal masks and subsumption pruning while resolving variables and
performs the search with learning, restarts, and clause reduction. SAT     dynamically rebucketing when needed. It emits retained clauses and
assignments are checked against original clauses and printed; UNSAT        the empty clause as textual DRAT for external elaboration, reports
emits learned additions and an empty clause as an external DRAT            UNSAT only on a refutation, and returns UNKNOWN if recognition or
stream, while unsupported inputs return UNKNOWN.                           refutation fails.
DPR                                        1.34 ×     1.34 ×        2/5    DPR                                        1.00 ×         1.00 ×           0/1
Structural conflict/OR recognition admits supported layouts, then          Bounded frontier-ordered Davis-Putnam elimination is attempted first,
hard-coded comparator cores seed selected 13- and 16-channel               using compact masks and subsumption before an in-process
searches before watched-literal CDCL fallback. Fallback SAT                watched-literal CDCL tail handles the residual formula. It logs
assignments are checked against the CNF, while UNSAT emits learned         resolvents and learned clauses, including witness-free additions, and
witness-free DPR/RUP additions and an empty clause; seeded UNSAT           reports UNSAT only after an empty-clause conflict; restrictive
or unsupported input returns UNKNOWN.                                      recognition, width bounds, or complete assignments return
VeriPB                                    2.01 ×      1.99 ×        3/5    UNKNOWN.
Odd blocks use embedded comparator portfolios, occurrence                  VeriPB                                    10.9 ×          6.59 ×           1/1
propagation, and residual DPLL; even blocks use watched-literal            Column-wise transfer maintains a subsumption-minimal boundary
CDCL, with the seven-block fallback also using CDCL. Checked SAT           clause summary, while watched-literal local DPLL searches each
assignments are printed; even-branch UNSAT logs RUP constraints            column and records propagation and branch-resolution clauses as
and an empty clause, while unsupported, even-SAT, or other                 VeriPB RUP steps. The final unassumed search emits UNSAT only on
unsuccessful cases return UNKNOWN; the seven-block fallback has no         conflict; recognition or height limits, and a satisfying search with no
UNSAT proof path.                                                          witness path, return UNKNOWN.

ssp-0                                                               164    station-repacking                                                         166
5 GBD instances · 1 validation · baseline 1/1                              9,842 GBD instances · 1,969 validation · baseline 1673/1969
The benchmark asks whether a subset of integer-weighted items sums         Choose exactly one channel for each station while avoiding
to a fixed target, using Boolean selectors for the choices. A CNF          incompatible pairs of selected station-channel options. A CNF
encoding adds auxiliary variables for arithmetic and a ripple-adder        encoding uses variables for station-channel choices, positive clauses to
circuit constrained to equal that target.                                  require a choice, and negative clauses to forbid multiple choices or
Proof format                             No verif.    + verif.    Solved   conflicting pairs.
GRAT                                     0.319 ×     0.320 ×        0/1    Proof format                             No verif.        + verif.      Solved
It recognizes a rigid ripple-adder layout and uses 64-bit bit-sliced       GRAT                                      0.544 ×        0.556 ×     1313/1969
propagation of singleton selector assignments to reconstruct the           Peeling with guaranteed extensions and station-level TabuCol-style
encoded weights and target. Packed meet-in-the-middle subset-sum           search, including breakout weighting, leads to watched-literal CDCL
search supplies candidates, which are propagated and checked against       with EVSIDS, restarts, and first-UIP learning. SAT candidates are
every CNF clause; failed recognition, search, or validation returns        extended and checked; only CDCL establishes UNSAT, recording
UNKNOWN, with no UNSAT certificate path.                                   learned clauses and deletions in a textual DRAT trace ending in the
DPR                                      0.319 ×     0.320 ×        0/1    empty clause while unsupported inputs return UNKNOWN.
It uses fixed-cardinality meet-in-the-middle search over                   DPR                                      0.615 ×         0.622 ×     1402/1969
complementary selector halves, after recovering weights and the            Randomized min-conflicts search with tabu moves, restarts, and
target from bit-lane evaluations of the ripple-carry circuit. Candidate    bounded residual repair first builds channel assignments using
assignments are expanded and checked against the full CNF;                 compact masks and station ordering, then falls back to watched-literal
unsupported, negative, or candidate-free inputs return UNKNOWN,            CDCL with learning and witness-free DPR/RUP clause additions. Only
and no UNSAT or DPR certificate path is implemented.                       CDCL can establish UNSAT; checked SAT assignments are certificates,
VeriPB                                   0.319 ×     0.320 ×        0/1    while unsupported encodings or failed checks return UNKNOWN.
It uses bit-parallel evaluation of the recognized topological circuit on   VeriPB                                   0.458 ×         0.466 ×     1184/1969
singleton selector assignments to recover weights and target bits. A       Bit-mask propagation with randomized greedy/min-conflicts
low-64-bit meet-in-the-middle filter generates candidates, each            construction and a tabu, adaptive-weighting retry leads to
checked against the complete CNF to reject collisions; unsupported or      component-wise CDCL with watched clauses, first-UIP analysis, and
uncertifiable searches return UNKNOWN, with no UNSAT or VeriPB             nonchronological backtracking. SAT models are independently
certificate path.                                                          checked; CDCL UNSAT results are replayed with RUP steps into a
                                                                           VeriPB certificate, while unsupported inputs or replay failures return
                                                                           UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

stedman-triples                                                       167    subgraph-isomorphism                                                  169
44 GBD instances · 9 validation · baseline 2/9                               194 GBD instances · 39 validation · baseline 12/39
These CNFs ask whether choices of change-ringing calls, orientations,        Subgraph isomorphism asks whether vertices of a pattern can be
and successor states can satisfy all constraints of a lifted Stedman state   injectively assigned to host vertices while preserving edges. CNF
system. The choices use construction variables, one-hot or compact           encodings can represent these choices as one-hot domains or bounded
state variables, and transition variables, with CNF clauses enforcing        bit blocks and add clauses forbidding incompatible pairs.
allowed states and propagated changes.                                       Proof format                             No verif.       + verif.   Solved
Proof format                             No verif.    + verif.     Solved    GRAT                                      1.07 ×        0.924 ×     14/39
GRAT                                     0.861 ×     0.861 ×          1/9    Direct and logarithmic recognition drives finite-domain CSP search
Explicit six-state block recognition leads into watched-literal CDCL         with propagation, MRV branching, and recursive proof search;
with first-UIP learning, activity-guided branching, and                      shortened logarithmic or auxiliary forms use watched-literal CDCL.
phase-randomized restarts. SAT assignments are checked against               Checked SAT assignments are reported; UNSAT branches emit textual
every original clause before printing; UNSAT emits textual DRAT              DRAT traces with learned clauses or tree nogoods, while unsupported
clauses and a terminal empty clause for external GRAT elaboration,           inputs return UNKNOWN.
while unsupported inputs or internal failures return UNKNOWN.                DPR                                      0.846 ×        0.362 ×      7/39
DPR                                      0.889 ×     0.889 ×          1/9    Graph-aware CSP search is distinctive: recognized direct or
Graph-projected search extracts oriented transitions, applies breakout       logarithmic forms with recovered alignment receive matching and
walks and subtour cuts, then seeds exact projected CSP search before         neighborhood filters, while unaligned forms use only propagation.
CDCL; recognized compact or signed layouts go directly to CDCL. It           SAT assignments are validated; UNSAT search emits witness-free DPR
emits checked SAT assignments only; no DPR proof path exists, and            additions, extending logarithmic blocks with one-hot clauses;
unsupported or unsuccessful searches return UNKNOWN rather than              unsupported inputs or proof branches not establishing UNSAT return
certified UNSAT.                                                             UNKNOWN.
VeriPB                                   0.791 ×     0.791 ×          0/9    VeriPB                                   0.878 ×        0.892 ×      8/39
Bounded recognition enables call-first branching in watched-literal          Graph-aware bitset search distinguishes this solver: eligible one-hot
CDCL with first-UIP learning and all-variable fallback; no specialized       inputs use matching filters, min-conflicts, and clique search, while
transition propagator is active. Checked SAT assignments are printed         bit-vector, auxiliary, or failed cases fall back to watched-literal CDCL.
without a completed VeriPB conclusion; UNSAT logs learned clauses            SAT models are checked; bounded one-hot UNSAT cases try
as augmented RUP constraints and writes an UNSAT conclusion                  TreeProof, while other UNSAT cases emit learned-clause RUP
unless proof logging is disabled, while unsupported inputs return            certificates and unsupported inputs return UNKNOWN.
UNKNOWN.
                                                                             subset-cardinality                                                    170
stone                                                                 168    10 GBD instances · 2 validation · baseline 0/2
14 GBD instances · 3 validation · baseline 1/3
                                                                             The benchmark asks whether a shared system of signed exact-two
Stone benchmarks ask whether markers can be placed on a two-parent           constraints can be satisfied. The CNF represents local blocks with
directed acyclic graph, with each marker assigned a red or non-red           complementary NAE-style clauses and adds endpoint constraints that
status. CNF clauses enforce one placement per vertex, red sources, a         impose a boundary parity or counting condition.
non-red sink, and two-parent propagation.
                                                                             Proof format                             No verif.       + verif.   Solved
Proof format                             No verif.    + verif.     Solved    GRAT                                  1.16·105 ×          430 ×       2/2
GRAT                                     1,640 ×      11.2 ×          3/3    On recognized complete inputs, complementary NAE-pair recognition
Source peeling and structural recognition recover mappings and graph         drives the strategy: XOR accumulators and ordered incidence swaps
orientation, accepting only an intact transition set or one canonical        cancel shared block variables, with exhaustive boundary rows closing
omission. A sink-reaching non-red omission yields a checked SAT              a DRAT proof. A weakened block gets a flow-based SAT-model
assignment; otherwise it emits a DRAT-style derivation for external          fallback or modulo-four proof; an unused mod-three routine prevents
checking, while unsupported cases return UNKNOWN without                     the supplied source from compiling.
general SAT search.
                                                                             DPR                                   1.23·105 ×          145 ×       2/2
DPR                                       1,500 ×     8.46 ×          3/3
                                                                             XOR parity cancellation drives complete-instance solving:
Co-occurrence mapping and structural recognition recover phases,             reconstructed exact-two blocks receive witness-free gate definitions
permutations, and the DAG, then identify missing combinations in the         and local lemmas, while incidence swaps eliminate internal variables
sink cone. The first sink-relevant hole yields a checked SAT                 into a boundary contradiction. With one missing NAE half, it tries a
assignment; otherwise it emits a proof ending in the empty clause for        modulo-four proof, then uses enumeration and max flow for SAT;
DPR checking, while unsupported inputs return UNKNOWN without                unsupported or failed cases return UNKNOWN.
general SAT search.
                                                                             VeriPB                               7.19·105 ×      1.06·105 ×       2/2
VeriPB                                     2.18 ×     2.14 ×          2/3
                                                                             For the recognized degree-two layout, incidence-graph reconstruction
Bit-mask recovery of polarity and color mappings, then DAG                   and XOR propagation determine consistent local switching, then a
reconstruction, validates the shuffled three-source encoding and             counting-gap test compares required true literals with available
locates missing tuples. Supported complete instances emit a VeriPB           variables. When the resulting contradiction is found, it emits one
derivation ending in UNSAT; recognized partial instances get checked         pseudo-Boolean cutting-planes proof; unsupported or
SAT assignments, but oversized complete or unsupported inputs and            noncontradictory cases return UNKNOWN, and no SAT-assignment
proof failures return UNKNOWN without SAT search.                            path is implemented.
                                                                                                     Harrison Green, Claire Le Goues, and Fraser Brown


subsumptiontest                                                        171    sum-of-3-cubes                                                         173
19 GBD instances · 4 validation · baseline 4/4                                10 GBD instances · 2 validation · baseline 0/2
The benchmark asks whether a Boolean CNF is satisfiable after clauses         The benchmark asks whether a target integer can be written as the
are repeatedly split into two extensions, adding a variable in both           sum of three signed cubes. CNF instances bit-blast bounded cube
polarities. The resulting clauses may be shuffled, while the family           circuits, using magnitude blocks, sign or selector variables, arithmetic
structure consists of complementary twins rather than an arbitrary            auxiliaries, and fixed target bits.
CNF.                                                                          Proof format                             No verif.     + verif.     Solved
Proof format                             No verif.     + verif.     Solved    GRAT                                 2.00·104 ×       4,320 ×          2/2
GRAT                                       323 ×       20.7 ×          4/4    Integer-construction search is active: the solver recognizes a narrow
A polarity-majority scan proposes a complete model while streaming            bit-blasted circuit shape and seeks bounded signed-cube identities
clauses, with a full recount and rescan as fallback when conflicts            through constructions, residue filtering, and cube-pair search. It
appear. For a narrow one-false-clause case, exact sign-flipped pair           completes and checks each candidate assignment; unsupported inputs
contractions derive opposite units and emit a textual DRAT refutation;        or failed searches return UNKNOWN, with no UNSAT certificate path.
failed recognition, verification, or derivation returns UNKNOWN.              DPR                                        2.00 ×      2.00 ×          1/2
DPR                                        93.6 ×      8.75 ×          4/4    Arithmetic shortcut search is active: a narrow circuit detector extracts
A sign-pattern reduction reverses clause divisions by matching one-bit        three operand words and searches bounded cube identities using
sign differences and repeatedly shrinking the formula to a core.              near-cancellation, modular roots, factorization, and divisors.
Bounded propagation and recursive search can yield a checked SAT              Candidates are completed and clauses checked; rejected or exhausted
assignment; UNSAT requires an explicit empty clause and a derivation          searches return UNKNOWN, with no UNSAT or DPR certificate path.
DAG that may add clauses without witnesses, while unsupported or              VeriPB                                     1.00 ×      1.00 ×          0/2
exhausted cases return UNKNOWN.                                               Modular arithmetic search leads: the solver recognizes a narrow cube
VeriPB                                     237 ×       6.00 ×          4/4    circuit and tests bounded constructions with factorization, roots, CRT,
Polarity-imbalance scanning first proposes a complete assignment and          and discriminant filters. If this fails, DPLL can emit a checked SAT
verifies every original clause. If it fails, width-layered closure of exact   assignment or a VeriPB RUP UNSAT log; unsupported cases return
complementary twins targets the least-imbalanced variable, then               UNKNOWN, without proof verification.
retries globally; a contradiction emits parent-linked VeriPB RUP steps,
while only a fully checked recovered model yields SAT and other cases
                                                                              summle                                                                 174
return UNKNOWN.
                                                                              26 GBD instances · 6 validation · baseline 6/6
                                                                              The benchmark asks whether a bounded read-once arithmetic
sudoku                                                                 172
                                                                              expression can reach a requested target from the multiset 1, 2, 2, 4, 4, 8,
30 GBD instances · 6 validation · baseline 0/6
                                                                              25, 100 using permitted binary operations. CNF bit-blasts operation
The family represents Sudoku-style digit assignments in CNF, using            choices, operands, intermediate values, and target conditions.
variables for cell or related finite-domain choices and clauses for
                                                                              Proof format                             No verif.     + verif.     Solved
Sudoku or other instance constraints. The benchmark question is
                                                                              GRAT                                     0.431 ×      0.436 ×          5/6
whether the resulting Boolean formula has a satisfying assignment;
some encodings include multiple grids and auxiliary variables.                Subset DP, meet-in-the-middle checks, and cached models or
                                                                              witnesses guide expression construction on three layouts while
Proof format                             No verif.     + verif.     Solved    watched-literal CDCL completes or searches the CNF. Satisfying
GRAT                                      1.00 ×       1.00 ×          0/6    assignments are checked against original clauses and emitted as
Watched-literal CDCL with activity-guided branching, 1-UIP learning,          DIMACS models; no independently checkable UNSAT certificate is
non-chronological backtracking, and restarts drives the active search.        produced, so refutations or unsupported inputs return UNKNOWN.
For SAT it prints an assignment; for UNSAT it writes learned-clause
                                                                              DPR                                      1,050 ×        447 ×          6/6
additions and an empty clause as textual DRAT for external GRAT
elaboration and checking, while size, parsing, or proof-output failures       Expression-table lookup and subset dynamic programming build a
return UNKNOWN.                                                               candidate operation sequence whose circuit is forced by unit
                                                                              assumptions before watched-literal CDCL completes remaining
DPR                                       1.00 ×       1.00 ×          0/6    variables. Failed construction invokes generic CDCL with learned
Order-prefix recognition prioritizes the first 17 objects, then uses          clauses logged as witness-free additions for external checking;
activity-based first-UIP CDCL with clause-scanning propagation,               unsupported shapes return UNKNOWN, and direct SAT construction
restarts, and fallback branching. The recognizer checks structure, not        emits no proof stream.
Sudoku semantics; SAT assignments are checked against original
                                                                              VeriPB                                     815 ×       64.8 ×          6/6
clauses, while UNSAT emits learned clauses plus an empty clause as
textual DPR for external elaboration; rejection or parse failure returns      Target extraction from repeated signatures and multiset dynamic
UNKNOWN.                                                                      programming construct a bounded arithmetic witness; forced selector
                                                                              and opcode bits are completed by watched-literal CDCL. Checked SAT
VeriPB                                    1.00 ×       1.00 ×          0/6    assignments are emitted, but exhaustion, conflicts, failed validation, or
The compiled executable is an unconditional UNKNOWN fallback: it              unrecognized layouts return UNKNOWN because no UNSAT or
only checks invocation shape, neither parses the CNF nor searches. An         VeriPB certificate path exists.
exploratory source file contains row, column, and box filtering with
bounded Sudoku backtracking, but it is not compiled or reachable, so
no SAT assignment or UNSAT certificate is emitted.
The Case for Automated Hyperspecialization:
Evidence from SAT

tensors                                                                175    test-configuration                                                     177
40 GBD instances · 8 validation · baseline 2/8                                44 GBD instances · 9 validation · baseline 4/9
The benchmark asks whether a three-way tensor over GF(2) is the               The benchmark asks whether n configurations of 46 options can obey
XOR of at most R rank-one outer products. CNF encodings use AND               fixed incompatibilities and implications while covering every
gates for factor products, XOR constraints for tensor entries, and            compatible option pair. Its CNF has per-row variables and
ordering constraints for interchangeable terms.                               pair-conjunction variables; variants require each pair to be absent
Proof format                             No verif.     + verif.     Solved    from a row or impose lexicographic row ordering.
GRAT                                       2.14 ×      2.14 ×          5/8    Proof format                             No verif.        + verif.   Solved
It searches for rank-one decompositions by choosing shared matrix             GRAT                                  7.81·104 ×           814 ×       9/9
updates that reduce residual slice ranks, with randomized                     Randomized maximum-coverage search over enumerated maximal
diversification and pivot-style fallback. It completes ordering and           cliques seeks a fixed-size row cover, repairs negative-coverage variants
auxiliary variables with dynamic programming and DPLL, checks                 locally, and clause-checks the resulting complete SAT assignment. On
every clause, and emits a SAT assignment; unsupported structure or            smaller recognized instances, an obstruction generator emits ASCII
failed search returns UNKNOWN, with no UNSAT certificate path.                DRAT additions for external elaboration and checking; recognition or
DPR                                       2.15 ×       2.15 ×          5/8    search failure returns UNKNOWN without a general SAT fallback.
It builds a GF(2) slice-space span by choosing minimum-rank residuals         DPR                                   5.05·104 ×           394 ×       9/9
across slicing modes, then factors residual matrices into rank-one            An exact recognizer for a capped fixed layout dispatches to a
terms with binary Gaussian elimination. It reconstructs and orders            compatibility-cover construction, pads and orders rows as needed,
factors, propagates and checks the clauses, and emits a SAT                   evaluates auxiliaries, and checks every clause before returning a SAT
assignment; bounded search failure or unsupported encodings return            assignment. Smaller instances use a hard-coded obstruction and DPR
UNKNOWN, with no UNSAT certificate path.                                      steps with witness-free clause additions; recognition or
VeriPB                                     2.04 ×      2.04 ×          5/8    proof-generation failure returns UNKNOWN without a general
It contracts XOR components into tensor cells, then uses bit-mask             fallback.
tabu/min-conflicts seeding, slice switches, and Gaussian-elimination          VeriPB                               8.25·104 ×          2,080 ×       9/9
rank factoring to construct factors. Comparator completion uses               Arithmetic-layout recognition selects a hard-coded compatibility cover
subset DP and DPLL before a clause-checked SAT assignment; failed             for SAT, pads and orders rows as required, reconstructs auxiliaries, and
construction invokes internal CDCL that can emit an UNSAT RUP                 checks every input clause before releasing the assignment. Smaller
proof for external checking, while unsupported or out-of-regime               recognized instances use fooling-set counting with premise lookup to
encodings return UNKNOWN.                                                     emit VeriPB RUP and cutting-plane proofs; unrecognized inputs or
                                                                              proof-generation failure return UNKNOWN without a SAT fallback.
termination-analysis                                                   176
68 GBD instances · 14 validation · baseline 13/14                             testpattern-generation                                                 178
The benchmark asks whether a Boolean assignment satisfies all                 52 GBD instances · 11 validation · baseline 11/11
clauses encoding termination-ordering constraints. Auxiliary variables        The benchmark asks whether a Boolean assignment satisfies a CNF
may represent circuit gate outputs in a Tseitin-style CNF, while the          encoding of a test-pattern or fault-detection condition. In
implementations recognize only selected layouts, not every possible           circuit-oriented instances, variables represent signals and clauses
encoding.                                                                     impose the relevant constraints, so SAT gives a test pattern and
Proof format                             No verif.     + verif.     Solved    UNSAT rules out one for that encoding.
GRAT                                     0.389 ×      0.373 ×         9/14    Proof format                             No verif.        + verif.   Solved
Bounded randomized local search first targets recognized, short               GRAT                                 2.11·10 −4 ×    5.22·10 −4 ×    10/11
Tseitin-like CNF and accepts only a fully checked model; other                Statistical recognition selects two bounded-width ATPG-miter
accepted inputs undergo propagation, bounded elimination, probing,            signatures without reconstructing topology. Watched-literal CDCL
and watched-literal CDCL. SAT models are clause-checked; UNSAT                uses VSIDS, first-UIP learning, and restarts, falling back to a
uses a textual DRAT log of preprocessing, probing, and learned clauses,       descending scan when the activity heap has no candidate; checked
while unsupported inputs or missing proof output return UNKNOWN.              SAT models are printed, while UNSAT emits DRAT additions and an
DPR                                      0.267 ×      0.316 ×         6/14    empty clause, and unsupported or failed cases return UNKNOWN.
AND/parity DAG reconstruction drives bounded gate repair with                 DPR                                  2.11·10 −4 ×    5.21·10 −4 ×    10/11
phases, random flips, and restarts; large circuits skip repair, and failure   Syntactic envelope recognition accepts only CNF formulas matching
falls back to CDCL, not UNSAT. Inputs outside unit-rich, mostly               bounded-width statistical signatures; it does not recover gates,
binary/ternary shapes return UNKNOWN; SAT models are checked,                 boundaries, or a netlist. Watched-literal CDCL supplies first-UIP
the CDCL fallback is uncapped, and UNSAT proof logs use root                  learning, activity-based branching, and restarts; checked SAT
conflicts and learned, potentially witness-free clause additions.             assignments are printed, while UNSAT produces learned clauses and
VeriPB                                   0.350 ×      0.413 ×         8/14    an empty clause for DRAT elaboration, with other outcomes
Conservative Tseitin recognition and bounded elimination of                   UNKNOWN.
low-occurrence outputs preserve semantic variables before                     VeriPB                                    6.53 ×          1.30 ×     11/11
watched-literal CDCL; recognized one-hot cases receive a bounded              Narrow recognition precedes parity contraction of adjacent
random-walk SAT probe, while unmatched layouts return                         equivalence or inversion pairs and signed clause rewriting.
UNKNOWN. A non-logging scout precedes a fresh VeriPB RUP run                  Watched-literal CDCL uses first-UIP learning and restarts; SAT checks
when needed; checked SAT assignments are accepted, but failed or              a reconstructed assignment, while UNSAT is certified by VeriPB RUP
incomplete UNSAT certification returns UNKNOWN.                               steps for learned and contracted clauses plus an empty conclusion;
                                                                              rejected, inconsistent, or proof-failed cases return UNKNOWN.
                                                                                                  Harrison Green, Claire Le Goues, and Fraser Brown


theorem-proving                                                     179    tree-decomposition                                                   181
8 GBD instances · 2 validation · baseline 2/2                              24 GBD instances · 5 validation · baseline 2/5
These benchmarks encode grid-based pebbling contradictions: they           The benchmark asks whether an undirected graph has an elimination
ask whether local Boolean rules can assign consistent states to grid       ordering of bounded width that obeys precedence constraints.
vertices. Source or root conditions, predecessor implications, and a       Structured CNF variables and clauses encode the graph, ordering, fill
designated sink condition are expressed with small CNF gadgets, often      edges, and width bound, with supported layouts varying by solver.
using two Boolean variables per vertex.                                    Proof format                             No verif.    + verif.     Solved
Proof format                             No verif.    + verif.    Solved   GRAT                                      1.72 ×      1.71 ×         3/5
GRAT                                      33.4 ×     8.85 ×         2/2    Structural recovery and mixed elimination search distinguish this
Support-hash grouping and DSU recovery reconstruct the                     solver: it recognizes only direct or scrambled encodings, combines
paired-variable DAG, validating a unique source, acyclicity, and           randomized min-fill/min-degree and annealing local search, and uses
topological order without checking rectangular dimensions. The             exact DFS on smaller graphs. A found order gets Horn or
recovered order drives DRAT additions for external elaboration,            renamable-Horn completion and clause verification; failures return
including boundary and interior clauses, a sink unit, and the empty        UNKNOWN, with no UNSAT certificate path.
clause; unrecognized inputs return UNKNOWN, with no SAT-model              DPR                                        1.13 ×     1.13 ×         2/5
path.                                                                      Structural recognition and randomized elimination search lead the
DPR                                        14.4 ×    0.474 ×        2/2    solver: it recovers a narrowly supported graph encoding, tries greedy
Exact structural recognition recovers paired variables, predecessor        min-fill/min-degree orders, and uses capped beam search as fallback.
DAG, and grid order from the two-variable OR-substituted rectangular       Successful orders receive residual Horn completion and clause
grid form. It emits witness-free DPR additions for the recovered order,    verification; unsupported or failed cases return UNKNOWN, and no
using head clauses and bridge clauses to derive the sink contradiction;    UNSAT certificate path exists.
unrecognized inputs and failures return UNKNOWN, with no                   VeriPB                                   0.872 ×     0.872 ×         1/5
SAT-search or model path.                                                  Precedence-aware randomized min-fill/min-degree search leads the
VeriPB                                     12.2 ×     2.93 ×        2/2    solver: it recognizes only the canonical layout, tries greedy orders, and
Two-pass counting sort reconstructs variable pairs and four-clause         falls back to heuristic repair stages. Successful orders receive Horn
grid gadgets, then checks dimensions, polarity, clause ownership, and      completion and clause verification before SAT assignment output;
an acyclic root-reachable order. The solver emits a cutting-planes         optional CDCL can generate RUP steps and an UNSAT conclusion,
certificate with one derivation per non-root vertex and a final sink       while normal failure returns UNKNOWN.
contradiction, while malformed or unrecognized inputs return
UNKNOWN and no SAT-solving fallback is implemented.                        trigonometric-functions                                              182
                                                                           6 GBD instances · 2 validation · baseline 1/2
tournament                                                          180    These instances ask whether Boolean assignments to input and
16 GBD instances · 4 validation · baseline 0/4                             internal variables can satisfy every clause in a circuit encoding of a
These instances ask whether a partially fixed tournament can be            trigonometric computation or relation. The benchmarks use
completed so every seven-vertex subset contains a cyclic triangle, not     gate-based bit-vector or Tseitin CNFs, while recognizers accept only
a transitive ordering. The CNF uses edge orientations and triangle         restricted structural layouts.
witnesses, with clauses linking witnesses to edges and requiring each      Proof format                             No verif.    + verif.     Solved
seven-set to be covered.                                                   GRAT                                       1.01 ×     1.07 ×         1/2
Proof format                             No verif.    + verif.    Solved   Structural case splitting canonicalizes small functional gate groups in
GRAT                                      1.00 ×     1.00 ×         0/4    the piecewise-lines layout, deriving constant and equivalence clauses
Score-based local search is the active technique: it flips free edge       before watched-literal CDCL; Taylor-layout instances skip this
orientations while incrementally tracking transitive seven-sets, using     preprocessing. UNSAT branches log DRAT clause additions, while
tabu moves, dynamic weights, focused randomness, and restarts. The         checked SAT models are returned and unsupported inputs or a
narrow encoding is checked before search; found assignments are            configured conflict cutoff yield UNKNOWN.
clause-checked, unsupported inputs return UNKNOWN, and the                 DPR                                       2.34 ×      2.10 ×         2/2
SAT-only path has no UNSAT certificate or exhaustion result.               Implication-graph equivalence substitution and blocked-clause
DPR                                       1.00 ×     1.00 ×         0/4    elimination simplify recognized gate-heavy CNFs, with bounded
Restricted tournament blow-up construction is tried first, duplicating     variable elimination attempted only on larger accepted instances.
core vertices under capacity constraints and rejecting remaining           First-UIP learning logs RUP clauses and a terminal empty clause for
transitive seven-sets. Only recognized encodings can yield checked         UNSAT; checked SAT assignments are returned, while unsupported
SAT assignments; unsupported inputs return UNKNOWN, and no                 inputs or failed checks yield UNKNOWN.
UNSAT derivation or exhaustion result is implemented.                      VeriPB                                   0.953 ×     0.596 ×         1/2
VeriPB                                    1.00 ×     1.00 ×         0/4    A conservative topology heuristic identifies likely source variables and
Stochastic min-conflict edge-flip search is active, maintaining selector   prefers them on activity ties, but all accepted CNFs use watched-literal,
values and seven-set violation counts while sampling unsatisfied sets      first-UIP CDCL search; no circuit-specific propagator or dispatch is
and applying scored flips, noise, and restarts. A specialized              active. UNSAT produces VeriPB RUP records, an empty-clause RUP,
prefix-completion branch checks constrained six-set-free extensions;       and an UNSAT conclusion, while checked SAT models are returned;
found SAT models are checked, unsupported encodings return                 malformed input or failed checks yields UNKNOWN.
UNKNOWN, and no active UNSAT certificate path exists.
The Case for Automated Hyperspecialization:
Evidence from SAT

tseitin-formulas                                                         183    unknown                                                            185
197 GBD instances · 68 validation · baseline 51/68                              118 GBD instances · 24 validation · baseline 12/24
These benchmarks ask whether a CNF encoding of XOR constraints                  These benchmarks ask whether Boolean variables can satisfy a
has a Boolean assignment satisfying every clause. A common                      structured encoding of a finite combinatorial construction. Clauses
encoding groups clauses that forbid one parity of variables, with               represent choices and enforce exact-one, uniqueness, incidence,
graph-shaped cases representing variables as edges between constraint           adjacency, forbidden-combination, or auxiliary-consistency conditions.
vertices and vertex charges as parity requirements.                             Proof format                             No verif.    + verif.   Solved
Proof format                             No verif.         + verif.    Solved   GRAT                                     0.609 ×     0.611 ×      3/24
GRAT                                      3.04 ×           2.77 ×       62/68   Bit-mask recognition and bounded Dancing Links search target
Exact parity-block recognition drives graph charge-parity and                   orthogonal Latin-square encodings; fixed balanced-design and
spanning-forest solving, with bounded packed GF(2) elimination for              bit-vector Latin constructions seed CDCL, with CDCL handling other
non-graph systems and a narrow repair for selected quadratic                    inputs. SAT assignments are rechecked, and UNSAT paths log derived
encodings. Checked SAT assignments are reconstructed from                       clauses and an empty clause for external DRAT elaboration; failed
recovered equations; selected graph contradictions receive attempted            direct orthogonal-Latin searches or budget exhaustion return
DRAT/extended-resolution proofs, while unsupported, oversized, or               UNKNOWN.
unproved cases, including dense inconsistencies, return UNKNOWN.                DPR                                      0.933 ×     0.856 ×     11/24
DPR                                      0.506 ×          0.513 ×       32/68   Bounded structural recognizers try cyclic-isotopy and Dancing Links
Complete parity-block decoding drives GF(2) solving: graph systems              for direct orthogonal-Latin encodings, residue or TabuCol searches for
use spanning forests, with bounded elimination and narrow repaired              five-colorings, and component CSP searches for signed-selector cases.
or quadratic-macro fallbacks. SAT assignments are clause-checked;               Failures fall through to CDCL with failed-literal probing; SAT models
supported UNSAT cases use graph or macro contractions to emit                   are checked against input, while UNSAT logging yields textual DPR
witness-free DPR clause additions, while rejected proof plans or failed         and proof or model-check failures return UNKNOWN.
stochastic searches return UNKNOWN, never establishing UNSAT.                   VeriPB                                   0.888 ×     0.696 ×     10/24
VeriPB                                    6.07 ×          4.45 ×        65/68   Choice-block recognition uses rare-polarity orientations, bitsets,
ANF/Mobius recovery yields XOR equations over signed variables or               singleton rules, MRV branching, and bounded DFS; narrow Latin
two-literal terms; graph components use charge propagation and tree             search tries affine constructions before MRV. Failed attempts fall back
reconstruction, while dense elimination produces SAT models only.               to CDCL; SAT models are checked, pigeonhole cases emit direct PB
Clause-checked models are reconstructed physically; graph                       proofs, while CDCL UNSAT traces end in RUP contradiction and
contradictions can receive VeriPB proofs, while a bounded clique                proof-generation failures return UNKNOWN.
fallback emits cutting-planes proofs and non-graph inconsistencies
return UNKNOWN without UNSAT certification.
                                                                                unknown-cases                                                      186
                                                                                20 GBD instances · 4 validation · baseline 4/4
uniform-random                                                            184
                                                                                The benchmark asks whether a Boolean assignment satisfies every
4,043 GBD instances · 809 validation · baseline 201/809
                                                                                clause of a CNF formula. Structured instances may encode selections
The benchmark asks whether a Boolean assignment can satisfy every               that cover requirements while forbidding combinations, or represent
clause in a signed-literal CNF formula. Inputs are restricted                   circuits and order constraints; these are recurring structures, not a
random-width-shaped DIMACS formulas with controlled clause                      universal encoding.
widths and related structural checks, which describe the encoding
                                                                                Proof format                             No verif.    + verif.   Solved
rather than establish statistical uniformity.
                                                                                GRAT                                     0.131 ×     0.131 ×       1/4
Proof format                             No verif.         + verif.    Solved   Four-incidence positive-cover recognition leads the search, followed
GRAT                                      1.28 ×          1.27 ×      332/809   by orientation, bounded graph/circuit and stochastic model attempts,
Pure 2-CNF instances use an SCC contradiction-path procedure; other             all accepted only after checking a full CNF assignment. When CDCL
accepted width classes first receive belief- or                                 proves UNSAT, it logs learned clauses and a final empty clause for
survey-propagation-seeded incremental local search with make/break              external checking; failed structural or internal searches do not
and age-aware choices. On failure, watched-literal 1-UIP CDCL                   establish UNSAT and can return UNKNOWN.
continues to a checked model or conflict, logging textual DRAT clauses
                                                                                DPR                                      0.106 ×     0.106 ×       0/4
for UNSAT; malformed or out-of-scope inputs return UNKNOWN.
                                                                                Polarity-normalized cover recognition leads to bitset propagation,
DPR                                       1.09 ×           1.09 ×     241/809   randomized repair, local search, and minimum-coverage DFS, with
Focused incremental local search uses clause-satisfaction state,                fixed-layout circuit and repeated-key paths as bounded fallbacks. SAT
break/make scores, and width-dependent probSAT- or Novelty-style                candidates are checked against the original CNF; only monotone DFS
choices. Only narrow complete-route instances enter watched-literal             within its 64-variable limit emits decision nogoods and may report
first-UIP CDCL; it can print a checked model or log witness-free DPR            UNSAT, while other failures or large-cover exhaustion return
additions for UNSAT, while other local-search misses and out-of-scope           UNKNOWN.
inputs return UNKNOWN.
                                                                                VeriPB                                   0.106 ×     0.106 ×       0/4
VeriPB                                    1.09 ×           1.08 ×     241/809   Monotone cover/forbidden-set search uses bitset filtering and
Incremental probSAT-style local search maintains make/break,                    smallest-uncovered branching, with local search and watched-literal
unsatisfied-clause, and sole-satisfier state, with weighted and                 CDCL fallbacks, accepting only clause-checked assignments. The
deterministic seed strategies. A watched-literal CDCL fallback is               complete monotone and CDCL paths replay learned or
available only for bounded instances; it can yield a checked SAT                decision-nogood clauses as RUP steps with a final empty constraint;
assignment or log RUP proof steps for UNSAT, while larger or failed             heuristic failures provide no proof, and unsupported or exhausted
searches can end UNKNOWN without an UNSAT certificate.                          cases return UNKNOWN.
                                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


waerden                                                               187    xor_op                                                              189
110 GBD instances · 22 validation · baseline 3/22                            3 GBD instances · 1 validation · baseline 1/1

The benchmark asks whether positions 1 through N can be                      The benchmark asks whether a directed relation on vertices can be a
two-coloured so one colour avoids every three-term arithmetic                strict ordering: it is asymmetric and transitive, yet every vertex must
progression and hits every K-term progression. Boolean variables             have a predecessor among three designated choices. CNF uses two
encode these conditions as positive and negative CNF clauses; some           XOR-related variables per relation atom and expands the logical
instances use folded representations.                                        constraints into clauses.
Proof format                             No verif.     + verif.     Solved   Proof format                             No verif.    + verif.    Solved
GRAT                                      1.04 ×      1.04 ×         4/22    GRAT                                      8,210 ×     375 ×          1/1
Bounded weighted local search first seeks a checked SAT assignment           Exact width-2 XOR decoding with fallbacks builds an
when a positive rank-2 clause exists, then complete DFS blocks               embedded-gadget proof: it names atoms, derives ordering clauses, and
positive edges and branches on the tightest unhit negative edge. Proof       greedily eliminates vertices to an empty clause. It has no SAT fallback:
logging records parent, leaf, exclusion, and deletion clauses for            only recognized three-predecessor schemas are handled, unsupported
external elaboration; restricted pure-polarity shapes or proof               inputs or failures return UNKNOWN, and DRAT is sent for external
inconsistencies can yield UNKNOWN.                                           elaboration and checking.
DPR                                       1.01 ×       1.02 ×        3/22    DPR                                   2.34·104 ×      128 ×          1/1
Incremental weighted local search leads the SAT attempt, using               Greedy elimination over predecessor bitsets replaces each removed
breakout weights, flip scores, and age tie-breaking. Failure falls back to   predecessor by its predecessors, emits canonicalization additions for
complete DFS with negative-clause branching; unsupported structure           used XOR gadgets, and ends with an empty clause when successful.
yields UNKNOWN, while checked SAT assignments are returned and               Recognition covers only the exact bounded three-predecessor macro
DFS may log witness-free conflict clauses without an implemented             layout; no general SAT or SAT-witness path exists, and unsupported or
UNSAT certification.                                                         failed constructions return UNKNOWN.
VeriPB                                   0.944 ×     0.912 ×         2/22    VeriPB                                    1,660 ×     121 ×          1/1
Two-watched-literal CDCL is the active engine, using activity-based          XOR-block recovery followed by in-process CDCL searches the
branching, 1-UIP conflict minimization, restarts, failed-literal probing,    recovered logical clauses rather than the expanded raw formula. On
and learned-clause reduction. It checks SAT assignments, returns             UNSAT it writes a VeriPB proof with XOR reductions and RUP steps,
UNKNOWN for unsupported structure, and on UNSAT attempts to                  but does not invoke a verifier; recognition mismatches, satisfiable
serialize learned clauses, deletions, and a final contradiction as VeriPB    outcomes, or proof failures return UNKNOWN.
proof text, without invoking a proof verifier.

xor-chain                                                             188
66 GBD instances · 14 validation · baseline 11/14
These instances ask whether a Boolean assignment satisfies a
connected system of parity equations. A typical CNF encoding uses
four clauses for each three-variable XOR and two for each two-variable
XOR; related instances use sequential counters and graph constraints.
Proof format                             No verif.     + verif.     Solved
GRAT                                      1.00 ×       1.00 ×       11/14
XOR-gate recognition and Gaussian elimination handle supported
parity systems; persistent XOR-tree logging, fresh definitions, and
RUP/resolution projections support UNSAT. On recognition failure, a
triangle-graph fallback uses blossom matching and sequential counters
for clause-checked SAT models; strengthened forms skip this path, and
unsupported or failed dispatch returns UNKNOWN.
DPR                                       1.00 ×       1.00 ×       11/14
Degree-two incidence-graph recognition selects only supported,
clause-complete binary and ternary parity groups in a connected
structure. Bit-packed GF(2) elimination yields SAT assignments
checked against every original clause, while UNSAT uses
spanning-tree XOR expressions, fresh definitions, chord cancellation,
and local RUP derivations; unsupported or failed cases return
UNKNOWN.
VeriPB                                    3.00 ×      2.99 ×        13/14
Direct XOR recognition uses BFS cycle reductions for parity instances,
clause-checking SAT assignments and emitting VeriPB derivations for
UNSAT contradictions; strengthened forms have only the latter path
and may return UNKNOWN. Counter variants reconstruct triangles
and use blossom matching for SAT or pseudo-Boolean proofs for
conflicting bounds; matching failure or unsupported cases return
UNKNOWN.
The Case for Automated Hyperspecialization:
Evidence from SAT

K     Extended: Solver taxonomy                                   learned clauses during search. Watched literals, activity
We used GPT-6 Astra (xhigh) and GPT-5.6 Luna (high) to            scores, or proof logging alone do not qualify.
iteratively generate and refine a taxonomy for seven dif-         Greedy construction. An assignment or domain solution
ferent questions about solver behavior. Here we describe          is built progressively without systematic backtracking or
our methodology and potential limitations (§K.1). We then         iterative local repair. Trivial fixed-phase candidates qualify
present the full taxonomy (§K.3).                                 only when actually tested as answer attempts.
                                                                  Exhaustive enumeration. Assignments or combinations
K.1    Methodology                                                are explicitly enumerated and checked, possibly in parallel
Given a query about a specific aspect of solver behavior, such    using machine-word bits. Ordinary CDCL branching is not
as “What solving strategies are used in the solvers?”, we first   counted as a separate enumeration algorithm.
built out a suitable taxonomy using GPT-6 Astra (xhigh) in        Native-domain local search. Neighborhood moves repair
Codex, providing the full suite of 567 generated solvers and      recovered domain objects, such as changing a color or swap-
their source code. We iteratively refined the taxonomy to         ping permutation entries. The moves act on these objects
ensure it covered all variation and properly distinguished        beyond individual CNF variable flips.
between closely related concepts (both LLM-mediated and           Constraint backtracking. Search assigns recovered finite-
with some human feedback).                                        domain variables or domain objects, such as colors or permu-
   Given a frozen taxonomy, we then tasked GPT-5.6 Luna           tations, and backtracks with constraint filtering. The search
(high) with annotating each solver independently for each         operates on domain constraints beyond ordinary Boolean
query and set of labels. We report results for all non-zero       DPLL.
counts. A given solver only contributes once to a given la-
                                                                  Circuit / equivalence reasoning. Recovered gate seman-
bel (even if it implements several variants) but each solver
                                                                  tics, circuit simulation, equivalence reasoning, or circuit
can contribute to multiple labels. The full listing of frozen
                                                                  rewriting solve or reduce the problem. Identifying gates only
taxonomies is provided in §K.3.
                                                                  to choose variable phases is insufficient.
K.2    Potential limitations                                      Cardinality / PB reasoning. Dedicated counting or bound
                                                                  propagation, cutting-plane deductions, or counting contra-
LLMs are fallible and our taxonomies may be incomplete
                                                                  dictions reason beyond ordinary CNF propagation. Merely
or inaccurate. For the use of these taxonomies in our paper
                                                                  printing a VeriPB certificate is insufficient.
(observing broad variation patterns) we believe this is an
acceptable risk. The exact counts of solvers for each label       WalkSAT-style search. Search selects an unsatisfied clause,
and the specific techniques listed, if changed slightly, would    then flips one of its variables using low-break scores or
not alter the conclusions we draw.                                noisy/random choices. An occasional random step within a
                                                                  different algorithm is insufficient.
K.3    Full taxonomy labels                                       Other graph algorithms. A dedicated graph procedure,
                                                                  such as reachability, bipartiteness testing, or isomorphism
    Æ Note that the content in this section is LLM-               reasoning, decides or constrains feasibility. Graph storage
    generated. These full taxonomy labels were gener-             and ordering alone are insufficient.
    ated with GPT-6 Astra (xhigh) with some human                 DPLL (no clause learning). Davis-Putnam-Logemann-
    feedback.                                                     Loveland search branches on Boolean variables, propagates
                                                                  consequences, and backtracks without learning conflict
K.3.1 Solving strategies. Whole solving procedures, in-           clauses. A CDCL implementation alone does not receive this
cluding systematic search, local search, algebraic and struc-     additional label.
tural reasoning, inference, and direct answer construction.       Weighted local search. Search adapts clause or constraint
The algorithm audit counts default-reachable solving roles,       penalties to redirect subsequent local moves. Static weights
excluding procedures used only for preprocessing or proof         and ordinary break counts alone are insufficient.
processing. Such procedures can still qualify in the other        Arithmetic / number theory. Arithmetic reasoning, factor-
studies. For a local-search flip, make counts clauses newly       ing, modular algebra, or integer-feasibility reasoning directly
satisfied, and break counts clauses made unsatisfied.             constructs an answer or proves impossibility. Parsing nu-
Structural construction / theorem. Recognized instance            meric features alone is excluded.
structure supports a witness construction or a combinatorial      Propagation-only solving. A distinct answer procedure
contradiction, such as a pigeonhole or counting argument.         propagates consequences to a fixed point and completes
The method must perform actual input-dependent reasoning.         an assignment deterministically without branching search.
CDCL. Conflict-driven clause learning combines Boolean            Propagation used only inside another solving algorithm is
decisions and propagation with conflict analysis, then reuses     excluded.
                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


ProbSAT-style search. Candidate flips are sampled with            guide branching. Failed-literal probing used only in prepro-
explicit nonuniform probabilities derived from make/break         cessing is excluded.
scores, such as inverse powers of break counts. Uniform           Belief / survey propagation. The solver iteratively ex-
random noise alone is excluded.                                   changes probabilistic messages on a factor graph, potentially
Tabu search / TabuSAT. A tabu list or tenure explicitly pro-      fixing variables according to the resulting beliefs or surveys.
hibits certain moves, potentially allowing exceptions when
                                                                  Input-feature answer rule. Names, hashes, sizes, or other
a move is sufficiently promising. Age-based tie-breaking or
                                                                  input signatures select a prescribed answer or candidate
a preference against recent flips alone is insufficient.
                                                                  without a demonstrated general structural derivation. This
XOR / GF(2) elimination. Parity equations are solved or re-       records the decision mechanism without judging its correct-
duced through row operations or Gaussian elimination over         ness.
GF(2), the two-element field with arithmetic modulo two.
                                                                  GSAT-style greedy flips. Improving variable flips are cho-
Recognizing exclusive-or (XOR) gates without elimination
                                                                  sen using make/break scores over all variables or a main-
is insufficient.
                                                                  tained set of promising variables. Selection only within one
State-space search. Search traverses explicit domain states,      unsatisfied clause is insufficient.
using methods such as breadth-first or depth-first search,
iterative deepening, heuristic search, bidirectional search, or   Independent random sampling. The solver generates and
beam search.                                                      checks fresh, independent complete candidates. This is dis-
                                                                  tinct from neighborhood search and restarts of that search.
Matching / flow. A recovered graph is solved using match-
ing, augmenting paths, maximum flow, or a Hall witness: a         2-SAT / implication solving. A dedicated procedure de-
set with too few neighbors to support the required matching.      cides 2-SAT, whose clauses have at most two literals, using
                                                                  strongly connected components of an implication graph or
Resolution / elimination. The solver explicitly generates
                                                                  an equivalent method. Binary-clause propagation alone is
resolvents, eliminates variables, or repeatedly applies res-
                                                                  excluded.
olution toward saturation. Conflict-clause learning within
CDCL alone does not receive this additional label.                Horn / tractable fragments. A dedicated algorithm solves
Meet-in-the-middle search. Search enumerates two partial          a recognized tractable fragment, such as Horn formulas (at
solution spaces and joins compatible halves using a table,        most one positive literal per clause) or dual-Horn formulas
hashing, or sorting. Looking up a stored complete answer is       (at most one negative literal). Ordinary unit propagation
excluded.                                                         alone is insufficient.
Dynamic programming. A recurrence combines and                    Novelty-style search. Search selects between the best and
caches subproblem results, for example over subsets, trees,       second-best candidates using avoidance of the most recently
or paths. Maintaining an ordinary assignment trail is insuffi-    flipped variable and a noise rule. Generic age-based tie-
cient.                                                            breaking alone is excluded.
Simulated annealing. Search accepts worsening moves               Local search (unspecified). Candidate assignments are re-
according to a temperature-dependent rule. Merely changing        peatedly repaired through neighborhood moves. This resid-
a random-noise rate over time is insufficient.                    ual category applies only when no more specific local-search
Stored witness / proof / answer. A reachable answer route         label fits the component.
loads, embeds, or retrieves a precomputed assignment, proof,      Population / evolutionary. Search maintains and evolves
or answer. Runtime memoization and newly derived wit-             multiple candidates through selection, mutation, crossover,
nesses are excluded.                                              or other population-based optimization. Repeated indepen-
Branch and bound. Search computes objective bounds and            dent starts alone are excluded.
uses them to prune subproblems that cannot improve the            Decision diagrams / compilation. The solver builds or
result. Feasibility backtracking without such bounds is ex-       manipulates a compiled Boolean representation, such as a bi-
cluded.                                                           nary decision diagram or zero-suppressed decision diagram,
Large-neighborhood search. Search relaxes or removes a            to decide satisfiability or construct a solution.
substantial part of a candidate assignment and reoptimizes        Continuous optimization. The solver optimizes a real-
the resulting neighborhood, often with an exact subsolver.        valued relaxation using gradients or continuous dynamics,
Other algorithm. The source implements a concrete algo-           then decodes Boolean assignments from the result.
rithm outside the named categories. The audit must give its       Configuration-checking search. A variable becomes eli-
precise name and explain the missing taxonomy category.           gible to flip again when a neighboring variable or constraint
Look-ahead SAT search. Tentative assignments and propa-           configuration changes. Timestamps alone do not establish
gation repeatedly estimate the consequences of choices and        this mechanism.
The Case for Automated Hyperspecialization:
Evidence from SAT

External engine, algorithm opaque. The solver invokes              Buffered proof output. Proof bytes or lines are explicitly
an external solving engine whose algorithm cannot be estab-        batched, or a larger output buffer is installed, to reduce out-
lished from the supplied implementation. A known engine            put calls. Ordinary proof logging alone is excluded.
name alone does not establish CDCL, and proof checkers are         Bit-count / scan intrinsics. Reachable computation uses
excluded.                                                          dedicated bit-counting, bit-scanning, or rotation intrinsics
LP / MIP optimization. An explicit linear-programming              or equivalent standard functions. Plain bitwise AND or XOR
or mixed-integer-programming solver or relaxation uses op-         alone is insufficient.
timization machinery. Native Boolean branching alone is            Reduced proof-output work. A concrete mechanism
insufficient.                                                      reuses serialized proof fragments, suppresses redundant
Pure random walk. A distinct search repeatedly makes               emitted steps, or avoids repeated serialization. A mathemati-
unguided or clause-focused random variable flips. Random           cally short proof alone does not qualify.
steps within a scored, noisy WalkSAT procedure alone do
                                                                   Specialized hot loops. Manual unrolling or dedicated fixed-
not receive this additional label.
                                                                   size or short-clause kernels specialize a recurring computa-
SMT / theory solving. Satisfiability modulo theories com-          tion. A constant loop bound or an inline annotation alone is
bines Boolean reasoning with a theory-specific decision pro-       insufficient.
cedure. Arithmetic preprocessing alone is excluded.
                                                                   Lookup tables. Precomputed operation or transition tables
K.3.2 Systems-level optimizations. Concrete mecha-                 replace recurring computation, for example with truth tables
nisms in input/output, CPU execution, memory management,           or byte population-count tables. Stored complete witnesses
incremental work, and parallelism. Conventional implemen-          and ordinary search memoization are excluded.
tations can qualify; novelty and measured benefit are not          Memory-mapped input. The solver maps the input file into
requirements.                                                      memory and accesses it through that mapping. An unused
Compiler / ISA flags. The default build explicitly requests        mapping wrapper or header alone is insufficient.
compiler optimization, instruction-set features, link-time op-     Branchless updates. Explicit masks, arithmetic, or table
timization, or related tuning. Such flags alone do not establish   lookups replace conditional selection in a recurring com-
vectorized execution or a measured speedup.                        putation. A conditional expression alone does not establish
Preallocation / reuse. Capacity reservation, scratch buffers,      branchless execution.
free lists, pools, or arenas reduce repeated memory allocation.    OS memory hints. Explicit operating-system advice re-
Ordinary container construction alone is excluded.                 quests access-pattern, paging, or read-ahead behavior. Mem-
Incremental state updates. Derived quantities, such                ory mapping alone is excluded; these hints are distinct from
as clause counts, move scores, or circuit values, are up-          CPU prefetch instructions.
dated from local changes instead of recomputed globally.
                                                                   Compact proof encoding. Proof records use an imple-
Assignment-trail writes alone are excluded.
                                                                   mented compact serialization, such as binary records,
Flat / compact storage. Flat arenas, offsets, packed records,      variable-length integers, deltas, or compression. A proof-
separate arrays for record fields, or compressed adjacency         format name or ordinary text formatting alone is insufficient.
organize data more compactly than fragmented or pointer-
                                                                   Alignment / cache blocking. Explicit alignment, padding,
heavy storage. An ordinary array alone is insufficient.
                                                                   tiling, or blocking organizes data or computation for locality.
Watched / blocking literals. Watched literals, cached sat-
                                                                   Contiguous storage alone is insufficient.
isfying literals, binary implication paths, or occurrence lists
restrict propagation to potentially affected clauses instead       Explicit SIMD. Packed vector operations execute through
of scanning every clause.                                          intrinsics, vector types, assembly, or a SIMD-specific library,
                                                                   such as SSE, AVX2, AVX-512, or NEON. Compiler flags and
Specialized parsing. A custom byte or integer parser, bulk
                                                                   scalar bitsets alone are excluded.
buffering, or explicit fast-I/O configuration avoids formatted
input overhead. Ordinary token splitting, formatted scan-          Branch-prediction hints. Explicit likelihood annotations
ning, or stream extraction alone is excluded.                      or profile hints tell the compiler which branch outcome is
Scalar word parallelism. Multiple logical values are packed        expected. Ordinary conditional statements do not qualify.
into scalar machine words or bitsets and processed together        CPU software prefetch. The solver issues a software
using bitwise operations. Ordinary scalar flags and random-        prefetch intrinsic or instruction for future memory ac-
number arithmetic are excluded.                                    cesses. Ordinary loads, buffering, capacity reservation, and
Lazy / deferred work. Generation stamps, lazy invalidation,        operating-system advice are separate.
deferred deletion or compaction, or delayed recomputation          GPU / accelerator kernels. A reachable route launches
avoid recurring bulk work. Simply omitting cleanup is insuf-       computation on a GPU or another accelerator. Headers, build
ficient.                                                           support, and unused code alone are excluded.
                                                                                    Harrison Green, Claire Le Goues, and Fraser Brown


Worker processes. Multiple solver-worker processes exe-           Domain filtering. Explicit finite domains or their supported
cute concurrently. A single subprocess, an execution wrapper,     values are pruned using domain-consistency reasoning be-
or process-cleanup code alone is insufficient.                    fore search starts or resumes. Ordinary Boolean unit propa-
Worker threads. A reachable route starts concurrent               gation alone is excluded.
threads or a parallel region for solver computation. Thread-      Failed-literal probing. Tentative literal assignments and
library dependencies and sequential restarts alone are            propagation derive forced values or other simplifications.
excluded.                                                         Probing used only to score the next branching decision be-
                                                                  longs to search tuning.
                                                                  Cardinality / PB reduction. Recovered counting or pseudo-
K.3.3 Preprocessing and inprocessing. Transforma-                 Boolean constraints are simplified through bound reason-
tions of a remaining problem before search or while search is     ing, forced values, compression, or rewriting before further
in progress. Before only and During only indicate exclusive       search. A direct counting refutation or the proof format alone
observed stages; Before + during means both occur in the          is excluded.
same solver. Stage unclear denotes unresolved timing. Ordi-       XOR / algebraic reduction. Parity or algebraic equations
nary per-decision propagation and general conflict learning       are eliminated or substituted to reduce a problem passed
alone are excluded.                                               to further solving. A complete Gaussian solver without a
Root unit simplification. Root-level unit propagation fixes       residual reduction role is excluded.
forced assignments and removes satisfied clauses or liter-        Literal substitution. Equivalent or complementary literals
als to simplify the residual problem before search starts or      are merged and substituted to rewrite the residual problem,
resumes. Ordinary propagation after each decision alone is        for example using implication-graph components. Detecting
excluded.                                                         an equivalence only to solve directly is excluded.
Clause cleanup. Duplicate literals, tautologies, or duplicate     Problem decomposition. The original instance is parti-
clauses are removed, including normalization that enables         tioned into independent or explicitly coordinated smaller
these reductions. Sorting only to recognize structure is ex-      subproblems for separate solving. Ordinary branches of one
cluded.                                                           search do not qualify.
Cone / core reduction. A relevant cone, core, or proper           Variable compaction. Active residual variables or literals
subset is extracted and solved or transformed, with a mecha-      are renumbered to shrink solver data structures after or
nism transferring the result to the original problem. Merely      during reduction. Relabeling only for recognition or input
ignoring clauses is insufficient.                                 permutation is excluded.
Structural strengthening. Implied constraints derived             Symmetry breaking. Canonical restrictions remove equiv-
from recovered structure strengthen a residual problem,           alent assignments, or a verified symmetry rewrites the prob-
for example equivalences between duplicate gates or order-        lem, reducing the remaining search space. Recognizing a
relation closure. Ordinary conflict learning alone is excluded.   symmetric family alone is insufficient.
                                                                  Pure-literal elimination. A variable occurring with only
Other preprocessing. A concrete transformation of the             one polarity is assigned or eliminated in a satisfiability-
remaining problem falls outside the named categories. The         preserving simplification. Merely preferring that polarity
annotation must identify the transformation and explain the       during search is excluded.
taxonomy gap; ordinary search machinery is excluded.
                                                                  Clause subsumption. A clause is removed because another
Resolution elimination. A variable is removed by resolv-          clause contains a subset of its literals. Removing only dupli-
ing clauses containing its positive and negative literals and     cate clauses belongs to clause cleanup.
retaining a satisfiability-equivalent residual problem, possi-    Clause vivification. Sequential literal assumptions and
bly subject to growth limits. Branching and Gaussian elimi-       propagation establish that a clause can be shortened or is re-
nation are separate.                                              dundant. Generic failed-literal probing without clause shrink-
Self-subsuming resolution. Resolution produces a clause           ing is separate.
that subsumes a parent and therefore shortens it. Ordi-           Blocked-clause elimination. A clause is removed when
nary subsumption and general conflict learning alone are          some literal blocks it: every resolvent on that literal is tau-
excluded; qualifying resolution-based learned-clause mini-        tological. Explicit generalized blocked or set-blocked rules
mization may overlap with the search-tuning category.             also qualify.
Gate / circuit reduction. Recovered gates are constant-           Implication reduction. Implied binary edges or clauses are
folded, substituted, rewritten, or functionally eliminated to     removed by transitive reduction or another demonstrated
reduce a residual search problem. Recognition or standalone       redundancy test. Building an implication graph alone is in-
circuit simulation alone is insufficient.                         sufficient.
The Case for Automated Hyperspecialization:
Evidence from SAT

K.3.4 Search tuning. Policies controlling decisions, learn-          Noisy move selection. Local moves use explicit noise or
ing, restarts, local moves, diversification, and effort. The cat-    a nonuniform probability rule, as in WalkSAT or ProbSAT.
egories describe choices within search, rather than naming           Randomized branching in complete search is separate.
whole solving algorithms.                                            LBD / glue quality. The number of distinct decision levels
Static / occurrence ordering. An explicit fixed variable             represented in a learned clause, called literal-block distance
or value order, occurrence score, or polarity count guides           (LBD) or glue, is computed and used to manage clauses or
decisions. Ordinary container iteration without a decision           control search.
policy is excluded.                                                  Look-ahead branch scoring. Tentative assignments, prop-
Scheduled restarts. A search restarts after a fixed budget           agation, or predicted downstream reductions score the next
or according to a predetermined schedule, such as Luby or            branching decision. Probing solely to derive forced literals
geometric intervals. Switching to a different algorithm alone        is preprocessing.
is separate.                                                         Stagnation control. Detected lack of progress changes
Input-dependent parameters. Input features determine                 search behavior, perturbs a candidate, or stops an attempt.
search budgets, thresholds, heuristic parameters, or modes.          A fixed stopping budget alone is insufficient.
Dispatch between unrelated algorithms without tuning a               Tabu / recency rules. Tabu tenure, move age, youngest-
search is separate.                                                  variable avoidance, or configuration eligibility constrain or
Bounded search effort. An individual search attempt has              prioritize moves. This broad category does not imply that
an explicit step, conflict, flip, node, or time limit. The experi-   every annotated solver implements TabuSAT.
ment’s overall timeout alone is excluded.                            Adaptive constraint weights. Penalties on clauses or con-
Biased / seeded phases. Preferred Boolean values are ini-            straints change during search to redirect local moves. Fixed
tialized or steered using polarity, recovered structure, a can-      weights supplied by the problem alone are excluded.
didate assignment, or a configured sign. Reusing past assign-        Temperature / noise control. Temperature, noise proba-
ments alone belongs to phase saving.                                 bility, or another exploration-strength parameter changes
Conflict-activity branching. Conflicts or learned clauses            over time or with stagnation. A fixed noise probability alone
update variable priorities, as in variable-state independent         is insufficient.
decaying sum (VSIDS) and its exponential variant. Static             Adaptive restarts. Observed search behavior, such as clause
occurrence scores and clause activity alone are excluded.            quality or stagnation, triggers restarts or changes their tim-
Phase saving. Previously assigned Boolean values are re-             ing. A fixed restart schedule alone is excluded.
membered and reused in later decisions. A single fixed pre-
ferred polarity is insufficient.                                     K.3.5 Structure recovered from CNF. Semantic objects
Domain-aware branching. Semantic quantities such as                  recovered or exploited beyond generic CNF clauses and liter-
remaining-domain size, graph degree, constraint slack, or            als. Recovering a representation does not by itself imply that
gate role guide decisions. Generic literal occurrence ordering       it simplifies the problem or tolerates every encoding variant.
is separate.                                                         Semantic components / cones. Meaningful components,
Learned-clause retention. A deliberate policy ranks, re-             cones of influence, layers, or decompositions are recovered
tains, or deletes learned clauses using quality, activity, size,     and exploited. Ordinary recursion or adjacency storage alone
recency, or related measures. Proof-format deletion book-            is insufficient.
keeping alone is excluded.                                           Problem graphs. A native problem graph is reconstructed
Diverse search starts. Search is deliberately retried with           whose vertices and edges represent domain objects, for ex-
distinct seeds, shuffled orders, perturbations, or initial as-       ample in coloring or reachability. Generic clause-variable
signments. One random initial state alone is insufficient.           incidence and watch graphs are excluded.
Learned-clause minimization. Redundant literals are re-              Gates / Boolean circuits. Gate semantics or a Boolean
moved from a learned conflict clause beyond ordinary con-            circuit are recovered from clauses and used in solving, re-
flict analysis. General preprocessing vivification is separate.      duction, or certification. This includes comparison circuits
Random branch / tie choices. Randomness selects search               and AND-inverter graphs; suggestive variable names alone
variables or values or resolves decision ties. Random-number         are insufficient.
tests, identifiers, and independent initial sampling alone are       Finite-domain variables. Boolean literals are grouped into
excluded.                                                            multi-valued variables and explicit domain constraints used
Make / break scoring. Local-search moves are scored by               in native search or propagation. Single Boolean variables or
their changes to satisfied or violated clauses or domain             incidental clause groups are excluded.
constraints. Make counts newly satisfied constraints; break          Cardinality / PB constraints. Counting constraints,
counts newly violated ones.                                          weighted Boolean sums, or inequalities are recovered from
                                                                                   Harrison Green, Claire Le Goues, and Fraser Brown


CNF and used in reasoning. Coefficients appearing only in        Sequential methods. Two or more different solving proce-
proof output are insufficient.                                   dures are attempted in sequence. Repeated seeds, recognition
Permutations / orders. A permutation, ordering, sequence,        variants, and proof emission after solving alone are excluded.
or positional combinatorial object is recovered and manip-       Candidate / phase transfer. An assignment, incumbent,
ulated directly. Sorting input clauses or variables alone is     preferred phase, or partial candidate produced by one
excluded.                                                        method is passed to another. Independent guesses and final
Arithmetic / modular structure. Integer, modular, polyno-        result printing are excluded.
mial, subset-sum, or number-theoretic quantities and equa-       Constraint / bound transfer. Constraints, algebraic rela-
tions are recovered beyond generic Boolean counting con-         tions, bounds, or deductions pass between distinct reasoning
straints. Numeric parsing alone is insufficient.                 methods. Ordinary clause sharing within one engine alone
Other recovered structure. A concrete semantic represen-         is insufficient.
tation falls outside the named categories. The annotation        Separate SAT / UNSAT routes. Distinct specialized proce-
must identify it and explain the taxonomy gap; generic clause    dures find satisfying assignments and derive unsatisfiability
storage is excluded.                                             certificates within one submission. The two outcomes of one
                                                                 generic clause-learning engine alone are insufficient.
Equivalence / implication. Semantic equivalence classes,
strongly connected implication components, or a tractable        Size / feature dispatch. Counts, estimated complexity, or
implication fragment form a higher-level representation.         other coarse instance features select different solving proce-
Generic implication storage for clause learning alone is ex-     dures. Changing a limit within one unchanged algorithm is
cluded.                                                          insufficient.
Matching / assignment. Matching, bipartite assignment,           General SAT fallback. An unsupported, unsuccessful, or
permutation-matrix, flow, or Hall-set roles and constraints      exhausted specialized route can invoke a generic SAT engine.
are recovered. A generic graph representation alone is insuf-    The label records a reachable fallback and does not guarantee
ficient.                                                         completeness.
                                                                 Repeated configurations. An outer coordinator runs re-
XOR / parity equations. Recovered parity constraints are
                                                                 peated starts or configurations of a method and handles their
represented as equations or an explicit parity system used
                                                                 success or failure. Restarts wholly internal to an unchanged
in reasoning or search. Treating XOR only as a circuit gate
                                                                 search loop are excluded.
or bitwise operation is insufficient.
                                                                 Budgeted handoff. A per-method resource limit triggers
Symmetry / group structure. A concrete symmetry, orbit,
                                                                 another method or an escalation. A final timeout without an
automorphism, or group action is identified and used in
                                                                 alternative, or a restart of the same method, is excluded.
reasoning or construction. Generic sorting or a symmetry
claim alone is insufficient.                                     Residual subsolver calls. A higher-level procedure condi-
                                                                 tionally or repeatedly invokes a distinct solver on residual
State-transition systems. Automata, transitions, traces,         instances or subproblems and uses its answers. Ordinary
planning states, or temporal steps are recovered and used for    recursive branches are excluded.
reasoning in a state space. A purely combinational circuit
alone is insufficient.                                           Unlogged / certifying stages. A search or check runs with-
                                                                 out proof logging, then is repeated or transfers information
Geometry / packing. Coordinates, shapes, intervals, place-       into a certifying run. Identical search replay is not required;
ments, physical-board adjacency, or geometric constraints        ordinary proof-format conversion alone is excluded.
are recovered for solving. A matrix used only for storage is
                                                                 Refinement loop. Distinct procedures, or abstraction, can-
excluded.
                                                                 didate, and refutation steps, alternate in a feedback loop.
Statistical models. A factor/message, correlation, spectral,     One-way preprocessing followed by a single solve is insuffi-
or other statistical representation supports inference or can-   cient.
didate generation. Ordinary clause incidence without statis-
                                                                 Adaptive effort allocation. Runtime progress or method
tical state is excluded.
                                                                 outcomes change how effort is allocated among methods. A
                                                                 fixed sequence of predetermined budgets is excluded.
K.3.6 Combining solving methods. Ways to select, com-            Parallel portfolio. Distinct solving procedures run concur-
bine, or exchange information between solving procedures.        rently and their results are coordinated. Sequential calls and
Outer coordination is distinguished from policies internal to    independent starts without different methods are excluded.
one search loop.
Structural dispatch. Recognized problem structure or en-         K.3.7 Encoding assumptions and safeguards. Input-
coding selects a solving procedure. Syntax checking or chang-    representation assumptions, recognition mechanisms, scope
ing one numerical heuristic alone is insufficient.               guards, and answer checks. Recognition and safeguards can
The Case for Automated Hyperspecialization:
Evidence from SAT

coexist with encoding dependence; these labels are not an          Sampled / fingerprint checks. Bounded simulation, sam-
empirical test of correctness or shuffle robustness.               pling, or fingerprints screen semantic recognition, equiva-
Unsupported-case rejection. A failed semantic or scope             lence, or candidate properties. Later exact validation is sep-
check intentionally reports UNKNOWN or rejects the spe-            arate; generic random search and hash-table equality are
cialized route. Generic timeouts and file-opening errors are       excluded.
excluded.                                                          Stored candidates / proofs. A reachable result route
                                                                   retrieves an embedded or external precomputed model,
Structural validity guards. A recovered template, invari-
                                                                   proof, or answer. Constants for a general construction, local-
ant, or encoding condition is checked before specialization,
                                                                   operation tables, and runtime memoization are excluded.
with explicit rejection or fallback on failure. Basic input syn-
tax checking alone is insufficient.                                Certificate / RUP checks. The supplied run path checks
                                                                   its own certificate or replays proof obligations before ac-
Relational recognition. Semantic roles are inferred from           cepting an UNSAT certificate. This includes reverse-unit-
incidence, gate or graph relations, or constraint patterns.        propagation (RUP) obligation checks and does not imply an
This can coexist with variable-ID assumptions and does not         independent checker of a complete serialized proof.
establish invariance under input permutation.
Exact templates / signatures. Fixed formula sizes, exact
templates, hashes, or names select a semantic route or candi-
date beyond generic complexity thresholds. Signature match-
ing is distinct from subsequent validation and is not an in-
tegrity judgment.
Original-CNF model checks. At least one reachable SAT
success route checks a completed candidate against every
original clause. The label does not imply that all success
routes do so; reduced-only and sampled checks are excluded.
Multiple encoding variants. Multiple encodings, orienta-
tions, variable layouts, or clause-pattern variants of the same
semantic task are explicitly handled. Supporting different
input sizes alone is insufficient.
Variable-ID / layout reliance. Arithmetic on variable iden-
tifiers, fixed offsets, or contiguous identifier blocks assigns
semantic roles. Generic array indexing, renumbering, and
literal encoding alone are excluded.
Model reconstruction. Eliminated variables or a domain
solution are lifted to a complete original-variable assignment
using dependencies, elimination records, or an explicit map-
ping. Printing an already complete assignment is excluded.
Canonicalized recognition. Signs, permutations, clause or
literal order, or equivalent encodings are canonicalized to
recognize structure across variants. Sorting only for dedupli-
cation or fast lookup is excluded.
Rejected-candidate fallback. Failure of candidate, domain,
or model validation resumes search or invokes another
method instead of reporting SAT. Parsing or recognition
failure alone is separate.
Domain / reduced checks. A reconstructed domain solu-
tion or reduced or partial candidate is explicitly validated
beyond ordinary search transitions, potentially before lifting
to CNF. This is distinct from checking every original clause.
Clause-order reliance. Input clause positions, adjacency,
or order determine semantic roles. Ordinary traversal and
sorting into order-independent groups are excluded.
