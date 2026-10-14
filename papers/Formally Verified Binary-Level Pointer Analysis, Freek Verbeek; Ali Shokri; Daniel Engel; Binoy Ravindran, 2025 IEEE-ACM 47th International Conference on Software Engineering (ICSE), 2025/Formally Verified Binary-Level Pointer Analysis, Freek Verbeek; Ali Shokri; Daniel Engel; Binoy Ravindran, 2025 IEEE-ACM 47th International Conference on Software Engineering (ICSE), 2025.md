                                               Formally Verified Binary-level Pointer Analysis
                                                                            Freek Verbeek∗† , Ali Shokri† , Daniel Engel∗, Binoy Ravindran†
                                                                                            ∗ Open Universiteit, Heerlen, The Netherlands

                                                                                             Email: {freek.verbeek, daniel.engel}@ou.nl
                                                                                               † Virginia Tech, Blacksburg, VA, USA

                                                                                              Email: {freek, ashokri, binoy}@vt.edu


                                                                                                                           abstraction everything is a pointer. There are no variables,
                                            Abstract—Binary-level pointer analysis can be of use in                        and memory can be considered as a flat unstructured address
arXiv:2501.17766v1 [cs.SE] 29 Jan 2025




                                         symbolic execution, testing, verification, and decompilation of                   space. In a typical x86-64 program, about 28% of all assembly
                                         software binaries. In various such contexts, it is crucial that
                                         the result is trustworthy, i.e., it can be formally established                   instructions write to memory1, producing tens of thousands of
                                         that the pointer designations are overapproximative. This paper                   pointers even in medium-sized programs. Moreover, control-
                                         presents an approach to formally proven correct binary-level                      flow related information is stored in writable memory, such as
                                         pointer analysis. A salient property of our approach is that                      the current return address and the currently caught exception
                                         it first generically considers what proof obligations a generic                   stack. Theoretically, if the destination of even a single memory
                                         abstract domain for pointer analysis must satisfy. This allows
                                         easy instantiation of different domains, varying in precision,                    write cannot be resolved, then the effect of executing that
                                         while preserving the correctness of the analysis. In the trade-                   memory write could result in either thrashing all memory
                                         off between scalability and precision, such customization allows                  (including such control-flow pertinent information) or forking
                                         “meaningful” precision (sufficiently precise to ensure basic sanity               into unrealistic states, such as when a memory write overlaps
                                         properties, such as that relevant parts of the stack frame are                    with the return address, even though in reality it did not. This
                                         not overwritten during function execution) while also allowing
                                         coarse analysis when pointer computations have become too                         may lead to a situation where it cannot even be established
                                         obfuscated during compilation for sound and accurate bounds                       what instruction is to be executed, let alone what an accurate
                                         analysis. We experiment with three different abstract domains                     next state can be. This is one of the key challenges in dealing
                                         with high, medium, and low precision. Evaluation shows that                       with binaries, preventing one from simply using techniques
                                         our approach is able to derive designations for memory writes                     developed for source code analysis and applying them to low-
                                         soundly in COTS binaries, in a context-sensitive interprocedural
                                         fashion.                                                                          level code found in binary executables [15].
                                            Index Terms—binary analysis, pointer analysis, formal meth-                       This paper presents an approach to formally verified binary-
                                         ods                                                                               level pointer analysis. Typically, such analyses are based on a
                                                                                                                           form of abstract interpretation [12], where an abstract domain
                                                                   I. I NTRODUCTION                                        is defined that overapproximates concrete semantics [5], [35].
                                            Pointer analysis is central to various forms of verification                   A fundamental challenge is choosing the “right” abstract
                                         and analysis for software containing pointers, facilitating the                   domain, as this essentially boils down to balancing precision
                                         construction of a state-based semantic model of software [10],                    vs. scalability. This paper thus first leaves the abstract domain
                                         [30], [1], [17], [38], [42]. It aims to statically resolve, for any               polymorphic and formulates a set of eight generic to-be-
                                         pointer in a given program, which region of the memory it                         refined functions, as well as the proof obligations that these
                                         may point to. Specifically, given any two pointers, it must be                    functions must satisfy. Over these generic functions, an exe-
                                         known whether they are aliasing, always referring to separate                     cutable algorithm for pointer analysis is formalized and proven
                                         regions in memory, or if they may possibly overlap. If a value                    correct. An instantiation thus defines an abstract domain and
                                         is written to memory, and no pointer information is known,                        an implementation of the generic functions. Any instantiation
                                         then one cannot accurately describe what the next state will                      that satisfies the proof obligations automatically constitutes a
                                         be. This can lead to overapproximative thrashing parts of the                     formally proven correct binary-level pointer analysis. As will
                                         memory state or forking, i.e., to conservatively considering                      be discussed later, all the formalism and proofs are carried out
                                         both separation and aliasing possibilities. Both such cases are                   in Isabelle/HOL and have been shared with the readers.
                                         undesirable as they will quickly lead to unrealistic states and                      We then provide three different instantiations of our generic
                                         path explosions. In other words, pointer analysis is a necessity                  functions, each of which strikes a different balance in the
                                         for building a state-based transition system that accurately                      trade-off between precision vs. scalability. First, pointer com-
                                         models the software under investigation. Such a model, then,                      putations form an abstract domain that keeps track of how
                                         typically precedes a verification or analysis effort aimed at                     pointers were computed: highly precise, but in practice one
                                         higher-level properties.                                                          must cap the domain to a given size and produce top (⊤) when
                                            The necessity for pointer analysis immensely exacerbates
                                         when dealing with binaries (i.e., machine or assembly code)                          1 Measured over several CoreUtils binaries and Firefox libraries with
                                         instead of source code. The reason is that at this level of                       different levels of optimization.



                                         ©2025 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
                                         reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or
                                         reuse of any copyrighted component of this work in other works.
that cap is exceeded. Second, pointer bases form an abstract        or assume alignment of regions. This paper aims to reduce the
domain where each pointer is represented only by its pointer        trusted code base by explicitizing such assumptions and either
base (e.g., a stack pointer, or the return value of a malloc):      proving them through invariants or reporting them explicitly
more coarse as it cannot be used for alias analysis, but still      otherwise. The trusted code base is thus reduced to the validity
allows accurate separation analysis (for binaries compiled          of explicit and configurable assumptions such as “regions
from source code, pointers based in different blocks can be         based on stack pointers of different functions are assumed to
assumed to be separate, even if an out-of-bounds occurs [31]).      be separate”.
Third, pointer sources are an abstract domain where a pointer          Limitations, assumptions and scope. A major assumption
is modeled by the set of sources (e.g., user inputs, initial        behind our approach is the treatment of partially overlapping
parameter values) used in its computation. This is highly           memory accesses. Memory accesses (reads or writes) to par-
coarse, but is scalable and still allows a form of separation       tially overlapping regions may happen, but we assume that
reasoning.                                                          they do not concern pointers. More details can be found in
   The pointer analysis presented in this paper is context-         Section III-A. Moreover, our approach has been implemented
sensitive and compositional. Context-sensitivity is desirable,      for the x86-64 architecture and does not deal with concurrency.
since pointers are passed through from function to function.        A fundamental limitation is that not all indirections may be
We derive function preconditions, which states that invariably      resolved, which may lead to unexplored paths.
a certain function is always called within in a context where,         The approach has been formally proven correct in Is-
e.g., register rdi contains a heap-pointer, or register rsi         abelle/HOL [36], [14], and has been mirrored in Haskell for
contains a pointer to within the stack frame of the caller.         experimental results. These confirm soundness relative to a
Per function, we can then derive a function postcondition that      ground truth obtained by observing executions. Moreover, they
summarizes which regions were written to/read from by the           show precision comparable to or improved upon the state-
function, and if after termination abstract pointers are left       of-the-art. We evaluate the effect of interprocedural bottom-
in return registers or global variables. Compositionally, these     up pointer analysis with respect to resolving indirections,
summaries can then be used for pointer analysis for callers of      identifying 135 cases where context-sensitive information al-
summarized functions. Due to space limitation, we focus our         lowed resolving a function callback. Finally, for all analyzed
presentation on intraprocedural analysis and do not expand on       functions it has been verified whether the result is sufficiently
the above technique for composition.                                precise to show that the return address has not been overwritten
   Bottom-up pointer analysis (i.e., binary analysis, in contrast   and that critical parts of the stack frame (e.g., storing non-
to top-down source code analysis) can be useful in various use      volatile register values) are unmodified during execution of
cases (see Section VI):                                             the function. This was successful for 99.6% of all analyzed
                                                                    functions.
