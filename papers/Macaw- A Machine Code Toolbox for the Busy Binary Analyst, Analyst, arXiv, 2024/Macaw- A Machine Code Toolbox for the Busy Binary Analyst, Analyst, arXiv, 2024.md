                                         Macaw: A Machine Code Toolbox for the Busy Binary
                                         Analyst
arXiv:2407.06375v3 [cs.PL] 19 Feb 2025




                                         RYAN G. SCOTT, Galois, Inc., United States
                                         BRETT BOSTON, , United States
                                         BENJAMIN DAVIS, Galois, Inc., United States
                                         IAVOR DIATCHKI, Galois, Inc., United States
                                         MIKE DODDS, Galois, Inc., United States
                                         JOE HENDRIX, , United States
                                         DANIEL MATICHUK, Galois, Inc., United States
                                         KEVIN QUICK, Galois, Inc., United States
                                         TRISTAN RAVITCH, , United States
                                         VALENTIN ROBERT, Galois, Inc., United States
                                         BENJAMIN SELFRIDGE, Galois, Inc., United States
                                         ANDREI S, TEFĂNESCU, , United States
                                         DANIEL WAGNER, , United States
                                         SIMON WINWOOD, , United States
                                         When attempting to understand the behavior of an executable, a binary analyst can make use of many dif-
                                         ferent techniques. These include program slicing, dynamic instrumentation, binary-level rewriting, symbolic
                                         execution, and formal veriﬁcation, all of which can uncover insights into how a piece of machine code behaves.
                                         As a result, there is no one-size-ﬁts-all binary analysis tool, so a binary analysis researcher will often combine
                                         several diﬀerent tools. Sometimes, a researcher will even need to design new tools to study problems that
                                         existing frameworks are not well equipped to handle. Designing such tools from complete scratch is rarely
                                         time- or cost-eﬀective, however, given the scale and complexity of modern instruction set architectures.
                                            We present Macaw, a modular framework that makes it possible to rapidly build reliable binary analysis
                                         tools across a range of use cases. Statically typed functional programming techniques are used pervasively
                                         throughout Macaw—these range from using functional optimization passes to encoding tricky architectural
                                         invariants at the type level to statically check correctness properties. The level of assurance that functional
                                         programming ideas aﬀord us allow us to iterate rapidly on Macaw’s development while still having conﬁ-
                                         dence that the underlying semantics are correct.
                                            Over a decade of development, we have used Macaw to support an industrial research team in building
                                         tools for machine code–related tasks. As such, the name “Macaw” refers not just to the framework itself,
                                         but also a suite of tools that are built on top of the framework. We describe Macaw in depth and describe
                                         the diﬀerent static and dynamic analyses that it performs, many of which are powered by an SMT-based
                                         symbolic execution engine. We put a particular focus on interoperability between machine code and higher-
                                         level languages, including binary lifting from x86 to LLVM, as well verifying the correctness of mixed C and
                                         assembly code.

                                         Authors’ addresses: Ryan G. Scott, Galois, Inc., United States, rscott@galois.com; Brett Boston, United States, brett@
                                         brett.boston; Benjamin Davis, Galois, Inc., United States, ben@galois.com; Iavor Diatchki, Galois, Inc., United States,
                                         diatchki@galois.com; Mike Dodds, Galois, Inc., United States, miked@galois.com; Joe Hendrix, United States, joe.d.
                                         hendrix@gmail.com; Daniel Matichuk, Galois, Inc., United States, dmatichuk@galois.com; Kevin Quick, Galois, Inc., United
                                         States, kquick@galois.com; Tristan Ravitch, United States, tristan@ravit.ch; Valentin Robert, Galois, Inc., United States,
                                         val@galois.com; Benjamin Selfridge, Galois, Inc., United States, benselfridge@galois.com; Andrei S, tefănescu, United States,
                                         andrei@stefanescu.io; Daniel Wagner, United States, me@dmwit.com; Simon Winwood, United States, simonjwinwood@
                                         gmail.com.


                                         2024. ACM 2475-1421/2024/9-ART1
                                         https://doi.org/


                                                                          Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:2                                                                                                 Scott et al.


ACM Reference Format:
Ryan G. Scott, Brett Boston, Benjamin Davis, Iavor Diatchki, Mike Dodds, Joe Hendrix, Daniel Matichuk,
Kevin Quick, Tristan Ravitch, Valentin Robert, Benjamin Selfridge, Andrei S, tefănescu, Daniel Wagner, and Si-
mon Winwood. 2024. Macaw: A Machine Code Toolbox for the Busy Binary Analyst. Proc. ACM Program.
Lang. 1, ICFP, Article 1 (September 2024), 29 pages.

1 INTRODUCTION
Binary analysis refers to not one class of tool, but many. Starting with an unknown binary, there
are many tasks that an engineer may want to accomplish. These may include discovering the struc-
ture of the binary, transforming the binary to achieve some goal, analyzing the binary to identify
particular properties or vulnerabilities, and/or formally verifying that the binary matches some
speciﬁcation. These broad tasks can be combined and specialized into many domains, objectives,
tool types, and instruction sets. The result is that there is as yet no optimal binary analysis tool,
but rather a large space of potentially useful designs.
   We present Macaw, a binary analysis toolkit which we have built to help us explore this design
space of tools. Macaw exists in a similar niche as frameworks such as Angr [Shoshitaishvili et al.
2016] and, to a lesser extent, reverse-engineering suites such as Ghidra [Rohleder 2019] and Binary
Ninja [Vector35 2023a]. What sets Macaw apart are the intended use cases. Macaw is not a stan-
dalone tool, but it is instead a Haskell library that can be used to rapidly construct and evaluate
binary analysis tools. The main Macaw library is also accompanied by a suite of libraries for dis-
assembly, representing architecture semantics, and symbolically executing machine code, which
we collectively refer to as the Macaw ecosystem. Macaw is designed to help us build quickly, max-
imize reuse of existing components, and avoid costly errors during prototyping. This imposes a
particular set of design constraints on the Macaw ecosystem, which we explain in this paper.
   The Macaw ecosystem was designed from the onset with statically typed functional program-
ming techniques in mind. This can be seen in the design of Macaw’s intermediate representation
(IR), which encodes information about the semantics of assembly operations and other architec-
ture considerations at the type level. Macaw’s IR needs to be rigid enough to rule out obviously
bad machine-code programs while ﬂexible enough to bootstrap the semantics of existing tools
which might have an ad hoc type system, such as the udis86 disassembler for x86 [Thampi 2014]
or the ARM XML speciﬁcation [Reid 2016].
   Macaw was built to support an industry research team developing novel binary analysis tools.
This team executed on multiple research projects over a decade, with a signiﬁcant amount of
personnel change over this time. In this environment, Macaw has served as a key library that
helped us develop successful tool prototypes. In this paper, we discuss the most interesting and
mature tool designs, which are:
    • Reopt, a binary lifter which converts x86-64 binaries to LLVM code and performs reopti-
       mizations on the lifted code. This was the original Macaw use-case.
    • SAW, a formal veriﬁcation platform that supports mixed C and machine code. See [Boston et al.
       2021; Chudnov et al. 2018; Dodds 2020] for industry use-cases of SAW.
    • Renovate, a static binary rewriter that allows users to add or remove code without executing
       the binary.
    • MCTrace, a binary instrumentation tool to insert probes to dynamically collect telemetry
       with low-overhead tracing, including in environments without an operating system.
    • Ambient-Verifier, a static veriﬁer that can prove the presence of weird machines [Dullien
       2020] in binaries (or lack thereof).
    • PATE, a relational veriﬁer that proves that two binaries have the same observable behaviors.
    • Cerridwen, a tool for ranking how similar a binary is to a known corpus of binaries.

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                         1:3


                           Macaw-Base                     Macaw dialects

                                                       Macaw-AArch32
       Crucible          Macaw-Symbolic                   Macaw-PPC                      ISA-speciﬁc libraries

                                                        Macaw-RISCV
                       Macaw-Refinement
                                                          Macaw-x86


    Fig. 1. The Macaw library ecosystem. An arrow A → B indicates that library A depends on library B.



     • Surveyor, an interactive debugger that, among other features, can step through machine
       code and inspect symbolic values.
To illustrate in more depth how Macaw works, we discuss two of these tools in detail, Reopt
and SAW. We focus on these two because they support very diﬀerent tasks and, as such, require
combining Macaw’s components in very diﬀerent and illustrative ways.
   A key component of Macaw’s design is its deep integration with Crucible [Christiansen et al.
2019], an SMT-backed symbolic execution engine. Although Crucible was originally developed
for simulating higher-level imperative programming languages such as C, the same technology
proves valuable for simulating the behavior of machine code as well. Many tools built on top
of Macaw—including SAW, Renovate, Ambient-Verifier, PATE, and Surveyor—leverage Cru-
cible to peform diﬀerent analyses, including static program analysis and formal veriﬁcation. Be-
cause Crucible also supports higher-level languages such as C, this makes it easier to simultane-
ously analyze codebases that mix these languages with machine code. This is something that SAW
takes advantage of, as it leverages Macaw and Crucible to verify mixed C and machine code.
   Macaw provides a speciﬁc point in the design space of binary analysis frameworks which has
proved useful for us in developing a wide range of capabilities. In Section 2, we discuss the core
design of the Macaw IR and supporting ecosystem, and we discuss how this design aligns with
goals. In Section 3, we explore the tools that we have built on top of Macaw in more detail. We
use this to explain how Macaw helps us to eﬀectively build tools in a variety of domains. In
Section 4, we compare Macaw to existing frameworks such as Angr, and we also compare Macaw-
based tools to similar eﬀorts. Many of the diﬀerences come down to tradeoﬀs; we describe both
the upsides and downsides of the choices that led to Macaw’s design. Section 5 concludes and
discusses our future design ambitions for Macaw.
   The source code for Macaw is publicly available at https://github.com/GaloisInc/macaw.

2   DESIGN OF THE MACAW ECOSYSTEM
The Macaw ecosystem consists of a set of Haskell libraries, whose relationships are depicted in
Figure 1. At the heart of the ecosystem is Macaw-Base, which only contains functionality that is
independent of any particular architecture. This includes the core Macaw intermediate represen-
tation (IR), code discovery, optimization passes, and an ELF loader for ingesting binaries.
   Any architecture-speciﬁc functionality is encapsulated in a Macaw dialect library. Macaw was
originally designed with x86-64 support in mind, which gave rise to the ﬁrst dialect, Macaw-x86.
Later, Macaw-AArch32, Macaw-PPC, and Macaw-RISCV were added. Each of these dialects are
built on top of other libraries that integrate Macaw with disassemblers for speciﬁc instruction set

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:4                                                                                        Scott et al.


architectures (ISAs), and they also encode the semantics of each architecture’s instructions into a
form that can be reasoned about.

2.1     Macaw-Base: Core Data Types and Algorithms
The Macaw-Base library is central to how Macaw works, as it deﬁnes the key data types and
operations needed to perform many binary analysis tasks. All of Macaw’s operations revolve
around an intermediate language (deﬁned in Macaw-Base) where each IR program consists of a
sequence of basic blocks. This IR contains all of the control ﬂow and ISA-independent functionality
needed to perform general analyses, but it is also designed to be extensible so that ISA-speciﬁc
functionality can be added in particular Macaw dialects.
   We built Macaw-Base with statically typed functional programming techniques in mind. Vari-
ous binary analysis-related algorithms can be expressed in relatively succinct fashion by applying
ideas from functional programming (see Section 2.1.5). Moreover, we use Macaw is used in veriﬁca-
tion, so there needs to be assurance the tooling and machine code semantics are correct. To improve
assurance, our implementation encodes information about register sizes, operation bitwidths, and
architectural aspects statically using Haskell’s rich type system, thus statically checking many
correctness properties of the implementation.
2.1.1 Typed Addresses. A key data type that is used in almost every Macaw algorithm is its notion
of machine addresses. Macaw-Base represents a machine address with the MemWord w type, which
consists of a machine word of size w bits:
      newtype MemWord ( w :: Nat ) = MemWord Word64
   Note that w is a type-level number, which means that this convention is checked at compile-
