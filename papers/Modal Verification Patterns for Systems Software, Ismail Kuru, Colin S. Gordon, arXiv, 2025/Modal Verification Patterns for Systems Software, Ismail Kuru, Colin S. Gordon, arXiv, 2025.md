                                               Modal Verification Patterns for Systems Software
                                                                      Ismail Kuru                                                      Colin Gordon
                                                                   ik335@drexel.edu                                                  csg63@drexel.edu
                                                                   Drexel University                                                  Drexel University
                                                                 Philadelphia, PA, USA                                              Philadelphia, PA, USA

                                         Abstract                                                                  typically intricate and naturally error-prone, despite how
                                         Although they differ in the functionality they offer, low-level           critical its correctness is. Typically systems software has, as a
                                         systems exhibit certain patterns of design and utilization of             primary focus, the task of abstracting from hardware details
                                         computing resources. In this paper we examine how modali-                 to simplify the construction of higher layers of the stack.
                                         ties have emerged as a common structure in formal verifi-                    Interacting with computing resources is the essential point
arXiv:2506.01719v3 [cs.LO] 27 Sep 2025




                                         cation of low-level software, and explain how many recent                 which shapes the design of low-level systems software. Ex-
                                         examples naturally share common structure in the relation-                ploiting these design choices has been an important field
                                         ship between the modalities and software features they are                of study. This survey examines these common patterns in
                                         used to reason about. We explain how the concept of a re-                 systems software, and their relationships to modalities. We
                                         source context (a class of system resources to reason about)              believe that certain properties of modalities enable us to
                                         naturally corresponds to families of modal operators indexed              understand and address the verification challenges of these
                                         by system data, and how this naturally leads to using modal               systems by tailoring specification and proof to the same
                                         assertions to describe resource elements (data in the relevant            patterns used to design the systems.
                                         context).                                                                    Contributions We argue that modal abstractions can be
                                                                                                                   used to identify and abstract system verification challenges.
                                         CCS Concepts: • Theory of computation → Modal and                         We justify our perspective by discussing prior systems that
                                         temporal logics; Logic and verification; • Software and                   have successfully used modalities for system verification,
                                         its engineering → Operating systems.                                      arguing that they fit into the verification design pattern we
                                         Keywords: separation logic, modal logic, verification, oper-              articulate, and explaining how this approach might apply to
                                         ating systems                                                             other systems’ verification challenges.
                                         ACM Reference Format:                                                         • Identifying System Verification Challenges: We
                                         Ismail Kuru and Colin Gordon. 2025. Modal Verification Patterns for             start with identifying common patterns in system ver-
                                         Systems Software. In 13th Workshop on Programming Languages and                 ification: virtualization, sharing, and translation.
                                         Operating Systems (PLOS ’25), October 13–16, 2025, Seoul, Republic of
                                                                                                                       • Introducing Modal Resource Contexts: Then we dis-
                                         Korea. ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/
                                         3764860.3768337
                                                                                                                         cuss the concept of resource which has already been an
                                                                                                                         essential concept in the design of systems. Inspired by
                                         1    Introduction                                                               the concept of resource in systems, we define what a
                                                                                                                         resource and its context are in the modal abstractions.
                                         Although they differ in the functionality they offer, low-level
                                                                                                                         For example, the transaction abstraction, which be-
                                         systems exhibit certain patterns of design and utilization of
                                                                                                                         haves like a container for in-memory dirty disk pages,
                                         computing resources. Systems software, in general, inter-
                                                                                                                         can be considered a resource context for any dirty
                                         faces with an underlying computing substrate such that any
                                                                                                                         in-memory disk page resource associated with it.
                                         software system at any higher level in the software stack
                                                                                                                       • Introducing Nominals for System Resources: Ex-
                                         can (at least indirectly) utilize the resources of the machine.
                                                                                                                         isting logics for systems software must frequently
                                            The last layer of software before the hardware is naturally
                                                                                                                         identify individual resources within a given context —
                                         critical to the correctness of an overall system, as essentially
                                                                                                                         nominalization (in the sense of hybrid logic) enables
                                         all software built on top of it assumes its correctness. And
                                                                                                                         identifying a resource in its context. For example, a
                                         because hardware is complex and highly diverse, the imple-
                                                                                                                         filesystem transaction is a context of resources for in-
                                         mentation of those lowest layers of the software stack is
                                                                                                                         memory updated disk blocks which have not yet been
                                                                                                                         saved to disk. The transaction identifier is used to as-
                                                                                                                         sociate a transaction with a disk block to persist so
                                         This work is licensed under a Creative Commons Attribution 4.0 Interna-         that, in case of a crash while persisting updated disk-
                                         tional License.
                                         PLOS ’25, Seoul, Republic of Korea
                                                                                                                         blocks, the filesystem can rollback the already persisted
                                         © 2025 Copyright held by the owner/author(s).                                   disk-blocks of the transaction, and restore the previ-
                                         ACM ISBN 979-8-4007-2225-7/25/10                                                ous consistent disk state. We discuss other examples
                                         https://doi.org/10.1145/3764860.3768337                                         to contextualize the existing systems surveyed.
PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea                                                             Kuru and Gordon


      • Taxonomy of Current Modal Approaches in Sys-               point in the model identified by a chosen nominal. Tradi-
        tem Verification: Based on these concepts, we sum-         tionally @ℓ 𝜑 asserts that 𝜑 is true in the state identified by ℓ.
        marize contemporary verification efforts using modal       Conceptually, given our context, we might like 𝑙 to indicate
        abstractions. We choose them from different domains,       truth in a particular data structure ℓ. However, most prior
        for example, reasoning about weak memory models            work on hybrid logics works in classical logics rather than a
        and storage persistence [5–7, 9, 13, 14, 19, 34, 49, 50]   substructural setting like separation logic. Newer work [5–
        and using different programming logics such as Iris [29]   7, 9, 13, 14, 34, 49, 50]:w surveyed here adapts this idea to
        and Dafny [36] because we would like to justify that       deal with different structures specified in separation logic.
        our definitions are neither domain nor programming
                                                                       Nominalization. Some classes of assertions benefit specif-
        logic dependent.
                                                                   ically from naming the explicit conditions where they are
                                                                   true (as opposed to simply requiring them to be true some-
2     Background on Modal Logics for                               where or everywhere as in the most classic modal operators).
      Programs, and Low-Level Systems                              Because these named conditions strongly resemble the nom-
      Software                                                     inals of hybrid logic, we refer to the general idea of naming
This section briefly recalls related concepts from modal logic     circumstances explicitly as nominalization, even though not
of particular relevance to our taxonomy (Section 2.1), and         all of the examples we discuss are actually hybrid logics.
enough general background on the systems software con-                 An example use of state naming explicitly in the asser-
cepts organized by our taxonomy for the connections to             tion appears in program logics with usage protocols (e.g.
modalities to be clear (Section 2.2).                              state transition systems resembling typestate [16, 48], which
                                                                   ensure the operations applied to some data occur in a speci-
2.1    Hybrid Logic, Dynamic Logic, and Nominals in                fied order, and that invariants for various conceptual states
       Program Logics                                              of the data — such as a file being open or closed — are re-
                                                                   spected). Protocol assertions are annotated with the name
   Dynamic Logics as Program Logics. We believe that for           of the last (abstract) state at which the protocol is ensured.
the kinds of informal reasoning and the sorts of data struc-       A classic application of this idea to systems is Halpern et
tures discussed in the previous section, ideas from modal          al.’s work adapting modal logics of knowledge to deal with
logic are a promising approach to formalization and veri-          distributed systems [21, 22, 24]. In most of that line of work,
fication. Broadly speaking modal logics incorporate modal          K𝑎 (𝑃) indicates that the node 𝑎 in the system knows or pos-
operators, which take as arguments a proposition expected          sesses knowledge of 𝑃 (for example, a Raft node may “know” a
to be true in another time [41], place [1, 17–19, 37], circum-     lower bound on the commit index). Alternatively, a modality
stance or point-of-view [23, 26], and result in a proposition      @𝑖 (𝑃) may represent that 𝑃 is true of/at the specific node
true in the current time, place, or circumstance at which          𝑖 [19] (e.g., that node 𝑖 has physically stored a certain piece
the truth of the modal operator is being evaluated. Classic        of data to reliable storage). These permit capturing specific
examples include modal necessity □𝑃 describing that 𝑃 is           concepts relevant to the correctness (and reasoning about
necessarily true, G(𝑃) meaning 𝑃 is true globally (i.e., for-      correctness) of a certain class of systems, involving facts
ever from this time onwards in temporal logics), or 𝐾𝑖 (𝑃)         about specific named entities in the system.
describing that a particular participant 𝑖 knows that 𝑃 is true.
The latter is an example of multimodal logic, where there is          In each of these cases, the fact that these facts are described
an family of modalities (modal operators) parameterized by         using a modality 𝑀 with the core modal property that if
some dimension of interest (there, participants).                  𝑃 ⇒ 𝑄, then 𝑀 (𝑃) ⇒ 𝑀 (𝑄). This means, for example, that
   Dynamic logic [42], a (multi)modal logic variant of weakest     if a process 𝑝 knows that the commit index is greater than
preconditions [12? ? ] which works with modalities of the          5 (e.g., K𝑝 (commitIndex > 5)) no extra work is required to
form [𝑝] (𝑃), which states that in the current program state,      conclude that the node knows it is greater than 3 (i.e., that
if program 𝑝 is run then afterwards 𝑃 will hold (modulo            K𝑝 (commitIndex > 3)), because this follows from standard
non-termination).                                                  properties of modal operators as described above. In contrast,
                                                                   if verification instead used a custom assertion
   Hybrid Logic. Hybrid logics [1, 2, 4, 17, 18] are a class
of modal logics that add two primary new concepts to a                                  minCommitIndex(5)
logic. Nominals ℓ ∈ Loc uniquely identify points in a model        to represent the former knowledge, one would need to sepa-
(e.g., a particular state in the state space the logic is used     rately provide custom reasoning to conclude
to reason about), so there is exactly one point in the model
where a nominal Loc (as a formula) is true. Satisfaction op-                            minCommitIndex(3)
erators are modal operators indexed by nominals, which             As our survey shows, the value of the modal view (which
enable claims about the truth of another proposition at the        grants both intuitive specifications and natural reasoning
Modal Verification Patterns for Systems Software                                   PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea


principles) is becoming apparent in systems software verifi-
cation.

2.2   Virtualization in Systems Software
One of the most common forms of abstraction provided
by systems software is virtualization, which abstracts the
relationship between conceptual and physical computing
                                                                                Figure 1. x86-64 page table lookups.
resources. Upper-levels of the software stack work with these
conceptual — virtual — resources, while the lower levels
of systems software deal with the translation of requests           address aligned to 4KB (4096 byte) boundaries. An address
expressed in terms of virtual resources into operations on          translation requires traversal of a series of tables starting
physical resources.                                                 from level 4. The traversal ends in the level 1 page table
   Operating System (OS) kernels virtualize memory loca-            with the final lookup to the actual page of physical memory
