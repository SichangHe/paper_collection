Logical Methods in Computer Science
Vol. 6 (3:6) 2010, pp. 1–41                                                            Submitted      Oct. 13, 2009
www.lmcs-online.org                                                                    Published      Aug. 18, 2010




           AUTOMATED VERIFICATION OF PRACTICAL GARBAGE
                           COLLECTORS

                             CHRIS HAWBLITZEL a AND EREZ PETRANK b
   a
       Microsoft Research, One Microsoft Way, Redmond, WA 98052, USA
       e-mail address: Chris.Hawblitzel@microsoft.com
   b
       Dept of Computer Science, Technion, Haifa 32000, Israel
       e-mail address: erez@cs.technion.ac.il


          Abstract. Garbage collectors are notoriously hard to verify, due to their low-level interac-
          tion with the underlying system and the general difficulty in reasoning about reachability
          in graphs. Several papers have presented verified collectors, but either the proofs were
          hand-written or the collectors were too simplistic to use on practical applications. In this
          work, we present two mechanically verified garbage collectors, both practical enough to
          use for real-world C# benchmarks. The collectors and their associated allocators consist
          of x86 assembly language instructions and macro instructions, annotated with precondi-
          tions, postconditions, invariants, and assertions. We used the Boogie verification generator
          and the Z3 automated theorem prover to verify this assembly language code mechanically.
          We provide measurements comparing the performance of the verified collector with that
          of the standard Bartok collectors on off-the-shelf C# benchmarks, demonstrating their
          competitiveness.




                                            1. Introduction
     Garbage collectors automatically reclaim dynamically allocated objects that will never
be accessed again by the program. Garbage collection is widely acknowledged for support-
ing fast development of reliable and secure software. It has been incorporated into modern
languages, such as Java and C#. Many recent projects have attempted to verify the safety
or correctness of garbage collectors. The goal of this verification is to reduce the trusted
computing base of a system and increase the system’s reliability. This is particularly im-
portant for secure systems based on proof-carrying code (PCC) [Nec97] or typed assembly
language (TAL) [MWCG98]; typical large-scale PCC/TAL systems can verify the safety
of the mutator (the program), but not of the run-time system that manages memory and
other resource on the mutator’s behalf. This prevents untrusted programs from customizing
   1998 ACM Subject Classification: D.2.4.
   Key words and phrases: Garbage Collection, Verification.
 b
    Part of this work was done while the author was on a sabbatical leave at Microsoft Research. Supported
by THE ISRAEL SCIENCE FOUNDATION (grant No. 845/06).




l      LOGICAL METHODS
       IN COMPUTER SCIENCE                   DOI:10.2168/LMCS-6 (3:6) 2010
                                                                                         c
                                                                                        CC
                                                                                             C. Hawblitzel and E. Petrank
                                                                                             Creative Commons
2                             C. HAWBLITZEL AND E. PETRANK




the run-time system. Furthermore, bugs in the unverified run-time systems could result in
security vulnerabilities that undermine the guarantees promised by PCC and TAL.
     Proving that garbage collectors are safe and correct has been a challenge. In this
work, we provide the first fully mechanized correctness proofs of garbage collectors and
allocators realistic enough to run large, off-the-shelf benchmarks. To make this verification
tractable, we exploit recent advances in automated theorem proving technology, using the
Boogie [BCD+ 05] and Z3 [dMB08b] tools to provide automated verification of the correctness
properties. Our key contribution is the expression of garbage collector specifications and
invariants in a style that allows efficient, automated verification.
     We verify two collectors, both practical enough for use with real-world C# benchmarks:
a Cheney copying collector [Min63, Che70], with a bump allocator; and a mark-sweep collec-
tor [McC60], with a local-cache allocator that allows fast bump-pointer allocation. Both are
simple enough to verify, yet efficient enough to support realistic benchmarks competitively.
The collectors and their associated allocators consist of x86 assembly language instructions
and macro instructions, annotated with preconditions, postconditions, invariants, and as-
sertions. These annotations require significant human effort to write, but once they are
written, the Boogie verification condition generator and the Z3 theorem prover verify the
annotated collectors automatically, with no further human intervention. The collectors and
allocators are entirely self-contained, relying on no unverified library code, and the ver-
ification relies on only a minimal set of trusted axioms and definitions describing 32-bit
arithmetic, x86 instructions, memory words, and the interface to the mutator.
     We show how to define higher-level abstractions, particularly abstractions drawn from
region-based type systems, in terms of these trusted axioms and definitions; these higher-
level abstractions provide forms of local reasoning that make automated verification tractable.
The verification ensures that if an allocation or garbage collection operation completes, then
the physical heap managed by the allocator and collector faithfully represents the abstract
graph of objects defined by the mutator. The verification also ensures that the garbage
collector deallocates all objects unreached during the collection. The verification does not
prove termination; verified collectors or allocators could fail to terminate because of an
infinite loop, or fail to terminate properly because of a 32-bit integer overflow exception, or
an explicit halt operation. (The allocators and collectors halt if they run out of memory, or
if the mutator relies on a feature not supported by our collectors, such as multithreading.)
     The collectors and allocators include support for objects, arrays, strings, header words,
interior pointers, static data scanning, stack scanning, object descriptors, stack frame de-
scriptors, return-address lookup tables, and bit-level data manipulation, making them re-
alistic enough to support off-the-shelf single-threaded C# benchmarks compiled with the
Bartok compiler, using the native Bartok memory layouts and descriptor formats. To assess
the efficacy of the proposed collectors, we ran the verified collectors with the Bartok runtime
and compared their performance with the standard Bartok mark-sweep and generational
copying collectors. The verified collectors demonstrated competitive performance.
     The contributions in this paper include:
(1) We provide the first mechanically verified garbage collectors that support a real-world
     object model, including vtables, arrays, object descriptors, stacks, etc.
(2) We provide the first mechanically verified garbage collectors that can link to code gen-
     erated by a real-world, optimizing compiler (Bartok).
              AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                           3




(3) We demonstrate how to apply automated verification to garbage collectors, including
    both copying and mark-sweep garbage collectors. This automation allows scaling the
    verification to realistic collectors without employing a huge human effort.
(4) We propose a simple, efficient, easy-to-verify mark-sweep collector and allocator based
    on local caches.
(5) We provide the first performance measurements of off-the-shelf C# benchmarks running
    on top of verified garbage collectors.

Outline. Section 2 discusses previous work on garbage collector verification. Section 3
describes Boogie and Z3. Section 4 presents a complete example mark-sweep collector and
allocator in the BoogiePL programming language [BCD+ 05], describing the specification
and invariants in detail. Section 5 generalizes Section 4’s ideas to cover copying collectors,
borrowing ideas from region-based type systems, and Section 6 presents a complete example
copying collector in detail. Section 7 presents two simple, yet practical, collectors (and their
allocators): a Cheney-queue copying collector and an iterative mark-sweep collector. Section
8 shows that the practical collectors perform reasonably well compared to Bartok’s native
collectors on a range of off-the-shelf C# benchmarks. Section 9 concludes.

Code availability. The garbage collectors were coded in an x86-like subset of the BoogiePL
language; a small tool automatically extracted the x86 instructions, which were assembled
and linked with the benchmarks (see Section 7.2). The complete BoogiePL code for the two
practical collectors is available as part of the public Microsoft Research Singularity RDK2
source (in “Source Code”, in the base/Imported/Bartok/runtime/verified/GCs directory,
which can be browsed without downloading all of Singularity) at:
   http://www.codeplex.com/singularity
The Boogie and Z3 tools (April 2008 release), used to verify the two collectors, are available
from:
   http://research.microsoft.com/specsharp/


                           2. Background and related work
    Hand-written proofs of garbage collector correctness, at least for abstract models of
garbage collectors, go back decades (e.g., [DLM+ 76, DG94, BTSR04, LP06]). The work
of Birkedal et al [BTSR04] is noteworthy for formally proving a Cheney copying collector
correct, rather than a mark-sweep collector, and emphasizing local reasoning based on sep-
aration logic. Nevertheless, the local reasoning is used mainly to separate pieces of the
invariant at a coarse granularity (e.g. separating invariants about forwarded objects from
unforwarded objects); we offer a different perspective on local reasoning in Section 5.
    Other work [Rus94, Gon96, Hav99, Jac98, GBB98, GGH07, Bur01, CGN03] has me-
chanically proven garbage collector correctness, but only for mark-sweep collectors, only
using abstract models of memory (for instance, representing the heap as just a mathe-
matical graph and the root set as just a mathematical set), only using abstract models of
programs rather than programs executable on real hardware, and (with the exception of
Russinoff [Rus94]), all using interactive theorem provers. For example, Russinoff [Rus94]
and Havelund [Hav99] both mechanically verify the same small (albeit concurrent) mark-
sweep algorithm, which consists of just 11 statements. In addition to the standard annota-
tions required to declare the algorithm’s invariants, both papers also required, as hints to the
4                              C. HAWBLITZEL AND E. PETRANK




theorem prover, many explicit user declarations of lemmas: 55 lemmas in Havelund [Hav99],
and over 100 lemmas in Russinoff [Rus94]. (Most of these lemmas are necessary because
the theorem provers lack the ability to automatically instantiate variables in definitions and
quantified formulas at useful values.) By contrast, the small collector presented in Section 4
requires no user-declared lemmas; a small number of triggering annotations embedded in
the source code and invariants provide the theorem prover with enough hints for the proof
to succeed.
     More recently, McCreight et al [MSLL07] used an interactive theorem prover to verify
the correctness of both mark-sweep and copying collectors written in a RISC-like assembly
language, with a more realistic memory model. Furthermore, their results are foundational,
requiring trust only in a small Coq proof checker (which is much smaller than Boogie/Z3),
a specification of correctness, and a RISC machine language model. This required an
enormous effort though, relying on over 10000 lines of Coq scripts per collector, and the
treatment of the memory still falls short of what realistic compilers expect: the collectors
assume that every object has exactly two fields, and there is no stack, no static data area,
no object and stack frame descriptors, and so on. We adopt McCreight et al’s definition of
correctness as a starting point for our work.
     Several papers [WA01, MSS01] use typed regions to implement type-safe copying garbage
collectors; these garbage collectors copy live data from an old region to a new region, and
then (safely) delete the old region. Type safety is a weaker property than correctness,
though, and these techniques don’t obviously extend to mark-sweep collection. We borrow
ideas from typed regions to help us verify our copying collector.
     Banerjee et al [BNR08] also use regions to aid program verification, providing a flexible
set of region constructors (region union, region intersection, etc.), and region predicates
(region disjointness, region subset, etc.). Although their programming language may be too
high level to express practical garbage collectors, their region operations could be useful
for GC verification in a lower-level language. Note that in contrast to typed regions and
Banerjee et al’s approach, we do not build regions into our logic or language directly; instead,
our garbage collectors construct regions from more primitive first-order logic concepts.
     Vechev et al [VYBR07] describe how to mechanically fit prefabricated, high-level garbage
collection building blocks together in a provably correct way, but they do not mechanically
verify the building blocks themselves. For instance, they assume that “The algorithm
skeleton is fixed, and the operations performed by the skeleton are known to be correct.
For example, we assume that basic stop-the-world tracing is implemented correctly (i.e.,
the trace procedure marks all the objects that are reachable from the pending set when
it executes without interruptions).” We expect our work to be complementary, since our
techniques could be used to verify building blocks for garbage collection.

                                     3. Boogie and Z3
     BoogiePL [BCD+ 05] is a simple imperative programming language designed to support
automated program verification. It includes pure (side-effect free) expressions, written in a
standard C/C#/Java syntax, imperative statements (which may update local variables and
global variables), pure functions, and imperative procedures. Procedures support precon-
ditions and postconditions, written with the keywords requires and ensures, that specify
what must be true upon entry to the procedure and what the procedure guarantees is true
              AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                            5




upon exit from the procedure. Within a procedure, loop invariants for while loops are writ-
ten with the invariant keyword. The following example shows a pure function Pos, which
returns true if its argument is positive, and a procedure IncreaseX that adds a positive
number y to a global variable x:
   function{:expand true} Pos(i:int)returns(bool){i>0}
   var x:int;
   procedure IncreaseX(y:int)
      requires Pos(y);
      modifies x;
      ensures x > old(x);
   {
      x := x + y;
   }
In this example, the expression old(x) refers to the value of x at the beginning of the
procedure’s execution, so that the postcondition “ensures x > old(x);” says that x will
have a larger value upon exit from the procedure than upon entry to the procedure. A
procedure must disclose all the global variables it modifies (just x in this example); this
allows callers of the procedure to know which variables remain unmodified by the procedure.
The expand true annotation turns a function definition into a macro that is expanded to
its definition whenever it is used, so that “requires Pos(y);” is just an abbreviation for
“requires y > 0;”. (Recursive or mutually recursive macro definitions are disallowed.)
     Our programs occasionally use the statement “assert P;”, which asks the verifier to
prove P, which is then used as a lemma for subsequent proving. (We do not use the statement
“assume P;”, which introduces a new lemma P without proof, since this would make our
verification unsound.)
     The Boogie tool generates verification conditions from the BoogiePL code. These ver-
ification conditions are logical formulas that, if valid, guarantee that each procedure call
satisfies the procedure’s precondition, each procedure guarantees its postcondition, and
each loop invariant holds on entry to the loop and is maintained by each loop iteration. For
example, the verification condition for the IncreaseX example above might be:
   Pos(y) ==> x + y > x
(Here, ==> is Boogie’s syntax for logical implication.)
     Boogie passes these verification conditions to an automated theorem prover, which
