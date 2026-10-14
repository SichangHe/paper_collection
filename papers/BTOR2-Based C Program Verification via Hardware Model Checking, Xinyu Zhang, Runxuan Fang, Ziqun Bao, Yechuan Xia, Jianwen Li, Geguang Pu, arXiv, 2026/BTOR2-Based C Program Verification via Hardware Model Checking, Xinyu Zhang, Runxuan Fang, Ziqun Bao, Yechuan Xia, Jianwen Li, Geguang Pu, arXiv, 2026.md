                                                     BTOR2-Based C Program Verification via
                                                          Hardware Model Checking
                                                         Xinyu Zhang, Runxuan Fang, Ziqun Bao, Yechuan Xia, Jianwen Li* , and Geguang Pu
                                                                                           East China Normal University
                                                                                 {westtide,rxfang,52285902029}@stu.ecnu.edu.cn
                                                                            {xiaozi465,lijwen2748}@gmail.com, ggpu@sei.ecnu.edu.cn


                                            Abstract—Program verification tools often rely on specific        symbolic execution [12], abstract interpretation [13], bounded
                                         intermediate representations and analysis backends, limiting         model checking, and Horn-clause solving [14]. However, these
                                         the reuse of verification algorithms and model checkers across       representations are not the task formats directly consumed
                                         frameworks. In contrast, hardware model checking has developed
                                         a mature backend ecosystem, where standard formats such as           by HWMCC-style hardware model checkers. The issue is
                                         BTOR2 support reusable algorithms for counterexample search          therefore not the absence of software-verification IRs, but
                                         and inductive safety proving. Applying these capabilities to C       the lack of a semantic encoding layer from assertion-based
                                         requires translating assertion-based programs into transition        C verification tasks to hardware model-checking transition
                                         systems that hardware model checkers can directly process.           systems.
                                            We present C2Btor, a method for encoding such verification
                                         tasks into BTOR2 models. C2Btor uses a program counter to               This paper addresses this gap by using BTOR2 as
arXiv:2607.17622v1 [cs.SE] 20 Jul 2026




                                         capture control transfers, represents data states and memory         the primary target representation. The reason is not that
                                         objects with bit-vectors and arrays, and maps assumptions            BTOR2 replaces lower-level formats such as AIGER, but that
                                         and assertion checks into BTOR2 constraints and bad-state            it provides a suitable interface for constructing program-level
                                         properties.                                                          transition systems before optional lowering to bit-level models.
                                            We evaluate C2Btor on SV-COMP C ReachSafety benchmarks
                                         and a curated assertion-category benchmark suite, comparing it
                                                                                                              BTOR2 preserves word-level bit-vector and array terms, and
                                         with representative program verification tools. C2Btor correctly     provides native constructs for states, transitions, constraints,
                                         solves 263 tasks, 101 more than CBMC configured with bounded         and bad-state properties. These features allow the encoding to
                                         model checking, and is especially effective on bit-vector bench-     keep finite-state program data, control-flow locations, assump-
                                         marks, where it solves 75.5% of the tasks with no wrong verdicts.    tions, and assertion failures explicit in the generated model.
                                         These results show that the BTOR2 route allows C program
                                         verification to benefit from advances in hardware model-checking
                                                                                                              AIGER remains useful as a lower-level target for the subset
                                         backends, expanding the available capability for counterexample      of generated models that can be bit-blasted and discharged by
                                         search, inductive safety proving, and word-level transition-system   AIGER-based engines.
                                         reasoning.                                                              We therefore propose C2Btor, a framework that trans-
                                            Index Terms—Program Verification, BTOR2, Model Checking,          lates C programs into BTOR2 transition systems and veri-
                                         Intermediate Representation
                                                                                                              fies the generated tasks using hardware model checkers. To
                                                                                                              separate C frontend processing from BTOR2-specific semantic
                                                                  I. Introduction
                                                                                                              encoding, C2Btor follows a three-stage route.
                                            Hardware model checking has developed a mature ecosys-               1) It uses the parser of CBMC [15] to lower the input C
                                         tem of automated backends for Reachability-safety analysis.                 program into Goto-IR1 , a verification-oriented IR with
                                         Through competitions such as the Hardware Model Checking                    explicit control flow and type information.
                                         Competition (HWMCC) [1], formats such as AIGER [2] and                  2) C2Btor encodes the Goto-IR program into a BTOR2
                                         BTOR2 [3] have become stable interfaces, enabling algorithms                transition system, including program-counter-based con-
                                         such as Bounded Model Checking (BMC) [4], k-Induction [5],                  trol flow, state and next expressions for data updates,
                                         and IC3/PDR [6, 7] to be implemented and reused over                        object-level pointer modeling, and the mapping from
                                         common inputs. Although these techniques were developed                     assumptions and assertions to constraint and bad nodes.
                                         mainly for hardware transition systems, C program verification          3) The generated BTOR2 task is discharged by hardware
                                         has a closely related safety objective: a program is unsafe if              model-checking backends for counterexample search and
                                         some feasible execution reaches an assertion failure, and safe              safety proving, rather than by CBMC’s bounded-model-
                                         otherwise. This raises a natural question: Can C reachability-              checking backend.
                                         safety tasks benefit from the mature automated backends              The main contributions of this paper are as follows:
                                         developed in hardware model checking?
                                                                                                                 • A C-to-BTOR2 encoding for a well-defined verification
                                            C program verification already has mature intermediate
                                                                                                                    fragment. We propose a set of encoding rules that trans-
                                         representations and tool ecosystems, as reflected in SV-
                                                                                                                    late assertion-based C verification tasks, via Goto-IR, into
                                         COMP [8]. Representations such as LLVM-IR [9], Constrained
                                         Horn Clauses (CHCs) [10], and SMT-LIB [11] have supported              1 https://diffblue.github.io/cbmc/group__goto-programs.html
     BTOR2 transition systems. The encoding uses an explicit           These tools differ in both backend algorithms and inter-
     program counter to model control flow, represents data         mediate representations. Goto-IR, LLVM-style representations,
     states and memory objects with bit-vectors and arrays,         SMT encodings, and CHCs expose control flow, data state,
     and maps assumptions and assertions uniformly to con-          memory, and verification conditions in different ways. This
     straint and bad nodes. This formulation makes explicit         paper is complementary: instead of building another C verifier
     the C fragment naturally supported by the BTOR2-based          over a software IR, we study whether assertion-based C tasks
     route, including finite-state, bit-vector-friendly programs    can be encoded into a standard hardware model-checking
     with structured control flow, nondeterministic inputs,         format and solved by hardware backends.
     fixed-width integer operations, local arrays, and restricted
                                                                    B. Hardware Model Checking, AIGER, and BTOR2
     object-level pointer relations.
   • An end-to-end framework for reusing hardware model                Hardware model checking is reachability analysis over tran-
     checking backends. We develop C2Btor, a tool frame-            sition systems with initial conditions, transition relations, and
     work that connects C reachability-safety tasks, the pro-       bad states. BMC [4] is effective for bounded counterexample
     posed BTOR2 encoding, and existing hardware model-             search, while k-Induction [5] and IC3/PDR [6, 7] prove un-
     checking backends. Given an assertion-based C program,         bounded safety through inductive reasoning. Recent backends
     C2Btor generates backend-consumable BTOR2 models               also include CAR-style reachability [24, 25] and optimized
     and enables different backend algorithms to be applied to      IC3/PDR variants [26].
     the same transition-system representation for counterex-          Hardware model checking also benefits from common task
     ample search and safety proving.                               formats. AIGER [2] is a compact bit-level representation used
   • Empirical findings on complementarity and backend              by model checkers such as SimpleCAR [27]. BTOR2 [3] is
     algorithm behavior. We evaluate C2Btor on SV-COMP              a word-level transition-system format over bit-vectors, arrays,
     C ReachSafety benchmarks and a curated assertion-              and state updates; it preserves word-level structure before bit-
     category dataset, showing that the BTOR2-based route           blasting [28], and rIC3 [29] can process BTOR2 directly. We
     can solve tasks not covered by bounded, SMT-based,             use BTOR2 as the primary C-encoding target and AIGER as
     or CHC-based software verifiers. We further analyze the        a lower-level target for the convertible subset.
     generated model-checking tasks on 390 BTOR2 models             C. Bridging Hardware and Software Analysis
     and 305 converted AIGER models, showing that backend
     algorithms play distinct roles in counterexample search           Hardware and software verification start from different
     and safety proving. These findings indicate that encoding      artifacts, but many tasks share the same transition-system core:
     C verification tasks into BTOR2 allows program verifica-       initial states, state updates, and error states. Existing work
     tion to benefit from advances in HWMCC-style backend           has explored the hardware-to-software direction: Btor2C [30]
     algorithms, thereby expanding the available capability for     translates BTOR2 circuits into C programs so that hardware
     bug finding and safety proving.                                models can be analyzed by software verifiers.
                                                                       Our work studies the reverse direction: translating C
   The remainder of this paper is organized as follows. Sec-        reachability-safety tasks into BTOR2 transition systems. Com-
