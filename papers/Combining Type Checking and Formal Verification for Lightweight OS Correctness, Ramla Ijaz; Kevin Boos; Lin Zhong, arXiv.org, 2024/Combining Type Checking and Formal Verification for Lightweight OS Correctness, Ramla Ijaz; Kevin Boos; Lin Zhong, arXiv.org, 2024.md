                                         Combining Type Checking and Formal Verification for Lightweight OS Correctness
                                                         Ramla Ijaz                                  Kevin Boos                                   Lin Zhong
                                                     ramla.ijaz@yale.edu                       kevinaboos@gmail.com                           lin.zhong@yale.edu
                                                       Yale University                            Theseus Systems                                Yale University

                                         Abstract                                                                guarantee the absence of overlap between the values of two
                                         This paper reports our experience of providing lightweight              separate instances of the same linear type. This shortcoming
                                         correctness guarantees to an open-source Rust OS, Theseus.              led to an insidious bug in the original memory subsystem of
                                         First, we report new developments in intralingual design that           Theseus [12], for which we report and contribute a solution.
                                         leverage Rust’s type system to enforce additional invariants               Motivated by the limitation of intralingual design, we ad-
                                         at compile time, trusting the Rust compiler. Second, we de-             vocate a hybrid approach that combines intralingual design,
arXiv:2501.00248v1 [cs.OS] 31 Dec 2024




                                         velop a hybrid approach that combines formal verification,              formal verification, and informal reasoning to achieve light-
                                         type checking, and informal reasoning, showing how the type             weight correctness for OSes (§4). We consider it lightweight
                                         system can assist in increasing the scope of formally verified          not only because it requires much less effort compared to
                                         invariants. By slightly lessening the strength of correctness           conventional formal verification, but also because its strength
                                         guarantees, this hybrid approach substantially reduces the              of guarantee is weaker due to usage of informal reasoning
                                         proof effort. We share our experience in applying this ap-              and implicit trust of the implementation language. We aim
                                         proach to the memory subsystem and the 10 Gb Ethernet                   to maximize use of the type system through intralingual de-
                                         driver of Theseus, demonstrate its utility, and quantify its            sign, as it is a low-effort way to realize stronger correctness
                                         reduced proof effort.                                                   guarantees. To that end, we introduce the idea of intralingual
                                                                                                                 specifications which allow the compiler to check type-related
                                                                                                                 correctness properties. Then, when proving an invariant, we
                                         1   Introduction                                                        only apply formal verification where said properties cannot
                                         Correctness is a desirable yet challenging property to achieve          be upheld by the type system, where the increased guarantee
                                         for systems software such as an operating system (OS). A key            justifies the proof effort. Since formal verification is expen-
                                         technology for correctness is formal verification. In recent            sive, we present three rules that help to increase the reach of
                                         years, various formal verification approaches have emerged              formally-verified invariants using the type system.
                                         that make different trade-offs between expressiveness and                  In §5, we report our experience in applying this approach to
                                         proof effort, i.e., what can be proven vs. how difficult it is to       revise the memory subsystem of Theseus and to implement a
                                         generate those proofs (§2).                                             driver for the Intel 82599 NIC. In the memory subsystem, we
                                            This paper presents our experience exploring new ways to             create representations of the Pages and Frames types, which
                                         ensure OS correctness. Toward achieving high expressiveness             are fundamental to memory management in Theseus. Using
                                         with low proof effort, we relax the strength of correctness             our hybrid approach, we verify functions that create these
                                         guarantees. We observe that while full formal verification is           representations and reason about how this leads to stronger
                                         desirable, the type system of the implementation language,              guarantees of the original Theseus invariants. In the process,
                                         i.e., Rust, combined with informal reasoning can also be used           we eliminate an insidious class of bugs. In the network driver,
                                         to provide weaker yet distinctly useful guarantees.                     we show that extending intralingual design can avoid com-
                                            In §3, we further develop the idea of intralingual design            mon driver bugs and that our hybrid approach can uphold
                                         introduced by Theseus OS [12], expanding its reach with new             core invariants with less proof effort than end-to-end verified
                                         techniques. Intralingual design uses language-level features            drivers.
                                         to enforce invariants via the compiler. We present the idea of a           We evaluate the “lightweightedness” of our approach and
                                         representation, a linear type instance that is the sole means of        quantify any performance overhead in §6. We show that the
                                         accessing a system resource, and show how to use language               hybrid approach has low development burden: the proof-to-
                                         features to shift resource management responsibilities into             implementation ratio is 1:117 for the memory subsystem, and
                                         the compiler. We then show how to use linear type instances             1:8.3 for the ixgbe driver. We find that our hybrid approach has
                                         as a proof of work, which can enforce correct ordering for              negligible performance overhead: our ixgbe driver performs
                                         operations. Lastly, we present how to write an intralingual             similarly to other research drivers with correctness guarantees,
                                         Hardware Abstraction Layer (HAL) that statically prevents               with a maximum throughput only 5% lower than the DPDK
                                         bugs at the hardware programming interface.                             ixgbe driver. We also use the intralingual HAL of our ixgbe
                                            We analyze the limits of intralingual design, showing that           driver to find previously unreported bugs in ixgbe drivers
                                         the invariants presented in [12] were based on an incomplete            from other Rust-based OSes such as ixy [15], Redox [6], and
                                         foundation: while Rust’s ownership model guarantees that                RedLeaf [28].
                                         an instance of a linear type has a single owner, it cannot                 In summary, this paper makes three contributions:
                                                                                                             1
• A new set of techniques to expand the scope and extend               it cannot be duplicated [21, 28]. The ownership of such an
  the reach of intralingual design.                                    instance automatically confers the right to use it without the
• A hybrid proof approach that combines type checking (as              need for runtime checks of its authenticity [16, 28]. Since a
  used by intralingual design), formal verification, and infor-        capability is of a linear type, it has a single owner, and Rust’s
  mal reasoning to improve OS correctness.                             built-in ownership rules can prevent data races and automati-
• Our experience applying this low-effort approach to in-              cally insert destructors. In §3.1, we take inspiration from this
  crease the proven correctness of a real system, namely the           idea by representing OS resources with linear-type instances.
  memory subsystem and ixgbe driver of Theseus.                           Linear Types for Statically-Enforced State Machines: A
                                                                       linear type system can prevent incorrect state machine tran-
                                                                       sitions by implementing the state machine using behavioral
2   Background and Related Work                                        type techniques, e.g., typestates and session types. When com-
                                                                       bined with linear types, a typestate protocol can be statically
Rust’s Type System. A language type system is a lightweight
                                                                       validated [16], imposing no runtime overhead.
formal method for encoding program behaviors. The Rust
programming language employs a linear (technically, affine)            Formal Verification. Formal verification is expensive; devel-
type system [32] in which a variable can only be used at most          opers often limit expressiveness, i.e., what can be proven, in
once. This prevents aliasing by restricting each instance to           order to control the cost. A formally-verified system consists
one owner, represented by a variable binding that "owns" the           of three parts: implementation, specification, and proof. Vari-
underlying memory. An instance of a linear type cannot be              ous formal verification approaches have emerged that make
duplicated via copying or cloning; rather, ownership of that           different trade-offs between expressiveness and proof effort,
instance can only be assigned (moved) to another variable              i.e. what can be proven vs. how difficult it is to generate those
binding, preventing the prior owner from using it again.               proofs. Interactive theorem proving is the most expressive,
   Rust’s linear type-based ownership model allows memory              as it can reason about higher-order logic but suffers from the
usage and aliasing to be statically determinable in most cases.        largest proof effort, measured by the proof-to-implementation
The compiler can track the lifetime of an instance and insert          ratio, 13: 1 for CertiKOS [17]. By employing SMT solvers
code, i.e., a drop handler, to reclaim it when its owner’s scope       to find proofs, later works were able to substantially lower
ends. As a result, Rust programs are both memory and concur-           the proof effort at the cost of limiting proof requirements
rency safe without underlying runtime or garbage collection,           to first-order logic. However, even so-called push-button ap-
achieving performance close to other systems programming               proaches [29, 30, 35, 36, 41] still suffer from significant proof
languages like C and C++. Not surprisingly, it has become              effort, even for very small system software and for proving
popular in systems programming in recent years, including              limited invariants, mainly restricted to the decidable portion
implementing operating systems [12, 22, 28].                           of first-order logic. For example, Serval [29], implemented
   In addition to ownership, Rust allows instances to be tem-          in 2K LoC, requires an additional 3.1K LoC for its specifica-
porarily "borrowed" by another variable binding (reference)            tion and verifier tools. Our hybrid approach aims to further
without transferring ownership. Rust enforces aliasing XOR             lower this proof effort by exploiting the type system of the
mutability, wherein there can only exist one mutable refer-            implementation language and informal reasoning, at the cost
ence or multiple immutable references to an owned instance             of lowered strength of guarantee.
at a given time, but not both.
                                                                       Other Related Work. Our work is complementary to the lit-
Rust for Correctness. Many have leveraged Rust’s type                  erature that also exploits linear types in systems software for
system to ensure correctness beyond safety. We next briefly            other purposes. The Singularity project [19] popularized lin-
review these ideas before developing them further in §3.               ear types for OS design and used them for zero-copy sharing
   Linear Types for Pairwise Operations: Many operations               of heap memory across software-isolated domains. Recent