attempts to prove the validity of the verification conditions. We use the Z3 theorem
prover [dMB08b], which is efficient, scales to large formulas, and reasons about many useful
first-order logic theories, including integers, bit vectors, arrays, and uninterpreted functions.
     Both Boogie and Z3 are part of the trusted computing base for the verified garbage
collectors. In other words, a bug in Boogie or Z3 could incorrectly lead to a buggy
garbage collector being declared “verified”. Currently, our trust in Boogie and Z3 rests
on the large amount of testing that they have endured (including testing at public competi-
tions [SMT08]). In the future, we may also be able to leverage Z3’s recent proof generation
feature [dMB08a], which generates proofs checkable with a smaller trusted computing base,
although the time and memory overheads of proof generation may be prohibitive.
     BoogiePL’s data types are more purely mathematical than the data types in conven-
tional programming languages. The type int represents mathematical integers, ranging
from negative infinity to positive infinity, while bv32 represents 32-bit values. The theorem
6                              C. HAWBLITZEL AND E. PETRANK




prover support for int is more mature and efficient than for bv32, so we used int wherever
possible (Section 7 describes how we reconciled this approach with the x86’s native 32-bit
words).
     BoogiePL also supports array types [int]t for any element type t, defining arrays as
simple mappings from mathematical integers to elements. The BoogiePL “select” expression
a[i] retrieves element i from array a, where i can be any integer. The BoogiePL “update”
expression a[i := v] generates a new array, equal to a except at element i, where the new
array contains the value v, so that (a[i := v])[i] == v is true for any a, i, and v. For
convenience, the statement “a[i] := v;” is an abbreviation for “a := (a[i := v]);”.
Arrays can also be multidimensional: an array a of type [int,int]t supports a select
expression a[i1,i2] and an update expression a[i1,i2 := v]. Note that BoogiePL arrays
lack many properties of say, Java arrays. For example, BoogiePL arrays are not references,
so there’s no issue of aliasing: the statement “a := b;” assigns a copy of array b to variable
a.
     Due to formatting constraints, the BoogiePL code shown in this paper omits most type
annotations. We abbreviate a<=b && b<c as a<=b<c, and function{:expand true} as
fun. The notation “∀T ” is an abbreviation for the universal quantifier “∀” with a particular
trigger “T”, used as a hint to Z3, as described further in Section 4.3. For now, the reader may
ignore the “T”. Finally, the code uses a convention that variables prefixed with a dollar sign
(e.g. “$x”) are “ghost” variables, erased before run-time, as described further in Section
4.1.

                4. A miniature mark-sweep collector in BoogiePL
     This section presents a miniature allocator and mark-sweep collector written in the
BoogiePL programming language, introducing some of the invariants used by the more
realistic collectors in subsequent sections. The allocator and collector are implemented as a
single BoogiePL file, shown in its entirety in Figures 2-6. As in previous verified collectors,
a large fraction of the code consists of preconditions, postconditions, loop invariants, and
auxillary definitions. These require human effort to write, but once written, verification
is fast and automated. When run on this example garbage collector, Boogie verifies all 7
procedures in the collector in less than 2 seconds; since Boogie and Z3 process BoogiePL
files entirely automatically, no human assistance or proof scripts are required:
   \Spec#\bin\Boogie.exe mini-ms.bpl

    Boogie program verifier version 0.90,
    Copyright (c) 2003-2008, Microsoft.

   Boogie program verifier finished
   with 7 verified, 0 errors
The miniature collector assumes that every object has exactly two fields, numbered 0 and
1, and each field holds a non-null pointer to some object. The collector manages memory
addresses in the range memLo...memHi - 1, where memLo and memHi are constants such that
0 < memLo <= memHi, but whose values are otherwise unspecified (see Figure 2). Memory
is object addressed, rather than byte addressed or word addressed, so that each memory
location in the range memLo...memHi - 1 contains either an entire object, or free space big
enough to allocate an object in. The variable Mem, of type [int,int]int, represents all of
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                          7




                                      C2 $toAbs[C2] == A2 A2
                     Mem[C1,0]
                      == C2
           root          C1                                 A1

                                      C3                                 A3
                                               $AbsMem[A1,1]
                    Mem[C1,1]
                                                    == A3
                     == C3
                                                           A4




                          Figure 1: Concrete and abstract graphs

memory; for each address i in the range memLo...memHi - 1 and field field in the range
0...1, the value Mem[i,field] holds the contents of the field field in the object at address
i. For conciseness, Figure 2 defines memAddr(i) to mean memLo <= i < memHi.
     The allocator and collector use a variable Color to represent the state of memory at
each address. If Color[i] is 0, the memory at address i is free. Otherwise, the memory is
occupied by an object and is either colored white (Color[i] == 1), gray (Color[i] == 2),
or black (Color[i] == 3).

4.1. Concrete and abstract states. To verify a garbage collector, we must specify what
it means for a collector to be correct. For the mark-sweep collector, the most obvious
criterion is that it frees all objects unreachable from the root and leaves all reachable ob-
jects unmodified. However, this definition of correctness is specific to one particular class
of collectors; it doesn’t account for collectors that move objects, and doesn’t account for
mutator-collector interaction, such as write barriers and read barriers. We’d like one defini-
tion of correctness that encompasses many classes of collectors, so we follow a more general
approach advocated by McCreight et al [MSLL07]. In this approach, the mutator defines
an abstract state, consisting of an abstract graph of abstract nodes. A memory manager is
responsible for representing the abstract state in memory. The memory manager exposes
procedures to initialize memory, allocate memory, read memory, and write memory (see
Initialize, Alloc, ReadField, and WriteField in Figures 3, 6). These four procedures
define the boundary between the memory manager and the mutator. The preconditions
and postconditions for these four procedures express the specification of memory manager’s
correctness, where correctness means that each of these procedures faithfully represents the
abstract state.
8                             C. HAWBLITZEL AND E. PETRANK




     To make this notion of correctness precise, the variable $AbsMem of type [int,int]int
defines the abstract state as a mapping from abstract nodes and fields to abstract values.
In the miniature memory model presented so far, each field contains a pointer to a node,
so the abstract values stored in the abstract graph are always abstract nodes. (Section 7
extends the set of abstract values with other values, such as primitive integers and null.)
For example, Figure 1 shows an abstract graph consisting of 4 nodes, A1, A2, A3, and A4,
each having two fields numbered 0 (on top) and 1 (on the bottom). In this example, A1’s
bottom field points to A3, so $AbsMem[A1,1] == A3. Integers represent abstract nodes, but
these integers can be any mathematical integers, and need not be related to the addresses
used by the computer’s actual memory. In fact, the variable $AbsMem is not represented at
run-time at all; it is used solely for verification. We call such variables “ghost variables”
(also known as “auxillary variables”), and we use a naming convention that prefixes each
ghost variable with a dollar sign.
     The function MutatorInv(...) defines the invariant that holds on the memory man-
ager’s data while the mutator is running. Initialize establishes MutatorInv, while Alloc,
ReadField, and WriteField require MutatorInv as a precondition and guarantee MutatorInv
as a postcondition. Each collector defines MutatorInv(var1...varn) as it wishes. The mu-
tator is not allowed to modify any of the variables var1...varn directly, but instead must
use ReadField, WriteField, and Alloc to affect these variables. Since MutatorInv varies
across collectors, a mutator that wants to work with all collectors should treat MutatorInv
as abstract. In this framework, the specifications for Initialize, Alloc, ReadField, and
WriteField are exactly the same across all collectors, except for the differing definitions of
MutatorInv.
     The function $toAbs:[int]int maps each concrete memory address in the range
memLo...memHi - 1 to an abstract node, or to NO_ABS. The memory management proce-
dures ensure that $toAbs is well formed (WellFormed($toAbs)), which says that any two
distinct concrete addresses i1 and i2 map to distinct abstract nodes, unless they map to
NO_ABS. (Note: we use a concrete-to-abstract mapping, rather than an abstract-to-concrete
mapping, because our invariants quantify over concrete addresses, not abstract addresses,
and these quantified concrete addresses make convenient arguments to $toAbs.) In Figure 1,
$toAbs maps addresses C1, C2, and C3 to abstract nodes A1, A2, and A3, respectively, while
all other concrete addresses map to NO_ABS. The function Pointer($toAbs,ptr,$abs) says
that $toAbs maps the concrete address ptr to the abstract node $abs.
     Suppose the mutator calls ReadField(C1,0), which will return the contents of field 0 of
the object at address C1. The precondition Pointer($toAbs,ptr,$toAbs[ptr]) requires
C1 to be a valid pointer, mapped to some abstract node (A1 in this example). In the minia-
ture memory model presented so far, all fields hold pointers, so the return value will also be
a pointer; the postcondition for ReadField ensures that the returned value is the pointer
corresponding to the abstract node $AbsMem[$toAbs[ptr],field] = $AbsMem[A1,0] =
A2. Since only one pointer, C2, maps to A2, the postcondition forces ReadField(C1,0)
to return exactly the address C2. (The well-formedness condition, WellFormed($toAbs)
ensures that no node other than C2 maps to A2.) Once the mutator obtains the pointer
C2 from ReadField(C1,0), it may call, say, ReadField(C2,1) to obtain the pointer C3.
In this way, the specification of ReadField allows the mutator to traverse the reachable
portion of memory, even though the specification never mentions reachability directly. The
specification does not obligate the memory manager to retain unreachable objects. Since
              AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                           9




A1, A2, and A3 do not point to A4, the memory manager need not devote any physical
memory for representing A4. In Figure 1, there is no concrete address that maps to A4.
     Note that Figure 3’s implementation of ReadField always returns a value val that
equals Mem[ptr,field]. Therefore, we could write an alternate version of ReadField that
didn’t bother to return a value val, and instead wrote “Mem[ptr,field]” in its postcondi-
tions in place of val (e.g. ensures Pointer($toAbs,Mem[ptr,field],...)). In this case,
the mutator could perform the load from Mem[ptr,field] itself, relying on ReadField’s
postcondition to ensure that Mem[ptr,field] corresponds to the proper abstract node.
Similarly, we could write an alternate version of WriteField that omitted the statement
Mem[ptr,field] := val, and instead wrote Mem[ptr,field := val] in place of Mem in its
postconditions. In this case the mutator could store val to Mem[ptr,field] itself, relying
on WriteField’s postconditions to ensure that MutatorInv holds after the store. In fact,
our practical garbage collectors use these alternate versions of ReadField and WriteField,
so that the practical mutators can inline the loads and stores (this avoids the run-time
overhead of making calls to ReadField and WriteField to perform the loads and stores.)
     The mutator allocates new abstract nodes by calling Alloc (Figure 6), passing in a
fresh abstract node $abs whose fields initially point to itself. (A “fresh” abstract node is
an abstract node that does not yet appear in the range of $toAbs.) Unlike ReadField and
WriteField, Alloc modifies $toAbs, which potentially invalidates any pointers that the
mutator possesses. (The mutator can’t use an invalid pointer that refers to an old version
of $toAbs, because Pointer($toAbs,...) for an old $toAbs won’t satisfy the preconditions
for ReadField and WriteField, which are in terms of the current $toAbs.) Therefore, the
mutator may pass in a root pointer, and the Alloc procedure returns a new root pointer
that points to the same abstract node as the old pointer. We could also allow ReadField
and WriteField to modify $toAbs, in which case these procedures would also require a
root (or roots) to be passed in. In practice, though, this would be an onerous burden on
the mutator.

4.1.1. Verifying collection effectiveness. The specification described so far hides the garbage
collection process behind the Initialize, ReadField, WriteField, and Alloc interfaces.
We also verify one internal property of the garbage collector, invisible to the mutator: after
a collection, only abstract nodes that the collector reached have physical memory dedicated
to them; unreached abstract nodes are not represented in memory. It’s easy to define an
axiom for reachability for any particular abstract graph: for any node A, if A is reachable,
then A’s children are also reachable. It’s difficult, though, to track reachability as the
edges in a graph evolve. For the two collectors presented here, the $AbsMem graph remains
unmodified throughout collection, but in general, this is not true: incremental collectors
interleave short spans of garbage collection with short spans of mutator activity, and the
mutator activity modifies $AbsMem. Therefore, we adopt a looser criterion: rather than
checking that all remaining allocated nodes at the end of a collection are reachable from the
root, we merely check that all remaining allocated nodes were reached from the root at some
time since the start of the collection. Verifying this property was only a small extension to
the rest of the verification. (For simplicity, Figures 2-6 omit this property, but the practical
garbage collectors in the public source release include verification of this property.)
10                          C. HAWBLITZEL AND E. PETRANK




function{:expand false} T(i) { true }
const NO_ABS:int, memLo:int, memHi:int;
axiom 0 < memLo <= memHi;
fun memAddr(i) { memLo <= i < memHi }

fun Unalloc(i) { i == 0 }
fun White(i) { i == 1 }
fun Gray(i) { i == 2 }
fun Black(i) { i == 3 }

var Mem:[int,int]int, Color:[int]int;
var $toAbs:[int]int, $AbsMem:[int,int]int;

