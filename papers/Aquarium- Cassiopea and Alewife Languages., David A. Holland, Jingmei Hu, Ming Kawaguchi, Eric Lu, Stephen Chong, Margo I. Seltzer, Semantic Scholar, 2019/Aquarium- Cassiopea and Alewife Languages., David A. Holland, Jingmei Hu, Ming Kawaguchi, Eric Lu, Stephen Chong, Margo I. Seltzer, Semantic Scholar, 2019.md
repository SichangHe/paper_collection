                                                      Aquarium: Cassiopea and Alewife Languages
                                                                                              (Prerelease Version of 20220108)

                                                       David A. Holland                                         Jingmei Hu                           Ming Kawaguchi
                                                      Harvard University                                   Harvard University                        Harvard University
                                                  dholland@eecs.harvard.edu                            jingmei_hu@g.harvard.edu                    ming@seas.harvard.edu

                                                               Eric Lu                                        Stephen Chong                           Margo I. Seltzer
                                                        Harvard University                                 Harvard University                   University of British Columbia
                                                     ericlu01@g.harvard.edu                              chong@seas.harvard.edu                      mseltzer@cs.ubc.ca
arXiv:1908.00093v5 [cs.PL] 13 Apr 2022




                                         Abstract                                                                        processor instruction sets, and Alewife, which is a specifica-
                                         This technical report describes two of the domain specific lan-                 tion or modeling language used for writing down machine-
                                         guages used in the Aquarium kernel code synthesis project.                      independent specifications for assembly language code
                                         It presents the language cores in terms of abstract syntax.                     blocks to be synthesized.
                                         Cassiopea is a machine description language for describ-                           Cassiopea also includes material for writing machine-
                                         ing the semantics of processor instruction sets. Alewife is                     dependent specifications (this is the target for the Alewife
                                         a specification language that can be used to write machine-                     translator), a concept of mapping modules used by the Ale-
                                         independent specifications for assembly-level instruction                       wife translator, and a simple representation of basic blocks
                                         blocks. An Alewife specification can be used to verify and                      in assembly language. These are described in this document.
                                         synthesize code for any machine described in Cassiopea,                            This document does not, however, describe any of the
                                         given a machine-specific translation for abstractions used                      other languages or file formats used in the Aquarium project
                                         in the specification. This article does not include an intro-                   or any of the Aquarium tools.
                                         duction to either the Aquarium system or the use of the                            The document is structured with six parts:
                                         languages. In addition to this version of the article being a
                                                                                                                             • The Cassiopea language and abstract syntax (Sec. 3)
                                         draft, the Aquarium project and the languages are work in
                                                                                                                             • Cassiopea types (Section 4)
                                         progress. This article cannot currently be considered either
                                                                                                                             • Cassiopea semantics (Section 5)
                                         final or complete.
                                                                                                                             • The Alewife language and abstract syntax (Section 6)
                                                                                                                             • Alewife types and semantics (Section 7)
                                         1    Introduction                                                                   • Alewife translation to Cassiopea (Section 8)
                                         The goal of the Aquarium project is to synthesize the
                                         machine-dependent parts of an operating system. This has                        2   Notation
                                         the potential to greatly reduce the amount of work needed                       In the abstract syntax, type judgments, and semantics judg-
                                         to port an operating system to a new machine architecture.                      ments we use italics for metavariables (e.g., 𝑣) and for
                                         It also potentially reduces the depth of knowledge needed                       words corresponding to types in the abstract syntax (e.g.,
                                         to do that work – currently an OS port requires deep expert                     declaration). We use typewriter font for words that cor-
                                         knowledge of both the OS and the new machine architecture                       respond to language keywords. The notation 𝛼𝑖 means “a
                                         – and with luck the overall amount of time involved as well.                    sequence of one or more 𝛼, each to be referred to elsewhere
                                            This document does not discuss either code synthesis or                      as 𝛼𝑖 ”. If there are no references outside the overbar, the 𝑖
                                         OS porting in any detail. It is intended as a supplement to                     subscript may be left off. Epsilon (𝜖) appearing in syntax rep-
                                         other project publications, which should in general be read                     resents an empty production. The notation ". . ." represents
                                         first. While this document includes discussions of and ratio-                   a string literal with arbitrary contents.
                                         nales for language features (as well as absence of language                        Bitvectors (machine integers) may be any width greater
                                         features) these discussions assume familiarity with the sur-                    than zero. Bitvector constants are represented as 0bC, which
                                         rounding context.                                                               can be thought of as an explicit sequence of zeros and ones.
                                            The two languages described in this document are Cass-                       The number of bits in a bitvector constant (that is, the number
                                         iopea1 , which is a register-transfer-list-style machine de-                    of digits) gives its type. Thus, 0b00 and 0b0000 are different.
                                         scription language used for writing down the semantics of                       In the concrete syntax, bitvector constants whose size is a
                                                                                                                         multiple of 4 can also be written in the form 0xC. These
                                         1 Cassiopea is named for a jelly(fish) that features symbiotic photosynthetic   are desugared in the parser and not shown further in this
                                         algae, which is for some reason spelled without the customary ’i’.              document.
   The Cassiopea and Alewife syntax should be considered                   • xop are identifiers bound to instructions (“operations”),
disjoint. Some elements are the same in each, but these are                  which are akin to procedures but distinguished from
specified separately regardless. They use the same metavari-                 them.
ables as well, which should not be mixed; any language                     • x𝜏 are identifiers for type aliases, which are bound to
construct in a judgment should be all Cassiopea or all Ale-                  base types in declarations.
wife. In a few places mixing is needed, in which case the                  • xmodule are the names of “modules”, which are used
translation defined in Section 8 is applied to allow inserting               to select among many possible groups of lowering
Alewife fragments into Cassiopea terms. The Alewife rules                    elements.
in Section 7 do use the same environments as the Cassiopea                 • Other identifiers x are used for other things, and
rules. These should be construed as holding only Cassiopea                   should be assumed to not range over the above el-
elements. Further details can be found in Section 7.                         ements.

                                                                       Note that all identifiers live in the same namespace, and
3   Cassiopea Overview                                                 rebinding or shadowing them is not allowed. All these identi-
This section covers the abstract syntax for Cassiopea.                 fiers can be thought of as variables, in the sense that they are
   Cassiopea is a register-transfer-list style language: it mod-       names that stand for other things. All of them are immutable
els instructions as non-Turing-complete procedures that up-            once defined, including the ordinary variables x that contain
date a machine state. Its executable semantics are covered in          plain values.
Section 5.                                                                Types. Types are divided syntactically into base types
   We model the machine from the assembly-language pro-                (integers, booleans, strings, bitvectors, etc.) and others (mem-
grammer’s perspective. In particular, we do not treat memory           ory regions and functions). User functions may handle only
as a huge block of address space but instead treat it in small         base types. Furthermore, memory regions and functions are
chunks passed in from somewhere else. We model both con-               second-class for reasons discussed below and are excluded
trol registers and general-purpose registers as well as other          in various places in the syntax and the typing rules.
machine state such as whether interrupts are enabled.                     We use index typing to capture the bit width of values.
   Furthermore we must allow assembler labels, which have                 Registers. Registers are represented in the specification
addresses, but those addresses are not resolved until after            with the metavariable 𝑟 , which stands for the underlying
programs are compiled and linked and must be treated as                abstract identity of a register. Declaring a register, e.g., with
abstract.                                                              letstate x : C reg as shown in Figure 2, allocates a fresh
   Notation. We use the following metavariables:                       register 𝑟 and binds the variable x to it. A subsequent decla-
     x, y, z Program variables (binders)                               ration of the form let y : C reg = x creates another variable
     r        Registers (abstract)                                     y that refers to the same underlying register. One might
     C        Integer constants (written in decimal)                   think of registers as numbered internally. We use the form
     0bC      Bitvector constants (written in binary)                  letstate control x : C reg to declare specific control regis-
    𝜏         Types                                                    ters, which are treated differently by the framing rules. The
     v        Values                                                   additional keyword dontgate inhibits state gating for the
     e        Expressions                                              register; this should be used for flags registers and anything
     S        Statements                                               similar that is implicitly used by all ordinary code.
     i, j     Rule-level integers                                         Some registers have associated with them a text form,
   (Other constructions are referred to with longer names.)            which is declared separately and is the form an assembler ex-
   A number of constructions are lists written out in long-            pects to parse. The Capstan uses this to extract an asssembly
hand (with a null case and a cons case) – these are written            program from aquarium’s internal representation. It is re-
out in longhand so that typing and semantic judgments can              ferred to by attaching the suffix .txt to the/a register variable.
be applied explicitly to each case, in order to, for example,          As some registers are not directly addressable by the assem-
propaate environment updates correctly.                                bler (e.g., they might be subfields of some larger addressable
   Identifiers and Variables. Identifiers are divided syntac-          unit or nonaddressable internal state), not all registers have
tically into seven categories:                                         a text form. This is not readily checked statically, at least
                                                                       not without introducing specific additional machinery, so
    • xmem are identifiers bound to memory regions, which              invalid .txt references fail at assembly code extraction time.
      are second-class.                                                   The type of a register is C reg, which is a register that
    • xfunc are identifiers bound to functions, which are              holds a C-bit bitvector. The bitvector value in question can
      second-class.                                                    be updated by assigning a new value; this is a statement
    • xproc are identifiers bound to procedures, which are             (e1 : = e2 ) and can only happen in places where statements
      second-class.                                                    are allowed. The construction ∗ e reads a register.
                                                                   2
                                      (Cassiopea Types)
      𝜏F                                 𝜏base | 𝜏mem | 𝜏func                                          (Cassiopea Values)
                                                                              ṽ F                                     v | fail
      𝜏base F        () | int | bool | string | x𝜏 | C bit                    vF            true | false | C | 0bC | ". . ."
       |                                  𝜏reg | 𝜏regs | 𝜏label                |                                  r | (xmem, C)
      𝜏reg F                                           C reg
      𝜏regs F                                    C reg set                                      (Cassiopea Expressions)
      𝜏label F                                      C label                   eF                                             ṽ | x
                                                                               |                                            e.txt
      𝜏mem F                        C1 bit C2 len C3 ref                       |                                        xfunc (e)
      𝜏func F                                 𝜏base𝑖 → 𝜏base                   |                                         unop e
                                                                               |                                    e1 binop e2
                                 (Cassiopea Operators)                         |                            e[C] | e[C1, C2 ]
      unop F                             − | b− | ¬ | bnot                     |                      let x : 𝜏base = e1 in e2
      binop F        = | ≠ | + | − | ∗ | / | < | <= | > | >=                   |                       if e1 then e2 else e3
       |                                         && | || | ⊕                   |                                      (xmem, e)
       |                >>| >>𝑆 |<<| band | bor | bxor                                                      ∗
                                                                               |                                e | fetch(e, C)
       |                                  b+ | b− | b∗ | b/                    |                                     branchto
       |                             b< | b<= | b> | b>=                       |                                   {x1, . . . , x𝑘 }
       |                        bs< | bs<= | bs> | bs>=                        |                                   ∥e∥ | e1 ∈e2
       |                                        ∪ | ∩ |⊆| \
                                Figure 1. Cassiopea types, values, operators, and expressions.

   The reader will note that the semantics rules for machines         regions are a property of programs (and thus are declared in
and declarations do not provide initial values for registers.         specifications) and not a property of the machine as a whole.
Instead, executions are defined in terms of some initial reg-            Pointers. A pointer literal has the form (xmem, C), in
ister state (and also some memory state), which is required           which xmem is the region name and C is the offset, shown
to have the right registers to match the machine definition.          in Figure 1. Because memory regions are second-class, xmem
This allows reasoning about the execution of programs and             must be specifically one of the available declared memory
program fragments in terms of many or all possible initial            regions. Pointer literals exist in the abstract syntax, but are
states. These issues are discussed further below.                     not allowed in the concrete syntax except in specifications.
   Memory. A memory region has the type                               The only way to get a pointer value is to look up a label (dis-
C1 bit C2 len C3 ref, shown in Figure 1. This refers                  cussed immediately below) or have it provided in a register
to a memory region that has C2 cells, each of which stores a          as part of the initial machine state.
bitvector of width C1 . This memory region is addressed with             A pointer literal is treated as a bitvector of the same width,
pointers of width C3 . Note that we assume byte-addressed             so one can appear in a register or in memory. However, we
machines, and for the purposes of both this specification             enforce a restriction (not captured in the semantics rules so
and our implementation, we assume bytes are 8 bits wide.              far) that no value in the initial machine state, whether in a
(This restriction could be relaxed if we wanted to model              register or in memory, is a pointer unless required to be so
various historic machines.) Thus a memory region of type              by the precondition part of the specification. All other values
32 bit 4 len 32 ref has 4 32-bit values in it, which can be           are restricted to be plain bitvector values.
addressed at byte offsets 0, 4, 8, and 12. These values can of           Addition and subtraction are allowed on pointers and
course be changed, like values in registers.                          they change the offset, but other bitvector operations (e.g.,
   Memory regions are named with identifiers. These names,            multiply) are disallowed and fail. Similarly, attempting to