tions and quantity (via virtual memory and paging [11]). Dis-       holding the requested data, and the low-order 12 bits being
tributed language runtimes may virtualize addresses, even           used to index into this page.
when processes may migrate across machines [28]. Filesys-              A page table tree is referred to as a (virtual) address space,
tems virtualize locations on disk [3, 27, 45, 46]. Programs         as it presents an abstraction of how different memory ad-
built on top of the corresponding systems software layer            dresses could be related in space. This functionality is used
work logically at the level of these virtualized resources, and     by operating systems to present fictional collocation or sepa-
it makes sense to specify the systems software directly in          ration of resources: a range of logically (virtually) contiguous
terms of those abstractions.                                        memory addresses may be translated to a range of physically
   Access by Translation. Accessing virtualized resources           disparate locations in actual memory. The address space then
via translation is a common way to virtualize notions of            acts as a kind of container for virtualized memory resources
location (e.g., virtual memory addresses, inodes or object          tied to that container.
IDs instead of disk addresses [3, 27, 45, 46]). B-trees, page          A typical OS manages multiple address spaces at once.
tables, and related structures both behave like maps, when          Each program is associated with a unique page table tree,
the corresponding physical resources exist as such just in          which is stored in a specific hardware register (cr3 in Fig-
a different location. Control over the lookup process (e.g,         ure 1). Using different mappings, which map only disjoint
handling the case of a missing translation entry) allows for        portions of physical memory in the map’s codomain, is how
additional flexibility, such as filling holes in sparse files, or   the OS ensures memory isolation between processes.
demand paging (both from disk or lazily populating anony-
                                                                    2.2.2 Virtualized Resources in Filesystems. Another
mous initially-zeroed mappings). Although the realization of
                                                                    important computer resource that is virtualized for access
these maps may differ from system to system based on the
                                                                    is disk blocks. Filesystems are software components that
context (and sometimes hardware details), they are semanti-
                                                                    abstract disk access on behalf of normal programs Similar to
cally — logically — partial maps, worth treating as such in
                                                                    how VMMs using page table trees to fabricate more memory
verification.
                                                                    addresses than what actually exists, filesystems use indexing
2.2.1 Virtualization of Memory Locations. A typical                 maps for fabricating more virtual disk page addresses which
general purpose computer virtualizes memory resources in            are conventionally called disk pages, to be distinguished from
RAM. A program asking for a memory unit from an operat-             physical disk block addresses. When a regular program ac-
ing system kernel is served with a memory address that is           cesses a file, it requests a specific logical offset from the start
virtualized such that it may be mapped to a physical RAM            of that file’s contents. As with virtual memory, the filesystem
location or not. As our informal definition suggests, the com-      may map adjacent logical blocks of a single file to physically
mon technique for virtualization of memory locations in OS          disparate parts of the disk (or even to different disks), though
kernels relies on translating (mapping) virtual addresses into      this translation mapping is implemented entirely in software
physical ones. The conceptual address translation map is            (as opposed to the hardware cooperation that exists for mem-
implemented with processor’s page table trees as shown in           ory virtualization).
Figure 1. In this Figure, we see a typical 4 levels of page ta-        Filesystems not only handle the address translation from
bles, a virtual address on the top indexing into the different      a disk-page to a disk-block but also need to handle different
levels of the page table tree (the larger rectangles along the      modes of computing where to find disk resources: a disk block
bottom are blocks of memory which serve as nodes of the             may live on a disk in stable storage, or the most up-to-date
tree along a particular lookup path). Fabrication of virtual        version of a block may live only in memory (for the filesystem
addresses out of limited physical addresses is provided with        to write to disk at a later time, batched for efficiency). To
entries in the page table tree where each points to a physical      handle the consistency of the disk resources in different
PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea                                                                      Kuru and Gordon


modes of execution, filesystems employ different policies            is decremented.1 These reference counts are a sound (but
when indexing the disk resource. Which data-structure is             incomplete) way to approximate reachability: if a decrement
going to be used to implement address translation from disk-         of a reference count decrements the count to 0, no other
pages to disk-blocks? What is going to be the update policy to       references to that memory exist in the program, and the
the indexing map implementing address translation, which             memory can be reclaimed.
defines the consistency policy for the disk resources? Different        Reasoning about the correctness of such code requires
filesystem implementations give different answers to these           reasoning about these reachability relations and reference
questions.                                                           counts, relative to specific stack frames.
   While exceptions exist [3, 27, 45, 46], most filesystems will
                                                                     2.2.4 Weak Memory Models. Multicore and multiproces-
continue to store a given block of a given file in the same
                                                                     sor systems do not directly write every memory update back
physical disk block for as long as the file exists. These filesys-
                                                                     to memory (or even a coherent hardware cache) individually,
tems with in-place updates need to implement some form of
                                                                     as this would be extremely slow. Instead, they effectively
journalling [8, 20] to ensure that a crash partway through an
                                                                     buffer reads and writes to and from memory locally within
in-place update can be rolled back using an undo journal that
                                                                     each CPU core [40]2 so that operations can be partially re-
records the original contents before in-place modification
                                                                     ordered and batched to improve performance. For most code
(so original contents could be restored after a crash) or com-
                                                                     — where the different CPUs are doing independent work —
pleted using a write-ahead journal that first writes new data
                                                                     this is transparent to software. But fine-grained concurrent
in unused space before also updating in place (so the journal
                                                                     systems code which has multiple CPU cores simultaneously
entries could be re-applied after a crash). Because disk blocks
                                                                     coordinating access to shared memory must reason about
associated with a file could now be in many states (on-disk,
                                                                     these (effective) bufferings and reorderings, whose details
journaled but not updated in place, or both) the specification
                                                                     vary across CPU architectures.
of these systems is complex. And because some states are
                                                                        Most of this coordination comes through reasoning about
only possible after a system failure, each line of filesystem
                                                                     what will be true after local operations are published to mem-
code has two conceptual post-conditions: one referring to
                                                                     ory, or what will be true after remote operations become visible
the successfully stored disk pages from a disk page container
                                                                     locally [10, 13, 47]. Each of these flavors of contingent rea-