tion II discusses related work. Section III introduces BTOR2,       pared with Btor2C, we must recover control flow, data updates,
Goto-IR, and the formulation of ReachSafety tasks in hardware       pointer operations, assumptions, and assertion failures from C
model checking. Section IV presents the proposed encoding           and encode them into a hardware model-checking format.
method, including the overall workflow, key translation rules,         By targeting BTOR2, our encoding turns C reachability-
and semantic boundaries. Section V reports the experimental         safety tasks into word-level transition systems consumed by
design and results. Section VI discusses applicability, limita-     hardware backends, allowing program verification to benefit
tions, and future work, and concludes the paper.                    from advances in counterexample search and safety proving.
                       II. Related Work                                                    III. Background
A. C Program Verification                                           A. Overview of C2Btor
   C program verification has been extensively studied, and            Figure 1 shows the pipeline of C2Btor. The input is a C
SV-COMP has helped establish a mature ecosystem of tools            program with assertions. C2Btor reuses the CBMC frontend
and benchmarks [8]. The ReachSafety category spans several          to parse, type-check, and normalize the program into Goto-IR.
paradigms: CBMC [15] and ESBMC [16] perform bit-precise             We use the following notation throughout the paper:
bounded model checking; Ultimate Automizer [17] uses in-                              F              E
                                                                                  C −−−→ GGotoIR −−C2Btor
                                                                                     CBMC
                                                                                                   −−→ MBTOR2 .
terpolation and refinement; CPAchecker [18] and Bubaak [19]
reflect configurable and portfolio verification; and AISE [20],     Goto-IR lowers structured C control flow into explicit program
Symbiotic [21], and VeriAbs [13] combine abstraction, sym-          locations and instructions. C2Btor then encodes the Goto-
bolic execution, and slicing. CHC-based tools such as Eldarica      IR program into a BTOR2 transition system with a set of
and TriCera [22, 23] reduce safety proving to invariant infer-      encoding rules. The generated BTOR2 model can then be
ence and Horn solving [14].                                         analyzed by different model-checking backends, such as BMC,
                         Program and Goto-IR                                                                      BTOR2 Model                                                                          Hardware Model Checking
            C program                                           Goto-IR
                                                                                                                       Model                                                                      BTOR2
     assume(C)                                            DECL                                                                                                                                                                     Reach(¬P)?
     for ( ... ; ... ; ... ) {               1            ASSIGN                  2                    M = (X, Init, Next, B, C)                                                          3       Model
                                                          L1: IF !(cond) GOTO L2
       ...                                                        body
     }                                                            Update(cond)                  X         Init            Next                 B                         C
                                                                                                                                                                                                                Multiple
     assert(P)                           Parser              GOTO L1             Model
                                                          L2: …                                                                                                                         Verify                Model Checkers


    A Control                                                  ¬cond                     A Control                                                     pc
                       L1             cond                                  L2                                 next(pc) =
       Flow                                         body                                     Fow in                                       cond                      ¬cond
                                                               GOTO                                            ite(cond, t, e)
                                      GOTO                                                   BTOR2                                             t                         e
                                                                                                                                                                                                                 k-
                                                                                                                                                                                                 BMC          induction
                                                                                                                                                                                                                            IC3/PDR      Others
                                                                                             Data
    B Data                                                                               B
                                 Explicit          ARRAY            Native                   and                   BV             ARRAY                       Native
       and                        Types                                                                            Sort            Sort                      Operators
                                                    Sort           Operators                 Instructions in
       Instructions
                                                                                             BTOR2
                                                                                                                                                                                                                     Results
                                                                                                                                                   objects
    C Pointers                                                                           C Pointers
                                                                                                                                 obj 0         obj 1         ...             obj n
       and                        0      1       ......    0   1       64 bit                and
       Memory                                                                                Memory P=<object, offset>           offset

                            *(p+i)=*(p + cast(i, signedbv[64]))                              in BTOR2                            0         1           2           ...         63




    D Verification                                                                       D Verification                                                                                          UNSAFE               SAFE         UNKNOWN
                                         ASSERT P                                                                           ASSERT ⇒ BAD
       Semantics                                                                             Semantics                                                                                            SAT with         UNSAT with
                                                                                             in BTOR2                                                                                             a witness        a certificate
                                                                                                                     ASSUME ⇒ CONSTRAINT
                                        ASSUME C



                                                                                         Fig. 1: Overview of C2Btor.


k-Induction, and IC3/PDR. The backend result is interpreted as                                                        conversions, expression evaluation rules, object layout, pointer
a program-verification result: SAT means Unsafe and UNSAT                                                             operations, and library-dependent constructs. To avoid reim-
means Safe, and an inconclusive run is reported as unknown.                                                           plementing a full C frontend, C2Btor uses the Goto-IR pro-
   Therefore, Section III-B explains the connection between                                                           duced by the CBMC frontend as its input representation. We
program verification and model checking, and Section III-C                                                            later write GGotoIR simply as G and abstract it as
introduces the Goto-IR representation. Section III-D summa-
rizes the BTOR2 concepts used in this work.                                                                                                             G = (L, Σ, Objects, Instructs, Verif).

B. From Program Verification to Model Checking                                                                        Here,
                                                                                                                                                                                      L = {ℓ1 , ℓ2 , . . . , ℓn }
   In a C program, an assertion expresses a condition that must
hold whenever execution reaches the corresponding program                                                             is the set of Goto-IR locations, where each ℓi is the location
point. SV-COMP ReachSafety tasks use the same idea, often                                                             of one Goto-IR instruction. Σ is the static symbol table with
by requiring that an error function such as reach_error is                                                            type information. For example,
unreachable [8].
   A transition system provides the target form for this reach-                                                                                            Σ = {int x : signedbv[64],
ability problem. It contains state variables, initial conditions,                                                                                                                    int a[2] : signedbv[64][2],
and transition updates. Assertions are represented as bad-state                                                                                                                      int *p : signedbv[64]}.
predicates, and assumptions restrict the feasible transitions.
If a bad state is reachable, the program is unsafe and the                                                            Objects is the collection of program state objects. A valuation
backend may return a counterexample. If all bad states are                                                            of these objects describes the dynamic program state:
proven unreachable, the program is safe under the generated
                                                                                                                                                                                      ν ∈ ValΣ (Objects).
model; otherwise the result is reported as unknown or timeout.
   This is the only model-checking interface required by                                                              Thus, at location ℓi , a Goto-IR state is
C2Btor. The encoder translates Goto-IR control and data up-
dates into BTOR2 state and next nodes, and maps verification                                                                                                             (ℓi , ν) ∈ L × ValΣ (Objects).
semantics to bad and constraint nodes. The resulting BTOR2
task can then be analyzed by hardware model-checking back-                                                               Instructs contains the lowered Goto-IR instructions. High-
ends using BMC, k-induction, or IC3/PDR.                                                                              level C control flow is represented by assignments and explicit
                                                                                                                      jumps.