and memory regions themselves, are not first class; variables         fetch from or store to a plain bitvector that is not a pointer
are not allowed to range over them. Also note that memory             fails. Note however that we do not statically distinguish

                                                                  3
pointers and plain bitvectors. (We could have used flow-                next block. It is thus necessary to be able both to name the
sensitive typing to reason about when registers and memory              external label to use and to specify the conditions when it
cells contain pointers and when they do not; but this adds              should be reached. For this purpose a predicate branchto is
substantial complexity and for our problem domain does                  provided. It may appear in the postcondition and governs the
not provide significant value.) Instead, we step to failure at          exit path from the block: if forced to true, the block branches
runtime. This can be seen in the semantics rules.                       to the external assembler label, and if false, the block falls
   Fetching from a pointer takes the form fetch (e,C). Storing          through from its last instruction. The concrete syntax is
to a pointer takes the form store(e1, 𝐶) ← e2 . The extra               branchto(dest) which also sets the assembler label used to
constant C specifies the width of the cell pointed to. (This is         dest. It is not valid to name more than one such assembler
not an offset.) Because we do not check pointers statically,            label.
we do not know the memory region being pointed to and                      Note that the assembler labels used in branching are,
cannot look up its cell size; thus we need the width explicitly         though also assembler labels, a separate mechanism unre-
for typing. It is checked at runtime.                                   lated to the labels attached to memory regions; they are code
   Labels. As mentioned above, the term “label” means an                labels rather than data labels and inherently work differently.
assembler label or linker symbol. These have addresses (or                 Also note that the implementation is slightly more compli-
depending on how one looks at them, they are addresses)                 cated than the description given above and the rules given
and those addresses are constants, but the constants are not            in the semantics section. In the implementation, the magic
known at assembly time, so we must model them abstractly.               number that triggers an external branch is not 255 but the
   When one declares a memory region, one may attach a                  number 𝑙 such that 𝑙 added to the instruction number of the
label to it, which is an additional identifier. This identifier         branch adds to 99. This detail affects only intermediate syn-
is created as a variable of type C label in Figure 1. The               thesis results in the internal format; the extracted assembly
value is a pointer to the first entry in the region, and a single       code is the same.
type subsumption rule allows this value to be accessed and                 Register Sets. Register sets are second-class elements
placed in an ordinary register or variable of suitable bitvector        intended to exist only as literals and only as the result of
type. The intended mechanism is that for each machine the               lowering machine-independent specifications that cannot
preferred instruction on that machine for loading assembler             directly talk about specific registers. Currently they do not
symbols into a register can be defined to take an operand               exist in the implementation. Register sets are not allowed to
of type C label, and then its value can be assigned to the              be operands to instructions to avoid state explosions when
destination register. This type restriction on the operand is           synthesizing. This restriction is currently not captured in
sufficient to synthesize programs that use labels correctly.            the abstract syntax or typing rules.
   Code Positions and Branching. Cassiopea code blocks                     Functions and Procedures. Functions, defined with def
may contain branches, either forward within the block                   in Figure 2, are pure functions whose bodies are expressions.
(branching backwards is forbidden) or to a single external              They produce values. They can access registers and memory,
assembler label outside the block. This model is sufficient             and can fail, but cannot update anything. Procedures, defined
for our block-oriented synthesis approach; more complex                 with proc, are on the other hand impure and their bodies
control flow can be handled with multiple blocks.                       are statements. They do not produce values, but they may
   Consequently, a branch may either go to the external                 update the machine state. They are otherwise similar, and
assembler label (which terminates execution of the current              are intended to be used to abstract out common chunks of
block) or skip zero or more instructions. We model branch               functionality shared among multiple instructions in machine
targets as an 8-bit skip count. In Figure 2, The statement              descriptions. Functions can also be used for state hiding in
BRANCH(0bC) skips 0bC instructions; BRANCH(0xff) jumps                  specifications.
to the external label. This statement may be used to define                Functions and procedures are second-class; they may be
both conditional and unconditional branch instructions. Such            called only by their own name and may not be bound to vari-
instructions should be defined to take an operand of type               ables or passed around. Furthermore, they are only allowed
8 bit to choose the branch destination. This magic number               to handle base types: higher-order functions are explicitly
should then be printed to the output assembly text using the            not supported.
built-in function textlabel, which replaces it with a valid                Operations. Operations (defined with defop in Figure 2)
assembler label, either the selected external label string or a         are essentially instructions, and we refer to these inter-
scratch label attached to the proper destination instruction.           changeably. An operation takes zero or more operands and
   Specifications do not need to be directly concerned with             transforms the machine state as defined by one or more state-
internal branches, which occur or not as needed. However,               ments. Operands are currently defined as expressions, but
external branches are part of a block’s specification; typically        are restricted as follows:
the purpose of a block with an external branch is to test some
condition and then either branch away or fall through to the
                                                                    4
                                                                                                         (Cassiopea Declarations)
                                                                         decls F                                       𝜖 | decl; decls
                        (Cassiopea Statements)                           decl F                                       type x𝜏 = 𝜏base
         SF                                     S; S                     |                                           let x : 𝜏base = e
          |                                xproc (e)                     |                                             let x.txt = e
          |                   let x : 𝜏base = e in S                     |                            def xfunc x𝑖 : 𝜏base𝑖 → 𝜏base = e
          |               for x ∈ (C1 . . . C2 ) do S                    |                             proc xproc x𝑖 : 𝜏base𝑖 → () = S
          |                   if e then S1 else S2                       |                                          letstate x : 𝜏reg
          |                                 e1 : = e2                    |                                letstate control x : 𝜏reg
          |                     store(e1, 𝐶) ← e2                        |                    letstate control dontgate x : 𝜏reg
          |                              BRANCH(e)                       |                                     letstate xmem : 𝜏mem
          |                              assert(e)                       |                             letstate xmem : 𝜏mem with x
          |                                    skip
          |                                  crash                       defops F                                    𝜖 | defop; defops
                                                                         defop F                       defop xop {txt = e, sem = S}
                                                                         |                   defop xop x𝑖 : 𝜏base𝑖 {txt = e, sem = S}
                                         Figure 2. Cassiopea statements and declarations.

    • They may be values, but not string values, and not                        A (single) lowering is a collection of declarations used
      fail.                                                                  to instantiate elements in Alewife translations, shown in
    • They may be variables of register type.                                Figure 3. These are placed into a module, with multiple mod-
    • They may be variables of label type.                                   ules per file, so that the lowerings associated with multi-
                                                                             ple related Alewife specifications can be kept together. The
This restriction affects what the synthesizer tries to generate;             import xmodule directive enables sharing common elements
a broader set of expressions may be accepted for verification                in one module xmodule across multiple specifications. The
or concrete execution and simply evaluated in place.                         modules used to lower a specification are selected using the
    There is an important distinction between “operations”                   lower-with declaration in Alewife.
and “instructions”. Operations are the units in which Cassio-                   A spec (specification) is a precondition and postcondition,
pea reasons about machine operations and the units in which                  which are boolean expressions, along with optional permis-
Cassiopea generates programs and code fragments, but they                    sion to destroy additional registers (the frame), shown in
do not necessarily need to be single instructions. The text                  Figure 3. Cassiopea specifications are produced by compiling
output to the assembler is arbitrary and can be computed                     Alewife specifications. Note that a module can also contain
on the fly based on the operand value. On some platforms                     frame declarations; these are added to any provided in the
the assembler defines so-called “synthetic instructions” that                Alewife specification. A code block is permitted to destroy
are potentially multiple real instructions. This facility takes              any register that is either explicitly listed in the frame decla-
that a step further by allowing the writer of the machine                    rations or mentioned in the postcondition, while it may read
description to define their own synthetics.                                  any register mentioned in the precondition and any control
    Other Constructs. e[C] and e[C1, C2 ] in Figure 1 extract                register. This restriction is currently not adequately captured
a single bit and a slice, respectively, from a bitvector. The off-           in the semantics rules.
sets are constants; a shift can be used beforehand if variable                  A program is a sequence of instruction invocations, shown
offsets are needed. The width of the slice must be constant                  in Figure 3.
for static typing.                                                              Built-in Functions. Here is a partial list of the built-in
    Machines, Lowering, Specifications, and Programs.                        functions in Cassiopea.
    A machine is the full description of a machine architecture;                 • empty (int C → C reg set) produces an empty regis-
it includes declarations (including types, constants, registers,                   ter set of the requested bit size.
functions and procedures) and also instructions, shown in                        • hex (C bit → string) prints numbers in hexadeci-
Figure 3. This is typically a standalone file but may be a set                     mal.
of files referenced via include.                                                 • bin (C bit → string) prints numbers in binary.
                                                                     5
                                                                                                    (Cassiopea Lowerings)
                                                                           modules F                     𝜖 | module; modules
                             (Cassiopea Machines)                          module F            module xmodule {decls; frame}
        machine F                         decls; defops
                                                                                                (Cassiopea Specifications)
                             (Cassiopea Programs)                          frame F                         reg-modify : xregi
        inst F                              xop | xop e                     |                        mem-modify : (xmemi , e𝑖 )
        insts F                          𝜖 | inst; insts                   frames F                          𝜖 | frame frames
        program F                                 insts                    pre F                                              e
                                                                           post F                                             e
                                                                           spec F                      decls; frames; pre; post
                           Figure 3. Cassiopea machines, lowerings, programs, and specifications.

   • dec (C bit → string) prints numbers in decimal.                  of the form 𝑒.hex, 𝑒.bin, and 𝑒.dec is converted to the built-
   • lbl (C label → string) prints labels (it returns the             in functions hex, bin, dec respectively. These print either
     label identifier as a string). This is for data labels at-       integers or bitvectors as strings in hexadecimal, binary, or
     tached to memory locations.                                      decimal respectively. The syntax x.lbl is similarly converted
   • textlabel (8 bit → string) prints branch offsets as              to the built-in function lbl. This produces the label (that is,
     assembler labels. This is for code labels, as described          the identifier naming the label) as a string. Further the con-
     above.                                                           crete syntax supports include files via an include directive,
   • format (string → string . . . → string) formats                  which is useful for sharing common elements.
     strings. The first argument is a format string; the re-
     mainder of the arguments are substituted into the for-           4   Cassiopea Static Typing
     mat string where a dollar sign appears followed by               This section describes the Cassiopea type system.
     the argument number (1-based). (A literal dollar sign               Environments. The type system uses two environments:
     can be inserted by using $$.) The number of additional           Δ maps type alias names to the types they represent, and Γ
     arguments expected is deduced from the contents of               maps variables to the types assigned to them. Recall from
     the format string.                                               the syntax that only base types may have alias names, so
   • bv_to_len (int C1 → C2 bit → C1 bit) returns a                   alias names can be treated as base types.
     new bitvector of size C1 with the same value up to the              Well-Formedness. Since types include alias names, we
     ability of the new size to represent that value.                 need to check that a proposed alias name is actually a type
   • bv_to_uint (C1 bit → int) converts a bitvector to                name. At the same time we insist that the widths of bitvectors
     unsigned int.                                                    be greater than zero. The judgment for this has the form
   • uint_to_bv_l (int C1 → int C2 → C1 bit) converts                 Δ ⊢wf 𝜏, shown in Figure 4. There is an intended invariant
     an unsigned int C2 into a bitvector of size C1 .                 that only well-formed types may be entered into the variable
   • isptr (C bit → bool) tests at runtime if a bitvector             typing environment Γ, so that types taken out of it do not
     value is a pointer or not.                                       need to be checked for well-formedness again.
   Note that some of these functions have their own typing               In a typing environment comprised of Δ mapping user-
rules, some of which are polymorphic in bitvector size. We            defined type names (type aliases) to types and Γ mapping
have not complicated the typing rules presented by including          program binders (variables) to types, we say that a type is
all of these as special cases.                                        well formed when all type names are well-formed and all
   Concrete Syntax. We do not describe the concrete syn-              indices are of type int and nonzero.
