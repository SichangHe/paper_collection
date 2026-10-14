                                             VeGo: Direct Deductive Formal Verification of Go
                                                Programs for Computer Science Education
                                                                    Tina Masoudi Christopher Dutchyn
                                                                        Department of Computer Science
                                                                          University of Saskatchewan
                                                                            Saskatoon, SK, Canada
arXiv:2608.22630v1 [cs.PL] 23 Aug 2026




                                                                     uka071@usask.ca cjd032@usask.ca

                                                                                      August 2026


                                                                                          Abstract
                                                  Teaching formal software verification to computer science undergraduates is historically
                                              hindered by a steep cognitive barrier: students must simultaneously master formal logic (Hoare
                                              triples, loop invariants, mathematical induction) and a new, specialized verification language
                                              (such as Dafny) or abstract specification formalism (such as TLA+). The original pedagogical
                                              foundation for software specification in computer science curricula was established by R.D.
                                              Tennent in Specifying Software (2002), which advocated integrating formal specifications directly
                                              alongside imperative programs. However, Tennent’s methodology lacked automated verification
                                              tool support over a modern, executable programming language.
                                                  In this paper, we present VeGo (Verified Go), a deductive formal verification system that
                                              enables direct verification of standard Go source code. VeGo incorporates Hoare-style contracts
                                              (//@ Requires, //@ Ensures, //@ Exsures), loop invariants and integer variants, well-founded
                                              recursive measures, block-level scope invariants (//@ Preserves), and equational reasoning
                                              chains with primed variables (x′ ) directly into non-intrusive Go comments. We detail the
                                              language selection rationale justifying Go as an ideal balance over C, C++, Java, and Rust,
                                              leveraging Go’s native multiple return values as a modern replacement for Pascal’s input-
                                              output (VAR) parameters. We detail the tool architecture, exploiting the theoretical equivalence
                                              between Static Single Assignment (SSA) form and first-order functional programming (Pfenning,
                                              Kelsey, Appel, Rastello), desugaring of clopen interval quantifiers and Reynolds’ skip statement,
                                              weakest precondition (wp) calculus, and native Hindley–Milner (HM[X]) constraint inference and
                                              verification condition resolution over SSA form. Furthermore, as Martin Kleppmann observes,
                                              formal methods are rapidly becoming accessible and practical due to AI coding agents, which
                                              assist developers and students in generating specifications while native HM[X]/SSA verifiers
                                              provide rigorous mathematical guardrails. We formalize contract precision checking (wp vs. sp)
                                              using an explicit analogy to Hindley-Milner (HM[X]) type inference. Finally, we evaluate VeGo
                                              across classroom case studies and outline a roadmap for formal concurrency specifications using
                                              epistemic temporal logic (Fagin et al., Owicki–Gries, Chandy–Misra).


                                         1    Introduction
                                         Formal software verification is critical for constructing high-assurance software systems. However,
                                         integrating formal methods into the core computer science undergraduate curriculum remains a
                                         persistent challenge. Historically, instructors faced a trade-off: either present formal logic abstractly
                                         using paper-and-pencil proofs without tool automation, or require students to learn a research-
                                         oriented specification language (e.g., Dafny [19], Spec#, or Coq/Isabelle) that is divorced from

                                                                                             1
the mainstream imperative programming languages students use in their day-to-day software
development.
    Furthermore, the conceptual framework for teaching software specification as a core computing
discipline was pioneered by R.D. Tennent in Specifying Software: A Curriculum Foundation for
Formal Methods [25]. Tennent demonstrated that rigorous reasoning about program correctness
should be integrated directly into imperative programming instruction. However, at the time of
its publication, Tennent’s methodology lacked automated tool support capable of executing and
verifying programs written in a modern, production-grade language.
    To fulfill this pedagogical vision, we developed VeGo (Verified Go). VeGo enables students
and instructors to write formal specifications directly inside standard Go source files using special
comment annotations (//@). Because specifications reside in comments, every VeGo file remains
100% valid Go source code that compiles and executes natively using standard Go toolchains, while
simultaneously undergoing static formal verification via the vegop verification engine and Visual
Studio Code Language Server Protocol (LSP) extension.


2     Language Selection Rationale: Why Go?
A foundational design decision in building VeGo was selecting the underlying programming language.
We evaluated several candidate paradigms before selecting Go:

    1. Purely Functional Languages (Haskell, OCaml, Standard ML): Functional languages
       excel at equational reasoning and immutability. However, core computer science curricula
       require students to master imperative state transformations, array manipulations, and mutable
       memory structures. While VeGo supports equational reasoning chains via primed variable
       annotations (x′ ), retaining an underlying imperative language is essential for algorithmic
       breadth.

    2. C: C suffers from severe semantic gaps, unhygienic preprocessor macros, lack of native boolean
       types (relying on integer truthiness), and unchecked pointer arithmetic. These low-level
       hazards distract second-year students from high-level algorithmic logic and formal contract
       specification.

    3. C++: The procedural subset of C++ is heavily entangled with complex object-oriented
       features, multiple inheritance, Liskov substitution friction, and template instantiation overhead
       when only clean data invariants and structural interface contracts are required.

    4. Java: Java lacks an effective procedural fragment; every function must be wrapped in class
       boilerplate (public static void main). Enforcing interface invariants requires introducing
       full-on object-oriented class mechanics rather than lightweight standalone functions and
       structural interfaces.

    5. Rust: Rust offers strong memory safety, but imposes steep cognitive friction on second-year
       students. Introductory code quickly collides with lifetime annotations (’a), borrow-checker
       restrictions, explicit trait bounds, and syntax overload (Result<T,E>).

    6. Go (The Ideal Balance): Go provides a “sweet spot” for educational formal verification:

         • Clean Imperative Semantics: Strict type safety without pointer arithmetic traps or
           undefined behavior.


                                                   2
         • Native Multiple Return Values with Result Identifiers (Pascal VAR Analogy): Go’s native
           support for returning multiple values with explicit names (func Divide(n, d int)
           (q, r int)) acts as a modern, side-effect-free replacement for Pascal’s input-output
           (VAR) parameters. Crucially, these named return identifiers (q, r) serve as first-class,
           mathematically bound target symbols in postcondition contracts (//@ Ensures n = d*q
           + r), providing intuitive result names for formal specification without requiring auxiliary
           result wrappers, pointer indirection, or heap object allocation.
         • First-Class Guardrails: Native boolean types, garbage collection, and high-level string/s-
           lice abstractions (avoiding null-terminated character array pitfalls).
         • Lightweight Structural Interfaces: Structural subtyping that naturally captures data
           invariants without class hierarchy overhead.
         • Native Concurrency Primitives: Channels and go routines providing a clean foundation
           for formal concurrency specifications.


3     Formal Verification in the Era of AI Code Generation
The modern motivation for teaching formal logic and program verification has been fundamentally
transformed by the rise of Artificial Intelligence (AI) code generation and Large Language Models
(LLMs). As Martin Kleppmann [16] and Adam Chlipala [3–5] observe across recent analyses of
programming language economics, the emergence of automated code synthesis alters how developers
and computer science students interact with formal methods:

    1. Accessibility via AI Specification Synthesis: Historically, drafting formal contracts,
       candidate loop invariants, and termination measures was a major friction point. AI coding
       agents dramatically lower this entry barrier by synthesizing candidate preconditions, postcon-
       ditions, and proof obligations, making formal verification practical for everyday developers
       and students [4, 16].
    2. Guardrails Against AI Slop (The Automated Verifier as Primary Reviewer): While
       LLMs rapidly generate vast volumes of code, they frequently produce “AI slop”—untested,
       edge-case-ridden code that appears plausible but contains subtle bugs, missing bounds, and
       logic hallucinations. In this paradigm, the automated HM[X]/SSA verifier serves as the
       primary, unassailable code reviewer, enforcing strict mathematical guardrails that audit and
       constrain AI-generated code.
    3. Subversion-Resistance for Free: As Chlipala points out [5], traditional security auditing
       attempts to enumerate every possible attack vector. Deductive formal verification flips this
       dynamic: by proving that an implementation adheres strictly to its formal specification,
       the software gains subversion-resistance for free, guaranteeing that hidden backdoors, buffer
       overflows, or AI hallucinations cannot breach verified contracts without failing verification.
    4. Overcoming Language Handicaps: Chlipala further demonstrates [3] that AI coding tools
       face major handicaps when targeting low-level languages (C/C++) due to pointer aliasing
       fictions, unhygienic macros, and undefined behaviors. VeGo’s selection of Go eliminates these
       low-level fictions, providing an ideal, alias-free imperative foundation for AI specification
       generation and native verification.
    5. Reinvesting the Productivity Windfall into Professional Software Engineering: If
       AI code generation delivers massive efficiency gains and speed, how should software engineering

                                                  3
      spend that productivity windfall? Rather than merely generating un-audited code faster,
      engineering organizations and computer science curricula can reinvest that efficiency gain
      into elevating software to true professional software engineering—producing formally verified,
      high-assurance code.


4     The VeGo Specification Language
VeGo embeds Hoare logic contracts [10, 11] directly into Go source code using special //@ comment
annotations. This allows source files to remain valid Go programs while enriching them with
first-order logic specifications that are processed by the native verifier.

4.1    Syntax Architecture and Logical Expressions
VeGo’s specification syntax provides a complete first-order logic grammar embedded within inline
comments:
    • Core Specification Constructs: Function contracts (//@ Requires, //@ Ensures, //@
      Exsures), loop annotations (//@ Invariant, //@ Variant), recursive termination measures
      (//@ Measure), user-defined inductive predicates (//@ Predicate), block invariants (//@
      Preserves), and immutability declarations (//@ Immutable).
    • Logical Operators: Conjunction (^), disjunction (v), negation (~), logical implication (->),
      and bi-implication (<->).
    • Quantifiers and Domains: Universal (Forall), existential (Exists), and unique existential
      (Unique) quantification over integer domains (Z or Z), boolean domains (B or B), and bounded
      integer intervals ([a, b], [a, b), (a, b], (a, b)).
    • Slice Range Quantifier Shorthand: Range expressions such as A[0:j) desugar automati-
      cally at parse time into bounded quantifiers. For example, order comparisons like A[j] >=
      A[0:j) desugar into:
         A[j] >= A[0:j)      ::=    Forall idx in Z :
                                      (((0 <= idx) ^ ( idx < j)) -> (A[j] >= A[ idx]))

 Annotation Line Termination (The Go Semicolon Insertion Analogy): VeGo directly
 extends Go’s native lexical semicolon insertion convention—where the last token on a line informs
whether a statement terminates or continues onto the next line—to multiline logic annotations. If
 an annotation line ends with an unclosed continuation token (such as a binary operator ^, v, ->, +,
-, or predicate assignment ::=), the lexer seamlessly treats the subsequent comment line (//@) as
 an inline continuation of the logic expression. Conversely, if the last token on an annotation line
 is a terminating token (an identifier, integer constant, closing parenthesis ), bracket ], or primed
 symbol x’), the parser infers statement termination. This allows long formal contracts and multiline
 inductive predicates (such as sumTo or sumRecPred) to span cleanly across multiple comment lines
without requiring explicit line-continuation backslashes or trailing semicolons.

4.2    Relational State Specifications, Multi-Primed Sequences, and Loop Scope
       Reconstitution
A central challenge in imperative program verification is formalizing state transitions—relating
updated or mutated values of variables after an operation to their original values prior to the

                                                  4
operation. VeGo addresses this by adopting the primed variable convention (x′ ), directly extending
Hoover & Rudnicki’s formal reasoning methodology [12]:

   • Pre-State vs. Post-State Binding: In any statement specification or relational assertion
     block, an unprimed identifier (x, r, A) denotes the pre-state value prior to statement execution.
     A primed identifier (x′ , r′ , A′ ) denotes the mutated post-state value immediately following
     the statement or single loop iteration.

   • Multi-Primed Sequences for Declarations and Assignments: In Go, the short variable
     declaration x := 0 defines and initializes x, binding the unprimed symbol x directly to
     the defined value (x = 0). Subsequent imperative assignments to x within the same scope
     introduce primed symbols (x′ , x′′ , x′′′ , . . . ) to track sequential mutations. For example, given
     the declaration and assignment sequence:

                                     x := 0; x = x + 1; x = x + 2

     x denotes the initial defined state (x = 0), x′ denotes the state after the first assignment
     (x′ = x + 1 = 1), and x′′ denotes the state after the second assignment (x′′ = x′ + 2 = 3).
     Following this sequence, the relational assertion holds:

                                 //@ Assert x = 0 ^ x’ = 1 ^ x’’ = 3

     Each prime level maps 1-to-1 to successive SSA version subscripts (x0 , x1 , x2 ) generated by
     the native verifier.

   • Loop Scope Reconstitution of Primes: Primed variables are scoped strictly to individual
     statement blocks and single loop iterations. Inside a loop body, x′ represents the updated
     value produced by that single iteration relative to x at the start of the iteration. At the end of
     each loop iteration (at the loop latch/back-edge), primed states are reconstituted : the updated
     value x′ becomes the unprimed state x at the header of the next iteration. This reconstitution
     allows the loop invariant at the top of a loop to refer directly to the updated counter and
     accumulator (i, s) from the end of the preceding iteration without requiring cumulative primes
     (i′′′′ ). Upon loop exit, the final loop state is bound to unprimed x for post-loop reasoning.

   • Relational Loop Variants: Loop termination measures use the primed convention to
     explicitly assert both non-negativity and strict monotonic decrease across a single loop
     iteration. For example, in integer division (Divide), the loop variant is specified as:

                                   //@ Variant 0 <= r’ = r - d < r

     This single proposition asserts that the post-iteration remainder r′ equals r − d, remains
     non-negative (0 ≤ r′ ), and strictly decreases relative to the pre-iteration remainder (r′ < r).

   • Array and Slice Mutation Invariants: When modifying slice elements in place, primed ar-
     ray syntax (A′ [i]) characterizes relational update properties (e.g., A′ [i] = 2·A[i]), distinguishing
     mutated elements from preserved un-mutated elements (A′ [k] = A[k] for k ̸= i).

   • SSA Version Mapping: The native verifier processes primed variables by mapping unprimed
     symbols (x) to their input SSA version (xk ) and primed symbols (x′ ) to their output SSA
     version (xk+1 ). This translates imperative state changes into clean, static first-order arithmetic
     constraints evaluated by the HM[X] engine.

                                                    5
     4.3    Function Contracts: Preconditions, Postconditions, Named Returns, and
            Refutation
     Functions declare preconditions (//@ Requires), postconditions (//@ Ensures), and negative post-
     conditions (//@ Exsures). Go’s native support for named return values (q, r) allows postconditions
     to bind return identifiers directly without requiring auxiliary result wrappers:

           Listing 1: Function contract specification with named returns and loop variant in VeGo.
1    //@ Requires n >= 0 ^ d > 0
2    func Divide(n, d int) (q, r int) {
3        q, r = 0, n
4        //@ Invariant n >= 0 ^ d > 0 ^ n = d*q + r ^ 0 <= r
5        //@ Variant 0 <= r’ = r - d < r
6        while d <= r {
7            q, r = q + 1, r - d
8        }
9        return q, r
10   }
11   //@ Ensures n = d*q + r ^ 0 <= r ^ r < d



     Proof by Contradiction (//@ Exsures): To support Reductio ad Absurdum reasoning, VeGo
     provides //@ Exsures <expr>, which asserts that state expr is mathematically impossible upon
     function completion. The native verifier evaluates Exsures by refutation, assuming expr holds at
     exit and deriving a logical contradiction (⊥). For example, in the Sieve of Eratosthenes, proving
     that no composite number p remains unmarked is specified as:

              //@ Exsures Exists p in [2, MAX] : (~COMPOSITE[p] ^ IsComposite(p))

     4.4    Loop Specifications and Variants
     Loops require an //@ Invariant and an integer //@ Variant termination measure (bounded below
     by 0 and strictly decreasing on each iteration).
        The SumLoop algorithm accumulates slice elements iteratively. Its partial sum invariant is
     specified via the inductive predicate sumTo(A, i, s), asserting that after i iterations, s equals the
     sum of the initial i elements:
           //@ Predicate sumTo(A, i, s)        ::=    (i <= 0 -> s = 0) ^
                                                      (i > 0 -> Exists t in Z :
                                                        (sumTo(A, i-1, t) ^ s = t + A[i-1]))

        Upon loop completion when i = |A|, sumTo(A, |A|, s) guarantees that result s is the complete
     sum of all elements in slice A:

             Listing 2: Loop invariant, variant, and inductive predicate scaffolding for SumLoop.
1    //@ Predicate sumTo(A, i, s) ::= ((i <= 0 -> s = 0) ^
2    //@ (i > 0 -> Exists t in Z : (sumTo(A, i-1, t) ^ s = t + A[i-1])))
3    //@ Requires |A| >= 0
4    func SumLoop(A []int) (s int) {
5        s = 0
6        //@ Invariant 0 <= i ^ i <= |A| ^ sumTo(A, i, s)
7        //@ Variant 0 <= (|A| - i’) = (|A| - i - 1) < (|A| - i)
8        for i := 0; i < len(A); i++ {
9            s = s + A[i]


                                                      6
10      }
11      return s
12   }
13   //@ Ensures sumTo(A, |A|, s)



     4.5   Recursive Functions and Structural Induction
     Recursive algorithms are verified via structural induction over well-founded measures (//@ Measure)
     and inductive logic predicates (//@ Predicate).
         The induction hypothesis specifies that calling SumRec(A, i) computes the sum of all elements
     in slice A over the clopen interval [i, |A|). We formalize this using an inductive logic predicate
     sumRecPred(A, i, s):

      //@ Predicate sumRecPred(A, i, s)           ::=       (i >= |A| -> s = 0) ^
                                                            (i < |A| -> Exists t in Z :
                                                              (sumRecPred(A, i+1, t) ^ s = t + A[i]))

         When evaluated at i = 0, sumRecPred(A, 0, s) establishes that result s is the complete sum
     of all elements in A:

                   Listing 3: Formal contract and recursive structural induction for SumRec.
1    //@ Predicate sumRecPred(A, i, s) ::= ((i >= |A| -> s = 0) ^
2    //@ (i < |A| -> Exists t in Z : (sumRecPred(A, i+1, t) ^ s = t + A[i])))
3    //@ Requires 0 <= i ^ i <= |A|
4    //@ Measure |A| - i
5    func SumRec(A []int, i int) (s int) {
6        if i >= len(A) {
7            return 0
8        }
9        t := SumRec(A, i+1)
10       return t + A[i]
11   }
12   //@ Ensures sumRecPred(A, i, s)



     4.6   Block-Level Scope Invariants (//@ Preserves)
     To enforce structural invariants across nested scopes or state transitions (such as asserting that
     a slice’s length remains invariant while its elements are mutated in place), VeGo provides //@
     Preserves <expr>:
1    //@ Preserves |A|
2    for i := 0; i < len(A); i++ {
3        A[i] = A[i] * 2
4    }



     4.7   Contract Precision and Principal Contracts: The HM[X] Analogy
     A novel contribution of VeGo is formalizing contract precision checking using an explicit analogy to
     Hindley-Milner (HM[X]) type inference.
        In HM[X] type systems, every expression has a principal type—the most general type from
     which all other valid types can be substituted. In deductive program verification, Dijkstra’s weakest
     precondition wp(C, Q) computes the most general (weakest) precondition required for command C

                                                        7
to terminate in postcondition Q. Dually, the strongest postcondition sp(P, C) computes the most
precise state guaranteed after executing C from precondition P .
    In VeGo, the pair (wp(C, Q), sp(P, C)) acts as the Principal Contract Pair. Just as HM[X]
warns against non-principal types, VeGo checks whether a declared specification (Pdeclared , Qdeclared )
matches the principal contract pair, exposing overly restrictive preconditions or under-specified
postconditions.

Case Study: Sorting Algorithm Hierarchy. Consider distinct implementations of array
sorting (Selection Sort, Insertion Sort, Shell Sort, Quick Sort, Bitonic Sort, and Permutation Index
Sort). All implementations satisfy the weak sorting postcondition:

          //@ Predicate sorted(A) ::= Forall i in [0, |A|-1) :                    A[i] <= A[i+1]

However, a function returning all zeros also satisfies sorted(A). To achieve principal postcondition
precision, the contract must establish permutation preservation:

                     //@ Ensures sorted(A) ^ multiset(A) == multiset(A’)

Furthermore, in Permutation Index Sort (examples/sorting/permutation sort.vgo), the algo-
rithm computes an explicit permutation index vector perm[i] such that Aout [i] = Ain [perm[i]]. By
evaluating contract precision against sp(P, C), VeGo guides students from weak, vacuous specifica-
tions up to complete, principal contract bounds.


5     System Architecture and Verification Pipeline
The VeGo architecture follows a multi-stage compiler pipeline implemented entirely in native Go:

    1. Preprocessing and Desugaring: The preprocessor extracts comment specifications, maps
       them to AST nodes, and desugars clopen intervals [a, b), slice-range quantifiers (A[0 : j)),
       guarded while loops, and Reynolds’ explicit no-op skip statement [24].

    2. CFG Construction and SSA Transformation: The control flow graph is transformed into
       Static Single Assignment (SSA) form following Cytron et al. [7] and Rastello [23]. Variable
       assignments are versioned (x0 , x1 , . . . ), eliminating imperative side effects for logic translation.


       Theoretical Foundation: SSA as First-Order Functional Programming. A central
       theoretical foundation in VeGo’s verification engine is the formal equivalence established by
       Kelsey [14], Appel [1], and Pfenning [22]: Static Single Assignment (SSA) form is mathemati-
       cally isomorphic to Continuation-Passing Style (CPS) and first-order functional programming.
       In SSA form, mutating an imperative variable within a loop iteration corresponds to invoking
       a tail-recursive function where loop ϕ-nodes serve as immutable function arguments.
       VeGo exploits this isomorphism directly. Because Go natively supports multiple return values,
       an imperative loop updating multiple state variables (e.g., q, r = q + 1, r - d) desugars
       into an SSA single-step transformation that models state updates as first-order functional tuple
       returns. This eliminates pointer-alias tracking and heap memory frames, transforming complex
       imperative loop body verifications into clean, equational HM[X] assertions over versioned
       variables.


                                                       8
    3. Weakest Precondition (wp) VC Generation: Using Dijkstra’s weakest precondition
       calculus [8], VeGo generates verification conditions (V C) for each execution path.

    4. Native HM[X] Constraint Solving: VCs are evaluated directly using VeGo’s native Hindley–
       Milner HM[X] constraint solver and Fourier–Motzkin linear arithmetic solver implemented
       entirely in Go, eliminating third-party theorem prover binary dependencies like Z3.

5.1    Student Development Workflow: From .vgo Specifications to Executable
       Binaries
A key operational requirement of VeGo is providing a seamless, production-grade engineering
workflow for computer science students. The typical student development loop progresses across
five distinct phases:

    1. Initial Project Setup and Library Annotations (.vgos Headers): As an initial project
       setup step, students define formal contracts for external third-party or standard library
       packages using specification header files (.vgos). These header specifications declare external
       function preconditions and postconditions, allowing internal project code to call library
       functions without triggering unverified call-site warnings or missing function errors.

    2. Authoring Verified Source Files (.vgo): Students write standard Go code enriched with
       formal comment annotations (//@ Requires, //@ Ensures, //@ Invariant, //@ Measure).
       Because contracts reside in Go comments, every .vgo file maintains complete syntax compati-
       bility with standard Go syntax trees.

    3. Interactive Verification Feedback: During development, the vegop verification engine
       operates as a background Visual Studio Code Language Server Protocol (LSP) extension.
       As students edit code, vegop automatically constructs VCs and evaluates them natively
       via HM[X] constraint solving over SSA, emitting real-time diagnostics (e.g., unproven loop
       invariants, boundary access warnings, or vacuous contract alerts) directly in the editor margin.

    4. Un-gated V Variant Compilation Path: To balance runtime performance with mathe-
       matical rigor, the VeGo compiler generates two compiled function targets: a gated entrypoint
       (FunctionName) with dynamic assertion wrappers, and an un-gated verified internal variant
       (FunctionName V). When a call site’s preconditions are statically verified by the native verifier,
       the compiler automatically rewrites the call to target FunctionName V directly. This simple-
       yet-verified path bypasses runtime assertion checks for all internal package calls, eliminating
       execution overhead while preserving mathematical safety guarantees.

    5. Transpilation, Native Execution, and Deployment: Running vegop compile solution.vgo
       (or vegop compile-pkg ./... across an entire module) transpiles verified .vgo code into
       clean .go files. Students then build and test standalone executables natively using standard
       Go toolchains (go build, go run, go test) across macOS, Linux, and Windows.


6     Pedagogical Evaluation and Case Studies
VeGo has been evaluated across a rich suite of computer science curriculum topics:




                                                    9
6.1   Tree and Heap Encoding Paradigms: Two via Arrays and One into Boxes
A central pedagogical contribution of VeGo is exposing students to structural abstraction by disen-
tangling abstract mathematical trees and heaps from their concrete physical memory representations.
We categorize and verify tree and heap implementations across three formal encoding paradigms:

  1. Compact Array Encoding (cAT / cH):

        • Memory Layout: Implicit binary tree stored in a contiguous 1-indexed slice A[1..N].
        • Navigational Indexing: Structural topology is computed implicitly via arithmetic index
          offsets: left(i) = 2i, right(i) = 2i + 1, and parent(i) = ⌊i/2⌋.
        • Data Predicate: The heap invariant cH is heap(A, N ) is defined as a universal quantifier
          over index pairs:

                     //@ Predicate cH is heap(A, N)        ::=     Forall i in [2, N] :
                                                                     A[i/2] <= A[i]

        • Contract Metrics: Loop invariants rely on linear arithmetic index bounds (2i ≤ N ),
          enabling rapid decision procedures in the native solver.

  2. Sparse Array Encoding (sAT / sH):

        • Memory Layout: Nodes are stored sparsely in a value vector Val[1..N] paired with an
          explicit parent link array Parent[1..N], where Parent[i] = p points to node i’s parent
          (with Parent[root] = 0).
        • Navigational Indexing: Parent-child links are stored in explicit index tables rather than
          implicit arithmetic offsets, permitting non-contiguous topological layouts.
        • Data Predicate: Tree validity sAT is tree(V al, P arent) requires acyclicity (Parent[i] <
          i), while heap validity sH is heap(V al, P arent) enforces parent-value dominance:

             //@ Predicate sH is heap(Val, Parent, N)            ::=   Forall i in [1, N] :
                                                                         (Parent[i] > 0 ->
                                                                           Val[Parent[i]] <= Val[i])

        • Contract Metrics: Invariants specify explicit parent path properties, requiring inductive
          path reachability predicates.

  3. Boxed BNF Pointer Encoding (bT / bH):

        • Memory Layout: Tree nodes are defined as an inductive boxed datatype given by a
          two-line BNF display:

                            Tree ::= Node(Key ∈ Z, left ∈ Inode, right ∈ Inode)
                                 |   Leaf()

            Concrete algebraic variants are declared using Go structures and a sum-type interface
            Inode:

            Listing 4: Boxed BNF pointer encoding using Go interfaces, structs, and receiver method
            specifications.
        1   type Inode interface {


                                                 10
        2       //@ Requires self != nil
        3       Depth() (res int)
        4       //@ Ensures res >= 0
        5   }
        6
        7   type Node struct {
        8       Key int
        9       left Inode
       10       right Inode
       11   }
       12
       13   type Leaf struct{}
       14
       15   //@ Requires n.left != nil ^ n.right != nil
       16   func (n Node) Depth() (res int) {
       17       return 1 + max(n.left.Depth(), n.right.Depth())
       18   }
       19   //@ Ensures res == 1 + max(n.left.Depth(), n.right.Depth())
       20
       21   //@ Requires true
       22   func (l Leaf) Depth() (res int) {
       23       return 0
       24   }
       25   //@ Ensures res == 0

        • Navigational Indexing: Direct pointer dereferences (n.left, n.right) and structural
          dispatch eliminate magic sentinel index numbers (such as 0 or -1).
        • Data Predicate: Inductive binary search tree validity bBST is bst(n) is defined recursively
          as a VeGo code predicate:

                    //@ Predicate bBST is bst(n)        ::=    (n == nil) v
                                                                ((bBST is bst(n.left) ^
                                                                 bBST is bst(n.right)) ^
                                                                 (n.left == nil v
                                                                 n.left.Key <= n.Key) ^
                                                                 (n.right == nil v
                                                                 n.Key <= n.right.Key))

        • Contract Metrics: Verified via structural induction over pointer height (//@ Measure
          n.Depth()).

6.2   Sorting Stability and Permutation Verification
We verify key-value record sorting (A[i].Key ≤ A[i + 1].Key) across Selection, Insertion, Shell,
Quick, Bitonic, and Permutation Index Sort, enforcing permutation preservation (multiset(A) =
multiset(A′ )).

6.3   Classical Textbook Benchmark Suite: Verification Under --strict Mode
To evaluate VeGo’s verification coverage across standard computer science curricula, we constructed
and formally verified an extensive benchmark archive derived from foundational algorithm textbooks:
   • Cormen, Leiserson, Rivest, and Stein (CLRS) [6]: Dynamic programming (matrix
     chain multiplication, rod cutting), graph search (A∗ and IDA*), disjoint-set union-find,

                                                 11
      multi-precision arithmetic, quicksort, heapsort, and string matching algorithms (Knuth-
      Morris-Pratt kmp matcher.vgo, Rabin-Karp rabin karp.vgo, and Naive String Matcher
      naive matcher.vgo).

    • Kleinberg & Tardos (KT) [15]: Greedy choice invariants, stable matching (Gale-Shapley),
      network flow structures, computational geometry (Graham scan convex hull), and Closest
      Pair of Points (closest points/divide.vgo).

    • Chris Okasaki (PFDS) [20]: Purely Functional Data Structures, including persistent
      red-black trees, splay trees, skip lists, and finger trees (deques and sequences).

    • Donald E. Knuth (TAOCP) [17]: 16 canonical algorithms spanning Volumes 1–4B,
      including Euclid’s GCD and Extended Bézout identity, Topological Sort (Algorithm T), AVL
      tree rebalancing, Heapsort (Algorithm H), Lexicographic Next-Permutation (Algorithm L),
      Gray code generation, Shellsort, and Dancing Links (DLX Algorithm X).

Verification Under --strict Mode. Crucially, all algorithms and data structures across the
CLRS, KT, Okasaki, and Knuth benchmark suites are verified 100% under VeGo’s --strict mode
(vegop --strict). Under --strict verification, every call-site precondition, loop invariant, and
recursive well-founded structural measure (//@ Measure) is statically proved by the native HM[X]
verifier without relying on any dynamic runtime assertion fallbacks.


7     Related Work and Comparative Analysis
Formal program verification has evolved across multiple distinct paradigms, ranging from abstract
modeling languages to interactive proof assistants and automated deductive verifiers. In this section,
we compare and contrast VeGo against prominent existing systems (summarized in Table 1).

Table 1: Comparative analysis of formal methods and verification systems in software education.
System          Target Language       Specification Style    Prover / Backend     Pedagogical Tool
                                                                                  Support
VeGo            Native Go             In-code comments       Native HM[X] over    Native IDE (LSP) +
                                      (//@)                  SSA                  Direct Execution
Dafny [19]      Novel language        First-class keywords   Boogie + Z3 SMT      IDE extension (re-
                                                                                  quires new PL)
Alloy [13]      Relational logic      Abstract model         SAT + Lean/Rocq      Visualizer (abstract
                                                                                  models)
TLA+ [18]       Temporal logic        State machine mod-     TLC + TLAPS          Model checker (code
                                      els                                         abstraction)
Tennent [25]    Pseudocode            Textbook contracts     Paper proofs         Manual proofs (no
                                                                                  prover)
Hoover–
Rudnicki [12]   First-order logic     Natural deduction      Mizar Checker        Interactive     proof
                                                                                  script engine



7.1    Dafny and Intermediate Verification Languages
Leino’s Dafny [19] represents a state-of-the-art automated program verifier. Dafny introduces a novel
imperative-functional research programming language with first-class contract keywords, translating

                                                 12
programs into Boogie intermediate verification language and leveraging Z3 SMT solving. While
Dafny is highly effective for advanced formal methods courses, requiring students to learn a novel
research language creates a dual cognitive burden. In contrast, VeGo embeds specifications directly
into standard Go comments, allowing code to be compiled and executed natively with zero language
friction.

7.2    Relational and Temporal Modeling Systems: Alloy and TLA+
Abstract modeling systems such as Jackson’s Alloy [13] and Lamport’s TLA+ [18] focus on
architectural design rather than direct code verification. Alloy uses a lightweight relational logic to
explore structural properties via SAT solvers and interactive provers (e.g., Lean, Rocq/Coq, and
Isabelle). TLA+ specifies concurrent and distributed systems using temporal logic, relying on the
TLC model checker or TLAPS proof assistant. Both systems operate on abstract mathematical
simplifications of the code rather than the full production source code. VeGo complements these
modeling formalisms by verifying imperative algorithms and data structures written directly in
production Go code.

7.3    Pedagogical Foundations: Tennent and Hoover–Rudnicki
VeGo directly builds upon the educational foundations of Tennent’s Specifying Software [25] and
Hoover & Rudnicki’s CMPUT 272 course notes [12]:

    • Tennent’s Specifying Software: Tennent established the curriculum foundation for in-
      tegrating pre/postconditions and loop invariants into imperative programming. However,
      Tennent’s framework lacked an automated theorem prover, relying exclusively on manual
      paper proofs and runtime ASSERT checks. VeGo provides the automated deductive verification
      engine and LSP IDE integration that Tennent’s methodology lacked.

    • Hoover & Rudnicki’s CMPUT 272: Hoover & Rudnicki introduced undergraduate
      students to formal natural deduction using the Mizar proof checker. Mizar requires students
      to construct explicit interactive proof scripts in a specialized mathematical dialect. VeGo
      automates verification condition generation and HM[X] constraint resolution, allowing students
      to focus on formulating correct contracts, invariants, and termination measures.


8     Concurrency Formalization Roadmap: Goroutines, Channels,
      and Epistemic Logic
A key future phase of VeGo expands verification to concurrent Go code (goroutines and channels).
Building on Owicki & Gries [21], Chandy & Misra’s UNITY [2], and Fagin et al.’s epistemic logic of
knowledge [9], VeGo specifies atomic channel communication (ch ← v) and non-overlapping spatial
separation across concurrent processes.


9     Conclusion
VeGo bridges the gap between theoretical formal methods and practical software development in
computer science education. By embedding Hoare logic contracts into standard Go comments,
students gain hands-on experience specifying, verifying, and executing high-assurance software.



                                                  13
AI Acknowledgment
We acknowledge the assistance of AI coding agents and Large Language Models (LLMs) in the
technical development of the VeGo verifier codebase, SSA desugaring algorithms, and diagnostic
analyzers, as well as in preparing the initial outlines, drafts, and LaTeX formatting of this paper.
All generated code and written content were reviewed, refined, and validated by the human authors.


References
 [1] Andrew W. Appel. SSA is functional programming. ACM SIGPLAN Notices, 33(4):17–20,
     1998.

 [2] K. Mani Chandy and Jayadev Misra. Parallel Program Design: A Foundation. Addison-Wesley,
     1988.

 [3] Adam Chlipala. The expensive fictions of low-level programming languages: AI coding tools
     are facing a major handicap in using popular languages. Technical Blog / Substack, 2026.

 [4] Adam Chlipala. Rewrite all the code, all the time: The coming economics of software engineering
     and an important place for formal methods. Technical Blog / Substack, 2026.

 [5] Adam Chlipala. Subversion-resistance for free from formal verification: Why we don’t need to
     worry about enumerating possible attacks. Technical Blog / Substack, 2026.

 [6] Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. Introduction
     to Algorithms. MIT Press, 3rd edition, 2009.

 [7] Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman, and F. Kenneth Zadeck.
     Efficiently computing static single assignment form and the control dependence graph. ACM
     Transactions on Programming Languages and Systems (TOPLAS), 13(4):451–490, 1991.

 [8] Edsger W. Dijkstra. Guarded commands, nondeterminacy and formal derivation of programs.
     Communications of the ACM, 18(8):453–457, 1975.

 [9] Ronald Fagin, Joseph Y. Halpern, Yoram Moses, and Moshe Y. Vardi. Reasoning About
     Knowledge. MIT Press, 1995.

[10] Robert W. Floyd. Assigning meanings to programs. In Proc. Symposia in Applied Mathematics,
     volume 19, pages 19–32. American Mathematical Society, 1967.

[11] C. A. R. Hoare. An axiomatic basis for computer programming. Communications of the ACM,
     12(10):576–580, 1969.

[12] H. James Hoover and Piotr Rudnicki. CMPUT 272: Formal reasoning and deductive verification
     course notes. Technical report, Department of Computing Science, University of Alberta, 2002.

[13] Daniel Jackson. Software Abstractions: Logic, Language, and Analysis. MIT Press, 2006.

[14] Richard A. Kelsey. A compiling with continuations transformation applicable to SSA form.
     ACM SIGPLAN Notices, 30(3):111–117, 1995.

[15] Jon Kleinberg and Éva Tardos. Algorithm Design. Addison-Wesley, 2006.


                                                14
[16] Martin Kleppmann. Formal methods in the age of AI code generation. Technical report,
     Technical Report / Blog, 2025.

[17] Donald E. Knuth. The Art of Computer Programming, volume Volumes 1–4B. Addison-Wesley,
     1997–2023.

[18] Leslie Lamport. Specifying Systems: The TLA+ Language and Tools for Hardware and Software
     Engineers. Addison-Wesley, 2002.

[19] K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In Proc.
     LPAR-16, volume 6355 of LNCS, pages 348–370. Springer, 2010.

[20] Chris Okasaki. Purely Functional Data Structures. Cambridge University Press, 1998.

[21] Susan Owicki and David Gries. An axiomatic proof technique for parallel programs I. Acta
     Informatica, 6(4):319–340, 1976.

[22] Frank Pfenning. Lecture notes on static single assignment form. Technical report, Carnegie
     Mellon University, Course 15-411: Compiler Design, 2011.

[23] Fabrice Rastello and Florent Bouchez Tichadou, editors. SSA-based Compiler Design. Springer,
     2016.

[24] John C. Reynolds. Theories of Programming Languages. Cambridge University Press, 1998.

[25] R. D. Tennent. Specifying Software: A Curriculum Foundation for Formal Methods. Cambridge
     University Press, 2002.




                                               15
