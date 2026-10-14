                                                rCanary: Detecting Memory Leaks Across Semi-automated
                                                        Memory Management Boundary in Rust
                                                                              Mohan Cui                                                             Hui Xu∗
                                                                  School of Computer Science,                                          School of Computer Science,
                                                                       Fudan University                                                     Fudan University

                                                                         Hongliang Tian                                                        Yangfan Zhou
                                                                               Ant Group                                               School of Computer Science,
                                                                                                                                            Fudan University
arXiv:2308.04787v2 [cs.SE] 1 Aug 2024




                                        ABSTRACT                                                                     automated deallocation is achieved by inserting the drop() in-
                                        Rust is an effective system programming language that guarantees             struction when each value goes out of the life scope [3]. As a system
                                        memory safety via compile-time verifications. It employs a novel             programming language, Rust enables users to evade automated deal-
                                        ownership-based resource management model to facilitate auto-                location and manage resources themselves, a lower control known
                                        mated deallocation. This model is anticipated to eliminate memory            as semi-automated memory management, to increase flexibil-
                                        leaks. However, we observed that user intervention drives it into            ity. Many companies and open-source projects thus switch to Rust,
                                        semi-automated memory management and makes it error-prone                    such as the web browser engine Servo [4], operating system Redox
                                        to cause leaks. In contrast to violating memory-safety guarantees            OS [5–7], LibOS Occlum [8, 9], and the embedded system Tock
                                        restricted by the unsafe keyword, the boundary of leaking mem-               OS [10–12]. In 2023, Rust has become the second programming
                                        ory is implicit, and the compiler would not emit any warnings for            language in the Linux kernel2 .
                                        developers.                                                                     We observed that the semi-automated memory management
                                           In this paper, we present rCanary, a static, non-intrusive, and           model may introduce memory leaks, such as issues listed in Table 4.
                                        fully automated model checker to detect leaks across the semi-               Studying memory leaks [13–15] is crucial for the system program-
                                        automated boundary. We design an encoder to abstract data with               ming language. If the program consumes a significant quantity
                                        heap allocation and formalize a refined leak-free memory model               of memory but never releases it, the memory usage will continue
                                        based on boolean satisfiability. It can generate SMT-Lib2 format             to rise. Moreover, remote attackers can exploit memory leaks to
                                        constraints for Rust MIR and is implemented as a Cargo compo-                launch a denial-of-service (DoS) attack [16]. Despite numerous
                                        nent. We evaluate rCanary by using flawed package benchmarks                 studies on leak detection for C/C++ programs [17–19], to the best
                                        collected from the pull requests of open-source Rust projects. The           of our knowledge, no work has been conducted for Rust. This scope
                                        results indicate that it is possible to recall all these defects with        includes FFIChecker [20] because it uses LLVM-IR to check for
                                        acceptable false positives. We further apply our tool to more than           Rust-C FFI. In our latest empirical study on Rust security promise,
                                        1,200 real-world crates from crates.io and GitHub, identifying 19            memory leak emerged as a member in a categorization of safety
                                        crates having memory leaks. Our analyzer is also efficient, that             requirements [21]. Rust experts rank it fourth out of 19 categories
                                        costs 8.4 seconds per package.                                               in the vote for significance.
                                                                                                                        Leaking memory was not a safe operation from a temporal per-
                                        KEYWORDS                                                                     spective. Until Rust version 1.0, the method of escaping from the
                                                                                                                     ownership model was an unsafe intrinsic (i.e., forget [22]). It was
                                        Memory Leak, Model Check, Semi-automated Memory Manage-
                                                                                                                     later marked as a safe method because it does not violate memory
                                        ment, Boolean Satisfiability, Ownership, Rust
                                                                                                                     safety directly. However, developers may thus find it hard to pin-
                                        ACM Reference Format:                                                        point ownership leaks because this operation is not restricted to the
                                        Mohan Cui, Hui Xu, Hongliang Tian, and Yangfan Zhou. 2024. rCanary:          unsafe scope, and the compiler does not detect it either. According
                                        Detecting Memory Leaks Across Semi-automated Memory Management               to our statistics, semi-automated memory management is preva-
                                        Boundary in Rust. In Proceedings of arxiv pre-print versions (arxiv). ACM,   lently used in the Rust community. As of 2023-01-30, we mined the
                                        New York, NY, USA, 13 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                                                                                                     latest crates from crates.io [23] and discovered that 5,717 reposi-
                                                                                                                     tories out of 103,516 employed this method. Compared to 21,506
                                        1     INTRODUCTION                                                           crates using unsafe keyword [24, 25], the potential vulnerability is
                                        Rust is an emerging programming language that focuses on mem-                a non-trivial problem for us to investigate.
                                        ory safety and efficiency. Ownership-based resource management                  We propose utilizing static analysis to detect leaks that cross
                                        model (OBRM) [1] can ensure memory safety but does not sacri-                the semi-automated boundary. Leak detection employs a taint-sink
                                        fice performance via static analysis. It is a prominent design of            approach: the object created at the tainted site (construction) must
                                        zero-cost abstractions [2]. Specifically, Rust employs non-lexical           reach the sink site (destruction) [26]. There are two types of exist-
                                        lifetime (NLL) to deduce the minimum lifespan of each value1 . Thus,         ing static approaches: iterative data-flow analysis [27] and sparse
                                        ∗ Corresponding author.
                                        1 https://rust-lang.github.io/rfcs/2094-nll.html                             2 https://lore.kernel.org/lkml/20210414184604.23473-1-ojeda@kernel.org/
arxiv, 2024,                                                                                  Mohan Cui, Hui Xu, Hongliang Tian, and Yangfan Zhou


value-flow analysis [28]. To our knowledge, the current work is in-    the resource is acquired during the initialization and released dur-
effective for Rust. The former monitors the values at each program     ing the destruction, ensuring proper resource management and
point throughout the control flow, which is flow-sensitive. How-       preventing leaks. In the ownership model, when the user initial-
ever, it lacks support for Rust syntax, such as ownership movement.    izes a value, the compiler will calculate the program point to in-
The latter tracks the values sparsely from the define-use chains       sert the drop() instruction and release the resource [1]. This in-
or the single static assignment (SSA) [29]. It is more efficient but   struction typically binds to object variables that implement Drop
flow-insensitive. The sparse representation does not check arbi-       trait [33], and the object is called owner of the resource (e.g.,
trary state-machine properties for all program paths. In addition,     Vec<T> [34]). Rust enables users not to instruct the automated deal-
some work infers the owner for C/C++ programs based on boolean         location that triggers semi-automated management. The escape
satisfiability [30], but it needs to be aligned with the ownership     hatch is ManuallyDrop<T> [35], a zero-cost wrapper that prevents
design.                                                                the compiler from calling T’s destructor. Once the object is encapsu-
   This paper introduces rCanary, a static, non-intrusive, and         lated in ManuallyDrop, it becomes an orphan object. As a smart
fully automated model checker to detect leaks across the semi-         pointer, ManuallyDrop can be dereferenced to disclose the generic
automated boundary. It consists of an encoder to transform value       field &T, which can then be cast into the raw pointer *T.
based on its type and leverages a refined leak-free model over            ManuallyDrop<T> is a customizable design for toggling between
the ownership model. The encoder can convert the typed value           automated deallocation and manual release. However, this design is
into a bit vector to simulate construction. The element of the bit     vulnerable to leaks if the programmers neglect to release them. In
vector indicates which field contains heap allocation. The leak-free   today’s Rust ecosystem, user intervention is a significant cause of
model is composed of formal rules based on boolean satisfiability      leaks. In this paper, we summarize two typical leak patterns across
to trace the deallocation. Our analyzer uses the encoder and formal    semi-automated boundaries: (i) orphan object missing drop() in-
rules to generate constraints for Rust MIR in SMT-Lib2 syntax [31],    struction in Mid-level Intermediate Representation (MIR); (ii) proxy
forming a 0–1 integer equality list. We implemented rCanary            type missing manual field deallocation in its Drop implementation.
as an external component in Cargo and applied it to the existing       They will be discussed in Sections 2.2 and 2.3.
flawed pull-request benchmarks collected from GitHub. The result
                                                                          Definition 2.1 (Heap Item, Rtoken). A heap item is an object
demonstrates that it can recall all the issues that match our leak
                                                                       containing the heap allocation with a fixed type (layout). It has an
pattern and identify 19 crates with memory leaks in real-world Rust
                                                                       exclusive rtoken to monitor the deallocation, and the rtoken can be
crates.
                                                                       transferred among variables through the data flow.
   Our main contributions are summarized as follows:
                                                                           If one object escapes from the ownership model, we expect
• We studied the issues of memory leaks across the semi-automated      pointer types (including raw pointers * and references &) to be
  memory management boundary in Rust and outlined two bug              responsible for deallocating them. As illustrated in Figure 1a, this
  patterns. We developed algorithms to identify them: an encoder       paper assumes that each value has an RAII token (rtoken) to mon-
  to abstract data having heap allocation and a leak-free memory       itor its deallocation and the definition is provided in Defition 2.1.
  model based on formal rules.                                         If the object possesses the rtoken, its identity is equivalent to the
• We implemented rCanary, a static, non-intrusive, and fully au-       owner. The primary distinction is that pointer types can hold the
  tomated model checker that can detect leaks for Rust packages. It    rtoken but can never be the owner.
  provides user-friendly diagnostics to pinpoint the buggy snippet.
  rCanary is open-sourced and can be modified for other research.      2.2    Motivating Example: Orphan Object
• We evaluate the effectiveness, usability, and efficiency of rCa-
                                                                       Creating an orphan object eliminates its drop() instruction in Rust
  nary. It can recall all bugs in the benchmark collected from
                                                                       MIR. Listing 1 illustrates an example of an orphan-object leak, and
  GitHub and discover 19 crates with memory leaks in open-source
                                                                       we will give the definition below.
  Rust projects. It is also capable of executing fast scans for the
  Rust ecosystem.                                                         Definition 2.2 (Orphan Object). An orphan object is the heap
                                                                       item wrapped by the smart pointer ManuallyDrop.
   We first present the root causes of memory leaks in the own-
ership model and illustrate two bug patterns (§2). Then overview          In Listing 1, we first construct a heap item Box<&str> by using
the system architecture of the analyzer because our algorithm has      Box::new (line 2). The initial holder of its rtoken is buf. The method
two critical components (§3). We detail how to abstract data and       ManuallyDrop::new takes the heap item and encapsulates it with
construct values (rtoken) in our model, an encoder that generates      ManuallyDrop that creates an orphan object (line 5). Then, we
bit vectors based on types (§4) and present a leak-free model, ex-     dereference it and cast it as a raw pointer. The rtoken is thus handed
plaining how resources be used to detect memory leaks (§5).            to ptr. From the ownership perspective, this line consumes the
                                                                       owner, restrains deallocation, and creates a raw pointer for further
2 PROBLEM STATEMENT                                                    usage.
                                                                          As depicted in Figure 1a, variable b is an owner and holds a rtoken
2.1 Why Leaks in the Ownership Model?                                  of the heap item. It can release the resource when its lifetime ends.
The Rust ownership model is derived from the programming id-           The pointers p1 and r1 merely point to the heap item and would not
iom Resource Acquisition Is Initialization (RAII) [32] used in C++,    free it. In contrast, the heap items pointed by p2 and r2 are orphan
where resources are acquired and released by objects. Specifically,    objects as they do not have owners. Thus, the poniters should act
rCanary: Detecting Memory Leaks Across Semi-automated Memory Management Boundary in Rust                                                                       arxiv, 2024,




          Stack Frame                                Heap Item                                                                         Leak Patterns



                                                                                                                  Assign to Variable                   Need:
                                                                              Escape from Ownership Model:                                             Manually Release
                                                                              Wrap arguments by ManuallyDrop
                                                                  （unused）    e.g., Box::into_raw( ), forget( )

         p2: pointer (field)                                                                                                                           Need:
                                                                                                                  Assign to Field
                                                                                                                                                       Manually Release
           r2: reference                                                                                                                               in Drop impl
            p1: pointer
           r1: reference
             b: Box<_>                                                                                            Retake the Inner
                                                                                                                                                       Automated Drop




               (a) The holder of the rtoken for the heap item.               (b) The assignments that cause the orphan-object and proxy-type leak.

