                                            CleanQ: a lightweight, uniform, formally specified interface for intra-machine
                                                                            data transfer
                                               Roni Haecki, Lukas Humbel, Reto Achermann, David Cock, Daniel Schwyn, Timothy Roscoe
                                                             Systems Group, Department of Computer Science, ETH Zurich


                                                                  Abstract                                 profiling, and monitoring such queues at runtime, making OS
                                                                                                           development more difficult and time-consuming.
                                            We present CleanQ, a high-performance operating-system
                                         interface for descriptor-based data transfer with rigorous for-      CleanQ addresses these problems not by simply proposing
                                         mal semantics, based on a simple, formally-verified notion of     yet another queue interface, but starting from a provably sound
arXiv:1911.08773v1 [cs.OS] 20 Nov 2019




                                         ownership transfer, with a fast reference implementation.         formal specification (presented in Section 3) of how a descrip-
                                            CleanQ aims to replace the current proliferation of similar,   tor queue should behave. This gives clear guarantees to clients
                                         but subtly diverse, and loosely specified, descriptor-based       of a queue (whether it be a device driver or an inter-process
                                         interfaces in OS kernels and device drivers. CleanQ has strict    communication system), and also states clear obligations on
                                         semantics that not only clarify both the implementation of        the code that implements an end-point of the queue.
                                         the interface for different hardware devices and software use-       The specification is strict, and so the chance of subtle mis-
                                         cases, but also enable composition of modules as in more          matches between the expectations of client and implementa-
                                         heavyweight frameworks like Unix streams.                         tion are eliminated. It allows for full concurrency between
                                            We motivate CleanQ by showing that loose specifications        actors, such as a driver process and a network card. It also
                                         derived from implementation lead to security and correctness      subsumes the memory model in use: the client of a CleanQ
                                         bugs in production systems that a clean, formal, and easily-      queue does not need to be concerned about weak consistency
                                         understandable abstraction helps eliminate. We further demon-     or non-coherent memory in order to write correct, portable
                                         strate by experiment that there is negligible performance cost    code to use it. However, CleanQ focuses purely on the data
                                         for a clean design: we show overheads in the tens of cycles       plane interface, leaving flexibility to system designers in how
                                         for operations, and comparable end-to-end performance to          such queues are instantiated and provisioned.
                                         the highly-tuned Virtio and DPDK implementations on Linux.           From the specification, we then proceed to a C interface
                                                                                                           which captures it. This interface is highly general. In Section 4
                                         1. Introduction                                                   we describe it and demonstrate its generality with a number
                                                                                                           of implementations we have built behind it, for network cards,
                                         CleanQ is a uniform operating system interface for transferring   storage adaptors, and inter-process communication. Moreover,
                                         bulk data, which abstracts from and unifies a wide variety of     the CleanQ C interface composes: we also describe CleanQ
                                         descriptor-based data transfer interfaces used by both software   modules that provide loopback, debugging and network stack
                                         and hardware in a modern OS.                                      functionality.
                                            Queues based on descriptor rings are pervasive in OS code         Finally, we evaluate the overhead of using our CleanQ im-
                                         for moving data between processes, hardware devices like net-     plementation modules on Linux and a microkernel-based re-
                                         work adaptors, kernel and user space, etc. Despite this there     search operating system in Section 5 to show both performance
                                         is a wide range of different queue interfaces and implementa-     and portability. We show that, despite the strict semantics and
                                         tions (even within a single OS). So-called standard interfaces    highly specified, uniform interface, CleanQ is cheap: it is com-
                                         to queues, where they exist, are typically specified informally   parable to Virtio and DPDK in operation latency and imposes
                                         using a reference implementation in C.                            less than 1% overhead for set/get operations using Memcached
                                            This leads to a serious problem, which we elaborate on in      [17].
                                         Section 2. Implementations cannot be reused (since the se-
                                         mantics are subtly different), and thus implementation bugs       2. Background and Motivation
                                         can recur (and do) when a new queue is built. The lack of
                                         clear semantics mean that bugs also arise due to inappropriate    CleanQ is a formalization of descriptor rings. Rings of de-
                                         use of a given descriptor queue, by a client programmer who       scriptors are a fairly pervasive technique for transferring data
                                         may not understand its subtleties, and also make it hard to       between end-points (software processes or threads, GPUs, ad-
                                         compose code modules which operate on queues of data, as is       dress spaces, hardware I/O devices, virtual machines, etc.) in
                                         possible with Unix Streams or other I/O frameworks. Without       a modern OS. Each descriptor refers to a region of memory
                                         a formally sound description of a queue’s behavior, it is im-     (usually elsewhere) plus some metadata, including which end
                                         possible to reason about the correct behavior of the OS which     of the communication “owns” the data (and metadata). The
                                         uses them. Finally, a lack of uniformity is a lost opportunity    Linux kernel alone has at least 6 different descriptor queue
                                         to build and apply standard tools for debugging, validating,      implementations, not including hardware-specific I/O queues
for network and storage devices.                                       prose and not formally specified. For example, consider the
   Descriptor rings work well because they highly decouple             virtqueue mechanism in Virtio [43] for transferring data
sender and receiver: sending data between a user process and           between a device driver and a virtual device.
a high-performance network adaptor using Intel’s DPDK [28],
for example, doesn’t require either side to touch payload data              A virtqueue consists of (1) a descriptor table spec-
as part of the transfer, and in the common case requires no                 ifying which buffers a driver is using for its device,
synchronization between sender and receiver. In such drivers,               (2) an available ring containing descriptors offered
interrupts and hardware register access is only used for coarse-            to the device, and (3) a used ring containing buffers
grained synchronization at low load levels; for the most part               processed by the device and returned to the driver.
each side of the communication can proceed in parallel without
explicit coordination.                                                 While the specification makes it clear that buffers available to
                                                                       the programmer are on one of the two rings, the corner-cases
   However, while the technique of descriptor rings is almost
                                                                       (such as adding a descriptor twice to a ring) are undocumented.
universal, there is little consensus on what a given ring should
                                                                       Programmers are ultimately advised to read the code. To make
look like. A great number of software interfaces, libraries and
                                                                       things worse, Virtio has two different queue interfaces–one
‘standards’ have been proposed over time (e.g. [16, 19, 43, 1,
                                                                       for the host and one for the guest–having slightly different
32, 22, 3]) all of which are variations or enhancements of the
                                                                       semantics (e.g. a memcpy on the host side).
same basic theme. Moreover, every new high-performance I/O
device adopts a different descriptor format for its I/O queues,        2.2. Lack of Portability and Reuse
including devices from the same vendor (e.g. [39, 24, 26, 27,
25, 4]).                                                               A further consequence of specification-via-implementation is
                                                                       that correctness often depends on a particular memory model.
2.1. The Continuing Emergence of Descriptor Bugs                       The combination of program operations and fences/barriers
This proliferation of implementations is often for good reasons:       required for correct operation is not at all obvious from the
queue implementations (whether communicating between pro-              documentation, and is different for different processor archi-
cesses or between software and hardware devices) have dif-             tectures. For example, when a device driver enqueues a buffer,
ferent requirements in how they are constructed and set up,            it first writes the buffer contents, then the descriptor, and fi-
metadata that may need to be passed with each buffer, and              nally updates the head pointer of the ring buffer to inform the
additional, implementation-specific semantics associated with          device that there is a new descriptor. On a machine with a
enqueue and dequeue operations. Examples are Virtio [43] for           weak memory model, these operations can be reordered and
buffer transfer between host and virtual machines, SKBufs[35]          the device notified before the descriptor is written to memory.
in the Linux network stack or mbufs in DPDK [28]. How-                     Consider, for example, invoking a Virtio [43] or fbuf [16]
ever, the proliferation of implementations combined with the           based queue between two cores: an Intel x86 machine imple-
difficulty of getting memory semantics right leads to a steady         ments Total Store Ordering [44], leading to a relatively simple
stream of serious bugs, ranging from performance problems              implementation: if a thread performs two writes w1 before
to critical security vulnerabilities.                                  w2, another thread that observes w2 will also have observed
   For example, the Virtio framework used in the QEMU em-              the effect of w1. Implementing buffer transfer for x86-TSO or
