                                            Directed Neuro-Symbolic Stochastic Execution for Verification of
                                                           Distributed Parallel AI Programs
                                                Gautham Koorma             Vikas Sharma           George Edwards         Mahdi Eslamimehr(B)∗
                                                                   Quandary Peak Research, Los Angeles, CA, USA
                                                                   gautham@quandarypeak.com, vikas@quandarypeak.com,
                                                                    george@quandarypeak.com, mahdi@quandarypeak.com



                                                                                                Abstract
                                                   Distributed parallel Artificial Intelligence (AI) programs expose reliability gaps that conventional
                                               testing cannot close: parallel executions are non-deterministic, and AI workloads bring high-dimensional
arXiv:2608.07947v1 [cs.AI] 8 Aug 2026




                                               inputs and non-linear operations that defeat fuzzing and symbolic execution in isolation. We present
                                               Directed Neuro-Symbolic Stochastic Execution (DNSSE), a hybrid testing framework that couples sched-
                                               ule prediction guided by a Large Language Model (LLM) with symbolic constraint solving and coverage-
                                               guided stochastic mutation. We model distributed AI executions as non-deterministic transition systems,
                                               specify correctness in linear temporal logic, and prove soundness, bounded completeness, and probabilis-
                                               tic completeness of the hybrid solver, together with an expected-cost analysis of LLM-guided schedule
                                               exploration. A scalable implementation on PyTorch and Ray detects 2.9× more concurrency bugs than
                                               the strongest baseline and raises average branch coverage from 68.6 % to 91.6 % across five realistic
                                               distributed AI benchmarks.
                                               Keywords: software testing, symbolic execution, fuzz testing, large language models, distributed sys-
                                               tems, parallel programming, formal verification


                                        1      Introduction
                                        Production AI systems such as data-parallel training pipelines, federated learning services, reinforcement
                                        learners, and high-throughput inference servers execute across heterogeneous clusters, coordinate thousands
                                        of concurrent activities, and manipulate models with billions of parameters. As these systems enter safety-
                                        and business-critical roles, ensuring their reliability and correctness has become a formidable and largely
                                        unsolved engineering challenge.
                                            The difficulty stems from two compounding sources of complexity. First, parallel programs are inher-
                                        ently non-deterministic: data races, deadlocks, and atomicity violations manifest only under particular
                                        interleavings, and empirical studies show that such faults are among the most frequent and damaging de-
                                        fects in multithreaded applications [1] and datacenter distributed systems [2]. Second, AI programs have
                                        high-dimensional continuous input spaces, and their control flow is guarded by non-linear operations (activa-
                                        tions, normalizations, tensor contractions) that resist classical analysis. Where the two paradigms intersect,
                                        the product of the interleaving space and the input space renders the reachable state space intractable for
                                        conventional testing.
                                            Existing techniques address at most one side of this product space. Symbolic execution [3] offers rigorous
                                        per-path reasoning but suffers from path explosion and from solver incompleteness on floating-point, non-
                                        linear arithmetic. Coverage-guided and parallel fuzzing [4–6] scales well but rarely penetrates regions guarded
                                        by tight numerical conditions, and it is oblivious to the scheduling dimension. Systematic concurrency
                                        testing [7] controls the scheduler but does not reason about numerical inputs. Testing techniques for deep-
                                        learning systems and libraries [8,9] target sequential APIs or the model function itself, leaving the distributed
                                        program that embeds the model out of scope.
                                            ∗(B) Corresponding author: mahdi@quandarypeak.com




                                                                                                   1
    To close this gap we propose Directed Neuro-Symbolic Stochastic Execution (DNSSE), which fuses three
engines into one directed search: a symbolic engine that solves the decidable fragment of path constraints,
a stochastic mutation engine that resolves the non-linear fragment by coverage-guided randomized search,
and a Large Language Model (LLM) scheduler that reads the semantic structure of distributed AI code and
ranks thread interleavings by their estimated potential to expose concurrency violations. The LLM acts only
as a learned prior over the schedule space; feasibility remains with the symbolic and stochastic engines, so
the formal guarantees never depend on the LLM being right.
    This paper makes four contributions: (1) DNSSE, a novel algorithm combining LLM-guided schedule
prediction with directed symbolic and stochastic execution for distributed parallel AI programs (Sects. 4–
5); (2) a formal framework based on transition systems and linear temporal logic (LTL), with proofs of
soundness, bounded completeness, and probabilistic completeness, plus an expected-cost bound quantifying
when learned ranking beats uniform exploration (Sect. 6); (3) a scalable architecture on PyTorch and Ray
that distributes tracing, constraint solving, and fuzzing across a cluster (Sect. 7); and (4) an evaluation
on five realistic distributed AI benchmarks, in which DNSSE detects 2.9× more concurrency bugs than the
strongest baseline (73 vs. 25 in aggregate) and raises average branch coverage from 68.6 % to 91.6 % (Sect. 8).


2    Related Work
Testing Concurrent Programs. Foundations for reasoning about concurrent executions were laid by
temporal logic [10, 11], still the standard language for specifying safety and liveness of interleaved compu-
tations. Precise dynamic race detection is exemplified by FastTrack [12], while race-directed scheduling
combines dynamic analysis with schedule synthesis to force concurrent programs into real races [7]; the
directed paradigm has been extended to deadlocks [13], atomicity violations [14], and timing analysis of
event-driven programs [15]. These techniques are effective for traditional Java/C/C++ code, but none of
them reasons about the non-linear numerical guards and tensor-level data flow that dominate AI workloads.