Figure 1: The relationship between rtoken, Rust owner, and heap item. In Figure 1a, the rtoken holders can be objects, refer-
ences, and pointers. The stack frame and heap chunks reflect the real data storage. When an object exists, the object holds the
rtoken (solid), while other pointers only point to it (dotted). If the object does not exist, pointer types hold the rtoken (solid).
In Figure 1b, the first argument of each method is wrapped with ManuallyDrop in the function body.


        Listing (1) Motivating example of orphan-object leak.                    2.3          Motivating Example: Proxy Type
 1   fn main() {                                                                 The proxy-type issue is caused by the unsound implementation of
 2       let mut buf = Box::new("buffer");                                       the Drop trait for the user-defined type, which is a mutated problem
 3       // heap item 'buf' becomes an orphan object
 4       let ptr =                                                               of the orphan-object leak. The proxy type is defined below.
 5           &mut *ManuallyDrop::new(buf) as *mut _;
 6       // leak by missing free operation on 'ptr'
                                                                                   Definition 2.3 (Proxy Type). A proxy type is a compound type
 7   +   unsafe { drop_in_place(ptr); }                                          having at least one field that stores an orphan object.
 8   }
                                                                                    Listing 2 shows a leak caused by the proxy type Proxy<T> (line 4).
                                                                                 After creating an orphan object Box<&str>, ptr is assigned to the
         Listing (2) Motivating example of proxy-type leak.                      field of a Proxy<T> object (line 15). However, the default Drop im-
 1   struct Proxy<T> {                                                           plementation is ignorant that the field ptr ought to be deallocated.
         ptr: *mut T,
                                                                                 Consequently, it may trigger a memory leak whenever a Proxy<T>
 2
 3   }
 4   impl<T> Drop for Proxy<T> {                                                 object is dropped. To solve this issue, we manually free the raw
 5       fn drop(&mut self) {                                                    pointer by calling drop_in_place on the field (line 7).
 6       // user should manually free the field 'ptr'
 7   +      unsafe { drop_in_place(self.ptr); }                                     As depicted in Figure 1b, if an orphan object is assigned to a field,
 8       }                                                                       although the compiler will append drop() to the proxy type, pro-
     }
 9
10   fn main() {
                                                                                 grammers are responsible for implementing a sound Drop method
11       let mut buf = Box::new("buffer");                                       to release its fields explicitly.
12       // heap item 'buf' becomes an orphan object                                These patterns can encompass primary scenarios caused by the
         let ptr =
                                                                                 lack of manual deallocation towards ManuallyDrop values, with
13
14           &mut *ManuallyDrop::new(buf) as *mut _;
15       let proxy = Proxy { ptr };                                              the difference of having drop() instructions in Rust MIR. Because
16       // leak by missing free 'proxy.ptr' in drop                             the place where a value is assigned can be variables and fields, even
17   }
                                                                                 valid for globals. The limitation is that we do not support some
                                                                                 complex data structures, such as storing orphan objects in static
Figure 2: Motivating examples of orphan-object and proxy-                        arrays or dynamic vectors.
type issues detected in rCanary, caused by the lack of man-
ual deallocation towards ManuallyDrop values.                                    3       DESIGN
                                                                                 This section overviews the design goals and presents the system
                                                                                 architecture of rCanary.

as the rtoken holder to release the resources. Figure 1b summarizes              3.1          Design Goals
the workflow: if the orphan object is assigned to another variable,              As with most existing static analysis analyzers, rCanary ana-
it will be leaked if the programmer does not release the resource                lyzes a source code representation [37–39]. We propose combining
explicitly. The fixed snippet employs drop_in_place [36] to free                 data-flow analysis and boolean satisfiability to design a static, non-
the heap item (line 7), indicating that ptr is the holder to free the            intrusive, and fully automated model checker on top of the Rust
resource and delete the rtoken in deallocation.                                  MIR. We have three design goals:
arxiv, 2024,                                                                                                          Mohan Cui, Hui Xu, Hongliang Tian, and Yangfan Zhou


                    CLI Interface                                                       Table 1: The Rust type classification in the encoder.
         Rust            CLI
                                          Contexts
       Package        Options
                                                                                                                                Encoding Representation
                    Hybraid Analyzer                                             Classification              Type                                                           Example
                         Encoder: Type System                                                                                Default      Length       Data Flow
    Cargo / rustc
                               Type Collector               Model Checker                                  Boolean              [0]           1               -         true, false
       Rust HIR
                                                                                      Primitive            Numeric              [0]           1               -         i8, u16, isize
                             ADT-DEF Analysis
                                                                                                            Texual              [0]           1               -         char, str
                                                     Z3: Constraint Builder
                               Type Encoding
       Rust MIR                                                                                             Array                E            1         Ctor / Ctx      [i32;1]
                                                            Graph Traversal
                                                                                                            Struct               E          Fixed       Ctor / Ctx      Vec<T>
                         Compiler: Rust MIR
        LLVM                                               Constraint Builder                            Enumerate               E          Fixed       Ctor / Ctx      Option<T>
                               Function Body                                                                                     E          Fixed       Ctor / Ctx      MaybeUninit<T>
       Backend                                                                          Object              Union
                                                           Constraints Solver                               Tuple                E          Fixed       Ctor / Ctx      (i32, String)
                            Control-Flow Graph
                                                                                                         Trait Object           [1]           1         Ctor / Ctx      dyn Clone+Copy
       lib / bin                                             Bug Reporter
                              Traversal Order                                                             Parameter             [1]           1         Definition      T, A, S
                                                                                                            Slice               [0]         Fixed            Ctx        &str, &[i32;1]
                                                                                       Pointer            Reference             [0]         Fixed            Ctx        & _, &mut _
         Figure 3: The system architecture of rCanary.                                                   Raw Pointer            [0]         Fixed            Ctx        *const _, *mut _
                                                                                    1 Abbreviation: E: Type Encoding, Ctor: Constructor, Ctx: Context.
                                                                                    2 The classification is from Rust reference but partially modified in this paper.
                                                                                    3 The parameter types (generics) are defined in signatures with no constructors.
                                                                                    4 Zero-sized types (ZSTs) are object types not listed in this table. Our encoder regards ZSTs as zeroed-
                                                                                      length vectors ([ ]), and the operations are optimized as NOP in Z3.
• Abstraction. rCanary focuses on heap values. It needs to recog-
  nize the values with heap allocation and encode them in a proper
  format for model check. The method should support the primary                 type definitions and then uses the result to accelerate encoding for
  features of Rust types, such as generics, mono-morphizations,                 mono-morphizations.
  etc. We chose the MIR variable (a.k.a. local) as the target because
                                                                                3.2.3 Model Checker. The second part is a model checker. We
  it retains type information and passes type checks.
                                                                                design a leak-free memory model consisting of formal rules to
• Usability. rCanary is designed as a general static analyzer for
                                                                                detect leaks, which are flow-sensitive and field-sensitive. The model
  Rust projects. It should analyze each crate within a Rust package
                                                                                checker uses the hybrid analyzer to get the encoder and metadata
  iteratively and report potential leaks across the semi-automated
                                                                                of Rust MIR. It can encode values to generate the Z3 variables and
  boundary. As an external component of the Rust toolchain, it
                                                                                apply formal rules for statements to generate the Z3 assertions.
  should support Cargo projects and provide a user-friendly in-
                                                                                Finally, the solver will be activated to solve constraints and the bug
  terface. The workflow should be fully automated, and no user
                                                                                reporter will emit issues with code spans for developers.
  annotation is required.
• Efficiency. rCanary is based on the theory of boolean satisfia-
                                                                                4       ENCODER: DATA ABSTRACTION
  bility. It traverses MIR functions to generate constraints and em-
  ploys SMT solver Z3 [40] to solve those constraints. The compu-               This section introduces the approach to constructing rtoken. It
  tation overhead should be seriously considered. It should balance             is an encoder that depicts data abstraction based on Rust types.
  precision and efficiency to achieve a fast scan for the large-scale           The encoder can identify heap items and transform them into bit
  project, even for the Rust ecosystem.                                         vectors.

                                                                                4.1         Data Abstraction
3.2      System Architecture
                                                                                A Rust project contains a set of types among all its variables. As
The framework of rCanary consists of three components: the CLI
                                                                                shown in Table 1, the Rust types can be classified into primitives,
interface, the hybrid analyzer, and the model checker, as shown in
                                                                                objects, and pointers [42]. The object types have a set of construc-
Figure 3.
                                                                                tors and a unique destructor. The constructor can be a function with
3.2.1 CLI Interface. The front end is a CLI program installed in the            a list of arguments (e.g., Vec::new [43]) or the local initialization.
toolchain. We implemented rCanary as an external component                      The destructor is the unique Drop implementation associated with
that can be invoked as a subcommand for Cargo. We provide sec-                  this type.
ondary configurations to enhance customization but not impede                       Each type has a rtoken constructor to illustrate the data ab-
compilation settings. It will be invoked after parsing the CLI param-           straction in the fully initialized state. The rtoken is represented as a
eters and initializing the configurations. The compilation metadata             fixed-length bit vector. Its member can take on values 𝜎 ∈ {−1, 0, 1}.
will be emitted after all MIR passes are finished. After analysis, the          These elements become the lifted boolean values [40], where 𝜎 = −1
bug reporter will notify users of potential leaks with bug locations.           is an uninitialized value, 𝜎 = 1 is holding a heap item, and 𝜎 = 0
                                                                                is the opposite (including not holding a heap item, stack-allocated
3.2.2 Hybrid Analyzer. The first component of the backend is a                  value, freed value or moved value). The lifted boolean values form
hybrid analyzer developed on top of Rust MIR. It evaluates the                  a semi-lattice [44]: the top element ⊤ is −1, and the bottom ele-
node order of the control-flow graph and employs the Tarjan algo-               ment ⊥ is 0. We separate Rust types into enumeration types (e.g.,
rithm [41] to eliminate loops. To model heap values, we designed                IpAddr [45]) and others (e.g., Vec [34]), because different variants
an encoder that can transform arbitrary types into fixed-length bit             in enum types can carry different types of data [42]. Thus, we define
vectors. It is efficient with linear complexity. It first analyzes the          the rtoken as below:
rCanary: Detecting Memory Leaks Across Semi-automated Memory Management Boundary in Rust                                                      arxiv, 2024,


 Algorithm 1: Encoder: Construct the rtoken for the given                       adtdefs (line 2). Those types are located not only in the local crate
 type in the fully-initialized state, represented as a fixed-                   but also in dependencies. Then we traverse each type and extract
 length bit vector.                                                             the definition of compound types by using ExtractAdtDefs (line 3).
                                                                                Finally, fields are flattened, so we can generate a dependency graph
     Input: mir: mir body of given function                                     of AdtDefs depG in AnalyzeDependencies (line 4). Since Rust re-
     Output: cache: cache of AdtDef analysis results                            stricts recursion in compound types, it still permits recursion in
