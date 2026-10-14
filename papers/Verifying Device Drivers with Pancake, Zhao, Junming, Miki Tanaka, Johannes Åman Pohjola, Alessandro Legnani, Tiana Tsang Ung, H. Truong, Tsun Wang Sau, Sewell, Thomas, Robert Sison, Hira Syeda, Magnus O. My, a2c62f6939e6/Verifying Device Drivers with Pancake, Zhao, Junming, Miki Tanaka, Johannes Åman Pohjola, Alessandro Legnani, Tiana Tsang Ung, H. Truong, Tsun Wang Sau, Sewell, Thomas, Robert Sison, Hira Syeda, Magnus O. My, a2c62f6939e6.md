                                                                        Verifying Device Drivers with Pancake

                                                  Junming Zhao1 , Miki Tanaka1 , Johannes Åman Pohjola4,5,1 , Alessandro Legnani2,3 ,
                                             Tiana Tsang Ung1 , H. Truong1 , Tsun Wang Sau1 , Thomas Sewell1 , Rob Sison1 , Hira Syeda3,4 ,
                                                               Magnus Myreen4 , Michael Norrish6 , and Gernot Heiser1
                                                            1 UNSW Sydney, Australia ({junming.zhao,miki.tanaka,thomas.sewell,r.sison,gernot}@unsw.edu.au)
                                                                                     2 ETH Zürich, Switzerland (alegnani@ethz.ch)
                                                                           3 University of Melbourne, Australia (hira.syeda@unimelb.edu.au)
                                                                          4 Chalmers University of Technology, Sweden (myreen@chalmers.se)
arXiv:2501.08249v2 [cs.PL] 30 May 2025




                                                                          5 University of Gothenburg, Sweden (johannes.aman.pohjola@gu.se)
                                                                        6 Australian National University, Australia (Michael.Norrish@anu.edu.au)



                                         Abstract                                                              rectness from a driver-appropriate systems programming
                                                                                                               language down to the binary. Likewise, with no formal
                                         Device driver bugs are the leading cause of OS compro-                semantics or verified compiler, recent proposals like that
                                         mises, and their formal verification is therefore highly              of [Chen et al., 2024] to verify drivers written in Rust
                                         desirable. To the best of our knowledge, no realistic and             [Klabnik and Nichols, 2017] have no plan to close the
                                         performant driver has been verified for a non-trivial de-             semantic gap to the binary.
                                         vice. We propose Pancake, an imperative language for
                                                                                                                  Devices are commodities: new ones are created all the
                                         systems programming that features a well-defined and
                                                                                                               time. Therefore, any practicable driver verification must
                                         verification-friendly semantics. Leveraging the verified
                                                                                                               have a high degree of usability and automation. Drivers
                                         compiler backend of the CakeML functional language,
                                                                                                               are typically written in C, but verification of C code is
                                         we develop a compiler for Pancake that guarantees that
                                                                                                               made needlessly expensive by C’s complicated seman-
                                         the binary retains the semantics of the source code. Us-
                                                                                                               tics. In short, the situation demands a performant sys-
                                         ing automatic translation of Pancake to the Viper SMT
                                                                                                               tems language with support for usable automated verifi-
                                         front-end, we verify a performant driver for an Ethernet
                                                                                                               cation, and a means of ensuring the properties of verified
                                         NIC.
                                                                                                               drivers are preserved at the binary level.
                                                                                                                  In this paper, we present verification of a performant,
                                         1     Introduction                                                    real-world Ethernet driver that demonstrates a new ap-
                                                                                                               proach to efficient development of performant and veri-
                                         Device driver bugs are the leading cause of OS compro-                fied device drivers, achieved through the choice of driver
                                         mises, accounting for the majority of the 1,057 CVEs                  design and the use of Pancake, a new imperative pro-
                                         reported for Linux in the period 2018–22 [MITRE Cor-                  gramming language designed specifically for verification
                                         poration, 2023]—clearly they should be the #1 targets of              of low-level systems code. Namely, we verify the Pan-
                                         OS verification efforts.                                              cake version of an Ethernet driver for LionsOS [Heiser
                                            While there have been prior efforts to verify                      et al., 2025], which uses single-threaded, single-purpose
                                         drivers [Alkassar, 2009; Alkassar and Hillebrand, 2008;               (“modular”) driver designs as advocated by Ryzhyk et al.
                                         Chen et al., 2016; Duan, 2013; Duan and Regehr, 2010;                 [2009a, 2010] and outperforms Linux networking with
                                         Kim et al., 2008; Möre, 2021; Penninckx et al., 2012],                its standard C driver. The Pancake version of the driver
                                         to our knowledge none have yet succeeded on realistic,                we verify also enjoys the excellent performance owing
                                         non-trivial devices, nor have they presented any perfor-              to the simple design, with reasonable overhead coming
                                         mance analysis of the drivers verified.                               from porting to Pancake. It will be made available as a
                                            Most of these efforts used highly manual interactive               choice of network drivers for LionsOS soon.
                                         theorem proving, and sometimes required drivers to be                    Our new programming language Pancake has several
                                         written and analysed in assembly. On the other hand, at-              features that facilitate verification, the most significant
                                         tempts to apply more usable methods like model check-                 being:
                                         ing [Kim et al., 2008] and automated deductive verifica-
                                         tion [Penninckx et al., 2012] left significant gaps between            • a verified compiler from Pancake to binary that lever-
                                         the analysed model and the real code.                                    ages the final stages of the verified CakeML com-
                                            Of the above, only Chen et al. [2016] provided an end-                piler [Tan et al., 2019]. This guarantees that the se-
                                         to-end verification story that preserved the driver’s cor-               mantics of drivers and other systems code written in


                                                                                                           1
      Pancake, will be preserved at the binary level. Sec-          VST [Appel, 2011] may help, but to date this has not
      tion 2 discusses the overall structure of Pancake’s se-       resulted in verified real-world drivers.
      mantics and the compiler.                                        Many attempts to make better systems programming
                                                                    languages incorporate advanced language features to
    • an automated deductive verification front-end for             make safety properties hold by construction. For ex-
      Pancake that leverages the Viper verification frame-          ample, Cogent’s linear type discipline prevents mem-
      work [Müller et al., 2016b], a middle-end for various         ory leaks [Amani et al., 2016], Rust’s borrow checker
      SMT solver-based verification back-ends. This takes           enforces ownership and lifetimes [Klabnik and Nichols,
      the form of (1) an annotation syntax for Pancake, and         2017], and Cyclone incorporates garbage collection and
      (2) a transpiler from annotated Pancake to the Viper          ML-style polymorphism [Jim et al., 2002]. Such features
      intermediate language (IL), which we explain in Sec-          can eliminate whole classes of bugs, or at least reduce
      tion 3.                                                       bug density, but at the cost of complicating the language
Using this support, we produce the first verification of            semantics and implementation. Garbage collection intro-
a device driver for a non-trivial device, a driver for a            duces unpredictable delays that are highly undesirable in
popular 1 Gb/s Ethernet card for the seL4-based Lion-               low-level systems code. Yet these approaches still fall
sOS [Heiser et al., 2025]. This paper reports on the de-            short of ensuring full functional correctness, and it is un-
sign of the Pancake language, mainly on its compiler and            clear how helpful they are in achieving it.
semantics, and on the verification of the Pancake Ether-               Functional correctness proofs routinely rely on signif-
net driver using the Viper front-end for Pancake.                   icantly stronger properties than type systems typically
   Our experience shows that Pancake’s automated de-                guarantee. A stronger type system can give more proper-
ductive verification support is easy to use for those with          ties, but unless it is so powerful (and undecidable) as to
a systems development background, allowing the verifi-              be a full-featured proof calculus, functional correctness
cation of critical guarantees for practical drivers (Sec-           proofs will need more.
tion 4). The verification of our Ethernet driver took                  The information provided by a type system is only use-
around three person-months. The driver was ported from              ful in verification if the type system is sound, but most
C to Pancake and then verified by the one member of                 practical languages have unverified type systems, or type
the team who had no prior verification experience. We               systems with known soundness bugs. Type systems can
expect the process will be even faster once a library of            be verified [Naraschewski and Nipkow, 1999], but type
example verified drivers is available. This demonstrates            soundness proofs are delicate, and have subtle interac-
Pancake as a viable alternative to C for systems-level              tions with even minor language changes. Maintaining a
code, but one with the advantage of accessible end-to-              type soundness proof for a living language can signifi-
end verification support.                                           cantly bog down development.
   Our evaluation in Section 5 shows that the verified                 Moreover, the safety guarantees of a language only
Pancake driver performs very close to the C version.                hold if no backdoors are used. But low-level systems
   In Section 6 we discuss the trusted computing base               programs often need to break out of type-safe envi-
(TCB) and threats to the validity of Pancake’s auto-                ronments. For example, driver code must adhere to
mated deductive verification story and end-to-end se-               hardware-specified data locations, layouts and access
mantic preservation, and our plan to address them with              protocols. Hence driver code in safe languages must use
further verification.                                               significant amounts of unsafe code, effectively escapes
                                                                    to C [Astrauskas et al., 2020; Evans et al., 2020], which
                                                                    mostly eliminates the benefits of safe languages.
2     Pancake Language and Compiler
                                                                       Instead of adding more safety features to a language,
                                                                    which tends to complicate the semantics, we believe sim-
2.1      The Rationale
                                                                    ple proofs require a simple formal semantics. Of course,
While C is the de-facto standard systems language, C’s              the semantics must exist in the first place: despite years
semantics has a number of undesirable properties for ver-           of research [Jung et al., 2018; Kan et al., 2018; Wang
ification: a complicated memory model, underspecified               et al., 2018; Weiss et al., 2019], there is still no complete
evaluation order, and the need to prove the absence of              formal specification of Rust.
undefined behaviour at almost every step. While the                    We propose Pancake as the solution—a radically min-
seL4 verification demonstrated that these challenges can            imal language that nonetheless offers a sufficiently ex-
be overcome, the cost was high: $350/SLOC just for                  pressive interface for writing low-level systems pro-
verifying the C code [Klein et al., 2009], and this cost            grams, such as device drivers, alongside a number of
continues to impact kernel evolution. Using a verified              advantages for formal verification. Most importantly,
compiler [Leroy, 2009] with the verification toolchain              the language is completely specified by a straightforward

                                                                2