Symbolic Execution and Hybrid Testing. Symbolic executors such as KLEE [3] and concolic test-
ing [16] enumerate feasible paths systematically by solving accumulated path constraints. Because solving
stalls on deep or non-linear conditions, hybrid systems hand off work between a fuzzer and a symbolic en-
gine, as in QSYM [17]. Orthogonally, parallel fuzzing scales stochastic testing to clusters: P-Fuzz distributes
fuzzing state through a database-centric architecture [4], AFL-EDGE partitions seeds into mutually exclu-
sive tasks [5], and KRAKEN adapts task allocation to program characteristics [6]. All of these systems
target sequential binaries or thread-oblivious executions; the schedule dimension of the search space is left
unexplored.

Verification and Testing of AI Systems. A complementary line of work tests the AI artifact itself.
DeepXplore [8] introduced coverage-guided whitebox testing of neural networks, and DeepREL fuzzes deep-
learning libraries through automatically inferred relational APIs [9]. On the formal side, Reluplex extends
SMT solving to verify piecewise-linear networks [18]. These techniques treat the model or the library API
as a sequential function; they do not address races, deadlocks, or atomicity violations arising when models
are trained or served by concurrent distributed programs.

LLMs for Software Testing. LLMs have recently been embedded in the testing loop. TitanFuzz uses
LLMs as zero-shot generators and mutators of deep-learning API programs [19], and Fuzz4All generalizes
LLM-driven fuzzing across languages and systems [20]. Closer to program analysis, LLM-powered symbolic
execution decomposes path-constraint reasoning into subtasks delegated to a model [21], hybrid concolic
testing employs LLMs for guided path exploration [22], and directed execution combined with LLM-driven
analysis has been applied to zero-day malware detection [23]. None of these efforts, however, uses an LLM to
navigate the schedule space of a distributed parallel AI program, nor do they integrate schedule prediction
with a hybrid symbolic–stochastic constraint solver. DNSSE fills precisely this gap.




                                                      2
3     Motivating Example
The listing below distills a data-parallel training loop in the style of PyTorch DistributedDataParallel [24]:
each worker backpropagates and, only when the loss falls below a threshold, updates a shared convergence
counter that a coordinator concurrently reads to decide termination.
      def worker(rank, model, loader, shared):
          for x, y in loader:
              out = model(x)                # softmax, tanh: non-linear
              loss = cross_entropy(out, y)
              loss.backward()               # async all-reduce hooks
              if loss.item() < THETA:       # data-dependent guard
                  t = shared.converged      # read shared counter
                  shared.converged = t + 1 # unsynchronized write
              optimizer.step()

   The read–modify–write on shared.converged is not atomic: if two workers interleave between the read
and the write, an increment is lost and the coordinator may never observe convergence. Exposing the defect
requires satisfying two coupled conditions at once. First, an input x must drive the loss below Θ, a constraint
routed through the cross-entropy of a softmax that lies outside decidable SMT theories, so purely symbolic
tools stall. Second, two workers must interleave within a window of a few instructions, which random
scheduling hits with vanishing probability, so even a fuzzer that finds a low-loss input almost never observes
the race. DNSSE divides the labor: the LLM scheduler flags the unsynchronized access pair as high risk
and ranks interleavings that place two workers inside the window first; the symbolic engine tracks the linear
index and control-flow constraints exactly; and the stochastic engine searches for x with loss(x) < Θ under
a branch-distance objective.


4     Formal Framework
4.1    System Model
Definition 1 (Distributed Parallel AI Program). Let P = ⟨T , S, I, O, ∆, s0 ⟩ be a distributed parallel AI
program, where T = {t1 , . . . , tn } is a finite set of threads or distributed workers; S is the set of global
states, each comprising all local thread states, the shared memory (e.g., model parameters and optimizer
state), and channel contents; I ⊆ Rd is the input space; O is the output space; ∆ : S × I × T → 2S is the
non-deterministic transition relation; and s0 ∈ S is the initial state.

    A thread t is enabled in s under x iff ∆(s, x, t) ̸= ∅, with En(s, x) the set of enabled threads.
Definition 2 (Schedule and Trace). A schedule of length k is a sequence σ = ti0 ti1 · · · tik−1 ∈ T k . Given an
                                                                 ti      ti      tik−1
                                                                0       1
input x ∈ I, the pair (σ, x) induces the set of traces π = s0 −−→  s1 −−→  · · · −−−→ sk with sj+1 ∈ ∆(sj , x, tij )
and tij ∈ En(sj , x) for all j. We write ΠD (P) for the set of traces of length at most D.
    Each transition is labeled with the memory events it performs: Rd(t, v) and Wr(t, v) denote thread t
reading or writing shared location v (tensors carry their accessed index sets). The happens-before relation
≺π of a trace π is the smallest partial order over events containing program order and synchronization order
(lock release to subsequent acquire, send to receive, collective barriers) [12].
Definition 3 (Concurrency Faults). Let π be a trace of P. (i) π exhibits a data race on v iff it contains
e1 = Wr(ti , v) and e2 ∈ {Rd(tj , v), Wr(tj , v)}, i ̸= j, unordered by ≺π . (ii) π exhibits an atomicity violation
iff a block declared atomic in ti is interleaved by a conflicting access of tj , j ̸= i, in a non-serializable order.
(iii) A state s is a deadlock iff En(s, x) = ∅ while some thread has not terminated.




                                                         3