time, not runtime. This makes critical use of GHC’s DataKinds extension, which allows natural
numbers to be promoted to the type level using the Nat kind [Yorgey et al. 2012]. For instance,
32-bit addresses have the type MemWord 32, 64-bit addresses have the type MemWord 64, and it is a
type error to mix up the two types without performing an explicit conversion.
   The w type parameter is one example of a key design choice made throughout Macaw’s code:
where possible, use GHC language extensions to encode invariants about machine code at the type
level. This tradition was inspired by the Crucible symbolic execution library [Christiansen et al.
2019], with which Macaw integrates (see Section 2.1.6).
   One example of where this strong typing discipline is put to use is in how Macaw encodes the
bit widths of AArch32 instructions. AArch32 processors have two instruction sets: ARM mode,
where each instruction is 32 bits, and Thumb mode, where each instruction is 16 bits. Macaw
encodes these bit widths at the type level, and as a result, attempting to mix the two instructions
sets without an explicit mode switch will result in a type error. This has caught many potential
errors when developing Macaw-based tools, as ARM and Thumb instructions can often occur
within the same binary.
   Note that although a MemWord represents an address, it does not encode any information about
where the address is in a binary (aside from a raw number), nor does it guarantee that the memory
at that address will be valid. Macaw-Base deﬁnes additional data types to attend to these needs.
At one level of abstraction higher than a MemWord is a MemAddr w, which consists of a region number
(addrBase) and an oﬀset into the region (addrOffset ). Note that multiple MemAddr s can inhabit the
same region:
      data MemAddr w = MemAddr
        { addrBase :: Int
        , addrOffset :: MemWord w

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                         1:5


     }
   A MemAddr value represents a relocatable region which may (or may not) be mapped to actual
memory. Macaw adopts the convention that the region number 0 always refers to absolute ad-
dresses. Other region numbers are used to represent concepts such as position-independent code.
   When Macaw encodes a binary, it needs to know information about each segment, i.e., each log-
ically distinct sequence of a in memory, along with the corresponding addresses and permissions.
The MemAddr type alone does not encode all this information, so Macaw-Base contains additional
abstractions for this. First, Macaw-Base deﬁnes a MemSegment data type, which describes the over-
all contents of a single segment:
  data MemSegment w = MemSegment
    { segmentBase :: Int
    , segmentOffset :: MemWord w
    , segmentFlags :: Flags
    , segmentContents :: SegmentContents w
    }
   Like a MemAddr , a MemSegment contains a region number (segmentBase ) and an oﬀset into that
region (segmentOffset ). Unlike MemAddr, a MemSegment also stores whether the segment has read,
write, or execute permissions (segmentFlags ), and it also maps each address in the segment to
its underlying memory contents (segmentContents ). The SegmentContents data type describes the
mapping of addresses to memory:
   newtype SegmentContents w =
     SegmentContents ( Map ( MemWord w ) ( MemChunk w ))

  data MemChunk w
    = ByteRegion ByteString
    | RelocationRegion ( Relocation w )
    | BSSRegion ( MemWord w )

  data Relocation w = ...
   The MemChunk type characterizes whether a chunk of memory is a sequence of speciﬁc bytes
(ByteRegion ), a relocatable region whose contents are computed by a Relocation value (RelocationRegion ),
or a .bss section that is initialized with all zeroes (BSSRegion ). The precise details of how diﬀerent
parts of binaries map to which MemChunk s are beyond the scope of this paper.
   Macaw-Base uses the MemSegmentOff data type to describe an address that is guaranteed to be
valid (i.e., point to valid memory). A MemSegmentOff value is simply a MemSegment plus an oﬀset into
the that segment:
  data MemSegmentOff w = MemSegmentOff
    { segoffSegment :: MemSegment w
    , segoffOffset :: MemWord w
    }
  Finally, a binary is a collection of MemSegment s, along with metadata describing what the entry-
point address is and which region numbers map to which segments.

2.1.2 Typed Memory Shapes. Another place where Macaw draws inspiration from Crucible is
in how Macaw encodes the shapes of values that are stored in memory. Although all data in a

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:6                                                                                              Scott et al.


binary can be thought of as a series of bytes, the shape of those bytes is very much dependent on
the context in which it is used. For example, some machine instructions interpret bytes as integers,
some instructions interpret bytes as ﬂoating-point values, and so on. It is all too easy to mix up
diﬀerent shapes, so Macaw encodes these shapes at the type level and parameterizes diﬀerent
operations based on what shapes they expect.
   Speciﬁcally, Macaw-Base deﬁnes a MacawType data type, which is shown in Figure 2. Note that
the data constructors of MacawType are only ever meant to be used at the type level (again, using
GHC’s DataKinds extension), which gives Macaw uses a pseudo-dependently typed ﬂair. Aside
from encoding invariants about memory shapes at the type level, it is also useful to be able to
check what sort of MacawType one has at runtime. This is achieved via a TypeRepr object, which
acts as a singleton type for MacawType [Eisenberg and Weirich 2012]. One can pattern-match on a
TypeRepr value to determine which sort of MacawType is used at runtime.


      data MacawType                                 data TypeRepr ( tp :: MacawType ) where
        = -- | A bitvector                             BVTypeRepr
          BVType Nat                                     :: NatRepr n
          -- | Floating - point                          -> TypeRepr ( BVType n )
        | FloatType FloatInfo                          FloatTypeRepr
          -- | A vector of types                         :: FloatInfoRepr fi
        | VecType Nat Type                               -> TypeRepr ( FloatType fi )
                                                       VecTypeRepr
      data FloatInfo                                     :: NatRepr n
        = -- | 32 - bit IEEE754                          -> TypeRepr tp
          SingleFloat                                    -> TypeRepr ( VecType n tp )
        | -- | 64 - bit IEEE754
          DoubleFloat                                data FloatInfoRepr ( fi :: FloatInfo ) where
        | ...                                          SingleFloatRepr ::
                                                         FloatInfoRepr SingleFloat
                                                       DoubleFloatRepr ::
                                                         FloatInfoRepr DoubleFloat
                                                       ...

Fig. 2. The definition of MacawType in Macaw, which describes the shape of machine-code values at the
type level. This type is witnessed at the value level by TypeRepr, which can be thought of as the singleton
type [Eisenberg and Weirich 2012] for MacawType.


2.1.3 From Addresses to Architectures. Just as Macaw’s address types are indexed by the number
of bits (w :: Nat) or a memory shape (tp :: MacawType), many Macaw abstract syntax types
are parameterized by an arch type parameter, which represents the processor architecture being
used. Doing so ensures that operations from separate architectures are not mixed up. For exam-
ple, Macaw-x86 instantiates arch with an X86_64 type, Macaw-AArch32 instantiates arch with
an AArch32 type, and so on. We refer to types like X86_64 and AArch32 as architecture extension
points. One example of an arch-indexed type is ArchReg , which is displayed in more detail in Fig-
ure 3. ArchReg uses GHC’s TypeFamilies extension [Schrijvers et al. 2008] to map an architecture
extension point to a register data type.
   Sometimes, arch-indexed data types must interact with w-indexed data types. A Macaw ar-
chitecure uniquely determines the number of bits in a machine address, so Macaw deﬁnes a

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                         1:7



     type family ArchReg arch :: MacawType -> Type
     type instance ArchReg X86_64 = X86Reg
     type instance ArchReg AArch32 = ARMReg
     ...

     type family RegAddrWidth ( r :: MacawType -> Type ) :: Nat
     type instance RegAddrWidth X86Reg = 64
     type instance RegAddrWidth ARMReg = 32
     ...

     type    family ArchStmt arch :: MacawType -> Type
     type    ArchAddrWidth arch = RegAddrWidth ( ArchReg arch )
     type    ArchAddrWord arch = MemWord ( ArchAddrWidth arch )
     type    ArchMemAddr arch = MemAddr ( ArchAddrWidth arch )
     type    ArchSegmentOff arch = MemSegmentOff ( ArchAddrWidth arch )

               Fig. 3. Type families and synonyms related to architecture extension points.


RegAddrWidth type family to bridge the gap between the former and the latter. This is such a com-
monly used type family that Macaw also provides a variety of type synonyms deﬁned on top of
RegAddrWidth for convenience, which are depicted in Figure 3.

2.1.4 The Macaw Intermediate Language. Macaw uses a three address code–based intermediate
language [Aho et al. 1986] that is centered around basic blocks (Block). Each basic block consists
of a list of statements (Stmt) followed by a special terminator statement (TermStmt ). These data
types are given in Figure 4.
   Each data type is parameterized by two type parameters: arch, which encodes the architecture,
and ids, which denotes the set of identiﬁers used in assignment instructions. The ids type param-
eter is unique to each decoded function, which ensures that instructions from diﬀerent functions
cannot be mixed without an explicit renaming step. The ids type parameter functions similarly to
the s type parameter in Haskell’s ST s type [Launchbury and Peyton Jones 1995].
   The control ﬂow in Macaw is oriented around Blocks, and a disassembled machine instruction
can correspond to multiple Stmts in a Block, depending on the complexity of the instruction. Note
that the Stmts in two blocks are allowed to overlap. For example, this is necessary to support
AArch32 binaries, where instructions can be in both ARM or Thumb mode depending on how
they are reached.
   A single Stmt can perform an assignment (AssignStmt ), write to memory (WriteMem), execute an
ISA-speciﬁc statement (ExecArchStmt ), or update register values (ArchState ). The Stmt type is also
used to encode metadata about which parts of a basic block correspond to the start of an instruction
(InstructionStart ) and any additional information that is useful for debugging purposes (Comment).
The Stmt data type has many auxiliary types used in its data constructors, so we will deﬁne ones
that are relevant to this paper as they become relevant.
   The core Macaw IR is compact and covers common operations present in multiple ISAs, which
are used to represent the behavior of many instructions. These operations primarily involve inte-
ger arithmetic (e.g., add and sub in x86-64), and Macaw encodes these operations using bitvectors
in a way that can be easily translated to SMT. More complicated operations (i.e., ones that do not
map directly to SMT) are put into syntactically separate parts of the Stmt language. For example,

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:8                                                                                         Scott et al.



        data Block arch ids = Block                                data Stmt arch ids where
          { blockStmts ::                                            AssignStmt
              [ Stmt arch ids ]                                        :: Assignment arch ids tp
          , blockTerm ::                                               -> Stmt arch ids
              TermStmt arch ids }                                    WriteMem
                                                                       :: ArchAddrValue arch ids
        data TermStmt arch ids                                         -> MemRepr tp
          = FetchAndExecute                                            -> Value arch ids tp
              RegState                                                 -> Stmt arch ids
               ( ArchReg arch )                                      ExecArchStmt
               ( Value arch ids )                                      :: ArchStmt arch
          | TranslateError                                                 ( Value arch ids )
              RegState                                                 -> Stmt arch ids
               ( ArchReg arch )                                      ArchState
               ( Value arch ids )                                      :: ArchMemAddr arch
              Text                                                     -> RegState
          | ArchTermStmt                                                   ( ArchReg arch )
              ArchTermStmt arch                                            ( Value arch ids )
               ( Value arch ids )                                      -> Stmt arch ids
              RegState                                               InstructionStart
               ( ArchReg arch )                                        :: ArchAddrWord arch
               ( Value arch ids )                                      -> Text
                                                                       -> Stmt arch ids
        type    family ArchStmt arch                                 Comment
          ::    ( MacawType -> Type ) -> Type                          :: Text
        type    family ArchTermStmt arch                               -> Stmt arch ids
          ::    ( MacawType -> Type ) -> Type

                       Fig. 4. Core data types used in Macaw’s intermediate language.


