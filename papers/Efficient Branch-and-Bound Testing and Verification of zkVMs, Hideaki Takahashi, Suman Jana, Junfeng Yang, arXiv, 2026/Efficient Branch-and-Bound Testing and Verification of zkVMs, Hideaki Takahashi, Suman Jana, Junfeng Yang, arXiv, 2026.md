                                           Efficient Branch-and-Bound Testing and Verification of zkVMs
                                                        Hideaki Takahashi                                              Suman Jana                                   Junfeng Yang
                                                         Columbia University                                      Columbia University                            Columbia University
                                                           New York, USA                                            New York, USA                                   New York, USA
                                                        ht2673@columbia.edu                                     suman@cs.columbia.edu                          junfeng@cs.columbia.edu

                                         Abstract                                                                                Keywords
                                         Zero-knowledge virtual machines (zkVMs) enable verifiable execu-                        Software Testing, Zero-Knowledge Proof, zkVM, Verification
                                         tion of general-purpose programs by translating virtual machine                         ACM Reference Format:
                                         semantics into algebraic constraints over execution traces. The cor-                    Hideaki Takahashi, Suman Jana, and Junfeng Yang. 2026. Efficient Branch-
                                         rectness of these constraints is critical: a single missing or incorrect                and-Bound Testing and Verification of zkVMs. In Proceedings of the 2026
arXiv:2609.15020v1 [cs.CR] 14 Sep 2026




                                         constraint can admit forged proofs (under-constrained) or reject                        ACM SIGSAC Conference on Computer and Communications Security (CCS
                                         valid executions (over-constrained). Existing approaches do not pro-                    ’26), November 15–19, 2026, The Hague, Netherlands. ACM, New York, NY,
                                         vide meaningful guarantees at production scale: fuzzers and unit                        USA, 21 pages. https://doi.org/10.1145/3830454.3846593
                                         tests often miss bugs, SMT solvers struggle with the size and non-
                                         linearity of constraints, and theorem provers require substantial                       1    Introduction
                                         manual effort.                                                                          Zero-knowledge proofs (ZKPs) enable verifiable computation by
                                            We present ZEBRA, a fully automated verification and bug-                            reducing program execution to the satisfaction of algebraic con-
                                         detection framework grounded in a precise correctness criterion:                        straints over a finite field. This process, arithmetization, has tradi-
                                         for a given program and input, the constraint system must admit ex-                     tionally been performed manually using domain-specific languages
                                         actly one valid execution trace—no more (soundness) and no fewer                        such as Circom [4] and Noir [3], a workflow that is both labor-
                                         (completeness). This reduces zkVM verification to a solution-set                        intensive and error-prone: even minor mismatches between in-
                                         cardinality problem over a canonical trace space, where redundan-                       tended semantics and generated constraints can produce severe
                                         cies such as null-row padding and non-deterministic permutations                        soundness or completeness violations [22, 28, 33].
                                         are eliminated prior to counting.                                                          zkVMs & the shifting trust boundary. Zero-Knowledge Vir-
                                            To compute cardinality tractably, ZEBRA lifts analysis from                          tual Machines (zkVMs) address the above-mentioned issue by fix-
                                         finite-field witnesses to an integer interval lattice, exploiting a                     ing a universal arithmetization at the level of a virtual machine,
                                         structural sparsity property of zkVM constraints: across 5 real-                        eliminating the need for per-program circuit construction [9]. De-
                                         world zkVMs, constraints utilize only 14.0% of their theoretical                        velopers write programs in standard languages (e.g., Rust, C++,
                                         connectivity capacity on average. This sparsity enables tight in-                       Go), which are compiled to a conventional ISA, typically RISC-V.
                                         terval propagation with limited over-approximation error. ZEBRA                         Program execution produces a trace of machine states; the zkVM
                                         performs a parallel branch-and-bound search that, unlike fuzzing,                       verifies that this trace satisfies a fixed constraint system encoding
                                         either produces a concrete counterexample or certifies the absence                      valid state transitions. Arithmetization is thus performed only once
                                         of violations within a bounded input region.                                            for the VM semantics and can be reused across arbitrary programs.
                                            We evaluate ZEBRA on five real-world zkVMs. ZEBRA discov-                            zkVMs have gained rapid adoption in blockchain, machine learning,
                                         ers 11 previously unknown vulnerabilities, including critical flaws                     and supply-chain verification [6, 14, 25, 32].
                                         enabling control-flow hijacking and proof forgery—none detected                            This shift in abstraction fundamentally changes the trust bound-
                                         by a state-of-the-art fuzzer; 6 have already been independently                         ary: correctness now depends entirely on the zkVM’s arithmetiza-
                                         confirmed and 3 have been fixed by developers. Compared to SMT-                         tion, the translation of virtual machine logic (CPU state transitions,
                                         based verification, ZEBRA is 51.5× faster, verifies 16.5 percentage                     memory consistency, ALU operations) into a polynomial constraint
                                         point more instances, and its range verification provides up to 63×                     system over a finite field [16, 17]. Concretely, for a fixed program
                                         efficiency gain over repeated single-input verification.                                and input, this system must admit exactly the valid execution traces,
                                                                                                                                 no more (soundness) and no fewer (completeness). In practice, these
                                         CCS Concepts                                                                            constraints operate over large two-dimensional trace tables with
                                         • Security and privacy → Software security engineering; Crypt-                          thousands of cells and non-linear constraints, expressed via Alge-
                                         analysis and other attacks.                                                             braic Intermediate Representation (AIR) and lookup arguments [9].
                                                                                                                                 Even a single missing or incorrect constraint can introduce criti-
                                                                                                                                 cal vulnerabilities: under-constrained systems admit forged proofs,
                                                                                                                                 while over-constrained systems reject valid executions. Real-world
                                                                                                                                 zkVMs have exhibited both failure modes; for instance, an under-
                                                                                                                                 constrained bug in RISC Zero was severe enough to warrant a
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   $50,000 bounty [24].
                                         CCS ’26, The Hague, Netherlands                                                            Limitations of existing approaches. Existing approaches to
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2871-6/2026/11                                                      securing zkVM constraints suffer from fundamental limitations.
                                         https://doi.org/10.1145/3830454.3846593                                                 Dynamic methods such as unit testing and fuzzing uncover shallow
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                                  Hideaki Takahashi, Suman Jana, and Junfeng Yang


bugs by sampling concrete inputs [15], but offer no completeness                            variables, updates propagate locally and introduce limited over-
guarantee: subtle constraint violations hidden in the vast state space                      approximation error. Consistent with this, real-world zkVMs exhibit
of a large prime field often remain undetected, as shown in our eval-                       low connectivity: their density 𝜌 = 𝑇arith (C)/(|C| ×𝑚)—measuring
uation. Formal verification via SMT solvers is precise but brittle [16].                    the fraction of variables touched per constraint relative to a dense
Interactive theorem provers such as Lean 4 can validate constraints                         system—averages 0.140 across different backends (Appendix A).
with high assurance [17], but require substantial manual effort                             Branch-and-bound refinement then reduces the remaining error
and specialized expertise. Therefore, no existing method simultane-                         by partitioning the trace space, enabling aggressive pruning while
ously achieves scalability, automation, and high semantic coverage                          preserving soundness.
over the full constraint system, while ZEBRA trades precision for
scalable region reasoning with a fully automated pipeline.                                  Parallel branch-and-bound certification. We use interval prop-
Our approach. We reduce zkVM verification to a solution-set                                 agation to guide a branch-and-bound search over the trace lattice,
cardinality estimation problem and solve it using interval-based                            certifying solution-set cardinality. Each branch splits the trace space
branch-and-bound over a canonicalized trace space. For a fixed                              into independent subproblems, enabling natural parallelism in con-
program 𝑃 and input 𝑥, let C(𝑃, 𝑥,𝑇 ) denote the constraint system                          trast to SMT solvers. The same refinement also tightens interval
evaluated on trace 𝑇 . We define the solution set                                           bounds, reduces over-approximation error, and accelerates conver-
                                                                                           gence. This design supports localized verification: by restricting
                     S(𝑃, 𝑥) = 𝑇 C(𝑃, 𝑥,𝑇 ) .                                               inputs to a bounded region, ZEBRA can certify correctness within
We find that correctness of zkVM constraints reduces to a cardi-                            that region without requiring a global proof over all inputs. If the
nality condition on S: the system is complete if |S| ≥ 1, sound if                          search terminates with |S| = 1 it certifies local correctness; other-
|S| ≤ 1, and fully correct iff |S| = 1. Under-constrained bugs mani-                        wise, it returns concrete counterexamples. A fixed-point iteration
fest as |S| > 1; over-constrained bugs as |S| = 0. This formulation                         over local certificates formally characterizes how they compose to-
provides a unified, precise criterion for zkVM correctness.                                 ward global correctness, analogous to composing layerwise bound
   We classify the cardinality of S(𝑃, 𝑥) via the following three                           propagation in neural network verification [26] albeit at a greater
components. Rather than computing |S| exactly, we classify regions                          computational cost. We leave the implementation of this iteration
of the search space as empty, singleton, or ambiguous, enabling                             as future work focusing on local verification in this paper.
early certification without exhaustive enumeration.
                                                                                            Evaluation. We implement ZEBRA in Rust and evaluate it on 5 real-
Canonicalized table space. We eliminate representational redun-
                                                                                            world zkVM backends: Pico, SP1, Sphinx, Valida, and Ziren. ZEBRA
dancy in execution traces by introducing a canonicalization layer
                                                                                            discovers 11 previously unknown zero-day vulnerabilities, of which
that maps each trace table to a unique canonical representation.
                                                                                            6 were confirmed by developers and 3 already fixed, demonstrating
Without canonicalization, padding, row permutations, or uncon-
                                                                                            that the approach scales to production constraint systems and sur-
strained witness cells can cause the same execution to be counted
                                                                                            faces bugs that fuzzing and formal methods have missed. Our code
multiple times, rendering solution-set cardinality meaningless.
                                                                                            is publicly available at https://github.com/Koukyosyumei/ZEBRA.
   The central correctness requirement is injectivity: distinct canon-
ical representations must correspond to distinct executions, so that
                                                                                            In summary, this paper makes the following contributions:
|S| faithfully reflects the number of distinct executions. A key struc-
tural observation is that real-world zkVM designs admit canoni-                              • A canonicalization-based correctness model that reduces
calizers of a simple and uniform form—in practice requiring on                                 zkVM verification to solution-set cardinality over a canonical
average fewer than 130 lines of code per zkVM. Across five inde-                               table space. We show that real-world zkVMs admit compact
pendent zkVM implementations, we formally verify the injectivity                               canonicalizers with formally verified correctness properties in
of all canonicalizers in Lean 4,1 establishing that canonicalization                           Lean, ensuring that solution-set cardinality reflects the number
is well-defined over equivalence classes of traces and preserves                               of distinct executions rather than representational artifacts.
solution-set cardinality.
                                                                                             • Sound interval propagation over polynomial constraints in
Sound interval propagation. We evaluate constraints over in-                                   a modular field, enabling over-approximate reasoning about
terval ranges instead of exact finite-field values, soundly over-                              feasible executions with formal soundness guarantees.
approximating all feasible executions. Modular arithmetic creates
                                                                                             • A parallel branch-and-bound algorithm for cardinality clas-
the main challenge: wrap-around at the field characteristic breaks
                                                                                               sification that either uncovers vulnerabilities or certifies local
standard interval behavior, so we design conservative propagation
                                                                                               correctness by proving that the solution set is empty or single-
rules that preserve soundness. During branch-and-bound search, if
                                                                                               ton within a bounded input region, rather than merely testing
propagation eliminates all interval assignments, then S(𝑃, 𝑥) = ∅;
                                                                                               for the existence of satisfying traces.
if all remaining assignments collapse to a singleton region, then
|S(𝑃, 𝑥)| = 1.                                                                               • Empirical evaluation identifying 11 zero-day vulnerabilities
    Our interval propagation benefits from the sparsity of zkVM                                in widely deployed zkVM projects.
constraint systems, which designers maintain to reduce verifica-
tion cost. Because each constraint touches only a small subset of                           2   Background
1We verify these properties at the algorithmic specification level; verifying full imple-   This section reviews the foundations of Zero-Knowledge Proof
mentation correctness in Lean is orthogonal and left to future work.                        (§ 2.1) and Zero-Knowledge Virtual Machine (§ 2.2).
Efficient Branch-and-Bound Testing and Verification of zkVMs                                                                                                  CCS ’26, November 15–19, 2026, The Hague, Netherlands


                               Program                     Input                      clk pc opcode     operand       ...
                             (a.k.a.   )               (a.k.a.         )
                                                                                      0   0 IMM32 Assets
                                                                                                   [-4, 3, 0, 0, 0]   ...         addr clk is_read is_write val     ...
                           pc opcode    operand         offset value                                                                                                                                             Accept
                                                                                      1   4 ADD32 [-8, -4, 1, 0, 1]   ...          -8   1    0            1     4   ...
Source Code                      Assets
                           0 IMM32 [-4, 3, 0, 0, 0]       0Assets12                                                                              Assets                                  Proof                     or
              Compiler     4 ADD32 [-8, -4, 1, 0, 1]      1     43         Executor           op_a op_b result              ...    -4   0    0            1     3   ...   Prover                      Verifier   Reject
                                                                                                       Assets
                                                                                                                                   -4   1    1            0     3   ...
                                                                                               3    1       4               ...
                                                                                                                                                                                   I have correctly
                                                                                                                                                                                     executed this
                             Instance Tables:                                                                                                                                          program
  Inputs                                                                                                  Trace Tables:


Figure 1: Typical workflow of a zkVM. The compiler converts source code into instance tables (Tinst ), which the executor expands
into trace tables (Ttrace ) representing the full execution history. If Ttrace satisfies all algebraic constraints with respect to Tinst ,
the prover can generate a final proof to convince the verifier that the target program was executed correctly.


2.1        Zero Knowledge Proof (ZKP)                                                                          them [8, 13, 29]. The prover generates a proof that all constraints
A Zero-Knowledge Proof (ZKP) is a protocol where a prover con-                                                 hold, which the verifier can succinctly check.
vinces a verifier that a statement 𝑅(𝑥, 𝑤) is true without revealing
anything beyond its validity [18]. It satisfies completeness, sound-                                         Example of Arithmetization. Consider a simplified execution
ness, and zero knowledge: completeness means true statements                                                 trace for a program consisting of three instructions: STORE -4 3,
are accepted, soundness means false statements are rejected except                                           which writes the immediate value 3 to memory address -4; STORE
with negligible probability, and zero knowledge means the proof                                              -8 1, which writes the value 1 to address -8; and ADD -12 -4
reveals nothing about 𝑤.                                                                                     -8, which reads from addresses -4 and -8, then writes the sum 4
                                                                                                             to address -12. The table column design is based on Valida [29],
ZK Programming. A ZKP system requires users to represent the                                                 whereas many columns are omitted.
target statement as polynomial constraints 𝐶, which is complex and                                              1. Program Table (𝑇prog ) is a read-only instance table that defines
error-prone, as high-level logic does not map directly to polyno-                                            the compiled machine code. Each row specifies the instruction
mial constraints. ZK DSLs such as Circom [4] and Noir [3] address                                            (opcode) and its associated destination (dst) and source (src1,
this by letting developers specify both witness computation P and                                            src2) operands. A lookup constraint between the CPU Table 𝑇CPU
constraints C, which are then compiled into executable code and                                              ensures that every instruction executed in (𝑇CPU ), defined by the
constraint systems. Despite this, maintaining consistency between                                            tuple (pc, opcode, dst, src1, src2), actually exists within 𝑇prog .
computation and constraints is difficult due to complex DSLs and                                                2. CPU Table (𝑇CPU ) serves as the main dynamic execution trace,
finite-field arithmetic, leading to bugs that cause under-constrained                                        where each row captures the current program counter (pc), the
or over-constrained circuits and resulting vulnerabilities.                                                  instruction being executed, and the values (val1, val2, res) pro-
                                                                                                             cessed during that cycle. Local AIR constraints ensure basic CPU
2.2        Zero Knowledge Virtual Machine (zkVM)                                                             logic, such as the validity of control flow and clock transitions, re-
While traditional ZK programming systems require developers to                                               quiring that next.pc = curr.pc + 4 and next.clk = curr.clk + 1.
learn new DSLs and define arithmetic circuits for specific tasks, a                                             3. ADD Table (𝑇Add ) validates arithmetic correctness. When the
Zero-Knowledge Virtual Machine (zkVM) provides a more general-                                               CPU executes an ADD instruction, a lookup constraint ensures that
purpose abstraction by enabling the proof of execution for any                                               the tuple (val1, val2, res) exists in 𝑇𝐴𝑑𝑑 as (a, b, c), where the AIR
program written in a standard high-level language (e.g., Rust, C++,                                          constraint a + b = c holds.
or Go). A zkVM typically adopts a modular architecture consist-
ing of a guest program, a prover, and a verifier (see Fig. 1). After
the execution of a guest program, a prover of a zkVM produces a                                                3        Threat Model & Motivating Example
cryptographic proof attesting that the guest program was correctly                                            Threat Model. This work focuses on soundness and completeness
executed, and the verifier can check its correctness succinctly.                                              violations in zkVMs arising from incorrect or incomplete constraint
                                                                                                              specifications. Our adversary exploits flaws in the constraint sys-
Trace Tables. A zkVM targets a specific ISA (e.g., RISC-V or custom
                                                                                                              tem to either (i) produce invalid execution traces that nevertheless
ones like Cairo [12] and Valida [29]) and executes compiled machine
                                                                                                              satisfy the constraints (under-constrained behavior), or (ii) cause
code to produce execution traces of state transitions. These traces
                                                                                                              valid executions generated by the VM executors to be rejected by
are encoded as finite-field matrices called trace tables, where each
                                                                                                              the constraints (over-constrained behavior).
row represents an execution event, and each column represents a
                                                                                                                  We explicitly exclude infrastructure-level issues, including bugs
machine state component, such as the clock. Static data like binaries
                                                                                                              in the compiler, executor, prover, or verifier implementations, as
and public inputs are also treated as read-only instance tables.
                                                                                                              well as attacks on the cryptographic protocol itself. We also ex-