4.2    Symbolic Executions and Path Constraints
During symbolic execution the input is a vector of symbolic variables X = [X1 , . . . , Xd ]T ; every branch along
a trace π contributes its condition (or negation), forming the path constraint
                                                             |π|−1
                                                                 ^
                                               Φπ (X) =              ck (X),                                    (1)
                                                              k=0

where ck (X) is the branch condition at step k over the symbolic store. A trace is feasible iff some x ∈ I
satisfies Φπ (x); any such witness x, paired with the schedule σ, is a replayable test case.

4.3    Correctness Properties in LTL
Let AP be a set of atomic propositions over S. LTL formulas are built from AP with Boolean connectives and
the temporal operators □ (always), ♢ (eventually), and ⃝ (next), with standard semantics over traces [25].
Freedom from data races and from deadlock are the invariants
                                        _                                                 
                       ϕrace = □ ¬            Wr(ti , v) ∧ Acc(tj , v) ∧ unord(ti , tj , v) ,           (2)
                                        ti ̸=tj , v
                                                 W               
                        ϕlive   =   □ run →           t∈T En(t) ,                                               (3)

where Acc is a read or write access and unord states that the two accesses are unordered by ≺π . Atomicity
of a block β requires that between begin(β) and end(β) no conflicting access of another thread occurs in a
non-serializable order (Definition 3). The verification goal is to decide whether some π ∈ ΠD (P) violates ϕ
(written π ̸|= ϕ) and, if so, to produce the witness pair (σ, x).

4.4    The Hybrid Constraint-Solving Problem
Path constraints of AI programs mix tractable and intractable conjuncts: array indexing, batching logic,
and synchronization guards yield linear arithmetic, whereas activation functions such as tanh and softmax
yield non-linear transcendental terms undecidable for standard SMT theories. Let L denote the decidable
fragment supported by the solver (quantifier-free linear real and integer arithmetic with arrays). We define
a syntactic classifier τ (c) ∈ {sym, stoch} that assigns each conjunct c to sym iff every term of c lies in L,
and partition
                                                                ^                      ^
              Φπ (X) = Φsym (X) ∧ Φstoch (X),         Φsym =         ck , Φstoch =           ck .          (4)
                                                                      τ (ck )=sym               τ (ck )=stoch

The hybrid constraint-solving problem is: given a property ϕ, find a schedule σ ∗ and input x∗ such that

                    Φsym (x∗ ) ∧ Φstoch (x∗ ) ∧ feasible(σ ∗ ) ≡ true           and   π(σ ∗, x∗ ) ̸|= ϕ.        (5)

DNSSE attacks Eq. (5) with an SMT solver for Φsym , randomized search for Φstoch , and an LLM prior over
candidate schedules σ.


5     The DNSSE Algorithm
DNSSE orchestrates three components (a symbolic engine, a stochastic mutation engine, and an LLM-driven
path scheduler) in one distributed worklist search over the state space of Definition 1.

5.1    Core Algorithm
Algorithm 1 presents the core loop. The worklist W holds tuples (s, Φ, σ, x): a frontier state, its accumu-
lated path constraint, the schedule prefix that reached it, and a concrete witness input x satisfying Φ, an
invariant central to the soundness proof (Sect. 6). Each iteration selects the highest-priority entry, checks


                                                             4
Algorithm 1 Directed Neuro-Symbolic Stochastic Execution
Require: Program P, LTL property ϕ, LLM M, depth bound D
Ensure: Counterexample trace πbug with witness (σ, x), or ∅
 1: W ← {(s0 , true, ε, xseed )}
 2: while W ̸= ∅ do
 3:   (s, Φ, σ, x) ← SelectState(W, M)
 4:   if π(s) ̸|= ϕ then
 5:      return π(s) {bug found; (σ, x) replays it}
 6:   end if
 7:   if |σ| ≥ D then
 8:      continue
 9:   end if
10:   E ← GetEnabledTransitions(s)
11:   σnext ← M.PredictSchedule(E, s, ϕ)
12:   for each transition e ∈ σnext do
13:       (s′ , c) ← ExecSymbolic(s, e); Φ′ ← Φ ∧ c
14:       if τ -classification of Φ′ is fully decidable then
15:           x′ ← SMTSolve(Φ′ )
16:       else
17:           x′ ← StochasticFuzz(Φ′ , s′ , x)
18:       end if
19:       if x′ ̸= UNSAT then
20:           W ← W ∪ {(s′ , Φ′ , σ · e, x′ )}
21:       end if
22:   end for
23: end while
24: return ∅



the property, and expands the frontier: the LLM ranks the enabled transitions, each ranked transition is
executed symbolically, and the extended constraint is solved by SMT when it lies in the decidable fragment
and by stochastic search otherwise. Constraints not satisfied within the mutation budget are re-enqueued
with decayed priority rather than discarded, so prioritization never erases part of the search space.