fun WellFormed($toAbs) {
  (∀Ti1.∀Ti2.
         memAddr(i1) && memAddr(i2)
     && $toAbs[i1] != NO_ABS
     && $toAbs[i2] != NO_ABS
     && i1 != i2
   ==> $toAbs[i1] != $toAbs[i2])
}
fun Pointer($toAbs, ptr, $abs) {
    memAddr(ptr) && $abs != NO_ABS && $toAbs[ptr] == $abs
}
fun ObjInv(i, $toAbs, $AbsMem, Mem) {
  $toAbs[i] != NO_ABS ==>
       Pointer($toAbs, Mem[i,0], $AbsMem[$toAbs[i],0])
   && Pointer($toAbs, Mem[i,1], $AbsMem[$toAbs[i],1])
}
fun GcInv(Color, $toAbs, $AbsMem, Mem) {
    WellFormed($toAbs)
 && (∀Ti. memAddr(i) ==>
              ObjInv(i, $toAbs, $AbsMem, Mem)
           && 0 <= Color[i] < 4
           && (Black(Color[i]) ==> !White(Color[Mem[i,0]])
                                 && !White(Color[Mem[i,1]]))
           && ($toAbs[i] == NO_ABS <==> Unalloc(Color[i])))
}
fun MutatorInv(Color, $toAbs, $AbsMem, Mem) {
    WellFormed($toAbs)
 && (∀Ti. memAddr(i) ==>
              ObjInv(i, $toAbs, $AbsMem, Mem)
           && 0 <= Color[i] < 2
           && ($toAbs[i] == NO_ABS <==> Unalloc(Color[i])))
}

              Figure 2: Miniature Mark-Sweep Collector: Definitions.
           AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                 11




procedure Initialize()
  modifies $toAbs, Color;
  ensures MutatorInv(Color, $toAbs, $AbsMem, Mem);
  ensures WellFormed($toAbs);
{
  var ptr;
  ptr := memLo;
  while (ptr < memHi)
    invariant T(ptr) && memLo <= ptr <= memHi;
    invariant (∀Ti. memLo <= i <ptr ==>
                    $toAbs[i] == NO_ABS && Unalloc(Color[i]));
  {
    Color[ptr] := 0;
    $toAbs[ptr] := NO_ABS;
    ptr := ptr + 1;
  }
}


procedure ReadField(ptr, field) returns (val)
  requires MutatorInv(Color, $toAbs, $AbsMem, Mem);
  requires Pointer($toAbs, ptr, $toAbs[ptr]);
  requires field == 0 || field == 1;
  ensures Pointer($toAbs, val, $AbsMem[$toAbs[ptr],field]);
{
  assert T(ptr);
  val := Mem[ptr,field];
}


procedure WriteField(ptr, field, val)
  requires MutatorInv(Color, $toAbs, $AbsMem, Mem);
  requires Pointer($toAbs, ptr, $toAbs[ptr]);
  requires Pointer($toAbs, val, $toAbs[val]);
  requires field == 0 || field == 1;
  modifies $AbsMem, Mem;
  ensures MutatorInv(Color, $toAbs, $AbsMem, Mem);
  ensures $AbsMem == old($AbsMem)[$toAbs[ptr],field := $toAbs[val]];
{
  assert T(ptr) && T(val);
  Mem[ptr,field] := val;
  $AbsMem[$toAbs[ptr],field] := $toAbs[val];
}

   Figure 3: Miniature Mark-Sweep Collector: Initialize, ReadField, WriteField.
12                        C. HAWBLITZEL AND E. PETRANK




procedure GarbageCollect(root)
  requires MutatorInv(Color, $toAbs, $AbsMem, Mem);
  requires root != 0 ==> Pointer($toAbs, root, $toAbs[root]);
  modifies Color, $toAbs;
  ensures MutatorInv(Color, $toAbs, $AbsMem, Mem);
  ensures root != 0 ==> Pointer($toAbs, root, $toAbs[root]);
  ensures (∀Ti.memAddr(i) && $toAbs[i] != NO_ABS ==>
                $toAbs[i] == old($toAbs)[i]);
  ensures root != 0 ==> $toAbs[root] == old($toAbs)[root];
{
  assert T(root);
  if (root != 0)
  {
    call Mark(root);
  }
  call Sweep();
}




procedure Mark(ptr)
  requires GcInv(Color, $toAbs, $AbsMem, Mem);
  requires memAddr(ptr) && T(ptr);
  requires $toAbs[ptr] != NO_ABS;
  modifies Color;
  ensures GcInv(Color, $toAbs, $AbsMem, Mem);
  ensures (∀Ti. !Black(Color[i]) ==> Color[i] == old(Color)[i]);
  ensures !White(Color[ptr]);
{
  if (White(Color[ptr]))
  {
    Color[ptr] := 2; // make gray
    call Mark(Mem[ptr,0]);
    call Mark(Mem[ptr,1]);
    Color[ptr] := 3; // make black
  }
}

        Figure 4: Miniature Mark-Sweep Collector: Garbage Collect, Mark.
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS            13




procedure Sweep()
  requires GcInv(Color, $toAbs, $AbsMem, Mem);
  requires (∀Ti. memAddr(i) ==> !Gray(Color[i]));
  modifies Color, $toAbs;
  ensures MutatorInv(Color, $toAbs, $AbsMem, Mem);
  ensures (∀Ti. memAddr(i) ==>
                     (Black(old(Color)[i]) ==> $toAbs[i] != NO_ABS)
                  && ($toAbs[i] != NO_ABS ==> $toAbs[i] == old($toAbs)[i]));
{
  var ptr;
  ptr := memLo;

    while (ptr < memHi)
      invariant T(ptr) && memLo <= ptr <= memHi;
      invariant WellFormed($toAbs);
      invariant (∀Ti. memAddr(i) ==>
          0 <= Color[i] < 4
       && !Gray(Color[i])
       && (Black(old(Color)[i]) ==>
               $toAbs[i] != NO_ABS
           && ObjInv(i, $toAbs, $AbsMem, Mem)
           && (Mem[i,0] >= ptr ==> !White(Color[Mem[i,0]]))
           && (Mem[i,1] >= ptr ==> !White(Color[Mem[i,1]])))
       && ($toAbs[i] == NO_ABS <==> Unalloc(Color[i]))
       && ($toAbs[i] != NO_ABS ==> $toAbs[i] == old($toAbs)[i])
       && (ptr <= i ==> Color[i] == old(Color)[i])
       && (i < ptr ==> 0 <= Color[i] < 2)
       && (i < ptr && White(Color[i]) ==> Black(old(Color)[i])));
    {
      if (White(Color[ptr]))
      {
        Color[ptr] := 0; // deallocate
        $toAbs[ptr] := NO_ABS;
      }
      else if (Black(Color[ptr]))
      {
        Color[ptr] := 1; // make white
      }
      ptr := ptr + 1;
    }
}

                 Figure 5: Miniature Mark-Sweep Collector: Sweep.
14                             C. HAWBLITZEL AND E. PETRANK




procedure Alloc(root, $abs) returns (newRoot,ptr)
  requires MutatorInv(Color, $toAbs, $AbsMem, Mem);
  requires root != 0 ==> Pointer($toAbs, root, $toAbs[root]);
  requires $abs != NO_ABS;
  requires (∀Ti. memAddr(i) ==> $toAbs[i] != $abs);
  requires $AbsMem[$abs,0] == $abs;
  requires $AbsMem[$abs,1] == $abs;
  modifies Color, $toAbs, Mem;
  ensures MutatorInv(Color, $toAbs, $AbsMem, Mem);
  ensures root != 0 ==> Pointer($toAbs,newRoot,old($toAbs)[root]);
  ensures Pointer($toAbs, ptr, $abs);
  ensures WellFormed($toAbs);
{

     while (true)
       invariant MutatorInv(Color, $toAbs, $AbsMem, Mem);
       invariant root != 0 ==> Pointer($toAbs, root, $toAbs[root]);
       invariant (∀Ti. memAddr(i) ==> $toAbs[i] != $abs);
       invariant root != 0 ==> $toAbs[root] == old($toAbs)[root];

     {
         ptr := memLo;

         while (ptr < memHi)
           invariant T(ptr) && memLo <= ptr <= memHi;
         {
           if (Unalloc(Color[ptr]))
           {
             Color[ptr] := 1; // make white
             $toAbs[ptr] := $abs;
             Mem[ptr,0] := ptr;
             Mem[ptr,1] := ptr;
             newRoot := root;
             return;
           }
           ptr := ptr + 1;
         }

         call GarbageCollect(root);
     }
}

                   Figure 6: Miniature Mark-Sweep Collector: Allocation.
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                         15




4.2. Allocation, marking, and sweeping. Figure 6’s Alloc procedure performs an (in-
efficient) linear search for a free memory address; if no free space remains, Alloc calls
the garbage collector. The collector recursively marks all nodes reachable from some root
pointer (the “mark phase”), and then deallocates all unmarked objects (the “sweep phase”).
Figures 4 and 5 show the code for the Mark and Sweep procedures. The next few paragraphs
trace the preconditions and postconditions for Mark and Sweep backwards, starting with
Sweep’s postconditions.
     A key property of Sweep is that it leaves no dangling pointers (pointers from allocated
objects to free space). This property is part of MutatorInv: each memory address i satisfies
ObjInv(i, ...), which ensures that if some object lives at i (if $toAbs[i] != NO_ABS),
then the object’s fields contain valid pointers to allocated objects (see Figure 2). Specif-
ically, the fields Mem[i,0] and Mem[i,1] are, like i, mapped to some abstract nodes, so
that $toAbs[Mem[i,0]] != NO_ABS and $toAbs[Mem[i,1]] != NO_ABS. To maintain this
property, Sweep must ensure that any object it deallocates had no pointers from objects
that remain allocated. Since Sweep deallocates white objects and leaves gray and black
objects allocated, Sweep’s preconditions requires that no gray-to-white or black-to-white
pointers exist.
     To rule out gray-to-white pointers, Sweep’s second precondition requires that no gray
objects exist at all:

                    requires (∀Ti. memAddr(i) ==> !Gray(Color[i]));
The GcInv function (see Figure 2) prohibits black-to-white pointers: every black object has
fields pointing to non-white objects. (This is known as the tri-color or three color invariant
[DLM+ 76].)
     The Mark procedure’s postconditions must satisfy Sweep’s preconditions. To ensure
that no gray objects exist at the end of the mark phase, Mark’s second postcondition says
that any non-black object at the end of the mark phase retained its original color from the
beginning of the mark phase. For example, any leftover gray objects must have been gray
at the beginning of the mark phase. Since no gray objects existed at the beginning, no gray
objects exist at the end. Mark obeys the ban on black-to-white pointers by coloring an object
black after its children are non-white. (Before coloring a node’s children, Mark temporarily
colors the node gray to indicate the node is “in progress”; without this intermediate step,
a cycle in the graph would send Mark into an infinite loop.)

4.3. Quantifiers and triggers. In the absence of universal and existential quantifiers,
many theories are decidable and have practical decision procedures. These include the
theory of arrays, the theory of linear arithmetic, the theory of uninterpreted functions, and
the combination of these theories. Unfortunately, adding quantifiers makes the theories
either undecidable or very slow to decide: the combination of linear arithmetic and arrays,
for example, is undecidable in the presence of quantifiers. This forces verification to rely
on heuristics for instantiating quantifiers. The choice of heuristics determines the success
of the verification.
     Many automated theorem provers, including Z3 [dMB08b, Mos09] and Simplify [DNS05],
use programmer-supplied triggers to guide quantifier instantiation. (Many other automated
theorem provers, such as CVC3 [GBT07] and Yices [Yic], use triggers internally, but do not
expose triggers directly to programmers.) Consider again Sweep’s precondition prohibiting
16                            C. HAWBLITZEL AND E. PETRANK




gray objects. Here are two ways to write this in BoogiePL syntax, each with a different
trigger:
   forall i::{memAddr(i)}memAddr(i)==>!Gray(Color[i]))
   forall i::{Color[i]} memAddr(i)==>!Gray(Color[i]))
Both have the same logical meaning, but use different instantiation strategies. The first asks
i to be instantiated with expression e whenever an expression memAddr(e) appears during an
attempt to prove a theorem. The second asks i to be instantiated with e whenever Color[e]
appears. Selecting appropriate triggers is challenging in general. With an overly selective
trigger, a quantified formula may never get instantiated, leaving a theorem unproved. With
an overly liberal trigger, a quantified formula may be instantiated too often (even infinitely
often), drowning the theorem prover in unwanted information.
     Shaz Qadeer suggested that we look at formulas of form forall i::{f(i)}f(i) ==> P,
using f(i) as a trigger. For example, we could use memAddr(i) as a trigger, although
this appears in so many places that it would be easy to accidentally introduce an infinite
instantiation loop. (The appearance of memAddr(ptr) inside the Pointer function, which
in turn appears in the ObjInv function, which in turn appears in the GcInv function, is
one example of such a loop.) To avoid accidental loops, we introduce a function T(i:int),
solely for use as a trigger, writing the invariants above as:
   forall i::{T(i)}T(i)==>memAddr(i)==>!Gray(Color[i]))
(Note that the ==> operator is right associative.)
     We define the function T to be true everywhere: for all i, T(i) == true. Thus, adding
T(e) to a logical formula doesn’t change the purely logical meaning of the formula. However,
T(e) does function as a hint to Z3, indicating that e is an interesting expression that should
be used to instantiate quantifiers. In this way, adding instances of T(e) for various e can
guide Z3’s quantifier instantiation, as illustrated further below.
     For conciseness, we abbreviate forall i::{T(i)}T(i)==> as ∀T i. To avoid instantia-
tion loops, we never write a formula of the form ∀T i.(...T(e)...), where e is some expression
other than a simple quantified variable.
     Based on the trigger T(i), we use two strategies to ensure sufficient instantiation of