formal semantics that fits in a few hundred lines of HOL4          1    fun example(1 N, 1 shared_addr) {
code, with a simple memory model, no notion of unde-               2      /@ requires mem_access(N) @/
fined behaviour, and no ambiguities in evaluation order.           3      /@ ensures mem_access(N) @/
                                                                   4      /@ ensures N == old(N) @/
   Pancake is an unmanaged language with no static type            5      /@ ensures shared_addr == old(shared_addr) @/
system, at a level of abstraction between C and assembly.          6      var x = 0;
The data representation and memory models are kept as              7      var i = 0;
simple as possible. The only kinds of data are machine             8      while (true) {
                                                                   9        /@ invariant 0 <= i && i < N && x <= 42 @/
words, code pointers, and structs. Programs cannot in-            10        /@ invariant mem_access(N) @/
spect the stack, which simplifies semantics. All memory           11        var new_x = lds 1 @base + @biw * i;
is statically allocated; there is no equivalent of malloc         12        if (i + 1 == N) {break;}
                                                                  13        if (new_x > 42) {break;}
and free.
                                                                  14        x = new_x;
                                                                  15        i = i + 1;
2.1.1   Non-Goals                                                 16      }
                                                                  17      /@ assert x <= 42 @/
                                                                          !stw shared_addr, x;
Concurrency User-level drivers running as separate                18
                                                                  19      return 0;
processes do not need to be multi-threaded. Even for              20    }
Linux in-kernel drivers, Ryzhyk et al. [2009a, 2010]
                                                                  Listing 1: Pancake code snippet (concrete syntax) with
demonstrate that single-threaded drivers are feasible and
                                                                  annotations.
performant. They furthermore show that 19% of Linux
driver bugs are concurrency bugs, which are automat-
ically eliminated by such a design. Single-threaded
drivers are much easier to verify, and map well onto the                 exp    :=   Const word | Var string | Label string
                                                                                 |   Struct exp⋆ | Field num exp
modular design of microkernel-based OSes. This ap-                               |   Load shape exp | LoadByte exp
proach is routinely used for drivers on seL4, including in                       |   Op binop exp⋆ | Cmp cmp exp exp
LionsOS, which outperforms Linux on networking using                             |   Shift shift exp num | BaseAddr
                                                                                 |   BytesInWord
this design [Heiser et al., 2025].
   Therefore, Pancake has no concurrency primitives,                    prog    :=   Skip | Dec string exp prog
and our Ethernet driver has no internal concurrency. We                          |   Assign string exp | Store exp exp
will see that this does not meaningfully inhibit perfor-                         |   StoreByte exp exp | Seq prog prog
                                                                                 |   If exp prog prog | While exp prog
mance.                                                                           |   Break | Continue | Call ret exp exp⋆
                                                                                 |   Raise string exp | Return exp | Tick
                                                                                 |   ShMemStore opsize exp exp
Rust-level verification Pancake is not intended to re-                           |   ShMemLoad opsize string exp
place Rust; rather, it targets a different niche.                                |   DecCall string shape exp exp⋆ prog
   Rust’s safety features benefit developers by allowing                         |   ExtCall string exp exp exp exp
them to write more trustworthy code in the absence of                            |   Annot string string
verification, and Rust-based verification tools like Verus                     Figure 1: Abstract syntax of Pancake.
and Prusti have been very successful. However, Rust is
a complex language with no authoritative formal seman-
tics, putting any verification on soft foundations. It also       2.2     The Language and its Semantics
requires trusting a large, unverified compiler, which has
been found to yield memory-unsafe binaries from type-             Pancake looks and feels like a traditional imperative lan-
checked memory-safe Rust code [Speykious, 2024]. Fur-             guage (see Listing 1, ignore the /@...@/ annotations for
thermore, “unsafe” code is required for implementing              now). Figure 1 shows the current abstract syntax of Pan-
device drivers in Rust, and existing tools have limited           cake. The nuts and bolts should be familiar to any pro-
support for verification of unsafe Rust.                          grammer. Mutable variables, if, while—nothing fancy.
   This level of verification may be sufficient for certain       This is a deliberate design decision: we want Pancake to
situations, but we aim for stronger guarantees. We take           feel simple and familiar to systems programmers. In our
the compiler out of our TCB by fully verifying it, based          experience, this has been borne out in practice: systems
on Pancake’s precise semantics. A simpler language with           programmers familiar with C have found Pancake easy
formal semantics makes verification easier in both auto-          to learn.
mated and interactive settings. Overall, what we offer               Another key design concern is to give programmers
is a framework for producing secure low-level compo-              direct access to low-level details without the language
nents with a very small TCB, through Pancake’s formal             getting in their way. This is part of the motivation for
semantics and verified compiler.                                  Pancake’s perhaps most radical design decision: no static


                                                              3
                                                                                                                         CakeML passes
type system, and no distinction between different kinds                                                         Languages               Transformations
of data. In sloganeering terms, Pancake is a language                                                      CakeML syntax
                                                                                                                                     Parse concrete syntax

where everything is a machine word. For example, there                        Pancake passes                CakeML AST               Infer types, exit if fail
                                                                                                                                     Introduce globals vars,
                                                                                                                                     eliminate modules, etc.
is no distinction between pointers and integers: it’s all         Transformations      Languages                 FlatLang:
                                                                                                                language             Global dead code elim.
                                                                                                                   without
words.                                                                               Pancake syntax              high-level
                                                                                                                                     Turn pattern matches into
                                                                                                                                     if-then-else decision trees
                                                                  Parse concrete                                  features
                                                                                                                                     Switch to de Bruijn
   We can treat a word as an integer by adding to it, or          syntax                                                             indexed local variables
                                                                                      Pancake AST                                    Fuse function calls
treat it as a pointer by dereferencing it. The programmer         Flatten structs
                                                                                                                                     into multi-arg calls
                                                                                                                                     Track closure values &
                                                                                                              ClosLang:
                                                                                                                                     inline small funct
can do pointer arithmetic freely, which is of course un-                                CrepLang:
                                                                                                            last language
                                                                                                             with closures           Introduce C-style fast
                                                                                                            (has multi-arg           calls where possible
safe in general. We do not attempt to make it safe; rather,                             imperative             closures)
                                                                                                                                     Remove deadcode
                                                                                         language
                                                                                                                                     Annotate closure creations
we give it a simple and well-defined semantics that can                               without structs
                                                                                                                                     Perform closure conv.
                                                              Normalise program
support formal verification, without the need for compli-                                                             BVL:
                                                                                                                                     Inline small functions
                                                                                                                   functional        Fold constants /shrink
cated rules about (say) pointer provenance. In this way,      Call optimisation
                                                                                                                   language
                                                                                                                     without
                                                                                                                                     Lets
                                                                                                                                     Split over-sized functions

the historically minded reader may find the language de-                                 LoopLang:                  closures
                                                                                                                                     Compile global vars into a
                                                               Shrink cutsets and       expressions                                  dynamically resized array
sign closer to BCPL than C.                                    delete unused           occur only on                 BVI:            Optimise Let-expressions
                                                               assignments                RHS of                  one global         Make some functions
   With this in mind, the data representation and memory                                assignment
                                                                                                                   variable          tail-recursive

                                                                   Replace loops        statements
                                                                                                                                     Switch to imperative style
models of Pancake are kept as simple as possible. There            with tail calls                                DataLang:
                                                                                                                  imperative
                                                                                                                                     Reduce caller-saved vars
                                                                                                                                     Combine adjacent
are only three kinds of data: machine words, code point-                                                           language          memory allocations
                                                                                                                                     Remove data abstraction
ers, and structs (whose fields are machine words, code
pointers, or nested structs). Local variables are stack-
                                                                                                                                Simplify program
allocated, and we do not allow pointers into the stack.
                                                                                              WordLang:                         Select target instructions
Global data may be stored in a statically allocated global                                    imperative
                                                                                                                                Perform SSA-like renaming
memory region.                                                                              language with
                                                                                            machine words,                      Force two-reg code (if req.)
   The operational semantics of Pancake is specified us-                                     memory and
                                                                                                                                Remove deadcode
                                                                                            a GC primitive
ing functional big-step semantics [Owens et al., 2016].                                                                         Allocate register names
In this style, the core of the semantics is a logical func-                                                                     Concretise stack
tion that looks like an interpreter, but is not necessarily                                                                     Introduce (raw) calls past
                                                                                               StackLang:                       function preambles
executable. This simplifies formal proofs of compiler                                           imperative                      Implement GC primitive
correctness by making the semantics more amenable to                                            language
                                                                                                                                Turn stack accesses into
                                                                                              with array-like                   memory accesses
term rewriting. The semantics of a program is defined in                                         stack and
                                                                                               optional GC                      Rename registers to match
terms of how it communicates with the outside world;                                                                            arch registers/conventions
specifically, as a possibly infinite trace of I/O events,                                                                       Flatten code
                                                                                               LabLang:
each of which denotes either a foreign function call or                                      assembly lang.
                                                                                                                                Delete no-ops (Tick, Skip)
                                                                                                                                Encode program as
a shared memory load/store operation. The semantics is                                                                          concrete machine code
parameterised on a model of the outside world and the                                       ARMv6                                                   Silver ISA
kind of I/O events that can occur.
                                                                                            ARMv8        x86-64               MIPS-64         RISC-V


2.3    Verified Compiler
                                                                         Figure 2: CakeML and Pancake compiler stack.
