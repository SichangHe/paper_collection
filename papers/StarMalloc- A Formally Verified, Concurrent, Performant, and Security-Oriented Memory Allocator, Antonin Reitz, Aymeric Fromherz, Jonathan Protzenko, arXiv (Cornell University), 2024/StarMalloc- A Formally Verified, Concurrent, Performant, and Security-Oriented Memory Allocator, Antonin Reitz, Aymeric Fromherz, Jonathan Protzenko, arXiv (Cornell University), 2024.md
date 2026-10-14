                                         StarMalloc: A Formally Verified, Concurrent, Performant, and
                                         Security-Oriented Memory Allocator
                                         ANTONIN REITZ, Inria, France
                                         AYMERIC FROMHERZ, Inria, France
arXiv:2403.09435v1 [cs.PL] 14 Mar 2024




                                         JONATHAN PROTZENKO, Microsoft Research, USA
                                         Despite the rise of memory-safe languages such as Rust or Go, most safety-critical, systems-oriented, low-level
                                         applications are still written in unsafe languages like C and C++. The reason is simple: the boundary between
                                         the OS and userland is fundamentally thought of, designed and explained in C terms through the various
                                         headers and man pages that capture the calling conventions, and thus, enshrine the C ABI as the correct level
                                         of abstraction when writing systems-oriented code. The system memory allocator (malloc, free. . . ) is a prime
                                         example. Sitting at the boundary between the OS and userland, the behavior of the system allocator was set in
                                         stone in 1989 in the C standard, and has fundamentally not changed since then. And due to its very low-level
                                         nature, an allocator must directly interface with the OS and juggle various low-level system APIs that are best
                                         accessed from C – indeed, such low-level memory management would hardly pass Rust’s borrow checker!
                                            But of all the low-level, safety-critical systems-oriented programs, the allocator is one of the very few
                                         hit with a proverbial double whammy. First, the allocator must assume the inevitable reality of software
                                         development: most client programs will be written in unsafe languages and as a result will be excruciatingly
                                         buggy. This means the allocator must go great lengths to include security mitigations against common heap
                                         vulnerabilities. But as a result a second penalty arises: the allocator itself is not only increasingly complex,
                                         but must remain written in exactly the same kind of memory-unsafe languages (e.g., C) to enjoy access to
                                         the OS APIs that it needs (e.g., mmap). Unsurprisingly, even widely-used and well-audited allocators, such
                                         as the one in glibc, have been the victim of bug reports in recent years. Given their security-critical aspect,
                                         allocators thus require strong, formal guarantees about their correctness and safety.
                                            In this work, we present StarMalloc, a verified, security-oriented, concurrent memory allocator that can
                                         be used as a drop-in replacement in real-world projects. Using the Steel separation logic framework, we
                                         show how to specify and verify StarMalloc, relying on dependent types and modular abstractions to enable
                                         efficient verification. As part of StarMalloc, we also develop several generic datastructures and proof libraries
                                         directly reusable in future systems verification projects. We finally show that StarMalloc can be used with
                                         real-world projects, including the Firefox browser, and evaluate it against 10 state-of-the-art memory allocators,
                                         demonstrating its competitiveness.

                                         1   INTRODUCTION
                                         In recent years, memory-safe languages such as Rust and Go have significantly risen in popular-
                                         ity and adoption, and to this date remain some of the fastest-growing languages [GitHub Team
                                         2023]. However, for safety-critical, low-level applications, C and C++ remain the languages of
                                         choice, owing to their ability to interact with the operating system and the memory in extremely
                                         low-level ways. While C and C++ allow developers to achieve high performance, particularly in
                                         resource-contrained environments, C and C++ are also fundamentally memory-unsafe, meaning
                                         they empower developers with the ability to “shoot themselves in the foot” with great ease, resulting
                                         in a rich cornocupia of well-known attack vectors, and especially of memory corruption bugs [Szek-
                                         eres et al. 2013]. Indeed, recent studies by Google [Chromium Project 2020] and Microsoft [MSRC
                                         Team 2019] estimate that memory-related errors, e.g., buffer overflows or dangling pointers, are
                                         the root cause of 70% of the security vulnerabilities in widely deployed software.
                                            Since no one in their right mind would expect the software industry to rewrite everything (and
                                         especially legacy code) in Rust, we now ask: what can be done to mitigate the impact of incorrect

                                         Authors’ addresses: Antonin Reitz, Inria, Paris, France, antonin.reitz@inria.fr; Aymeric Fromherz, Inria, Paris, France,
                                         aymeric.fromherz@inria.fr; Jonathan Protzenko, Microsoft Research, Redmond, USA, protz@microsoft.com.
2                                                                                              Reitz et al.


memory management in existing software codebases? As argued by Berger [2012], “the software
industry is in a position similar to that of the automobile industry of the 1950s, delivering software
with lots of horsepower and tailfins but no safety measures of any kind”. One particular such airbag
is the memory allocator, which oftentimes is the last line of defense against incorrect memory
management performed by the client program. Realizing this, modern memory allocators [Berger
and Zorn 2006; GrapheneOS Development Team 2021; Leijen et al. 2019; LLVM Project 2023; Novark
and Berger 2010; Silvestro et al. 2017] often include mitigations against common heap vulnerabilties,
for instance by randomizing allocations, or separating heap metadata from the heap itself. The net
effect is that attacks are harder to conduct, and as such the allocator successfully provides some
degree of protection against incorrect programs.
   Alas, allocators themselves are not immune to the kind of bugs they are supposed to defend
against! They are typically written in C/C++; and because they stand on the critical path of most, if
not all, client programs, allocators also must fulfill numerous goals [Wilson et al. 1995], such as: high
performance; low memory consumption; maximizing concurrency; minimizing heap contention;
and so on. Meeting these goals requires custom data structures and low-level pointer and bit
manipulations, and typically entails bugs: even widely used and audited allocators such as glibc are
not immune, and several issues were reported in recent years [glibc 2017a,b, 2020; MSRC Team
2021; MySQL 2019; Portal 2013; Sautereau 2021; Theftguy 2020].
   Because allocators are so critical, they deserve, in our opinion, the highest degree of assurance;
that is, allocators ought to be formally verified, in order to guarantee that no matter the input, they
will always correctly and safely maintain their data structures and invariants, hence functional
correctness. Formal verification has been successfully applied to a variety of application domains,
such as compilers [Barthe et al. 2020; Kumar et al. 2014; Leroy 2006], operating systems [Gu et al.
2016; Klein et al. 2018, 2009], and cryptography [Almeida et al. 2020; Appel 2015; Erbsen et al.
2019; Polubelova et al. 2020; Protzenko et al. 2020; Ye et al. 2017]. Formal verification has also
been applied to memory allocators [Appel and Naumann 2020; Gu et al. 2016; Jiang et al. 2019;
Mangano et al. 2016; Marti et al. 2006; Sahebolamri et al. 2018; Sammler et al. 2021; Tuch et al. 2007].
But to the best of our knowledge, formal verification was never applied to a real-world allocator,
complete with advanced book-keeping data structures, sharded allocation pools and performance
optimizations, fine-grained concurrency, defensive security mitigations, and so on; in short, there
is no verified, state-of-the-art modern memory allocator.
   We posit there are several reasons for this glaring omission from the formal verification landscape.
First, the secure allocator community has little overlap with the PL community, meaning there
are many well-established, peer-validated allocator designs, but they have yet to be subjected to
formal verification; in other words, the difficulty today lies not in proving a design secure, but
rather in proving its implementation secure. As a consequence, a second possible explanation is
that verifying a real-world, system allocator is a veritable challenge. The allocator sits below the
usual level of abstraction of typical verification frameworks; requires extensive modeling of the
environment, and notably the behavior of a variety of OSes and their APIs that each vary in slightly
non-POSIX ways, a notoriously tedious task; and requires verifying data structures with punishing
amounts of complexity, entangling as many as five linked lists together. For all of these reasons,
we are not aware of any real, secure, verified allocator that is simultaneously performant, features
the latest security features, and can act as a drop-in replacement for malloc, free, and the myriad of
slightly non-standard auxiliary APIs that must be implemented nonetheless for “real-world” use.
   In this work, we propose StarMalloc, the first verified, real-world, efficient, security-oriented,
concurrent memory allocator. Our design is based on hardened_malloc [GrapheneOS Development
Team 2021], a scalable, security-focused, general purpose memory allocator with a focus on long-
term performance and memory usage. Doing so, we leverage the latest advances in allocator design,
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                   3


embrace a solution that has met the approval of the security community and whose merits are not
up for debate, all the while providing a state-of-the-art and verified allocator. StarMalloc comes as
C code; our theorems show that we not only avoid memory errors (such as out of bounds accesses
within the allocator’s internal data structures), but also functionally behave like an allocator, even
with a complex design (slabs, separate metadata, contiguous size classes, bitmaps and bit-level
arithmetic, doubly-linked lists within a static array, AVL trees with constant-time metadata access,
FIFO queues) that incorporates additional security mechanisms (zeroing, guard pages, quarantine).
   StarMalloc is authored and verified using the F★/Steel [Fromherz et al. 2021; Swamy et al. 2016]
separation logic framework, and is readily available as a C library. Our code is open-source, and
extensive testing has shown that StarMalloc can provide a drop-in replacement for the system
allocator on real-world programs. Our contributions are the following: .
• A new specification logic specification of a memory allocator and its security defense mechanisms
• A collection of base libraries for the verification of low-level, raw memory-manipulating programs
• A modular approach to verification with multiple layers that leverages dependent types and
ML-style abstractions
• A verified implementation of a security-oriented allocator, StarMalloc
• An evaluation against 10 existing memory allocators on widely used benchmarks and real-world
projects, including Mozilla Firefox, showing performance to be competitive.


2     RELATED WORK
2.1    Toward Secure Memory Allocators
Dynamic memory allocation in its current form stems from the original 1989 version of the C
standard which specifies malloc, calloc, realloc and free. Since 1989, the purpose has remained the
same: to provide a portable, abstract interface between the OS and the client program. Each operating
system exposes a system call that allows a process to request more memory (originally brk, later
on, with the advent of virtual memory, mmap or VirtualAlloc). Relying on this OS-specific system
call, the allocator grows the heap as needed (to avoid too-frequent syscalls) and maintains internal
book-keeping data structures that allow it to service the allocation and de-allocation requests
from the client program. The client program, by virtue of relying on the system-provided dynamic
memory allocator, is happily unaware of all of these implementation details.
   Even though the mandate of an allocator is simple, the design space for possible implementation is
large [Wilson et al. 1995]. As noted in the introduction, the allocator must satisfy several constraints
that are oftentimes at odds with each other: low fragmentation, good multithreaded behavior, cache
locality, great performance, and of course, security. What constitutes a good design also changes
over time: one notable inflexion point in the design of allocators happened in the late 2000s, when
better benchmarking increased awareness of fragmentation; combined with the generalization of
multi-processor systems, this led to a new generation of allocators, the most notable of which is
jemalloc [Evans 2006], which became the standard in Mozilla Firefox and many BSDs.
   More recently, the seemingly never-ending stream of memory vulnerabilities led to new designs:
state-of-the art allocators not only enjoy high performance, but also now incorporate security at
their core. Security concerns led to typed memory allocators [Akritidis 2010; van der Kouwe et al.
2018], allocators for tagged memory (e.g., CHERI [Bramley et al. 2023; Watson et al. 2019]), or
hardened memory allocators [Berger and Zorn 2006; Felker 2020; GrapheneOS Development Team
2021; Leijen et al. 2019; LLVM Project 2023; Novark and Berger 2010; Silvestro et al. 2017]. In short,
designing a “good” memory allocator remains an active research area, and incorporating defensive
security measures is now de rigueur.
4                                                                                              Reitz et al.


2.2   Verified Memory Allocators
Given their critical aspect, userspace memory allocators have long been considered an interest-
ing target for formal verification. Using the Isabelle/HOL proof assistant [Nipkow et al. 2002],
Sahebolamri et al. [2018] verify a simple sequential memory allocator where a linked list inter-
twined with data keeps track of allocation units. This is akin to the original design explained
in the K&R book [Kernighan and Ritchie 1988], but a far cry from what modern allocators do.
Appel and Naumann [2020] verify an array-of-bins malloc/free system using the Verified Software
Toolchain [Appel 2011] embedded in Coq. Their implementation does not support concurrency (it is
single-threaded), and is intended for use with verified clients, meaning it is unsuitable in adversarial
settings. They do, however, add extra reasoning in Coq to model resource awareness and exhaustion.
Sammler et al. [2021] develop a methodology to verify C code using the Iris framework [Jung et al.
2018, 2015; Krebbers et al. 2017], and apply it to the verification of a small thread-safe allocator con-
sisting of 68 lines of code. An illustrative example fits within 68 lines of code, but a modern memory
allocator that meets state-of-the-art, “real-world” constraints needs more than that. Wickerson
et al. [2010] use rely-guarantee [Jones 1983], a verification technology that predates the widespread
adoption of separation logic, to verify the Unix Version 7 memory manager. Unix version 7 was
released in 1979, and its memory manager relies on sbrk, which according to its man page is a
“historical curiosity”. Many other works [Fang et al. 2018; Yu et al. 2003] verify simplistic memory
allocators, but to the best of our knowledge, none verify a state-of-the-art, competitive, real-world
allocator. One exception is Zhang et al. [2019], which verifies a non-trivial allocator design, except
they operate on a specification, and have no actual implementation.
   Perhaps more importantly, none of these allocators are intended to act as drop-in replacements
