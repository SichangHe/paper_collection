                                        UnsafeChecker: Finding Soundness Bugs in Rust Safe
                                        Abstractions
                                        XIZHE YIN∗ , Nanjing University, China
                                        YAOKUN ZHANG∗ , Nanjing University, China
                                        YANG FENG† , Nanjing University, China
                                        BAOWEN XU, Nanjing University, China
                                        Rust guarantees memory safety without garbage collection through a strict ownership and borrowing system.
arXiv:2609.09641v1 [cs.PL] 9 Sep 2026




                                        However, for low-level systems programming, many widely used libraries rely on the unsafe keyword. These
                                        libraries encapsulate raw-pointer operations behind safe APIs to form safe abstractions. A single mistake in
                                        this internal unsafe code can break its safety contract, rendering the abstraction unsound and allowing safe
                                        clients to trigger undefined behavior. Detecting these potential soundness violations is challenging. Existing
                                        static analysis tools for C/C++ ignore Rust-specific safety contracts, while current Rust tools lack the deep
                                        semantic modeling required to track the contexts that raw pointers erase.
                                           To address this gap, we present UnsafeChecker, a compiler-integrated static analysis framework for de-
                                        tecting potential soundness violations in Rust safe abstractions. UnsafeChecker analyzes Rust MIR using a
                                        flow-sensitive abstract interpretation that maintains a shared state with three components: ownership, ob-
                                        ject validity, and layout. Each warning rule consumes the subset of facts needed for the corresponding Rust
                                        safety obligation. UnsafeChecker reports both instruction-level undefined behavior and boundary-level con-
                                        tract violations that may escape through safe APIs. We evaluate UnsafeChecker on a benchmark of 46 Rust-
                                        Sec vulnerabilities, which contain 53 ground-truth bugs. UnsafeChecker outperforms several state-of-the-art
                                        tools, detecting 32 CVEs and covering 36 bugs (67.9% recall) with 51.6% alert-level precision. Furthermore,
                                        in a large-scale scan of real-world crates on crates.io, UnsafeChecker uncovered 114 previously unknown
                                        bugs across 83 crates, with 45 confirmed and 27 already fixed by maintainers.
                                        Additional Key Words and Phrases: Rust, Static Analysis, Memory Safety, Unsafe Code, Abstract Interpreta-
                                        tion

                                        1 Introduction
                                        Rust has become popular in systems programming, adopted by major projects such as Android
                                        and the Linux kernel [19, 21, 28]. A key reason for this popularity is that Rust guarantees memory
                                        safety without garbage collection. This makes it an ideal choice for building low-level systems that
                                        demand both high performance and strict safety. To achieve this, Rust relies on a strict ownership
                                        and borrowing system. For safe references, the compiler statically tracks their semantic context—
                                        specifically ownership relations, lifetimes, and type layouts —to enforce critical safety invariants.
                                        This ensures that every value has a unique owner, no reference outlives its data, and memory
                                        accesses are strictly bounded. As long as code remains within the safe subset of the language (Safe
                                        Rust), the compiler guarantees that these invariants hold, ensuring memory safety [24, 26].
                                          However, the strict ownership model can be too restrictive for low-level tasks, such as direct
                                        hardware manipulation and high-performance data structures. To support this, Rust provides the
                                        unsafe keyword, which relaxes compiler checks and permits the use of raw pointers [24]. Raw
                                        pointers behave as plain addresses and do not carry the ownership, lifetime, or layout guarantees
                                        that Safe Rust relies on. As a result, the compiler cannot statically enforce these safety invariants
                                        ∗
                                            Both authors contributed equally to this research.
                                        †
                                            Yang Feng is the corresponding author.

                                        Authors’ Contact Information: Xizhe Yin, xizheyin@smail.nju.edu.cn, Nanjing University, Nanjing, Jiangsu, China; Yaokun
                                        Zhang, yaokunzhang@smail.nju.edu.cn, Nanjing University, Nanjing, Jiangsu, China; Yang Feng, Nanjing University, Nan-
                                        jing, China, fengyang@nju.edu.cn; Baowen Xu, Nanjing University, Nanjing, China, bwxu@nju.edu.cn.
2                                                       Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


for them. In practice, library developers encapsulate unsafe blocks behind safe APIs, forming safe
abstractions. For example, the standard library implements types such as Vec and Mutex with un-
safe code, but exposes safe interfaces. This design relies on a critical contract: the internal unsafe
code must manually uphold the same safety invariants mandated by Safe Rust. If this contract is
broken, the abstraction is unsound, allowing safe client code to trigger undefined behavior [3, 25].
Because the compiler does not validate these conditions inside unsafe blocks, a single implemen-
tation error can compromise the safety of the entire library [28]. This gap motivates automated
analyses for detecting potential soundness violations in safe abstractions.
   Existing approaches fall short because they prioritize execution errors over whether unsafe code
upholds the contract relied on by safe APIs. Tools designed for C and C++ operate on a flat memory
model. They check for invalid memory accesses (e.g., buffer overflows) but ignore Rust’s safety con-
tracts. They also lack a language-level definition of the safety invariants that Safe Rust enforces.
In Rust, these invariants are part of the soundness contract of safe abstractions [26]. For exam-
ple, duplicating a raw pointer is valid in C. In Rust, however, if that pointer represents a unique
resource (e.g., Box<T>), duplicating it violates ownership uniqueness. Since C/C++ tools do not
model ownership semantics, they cannot detect such contract violations. Similarly, existing Rust
tools often rely on syntactic pattern matching or general memory safety checks. While effective
for specific bug classes, they lack the deep semantic modeling required to check that an abstraction
maintains its safety invariants. They do not track the semantic context—ownership, lifecycle, and
layout—that the compiler erases in unsafe blocks. Consequently, they cannot reliably check that
an unsafe implementation preserves the invariants required by its safe API.
   To detect potential soundness violations in safe abstractions, we design UnsafeChecker, a three-
component static analysis framework for Rust. UnsafeChecker targets bugs where unsafe
pointer operations violate the safety obligations that safe clients rely on. It analyzes Rust MIR
by tracking three kinds of facts: ownership, object validity, and layout (Section 3). Specifically,
the ownership component captures aliasing and resource uniqueness; the object-validity compo-
nent tracks states such as live, moved, dropped, or uninitialized; and the layout component mod-
els pointer bounds, alignment, mutability, and offsets. These facts are maintained in one shared
flow-sensitive state. Some checks are domain-local, such as layout-centered bounds checks, while
others combine facts across components through shared object and pointer identities. The anal-
ysis is flow-sensitive. It propagates this composite state along the CFG until reaching a fixpoint.
UnsafeChecker then checks instruction-level UB (e.g., out-of-bounds and invalid dereference) and
boundary-level violations that can escape through safe APIs (e.g., returning a dangling pointer).
   The contributions of this paper can be summarized as follows:
• Framework: We propose a MIR-level static analysis that maintains ownership, object-validity,
  and layout facts in a shared flow-sensitive state. This design supports both domain-local checks,
  such as spatial layout violations, and composite checks, such as dangling pointers and double
  frees that require ownership and validity facts.
• Tool: We implemented UnsafeChecker as a compiler plugin. It analyzes Rust MIR efficiently and
  fits into existing build pipelines.
• Study: We evaluated UnsafeChecker on a benchmark of 46 RustSec vulnerabilities (comprising
  53 ground-truth bugs). The results show that UnsafeChecker detects 32 vulnerabilities (69.6%
  recall) and covers 36 bugs (67.9% recall), with an alert-level precision of 51.6%, outperforming
  several state-of-the-art tools [4, 7, 16]. Furthermore, when applied to a large-scale scan of real-
  world Rust crates, UnsafeChecker uncovered 114 previously unknown bugs across 83 crates.
  Among these, developers have confirmed 45 as genuine vulnerabilities, and 27 have already
  been fixed.
    UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                       3


    2 Background and Motivating Examples
    This section motivates our analysis goal and the semantic gaps introduced by unsafe. We first
    define soundness for safe abstractions and the safety invariants that Safe Rust enforces. We then
    walk through three real-world bugs from our evaluation to show how unsafe implementations
    violate these invariants. These examples motivate tracking three kinds of semantic context that
    raw pointers erase.

    2.1    Background: Soundness and Semantic Gaps
    In Rust, a safe abstraction is a public API that exposes a safe interface while internally using unsafe
    code. It acts as a contract: as long as the API is used from Safe Rust, the abstraction guarantees that
    no undefined behavior (UB) occurs. Because the compiler does not validate safety requirements
    inside unsafe, this contract depends on the developer upholding Rust’s safety invariants in the
    implementation. If the implementation violates these invariants, the abstraction becomes unsound
    and safe client code may trigger UB [24, 26].
       A soundness violation means that a safe abstraction fails to uphold this safety contract. The Rust
    Reference defines soundness as follows [26]:
             “Unsafe code that satisfies this property for any safe client is called sound; if unsafe
             code can be misused by safe code to exhibit undefined behavior, it is unsound.”
    This means that there exists a safe usage of the API that can lead to undefined behavior (UB).
    Unsoundness can manifest in two ways. First, the unsafe implementation may directly execute an
    instruction-level UB (e.g., invalid dereference, out-of-bounds access, or use of uninitialized memory)
    under safe inputs. Second, the API may return or leak an invalid state to safe code (e.g., a dangling
    pointer or duplicated ownership), so that UB may occur later in the caller, even if the callee itself
    does not crash. We refer to the conditions that safe code relies on— such as aliasing, validity, and
    layout requirements—as safety invariants. Ensuring soundness requires checking whether unsafe
    code maintains these invariants, not just detecting crashes.
       Safe Rust establishes these safety invariants through three core mechanisms: (1) unique own-
    ership, which ensures resources have a single owner to prevent double-free; (2) borrowing rules,
    which ensure references do not outlive the data they refer to, preventing dangling pointers; and
    (3) memory layout, which ensures pointers are aligned and within bounds. In this work, we cate-
    gorize the corresponding safety invariants into three dimensions: ownership, lifecycle, and layout.
    Within unsafe blocks, the compiler no longer enforces these rules, so an analysis must check them
    to reason about soundness.

    2.2    Motivating Examples
    We now illustrate how soundness violations manifest in real-world code, using bugs detected in
    our evaluation (Section 5).

    Listing 1 Soundness violation via ptr::read in remoteprocess
1 pub trait ProcessMemory {
2         fn copy_struct<T>(&self, addr: usize) -> Result<T, Error> {
3             let mut data = vec![0; std::mem::size_of::<T>()];
4             self.read(addr, &mut data)?;
5             Ok(unsafe { std::ptr::read(data.as_ptr() as *const T) })
6         }
7}
     4                                                      Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


     Example A. Listing 1 shows a soundness violation in the remoteprocess crate. The function
     copy_struct, provided by the ProcessMemory trait, is a safe abstraction that claims to safely
     read a struct T from a target process. It encapsulates low-level memory manipulation within an
     unsafe block. The function (1) allocates a local byte buffer (data); (2) fills it with raw bytes from
     the target; and (3) uses ptr::read to bitwise copy the buffer into a value of type T.
        This implementation is unsound for two reasons. First, it violates memory layout requirements,
     specifically pointer alignment. In Rust, Vec<u8> provides only 1-byte alignment for its buffer. If
     the generic type T requires stricter alignment (e.g., 8 bytes for u64), casting *const u8 to *const
     T yields a pointer that is not guaranteed to be properly aligned. Using ptr::read through such
     a pointer is undefined behavior. Second, it violates the unique ownership guarantee. Rust marks
     types safe for bitwise duplication as Copy (e.g., i32). Non-Copy types, however, often own heap
     allocations (e.g., String). Bitwise copying such types duplicates their internal pointers, causing
     two values to own the same resource. Without a Copy bound on T, ptr::read creates a second
     owner. This results in a double-free error when both the returned object and the original resource
     go out of scope and attempt to deallocate the same memory.
     use remoteprocess::{LocalProcess, ProcessMemory};
     #[derive(Debug)]
     struct Victim(String);
     fn main() {
         let victim = Victim("Hello from heap".to_string());
         let _copy: Victim = LocalProcess.copy_struct(&victim as *const _ as usize).unwrap();
     }
        A single safe client can trigger both issues. The Proof-of-Concept (PoC) above calls copy_struct
     on a non-Copy type. It triggers UB in two ways. First, ptr::read::<Victim> reads from a Vec<u8>
     buffer that may not satisfy Victim’s alignment. Second, since Victim is non-Copy and owns a
     String, the bitwise copy duplicates the owning pointer. Dropping the value causes a double free.
     This demonstrates that detecting unsoundness requires more than local crash checks; it necessi-
     tates tracking layout constraints and ownership relations.
     Listing 2 Dangling pointer due to ptr::read in iterator
 1 impl<V> Iterator for Keys<V> {
 2       fn next(&mut self) -> Option<usize> {
 3           while self.pos < self.max {
 4               let opt = unsafe { ptr::read(self.head.add(self.pos)) };
 5               if opt.is_some() {
 6                   self.pos += 1;
 7                   return Some(self.pos - 1);
 8               }
 9               self.pos += 1;
10           }
11           None
12       }
13 }



     Example B. Listing 2 shows a violation in the emap crate. The iterator’s next method returns
     a key from the map by using unsafe ptr::read to copy bytes from the internal buffer (line 4).
     As shown in the PoC below, after m.keys().next() returns, the map m still considers the slot
     occupied. Accessing it via m.get(0) triggers a use-after-free.
     let mut m: Map<String> = Map::with_capacity_none(1);
     m.insert(0, String::from("hello"));
     let _ = m.keys().next();   // ptr::read copies bytes; dropping m[0] in next()
     let s = m.get(0).unwrap(); // returns dangling reference -- UAF!
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                         5


    As an implementation of the Iterator trait, this method acts as a safe abstraction. The problem