tax in detail here; however, it does not stray very far from             Expressions. Expressions produce values that have types.
the abstract syntax. The operator precedence and most of the          Because types appear explicitly in some expressions (e.g.,
operator spellings are taken from C but most of the rest of           let), we need both environments, so the form of an expres-
the concrete syntax is ML-style. There are also a few things          sion typing judgment is Δ, Γ ⊢ e : 𝜏, shown in Figure 5. This
desugared in the parser and not shown in the abstract syntax.         means that we conclude e has type 𝜏. Note that the .txt form
As already mentioned, bitvector constants whose size is a             is restricted to registers; it is specifically for extracting the
multiple of 4 can also be written in the form 0xC. Syntax             assembly text form of a register. We have not written out a
                                                                  6
                                                          (Type Well-Formedness)

                                         Δ ⊢wf ()       Δ ⊢wf int       Δ ⊢wf bool        Δ ⊢wf string

                                     C>0                 C>0                    C>0                   C>0
                                 Δ ⊢wf C bit          Δ ⊢wf C reg       Δ ⊢wf C label         Δ ⊢wf C reg set

                           C1 > 0, C2 > 0, C3 > 0                Δ(x) = 𝜏         Δ ⊢wf 𝜏     ∀𝑖, Δ ⊢wf 𝜏𝑖       Δ ⊢wf 𝜏𝑟
                        Δ ⊢wf C1 bit C2 len C3 ref                      Δ ⊢wf x                      Δ ⊢wf 𝜏𝑖 → 𝜏𝑟
                                                Figure 4. Cassiopea type well-formedness.

                                                            (Expression Typing)

                       Δ, Γ ⊢ C : int         Δ, Γ ⊢ ". . ." : string       Δ, Γ ⊢ true : bool        Δ, Γ ⊢ false : bool

                         C = {0, 1}k                  Δ ⊢wf 𝜏         Γ(x) = 𝜏          Δ ⊢wf 𝜏           Δ, Γ ⊢ e : 𝜏reg
                      Δ, Γ ⊢ 0bC : k bit     Δ, Γ ⊢ fail : 𝜏           Δ, Γ ⊢ x : 𝜏         Δ, Γ ⊢ e.txt : string

               Δ, Γ ⊢ xfunc : 𝜏base𝑖 → 𝜏base       ∀i, Δ, Γ ⊢ e𝑖 : 𝜏base𝑖 Δ, Γ ⊢ e : 𝜏base1
                                             
                                                                                                 ⊨ unop : 𝜏base1 → 𝜏base2
                               Δ, Γ ⊢ xfunc (e𝑖 ) : 𝜏base                                         Δ, Γ ⊢ unop e : 𝜏base2

                            Δ, Γ ⊢ e1 : 𝜏base1         Δ, Γ ⊢ e2 : 𝜏base1        ⊨ binop : 𝜏base1 → 𝜏base1 → 𝜏base2
                                                           Δ, Γ ⊢ e1 binop e2 : 𝜏base2

                 Δ, Γ ⊢ e : C2 bit        0 ≤ C1 < C2           Δ, Γ ⊢ e : C3 bit        0 ≤ C1 < C2 ≤ C3            k = C2 − C1
                         Δ, Γ ⊢ e[C1 ] : 1 bit                                      Δ, Γ ⊢ e[C1, C2 ] : k bit

                                      Δ, Γ ⊢ e1 : 𝜏base          x ∉ Δ, Γ        Δ, Γ [x ↦→ 𝜏base ] ⊢ e2 : 𝜏2
                                                       Δ, Γ ⊢ let x : 𝜏base = e1 in e2 : 𝜏2

                                              Δ, Γ ⊢ b : bool        Δ, Γ ⊢ e1 : 𝜏        Δ, Γ ⊢ e2 : 𝜏
                                                        Δ, Γ ⊢ if b then e1 else e2 : 𝜏

                        Δ, Γ ⊢ e : int          Δ, Γ ⊢ xmem : _ bit _ len C ref             Δ, Γ ⊢ e : _ bit        C>0
                                         Δ, Γ ⊢ (xmem, e) : C bit                           Δ, Γ ⊢ fetch(e, C) : C bit

                                  Δ, Γ ⊢ e : C reg         Δ, Γ ⊢ x : C label
                                 Δ, Γ ⊢ e : C bit
                                          ∗
                                                             Δ, Γ ⊢ x : C bit         Δ, Γ ⊢ branchto : bool

               ∀i ∈ (1 . . . k), Δ, Γ ⊢ x𝑖 : C reg       Δ, Γ ⊢ e : C reg set         Δ, Γ ⊢ e1 : C reg Δ, Γ ⊢ e2 : C reg set
               Δ, Γ ⊢ {x1, . . . , x𝑘 } : C reg set         Δ, Γ ⊢ ∥e∥ : int                       Δ, Γ ⊢ e1 ∈e2 : bool
                                          Figure 5. Cassiopea typing rules for expressions.

separate rule for each unary and binary operator. The types                     semantics) that allows taking a subrange of a memory region
of operators are as shown in Figure 6. Note that the bitvector                  as a new smaller region. We have not needed this for our use
operators are polymorphic in bit size.                                          cases, and keeping the set of possible regions fixed simplifies
   Arguably the right hand argument of the shift operators                      a number of things.