quantified formulas. First, we write explicit assertions of T(e) for various expressions e that
appear in the program. This helps Z3 prove formulas (∀T i.P(i))==>P(e). For example, the
ReadField procedure explicitly asserts T(ptr) to instantiate the quantifiers in MutatorInv
at the value ptr.
     Second, we use the trigger T(i) to prove formulas of the form (∀T i.P(i))==>(∀T j.Q(j)).
In this case, since T appears in both quantifiers, Z3 automatically instantiates P at i=j
to prove Q(j). This second strategy isn’t sufficient for all P and Q; for example, know-
ing ∀T i.a[i + 5] == 0 does not prove ∀T j.a[j + 6] == 0, even though mathematically,
both these formulas are equivalent. Nevertheless, this strategy works well for purely local
reasoning. For example, Sweep’s loop invariant maintains the property:
                           ∀T i.memAddr(i)==>!Gray(Color[i])
If the loop updates Color by changing Color[ptr] to 1 (white), then the theorem prover
attempts to prove:
        (memAddr(i)==>!Gray(Color[i]))
   ==> (memAddr(i)==>!Gray(Color’[i]))
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                         17




where Color’ == Color[ptr := 1]. In the case where i != ptr, Color[i] == Color’[i]
and the proof is trivial. In the case where i == ptr, !Gray(Color’[i]) == !Gray(1) == true.
The proof is easy because the formula memAddr(i) ==>              !Gray(Color[i]) is entirely
local; it depends only on array elements at index i.
     Many formulas depend on non-local array elements, though. Consider how Mark main-
tains this piece of the tri-color invariant (no black-to-white pointers) from GcInv in Figure
2:
   Black(Color[i]) ==> !White(Color[Mem[i,0]])
This depends not only on i’s color, but on the color of some other node Mem[i,0]. For
non-local formulas, the local instantiation strategy suffices for some programs but not for
others. For example, it suffices for the collector in Figures 2-6 (we invite the reader to write
out the verification conditions by hand to see), but did not suffice for an analogous copying
collector that we wrote (it did not sufficiently instantiate information about objects pointed
to by forwarding pointers). This limitation motivated the use of regions, as described in
the next section.

                                        5. Regions
     A mark-sweep collector appears easier to verify than a copying collector, because the
mark-sweep collector doesn’t modify pointers inside objects. As the previous section men-
tioned, the mark-sweep collector in Figures 2-6 passed verification even with a very simple
triggering strategy, while the analogous copying collector did not. Therefore, this section
augments the two strategies described in the previous section with a third instantiation
strategy, based on regions. Together, these three strategies were sufficient for both mark-
sweep and copying collectors. (Although regions aren’t necessary for our mark-sweep col-
lector, and can be omitted for strictly non-moving mark-sweep collectors, regions would
be useful for mark-sweep collectors that employ compaction, or for collectors that combine
mark-sweep and copying collection.)
     Regions have proven useful for verifying the type safety of copying collectors [WA01,
MSS01], which suggests that they might also help verify the correctness of copying collectors.
Type systems for regions are similar to the verification presented in Section 4: Section 4’s
verification mapped concrete addresses to abstract nodes, while type systems type-check
a region by mapping concrete addresses in the region to types (e.g., a type system with
types Parent and Child might map Figure 1’s C1 to Parent and C2 and C3 to Child).
This suggests a strategy for importing regions (and the ease of verifying copying collectors
via regions) from type systems: rather than defining just one concrete-to-abstract mapping
$toAbs, allow multiple regions, where each region is an independent concrete-to-abstract
mapping.
     For example, consider how Figure 2’s object invariant uses $toAbs:
ObjInv(i,$toAbs,$AbsMem,Mem) =
   $toAbs[i] != NO_ABS ==>
       Pointer($toAbs, Mem[i,0], $AbsMem[$toAbs[i],0])
       ...
Expanding the Pointer function exposes a non-local invariant:
   $toAbs[i] != NO_ABS ==>
       ... $toAbs[Mem[i,0]] != NO_ABS ...
18                            C. HAWBLITZEL AND E. PETRANK




This invariant is crucial; as discussed in Section 4, it ensures that no dangling pointers
exist. However, it’s not obvious how to prove that this invariant is maintained when
$toAbs[Mem[i,0]] changes. Therefore, the remainder of this paper adopts a region-based
object invariant:
   ObjInv(i,$rs,$rt,$toAbs,$AbsMem,Mem) =
      $rs[i] != NO_ABS ==>
          Pointer($rt, Mem[i,0], $AbsMem[$toAbs[i],0])
     ...
This object invariant describes an object living in a source region $rs, whose fields point
to some target region $rt. Expanding the Pointer function yields:
   $rs[i] != NO_ABS ==>
       ... $rt[Mem[i,0]] != NO_ABS ...
Now we adopt another idea from region-based type systems: regions only grow over time,
and are then deallocated all at once; deallocating a single object from a region is not
allowed. In our setting, this means that for any address j and region $r, $r[j] may
change monotonically from NO_ABS to some particular abstract node, but thereafter $r[j]
is fixed at that abstract node. The function RExtend expresses this restriction; the memory
manager only changes $r to some new $r’ if RExtend($r,$r’) holds:
   fun RExtend($r:[int]int,$r’:[int]int) {
      (forall i::{$r[i]}{$r’[i]}
         $r[i] != NO_ABS ==> $r[i] == $r’[i])
   }
RExtend’s quantifier is not based on T; instead, it can trigger on either $r[i] or $r’[i].
(Note that RExtend introduces no instantiation loops, because it only mentions r and r’
at index i, and does not mention T at all.) In combination with the second strategy from Sec-
tion 4, this triggering allows Z3 to prove formulas of the form (∀T i.P(r[e]))==>(∀T i.P(r’[e])),
where e depends on i. For example, given the guarantee that RExtend($rt,$rt’), the ob-
ject invariant ensures that if $rt[Mem[i,0]] != NO_ABS, then $rt’[Mem[i,0]] != NO_ABS.
      Given this region-based object invariant, a memory manager can express all other in-
variants about node i as purely local invariants. For example, our region-based mark-sweep
collector relates i’s color to i’s region state using purely local reasoning, using a first re-
gion $r1 to represent the set of all currently allocated objects and a second region $r2 to
represent the set of objects reached so far during the current collection:
       (White(Color[i]) ==>
              $r1[i] != NO_ABS && $r2[i] == NO_ABS
          && ObjInv(i,$r1,$r1,$toAbs,$AbsMem,Mem))
   && (Gray(Color[i]) ==>
              $r1[i] != NO_ABS && $r2[i] != NO_ABS
          && $r1[i] == $r2[i]
          && ObjInv(i,$r1,$r1,$toAbs,$AbsMem,Mem))
   && (Black(Color[i]) ==>
              $r1[i] != NO_ABS && $r2[i] != NO_ABS
          && $r1[i] == $r2[i]
          && ObjInv(i,$r2,$r2,$toAbs,$AbsMem,Mem))
              AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                          19




If i is black, then ObjInv(i,$r2,$r2,...) ensures that i’s fields point to members of
region $r2. Members of $r2 cannot be white, since the invariant above forces white nodes
to not be members of $r2. Thus, the invariant indirectly expresses the standard tri-color
invariant (no black-to-white pointers), and the collector need not state the tri-color invariant
directly.
     We briefly sketch the region lifetimes during a mark-sweep garbage collection. The
collector’s mark phase begins with $r1 equal to $toAbs and $r2 empty (i.e. $r2 maps
all nodes to NO_ABS). At the beginning of the mark phase, all allocated objects are white,
so the invariant above needs ObjInv(i,$r1,$r1,...), and requires that no objects be
members of $r2. As the mark phase marks each reached node i gray, it adds i to $r2, so
that $r2[i] != NO_ABS. At the end of the mark phase, $r2 contains exactly the reached
objects, while $r1 and $toAbs are the same as at the beginning of the mark phase. The
sweep phase then removes unreached objects from $toAbs until $toAbs == $r2; Sweep
leaves $r1 and $r2 unmodified. After sweeping, only the objects in $r2 remain allocated
(sweeping removes all objects in $r1 that aren’t in $r2). At this point, $r1 is no longer
useful, so the mutator takes an action analogous to “deallocating” region $r1: it simply
forgets about $r1, throwing out all invariants relating to $r1 and keeping only the invariants
for $r2. In the next collection cycle, $r2 becomes the new $r1, and the process repeats.

                  6. A miniature copying collector in BoogiePL
     This section applies the previous section’s region-based verification to a miniature copy-
ing collector. Like the miniature mark-sweep collector, the miniature copying collector is a
single BoogiePL file; it is shown in its entirety in Figures 7-12.
     The copying collector is a standard two-space Cheney-queue collector [Che70]. The
heap consists of two equally sized spaces. At any given time, one of the spaces is called
from-space and the other is called to-space. From-space ranges from address Fi to Fl, while
to-space ranges from address Ti to Tl (where the F and T stand for from and to, and the
i and l indicate the initial address and the limit of each space).
     The allocator, shown in Figure 12, alloctes objects in from-space until from-space fills
up. The memory Fi...Fk contains allocated objects, and the memory Fk...Fl contains free
space, so that allocation simply requires bumping the variable Fk up by one.
     When from-space fills up with objects (so that Fk == Fl), the allocator calls the col-
lector, shown in Figure 11. The collector traverses all from-space objects reachable from
the root pointer, and copies these objects into to-space. (All objects left in from-space
are garbage, and are simply ignored by the mutator and collector.) The collector swaps
the Fi...Fl variables with the Ti...Tl variables, so that from-space becomes to-space and
to-space becomes from-space. The collector then returns returns control to the allocator,
which attempts allocation again. (Note that if no garbage existed before the collection,
then no free memory will be available after the collection; in this case, the allocator is out
of memory and has no choice but to give up.)
     The forwardFromspacePointer procedure copies a single object, with address ptr,
from from-space to to-space. However, before copying the object, it checks to make sure
that the object wasn’t already copied earlier. More specifically, for each object copied to
to-space, forwardFromspacePointer sets a forwarding pointer that points from the old
from-space object to the new to-space copy. The variable FwdPtr is an array mapping
each old from-space object’s address to the corresponding new to-space object address. If
20                          C. HAWBLITZEL AND E. PETRANK




function{:expand false} T(i) { true }
const NO_ABS:int, memLo:int, memMid:int, memHi:int;
const MAP_NO_ABS:[int]int;
axiom (∀Ti. MAP_NO_ABS[i] == NO_ABS);
axiom 0 < memLo && memLo <= memMid && memMid <= memHi;
fun memAddr(i) { memLo <= i < memHi }

var Mem:[int,int]int, FwdPtr:[int]int;
var $toAbs:[int]int, $AbsMem:[int,int]int;
var $r1:[int]int, $r2:[int]int;

// Fromspace ranges from Fi to Fl, where Fk..Fl is empty
//   Tospace ranges from Ti to Tl, where Tk..Tl is empty
var Fi:int;
var Fk:int;
var Fl:int;
var Ti:int;
var Tj:int;
var Tk:int;
var Tl:int;

fun WellFormed($r) {
  (∀Ti1.∀Ti2. memAddr(i1)
     && memAddr(i2)
     && $r[i1] != NO_ABS
     && $r[i2] != NO_ABS
     && i1 != i2
   ==> $r[i1] != $r[i2])
}

fun Pointer($r, ptr, $abs) {
    memAddr(ptr) && $abs != NO_ABS
 && $r[ptr] == $abs
}

fun ObjInv(i, $rs, $rt, $toAbs, $AbsMem, Mem) {
  $rs[i] != NO_ABS ==>
      Pointer($rt, Mem[i,0], $AbsMem[$toAbs[i],0])
   && Pointer($rt, Mem[i,1], $AbsMem[$toAbs[i],1])
}


                Figure 7: Miniature Copying Collector: Definitions.
            AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                21




fun GcInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl,
                $r1, $r2, $toAbs, $AbsMem, Mem) {
    WellFormed($toAbs)
 && memLo <= Fi && Fi <= Fk && Fk <= Fl && Fl <= memHi
 && memLo <= Ti && Ti <= Tj && Tj <= Tk && Tk <= Tl && Tl <= memHi
 && (Fl <= Ti || Tl <= Fi)
 && (∀Ti. memAddr(i) ==>
         ($r2[i] != NO_ABS ==> $toAbs[i] == $r2[i])
     && ($r1[i] != NO_ABS <==> Fi <= i < Fk)
     && ($r2[i] != NO_ABS <==> Ti <= i < Tk)
     && (Fi <= i < Fk ==>
             (FwdPtr[i] == 0 <==> $toAbs[i] != NO_ABS)
          && (FwdPtr[i] != 0 ==> Pointer($r2, FwdPtr[i], $r1[i]))
          && (FwdPtr[i] == 0 ==> $toAbs[i] == $r1[i]
                                 && ObjInv(i, $r1, $r1, $toAbs, $AbsMem, Mem)))
     && (Ti <= i < Tk ==>
              FwdPtr[i] == 0 && $toAbs[i] != NO_ABS && $toAbs[i] == $r2[i])
     && (Ti <= i < Tj ==> ObjInv(i, $r2, $r2, $toAbs, $AbsMem, Mem))
     && (Tj <= i < Tk ==> ObjInv(i, $r2, $r1, $toAbs, $AbsMem, Mem)))
}


