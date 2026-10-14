                                              Forward Symbolic Execution for Trustworthy
                                                Automation of Binary Code Verification⋆

                                             Andreas Lindner1 , Karl Palmskog2 , Scott Constable3 , Mads Dam2 ,
                                                          Roberto Guanciale2 , and Hamed Nemati2
                                                                      1
                                                                        Uppsala University, Sweden
                                                                    andreas.lindner@angstrom.uu.se
                                                              2
                                                                 KTH Royal Institute of Technology, Sweden
arXiv:2304.08848v2 [cs.PL] 13 Jan 2026




                                                                {palmskog,mfd,robertog,hnemati}@kth.se
                                                                       3
                                                                         Intel Labs, United States
                                                                     scott.d.constable@intel.com


                                                 Abstract. Control flow in unstructured programs can be complex and
                                                 dynamic, which makes static analysis difficult. Yet, automated reasoning
                                                 about unstructured control flow is important when certifying properties
                                                 of binary (machine) code in trustworthy systems, e.g., cryptographic rou-
                                                 tines. We present a theory of forward symbolic execution for unstructured
                                                 programs suitable for use in theorem provers that enables automated ver-
                                                 ification of both functional and non-functional program properties. The
                                                 theory’s foundation is a set of inference rules where each member cor-
                                                 responds to an operation in a symbolic execution engine. The rules are
                                                 designed to give control over the tradeoff between the preservation of pre-
                                                 cision and introduction of overapproximation. We instantiate our theory
                                                 for BIR, a previously proposed intermediate language for binary analysis.
                                                 We demonstrate how symbolic executors can be constructed for BIR with
                                                 common optimizations such as pruning of infeasible symbolic states. We
                                                 implemented our theory in the HOL4 theorem prover using the HolBA
                                                 binary analysis library, obtaining machine-checked proofs of soundness of
                                                 symbolic execution for BIR. We practically evaluated two applications of
                                                 our theory: verification of functional properties of RISC-V binaries and
                                                 verification of execution time bounds of programs running on the ARM
                                                 Cortex-M0 processor. The evaluation shows that such verification can be
                                                 automated with moderate overhead on medium-sized programs.

                                                 Keywords: symbolic execution · theorem proving · binary analysis


                                         1     Introduction
                                         Unstructured programming permits “jumps of the control to strange places”
                                         via labels and goto instructions, resulting in control flow with the appearance
                                         ⋆
                                             This preprint has not undergone peer review (when applicable) or any post-
                                             submission improvements or corrections. The Version of Record of this contribution
                                             is published in “Proceedings of the 27th International Conference on Verification,
                                             Model Checking, and Abstract Interpretation – VMCAI 2026”, and is available on-
                                             line at https://doi.org/10.1007/978-3-032-15700-3_8.
2       Lindner et al.

of a “can of spaghetti” [28]. Structured programming [17], where instructions or
statements have a single exit point, is now the norm for code written by software
developers—but code with unstructured control flow lives on in high assurance
systems, e.g., as output of compilers and as hand-optimized assembly.
    Static analysis of unstructured code, e.g., of RISC-V binaries [59], is difficult
due to its complex, dynamic control flow. For instance, jump targets may be
computed at runtime from register and memory values (indirect jumps). Nev-
ertheless, trustworthy automated reasoning about binary code is important for
certifying the correctness of high-assurance systems. In particular, binary verifi-
cation may be used for translation validation when using untrusted compilers [53]
and for directly ensuring the correctness of low-level cryptographic code [46] and
security mechanisms such as software fault isolation [60].
    We believe forward symbolic execution is well-suited for automating binary
verification. Such an approach explores program paths with symbolic input, nat-
urally captures cause-effect in control and data flow, tracks how data drives
behavior without source-level types, and integrates well with control-flow re-
construction and memory-alias analysis. Based on these insights, we present a
general theory of forward symbolic execution for unstructured programs suit-
able for use in interactive theorem provers. The basis of the theory is a set of
core inference rules, each corresponding to operations in an abstract symbolic
execution engine, designed to control the tradeoff between precision and overap-
proximation, which is important when analyzing real-world binary code (Sec. 3
and 4). The theory can be instantiated for unstructured languages by relating
their concrete and symbolic semantics. We instantiate the theory for BIR, a pre-
viously proposed intermediate language for binary analysis [42], and construct
sound symbolic executors with optimizations such as pruning of infeasible states.
We implemented the theory in the HOL4 theorem prover [32] and instantiated it
using the HolBA binary analysis library [42], providing machine-checked proofs
of soundness of symbolic execution for BIR (Sec. 5).
    Using our implementation, we extended HolBA with support for two novel
applications: (1) automated verification of functional properties of RISC-V bi-
naries using contracts and (2) automated verification of execution time bounds
of binaries executing on the ARM Cortex-M0 processor. We call this extension
HolBA-SE. Our application of HolBA-SE for functional verification of RISC-
V code is based on previous work which lifts RISC-V instructions to BIR [42]
while preserving semantics as defined by L3 [25], and provides Hoare-style con-
tracts for binary programs [44]. To this we add trustworthy automation of BIR
contract proofs and for propagating such proofs to RISC-V level (Sec. 6). We
applied HolBA-SE to RISC-V case studies from two high-assurance domains,
namely, cryptography and operating system kernels, indicating that we can au-
tomate translation validation and verification of hand-written assembly outside
the scope of verified compilers. In our application of HolBA-SE for verification of
execution time bounds (Sec. 7), we rely on the fact that in relatively simple pro-
cessors such as the ARM Cortex-M0, instructions take constant time to execute.
This means that we can explicitly represent execution time as a symbolic state
                   Forward Symbolic Execution for Binary Code Verification        3

variable, which we use to perform a collection of case studies on ARM Cortex-M0
binaries where we verify their execution time bounds. Our evaluation compares
our results against an established industrial tool, aiT, showcasing the potential
of our approach for trustworthy worst-case execution time (WCET) analysis.
    In summary, we make the following contributions:
 1. We propose a general theory of symbolic execution for unstructured pro-
    grams designed and adapted for use in interactive theorem provers.
 2. We provide an implementation of our theory in the HOL4, along with an
    instantiation for the BIR language and machine-checked soundness proofs.
 3. We design symbolic executors that automatically apply our theory’s infer-
    ence rules for symbolic execution of BIR programs generated from RISC-V
    and Cortex-M0 machine code, building HOL4 progress structure theorems.
 4. Using progress structures, we implement automation for functional verifica-
    tion of RISC-V programs and WCET verification for Cortex-M0 programs
    on top of the HolBA library, experimentally evaluated in several case studies.
   Source code for HolBA-SE and our verification case studies is available under
an open source license [43], and has been integrated into the HolBA library [33].


2     Background
We use BIR [42] as a vehicle for explaining our theory and implementation.
BIR (Binary Intermediate Representation) is an intermediate language designed
for binary analysis. It abstracts away ISA (Instruction Set Architecture) details
while preserving the semantics of binaries, enabling architecture-independent
reasoning about machine code. Beyond serving as a convenient notation in this
paper, BIR provides a general framework for implementing trustworthy binary
analyses, thanks to its formal semantics and implementation in the HOL4 theo-
rem prover. The application of symbolic execution to binary code presents unique
challenges. To illustrate these, we use a modular exponentiation (ModExp) rou-
tine expressed in BIR, whose control flow graph is presented in Fig. 2. The
pseudocode of the corresponding modular exponentiation algorithm is shown in
Fig. 1. For simplicity, the program operates only on 32-bit words instead of rely-
ing on a bignum library. The program highlights key challenges—unstructured
control flow, path explosion, expression growth, and memory aliasing—that mo-
tivate our symbolic execution rules and optimizations.

2.1   The BIR language
A BIR program consists of uniquely labeled blocks, with each block containing
a sequence of statements. In the running example, the blocks consist of a sin-
gle statement and are labeled by 1, . . . , 14. Labels l ∈ Lp correspond to specific
locations in the program p and are commonly used as the target for jump in-
structions. BIR statements include assignment of BIR expressions to variables
(e.g., SP := SP - 8), unconditional and conditional jumps (e.g., goto R3 and
4       Lindner et al.

 f (e , b , m ):
   [ prologue ]
   r := 1
   for i in 0 .. 31 {
      if e [ i ]
          r := ( r * b )% m
      b := ( b * b )% m
   }
   return r
   [ epilogue ]


Fig. 1: ModExp pseudocode.
                                             Fig. 2: BIR CFG of ModExp.


if R3=32 goto 6), a halt statement to indicate execution termination, and
assert to evaluate a boolean expression and terminate execution if the asser-
tion fails. Expressions in BIR include constants v ∈ BV , variables x ∈ BVars,
conditionals, arithmetic operations, and memory operations such as load (ld)
and store (st).
    Fundamentally, the content of the following sections is not specific to BIR,