for the system allocator, and have not been evaluated as such. Based on a combination of careful
examination of the papers above, and personal communications with some of the authors, it is our
understanding that none of these allocators ever intended to be usable in the real world. This is by
no means shocking: providing a system allocator requires implementing a wide API surface (both
POSIX and non-standard but widely used APIs), while also deploying sophisticated implementation
techniques to provide performance and security. In short, all of the userspace allocators we are
currently aware of are proof-of-concepts, written without performance or security in mind, and as
such without any ambition to act as deployable system components.
   Beyond userspace allocators, previous verification projects aimed to provide verified operating
systems and microkernels, which thus required kernel space memory management [Gu et al. 2016;
Mangano et al. 2016; Marti et al. 2006; Tuch et al. 2007]. Being located in the kernel, these allocators
have different constraints. First, kernels have a lot of static data structures so these allocators do
not need to service as many small heap-based allocations; second, kernels oftentimes have global
locks for data structures [Peters et al. 2015], meaning concurrency isn’t as much of a concern for
the allocator. Furthermore, in the context of verified OS kernels like above, additional proofs ensure
that the in-kernel allocator does not need to be defensive against other parts of the kernel, which
means even in this context, a full-fledged defensive general-purpose security-oriented allocator
was not typically the object being studied.
   One last area of related work to note is that of automatic memory management runtime systems,
i.e., garbage collectors. Automatic memory management has received more attention from the
verification community, with numerous runtime systems and garbage collectors being studied
and verified, starting with Doligez and Gonthier [1994]; Doligez and Leroy [1993], all the way to
CakeML’s verified runtime system and GC [Sandberg Ericsson et al. 2019]. We speculate that this is
due to a proximity between the theorem proving community and the garbage-collected, functional
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                                                      5


                          regular allocations mmap’d memory region                                       metadata mmap’d memory region


    Size Class 16
                                                                     Metadata 16               partial       empty       full
                          0x0000      0x1000          0xffffff000
    start = 0x0000
                                                …
                                                                            full

                           slab        slab             slab                empty

                                                                            partial
                                                                                                                                 …
                                                                            quarantine, etc.




    Size Class 32                                                    Metadata 32
    start = 0x100000000

    etc.                                                             etc.



Fig. 1. Architecture of StarMalloc. All regular allocations live in a single mmap’d memory region (left). All
metadata lives in a single distinct mmap’d memory region (right). All allocations are contiguous. All metadata
is contiguous. Accessing the n-th slab of the m-th size class thus boils down to pointer arithmetic, and
similarly for the metadata. We rely on virtual memory to ensure only in-use pages occupy memory. Only a
single arena is shown for conciseness; other arenas and their metadata are laid out contiguously in the same
two mmap’d regions.



languages that they reason about and are implemented in (e.g., OCaml). Alas, we do not see how to
reuse the foundational background of GC systems in the context of manual memory allocation.

3     DESIGN AND OVERVIEW OF STARMALLOC
In this work, we design, implement and verify StarMalloc. Many of our design choices leverage hard-
ened_malloc [GrapheneOS Development Team 2021], a modern, security-oriented memory allocator
heavily based on the OpenBSD malloc design. We therefore inherit many of hardened_malloc’s
advantages, such as low memory fragmentation, low contention, a security-oriented default design,
and good long-term performance and scalability. To achieve these goals, hardened_malloc, and
therefore StarMalloc, rely on a variety of technical choices. We informally review and describe
these design choices here; Section 4 formally captures those same design choices in F★.

3.1        System Architecture
Figure 1 describes the overall architecture of StarMalloc. We proceed top-down, and describe the
sequence of steps taken in order to fulfill a memory allocation request.
AVL tree for large allocations. If the allocation exceeds the page size (4kB), it is deemed a “large
allocation”. Large allocations are tracked in an auxiliary map, implemented using an AVL tree (not
shown in Figure 1). Large allocations are directly forwarded to the OS (via mmap); once the syscall
returns, StarMalloc receives a fresh address of the desired size; inserts a new entry into the AVL
tree that maps the fresh address to its size; and returns the fresh address to the client. (We explain
in the free paragraph, below, why keeping track of the large allocation size is important.)
Memory-mapped region for regular allocations. If the allocation is equal to, or smaller than
the page size (4kB), it is a regular allocation. Relying on modern OSes and their treatment of virtual
memory, we perform a single call to mmap at allocator initialization-time, which reserves a region
of virtual memory for all regular allocations. At the beginning, none of the corresponding pages
are used; unless the client program allocates substantial amounts of memory, the virtual memory
manager guarantees that the actual memory usage will be correspondingly low. Throughout
StarMalloc, we take care to return unused pages to the OS to be used for other purposes, but retain
the virtual address space which remains unchanged throughout the execution of the program.
6                                                                                               Reitz et al.


Arenas. The large memory region for regular allocations is first subdivided into arenas. The number
of arenas is set at compile-time; using thread-local storage, we associate an arena to each thread.
Arenas are not protected by locks, which operate at a smaller level of granularity. The point of
arenas is to spread out allocations in order to statically reduce contention. The allocator looks up
the arena associated to the current thread, then proceeds within this arena.
Size classes. Each arena is further subdivided into size classes, which contain allocations of a given
size; each regular allocation is rounded up to the nearest available size class. Just like the number
of arenas, the number of size classes is fixed: there are 27 size classes for different multiples of
16 bytes up to the page size. (We show later in this paper how StarMalloc is written for a generic
number of size classes, which the user can trivially adjust at F★ compile-time. This paves the way
for further extensions, e.g., handling ARM’s 64kB large pages.)
   Thanks to virtual memory, only the portions of each size class that are in use are backed by
physical memory. Each size class is associated to metadata that needs to be updated whenever an
allocation takes place within that size class: for that reason, size classes are each protected by an
individual lock. Recall that the mapping of threads to arenas is not injective (the number of arenas
is fixed): the lock thus prevents two threads from racing to allocate within the same size class.
Slabs. Each size class is made up of slabs. A slab is exactly one page, divided into allocation units,
called slots. All slabs within a size class are divided into the same slot size. That is, within the 4kB
size class, each slab contains one slot; and within the 32B size class, each slab contains 128 slots.
   Each size class tracks all of its slabs using size class metadata. The metadata keeps track of free
slabs, and to reduce memory fragmentation, it also separately tracks partially filled slabs, which are
prioritized for allocation. The tracking of all three kinds of slabs is achieved using doubly-linked lists
to efficiently insert/remove when implementing malloc/free. Additionally, the size class metadata
contains another two extra lists for security (detailed in Section 3.2). (In practice, our lists have a
special marker for the last used slab, so as not to initially contain, e.g., 1M elements for the list of
free slabs.)
   To fulfill an allocation request, the allocator acquires the lock for that size class, looks for a
partial of free slab (i.e., one where there is space left) in the metadata, then proceeds.
Slots. Each slab is made up of individual slots. The design of StarMalloc ensures that each individual
allocation is aligned to 16 bytes, which guarantees better performance on modern processors. To
keep track of which slots are used or available within a given slab, StarMalloc maintains slab
metadata; in practice, this is a bitmap. We eschew free lists, because we cannot guarantee that
an attacker will be unable to corrupt them, even in the presence of an encoding. Conversely, our
bitmaps live in a separate mmap’d region, which ensures that an attacker cannot materialize the
metadata virtual address. This is the final step for the allocator: once a suitable slab is identified, a
slot is taken within that slab, the slab metadata is updated, the size class lock is released, and the
address of the corresponding slot is returned to the client program.
Freeing. In order to free, the allocator first performs a pointer comparison to determine whether
the pointer belongs to the mmap’d region of regular allocations. If so, further pointer difference
operations and bit manipulations allow determining the arena and size class that the pointer
belongs to. StarMalloc then acquires the relevant lock, locates the suitable slab, updates the bitmap
(slab metadata), size class metadata, then releases the lock. If this leads to a new empty slab, the
corresponding slab is moved to quarantine (more on quarantine below), and returned back to the OS
by calling mmap to modify the flags for that page. Should the pointer be invalid (i.e., not correspond
to a slot), the allocator leaves the bitmap unchanged and releases the lock. If the pointer belongs to
none of the allocator’s arenas, then the pointer must be a large allocation. A lookup in the AVL map
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                    7


allows i) ensuring that the pointer is indeed valid, and ii) retrieving its size. This allows StarMalloc
to call munmap, which given a pointer and its size, releases the corresponding pages back to the OS.
Concurrency. We mentioned above how our design relies on locks for size classes. We note that
this is a fine-grained concurrency design, aiming to mitigate contention. A lock-free allocator would
be ideal, but to the best of our knowledge, cannot be implemented using segregated metadata, which
is a crucial security feature we are not willing to relinquish. Conversely, large-grained concurrency
at the level of arenas would be highly undesirable. Several threads may be concurrently touching
the same arena, but in different size classes; fine-grained locks avoid needless contention on that
arena. We remark that if, even in the presence of our fine-grained locks, contention is still an issue,
the user can increase the number of arenas to better support highly threaded programs.



3.2   Allocator Hardening
Our design not only incorporates all of the mechanisms described above, but adds extra mechanisms
in order to defend against heap corruption vulnerabilities. This is consistent with our earlier claim
that the allocator is the last line of defense, but also highlights the need for verification: the design
above is non-trivial with many subtle invariants, and becomes even more so once the security
mechanisms are added. Many hardening techniques have been, and continue to be proposed. We
adopt the most widely-implemented ones amongst security-oriented allocators [Yun et al. 2021],
suggesting their importance and effectiveness. We now review each one of the main security
mechanisms StarMalloc implements.
Segregated metadata. As mentioned above, our metadata lives in a separate address space (i.e., an
mmap’d region that is disjoint from the regular allocation region). If an attacker manages to write
past a given slot, the damage is limited since the allocator’s internal data structures are untouched.
Zeroing. Just like Apple’s OSX allocator [Apple Security Research 2022], we zero-out memory
upon freeing. We do this either using a cryptographic-grade secure zeroing function (regular
allocations) which is resistant to rogue C compiler optimizations, or munmap (large allocations).
This defends against an attacker observing sensitive data through a reused memory allocation slot.
Furthermore, upon allocation, we verify that the memory is still zeroed out. If not, the memory
was corrupted, and we return NULL as a further defensive security measure, rather than returning
possibly poisoned memory to the client program.
Quarantine. Once a slab becomes empty, we do not reuse it immediately and instead keep it in
quarantine. This is implemented using a fourth linked list within a given size class, which keeps
track of quarantined slabs. Unlike the other linked lists (full, empty, partial), the quarantine list
exposes a queue interface (also implemented for StarMalloc). The idea is to let the slab “cool off” to
make any subsequent accesses to any pointer in it an OS page fault error. This defends against double
frees, and generally accessing freed memory. In practice, we simply call madvise(DONT_NEED) to
return the page to the OS. Using a queue allows us to reclaim pages from quarantine (so as not to
exhaust virtual memory tables) in a first-in, first-out order, relying on customizable compile-time
parameters to specify what is a sufficiently long time before a quarantined page becomes reusable.
Guard pages. Within size classes, some of the slabs are marked as inaccessible via mmap, meaning
that any access to them causes a fault. We call these guard pages. The chief reason for guard pages
is to prevent against large buffer overruns that may attempt to linearly read past an allocation unit.
These are tracked in the final, fifth doubly-linked list.
8                                                                                               Reitz et al.


Canaries. Each slot is terminated by a canary, consisting of a magic number, which can absorb
small buffer overflows instead of corrupting the next slot. We check the integrity of a canary when
freeing a slot, which can detect overflows a posteriori (but often too late to entirely prevent attacks).

4     MODELING THE ESSENCE OF A SECURITY-ORIENTED ALLOCATOR
Section 3 provided a high-level, informal description of StarMalloc. We now show how to precisely
and accurately capture the behavior of StarMalloc, by specifying its well-formedness and functional
correctness through the use of a dependently typed concurrent separation logic. We start by
providing background about concurrent separation logic, and its encoding into F★.