ulator and the KVM virtual machine monitor has allowed a               similar models, it suffices to ensure correct write ordering.
malicious guest to break security by inserting more requests               However, machines with weak memory consistency like
than the size of the queue [13]. Changing the queue parameters         ARMv7, ARMv8, or IBM Power [18] allow considerable re-
in Virtio has caused the hosting QEMU process to crash [41]).          laxation in the visibility order from a given core: any load,
   Worse, these bugs have not only been appearing for a long           store, or atomic instruction can be extensively reordered
time – they continue to appear [7, 8, 9, 40, 12, 10, 11, 13, 15,       around other loads and stores. A correct queue therefore
14, 41, 6] in Linux and Android (and, we suspect, other system         requires tricky use of barrier and fence instructions.
software). A new class of “double-fetch” bugs/vulnerabilities              Moreover, given the number of descriptor queue imple-
have recently appeared [46] whereby data is fetched twice but          mentations in a typical OS, it is surprising and disappointing
changed by another party in between. All these bugs ultimately         that generic functionality cannot be shared among implemen-
boil down to production code making incorrect assumptions              tations, nor can implementations compose efficiently into a
about when and how memory can be accessed safely by one                pipeline, in the manner of more heavyweight data transfer
side of a descriptor queue-based channel: when it is safe to           frameworks like Streams in AT&T [42] and Plan 9 [38], or the
reuse a buffer, when an endpoint can safely enqueue another            protocol modules in the x-Kernel [23].
buffer, etc.                                                           2.3. CleanQ
   We argue the main reason this problem is not going away
is the prevalence of specification by implementation: The              The duplication of code and continuing stream of new bugs in
documentation–where it exists at all–is written in English             ad-hoc descriptor queues led us to develop CleanQ, a formally-


                                                                   2
     OA                                         QAB                       We therefore take the concept of ownership as our primitive
 (owned by A)
                        A.enqueue()          (queued A→B)              abstraction, and base our formal invariants1 on the following
                                                Queue                  four properties that must hold if an entity can really be said to
          A.dequeue()               B.dequeue()                        “own” a thing:
    QBA                 B.enqueue()
                                                 OB                    1. A thing has at most one owner.
(queued B→A)                                 (owned by B)              2. If an entity owns a thing, it has exclusive use of it.
                Figure 1: Ownership transfer                           3. An entity knows whether it owns a thing or not.
                                                                       4. Ownership can be transferred.
specified data transfer model for descriptor queues with an               From the first property we infer the fundamental invariant
associated C-language interface.                                       of the model:
   To the best of our knowledge, CleanQ is the first practical,
formally-specified, general-purpose descriptor ring abstrac-                                         OA ∩ OB = 0/
tion, and we show that the generality and strict semantics of
CleanQ come with negligible performance penalty compared               The set of things owned by A (OA ) is disjoint from the set of
with poorly-specified (but well-implemented) subsystems in             things owned by B (OB ), for any processes A and B. Note that
production use.                                                        a process is anything that might read or modify a buffer: a
   By decoupling rigorously defined data transfer semantics            user-space process, a device driver, a hardware component
from implementation, CleanQ allows clients and implementa-             (e.g. a network card).
tions to be developed and tested separately with much greater             The second property expresses the most important guar-
assurance of correctness. CleanQ is a specification and not an         antees that the system must provide to processes (and that
implementation, thus leaving orthogonal issues like metadata,          processes must, in turn, respect): First, if A owns a buffer,
setup, and additional semantics to the implementation while            any changes to the buffer visible to A must be due to modi-
adhering to a single common model for data transfer.                   fications A itself made since gaining ownership; Second, no
   CleanQ is highly general: it can express a variety of hard-         other process (B) may rely on the contents of the buffer until
ware descriptor queues as well as communication channels               A relinquishes ownership and B acquires it; Third, all changes
between processes in an OS. We demonstrate this functional-            caused by A (while it owned the buffer) must be visible to B
ity by later implementing, among other things, a debugging             immediately upon acquiring ownership. This guarantees iso-
module which is transparent to a CleanQ queue but applies              lation among processes, and provides clear requirements for
rigorous online checking of its arguments.                             any code needing to manage a weak or non-coherent memory
   CleanQ is not “yet another queue implementation”, nor               system (by dictating barriers, flushes, etc. see Section 3.4).
is it a bug-finding technique for existing implementations.               The third and fourth properties force us to elaborate the
Moreover, our goal is not to build a formally verified system          formal model: If atomic transfer were possible, we could stick
(such as seL4 [31] or CertiKOS [21]), but rather a sound               with just the sets by A and B and the bookkeeping problem
basis for reasoning about the system and its behavior and              would be straightforward. Generally however, no atomic trans-
having clearly defined semantics. CleanQ is an example of              fer of ownership is possible: most implementations (especially
how a useful subset of the benefits and guarantees of full-stack       hardware) transfer buffers by means of a descriptor ring or
verification can be practically introduced into existing systems       similar. The relinquishing process enqueues a descriptor re-
in a portable and incremental manner                                   ferring to the buffer to be transferred, which the acquiring
   A concise, formally-sound model such as CleanQ is essen-            process (eventually) dequeues.
tial to the development and proof of formal systems software,             Note that the transfer sets (QAB and QBA ) at this point do
but it is just as important for non-verified systems such as           not preserve ordering. We add the FIFO property by refining
Linux. As long as the implementation of a CleanQ module ad-            the model in section 3.2.
heres to the specification, we can guarantee properties proved            While a buffer is in the queue (descriptor ring), it cannot be
on the formal model.                                                   said to belong to either A or B in a way compatible with our
                                                                       4 properties. If the buffers queued from A to B (QAB ) belong
3. Model                                                               to A, A is free to modify them as it likes (property 2). But as
The interfaces we consider (e.g. virtio) all transfer data in          soon as the descriptor is dequeued, B will assume it owns it
buffers (packets, VM pages, disk blocks, etc.) between pro-            (e.g. the NIC will start writing). As enqueue and dequeue are
cesses (including software processes, device drivers, hardware         asynchronous, A has no way of knowing when to stop writing!
devices, etc.). The copy itself is simple (for a zero-copy im-         Likewise, assigning ownership of QAB to B violates property
plementation, it is completely absent). The principal difficulty       3: B gains ownership (and thus responsibility) without being
is the bookkeeping: When can a process safely read a buffer            informed (when A enqueues). The queues are therefore distinct
it has received? When must it stop writing before handing it
off? When, exactly, is the buffer handed off?                             1 Properties that must always hold.




                                                                   3
                                             A.enqueue()                                                          OA -{X}                       QAB∪{X}
         OA                             (tail+1) % N ≠recl →            QAB                                                   A.enqueue(X)
                    recl++; OA+={Y}       tail++; OA-={X}                                                                                           Queue
                                            tail                                                        QBA                             OB
    A.dequeue()




                                                                                  B.dequeue()
                                                                    head≠tail →
                                                   X
                  recl≠done →



                                                            head                                                  OA -{X}                       LAB+[X]




                                                                      head++
                                               Y
                                        recl                                                            LBA                             LB
                                                                                                                                         hd++
                                                       done                                                                         X
                                          done≠head → done++                                                              Y
      QBA                                    B.enqueue()
                                                                          OB
                   Figure 2: Ownership in the i82599 ring buffer                                                      Figure 3: Refinement steps