is that ptr::read creates a bitwise copy of the value (e.g., String) from the buffer into a temporary
variable opt. Since the function returns Option<usize> and not the value itself, opt is dropped at
the end of the scope. This drop frees the underlying heap memory (e.g., the string buffer). However,
the map does not update its state to mark the slot as empty, so it retains a pointer to the now-freed
memory. The compiler cannot enforce this logical state update through raw pointers inside unsafe.
This violation leaves the map in an inconsistent state: subsequent access (e.g., via get) triggers a
use-after-free (UAF), and dropping the map causes a double free.
    The key observation is that ptr::read duplicates ownership into a temporary variable, which is
dropped at the end of the scope. When this temporary variable is dropped, it invalidates the resource
held by the map. By tracking the ownership relation and memory liveness state of opt, we
can detect the dangling pointer.

2.3   Key Insight: Tracking Lost Semantics to Check Safety Invariants
To detect these soundness violations, we must track the semantic information erased by unsafe to
check safety invariants. Our key insight is that soundness relies on maintaining invariants across
three interconnected dimensions: ownership, lifecycle, and layout. Standard value-based dataflow
analysis is insufficient as it treats pointers as simple values. While it propagates memory addresses,
it fails to record ownership, liveness, or layout constraints. Consequently, it cannot explain why
ptr::read in Listing 1 duplicates ownership, or why the map in Listing 2 returns a reference to
freed memory.
   To address this, we track these semantics via a flow-sensitive abstract state. This state records
aliasing, ownership relations, lifecycle states, and layout attributes. We propagate this state along
the control flow graph (CFG), merging states at join points to conservatively over-approximate all
execution paths. Crucially, these dimensions interact. For example, dropping an owner invalidates
all aliases to the underlying resource.
   Figure 1 illustrates this using List-
ing 1. The figure distinguishes owner
nodes from non-owning alias views:
data(o0) and ret(o3) are owning
values, whereas the pointer-derived
view o1 records an alias to the un- Fig. 1. Ownership duplication in Listing 1. Solid ownership edges
derlying buffer rather than owner- identify owners; alias edges connect non-owning pointer views to
ship by itself. The event order is: first, the underlying resource.
data(o0) owns the heap buffer data.buf(o2); second, self.read links the raw pointer view o1
to that buffer; third, ptr::read creates the returned owner ret(o3) from the same resource. The
ptr::read operation therefore creates a second owning view of the heap resource. Let o0 denote
the stack object data (Vec<u8>), and o2 its heap buffer. o0 owns o2 . The memory at addr is denoted
as o1 . self.read makes o2 an alias of o1 . Then, ptr::read creates a new object o3 from o2 . Our
analysis tracks that o3 aliases o2 , and by transitivity, o1 . Thus, o1 , o2 , and o3 form an owning alias
set. We report an alarm when this set contains two distinct Live non-Copy owners (o1 and o3 ),
which violates the unique ownership invariant.

3 Approach
In this section, we present UnsafeChecker, a flow-sensitive dataflow analysis for detecting poten-
tial soundness violations in Rust safe abstractions. As discussed in §2, once code enters unsafe,
raw pointers may erase semantic context that Safe Rust relies on. UnsafeChecker tracks this con-
text with three components: ownership, object validity, and layout. The components are stored in
6                                                           Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu




Fig. 2. Overview of UnsafeChecker’s workflow. UnsafeChecker compiles a crate to MIR, constructs a shared
abstract state Σ with ownership, object-validity, and layout facts, and iteratively applies transfer functions
to a fixpoint while checking instruction-level UB and boundary-level contract violations.


one shared abstract state, but individual transfer and warning rules update or consume only the
facts relevant to the modeled MIR operation.


3.1   Overview
Figure 2 illustrates the overall workflow of UnsafeChecker. Given a Rust crate, UnsafeChecker
first compiles it to MIR (Rust’s Mid-level Intermediate Representation) using the Rust compiler,
rustc. It then abstracts MIR places into three kinds of locations: stack owners (𝒮𝒪), pointer loca-
tions (𝒫), and Copy data (𝒱𝑐𝑜𝑝𝑦 ). Based on this abstraction, UnsafeChecker runs a flow-sensitive
dataflow analysis on each function’s CFG. The analysis iteratively applies transfer functions to
propagate a shared abstract state Σ until reaching a fixpoint. Σ stores ownership, object-validity,
and layout facts, which capture the semantic context that raw pointers may erase. During propa-
gation, UnsafeChecker performs instruction-level execution checks to report undefined behavior
(e.g., Use-After-Free and Out-of-Bounds). At function boundaries, it additionally checks API-level
contract violations that can affect safe clients, such as returning dangling pointers or duplicating
ownership.

    Scope of Analysis. Our goal is to detect potential unsoundness in Rust safe abstractions: whether
a safe API can lead to undefined behavior when invoked from safe code. Accordingly, we focus on
undefined behavior (UB) and contract violations that arise from unsafe pointer operations and that
can compromise memory safety guarantees for safe clients. According to the Rust Reference [26],
we target the following UB categories relevant to memory safety: [pointer-access], [place-
projection], [alias], [immutable], and the pointer- and allocation-related parts of [invalid].
We also detect resource leaks, which are a critical error for many safe abstractions. The corre-
sponding checks consume the subset of ownership, object-validity, and layout facts needed by
each modeled Rust obligation. In addition, we implement three lightweight auxiliary checks used
in our evaluation (Section 5). First, we flag integer overflow in index and size computations, since
wrap-around can invalidate subsequent bounds reasoning. Second, we flag division-by-zero, since
it triggers panics and can invalidate control-flow assumptions. Third, we flag invalid UTF-8 passed
to unsafe string constructors (e.g., str::from_utf8_unchecked), since it violates the documented
safety precondition of these APIs and can invalidate subsequent reasoning about string operations.
We exclude [race], [intrinsic], [target-feature], [call], [asm], [runtime], and other Ref-
erence items that fall outside our scope. This is a scoped bug-finding claim rather than a theorem of
full Rust semantic soundness. The claim is limited to the MIR operations, library/API models, and
memory-safety categories covered by UnsafeChecker. It does not cover concurrency or data races,
unavailable or opaque callees, unmodeled library behavior, inline-depth cutoffs, FFI behavior, or
pointer-integer-pointer round trips where object identity or provenance is lost.
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                        7


3.2   Variable Abstraction
We model memory with abstract locations and abstract heap objects. An abstract location
ℓ ∈ ℒ represents a MIR place. In Rust’s MIR, a place is a path to a memory location, such as a local
variable x, a field projection x.f, or a dereference *p. To support precise field-sensitive analysis,
we treat field projections (e.g., x.f) as distinct abstract locations from their parents (x). This allows
us to track partial ownership and independent borrows of disjoint fields. However, we do not track
dereferences *p as base locations; instead, they are resolved to the abstract objects pointed to by
p using the points-to relation.
   We partition ℒ into three disjoint subsets: stack owners (𝒮𝒪), pointer locations (𝒫), and Copy
data locations (𝒱𝑐𝑜𝑝𝑦 ). We also track a set of abstract heap objects ℋ𝒪 that represent dynamic
allocations.
      • 𝒮𝒪 ⊆ ℒ: stack owners. Locations of non-Copy types (e.g., Vec, Box) that act as roots of
         ownership. They reside on the stack and may manage heap resources.
      • 𝒫 ⊆ ℒ: pointer locations. Locations holding references or raw pointers (e.g., *mut T, &T).
         They access objects indirectly without owning them. We include raw pointers in 𝒫 (even
         though they are Copy) to track aliasing precisely.
      • 𝒱𝑐𝑜𝑝𝑦 ⊆ ℒ: Copy data locations. Other Copy locals (e.g., usize, bool). The layout domain
         uses these values for arithmetic reasoning.
   For heap allocations, we use an allocation-site abstraction. All allocations from the same MIR
instruction map to one canonical heap object ℎ𝑙𝑜𝑐 ∈ ℋ𝒪. Note that ℋ𝒪 ∩ ℒ = ∅. We unify all
resources whose lifecycle must be tracked by defining ownership nodes as 𝒪 = 𝒮𝒪 ∪ ℋ𝒪. This
set includes both stack owners and heap objects.
   For a composite ownership root 𝑣 ∈ 𝒮𝒪 that encapsulates an internal pointer used for memory
access (e.g., a Vec’s buffer pointer), we denote the corresponding pointer location (an access path
in ℒ) by 𝑝𝑣 ∈ 𝒫.
   To illustrate, consider the Vec<T> variable data in Listing 1. The variable data resides on the
stack (data ∈ 𝒮𝒪) and manages a dynamically allocated buffer (data.buf ∈ ℋ𝒪). In Safe Rust,
the ownership model ensures that when data goes out of scope, it automatically deallocates
data.buf. Unsafe Rust, however, allows pointers (𝒫) to bypass these checks, potentially intro-
ducing aliasing, invalid lifecycle states, or out-of-bounds access. Based on the variable abstraction
above, UnsafeChecker tracks these risks through three components, as detailed next.

3.3   Ownership Domain (𝜎𝐴 )
To detect memory safety violations in unsafe code, UnsafeChecker tracks the ownership topol-
ogy that is typically erased during compilation. The ownership domain 𝒟𝑂𝑤𝑛 approximates the
relational structure of the heap by tracking three key relations: ⟨Pt, Own, Alias⟩.
• Points-to Relation (Pt ∶ 𝒫 ⇀ ℘(𝒪)). A standard may-points-to map that links each pointer
  location 𝑝 to the set of objects it may reference. This relation resolves indirect accesses: derefer-
  encing 𝑝 is treated as an access to all 𝑜 ∈ Pt(𝑝). At control-flow joins, points-to sets are merged
  by union, so Pt(𝑝) accumulates possible targets from all incoming paths.
• Ownership Hierarchy (Own ∶ 𝒪 → ℘(ℋ𝒪)). Tracks the vertical management of resources.
  For an object 𝑜 , Own(𝑜) is the set of heap resources for which 𝑜 is currently responsible. This
  explicitly represents the RAII structure (e.g., a Vec owning its buffer), allowing the analysis to
  determine which resources are affected when an object is dropped.
• Ownership Aliasing (Alias ∶ 𝒪 → ℘(𝒪)). Tracks the horizontal aliasing between owners.
  Alias(𝑜) is the set of objects that claim ownership of the same underlying resource as 𝑜 . While
  Safe Rust enforces unique ownership (|Alias(𝑜)| = 1), unsafe code can introduce duplication (e.g.,
8                                                          Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


  via ptr::read). We track these sets to detect when multiple objects believe they own the same
  resource, which is the structural precursor to double-free bugs.
   The domain forms a lattice ordered by component-wise subset inclusion (⊑). The join operation
(⊔) computes the component-wise set union, yielding a conservative may-approximation for the
modeled ownership facts. For the aliasing component, the union accumulates ownership claims
from all incoming control-flow paths: Alias⊔ (𝑜) = Alias1 (𝑜) ∪ Alias2 (𝑜). This ensures that if an
ownership duplication exists on any path, it is preserved and checked in the subsequent analysis.

3.4   Object-Validity (Lifecycle) Domain
The second dimension of our analysis is the object-validity domain 𝒟𝐿𝑖𝑓 𝑒 , which tracks the
runtime validity of memory objects. While Safe Rust relies on static lifetimes to prevent use-after-
free, unsafe code bypasses these checks, necessitating a flow-sensitive model of object states. We
retain the term lifecycle only to denote these runtime object states (e.g., Live, Moved, and Dropped),
distinct from Rust’s compile-time lifetime system. We define the lifecycle state 𝜎𝑂 ∶ 𝒪 → ℘(Σ𝑎𝑡𝑜𝑚 )
as a mapping from each object to a set of possible atomic states. Elements of 𝒟𝐿𝑖𝑓 𝑒 are such maps.
   We model the lifecycle of a Rust object using a finite set of mutually exclusive atomic states Σ𝑎𝑡𝑜𝑚 .