C. Goto-IR as a Frontend Representation                                                                               Example 1. Control-Flow Lowering. A conditional branch
   Generating a transition system directly from C source code                                                         instruction if (A) { B } else { C } is lowered to a con-
is complicated. C contains structured control flow, implicit                                                          ditional goto and two explicit branch blocks:
                                                                    This example is schematic: names such as pc, i, and sum stand
L1: if !A goto L_else
L2: B                                                               for previously defined node identifiers. The important point is
L3: goto L_end                                                      that every computed value is a numbered node, and later lines
L_else: C
L_end: ...                                                          build larger expressions by referring to earlier identifiers.
                                                                       The BTOR2 keywords can be grouped as follows.
A loop for (I; A; U) { B } is lowered to a condition
check and a back edge:                                              1) Line and node definitions. Each line has a unique id
L1: I                                                               and defines either a sort or a node. Node lines include
L2: if !A goto L_end
L3: B                                                               constants such as constd, persistent variables such as state,
L4: U                                                               nondeterministic inputs such as input, and expression nodes
L5: goto L2
L_end: ...                                                          such as eq, add, or ite.
                                                                    2) Transition symbols. state, init, and next define the transi-
   Goto-IR represents pointer operations as explicit typed
                                                                    tion system. state declares a variable preserved across steps,
expressions. Pointer reads and writes keep the dereference
                                                                    init constrains its initial value, and next defines its value in the
operation visible, while pointer arithmetic and casts expose the
                                                                    next step. In encodings produced by C2Btor, ite is commonly
bit-vector expression used to compute the accessed address.
                                                                    used inside next expressions to encode guarded control-flow
Example 2. Pointer Expressions. A pointer read such as r            and data updates.
= *(p + i) is represented as:
                                                                    3) Data symbols. Data is typed by sort lines. The main
              r := ∗(p + cast(i, signedbv[64])).                    sorts used here are bitvec and array. Bit-vectors represent
                                                                    integers, Booleans, program locations, object identifiers, and
Similarly a pointer write *(p + i) = v can be:
                                                                    offsets; arrays represent indexed program objects or memory-
              ∗(p + cast(i, signedbv[64])) := v.                    like objects. Constants such as const and constd provide
                                                                    typed literal values.
   Verif contains verification-relevant instructions such as
                                                                    4) Operator symbols. BTOR2 provides many typed operators;
assert(p) and assume(c). Assertions define bad-state condi-
                                                                    the complete set is given in the BTOR2 specification [3].
tions, while assumptions define path constraints. In summary,
                                                                    This paper mainly uses Boolean and bit-vector operators such
Goto-IR gives C2Btor an explicit, typed, and verification-
                                                                    as not, and, eq, slt, arithmetic operators such as add, sub,
oriented program representation; the rules for translating this
                                                                    mul, udiv, conditional ite, and array read/write. Each operator
representation into BTOR2 are presented in Section IV.
                                                                    produces another typed node.
D. BTOR2 Transition Systems                                         5) Verification symbols. bad defines an error-state predicate,
   BTOR2 is a word-level transition-system format for model         and constraint restricts feasible traces. They correspond to B
checking [3]. It is not a programming language with sequential      and C in MBTOR2 . A backend checks whether some bad node
statements. Instead, a BTOR2 file is a numbered list of typed       can become true along a trace satisfying the init, next, and
definitions. Each line starts with a unique identifier, and         constraint lines.
later lines refer to earlier identifiers to build expressions and     In summary, BTOR2 provides the target vocabulary for
transition-system components. Thus, a BTOR2 model is a              numbered expressions, states, data, operations, and reachability
graph of sorts, state nodes, input nodes, expression nodes,         properties. Section IV explains how C2Btor performs this
and property nodes. We write the generated BTOR2 transition         encoding for control flow, data state, pointer-related objects,
system as                                                           and verification assertions.
                 MBTOR2 = (X, Init, Next, B, C).
Here, X is the set of BTOR2 state nodes, Init gives their initial                           IV. Methodology
values or constraints, and Next gives their synchronous next-
state updates. B is the set of bad-state predicates, and C is the   A. Overview
set of path constraints.                                               The goal of this methodology is not to redefine C semantics.
   The following sketch shows the style of BTOR2 lines:             Instead, C2Btor encodes the control flow, objects, instructions,
1 sort bitvec 32
2 sort bitvec 64
                                                                    and verification semantics already made explicit in Goto-IR
29 sort bitvec 1                                                    into a BTOR2 transition system. Given the Goto-IR object
36 constd 1 4          ; integer constant 4
54 eq 29 pc L_cond     ; pc == loop condition
                                                                    G = (L, Σ, Objects, Instructs, Verif) defined in Section III-C,
55 slt 29 i 36         ; i < 4                                      we write O = Objects, I = Instructs, and V = Verif for
56 not 29 55           ; !(i < 4)
57 and 29 54 56        ; exit guard
                                                                    compact notation. The overall mapping is
59 and 29 54 55        ; body guard
65 add 2 p offset      ; p + offset
101 ite 1 guard val old; guarded read/update
                                                                          G = (L, Σ, O, I, V ) → M = (X, Init, Next, B, C).
141 next 1 sum 140     ; next(sum)
200 bad 57             ; reachable error                            We organize the encoding rules by the following aspects:
     Algorithm 1: Symbolic workflow of C2Btor                                 and ti is the encoded pc value of that target. The expression
   Input: G = (L, Σ, O, I, V ), where L = {ℓ1 , . . . , ℓn }                  E(ci ) is the BTOR2 encoding of the guard, and pchalt is the
   Output: M = (X, Init, Next, B, C)                                          terminal location. An unconditional GOTO is treated as the same
 1 foreach ℓi ∈ L do
                                                                              rule with a true guard. The local successor for a conditional
 2     nodei ← bv64 (i); ati ← (pc = nodei )         // control code
         and guard                                                            branch is
 3 X ← {pc} ∪ Xdata (Σ, O) ∪ Xmem (Σ, O) ∪ Xaux      // BTOR2                                    δi = ite(E(ci ), ti , i + 1).
     states
 4 Init ← Initpc ∪ Initdata ∪ Initmem       // initial states                 BTOR2 requires one next node for pc, so all local control-flow
 5 foreach x ∈ X do                                                           rules are chained into one expression:
 6      Ux ← ∅                             // guarded updates
 7 B ← ∅; C ← ∅                                                                   next(pc) = ite(pc = 0, δ0 , ite(pc = 1, δ1 , . . . , pchalt )).
 8 foreach ℓi ∈ L do
 9     ιi ← I[ℓi ]                  // instruction at location ℓi             The same pattern is used later for data states: C2Btor collects
10     (∆i , δi , Bi , Ci ) ← Step(ιi , ati , Σ, O) // local encoding         guarded candidate updates and folds them into a single one,
11     Upc ← Upc ∪ {(ati , δi )}                // control-flow update
12     foreach (x, g, v) ∈ ∆i do                                                          next(x) = ite(g1 , v1 , ite(g2 , v2 , . . . , x)).
13          Ux ← Ux ∪ {(g, v)}               // data or memory update
14        B ← B ∪ B i ; C ← C ∪ Ci                  // properties and         The final default value preserves the current state when no
           constraints                                                        guard is enabled.
15    foreach x ∈ X do                                                           Loops are not unrolled by C2Btor. Back edges in Goto-
16        Next(x) ← Fold(Ux , default(x))       // one next per state         IR are encoded directly in next(pc), so a source-level loop
17    return M = (X, Init, Next, B, C)                                        becomes a cycle in the generated BTOR2 transition system.
                                                                              Whether this cycle is explored using bounded model checking,
                                                                              k-induction, IC3/PDR, or another hardware model-checking
 Aspect                    Goto-IR source                BTOR2 target         algorithm is a responsibility of the backend. Hence, C2Btor
 Control flow              L, GOTO, RETURN               pc, next(pc)
                                                                              does not produce a fixed-depth C-to-BMC formula; it pro-
 Data state                Σ, O                          X, Init              duces a transition system that can be consumed by multiple
 Instruction updates       I                             Next                 unbounded or bounded hardware model checkers.
 Pointers and memory       Oaddr , pointer expressions   Xmem , read, write
 Verification              V                             B, C                 C. Data State
                                                                                 Data-state rules decide which BTOR2 states are created for