(e.g, a disk tree) , which can be uniquely identified by the
                                                                     soning depend on use of certain fence or memory barrier
last successful commit identifer (e.g., a transaction identifier
                                                                     operations, which block execution of a CPU until either all
or snapshot identifier), as the current view of the disk in
                                                                     incoming or outgoing memory transactions are complete.
the specification for continued execution, and one referring
to the previous view of the disk in the specification for the        2.2.5 Actor Model. An alternative approach to addressing
stable state established in the event of a hardware failure          the shared memory concurrency complication, i.e., data races,
immediately after that operation.                                    is to use actors [25? ] by eliminating shared mutable state
                                                                     and enforcing updates on exclusive local mutable state via
                                                                     exchanging immutable messages among processes. This is a
2.2.3 Reference Counting Memory Reclamation. It is                   way of sequentializing the concurrent interleaved execution.
safe to reclaim memory (for later reuse) when that memory            Often correctness of one actor depends on knowledge about
allocation will no longer be used by the client program. Since       other actors. In a typical consensus algorithm, for example,
that property itself is undecidable, sound heuristics are used       an operation is committed if a quorum of nodes reach an
instead. A common proxy for the program never accessing              agreement on it.
an allocation again is to check that there is no access path            Therefore, as expected, the specification of an actor in
from data a program can trivially access (e.g., local variables      the current view would refer to the other actors’ states and
stored on the stack) to a memory allocation — that is, when          has to validate that the shared knowledge amongst actors is
the allocation is no longer reachable. In that case the program      preserved [19].
cannot access the memory again, so the memory location
can be reclaimed soundly — i.e., without violating any access        3    Contingency Decomposition of a System
through a reference to it.                                           In this section, we argue the position that modalities should
   To reclaim the allocated memory location that is no longer        be a go-to approach when specifying and verifying low-level
being accessed, many systems use a well-known method                 systems code. We explain how the concept of a resource con-
called reference counting in which each memory allocation            text helps guide the design of new modalities for verification
includes not only its data but also a counter of how many            of systems code, and we justify our perspective by discussing
pointers to that memory exist in the rest of the program. Any        1 This may be done using library functions for a reference counting system,
time a new reference to the allocated memory is created, the         or the operations may be inserted by a compiler.
counter is incremented, and every time an existing refer-            2 This is a layer below the better-known L1 cache, which is coherent across

ence is destroyed (by overwriting or dropping) the counter           all CPUs in the system.
Modal Verification Patterns for Systems Software                                     PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea


prior systems that have used modalities for systems verifica-         modalities in the literature [44]. These modalities are typi-
tion successfully, arguing that they fit into the verification        cally multi-modal, with a form of roughly 𝑀 𝑐𝑡𝑥𝑡 𝜙 ≜ . . . →
design pattern we articulate, and explaining how this ap-             𝜙 𝑐𝑡𝑥𝑡, such that the evaluation of the modality incorporates
proach might apply to other systems verification challenges.          the 𝑐𝑡𝑥𝑡 arguments into the evaluation of 𝜙.
   To explain our ideas in the general systems understanding,
we briefly recap some of the background and themes our                   Shallow Modalities in Separation Logic. In a substruc-
ideas build on again, casting them in a certain way to bring          tural setting [32, 43] the implication → is typically replaced
out the relevance of our philosophy.                                  with substructural implication −∗. This definition also reveals
                                                                      a subtlety about the denotation of assertions 𝜙 — they are
                                                                      effectively predicates of some kind, functions from some pos-
3.1   Encoding Modalities in Program Logics
                                                                      sible world into some logical algebra such as a BI-algebra [39].
Program logics which would like to enjoy modal propositions           Taking this interpretation literally gives rise to a convenient
need to have an underlying model that allows encoding of              way to embed new modalities in Iris in a way well-suited
the propositions. A Kripke model can be roughly seen as a             to many use cases. If 𝐵 is a type with a BI-algebra struc-
triple of set of worlds (e.g., program states), a binary relation     ture, then any space of predicate functions (e.g., val → 𝐵
between worlds (e.g., transition relations between states) and        as a simplification) also carries a BI-algebra structure, lifted
a state interpretation function. For a modality 𝑀, 𝑀 (𝜙) is           from 𝐵, often called the pointwise lifting of the algebra. A
true in one state/world 𝑤 if states related to 𝑤 by the binary        number of projects for systems software verification [5–
relation satisfy 𝑃. Whether this is all related states, or just       7, 9, 13, 14, 34, 49, 50] now take advantage of this, explicitly
one, or something else varies depending on what 𝑀 is meant            or implicitly lifting the BI-algebra structure from Iris itself to
to model, but the modality is always tied to the relation of          Iris predicates used as assertions within modalities. Connect-
interest. For multimodal logics there are multiple relations.         ing this to Iris’s typeclasses for interactive proofs [31, 33]
For example, for Dynamic Logic, there is a modality for each          then permits working within the embedded logic just as if
program, and the relation for running program “command”               working in Iris.
(in old program logic parlance) 𝐶 is the relationship between            In addition, the modal definitions themselves may repre-
states before and after executing 𝐶.                                  sent ownership of resources in a substructural setting [15, 30,
                                                                      43]. This allows modalities to simultaneously represent own-
   Encoding Hoare Triples. Following Pratt’s original rep-            ership of certain resources used for interpreting the modality
resentation [42], we can encode a Hoare triple {𝑃 }𝐶{𝑄 }              itself, as well as whatever resource ownership is implied by
(asserting that if 𝑃 holds in some state, then executing 𝐶 will       the modal argument.
yield a state where 𝑄 holds) as 𝑃 → [𝐶] (𝑄). However, for
this to hold for a specific programming language and asser-           3.2   Decomposing a System into its Constituents
tion language, the modal representation requires a semantics                Contingently
in terms of an underlying model.
                                                                      Many existing program logics for system verifications have
   Conventionally, a Kripke model with its constituent must
                                                                      a common structure, which maps to modalities with a couple