should be allowed to be a different width. There is one rule                       Statements. Statements do not produce values. We still
for pointer literals that covers both the expression and the                    need both environments, though, so the form of a typing
value form. There is no rule (either in the typing or in the

                                                                            7
                              −                                                                     int → int
                             b−                                                              ∀C,C bit → C bit
                             ¬                                                                    bool → bool
                            bnot                                                             ∀C,C bit → C bit

                              =       ≠                                 ∀𝜏base , 𝜏base → 𝜏base → bool
                              +        −       ∗          /                         int → int → int
                              <       <=       >         >=                       int → int → bool
                             &&        ||      ⊕                              bool → bool → bool
                             >>     >>𝑆       <<                      ∀C,C bit → C bit → C bit
                            band     bor     bxor                     ∀C,C bit → C bit → C bit
                             b+       b−      b∗       b/             ∀C,C bit → C bit → C bit
                             b<      b<=      b>      b>=              ∀C,C bit → C bit → bool
                            bs<     bs<=     bs>      bs>=             ∀C,C bit → C bit → bool
                              ∪       ∩        \           ∀C,C reg set → C reg set → C reg set
                              ⊆                                ∀C,C reg set → C reg set → bool
                                        Figure 6. Cassiopea typing rules for unop and binop.

                                                          (Statement Typing)
                           Δ, Γ ⊢ S1      Δ, Γ ⊢ S2      Δ, Γ ⊢ xproc : 𝜏base𝑖 → ()             ∀i, Δ, Γ ⊢ e𝑖 : 𝜏base𝑖
                                                                                       

                                 Δ, Γ ⊢ S1 ; S2                               Δ, Γ ⊢ xproc (e𝑖 )

                     Δ, Γ ⊢ e : 𝜏base     x ∉ Δ, Γ       Δ, Γ [x ↦→ 𝜏base ] ⊢ S      x ∉ Δ, Γ         Δ, Γ [x ↦→ int] ⊢ S
                                   Δ, Γ ⊢ let x : 𝜏base = e in S                      Δ, Γ ⊢ for x ∈ (C1 . . . C2 ) do S

                       Δ, Γ ⊢ e : bool       Δ, Γ ⊢ S1        Δ, Γ ⊢ S2      Δ, Γ ⊢ e1 : C reg         Δ, Γ ⊢ e2 : C bit
                               Δ, Γ ⊢ if e then S1 else S2                                 Δ, Γ ⊢ e1 : = e2

                        Δ, Γ ⊢ e1 : C1 bit        Δ, Γ ⊢ e2 : C2 bit         Δ, Γ ⊢ e : 8 bit         Δ, Γ ⊢ e : bool
                                Δ, Γ ⊢ store(e1, C2 ) ← e2                  Δ, Γ ⊢ BRANCH(e)         Δ, Γ ⊢ assert(e)

                                                      Δ, Γ ⊢ skip          Δ, Γ ⊢ crash
                                          Figure 7. Cassiopea typing rules for statements.

judgment for a statement is Δ, Γ ⊢ S, shown in Figure 7. This               any references need to be quantified. (That in turn is not
means that S is well typed.                                                 allowed to avoid needing to send these quantifiers to the
   Declarations. Declarations update the environment. The                   SMT solver.)
form of a typing judgment for a declaration is Δ, Γ ⊢ decl ▷                   Machines. A machine is some declarations followed by
Δ ′, Γ ′, and a judgment for a list of declarations has the same            some defops, so the typing rule is just sequencing, shown
form, shown in Figure 8. This means that the declaration                    in Figure 9, but there is a wrinkle: the initial environment
(or list) is well typed and produces the new environment on                 for the machine is not an input. Δbuiltin is the (fixed) environ-
the right. One can think of the ⊢ ▷ as the tail and head of                 ment describing the built-in type aliases. (Currently there
an arrow with the element transforming the environments                     are none.) Γbuiltin is the environment describing the types of
labeling the body.                                                          built-in variables. This notionally includes the built-in func-
   We impose an additional syntactic restriction on decla-                  tions. (But as mentioned earlier some of them actually have
rations found in a machine description (as opposed to the                   their own typing rules.) The form of a typing judgment for
additional declarations that may appear in a specification):                a machine is ⊢ machine ▷ Δ, Γ. This means that the machine
they may not use the expression forms that refer to ma-                     description is well typed and provides the environment on
chine state (registers or memory), because when defining
the machine, there is no specific machine state to refer to;

                                                                       8
                                                             (Declaration Typing)
                                                          Δ, Γ ⊢ decl ▷ Δ ′, Γ ′         Δ ′, Γ ′ ⊢ decls ▷ Δ ′′, Γ ′′
                                  Δ, Γ ⊢ 𝜖 ▷ Δ, Γ                     Δ, Γ ⊢ decl; decls ▷ Δ ′′, Γ ′′

                    Δ ⊢wf 𝜏base       x𝜏 ∉ Δ, Γ           Δ ′ = Δ[x𝜏 → 𝜏base ]         Δ, Γ ⊢ x : 𝜏reg         Δ, Γ ⊢ e : string
                                Δ, Γ ⊢ type x𝜏 = 𝜏base ▷ Δ , Γ   ′
                                                                                            Δ, Γ ⊢ let x.txt = e ▷ Δ, Γ

                                  Δ ⊢wf 𝜏base         x ∉ Δ, Γ        Δ, Γ ⊢ e : 𝜏base         Γ ′ = Γ [x ↦→ 𝜏base ]
                                                     Δ, Γ ⊢ let x : 𝜏base = e ▷ Δ, Γ ′

                                                           Δ ⊢wf 𝜏base𝑖 → 𝜏base
                                                                                  
             xfunc ∉ Δ, Γ       Γ ′ = Γ[∀i, x𝑖 ↦→ 𝜏base𝑖 ]     Δ, Γ ′ ⊢ e : 𝜏base   Γ ′′ = Γ [xfunc ↦→ x𝑖 : 𝜏base𝑖 → 𝜏base ]
                                                                                                                          

                                                 Δ, Γ ⊢ def xfunc x𝑖 : 𝜏base𝑖 → 𝜏base = e ▷ Δ, Γ ′′

     Δ ⊢wf 𝜏base𝑖 → ()         xproc ∉ Δ, Γ           Γ ′ = Γ [∀i, x𝑖 ↦→ 𝜏base𝑖 ]        Δ, Γ ′ ⊢ S        Γ ′′ = Γ[xproc ↦→ x𝑖 : 𝜏base𝑖 → () ]
                                                                                                                                            

                                                 Δ, Γ ⊢ proc xproc x𝑖 : 𝜏base𝑖 → () = S ▷ Δ, Γ ′′

                                           Δ ⊢wf C reg           x ∉ Δ, Γ           Γ ′ = Γ [x ↦→ C reg]
                                                       Δ, Γ ⊢ letstate x : C reg ▷ Δ, Γ ′

                                           Δ ⊢wf C reg           x ∉ Δ, Γ           Γ ′ = Γ [x ↦→ C reg]
                                                  Δ, Γ ⊢ letstate control x : C reg ▷ Δ, Γ ′

                                           Δ ⊢wf C reg           x ∉ Δ, Γ           Γ ′ = Γ [x ↦→ C reg]
                                        Δ, Γ ⊢ letstate control dontgate x : C reg ▷ Δ, Γ ′

                   Δ ⊢wf C1 bit C2 len C3 ref                xmem ∉ Δ, Γ            Γ ′ = Γ [xmem ↦→ C1 bit C2 len C3 ref]
                                          Δ, Γ ⊢ letstate xmem : C1 bit C2 len C3 ref ▷ Δ, Γ ′

                                             Δ ⊢wf C1 bit C2 len C3 ref      Δ ⊢wf C3 label
              xmem ∉ Δ, Γ         x ∉ Δ, Γ            Γ ′ = Γ [xmem ↦→ C1 bit C2 len C3 ref]                       Γ ′′ = Γ ′ [x ↦→ C3 label]
                                   Δ, Γ ⊢ letstate xmem : C1 bit C2 len C3 ref with x ▷ Δ, Γ ′′

                                                        Δ, Γ ⊢ defop ▷ Δ ′, Γ ′         Δ ′, Γ ′ ⊢ defops ▷ Δ ′′, Γ ′′
                                Δ, Γ ⊢ 𝜖 ▷ Δ, Γ                      Δ, Γ ⊢ defop; defops ▷ Δ ′′, Γ ′′

                             xop ∉ Δ, Γ          Δ, Γ ⊢ e : string          Δ, Γ ⊢ S         Γ ′ = Γ [xop ↦→ () → ()]
                                                 Δ, Γ ⊢ defop xop {txt = e, sem = S} ▷ Δ, Γ ′

                      Δ ⊢wf 𝜏base𝑖 → ()              xop ∉ Δ, Γ
                                             
                                                                     ∀i, 𝜏base𝑖 ≠ string ∧ 𝜏base𝑖 ≠ () ∧ 𝜏base𝑖 ≠ 𝜏regs
               Γ ′ = Γ[∀i, x𝑖 ↦→ 𝜏base𝑖 ]         Δ, Γ ′ ⊢ e : string       Δ, Γ ′ ⊢ S   Γ ′′ = Γ[xop ↦→ x𝑖 : 𝜏base𝑖 → () ]
                                                                                                                         

                                          Δ, Γ ⊢ defop xop x𝑖 : 𝜏base𝑖 {txt = e, sem = S} ▷ Δ, Γ ′′
                                           Figure 8. Cassiopea typing rules for declarations.

the right for use of other constructs that depend on the ma-                   the judgment on a machine; and one that says that a frame
chine. (Specs and programs are only valid relative to a given                  (modifies list) is well typed, which has the form Δ, Γ ⊢ frames.
machine.)                                                                      This lets us write the real rule, which has the form machine ⊢
   Specifications. For specifications we need two helper                       spec and means that the specification is well typed under the
rules, shown in Figure 9: one that applies an additional list                  machine description.
of declarations to a machine, which has the same form as
                                                                           9
                                                              (Machine Typing)
                                       Δbuiltin, Γbuiltin ⊢ decls ▷ Δ, Γ             Δ, Γ ⊢ defops ▷ Δ ′, Γ ′
                                                             ⊢ decls; defops ▷ Δ ′, Γ ′
                                                            (Specification Typing)
                                                 ⊢ machine ▷ Δ, Γ               Δ, Γ ⊢ decls ▷ Δ ′, Γ ′
                                                            ⊢ machine; decls ▷ Δ ′, Γ ′

                            ∀i, Δ, Γ ⊢ xregi : C𝑖 reg           ∀i, Δ, Γ ⊢ e𝑖 : int             ∀i, Δ, Γ ⊢ xmemi : 𝜏mem
                           Δ, Γ ⊢ reg-modify : xregi                       Δ, Γ ⊢ mem-modify : (xmemi , e𝑖 )

                                                              Δ, Γ ⊢ frame             Δ, Γ ⊢ frames
                                                 Δ, Γ ⊢ 𝜖           Δ, Γ ⊢ frame frames

                     ⊢ machine; decls ▷ Δ, Γ            Δ, Γ ⊢ frame              Δ, Γ ⊢ pre : bool         Δ, Γ ⊢ post : bool
                                                     machine ⊢ decls; frames; pre; post
                                                              (Program Typing)
                           Δ, Γ ⊢ xop : (() → ())           Δ, Γ ⊢ xop : 𝜏base𝑖 → ()                ∀i, Δ, Γ ⊢ e𝑖 : 𝜏base𝑖
                                                                                            

                                    Δ, Γ ⊢ xop                                        Δ, Γ ⊢ xop e𝑖

                                      Δ, Γ ⊢ inst           Δ, Γ ⊢ insts        ⊢ machine ▷ Δ, Γ          Δ, Γ ⊢ program
                         Δ, Γ ⊢ 𝜖           Δ, Γ ⊢ inst; insts                            machine ⊢ program
                          Figure 9. Cassiopea typing rules for machine, specification, and program.

   Programs. A program is a sequence of calls to instruc-                         each label maps to a pointer that points to the base (offset
tions. We need judgments of the form Δ, Γ ⊢ inst for a single                     0) of the region associated with the label. However, we take
instruction and also Δ, Γ ⊢ insts for the sequence, shown in                      advantage of the polymorphism and dynamic typing of paper
Figure 9. There are two cases for a single instruction because                    rules to also store the following in the same environment:
of a minor glitch in formulation: because the overbar nota-
tion means “one or more”, there are two cases in the syntax                           • xfunc (function names) map to pairs {x𝑖 , e}, which give
for instructions, one for zero operands and one for one or                              the list of argument names and the body for functions.
more operands; we need typing rules for both cases. Mean-                             • xproc (procedure names) map to pairs {x𝑖 , S}, which
while the type entered into Γ for a zero-operand instruction                            give the list of argument names and the body for pro-
is unit to unit, not 𝜖 to unit, to avoid needing an additional                          cedures.
form for types just for this case. (Notice that a one-operand                         • xop (operation/instruction names) map to triples
instruction may not have type unit to unit because unit is                              {x𝑖 , e, S}, which give the list of argument names, the
not allowed as an instruction operand, so the type is not am-                           expression for the text form, and the body for opera-
biguous.) These rules let us write a judgment for a program,                            tions.
which has the form machine ⊢ program and means that the                               • r.txt (the form for the text version of a register) maps
program is well typed relative to the machine.                                          to a value.
   Soundness. Note that even though we do not check cer-                              • The word EXTBRANCH maps to a branch state, which
tain things statically, the type system remains sound: we                               must be either ext or ·. This reports whether, after
include the necessary checks and failure states in the seman-                           executing a program, it branched to the external label
tics so that evaluation does not get stuck.                                             or not.
                                                                                  Since identifiers are not allowed to overlap in well-typed
5   Cassiopea Semantics                                                           programs, and register identities are not strings at all, and
This section defines the semantics of Cassiopea.                                  EXTBRANCH is reserved, this usage creates no conflicts.
  Environment. The execution environment Λ maps Cass-                               Note that xmem , x𝜏 , and xmodule do not appear in Λ as these
iopea variables x to values v. For labels on memory regions,                      require no translation/lookup at runtime.
                                                                           10
                                          (Expression Semantics)
        Λ(x) = v           Λ ⊢ (𝜌, 𝜎, e) ⇓ r           Λ(r.txt) = v           Λ ⊢ (𝜌, 𝜎, e) ⇓ r          r.txt ∉ Λ
    Λ ⊢ (𝜌, 𝜎, x) ⇓ v                Λ ⊢ (𝜌, 𝜎, e.txt) ⇓ v                       Λ ⊢ (𝜌, 𝜎, e.txt) ⇓ fail

          ∀i, Λ ⊢ (𝜌, 𝜎, e𝑖 ) ⇓ v𝑖        Λ(xfunc ) = {x𝑖 , e}          Λ[∀i, x𝑖 ↦→ v𝑖 ] ⊢ (𝜌, 𝜎, e) ⇓ ṽ
                                            Λ ⊢ (𝜌, 𝜎, xfunc (e𝑖 )) ⇓ ṽ

Λ ⊢ (𝜌, 𝜎, e) ⇓ v1       ṽ2 = unop v1        Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ v1        Λ ⊢ (𝜌, 𝜎, e2 ) ⇓ v2       ṽ3 = v1 binop v2
      Λ ⊢ (𝜌, 𝜎, unop e) ⇓ ṽ2                                      Λ ⊢ (𝜌, 𝜎, e1 binop e2 ) ⇓ ṽ3

Λ ⊢ (𝜌, 𝜎, e) ⇓ 0bC        C = b0 . . . bC𝑖 . . . bn     Λ ⊢ (𝜌, 𝜎, e) ⇓ 0bC            C = b0 . . . bC𝑖 . . . bC 𝑗 . . . bn
           Λ ⊢ (𝜌, 𝜎, e[C𝑖 ]) ⇓ bC𝑖                                  Λ ⊢ (𝜌, 𝜎, e[C𝑖 , C 𝑗 ]) ⇓ bC𝑖 . . . bC 𝑗

                        Λ ⊢ (𝜌, 𝜎, e) ⇓ (xmem, C)               Λ ⊢ (𝜌, 𝜎, e) ⇓ (xmem, C)
                         Λ ⊢ (𝜌, 𝜎, e[_]) ⇓ fail                Λ ⊢ (𝜌, 𝜎, e[_, _]) ⇓ fail

                           Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ v1          Λ[x ↦→ v1 ] ⊢ (𝜌, 𝜎, e2 ) ⇓ ṽ2
                                  Λ ⊢ (𝜌, 𝜎, let x : 𝜏base = e1 in e2 ) ⇓ ṽ2

   Λ ⊢ (𝜌, 𝜎, e) ⇓ true          Λ ⊢ (𝜌, 𝜎, e𝑡 ) ⇓ ṽ𝑡      Λ ⊢ (𝜌, 𝜎, e) ⇓ false             Λ ⊢ (𝜌, 𝜎, e 𝑓 ) ⇓ ṽ 𝑓
       Λ ⊢ (𝜌, 𝜎, if e then e𝑡 else _) ⇓ ṽ𝑡                        Λ ⊢ (𝜌, 𝜎, if e then _ else e 𝑓 ) ⇓ ṽ 𝑓

       Λ ⊢ (𝜌, 𝜎, e) ⇓ r        𝜌 (r) = v       Λ ⊢ (𝜌, 𝜎, e) ⇓ (xmem, C)             𝜎 (xmem, C) = (v, C𝑙 )
             Λ ⊢ (𝜌, 𝜎, e) ⇓ v
                           ∗
                                                                 Λ ⊢ (𝜌, 𝜎, fetch(e, C𝑙 )) ⇓ v

                 Λ ⊢ (𝜌, 𝜎, e) ⇓ (xmem, C)               𝜎 (xmem, C) = (_, C𝑚 )           C𝑚 ≠ C𝑙
                                       Λ ⊢ (𝜌, 𝜎, fetch(e, C𝑙 )) ⇓ fail

         Λ ⊢ (𝜌, 𝜎, e) ⇓ (xmem, C)             (xmem, C) ∉ 𝜎                  Λ ⊢ (𝜌, 𝜎, e) ⇓ 0bC
                Λ ⊢ (𝜌, 𝜎, fetch(e, C𝑙 )) ⇓ fail                      Λ ⊢ (𝜌, 𝜎, fetch(e, C𝑙 )) ⇓ fail

                                                 Λ ⊢ (𝜌, 𝜎, e) ⇓ C
                                      Λ ⊢ (𝜌, 𝜎, (xmem, e)) ⇓ (xmem, C)

                      Λ(EXTBRANCH) = ext                             Λ(EXTBRANCH) = ·
                  Λ ⊢ (𝜌, 𝜎, branchto) ⇓ true                   Λ ⊢ (𝜌, 𝜎, branchto) ⇓ false

                        ∀i ∈ (1 . . . k), Λ(x𝑖 ) = r𝑖                Λ ⊢ (𝜌, 𝜎, e) ⇓ {r1, . . . , rC }
                Λ ⊢ (𝜌, 𝜎, {x1, . . . , x𝑘 }) ⇓ {r1, . . . , r𝑘 }         Λ ⊢ (𝜌, 𝜎, ∥e∥) ⇓ C

            Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ r         Λ ⊢ (𝜌, 𝜎, e2 ) ⇓ {r1, . . . , r𝑘 }       ∃i ∈ (1 . . . k), ri = r
                                           Λ ⊢ (𝜌, 𝜎, e1 ∈e2 ) ⇓ true

            Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ r         Λ ⊢ (𝜌, 𝜎, e2 ) ⇓ {r1, . . . , r𝑘 }       ∀i ∈ (1 . . . k), ri ≠ r
                                          Λ ⊢ (𝜌, 𝜎, e1 ∈e2 ) ⇓ false
                           Figure 10. Cassiopea semantics for expressions.




                                                           11
   Machine State. In addition to the execution environment,              skip or crash) and in the course of doing so changes the ma-
we also need a representation of machine state. We define                chine state from 𝜌, 𝜎 to 𝜌 ′, 𝜎 ′, and produces a branching state
two stores, one for registers and one for memory. The regis-             𝜉, which can be either an 8-bit bitvector, the reserved value
ter store 𝜌 maps registers r to values v. The memory store 𝜎             ext, or a dot (·). As with expressions, statements can fail. Ex-
is more complicated: it maps pairs (xmem, C) (that is, pointer           plicit failure rules are shown for bad stores (corresponding to
literals) to pairs (v, C𝑙 ), where v is the value stored at that         the cases for bad fetches) and for a failed assertions. We also
location and C𝑙 is the bit width. The bit widths of memory               similarly include, but do not show, the obvious failure prop-
regions are invariant, both across the region when they are              agation rules for cases where sub-statements, or expressions
declared and also over time. They are used to check the ac-              within statements, fail.
cess widths appearing in fetch and store operations. Also                   Declarations. The semantics for declarations have judg-
note that new entries cannot be created in either the register           ments of the form Λ, (𝜌, 𝜎) ⊢ decl ▷ Λ′, shown in Figure 12.
store or the memory store, as real hardware does not permit              This means that the given declaration updates Λ as shown.
such actions. The values stored in registers and memory re-              As stated above, we do not initialize the machine state while
gions are restricted by the typing rules to bitvectors (whether          handling declarations; this instead allows us to work with ar-
constants or pointers) of the appropriate width.                         bitrary (or universally quantified) machine states afterwards.
   Notice that stepping through the declarations does not                However, because the let-binding declaration evaluates an