Arithmetization of the VM. A zkVM converts execution logic into                                               clude zero-knowledge leakage, as confidentiality guarantees are
polynomial constraints over trace tables to prove correctness with-                                           application-specific and orthogonal to the correctness of the con-
out revealing traces. Modern zkVMs use two types of constraints:                                              straint satisfaction [28].
Algebraic Intermediate Representation (AIR) constraints [5, 14] en-                                           Motivating Example. Before presenting the technical details, we
force local transitions between rows, and lookup constraints en-                                              illustrate a simplified yet representative bug to build intuition for
sure global consistency across tables by matching entries between                                             how our method identifies constraint bugs.
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                                                                 Hideaki Takahashi, Suman Jana, and Junfeng Yang



    clk pc   op val1 val2 res ...
                                                               clk pc     op val1 val2 res                     ...      Let winst = (𝑤𝑠1 , . . . , 𝑤𝑠𝑘 ) and wtrace = (𝑤𝑑1 , . . . , 𝑤𝑑𝑚 ) be the
                                                              [0, p] 0 STR Assets
                                                                             3    0                   [0, p]   ...
    0   0 STR Assets
                3    0       3   ...                                                                                 column widths of 𝑘 instance tables and 𝑚 trace tables, respectively.
                                                              [0, p] 4 ADD         3        1         [0, p]   ...
    1   4 ADD      3    1    4   ...
                                                                          Branch (1st row's clk)
                                                                                                                     The spaces of instance and trace tables are then defined as:
                               ← Missing constraint                                                                                    𝑘                                  𝑚
                                                                                                                                       Ö                                  Ö
                                                                                                                                             (F𝑤𝑠𝑖 ) ∗,                         (F 𝑑 𝑗 ) ∗ .           (1)
                                                 clk     pc    op val1 val2 res                 ...                                                                                𝑤
                   a   b
                     Assets
                            c                                                                                                     S=                                D=
                   3   1    4                   [0, p/2] 0 STRAssets
                                                                3    0                 3        ...
                                                                                                                                       𝑖=1                                𝑗=1
                                                [0, p]   4 ADD        3      1     [0, p]       ...
    zkVM                                                       Branch
                                                                                                                     4.2    Constraint System
                                       clk pc    op val1 val2 res            ...
                                                                                                                     A zkVM proves correctness of execution by enforcing algebraic
                                                                                                    Interval
    This trace satisfies the
                                       0   0 STR Assets
                                                  3     0             3      ...                    Singleton
                                                                                                                     constraints over trace tables, formally defined as follows.
    constraint, indicating that the
    zkVM is under-constrained.         1   4 ADD         3      1   [0, p]   ...                 p: Prime
                                                                                                                       Definition 4.1 (AIR-Lookup-based zkVM Constraints). For-
                                                                                                                     mally, a constraint system in a zkVM is a function C : S × D →
Figure 2: Motivating Example. Missing constraint allows mul-                                                         {True, False}, which is defined as
tiple satisfying tables, leading to under-constrained bugs that                                                           C(Tinst, Ttrace ) =
ZEBRA can identify via branch-and-bound. Green values in-
                                                                                                                                                                               ) (2)
                                                                                                                           Û                  Û
dicate intervals.                                                                                                              𝐴(T       ) ∧
                                                                                                                                     trace        𝐿(T , T   ) ∧ 𝑃𝑉 (T , T
                                                                                                                                                           inst   trace                inst    trace
                                                                                                                           𝐴∈ A                   𝐿∈ L
                                                                                                                     Here, A denotes a set of AIR constraints, which enforce local transition
                                                                                                                     rules between consecutive rows of trace tables, L denotes a set of
   Consider a simple program with two instructions: STORE and ADD,                                                   lookup constraints enforcing global consistency across tables, and 𝑃𝑉
where the inputs to ADD are concretely given: 3 and 1 (see Fig. 2).                                                  is a public value constraint that directly inspects the public tables.
In this case, the constraint linking the ADD result to the CPU state
contains a zkVM constraint bug: while the system enforces that                                                          Note that while AIR and lookup constraints are used to generate
(val1, val2, res) appears in the ADD table, it does not enforce that                                                 cryptographic proofs, and therefore must satisfy certain algebraic
res is uniquely determined by val1 and val2 . As a result, in addition                                               formats, the public value constraint is an auxiliary function that
to the intended execution trace {val1 : 3, val2 : 1, res : 4}, a second                                              directly checks properties of public tables and can be arbitrary.
trace {val1 : 3, val2 : 1, res : 7} also satisfies the constraints,
indicating an under-constrained violation.
                                                                                                                     4.3    Bugs in zkVMs
   ZEBRA reasons about sets of executions by lifting table cells                                                     To define bugs precisely, we reason about canonical trace tables,
to intervals. For the ADD step, we initialize res ∈ [0, 𝑝 − 1]. In                                                   which uniquely represent execution traces. This avoids multiplic-
a correct system, constraint propagation enforces res = val1 +                                                       ities caused by padding, permutation, or other representational
val2 = 4, collapsing the interval to the singleton [4, 4]. In the                                                    redundancies in trace tables. For example, a zkVM might pad a trace
buggy system, there are multiple values (e.g., 4 and 7) satisfy the                                                  table with empty rows to match a power-of-two height. Both the
constraints, enabling ZEBRA to detect the under-constrained bug                                                      unpadded and padded versions might satisfy constraints, but they
by producing multiple concrete traces satisfying the constraints.                                                    represent the same execution trace. Our canonicalization ensures
   While this motivating example assumes that the program and                                                        these are treated as the same trace table. The detailed modeling and
input are concrete values, § 5.5 shows ZEBRA can handle the case                                                     construction of canonical trace tables is deferred to § 4.4.
when they are given as range intervals.                                                                                  Let D̂ ⊆ D denote the set of canonical trace tables, and we define
                                                                                                                     a canonical solution set, which is the set of all canonical trace tables
                                                                                                                     that satisfy the constraints for the fixed instance tables.
4       Definitions of zkVM Vulnerabilities
This section introduces a formal model of constraint systems and                                                        Definition 4.2 (Canonical Solution Set). For a given instance
bugs in zkVMs. Our model abstracts away prover and cryptographic                                                     table Tinst ∈ S, we define its canonical solution set as
details, focusing instead on the semantic relationship between in-                                                             Q (Tinst ) = {Ttrace ∈ D̂ | C(Tinst, Ttrace ) = True}.                  (3)
stance tables, trace tables, and constraints. This abstraction enables
                                                                                                                        We first define the local completeness and soundness properties
a precise classification of under-constrained (soundness) and over-
                                                                                                                     of the constraints in zkVMs, which are desired properties of the
constrained (completeness) bugs in the constraint systems of zkVM.
                                                                                                                     constraints of the zkVM for the fixed instance tables.

4.1          Instance and Trace Tables                                                                                  Definition 4.3 (Local Completeness). We say the constraint C
                                                                                                                     in a zkVM is locally complete for the instance tables Tinst if
Let F be a finite field used by the zkVM to represent scalar values.
For a positive integer 𝑤, we write (F𝑤 ) ∗ to denote the set of matrices                                                               ∃ Ttrace ∈ D. C(Tinst, Ttrace ) = True                          (4)
over F with 𝑤 columns and an arbitrary number of rows.                                                                  Definition 4.4 (Local Soundness). We say the constraint C in
   We distinguish between instance, which encodes execution-invariant                                                a zkVM is locally sound for the instance tables Tinst if
data such as the program binary and public inputs, and trace tables,
                                                                                                                                                      |𝑄 (Tinst )| ≤ 1                                 (5)
which record execution-dependent data like the CPU table. For the
purposes of this formalization, it is assumed that the given program                                                    Based on the above desired properties, we classify zkVM bugs
binary represents a deterministic program.                                                                           according to the cardinality of the canonical solution set Q (Tinst ).
Efficient Branch-and-Bound Testing and Verification of zkVMs                                                CCS ’26, November 15–19, 2026, The Hague, Netherlands


   Definition 4.5 (Over-Constrained zkVM). We say the con-                           5     ZEBRA: Design
straint C is locally over-constrained for Tinst if |Q (Tinst )| = 0.                 The primary challenge in testing and verifying zkVMs lies in the
Under our threat model, the execution trace generated by the VM                      massive, non-linear constraint system C defined over multiple trace
executor for the program and input encoded in 𝑇inst is a valid execu-                tables. ZEBRA addresses this by shifting from individual-witness
tion. Thus, |𝑄 (𝑇inst )| = 0 means that the constraint system rejects                sampling to an integer interval lattice: modeling trace cells as in-
this valid execution trace, and is thus over-constrained for 𝑇inst .                 tervals allows the branch-and-bound method to formally and effi-
                                                                                     ciently certify whole regions of the search space at once.
   Definition 4.6 (Under-Constrained zkVM). We say the con-
straint C is locally under-constrained for Tinst if |Q (Tinst )| > 1.                5.1    Localized Verification
This means that multiple distinct execution traces satisfy the con-                  Instead of attempting to verify the global correctness of the entire
straint for the same program and inputs, enabling unsound proofs.                    VM at once, we isolate a specific target table𝑇target ∈ D𝑖 . In this local-
                                                                                     ized mode, we assume the peripheral tables Trest = Ttrace \ {𝑇target }
                                                                                     are semantically correct and consistent with the static instance
4.4     Canonical Representation
                                                                                     tables 𝑇inst . This allows us to derive a localized constraint func-
To formally reason about the uniqueness of solutions in 𝑄 (Tinst ), we               tion C by partially evaluating C on the fixed witness: C(𝑇target ) =
must ensure that the trace tables in D map 1-to-1 with execution                     C(Tinst, Trest ∪ {𝑇target }). This modularity allows ZEBRA to bypass
traces. In practice, a zkVM might introduce representational re-                     the complexity of global consistency proofs while exhaustively
dundancies, such as padding rows or permuting non-deterministic                      verifying the arithmetic correctness of individual units.
lookup tables, which could artificially inflate the cardinality of
𝑄 (Tinst ) without representing a true logic bug. We resolve this by                 5.2    The Trace Interval Lattice
defining a canonical space D̂ ⊆ D that filters out such artifacts.
                                                                                     We model the search space for 𝑇target as a lattice of integer intervals.
    We first introduce the set of semantic execution records E, and
                                                                                     This choice is motivated by the observation that complex zkVM
the canonicalizer R : D → E that maps trace tables to a set of
                                                                                     constraints can be soundly approximated on intervals, enabling
execution records. Intuitively, R replays the trace tables to obtain
                                                                                     efficient and parallel traversal of the entire search space.
the set of execution records E, abstracting away the redundancy.
                                                                                        We first introduce the following notations:
Specifically, we view that R is a union of canonicalizers for each
                                                                                        1) Integer Interval: Each cell is abstracted as an integer interval,
table, i.e., R (Ttrace ) = R cpu (𝑇cpu ) ∪ R add (𝑇add ) ∪ R mul (𝑇mul ) ∪ · · · .
                                                                                     where a set of intervals is denoted as I = {[𝑎, 𝑏] ∈ Z × Z | 𝑎 ≤ 𝑏}.
    For example, consider an ALU Add Table with columns for inputs
                                                                                        2) Interval Matrix Let 𝑇e ∈ I𝐻 ×𝑊 denote an interval matrix,
(a, b), output (res), carry bits (c), and a selector (s). While the raw
                                                                                     where each cell 𝑇e𝑖,𝑗 is filled with an integer interval 𝐼𝑖,𝑗 . This 𝑇e
table 𝑇Add includes all these columns with dummy padding rows
                                                                                     serves as a search state in our ZEBRA.
(where s = 0), the canonicalizer R acts as a semantic projection:
                                                                                        Since the integer domain Z forms a lattice naturally with the
         R Add (𝑇Add ) = {(a𝑖 , b𝑖 , res𝑖 ) | row𝑖 ∈ 𝑇Add ∧ s𝑖 = 1}           (6)    partial order given by inequality, the meet by min, and the join by
                                                                                     max, the set of all such states 𝑇e itself forms a lattice [10], under the
By filtering out internal witnesses (e.g., c) and padding, and nor-
                                                                                     partial order of interval inclusion (𝑇e ⊑ 𝑇e′ if ∀𝑖, 𝑗 . 𝑇e𝑖,𝑗 ⊆ 𝑇e𝑖,𝑗
                                                                                                                                                         ′ ).
malizing the permutation, R maps different raw representations of
                                                                                        3) Interval-to-Field Embedding: To bridge the gap between
the same computation to a unique record set.
                                                                                     the finite field and integer interval, we introduce the interval-to-
   Definition 4.7 (Semantic Eqivalence of Trace Tables). We                          field embedding of the integer interval J·K𝑝 : I → 2F𝑝 by: J𝐼 K𝑝 =
define a binary relation ∼ R on D derived from the canonicalizer R.                  {𝑥 mod 𝑝 | 𝑥 ∈ Z 𝑠.𝑡 . 𝑎 ≤ 𝑥 ≤ 𝑏}. This is also naturally extended
Two sets of dynamic traces T1, T2 ∈ D are semantically equivalent if                 to the embedding for a table: J𝑇eK𝑝 = {𝑇 | ∀𝑖, 𝑗 . 𝑇𝑖,𝑗 ∈ J𝑇e𝑖,𝑗 K𝑝 }.
and only if they reconstruct to the same execution record:
                                                                                     5.3    Sound Over-approximation of Constraints
                    T1 ∼ R T2 ⇐⇒ R (T1 ) = R (T2 )                            (7)    This section derives the sound over-approximation for the three
                                                                                     classes of zkVM constraints: AIR, Lookups, and public value check.
We then define the canonical trace tables space as the quotient set:
                                                                                     Soundness Condition. For a localized zkVM constraint C : F𝐻  𝑝
                                                                                                                                                    ×𝑊 →

   Definition 4.8 (Canonical Trace Table Space). The space of                        {True, False}, its sound over-approximation for an integer interval
canonical trace tables, denoted D̂, is defined as the quotient set of D              is formally defined as follows:
by the relation ∼ R:
                                                                                        Definition 5.1 (Sound Over-Approximation). C         e : I𝐻 ×𝑊 →
                  D̂ := D/∼ R = {[Ttrace ] ∼| Ttrace ∈ D}                     (8)    {True, False, Uncertain} is a sound over-approximation of the con-
                                                                                     straint C : F𝐻
                                                                                                  𝑝
                                                                                                    ×𝑊 → {True, False} if for any 𝑇
                                                                                                                                  e ∈ I𝐻 ×𝑊 , it holds:
, where [Ttrace ] ∼ represents the equivalence class of traces indistin-
guishable from Ttrace by ∼ R.                                                           (1) C(
                                                                                             e 𝑇e) = True =⇒ ∀𝑇 ∈ J𝑇eK𝑝 . C(𝑇 ) = True.
                                                                                        (2) C(
                                                                                             e 𝑇e) = False =⇒ ∀𝑇 ∈ J𝑇eK𝑝 . C(𝑇 ) = False.
   By construction, there exists a natural bijection between the
                                                                                        (3) C(
                                                                                             e 𝑇e) = Uncertain whenever neither (1) nor (2) can hold.
canonical trace space D̂ and the image of the canonicalizer Im(R) ⊆
E. This ensures that every set of canonical dynamic traces corre-                    This ensures that any definitive result (True or False) returned by
sponds to a unique semantic execution trace.                                         e is globally valid for all points in the sub-lattice.
                                                                                     C
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                        Hideaki Takahashi, Suman Jana, and Junfeng Yang


AIR Constraints. AIR A consists of a set of polynomials {𝜙 1, 𝜙 2, . . . }      a set of concrete tables. Each table 𝑇𝑖 is added to the result set 𝑄
where each polynomial 𝜙 : F2𝑊 → F is defined for two consecutive                only if its canonical representation R (𝑇𝑖 ) has not been seen before.
rows. The satisfaction of A for a concrete table 𝑇 is defined as                Bug Condition. Any discrepancy in the cardinality of 𝑄 (𝑇e) signals
       A (𝑇 ) := ∀𝜙 ∈ A. ∀𝑖 ∈ {1, . . . , 𝐻 − 1}. 𝜙 (𝑇𝑖 ,𝑇𝑖+1 ) = 0    (9)      a critical vulnerability: an under-constrained bug is reported if
                                                                                |𝑄 (𝑇e)| > 1, while an over-constrained bug is flagged if |𝑄 (𝑇e)| = 0.
, where 𝑇𝑖 denotes the 𝑖-th row of the table 𝑇 .                                Framework Guarantee. The reliability of ZEBRA rests on the
   We then define the sound over-approximation 𝜙˜ using the basic               convergence and completeness properties of the branch-and-bound
interval arithmetic (see Appendix B.2 for the details). The satisfiabil-        framework applied to the interval lattice of the target table. By em-
ity of AIR over 𝑇e is over-approximated using the zero-satisfiability           ploying a sound approximation C,  e ZEBRA ensures that any region
predicate 𝑆𝐴𝑇𝑍 ( [𝐿, 𝐻 ]) ⇐⇒ ∃𝑘 ∈ Z. 𝑘𝑝 ∈ [𝐿, 𝐻 ]:                              of the search space pruned as False is mathematically guaranteed
                                                                                to contain no valid execution trace for the target component.
         
         
          True             if ∀𝜙 ∈ A. ∃𝑘 ∈ Z. 𝜙˜ (𝑇e) = [𝑘𝑝, 𝑘𝑝]                  Theorem 5.2 (Soundness and Completeness of Local Veri-
 e(𝑇e) := False             if ∃𝜙 ∈ A. ¬𝑆𝐴𝑇𝑍 (𝜙˜ (𝑇e))            (10)
         
         
 A                                                                              fication). Let C be a localized zkVM constraint system restricted
         
          Uncertain        otherwise                                           to a target table 𝑇target , given fixed instance tables Tinst and assumed
         
         
                                                                                valid peripheral trace tables Trest . Then, Algo. 1 terminates, and the
Lookup Constraints. Lookup constraints ensure consistency be-                   resulting canonical solution set 𝑄 satisfies:
tween the target table 𝑇 and auxiliary tables. We categorize these                   • Local Soundness: Every element 𝑇 ∈ 𝑄 is a concrete trace
into five types: Program, Byte, ALU, Control-Flow, and Memory.                          that satisfies the localized constraints: C(𝑇 ) = True.
Detailed constructions are in Appendix B.1. For all types, the sound                 • Local Completeness: For any concrete 𝑇 with C(𝑇 ) = True,
over-approximation L    e returns True if the interval collapses to a                   there exists 𝑇 ′ ∈ 𝑄 such that R (𝑇 ′ ) = R (𝑇 ).
valid singleton, False if the intervals are entirely disjoint from valid
                                                                                See Appendix B.4 for the proof sketch.
states, and Uncertain otherwise.
   (L-1) Program: Lprog ensures every executed instruction (PC,
opcode, operands) exists in the static program table 𝑇prog .                    Algorithm 1 Branch-and-Bound Lattice Search for zkVM
   (L-2) Byte: Lbyte enforces 8-bit range [0, 255] and bitwise consis-          Require: Localized constraints C with respect to the given in-