fun MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl,
                      $toAbs, $AbsMem, Mem) {
    WellFormed($toAbs)
 && memLo <= Fi && Fi <= Fk && Fk <= Fl && Fl <= memHi
 && memLo <= Ti && Ti == Tj && Tj == Tk && Tk <= Tl && Tl <= memHi
 && (Fl <= Ti || Tl <= Fi)
 && (∀Ti. memAddr(i) ==>
         ObjInv(i, $toAbs, $toAbs, $toAbs, $AbsMem, Mem)
     && (Fi <= i < Fk ==> FwdPtr[i] == 0)
     && ($toAbs[i] != NO_ABS <==> Fi <= i < Fk))
}


// As a region evolves, it adds new mappings, but each mapping is
// permanent: RExtend ensures that new mappings do not overwrite old mappings.
fun RExtend(rOld, rNew) returns (bool)
{
  (forall i::{rOld[i]}{rNew[i]} rOld[i] != NO_ABS ==> rOld[i] == rNew[i])
}


           Figure 8: Miniature Copying Collector: Definitions, continued.
22                         C. HAWBLITZEL AND E. PETRANK




procedure Initialize()
  modifies $toAbs, FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl;
  ensures MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
  ensures WellFormed($toAbs);
{
  $toAbs := MAP_NO_ABS;
  Fi := memLo;
  Fk := memLo;
  Fl := memMid;
  Ti := memMid;
  Tj := memMid;
  Tk := memMid;
  Tl := memHi;
}


procedure ReadField(ptr, field) returns (val)
  requires MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
  requires Pointer($toAbs, ptr, $toAbs[ptr]);
  requires field == 0 || field == 1;
  ensures Pointer($toAbs, val,
                    $AbsMem[$toAbs[ptr],field]);
{
  assert T(ptr);
  val := Mem[ptr,field];
}


procedure WriteField(ptr, field, val)
  requires MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
  requires Pointer($toAbs, ptr, $toAbs[ptr]);
  requires Pointer($toAbs, val, $toAbs[val]);
  requires field == 0 || field == 1;
  modifies $AbsMem, Mem;
  ensures MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
  ensures $AbsMem ==
    old($AbsMem)[$toAbs[ptr],field := $toAbs[val]];
{
  assert T(ptr) && T(val);
  Mem[ptr,field] := val;
  $AbsMem[$toAbs[ptr],field] := $toAbs[val];
}

         Figure 9: Miniature Copying Collector: Initialization, Read, Write.
               AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                  23




procedure forwardFromspacePtr(ptr, $freshAbs) returns(ret)
  requires GcInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $r1, $r2, $toAbs, $AbsMem, Mem);
  requires T(ptr) && Fi <= ptr < Fk;
  requires T($freshAbs) && $freshAbs != NO_ABS;
  requires (∀Ti. memAddr(i) ==> $toAbs[i] != $freshAbs);

    modifies FwdPtr, $toAbs, $r2, Tk, Mem;

    ensures    GcInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $r1, $r2, $toAbs, $AbsMem, Mem);
    ensures    T(ret) && Pointer($r2, ret, $r1[ptr]);
    ensures    (∀Ti. memAddr(i) ==> $toAbs[i] != $freshAbs);
    ensures    (∀Ti. i != old(Tk) ==> Mem[i, 0] == old(Mem)[i, 0]);
    ensures    (∀Ti. i != old(Tk) ==> Mem[i, 1] == old(Mem)[i, 1]);
    ensures    RExtend(old($r2), $r2);
{
    if (FwdPtr[ptr] != 0) {

        // object already copied
        ret := FwdPtr[ptr];

    }
    else {
      // copy object to to-space

        while (Tk >= Tl) {
          // out of memory
        }

        assert T(ptr) && T(Tk);
        ret := Tk;
        Mem[ret, 0] := Mem[ptr, 0];
        Mem[ret, 1] := Mem[ptr, 1];
        FwdPtr[ret] := 0;
        $toAbs[ret] := $r1[ptr];
        $r2[ret] := $r1[ptr];
        $toAbs[ptr] := NO_ABS;
        FwdPtr[ptr] := ret;
        Tk := Tk + 1;

    }
}


                   Figure 10: Miniature Copying Collector: Forwarding.
24                              C. HAWBLITZEL AND E. PETRANK




procedure GarbageCollect(root, $freshAbs) returns(newRoot)
  requires MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
  requires root != 0 ==> Pointer($toAbs, root, $toAbs[root]);
  requires T($freshAbs) && $freshAbs != NO_ABS;
  requires (∀Ti. memAddr(i) ==> $toAbs[i] != $freshAbs);
  modifies FwdPtr, $toAbs, $r1, $r2, Fi, Fk, Fl, Ti, Tj, Tk, Tl, Mem;
  ensures MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
  ensures root != 0 ==> Pointer($toAbs, newRoot, old($toAbs)[root]);
  ensures (∀Ti. memAddr(i) ==> $toAbs[i] != $freshAbs);
{
  var fwd0, fwd1, temp;
  assert T(root);
  $r1 := $toAbs;
  $r2 := MAP_NO_ABS;
  if (root != 0) {
    call newRoot := forwardFromspacePtr(root, $freshAbs);
  }
  while (Tj < Tk)
    invariant T(Tj) && T(root) && T(newRoot);
    invariant GcInv(FwdPtr,Fi,Fk,Fl,Ti,Tj,Tk,Tl,$r1,$r2,$toAbs,$AbsMem,Mem);
    invariant root != 0 ==> Pointer($r2, newRoot, old($toAbs)[root]);
    invariant (∀Ti. memAddr(i) ==> $toAbs[i] != $freshAbs);
  {
    assert T(Mem[Tj,0]) && T(Mem[Tj,1]);
    call fwd0 := forwardFromspacePtr(Mem[Tj,0], $freshAbs);
    call fwd1 := forwardFromspacePtr(Mem[Tj,1], $freshAbs);
    Mem[Tj,0] := fwd0;
    Mem[Tj,1] := fwd1;
    Tj := Tj + 1;
  }
  temp := Fi;
  Fi := Ti;
  Ti := temp;

     temp := Fl;
     Fl := Tl;
     Tl := temp;

     Fk := Tk;
     Tj := Ti;
     Tk := Ti;

     $toAbs := $r2;
}

                 Figure 11: Miniature Copying Collector: Garbage Collection.
              AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                  25




procedure Alloc(root, $abs) returns (newRoot,ptr)
  requires MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
  requires root != 0 ==>
             Pointer($toAbs, root, $toAbs[root]);
  requires $abs != NO_ABS;
  requires (∀Ti. memAddr(i) ==> $toAbs[i] != $abs);
  requires $AbsMem[$abs,0] == $abs;
  requires $AbsMem[$abs,1] == $abs;

    modifies FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, Mem, $r1, $r2;

    ensures   MutatorInv(FwdPtr, Fi, Fk, Fl, Ti, Tj, Tk, Tl, $toAbs, $AbsMem, Mem);
    ensures   WellFormed($toAbs);
    ensures   root != 0 ==>
                Pointer($toAbs, newRoot, old($toAbs)[root]);
    ensures   Pointer($toAbs, ptr, $abs);

{
    newRoot := root;
    assert T(root);

    if (Fk >= Fl) {
      call newRoot := GarbageCollect(root, $abs);
    }

    while (Fk >= Fl) {
      // out of memory
    }

    assert T(newRoot) && T(Fk);

    ptr := Fk;
    $toAbs[ptr] := $abs;
    $r1[ptr] := $abs;

    Mem[ptr,0] := ptr;
    Mem[ptr,1] := ptr;
    FwdPtr[ptr] := 0;

    Fk := Fk + 1;
}

                   Figure 12: Miniature Copying Collector: Allocation.
26                             C. HAWBLITZEL AND E. PETRANK




FwdPtr[ptr] is non-zero, then the object at from-space address ptr was already copied
to the to-space address FwdPtr[ptr], and forwardFromspacePointer simply returns this
to-space address. Otherwise, forwardFromspacePointer copies each field of the object into
to-space, sets FwdPtr[ptr] to the to-space address, and returns the to-space address.
     When the collector copies an object to to-space, the fields of the copied object initially
point back to from-space. The collector later fixes up the pointers to point to to-space by
calling forwardFromspacePointer on each field of the to-space object. The set of objects
not yet fixed form a contiguous work area in to-space. The collection algorithm in Figure
11 treats this work area as a “scan queue”: forwardFromspacePointer adds newly copied
objects to the back of the queue (Tk), and GarbageCollect fixes objects from the front
of the queue (Tj). When the queue is empty (Tj == Tk), all objects are fixed, and the
collection is done.
     The copying collector shares the same region-based ObjInv from Section 5. Other
invariants differ from the mark-sweep collector, though. For example, the copying collector
has no colors, so there is no invariant to relate colors to regions. There are invariants that
relate the forwarding pointer to regions, though. For example, each object i in from-space
satisfies this invariant, which ensures that no object with a non-null forwarding pointer is
present in $toAbs, and that any forwarding pointer points to a resident of $r2:
    (FwdPtr[i] == 0 <==> $toAbs[i] != NO_ABS)
&& (FwdPtr[i] != 0 ==> Pointer($r2,FwdPtr[i],$r1[i]))
     The region $r2 is empty at the start of the collection. The collector adds each object
that it creates in to-space to $r2, while leaving $r1 unchanged. The collector also updates
$toAbs to reflect the current concrete location of each abstract object (either moved to
to-space, or still living in from-space); at the end, the collector assigns $r2 to $toAbs, and
throws out all invariants related to $r1.
     During the collection, each fixed object in to-space points from region $r2 to region
$r2:
      ObjInv(i,$r2,$r2,$toAbs,$AbsMem,Mem)
Each object still in the to-space scan queue points from region $r2 back to region $r1:
      ObjInv(i,$r2,$r1,$toAbs,$AbsMem,Mem)
Meanwhile, each object in from-space points from region $r1 to region $r1:
      ObjInv(i,$r1,$r1,$toAbs,$AbsMem,Mem)
In this way, the region variables $r1 and $r2 concisely specify the state of each object.

                           7. Practical verified collectors
     This section applies the region-based verification from the previous two sections to real-
istic copying and mark-sweep collectors, replacing the naive recursive mark-sweep algorithm
of Figures 2-6 with a more efficient iterative algorithm in subsection 7.1, then replacing high-
level language constructs with assembly language in subsection 7.2, and then replacing the
miniature 2-field, 1-root memory model with a Bartok-compatible memory model in sub-
section 7.3. If sections 4-6 were the inspiration, this section is the perspiration; the code for
the realistic collectors is far longer than Figures 2-12, but not fundamentally much more
interesting. We present only short description and selected highlights of the code, including
a large excerpt from the realistic copying collector in subsection 7.4; the reader can find the
full code and complete invariants in the public release.
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                          27




7.1. Practical mark-sweep algorithm. Our verified mark-sweep collector uses the stan-
dard 3-color invariant. In the beginning of the collection all objects are white and the goal
is to mark black all objects reachable from the roots. After this marking process, the sweep
process can go over the objects to reclaim all white objects and to mark all black objects
white in preparation for the next collection. In the beginning of the collection all objects
directly reachable from the roots are put into a list denoted the mark-stack. All objects
in this list are colored gray, meaning that they have been reached, but their descendants
have not yet been traversed. After the roots have been scanned, the collector proceeds by
iteratively choosing a gray object O from the mark-stack, inserting O’s direct descendants
into the mark-stack and marking O black. The black color signifies that the object is reach-
able and all its direct descendants have been noticed (i.e., put in the mark-stack). The
unallocated color labels free space.
     Keeping the object color requires two bits per object. The colors can be kept in the ob-
ject header or in a separate table. Following previous work (e.g., [DKP00, ALPP03, KP06])
we have chosen the latter. Bartok assumes that objects are 4-byte aligned. Therefore, it
is enough to keep two color bits per 4 bytes (creating a space overhead of 6%). The two
bits that correspond to the beginning of an object specify its color. All other bit pairs are
marked as unallocated. This provides an additional benefit. When a pointer in the heap
points to a location that is marked unallocated, we know that the said pointer is an interior
pointer. Interior pointers that are discovered during the tracing stage must be treated in a
special manner. The collector needs to find the beginning of the object in order to discover
its header and from it information on pointer fields in the object.
     The algorithm follows a very simple collection scheme. One could choose a simpler
scheme for verification, for example, by giving up the mark-stack and searching the heap
for gray objects, or employing recursion. One could also complicate the scheme and make it
more efficient, for example, by using bit-wise sweep. However, we attempted to find the mid-
dle way between simplicity and efficiency, in order to enable verification while maintaining
the practicability of the collector.

7.1.1. The allocator. A major performance consideration is the allocator. Therefore, we
paid special attention to making the allocator efficient, cache-friendly, scalable, and sim-
ple. We chose the local allocation cache method that was first invented and used with
the IBM JVM allocator [Bor02] and later employed and explained in [BBYG+ 05, KP06].
This method provides efficiency by allowing bump-pointer allocation with a mark-sweep
collection. The mutator holds a local cache in which it allocates small objects by simply
bumping a pointer. When the space in the cache is exhausted, the mutator acquires a new
local cache from the first chunk in the free list. If that chunk is too large (larger than some
threshold maxCacheSize), then only maxCacheSize bytes of the first chunk are taken for the
local cache, and the rest is left for future cache allocations. Allocation of large objects use
the free list directly; however, since most allocated objects in typical programs are small,
most allocation work is efficient. Furthermore, these allocations are cache-friendly since the
spatial order of allocated objects in the memory matches the temporal order in which the
program allocates them.
     Since the mutator only acquires objects or spaces of substantial size from the free list,
