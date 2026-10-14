                                         Petri Nets-based Methods on Automatically Detecting for
                                         Concurrency Bugs in Rust Programs
                                         KAIWEN ZHANG and GUANJUN LIU∗ , Tongji university, China
                                         Rust’s memory safety guarantees, notably ownership and lifetime systems, have driven its widespread
                                         adoption. Concurrency bugs still occur in Rust programs, and existing detection approaches exhibit significant
                                         limitations: static analyzers suffer from context insensitivity and high false positives, while dynamic methods
                                         incur prohibitive runtime costs due to exponential path exploration. This paper presents a Petri net-based
arXiv:2212.02754v3 [cs.PL] 23 Sep 2025




                                         method for efficient, precise detection of Rust concurrency bugs. The method rests on three pillars: (1) A syntax-
                                         preserving program-to-Petri-net transformation tailored for target bug classes; (2) Semantics-preserving state
                                         compression via context-aware slicing; (3) Bug detection through efficient Petri net reachability analysis.
                                            The core innovation is its rigorous, control-flow-driven modeling of Rust’s ownership semantics and
                                         synchronization primitives within the Petri net structure, with data operations represented as token movements.
                                         Integrated pointer analysis automates alias identification during transformation. Experiments on standard Rust
                                         concurrency benchmarks demonstrate that our method outperforms the state-of-the-art methods LockBud
                                         and Miri that are both tools of detecting concurrency bugs of Rust programs. Compared to LockBud, our
                                         approach reduces false positives by 35.7% and false negatives by 28.3% , which is obtained through our precise
                                         flow-sensitive pointer analysis. Compared with Miri that is a dynamic analysis tool, although Miri can obtain
                                         the same detection results, our method achieves 100× faster verification speed since our method takes a state
                                         reduce algorithm.
                                         CCS Concepts: • Software and its engineering; • Security and privacy → Trust frameworks;
                                         Additional Key Words and Phrases: Concurrent bugs, Petri Net, Rust Language
                                         ACM Reference Format:
                                         Kaiwen Zhang and Guanjun Liu. 2024. Petri Nets-based Methods on Automatically Detecting for Concurrency
                                         Bugs in Rust Programs. 1, 1 (September 2024), 26 pages. https://doi.org/XXXXXXX.XXXXXXX

                                         1    Introduction
                                         Concurrent programming is essential for modern software performance but introduces non-
                                         deterministic defects-data races that evade traditional testing. Rust addresses this via its ownership
                                         system, where the borrow checker statically enforces memory safety and thread safety [11, 16].
                                         This eliminates entire vulnerability classes without runtime overhead.
                                            However, Rust’s guarantees remain bounded:Its type system cannot prevent high-level con-
                                         currency logic errors—deadlocks from cyclic lock dependencies, atomicity violations in different
                                         execution paths, or data races in unsafe blocks—which persist despite memory safety. Empirical
                                         evidence confirms that unsafe code blocks bypassing compiler checks proliferate in real-world
                                         Rust crates [8, 28], reintroducing precisely the vulnerabilities Rust aims to eliminate. Concurrency
                                         bug detection divided into static and dynamic analysis: Static methods identify bugs via prede-
                                         fined models such as lock graphs for deadlock detection or refinement types in theorem proving,
                                         Authors’ Contact Information: Kaiwen Zhang, zhangkw@tongji.edu.cn; Guanjun Liu, liuguanjun@tongji.edu.cn, Tongji
                                         university, Shanghai, China.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
                                         full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM XXXX-XXXX/2024/9-ART
                                         https://doi.org/XXXXXXX.XXXXXXX


                                                                                                            , Vol. 1, No. 1, Article . Publication date: September 2024.
2                                                                                         Zhang and Liu.


yet suffer either high false positives due to oversimplified semantics (e.g., omitted control-flow
paths) in pattern-matching methods, or poor scalability from labor-intensive modeling in proof
assistants; Dynamic methods, while effective for observable runtime behaviors, incur coverage
gaps that miss deep-seated flaws. To combine the advantages of both methods, we propose a Petri
net-based method that semantic translation of program logic into net structures ensuring static
rigor and enables exhaustive state exploration via reachability graphs achieving the effectiveness of
dynamic verification. This resolves expressiveness limitations of ad-hoc models and state explosion
in dynamic analysis, all without imposing manual modeling overhead.
   However, existing Petri net-based methods [7, 10, 14, 15, 17, 23, 27] for concurrency bug detection
face three fundamental limitations:
   1. Reliance on manual modeling of program logic into nets, incurring prohibitive overhead for
industrial-scale projects. To address this problem, we propose an automated framework leveraging
Rust’s Mid-Level IR (MIR):its control-flow graph inherently exposes execution paths, where data
operations within basic blocks such as memory accesses directly map to token flows in Petri net
places/transitions. By transforming each function into a self-contained subnet and composing
the global net via call-graph topology, we establish a complete formal rule set including token
consumption/regeneration for ownership transfers and lifetime constraints proven via equiva-
lence to preserve Rust’s compile-time safety guarantees while enabling fully equivalent semantic
transformations.
   2. The reliance on non-trivial extensions for data race detection via token-to-memory mappings
drastically increases complexity. Using base Petri nets necessitates transforming each data operation
individually, causing exponential net growth—a state explosion problem mirroring dynamic analysis:
while dynamic methods suffer from combinatorial path explosion, Petri nets face marking-space
explosion from model scaling. Our dual-strategy solution addresses this by:(1) Unsafe-centric
transformation, selectively mapping only unsafe block data operations to places and extracting
race-sensitive memory accesses via control-flow analysis, avoiding full-statement conversion; (2)
Control-flow-driven state compression, merging synchronization-independent paths via program
slicing and applying partial-order reduction to collapse symmetric states, reducing net size while
preserving deadlock/atomicity violation detection completeness.
   3. Inaccurate place/transition mappings during automated translation, which manifest as erro-
neous concurrent access to shared resources, primarily stem from unverified aliasing relationships
between variables accessing identical memory. Our solution introduces static alias-driven place
binding through three key mechanisms: first, integration with Rust’s compiler to coalesce poten-
tially aliased variables into identical places; second, generation of guard functions derived from
Unsafe blocks, ensuring that multiple accesses to the same resource within a basic block trigger
creation of only one identifying transition; and third, application of over-approximated analysis for
may-alias scenarios like cross-function pointer aliasing. This conservative approach intentionally
admits bounded false positives while guaranteeing the complete elimination of false negatives.
   The main contributions of this paper are as follows:
    1. The first automated translation from Rust MIR to Petri nets via ownership-semantic-preserving
       token lifecycle rules, eliminating manual modeling while ensuring equivalence.
    2. An extension-free concurrency bugs detection methodology using transition-labeling (read,write)
       in base Petri nets.
    3. A scalable verification engine integrating alias-analysis place binding and control-flow state
       compression.
 The rest of this paper is organized as follows. Section 3 gives an overview of Rust’s concurrency
model and the basic definition of Petri nets, giving a motivational example. Section 4 details the rules

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                            3


and algorithms for transforming Rust programs into Petri nets. Section 5 presents the algorithm for
concurrent bug detection based on the state reachability graph of the Petri nets. The experimental
results are presented in Section 6 to demonstrate the effectiveness of the proposed method. Section
7 concludes the paper.

2     Related Work
Despite Rust’s compile-time memory safety guarantees, empirical studies reveal that unsafe code
blocks which bypass compiler protections are pervasively adopted in real-world Rust libraries [8, 26,
28, 29], with significant portions of crates directly or transitively relying on unsafe operations even
in prominent projects where low-level optimizations necessitate such implementations. Critically,
these unsafe constructs reintroduce C/C++-style vulnerabilities including null pointer dereferences
and memory access violations—precisely the risks Rust aims to eliminate. Static analyzers address
memory safety issues but neglect concurrency vulnerabilities: Rudra [2] detects unsafe API misuse
through pattern matching, Mir-Checker [13] employs MIR-based symbolic execution to identify
memory errors, and SafeDrop [6] utilizes path-sensitive data flow analysis for ownership bugs.
   Specialized concurrency tools face inherent limitations: Miri’s [18] dynamic analysis achieves
precise data race detection via happens-before tracking but incurs prohibitive 𝑂 (𝑛 2 ) thread inter-
leaving overhead, restricting practical use to ≤ 4 threads while failing to detect unexplored-path
deadlocks. Conversely, Lockbud’s [20, 21] static lock-graph approach predicts deadlocks but gener-
ates false positives/negatives due to inadequate path-sensitive alias analysis at synchronization
points. Formal method adaptations struggle with Rust-specific challenges: theorem provers like
Prusti [1], RustBelt [9] and Krust [25] require substantial code annotation overhead for refinement-
type proofs, while model checkers suffer state explosion exacerbated by ownership semantics when
naively translating to LLVM IR.
   Consequently, Rust concurrency verification persistently confronts dual challenges: (1) static
analysis complexity, where pointer-analysis-dependent techniques require model restructuring for
distinct bug patterns such as lock graphs needing redesign for condition variables, with existing
models lacking native concurrency semantics support and thus forcing heuristic approximations in
detection algorithms that degrade precision and induce high false positives[3, 4, 12, 19]; and (2)
dynamic analysis limitations, as execution-dependent methods exhibit insufficient path coverage
for long-running tasks[5, 22], systematically omitting potential deadlocks in unexplored states.

3     Background and Motivation
3.1    Rust Concurrency Model
Rust’s core safety mechanisms, particularly its ownership system and lifetime management, ensure
memory safety at compile time. The ownership system operates on three fundamental rules: (1)
Each value has a single owner; (2) Ownership moves when reassigned, invalidating the original
variable; (3) Data access occurs through borrowing, with immutable references allowing shared
access or mutable references for exclusive modification. For example:
let s1 = String::from("hello");
let s2 = s1; // Ownership moves to s2, s1 becomes invalid
Complementing ownership, lifetimes (’a) are compile-time annotations that manage reference
validity, preventing dangling pointers by ensuring references don’t outlive their data:
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    // Returned reference valid within 'a lifetime scope
}

                                                           , Vol. 1, No. 1, Article . Publication date: September 2024.
4                                                                                           Zhang and Liu.


  Rust’s concurrency model builds upon these foundations through thread-level parallelism using
std::thread, regulated by Send and Sync traits that govern cross-thread data transfer and sharing.
The Send trait allows ownership transfer between threads, while Sync permits concurrent access
through immutable references:
// Arc<T> implements Sync for shared immutable access
let data = Arc::new(Mutex::new(0));
Despite these compile-time checks, concurrency bugs like deadlocks or atomicity violations under
relaxed memory orderings (e.g., Relaxed) can still occur when synchronization primitives are
misused.
   Our analysis leverages Rust’s Mid-level Intermediate Representation (MIR), which simplifies pro-
gram syntax while preserving control flow and concurrency semantics. MIR decomposes programs
into basic blocks representing discrete execution states, with concurrent program state modeled
as their aggregation. This abstraction provides the foundation for detecting concurrency error
patterns:
// MIR representation captures control flow and state transitions
bb0: {
    _1 = 42;                 // State assignment
    _2 = lock(_1);           // Concurrency operation
    ...
}