4.1    Background
Concurrent Separation Logic. Separation logic [Ishtiaq and O’Hearn 2001; O’Hearn et al.
2001; Reynolds 2002] is a Hoare-style program logic that is well-suited to reasoning about heap-
manipulating programs: the Hoare triple { 𝑃 } 𝑐 { 𝑄 } represents that, if precondition 𝑃 is initially sat-
isfied, then the program 𝑐 executes without error, that is, the program is memory safe, and the post-
condition 𝑄 is satisfied when 𝑐 terminates, which can be used to specify the functional correctness of
the program. As an example, the specification of memory allocation is { 𝑒𝑚𝑝 } 𝑟 = 𝑎𝑙𝑙𝑜𝑐 (𝑣) { r ↦→ 𝑣 },
where 𝑒𝑚𝑝 corresponds to the empty predicate, always trivially true, while r ↦→ v represents that 𝑟
is live and points to the value 𝑣.
    Separation logic predicates can be composed: 𝑃 ∗ 𝑄 represents that 𝑃 and 𝑄 relate to separated
(i.e., disjoint) regions of memory. This enables modular reasoning through the separation logic
frame rule: if { 𝑃 } 𝑐 { 𝑄 } holds, then so does { 𝑃 ∗ 𝑅 } 𝑐 { 𝑄 ∗ 𝑅 }; any predicate 𝑅 relating to a
part of memory separated from the execution of 𝑐 is left unchanged.
    Concurrent Separation Logic (CSL) [Brookes 2007; O’Hearn 2007] extends separation logic to
provide guarantees in concurrent settings. In CSL, the Hoare triple { 𝑃 } 𝑐 { 𝑄 } captures the
thread-safety of the program 𝑐, namely, the memory safety and functional correctness guarantees
still hold in the presence of threads executing concurrently.
F★ and KaRaMeL. F★ [Swamy et al. 2016] is a proof assistant and program verification framework.
It allows users to write, specify, and prove programs in a functional language with a rich type
system based on dependent types and user-extensible effects [Rastogi et al. 2021]. To simplify
verification, F★ discharges proof obligations using an automated SMT solver [de Moura and Bjørner
2008], while also offering metaprogramming and tactic-based verification facilities [Martínez et al.
2019] in a style similar to Lean [Ebner et al. 2017] or Idris [Brady 2013].
   While F★ code extracts to OCaml by default, a subset of the F★ language also extracts to idiomatic
C code through the KaRaMeL compiler [Protzenko et al. 2017]. This toolchain was previously
successfully used to provide verified C implementations of security-critical applications such as
cryptographic libraries [Ho et al. 2022; Polubelova et al. 2020; Protzenko et al. 2020] or binary
parsers and serializers [Ramananandro et al. 2019; Swamy et al. 2022].
Steel. Steel [Fromherz et al. 2021; Swamy et al. 2020] is a recent framework embedded in F★ that
allows the use of concurrent separation logic to specify and prove the correctness and safety of
concurrent F★ programs. To introduce the reader to Steel and to the F★ syntax used throughout
this paper, we present below the signature of the malloc function that we aim to implement.
val malloc (size: size_t) : Steel (array uint8) emp (𝜆 r → null_or_slarray r)
  (requires 𝜆h0 → ⊤) (ensures 𝜆h0 r h1 → not (is_null r) =⇒ length r ≥ size)
  The malloc function takes as argument the number of bytes size that must be allocated. It has
the Steel effect, indicating that it belongs to the Steel framework. This effect has several indices.
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                                  9


First, array uint8 corresponds to the return type of this function. The second and third indices are
separation logic predicates, of type slprop. They mimic the specification of memory allocation we
introduced earlier: malloc consumes emp (second index), which carries no ownership, and returns
null_or_slarray r, where r refers to the returned value. slarray r is the Steel equivalent of r ↦→ _, but
applied to arrays instead of references. To faithfully model malloc according to the C standard, we
account for the fact that r may be null. Steel’s separation logic predicates can capture a rich class
of properties about memory; for this paper’s purposes, it is sufficient to see them as representing
a notion of memory ownership. The fourth and fifth indices lighten the formalism and simplify
the verification effort. In Steel, these allow us to specify properties about the contents of memory
using the requires and ensures clauses, operating on the initial memory h0 and the final memory h1.
This style has been used successfully by tools such as Dafny [Leino 2010] or Steel’s predecessor,
Low∗ [Protzenko et al. 2017], and seems to be a natural style for writing these specifications. Here,
the precondition (fourth index) is trivial. The post-condition (fifth index) states that, if the array
returned is not NULL, then its length is at least the size initially requested.
   When written in the KaRaMeL-compatible fragment, Steel code extracts to idiomatic C code. For
instance, the Steel malloc signature above will yield the following standard C function prototype:
uint8_t∗ malloc(size_t size). This signature is more precise than that of the C standard (uint8_t∗ instead
of void∗); in practice, we add a wrapper that performs a cast, so as to match the expected ABI and
thus provide a drop-in replacement for existing userspace memory allocators. In the rest of this
paper, we go over the various steps that ultimately produce a memory allocator satisfying this Steel
signature, thus guaranteeing memory safety, functional correctness, and thread-safety.

4.2   Specifying the Allocator Architecture
We now present how to leverage dependently typed separation logic to specify the architecture of
StarMalloc. Our specification is modular, and relies on several tiers of composable abstractions. We
give an overview from the ground up, starting with our handling of regular allocations.
Tying Slots and Metadata. As described in Section 3.1, a slab is a memory page seen as an array
of slots of the same bytesize 𝑠. During allocation, ownership of one of these slots is given to a client
when 𝑠 or less bytes of memory are requested. The role of the allocator is to keep track of which
slots were previously allocated, and which ones the allocator still owns, and is therefore able to
transfer to a client. To do so, the allocator relies on slot metadata.
   Abstractly, the metadata slots_md maps each slot index to a boolean b, indicating whether the slot
is available for allocation (i.e., owned by the allocator). Therefore, given a slot and corresponding
boolean b, available_slot b slot either states that the allocator owns the slot (b = true, using the slarray
predicate we saw earlier), or states no ownership at all.
let available_slot b slot : slprop = if b then slarray slot else emp
   Before stating ownership at the level of an entire slab, we take a detour and introduce a helper
combinator, called starseq, below, which given a sequence s of length n, and a predicate p, returns
p s[0] 0 ∗ ... ∗ p s[n] n. Unbound names (e.g., the type a below) are implicitly bound at the top.
type idx (s:seq a) = i:nat{i < length s}
let starseq' (p: a → nat → slprop) (s:seq a) (i:idx s) = if i = length s then emp else p s.[i] i ∗ starseq' p s (i + 1)
let starseq p s : slprop = starseq' p s 0
   This combinator can be useful in a variety of contexts, not just for tying slots to their metadata: its
definition is fully generic and works for sequences of any type a with any separation logic predicate
p. To conveniently reason about this predicate, we also provide generic lemmas to, e.g., extract
the slprop corresponding to a given index, or to easily update the sequence s and modify starseq
10                                                                                             Reitz et al.


accordingly without needing to unfold its definition. This programming style is representative of
our methodology; when possible, we define proof idioms and helpers generically, and instantiate
them when needed throughout the codebase. This reduces both code duplication and the proof
effort; we only need to perform proofs on the generic version, instantiations come at no extra cost.
   Our metadata is conceptually a map from slots to booleans; in our specifications, however, we use
a smarter formulation that avoids tedious reasoning on the domain of the map. Since we statically
know the number of slots in a slab, and that each slot has associated metadata, we can represent
metadata as a sequence of booleans of length equal to the number of slots. With that, we can
define the ownership for an entire slab as the conjunction of available_slot for all slots in the slab by
iterating over all elements in the metadata sequence slots_md𝑣 , using the starseq predicate.
type mempage = a:array uint8{length a == page_size}
let slots_sl size slots_md𝑣 (slab:mempage) : slprop =
   starseq (𝜆 b i → available_slot b slab[i∗size..(i+1)∗size−1]) slots_md𝑣
   While we have been operating on a representation of metadata as a mathematical sequence,
metadata will in practice be a memory object (in our case, a bitmap), that the allocator must be able
to safely access and update. Hence, we also need to specify that the allocator has ownership of a
memory region corresponding to well-formed metadata, and tie its contents to the slots_sl predicate
above. We do it as follows, reflecting the current contents of the metadata as a sequence of booleans
via the Bitmap.as_seq helper:
let slab_sl size (slots_md:bitmap) (slab:mempage) : slprop =
   sldep (bitmap_sl slots_md) (𝜆 slots_md𝑣 → slots_sl size (Bitmap.as_seq slots_md𝑣 ) slab)
   The sldep predicate is a generic Steel predicate that captures the combination of two slprops p
and q, where the second depends on the contents of the first. In the example above, assuming
that the bitmap slots_md contains the value slots_md𝑣 , the predicate slab_sl thus corresponds to
bitmap_sl slots_md ∗ slots_sl size (Bitmap.as_seq slots_md𝑣 ) slab.
   Separating into different composable abstractions is a key component of our verification method-
ology. First, it enables modular verification, where each component can be verified in isolation
in a smaller proof context, as we will see in Section 5. Second it simplifies code maintenance and
updates to the codebase. For instance, while we represent metadata as a bitmap, switching to a
different datastructure, e.g., a free list would be straightforward, and only require changes to slab_sl,
and not to the layers below.
Slabs. As described in Section 3.1, slab metadata keeps track of empty, partially filled, and full slabs
to efficiently find a slab in which to perform allocation while minimizing memory fragmentation.
Since clients can perform calls to malloc and free in (almost) any order, slabs of different kinds can
be intertwined. To efficiently access the next empty or partial slab during allocation, the metadata
relies on list-like structures.
   While lists have a well-known, textbook separation logic specification, one difficulty arises when
attempting to use them to implement a memory allocator. List-like structures typically rely on
dynamic memory allocation when, e.g., creating and inserting a new cell, which is exactly what our
allocator must implement! To circumvent this circularity, we leverage the fact that the maximum
number of slabs is statically known (based on the amount of memory available for the entire
allocator), and instead implement a library for linked lists where all cells are part of one single
static array. To do so, we first specify what is considered a well-formed list inside the sequence
slabs_md𝑣 as is_list, below. The predicate is mostly concerned with well-formedness of the sequence
of indices, i.e., they are all in bounds, and represent a non-cyclic list. In particular, this predicate
does not capture ownership, and has therefore type prop, and not slprop.
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                          11


type cell (a:Type) = {data : a; next: size_t}
let rec is_list' (slabs_md𝑣 :seq (cell a)) (idx:size_t) (count:nat) : prop =
   if count > length slabs_md𝑣 then ⊥// Cyclic list
   else if idx = null_idx then ⊤// Terminal case
   else if idx < 0 || idx ≥ length slabs_md𝑣 then ⊥// Out−of−bound
   else is_list' slabs_md𝑣 (slabs_md𝑣 [idx].next) (count+1)
let is_list slabs_md𝑣 idx = is_list' slabs_md𝑣 idx 0
   Equipped with this, we can now define the separation logic predicate capturing ownership of
three well-formed linked lists with head pointers idx𝑒 , idx𝑝 , and idx 𝑓 (for empty, partial, and full
slabs respectively) inside the array ptr. To do so, we use slrefine, another generic Steel separation
logic combinator. slrefine slp p captures the ownership of the separation logic predicate slp, and
that p holds on the memory contents of slp. In addition to the well-formedness of the lists, we also
require that they partition all of the slabs metadata: all slabs are indeed managed by the allocator.
let arraylist_sl (ptr:array (cell a)) (idx𝑒 idx𝑝 idx 𝑓 : size_t) : slprop = slrefine (slarray ptr) (𝜆 slabs_md𝑣 →
   is_list slabs_md𝑣 idx𝑒 ∧ is_list slabs_md𝑣 idx𝑝 ∧ is_list slabs_md𝑣 idx 𝑓 ∧ partition slabs_md𝑣 idx𝑒 idx𝑝 idx 𝑓 )
   Since the lists dynamically evolve, the head pointers can change, e.g., when inserting at the
head of the list. We thus must store their current values in valid memory locations, on which the
allocator must have ownership. This can be captured by reusing the sldep predicate seen previously.
let ind_arraylist_sl (r: array (cell a)) (r𝑒 r𝑝 r 𝑓 : ref size_t) =
   sldep (ptr r𝑒 ∗ ptr r𝑝 ∗ ptr r 𝑓 ) (𝜆 (idx𝑒 , idx𝑝 , idx 𝑓 ) → arraylist_sl r idx𝑒 idx𝑝 idx 𝑓 )
   Just like before, we briefly comment our design choices. Here, because of the fixed size of our
allocations, our “arraylist” is a much simpler separation logic predicate than an actual linked list,
which would require us to follow series of pointers through the heap, and would also require us
to prove their termination. We avoid this specification burden and we simply talk about indices
within statically-known bounds, in our opinion a much more judicious choice.
   The last step is now to instantiate this generic linked list with the concrete metadata for slabs, and