there is no need to keep small chunks in it. Thus, sweep only fills the free-list with large
enough spaces; in our implementation the minimum cache size was set to 256 bytes and
28                             C. HAWBLITZEL AND E. PETRANK




objects of size 192 or up are considered large (and are thus directly allocated from the free
list).
     The mark-sweep collector invariants follow the region-based approach of Section 5,
sharing the definition of Pointer and ObjInv with the copying collector. Unlike earlier
sections, though, this mark-sweep collector has a free list with non-trivial structure. We
use two ghost variables, $fs and $fn to represent the size of each free list entry and the
next-list-entry pointer in each free list entry. Any address i where $fs[i] != 0 holds a free
list entry. Each free list entry must be at least 8 bytes: 4 bytes to store the next pointer,
and 4 bytes to store the size. The central invariant ensures, among other things, that the
space occupied by each free list entry does not overlap with any object or any other free
list entry:

     $fs[i] != 0 ==>
          $toAbs[i] == NO_ABS
      && i + 8 <= i + $fs[i] <= memHi
      && (∀T j. i < j < i + $fs[i] ==>
               $toAbs[j] == NO_ABS && $fs[j] == 0)
      && ...
It also ensures that any non-null next-list-entry pointer points to a subsequent list entry,
and that there are no other non-null next-list-entry pointers between the i and $fn[i]:
     $fs[i] != 0 ==>
          ($fn[i] != 0 ==> i + $fs[i] < $fn[i] <= memHi
             && $fs[$fn[i]] != 0)
      && (∀T j. i < j < $fn[i]
             && $fs[j] != 0 ==> $fn[j] == 0)
To allocate a new local cache, the allocator disconnects the first list element from the rest
of the free list. (For convenience in this case, the invariants allow disconnected list elements
to co-exist with the rest of the free list.)

7.1.2. Pseudo-code. Figure 13 specifies the marking phase, written as high-level pseudocode.
The objects reachable from the roots are marked, and then, using the mark-stack, all
reachable objects are popped from the stack, marked black, and their children are marked
gray (and pushed to the markStack if necessary).
     The sweep phase is also depicted in Figure 13. We keep a very simple algorithm. Note
that we do not bother maintaining information that would allow jumping over unallocated
objects (hence the statement “addr += 4;”, which jumps only over one word). There are
various other optimizations possible, but we chose a version that keeps the balance between
simplicity and efficiency.
     Finally, the pseudo-code of the allocator is provided in Figure 14. Small objects are
allocated from the local cache. A slow path occurs when the cache is exhausted or the
allocation is of a large object. In these cases the free-list must be traversed. For a cache
allocation any chunk is good, so the first chunk is used. If the first chunk is very large, then
only part of it is assigned as the current cache. For large objects, the list is traversed using
a first-fit allocation strategy. After the object is allocated from the chunk, the remains of
the chunk is returned to the free list only if the created smaller chunk has size larger than
minCacheSize.
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                          29




pseudocode Mark()
   for each object Obj directly reachable from roots
      markStack.push(Obj);
      Color[Obj] := GRAY;
   Obj := markStack.pop();
   while (Obj != null)
      for each object A referenced by Obj
         if (White(Color[A])) then
            markStack.push(A);
            Color[A] := GRAY;
      Color[Obj] := BLACK;
      Obj := markStack.pop();

pseudocode Sweep()
   Initialize free-list to null;
   Clear any local cache currently in use;
   for (addr := heapStart; addr < heapEnd; )
      color := Color[addr];
      if (Black(color))
         // Check free region prior to this object.
         regionSize := size of region since previous black object.
         if (regionSize >= minCacheSize)
            Add accumulated region to free-list;
         Color[addr] := WHITE;
         addr += SizeOf(addr);
      elseif (White(color))
         Color[addr] := UNALLOCATED;
         addr += SizeOf(addr);
      elseif (Unallocate(color))
         addr += 4; // Step over free space.


                            Figure 13: Mark-sweep pseudocode.

7.2. From BoogiePL to x86. So far, this paper has expressed all memory management
code in BoogiePL or in pseudocode, neither of which were designed to execute on real
computers. We decided to write our real copying and mark-sweep collectors (and allocators)
in x86 assembly language, for two reasons. First, we didn’t want a high-level language
compiler in our trusted computing base. Second, the mutator-to-allocator interface requires
some assembly language to read the stack pointer, so that the collectors can scan the roots
on the stack. We still wanted to use Boogie to verify our code, so this left us with a
choice: translate annotated x86 into BoogiePL, or translate BoogiePL into x86. The former
approach is the most common way to use BoogiePL, but we chose the latter approach, for
the following reason. Since the garbage collectors are written in BoogiePL, the Boogie and
Z3 tools guarantee that we really have verified the collectors, at least in BoogiePL form, even
if our BoogiePL-to-x86 translation subsequently turns the verified BoogiePL into erroneous
30                            C. HAWBLITZEL AND E. PETRANK




pseudocode Allocate(size)
   If (size < largeObject) // A small object
      if (size > cacheSize ) // Cache too small
         If (free-list empty)
            Call GC;
            if (free-list empty)
               Out of Memory;
         Allocate cache from first free-list chunk;
      // Allocate in local cache
      objectStart := cachePtr + cacheSize - size;
      cacheSize -= size;
      Color[objectStart] := WHITE;
      Initialize memory objectStart ... objectStart + size - 1 to zero.
      return objectStart;
   else // A large object
      Find first large-enough free-list chunk C;
      If none exist then
         call GC;
         Find first large-enough free-list chunk C;
         If none exists then Out Of Memory;
      objectStart := C.ptr + C.size - size;
      C.size -= size;
      if (C.size < minCacheSize)
         remove C from free-list;
      Color[objectStart] := WHITE;
      Initialize memory objectStart ... objectStart + size - 1 to zero.
      return objectStart;


                            Figure 14: Allocation pseudocode.

x86 code. (If we had translated x86 to BoogiePL, we would have had to ask the reader to
trust that our translator didn’t just produce a trivially verifiable BoogiePL program.)
     We wrote a small tool to automatically translate an x86-like subset of BoogiePL into
MASM-compatible x86 code, which we then assemble and link with Bartok-compiled bench-
marks. The tool rejects BoogiePL programs that do not conform to the x86-like subset,
such as programs that attempt to use ghost variables at run-time. The x86-like subset
of BoogiePL (an example of which appears in Figures 15-16) consists of top-level variable
declarations, non-recursive pure function declarations, and non-recursive procedure declara-
tions. Each procedure is either a macro that gets inline-expanded, or a run-time procedure
called with the x86 CALL instruction. The tool enforces matching CALL and RETURN in-
structions; the BoogiePL code may read the stack pointer at any time, but may not write it.
Each procedure consists of local variable declarations followed by a sequence of statements.
Since there’s no recursion, local variables are statically allocated, as in early FORTRAN.
Global and local variables may be ghost variables, of any type, or physical variables, of type
int. The tool enforces our convention that ghost variables always begin with a $ character.
The predefined global variables eax, ebx, ecx, edx, esi, edi, ebp, and esp, all of type int,
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                       31




represent the x86 registers. We maintain the invariant that all registers, physical variables,
and words in memory hold an integer in the range 0..232 − 1 at all times.
     Each statement in a procedure is a label (used as a jump or branch target), an as-
signment to a ghost variable (ignored by the translation), an assignment to a register or
physical variable, a procedure call, or a control statement. Control statements are either
unconditional jumps (“goto label;”) or conditional branches:
if(operand1 cmp operand2) { goto label; }
where operand1 and operand2 are registers, physical variables, or integer constants, and
cmp is a comparison operator. Most statements are translated into single x86 instructions,
but conditional branches translate into 2 x86 instructions (a compare and a branch). A
procedure call either translates into an inline expansion of the called procedure, or a single
x86 CALL instruction.
     Each assignment statement is either a simple move operation “operand1 := operand2;”,
an arithmetic operation, or a memory operation. Arithmetic operations can either stati-
cally check for 32-bit integer overflow, or check at run-time. For example, the statement
“call eax := Sub(eax, 5);” statically verifies that eax - 5 does not overflow, because
of the (tool-supplied) specification of Sub (where word(e) means that 0≤e< 232 ):
procedure Sub(x:int, y:int) returns(ret:int);
   requires word(x - y);
   ensures ret == x - y;
The program is not allowed to modify predefined global variables, like Mem, directly. To read
or write memory, the program must call tool-supplied Load and Store procedures, which the
tool translates into x86 MOV instructions. The preconditions for Load and Store guarantee
that the verified code does not read or write outside its allowed memory area, and that all
reads and writes are to 4-byte aligned addresses. In contrast to the two-dimensional memory
Mem[objAddress,field] presented earlier, Load and Store work with a one-dimensional
memory Mem[byteAddress].

7.3. The Bartok memory model. Our verified garbage collectors form a critical piece of
our long-term goal: an entire verified run-time system for Bartok-compiled code. Because
the existing Bartok run-time system contains over 70,000 lines of code, we decided to take
an incremental approach towards creating a verified run-time system, starting with as small
a run-time system as possible, so as to make the verification as easy as possible. We still
wanted to be able to run real Bartok-compiled benchmarks, though, and these benchmarks
rely on many non-trivial run-time system features. So before attempting to verify any run-
time system code, we examined the 12 large benchmarks used in previous papers [CHP+ 08,
PPS08] to see which features could be evicted from the run-time system. We found that
we could remove two major features, while still supporting 10 of the 12 benchmarks:
• Only one benchmark (SpecJBB) was multithreaded, so we omitted support for multi-
  threading from our run-time system.
• Only one of the remaining benchmarks (mandelform) relied on GC support for unsafe
  code, such as pinning objects (to cast GC-managed pointers to unmanaged pointers for
  unsafe code) and handling callbacks from unsafe code to safe code. Our verified GC
  simply halts any program that tries to use these features.
This still left a moderately large set of features to support:
32                             C. HAWBLITZEL AND E. PETRANK




• Objects have a header word, pointing to a virtual method table (vtable). Before the
  header word, there is a “pre-header” that holds a hash code or other primitive value.
• Non-indexed object types can have any number of fields. Indexed object types can be
  strings, single-dimensional arrays, or multi-dimensional arrays, each having a different
  memory layout. Array element types can be pointers, primitive values, structs without
  pointers, or structs with pointers. We implemented only partial support for arrays of
  structs with pointers, since the 10 benchmarks did not rely on full support.
• Pointers point to an object’s header word, with one exception: root pointers may be
  interior pointers that point to data inside an object, ranging from the header word up
  to, and including, the address of the end of the object (i.e. the address of the first word
  beyond the object’s last field or array element).
• An object’s virtual method table has fields that the collector can read to compute the
  length of an object and to determine which fields of an object are pointers. Bartok’s
  pointer-tracking representation consists of 2 compact bit-level formats for non-indexed
  objects, 1 non-compact format for non-indexed objects, 1 format for strings, 2 formats
  for single-dimensional arrays, and 2 formats for multi-dimensional arrays. Our collectors
  support all of these (except for some arrays of structs with pointers).
• Roots may live on the stack or in static data segments. Each static data segment has a
  bitmap, with one bit per static data word, indicating pointers and non-pointers in the
  segment. Finding pointers on the stack is more complicated; the collector has to traverse
  frame pointers to find the stack frames, and it has to look up return addresses in a sorted
  table of return addresses to find a descriptor for each frame. To simplify finding pointers,
  we set a compiler flag telling Bartok to treat all registers as caller-save registers, with no
  callee-save registers.
Although the complete BoogiePL specification of the features above is rather long and
tedious, it’s worth showing one example. One of the compact pointer-tracking formats is a
dense format, using one bit per field. The specification for this says that if the tag of an
object for abstract node $abs, with vtable vt, is DENSE_TAG, then each field is a pointer if
and only if the corresponding bit in the vtable’s mask field is 1:

     tag(vt)==DENSE_TAG ==> (∀T j.2<=j<numFields($abs)==>
       VFieldPtr($abs,j)==(j<30 && getBit(mask(vt),2+j)))

where mask looks up a 32-bit value from the vtable (in read-only memory), and tag and
getBit extract bits from words:
   fun mask(vt:int) { ro32(vt + ?VT_MASK) }
   fun tag(vt:int) { and(mask(vt), 15) }
   fun getBit(x:int,i:int) { 1 == and(shr(x, i), 1) }
The mutator-allocator interface specification uses the uninterpreted function VFieldPtr to
state which physical values are primitive values, and which are pointer values. The Value
function states the meaning of values in each of these two cases:
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                          33




   fun Value(isPtr,$r,v,$abs) {
       (isPtr && word(v) && gcAddrEx(v) && !word($abs)
                             && Pointer($r, v - 4, $abs))
   || (isPtr && word(v) && !gcAddrEx(v) && $abs == v)
   || (!isPtr && word(v) && $abs == v)
   }
For primitive data, the data’s abstract value equals its concrete value. Pointer data may
point to GC memory, under the collector’s control, or they may point outside GC memory,
in which case the collector treats them the same as primitive values. The “- 4” in the
Pointer specification converts a pointer to a header word into a pointer to the beginning of
the object (the pre-header).
     Interior pointers are defined like the ordinary pointers shown above, but may have
offsets larger than 4, which forces the collector to search for the beginning of the object.
The mark-sweep collector already has a table of colors, so it simply searches backwards
from the interior pointer to find the first word whose color isn’t unallocated. We also had
to add an analogous bit map to the copying collector, with one bit per heap word, solely
for the purpose of handling interior pointers. (On the bright side, these bit maps did give
us a chance to exercise Z3’s bit vector support.)
     Before we added support for Bartok’s memory model, the trusted mutator-allocator