tency (e.g., AND, XOR). Lebyte uses bit-masking to track fixed/varying              stance tables Tinst and the target table 𝑇target
bits for tight interval bounds.                                                     eroot ← Initialize all cells in 𝑇target with interval [0, 𝑝 − 1]
                                                                                 1: 𝑇
   (L-3) ALU : Lalu validates word-level arithmetic ⋄ ∈ {+, −, ×, ÷, . . . }.    2: Queue.push(𝑇         eroot ),    Q←∅                    ⊲ Initialization
Lealu leverages opcode-specific interval approximations ⋄˜ to detect             3: while Queue is not empty do
arithmetic soundness violations.                                                 4:     𝑇e ← Queue.pop()
   (L-4) Control-Flow: Lcf verifies the transitions of program coun-             5:      flag ← C(   e 𝑇e)
ters pc′ = cf ◦ (pc, 𝑎, 𝑏, 𝑐). L
                               ecf lifts the transition function to its          6:      if flag = False then continue                             ⊲ Pruned
interval-based counterpart cf  f◦ .                                              7:      else if flag = True then                                 ⊲ Certain
   (L-5) Memory: Lmem enforces global Read-After-Write consis-                   8:           {𝑇1,𝑇2, ..} ← Concretize(𝑇e)
tency and zero-value initialization. L     emem models a memory by               9:           Q ← Q ∪ { 𝑇𝑖 | 𝑇𝑖 ∈ {𝑇1,𝑇2, ..}, ∀𝑞 ∈ Q, R (𝑞) ≠ R (𝑇𝑖 )}
dynamically splitting address segments to track value intervals                 10:      else                                                  ⊲ Uncertain
across the execution timeline.                                                  11:           (𝑖, 𝑗) ← SelectCellToSplit(𝑇e)
Public Value Check. Public value constraint 𝑃𝑉 inspects the pub-                12:           (𝑇e𝑙𝑒 𝑓 𝑡 , 𝑇e𝑟𝑖𝑔ℎ𝑡 ) ← SplitInterval(𝑇e𝑖,𝑗 )
lic parts of tables, such as the final execution state, including the           13:          Queue.push(𝑇e𝑙𝑒 𝑓 𝑡 ), Queue.push(𝑇e𝑟𝑖𝑔ℎ𝑡 )
final program counter and exit code. Most of these constraints are              14: if |Q| > 1 then Found Under-Constrained Bug
simple equalities (=) or non-equalities (≠), and they can be evaluated          15: if |Q| = 0 then Found Over-Constrained Bug
over the integer interval domain in the same way as AIR.

5.4     Lattice Branch-and-Bound Search
Algo. 1 systematically explores the lattice from the initial state 𝑇eroot
                                                                                5.5    Input Range Verification
toward concrete traces. One of the natural choices of initial interval          We apply input range verification to instruction tables, such as ALU
is [0, 𝑝 − 1], where 𝑝 is the prime order of the finite field F𝑝 .              and Control-Flow tables, whose columns cleanly partition into in-
                                                                                puts, output, and other auxiliary cells. Under a sound and complete
Basic Workflow. The algorithm maintains a queue of search states.
                                                                                constraint system, fixing the inputs determines a unique canonical
In each iteration, it 1) SelectCellToSplit(𝑇e) selects a state 𝑇e and a
                                                                                row: local soundness forces at most one satisfying assignment to
"divisible" cell 𝑇e𝑖,𝑗 , where an interval [𝑎, 𝑏] is considered divisible       the output, and local completeness forces at least one.
if 𝑎 ≠ 𝑏; 2) SplitInterval(𝑇e𝑖,𝑗 ) branches by splitting the interval 𝑇e𝑖,𝑗        To verify a range, we initialize the inputs with a broad interval
into 𝑘 smaller intervals {𝐼 1, . . . , 𝐼𝑘 }, and ;3) C
                                                     e evaluates the new        [𝐿, 𝑅] rather than a singleton value. Because our branch-and-bound
states. If C(
           e 𝑇e) = False, the entire sub-lattice is discarded, efficiently      algorithm maintains a total cover of the search space, it systemati-
pruning the search space. When C(      e 𝑇e) = True, 𝑇e is concretized into     cally partitions this range until every valid execution trace is found
Efficient Branch-and-Bound Testing and Verification of zkVMs                                    CCS ’26, November 15–19, 2026, The Hague, Netherlands


and canonicalized. Let I𝑖𝑛 be the set of inputs initialized with in-      requirements or utilize row permutations. Without normalizing
tervals, and let 𝑉 = 𝐼 ∈ I𝑖𝑛 |𝐼 | be the total number of discrete input   these variations, a solver would report an inflated cardinality for 𝑄,
                     Î
combinations within that range. If the constraint system is perfectly     leading to false-positive under-constrained bug reports.
sound and complete, each unique input combination should corre-              To address this, ZEBRA utilizes a canonicalizer (R) to project raw
spond to exactly one semantically distinct execution trace. ZEBRA         trace tables into unique sets of semantic execution records. This
evaluates the correctness of the range by comparing the cardinality       function acts as a semantic filter, ignoring internal helper columns
of the resulting canonical solution set |𝑄 | with the expected volume     and padding while normalizing permutations.
𝑉 : sound and complete if |𝑄 | = 𝑉 ; under-constrained if |𝑄 | > 𝑉 ;         For tables representing each ALU and control-flow instruction,
over-constrained if |𝑄 | < 𝑉 .                                            the canonicalized representation of a single row is implemented as a
                                                                          tuple of the current program counter, the next program counter, and
6     ZEBRA: Implementation                                               all operands, which sufficiently captures the input and the output
We implement ZEBRA as a high-performance localized verification           effect of each instruction (see Fig. 8 for the example pseudocode).
engine in approximately 4,500 lines of Rust.                                 For tables that manage memory instructions such as LW and SW,
                                                                          the canonicalized representation of each row is a tuple of columns
6.1      Automated Constraint Extraction                                  corresponding to accessed memory values and immediates.
                                                                             The CPU table canonicalizer focuses on reconstructing the uni-
ZEBRA automates the extraction of arithmetic constraints from
                                                                          fied timeline of execution. Each row is projected into a tuple com-
source code of Plonky3-based zkVMs using a dual-path architecture:
                                                                          prising the clock cycle, the program counter, and a record of mem-
a macro-based engine for AIR and static semantic lifting for lookups.
                                                                          ory writes performed during that cycle.
The framework is highly extensible; adapting ZEBRA to a new
zkVM requires around 500 lines of tailored code.                          Formalized correctness in Lean 4. We formalize the canonicalizer
AIR Extraction via Rust Macros. To handle diverse zkVM forks,             design in Lean 4 and verify its key correctness properties at the level
ZEBRA uses a unified Rust macro interface that intercepts sym-            of the algorithmic specification. The development assumes that, for
bolic execution. This automatically captures symbolic nodes (e.g.,        each zkVM, the trace-table generator records every execution step
Add, Mul, IsTransition) directly from AIR definitions, ensuring           as a non-padding row, with no spurious or missing records. Under
compatibility across heterogeneous implementations.                       this assumption, we prove three properties.
Lookup Extraction and Semantic Lifting. ZEBRA statically                     First, generator-independence: any two generators satisfying this
analyzes cross-table value transfers, which are implemented as            assumption produce the same canonical form for a given execution,
channel-based virtual buses, and reconstructs their functional intent     ensuring that representational artifacts such as padding and row
into semantically equivalent symbolic constraints (Fig. 3).               permutations are absorbed by R. Second, a constructive bijection be-
                                                                          tween the canonical trace space and the image of the canonicalizer,
Public Value and Extensibility. Public value constraints, typi-
                                                                          establishing that canonical representations correspond one-to-one
cally simple checks in standard Rust, are manually rewritten in our
                                                                          with trace equivalence classes. Third, injectivity with respect to
symbolic representation.
                                                                          distinct executions, which underpins the cardinality criterion of
                                                                          § 4.3: distinct executions map to distinct canonical forms, so |𝑄 |
                                                                          counts distinct executions rather than representational variants.
      clk op                                                   ...
                                 Assets                                      The framework is instantiated for the concrete column layouts of
       ... ... ... ... ... ... ... ... ... ... ... ... ... ... ...
                                                                          each evaluated zkVM; see Appendix C.1 for the formal statements.
                       receives an instruction tuple when op=ADD

                                                                          6.3    Search Optimization
                                                               ...
                                     Assets                               The search space for zkVM trace tables is inherently high-dimensional,
               ... ... ... ... ... ... ... ... ... ... ... ... ...
                                                                          often involving thousands of cells in a table. To ensure that ZEBRA
      convert to symbolic expr                                            can traverse this lattice within practical time limits, we implement
                                               =                          several systems-level optimizations, including parallel execution,
                                                                          heuristic prioritization, and strategic initialization.
Figure 3: The CPU table offloads complex operation con-                   Parallelization. The search process is implemented as a multi-
straints to auxiliary tables such as the ADD table, by connect-           thread parallelized algorithm. Multiple worker threads concurrently
ing their columns via a channel, and ZEBRA converts them                  pop candidate tables from a global queue, evaluate (C̃), and execute
into semantically equivalent constraints.                                 recursive partitioning. If a thread determines that a sub-lattice is
                                                                          False, it immediately discards the entire branch and steals the next-
                                                                          highest-priority candidate from the queue.
6.2      Canonicalization                                                 Backward Refinement. To accelerate the convergence of the
A significant challenge in zkVM verification is representational re-      branch-and-bound search, ZEBRA implements Backward Inter-
dundancy, where multiple distinct matrices may represent the same         val Refinement, which propagates constraints in reverse to shrink
execution trace due to implementation-level artifacts. For instance,      the search space, based on common patterns in real-world zkVMs:
a zkVM might pad a trace table with empty rows to satisfy height          Conditional Constant-Gate, Conditional Variable-Gate, and Affine
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                    Hideaki Takahashi, Suman Jana, and Junfeng Yang



      𝐼𝑠 = [1, 1]   𝑠 · (𝑣 − [𝜏, 𝜏]) = 0                                      number of constraints that are already definitively satisfied over the
                                            (Conditional-Const-Gate)          corresponding interval region. We call a state almost valid when
                𝐼 𝑣 ← 𝑣 ∩ [𝜏, 𝜏]
                                                                              𝜂 (𝑇e) is close to | C|.
                                                                                                   e Because an under-constrained bug manifests
              𝐼𝑠 = [1, 1] 𝑠 · (𝑎 − 𝑏) = 0                                     as a second, distinct satisfying trace, regions in which most con-
                                                    (Conditional-Var-Gate)
                       𝐼𝑎 , 𝐼𝑏 ← 𝑎 ∩ 𝑏                                        straints are already satisfied are heuristically more likely to yield
 𝐼𝑎 = [𝑎𝑙𝑜 , 𝑎ℎ𝑖 ] 𝐼𝐿 = [ℓ, ℎ] 𝐼𝑒 = [𝑒𝑙𝑜 , 𝑒ℎ𝑖 ]                              such a trace after further refinement than regions in which fewer
      𝑎 = 𝐿 − 𝑑 · 𝑒 𝑑 > 0 𝑎, 𝑒 ∉ FV(𝐿)                                        constraints are definitively satisfied. This score affects only the
|ℓ | + |ℎ| + 𝑑 (|𝑒𝑙𝑜 | + |𝑒ℎ𝑖 |) + |𝑎𝑙𝑜 | + |𝑎ℎ𝑖 | < 𝑝                        order in which states are explored and is never used to prune a
                                                  (Affine-Backward)     region; therefore, it does not affect soundness or the set of states
                       ℓ − 𝑎ℎ𝑖       ℎ − 𝑎𝑙𝑜
       𝐼𝑒 ← 𝐼𝑒 ∩                  ,                                           explored when the search runs to completion.
                            𝑑            𝑑
                                                                                  Warm-Starting: ZEBRA can also leverage domain knowledge of
                                                                              the virtual machine. In particular, the search can be warm-started
Figure 4: Rules for Backward Refinement. FV(𝐿) is a set of                    by initializing the lattice near the "honest" execution trace produced
free variables in an expression 𝐿.                                            by the VM’s executor. This initialization allows the tool to quickly
                                                                              determine whether a second, conflicting witness exists by exploring
                                                                              the neighborhood of a known valid execution.
Backward Refinement. We denote the interval assigned for a vari-
able 𝑥 by 𝐼𝑥 , and the interval evaluated for an expression 𝐿 by 𝐼𝐿 .
See Fig. 4 for the formal inference rule and Appendix C for proofs.           7   Evaluation
    (BR-1) Conditional Constant-Gate: A common pattern in zkVM                We conduct a comprehensive evaluation to answer the following
arithmetization is the use of a selector variable (𝑠) to gate a specific      research questions:
constraint. For instance, a constraint might enforce that a register          RQ1: How effectively can ZEBRA locally verify real-world zkVMs
𝑣 must equal a target constant 𝜏 only when 𝑠 = 1. ZEBRA auto-                 at a given input point?
matically detects this pattern and shrinks the interval of 𝑣 to its           RQ2: How effectively can ZEBRA locally verify real-world zkVMs
intersection 𝑣 ∩ [𝜏, 𝜏]. If the intersection 𝑣 ∩ [𝜏, 𝜏] is empty, the         over a given input range?
branch is immediately pruned as unsatisfiable.                                RQ3: How does increasing the number of parallel workers affect
    (BR-2) Conditional Variable-Gate: Another popular pattern is              ZEBRA’s verification throughput?
conditional equality used to represent register-to-register moves or          RQ4: What is the contribution of each optimization to the verifica-
alias resolution. ZEBRA replaces the intervals for both 𝑎 and 𝑏 with          tion performance of ZEBRA?
their intersection 𝑎 ∩ 𝑏, and prunes the state if they are disjoint.          RQ5: Can ZEBRA uncover previously unknown bugs in real-world
    (BR-3) Affine Backward Refinement: The third common pattern               zkVM implementations?
is the affine relation. In many zkVMs, a value is decomposed into             RQ6: How does the bug-detection performance of ZEBRA compare
smaller limbs or quotients, and they are modeled as affine relations          to existing fuzzers?
of the form 𝑎 = 𝐿 − 𝑑 · 𝑒, where 𝑎 is a remainder or low-limb                 Benchmarks. We evaluate ZEBRA on five real-world zkVMs imple-
variable, 𝐿 is an affine symbolic expression (independent of 𝑎 and            mented using Plonky3: Pico [7], SP1 [27], Sphinx [1], Valida [19, 30],
𝑒), 𝑒 is a quotient variable, and 𝑑 > 0 is a constant stride. Given           and Ziren [23]. These systems were selected based on their popu-
the current interval bounds for the affine expression 𝐼𝐿 = [ℓ, ℎ], the        larity, measured by the number of GitHub stars and forks. Pico, SP1,
limb 𝐼𝑎 = [𝑎𝑚𝑖𝑛 , 𝑎𝑚𝑎𝑥 ], and the variables 𝑎 and 𝑒 do not occur free         and Sphinx target the RISC-V architecture, Ziren targets MIPS, and
in 𝐿, we can derive tighter bounds for the quotient 𝑒.                        Valida targets a custom instruction set architecture (ISA). Our study
Certified Circuit Elision. Many zkVMs use range-check circuits                focuses on verifying and testing the core tables of these zkVMs, in-
to verify that four-limb field elements fit within a specific range,          cluding the CPU table, ALU tables, control-flow tables, and memory
like the BabyBear or KoalaBear range. Following best practices in             instruction tables.
formal verification, we simplify these by lifting them into dedicated         Configurations. Experiments were conducted on an Intel Xeon
IR nodes, such as BabyBearRange or KoalaBearRange. This allows                2.20GHz server with 31GB RAM running Ubuntu 22.04.3 LTS, uti-
the interval evaluator to apply immediate bounds to the variable,             lizing four worker threads by default. We distinguish between
significantly reducing the complexity of the symbolic tree and                instruction tables, which constrain the input-output effects of spe-
accelerating the pruning process.                                             cific opcodes (e.g., ALU, control-flow, and memory instruction ta-
Optimization for Detecting Under-Constrained Bugs. In addi-                   bles), and non-instruction tables, which manage global state and
tion to the general optimizations that help the search terminate as           execution flow (e.g., the CPU table and global memory table).
early as possible, we introduce two techniques specifically designed             Exhaustive verification analysis (RQ1–3) focused exclusively
to detect under-constrained bugs, which require finding satisfying            on instruction tables. We excluded non-instruction tables from
assignments as quickly as possible.                                           this exhaustive scope because their high dimensionality (60–100
    Prioritization: Rather than exploring the lattice using a naive           columns) and trace-dependent row counts make interval-based
depth-first or breadth-first strategy, ZEBRA uses a priority queue            search computationally impractical for a full proof.
to direct the search toward regions that are more likely to contain              Instead, for bug detection (RQ5-6), we expanded our scope to
valid but unintended execution traces. For each search state 𝑇e, we           include these non-instruction tables by leveraging warm-starting.
define its priority score as 𝜂 (𝑇e) ≜ 𝑐˜ ∈ Ce 1 (𝑐˜ (𝑇e) = True), i.e., the   For each table, we generate up to 30 short programs whose opcodes
                                      Í
Efficient Branch-and-Bound Testing and Verification of zkVMs                                        CCS ’26, November 15–19, 2026, The Hague, Netherlands


and operands are instantiated uniformly at random. Thus, for a             that interval approximations lack, suggesting that hybrid interval-
zkVM with 𝑛 target tables, we use up to 30𝑛 honest seed traces             SMT approaches could further improve the zkVM verification.
in total. We execute each program using the target zkVM’s native
executor and table generator to obtain one honest seed trace. During         Answer to RQ1: ZEBRA outperforms SMT verification in
the search, ZEBRA randomly selects subsets of target columns and             both efficiency and coverage, achieving a 48.0% success rate (a
incrementally increases the subset size. The selected columns are            16.5 percentage point (pp) improvement over Z3) and a 51.5×
lifted to interval domains, while the remaining cells retain their           speedup, establishing a new performance benchmark for auto-
concrete witness values from the seed trace. This warm-starting              mated ZK constraint analysis.
strategy enables ZEBRA to explore a localized neighborhood of
valid executions and identify bugs in complex, large-scale tables.
    For single-point trials, we performed 200 independent runs per
                                                                           7.2     RQ2: Range Verification Performance