• It can be integrated into a disassembly algorithm [37]. A
                                                                       In summary, we contribute:
  large facet of disassembly is assessing which instruction
                                                                    • A formally proven correct approach to binary-level pointer
  addresses are reachable (i.e., control flow recovery). A
                                                                       analysis that leaves the abstract domain generic, allowing
  key challenge is resolving indirections, i.e., dynamically
                                                                       easy development of instantiations with different character-
  computed control flow transfers. Context-sensitive pointer
                                                                       istics (e.g., different levels of preciseness);
  analysis can assist, by providing information on which
                                                                    • An evaluation over roughly 1.4 million assembly instruc-
  pointers are passed to a function.
                                                                       tions, showing scalability and applicability of the approach.
• It can be a preliminary step to a decompilation effort [11].
                                                                       Section II studies the related work. Sections III and IV pro-
  Specifically, one of the steps in decompilation is to recover
                                                                    vide details of our generic functions and their three different
  variables. Bottom-up pointer analysis provides information
                                                                    levels of instantiation, respectively. Section V, demonstrates
  on which memory writes actually constitute variables.
                                                                    the realization of interprocedural pointer analysis through our
• It can be the base of a bottom-up dataflow analysis. The
                                                                    general functions. While Section VI looks at several use
  function summaries already provide a form of dataflow
                                                                    cases of the introduced approach, Section VII relates the
  analysis, by providing information on in- and output rela-
                                                                    experimental results to those produced by the state-of-the-art
  tions. They can be used to verify whether functions adhere
                                                                    tools currently available. Section VIII concludes the paper.
  to a calling convention and to see which state parts are
  overwritten or preserved by a given function. We also                                  II. R ELATED W ORK
  demonstrate by example that an overapproximative pointer             Source-level pointer analysis has been an active research
  analysis can be used for live variable analysis.                  field for decades [22]. Its typical use cases lie in top-down con-
   We emphasize the need for formally proven correct binary-        texts: it takes as input source code, and provides information
level pointer analysis. Symbolic treatment of pointers and          to the compiler for doing optimizations and data flow analyses.
memory is notoriously difficult. Existing approaches typically      We here do not aim to provide an overview of this field,
make various assumptions implicitly, e.g., they may implicitly      since our work focuses on bottom-up contexts: taking as input
assume a return address cannot be overwritten, assume sepa-         a binary, the result of pointer analysis provides information
ration between pointers based on heuristics or best practices,      usable for decompilation and verification.
   Generally, source-level approaches to program analysis             binary. Pointer aliasing is dealt with by thrashing the symbolic
cannot directly be applied to binary-level programs [6].              state [29]. Verbeek et al. present an overapproximative ap-
Various research therefore focuses on symbolic execution              proach to control flow reconstruction based on forking the state
and/or abstract interpretation specifically tailored to the binary    non-deterministically [43]. Their output can be exported to the
level. We distinguish underapproximative techniques from              Isabelle/HOL theorem prover where it can be formally proven
overapproximative ones. In this discussion, we specifically           correct. An important use case for overapproximative control
focus on how these techniques deal with pointers.                     flow reconstruction is trimming a binary by removing provably
   Underapproximative approaches:                                     unreachable code. B IN T RIMMER uses abstract interpretation
SAGE combines symbolic execution of assembly code with                to prove the reachability of dead code and trim the binary
fuzz testing, allowing exposure of real-life vulnerabilities in       accordingly.
real-life software [21]. Initially, SAGE did “not reason about           Using abstract interpretation for the purpose of control
symbolic pointer dereferences”, but it has been combined with         flow reconstruction (i.e., resolving of indirections) is different
Yogi allowing runtime behavior observed from test cases to            from using abstract interpretation for resolving designations
be used in refining abstractions to find whether pointers may         of memory writes (i.e., pointer analysis). It can be seen as a
be possibly aliasing [20]. S2 E is a platform for traversing          specific form of the more generic technique value set analysis
binaries, allowing exploration of hundreds of thousands of            (VSA).
paths using selective symbolic execution [9], [8]. S2 E provides         Value Set Analysis. Various approaches use abstract in-
an approach where dereferencing a symbolic pointer provides           terpretation to do VSA: mapping state parts to abstract rep-
next states with possible concrete values based on the symbolic       resentations of a set of values that the state part may hold
pointer and the current path constraints. A similar approach          at a certain program point. C ODESURFER / X 86 utilizes as
is taken by F UZZ BALL, a symbolic execution framework for            abstract domain a tuple storing a base and an offset [5], [39].
binaries, mainly concerned with improving the path coverage           The offset is modeled by an abstract domain that combines
of binary fuzzers [3], [33]. It explores individual paths one         intervals and congruences. Frameworks such as BAP [7] and
by one and chooses concrete values for offsets in pointers.           ANGR [41] provide implementations of binary-level VSA.
B INSEC is a code analysis tool with a focus on the security          Abstract domains are typically a form of signed-agnostic
properties of binaries [16], [13]. It has been applied to find        intervals [35]. To our knowledge, BinPointer [26] is the work
use-after-free bugs [18] and for reachability analyses [19].          closest related to the contribution in this paper. Kim et al.
Symbolic execution is based on forking, using an SMT solver           provide binary-level context-insensitive pointer analysis in a
to prune infeasible paths. B INSEC is based on bounded ver-           sound and overapproximative fashion, while also targeting
ification, making it underapproximative. Kapus et al. provide         scalability and evaluating preciseness of their produced out-
an interesting approach by concretizing and segmenting the            put. Their abstract domain is conceptually equivalent to the
memory model so that symbolic pointers can only refer to              “pointer bases” domain presented in this paper, which is also
single memory segments [24]. Use of a test harness ensures            similar to the abstract domain found in [5]. BinPointer reaches
both termination and that allocations always have a concrete          the conclusion of 100% soundness by running test-cases, while
size.                                                                 we reach 100% soundness through formal proofs.
   These methods underapproximate either by not exploring                Summary of relation to overapproximative approaches.
all paths, or by underapproximating pointer values. Underap-          Existing approaches use abstract interpretation to reconstruct
proximation typically is very well suited for finding bugs and        control flow, or to do VSA. It is a well-known issue that
vulnerabilities in software: it leads to few false negatives and      in realistic, optimized and stripped COTS binaries, computa-
provides excellent scalability. It is suitable in the context of      tions quickly become too complicated and obfuscated to be
testing and binary exploration. In contrast, our pointer analysis     amenable for VSA sufficiently precise to enable reasoning
is overapproximative, quantifying over all execution paths and        over separation [45]. This paper presents the first approach to
all values. This makes it suitable in the contexts of verification    VSA that is formally proven correct, that is generic wrt. the
and lifting to higher-level representations.                          abstract domain and that therefore allows different domains
   Overapproximative approaches:                                      with different levels of preciseness to be used. To the best
Control Flow Reconstruction. Overapproximative ap-                    of our knowledge, there exists no approach that can over-
proaches to binary analysis are generally based on a form of          approximatively assign pointer designations to virtually all
abstract interpretation. Many approaches are aimed at control         memory writes in large COTS binaries, in a context-sensitive
flow reconstruction and resolving of indirect branches. By hav-       interprocedural fashion. In Section VII we aim to provide a
ing abstract values represent a set of possible jump targets, an      more technical head-to-head comparison with existing tools.
indirection can be resolved by concretizing the abstract value
to all instruction addresses it represents. JAKSTAB performs                 III. OVERVIEW OF G ENERIC C ONSTITUENTS
binary analysis and control flow reconstruction based on this            There are three major constituents required to formulate the
principle [27], [28]. The user manually provides a harness            correctness theorem. First of all, a concrete semantics that
modeling the initial state, and relative to that initial state, the   provides a step function step over concrete states (denoted by
generated control flow graph overapproximates all paths in the        s, s′ , . . .). Second, an abstract semantics, defined by 1.) an
abstract step function step over abstract states (denoted by σ,     Every read/write updates the alignment information and taints
σ ′ , . . .), and 2.) a join (denoted ⊔). Third, a concretization   values in memory accordingly. The result is a type S modeling
function γS that maps abstract states to sets of concrete states.   concrete states and function step: a formal but fully executable
    We prove the following two theorems:                            semantics, in which small assembly programs can be executed
    Theorem 1: Function γS is a simulation relation [4] between     on concrete initial states.