but requires the underlying concrete model and its semantics to satisfy some
properties, which indeed are satisfied by BIR. The concrete execution is mod-
eled by a deterministic and total transition relation → . In BIR, states ⊥ and
⊤ (reached by failed assertions and halt, respectively) represent failing and suc-
cessful terminating states that can only transition to themselves; every concrete
state s ∈ S consists of a program counter and a store, extracted by pc(s) and
store(s), respectively; Stores δ partially map variables x ∈ BVars to concrete
values v ∈ BV , and instructions are addressed using labels ranged over by l.
    Because code is unstructured, we use sets of labels L ⊆ Lp (not necessarily
consecutive) to identify fragments of binary code. We define s ⇝L s′ = {(s, s′ ) |
s → s′ ∧ pc(s) ∈ L} as the restriction of the transition relation, where source
states must belong to a fragment L, and →nL for the application of n transitions.
Note that these relations are partial and deterministic, and if s0 →nL sn then
each intermediate state has program counter in L: if i < n and s0 →iL si then
pc(si ) ∈ L.


2.2   Running example

The BIR program in Fig. 2 implements modular exponentiation using the stan-
dard right-to-left method, computing be mod m. Parameters e, b, and m are
passed in BIR variables R0-R2, and R3 stores the return address. The first in-
struction (line 1) asserts that the stack pointer (SP) is restricted to the designated
stack region of memory, spanning addresses 0x1000 to 0x1500. This assumption
becomes the initial path condition during symbolic execution. Lines 2–3 form
                   Forward Symbolic Execution for Binary Code Verification         5

the function prologue: the function allocates two words to the stack and then
pushes the return address (passed in through the R3 register ) onto the stack,
whose top is pointed to by the stack pointer SP. In BIR, memory is modeled as
a single map variable M , which is accessed and modified by the operations ld
(load) and st (store). The local variable r is stored at address SP - 8, and line
4 sets its initial value to 1. The loop counter i is tracked in register R3, which
is initialized to 0 at line 5. Line 6 is a conditional jump that evaluates the if
condition and determines the subsequent control flow. Lines 7 and 8 implement
the multiplication-and-modulo operations of the pseudocode: line 7 updates the
memory location, where r is allocated on the stack, while line 8 updates the
base value b directly in a register. Lines 9 and 10 implement the loop’s iteration
logic, incrementing the counter and branching back to line 6 until 32 iterations
have been completed, after which execution proceeds to line 11. At this point,
the value of r is reloaded from the stack into the return register R0. Finally, lines
12–14 constitute the epilogue: the function restores the original return address,
resets the stack pointer, and executes an indirect jump via R3 to return control
to the caller.

2.3   Challenges and approach
This example highlights several core difficulties of symbolic execution for binary
code: C1 Unstructured control flow: Indirect jumps complicate reconstruc-
tion of feasible control-flow targets, since jump addresses may depend on runtime
values in registers or memory. For instance, instead of branching directly at line
6, the program could implement the conditional jump via a lookup table stored
in memory, where the target address is computed from the branch condition,
e.g., goto ld(M, 0x100+(((R0>>R3)&1)*4)). In this case, the jump destina-
tions (e.g., lines 7 and 8) are retrieved from memory addresses 0x104 and 0x100,
respectively. Such table-based indirection introduces an additional layer of com-
plexity, requiring the analysis to identify all feasible addresses and corresponding
memory contents to recover the possible control flow. C2 Path explosion: The
conditional branch inside the loop leads to an exponential number of feasible
execution paths, in this case 232 ). C3 Expression growth: Operations that
repeatedly manipulate memory and registers, such as the modular multiplica-
tion in line 7, duplicate symbolic expressions, and cause exponential expression
growth. C4 Memory aliasing: Since binary programs operate on flat memory,
reasoning about disjointness of memory locations becomes necessary, for exam-
ple, to show that internal loop operations do not overwrite the return address.
C5 Repeated fragments: Loops and repeated function calls execute multiple
times the same code fragments, leading to redundant symbolic computations if
treated naively. C6 Interval reasoning: Many analyses require reasoning about
bounded counters or index values (e.g., the loop variable), which is difficult to
express without explicit support for symbolic intervals. C7 Architectural de-
pendencies: Symbolic execution at the binary level is tightly coupled to the ISA
and its semantics. Without an intermediate language like BIR, each symbolic ex-
ecutor must be tailored to a specific ISA, limiting reuse across architectures.
6       Lindner et al.

     Our approach to addressing these challenges simultaneously is built on three
key elements. Forward exploration: for unstructured code (C1), feasible tar-
gets of indirect jumps or table lookups can only be determined by symbolically
executing the preceding instructions. Compositional inference rules: These
rules support controlled overapproximation through the introduction of free sym-
bols. The rules address C1 (path explosion) and C2 (expression blow-up) by
merging equivalent states and bounding symbolic expression growth, while C4
(memory aliasing) is mitigated through simplification rules that identify equiva-
lent or disjoint memory accesses. The rules also address C5 (repeated fragments)
by allowing the instantiation of previously analyzed code fragments, and address
C6 (interval reasoning) by manipulating path conditions and free symbols in a
sound manner. Integration with HolBA: Binaries are lifted into BIR, an in-
termediate language with a formally verified transpiler in HOL4. HolBA provides
an ISA-independent substrate, directly addressing C7 by allowing the same sym-
bolic executor to reason about RISC-V, ARM, or other architectures once their
lifting to BIR is defined.
     Our symbolic execution data structures and soundness definitions are de-
signed to allow incremental proofs, facilitating implementation of proof automa-
tions in interactive theorem provers. As an instance, we describe our imple-
mentation of automatic symbolic executors and semi-automatic optimization
procedures within HOL4 and showcase the verification of binary code proper-
ties.


3   Symbolic Semantics

The inference rules for symbolic execution in Sec. 4 are general, but require
a symbolic semantics for individual instructions of the specific model. In this
section, we lay down notation for the symbolic semantics and we exemplify a
few rules for the symbolic semantics of BIR, which captures the main traits of
the semantics supported by our symbolic executor.
     We assume symbols α that range over the set BSyms and a symbolic expres-
sion language that supports at least first-order logic. Symbolic expressions are
denoted by v ∈ BV . A symbolic store δ is a mapping of variables to symbolic
expressions. We use δ id to refer to the symbolic store that maps each variable to
a different symbol, i.e., δ id (V) = αV for each V. We use ϕ for boolean symbolic ex-
pressions, which are used, for instance, as path conditions. A symbolic state s is
a triple of a concrete program counter l, a symbolic store δ, and a path condition
ϕ. We define the accessor functions pc(s) = l, store(s) = δ, path(s) = ϕ.
     The symbolic and concrete semantics are connected using a partial interpre-
tation H : BSyms → BV , mapping symbols to concrete values. Interpretation is
lifted to symbolic expressions and stores, i.e., the interpretation H(v) produces
a concrete value, and H(δ) produces a concrete store. The resolution function
tϕ (v) = {v | ∃H. H(ϕ) ∧ H(v) = v} computes the set of all concretizations of
the symbolic expression v under the path condition ϕ.
                   Forward Symbolic Execution for Binary Code Verification                    7

Definition 1. The symbolic state s matches a concrete state s via the inter-
                       H
pretation H, written s ▷ s, if pc(s) = pc(s), H(store(s)) = store(s), and
H(path(s)).
                                                H                                         H
For sets of symbolic states Π, we write Π ▷ s if there is an s ∈ Π such that s ▷ s.
   We exemplify the symbolic transition rule for conditional jumps in BIR:
p(l) = if e goto et else ef     ϕt = LeMδ     ϕf = ¬ϕt      x ∈ {t, f } lb ∈ tϕ∧ϕx (Lex Mδ )
                              p ⊢ (l, δ, ϕ) ,→ (lb , δ, ϕ ∧ ϕx )
Note that the rule hypothesis requires knowing the current instruction. There-
fore, without loss of generality, we treat the program counter as a concrete value
rather than a symbolic expression. In fact, the rules are defined to account for
all possible target values of the program counter via the resolution function. The
rules use symbolic evaluation of the BIR expressions, which is written as LeMδ
and substitutes in e all variables with the corresponding symbolic expression
from the store δ and results in a symbolic expression.
    In the following, we use the total function symsem(s) = {s′ | s ,→ s′ } to
represent all possible successors of an input state in the symbolic semantics.
Soundness means that the symbolic semantics overapproximates the concrete
one, which we formulate as a simulation.
                   H                                                                  H
Theorem 1. If s ▷ s and s → s′ , then exists s′ ∈ symsem(s) such that s′ ▷ s′ .
Note that the same interpretation function H is used for matching both source
and target states.


4     Symbolic Execution
One could build the symbolic executor by iteratively applying symsem(s). How-
ever, this usually results in a large execution tree, which is infeasible to directly
compute. Similarly, this naive approach neither allows for overapproximations,
which is useful to speed up computation, nor to reuse previous results. The
main goal of the symbolic execution rules below is to formalize sound compo-
sitions, specializations, computation reuses, simplifications, and approximations
that preserve soundness throughout the analysis. While we exemplify the rules
only for the symbolic semantics of BIR, the inference rule system has been proven
correct for any symbolic and concrete semantics that satisfies Theorem 1.

4.1   Progress structures
The first building block is the formalization of the intermediate results of sym-
bolic execution. Symbolic execution iteratively builds up and composes symbolic
execution trees, but only keeps track of the roots and the leaves of the trees and
disregards the internal nodes that are constructed with the symbolic semantics.
We call this object a progress structure and denote it as s ⇝L Π. A progress
8       Lindner et al.

structure captures that all concrete states matched by the source state s execute
through the label set L and eventually reach a concrete state that is matched
by one of the target states in Π.
    In order to formally define the meaning of a progress structure, we first