1  Function AdtDefAnalysis(mir)                                                 GenericArgs (e.g., Vec<Vec<i32> >). Thus, we break the recursion
 2    tys ← CollectTypes(mir)                                                   within GenericArgs and construct a directed acyclic graph (DAG).
 3    adtdefs ← ExtractAdtDefs(tys)                                             AdtDef and GenericArgs. We will analyze if each type is a heap
 4    depG ← AnalyzeDependencies(adtdefs)                                       item or is able to become one in mono-morphizations. It is crucial
 5    cache ← ∅                                                                 to define the form of the heap item and tackle the generics. The
 6    foreach depCC in depG do                                                  heap-item unit in Definition 4.2 is the identity of heap items derived
 7        depQueue ← InverseToposort(depCC)                                     from the collection types in the standard library. PhantomData [48]
                                                                                is the marker that informs the compiler that one type is a container
 8        foreach adtdef in depQueue do
                                                                                and stores the typed value on the heap. If it is held by a flattened
 9            result.heap_item ← hasHeapItemUnit(adtdef )
                                                                                type, at least one field is allocated on the heap. In Definition 4.3, the
10            result.isolated_parameter ←
                                                                                isolated parameter demonstrates whether a generic parameter can
               hasIsolatedParameter(adtdef )
                                                                                be further mono-morphized as a heap item. If an isolated parameter
11            cache ← result
                                                                                mono-morphizes into a heap-item type, this mono-morphization
12      return cache                                                            will generate a heap item.

   Input: ty: type metadata in MIR                                                  Definition 4.2 (Heap-item Unit). A heap-item unit has a
   Output: bool: the result of field encoding                                   PhantomData<T> field with a typed generic parameter and a pointer
13 Function EncodeField(ty)                                                     field to store the value T.
14    if hasHeapItemUnit(ty.adtdef ) then
                                                                                   Definition 4.3 (Isolated Parameter). An isolated parameter
          return TRUE
                                                                                is a stand-alone and typed generic parameter (e.g., T but not &T).
15

16      foreach generic in ty.genericargs do
17         if isIsolatedParameter(generic) then                                 Result Solving. For each connected component depCC, we use
18             return EncodeField(generic)                                      InverseToposort to compute the subgraph’s inverse topological
                                                                                order (line 7). We will recursively search whether each AdtDef
19      return FALSE                                                            contains the heap-item unit and the isolated parameter (lines 9, 10).
                                                                                The result comprises two parts: (i) a boolean value indicating if
                                                                                it contains a heap item; (ii) a boolean vector indicating if each
                                                                                generic parameter is an isolated parameter (e.g., the result of the
   Definition 4.1 (Rtoken). For the non-enumeration type, rtoken
                                                                                vector Vec<T,A> [34] is (1) [0, 1], as shown in Figure 4). It can be
is a fixed-length bit vector. Each member denotes whether this ini-
                                                                                simplified by using inverse topo-order. We first determine whether
tialized field is a heap item. For the enumeration type, if its variance
                                                                                each field is a heap-item unit or an isolated parameter. If neither, we
can be determined, rtoken is a fixed bit vector of its associated data.
                                                                                can read from the successive node to identify if this field contains
Otherwise, the extent is zeroed (unknown).
                                                                                a heap-item unit or isolated parameter directly. Furthermore, the
   This data abstraction is field-sensitive as it uses the member               results are cached as one AdtDef being analyzed (line 11).
inside the bit vector to simulate the field. Notably, it disregards
the alignment and focuses on the field index; namely, the index                 4.3    Type Encoding: Rtoken Constructor
corresponds to the field order specified in the type definition. Enu-           The encoder constructs the rtoken as a bit vector by iteratively call-
meration types require a variance index (i.e., discriminant) as the             ing function EncodeField (line 13) on each field to decide whether
length of the rtoken generated by different variants may be differ-             this field is a heap item in the fully initialized state. As the type
ent. If the discriminant is lost, the rtoken is unknown. This rule can          of the field consists of AdtDef and GenericArgs, the encoder first
be applied to compound types that have enumeration fields.                      queries the cache whether the AdtDef has a heap item unit (line 14).
                                                                                If not, it will search for each isolated parameter available and verify
4.2     ADT-Definition Analysis                                                 if its GenericArg projects to a heap-item type recursively (line 17).
ADT-Definition [46] (AdtDef) analysis determines the possibility                    We present an example in Figure 4. The rtoken constructor of
of a defined type becoming the heap item when fully initialized.                String [49] is [1]. Our algorithm analyzes its field and finds it is
The algorithm is in Algorithm 1.                                                a mono-morphization on Vec. Since Vec<T, A> contains a heap-
Preprocessing. An arbitrary type consists of a type definition (Adt-            item unit, the result of String is [1] with no need to handle the
Def [46]) and a list of the generic arguments (GenericArgs [47]). For           generics. Likewise, the rtoken constructor of Vec<u8,Global> is
instance, Vec<i32> consists of the AdtDef Vec<_> and the generic                [1, 0]. Our algorithm first analyzes the field RawVec and finds that
argument i32. In preprocessing, we invoke an inter-procedural                   it contains a heap-item unit. It then analyzes the second field usize
visitor CollectTypes to collect all encountered types into the set              and concludes the result of the second field is 0.
arxiv, 2024,                                                                                                               Mohan Cui, Hui Xu, Hongliang Tian, and Yangfan Zhou


                    Adt-Def Analysis:         Result:(0) [A:1]
                                                                                                       Property 5.4. The type associated with the rtoken is fixed across
                    Vec<T,A>                        alloc: A                                        statements and function calls.
                       Result:(1) [T:0,A:1]   Result:(1) [T:0]            Result:(0) [T:0]              Property 5.1 ensures that the rtoken is exclusive at each program
    Vec<T,A>             raw: RawVec<T,A>        ptr: Unique<T>             pointer: const* T
                                                                                                    point. Like Rust owner, rtoken can be transferred through state-
AdtDef Result:
(1) [T:0,A:1]          Result:(0) [-]         Result:(0) [-]              Result:(0) [T:0]          ments and functions, but the holder is extended to pointer types
                            len: usize             cap: usize             _marker: PhantomData<T>
                                                                                                    (i.e., references and raw pointers). Property 5.2 indicates that each
                                                                                                    heap item must execute its destructor at the end of its lifetime to
                   QUERY
               Adt-Def Result                                                                       release the resource, but it cannot guarantee that the deallocation
                                                                            AdtDef Result:          method will free all required fields. This deficiency is remedied by
                                                                            (1) [-]
                                                                                                    Property 5.3, which improves the soundness of the Drop implemen-
     String             vec: Vec<u8,Global>   mono-morphization: u8
                                                                            Encoding:               tation. Noncompliance with Property 5.2 is the primary cause of
                    Type Encoding:                                          [1]
                    String
                                              mono-morphization: Global
                                                                                                    orphan-object leaks, while Property 5.3 targets proxy-type issues.
                                                                                                        Property 5.4 is an additional requirement. Table 2 lists the core
                                                                                                    syntax of Rust MIR for leak detection [2, 51, 52]. As in Table 2, ad-
Figure 4: Example of the encoder, including AdtDef anal-
                                                                                                    dressing has two distinct forms, Reference and AddressOf, which
ysis for Vec<T,A> and type encoding for String. The types
                                                                                                    create a reference and a raw pointer, respectively. The syntax for
have been flattened, forming a directed acyclic graph (DAG).
                                                                                                    dereferencing is in Place item. The pointer types represent the
Results are propagated forward using reverse topological
                                                                                                    types of pointed places (e.g., &Vec<u8>) but can be cast easily. This
sorting.
                                                                                                    property aims at restricting the ambiguity among pointee places.
                                                                                                    Since rtokens are constructed by the typed encoder, the type held
   This algorithm is efficient, and the maximal time complexity                                     by pointers is fixed in 𝐻 and can be inferred through contexts. The
is 𝑂 (𝑓 𝑑), where 𝑓 is the maximum size among fields and 𝑑 is the                                   default rtoken constructor for pointer types is [0], so pointers can-
maximum depth among GenericArgs. AdtDef analysis accelerates                                        not be the holder without contexts. Property 5.4 simplifies pointer
encoding via a cached hash table. It is exempt from searching in                                    access by binding each variable with a fixed type. Thus, we do
fields recursively or suffering from various mono-morphizations.                                    not need to distinguish objects and pointers (i.e., addressing and
Trait objects and parameters are conservatively regarded as heap                                    dereferencing).
items, as shown in Table 1. At last, the rtoken constructors of the
pointer types are always 0®, and they should be inferred from the                                   5.2    Assignment Rules
context as explained in Section 5.                                                                  5.2.1 Graph Traversal. Functions are represented as control flow
                                                                                                    graphs in MIR, which are directed graphs composed of basic blocks
5     LEAK-FREE MODEL: FORMAL RULES                                                                 as nodes and control flows as edges. rCanary will extract each
In this section, we present a refined memory model consisting of                                    function in the project, excluding dependencies, as the entry to start
formal rules that can be applied to generate constraints on top of                                  the analysis. We employ the Tarjan algorithm [41] to separate each
Rust MIR to detect leaks across the semi-automated management                                       strongly connected component (SCC) into DAG, then calculate the
boundary.                                                                                           topological order for each DAG. In each node, we will analyze the
                                                                                                    statements from the top-down order, which is flow-sensitive. Once
5.1      Leak-free Typed Memory Model                                                               it encounters a node with multiple predecessors, it will merge the
                                                                                                    states of all preceding nodes using 𝜙 operation [44]. Since the 𝜙
Each heap item has a unique rtoken to monitor the deallocation as
                                                                                                    function is monotonic, the algorithm will traverse loops for one
soon as it is constructed. The refined leak-free model has the form:
                                                                                                    time; namely, each node generates constraints only once. As it is not
                            𝐻 ; 𝑀; 𝐶 ⊢ 𝑠 ⇒ 𝑀 ′ ; 𝐶 ′                                                an iterative dataflow analysis approach, we do not need to reach the
   𝐻 is the set of the heap items bounded with Rust types, 𝑀 is                                     fixed point in iterations; instead, we only focus on the transferring
a mapping of holder candidates for each rtoken in each program                                      of rtokens. Once all the nodes have been analyzed, the generation
point, and 𝐶 is a set of constraints. After analyzing a statement,                                  phase terminates. So we obtain a set of constraints, that are SMT
this model will update the mapping 𝑀 ′ and the constraint set 𝐶 ′ .                                 expressions and will be solved by Z3 solver.
Our leak-free model is monotonic [50] as the bit vector becomes a
                                                                                                    5.2.2 Syntactic Rules. All the assignments connect Place with
semi-lattice [44]. In this model, a leak-free function should satisfy
                                                                                                    Rvalue in Rust MIR. move (explicit) and copy (implicit) are different
the following properties:
                                                                                                    semantics [42] with distinct rules. Due to space constraints, we only
  Property 5.1. There exists one and only one rtoken for each                                       describe two representative rules.
heap item allocated but not deallocated.                                                            move Syntax. The rule for move syntax is 𝐴𝑆𝐺𝑁 𝑀. 𝜎®𝑥 , 𝜎®𝑦 represent
                                                                                                    the prior states of whether variables 𝑥 and 𝑦 hold the rtoken, which
   Property 5.2. Every heap item except the return value must                                       are stored in 𝑀. 𝜎®𝑥 ′, 𝜎®𝑦 ′ are the posterior states (new); term new
execute drop() to free the rtoken before return.                                                    represents the new states after executing the statement and these
    Property 5.3. The drop() instruction must free all necessary                                    states do not exist in 𝑀 until the constraint building of this state-
fields.                                                                                             ment is finished. If the rvalue carries the rtoken, the holder should
                                                                                                    be explicitly switched to the lvalue. move indicates that the rvalue