the concrete and abstract semantics:
                                                                    B. Abstract Semantics
            s ∈ γS (σ) =⇒ step(s) ∈ γS (step(σ))                       The abstract state stores abstract values. The datatype for
This theorem shows that the abstract semantics overapproxi-         abstract values, denoted V, is left completely polymorphic. We
mate the concrete ones.                                             assume existence of a special ⊤ element. Over this datatype,
   Second, we define an algorithm that performs symbolic            the following generic (i.e., undefined) functions are assumed
execution, while maintaining a mapping φ from the visited           to be available:
instruction addresses to the abstract states. Whenever an in-            γV Concretization            V 7→ {V}
struction address is visited twice, the current abstract state is         S    Abstract semantics Operation × [V] 7→ V
joined with the abstract state stored during the previous visit,          ⊔ Join                      V × V 7→ V
and the algorithm proceeds if the joined state is unequal to             ⊲⊳ Separation                hV × Vi × hV × Vi 7→ B
the stored one. In essence, this is a fixed-point computation.            ⊑ Enclosure                 hV × Vi × hV × Vi 7→ B
We prove:                                                                == Aliassing                 hV × Vi × hV × Vi 7→ B
   Theorem 2: The mapping φ produced by the algorithm               For sake of presentation, we omit functions used for getting
provides invariants:                                                initial abstract values. Function S takes as input the name of
            s is reachable =⇒ s ∈ γS (φ(s.rip))                     an operation executed by an assembly instruction (e.g, add).
                                                                    Note that a single assembly instruction may execute several
   In words, any concrete reachable state s is included in the      such operations (e.g., imul). Function S symbolically executes
set of states represented by the abstract state stored in mapping   that operation on abstract values. The separation, enclosure
φ associated to its instruction pointer rip. Reachability means     and aliassing relations are over abstract regions. Function γR
that s is reachable from some unconstrained concrete state,         concretizes an abstract region ha, sii by applying γV to both
with rip as the entry point, through a path of resolved control     the address and the size.
flow transfers.                                                        The above generic functions must satisfy a set of 26 proof
A. Concrete Semantics                                               obligations. Most of these are trivial (e.g., the join must be
                                                                    a commutative semigroup over V; enclosure is transitive and
   The concrete semantics are largely straightforward, except
                                                                    reflexive). We here provide some examples of interesting proof
for the treatment of partially overlapping memory accesses. At
                                                                    obligations. Join, separation, enclosure, aliasing, and abstract
the binary level, any memory access occurs through pointer
                                                                    semantics must be overapproximative. For separation, this
computations. We formulate the assumption that any region
                                                                    means that concretizing separate abstract regions must produce
in memory storing a pointer is from there on not accessed
                                                                    separate concrete regions; note that concrete separation ⊲⊳
in a partially overlapping fashion. For example, consider
                                                                    can be expressed in terms of linear equalities for non-tainted
a scenario where region hrsp0 − 16, 8i has been accessed
                                                                    values. For the semantics, overapproximation is formulated by
(denoting the 8-byte region 16 bytes below the original
                                                                    stating that the result of applying some concrete operation 
value of the stackpointer rsp). From that point on, regions
                                                                    must be overapproximated by the semantics provided by S
hrsp0 − 16, 4i and hrsp0 − 12, 4i are still considered valid
                                                                    for the corresponding symbolic operation . Here,  can,
accesses. Region hrsp0 − 12, 8i is not, as it partially overlaps
                                                                    e.g., be an arithmetic, logical or bitvector operation. The
with a previously accessed region. As a consequence of this
                                                                    presentation shows binary operators, but this easily extends to
assumption, any partially overlapping access is assumed not to
                                                                    n-ary operators. Finally, there is a set of algebraic properties
produce a pointer. Since we are interested in pointer analysis,
                                                                    concerning the relations over regions, such as “Enclosure in
we therefore allow the concrete semantics to make values
                                                                    separate region”.
read from or written to by partially overlapping access to
become tainted. Overapproximation then concerns untainted                       IV. OVERVIEW OF I NSTANTIATIONS
values only.                                                           We provide three different instantiations, each of which has
   The concrete states stores concrete values, denoted V. A         been formally defined in Isabelle/HOL and for each of which
concrete value is either an immediate bitvector or the special      all proof obligations have been proven. All three domains are
value ⊤ (tainted). A concrete state contains an assignment of       represented by sets of elements from a different universe: C, B
registers to concrete values. Concrete memory assigns concrete      and S. Elements of these domains satisfy the following syntax:
values to concrete regions: tuples of type V × V containing                           C                           B                           S
the address and size of the region. A priori, no memory               {c0 , c1 , . . .}   |   {b0 , b1 , . . .}       |   {s0 , s1 , . . .}
alignment information is available and thus concrete memory            Constant                   Bases                     Sources
must store concrete values as well as the current alignment.          Computation
 The join must be overapproximative:             γV (a0 ) ⊆ γV (a0 ⊔ a1 )
 Separation must be overapproximative:           r0 ⊲⊳ r1 ∧ r0 ∈ γR (r0 ) ∧ r1 ∈ γR (r1 ) =⇒ r0 ⊲⊳ r1
 Semantics must be overapproximative:            v0 ∈ γV (a0 ) ∪ {⊤} ∧ v1 ∈ γV (a1 ) ∪ {⊤} =⇒ v0  v1 ∈ γV (S(, a0 , a1 )) ∪ {⊤}
 The join respects separation:                   r ⊲⊳ ha0 ⊔ a1 , si i =⇒ r ⊲⊳ ha0 , si i
 The join respects enclosure:                    ha0 , si i ⊑ ha0 ⊔ a1 , si i
 Enclosure in separate region:                   r0 ⊑ r1 ∧ r1 ⊲⊳ r2 =⇒ r0 ⊑ r2
                                                Fig. 1: Examples of Proof Obligations


     The abstract points first of all concern symbolic expressions,     of bases to allow the abstract pointer to non-deterministically
denoted by type E. As operators, symbolic expressions have              represent different pointers with bases.
arithmetic and logical operations, bit-level operations such as            Pointers with sources. Expressions of the form
                                                                                         S
sign-extension or masking, and other operations related to              {s0 , s1 , . . .} fully abstract away from how the pointer
x86-64 assembly instructions. There is a dereference operator           is computed. Whereas pointers with identifiable bases contain
∗he, sii – where e and si are symbolic expressions – that mod-          sufficient information at least for roughly establishing a
els reading si bytes from address e. As operands, symbolic              memory designation, a pointer parameterized with sources
expressions have immediate values, state parts, constants or            only concerns what information has been used in the
heap-pointers. Immediate values are words of fixed size. State          computation of the pointer. In other words, the pointer has
parts can be registers (e.g., rax, edi, . . .) or flags (ZF, CF,        been computed by some expression with operands from the
. . . ). Constants are values of state parts relative to the initial    given set of sources. The following sources are possible:
state. For example, rax0 denotes a constant: the initial value
stored in register rax. Constants thus represent initial values                  Source ≡ Constant c | Base b | Fun name
of state parts when the current function was called. A heap-            A source can be a constant, a base or the return value of some
pointer is an expression of the form alloc[id ] and models                                                                         S
                                                                        function. For example, expression {rdi0, rsi0, Fun getc} in-
the return value of an allocation function such as malloc. The          dicates a pointer that has been computed using only the initial
id is an identifier to distinguish different mallocs. A constant        values of registers rdi and rsi and the return value of function
computation is a symbolic expression with as operands only              getc.
immediate values and constants.                                            Example 1: Consider the running example in Figure 2.
     Pointers with constant computations. An expression                 The example allocates memory and performs some memory
                                C
of the syntax {c0 , c1 , . . .} is based on a non-empty set             writes. Two regions (at addresses 0x3006 and 0x3008) are
of constant computations. It non-deterministically represents           relative to the initial value of the stackpointer rsp0. The
any value from the given set. For example, expression                   abstract pointers corresponding to these memory writes may be
                         C
{rsp0 − 8, rdi0 + 16} simply represents any of the two con-             represented in C: respectively {rsp0 − 16}C and {rsp0 − 8}C .
stant computations. This domain is the most concrete.                   The memory write at address 0x3005 occurs on the heap. Even
                                                                    B
     Pointers with bases. Expressions of the form {b0 , b1 , . . .}     if offset is some convoluted dynamically computed offset, the