need to introduce some auxiliary notation. The function Λ(s) returns the set of
symbols that occur in s, and we overload it for sets of states as the union of
symbols in the states. For a progress structure s ⇝L Π, we call bs(s ⇝L Π) =
Λ(s) its bound symbols and fs(s ⇝L Π) = Λ(Π) \ Λ(s) its free symbols. We use
H ′ ⊇ H to represent that the partial function H ′ extends H, i.e. Dom(H ′ ) ⊇
Dom(H) and H ′ (α) = H(α) for all α ∈ Dom(H).
    The following two definitions support the formulation needed to overapprox-
imate with fresh symbols in target states of progress structures.
Definition 2. An interpretation H is minimal for s, written as ↓s (H), if
Dom(H) = Λ(s).
This predicate is applied to source states to ensure that interpretations can be
extended with arbitrary values for free symbols not occurring in the initial state.


Definition 3. The symbolic state s′ loosely matches the concrete state s′ via H,
              H                                                         H’
written as s′ ▶ s′ , if there is an interpretation H ′ ⊇ H such that s′ ▷ s′ .
This predicate relaxes matching using interpretation extension to allow free sym-
bols in target states s′ to take on arbitrary values in the matching of concrete
states s′ . We then define the meaning of a progress structure via its soundness.
Definition 4. A progress structure is sound, written ⊢ s ⇝L Π, if for every
                                  H
interpretation ↓s (H) and state s ▷ s, exists s →nL s′ where n > 0, and exists
                      H
s′ ∈ Π such that s′ ▶ s′ .
Compared with the soundness of the symbolic semantics (Theorem 1), the for-
mulation of the soundness of the symbolic execution is different in two ways.
   First, we assume minimality of the initial interpretation (↓s (H)) and allow
                                      H
loose matches for final states (s′ ▶ s′ ), which together enable the introduction
of fresh symbols. For example, suppose that the architecture has only registers
R1 and R2 and we symbolically execute line 8 of Fig. 2. The symbolic semantics
is (8, δ id , T ) ,→ (9, δ id [R1 7→ αR1 ∗ αR1 %αR2 ], T ). Progress structures allow for-
getting the exact value assigned to R1, producing the sound progress structure
(8, δ id , T ) ⇝{8} {(9, δ id [R1 7→ α′ ], T )} (as long as α′ ̸∈ Λ(δ id )). Because we re-
quire any initial interpretation to be minimal (e.g., for a state {R1 7→ 2, R2 7→ 3}
the interpretation has to be {αR1 7→ 2, αR2 7→ 3}), this does not map the fresh
symbol α′ . Instead, the loose interpretation matching allows to choose any ex-
tended interpretation (e.g. {αR1 7→ 2, αR2 7→ 3, α′ 7→ 1}) that maps α′ to any
value, including the value that the concrete execution produces. If we had not
assumed the initial interpretation to be minimal, the definition would be too
strict and would not allow overapproximation with fresh symbols. For example,
                    Forward Symbolic Execution for Binary Code Verification                  9

symsem(s) = Π pc(s) ∈ L                            ⊢ s ⇝L Π ∪ {(l, δ, ϕ)}
                             symbstep                                                     case
        ⊢ s ⇝L Π                         ⊢ s ⇝L Π ∪ {(l, δ, ϕ ∧ ϕ′ ), (l, δ, ϕ ∧ ¬ϕ′ )}
⊢ s ⇝L Π ∪ {s′ } ∀H. H(¬path(s′ ))                  ⊢ s ⇝L Π α ′ ∈
                                                                 / Λ(s) ∪ Λ(Π)
                                      infeasible                                      rename
             ⊢ s ⇝L Π                                   ⊢ s[α′ /α] ⇝L Π[α′ /α]
       ⊢ s ⇝L Π ∪ {s′ }     α∈
                             / Λ(s)      α′ ∈
                                            / Λ(s) ∪ Λ(s′ )
                                                              freesymb_rename
                     ⊢ s ⇝L Π ∪ {s′ [α′ /α]}
               ⊢ s ⇝L Π      α ∈ Λ(s)     Λ(v) ∩ fs(s ⇝L Π) = ∅
                                                                     subst
                              ⊢ s[v/α] ⇝L Π[v/α]
     Fig. 3: Overview of the symbolic-execution core inference-rules, part 1.




it would require satisfying the property also for all interpretations that bind α′
to some other values, including the ones that do not match the final value of R1.

   Second, the concrete execution does not occur as an assumption but is a
conjunct of the conclusion instead. Therefore, a sound progress structure also
guarantees the termination of the concrete execution: the concrete source state
must, in a finite number of transitions within L, reach a concrete target state
that is loosely matched by one of the target states. We require n > 0 to be able
to prove properties for looping code by ensuring progress when the source and
target states point to the same label.

   Unstructured code can be handled well with this soundness definition as
arbitrary control flows are contained and abstracted as label sets, which represent
code fragments. Note that indirect jumps are already handled by the symbolic
semantics, which assumes knowledge about all feasible jump targets and captures
those in the symbolic state set of Theorem 1.

    A sound progress structure ensures that all matched concrete executions
only encounter program labels in L before matching one of the targets s′ ∈ Π.
Therefore, if pc(s′ ) ∈
                      / L then pc(s′ ) is only encountered once in the end. For
example, the progress structure from the previous paragraph guarantees that the
program counter of the target state 9 is only encountered in the final execution
state, because the relation s →nL s′ establishes that s′ is reached and no transition
is taken from a state pointing to 9 ∈   / {8}. This allows establishing properties
when reaching a certain label of the program for the first time. Because in
Definition 4 the label set only appears in the relation s →nL s′ , which is under
an existential quantifier, extending label sets is permissible. We therefore may
add 9 to the label set of the previous progress structure and obtain a sound
but weaker progress structure: (8, δ id , T ) ⇝{8,9} {(9, δ id [R1 7→ α′ ], T )}. In fact,
since the program counter of the target state is now in the label set, according
to Definition 4, the concrete execution may go through loosely matching states
several times, and thus potentially execute instructions 8 and 9 multiple times.
10      Lindner et al.

4.2   Inference rules

The core set of inference rules in Fig. 3 and Fig. 4 form the foundation of the
symbolic execution. Each rule is a core operation that an execution engine can
carry out while guaranteeing sound results.
Rule symbstep. This is the base rule to obtain a progress structure from a
single step of the symbolic semantics. Because the concrete transition relation
and the function symsem(s) are total, the simulation of Theorem 1 implies that
the corresponding progress structure is sound.
Rules case, infeasible, rename, and freesymb_rename. While the
symbolic semantics can already generate multiple states for individual instruc-
tions (e.g., for conditional branches), the rule case allows further splitting a
target state by a path condition conjunct. This can be useful to analyze differ-
ent cases of the same execution path individually (e.g., one representing the case
that two registers point to different memory locations and the one representing
memory aliasing). The rule infeasible allows dropping of infeasible paths, and
rename allows straightforward renaming of symbols. Rule freesymb_rename
allows renaming of free symbols specifically, under more relaxed assumptions.
Rule subst. This rule allows to derive specialized progress structures from
general ones, by substituting single symbols with symbolic expressions. This
is needed for reusing previous computations of binary fragments, e.g., the same
code executing multiple times on several paths. By requiring that the substituted
symbol is bound, the rule prevents the substitution of free symbols, to avoid
missing concrete executions. Additionally, the symbols of the symbolic expression
must not appear as free symbols, because they would become bound symbols
otherwise, which may also lead to missing concrete executions.
Rule simplify. This rule combines two purposes: simplifying a symbolic ex-
pression of a target state by replacing it with an equivalent one and also intro-
ducing a fresh symbol in the new symbolic expression.
     Simplification requires the expressions to be equivalent under the path con-
dition of the state that is being changed. For example, if the path condition
entails αb > 0, then we may use this rule to replace αa ∗ αb > 0 with αa > 0 in
the store. This rule is particularly important for memory operations of binary
code, by allowing for the simplification of store and load expressions under the
path condition, as identified and applied in previous work [24, 18, 13]. In this
way, load expressions can be matched with store expressions if their addresses
agree in all interpretations, or bypass them if the accessed memory range is al-
ways completely disjoint. Similarly, store expressions can be removed if they are
superseded by stores to the same addresses.
     The introduction of a fresh symbol α requires that it does not occur in the