must always occur in pairs, e.g., memory allocation/deallo-            works have used Rust’s ownership model for features such
cation, lock acquisition/release, and reference count incre-           as lightweight fault isolation [28], zero-copy communication
ment/decrement. Mismatchings of such pairwise operations               [31], compiler-checked session types [20], decentralized re-
are common in the Linux kernel [23, 24, 39]. This prob-                source management [12], and static information flow control
lem can be solved by using linear types, placing the first             and automatic program state manipulation [11].
operation in the constructor and the second in the destruc-               Related to our hybrid approach, Yang and Hawblitzel cre-
tor. Rust itself follows this design pattern for heap-allocated        atively combined formal verification and a safe implementa-
data structures (Vec<T> [9]), locks (MutexGuard<T> [8]), and           tion language by dividing the OS into a lower core Nucleus
reference-counted pointers (Arc<T> [7]).                               and a higher kernel in building the Verve OS [40]. They
   Linear Types as Unforgeable Capabilities: In Rust, an in-           applied formal verification to the Nucleus, implemented in
stance of a linear type is a unique and unforgeable capability         assembly, for safety and correctness, while relying on the
as long as it does not implement the Clone trait, meaning              implementation language (C#) for the kernel’s safety. Our
                                                                   2
hybrid approach does not mandate a strict division between                  1   // Pages is a representation of a range of virtual pages.
verified and unverified OS portions. Instead, we use a combi-               2   struct Pages<S: State> {
                                                                            3      range: RangeInclusive<usize>
nation of proof techniques in whichever subsystem we aim                    4   }
to prove an invariant about, pairing each correctness property              5   // The possible states a Pages instance can be in.
                                                                            6   enum State {
with the proof technique best suited to it. Our work designs                7      Free,
and implements the OS so that the Rust type system can pro-                 8      Allocated,
                                                                            9      Mapped,
vide guarantees that go beyond safety, in collaboration with               10      Unmapped
formal verification.                                                       11   }
                                                                           12   // Only Pages in the Mapped state can access memory.
   Related to our application of intralingual design to The-               13   impl Pages<Mapped> {
seus’s ixgbe driver, Vigor [41] found errors in the DPDK                   14      pub fn write(&mut self, data: [u8]);
                                                                           15      pub fn read(&self) -> &[u8];
ixgbe driver by symbolically executing it against an 82599                 16      fn unmap(self) -> Pages<Unmapped>;
hardware model, using assertions to catch bit-level errors.                17   }
                                                                           18
TinyNF [33] introduced a simplified driver model with fewer                19   impl<S: State> Drop for Pages<S> {
code paths, enabling faster verification of network functions              20      fn drop(&mut self) {
that run on top of it. Ironclad [18] verified a 1 Gbps Ethernet            21         match S {
                                                                           22            State::Free => {
driver using the Dafny verification language. Unlike these                 23               // Re-take ownership of the pages by replacing it
approaches, our method proves driver correctness using a                   24               // with an empty range; return it to page allocator.
                                                                           25               let pages = replace(&mut self, Pages::empty());
combination of the Rust type system and verification, which                26               free_pages_list.insert(pages);
reduces both specification and proof effort.                               27            }
                                                                           28            State::Mapped => {
                                                                           29               // PTE(s) have been cleared, so we transition
                                                                           30               // the Pages to the Unmapped state.
3     Intralingual Design                                                  31               let pages = replace(&mut self, Pages::empty());
                                                                           32               pages.unmap(); // Drop the returned Pages<Unmapped>
Intralingual design [12] aims to maximize the compiler’s role              33           } ...
in enforcing correctness by leveraging programming language                34         }
                                                                           35      }
features, namely type systems, to more precisely convey sys-
                                                                           36   }
tem requirements to the compiler. In other words, it encodes
                                                                        Listing 1. An example of using an IRS to manage virtual memory. A
the requirements into the implementation itself, such that they
                                                                        Pages instance is a representation of a range of pages, which can be
can be enforced by the compiler. Many requirements can-                 in one of four states. When a Pages<Mapped> instance is dropped,
not be so encoded because the type system is not expressive             it is eventually returned to the Free state and stored in the list of
enough to convey them. We categorize these requirements                 free pages. The code has been simplified for brevity/readability.
as extralingual. Our objective herein is to build upon recent
works on Rust for Correctness (§2) and introduce a system-
atic methodology for incorporating linear types and other
type-based techniques into low-level system design.                     compiler, which ensures that (i) there is only ever one mutable
   We leverage linear types in three ways. (i) First, we use lin-       reference to the representation at a time, and (ii) access to the
ear types to create an exclusive representation for a resource,         representation is governed by the rules conveyed via the type
both physical and virtual (§3.1). (ii) Second, we use linear            system. We note that Rust already use linear type instances as
types as a proof of work by using distinct types for function           a limited form of representations for memory objects, but IRS
return values and preventing said types from being otherwise            extends this to apply representation types to arbitrary system
instantiated via any other code path (§3.2). (iii) Third, we em-        resources beyond just memory. We realize the following key
ploy type-system techniques to enforce datasheet-compliant              features of an IRS:
communication with the hardware (§3.3).
                                                                        Changing Access Rights via Typestates. The access rights
                                                                        of a representation are defined by publicly visible methods
3.1   Intralingual Representation System                                of its type. Each typestate represents a distinct set of access
We present an Intralingual Representation System (IRS) that             rights, which change with state transitions. A state transi-
shifts some of the responsibility of managing system re-                tion method takes a representation as input, consumes it, and
sources from the OS to the compiler. Typically, an OS creates           changes its state. For example, in Listing 1, a Pages instance
software objects to represent physical or abstract resources,           is a representation that can be in one of four states: Free,
e.g., Linux uses struct page objects to represent physical              Allocated, Mapped, or Unmapped (L6); its methods transition
memory frames. The IRS combines the representation of a                 the representation between these states, e.g., unmap() in L16.
resource with the authority to use it, through linear types: the        The compiler can enforce that the representation is accessed
ownership of the linear-type instance denotes the sole author-          according to the restrictions of its current state. For example,
ity to use the resource. We call this instance a representation         in the Free, Allocated, and Unmapped states, page table en-
of the resource. Representations in an IRS are checked by the           tries (PTEs) are not set up for the given pages, so the Pages
                                                                    3
representation cannot be used to access the underlying mem-                 1    // register struct which is mapped to the MMIO region
ory range. This is statically enforced by implementing read()               2    pub struct IntelIxgbeRegisters {
                                                                            3        rxctrl:     ReadWrite<u32>,
and write() only for Pages in the Mapped typestate (L14).                   4        pub gprc:   ReadOnly<u32>,
                                                                            5        fctrl:      ReadWrite<u32>,
Delegation via Ownership Transfer, Sharing, Borrowing.                      6    }
                                                                            7
A representation is a singleton with either one exclusive owner             8    // linear types that serve as a proof of work
or multiple owners that can only mutably access it through a                9    pub struct RxCtrlDisabled(());
                                                                           10    pub struct FilterCtrlSet(());
mutual exclusion mechanism, upholding Rust’s aliasing XOR
                                                                           11
mutability (§2). An owner can conveniently delegate authority              12    // filters that can be enabled
by granting access to the representation in one of three ways:             13    bitflags! {
                                                                           14        pub struct FilterCtrlFlags: u32 {
(i) transferring ownership to a new owner who gains exclusive              15            const STORE_BAD_PACKETS              = 1 << 1;
access, (ii) sharing ownership via a reference-counted smart               16            const MULTICAST_PROMISCUOUS_ENABLE   = 1 << 8;
                                                                           17            const UNICAST_PROMISCUOUS_ENABLE     = 1 << 9;
pointer so multiple parties can co-own the representation, or              18            const BROADCAST_ACCEPT_MODE          = 1 << 10;
(iii) temporary (scoped) lending to a borrower that can access             19        }
                                                                           20    }
the representation through a reference.                                    21
                                                                           22    // register access methods
Returning Representations via Automatic Destructors.                       23    impl IntelIxgbeRegisters {
We can shift the complex responsibility of realizing correctly-            24        pub fn rxctrl_rx_disable(&mut self) -> RxCtrlDisabled;
                                                                           25        pub fn fctrl_write(
ordered cleanup sequences from the programmer to the com-                  26            &mut self,
piler by placing all cleanup code in a linear type’s destructor            27            val: FilterCtrlFlags,
                                                                           28            rx_disabled: RxCtrlDisabled
(a Rust Drop handler). This is important for representations               29        ) -> FilterCtrlSet;
that represent physical resources (e.g., physical frames) that             30        pub fn rxctrl_rx_enable(&mut self, fctrl_set: FilterCtrlSet)
                                                                           31    }
should never be destroyed: these representations must be
returned to the OS for future use. With typestates, a repre-            Listing 2. A portion of the Intel 10 GbE driver intralingual HAL.
                                                                        The padding between the registers which forces them to lie at their
sentation can have multiple drop handlers, one for each state;
                                                                        correct offset in the MMIO region is ommitted for space.
each state’s drop handler undoes any changes made when
entering that state, reverting the representation to its previous
state. The drop handler for the initial state finally returns the       used for this purpose is simply a type that can only be in-
instance back to the OS for storage. For example, in Listing 1,         stantiated by a single function that first performs the required
the drop handler for Pages in the Mapped state removes the              “work.” To prevent instances of this type from being created
PTEs and converts it to the Unmapped state (L28). Then, each            anywhere, we ensure it is composed of a private inner type
predecessor state’s drop handler is iteratively invoked until           that is inaccessible outside of the type’s module.
the Pages instance returns to the Free state, upon which the               Combining linear types as a proof of work with strongly-
Pages<Free> instance is returned to a redblack-tree of free             typed function interfaces can statically enforce an order be-
page chunks maintained by the page allocator (L22).                     tween “stages” of operations. That is, we can create a chain of
                                                                        functions where one function creates and returns an instance
Representation vs. Capability: The notion of a representa-              of a linear type to be consumed by the next function, effec-
tion may remind the readers of that of a capability. Like a             tively requiring each instance of a linear type to be used in the
capability, a representation is also unforgeable and delegable.         order it is created for progress to be made. In fact, this pattern
Unlike a capability, a representation is unique in that no two          of instantiation and then consumption lies at the core of many
representations exist in the system for the same resource. This         ways in which we use linear types (§2). The difference here
precludes derivation in which multiple copies of a capability,          is in what the type instance represents.
with varying access rights, exist at the same time. Importantly,
in-built language features do not provide all features of a ca-         3.3     Intralingual Hardware Abstraction Layers
pability system as reported by [27, 38]. Instead the OS must
use language-level mechanisms to implement these features,              An intralingual Hardware Abstraction Layer (HAL) enforces
such as revocation via a level of indirection.                          datasheet-provided rules for communicating with a given
                                                                        hardware device at compile-time. It is system-independent
                                                                        code that is reusable across drivers written in the same lan-
                                                                        guage. An intralingual HAL uses basic type system features
3.2   Linear Types as Proof of Work                                     such as structs with associated methods, type wrappers, vis-
The other main way we use linear types is to indicate that a            ibility modifiers, and enums to restrict access to MMIO fields
certain function has been executed, by returning a dedicated            and limit what can be written to them. It also uses linear types
type instance from the function. In this manner, a linear type          as a proof of work to enforce inter-field dependencies.
instance no longer represents a spatial resource, but rather               The core part of the intralingual HAL is a struct to repre-
a proof of a temporal action having occurred. A linear type             sent the layout of memory-mapped I/O (MMIO) registers and
                                                                    4
other I/O data structures, which can then be overlaid atop a            proof effort than formal verification. With intralingual design,
region of memory. This ensures that every register and bitfield         the proof effort is basically the implementation effort. We use
is always accessed in a type-safe manner at its correct offset          the SMT-based formal verification to prove select, important
(and alignment) within the underlying memory region. Our                properties. Unlike end-to-end verification common in most
approach precludes the unsafe pointer arithmetic commonly               formally verified systems, we employ selective verification
used to access MMIO registers, which cannot be reasoned                 and rely on the type system to carry forward proven invariants
about by the compiler. In Listing 2, the IntelIxgbeRegisters            throughout the system. Manual code inspection is only used
struct (L2) is part of the intralingual HAL for the Intel 82599         in a few simple cases where the type system is limited.
NIC. It defines the layout of the memory-mapped registers                  We also embrace informal reasoning, especially prose proofs,
taken from the datasheet [4].                                           to reason about higher-level invariants. Prose proofs can
   For portability, an initial version of the HAL may only              “stitch” together invariants proven by different proof tech-
use Rust primitive types or types that are also part of the             niques (and those specified in different languages) without
HAL. But a developer can tailor the HAL so that it references           requiring a unified formal specification, significantly lower-
system-specific types that carry an invariant, and that invariant       ing the proof effort. Within a prose proof, we use natural
serves as a valid pre-condition for a HAL function. For exam-           language to express the invariants and justify how they com-
ple, the set_entry function for a PTE in Theseus consumes               bine to imply a high-level invariant.
the type AllocatedFrame rather than a u64 physical address.                Given that a linear-type system itself cannot guarantee
AllocatedFrame carries the invariant that there is no existing          uniqueness of the resource represented by an instance, and
PTE for that frame, so it helps uphold the requirement that             that such uniqueness is the foundation of an IRS (§3.1), the
Theseus only adds PTEs for unmapped frames.                             uniqueness of a linear-type instance is an excellent candidate
                                                                        for formal verification. To formally verify that a linear-type
3.4   Limitations of Intralingual Design                                instance is unique, we only need to formally verify that the
                                                                        type’s constructors will never create instances that represent
Intralingual design, while powerful, is limited due to its re-
liance on the language’s type system. Firstly, it cannot reason         overlapping resources.
about unrestricted types: where they originated from or the             4.1   Rules to Extend the Reach of Verified Invariants
validity of their values. This limitation is fundamental to an
OS, in which the lowest layers must use built-in unrestricted/          As formal verification is the main source of proof effort in
                                                                        our hybrid approach, we give three rules to leverage the type
primitive data types like u32 in order to interact with hard-
                                                                        system to extend the reach of formally-verified guarantees.
ware.
   Moreover, as the IRS design uses a linear-type instance                 (i) Rule of Invariant Preservation: Once we have used
to represent an OS resource, a linear type system itself can-           formal verification to prove an invariant for a given linear
not guarantee uniqueness of the resource represented. This              type instance, the type system ensures that invariant will
goes beyond the intralingual (type-level) uniqueness based on           hold for the instance’s lifetime. No further verification is
                                                                        needed as long as arbitrary changes to the type’s fields are
Rust’s ownership model: no two variables of the same linear
                                                                        disallowed. A proven invariant for all instances of a type is
type can own the same value (memory object), but there is no
guarantee that the resources represented by the values (mem-            called a type invariant. Type invariants act as implicit pre-
ory objects) do not overlap. If there is an overlap, multiple           conditions when that type is used as a function argument and
instances of this type can give access to the same resource,            post-conditions when it is used in a return value, reducing the
i.e., the overlapping parts. This limitation underlies our dis-         lines of specification we have to write.
                                                                           (ii) Rule of Composition: An instance of a composite type
covery of an important bug in Theseus’s memory subsystem,
                                                                        is unique if its members are unique. Therefore, it is unneces-
discussed in §5.3.3.
   Finally, a linear type system is not as expressive as many           sary to formally verify uniqueness as a type invariant for every
formal verification techniques due to the limited invariants            representation in an IRS. Instead, by verifying the uniqueness
that can be enforced by the type system. Generally, it is inca-         property of select basic types in the system, e.g., Pages in
pable of proving any algorithmic property, e.g., that a sort()          Listing 1, we can rely on the type system to propagate and
                                                                        automatically enforce uniqueness for composite types built
function actually performs sorting.
                                                                        from these verified basic types. For example, a representa-
                                                                        tion of a device’s MMIO registers is composed solely of a
4     Hybrid Approach for Correctness                                   Pages<Mapped> instance; thus, the MMIO representation is
To overcome the limitations of intralingual design and the              unique because Pages<Mapped> is unique.
high proof effort of formal verification, we argue for a hy-               (iii) Rule of Reuse: Using Rust generics, we can formally
brid approach that pairs a correctness property with a proof            verify that a piece of generic code upholds an invariant, and
technique. We maximize the use of the type system because               the compiler automatically extends this verification to all spe-
it gives a high strength of guarantee with significantly lower          cialized instances. As an example, after writing and verifying
                                                                    5
just one implementation of a generic representation creator,            4.3   Increase in Trusted Code
we can then use it to create many other verified representa-            Selective verification leads to increased amounts of trusted
tions: Pages, Frames, and PCIDevice. In general, we strive to           code. Within a module, we trust that unverified code will not
verify code at lower layers of the system, with more generic/           break invariants proven by verified code. For every depen-
primitive types to increase the reusability of said formal proof.       dency of verified code, we must write a trusted specification
Types composed from these primitive types can directly call             so that the verifier can reason about its behavior. In our work,
the verified methods.                                                   we trust the Rust core and alloc libraries and have written
                                                                        trusted specification for multiple functions in the mem, num,
                                                                        cmp, option, result and vec modules. We also add trusted
4.2    Intralingual Specifications
                                                                        specification to other kernel crates in Theseus. In contrast,
While the type system can ensure certain properties, it alone           end-to-end verified systems have much smaller trust code.
cannot prove general correctness of the system implemen-
tation. Taking inspiration from how specifications used in
                                                                        5     Implementation
formal verification can prove correctness, we introduce a hy-
brid proof technique called intralingual specifications. We             We applied intralingual design (§3) and our hybrid correctness
realize these by leveraging Rust macros to specify correctness          approach (§4) to parts of Theseus OS. For each subsystem we
properties about a given type directly in the code, such that           modified, we identified the invariants of interest, implemented
they are automatically checked at compile time; this increases          an IRS and intralingual HAL. We then used Prusti [10], a
their strength of guarantee with low effort.                            Rust-based SMT-verification tool, to formally verify select
   The type-based properties that occur most frequently (in             functions which would help uphold the invariants along with
our experience) are that: (i) a type must not implement certain         the intralingual code. Our goal was to maximize reliance
traits, (ii) a type is composed of another type, (iii) a function       on the type system and compiler while minimizing formal
consumes an instance of a type, (iv) a type’s inner fields are          verification, either by applying our rules from §4.1 or by
private. For example, instances of the Pages type in Listing 1          writing intralingual specifications (§4.2).
must be unique. A proof of uniqueness here requires that the               To address the primary limitation of an IRS, the lack of
type is linear and does not expose its inner fields. These re-          a uniqueness guarantee, we wrote a verified generic inter-
quirements can be coded by implementing neither the Clone               face that creates representations. We then used this inter-
nor DerefMut traits for Pages, and by setting its range field           face to instantiate representations for both Frames and Pages,
to private, respectively. A change in the codebase, e.g., a             which form the basis of memory management in Theseus.
heedless developer implementing Clone for Pages, could in-              The uniqueness proof of Pages and Frames is essential to up-
advertently break the proof of uniqueness. Since said changes           holding the bijective mapping invariant of Theseus: each page
would not violate Rust type rules, the compiler alone could             in the system’s virtual address space can only be mapped to
not catch them.                                                         one frame of the physical address space, and vice versa. This
   To check such properties at compile time, we employ Rust             prevents extralingual aliasing, which is necessary to realize
macros to write static assertions. These assertions generate            memory isolation and safety for all system memory, not just
code that aborts compilation if the condition is not satisfied.         the heap and stack. In the network driver, we build upon said
We have written a tool to collect these assertions into a sepa-         memory invariants to show how our implementation upholds
rate file from the code base to make it easier for a developer          three correctness properties of a network driver: correct bit-
to review. For example, to prevent implementation of traits             level communication, software resource management, and
for the Pages type, we can add this line to Listing 1:                  bookkeeping of hardware state.
      assert_not_impl_any!(Pages: DerefMut, Clone);
To ensure that the inner field of Pages is private, we add this         5.1   Overview
attribute to the top of the Pages struct:                               In this section we detail our implementation of the RepCreator,
                #[private_fields("range")]                              our changes to the memory subsystem of Theseus, and our
We also implement additional attributes, #[nomutates] and               10 GbE ixgbe driver. The RepCreator is a struct with veri-
#[nocalls], to help prevent unverified functions from break-            fied methods to create representations. It maintains the 1-to-1
ing invariants proven by verified functions in the same module.         mapping between the physical resource and its software rep-
These attributes are placed at the top of a function to blacklist       resentation(s), shown as step ○ 1 in Figure 1. It is a prominent
the argument fields that should not be mutated and functions            example of how we use formal verification to increase the
that should not be called. Standard Rust can only enforce visi-         strength of guarantee of an IRS invariant. By following the
bility modifiers at a module boundary, but these attributes can         Rule of Reuse, we not only reduce the lines of code for cre-
enforce visibility restrictions within a module. Our implemen-          ating representations but also the lines of specification and
tation of these macros is available in the proc-assertions              proof. We implemented the RepCreator in 392 SLOC and its
crate on the Rust crate registry [5].                                   proof-to-implementation ratio is 1:56.
                                                                    6
                                                                                                                 Table 1. We found that approximately 50% of bugs in the DPDK
                                 Virtual Address Space                                                           ixgbe driver [2] can be eliminated with our hybrid approach. We
          1                                                                                                      classified bugs based on the correctness technique that can be used to
        RepCreator                                            5       IxgbeNIC                                   prevent them. A complete list of the bugs with the proposed solution
       Pages<Free>
                                    MEMORY                                       Queues                          for each can be found in Appendix A.
                                   SUBSYSTEM




                                                                                              IXGBE DRIVER
                                                                                Descriptor
          allocate                                                                Ring
                                                                                                                                Prevention Technique     Number of Bugs
                                                               Ixgbe              Packet                                        Basic Rust                  4 (13.8%)
     Pages<Allocated>                                         Registers           Buffer                                        Intralingual HAL            5 (17.2%)
          2 map          Pages<Mapped>              cast_as                                                                     IRS                         6 (20.7%)
                                                                                   Queue
                                                         3    PciDevice           Registers                                     Formal Verification        12 (41.4%)
    Frames<Allocated>                                                                                                           Hardware Issue              2 (6.9%)
          allocate                                            get_device

      Frames<Free>                                            PciDevice                    PCI
                                                                                        SUBSYSTEM                    1    pub struct RepCreator<T: ResourceIdentifier, R> {
        RepCreator                                            RepCreator                                             2        // for reps created before heap initialization
                                                                                                                     3        array: Option<StaticArray<T>>,
          1                                                       4
                                                                                                                     4        list: List<T>,
                       Physical Address Space                              PCI Bus
                                                                                                                     5        constructor: fn(&T) -> R
                                                                                                                     6    }
           Representation (created by RepCreator)              repr    consumed by
                                                                        this function                                7
              Representation (created by cast fn)                           verified                                 8    impl<T: ResourceIdentifier, R> RepCreator<T,R> {
                                                                           function
          Representation (unique by composition)
                                                                                                                     9        #[ensures(result.is_ok() ==> {
                                                                                                                    10            forall(|i: usize| i < old(self.list.len()) ==>
Figure 1. The Interplay of an IRS and Formal Verification in Theseus:                                               11                !old(self.list.lookup(i)).overlaps(&id))
                                                                                                                    12            &&
We create representations for Pages, Frames and PciDevices using                                                    13            result.is_ok() ==> self.list.lookup(0)) == id
the RepCreator, ensuring there is a 1-to-1 mapping between the                                                      14        })]
                                                                                                                              pub fn create_unique_representation(&mut self, id: T)