be picked. Gordon provides a Kripke model for an actor-
                                                                      extra dimensions of design. We summarize our discussion of
based hybrid modal logic [19], in which the transition re-
                                                                      these logics in Table 1. We discuss, based on examples, com-
lation is indexed by a particular command and a particular
                                                                      mon aspects of how we intuitively think about correctness
actor, relating pre- and post-states of a specific actor refer-
                                                                      of systems code in many contexts, articulate those pieces,
enced by a nominal executing the command. Gordon encodes
                                                                      and call out the commonalities across a range of systems.
this hybrid logic as a library in the Dafny program logic [36]
with the help of two state invariants and rely-guarantee as-
sertions checking the stability of invariants. Wagner et al.          3.3   Resource
take a similar approach to the design of their separation logic       Consider first the address space abstraction in an OS ker-
and utilize a Kripke model for reference-counted memory               nel. An address space of a process is a container of virtual
reasoning principles [50].                                            addresses referencing data in memory. One would expect
   On the other hand, program logics such as Iris [29] utilizes       to have points-to assertions from separation logic to specify
Kripke models for their separation algebras (a collection of          ownership of a memory reference pointing to some data. In
CMRAs as an algebraic cousin of a BI-algebra [39]), modeling          the classic setting [? ], such a points-to assertion 𝑥 ↦→ 𝑣 as-
modalities for both heap extension and step indexing [38].            serts ownership of memory location 𝑥, and that the contents
However in general, many modalities can be given proof-               of that memory location are 𝑣. But that ownership is relative
theoretic semantics directly within a logic. This is the case         to a specific address space — a specific container. We tend
for Iris’s weakest precondition modality (which is defined            to think directly about what is true in an address space, with
within the Iris logic itself), as well as for a wide range of other   the simplest piece being an association between a virtual
PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea                                                                      Kuru and Gordon


                                            Table 1. Modal Decomposition of Program-Logics.

                Modality                        Context      Elements         Nominalization    Context Steps
                                                                  𝛾
               Post-Crash [5–7]                   ^𝑃         ℓ ↦→𝑛 𝑣              Strong        Crash Recovery
                                                  𝑡
               NextGen [49]                      ↩→ 𝑃       Own (t(a))            Strong        Determined Based on the
                                                                                                Model∗
                                                𝐼𝐶𝑢𝑡 𝑛
               StackRegion∗ [49]                ↩→ 𝑃         n ℓ ↦→ 𝑣             Strong    Alloc and Return to/from stack
               Actor [19]                        @𝜄 P     Variable values         Weak      Send Message
               Memory-Fence [9, 13, 14]       △𝜋 and ▽𝜋       ℓ ↦→ 𝑣              Weak      Fence Acquire and Release
               Address Space [34]                [r]P         ℓ ↦→ 𝑣              Weak      Address Space Switch
               Ref-Count [50]                    @ℓ P         ℓ1 ↦→ 𝑣             Weak      Allocating, Dropping and Shar-
                                                                                            ing a Reference
                      *The StackRegion Modality is an instance of NextGen (called the Independence Modality in [49]).


address and the data it points to. We call the simplest piece,              requires having the resource elements loaded into the mem-
in this and other examples, the resource element:                           ory
Definition 3.1 (Resource Elements). The simplest atomic                                            𝑃 ≜ ℓ1 ↦→ 𝑣...
facts we want to work with in a particular setting, specific                to be in the resource context of the address space modal-
to that setting.                                                            ity with the root 𝑟 1, and, once the new address space is
   By definition, the resource elements are specific to some                loaded—i.e., cr3 is loaded with the other address space root
limited domain or setting. For example, knowing that a cer-                 address—the resource elements (𝑄) that were loaded in the
tain address points to a 32-bit signed integer representing 3               previous view of the memory are now introduced to the
is knowledge restricted to a certain address space. In general,             resource context with the root 𝑟 2.
we call these domains that any resource element is tied to                     Weak-Memory. When considering weak memory models,
resource contexts:                                                          we consider address-value mappings of thread-local views in
Definition 3.2 (Resource Context). A resource context is                    C11 memory model [35]). Modalities Δ𝜋 (𝑃) and ∇𝜋 (𝑃) with
an abstraction, context, or container of resource elements of               𝑃 represent the memory address-value mappings that held
the same type, e.g., an address space of a process.                         before or will hold after certain memory fence operations by
                                                                            thread 𝜋. The elements are points-to assertions, each specific
   We discuss a range of examples for each of these in turn.                to views of memory after those fence operations.
   Table 1 gives additional examples of systems and their
corresponding resource elements and contexts where these                       Reference Counting. When dealing with reference count-
elements reside, though none of the work in that table ana-                 ing APIs, we may care to specify reachability of memory
lyzes itself according to the structure we are giving.                      nodes (ℓ ↦→ 𝑣) in a certain context defined by a shared root
   Except for the Post-Crash-Modality, one can think of the                 address. A shared memory address ℓ can be the root of the
resource contexts in the first column in Table 1 as contain-                graph (@ℓ (ℓ1 ↦→ 𝑣 1 ∗ ... ∗ ℓ 𝑗 ↦→ 𝑣 𝑗 )) that can be a container
ers for the corresponding resource elements in the second                   of memory nodes (ℓ1 ↦→ 𝑣) that are reachable from the root
column.                                                                     ℓ.
   Stack Regions. When reasoning about stack frame con-                        Actors. When specifying the consistency of an actor in