rCanary: Detecting Memory Leaks Across Semi-automated Memory Management Boundary in Rust                                                                                                                   arxiv, 2024,

                                                                                                                                         n     o
                             [𝑀𝐸𝑅𝐺𝐸 𝜙 ]     𝑀 ⊢ ∀𝑥:𝜎®𝑥 𝜎®𝑥 ′ new 𝐶 ′ =𝐶∧ {𝜎®𝑥 ′ =∩𝑖 }             [𝑅𝐸𝑇 𝑈 𝑅𝑁 ]   𝑀 ⊢ ∀𝑥:𝜎®𝑥 𝐶 ′ =𝐶∧ 𝜎®𝑥 =0®
                                               𝐻 ; 𝑀; 𝐶 ⊢ 𝜙 (𝑥 ) ⇒ 𝑀 [𝑥↦→𝜎®𝑥 ′ ] ; 𝐶 ′                              𝐻 ; 𝑀; 𝐶 ⊢ return ⇒ 𝐶 ′
                                        [𝐴𝑆𝐺 𝑁 𝑀 ]   𝑀 ⊢ 𝑥:𝜎®𝑥 , 𝑦:𝜎®𝑦 𝜎®𝑥 ′ , 𝜎®𝑦 ′ new 𝐶 ′ =𝐶∧{ 𝜎®𝑦 =0® }∧{ 𝜎®𝑥 ′ =0® }∧{ 𝜎®𝑦 ′ =𝜎®𝑥 }
                                                                 𝐻 ; 𝑀; 𝐶 ⊢ 𝑦=move 𝑥 ⇒ 𝑀 [𝑦↦→𝜎®𝑦 ′ , 𝑥↦→𝜎®𝑥 ′ ]; 𝐶 ′
                                 [𝐴𝑆𝐺 𝑁 𝑀 −𝑅𝐸𝐴𝐷𝐹 ]    𝑀 ⊢ 𝑥 .𝑓 :𝜎 𝑓 , 𝑦:𝜎®𝑦 𝜎 𝑓′ , 𝜎®𝑦 ′ new 𝐶 ′ =𝐶∧{ 𝜎®𝑦 =0® }∧{𝜎 𝑓′ =0}∧{ 𝜎®𝑦 ′ =Ext(𝜎 𝑓 ) }
                                                                      𝐻 ; 𝑀; 𝐶 ⊢ 𝑦=move 𝑥 .𝑓 ⇒ 𝑀 [𝑦↦→𝜎 𝑦′ , 𝑥 .𝑓 ↦→𝜎 𝑓′ ]; 𝐶 ′
                                [𝐴𝑆𝐺 𝑁 𝑀 −𝑊 𝑅𝐼𝑇 𝐸𝐹 ]   𝑀 ⊢ 𝑥:𝜎®𝑥 , 𝑦.𝑓 :𝜎 𝑓 𝜎®𝑥 ′ , 𝜎 ′ new 𝐶 ′ =𝐶∧{𝜎 𝑓 =0}∧{ 𝜎®𝑥 ′ =0® }∧{𝜎 𝑓 =Srk(𝜎®𝑥 ) }
                                                                                         𝑓
                                                                        𝐻 ; 𝑀; 𝐶 ⊢ 𝑦.𝑓 =move 𝑥 ⇒ 𝑀 [𝑦.𝑓 ↦→𝜎 𝑓′ , 𝑥↦→𝜎®𝑥 ′ ]; 𝐶 ′
                                     [𝐴𝑆𝐺 𝑁 𝑀 −𝐹𝑇 𝑂𝐹 ]      𝑀 ⊢ 𝑥 .𝑓 :𝜎𝑥 , 𝑦.𝑓 :𝜎 𝑦 𝜎𝑥′ , 𝜎 𝑦′ new 𝐶 ′ =𝐶∧{𝜎 𝑦 =0}∧{𝜎𝑥′ =0}∧{𝜎 𝑦′ =𝜎𝑥 }
                                                                    𝐻 ; 𝑀; 𝐶 ⊢ 𝑦.𝑓 =move 𝑥 .𝑓 ⇒ 𝑀 [𝑦.𝑓 ↦→𝜎 𝑦′ , 𝑥 .𝑓 ↦→𝜎𝑥′ ]; 𝐶 ′
                               [𝐴𝑆𝐺 𝑁 𝐶 ]    𝑀 ⊢ 𝑥:𝜎®𝑥 , 𝑦:𝜎®𝑦 𝜎®𝑥 ′ , 𝜎®𝑦 ′ new 𝐶 ′ =𝐶∧{ 𝜎®𝑦 =0® }∧{ { 𝜎®𝑥 ′ =𝜎®𝑥 ∧𝜎®𝑦 ′ =0® }∨{ 𝜎®𝑦 ′ =𝜎®𝑥 ∧𝜎®𝑥 ′ =0® } }
                                                                        𝐻 ; 𝑀; 𝐶 ⊢ 𝑦=𝑥 ⇒ 𝑀 [𝑦↦→𝜎®𝑦 ′ , 𝑥↦→𝜎®𝑥 ′ ]; 𝐶 ′
                       [𝐴𝑆𝐺 𝑁 𝐶 −𝑅𝐸𝐴𝐷𝐹 ]      𝑀 ⊢ 𝑥 .𝑓 :𝜎 𝑓 , 𝑦:𝜎®𝑦 𝜎 𝑓′ , 𝜎®𝑦 ′ new 𝐶 ′ =𝐶∧{ 𝜎®𝑦 =0® }∧{ {𝜎 𝑓′ =𝜎 𝑓 ∧𝜎®𝑦 ′ =0® }∨{ 𝜎®𝑦 ′ =Ext(𝜎 𝑓 )∧𝜎 𝑓′ =0} }
                                                                           𝐻 ; 𝑀; 𝐶 ⊢ 𝑦= 𝑥 .𝑓 ⇒ 𝑀 [𝑦↦→𝜎 𝑦′ , 𝑥 .𝑓 ↦→𝜎 𝑓′ ]; 𝐶 ′
                        [𝐴𝑆𝐺 𝑁 𝐶 −𝑊 𝑅𝐼𝑇 𝐸𝐹 ]   𝑀 ⊢ 𝑥:𝜎®𝑥 , 𝑦:𝜎 𝑓 𝜎®𝑥 , 𝜎 ′ new 𝐶 ′ =𝐶∧{𝜎 𝑓 =0}∧{ { 𝜎®𝑥 ′ =𝜎®𝑥 ∧𝜎 ′ =0}∨{𝜎 ′ =Srk(𝜎®𝑥 )∧𝜎®𝑥 ′ =0® } }
                                                                         ′
                                                                             𝑓                                                     𝑓              𝑓
                                                                            𝐻 ; 𝑀; 𝐶 ⊢ 𝑦.𝑓 =𝑥 ⇒ 𝑀 [𝑦.𝑓 ↦→𝜎 𝑓′ , 𝑥↦→𝜎®𝑥 ′ ]; 𝐶 ′
                           [𝐴𝑆𝐺 𝑁 𝐶 −𝐹𝑇 𝑂𝐹 ]     𝑀 ⊢ 𝑥 .𝑓 :𝜎𝑥 , 𝑦.𝑓 :𝜎 𝑦 𝜎𝑥′ , 𝜎 𝑦′ new 𝐶 ′ =𝐶∧{𝜎 𝑦 =0}∧{ {𝜎𝑥′ =𝜎𝑥 ∧𝜎 𝑦′ =0}∨{𝜎 𝑦′ =𝜎𝑥 ∧𝜎𝑥′ =0} }
                                                                        𝐻 ; 𝑀; 𝐶 ⊢ 𝑦.𝑓 =𝑥 .𝑓 ⇒ 𝑀 [𝑦.𝑓 ↦→𝜎 𝑦′ , 𝑥 .𝑓 ↦→𝜎𝑥′ ]; 𝐶 ′


                                      Figure 5: The intra-procedural rules in the leak-free memory model.


𝑥 is no longer the holder. Thus, the constraint consists of three                                                    Table 2: The core syntax of Rust MIR.
parts: (i) 𝜎®𝑦 = 0®: since it will overwrite 𝑦, 𝜎®𝑦 cannot hold the rtoken
to prevent leaks, which satisfies Property 5.2; (ii) 𝜎®𝑥 ′ = 0®: due to                           Category              Item                  Syntax                                   Description

move syntax, the new state 𝜎®𝑥 ′ is not the holder; (iii) 𝜎®𝑦 ′ = 𝜎®𝑥 : 𝜎®𝑦 ′                       Index
                                                                                                                   BasicBlockId
                                                                                                                     LocalId
                                                                                                                                       𝑏∈Z
                                                                                                                                       𝑙 ∈Z
                                                                                                                                                                    Const index of basic block started with 0.
                                                                                                                                                                    Const index of local started with 0.
will take 𝜎®𝑥 . The last two parts guarantee the exclusiveness of the                                                 DefId            𝑓 ∈Z                         Internal index of function in compiler.

rtoken defined in Property 5.1.                                                                                        Local
                                                                                                                       Type
                                                                                                                                       𝑣 ∈ {𝑣0 , 𝑣1 , ...}
                                                                                                                                       𝑡 ∈ 𝑇 (𝑃 )
                                                                                                                                                                    Variable and temporary in function.
                                                                                                                                                                    Explicit type of local.
copy Syntax. The rule for copy syntax is 𝐴𝑆𝐺𝑁𝐶. Since the rvalue                                   Variable
                                                                                                                       Place           𝑝 = 𝑣 |𝑣.𝑓 |𝑣 [𝑖 ] | ∗ 𝑣     Direct, field, index, deference access to the local.
is still valid, only one of 𝜎®𝑥 ′ and 𝜎®𝑦 ′ can derive the rtoken if 𝜎®𝑥 is                                           Operand          𝑜 = copy 𝑝 |move 𝑝           The way of create values via loading place.
                                                                                                                     Statement         𝑠 ∈ 𝑆𝑇 𝑀𝑇 (𝑏 )               Statements for function body in each block.
holding it. Otherwise, neither of them is the holder. Thus, inference                             Function
                                                                                                                    Terminator         𝑗 ∈ 𝑇 𝐸𝑅𝑀 (𝑏 )               Terminator for function body in each block.
for the new states 𝜎®𝑥 ′, 𝜎®𝑦 ′ is required. The constraint consists of                                            StorageLive         𝑙𝑖𝑣𝑒 (𝑣)                     Mark the beginning of the live range for local.
                                                                                                  Liveness
two parts: (i) 𝜎®𝑦 = 0®: the first part is unchanged; (ii) {𝜎®𝑥 ′ = 𝜎®𝑥 ∧                                          StorageDead         𝑑𝑒𝑎𝑑 (𝑣)                     Mark the end of the live range for local.
                                                                                                                                       𝑝 =𝑜                         Yield the operand without changing it.
𝜎®𝑦 ′ = 0® } ∨ {𝜎®𝑦 ′ = 𝜎®𝑥 ∧ 𝜎®𝑥 ′ = 0® }: the second part guarantees the
                                                                                                                   Assignment
                                                                                                                    Reference          𝑝 =&_𝑝                       Crate a reference to the place.
exclusiveness by distributed to 𝜎®𝑥 ′ or 𝜎®𝑦 ′ only. The member who                               Statement         AddressOf
                                                                                                                      Casting
                                                                                                                                       𝑝 =∗_𝑝
                                                                                                                                       𝑝 = 𝑝 𝑎𝑠 𝑡
                                                                                                                                                                    Crate a raw pointer to the place.
                                                                                                                                                                    Cast type by using keyword "as".
is not the holder must stay zeroed to satisfy Property 5.1. After                                                  Discriminant        𝑑𝑖𝑠𝑐 (𝑝, 𝑐 )                 Write the discriminant for enum place.