The Pancake compiler is verified, and thus not in the
TCB. This sidesteps the need for fragile validation of
compiler output on a program-by-program basis [Sewell
et al., 2013].                                                     time.
   We reuse the lower parts of the verified CakeML com-               By contrast, Pancake is explicitly designed to be un-
piler [Kumar et al., 2014; Tan et al., 2019], which com-           managed and close to hardware, and to have no run-
piles CakeML programs to machine code for six archi-               time. Yet by integration into the CakeML ecosystem,
tectures. Figure 2 shows the CakeML compiler on the                it can reuse many of the existing correctness proofs
right and the Pancake compiler on the left. Arrows de-             for the CakeML compiler. The CakeML compiler pro-
note compilation passes, and yellow boxes denote inter-            vides backends for various target architectures [Tan et al.,
mediate representations.                                           2019] verified against detailed models of the target ISA
   CakeML itself is a high-level functional programming            semantics.
language, unsuited for low-level systems programming.                 The first few phases of the Pancake compiler go
For example, CakeML’s memory management is all han-                through two new intermediate languages (ILs). The first
dled by the language runtime, and memory allocation                compiler phase flattens structs and converts the programs
may trigger a stop-the-world garbage collection at any             to CrepLang, which is a stepping stone into LoopLang.


                                                              4
In LoopLang, we compute minimal live sets and divide                        this indirection in Pancake by adding native support for
loops (including their break and continue statements)                       shared memory.
into tail-recursive functions that better fit the CakeML IL
called WordLang. When the program under compilation                            A key challenge here is that the ISA models used by
is translated from LoopLang to WordLang, all loops are                      the compiler proofs [Tan et al., 2019] are inherently se-
replaced with fast tail-calls, as WordLang has no loops.                    quential, and >100 kSLOC of proofs inextricably rely on
Later, as in CakeML, these tail calls will be realised as                   this fact. While previous work has integrated driver mod-
fast simple jumps in the generated machine code.                            els for specific devices directly into an ARM ISA model
   Once we have entered WordLang, we use the CakeML                         with an interleaving semantics [Alkassar et al., 2007],
compiler’s compilation phases, including its phases for                     this approach would require us to abandon much of the
instruction selection, register allocation, concretisation                  existing proof base, and would not provide the modular-
of the stack, and, at the end, encoding of the entire pro-                  ity needed to target multiple ISAs and devices. We there-
gram into concrete machine code.                                            fore parameterise the language semantics on a model for
                                                                            shared memory, which supports proof reuse and provides
   The compiler correctness proofs allow safety and live-
                                                                            flexibility for incorporating arbitrary devices.
ness properties of Pancake programs to carry over to the
machine code that runs them.                                                   We add shared memory semantics to all compiler
   Our Pancake compiler has a special feature which pro-                    ILs from Pancake downwards, and verify the full
duces not only the output machine code, but also predicts                   compilation chain. We give load/store operations on
the concrete maximum stack size the program can use, as                     shared memory regions a special syntax (ShMemLoad and
long as the input program has recursive calls only in tail                  ShMemStore in Figure 1). In the semantics, these opera-
position. We have proved that this bound suffices for run-                  tions are considered observable events. At the end of the
ning the Pancake program without running out of stack                       compiler pipeline they are converted to ordinary loads
space. This allows Pancake to guarantee the absence of                      and stores.
premature termination arising from stack overflows.
   The functional correctness proof of the Pancake com-                        Another challenge arising from the CakeML lineage is
piler follows the style of the CakeML proofs. The top-                      the issue of function entry points. The CakeML compiler
level correctness theorem states that the source Pan-                       expects code to only ever be called via the main function,
cake program and the compiler-generated machine code                        and to exit entirely when main returns. Moreover, main is
exhibit exactly the same observable I/O events, if the                      preceded by lengthy initialisation, and does not support
compiler-generated code is run with enough stack space.                     parameters.
   The compiler and the associated proofs are open                             Device drivers in LionsOS must support several func-
source.1                                                                    tions as entry points, and for these to support re-
                                                                            entry. Thus, using CakeML’s execution flow demands
                                                                            workarounds, such as branching in the main function
2.4     Challenges with Device Drivers
                                                                            based on data indirectly passed through memory, and
Using CakeML as Pancake’s backend compiler presents                         manually editing the compiler output to return to the
a number of issues when compiling device driver code.                       caller. Even then, a substantial performance penalty
First, CakeML assumes exclusive ownership of its stati-                     arises from repeated re-initialisation. This is clearly nei-
cally allocated memory region, and that this memory is                      ther scalable nor performant.
not observable by the environment. These assumptions
                                                                               We address this by implementing support for multiple
are not valid for memory-mapped device registers, which
                                                                            entry points. A function declaration can be tagged with
are special memory locations used for interfacing with
                                                                            the export keyword, which extends the generated com-
device hardware, nor do they hold when devices directly
                                                                            piler output to expose the function to the calling conven-
write to memory (DMA). They also do not fit the Lion-
                                                                            tions of the target platform, and to restore the state ini-
sOS model, which heavily depends on shared-memory
                                                                            tialised by the main function when the exported function
communication between OS components [Heiser et al.,
                                                                            is called. This circumvents the re-initialisation, and han-
2025].
                                                                            dles argument passing and returning to the caller with-
   With this limitation, any interaction with the device                    out programmer intervention. It enables calling into the
from CakeML would have to be mediated by FFI calls to                       Pancake driver as if it were written in C. The top-level
C, adding a layer of indirection to the TCB. We eliminate                   compiler correctness proof currently accounts only for
   1 http://code.cakeml.org for source, or http://cakeml.org for            the main entry point in that some of the assumptions are
pre-packaged versions. Note that Pancake is fully integrated into the       too specific to initialisation, which need to be relaxed to
CakeML compiler, rather than a stand-alone release.                         account for the re-entry points.


                                                                        5
2.5    Verification Approaches                                      cerning our encoding of Pancake’s machine word type,
                                                                    and our encoding of (shared and unshared) memory in
For the purpose of using Pancake to produce high-                   Viper. Our objective an encoding that maximises the
assurance device drivers, the verified compiler (Sec-               performance of the resulting queries to Viper’s backend,
tion 2.3) is only half of the story: we must also be sure           while still being sound—that is, it should never produce
that the Pancake code implements the device driver cor-             a Viper query that is verifiable as true, when the state-
rectly (incorrect source + verified compiler = incorrect            ment about Pancake code that it is supposed to encode is
machine code).                                                      false.
   The gold-standard (but potentially expensive) way                   We aim for most produced queries to take seconds or
to verify source code is to use interactive theorem-                minutes to verify, to make verification usable as an ac-
proving (ITP), as done by (for example) the seL4 [Klein             tive part of a driver developer’s workflow. Our overrid-
et al., 2014] and CertiKOS [Gu et al., 2016] kernels,               ing concern is to prevent the transpiler from producing
and the CompCert [Leroy, 2009], and CakeML [Kumar                   queries that cause the Viper SMT-based back-end either
et al., 2014] (and thus Pancake) compilers. As Pancake              to diverge or to take a prohibitively long time to be used
is an imperative language, it would be natural to use an            for continuous integration testing. We leave proving the
ITP-based implementation of Hoare logic. We describe                soundness of the encoding to future transpiler verifica-
preliminary and future work on ITP-based approaches to              tion work (see Section 6).
source verification in Section 6.2.
   For productivity, given the commodity nature of de-
vices, we use automated deductive verification, rather              3.1   Machine-Word Encoding
than an ITP. Using Viper [Müller et al., 2016b] (and
                                                                    For the best query performance, we encode Pancake’s
its realisation of Hoare logic) increases the size of the
                                                                    machine-size word variables as integers in Viper.
trusted computing base (see Section 6.1), but can be ex-
                                                                       As a language whose only primitive type is machine-
pected to be less expensive in terms of developer time
                                                                    size words, Pancake’s word variables have bitvector se-
and expertise. Our case study bears this out.
                                                                    mantics and overflows are well-defined behaviour, i.e.,
   To support this, Pancake syntax includes Viper an-
                                                                    the variable is wrapped modulo the word size.
notations (visible in Listing 1). They resemble com-
                                                                       To preserve this semantics when encoding these as in-
ments in the source code, and can appear at the top level
                                                                    tegers in Viper, which are signed and unbounded, one
and within function bodies. Top-level annotations are
                                                                    option is to treat arithmetic operations as modulo the
used, for instance, to specify function contracts, while
                                                                    word size. However, this approach significantly slows
in-function annotations can be used for loop invariants.
                                                                    verification due to the mixing of arithmetic that is lin-
The Pancake compiler ignores annotations, but the Viper
                                                                    ear (such as addition, subtraction etc.) versus non-linear
transpiler (Section 3) preserves the annotations so that
                                                                    (such as modulo and bitvector operations) with respect to
verification can be carried out.
                                                                    Viper’s unbounded signed integer space. Poor query per-
                                                                    formance due to mixing of different theories that require
3     A Viper Front-end for Pancake                                 handling by different solver strategies is a well-known
                                                                    hazard for SMT solvers [Jovanovic and Barrett, 2013].
Our verifier transpiles annotated Pancake code into the                Instead, since overflows are rarely intended behaviour,
Viper IL, then verifies the generated Viper code using              we adopt Prusti’s approach, treating overflows as verifi-
Viper’s symbolic execution backend Silicon [Schwer-                 cation failures. We do this by checking the bounds of
hoff, 2016]. This approach is comparable to that of Viper           every variable after having unrolled all arithmetic oper-
front-ends such as Gobra [Wolf et al., 2021] for Go and             ations into three-address code. We make this decision
Prusti [Astrauskas et al., 2022] for Rust.                          to ensure soundness at the mild expense of disallowing
   Our transpiler first uses a diagnostic feature of the Pan-       intended machine word overflows. These were used in