from the ownership sets (and from each other):                                                      descriptors in Figure 2). The driver keeps track of which de-
                                                                                                    scriptors it has dequeued (and are safe for reuse), with the
                                        OA ∩ QAB = OB ∩ QAB = 0/
                                                                                                    recl pointer. This points to the oldest descriptor in QBA (the
                                        OA ∩ QBA = OB ∩ QBA = 0/                                    last shaded). The i82599 processes buffers in order. recl
                                                   QAB ∩ QBA = 0/                                   divides the region between tail and done into the returned
                                                                                                    descriptor queue (QBA ) (recl to done) and ‘free’ descriptors
   This is the complete model, illustrated by Figure 1. Here                                        (tail to recl).
we see the four sets describing the transfer of ownership be-                                          All four of the queue operations consist of atomically incre-
tween processes A and B, and the allowable transitions. Bar-                                        menting a pointer (as indicated in gray in Figure 2, together
ring A.register() and B.register() (which add buffers                                               with the guards (→) against letting the head of a queue over-
to, and remove them from bookkeeping), the four opera-                                              take its tail).
tions (A|B.enqueue(), A|B.dequeue()) transfer ownership                                                This shows that the CleanQ specification and its notion of
of buffers clockwise: OA → QAB → OB → QBA → OA .                                                    ownership do, in fact, model the i82599 hardware queues
   One final invariant completes the model, and expresses that                                      – CleanQ closely corresponds to the design of real, high-
buffers are never lost, or invented out of thin air:                                                performance hardware. The extremely simple implementation
                                                                                                    possible in this case also demonstrates that there is no inherent
                                      OA ∪ QAB ∪ QB ∪ QBA = CONST                                   overhead to a well-specified formal interface, such as CleanQ.
3.1. Modelling the Intel i82599 Descriptor Ring                                                        OA (the buffers owned by A) cannot be defined by the con-
                                                                                                    tent of the descriptor ring. A might have e.g. register-ed a
Figure 2 illustrates the descriptor ring buffer of the Intel i82599                                 pool of buffers, shared between multiple queues. Operations
10GbE network controller [29, 27] used in Intel’s popular                                           on OA are thus defined abstractly:
X520 server network cards, and how it is interpreted in the
CleanQ model. The ring itself (figure center) is a circular                                                      A.enqueue(X) : OA := OA − {X}
buffer with two pointers: head and tail. The descriptors                                                         A.dequeue(Y) : OA := OA ∪ {Y }
from head up to (but not including) tail are those enqueued
but not yet taken by the device i.e. the set QAB (here A is the                                     Any implementation of A.enqueue() must cause A to relin-
driver and B the NIC).                                                                              quish ownership of X and that of A.dequeue() cause A to
   The driver enqueues X by writing at tail, then increment-                                        take ownership of Y . This is not a property on the ring buffer,
ing the pointer, atomically transferring X from OA to QAB . The                                     but rather a correctness requirement for software that uses the
NIC dequeues by incrementing head, atomically moving a                                              ring buffer: It tells the programmer exactly when they must
buffer from QAB to OB , (done up to head). The done2 pointer                                        relinquish ownership, and exactly when they may assume they
is only modified by hardware and points to the last (oldest)                                        have re-acquired it.
buffer that the NIC has dequeued but not yet processed.
   Only tail, head and done have hardware-dictated mean-                                            3.2. Refinement
ing — The NIC doesn’t distinguish (and doesn’t need to) be-                                         This notion of a ‘specification to be implemented’ is a data
tween buffers that are enqueued back to the driver (QBA ) and                                       refinement (as used e.g. in the seL4 proof [5, 47]), and is also
already dequeued in software and ready for reuse (unshaded                                          how our i82599 interpretation is formally specified. Figure 3
   2 There are two hardware modes: An explicit done pointer, or a done bit                          depicts a stepwise refinement of A.enqueue(X) from the
in the descriptor which defines an implicit done pointer                                            abstract set-based model described so far, via an intermediate


                                                                                                4
  OA -{X}          A.enqueue(X)
                                       QAB∪{X} -ΔAB                       A Owns X
                                                                                                  Queued:
                                                                                                                        B Owns X
                                                                                                    A →B
         A.dequeue()                       Queue
                                  B.dequeue()                               X[0]:= x 5                                 X[1]:= y

QBA∪ΔBA                                                                                                                        3
                                       OB∪ΔAB -ΔBA




                                                                               rf




                                                                                                                        ce
                   B.enqueue()




                                                                                 en




                                                                                                                       en
                                                                                  ce




                                                                                                                     rf
       Figure 4: Weak postconditions for concurrency                                 *(tail++)= X           X= *(++head)
                                                                                                    data
                                                                                            1                  2




                                                                                                                      wf
                                                                                  e
                                                                                                  dependent




                                                                                 nc
model where queues become lists (establishing FIFO order),




                                                                                                                       en
                                                                                 e




                                                                                                                          ce
                                                                              wf
to the ring buffer model just described.
   Each layer is the ownership transfer ring (c.f. Figure 1) at a           x:= X[1]                                    z:= X[0]
given refinement level. Double lines indicate elements linked                4                                                 6
by the state relation e.g. the set QAB contains exactly the el-
ements of the list LAB which is in turn the descriptors from                          Figure 5: Ownership implies fences
done up to head in the ring. Red arrows highlight the refine-
ment of A.enqueue(X), from set insertion (QAB ∪ {X}) to list            as ARM and Power [34]) and partially- or non-coherent sys-
append (LAB + [X]) and finally pointer increment (head++).              tems (e.g. accelerators) may violate the exclusivity guarantees
   The state relations, and refined datatypes and operations are        by reordering memory operations past the ownership transfer
all formalised in Isabelle/HOL. Following the convention used           (by reordering or speculatively executing instructions, or by
in Formal Methods conferences, we do not include them here              serving stale values from non-coherent caches).
for space reasons, but all Theory sources will be published                Consider Figure 5, depicting the transfer of the buffer X
and are available on request.                                           between sender A and receiver B, on a hypothetical very-weak-
                                                                        memory architecture (similar situations are or were observable
3.3. Concurrency                                                        on IBM Power and DEC Alpha systems). In the absence
CleanQ is fully concurrent, and mandates no locks. A and                of fences (barriers), the only orderings guaranteed are those
B may simultaneously enqueue and dequeue to their shared                with a data dependency, marked with a solid arrow. The two
queues, as long as the invariants are preserved. For the i82599         dotted arrows between A’s modifications to the buffer and its
this reflects that, for example, head is updated by the NIC             relinquishing ownership (incrementing tail) only indicate the
obliviously to everything except that it does not overtake tail.        intended ordering; These operations may occur in any order.
The driver is free to enqueue at tail at precisely the moment           In particular, the execution order indicated by the circled red
that the NIC dequeues at head.                                          numbers is consistent with the constraints (and can actually be
   The strict postconditions of Figure 3 are not preserved by           observed).
the actions of a concurrent process. For example, the strict               Here we see A relinquish ownership (1), then B acquire it (2)
postcondition Qnew        old
                 AB = QAB ∪ {X} for A.enqueue(X) is invali-
                                                                        and immediately write value y to X[1] (3). Only then are A’s
dated if B dequeues X.                                                  modifications scheduled: It reads the value in X[1] (y, at 4),
   In reasoning about A, we cannot rely on X being in QAB ,             and writes it into X[0] (5). Finally, B reads the value in X[0],