adding new constraints to update 𝐶 ′ , the analyzer will remap 𝑥, 𝑦                                                     Goto           𝑔𝑜𝑡𝑜 (𝑏 )                    Jump to the successor of the current block.
                                                                                                                                                                    Return from the function.
to the latest state and update the mapping to 𝑀 ′ .
                                                                                                                       Return          𝑟𝑒𝑡𝑢𝑟𝑛
                                                                                                 Terminator
                                                                                                                        Drop           𝑑𝑟𝑜𝑝 (𝑝, 𝑏 )                 Destruct the place and go to the next block.
                                                                                                                        Call           𝑐𝑎𝑙𝑙 (𝑓 , 𝑝, [𝑜 ], 𝑏 )       Call function: operand list and return place.
                                                                                                 1 This table only displays a subset of the syntax relevant to our paper and the category has been modified for analysis. The
5.2.3 Field Primitives. The rtoken is field-sensitive. The arbitrary                               full syntax can be found in RFC#1211.
rtoken is a bit vector, whereas the field representation is a boolean
member. Field operations may result in incompatible length issues
                                                                                                 Table 3: The field primitives in leak-free memory model.
in bit vectors for some assignments. To address them, we propose
two field primitives, Ext and Srk, as listed in Table 3.
                                                                                                 Primitive          Description               Syntax                                Operation

   Definition 5.1 (Extend). Ext primitive extracts the field of                                  Ext (𝑣.𝑓 )        read from field          𝑣1 = 𝑣.𝑓              Sign-extend 𝑣.𝑓 and meet with init rtoken.
                                                                                                 Srk (𝑣)           write to field           𝑣1 .𝑓 = 𝑣             Join 𝑣 into a bit vector (length = 1).
the rvalue. Then it sign-extends the field and meets with the rtoken                             -                 field to field           𝑣1 .𝑓 = 𝑣.𝑓           No additional action.
encoded through the field’s type.

   Definition 5.2 (Shrink). Srk primitive joins all the members
of the rvalue to generates a one-lengthed bit vector.                                          5.3         Function Handling
                                                                                               5.3.1 Constructor and Destructor. Each heap item requires a con-
  Ext is only used for fields accessed in rvalues, whereas Srk is                              structor to create the rtoken. Rust provides two kinds of construc-
used for fields accessed in lvalues. Field primitives improve the                              tors: (i) function constructor: it returns a fully initialized value, such
adaptability of field operations because the lengths of the lvalue                             as Vec::new; (ii) local constructor: it declares the object and initial-
and rvalue could not be identical. Since field access is possible at                           izes fields later [42]. The initialized field can be used but the object
any depth, we set the maximum depth to one and designated other                                cannot cross the function boundaries before it is fully initialized.
minor accesses untracked.                                                                      All function inputs are treated as fully-initialized values, and the
arxiv, 2024,                                                                                       Mohan Cui, Hui Xu, Hongliang Tian, and Yangfan Zhou


   struct Proxy<T> { ptr: *mut T }                                          other types will not be deallocated by default. The taint analysis can
   impl<T> Drop for Proxy<T> {                                              streamline inter-procedural analysis and reduce constraint scales.
       fn drop(&mut self) {
           // user should manually deallocate the buffer in drop
       +   unsafe { Box::from_raw(self.ptr); }

   }
       }                                                                    5.4    Example of Leak-free Model
   fn main() {
       let mut buf = Box::new("buffer");                                    We illustrate a case of the constraints built upon a proxy-type issue,
       // transform the heap item 'buf' into the orphan object
       let ptr = Box::into_raw(buf);
                                                                            as shown in Figure 6. The green box represents the constraints
       let proxy = Proxy { ptr };
       // leak due to lacking releasing 'proxy.ptr' in drop
                                                                            generated by each statement, while the gray box represents the
   }                                                                        states of variables when the program analysis is complete. Box::new
     Final States in Z3 Solver                                              is a function constructor that creates the heap item Box<&str>
    buf = [1,0]   buf’ = [0,0]                                              and generates rtoken [1, 0] held by buf. Box::into_raw is a taint
    ptr = [1,0]   ptr’ = [0,0]                                              source, that transfers the rtoken to ptr. This call site is recorded by
    proxy = [1]   proxy’ = [1]∩[1] = [1]                                    the bug reporter. ptr is then assigned to the field of proxy, which
                                                                            is created by the local constructor. Since the length of Proxy 1 does
                                                                            not match ptr (2), the field access requires SRK primitive. As for
Figure 6: Example of the constraints built for the proxy-type
                                                                            drop(), the destructor rtoken ([1]) is generated by negating the bit
leak snippet. Those constraints are manually translated from
                                                                            vector [0] of the constructor rtoken for Proxy. We intersect this
MIR to the source code to enhance readability.
                                                                            destructor rtoken with the current state to simulate deallocation.
                                                                            When encountering a return, it asserts that the latest states of
                                                                            variables are zeroed (i.e., buf’, ptr’, and proxy’), indicating that
rtokens are constructed before the first statement of the function.
                                                                            all of them are released. If all constraints above are satisfied, the
The constructor and destructor are defined as follows:
                                                                            function is confirmed to be leak-free. However, due to the destructor
   Definition 5.3 (Rtoken Constructor). A function construc-                of Proxy cannot delete the field, the result of constraint solving is
tor creates rtoken by type encoding, and a local constructor creates 0®     UNSAT, and the recorded call site will be emitted to the user.
with the same length.
                                                                            6     EVALUATION
   Definition 5.4 (Rtoken Destructor). A destructor negates
the bit vector of the rtoken constructed by type encoding.                  We built a prototype of rCanary as an external component for
                                                                            Cargo and rustc and added around 8k lines of Rust code. The an-
   The local constructor is initialized to zero to facilitate partial       alyzer is implemented specifically upon the rustc-v1.62 toolchain.
initialization, which can be updated by initializing fields later. For      We have conducted comprehensive evaluations of rCanary us-
destructors like drop(), the rtoken will meet it with a destructor          ing real-world Rust programs. Our evaluation aims to answer the
rtoken to achieve deallocation. Since the rtoken destructor negates         following research questions (RQs):
the bit vector constructed by type encoding, it can destroy the             • RQ1. How effective is rCanary at detecting existing leak bugs?
rtoken and keep the leaked field remaining after calling drop().            • RQ2. How capable is rCanary of finding real-world leak vulner-
Therefore, our model is field-sensitive and supports partial initial-         abilities?
ization, partial deallocation, and partial movement.                        • RQ3. How efficient is rCanary in analyzing Rust ecosystem?
5.3.2 Inter-procedural Refinement. Errors propagation plague inter-         • RQ4. How is rCanary compared to other approaches?
procedural analysis based on boolean satisfiability [40]. If it has an      Experimental Setup. The following experiments were conducted
incorrect constraint in the callee, the result of constraint solving        on a machine with a 2GHz Intel CPU and 32GB of RAM running
is unsatisfied (i.e., UNSAT). We observed that the leaks across the         64-bit Ubuntu LTS 22.04.
semi-automated boundary have specific patterns; thus we use taint
analysis to simplify function boundaries; these functions are also          6.1    Effectiveness Evaluation (RQ1, RQ4)
used in the bug reporter to suppress false positives. The components
                                                                            6.1.1 Benchmark Generation. Since rCanary is the first static
are as follows:
                                                                            work aimed at memory leaks across a semi-automated memory
• The taint source consumes a heap item and returns pointer type            management model in Rust, we do not have a benchmark that
  or ManuallyDrop.                                                          previously existed to evaluate. Therefore, we devised an objective
• The taint sanitizer consumes a ManuallyDrop or pointer type               benchmark containing nine crates with fixed pull requests of leak
  and returns a heap item.                                                  issues as the ground truth for evaluation; this benchmark can also
   Box::leak [53] and Box::from_raw [54] are examples of taint              be utilized in the subsequent study. To evaluate the effectiveness,
sources and sanitizers. The taint source consumes the owner and             several leak analyzers are applied to these crates.
returns a pointer; the value cannot be freed, or this function will            The benchmark generation rigorously follows the procedure be-
return a dangling pointer. When encountering a taint source, the            low. We retrieve results searching from GitHub using the keyword
call site will be recorded as a potential leak candidate if the result of   Memory Leak, restricting the language to Rust, and concentrating
the constraint solver is UNSAT. The taint sanitizer is the opposite that    exclusively on the Issue and Rull Request sections of repositories,
retrieves the owner to activate automated allocation. As for other          sorted by Github’s default order. We filter the top 30 pages and
functions, we assume the object arguments will invoke drop() and            exclude the following irrelevant items:
rCanary: Detecting Memory Leaks Across Semi-automated Memory Management Boundary in Rust                                                                                                                               arxiv, 2024,


Table 4: Effectiveness evaluation results of rCanary versus FFIChecker, Saber, ASAN, Miri, and libFuzzer on nine package
benchmarks. These bugs are non-trivial from their pull requests (PR); the types of bugs include orphan object (OO) and proxy
type (PT). The reports are classified into true positives (TF) and false positives (FP).

                                           Package                                                            Issue              rCanary            FFIChecker               Saber         ASAN          Miri        libFuzzer
 Name                 Functions           LoC        Tests      AdtDef           Ty        Taint         PR        Pattern        TP        FP            TP/FP               TP/FP        TP/FP         TP/FP         TP/FP
 napi-rs                  1428           20.9k         14          724         2408          86       #1230          PT          1+18        4              0/0                0/5          FAIL         FAIL          FAIL
 rust-rocksdb             3295           30.2k         43          503         1593          17       #658           OO          1+16        0              1/0                0/8          0/13         FAIL           1/0
 arrow-rs                 6164          149.6k        1202         1293        7452          21       #1878          OO           1+0        0             FAIL               FAIL           0/1          2/8          FAIL
 arma-rs                  179            2.2k          66          243          858          3         #22           OO           1+0        0              0/0                0/6           0/1          0/0           0/0
 ruffle                   6474          135.8k        915         11301        67092         5        #6528          PT           1+0        0              0/0               0/12          FAIL         FAIL          FAIL
 flaco                     22            0.4k          0           258          729          14        #12           PT           2+0        0             FAIL                0/3           0/0          0/0          FAIL
 pprof-rs                 110            2.3k          9           162          508          3         #84           PT           1+0        0              1/0                0/2          FAIL          0/0           1/0
 rowan                    406            4.4k          5           118          442          10       #112           PT           1+0        3              1/0                0/7           0/0          0/0           0/0
 Fornjot                  688            11.8k         40          304         13141         2        #646           PT           1+0        0              0/0               FAIL           0/0          0/0           1/0
    Failed: FFIChecker: internal errors (self abort due to panic); Saber: the minimum Rust version supported (LLVM14) conflicts with the maximum SVF support (LLVM13); ASAN: cannot integrate LeakSanitizer
    into cargo tests; Miri: does not support to test extern FFI calls; libFuzzer: cannot generate fuzz targets through cargo-fuzz.