hardware resource and the software representation ○ 1,○ 4 . Functions                                               15
                                                                                                                    16            -> Result<R, RepresentationCreationError>
consume instances of Pages and Frames to transition them into the                                                   17        {
next state and to maintain the 1-to-1 mapping ○   2 . Once PTEs are                                                 18            if !self.list.elem_overlaps(id) {
                                                                                                                    19                self.list.push(&id);
added, a Pages instance is in the Mapped state and its represented
                                                                                                                    20                Ok(self.constructor(&id))
memory can be cast to other representations ○ 3 . We formally verify                                                21            } ...
the cast functions to uphold uniqueness. IxgbeNIC consists of mul-                                                  22        }

tiple representations and is unique by Rule of Composition ○  5.                                                    23    }
                                                                                                                    24
                                                                                                                    25    pub trait ResourceIdentifier: Copy {
                                                                                                                    26        #[pure]
   We used the RepCreator to instantiate Pages and Frames in                                                        27        fn overlaps(&self, other: &Self) -> bool;
                                                                                                                    28    }
the memory subsystem. Pages and Frames can be in different
typestates; the Mapped state gives access to the represented                                                     Listing 3. A RepCreator object provides a verified interface to
                                                                                                                 create unique representations. The postconditions of its public
memory (○   2 in Figure 1). The map state transition function
                                                                                                                 method specify that, if successful, the representation did not overlap