tents, the resource element would be a stack-memory points-                 the current view, we need to refer to other actors’ state:
to assertion ( n ℓ ↦→ 𝑣) indicating that a certain offset into              @𝜄 (𝑃) asserts that 𝑃 is true in the actor referenced actor ID
stack region 𝑛 holds value 𝑣. The regions (frames) themselves               𝜄. Assertions may mention local variables and state at the
are the contexts.                                                           designated actor by name, so the interpretation of variables
   Virtual Memory. For virtual memory management, a                         in assertions depends on which actor the assertion applies
virtual-points-to, ℓ ↦→ 𝑣, is an ownership assertion pairing a              to.
virtual address (ℓ) with data (𝑣) in an address space, which is                Post-Crash. The resource element of Post-Crash Modal-
a resource context for virtual address mappings, ℓ ↦→ 𝑣, and                ity is not obvious in Table 1, and needs a bit of explanation.
uniquely identified with a root address. Logically, specifying              Perennial, based on the Iris logic, has both disk-points-to
an address space switch [34] from the address space with                    assertions 𝑑 [p] ↦→𝑛 𝑣 (for a specific disk 𝑑) and in-memory
the root address 𝑟 2 to the one with the root address 𝑟 1                                              𝛾
                                                                            points-to assertions ℓ ↦→𝑛 . Perennial crash-recovery logic
              {[𝑟 1]𝑃 ∗ 𝑄 }𝑐𝑟 3 := 𝑟 1{𝑃 ∗ [𝑟 2]𝑄 }cr3                      book-keeps resource names (can be thought of as logical
Modal Verification Patterns for Systems Software                                               PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea


variables) 𝛾 to identify which assertions (resource elements)                 case of the Ref-Count modality, @ℓ (ℓ1 ↦→ 𝑣) says that ℓ
remain valid after a crash — these assertions are only usable                 points to a reference count wrapping ℓ1 , while placing the
while the names in 𝛾 are valid, and a crash resets them, dis-                 ℓ1 ↦→ 𝑣 under a jump modality for a different location entails
carding assumptions about volatile state. A subtlety of the                   talking about a different region of memory.
notion of a resource context is that, unlike the earlier exam-                    In general, use cases where code frequently manipulates
ples, the context does not need to be a literal data structure.               small parts of multiple contexts together should prefer strong
It can instead be (various forms of) a set of executions, as                  nominalization, while use cases where usually larger por-
in the Post-Crash and NextGen modalities. The Post-Crash                      tions of a single context are at issue should prefer weak
modality ⋄ expresses that the assertion 𝑃 will be true after                  nominalization.
a crash discards all unstable storage (i.e., RAM). This was
the inspiration for the NextGen modality, which is in fact                    4    Conclusion
a framework for defining “after-𝑡” modalities, where 𝑡 is an
                                                                              We have argued that there is a systematic pattern emerging in
transformation of the global state.3
                                                                              the use of modalities in the verification of low-level systems
3.4    Nominals for Systems Resource Contexts                                 software, and explained how a range of modern work fits into
                                                                              this pattern. While most of our examples come from public
Finally, another design point is the question of whether or
                                                                              verification work carried out in Iris, we have one example
not resource element assertions must explicitly track their
                                                                              of these ideas applying in Dafny. We are applying these
corresponding context, or if they implicitly pick up their
                                                                              ideas in ongoing work using different modalities for different
context from where they are used.
                                                                              parts of a copy-on-write filesystem (e.g., for assertions true
   Strong nominalization is the case where resource elements
                                                                              in different snapshots), and are observing more structured
must explicitly include the identity of their intended context,
                                                                              specifications as a result. So not only are the modalities
while weak nominalization occurs when the resource ele-
                                                                              observably present, but they are demonstrably useful for
ments implicitly pick up the relevant context from how they
                                                                              conducting proofs of systems software. We believe that these
are used. The first three modalities in Table 1 are strongly
                                                                              essential patterns in the designs of modal abstractions for
nominalized, with the resource elements generally carrying
                                                                              systems verification constitute a fundamental concept when
identifiers of a specific modality usage.4 The rest are weakly
                                                                              working out how to specify different kinds of systems code.
nominalized.
   This choice trades off complexity against flexibility and
scoping constraints. Strongly nominalized elements track                      References
additional specifier/prover-visible book-keeping data. But in                  [1] Carlos Areces, Patrick Blackburn, and Maarten Marx. 2001. Hybrid
                                                                                   logics: Characterization, interpolation and complexity. The Journal of
exchange for carrying those identifiers of their context with
                                                                                   Symbolic Logic 66, 3 (2001), 977–1010.
them, strongly nominalized elements can be used together                       [2] Patrick Blackburn and Jerry Seligman. 1995. Hybrid languages. Journal
under any modality. For example, one can use the StackRe-                          of Logic, Language and Information 4, 3 (1995), 251–272.
gion modality to talk about two different stack frames si-                     [3] Jeff Bonwick, Matt Ahrens, Val Henson, Mark Maybee, and Mark
multaneously for code which accesses multiple stack frames:                        Shellenbaum. 2003. The Zettabyte File System. In Proc. of the 2nd
                                                                                   Usenix Conference on File and Storage Technologies (USENIX FAST).
 n ℓ ↦→ 𝑣 ∗ n+1 ℓ ′ ↦→ 𝑣 ′ . Using a given strongly nominal-                   [4] Torben Braüner. 2010. Hybrid logic and its proof-theory. Vol. 37.