partly abstract away from how the pointer is computed. It                                                                             B
                                                                        abstract pointer will be representable in B: {Alloc 0x3003} .
keeps track only of positive addends in the computation that            Finally, the memory write at address 0x3007 writes to the
can be recognized as a basis for a pointer. The given set is            address initially stored in register rdx plus the return value
a non-empty set of bases. A base is defined by the following            of function getc. The abstract pointer is representable in S:
datastructure:                                                                             S
                                                                        {rdx0, Fun getc} .

 Base ≡ StackPointer f | Global a | Alloc id | Symbol name              A. Separation over Abstract Pointers
                                                                           Each of the three domains allows a different type of
Four types of pointer bases are recognized. The base may                reasoning over separation. Intuitively, separation between two
be the stackpointer (in x86-64 this is register rsp) pointing           pointers implies that necessarily – i.e., for any address rep-
to somewhere in the stackframe of a certain function f . The            resented by the two pointers – two memory writes commute.
base may be a global address a. At the binary level, the global         Separation is denoted by the infix operator ⊲⊳.
address space is pointed to using immediate values and thus                Consider two pointers p0 +offset and p1 . If both pointers are
a is a 64-bit immediate word. The base may be the result                defined by constant computations, separation can be decided
of some dynamic memory allocation. Finally, a base can be               by an SMT solver. For the other domains, however, one
a named symbol. At the binary level, external variables are             may argue that separation cannot be guaranteed under any
named symbols with immediate addresses.                                 circumstances. We argue this is too strict. For example, if
   Note that any pointer will have at most one base. For                one pointer is based on the heap and the other on the local
example, no pointer computation would allow addition of the             stack, then it is safe to assume that even if offset is chosen
stack pointer and a heap address. The datastructure allows a set        nefariously, writes to the two pointers will either cause a
                                                                                                              C
                                                                       σ.rsp                      =    {rsp0}
                                                                                                             C
0x3000 : mov rbp , rsp                                                 σ.rbp                      =    {rsp0}
0x3001 : call getc                                                     σ.rcx                      =    {Fun getc}S
                                                                                                                       C
0x3002 : mov rcx , rax                                                 σ.rax                      =    {alloc[0x3003]}
                                                                                                                 C
0x3003 : call malloc                                                   σ.rsi                      =    {rsp0 − 8}
0x3004 : lea rsi , [ rbp - 8]                                          σ.∗h{Alloc 0x3003}B i      =    {rsp0 − 8}C
0x3005 : mov qptr [ rax + offset ] , rsi                                                C                              B
                                                                       σ.∗h{rsp0 − 16} , 8i       =    {Global 0x2000}
0x3006 : mov qptr [ rsp -16] , 0x2000                                                       S
                                                                       σ.∗h{rdx0, Fun getc} i     =    {alloc[0x3003]}
                                                                                                                       C
0x3007 : mov qptr [ rdx + rcx ] , rax                                                 C
                                                                       σ.∗h{rsp0 − 8} , 4i        =    ⊤
0x3008 : mov dptr [ rsi ] , 0
                 (a) x86-64 Assembly                                                    (b) Abstract State

Fig. 2: Assembly code. For sake of presentation, pseudo code is given on the right. offset denotes some dynamically computed
offset. Instruction lea loads an address into register rsi without reading from memory. The binary has a data section with
address range 0x2000 to 0x2040.


segmentation fault or they will commute. Assuming separation             is assumed to be separate from the global address space and the
is thus safe. On the other hand, we argue that if both pointers          heap. As argued above, separation over different stackframes
are based on local stackframes of different functions, then              is desirable, but not necessarily. The global address space is
assuming separation is dangerous as a stack overflow may                 assumed to be separate from the local address space and the
cause the pointers to overlap.                                           heap. The global address is not necessarily assumed to be
   It may be the case that separation is not necessarily true,           separate from the symbols in the binary, i.e., external variables.
but desirable. Consider a pointer with source set {rdi0}. The            Both are typically constant immediates, within the range of
only way for that pointer to overlap with the stackframe of the          addresses within the binary. Separation is considered to be
current function, is if initially – at the time the current function     desirable. If two global addresses are based on immediates that
was called – register rdi contained a pointer to below its               fall within the range of different data sections of the binary,
own stackframe. That is invalid source code and can therefore            then separation is considered desirable.
be considered undesirable. For various use cases, it can be                 Two allocations with different ids are assumed to be sep-
useful to distinguish “necessarily” separation from “desirable”          arate, as different ids ensure these were different calls to
separation (see Section VI).                                             malloc. A pointer based on malloc should not lead to a
   For domains B and S, whether two abstract pointers are                write overlapping with the region of a different malloc.
separate is in essence domain specific knowledge on what                 Whether this separation should be considered necessary or
assumptions can validly be made when dealing with an x86-                desirable is debatable. Heap overflows are common and critical
64 binary. In Figure 3, this knowledge will be encoded in                vulnerabilities, and if these are part of the attacker model,
algebraic definitions. Depending on ones view, one may easily            then this separation should be considered desirable. Note that
add or remove cases of separation, and move cases from                   two pointers based on allocations with the same id, are not
“desirable” to “necessarily” or the other way around.                    necessarily not separate.
   Pointers with constant computations. For two constant                    Pointers with sources. Since pointers with sources are
computations, separation can be formulated as a linear pro-              more abstract, there are fewer cases that allow deciding
gramming problem, solvable by an SMT solver [34]. This                   separation necessarily. For example, consider two pointers
requires the size of the regions pointed to, to be known.                with source sets {rdi0} and {rsi0}. Whether these can be
Typically, these sizes can syntactically be inferred from the            considered separate depends on the initial state of the current
current instruction. We define function SMT[⊲⊳] as a function            function, i.e., whether registers rdi and rsi initially were
that takes as input two constant computations c0 and c1 ,                separate. However, there still are cases when separation can be
and two sizes si 0 and si 1 and returns true if and only if              decided. First, when two sources are actually bases, the above
the following SMT problem is unsatisfiable: c0 ≤ a <                     relation ⊲⊳B can used as decision procedure. Second, consider
c0 + si 0 ∧ c1 ≤ a < c1 + si 1 . In words, an address a that is          a pointer computed using constant rdi0 and a newly allocated
in both regions should be unsatisfiable. Constant computations           pointer. As long as the allocation happened within the current
typically consist of arithmetic operations containing only +,            function, separation can safely be assumed: essentially this
− and ∗, and bit-level operations supported by SMT-theory                assumes that the initial state cannot predict where malloc
QF BV.                                                                   will allocate memory. Since sources of the form Fun f do
   Pointers with bases. Separation for pointers with bases can           not represent pointers, separation between these sources and
be decided algebraically. Figure 3 presents relation ⊲⊳B , i.e.,         all other sources can be assumed. Finally, consider a source
separation over bases. The local stack frame of any function f           rdi0, i.e., the initial value of register rdi when the current
                Necessarily:
                    StackPointer f       ⊲⊳B   Alloc id
                    StackPointer f       ⊲⊳B   Global a
                    StackPointer f       ⊲⊳B   Symbol name
                    Global a             ⊲⊳B   Alloc id
                    Alloc id0            ⊲⊳B   Symbol name
                    Alloc id0            ⊲⊳B   Alloc id1                   if   id0 6= id1
                    Base b0              ⊲⊳S   Base b1                     ≡    b0 ⊲⊳B b1
                    Constant c           ⊲⊳S   Base Alloc id               if   id belongs to current function
                    Fun f                ⊲⊳S   s1
                Desirable:
                    StackPointer f       ⊲⊳B   StackPointer f ′            if   f 6= f ′
                    Global a             ⊲⊳B   Global a′                   if   a and a′ are from different data sections
                    Global a             ⊲⊳B   Symbol name
                    Constant c           ⊲⊳S   Base StackPointer f         if   f is current function

              Fig. 3: Separation over abstract pointers: the smallest symmetric relation such that the above holds.


function was called. It is possible that the caller initialized          Abstract States. A state stores values for registers, flags
rdi with a pointer to the stackframe of the callee, but we             and memory. An abstract state part is defined by the following
consider it undesirable.                                               datatype:
   Example 2: Revisiting Example 1, we address the memory
accesses in order of execution. First a write happens to pointer                 SP ≡ Register r | Flag f | Memory (V × N?)
                         B