(table, opcode) pair using 32-bit random operands and a 100-second         Tab. 2 reports the speedup of ZEBRA’s input range verification over
timeout. Range verification (RQ2) targeted the standard two-operand        a theoretical iterative point-wise verification baseline, where the
(𝑜𝑝_𝑏, 𝑜𝑝_𝑐) instruction format by injecting a random interval of          baseline cost for a volume |𝑉 | is computed as |𝑉 | times the mean
width 𝑟 ∈ {1, 2, 8, 32, 128} into one randomly selected limb per in-       single-point verification time from RQ1. Even at the smallest volume
put. This configuration yields a search volume proportional to 𝑟 2         |𝑉 | = 22 , ZEBRA already outperforms point-wise enumeration,
to evaluate solver convergence under uncertainty. Scalability (RQ3)        because a single interval-lattice traversal covers multiple discrete
reuses exactly the single-point opcode-wise benchmark instances            inputs with shared pruning. As |𝑉 | grows, the gap widens rapidly: at
from RQ1, with the same operands, random seeds, and timeout;               |𝑉 | = 214 , ZEBRA achieves 34.1× on SP1, 39.7× on Ziren, 42.1× on
only the number of worker threads 𝑊 ∈ {1, 2, 3, 4} is varied. We           Sphinx, 44.2× on Pico, and 63.1× on Valida. This sublinear growth in
compared ZEBRA against two baselines: the Z3 SMT solver (using             verification time with respect to volume is the core benefit of input
QF_BV logic via SMT-LIB2) and Arguzz, a mutation-based fuzzer              range verification: branch-and-bound collapses large contiguous
we extended to support our five target zkVMs (see Appendix D for           regions into a single sound judgment, whereas iterative point-wise
the detailed configurations for those baselines).                          verification pays the full verification cost at every point.
                                                                               Fig. 5 shows this effect on the ADD table across all zkVMs, plot-
                                                                           ting ZEBRA’s measured verification time against the corresponding
7.1     RQ1: Local Verification Performance                                theoretical iterative point-wise verification cost as the volume in-
Table 1 reports local verification performance under two aggre-            creases. The solid curves lie strictly below the dashed iterative
gations. Opcode-wise treats each instruction opcode as a distinct          point-wise verification references, and the vertical gap widens as
target (e.g., ADD, BEQ); table-wise groups opcodes that share a sin-       volume grows, confirming that ZEBRA verifies orders of magnitude
gle trace table (e.g., all bitwise operations folded into one Bitwise      more inputs than point-wise testing would allow; equivalently, for
table) into one entry. We use opcode-wise figures as the headline          a fixed target volume, ZEBRA reaches it substantially faster. See Ap-
figures and report table-wise figures as a robustness check.               pendix D for the SMT solver baseline for range verification, where
                                                                           the Z3 SMT solver exhibits a scalability bottleneck.
Overall Performance. At the opcode level, ZEBRA verified 48.0%
(61/127) of instruction targets, against Z3’s 31.5% (40/127), a +16.5 pp     Answer to RQ2. ZEBRA achieves substantial amortized effi-
gain. Aggregating by table widens the gap to +28.6 pp (55.8% vs.             ciency by processing input domains as unified interval lattices
27.2%), confirming that ZEBRA’s advantage is not an artifact of              rather than discrete points, yielding up to a 63× speedup over
how opcodes are bucketed. On the 31 operations that both tools               the theoretical iterative point-wise verification baseline.
certify, ZEBRA is on average 51.5× faster.

Per-zkVM Analysis. ZEBRA outperforms Z3 on every evaluated                 7.3     RQ3: Parallel Search Scalability
zkVM. The opcode-wise gap is largest on Ziren (+22.0 pp) and SP1           Tab. 3 shows speedups from 𝑊 = 1 baseline. Ziren drops from
(+18.8 pp), and remains positive on Sphinx (+16.7 pp) and Pico             0.521s to 0.246s (2.12×) at 𝑊 = 4, while SP1, Sphinx, and Pico
(+12.0 pp); on Valida the two tools tie at 18.2% opcode-wise but           achieve 1.24–1.63×, showing that ZEBRA effectively distributes
ZEBRA leads 33.3% vs. 16.7% table-wise. Valida’s lower absolute            independent sub-lattices across workers.
coverage is consistent with its bit-decomposition-heavy design,
in which several tables use up to 4× as many columns as their                Answer to RQ3. The multi-threaded parallelized algorithm
counterparts in other zkVMs; the resulting blow-up inflates the              significantly enhances ZEBRA’s throughput, providing up to a
search space for any solver operating cell-by-cell. The largest table-       2.12x speedup with 4 workers.
wise speedup, 82.4× on SP1, is driven by its jump table: ZEBRA
certifies JAL and JALR in ≈ 5 ms each, whereas Z3 spends ≈ 1.3 s.
                                                                           7.4     RQ4: Ablation Study of Optimizations
Failure Analysis. Successful verifications included simple ALU ta-         Tab. 4 shows the ablation result, where #T and #O show the number
bles, multiplication, shifts, and jumps. However, deep non-linearities,    of locally verified tables and instruction opcodes, respectively. We
such as division and multi-byte stores, remained beyond the 100s
timeout. Notably, Z3 solved the division table in Valida that ZEBRA        2 The two operations in Valida verified by ZEBRA and Z3 belong to different sets
could not, as bit-vector theory provides formal decision procedures        without any overlap.
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                                                                                                                                                                    Hideaki Takahashi, Suman Jana, and Junfeng Yang


Table 1: Local verification performance at a single input point for ZEBRA and the Z3 SMT solver. 𝑁 is the number of tables
or opcodes. Table-wise, 𝑁 𝑣 counts fully verified tables and Succ% is the fraction of verified opcodes averaged over tables;
opcode-wise, 𝑁 𝑣 and Succ% denote verified opcodes and 𝑁 𝑣 /𝑁 . Time is the average verification time. 𝑁𝑐 is the number of
instances verified by both, and Spd is the average speedup of ZEBRA over Z3 on this common set. ZEBRA achieves higher
coverage (+16.5 pp) and up to 51.5× speedup.

                                                                                                    Table-Wise                                                                                                                                                Opcode-Wise
zkVM                                                       ZEBRA                                                          SMT                                                                                                      ZEBRA                                                         SMT
                                       𝑁                                                                                                                              𝑁𝑐         Spd            𝑁                                                                                                                              𝑁𝑐     Spd
                                                 𝑁𝑣      Succ%                        Time                𝑁𝑣         Succ%           Time                                                               𝑁𝑣                        Succ%             Time          𝑁𝑣        Succ%                             Time
Valida                                 7          2       33.3%                   0.010s                   1           16.7%      0.593s                              0        NA2              11       2                        18.2%            0.010s          2           18.2%                         0.593s            0      NA
Sphinx                                 7          4       57.1%                   0.109s                   2           28.6%      1.429s                              2        4.7x             18      10                        55.6%            0.158s          7           38.9%                         1.630s            7     22.3x
 Pico                                  8          4       50.0%                   0.095s                   2           25.0%      1.117s                              2        4.0x             25      10                        40.0%            0.144s          7           28.0%                         1.274s            7     27.5x
  SP1                                  10         6       60.0%                   0.070s                   3           33.3%      4.621s                              3        82.4x            32      16                        50.0%            0.100s         10           31.2%                         2.497s            9     56.8x
 Ziren                                 12         8       66.7%                   0.239s                   2           28.2%      4.516s                              2        1.6x             41      23                        56.1%            0.246s         14           34.1%                         2.976s            8     92.2x
             All                       44        24       55.8%                   0.132s                  10           27.2%      3.339s                              9        29.8x           127      61                        48.0%            0.169s         40           31.5%                         2.204s            31    51.5x

                                                valida                                                           sphinx                                                               pico                                                              sp1                                                            ziren
                        10000             ZEBRA (bb)                                        10000          ZEBRA (bb)                                         10000           ZEBRA (bb)                                        10000          ZEBRA (bb)                                        10000          ZEBRA (bb)
                                          iterative                                                        iterative                                                          iterative                                                        iterative                                                        iterative
                                          point-wise                                                       point-wise                                                         point-wise                                                       point-wise                                                       point-wise
Verified input volume




                                                                    Verified input volume




                                                                                                                                      Verified input volume




                                                                                                                                                                                                        Verified input volume




                                                                                                                                                                                                                                                                         Verified input volume
                                          verification                                                     verification                                                       verification                                                     verification                                                     verification
                         1000                                                                1000                                                              1000                                                              1000                                                             1000

                          100                                                                 100                                                               100                                                               100                                                              100

                           10                                                                  10                                                                10                                                                10                                                               10

                            1                                                                   1                                                                 1                                                                 1                                                                1
                                10 2           10 1         100                                  10 2           10 1       100                                     10 2            10 1          100                                 10 2            10 1         100                                 10 2            10 1          100
                                       Mean verification time (s)                                       Mean verification time (s)                                         Mean verification time (s)                                       Mean verification time (s)                                       Mean verification time (s)


Figure 5: Verified input volume (y) versus mean verification time (x) for ZEBRA on the ADD table. The widening vertical gap at
larger volumes indicates that interval-lattice reasoning amortizes increasingly well as the range grows. Z3 SMT solver cannot
certify any of these tables even for a singleton input.

Table 2: Speedup of ZEBRA’s input range verification over                                                                                                                                    Table 4: Impact of Backward Refinement (BR) and Certified
the iterative point-wise baseline, across input volumes |𝑉 |.                                                                                                                                Circuit Elision (CCE). Suc% is opcode-wise average. BR and
                                                                                                                                                                                             CCE contribute to coverage by 24.4 and 11.8 pp, respectively.
                                zkVM                  |𝑉 | = 22     |𝑉 | = 26                             |𝑉 | = 210           |𝑉 | = 214
                                Valida                  3.9×         30.1×                                  49.7×                63.1×                                                                                                                             ZEBRA                                               ZEBRA
                                                                                                                                                                                               zkVM                                 ZEBRA
                                Sphinx                  2.8×         18.3×                                  35.1×                42.1×                                                                                                                             w.o. BR                                            w.o. CCE
                                 Pico                   3.0×         27.3×                                  39.5×                44.2×                                                                             #T                   #O       Suc%           #T #O Suc%                                         #T #O Suc%
                                  SP1                   1.7×         10.0×                                  28.4×                34.1×                                                        Valida                2                    2       18.2%           2   2 18.2%                                        2    2 18.2%
                                 Ziren                  2.5×         16.2×                                  31.2×                39.7×                                                        Sphinx                4                   10       55.6%           2   5 27.8%                                        4   10 55.6%
                                                                                                                                                                                               Pico                 4                   10       40.0%           2   5 20.0%                                        4   10 40.0%
                                                                                                                                                                                                SP1                 6                   16       50.0%           3   7 21.9%                                        5   12 37.5%
Table 3: Impact of parallelization on verification throughput                                                                                                                                  Ziren                8                   23       56.1%           4  11 26.8%                                        5   12 29.3%
with respect to the number of parallel worker threads 𝑊                                                                                                                                        Total               24                   61       48.0%          13 30 23.6%                                        20 46 36.2%

                                         zkVM             𝑊 =1                         𝑊 =2                𝑊 =3            𝑊 =4
                                         Valida           0.011                        0.011               0.011           0.010                                                             primary driver of verification coverage: disabling it drops coverage
                                         Sphinx           0.257                        0.168               0.166           0.158                                                             from 48.0% to 23.6% (-31 operations), with the largest losses on Ziren
                                          Pico            0.179                        0.156               0.150           0.144                                                             (-12), SP1 (-9), Sphinx (-5) and Pico (-5). CCE is more architecture-
                                           SP1            0.148                        0.123               0.105           0.100                                                             specific, reducing coverage to 36.2% (-11.8 pp, -15 operations) when
                                          Ziren           0.521                        0.271               0.260           0.246                                                             disabled. The effect is strongest on Ziren (-11) and SP1 (-4), whose
                                                                                                                                                                                             AIR constraints contain selector-multiplied sub-expressions that
                                                                                                                                                                                             CCE simplifies; Pico is unaffected, as its constraint structure is al-
conduct an ablation study to quantify the contributions of Back-                                                                                                                             ready relatively canonical. CCE also improves efficiency, cutting
ward Refinement (BR) and Certified Circuit Elision (CCE). BR is the                                                                                                                          mean verification time by up to 42% on Ziren and SP1.
Efficient Branch-and-Bound Testing and Verification of zkVMs                                    CCS ’26, November 15–19, 2026, The Hague, Netherlands



  Answer to RQ4: BR and CCE form a synergistic pipeline: BR                  Answer to RQ5. ZEBRA identified 11 previously unknown
  contributes a 24.4 pp coverage increase via search-space reduc-            bugs across five real-world zkVMs, plus 2 known design choices,
  tion, and CCE adds up to 11.8 pp through constraint simplifica-            for 13 total flagged behaviors.
  tion. Neither alone matches the full ZEBRA pipeline.
                                                                         7.6     RQ6: Comparison with Fuzzer
                                                                         Overall Detection Efficiency. We evaluate ZEBRA ’s bug-detection
                                                                         capability against Arguzz, a state-of-the-art mutation-based zkVM
7.5     RQ5: Previously Unknown Bugs                                     fuzzer. Arguzz was run for six hours per target but failed to identify
ZEBRA identified 13 under- and over-constrained behaviors across         any vulnerabilities in these benchmarks, consistent with prior limi-
the evaluated zkVMs (see Tab. 5). Of these, 11 are previously un-        tations. In contrast, ZEBRA flagged 13 under- and over-constrained
known bugs discovered via warm-started bug-finding mode; the             behaviors, 11 of them previously unknown bugs, with a 100-second
remaining 2 (IDs 11 and 13) are intentional design choices surfaced      budget applied per table (on average 900 seconds per zkVM) rather
during exhaustive verification. We classify severity into five cat-      than per discovered bug.
egories: Critical affects arbitrary programs; High affects specific      Root Cause Analysis. ZEBRA and Arguzz both target soundness
instruction families; Medium provides limited exploitability; Design     and completeness bugs in zkVM constraints. For under-constrained
Flaw denotes ISA-vs-constraint mismatches that occur only for cor-       detection, however, ZEBRA explores a strictly larger search space
rupted programs; and Design Choice denotes behaviors structurally        than Arguzz due to their structural gap. The zkVM prover pipeline
required to preserve constraint well-formedness.                         composes two stages: an executor 𝐸 mapping a program to an exe-
   ID 1 is a critical under-constrained bug in Valida where the          cution trace, and a table generator 𝐺 lifting the trace into full tables
is_beq and is_bne CPU flags are not linked to the opcode. Due            T ∈ D by populating auxiliary columns such as selector flags, carry
to the lack of those links, a prover can toggle them to manipulate       bits, and padding witnesses. Arguzz mutates 𝐸 itself into a faulty
program counter transitions. IDs 2, 3, and 7 allow premature ter-        executor 𝐸 ′ , so the tables it tests are of the form 𝐺 (𝐸 ′ (𝑃)). ZEBRA
mination. In Valida, CPU constraints accept a matrix of padding          searches directly over D. Because 𝐺 is a deterministic function,
rows, enabling empty executions. In Sphinx, termination is checked       Arguzz’s reachable tables are contained in Im(𝐺 ◦ 𝐸 ′ ) ⊊ D. Any
via next_pc = 0, but this is bypassed for sufficiently short traces.     under-constrained bug whose exploit requires an auxiliary column
IDs 4 and 5 further show soundness issues: branch instructions           to take a value 𝐺 would not produce lies outside this image and is
do not verify the second operand address, enabling substitution of       undetectable by executor-level mutation under any time budget; 𝐺
comparison values, and the Memory table does not enforce that            does not bind a real malicious prover who writes 𝑇 directly.
initial reads return zero, allowing arbitrary initial memory.               Bug ID 1 (Valida) illustrates this. The is_beq and is_bne flags
   IDs 8, 9, 10, and 12 are classified as Design Flaw, reflecting gaps   are set by 𝐺 as pure functions of the opcode, so Arguzz cannot
between VM logic and constraints due to corrupted programs. All of       observe them as independent variables. The constraint system fails
them are due to program counter overflow over a finite field, where      to tie them back to the opcode, so a prover writing 𝑇 directly can
the counter wraps around to zero and falsely signals termination,        set is_beq = 1 on a non-BEQ instruction and hijack control flow.
despite the assumption that only HALT sets next_pc = 0. This             The bug lives exactly in the gap between Im(𝐺 ◦ 𝐸 ′ ) and D, and the
behavior can happen only when the counter can be extremely               executor-mutation fuzzers cannot catch it.
large, and developers noted that these systems assume well-formed
compiler-generated binaries, making such edge cases rare; thus,              Answer to RQ6. ZEBRA outperforms mutation-based fuzzers
these behaviors remain unfixed in favor of performance.                      by operating directly on the table domain D rather than the
   IDs 11 and 13 are classified as Design Choice because the over-           executor-reachable state spaces. While Arguzz found no bugs
constrained behavior is structurally necessary: enforcing next_pc <          even after 6 hours/zkVM, ZEBRA detected 13 under- and over-
𝑝 in the jump table prevents silent field wrap-around, which would           constrained behaviors, including 11 zero-day bugs in 900 sec-
otherwise enable the PC-overflow bugs. We nonetheless label these            onds/zkVM.
as over-constrained rather than intended behavior as the zkVM ex-
ecutors themselves execute such jumps without error, and the rejec-
tion discards traces that are semantically valid executions. However,
                                                                         8     Related Work
this reflects the zkVM designers’ intention to trade completeness        The correctness of zkVM constraint systems has become an active
on these edge cases for prover performance, as supporting targets        area of research as these systems gain adoption in production. Prior
≥ 𝑝 would require an additional range-decomposition machinery.           work falls into three broad categories: dynamic testing, SMT-based
   Note that our findings are not tied to specific hand-crafted pro-     automated verification, and interactive theorem proving.
grams or inputs. Eight findings (IDs 1–3, 7–10, and 12) are reachable    Dynamic Testing. Traditional testing methodologies for zkVMs
from any suitable warm-start program and are independent of its          rely on point-wise sampling to surface logic discrepancies. Pro-
concrete contents. IDs 4–6 require only the presence of a relevant       duction zkVMs such as SP1 employ extensive negative unit tests
instruction family, such as branch or memory operations, rather          that inject random mutations into the proof generation process to
than a particular program or input. IDs 11 and 13 were found during      uncover under-constrained bugs. zkFuzz [28] introduced the first
exhaustive verification rather than warm-started bug finding and         general fuzzing framework for ZK circuits based on code muta-
therefore do not depend on the RQ5 trace corpus.                         tion, and Arguzz [15] extended these ideas to zkVMs by combining
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                       Hideaki Takahashi, Suman Jana, and Junfeng Yang