ized assertion element under different modalities for different                    Springer Science & Business Media.
frames does not change its meaning. Likewise, weak-memory                      [5] Tej Chajed. 2022. Verifying a concurrent, crash-safe file system with
specific modalities existentially quantify over other views,                       sequential reasoning. Ph.D. Dissertation. Machetutes Institute of Tech-
related to the “current” view (the one where the current                           nology, Cambridge, MA. Available at https://dspace.mit.edu/handle/
                                                                                   1721.1/144578.
thread’s assertions are evaluated), and evaluate a resource (a                 [6] Tej Chajed, Joseph Tassarotti, and Contributors. 2023. Post-crash
thread-local view of an address-value mapping) with respect                        modality in Perennial’s Coq Mechanization. https://github.com/mit-
to those other views. Given that views are identified by nom-                      pdos/perennial/blob/master/src/goose_lang/crash_modality.v
inals, referring to all the other views makes weak-memory                      [7] Tej Chajed, Joseph Tassarotti, M. Frans Kaashoek, and Nickolai Zel-
modalities strongly nominalized.                                                   dovich. 2019. Verifying concurrent, crash-safe systems with Peren-
                                                                                   nial. In Proceedings of the 27th ACM Symposium on Operating Systems
   By contrast, weakly nominalized elements are more con-                          Principles (Huntsville, Ontario, Canada) (SOSP ’19). Association for
cise, but then make talking about multiple contexts together                       Computing Machinery, New York, NY, USA, 243–258. doi:10.1145/
marginally more complex: changing which modality an as-                            3341301.3359632
sertion is used with drastically changes its meaning. In the                   [8] Sailesh Chutani, Owen T Anderson, Michael L Kazar, Bruce W Leverett,
                                                                                   W Anthony Mason, and Robert N Sidebotham. 1992. The Episode file
3 The transformations are subject to some technical constraints that are           system. In Proceedings of the USENIX Winter 1992 Technical Conference.
unrelated to our point here.                                                       San Fransisco, CA, USA, 43–60.
4 The Post-Crash modality does not look like this in the presentation here;    [9] Hoang-Hai Dang, Jacques-Henri Jourdan, Jan-Oliver Kaiser, and Derek
technically the definition of ⋄ quantifies over names 𝛾 internally, dealing        Dreyer. 2019. RustBelt meets relaxed memory. Proc. ACM Program.
with sets of possible contexts.                                                    Lang. 4, POPL, Article 34 (Dec. 2019), 29 pages. doi:10.1145/3371102
PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea                                                                                      Kuru and Gordon


[10] Hoang-Hai Dang, Jaehwang Jung, Jaemin Choi, Duc-Than Nguyen,                 [31] Robbert Krebbers, Jacques-Henri Jourdan, Ralf Jung, Joseph Tassarotti,
     William Mansky, Jeehoon Kang, and Derek Dreyer. 2022. Compass:                    Jan-Oliver Kaiser, Amin Timany, Arthur Charguéraud, and Derek
     strong and compositional library specifications in relaxed memory                 Dreyer. 2018. MoSeL: A general, extensible modal framework for
     separation logic. In Proceedings of the 43rd ACM SIGPLAN International            interactive proofs in separation logic. Proceedings of the ACM on
     Conference on Programming Language Design and Implementation. 792–                Programming Languages 2, ICFP (2018), 1–30.
     808.                                                                         [32] Robbert Krebbers, Ralf Jung, Aleš Bizjak, Jacques-Henri Jourdan, Derek
[11] Peter J. Denning. 1970. Virtual Memory. ACM Comput. Surv. 2, 3 (Sept.             Dreyer, and Lars Birkedal. 2017. The essence of higher-order con-
     1970), 153–189. doi:10.1145/356571.356573                                         current separation logic. In European Symposium on Programming.
[12] Edsger W. Dijkstra. 1975. Guarded commands, nondeterminacy and                    Springer, 696–723.
     formal derivation of programs. Commun. ACM 18, 8 (1975), 453–457.            [33] Robert Krebbers, Amin Timany, and Lars Birkedal. 2017. Interactive
     http://doi.acm.org/10.1145/360933.360975                                          proofs in higher-order concurrent separation logic. In Principles of
[13] Marko Doko and Viktor Vafeiadis. 2016. A Program Logic for C11                    Programming Languages (POPL). http://cs.au.dk/~birke/papers/ipm-
     Memory Fences. In Proceedings of the 17th International Conference on             conf.pdf
     Verification, Model Checking, and Abstract Interpretation (St. Petersburg,   [34] Ismail Kuru and Colin S. Gordon. 2025. Modal Abstractions for Virtu-
     FL, USA). doi:10.1007/978-3-662-49122-5_20                                        alizing Memory Addresses. Proceedings of the ACM on Programming
[14] Marko Doko and Viktor Vafeiadis. 2017. Tackling Real-Life Relaxed                 Languages 9, OOPSLA2 (2025). doi:10.1145/3763134
     Concurrency with FSL++. In Programming Languages and Systems: 26th           [35] Ori Lahav, Viktor Vafeiadis, Jeehoon Kang, Chung-Kil Hur, and Derek
     European Symposium on Programming, ESOP 2017 (Uppsala, Sweden).                   Dreyer. 2017. Repairing sequential consistency in C/C++ 11. In Proceed-
     doi:10.1007/978-3-662-54434-1_17                                                  ings of the 38th ACM SIGPLAN Conference on Programming Language
[15] Kosta Došen. 1992. Modal translations in substructural logics. Journal            Design and Implementation. 618–632.
     of Philosophical Logic 21, 3 (1992), 283–336.                                [36] K Rustan M Leino. 2010. Dafny: An automatic program verifier for
[16] Ronald Garcia, Éric Tanter, Roger Wolff, and Jonathan Aldrich. 2014.              functional correctness. In Logic for Programming, Artificial Intelligence,
     Foundations of typestate-oriented programming. ACM Transactions                   and Reasoning. Springer, 348–370.
     on Programming Languages and Systems (TOPLAS) 36, 4 (2014), 1–44.            [37] Tom Murphy, Karl Crary, Robert Harper, and Frank Pfenning. 2004.
[17] George Gargov and Valentin Goranko. 1993. Modal logic with names.                 A symmetric modal lambda calculus for distributed computing. In
     Journal of Philosophical Logic 22, 6 (1993), 607–636.                             Proceedings of the 19th Annual IEEE Symposium on Logic in Computer