Table 5: Real-world vulnerability evaluation results of rCanary with the detailed issue description. After the manual check,
these vulnerabilities are classified into orphan-object (OO) and proxy-type (PT), along with their leak scenarios.

 Crate                         Functions          LoC           Location            Pattern           Summary               Description
 basic_dsp #52                     1998           30.3k           mod.rs               PT         LeakedDropImpl            Struct VectorBox<B,T> leaks the field argument in its Drop impl.
 symsynd #15                        35             0.5k            cabi.rs             PT         LeakedDropImpl            Field message stored a boxed slice in struct CError should be freed in Drop impl.
 rustfx #3                          263            4.8k           core.rs*             PT         LeakedDropImpl            Field host in struct OfxHost and String in enum PropertyValue.
 signal-hook #150                   234           5.4k            raw.rs               OO            Overwriting            Calling init() multiple times will leak AtomicPtr in slot and trigger panicking.
 rust-vst2 #42                      207           4.1k            host.rs              OO            Overwriting            Global LOAD_POINTER in call_main() will leak host for multiple assignments.
 synthir #1                         489           7.9k         emulator.rs             OO            Overwriting            MASKS_ALL and MASKS_BIT may leak the pointed Vec<BigUint>.
 relibc (redox-os) #180            1709          32.0k           mod.rs*               OO            Overwriting            Calling init() will overwrite PTHREAD_SELF; packet_data_ptr may be leaked.
 tinyprof #1                        26            0.5k          profiler.rs            OO            Overwriting            Assign by dereferencing to PROFILER_STATE_SENDER will leak the front chunck.
 teaclave-sgx #441                 7558          147.4k          func.rs*              OO            Overwriting            session_ptr and p_ret_ql_config may be leaked if overwrites to it.
 tor_patches #1                     288           4.1k          tor_log.rs             OO            Overwriting            Rewriting to LAST_LOGGED_FUNCTION and LAST_LOGGED_MESSAGE will leak box.
 log #314                            438           5.0k           lib.rs               OO             Finalization          set_boxed_logger leaks a boxed Log to LOGGER along with potential spin loop.
 tracing #1517                      3375          61.0k        dispatch.rs             OO             Finalization          Intentional leak towards a global GLOBAL_DISPATCH, the relevant issue in #1517.
 rust-appveyor #1                  43753         733.4k      thread_local.rs           OO             Finalization          KEYS and LOCALS need finalization function to clean up.
 ServoWsgi                         11606         236.2k          opts.rs               OO                Lazy               DEFAULT_OPTIONS needs finalization to clean up, especially for multi threads exit.
 rux                                585           9.9k           lazy.rs               OO                Lazy               The current lazy static uses the ’static that cannot be freed in multi threads.
 next_space_coop                   20477         317.1k          lazy.rs               OO                Lazy               The current lazy static uses the ’static that cannot be freed in multi threads.
 rio #52                            95             3.0k            lazy.rs             OO              PanicPath            If the assertion goes into unwinding, the value will be leaked inside a panic.
 sled #1458                        1350           32.8k            lazy.rs             OO              PanicPath            If the assertion goes into unwinding, the value will be leaked inside a panic.
   The item having * indicates vulnerabilities located in multiple files. Additionally, we did not open an issue specifically for scenario Lazy because it is a common design flaw in lazy_static implementations.



• Leaks caused by reference cycles.                                                                                        FFIChecker is built on a specific Rust version and only supports
• Leaks caused solely by manual memory management.                                                                      Rust-C FFI. Saber is a component of the source code analyzer SVF
• Leaks caused by outside FFI functions.                                                                                that employs inter-procedural sparse value-flow analysis to detect
• Leaks referred to sensitive information leaking (e.g., private key                                                    leaks for LLVM-based languages. Due to compatibility needs for
  leaks).                                                                                                               LLVM, we modified Saber to conform to the allocators in Rust
• Repositories used for language teaching or learning.                                                                  1.57. Other methods are based on dynamic analysis. LeakSani-
                                                                                                                        tizer is a memory leak detector, but an executable file or unit test
   After applying the above filters, the authors audit the buggy snip-                                                  is required to expose vulnerabilities. Similarly, Miri requires the
pet and confirm that leaks were caused across the semi-automated                                                        attribute #[text] to annotate the unit tests. As for libFuzzer, we
boundaries, matching our bug patterns. Finally, nine repositories                                                       employ cargo-fuzz to manually activate fuzzing to buggy func-
are retained, as listed in Table 4.                                                                                     tions after generating fuzz targets. LeakSanitizer, Miri, and lib-
                                                                                                                        Fuzzer are components in Rust, so we invoke them via the Rust
6.1.2 Comparing Tools. We compare our tool to the static bug
                                                                                                                        1.62 toolchain.
detector FFIChecker [20] for Rust-C FFI, the static leak analyzer
Saber (from SVF [28]), the runtime leak detector LeakSanitizer                                                           6.1.3 Bug Report. Our analyzer integrated a filter into the bug
(from Google AddressSanitizer [55]), the MIR interpreter Miri [56,                                                       reporter to refine the output. After analyzing bug reports in the
57], and the fuzzing tool libFuzzer (from LLVM) [58]. Because nu-                                                        experiments, we identified the following factors that can be the
merous static leak detectors do not support Rust projects, we can                                                        root cause of irrelevant outputs: (i) Callee Propagation: incorrect
only compare LLVM-based approaches [59].                                                                                 constraints or leaks in the callees will affect callers. (ii) Extern
arxiv, 2024,                                                                                                           Mohan Cui, Hui Xu, Hongliang Tian, and Yangfan Zhou


Function: many extern functions intentionally leak resources in                                                                                                    C o n s tr a in t S o lv in g
the return value for FFI use. Thus, we devise a filter integrated into                                                                                              C o n s tr a in t B u ild in g
                                                                                                                                                                     A d tD e f A n a ly s is
the bug reporter to filter the irrelevant items, although they may
                                                                                                   2 %         1 8 %                                       8 0 %




                                                                                           t
trigger memory leaks. The filter only reports the taint source in the




                                                                                       jo
                                                                                     rn
top entry and ignores the return value of extern functions if any




                                                                                F o
                                                                                                   2 %                   3 1 %                                     6 8 %




                                                                                       an
                                                                                     w
leak exists.




                                                                                 ro
                                                                                                         5 %                     3 5 %                                     6 0 %




                                                                                          s
                                                                                      f-r
                                                                                     ro
6.1.4 Results. rCanary can recall all related issues with accept-                                        6 %                      3 5 %                                    5 9 %




                                                                                p p
                                                                                       co
able false positives, as shown in Table 4. The number behind +




                                                                                     fla
                                                                                                     4 %                         3 9 %                                      5 8 %




                                                                                          e
                                                                                      ffl
indicates that the developers should manually check the FFI func-




                                                                                     ru
                                                                                                   2 %                              4 7 %                                          5 1 %




                                                                                          s
tions called by Rust that can free the orphan objects because Rust




                                                                                       -r
                                                                                     p i
                                                                                 n a
would not deallocate them. FFIChecker can detect three of them,                                    1 %                                       7 0 %                                         2 9 %




                                                                                       rs
                                                                                      a-
but it only supported Rust-C FFI and LLVM-IR lost the language




                                                                                 m
                                                                                                   1 %                                       7 1 %                                         2 8 %




                                                                                ar

                                                                                          s
                                                                                       -r
information. Saber fails to recall any issues because its report pro-




                                                                                     w
                                                                                 ro
                                                                                                   1 %             2 5 %                                       7 3 %




                                                                                ar
                                                                                       d b
vides no valuable information for users to locate the bug. Like




                                                                                     ks
                                                                                               0                       2 0                  4 0      6 0                            8 0              1 0 0




                                                                                o c
FFIChecker, the primary cause is that LLVM-IR lost high-level pro-




                                                                                -r
                                                                            st
gramming language features. LeakSanitizer, Miri, and libFuzzer




                                                                           ru
cannot evaluate generic functions and highly depend on the cover-
                                                                         Figure 7: The time distribution results on the benchmark.
age of sufficient unit tests for leak functions. Furthermore, Miri is
                                                                         For the virtual workspace, we individually test each crate
insufficient for functions that invoke FFI calls. Although rCanary
                                                                         inside and calculate the average percentage distribution in
supports functions with the extern keyword, it still cannot cross
                                                                         three phases.
the FFI boundary. Since compared tools are limited in leak detection
for Rust semi-automated boundaries, they have better pattern or
language support than rCanary.
                                                                         on evaluated crates. That indicates rCanary is promising to be
6.2      Real-world Vulnerability Evaluation (RQ2)                       a general, reliable, and fast source-code leak scanner for the Rust
More than 1,200 real-world Rust crates were downloaded and ana-          ecosystem.
lyzed from crates.io and GitHub. All of these packages are evaluated        We examine the time distribution of the overhead among three
by using a central script. The analyzer takes each local function        phases toward our benchmarks in Figure 7. All experiments were
as a distinct entry with a new context for each project and checks       repeated five times. The cost can be divided into AdtDef analysis,
the satisfiability of the leak-free memory model to detect potential     constraint building, and constraint solving. The median distribu-
leaks in their function bodies.                                          tions are AdtDef analysis at 5%, constraint building at 35%, and
   Among the evaluated packages, 3.0% have conflicted Rust ver-          constraint solving at 59%. The algorithm of AdtDef analysis is effi-
sion after switching toolchain, 11.6% have an unsupported virtual        cient, and the constraint-related phases cost most of the time (more
Cargo workspace, and 85.4% have been effectively analyzed. After         than 95%). The cost of constraint building and constraint solving
diagnostics are sent to the bug reporter, we manually check the          does not illustrate explicit relevance because the front contains type
source code and categorize them based on leak patterns and real-         encoding which suffers from macros expansion due to generating
world scenarios. The report outputs the vulnerabilities with related     massive types that may drag down the speed (e.g., the types count
functions and further pinpoints the detailed bug locations.              in ruffle). As our algorithm does not support pointer arithmetic,
   We listed 19 crates with memory leaks, and the detailed descrip-      the solver’s performance might be improved if such operations are
tions are listed in Table 5. Those vulnerabilities are non-trivial       commonly used as in crate arma-rs.
with different scenarios. For example, the orphan-object leak in the
popular crate signal-hook from crates.io exposes that repeated as-       6.4     Case Study
signment to a static mut pointer can cause leaks in the local thread.
                                                                         As globals are represented as normal variables in MIR, we did not
The proxy-type vulnerabilities in basic_dsp have generic-type pa-
                                                                         initially consider peculiarities when designing rCanary. However,
rameters invisible for dynamic tests without mono-morphization.
                                                                         real-world vulnerabilities have revealed some issues. Many pro-
We observe that the reassignment of the static pointer is error-prone
                                                                         grammers use static mut values to store global data on the heap
to memory leaks, which will be discussed in the case study.
                                                                         chunk, but numeral implementations are unsound, including:
6.3      Performance Evaluation (RQ3)                                    • Unsound initialized functions that can overwrite the previously
We expect rCanary to be an efficient static scanner for the Rust           stored value without deallocation, potentially leading to denial-
ecosystem. It should not impose significant overhead on the target.        of-service attacks or memory exhaustion.
At the ecosystem scale, rCanary took about 96 minutes to scan            • Static values that are thread-unsafe or non-finalizing which can-
1.2k real-world Rust packages. It took 8.4 seconds on average to           not be deallocated when threads exit, including static mut and
analyze each package. Since we use incremental compilation, it             lazy values.
does contain the overhead of the compilation elapsed. Furthermore,       • Incapability to deal with the poisoned static values if the first
there was no aborting or panicking while running the analyzer              initialization panics.
rCanary: Detecting Memory Leaks Across Semi-automated Memory Management Boundary in Rust                                                                     arxiv, 2024,


    Table 6: The attributes for the real-world leak scenarios.                  pointers to access objects, but the rtoken holder must be exclu-
                                                                                sive [69, 70]. We extend the proprietor to all pointer types and pro-
       Scenario      Panic Only   Invalid Use   Work Around   Memory Safe       vide an explicit boundary between stack-only and heap-allocated
    LeakedDropImpl       ×            ✓             ✓             ×             data for Rust types.
      Overwriting        ×            ×             ✓             ✓             Static leak detection. Numerous static analysis studies focus on
      Finalization       ×            ×             ×             ✓
                                                                                leak detection. FFIChecker [20] is designed for Rust-C FFI based
         Lazy            ×            ✓             ×             ✓
       PanicPath         ✓            ✓             ✓             ✓             on LLVM IR. Rupta [71] is a flow-insensitive but context-sensitive
                                                                                point-to alias analysis model designed for Rust MIR, with the poten-
                                                                                tial to be used for leak detection in the future. Saturn [72] is based
                                                                                on boolean satisfiability, which is context- and path-sensitive. rCa-
                                                                                nary, unlike Saturn, is a path-insensitive but flow-sensitive checker.
   We summarize the attributes for real-world leak scenarios in                 Clouseau [30] is a flow- and context-sensitive ownership model,