just because A has executed enqueue(X). We can, however,                and sees the value y that it itself wrote. B has communicated
infer that X is in one of QAB , OB or QBA — everywhere                  to itself by traveling into the ‘past’!
B might have put it, without A doing anything (i.e. calling                A sufficient fix in this case is to add the read and write
dequeue). Figure 4 summarizes the weakened postcondition                fences as indicated. A’s read from X[0] is forced to commit
for enqueue(X) that is preserved under interference by B.               before the increment to tail (as it also involves a read), and
   These weakened postconditions are a prerequisite for veri-           likewise the write to X[1]. The read and write fences in B are
fying the correctness of a particular implementation under full         redundant in this example (as in fact is A’s write fence due to
concurrency, using Owicki-Gries [36] logic as, for example, in          the data dependency). If not all instructions in A and B are
the verification of the eChronos real-time operating system [2].        known however, all four barriers are necessary.
We have formalized these, also in Isabelle/HOL, including                  Where the ownership model helps here is that all four barri-
noninterference and refinement proofs for all abstract levels.          ers can be inferred from the guarantees and responsibilities of
                                                                        ownership: A must ensure that any writes to X become visible
3.4. Caches and Memory Fences
                                                                        to B before B learns that it owns X (i.e. A’s write to tail
Knowing exactly when ownership is gained and lost is essen-             becomes visible to B). The last point at which A can ensure
tial to knowing exactly which cache management operations               this (as B’s dequeue is asynchronous) is when it enqueues X –
and fences/barriers are needed, and when, in order to correctly         Hence the write fence before updating tail. Likewise A must
provide the guarantees implied by our ‘four properties of own-          not rely on X after relinquishing ownership – Hence the read
ership’. In particular, weak-memory-model architectures (such           fence before the enqueue. An equivalent argument implies the


                                                                    5
necessity of the fences on B’s side (e.g. in the absence of a             Register takes a contiguous region of memory, previously
data dependency).                                                      owned by neither side of the queue, inserts it into the set of
  Furthermore, it should be possible to automatically place the        owned buffers, and returns an identifier for it to be used in sub-
required fences, for some combination of a (possibly-stronger)         sequent enqueue and dequeue operations. Register is typically
memory model (e.g. ARM or TSO) and known code in A and                 used in conjunction with buffer pools or slab allocators that
B. Such automatic inference in code of similar complexity              allocate a large chunk of memory at once.
was demonstrated by Liu et. al. [33]                                      Register is of practical importance in cases where address-
                                                                       related state must be set up in advance, for example regions
4. Interface and Implementation                                        for RDMA-based transfers, or programming an IOMMU to
In this section we describe the C interface we derive from             make a region of memory accessible to both sides of the queue.
the formal model in the previous section, together with a              In simple shared-memory cases it can be implemented as a
set of implementations (termed “modules”, following Unix               null operation which returns the pointer address as the handle.
Streams [42]) we have built and evaluated for inter-process               The mem argument is an OS-specific handle to a memory
communication and device drivers.                                      resource, e.g. a pointer to anonymous memory, a file handle
   Figure 7 shows the software architecture. To show the               to a mapped segment, or a capability to physical memory. The
applicability of CleanQ to different devices and other use-            memory region has to be at least read-accessible from the
cases, we have implemented modules for an AHCI [30] stor-              calling process. At no time may the set of registered regions
age host adapter, an Intel e1000 NIC [25], an Intel i82599             overlap with each other.
10Gb NIC [27], a Solarflare SFN5122F low-latency NIC [45],                Deregister removes a previously-registered region with the
a network protocol stack implementing UDP/IP, a shared-                supplied id from the queue. Deregister can only succeed if the
memory inter-process queue, and a DPDK [28] module for                 region has not already been deregistered, and all memory in
the Intel i82599 10Gb NIC. We also implemented a debug                 the region is currently owned by the calling process.
module, which checks the interface contract at runtime. We                Enqueue enqueues a buffer of a previously registered re-
describe the detail of the network stack and debug modules             gion for ownership transfer. Buffers are identified by a region
in section 4.2.                                                        id, an offset into this region and a length. The buffer described
   We have applied CleanQ in Linux, DPDK, and a                        by offset and length, must lie within the registered region,
microkernel-based research OS, showing that it is deployable           and must be owned by the process (i.e. a buffer cannot be en-
across multiple, complete existing systems. An additional,             queued twice without dequeuing it beforehand). The operation
Rust-based implementation which exploit’s Rust’s ownership-            can fail if the underlying queue has run out of space.
based type system is beyond the scope of this paper.                      The valid payload is specified by a further offset and length
                                                                       within the buffer, allowing clients to leave space for headers
4.1. Definition                                                        and footers (meta data) added later.
Figure 6 shows the C declarations for CleanQ. This interface is           As specified, a successful enqueue relinquishes ownership
implemented by generic code which performs various integrity           of the buffer and inserts it into the transfer set. Eventually the
checks (such as region bounds for buffers) before calling cor-         ownership of the buffer will be obtained by the peer process,
responding module-specific methods in a vtable associated              but there is no guarantee when this happens.
with the struct cleanq argument.                                          A client must not alter a buffer once it has given up own-
   The enqueue and dequeue methods must adhere to their                ership, and doing so will result in undefined behavior. Since
specification introduced in section 3. The additional notify,          we know precisely when we yield the ownership and which
register, and deregister calls are described below.                    memory region is described by the buffer, the implementa-
   We now describe the semantics of the CleanQ interface               tion can and must guarantee that all changes to the buffer are
functions in detail. Interface calls that do not satisfy the re-       observable (using memory fences) before the ownership is
quired preconditions are bugs on the caller side and cause             transferred.
undefined behavior (though many are caught by the generic                 The flags field allows additional metadata to be passed
checking code). As in section 3, “process” denotes anything            along orthogonally with the buffer, with the proviso that the
that changes buffers, for instance a software driver or the            formal semantics from section 3 are not altered in any way.
hardware of a network interface card.                                  For example, a DMA copy engine might require the client to
   Creation and destruction of queues is not part of the inter-        distinguish source and destination buffers for a copy.
face, since these processes are highly implementation specific            Dequeue removes a previously enqueued buffer from the
and typically need module specific parameters, such as device          queue and transfers ownership of the buffer to the calling
registers of a network card, a shared memory buffer for the            process. As long as the process owns a buffer, the process can
loopback/IPC queue, or another queue in case of the debug              alter the contents of this buffer. Dequeue can be called any
queue. Creating a queue must include initializing the cleanq           time but returns an error if there is nothing to dequeue.
data structure including the generic state and vtable.                    Absent an error, a correct implementation must return a


                                                                   6
err_t cl ea n q_ re g is t er ( struct cleanq *q , void * mem , regionid_t * rid ) ;
err_t c l e a n q _ d e r e g i s t e r ( struct cleanq *q , void * mem , regionid_t rid ) ;
err_t cle anq_en queue ( struct cleanq *q , regionid_t rid , size_t offset , size_t length ,
                                    size_t valid_data , size_t valid_length , uint64_t flags ) ;
err_t cle anq_de queue ( struct cleanq *q , regionid_t * rid , size_t * offset , size_t * length ,
                                    size_t * valid_data , size_t * valid_length , uint64_t * flags ) ;
err_t cleanq_notify ( struct cleanq * q ) ;
                                              Figure 6: The CleanQ library interface

                CleanQ Generic Interface                               4.3. Networking
                     Common Code                                       We have built a full-duplex UDP protocol stack which sits atop
NetworkQ     AHCIQ     LoopbackQ    DebugQ     EthernetQ               a CleanQ module implementing a NIC’s hardware queues and
                                                                       which itself consists of two CleanQ modules: one for the
                UDPQ      IPQ    DPDKQ                                 UDP headers and one for IP and Ethernet headers. The result
      Figure 7: Implemented modules of CleanQ Library
                                                                       is a dataplane implementation similar to Arrakis [37]. The
                                                                       structure of the enqueue call is shown in figure 8. In order to
valid buffer, i.e. one that is within a previously registered
region and is not yet owned by the calling process. As with            struct udp_q * que = ...
enqueue, a subset of the buffer can be declared valid using            struct cleanq * q = ( struct cleanq *) que ;
valid_data and valid_length, to allow stripping of head-               cle anq_en queue (q , ...) {
                                                                         // Some interface checks
ers (for example, in the UDP queue example we show in                    q . enq (q , ...) {
section 4.2).                                                                // Build UDP header
   Metadata about the transfer can, as with enqueue, be re-                  q - > ip_q . enq (q - > ip_q , ...) {
turned in flags. Again, this is implementation defined but                       // Build IP + Ethernet header
                                                                                 ip_q - > nic_q . enq ( ip_q - > nic_q , ...) {
must be orthogonal to the memory ownership semantics. It                            // Build descriptor and inform Hardware
can be used to signal corrupt packets from a network adapter,          } } } }
for example, or as part of a chaining protocol (section 4.4)                     Figure 8: Stacking queues to implement UDP
   Notify is an optional performance optimization mechanism:
for example, a doorbell informing the process on the other side        implement different layers of the stack, we use valid_data
of the queue that there might (i.e. no guarantee) be buffers           and valid_length. When receiving a packet, each layer
in the queue that are ready for processing. It has no formal           reads and interprets the header found at offset valid_data.
semantics at all, and its use (or omission) must not affect the        To pass a packet up to the next higher layer valid_data is
correctness of any implementation relative to the specification.       incremented by the header size, such that the next higher layer
                                                                       will ignore the current layer’s header.
4.2. Module Composition and Debugging
                                                                       4.4. Discussion
We have implemented CleanQ modules which communicate
with a variety of hardware devices using their native descriptor       Our experience building a number of CleanQ modules, and
format and protocol, along with inter-process communication            composing them, has so far been very positive. Implementa-
channels which pass descriptors in shared memory using a               tion is generally straightforward, similar to a Virtio queue or an
variant of FastForward [20]. Despite incorporating basic run-          ad-hoc implementation, and establishes that the model is suffi-
time checks, we show in Section 5 that these modules are               ciently general to cover all the use-cases we have encountered
comparable in performance with the “native” implementations            so far.
they replace. However, CleanQ’s formally specified interface              CleanQ’s formal semantics make it very clear what obli-
has a further advantage: in contrast to ad-hoc, C-specified            gations exist for a module programmer at every point in the
queues, CleanQ modules can compose in a pipeline or stack,             code, and remove most of the uncertainty about what the code
analogous to System V streams. The “null” implementation (a            needs to guarantee and when. The use of stackable modules
module which sits in front of another CleanQ module but sim-           provides the expected benefits in composability, and we have
ply passes data through) imposes negligible overhead, and we           made extensive use of the debug module for checking.
have implemented a debug module which augments CleanQ’s                   Compared with other queue implementations in systems
default bounds checks with more extensive bookkeeping to               like Linux, however, CleanQ is something of a radical simpli-
detect violations of the queue’s contract by either client or          fication, and this might raise several concerns.
downstream module. For example, it maintains an operation                 Firstly, we are paying the price of abstraction: the clearer
log for debugging purposes, and detects overlapping or dupli-          interface requires indirect method calls for each module. His-
cate enqueues, which prevent “double fetch” race condition             torically these have been viewed as expensive, but as we show
vulnerabilities [46].                                                  in Section 5 modern processors have reduced this overhead to


                                                                   7
considerably less than the cost of, e.g., formatting hardware
descriptors, and so this appears not to be an issue.
   Secondly, each enqueue or dequeue operation acts on a
single buffer: there is no batching. In practice, the cost of
multiple enqueue/dequeue operations is sufficiently small in
our implementations that this does not degrade performance
significantly.
   Finally, we do not directly support chaining of multiple, dis-
contiguous buffers as with BSD mbufs or Linux sk_bufs.
Instead, we chain buffers using a simple protocol above
CleanQ’s single-buffer enqueue/dequeue operations. As with
batching, the additional overhead is small for our usecases.                   Figure 9: Overhead of C interface implementation
   Our argument, backed up by performance measurements, is
that the simplicity and rigorous semantics of CleanQ outweigh            the module (before the vtable invocation). We run the bench-
the small overhead the design might incur.                               mark of 100,000 repetitions and account for our measuring
                                                                         instrumentation.
5. Evaluation                                                               Figure 9 shows the median (and standard deviation) of each
                                                                         of the four operations. We observe that the cost of the thin
To evaluate the performance of CleanQ we first benchmark the
                                                                         library layer of our CleanQ implementation is on the order
overhead of our implementation of the interface, then compare
                                                                         of tens of cycles for the enqueue, dequeue and deregister
the equivalent operations of Virtio to our queues. Following
                                                                         operation whereas register requires an additional check that
this, we set the overhead into perspective of a real application.
                                                                         the memory region is actually owned by the caller resulting in
We then further evaluate the different mechanisms of stacking,
                                                                         about 400 cycles overhead for a system call and the required
the debug queue and finish the performance benchmarks with
                                                                         bookkeeping.
a more complex example of an implementation of a UDP stack
based on our queues as well as on DPDK. Finally we discuss                  The results show that our implementation adds little
the performance of CleanQ based on the previously presented              overhead in exchange for a well-defined and clean interface
benchmarks.                                                              based on a formal model. The overheads of the fast-path
   With these benchmarks we show that there is no significant            operations enqueue/dequeue are less than 30 cycles and
performance loss when changing from existing systems to                  require fewer cycles than the simple loopback module. We
CleanQ while we gain a clean, easier to use, well-defined                expect the register/deregister operations to be on the slow-path
interface with the ability to stack queues. Furthermore, in our          but nevertheless they only add a few hundred cycles at most
implementation of the interface we added sanity checks on the            for the bookkeeping operations.
buffers through the thin library layer that are not included in
most systems.                                                            5.2. Comparison with Virtio
   All experiments were conducted on a two-socket Intel Xeon
E5-2670 v2 (Ivy-Bridge, 2.5 GHz) system with hyper thread-               In this benchmark we compare the operations of CleanQ (with
ing disabled. We used an i82559-based Intel X520 dual-port               our loopback module) that have an equivalent in Virtio (ad-
10GbE card to evaluate the performance of the UDP queue.                 d/get vs. enqueue/dequeue) to show that the performance is
Unless indicated otherwise, all measurements are taken using             comparable.
the timestamp counter of the processor. We evaluated CleanQ                 We compare CleanQ with Virtio (both on Linux) by mea-
on Linux (Ubuntu 18.04 LTS) and a microkernel-based re-                  suring the calls to the application interface of CleanQ and
search OS.                                                               Virtio’s virtqueue implementation. To measure the perfor-
                                                                         mance of Virtio we adapted one of the Linux Virtio tests,
5.1. The Overhead of Common Code
                                                                         adding measurement code and increasing the number of rep-
This benchmark shows that the performance overhead of our                etitions. The Virtio test uses virtqueue_add_inbuf() to
C implementation, which provides some sanity checks as com-              add buffers to the queue and after the host side has removed
mon code, is small in absolute terms for all four operations             them, the buffers are reclaimed from the guest side by calling
enqueue, dequeue, register and deregister.                               virtqueue_get_buf(). Note, the host side of the virtqueue
   The benchmark setup is as follows: We configured CleanQ               is accessible through a different interface that requires a
to use the loopback-module which resembles an in-memory                  memcpy for adding data to the queue. For fairness we did
ring buffer where enqueue writes the descriptor into memory              not include the host side interface operations in this bench-
and dequeue reads the descriptor contents from memory and                mark. The result of the benchmark is shown in Figure 10.
the corresponding pointers are updated accordingly. We mea-              Enqueueing a descriptor to the Virtio virtqueue costs 56 cy-
sure at two points: at the calls to the interface and the calls to       cles while enqueuing a buffer through our interface and then


                                                                     8
Figure 10: Performance of Virtio ring buffer (add/get) com-
pared to CleanQ (enqueue/dequeue) both running on Linux                      Figure 11: Memcached set/get processing time

processing it in the module costs 72 cycles. Getting a descrip-
tor from the virtqueue is more expensive at 100 cycles while
dequeueing a buffer from CleanQ only costs 64 cycles.
   Overall the performance is similar to Virtio’s guest side
while CleanQ provides additional checks on the buffers, a
cleaner and simpler interface that allows for more complex
constructs by stacking queues on top of each other.
5.3. Placing library overhead in context
To put our C implementation overhead of CleanQ into per-
spective, we measure the total processing time of Memcached
(v1.5.10) [17] including network stack and hashtable lookup
for set and get requests. This is a simple application context
in which CleanQ interface can be used.                                Figure 12: Linux: kernel to userspace network stack perfor-
   We send small get/set requests (key + value < 16 bytes) over       mance on receive path
the network to our Memcached server. We profile incoming
requests by measuring the network stack processing time and
                                                                      invokes the same operation on the next module in the stack
the duration of Memcached handling the get/set request. Note,
                                                                      and therefore all observed overhead originates from stacking
the resolution of the software timestamps provided by the
                                                                      itself. We measure at different levels of the stack the time it
network stack is one microsecond (or 2500 cycles).
                                                                      takes until the lower level completes the operation. Again, we
   The results, in the form of a CDF plot of 100,000 set/get
                                                                      conducted 100,000 runs for each operation.
operations, are shown in Figure 11 for request handling in
Memcached and Figure 12 for processing the packet in the                 Figure 13 shows the median execution time and standard
network stack. The median time spent from the kernel to the           deviation at three different points of measurement: i) the base
userspace application on the receive path of a UDP packet is          line (loopback) represents the lowest level of the stack which
3 microseconds or around 7500 cycles. The median of both              includes only the loopback module (corresponding to sec-
set/get is around 3450 cycles (1.3 µs). Combining these two           tion 5.1) ii) Null 1 represents the time taken when a single
measurements results in 10950 cycles (4.38 µs) that are spent         null module is stacked on top of the loopback module. We
over the application’s path on which the CleanQ interface             observe a negligible overhead for a single stack of less than
could realistically be used.                                          10 cycles for any of the operations. iii) Null 10 measures the
   Comparing the time spent in the library on the fast path to        full stack of ten null modules stacked on top of the loopback