p0 = {Alloc 0x3003} . Then, a write happens to pointer
p1 = {rsp0 − 16}C = {StackPointer 0x3000}B . These two                 A memory statepart is represented as a region, a tuple with
regions are necessarily separate for all three domains. Then, a        an abstract pointer and optionally a size. Whenever clear from
                                                  S
write happens to pointer p2 = {rdx0, Fun getc} . Separation            context, we will omit the constructors. For example, sp = rax
between p0 and p2 follows necessarily for domains B and S.             simply means that statepart sp equals register rax. An abstract
However, separation between p1 and p2 is not necessarily true.         state is a partial mapping from stateparts to abstract values:
It is, however, desirable. Finally, a write happens to pointer         S ≡ SP ⇀ V.Notation σ.r denotes the current value stored in
                   C
p3 = {rsp0 − 8} . Similar reasoning applies for separation             register r. Memory partitions the address space into separate
with p0 and p2 . For domain C, separation between p1 and p3            abstract regions, and assigns stored values to each of these
is decided by an SMT solver.                                           regions. Notation σ.∗hri denotes the value stored in region r,
   In similar fashion, enclosure and aliassing are instantiated.       where the size is omitted when not available.
The join is defined as set-union. Instantiating abstract seman-           Example 3: Revisit the running example in Figure 2. Based
tics and concretization is straightforward.                            on the separation relations decided in Example 2, the state σ in
         V. I NTRAPROCEDURAL P OINTER A NALYSIS                        Figure 2b can model the state after execution of the assembly
   Algorithmically, intraprocedural pointer analysis can be            snippet. Note that this state is based on desirable separation,
achieved using a standard abstract interpretation algo-                as otherwise regions would need to get joined. Intuitively, the
rithm [12], [23]. Essentially, starting at some initial abstract       following claims are modeled by this state:
state with the instruction pointer set to the entry point of the       • Any region based on a heap-pointer allocated at line 0x3003
binary (or a function of interest), symbolic execution traverses         contains no pointers other than the pointer rsp0 − 8.
the assembly instructions step-by-step using function step.            • The 8-byte region at address rsp0 − 16 stores a value that
It runs until a return statement, or an exiting function call.           may point to the global data section.
Whenever an instruction address is visited twice, the current
                                                                       • A memory write has occurred that is determined by the
state σcurr is compared to the state σstored belonging to the
                                                                         initial value of register rdx as well as input provided via
previous visit. If state σstored is more abstract then state σcurr ,
                                                                         function getc. That memory write was assumed to be
exploration can stop. Otherwise, the two states must be joined
                                                                         separate from all others.
to a state σjoin . That state is stored and exploration continues.
                                                                       • If the value stored in region hrsp0 − 8, 4i would be deref-
Effectively, this algorithm provides a (partial) mapping from
                                                                         erenced, then no information on its designation in memory
instruction addresses to stored symbolic states. A post-state
                                                                         is known.
σpost is computed by taking the supremum of all terminal
non-exiting states. Thus, we define state and a symbolic step            The claims in the above example can be formalized by con-
function on top of the generic constituents.                           cretization of abstract states to concrete ones. Concretization
of state parts is provided by function γSP of type SP 7→ 2SP :           Integration into Disassembly: A fundamental problem
                                                                      in disassembly is resolving indirections. Typically, indirect
      γSP (Register r) ≡       { Register r }
                                                                      jumps can be analyzed through intraprocedural analysis. For
      γSP (Flag f)     ≡       { Flag f }
                                                                      example, they are the result of reading a jump table induced
      γSP (Memory r) ≡         { Memory r | r ∈ γR (r) }
                                                                      by a switch statement. For indirect calls, however, often
  Definition 1: The concretization of states is function γS of        interprocedural analysis is necessary. An indirect call is often
type S 7→ 2S , and is defined as:                                     the result of a function callback. These typically happen across
   γS (σ) ≡ {s | ∀sp · σ.sp = v =⇒                                    function boundaries: a function pointer is passed from function
                    ∀sp ∈ γSP (sp) · ∃v ∈ γV (v) · s.sp = v}          to function until it is called. This scenario mandates context-
                                                                      sensitive interprocedural analysis where the context provides
In words, abstract state σ is mapped to any concrete state s          sufficient information to resolve indirect calls.
in which both all stateparts and all stored values have been
concretized.                                                           Function f :
   Abstract Step Function. Every assembly instruction can              0x6000 : mov qword ptr [0 x2010 ] , 0 x6050
be written as a sequence of micro-instructions of the following        0x6001 : call 0 x6500
form:                                                                  0x6002 : call exit
                    dst := f (in0 , in1 , . . .)                       ...
A single destination – be it a register, a memory region or            0x6050 : push rbp
a flag – gets assigned the return value of a pure operation            0x6051 : . . .
f that is based on zero or more input-operands (registers,             ...
memory regions, flags, or immediate values). The operation             Function g:
typically corresponds to a mnemonic, e.g., add or imul. In             0x6500 : mov rax , qword ptr [0 x2010 ]
x86-64, many (but not all) instructions have one destination           0x6501 : call rax
operand (register or memory) and may set a list of flags.              0x6502 : ret
Typically, it cannot be the case that both destination and
sources are memory. We here make no assumptions, and                                 Fig. 4: Example of Indirect Call
generalize the symbolic step function over any sequence of
micro-instructions. Transformation from basic assembly to               Figure 4 provides an example. Function pointer 0x6050 is
sequences of micro-instructions can be done, e.g., using the          written to a global variable (at address 0x2010). Function h
Ghidra decompiler which translates assembly instructions of           will be analyzed in a context where the pre-state provides:
various architectures into low P-code [40].                                                              B
                                                                                σpre .∗h{Global 0x2010} i = {0x6050}
                                                                                                                         C
   The semantics of executing a micro-instruction µ consists
of resolving the input-operands, applying operation f , and           When symbolically executing the indirect call at Line 0x6501,
writing the produced value to the state. This is implemented          it is overapproximatively known that any pointer stored in
in function step(µ, σ). The abstract semantics S are used to          the global address space based on address 0x2010 points
apply operation f on abstract values. Functions read(r, σ) and        to instruction address 0x6050. The recursive traversal can
write(r, a, σ) are defined that take care of memory accesses          therefore consider 0x6050 as a reachable instruction address.
in abstract states.                                                   Note that in a stripped binary, functions are not delineated:
   Correctness and Termination. Correctness – the abstract            it is not known what addresses are function entries. Without
semantics overapproximate the concrete semantics – has been           context, the indirect call at Line 0x6501 cannot be resolved
defined at the start of Section III and has been formally proven      and the entire function at entry 0x6050 would have been
correct in Isabelle/HOL. Note that it may be the case that paths      missed. Section VII-B provides data on how many indirections
are unexplored due to unresolved indirections.                        can be resolved in practice.
   Termination has also been proven, but it requires the proof           Preliminary to Decompilation: At the assembly level,
obligation that there does not exist an infinite chain of different   there are no variables. Bottom-up analysis, such as decom-
states such that σ0 ⊔ σ1 ⊔ . . .. We thus ensure termination          pilation, has no ground truth as to what regions in memory
by putting bounds on the sizes of the sets of the abstract            constituted variables. A variable in source code typically is
pointers. These bounds are chosen manually. They do not               compiled to a memory region, with the characteristic that this
affect correctness. Making them larger makes the pointers             region is separate from any memory write not to the same
more precise, but increases running times. For bounds C, B,           variable. As example consider Figure 5. It shows assembly
and S the bounds are resp. 10, 5 and 250. Any pointer with            with some hypothetical pointer analysis result on the right.
more elements is shifted to ⊤.                                        Based on the derived pointers, a decompilation tool can assign
                                                                      a variable x to lines 0x7000 and 0x7002.
                        VI. U SE C ASES                                  Bottom-up Dataflow Analysis: The post-state produced
  We here discuss several use cases with small pedagogical            by analysis of a function provides overapproximative insight
examples.                                                             into what parts of the state are modified by a function. One
                                                                                                                                 C
   0x7000 :       mov qword ptr [ rdi ] , 42                          x       :=   42              rdi    =     {rsp0 − 48}
                                                                                                                           B
   0x7001 :       mov qword ptr [ rsi ] , 43                          *rsi    :=   43              rsi    =     {Alloc id }
   0x7002 :       mov qword ptr [ rbp -40] , 44                       x       :=   44              rbp    =     {rsp0 − 8}C
                          (a) x86-64 Assembly                             (b) Decompiled                 (c) Abstract Pointers

                       Fig. 5: Assembly code, decompiled to code with variables based on abstract pointers.