Encoding workflow. Algorithm 1 shows the overall encoding                     program objects and which initial values are placed in Init.
workflow. Its role is to connect the categories above, not to                 For each Goto-IR type τ , let W (τ ) be its bit-width under the
expose implementation details.                                                frontend’s target-machine configuration; in practice, this width
                                                                              is usually 32 or 64 bits for machine integer and pointer-related
B. Control-Flow Encoding
                                                                              types.
   The program counter pc is a 64-bit bit-vector state. A
                                                                              1) Scalars and constants. Boolean and integer-like objects,
BTOR2 line such as 2 sort bitvec 64 declares the 64-bit
                                                                              including char, short, int, long, unsigned variants, and
sort; the actual program counter is a state node that uses this
                                                                              enum objects, are represented as bit-vector states:
sort. The value stored in pc is not a BTOR2 line id. Instead,
pc = i means that the current transition executes the Goto-                                      x:τ       7→     x : BV(W (τ )).
IR location ℓi . For compact formulas below, atℓi abbreviates
                                                                              For example, in our encoding, bool is encoded as BV(1), while
pc = i.
                                                                              int and unsigned int are encoded as BV(64). Signedness does
   The two BTOR2 keywords used most often in this encoding
                                                                              not change the state sort. A signed integer and an unsigned
are next and ite. A next node defines the value of a state in
                                                                              integer of the same width have the same state type; signedness
the next transition step. An expression ite(c, a, b) means “if c
                                                                              only selects the operator used later by an instruction. Constants
then a else b”. A next defines how a state changes, while ite
                                                                              are generated with the width required by their expression
is only a way to build the right-hand side of a next definition.
                                                                              context.
   Let Ii be the Goto-IR instruction at location ℓi . The next
value of pc has four common cases:                                            2) Arrays. For an array object a : τ [N ], C2Btor uses
                                                                             either scalarization or a BTOR2 array state. A small statically
         
          i + 1, Ii is sequential,                                           bounded array can be scalarized into element states:
         
         t ,       Ii = GOTO(ci , ℓti ) ∧ E(ci ),                                    a 7→ {a0 , a1 , . . . , aN −1 },
  pc′ =
             i                                                                                                              ai : BV(W (τ )).
                                                      (pc = i)
         
          i  + 1,  Ii = GOTO(ci , ℓti ) ∧ ¬E(ci ),
         
                                                                             For larger arrays, C2Btor uses a native BTOR2 array state:
           pchalt , Ii ∈ {RETURN, END}.
                                                                                              a : τ [N ]    7→     a : Array(N, τ ).
Here, i+1 denotes the next executable location in the Goto-IR
sequence, Ii = GOTO(ci , ℓti ) denotes a conditional Goto-IR                  Here, Array(N, τ ) is a paper-level shorthand: N denotes the
branch at location ℓi , ci is its guard, ℓti is its target location,          index range of the array and τ denotes the element type.
In BTOR2, this state is implemented by a native array sort            and array writes may add extra guards, such as an index
with a bit-vector index sort and an element sort of width             equality or an object-identifier check.
W (τ ). BTOR2 read returns an element, and write returns              4) Lowered branches and loops. Conditional control flow has
an updated array state. Scalarization avoids array reasoning          already been lowered by Goto-IR. A source if-else becomes
for small arrays, whereas native array states avoid expanding         conditional GOTO instructions, and for/while loops become
large arrays into many state variables.                               the same conditional branches with back edges. Their effect
3) Structures and layout. Structures are represented by field         on pc is encoded by the control-flow rules in Section IV-B;
projection. For example, struct S { int x; unsigned                   they are not separate high-level C constructs in the BTOR2
int y; }; struct S s; is encoded as one object-level                  model.
record whose fields are stored separately:
                                                                      E. Pointers and Memory
           s 7→ hx : sx , y : sy i,
         s.x 7→ sx : BV(64),          s.y 7→ sy : BV(64).                C2Btor encodes memory as an object-level memory model
                                                                      instead of one flat byte-addressed array, and each statically
The first line records that s is still one structure object; the      resolved addressable object has an object id, and each pointer
second line shows the BTOR2 state created for each field. Ad-         is interpreted as an object-offset pair. The object id selects the
dressable structures and arrays also receive layout information,      logical object; the offset is the byte position inside that object.
such as object identifiers, field offsets, and element sizes. That
                                                                      1) Addressable objects. Memory is stored as a finite object
layout is used by the pointer rules, but it does not require every
                                                                      map built from the symbol table:
object to be represented as a byte-addressed memory array.
4) Pointer values. Pointer-typed variables are also stored as                        M = {id(o) 7→ repr(o) | o ∈ Oaddr }.
64-bit bit-vector states. This rule only says how the pointer
value is stored. Pointer arithmetic, dereference reads, writes,       Here, Oaddr contains the addressable objects selected for the
and linked data structures are handled by the object-level            encoding. Their backing representations are the data states
pointer model in Section IV-E.                                        introduced earlier:
5) Initialization. Static zero initialization and explicit initial-    scalar x     7→       BV state,
izers are encoded in Init. Verification nondeterminism is not           array a      7 →     scalarized elements or a BTOR2 array state,
initialization: a call such as __VERIFIER_nondet_int() is               struct s       7 →   projected field states.
an instruction-level input and is captured in Next.                   Only objects that can be statically resolved become backing
D. Instruction Encoding                                               objects for pointer accesses.
   Instruction rules describe how Goto-IR expressions and             2) Pointer representation. A pointer value is modeled as
instructions generate BTOR2 operators and next-state updates.
                                                                                                p = hobj(p), off(p)i.
1) Arithmetic expressions. Arithmetic expressions are en-
coded using native BTOR2 bit-vector operators. For example,           For example,
addition, subtraction, multiplication, division, and remainder
become the corresponding word-level operators of the required         &a[i] = hid(a), i·sizeof(int)i,           &s.g = hid(s), fieldoff(g)i.
width. Signedness selects the signed or unsigned variant where        The pointer type comes from the Goto-IR expression type and
BTOR2 distinguishes them.                                             the symbol table. Layout information comes from the target
2) Bitwise, logical, and cast expressions. Bitwise operations,        configuration, including sizeof, element size, field offset,
logical operations, comparisons, shifts, and conditional expres-      alignment, and object bounds. Thus p + 1 preserves the object
sions are also encoded with native BTOR2 operators, such as           id and advances the offset by the size of the pointed-to type:
and, or, not, eq, slt, shifts, and ite. Casts are encoded as
truncation, zero extension, sign extension, or reinterpretation                    p + i = hobj(p), off(p) + i · sizeof(∗p)i.
at the required bit-width.
                                                                      3) Dereference by object dispatch. A dereference is resolved
3) Assignments. For a simple assignment at location ℓi ,
                                                                      by dispatching on the object id and then using the offset inside
written Ii : x := e, C2Btor encodes the right-hand side as
                                                                      the selected backing object:
E(e) and adds one guarded update to Tx :
                                                                                        
                 Tx ← Tx ∪ {(pc = i, E(e))}.                                            
                                                                                        accessa (off(p), τ ), obj(p) = id(a),
                                                                          deref(p, τ ) = accesss (off(p), τ ), obj(p) = id(s),
If this is the only assignment to x, the resulting update is                            
                                                                                        
                                                                                          unsupported,           otherwise.
                next(x) = ite(pc = i, E(e), x).
                                                                      For a read, access returns the selected scalar, array element,