the application’s time spent in other code, leaves the overhead       module where the entire stack of ten modules results in about
of the library at < 1%. The small overhead of the library is          100 cycles overhead compared to the baseline.
dominated by the processing time of other parts of the code.             Each additional module stacked on top corresponds to an
5.4. Module Stacking Overhead                                         additional indirect function call, which results in the overhead
                                                                      of less than 10 cycles for stacking a single module. Moreover,
In this experiment we measure the scalability of the imple-           our results suggest that the overhead per stacked module stays
mentations module stacking. We repeat the same experiment             constant when more modules are stacked. With this experi-
of section 5.1, but we now stack ten null modules on top of the       ment we have shown that CleanQ’s stacking functionality is
loopback module. The null module mimics a no-op: it only              efficient.


                                                                  9
          Figure 13: Overhead of stacking queues                                   Figure 15: Performance of UDP queue

5.5. Debug Module Overhead                                             additional 50-80 cycles are dwarfed by the 3450 cycles pro-
                                                                       cessing time of our simple example application (Memcached)
In this experiment we measure the overhead of the debug                resulting in less than 2% overhead.
module that performs additional checks of buffer ownership
on every queue operation.                                              5.6. UDP Queue
   We repeat the experiment of section 5.1 with the only dif-
ference being that we stack the debug module on top of the             In this benchmark we show that we can implement a more
loopback module. Again we perform 100,000 repetitions and              complex construct based on our stacking mechanism to realize
measure the total execution time of each module in the stack.          a high-performance, low overhead UDP network stack sim-
                                                                       ilar to that in the Arrakis system [37]. This benchmark was
                                                                       implemented on the microkernel OS.
                                                                          This benchmark consists of a UDP/IP echo server using
                                                                       CleanQ: a UDP module and an IP/Ethernet module both
                                                                       stacked on top of the e10k module which drives the Intel
                                                                       X520 dual-port 10GbE card. The resulting queue is a stack
                                                                       of three modules. The network card has a distinct queue for
                                                                       transmit and receive and for each of the two hardware queues
                                                                       we initialize a CleanQ stack. Note, the e10k module will need
                                                                       to convert from and to the descriptor format the network card
                                                                       understands. We generate 64-byte UDP packets and send them
                                                                       to the echo server with the CleanQ stack. We measure the
            Figure 14: Overhead of debug queue
                                                                       processing time for sending and receiving the packet on the
                                                                       echo server.
   Figure 14 shows the median completion time for each opera-             Figure 15 shows the median and standard deviation based