3.2    Petri Net
A net is a 3-tuple 𝑁 = (𝑃,𝑇 , 𝐹 ), where 𝑃 is a finite set of places, 𝑇 is a finite set of transitions,
𝐹 ⊆ (𝑃 ×𝑇 ) ∪ (𝑇 × 𝑃) is a finite set of arcs, and 𝑃 ∩𝑇 = ∅. A net can be viewed as a directed bipartite
graph where places are represented by circles and transitions by rectangles. The pre-set and post-set
of a node 𝑥 ∈ {𝑃 ∪ 𝑇 } are define as •𝑥 = {𝑦 ∈ 𝑃 ∪ 𝑇 |(𝑦, 𝑥) ∈ 𝐹 } and 𝑥 • = {𝑦 ∈ 𝑃 ∪ 𝑇 |(𝑥, 𝑦) ∈ 𝐹 },
respectively. In this paper, it is assumed that the weight of each directed arc is 1, that is, the
firing of a transition consumes or generates only one token in a connected place. A marking of
𝑁 = (𝑃,𝑇 , 𝐹 ) is a mapping 𝑀 : 𝑃 → N where 𝑀 (𝑝) is the number of tokens in place 𝑝. A net 𝑁
with an initial marking 𝑀0 is called a Petri Net and denoted as (𝑁 , 𝑀0 ). Transition 𝑡 is enabled at
𝑀 if ∀𝑝 ∈•𝑡 : 𝑀 (𝑝) > 0, denoted as 𝑀 [𝑡⟩. A marking 𝑀 is a deadlock if any transition is disabled
                                                                             ′
at 𝑀. Firing an enabled transition 𝑡 yields a new marking 𝑀 ′ : 𝑀 (𝑝) = 𝑀 (𝑝) − 1 if 𝑝 ∈• 𝑡\𝑡 • ;
𝑀 (𝑝) = 𝑀 (𝑝) + 1 if 𝑝 ∈𝑡 \ 𝑡; and otherwise 𝑀 (𝑝) = 𝑀 (𝑝). This is denoted as 𝑀 [𝑡⟩𝑀 ′ . A marking
   ′                           •  •                    ′

𝑀𝑘 is reachable from 𝑀 if 𝑀𝑘 = 𝑀 or there exists a non-empty transition sequence 𝜎 = 𝑡 1𝑡 2 . . . 𝑡𝑘
such that 𝑀 [𝑡 1 ⟩𝑀1 [𝑡 2 ⟩ . . . 𝑀𝑘 −1 [𝑡𝑘 ⟩𝑀𝑘 (abbreviated as 𝑀 [𝜎⟩𝑀𝑘 ). All markings reachable from 𝑀0
in a Petri net is written as M.
   The dynamic behavior of a Petri net is captured through its reachability graph, which is a directed
graph 𝑅𝐺 = (𝑉 , 𝐸) defined as follows:
      • 𝑉 is the set of all reachable markings M starting from the initial marking 𝑀0 , i.e., 𝑉 = M.
      • 𝐸 is the set of directed edges labeled with transitions 𝑡 ∈ 𝑇 , where (𝑀, 𝑡, 𝑀 ′ ) ∈ 𝐸 if and only
        if 𝑀 [𝑡⟩𝑀 ′ .
The reachability graph provides a systematic way to explore all possible states (markings) of a Petri
net and the transitions between them. Each node in 𝑅𝐺 corresponds to a marking, and each directed
edge represents the firing of a transition leading from one marking to another. If the reachability
graph contains a cycle, it indicates the potential for repeated execution of certain transitions.

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                            5


3.3    A Motivating Example
To detect concurrency bugs using Petri nets, the Rust program is first translated into a Petri net.
This transformation is based on Rust’s MIR, which simplifies the control flow and concurrency
constructs. Using the Petri net, a reachability graph is generated to systematically explore all
possible program states and identify bug patterns. The Fig. 1 provides a complete example, showing
the source code, its corresponding MIR and Petri net representation, and the reachability graph
with identified bug patterns such as deadlock, atomicity violation, and data race. Additionally, the
MIR in Fig. 1 only includes the parts relevant to concurrency constructs; a complete MIR example
can be found at https://play.rust-lang.org/?version=stable&mode=debug&edition=2021.
   The Rust program in the upper left portion of Fig. 1 demonstrates multiple concurrency con-
structs, including atomic variables, mutexes, and unsafe global variable access. This program
illustrates potential concurrency issues that are modeled in the corresponding MIR and Petri net
representations. Key concurrency bugs in the program are identified as follows:

   Deadlock: A potential deadlock occurs in the spawned thread. Specifically, the second call to
lock_clone.lock() inside the closure attempts to acquire the mutex while the same thread already
holds the lock. If another thread attempts to access the same mutex, a circular waiting condition
may arise, leading to a deadlock.

  Atomicity Violation: The use of atomic_var.store() and atomic_var.load() with Ordering::Relaxed
creates an atomicity violation. Relaxed memory ordering allows reordering of operations, which
may cause inconsistent or unexpected behavior when threads read or write the atomic variable.
This is particularly relevant in the main thread when the value of atomic_var is checked.

  Data Race: Unsafe access to the global variable GLOBAL_DATA introduces a data race. Since
GLOBAL_DATA is accessed and modified without synchronization in both the spawned thread and
the main thread, multiple threads can concurrently read and write to it. This leads to undefined
behavior and violates Rust’s safety guarantees. These issues are captured and analyzed in the
Petri net representation and the corresponding reachability graph, as shown in the Fig. 1. The
reachability graph highlights states where these bugs manifest, such as the deadlock state and
paths leading to atomicity violations or data races.

4     Methodology
Rust concurrency errors mainly stem from uncontrolled contention on shared resources, including
deadlocks, atomicity violations, and synchronization failures. Crucially, synchronization primitive
operations occur in the terminator statement of the MIR basic block - the final instruction to which
the control flow jumps, such as lock acquisition/release, atomic variable access. This allows us to
focus on the terminator to capture synchronization points. However, for data race issues that may
involve unsafe memory operations, we rely on explicitly marked Unsafe blocks in the Rust source
code. When an Unsafe context is detected, the entire basic block is scanned to identify all memory
access patterns and pointer operations.
  To unify the semantics of control flow and resource interaction, we propose a program Petri
net (PPN), a labeled extension of the basic Petri net. PPN solves two key problems through static
analysis techniques: (1) parsing concurrency primitives (such as thread spawn, join, and resource
scope) from the API call pattern of MIR; (2) identifying shared resource aliases through pointer
analysis. This dual analysis ensures accurate modeling of inter-thread synchronization and shared
memory dependencies.

                                                           , Vol. 1, No. 1, Article . Publication date: September 2024.
6                                                                                                                                                                                                            Zhang and Liu.


    1. static mut GLOBAL_DATA: usize = 0;                                                                                                                  Petri Net
    2.
                                                                                                                                           p0              main_start                p11            closure_start
    3. fn main() {
    4.    let atomic_var = Arc::new(AtomicUsize::new(0));                                             MIR:main                             t0                                        t11                     MIR:closure
    5.    let lock = Arc::new(Mutex::new(0));                                                                 bb0                          p1                                        p12                            bb0
    6.    atomic_var.store(1, Ordering::Relaxed);                                                                                 bb0
                                                                                                               ...                         t1                                                                        ...
                                                                                                                                                                                     t12
    7.    let lock_clone = Arc::clone(&lock);                                              line 6             bb5                                                                                                   bb2        line 10
    8.    let atomic_clone = Arc::clone(&atomic_var);                                                                                      p2                                        p13
                                                                                                               ...                                                                                                   ...
    9.    let handle = thread::spawn(move || {                                                                                                                                       t13
                                                                                           line 9             bb8                          t2                                                                       bb4        line 11
    10.      let mut lock_data = lock_clone.lock().unwrap();                                                                                                                                                         ..
                                                                                                                                           p3                              Atomic    p14
    11.      atomic_clone.store(2, Ordering::Relaxed);                                                        bb9                          t3                                        t14                            bb7        line 12
    12.      let mut lock_data = lock_clone.lock().unwrap();                                                                                                                                                         ..
    13.      unsafe {                                                                     line 17             bb10                         p4                                p21     p15                            bb15




                                                                                                                                               
    14.         GLOBAL_DATA = 42;                                                                                                                                                    t15                             ..
    15.      }                                                                                                                             t4
                                                                                                              bb11                                                                                                  bb9
    16. });                                                                                                                                p5                 p22         Mutex      p16
    17. let atomic_value = atomic_var.load(Ordering::Relaxed);                                                                     t5                t6                              t16
                                                                                                 bb12                 bb13                                                                                          bb10       line 14
    18. if atomic_value == 2 {
    19.      unsafe {
                                                                                                        ...                       p6                 p7                              p17
                                                                                          line 27             bb14                                                                   t17                            bb11
    20.         GLOBAL_DATA = 24;                                                                                                t7                   t8
                                                                                                               ...
    21.      }
                                                                                                              bb18                        p8                                         p18
    22. } else {
                                                                                                                                          t9                        p23              t18
    23.      unsafe {
    24.         GLOBAL_DATA = 24;                                                                                                         p9                          global data    p19
    25.      }
    26. }                                                                                                                                 t10                                            t19
    27. handle.join().unwrap();                                                                                                           p10              main_end                  p20            closure_end
    28. }
                                                                                            t2 , t3 , t11 , t12 , t13
                     p8 , p13 , p21 , p22 . p23              p2 , p14 , p21 , p22 , p23                                      p4 , p14 , p21 , p23
                                                                                                                                                                                         p6 , p18                   p7 , p18
                                     t13                                                                                                       t14
     No enabled                                                                                         t4
                       p8 , p14 , p21 , p23                     p5 , p15 , p21 , p23                                         p4 , p15 , p21 , p23
     transitions                                                                                                                                                                    t7              t18

                          Deadlock                                                Atomic Violation                                                                                              Data Race
                                                                         State Reachable Graph


                                       Fig. 1. Illustration: Rust Code, MIR, Petri Net, and Bug Detection



                                                        RustC                                                        Transformer                                                     Optimization
                    Rust                                                                                                                 bb0                                  1. CallGraph: Remove Non-
                   Source                         Construct CallGraph                                                                                                                Conc Instance
                                                                                                                                                     bb2
                    Code                                                                                                         bb1
                                                                                                                                                     bb3
                                                                                                                                                                              2. MIR: Merge P-T Chains

                                                                                                                                         bb4                                                Generate
                                                      Mono MIR                                  CallGraph                                                                            State Reachable Graph
                                                                                                                                        MIR
                                                  Control Dependence                                 bb2 -> [return: bb3, unwind: bb8];
                                                                                          _6 = Result::<MutexGuard<'_, ()>, _>::unwrap(move _7)                                          External Tools: Tina/Lola/Pnml
               Detected
                                                                                                              bb2                  bb8                                                  Deadlock,
               Bug Kind
                                                    Static Analysis                                                                                                                 Atomicity Violation,
                                                  Lock/Atomic/Unsafe                                          bb3        Mutex                                                          Data Race


                                      User Interface                                                    Mapping to Petri Nets                                                                  Bug Detection


                                                                   Fig. 2. The framework of PPN


  The constructed PPN is streamlined to eliminate redundant states and transitions, improving
analyzability while retaining the core behavioral semantics. The optimized net generates a reach-
ability graph that supports systematic exploration of concurrent execution paths to detect bug
modes such as deadlock, atomicity violation, and data race. Figure 2 shows the entire process from
MIR extraction to detect bugs.

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                             7


4.1     Program Representation
We formally define a Rust program as a 6-tuple:
                                        Prog = (F , 𝐺 call, CF G, Σ, D, 𝜄)
where each component is specified as follows:
      1. Function Set F : The set of monomorphized functions
                                          F = {𝑓1,...,𝑛 | 𝑓 ∈ Decl} ∪ C
         where 𝑓1,...,𝑛 denotes generic functions instantiated with concrete types, C represents closure
         instances with captured environments.
      2. Call Graph 𝐺 call = (F , 𝐸 Λ ) with context-labeled edges:
                      𝐸 Λ ⊆ F × 𝐸𝑡 × F ,      𝐸𝑡 = {spawn, join, scope, normal_call}
      3. Control flow graph CF G = {(𝑏𝑏 𝑓 , 𝛿 𝑓 , 𝜇 𝑓 )} 𝑓 ∈ F with 𝑏𝑏 𝑓 basic blocks,
         𝛿 𝑓 ⊆ 𝑏𝑏 𝑓 × {𝑆𝑤𝑖𝑡𝑐ℎ, 𝐺𝑜𝑡𝑜, . . . , 𝑅𝑒𝑡𝑢𝑟𝑛} ×𝑏𝑏 𝑓 , and 𝜇 𝑓 : 𝑏𝑏 𝑓 → Σ∗ satisfying ∀𝑏 ∈ 𝑏𝑏 𝑓 , 𝜇 𝑓 (𝑏) =
         𝑠 1 ; . . . ; 𝑠𝑛 ∧ 𝑠𝑛 ∈ Termination.
      4. Statement with Termination Σ defined inductively:
               Σ ::= 𝐶𝑎𝑙𝑙 (𝑓 )   (𝑓 ∈ F )
                      | 𝐿𝑜𝑐𝑘 (𝑚, 𝜅) | 𝑈 𝑛𝐿𝑜𝑐𝑘 (𝑚)     (𝑚 ∈ {𝑀𝑢𝑡𝑒𝑥, . . .}, 𝜅 ∈ {𝑙𝑜𝑐𝑘, 𝑟𝑒𝑎𝑑, . . .})
                      | 𝐴𝑡𝑜𝑚𝑖𝑐 (𝑜𝑟𝑑)     (𝑜𝑟𝑑 ∈ {𝑅𝑒𝑙𝑎𝑥𝑒𝑑, 𝑆𝑒𝑞𝐶𝑠𝑡, . . .})
                      | 𝑈 𝑛𝑠𝑎𝑓 𝑒 (op)   (𝑜𝑝 ∈ {𝑢𝑠𝑒, 𝑎𝑑𝑑𝑟𝑒𝑠𝑠, . . .)
      5. Data Domain D = (M, A, U) where M is the set of synchronization resources, A is the set
         of atomic variables, U is the set of unsafe data.
      6. Entry Point 𝜄 = (main, Γ0 ) with: Γ0 = (api0, heap0, panic_handler).
   It is important to note that the current version of Rust is still evolving, and many advanced
features may not yet be fully supported by available tools, such as the latest language constructs
or specific library functions. As a result, while our approach captures a large portion of Rust’s
core features, it deliberately omits niche syntax such as procedural macros or inline assembly to
ensure the accuracy and feasibility of the conversion process through a simplified subset. This
subset focuses exclusively on concurrency-critical elements, enabling rigorous conversion rules
that maintain semantic correctness while reducing complexity.
   Within this methodology, we initially aggregate all monomorphized functions produced post-
trait resolution to resolve generic types. Subsequently, we traverse this collection to construct
an inter-procedural call graph. Given our focus on concurrency bug detection, function calls are
categorically classified into concurrent calls and normal calls. The former abstracts thread control
primitives including scope, spawn, and join as unified thread forking and synchronization actions.
During call graph construction, we concurrently instrument basic blocks to monitor accesses to
shared variables, specifically non-atomic mutable globals, alongside unsafe data operations. These
observed patterns directly map to the targeted bug types. Furthermore, since Petri nets necessitate
an initial state, we designate the program entry point, typically the main function, as the root node.
Thread-spawning actions generate parallel transitions, while shared access points induce state
conflicts. This methodology deliberately prioritizes verification tractability above full-language
coverage, ensuring practical scalability, formal soundness in model translation, and adaptability
to Rust’s evolution through extensible annotation rules. Consequently, it enables comprehensive
concurrent bug detection while minimizing ambiguities.

                                                            , Vol. 1, No. 1, Article . Publication date: September 2024.
8                                                                                               Zhang and Liu.


4.2     Program Petri Net
The PPN extends classical Petri nets by explicitly distinguishing between control flow and resource
operations. This partitioning enables PPN to represent the dual nature of Rust programs, where
control flow is governed by both sequential and concurrent transitions, and resource access is
mediated through synchronization primitives, atomic variables, and unsafe operations. Notably,
the incorporation of concurrency control transitions, which are associated with concurrency APIs,
provides an important advantage: it allows us to identify functions that may execute concurrently. Its
core innovation is that by binding control transitions to concurrent APIs, potential parallel execution
domains are essentially identified, thereby automatically and accurately identifying concurrent
function boundaries. In contrast, Lock-Graph assume that function calls are completely unordered
interactions, which can easily produce high false positives due to path over-approximation; PPN
uses the partial order modeling capability of Petri nets to explicitly characterize the dynamic
interaction of thread forks, order constraints of synchronization events, and resource conflicts,
fundamentally avoiding such false positives while maintaining verification scalability.


    Definition 1. A PPN is a 5-tuple (𝑃,𝑇 , 𝐹, 𝑀,𝑊 ) where:

      1. 𝑃 = 𝑃𝑐 ∪ 𝑃𝑟 represents the finite set of places: 𝑃𝑐 represent control places (program state nodes)
         while 𝑃𝑟 represent resource places (shared variables/resources).
                                                                                       seq                 seq
      2. 𝑇 = 𝑇𝑐 ∪ 𝑇𝑜 represents the finite set of transitions, specifically: 𝑇𝑐 = 𝑇𝑐 ∪ 𝑇𝑐conc where 𝑇𝑐
         represent sequential control operations (e.g., conditionals, loops) and 𝑇𝑐conc represent concurrency
                                    sync            unsafe         sync
         control operations; 𝑇𝑜 = 𝑇𝑜 ∪𝑇𝑜atom ∪𝑇𝑜           where 𝑇𝑜 represent synchronization primitives,
                                                    unsafe
         𝑇𝑜atom represent atomic operations, and 𝑇𝑜        represent unsafe memory operations such as raw
         pointer dereference.
      3. 𝐹 ⊆ (𝑃 ×𝑇 ) ∪ (𝑇 × 𝑃) represents the directed arcs, partitioned into control arcs 𝐹𝑐 ⊆ (𝑃𝑐 ×𝑇𝑐 ) ∪
         (𝑇𝑐 × 𝑃𝑐 ) and resource-operator arcs 𝐹𝑟𝑜 ⊆ (𝑃𝑟 × 𝑇𝑜 ) ∪ (𝑇𝑜 × 𝑃𝑟 ).
      4. 𝑀 : 𝑃 → N represents the marking function with 𝑀 (𝑝) denoting token count at place 𝑝, where
         𝑀0 specifies the initial marking.
      5. 𝑊 : 𝐹 → N+ represents the weight function assigning positive integers to arcs.


4.3     Transformation from Rust Program to PPN
The PPN-based modeling of Rust’s concurrency APIs employs a three-layer translation framework
leveraging control flow isomorphism () between CFGs and PPNs, preserving basic block semantics
with minimal overhead:

      1. CFG conversion bijectively maps each basic block to control place 𝑝𝑏 ∈ 𝑃𝑐 representing
         program counter states during execution;
      2. Terminator-driven transition typing generates categorized transitions: branch terminators
                                                                             𝑠𝑦𝑛𝑐
         such as 𝑠𝑤𝑖𝑡𝑐ℎ𝐼𝑛𝑡, synchronization primitives instantiate 𝑇𝑜             with exclusion semantics,
                                        𝑢𝑛𝑠𝑎𝑓 𝑒
         and unsafe scopes produce 𝑇𝑜           ;
      3. Call graph-mediated inter-function linking transforms invocations into transitions: concur-
         rent calls enable parallel token flow to 𝑝𝑒𝑛𝑡𝑟 𝑦 𝑓 via 𝑇𝑐𝑐𝑜𝑛𝑐 , while sequential calls enforce token
         propagation through 𝑝𝑏 ′ .

    Let T : Prog → 𝑃𝑃𝑁 be the transformation function. We formalize thread operations as:

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                                                9


4.3.1 CFG Structural Mapping (Intra-function). For each function 𝑓 ∈ F with CF G 𝑓 = (𝑏𝑏 𝑓 , 𝛿 𝑓 , 𝜇 𝑓 ):
                    T (𝑓 ) = (𝑃 𝑓 ,𝑇𝑓 , 𝐹 𝑓 )         where:
                                 𝑓        𝑓
                        𝑃 𝑓 = {𝑝 start, 𝑝 end } ∪ {𝑝𝑏 | ∀𝑏 ∈ 𝑏𝑏 𝑓 }
                        𝑇𝑓 = {𝑡𝑏 | ∀𝑏 ∈ 𝑏𝑏 𝑓 } ∪ {𝑡𝛿 | ∀𝛿 ∈ 𝛿 𝑓 }
                                       𝑓                          𝑓
                                                                                       Ø
                                                       𝑏 ret
                        𝐹 𝑓 = {(𝑝 start, 𝑡𝑏 0 )} ∪ {(𝑡 ret   , 𝑝 end )}           ∪             {(𝑝𝑏 , 𝑡𝑏 ), (𝑡𝑏 , 𝑝𝑏 ′ )}
                                                                                      𝑏 ∈𝑏𝑏 𝑓

  The transformation T converts a function 𝑓 ’s CF G 𝑓 = (𝑏𝑏 𝑓 , 𝛿 𝑓 , 𝜇 𝑓 ) into a subnet of PPN
                                                                                                                                     𝑓
(𝑃 𝑓 ,𝑇𝑓 , 𝐹 𝑓 ) through element-wise mapping: the control places 𝑃 𝑓 include the function entry 𝑝 start
                𝑓
and exit 𝑝 end augmented by distinct places 𝑝𝑏 for each basic block 𝑏 ∈ 𝑏𝑏 𝑓 ; the transitions 𝑇𝑓
consist of block activation transitions 𝑡𝑏 for every 𝑏 ∈ 𝑏𝑏 𝑓 combined with terminator transitions 𝑡𝛿
                                                                                                           𝑓
encoding control flow decisions in 𝛿 𝑓 ; the arcs 𝐹 𝑓 establish connectivity initiating from (𝑝 start, 𝑡𝑏 0 )
                                             𝑏 ret     𝑓
for the entry block, terminating at (𝑡 ret         , 𝑝 end ) for return points, and chaining intra-block sequences
via {(𝑝𝑏 , 𝑡𝑏 ), (𝑡𝑏 , 𝑝𝑏 ′ )} pairs that preserve CFG topology through rigorous place-transition corre-
spondence, thus ensuring structural congruence between CFG paths and PPN firing sequences.
4.3.2   Call Graph Mapping (Inter-function).
  Definition 2 (Core Transformation Tcall ).
                                               (
                                                𝑡𝜏 ∈ 𝑇𝑐𝜏
                  Tcall (𝛿 call, 𝑝𝑏 , 𝑝𝑏 ′ ) =
                                                 𝐹𝑐 ← 𝐹𝑐 ∪ Φ𝜏 (𝑝𝑏 , 𝑝 start, 𝑝 end, 𝑝𝑏 ′ )
                                                                      𝑓        𝑓


where 𝜏 = 𝜏 (𝛿 call ) and:
              ΦNormal = {(𝑝𝑏 , 𝑡𝜏 ), (𝑡𝜏 , 𝑝 start ), (𝑝 end, 𝑡 ret ), (𝑡 ret, 𝑝𝑏 ′ )}
                                                  𝑓         𝑓


              ΦSpawn = {(𝑝𝑏 , 𝑡𝜏 ), (𝑡𝜏 , 𝑝 start ), (𝑝 end, ⊥)}
                                                  𝑓         𝑓


                 ΦJoin = {(𝑝 end, 𝑡𝜏 ), (𝑡𝜏 , 𝑝𝑏 ′ )}
                                 𝑓

                              𝑛
                                                                         !                              𝑛
                              Ø                                                                         Ø
                ΦScope =             ΦSpawn (𝑝𝑏 , 𝑝 start
                                                    𝑓𝑖        𝑓𝑖                                                    𝑓
                                                          , 𝑝 end , ⊥)       ∪ {(𝑡 sync, 𝑝𝑏 ′ )} ∪             {(𝑝 end
                                                                                                                    𝑖
                                                                                                                       , 𝑡 sync )}
                              𝑖=1                                                                        𝑖=1

   The transformation Tcall formalizes the mapping through a type-driven methods 𝜏 (𝛿 call ) that
classifies call operations into four categories: Normal (synchronous function calls), Spawn (thread
creation), Join (thread synchronization), and Scope (parallel scopes). For each type 𝜏, it generates
a specialized transition 𝑡𝜏 ∈ 𝑇𝑐𝜏 and extends the arc set 𝐹𝑐 via arc generator Φ𝜏 . Specifically: for
Normal calls, ΦNormal creates sequential path 𝑝𝑏 → 𝑡𝜏 → 𝑝 start initiating callee execution followed
                                                              𝑓
                  𝑓
by return path 𝑝 end → 𝑡 ret → 𝑝𝑏 ′ ensuring control returns to post-call block; for Spawn operations,
ΦSpawn establishes concurrent path 𝑝𝑏 → 𝑡𝜏 → 𝑝 start launching parallel thread while marking callee
                                                                  𝑓

exit with ⊥ denoting detached termination; for Join synchronization, ΦJoin constructs blocking
path 𝑝 end → 𝑡𝜏 → 𝑝𝑏 ′ requiring thread completion token to proceed; for Scope constructs, ΦScope
        𝑓

combines parallel spawn arcs 𝑛𝑖=1 ΦSpawn with barrier synchronization 𝑛𝑖=1 (𝑝 end
                                 Ð                                          Ð      𝑓𝑖
                                                                                      → 𝑡 sync ) →
𝑝𝑏 ′ enforcing all scoped threads complete before exit. This unified transformation preserves: 1)
call-return semantics via 𝑡 ret sequencing; 2) asynchronous parallelism via ⊥-terminated paths;
3) blocking synchronization via 𝑡𝜏 ’s enabling condition; 4) collective synchronization via 𝑡 sync ’s
barrier semantics—all while maintaining structural congruence between CFG paths and PPN firing
sequences.

                                                                             , Vol. 1, No. 1, Article . Publication date: September 2024.
10                                                                                                     Zhang and Liu.

                                                                                 𝑠𝑦𝑛𝑐
                                                     𝑃 ← 𝑃𝑟 ∪ 𝑝𝑚𝑢𝑡𝑒𝑥
                                                                    ( , 𝑡 ∈ 𝑇𝑜 , 𝑀 [𝑝𝑚𝑢𝑡𝑒𝑥 ] ← 1
                                                     𝑟
                                                    
                                                    
                                                    
4.3.3 Lock and Unlock Operations. T (mutex) =                        {(𝑝𝑚𝑢𝑡𝑒𝑥 , 𝑡)}, if mutex = lock
                                                     𝐹𝑟𝑜 ← 𝐹𝑟𝑜 ∪ {(𝑡, 𝑝𝑚𝑢𝑡𝑒𝑥 )}, if mutex = drop
                                                    
                                                    
                                                    
A mutex resource 𝑝𝑚𝑢𝑡𝑒𝑥 is created and initialized with a token (𝑀 [𝑝𝑚𝑢𝑡𝑒𝑥 ] = 1). For a lock oper-
ation, the token is transferred from 𝑝𝑚𝑢𝑡𝑒𝑥 to the lock transition 𝑡, and for a drop operation the
token is returned. This enforces exclusive access.
                                                                                    𝑠𝑦𝑛𝑐
                                                     
                                                     
                                                      𝑃𝑟 ← 𝑃𝑟 ∪ 𝑝𝑟 𝑤𝑙𝑜𝑐𝑘 , 𝑡 ∈ 𝑇𝑜 , 𝑀 [𝑝𝑟 𝑤𝑙𝑜𝑐𝑘 ] ← 𝑛
                                                                                  , 𝑡, 1)}, if rwlock = read
                                                     
                                                                     {(𝑝
                                                     
                                                     
                                                                      𝑟 𝑤𝑙𝑜𝑐𝑘
                                                                     
4.3.4 Read-Write Lock Operations. T (rwlock) =                       
                                                                     
                                                      𝐹 𝑟𝑜 ← 𝐹 𝑟𝑜 ∪   {(𝑝        , 𝑡, 𝑛)}, if rwlock = write
                                                     
                                                                     𝑟 𝑤𝑙𝑜𝑐𝑘
                                                     
                                                                     {(𝑡, 𝑝𝑟 𝑤𝑙𝑜𝑐𝑘 , 𝑛)}, if rwlock = drop
                                                                     
                                                                    
Let 𝑛 ∈ 𝑁 + be the maximum number of concurrent readers allowed. The read-write lock resource
𝑝𝑟 𝑤𝑙𝑜𝑐𝑘 is initialized with 𝑛 tokens. A read operation consumes 1 token allowing up to 𝑛 concurrent
readers, while a write operation consumes all 𝑛 tokens for exclusive access. The drop operation
returns the tokens.
4.3.5 Condition Variables Operations. Condvar(lock) represents a condition variable and the lock
resource associated with it. This transformation creates resource places for the lock (𝑝𝑙 ), condition
(𝑝𝑐𝑜𝑛𝑑 ), and waiting state (𝑝 𝑤𝑎𝑖𝑡 ). The notify operation signals by transferring a token to 𝑝𝑐𝑜𝑛𝑑 ,
while the wait operation sequences transitions (via 𝑡𝑙𝑜1 , 𝑡𝑐𝑜 , 𝑡𝑙𝑜2 ) to model a thread waiting on the
condition. This ensures proper synchronization between waiting and notification.
                        𝑃𝑟 ← 𝑃𝑟 ∪ {𝑝𝑙 , 𝑝𝑐𝑜𝑛𝑑 , 𝑝 𝑤𝑎𝑖𝑡 }, 𝑡𝑙𝑜1, 𝑡𝑙𝑜2 ∈ 𝑇𝑜𝑠𝑦𝑛𝑐 , 𝑡𝑐𝑜 ∈ 𝑇𝑜𝑠𝑦𝑛𝑐 , 𝑀 [𝑝𝑙 ] ← 1
                        
                        
                        
                        
T (condvar(lock)) = 𝐹𝑟𝑜 ← 𝐹𝑟𝑜 ∪ {(𝑡𝑐𝑜 , 𝑝𝑐𝑜𝑛𝑑 )},                                                                     nofity
                        
                         𝐹𝑟𝑜 ← 𝐹𝑟𝑜 ∪ {(𝑡𝑙𝑜1, 𝑝𝑙 ), (𝑡𝑐𝑜 , 𝑝 𝑤𝑎𝑖𝑡 ), (𝑝 𝑤𝑎𝑖𝑡 , 𝑡𝑙𝑜2 ), (𝑝𝑙 , 𝑝𝑙𝑜2, (𝑝𝑐𝑜𝑛𝑑 , 𝑝𝑙𝑜2 ))}, wait
                        
                        
                                                                                  𝑠𝑦𝑛𝑐
                                                       𝑃 ← 𝑃𝑟 ∪ 𝑝𝑐ℎ𝑎𝑛
                                                                     ( , 𝑡 ∈ 𝑇𝑜 , 𝑀 [𝑝𝑐ℎ𝑎𝑛 ] ← 𝑛
                                                       𝑟
                                                      
                                                      
                                                      
4.3.6 Bounded Channel Operation. T (channel) =                        {(𝑡, 𝑝𝑐ℎ𝑎𝑛 )}, if channel = send
                                                       𝐹𝑟𝑜 ← 𝐹𝑟𝑜 ∪ {(𝑝𝑐ℎ𝑎𝑛 , 𝑡)}, if channel = recv
                                                      
                                                      
                                                      
                                                   (
                                                     𝑃𝑟 ← 𝑃𝑟 ∪ 𝑝𝑎𝑡𝑜𝑚𝑖𝑐 , 𝑡 ∈ 𝑇𝑜𝑎𝑡𝑜𝑚𝑖𝑐 , 𝑀 [𝑝𝑎𝑡𝑜𝑚𝑖𝑐 ] ← 1
4.3.7 Atomic Variable Operations. T (atomic) =
                                                     𝐹𝑟𝑜 ← 𝐹𝑟𝑜 ∪ {(𝑡, 𝑝𝑎𝑡𝑜𝑚𝑖𝑐 ), (𝑝𝑎𝑡𝑜𝑚𝑖𝑐 , 𝑡)}
The atomic variable 𝑝𝑎𝑡𝑜𝑚𝑖𝑐 is created with a single token to guarantee atomic access. Both load and
store operations are modeled by bidirectional transitions, ensuring that operations occur atomically
and respect memory ordering.
                                           (
                                                                        𝑢𝑛𝑠𝑎𝑓 𝑒
                                             𝑃𝑟 ← 𝑃𝑟 ∪ 𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 , 𝑡 ∈ 𝑇𝑜        , 𝑀 [𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 ] ← 1
4.3.8 Unsafe Data Access. T (unsafe) =
                                             𝐹𝑟𝑜 ← 𝐹𝑟𝑜 ∪ {(𝑡, 𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 ), (𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 , 𝑡)}
Unsafe data access is modeled using a dedicated resource 𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 (initialized with a token). The
bidirectional conversions allow read and write operations on insecure data; reads and writes do
not change the state of the data.

4.4    Algorithms for Petri Net Transformation
The algorithm ?? constructs a simple program model Prog from Rust source code 𝑅𝑆𝐶 and converts
it to a PPN. It comprises two phases: Phase 1 builds the Prog by compiling 𝑅𝑆𝐶 to obtain monomor-
phized functions F , extracting the MIR into CFG for each function 𝑓 ∈ F , and iterating over all
basic blocks and statements to collect program elements such as synchronization primitives M,
atomic variables A , and unsafe data U while handling resource operations including locks, atomic

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                           11


Algorithm 1 Source-to-Prog and Prog-to-PPN Conversion
Require: Rust Source Code 𝑅𝑆𝐶
Ensure: Program Petri Net 𝑃𝑃𝑁 = (𝑃,𝑇 , 𝐹, 𝑀0,𝑊 )
 1: Phase 1: Build Prog model from source
 2: Initialize F ← ∅, 𝐺 call ← (∅, ∅), CF G ← ∅, Σ ← ∅, D ← (∅, ∅, ∅), 𝜄 ← null
 3: Compile 𝑅𝑆𝐶 to get monomorphized functions: F ← {all 𝑓𝜏1 ,...,𝜏𝑛 }
 4: for all Function 𝑓 ∈ F do
 5:     Extract MIR as CF G 𝑓 = (𝑏𝑏 𝑓 , 𝛿 𝑓 , 𝜇 𝑓 )
 6:     CF G ← CF G ∪ {CF G 𝑓 }
 7:     for all Basic block 𝑏 ∈ 𝑏𝑏 𝑓 do
 8:         for all Statement 𝑠 ∈ 𝜇 𝑓 (𝑏) do
 9:               Σ ← Σ ∪ {𝑠}
10:               if 𝑠 is resource operation then
11:                    if 𝑠 = Lock(𝑚, 𝜅) or UnLock(𝑚) then
12:                        M ← M ∪ {𝑚, 𝜅, 𝑓 , 𝑠.𝑙𝑜𝑐𝑎𝑡𝑖𝑜𝑛}                            ⊲ Add to sync primitives
13:                    else if 𝑠 = Atomic(ℓ, 𝑜𝑟𝑑) then
14:                         A ← A ∪ {𝑎, 𝑜𝑟𝑑, 𝑓 , 𝑠.𝑙𝑜𝑐𝑎𝑡𝑖𝑜𝑛}                        ⊲ Add to atomic variables
15:                    else if 𝑠 = Unsafe(𝑜𝑝) then
16:                        U ← U ∪ {𝑢, 𝑜𝑝, 𝑓 , 𝑏𝑏 𝑓 }                                   ⊲ Add to unsafe data
17:                    end if
18:               end if
19:         end for
20:         if 𝑠 term is call operation then
21:               Get callee 𝑓 𝑗 and call type 𝜆, 𝐺 call ← 𝐺 call ∪ {(𝑓 , 𝑡, 𝑓 𝑗 )}
22:         end if
23:     end for
24: end for
25: Run alias analysis on(D: D ← AliasAnalysis(D)
                                (main, Γ0 )         if binary program
26: Set entry point: 𝜄 ←
                                (API entries, Γ0 ) if library
27: Construct Prog ← (F , 𝐺 call, CF G, Σ, D, 𝜄)
28: Phase 2: Transform Prog to PPN
29: Apply Program-to-PPN Conversion (Algorithm 2) on Prog
30: return Resulting 𝑃𝑃𝑁



accesses, and unsafe statements; it then performs alias analysis on dependency data D and sets the
entry point 𝜄 based on whether the program is a binary or a library. Phase 2 invokes the Algorithm
2 to transform the constructed Prog model into the final PPN, ensuring the conversion preserves
the program’s concurrent behavior semantics for formal verification.
    This algorithm 2 transforms the Prog into a PPN by iterating over all functions 𝑓 ∈ F to add
                                      𝑓     𝑓                                             𝑓        𝑓
function entry and exit places (𝑝 entry, 𝑝 exit ) along with corresponding transitions (𝑡 start, 𝑡 return ); it
then processes each basic block 𝑏 to introduce control places (𝑝𝑏 ) and transitions (𝑡𝑏 ), connecting
them via arcs based on the control flow. Subsequent iterations handle the terminator statements
𝑠 term : if a block is marked unsafe, unsafe statements are mapped using predefined rules; otherwise,
call operations are resolved through the call graph 𝐺 call , synchronization primitives map to mutexes,
read-write locks, condition variables, or channels, and atomic operations utilize specific mapping

                                                           , Vol. 1, No. 1, Article . Publication date: September 2024.
12                                                                                                 Zhang and Liu.


Algorithm 2 Program-to-PPN Conversion
Require: Program Prog = (F , 𝐺 call, CF G, Σ, D, 𝜄)
Ensure: PPN 𝑃𝑃𝑁 = (𝑃,𝑇 , 𝐹, 𝑀0,𝑊 )
 1: Initialize 𝑃 ← ∅,𝑇 ← ∅, 𝐹 ← ∅, 𝑀0 ← ∅,𝑊 ← ∅
 2: for all Function 𝑓 ∈ F do
                                                             𝑓         𝑓
 3:     Add function entry place and return place: 𝑃 ← 𝑃 ∪ {𝑝𝑒𝑛𝑡𝑟 𝑦 , 𝑝𝑒𝑥𝑖𝑡 }
                                                               𝑓   𝑓
  4:    Add start/return transitions: 𝑇 ← 𝑇 ∪ {𝑡𝑠𝑡𝑎𝑟𝑡 , 𝑡𝑟𝑒𝑡𝑢𝑟𝑛 }
                                   𝑓     𝑓         𝑓        𝑓
 5:     Add arcs: 𝐹 ← 𝐹 ∪ {(𝑝𝑒𝑛𝑡𝑟 𝑦 , 𝑡𝑠𝑡𝑎𝑟𝑡 ), (𝑡𝑟𝑒𝑡𝑢𝑟𝑛 , 𝑝𝑒𝑥𝑖𝑡 )}
 6:     for all Basic block 𝑏 ∈ 𝑏𝑏 𝑓 do
 7:         Add control places and transitions 𝑝𝑏 : 𝑃 ← 𝑃 ∪ {𝑝𝑏 }, 𝑡𝑏 : 𝑇 ← 𝑇 ∪ {𝑡𝑏 }
 8:         Add arcs: 𝐹 ← 𝐹 ∪ {(𝑝𝑏 , 𝑡𝑏 )}
 9:     end for
                                 𝑓
10:     Add arc: 𝐹 ← 𝐹 ∪ {(𝑡𝑠𝑡𝑎𝑟𝑡 , 𝑝𝑏 0 )}
11:     for all Basic block 𝑏 ∈ 𝑏𝑏 𝑓 do
12:         if b is unsafe-marked then
13:             for all Statement 𝑠 ∈ 𝜇 𝑓 (𝑏) do
14:                   Map to resource operation using Rules 4.3.8
15:             end for
16:         else if
17:              thenLet 𝑠 term = terminator of 𝑏
18:             if 𝑠 term is a Call operation then
19:                   Add call arcs via 𝐺 call edges (Rule 4.3.2)
20:             else if 𝑠 term is a Sync primitive then
21:                   Map via Rules 4.3.3, 4.3.4, 4.3.5, 4.3.6
22:             else if 𝑠 term is an Atomic operation then
23:                   Map via Rule 5.3
24:             end if
25:         end if
26:     end for
27: end for
28: Set initial marking for entry points: ∀𝑝 ∈ 𝐴𝑃𝐼 init, 𝑀0 (𝑝) ← 1
29: return 𝑃𝑃 𝑁 = (𝑃,𝑇 , 𝐹, 𝑀0,𝑊 )




rules. Finally, the algorithm sets the initial marking 𝑀0 on entry places to represent initial program
states, generating a PPN that models data dependencies and concurrency patterns for static analysis
of program behaviors.
   The complexity of the algorithm depends on the size of the CFG, the function call graph, and the
number of resources and operations. Let |𝐵| be the number of basic blocks and |𝐸| be the number
of edges in the CFG, |𝐹 | the number of functions, and |𝑅| the number of resources, each with |𝑂 |
operations. Constructing the control flow has a complexity of 𝑂 (|𝐵| + |𝐸|), and resource operations
require 𝑂 (|𝑅| · |𝑂 |). Therefore, the overall complexity of the algorithm is 𝑂 ((|𝐵| + |𝐸|) · |𝐹 | + |𝑅| · |𝑂 |).
This complexity ensures that the algorithm is efficient and scalable for typical program sizes, making
it suitable for practical analysis of concurrent systems.

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                           13


5     Detect General Concurrency Bugs
5.1    Deadlock Detection
Deadlocks represent a critical class of concurrency bugs where threads are permanently unable to
proceed due to cyclic resource dependencies. Petri nets utilize transition firing rules to model state
changes, dynamically capturing all possible behaviors of a program. However, previous research
on deadlocks in Petri nets has focused predominantly on global deadlocks, which are defined as the
termination of the entire program. A deadlock state is defined as a state where no transitions are
enabled under non-terminal markings. For the detection of local deadlocks, more precise transition
definitions and complex logical formulas are required. Local deadlocks in the reachability graph
are often represented as cycles, where certain shared resources never receive tokens. We classify
this type of deadlock as a "deadlock class" in which some locks or resources remain perpetually
unavailable. To formalize, if there exists a cycle in the reachability graph where, within the cycle, a
resource remains at zero tokens indefinitely, we define this as a local deadlock. In our approach,
we combine the detection algorithms for these two types of deadlocks. If the program reaches a
terminal mark, the global deadlock detection method is applied. If the program does not reach a
terminal marking, the local deadlock detection method is used.
   We consider two types of deadlock pattern within our methods:
    1. A global deadlock is formally defined as a marking 𝑀 satisfying two necessary and sufficient
       conditions: (1) no transitions are enabled (Enabled(𝑀) = ∅), indicating the impossibility of any
       further state evolution, and (2) 𝑀 does not constitute a valid termination state 𝑀final – where
       termination is explicitly characterized by the concurrent fulfillment of two requirements: (i)
       complete termination of the main function’s execution, and (ii) restoration of all resource
       places to their initial token capacities (∀𝑝 ∈ 𝑃𝑟 , 𝑀 (𝑝) = Init(𝑝)); consequently, the formal
       deadlock criterion is expressed as Enabled(𝑀) = ∅ ∧ 𝑀 ≠ 𝑀final .
    2. A local deadlock denotes a partial system failure where one or more threads become indefi-
       nitely blocked due to resource contention while other threads continue normal execution—a
       condition undetectable by global deadlock methods. This manifests in three distinct scenarios:
       (1) program termination occurs without recognizing perpetually blocked threads (functionally
       resembling undetected global deadlock); (2) active threads suspend execution waiting for
       blocked threads to release resources, ultimately triggering global deadlock; or (3) the system
       enters cyclic behavior whereby it periodically revisits identical states in the reachability
       graph. Crucially, local deadlocks are formally identified in cyclic scenarios when at least one
       lock-related resource place 𝑝𝑟 exhibits persistent token starvation (∀𝑀𝑖 ∈ cycle , 𝑀𝑖 (𝑝𝑟 ) = 0)
       and never regains its initial token capacity, indicating irrevocable resource seizure preventing
       thread progression through the cycle.
This algorithm 3 employs a tiered detection architecture, prioritizing computational resources
for deadlock patterns while ensuring rare but dangerous partial deadlocks are captured. Model
reduction during preprocessing downgrades state space complexity, solving the state explosion
problem. Innovatively integrates three deadlock scenarios into a unified framework: Scenario 1
through post-termination thread resource auditing, Scenario 2 via standard global detection, and
Scenario 3 through optimized cycle analysis using SCC decomposition.

5.2    Data Race Detection
Data races in Rust manifest themselves primarily through two mechanisms: (1) explicit unsafe
operations on global static data through raw pointers; and (2) logical flaws in manually implemented
Sync traits that violate thread safety guarantees. Both patterns bypass borrow rule checks via
the Unsafe annotation, formally defined in this study as concurrent unsynchronized accesses to a

                                                           , Vol. 1, No. 1, Article . Publication date: September 2024.
14                                                                                             Zhang and Liu.


Algorithm 3 Deadlock Detection in PPN
Require: Reachability graph 𝑅𝐺 = (𝑉 , 𝐸) with |𝑀 | = 𝑛 markings,
              Resource places 𝑃𝑟 with initial capacities Init(𝑝𝑟 ), final marking classes: 𝑀 𝑓 𝑖𝑛𝑎𝑙
Ensure: Set 𝐷𝑀: global deadlocks + local deadlock cycles
 1: 𝐷𝑀 ← ∅
 2: Apply model reduction (Sec. 5.5) to compress G
 3: Phase 1: Global & Scenario 1 Detection
 4: for all 𝑀 ∈ 𝑅𝐺 do
 5:     if Enabled(𝑀) = ∅ then
 6:         if 𝑀 ∈ Mfinal then
 7:             if ∃𝑝𝑟𝑡 ∈ {• (𝑡𝑖 ), (𝑡𝑖 ) • } : 𝑀 (𝑝𝑟𝑡 ) ≠ Init(𝑝𝑟𝑡 ) then
 8:                 𝐷𝑀 ← 𝐷𝑀 ∪ {⟨𝑀, 𝑡𝑖 ⟩}                                                          ⊲ Scenario 1
 9:             end if
10:         else
11:             𝐷𝑀 ← 𝐷𝑀 ∪ {𝑀 }                                           ⊲ Global deadlock (Covers Scenario 2)
12:         end if
13:     end if
14: end for
15: Phase 2: Cycle Analysis for Scenario 3
16: Compute SCCs using Tarjan’s algorithm
17: for all cycle 𝐶 ⊂ 𝑛𝑜𝑛𝑡𝑟𝑖𝑣𝑖𝑎𝑙𝑆𝐶𝐶 ∈ 𝑅𝐺 do
18:     for all 𝑝𝑟 ∈ 𝑃𝑟 with usedInCycle(𝐶, 𝑝𝑟 ) do
19:         if ∀𝑀𝑖 ∈ 𝐶, 𝑀𝑖 (𝑝𝑟 ) = 0 then
20:             if ∄𝑡 ∈ 𝑇𝑢𝑛𝑙𝑜𝑐𝑘 enabled in 𝐶 and not BenignCycle(C) then
21:                 𝐷𝑀 ← D ∪ {𝐶}                                                                  ⊲ Scenario 3
22:             end if
23:         end if
24:     end for
25: end for
26: return 𝐷𝑀


shared memory location where at least one access is a write. Within the PPN, data races are detected
by analyzing the markings in the state reachability graph, where multiple enabled transformations
concurrently access the same unsafe data location 𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 ∈ 𝑃𝑟 with either a read-write conflict
or a write-write conflict. Crucially, our model distinguishes benign shared reads from dangerous
write conflicts through transformation metadata annotations.
  Definition 3 (Data Race). Given a RG of a PPN 𝑁 , a marking 𝑀 is said to exhibit a data race on
an unsafe data place 𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 ∈ 𝑃𝑟 if there exist two distinct transitions 𝑡 1, 𝑡 2 ∈ 𝑇 such that:
    • Both 𝑡 1 and 𝑡 2 are enabled in 𝑀: 𝑡 1, 𝑡 2 ∈ Enabled(𝑀).
    • Both transitions access the same unsafe data place 𝑝 unsafe .
    • At least one of the transitions is a write operation.
  This algorithm 4 identifies data races in a PPN using the reachability graph. For each marking
𝑀, it computes the set of enabled transitions Enabled(𝑀) and iterates over all unsafe data places
𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 . A conflict set is constructed by identifying pairs of enabled transitions (𝑡 1, 𝑡 2 ) that operate
on the same unsafe data place and where at least one transition performs a write operation. To
enhance the precision and clarity of bug reports, operations originating from the same unsafe block

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                           15


Algorithm 4 Data Race Detection in PPN
Require: Reachability Graph 𝑅𝐺 = (𝑉 , 𝐸), Unsafe Data Places 𝑃 unsafe
Ensure: Data Race Reports R
 1: R ← ∅
 2: for all 𝑀 ∈ 𝑅𝐺 do
 3:     Enabled(𝑀) ← {𝑡 ∈ 𝑇 | 𝑡 is enabled in 𝑀 }
 4:     for all 𝑝𝑢𝑛𝑠𝑎𝑓 𝑒 ∈ 𝑃𝑢𝑛𝑠𝑎𝑓 𝑒 do
 5:         ConflictSet ← {(𝑡 1, 𝑡 2 ) | 𝑡 1, 𝑡 2 ∈ Enabled(𝑀), 𝑡 1 ≠ 𝑡 2, 𝑝 unsafe ∈• 𝑡 1 ∩• 𝑡 2,
                                                          and at least one of 𝑡 1, 𝑡 2 is a write}
 6:         for all (𝑡 1, 𝑡 2 ) ∈ ConflictSet do
 7:             Loc1 ← Metadata(𝑡 1 ), Loc2 ← Metadata(𝑡 2 )
 8:             if Loc1 = Loc2 then
 9:                 continue                                                  ⊲ Filter same-location conflicts
10:             end if
11:             R ← R ∪ {(𝑝 unsafe, 𝑀, 𝑡 1, 𝑡 2 )}
12:         end for
13:     end for
14: end for
15: return R


or associated with the same code location are grouped and aggregated into a single bug report. This
aggregation reduces redundant reporting of data races caused by the same unsafe access pattern,
making the detection process more interpretable and actionable for developers.

5.3   Atomicity Violation Detection
Atomicity violations occur when the intended atomic behavior of operations on shared atomic
variables is violated. In multithreaded programs, these violations arise when the execution of
operations on shared variables is interrupted or interleaved with operations from other threads,
leading to inconsistent states. In this work, we adopt the general atomicity violation pattern from
[5].
  Definition 4 (Atomicity Violation: Unsynchronized Load-Store). Given a PPN and an
atomic variable place 𝑝 atomic ∈ 𝑃𝑟 , an atomicity violation occurs when:
   • There exists a relaxed load operation 𝑡𝑙𝑜𝑎𝑑 on 𝑝𝑎𝑡𝑜𝑚𝑖𝑐 .
   • Two distinct relaxed store operations 𝑡𝑠𝑡𝑜𝑟𝑒1 and 𝑡𝑠𝑡𝑜𝑟𝑒2 occur on the same atomic variable 𝑝𝑎𝑡𝑜𝑚𝑖𝑐 .
   • The relaxed load operation 𝑡𝑙𝑜𝑎𝑑 is preceded by at least two distinct relaxed load operations 𝑡𝑠𝑡𝑜𝑟𝑒1
     and 𝑡𝑠𝑡𝑜𝑟𝑒2 .
   • The relaxed load operation 𝑡𝑙𝑜𝑎𝑑 is followed by a branching operation, such as a conditional if or
     switch, or implicit control flow due to function calls.
    This algorithm 5 detects atomicity violations exclusively via Petri net reachability graph, moti-
vated by three pivotal insights: atomicity violations manifest as specific path patterns (≤ 2 relaxed
stores between a relaxed load and its control-dependent branch); synchronization operations break
these patterns and must terminate backtracking; and RG’s sparsity (average in-degree 𝑑 ≪ |M |)
enables efficient traversal. Thus, it constructs state-input transition map M𝑇 for 𝑂 (1) predecessor
lookup, recursively backtracks from each relaxed-load state transition 𝑠 load to collect relaxed stores
𝑡𝑠 accessing the same atomic place 𝑝𝑎 , reporting violations when: 1) subsequent branch transition
𝑡 branch exists; 2) ≤ 2 distinct 𝑡𝑠 are found; 3) no synchronization intervenes.

                                                           , Vol. 1, No. 1, Article . Publication date: September 2024.
16                                                                                       Zhang and Liu.


Algorithm 5 Atomicity Violation Detection in PPN
Require: Reachability Graph 𝑅𝐺 = (𝑉 , 𝐸), 𝑃 atomic , 𝑇branch
Ensure: Violation set V
 1: V ← ∅
 2: Build transition-state map M𝑇 (𝑠) ← {𝑡 | (𝑣 ′, 𝑣, 𝑡) ∈ 𝐸}
 3: for all 𝑣 load ∈ 𝑉 where ∃𝑡 load ∈ 𝑇relaxed-load fired at 𝑣 load do
 4:     if ∃𝑣 next : (𝑣 load, 𝑣 next, 𝑣 branch ) ∈ 𝐸 then                         ⊲ Branch after load
 5:         Stores ← ∅
 6:         Visited ← ∅
 7:         Backtrack(𝑠 load, 𝑝 atomic, Stores, Visited)
 8:         if |{𝑡𝑠 ∈ Stores | 𝑡𝑠 is store}| ≥ 2 then
 9:              V ← V ∪ {(𝑝 atomic, 𝑠 load, Stores)}
10:         end if
11:     end if
12: end for
13: return V
14: procedure Backtrack(𝑠, 𝑝𝑎 , Stores, Visited)
15:     if 𝑠 ∈ Visited then return
16:     end if
17:     Visited ← Visited ∪ {𝑠}
18:     for all 𝑡 ∈ M𝑇 (𝑠) do                                                  ⊲ Incoming transitions
19:         if 𝑡 accesses 𝑝𝑎 and 𝑡 ∈ 𝑇relaxed-store then
20:              Stores ← Stores ∪ {𝑡 }
21:         else if 𝑡 is synchronization then continue                                  ⊲ Stop at sync
22:         end if
23:         Backtrack(source(𝑡), 𝑝𝑎 , Stores, Visited)
24:     end for
25: end procedure



5.4     Complexity Analysis of Detection Algorithms
The complexity of detecting deadlocks, data races, and atomicity violations depends on the structure
of the RG and the PPN. Let |𝐸| the number of edges in the RG, |𝑃 | the number of places, |𝑇 | the
number of transitions, and |𝐹 | the number of arcs in the PPN. The complexity for each detection
algorithm is analyzed as follows:
    1. Global Deadlock Detection: The global deadlock detection algorithm iterates over all
       reachable states in the RG. For each state, the algorithm checks whether the set of enabled
       transitions is empty. This requires a traversal of all |M | states in the RG, with each state
       requiring 𝑂 (|𝑇 |) time to determine enabled transitions. Thus, the overall complexity of global
       deadlock detection is:
                                             𝑂 (|M | · |𝑇 |)
         The space complexity is 𝑂 (|M |), as all markings in the RG must be stored.
      2. Cycle Deadlock Detection: Detecting cycle deadlocks involves identifying all cycles in the
         RG and analyzing the transitions within each cycle. For a given cycle, the algorithm checks
         if there exists a resource place that remains without tokens for the entire cycle. Detecting
         cycles in the RG requires 𝑂 (|𝐸| + |M |) time using Tarjan’s strongly connected components
         (SCC) algorithm. For each cycle, transitions are checked to determine if resource places

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                                17


        are perpetually empty. In the worst case, every cycle involves all transitions, resulting in a
        complexity of 𝑂 (|cycles| · |𝑇 |). Therefore, the total complexity of cycle deadlock detection is:
                                         𝑂 ((|E | + |M |) + |cycles| · |𝑇 |)
         Space complexity is dominated by storing cycles and their associated transitions, which is
         proportional to the number of cycles.
      3. Data Race Detection: The data race detection algorithm analyzes all states in the RG.
         For each state, the enabled transitions are identified, and all pairs of enabled transitions
         are compared to detect conflicting operations on shared ‘unsafe‘ data places. This requires
         𝑂 (|𝑇 | 2 ) comparisons per state, leading to a total complexity of:
                                                   𝑂 (|M | · |𝑇 | 2 )
         Additional filtering to group operations by unsafe blocks or code locations involves metadata
         checks, which have negligible overhead compared to the pairwise transition comparisons.
         The space complexity is 𝑂 (|M |) for storing state information.
      4. Atomicity Violation Detection: Detecting atomicity violations involves analyzing transitions
         labeled as Relaxed Load or Relaxed Store. For each Relaxed Load, the algorithm performs a
         backward traversal of the RG to identify all preceding transitions affecting the same resource
         place. Identifying Relaxed Load transitions requires 𝑂 (|𝑇 |) time, and for each such transition,
         a backward traversal over the RG has a complexity of 𝑂 (|𝐸|). Thus, the total complexity is:
                                                    𝑂 (|𝑇 | · |𝐸|)
        The space complexity is 𝑂 (|M |), as it depends on the storage of visited states during backward
        traversal.

5.5     IMPROVE PERFORMANCE
To improve the efficiency of detection algorithms, such as those for state reachability and concur-
rency bug detection, we simplify Petri nets by reducing the number of places and transitions while
preserving their behavioral properties. This is crucial to mitigate the state space explosion problem,
which often hampers analysis in complex systems. In Algorithms 6, we present three key reduction
methods:
   Linear Sequence Simplification: For branchless place-transition alternating paths (denoted
as 𝑝𝑖 → 𝑡 1 → 𝑝 2 → · · · → 𝑝𝑘 ), compression is applied when path length exceeds thresh-
old 𝐿min (typically 3 nodes) and every internal transition has exactly one input and output arc
(𝑖𝑛𝑑𝑒𝑔(𝑡𝑖 ) = 𝑜𝑢𝑡𝑑𝑒𝑔(𝑡𝑖 ) = 1). The reduction identifies endpoints 𝑝𝑖 and 𝑝𝑘 via connectivity
analysis, creates new transition 𝑡𝑛𝑒𝑤 representing the sequence, updates flow relation to 𝐹 ←
(𝐹 \ {(𝑝𝑖 , 𝑡 1 ), (𝑡 1, 𝑝 2 ), . . . , (𝑡𝑛 , 𝑝𝑘 )}) ∪ {(𝑝𝑖 , 𝑡𝑛𝑒𝑤 ), (𝑡𝑛𝑒𝑤 , 𝑝𝑘 )} with weight aggregation, and removes
all intermediate nodes {𝑝 2, . . . , 𝑝𝑘 −1, 𝑡 1, . . . , 𝑡𝑛 }, preserving firing sequence equivalence while re-
ducing state space dimensionality.
   Concurrency-Irrelevant Call Chain Removal: This method eliminates nodes exclusively belonging
to sensitive paths (those containing ≥ 1 transition from 𝑇𝑐conc or place adjacent to 𝑃𝑟 ) while
preserving nodes shared with non-sensitive paths. All paths from 𝑝 start to 𝑝 end are classified into
sensitive
Ð            (𝜋𝑆 ) and non-sensitive (𝜋 𝑁 ) sets. For each node 𝑣 in sensitive paths 𝜋 ∈ 𝜋𝑆 , if 𝑣 ∉
   𝜋 𝑁 {𝑣 |𝑣 ∈ 𝜋 𝑁 } and 𝑣 ≠ 𝑝 start , it is marked for deletion. Marked nodes and adjacent arcs are
removed, with connectivity maintained through 𝑝 start ’s external links, ensuring only path-exclusive
sensitive segments are eliminated without affecting shared components.
   Non-Concurrent Loop Optimization: For each loop 𝑙 within function-derived subnets F , when
its transitions 𝑇𝐿 contain no concurrency operations (𝑇𝐿 ∩ 𝑇𝑐𝑐𝑜𝑛𝑐 = ∅) and places 𝑃𝐿 contain no

                                                                , Vol. 1, No. 1, Article . Publication date: September 2024.
18                                                                                               Zhang and Liu.


resource places (𝑃𝐿 ∩ 𝑃𝑟 = ∅), the cycle is broken by removing exactly one back-edge (𝑡𝑙𝑎𝑠𝑡 , 𝑝 𝑓 𝑖𝑟𝑠𝑡 )
where 𝑡𝑙𝑎𝑠𝑡 is the final transition before looping and 𝑝 𝑓 𝑖𝑟𝑠𝑡 is the cycle entry point, preserving all
external connections to loop nodes while eliminating cyclic behavior through minimal structural
modification.

6                  Experimental Evaluation
6.1                 Experiment Setup and Benchmarks
To rigorously assess our Petri net-based framework against state-of-the-art tools (LockBud and
Miri), we designed three benchmark sets spanning controlled tests and real-world Rust projects:
L-Bench (LockBud’s test suite), M-Bench (Miri’s concurrency tests), and P-Bench (our curated
projects including Rayon-demo (24k LoC) and Openethereum (128k LoC)). These benchmarks mea-
sure detection capabilities for deadlocks, data races, and atomicity violations through metrics
including real bugs (RB), false positives/negatives (FP/FN), and time efficiency. Our results demon-
strate that integrating structural analysis—enhancing classical Petri nets with constraint arcs for
memory ordering and hierarchical subnets for contextual lock modeling—with state reachability
exploration—using partial-order reduction to prune redundant interleavings—overcomes inherent
Petri net limitations in detecting local deadlocks and atomicity violations. For deadlocks, traditional
approaches ignored dynamic contexts, causing LockBud’s false positives in lock-closure (FP=1),
while our hybrid method achieved 100% in inter (12/12 RBs detected) versus Miri’s 91.7% false
negative rate. For atomicity violations, LockBud misflagged safe SeqCst operations in atomic-SeqCst
(FP=4) due to unmodeled memory semantics, whereas our constraint arcs embedded Rust’s memory
model, enabling precise detection of all true violations in atomic-violation (4/4 RBs). State explo-
ration further exposed Miri’s coverage gaps—detecting all address_reuse data races (2/2 RBs) versus
its false negatives—through targeted path analysis. Crucially, our approach scaled to industrial
projects: in Openethereum (128k LoC), we detected all 27 deadlocks with zero false positives and
74.4% higher precision than LockBud (FP=3), resolving the tension between structural soundness
and dynamic completeness that limits existing tools.
                                             Table 1. Result on detection of deadlocks.

                                                                     #Deadlock                    Time (s)
                   Benchmark          LoC    Lock RB
                                                             LockBud        Miri   Our    LockBud Miri        Our
                        conflict       75      3      1           1        3(FP:3)   1      0.05     15.89     4.9
                     conflict-inter    52      2      1           1           0      1      0.23      0.31     0.31
 L-Bench




                          intra        57      4      4        6(FP:2)    1(FN:3)    4      2.28      1.26     1.10
                          inter        178     6      12    14(FP:3,FN:1) 1(FN:11) 12       1.13      0.97     2.3
                     lock-closure      40      4      1        2(FP:1)    0(FN:1)    1      0.24      0.35     0.26
                    condvar-struct     273     8      4        1(FN:3)    2(FN:2)    4      2.01      1.17     1.77
                       static-ref      13      1      1           1           1      1      0.05      0.79     0.21
 P-Bench M-Bench




                     singlethread      45      2      0        6(FP:6)        0      0      0.18      1.8      0.08
                      mutex-leak        8      1      1        0(FN:1)        1      1      0.10      0.33     0.16
                          sync         266     7      1        1(FP:1)      0(FN)    1      0.08      1.27     2.53
                      nopreempt        87      5      3        5(FP:2)        3      3      0.26      0.31     0.28
                     Rayon-demo       24k      72     2        0(FN:2)        ✗      2      4.18        -     10.15
                         RCore        22k     263     8           8           ✗      8      7.82        -     15.12
                      Tikv-client     29k      4      0           0           ✗      0      34.12       -     53.50
                    Openethereum      128k    441     27      30(FP:3)        ✗     27      45.32       -     79.12


, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                           19


Algorithm 6 Petri Net Reduction Algorithm
Require: Program Petri net 𝑃𝑃𝑁 = (𝑃,𝑇 , 𝐹,𝑊 , 𝑀0 ), resource places 𝑃𝑟 , concurrent transitions
    𝑇𝑐𝑐𝑜𝑛𝑐 ∈ 𝑇 , entry point:{𝑝𝑠𝑡𝑎𝑟𝑡 , 𝑝𝑒𝑛𝑑 }
Ensure: 𝑃𝑃𝑁 ′ = (𝑃 ′,𝑇 ′, 𝐹 ′,𝑊 ′, 𝑀0′ )
 1: procedure ReducePetriNet
 2:      CompressLinearSeqences(𝑃𝑃𝑁 )
 3:      PruneSensitiveChains(𝑃𝑃𝑁 , 𝑝𝑠𝑡𝑎𝑟𝑡 , 𝑝𝑒𝑛𝑑 ,𝑇𝑐𝑐𝑜𝑛𝑐 , 𝑃𝑟 )
 4:      ReduceLocalLoops(𝑃𝑃𝑁 ,𝑇𝑐𝑐𝑜𝑛𝑐 , 𝑃𝑟 )
 5:      return 𝑃𝑃𝑁
 6: end procedure
 7: function CompressLinearSeqences(𝑃𝑃𝑁 )
 8:      for all maximal linear path 𝜋 = [𝑝𝑠 → 𝑡 1 → · · · → 𝑝𝑘 ] do
 9:          if |𝜋 | ≥ 3 and ∀𝑡𝑖 ∈ 𝜋 : indeg = outdeg(𝑡𝑖 ) = 1 then
10:              Replace 𝜋 with 𝑝𝑠 → 𝑡 new → 𝑝𝑘
11:              Remove intermediate nodes {𝑝 2, . . . , 𝑝𝑘 −1, 𝑡 1, . . . , 𝑡 |𝜋 |/2 }
12:          end if
13:      end for
14: end function
15: function PruneSensitiveChains(𝑃𝑃𝑁 , 𝑝𝑠𝑡𝑎𝑟𝑡 , 𝑝𝑒𝑛𝑑 ,𝑇𝑐𝑐𝑜𝑛𝑐 , 𝑃𝑟 )
16:      Sensitive paths:𝜋𝑆 ← ∅, non-sensitive paths:𝜋 𝑁 ← ∅
17:      for place-transition paths:𝜋𝑝𝑡 ∈ [𝑝𝑠𝑡𝑎𝑟𝑡 → 𝑡 1 → 𝑝 1 → · · · → 𝑝𝑒𝑛𝑑 ] do
18:          if ∃𝑡 ∈ 𝜋𝑝𝑡 : (𝑡 ∈ 𝑇𝑐𝑐𝑜𝑛𝑐 ∨ 𝑝 = {•𝑡 ∪ 𝑡 • } ∈ 𝑃𝑟 ) then
19:              𝜋𝑆 ← 𝜋𝑆 ∪ {𝜋𝑝𝑡 }
20:          else
21:              𝜋 𝑁 ← 𝜋 𝑁 ∪ {𝜋𝑝𝑡 }
22:          end if
23:      end for
24:      for 𝜋 ∈ 𝜋𝑆 do
25:          for each node 𝑣 ∈ 𝜋 do
                         Ð
26:              if 𝑣 ∉ 𝜋𝑝𝑡 ∈𝜋𝑁 {𝑣 |𝑣 ∈ 𝜋𝑝𝑡 } and 𝑣 ≠ 𝑝𝑠𝑡𝑎𝑟𝑡 then
27:                   Mark 𝑣 for deletion: 𝑉𝑑𝑒𝑙 ← 𝑉𝑑𝑒𝑙 ∪ {𝑣 }
28:              else
29:                   break
30:              end if
31:          end for
32:      end for
33:      Remove all 𝑣 ∈ 𝑉del and adjacent arcs
34: end function
35: function ReduceLocalLoops(𝑃𝑃𝑁 ,𝑇𝑐𝑐𝑜𝑛𝑐 , 𝑃𝑟 )
36:      for each function subnet 𝑓 ∈ F do
37:          for each loop 𝑙 ∈ 𝐿 do
38:              Extract 𝑃𝐿 ,𝑇𝐿 within 𝑙
39:              if 𝑇𝐿 ∩ 𝑇𝑐𝑐𝑜𝑛𝑐 = ∅ and 𝑃𝐿 ∩ 𝑃𝑟 = ∅ then
40:                   Break loop by removing (𝑡 last, 𝑝 first ) ∈ 𝐹
41:              end if
42:          end for
43:      end for
44: end function

                                                           , Vol. 1, No. 1, Article . Publication date: September 2024.
20                                                                                              Zhang and Liu.


                                      Table 2. Result on detection of data races.

                                                                    #Race Condition               Time (s)
             Benchmark          LoC RB            UnsafeOp
                                                                 LockBud Miri Our           LockBud Miri Our
                 datarace       226       1           34            ✗         1     1          -      0.36  0.08
                                                                    ✗
 M-Bench




              address-reuse     61        2           5                    1(FN:1)  2          -     16.02 0.36
             disable-datarace   31        1           5             ✗         1     1          -      0.34  0.22
                static-use      30        1           7             ✗         1     1          -      0.31  0.49
                 arc-asptr      46        1           3             ✗         1     1          -     149.41 0.49
                  simple        75        0           0             ✗         0     0          -      0.08  0.22

                                 Table 3. Result on detection of atomicity violation.

                                                                    #Race Condition                Time (s)
             Benchmark          LoC Atomic             RB
                                                               Lockbud Miri        Our      LockBud Miri         Our
               atomic-assert    226           8         1       0(FN:1) 0(FN:1)      1        0.47    15.73      0.45
 L/P-Bench




             atomic-violation   72            5         4          4     0(FN:4)     4        0.18    17.03      0.08
              atomic-closure    115           8         1       0(FN:1) 0(FN:1)      1        0.13    19.55      0.89
              atomic-SeqCst     72            5         0       4(FP:4)     0        0        0.34    16.33      0.12
                atomic-Ptr      294           7         2       0(FP:2)     2     0(FN:2)     2.42     1.64      2.85


6.2          Research Questions
While Petri nets offer formal foundations for concurrency modeling, their application to real-world
Rust programs faces three fundamental challenges. To address these challenges and evaluate our
integrated approach, we formulate the following research questions:To address the limitations of
Petri nets in concurrency bug detection and validate our integrated approach, we formalize three
research questions:
   RQ1: How can Rust’s ownership and lifetime semantics be formally encoded into Petri net token
flows while preserving bisimulation equivalence with the original program’s behavior?
   RQ2: What inherent limitations of Petri nets in detecting local deadlocks and atomicity violations
can be overcome by integrating structural analysis with state reachability exploration?
   RQ3: To what extent does our compression methods reduce the reachable state space without
compromising detection completeness for deadlocks and data races?

6.3          RQ1: Correctness of Ownership-Semantic Transformation
Since the semantic equivalence of Rust programs and Petri nets within a subset of simplified
grammars has been demonstrated in section 4.3, we can build on this conclusion to discuss the
notions of soundness and completeness of transformations and subsequent analyses.
  Definition 5 (Rust Ownership in PPN). The ownership system of Rust is mapped to PPN token
semantics as follows:
   • Ownership: 𝑀 (𝑝𝑟 ) = 1 ⇐⇒ unique ownership of resource 𝑟 .
   • Borrowing: ∃𝑡 ∈ 𝐸𝑛𝑎𝑏𝑙𝑒𝑑 (𝑀 (𝑝𝑟 )), 𝑝𝑟 ∈• 𝑡 borrows of 𝑟 .
   • Lifetime: 𝑙𝑖 𝑓 𝑒𝑡𝑖𝑚𝑒 (𝑟 ) = [𝑡𝑠𝑡𝑎𝑟𝑡 , 𝑡𝑒𝑛𝑑 ] ⇐⇒ 𝑀 (𝑝𝑟 ) ≠ 𝑝𝑟 .𝑐𝑎𝑝𝑡𝑖𝑐𝑖𝑡𝑦.
Transition preconditions enforce Rust’s ownership rules: (1) •𝑡𝑚𝑜𝑣𝑒 = {𝑝𝑥 , 𝑝𝑟 };(2) •𝑡𝑏𝑜𝑟𝑟𝑜𝑤 = {𝑝𝑥 , 𝑝𝑟 }
     •
and 𝑡𝑏𝑜𝑟𝑟𝑜𝑤 = {𝑝𝑥 , 𝑝𝑟 }.


, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                             21


   Theorem 1 (Soundness of Concurrency Analysis). The transformation from Rust programs to
Petri nets preserves concurrency semantics, ensuring no false positives in detecting deadlocks, atomicity
violations, and data races. Formally, for any program 𝑃𝑟𝑜𝑔 in our defined subset and its PPN:
                    ¬∃𝜎 ∈ Reach(𝑃𝑃 𝑁 ) : 𝜎 ⊨ 𝜑 =⇒ ¬∃𝜏 ∈ Traces(𝑃𝑟𝑜𝑔) : 𝜏 ⊨ 𝜑
where 𝜑 ∈ {deadlock, atomicity_violation, data_race}. This guarantee stems from three pillars: (1)
Control flow isomorphism ensures basic blocks map bijectively to places (𝑏𝑏 𝑓 ↔ 𝑝𝑏 ) and control
operations to transitions (𝛿 𝑓 ↔ 𝑡𝑐 ), preserving execution paths; (2) Resource binding consistency models
synchronization primitives through dedicated places (𝑝𝑚 for mutexes) and transitions (𝑡 lock, 𝑡 unlock )
with token semantics mirroring lock states; (3) Interleaving surjectivity encodes all possible thread
schedules via concurrent transition firings in 𝑇conc , explicitly representing non-deterministic execution
paths.
   Proof. Soundness is established through operational correspondence: For deadlock freedom,
if no siphon-trap imbalance (•𝑆 ⊊ 𝑆•) exists in PPN, the program’s wait-for graph contains
no cycles. For data race absence, conflicting access pairs (𝑡 𝑤 , 𝑡𝑟 ) in 𝑇unsafe are always separated
by synchronization transitions (𝑡 sync ) when required by program logic. Atomicity violations are
prevented because atomic regions Atomic(𝑜𝑟𝑑) map to atomic transition sequences [𝑡 begin, . . . , 𝑡 end ]
where intermediate firings are disabled by guard conditions. The proof leverages the control flow
isomorphism which guarantees that for every program execution path 𝜏, there exists a firing
sequence 𝜎 in PPN with identical synchronization events and memory access ordering.                    □
  Theorem 2 (Completeness of Concurrency Bug Detection). The PPN model detects all
concurrency bugs present in the original program:
                    ∃𝜏 ∈ Traces(𝑃𝑟𝑜𝑔) : 𝜏 ⊨ 𝜑 =⇒ ∃𝜎 ∈ Reach(𝑃𝑃 𝑁 ) : 𝜎 ⊨ 𝜓 (𝜑)
with defect mapping 𝜓 :
                        𝜓 (deadlock) ≜ ∃𝑆 ⊆ 𝑃𝑟𝑜𝑔 : •𝑆 ⊊ 𝑆•
            𝜓 (atomicity_violation) ≜ ∃𝑡 load ∈ [𝑡 begin, 𝑡 end ] : fire(𝑡 load )
                       𝜓 (data_race) ≜ ∃𝑡 𝑤 , 𝑡𝑟 ∈ 𝑇atom : concurrent(𝑡 𝑤 , 𝑡𝑟 ) ∧ ¬unsafe(𝑝𝑟 )
Completeness holds for bounded thread creation and finite recursion depth.
   Proof. Completeness follows from state space coverage and defect manifestation: (1) Deadlocks
manifest as token starvation in siphons where resource places 𝑝𝑚 are held while waiting places
𝑝 wait have tokens but cannot fire due to missing resources; (2) Data races occur when conflicting
atomic transitions (𝑡 𝑤 for write, 𝑡𝑟 for read) fire concurrently without mutual exclusion tokens in
𝑝𝑚 ; (3) Atomicity violations appear when intermediate transitions 𝑡 load fire between 𝑡 begin and 𝑡 end
of an atomic region, detectable through forbidden state patterns. The reachability graph covers all
thread interleavings by construction, as each spawn operation (thread :: spawn) generates new
tokens in thread-specific places, enabling concurrent firing of transitions in different thread subnets.
Partial-order reduction preserves bug traces while mitigating state explosion.                         □

6.4   RQ2: Effectiveness on Detecting Concurrency Bugs
The results in Table 1 demonstrate the performance of our tool compared to LockBud and Miri
across various benchmarks, including L-Bench, M-Bench, and P-Bench. Miri, as a Rust interpreter,
exhibits robust runtime concurrency detection capabilities, supporting asynchronous operations
and multiple concurrency primitives. However, it is limited to executable crates, making it incapable
of directly analyzing library crates without executable test cases. Furthermore, its runtime reports

                                                             , Vol. 1, No. 1, Article . Publication date: September 2024.
22                                                                                                  Zhang and Liu.


are often challenging to interpret, and its reliance on incomplete models of certain concurrency
scenarios can lead to false negatives, as shown in benchmarks such as condvar-struct and inter.
   LockBud is a lightweight tool based on lock graph analysis, offering efficiency in detecting
locking-related issues. Nevertheless, it suffers from two primary sources of false positives: first,
its conservative assumption that multiple read operations on a RwLock could block subsequent
write locks; second, its inability to accurately model thread states, leading to lifecycle analysis
errors for locks with different aliases. These shortcomings are evident in its results for benchmarks
like intra and conflict-inter. Additionally, LockBud struggles with condvar-based synchronization
mechanisms, as it cannot definitively determine whether a notify signal has already occurred prior
to a thread’s wait, resulting in both false positives and false negatives. Fig. 3 illustrates examples of
both false positives and false negatives reported by Lockbud. The first type of false positives in
Lockbud is due to a lack of thread modeling. In Fig. 3(a), the thread creation function is called in
line 5. Due to the lifetime constraint, the code from lines 1 to 4 has been executed and the lock
held by it has been released, so there is no competition for lock resources after thread creation,
there is no deadlock. Moving lines 5 to 9 of the code before line 1 will not result in a deadlock, but
Lockbud will still produce a false positive. The false negative occurs because Lockbud lacks proper
modeling of recursive calls, mistakenly assuming that locks in recursive calls have already been
released during its lifetime analysis.


           1. {
           2. let _b = lock_b1.lock().unwrap();            1. fn recur(&self){
           3. let _a = lock_a1.lock().unwrap();            2. match *self.mu.lock() {
           4. }                                            3.      1=> self.recur(),
           5. let th = thread::spawn(move || {             4.      _=> {
           6. let _a = lock_a2.lock().unwrap();            5.        //*self.mu.lock() += 1;
           7. let _b = lock_b2.lock().unwrap();            6.      }
           8. });                                          7. };
           9. th.join().unwrap(); 
                                                           8. }

                    (a) Example of a false positive.                  (b) Example of a false negative.


                        Fig. 3. Examples of false positives and false negatives in Lockbud.


   In comparison, our Petri net-based approach leverages state reachability analysis, allowing for
precise modeling of concurrency scenarios. By specifying function entry points and systematically
exploring potential deadlock states, our tool achieves comprehensive coverage while maintaining
accuracy, as evidenced by its performance in detecting all true deadlocks in benchmarks like inter
and lock-closure. Furthermore, our tool produces precise reports with no false positives across the
evaluated benchmarks.
   The results in Table 2 and Table 3 demonstrate the detection of data races and atomicity violations,
as these two categories share common characteristics. Atomicity violations are typically caused by
relaxed memory orderings, leading to concurrent load or store operations across threads. These
issues can also be considered as a special case of race conditions. As such, we evaluate both types
of bugs together. LockBud does not support the detection of data race bugs. For atomicity violation
detection, it only focuses on the sequential usage patterns of atomic APIs within a single thread.
Consequently, it fails to detect atomicity violations in multithreaded scenarios. Moreover, even
when changes are made to memory ordering or additional locks are added, LockBud still incorrectly
reports the presence of atomicity violations, reflecting limitations in its modeling of synchronization

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                           23


and memory order semantics. Miri relies on runtime analysis. While effective in detecting race
conditions and atomicity violations, it is prone to termination errors if unwrap operations are
not preemptively handled. Additionally, due to its reliance on executed paths, some concurrency
issues may be missed, particularly if the problematic execution path is not covered during testing.
Our Petri net-based framework exhibits significant advantages in both data race and atomicity
violation detection. By explicitly modeling transitions for unsafe data operations, our framework
not only detects traditional race conditions but is also theoretically capable of identifying more
complex concurrency bugs such as use-after-free (UAF) and null pointer dereferences. However,
in this study, we focus specifically on race conditions where at least one operation on the same
unsafe data is a write. This approach extends naturally to the detection of atomicity violations
by capturing relaxed memory ordering operations and store that occur concurrently without
appropriate synchronization mechanisms. Overall, the results highlight the flexibility and precision
of our approach in detecting both data races and atomicity violations, demonstrating its superiority
over LockBud and Miri in addressing multithreaded and relaxed-memory scenarios. However, as
the detection of atomicity violations is inherently challenging in multithreaded environments,
further refinement of the Petri net’s modeling capabilities could further improve its accuracy and
applicability.


        1. struct Signal {                                    1. struct EvilSend<T>(T);
        2. data: Option<T>,                                   2. type T=AtomicCell;
        3. ready: AtomicBool,                                 3. fn racy_read_discarded(){
        4. }                                                  4. evilSend.0.store(0);
        5. fn push(){               // Thread 1               5. let writer = thread::spawn(move || {
        6. (*signal).data = cache.into_data();˅               6.       evilSend.0.store(1, Relaxed);
        7. (*signal.ready).store.(true,Relaxed);              7. });
        8. }                                                  8. if evilSend.0.load(Relaxed) == 1{
        9. fn pop(){               // Thread 2                9.        panic!
        10. while !signal.ready.load(Relaxed){}               10. }
        11. return signal.data;                               11. writer.join().unwrap();
        12.}                                                  12. }

              (a) Example in AtomVChecker.                                (b) Example in PPN.


                Fig. 4. Examples of AtomVChecker and PPN detecting atomicity violations.


   For example, another existing atomicity violation detection tool, AtomVChecker [24], identifies
several patterns of atomicity violations in Rust, as shown in Fig. 4(a). These include operations
like push and pop performed in different threads, where relaxed memory ordering may cause pop
to return an uninitialized variable. The PPN approach discussed in this paper primarily detects
race conditions caused by multiple store operations, leading to undefined behavior during a load.
AtomVChecker cannot report errors in Fig. 4(b), while PPN cannot detect the atomicity violations
in Fig. 4(a). The two approaches can complement each other. In future work, we will use advanced
nets to represent the dependencies between data.

6.5   RQ3: Efficiency of State Compression in Bug Detection
The proposed reduction methods demonstrate exceptional efficiency in bug detection by funda-
mentally addressing state explosion through three complementary techniques: (1) linear sequence
compression eliminates intermediate states while preserving firing sequences, (2) sensitive call

                                                           , Vol. 1, No. 1, Article . Publication date: September 2024.
24                                                                                               Zhang and Liu.


chain pruning removes concurrency-irrelevant paths while protecting shared nodes, and (3) lo-
calized loop abstraction breaks cycles without resource access—collectively achieving average
structural reductions of 34.88% for places, 37.21% for transitions, and 33.76% for flow relations
while enabling superlinear state space compression (e.g., Rayon-demo’s 94.5% reduction from
1259 to 69 states), where the remarkably small post-reduction state spaces (𝑆𝑡𝑎𝑡𝑒𝑠 ′ ) directly result
from deadlock-induced state space truncation during coverability graph generation, as deadlock
states become terminal nodes that prevent further state expansion; crucially, the methods’ for-
mal preservation of safety and liveness properties ensures all concurrency bugs—including the
atomic violations detected in the 123-state reduced model (from 127 original states) and deadlocks
in condvar-lock (116→32 states)—remain verifiable while reducing verification complexity from
exponential to near-linear, with maximal processing time of just 4.8ms for industrial-scale models
(2316 elements), thereby overcoming the fundamental state explosion barrier that traditionally
limits Petri net verification.


                        Table 4. Effectiveness Evaluation of Petri Net Reduction Methods

                                   Original Model                         Reduction Effectiveness (%)
       Benchmarks
                                 |P|+|T|+|F| States Places              Transitions Flow Time(ms) 𝑆𝑡𝑎𝑡𝑒𝑠 ′
          intra                      313       55   20.00                  21.43     17.86      1.5   48
          inter                      168       40   38.10                  44.74     38.64      0.6   12
       condvar-lock                  210      116   41.51                  44.68     40.91      1.5   32
     atomic-violation                555      127   24.03                  27.56     23.75      1.3   123
       Rayon-demo                   2316      1259  48.29                  50.80     47.66      4.8   69
    Average Reduction                 -         -      -                   34.88     37.21     33.76   -
                                                     Original−Reduced
     • All values represent percentage reduction:   Original   × 100
     • Combined reduction applies all three methods sequentially




7    Conclusion
In this work, we proposed a formal framework for detecting concurrency bugs in Rust programs
using Petri nets. By defining a precise program model and converting it into a PPN representation,
we enabled the systematic analysis of deadlocks, data races, and atomicity violations. The formal
definitions of these bug patterns, coupled with RG traversal and tailored detection algorithms,
ensure both the soundness and completeness of our approach. To improve the scalability of the
framework, we introduced a Petri net simplification algorithm that reduces the size and complexity
of the net while preserving its execution semantics. This optimization enhances the efficiency of the
bug detection process without sacrificing accuracy. Through the rigorous construction of resource
places, transitions, and state-based analysis, our method captures the essential synchronization
and unsafe operation semantics of Rust programs. By leveraging the expressiveness of Petri nets,
this framework provides a unified and formalized approach to identifying key concurrency bugs,
ensuring correctness and reliability in the detection process. Future work will focus on extending
this framework to handle more advanced concurrency patterns, improving the performance of state
exploration algorithms, and applying the methodology to real-world Rust programs to validate its
effectiveness and scalability.

, Vol. 1, No. 1, Article . Publication date: September 2024.
Petri Nets-based Methods on Automatically Detecting for Concurrency Bugs in Rust Programs                                  25


References
 [1] Vytautas Astrauskas, Aurel Bílỳ, Jonáš Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli, and
     Alexander J Summers. 2022. The Prusti Project: Formal Verification for Rust. In NASA Formal Methods Symposium.
     Springer, 88–108.
 [2] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021. RUDRA: finding memory safety bugs
     in Rust at the ecosystem scale. In Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles.
     84–99.
 [3] Yuandao Cai, Peisen Yao, and Charles Zhang. 2021. Canary: practical static detection of inter-thread value-flow bugs. In
     Proceedings of the 42nd ACM SIGPLAN International Conference on Programming Language Design and Implementation.
     1126–1140.
 [4] Yuandao Cai, Chengfeng Ye, Qingkai Shi, and Charles Zhang. 2022. Peahen: Fast and precise static deadlock detection
     via context reduction. In Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium
     on the Foundations of Software Engineering. 784–796.
 [5] Yan Cai, Hao Yun, Jinqiu Wang, Lei Qiao, and Jens Palsberg. 2021. Sound and efficient concurrency bug prediction.
     In Proceedings of the 29th ACM Joint Meeting on European Software Engineering Conference and Symposium on the
     Foundations of Software Engineering. 255–267.
 [6] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: Detecting memory deallocation bugs of rust
     programs via static data-flow analysis. ACM Transactions on Software Engineering and Methodology 32, 4 (2023), 1–21.
 [7] Jieqi Ding, Han Zhu, Huibiao Zhu, and Qin Li. 2009. Formal Approaches to Deadlock Analysis in Competitions of
     Shared Web Resources. In 2009 Third IEEE International Symposium on Theoretical Aspects of Software Engineering.
     IEEE, 327–328.
 [8] Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust used safely by software developers?. In
     Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering. 246–257.
 [9] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the foundations of
     the Rust programming language. Proceedings of the ACM on Programming Languages 2, POPL (2017), 1–34.
[10] Ekkart Kindler. 2006. The petri net markup language and iso/iec 15909-2: Concepts, status, and future directions.
     Entwurf komplexer Automatisierungssysteme 9 (2006), 35–55.
[11] Steve Klabnik and Carol Nichols. 2019. The Rust Programming Language (Covers Rust 2018). No Starch Press.
[12] Xin Li, Yongjuan Liang, Hong Qian, Yi-Qi Hu, Lei Bu, Yang Yu, Xin Chen, and Xuandong Li. 2016. Symbolic execution of
     complex program driven by machine learning based constraint solving. In 2016 31st IEEE/ACM International Conference
     on Automated Software Engineering (ASE). 554–559.
[13] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John CS Lui. 2021. MirChecker: detecting bugs in Rust programs
     via static analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security.
     2183–2196.
[14] Hongwei Liao, Yin Wang, Hyoun Kyu Cho, Jason Stanley, Terence Kelly, Stéphane Lafortune, Scott Mahlke, and Spyros
     Reveliotis. 2013. Concurrency bugs in multithreaded software: Modeling and analysis using Petri nets. Discrete Event
     Dynamic Systems 23, 2 (2013), 157–195.
[15] Guanjun Liu. 2022. Petri Nets: Theoretical Models and Analysis Methods for Concurrent Systems. Springer Singapore.
[16] Nicholas D Matsakis and Felix S Klock. 2014. The rust language. ACM SIGAda Ada Letters 34, 3 (2014), 103–104.
[17] Tom Meyer. 2020. A Petri-Net semantics for Rust. Master’s thesis. University of Rostock.
[18] Miri. 2023. An Interpreter for Rust’s Mid-Level Intermediate Representation. https://github.com/rust-lang/miri.
[19] Pengxiang Ning and Boqin Qin. 2020. Stuck-me-not: A deadlock detector on blockchain software in Rust. Procedia
     Computer Science 177 (2020), 599–604.
[20] Boqin Qin, Yilun Chen, Haopeng Liu, Hua Zhang, Qiaoyan Wen, Linhai Song, and Yiying Zhang. 2024. Understanding
     and Detecting Real-World Safety Issues in Rust. IEEE Transactions on Software Engineering (2024).
[21] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Understanding memory and thread safety
     practices and issues in real-world Rust programs. In Proceedings of the 41st ACM SIGPLAN Conference on Programming
     Language Design and Implementation. 763–779.
[22] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson. 2022. Verifying dynamic
     trait objects in rust (ICSE-SEIP ’22). Association for Computing Machinery, New York, NY, USA, 321–330. https:
     //doi.org/10.1145/3510457.3513031
[23] Jean-Baptiste Voron and Fabrice Kordon. 2008. Transforming sources to petri nets: a way to analyze execution of
     parallel programs.. In Simutools. 13.
[24] Cheng Wang, Tengfei Tu, Sujuan Qin, Guangjun Wu, Fei Gao, and Mingchao Wan. 2024. Understanding Atomics
     and Memory Ordering Issues in Real-World Rust Software. In 2024 IEEE 35th International Symposium on Software
     Reliability Engineering (ISSRE). IEEE, 582–592.



                                                                  , Vol. 1, No. 1, Article . Publication date: September 2024.
26                                                                                                        Zhang and Liu.


[25] Feng Wang, Fu Song, Min Zhang, Xiaoran Zhu, and Jun Zhang. 2018. Krust: A formal executable semantics of rust. In
     2018 International Symposium on Theoretical Aspects of Software Engineering (TASE). IEEE, 44–51.
[26] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R Lyu. 2021. Memory-safety challenge considered
     solved? An in-depth study with all Rust CVEs. ACM Transactions on Software Engineering and Methodology (TOSEM)
     31, 1 (2021), 1–25.
[27] Weili Yao and Xudong He. 1997. Mapping Petri nets to concurrent programs in CC++. Information and Software
     Technology 39, 7 (1997), 485–495.
[28] Chengquan Zhang, Yang Feng, Yaokun Zhang, Yuxuan Dai, and Baowen Xu. 2024. Beyond Memory Safety: an Empirical
     Study on Bugs and Fixes of Rust Programs. In 2024 IEEE 24th International Conference on Software Quality, Reliability
     and Security (QRS). IEEE, 272–283.
[29] Shuofei Zhu, Ziyi Zhang, Boqin Qin, Aiping Xiong, and Linhai Song. 2022. Learning and programming challenges of
     rust: a mixed-methods study. In Proceedings of the 44th International Conference on Software Engineering (Pittsburgh,
     Pennsylvania) (ICSE ’22). Association for Computing Machinery, New York, NY, USA, 1269–1281. https://doi.org/10.
     1145/3510003.3510164




, Vol. 1, No. 1, Article . Publication date: September 2024.