Table 6. All of them may lead to performance degradation, but                   but our work has a field-sensitive data abstraction and provides
only panicpath is caused by panic. Lazy and finalization are valid              features like partial initialization. Some studies employ symbolic
uses, where leaking thread-local values that are not harmless if                execution [73] and abstract interpretation [74, 75] to detect leaks for
only one thread. Leakeddropimpl, overwriting, and panicpath have                C/C++ programs such as KLEE [18], Clang [17], and Sparrow [19].
workaround functions that can be repeatedly invoked to consume                  Also, the full-sparse value-flow analysis [26, 28, 76] monitors value
memory quickly, potentially leading to memory exhaustion and                    flow and define-use chains via top-level and address-taken pointers
denial of service. Among them, overwriting has the lowest cost.                 to detect leaks. Like SVF, semi-sparse flow-sensitive analysis [77, 78]
As for Leakeddropimpl, even if the Drop is fixed (Listing 2), it is             can identify define-use chains by explicitly placing top-level point-
not memory-safe if users assign fields from the pointers that are               ers in SSA form.
not orphan objects. Therefore, the current design has significant
security risks.                                                                 8     CONCLUSION
                                                                                Semi-automated memory management model cannot prevent mem-
6.5      Discussion                                                             ory leaks in Rust. In this paper, we studied the root cause of memory
                                                                                leaks caused by this model and summarized bug patterns. We pre-
Like most static analyzers, rCanary is neither sound nor complete.
                                                                                sented rCanary, a static, non-intrusive, and fully automated model
The heap-item unit hinges on PhantomData. It conventionally cov-
                                                                                checker based on boolean satisfiability to detect them. We imple-
ers collection types in the standard library but may cause false
                                                                                mented this tool on top of Rust MIR and evaluated it through real-
positives for some user-defined types. The field primitives cannot
                                                                                world Rust projects. rCanary can efficiently recall our benchmarks
eliminate false negatives introduced by restricting the depth of
                                                                                and find 19 crates with memory leaks with high efficiency.
the field access, which can be refined in future work. Furthermore,
our model is insufficient if users store orphan objects in arrays or
containers (e.g., Vec and HashMap), and it does not support pointer             REFERENCES
arithmetic either.                                                               [1] N. D. Matsakis and F. S. Klock, “The rust language,” ACM SIGAda Ada Letters,
   We also discovered that the boundary between automated and                        vol. 34, no. 3, pp. 103–104, 2014, doi:10.1145/2692956.2663188.
                                                                                 [2] R. Jung, J.-H. Jourdan, R. Krebbers, and D. Dreyer, “Rustbelt: Securing the founda-
manual deallocation is unclear in FFI scenarios. To prevent leaks                    tions of the rust programming language,” Proceedings of the ACM on Programming
across the semi-automated boundary, we have the insight that it                      Languages, vol. 2, no. POPL, pp. 1–34, 2017, doi:10.1145/3158154.
                                                                                 [3] S. Klabnik and C. Nichols, The Rust Programming Language (Covers Rust 2018).
is necessary to design a wrapper like ManuallyDrop with a set of                     No Starch Press, 2019.
APIs. It needs to downcast the owner for pointer types and use an                [4] B. Anderson, L. Bergstrom, M. Goregaokar, J. Matthews, K. McAllister, J. Moffitt,
explicit annotation for external functions to check the double-free                  and S. Sapin, “Engineering the servo web browser engine using rust,” in Pro-
                                                                                     ceedings of the 38th International Conference on Software Engineering Companion,
or leak issues in FFI via static analysis.                                           2016, pp. 81–89, doi:10.1145/2889160.2889229.
                                                                                 [5] A. Light, “Reenix: Implementing a unix-like operating system in rust,”
                                                                                     Undergraduate Honors Theses, Brown University, 2015. [Online]. Available:
7      RELATED WORK                                                                  https://api.semanticscholar.org/CorpusID:18213575
                                                                                 [6] Y. Liang, L. Wang, S. Li, and B. Jiang, “Rustpi: A rust-powered reliable
Ownership model. rCanary adds formal rules to the Rust own-                          micro-kernel operating system,” in 2021 IEEE International Symposium on Soft-
ership model. Leak-free memory model shares many similarities                        ware Reliability Engineering Workshops (ISSREW). IEEE, 2021, pp. 272–273,
                                                                                     doi:10.1109/ISSREW53611.2021.00075.
with ownership syntax [30, 60], and C++ smart pointers [61]. It                  [7] RedoxOS, RedoxOS Contributors. 2022. https://www.redox-os.org/.
resembles linear types [62, 63] to support Rust syntax features such             [8] Y. Shen, H. Tian, Y. Chen, K. Chen, R. Wang, Y. Xu, Y. Xia, and S. Yan, “Oc-
as ownership movement [64]. Clarke et al. [30] proposed a strict                     clum: Secure and efficient multitasking inside a single enclave of intel sgx,” in
                                                                                     Proceedings of the Twenty-Fifth International Conference on Architectural Sup-
ownership model named ownership type that asserts the owning                         port for Programming Languages and Operating Systems, 2020, pp. 955–970,
relation between objects [65, 66]. Clouseau [30] adds the features                   doi:10.1145/3373376.3378469.
                                                                                 [9] S. Lankes, J. Breitbart, and S. Pickartz, “Exploring rust for unikernel development,”
of ownership transfer, arbitrary aliases, and ownership invariant                    in Proceedings of the 10th Workshop on Programming Languages and Operating
at function boundaries to enhance scalability, which is one of the                   Systems, 2019, pp. 8–15, doi:10.1145/3365137.3365395.
foundations of our model. Although some language extensions are                 [10] A. Levy, M. P. Andersen, B. Campbell, D. Culler, P. Dutta, B. Ghena, P. Levis, and
                                                                                     P. Pannuto, “Ownership is theft: Experiences building an embedded os in rust,”
proposed to allow read-only aliases [67, 68], the strict definition                  in Proceedings of the 8th Workshop on Programming Languages and Operating
does not require right-hand-side pointers [62]. Our model allows                     Systems, 2015, pp. 21–26, doi:10.1145/2818302.2818306.
arxiv, 2024,                                                                                                             Mohan Cui, Hui Xu, Hongliang Tian, and Yangfan Zhou


[11] A. Levy, B. Campbell, B. Ghena, D. B. Giffin, S. Leonard, P. Pannuto, P. Dutta,        [36] std::ptr::drop_in_place, 2024, https://doc.rust-lang.org/std/ptr/fn.drop_in_place.
     and P. Levis, “The tock embedded operating system,” in Proceedings of the                   html (Accessed on 07/26/2024).
     15th ACM Conference on Embedded Network Sensor Systems, 2017, pp. 1–2,                 [37] M. Cui, C. Chen, H. Xu, and Y. Zhou, “Safedrop: Detecting memory deallocation
     doi:10.1145/3131672.3136988.                                                                bugs of rust programs via static data-flow analysis,” ACM Transactions on Software
[12] A. Levy, B. Campbell, B. Ghena, D. B. Giffin, P. Pannuto, P. Dutta, and P. Levis,           Engineering and Methodology, vol. 32, no. 4, pp. 1–21, 2023, doi:10.1145/3542948.
     “Multiprogramming a 64kb computer safely and efficiently,” in Proceedings              [38] Y. Bae, Y. Kim, A. Askar, J. Lim, and T. Kim, “Rudra: finding memory safety bugs
     of the 26th Symposium on Operating Systems Principles, 2017, pp. 234–251,                   in rust at the ecosystem scale,” in Proceedings of the ACM SIGOPS 28th Symposium
     doi:3132747.3132786.                                                                        on Operating Systems Principles, 2021, pp. 84–99, doi:10.1145/3477132.3483570.
[13] S. Nagarakatte, M. M. Martin, and S. Zdancewic, “Watchdog: Hardware for safe           [39] Z. Li, J. Wang, M. Sun, and J. C. Lui, “Mirchecker: detecting bugs in rust programs
     and secure manual memory management and full memory safety,” in 2012 39th                   via static analysis,” in Proceedings of the 2021 ACM SIGSAC Conference on Computer
     Annual International Symposium on Computer Architecture (ISCA). IEEE, 2012,                 and Communications Security, 2021, pp. 2183–2196, doi:10.1145/3460120.3484541.
     pp. 189–200, doi:10.1145/2366231.2337181.                                              [40] L. d. Moura and N. Bjørner, “Z3: An efficient smt solver,” in International
[14] M. Hicks, G. Morrisett, D. Grossman, and T. Jim, “Experience with safe manual               conference on Tools and Algorithms for the Construction and Analysis of Systems.
     memory-management in cyclone,” in Proceedings of the 4th international sympo-               Springer, 2008, pp. 337–340. [Online]. Available: https://link.springer.com/
     sium on Memory management, 2004, pp. 73–84, doi:10.1145/1029873.1029883.                    chapter/10.1007/978-3-540-78800-3_24
[15] A. Balasubramanian, M. S. Baranowski, A. Burtsev, A. Panda, Z. Rakamarić,              [41] H. N. Gabow and R. E. Tarjan, “A linear-time algorithm for a special case of
     and L. Ryzhyk, “System programming in rust: Beyond safety,” in Proceedings                  disjoint set union,” in Proceedings of the Fifteenth Annual ACM Symposium on
     of the 16th Workshop on Hot Topics in Operating Systems, 2017, pp. 156–161,                 Theory of Computing, ser. STOC ’83,. Association for Computing Machinery,
     doi:10.1145/3102980.3103006.                                                                1983, doi:10.1145/800061.808753.
[16] C.-. U. R. Consumption, 2024, https://cwe.mitre.org/data/definitions/400.html          [42] R. Group, “The rust reference,” 2024, https://doc.rust-lang.org/reference (Accessed
     (Accessed on 07/26/2024).                                                                   on 07/26/2024).
[17] C. Lattner, “Llvm and clang: Next generation compiler technology,” in The BSD          [43] std::vec::Vec::new, 2024, https://doc.rust-lang.org/std/vec/struct.Vec.html#
     conference, vol. 5, 2008, pp. 1–20. [Online]. Available: https://reup.dmcs.pl/wiki/         method.new (Accessed on 07/26/2024).
     images/0/09/53_BSDCan2008ChrisLattnerBSDCompiler.pdf                                   [44] A. Møller and M. I. Schwartzbach, “Static program analysis,” Notes. Feb, 2012.
[18] C. Cadar, D. Dunbar, D. R. Engler et al., “Klee: unassisted and automatic              [45] std::net::IpAddr, 2024, https://doc.rust-lang.org/std/net/enum.IpAddr.html (Ac-
     generation of high-coverage tests for complex systems programs.” in OSDI, vol. 8,           cessed on 07/26/2024).
     2008, pp. 209–224. [Online]. Available: https://www.usenix.org/legacy/event/           [46] rustc_middle::ty::adt::AdtDef, 2024, https://doc.rust-lang.org/nightly/nightly-
     osdi08/tech/full_papers/cadar/cadar.pdf                                                     rustc/rustc_middle/ty/adt/struct.AdtDef.html (Accessed on 07/26/2024).