tion including standard errors. We observe an overhead for the         on 100,000 measured packets for the e10k module and the
additional checks and stacking of the debug module of about            rest of the UDP network stack (Ethernet/IP/UDP) combined.
50-80 cycles for the enqueue and dequeue operations respec-            We observe a much higher standard deviation compared to
tively and a total duration of 120-130 cycles. The deregister          previous experiments.
operation only adds about 20 cycles of overhead. Register is              On investigation, this latency distributed is heavily bimodal:
the most expensive operation adding 300 cycles.                        the latency highly depends on whether the NIC hardware reg-
   The results show that even with tracking ownership, which           isters need to be updated. A write to the device register results
requires lookup and updating internal data structures to re-           in a 10x increase of the enqueue operation, but is only per-
flect the change of ownership, we observe a total completion           formed for a small fraction of enqueues. How frequently this
time for the two fast-path operations of less than 130 cycles.         expensive register write occurs depends on load and batching
Deregister simply checks whether the region has been regis-            heuristics, but is inherent in the hardware and not a feature of
tered before and then removes it if all buffers are owned by           CleanQ per se.
the caller, resulting in low overhead. The register operation             Enqueuing buffers into the transmit and receive queues of
requires verifying the size and access rights which requires a         the NIC take about 90 cycles whereas processing the UDP
syscall in our implementation, resulting in a 2x increase which        module takes about 100-250 cycles. When a buffer is written
is, however, still less that 0.3µs                                     into the hardware descriptor queue, the descriptor needs to
   Putting the overhead of the debug into perspective, despite         be formatted which takes most of the 90 cycles. The work
an increase of up to 2x relative to the loopback module, the           done by the UDP module includes growing the valid pointers


                                                                  10
                         Pkt/s      Standard deviation                  stack using CleanQ reached 742,600 pkts/s. Incorporating the
          DPDK          705,000           3362                          CleanQ interface into DPDK resulted in similar performance
         CleanQ         713,100           7305                          while implementing a UDP stack using only CleanQ increased
       CleanQ UDP       742,600           5066                          performance by 5%.
                                                                           This result shows that incorporating a CleanQ into a high-
     Table 1: DPDK vs. CleanQ vs. CleanQ UDP results                    performance networking framework (DPDK) does not degrade