5.2    LLM-Guided Schedule Prediction
The LLM scheduler differentiates DNSSE from classical directed testing. Given state s, enabled transitions
E, and property ϕ, the model receives a serialized context (thread program counters, lock and channel state,
pending collectives, and the source fragments adjacent to each enabled transition) and generates a ranking
of E. If the returned ranking is malformed or incomplete, DNSSE falls back to a uniform random order, so
scheduling always yields a permutation of E; Sect. 6 exploits this. The final priority combines the normalized
LLM confidence PM (e) with a structural risk heuristic:

                                                                                sh(e) |Tacc (e, s)|
                 score(e) = α PM (e) + (1 − α) H(e, s),            H(e, s) =          ·             ,         (6)
                                                                               ops(e)     |T |

where sh(e) and ops(e) count shared-variable accesses and total operations of e, Tacc (e, s) is the set of threads
concurrently accessing the memory region e touches, and α ∈ [0, 1] balances learned against structural
evidence.

5.3    Stochastic Constraint Solving
For constraints containing non-linear conjuncts, DNSSE minimizes the classical branch-distance objec-
tive [26]. Each conjunct c of Φstoch contributes a non-negative distance d(c, x) that is zero iff c holds
under x (e.g., d(a ≤ b) = max(0, a − b), evaluated on the concrete execution), and the solver seeks
                                                           X
                      x∗ = arg min F (x),       F (x) =          d(c, x) s.t. Φsym (x),               (7)
                                  x∈I
                                                               c ∈ Φstoch

accepting x∗ as a witness iff F (x∗ ) = 0. The search perturbs the current witness with coverage-guided
mutations (Gaussian noise, boundary values, dimension-wise crossover of corpus seeds), projecting candidates


                                                        5
onto the subspace satisfying Φsym when the projection is linear and re-validating them with the SMT solver
otherwise. Every accepted witness comes from a concrete replayed execution, so floating-point semantics are
exact by construction and no solver-level approximation of transcendental functions is needed.

Complexity. Let B bound the per-thread branching factor, n = |T |, and D the depth bound. Each step     
chooses one of at most n enabled threads and one of at most B branch outcomes, so |ΠD (P)| = O (Bn)D :
the schedule and input dimensions multiply, which is precisely the explosion that defeats single-paradigm
tools. DNSSE does not shrink this worst case, as no sound and complete method can, but it changes
the order of the visit; Proposition 1 quantifies the expected saving under a budget. Per node, one SMT
query over conjunctive QF LRA constraints is decidable in polynomial time (NP-hard once integers enter),
one stochastic solve costs O(k · d) for k mutation rounds on d-dimensional inputs, and the LLM adds one
bounded-length inference whose empirical share of runtime is measured in Sect. 8.


6    Formal Guarantees
Throughout, P, ϕ, and D are fixed, and “DNSSE returns πbug ” means Algorithm 1 terminates at its
property-violation return.
Lemma 1 (Partition Correctness). For every path constraint Φπ (X), the partition of Eq. (4) is a logical
equivalence: Φπ ≡ Φsym ∧ Φstoch , and Φπ is satisfiable iff Φsym ∧ Φstoch is satisfiable.

Proof. Each conjunct of Eq. (1) is mapped by the classifier τ to exactly one sub-conjunction, with no other
change, so both sides of Eq. (4) contain the same conjuncts; by associativity and commutativity of ∧ they
are logically equivalent and thus equisatisfiable.
Lemma 2 (Witness Invariant). Every tuple (s, Φ, σ, x) ever inserted into W satisfies Φ(x) = true, and x
replayed under schedule σ drives P from s0 to s.
Proof. By induction on insertions. The initial tuple carries Φ = true, satisfied by any seed. A tuple
(s′ , Φ′ , σ · e, x′ ) is inserted only after the guard x′ ̸= UNSAT; both solver branches return x′ only when
Φ′ (x′ ) holds: the SMT solver by producing a model, and the stochastic solver by concretely executing the
program and checking F (x′ ) = 0 in Eq. (7), with Lemma 1 combining the fragments. Symbolic execution of
e from s extends the trace by exactly e, so replaying σ · e under x′ reaches s′ .
Theorem 1 (Soundness). If DNSSE returns πbug , then πbug is a feasible execution of P that violates ϕ,
and the returned pair (σ, x) deterministically replays it.
Proof. The returned trace is π(s) for the selected tuple. By Lemma 2, its witness x satisfies the accumulated
constraint and replaying σ under x reproduces exactly the transitions of π(s), so πbug ∈ ΠD (P) is feasible,
not merely symbolically consistent; and the property check verified π(s) ̸|= ϕ before returning. Hence the
output is a genuine counterexample and DNSSE reports no false positives.
Theorem 2 (Bounded Completeness). Assume (i) the SMT solver is sound and complete for L and (ii)
the stochastic solver is an oracle for Φstoch , returning a witness whenever one exists. Then DNSSE explores
every feasible trace of length at most D; in particular, if some π ∈ ΠD (P) violates ϕ, DNSSE returns a
counterexample.