cake compiler to extract the abstract syntax tree (AST)             the original C implementation of the driver but could be
of the input program, which includes Pancake-level (1)              avoided with a one line change in the Pancake version.
annotations of the kind shown in Listing 1 as well as                  Another concern is that bitvector operations are also
(2) hooks into a device model that we will describe in              non-linear with respect to Viper integers, causing similar
Section 3.3. It then translates that AST into our chosen            performance concerns. Observing that almost all bitvec-
encodings for Pancake’s variables, values, memory lo-               tor operations in our driver occur as part of bit masking,
cations, and annotated logical assertions over these, as            shifting etc., for accesses to device memory as part of
expressed in Viper IL code.                                         a well defined device interface, we instead abstract this
   The rest of this section documents and explains the              device interface, which we cover in Section 3.3. Addi-
most interesting of these encoding decisions, those con-            tionally we precompute constant expressions and apply


                                                                6
heuristics to rewrite common bitvector operations, e.g.            1    method store_rx_free(heap: IArray,
x&255 is rewritten as x%256. Although the rewritten op-            2        device: Ref, addr: Int, value: Int)
erations still use non-linear arithmetic, performance is           3
                                                                   4    /@ shared rw u64 rx_free[lower..upper] @/
improved compared to bitvector operations. This elim-
inates the vast majority of bitvector operations, with the        Listing 2: Method signature of shared memory store in
remaining few in our Ethernet driver turning out to be            device model and the corresponding top-level annotation
reasonably performant as Viper queries.                           in Pancake, specifying that shared memory accesses to
                                                                  the address range lower..upper should transpile to a
                                                                  Viper invocation of store_rx_free or load_rx_free.
3.2    Local Memory Encoding
As mentioned in Section 2, Pancake disallows pointers
to stack variables, which simplifies modelling them in            and memory regions. They also specify requires and
Viper: we do not have have to manage any kind of access           ensures clauses for the hardware interfaces, as asser-
permission or to check for references to invalid memory.          tions in terms of a global device state and the non-device
   For all other memory, the memory model of Pancake              memory. This is a good fit with how the Pancake seman-
poses unique challenges due to its assembly-like nature,          tics models shared memory operations (Section 2) as ob-
such as the lack of first-order support for arrays and re-        servable events, whose interpretation is parameterised on
liance on pointer arithmetic for memory operations. Due           a model of the environment—a semantics which is also
to the lack of information about what different memory            preserved by the Pancake compiler.
regions represent—be they arrays, structs or other data              For interactions via shared memory with other OS
structures—we must adopt the most naive modelling ap-             components, we make it the responsibility of the driver
proach: with the exception of shared and device memory            developer to specify a neighbouring component model
(described in the next section), we encode memory as an           similarly in a separate Viper file. The developer should
array of words. This approach results in non-idiomatic            use this to capture the guarantees the driver should meet
Viper code but captures Pancake’s native word-size treat-         for the Viper verification to enforce, as well as any as-
ment of memory operations accurately.                             sumptions about the behaviour of those neighbouring
   The various memory regions a function needs access             components with respect to the shared memory.
to, and with which permission, are added via annotations             We then provide a syntax for top-level Pancake an-
encoded as an iterated separating conjunction [Müller             notations that allow the driver developer to specify the
et al., 2016a], which can be verified efficiently in Viper.       correct method(s) to use for a shared memory operation,
                                                                  according to the address range the driver interacts with,
                                                                  allowing the transpiler to infer automatically which Viper
3.3    Shared and Device Memory Encoding
                                                                  method the produced Viper model should invoke in place
As mentioned in Section 2.4, Pancake includes dedicated           of the shared memory interaction (see Listing 2).
load/store operations for shared memory regions, whose               This way, the driver developer is not required to spec-
behaviour in a sense resembles volatile variables in C,           ify the model of the device or neighbouring component
whose accesses cannot be reordered or optimized away              before they implement their driver in Pancake. Further-
by the compiler. Thus, driver code uses these primitives          more, they do not have to modify their Pancake driver’s
for accesses to device memory, as well as accesses to             shared memory accesses after specifying these models—
memory shared between it and other OS components.                 they instead add extra annotations to specify which Viper
Given this sharing, we cannot encode shared memory in             methods the transpiler should produce in place of load-
Viper simply as an array of words, because we cannot              s/stores to given shared memory addresses. This ap-
rely on its contents not to change between accesses.              proach ensures the separation of driver implementation
   Device register accesses, needed for implementing              and device specification, whilst also improving verifica-
drivers, make extensive use of bitwise operations to ac-          tion speeds.
cess the correct bits. As stated before, these operations
result in bad performance so we seek to avoid them
                                                                  4     Verified Ethernet Driver
where possible.
   To limit these, we model accesses to shared mem-
                                                                  4.1     Overview
ory as separate Viper method calls, which the driver de-
veloper should specify in an external Viper file repre-           We formally verify a single-core i.MX Ethernet driver
senting the device model for the driver’s target device.          for LionsOS [Heiser et al., 2025]. LionsOS uses a sim-
These methods define valid operations for specific ad-            ple OS-side interface for device drivers with zero-copy
dress ranges corresponding to particular device registers         shared-memory communication for network data. The


                                                              7
                                                                os.vpr
                                                             device.vpr
                                                                                              The device state consists of RX (receive) and TX
                                                                                           (transmit) hardware descriptor rings, with each ring de-
 driver.                 driver.                driver.vpr
                                                                           yes/no/         composed into three integer sequences representing data
                                                              Viper       try harder
             Manual                Transpiler                                              addresses, lengths, and bitfields. These integers repre-
           annotations
                                                                                           sent machine words and are converted to bitvectors when
                                                                                           bit-level operations are required. As discussed above, by
             Figure 3: Driver verification workflow.
                                                                                           isolating the descriptor components, such a decomposi-
                                                                                           tion simplifies verification and reduces SMT solver com-
interface employs lock-free, bounded, single-producer,                                     plexity, particularly when using non-linear arithmetic
single-consumer (SPSC) queues that contain meta data                                       and bitvector operations. Each shared memory operation
buffers for data addresses and lengths, as well as con-                                    corresponds to a Viper method in the device model, with
trol information for signaling requests. The driver syn-                                   memory loads returning non-deterministic values within
chronises with the rest of the OS via semaphores (imple-                                   valid ranges, and memory stores satisfying both address
mented as seL4 Notifications).                                                             and value requirements.
   The target driver, implemented in Pancake, controls                                        We model the non-determinism of the values the driver
the MAC-NET 1 Gb/s Ethernet core common to NXP                                             could possibly obtain from the device by underspecify-
i.MX 8M Mini, Dual, QuadLite and Quad Applications                                         ing its interface methods, forcing the verification of the
Processors present in various Arm-based NXP system-                                        calling context of the method (i.e. the Pancake code that
on-chips (SoC), operating as a network interface card                                      invoked the shared memory operation) to account for a
(NIC). The NIC uses DMA descriptor rings for passing                                       wide range of possible values constrained only by their
the addresses of data packets. This driver will be made                                    ensures clauses. For example, load_EIR in Listing 3
available for LionsOS as a choice of network drivers                                       ensures that the return value is a valid unsigned 32-bit
alongside the C version. The driver incorporates formal                                    word value, as captured by bounded32(retval). Verifi-
specifications through annotations using Hoare logic and                                   cation must subsequently succeed for any value returned
the Viper verification framework.                                                          by that interface that satisfies the ensures, i.e., any un-
                                                                                           signed 32-bit word value.
                     Component                           Line Count
                     C Driver                                   351                        What is verified This verification work establishes the
                  Pancake Driver                                411                        following four classes of critical guarantees:
               Pancake annotations                              558
                                                                                           1. Compliance with NIC device interfaces (Section 4.2):
               Viper Device model                               391
                                                                                              we verify that:
            Viper OS interfacing model                          298
                                                                                              • device memory accesses are within the right ad-
Table 1: Lines of code comparisons between the Ethernet                                         dress ranges; and
driver in Pancake implementation and C implementation,                                        • values written to the device obey the device’s re-
and the lines of code of our verification artifacts.                                            quirements.

Verification workflow Figure 3 shows the resulting                                         2. Compliance with neighbouring OS component inter-
verification workflow. The programmer annotates the                                           faces (Section 4.3): we verify that the driver adheres
Pancake source of the driver and processes the resulting                                      to the network queue signalling protocols, specifi-
source with the transpiler, which produces the Viper in-                                      cally:
put. The programmer also supplies Viper specifications                                        • for consuming meta data buffers from network
of the device interface as well as the interface between                                        queues, the driver requests the OS wake-up signals
the driver and the rest of LionsOS. These are then pro-                                         OS if hardware rings have vacancy,
cessed by Viper, which returns a result (proved or falsi-
fied) or times out. Table 1 shows the total size of our                                       • for providing meta data buffers to the OS, the driver
verification artifacts.                                                                         notifies the OS’s semaphores if and only if (i) a sig-
                                                                                                nal was explicitly requested by the OS and (ii) the
                                                                                                queue state has been changed by the driver; and
Device model We model the hardware NIC device and                                             • the driver clears signal requests after notifying the
its non-deterministic state in Viper specifications. The                                        OS (to prevent double signalling)
model is then connected to Pancake driver source code
after transpilation, using the top-level Pancake annota-                                   3. Guaranteed data integrity across transfers (Sec-
tions as described in Section 3.3.                                                            tion 4.4): we verify that there is no data loss in the


                                                                                       8
     driver by enforcing integrity check on packet meta            1. Method-specific requirements, such as the store_EIR
     data (addresses and lengths) on all pathways of meta             method’s requires of both an address and a value
     data transfers in the driver (note that, with Lion-              requirement—namely, that the address is the EIR’s and
     sOS [Heiser et al., 2025], the driver never needs to             that the driver only ever writes a particular IRQ_MASK
     access or map the packet data itself, and hence never            constant to it;
     violates the integrity or confidentiality of the packet
     data); and                                                    2. Device-wide invariants—in this example, captured by
                                                                      valid_device in store_EIR’s third requires clause.