of the buffer to make space for the network headers as well             throughput and can even deliver better performance.
as formatting the UDP, IP and Ethernet headers including the            5.8. Discussion
generation of checksums which account for the majority of
the 250 cycles latency.                                                 In the evaluation we demonstrated that CleanQ provides a
   Dequeuing from the NIC queue is generally more expensive             clean and well defined queue abstraction with a strong notion
than enqueuing descriptors which result in 200-400 cycles               of ownership transfer while still being lightweight (compared
latency. Dequeuing on the UDP module takes 20 cycles on the             to full stack verification) and able to deliver comparable per-
transmit queue and 120 cycles on the receive path. Whenever             formance to Virtio’s virtqueue in a direct comparison. We
the NIC completes a descriptor it updates the status bit of             have shown a C implementation of CleanQ with low overhead
the descriptor which in turn ends up in main memory or the              in absolute numbers as well as when used in an application
last level cache introducing latency (90-150 cycles) when the           context the resulting overhead to be less than 1% of the receive
descriptor is read by software. Moreover, the UDP module                and processing time of Memchached get/set request. We fur-
needs to verify the headers on the received descriptors.                ther show the that the overhead of CleanQ is not only dwarfed
   To summarize, the performance characteristics of the hard-           by application processing time but also by interfacing with the
ware descriptor queues is generally dominated by the cost of            hardware itself such as by formatting descriptors and writing
formatting a descriptor and updating the register containing            registers.
the receive and send pointers. Moreover, writing hardware                  Furthermore, we have demonstrated CleanQ’s flexibility in
registers to inform the card about the software state can be ex-        building efficient protocols and adding strict bounds checks by
pensive (> 3000 cycles) and batching the updates can amortize           stacking of modules – a feature which is enabled by the well
the cost which is the source of the large variance in this ex-          defined abstraction of CleanQ. We have shown that stacking
periment. We conducted similar experiments on a SolarFlare              a module has a small overhead and is scalable to multiple
SNF5122F with comparable results.                                       modules. Finally, we have demonstrated this functionality by
   Putting this into comparison of the library overhead, format-        implementing a UDP network stack.
ting a descriptor costs twice as much as our interface abstrac-
tion.
                                                                        6. Conclusion
                                                                        CleanQ demonstrates that it is possible to unify many of the
5.7. DPDK
                                                                        proliferation of descriptor queues in common usage behind a
In this benchmark we want to show that the CleanQ interface             single interface with strict formal semantics, at no performance
can also be integrated into existing systems without degrading          cost on the dataplane.
performance.                                                               The benefits begin with the elimination of many subtle bugs
   We implemented a module based on the DPDK Intel ixgbe                which appear (and reappear) whenever such an interface is
driver for the (i82599-based) Intel X520. We reuse the setup            defined informally. These include failing to catch all the us-
code and control plane of DPDK [28] but reimplement the                 age cases, as well as different interpretations of the interface
dataplane as a CleanQ module. Additionally, we stacked the              between client and implementation (which a strict formal spec-
UDP stack on top of the NIC CleanQ module.                              ification prevents). The ownership-transfer model of CleanQ is
   We compare the CleanQ module (and the UDP stack) to                  sound under lock-free concurrency, and provides a framework
the original DPDK driver, measuring the packets per second              for the verification of implementations.
of a single NIC queue using one core running a UDP echo                    The many CleanQ modules already implemented show that
server implemented using DPDK routines (send/recv burst).               such an interface is widely applicable within an OS, and also
Furthermore, we also measure the performance of the CleanQ              permits the composition of modules to provide reuse of func-
UDP stack directly using the CleanQ interface. To generate              tionality.
load we implemented a benchmark using standard sockets. On                 Moreover, this generality, composability, and soundness
each core we run a thread which sends and receives the UDP              come at a low cost: CleanQ matches Virtio for operation
packets in a closed loop with a configurable amount of packets          latency and imposes less than 1% overhead on end-to-end
in flight. Table 1 shows packets per second (median of 10               application workloads such as Memcached.
runs) using minimum-sized packets.                                         The Isabelle/HOL formalisations will be published sepa-
   DPDK alone achieves a throughput of 705,000 pkts/s while             rately as an extended technical report, and all CleanQ modules
DPDK using CleanQ achieved 713,100 pkts/s and the full UDP              and support code will be released under an open source license.


                                                                   11
References                                                                         [23] Norman C. Hutchinson and Larry L. Peterson. The X-Kernel: An
                                                                                        Architecture for Implementing Network Protocols. IEEE Trans. Softw.
 [1] Zach Amsden, Daniel Arai, Daniel Hecht, Anne Holler, Pratap Subrah-                Eng., 17(1):64–76, January 1991.
     manyam, and Vmware Inc. VMI: An Interface for Paravirtualization,             [24] Intel Corporation. Intel 82571 1 GbE Controller: Datasheet.
     2006.
 [2] June Andronick, Corey Lewis, Daniel Matichuk, Carroll Morgan, and             [25] Intel Corporation.       PCIe GbE Controllers Open Source Soft-
     Christine Rizkallah. Proof of OS scheduling behavior in the presence               ware Developer’s Manual 631xESB/632xESB, 82563EB/82564EB,
     of interrupt-induced concurrency. In Jasmin Christian Blanchette and               82571EB/82572EI & 82573E/82573V/82573L, 2009. Revision 2.3.
     Stephan Merz, editor, International Conference on Interactive Theorem         [26] Intel Corporation. Intel 82576 Gigabit Ethernet Controller Datasheet,
     Proving, pages 52–68, Nancy, France, August 2016. Springer.                        December 2010. Revision 2.61.
 [3] Matias Bjørling, Jens Axboe, David Nellans, and Philippe Bonnet.              [27] Intel Corporation. Intel 82599 10 GbE Controller Datasheet, December
     Linux Block IO: Introducing Multi-queue SSD Access on Multi-core                   2010. Revision 2.6.
     Systems. In Proceedings of the 6th International Systems and Stor-            [28] Intel Corporation. Data plane development kit. https://www.dpdk.
     age Conference, SYSTOR ’13, pages 22:1–22:10, Haifa, Israel, 2013.                 org/. August 2018.
     ACM.                                                                          [29] Intel Corporation.       Intel ethernet converged network adapter
 [4] Broadcom. Standard Broadcom NetXtreme II Family Highly Integrated                  x520.            https://www.intel.com/content/www/us/en/
     Media Access Controller, October 2008. Revision PG203-R.                           ethernet-products/converged-network-adapters/
 [5] David Cock, Gerwin Klein, and Thomas Sewell. Secure Microkernels,                  ethernet-x520-server-adapters-brief.html.                       August
     State Monads and Scalable Refinement. In Proceedings of the 21st                   2018.
     International Conference on Theorem Proving in Higher Order Logics,           [30] Intel Corporation. Seiral ata advanced host controller interface
     TPHOLs ’08, pages 167–182, Berlin, Heidelberg, 2008. Springer-                     (ahci) 1.3.1. https://www.intel.com/content/www/us/en/io/
     Verlag.                                                                            serial-ata/serial-ata-ahci-spec-rev1-3-1.html. August
 [6] MITRE Corporation. CVE-2017-9986,. https://cve.mitre.org/                          2018.
     cgi-bin/cvename.cgi?name=CVE-2017-9986. November 2017.                        [31] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick,
 [7] CVE Details. CVE-2004-0555. https://www.cvedetails.com/                            David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt,
     cve/CVE-2004-0555/. July 2004.                                                     Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and
                                                                                        Simon Winwood. seL4: Formal Verification of an OS Kernel. In
 [8] CVE Details. CVE-2008-1317. https://www.cvedetails.com/                            Proceedings of the ACM SIGOPS 22Nd Symposium on Operating
     cve/CVE-2008-1317/. March 2008.                                                    Systems Principles, SOSP ’09, pages 207–220, Big Sky, Montana,
 [9] CVE Details. CVE-2010-1187. https://www.cvedetails.com/                            USA, 2009. ACM.
     cve/CVE-2010-1187/. Oktober 2010.                                             [32] Alexander Krizhanovsky. Linux Netlink Mmap: Bulk Data Transfer