application of this, is that it can be used to verify whether a                             VII. E VALUATION
certain function abides by a calling convention. The calling
convention designates certain registers to be non-volatile, i.e.,        In addition to the formal proofs of the soundness of our
they must be preserved by a function. This can be observed            approach, we provide a prototype implementation and con-
from the post-state directly. If the post-state provides that, for    ducted a series of experimental studies to evaluate soundness
                              C
a register r: σpost .r = {r0 } ,then this indicates that register r   and preciseness. We run 1.) a comparative evaluation against
has been properly preserved. Many compilers use a push/pop            the state-of-the-art, and 2.) a more in-detail evaluation per
pattern to achieve such preservation: a register value is initially   instantiation.
pushed to the local stack, and popped just before return.
Calling convention adherence requires abstract pointer analysis       A. Comparative Evaluation
to be sufficiently precise throughout symbolic execution that
                                                                         The closest related works to our binary pointer analyzer
the local region into which a register value is pushed is not
                                                                      are BinPointer [26] and BPA [25]. Unfortunately, even after
overwritten. A push/pop pattern is not necessary though: our
                                                                      contacting the authors of the papers, either their source code
approach is transparent to the means of register preservation
                                                                      was not available or the code was not runnable on our
a function may use.
                                                                      examples. Therefore, to stay fair in our comparison, we used
   We provide an additional example demonstrating this over-          the exact same dataset of binaries that BinPointer and BPA
approximative form of pointer analysis can be used for live           used (SPEC 2006 V1) and we employed the same definition
variable analysis. Consider a function returning with the state       of soundness and precision they used in their paper.
in Example 3. The pointer allocated at line 0x3003 is stored             We map all abstract pointers to a subset of {L, G, H}
in the return register rax and can therefore considered to be         (for: local, global, heap). Domains that are provably within
live. However, if the state overapproximately indicates that          the current stackframe are mapped to {L}, domains that are
the pointer is not returned and not written to global memory,         relative to the stackpointer but that may possibly be above
the pointer can be considered as “not live” after return of the       the current stack frame (e.g., point to the stackframe of a
function.                                                             caller) are mapped to {L, H}. Global bases are mapped to
   Finding suspect patterns for automated exploit gener-              {G}. Top is mapped to {L, G, H}, the rest is considered heap
ation: Pointer analysis can enhance real-world downstream             and mapped to {H}. This produces function PA that maps
analyses. As an example, we consider automated exploit                instruction addresses to observations.
generation: automatically finding bugs and generating working            To assess the ground truth, we built an instrumentation tool
exploits [2], [44]. One of the many challenges in this field,         based on the dynamic binary instrumentation tool PIN [32].
is to deal with state space explosion. Our pointer analysis           Each memory write observed at run-time to some address a
can be used to find patterns in the binary that may lead to           is mapped to an element of {L, G, H}. If rsp0 − 0x10000 ≤
vulnerabilities, thereby pruning the state space to be explored.      a ≤ rsp0, address a is considered local (here rsp0 denotes
   As a concrete case study, we can enumerate all instructions        the value of the stackpointer when the current function was
in a binary that do a function call to an external function, and      called). We cannot know how large the stackframe is, and
that pass a pointer to the current stackframe as parameter to         overapproximate the size with the constant 0x10000 for sake
that function. This is a suspect pattern, as the external function    of observation. If address a is a memory address covered by
has been given the opportunity to overwrite the return address.       any of the sections where the binary is located at run-time, it
We have applied our pointer analysis to the ret2win challenge         is considered global. In all other cases, address a is considered
provide by ROP emporium2. The above heuristic finds an                heap. By running multiple executions, each memory write
instruction at address 0x400701: call memset where register           is mapped to a subset of {L, G, H} as well. This produces
rdi (the first parameter under the System V ABI calling               function GT that maps instruction addresses to observations.
convention) contains a local pointer. Indeed, the example is          The total set of (instruction addresses of) observed memory
(purposefully) exploitable, and the exploit leverages exactly         writes is denoted with W.
this particular instruction.                                             Soundness: We consider a static pointer analysis to be sound
                                                                      if its results support the ground truth, i.e., the observations
                                                                      of PIN. In other words, the pointer analysis must predict a
  2 https://ropemporium.com                                           superset of the ground truth. Soundness is computed using the
recall: the percentage of supported memory writes to the total        A holistic way of looking at precision, is 1.) to see whether
number. If the recall is 100%, the pointer analysis is sound.       the pointer analysis is sufficiently precise such that for each
   Precision: Soundness does not imply usefulness. For exam-        function all its pointers are assigned a domain separate from
ple, if the pointer analysis returns ⊤ for all the instructions,    the top of the stack frame (where the return address is stored),
it will be consider sound but useless. We therefore measure         and 2.) that it enables resolving indirections. Table II shows
precision as well. In words, precision measures the specificity     that for 94.2% of all functions this was the case (OK). For
of the returned pointer domains. The precision is computed          5.41% of the functions, not all indirections could be resolved
as the total average of the percentage of domains that PA           (UN), but all resolved paths ending in a return were OK.
overapproximated but were not observed by GT.                       Finally, for 0.39% of the functions, our pointer analysis was
                                                                    not sufficiently precise to show that the return address was not
 recall      ≡ 100 ∗ |{a∈W·GT(a)⊆PA(a)}|
                            |W |                                    overwritten (ERR). This typically happens for functions with
 precision ≡ 100 ∗ avga∈W (1 − |PA(a)\GT(a)|
                                     3       )                      complex stackpointer manipulation, such as stack probing or
                                                                    dynamic stack allocation.
   Table I shows results. The authors of BinPointer have
reported that the recall of their approach on the SPEC dataset
                                                                                         VIII. C ONCLUSION
is 100%. Since we also observed the same recall for our
approach on this dataset, we do not include it in the table. As        This paper presented an approach to formally proven correct
the results show, when it comes to heap and global memory           binary-level pointer analysis, that aims to assign a desig-
accesses, our approach achieves over a 29% and 15% higher           nation to each memory write in a binary. The designations
precision compared to BinPointer and BPA. For the local             are provably overapproximative: the write provably cannot
memory accesses, our approach shows almost similar precision        occur to any region in memory outside of its designation.
compared to that of BinPointer. All other larger case studies       Evaluation confirms this soundness, and shows that precision
reported in [26] are not publicly available. Interpreting and       is comparable to or improves upon the state-of-the-art.
comparing their published results subjectively, we conclude            Many existing approaches to binary analysis, whether it
that our work achieves at least similar precision. The largest      is disassembly, decompilation, binary patching or security
reported binary for BinPointer is 161K instructions. In the next    analysis, are unsound. State-of-the-art tools apply heuristics,
section, we show that our tool scales upto 507K instructions,       incorporate best practices, and are generally based on extensive
and we thus argue we are at least as scalable as well.              human-in-the-loop knowledge. Decompilation becomes a form
                                                                    of art rather than an algorithm. We envision an overapprox-
B. Per-instantiation Evaluation
                                                                    imative – provably sound – approach as an alternative. This
   We also evaluate per instantiation soundness and precision.      requires provably sound disassembly, control flow reconstruc-
As case studies, we consider a set of binaries covering over        tion, decompilation, and type inference, to begin with. At the
1M instructions (see Table II). Overall recall is 100%.             heart of all of these overapproximative techniques lies a proper
   We discuss precision in more detail (see Figure 6). In-          understanding of the semantics of each individual instruction.
stantiation C is always 100% precise – as no abstraction is         Binary-level pointer analysis aims to aid these future endeavors
applied – unless it assigns ⊤ to a pointer. It may assign,          in overapproximative binary analysis, by indicating what the
                           C
e.g., {rsp0 − 8, 0x3000} , in which case on different paths the     effect of each memory write in a binary can be.
pointer can be local or global (0.79% of the overall memory
writes). Overall, instantiation C assigns a non-⊤ pointer to                     DATA -AVAILABILITY S TATEMENT
85.22% of all memory writes.
   Instantiation B, then, only marginally improves that number.       The implementation of the pointer analysis in this paper, all