If several locations assign to x, all candidate updates are           or structure field. For a write, the same object guard is used
combined by the folded form in Equation IV-B. Pointer writes          to update the corresponding backing state.
4) Validity and unsupported cases. Pointer safety is ex-                       1              6               3
                                                                                                              1                     24
                                                                                                                                                                 5
                                                                                                                                                                 2
                                                                                                                                                                             1
                                                                                                                                                                                          25           FAIL

pressed by object-level predicates:                                   700
                                                                              93                                            85      46
                                                                                                                                                   162                                                 OOM

                              ∨ (                                                            269
                                                                                                                                                                           324
                                                                                                                                                                                                       UNKNOWN



     valid(p, τ ) ≡ p 6= 0 ∧
                                                                      600                                                                                                                              OOT
                                    obj(p) = id(o)                                                           413
                                                                                                                                                   148
                                                                                                                                                                430                                    FT
                                                                              306                                                   377                                                  465
                                                                      500                                                                                                                              TF
                              o∈T (p)                                                                                       430
                                                                                                                                                                                                       FF
                                                                                                                                                                            33

                     ∧ aligned(off(p), τ )
                                                                                                                                                                                 FT=8
                                                                      400
                                                                                     FT=3                                                                                        TF=2                  TT

                                                           )                                 278              5                                                             82
                                                                                     TF=6                                                          215
                                                                              59                                   TF=32

                     ∧ off(p) + sizeof(τ ) ≤u sizeof(o) .             300

                                                                                                             126                    163
                                                                                                                                                                118                            TF=20

                                                                                                   FT=2                                             49
                                                                      200
                                                                                              49                            128                                                          122
The predicate checks non-nullness, object match, alignment,                   305
                                                                                                                                    82
                                                                                                                                          TF=1                             323

                                                                                                                                                                218
and object bounds. When Goto-IR contains such checks as               100
                                                                                             169             193
                                                                                                                            130
                                                                                                                                    80
                                                                                                                                                   199
                                                                                                                                                                                         141


assertions or equivalent guards, their violations are translated       0
                                                                              Aise          Bubaak        CPAchecker       ESBMC   CBMC          Symbiotic   Uautomizer   Veriabs       C2Btor

into BTOR2 bad predicates. If the target object, offset, or
access type cannot be statically represented by the object-level      Fig. 2: Comparison of C2Btor with other program verifiers
model, C2Btor rejects the translation instead of emitting an          on SV-COMP benchmarks.
unsound approximation.
   In short, pointers are represented as object-offset pairs rather
than concrete byte addresses. Dereferences are resolved by                  RQ3: How do hardware model-checking algorithms per-
dispatching on the object id to finite typed backing objects,                    form on the verification tasks generated by C2Btor?
while the offset, access type, alignment, and object bounds                 RQ4: What properties and C semantics are currently cov-
determine the precise read or write location.                                    ered by C2Btor, and where are its verification bound-
                                                                                 aries?
F. Verification Properties
                                                                      B. Experimental Environment
   C2Btor encodes verification as reachability over bad pred-
icates and path constraints. A Goto assertion ASSERT cℓ at               All experiments were conducted on the same server
location ℓ becomes a location-guarded bad predicate:                  equipped with an Intel Xeon Gold 6132 CPU at 2.60 GHz, 28
                                                                      cores, and 96 GB memory, running CentOS 7 Core on x86_64.
                       bℓ = atℓ ∧ ¬E(cℓ ).                            Each verification task was limited to 900 s and 16 GB. C2Btor
                                                                      is developed based on CBMC 6.7.1. The implementation
Thus an assertion fails only when execution reaches ℓ and the         is available in the artifact repository.2 We implemented our
encoded condition is false. A Goto assumption ASSUME cℓ is            experimental scripts for execution and resource control, while
not an error; it is a path filter encoded as a constraint:            keeping the result classification consistent with BenchExec-
                      χℓ = (¬atℓ ) ∨ E(cℓ ).                          style.3 Each tool result is normalized as follows:
                                                                         • Correct verdicts. TT denotes a True verdict on a true
Multiple assertions and assumptions are collected into B and                task, and FF denotes a False verdict on a false task. The
C, and explicit runtime checks or error locations are handled               correct-verdict rate is (T T + F F )/N .
by the same bad-predicate rule when they already appear.                 • Wrong verdicts. TF is a false alarm, namely a False

G. Summary                                                                  verdict on a true task; FT is a missed bug, namely a
                                                                            True verdict on a false task. The wrong-verdict rate is
  The encoding maintains one consistent chain of symbols                    (T F + F T )/N .
across the chapter:                                                      • Inconclusive outcomes. Unknown, OOT, and OOM

   ℓi   7→    nodei = bv64 (i)     7→    ati = (pc = nodei ).               mean that the tool does not return a Boolean verdict
                                                                            within the configured resource limit. The inconclusive
Control-flow rules populate Upc , instruction rules populate the            rate is (Unknown + OOT + OOM )/N .
update lists Ux for data and memory states, and verification             • Abnormal outcomes. FAIL denotes an unsupported-
rules populate B and C. Each update list is folded into one                 input failure before solving, while ERR denotes a crash.
BTOR2 next expression. The result is the BTOR2 transition                   These outcomes are reported separately when needed
system M = (X, Init, Next, B, C).                                           because they usually reflect semantic coverage boundaries
                                                                            or implementation robustness problems rather than ordi-
                         V. Evaluation                                      nary backend verdicts.
A. Experimental Design
                                                                      C. RQ1: Verification Capability on SV-COMP Benchmarks
  Our experiments focus on four research questions:
                                                                        Dataset. To evaluate verification capability on standard
  RQ1: Can C2Btor perform end-to-end verification on sup-
                                                                      benchmarks, we use 773 C ReachSafety tasks from SV-COMP
        ported standard C verification tasks?
                                                                      2026, covering Array, BV, and Loop programs.
  RQ2: Does the C-to-BTOR2 representation route pro-
        vide complementary solving capability to existing                   2 https://anonymous.4open.science

        software-verification routes?                                       3 https://github.com/sosy-lab/benchexec
                                                                                                    is strongest on BV tasks, where it correctly solves 75.5%
                                                                                        FAIL
500           61                 64
                                                        101
                                                                             65
                                                                                        OOM         of the benchmarks, reports no wrong verdicts, and is second
                                 46
                                                                                        UNKNOWN     only to CPAchecker. This advantage is not captured by overall
                                                         14                             OOT
400
              143
                                                                                        FT
                                                                                                    solved rate alone: VeriAbs has the highest overall solved rate
                                                                             197
                                128
                                                                                        TF          in Table I, but solves no BV task in this experiment. The
                                                                                        FF
300
                                                        239
                                                                                        TT
                                                                                                    contrast reflects different method strengths. VeriAbs mainly
              107                48
                                                                             37                     extends bounded model checking with abstract acceleration
200                              75
                                                                             72                     and k-induction for large or unknown loop bounds, whereas
                                                                 FT=3
                                 29                      43                                         BV programs match the BTOR2 route more directly: both
100           214
                                                         54
                                                                             154
                                                                                                    BTOR2 and hardware model checkers natively support fixed-
                                135

                                                         71
                                                                                                    width bit-vector operations and transition-system structure.
 0                                                                                                  Thus, bit-vector-heavy programs fit the target representation
            ESBMC              CBMC                   Eldarica             C2Btor
                                                                                                    more naturally than memory-intensive programs.
Fig. 3: Comparison of assertion verification and expressiveness                                        Array tasks are the main precision and scalability bottle-
on a curated benchmark set.                                                                         neck. C2Btor correctly solves 17.7% of the Array benchmarks,
                                                                                                    which is close to CPAchecker but clearly below the strongest