4. Memory safety through region isolation and restricted              For our NIC, valid_device asserts that the state of
   access controls (Section 4.5): we verify that access               the hardware descriptors remains valid: the bitfields
   to TX-related states and RX-related states are cor-                are cleared and set properly according to the device’s
   rectly restricted to the parts of the driver responsible           documented specifications, data pointers are 32-bit
   for transmitting and receiving, respectively.                      width and byte-aligned, and data lengths are within
                                                                      16-bit bounds.
4.2     Device Interface Compliance
                                                                   The device state of our NIC device, as modelled by
First, we enforce that the driver only accesses the parts          device and asserted valid by valid_device(device),
of device memory that comprise the NIC’s hardware in-              comprises the hardware descriptor rings, with each ring
terfaces for packet receipt and transmission— namely,              decomposed into three integer sequences representing
the device’s RX (receive) and TX (transmit) hardware               data addresses, lengths, and bitfields. These integers
descriptor ring regions and other essential registers. To          represent machine words and are converted by Viper to
enforce this, recall from Section 3.3 that our transpiler          bitvectors when bit-level operations are required. Our
supports and looks for top-level Pancake annotations that          decomposition of these descriptor components into na-
specify which addresses correspond to valid device in-             tive Viper integers thus simplifies verification and re-
terfaces, as illustrated in Listing 2. Our verifier will re-       duces SMT solver complexity, particularly when using
ject any Pancake drivers that attempt to invoke a shared           non-linear arithmetic and bitvector operations.
memory load or store operation on an address that is not              Note that, while the presence of valid_device in the
covered by any such annotations.                                   requires clauses of device interface methods requires
                                                                   the driver not to violate the validity of the device state, its
 1    method store_EIR(device: Ref, addr: Int,                     presence also in the ensures clauses of all device meth-
 2        value: Int)                                              ods specifies that we can assume the device itself will
 3      requires addr == (REG_BASE + EIR_OFFSET)
                                                                   maintain that same validity invariant through all driver-
 4      requires value == IRQ_MASK
 5      requires valid_device(device)                              device interactions.
 6      ensures valid_device(device)
 7
 8    method load_EIR(device: Ref, addr: Int)                      4.3    OS Communication Protocols
 9      returns (retval: Int)
10      requires addr == (REG_BASE + EIR_OFFSET)                   Using much the same approach just described in the pre-
11      requires valid_device(device)                              vious section for specifying valid device interactions, we
12      ensures bounded32(retval)                                  constrain the driver’s access to shared memory regions
13      ensures valid_device(device)
                                                                   for network SPSC queues through annotations when in-
14
15    /@ shared rw u32 EIR[REG_BASE + EIR_OFFSET] @/               terfacing with LionsOS components. We also model
                                                                   the shared SPSC queues non-deterministically to verify
Listing 3: Examples of device register store/load inter-
                                                                   the driver maintains protocol compliance—assuming the
faces in the device model as specified by Viper methods
                                                                   neighbouring OS component maintains it too—without
using requires and ensures, and corresponding top-
                                                                   assuming specific state values.
level Pancake annotation.

                                                                   4.4    Data Integrity
   Second, we verify that, whenever the driver interacts
with these device interfaces, it does so in the required           To ensure reliable data transfer between the OS and the
way not to put the device into a bad state, as specified by        device during the translation between hardware descrip-
its documentation and captured by our device model. To             tor and SPSC formats, we verify that the driver maintains
enforce this, we specify two kinds of requires clauses             data integrity by tracking packet addresses and lengths.
for device interface methods, as illustrated in Listing 3             For example, we check that the given data address
for a representative pair of examples, the store and load          and data length are stored properly after updating the TX
methods for EIR, a particular device register:                     hardware descriptor ring, as shown in Listing 4.


                                                               9
                                                                                Received Throughput (Mb/s)




                                                                                                                                                            Driver CPU Utilisation (%)
 1    buffer = net_dequeue(os_tx_avail);
                                                                                                             1000                                     100
 2    update_tx_hw_ring(hw_tail, buffer);                                                                     900
                                                                                                                           Pancake Xput               90
                                                                                                                                 C Xput
 3    /@ assert(device.hw_ring_tx[hw_tail].data_addr                                                          800    Pancake Driver CPU
                                                                                                                                                      80
 4          == buffer.data_addr) @/                                                                           700          C Driver CPU               70
                                                                                                              600                                     60
      /@ assert(device.hw_ring_tx[hw_tail].data_len
 5
                                                                                                              500                                     50
            == buffer.data_len) @/                                                                                                                    40
 6
                                                                                                              400
                                                                                                              300                                     30
Listing 4: Data integrity verification example in anno-                                                       200                                     20
tated Pancake. For brevity, unwrapping of predicates re-                                                      100                                     10
ferred to by the assertions is omitted.                                                                         0                                     0




                                                                                                                   0
                                                                                                                 100
                                                                                                                 200
                                                                                                                 300
                                                                                                                 400
                                                                                                                 500
                                                                                                                 600
                                                                                                                 700
                                                                                                                 800
                                                                                                                 900
                                                                                                                1000
                                                                                                                        Requested Throughput (Mb/s)
   We establish this integrity check on all pathways of
data transfers in the driver. We also verify data trans-                        Figure 4: Performance of Ethernet Driver written in
fer completeness by ensuring that within the driver, the                        Pancake vs C, in terms of achieved throughput (Xput)
number of SPSC queue operations align with the number                           and Driver CPU utilisation.
of hardware descriptor ring state changes, so there is no
data loss in the driver.




                                                                                                                                                            Total CPU Utilisation (%)
                                                                                                                                                      100
                                                                                                             1400   Pancake RTT                       90
                                                                                                             1200         C RTT
                                                                                                                                                      80


                                                                                Mean RTT (µs)
                                                                                                                    Pancake CPU
4.5       Memory Access Control                                                                              1000         C CPU                       70
                                                                                                              800                                     60
In addition to the memory access constraints described                                                                                                50
                                                                                                              600                                     40
in Sections 4.2 and 4.3, we also verify that only the parts                                                   400                                     30
of the driver responsible for packet transmission access                                                      200                                     20
                                                                                                                                                      10
any TX-related descriptor rings and SPSC queue state,                                                           0                                     0
                                                                                                                   0
                                                                                                                 100
                                                                                                                 200
                                                                                                                 300
                                                                                                                 400
                                                                                                                 500
                                                                                                                 600
                                                                                                                 700
                                                                                                                 800
                                                                                                                 900
                                                                                                                1000
and likewise that only its packet receipt paths access RX-
related state.
                                                                                                                        Requested Throughput (Mb/s)
   We enforce this using Viper’s native permissions to
specify access controls, in this way providing formal ver-
ification of memory safety and region isolation. In ef-                         Figure 5: Performance of Ethernet Driver written in
fect, our driver verification applies a separation logic-like                   Pancake vs C, in terms of average round trip time (RTT)
principle by partitioning the driver’s global memory into                       with standard deviation and total CPU utilisation.
RX and TX regions (which reflects their use in LionsOS
[Heiser et al., 2025]).                                                         NIC and echoes them back. We use an external load gen-
                                                                                erator that sends an adjustable load (requested through-
5      Performance Evaluation                                                   put) to the target system, and measures the amount of
                                                                                data received back (received throughput) as well as the
We now examine how our verified Pancake driver com-                             latency. On the evaluation system we also measure CPU
pares to the original C implementation.                                         load.
   Pancake driver compilation time is a matter of sec-                             Figure 4 shows the result. Like the C driver, the Pan-
onds, and the verification of the driver in full takes                          cake driver has no problems handling the requested load:
around 20 minutes on a typical laptop. When verified                            the received throughput equals the requested. The Pan-
separately, the device model takes 10 minutes and the                           cake version of the driver uses slightly more CPU time
driver’s functions each take around 1 minute.                                   to handle the load than the C version, the difference is
   Our evaluation platform is an AVnet MaaXBoard with                           about 10%. Viewed in the context of LionsOS using less
an NXP i.MX8MQ SoC, having four Arm Cortex A53                                  than half the CPU of Linux to handle a particular net-
cores capable of a maximum of 1.5 GHz. We run our                               work load, the slightly increased overhead of the Pancake
measurements at a fixed clock rate of 1 GHz to avoid the                        driver is in the noise.
need for thermal management.2 The board has 2 GiB of                               Figure 5 puts this slight increase into context, by look-
RAM and the on-chip 1 Gb/s NIC specified earlier (in                            ing at latency (RTT) and the overall CPU use of the
Section 4).                                                                     whole system. The difference in CPU usage of the
   The evaluation system runs a networking client on Li-                        drivers becomes unnoticeable. Similarly, the differences
onsOS. The client simply receives data packets from the                         in latency is well within the variance of the results. This
     2 Note that running at a low clock rate will magnify software over-        is in the context of LionsOS using less than half the
heads, and as such presents a pessimistic performance.                          CPU of Linux to handle a particular network load [Heiser


                                                                           10
et al., 2025]. We can summarise that the performance                 ensures specifications we impose on return from device
cost of the verified driver is in the noise.                         interfaces in our device model. This includes trusting
                                                                     that the device’s initialisation process establishes a valid
                                                                     initial state. Verification of the device hardware and ini-
6     Discussion                                                     tialisation process would be needed to gain further assur-
While our main results are formally verified, no proof               ance of this.
about a real-world artifact is ever fully complete and                  Meanwhile, we assume that the neighbouring OS
self-contained: there will always be a trusted computing             components comply with the SPSC queue protocols, as
base (TCB). The TCB, in brief, is everything that we rely            mentioned in Section 4.3, and that the driver acts as the
on for the correct operation of our system, but which is             sole consumer or producer per queue. We will need to
currently outside the scope of the formal verification ef-           leverage Viper’s access permission system to establish
fort. For a formal verification result, the TCB is the main          more sophisticated guarantees about concurrent accesses
threat to validity.                                                  and thread safety properties.
   In Section 6.1, we discuss our TCB. Section 6.2 dis-                 Finally, we trust the operating system kernel and its