[19] Y. Jung and K. Yi, “Practical memory leak detector based on parameterized              [47] rustc_middle::ty::generic_args::GenericArgs, 2024, https://doc.rust-lang.org/
     procedural summaries,” in Proceedings of the 7th international symposium on                 nightly/nightly-rustc/rustc_middle/ty/generic_args/type.GenericArgs.html (Ac-
     Memory management, 2008, pp. 131–140, doi:10.1145/1375634.1375653.                          cessed on 07/26/2024).
[20] Z. Li, J. Wang, M. Sun, and J. C. Lui, “Detecting cross-language memory manage-        [48] std::marker::PhantomData, 2024, https://doc.rust-lang.org/std/marker/struct.
     ment issues in rust,” in European Symposium on Research in Computer Security.               PhantomData.html (Accessed on 07/26/2024).
     Springer, 2022, pp. 680–700, doi:10.1007/978-3-031-17143-7_33 .                        [49] std::string::String, 2024, https://doc.rust-lang.org/std/string/struct.String.html
[21] M. Cui, S. Sun, H. Xu, and Y. Zhou, “Is unsafe an achilles’ heel? a comprehensive           (Accessed on 07/26/2024).
     study of safety requirements in unsafe rust programming,” in Proceedings of the        [50] F. Nielson, H. R. Nielson, and C. Hankin, Principles of program analysis. Springer
     IEEE/ACM 46th International Conference on Software Engineering, 2024, pp. 1–13,             Science & Business Media, 2004.
     doi:10.1145/3597503.3639136.                                                           [51] E. Reed, “Patina: A formalization of the rust programming language,” University
[22] R. lang Group, “Unsafe intrinsic mem::forget in rust re-                                    of Washington, Department of Computer Science and Engineering, Tech. Rep.
     lease      version     0.12,”   2015,     https://github.com/rust-lang/rust/blob/           UW-CSE-15-03-02, p. 264, 2015. [Online]. Available: https://api.semanticscholar.
     ba4081a5a8573875fed17545846f6f6902c8ba8d/src/libcore/intrinsics.rs#L302                     org/CorpusID:10124530
     (Accessed on 07/26/2024).                                                              [52] F. Wang, F. Song, M. Zhang, X. Zhu, and J. Zhang, “Krust: A formal executable
[23] R. Group, “The rust community’s crate registry,” 2024, https://crates.io (Accessed          semantics of rust,” in 2018 International Symposium on Theoretical Aspects of Soft-
     on 07/26/2024).                                                                             ware Engineering (TASE). IEEE, 2018, pp. 44–51, doi:10.1109/TASE.2018.00014.
[24] V. Astrauskas, C. Matheja, F. Poli, P. Müller, and A. J. Summers, “How do pro-         [53] std::boxed::Box::leak, 2024, https://doc.rust-lang.org/std/boxed/struct.Box.html#
     grammers use unsafe rust?” Proceedings of the ACM on Programming Languages,                 method.leak (Accessed on 07/26/2024).
     vol. 4, no. OOPSLA, pp. 1–27, 2020, doi:10.1145/3428204.                               [54] std::boxed::Box::from_raw, 2024, https://doc.rust-lang.org/std/boxed/struct.Box.
[25] A. N. Evans, B. Campbell, and M. L. Soffa, “Is rust used safely by software                 html#method.from_raw (Accessed on 07/26/2024).
     developers?” in Proceedings of the ACM/IEEE 42nd International Conference on           [55] K. Serebryany, D. Bruening, A. Potapenko, and D. Vyukov, “ { AddressSanitizer } :
     Software Engineering, 2020, pp. 246–257, doi:10.1145/3377811.3380413.                       A fast address sanity checker,” in 2012 USENIX Annual Technical Conference
[26] Y. Sui, D. Ye, and J. Xue, “Detecting memory leaks statically with full-sparse              (USENIX ATC 12), 2012, pp. 309–318. [Online]. Available: https://www.usenix.
     value-flow analysis,” IEEE Transactions on Software Engineering, vol. 40, no. 2, pp.        org/conference/atc12/technical-sessions/presentation/serebryany
     107–122, 2014, doi:10.1109/TSE.2014.2302311.                                           [56] S. Olson, “Miri: an interpreter for rust’s mid-level intermediate representation,”
[27] M. Orlovich and R. Rugina, “Memory leak analysis by contradiction,” in                      Technical report, Tech. Rep., 2016. [Online]. Available: https://solson.me/miri-
     International Static Analysis Symposium.            Springer, 2006, pp. 405–424,            report.pdf
     doi:10.1007/11823230_26.                                                               [57] R. Jung, H.-H. Dang, J. Kang, and D. Dreyer, “Stacked borrows: an aliasing model
[28] Y. Sui and J. Xue, “Svf: interprocedural static value-flow analysis in llvm,” in            for rust,” Proceedings of the ACM on Programming Languages, vol. 4, no. POPL,
     Proceedings of the 25th international conference on compiler construction, 2016, pp.        pp. 1–32, 2019, doi:10.1145/3371109.
     265–266, doi:10.1145/2892208.2892235.                                                  [58] K. Serebryany, “Continuous fuzzing with libfuzzer and addresssanitizer,” in
[29] A. W. Appel, “Ssa is functional programming,” Acm Sigplan Notices, vol. 33, no. 4,          2016 IEEE Cybersecurity Development (SecDev).              IEEE, 2016, pp. 157–157,
     pp. 17–20, 1998, doi:10.1145/278283.278285.                                                 doi:10.1109/SecDev.2016.043.
[30] D. L. Heine and M. S. Lam, “A practical flow-sensitive and context-sensitive           [59] C. Lattner and V. Adve, “Llvm: A compilation framework for lifelong
     c and c++ memory leak detector,” in Proceedings of the ACM SIGPLAN 2003                     program analysis & transformation,” in International Symposium on Code
     conference on Programming language design and implementation, 2003, pp. 168–                Generation and Optimization, 2004. CGO 2004.                 IEEE, 2004, pp. 75–86,
     181, doi:10.1145/781131.781150.                                                             doi:10.1109/CGO.2004.1281665.
[31] S.-L. T. S. M. T. LIBRARY, 2024, http://smtlib.cs.uiowa.edu/ (Accessed on              [60] D. Clarke, “An object calculus with ownership and containment,” 2001. [Online].
     07/26/2024).                                                                                Available: https://courses.cs.washington.edu/courses/cse590p/01wi/clarke-fool8.
[32] T. Ramananandro, G. Dos Reis, and X. Leroy, “A mechanized semantics                         pdf
     for c++ object construction and destruction, with applications to resource             [61] D. Edelson and I. Pohl, Smart pointers: They’re smart, but they’re not pointers.
     management,” ACM SIGPLAN Notices, vol. 47, no. 1, pp. 521–532, 2012,                        Citeseer, 1992. [Online]. Available: https://citeseerx.ist.psu.edu/document?repid=
     doi:10.1145/2103621.2103718.                                                                rep1&type=pdf&doi=d78dd0f23e9c75b4841111b1978c2997d9965c18
[33] std::ops::Drop, 2024, https://doc.rust-lang.org/std/ops/trait.Drop.html (Accessed      [62] P. Wadler, “Linear types can change the world!” in Programming concepts
     on 07/26/2024).                                                                             and methods, vol. 3, no. 4. Citeseer, 1990, p. 5. [Online]. Available:
[34] std::vec::Vec, 2024, https://doc.rust-lang.org/std/vec/struct.Vec.html (Accessed            https://api.semanticscholar.org/CorpusID:58535510
     on 07/26/2024).                                                                        [63] J.-Y. Girard, “Linear logic: its syntax and semantics,” London Mathematical Society
[35] std::mem::ManuallyDrop, 2024, https://doc.rust-lang.org/std/mem/struct.                     Lecture Note Series, pp. 1–42, 1995.
     ManuallyDrop.html (Accessed on 07/26/2024).                                            [64] B. C. Pierce, Advanced topics in types and programming languages. MIT press,
                                                                                                 2004.
rCanary: Detecting Memory Leaks Across Semi-automated Memory Management Boundary in Rust                                                                                   arxiv, 2024,


[65] J. Noble, J. Vitek, and J. Potter, “Flexible alias protection,” in European Conference        2024, pp. 60–72.
     on Object-Oriented Programming. Springer, 1998, pp. 158–185. [Online].                   [72] Y. Xie and A. Aiken, “Context-and path-sensitive memory leak detection,” in
     Available: https://link.springer.com/chapter/10.1007/BFb0054091                               Proceedings of the 10th European software engineering conference held jointly
[66] D. G. Clarke, J. M. Potter, and J. Noble, “Ownership types for flexible alias                 with 13th ACM SIGSOFT international symposium on Foundations of software
     protection,” in Proceedings of the 13th ACM SIGPLAN conference on Object-                     engineering, 2005, pp. 115–125, doi:10.1145/1081706.1081728.
     oriented programming, systems, languages, and applications, 1998, pp. 48–64, doi:        [73] J. C. King, “Symbolic execution and program testing,” Communications of the
     10.1145/286936.286947.                                                                        ACM, vol. 19, no. 7, pp. 385–394, 1976, doi:10.1145/360248.360252.
[67] J. Boyland, “Alias burying: Unique variables without destructive reads,” Software:       [74] P. Cousot and R. Cousot, “Abstract interpretation: a unified lattice model for static
     Practice and Experience, vol. 31, no. 6, pp. 533–553, 2001, doi:10.1002/spe.370.              analysis of programs by construction or approximation of fixpoints,” in Proceed-
[68] D. Walker and G. Morrisett, “Alias types for recursive data structures,” in                   ings of the 4th ACM SIGACT-SIGPLAN symposium on Principles of programming
     International Workshop on Types in Compilation. Springer, 2000, pp. 177–206.                  languages, 1977, pp. 238–252, doi:10.1145/512950.512973.
     [Online]. Available: https://link.springer.com/chapter/10.1007/3-540-45332-6_7           [75] ——, “Systematic design of program analysis frameworks,” in Proceedings of the
[69] C. Boyapati, R. Lee, and M. Rinard, “Ownership types for safe programming:                    6th ACM SIGACT-SIGPLAN symposium on Principles of programming languages,
     Preventing data races and deadlocks,” in Proceedings of the 17th ACM SIGPLAN                  1979, pp. 269–282, doi:10.1145/567752.567778.
     conference on Object-oriented programming, systems, languages, and applications,         [76] B. Hardekopf and C. Lin, “Flow-sensitive pointer analysis for millions of lines of
     2002, pp. 211–230, doi:10.1145/582419.582440.                                                 code,” in International Symposium on Code Generation and Optimization (CGO
[70] D. Clarke and S. Drossopoulou, “Ownership, encapsulation and the disjointness                 2011). IEEE, 2011, pp. 289–298, doi:10.1109/CGO.2011.5764696.
     of type and effect,” in Proceedings of the 17th ACM SIGPLAN conference on Object-        [77] S. Cherem, L. Princehouse, and R. Rugina, “Practical memory leak detection
     oriented programming, systems, languages, and applications, 2002, pp. 292–310,                using guarded value-flow analysis,” in Proceedings of the 28th ACM SIGPLAN
     doi:10.1145/582419.582447.                                                                    Conference on Programming Language Design and Implementation, 2007, pp. 480–
[71] W. Li, D. He, Y. Gui, W. Chen, and J. Xue, “A context-sensitive pointer analysis              491, doi:10.1145/1250734.1250789.
     framework for rust and its application to call graph construction,” in Proceedings       [78] B. Hardekopf and C. Lin, “Semi-sparse flow-sensitive pointer analysis,” ACM
     of the 33rd ACM SIGPLAN International Conference on Compiler Construction,                    SIGPLAN Notices, vol. 44, no. 1, pp. 226–238, 2009, doi:10.1145/1594834.1480911.