It assigns pointers to 0.95% more memory writes, and for those      case studies, and the formal Isabelle/HOL proofs are available
only the base of the pointer is known. However, the value of        anonymously at: https://doi.org/10.5281/zenodo.14223108.
this instantiation fluctuates per binary: for some it did not
improve on C at all, but for others up to 5% more memory                                ACKNOWLEDGMENTS
writes got assigned a non-⊤ pointer. These are typically the
hard cases, e.g., a local pointer to an array for which only a         We would like to thank the anonymous reviewers for their
base could be established.                                          insightful comments and suggestions, which helped to greatly
   Instantiation S, finally, assigns a non-⊤ pointer to all         improve the paper.
memory writes. Figure 6 shows that this mostly concerns heap-          This work is supported by the Defense Advanced Research
pointers. From this we can conclude that the cap on the number      Projects Agency (DARPA) and Naval Information Warfare
of sources is never hit, since otherwise this instantiation would   Center Pacific (NIWC Pacific) under Contract No. N66001-
assign ⊤. For those writes where both C and B assign ⊤,             21-C-4028, by DARPA and the Army Contracting Command
instantiation S at least provides us with information on which      Aberdeen Proving Grounds (ACC-APG) under Prime Contract
sources (e.g., function inputs or mallocs) were used to com-        No. W912CG23C0024, and by DARPA under Prime Contract
pute the pointer value.                                             No. HR001124C0492.
                                                             Local                                 Global                                   Heap
            Binary        #instructions
                                              BPA      BinPointer    This paper      BPA       BinPointer    This paper      BPA      BinPointer      This paper
             mcf               2.4K           26.3       100.0         100.0         27.0         85.7          91.5         N/A         N/A             57.8
             lbm               2.2K           22.3        99.5         100.0         73.1        100.0          66.7         N/A         N/A             33.3
        libquantum             9.6K           47.9       100.0         100.0         100.0       100.0         100.0          6.9         6.9            50.0
            bzip2               11K           16.9        93.2          89.2         51.7         51.7          100           3.6        21.8             40
            sjeng               22K           32.7        97.5          79.1         55.1         55.6          99.8         N/A         N/A             56.1
            milc                23K           49.4        99.4          93.3         81.2         88.9          95.2         23.7        23.7            51.1
           hmmer                60K           38.0        99.9          98.9         76.4         76.4         100.0          7.6        11.5            65.4
          h264ref              100K           35.3        97.3          97.1          6.2         65.5          90.6         24.2        40.8            47.6
          Average                             33.6        98.4          94.7         58.8         78.0          93.0         13.2        20.9            50.2

         TABLE I: Comparison study of the precision (%) of BPA, BinPointer, and this paper on the SPEC dataset.

                                       C                                             B                                               S

                                       L                                              L                                               L
                                     43.83                                          44.11                                           44.13


                             0.79                                            0.82                                           0.82            0.07
                                      0.06                                          0.06                                            0.07

                                      0.02                                          0.02                                            0.33
                     14.14                        26.38              14.45                        26.70             14.45                          40.11
                              G               H                               G               H                              G               H
                                  ⊤ : 14.78                                       ⊤ : 13.83                                         ⊤: 0