Table 5: Under- and over-constrained behaviors discovered by ZEBRA. UC = under-constrained; OC = over-constrained. Severity:
Critical: affects arbitrary programs; High: affects specific instruction families with broad consequences; Medium: affects specific
instruction families with limited exploitability; Design Flaw: affects only malformed programs. Design Choice: structurally
required to preserve constraint well-formedness.

 zkVM       ID    Type           Severity           Description                                                                                Status
                                                    Opcode flags such as is_beq / is_bne are not properly linked to the opcode;
             1      UC            Critical                                                                                                      Fixed
                                                    suppressing these flags allows malicious provers to alter control flow.
                                                    The CPU table does not constrain is_real = 1 on the first row;
 Valida      2      UC            Critical                                                                                                      Fixed
                                                    a prover can produce an accepted proof of empty execution for any program.
                                                    The Final instruction is not constrained to be STOP in any verification stage;
             3      UC            Critical                                                                                                      Fixed
                                                    execution may halt arbitrarily for any program with an accepted proof.
                                                    Branch instructions do not verify the second operand when it is an address;
             4      UC              High                                                                                                     In contact
                                                    a prover can substitute an arbitrary address to alter the comparison value.
                                                    The Memory table does not constrain zero-initialized cells to hold zero;
             5      UC              High                                                                                                     Confirmed
                                                    a prover can supply non-zero initial values to any cell.
                                                    Written values lack a range check; distinct byte decompositions evaluate
             6      UC            Medium                                                                                                     In contact
                                                    identically over the finite field, allowing the modification of written values.
                                                    When the execution trace is sufficiently short, program termination is not
             7      UC            Critical                                                                                                   In contact
Sphinx                                              checked, allowing a malicious prover to terminate prematurely.
                                                    only next_pc = 0 is required to show the normal termination; counter overflow
             8      UC         Design Flaw                                                                                                   In contact
                                                    over finite field can satisfy this condition without executing a halt instruction.
                                                    The verifier uses next_pc = 0 as proof of normal termination by a halt syscall;
  Pico       9      UC         Design Flaw                                                                                                   Confirmed
                                                    counter overflow produces the same field value, falsely signaling a clean halt.
                                                    Both next_pc = 0 and exit_code = 0 checks the successful termination,
            10      UC         Design Flaw                                                                                                   In contact
  SP1                                               yet neither condition distinguishes a halt syscall from counter overflow.
                                                    Jump table enforces next_pc < 𝑝 where 𝑝=231 −227 +1; jump targets ≥ 𝑝 are
            11      OC        Design Choice                                                                                                    Known
                                                    unrepresentable in a valid trace, causing the table to reject it.
                                                    The same next_pc = 0 check is applied over KoalaBear (𝑝=231 −224 +1);
            12      UC         Design Flaw                                                                                                   Confirmed
 Ziren                                              counter overflow satisfies the halt condition without a halt syscall.
                                                    Jump table enforces next_pc < 𝑝 where 𝑝=231 −224 +1; jump targets ≥ 𝑝 are
            13      OC        Design Choice                                                                                                    Known
                                                    unrepresentable in a valid trace, causing the table to reject it.


metamorphic testing with fault injection into the virtual machine’s              ZIVER [16] addresses the last point with an inductive consistency-
executor. While effective at uncovering shallow bugs, these dynamic              checking algorithm for SP1 that supports lookups, but requires
approaches provide no theoretical guarantee of completeness and                  manual translation to a custom DSL and covers only 7 small sub-
are structurally unable to reach tables whose helper columns are                 components. Finally, while finite-field–aware SMT theories such as
populated only during witness generation.                                        cvc5 have recently emerged, they still lack support for constraint
                                                                                 patterns common in zkVMs, such as disequality (≠) constraints
SMT-based Verification. Another direction is SMT solvers to                      used in public value checks.
verify ZK constraint systems automatically. Picus [22] combines
structural analysis with SMT-based reasoning to detect under-
constrained bugs in ZK circuits, and has been extended to SP1 [20]
and Ziren [21]. These deployments, while promising, have three                   Interactive Theorem Proving. Interactive theorem provers (ITPs)
structural limits, and they are not directly comparable to our evalu-            offer strong correctness guarantees at the cost of substantial manual
ated Z3 baseline and cannot serve as drop-in experimental baselines              effort. Cairo and Jolt have been formalized in Lean and ACL2 [2, 17].
for ZEBRA: Picus targets determinism, so over-constrained behav-                 OSS tools such as Clean [31] and zkLean [11] pursue the com-
iors are out of scope; published deployments verify only small                   plementary approach of co-designing circuits alongside their cor-
sub-chips, as scaling is blocked by Plonky3’s lack of modular con-               rectness proofs. Despite their strong correctness guarantees, they
straint blocks and I/O annotations [20]; and Picus’s circuit model               require expert-written proofs for every new component or archi-
does not natively handle lookup or permutation constraints [16].                 tectural change, and scale poorly as zkVM designs evolve.
Efficient Branch-and-Bound Testing and Verification of zkVMs                                         CCS ’26, November 15–19, 2026, The Hague, Netherlands


Relation to abstract interpretation. ZEBRA’s interval evalu-              from true under- and over-constrained behaviors, and developed
ator can be viewed as an abstract interpretation of a finite con-         an interval-based branch-and-bound engine for reasoning about
straint system, and its branch-and-bound structure is related to          sets of executions.
interval constraint propagation. Classical abstract interpretation           Across five real-world zkVMs, ZEBRA uncovers 11 previously
typically computes an inductive invariant or fixpoint over a pro-         unknown bugs, including vulnerabilities enabling control-flow hi-
gram’s control-flow semantics. ZEBRA instead analyzes a bounded,          jacking and forged proofs, all missed by a state-of-the-art fuzzer.
already-extracted zkVM constraint instance and uses three-valued          Compared to SMT-based verification, ZEBRA achieves higher cov-
interval evaluation as a sound pruning oracle inside a finite branch-     erage (+16.5 pp) and a 51.5× speedup, while input range verification
and-bound search. Its output is a cardinality classification of canon-    provides up to 63× efficiency gains over point-wise testing.
ical satisfying trace tables, rather than a reachability invariant.          These results suggest that reasoning about solution-set cardinal-
This setting additionally requires sound treatment of finite-field        ity via interval-based branch-and-bound provides a practical and
wrap-around, selector-gated polynomial constraints, lookup and            scalable foundation for zkVM constraint verification.
public-value constraints, and canonicalization of padding, permu-
tation, and auxiliary-witness redundancy. Thus, our contribution
is not interval abstraction itself, but its finite-field specialization   Acknowledgments
and integration with canonicalized cardinality reasoning for zkVM         We sincerely thank the anonymous reviewers for their insight-
constraints.                                                              ful feedback. We would also like to thank Tim Roughgarden and
                                                                          Mahimna Kelkar at The Columbia-Ethereum Research Center for
9    Limitations and Future Work                                          Blockchain Protocol Design for constructive and helpful discussions.
                                                                          Hideaki is supported by Funai Fellowship and Columbia-Ethereum
Global verification. ZEBRA’s correctness guarantees are table-            Center Fellowship. Junfeng is also supported by DARPA ScAN,
localized: given a set of consistent zkVM tables, ZEBRA certifies         NSF CNS 2526620, Google, Samsung, Amazon, and Columbia CAIFI
the target table. Bugs from cross-table interactions, such as lookup      (with Capital One), Enterprise AI (with Infosys), and CDFT centers.
arguments whose two sides are individually satisfied but whose
interface is mis-specified, fall outside this guarantee. No existing
automated technique verifies these cross-table interfaces. A fixed-       References
point iteration over local certificates produced by ZEBRA can for-         [1] Argument Computer. [n. d.]. Sphinx. https://github.com/argumentcomputer/
                                                                               sphinx. Accessed: 2026-04-21.
mally compose toward global correctness, analogous to layerwise            [2] Jeremy Avigad, Lior Goldberg, David Levit, Yoav Seginer, and Alon Titelman. 2022.
bound propagation in neural network verification [26] albeit at                A verified algebraic representation of cairo program execution. In Proceedings
greater computational cost. Reducing this cost via smarter branch-             of the 11th ACM SIGPLAN International Conference on Certified Programs and
                                                                               Proofs. 153–165.
and-bound is a natural direction for future work.                          [3] Aztec Network. 2024. Noir: The Universal Language of Zero-Knowledge. https:
Precision loss from interval abstraction. Interval abstraction                 //noir-lang.org. Accessed: February 23, 2025.
is sound but incomplete: over-approximation may merge feasible             [4] Marta Bellés-Muñoz, Miguel Isabel, Jose Luis Muñoz-Tapia, Albert Rubio, and
                                                                               Jordi Baylina. 2022. Circom: A circuit description language for building
and infeasible assignments and therefore return Uncertain even                 zero-knowledge applications. IEEE Transactions on Dependable and Secure
when the concrete constraint system has a definite answer. This                Computing 20, 6 (2022), 4733–4751.
                                                                           [5] Eli Ben-Sasson, Iddo Bentov, Yinon Horesh, and Michael Riabzev. 2018. Scalable,
imprecision cannot produce a false certificate or a spurious bug               transparent, and post-quantum secure computational integrity. Cryptology
report, because ZEBRA prunes a region only when it is definitely               ePrint Archive (2018).
infeasible and reports an under-constrained bug only after con-            [6] Wyatt Benno, Alberto Centelles, Antoine Douchet, and Khalil Gibran. 2026. Jolt
                                                                               Atlas: Verifiable Inference via Lookup Arguments in Zero Knowledge. arXiv
structing two distinct concrete satisfying traces. However, it may             preprint arXiv:2602.17452 (2026).
force additional splitting and, under a finite time budget, reduce         [7] Brevis Network. [n. d.]. Pico. https://github.com/brevis-network/pico. Accessed:
verification coverage or delay the discovery of a second witness               2026-04-21.
                                                                           [8] OpenVM Contributors. 2025. OpenVM Whitepaper. Whitepaper. OpenVM.
in under-constrained cases. Tighter abstract domains or a hybrid               https://openvm.dev/whitepaper.pdf
interval–SMT procedure could address these residual cases.                 [9] Tim Dokchitser and Alexandr Bulkin. 2023. Zero knowledge virtual machine
                                                                               step by step. Cryptology ePrint Archive (2023).
Verifying Canonicalizer Implementation. While the canonical-              [10] Antonio J Fernández and Patricia M Hill. 2006. An interval constraint branching
izer algorithm is formally verified in Lean 4, verifying the equiv-            scheme for lattice domains. J. Univers. Comput. Sci. 12, 11 (2006), 1466–1499.
alence between the Lean specification and the actual Rust imple-          [11] Galois, Inc. [n. d.]. zkLean. https://github.com/GaloisInc/zkLean. Accessed
                                                                               2026-04-23.
mentation is left for future work.                                        [12] Lior Goldberg, Shahar Papini, and Michael Riabzev. 2021. Cairo–a Turing-
Verifying non-Instruction Table. We exclude the non-instruction                complete STARK-friendly CPU architecture. Cryptology ePrint Archive (2021).
table from exhaustive verification in our current prototype due to        [13] Ulrich Haböck. 2022. Multivariate lookups based on logarithmic derivatives.
                                                                               Cryptology ePrint Archive (2022).
its high complexity; scaling ZEBRA to cover it through advanced           [14] Yahya Hassanzadeh-Nazarabadi and Sanaz Taheri-Boshrooyeh. 2025. Constraint-
heuristics such as opcode-based slicing is an interesting direction            Level Design of zkEVMs: Architectures, Trade-offs, and Evolution. arXiv preprint
for future work.                                                               arXiv:2510.05376 (2025).
                                                                          [15] Christoph Hochrainer, Valentin Wüstholz, and Maria Christakis. 2025. Ar-
                                                                               guzz: Testing zkvms for soundness and completeness bugs. arXiv preprint
                                                                               arXiv:2509.10819 (2025).
10     Conclusion                                                         [16] Jingyu Ke, Boxuan Liang, and Guoqiang Li. 2025. Consistency Verification
We presented ZEBRA, a fully automated framework for testing and                for Zero-Knowledge Virtual Machine on Circuit-Irrelevant Representation.
                                                                               Cryptology ePrint Archive (2025).
verifying zkVM constraint systems. We introduced a formalization          [17] Carl Kwan, Quang Dao, and Justin Thaler. 2024. Verifying jolt zkVM lookup
of zkVM vulnerabilities that separates representational redundancy             semantics. Cryptology ePrint Archive (2024).
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                                      Hideaki Takahashi, Suman Jana, and Junfeng Yang


[18] Ryan Lavin, Xuekai Liu, Hardhik Mohanty, Logan Norman, Giovanni Zaarour, and         Table 6: Constraint density 𝜌 = 𝑇arith (C)/(|C| · 𝑚) measured
     Bhaskar Krishnamachari. 2024. A Survey on the Applications of Zero-Knowledge         across five real-world zkVMs. |C| is the number of AIR con-
     Proofs. arXiv preprint arXiv:2408.00243 (2024).
[19] Lita Foundation. [n. d.]. Valida VM. https://github.com/lita-xyz/valida-vm. Ac-
                                                                                          straints, 𝑚 is the total number of trace cell variables, and 𝑇arith
     cessed: 2026-04-21.                                                                  is the arithmetic gate count after common-subexpression
[20] Shankara Pailoor. 2025. Verifying SP1 circuit determinism with Picus: A              elimination. All values are means across the evaluated tables
     collaboration between Veridise and Succinct. https://veridise.com/blog/audit-
     insights/verifying-sp1-circuit-determinism-with-picus-a-collaboration-               per zkVM. Lower 𝜌¯ indicates sparser constraint graphs.
     between-veridise-and-succinct/. Accessed 2026-04-23.
[21] Shankara Pailoor. 2025. Verifying Ziren’s circuits with Picus: Another step
     towards deterministic zkVMs. https://audithub.dev/blog/picus/verifying-zirens-                 zkVM          #tables          𝑚         |C|       𝑇arith        𝜌¯
     circuits-with-picus-another-step-towards-deterministic-zkvms/. Accessed 2026-
     04-23.                                                                                         Sphinx                8     63.1       76.9        242.0     0.081
[22] Shankara Pailoor, Yanju Chen, Franklyn Wang, Clara Rodríguez, Jacob Van Geffen,                Pico                  9     59.3       79.1        237.3     0.086
     Jason Morton, Michael Chu, Brian Gu, Yu Feng, and Işıl Dillig. 2023. Automated
     detection of under-constrained circuits in zero-knowledge proofs. Proceedings                  Ziren                13     41.8       51.7        171.5     0.107
     of the ACM on Programming Languages 7, PLDI (2023), 1510–1532.                                 Valida                9     36.2       33.8        139.2     0.187
[23] ProjectZKM. [n. d.]. Ziren. https://github.com/ProjectZKM/Ziren. Accessed:
     2026-04-21.
                                                                                                    SP1                  11     42.1       55.7        501.4     0.227
[24] RISC Zero. 2025. Security Disclosure: A missing constraint was recently discov-                Overall             50      47.4       58.3        261.4    0.140
     ered in the rv32im circuit. https://x.com/RiscZero/status/1935404812146725042.
     RISC-V instructions in risc0-zkvm versions 2.0.0–2.0.2 were affected; patch re-
     leased in version 2.1.0.
[25] Javier Ron and Martin Monperrus. 2026. Verifiable Provenance of Software
     Artifacts with Zero-Knowledge Compilation. arXiv preprint arXiv:2602.11887           B Design Details
     (2026).
[26] Zhouxing Shi, Qirui Jin, J. Zico Kolter, Suman Jana, Cho-Jui Hsieh, and Huan         B.1 Sound Over-Approximation of Constraints
     Zhang. 2025. Neural Network Verification with Branch-and-Bound for General           This section provides the rigorous formalization of the interval-
     Nonlinearities. In Tools and Algorithms for the Construction and Analysis of
     Systems (TACAS). Springer.                                                           based sound over-approximations used by ZEBRA. We transition
[27] Succinct Labs. 2026. SP1. https://github.com/succinctlabs/sp1. Accessed: 2026-       from concrete constraints over the finite field F𝑝 to an abstract inter-
     04-21.
[28] Hideaki Takahashi, Jihwan Kim, Suman Jana, and Junfeng Yang. 2025. zkFuzz:
                                                                                          val domain I, ensuring that the conditions defined in Definition 5.1
     Foundation and Framework for Effective Fuzzing of Zero-Knowledge Circuits.           are strictly maintained for all lookup categories.
     arXiv preprint arXiv:2504.11961 (2025).
[29] Morgan Thomas, Mamy Ratsimbazafy, Marcin Bugaj, Lewis Revill, Carlo Modica,
     Sebastian Schmidt, Ventali Tan, Daniel Lubarov, Max Gillett, and Wei Dai. 2025.      B.2     Preliminaries and Interval Arithmetic
     Valida ISA Spec, version 1.0: A zk-Optimized Instruction Set Architecture. arXiv     We first provide several additional notations related to intervals.
     preprint arXiv:2505.08114 (2025).
[30] Valida. [n. d.]. Valida (Old Version). https://github.com/valida-xyz/valida. Ac-        1) Interval Membership: For an integer 𝑎 ∈ Z and an interval
     cessed: 2026-04-21.                                                                  [𝐿, 𝑅] ∈ I, we denote 𝑎 ∈ [𝐿, 𝑅] if 𝐿 ≤ 𝑎 ≤ 𝑅, and 𝑎 = [𝐿, 𝑅] if
[31] Verified-zkEVM. [n. d.]. Clean: A verified zkEVM. https://github.com/Verified-
     zkEVM/clean/. Accessed 2026-04-23.
                                                                                          𝑎 = 𝐿 = 𝑅.
[32] Lizheng Wang, Hancheng Lou, Chongrong Li, Yu Yu, and Yuncong Hu. 2026.                  2) Interval Arithmetic: The basic arithmetic operations, add,
     zkAgent: Verifiable Agent Execution via One-Shot Complete LLM Inference Proof.       sub, and mul, are defined as:
     Cryptology ePrint Archive (2026).
[33] Hongbo Wen, Jon Stephens, Yanju Chen, Kostas Ferles, Shankara Pailoor, Kyle                [𝑎, 𝑏] + [𝑐, 𝑑] = [𝑎 + 𝑐, 𝑏 + 𝑑]
     Charbonnet, Isil Dillig, and Yu Feng. 2024. Practical Security Analysis of { Zero-
     Knowledge } Proof Circuits. In 33rd USENIX Security Symposium (USENIX                      [𝑎, 𝑏] − [𝑐, 𝑑] = [𝑎 − 𝑑, 𝑏 − 𝑐]
     Security 24). 1471–1487.
                                                                                                 [𝑎, 𝑏] · [𝑐, 𝑑] = [min(𝑎𝑐, 𝑎𝑑, 𝑏𝑐, 𝑏𝑑), max(𝑎𝑐, 𝑎𝑑, 𝑏𝑐, 𝑏𝑑)]