source state, and also not in the target state where it is introduced. Otherwise,
this could interfere with other usages of this symbol as per the soundness prop-
erty of the progress structure. To avoid unnecessary overapproximation, the path
condition of the modified state is extended with a constraint on α. Intuitively,
it is fixed to the value of the original symbolic expression that it replaces in the
                    Forward Symbolic Execution for Binary Code Verification           11

                                       ∀H. H(ϕ ∧ α = v ′′ ⇒ v = v ′ )
          ⊢ s ⇝L Π ∪ {(l, δ, ϕ)}
                                          α ̸∈ Λ(s) ∪ Λ((l, δ, ϕ))
               δ(x) = v
                                           Λ(v ′′ ) ⊆ Λ((l, δ, ϕ))
                                                                        simplify
                  ⊢ s ⇝L Π ∪ {(l, δ[x 7→ v ′ ], ϕ ∧ α = v ′′ )}

             s1 ⇒ s′1     ⊢ s′1 ⇝L Π ∪ {s2 }
             s2 ⇒ s′2     Λ(s1 ) ∩ fs(s′1 ⇝L Π ∪ {s2 }) = ∅
                                                                  consequence
                           ⊢ s1 ⇝L Π ∪ {s′2 }

                                          ∀H. H(path(s) ⇒ ϕ′ )
              ⊢ s ⇝L Π ∪ {(l, δ, ϕ)}
                                          Λ(ϕ′ ) ⊆ Λ(path(s))
                                                                    transfer
                         ⊢ s ⇝L Π ∪ {(l, δ, ϕ ∧ ϕ′ )}

     ⊢ sA ⇝LA ΠA        ⊢ sB ⇝LB ΠB         Λ(sA ) ∩ fs(sB ⇝LB ΠB ) = ∅
                                                                           sequence
                     ⊢ sA ⇝LA ∪LB (ΠA \ {sB }) ∪ ΠB

     Fig. 4: Overview of the symbolic-execution core inference-rules, part 2.


modified target state, to retain exactly the feasible set of state concretizations
and not add any overapproximation in the process. For example, executing line 8
of Fig. 2 with symbstep produces the sound progress structure (8, δ id , T ) ⇝{8}
{(9, δ id [R1 7→ v], T )}, where v = (R1∗R1)%R2. Using simplify, we can introduce
α in place of v and obtain (8, δ id , T ) ⇝{8} {(9, δ id [R1 7→ α], α = v)}.
Rule consequence. This rule allows to strengthen the path condition of the
source state and to weaken the path condition of a target state. Free symbols of
the structure s′1 ⇝L Π ∪ {s2 } must not occur in s1 to avoid capturing them.
    We say that s is weaker than s′ , written as s ⇒ s′ , if the two states have the
same store and program counter and the path condition of s implies the path
condition of s′ , i.e., s = (l, δ, ϕ) ∧ s′ = (l, δ, ϕ′ ) ∧ ∀H. H(ϕ ⇒ ϕ′ ). It is obvious
that s ⇒ s′ implies that every state s matched by s is also matched by s′ .
    Applying consequence to the example before allows removing the con-
straint on α from the path condition of the final state, weakening it, and ob-
taining (8, δ id , T ) ⇝{8} {(9, δ id [R1 7→ α], T )}. This results in overapproximation,
since the value of R1 is now unconstrained.
Rule transfer. This rule is complementary to consequence and it allows
for strengthening the target path conditions based on the source path condition.
This is permitted because the interpretation H in Definition 4 is extended when
loosely matching target states, and therefore the initial path condition is also
satisfied in all target states.
Rule sequence. Finally, this rule allows the sequential composition of two
symbolic executions. This operation implicitly widens the code fragment scope
by merging the two label sets. Applying this operation only makes sense in case
sB occurs in ΠA , which also does not introduce overapproximation. We require
12      Lindner et al.

that there is no free symbol in the second execution (B) that is bound in the
first execution (A). Otherwise, the result may miss concrete executions.
    To continue with the example from before, we need to first execute line 9
with symbstep to obtain (9, δ id [R1 7→ α], T ) ⇝{9} {(10, δ id [R1 7→ α][R3 7→
αR3 + 1], T )}. The sequential composition of the two progress structures renders
(8, δ id , T ) ⇝{8,9} {(10, δ id [R1 7→ α][R3 7→ αR3 + 1], T )}, which is allowed because
the second progress structure has no free symbols.

4.3   Symbolic execution example
We illustrate our rules on the modular exponentiation of Fig. 2. We focus on
using symbolic execution to establish control-flow graph integrity, i.e., verifying
that the link register R3 is correctly restored. We use this example to show
how overapproximation helps scalability: it allows us to abstract from values
irrelevant to control flow while still proving its integrity. A naïve executor that
only applies symbstep and sequence would quickly become inefficient due to
branching and expression growth.
    We start analysing the loop body. Starting from path condition ϕ0 , exe-
cuting line 6 with symbstep yields this progress structure for the conditional
branch: (6, δ id , ϕ0 ) ⇝6 {sT , sF }, where sT = (7, δ id , ϕ0 ∧ (αR0 >> α1 )&1) and
sF (8, δ id , ϕ0 ∧ ¬((αR0 >> α1 )&1)). The two final states are produced directly by
applying the symbolic semantics for individual instructions, rather than manu-
ally identifying the branch conditions and applying case.
    The two paths can be analysed individually, starting from the corresponding
state produced above, simply using symbstep and sequence. This results in
sT ⇝[7...9] s1 , where s1 = (10, δ1 , ϕ0 ∧ (αR0 >> α1 )&1) and δ1 = δ id [R3 7→ α1 +
1][R1 7→ αR1 ∗αR1 %αR2 ][M 7→ st(αM , αSP , ld(αM , αSP )∗αR1 %αR2 )], and sF ⇝[7...9] s2 ,
where s2 = (10, δ2 , ϕ0 ∧ ¬(αR0 >> α1 )&1) and δ2 = δ id [R3 7→ α1 + 1][R1 7→
αR1 ∗ αR1 %αR2 ]. These two progress structures one by one with the one obtained
from line 6 via sequence renders: (6, δ id , ϕ0 ) ⇝[6...9] {s1 , s2 }.
    Overapproximating the behavior of the loop reduces the complexity of the
analysis. For instance, when establishing control flow integrity and termination,
the values of R1 and the stack variable where r is stored are irrelevant. Overap-
proximating the former allows us to avoid duplicating the size of the expression
for R1 at each loop iteration (due to the double reference to the previous value
of R1). Overapproximating the latter allows us to merge the two symbolic states
resulting from the loop execution. In both cases, the approach is similar.
    For the memory operation, we first transform s2 to an identical one us-
ing simplify by explicitly storing the current memory value at αSP : (10, δ2 [M 7→
st(αM , αSP , ld(αM , αSP ))], ϕ0 ∧¬(αR0 >> α1 )&1). Then for both states, we use sim-
plify to introduce the fresh symbol α′ for ld(αM , αSP ) ∗ αR1 %αR2 and ld(αM , αSP )
respectively to make the two symbolic stores identical. Finally, we remove the
equality introduced in the path condition and drop the branch condition con-
juncts introduced at line 6 with consequence, which allows to merge the two
states that are now identical and obtain the progress structure: (6, δ id , ϕ0 ) ⇝[6...9]
(10, δ id [R3 7→ α1 + 1][R1 7→ αR1 ∗ αR1 %αR2 ][M 7→ st(αM , αSP , α′ )], ϕ0 ).
                     Forward Symbolic Execution for Binary Code Verification              13

    Merging two states to avoid path explosion is a common technique [40] and
similar to widening for reaching fixed points in abstract interpretation [15]. A
similar approach can be used to introduce a new symbol α′′ that allows to
abstract from the details of the expression computed for R1: (6, δ id , ϕ0 ) ⇝[6...9]
(10, δ id [R3 7→ α1 + 1][R1 7→ α′′ ][M 7→ st(αM , αSP , α′ )], ϕ0 ).
    The progress structure for the loop body can be used when creating a progress
structure for the whole example function. The process for this is sequential exe-
cution from the first line, greedily instantiating the loop body progress structure
whenever possible. Instantiation of progress structures requires instantiation of
symbols of the state via subst and massaging of expressions (like reordering
store operations in symbolic memory) via simplify and rename. Additionally,
after each instantiation and subsequent composition with sequence, it is nec-
essary to remove the infeasible branch of the loop body progress structure with
infeasible and drop the introduced conjunct with consequence. Using sim-
plify, we remove store operations that have the same symbolic address (αSP −4),
thus maintaining an overall smaller memory expression. This is a standard sim-
plification enabled by array axiomatization [24, 18, 13]. After completing all
operations, we finally obtain the overall progress structure:
                                                                                   
                                       SP 7→ αSP , R0 7→ αa , R1 7→ αb , R3 7→ αR3
 (1, δ id , ϕ0 ) ⇝{1..14} {(15, δ id                                                  , ϕ0 )}
                                         M 7→ st(st(αM , αSP , αR3 ), αSP − 4, αa )

   This progress structure has only one reachable state, which implies guaran-
teed termination in a matching state at line 15, at which the registers SP and R3
are restored to their initial values.


5    Implementation
This section gives an overview of our implementation in the HOL4 theorem
prover of our symbolic execution theory and its instantiation for BIR.
    We build on HolBA, a library for binary analysis implemented in Standard
ML (SML) using the HOL4 theorem prover [32]. HolBA follows the architec-
ture of traditional binary analysis tools such as the Binary Analysis Platform
(BAP) [10] in that it transpiles machine code to a single intermediate lan-
guage (BIR for HolBA) in which analyses are performed. In contrast to BAP,
HolBA builds directly on formal ISA models as defined in their L3 specifica-
tions [25, 26], and produces HOL4 lifting theorems linking machine code behavior
with transpiled BIR behavior via simulation relations. This significantly reduces
the trusted computing base (TCB) of HolBA compared to similar tools. Fig. 5
illustrates the organization of HolBA and the relations between its components.
    Our extension, HolBA-SE, adds to HolBA (1) a standalone HOL4 theory on