Proof. By induction on trace length ℓ ≤ D, every feasible prefix is eventually dequeued. The base case
is the initial tuple. When a prefix is expanded, the expansion loop iterates over the entire ranked list,
which by construction (Sect. 5.2, uniform fallback) is a permutation of all enabled transitions; prioritization
reorders but never removes. Satisfiability of each extension is decided exactly: decidable constraints by
assumption (i), mixed constraints by assumption (ii) with Lemma 1. Hence exactly the feasible extensions
of length ℓ + 1 are inserted, and none is starved, because re-enqueued entries retain positive priority and
the depth bound makes the tree finite (O((Bn)D ) nodes). A violating trace within depth D is therefore
eventually dequeued and detected by the property check.



                                                      6
                                                  LLM Scheduler (M)

                                                                schedule

                                           task                                 task
                                                  Central Coordinator




                                                         shared state
                                         Ray Worker 1                    Ray Worker N


                                         Z3 SMT Solver                  LibFuzzer Engine


                                                   Redis State Store



                          Figure 1: System architecture of the DNSSE framework.


   Assumption (ii) idealizes the fuzzer; the next theorem replaces it with a quantitative statement about
the real, randomized solver.
Theorem 3 (Probabilistic Completeness of Stochastic Solving). Let Φ = Φsym ∧ Φstoch be satisfiable and let
S = {x ∈ I | Φ(x)} denote its witness set. Suppose each mutation round draws its candidate from a proposal
distribution q with q(S) ≥ ε > 0 (full support, e.g., a Gaussian kernel mixed with uniform restarts). Then
the probability that k independent rounds all fail to find a witness is at most (1 − ε)k , so the solver succeeds
with probability at least 1 − (1 − ε)k → 1 as k → ∞, and the expected number of rounds to success is at most
1/ε.

Proof. Each round independently lands in S with probability at least ε, so Pr[no witness in k] ≤ (1 − ε)k ;
the success probability is its complement, and a geometric random variable with parameter ε has expectation
1/ε. Coverage guidance and Φsym -projection only reallocate proposal mass, while uniform restarts preserve
q(S) ≥ ε, so the bound also covers the guided search.
   Finally, we quantify what the LLM buys. Prioritization cannot enlarge the set of explorable traces
(Theorem 2); its value is the expected cost to the first counterexample under a finite budget.
Proposition 1 (Expected Exploration Cost under Ranking). Let Σ be the set of maximal schedules explored
at some frontier, N = |Σ|, of which a nonempty subset B ⊆ Σ exposes the target violation. Uniform
random exploration without replacement dequeues its first element of B after (N + 1)/(|B| + 1) schedules in
expectation. If with probability p the ranked order places some element of B within the first m positions, the
expected number of schedules explored before exposure is at most

                                          E[cost] ≤ p m + (1 − p) N.                                         (8)

For a single buggy schedule (|B| = 1) the uniform baseline is (N + 1)/2, so any ranker with p > 1/2 and
m < N/2 strictly wins, and the advantage grows linearly in N when m ≪ N .

Proof. The uniform figure is the standard expectation of the minimum position of |B| marked items in a
uniformly random permutation of N items. For the bound, condition on the ranking event: with probability
p exposure occurs within the first m dequeues; otherwise it occurs after at most N . Taking expectations
yields Eq. (8).


7    System Architecture and Implementation
DNSSE is implemented in Python 3.11 on PyTorch 2.1 [27] and the Ray 2.9 distributed computing frame-
work [28]. Figure 1 shows the architecture, a master–worker design coordinated through Ray’s actor model.




                                                              7
LLM Scheduler. The scheduler is a Llama 3 8B model [29] served through vLLM [30] with 4-bit quan-
tization, fine-tuned on 12,000 annotated concurrency-bug traces from open-source distributed AI projects,
each pairing a serialized scheduling context with the transition that led to a confirmed violation. The infer-
ence prompt encodes the execution state, enabled transitions, and target LTL property; the model emits a
JSON-formatted ranking, with the uniform fallback of Sect. 5.2 engaging on malformed output.

Coordinator and State Store. A singleton Ray actor maintains the global worklist W as a priority
queue keyed by the scores of Eq. (6) and dispatches expansion tasks through Ray’s asynchronous task API;
workers are stateless between tasks, so a crashed worker is simply restarted and its task re-issued, preserving
the invariant of Lemma 2. A centralized Redis instance holds the global coverage bitmap, deduplicated
bug reports, and a cache mapping canonicalized constraints to witnesses; workers merge coverage deltas
idempotently, suppressing redundant exploration without global locking.

Execution Workers. Each worker runs a sandboxed instance of the target program, intercepting the
PyTorch computational graph with torch.fx to extract symbolic expressions during the forward pass. Con-
ditions over standard arithmetic are classified by τ (Sect. 4.4) as decidable and forwarded to Z3 4.12 [31];
conjuncts involving activation functions and tensor contractions go to an embedded LibFuzzer engine imple-
menting the search of Eq. (7). Schedule control instruments synchronization points (locks, queues, collectives)
with a cooperative scheduler that realizes the prefix σ deterministically.

Reproducibility. Experiments run on an Ubuntu 22.04 cluster with 8 NVIDIA A100 (80 GB) GPUs and
64 CPU cores, with pinned dependencies (PyTorch 2.1, Ray 2.9, Z3 4.12, vLLM 0.3, Transformers 4.38) in
Docker containers, LLVM IR for C/C++ runtime components generated by Clang 17, and fixed random
seeds. We plan to release DNSSE under the MIT license on GitHub; at this time, the source code is publicly
available.1