to tie it to the underlying memory and slots metadata. In our case, slab metadata will correspond to
a status, represented as an enumeration of the possible slab states. In memory, the slab metadata
will therefore be an array of cell status, which permits efficient accesses and updates of metadata; if
the list structure does not need to be modified, these operations are performed in constant time.
type status = | Empty | Partial | Full
let empty_slab md𝑣 = ∀(i:nat{i < length md𝑣 }). md𝑣 .[i] == true
let dispatch stat (slab_md:bitmap) (slab:mempage) = slrefine (slab_sl slab_md slab) (𝜆 (md𝑣 , _) →
   match stat with | Empty → empty_slab md𝑣 | Partial → partial_slab md𝑣 | Full → full_slab md𝑣 )

let slabs_sl r𝑒 r𝑝 r 𝑓 (slabs_md:array (cell status)) (slots_md:array bitmap) (mem:array uint8) = sldep
   (ind_arraylist_sl slabs_md r𝑒 r𝑝 r 𝑓 ) (𝜆 (idx𝑒 , idx𝑝 , idx 𝑓 , slabs_md𝑣 ) →
      starseq (𝜆 stat i → dispatch stat (ith_slot slots_md i) (ith_page mem i)) slabs_md𝑣 )
   This specification combines several of the generic predicates seen previously. First, for a given
slab, dispatch refines slab_sl with additional constraints linking the slab status to its contents. For an
Empty slab, all slots in the slab must be free, as captured by empty_slab. Predicates for partial and full
slabs (omitted) are similar. To generalize this property to all slabs, we combine dispatch with starseq;
ith_slot and ith_page (omitted) select the subarrays corresponding to the i-th slot metadata and i-th
memory page respectively. Finally, we tie the memory and slot metadata to the slab metadata using
the sldep combinator; this captures that they are in separated, independent regions of memory.
12                                                                                                  Reitz et al.


   The use of our generic combinators to structure specifications here has several advantages; first,
they allow us to better separate different concepts, both in the specification and in the later proof
that the implementation abides by it. For instance, we can reason separately about the shape of the
slab metadata (i.e., linked lists in a static array), and its contents, which determine the structure
and availability of the underlying slots. This enables easier to read specifications, where irrelevant
parts in a given context can remain abstract. Additionally, this permits writing modular, verified
code by following the specification which simplifies code maintenance. As an example, during the
development of StarMalloc, we replaced the linked lists presented in this section by doubly-linked
lists to improve performance. This change only required replacing the definitions of arraylist_sl and
providing functions to perform list operations with the same interface as arraylist. The code and
proofs operating on the contents of the lists (i.e., the slabs metadata) was left unchanged.
Size Classes. Now that we captured the memory layout of and interaction between data, slab
metadata, and slots metadata, all that remains is to gather slabs into size classes for allocation units
of different sizes. To do so, we first collect all relevant values for a given size class into a struct,
of type sc_data. The size of memory handled by a size class, called sc_size, is fixed statically and is
defined as the size of a memory page (given by the OS) multiplied with a user-provided number of
pages per size class. The size field represents the size of an allocation unit for this size class; we
restrict the values it can take to respect alignment constraints.
type sc_data = {
  size: size_t{size % 16 == 0 ∧ size > 0};
  empty_ptr: ref size_t;
  partial_ptr: ref size_t;
  full_ptr: ref size_t;
  mem: array uint8{length mem == sc_size};
  slabs_md: array (cell status){length slabs_md == nbr_pages};
  slots_md: array bitmap{length slots_md == nbr_pages}; }

   Building upon the previous predicates, defining the predicate size_class_sl corresponding to one
size class is now straightforward. With these definitions in hand, we can now provide the following
Steel signature for allocation inside one size class.
let size_class_sl (sc: sc_data) = slabs_sl sc.empty_ptr sc.partial_ptr sc.full_ptr sc.slabs_md sc.slots_md sc.mem
val sc_malloc (sc: sc_data) : Steel (array U8.t) (size_class_sl sc) (𝜆 r → size_class_sl sc ∗ null_or_slarray r)
   (requires 𝜆h0 → ⊤) (ensures 𝜆h0 r h1 → not (is_null r) =⇒ length r == sc.size)

Alignment. In C, memory accesses where the address is not a multiple of the size of the object
being accessed are undefined behavior. To make things tractable, the C standard thus dictates that
the values returned by malloc be suitably aligned for “any object with a fundamental alignment
requirement”. In practice, this means that malloc satisfies the alignment requirements of the largest
scalar type, typically long double, which is either 8 or 16 depending on the ABI. Naturally, larger
alignments are oftentimes needed, for instance when using vector types (SSE, SSE2). To that end,
C11 and later define aligned_alloc, which supersedes previous extensions such as memalign and
posix_memalign. All the standard specifies is that aligned_alloc may fail if the alignment is invalid or
greater than that supported by the platform.
   We implement both regular (malloc) and aligned (aligned_alloc) APIs, along with wrappers that
provide ABI compatibility with non-standard APIs that predate C11. As to our implementation
choices, we follow typical behavior and support any power of two between 16 and the page size.
We could easily support larger alignments, but have not yet found a reason to do so. For simplicity
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                    13


and performance, our malloc returns values that are always aligned on a 16-byte boundary, which
is stricter than what some older ABIs (e.g., Linux x86) permit. To achieve this, we carry around a
predicate aligned that appears at slab-allocation time, namely, aligned page_size. This captures our
assumption that calls to mmap always return page-aligned memory. The predicate then makes its
way throughout our code, and is eventually provided to the client as a post-condition of malloc
(aligned 16) or aligned_malloc (aligned n). To facilitate reasoning within StarMalloc, we mostly keep
the predicate abstract. Non-linear arithmetic is circumscribed to one well-controlled lemma that
goes from aligned page_size to smaller alignment constraints, thus limiting issues with SMT solvers.
Concurrency. The function sc_malloc above is close to our target signature for malloc outlined in
4.1, with one key difference: it requires (and returns after execution) exclusive ownership of the
size class through size_class_sl. When operating in a concurrent setting, guaranteeing ownership
can be tricky; we must ensure that no thread executing concurrently also accesses the size class.
   To do so, we rely on locks, which have a natural model in CSL. A CSL lock is a value associated to
a given predicate, with (blocking) acquire and release functions, shown below. We refer the interested
reader to [Fromherz et al. 2021; Jung et al. 2018] for a more detailed presentation of CSL locks.
val lock (p:slprop) : Type
val acquire (l: lock p) : Steel unit emp (𝜆 _ → p)
val release (l: lock p) : Steel unit p (𝜆 _ → emp)
   We leverage this to provide fine-grained concurrency, where, instead of relying on one global