adds PTEs using an intralingual HAL. By applying our hybrid                                                      with any pre-existing representation and its identifying information
approach to the memory management subsystem of Theseus,                                                          was added to the bookkeeping. The Prusti keyword ensures starts a
we provide a stronger guarantee of the bijective mapping be-                                                     post-condition, old returns the value of an argument at the beginning
tween pages and frames, a core invariant of Theseus [12]. The                                                    of a function, and result refers to the return value
implementation effort for the memory subsystem changes was
1.3k SLOC with a proof-to-implementation ratio of 1:171.                                                         performance of the NIC driver is highly sensitive to overhead
   We implemented the ixgbe NIC driver of Theseus using                                                          and can be easily quantified, which allows us to evaluate any
our approach. The driver supports the Intel 10 GbE 82599                                                         overhead from the intralingual design. Third, after reviewing
NIC. Representations in the network driver are created in                                                        the bugs in the DPDK ixgbe driver, we found that a majority
three ways: through the RepCreator, e.g. , PciDevice, through                                                    could be prevented by techniques presented in this paper (Ta-
verified memory cast functions, e.g., IxgbeRegisters, or by                                                      ble 1), motivating us to focus on a network driver to evaluate
applying the Rule of Composition, e.g. IxgbeNIC (○       3 ,○
                                                            4 ,○
                                                               5                                                 our intralingual design techniques.
in Figure 1). The driver implementation was 2k SLOC, of
which only 141 lines required verification. The proof-to-                                                        5.2     Intralingual Representation System (IRS)
implementation ratio of the verified portion of the driver was                                                   An IRS uses a linear type system to shift resource manage-
1:8.3. The complete breakdown along with the additional                                                          ment tasks to the compiler, but the guarantees it provides are
effort to write external specifications is given in Table 2.                                                     weak if we don’t prove the uniqueness of every representation.
   We choose the NIC driver for three reasons. First, there is a                                                 To simplify this task, we implemented a generic representa-
rich literature about formally verifying its properties [18, 33].                                                tion creator; a portion of the code is given in Listing 3. The
We will be able to tease out the strengths and weaknesses                                                        representation creator is a generic struct (L1) composed of
of our approach in providing similar guarantees. Second, the                                                     verified bookkeeping data structures and a private constructor
                                                                                                             7
that creates a representation when given an identifier (L5).            as a frame can only be present in a single PTE. The mem-
The constructor can only be called through a verified method            ory subsystem of Theseus only adds a PTE when creating
of RepCreator in which we search the list of existing repre-            a Pages<Mapped> instance, and only removes it when drop-
sentations to make sure an overlapping one has not already              ping the same instance. Thus, proving the bijective mapping
been instantiated (L15).                                                invariant necessitates proving the correct construction and
   The RepCreator uses two generic types: R is the type of              destruction of a Pages<Mapped> instance.
the representation, and T is the type of the identifier; it con-
                                                                        5.3.1 Intralingual Design of the Memory Subsystem The
tains all the information required to create a representation
                                                                        functions to walk the page table and update PTEs are cate-
but itself does not give access to any resource. The former
                                                                        gorized as part of the intralingual HAL of the memory sub-