memory accesses are their own category, as they must be decomposed into SMT-friendly opera-
tions via symbolic execution (see Section 2.1.6). There is also a separate category for architecture-
speciﬁc extensions (e.g., data cache hints in PowerPC), for which each ISA has a small number of
instructions. Depending on where these instructions can occur in a basic block, these ISA-speciﬁc
instructions are put into ArchStmt or ArchTermStmt .
   Separating common operations from more complicated ones reﬂects a key Macaw design deci-
sion: the Macaw IR does not attempt to be generic enough to encode every possible instruction
directly. One beneﬁt for this decision is that it keeps the Macaw IR relatively readable. Although
Macaw could expand every instruction directly to core operations, this could easily cause the
number of Stmts to balloon in size. For example, x86-64’s AES-NI instructions would likely need
hundreds of bitvector operations to encode directly. Another beneﬁt is that some instructions per-
form eﬀects that not all Macaw clients need to model, so putting them into architecture-speciﬁc
extensions means that clients only “pay” for extensions that they reason about. This gives Macaw
users a high degree of control when mixing diﬀerent components.
2.1.5 Code Discovery. One of the most important passes in Macaw-Base is code discovery. The
core discovery pass identiﬁes all of the functions in a binary that are reachable from a set of entry

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                         1:9



        Entry point                            Exploration frontier
         addresses
                                            Call

                                                        Branch
                                  Classify                                  Disassemble block

                               Return
       Discovered
                                                 Rewrite (simplify)
       functions

                              Fig. 5. Macaw’s core code discovery algorithm.



point addresses. This pass also distinguishes intra-procedural control ﬂow like branches, jumps,
and switch statements from inter-procedural control ﬂow such as calls, tail calls, and returns. Code
discovery is required for compositional code analysis passes and designed to work even when a
binary lacks symbol tables or other static mechanisms for identifying layout.
   The core algorithm that powers code discovery is illustrated in Figure 5. The algorithm discovers
one function at a time by taking candidate function addresses from the exploration frontier, which
is seeded with an initial set of entry points. Usually, these entry points are taken from the entry
point address of an ELF binary, the dynamic entry points of a shared library, the addresses of static
symbols (when available), as well as function addresses derivable from metadata, such as DWARF
unwinding tables. Macaw also supports specifying custom entry points, which can be useful for
binaries that lack symbol information (e.g., stripped binaries).
   The main part of the algorithm is the block decoding loop, which discovers functions by de-
coding their individual blocks. First, Macaw decodes an instruction using a low-level disassembly
function for the speciﬁc architecure. Next, Macaw lifts the instruction into a semantic represen-
tation as a sequence of Stmts. If the instruction changes control ﬂow (e.g., x86-64’s call), Macaw
will terminate the block with a TermStmt ; otherwise, it will restart the loop and continue decoding
the block.
   Next, Macaw performs rewriting, which simpliﬁes terms in the block to improve readability
and simplify later analyses. Afterwards, Macaw analyzes the block to determine what kind of
control-ﬂow transfer terminates the block, be it a jump, function call, or otherwise. To this end,
Macaw tracks abstract domains for each machine register, using techniques inspired by value-set
analysis [Balakrishnan and Reps 2004] to update the domains as new blocks are discovered. At the
end of analysis, Macaw consults the abstract return address, as well as the addresses and bounds
of jump tables, to classify how the block terminates. Targets of function calls are added to the
exploration frontier as they are classiﬁed, which is used in subsequent iterations of the algorithm.
   An example rewriting pass. One optimization that Macaw’s rewriting pass enables is converting
values to mux head normal form (MHNF), where if-then-else expressions (i.e., muxes) are raised
as far up in the CFG as possible. As an example, consider this minimized CFG (pretty-printed for
compactness):

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:10                                                                                       Scott et al.


   r1 := ...
   r2 := Mux r1 0 x4 0 x28
   r3 := Add r2 0 x100a3e50
   { ip => r3 }
  This CFG is not in MHNF, as it contains a mux expression (r2) that is nested within another
expression’s deﬁnition (r3). To convert this CFG to MHNF, we want to rewrite it into something
that looks more like this:
   r1 := ...
   r4 := Mux r1 0 x100a3e54 0 x100a3e78
   { ip => r4 }
   Where 0x100a3e54 and 0x100a3e78 have folded away the constant addition of 0x100a3e50 to 0x4
and 0x28, respectively. This way, the instruction pointer (ip) value is directly a mux expression.
MHNF CFGs are preferable from a code discovery perspective, as Macaw’s code discovery pass is
more likely to notice branch statements when all of the branching is encoded as a top-level mux
in the instruction pointer register.
   One nice consequence of Macaw being written in a functional language is that the MHNF pass
can be implemented in a very simple, easy-to-follow, and relatively terse fashion. The MNHF pass
(as well as the rest of the rewriter’s passes) are implemented in the Rewriter monad, which is a
state monad that carries around the necessary state as well as the list of statements that have been
rewritten so far:
   newtype Rewriter arch s src tgt a =
     Rewriter ( StateT ( RewriteState arch s src tgt ) ( ST s ) a )

   data RewriteState arch s src tgt =
     RewriteState
       ( RewriteContext arch s src tgt )
       [ Stmt arch tgt ]
   Most of the details of RewriteContext are not essential to understanding the MNHF pass, so we
elide them here. A useful helper function that we need in order to simplify constant expressions
(such as the Add expression in the example above) is rewriteApp :
   rewriteApp ::
     App ( Value arch tgt ) tp ->
     Rewriter arch s src tgt ( Value arch tgt tp )
   rewriteApp app =
     case app of
       BVAdd _ x ( BVValue _ 0) -> do
         pure x
       BVAdd w ( BVValue _ x ) ( BVValue _ y ) -> do
         pure ( BVValue w ( toUnsigned w (x + y )))

         -- No normal rewrites available ,
         -- now try MHNF for enabling code discovery
         _ -> rewriteMhnf app




Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                        1:11


  The full deﬁnition of rewriteApp is omitted for brevity, but the code above shows the essence of
the function. Expressions that can be simpliﬁed with simple syntactic rewrites are simpliﬁed, and
everything else is delegated to rewriteMhnf , the function which performs the MHNF pass:
   rewriteMhnf ::
     App ( Value arch tgt ) tp ->
     Rewriter arch s src tgt ( Value arch tgt tp )
   rewriteMhnf app =
     case app of

        BVAdd w
             ( valueAsApp -> Just ( Mux p c t f ))
             v@ ( BVValue _ _ ) -> do
          t ' <- rewriteApp ( BVAdd w t v )
          f ' <- rewriteApp ( BVAdd w f v )
          rewriteApp $ Mux p c t ' f '

        BVAdd w
             ( valueAsApp -> Just ( Mux p c t f ))
             v@ ( RelocatableValue _ _) -> do
          t ' <- rewriteApp ( BVAdd w t v )
          f ' <- rewriteApp ( BVAdd w f v )
          rewriteApp $ Mux p c t ' f '

        -- no more rewrites applicable , so return the final result
        _ -> evalRewrittenRhs ( EvalApp app )

  -- Add an assignment statement that evaluates the right hand side
  -- and return the resulting value .
  evalRewrittenRhs ::
    AssignRhs arch ( Value arch tgt ) tp ->
    Rewriter arch s src tgt ( Value arch tgt tp )
   This function recognizes if-expressions (i.e., Muxes) that appear nested underneath bitvector ad-
ditions (i.e., BVAdds) If it encounters such an if-expression, it pushes the addition down through the
branches of the if-expression, simplifying constant expressions with rewriteApp along the way.
If it encounters any other type of expression, then it assigns the expression to a fresh identiﬁer,
records the assignment in the RewriteState , and returns the assigned expression as a Value via
evalRewrittenRhs .
   The MHNF rewriting pass involves a number of distinct steps: constant simpliﬁcation, pattern
recognition, the MNHF rewrites themselves, and appending new assignments to the current state.
Thanks to the use of the Rewriter monad, we are able to separate the concerns of appending new
assignments from the “business logic” of performing rewrites. Thanks to Haskell’s pattern match-
ing, recognizing the shapes of if-expressions is straightforward. And thanks to classic functional
programming techniques, we are able to compartmentalize the tedious (but mechanical) details of
simplifying constant expressions in a single rewriteApp function.




                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:12                                                                                            Scott et al.



                                                    Flexdis86
                                                                                   Macaw-X86
                    x86-64 binary             (AST of disassembled
                                                                                  (Macaw CFG)
                                                  instructions)

Fig. 6. The architecture of Macaw-x86, describing the process of going from an x86-64 binary to a Macaw
CFG.



2.1.6 Symbolic Execution via Crucible. A key component of the Macaw ecosystem is Macaw-
Symbolic, which deﬁnes functionality for simulating Macaw IR programs with Crucible, a sym-
bolic execution library targeting imperative code [Christiansen et al. 2019]. Using Macaw-Symbolic,
one can simulate a binary with symbolic data, such as symbolic register states or stack contents.
During simulation, Crucible will generate veriﬁcation conditions that are discharged to an SMT
solver.
   Besides machine code, Crucible also includes dialects targeting other imperative programming
languages, including C, Java, and Rust. Crucible’s LLVM dialect (which enables reasoning about
C code) has been battle-tested on a large number of veriﬁcation problems from the SV-COMP
veriﬁcation competition [Scott et al. 2021]. Moreover, Crucible can reason about code that mixes
languages, such as C programs that use inline assembly (see Section 3.2).

   Symbolic Code Discovery. The Macaw ecosystem also includes an additional, optional method
of code discovery provided by the Macaw-Refinement library. This library utilizes symbolic ex-
ecution to discover code targets, which can supplement the simpler, pattern-based heuristics that
Macaw-Base uses.
   As an example, consider a switch statement whose expression is an integer i whose range of
possible values was previously constrained by an if statement. When the various case targets of
the switch statement are small and regularly sized, the compiler may encode the switch statement
as a jump to i * s, where s is the size of the largest case block. Macaw-Base’s pattern-based
heuristics will not be aware the constraints from the if statement, and thus they cannot limit the
scope of possible jump targets to the speciﬁc set of valid addresses. Using Macaw-Refinement,
on the other hand, allows an SMT solver to indicate the constrained set of possible jump targets
to add those to the discovery frontier.

2.2    Macaw-x86: The First Macaw Dialect
Macaw-x86, which targets the x86-64 ISA, was the ﬁrst ISA dialect that we developed alongside
the Reopt tool (see Section 3.1). The architecture of Macaw-x86 is pictured in Figure 6. While
this ﬁgure is speciﬁc to x86-64, it establishes a general pattern that we continued to use when
developing future dialects, albeit with some notable diﬀerences (which we will address later).
   Because Macaw-x86 was our ﬁrst attempt at a dialect, we did not have an existing methodology
for integrating an ISA into Macaw, nor did we have a clear picture of what design choices one
could make in the process of developing a dialect. One notable decision that we made (perhaps
unconsciously) during development was to hand-write most of the code in Macaw-x86. This is
because the Reopt tool needed to be able to run on x86-64 binaries with a relatively quick turn-
around time, and as such, we could not wait until we had 100% coverage of the x86-64 ISA before
demonstrating results. As such, we implemented support for individual x86-64 instructions on an
as-needed basis, manually implementing whatever scaﬀolding was necessary for Macaw to reason
about each instruction.

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                          1:13


2.2.1 Disassembling x86-64 Binaries Using Flexdis86. The ﬁrst step that Macaw-x86 performs
when analyzing a binary is to diassemble it—that is, to ingest the binary’s raw bytes into a more
structured representation. A binary’s contents can be thought of as a stream of instructions, and
the role of a disassembler is to parse one instruction from the stream at a time. We wrote our own
x86-64 disassembler library1 , named Flexdis86, which represents each instruction as a Haskell
data type, called an InstructionInstance . An InstructionInstance captures all of an instruction’s
relevant properties, such as its name, opcode, size, and operands (be they immediate values, regis-
ters, addresses, or otherwise).
   The main entrypoint into Flexdis86 is the disassembleInstruction function:
   disassembleIn st ru ct io n ::
     ByteReader m => NextOpcodeTable -> m InstructionIns ta nc e
   The ByteReader class characterizes Haskell monads that can represent instruction streams. Flexdis86