specification was fairly short and readable. After adding Bartok’s memory model, the
specification ballooned to hundreds of lines of bit-level details. At this point, we started to
wonder if the specification itself had bugs. We used two techniques to test the specification.
First, we used Boogie’s “smoke” feature, which attempts to prove false at various points in
the program. This did not turn up any bugs. Second, we hand-translated the specification
into C# code, and then added run-time assertions to the original Bartok garbage collectors
based on this C# code. We saw many assertion violations, which led us to 5 specification
bugs, ranging from mundane (forgetting to multiply by 4 to convert a word address to a
byte address) to subtle (forgetting that Bartok compresses the sorted return address tables
by omitting any entry whose descriptor is identical to the previous entry).

7.4. Example: The CopyAndForward Procedure. As a larger example, Figures 15-16
show a complete excerpt from the realistic verified copying collector: the CopyAndForward
procedure, which copies an object from from-space to to-space. (This procedure corresponds
to the portion of the miniature copying collector’s forwardFromspacePtr procedure that
copies an object from from-space to to-space, after determining that the object hasn’t al-
ready been forwarded.) In addition, the right-hand side of Figures 15-16 shows the generated
MASM-compatible x86 code generated by our BoogiePL-to-x86 translation tool.
     The CopyAndForward procedure is implemented using the control, arithmetic, and mem-
ory constructs described in subsection 7.2: if, goto, call, AddChecked, Sub, etc. There’s
one slight embellishment in the implementation: the x86-like subset of BoogiePL distin-
guishes between the read-only memory that describes Bartok-generated GC tables, the
read-write stack memory that the mutator controls, and the read-write heap memory that
the garbage collector controls. The variable $GcMem represents the last of these, and the
garbage collector uses GcLoad and GcStore operations to read and write $GcMem. The
translator turns GcLoad and GcStore into x86 mov instructions, as seen on the right-hand
side of Figures 15-16.
34                             C. HAWBLITZEL AND E. PETRANK




      The CopyAndForward procedure relies on several helper procedures, also written in
BoogiePL and verified using Boogie/Z3 (and all available in the public source release). The
GetSize procedure accepts a pointer in register ecx to an object with vtable edx, and
computes the size of the object. (This is complicated in general, because the object may be
a non-index type, a string, or a single- or multi-dimensional array.) The inline procedure
copyWord copies a single field, with field index edi, from from-space object ecx to to-space
object esi. (We split this into a separate procedure, because the verification time of the
separate procedures was lower than the verification time of a single, combined procedure.)
Finally, the inline procedure bb4SetBit sets a single bit, at position esi, in a bit-vector at
address edi. (The bit vector consists of an array of 4-byte words, each containing 32 bits
of the bit vector.) Note that the translator inlines the code from copyWord and bb4SetBit
directly into the code for CopyAndForward, as seen on the right-hand side of Figures 15-16.
      The miniature collectors used a trigger T in quantifiers to guide quantifier instantiation.
To reduce unnecessary quantifier instantiation, the realistic collector implementation uses
seperate triggers for separate purposes: TV is used for general-purpose values, including
pointers, while TO is used for field indices.
      The preconditions to CopyAndForward specify the following:
• The ecx register contains a pointer $ptr, which is a valid pointer to a from-space object.
• The copying collector’s overall invariant CopyGcInv on GC memory holds. (This invariant
   is like the GcInv invariant in the miniature copying collector, although it deals with more
   complexities than the miniature collector. For example, the object at address Tj, the
   head of the scan queue, may be in the middle of being scanned as CopyAndForward runs.
   The CopyGcInv keeps track of both the beginning of this head object, Tj, and the end of
   the head object, $_tj.)
• The from-space object has not been forwarded (!IsFwdPtr(...)). Note that unlike the
   miniature copying collector, the real collector stores the forwarding pointer in the header
   field of a from-space object after the from-space object is copied, overwriting the vtable
   (virtual method table) pointer in the header. (The collector can distinguish a vtable
   pointer from a forwarding pointer, because vtables do not live in to-space.) Also note
   that the header field follows the pre-header field, so it lives at address $ptr + 4 rather
   than $ptr.
• The object has been reached. (This is used to prove that all copied objects were reached
   during the collection, so that non-reached objects are actually collected.)
      To copy an object, CopyAndForward first loads the vtable from the object’s header and
calls GetSize to get the size of the object, which it places in ebp. It then reserves space for
the copied object in to-space, by adding ebp bytes to the to-space scan queue tail Tk and
checking that this addition causes neither a 32-bit integer overflow nor an overflow past the
to-space limit Tl. (With additional effort, we could probably prove that enough space will
always be available in to-space, but the run-time cost of checking for space is small.)
      After reserving memory in to-space, CopyAndForward enters a loop that copies each
field edi of the object. The “assert” statements after the loop label specify the loop
invariants. (For conciseness, Figure 16 omits most of the loop invariants, which are similar
to CopyAndForward’s postconditions, but longer.)
      After copying the object, CopyAndForward overwrites the old from-space object’s vtable
with a forwarding pointer to the new to-space object. (Note that the x86 load-effective-
address instruction lea simply computes an address.) Next, CopyAndForward sets a bit in
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                         35




                            BoogiePL code          x86          Time to
                            (non-comment,      instructions      verify
                            non-blank lines) (before inlining) (seconds)
               Trusted defs       546
               Shared code        779              177             12
               Copying           2398              802            115
               Mark-sweep        3038              865             70

                     Table 1: Verification times for practical collectors

the GC bit vector to indicate the start of an object, so that the collector can later find the
start of the object from an interior pointer. Finally, CopyAndForward updates the ghost
variables $r2 and $toAbs and returns.
    At the end of CopyAndForward, the postconditions guarantee that:
• The overall invariant CopyGcInv still holds
• The new $r2 is a valid extension of the old $r2
• The return value, eax, is a valid pointer to a to-space object. Furthermore, the fields of
  the object point back to from-space. (In region terminology, the object points from the
  to-space region $r2 to the from-space region $r1.)
• The to-space scan queue grows at the tail (Tk), but remains the same at the head (Tj).
• The object at the head of the to-space queue (Tj) is unmodified.
• The to-space object pointed to by eax is actually located in the to-space memory area
  Ti...Tl.


                                     8. Performance
     This section presents performance results, measured on a single core of a 4-core, 2.4GHz
Intel Core2 with 4GB of RAM, 4MB of L2 cache, and a 64KB L1 cache.
     Verifying the copying collector, mark-sweep collector, and the code shared between the
collectors took 115 seconds, 70 seconds, and 12 seconds, respectively (see Table 1). This fast
verification reflects our choice of a simple trigger T(i). The copying collector and mark-
sweep collector contained 802 x86 instructions (before inlining) and 865 x86 instructions
(before inlining), plus 177 x86 instructions (before inlining) shared between the collectors.
The BoogiePL files for the copying and mark-sweep collectors contained 2398 non-comment,
non-blank lines and 3038 non-comment, non-blank lines, plus 779 non-comment, non-blank
lines of BoogiePL code shared between the collectors. Thus, there are about 2-3 lines of
annotation per x86 instruction. These annotations require a non-trivial amount of human
effort to write, but the effort is not too much greater than the effort spent in ordinary
development and testing. The trusted definitions, including x86 instruction specifications
and the Bartok interface specification, occupied 546 non-blank, non-comment lines.
     Figure 17 shows the performance of the 10 benchmarks cited in Section 7 as a function of
heap size, both for our verified memory managers and for Bartok’s native run-time system.
We denote the verified copying collector by vc, the verified mark-sweep collector by vms,
the generational copying Bartok collector by gen, and the Bartok standard mark-sweep col-
lector by ms. These results demonstrate that (a) our collectors work on real benchmarks,
and (b) the space and time consumption is in the same ballpark as Bartok’s native run-time
  36                         C. HAWBLITZEL AND E. PETRANK