initialize the machine state. We want to reason about exe-               expression, it potentially needs access to a machine state.
cutions over ranges of possible starting machine states; so              Consequently we write the rules so they accept a machine
instead we provide a judgment that uses the typing envi-                 state as input, but do not update it. In the case of machine
ronments to restricts the stores to forms consistent with the            descriptions, where there is no machine state, we pass empty
declarations. This is discussed further below.                           environments; let declarations in machine descriptions are
   Expressions. We describe expressions with a large-step                not allowed to reference machine state. In the case of the
operational semantics, shown in Figure 10. The form of an                additional declarations that accompany a specification, we
expression semantic judgment is: Λ ⊢ (𝜌, 𝜎, e) ⇓ v, which                pass in the initial machine state; this allows values from the
means that given the environment Λ and the machine state                 initial machine state to be globally bound so they can be
𝜌, 𝜎, the expression e evaluates to the value v. Expressions             referred to in the postcondition.
may refer to the machine state, but not modify it. Expressions              We give first the rules for a list of declarations, then the
can fail; in addition to the explicit failure cases seen, some of        rules for the various declarations, then the rules for a list of
the operators and built-in functions can fail. For example, as           operation definitions and a rule for a single operation defini-
mentioned earlier, attempting bitvector arithmetic other than            tion. Note that several of the declarations do not update Λ,
addition and subtraction on pointers will fail. Furthermore,             and nothing is placed in Λ for memory regions. For registers,
division by zero fails.                                                  only the mapping of the identifier to its underlying register
   Note that we currently do not statically check (in the typ-           r is entered; nothing for r is inserted.
ing rules) that the .txt form is present for every register or              Machines. As with the typing rules, the semantics rule
that it is defined for registers on which it is used. Thus we            for a whole machine description integrates the initial envi-
have an explicit failure rule for when no matching declara-              ronment and gives a judgment of the form ⊢ machine ▷ Λ′,
tion has been seen. We also have failure rules for bad fetch             shown in Figure 13. We also include a comparable form that
operations: if the length annotation is wrong, if the pointer            includes additional declarations, as it will be used below.
is not in the machine state (this covers both unaligned ac-                 Programs. Instructions update the machine state, and we
cesses and out of bounds accesses), or if the value used is              chose to represent programs as lists of instructions rather
not a pointer. Similarly, we have failure rules for when bit             than having dummy instruction forms for skip and sequence.
indexing/slicing a pointer. We do not, conversely, need ex-              Consequently the form of the judgments is slightly different,
plicit failure checks or rules for the bit indexes in the bit            and there are several of them, shown in Figure 14.
extraction/slicing constructs as they are statically checked.               First, we can execute an individual instruction using the
   Also note that we include in the semantics the obvious                form Λ ⊢ (𝜌, 𝜎, inst) → (𝜌 ′, 𝜎 ′, 𝜉), meaning that the instruc-
failure propagation rules for when subexpressions fail. We               tion executes and updates the machine state 𝜌, 𝜎 to 𝜌 ′, 𝜎 ′, pro-
do not show these explicitly as they are not particularly                ducing the branching state 𝜉. Then, a list of instructions exe-
interesting or informative; however, note that the && and ||             cutes using the form Λ ⊢ (𝜌, 𝜎, insts, 𝜉) → (𝜌 ′, 𝜎 ′, insts ′, 𝜉 ′),
logical operators short-cut left to right.                               which means that the list steps to a new list and updates
   Statements. Unlike expressions, statements can change                 both the machine state and the branching state. When the
machine state. Thus, the form of a machine state semantics               instruction list runs out, these reduce to a shorter form via
judgment (also large step) is Λ ⊢ (𝜌, 𝜎, S) ⇓ (𝜌 ′, 𝜎 ′, S ′, 𝜉),        a judgment of the form Λ ⊢ (𝜌, 𝜎, insts, 𝜉) → (𝜌 ′, 𝜎 ′), which
shown in Figure 11. This means that the statement S eval-                discards the instructions and branching state and produces
uates to the irreducible statement S’ (which must be either
                                                                    12
                                                           (Statement Semantics)
                                Λ ⊢ (𝜌, 𝜎, S1 ) ⇓ (𝜌 ′, 𝜎 ′, skip, ·)            Λ ⊢ (𝜌 ′, 𝜎 ′, S2 ) ⇓ (𝜌 ′′, 𝜎 ′′, S2′ , ·)
                                                       Λ ⊢ (𝜌, 𝜎, S1 ; S2 ) ⇓ (𝜌 ′′, 𝜎 ′′, S2′ , ·)

                    ∀i, Λ ⊢ (𝜌, 𝜎, e𝑖 ) ⇓ v𝑖        Λ(xproc ) = {x𝑖 , S}           Λ[∀i, x𝑖 ↦→ v𝑖 ] ⊢ (𝜌, 𝜎, S) ⇓ (𝜌 ′, 𝜎 ′, S ′, ·)
                                                      Λ ⊢ (𝜌, 𝜎, xproc (e𝑖 )) ⇓ (𝜌 ′, 𝜎 ′, S ′, ·)

                                      Λ ⊢ (𝜌, 𝜎, e) ⇓ v            Λ[x ↦→ v] ⊢ (𝜌, 𝜎, S) ⇓ (𝜌 ′, 𝜎 ′, S ′, ·)
                                               Λ ⊢ (𝜌, 𝜎, let x : 𝜏base = e in S) ⇓ (𝜌 ′, 𝜎 ′, S ′, ·)

                               ∀i ∈ (C1, C1 + 1, . . . , C2 ), Λ[x ↦→ i] ⊢ (𝜌𝑖 , 𝜎𝑖 , S) ⇓ (𝜌𝑖+1, 𝜎𝑖+1, skip, ·)
                                   Λ ⊢ (𝜌𝐶1 , 𝜎C1 , for x ∈ (C1 . . . C2 ) do S) ⇓ (𝜌 C2 +1, 𝜎C2 +1, skip, ·)

                                         Λ ⊢ (𝜌, 𝜎, e) ⇓ true              Λ ⊢ (𝜌, 𝜎, S) ⇓ (𝜌𝑡 , 𝜎𝑡 , S𝑡 , ·)
                                                Λ ⊢ (𝜌, 𝜎, if e then S else _) ⇓ (𝜌𝑡 , 𝜎𝑡 , S𝑡 , ·)

                                        Λ ⊢ (𝜌, 𝜎, e) ⇓ false              Λ ⊢ (𝜌, 𝜎, S) ⇓ (𝜌 𝑓 , 𝜎 𝑓 , S 𝑓 , ·)
                                                Λ ⊢ (𝜌, 𝜎, if e then _ else S) ⇓ (𝜌 𝑓 , 𝜎 𝑓 , S 𝑓 , ·)

                               Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ r         r∈𝜌           Λ ⊢ (𝜌, 𝜎, e2 ) ⇓ v             𝜌 ′ = 𝜌 [r ↦→ v]
                                                     Λ ⊢ (𝜌, 𝜎, e1 : = e2 ) ⇓ (𝜌 ′, 𝜎, skip, ·)

          Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ (xmem, C)          𝜎 (xmem, C) = (_, C𝑙 )            Λ ⊢ (𝜌, 𝜎, e2 ) ⇓ v           𝜎 ′ = 𝜎 [(xmem, C) ↦→ (v, C𝑙 )]
                                               Λ ⊢ (𝜌, 𝜎, store(e1, C𝑙 ) ← e2 ) ⇓ (𝜌, 𝜎 ′, skip, ·)

                                 Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ (xmem, C)              𝜎 (xmem, C) = (_, C𝑚 )               C𝑚 ≠ C𝑙
                                           Λ ⊢ (𝜌, 𝜎, store(e1, C𝑙 ) ← e2 ) ⇓ (𝜌, 𝜎, crash, ·)

                Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ (xmem, C)           (xmem, C) ∉ 𝜎                                Λ ⊢ (𝜌, 𝜎, e1 ) ⇓ 0bC
              Λ ⊢ (𝜌, 𝜎, store(e1, C𝑙 ) ← e2 ) ⇓ (𝜌, 𝜎, crash, ·)               Λ ⊢ (𝜌, 𝜎, store(e1, C𝑙 ) ← e2 ) ⇓ (𝜌, 𝜎, crash, ·)

                                   Λ ⊢ (𝜌, 𝜎, e) ⇓ true                                    Λ ⊢ (𝜌, 𝜎, e) ⇓ false
                        Λ ⊢ (𝜌, 𝜎, assert(e)) ⇓ (𝜌, 𝜎, skip, ·)                 Λ ⊢ (𝜌, 𝜎, assert(e)) ⇓ (𝜌, 𝜎, crash, ·)

                                 Λ ⊢ (𝜌, 𝜎, e) ⇓ 0                        Λ ⊢ (𝜌, 𝜎, e) ⇓ 0bC               0x00 < 0bC < 0xff
                    Λ ⊢ (𝜌, 𝜎, BRANCH(e)) ⇓ (𝜌, 𝜎, skip, ·)                 Λ ⊢ (𝜌, 𝜎, BRANCH(e)) ⇓ (𝜌, 𝜎, skip, 0bC)

                                                               Λ ⊢ (𝜌, 𝜎, e) ⇓ 0xff
                                                  Λ ⊢ (𝜌, 𝜎, BRANCH(e)) ⇓ (𝜌, 𝜎, skip, ext)
                                           Figure 11. Cassiopea semantics for statements.

an output machine state. That in turn allows us to draw con-                        We include a final judgment of the form machine ⊢
clusions of the form machine ⊢ (𝜌, 𝜎, program) → (𝜌 ′, 𝜎 ′),                     (𝜌, 𝜎, program) → (𝜌 ′, 𝜎 ′) that puts the machine on the
which means that a machine with the initial state 𝜌, 𝜎 exe-                      left-hand side of the turnstile. It means that under a given
cutes the program to produce the new machine state (𝜌 ′, 𝜎 ′).                   machine the program maps 𝜌, 𝜎 to 𝜌 ′, 𝜎 ′. There is a limitation
   Note that there are two versions of the judgment for in-                      in the way we have formulated programs and the rules for
structions, one specialized for no arguments/operands. In-                       programs, which is that there is no easy way to represent fail-
structions with no operands are declared as taking unit, but                     ure. (Failure in this might represent triggering an exception
invoked with empty operands (not with unit) to correspond                        and stopping execution, which we do not model, or invoking
to the way assembly languages normally work.                                     “unpredictable” or “undefined” behavior in the processor and
                                                                                 transitioning to an arbitrary unknown machine state.)
                                                                           13
                                                      (Declaration Semantics)
                                                      Λ, (𝜌, 𝜎) ⊢ decl ▷ Λ′          Λ′, (𝜌, 𝜎) ⊢ decls ▷ Λ′′
                                Λ, (𝜌, 𝜎) ⊢ 𝜖 ▷ Λ                   Λ, (𝜌, 𝜎) ⊢ decl; decls ▷ Λ′′

                                                                                   Λ ⊢ (𝜌, 𝜎, e) ⇓ v
                            Λ, (𝜌, 𝜎) ⊢ type x𝜏 = 𝜏base ▷ Λ         Λ, (𝜌, 𝜎) ⊢ let x : 𝜏base = e ▷ Λ[x ↦→ v]

                                                Λ ⊢ (𝜌, 𝜎, x) ⇓ r           Λ ⊢ (𝜌, 𝜎, e) ⇓ v
                                             Λ, (𝜌, 𝜎) ⊢ let x.txt = 𝑒 ▷ Λ[r.txt ↦→ v]

                             Λ′ = Λ[xfunc ↦→ {x𝑖 , e}]                                 Λ′ = Λ[xproc ↦→ {x𝑖 , S}]
                Λ, (𝜌, 𝜎) ⊢ def xfunc x𝑖 : 𝜏base𝑖 → 𝜏base = e ▷ Λ′          Λ, (𝜌, 𝜎) ⊢ proc xproc x𝑖 : 𝜏base𝑖 → () = S ▷ Λ′

                            Λ′ = Λ[x ↦→ r]          r fresh                   Λ′ = Λ[x ↦→ r]           r fresh
                         Λ, (𝜌, 𝜎) ⊢ letstate x : 𝜏reg ▷ Λ     ′
                                                                    Λ, (𝜌, 𝜎) ⊢ letstate control x : 𝜏reg ▷ Λ′

                                                      Λ′ = Λ[x ↦→ r]             r fresh
                                       Λ, (𝜌, 𝜎) ⊢ letstate control dontgate x : 𝜏reg ▷ Λ′

                                                                                  Λ′ = Λ[x ↦→ (xmem, 0)]
                     Λ, (𝜌, 𝜎) ⊢ letstate xmem : 𝜏mem ▷ Λ            Λ, (𝜌, 𝜎) ⊢ letstate xmem : 𝜏mem with x ▷ Λ′

                                                    Λ, (𝜌, 𝜎) ⊢ defop ▷ Λ′           Λ′, (𝜌, 𝜎) ⊢ defops ▷ Λ′′
                              Λ, (𝜌, 𝜎) ⊢ 𝜖 ▷ Λ                    Λ, (𝜌, 𝜎) ⊢ defop; defops ▷ Λ′

                                                         Λ′ = Λ[xop ↦→ {[ ], e, 𝑆 }]
                                            Λ, (𝜌, 𝜎) ⊢ defop xop {txt = e, sem = S} ▷ Λ′

                                                         Λ′ = Λ[xop ↦→ {𝑥𝑖 , e, 𝑆 }]
                                       Λ, (𝜌, 𝜎) ⊢ defop xop x𝑖 : 𝜏base𝑖 {txt = e, sem = S} ▷ Λ′
                                         Figure 12. Cassiopea semantics for declarations.

                   (Machine Semantics)                                      (they are properties on initial and final register and mem-
                                                                            ory states), and the last one says what it means for a pro-
      Λbuiltin, ({}, {}) ⊢ decls ▷ Λ     Λ ⊢ defops ▷ Λ′                    gram to satisfy a specification. Note that the reg-modify and
                                                                            mem-modify rules as shown are slightly misleading, because
                     ⊢ decls; defops ▷ Λ′                                   the register and pointer list provided in the input specifica-
      Figure 13. Cassiopea semantics for machines.                          tion is implicitly augmented with all registers and pointers
                                                                            mentioned in the postcondition before it gets to this point.
                                                                               Machine State Validity. As discussed above, we do not
                                                                            initialize the machine state while processing declarations.
   The intended behavior is that a program that fails during                Instead we treat the starting machine state as an input (e.g.,
execution (that is, the body of one of its instructions steps to            in the final judgment about programs) or quantify it uni-
crash) enters a state where no postcondition can evaluate                   versally as in the specification judgment. This requires that
to true. We have decided for the moment that working                        we have a predicate to reject machine states that do not
this explicitly into the formalism would result in a lot of                 match the machine description. The validity judgment has
complication and obscuration without providing any useful                   the form Δ, Γ, Λ ⊢ 𝜌, shown in Figure 16, and correspond-
information.                                                                ingly for 𝜎 (except without Λ) and then for 𝜌, 𝜎 (both stores
   Specifications. For specifications we need three judg-                   at once). This means that the given stores match the given
ments, shown in Figure 15: the first two state what the                     environments.
reg-modify and mem-modify clauses mean, respectively
                                                                       14
                                                          (Program Semantics)
                                     Λ(xop ) = {[ ], _, 𝑆)}             Λ ⊢ (𝜌, 𝜎, S) ⇓ (𝜌 ′, 𝜎 ′, skip, 𝜉)
                                                        Λ ⊢ (𝜌, 𝜎, xop ) → (𝜌 ′, 𝜎 ′, 𝜉)

       ∀i, Λ ⊢ (𝜌, 𝜎, e𝑖 ) ⇓ v𝑖      Λ(xop ) = {x𝑖 , _, 𝑆 }            Λ′ = Λ[∀𝑖, x𝑖 ↦→ v𝑖 ]            Λ′ ⊢ (𝜌, 𝜎, S) ⇓ (𝜌 ′, 𝜎 ′, skip, 𝜉)
                                                      Λ ⊢ (𝜌, 𝜎, xop e𝑖 ) → (𝜌 ′, 𝜎 ′, 𝜉)

                         Λ ⊢ (𝜌, 𝜎, inst) → (𝜌 ′, 𝜎 ′, 𝜉)
                 Λ ⊢ (𝜌, 𝜎, inst; insts, ·) → (𝜌 ′, 𝜎 ′, insts, 𝜉)         Λ ⊢ (𝜌, 𝜎, inst; insts, 0x01) → (𝜌, 𝜎, insts, ·)

                                        0bC > 0x01
              Λ ⊢ (𝜌, 𝜎, inst; insts, 0bC) → (𝜌, 𝜎, insts, 0bC b− 0x01)                      Λ ⊢ (𝜌, 𝜎, _, ext) → (𝜌, 𝜎, 𝜖, ext)

                                   ⊢ machine ▷ Λ             Λ ⊢ (𝜌, 𝜎, program, ·) →∗ (𝜌 ′, 𝜎 ′, 𝜖, 𝜉)
                                               machine ⊢ (𝜌, 𝜎, program) → (𝜌 ′, 𝜎 ′, 𝜉)
                                          Figure 14. Cassiopea semantics for programs.

                                                       (Specification Semantics)
                                        ∀i, Λ ⊢ (𝜌, 𝜎, xregi ) ⇓ r𝑖            ∀r ∉ {r𝑖 }, 𝜌 (r) = 𝜌 ′ (r)
                                                     Λ, 𝜌, 𝜎, 𝜌 , 𝜎 ⊢ reg-modify : xregi
                                                              ′    ′


  ∀i, Λ ⊢ (𝜌, 𝜎, (xmemi , e𝑖 )) ⇓ (xmemi , C𝑖 )        ∀xmem, C, (xmem, C) ∉ {(xmemi , C𝑖 )},                 𝜎 ((xmem, C)) = 𝜎 ′ ((xmem, C))
                                               Λ, 𝜌, 𝜎, 𝜌 ′, 𝜎 ′ ⊢ mem-modify : (xmemi , e𝑖 )

                                                       Λ, 𝜌, 𝜎, 𝜌 ′, 𝜎 ′ ⊢ frame             Λ, 𝜌, 𝜎, 𝜌 ′, 𝜎 ′ ⊢ frames
                             Λ, 𝜌, 𝜎, 𝜌 ′, 𝜎 ′ ⊢ 𝜖                  Λ, 𝜌, 𝜎, 𝜌 ′, 𝜎 ′ ⊢ frame frames

                       ⊢ machine; decls ▷ Δ, Γ      ⊢ machine ▷ Λ          ∀𝜌, 𝜎, (Δ, Γ, Λ ⊢ 𝜌, 𝜎) =⇒