lock, we associate one lock to each size class, packed together in one dependently typed struct.
type size_class = {
    data : sc_data; // The content of the sizeclass
    lock : lock (size_class_sl data); // Mutex locking ownership of the sizeclass }
   We store the different size classes inside a global array, shown below. However, as the array
resides in memory, we now need to retrieve its ownership before accessing it. Hiding this ownership
behind a global lock would not be acceptable, as it would make our fine-grained concurrency design
useless. Instead, we observe that, after initialization, all accesses to the size classes are read-only;
the specificities of size classes are fixed at compile-time. To avoid relying on locks, we instead
implement a novel model of frozen arrays in Steel, that can be safely accessed concurrently by any
thread once initialized, but do not provide any update facility.
val scs : frozen_array size_class{length scs == nb_sc}
   We finally show the entrypoint of our allocator for regular allocations, the small_malloc function,
with the signature outlined in Section 4.1. For presentation purposes, we assume that our allocator
only contains two size classes, we will show in Section 5 how to make their exact number con-
figurable in our implementation. In practice, to further reduce contention, we also separate size
classes into different arenas; the global size_classes frozen array becomes of size nb_sc ∗ nb_arenas; if
small_malloc is called by a thread with arena id i, it only tries to allocate in the size classes between
indices i ∗ nb_arenas and (i + 1) ∗ nb_arenas excluded.
inline_for_extraction with_lock lock f = acquire lock; let res = f () in release lock; res
let small_malloc bytes =
   let sc = scs[0] in if bytes ≤ sc.data.size then with_lock sc.lock (𝜆 () → sc_malloc sc.data)
   else let sc = scs[1] in if bytes ≤ sc.data.size then with_lock sc.lock (𝜆 () → sc_malloc sc.data)
   else return null
  One important thing to note is that, while CSL and CSL locks ensure thread-safety, this model does
not allow to formally prove the absence of deadlocks. To alleviate this issue, we syntactically ensure
14                                                                                                        Reitz et al.


that all uses of locks are done in a scoped way. To do so, we define a combinator, called with_lock,
which takes as arguments a lock and a thunked Steel function. This combinator is annotated with
the F★ inline_for_extraction attribute, which indicates to unfold its definition at compile-time; in the
generated C code all calls to with_lock are replaced by the body of the combinator.
Large Allocations. Compared to regular allocations, the specification and implementation of large
allocations is much simpler. Large allocations are performed through direct calls to mmap; the
allocator keeps track of the pointers that have been allocated using a map from pointers to their
length to free the correct amount of data through munmap.
   We adopt a similar generic methodology for large allocations; the specification and implemen-
tation rely on an abstract model of a map and of its basic primitives (e.g., insertion). We then
instantiate this abstract model with a new implementation of AVL trees in Steel; using any other
data structure would be straightforward. Similarly to size classes, we rely on a lock to ensure the
thread-safety of large allocations. A first version of our implementation called mmap at each AVL
node allocation, which was highly inefficient; to improve the performance of large allocations,
we instead reused the slab allocator previously presented. Thanks to our tight abstractions and
abstract model, performing this change was straightforward.

4.3   Specification of Security Mechanisms
While the presentation so far has focused on functional properties of the allocator, we now present
how to extend our formalization to support a range of security mechanisms. Leveraging the modular
abstractions previously presented, we show how changes to the existing code are concise, and
do not require large-scale modification across the code base. Our chief result is that the allocator
remains correct and memory-safe in the presence of all these security mechanisms; proving that the
implementation of these mechanisms effectively defend against attacks would require an attacker
model that is, to the best of our knowledge, beyond what current state-of-the-art in program
verification can do. That being said, we certainly hope to tackle this in future work.
Zeroing on Allocations. To specify that allocations must be zero-filled, we extend the specification
of malloc presented in Section 4.1 as follows, adding an extra postcondition in the ensures clause.
val malloc (size: size_t) : Steel (array uint8) emp (𝜆 r → null_or_slarray r) (requires 𝜆_ → ⊤)
  (ensures 𝜆_ r h1 → not (is_null r) =⇒ (length r ≥ size ∧ (∀ (i:nat{i < size}). get (h1.[r]) i == 0)))
  The postcondition ensures that the contents of the returned pointer r in the final state h1 only
consists of zeros. As mentioned in Section 3.1, our free operation takes care of zeroing, and our
malloc operation (and others) takes care of checking that memory is still zero. If the memory is
corrupted, the allocator returns NULL, thus satisfying the postcondition.
Quarantine. Quarantined slabs are a special kind of slabs, disjoint from the full, partial or empty
slabs previously presented. To keep track of which slabs are quarantined, we extend the slab
metadata to support a fourth doubly linked list, associated to a fourth status.
type status = Empty | Partial | Full | Quarantine
let dispatch stat slab_md slab = slrefine (slab_sl slab_md slab) (𝜆 (md𝑣 , _) →
   match stat with ... | Quarantine → quarantine_slab md𝑣 )

let arraylist_sl ptr idx𝑒 idx𝑝 idx 𝑓 idx𝑞 = slrefine (slarray r) (𝜆 md𝑣 → ... ∧ is_list md𝑣 idx𝑞 )
    To enable the reuse of quarantined slabs, we define a queue data structure on top of doubly
linked lists. This permits to easily access the first quarantined slab, and unquarantine it by moving
it to the list of empty slabs after a sufficiently long time; we omit this for presentation purposes.
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                            15


  Thanks to our modular approach coupled with strong abstractions, required changes to the
codebase are highly localized, and most of our code is left unchanged. In addition to the changes
shown above, we need to add a fourth head pointer to the sc_data structure, and modify the code
and proof relating to the slabs_sl predicates, but all layers above (e.g., operating on top of sc_malloc)
or below (e.g., code operating at the slots level, on the slab_sl predicate) are entirely unchanged.
Guard Pages. Our specification extension to support guard pages is similar to the one previously
presented for quarantine: we add a fifth linked list to the slabs metadata, and perform localized
changes in the codebase accordingly. One key difference however is that the separation logic
predicate we devise, slab_guard, is an abstract predicate for which we only provide an introduction
rule, as shown below. This induces a form of monotonicity: once a slab is marked as slab_guard, by
virtue of abstraction, it can never be eliminated to retrieve a separation logic predicate on which the
allocator could operate, or that it could transform to an slarray to pass to the client. Under the hood,
the introduction rule is implemented as a call to mmap with the PROT_NONE flag; this ensures that
any access to a guard page will result in a SIGSEGV returned by the OS.
let dispatch stat slab_md slab = match stat with ... | Guard → slab_guard slab
val slab_guard slab : slprop
val slab_guard_intro slab : Steel unit (slarray slab) (𝜆 _ → slab_guard slab)

   Additionally, guard pages must appear following a specified pattern; typically, every guard_int
pages, where guard_int is a statically fixed, user-defined constant. To specify this, we extend the
slabs_sl predicate, and in particular its starseq component iterating over all slabs as follows. guard_int
and guard_start are two global Steel constants that can be easily changed without modifying other
parts of the code, thus making experimenting with different guard pages patterns trivial.
let slabs_sl ... = ... starseq (𝜆 stat i → dispatch ... ∧ (i % guard_int = guard_start) =⇒ stat = Guard) ...


5   IMPLEMENTING, VERIFYING, EXTRACTING TO C
We mentioned earlier that Steel admits a subset that compiles to C. We now implement our allocator
in that subset; show that it refines the specification from Section 4; and demonstrate how to extract it
to C while keeping the implementation generic. We thus obtain a provably correct implementation
of the security-oriented StarMalloc, which currently consists of 26,000 lines of F★ code, extracting
to about 4,300 lines of executable C code. Our code is open-source on GitHub and, to the best of
our knowledge, is the second-largest Steel project to date.
Specification-Guided Implementation. To enable efficient verification, we adopt a specification-
guided (also called proof-oriented) approach when implementing StarMalloc. Concretely, our imple-
mentation closely follows the abstractions and structure of the specification presented in Section 4.
This yields several benefits. First, particularly complex pieces of code (e.g., optimized implemen-
tation of bitmaps) are naturally circumscribed within the boundaries of the specification-driven
abstractions. Second, verification conditions to prove that the code satisfies its functional specifica-
tion are simpler, as we leverage the successive layers of abstractions to hide as many implementation
details as possible; this greatly reduces the proof effort needed to establish the safety and functional
correctness of our allocator. Third, by leveraging the modularity of the specification and F★’s
abstraction facilities, our code admits a natural separation into different modules (e.g., to operate
at the slots level or at the slabs level) where the implementation details can be hidden behind
strong abstractions (interfaces in F★ jargon). As mentioned in Section 4.2, this allows to easily
perform code optimizations (e.g., by replacing linked lists by doubly linked lists) without impacting
the rest of the code and proofs, as long as the interfaces are left unchanged. This also permits
16                                                                                                Reitz et al.


highly parallel builds, which greatly reduce the verification time and the development cycles: if
module A depends on module B, F★ only needs to verify the interface of module B, not its complete
implementation before verifying module A. Case in point, the entire verification of StarMalloc only
requires 30-40 minutes on a modern laptop; in practice, we rarely perform builds from scratch
during a development cycle, making iterating much faster.
Static Parametrization, Partial Evaluation. General-purpose allocators such as StarMalloc can
be used in many contexts; thus, they must be easily configurable. Clients operating in a purely
sequential setting might want do disable arenas to avoid memory waste, while clients that only
perform very small allocations might want to disable the larger size classes. When modifying the
allocator configuration, some changes simply require modifying global variables (e.g., to adapt the
size of a global array), but others are more involved, requiring deeper changes to the allocator’s
implementation (e.g., to initialize different numbers of size classes with different shapes).
   When implementing an unverified allocator in C, a common technique is to rely on preprocessor
macros to generate suitable code. This is however error-prone, and not ideal for security-critical
code. Performing deep modifications into the code is also not acceptable; even in a verified setting
where these changes could be safely performed, the effort involved would deter most clients.
   We leverage F★’s normalizer, a key component of dependently typed languages which allows
reducing pure terms at F★-compile time, that is, before extraction to C takes places – one can
think of it as a principled preprocessor that is even more powerful that C++ templates. We use the
normalizer to verifiably specialize our code according to a user-provided configuration. Following
the methodology outlined in the previous sections, we implement and verify our allocator in a
generic style, abstracting over the configuration details. For instance, size class initialization is
performed through the recursive function init_size_classes below, which takes as arguments arrays
for the size classes and metadata, as well as a list of sizes l representing the size classes configuration.
let rec init_size_classes size_classes md l = match l with
   | [] → ()
   | slot_size :: tl → init_size_class slot_size size_classes[0] md[0];
                      init_size_classes tl size_classes[1..] md[1..]
let init size_list =
   let size_classes = mmap .. in let md = mmap .. in
   init_size_classes size_classes md size_list

   While this code is valid in Steel and successfully verifies, it is however not compatible with
KaRaMeL extraction: mathematical lists cannot natively extract to C. For presentation purposes, we
will assume that a client wishes to have two size classes, of slot size 16B and 32B respectively; they
will specify this by modifying the global variable sc_list. We rely on the F★ primitive norm to instruct
the compiler to reduce the application init sc_list, according to the reduction steps custom_steps
(omitted), which include for instance unfolding the definition sc_list and reducing pattern matchings
operating on lists, but not unfolding the definition init_size_class. After normalization, all occurrences
of lists disappeared, which enables KaRaMeL to extract to the idiomatic C init shown below.
let sc_list = [16; 32]
let init = norm custom_steps (init sc_list)

void init() { // Generated C code after normalization
  size_classes = mmap .. ;
  md = mmap ..;
  init_size_classes size_classes[0] md[0] 16;
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                  17


    init_size_classes size_classes[1] md[1] 32; }


   This approach makes it straightforward to configure StarMalloc according to a client’s needs. We
only need to modify the value sc_list and to recompile our project; apart from this variable, all the
code and proofs are left unchanged. We apply this methodology to all parts of StarMalloc where the
static configuration impacts the shape of the code; this includes for instance selecting an appropriate
size class in which to allocate, and handling arenas. We emphasize that this specialization at
extraction-time is entirely verified, and hence, untrusted; F★’s normalizer is a key component of its
typechecker, and hence already part of the TCB.
Generic, Reusable Libraries. As part of the development of StarMalloc, we defined and imple-
mented a range of generic libraries which we instantiated to fit our needs. We already presented
several of them in Section 4; they include datastructures (statically allocated doubly linked lists,
efficient bitmaps, AVL trees, frozen arrays, FIFO queues), proof idioms and generic separation logic
combinators (starseq, extensions and helpers for slrefine and sldep), concurrency primitives (separa-
tion logic locks with native extraction to pthread mutexes), and modeling of the interaction with
the OS (axiomatization of memory-related syscalls, e.g., mmap). These libraries required significant
engineering and modeling effort, and represent a large part of our development, totalling close to
13,000 lines of F★ code. While crucial to the development of StarMalloc, they are a contribution of
their own, which significantly decreases the effort required for future systems verification projects
in F★. We organized our codebase to ensure they are entirely separate from the core of StarMalloc,
and hope to upstream them to the Steel standard library in the future to benefit to the community.
   Native, idiomatic extraction of locks was contributed to KaRaMeL for this work, and will support
further F★ concurrent verification developments. This required reconciling the Steel model of
locks (where locks are values) with a low-level extraction that relies on pthread and its semantics
(where the address of a lock matters). We achieved this by adding dedicated passes in the KaRaMeL
compiler, allowing us to support global variables that contain locks (the static array of size classes).
This represents a significant improvement over the pre-existing implementation of locks that relied
on a simple compare-and-swap primitive.
Other Supported Features. While our presentation focused on malloc for brevity reasons, appli-
cations typically rely on all memory management primitives specified by the C standard [ISO 1999,
§7.20.3]. To be usable in production by real-world applications, StarMalloc thus also specifies and
implements the other primitives specified by the C99 standard, i.e., free, realloc, and calloc. It also
includes recent extensions, such as aligned_alloc introduced in the C11 standard [ISO 2011, §7.22.3].

6    EVALUATION
We now compare StarMalloc with other state-of-the-art memory allocators, including security-
oriented allocators, such as hardened_malloc [GrapheneOS Development Team 2021], DieHarder [No-
vark and Berger 2010], and regular allocators, such as the glibc and the next-gen musl allocators.
   Doing so, we aim to i) evaluate the performance of StarMalloc against other allocators; ii)
determine whether StarMalloc can be used as a drop-in replacement in existing, widely used
applications and iii) assess the time and effort spent developing StarMalloc, and whether the
methodology can be expanded to support further optimizations (security or performance) with
reasonable time and effort.
   Our evaluation relies on two sets of benchmarks. To provide a fine-grained performance com-
parison with other allocators, we reuse mimalloc-bench [Leijen et al. 2018], a comprehensive and
popular suite which contains a selection of benchmarks from the academic literature and several
18                                                                                          Reitz et al.


real-world applications. To evaluate the real-world readiness of our allocator, we finally describe
our integration of StarMalloc within Firefox, which required an extensive set of allocator features.


6.1   Performance Evaluation
We start by evaluating the performance of StarMalloc, comparing the execution time and memory
usage. Throughout this work, we improved mimalloc-bench by allowing the use of the testsuite
with recent compiler toolchains and fixed several compilation issues and bugs in benchmarking
scripts; we contributed several patches that were merged into the mimalloc-bench repository.
Experimental setup. We run experiments on a 4-core, 8-thread machine with an Intel(R) Xeon(R)
CPU E5-1620 0 @ 3.60GHz processor and 12GB memory, using Linux 6.1 and glibc 2.38. To ensure
reproducible results, we use the “performance” scaling governor (meaning all cores pegged at
maximum speed without dynamic CPU scaling), and increase vm.max_map_count from 65,530 to
1,048,576 to ensure allocators using a large number of memory mappings, such as hardened_malloc
and StarMalloc for guard pages, work properly.
Total Execution Time. As we mentioned before, a meaningful way to measure an allocator’s
performance is to measure the client program’s total execution time. We evaluate several state-of-
the-art allocators on a variety of realistic workloads from mainstream programs; complete results
are available in the Appendix. We focus on the most salient comparisons in Table 1, where we
consider StarMalloc, along with the allocators mentioned earlier. The time difference between
StarMalloc and hardened_malloc measures the cost of verification, or more precisely, the penalty
for the last few performance optimizations we have yet to implement. The time difference between
hardened_malloc and glibc measures the cost of security: while performant and widely-used, glibc’s
allocator design is known to be a possible liability from a security perspective.
   Recall that our allocator is generic and that numerous parameters can be tweaked. Aiming for
an apples-to-apples comparison, we use the same configuration as hardened_malloc, namely, the
guard page interval set to 2 and the number of arenas set to 4, with quarantine and zeroing enabled.
   The most meaningful comparison is thus between StarMalloc and hardened_malloc. The first
series of benchmarks are real-world applications. For most applications, the performance overhead
is within 0.84x to 1.38x; one notable outlier is redis, a key-value database. After careful inspection
of the code, differences in redis seem to be due to a large number of allocations of size slightly
exceeding the page size. While these allocations fall into StarMalloc’s large allocations, requiring
repeated calls to mmap, hardened_malloc’s slab allocator can be used for allocations of up to 131072
bytes (i.e. 32 standard 4k pages) by combining several pages together. We did not yet implement this
optimization in StarMalloc, but do not foresee any difficulty doing so. We remark that compared to
another defensive allocator like DieHard, we exhibit much better variance and overall performance.
   The second series of benchmarks stress-test the allocator via specific allocation patterns which
are not representative of real-world applications. We remark that for most of these, StarMalloc
performs within 30% of hardened_malloc. One notable exception is rptestN, which particularly
tests large allocations, and exhibits the same limitations as redis.
   Since we inherit most of the design choices from hardened_malloc, our performance is further
apart from a non-security-oriented allocator like glibc. This is the cost of defensive security
measures; ultimately, application developers will have to decide how much importance they attach to
the security of their applications. Nevertheless, StarMalloc outperforms mng for some benchmarks.
   Broadening our scope to look at other allocators (Table 3), we observe a greater variety of