cusses alternative verification approaches we are pursu-             user-level support libraries not to crash or malfunction.
ing that would reduce the TCB further. Finally, Sec-                 LionsOS runs on the seL4 OS microkernel, which is ver-
tion 6.3 discusses potential usability improvements to the           ified not to crash [Klein et al., 2014], and relies on the
verification front-end.                                              seL4 Microkit support library, whose main server loop
                                                                     has been verified not to exhibit undefined behaviour [Pa-
                                                                     turel et al., 2023]. However, functional properties of in-
6.1    Threats to Validity                                           dividual seL4 system calls relied on by Microkit have not
For the Pancake compiler correctness proofs, we trust:               yet been verified.
that the HOL4 theorem prover is a sound implementation
of higher order logic; that the official specification of the        6.2    Future Verification Efforts
Arm ISA is correctly implemented by the CPU [Kanabar
et al., 2022]; and that an unverified linker for connect-            We are continuing to implement more drivers for Lion-
ing the Pancake binary to external code such as LionsOS              sOS in Pancake and to apply the verification method pre-
library routines is correct. With these as the TCB, the              sented in this paper to those drivers firstly to produce
Pancake compiler is verified, just like the CakeML com-              more verified drivers but also to assess and improve the
pilation passes that it leverages, to preserve the semantics         verification process. We also have various verification
of the main function of the source program.                          related future projects based on Pancake, including those
   Our verification results presented here establish cer-            we discuss below.
tain observable properties of the driver including its be-
haviour after reentry. Putting these together, the verified          Transpiler verification Proving the formal correct-
compiler guarantees that the binary obtained by compil-              ness of the transpiler implementation, as mentioned
ing this driver should preserve the verified observable              in Section 3, is in progress. This means that the tran-
properties, although we are not (yet) providing links be-            spiler is currently included as part of the TCB, as dis-
tween the two results formally, in the sense that there is           cussed in Section 6.1. What we aim to prove here is to
no theorem yet to state this on a single, unified formal-            establish the validity at the level of the Pancake input of
ism. Future work will strengthen this by verifying the               the statements proved on at the level of the transpiled
transpiler as well as extending the compiler proofs to ac-           Viper IL code. Such a proof would complete our end-to-
count for reentry points.                                            end verification story, by allowing us to soundly infer the
   Moreover, while we plan to verify our transpiler from             correctness of our initial Pancake code from a successful
annotated Pancake to Viper (Section 6.2), this is not done           verification run of the corresponding Viper IL code. This
yet. Until then, a mistake in the transpiler could pro-              still assumes the correct operation of the Viper toolchain
duce a Viper query that the underlying SMT-based back-               which our verification step relies on. Efforts exist to val-
end can prove true, even if the property as specified at             idate parts of this toolchain [Gössi, 2016; Parthasarathy
the Pancake program point via Viper annotations is false.            et al., 2024].
Beyond this, we also trust the Viper verification infras-               We will do this proof using the theorem prover HOL4,
tructure and SMT solvers called by its backends to dis-              which Pancake compiler is implemented. Though the
charge the Hoare logic queries specified using its input             current Rust implementation of the transpiler contains
language soundly, i.e., only when true.                              7 kLOC, a significant portion of this code consists of
   Like any device driver, we trust the device not to                workarounds for extracting the underlying abstract syn-
malfunction—that is, to guarantee that it meets the                  tax from an unparsed Pancake program without interfac-

                                                                11
ing directly with the existing Pancake parser. We can re-           6.3    Transpiler usability improvements
move these workarounds entirely by connecting the tran-
spilation to the Pancake parser and handling its formal             The current workflow involves transpiling Pancake into
syntax and the semantics directly, which will simplify              Viper for verification. Whilst the transpiler allows for
the implementation considerably, making the verification            direct verification, error messages are tied to the gener-
easier.                                                             ated Viper code and are not reflected back to the Pan-
                                                                    cake code, complicating debugging. Additionally, while
                                                                    many annotations are automatically inferred, some re-
Interactive theorem proving for Pancake programs                    quire manual specification, increasing the effort required
The formal semantics for Pancake and the compiler for               from the programmer.
it are developed in the HOL4 interactive theorem prover.               In addition to the command line tool we have built
It would be natural to verify a Pancake program entirely            an initial development environment for verified Pancake
in HOL4. We have performed a number of small exper-                 based on Microsoft’s VS Code framework. As of yet
iments in this style, verifying simple example programs             this lacks some features like support for the separate
such as a loop that sums the elements of an array. These            Viper device model. The transpiler supports verifying
experiments are an important validation of the Pancake              functions individually. This could be integrated into
formal semantics. The compiler correctness proof estab-             the development environment to allow for efficient re-
lishes that the formal semantics captures the behaviour             verification of only modified functions.
of the binary, but that is only useful if it is possible to            Despite these shortcomings, we expect that these tools
reason at the level of the semantics.                               can be combined and improved to form a cohesive and
   We have done some of these proofs by directly manip-             usable toolchain for writing and verifying device drivers.
ulating the Pancake semantics in HOL4. We have also
constructed a Hoare-style precondition-postcondition
logic for Pancake programs, which is a standard ap-                 7     Related Work
proach to verification of programs in an imperative lan-
guage such as Pancake. This gives us a comparison point             Among various verification efforts in the OS context, a
to our Viper-based approach. Our Hoare logic is far more            number of prior works have investigated verification of
user-friendly than directly working with the semantics,             device drivers at various programming language levels.
but far less user-friendly than using the transpiler. One           Within this space, researchers have employed different
advantage of the Hoare logic is that its correctness results        verification approaches like model checking [Kim et al.,
compose directly with the compiler correctness theorem              2008] and interactive theorem proving [Möre, 2021].
in HOL4, producing a binary correctness theorem with a              Among these efforts, [Penninckx et al., 2012] developed
minimal TCB, useful for small safety-critical programs              their verification using VeriFast [Jacobs et al., 2010], a
whose correctness must be certified.                                deductive verification approach similar to ours. They
   Another strength of HOL4 is its general logic, which             also notably extended their analysis to include concur-
allows us to phrase and prove properties that we could              rency properties beyond our current scope. However, a
not easily express in Viper. We are interested in rea-              common limitation across all these approaches was the
soning about concurrent scenarios. LionsOS encourages               significant gap between the analysed model and the ac-
systems to be composed from smaller components (such                tual executable code—a gap which we narrow by using
as our Ethernet driver), most of which are internally               Pancake’s verified compilation stack.
single-threaded but execute in parallel. We think that                 Others, which we detail below, have done better at
studying a parallel protocol in HOL4 and proving cor-               closing such gaps (e.g. in some cases providing support
rectness of each Pancake component against that proto-              for direct access by drivers to memory-mapped device
col using Viper is an interesting direction for future work.        ports, as we have), but failed to demonstrate scalability
   This composition of components will be correct if                beyond the simplest serial drivers – among other reasons,
each component performs the correct I/O actions. The                by failing to include any performance evaluation of the
I/O behaviour of a program can be captured in a single              drivers they verified.
value using interaction trees [Xia et al., 2020]. These                The earliest driver verification effort for a non-trivial
are a new approach to program semantics that use an in-             device we are aware of is that of Alkassar [2009]; Alka-
finite coinductive tree of input and output event nodes             ssar and Hillebrand [2008], who verified a (still simpli-
to model a program. We have developed an alternative                fied) ATAPI hard disk device driver in Isabelle/HOL in-
semantics for Pancake using interaction trees, and have             teractive proof assistant [Nipkow et al., 2002] as part of
experimented with proofs that programs obey an I/O pro-             the Verisoft project. Similar to our work, they verify
tocol using this semantics. This is a promising approach            their driver relative to a functional model of the memory-
to verifying, for instance, a whole network sub-system.             mapped device – in their case, based on a subset of the


                                                               12
ATAPI standard. However, the type safety of the frag-               notate each driver function. They mostly establish mem-
ment of C they used for most of their OS limited their              ory safety and address a public/private data distinction.
ability to model direct access to memory-mapped device              There does not appear to be any clear statement of the
ports directly from that language; consequently, they in-           function of the driver or of functional correctness. The
stead had to write and verify their driver in a MIPS-like           Ironclad paper gives some performance data, showing
assembly language.                                                  overheads of up to two orders of magnitude for single
   Duan and Regehr [2010] presented a framework for                 requests to their verified versus their unverified system,
verifying device drivers integrated with the L3 model of            but no measurements of the driver alone or of the system
ARM machine code [Fox, 2003; Fox and Myreen, 2010]                  under load, which would be needed to make a direct com-
for HOL4 [Slind and Norrish, 2008], with a UART driver              parison to our work. They also note that performance is
as the case study. Like Alkassar and Hillebrand [2008]              not their priority, whereas our goal here is to achieve both
they did not support reasoning about DMA, but Duan                  of high guarantees and performance.
[2013] later added support in the form of Hoare triples                Erbsen et al. [2021] offers an end-to-end story of
for device memory access scenarios. The way we inte-                a simple embedded system that includes an Ethernet
grate shared memory access in Pancake with the speci-               driver. However, this system is simple enough that it
fication of requires and ensures as Viper annotations               does not require an operating system in the usual sense.
is similar, and allows us to impose the requirements of             They also report ten-fold overhead as the performance
our device model on our driver’s device memory ac-                  results for the whole system. Again, their work does not
cess directly from the Pancake language. Schwarz and                provide analysis on the driver by itself, making a direct
Dam [2014] further extend the L3 model to support de-               performance comparison difficult.
vice drivers with DMA. This goes further than the device               We are also aware of some current efforts by Chen
model of our paper, as the Ethernet device we verify is             et al. [2024] to verify device drivers written in Rust
documented not to interfere with the hardware ring in-              [Klabnik and Nichols, 2017] using the Verus automated
dices, which are left under the control of the driver.              deductive verifier [Lattuada et al., 2023]. However, with-
   As part of the CertiKOS project, Chen et al. [2016]              out a formal semantics let alone a verified compiler,