8     Experimental Evaluation
Our evaluation answers three research questions. RQ1: How does DNSSE compare with state-of-the-art
methods in coverage and bug detection? RQ2: What overhead do the LLM scheduler and hybrid solver
introduce? RQ3: How much does each component contribute?

8.1    Experimental Setup
Baselines. We compare against (1) KLEE-AI, an adaptation of KLEE [3] extended to tensor operations
through LLVM bitcode instrumentation (pure symbolic execution); (2) P-Fuzz [4], a distributed grey-box
fuzzer with 8 parallel instances (scalable stochastic testing); and (3) Random, uniformly random schedules
and inputs.

Benchmarks. The suite comprises five applications representative of production distributed AI work-
loads: Dist-Train, data-parallel training with gradient synchronization across 4 workers in the style of
DistributedDataParallel [24] (8,200 LOC); Fed-Learn, a federated aggregation server with asynchronous,
differentially private client updates (6,400 LOC); RL-Agent, multi-agent reinforcement learning with shared
replay buffers (5,900 LOC); Graph-GNN, a distributed graph neural network with partitioned message
passing (7,100 LOC); and Infer-Serve, a concurrent inference server with dynamic batching and model
sharding (9,300 LOC). Each experiment runs with a 1-hour wall-clock budget (KLEE-AI additionally re-
ceives 24 hours); reported numbers average 5 independent runs with fixed seeds.
   1 DNSSE temporary codebase host: https://drive.google.com/drive/folders/1o43AblLAnRNejZGa2_cpGUJN3el3Kon-?usp=

drive_link




                                                       8
Table 1: Branch coverage and confirmed concurrency bugs per method. T/O: KLEE-AI exceeded its extended
24-hour budget.

                                 Coverage (%)                                    Bugs
      Benchmark      Rand.    KLEE-AI P-Fuzz           DNSSE      Rand.    KLEE-AI P-Fuzz      DNSSE
      Dist-Train      42.1      58.3        65.4        89.2        1             3     5         14
      Fed-Learn       38.5      49.1        71.2        93.7        0             2     4         11
      RL-Agent        45.0      52.4        68.9        91.5        2             1     6         17
      Graph-GNN       40.2      55.7        62.1        88.4        1             2     3         12
      Infer-Serve     51.3      61.8        75.4        95.1        3             4     7         19
      Mean / Total    43.4      55.5        68.6        91.6        7             12   25         73



                        Table 2: DNSSE component time breakdown (% of total).

                                Benchmark      LLM         SMT    Fuzz    Other
                                Dist-Train      15.2       28.4   41.7    14.7
                                Fed-Learn       13.8       31.2   38.9    16.1
                                RL-Agent        14.1       22.6   48.3    15.0
                                Graph-GNN       16.4       18.9   51.2    13.5
                                Infer-Serve     12.0       39.7   33.1    15.2



8.2     Bug Detection and Coverage (RQ1)
Table 1 reports branch coverage and confirmed concurrency bugs (data races, deadlocks, atomicity viola-
tions). DNSSE outperforms every baseline on every benchmark: in aggregate it detects 73 bugs versus 25
for P-Fuzz (2.9×), 12 for KLEE-AI, and 7 for Random, and it raises mean branch coverage to 91.6 % versus
68.6 %, 55.5 %, and 43.4 %, respectively. Random and P-Fuzz consumed the full 1-hour budget and KLEE-AI
timed out at 24 hours on every benchmark, whereas DNSSE completed exploration in 1,590–2,680 s (mean
2,134 s).
    Per benchmark, DNSSE adds 19.7–26.3 coverage percentage points over P-Fuzz (26.1 %–42.4 % relative)
and up to 55.2 points over random scheduling (Fed-Learn). The largest relative gain occurs on Graph-
GNN, whose deep guards in the message-passing logic are rarely penetrated by P-Fuzz; the LLM contributes
most visibly on Infer-Serve, steering exploration through the batching and sharding logic. Mechanistically,
KLEE-AI times out on paths guarded by non-linear activations, while P-Fuzz lacks semantic awareness of
the scheduling space and misses interleaving-dependent defects such as the lost-update race of Sect. 3. Early
completion on every benchmark reflects Proposition 1: directed scheduling reaches the interesting region of
the schedule space early.

8.3     Performance Overhead (RQ2)
Table 2 breaks down where DNSSE spends its time. The LLM scheduler accounts for 12.0 %–16.4 % of
execution time (14.3 % on average), an overhead more than repaid by the pruning of unproductive exploration
reflected in the RQ1 completion times. The stochastic solver dominates on benchmarks rich in non-linear
operations (51.2 % on Graph-GNN), whereas the SMT share peaks on the predominantly linear Infer-Serve
(39.7 %), evidence that the classifier τ routes constraints as intended.




                                                       9
8.4    Ablation Study (RQ3)
Disabling individual modules isolates their contributions. Replacing the LLM scheduler with random schedul-
ing reduces bug detection by 58 %, confirming that semantic schedule guidance, not merely hybrid constraint
solving, drives the concurrency results. Disabling the stochastic solver (SMT only) causes timeouts on 3 of 5
benchmarks, reproducing the KLEE-AI failure mode. Removing the SMT solver (fuzzing only) lowers cov-
erage by 31 % on average: random mutation solves tight linear conditions only with vanishing probability,
as the 1/ε expectation of Theorem 3 predicts for witness sets of small measure. The components are thus
complementary, each covering a failure mode of the other two.