Λ, (𝜌, 𝜎) ⊢ decls ▷ Λ′ =⇒        Λ′ ⊢ (𝜌, 𝜎, pre) ⇓ true =⇒          ∀𝜌 ′, 𝜎 ′, (Λ′ ⊢ (𝜌, 𝜎, program, ·) →∗ (𝜌 ′, 𝜎 ′, 𝜖, 𝜉)) =⇒
                         (Λ′ [EXTBRANCH ↦→ 𝜉] ⊢ (𝜌 ′, 𝜎 ′, post) ⇓ true ∧ Λ′, 𝜌, 𝜎, 𝜌 ′, 𝜎 ′ ⊢ frames)
                                            machine, (decls; frame; pre; post) ⊢ program
                                       Figure 15. Cassiopea semantics for specifications.

                                                        (Machine State Validity)
                           (∀x, Δ, Γ ⊢ x : C reg ∧ Λ(x) = r) ⇔ (∃v, 𝜌 (r) = v ∧ Δ, Γ ⊢ v : C bit)
                                                                   Δ, Γ, Λ ⊢ 𝜌

                                            ∀xmem, Δ, Γ ⊢ xmem : C1 bit C2 len C3 ref ⇔
                    (∀i ∈ {0, C1 /8, . . . , (C2 − 1) ∗ C1 /8}, ∃v, 𝜎 (xmem, i) = (v, C1 ) ∧ Δ, Γ ⊢ v : C1 bit) ∧
                              (∀i ∉ {0, C1 /8, . . . , (C2 − 1) ∗ C1 /8}, Λ ⊢ (𝜌, 𝜎, (xmem, i)) ⇓ fail)
                                                                       Δ, Γ ⊢ 𝜎

                                                          Δ, Γ, Λ ⊢ 𝜌             Δ, Γ ⊢ 𝜎
                                                                  Δ, Γ, Λ ⊢ 𝜌, 𝜎
                                           Figure 16. Cassiopea machine state validity.




                                                                          15
   We use this with the typing environments that come from            6   Alewife Overview
both the machine description and the additional declarations          This section describes Alewife, our specification language
arising from a specification. In the case of registers we need        for writing abstracted machine-independent specifications
access to Λ to handle the names of registers. We do not use           of low-level code.
the Λ generated from the additional declarations in a speci-             Alewife specifications are abstractions of machine-level
fication; this avoids circularity. This is acceptable, because        Cassiopea specifications; we say that Cassiopea constructs
specifications are not allowed to define new registers. For           are lifted into Alewife and Alewife constructs are lowered
memory regions we need to enumerate the valid offsets for             into Cassiopea. Alewife is only for specifications, so there
the region (note the literal 8 that hardwires 8-bit bytes) and        are no statements, no updates, and no notion of instructions
check the cell width.                                                 or programs. We refer to the single synthesis problem in one
   Branching. To handle branching, we allow statements                Alewife specification as a block.
to produce a branching state, which indicates the number                 Notation. We use the following metavariables:
of instructions to skip over. Normally this is ·, which means             x, y, z Program variables (binders)
none and has no effect; however, when an instruction body                 r        Registers (abstract)
produces something else we use it to branch. A nonzero                    C        Integer constants (written in decimal)
bitvector results in skipping the indicated number of instruc-            0bC      Bitvector constants (written in binary)
tions; the out-of-band additional value ext causes a branch               N        Symbolic integer constants
to the external label. The magic number used to select the                𝜏        Types
external label appears only in one of the statement rules;                v        Values
beyond that point we use ext explicitly.                                  e        Expressions
   The program rule in Figure 15 inserts the branch state                 i, j     Rule-level integers
produced by the program into Λ, where it provides a value                (Other constructions are referred to with longer names.)
for the branchto predicate found in the postcondition. This              As noted previously, Alewife types and expressions should
allows specifications to enforce the external branching be-           be considered distinct from Cassiopea ones (even where they
havior.                                                               correspond directly). We use the same letters in the hopes
                                                                      that this will cause less confusion (even in the definition
                                                                      of the translation) than picking an entirely different set of
                                                                      letters for Alewife.
                                                                         Identifiers and Variables. In Alewife there are five syn-
                                                                      tactic categories of identifiers: As in Cassiopea, xmem name
                                                                      memory regions. xfunc name functions, and x𝜏 are type aliases.
                                                                      xmodule name Cassiopea lowering modules, which are used
                                                                      to instantiate the abstract elements and conduct Alewife–
                                                                      Cassiopea translation for synthesis. Other x are ordinary
                                                                      variables that range over other things, and may be presumed
                                                                      to not range over the above reserved categories. All variables
                                                                      are immutable, in the sense that their values do not change
                                                                      once bound.
                                                                         Symbolic Constants. In Alewife symbolic constants N
                                                                      are permitted to occur in some places where only integer
                                                                      constants are allowed in the corresponding Cassiopea con-
                                                                      structions. In particular, the bit sizes associated with types
                                                                      (and the lengths of memory regions, which are functionally
                                                                      similar) may be given as symbolic values x instead of integer
                                                                      constants. These must be bound to integer constants either
                                                                      directly in the Alewife spec, in the Cassiopea lowering, or
                                                                      by the Cassiopea machine description. This allows the con-
                                                                      crete sizes of bitvectors to vary depending on the machine
                                                                      architecture.
                                                                         Types. As in Cassiopea, Alewife types are divided syn-
                                                                      tactically into base types and others, shown in Figure 17.
                                                                      The chief difference from Cassiopea is that bit widths (and
                                                                      the lengths of memory regions) can be symbolic constants.

                                                                 16
                                                                                                        (Alewife Operators)
                                                                          unop F                            − | b− | ¬ | bnot
                                                                          binop F        = | ≠ | + | − | ∗ | / | < | <= | > | >=
                      (Alewife Symbolic Constants)                         |                                           && | || | ⊕
      N F                                           C|x                    |                 >>| >>𝑆 |<<| band | bor | bxor
                                                                           |                                  b+ | b− | b∗ | b/
                                      (Alewife Types)                      |                              b< | b<= | b> | b>=
     𝜏F                               𝜏base | 𝜏mem | 𝜏func                 |                        bs< | bs<= | bs> | bs>=
                                                                           |                                           ∪ | ∩ |⊆| \
     𝜏base F                             int | bool | x𝜏
      |                         N vec | N ptr | N reg                                                 (Alewife Expressions)
      |                                  N label | 𝜏regs                  eF                                                    v|x
     𝜏regs F                                 N reg set                     |                                               xfunc (e)
                                                                           |                                                 unop e
     𝜏mem F                      N1 bit N2 len N3 ref                      |                                           e1 binop e2
     𝜏func F                               𝜏base𝑖 → 𝜏base                  |                                   e[C] | e[C1, C2 ]
                                                                           |                             let x : 𝜏base = e1 in e2
                                     (Alewife Values)                      |                              if e1 then e2 else e3
      vF            true | false | C | 0bC | (xmem, C)                     |                                             (xmem, e)
      |                                             fail                                                       ∗
                                                                           |                                       e | fetch(e, N )
                                                                           |                                            branchto
                                                                           |                                          {x1, . . . , x𝑘 }
                                                                           |                                           ∥e∥ | e1 ∈e2
                      Figure 17. Alewife symbolic constants, types, values, operators and expressions.