[10] CVE Details. CVE-2015-1805. https://www.cvedetails.com/                            for Kernel Database. http://natsys-lab.blogspot.com/2015/
     cve/CVE-2015-1805/. August 2015.                                                   03/linux-netlink-mmap-bulk-data-transfer.html. March
[11] CVE Details. CVE-2015-5366. https://www.cvedetails.com/                            2015.
     cve/CVE-2015-5366/. August 2015.                                              [33] Feng Liu, Nayden Nedev, Nedyalko Prisadnikov, Martin Vechev, and
[12] CVE Details. CVE-2015-7613. https://www.cvedetails.com/                            Eran Yahav. Dynamic Synthesis for Relaxed Memory Models. In
                                                                                        Proceedings of the 33rd ACM SIGPLAN Conference on Programming
     cve/CVE-2015-7613/?q=CVE-2015-7613. September 2015.                                Language Design and Implementation, PLDI ’12, pages 429–440,
[13] CVE Details. CVE-2016-5403. https://www.cvedetails.com/                            Beijing, China, 2012. ACM.
     cve/CVE-2016-5403/. August 2016.
                                                                                   [34] Luc Maranget, Susmit Sarkar, and Peter Sewell. A Tutorial Introduction
[14] CVE Details. CVE-2016-7618. https://www.cvedetails.com/                            to the ARM and POWER Relaxed Memory Models. 2012.
     cve/CVE-2017-7618/. August 2017.
                                                                                   [35] David S. Miller. How skbuffs work. Onlin., http://vger.kernel.
[15] CVE Details. CVE-2017-14916. https://www.cvedetails.com/                           org/~davem/skb.html.
     cve/CVE-2017-14916/. December 2017.
                                                                                   [36] Susan Owicki and David Gries. An axiomatic proof technique for
[16] Peter Druschel and Larry L. Peterson. Fbufs: A High-bandwidth                      parallel programs i. Acta Inf., 6(4):319–340, December 1976.
     Cross-domain Transfer Facility. In Proceedings of the Fourteenth
     ACM Symposium on Operating Systems Principles, SOSP ’93, pages                [37] Simon Peter, Jialin Li, Irene Zhang, Dan R. K. Ports, Doug Woos,
     189–202, Asheville, North Carolina, USA, 1993. ACM.                                Arvind Krishnamurthy, Thomas Anderson, and Timothy Roscoe. Ar-
                                                                                        rakis: The Operating System is the Control Plane. In Proceedings of
[17] Brad Fitzpatrick. Distributed Caching with Memcached. Linux J.,                    the 11th USENIX Conference on Operating Systems Design and Im-
     2004(124):5–, August 2004.                                                         plementation, OSDI’14, pages 1–16, Broomfield, CO, 2014. USENIX
[18] Shaked Flur, Kathryn E. Gray, Christopher Pulte, Susmit Sarkar, Ali                Association.
     Sezgin, Luc Maranget, Will Deacon, and Peter Sewell. Modelling                [38] David Leo Presotto. Multiprocessor Streams for Plan 9. In in Proceed-
     the ARMv8 Architecture, Operationally: Concurrency and ISA. In                     ings of the United Kingdom UNIX User Group Summer Proceedings,
     Proceedings of POPL: the 43rd ACM SIGPLAN-SIGACT Symposium                         pages 11–19, 1993.
     on Principles of Programming Languages, 2016.
                                                                                   [39] Realtek Semi-Conductor Co., Ltd. RTL8029AS: Realtek PCI Full-
[19] Andrew Friedley, Torsten Hoefler, Greg Bronevetsky, Andrew Lums-                   Duplex Ethernet Controller with built-in SRAM, January 1997.
     daine, and Ching-Chen Ma. Ownership Passing: Efficient Distributed
     Memory Programming on Multi-core Systems. In Proceedings of the               [40] RedHat.       CVE-2015-9016.         https://access.redhat.com/
     18th ACM SIGPLAN Symposium on Principles and Practice of Parallel                  security/cve/cve-2015-9016. August 2015.
     Programming, PPoPP ’13, pages 177–186, Shenzhen, China, 2013.                 [41] RedHat.       CVE-2017-17381.        https://access.redhat.com/
     ACM.                                                                               security/cve/cve-2017-17381. November 2017.
[20] John Giacomoni, Tipp Moseley, and Manish Vachharajani. Fastforward            [42] D.M. Ritchie. A stream input-output system. AT&T Bell Laboratories
     for efficient pipeline parallelism: A cache-optimized concurrent lock-             Technical Journal, 63:1897–1910, 10 1984.
     free queue. In Proceedings of the 13th ACM SIGPLAN Symposium on
     Principles and Practice of Parallel Programming, PPoPP ’08, pages             [43] Rusty Russell. Virtio: Towards a De-facto Standard for Virtual I/O
     43–52, New York, NY, USA, 2008. ACM.                                               Devices. SIGOPS Oper. Syst. Rev., 42(5):95–103, July 2008.
[21] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan Wu, Jieung Kim, Vil-               [44] Peter Sewell, Susmit Sarkar, Scott Owens, Francesco Zappa Nardelli,
     helm Sjöberg, and David Costanzo. CertiKOS: An Extensible Archi-                   and Magnus O. Myreen. X86-TSO: A Rigorous and Usable Program-
     tecture for Building Certified Concurrent OS Kernels. In Proceedings               mer’s Model for x86 Multiprocessors. Commun. ACM, 53(7):89–97,
     of the 12th USENIX Conference on Operating Systems Design and                      July 2010.
     Implementation, OSDI’16, pages 653–669, Savannah, GA, USA, 2016.              [45] Solarflare Communications, Inc. Solarflare SFN5122F Dual-Port
     USENIX Association.                                                                10GbE Enterprise Server Adapter, 2010.
[22] Sangjin Han, Scott Marshall, Byung-Gon Chun, and Sylvia Ratnasamy.            [46] Pengfei Wang, Jens Krinke, Kai Lu, Gen Li, and Steve Dodier-Lazaro.
     MegaPipe: A New Programming Interface for Scalable Network I/O.                    How double-fetch situations turn into double-fetch vulnerabilities: A
     In Proceedings of the 10th USENIX Conference on Operating Systems                  study of double fetches in the linux kernel. In Proceedings of the 26th
     Design and Implementation, OSDI’12, pages 135–148, Hollywood,                      USENIX Conference on Security Symposium, SEC’17, pages 1–16,
     CA, USA, 2012. USENIX Association.                                                 Berkeley, CA, USA, 2017. USENIX Association.


                                                                              12
[47] S. Winwood, G. Klein, T. Sewell, J. Andronick, D. Cock, and M. Nor-
     rish. Mind the gap. In S. Berghofer, T. Nipkow, C. Urban, and M. Wen-
     zel, editors, Theorem Proving in Higher Order Logics (TPHOLs), vol-
     ume 5674 of Lecture Notes in Computer Science, Berlin, Heidelberg,
     2009. Springer-Verlag.




                                                                             13