The base state is Live, representing a fully initialized and valid object. Memory that is allocated
but not yet initialized is tracked as Uninit; reading from it is undefined behavior. When owner-
ship is transferred, the object enters the Moved state, and subsequent access is a Use-After-Move
error. Once a destructor runs, the object becomes Dropped, and the pointer to it is no longer valid,
leading to a dangling pointer. Any access to this pointer constitutes a Use-After-Free error. Special
handling is required for manual management: ManuallyDropped indicates an object (e.g., wrapped
in ManuallyDrop) that remains valid but whose automatic destructor is suppressed. Finally, For-
gotten represents an object explicitly consumed (e.g., via mem::forget); it is semantically moved,
and its resources are leaked rather than freed.
   To handle control-flow uncertainty (e.g., a variable is dropped in one branch but not another),
we construct the domain as a power set lattice 𝒮 = ℘(Σ𝑎𝑡𝑜𝑚 ). In this lattice, an abstract state 𝑆 ∈ 𝒮
represents the disjunction of all possible runtime states, ordered by set inclusion (⊆). At control-
flow merge points, the join operation (⊔) is defined as set union (∪), which yields a conservative
may-approximation for the modeled object-validity facts. For example, if a variable is initialized on
one path and moved on another, its state at the merge point is exactly {Live, Moved}. This power-
set design is necessary for precise error reporting. Rather than collapsing to a generic “Unknown”
state, UnsafeChecker retains the specific set of possible states. This supports conditional reports
(e.g., “Potential Use-After-Free on some paths”).

3.5   Layout Domain
The third component of our analysis is the layout domain 𝒟𝐿𝑎𝑦 , which models the physical prop-
erties of pointers relative to their underlying memory allocations. The layout domain complements
the qualitative reasoning of ownership domain and lifecycle domain by maintaining byte-level pre-
cision for pointer bounds, alignment, and mutability. This enables checks for array indexing and
pointer arithmetic.
   For a pointer 𝑝 , the layout domain tracks its abstract state 𝜎𝐿 (𝑝) as a tuple:
                              𝜎𝐿 (𝑝) = (base, size, offset, align, null, mut)
Formally, 𝜎𝐿 is a map from pointer locations to such tuples. Here, base denotes the target memory
block (heap, stack, or ⊤), while size represents the minimum guaranteed buffer capacity. The offset
interval [𝑙, 𝑢] tracks the pointer’s position relative to the base, and align records the alignment
guarantee. Finally, null and mut capture the pointer’s nullability and mutability.
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                                 9


  We use an explicit invalid-pointer element as the bottom state of the layout domain:
                                 ⊥Lay = (⊥, 0, ⊥, 1, MaybeNull, Unknown)
   We define the partial order ⊑Lay so that larger elements represent weaker safety guarantees.
Specifically, a state 𝑠2 is considered less precise than 𝑠1 (𝑠1 ⊑Lay 𝑠2 ) if it provides a smaller guaran-
teed buffer size (𝑧1 ≥ 𝑧2 ), a smaller alignment (𝑎1 ≥ 𝑎2 ), or a wider offset interval ([𝑙1 , 𝑢1 ] ⊆ [𝑙2 , 𝑢2 ]).
For the discrete attributes, we enforce NonNull ⊑ MaybeNull and Mut ⊑ Immut. Intuitively, 𝜎𝐿
stores conservative spatial facts. It uses lower bounds for guarantees (e.g., size and align), and an
over-approximating interval for possible offsets. Therefore, the join operation (⊔Lay ) keeps only
guarantees that hold on all incoming paths, while merging the set of possible offsets. It also down-
grades capabilities (e.g., to Immut or MaybeNull) unless they are guaranteed everywhere.
   At control-flow merge points, the join operation ⊔Lay computes the safe lower bound of guar-
antees. For example, it takes the minimum capacity (size⊔ = min(𝑧1 , 𝑧2 )) and the union of offset
intervals. If the target bases differ (𝑏1 ≠ 𝑏2 ), we set 𝑏⊔ = ⊤ but keep the common lower-bound
constraints. This decouples spatial safety from temporal safety: even if the exact object identity is
uncertain, UnsafeChecker can still prove that an access stays within the shared physical bounds.
   Finally, to support low-level pointer arithmetic and casting (e.g., reinterpreting *mut u64 as *mut
u8), we track all offsets and sizes in bytes. The size field reflects the total allocated capacity rather
than the initialized length. Although accessing uninitialized bytes within the allocated bounds is
spatially safe (i.e., no buffer overflow), it constitutes Undefined Behavior. This violation is detected
independently by the lifecycle domain, which tracks the Uninit state.

3.6   Abstract Semantics and Dataflow Propagation
We formalize the static analysis as a flow-sensitive abstract interpretation over the Rust MIR. The
analysis propagates the composite abstract state Σ = (𝜎𝐴 , 𝜎𝑂 , 𝜎𝐿 ) through the control flow graph
(CFG). This section defines the lattice structure, the symbolic initial state for procedure summaries,
and the transfer functions governing state transitions.
  The global abstract domain is the product of the three sub-domains defined above: 𝒟 = 𝒟𝑂𝑤𝑛 ×
𝒟𝐿𝑖𝑓 𝑒 × 𝒟𝐿𝑎𝑦 . The composite partial order ⊑ and join operator ⊔ are defined component-wise,
applying the respective domain-specific operations described in §3.3–3.5. This lets the analysis
compute a conservative may-approximation of the modeled program facts across all components
simultaneously.
3.6.1 Symbolic Initial State. To support the analysis of libraries, we construct a generic symbolic
precondition Σinit at the entry points (public APIs). For internal functions, the initial state is
directly propagated from their call sites via full inlining. For an entry point function 𝐹 , we construct
a symbolic initial state Σinit that reflects Rust’s ABI guarantees:
  Ownership. We assume mutable references do not alias, and owned objects form disjoint trees.
Each ownership node 𝑜 starts in a singleton alias set (Alias(𝑜) ← {𝑜}). Each pointer argument
𝑝 ∈ 𝐴𝑟𝑔𝑠𝐹 points to a fresh symbolic object (Pt(𝑝) = {𝑜𝑝 }). Local pointers start empty (Pt(𝑝) = ∅).
For composite arguments 𝑣 (e.g., Vec), we create a fresh heap object ℎ𝑣 and set Own(𝑣) = {ℎ𝑣 }.
  Lifecycle. We assume caller-provided values are valid. Input arguments start as Live. Local vari-
ables start as Uninit to capture use-before-def patterns in unsafe code.
 Layout. Pointers derived from arguments start with symbolic constraints. For a container argu-
ment 𝑣 , its internal pointer 𝑝𝑣 has a symbolic capacity 𝜅𝑣 and the alignment of 𝑇 :
                𝜎𝐿 (𝑝𝑣 ) = (ℎ𝑣 , 𝜅𝑣 ⋅ size_of(𝑇 ), [0, 0], align_of(𝑇 ), NonNull, mut_of(𝑣))
10                                                      Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


We also set Pt(𝑝𝑣 ) = {ℎ𝑣 }. This representation lets UnsafeChecker check constraints such as 𝑖 < 𝜅𝑣
without concrete values.
3.6.2 Auxiliary Operations. To simplify the operational semantics, we define auxiliary functions
that update the ownership topology and lifecycle states. They capture common patterns such as
resource destruction and overwriting.
  Topology Updates (Transfer, Alias Merge, and Isolate). These operations maintain the integrity of
the ownership graph during variable assignments.
• Transfer (TRansfeR(𝑦, 𝑥, 𝜎𝐴 )): Models the standard ownership transfer (move semantics).
  When a value is moved from 𝑥 to 𝑦 , this operation updates the topology by structurally replac-
  ing 𝑥 with 𝑦 in all aliasing sets and transferring the heap ownership mapping from 𝑥 to 𝑦 . This
  ensures that the new owner 𝑦 inherits the exact relationships of the original owner 𝑥 .
• Alias Merge (AliasMeRge(𝑦, 𝑥, 𝜎𝐴 )): Handles the creation of ownership aliases, such as when
  using ptr::read to duplicate a non-Copy value. This operation merges the equivalence classes
  of 𝑥 and 𝑦 into a single clique and merges heap ownership information by Own(𝑦) ← Own(𝑦) ∪
  Own(𝑥). This reflects the physical reality that both variables now claim ownership of the same
  underlying resource, allowing the analysis to track potential double-free violations if both are
  dropped.
• Isolate (Isolate(𝑥, 𝜎𝐴 )): Disconnects a variable 𝑥 from the ownership topology. Before 𝑥 is
  overwritten or invalidated, this operation removes it from all alias sets of its neighbors and
  resets its own alias set to a singleton. This preserves the symmetry of the aliasing relation and
  ensures that the old identity of 𝑥 does not affect the new value. It also clears 𝑥 ’s heap ownership
  mapping (Own(𝑥) ← ∅).
  Resource Management (Drop and Clear). These operations handle the destruction and overwrit-
ing of resources to prevent leaks and invalid access.
• Recursive Drop (RecuRsiveDRop(𝑢, Σ)): Models the cascading execution of destructors. It
  propagates the Dropped state not just to 𝑢 , but to all its ownership aliases.
           RecuRsiveDRop(𝑢, Σ) = fold(Σ′ , 𝜎𝐴 .Own(𝑢), 𝜆(𝜎 , ℎ).RecuRsiveDRop(ℎ, 𝜎))
  where Σ′ marks all aliases of 𝑢 as Dropped. This propagation is essential for detecting temporal
  violations: if one owner drops the resource, all other aliases must immediately reflect this invalid
  state to detect subsequent use-after-free errors.
• Clear (CleaR(𝑥, Σ)): Prepares a variable 𝑥 for overwriting after MIR drop effects have been
  handled explicitly by T-Drop. If 𝑥 ∈ 𝒪, it freshens the abstract identity of 𝑥 by calling Isolate
  to disconnect it from the previous ownership topology. If 𝑥 ∈ 𝒫, it resets pointer-specific state
  by setting Pt(𝑥) ← ∅ and 𝜎𝐿 (𝑥) ← ⊥Lay . If 𝑥 ∈ 𝒱𝑐𝑜𝑝𝑦 , it performs no state mutation. It does not
  introduce an additional destructor beyond the drops already present in MIR.
  State Transitions (Consume and Forget). We employ lightweight helpers to model affine type
semantics:
• Consume (Consume(𝑥, 𝜎𝑂 )): Transitions a variable 𝑥 and all its non-Copy sub-locations (fields)
  to the Moved state. This invalidates 𝑥 and any derived field pointers, preventing Use-After-Move
  errors.
• Forget (FoRget(𝑥, Σ)): Transitions 𝑥 to the Forgotten state (modeling mem::forget). Cru-
  cially, this operation propagates the Forgotten state to all fields of 𝑥 , ensuring that pointers to
  sub-fields (e.g., &x.f) are invalidated even if taken before the call.
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                       11


3.6.3 Transfer Functions (Operational Semantics). We formalize the transfer functions as inference
rules of the form Instruction,Σ→Σ
                                Preconditions
                                 ′            . These rules are summarized in Figure 3. For presentation,
we write a small instruction language that abstracts common MIR patterns, including allocation
(x = Alloc(T)), address-taking and casts (p = AddrOf(k, x) and p = Cast(k, q)), and pointer
arithmetic (p = q.offset(i)). Type parameters, size_of, align_of, field offsets, mutability, and
ABI layout facts are obtained from rustc MIR type and layout queries. We write Σ = (𝜎𝐴 , 𝜎𝑂 , 𝜎𝐿 ).
When a rule invokes an auxiliary operation and obtains an intermediate state Σ1 (e.g., CleaR
or Isolate), we write Σ1 = (𝜎𝐴1 , 𝜎𝑂1 , 𝜎𝐿1 ) and apply subsequent updates to these components.
We write StRongTaRget(𝑂𝑑𝑠𝑡 ) when 𝑂𝑑𝑠𝑡 = {𝑜} and 𝑜 denotes a singleton abstract object in the
current context. Allocation-site summaries and merged objects are not strong targets and therefore
use weak updates.
   Rule intuition. T-Alloc creates a fresh heap object and initializes all three domains: it sets life-