11     Ethical Considerations                                                                3) Row Membership: We view a table as a set of rows. For
We responsibly disclosed all previously unknown vulnerabilities                           instance, when a row vector 𝑣® ∈ F𝑊 appears as a row of a table
                                                                                          𝑇 ∈ F𝐻  ×𝑊 , we write 𝑣® ∈ 𝑇 .
discovered in public projects. We first contacted the maintainers                               𝑝
privately and created public GitHub issues only with their approval.                         4) Interval Area: Let |[𝐿, 𝑅]| = 𝑅 − 𝐿 + 1, meaning the area of
We also worked closely with each team to assess the severity of the                       the interval [𝐿, 𝑅]. For a vector of intervals 𝐼® = (𝐼 1, 𝐼 2, . . . , 𝐼 𝑤 ), we
issues and support the development of appropriate fixes.                                  define |𝐼®| = 𝑤𝑗=1 |𝐼 𝑗 |.
                                                                                                        Î
                                                                                             5) Column Projection We define a column projection 𝔣𝑖 as
A     Overview of zkVMs                                                                   a functional that extracts a value from the table based on row 𝑖.
                                                                                          Formally, 𝔣𝑖 (𝑇 ) returns a linear combination of cells in the 𝑖-th row:
   Sparsity in zkVMs. Across 50 tables from five production zkVMs
(Table 6), we observe 𝜌 ranging from 0.017 (Sphinx CPU) to 0.809                                                                   𝑊
                                                                                                                                   ∑︁−1
(SP1 Branch), with an overall mean of 𝜌¯ = 0.140 — the typical                                                         𝔣𝑖 (𝑇 ) =          𝛼 𝑗 · 𝑇𝑖,𝑗                      (11)
constraint uses only 14% of its theoretical connectivity. Three of                                                                  𝑗=0

the five zkVMs (Sphinx, Pico, Ziren) are consistently sparse with                         , where 𝛼 𝑗 ∈ F𝑝 is a fixed coefficient specific to each 𝔣. In the interval
𝜌¯ ≤ 0.11; SP1 and Valida contain a small number of dense tables                          domain, 𝔣𝑖 (𝑇e) is similarly computed using interval arithmetic.
(notably SP1 Branch and Valida Mul32) that raise their per-zkVM
                                                                                             6) Vector Projections: We define a vector projection ®𝔣𝑖 as a
averages, but remain below 𝜌¯ = 0.23 overall.
                                                                                          tuple of 𝑘 column projections:
   Example Arithmetization. Fig. 6 shows the example arithmetiza-
tion of a zkVM.                                                                                          ®𝔣𝑖 (𝑇 ) = 𝔣𝑖,1 (𝑇 ), 𝔣𝑖,2 (𝑇 ), . . . , 𝔣𝑖,𝑘 (𝑇 )  ∈ F𝑘        (12)
                                                                                                                                                                 𝑝
Efficient Branch-and-Bound Testing and Verification of zkVMs                                                                                  CCS ’26, November 15–19, 2026, The Hague, Netherlands



                            Lookup: Program ⇔ CPU                                                                                                                   AIR of ADD
              (pc,opcode,dst,src1,src2) from     must show in                                                                                               curr.c = curr.a + curr.b



                                                                                                                                                                          a b    c
                                                                                                                                                                          Assets
                                                                                                        clk pc op    dst src1 src2 val1 val2 res                        3   1    4
      pc op            dst src1 src2
                                                                                                         0     0 STR -4     3     0     0    0     3
                                                               AIR of CPU                                                  Assets
       0 STR -4    3                        0                                                                                                                     Lookup: CPU ⇔ Add
            Assets                                   ・next.clk = curr.clk + 1                            1     4 STR -8     1     0     0    0     1
                                                                                                                                                           if opcode is ADD, (val1, val2,
       4 STR -8    1                        0        ・next.pc = curr.pc + 4                              2     8 ADD -12    -4   -8     3    1     4       res) from       must exist in  .
       8 ADD -12                  -4        -8       ・If op is STR, src1 = res



Figure 6: Conceptual arithmetization of a zkVM execution. The Program Table (𝑇prog ) is an instance table defining the compiled
instructions. The CPU Table (𝑇CPU ) records the cycle-by-cycle execution state, and its AIR enforces the main CPU logic, such as
valid transitions of pc and clk. The ADD Table (𝑇Add ) validates the correctness of the addition operation. Global consistency is
enforced by lookup constraints, ensuring all entries in 𝑇CPU match auxiliary tables.

 clk pc op   dst src1 src2 val1 val2 res is_pad
                                                                                                                    𝑇prog . Let 𝑝𝑟𝑜𝑔
                                                                                                                                  ® 𝑖 be the vector projection of the columns correspond-
                                                                      Canonicalized Representation
 0   0 STR -4     3   0
                    Assets
                           0       0    3        0
                                                     Replay             (Set of Execution Records)                  ing to the program counter, opcode, and operands.
 1   4 STR -8     1   0    0       0    1        0
 2   8 ADD -12    -4     -8   3    1    4        1                     At clk=0, run (STR, -4, 3) at pc=0,                     L                                −−−→ (𝑇 ) ∈ 𝑇
                                                                                                                                     (𝑇 ) := ∀𝑖. 𝔰 (𝑇 ) = 1 =⇒ 𝔭𝔯𝔬𝔤                  (13)
                                                                                                                                 prog                  𝑖                      𝑖        prog
                                                                              storing 3 at addr=-4
 clk pc op   dst src1 src2 val1 val2 res is_pad
                                                                       At clk=1, run (STR, -8, 1) at pc=4,              The sound over-approximation L     prog returns True if any active
 0   0 STR -4     3      0    0    0    3        0   Replay
 1   4 STR -8     1 Assets
                      0    0       0    1        0
                                                                                storing 1 at addr=-8                 row’s program-related columns collapse into a singleton vector
                                                                      At clk=2, run (ADD, -12, -4, -8) at
 2   8 ADD -12    -4    -8    3    1    4        0                   pc=8, loading 3 from addr=-4 and 1 from         that is present in 𝑇prog , and returns False if the interval vector of
 0   0 NOP   0    0      0    0    0    0        1     Padding           addr=-8, storing 4 at addr=-12              program-related columns is entirely disjoint from any row in 𝑇prog .
                                                     Conditionally
 clk pc op   dst src1 src2 val1 val2 res is_pad       Free Var                                                       In other cases, L
                                                                                                                                      prog returns Uncertain.
 0   0 STR -4     3      0    0   123   3        0
                       Assets                                               All tables correspond to
                                                         Replay
 1   4 STR -8     1      0    0    0    1        0                         the same execution trace.
 2   8 ADD -12    -4     -8   3    1    4        0                                                                                       
                                                                                                                                          True             if ∀𝑖. 1 ∈ 𝔰𝑖 (𝑇e) =⇒
                                                                                                                                                                 −−−→ (𝑇e)| = 1∧
                                                                                                                                         
                                                                                                                                         
                                                                                                                                         
                                                                                                                                         
                                                                                                                                                               |𝔭𝔯𝔬𝔤   𝑖
                                                                                                                                                                −− −→ (𝑇e) ∈ 𝑇
                                                                                                                                         
Figure 7: To resolve representational redundancies in trace                                                                              
                                                                                                                                                                𝔭𝔯𝔬𝔤            prog
                                                                                                                                         
                                                                                                                           Lprog (𝑇 ) :=                                                       (14)
                                                                                                                                         
                                                                                                                                                                     𝑖
tables like null-row padding and conditionally free variables,                                                             e      e
                                                                                                                                         
                                                                                                                                          False            if ∃𝑖. [1, 1] = 𝔰𝑖 (𝑇e) and
a canonicalizer (R) maps trace tables to a unique set of se-                                                                             
                                                                                                                                                                 −−−→ (𝑇e)K ∩ 𝑇
                                                                                                                                                                J𝔭𝔯𝔬𝔤               prog = ∅
                                                                                                                                         
                                                                                                                                         
mantic execution records, ensuring a one-to-one mapping.                                                                                 
                                                                                                                                                                        𝑖   𝑝
                                                                                                                                                            otherwise
                                                                                                                                         
                                                                                                                                          Uncertain
                                                                                                                                         
                                                                                                                       L-2) Byte Lookup. : The Byte lookups enforce precomputed rela-
                                                                                                                    tions over a restricted range [𝐿, 𝑅], typically [0, 255]. Let 𝔞𝑖 , 𝔟𝑖 , 𝔠𝑖
In the interval domain, ®𝔣𝑖 (𝑇e) = 𝐼𝑖,1, 𝐼𝑖,2, . . . , 𝐼𝑖,𝑘 ∈ I𝑘 is the Carte-                                      be the projections for the output and operands of a byte operation
                                                           
sian product of the resulting intervals.                                                                            ★. Then the semantic meaning of the Byte Lookup constraints can
    7) Interval Disjointness Two intervals 𝐼, 𝐽 are disjoint (𝐼 ∩𝐽 = ∅)                                             be written as:
if [[𝐼 ]] 𝑝 ∩ [[𝐽 ]] 𝑝 = ∅. An interval vector 𝐼® ∈ F𝑊    𝑝 is disjoint from a
table 𝑇 ⊆ F𝑝  𝐻 ×𝑊   , written as [[𝐼 ]] 𝑝 ∩ 𝑇 = ∅, if no vector 𝑣 ∈ [[𝐼®]] 𝑝
                                    ®                                                                                            Lbyte (𝑇 ) := ∀𝑖. 𝔰𝑖 (𝑇 ) = 1 =⇒                              (15)
exists in 𝑇 .                                                                                                                               𝐿 ≤ 𝔟𝑖 (𝑇 ) ≤ 𝑅 ∧ 𝐿 ≤ 𝔠𝑖 (𝑇 ) ≤ 𝑅 ∧                (16)
    8) Vector Embedding For a vector of intervals 𝐼® = (𝐼 1, . . . , 𝐼𝑘 ),
                                                                                                                                            𝔞𝑖 (𝑇 ) = 𝔟𝑖 (𝑇 ) ★ 𝔠𝑖 (𝑇 )                        (17)
we also define a vector embedding [[𝐼®]] 𝑝 = [[𝐼 1 ]] 𝑝 ×· · ·× [[𝐼𝑘 ]] 𝑝 ⊆
F𝑘𝑝 .                                                                                                               The Range-check operation is treated as a special case where Eq. 17
                                                                                                                    is omitted, effectively enforcing only the range constraint.
                                                                                                                        The sound over-approximation L    byte semantically lifts each byte
B.3          Sound Over-Approximation of Lookup                                                                     operation ★ into an over-approximated operator ★˜ over intervals
             Constraints                                                                                            that uses bit-masking to track fixed and varying bits to derive tight
We denote 𝔰𝑖 (𝑇˜ ) as the interval projection of the selector for the                                               bounds (see Tab. 7). L  byte returns True if the operand intervals fit
𝑖-th row. A row is considered "active" if 1 ∈ 𝔰𝑖 (𝑇˜ ).                                                             entirely within the permitted byte range and the output interval
                                                                                                                    matches the result of the lifted operation as a singleton. Conversely,
   L-1) Program Lookup. : The Program Lookup Lprog ensures that                                                     it returns False if any operand is disjoint from the required range or
the executed instruction is consistent with the static program binary                                               if the claimed result interval is disjoint from the possible outcomes
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                             Hideaki Takahashi, Suman Jana, and Junfeng Yang


                                                         ˜ In other
of the interval-based approximation of bitwise operation ★.
cases, it just returns Uncertain.
                                                                                     L
                                                                                     ecf (𝑇e)                                                                  (23)
                                                                                          True          if ∀𝑖. 1 ∈ 𝔰𝑖 (𝑇e) =⇒
                                 if ∀𝑖. 1 ∈ 𝔰𝑖 (𝑇e) =⇒
                                                                                         
                True                                                                    
                                                                                                            |𝔭𝔠 ′𝑖 (𝑇e)| = 1∧
               
                                                                                        
                                                                                         
                                                                                        
                                                                                         
                                   𝔟𝑖 ⊆ [𝐿, 𝑅] ∧ 𝔠𝑖 ⊆ [𝐿, 𝑅]∧
               
                                                                                        
                                                                                                            𝔭𝔠 ′𝑖 (𝑇e) = cf(𝔭𝔠
                                                                                         
               
                                                                                                                        e 𝑖 (𝑇e), 𝔞𝑖 (𝑇e), 𝔟𝑖 (𝑇e), 𝔠𝑖 (𝑇e))
                                                                                      :=
                                                                                         
                                                                                         
                                   |𝔞𝑖 (𝑇e)| = 1 ∧ 𝔞𝑖 (𝑇e) = 𝔟𝑖 (𝑇e) ★
               
                                                                    e 𝔠𝑖 (𝑇e)
                                                                                                         if ∃𝑖. [1, 1] = 𝔰𝑖 (𝑇e) ∧
               
                                                                                           False
               
  Lbyte (𝑇 ) := False
               
                                                                                        
                                 if ∃𝑖. [1, 1] = 𝔰𝑖 (𝑇 ) ∧
  e                                                                                      
                                                                                         
                                                                                                            𝔭𝔠 ′𝑖 (𝑇e) ∩ cf(𝔭𝔠
                                                      e                                  
               
                                  𝔟𝑖 ⊈ [𝐿, 𝑅] ∨ 𝔠𝑖 ⊈ [𝐿, 𝑅] ∨
                                                                                         
                                                                                         
                                                                                                                         e 𝑖 (𝑇e), 𝔞𝑖 (𝑇e), 𝔟𝑖 (𝑇e), 𝔠𝑖 (𝑇e)) = ∅
                                                                                        
                                                                                                         otherwise
               
                                                                                        
                                                                                          Uncertain
               
               
                                   𝔞𝑖 (𝑇e) ∩ (𝔟𝑖 (𝑇e) ★
                                                       e 𝔠𝑖 (𝑇e)) = ∅                    
                                                                                                                                                                (24)
               
               
                Uncertain       otherwise
               
               
                                                                             (18)
                                                                                       Table 9 lists the cf
                                                                                                         e approximation for each implemented control-
                                                                                    flow opcode. In all branch instructions, 𝔞 and 𝔟 are the two operands
                                                                                    compared by the branch condition, 𝔠 is the signed branch offset
   L-3) ALU Lookup. : For lookups involving the Arithmetic Logic
                                                                                    (relative to the current PC), and 𝛿 is the default sequential step size
Unit (ALU), we reduce the constraints to semantically equivalent
                                                                                    (e.g., 4 for RISC-V). The condition evaluation reuses the interval
algebraic equations over integer intervals. Specifically, let 𝔞𝑖 , 𝔟𝑖 ,
and 𝔠𝑖 be the column projections corresponding to the output, the                   predicates Eq,
                                                                                                 f SLt,
                                                                                                    g SLe,g and Lt e from Table 8.
first input operand, and the second input operand, respectively.                        L-5) Memory Lookup. : The Memory Lookup constraint Lmem
The concrete constraint semantically ensures that the output is the                 ensures global Read-After-Write (RAW) consistency. For each row
result of the VM-level operation ⋄ ∈ {+, −, ×, ÷, . . . } applied to the            𝑖, let 𝔞𝔡𝔡𝔯𝑖 (𝑇˜ ), 𝔳𝔞𝔩𝑖 (𝑇˜ ), and 𝔱𝔶𝔭𝔢𝑖 (𝑇˜ ) be the column projections for
inputs:                                                                             the address, value, and access type, respectively.
                                                                                        ZEBRA maintains an Abstract Segmented Memory state M̂,
                                                                                    which is updated or queried chronologically. The abstract evaluator
      Lalu (𝑇 ) := ∀𝑖. 𝔰𝑖 (𝑇 ) = 1 =⇒ 𝔞𝑖 (𝑇 ) = 𝔟𝑖 (𝑇 ), ⋄, 𝔠𝑖 (𝑇 )         (19)     emem is defined by the aggregate result of a consistency check
                                                                                    L
                                                                                    performed on each operation:
   The sound approximation L ealu (𝑇e) leverages a library of sound
interval approximations e⋄ for each ALU operation (see Tab. 8).
These transformers map the input interval to the smallest possible                    emem (𝑇˜ ) =
                                                                                      L                                                                        (25)
interval bound. The approximation is formally defined as:                             
                                                                                      
                                                                                       True          if ∀𝑖, 1 ∈ 𝔰𝑖 (𝑇˜ ) =⇒
                                                                                                      IsRAM(𝔞𝔡𝔡𝔯𝑖 (𝑇˜ ), 𝔳𝔞𝔩𝑖 (𝑇˜ ), 𝔱𝔶𝔭𝔢𝑖 (𝑇˜ ), M̂) = True
                                                                                      
                                                                                      
                                                                                      
                                                                                      
                                                                                      
                                if ∀𝑖. 1 ∈ 𝔰𝑖 (𝑇e) =⇒                                                 if ∃𝑖, [1, 1] = 𝔰𝑖 (𝑇˜ )∧
                                                                                      
                                                                                      
             
             
              True                                                                     False
                                                                                                      IsRAM(𝔞𝔡𝔡𝔯𝑖 (𝑇˜ ), 𝔳𝔞𝔩𝑖 (𝑇˜ ), 𝔱𝔶𝔭𝔢𝑖 (𝑇˜ ), M̂) = False
             
                                    |𝔞𝑖 (𝑇e)| = 1 ∧ 𝔞𝑖 (𝑇e) = 𝔟𝑖 (𝑇e) e
                                                                                      
                                                                      ⋄ 𝔠𝑖 (𝑇e)
             
                                                                                     
             
                                                                                     
                                                                                      
                                                                                      
 ealu (𝑇e) := False
             
             
 L                              if ∃𝑖. [1, 1] = 𝔰𝑖 (𝑇 ) and                                           otherwise
                                                                                      
                                                      e                                Uncertain
                                                                                      
                                                                                      
                                                                                                                                                            (26)
             
                                    𝔞𝑖 (𝑇e) ∩ (𝔟𝑖 (𝑇e) e
                                                       ⋄ 𝔠𝑖 (𝑇e)) = ∅
             
             
             
             
             
              Uncertain
             
                                                                                       ZEBRA initializes M̂ with a single segment ([0, 2𝑊 − 1], [0, 0])
             
                                                                   (20)
In the False case, the evaluator identifies that the interval of the                representing zero-initialization of the entire address space, so every
claimed result 𝔞𝑖 (𝑇e) is disjoint from the range of possible outcomes              address has a defined stored value throughout the execution.
produced by the operands under the operation e      ⋄.                                 The internal logic of IsRAM(b   𝑎, b 𝑡 , M̂) handles the stateful na-
                                                                                                                          𝑣,b
                                                                                    ture of memory. For the write case, IsRAM updates M̂ by splitting
   L-4) Control Flow Lookup. : Let 𝔭𝔠𝑖 and 𝔭𝔠 ′𝑖 be column projections              any segments that intersect with 𝑎b and inserting the new value b     𝑣.