is a linear type, and the latter is a clonable type which im-
                                                                        system; a PTE can only be manipulated through a type-safe
plements the ResourceIdentifier trait (L25). We created the
                                                                        interface. We use an IRS to create a Frames and Pages type,
ResourceIdentifier trait so that the system developer can
                                                                        instances of which are the unique representation of a region
define what it means for representations of the same type to
                                                                        of physical or virtual memory, respectively. With typestate
overlap. The overlap trait method is considered part of the
                                                                        programming, we create four possible states for instances
specification, and the correctness of our invariant depends on
                                                                        of the Frames and Pages types: Free, Allocated, Mapped, and
its correct definition.
                                                                        Unmapped. Pages<Mapped> instances (which represent acces-
   For example, a representation of a PCI device is a PCIDevice
                                                                        sible memory) are used according to the rules of the Rust
object and its identifier is its bus, device, and function (slot)
                                                                        type system: one mutable reference or multiple immutable
numbers, collectively given by the type PCILocation. The
                                                                        references, which corresponds to a single writer or multiple
implementation of ResourceIdentifier for PCILocation de-
                                                                        readers to the underlying memory, but not both at the same
fines an overlap as when the bus, device and function num-
                                                                        time. A detailed code example of the Pages type is given in
bers are equal. Before scanning the PCI bus, we instantiate
                                                                        Listing 1.
a RepCreator <PCILocation, PCIDevice> object, and for ev-
                                                                           The memory subsystem first creates and stores Frames<Free>
ery connected device we create a representation of it through
                                                                        and Pages<Free> instances during its initialization routine,
the create_unique_representation method.
                                                                        once we have information about the size of the physical ad-
5.2.1 Proof Sketch: A Representation is Unique The unique-              dress space. A task will allocate Frames and Pages when it
ness invariant of an IRS states: Every representation is unique:        needs more memory; the allocate function transitions these
there is no overlap between representations of the same type.           instances to the Allocated state and returns them to the caller.
   We use our hybrid approach for correctness (§4) to present           The mapping function consumes instances in an Allocated
a prose proof of the uniqueness invariant, wherein we ex-               state, converts them to a Mapped state, and adds PTEs that
plicitly state where each proof technique is used. We list              associate each page represented by the Pages instance with
the Lemmas required to prove the invariant, and next to each            one frame represented by the Frames instance in order to cre-
Lemma we list the techniques used to prove it: formal verifica-         ate an exclusive, bijective mapping. The mapping function
tion (F), the type system (T) or intralingual spec assertion (IS).      returns the Pages<Mapped> instance to the caller such that it
We use a prose proof (P) to tie multiple techniques together.           can be used to access the underlying memory, but forgets
Our proof is based on the following three Lemmas.                       the Frames<Mapped> instance immediately as an efficiency
                                                                        optimization. The pages represented by a Pages<Mapped> in-
Lemma 1. A representation cannot be cloned or copied as it
                                                                        stance are unmapped upon being dropped, during which the
is a linear type and does not implement the Clone trait. [T, IS,
                                                                        drop handler clears the associated PTEs and transitions it
P]
                                                                        to the Unmapped state. The drop handler also recreates the
Lemma 2. Functions that create a representation or mutate
                                                                        previously-forgotten Frames<Unmapped> instance from infor-
its resource identifier always prevent overlaps. [F]
                                                                        mation stored in the PTEs. Once their TLB entries are invali-
Lemma 3. The resource identifier field of a representation is
                                                                        dated, the Frames and Pages are transitioned to the Allocated
never changed in unverified functions. [T, IS, P]
                                                                        state and then dropped, which subsequently transitions them
   These conditions prove that a representation is unique at
                                                                        to the Free state, which finally returns them to the allocator
the time of instantiation (by using the RepCreator). Then, for
                                                                        to be stored for future use.
its lifetime, it cannot be duplicated or mutated in a way that
would jeopardize its uniqueness.                                        5.3.2 Hybrid Approach to Uphold Uniqueness We use
                                                                        formal verification to uphold the uniqueness guarantee of
5.3   Memory Management                                                 Frames and Pages, and to prove that functions which cast
We use our hybrid approach to uphold the bijective map-                 a pointer lying in the page range of a Pages<Mapped> also
ping invariant of Theseus. Isolation in Theseus without the             uphold uniqueness.
use of hardware address spaces relies upon this invariant al-              For Pages and Frames, we introduce the linear type Chunk
ways being upheld. The invariant can be equivalently restated           that is initially created through the RepCreator. The resource
                                                                    8
Table 2. Code size and verification times for the formally-verified portions we contributed to Theseus. For the PCI crate and ixgbe driver
which contain a large amount of unverified code, we only included the verified functions as part of the implementation size.

                               Intralingual Spec   Prusti Spec   Prusti Proof   Impl   Rust Compilation   Prusti Processing   Verification
                                    (SLOC)                         (SLOC)                                         (s)
      Rust External Spec                0             295             0           0           -                    -               -
      Theseus External Spec             0             14              0          0            -                    -               -
      Representation Creator            0             66              7         392         9.05                18.98           190.74
      Frame Allocator                  13             28              0         151         9.60                 9.04            69.65
      Page Allocator                   13             24              0         142         9.57                 8.70            65.43
      Memory Functions                 15             164             8         1076        41.33               71.29           459.08
      PCI Functions                     3              2              0          36         10.68                5.94            21.83
      ixgbe Driver                     16             41             17         141         16.03               11.91           114.54
      Total                            60             634            32         1938        96.26              125.86           922.27


identifier is a RangeInclusive<usize>. We also formally ver-                   The original Theseus relied on manual checks in place of
ify the methods split() and merge() that create Chunk in-                   formal verification to prove this invariant, as uniqueness is
stance(s) by consuming existing ones. We make its inner field               beyond the scope of intralingual design. In the frame alloca-
private to prevent mutable access outside of its methods, and               tor bookkeeping code, we discovered a bug that led to the
use static assertions to make sure a Chunk instance is only                 instantiation of overlapping Frames instances, violating the
mutably accessible from its verified methods. These joint                   bijective mapping invariant. This bug only manifested in a
properties of Chunk prove that every instance is unique. Both               very particular code path that had not occurred in over four
Frames and Pages are composed of only the Chunk type, for                   years of frame allocator code usage. This bug stalled network
which the static assertion:                                                 driver development for over one person-month, motivating
       assert_fields_type!(Pages: range: Chunk);                            us to explore ways to incorporate formal verification into an
ensures this composition relationship always holds (§4.2).                  intralingual system.
Consequently, Frames and Pages are unique by the Rule of
Composition, ensured by the Rust language — an example of
how the type system can extend formally-verified invariants                 5.4   ixgbe Driver
to other types (§4.1).
   We verify the cast functions to prove that the returned refer-           We implemented the ixgbe driver for the Intel 82599 NIC.
ence is unique. The cast functions consume a Pages<Mapped>,                 Our goal was to write a "correct by construction" driver where
so its uniqueness invariant serves as a pre-condition to the                most bugs could be caught at compile time. We define cor-
functions. To prove uniqueness of the newly created repre-                  rectness properties, then detail how intralingual design and
sentation, we only need to prove that the returned reference                formal verification work together to uphold them. Through
(and the memory we access through it) lies within the given                 a review of previous works [18, 33], we can broadly classify
page range. If there are multiple pointer casts from within the             correctness into three properties.
same page range, we prove that the instances they point to do                  P.1. Datasheet-compliant bit-level communication: When
not overlap. Since we cannot verify unsafe code, we separate                accessing the MMIO registers or data structures, the driver
a casting function into two. The first is verified and returns              must enforce the read/write restrictions for every field. Past
the address of the pointer. The second function is trusted and              work ensures this property either through IDLs [14, 26, 37]
consists of a single line of unsafe code that actually performs             or symbolic execution [33].
the cast. The cast functions are generic and can be used to                    P.2. Creation and management of software resources: The
cast untyped memory to an instance of any “plain old data”                  driver uses data structures, e.g., a ring buffer of packet de-
type following the Rule of Reuse.                                           scriptors, to communicate with the device, and it must map
                                                                            them with the required alignment and length. The underlying
                                                                            memory must be accessible to the driver and device, and be
5.3.3 Proof of Uniqueness: a Bug Revealed The proof of                      returned to the OS when no longer in use.
uniqueness of Pages and Frames greatly increases the strength                  P.3. Valid bookkeeping state: The driver maintains book-
of guarantee of the bijective mapping invariant. The previous               keeping state such as the index of the next descriptor to use,
reasoning behind this invariant was that the map function                   the filter table that stores forwarding rules, etc. The driver pro-
consumes both a Pages<Allocated> and Frames<Allocated>                      vides an interface to the OS to use device functions, and after
instance, assuming both are unique. It then adds PTEs for                   every interface call, the driver must update its bookkeeping
them and returns a Pages<Mapped> instance. This uniqueness                  state to accurately reflect the device state.
property is no longer just an assumption, instead a valid pre-                 We use an intralingual HAL to uphold P.1. and use IRS and
condition to the map function.                                              formal verification to uphold P.2. and P.3..
                                                                        9
5.4.1 Intralingual Design of the ixgbe Driver The ixgbe                  the destination queue of a packet [1], and our use of typestates
driver uses an intralingual HAL to communicate with the                  prevents them.
device. It prevents bugs at the driver↔device interface at
compile time (P.1.), as shown (in part) in Listing 2.                    5.4.2 Hybrid Approach to Correctness Properties We
   We implement an IRS in the driver that shifts some resource           use formal verification to help uphold P.2. and P.3.. The driver