8.5    Discussion, Limitations, and Threats to Validity
DNSSE’s guarantees are conditional in two respects. First, Theorem 2 idealizes the stochastic solver; on real
budgets DNSSE inherits only the probabilistic guarantee of Theorem 3, so a stochastic failure never proves
infeasibility, so DNSSE re-enqueues rather than prunes such branches. Second, the LLM affects efficiency,
not correctness: a bad ranking degrades Eq. (8) toward the uniform baseline but cannot induce false positives
(Theorem 1). The main practical costs are LLM inference latency and the one-time fine-tuning corpus of
curated bug traces.
    Regarding validity: our benchmarks, though modeled on production workloads (36,900 LOC total),
are curated constructions, and results may differ on industrial codebases (external); LLM inference and the
stochastic solver are randomized, mitigated by averaging 5 runs with fixed seeds (internal); and bug counts are
deduplicated by distinct happens-before configuration (Definition 3), avoiding inflation by re-manifestations
of one root cause (construct).


9     Conclusion
We introduced DNSSE, a hybrid framework for verifying distributed parallel AI programs that integrates
LLM-guided schedule prediction with symbolic execution and coverage-guided stochastic mutation, on an
explicit formal foundation: a transition-system model with LTL specifications, proofs of soundness and
bounded completeness, a probabilistic-completeness bound for the stochastic solver, and an expected-cost
analysis of learned schedule ranking. Empirically, DNSSE detects 2.9× more concurrency bugs than the
strongest baseline and raises average branch coverage from 68.6 % to 91.6 % at an LLM overhead of 14.3 %
of runtime. Future work includes reducing scheduler latency through speculative decoding, extending the
execution model to heterogeneous accelerators, and applying DNSSE to safety-critical autonomous systems.

Acknowledgments. The authors thank the engineering team at Quandary Peak Research for their support
and infrastructure provisions during the empirical evaluation.


References
 [1] Lu, S., Park, S., Seo, E., Zhou, Y.: Learning from mistakes: a comprehensive study on real world con-
     currency bug characteristics. In: Proc. 13th Int. Conf. on Architectural Support for Programming Lan-
     guages and Operating Systems (ASPLOS), pp. 329–339. ACM (2008). doi:10.1145/1346281.1346323
 [2] Leesatapornwongsa, T., Lukman, J.F., Lu, S., Gunawi, H.S.: TaxDC: a taxonomy of non-deterministic
     concurrency bugs in datacenter distributed systems. In: Proc. 21st Int. Conf. on Architectural Support
     for Programming Languages and Operating Systems (ASPLOS), pp. 517–530. ACM (2016). doi:10.
     1145/2872362.2872374
 [3] Cadar, C., Dunbar, D., Engler, D.: KLEE: unassisted and automatic generation of high-coverage tests
     for complex systems programs. In: Proc. 8th USENIX Symposium on Operating Systems Design and
     Implementation (OSDI), pp. 209–224. USENIX Association (2008)
 [4] Song, C., Zhou, X., Yin, Q., He, X., Zhang, H., Lu, K.: P-Fuzz: a parallel grey-box fuzzing framework.
     Applied Sciences 9(23), 5100 (2019). doi:10.3390/app9235100


                                                      10
 [5] Wang, Y., Zhang, Y., Pang, C., Li, P., Triandopoulos, N., Xu, J.: Facilitating parallel fuzzing
     with mutually-exclusive task distribution. In: Proc. 17th EAI Int. Conf. on Security and Privacy in
     Communication Networks (SecureComm). LNICST, vol. 399, pp. 185–206. Springer, Cham (2021).
     doi:10.1007/978-3-030-90022-9_10
 [6] Zhou, A., Huang, H., Zhang, C.: KRAKEN: program-adaptive parallel fuzzing. Proc. ACM Softw. Eng.
     2(ISSTA), 274–296 (2025). doi:10.1145/3728882
 [7] Eslamimehr, M., Palsberg, J.: Race directed scheduling of concurrent programs. In: Proc. 19th ACM
     SIGPLAN Symposium on Principles and Practice of Parallel Programming (PPoPP), pp. 301–314. ACM
     (2014). doi:10.1145/2555243.2555263

 [8] Pei, K., Cao, Y., Yang, J., Jana, S.: DeepXplore: automated whitebox testing of deep learning systems.
     In: Proc. 26th Symposium on Operating Systems Principles (SOSP), pp. 1–18. ACM (2017). doi:
     10.1145/3132747.3132785
 [9] Deng, Y., Yang, C., Wei, A., Zhang, L.: Fuzzing deep-learning libraries via automated relational API
     inference. In: Proc. 30th ACM Joint European Software Engineering Conf. and Symposium on the
     Foundations of Software Engineering (ESEC/FSE), pp. 44–56. ACM (2022). doi:10.1145/3540250.
     3549085
[10] Pnueli, A.: The temporal logic of programs. In: Proc. 18th Annual Symposium on Foundations of
     Computer Science (FOCS), pp. 46–57. IEEE (1977). doi:10.1109/SFCS.1977.32
[11] Manna, Z., Pnueli, A.: Verification of concurrent programs: the temporal framework. In: Boyer, R.S.,
     Moore, J S. (eds.) The Correctness Problem in Computer Science, pp. 215–273. Academic Press, London
     (1981)