added support for verifying drivers and integrating them            the possibility of end-to-end assurances for Rust-based
with their OS verification framework in the Rocq (for-              drivers still seems remote.
merly Coq) interactive proof assistant. Unlike the above               Finally, there has been also been work on driver syn-
works, whose drivers were implemented in assembly,                  thesis by [Ryzhyk et al., 2009b, 2014] that took as in-
the serial and interrupt controller device drivers Chen             put detailed specifications of interfaces for (1) the device
et al. [2016] verified are implemented in ClightX [Gu               class the driver needs to implement, the (2) device it-
et al., 2015], an extension of the CompCert Clight lan-             self and (3) OS service it needs to provide to the rest of
guage [Leroy, 2009] with extra instrumentation to sup-              the OS, written in a custom specification language. Al-
port CertiKOS’s abstraction-guided approach to OS veri-             though, like in our work, their device interface included
fication. Like our work, their use of a verified compiler (a        details such as valid registers and their sizes, it also in-
modification of CompCert) to compile the driver down to             cluded more detailed elements like a state transition di-
binary gives some assurance that any properties proved at           agram. In our work, we have a model of device state
the driver source level are preserved down to the binary.           that we use for specifying and verifying the maintenance
However, driver verification in their framework requires            of invariants (the valid_device(device) assertion seen
interactive proofs in Rocq, for a C variant whose proof             in Listing 3 and explained in Section 4.2)—this could in
relies on adding abstract state elements that can influence         future form the basis for more detailed, state machine-
program execution. This is more disruptive to the origi-            based specifications of internal device states. Note, how-
nal code than mere annotations or typical “ghost state”,            ever, that this synthesis work could not deal with DMA.
and arguably requires more formal methods experience
than automated deductive verification via annotations.              8   Conclusion
   Unlike our work, none of the works above presented
any analysis or discussion their drivers’ performance.              This paper presents, to our knowledge, the first formal
   The Ironclad verification [Hawblitzel et al., 2014] in-          verification of a demonstrably performant driver for a re-
cludes a network driver. They verify assembly code by               alistic, non-trivial device, the Ethernet NIC common to a
translating it into Dafny code along with assertions. They          number of variants of NXP i.MX 8M processors.
argue that verification at the level of assembly avoids is-            It also introduces the Pancake systems programming
sues with the compiler; since we have a verified com-               language, designed especially for systems-level code to
piler we prefer to verify the sources that the program-             be amenable to formal verification. With Pancake, it
mer writes. Like in our work, the Ironclad authors an-              makes two enabling contributions: (1) a verified com-

                                                               13
piler that carries the semantics of Pancake down to bi-                         Gerwin Klein, and Gernot Heiser. 2016. Cogent: Verifying High-
nary, leveraging CakeML’s verified compiler backend;                            Assurance File System Implementations. In International Confer-
                                                                                ence on Architectural Support for Programming Languages and Op-
and (2) an automated deductive verification front-end                           erating Systems. Atlanta, GA, USA, 175–188.
that takes Pancake with Viper annotations, leveraging the
Viper SMT-based verification framework.                                      Andrew W. Appel. 2011. Verified Software Toolchain. In European
                                                                               Symposium on Programming (Lecture Notes in Computer Science),
   This work shows that Pancake is usable for develop-                         Vol. 6602. Springer, 1–17.
ing verified, performant drivers. A PhD student with a
systems background and not much formal methods ex-                           Vytautas Astrauskas, Aurel Bílỳ, Jonáš Fiala, Zachary Grannan,
perience was able to write and verify the aforementioned                       Christoph Matheja, Peter Müller, Federico Poli, and Alexander J
                                                                               Summers. 2022. The Prusti project: Formal verification for Rust. In
Ethernet driver in a few person-months. The Pancake                            NASA Formal Methods Symposium. Springer, 88–108.
driver shows performance very close to C.
   This work paves the way for verified development                          Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller,
                                                                               and Alexander J. Summers. 2020. How do programmers use un-
of performant device drivers—a leading source of OS                            safe Rust? Proceedings of the ACM on Programming Languages 4,
vulnerabilities—as common-place infrastructure.                                OOPSLA (2020), 136:1–136:27.

                                                                             Hao Chen, Xiongnan (Newman) Wu, Zhong Shao, Joshua Lockerman,
Acknowledgements                                                               and Ronghui Gu. 2016. Toward compositional verification of inter-
                                                                               ruptible OS kernels and device drivers. In ACM SIGPLAN Confer-
                                                                               ence on Programming Language Design and Implementation. 431–
Many thanks to Alessandro Legnani’s project co-                                447.
supervisors Toby Murray, for his role in envisioning the
use of Viper, and Peter Müller for his feedback on this.                     Xiangdong Chen, Zhaofeng Li, Jerry Zhang, and Anton Burtsev. 2024.
                                                                                Veld: Verified Linux Drivers. In Workshop on Kernel Isolation,
We thank also Krishnan Winter, Benjamin Nott, Craig
                                                                                Safety and Verification. ACM, New York, NY, USA, 23–30.
McLaughlin and Remy Sasseau for their past and ongo-
ing contributions to other aspects of Pancake. Finally,                      Jianjun Duan. 2013. Formal Verification of Device Drivers in Embed-
we thank Isitha Subasinghe and Zoltan Kocsis, for their                         ded Systems. Ph.D. Dissertation. University of Utah, USA.
help understanding SMT performance issues from theory                        Jianjun Duan and John Regehr. 2010. Correctness Proofs for Device
mixing.                                                                         Drivers in Embedded Systems. In Systems Software Verification.
   The development of Pancake was made possible                                 USENIX Association, Vancouver, BC, CA.
through the generous support of multiple organisations:                      Andres Erbsen, Samuel Gruetter, Joonwon Choi, Clark Wood, and
the UAE Technology Innovation Institute (TII) under                            Adam Chlipala. 2021. Integration Verification across Software and
the Secure, High-Performance Device Virtualisation for                         Hardware for a Simple Embedded System. In ACM SIGPLAN Con-
                                                                               ference on Programming Language Design and Implementation.
seL4 project, DARPA under prime contract FA 8750-24-
9-1000, UK’s National Cyber Security Centre (NCSC)                           Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is
under project NSC-1686, and the German Agentur für                             Rust Used Safely by Software Developers?. In International Con-
                                                                               ference on Software Engineering. 246–257.
Innovation in der Cybersicherheit GmbH (Cyberagen-
tur). Finally, Junming Zhao gratefully acknowledges the                      Anthony Fox. 2003. Formal specification and verification of ARM6.
topup scholarship donated by the winners of the 2023                           In International Conference on Theorem Proving in Higher Order
                                                                               Logics (Lecture Notes in Computer Science), Vol. 2758. Springer,
ACM Software System Award.
                                                                               Rome, Italy, 25–40.

References                                                                   Anthony Fox and Magnus Myreen. 2010. A Trustworthy Monadic For-
                                                                               malization of the ARMv7 Instruction Set Architecture. In Interna-
Eyad Alkassar. 2009. OS Verification Extended – On the Formal Verifi-          tional Conference on Interactive Theorem Proving (Lecture Notes in
  cation of Device Drivers and the Correctness of Client/Server Soft-          Computer Science), Vol. 6172. Springer, Edinburgh, UK, 243–258.
  ware. Ph.D. Dissertation. Saarland University, Computer Science
  Department.                                                                Cyrill Martin Gössi. 2016. A Formal Semantics for Viper. Master’s
                                                                               thesis. ETH Zürich.
E. Alkassar, M. Hillebrand, S. Knapp, R. Rusev, and S. Tverdyshev.
   2007. Formal Device and Programming Model for a Serial Interface.         Ronghui Gu, Jérémie Koenig, Tahina Ramananandro, Zhong Shao,
   In International Verification Workshop. Bremen, DE, 4–20.                   Xiongnan (Newman) Wu, Shu-Chun Weng, Haozhong Zhang, and
                                                                               Yu Guo. 2015. Deep Specifications and Certified Abstraction Lay-
Eyad Alkassar and Mark A. Hillebrand. 2008. Formal Functional Ver-             ers. In ACM SIGPLAN-SIGACT Symposium on Principles of Pro-
  ification of Device Drivers. In Verified Software: Theories, Tools           gramming Languages. ACM, 595–608.
  and Experiments (Lecture Notes in Computer Science), Vol. 5295.
  Springer, Toronto, Canada, 225–239.                                        Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (Newman) Wu, Jieung
                                                                               Kim, Vilhelm Sjöberg, and David Costanzo. 2016. CertiKOS: An
Sidney Amani, Alex Hixon, Zilin Chen, Christine Rizkallah, Peter               Extensible Architecture for Building Certified Concurrent OS Ker-
   Chubb, Liam O’Connor, Joel Beeren, Yutaka Nagashima, Japheth                nels. In USENIX Symposium on Operating Systems Design and Im-
   Lim, Thomas Sewell, Joseph Tuong, Gabriele Keller, Toby Murray,             plementation. USENIX Association, Savannah, GA, US, 653–669.




                                                                        14
Chris Hawblitzel, Jon Howell, Jacob R. Lorch, Arjun Narayan,                Xavier Leroy. 2009. Formal verification of a realistic compiler. Com-
  Bryan Parno, Danfeng Zhang, and Brian Zill. 2014.    Iron-                  mun. ACM 52, 7 (2009), 107–115.
  clad Apps: End-to-End Security via Automated Full-System
  Verification. In USENIX Symposium on Operating Systems                    MITRE Corporation. 2023.      Linux ≫ Linux Kernel: Se-
  Design and Implementation. Broomfield, CO, US, 165–                         curity Vulnerabilities (CVSS score ≥ 9).        https:
  181.            https://www.usenix.org/conference/osdi14/                    //www.cvedetails.com/vulnerability-list.php?vendor_
   technical-sessions/presentation/hawblitzel                                  id=33&product_id=47&version_id=&page=1&hasexp=0&
                                                                               opdos=0&opec=0&opov=0&opcsrf=0\&opgpriv=0&opsqli=