TABLE I: Percentage comparison of C2Btor with other pro-                                            tools in this category. At the same time, Array accounts for
gram verifiers on SV-COMP benchmarks (Correct / Wrong /                                             19 of the 20 TF false alarms and has a high inconclusive rate
Inconclusive, %).                                                                                   of 76.2%. Among the three benchmark categories, Array tasks
                                                                                                    are the most diﬀicult for the current BTOR2 route: they tend
 Tool                   Array             BV              Loop             All    TF/FT
                      (N = 412)        (N = 49)         (N = 312)       (N = 773) (all)
                                                                                                    to induce larger bit-level encodings and more OOT outcomes.
                                                                                                    This concentration suggests that array-heavy programs stress
 AISE                 22.3/2.2/75.2   67.3/0.0/32.7     76.6/0.0/23.4   47.1/1.2/51.6         6/3
 Bubaak               13.1/0.2/85.9   38.8/0.0/61.2     46.5/0.3/52.2   28.2/0.3/70.8         0/2   both the object/array encoding and the backend solver, making
 CPAchecker           17.5/7.8/74.3   89.8/0.0/10.2     65.1/0.0/34.6   41.3/4.1/54.2        32/0   this category the current boundary of C2Btor’s accuracy and
 ESBMC                19.2/0.0/80.8   71.4/0.0/28.6     46.2/0.0/53.8   33.4/0.0/66.6         0/0
 CBMC-BMC-200         9.2/0.0/86.9    67.3/0.0/32.7     29.2/0.3/67.9   21.0/0.1/75.8         1/0
                                                                                                    solving effectiveness.
 Symbiotic            16.0/0.0/83.5   73.5/0.0/24.5     46.8/0.0/2.2    32.1/0.0/47.0         0/0      Loop tasks show a more balanced result. C2Btor correctly
 UAutomizer           19.2/0.0/80.3   71.4/0.0/26.5     71.2/0.0/28.2   43.5/0.0/55.9         0/0   solves 49.0% of the Loop benchmarks, outperforming Bubaak
 VeriAbs              45.4/1.7/52.7   0.0/0.0/100.0     69.9/1.0/29.2   52.4/1.3/46.2         2/8
 C2Btor (Ours)        17.7/4.6/76.2   75.5/0.0/24.5     49.0/0.3/44.6   34.0/2.6/60.2        20/0   and the bounded CBMC baseline. The low wrong-verdict rate
                                                                                                    of 0.3% suggests that the program-counter-based transition
                                                                                                    relation can handle a meaningful subset of standard loop safety
   Comparison tools. The comparison covers three groups:                                            tasks. Manual inspection of abnormal outcomes indicates that
   • Top tools in the SV-COMP C ReachSafety category :
                                                           4                                        these cases are mainly caused by loop tasks combined with
     CPAchecker, ESBMC with --kind, and Symbiotic;                                                  array or memory features, where unsupported frontend cases
   • SOTA tools on the Array and Loop subsets: AISE,
                                                                                                    and backend diﬀiculty overlap.
     Bubaak, VeriAbs, and UAutomizer;
   • Baseline: CBMC with --bmc --unwind 200.
                                                                                                     Answer to RQ1: C2Btor establishes an effective ver-
                                                                                                     ification route. It generates BTOR2 models for 96.7%
The above tools are run with their corresponding SV-COMP
                                                                                                     of the tasks and obtains correct verdicts for 263 tasks,
tool configurations.5
                                                                                                     while other cases remain inconclusive or become TF false
   Figure 2 shows that C2Btor generates BTOR2 models for
                                                                                                     alarms. It also performs well on BV tasks, correctly solving
748 out of 773 tasks. Model generation is reported separately
                                                                                                     75.5% of them without wrong verdicts. This confirms
from verification correctness: C2Btor correctly solves 263
                                                                                                     the effectiveness of the C2Btor modeling route and its
tasks, 101 more than the bounded CBMC baseline, while the
                                                                                                     advantage on BV tasks.
remaining generated cases may still be inconclusive or wrong-
verdict outcomes. This shows that the BTOR2 route can benefit
                                                                                                    D. RQ2: Complementarity across Verification Encodings
from backend model-checking algorithms beyond bounded
unwinding. All wrong verdicts of C2Btor are TF false alarms,                                           Dataset. To evaluate whether the C2Btor route provides
which can be further inspected through counterexample or                                            solving behavior complementary to existing verification encod-
witness validation; more importantly, no FT missed bug is                                           ings, especially on what kinds of assertions it can verify, we
observed, whereas three comparison tools report at least one                                        combine self-constructed programs with benchmarks from the
FT case.                                                                                            TriCera dataset [23]6 , yielding a curated assertion benchmark
   Table I reports the same experiment as category-level Cor-                                       set of 525 tasks.
rect / Wrong / Inconclusive percentages, with T F for false                                            Verification routes. There are four representative routes:
alarms and F T for missed bugs. The results show that C2Btor                                           • ESBMC: LLVM-IR and SMT solving;
                                                                                                       • CBMC: Goto-IR and SAT solving;
      4 https://sv-comp.sosy-lab.org/2026/results/results-verified/
      5 https://gitlab.com/sosy-lab/benchmarking/fm-tools/-/tree/main/data                           6 https://zenodo.org/records/5831003
TABLE II: Assertion verification and expressiveness comparison on the curated benchmark set. For each baseline tool, entries
report Tool solved / Tool-only / C2Btor-only tasks; the last column reports tasks solved by C2Btor.

Assertion target          Representative tasks                                      N    ESBMC           CBMC             Eldarica          C2Btor (Ours)
Functional correctness    Tree/Array: arithmetic, search, sort, and            324      133 / 13 / 2    87 / 7 / 42       71 / 2 / 53            122
                          data-structure operation checks
Pointer consistency       Lists/Heap: next/prev pointers, aliasing, and        181      168 / 70 / 4   70 / 15 / 47   40 / 16 / 78               102
                          nullness checks
Boundary safety           Stack/Queue/Array: capacity and bounds checks         20      20 / 18 / 0      8/8/2            15 / 13 / 0             2
Overall                   Assertion-category dataset                           525 321 / 101 / 6 165 / 30 / 91 126 / 31 / 131                    226



  • Eldarica: CHC encoding with CHC solving;                              TABLE III: Model-checking tool and algorithm comparison
  • C2Btor: BTOR2 encoding with btor-ic3 model checker.
                                                                          on the BTOR2 dataset.

   From the overall results in Table II, C2Btor correctly solves          Backend              Correct (TT/FF) TF FT OOT OOM Unknown FAIL
226 out of 525 tasks, showing that it already provides non-               rIC3-BMC             69 (0/69)          0   0     211         0         0    110
trivial end-to-end solving capability. Compared with ESBMC,               rIC3-k-Induction     177 (108/69)       0   0     103         0         0    110
                                                                          rIC3-IC3             253 (177/76)       0   0      33         0         0    104
the additional gain of C2Btor is limited, suggesting that the             simpleCAR-IC3        230 (170/60)       0   0      23         0         0    137
LLVM-IR/SMT-based route still provides stronger overall cov-
erage in C semantic parsing, program modeling, and backend
verification. However, compared with CBMC and Eldarica,
                                                                           Answer to RQ2: Yes. C2Btor provides a distinct and use-
C2Btor solves more tasks correctly. This is because the former
                                                                           ful verification route that complements existing software-
are respectively constrained by a single --bmc configuration
                                                                           verification routes. The BTOR2 route solves tasks that are
or a CHC/CEGAR solving route, whereas C2Btor can reuse a
                                                                           not solved by CBMC-BMC and Eldarica, showing inde-
broader set of BTOR2 backend algorithms. This indicates that
                                                                           pendent solving capability. This complementarity is most
one advantage of the BTOR2 transition-system representation
                                                                           visible on functional-correctness and restricted pointer-
is its ability to host diverse model-checking algorithms.
                                                                           consistency assertions, where local value relations, array-
   This complementarity is not uniformly distributed across                element relations, return-value assertions, and object-level
different assertion targets. For functional-correctness tasks,             pointer relations can be effectively represented as finite
C2Btor correctly solves 122 tasks, close to the 133 tasks                  bit-vector transition systems.
solved by ESBMC. This category is the largest one and
mainly includes return-value comparisons, local numeric re-
                                                                          E. RQ3: Backend Algorithms on Generated Hardware Models