[12] Flanagan, C., Freund, S.N.: FastTrack: efficient and precise dynamic race detection. In: Proc. 30th
     ACM SIGPLAN Conf. on Programming Language Design and Implementation (PLDI), pp. 121–133.
     ACM (2009). doi:10.1145/1542476.1542490

[13] Eslamimehr, M., Palsberg, J.: Sherlock: scalable deadlock detection for concurrent programs. In: Proc.
     22nd ACM SIGSOFT Int. Symposium on Foundations of Software Engineering (FSE), pp. 353–365.
     ACM (2014). doi:10.1145/2635868.2635918
[14] Eslamimehr, M., Lesani, M., Edwards, G.: Efficient detection and validation of atomicity violations in
     concurrent programs. J. Syst. Softw. 137, 618–635 (2018). doi:10.1016/j.jss.2017.06.001

[15] Eslamimehr, M., Samimi, H.: Timing analysis of event-driven programs with directed testing. In: Proc.
     15th Int. Workshop on Worst-Case Execution Time Analysis (WCET). OASIcs, vol. 47, pp. 21–31.
     Schloss Dagstuhl–Leibniz-Zentrum für Informatik (2015). doi:10.4230/OASIcs.WCET.2015.21
[16] Godefroid, P., Klarlund, N., Sen, K.: DART: directed automated random testing. In: Proc. 26th ACM
     SIGPLAN Conf. on Programming Language Design and Implementation (PLDI), pp. 213–223. ACM
     (2005). doi:10.1145/1065010.1065036
[17] Yun, I., Lee, S., Xu, M., Jang, Y., Kim, T.: QSYM: a practical concolic execution engine tailored for
     hybrid fuzzing. In: Proc. 27th USENIX Security Symposium, pp. 745–761. USENIX Association (2018)
[18] Katz, G., Barrett, C., Dill, D.L., Julian, K., Kochenderfer, M.J.: Reluplex: an efficient SMT solver
     for verifying deep neural networks. In: Proc. 29th Int. Conf. on Computer Aided Verification (CAV).
     LNCS, vol. 10426, pp. 97–117. Springer, Cham (2017). doi:10.1007/978-3-319-63387-9_5
[19] Deng, Y., Xia, C.S., Peng, H., Yang, C., Zhang, L.: Large language models are zero-shot fuzzers: fuzzing
     deep-learning libraries via large language models. In: Proc. 32nd ACM SIGSOFT Int. Symposium on
     Software Testing and Analysis (ISSTA), pp. 423–435. ACM (2023). doi:10.1145/3597926.3598067




                                                     11
[20] Xia, C.S., Paltenghi, M., Tian, J.L., Pradel, M., Zhang, L.: Fuzz4All: universal fuzzing with large
     language models. In: Proc. 46th IEEE/ACM Int. Conf. on Software Engineering (ICSE), Article 126,
     pp. 1–13. ACM (2024). doi:10.1145/3597503.3639121
[21] Li, Y., Meng, R., Duck, G.J.: Large language model powered symbolic execution. Proc. ACM Program.
     Lang. 9(OOPSLA2) (2025). doi:10.1145/3763163

[22] Eslamimehr, M.: Hybrid concolic testing with large language models for guided path exploration. arXiv
     preprint arXiv:2601.12274 (2026)
[23] Edwards, G., Eslamimehr, M.: Synergistic directed execution and LLM-driven analysis for zero-day
     AI-generated malware detection. arXiv preprint arXiv:2603.09044 (2026)

[24] Li, S., Zhao, Y., Varma, R., et al.: PyTorch distributed: experiences on accelerating data parallel
     training. Proc. VLDB Endow. 13(12), 3005–3018 (2020). doi:10.14778/3415478.3415530
[25] Baier, C., Katoen, J.-P.: Principles of Model Checking. MIT Press, Cambridge, MA (2008)
[26] Korel, B.: Automated software test data generation. IEEE Trans. Softw. Eng. 16(8), 870–879 (1990).
     doi:10.1109/32.57624
[27] Paszke, A., Gross, S., Massa, F., et al.: PyTorch: an imperative style, high-performance deep learning
     library. In: Advances in Neural Information Processing Systems 32 (NeurIPS), pp. 8024–8035 (2019)
[28] Moritz, P., Nishihara, R., Wang, S., et al.: Ray: a distributed framework for emerging AI applications.
     In: Proc. 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI), pp.
     561–577. USENIX Association (2018)
[29] Grattafiori, A., Dubey, A., Jauhri, A., et al.:      The Llama 3 herd of models. arXiv preprint
     arXiv:2407.21783 (2024)
[30] Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C.H., Gonzalez, J.E., Zhang, H., Stoica,
     I.: Efficient memory management for large language model serving with PagedAttention. In: Proc.
     29th Symposium on Operating Systems Principles (SOSP), pp. 611–626. ACM (2023). doi:10.1145/
     3600006.3613165
[31] de Moura, L., Bjørner, N.: Z3: an efficient SMT solver. In: Proc. 14th Int. Conf. on Tools and Algo-
     rithms for the Construction and Analysis of Systems (TACAS). LNCS, vol. 4963, pp. 337–340. Springer,
     Heidelberg (2008). doi:10.1007/978-3-540-78800-3_24




                                                    12