Fig. 6: Precision results per instantiation. The numbers are percentages. For example, instantiation C assigned a local pointer
to 43.83% of all memory accesses, and to 0.79% a pointer set with both a local and a global pointer.


   Binary            #instrs        Time (m:ss)              #functions                   [4] C. Baier and J.-P. Katoen, Principles of model checking. MIT press,
                                                     OK        UN       ERR                   2008.
   du                30K            0:09             173       7        0                 [5] G. Balakrishnan and T. Reps, “Analyzing memory accesses in x86
   gzip              14K            0:04             101       5        0                     executables,” in International conference on compiler construction.
   host              12K            0:04             62        8        2                     Springer, 2004, pp. 5–23.
   sha512sum         10K            0:05             36        3        0
   sort              18K            0:08             146       8        0                 [6] ——, “Wysinwyx: What you see is not what you execute,” ACM Trans-
   spec/*            150K           1:22             942       41       11                    actions on Programming Languages and Systems (TOPLAS), vol. 32,
   sqlite3           319K           1:33             1687      144      8                     no. 6, pp. 1–84, 2010.
   ssh               124K           1:01             523       32       8                 [7] D. Brumley, I. Jager, T. Avgerinos, and E. J. Schwartz, “Bap: A binary
   tar               91K            0:15             300       17       0                     analysis platform,” in Computer Aided Verification, G. Gopalakrishnan
   vim               507K           4:26             2922      86       1                     and S. Qadeer, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg,
   wc                6K             0:01             46        4        0                     2011, pp. 463–469.
   wget2             61K            0:10             578       81       2                 [8] V. Chipounov, V. Georgescu, C. Zamfir, and G. Candea, “Selective
   xxd               2K             0:01             13        0        0                     symbolic execution,” in Proceedings of the 5th Workshop on Hot Topics
   zip               24K            1:09             103       2        0                     in System Dependability (HotDep), 2009.
   Total             1.4M                            94.2%     5.41%    0.39%             [9] V. Chipounov, V. Kuznetsov, and G. Candea, “The s2e
                                                                                              platform: Design, implementation, and applications,” ACM Trans.
TABLE II: Evaluation on an Apple M1 Pro with 32 GB of                                         Comput. Syst., vol. 30, no. 1, feb 2012. [Online]. Available:
                                                                                              https://doi.org/10.1145/2110356.2110358
memory. Memory usage was at most roughly 15GB for vim.
                                                                                         [10] J.-D. Choi, M. Burke, and P. Carini, “Efficient flow-sensitive inter-
                                                                                              procedural computation of pointer-induced aliases and side effects,”
                                                                                              in Proceedings of the 20th ACM SIGPLAN-SIGACT symposium on
                                                                                              Principles of programming languages, 1993, pp. 232–245.
                                    R EFERENCES
                                                                                         [11] C. Cifuentes and K. J. Gough, “Decompilation of binary programs,”
                                                                                              Software: Practice and Experience, vol. 25, no. 7, pp. 811–829, 1995.
[1] L. O. Andersen, “Program analysis and specialization for the C program-
    ming language,” Ph.D. dissertation, DIKU, University of Copenhagen,                  [12] P. Cousot and R. Cousot, “Abstract interpretation: a unified lattice model
    1994.                                                                                     for static analysis of programs by construction or approximation of
[2] T. Avgerinos, S. K. Cha, A. Rebert, E. J. Schwartz, M. Woo, and                           fixpoints,” in Proceedings of the 4th ACM SIGACT-SIGPLAN symposium
    D. Brumley, “Automatic exploit generation,” Communications of the                         on Principles of programming languages, 1977, pp. 238–252.
    ACM, vol. 57, no. 2, pp. 74–84, 2014.                                                [13] L.-A. Daniel, S. Bardin, and T. Rezk, “Binsec/rel: Efficient relational
[3] D. Babić, L. Martignoni, S. McCamant, and D. Song, “Statically-                          symbolic execution for constant-time at binary-level,” in 2020 IEEE
    directed dynamic automated test generation,” in Proceedings of the 2011                   Symposium on Security and Privacy (SP). IEEE, 2020, pp. 1021–1038.
    International Symposium on Software Testing and Analysis, ser. ISSTA                 [14] J. Dawson, “Isabelle theories for machine words,” Electronic Notes in
    ’11. New York, NY, USA: Association for Computing Machinery, 2011,                        Theoretical Computer Science, vol. 250, no. 1, pp. 55–70, 2009.
    p. 12–22. [Online]. Available: https://doi.org/10.1145/2001420.2001423               [15] S. Debray, R. Muth, and M. Weippert, “Alias analysis of executable
     code,” in Proceedings of the 25th ACM SIGPLAN-SIGACT symposium              [33] L. Martignoni, S. McCamant, P. Poosankam, D. Song, and P. Maniatis,
     on Principles of programming languages, 1998, pp. 12–24.                         “Path-exploration lifting: Hi-fi tests for lo-fi emulators,” SIGPLAN
[16] A. Djoudi and S. Bardin, “BINSEC: binary code analysis with low-level            Not., vol. 47, no. 4, p. 337–348, mar 2012. [Online]. Available:
     regions,” in Tools and Algorithms for the Construction and Analysis              https://doi.org/10.1145/2248487.2151012
     of Systems - 21st International Conference, TACAS 2015, Held as             [34] L. d. Moura and N. Bjørner, “Z3: An efficient smt solver,” in Inter-
     Part of the European Joint Conferences on Theory and Practice of                 national conference on Tools and Algorithms for the Construction and
     Software, ETAPS 2015, London, UK, April 11-18, 2015. Proceedings,                Analysis of Systems. Springer, 2008, pp. 337–340.
     ser. Lecture Notes in Computer Science, C. Baier and C. Tinelli,            [35] J. A. Navas, P. Schachte, H. Søndergaard, and P. J. Stuckey, “Signedness-
     Eds., vol. 9035. Springer, 2015, pp. 212–217. [Online]. Available:               agnostic program analysis: Precise integer bounds for low-level code,” in
     https://doi.org/10.1007/978-3-662-46681-0 17                                     Asian Symposium on Programming Languages and Systems. Springer,
[17] M. Emami, R. Ghiya, and L. J. Hendren, “Context-sensitive interpro-              2012, pp. 115–130.
     cedural points-to analysis in the presence of function pointers,” ACM       [36] T. Nipkow, M. Wenzel, and L. C. Paulson, Isabelle/HOL: a proof
     SIGPLAN Notices, vol. 29, no. 6, pp. 242–256, 1994.                              assistant for higher-order logic. Springer, 2002.
[18] J. Feist, L. Mounier, S. Bardin, R. David, and M. Potet, “Finding           [37] C. Pang, R. Yu, Y. Chen, E. Koskinen, G. Portokalidis, B. Mao, and
     the needle in the heap: combining static analysis and dynamic                    J. Xu, “SoK: All you ever wanted to know about x86/x64 binary
     symbolic execution to trigger use-after-free,” in Proceedings of                 disassembly but were afraid to ask,” in 2021 IEEE Symposium on
     the 6th Workshop on Software Security, Protection, and Reverse                   Security and Privacy (SP). IEEE, 2021, pp. 833–851.
     Engineering, SSPREW@ACSAC 2016, Los Angeles, California, USA, [38] G. Ramalingam, “The undecidability of aliasing,” ACM Trans. Program.
     December 5-6, 2016, M. D. Preda, N. Stakhanova, and J. T.                        Lang. Syst., vol. 16, no. 5, p. 1467–1471, sep 1994. [Online]. Available:
     McDonald, Eds. ACM, 2016, pp. 2:1–2:12. [Online]. Available:                     https://doi.org/10.1145/186025.186041
     https://doi.org/10.1145/3015135.3015137                                     [39] T. Reps and G. Balakrishnan, “Improved memory-access analysis for
[19] G. Girol, B. Farinier, and S. Bardin, “Not all bugs are created                  x86 executables,” in International Conference on Compiler Construc-
     equal, but robust reachability can tell the difference,” in Computer             tion. Springer, 2008, pp. 16–35.
     Aided Verification - 33rd International Conference, CAV 2021,               [40] R. Rohleder, “Hands-on Ghidra tutorial about the software reverse
     Virtual Event, July 20-23, 2021, Proceedings, Part I, ser. Lecture               engineering framework,” in Proceedings of the 3rd ACM Workshop on
     Notes in Computer Science, A. Silva and K. R. M. Leino, Eds.,                    Software Protection, 2019, pp. 77–78.
     vol. 12759. Springer, 2021, pp. 669–693. [Online]. Available:               [41] Y. Shoshitaishvili, R. Wang, C. Salls, N. Stephens, M. Polino,
     https://doi.org/10.1007/978-3-030-81685-8 32                                     A. Dutcher, J. Grosen, S. Feng, C. Hauser, C. Kruegel, and G. Vigna,
[20] P. Godefroid, P. de Halleux, A. V. Nori, S. K. Rajamani, W. Schulte,             “Sok: (state of) the art of war: Offensive techniques in binary analysis,”
     N. Tillmann, and M. Y. Levin, “Automating software testing using                 in 2016 IEEE Symposium on Security and Privacy (SP), 2016, pp. 138–
     program analysis,” IEEE software, vol. 25, no. 5, pp. 30–37, 2008.               157.
[21] P. Godefroid, M. Y. Levin, and D. A. Molnar, “Automated whitebox fuzz       [42] B. Steensgaard, “Points-to analysis in almost linear time,” in Proceed-
     testing,” in Proceedings of the Network and Distributed System Security          ings of the 23rd ACM SIGPLAN-SIGACT symposium on Principles of
     Symposium, NDSS 2008, San Diego, California, USA, 10th February -                programming languages, 1996, pp. 32–41.
     13th February 2008. The Internet Society, 2008. [Online]. Available:        [43] F. Verbeek, J. Bockenek, Z. Fu, and B. Ravindran, “Formally verified
     https://www.ndss-symposium.org/ndss2008/automated-whitebox-fuzz-testing/         lifting of c-compiled x86-64 binaries,” in Proceedings of the 43rd ACM
[22] M. Hind, “Pointer analysis: Haven’t we solved this problem yet?”                 SIGPLAN International Conference on Programming Language Design
     in Proceedings of the 2001 ACM SIGPLAN-SIGSOFT workshop on                       and Implementation, 2022, pp. 934–949.
     Program analysis for software tools and engineering, 2001, pp. 54–61.       [44] W. You, P. Zong, K. Chen, X. Wang, X. Liao, P. Bian, and B. Liang,
[23] S. Horwitz, A. Demers, and T. Teitelbaum, “An efficient general iterative        “Semfuzz: Semantics-based automatic generation of proof-of-concept
     algorithm for dataflow analysis,” Acta Informatica, vol. 24, no. 6, pp.          exploits,” in Proceedings of the 2017 ACM SIGSAC conference on
     679–694, 1987.                                                                   computer and communications security, 2017, pp. 2139–2154.
[24] T. Kapus and C. Cadar, “A segmented memory model for symbolic               [45] Z. Zhang, W. You, G. Tao, G. Wei, Y. Kwon, and X. Zhang, “BDA:
     execution,” in Proceedings of the 2019 27th ACM Joint Meeting on                 practical dependence analysis for binary executables by unbiased whole-
     European Software Engineering Conference and Symposium on the                    program path sampling and per-path abstract interpretation,” Proceed-
     Foundations of Software Engineering, ser. ESEC/FSE 2019. New                     ings of the ACM on Programming Languages, vol. 3, no. OOPSLA, pp.
     York, NY, USA: Association for Computing Machinery, 2019, p.                     1–31, 2019.
     774–784. [Online]. Available: https://doi.org/10.1145/3338906.3338936
[25] S. H. Kim, C. Sun, D. Zeng, and G. Tan, “Refining indirect call targets
     at the binary level.” in NDSS, 2021.
[26] S. H. Kim, D. Zeng, C. Sun, and G. Tan, “BinPointer: towards precise,
     sound, and scalable binary-level pointer analysis,” in Proceedings of the
     31st ACM SIGPLAN International Conference on Compiler Construc-
     tion, 2022, pp. 169–180.
[27] J. Kinder, “Static analysis of x86 executables,” Ph.D. dissertation,
     Technische Universität, Darmstadt, Nov. 2010. [Online]. Available:
     http://tuprints.ulb.tu-darmstadt.de/2338/
[28] J. Kinder and D. Kravchenko, “Alternating control flow reconstruction,”
     in Verification, Model Checking, and Abstract Interpretation, V. Kun-
     cak and A. Rybalchenko, Eds. Berlin, Heidelberg: Springer Berlin
     Heidelberg, 2012, pp. 267–282.
[29] J. Kinder and H. Veith, “Jakstab: A static analysis platform for binaries,”
     in International Conference on Computer Aided Verification. Springer,
     2008, pp. 423–427.
[30] W. Landi, B. G. Ryder, and S. Zhang, “Interprocedural modification side
     effect analysis with pointer aliasing,” ACM SIGPLAN Notices, vol. 28,
     no. 6, pp. 56–67, 1993.
[31] X. Leroy and S. Blazy, “Formal verification of a c-like memory
     model and its uses for verifying program transformations,” Journal of
     Automated Reasoning, vol. 41, no. 1, pp. 1–31, 2008.
[32] C.-K. Luk, R. Cohn, R. Muth, H. Patil, A. Klauser, G. Lowney,
     S. Wallace, V. J. Reddi, and K. Hazelwood, “Pin: building customized
     program analysis tools with dynamic instrumentation,” Acm sigplan
     notices, vol. 40, no. 6, pp. 190–200, 2005.