symbolic execution and progress structures, (2) an instantiation of this theory
for BIR, (3) general SML procedures automating proofs of progress structure
soundness and program properties, (4) an integration of these to perform auto-
matic verification of (i) contracts for RISC-V programs and (ii) execution time
bounds for ARM Cortex-M0 programs. Thanks to the embedding of HOL4 in
14      Lindner et al.

       HOL4
                    ISA Models
                                                        HolBA                                      Type
                                                                  Type Checker
          RISC-V       Cortex-M0       ARMv8                                                      Failures

                                                                   Weakest       Contract        Contract
                                                                  Precondition   Theory         Theorems
              Transpiler                    BIR
                                                                   Symbolic
                                                                                            Execution Time
                                                                   Execution
                                                                                               Bounds
        Partial              Resolving            Static Single    Relational                  Absence of
       Evaluation          Indirect Jumps         Assignment        Analysis                  Side Channels



Fig. 5: Architecture of HolBA, a HOL4-based binary analysis library. Compo-
nents and outputs relevant to HolBA-SE are highlighted.

SML, each HolBA-SE verification task can be manifested as a custom SML pro-
gram that reads files such as disassembly and then generates and checks the
relevant HOL4 definitions and theorems.

5.1   Results formalized and proved in HOL4
Our standalone theory of symbolic execution in HOL4 encodes the definitions
and proofs of all rules from Sec. 4 using predicate sets and inductive relations. To
integrate this theory with BIR as represented in HolBA, we encoded the symbolic
semantics as described in Sec. 3 and proved Theorem 1 in HOL4, establishing
that the semantics is sound with respect to the existing concrete BIR semantics.
The definitions and proofs of the symbolic execution rules consist of around
16,000 lines of HOL4 (SML) code and took 8 person months to develop.

5.2   Symbolic executors and progress structures in HolBA-SE
Our approach to practical symbolic execution of BIR is to provide a framework
inside HOL4 and HolBA where symbolic executors with different strategies are
expressed as proof-producing SML procedures. Here, strategy refers to how the
executor composes underlying execution blocks when run, and proof-producing
refers to how a procedure produces a HOL4 theorem when (or if) it terminates. In
executors, such theorems are witnesses that a specific progress structure (“sum-
mary”) has the required properties. In a program verification workflow, progress
structure theorems obtained from executors are decomposed and reused in other
theorems, e.g., in Hoare-style contract proofs as described in Sec. 6.
    In practice, our framework is a high-level abstraction layer (SML API) for
leveraging symbolic execution rules. For a selection of rules, we provide param-
eterized execution blocks that perform one primitive symbolic operation and
return a HOL4 theorem. When running an executor, such parameterized blocks
are composed and interleaved with domain-specific post-processing steps. For
example, one may apply the infeasible rule to prune branches, or simplify ex-
pressions for constant propagation and memory accesses. ISAs may require dif-
                  Forward Symbolic Execution for Binary Code Verification      15

ferent approaches due to specific uses of expression combinations. We developed
symbolic executors for RISC-V and ARM Cortex-M0 with this in mind.

5.3   Practical evaluation of symbolic execution using HolBA-SE
For application in practical automated verification tasks related to binary code,
a symbolic executor needs to be fast and scalable enough to handle hundreds of
instructions with complex control flow. To achieve this, we developed optimized
executors for RISC-V and ARM Cortex-M0 and integrated them with the SMT
solver Z3 [23], letting it discharge conditions that are BIR expressions, constant
program memory lookups and symbolic value concretizations. This approach in-
creases the TCB, but we believe the trade-off is attractive since the performance
boost is considerable and the scope of discharged conditions is restricted.


            Program Description                      #Instrs Time
            aes-unopt AES cipher, -O0 optimization       310 71.38 s
            aes         AES cipher, -O1 optimization     130 6.84 s
            chacha20 ChaCha20 cipher                     177 46.28 s
            incr        increment variable                 1 0.04 s
            isqrt       integer square root                6 0.12 s
            kernel-trap S3K kernel trap routines          79 9.21 s
            mod2        modulo two computation             1 0.09 s
            modexp      modular exponentiation            10 0.26 s
            motor_set nested calls and branching          66 3.94 s
            swap        swap memory location               5 0.19 s

Table 1: RISC-V programs and their symbolic execution running times. The
number of instructions are for instructions processed during symbolic execution.


    To investigate performance and scalability in practice, we applied our sym-
bolic executor for RISC-V to a collection of disassembled binaries and measured
the time to generate a progress structure theorem; the results are shown in Ta-
ble 1. All experiments were run on an Intel Core i5-9600K with 32GB RAM. Per
the table, building HOL4 progress structure theorems for BIR programs corre-
sponding to disassembly with hundreds of instructions generally takes minutes
at most. Time increases with both the number of BIR instructions symbolically
executed and the store complexity, which refers to how much information needs
to be stored in the symbolic state. In ciphers where all output bits depend on
all input bits, expressions may be replicated many times in symbolic memory.


6     Application: Automated Verification of Functional
      Properties of RISC-V Binaries
We automated functional verification in HolBA-SE for RISC-V binaries by in-
tegrating symbolic execution with previous work on binary lifting to BIR [42]
16       Lindner et al.


            RISC-V             Source     0                 1
                                                Binary              Disassembly
            contract            code

                 7                                                        3
                                                                2
              BIR             Progress        BIR spec. &            RISC-V
            contract      6   structure   5    program      4         spec.

     Fig. 6: Binary analysis workflow using HolBA-SE; source code is optional.


and a theory of Hoare-style binary contracts [44]. The result is a workflow with
the steps below as illustrated in Fig. 6, supporting the RV64G instruction set
variant of RISC-V, a collection of uncompressed general 64-bit instructions [59].
As with most theorem prover based verification, the workflow is incomplete in
the sense that verification steps can fail without specifications being false.

0. Compilation: Compile a source program to a RV64G binary. This step is
   optional, but adjustments to compilation can affect verification.
1. Disassembly: Disassemble the RV64G binary.
2. Lifting: Transpile the disassembly to BIR and generate a HOL4 lifting the-
   orem connecting the BIR program to corresponding RV64G binary code.
3. RISC-V specification: Specify program boundaries inside disassembly and
   define pre- and post-conditions using the L3 model of RISC-V.
4. BIR specification: Translate RISC-V pre-conditions and post-conditions
   to BIR expressions and prove equivalence in HOL4.
5. Symbolic execution: Symbolically execute the BIR program in HOL4 ac-
   cording to the program boundaries and obtain a progress structure theorem.
6. Symbolic transfer: Prove a HOL4 contract theorem for the BIR program
   using the pre- and post-conditions via the progress structure theorem.
7. Backlifting: Prove a RISC-V contract theorem by way of the BIR contract
   theorem and the lifting theorem.

All steps except 3 and 4 (writing and translating specifications) are mostly or
fully automated. Steps 5, 6, and 7 are novel contributions.

6.1     Contract proof automation using symbolic execution
Steps 5 and 6 in the workflow in Fig. 6 crucially rely on sound progress struc-
tures produced by symbolic execution to prove Hoare-style contracts for BIR
programs. The idea is that since our approach allows overapproximation, we can
use a progress structure to establish a postcondition Q starting from a precon-
dition P , but we cannot in general guarantee that it is the strongest one. The
following theorem connects progress structures and Hoare-style contracts.
Theorem 2. Given ⊢ s ⇝L Π, let L̄ be the complement of L. Then, if
                                                                                  H
 – for every s if pc(s) = pc(s) and P (s) then there exists H such that s ▷ s
                    Forward Symbolic Execution for Binary Code Verification       17

        # include < stdint .h >
        uint64_t incr ( uint64_t i ) { return i + 1; }

        incr :      file format elf64 - littleriscv
        Disassembly of section .text :
        0000000000010488 < incr >:
           10488:         00150513                  addi       a0 , a0 ,1
           1048 c :       00008067                  ret

        Definition riscv_incr_pre_def : (* RISC - V precondition *)
         riscv_incr_pre ( pre_x10 : word64 ) ( m : riscv_state ) : bool =
         ( m . c_gpr m . procID 10 w = pre_x10 )
        End
        Definition riscv_incr_post_def : (* RISC - V postcondition *)
         riscv_incr_post ( pre_x10 : word64 ) ( m : riscv_state ) : bool =
         ( m . c_gpr m . procID 10 w = pre_x10 + 1 w )
        End

        Theorem riscv_cont_incr : (* RISC - V contract *)
         riscv_cont incr_progbin 0 x10488w {0 x1048cw }
          ( riscv_incr_pre pre_x10 ) ( riscv_incr_post pre_x10 )


Fig. 7: Example verified program that increments a 64-bit unsigned integer rep-
resented in C (top), corresponding RV64G disassembly (below top), and RISC-V
specification (below disassembly) and contract theorem in HOL4 (bottom).


                H                    H
 – for every s ▷ s, s′ ∈ Π, and s′ ▶ s′ if P (s) then Q(s′ )
 – for every s′ ∈ Π, pc(s′ ) ∈ L̄ holds,
we have that for every state such that pc(s) = l and P (s) there is a state s′ and
an n > 0 such that s →nL s′ , pc(s′ ) ∈ L̄, and Q(s′ ).