cycle to Live, records ownership edges, and initializes points-to and layout facts. The fresh pointer
starts with Mut capability because a newly allocated owned object is uniquely mutable at alloca-
tion time; later borrows and casts can downgrade or propagate this capability. T-Move transfers
the ownership topology and marks the source as Moved. T-ReadBits models ptr::read: it cre-
ates a new owner and merges alias sets to represent ownership duplication. T-DRop, T-FoRget,
and T-ManDRop update lifecycle and trigger the corresponding topology updates. T-ManDRop
moves the binding 𝑥 into the wrapper 𝑦 : the source binding 𝑥 becomes moved, but 𝑦 denotes valid
storage with suppressed automatic destruction. Therefore, ManuallyDropped is not included in In-
validSet; access through the wrapper is not reported as use-after-move. T-Load reads Copy data
and does not change ownership or lifecycle. Non-Copy value movement is handled by T-Move or
by ownership-producing API rules such as T-ReadBits, rather than by T-Load. T-StoRe-S and T-
StoRe-W write through pointers, using strong updates only when the destination denotes a single-
ton target and weak updates for merged targets or allocation-site summaries. T-PtRWRite models
ptr::write, which overwrites memory without dropping the old value. T-AddROf, T-Cast, and
T-UsePtR handle address-taking, casts, and pointer propagation separately. address-taking creates
target and layout facts from a place, casts preserve points-to and layout facts except for mutabil-
ity changes, and pointer propagation copies the existing facts unchanged. T-Offset propagates
bounds and alignment through pointer arithmetic; the gcd term gives a conservative lower bound
on the resulting pointer alignment after advancing by multiples of sizeof(𝑇 ).
3.6.4 Termination and Fixed-Point Iteration. The solver uses a standard worklist algorithm over
the CFG. It iterates until all program points reach a post-fixpoint. Termination follows from the
height of the abstract domains:
      • Finite domains (𝜎𝐴 , 𝜎𝑂 ). The ownership and lifecycle domains range over finite sets. ℒ
        is finite for a function body, and ℋ𝒪 is finite due to the allocation-site abstraction. The
        transfer functions are monotone w.r.t. ⊑, so ascending chains stabilize.
      • Layout domain (𝜎𝐿 ). The interval component has infinite height. We apply widening at
        loop headers when the interval grows, and optionally apply narrowing based on simple
        loop guards (e.g., i < len) to recover precision.
This combination guarantees termination and keeps the layout analysis practical.
3.6.5 Inter-Procedural Analysis via Full Inlining. Given that unsafe code regions in Rust typically
involve shallow call chains and static dispatch (e.g., calls to Vec::set_len or intrinsic functions),
we adopt a full inlining approach for inter-procedural analysis. This strategy offers full context
sensitivity by performing a recursive, depth-first traversal of the call graph.
12                                                                                  Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


 T-Alloc
        x = Alloc(T)             ℎ = fresh_heap(𝑥)               𝑝𝑥 ∈ 𝒫
     Σ1 = CleaR(𝑥, Σ)                                                                            T-Move
     𝜎𝑂′ = 𝜎𝑂1 [𝑥 ↦ {Live}, ℎ ↦ {Live}]                                                                        y = x       !𝐶𝑜𝑝𝑦(𝑥)
     𝜎𝐴′ = 𝜎𝐴1 [Own(𝑥) ↦ {ℎ}]                                                                      Σ1 = CleaR(𝑦, Σ)
     𝜎𝐴′ .Pt(𝑝𝑥 ) = {ℎ}                                                                            𝜎𝐴′ = TRansfeR(𝑦, 𝑥, 𝜎𝐴1 )
     𝜎𝐿′ = 𝜎𝐿1 [𝑝𝑥 ↦ (ℎ, size(𝑇 ), [0, 0], align(𝑇 ), NonNull, Mut)]                               𝜎𝑂′ = Consume(𝑥, 𝜎𝑂1 )[𝑦 ↦ {Live}]

     T-ReadBits
                 y = ptr::read(p)               𝑦 ∈𝒪
      Σ1 = CleaR(𝑦, Σ)                                                            T-ManDrop
      𝑂𝑠𝑟𝑐 = 𝜎𝐴1 .Pt(𝑝)                                                                          y = ManuallyDrop(x)
      𝜎𝑂′ = 𝜎𝑂1 [𝑦 ↦ {Live}]                                                       Σ1 = CleaR(𝑦, Σ) 𝜎𝐴′ = TRansfeR(𝑦, 𝑥, 𝜎𝐴1 )
      𝜎𝐴′ = fold(𝜎𝐴1 , 𝑂𝑠𝑟𝑐 , 𝜆(𝜎, 𝑜).AliasMeRge(𝑦, 𝑜, 𝜎 ))                        𝜎𝑂′ = Consume(𝑥, 𝜎𝑂1 )[𝑦 ↦ {ManuallyDropped}]

                                           T-Store-S
      T-Load                                *p = x           𝑂𝑑𝑠𝑡 = 𝜎𝐴 .Pt(𝑝)       𝑥∈𝒪        𝑂𝑑𝑠𝑡 = {𝑜}    StRongTaRget(𝑂𝑑𝑠𝑡 )
      y = *p      𝑦 ∈ 𝒱𝑐𝑜𝑝𝑦                                        Σ1 = CleaR(𝑜, Σ)       ′
                                                                                         𝜎𝐴 = TRansfeR(𝑜, 𝑥, 𝜎𝐴1 )
        Σ′ = CleaR(𝑦, Σ)                                           𝜎𝑂′ = Consume(𝑥, 𝜎𝑂1 )[𝑜 ↦ {Live}]

        T-Store-W
         *p = x         𝑂𝑑𝑠𝑡 = 𝜎𝐴 .Pt(𝑝)          𝑥∈𝒪             ¬StRongTaRget(𝑂𝑑𝑠𝑡 )                   T-Drop
                𝜎𝐴′ = fold(𝜎𝐴 , 𝑂𝑑𝑠𝑡 , 𝜆(𝜎 , 𝑜).AliasMeRge(𝑜, 𝑥, 𝜎 ))                                                  drop(x)
                𝜎𝑂′ = Consume(𝑥, 𝜎𝑂 )[∀𝑜 ∈ 𝑂𝑑𝑠𝑡 ∶ 𝑜 ↦ 𝜎𝑂 (𝑜) ∪ {Live}]                                    Σ′   = RecuRsiveDRop(𝑥, Σ)

                                                               T-PtrWrite
                   T-Forget                                     ptr::write(p, x)            𝑂𝑑𝑠𝑡 = 𝜎𝐴 .Pt(𝑝)           𝑂𝑑𝑠𝑡 = {𝑜}
                    mem::forget(x)                                   Σ1 = Isolate(𝑜, Σ) 𝜎𝐴′ = TRansfeR(𝑜, 𝑥, 𝜎𝐴1 )
                   Σ′ = FoRget(𝑥, Σ)                                 𝜎𝑂′ = Consume(𝑥, 𝜎𝑂1 )[𝑜 ↦ {Live}]

                                   T-AddrOf
                                                                 p = AddrOf(k, x)
                                     Σ1 = CleaR(𝑝, Σ) 𝜎𝐴′ = 𝜎𝐴1 [Pt(𝑝) ↦ {𝑥}]
                                     𝜎𝐿′ = 𝜎𝐿1 [𝑝 ↦ (𝑥, size(𝑥), [0, 0], align(𝑥), NonNull, mut(𝑘))]

     T-Cast                                                                       T-UsePtr
     p = Cast(k, q)             𝜎𝐿 (𝑞) = (𝑏𝑞 , 𝑠𝑞 , 𝑜𝑞 , 𝑎𝑞 , 𝑛𝑞 , 𝑚𝑞 )                                  p = Use(q)
      Σ1 = CleaR(𝑝, Σ)        𝜎𝐴′ = 𝜎𝐴1 [Pt(𝑝) ↦ 𝜎𝐴1 .Pt(𝑞)]                       Σ1 = CleaR(𝑝, Σ) 𝜎𝐴′ = 𝜎𝐴1 [Pt(𝑝) ↦ 𝜎𝐴1 .Pt(𝑞)]
      𝜎𝐿′ = 𝜎𝐿1 [𝑝 ↦ (𝑏𝑞 , 𝑠𝑞 , 𝑜𝑞 , 𝑎𝑞 , 𝑛𝑞 , mut(𝑘))]                            𝜎𝐿′ = 𝜎𝐿1 [𝑝 ↦ 𝜎𝐿 (𝑞)]

                 T-Offset
                 p = q.offset(i)               𝜎𝐿 (𝑞) = (𝑏, 𝑠, [𝑙, 𝑢], 𝑎, 𝑛, 𝑚)      val(𝑖) = [𝑖𝑚𝑖𝑛 , 𝑖𝑚𝑎𝑥 ]      sz = sizeof(𝑇 )
                                    Σ1 = CleaR(𝑝, Σ)
                                    𝜎𝐴′ = 𝜎𝐴1 [Pt(𝑝) ↦ 𝜎𝐴1 .Pt(𝑞)]
                                    𝜎𝐿′ = 𝜎𝐿1 [𝑝 ↦ (𝑏, 𝑠, [𝑙 + 𝑖𝑚𝑖𝑛 ⋅ sz, 𝑢 + 𝑖𝑚𝑎𝑥 ⋅ sz], gcd(𝑎, sz), 𝑛, 𝑚)]


                                        Fig. 3. Core Intra-Procedural Transfer Functions.

   Recursive traversal. When the analysis encounters a call d = F(args), it temporarily switches
to the callee and analyzes F in the caller context. Concretely, we create a fresh analysis context for
F and initialize its entry state from the caller’s current state. We then model parameter passing by
binding actual arguments to the callee’s formal parameters. After the callee reaches a fixed point,
we map the abstract state of its return value back to the destination d in the caller, and resume
propagation at the successor of the call site. This on-the-fly inlining preserves the caller’s context
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                                      13


                                E-AliasRet
                                 𝑜1 , 𝑜2 ∈ 𝒱𝑜𝑢𝑡       𝑜1 ≠ 𝑜2    Own(𝑜1 ) ∩ Own(𝑜2 ) ≠ ∅
                                       Σ𝑓 𝑖𝑛𝑎𝑙 ⊢ 𝜄end ⟹ ERR(DoubleOwneRship)

           E-MutAlias
                                                   𝑝1 , 𝑝2 ∈ 𝒱𝑜𝑢𝑡 ∧ 𝑝1 ≠ 𝑝2
           is_ref(𝑝1 ) ∧ is_ref(𝑝2 )         Pt(𝑝1 ) ∩ Pt(𝑝2 ) ≠ ∅     (𝜎𝐿 (𝑝1 ).mut = Mut ∨ 𝜎𝐿 (𝑝2 ).mut = Mut)
                                             Σ𝑓 𝑖𝑛𝑎𝑙 ⊢ 𝜄end ⟹ ERR(MutAlias)

            E-Dangling
            𝑝 ∈ 𝒱𝑜𝑢𝑡      sizeof(𝑇 ) > 0       ∃𝑜 ∈ Pt(𝑝).𝜎𝑂 (𝑜) ∩ {Dropped, Moved, Forgotten, Uninit} ≠ ∅
                                           Σ𝑓 𝑖𝑛𝑎𝑙 ⊢ 𝜄end ⟹ ERR(DanglingPtR)

          E-Layout
                          𝑣 ∈ 𝒱𝑜𝑢𝑡 ∧ Type(𝑣) = Vec < 𝑇 >            𝑝 = 𝑣.ptr, ℓ = 𝑣.len, 𝑐 = 𝑣.cap
          (𝜎𝐿 (𝑝).size < 𝑐 ⋅ sizeof(𝑇 )) ∨ (ℓ > 𝑐) ∨ (𝜎𝐿 (𝑝).align < align_of(𝑇 )) ∨ (𝑐 ⋅ sizeof(𝑇 ) > isize::MAX)
                                           Σ𝑓 𝑖𝑛𝑎𝑙 ⊢ 𝜄end ⟹ ERR(InvalidLayout)

                       E-Leak
                        ℎ ∈ ℋ𝒪         Dropped ∉ 𝜎𝑂 (ℎ)         ∀𝑣 ∈ 𝒱𝑜𝑢𝑡 .ℎ ∉ Own(𝑣) ∧ ℎ ∉ Pt(𝑣)
                                                  Σ𝑓 𝑖𝑛𝑎𝑙 ⊢ 𝜄end ⟹ ERR(LeaK)


               Fig. 4. Soundness Violation Detection Rules (Part 1: Boundary-Level Checks).

and makes aliasing, lifecycle, and layout constraints flow naturally across calls, without building
a separate inter-procedural CFG ahead of time.
  Recursion and external calls. To avoid non-termination, we impose an inline depth limit (default
𝑘 = 3). If the limit is reached, or the callee body is unavailable (e.g., FFI), we use a conservative
summary. The summary may mutate any reachable state of mutable arguments, and it returns an
unconstrained value (⊤).

3.7   Detecting Potential Violations
We formalize detection as judgment rules of the form Σ ⊢ Ctx ⟹ ERR(𝜅). Ctx denotes either
a runtime instruction 𝜄 or the function exit point 𝜄end . The rules are summarized in Figure 4 and
Figure 5. We treat both boundary-level contract violations and instruction-level UB as evidence of
unsoundness. Accordingly, we organize detection into two granularities. The first is a boundary-
level check at 𝜄end , which focuses on safety invariants exposed to safe clients. The second is an
instruction-level check during propagation, which focuses on instruction-level UB inside unsafe
code (e.g., invalid dereference and out-of-bounds access).
   Boundary-Level Checks. The core question is whether a safe API can leak an unsafe state that