management to the compiler, helping to maintain P.2.. In the             creates multiple representations using verified functions that
initialization code, the driver creates a software representa-           cast untyped memory of a Pages<Mapped> (§5.3.2). For the
tion of each physical NIC (IxgbeNIC), which is composed of               driver to completely uphold P.2., we updated the verification
representations of receive queues (RxQueue), transmit queues             to also prove alignment invariants in addition to uniqueness.
(TxQueue), and device registers. Receive and transmit queues             The alignment and uniqueness properties of the newly cre-
are further composed of descriptor rings, packet buffers, and            ated representations are now type invariants, and we never
queue registers. This compositional relationship is shown in             need to re-verify these properties following the Rule of Type
the ixgbe driver module of Figure 1. The driver creates de-              Preservation.
scriptor rings, packet buffers and registers through a verified             We also formally verify core functions that update book-
interface, so RxQueue and TxQueue representations are unique             keeping state to uphold P.3.. We verify the send_batch and
by the Rule of Composition.                                              receive_batch functions to prove that the value of the next
   We create representations to descriptor rings, packet buffers,        descriptor to use always lies within the descriptor ring. We ver-
and queue registers by using a cast function which takes                 ify the add_filter function to prove that a new filter is added
ownership of a Pages<Mapped> instance and casts an untyped               with the given IP addresses and port numbers, as long as there
pointer within the page range to a Rust reference with the type          is an unused filter slot (the 82599 NIC only offers 128) and
of the representation; the lifetime of the reference is tied to          no existing identical filter. It is the software driver’s responsi-
the Pages<Mapped> instance. In Figure 1, the cast_as function            bility to prevent this logical error. Since we limit verification
consumes Pages<Mapped> instances to create certain represen-             to a few functions in the driver module, we need to make
tations (marked in purple). The driver’s ownership of the                sure that other functions within the module do not break the
Pages<Mapped> instance inherently proves that it has access              verified invariants. For that, we add the #[nomutates] macro
to the represented memory (P.2.). When representations cre-              at the top of unverified functions to ensure they cannot mutate
ated through a cast function are dropped, the Pages<Mapped>              bookkeeping state.
instances they are composed of are also dropped. The drop
handler unmaps the pages and returns them to the OS (P.2.).              6     Evaluation
   IxgbeNIC also owns its PCIDevice representation, so that              We evaluate the performance of the updated memory subsys-
no other entity in the system can access its PCI configuration           tem of Theseus and the ixgbe network driver, and quantify
space once it is initialized. The drop handler for PCIDevice             the verification effort. Our objective is to find any perfor-
returns the representation to the OS so that the NIC can be              mance difference caused by code changes resulting from the
initialized again. With this design, the IxgbeNIC representa-            verification process. We assess the proof effort needed to
tion is unique by the Rule of Composition and its methods                formally verify sections of the memory subsystem and the
are the only way to communicate with the device. With the                network driver to gauge the “lightweightedness” of the hy-
IRS, we can now rely on Rust’s inbuilt rules to prevent any              brid approach, partly by comparing our network driver with
race conditions or illegal accesses to device memory.                    formally verified network drivers reported in the literature,
   We use typestates to prevent the OS from accessing dis-               namely Ironclad [18] and TinyNF [33]. Additionally, we test
abled device features and writing meaningless values to book-            the effectiveness of an intralingual HAL by inserting it as the
keeping state (P.3.). We implement typestates for the RxQueue            hardware interface layer for other Rust ixgbe drivers.
and TxQueue types; both can be in either the Enabled or
Disabled state. In the Disabled state, the send() and receive()          6.1   Performance Comparison
methods are not exposed. In addition, the RxQueue has two
additional states: L3/L4 Filter and RSS, representing two dif-           Setup. All our measurements were collected on an Intel(R)
ferent NIC features: 5-tuple filters and Receive Side Scaling            Xeon(R) Gold 6252N CPU at 2.30 GHz with hyper-threading
(RSS), which are used to distribute incoming packets among               disabled. To measure the Ethernet driver performance, we
receive queues. These features are important enough to merit             employ the RFC2544 benchmarking setup, which involves
their own typestates because as NIC bandwidth increases,                 two machines (a device-under-test and a tester) connected
it can only be fully utilized by employing multiple queues.              by two 10 Gbps links. Each machine has two Intel 82599
Different filter types are also mutually exclusive, and a queue          Ethernet Controllers, with one port per NIC in use. On the
used for RSS must not be used by a 5-tuple filter [4]. These             device-under-test, we run the forwarder on either Theseus (to
misconfiguration errors commonly lead to confusion about                 test our driver) or Ubuntu 18.04 (for the comparison driver).
                                                                         The tester machine runs the MoonGen Packet Generator in
                                                                    10
                                                               Theseus               Verified Theseus
                                                                                                                                               less than the timer period (42 ns). The second microbench-
                                                                                                                                               mark is taken from the original Theseus paper [12], which
                        8000
                                                                                                                                               separately measures the time to map a page, remap it, and then
                                                                                                                                               unmap it, with an increasing number of mappings. Figure 2
                        6000                                                                                                                   shows no significant difference between the two versions.
           Time (ns)




                                                                                                                                               ixgbe Driver. We find that the performance of ixgbe dri-
                        4000
                                                                                                                                               vers written with our hybrid approach is comparable to that
                        2000
                                                                                                                                               of the DPDK ixgbe driver, which does not come with any
                                                                                                                                               correctness guarantee. We test two versions of our driver:
                             0                                                                                                                 ixgbe_hybrid, a standard driver where packet buffers can be
                                   10^2

                                          10^3

                                                 10^4

                                                        10^5



                                                                   10^2

                                                                           10^3

                                                                                  10^4

                                                                                         10^5



                                                                                                 10^2

                                                                                                         10^3

                                                                                                                 10^4

                                                                                                                        10^5
                                                                                                                                               used in any order after receipt, and ixgbe_hybrid(restricted),
                                           (a) Map                        (b) Remap                     (c) Unmap                              which sends packet buffers in the order they are received.
                                                                     Total Mappings
Figure 2. The individual time to map, remap, and unmap a 4 KiB                                                                                 We implement the restricted version because TinyNF [33]
page does not increase when verification is added to Theseus. The                                                                              demonstrated that a driver using the restricted model is sim-
results presented are the mean times for 1 page, with the error bars                                                                           ple enough to be amenable to verification and can also achieve
representing the standard deviation.                                                                                                           maximum throughput. To have a fair comparison we need to
                                                                                                                                               use the same driver model.
                                                                                                                                                  In Figure 3 we show the packet round-trip latency as traffic
                        14                                                                                                                     throughput increases. The last latency measurement is taken
                                          hybrid_theseus
                                          hybrid(restricted)_theseus                                                                           at the maximum throughput that can be handled by the driver.
                        12                safe_rust_ubuntu                                                                                     ixgbe_hybrid achieves a maximum bidirectional throughput
  Median Latency (μs)




                                          tinyNF_ubuntu
                        10                DPDK-23.11.2_ubuntu
                                                                                                                                               of 19 Gbps, only 5% lower than the 20 Gbps achieved by
                                                                                                                                               the DPDK ixgbe driver. DPDK is a highly optimized driver
                         8                                                                                                                     that uses SIMD instructions to process packets in batches
                                                                                                                                               and can maintain a lower round-trip latency per-packet than
                         6
                                                                                                                                               ixgbe_hybrid. ixgbe_hybrid(restricted) can handle the NIC’s
                         4                                                                                                                     maximum throughput of 20Gbps due to fewer operations per
                                 0.0       2.5          5.0       7.5         10.0        12.5   15.0           17.5           20.0            packet. ixgbe_hybrid(restricted), the TinyNF ixgbe driver, and
                                                                 Throughput (Gbps)
                                                                                                                                      ]        the DPDK ixgbe driver all have similar latency profiles as
                                                                                                                                               was reported previously for the restricted driver model by
Figure 3. A performance comparison of ixgbe drivers demonstrates
                                                                                                                                               TinyNF [33].
that the hybrid driver has only 5% lower maximum throughput than
DPDK and has a latency profile similar to other research drivers like
safe_rust [34]. The observed latency spike at 10 Gbps is likely a
hardware issue and has been reported in previous works [33, 34]. In                                                                            6.2   Verification and Implementation Effort
the legend, the OS for each driver is indicated alongside its name.                                                                            Table 2 reports the size (in SLOC) and verification times
The shaded region illustrates the range between the 5th and 95th
                                                                                                                                               for the verified additions to Theseus. We find that the proof
percentiles.
                                                                                                                                               effort is magnitudes lower than end-to-end formally veri-
                                                                                                                                               fied systems, and verification times are within minutes. All
                                                                                                                                               verification times are measured using the Prusti 2023-08-22
a VM with PCI passthrough to the NIC. We first run the
                                                                                                                                               release. We time the verification of each crate individually,
RFC2544 zero packet loss test, used by DPDK [3], to find the
                                                                                                                                               only exporting specifications from dependencies without ver-
maximum bidirectional throughput the driver could handle.
                                                                                                                                               ifying them. To identify where Prusti spends most of its time,
Then, in line with recent works on driver design [33, 34], we
                                                                                                                                               we separately measure the time taken by the Rust compiler,
measure round-trip latency as background traffic increases
                                                                                                                                               the generation of verification conditions by Prusti, and the