is primarily meant to be used with a ByteReader instance that eﬃciently reads a binary from disk,
but Flexdis86 also supports a simpler ByteReader instance that can be used to mock the contents
of a binary for testing purposes.
   Because x86-64 is a very large ISA with well over 1,000 instructions, writing a feature-complete
disassembler for x86-64 is no small feat. To make this task more manageable, disassembleFunction
takes an NextOpcodeTable argument, which represents a lookup table that maps an instruction
opcode to possible InstructionInstance values:
   type NextOpcodeTable = Vector OpcodeTable

   data OpcodeTable
      = -- There are still more opcode bytes to parse .
        OpcodeTable NextOpcodeTable
        -- All of the opcode bytes have been parsed , resulting in
        -- a list of possible instruction candidates .
      | OpcodeTableEntry ! InstructionCan di da te
   To understand how NextOpcodeTable works, consider the pop instruction. Some versions of the
pop instruction have opcodes that begin with the byte 0f, so a NextOpcodeTable would have an entry
at index 0f containing a OpcodeTable that handles the remaining opcode bytes. This OpcodeTable
would then contain another, smaller NextOpcodeTable with entries at indices a1 and a9, each con-
taining OpcodeTableEntry values for pop. These table entries represent two variants of the instruc-
tion with the opcodes 0f a1 and 0f a9, respectively. The smaller NextOpcodeTable would also map
any opcode bytes for other instructions whose opcodes begin with 0f (e.g., the addps instruction,
which can use the opcode 0f 58).
   Constructing a NextOpcodeTable is by far the most tedious part of Flexdis86’s disassembler. To
make this process less tedious, we partially automate it by leveraging the udis86 project [Thampi
2014], which implements an x86 and x86-64 disassembler for C. Flexdis86 uses udis86’s XML
table describing all x86-64 instructions to automatically generate a NextOpcodeTable value. This
automation does save us quite a bit of time, but it is not perfect. Flexdis86’s version of the XML ta-
ble makes some manual tweaks, such as adding additional instructions not covered by udis86 .
We also do not automate any of the logic for turning InstructionCandidate s into full-ﬂedged
InstructionInstance s, which can be surprisingly complicated due to the sheer number of instruc-
tion preﬁxes that x86-64 uses to distinguish diﬀerent instructions.

1 Flexdis86 contains both an x86-64 disassembler and assembler, but we do not use the assembler from Macaw.



                               Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:14                                                                                         Scott et al.


2.2.2 Encoding x86-64 Semantics Using Macaw-x86. After disassembling a binary’s instructions,
the next step is to reify them into a semantic representation that Macaw can reason about. The
Macaw-x86 dialect accomplishes this by deﬁning an InstructionDef for each x86-64 instruction,
which converts an InstructionInstance from Flexdis86 into a list of Macaw basic blocks:
   newtype InstructionSema nt ic s = InstructionSem ant ic s
     ( forall st ids . InstructionInst an ce -> X86Generator st ids ())

   -- A monad for generating Macaw basic blocks .
   data X86Generator st ids a

   -- A pair of an instruction mnemonic ( e. g ., `pop `)
   -- alongside its semantics .
   type InstructionDef = ( ByteString , InstructionSem an ti cs )
   We also deﬁne a small domain-speciﬁc language for deﬁning InstructionDef values that makes
it more obvious what an instruction’s semantics mean at a glance. As a small example, here is the
complete semantics for the cbw (convert byte to word) instruction in Macaw-x86:
   def_cbw :: InstructionDef
   def_cbw = defNullary " cbw " $ do
     v <- get al
     ax .= sext n16 v
   These semantics use defNullary to signify that the cbw instruction does not take any operands.
It ﬁrst reads a byte from the al register (get al), uses sign extension (sext) to convert the byte into
a two-byte value (n16), and ﬁnally copies the two-byte value into the ax register (ax .= ...). The
InstructionDef DSL also includes shorthand for other common machine code idioms (immediate
values, memory locations, oﬀsets, etc.) that are not shown above.
   Unlike Flexdis86, where we made an eﬀort to automate at least some parts of the implemen-
tation, all of the semantics implemented in Macaw-x86 are completely hand-written. This was
largely a practical consideration, as we wanted to demonstrate results for the subset of x86-64
instructions that we encountered the most on the Reopt project, and hand-writing the seman-
tics for these hand-picked instructions proved a fast way to accomplish this. Our methodology
was to carefully read the Intel x86-64 ISA manual [Intel 2024] and extract formal semantics for
each instruction’s entry in the manual. Although the list of instructions covered by Macaw-x86’s
semantics has grown over the years, it is still far from complete.
   The choice to hand-write Macaw-x86’s semantics, while expedient in the short-term, poses a
challenge to long-term maintenance. If we use Macaw-x86 on a binary containing an instruction
that is not covered by the list of covered instructions, then we must add the instruction’s semantics
manually, which is a time-consuming process. Not only that, but this is an error-prone process, as
human programmers are liable to make mistakes when translating the ISA manual’s prose.


2.3 Macaw-PPC: A More Automated Dialect
As we gained experience developing the Macaw-x86 dialect, it became increasingly clear that
manually curating dialects for large ISAs did not scale well as well as we’d like. We decided that if
we were to add another Macaw dialect for a big ISA, we would make a concerted eﬀort to automate
as much of the process as was reasonable. That opportunity came when we developed the next
dialect, Macaw-PPC. The architecture of Macaw-PPC is pictured in Figure 7. Our focus with

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                          1:15


                                        Dismantle-PPC
                                                                      semMC-PPC                   Macaw-PPC
        PowerPC binary               (AST of disassembled
                                                                    (What4 program)              (Macaw CFG)
                                         instructions)

                         (via LLVM                    (via hand-written         (via Macaw-SemMC)
                         TableGen)                   base set semantics +
                                                     automated SemMC
                                                    semantics translation
                                                         via Crucible)


Fig. 7. The architecture of Macaw-PPC, describing the process of going from an PowerPC binary to a Macaw
CFG.


Macaw-PPC was to support both 32- and 64-bit PowerPC binaries, although we tend to exercise
the 32-bit PowerPC code paths more often due to its prevalence in embedded software.
2.3.1 Disassembling PowerPC Binaries Using Dismantle. The ﬁrst step in developing Macaw-PPC
was to generate a disassembler. We used the udis86 disassembler in order to (partially) generate
Macaw-x86’s disassembler, but because udis86 is speciﬁc is x86, we could not do something similar
PowerPC. As a result, we developed a more general solution: a cross-architecture assembler and
diassembler generation library called Dismantle. Dismantle would become the basis for Macaw-
PPC’s disassembler, as well as the the disassembler for most Macaw dialects going forward.
   Dismantle works by consulting the data provided by LLVM’s TableGen tool [LLVM Project
2024]. LLVM uses TableGen as part of its code generator to describe the encodings, types, and
operands of machine instructions. TableGen data is also ideal for generating disassemblers, so
Dismantle is able to use TableGen with little or no changes required.2
   TableGen data ﬁles are large, and we don’t want to have to load a data ﬁle every time we disas-
semble a PowerPC binary, as this would be prohibitively expensive. Our solution is to instead load
the data ﬁle only once when compiling the package. We use Template Haskell [Sheard and Jones
2002] to load the PowerPC data ﬁle at compile time, parse it, and then use Template Haskell to
generate code for an eﬃcient disassembler based on the TableGen information. Note that we trade
runtime eﬃciency in exchange for much more work at compile-time: it can take several minutes
to compile all of Dismantle. This is a theme that would continue to reappear as we moved in the
direction of increased automation.
2.3.2 Semi-Automated PowerPC Semantics Using SemMC. Just like with disassembling PowerPC,
we sought to futher automate the process of encoding the semantics of PowerPC instructions into
Macaw. Luckily for us, Heule et al. [2016] had recently published work on how to automatically
generate formal semantics for x86-64using a techique called stratiﬁed synthesis. Although this work
came out well after we hand-wrote our own formal semantics for x86-64, we decided to apply strat-
iﬁed synthesis when developing PowerPC semantics. We developed a library for performing this
form of synthesis (for PowerPC and for other ISAs) and named it SemMC (Semantics of Machine
Code).
   The SemMC library is designed to learn machine code semantics by starting with a core base set
of instructions for which the semantics are hand-written. Using this base set, we execute SemMC
on a series of fuzzer-generated machine states and instructions and use the results to learn the
semantics of instructions that are not in the base set. To further increase our conﬁdence that the
2 Typically, the only time where we need to modify the TableGen data for Dismantle’s purposes is to work around LLVM

bugs.


                               Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:16                                                                                                        Scott et al.


learned semantics are correct, we run the randomly generated machine states on actual PowerPC
hardware and use that as an oracle for what behavior should be considered correct. We repeat this
process until we have a complete formal description of the ISA’s semantics. In this sense, SemMC’s
stratiﬁed synthesis is semi-automated: some manual eﬀort is required to describe the semantics of
the base set, but everything else is fully automated.
   Much like with the semantics implementation in Macaw-x86, the semantics of SemMC base
set instructions are speciﬁed using a DSL. For example, here are the semantics of PowerPC’s nand
instruction in SemMC:
   definePPCOpcode NAND xform3c $ \ rA rB rS -> do
     comment " NAND ␣ (X - form ) "
     let res = bvnot ( bvand ( Loc rS ) ( Loc rB ))
     defLoc rA res
   Here, definePPCOpcode takes the instruction name and what instruction form to use.3 We use
xform3c , which indicates an X-form instruction with three operands. These operands are then
bound as rA, rB, and rC, which can then be used in the instruction’s deﬁnition. Finally, we use
defLoc to store the result of performing a bitwise-AND of the values from the rS and rB operands
into the location that the operand rA uses.
   SemMC converts the DSL into an intermediate language called What4. What4 programs are