[18] Valentin Goranko. 1996. Hierarchies of modal and temporal logics                  Science, 2004. IEEE, 286–295.
     with reference pointers. Journal of Logic, Language and Information 5,       [38] Hiroshi Nakano. 2000. A Modality for Recursion. In Logic in Computer
     1 (1996), 1–24.                                                                   Science (LICS). 255–266. http://www602.math.ryukoku.ac.jp/~nakano/
[19] Colin S Gordon. 2019. Modal assertions for actor correctness. In                  papers/modality-lics00.ps.gz
     Proceedings of the 9th ACM SIGPLAN International Workshop on Pro-            [39] Peter W O’Hearn and David J Pym. 1999. The logic of bunched impli-
     gramming Based on Actors, Agents, and Decentralized Control. 11–20.               cations. Bulletin of Symbolic Logic 5, 2 (1999), 215–244.
[20] Robert Hagmann. 1987. Reimplementing the Cedar file system us-               [40] Scott Owens, Susmit Sarkar, and Peter Sewell. 2009. A better x86
     ing logging and group commit. In Proceedings of the eleventh ACM                  memory model: x86-TSO. In Theorem Proving in Higher Order Logics.
     Symposium on Operating systems principles. 155–162.                               Springer, 391–407.
[21] Joseph Y Halpern. 2017. Reasoning about uncertainty. MIT press.              [41] Amir Pnueli. 1977. The temporal logic of programs. In 18th Annual
[22] Joseph Y Halpern and Ronald Fagin. 1989. Modelling knowledge and                  Symposium on Foundations of Computer Science (FOCS 1977). ieee, 46–
     action in distributed systems. Distributed computing 3 (1989), 159–177.           57.
[23] Joseph Y Halpern and Yoram Moses. 1985. A guide to the modal                 [42] Vaughan R Pratt. 1976. Semantical consideration on Floyd-Hoare logic.
     logics of knowledge and belief. In Proceedings of the 9th international           In Foundations of Computer Science, 1976., 17th Annual Symposium on.
     joint conference on Artificial intelligence-Volume 1. Morgan Kaufmann             IEEE, 109–121.
     Publishers Inc., 480–490.                                                    [43] Greg Restall. 1993. Modalities in substructural logics. Logique et
[24] Joseph Y Halpern and Yoram Moses. 1990. Knowledge and common                      Analyse 36, 141/142 (1993), 25–38.
     knowledge in a distributed environment. Journal of the ACM (JACM)            [44] Greg Restall. 2002. An introduction to substructural logics. Routledge.
     37, 3 (1990), 549–587.                                                       [45] Ohad Rodeh, Josef Bacik, and Chris Mason. 2013. BTRFS: The Linux
[25] Carl Hewitt, Peter Bishop, Irene Greif, Brian Smith, Todd Matson, and             B-Tree Filesystem. ACM Trans. Storage 9, 3, Article 9 (Aug. 2013),
     Richard Steiger. 1973. Actor induction and meta-evaluation. In Proceed-           32 pages. doi:10.1145/2501620.2501623
     ings of the 1st Annual ACM SIGACT-SIGPLAN Symposium on Principles            [46] Mendel Rosenblum and John K. Ousterhout. 1992. The Design and
     of Programming Languages (Boston, Massachusetts) (POPL ’73). As-                  Implementation of a Log-structured File System. ACM Trans. Comput.
     sociation for Computing Machinery, New York, NY, USA, 153–168.                    Syst. 10, 1 (Feb. 1992), 26–52. doi:10.1145/146941.146943
     doi:10.1145/512927.512942                                                    [47] Filip Sieczkowski, Kasper Svendsen, Lars Birkedal, and Jean Pichon-
[26] Jaakko Hintikka. 1962. Knowledge and belief. Cornell University Press.            Pharabod. 2015. A separation Logic for Fictional Sequential Consis-
[27] Dave Hitz, James Lau, and Michael A Malcolm. 1994. File System                    tency. In European Symposium on Programming. Springer, 736–761.
     Design for an NFS File Server Appliance.. In USENIX Winter, Vol. 94.         [48] Robert E Strom and Shaula Yemini. 1986. Typestate: A programming
[28] Eric Jul, Henry Levy, Norman Hutchinson, and Andrew Black. 1988.                  language concept for enhancing software reliability. IEEE transactions
     Fine-grained mobility in the Emerald system. ACM Transactions on                  on software engineering 1 (1986), 157–171.
     Computer Systems (TOCS) 6, 1 (1988), 109–133.                                [49] Simon Friis Vindum, Aïna Linn Georges, and Lars Birkedal. 2025. The
[29] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak, Lars             Nextgen Modality: A Modality for Non-Frame-Preserving Updates in
     Birkedal, and Derek Dreyer. 2018. Iris from the ground up: A modular              Separation Logic. In Proceedings of the 14th ACM SIGPLAN International
     foundation for higher-order concurrent separation logic. Journal of               Conference on Certified Programs and Proofs (Denver, CO, USA) (CPP
     Functional Programming 28 (2018), e20.                                            ’25). 83–97. doi:10.1145/3703595.3705876
[30] Norihiro Kamide. 2002. Kripke semantics for modal substructural              [50] Andrew Wagner, Zachary Eisbach, and Amal Ahmed. 2024. Realistic
     logics. Journal of Logic, Language and Information 11, 4 (2002), 453–             Realizability: Specifying ABIs You Can Count On. Proc. ACM Program.
     470.                                                                              Lang. 8, OOPSLA2, Article 315 (Oct. 2024), 30 pages. doi:10.1145/
Modal Verification Patterns for Systems Software   PLOS ’25, October 13–16, 2025, Seoul, Republic of Korea


     3689755