Gernot Heiser, Ivan Velickovic, Peter Chubb, Alwin Joshy, Anuraag              0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&
  Ganesh, Bill Nguyen, Cheng Li, Courtney Darville, Guangtao Zhu,              opfileinc=0&opginf=0&cvssscoremin=9&cvssscoremax=
  James Archer, Jingyao Zhou, Krishnan Winter, Lucy Parker, Szy-               0&year=0&month=0&cweid=0\&order=1&trc=3034&sha=
  mon Duchniewicz, and Tianyi Bai. 2025. Fast, Secure, Adaptable:              544260ec3a86a7e17f8b02b39d6342815d8d4bd5      Accessed:
  LionsOS Design, Implementation and Performance. arXiv preprint               2023-01-25.
  (Jan. 2025), 14. https://arxiv.org/abs/2501.06234
                                                                            Tomas Möre. 2021. Formal verification of device driver monitors in
Bart Jacobs, Jan Smans, and Frank Piessens. 2010. A Quick Tour of             HOL 4. Masters Thesis. School of EECS, KTH, SE.
  the VeriFast Program Verifier. In Asian Symposium on Programming
  Languages and Systems (APLAS) (Lecture Notes in Computer Sci-             Peter Müller, Malte Schwerhoff, and Alexander J Summers. 2016a.
  ence), Vol. 6461. Springer, 304–311.                                         Automatic verification of iterated separating conjunctions using
                                                                               symbolic execution. In International Conference on Computer
Trevor Jim, J. Gregory Morrisett, Dan Grossman, Michael W. Hicks,              Aided Verification. Springer, 405–425.
   James Cheney, and Yanling Wang. 2002. Cyclone: A Safe Dialect
   of C. In USENIX. USENIX, Monterey, CA, USA, 275–288.                     Peter Müller, Malte Schwerhoff, and Alexander J Summers. 2016b.
                                                                               Viper: A verification infrastructure for permission-based reasoning.
Dejan Jovanovic and Clark W. Barrett. 2013. Being careful about the-           In International Conference on Verification, Model Checking and
  ory combination. 42, 1 (2013), 67–90.                                        Abstract Interpretation. Springer, St. Petersburg, FL, US, 41–62.
Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek
                                                                            Wolfgang Naraschewski and Tobias Nipkow. 1999. Type Inference Ver-
   Dreyer. 2018. RustBelt: Securing the Foundations of the Rust Pro-
                                                                              ified: Algorithm W in Isabelle/HOL. Journal of Automated Reason-
   gramming Language. In ACM SIGPLAN-SIGACT Symposium on
                                                                              ing 23, 3-4 (1999), 299–318.
   Principles of Programming Languages. 66:1–66:34.
                                                                            Tobias Nipkow, Lawrence Paulson, and Markus Wenzel. 2002. Is-
Shuanglong Kan, David Sanán, Shang-Wei Lin, and Yang Liu. 2018.
                                                                              abelle/HOL — A Proof Assistant for Higher-Order Logic. Lecture
  K-Rust: An Executable Formal Semantics for Rust. CoRR
                                                                              Notes in Computer Science, Vol. 2283. Springer.
  abs/1804.07608 (2018). Preprint.

Hrutvik Kanabar, Anthony C. J. Fox, and Magnus O. Myreen. 2022.             Scott Owens, Magnus Myreen, Ramana Kumar, and Yong Kiam Tan.
  Taming an Authoritative Armv8 ISA Specification: L3 Validation               2016. Functional Big-Step Semantics. In European Symposium on
  and CakeML Compiler Verification. In International Conference on             Programming. Eindhoven, The Netherlands, 27.
  Interactive Theorem Proving. 20:1–20:22.
                                                                            Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter
Moonzoo Kim, Yunja Choi, Yunho Kim, and Hotae Kim. 2008. Formal               Müller, and Alexander J Summers. 2024. Towards Trustworthy Au-
  Verification of a Flash Memory Device Driver – An Experience Re-            tomated Program Verifiers: Formally Validating Translations into
  port. In SPIN Workshop on Model Checking Software (Lecture Notes            an Intermediate Verification Language. Proceedings of the ACM on
  in Computer Science), Vol. 5156. Los Angeles, CA, US, 144–159.              Programming Languages 8, PLDI (2024), 1510–1534.

Steve Klabnik and Carol Nichols. 2017. The Rust Programming Lan-            Mathieu Paturel, Isitha Subasinghe, and Gernot Heiser. 2023. First
   guage. No Starch Press.                                                    steps in verifying the seL4 Core Platform. In Asia-Pacific Workshop
                                                                              on Systems (APSys). ACM, Seoul, KR, 7.
Gerwin Klein, June Andronick, Kevin Elphinstone, Toby Murray,
  Thomas Sewell, Rafal Kolanski, and Gernot Heiser. 2014. Com-              Willem Penninckx, Jan Tobias Mühlberg, Jan Smans, Bart Jacobs, and
  prehensive Formal Verification of an OS Microkernel. ACM Trans-             Frank Piessens. 2012. Sound Formal Verification of Linux’s USB
  actions on Computer Systems 32, 1 (Feb. 2014), 2:1–2:70.                    BP Keyboard Driver. In NASA Formal Methods Symposium (Lecture
                                                                              Notes in Computer Science), Vol. 7226.
Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick,
  David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt,             Leonid Ryzhyk, Peter Chubb, Ihor Kuz, and Gernot Heiser. 2009a.
  Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and            Dingo: Taming Device Drivers. In EuroSys Conference. Nuremberg,
  Simon Winwood. 2009. seL4: Formal Verification of an OS Kernel.             DE, 275–288.
  In ACM Symposium on Operating Systems Principles. ACM, Big
  Sky, MT, USA, 207–220.                                                    Leonid Ryzhyk, Peter Chubb, Ihor Kuz, Etienne Le Sueur, and Gernot
                                                                              Heiser. 2009b. Automatic Device Driver Synthesis with Termite. In
Ramana Kumar, Magnus Myreen, Michael Norrish, and Scott Owens.                ACM Symposium on Operating Systems Principles. Big Sky, MT,
  2014. CakeML: A Verified Implementation of ML. In ACM                       US, 73–86.
  SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
  guages. ACM, San Diego, 179–191.                                          Leonid Ryzhyk, Adam Christopher Walker, John Keys, Alexander
                                                                              Legg, Arun Raghunath, Michael Stumm, and Mona Vij. 2014. User-
Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha             Guided Device Driver Synthesis. In USENIX Symposium on Oper-
  Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Haw-                ating Systems Design and Implementation. Broomfield, CO, USA,
  blitzel. 2023. Verus: Verifying Rust Programs using Linear Ghost            661–676.
  Types. Proceedings of the ACM on Programming Languages 7,
  OOPSLA1 (April 2023), 30. https://doi.org/10.1145/3586037



                                                                       15
Leonid Ryzhyk, Yanjin Zhu, and Gernot Heiser. 2010. The Case for             Yong Kiam Tan, Magnus Myreen, Ramana Kumar, Anthony Fox, Scott
  Active Device Drivers. In Asia-Pacific Workshop on Systems (AP-              Owens, and Michael Norrish. 2019. The verified CakeML compiler
  Sys). New Delhi, India, 25–30.                                               backend. Journal of Functional Programming 29 (Feb. 2019), 57.

Oliver Schwarz and Mads Dam. 2014. Formal Verification of Secure             Feng Wang, Fu Song, Min Zhang, Xiaoran Zhu, and Jun Zhang. 2018.
   User Mode Device Execution with DMA. In Hardware and Soft-                   KRust: A Formal Executable Semantics of Rust. In 2018 Interna-
   ware: Verification and Testing. Springer International Publishing,           tional Symposium on Theoretical Aspects of Software Engineering
   Cham, 236–251.                                                               (TASE). IEEE Computer Society, 44–51.

Malte H Schwerhoff. 2016. Advancing automated, permission-based              Aaron Weiss, Daniel Patterson, Nicholas D. Matsakis, and Amal
  program verification using symbolic execution. Ph.D. Dissertation.           Ahmed. 2019. Oxide: The Essence of Rust. CoRR abs/1903.00982
  ETH Zurich.                                                                  (2019). Preprint.

Thomas Sewell, Magnus Myreen, and Gerwin Klein. 2013. Transla-               Felix A Wolf, Linard Arquint, Martin Clochard, Wytse Oortwijn,
  tion Validation for a Verified OS Kernel. In ACM SIGPLAN Con-                 João C Pereira, and Peter Müller. 2021. Gobra: Modular specifi-
  ference on Programming Language Design and Implementation.                    cation and verification of Go programs. In International Conference
  ACM, Seattle, Washington, USA, 471–481.                                       on Computer Aided Verification. Springer, 367–379.

Konrad Slind and Michael Norrish. 2008. A Brief Overview of HOL4.            Li-yao Xia, Yannick Zakowski, Paul He, Chung-Kil Hur, Gregory
  In International Conference on Theorem Proving in Higher Order                Malecha, Benjamin C. Pierce, and Steve Zdancewic. 2020. Inter-
  Logics. Springer, Montréal, Canada, 28–32.                                    action trees: representing recursive and impure programs in Coq.
                                                                                Proceedings of the ACM on Programming Languages 4 (Jan. 2020),
Speykious. 2024. cve_rs 0.6.0 - Rust. https://docs.rs/cve-rs/0.                 51:1–51:32.
  6.0/cve_rs/ Accessed: 2025-04-18.




                                                                        16