stored on disk using an S-expression–based representation so that upstream programs (e.g., Macaw-
PPC) can parse and interpret the semantics they contain. For example, the What4 representation
of the nand semantics above is the following S-expression:
   ; ; NAND ( X-form )
   (( operands
     (( rA Gprc )
       ( rB Gprc )
       ( rS Gprc )))
     ( in
       ( op . rS op . rB loc . IP ))
     ( defs
       (( op . rA
         ( with
           ()
           ( bvnot
             ( bvand op . rS op . rB ))))
         ( loc . IP
           ( with
             ()
             ( bvadd loc . IP # x0000000000000004 ))))))
   The What4 representation of SemMC semantics explicitly indicate which operands are inputs
or outputs (via the in section), and it precisely captures how each output is modiﬁed when invok-
ing the instruction. In addition to updating the rA operand, the What4 version also updates the
instruction pointer IP, which is a lower-level detail that was elided in the DSL encoding.


3 Instruction forms describe how instructions are encoded in PowerPC. It is not essential to understand how instruction

forms work to read this section.


Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                        1:17


                             via oﬃcial ARM
                            XML speciﬁcation               Dismantle-ARM-XML
      AArch32 binary
                                                       (AST of dismantled instructions)
                                             RM
                                      c ial A tion
                                   oﬃ        ca
                                via speciﬁ
                                   L
                                XM
                                                                        via
      ASL-Translator via Crucible SemMC-AArch32                    Macaw-SemMC             Macaw-AArch32
      (Crucible CFG)              (What4 program)                                           (Macaw CFG)


Fig. 8. The architecture of Macaw-AArch32, describing the process of going from an AArch32 binary to a
Macaw CFG.


   The DSL is a convenient way for humans to write What4 semantics in the base set, but SemMC
also needs to be able to synthesize What4 semantics based on fuzzing. This is a more complicated
process, as SemMC must be able to reason about how a machine’s state updates when invoking
an instruction, and it must be able to do this where not all parts of the machine state are known
ahead of time—that is, when some parts of the machine state are symbolic.
   To make this process simpler, SemMC leverages the Crucible [Christiansen et al. 2019] sym-
bolic execution library. Crucible is primarily designed for imperative programming languages,
such as C or Rust, but Crucible also works well for machine code as well. SemMC leverages Cru-
cible when synthesizing What4 semantics for instructions not in the base set.
   Finally, once we have What4 semantics for all PowerPC instructions, we translate the What4
programs into Macaw CFGs using the Macaw-SemMC library. As was the case with Dismantle,
we do not want to perform all of this conversion at runtime, as we would need to read many,
many What4 S-expression ﬁles in order to look up the semantics for all of the instructions used in
a typical PowerPC program. As such, Macaw-SemMC uses Template Haskell to look up all What4
S-expression ﬁles at compile time and generate Macaw CFG–based semantics for each PowerPC
instruction, thereby avoiding the need to consult any What4 ﬁles at runtime.
   The payoﬀ of introducing SemMC as part of the semantics translation is that we gain a sig-
niﬁcant amount of automation in the overall process, thereby avoiding some of the maintenance
headaches that pervade Macaw-x86’s fully manual approach to semantics. There is a cost to doing
so, however: SemMC’s extra layers of abstraction make it so that it approximately two minutes to
compile the semantics for the entire PowerPC ISA.

2.4    Macaw-AArch32: An Even More Automated Dialect
Using SemMC to automate the development of Macaw-PPC oﬀered signiﬁcant advantages in how
conﬁdent we were in the resulting PowerPC semantics’ correctness, and it made the code more
maintainable as well. The SemMC approach is not foolproof, however. SemMC still requires human
beings to curate semantics for base set instructions by hand, and while the size of the base set is
smaller than the size of the overall ISA, curating the base set can still be a tedious (and potentially
error-prone) process.
   When developing Macaw-AArch32, a Macaw dialect for the 32-bit ARM ISA, we had an op-
portunity to develop the level of automation even further. ARM maintains machine-readable, ex-
ecutable speciﬁcations of every instruction [Reid 2016], which gives Macaw-AArch32 an oﬃcial

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:18                                                                                            Scott et al.


                                                     GRIFT
                                                                                  Macaw-RISCV
                    RISC-V binary             (AST of disassembled
                                                                                  (Macaw CFG)
                                                  instructions)

Fig. 9. The architecture of Macaw-RISCV, describing the process of going from an RISC-V binary to a Macaw
CFG.


source of truth for how to disassemble and interpret any given instruction. Combining the oﬃcal
ARM speciﬁcations with Template Haskell allows us to automate almost every aspect of Macaw-
AArch32’s development.
   The architecture of Macaw-AArch32 is pictured in Figure 8. Like Macaw-PPC, Macaw-AArch32also
relies on the Dismantle package in order to disassemble binaries. One notable diﬀerence in how
Dismantle’s PowerPC and AArch32 dialects work is that Dismantle uses LLVM TableGen data
for PowerPC, whereas it uses the ARM XML speciﬁcations for AArch32. Note that the construct-
ing parse tables via the XML speciﬁcations is quite slow: it takes over an hour to build tables for
the entire ISA. As such, we pre-compute the parse tables and store them on disk so that they can
simply be loaded directly during subsequent rebuilds of Dismantle.
   There is also a SemMC dialect for AArch32, but unlike the SemMC dialect for PowerPC, it does
not generate semantics for ARM instructions using stratiﬁed synthesis. Instead, it uses a dedicated
library (named ASL-Translator) to convert the ARM XML speciﬁcation’s semantics directly into
the What4 intermediate language that SemMC uses. The XML speciﬁcation is written in ASL [Reid
2016], a custom-purpose imperative programming language with a strong types. As it turns out,
the typing discipline that ASL uses is a natural ﬁt for Crucible, so ASL-Translatorheavily relies
on Crucible to translate the imperative, ASL-based semantics into a purely functional, What4-
based encoding.
   Note that ASL-Translator is almost, but not completely, automated. ASL-Translator man-
ually deﬁnes a handful of primitives to give semantics to low-level ASL operations (e.g., bitvec-
tor slicing, querying the program counter value, etc.) This is by far the trickiest part of ASL-
Translator to write, and the vast majority of bug reports ultimately step from incorrectly im-
plementing these primitives.
   Like Macaw-PPC, Macaw-AArch32’s heavy use of Template Haskell (both in ASL-Translatorand
in other parts of the dialect) incurs a signiﬁcant compile-time performance penalty. In fact, the
performance penalty is even more severe for Macaw-AArch32: it takes well over 5 minutes to
compile the parts of the dialect that rely on ASL-Translator-generated semantics. While it is
likely that these times could be improved by working harder to reduce the size of the generated
code, this reﬂects the general trend that the more one uses Template Haskell, the longer one has
to wait.

2.5    Macaw-RISCV: Revisiting a Manually-Written Dialect
The most recently introduced Macaw dialect is Macaw-RISCV, which targets the RISC-V archi-
tecture. The architecture of Macaw-RISCV is pictured in Figure 9. In stark contrast to previous
Macaw dialects, which have moved increasingly in the direction of automatically generating dis-
assemblers and semantics for their respective ISAs, Macaw-RISCV implements its RISC-V disas-
sembler and semantics completely by hand. This choice was motivated by the fact that RISC-V
adheres to the reduced instruction set computer (RISC) philosophy. The base set of RISC-V in-
structions (not including extensions) only consists of 48 instructions, which are composed of a

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                        1:19


                                     Manual–Automated Spectrum
      Fully manual                                                                          Fully automated
                             M ac                 M ac            M ac            M ac
                                    aw-                  aw-             aw-             aw-
                                       RISC                 x86             PPC             AAr
                                              V                                                c h32


Fig. 10. How much automation each Macaw dialect requires to implement on a scale from “Fully manual”
(entirely written by humans) to “Fully automated” (derived entirely from external sources by machines).


relatively small number of diﬀerent opcodes. As such, it is viable to hand-write a Macaw dialect
for RISC-V.

2.6   The Manual-Automated Spectrum
Each Macaw dialect exists on a spectrum of how much automation is used to implement the code
supporting the dialect’s ISA, as depicted in Figure 10. One far end of the spectrum is hand-writing
all of the code (e.g., Macaw-RISCV). The opposite end of the spectrum is fully automating the
generation of all ISA-related code (no dialect meets this criterion exactly, but Macaw-AArch32
comes the closest).
   Having developed four Macaw dialects, we have honed some intuition regarding whether to
use a hand-written approach, an automated approach, or somewhere in between when creating a
new dialect. There are various questions one must ask to determine which approach is right for a
given ISA:
    • How many diﬀerent instructions are there? It is possible to exhaustively go through all of
       the instructions in a small, RISC architecture, but for non-RISC architectures, the pain of
       going through every instruction will be more pronounced.
    • How clear is the ISA speciﬁcation regarding instruction semantics? Diﬀerent ISA semantics
       are written with diﬀerent levels of formality. For instance, the ARM XML speciﬁcation is
       written with extreme formality, while the Intel x86-64 ISA manual is less so, sometimes re-
       quiring humans to interpret dense English-language prose in order to determine how certain
       instructions behave. For the latter case, a SemMC-like approach can help.
    • How tolerant are you of long compile times? While automatically generating code with Tem-
       plate Haskell can increase ISA coverage and conﬁdence in the generated code, it comes with
       a severe downside of noticeably increasing compile times. It is worth asking the question of
       whether this compile-time slowdown is acceptable for a given project.

3 CASE STUDIES
3.1 Reopt
Reopt [Hendrix et al. 2019] is an optimization tool that lifts functions in a compiled binary into
LLVM bitcode, optimizes the intermediate bitcode, and then recompiles it into a new executable.
Reopt currently supports x86-64 binaries compiled in the ELF format for Linux. The Macaw li-
brary began its life as an internal component of the Reopt tool, and much of Macaw’s design
reﬂects considerations that were important at the time of Reopt’s development. The source code
for Reopt is publicly available at https://github.com/GaloisInc/reopt.
  The primary challenge in designing a tool like Reopt is going from Macaw’s IR, which only
has very minimal type information associated with each basic block, to the LLVM IR, which has a
comparatively richer type system. At the Macaw level, most values in general-purpose registers

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:20                                                                                                  Scott et al.



                      Macaw         Block recovery                   Constraint              Reopt
                                                                     generation


Initial entry            Incremental                                 Constraint
   points              block discovery                                solving

                                 New entry points
                                    identiﬁed                      Func recovery           LLVM gen


                                     Fig. 11. Reopt’s function recovery loop.




look like integers, but when Reopt outputs LLVM bitcode, it is helpful to distinguish between
integers, structs, pointers, and function pointers.
   To this end, Reopt includes a type-based function recovery pass, which is depicted in Figure 11.
Starting from a list of initial entry point functions (which are either inferred from the binary or
user-speciﬁed), the tool calls Macaw to discover the closure of basic blocks reachable from the
currently known blocks. Once the basic blocks have been recovered (c.f. Section 2.1.5), Reopt
performs a demand analysis, allowing it to compute the x86-64 arguments and return registers
on a per-block basis, aggregating them into register “demand sets” for entire functions, which are
then synthesized into appropriate argument and return values for the whole function.
   At this point, we only know the size of registers, but not whether they contain integers, ﬂoating-
point values, or, for those registers whose size matches that of virtual addresses for the architec-
ture, data or code pointers. However, there is information in the instruction ﬂow that can help
distinguish between all these cases, sometimes uniquely identifying what high-level type a reg-
ister should have. In order to produce better LLVM code, Reopt will gather constraints for all
intermediate registers, function arguments, and return values. For instance, a register ﬂowing into
the memory operand of a memory operation ought to be some pointer, while a value coming out of
a division operation must be numeric. Reopt will solve these constraints to determine a candidate
type for every function. Reopt also has some experimental support for row types, allowing it to
recover structural types, including recursive ones such as linked lists.
   During this process, Reopt may uncover calls to other functions, in which case Macaw’s code
discovery will need to be invoked once more. For instance, if a function’s argument is determined
to hold function pointers, all concrete values ﬂowing into this argument position can be safely
added to the candidate entry points pool. Thanks to Macaw’s incremental design, Reopt is able
to resume block discovery with those new entry points without incurring duplicate work. Once
all of the constraints are solved, the ﬁnal output is an LLVM program consisting of all the function
deﬁnitions that have been recovered, which now have much richer types.

3.1.1 Reopt Type Constraints. Reopt’s approach to reverse engineering types for assembly func-
tions is loosely based on the TIE system described in Lee et al. [2011]. The type system presented
in that work is slightly more sophisticated than what Reopt needs. For instance, Reopt generates
LLVM, which does not distguish between the types of signed and unsigned integers, so Reopt does
not bother to track this information. Likewise, where TIE relies on value-set analysis to get more

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                        1:21


precise oﬀset information in structured types, Reopt relies on Macaw’s symbolic oﬀsets, which
may either be concrete oﬀsets or opaque to its analysis.
    Ultimately, Reopt is concerned with distinguishing pointers from non-pointer values. Without
the type inference pass, Reopt would lift all pointer arithmetic to integer arithmetic and would
have to introduce an LLVM inttoptr cast every time such a value would be in address position in a
memory load or store instruction. This is important because treating pointers as integers up to the
last second inhibits LLVM optimizations and obfuscates pointer manipulation for both human and
tool consumers of the lifted IR. Instead, pointer arithmetic can be lifted to pointer-manipulating
instructions, describing them using types with richer structure, beneﬁting the readability of the
lifted code, and enabling more complex code analyses and transformations. Knowing these types,
Reopt can produce the more appropriate getelementptr LLVM instruction, operating over typed
pointers. We give an instance of such an output change in Figure 12.

     ;; Original x86 -64 instruction
     cmpb   $0x30 ,0 x3 (% rax )                         ; in AT & T syntax
     cmp    BYTE PTR [ rax +0 x3 ] ,0 x30                ; in Intel syntax

     ;; Translation without type inference
     ;; % t0 corresponds to % rax and is given type i64
     % t1 = add i64 % t0 , 0 x3
     % t2 = load i8 , i8 * inttoptr ( i64 % t1 to i8 *)
     % t3 = icmp eq i8 % t2 , 0 x30

     ;; Translation with type inference
     ;; % t0 corresponds to % rax and is given type {{ i8 , i8 , i8 } ,{ i8 , i8 }}*
     % t1 = getelementptr {{ i8 , i8 , i8 } ,{ i8 , i8 }} ,
                             {{ i8 , i8 , i8 } ,{ i8 , i8 }}* % t0 , i32 0, i32 1
     % t2 = getelementptr { i8 , i8 }, { i8 , i8 }* % t1 , i32 0, i32 0
     % t3 = load i8 , i8 * % t2
     % t4 = icmp eq i8 % t3 , 0 x30

Fig. 12. Example of the impact of Reopt ’s type inference on LLVM output. getelementptr instructions only
help LLVM’s type system and have no performance impact.


3.1.2 Reopt Limitations. Reopt’s function recovery, as sophisticated as it is, may still not be
enough to infer a precise type for a function. One reason is that Macaw’s code discovery is not
perfect, and when it cannot process all of the instructions in a basic block, it will conservatively
bail out and possibly omit some instructions that are crucial for inferring the types of the block’s
inputs and outputs. To help alleviate this problem, Reopt includes an option to supply header ﬁles,
as well as debug information ﬁles, which contain function type signatures that Reopt should as-
sume when it encounters known functions. This is particularly useful for external function calls
(e.g., from libc), where Reopt either does not have the entire function deﬁnition available, or the
full deﬁnition is suﬃciently low-level that analyzing it proves costly.
   Recent work has also been aimed at addressing limitations when working with stripped binaries
with no debug sections. Such binaries have historically proven challenging for Reopt, as the only
entry point initially known for such binaries is the one listed as entry point of the executable.
Typically, this will be the address of a symbol that would have been named _start before stripping,
and whose code does not contain an explicit call to the address of the main symbol.

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:22                                                                                          Scott et al.


   void _start () {
     // Some scaffolding code , ending with :
     __libc_start_main (& main ); // `main ` called back when C runtime ready
   }
   Instead, the start routine will call the C run-time scaﬀolding symbol, __libc_start_main , passing
the address of the main symbol as an argument to it. As such, the binary does not contain any
explicit call to main, and Macaw will subsequently miss the main function and stop exploring right
away. This is where the type-driven analysis of Reopt can help. In this case, Reopt knows that
__libc_start_main expects a function pointer thanks to the libc debug information. Upon noticing
the address of main ﬂowing into a call to __libc_start_main , Reopt will instruct Macaw to resume
block discovery with this new address as a function entry point.
   There are three reasons why we designed Reopt to use a type-based approach. First, Reopt
favors this approach over heuristical ones, as this not only applies to discovering the main symbol
in a stripped binary, but also any function address passed to a higher-order function, be it in an
external library or locally within the binary being lifted. Second, Reopt prefers a discovery-guided
approach, where we only inspect bytes of the code section when we witness an explicit ﬂow of
control to it, over a greedy inspection of the entire code section, as it still allows us to avoid false
positives such as dead code, nop paddings, or misaligned decodings. Finally, Reopt favors a type-
aware approach to a greedy inspection of all pointer-sized values that could look like they could
point to code, as some ﬂoating-point values may also look like pointers to the code segment, and
this would also yield false positives. In all the above cases, not only does Reopt ﬁnd known-to-be-
reachable addresses, it also discovers them in a context where it knows the type of their arguments
and return value, which allows Reopt to properly lift these basic blocks into well-typed LLVM
functions.


3.2    SAW
The Software Analysis Workbench (SAW) [Dockins et al. 2016] is a veriﬁcation tool that can rea-
son about the behavior of imperative programs by proving them equivalent to functional spec-
iﬁcations. SAW supports a variety of diﬀerent source languages, including code written in C,
Java, Rust, and most relevantly for this work, x86-64. SAW has been successfully used to verify
a variety of industrial-strength cryptographic libraries written in a mixture of C and x86-64, in-
cluding the s2n Transport Layer Security (TLS) stack [Chudnov et al. 2018], the AWS LibCrypto
library [Boston et al. 2021], and the BLST library [Dodds 2020]. The source code for SAW is pub-
licly available at https://github.com/GaloisInc/saw-script.
   SAW ingests x86-64 machine code by leveraging Macaw to lift assembly instructions into a
Crucible control-ﬂow graph. Separately from the machine code itself, SAW also takes as input a
list of speciﬁcations that describe the intended behavior of each assembly function. These speci-
ﬁcations consist of Hoare-style pre- and post-conditions that describe the shape of memory and
the behavior of the function itself. SAW checks each function against its speciﬁcation by symboli-
cally executing the function’s CFG and ensuring that the conditions described in the function are
respected along the way, discharging any non-trivial proof goals to an SMT solver.
   Aside from checking functional correctness, SAW also checks that a function is memory safe.
In the context of a language like C, this is a well understood problem, as the C standard dictates
what it means for a C program to interact with memory in a valid way. The notion of memory
safety becomes blurrier with assembly code, however, as there are almost no universally accepted
rules on what constitutes safe reads and writes. The only guidelines that one can typically rely on


Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                        1:23


are the conventions used within a particular program, as well as the Application Binary Interface
(ABI) for calling external functions.
  SAW speciﬁcally targets programs with mixed C and x86-64 code where the C code controls the
program’s memory, and all x86-64 functions only ever access the C code’s memory. In this setting,
SAW can leverage Crucible’s LLVM-based memory model for modeling both types of code. This
means that SAW is able to prove all memory reads and writes in the x86-64 code are correct with
respect to the host language’s memory model. As a small example of how SAW’s x86-64 support
works, we will verify the behavior of a tiny increment assembly function that takes a single pointer
argument and increments the value it points to by one.
           increment :                                      // Equivalent C code :
             mov rax , [ rdi ]                              void increment ( uint64_t * i )
             add rax , 1                                    {
             mov [ rdi ], rax                                 * i += 1;
             ret                                            }
  We can write a SAW speciﬁcation increment_spec that captures the intended behavior:
                   let increment_spec = do {
                      ptr <- llvm_alloc ( llvm_int 64);
                      val <- llvm_fresh_var " val " ( llvm_int 64);
                      llvm_points_to ptr ( llvm_term val );
                      llvm_execute_fun c [ ptr ];
                      llvm_points_to ptr ( llvm_term {{ val + 1 }});
                   };
   This speciﬁcation declares a series of statements, where each statement before the llvm_execute_func
is a pre-condition and each statement after is a post-condition. The pre-conditions state that the
function accepts a single pointer argument that points to an arbitrary 64-bit LLVM integer value.
The post-condition states that after the function is invoked, the pointer argument will then point to
the initial integer value plus one. Again, we are leveraging LLVM to describe the shape of memory,
and all of the commands used here could apply to C functions just as much as x86-64 ones.
   The increment function can be checked against increment_spec by running:
       llvm_verify_x86 " ./ increment_bin " " increment " increment_spec z3 ;
   Here, increment_bin is the ELF binary that deﬁnes increment , and z3 is the SMT solver to dis-
charge proof goals to during symbolic execution. This is the only command that is machine code–
speciﬁc, as this is where Macaw is used to lift the assembly code in increment to a CFG and pass
it on to SAW’s symbolic execution engine. Although the llvm_verify_x86 command is speciﬁc to
the x86-64 ISA, it could very easily be extended to handle other architectures as well 4 .

3.3 Other Case Studies
   Ambient-Verifier. A veriﬁcation tool built on top of Macaw that evaluates whether or not
it is possible to trigger a weird machine (WM) [Dullien 2020] in a binary, i.e., a code execution
path that occurs outside of the intended speciﬁcation of the program. One challenging aspect of
triaging the presence of WMs is determining what environmental conditions—such as command-
line arguments, environment variables, or ﬁle system state—are strictly required to trigger the
WM, and which conditions are irrelevant to the WM. To this end, Ambient-Verifier leverages
symbolic execution to make certain parts of the environment symbolic to explore the diﬀerent
4 For example, an llvm_verify_aarch32 command is planned: anonymized for review



                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:24                                                                                        Scott et al.


execution paths, which can help users of the tool determine which parts of the environment are
most relevant to the WM at hand.
   Many WMs reside in a shared library that a binary depends on, such as libc. To this end, it is
important to be able symbolically execute the code inside of low-level shared libraries, but this can
be diﬃcult due to how often these libraries contain low-level functions and system calls. While
Crucible can simulate this type of code, the performance is often impractically slow.
   To allow the tool to execute shared libraries in an eﬃcient manner, Ambient-Verifier includes
a mechanism for overriding the behavior of functions and system calls. For instance, Ambient-
Verifier can intercept calls to the getppid system call and replace it with a version that returns
a fresh, symbolic integer as the process ID. While this does not faithfully emulate the actual im-
plementation of getppid, this can be an acceptable compromise to make to speed up symbolic
execution, especially for WMs where the behavior of getppid is irrelevant.
   The source code for Ambient-Verifier is publicly available at https://github.com/GaloisInc/ambient-veriﬁe

   PATE (Patches Assured up to Trace Equivalence). A relational veriﬁcation [Barthe et al. 2011,
2013] tool that proves that a property about a binary’s observable behavior holds before and after a
patch is applied to the binary’s code. A typical use case for PATE is verifying that security-oriented
patches ﬁx undesirable behaviors in a binary without adversely aﬀecting other parts of the binary.
First, PATE splits the original and patched binaries into conﬂict-free acyclic regions (CFARs). A
CFAR is a collection of basic blocks with control ﬂow between them, but with no backedges. PATE
uses the original binary as the behavioral speciﬁcation, inferring frame conditions for each CFAR.
PATE then symbolically executes each CFAR in the original and patched binary, and if the patched
binary fails to satisfy the frame condition inferred from the original binary, then PATE produces
a summary of the conditions that lead to exhibiting diﬀerent behavior.
   The source code for PATE is publicly available at https://github.com/GaloisInc/pate.

   Cerridwen. A tool that quantiﬁes similarities among x86-64 binaries. The algorithm for ranking
similarity largely follows the description in [David et al. 2017]. Cerridwen decomposes a binary
into strands—that is, data-ﬂow slices of basic blocks [David et al. 2016]—which are used as units
of measurement for comparing how similar the binary is to a corpus of known binaries. The basic
blocks resulting from Macaw’s code discovery are used to compute each strand, which consists
of the operations that lead to the computation of a single value within a basic block.
   The source code for Cerridwen is publicly available at https://github.com/GaloisInc/cerridwen.

   Renovate. A static binary rewriting library for ELF binaries. Using Renovate, one can add,
remove, or rewrite basic blocks in a statically linked binary without needing to execute it. The core
of Renovate’s rewriting machinery is architecture-independent, and there exist x86-64, PowerPC,
and AArch32 backends. One particular use case for Renovate is achieving binary diversity [Cohen
1993]—that is, randomizing the layout of basic blocks to make it more resilient to attackers.
   The source code for Renovate is publicly available at https://github.com/GaloisInc/renovate.

  MCTrace. An x86-64 and PowerPC binary instrumentation tool that is heavily inspired by
DTrace [Cantrill et al. 2004; Gregg and Mauro 2011], but does not require any special kernel sup-
port or recompiling the program to be traced. MCTrace reads the same tracing speciﬁcations as
DTrace (written in the D language) and leverage’s Renovate’s binary rewriting capabilities to in-
sert probes into binaries. The traces that these probes generate can support a variety of diﬀerent
systems. For example, MCTrace-instrumented binaries have been successfully run on bare metal
using an MPC5777C PowerPC microcontroller.
  The source code for MCTrace is publicly available at https://github.com/GaloisInc/mctrace.

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                        1:25


   Surveyor. A library for interactively debugging LLVM, JVM, x86-64, and PowerPC programs,
using an interface inspirted by gdb and emacs. Notably, Surveyor is a symbolic debugger: it sup-
ports setting breakpoints during Crucible’s symbolic execution, and it can inspect the values of
arguments to a basic block, which may possibly be symbolic themselves. Surveyor also supports
stepping through a binary’s execution and recording a trace of symbolic events, which can be
replayed later.
   The source code for Surveyor is publicly available at https://github.com/GaloisInc/surveyor.

4   RELATED WORK
   Reverse Engineering Frameworks. The closest tools to Macaw in terms of capabilities are indus-
trial binary analysis frameworks such as Ghidra [Rohleder 2019], Binary Ninja [Vector35 2023a],
Radare2 [Alvarez 2023], and IDA Pro [Eagle 2011]. Like Macaw, these frameworks handle a mul-
titude of binary analysis tasks such as reverse engineering, disassembly, decompilation, and static
analysis. Each framework also includes a native IR that abstracts some low-level architectural
details—for example, Ghidra’s P-Code [Naus et al. 2023] and others [Radare2 Book 2023; Rolles
2018; Vector35 2023b].
   The main diﬀerence between these tool and Macaw lies in their respective design goals. Ghidra
and similar are intended for industrial-strength reverse engineering applications. Macaw is in-
tended to be a research-oriented toolkit for rapidly building novel binary analysis tools. For the
user, these binary analysis frameworks oﬀer a polished experience which Macaw does not seek
to provide. For example, Ghidra features a full, graphical IDE that allows users to visualize disas-
sembled programs, label ﬁelds, rename variables, and more. We have experimented with diﬀerent
UI approaches via the Surveyor tool, but as exploratory tools, not fully-developed capabilities.
   Macaw’s greatest strength is providing a platform to build new binary analysis tools from
scratch. Frameworks such as Ghidra typically support plugins via some API, but this is usually
meant for extending the existing functionality rather than building standalone applications. In
this sense, Macaw occupies a diﬀerent niche in the design space. Indeed, it is possible to build a
custom analysis tool with Macaw and integrate its capabilities into Ghidra’s IDE.
   Another diﬀerence is Macaw’s intrinsically typed IR, which encodes invariants about well-
formedness at the type level. This guarantees that IR values are valid in the context of the analyses
they want to perform. To our knowledge, none of the other IRs mentioned earlier employ a com-
parable approach to IR validity. There have been eﬀorts to give formal semantics to P-Code, but
this eﬀort is external to the actual P-Code representation used in Ghidra [Naus et al. 2023].
   Binary Lifting. Reopt is one tool in the large space of binary lifters and rewriters; see Schulte et al.
[2022] for a comparison. Reopt lifts machine code to the LLVM IR, which puts it in the same
category as lifters such as McSema [Dinaburg and Ruef 2014], SecondWrite [Anand et al. 2013],
RevGen [Chipounov and Candea 2011], and rev.ng [Di Federico et al. 2017]. It diﬀers primarily in
the style of LLVM code that it produces. Most LLVM-based lifters map processor registers directly
to LLVM variables with an explicit stack, which results in atypical LLVM code. Reopt uniﬁes the
machine code stack with the LLVM stack in an eﬀort to produce more “human-friendly” LLVM.
   Symbolic Execution of Machine Code. Macaw leverages Crucible’s support for forward sym-
bolic execution [King 1976; Schwartz et al. 2010] to analyze the behavior of programs. Other binary
analysis frameworks use symbolic execution as well, examples of which include Angr [Shoshitaishvili et al.
2016], BAP [Brumley et al. 2011], Triton [Saudel and Salwan 2015], Mayhem [Cha et al. 2012], and
KLEE-Native [Vegasena and Goodman 2019]. Most of these leverage dynamic symbolic execution
(also known as concolic execution), while Macaw uses static symbolic execution by lifting a binary
to a high-level IR and analyzing it using symbolic values.

                             Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:26                                                                                       Scott et al.


   This reﬂects a diﬀerence in the types of problems we have typically targeted with Macaw. Other
tools typically use symbolic execution in bug-ﬁnding (for which dynamic symbolic execution is
well-suited) while we have often used Macaw to support exhaustive exploration or formal veriﬁ-
cation (for which static symbolic execution is necessary).
   Angr is static insofar as it lifts binaries to an IR and performs additional analyses, but it is
also provides dynamic analyses such as a symbolic-assisted fuzzer [Stephens et al. 2016]. This is
similar to our Macaw-based tool Ambient-Verifier, but Angr uses a combination of static and
dynamic symbolic execution depending on the use case. For example, Angr can directly interact
with ﬁles and the operating system, whereas Ambient-Verifier can only model ﬁlesystem and
OS interactions in an abstract way.
   Another important distinction is that Angr often concretizes certain types of symbolic values
during execution, depending on the concretization strategy that the user chooses. With the default
concretization strategy, Angr will concretize symbolic addresses that are written to, as well as
symbolic length values passed to the read() and write() system calls. This is done primarily for
performance reasons, as preserving all symbolic values can often lead to VCs that are prohibitively
expensive to solve for. By contrast, Ambient-Verifier (and Macaw more generally) propagates
symbolic values throughout its analyses. This means that Ambient-Verifier will explore more
paths by default, but perhaps at the expense of additional analysis time.

   Formal Veriﬁcation of Machine Code. Our Macaw-based veriﬁcation tool SAW is similar to Vale [Bond et al.
2017; Bosamiya et al. 2020; Fromherz et al. 2019], a tool for writing veriﬁed x86-64 assembly code.
Vale integrates with Low* [Protzenko et al. 2017] to allow veriﬁcation of mixed C/x86-64 code.
Vale and Low* are used in the implementation of EverCrypt [Protzenko et al. 2020], a library of
veriﬁed C/x86-64 cryptography.
   Unlike Vale and Low*, SAW is primarily used to verify pre-existing C/x86-64 code, whereas
Vale and Low* are primarily meant for writing code and proofs simultaneously. Because SAW
veriﬁes x86-64 code as-is, SAW makes essential use of Macaw’s binary lifting as part of the overall
veriﬁcation process. Vale, on the other hand, generates x86-64 code from a veriﬁed domain-speciﬁc
language, so it does not rely on binary lifting.

5      CONCLUSIONS AND NEXT STEPS
Macaw has been a keystone technology for us in developing binary analysis tools over a decade.
Macaw’s core IR builds in multiple features that let us build rapidly and with conﬁdence, while
its symbolic execution capabilities have enabled a diverse range of testing and veriﬁcation tools.
   Our current focus is on improving Macaw’s code discovery capabilities. A common pain point is
discovering the targets of calls through jump tables—by default, Macaw uses simple pattern-based
heuristics. We have developed Macaw-Refinement (Section 2.1.6) as a more accurate alternative.
However, its reliance on SMT solving can increase discovery time in a way that is unacceptable for
many applications. We are currently investigating how to limit SMT calls to only the places that
the pattern-based heuristic fails. Our eventual goal is to make Macaw-Refinement fast enough
to be the default code discovery algorithm which would bring many more target binaries within
reach.

ACKNOWLEDGMENTS
This work relates to Department of Navy award #N00014-22-1-2588 issued by the Oﬃce of Naval
Research. Any opinions, ﬁndings, and conclusions or recommendations expressed in this material
are those of the author(s) and do not necessarily reﬂect the views of the Oﬃce of Naval Research.

Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                             1:27


REFERENCES
Alfred V. Aho, Ravi Sethi, and Jeﬀrey D. Ullman. 1986. Compilers: principles, techniques, and tools. Addison-Wesley Longman
   Publishing Co., Inc., USA.
Sergi Alvarez. 2023. Libre and Portable Reverse Engineering Framework. https://www.radare.org/n/
Kapil Anand, Matthew Smithson, Khaled Elwazeer, Aparna Kotha, Jim Gruen, Nathan Giles, and Rajeev Barua. 2013. A
   Compiler-Level Intermediate Representation Based Binary Analysis and Rewriting System. In Proceedings of the 8th
   ACM European Conference on Computer Systems (Prague, Czech Republic) (EuroSys ’13). Association for Computing
   Machinery, New York, NY, USA, 295–308. https://doi.org/10.1145/2465351.2465380
Gogul Balakrishnan and Thomas Reps. 2004. Analyzing Memory Accesses in x86 Executables. In Compiler Construction,
   Evelyn Duesterwald (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 5–23.
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2011. Relational Veriﬁcation Using Product Programs. In FM 2011:
   Formal Methods, Michael Butler and Wolfram Schulte (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 200–214.
   https://doi.org/10.1007/978-3-642-21437-0_17
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2013. Beyond 2-Safety: Asymmetric Product Programs for Relational
   Program Veriﬁcation. In Logical Foundations of Computer Science, Sergei Artemov and Anil Nerode (Eds.). Springer Berlin
   Heidelberg, Berlin, Heidelberg, 29–43. https://doi.org/10.1007/978-3-642-35722-0_3
Barry Bond, Chris Hawblitzel, Manos Kapritsos, K. Rustan M. Leino, Jacob R. Lorch, Bryan Parno, Ashay Rane, Srinath
   Setty, and Laure Thompson. 2017. Vale: Verifying High-Performance Cryptographic Assembly Code. In Proceedings
   of the 26th USENIX Conference on Security Symposium (Vancouver, BC, Canada) (SEC’17). USENIX Association, USA,
   917–934.
Jay Bosamiya, Sydney Gibson, Yao Li, Bryan Parno, and Chris Hawblitzel. 2020. Veriﬁed Transformations and Hoare Logic:
   Beautiful Proofs for Ugly Assembly Language. In Software Veriﬁcation: 12th International Conference, VSTTE 2020, and
   13th International Workshop, NSV 2020, Los Angeles, CA, USA, July 20–21, 2020, Revised Selected Papers (Los Angeles, CA,
   USA). Springer-Verlag, Berlin, Heidelberg, 106–123. https://doi.org/10.1007/978-3-030-63618-0_7
Brett Boston, Samuel Breese, Joey Dodds, Mike Dodds, Brian Huﬀman, Adam Petcher, and Andrei Stefanescu. 2021. Veriﬁed
   cryptographic code for everybody. In CAV 2021. https://doi.org/10.1007/978-3-030-81685-8_31
David Brumley, Ivan Jager, Thanassis Avgerinos, and Edward J. Schwartz. 2011. BAP: A Binary Analysis Platform. In Com-
   puter Aided Veriﬁcation, Ganesh Gopalakrishnan and Shaz Qadeer (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
   463–469. https://doi.org/10.1007/978-3-642-22110-1_37
Bryan M. Cantrill, Michael W. Shapiro, and Adam H. Leventhal. 2004. Dynamic Instrumentation of Production Systems.
   In Proceedings of the Annual Conference on USENIX Annual Technical Conference (Boston, MA) (ATEC ’04). USENIX
   Association, USA, 2. https://doi.org/10.5555/1247415.1247417
Sang Kil Cha, Thanassis Avgerinos, Alexandre Rebert, and David Brumley. 2012. Unleashing Mayhem on Binary Code. In
   2012 IEEE Symposium on Security and Privacy. 380–394. https://doi.org/10.1109/SP.2012.31
Vitaly Chipounov and George Candea. 2011. Enabling Sophisticated Analyses of ×86 Binaries with RevGen. In Proceedings
   of the 2011 IEEE/IFIP 41st International Conference on Dependable Systems and Networks Workshops (DSNW ’11). IEEE
   Computer Society, USA, 211–216. https://doi.org/10.1109/DSNW.2011.5958815
David Thrane Christiansen, Iavor S. Diatchki, Robert Dockins, Joe Hendrix, and Tristan Ravitch. 2019. Dependently
   Typed Haskell in Industry (Experience Report). Proc. ACM Program. Lang. 3, ICFP, Article 100 (July 2019), 16 pages.
   https://doi.org/10.1145/3341704
Andrey Chudnov, Nathan Collins, Byron Cook, Joey Dodds, Brian Huﬀman, Colm MacCárthaigh, Stephen Magill, Eric
   Mertens, Eric Mullen, Serdar Tasiran, Aaron Tomb, and Eddy Westbrook. 2018. Continuous Formal Veriﬁcation of
   Amazon s2n. In Computer Aided Veriﬁcation, Hana Chockler and Georg Weissenbacher (Eds.). Springer International
   Publishing, Cham, 430–446. https://doi.org/10.1007/978-3-319-96142-2_26
Frederick B. Cohen. 1993. Operating System Protection through Program Evolution. Comput. Secur. 12, 6 (oct 1993), 565–584.
   https://doi.org/10.1016/0167-4048(93)90054-9
Yaniv David, Nimrod Partush, and Eran Yahav. 2016. Statistical Similarity of Binaries. SIGPLAN Not. 51, 6 (jun 2016),
   266–280. https://doi.org/10.1145/2980983.2908126
Yaniv David, Nimrod Partush, and Eran Yahav. 2017. Similarity of Binaries through Re-Optimization. In Proceedings of the
   38th ACM SIGPLAN Conference on Programming Language Design and Implementation (Barcelona, Spain) (PLDI 2017).
   Association for Computing Machinery, New York, NY, USA, 79–94. https://doi.org/10.1145/3062341.3062387
Alessandro Di Federico, Mathias Payer, and Giovanni Agosta. 2017. rev.ng: a uniﬁed binary analysis framework
   to recover CFGs and function boundaries. In Proceedings of the 26th International Conference on Compiler Con-
   struction (Austin, TX, USA) (CC 2017). Association for Computing Machinery, New York, NY, USA, 131–141.
   https://doi.org/10.1145/3033019.3033028
Artem Dinaburg and Andrew Ruef. 2014. McSema: Static Translation of X86 Instructions to LLVM. In ReCon 2014 Confer-
   ence, Montreal, Canada. https://recon.cx/2014/slides/McSema.pdf


                                Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
1:28                                                                                                           Scott et al.


Robert Dockins, Adam Foltzer, Joe Hendrix, Brian Huﬀman, Dylan McNamee, and Aaron Tomb. 2016. Construct-
   ing Semantic Models of Programs with the Software Analysis Workbench. In Veriﬁed Software. Theories, Tools,
   and Experiments, Sandrine Blazy and Marsha Chechik (Eds.). Springer International Publishing, Cham, 56–72.
   https://doi.org/10.1007/978-3-319-48869-1_5
Joey Dodds. 2020. Announcing the ‘blst’ BLS Veriﬁcation Project. https://galois.com/blog/2020/09/announcing-the-blst-bls-veriﬁcation-p
Thomas Dullien. 2020. Weird Machines, Exploitability, and Provable Unexploitability. IEEE Transactions on Emerging Topics
   in Computing 8, 2 (2020), 391–403. https://doi.org/10.1109/TETC.2017.2785299
Chris Eagle. 2011. The IDA Pro Book: The Unoﬃcial Guide to the World’s Most Popular Disassembler. No Starch Press, USA.
Richard A. Eisenberg and Stephanie Weirich. 2012. Dependently Typed Programming with Singletons. SIGPLAN Not. 47,
   12 (sep 2012), 117–130. https://doi.org/10.1145/2430532.2364522
Aymeric Fromherz, Nick Giannarakis, Chris Hawblitzel, Bryan Parno, Aseem Rastogi, and Nikhil Swamy. 2019. A Veriﬁed,
   Eﬃcient Embedding of a Veriﬁable Assembly Language. Proc. ACM Program. Lang. 3, POPL, Article 63 (jan 2019),
   30 pages. https://doi.org/10.1145/3290376
Brendan Gregg and Jim Mauro. 2011. DTrace: Dynamic Tracing in Oracle Solaris, Mac OS X and FreeBSD (1st ed.). Prentice
   Hall Press, USA. https://doi.org/10.5555/1971960
Joe Hendrix, Guannan Wei, and Simon Winwood. 2019. Towards veriﬁed binary raising. In Workshop on Instruction Set
   Architecture Speciﬁcation (co-located with ITP 2019), Vol. 6.
Stefan Heule, Eric Schkufza, Rahul Sharma, and Alex Aiken. 2016. Stratiﬁed synthesis: automatically learning the x86-
   64 instruction set. In Proceedings of the 37th ACM SIGPLAN Conference on Programming Language Design and Imple-
   mentation (Santa Barbara, CA, USA) (PLDI ’16). Association for Computing Machinery, New York, NY, USA, 237–250.
   https://doi.org/10.1145/2908080.2908121
Intel. 2024. Intel 64 and IA-32 Architectures Software Developer’s Manual. https://www.intel.com/content/www/us/en/developer/articles/tec
James C. King. 1976.          Symbolic execution and program testing.           Commun. ACM 19, 7 (jul 1976), 385–394.
   https://doi.org/10.1145/360248.360252
John Launchbury and Simon L. Peyton Jones. 1995. State in Haskell. Lisp Symb. Comput. 8, 4 (dec 1995), 293–341.
   https://doi.org/10.1007/BF01018827
JongHyup Lee, Thanassis Avgerinos, and David Brumley. 2011. TIE: Principled Reverse Engineering of Types in Binary
   Programs. (2 2011). https://doi.org/10.1184/R1/6469466.v1
LLVM Project. 2024. TableGen Overview. https://llvm.org/docs/TableGen/
Nico Naus, Freek Verbeek, Dale Walker, and Binoy Ravindran. 2023. A Formal Semantics For P-Code. In Veriﬁed Software.
   Theories, Tools and Experiments.: 14th International Conference, VSTTE 2022, Trento, Italy, October 17–18, 2022, Revised Se-
   lected Papers (Trento, Italy). Springer-Verlag, Berlin, Heidelberg, 111–128. https://doi.org/10.1007/978-3-031-25803-9_7
Jonathan Protzenko, Bryan Parno, Aymeric Fromherz, Chris Hawblitzel, Marina Polubelova, Karthikeyan Bhargavan, Ben-
   jamin Beurdouche, Joonwon Choi, Antoine Delignat-Lavaud, Cédric Fournet, Natalia Kulatova, Tahina Ramananan-
   dro, Aseem Rastogi, Nikhil Swamy, Christoph M. Wintersteiger, and Santiago Zanella-Beguelin. 2020. EverCrypt: A
   Fast, Veriﬁed, Cross-Platform Cryptographic Provider. In 2020 IEEE Symposium on Security and Privacy (SP). 983–1002.
   https://doi.org/10.1109/SP40000.2020.00114
Jonathan Protzenko, Jean-Karim Zinzindohoué, Aseem Rastogi, Tahina Ramananandro, Peng Wang, Santiago Zanella-
   Béguelin, Antoine Delignat-Lavaud, Cătălin Hriţcu, Karthikeyan Bhargavan, Cédric Fournet, and Nikhil Swamy. 2017.
   Veriﬁed Low-Level Programming Embedded in F*. Proc. ACM Program. Lang. 1, ICFP, Article 17 (aug 2017), 29 pages.
   https://doi.org/10.1145/3110261
Radare2 Book. 2023. ESIL. https://book.rada.re/disassembling/esil.html
Alastair Reid. 2016. Trustworthy speciﬁcations of ARM® v8-A and v8-M system level architecture. In 2016 Formal Methods
   in Computer-Aided Design (FMCAD). 161–168. https://doi.org/10.1109/FMCAD.2016.7886675
Roman Rohleder. 2019. Hands-On Ghidra - A Tutorial about the Software Reverse Engineering Framework. In Proceed-
   ings of the 3rd ACM Workshop on Software Protection (London, United Kingdom) (SPRO’19). Association for Computing
   Machinery, New York, NY, USA, 77–78. https://doi.org/10.1145/3338503.3357725
Rolf Rolles. 2018. Hex-Rays Microcode API vs. Obfuscating Compiler. https://hex-rays.com/blog/hex-rays-microcode-api-vs-obfuscating-
Florent Saudel and Jonathan Salwan. 2015. Triton: Concolic execution framework. In Symposium sur la sécurité des tech-
   nologies de l’information et des communications (SSTIC).
Tom Schrijvers, Simon Peyton Jones, Manuel Chakravarty, and Martin Sulzmann. 2008.                      Type Checking with
   Open Type Functions. In Proceedings of the 13th ACM SIGPLAN International Conference on Functional Program-
   ming (Victoria, BC, Canada) (ICFP ’08). Association for Computing Machinery, New York, NY, USA, 51–62.
   https://doi.org/10.1145/1411204.1411215
Eric Schulte, Michael D. Brown, and Vlad Folts. 2022. A Broad Comparative Evaluation of X86-64 Binary Rewriters. In
   Proceedings of the 15th Workshop on Cyber Security Experimentation and Test (Virtual, CA, USA) (CSET ’22). Association
   for Computing Machinery, New York, NY, USA, 129–144. https://doi.org/10.1145/3546096.3546112


Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
Macaw: A Machine Code Toolbox for the Busy Binary Analyst                                                           1:29


Edward J. Schwartz, Thanassis Avgerinos, and David Brumley. 2010. All You Ever Wanted to Know about Dynamic Taint
   Analysis and Forward Symbolic Execution (but Might Have Been Afraid to Ask). In Proceedings of the 2010 IEEE Sympo-
   sium on Security and Privacy (SP ’10). IEEE Computer Society, USA, 317–331. https://doi.org/10.1109/SP.2010.26
Ryan Scott, Robert Dockins, Tristan Ravitch, and Aaron Tomb. 2021. Crux: Symbolic Execution Meets SMT-based Veriﬁca-
   tion (Competition Contribution). https://doi.org/10.5281/zenodo.6147218
Tim Sheard and Simon Peyton Jones. 2002. Template meta-programming for Haskell. In Proceedings of the 2002 ACM
   SIGPLAN Workshop on Haskell (Pittsburgh, Pennsylvania) (Haskell ’02). Association for Computing Machinery, New
   York, NY, USA, 1–16. https://doi.org/10.1145/581690.581691
Yan Shoshitaishvili, Ruoyu Wang, Christopher Salls, Nick Stephens, Mario Polino, Audrey Dutcher, John Grosen, Siji Feng,
   Christophe Hauser, Christopher Kruegel, and Giovanni Vigna. 2016. SoK: (State of) The Art of War: Oﬀensive Tech-
   niques in Binary Analysis. In IEEE Symposium on Security and Privacy.
Nick Stephens, John Grosen, Christopher Salls, Andrew Dutcher, Ruoyu Wang, Jacopo Corbetta, Yan Shoshitaishvili,
   Christopher Kruegel, and Giovanni Vigna. 2016. Driller: Augmenting fuzzing through selective symbolic execution..
   In NDSS, Vol. 16. 1–16.
Vivek Thampi. 2014. udis86: Disassembler Library for x86 and x86-64. https://github.com/vmt/udis86
Vector35. 2023a. Binary Ninja. https://binary.ninja/
Vector35. 2023b. Binary Ninja Intermediate Language: Overview. https://docs.binary.ninja/dev/bnil-overview.html
Sai Vegasena and Peter Goodman. 2019.                           Binary symbolic execution with KLEE-Native.
   https://blog.trailofbits.com/2019/08/30/binary-symbolic-execution-with-klee-native/
Brent A. Yorgey, Stephanie Weirich, Julien Cretin, Simon Peyton Jones, Dimitrios Vytiniotis, and José Pedro Magalhães.
   2012. Giving Haskell a Promotion. In Proceedings of the 8th ACM SIGPLAN Workshop on Types in Language Design and
   Implementation (Philadelphia, Pennsylvania, USA) (TLDI ’12). Association for Computing Machinery, New York, NY,
   USA, 53–66. https://doi.org/10.1145/2103786.2103795




                                Proc. ACM Program. Lang., Vol. 1, No. ICFP, Article 1. Publication date: September 2024.