on the 𝑖-th row. The semantic meaning of the Control Flow Lookup                    Since any write is locally valid, this operation always returns True.
is expressed via the opcode-specific function cf, which computes                    For the read case, the evaluator verifies b   𝑣 against the segments in
the next program counter from the current PC and operands:                          M̂ that intersect with 𝑎b:
                                                                                          • Returns True if b
                                                                                                            𝑣 contains the stored value interval of every
                                                                                            intersecting segment.
           Lcf (𝑇 ) := ∀𝑖. 𝔰𝑖 (𝑇 ) = 1 =⇒                                   (21)          • Returns False if b
                                                                                                             𝑣 is disjoint from the stored value of some
                   𝔭𝔠 ′𝑖 (𝑇 ) = cf(𝔭𝔠𝑖 (𝑇 ), 𝔞𝑖 (𝑇 ), 𝔟𝑖 (𝑇 ), 𝔠𝑖 (𝑇 ))     (22)            intersecting segment.
                                                                                          • Returns Uncertain otherwise.
   We naturally derive the sound interval approximation cf        e based
on e⋄, and the sound over-approximation L     g cf returns  True when pc′           B.4     Proof of Theorem 5.2
is a singleton such that pc′ = cf   f◦ (pc, 𝑎, 𝑏, 𝑐), False when pc′ and               Proof Sketch. The proof proceeds by establishing three prop-
cf
f◦ (pc, 𝑎, 𝑏, 𝑐) are entirely disjoint, and Uncertain in other cases.               erties: termination, soundness, and completeness.
Efficient Branch-and-Bound Testing and Verification of zkVMs                                               CCS ’26, November 15–19, 2026, The Hague, Netherlands


Table 7: Sound Over-Approximated Constraints for Byte Lookup Tables. Here 𝑎𝑙𝑜 , 𝑎ℎ𝑖 (resp. 𝑏𝑙𝑜 , 𝑏ℎ𝑖 ) are the lower and upper
bounds of the first (resp. second) byte operand interval; 𝑣 = (𝑎𝑙𝑜 ⊕ 𝑎ℎ𝑖 ) | (𝑏𝑙𝑜 ⊕ 𝑏ℎ𝑖 ) is the varying-bit mask; all values are in
[0, 255].

      Opcode                              ˜
                  Interval Approximation (★)                                       Soundness Notes
                                                                                   Bits forced to 0 in either operand cannot appear in result;
      BitAnd       [(𝑎𝑙𝑜 & 𝑏𝑙𝑜 ) & ¬𝑣, min(𝑎ℎ𝑖 , 𝑏ℎ𝑖 )]                            upper bound uses min(𝑎ℎ𝑖 , 𝑏ℎ𝑖 ) since AND cannot exceed
                                                                                   either input.
                                                                                   Lower bound: bits set in both 𝑎𝑙𝑜 and 𝑏𝑙𝑜 are definitely set;
      BitOr        [(𝑎𝑙𝑜 | 𝑏𝑙𝑜 ), (𝑎ℎ𝑖 | 𝑏ℎ𝑖 ) | 𝑣]                                upper bound: all bits present in either operand’s high end,
                                                                                   extended by varying bits.
                                                                                   Fixed bits (those not in 𝑣) produce a known XOR result;
      BitXor       [(𝑎𝑙𝑜 ⊕ 𝑏𝑙𝑜 ) & ¬𝑣, (𝑎𝑙𝑜 ⊕ 𝑏𝑙𝑜 ) | 𝑣]
                                                                                   varying bits are treated conservatively as either 0 or 1.
                                                                                   Exact when intervals are non-overlapping; uncertain
      Lt           [1, 1] if 𝑎ℎ𝑖 < 𝑏𝑙𝑜 ;   [0, 0] if 𝑎𝑙𝑜 ≥ 𝑏ℎ𝑖 ;   else [0, 1]
                                                                                   when the comparison outcome depends on the concrete values.
                                                                                   Evaluates bit 7 (sign bit) of an 8-bit byte;
      MSB          [1, 1] if 𝑎𝑙𝑜 ≥ 128;     [0, 0] if 𝑎ℎ𝑖 < 128;     else [0, 1]
                                                                                   exact when the interval lies entirely above or below 128.


   Termination. The search space is a finite integer lattice I𝐻 ×𝑊                   Core Definitions. We define a Config to encapsulate the domain-
defined over the range [0, 𝑝 −1]. In each iteration of the branch-and-               specific logic for identifying valid state transitions and projecting
bound search, SplitInterval partitions a "divisible" cell (𝑎 ≠ 𝑏) into               them into a normalized form. The canonicalizer R maps a trace to
strictly smaller sub-intervals. Because the volume of the intervals                  a unique set of semantic execution records.
decreases monotonically and the search space is discrete and finite,
                                                                                       structure Config (Repr : Type) where
the algorithm must terminate.
                                                                                         isReal : Row →Bool
    Local Soundness. By its definition, local soundness requires that                    projectRow : Row →Repr
every reported trace satisfies the constraints. In Algorithm 1, a trace
𝑇 is added to 𝑄 only if 𝐶˜ (𝑇˜ ) = True. According to the Soundness                    def canonicalize
Condition (Definition 5.1), if 𝐶˜ (𝑇˜ ) = True, then for all 𝑇 ∈ [[𝑇˜ ]] 𝑝 ,               (cfg : Config Repr) (t : Trace) : Finset Repr :=
                                                                                         ((t.filter cfg.isReal).map cfg.projectRow).toFinset
it is guaranteed that 𝐶 (𝑇 ) = True. Thus, every element in 𝑄 is a
mathematically valid execution trace.                                                The tuple type Repr is per-table, for example, the ALU tuple (the
                                                                                     first input, the second input, the output) for arithmetic instructions,
   Local Completeness. Local Completeness requires that no valid                     or a control-flow tuple capturing program-counter transitions for
trace is omitted. This is guaranteed by two mechanisms.                              branches and jumps.
   First, the SplitInterval function maintains a total cover of the                      Independent of the canonicalizer, we model the zkVM’s notion of
search space, ensuring the union of child nodes equals the parent                    a semantic record for each table. Record is the zkVM-level abstract
node.                                                                                semantics of an opcode execution, and the structure RecordIdentity
   Second, A branch is only discarded if 𝐶˜ (𝑇˜ ) = False. By Defi-                    Record Identity carries an injection toIdentity that assigns a
nition 5.1, if 𝐶˜ (𝑇˜ ) = False, then no 𝑇 ∈ [[𝑇˜ ]] 𝑝 exists such that              unique identity to each record, witnessing that the zkVM’s record
𝐶 (𝑇 ) = True. Therefore, pruning never discards a satisfying solu-                  type is fine-grained enough to distinguish every distinct execution
tion.                                                                                of the opcode.
   Finally, the canonicalizer R ensures that representational re-
dundancies (such as padding or permutations) are mapped into a                         structure RecordIdentity (Record Identity : Type) where
unique semantic normal form. This ensures that the cardinality                           toIdentity : Record →Identity
of 𝑄 accurately reflects the number of semantically distinct solu-                       injective : Function.Injective toIdentity
tions, identifying under-constrained (|𝑄 | > 1) or over-constrained
(|𝑄 | = 0) behaviors.                                                □
                                                                                     Faithful Table Generation Assumption. The single per-zkVM
                                                                                     modeling assumption is that the table generator is faithful: its non-
C Implementation Details                                                             padding projected rows reproduce exactly the records of the under-
C.1 Canonicalization                                                                 lying execution, independently of row order, padding placement,
                                                                                     or helper-column values.
To ensure that our solution-set cardinality criterion (|𝑄 |) accurately
distinguishes semantic bugs from representational artifacts, we                        def TableEncodesRecords
formalize our canonicalizer in Lean 4. This lets us prove that the                         (cfg : Config Identity) (recordId : RecordIdentity
canonicalizer is invariant under representational artifacts of the                              Record Identity)
table generator and one-to-one on semantically distinct executions.                        (records : RecordSet Record) (table : Trace) : Prop :=
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                              Hideaki Takahashi, Suman Jana, and Junfeng Yang


Table 8: Sound Over-Approximated Constraints for ALU Lookup Tables. 𝑊 = 232 ; 𝑎𝑙𝑜 , 𝑎ℎ𝑖 and 𝑏𝑙𝑜 , 𝑏ℎ𝑖 are the lower and upper
bounds of the two 32-bit input operand intervals. Signed operations first reinterpret the unsigned interval as a two ’s-complement
signed interval via the mapping 𝑥 ↦→ 𝑥 − 𝑊 for 𝑥 ≥ 231 . “Full word” denotes [0,𝑊 − 1].

    Opcode                                         ˜
                           Interval Approximation (⋄)                                      Soundness Notes
                           [𝑎𝑙𝑜 +𝑏𝑙𝑜 , 𝑎ℎ𝑖 +𝑏ℎ𝑖 ] if no overflow;
                                                                                           Exact for singletons (mod 𝑊 ); overflow is certain when
    AddU                   [𝑎𝑙𝑜 +𝑏𝑙𝑜 −𝑊 , 𝑎ℎ𝑖 +𝑏ℎ𝑖 −𝑊 ] if overflow certain;
                                                                                           𝑎𝑙𝑜 + 𝑏𝑙𝑜 ≥ 𝑊 , impossible when 𝑎ℎ𝑖 + 𝑏ℎ𝑖 < 𝑊 .
                           full word otherwise
                           [𝑎𝑙𝑜 −𝑏ℎ𝑖 , 𝑎ℎ𝑖 −𝑏𝑙𝑜 ] if no underflow;
                                                                                           Exact for singletons (mod 𝑊 ); underflow is certain when
    SubU                   [𝑎𝑙𝑜 +𝑊 −𝑏ℎ𝑖 , 𝑎ℎ𝑖 +𝑊 −𝑏𝑙𝑜 ] if underflow certain;
                                                                                           𝑎ℎ𝑖 < 𝑏𝑙𝑜 , impossible when 𝑎𝑙𝑜 ≥ 𝑏ℎ𝑖 .
                           full word otherwise
                                                                                           Exact for singletons (mod 𝑊 ); returns full word when
    Mul                    [𝑎𝑙𝑜 × 𝑏𝑙𝑜 , 𝑎ℎ𝑖 × 𝑏ℎ𝑖 ] mod 𝑊
                                                                                           𝑎ℎ𝑖 × 𝑏ℎ𝑖 ≥ 𝑊 and operands are not singletons.
                                                                                           Signed high-word: C = {𝑎𝑙𝑜 𝑏𝑙𝑜 , 𝑎𝑙𝑜 𝑏ℎ𝑖 , 𝑎ℎ𝑖 𝑏𝑙𝑜 , 𝑎ℎ𝑖 𝑏ℎ𝑖 }
    MulH / MulHS           [min(C) ≫ 32, max(C) ≫ 32] mod 𝑊                                over signed 32-bit interpretation; arithmetic right-shift
                                                                                           by 32.
                                                                                           Unsigned high-word: logical right-shift of 64-bit
    MulHU                  [⌊𝑎𝑙𝑜 × 𝑏𝑙𝑜 /𝑊 ⌋, ⌊𝑎ℎ𝑖 × 𝑏ℎ𝑖 /𝑊 ⌋]                              product by 32; monotone in both operands so
                                                                                           endpoint products bound the result.
                                                                                           Signed full 64-bit product split into lower (TL) and
                           lo(𝑃) ∈ [min(C) & (𝑊 −1), max(C) & (𝑊 −1)]
    MulTL / MulTH                                                                          upper (TH) 32-bit halves;
                           hi(𝑃) ∈ [min(C) ≫ 32, max(C) ≫ 32]
                                                                                           C over signed interpretation of both intervals.
                                                                                           Unsigned full 64-bit product split into lower (TUL) and
                           lo(𝑃) ∈ [𝑎𝑙𝑜 𝑏𝑙𝑜 & (𝑊 −1), 𝑎ℎ𝑖 𝑏ℎ𝑖 & (𝑊 −1)]
    MulTUL / MulTUH                                                                        upper (TUH) 32-bit halves; monotone so endpoint
                           hi(𝑃) ∈ [𝑎𝑙𝑜 𝑏𝑙𝑜 ≫ 32, 𝑎ℎ𝑖 𝑏ℎ𝑖 ≫ 32]
                                                                                           products suffice.
                                                                                           Exact for singletons; lower bound is 0 (AND can clear
    And                    [0, min(𝑎ℎ𝑖 , 𝑏ℎ𝑖 )]                                            all bits); upper bound min(𝑎ℎ𝑖 , 𝑏ℎ𝑖 ) since AND cannot
                                                                                           exceed either input.
                                                                                           Exact for singletons; lower bound: bits set in the larger
                           [𝑎𝑙𝑜 |𝑏𝑙𝑜 , 𝑎ℎ𝑖 |𝑏ℎ𝑖 ]       if 𝑎 and 𝑏 are singletons
    Or                                                                                     operand are preserved; upper bound:
                           [max(𝑎𝑙𝑜 , 𝑏𝑙𝑜 ), 2 ⌈log2 ( (𝑎ℎ𝑖 |𝑏ℎ𝑖 )+1) ⌉ − 1] else
                                                                                           next power-of-two minus 1 covering 𝑎ℎ𝑖 |𝑏ℎ𝑖 .
                                                                                           Exact for singletons; XOR can produce any value up
                           [𝑎𝑙𝑜 ⊕ 𝑏𝑙𝑜 , 𝑎ℎ𝑖 ⊕ 𝑏ℎ𝑖 ]            if 𝑎 and 𝑏 are singletons
    Xor                                                                                    to the highest bit set in either operand,
                           [0, 2 ⌈log2 ( (𝑎ℎ𝑖 |𝑏ℎ𝑖 )+1) ⌉ − 1] else
                                                                                           hence lower bound is 0.
                                                                                           Unsigned floor division; returns full word if 𝑏𝑙𝑜 = 0
    Div                    [⌊𝑎𝑙𝑜 /𝑏ℎ𝑖 ⌋, ⌊𝑎ℎ𝑖 /𝑏𝑙𝑜 ⌋]
                                                                                           (division by zero possible).
                                                                                           Signed division; C = {𝑎𝑙𝑜 /𝑏𝑙𝑜 , 𝑎𝑙𝑜 /𝑏ℎ𝑖 , 𝑎ℎ𝑖 /𝑏𝑙𝑜 , 𝑎ℎ𝑖 /𝑏ℎ𝑖 }
    SDiv                   [min(C), max(C)]                                                over signed interpretation; full word if 0 ∈ [𝑏𝑙𝑜 , 𝑏ℎ𝑖 ]
                                                                                           or if 𝑎𝑙𝑜 = INT_MIN and 𝑏 = [−1, −1].
                           [1, 1] if 𝑎 and 𝑏 are equal singletons;                         Eq and NEq are duals: NEq g inverts the singleton
    Eq / NEq               [0, 0] if [𝑎𝑙𝑜 , 𝑎ℎ𝑖 ] ∩ [𝑏𝑙𝑜 , 𝑏ℎ𝑖 ] = ∅;                      cases; exact whenever the intervals are disjoint
                           [0, 1] otherwise                                                or both singletons.
                                                                                           Unsigned less-than over 32-bit words; exact when
    Lt                     [1, 1] if 𝑎ℎ𝑖 < 𝑏𝑙𝑜 ;   [0, 0] if 𝑎𝑙𝑜 ≥ 𝑏ℎ𝑖 ;   else [0, 1]
                                                                                           intervals are entirely on one side of each other.
                                                                                           Signed less-than; bounds interpreted as two’s
    SLt                    [1, 1] if 𝑎ℎ𝑖 < 𝑏𝑙𝑜 ;   [0, 0] if 𝑎𝑙𝑜 ≥ 𝑏ℎ𝑖 ;   else [0, 1]
                                                                                           -complement signed 32-bit integers before comparison.
                                                                                           Signed less-than-or-equal; same as SLt but with
    SLe                    [1, 1] if 𝑎ℎ𝑖 ≤ 𝑏𝑙𝑜 ;   [0, 0] if 𝑎𝑙𝑜 > 𝑏ℎ𝑖 ;   else [0, 1]     non-strict inequality, so the certain-true condition uses
                                                                                           ≤ instead of <.
                                                                                           Logical right-shift by a possibly-uncertain amount;
                           [0, 0] if 𝑏𝑙𝑜 ≥ 32;
                                                                                           shifting by ≥ 32 always yields 0; shifting by a range
    SRL                    [𝑎𝑙𝑜 ≫ 𝑏ℎ𝑖 , 𝑎ℎ𝑖 ≫ 𝑏𝑙𝑜 ] if 𝑏ℎ𝑖 < 32;
                                                                                           [𝑏𝑙𝑜 , 𝑏ℎ𝑖 ] yields minimum at the maximum shift and
                           [0, 𝑎ℎ𝑖 ≫ 𝑏𝑙𝑜 ] otherwise
                                                                                           maximum at the minimum shift.
Efficient Branch-and-Bound Testing and Verification of zkVMs                                      CCS ’26, November 15–19, 2026, The Hague, Netherlands