procedure CopyAndForward($ptr, $_tj)
  requires ecx == $ptr;
  requires CopyGcInv(...);
  requires Pointer($r1, $ptr, $r1[$ptr]) && TV($ptr);
  requires !IsFwdPtr($GcMem[$ptr + 4]);
  requires $_tj <= Tk;
  requires reached($toAbs[$ptr], $Time);
  modifies $r2, $GcMem, $toAbs, Tk, $gcSlice;
  modifies eax, ebx, ecx, edx, esi, edi, ebp, esp;
  ensures CopyGcInv(...);
  ensures RExtend(old($r2), $r2);
  ensures Pointer($r2, eax, $r1[$ptr]);
  ensures Tj == old(Tj);
  ensures Tk >= old(Tk);
  ensures old($toAbs)[Tj] != NO_ABS ==>
             $toAbs[Tj] != NO_ABS && $toAbs[Tj] == old($toAbs)[Tj];
  ensures (forall j::{TO(j)} TO(j) ==>
              0 <= j && Tj + 4 * j < $_tj ==>
                 $GcMem[Tj + 4 * j] == old($GcMem)[Tj + 4 * j] && ...;
  ensures Ti <= eax && eax < Tk && gcAddrEx(eax + 4);
{
  var tmp;

  call edx := GcLoad(ecx + 4);                  =⇒ mov edx,dword ptr [ecx+4]
  esp := esp - 4; call GetSize($ptr, ...);      =⇒ call ?GetSize
  ebp := eax;                                   =⇒ mov ebp,eax
  assert TO(numFields($r1[$ptr]));

  esi := Tk;                                    =⇒ mov esi,dword ptr $$Tk
  call Tk := AddChecked(Tk, ebp);               =⇒ add dword ptr $$Tk,ebp
                                                   jc overflowed
  assert TV(esi);

  eax := Tl;                                    =⇒ mov eax,dword ptr $$Tl
  if (Tk <= eax) { goto skip1; }                =⇒ cmp dword ptr $$Tk,eax
                                                   jbe CopyAndForward$skip1
    // out of memory
    call DebugBreak();                          =⇒ int 3
  skip1:                                        =⇒ CopyAndForward$skip1:

  edi := 0;                                     =⇒ mov edi,0
  edx := 0;                                     =⇒ mov edx,0

              Figure 15: Realistic Copying Collector: forwarding, part 1/2.
               AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS          37




    loop:                                      =⇒ CopyAndForward$loop:
        // loop invariants:
        assert 4 * edi == edx;
        assert TO(edi) && 0 <= edi && edi <= numFields($r1[$ptr]);
        assert CopyGcInv(...);
        assert RExtend(old($r2), $r2);
        ...
      if (edx >= ebp) { goto loopEnd; }       =⇒ cmp edx,ebp
                                                  jae CopyAndForward$loopEnd
      // copy one field:
      call copyWord($ptr,$_tj,esi,edi,ebp);   =⇒ mov eax,dword ptr [ecx+4*edi]
                                                  mov dword ptr [esi+4*edi],eax
      call edi := Add(edi, 1);                =⇒ add edi,1
      call edx := Add(edx, 4);                =⇒ add edx,4
      goto loop;                              =⇒ jmp CopyAndForward$loop
    loopEnd:                                  =⇒ CopyAndForward$loopEnd:

    // set forwarding pointer:
    call eax := Lea(esi + 4);                  =⇒ lea eax,dword ptr [esi+4]
    call GcStore(ecx + 4, eax);                =⇒ mov dword ptr [ecx+4],eax
    eax := esi;                                =⇒ mov eax,esi
    // set bit in table:
    call esi := Sub(esi, Ti);                   =⇒ sub esi,dword ptr $$Ti
    edi := BT;                                  =⇒ mov edi,dword ptr $$BT
    call bb4SetBit(...);                        =⇒ mov ecx,esi
                                                   shr esi,7
                                                   shr ecx,2
                                                   add esi,esi
                                                   add esi,esi
                                                   add esi,edi
                                                   and ecx,31
                                                   mov edi,1
                                                   shl edi,cl
                                                   mov ecx,edi
                                                   mov edi,dword ptr [esi]
                                                   or edi,ecx
                                                   mov dword ptr [esi],edi
    $r2[eax] := $r1[$ptr];
    $toAbs[eax] := $toAbs[$ptr];
    $toAbs[$ptr] := NO_ABS;
    assert TO(1);
    assert TV(eax - Ti);

    esp := esp + 4; return;                      =⇒ ret
}

               Figure 16: Realistic Copying Collector: forwarding, part 2/2.
38                                                  C. HAWBLITZEL AND E. PETRANK




 4.4                    VC      VMS      GEN        MS                     30
                                                                                                                                                  VC
 4.2                                                                       25
                                                                                                                                                  VMS
                                                                           20
     4                                                                                                                                            GEN
                                                                           15
 3.8                                                                                                                                              MS
                                                                           10
 3.6                                                                           5
 3.4                                                                           0
         0     200            400            600          800      1000            0     500       1000       1500          2000        2500     3000

                             (a) Othello                                                                    (b) Ahc

 80                                                                        60                      VC       VMS      GEN       MS
                                                                    VC
 60                                                                 VMS    50
                                                                    GEN
 40                                                                        40
                                                                    MS
 20                                                                        30

     0                                                                     20
         0    1000           2000            3000         4000     5000            0    2000       4000       6000         8000     10000        12000


                                (c) Go                                                                    (d) Xlisp

 4.5                                                                       7
                                                                    VC                                                                            VC
                                                                           6
                                                                    VMS                                                                           VMS
     4                                                                     5
                                                                    GEN                                                                           GEN
                                                                           4
                                                                    MS                                                                            MS
 3.5                                                                       3
                                                                           2
     3                                                                     1
         0       5000                10000          15000         20000     2000        7000      12000      17000         22000    27000        32000


                              (e) Crafty                                                                  (f) Zinger

 11                     VC      VMS      GEN        MS                     1.8                     VC       VMS      GEN      MS
                                                                           1.6
     9                                                                     1.4
                                                                           1.2
     7
                                                                             1
     5                                                                     0.8
                                                                           0.6
     3                                                                     0.4
         0    20000          40000       60000           80000    100000           0           50000         100000            150000           200000


                                (g) Sat                                                                   (h) Asmlc

     6                  VC      VMS      GEN        MS                     250                     VC       VMS      GEN      MS
 5.5
                                                                           200
     5
 4.5                                                                       150
     4
                                                                           100
 3.5
     3                                                                      50
     300000           800000                  1300000            1800000       300000              800000              1300000                 1800000


                               (i) Lcsc                                                                   (j) Bartok


Figure 17: Performance Comparisons: overall running time (in seconds) vs. heap size (KB)
             AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                          39




system. We emphasize the “ballpark” nature of the comparison between the verified collec-
tors and the native Bartok collectors, because this comparison is highly unfair to the native
collectors, which support more features than the verified collectors. In particular, Bartok’s
native run-time system supports multithreading, which adds synchronization overhead to
the mutator and memory manager.
      Bartok’s native collectors were not designed to be used with a fixed heap size; they
expect to grow the heap as needed. To get a time vs. space plot for the Bartok collectors,
we varied the triggering mechanism used for heap growth, and then measured the actual
heap space used. For the generational collector, we set the nursery size to 4MB or 1/4 of
the maximum heap size, whichever was smaller.
      Several benchmarks created fragmentation that made it difficult for the verified mark-
sweep collector to find space for very large objects. The standard Bartok mark-sweep
collector simply grows the heap when the current heap lacks space for a very large object;
we configured the verified mark-sweep collector to set aside part of the heap as a wilderness
area, used as a last resort for very large object allocation. While this wilderness area
enabled these benchmarks to keep running under heavy fragmentation, the performance
still suffered, as seen in figures 17(f), 17(g), and 17(j). For other benchmarks, though, the
verified mark-sweep collector performed well across a large spectrum of heap sizes. The
verified copying collector, as expected, required a larger minimum heap size, but performed
asymptotically well as the heap size increased.

                                       9. Conclusion
     We have presented two simple collectors with the minimal set of properties required to
make them reasonably efficient in a practical setting. We have mechanically verified that
these collectors maintain a heap representation that is faithful to a mutator-defined abstract
heap, and have run the collector on large, off-the-shelf C# benchmarks.
     Given the large size of the mutator-allocator specification, we were very curious to see
whether our collectors would run correctly the first time. Alas, running the verified copying
collector revealed two specification bugs that we hadn’t caught before: Initialize’s post-
condition forgot to ensure that the ebp register was saved, and the allocation postcondition
specified a return value that was off by 4 bytes (a header/pre-header confusion). Thus, the
copying collector ran correctly the third time we tried it, which is still no small achievement
for a garbage collector hand-coded in assembly language. Furthermore, we were then able to
verify the mark-sweep collector against the debugged specification, so that the mark-sweep
collector ran correctly the first time we tried it. In addition, having a clear and well-tested
specification is useful for TAL/PCC verifiers: based on the specification, we found a bug
in our TAL verifier [CHP+ 08], which didn’t check that the sparse pointer tracking formats
mention no field more than once; this bug can allow TAL code to crash when linked to
Bartok’s native sliding/compacting collector.
     The fast verification times give us hope that there is still room to grow to support
more features and better GC algorithms. In particular, multithreading and pinning are
essential for many applications and libraries. Pinning should be easy for the mark-sweep
collector, but would complicate the copying collector: pinned objects fragment the heap,
forcing the allocator to allocate from a non-contiguous free space. Multithreading would
require reasoning about mutual exclusion (e.g. to keep allocators in different threads from
allocating the same memory simultaneously), reasoning about suspending mutator threads
40                                C. HAWBLITZEL AND E. PETRANK




during collection, and support for a more elaborate object pre-header word (for monitor
operations on objects). As the collectors grow, modularity becomes more important, so
we’re interested to see if the Boogie/Z3 approach can be combined with modular verification
approaches based on separation logic and/or higher-order logic; hopefully, the automation
provided by Boogie/Z3 will allow verification at a scale where modularity becomes essential.

Acknowledgments. The authors would like to thank Nikolaj Bjørner, Shaz Qadeer, Shu-
vendu Lahiri, Bjarne Steensgaard, Jeremy Condit, Juan Chen, Zhaozhong Ni, and the
anonymous reviewers for many helpful discussions, suggestions, and comments.

                                             References
[ALPP03]   Hezi Azatchi, Yossi Levanoni, Harel Paz, and Erez Petrank. An on-the-fly mark and sweep
           garbage collector based on sliding view. In OOPSLA’03 ACM Conference on Object-Oriented
           Systems, Languages and Applications, ACM SIGPLAN Notices, Anaheim, CA, November 2003.
           ACM Press.
[BBYG+ 05] Katherine Barabash, Ori Ben-Yitzhak, Irit Goft, Elliot K. Kolodner, Victor Leikehman, Yoav
           Ossia, Avi Owshanko, and Erez Petrank. A parallel, incremental, mostly concurrent garbage
           collector for servers. ACM Transactions on Programming Languages and Systems, 27(6):1097–
           1146, November 2005.
[BCD+ 05] Mike Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and K. Rustan M. Leino.
           Boogie: A modular reusable verifier for object-oriented programs. In Formal Methods for Com-
           ponents and Objects: 4th International Symposium, FMCO, 2005.
[BNR08]    Anindya Banerjee, David A. Naumann, and Stan Rosenberg. Regional logic for local reasoning
           about global invariants. In ECOOP, pages 387–411, 2008.
[Bor02]    Sam Borman. Sensible sanitation — understanding the IBM Java garbage collector, part 1:
           Object allocation. IBM developerWorks, August 2002.
[BTSR04] Lars Birkedal, Noah Torpe-Smith, and John C. Reynolds. Local reasoning about a copying
           garbage collector. In Conference Record of the Thirty-First Annual ACM Symposium on Prin-
           ciples of Programming Languages, number 39 (1) in ACM SIGPLAN Notices, pages 220–231,
           Venice, January 2004. ACM Press.
[Bur01]    L. Burdy. B vs. Coq to prove a garbage collector. In R. J. Boulton and P. B. Jackson, editors,
           Fourteenth International Conference on Theorem Proving in Higher Order Logics: Supplemental
           Proceedings, pages 85–97, September 2001. Report EDI–INF–RR–0046, Division of Informatics,
           University of Edinburgh.
[CGN03]    Solange Coupet-Grimal and Catherine Nouvet. Formal verification of an incremental garbage
           collector. The Journal of Logic and Computation, 13(6):815–833, 2003.
[Che70]    C. J. Cheney. A non-recursive list compacting algorithm. Communications of the ACM,
           13(11):677–8, November 1970.
[CHP+ 08] Juan Chen, Chris Hawblitzel, Frances Perry, Mike Emmi, Jeremy Condit, Derrick Coetzee,
           and Polyvios Pratikakis. Type-preserving compilation for large-scale optimizing object-oriented
           compilers. SIGPLAN Not., 43(6):183–192, 2008.
[DG94]     Damien Doligez and Georges Gonthier. Portable, unobtrusive garbage collection for multipro-
           cessor systems. In Conference Record of the Twenty-first Annual ACM Symposium on Principles
           of Programming Languages, ACM SIGPLAN Notices, Portland, OR, January 1994. ACM Press.
[DKP00]    Tamar Domani, Elliot Kolodner, and Erez Petrank. A generational on-the-fly garbage collector
           for Java. In Proceedings of SIGPLAN 2000 Conference on Programming Languages Design and
           Implementation, ACM SIGPLAN Notices, Vancouver, June 2000. ACM Press.
[DLM+ 76] Edsgar W. Dijkstra, Leslie Lamport, A. J. Martin, C. S. Scholten, and E. F. M. Steffens. On-
           the-fly garbage collection: An exercise in cooperation. In Lecture Notes in Computer Science,
           No. 46. Springer-Verlag, New York, 1976.
[dMB08a] Leonardo de Moura and Nikolaj Bjørner. Proofs and refutations, and z3. In 7th International
           Workshop on the Implementation of Logics, 2008.
               AUTOMATED VERIFICATION OF PRACTICAL GARBAGE COLLECTORS                                                          41




[dMB08b] Leonardo de Moura and Nikolaj Bjorner. Z3: An efficient smt solver. In Conference on Tools
         and Algorithms for the Construction and Analysis of Systems (TACAS), 2008.
[DNS05]  David Detlefs, Greg Nelson, and James B. Saxe. Simplify: a theorem prover for program
         checking. J. ACM, 52(3):365–473, 2005.
[GBB98]  Healfdene Goguen, Richard Brooksby, and Rod Burstall. An abstract formulation of memory
         management, December 1998. draft.
[GBT07]  Yeting Ge, Clark Barrett, and Cesare Tinelli. Solving quantified verification conditions using
         satisfiability modulo theories. In CADE, pages 167–182, 2007.
[GGH07]  H. Gao, J. F. Groote, and W. H. Hesselink. Lock-free parallel and concurrent garbage collection
         by mark&sweep. Sci. Comput. Program., 64(3):341–374, 2007.
[Gon96]  Georges Gonthier. Verifying the safety of a practical concurrent garbage collector. In R. Alur
         and T. Henzinger, editors, Computer Aided Verification CAV’96, Lecture Notes in Computer
         Science, New Brunswick, NJ, 1996. Springer-Verlag.
[Hav99]  Klaus Havelund. Mechanical verification of a garbage collector. In FMPPTA’99, 1999.
[Jac98]  Paul B. Jackson. Verifying a garbage collection algorithm. In Proceedings of 11th International
         Conference on Theorem Proving in Higher Order Logics TPHOLs’98, volume 1479 of Lecture
         Notes in Computer Science, pages 225–244, Canberra, September 1998. Springer-Verlag.
[KP06]   Haim Kermany and Erez Petrank. The Compressor: Concurrent, incremental and parallel
         compaction. In Proceedings of SIGPLAN 2006 Conference on Programming Languages Design
         and Implementation, ACM SIGPLAN Notices, pages 354–363, Ottawa, June 2006. ACM Press.
[LP06]   Yossi Levanoni and Erez Petrank. An on-the-fly reference counting garbage collector for Java.
         ACM Transactions on Programming Languages and Systems, 28(1), January 2006.
[McC60]  John McCarthy. Recursive functions of symbolic expressions and their computation by machine.
         Communications of the ACM, 3:184–195, 1960.
[Min63]  Marvin L. Minsky. A Lisp garbage collector algorithm using serial secondary storage. Technical
         Report Memo 58 (rev.), Project MAC, MIT, Cambridge, MA, December 1963.
[Mos09]  Michal Moskal. Programming with triggers. In SMT ’09: Proceedings of the 7th International
         Workshop on Satisfiability Modulo Theories, 2009.
[MSLL07] Andrew McCreight, Zhong Shao, Chunxiao Lin, and Long Li. A general framework for certifying
         garbage collectors and their mutators. In PLDI [PLD07].
[MSS01]  Stefan Monnier, Bratin Saha, and Zhong Shao. Principled scavenging. In PLDI [PLD01].
[MWCG98] Greg Morrisett, David Walker, Karl Crary, and Neal Glew. From System F to typed assembly
         language. In POPL ’98: 25th ACM Symposium on Principles of Programming Languages, pages
         85–97, January 1998.
[Nec97]  George Necula. Proof-Carrying Code. In ACM Symposium on Principles of Programming Lan-
         guages, pages 106–119. ACM Press, 1997.
[PLD01]  Proceedings of SIGPLAN 2001 Conference on Programming Languages Design and Implemen-
         tation, ACM SIGPLAN Notices, Snowbird, Utah, June 2001. ACM Press.
[PLD07]  Proceedings of SIGPLAN 2007 Conference on Programming Languages Design and Implemen-
         tation, ACM SIGPLAN Notices, San Diego, CA, June 2007. ACM Press.
[PPS08]  Filip Pizlo, Erez Petrank, and Bjarne Steensgaard. A study of concurrent real-time garbage
         collectors. In Proceedings of SIGPLAN 2008 Conference on Programming Languages Design
         and Implementation, ACM SIGPLAN Notices, pages 33–44, Tucson, AZ, June 2008. ACM
         Press.
[Rus94]  David M. Russinoff. A mechanically verified incremental garbage collector. Formal Aspects of
         Computing, 6:359–390, 1994.
[SMT08]  Satisfiability modulo theories competition (SMT-COMP). http://www.smtcomp.org/2008/,
         2008.
[VYBR07] Martin Vechev, Eran Yahav, David Bacon, and Noam Rinetzky. CGCExplorer: A semi-
         automated search procedure for provably correct concurrent collectors. In PLDI [PLD07].
[WA01]   Daniel C. Wang and Andrew W. Appel. Type-preserving garbage collectors. In PLDI [PLD01].
[Yic]    The YICES SMT solver. http://yices.csl.sri.com/tool-paper.pdf.




                                            This work is licensed under the Creative Commons Attribution-NoDerivs License. To view
                                            a copy of this license, visit http://creativecommons.org/licenses/by-nd/2.0/ or send a
                                            letter to Creative Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or
                                            Eisenacher Strasse 2, 10777 Berlin, Germany