from 0 to the maximum throughput in 1 Gbps increments.
                                                                                                                                               runtime for the Viper verification back end.
Memory Subsystem. We find that Theseus with formally-                                                                                             The formally-verified portion of Theseus consists of: (i)
verified code (Verified Theseus) performs similarly to the                                                                                     external specifications for types and functions from the Rust
original Theseus that had no verified code. We run two mem-                                                                                    core library and for select crates in Theseus, (ii) a generic
ory subsystem microbenchmarks. The first microbenchmark                                                                                        representation constructor including verified data structure
is a Rust version of LMBench’s [25] memory map. In this                                                                                        implementations, (iii) portions of the page and frame allocator
benchmark, a 4 KiB page is mapped, written, and unmapped                                                                                       code that include methods to create and modify a Chunk, (iv)
100,000 times. Both versions of Theseus show identical per-                                                                                    definitions of memory related structs and memory functions
formance, a mean time of 1.99 𝜇s with a standard deviation                                                                                     that take a Pages<Mapped> and cast a pointer in its page range,
                                                                                                                                          11
Table 3. Bugs found in the ixgbe drivers from three Rust-based OSes that can be prevented by the intralingual HAL. For some bugs, identical
versions were found in the DPDK driver using symbolic execution [41].

                                                                        Present in Driver                     Intralingual HAL
                     Bug Description                                                                                                     DPDK ID
                                                             ixy [15]        Redox [6]   Redleaf [28]              Solution
 Write to reserved bit of EIMC register                        ✓                              ✓            register access function        23
 Write to reserved bits of DTXMXSZRQ register                  ✓                ✓             ✓            register access function
 RDRXCTL register is not set to default value                  ✓                ✓             ✓            register access function
 Write to FCTRL register without clearing RXCTRL.RXEN          ✓                ✓             ✓         linear type as a proof of work     21


(v) select functions in the PCI crate, and (vi) select ixgbe                      The ixgbe_hybrid(restricted) driver’s HAL is 634 SLOC,
driver functions.                                                              while the hardware model is 1.2k SLOC, though the register
   We next compare the proof effort required for our light-                    map and relevant functions for TinyNF are only 615 SLOC.
weight correctness guarantees to that for stronger correctness                 With the intralingual HAL, we only need to encode the data
guarantees using end-to-end verification, e.g., Ironclad [18],                 sheet information once, within the implementation. Hardware
and symbolic execution, e.g., TinyNF [33].                                     models require double the effort, encoding the same informa-
                                                                               tion in both the model and the driver.
Proof Effort in the Memory Subsystem Compared. The
proof-to-implementation ratio for changes to the memory sub-                   Overhead of Intralingual Spec. We added just 60 lines of
system of Theseus (including the representation creator code)                  intralingual specification to prevent code changes from com-
is 1:117. This is lower than the 10:1 proof-to-implementation                  promising the type-based properties that uphold invariants
ratio of an end-to-end verified page table implementation writ-                for the memory subsystem and the ixgbe driver. The spec-
ten in Rust [13], by more than two orders of magnitude. This                   ification includes preventing the implementation of Clone
minimal proof effort is a direct result of our hybrid approach,                and DerefMut for base representation types and maintaining
and comes at the cost of lower strength of guarantee and a                     the compositional relationship between representations. Any
larger TCB. We only use SMT verification for one property                      struct field updated through formally verified methods is
(uniqueness), and use other techniques to reason about the                     made private, typestate transition methods always consume
correctness of writes to the page table.                                       representations in their previous state, and unverified func-
                                                                               tions that take mutable references are prevented from modi-
Proof Effort for the ixgbe Driver Compared. The verified
                                                                               fying verified values. It is easier to review these 60 lines of
part of the hybrid ixgbe driver has a proof-to-implementation
                                                                               assertions than to search for the properties in the thousands
ratio of 1:8.3, less than the 1:4.8 ratio of the Ironclad apps
                                                                               of lines of code in the memory and ixgbe crates, making our
Intel 82541PI 1 GbE driver [18], the only end-to-end verified
                                                                               hybrid approach more maintainable.
Ethernet driver we could find. The 82541PI is a simpler de-
vice but the driver structure is similar, and we make sure to                  6.3   Bugs Prevented
prove the same invariants for the hybrid driver. A strength of
                                                                               Most techniques from §3 and §4 help write “correct by con-
the hybrid approach is that it significantly reduces the lines
                                                                               struction” code to prevents bugs at implementation time. Nev-
of specification by verifying type invariants once and rely-
                                                                               ertheless, the intralingual HAL is portable and can be used
ing on the type system to carry them forward. Our hybrid
                                                                               to find bugs by retrofitting it into an existing implementation.
method achieves a specification-to-implementation ratio of
                                                                               We inserted the ixgbe intralingual HAL as the driver-hardware
1:3.4, compared to 1:2 for the Ironclad driver. Unlike the Iron-
                                                                               interface in the ixgbe drivers from three other open-source
clad driver, the hybrid driver does not add specification to
                                                                               Rust OSes, namely, Redleaf [28], Redox [6], and ixy [15].
check invariants for the PciDevice, RxQueue, TxQueue types
                                                                               It revealed four previously unreported bugs as detailed in
since they have already been proven in the type constructors.
                                                                               Table 3. Three were present in all the drivers most likely be-
Intralingual HAL vs a Hardware Model. We compare the                           cause the Redleaf and Redox drivers are adapted from ixy.
effort that goes into writing an intralingual HAL with that                    We submitted fixes for these bugs, which have already been
of writing a hardware model and show that they take equiva-                    accepted into the corresponding mainlines.
lent effort to encode the same subset of device behavior. The
TinyNF ixgbe driver itself does not contain any verified func-                 7     Concluding Remarks
tions. Instead, invariants about it are proven by symbolically                 Using the Theseus operating system as an experimental ground,
executing it against a 82599 hardware model. The hardware                      we show that Rust’s type system can be used to provide
model contains assertions about bit-level communication with                   weaker but useful correctness guarantees for system software,
the device. Vigor used the same hardware model to find bugs                    especially when combined with formal verification in a hybrid
in the DPDK ixgbe driver through symbolic execution [41].                      approach. The key is to cleverly exploit the intralingual design
                                                                               patterns described in §3 to expand the reach of guarantees
                                                                        12
from formally-verified code, by using rules and intralingual                           [18] Chris Hawblitzel, Jon Howell, Jacob R Lorch, Arjun Narayan, Bryan
specifications described in §4. Our approach makes previ-                                   Parno, Danfeng Zhang, and Brian Zill. Ironclad apps: End-to-end
ously impossible trade-offs between proof effort, strength of                               security via automated full-system verification. In Proc. USENIX
                                                                                            OSDI, 2014.
guarantee, and size of trust base. In practice, it has already                         [19] Galen C. Hunt and James R. Larus. Singularity: Rethinking the software
prevented and discovered bugs in multiple Rust-based oper-                                  stack. ACM SIGOPS Operating Systems Review, 2007.
ating systems. We hope that sharing our experience with the                            [20] Thomas Bracht Laumann Jespersen, Philip Munksgaard, and Ken Friis
community will help develop it further and present/discover                                 Larsen. Session types for Rust. In Proc ACM SIGPLAN Wrkshp.
bugs in the growing body of Rust software systems.                                          Generic Programming, 2015.
                                                                                       [21] Chinmay Kulkarni, Sara Moore, Mazhar Naqvi, Tian Zhang, Robert
                                                                                            Ricci, and Ryan Stutsman. Splinter:bare-metal extensions for multi-
Acknowledgments                                                                             tenant low-latency storage. In Proc. USENIX OSDI, 2018.
                                                                                       [22] Amit Levy, Bradford Campbell, Branden Ghena, Daniel B Giffin, Pat
This work is supported in part by National Science Foundation
                                                                                            Pannuto, Prabal Dutta, and Philip Levis. Multiprogramming a 64kb
Award # 2416594.                                                                            computer safely and efficiently. In Proc. ACM SOSP, 2017.
                                                                                       [23] Jian Liu, Lin Yi, Weiteng Chen, Chengyu Song, Zhiyun Qian, and