Table 9: Sound Over-Approximated Next-PC Computation cf   e for Control-Flow Opcodes. pc denotes the current program counter
interval; 𝛿 is the default step size; ⊕ denotes unsigned modular addition (AddU). Branch outcomes are computed using the
three-valued predicates from Table 8.


               Opcode       cf(pc,
                            e      𝔞, 𝔟, 𝔠)                      Notes
                            pc ⊕ 𝔠 if Eq(𝔞,
                                         f 𝔟) = [1, 1];
               BEQ          pc ⊕ [𝛿, 𝛿] if Eq(𝔞,
                                            f 𝔟) = [0, 0];       Branch taken iff 𝔞 = 𝔟 (unsigned).
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
                            pc ⊕ 𝔠 if Eq(𝔞,
                                         f 𝔟) = [0, 0];
               BNE          pc ⊕ [𝛿, 𝛿] if Eq(𝔞,
                                            f 𝔟) = [1, 1];       Branch taken iff 𝔞 ≠ 𝔟.
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
                            pc ⊕ 𝔠 if SLt(𝔞,
                                         g 𝔟) = [0, 0];
               BGE          pc ⊕ [𝛿, 𝛿] if SLt(𝔞,
                                            g 𝔟) = [1, 1];       Branch taken iff 𝔞 ≥𝑠 𝔟 (signed).
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
                            pc ⊕ 𝔠 if SLe(𝔞,
                                         g 𝔟) = [0, 0];
               BGT          pc ⊕ [𝛿, 𝛿] if SLe(𝔞,
                                            g 𝔟) = [1, 1];       Branch taken iff 𝔞 >𝑠 𝔟 (signed).
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
                            pc ⊕ 𝔠 if SLe(𝔞,
                                         g 𝔟) = [1, 1];
               BLE          pc ⊕ [𝛿, 𝛿] if SLe(𝔞,
                                            g 𝔟) = [0, 0];       Branch taken iff 𝔞 ≤𝑠 𝔟 (signed).
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
                            pc ⊕ 𝔠 if SLt(𝔞,
                                         g 𝔟) = [1, 1];
               BLT          pc ⊕ [𝛿, 𝛿] if SLt(𝔞,
                                            g 𝔟) = [0, 0];       Branch taken iff 𝔞 <𝑠 𝔟 (signed).
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
                            pc ⊕ 𝔠 if Lt(𝔞,
                                         e 𝔟) = [0, 0];
               BGEU         pc ⊕ [𝛿, 𝛿] if Lt(𝔞,
                                            e 𝔟) = [1, 1];       Branch taken iff 𝔞 ≥𝑢 𝔟 (unsigned).
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
                            pc ⊕ 𝔠 if Lt(𝔞,
                                         e 𝔟) = [1, 1];
               BLTU         pc ⊕ [𝛿, 𝛿] if Lt(𝔞,
                                            e 𝔟) = [0, 0];       Branch taken iff 𝔞 <𝑢 𝔟 (unsigned).
                            (pc ⊕ 𝔠) ∪ (pc ⊕ [𝛿, 𝛿]) otherwise
               JAL          pc ⊕ 𝔟                               Unconditional jump; target = pc + 𝔟 (signed offset).
               JALR         AddU(𝔟,
                                     𝔠)                         Indirect jump; target = (𝔟 + 𝔠) mod 𝑊 (register + immediate).
               Jumpi        𝔟                                    Absolute indirect jump; target is the value of register 𝔟 directly.


     ∀identity, identity ∈Finset.image recordId.toIdentity                        (h2 : TableGeneratorFaithful cfg recordId gen2 )
          records ↔                                                               (records : RecordSet Record) :
       ∃row ∈table, cfg.isReal row ∧cfg.projectRow row =                          canonicalize cfg (gen1 records) = canonicalize cfg (
            identity                                                                   gen2 records) := by
                                                                                rw [canonicalize_generated_eq_recordIds cfg recordId gen
  def TableGeneratorFaithful                                                         1 h1 records,
      (cfg : Config Identity) (recordId : RecordIdentity                            canonicalize_generated_eq_recordIds cfg recordId gen2
           Record Identity)                                                               h2 records]
      (generateTable : RecordSet Record →Trace) : Prop :=
    ∀records, TableEncodesRecords cfg recordId records (
         generateTable records)
                                                                            Property 2: Quotient–image bijection. The canonical trace space
                                                                            Db = D/∼ R of Definition 4.8, and the image Im(R) are formalized
Property 1: Generator-independence. We first prove that any                 as follows:
two faithful generators, regardless of how they order rows or insert
padding, result in the same canonicalized representation.                     abbrev CanonicalTraceSpace (cfg : Config Repr) :=
                                                                                  Quotient (semanticSetoid cfg)
  theorem canonicalize_generator_independent
      (cfg : Config Identity) (recordId : RecordIdentity                      abbrev CanonicalizerImage (cfg : Config Repr) :=
           Record Identity)                                                     {reprs : Finset Repr // ∃table,
      (gen1 gen2 : RecordSet Record →Trace)                                      canonicalize cfg table = reprs }
      (h1 : TableGeneratorFaithful cfg recordId gen1 )
CCS ’26, November 15–19, 2026, The Hague, Netherlands                                                  Hideaki Takahashi, Suman Jana, and Junfeng Yang


The map quotientToImage then lifts canonicalize through the quo-          Column Map                              Canonicalizer
tient, sending each equivalence class to the canonical form shared          0:                    0 fn canonicalized_repr_add(table) {
by its representatives, and is proved to be bijective:                      1:                    1    let record_reprs = HashSet::new();
                                                                            2:                    2    for i in 0..n {
  theorem canonicalTraceSpace_equiv_image
                                                                            3:                    3      if table[i][15].is_not_zero() {
    (cfg : Config Repr) :                                                   4:                    4         record_reprs.insert(
    Function.Bijective (quotientToImage cfg)                                5:                    5            format!(
                                                                            6:                    6              "x: {}, y: {}, z: {}",
Property 3: Record-set injectivity. We further prove that distinct          7:                    7               table[i][[7, 8, 9, 10]],
                                                                            8:                    8               table[i][[11, 12, 13, 14]],
executions produce distinct canonical forms, provided the record
                                                                            9:                    9               table[i][[0, 1, 2, 3]]
encoding is injective.                                                     10:                    10           )
  theorem canonicalize_generated_eq_iff_records_eq                         11:                    11         );
      (cfg : Config Identity) (recordId : RecordIdentity                   12:                    12     }
           Record Identity)                                                13:                    13   }
                                                                           14:                    14   return record_reprs;
      (generateTable : RecordSet Record →Trace)
                                                                           15: is_real            15 }
      (hgen : TableGeneratorFaithful cfg recordId
           generateTable)
      (records1 records2 : RecordSet Record) :                          Figure 8: Pseudo-code of a canonicalizer (R) for the ADD
      canonicalize cfg (generateTable records1 ) =                      table. R projects raw trace tables into unique sets of semantic
        canonicalize cfg (generateTable records2 ) ↔                    execution records, filtering out internal helper witnesses (e.g.,
      records1 = records2                                               carry bits) and padding rows (via the is_real selector).
This theorem discharges the cardinality interpretation: |𝑄 | counts
semantically distinct executions rather than representational vari-     C.2     Search Optimization
ants. Injectivity of rid is required because two different executions
                                                                           Lemma C.1 (Soundness of Conditional-Const-Gate). Let 𝑇˜
could otherwise collide on the same operand tuple.
                                                                        be an interval state, and let 𝑠, 𝑣 be cells of 𝑇˜ with 𝐼𝑠 = [1, 1]. Suppose
Instantiation. Each evaluated zkVM specializes the framework            the constraint 𝑠 · (𝑣 − 𝜏) = 0 holds over F𝑝 for some constant 𝜏 ∈ F𝑝 .
by fixing the column layout of cfg for each supported table. As         Then the refinement 𝐼 𝑣 ← 𝐼 𝑣 ∩ [𝜏, 𝜏] is sound: for every concrete
an example, consider Fig. 8, where the column map defines the           𝑇 ∈ J𝑇˜ K𝑝 satisfying the constraint, 𝑇 remains in J𝑇˜ ′ K𝑝 , where 𝑇˜ ′ is 𝑇˜
purpose of each column, while the canonicalizer is shown in Rust-       with 𝐼 𝑣 replaced by the refined interval.
style pseudo-code. This figure is based on the actual implementation       Proof. Fix any𝑇 ∈ J𝑇˜ K𝑝 satisfying 𝑠 ·(𝑣 −𝜏) = 0. Since 𝐼𝑠 = [1, 1],
for SP1’s AddSub table. This table identifies the first input operand   the concrete value of 𝑠 in 𝑇 equals 1, so the constraint reduces to
as the byte-limb group at columns 7–10, the second at columns 11–       𝑣 − 𝜏 = 0 in F𝑝 , i.e., 𝑣 = 𝜏. Hence 𝑣 ∈ J[𝜏, 𝜏]K𝑝 , and therefore
14, and the result at columns 0–3. The corresponding configuration      𝑣 ∈ J𝐼 𝑣 ∩ [𝜏, 𝜏]K𝑝 . All other cells are unchanged, so 𝑇 ∈ J𝑇˜ ′ K𝑝 . □
assembles these indices into the ALU operand tuple (𝑏, 𝑐, 𝑎):
  def addConfig (isReal : Row →Bool) : Config ALU.Tuple :=                   Lemma C.2 (Soundness of Conditional-Var-Gate). Let 𝑇˜ be
    mkALUConfig [7, 8, 9, 10] [11, 12, 13, 14] [0, 1, 2, 3]             an interval state, and let 𝑠, 𝑎, 𝑏 be cells of 𝑇˜ with 𝐼𝑠 = [1, 1]. Suppose
         isReal                                                         the constraint 𝑠 · (𝑎 − 𝑏) = 0 holds over F𝑝 . Then the refinement
                                                                        𝐼𝑎 , 𝐼𝑏 ← 𝐼𝑎 ∩ 𝐼𝑏 is sound.
Then, the record-set injectivity theorem states:
                                                                           Proof. Fix any𝑇 ∈ J𝑇˜ K𝑝 satisfying 𝑠·(𝑎−𝑏) = 0. Since 𝐼𝑠 = [1, 1],
  theorem add_one_to_one (isReal : Row →Bool)
                                                                        we have 𝑠 = 1 in 𝑇 , and the constraint reduces to 𝑎 = 𝑏 in F𝑝 . Let 𝑣
      (tableId : ALU.Tuple →Identity)
                                                                        denote this common value. Then 𝑣 ∈ J𝐼𝑎 K𝑝 (since 𝑎 was assigned
      (recordId : Generic.RecordIdentity Record Identity)
                                                                        from 𝐼𝑎 ) and 𝑣 ∈ J𝐼𝑏 K𝑝 (since 𝑏 = 𝑎 was assigned from 𝐼𝑏 ), so
      (generateTable : Generic.RecordSet Record →Trace)
                                                                        𝑣 ∈ J𝐼𝑎 K𝑝 ∩ J𝐼𝑏 K𝑝 ⊆ J𝐼𝑎 ∩ 𝐼𝑏 K𝑝 . The same holds symmetrically for 𝑏,
      (hgen : Generic.TableGeneratorFaithfulToIds
                                                                        so 𝑇 ∈ J𝑇˜ ′ K𝑝 .                                                    □
        (addConfig isReal) tableId recordId generateTable)
      (records1 records2 : Generic.RecordSet Record) :                      Lemma C.3 (Soundness of Affine-Backward). Let 𝑇˜ be an
      Generic.recordIdsOfTable (addConfig isReal) tableId (             interval state, let 𝐿 be an affine expression over cells of 𝑇˜ , and let
           generateTable records1 ) =                                   𝑎, 𝑒 be cells with 𝑎, 𝑒 ∉ FV(𝐿). Let 𝑑 > 0 be a constant, and let
        Generic.recordIdsOfTable (addConfig isReal) tableId             𝐼𝑎 = [𝑎𝑙𝑜 , 𝑎ℎ𝑖 ], 𝐼𝐿 = [ℓ, ℎ], 𝐼𝑒 = [𝑒𝑙𝑜 , 𝑒ℎ𝑖 ] be the current intervals.
             (generateTable records2 ) ↔                                Suppose the side condition
      records1 = records2
                                                                                     |ℓ | + |ℎ| + 𝑑 (|𝑒𝑙𝑜 | + |𝑒ℎ𝑖 |) + |𝑎𝑙𝑜 | + |𝑎ℎ𝑖 | < 𝑝       (★)
The corollary states that this add canonicalizer is one-to-one on
record sets, conditional on the generator being faithful and on the     holds, and the constraint 𝑎 = 𝐿−𝑑·𝑒 holds over F𝑝 . Then the refinement
record encoding being injective. Analogous corollaries hold for
                                                                                                                         
                                                                                                        ℓ − 𝑎ℎ𝑖     ℎ − 𝑎𝑙𝑜
                                                                                         𝐼𝑒 ← 𝐼𝑒 ∩
other zkVMs’ instruction tables.
                                                                                                                 ,
                                                                                                           𝑑           𝑑
Efficient Branch-and-Bound Testing and Verification of zkVMs                                        CCS ’26, November 15–19, 2026, The Hague, Netherlands


is sound.                                                                    rules: program-counter modification, ALU result and operand modi-
                                                                             fication, instruction replay, and syscall-identifier modification. In all
    Proof. Fix any 𝑇 ∈ J𝑇˜ K𝑝 satisfying 𝑎 = 𝐿 − 𝑑 · 𝑒 in F𝑝 . By            cases we apply the safe remainder/division transformation provided
definition of J·K𝑝 , there exist integer witnesses 𝑎ˆ ∈ [𝑎𝑙𝑜 , 𝑎ℎ𝑖 ] and     by Arguzz to avoid spurious divide-by-zero crashes that would oth-
𝑒ˆ ∈ [𝑒𝑙𝑜 , 𝑒ℎ𝑖 ] reducing modulo 𝑝 to the values of 𝑎 and 𝑒 in 𝑇 , and an   erwise dominate the coverage signal.
integer witness 𝐿ˆ ∈ [ℓ, ℎ] obtained by evaluating 𝐿 over the integer           All experiments are run with the same random seeds, on identical
witnesses of its free variables (well-defined since 𝑎, 𝑒 ∉ FV(𝐿)). By        hardware to the one used for our ZEBRA, and for the same wall-
the side condition (★), the triangle inequality gives                        clock budget of six hours per target.
 ˆ 𝑒−
|𝐿−𝑑· ˆ 𝑎|   ˆ
        ˆ ≤ |𝐿|+𝑑·| 𝑒ˆ|+|𝑎|
                         ˆ ≤ |ℓ |+|ℎ|+𝑑 (|𝑒𝑙𝑜 |+|𝑒ℎ𝑖 |)+|𝑎𝑙𝑜 |+|𝑎ℎ𝑖 | < 𝑝,       Input Range Verification via SMT solver. We also conduct the input
                                                                             range verification via the SMT solver. Specifically, the blocking-
so 𝐿ˆ − 𝑑 · 𝑒ˆ − 𝑎ˆ ∈ (−𝑝, 𝑝). Since this integer quantity reduces to 0
                                                                             closure mechanism is repurposed accordingly: the verification starts
modulo 𝑝 (by the constraint), it must equal 0 in Z. Hence 𝑎ˆ = 𝐿ˆ −𝑑 · 𝑒ˆ
                                                                             from applying Z3 solver to the constraints without blocking closure,
holds over Z, which rearranges to 𝑒ˆ = (𝐿ˆ − 𝑎)/𝑑.ˆ      Applying interval
                                                                             and each iteration extracts the satisfying input and output from
arithmetic over Z, we have 𝐿ˆ − 𝑎ˆ ∈ [ℓ − 𝑎ℎ𝑖 , ℎ − 𝑎𝑙𝑜 ]. Dividing by
                                                                             Z3’s returned model and appends a blocking constraint forbidding
𝑑 > 0 gives 𝑒ˆ ∈ [(ℓ − 𝑎ℎ𝑖 )/𝑑, (ℎ − 𝑎𝑙𝑜 )/𝑑]. Since 𝑒ˆ is an integer,
                                                                             that input-output pair. The loop terminates once Z3 returns unsat,
                                                                             where every input in 𝑉 admitting is expected to be enumerated.
                                                
                               ℓ − 𝑎ℎ𝑖     ℎ − 𝑎𝑙𝑜
                       𝑒ˆ ∈             ,              .
                                  𝑑           𝑑                                  Tab. 10 reports the resulting speedups over the point-wise verifi-
                                                                             cation with the Z3 SMT solver, averaged over all opcodes per zkVM.
Combined with 𝑒ˆ ∈ J𝐼𝑒 K𝑝 , we conclude 𝑒ˆ lies in the refined interval,
                                                                             Three observations stand out. First, the speedup never reaches
so 𝑇 ∈ J𝑇˜ ′ K𝑝 .                                                    □       1×: across every zkVM and every |𝑉 |, the SMT range query is
                                                                             slower than the corresponding |𝑉 | independent point queries. This
D     Experiment Details                                                     is structural rather than incidental to our encoding. Blocking-clause
   Configurations of SMT Baseline. For the SMT baseline, each trace          enumeration must, by construction, issue at least |𝑉 | sat calls (one
cell is materialized as a 32-bit bit-vector variable, and every AIR          per witness in 𝑉 ) plus a final unsat call to certify exhaustion, while
constraint is translated into its bit-vector equivalent, with field-         accumulating |𝑉 | blocking literals that progressively dilate each
prime equalities reduced via bvurem. An SMT solver, however, is              subsequent solve. Second, the trend is non-monotonic, peaking
an existential procedure: it returns a single satisfying assignment          near |𝑉 | =26 : for small |𝑉 | the per-query process and parser over-
or certifies that none exists, but it cannot directly decide whether         heads dominate the ratio, whereas for large |𝑉 | the cumulative
a constraint set is tightly determined by its inputs. To turn it into        blocking-clause bloat slows late iterations enough to outweigh the
an under-constraint detector, we first execute the zkVM’s refer-             amortization. Third, the largest volume |𝑉 | =214 exhausts the solver
ence emulator to obtain an honest input–output pair (x★, y★), then           budget on every zkVM, and Valida fails to produce data for any
append a blocking constraint that excludes y★ from the solver’s              |𝑉 |: sequential SMT enumeration does not scale to input regions of
output space. The resulting query is satisfiable iff there exists an         practical interest.
alternative trace that agrees with the honest input x★ and the AIR
but disagrees with y★, i.e., a witness of under-constrained behavior;        Table 10: Speedup of Z3 SMT solver’s input range verification
otherwise the query is unsatisfiable, certifying that no such bug            over the iterative point-wise baseline, across input volumes
exists for that input. Each per-table formula is dispatched to Z3            |𝑉 |. T/O denotes the timeout.
under the same wall-clock timeout used for ZEBRA.
   Configurations of Fuzzer Baseline. We use Arguzz, the state-of-                  zkVM       |𝑉 | = 22   |𝑉 | = 26    |𝑉 | = 210    |𝑉 | = 214
the-art fuzzer for zkVMs [15], as the common driver across all five                 Valida       T/O         T/O           T/O           T/O
targets. Arguzz combines metamorphic testing of zkVM circuit exe-                   Sphinx       0.4×        0.6×         0.5×           T/O
cutions with controlled fault injection into the host-side executor,                 Pico        0.6×        0.6×         0.5×           T/O
which lets it expose both completeness violations (the prover re-                     SP1        0.6×        0.7×         0.5×           T/O
fuses an honestly executed program) and soundness violations (the                    Ziren       0.5×        0.7×         0.5×           T/O
verifier accepts a tampered execution).
   SP1 and Pico are supported by the original Arguzz release, and
we additionally implemented Arguzz front-ends for other Sphinx,
Ziren, and Valida. For each new target, we follow the extension
architecture prescribed by Arguzz: a description of the target ISA’s
opcodes, an enumeration of the fault sites exposed by the host
executor, a project generator that emits a host/guest pair against
the zkVM’s SDK, and a small patch to the executor that realizes
the fault primitives. For Ziren we replace Arguzz’s RISC-V opcode
table with the MIPS32r2 instruction set and retarget the syscall-
identifier injection to MIPS’ syscall convention. For Valida whose
ISA is a custom one, we also support basic transferable injection