6.2   Workflow example
To explain the steps in our workflow, we use the example defined in Fig. 7, which
includes a simple program incr that increments its argument by one.
    For step 0, compilation, our toolchain and workflow only require a RV64G
binary. However, we expect many users to perform binary analysis on programs
for which they have source code, enabling control over optimizations which can
affect binary size. Fig. 7 (top) shows the source for the example. In step 1,
we disassemble RV64G binaries using gnu-objdump for further processing. The
middle box in Fig. 7 shows our example’s disassembly. This step is not strictly
necessary, since lifting can be performed directly on the binary, but we found
disassembly useful as a reference for specification. For step 2, lifting, HolBA-SE
parses the disassembly using specifications of program bounds (address of initial
instruction and address after final instruction to lift) and translates the indicated
input into a BIR program inside HOL4 along with a lifting theorem connecting
input and output. For step 3, RISC-V specification, we express binary contracts
as pairs of pre- and postconditions in HOL4 using the riscv machine state type
defined by the L3 model, as illustrated in the middle of Fig. 7, where a0 is the
18     Lindner et al.

standardized application binary interface (ABI) name of the register x10. Hence,
the postcondition says that register a0 is incremented by one.
    For step 4, BIR specification, we manually translate RISC-V pre- and post-
conditions to BIR to enable symbolic execution. Using the BIR specification, we
symbolically execute the BIR program and perform transfer and backlifting (steps
5, 6, and 7). We use the BIR precondition as a path condition and leverage the
progress structure theorem to automatically prove a BIR contract via Theorem 2,
and finally obtain a RISC-V contract, as shown in the lowermost parts of Fig. 7.
The contract primitive riscv_cont was defined in earlier work [44] and uses the
HOL4 representation of the increment program disassembly (incr_progbin).


6.3   Case studies