performance profile across allocators, with greater variation on micro-benchmarks than on realistic
workloads. These results suggest that no single choice of optimizations is the “right” one for every
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                          19


                                          Time                                       RSS
       Benchmark               dh hm mng                st glibc           dh hm mng            st glibc
       barnes               1.036 1.0        1.0       1.0      1.0     0.774 1.0 0.745 0.832 0.699
       cfrac                1.446 1.0 0.738         1.278 0.544         0.261 1.0       0.1   0.81 0.113
       espresso             1.273 1.0 1.301         2.284 0.707          0.18 1.0 0.066 1.399 0.062
       gs                   2.278 1.0 0.678         1.304 0.339         0.797 1.0 0.524       1.39 0.513
       larsonN            17.097 1.0 2.251          1.036     0.09      0.659 1.0 0.369 2.277 0.664
       larsonN-sized      16.823 1.0         2.2    1.008 0.088          0.69 1.0 0.351 2.292        0.78
       leanN                6.249 1.0 1.421         1.086 0.617         1.421 1.0 0.688 1.417        0.78
       lua              timeout 1.0        1.05     1.554 0.729 timeout 1.0 0.639 1.338 0.654
       mathlib               ERR 1.0 0.779          1.221 0.645          ERR 1.0 0.626 2.004 0.676
       redis                2.809 1.0      0.82 16.379 0.592            0.493 1.0 0.216 1.339 0.205
       rocksdb               ERR 1.0 ERR            0.843 0.813          ERR 1.0 ERR 1.471 0.785
       z3                   5.063 1.0 0.813         1.375 0.688         0.622 1.0 0.417 1.294 0.401
       alloc-test1          2.051 1.0 0.922         1.291 0.515         0.447 1.0 0.292 1.471 0.305
       alloc-testN        12.566 1.0 3.693          1.574 0.136         0.302 1.0 0.247 2.678 0.201
       cache-scratch1       1.006 1.0 0.994         0.994 0.994         0.205 1.0 0.133 0.445 0.133
       cache-scratchN       0.977 1.0 0.977            1.0 0.977         0.22 1.0 0.144 0.555 0.159
       cache-thrash1        1.006 1.0 0.994            1.0 0.994        0.219 1.0 0.143 0.401 0.143
       cache-thrashN           1.0 1.0       1.0       1.0      1.0     0.204 1.0 0.135 0.517 0.133
       glibc-simple            1.5 1.0 1.187        1.931 0.453         0.248 1.0 0.055 0.744 0.058
       glibc-thread       10.033 1.0 3.161          1.679 0.074         0.133 1.0 0.032 2.813 0.056
       malloc-large         3.604 1.0 1.034         1.046 0.539         0.928 1.0 0.918 0.928 1.196
       mleak10              1.692 1.0 0.923            1.0 1.231        0.284 1.0     0.07 0.682 0.146
       mleak100             1.754 1.0        1.0    1.041 1.369         0.258 1.0 0.062 0.618 0.128
       mstressN             5.251 1.0 1.722         1.605 0.435         0.811 1.0 0.681       1.12 1.521
       rbstress1             1.14 1.0 0.809         0.895 0.812         1.177 1.0 0.905 0.925 0.708
       rbstressN            1.285 1.0 0.782         0.939     0.76      0.705 1.0 0.684 0.941          1.0
       rptestN              7.521 1.0 1.414 19.537 0.387                0.534 1.0 0.234       2.59 0.254
       sh6benchN          22.109 1.0 3.239          1.649 0.175         1.771 1.0 0.868       1.12 1.056
       sh8benchN          13.098 1.0 2.229          1.256 0.133         1.075 1.0 0.803       1.21 0.982
       xmalloc-testN        8.978 1.0 1.543          1.17 0.205         0.836 1.0 0.066 0.393 0.815
Table 1. Execution time and peak RSS for StarMalloc (“st”, this work), hardened_malloc (“hm”, [GrapheneOS
Development Team 2021]), DieHarder [Novark and Berger 2010] (“dh”), nextgen implementation for musl
libc (“mng”, [Felker 2020]), and the glibc allocator (“glibc”). Results are normalized and presented relative to
hardened_malloc. ERR corresponds to crashes during execution.
workload. Additional benchmarks (not listed here) on different processors show that microarchi-
tecture revisions can also significantly influence the final results. We believe that by addressing
the long tail of micro-optimizations (such as carefully annotating each branch with likely/unlikely
attributes, optimizing size class selection, or supporting larger slab allocations), we can meet the
performance of hardened_malloc. In short, on most benchmarks, our verified code is almost as
efficient as the unverified one, and for a few corner cases, the performance can be regained with
many time-consuming small fixes which we intend to enact.
Memory usage. We measure the Resident Set Size (RSS), with swap disabled to get an accurate
reading of the memory footprint of a running program. RSS only counts pages that are actually
used, as opposed to the virtual memory usage; this is what we want. We observe a wide variety of
behaviors; in several cases, StarMalloc outperforms hardened_malloc, while in others, its memory
footprint is larger than hardened_malloc. While our allocator design is inspired by hardened_malloc,
we posit that this variance is due to minor implementation differences, especially in the quarantine.
We remark that glibc’s allocator, too, exhibits suboptimal behavior compared to hardened_malloc
20                                                                                              Reitz et al.


on several test cases, despite the absence of a quarantine mechanism, which greatly increase the
memory usage; this again suggests that no design is ideal for all applications.

6.2   Security Evaluation
We adopt the state-of-the-art security-oriented allocator design from hardened_malloc, and as
such, inherit its security guarantees. Out of due diligence, we confirm that our implementation,
unsurprisingly, is capable of defending against a wide variety of attacks, and as such, provides an
efficient “last line of defense” against exploitation and programmer mistakes. We tested various
use-after-frees (UAFs) found in recent fuzzing-based work [Yagemann et al. 2023], and confirmed
that they were indeed caught. We tested a “classic” CVE [National Vulnerability Database 2016] for
a UAF in bzip2, also prevented by StarMalloc. We tested a series of exploits from the how2heap
repository [The Shellphish Team 2023]. We prevent the “fastbin_reverse_into_cache”, “fastbin_dup”
and “tcache poisoning” exploits, all of which are successful with the most recent version of glibc
(2.38). We thus conclude that the security measures we implemented are, as we expected, effective.
We re-emphasize that use-after-frees and double-frees are still very much active attack vectors, and
continue to pop up in mainstream software [National Vulnerability Database 2023a,b].

6.3   Firefox Integration
To assess whether StarMalloc can be deployed as a drop-in replacement into real-world projects,
we integrated it into Mozilla Firefox, raising interesting challenges: first, the replacement allocator
must to provide non-standard extensions of malloc and free [Hommey 2012]; second Firefox, and
hence the underlying allocator, must work in a highly concurrent setting, supporting many threads
and processes in parallel. To evaluate the user-facing impact of using StarMalloc, we relied on Jet-
Stream2 [2022], a “benchmark suite focused on the most advanced web applications”. We integrated
StarMalloc with Firefox 118.0.2 and successfully ran the entire benchmark suite, demonstrating a
performance overhead of 5.1% and 12.1% compared to a version compiled with hardened_malloc
and glibc respectively; this suggests the applicability of StarMalloc to real-world usecases.

6.4   Proof Effort
We estimate that our implementation effort for StarMalloc took            Component                 LoC
two person-years. This includes building a substantial foundation         Reusable Libraries
                                                                            Bitmaps                1,520
that was missing from the Steel project, starting from arrays, and
                                                                            List                   2,754
moving up to data structures (AVL trees, bitmaps, arraylists, queues).
                                                                            Queue                    494
A lot of work was foundational, and aimed at understanding how to           AVL                    4,283
successfully model, verify and extract an extremely low-level view          Misc                   3,692
of memory within the framework. We believe that this effort will          StarMalloc              12,972
be highly reusable, and intend to upstream it as soon as possible.        C glue                     303
   We reiterate that a substantial amount of effort went into building    Total                   26,102
strong, tight abstraction boundaries between the various compo-
                                                                         Table 2. Lines of F★ code for
nents of StarMalloc. In less than a week, we implemented a first
                                                                         each component of StarMalloc,
batch of security mechanisms without affecting the rest of the code.     excluding whitespace and com-
More recently, we improved the quarantine mechanism, relying             ments. Misc includes starseq,
on the tight abstraction boundaries to preserve verification and         other helpers related to sldep
extraction. The tight abstractions have the added benefit of pre-        and slrefine, plus various library
serving a lot of intermediary verification files, meaning that one       functions not found in F★’s stan-
can efficient rebuild and re-extract StarMalloc when iterating on        dard library.
one sub-component.
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                                    21


7   FUTURE WORK AND CONCLUSION
StarMalloc is a verified, efficient, security-oriented memory allocator that implements state-of-the-
art performance and defensive design choices. Using the F★ proof assistant and the Steel separation
logic framework, we verified, implemented and extracted to C a complete allocator that can be
used as a drop-in replacement for realistic workloads. To the best of our knowledge, this is the first
concurrent allocator that is simultaneously verified, hardened, and efficient.
   Most of our future work centers on closing the gap between StarMalloc and hardened_malloc
(our chief source of inspiration), both in terms of performance and breadth of security features.
Overall, we believe that there is currently a gap in real-world verified software stacks when it
comes to allocators, and we hope that StarMalloc can represent a first step towards filling that gap.

ACKNOWLEDGMENTS
We would like to thank Daan Leiijen for clarifications about many parts of mimalloc and mimalloc-
bench, Matthew Parkinson for discussions about allocators security mechanisms, and Tim Bourke
for valuable feedback about earlier versions of this paper.

REFERENCES
 Periklis Akritidis. 2010. Cling: A Memory Allocator to Mitigate Dangling Pointers.. In Proceedings of the USENIX Security
   Symposium.
 José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, Benjamin Grégoire, Adrien Koutsos, Vincent Laporte, Tiago Oliveira,
   and Pierre-Yves Strub. 2020. The Last Mile: High-Assurance and High-Speed Cryptographic Implementations. In
   Proceedings of the IEEE Symposium on Security and Privacy (S&P).
 Andrew W. Appel. 2011. Verified Software Toolchain. In Proceedings of the European Conference on Programming Languages
   and Systems (ESOP).
 Andrew W. Appel. 2015. Verification of a Cryptographic Primitive: SHA-256. In ACM Transactions on Programming
   Languages and Systems (TOPLAS).
 Andrew W Appel and David A Naumann. 2020. Verified sequential malloc/free. In Proceedings of the International
   Symposium on Memory Management (ISMM).
 Apple Security Research. 2022. Towards the next generation of XNU memory safety: kalloc_type. https://security.apple.c
   om/blog/towards-the-next-generation-of-xnu-memory-safety/.
 Gilles Barthe, Sandrine Blazy, Benjamin Grégoire, Rémi Hutin, Vincent Laporte, David Pichardie, and Alix Trieu. 2020.
   Formal Verification of a Constant-Time Preserving C Compiler. In Proceedings of the ACM Symposium on Principles of
   Programming Languages (POPL).
 Emery D. Berger. 2012. Software Needs Seatbelts and Airbags: Finding and Fixing Bugs in Deployed Software is Difficult
   and Time-Consuming. Here Are Some Alternatives. Commun. ACM (2012).
 Emery D. Berger and Benjamin G. Zorn. 2006. DieHard: Probabilistic Memory Safety for Unsafe Languages. In Proceedings
   of the Conference on Programming Language Design and Implementation (PLDI).
 Edwin Brady. 2013. Idris, a general-purpose dependently typed programming language: Design and implementation.
   Journal of Functional Programming 23 (9 2013), 552–593. Issue 05.
 Jacob Bramley, Dejice Jacob, Andrei Lascu, Jeremy Singer, and Laurence Tratt. 2023. Picking a CHERI Allocator: Security
   and Performance Considerations. In Proceedings of the International Symposium on Memory Management (ISMM).
 Stephen Brookes. 2007. A Semantics for Concurrent Separation Logic. In Theoretical Computer Science (TCS).
 The Chromium Project. 2020. Memory Safety. https://www.chromium.org/Home/chromium-security/memory-safety/.
 Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In Proceedings of the Conference on Tools and
   Algorithms for the Construction and Analysis of Systems (TACAS).
 Damien Doligez and Georges Gonthier. 1994. Portable, unobtrusive garbage collection for multiprocessor systems. In
   Proceedings of the ACM Symposium on Principles of Programming Languages (POPL).
 Damien Doligez and Xavier Leroy. 1993. A concurrent, generational garbage collector for a multithreaded implementation
   of ML. In Proceedings of the ACM Symposium on Principles of Programming Languages (POPL).
 Gabriel Ebner, Sebastian Ullrich, Jared Roesch, Jeremy Avigad, and Leonardo de Moura. 2017. A Metaprogramming
   Framework for Formal Verification. In Proceedings of the International Conference on Functional Programming (ICFP).
 Andres Erbsen, Jade Philipoom, Jason Gross, Robert Sloan, and Adam Chlipala. 2019. Simple High-Level Code for
   Cryptographic Arithmetic - With Proofs, Without Compromises. In Proceedings of the IEEE Symposium on Security and