However, an additional difference is that pointers (ptr) are           on machine state or that depend on machine state on some
distinguished from plain bitvectors (vec). This is reasonably          machines and not others. Such functions can also depend on
possible in Alewife, because it need not reason about the              constants or other elements that are not visible in the Alewife
progression of values through machine registers, only before           specification at all. The lower-with declarations specify all
and after states. Strings and unit are also absent, as they are        lowering modules that are used to compile this Alewife spec-
not needed for specifications.                                         ification into a Cassiopea specification. The module name
   Values and Expressions. The values in Alewife corre-                xmodule is used to look up the Cassiopea lowering module
spond directly to the values in Cassiopea as do operators and          to apply. The region declarations declare memory regions,
most expressions, shown in Figure 17. Note that the width              like the memory-typed letstate declarations in Cassiopea.
argument of fetch can be a symbolic size.                              (These are implicitly always provide, because, for memory
   Declarations and Frames. Alewife declarations come in               regions, the corresponding require declaration would be
two forms: require and provide, shown in Figure 18. The                entirely equivalent, requiring duplication in the Cassiopea
second form declares elements in the ordinary way, while               lowering.) Note that the parameters of the region can be
the first form declares an element that must be provided               symbolic constants if abstraction is needed.
by the Cassiopea lowerings or the Cassiopea machine de-                   Frame declarations in Alewife, annotated with
scription. In this case, the type is given, but not the value.         reg-modify and mem-modify, are exactly the same as in
This functions as a form of import, and allows an Alewife              Cassiopea. Because Alewife files are machine-independent,
file to be checked on its own separately from any particular           the registers mentioned must be abstract and concretized
machine description or Cassiopea lowerings. However, we                via the Cassiopea lowerings.
do not currently define or implement such a check. Note that              Block-lets. While Alewife expressions include let-
it is possible to require functions that implicitly depend             bindings, the scope of those let-bindings is conventional:
                                                                  17
                                       (Alewife Declarations)
      decls F                                      𝜖 | decl; decls
      decl F                                   require type x𝜏
       |                                require value x : 𝜏base                                            (Initial State Bindings)
       |                              require func xfunc : 𝜏func                      block-lets F            𝜖 | block-let; block-lets
       |                                   provide type x𝜏 = 𝜏                        block-let F                     let x : 𝜏base = e
       |                             provide value x : 𝜏base = e                                        (Alewife Specifications)
       |             provide func xfunc : x𝑖 : 𝜏base𝑖 → 𝜏base = e                      pre F                                          e
       |                                     region xmem : 𝜏mem                        post F                                         e
       |                             region xmem : 𝜏mem with x                         spec F             decls; block-lets; pre; post
       |                                     lower-with xmodule
       |                                         reg-modify : x𝑖
       |                                mem-modify : (xmemi , e𝑖 )
                                 Figure 18. Alewife declarations, block-lets, and specifications.

it lasts until the end of the expression. To refer to values                 Translation. The translation (lowering) from Alewife
taken from the initial state (that is, the machine state of               to Cassiopea, defined in the next section, appears cross-
which the precondition must be true), we need a way to bind               recursively in the rules in this section. Because Δ, Γ are Cass-
these values so their scope extends to the postcondition. The             iopea environments, they map identifiers to Cassiopea types,
block-lets serve this purpose in Alewife, shown in Figure 18,             not Alewife ones. This means Alewife types must be lowered
much like the additional declarations seen in Cassiopea specs             on the fly to update them correctly.
can. These are found within a block (because a block corre-                  Integer Constant Extraction. The integer constant ex-
sponds to a synthesis problem, it is meaningful to associate              traction rules do a simple pass over Cassiopea declarations to
before and after machine states with it), and the scope is the            extract the variables defined as integer constants, shown in
entire block.                                                             Figure 19. These populate a substitution environment Σ that
   Specifications. A full specification starts with a preamble            we use for lowering Alewife types containing symbolic con-
of declarations, shown in Figure 18. It also includes block-              stants. These rules are judgments of the form Σ ⊢ decl ▷ Σ ′
lets and the pre- and post-conditions for the block. Common               or Σ ⊢ decls ▷ Σ ′, plus one of the form ⊢ machine ▷ Σ for a
declarations can be shared with include.                                  whole machine description.
                                                                             Typing. The declaration typing rules are intended to ac-
                                                                          cumulate types for all the declarations in an Alewife spec-
7   Alewife Typing and Semantics                                          ification. They are applied concurrently with the Cassio-
We do not provide (or implement) a full typechecking pass for             pea declaration rules to the Alewife specification, the Cass-
Alewife. Instead, when we lower to Cassiopea, we allow the                iopea machine description, and the Cassiopea lowering.
Cassiopea typechecker to reject invalid results, which might              The declaration typing rules have judgments of the form
be caused by invalid Alewife input or by bad/mismatched                   Δ, Γ, Σ ⊢ decl ▷Δ ′, Γ ′, Σ ′ and Δ, Γ, Σ ⊢ decls▷Δ ′, Γ ′, Σ ′, shown
Cassiopea lowering definitions. The rules provided here are               in Figure 20. These mean that the declaration or declarations
for doing scans over the declarations sufficient to make the              update the type environment (and integer constant environ-
translation to Cassiopea work and no more.                                ment) as shown. Note that there is a special-case rule for
   Environments. We retain the Cassiopea typing environ-                  provide value for when the value is an integer constant;
ments, Δ, Γ. We add an additional environment Σ, which                    this enters the constant into Σ. The integer constants are
maps identifiers to integer constants. This is a projection of            in turn used when lowering the types of memory regions,
the Cassiopea execution environment Λ: it holds mappings                  which can be seen in the last two rules.
only for variables defined as integer constants and excludes                 Block-lets. The rules for block-lets are effectively the
everything else. We include a separate set of rules for extract-          same as the rules for declarations, shown in Figure 21. The
ing these integer constants without doing a full Cassiopea                ways in which block-lets are special mostly do not apply
execution. (Among other things, this avoids involving ma-                 here. Note however that even though we pass through Σ
chine state or the machine state stores.)                                 (for consistency of the form of the rules) there is no rule

                                                                     18
                                          (Cassiopea Integer Constant Extraction)
                                            Σ ⊢ decl ▷ Σ ′       Σ ′ ⊢ decls ▷ Σ ′′      Σ ⊢ decls ▷ Σ ′
                              Σ⊢𝜖▷Σ                Σ ⊢ decl; decls ▷ Σ ′′             ⊢ decls; defops ▷ Σ ′

                                                             Σ ′ = Σ[x ↦→ C]                    e≠C
                         Σ ⊢ type x𝜏 = 𝜏base ▷ Σ     Σ ⊢ let x : int = C ▷ Σ      ′
                                                                                      Σ ⊢ let x : 𝜏base = e ▷ Σ

                        Σ ⊢ def xfunc x𝑖 : 𝜏base𝑖 → 𝜏base = e ▷ Σ        Σ ⊢ proc xproc x𝑖 : 𝜏base𝑖 → () = S ▷ Σ

                                   Σ ⊢ letstate x : 𝜏reg ▷ Σ        Σ ⊢ letstate xmem : 𝜏mem ▷ Σ

                                 Σ ⊢ letstate xmem : 𝜏mem with x ▷ Σ            Σ ⊢ let x.txt = e ▷ Σ
                                        Figure 19. Cassiopea integer constant extraction.

for loading integer constants into Σ from block-lets. Integer               The fixpoint-based evaluation strategy for declarations
constants used in types and defined in the Alewife specifica-            is required, because the Alewife declarations rely on the
tion should be defined with provide value; block-lets are                Cassiopea lowering file (most notably for resolving sym-
intended to provide access to machine state.                             bolic constants), but the Cassiopea lowering file is in turn
   Specifications. The rule for the semantics of an entire               also specifically allowed to refer to objects declared by the
specification is large and complex. The conclusion is that               Alewife specification, such as memory regions. In the im-
a given machine, lowering module, and Alewife specifica-                 plementation this circularity is resolved by lifting both the
tion produce a final translation output Ω. The rules work by             Cassiopea and Alewife declarations (and block-lets) into
nondeterministically taking fixpoints over all the material              a common representation and topologically sorting them
included. decls is the combination of all declarations found             based on identifier references. (Genuinely circular references
both in the initial specification and all the included lowering          among identifiers are prohibited.) From this point, they can
modules, and frames is the combination of all frame infor-               be handled in order in a more conventional way.
mation (part of the declarations in Alewife; separated in                   Complete Output. Note that the output includes the
Cassiopea). Similarly, the final set of environments Γ, Δ, Σ             declarations from the Cassiopea lowering modules (each
represent fixpoints produced by processing all the declara-              declslower ). Apart from symbolic constants, we do not substi-
tions.                                                                   tute the definitions of the lowering elements, as that would
   In Figure 22, the first premise expands the Alewife specifi-          greatly complicate things, especially with functions; instead
cation as we will need to work with the components. The                  we include the definitions and let the translation refer to
next two premises generate initial environments: the Cassio-             them. In fact, because of the declaration ordering issues, in
pea typing environments induced by the machine descrip-                  the implementation the lowering declarations and translated
tion, and its integer constants, and then we require that these          Alewife declarations can be arbitrarily interleaved in the
are included in the final environments. In the fifth and sixth           output.
premises, we then require that the result of processing the                 Note furthermore that it would not be sufficient to in-
declarations from the specification appears in the final envi-           clude only the lowering declarations explicitly imported
ronments, and that the translation of these to Cassiopea is              with require declarations, as those may refer freely to other
included in the final declarations and frame rules. Then for             things declared in the lowering module that the Alewife
every lowering module requested by the specification, we                 specification itself may have no cognizance of whatsoever.
require that it be provided in the input modules list and that
its components appear in the final declarations and frame
rules. This is followed by two more rules to ensure that these
results are represented in the final environments. Later, we
include the block-let material in the final environments, in-
clude its lowered form in the final declaration list (block-lets
lower to declarations), bind the lowerings of the pre- and
postconditions, and define the output.


                                                                    19
                                                    (Alewife Declaration Typing)
                                     Δ, Γ, Σ ⊢ decl ▷ Δ ′, Γ ′, Σ ′      Δ ′, Γ ′, Σ ⊢ decls ▷ Δ ′′, Γ ′′, Σ ′′
                                                    Δ, Γ, Σ ⊢ decl; decls ▷ Δ ′′, Γ ′′, Σ ′′

                                       Δ ⊢wf x𝜏                          Δ, Γ, Σ ⊢ AC⟦𝜏base ⟧ = 𝜏                 Γ(x) = 𝜏
                         Δ, Γ, Σ ⊢ require type x𝜏 ▷ Δ, Γ, Σ           Δ, Γ, Σ ⊢ require value x : 𝜏base ▷ Δ, Γ, Σ

                                               Δ, Γ, Σ ⊢ AC⟦𝜏func ⟧ = 𝜏            Γ(xfunc ) = 𝜏
                                             Δ, Γ, Σ ⊢ require func xfunc : 𝜏func ▷ Δ, Γ, Σ

                                     Δ, Γ, Σ ⊢ AC⟦𝜏⟧ = 𝜏 ′             Δ ⊢wf 𝜏 ′       Δ ′ = Δ[x𝜏 → 𝜏 ′]
                                                Δ, Γ, Σ ⊢ provide type x𝜏 = 𝜏 ▷ Δ ′, Γ, Σ

                                     Δ, Γ ⊢ C : int         Γ ′ = Γ[x ↦→ int]            Σ ′ = Σ[x ↦→ C]
                                           Δ, Γ, Σ ⊢ provide value x : int = C ▷ Δ, Γ ′, Σ ′

          Δ, Γ, Σ ⊢ AC⟦𝜏base ⟧ = 𝜏      Δ ⊢wf 𝜏         e≠C           Δ, Γ, Σ ⊢ AC⟦e⟧ = e ′             Δ, Γ ⊢ e ′ : 𝜏       Γ ′ = Γ[x ↦→ 𝜏]
                                            Δ, Γ, Σ ⊢ provide value x : 𝜏base = e ▷ Δ, Γ ′, Σ

                               ∀i, Δ, Γ, Σ ⊢ AC⟦𝜏base𝑖 ⟧ = 𝜏𝑖 ∧ Δ ⊢wf 𝜏𝑖              Δ, Γ, Σ ⊢ AC⟦𝜏base ⟧ = 𝜏
       Δ ⊢wf 𝜏          Δ, Γ, Σ ⊢ AC⟦e⟧ = e ′      Γ ′ = Γ [∀i, x𝑖 ↦→ 𝜏𝑖 ]            Δ, Γ ′ ⊢ e ′ : 𝜏 Γ ′′ = Γ [xfunc ↦→ (x𝑖 : 𝜏𝑖 → 𝜏)]
                                Δ, Γ, Σ ⊢ provide func xfunc : x𝑖 : 𝜏base𝑖 → 𝜏base                = e ▷ Δ, Γ ′′, Σ

                                 Δ, Γ, Σ ⊢ AC⟦N1 bit N2 len N3 ref⟧ = C1 bit C2 len C3 ref
                               Δ ⊢wf C1 bit C2 len C3 ref    Γ ′ = Γ [xmem ↦→ C1 bit C2 len C3 ref]
                                     Δ, Γ, Σ ⊢ region xmem : N1 bit N2 len N3 ref ▷ Δ, Γ ′, Σ

               Δ, Γ, Σ ⊢ AC⟦N1 bit N2 len N3 ref⟧ = C1 bit C2 len C3 ref           Δ ⊢wf C1 bit C2 len C3 ref
    Δ ⊢wf C3 label          Δ, Γ, Σ ⊢ AC⟦N3 label⟧ = C3 label      Γ ′ = Γ [xmem ↦→ C1 bit C2 len C3 ref; x ↦→ C3 label]
                                 Δ, Γ, Σ ⊢ region xmem : N1 bit N2 len N3 ref with x ▷ Δ, Γ ′, Σ

                                                  Δ, Γ, Σ ⊢ lower-with xmodule ▷ Δ, Γ, Σ

                          Δ, Γ, Σ ⊢ AC⟦reg-modify : x𝑖 ⟧ = reg-modify : x𝑖                     Δ, Γ ⊢ reg-modify : x𝑖
                                                   Δ, Γ, Σ ⊢ reg-modify : x𝑖 ▷ Δ, Γ, Σ

             Δ, Γ, Σ ⊢ AC⟦mem-modify : (xmemi , e𝑖 )⟧ = mem-modify : (xmemi , e𝑖′)                  Δ, Γ ⊢ mem-modify : (xmemi , e𝑖′)
                                              Δ, Γ, Σ ⊢ mem-modify : (xmemi , e𝑖 ) ▷ Δ, Γ, Σ
                                          Figure 20. Alewife typing rules for declaration.