enables safe callers to trigger UB. We perform these checks at function exit (𝜄end ) and apply them to
observable output variables. We let 𝒱𝑜𝑢𝑡 denote the set of values that escape to the caller at exit—
return values, out-parameters (e.g., mutable reference targets that remain visible to the caller),
and any other exposed references or owned values. Our boundary checks consider only variables
in 𝒱𝑜𝑢𝑡 . E-AliasRet prevents double-free by ensuring no two return values claim ownership of
the same underlying resource (checking intersection of Own sets). E-MutAlias enforces Rust’s
uniqueness guarantee by detecting if multiple return values (specifically references) alias the same
location with at least one being mutable. E-Dangling ensures exposed pointers do not target
invalid memory. E-Layout checks that assembled containers (e.g., Vec::from_raw) satisfy their
14                                                                          Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


                 E-Access
                 𝜄 ∈ {read(𝑝), write(𝑝)}         𝑜 ∈ Pt(𝑝)       sizeof(𝑇 ) > 0        𝑆 = 𝜎𝑂 (𝑜) ∩ InvalidSet ≠ ∅

                                             ⎧ERR(UAF) if Dropped ∈ 𝑆
                               Σ⊢𝜄 ⟹          ERR(UBD) if Uninit ∈ 𝑆
                                             ⎨
                                             ⎩ERR(UAM) if (Moved ∈ 𝑆) ∨ (Forgotten ∈ 𝑆)

            E-DoubleFree
             𝜄 = drop(𝑥)      (∃ℎ ∈ Own(𝑥).Dropped ∈ 𝜎𝑂 (ℎ)) ∨ (𝜎𝑂 (𝑥) ∩ {Moved, Forgotten, Uninit} ≠ ∅)
                                                  Σ ⊢ 𝜄 ⟹ ERR(DoubleFRee)

                     E-RefCreation
                                                   𝜄 = mk_ref(𝑝)         𝑜 ∈ Pt(𝑝)
                                    ERR(InvalidRef)          if (sizeof(𝑇 ) > 0) ∧ (𝜎𝑂 (𝑜) ∩ InvalidSet ≠ ∅)
                     Σ⊢𝜄 ⟹ {
                                    ERR(Null/Align)          if 𝜎𝐿 (𝑝).align < align_of(𝑇 )

E-OOB/MA
     𝜄 = access(𝑝)    (_, size, [𝑙, 𝑢], align, _, _) = 𝜎𝐿 (𝑝)
                                                                         E-NullDeref
        ERR(OOB) if 𝑙 < 0 ∨ (𝑢 + sizeof(𝑇 )) > size                       𝜄 ∈ {deref(𝑝), mk_ref(𝑝)}         𝜎𝐿 (𝑝).null = MaybeNull
 Σ⊢𝜄 ⟹ {
        ERR(MA) if align < align_of(𝑇 )                                                  Σ ⊢ 𝜄 ⟹ ERR(NullDeRef)

                                   E-SizeMismatcH
                                   𝜄 ∈ {ptr::read/write … }              𝜎𝐿 (𝑝).size < sizeof(𝑇 )
                                                 Σ ⊢ 𝜄 ⟹ ERR(SizeMismatch)

                             E-Proj
                              𝜄 = Proj(𝑝, 𝑓 )       𝛿 = offset(𝑓 )       𝜎𝐿 (𝑝).size < 𝛿 + sizeof(𝑓 )
                                                  Σ ⊢ 𝜄 ⟹ ERR(InvalidPRoj)

                       E-PtrAritH
                       𝜄 = 𝑝.add(𝑛)         (_, size, [_, 𝑢], _, _, _) = 𝜎𝐿 (𝑝)      𝑢 + 𝑛 ⋅ sizeof(𝑇 ) > size
                                                Σ ⊢ 𝜄 ⟹ ERR(InvalidPtRARith)

            E-SliceInvalid
             𝜄 = slice::from_raw(𝑝, 𝑙𝑒𝑛)           (𝑙𝑒𝑛 ⋅ sizeof(𝑇 ) > isize::MAX) ∨ (𝑙𝑒𝑛 ⋅ sizeof(𝑇 ) > 𝜎𝐿 (𝑝).size)
                                                  Σ ⊢ 𝜄 ⟹ ERR(InvalidSlice)

                                           E-MutateImmut
                                            𝜄 = write(𝑝, _)          𝜎𝐿 (𝑝).mut = Immut
                                             Σ ⊢ 𝜄 ⟹ ERR(MutateImmutable)


Fig. 5. Soundness Violation Detection Rules (Part 2: Instruction-Level Checks). InvalidSet                                        =
{Dropped, Moved, Forgotten, Uninit}.


validity invariants on internal components (pointer, length, and capacity). This includes capacity
bounds, length limits, alignment, and isize::MAX overflow. Finally, E-LeaK identifies resource
leaks by checking for any heap object ℎ that remains live (Dropped ∉ 𝜎𝑂 (ℎ)) at function exit but
is unreachable from the caller (i.e., not owned or pointed to by any variable in 𝒱𝑜𝑢𝑡 ).

   Instruction-Level Checks. E-Access guards against UAF, UBD, and UAM. E-DoubleFRee pre-
vents dropping invalid or already-dropped resources. It checks the state of the resource rather than
just the variable, which reduces false positives from spurious aliasing. E-RefCReation ensures
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                      15


references are created from valid, aligned, non-null pointers. E-OOB/MA and E-NullDeRef han-
dle standard memory errors. E-PtRARith and E-PRoj enforce in-bounds requirements for pointer
arithmetic and field projection (covering [place-projection] UB). E-SliceInvalid prevents the
creation of invalid slices (e.g., length exceeding allocation).

4 Experiment Settings
4.1   Research Questions
We evaluate UnsafeChecker by answering the following research questions:
RQ1. Effectiveness: On a ground-truth CVE benchmark, can our framework outperform state-
     of-the-art tools in detecting Rust-specific UBs?
RQ2. Precision and Recall Analysis: What precision/recall trade-offs does our framework ex-
     hibit, and what are the main sources of false positives and false negatives?
RQ3. Efficiency: Is our framework efficient enough for real-world use, with acceptable analysis
     time and memory overhead on large Rust crates?
RQ4. Large-Scale Discovery of Unknown Bugs: Can our framework discover previously unre-
     ported bugs in real-world Rust crates at scale?

4.2   Dataset Construction
We constructed two distinct datasets to support the studies in Section 5:
Dataset A (Known Vulnerabilities): We selected 46 CVEs from the RustSec Advisory Database.
To construct a focused benchmark, we specifically targeted soundness issues caused by unsafe
memory operations (e.g., buffer overflow, use-after-free, uninitialized memory) that fall within
our sequential analysis scope. Accordingly, we excluded vulnerabilities that rely on external se-
mantics (e.g., FFI, platform-specific hardware) or application-specific logic errors (e.g., index desyn-
chronization or complex state machine bugs). Because many baseline tools rely on older compiler
versions that often fail to compile the original crates, we extracted the key vulnerable code into
minimized libraries that faithfully reproduce the original bugs. We manually verified these test
cases and inspected the tool warnings to ensure that any potential new bugs in the constructed
code are correctly identified, avoiding incorrect false positive reports. We use RustSec-derived
cases rather than Miri or Rudra benchmark suites as the primary benchmark because Miri is an
execution validator rather than a static-analysis benchmark, and Rudra includes bug classes out-
side our current modeled scope; all baselines are therefore compared on the same RustSec-derived
subjects. This dataset serves as the ground truth for measuring detection effectiveness.
Dataset B (Wild Crates): To evaluate the bug detection capability of UnsafeChecker in the wild,
we scanned the entire crates.io registry. Due to the large volume of results, it is impractical to
manually audit all of them. Instead, we manually inspected the reports from approximately 10,000
crates to verify the findings. From this inspected subset, we identified 83 distinct crates containing
potential bugs, which form Dataset B. These crates span diverse domains, including data structures,
memory management, and no-std libraries, with a total of over 30 million downloads.

4.3   Baseline Selection
We selected three representative baselines covering distinct Rust static analysis paradigms, ensur-
ing fair comparison against state-of-the-art tools. All baselines used their latest stable versions
and default configurations to match real-world usage. All experiments were conducted on the
same machine with an Intel Core i7 processor and 64GB of RAM, running Ubuntu 22.04 LTS.
   (1) MirChecker [16]: MIR-level static analyzer, uses numerical/symbolic analysis for generic
        errors (e.g., integer overflow) but lacks Rust-specific ownership tracking.
16                                                            Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


      (2) Rudra [4]: Unsafe code pattern matcher, flags risky unsafe constructs (e.g., ‘ptr::copy‘ in
          unsafe blocks) but lacks semantic understanding.
      (3) SafeDrop [7]: Deallocation-focused analyzer, detects double free/UAF but ignores align-
          ment/OOB and nested ownership.

4.4     Implementation
Our prototype, UnsafeChecker, is implemented as a Rust compiler plugin based on the MIR (Mid-
level Intermediate Representation). It uses the rustc_middle and rustc_mir_dataflow libraries
for MIR traversal and dataflow analysis. For symbolic modeling of memory layouts and values,
we drew inspiration from the design of MIRAI [22], an abstract interpreter for Rust. While MIRAI
focuses on generic property verification (e.g., panics and standard assertions) using a heavy-weight
solver-based approach, our implementation specializes its symbolic memory model to efficiently
track Rust’s unique ownership and lifecycle semantics alongside spatial constraints. For numerical
analysis, we integrate the Apron numerical abstract domain library. Constraint solving is handled
by the Z3 SMT solver.

5 Results and Analysis
5.1     RQ1: Effectiveness
To evaluate the effectiveness of UnsafeChecker in detecting real-world vulnerabilities, we tested it
against Dataset A, which comprises 46 known CVEs. In contrast to RQ4, which targets open-world
bug discovery in the wild (Dataset B), RQ1 evaluates detection effectiveness on a closed benchmark
with ground truth and compares against state-of-the-art baselines. We compared our results with
three baseline tools: MirChecker, Rudra, and SafeDrop. Table 1 presents the comparative results.
We count a CVE as detected if a tool reports at least one true positive alert that matches the
vulnerability, based on our manual audit of the tool outputs.
Table 1. Comparison of bug detection effectiveness on 46 known vulnerabilities (Dataset A). Detected by
Type counts the number of unique bugs (ground-truth patterns) successfully detected by each tool for each
category. Total Bugs is the number of detected bugs out of the 53 total ground-truth bugs. Total CVE is
the number of unique CVEs detected out of 46. The Recall (Bug) column reports bug-level recall. Total
Alerts shows the total number of warnings generated by the tool, TP Alerts is the number of true positive
alerts, and Precision is computed as TP Alerts/Total Alerts. The number in parentheses in the header row
indicates the number of ground-truth bugs for that specific unsoundness category.

 Tool                       Detected by Type (Bugs)       Total       Total     Recall    TP      Total    Precision
                        Uninit (24)   OOB (25) Own (4)   Bugs (53)   CVE (46)   (Bug)    Alerts   Alerts
 MirChecker                  0           0        0          0          0        0.0%      0       45        0.0%
 SafeDrop                    0           0        1          1          1        1.9%      1        4        25.0%
 Rudra                      11           0        0         11         11       20.9%     11       11       100.0%
 UnsafeChecker (Ours)       15          19        2         36         32       67.9%     64       124      51.6%


  UnsafeChecker detected 32 out of 46 vulnerabilities (69.6%), significantly outperforming the best
baseline, Rudra, which detected only 11 (23.9%). As shown in Table 1, UnsafeChecker demonstrates
superior effectiveness across all vulnerability categories. At the bug level (ground-truth patterns),
UnsafeChecker successfully covered 36 out of 53 bugs (67.9%), including 15 uninitialized mem-
ory bugs and 19 out-of-bounds bugs, whereas Rudra only covered 11 bugs in total. Compared with
Rudra, UnsafeChecker identified an additional 21 CVEs. The 53 ground-truth bug patterns fur-
ther refine into six categories: 11 uninitialized-memory bugs, 13 length or state-consistency bugs,
25 out-of-bounds or pointer-boundary bugs, 1 use-after-free bug, 1 double-ownership bug, and
 UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                                 17




1 pub fn into_inner(self) -> T {
2     let span: *const Span = &self.span;
                                                           1 fn random_seed(_: &Path, _: &str) -> [u64; 2] {
3     let inner: *const ManuallyDrop<T> = &self.inner;
                                                           2     use std::mem::uninitialized as rand;
4     mem::forget(self);
                                                           3     unsafe { [rand::<u64>() ^ 0x12345678,
5     let _span = unsafe { span.read() };
                                                           4                     rand::<u64>() ^ 0x87654321] }
6     let inner = unsafe { inner.read() };
                                                           5}
7     ManuallyDrop::into_inner(inner)
8}



 Listing 3. Buggy code for RUSTSEC-2023-0078                 Listing 4. An instance of uninitialized used for
 in tracing: take field pointers and then call               entropy generation.
 mem::forget.

 2 dangling-pointer bugs. Table 1 aggregates these fine-grained labels into three analysis-facing
 groups: uninitialized-memory and length/state-consistency bugs are reported under uninitialized
 memory, out-of-bounds and pointer-boundary bugs under out-of-bounds, and use-after-free, dou-
 ble ownership, and dangling pointers under dangling pointers.
    To further illustrate UnsafeChecker’s detection capability, we highlight three representative
 cases missed by all baselines. One example is RUSTSEC-2023-0078 in the well-known tracing
 crate maintained by tokio-rs. Listing 3 shows the vulnerable pattern: it takes pointers to fields
 and then calls mem::forget(self). This is UB because mem::forget(self) consumes (moves)
 self; after that point, self is no longer live and the compiler may reuse its stack storage, inval-
 idating the saved pointers to its fields. The advisory was fixed by replacing mem::forget with
 ManuallyDrop in Instrumented::into_inner 1 , which keeps the storage valid when taking field
 pointers. In our model, mem::forget(self) transitions self to the Forgotten state, which rep-
 resents a semantic move with destructor suppression. Subsequent reads through pointers derived
 from self are then reported as a use-after-move alarm. Reading from uninitialized memory is un-
 defined behavior in Rust. In RUSTSEC-2018-0022, the developer used std::mem::uninitialized
 to read stack garbage for entropy. For example, Listing 4 shows an instance reported in the tempo-
 rary crate 2 . UnsafeChecker’s lifecycle domain tracks the Uninit state of the returned value and
 reports the subsequent read as an uninitialized-memory violation. For pointer bounds, we detect an
 unsoundness of wrflib 3 in RUSTSEC-2025-0072. The functions under wrflib::byte_extract
 are wrappers over pointer offset (e.g., data.as_ptr().add(offset)) without sufficient bounds
 checks. Our layout domain models the spatial attributes of the pointer and the bounds of the al-
 location. By propagating these constraints to the dereference point, it can determine that offset
 may exceed the object’s size, pinpointing the out-of-bounds violation.
    Baselines missed these cases because they require semantic reasoning over object states and
 derived pointers, rather than matching a specific risky API signature. UnsafeChecker detected
 more than 20 vulnerabilities that were missed by all other baselines. This demonstrates that Un-
 safeChecker fills a significant gap in Rust static analysis.

 5.2   RQ2: Precision and Recall Analysis
 While RQ1 focuses on effectiveness (recall), this section analyzes the trade-off between precision
 and recall by inspecting false positives and false negatives. As shown in Table 1, UnsafeChecker
 generated a total of 124 alerts. Among them, 64 are true positive alerts (which successfully cover
 the 36 ground-truth bugs) and 60 are false positive alerts, resulting in an alert-level precision
 1
   https://github.com/tokio-rs/tracing/pull/2765
 2
   https://github.com/stainless-steel/temporary/issues/2
 3
   https://rustsec.org/advisories/RUSTSEC-2025-0072.html
18                                                     Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


of 51.6%. Despite its high recall compared to baselines, UnsafeChecker missed 14 vulnerabilities
(30.4%) and 17 ground-truth bugs (32.1%). We organize the main sources of imprecision by domain
(Section 3).
5.2.1 False Positives. We analyzed the 60 false positives to identify the primary sources of impreci-
sion. The largest share (51.7%, 31/60) stems from the layout domain, primarily because our layout
facts are conservative lower bounds and our arithmetic reasoning uses widening and interval ab-
stractions. When indices depend on complex non-linear operations (e.g., bitwise arithmetic) or
external inputs, our solver may fail to derive tight constraints. In such cases, we keep conservative
offset intervals, which can lead to potential out-of-bounds or misalignment alarms. The lifecycle
domain contributes another 35.0% (21/60), often caused by control-flow merges and opaque calls.
Our lifecycle domain represents uncertainty as sets of states (e.g., {Live, Uninit}), so conditional
initialization patterns naturally lead to “maybe uninitialized” alarms. This is amplified at external
call boundaries (e.g., FFI) and at recursion cutoffs, where we conservatively over-approximate ef-
fects and may lose the evidence needed to prove initialization. Finally, the ownership domain
accounts for 13.3% (8/60), typically arising from path-insensitive aliasing approximations in func-
tions with complex control flows, where the tool may incorrectly infer double frees by merging
disjoint paths.
   Dataset B should not be interpreted as a closed-world precision experiment, because the remain-
ing warnings were not exhaustively labeled. Instead, it measures alarm density, triage workload,
and validated discovery yield. Among the approximately 10,000 manually inspected crates, Un-
safeChecker flagged 378 crates and produced 2,639 raw warnings, which were de-duplicated into
1,736 unique warnings during triage. This bounded workload led to 114 Miri-validated bugs across
83 crates; 45 have been acknowledged by developers or RustSec experts, and 27 have been fixed. For
alert-volume context, Rudra successfully compiled and analyzed 2,892 crates in the same 10,000-
crate set, flagged 119 crates, and produced 326 warnings. On the same Rudra-compilable subset,
UnsafeChecker flagged 141 crates and produced 1,296 raw warnings, deduplicated to 784 unique
warnings. These numbers describe workload and triage scale, not closed-world precision.
5.2.2 False Negatives. We manually inspected the 14 missed vulnerabilities and grouped their pri-
mary causes into four scope or precision boundaries. First, 7 missed CVEs require library or API
semantics not explicitly modeled by the current implementation, such as Cell, alignment-related
allocation APIs, debug_assert, or specialized crate APIs. For example, UnsafeChecker missed
RUSTSEC-2023-0017 (maligned) because we do not yet model Layout::from_size_align, lead-
ing to missing layout constraints for the allocated pointer. Second, 3 require more precise numeric,
loop, or iterator reasoning than our current interval abstraction maintains. Third, 2 require per-
element array or initialization-state tracking finer than our current memory abstraction. Finally,
2 depend on external or cross-boundary logic state, such as cache behavior or raw-pointer state
changes across method sequences. Despite these misses, UnsafeChecker’s detection capability re-
mains significantly higher than all baselines. The missed cases identify engineering and modeling
boundaries rather than invalidating the modeled warning rules.

5.3   RQ3: Efficiency
We evaluated the runtime efficiency of UnsafeChecker to determine its suitability for real-world
development workflows. We report both end-to-end running time and the split between Un-
safeChecker’s analysis pass and compilation/non-analysis overhead. The end-to-end number
reflects user-visible cost, while the split isolates the cost of the analysis itself. We measured the
running time and memory overhead for 9 representative crates from Dataset B, ranging from
small utilities to large-scale applications.
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                                                                             19


  Table 2 details the performance metrics for these crates. Across the 9 crates, the median end-to-
end running time is 11.4s, with a maximum of 264.0s. For small libraries (<10k LOC), the analysis
typically completes within 10 seconds. For large crates (>100k LOC), the analysis finishes within
5 minutes, and the slowest case we measured (meilisearch) completes in about 264s. The median
memory usage is 475.2 MB and the peak is 4.3 GB, which fits typical developer machines.

Table 2. Efficiency of UnsafeChecker on Real-World Crates. A(s) reports UnsafeChecker analysis time,
C/O(s) reports compilation and other non-analysis overhead, and T(s) reports end-to-end time.

                    Small (<10k LOC)                             Medium (10k-100k LOC)                                   Large (>100k LOC)
 Crate       LOC      A(s)   C/O(s)    T(s)   M(MB)    Crate   LOC     A(s)   C/O(s)   T(s)   M(MB)    Crate          LOC     A(s)    C/O(s)   T(s)    M(MB)
 bitflags    5.0k      0.6      0.3     0.9    118.7   serde   33.3k    4.4      1.7    6.1    275.7   diesel        126.8k    89.2     24.3   113.5   1350.2
 log         3.8k      1.1      0.5     1.6    109.0   regex   96.5k    6.8      1.8    8.6    505.2   meilisearch   244.6k   211.7     52.3   264.0   4329.2
 bytes       7.1k      8.7      2.7    11.4    170.2   tokio   93.1k   14.6      4.5   19.1    475.2   nushell       287.6k    70.9     23.7    94.6   2853.6



   The running time does not strictly correlate with LOC, as it also depends on code complexity
(e.g., heavy use of macros or complex control flows). For instance, diesel (126.8k LOC) takes
longer (113.5s) than nushell (287.6k LOC, 94.6s). Overall, these results show that our shared-
state analysis is efficient enough for daily use. At ecosystem scale, running on a compute server,
UnsafeChecker analyzed over 100,000 crates within two days.
   We also compared the efficiency of UnsafeChecker against the baselines on Dataset A (the CVE
benchmark). The reported times include both Rust compilation and tool execution. UnsafeChecker
analyzed all 46 CVE cases in 35.7 seconds (0.78s per case on average). In contrast, Rudra took 179.7
seconds (5× slower), and MirChecker required 781.9 seconds (> 20× slower). SafeDrop achieved a
similar speed (36.1s), but as shown in RQ1, it only detected one vulnerability in this dataset. This
indicates that UnsafeChecker keeps the analysis cost practical while preserving the RQ1 effective-
ness advantage.

5.4         RQ4: Large-Scale Discovery of Unknown Bugs
We applied UnsafeChecker to the entire crates.io registry to demonstrate its scalability. Running on
a compute server, UnsafeChecker analyzed over 100,000 crates within two days. Unlike RQ1–RQ3,
which evaluate against a ground-truth CVE benchmark, RQ4 targets open-world bug discovery,
where no complete ground truth exists. Due to the high volume of alarms from over 100,000 crates,
we employed random sampling to select approximately 10,000 crates for manual verification. This
process yielded 83 distinct crates with potential bugs (Dataset B). Our verification criterion is
strict: a warning is considered a bug only if we can construct a Proof-of-Concept (PoC) triggering
undefined behavior (UB) on MIRI via safe public APIs.
   The results are summarized in Table 3. Within the manually inspected subset, UnsafeChecker
identified 114 Miri-validated bugs across 83 crates. Importantly, we manually validated these
reports by constructing executable PoCs that trigger UB in Miri through safe public APIs. The
PoCs were manually written; UnsafeChecker’s reports guided their construction by identifying the
unsafe operation, the violated invariant, and the relevant state trace. This result should be read as
open-world discovery yield rather than alert-level precision. We reported all these findings to the
crate maintainers. As of the time of writing, developers or RustSec experts have acknowledged 45
bugs and fixed 27 of them. Eleven validated findings have received public vulnerability identifiers.
The remaining reports are currently pending developer response. The flagged crates range from
small utilities to large libraries, confirming the tool’s scalability. Figure 6 details the characteristics
of the flagged crates. These libraries are widely used and actively maintained, as reflected by their
download statistics, meaning that they affect the Rust ecosystem’s security. Vulnerabilities span 34
20                                                                                                                                                                                                                 Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


                        57                                                                                                                      39                                                                                                                           48
                                                                  52                                                                                                   36                                                                                                                                        44


                        42                                                                                                                      29                                                                                                                           36
                                                                                                                                                         26                                                                                                                                        32
     Crates with bugs




                                                                                                                             Crates with bugs




                                                                                                                                                                                                                                                          Crates with bugs
                        28                                                                                                                      19                                                                                                                           24

                                                    15
                        14                                                      11                                                               9                                   8            8                                                                          12
                                                                                              4                                                                                                                4                                                                                                               4
                                                                                                           1                                                                                                                1                                                         2                                                     1
                         0                                                                                                                       0                                                                                                                            0
                             1         2        3             4             5             6            7            8                                1             2             3            4            5            6            7        8                                   1            2             3             4            5            6        7
                          10      10       10            10            10            10           10           10                                 10          10            10           10           10           10           10       10                                    10         10            10            10           10           10       10
                                                    Total Downloads                                                                                                          Recent 90d Downloads                                                                                                                     LoC

                                 (a) Total Downloads              (b) Recent 90-day Downloads              (c) LoC Distribution
                                             Fig. 6. Characteristics of 83 Flagged Crates (114 Miri-Validated Bugs)

categories, with data-structures, no-std, and memory-management being most frequent, indicating
that even foundational libraries often fail to guarantee memory safety.
   The issues detected by UnsafeChecker encompass a broad spectrum of memory safety viola-
tions, along with a small set of auxiliary checks. They are not concentrated in a fixed ptr::read
or mem::forget pattern: at the bug level, these two APIs account for only 5 and 1 of the 53 Dataset
A bug patterns covered by UnsafeChecker, and 19 and 4 of the 114 Dataset B bugs, respectively.
In Dataset B, the validated bugs involve 129 related unsafe-API call sites across 21 APIs, including
pointer arithmetic and offset APIs, unchecked slice/string construction APIs, raw ownership or
allocation-takeover APIs, and type or initialization invariant bypasses. In Table 3, we categorize
these 114 reports by their observable manifestations—such as out-of-bounds (OOB) access or use-
after-free (UAF)—to facilitate reporting and comparison. However, UnsafeChecker detects these
vulnerabilities by identifying invariant violations over the facts maintained in its shared abstract
state. Specifically, violations in the layout domain account for the majority of cases, including out-
of-bounds (60 cases), misaligned access (11 cases), and various forms of invalid pointers (e.g.,
null dereferences). These issues typically arise from incorrect pointer arithmetic or unchecked
casts that violate spatial memory constraints. The ownership domain and lifecycle domain are crit-
ical for detecting temporal safety issues; they identified ownership duplication (17 cases) and
dangling pointers (7 cases) by tracking invalid object state transitions, such as accessing moved
values or dropping the same resource twice. Beyond these, UnsafeChecker also flagged a small
set of auxiliary issues, including resource leaks (5 cases), integer overflow, division by zero,
and UTF-8 validation. These issues are not strictly memory-unsafe by themselves (e.g., mem-
ory leaks are safe in Rust), but they frequently indicate logical errors or appear in index and size
computations that feed into unsafe memory accesses.
Table 3. Summary of detected, confirmed, and fixed issues by type. Abbreviations: OOB (Out-of-Bounds),
OD (Ownership Duplication), MA (Misaligned Access), IO (Integer Overflow), IP (Invalid Pointer), DP (Dan-
gling Pointer), DBZ (Division by Zero), UTF8 (UTF-8 Validation), RL (Resource Leak), NP (Null Pointer), UM
(Uninitialized Memory). Crates counts unique crates per type (a crate may appear in multiple columns), so
summing this row will over-count and can exceed the total.

                                                                                                           OOB OD MA IO IP DP DBZ UTF8 RL NP UM Other Total
                                                         Crates                                                42       13          8                     3             3                6             1                        1                 5   2                      1             2                     83
                                                         Detected                                              60       17         11                     3             3                7             1                        1                 5   2                      1             3                     114
                                                         Confirmed                                             20       10          4                     2             2                2             1                        1                 1   1                      1             0                     45
                                                         Fixed                                                 13       6           0                     1             1                1             1                        1                 1   1                      1             0                     27

   Table 3 shows that layout-related issues dominate the reports: Out-of-Bounds accounts for 52.6%
(60/114) and misaligned access accounts for 9.6% (11/114). Temporal and ownership-related issues
are also common, including ownership duplication (17/114) and dangling pointers (7/114). These
  UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                   21


  distributions align with our three-component classification, with most confirmed bugs rooted in
  violations of layout, object-validity, or ownership invariants.
  5.4.1 Case Studies. We present four case studies of real-world bugs. Cases 1, 3, and 4 illustrate
  how our framework detects composite UBs missed by baselines, while Case 2 demonstrates an
  auxiliary check for resource leaks.
     Case 1: Dangling Pointer in multiversx_chain_vm (132k downloads). We detected a criti-
  cal drop-safety violation in multiversx_chain_vm that leads to a dangling pointer. The function
  with_shared_mut_ref, shown in Listing 5, uses unsafe code to duplicate ownership of a value
  behind a mutable reference (&mut T) using std::ptr::read. This operation performs a bitwise
  copy of the underlying value without consuming the original, effectively creating two owners for
  the same resource: one in the temporary Rc and one still behind the reference. If the user-provided
  closure f panics, the temporary Rc is dropped during stack unwinding, deallocating the underlying
  resource obj. However, the original slot still contains a stale copy of obj. As a result, the caller
  can later access freed memory through t, and dropping t triggers a double free.

  Listing 5 Double Free vulnerability in multiversx_chain_vm triggered by panic unwinding.
 1 pub fn with_shared_mut_ref<T, F>(t: &mut T, f: F) {
 2     unsafe {
 3         // ... (extract obj) ...
 4         let obj = std::ptr::read(t);
 5         let obj_rc = Rc::new(obj);
 6         f(obj_rc.clone());       // [2] Panic drops obj_rc (Free #1); skips [3]
 7         std::ptr::write(t, ...); // [3] Restore t (Only on normal return)
 8     }
 9     // ...
10 }


     Case 2: Resource Leak in bytes-kman. While memory leaks are strictly considered safe in
  Rust’s semantic model (e.g., Box::leak is a safe function), they often indicate logical bugs in re-
  source management. As an auxiliary check, UnsafeChecker identifies such resource leaks. We de-
  tected a significant leak in the from_bytes implementation for arrays in bytes-kman. As shown in
  Listing 6, the code first collects deserialized elements into a temporary Vec<T>. To return a fixed-
  size array [T; LEN], it converts the vector into a boxed slice and calls Box::leak to obtain a static
  reference. Finally, it uses ptr::read to copy the data from this static reference into the return
  value. Although Box::leak intentionally extends the lifetime of the heap memory, ptr::read
  only performs a bitwise copy without taking ownership of the backing allocation. Consequently,
  the leaked heap memory becomes unreachable and is never deallocated. UnsafeChecker flagged
  this issue by checking that the heap object remains live at function exit but becomes unreachable
  from the caller (Rule E-Leak).
  Listing 6 Memory Leak in bytes-kman due to Box::leak and ptr::read.
1 fn from_bytes(buffer: &mut TBuffer) -> Option<Self> {
2     let mut res = Vec::with_capacity(LEN);
3     // ... (fill res) ...
4     let res = Box::leak(res.into_boxed_slice()); // [1] Leak heap memory
5     let res = unsafe {
6         std::ptr::read(res.as_ptr() as *const [T; LEN]) // [2] Copy bits; [1] never freed!
7     };
8     Some(res)
9}


    Case 3: Ownership Duplication in doubly. We identified a critical double free in the
  pop_back method of doubly (Listing 7). The code uses ptr::read to duplicate ownership of
  the value from the heap node into val. It then drops the node by reconstructing a Box from the
  22                                                             Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


  raw pointer. However, dropping a Box<Node<T>>(line 8) automatically drops its content. Since
  ptr::read duplicates the value without consuming the original, this drop frees the resource while
  val still holds a copy, causing a double free. Our tool detected this by tracking the ownership
  alias created by ptr::read and flagging the subsequent drop on the aliased path.
  Listing 7 Ownership Duplication leading to Double Free in doubly.
 1 pub fn pop_back(&mut self) -> Option<T> {
 2     unsafe {
 3         if self.length == 0 {
 4              None
 5         } else {
 6              let val = ptr::read(&(*self.last).value); // [1] Ownership duplication
 7              // ... (pointer updates) ...
 8              let old_last = self.last;
 9              // ...
10              drop(mem::transmute::<_, Box<Node<T>>>(old_last)); // [2] Drop box implicitly drops value (Free #1)
11              Some(val) // [3] Caller drop causes Free #2
12         }
13     }
14 }


     Case 4: Out-of-Bounds in auto_vec. We identified an Out-of-Bounds (OOB) vulnerability in
  the iterator implementation of auto_vec, a vector implementation with automatic child removal.
  As shown in Listing 8, the iter method initializes the iterator by calculating a current pointer
  that points before the start of the backing array. It computes (&children[0]).sub(1), intending
  to increment it back to the start in the first call to next(). However, in Rust (and LLVM), per-
  forming pointer arithmetic that moves a pointer outside the allocated object (even momentarily)
  is undefined behavior, unless it points one past the end. Moving before the start is always illegal.
  Our tool detected this via the layout domain, which tracks the pointer offset relative to the base
  object. The operation sub(1) resulted in a negative offset, triggering Rule E-OOB/MA.
  Listing 8 Out-of-Bounds access in auto_vec iterator initialization.
1 pub fn iter(&self) -> Iter<T> {
2     Iter {
3         last: &self.children[self.len() - 1] as *const _,
4         current: unsafe {
5             (&self.children[0] as *const ...).sub(1) // [1] UB: moves ptr BEFORE alloc start
6         },
7         lifetime: PhantomData,
8     }
9}




  6 Discussion
  6.1   Comparison with Baselines
  UnsafeChecker detects potential soundness violations by checking whether unsafe code upholds
  the safety invariants required by its safe APIs within the modeled scope. This goal differs from
  generic bug-finding tools, which focus on localized execution errors (e.g., panics or crashes) rather
  than invalid states escaping through safe boundaries. Baselines provide strong solutions for spe-
  cific bug classes. Rudra is a pattern matcher over unsafe idioms. SafeDrop focuses on deallocation
  bugs by recognizing specific lifetime-ending events. MirChecker applies generic symbolic reason-
  ing over MIR but does not model Rust-specific ownership contracts. In contrast, UnsafeChecker
  restores the semantic context erased by unsafe code. It maintains a shared state with ownership,
  object-validity, and layout components. The value of this design is not that every warning rule
  uses all components at once, but that each rule can consume the facts required by the correspond-
  ing Rust obligation within one flow-sensitive MIR state. Potential soundness violations often span
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                     23


multiple steps and multiple kinds of invariants. For example, the doubly bug (Listing 7) starts from
duplicating a raw pointer and later frees the underlying object. The tracing bug (Listing 3) per-
forms a move-like action (mem::forget(self)) and then dereferences pointers derived from self.
These cases require an analysis to track how ownership transfers and drops affect the liveness of
aliased pointers. Pattern-based checks remain valuable for quickly flagging common misuse pat-
terns, but they are not designed to connect such multi-step interactions. Similarly, layout-related
bugs such as wrflib (Section 5.1) require reasoning about derived pointers and bounds across mul-
tiple statements. By tracking these semantics flow-sensitively, UnsafeChecker can detect complex
violations that evade pattern matchers. Furthermore, to explain potential alarms, UnsafeChecker
retains alternative object-validity states at control-flow joins instead of collapsing them to a coarse
unknown state. For example, the lifecycle domain represents uncertainty as sets of states (e.g.,
{Live, Uninit}), which helps explain potential alarms but does not eliminate path-insensitivity
(Section 5.2).

6.2   Threats to Validity
We identify potential threats to the validity of our experimental results:
   Internal Validity. The accuracy of our evaluation relies on the correctness of our ground truth
and verification process. For Dataset A, we used established CVEs from the RustSec database. For
Dataset B, the lack of ground truth poses a challenge. To mitigate bias in our manual verification,
we use a strict criterion: we treat a warning as a bug only if we can construct an executable PoC
that triggers Undefined Behavior in Miri. This ensures that our reported True Positives are genuine
soundness violations. Another potential threat is the configuration of baseline tools. To ensure fair-
ness, we used their latest stable versions with default configurations. We also minimized libraries
to resolve compilation errors, ensuring a fair comparison with baselines.
   External Validity. Our results on Dataset A (46 CVEs) and Dataset B (83 flagged crates) might
not generalize to all Rust crates. Specifically, our strict inclusion criteria for Dataset A resulted
in a somewhat imbalanced distribution of bug types, which may not perfectly reflect the natural
distribution of unknown bugs found in the wild (Dataset B). However, Dataset A still covers the
most critical categories of memory safety CVEs (e.g., Uninit, OOB, UAF). Furthermore, Dataset B is
drawn from the entire crates.io registry, covering diverse domains from low-level utilities to high-
level applications. While we cannot claim effectiveness on non-public codebases, our evaluation
on the public ecosystem provides strong evidence of UnsafeChecker’s real-world applicability.

6.3   Limitations and Future Work
UnsafeChecker has several limitations, though they do not significantly undermine its effective-
ness in detecting common vulnerabilities. (1) Scope. UnsafeChecker focuses on sequential mem-
ory safety violations and soundness issues. It does not target application-level logic bugs. Addition-
ally, it does not model concurrency or synchronization primitives. As a result, it cannot detect data
races or improper use of Sync/Send traits. However, empirical evidence suggests that sequential
memory safety violations remain the primary source of unsoundness in Rust ecosystems. (2) Preci-
sion and Over-approximation. As a static analyzer, UnsafeChecker uses conservative warning
generation for the modeled cases, which can introduce false positives. At the same time, bounded
inlining, opaque calls, unmodeled APIs, and lost pointer identity can still cause false negatives.
Our layout domain uses interval abstraction for pointer arithmetic, which can be imprecise for
complex non-linear computations (e.g., bitwise operations). Additionally, we handle FFI calls and
deep recursion conservatively by over-approximating their effects. Despite these approximations,
our evaluation demonstrates that UnsafeChecker maintains a practical precision rate. (3) Mod-
eling Scope. Our analysis primarily focuses on modeling key APIs that are critical for memory
24                                                      Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


safety semantics, such as Vec, Box, and raw pointer operations. We do not fully model the entire
Rust standard library, particularly specialized APIs (e.g., custom allocators) or complex interior
mutability patterns (e.g., deep usage of RefCell). However, our targeted modeling strategy cov-
ers the majority of unsafe usage patterns in our datasets, and unmodeled APIs can be supported
with additional engineering effort.
   We identify several promising directions for future research. First, while our framework ef-
fectively targets sequential memory safety, extending it to model concurrency primitives would
broaden its applicability to multi-threaded contexts, such as detecting data races. Second, integrat-
ing more expressive abstract domains could further refine precision in complex pointer arithmetic
involving non-linear constraints. Finally, as the Rust ecosystem evolves, expanding the semantic
modeling of standard library APIs remains an ongoing engineering effort to support emerging safe
abstractions.

7 Related Work

Static Analysis for Unsafe Rust. Several tools analyze Rust code to detect memory safety risks.
Rupta [15] performs context-sensitive pointer analysis on Rust MIR, which provides a foundation
for MIR-level reasoning about pointer behavior. MirChecker [16] applies symbolic execution to
Rust MIR and targets generic bugs such as integer overflows and panics. Rudra [4] uses heuristic
pattern matching to flag risky unsafe constructs and reports issues such as incorrect Vec::set_len
usage and variance-related mistakes. SafeDrop [7] focuses on deallocation bugs (e.g., Use-After-
Free and Double-Free). These tools are effective for specific bug classes but do not directly check
whether a safe API upholds Rust’s safety invariants. In contrast, UnsafeChecker detects potential
soundness violations in safe abstractions by modeling the ownership, object-validity, and layout
facts relevant to its warning rules. Safe4U [14] checks safe encapsulations against contracts mined
from API documentation. We treat it as complementary and exclude it from our baseline compar-
ison.

Rust Semantics and Verification. Stacked Borrows [11] and Tree Borrows [27] define opera-
tional models for Rust aliasing, borrowing, and pointer provenance. These semantics are foun-
dational for explaining when reference and pointer operations are valid. UnsafeChecker has a
narrower and more implementation-oriented goal: it does not attempt to implement a complete
Rust provenance or aliasing semantics. Instead, it tracks the ownership, object-validity, and layout
facts needed by its warning rules over MIR, and treats behaviors outside these models, such as
pointer-integer-pointer round trips and unmodeled library semantics, as outside its current scope.
   RustBelt [12] and Aeneas [10] provide proof-oriented foundations and verification workflows
for Rust programs. Such systems target correctness arguments under explicit semantic models
and specifications. In contrast, UnsafeChecker is an automatic static bug detector for unsafe im-
plementations of safe abstractions: it scales to crate-level analysis and reports potential violations
that can be validated dynamically, rather than proving full Rust semantic correctness.
   Place Capability Graphs [9] are closest in spirit to UnsafeChecker’s ownership reasoning, since
they model permissions and capability changes for Rust places. The scope differs, however. PCG
provides a general-purpose model of Rust’s ownership and borrowing guarantees, whereas Un-
safeChecker combines ownership facts with object-lifecycle and layout facts to detect specific
classes of memory-safety-relevant violations in unsafe safe abstractions. Accordingly, our evalua-
tion measures large-scale bug-finding yield and validation of reported issues, rather than semantic
model coverage or direct verification strength.
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                                        25


Dynamic Analysis and Program Verification Tools. Miri [23] provides a concrete interpreter
for detecting Undefined Behavior in Rust and serves as a ground-truth validator for many analy-
ses, including ours. Its coverage depends on available test inputs. Formal tools such as Kani [5],
Prusti [2], Creusot [8], and Verus [13] can prove properties against specifications, but scaling them
to large codebases with extensive raw-pointer manipulation remains challenging. OOM-Guard [6]
mitigates out-of-memory risks at runtime and is orthogonal to memory corruption.

Development Support and Documentation Analysis. VRLifeTime [30] and Yuga [18] integrate
dataflow analyses into IDEs for lifetime visualization, primarily targeting safe code and explicit
lifetimes. ’R [20] and RustC4 [29] detect inconsistencies between code and documentation, while
rust-code-analysis [1] provides structural metrics. Cargo-call-stack [17] analyzes stack usage for
embedded systems. These tools improve developer workflows but do not directly check soundness
invariants inside unsafe implementations.

8 Conclusion
In this paper, we presented UnsafeChecker, a static analysis framework for detecting potential
soundness violations in Rust safe abstractions. By maintaining ownership, object-validity, and
layout facts in a shared MIR-level state, UnsafeChecker reports both boundary-level contract vi-
olations and instruction-level undefined behavior within its modeled sequential memory-safety
scope. Our evaluation on a dataset of known vulnerabilities demonstrates that UnsafeChecker
significantly outperforms state-of-the-art tools, detecting 36 out of 53 ground-truth bugs with
51.6% alert-level precision. Additionally, UnsafeChecker successfully discovered 114 previously
unknown bugs in popular crates from crates.io, with 45 of them confirmed and 27 fixed by devel-
opers.

References
 [1] Luca Ardito, Luca Barbato, Marco Castelluccio, Riccardo Coppola, Calixte Denizet, Sylvestre Ledru, and Michele
     Valsesia. 2020. rust-code-analysis: A Rust library to analyze and extract maintainability information from source
     codes. SoftwareX 12 (2020), 100635. doi:10.1016/j.softx.2020.100635
 [2] Vytautas Astrauskas, Aurel Bílý, Jonáš Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli, and
     Alexander J. Summers. 2022. The Prusti Project: Formal Verification for&nbsp;Rust. In NASA Formal Methods: 14th
     International Symposium, NFM 2022, Pasadena, CA, USA, May 24–27, 2022, Proceedings (Pasadena, CA, USA). Springer-
     Verlag, Berlin, Heidelberg, 88–108. doi:10.1007/978-3-031-06773-0_5
 [3] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexander J. Summers. 2020. How do
     programmers use unsafe rust? Proc. ACM Program. Lang. 4, OOPSLA, Article 136 (Nov. 2020), 27 pages. doi:10.1145/
     3428204
 [4] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021. Rudra: Finding Memory Safety Bugs
     in Rust at the Ecosystem Scale. In Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles
     (Virtual Event, Germany) (SOSP ’21). Association for Computing Machinery, New York, NY, USA, 84–99. doi:10.1145/
     3477132.3483570
 [5] Twain Byrnes, Yoshiki Takashima, and Limin Jia. 2024. Automatically Enforcing Rust Trait Properties. In Verification,
     Model Checking, and Abstract Interpretation, Rayna Dimitrova, Ori Lahav, and Sebastian Wolff (Eds.). Springer Nature
     Switzerland, Cham, 210–223.
 [6] Chengjun Chen, Zhicong Zhang, Hongliang Tian, Shoumeng Yan, and Hui Xu. 2023. OOM-Guard: Towards Improving
     the Ergonomics of Rust OOM Handling via a Reservation-Based Approach. In Proceedings of the 31st ACM Joint
     European Software Engineering Conference and Symposium on the Foundations of Software Engineering (San Francisco,
     CA, USA) (ESEC/FSE 2023). Association for Computing Machinery, New York, NY, USA, 733–744. doi:10.1145/3611643.
     3616303
 [7] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: Detecting Memory Deallocation Bugs of
     Rust Programs via Static Data-flow Analysis. ACM Trans. Softw. Eng. Methodol. 32, 4, Article 82 (may 2023), 21 pages.
     doi:10.1145/3542948
26                                                                 Xizhe Yin, Yaokun Zhang, Yang Feng, and Baowen Xu


 [8] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022.                             Creusot: A&nbsp;Foundry
     for&nbsp;the&nbsp;Deductive Verification of&nbsp;Rust Programs. In Formal Methods and Software Engineer-
     ing: 23rd International Conference on Formal Engineering Methods, ICFEM 2022, Madrid, Spain, October 24–27, 2022,
     Proceedings (Madrid, Spain). Springer-Verlag, Berlin, Heidelberg, 90–105. doi:10.1007/978-3-031-17244-1_6
 [9] Zachary Grannan, Aurel Bílý, Jonáš Fiala, Jasper Geer, Markus de Medeiros, Peter Müller, and Alexander J. Summers.
     2025. Place Capability Graphs: A General-Purpose Model of Rust’s Ownership and Borrowing Guarantees. Proc. ACM
     Program. Lang. 9, OOPSLA2, Article 344 (2025), 28 pages. doi:10.1145/3763122
[10] Son Ho, Aymeric Fromherz, and Jonathan Protzenko. 2024. Sound Borrow-Checking for Rust via Symbolic Semantics.
     Proc. ACM Program. Lang. 8, ICFP, Article 251 (2024), 29 pages. doi:10.1145/3674640
[11] Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2019. Stacked borrows: an aliasing model for Rust.
     Proc. ACM Program. Lang. 4, POPL, Article 41 (Dec. 2019), 32 pages. doi:10.1145/3371109
[12] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2018. RustBelt: Securing the Foundations of
     the Rust Programming Language. Proc. ACM Program. Lang. 2, POPL, Article 66 (Dec. 2018), 34 pages. doi:10.1145/
     3158154
[13] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
     and Chris Hawblitzel. 2023. Verus: Verifying Rust Programs using Linear Ghost Types (extended version). arXiv
     preprint arXiv:2303.05491 (2023).
[14] Huan Li, Bei Wang, Xing Hu, and Xin Xia. 2025. Safe4U: Identifying Unsound Safe Encapsulations of Unsafe Calls in
     Rust using LLMs. Proc. ACM Softw. Eng. 2, ISSTA, Article ISSTA021 (June 2025), 24 pages. doi:10.1145/3728890
[15] Wei Li, Dongjie He, Yujiang Gui, Wenguang Chen, and Jingling Xue. 2024. A Context-Sensitive Pointer Analysis
     Framework for Rust and Its Application to Call Graph Construction. In Proceedings of the 33rd ACM SIGPLAN Inter-
     national Conference on Compiler Construction (Edinburgh, United Kingdom) (CC 2024). Association for Computing
     Machinery, New York, NY, USA, 60–72. doi:10.1145/3640537.3641574
[16] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John C.S. Lui. 2021. MirChecker: Detecting Bugs in Rust Programs
     via Static Analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security
     (Virtual Event, Republic of Korea) (CCS ’21). Association for Computing Machinery, New York, NY, USA, 2183–2196.
     doi:10.1145/3460120.3484541
[17] Per Lindgren, Nils Fitinghoff, and Jorge Aparicio. 2019. Cargo-call-stack Static Call-stack Analysis for Rust. In 2019
     IEEE 17th International Conference on Industrial Informatics (INDIN), Vol. 1. 1169–1176. doi:10.1109/INDIN41052.2019.
     8972088
[18] Vikram Nitin, Anne Mulhern, Sanjay Arora, and Baishakhi Ray. 2023. Yuga: Automatically Detecting Lifetime Anno-
     tation Bugs in the Rust Language. arXiv:2310.08507 [cs.SE] https://arxiv.org/abs/2310.08507
[19] Miguel Ojeda et al. 2021. Rust for Linux: The path to safe systems programming. Linux Kernel Documentation (2021).
     https://www.kernel.org/doc/html/latest/rust/index.html
[20] Wanrong Ouyang and Baojian Hua. 2021. ′ R: Towards Detecting and Understanding Code-Document Violations in
     Rust. In 2021 IEEE International Symposium on Software Reliability Engineering Workshops (ISSREW). 189–197. doi:10.
     1109/ISSREW53611.2021.00063
[21] Jeff Vander Stoep and Stephen Hines. 2021. Rust in the Android platform. Google Security Blog. https://security.
     googleblog.com/2021/04/rust-in-android-platform.html
[22] The MIRAI Developers. 2024. MIRAI: A Rust mid-level intermediate representation abstract interpreter. https://
     github.com/facebookexperimental/MIRAI. Accessed: 2025-06-20.
[23] The Rust Project. 2025. Miri: An Undefined Behavior Interpreter for Rust. GitHub repository. https://github.com/rust-
     lang/miri
[24] The Rust Project. 2025. The Rust Programming Language. Rust Project. https://doc.rust-lang.org/book/
[25] The Rust Project. 2025. The Rust Programming Language. GitHub repository. https://github.com/rust-lang/rust
[26] The Rust Project. 2025. The Rust Reference. Rust Project. https://doc.rust-lang.org/reference/behavior-considered-
     undefined.html
[27] Neven Villani, Johannes Hostert, Derek Dreyer, and Ralf Jung. 2025. Tree Borrows. Proc. ACM Program. Lang. 9, PLDI,
     Article 188 (2025), 24 pages. doi:10.1145/3735592
[28] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R. Lyu. 2021. Memory-Safety Challenge Con-
     sidered Solved? An In-Depth Study with All Rust CVEs. ACM Trans. Softw. Eng. Methodol. 31, 1, Article 3 (Sept. 2021),
     25 pages. doi:10.1145/3466642
[29] Yichi Zhang, Zixi Liu, Yang Feng, and Baowen Xu. 2024. Leveraging Large Language Model to Assist Detecting Rust
     Code Comment Inconsistency. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software
     Engineering (Sacramento, CA, USA) (ASE ’24). Association for Computing Machinery, New York, NY, USA, 356–366.
     doi:10.1145/3691620.3695010
UnsafeChecker: Finding Soundness Bugs in Rust Safe Abstractions                                               27


[30] Ziyi Zhang, Boqin Qin, Yilun Chen, Linhai Song, and Yiying Zhang. 2020. VRLifeTime – An IDE Tool to Avoid
     Concurrency and Memory Bugs in Rust. In Proceedings of the 2020 ACM SIGSAC Conference on Computer and Com-
     munications Security (Virtual Event, USA) (CCS ’20). Association for Computing Machinery, New York, NY, USA,
     2085–2087. doi:10.1145/3372297.3420024