22                                                                                                            Reitz et al.


   Privacy (S&P).
 Jason Evans. 2006. A scalable concurrent malloc (3) implementation for FreeBSD. In BSDCan — The Technical BSD
   Conference.
 Bin Fang, Mihaela Sighireanu, Geguang Pu, Wen Su, Jean-Raymond Abrial, Mengfei Yang, and Lei Qiao. 2018. Formal
   modelling of list based dynamic memory allocators. Science China Information Sciences 61 (2018), 1–16.
 Rich Felker. 2020. Comparison between hardened_malloc and musl mallocs. https://www.openwall.com/lists/musl/2020/0
   5/13/1.
 Aymeric Fromherz, Aseem Rastogi, Nikhil Swamy, Sydney Gibson, Guido Martínez, Denis Merigoux, and Tahina Ra-
   mananandro. 2021. Steel: Proof-Oriented Programming in a Dependently Typed Concurrent Separation Logic. In
   Proceedings of the International Conference on Functional Programming (ICFP).
 GitHub Team. 2023. The top programming languages. https://octoverse.github.com/2022/top-programming-languages
 glibc. 2017a. Bug 22343 (CVE-2018-6485) - Integer overflow in posix_memalign (CVE-2018-6485). https://sourceware.org
   /bugzilla/show_bug.cgi?id=22343.
 glibc. 2017b. Bug 22375 (CVE-2017-17426) - malloc returns pointer from tcache_get when should return NULL (CVE-2017-
   17426). https://sourceware.org/bugzilla/show_bug.cgi?id=22375.
 glibc. 2020. Bug 26306 - Confusion in malloc.c about the fastbins size check. https://sourceware.org/bugzilla/show_bug.c
   gi?id=26306.
 GrapheneOS Development Team. 2021. hardened_malloc – GrapheneOS’s hardened memory allocator. https://github.com
   /GrapheneOS/hardened_malloc/blob/main/README.md#security-properties.
 Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan Newman Wu, Jieung Kim, Vilhelm Sjöberg, and David Costanzo. 2016.
   CertiKOS: An Extensible Architecture for Building Certified Concurrent OS Kernels. In Proceedings of the USENIX
   Symposium on Operating Systems Design and Implementation (OSDI).
 Son Ho, Jonathan Protzenko, Abhishek Bichhawat, and Karthikeyan Bhargavan. 2022. Noise*: A library of verified
   high-performance secure channel protocol implementations. In Proceedings of the IEEE Symposium on Security and
   Privacy (S&P).
 Mike Hommey. 2012. Hooking the memory allocator in Firefox. https://glandium.org/blog/?p=2848.
 Samin S. Ishtiaq and Peter W. O’Hearn. 2001. BI as an Assertion Language for Mutable Data Structures. In Proceedings of
   the ACM Symposium on Principles of Programming Languages (POPL).
 ISO. 1999. ISO/IEC 9899:1999 C standard. https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf.
 ISO. 2011. ISO/IEC 9899:2011 C standard. https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf.
 JetStream2. 2022. JetStream 2.1 In-Depth Analysis. https://browserbench.org/JetStream/in-depth.html.
 Ke Jiang, David Sanan, Yongwang Zhao, Shuanglong Kan, and Yang Liu. 2019. A Formally Verified Buddy Memory
   Allocation Model. In Proceedings of the International Conference on Engineering of Complex Computer Systems (ICECCS).
 Cliff B. Jones. 1983. Tentative steps toward a development method for interfering programs. In ACM Transactions on
   Programming Languages and Systems (TOPLAS).
 Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
   ground up: A modular foundation for higher-order concurrent separation logic. Journal of Functional Programming 28
   (2018).
 Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
   Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning. In Proceedings of the ACM Symposium on
   Principles of Programming Languages (POPL).
 Brian W Kernighan and Dennis M Ritchie. 1988. The C programming language. (1988).
 Gerwin Klein, June Andronick, Matthew Fernandez, Ihor Kuz, Toby Murray, and Gernot Heiser. 2018. Formally verified
   software in the real world. Commun. ACM 61, 10 (2018), 68–77.
 Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dhammika Elkaduwe, Kai
   Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. 2009. seL4: Formal
   Verification of an OS Kernel. In Proceedings of the ACM Symposium on Operating Systems Principles (SOSP).
 Robbert Krebbers, Ralf Jung, Aleš Bizjak, Jacques-Henri Jourdan, Derek Dreyer, and Lars Birkedal. 2017. The Essence of
   Higher-Order Concurrent Separation Logic. In Proceedings of the European Conference on Programming Languages and
   Systems (ESOP).
 Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens. 2014. CakeML: A Verified Implementation of ML.
   In Proceedings of the ACM Symposium on Principles of Programming Languages (POPL).
 Daan Leijen, Julien Voisin, and Matthew Parkinson. 2018. mimalloc-bench – Suite for benchmarking malloc implementation.
   https://github.com/daanx/mimalloc-bench.
 Daan Leijen, Benjamin Zorn, and Leonardo de Moura. 2019. Mimalloc: Free list sharding in action. In Proceedings of the
   Asian Conference on Programming Languages and Systems (ASPLAS).
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                                       23


 K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional Correctness. In Proceedings of the
   Conference on Logic for Programming, Artificial Intelligence, and Reasoning (LPAR).
 Xavier Leroy. 2006. Formal certification of a compiler back-end, or: programming a compiler with a proof assistant. In
   Proceedings of the ACM Symposium on Principles of Programming Languages (POPL).
 Paul Liétar, Theodore Butler, Sylvan Clebsch, Sophia Drossopoulou, Juliana Franco, Matthew J. Parkinson, Alex Shamis,
   Christoph M. Wintersteiger, and David Chisnall. 2019. Snmalloc: A Message Passing Allocator. In Proceedings of the
   2019 ACM SIGPLAN International Symposium on Memory Management (Phoenix, AZ, USA) (ISMM 2019). Association for
   Computing Machinery, New York, NY, USA, 122–135. https://doi.org/10.1145/3315573.3329980
 Beichen Liu, Pierre Olivier, and Binoy Ravindran. 2019. Slimguard: A secure and memory-efficient heap allocator. In
   Proceedings of the ACM/IFIP/USENIX International Middleware Conference.
 LLVM Project. 2023. Scudo Hardened Allocator. https://llvm.org/docs/ScudoHardenedAllocator.html.
 Frédéric Mangano, Simon Duquennoy, and Nikolai Kosmatov. 2016. Formal verification of a memory allocation module of
   Contiki with Frama-C: a case study. In Proceedings of the International Conference on Risks and Security of Internet and
   Systems (CRiSIS).
 Nicolas Marti, Reynald Affeldt, Akinori Yonezawa, and Department Of Computer Science. 2006. Formal Verification of the
   Heap Manager of an Operating System using Separation Logic. In Proceedings of the International Conference on Formal
   Engineering Methods (ICFEM).
 Guido Martínez, Danel Ahman, Victor Dumitrescu, Nick Giannarakis, Chris Hawblitzel, Catalin Hritcu, Monal
   Narasimhamurthy, Zoe Paraskevopoulou, Clément Pit-Claudel, Jonathan Protzenko, Tahina Ramananandro, Aseem
   Rastogi, and Nikhil Swamy. 2019. Meta-F*: Proof Automation with SMT, Tactics, and Metaprograms. In Proceedings of
   the European Conference on Programming Languages and Systems (ESOP).
 MSRC Team. 2021. BadAlloc – Memory allocation vulnerabilities could affect wide range of IoT and OT devices in
   industrial, medical, and enterprise networks. https://msrc-blog.microsoft.com/2021/04/29/badalloc-memory-allocation-
   vulnerabilities-could-affect-wide-range-of-iot-and-ot-devices-in-industrial-medical-and-enterprise-networks/.
 The MSRC Team. 2019. A Proactive Approach to More Secure Code. https://msrc.microsoft.com/blog/2019/07/a-proactive-
   approach-to-more-secure-code/.
 MySQL. 2019. Bug #94647 - Memory leak in MEMORY table by glibc. https://bugs.mysql.com/bug.php?id=94647.
 National Vulnerability Database. 2016. Use-after-free vulnerability in bzip2. CVE-2016-3189 https://nvd.nist.gov/vuln/deta
   il/CVE-2016-3189.
 National Vulnerability Database. 2023a. OpenSSH server (sshd) 9.1 introduced a double-free vulnerability during op-
   tions.kex_algorithms handling. CVE-2023-25136 https://nvd.nist.gov/vuln/detail/CVE-2023-25136.
 National Vulnerability Database. 2023b. A use after free vulnerability exists in curl <v8.1.0. CVE-2023-28319 https:
   //nvd.nist.gov/vuln/detail/CVE-2023-28319.
 Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. 2002. Isabelle/HOL: a proof assistant for higher-order logic.
   Vol. 2283. Springer Science & Business Media.
 Gene Novark and Emery D Berger. 2010. DieHarder: securing the heap. In Proceedings of the ACM Conference on Computer
   and Communications Security (CCS).
 Peter W. O’Hearn. 2007. Resources, Concurrency, and Local Reasoning. In Theoretical Computer Science (TCS).
 Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs That Alter Data Structures.
   In Proceedings of the International Workshop on Computer Science Logic (CSL).
 Sean Peters, Adrian Danis, Kevin Elphinstone, and Gernot Heiser. 2015. For a microkernel, a big lock is fine. In Proceedings
   of the Asia-Pacific Workshop on Systems (APSys).
 Marina Polubelova, Karthikeyan Bhargavan, Jonathan Protzenko, Benjamin Beurdouche, Aymeric Fromherz, Natalia
   Kulatova, and Santiago Zanella-Béguelin. 2020. HACLxN: Verified Generic SIMD Crypto (for All Your Favourite Platforms).
   In Proceedings of the ACM Conference on Computer and Communications Security (CCS).
 Red Hat Customer Portal. 2013. CVE-2013-4332. https://access.redhat.com/security/cve/cve-2013-4332.
 Jonathan Protzenko, Bryan Parno, Aymeric Fromherz, Chris Hawblitzel, Marina Polubelova, Karthikeyan Bhargavan,
   Benjamin Beurdouche, Joonwon Choi, Antoine Delignat-Lavaud, Cédric Fournet, Natalia Kulatova, Tahina Ramananandro,
   Aseem Rastogi, Nikhil Swamy, Christoph M. Wintersteiger, and Santiago Zanella-Béguelin. 2020. EverCrypt: A Fast,
   Verified, Cross-Platform Cryptographic Provider. In Proceedings of the IEEE Symposium on Security and Privacy (S&P).
 Jonathan Protzenko, Jean-Karim Zinzindohoué, Aseem Rastogi, Tahina Ramananandro, Peng Wang, Santiago Zanella-
   Béguelin, Antoine Delignat-Lavaud, Catalin Hritcu, Karthikeyan Bhargavan, Cédric Fournet, and Nikhil Swamy. 2017.
   Verified Low-Level Programming Embedded in F*. In Proceedings of the International Conference on Functional Programming
  (ICFP).
 Tahina Ramananandro, Antoine Delignat-Lavaud, Cédric Fournet, Nikhil Swamy, Tej Chajed, Nadim Kobeissi, and Jonathan
   Protzenko. 2019. EverParse: Verified Secure Zero-Copy Parsers for Authenticated Message Formats.. In Proceedings of the
   USENIX Security Symposium.