8     Lowering Alewife                                                         So instead, we write only enough typing rules to prepare
The semantics of an Alewife specification depend on material                material for writing a translation (lowering) to Cassiopea,
taken from a Cassiopea mapping and machine description.                     and then apply the Cassiopea typing (and, implicitly, seman-
This does not preclude defining a semantics for Alewife                     tics) to the lowered material. That material goes into the
in terms of that material or even some abstracted concept                   Cassiopea typing environments Δ, Γ, and as discussed in the
of what any such Cassiopea material might be. However,                      previous section, we also maintain an additional environ-
doing so is complicated (as can be seen from the material                   ment Σ of integer constants used for substituting symbolic
in the previous section, which does not even attempt to                     constants in types.
handle expression evaluation) and not necessarily rewarding                    This section defines the translation. AC⟦𝑎⟧ defines the
or illuminating.                                                            Cassiopea lowering of an Alewife element 𝑎. We make the

                                                                       20
                                                    (Alewife Specification Typing)
                                               Δ, Γ, Σ ⊢ block-let ▷ Δ ′, Γ ′, Σ ′    Δ ′, Γ ′, Σ ⊢ block-lets ▷ Δ ′′, Γ ′′, Σ ′′
                     Δ, Γ, Σ ⊢ 𝜖 ▷ Δ, Γ, Σ                   Δ, Γ, Σ ⊢ block-let; block-lets ▷ Δ ′′, Γ ′′, Σ ′′

                   Δ, Γ, Σ ⊢ AC⟦𝜏base ⟧ = 𝜏        Δ ⊢wf 𝜏     Δ, Γ, Σ ⊢ AC⟦e⟧ = e ′         Δ, Γ ⊢ e ′ : 𝜏     Γ ′ = Γ [x ↦→ 𝜏]
                                                    Δ, Γ, Σ ⊢ let x : 𝜏base = e ▷ Δ, Γ ′, Σ

                            Δ, Γ, Σ ⊢ decls ▷ Δ ′, Γ ′, Σ ′ Δ ′, Γ ′, Σ ′ ⊢ block-lets ▷ Δ ′′, Γ ′′, Σ ′′
     Δ , Γ , Σ ⊢ AC⟦pre⟧ = pre
       ′′    ′′                ′
                                     Δ , Γ , Σ ⊢ AC⟦post⟧ = post ′
                                       ′′ ′′
                                                                              Δ ′′, Γ ′′ ⊢ pre ′ : bool                Δ ′′, Γ ′′ ⊢ post ′ : bool
                                             Δ, Γ, Σ ⊢ decls; block-lets; pre; post ▷ Δ ′′, Γ ′′, Σ ′′
                                         Figure 21. Alewife typing rules for specifications.

                                                  (Alewife Specification Semantics)
                                                  spec = declsale ; block-lets; pre; post
                            ⊢ machine ▷ Δ0, Γ0      ⊢ machine ▷ Σ0         (Δ0 ⊆ Δ) ∧ (Γ0 ⊆ Γ) ∧ (Σ0 ⊆ Σ)
    Δ, Γ, Σ ⊢ declsale ▷ Δ, Γ, Σ   Δ, Γ, Σ ⊢ AC⟦declsale ⟧ ⊆ decls; frames            (∀xmodule , lower-with xmodule ∈ declsale =⇒
                 module xmodule { declslower ; frameslower } ∈ modules ∧ declslower ⊆ decls ∧ frameslower ⊆ frames)
            Δ, Γ ⊢ decls ▷ Δ, Γ   Σ ⊢ decls ▷ Σ        Δ, Γ, Σ ⊢ block-lets ▷ Δ, Γ, Σ      Δ, Γ, Σ ⊢ AC⟦block-lets⟧ ⊆ decls
                  Δ, Γ, Σ ⊢ AC⟦pre⟧ = pre ′         Δ, Γ, Σ ⊢ AC⟦post⟧ = post ′           Ω = decls; frames; pre ′; post ′
                                                         machine, modules, spec ▷ Ω
                                             Figure 22. Alewife semantics for specifications.

                                          Alewife – Cassiopea Type Translation
                   C          N =C                              (
                                                                   Δ(x𝜏 ) x𝜏 ∈ Δ
                  
                  
Δ, Γ, Σ ⊢ AC⟦N ⟧ = Σ(x)        N = x ∧ x ∈ Σ Δ, Γ, Σ ⊢ AC⟦x𝜏 ⟧ =
                  
                  
                                                                   ⊥      x𝜏 ∉ Δ
                               N =x∧x ∉ Σ
                  
                  ⊥
                  
                  
       AC⟦int⟧ = int                                         AC⟦bool⟧ = bool
    AC⟦N vec⟧ = AC⟦N ⟧ bit                                 AC⟦N ptr⟧ = AC⟦N ⟧ bit
    AC⟦N reg⟧ = AC⟦N ⟧ reg                           AC⟦N reg set⟧ = AC⟦N ⟧ reg set

AC⟦N1 bit N2 len N3 ref⟧ = AC⟦N1 ⟧ bit AC⟦N2 ⟧ len AC⟦N3 ⟧ ref
            AC⟦𝜏base𝑖 → 𝜏base ⟧ = AC⟦𝜏base𝑖 ⟧ → AC⟦𝜏base ⟧

                                         Figure 23. Alewife – Cassiopea type translation.

translation polymorphic over the various kinds of element;                     Notice that the translations for require declarations are
that is, AC⟦𝜏⟧ is the translation of a type (shown in Fig-                   empty, because the declarations from the mapping module
ure 23), AC⟦e⟧ is the translation of an expression, etc. Some                are output along with the translated Alewife specification.
of the translation rules rely on the environments; these are
written Δ, Γ, Σ ⊢ AC⟦𝑎⟧ (shown in Figure 24).
   Some of the translation rules produce ⊥. If these are
reached, the translation fails; this can happen if the Ale-
wife spec was malformed and, potentially, if the mapping
module failed to declare elements that were expected of it or
declared them in an incompatible or inconsistent way. The
rules in the previous section exclude some of these cases,
but we are not (yet) prepared to argue that they rule out all
translation-time failures.
                                                                        21
                                        Alewife – Cassiopea Expression Translation
                    (                                          (
                        x   x∈Γ                                  xfunc (AC⟦e⟧) xfunc ∈ Γ
Δ, Γ, Σ ⊢ AC⟦x⟧ =                    Δ, Γ, Σ ⊢ AC⟦xfunc (e)⟧ =
                        ⊥   x∉Γ                                  ⊥             xfunc ∉ Γ
      AC⟦true⟧ = true                           AC⟦false⟧ = false
         AC⟦C⟧ = C                                 AC⟦0bC⟧ = 0bC
    AC⟦unop e⟧ = unop AC⟦e⟧                 AC⟦e1 binop e2 ⟧ = AC⟦e1 ⟧ binop AC⟦e2 ⟧
      AC⟦e[C]⟧ = AC⟦e⟧[C]                    AC⟦e[C1, C2 ]⟧ = AC⟦e⟧[C1, C2 ]
AC⟦let x : 𝜏base = e1 in e2 ⟧ = let x : AC⟦𝜏base ⟧ = AC⟦e1 ⟧ in AC⟦e2 ⟧
 AC⟦if e1 then e2 else e3 ⟧ = if AC⟦e1 ⟧ then AC⟦e2 ⟧ else AC⟦e3 ⟧
                              (
                                (xmem, AC⟦e⟧) xmem ∈ Γ
  Δ, Γ, Σ ⊢ AC⟦(xmem, e)⟧ =
                                ⊥              xmem ∉ Γ
     AC⟦fail⟧ = fail
        AC⟦ ∗ e⟧ = ∗ AC⟦e⟧        AC⟦fetch(e, N )⟧ = fetch(AC⟦e⟧, AC⟦N ⟧)
AC⟦branchto⟧ = branchto           AC⟦{x1, . . . , x𝑘 }⟧ = {AC⟦x1 ⟧, . . . , AC⟦x𝑘 ⟧}
       AC⟦∥e∥⟧ = ∥AC⟦e⟧∥                AC⟦e1 ∈e2 ⟧ = AC⟦e1 ⟧ ∈AC⟦e2 ⟧

                                       Alewife – Cassiopea Block-Lets Translation
    AC⟦let x : 𝜏base = e⟧ = let x : AC⟦𝜏base ⟧ = AC⟦e⟧

                                    Alewife – Cassiopea Declaration Translation
                                                    (
                                                     𝜖 x𝜏 ∈ Δ
                 Δ, Γ, Σ ⊢ AC⟦require type x𝜏 ⟧ =
                                                      ⊥ x𝜏 ∉ Δ
                                                    (
                                                     𝜖 x∈Γ
          Δ, Γ, Σ ⊢ AC⟦require value x : 𝜏base ⟧ =
                                                      ⊥ x∉Γ
                                                    (
                                                     𝜖 xfunc ∈ Γ
        Δ, Γ, Σ ⊢ AC⟦require func xfunc : 𝜏func ⟧ =
                                                      ⊥ xfunc ∉ Σ
                        AC⟦provide type x𝜏 = 𝜏⟧ = type x𝜏 = AC⟦𝜏⟧
               AC⟦provide value x : 𝜏base = e⟧ = let x : AC⟦𝜏base ⟧ = AC⟦e⟧
AC⟦provide func xfunc : x𝑖 : 𝜏base𝑖 → 𝜏base = e⟧ = def xfunc x𝑖 : AC⟦𝜏base𝑖 ⟧ → AC⟦𝜏base ⟧
                                                      = AC⟦e⟧
                         AC⟦region xmem : 𝜏mem ⟧ = letstate xmem : AC⟦𝜏mem ⟧
               AC⟦region xmem : 𝜏mem with x⟧ = letstate xmem : AC⟦𝜏mem ⟧ with x
                         AC⟦lower-with xmodule ⟧ = 𝜖
                            AC⟦reg-modify : x𝑖 ⟧ = reg-modify : AC⟦x𝑖 ⟧
                 AC⟦mem-modify : (xmemi , e𝑖 )⟧ = mem-modify : (AC⟦xmemi ⟧, AC⟦e𝑖 ⟧)

                                          Figure 24. Alewife – Cassiopea translation.

9    Conclusion                                                       Cassiopea that can be used used to describe the semantics
In this technical report, we described two domain specific            of many different processor ISAs at the assembly language
languages involved in the Aquarium kernel synthesis project.          level. Then, we presented a specification language named
First, we presented a machine modeling language named                 Alewife that allows stating abstract specifications for blocks
                                                                      of assembly code, such that these abstract specifications can
                                                                 22
be lowered to concrete specifications and used for synthesis
and verification against Cassiopea machine descriptions.
  We note that this is work in progress, and does not yet
present a final or complete view of either the Aquarium
system or the languages presented.




                                                               23