lations, array-element relations, and loop postcondition asser-
tions. Therefore, in this category, C2Btor mainly provides                   Dataset. To evaluate the capability and task sensitivity
comparable coverage rather than substantial unique solving                of backend hardware model-checking algorithms, we start
capability. For the currently supported restricted pointer as-            from 390 validated BTOR2 models generated by C2Btor and
sertions, C2Btor provides more complementary value relative               convert them to AIGER through the btor2aiger tool [1, 3],
to CBMC and Eldarica, because pointer relations can often                 obtaining a second dataset of 305 AIGER models. The re-
be finitized into object identifiers, field relations, or index           maining 85 models are excluded because their array structures
relations, and further reduced to bit-vector representations.             are not supported by the tool.
This matches the bit-precise transition-system representation                Model-checking tools and algorithms. We compare the
of BTOR2. In contrast, boundary-safety tasks are not the                  following tools and algorithm configurations:
current strength of C2Btor. These tasks usually involve array                • rIC3-BMC [29]: --bmc for AIGER and --wlbmc for
bounds, capacity constraints, and range relations inside loops,                BTOR2;
and therefore more directly expose the coverage boundary of                  • rIC3-k-Induction: --kind for AIGER and --wlkind
the current translation implementation.                                        for BTOR2;
   Overall, C2Btor can reuse BTOR2 backend model-checking                    • rIC3-IC3: --ic3 for both AIGER and BTOR2;
algorithms, which is one of its advantages over CBMC and                     • simpleCAR-IC3 [25, 27]: --ic3 for both AIGER and
Eldarica. For boundary-capacity checks, complex heap/list                      BTOR2;
semantics, and tasks requiring stronger global invariant rea-                • super_prove [31]: portfolio-based unbounded model
soning, the current method still has room for improvement. At                  checking on AIGER.
the same time, C2Btor provides an additional solving route for            For this backend-level experiment, TT denotes a true-label
a subset of finite and explicit-state C safety tasks, especially          task proved safe by the solver, corresponding to a solver-level
local functional assertions, relational assertions, and assertions        UNSAT result. FF denotes a false-label task for which the
expressible as bit-vector reachability.                                   solver finds a counterexample, corresponding to a solver-level
                                                                          SAT result.
TABLE IV: Model-checking tool and algorithm comparison               F. RQ4: Semantic Coverage and Verification Boundaries
on the AIGER dataset.
                                                                      Answer to RQ4: C2Btor has a clear and useful effective
Backend            Correct (TT/FF) TF FT OOT OOM Unknown FAIL
                                                                      scope: finite-state, bit-precise, assertion-based reachability
rIC3-BMC           78 (0/78)      0   0   64   163       0       0    safety. This scope already supports meaningful C verifica-
rIC3-k-Induction   212 (134/78)   0   0   93     0       0       0
rIC3-IC3           268 (190/78)   0   0   37     0       0       0    tion tasks with explicit control flow, local data reasoning,
simpleCAR-IC3      275 (198/77)   0   0   30     0       0       0    and restricted object-level pointer relations, while also
super_prove        276 (200/76)   0   0   26     2       0       1
                                                                      identifying concrete targets for extending BTOR2-based
                                                                      C verification.

   Table III shows a clear division of labor among BTOR2                C2Btor encodes an assertion violation as a BTOR2 bad
backend algorithms between safety proving and counterexam-           state, and verification checks whether this state is reachable
ple finding. For tasks that require proving safety, BMC can          in the generated transition system. This formulation naturally
only search for counterexamples within a bounded unfolding           matches C programs whose behavior can be represented by
depth and cannot establish unbounded safety. In contrast, k-         explicit control-flow transitions and fixed-width data updates.
induction and IC3/PDR can construct inductive safety evi-            The current encoding supports control flow with branches and
dence, with rIC3-IC3 proving the largest number of true-             loops, nondeterministic inputs, fixed-width integer operations,
label tasks. On BTOR2 models generated by C2Btor, word-              assumptions and assertions, local array accesses, and restricted
level BMC is also sensitive to array sorts, memory objects,          object-level pointer relations. The preceding results show that
and control-flow unfolding, which can quickly enlarge the            this semantic fragment is practically useful: C2Btor provides
generated formulas and lead to many OOT or FAIL outcomes.            end-to-end verification capability on standard ReachSafety
IC3/PDR does not rely only on depth-based unrolling; instead,        tasks, behaves particularly well on BV-heavy programs and
it advances the reachable state space in a property-directed         local functional assertions, and generates BTOR2/AIGER
way, which explains why it covers more safety proofs while           models that can reuse hardware model-checking algorithms.
still finding counterexamples.                                          The experiments also make the current boundary concrete.
   Table IV shows that the AIGER subset has a higher solving         Array-intensive programs are the main stress cases, because
ratio. On this bit-level subset, counterexample finding is no        array updates, symbolic indices, and loops can produce large
longer the main source of difference, since most configurations      word-level transition relations and shift more memory rea-
find a similar number of false-label cases. The main separation      soning to the backend. Programs involving complex aliasing,
comes from safety proving: IC3-style backends with stronger          dynamic heap manipulation, complex standard-library behav-
simplification, induction, and portfolio strategies prove more       ior, floating-point arithmetic, or full C undefined-behavior
safe tasks. This indicates that optimizations in hardware            semantics require stronger frontend modeling than the current
model-checking algorithms can further improve the verification       prototype provides. These cases point to the next extension
capability of models generated by C2Btor. However, this result       targets: more compact memory encodings, richer heap and
must be interpreted together with the input scope: the AIGER         alias modeling, library summaries, and broader C semantic
subset excludes array-related models, so its higher solving ratio    coverage.
is not a full replacement for complete BTOR2 coverage.                  Overall, C2Btor already provides a practical hardware-
   Overall, the models generated by C2Btor can indeed reuse          model-checking route for a useful class of finite, bit-precise C
hardware model-checking backends, but backend effectiveness          reachability-safety tasks. The current boundaries further clar-
depends on both the verification objective and the target            ify how BTOR2-based program verification can be extended
format. The advantage of BTOR2 is that it preserves word-            toward broader C semantics.
level expressiveness and can model array-related programs, al-
                                                                                            VI. Conclusion
though current BTOR2 backends still face input-compatibility
and tool-robustness bottlenecks. After conversion to AIGER,            This paper presented C2Btor, a C-to-BTOR2 verification
C2Btor can benefit from more mature bit-level backends, but          route for assertion-based reachability safety. C2Btor models
this comes at the cost of losing array-structure coverage.           the program into a BTOR2 transition system by encoding
                                                                     control flow with a program counter, representing program
  Answer to RQ3: Hardware model-checking algorithms                  data with bit-vectors and arrays, and mapping assumptions
  are effective on the verification tasks generated by C2Btor,       and assertion violations to BTOR2 constraints and bad states.
  and their effects are algorithm-specific. BMC is useful for        The evaluation shows that this route is effective in practice:
  exposing counterexamples, while induction- and IC3/PDR-            C2Btor generates BTOR2 models for 96.7% of the standard
  style algorithms are more effective at proving program             ReachSafety tasks and obtains correct verdicts for 263 cases,
  safety. The results further show that progress in hardware         while keeping model generation distinct from verification
  model checking can directly improve the verification ca-           correctness. It is particularly effective on BV-heavy programs,
  pability of C programs translated by C2Btor.                       where it solves 75.5% of the tasks without wrong verdicts,
                                                                     and it also provides complementary solving capability over