24                                                                                                             Reitz et al.


 Aseem Rastogi, Guido Martínez, Aymeric Fromherz, Tahina Ramananandro, and Nikhil Swamy. 2021. Programming and
   Proving with Indexed Effects. Technical Report. https://www.fstar-lang.org/papers/indexedeffects/.
 John Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings of the IEEE Symposium
   on Logic in Computer Science (LICS).
 Chris Rohlf. 2020. Isolation Alloc. https://struct.github.io/iso_alloc.html.
 Arash Sahebolamri, Scott D Constable, and Steve J Chapin. 2018. A Formally Verified Heap Allocator. Electrical Engineering
   and Computer Science - Technical Reports (2018). https://surface.syr.edu/eecs_techreports/182.
 Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. 2021. RefinedC:
   Automating the Foundational Verification of C Code with Refined Ownership Types. In Proceedings of the Conference on
   Programming Language Design and Implementation (PLDI).
 Adam Sandberg Ericsson, Magnus O Myreen, and Johannes Åman Pohjola. 2019. A verified generational garbage collector
   for CakeML. Journal of Automated Reasoning 63 (2019), 463–488.
 Thibaut Sautereau. 2021. Undefined behavior in get_large_size_class(). https://github.com/GrapheneOS/hardened_malloc/
   issues/133.
 Sam Silvestro, Hongyu Liu, Corey Crosser, Zhiqiang Lin, and Tongping Liu. 2017. FreeGuard: A Faster Secure Heap
   Allocator. In Proceedings of the ACM Conference on Computer and Communications Security (CCS).
 Nikhil Swamy, Catalin Hritcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon Forest, Karthikeyan
   Bhargavan, Cédric Fournet, Pierre-Yves Strub, Markulf Kohlweiss, Jean-Karim Zinzindohoué, and Santiago Zanella-
   Béguelin. 2016. Dependent Types and Multi-Monadic Effects in F*. In Proceedings of the ACM Symposium on Principles of
   Programming Languages (POPL).
 Nikhil Swamy, Tahina Ramananandro, Aseem Rastogi, Irina Spiridonova, Haobin Ni, Dmitry Malloy, Juan Vazquez, Michael
   Tang, Omar Cardona, and Arti Gupta. 2022. Hardening attack surfaces with formally proven binary format parsers. In
   Proceedings of the Conference on Programming Language Design and Implementation (PLDI).
 Nikhil Swamy, Aseem Rastogi, Aymeric Fromherz, Denis Merigoux, Danel Ahman, and Guido Martínez. 2020. SteelCore:
   An Extensible Concurrent Separation Logic for Effectful Dependently Typed Programs. In Proceedings of the International
   Conference on Functional Programming (ICFP).
 Laszlo Szekeres, Mathias Payer, Tao Wei, and Dawn Song. 2013. SoK: Eternal War in Memory. In Proceedings of the IEEE
   Symposium on Security and Privacy (S&P).
 The Shellphish Team. 2023. Educational Heap Exploitation. https://github.com/shellphish/how2heap.
 Theftguy. 2020. Major Bug in glibc is Killing Applications With a Memory Limit. https://thehftguy.com/2020/05/21/major-
   bug-in-glibc-is-killing-applications-with-a-memory-limit/.
 Harvey Tuch, Gerwin Klein, and Michael Norrish. 2007. Types, Bytes, and Separation Logic. In Proceedings of the ACM
   Symposium on Principles of Programming Languages (POPL).
 Erik van der Kouwe, Taddeus Kroes, Chris Ouwehand, Herbert Bos, and Cristiano Giuffrida. 2018. Type-After-Type:
   Practical and Complete Type-Safe Memory Reuse. In Proceedings of the Annual Computer Security Applications Conference
   (ACSAC).
 Robert NM Watson, Simon W Moore, Peter Sewell, and Peter G Neumann. 2019. An introduction to CHERI. Technical
   Report. University of Cambridge, Computer Laboratory.
 John Wickerson, Mike Dodds, and Matthew Parkinson. 2010. Explicit stabilisation for modular rely-guarantee reasoning.
   In Proceedings of the European Conference on Programming Languages and Systems (ESOP).
 Brian Wickman, Hong Hu, Insu Yun, DaeHee Jang, JungWon Lim, Sanidhya Kashyap, and Taesoo Kim. 2021. Preventing
   Use-After-Free Attacks with Fast Forward Allocation. In Proceedings of the USENIX Security Symposium.
 Paul R. Wilson, Mark S. Johnstone, Michael Neely, and David Boles. 1995. Dynamic storage allocation: A survey and
   critical review. In Proceedings of the International Workshop on Memory Management (IWMM).
 Carter Yagemann, Simon P. Chung, Brendan Saltaformaggio, and Wenke Lee. 2023. PUMM: Preventing Use-After-Free
   Using Execution Unit Partitioning. In Proceedings of the USENIX Security Symposium.
 Katherine Q. Ye, Matthew Green, Naphat Sanguansin, Lennart Beringer, Adam Petcher, and Andrew W. Appel. 2017.
   Verified Correctness and Security of mbedTLS HMAC-DRBG. In Proceedings of the ACM Conference on Computer and
   Communications Security (CCS).
 Dachuan Yu, Nadeem A Hamid, and Zhong Shao. 2003. Building certified libraries for PCC: Dynamic storage allocation. In
   Proceedings of the European Conference on Programming Languages and Systems (ESOP).
 Insu Yun, Woosun Song, Seunggi Min, and Taesoo Kim. 2021. HardsHeap: a universal and extensible framework for
   evaluating secure allocators. In Proceedings of the ACM Conference on Computer and Communications Security (CCS).
 Yu Zhang, Yongwang Zhao, David Sanan, Lei Qiao, and Jinkun Zhang. 2019. A verified specification of TLSF memory
   management allocator using state monads. In Proceedings of the International Symposium on Dependable Software
   Engineering: Theories, Tools, and Applications (SETTA).
StarMalloc: A Formally Verified, Security-Oriented Memory Allocator                                             25


  Benchmark               dh      ff hm        iso mi-sec mng scudo                  sg sn-sec         st glibc
  barnes               1.036 1.005 1.0 1.003            1.003      1.0 1.005        1.0      1.0      1.0      1.0
  cfrac                1.446 0.762 1.0 0.986            0.646 0.738 0.675 0.541           0.528    1.278 0.544
  espresso             1.273 0.917 1.0 0.999            0.736 1.301 0.753 0.707           0.642    2.284 0.707
  gs                   2.278 1.157 1.0 0.435            0.357 0.678 0.374 0.339           0.452    1.304 0.339
  larsonN            17.097 2.164 1.0 6.254             0.144 2.251 0.215          0.09   0.073    1.036     0.09
  larsonN-sized      16.823 2.121 1.0 6.165             0.141      2.2 0.211 0.088        0.072    1.008 0.088
  leanN                6.249 0.707 1.0        6.81      0.602 1.421 0.666 0.615           0.515    1.086 0.617
  lua                    TO 1.382 1.0 0.883             0.768     1.05 0.755 0.728        0.724    1.554 0.729
  mathlib               ERR 0.726 1.0 1.258             0.652 0.779 0.686 0.649           0.562    1.221 0.645
  redis                2.809 0.764 1.0 1.449            0.919     0.82 0.638       0.59   0.559 16.379 0.592
  rocksdb               ERR 0.921 1.0 ERR               0.903 ERR 0.874 0.829              ERR     0.843 0.813
  z3                   5.063 0.813 1.0         1.0       0.75 0.813       0.75 0.688      0.625    1.375 0.688
  alloc-test1          2.051 0.757 1.0 1.096            0.587 0.922 0.569 0.521           0.426    1.291 0.515
  alloc-testN        12.566 0.288 1.0 5.185             0.158 3.693 0.166 0.135           0.112    1.574 0.136
  cache-scratch1       1.006 1.006 1.0         1.0      0.994 0.994 0.994 0.994           0.994    0.994 0.994
  cache-scratchN       0.977 1.023 1.0         1.0      0.977 0.977 0.977 0.977           0.977       1.0 0.977
  cache-thrash1        1.006   1.05 1.0        1.0      0.994 0.994 0.994 0.994           0.994       1.0 0.994
  cache-thrashN           1.0 1.023 1.0 1.186              1.0     1.0     1.0      1.0      1.0      1.0      1.0
  glibc-simple            1.5 0.632 1.0 0.976           0.519 1.187 0.567 0.456           0.313    1.931 0.453
  glibc-thread       10.033 0.284 1.0 5.295              0.11 3.161       0.12 0.071      0.061    1.679 0.074
  malloc-large         3.604 1.036 1.0        0.58      0.538 1.034 1.036 0.539           0.545    1.046 0.539
  mleak10              1.692     5.0 1.0       1.0      0.923 0.923        1.0 1.231      0.923       1.0 1.231
  mleak100             1.754 5.566 1.0 1.041            1.016      1.0 1.057 1.369        0.975    1.041 1.369
  mstressN             5.251 0.812 1.0 2.677            0.462 1.722        0.7 0.413      0.354    1.605 0.435
  rbstress1             1.14   0.85 1.0 0.984           0.863 0.809 0.764 0.817           0.779    0.895 0.812
  rbstressN            1.285 0.757 1.0 1.051            0.797 0.782 0.755 0.805           0.883    0.939     0.76
  rptestN              7.521 3.404 1.0 2.432            0.471 1.414 1.015 0.397           0.535 19.537 0.387
  sh6benchN          22.109 0.305 1.0 7.598             0.129 3.239 0.502 0.173           0.074    1.649 0.175
  sh8benchN          13.098 0.302 1.0 9.578             0.121 2.229 0.648 0.134           0.063    1.256 0.133
  xmalloc-testN        8.978 0.298 1.0 3.559            0.116 1.543 1.887 0.204           0.062     1.17 0.205
Table 3. Execution time of various programs, measured against the following allocators: dieharder (“dh”,
[Novark and Berger 2010], revision 640949f), FFmalloc (“ff”, [Wickman et al. 2021], revision 2f24ecf), hard-
ened_malloc default version (“hm”, [GrapheneOS Development Team 2021], revision 995ce07), isoalloc (“iso”,
[Rohlf 2020], revision 2670d5f), mimalloc-secure (“mi-sec”, [Leijen et al. 2019], revision b66e321), nextgen
malloc implementation for musl libc (“mng”, [Felker 2020], revision 2ed5881), scudo (“scudo”, [LLVM Project
2023], revision 1654d7d), slimguard (“sg”, [Liu et al. 2019], revision 7d9139a), snmalloc-secure (“sn-sec”, [Liétar
et al. 2019], revision dc12688), StarMalloc (“st”, this work), and the glibc allocator (“glibc”, version 2.38). All
times are normalized and presented relative to hardened_malloc. Benchmarks ending in N exercise very
narrow patterns of allocation which stress-test the allocator and are not representative of a general usage
pattern. StarMalloc exhibits pathologically bad performance on the rptestN and redis benchmarks, which
particularly test large allocations, currently under-optimized in StarMalloc. ERR corresponds to crashes
during benchmarking, and TO represents cases that exceeded the time allocated for benchmarking



A   PERFORMANCE BENCHMARKS
26                                                                                             Reitz et al.


  Benchmark             dh      ff hm        iso mi-sec mng scudo              sg sn-sec       st glibc
  barnes             0.774  1.158 1.0 0.959        0.753 0.745 0.702 0.686            0.74 0.832 0.699
  cfrac              0.261  8.595 1.0 1.046          0.15     0.1 0.181 0.111        0.124   0.81 0.113
  espresso            0.18  0.924 1.0 1.203        0.144 0.066 0.122 0.063           0.327 1.399 0.062
  gs                 0.797  1.876 1.0 1.383        0.766 0.524 0.553 0.517           0.743   1.39 0.513
  larsonN            0.659  2.213 1.0 0.921        0.906 0.369 0.462         0.69    1.137 2.277 0.664
  larsonN-sized       0.69  2.251 1.0 0.933        0.938 0.351 0.469 0.676           1.129 2.292     0.78
  leanN              1.421  7.883 1.0 2.834        1.117 0.688 0.856 0.754           1.153 1.417     0.78
  lua                  TO   1.077 1.0 1.334        0.764 0.639 0.753 0.645           0.794 1.338 0.654
  mathlib             ERR    2.25 1.0 4.711        1.071 0.626 0.718         0.66    0.891 2.004 0.676
  redis              0.493  2.095 1.0 1.166        0.369 0.216 0.255 0.207           0.301 1.339 0.205
  rocksdb             ERR   1.859 1.0 ERR            1.03 ERR 0.755 0.774             ERR 1.471 0.785
  z3                 0.622  1.593 1.0 1.511        0.615 0.417 0.459          0.4    0.646 1.294 0.401
  alloc-test1        0.447 16.602 1.0 2.122          0.42 0.292 0.362 0.305          0.368 1.471 0.305
  alloc-testN        0.302 19.276 1.0       0.92   0.611 0.247 0.285 0.201           0.295 2.678 0.201
  cache-scratch1 0.205      2.737 1.0       1.07   0.288 0.133 0.141 0.133           0.141 0.445 0.133
  cache-scratchN      0.22  2.933 1.0 1.227        0.309 0.144 0.152 0.146           0.153 0.555 0.159
  cache-thrash1      0.219   2.94 1.0 1.151        0.308 0.143 0.149 0.142            0.15 0.401 0.143
  cache-thrashN 0.204       2.735 1.0 1.072        0.285 0.135 0.141 0.135           0.141 0.517 0.133
  glibc-simple       0.248  1.343 1.0 1.119        0.201 0.055 0.206 0.058           0.086 0.744 0.058
  glibc-thread       0.133  0.547 1.0 0.599        0.458 0.032 0.096 0.057           0.428 2.813 0.056
  malloc-large       0.928  1.084 1.0 4.295        1.288 0.918 0.918 1.197           1.547 0.928 1.196
  mleak10            0.284  2.683 1.0 1.018        0.294    0.07 0.156 0.143            0.1 0.682 0.146
  mleak100           0.258 12.671 1.0 0.974        0.266 0.062 0.141 0.139            0.09 0.618 0.128
  mstressN           0.811  1.041 1.0 2.407        1.774 0.681 0.755 1.561           1.329   1.12 1.521
  rbstress1          1.177  1.093 1.0        2.0   0.868 0.905 1.004 0.708           0.802 0.925 0.708
  rbstressN          0.705  1.023 1.0 1.803        1.277 0.684       0.76 1.096      1.062 0.941      1.0
  rptestN            0.534  0.736 1.0       0.81   0.611 0.234 0.257 0.265           0.699   2.59 0.254
  sh6benchN          1.771  5.287 1.0 5.416        0.901 0.868 1.189 1.061           0.987   1.12 1.056
  sh8benchN          1.075  1.004 1.0 2.673          1.39 0.803 0.774 0.996          1.259   1.21 0.982
  xmalloc-testN      0.836  0.956 1.0 0.536        0.625 0.066 0.746 0.806           0.564 0.393 0.815
Table 4. Resident Set Size (RSS) memory usage for various programs, measured against the same set of
allocators as Table 3. Numbers are, as before, normalized and presented relative to hardened_malloc.