References                                                                                  Qiuping Yi. LinKRID: Vetting imbalance reference counting in linux
                                                                                            kernel with symbolic execution. In Proc. USENIX Security, 2022.
 [1] DPDK bug 399: ixgbe X540 PMD RSS is zero for NFSv3 NULL reply.                    [24] Junjie Mao, Yu Chen, Qixue Xiao, and Yuanchun Shi. RID: finding
     https://bugs.dpdk.org/show_bug.cgi?id=399. Accessed: 2023-03-08.                       reference count bugs with inconsistent path pair checking. In Proc.
 [2] DPDK Ixgbe Bug List. https://bugs.dpdk.org/buglist.cgi?bug_status=                     ACM ASPLOS, 2016.
     __all__&content=ixgbe&no_redirect=1&order=bug_id&product=                         [25] Larry W McVoy, Carl Staelin, et al. lmbench: Portable tools for perfor-
     DPDK&query_format=specific. Accessed: 2023-10-11.                                      mance analysis. In USENIX ATC, 1996.
 [3] Intel       Ethernet’       s       Performance         Report       with         [26] Fabrice Mérillon, Laurent Réveillère, Charles Consel, Renaud Marlet,
     DPDK           23.03.                     https://fast.dpdk.org/doc/perf/              and Gilles Muller. Devil: An IDL for hardware programming. In Proc.
     DPDK_23_03_Intel_NIC_performance_report.pdf.                    Accessed:              USENIX OSDI, 2000.
     2024-10-20.                                                                       [27] Mark Samuel Miller. Robust Composition: Towards a Unified Approach
 [4] Intel® 82599 10 GbE controller datasheet. https://www.intel.com/                       to Access Control and Concurrency Control. PhD thesis, Johns Hopkins
     content/www/us/en/content-details/331520/intel-82599-10-gigabit-                       University, Baltimore, Maryland, USA, May 2006.
     ethernet-controller-datasheet.html. Accessed: 2023-03-14.                         [28] Vikram Narayanan, Tianjiao Huang, David Detweiler, Dan Appel,
 [5] proc_assertions v0.1.1. https://crates.io/crates/proc_assertions. Ac-                  Zhaofeng Li, Gerd Zellweger, and Anton Burtsev. RedLeaf: Isola-
     cessed: 2024-10-20.                                                                    tion and communication in a safe operating system. In Proc. USENIX
 [6] Redox - your next(gen) os. https://www.redox-os.org/. Accessed:                        OSDI, 2020.
     2017-08-11.                                                                       [29] Luke Nelson, James Bornholt, Ronghui Gu, Andrew Baumann, Emina
 [7] Struct std::sync::Arc. https://doc.rust-lang.org/std/sync/struct.Arc.html.             Torlak, and Xi Wang. Scaling symbolic evaluation for automated
     Accessed: 2023-08-02.                                                                  verification of systems code with serval. In Proc. ACM SOSP, 2019.
 [8] Struct std::sync::Mutex.              https://doc.rust-lang.org/std/sync/         [30] Luke Nelson, Helgi Sigurbjarnarson, Kaiyuan Zhang, Dylan Johnson,
     struct.Mutex.html. Accessed: 2023-08-02.                                               James Bornholt, Emina Torlak, and Xi Wang. Hyperkernel: Push-button
 [9] Struct std::vec::Vec. https://doc.rust-lang.org/std/vec/struct.Vec.html.               verification of an os kernel. In Proc. ACM SOSP, 2017.
     Accessed: 2023-08-02.                                                             [31] Aurojit Panda, Sangjin Han, Keon Jang, Melvin Walls, Sylvia Rat-
[10] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J Sum-                 nasamy, and Scott Shenker. NetBricks: Taking the V out of NFV. In
     mers. Leveraging Rust types for modular specification and verification.                Proc. USENIX OSDI, 2016.
     In Proc. ACM OOPSLA, 2019.
                                                                                       [32] Benjamin C Pierce. Advanced topics in types and programming lan-
[11] Abhiram Balasubramanian, Marek S. Baranowski, Anton Burtsev, Au-                       guages, chapter 1. MIT press, 2004.
     rojit Panda, Zvonimir Rakamarić, and Leonid Ryzhyk. System pro-                  [33] Solal Pirelli and George Candea. A simpler and faster NIC driver model
     gramming in Rust: Beyond safety. In Proc. Workshp. Hot Topics in                       for network functions. In Proc. USENIX OSDI, 2020.
     Operating Systems (HotOS), 2017.                                                  [34] Solal Pirelli and George Candea. Safe low-level code without overhead
[12] Kevin Boos, Namitha Liyanage, Ramla Ijaz, and Lin Zhong. Theseus:                      is practical. In ICSE, 2023.
     an experiment in operating system structure and state management. In              [35] Helgi Sigurbjarnarson, James Bornholt, Emina Torlak, and Xi Wang.
     Proc. USENIX OSDI, November 2020.                                                      Push-Button verification of file systems via crash refinement. In Proc.
[13] Matthias Brun, Reto Achermann, Tej Chajed, Jon Howell, Gerd Zell-                      USENIX OSDI, 2016.
     weger, and Andrea Lattuada. Beyond isolation: OS verification as a                [36] Helgi Sigurbjarnarson, Luke Nelson, Bruno Castro-Karney, James Born-
     foundation for correct applications. In Proc. Workshp. Hot Topics in                   holt, Emina Torlak, and Xi Wang. Nickel: A framework for design
     Operating Systems (HotOS), 2023.                                                       and verification of information flow control systems. In Proc. USENIX
[14] Christopher L Conway and Stephen A Edwards. NDL: a domain-                             OSDI, 2018.
     specific language for device drivers. In ACM Sigplan Notices, 2004.               [37] Jun Sun, Wanghong Yuan, Mahesh Kallahalla, and Nayeem Islam. Hail:
[15] Paul Emmerich, Maximilian Pudelko, Simon Bauer, and Georg Carle.                       a language for easy and correct device access. In Proceedings of the
     User space network drivers. In Proceedings of the Applied Networking                   5th ACM international conference on Embedded software, 2005.
     Research Workshop, 2018.                                                          [38] Thorsten Von Eicken, Chi-Chao Chang, Grzegorz Czajkowski, Chris
[16] Manuel Fahndrich and Robert DeLine. Adoption and focus: Practical                      Hawblitzel, Deyu Hu, and Dan Spoonhower. J-Kernel: A capability-
     linear types for imperative programming. In PLDI, 2002.                                based operating system for Java. Secure Internet programming, 1999.
[17] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan Newman Wu, Jieung                      [39] Chao Xu, Xiaozhu Lin, Yuyang Wang, and Lin Zhong. Automated
     Kim, Vilhelm Sjöberg, and David Costanzo. CertiKOS: An extensible                      OS-level device runtime power management. In Proc. ACM ASPLOS,
     architecture for building certified concurrent OS kernels. In Proc.                    2015.
     USENIX OSDI, 2016.
                                                                                  13
[40] Jean Yang and Chris Hawblitzel. Safe to the last instruction: automated        A    Classification of DPDK Ixgbe Driver Bugs
     verification of a type-safe operating system. In PLDI, 2010.
[41] Arseniy Zaostrovnykh, Solal Pirelli, Rishabh Iyer, Matteo Rizzo, Luis
                                                                                    In Table 4 we detail DPDK ixgbe bugs [2] and the technique
     Pedrosa, Katerina Argyraki, and George Candea. Verifying software              that can be used to prevent them. At the time of compiling this
     network functions with no verification expertise. In Proc. ACM SOSP,           list, there were 93 reported bugs which referenced the ixgbe
     2019.                                                                          driver. Of those 93, 29 were actually related to the driver. The
                                                                                    remaining bugs were either invalid, or concerned with other
                                                                                    parts of the DPDK framework and not the driver specifically.
                                                                                    A condensed version of this table is given in the paper.




                                                                               14
Bug ID                                                  Notes                                                       Resolution
  21     "Ixgbe driver changes FCTRL without first disabling RXCTRL.RXEN"                                  Intralingual HAL
  22     "Ixgbe driver sets RDRXCTL with the wrong RSCACKC and FCOE_WRFIX values"                          Intralingual HAL
  23     "Ixgbe driver writes to reserved bit in the EIMC register"                                        Intralingual HAL
  25     "Ixgbe driver sets TDH register after TXDCTL.ENABLE is set"                                       Intralingual HAL
  26     "Ixgbe driver does not ensure FWSM firmware mode is valid before using it"                        Intralingual HAL
  57     Null pointer de-reference                                                                         Basic Rust
  69     Maximum wait time for link to come up was too small                                               Formal verification
 103     Deadlock during initialization                                                                    Formal verification
         Segmentation fault when in-use rx queues are freed.
 116                                                                                                       Intralingual representations
         This can be prevented by an IRS.
 216     Burst size should be >= 4 to use a vectorized function                                            Formal verification
 263     "ixgbe does not support 10GBASE-T copper SFP+"                                                    Hardware issue
 350     "ixgbe: incorrect speed capabilities advertised for X553 devices"                                 Formal verification
 372     Driver needs to separately handle different error cases.                                          Formal verification
 388     "ixgbe: link state race condition can occur when starting a fiber port"                           Basic Rust
         Filtering and RSS are enabled at the same time, leading to confusing results.
 399                                                                                                       Intralingual representations
         Typestates would prevent enabling both features simultaneously.
 447     Resource cleanup always occurs with representation drop handlers                                  Intralingual representations
 514     Runtime flag check does not check for IPv6 flag                                                   Formal verification
 516     Vectorized functions should receive the specified number of packets, but always receive 32        Formal verification
 629     Device marks checksum as invalid.                                                                 Hardware issue
         Rx queue was initialized even though failed to allocate packet buffers.
 643     With an IRS, it would be impossible to create an rx queue unless packet buffers                   Intralingual representations
         are created and then owned by it.
  650    Improvements to prevent packet loss                                                               Formal verification
  664    Reta table can be set before the device is started. Typestates would prevent this.                Intralingual representations
  869    Use after free                                                                                    Basic Rust
  882    Bug in receive function lets application use packet buffer that is still in descriptors           Formal verification
 1034    Enabled IPv4 checksum offload even though device doesn’t support it.                              Formal verification
         A single API to set flow rules for different drivers, leads to setting invalid flow rules
 1057                                                                                                      Basic Rust
         for some devices. Strongly typed interfaces which prevent invalid arguments would prevent this.
 1106    Missing OR operator                                                                               Formal verification
 1249    Missing NEGATION operator                                                                         Formal verification
         Port is restarted without restarting queues.
 1259                                                                                                      Intralingual representations
         Typestates for representations would prevent this.
                                                    Table 4. List of DPDK ixgbe bugs




                                                                 15