CBMC-BMC and Eldarica on functional correctness and re-              riabs: Verification by abstraction and test generation,”
stricted pointer-consistency assertions. The backend experi-         in 2019 34th IEEE/ACM International Conference on
ments further show that C2Btor-generated models can directly         Automated Software Engineering (ASE). IEEE, 2019,
benefit from hardware model-checking algorithms, especially          pp. 1138–1141.
k-induction, IC3/PDR, and portfolio-based proving. Future       [14] N. Bjørner, A. Gurfinkel, K. McMillan, and A. Ry-
work will extend this route with more compact memory                 balchenko, “Horn clause solvers for program verifica-
encodings, richer alias and heap modeling, stronger library          tion,” in Fields of Logic and Computation II: Essays
summaries, broader C semantic coverage, and more adaptive            Dedicated to Yuri Gurevich on the Occasion of His 75th
backend selection.                                                   Birthday. Springer, 2015, pp. 24–51.
                                                                [15] E. Clarke, D. Kroening, and F. Lerda, “A tool for check-
                         References                                  ing ansi-c programs,” in International Conference on
 [1] A. Biere, N. Froleyks, and M. Preiner, “Hardware model          Tools and Algorithms for the Construction and Analysis
     checking competition 2025,” in 2025 Formal Methods in           of Systems. Springer, 2004, pp. 168–176.
     Computer-Aided Design (FMCAD). IEEE, 2025, pp.             [16] L. Cordeiro, B. Fischer, and J. Marques-Silva, “Smt-
     1–1.                                                            based bounded model checking for embedded ansi-c
 [2] A. Biere, K. Heljanko, and S. Wieringa, “Aiger 1.9 and          software,” IEEE Transactions on Software Engineering,
     beyond,” 2011.                                                  vol. 38, no. 4, pp. 957–974, 2011.
 [3] A. Niemetz, M. Preiner, C. Wolf, and A. Biere, “Btor2,     [17] M. Heizmann, Y.-F. Chen, D. Dietsch, M. Greitschus,
     btormc and boolector 3.0,” in International Conference          J. Hoenicke, Y. Li, A. Nutz, B. Musa, C. Schilling,
     on Computer Aided Verification. Springer, 2018, pp.             T. Schindler et al., “Ultimate automizer and the search
     587–595.                                                        for perfect interpolants: (competition contribution),” in
 [4] A. Biere, A. Cimatti, E. M. Clarke, O. Strichman, and           International Conference on Tools and Algorithms for the
     Y. Zhu, “Bounded model checking.” Handbook of satis-            Construction and Analysis of Systems. Springer, 2018,
     fiability, vol. 185, no. 99, pp. 457–481, 2009.                 pp. 447–451.
 [5] D. Jovanović and B. Dutertre, “Property-directed k-        [18] D. Baier, D. Beyer, P.-C. Chien, M.-C. Jakobs,
     induction,” in 2016 Formal Methods in Computer-Aided            M. Jankola, M. Kettl, N.-Z. Lee, T. Lemberger,
     Design (FMCAD). IEEE, 2016, pp. 85–92.                          M. Lingsch-Rosenfeld, H. Wachowitz et al., “Soft-
 [6] A. R. Bradley, “Sat-based model checking without                ware verification with cpachecker 3.0: Tutorial and user
     unrolling,” in International Workshop on Verification,          guide,” in International Symposium on Formal Methods.
     Model Checking, and Abstract Interpretation. Springer,          Springer, 2024, pp. 543–570.
     2011, pp. 70–87.                                           [19] M. Chalupa and C. Richter, “Bubaak: Dynamic coop-
 [7] N. Eén, A. Mishchenko, and R. Brayton, “Eﬀicient im-            erative verification: (competition contribution),” in In-
     plementation of property directed reachability,” in 2011        ternational Conference on Tools and Algorithms for the
     Formal Methods in Computer-Aided Design (FMCAD).                Construction and Analysis of Systems. Springer, 2025,
     IEEE, 2011, pp. 125–134.                                        pp. 212–216.
 [8] D. Beyer and J. Strejček, “Evaluating software verifiers   [20] Z. Wang and Z. Chen, “Aise: A symbolic verifier by syn-
     for c, java, and sv-lib: (report on sv-comp 2026),” in          ergizing abstract interpretation and symbolic execution
     International Conference on Tools and Algorithms for the        (competition contribution),” in International Conference
     Construction and Analysis of Systems. Springer, 2026,           on Tools and Algorithms for the Construction and Anal-
     pp. 461–502.                                                    ysis of Systems. Springer, 2024, pp. 347–352.
 [9] F. Merz, S. Falke, and C. Sinz, “Llbmc: Bounded model      [21] M. Jonáš, K. Kumor, J. Novák, J. Sedláček, M. Trtík,
     checking of c and c++ programs using a compiler ir,”            L. Zaoral, P. Ayaziová, and J. Strejček, “Symbiotic
     in International Conference on Verified Software: Tools,        10: Lazy memory initialization and compact symbolic
     Theories, Experiments. Springer, 2012, pp. 146–161.             execution: (competition contribution),” in International
[10] A. Gurfinkel, “Program verification with constrained            Conference on Tools and Algorithms for the Construction
     horn clauses,” in International Conference on Computer          and Analysis of Systems. Springer, 2024, pp. 406–411.
     Aided Verification. Springer, 2022, pp. 19–29.             [22] H. Hojjat and P. Rümmer, “The eldarica horn solver,”
[11] C. Barrett, A. Stump, C. Tinelli et al., “The smt-lib           in 2018 Formal Methods in Computer Aided Design
     standard: Version 2.0,” in Proceedings of the 8th in-           (FMCAD). IEEE, 2018, pp. 1–7.
     ternational workshop on satisfiability modulo theories     [23] Z. Esen and P. Rümmer, “Tricera: Verifying c programs
     (Edinburgh, UK), vol. 13, 2010, p. 14.                          using the theory of heaps,” in 2022 Formal Methods in
[12] J. C. King, “Symbolic execution and program testing,”           Computer-Aided Design (FMCAD). IEEE, 2022, pp.
     Communications of the ACM, vol. 19, no. 7, pp. 385–394,         380–391.
     1976.                                                      [24] X. Zhang, S. Xiao, Y. Xia, J. Li, M. Chen, and G. Pu,
[13] M. Afzal, A. Asia, A. Chauhan, B. Chimdyalwar,                  “Accelerate safety model checking based on comple-
     P. Darke, A. Datar, S. Kumar, and R. Venkatesh, “Ve-            mentary approximate reachability,” IEEE Transactions
     on Computer-Aided Design of Integrated Circuits and
     Systems, vol. 42, no. 9, pp. 3105–3117, 2023.
[25] Y. Xia, A. Becchi, A. Cimatti, A. Griggio, J. Li, and
     G. Pu, “Searching for i-good lemmas to accelerate safety
     model checking,” in International Conference on Com-
     puter Aided Verification. Springer, 2023, pp. 288–308.
[26] X. Zhou, G. Hu, H. Zhang, and W. Zhang, “A-
     ic3: Learning-guided adaptive inductive generaliza-
     tion for hardware model checking,” arXiv preprint
     arXiv:2604.21688, 2026.
[27] J. Li, R. Dureja, G. Pu, K. Y. Rozier, and M. Y.
     Vardi, “Simplecar: An eﬀicient bug-finding tool based on
     approximate reachability,” in International Conference
     on Computer Aided Verification. Springer, 2018, pp.
     37–44.
[28] A. Biere, “Tutorial on world-level model checking,” in
     2020 Formal Methods in Computer Aided Design (FM-
     CAD). IEEE, 2020, pp. 1–1.
[29] Y. Su, Q. Yang, Y. Ci, T. Bu, and Z. Huang, “The ric3
     hardware model checker,” in International Conference on
     Computer Aided Verification. Springer, 2025, pp. 185–
     199.
[30] D. Beyer, P.-C. Chien, and N.-Z. Lee, “Bridging hardware
     and software analysis with btor2c: A word-level-circuit-
     to-c translator,” in International Conference on Tools and
     Algorithms for the Construction and Analysis of Systems.
     Springer, 2023, pp. 152–172.
[31] A. Mishchenko, R. Brayton, and N. Een, “Using specula-
     tion for sequential equivalence checking,” in Proceedings
     of International Workshop on Logic & Synthesis, 2012,
     pp. 139–145.