To validate that HolBA-SE can be used to verify real-world RISC-V binaries, we
performed case studies for two high-assurance system software domains: cryp-
tography (ChaCha20 encryption) and operating systems (S3K trap functions).
ChaCha20 encryption. ChaCha20 is a stream cipher that performs twenty
rounds of the ChaCha algorithm as defined by Bernstein [8, 48]. We obtained
a ChaCha20 binary by compiling a reference implementation in C using GCC
with optimization level O1. We focused on specifying and verifying the byte
encryption loop body of the ChaCha20 binary, taking inspiration from similar
specifications in hacspec [9]. We abstractly define a ChaCha round in HOL4
as a transformation of 16 variables holding unsigned 32-bit words (array in the
source code), built up from lines that update two variables at a time using word
addition, XOR (??), and left rotation (#<<~):
chacha_line a b c d s ( m : word32 -> word32 ) =
 let m = ( a =+ ( m a ) + ( m b )) m in
 let m = ( d =+ (( m d ) ?? ( m a )) # < <~ s ) m in m

Our verification of byte encryption establishes the connection between this high-
level specification in HOL4 (updating the “memory function” m) and how the loop
body of the RISC-V binary behaves, as in functional translation validation. The
verification process took around 4 minutes on the machine described in Sec. 5.3.
S3K trap functions. S3K is an open source capability-based separation kernel
targeting embedded RISC-V systems [36]. Practically, S3K manages a collection
of user processes and ensures that they adhere to given restrictions on execution
time (slices), memory access, and interprocess communication. We specified and
verified two key handwritten RISC-V assembly routines from S3K: trap_entry
and trap_exit. The routine trap_entry is entered when the user process is
interrupted or an exception is encountered. It loads a pointer to the process’s
process control block (PCB) from the special mscratch RISC-V register, and
then stores the user process’s context (general purpose registers) to the PCB.
The routine trap_exit is entered when the kernel resumes a user process. It
loads the user process’s context from the PCB, replacing register values with the
values from the PCB. We obtained disassembly for the routines from the S3K
                  Forward Symbolic Execution for Binary Code Verification     19

author, consisting of 81 instructions. After adjusting lifting for special RISC-V
instructions such as csrrw, we expressed routine contracts in terms of assignment
of registers to memory locations (trap_entry), and assignments of memory lo-
cations to registers (trap_exit). The S3K author validated our specifications,
and we then translated them to BIR manually and performed the verification
process separately for each routine, which took around 7 minutes in total on the
machine described in Sec. 5.3.


7     Application: Execution Time Bounds for Cortex-M0

The ARM Cortex-M0 processor allows for predictable execution times, due to
lack of caches and a very short three-stage pipeline. According to the reference
manual [2], ALU instructions take 1 cycle, while memory interactions take 1
extra cycle and control flow changes take 2 extra cycles. The Cortex-M0 formal
model in HOL4 [26] maintains a clock cycle counter for this.


7.1   Representing execution time in BIR

To accommodate this simple timing model, BIR programs increment a cycle
counter variable c with the execution time needed by the instructions. Through-
out symbolic execution, the cycle counter is an incrementing constant value along
each execution path. When paths are merged, the cycle counter is approximated
as an interval, where the bounds are encoded in the path condition, linked to
the symbolic store by a free symbol. For example, the cycle counter interval
[αc + 5, αc + 8] consists of c 7→ α′ in the store and the path condition conjunct
αc + 5 ≤ α′ ≤ αc + 8. The interval for the cycle counter corresponds to the sound
best-case and worst-case execution time bounds, or BCET and WCET for short.
    The example program in Fig. 2 contains two conditional jumps: line 6 and
line 10. The latter is for the loop iteration and is executed exactly 32 times,
contributing a constant execution time. The former depends on the bits of R0,
where taking the branch skips line 7. When executing as in Sec. 4.3, the two
paths through the loop body have constant execution time and merge into an
interval. During composition and instantiation, the interval bounds are added
together accordingly. Interestingly, equality of lower and upper bounds proves
the absence of timing side channels. While the example program is not free of
side channels, we can make its execution time independent of R0, e.g., balancing
the execution times of the loop body branches by inserting nops.


7.2   Evaluation

We curated a set of evaluation programs, which we compiled with GCC unopti-
mized (except for the one marked with o3 and the assembly program ldldbr8),
tested on hardware, and then analyzed using both AbsInt aiT and HolBA-SE;
the results are presented in Table 2. Concerning choice of programs, ldldbr8 is a
20      Lindner et al.

           Program             Testing  aiT     HolBA-SE
name         #instrs #splits BCET WCET WCET BCET WCET eval
ldldbr8             34        0      60      60      55†       60    60∗       1s
aes                543        1    3761    3761    3761†     3761 3761∗ 8.4 min
modexp             130       11   54358   93540   197721    43704 197560 11.4 min
- uidivmod          85        9    1362    1778     3062     1332   3060 5.9 min
motor_set          165        6     272     280      283      264    280      49 s
motor_set o3       112       12      73      91      92†       68     96      89 s
pid               2257      294    4589    5483     7521     1849   7529 61.8 min
- fadd             401       70      77     155      188       68    178 12.4 min
- fdiv             287       34     118     541      640       87    591 14.5 min
Table 2: Per program, the number of binary instructions, where splits are con-
ditional or indirect jumps, BCET and WCET values are in clock cycles, and aiT
only provides WCET. † indicates unsound result and ∗ indicates constant time.


manually constructed counterexample to aiT soundness, aes showcases constant-
time proofs via overapproximation to avoid state size explosion due to loops,
modexp is the running example from Sec. 2.2, and motor_set and pid exemplify
embedded applications where execution time may be an important factor.
    Testing a program consists of generating 1000 random input states and col-
lecting observed BCET and WCET when executing on an STM32F051R8T6
chip measuring the clock cycles using the processor SysTick timer. We use Ab-
sInt aiT [1] that is part of AbsInt a3 for ARM Version 22.04. It is based on
abstract interpretation and is the industry standard for obtaining safe WCET
bounds with static analysis, but does not provide BCET values. For evaluations,
aiT runs within 4 s for each program. Testing and HolBA-SE count cycles as
in the ARM specification of execution time for Cortex-M0 [2], starting after the
first instruction has been fetched and decoded. The aiT tool instead assumes an
initially empty pipeline, adding two or more clock cycles its analysis.
    Program ldldbr8 consists of a sequence of 8 blocks, where each block is
two loads and an unconditional branch to the next block, and a final nop. As
there is trivially only one path (no splits), execution time is constant. The result
illustrates that the pipeline in aiT can produce unsound results, and in con-
trast, the model in HOL4 is precise. Further experiments have revealed that the
pipeline modeled in aiT is not equivalent to the Cortex-M0 pipeline. This has
been confirmed with AbsInt along with the unsound result indicated with a † in
the table, which subsequently has been fixed in aiT. Considering the different
cycle counting of aiT, the programs aes and motor_set o3 also represent coun-
terexamples to the aiT analysis. However, HolBA-SE proves constant execution
time for ldldbr8 and aes, indicated using ∗ .
    Generally, the results of aiT and the symbolic execution are relatively similar.
The program motor_set is as in Sec. 5.3, aes performs AES encryption with
10 rounds, modexp is the example from Sec. 2.2, and pid is a larger case study
for analyzing a compiled PID controller. Since our processor does not support
division and modulo, modexp uses the inefficient but easily analyzable emulation
                   Forward Symbolic Execution for Binary Code Verification       21

function uidivmod. Similarly, pid uses 11 floating-point operation emulation
functions, provided as precompiled binaries with intricate control flows, like fadd
and fdiv.


8   Related Work
Symbolic execution [5, 50] was first introduced in the context of software testing
by King [38] and applied to formal verification in follow-up work [30]. Sub-
sequently, it became widely used in both testing [22, 4, 52, 13] and verifica-
tion [20, 14]. Concolic execution [27, 55] underapproximates for performance
and targets bug-finding, whereas we target verification and maintain soundness.
    Our core rules (Sec. 4.3) support standard techniques for making symbolic
execution scalable. Array axiomatization [24, 18, 13] can flatten memory, en-
abling load–store bypassing and eliminating overwritten stores, curbing expres-
sion growth and solver load. Constant propagation reduces term size, while in-
terval abstractions approximate expressions by bounded values [15, 13, 29]. State
merging mitigates path explosion [40], akin to widening in abstract interpreta-
tion [15]. Interpolation reuses results by relaxing initial path conditions without
introducing new paths [35] and value analysis can resolve indirect jumps [37].
    In the context of binary verification, symbolic execution underpins transla-
tion validation [16, 34, 21], validation of compiler optimizations [56], analysis of
side-channel absence [18, 19], and test generation to validate side-channel mod-
els [47, 11], and data-flow/overflow analysis [57]. Many implementations rely on
intermediate languages for architectural independence [10, 57, 13] but do not
offer the theorem prover based trustworthiness of HolBA-SE.
    Mazzucato et al. [46] perform automated proofs in HOL Light of relational
properties of ARMv8 and x86 machine code using Hoare logic. In their work,
symbolic execution is one of many possible proof tactics; we provide a general
symbolic execution theory independent of program logics and focus on proof au-
tomation for an intermediate language. Sammler et al. [51] import traces from
SMT-based symbolic execution of binary code into Coq for reasoning; in con-
trast, our symbolic execution produces certified theorems inside HOL4. Previous
works typically use weakest preconditions to verify functional properties of un-
structured code [7, 44, 6], while our approach uses strongest postconditions.
    WCET is fundamental in high assurance domains [12, 58, 54, 49, 39, 3].
While we target a simple microarchitecture, prior work also abstracts com-
plex timing features (e.g., caches, pipelines) to enable sound analysis [31, 41].
Maroneze et al. extend the verified CompCert compiler with a verified loop-
bound estimation [45]. However, they restrict to having a constant for WCET
per instruction, which introduces overapproximation with our timing model.


9   Conclusion
We presented a theory of symbolic execution for unstructured programs suitable
for theorem prover use. The theory builds on inference rules that are the basis
22      Lindner et al.

of automated symbolic executors with common optimizations and adaptations
for code using specific ISAs. We instantiated the theory for the BIR language,
providing machine-checked proofs of soundness of symbolic execution of BIR in
HOL4. Applications of our implementation [43] demonstrate proof automation
in several case studies. Scaling further is possible via binary slicing and modular
verification, but automation of such approaches is left to future work.


Acknowledgments The authors thank Henrik Karlsson and Didrik Lundberg
for their help with HolBA-SE case studies. This work was partially supported
by the Wallenberg AI, Autonomous Systems and Software Program (WASP)
funded by the Knut and Alice Wallenberg Foundation and a gift from Intel.


References

 1. aiT Worst-Case Execution Time Analyzers. https://www.absint.com/ait/index.
    htm, accessed: 2022-12-23
 2. Cortex-M0 Technical Reference Manual r0p0 - Instruction set summary.
    https://developer.arm.com/documentation/ddi0432/c/programmers-model/
    instruction-set-summary, accessed: 2022-12-23
 3. Abella, J., Hernandez, C., Quiñones, E., Cazorla, F.J., Conmy, P.R., Azkarate-
    askasua, M., Perez, J., Mezzetti, E., Vardanega, T.: WCET analysis methods: Pit-
    falls and challenges on their trustworthiness. In: International Symposium on In-
    dustrial Embedded Systems. pp. 1–10 (2015). https://doi.org/10.1109/SIES.2015.
    7185039
 4. Avgerinos, T., Rebert, A., Cha, S.K., Brumley, D.: Enhancing symbolic execu-
    tion with Veritesting. In: International Conference on Software Engineering. p.
    1083–1094 (2014). https://doi.org/10.1145/2568225.2568293
 5. Baldoni, R., Coppa, E., D’elia, D.C., Demetrescu, C., Finocchi, I.: A survey of
    symbolic execution techniques. ACM Comput. Surv. 51(3) (May 2018). https:
    //doi.org/10.1145/3182657
 6. Barnett, M., Leino, K.R.M.: Weakest-precondition of unstructured programs. In:
    Workshop on Program Analysis for Software Tools and Engineering. pp. 82––87
    (2005). https://doi.org/10.1145/1108792.1108813
 7. Barthe, G., Rezk, T., Saabas, A.: Proof obligations preserving compilation. In:
    Formal Aspects in Security and Trust. pp. 112–126 (2006). https://doi.org/10.
    1007/11679219_9
 8. Bernstein, D.J.: Chacha, a variant of Salsa20. In: Workshop Record of SASC, vol.
    8. pp. 3–5 (2008), http://cr.yp.to/chacha/chacha-20080128.pdf
 9. Bhargavan, K., Kiefer, F., Strub, P.Y.: hacspec: Towards verifiable crypto stan-
    dards. In: International Conference of Security Standardisation Research. pp. 1–20
    (2018). https://doi.org/10.1007/978-3-030-04762-7_1
10. Brumley, D., Jager, I., Avgerinos, T., Schwartz, E.J.: BAP: A binary analysis plat-
    form. In: Computer Aided Verification. pp. 463–469 (2011). https://doi.org/10.
    1007/978-3-642-22110-1_37
11. Buiras, P., Nemati, H., Lindner, A., Guanciale, R.: Validation of side-channel mod-
    els via observation refinement. In: International Symposium on Microarchitecture.
    p. 578–591 (2021). https://doi.org/10.1145/3466752.3480130
                    Forward Symbolic Execution for Binary Code Verification          23

12. Byhlin, S., Ermedahl, A., Gustafsson, J., Lisper, B.: Applying static WCET analy-
    sis to automotive communication software. In: Euromicro Conference on Real-Time
    Systems. pp. 249–258 (2005). https://doi.org/10.1109/ECRTS.2005.7
13. Cha, S.K., Avgerinos, T., Rebert, A., Brumley, D.: Unleashing mayhem on binary
    code. In: Symposium on Security and Privacy. pp. 380–394 (2012). https://doi.
    org/10.1109/SP.2012.31
14. Coen-Porisini, A., Denaro, G., Ghezzi, C., Pezzé, M.: Using symbolic execution for
    verifying safety-critical systems. In: European Software Engineering Conference.
    pp. 142–151 (2001). https://doi.org/10.1145/503209.503230
15. Cousot, P.: Abstract interpretation. ACM Comput. Surv. 28(2), 324–328 (Jun
    1996). https://doi.org/10.1145/234528.234740
16. Currie, D., Feng, X., Fujita, M., Hu, A.J., Kwan, M., Rajan, S.: Embedded software
    verification using symbolic execution and uninterpreted functions. International
    Journal of Parallel Programming 34(1), 61–91 (2006). https://doi.org/10.1007/
    s10766-005-0004-8
17. Dahl, O.J., Dijkstra, E.W., Hoare, C.A.R. (eds.): Structured programming. Aca-
    demic Press Ltd. (1972)
18. Daniel, L.A., Bardin, S., Rezk, T.: Binsec/Rel: Efficient relational symbolic exe-
    cution for constant-time at binary-level. In: Symposium on Security and Privacy.
    pp. 1021–1038 (2020). https://doi.org/10.1109/SP40000.2020.00074
19. Daniel, L.A., Bardin, S., Rezk, T.: Hunting the Haunter–efficient relational sym-
    bolic execution for Spectre with Haunted RelSE. In: Network and Distributed
    Systems Security (2021). https://doi.org/10.14722/ndss.2021.24286
20. Dannenberg, R., Ernst, G.: Formal program verification using symbolic execution.
    IEEE Transactions on Software Engineering SE-8(1), 43–52 (1982). https://doi.
    org/10.1109/TSE.1982.234773
21. Dasgupta, S., Dinesh, S., Venkatesh, D., Adve, V.S., Fletcher, C.W.: Scalable val-
    idation of binary lifters. In: Conference on Programming Language Design and
    Implementation. pp. 655–671 (2020). https://doi.org/10.1145/3385412.3385964
22. David, R., Bardin, S., Feist, J., Mounier, L., Potet, M.L., Ta, T.D., Marion, J.Y.:
    Specification of concretization and symbolization policies in symbolic execution.
    In: International Symposium on Software Testing and Analysis. pp. 36––46 (2016).
    https://doi.org/10.1145/2931037.2931048
23. De Moura, L., Bjørner, N.: Z3: An efficient SMT solver. In: International Confer-
    ence on Tools and Algorithms for the Construction and Analysis of Systems. pp.
    337–340 (2008). https://doi.org/10.1007/978-3-540-78800-3_24
24. Farinier, B., David, R., Bardin, S., Lemerre, M.: Arrays made simpler: An efficient,
    scalable and thorough preprocessing. In: International Conference on Logic for
    Programming, Artificial Intelligence and Reasoning. vol. 57, pp. 363–380 (2018).
    https://doi.org/10.29007/dc9b
25. Fox, A.: Improved tool support for machine-code decompilation in HOL4.
    In: Interactive Theorem Proving. pp. 187–202 (2015). https://doi.org/10.1007/
    978-3-319-22102-1_12
26. Fox, A.: L3: A Specification Language for Instruction Set Architectures (Retrieved
    2025-11-17), https://acjf3.github.io/l3
27. Godefroid, P., Klarlund, N., Sen, K.: DART: Directed automated random testing.
    In: Conference on Programming Language Design and Implementation. pp. 213–
    223 (2005). https://doi.org/10.1145/1065010.1065036
28. Hamming, R.R.: Art of Doing Science and Engineering: Learning to Learn. CRC
    Press (1997). https://doi.org/10.1201/9781482283198
24      Lindner et al.

29. Hansen, T., Schachte, P., Søndergaard, H.: State joining and splitting for the sym-
    bolic execution of binaries. In: International Workshop on Runtime Verification.
    pp. 76–92 (2009). https://doi.org/10.1007/978-3-642-04694-0_6
30. Hantler, S.L., King, J.C.: An introduction to proving the correctness of programs.
    ACM Comput. Surv. 8(3), 331–353 (Sep 1976). https://doi.org/10.1145/356674.
    356677
31. Heckmann, R., Langenbach, M., Thesing, S., Wilhelm, R.: The influence of pro-
    cessor architecture on the design and the results of WCET tools. Proceedings of
    the IEEE 91(7), 1038–1054 (2003). https://doi.org/10.1109/JPROC.2003.814618
32. HOL development team: HOL interactive theorem prover, https:
    //hol-theorem-prover.org, retrieved 2025-11-17.
33. HolBA contributors: HolBA - Binary analysis in HOL, https://github.com/
    kth-step/HolBA, retrieved 2025-11-17.
34. Iosif-Lazar, A.F., Al-Sibahi, A.S., Dimovski, A.S., Savolainen, J.E., Sierszecki, K.,
    Wasowski, A.: Experiences from designing and validating a software modernization
    transformation. In: International Conference on Automated Software Engineering.
    pp. 597–607 (2015). https://doi.org/10.1109/ASE.2015.84
35. Jaffar, J., Murali, V., Navas, J.A., Santosa, A.E.: Tracer: A symbolic execution
    tool for verification. In: Computer Aided Verification. pp. 758–766 (2012). https:
    //doi.org/10.1007/978-3-642-31424-7_61
36. Karlsson, H.A.: S3K: Capability based separation kernel for embedded RISC-V,
    https://github.com/kth-step/s3k, retrieved 2025-11-16.
37. Kinder, J., Zuleger, F., Veith, H.: An abstract interpretation-based framework
    for control flow reconstruction from binaries. In: International Conference on
    Verification, Model Checking, and Abstract Interpretation. pp. 214–228 (2009).
    https://doi.org/10.1007/978-3-540-93900-9_19
38. King, J.C.: Symbolic execution and program testing. Commun. ACM 19(7), 385–
    394 (Jul 1976). https://doi.org/10.1145/360248.360252
39. Kirner, R., Puschner, P.: Classification of WCET analysis techniques. In: Inter-
    national Symposium on Object-Oriented Real-Time Distributed Computing. pp.
    190–199 (2005). https://doi.org/10.1109/ISORC.2005.19
40. Kuznetsov, V., Kinder, J., Bucur, S., Candea, G.: Efficient state merging in sym-
    bolic execution. In: Conference on Programming Language Design and Implemen-
    tation. p. 193–204 (2012). https://doi.org/10.1145/2254064.2254088
41. Li, X., Roychoudhury, A., Mitra, T.: Modeling out-of-order processors for WCET
    analysis. Real-Time Syst. 34(3), 195–227 (nov 2006). https://doi.org/10.1007/
    s11241-006-9205-5
42. Lindner, A., Guanciale, R., Metere, R.: TrABin: Trustworthy analyses of binaries.
    Science of Computer Programming 174, 72–89 (2019). https://doi.org/10.1016/j.
    scico.2019.01.001
43. Lindner, A., Palmskog, K., Lundberg, D.: HolBA-SE (Nov 2025). https://doi.org/
    10.5281/zenodo.15043917
44. Lundberg, D., Guanciale, R., Lindner, A., Dam, M.: Hoare-style logic for un-
    structured programs. In: Software Engineering and Formal Methods. pp. 193–213
    (2020). https://doi.org/10.1007/978-3-030-58768-0_11
45. Maroneze, A., Blazy, S., Pichardie, D., Puaut, I.: A formally verified WCET esti-
    mation tool. In: International Workshop on Worst-Case Execution Time Analysis.
    vol. 39, pp. 11–20 (2014). https://doi.org/10.4230/OASIcs.WCET.2014.11
46. Mazzucato, D., Mohamed, A., Lee, J., Barrett, C., Grundy, J., Harrison, J.,
    Păsăreanu, C.S.: Relational Hoare logic for realistically modelled machine code.
                    Forward Symbolic Execution for Binary Code Verification           25

    In: Computer Aided Verification. pp. 389–413 (2025). https://doi.org/10.1007/
    978-3-031-98668-0_19
47. Nemati, H., Buiras, P., Lindner, A., Guanciale, R., Jacobs, S.: Validation of ab-
    stract side-channel models for computer architectures. In: Computer Aided Verifi-
    cation. pp. 225–248 (2020). https://doi.org/10.1007/978-3-030-53288-8_12
48. Nir, Y., Langley, A.: ChaCha20 and Poly1305 for IETF Protocols. RFC 8439 (Jun
    2018). https://doi.org/10.17487/RFC8439
49. Nowotsch, J., Paulitsch, M.: Leveraging multi-core computing architectures in
    avionics. In: European Dependable Computing Conference. pp. 132–143 (2012).
    https://doi.org/10.1109/EDCC.2012.27
50. Păsăreanu, C.S., Visser, W.: A survey of new trends in symbolic execution for
    software testing and analysis. Int. J. Softw. Tools Technol. Transfer 11(4), 339–
    353 (2009). https://doi.org/10.1007/s10009-009-0118-1
51. Sammler, M., Hammond, A., Lepigre, R., Campbell, B., Pichon-Pharabod, J.,
    Dreyer, D., Garg, D., Sewell, P.: Islaris: verification of machine code against au-
    thoritative ISA semantics. In: International Conference on Programming Language
    Design and Implementation. p. 825–840 (2022). https://doi.org/10.1145/3519939.
    3523434
52. Saxena, P., Poosankam, P., McCamant, S., Song, D.: Loop-extended symbolic exe-
    cution on binary programs. In: International Symposium on Software Testing and
    Analysis. p. 225–236 (2009). https://doi.org/10.1145/1572272.1572299
53. Sewell, T.A.L., Myreen, M.O., Klein, G.: Translation validation for a verified OS
    kernel. In: Conference on Programming Language Design and Implementation. pp.
    471–482 (2013). https://doi.org/10.1145/2491956.2462183
54. Souyris, J., Pavec, E.L., Himbert, G., Borios, G., Jégu, V., Heckmann, R.: Comput-
    ing the worst case execution time of an avionics program by abstract interpretation.
    In: International Workshop on Worst-Case Execution Time Analysis. vol. 1, pp.
    21–24 (2007). https://doi.org/10.4230/OASIcs.WCET.2005.810
55. Stephens, N., Grosen, J., Salls, C., Dutcher, A., Wang, R., Corbetta, J., Shoshi-
    taishvili, Y., Kruegel, C., Vigna, G.: Driller: Augmenting fuzzing through selec-
    tive symbolic execution. In: Network and Distributed System Security Symposium
    (2016). https://doi.org/10.14722/ndss.2016.23368
56. Tristan, J.B., Leroy, X.: Formal verification of translation validators: A case study
    on instruction scheduling optimizations. In: Symposium on Principles of Program-
    ming Languages. pp. 17–27 (2008). https://doi.org/10.1145/1328438.1328444
57. Wang, T., Wei, T., Lin, Z., Zou, W.: Intscope: Automatically detecting integer
    overflow vulnerability in X86 binary using symbolic execution. In: Network and
    Distributed System Security Symposium (2009)
58. Wartel, F., Kosmidis, L., Lo, C., Triquet, B., Quiñones, E., Abella, J., Gogonel, A.,
    Baldovin, A., Mezzetti, E., Cucu, L., Vardanega, T., Cazorla, F.J.: Measurement-
    based probabilistic timing analysis: Lessons from an integrated-modular avionics
    case study. In: International Symposium on Industrial Embedded Systems. pp.
    241–248 (2013). https://doi.org/10.1109/SIES.2013.6601497
59. Waterman, A., Lee, Y., Patterson, D.A., Asanović, K.: The RISC-V instruction set
    manual, volume I: User-level ISA, version 2.1. Tech. Rep. UCB/EECS-2016-118,
    EECS Department, University of California, Berkeley (May 2016), https://www2.
    eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-118.pdf
60. Zhao, L., Li, G., De Sutter, B., Regehr, J.: ARMor: fully verified software fault
    isolation. In: International Conference on Embedded Software. pp. 289–298 (2011).
    https://doi.org/10.1145/2038642.2038687
