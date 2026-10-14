                                         Verification of a Generational Garbage Collector
                                         SHENGYI WANG, Princeton University and Shanghai Qi Zhi Institute, China
                                         KATHRIN STARK, Heriot-Watt University, Scotland
                                         ANDREW W. APPEL, Princeton University, USA
                                         We have formally verified in Rocq+VST a multi-generation collector with support for mutable references,
                                         written in C and compatible with OCaml data types. Its carefully specified API supports C programs or
                                         CertiRocq (a verified compiler from Rocq to C) is similar to that of OCaml’s collector. We have demonstrated
                                         the adequacy of our API specification for the mutator (client of the garbage collector) by verifying client
arXiv:2609.13186v1 [cs.PL] 31 Jul 2026




                                         programs. Our program and our verification are modular so that (1) the API spec is independent of the
                                         implementation (e.g., the choice of copying vs. mark-and-sweep, generational-vs-nongenerational) and (2)
                                         the specification and verification of components of the implementation (such as the forwarding function) are
                                         independent of other components (e.g., design decisions regarding older generations, multiple threads, or
                                         “remembered sets” of mutable references).

                                         1 Introduction
                                         We have formally verified the correctness of a multi-generation copying garbage collector with
                                         support for mutable references and updatable arrays, compatible with OCaml data representations.
                                         We have done so in a modular way, so that some of the component functions and their verifications
                                         could be repurposed into other garbage-collector frameworks, such as the OCaml 4 or OCaml 5
                                         garbage collectors. Our Rocq proofs are available open-source (see Appendix A).
                                           To provide assurance that the formal specification of the collector is strong enough, we have
                                         furthermore verified clients of the collector (“mutator" programs); and we have designed that
                                         specification to abstract (hide from the client) unneeded information, such as the fact that the
                                         collector is generational, or the details of its remembered set for mutable references. Our interface
                                         (and its specification) can be used from the C source-language, and reasoned about in the C
                                         semantics; it does not require reasoning at the assembly-language level and does not require any
                                         special support from the C compiler. Thus it also supports proved-correct compilers from functional
                                         languages to C, and we have demonstrated this [Korkut et al. 2025] with the CertiRocq verified
                                         compiler for Rocq [Paraskevopoulou et al. 2021].
                                            Background. Programming languages that allow dynamic allocation of pointer data structures
                                         generally have a mechanism for reclaiming objects or records that are no longer needed. Some
                                         languages, such as C, leave this task entirely to the programmer—which makes APIs more complex,
                                         makes programming more difficult, and leads to bugs and unsafety. Other languages, such as Rust,
                                         have a type system that keeps track of single versus shared ownership (multiple pointers to the
                                         same object) and allows type-directed (and safe) deallocation; this can be highly efficient, but
                                         there is still some programming and API burden (and restrictions on sharing patterns). Finally,
                                         languages such as Lisp, Scheme, ML, Haskell, Java, or Python have automatic garbage collection
                                         (g.c.): graph-traversal algorithms determine which objects are no longer in use and reclaim them
                                         automatically. Programmers in such languages don’t need to keep track of shared versus single-
                                         owner data structures, but pay a modest price both in the overhead of object descriptors (so the g.c.
                                         can understand how to traverse the graph) and in the cost of executing the graph traversals.
                                            Garbage collection has a long history with thousands of papers published since 1960 [Jones et al.
                                         2023]. Some of the principles are,
                                         Authors’ Contact Information: Shengyi Wang, wangshengyi@sqz.ac.cn, Princeton University and Shanghai Qi Zhi Institute,
                                         Shanghai, China; Kathrin Stark, K.Stark@hw.ac.uk, Heriot-Watt University, Edinburgh, Scotland; Andrew W. Appel,
                                         appel@princeton.edu, Princeton University, Princeton, NJ, USA.
2                                                                        Shengyi Wang, Kathrin Stark, and Andrew W. Appel


      • Live objects are those reachable from roots which are the global and/or local variables of
         the program.
      • The location of these roots must be described to the collector, with particular attention to
        which local variables are still in use.1
      • Mark and sweep collection leaves live objects in place, and reclaims the memory used by
         garbage objects by putting them into a data structure that can be used by the allocator.
      • Copying collection moves live objects out of the space they were in, the from-space, into a
         to-space, leaving a large contiguous from-space as a region of memory available for allocation.
      • Generational collection relies on the observations that (1) new objects, when created and
         initialized, necessarily point to older objects; and (2) older objects that have already survived
         garbage collection(s) will likely have a longer future lifetime than younger objects. Therefore,
         if mutable update (storing new pointer values into existing objects) is rare, then the mostly
         preserved invariant of newer objects pointing to older objects can be exploited to focus g.c.
         attention on just the smaller, newer object spaces.
      • When mutable update is permitted, generational collection typically requires a remembered
         set keeping track of object fields that may house pointers from older objects into younger
         ones.
      • Generational collectors may be purely mark-and-sweep or purely copying, or may be
         organized with copying collection from nurseries to an older generation, and mark-and-
         sweep in the older generation.
      • Shared-memory concurrent programs are typically arranged so that each thread has its own
         nursery (which eliminates synchronization during object allocation) but older generations
         are shared between threads (requiring synchronization when starting garbage collections).
   All of these principles were established decades ago, though there have been significant new
developments in, for example, the details of how shared-memory concurrent programs should
manage private nurseries with shared older generations [Sivaramakrishnan et al. 2020].
   In this paper we explain a simple multi-generation single-thread copying collector, we explain its
invariants and the specifications (preconditions/postconditions) of each of its component functions;
and we discuss how those verified functions could be repurposed in other configurations of a
collector.
   A multi-generation collector such as we have implemented is not necessarily optimal. “Using
multiple generations has a number of drawbacks" [Jones et al. 2023, §9.5]. The state of the art seems
to be hybrid 2-generation collectors that use copying collection for the nursery and mark-sweep
collection for the older generation [Jones et al. 2023][Sivaramakrishnan et al. 2020]. Therefore we
have organized both our collector and its proof so that many important components can be used in
such collectors.
  Contributions. We build on previous work by Wang et al. [2019], who verified a multi-generation
copying collector for a subset of the OCaml data formats. In the current work,
    • We add functionality: mutable references and updateable arrays.
    • We add expressiveness: with lemmas regarding the ability to allocate new objects, and in
       general, by strengthening the specification enough so that mutator programs can actually
       be proved correct.
1 A local variable is live in the terminology of compiler optimization if its contents might be fetched in the future. This

determination is Turing-complete but can be conservatively approximated by optimizing compilers. A g.c.-heap object is
reachable if there is a chain of pointers from a live root to the object. One could, in principle, say that a g.c.-heap object is
“live" only if the program will actually traverse such a path in the future, but this determination is also Turing-complete and
not easy to approximate, so in practice we say that g.c.-heap objects are live if they are reachable from a live root.
Verification of a Generational Garbage Collector                                                      3


     • We fix bugs: The previous collector was verified correct in Rocq w.r.t. its specification. But
        when Korkut et al. [2025] verified clients of this collector, they found that this specification
        was too weak to prove the clients correct. When we strengthened the specification, we
        found that the C program (the g.c.) did not satisfy the correct specification. At least one of
        the bugs was a corner case unlikely to have been uncovered in testing. We fixed the bugs.
     • We ensure modularity: e.g., by proving the forward function correct w.r.t. a specification
        usable in other g.c. designs.
     • We used AI to adapt the proofs: The previous work, a proof of a multi-generation collector
        without mutable references, needed significant adaptation of its internal invariants and
        proofs in Rocq. We used OpenAI Codex to adjust invariants and adapt the Rocq proofs, as
        described in a separate technical report [Wang 2026]. However, the adjustments (in previous
        bullet points) to the client-side specifications were not done with AI.
This collector was designed and built primarily as a g.c. for CertiRocq [Anand et al. 2017], a verified
compiler for Rocq. Therefore, plug-compatibility with OCaml’s g.c. is not an explicit goal. Our object
formats are the same as OCaml’s (though we omit lazy/force tags and fiber-continuation objects);
our mutator interface is similar but not identical. CertiRocq generates C code (compilable with
CompCert or with LLVM or gcc, though only the CompCert path is fully verified); our collector’s
API is compatible with both CertiRocq-generated code and handwritten C code for low-level
libraries [Korkut et al. 2025].
   One might think that since Rocq’s Gallina programming language is purely functional, a Rocq
program does not need mutation. However, there are several uses for mutation: Rocq’s built-in
persistent arrays with a functional API but an imperative implementation [Armand et al. 2010],
Rocq’s coinduction (if implemented using lazy evaluation with thunk update), or in functional
programs that access mutation via a monadic interface [Korkut 2024]. Furthermore, our collector
could also be used for semifunctional languages such as OCaml or Standard ML (which have explicit
mutation) or for lazy languages such as Haskell (which need mutation for thunk update).
   Other verified collector+mutator combinations. There are many papers describing pencil-and-
paper proofs of g.c. algorithms (starting with Dijkstra [1968]); or mechanized proofs of abstract
models of g.c. programs but not proofs of the actual programs [Yang and Wrigstad 2022]; or proofs
of garbage collector programs without a demonstration that the specification is strong and detailed
enough to actually prove mutators correct [Shamsu et al. 2024].
   However, an important aspect of our work is a usable specification interface, with the ability to
practically verify correctness of mutator programs that are clients of our collector, and the ability
to practically verify other collectors that satisfy the same specification interface. By verifying the
mutator and collector in the same program logic, or at least in program logics compatible with the
same operational semantics, one can prove end-to-end correctness of the whole collector+mutator
system.
   A few others have also verified across that interface, but in each case there are significant
limitations on both the API and on the tricky combination of mutable references and generational
collection:
     • McCreight et al. [2007] verified three nongenerational collectors: mark-and-sweep, Cheney-
        style copying, Baker’s concurrent copying. They also specified an interface to the mutator
        and verified the correctness of a mutator (client) program. The programs are written, and
        the interfaces are specified, in the SCAP (Stack-based Certified Assembly Programming)
        language, which means that it may be difficult to port to mutators not written in SCAP, or
        variations of the collector not written in SCAP. Baker’s algorithm is concurrent—so one
        must reason about race conditions—and uses a read barrier—that is, dereferencing (loading)
4                                                         Shengyi Wang, Kathrin Stark, and Andrew W. Appel


       an object field requires more than just a simple load instruction, so the compiler for the
       mutator must be rather specialized in how it generates code.
     • McCreight et al. [2010] verifed a nongenerational Cheney-style copying collector, with
       a specification of the mutator interface, and verified the correctness of client programs.
       Programs are written in CompCert C. Standard CompCert compiles through a series of
       intermediate languages, each using a memory model with abstract block numbers, and
       the semantics is insensitive to renumbering of blocks. McCreight et al.’s collector inserts
       a new intermediate language GCminor into this sequence, which takes advantage of this
       insensitivity to make the garbage collector’s rearrangement of data transparent to the
       mutator, and to proofs of correctness of the mutator. However, (unlike the C language in
       which our system is specified) there are no program logics or semiautomated reasoning
       systems for GCminor, with which to prove client programs correct.
     • Sandberg Ericsson et al. [2019] verified a two-generation collector for CakeML, including
       the verification of its mutator client, that is, ML programs compiled to the “StackLang”
       intermediate representation. But their work has some limitations: They avoid having a
       general mechanism for remembered sets, by segregating mutable references into a region
       of the heap where they are never collected. This is an idiosyncratic approach chosen for
       convenience in verification, and it will not scale well to applications that allocate large data
       structures containing mutable references that eventually will need to be reclaimed. They use
       a two-generation copying collector, which will not perform well at scale compared either
       to a hybrid collector or a multi-generation copying collector [Jones et al. 2023, §9.5]. The
       specification of their collector-mutator interface is tied so tightly to a low-level intermediate
       language of CakeML that it is difficult to see how to use the collector in other contexts—
       however, there are mechanized correctness-proving tools for CakeML programs [Guéneau
       et al. 2017].

2   Interface between collector and mutator
In the terminology of garbage collection, the client of the collector (the program doing useful work)
is called the “mutator." The mutator builds and traverses a directed graph of objects. Each object is
represented as 𝑛 + 1 words in memory, with a header (or equivalently descriptor) and 𝑛 fields, each
of which may be either a pointer to another heap object, an integer, or an “outlier" (pointer to a
non-heap object). Graph nodes represented by integers or outliers have out-degree zero. Graph
nodes may have arbitrary in-degree; that is, there may be sharing or even cycles in the graph.
   We specify and prove our g.c. using the Verifiable C program logic, which is a higher-order
separation logic mechanized in the Verified Software Toolchain [Appel et al. 2014; Cao et al. 2018],
which is itself formalized and executed in Rocq (Coq). Since Verifiable C is a separation logic, it
naturally accommodates descriptions of tree nodes whose child-pointers point to disjoint data
structures. But graph structures with sharing are not as natural a fit for separation logic. To
accommodate a graph in VST, we use the CertiGraph library [Wang et al. 2019] that represents an
abstract graph, with a separation-logic embedding as simply the iterated separating conjunction
(“big star”) of all the graph nodes.
   subsection 2.1 presents the API. First we will explain the API informally, with pictures and
diagrams indicating objects, fields, pointers, and separated regions of the heap.
   Our g.c. is designed to support an OCaml-like language and uses OCaml object formats. OCaml
values can be pointers or unboxed integers; to allow the garbage collector to distinguish between
those, (word-aligned) pointer values are represented with even numbers, and unboxed integers
are represented with odd numbers. In the C program (for the g.c., or for mutators written in C or
code-generated into C), we use the value typedef:
Verification of a Generational Garbage Collector                                                                                  5


                             Listing 1. value type that can be either pointer or integer
typedef void ∗value             __attribute((aligned(_Alignof(void ∗))));
That is, a value is a pointer-to-void (which is a C idiom for a pointer to an unknown type); the
attribute is semantically transparent to the C compiler but serves a hint to our program verifier
(VST) that the value might hold an integer instead of a pointer (see Appendix B).



       Fig. 2. The mutator has local and global variables that                               2                  2
       are roots of the graph objects. Each object has a 1-word
                                                                                                      3
       header containing its length (as well as a tag field). The root
       graph may have outliers that are not garbage collected root                           1                  1
       but are managed by other means. The one-field object
       at bottom right of the graph of objects (the dashed- root                                     graph
       line enclosed region) is unreachable, i.e., garbage.
                                                                                                                    outlier
   An OCaml object has a 1-word descriptor containing, among other things, the length of the object
in words (not counting descriptor) and an 8-bit tag that the mutator may use to distinguish data
constructors. Each word after the descriptor is a value unless the tag is ≥ 251, in which case all
words are considered nonpointers regardless of their last bit. The base address of an object is the
address of the first field after the descriptor. Minsky and Madhavapeddy [2022, Chapter 23] provide
details.


    Fig. 3. The mutator is given a con-
    tiguous space for allocation of new                                                                                1
                                                                           allocation




    objects, from address alloc to limit.
                                                                              arena




    When an 𝑛-field object is allocated,             alloc                                   alloc                   allocation
    the new object will be at address                limit                                   limit                      arena
    alloc + 1 · word_size;        one must
    add (1 + 𝑛) · word_size to alloc, and
                                                                                             root2
    initialize the fields. Here, the opera-                                  2                                         2
    tion root2=C(root1) is illustrated, for         root1                                    root1
    a unary data constructor C.
       The alloc and limit are compo-
    nents of the thread-info; see Figure 5.


   The g.c. must be able to find the live roots in the mutator’s stack and global variables. Some
garbage collectors do this by having the mutator’s compiler produce precise stack maps [Jones
et al. 2023, Chapter 11]; but our g.c. is meant for mutators written in C, and C compilers do not
produce such stack maps. Therefore we adapt a technique described by McCreight et al. [2010]—see
Figure 4. The mutator maintains a linked list of frames, one for each (nominal) stack frame of the C
program and stored as a local addressable struct within that stack frame.2
   The mutator’s C program need not keep the current function’s variables in the topmost frame-
struct while operating upon them; it can use ordinary local variables that the C compiler will keep
in registers. But before each function call, to another C function or to the collector, the C program
2We say nominal because the C compiler might choose to inline some function calls, in which case our linked list of

root-frames will not correspond 1-1 to C stack frames but will still be semantically correct: if the optimizing compiler inlines
function 𝑓 into 𝑔, the resulting function’s stack frame will have two root-frames in the linked list.
6                                                              Shengyi Wang, Kathrin Stark, and Andrew W. Appel




                                                                                          C funct. stack frame
                                                                   fp




                                                                                                                          frame
         Fig. 4. The C program maintains a linked list of frame
         structs within its own function-call stack, using the
         clever trick [McCreight et al. 2010] of declaring them                                                    root
         as addressable local structure variables. Addressable                                                     root
         local structures is one of those crazy features of C
         that can lead, if abused, to dangling pointers, so the




                                                                                          C function stack frame
         mutator’s correctness proof must show that this is




                                                                                                                          frame
         managed well. The g.c. doesn’t care where this linked
         list is stored, as long as it is separate from the heap
         and graph. Ordinary local variables such as 𝑥 that                                                        root
         contain live roots must be copied into the frame-struct
         before calling garbage_collect(), or calling functions                                                     x
         that might call garbage_collect. The frame-pointer fp
         is a component of the thread-info; see Figure 5.


struct thread_info {
   value ∗alloc;          /∗ beginning of allocation arena ∗/
   value ∗limit;          /∗ end of allocation arena ∗/
   struct heap ∗heap;     /∗ heap−management data structure, opaque to mutator ∗/
   struct stack_frame ∗fp; /∗ linked list of root frames ∗/
   unsigned int nalloc; /∗ number of words needed to allocate after collection ∗/
};

      Fig. 5. The mutator maintains a thread_info structure in which
                                                                                       alloc
                                                                        thread_info




                                                                                                                                  allocation
      it keeps its alloc and limit pointers, the heap management                       limit                                         arena
      pointer, its stack-of-frames pointer fp, and (when calling the                   heap
      g.c.) the number of words nalloc that it needs for the next-to-                     fp
      be-allocated object.                                                            nalloc
          The heap management data structure is an abstract data
      type. That is, the mutator keeps an opaque pointer to it and
                                                                                      stack of
                                                                                       frames




      never traverses it directly. In that data structure are all the                                               heap management
      free spaces of the older generations (but not the free space of                                                 data structure
      the nursery, which is the allocation arena), remembered sets                                                   (opaque to mutator)
      for mutable ref-updates, and the data structures to keep track
      of all the generations.


must store all local variables that might be live pointers into the topmost frame, and must fetch
them back after the call. The head of this linked list is the frame pointer fp.
   The thread info structure (Figure 5) allows the mutator and collector to communicate about
available space for allocation.
   All the memory words between alloc and limit are available for allocation.3 The heap field points
to the g.c.’s internal data structure that keeps track of memory regions and is opaque to the mutator.
When calling the collector (Figure 6), the mutator sets the frame pointer fp to the stack-of-frames
3 This is similar but not identical to OCaml’s interface.
Verification of a Generational Garbage Collector                                                                                                                                                7



    Fig. 6. Mutator’s view of the g.c.
    interface, at the time of calling




                                                                                                                                          allocation
                                                                                                                                                               heap management




                                                                                                                                             arena
    garbage_collect. The mutator is re-
                                                                              alloc                                                                              data structure




                                                              thread_info
    questing that the collector should                                        limit                                                                             (opaque to mutator)
    ensure at least 2 words in the alloca-                                    heap
    tion arena. As illustrated, there ap-                                        fp
    pear to be at least two words there                                      nalloc                          2
    already, and furthermore the muta-
                                                                                                                                                                  2                     2




                                                                                                                                  frame
    tor can determine this quickly by cal-
    culating limit−alloc, in which case
                                                                                                                                                                            3


                                                                                           stack of frames
    this call would be unnecessary.                                                                                        root
       The graph is quasi-opaque to the                                                                                    root                                   1                     1
    mutator’s correctness proof: that is,
    one block at a time can be visible
                                                                                                                                                                           graph



                                                                                                                                  frame
    using ramification lemmas.
       The outliers region is not garbage-
                                                                                                                           root
    collected but is managed separately
    by the runtime system or foreign                                                                                                                        outliers
    functions.


   Fig. 7. Allocating a new record.
   This is like Figure 3 but in the
   larger context. When not calling                                                                                                               1
   garbage_collect, roots in the top-                                                                                                                                  heap management
                                                                                           alloc                                                                         data structure
                                                                                                                                               allocation




   most frame are typically kept in
                                                                            thread_info




                                                                                                                                                  arena




   registers (i.e., nonaddressable lo-                                                     limit                                                                        (opaque to mutator)
   cal variables of the C program), as                                                     heap
                                                                                              fp
   is the thread-info pointer ti. The                                                     nalloc
   mutator stores roots into the top-
   most frame just before calling the
                                                                                                                                                                       2                    2
                                                                                                                                          frame
                                         registers / locals




   collector and fetches them back
                                                              ti
   afterwards (because the copying                            root                                                                                                               3
                                                                                                         stack of frames




   collector may have moved the ob-
   jects they point to). Here, the mu-                        root                                                                                                     1
   tator has just allocated a new ob-
                                                                                                                                                                                graph
                                                                                                                                      frame




   ject, by adjusting ti→ alloc (old
   value shown with dashed arrow)
   and making a local variable point                                                                                          root
   to the object (dotted arrow). This
   indicates that two words of mem-
   ory have left the allocation space
   and joined the graph.


data structure and sets nalloc to the number of words of free space needed to allocate the next
object(s).
  Updating a mutable reference. A generational garbage collector is permitted to assume that every
pointer is from a younger object to an older object, except as explicitly noted when updating a
mutable reference or array. The g.c. provides an mutable_update mechanism by which the mutator
8                                                                                  Shengyi Wang, Kathrin Stark, and Andrew W. Appel



    Fig. 8. Updating a mutable reference.
    The mutator has stored a new pointer
                                                                           alloc                            heap management




                                                            thread_info




                                                                                           alloc.
                                                                                           arena
    value (bold arrow) into a field that
                                                                           limit                              data structure
    previously pointed elsewhere (dashed                                   heap                              (opaque to mutator)
    arrow). It must do so by calling the                                      fp
    mutable_update function, which (in ad-                                nalloc
    dition to storing the new value as
    shown) adds the address to the remem-                                                                  2                2



                                                 registers / locals
    bered set (part of the heap manage-                               ti
    ment data structure). One might notice                            x                                            3
                                                                               update(ti,y,x);
    as well that limit has changed (from                              y                                    1              graph
    the dashed arrow to the solid arrow);
    mutable_update has stolen a word from
    the end of the allocation space to add to
    the remembered-set data structure.



                                                                                                    2 t            2
                                                                                                    p
                                                                                    x               q      3
    Fig. 9. Fetching a field of an object. The muta-
                                                                                    y               1
    tor can fetch field 0 or field 1 of pointer 𝑥. To                                                              1
    reason about that in separation logic, the Certi-
    Graph library provides ramification lemmas for fo-                                                    graph
    cusing on a single object. One such lemma proves
    that the original graph predicate 𝑔 is equivalent
    to 𝑥 ↦→ (2, 𝑝, 𝑞) ∗ (𝑥 ↦→ (2, 𝑝, 𝑞) −∗ 𝑔).                                                2 t
       In this illustration, 𝑡 is the constructor tag. The                                    p                    2
    mutator can fetch 𝑥 [−1] and bitwise-and with bi-                                         q
                                                                                    x                      3
    nary 000...00011111111 to get the tag, which it may
                                                                                    y               1
    need for discriminating on data constructors.                                                                  1


                                                                                                          graph′


can inform the g.c. of ref-updates; see Figure 8. This information is kept in a remembered set within
the heap management data structure.
   Dereferencing a pointer. The graph (depicted in Figure 2 and Figure 6) is a quasi-opaque data
structure. That is, the mutator program has pointers directly to objects within it, and can directly
fetch fields of those objects; but reasoning about these objects in separation logic is not so simple.
Separation logic is very natural for trees, where we know that the left subtree and the right
subtree occupy disjoint memory regions; and we can use it to assert that the thread_info struct
is disjoint from the allocation arena, both of which are disjoint from the stack of frames, and the
heap management data structure, and so on. But the object graph is not a tree structure; when
constructing 𝐶 (𝑥, 𝑦) for some constructor 𝐶, it may be that 𝑥 and 𝑦 are the same pointer, or 𝑥 points
within 𝑦 (there is a path from 𝑦 to 𝑥). To reason about this, we need to focus on one object within
the graph as shown in Figure 9. See, for example, the Localize rule of Wang et al. [2019, Equation
1].
Verification of a Generational Garbage Collector                                                                      9



   Fig. 10. Outlier data structures can point into the graph,
                                                                          (roots)
   but they must be registered using mutable_update.                                                   machine
      A function closure (such as the “2” object in this graph)                                          code
                                                                                                2
   has a code pointer to the start address of a machine-                                                  for
   language function and an environment 𝑒, a value typically                                    e      function
                                                                                    3
                                                                                                           f
   represented by graph nodes, representing the free vari-
                                                                                                1
   ables of the function. The code pointer is typically not a
   graph node itself, but needs to be accounted for in the                                                    data
                                                                                        graph                struc-
   separation-logic predicates; we call it an outlier.
                                                                                                              ture
      Another use for outliers is for opaque data structures                                               managed
   managed by a foreign function (i.e., a C function in the                                                   in a
   runtime system, callable from the functional program that                                                foreign
   uses OCaml data types). The functional program cannot                                    outliers       function
   dereference such pointers, but can pass them as arguments
   back to the foreign function.


   Outliers. Function closures, such as the one in Figure 10, point into the compiled program, to
addresses that may not be convenient to represent as graph nodes, i.e., addresses outside the heap.4
In the CompCert C semantics, pointer values may be in an allocated state or a freed state. It is
illegal to do any operation on a freed pointer value, even address comparison [Leroy et al. 2014].
The garbage collector does need to do address comparisons on function-pointer values, since any
pointer field within a graph object may need to be tested to see whether it is within the bounds of
the from-space (see section 5). Therefore, in VST’s program logic (proved sound w.r.t. the CompCert
semantics), to do address comparisons on function pointers, we need to reason explicitly about
the validity of such pointers. For that reason, our correctness specification and proofs maintain an
outlier set of known-valid pointers.
   Another use for outliers is to implement pointers to objects managed by the runtime system (or
by foreign functions). The mutator cannot directly deference such pointers (since the focusing-by-
ramification lemma applies only to objects in the graph), but fields of graph objects can contain
such pointers, and the mutator can pass them to foreign function calls which will know how to
traverse those objects.
   Such foreign data structures might even contain pointers back into the graph. The foreign
function can register such roots by calling mutable_update (see subsection 2.1).

2.1   API operations
In summary, the API for the mutator must support the following operations:
     • available(ti,n) Test whether there is enough space in the nursery to allocate a new
        object with 𝑛 fields. This is simply (ti→ limit)−(ti→ alloc) ≥ n+1.
     • alloc(ti,𝑑,𝑣 1 ,...,𝑣𝑛−1 ) With precondition that enough space is available, allocate a new
        object with descriptor 𝑑, with 𝑛 pointer fields or 𝑛 words of nonpointer data (depending
        on the descriptor’s tag), and initialize all the pointer fields with given data. This is simple:
        p=ti→ alloc+1 is the address of the new object, ti→ alloc+=n+1 allocates the space, p[−1]=d
        initializes the descriptor word, and, for each 𝑖, p[𝑖]=𝑣𝑖 initializes the fields.
     • dereference(p,i) Given a pointer 𝑝 to an 𝑛-field object in the graph and a number 𝑖 < 𝑛,
        fetch the 𝑖th field of the object into a local variable.
4 Unless, of course, your ML compiler does put all machine code into movable graph objects [Appel 1990].
10                                                        Shengyi Wang, Kathrin Stark, and Andrew W. Appel


      • garbage_collect(ti) Invoke the garbage collector to ensure that the allocation space
         contains least ti→ nalloc, by reclaiming dead objects and/or asking the operating system
         for more virtual memory.
      • mutable_update(ti,p,x) Store value 𝑥 into a field at address 𝑝 within an existing object
         𝑏. This not only performs ∗p=x; but also (if 𝑥 is a pointer) adds address 𝑝 to the remembered
         set (see Figure 8). The field offset (𝑝 − 𝑏) need not be a constant; the mutator could compute
         it, i.e., subscript an array. Thus, this operation handles updateable arrays as well as mutable
         references. The function does not need to know the address 𝑏, only the field address.
   During all these operations, the mutator has access to the general thread information structure,
but the heap management data structures and the graph’s internal representation remain opaque
to it.

3     Formal specification of the collector
The mutator builds and traverses a directed graph of object pointers. The garbage collector’s job is
to delete unreachable objects and rearrange the reachable ones so that the free space is contiguous
(to allow fast allocation). The mutator is not supposed to care about the exact addresses of objects,
only the structure of the graph. Therefore, if the collector removes unreachable objects from the
graph, and moves reachable objects to new addresses while leaving a graph isomorphic to the
reachable subgraph of the original graph, the mutator should not notice the difference.
   We have told this story in pictures. Now we will express those pictures as resource predicates in
separation logic for the different API operations. Each specification has a precondition PRE with
a PROPositional component, a PARAMeter-value component, a GLOBALs linkage, and a spatial
component that is a SEParating conjunction of resources. The POSTcondition has a PROPositional
component, a RETURN-value specifier, and a spatial (SEP) component.

3.1    Garbage collection
Listing 11 gives an abridged and partially expanded presentation of the VST funspec, or function
specification, for the garbage_collect function. In the mechanized development, the spatial resources
shown explicitly here are packaged in the auxiliary predicate gc_sep. We expand them in this
listing so that their roles can be explained individually.
   The SEP component of the garbage_collect precondition.
The precondition’s first spatial conjunct (Listing 11 line 9) is a separation- ti −→ alloc
logic “points-to,” written in VST as data_at sh thread_info_type 𝑣 ti, where                 limit
in this case 𝑣 is a 5-tuple because struct thread_info has 5 fields. This                    heap_p
data_at describes the picture at right (compare with upper left of Figure 6).                fp
Value ti is a pointer to a struct thread_info with those five field values.                  nalloc
The value alloc is the address of the allocation space shown in Figure 6, alloc+WORD_SIZE∗avail is
the limit, heap_p is the address of the heap-management data structure, and so on.
   The values alloc, avail, etc., are quantified in lines 2–4; that is, whenever the garbage_collect
function is called, (the proof of) the caller must exhibit some values of those quantified variables
that will make all the precondition predicates satisfiable. In lines 2-4, the val type is a CompCert
value (typically a pointer value), Z is Rocq’s integer type, Ptrofs.int is the type of integers modulo
2𝑘 (if integers are 𝑘 bits and 𝑘 = 8 · word_size).
   The conjunct alloc_space alloc avail describes another part of Figure 6, the region in which the
mutator may allocate new records:
     Verification of a Generational Garbage Collector                                    11


                                       Listing 11. Function spec. of garbage_collect
 1   DECLARE _garbage_collect
 2   WITH rsh: share, sh: share, gv: globals, ti: val, g: LGraph, h: heap,
 3          alloc: val, avail: Z, heap_p: val, frames: list frame, nalloc: Ptrofs.int,
 4          roots : roots_t, outlier: outlier_t
 5   PRE [tptr thread_info_type]             (∗ struct thread_info ∗ti ∗)
 6     PROP (readable_share rsh; writable_share sh;
 7             full_gc g h (frames2rootpairs frames) roots outlier)
 8     PARAMS (ti) GLOBALS (gv)
 9     SEP (data_at sh thread_info_type
10              (alloc, (alloc + WORD_SIZE ∗ avail,
11                             (heap_p, (ti_fp frames, Vptrofs nalloc))))
12              ti;
13           allocation_space alloc avail;
14           graph_rep g;
15           frames_rep sh frames;
16           heap_management h heap_p;
17           outlier_rep outlier;
18           mem_mgr gv; all_string_constants rsh gv)
19   POST [tvoid]               (∗ this is a void−returning function ∗)
20     EX g': LGraph, EX frames': list frame, EX h': heap, EX roots': roots_t,
21     EX alloc': val, EX avail': Z,
22     PROP (full_gc g' h' (frames2rootpairs frames') roots' outlier;
23              garbage_collect_relation roots roots' g g';
24              frame_shells_eq frames frames';
25              Ptrofs.unsigned nalloc <= avail')
26     RETURN ()
27     SEP (data_at sh thread_info_type
28              (alloc', (alloc' + WORD_SIZE ∗ avail',
29                                (heap_p, (ti_fp frames', Vundef))))
30              ti;
31           allocation_space alloc' avail';
32           graph_rep g';
33           frames_rep sh frames';
34           heap_management h' heap_p;
35           outlier_rep outlier;
36           mem_mgr gv; all_string_constants rsh gv).



                                     alloc −→



         alloc + WORD_SIZE · avail −→
12                                                                       Shengyi Wang, Kathrin Stark, and Andrew W. Appel


   The conjunct frames_rep sh frames (fig. 11 line 15) describes the linked-list-of-frames data
structure, with ti_fp(frames) being the start address of the list.
   On line 18, heap_management h heap_p is the heap management data structure, rooted at
address heap_p, whose contents are described by the h value. This conjunct does not describe the
actual objects of the heap, just the management data structures. The structure of the heap type
need not be known by the mutator (or by its proof of correctness).
   The graph_rep conjunct (line 14) describes all the graph objects shown in Figure 6. Unlike the
other conjuncts, it does not have a single root address (such as ti, alloc, or ti_fp(frames)). Instead,
the labeled-graph type (LGraph) describes an address for each vertex of graph g. To characterize
this formally, we describe a directed graph structure in Rocq using the CertiGraph library [Wang
et al. 2019] (github.com/CertiGraph/CertiGraph). This library can describe the embedding into VST
separation logic of vertices, edges, vertex labels, edge labels, and so on.
   Objects outside the garbage-collected heap, that may point into the heap or may be targets of
pointers within the heap, we call outliers. That’s a separate region of memory characterized by the
predicate outlier_rep.
   The last two separating conjuncts (line 18) give the g.c. access to the malloc/free memory manager
(in case it wants to create a new generation, for example) and the read-only string literals of the
program (in case it wants to print an error message).
   The current mechanized definition of gc_sep additionally contains heap_remset_rep and remset_rep,
which represent the collector’s concrete and logical remembered-set state. These internal book-
keeping resources are omitted from Listing 11; their role in the correctness argument is discussed
in subsection 7.3.
   The PROP component of the garbage_collect precondition. The propositional component of the
precondition states that the quantified values of the WITH clause must satisfy these propositions:
the graph g must be compatible with the heap h, the stack of frames, the roots within those frames,
and the outliers. In addition, the permission-share rsh (used for accessing string literals) gives at
least read permission, and the share sh gives the frames data structure at least write permission.
   The garbage-collect postcondition. The garbage collector produces a new graph g' with new roots'
that live within an adjusted frames'. It provides a fresh allocation space beginning at address alloc'
containing avail' words; and it updates its heap-management data structure to abstract value h'.
The postcondition starts with existential quantifiers for all of these values; in the PROP clause it
asserts that all these values are compatible with each other; and in the SEP clause it asserts that all
these values are represented in memory.
   In addition, there are two PROP clauses relating the old graph to the new graph (garbage_collect_relation)
and relating the old stack of frames to the new one (frame_shells_eq); see also Figure 12. The last
PROP clause guarantees that the allocation space is big enough to satisfy the mutator’s request.
   We have proved several properties of garbage_collect_relation 𝑟 1 𝑟 2 𝑔1 𝑔2 . In particular, under
appropriate conditions (that are satisfied immediately after a completed collection), there is a graph
isomorphism between the reachable subset of graph 𝑔1 with roots 𝑟 1 and the reachable subset of 𝑔2
with roots 𝑟 2 (garbage_collect_isomorphism).5

3.2    Proving correctness of mutator operations
  Correctness of allocating an object. Recall that alloc allocates and initializes a new object with
descriptor 𝑑 and supplied values 𝑣 1, . . . , 𝑣𝑛 . Operationally, it chooses the address of the new object,
5 You might think that, after a collection, graph 𝑔
                                                    2 is the same as its reachable subset; but that is not true of a generational
collector, which is not obligated to collect all the garbage at every collection.
     Verification of a Generational Garbage Collector                                                                       13


                                                                             fp                     fp
                                                                                   f1                     f1




                                                                                            frame




                                                                                                                    frame
               Fig. 12. The copying garbage collector may
               move any or all of the root objects 𝑥, 𝑦, 𝑧 to new
               addresses 𝑥 ′, 𝑦 ′, 𝑧 ′ . But the addresses of all the             r1    x                r1    x′
               frames (𝑓1, 𝑓2, 𝑟 1, 𝑟 2, 𝑟 3 ) in the stack-of-frames             r2    y                r2    y′
               must stay the same. This relation is expressed by
               the predicate frame_shells_eq.                                      f2                     f2




                                                                                            frame




                                                                                                                    frame
               The function frames2rootpairs takes an abstract
               list(frame) value such as this, and extracts to the                r3    z                r3    z′
               list of address/value pairs [(𝑟 1, 𝑥); (𝑟 2, 𝑦); (𝑟 3, 𝑧)].


     Listing 13. Schema of the function specification of alloc. The predicate in_graph is typically type-directed
     and therefore the values 𝑣 1, . . . , 𝑣𝑛 have types 𝑋 1, . . . , 𝑋𝑛 , respectively. The notation app d [v1, ..., vn] is
     an abuse of notation: it represents the application of a typed constructor, described by the descriptor d, to a
     list of arguments. See section 4 of [Korkut et al. 2025] for further details.
 1   DECLARE _alloc_spec
 2      WITH rsh : share, sh: share, gv : globals, ti : val, g : LGraph,
 3           roots : roots_t, sh : share, outlier : outlier_t, t_info : thread_info
 4           p1 ... pn : rep_type, d : cRep, v1 ... vn : X1... Xn
 5      PRE [tptr thread_info_type; val; int_or_ptr_type; ...; int_or_ptr_type)
 6         PROP (readable_share rsh; writable_share sh;
 7                 full_gc g c t_info roots outlier;
 8                 in_graph g outlier v1 p1, ..., in_graph g outlier vn pn;
 9                 add_node_compatible g [v1...vn];
10                 n < headroom t_info;
11                 mem_mgr gv; all_string_constants rsh gv
12                 )
13         (PARAMS (ti, rep_type_val p1, ..., rep_type_val pn))
14         (GLOBALS [gv])
15         (SEP (gc_sep g t_info roots outlier ti sh gv))
16      POST [ int_or_ptr_type ]
17        EX (p' : rep_type) (g' : graph) (t_info' : thread_info),
18          PROP (in_graph g' outlier (app d [v1, ..., vn]) p';
19                   ti_frames t_info = ti_frames t_info';
20                   gc_graph_iso g roots g' roots;
21                   headroom t_info' = headroom t_info − Z.of_nat (S n))
22          RETURN (rep_type_val g' p')
23          SEP (gc_sep g' t_info' roots outlier ti sh gv).


     advances the allocation pointer by the required number of words, writes the descriptor word, and
     initializes the object fields. However, a specification that described only this low-level memory
     update would be too weak to compose with the garbage collector and with later operations on
     graph-structured values. The actual specification is shown in Figure 13.
14                                                         Shengyi Wang, Kathrin Stark, and Andrew W. Appel


   The precondition contains the same assumptions as the garbage-collector specification. In
particular, the spatial part describes the thread-info structure, the linked list of stack frames, heap-
management data, and the concrete representation of the graph. In the mechanized development,
these spatial resources are packaged in the predicate gc_sep. The schematic specification above
suppresses its remembered-set parameters, which are unchanged by this allocation operation.
   There are two additional requirements specific to allocation. First, the allocation area must
contain enough free space. (We discuss the workflow for checking this condition before calling
alloc in the next subsection.) For a thread-info structure t_info, the available space is computed
as the distance between the current allocation pointer and the allocation limit; we write this as
headroom t_info and require this headroom to be larger than 𝑛.
   Second, the specification must describe the values and their location passed as fields of the new
object. Such values may be immediate data, represented by repZ z; outlier pointers, represented
by repOut p; or pointers to nodes in the graph, represented by repNode v. These alternatives are
captured by the type rep_type which can be transformed to the C value type using the function
rep_type_val.
   As the mutator should not know about the exact graph layout in memory, the propositional part
of the precondition contains predicates of the form in_graph g outlier v_i p_i that should entail at
least how the values are encoded in the graph. Usually it is stronger, and in a type-directed manner
might add additional propositional information to simplify later reasoning, such as the existence
of subvalues in the graph. The predicate in_graph is intentionally parameterized, since different
clients may use different type-specific representation predicates. Nevertheless, it must satisfy a
small of structural properties, as being stable under graph extension and graph isomorphism.
   The postcondition produces a new graph 𝑔′ and a new thread-info structure t_info'. Since
allocation does not perform garbage collection, the root set and linked list of stack frames are
unchanged. Moreover, 𝑔′ is isomorphic to the old graph 𝑔 on the previous roots.
   Additionally, the graph contains (at position 𝑝 ′ ) the new object app d [v1,...,vn] whose descriptor
is 𝑑, with edges from this fresh node to the graph values among 𝑣 1, . . . , 𝑣𝑛 . These minimal conditions
are fulfilled by the “constructor representation predicate“, graph_cRep g p (boxed d n) [p1 ... pn]
that represents (in this example) a boxed constructor (a record pointer, not an unboxed integer) with
tag 𝑑 and length n, whose out-edges are labeled with 𝑝1...𝑝𝑛. To preserve well-formedness of the
graph and heap, the newly introduced edges must originate only from the freshly allocated node;
their targets must already be valid graph nodes or permitted outliers; and no duplicate edge should
be introduced. This is ensured by the add_node_compatible predicate. These side conditions are
satisfied naturally when allocating constructor nodes.
   Finally, the postcondition records the effect on the allocation area. The new thread-info structure
has the same stack-frame list as before, but its available nursery space has decreased by 𝑛 + 1 words:
one word for the descriptor and 𝑛 words for the fields. Although this fact could be recovered by
invoking the availability predicate again, storing the updated value of headroom directly in the
postcondition makes subsequent allocation proofs more convenient.
   Ensuring enough space for allocation. To ensure that there is enough space to allocate one or
more objects whose size (including descriptors) totals 𝑛, the mutator calls the available test before
allocating (Listing 14).
   We separate the available test from the garbage_collect call for two reasons. First, it avoids the
cost of storing and fetching root pointers in the common case that no collection is needed. Second,
if an extended basic block (tree of control flow) will predictably allocate several records whose total
size is ≤ 𝑛, multiple available tests can be coalesced into a single one.
    Verification of a Generational Garbage Collector                                                               15


                                     Listing 14. Ensuring space to allocate an object
1   if (!available(ti,n)) {
2        store root pointers into the topmost frame;
3        ti→ nalloc=n;
4        garbage_collect(ti);
5        fetch root pointers back from the topmost frame;
6   }


      To allocate a new object, the mutator will now always first ensure there’s enough space. If it
    needs to call the garbage collector, it simply passes the ti pointer. To prove correctness of this call,
    the mutator proof must satisfy the precondition of garbage_collect; that is, demonstrate values
    rsh, sh, gv, ti, g, h, alloc, etc. such that all the propositions in the precondition hold and all the
    separating conjuncts (thread-info struct, allocation space, graph, etc.) exist in memory.
      The postcondition of the if-statement in Listing 14, whether or not the then branch is taken, is
    that that limit − alloc ≥ 𝑛. This allows the allocate operations illustrated in Figure 7 to be proved
    correct.
       Correctness of dereferencing a pointer. Consider a pointer p to an object with 𝑛 fields in the graph
    and an index 𝑖 < 𝑛. The function dereference(p,i) retrieves the 𝑖-th field of the object into a local
    variable. Operationally, this corresponds to the C statement y = x[𝑖];, where x is the memory address
    of the object in the graph. Throughout this section we use the example shown in Figure 9, with
    𝑖 = 0.
       Since dereference only reads the graph and never modifies it, its specification (Listing 15) requires
    substantially weaker assumptions about the garbage collector layout than for example allocation.
    The only spatial requirement is that the graph is represented in memory. Again, the existence of
    the particular node being dereferenced are expressed in the propositional part of the assertion.
       Again, the particular node will be described in the propositional part, here via the in_graph
    predicate. In case that (as in Figure 9) 𝑣 describes a constructor with two arguments, recall that this
    predicate would imply the “constructor representation predicate“, graph_cRep g vx (boxed t 2) [p;q]
    that represents (in this example) a boxed constructor with tag 𝑡 and length 2, and out-edges that
    are labeled with 𝑝 and 𝑞. Additionally, this predicate typically implies propositional predicates
    describing the values at 𝑝 and 𝑞, added to the postcondition.
       In order for the VST separation Hoare logic to dereference a pointer 𝑥, there must be a sep clause
    of the form 𝑥 ↦→ (𝑣 0, 𝑣 1, . . .), written in VST as data_at 𝜋 𝜏 [𝑣 0 ; 𝑣 1 ; . . .] 𝑥, with 𝜋 a permission-share
    and 𝜏 a C struct or array type. We employ CertiGraph’s focusing rule to transform the precondition
    into:
    let 𝐴:= data_at graph_rep g (Tarray int_or_ptr_type 2) [rep_type_val g p; rep_type_val g q])
    in PROP(graph_cRep g vx (boxed t 2) [p;q])
        ...
        SEP(𝐴; 𝐴 −∗ graph_rep g)
    This is just as illustrated in Figure 9, and the conjunct 𝐴 is sufficient to fetch x[0] or x[1].
      After the fetch, one can simply use wand adjointness to transform
    𝐴 ∗ (𝐴 −∗ graph_rep g) back into graph_rep g.
16                                                        Shengyi Wang, Kathrin Stark, and Andrew W. Appel


                                  Listing 15. Funspec for dereference
DECLARE _dereference2
 WITH g : graph, outlier : outlier_t,
      v: X, vx: rep_type
 PRE [int_or_ptr_type]
 PROP (in_graph g outlier (app v.descr v.proj1 v.proj2) vx)
  PARAMS (rep_type_val g vx)
  GLOBALS (gv)
  SEP (graph_rep g)
 POST [tptr int_or_ptr_type]
 EX (p q: rep_type) (sh: share),
 PROP (in_graph g outlier x.proj1 p; in_graph g outlier x.proj2 q; writable_share sh)
 RETURN (rep_type_val g p)
 SEP (let A := data_at sh (Tarray int_or_ptr_type 2)
                      [rep_type_val g p; rep_type_val g q] (rep_type_val g vx)
   in A ∗ A −∗ graph_rep g).


  Correctness of updating a mutable reference. Listing 16 shows the function specification for
mutable_update(ti,p,x), which sets a mutable reference (or array slot) at address p to value x. It
works on similar principles as those discussed above.

3.3   Adequacy claim
In section 6 and section 7 we will prove that the garbage collector (with all the operations listed at
the beginning of subsection 2.1) implements its specification (including the funspecs in Listing 11
and 16, along with supporting lemmas mentioned in subsection 3.2). But whenever one proves
that a program module implements an API specification, one must wonder whether it is really the
right specification. The most reliable way to demonstrate adequacy of a specification is to use that
specification to prove correctness of clients of that API.


   Theorem 1. The g.c. specification is adequate for proving correctness of mutators that allocate and
traverse data structures.
   Proof. Our garbage collector has been used in the runtime system of CertiRocq, a compiler
from Rocq to C that uses OCaml data representations. The Verified Foreign Function Interface
(VeriFFI) for CertiRocq [Korkut et al. 2025, sections 9 and 11] supports proofs of correctness of
client programs that exercise the garbage collector.                                           □
   Section 9.2 of Korkut et al. summarizes the Rocq/VST proof of a function uint63_to_nat that
converts an unboxed 63-bit unsigned integer to a Peano natural number represented with data
constructors S and O (see Listing 17). Lines 5–12 implement the pattern shown in Listing 14.
Because the local variable temp is live after the call to garbage_collect, and it may contain a heap
pointer, it must be stored into the stack of frames (at line 6) and fetched back afterwards (at line
11). Lines 7,8,11 implement pushing and popping from the stack of frames; note that both roots
and fr are addressable local variables. The function alloc_make_nat_S is an instance of the alloc
API operation, specialized to a 1-field record; a precondition of this function is that at least 2 words
of space remain between alloc and limit; this is ensured by the if statement.
Verification of a Generational Garbage Collector                                                      17


                                     Listing 16. Funspec for mutable_update
Definition int_mutable_update_spec :=
 DECLARE _mutable_update
    WITH ti: val, v: exterior_t, t_info: thread_info, sh: share, g: LGraph,
          it: interior_t, outlier: outlier_t, rh: remset_heap
 PRE [tptr thread_info_type, tptr int_or_ptr_type, int_or_ptr_type]
 PROP (writable_share sh;
        1 <= headroom t_info;
        graph_heap_compatible g (ti_heap t_info).(pt_heap);
        remset_heap_and_heap_compatible rh (ti_heap t_info).(pt_heap);
        mutable_location_compatible g it;
        exterior_compatible g outlier v)
    PARAMS (ti; interior_address it g; exterior2val g v)
    GLOBALS ()
    SEP (graph_rep g;
          outlier_rep outlier;
          before_gc_thread_info_rep sh t_info ti;
          heap_remset_rep g (ti_heap t_info).(pt_heap) rh)
 POST [tvoid]
    EX g': LGraph, EX t_info': thread_info, EX rh': remset_heap,
    PROP (mutable_graph_update g it v g';
            t_info' = decr_info_nursery t_info (exterior2val g v);
            rh' = mtb_upd_remset_heap (exterior2val g v) (RemSetInterior it) rh)
    RETURN ()
    SEP (graph_rep g';
          outlier_rep outlier;
          before_gc_thread_info_rep sh t_info' ti;
          heap_remset_rep g' (ti_heap t_info').(pt_heap) rh').


   In the function uint63_to_nat, at the time one decides to allocate a new record (at line 5), all
the values to be used in initializing fields of that record are already in local variables (in this case,
temp). This is typical of how programs allocate. But Section 11 of Korkut et al. describes a more
challenging case: converting a list of characters into a packed bytestring. In this case, since the
length of the string is dynamic without an a priori bound, the values to be stored cannot all be in
local variables at once; during the loop that initializes the fields, the mutator must also traverse
(dereference) data structures in the graph. During that loop, the full_gc invariant does not hold,
since there is already partially allocated record. Therefore, the precondition (and postcondition) of
the dereference operation must be (and is) weaker than full_gc.

4   Garbage collector implementation
We have implemented (and verified) a multi-generation copying collector inspired by the one that
Reppy [1993] built for Standard ML. Because we want the specifications and proofs of components
of the collector to be independent of the precise details of how the generations work, we will first
describe some abstract principles.
     18                                                             Shengyi Wang, Kathrin Stark, and Andrew W. Appel


                        Listing 17. A function that allocates; see Figure 2 of Korkut et al. [2025]
 1   value uint63_to_nat (struct thread_info ∗tinfo, value t) {
 2     uint64 i = ((uint64)t)>>(uint64)1; /∗ strip off the tag ∗/
 3     value temp = make_nat_O(); /∗ create the base case ∗/
 4     while (i) {
 5       if (available(tinfo, 2)) { /∗ test whether we need to call g.c. ∗/
 6          value roots[1]={temp}; /∗ register the root−pointer temp ∗/
 7          struct stack_frame fr = {roots+1,roots,tinfo→ fp};
 8          tinfo→ fp= &fr;
 9          tinfo→ nalloc = 2; /∗ state the need for 2 words ∗/
10          garbage_collect(tinfo);
11          temp=roots[0]; tinfo→ fp=fr.prev; /∗ pop the frame stack ∗/
12       }
13       temp = alloc_make_nat_S(tinfo, temp); /∗ apply S constructor to temp ∗/
14       i−−;
15     }
16   return temp;
17   }


        The heap is a sequence of 𝑁ℎ spaces (see Listing 18). Each space is a contiguous region of memory
     from space_start to space_start+total_space. In each space, the portion up to space_start+used_space


          Listing 18. Rocq code describing the functional model of a space, and a heap as a squence of spaces.
     Record space : Type := Build_space {
        space_start: val;
        used_space: Z;
        available_space: Z;
        total_space: Z;
        space_sh: share;
        used_leq_available: 0 ≤ used_space ≤ available_space;
        available_leq_total: available_space ≤ total_space;
        space_upper_bound: total_space <= MAX_SPACE_SIZE; }.

     Record heap : Type := Build_heap {
        spaces : list space;
        spaces_size : Zlength spaces = MAX_SPACES }.


     Listing 19. The C structs characterizing a heap. Not shown are the separation logic predicates space_rep
     and heap_rep that relate these to space and heap in the obvious way: used_space between start and next,
     available_space between start and limit, total_space between start and rem_limit.
     struct space { value ∗start, ∗next, ∗limit, ∗rem_limit; };
     struct heap { struct space spaces[MAX_SPACES]; };
Verification of a Generational Garbage Collector                                                         19


                                                   Listing 20.
Definition graph_heap_compatible (g: LGraph) (h: heap): Prop :=
 let 𝑁𝑔 := length g.(glabel).(g_gen) in
 (∗ each active generation is compatible with the graph ∗)
 Forall (generation_space_compatible g)
          (combine (combine (nat_inc_list 𝑁𝑔 ) g.(glabel).(g_gen)) h.(spaces)) ∧
 (∗ each inactive generation's space−pointer is NULL ∗)
 Forall (eq nullval) (skipn 𝑁𝑔 (map space_start h.(spaces))) ∧
 (∗ There are not more active generations than the length of the array ∗)
 𝑁𝑔 <= length h.(spaces).


contains graph objects; the portion from there to space_start+available_space is available for allo-
cating new objects; and the remainder up to space_start+total_space is used for other purposes.
(The space_sh is a permission share, and other invariants will generally enforce that space_sh gives
the g.c. at least read+write permission on its heap spaces).
    For example, in a simple Cheney-style copying collector there are two spaces (𝑁ℎ = 2). In each
space, available_space is equal to total_space. The mutator’s alloc is set to space[0].space_start
and its limit is set to space[0].space_start+available_space. The mutator allocates in space 0 until
it reaches its limit. Then the g.c. copies (forwards) all reachable objects into space 1, and the spaces
swap roles (meaning that the mutator’s alloc is set to space[1].space_start before resuming).
    In our collector, there are 𝑁ℎ generations, each twice as large as the last.
    In either of these arrangements, every graph object must live in the used part of one of the
spaces. Each graph vertex is labeled with its space-number in the range [0, 𝑁𝑔 ). Spaces in the range
[𝑁𝑔 , 𝐻ℎ ) must be marked as inactive, space_start=nullval.
    The predicate graph_heap_compatible characterizes these properties (Listing 20).

5     Cheney’s algorithm
At the heart of a generational copying collector is an algorithm for a copying a from-space to a
to-space—see Jones et al. [2023, Chapter 4]. For that we use Cheney’s algorithm [Jones et al. 2023,
Algorithms 4.2+4.3], with a variation for local depth-first traversal [Jones et al. 2023, Section 4.2] to
improve cache locality. Figure 21 illustrates Cheney’s algorithm.
   Garbage collectors traverse object graphs, by depth-first search or breadth-first search or by other
means. Depth-first search requires an auxiliary stack; breadth-first search requires an auxiliary
queue. One can avoid a separate stack by using pointer reversal within the graph, but this has high
overhead. The beauty of Cheney’s breadth-first algorithm is that the space between scan and next is
the queue, so no auxiliary structure is required. But the disadvantage of pure breadth-first copying
is that, if 𝑥 points to 𝑦, 𝑥 and 𝑦 are unlikely to be adjacent after copying. If they are in different cache
blocks, then memory locality will suffer. In contrast, depth-first search improves cache locality in
traversing data structures. A reasonable compromise is to use mostly breadth-first copying with
local depth-first copying, which uses an auxiliary stack of bounded depth. Lines 21-24 of Listing 22
implement this. We have proved it correct, but we have not done extensive measurements of its
performance.

5.1    The forward Function
The forward function performs the core operation of Cheney’s algorithm. Its implementation is
shown in Listing 22.
20                                                                           Shengyi Wang, Kathrin Stark, and Andrew W. Appel



                  from-space         to-space from-space                 to-space from-space                 to-space
                                                      scan                              scan                             scan
                         2                            next                  2                                   2
                         p                                                      p                                   p
                         q                                                      q       next                        q
             x           1                        x           1                     x             1             2
             y                                    y                                 y
                         2                                    2                                                          next


                         1                                    1                                   1

                         2                                    2                                   2



                               (A)                           (B) root x forwarded              (C) roots x,y forwarded
                                         2                                  2                                   2
                                         p            scan                  p                                   p
                                             q                              q           scan                    q
             x           1               2        x           1             2       x             1             2
             y                                    y                                 y

                                         2                                  2                                   2
                                                                                                                         scan
                         1                            next    1                         next      1                      next




                     (D) first field forwarded           (E) second field forwarded        (F) more fields forwarded


                                     2                               Fig. 21. Cheney’s algorithm. At the start, scan
                                     p
                                     q                               and next point at the beginning of the to-
         x           1               2                               space. First, the roots are forwarded, meaning
         y                                                           that the contents of records they point to are
                                                                     copied verbatim and a forwarding pointer (dot-
                                     2
                                                 scan                ted line) is installed. The ★ indicates records
                     1                           next                that have been forwarded. Then, each field be-
                                                                     tween scan and next is forwarded. Eventually
                                                                     scan catches up with next, and the algorithm
                                                                     is finished; the entire from-space may now be
                                                                     re-used for other purposes.
                 (G) scan catches up to next


     Line 2: next is a pointer-to-pointer so that it can be advanced as illustrated in Figure 21.
     Line 4: To test whether the last bit is 0 or 1, indicating pointer or nonpointer (respectively),
       we must use the function is_ptr, which in turn uses test_int_or_ptr; see Appendix B for an
       explanation of that and of int_or_ptr_to_ptr and ptr_to_int_or_ptr.
     Line 6: The Is_from function needs to be specially axiomatized; see Appendix C.
     Line 7: Hd_val indexes v[−1] to fetch the object descriptor, and at line 11 Wosize_hd extracts
       the size field from the descriptor.
     Line 8: The test hd==0 detects the ★ mark illustrated in Figure 21, and line 18 places the ★
       mark.
     Verification of a Generational Garbage Collector                                                                   21


                                              Listing 22. The forward function
 1   void forward (value ∗from_start, value ∗from_limit,
 2                       value ∗∗next, value ∗p, int depth) {
 3     value ∗v, va = ∗p;
 4     if (is_ptr(va)) { /∗ see Appendix B ∗/
 5        v = (value∗)int_or_ptr_to_ptr(va);
 6        if (Is_from(from_start, from_limit, v)) { /∗ see Appendix C ∗/
 7           header_t hd = Hd_val(v);
 8           if (hd == 0) {
 9              ∗p = Field(v,0); /∗ already forwarded, follow forwarding pointer ∗/
10           } else { /∗ copy to to−space and install forwarding pointer ∗/
11              int i, sz=Wosize_hd(hd);
12              value ∗newv = ∗next+1;
13              ∗next = newv+sz;
14              Hd_val(newv) = hd;
15              for(i = 0; i < sz; i++) {
16                 Field(newv, i) = Field(v, i);
17              }
18              Hd_val(v) = 0;
19              Field(v, 0) = ptr_to_int_or_ptr((void ∗)newv);
20              ∗p = ptr_to_int_or_ptr((void ∗)newv);
21              if (depth>0)
22                if (!No_scan(Tag_hd(hd)))
23                     for (i=0; i<sz; i++)
24                       forward(from_start, from_limit, next, &Field(newv,i), depth−1);
25   }}}}

                                                        fp
                                                                                      frame




        Fig. 23. Does this graph have 5 vertices,
                                                                                                        2           2
                                                             stack of frames




        or 10? That is, should the boxes labeled
                                                                               root
        “root” or “outlier” be considered as graph                             root                          3
        vertices, or should they bey nonvertices
        whose contents are addresses of ver-                                                            1           1
                                                                                      frame




        tices? The dashed oval labeled “graph”
        hints at our design choice: root boxes                                                outlier       graph
        and outliers are not graph vertices.                                   root              root


           Line 19 places the        forwarding pointer.
           Line 21: If depth>0 this performs a local depth-first traversal (to improve locality of reference).
             The default setting depth=0 disables this feature, but a value of ∼10 would also be reasonable.

     5.2    Exterior and Interior Pointers
     The forward function’s implementation works regardless of how the mutator’s root pointers are
     organized, regardless of how many generations the collector has (or whether it’s generational at
22                                                         Shengyi Wang, Kathrin Stark, and Andrew W. Appel


all), and regardless of how “remembered sets” are organized for mutable references. Therefore we
seek a formal specification of forward (that is, a funspec) that’s independent of these issues as well.
   As we have discussed, the mutator manages a set of root pointers. When it calls the collector,
the mutator must indicate the locations where it stores those roots. We use a stack-of-frames
data structure (Figure 23), but the same considerations would apply regardless of the particular
data structure used. In the specification of the interface between mutator and collector, should
we consider that each “root” box in the stack of frames is a graph node (with out-degree 1), or
should we say that they are outside the graph, pointing in? Each of these design choices has its
disadvantages:
       • If root-boxes are graph vertices, then whenever the mutator copies a root-pointer, its
         correctness proof needs to create a new graph vertex; and when the root is no longer active,
         destroy the vertex. This is quite a bit of bookkeeping. In such a model, the “managed g.c.
         heap” contains a subset of the “graph,” and there are parts of the graph that the g.c. does
         not manage.
       • If root-boxes are not vertices, then our specification must distinguish between interior
         pointers (from one vertex to another) and exterior pointers (from outside the graph to graph
         vertices). In this model, the “managed g.c. heap” is corresponds 1-1 to the graph + allocable
         space. Our specification is based on this principle.
In order to ease the bookkeeping burden for those who prove the correctness of mutators (clients
of our g.c.), we have chosen the second way: root-boxes are not vertices, and we have two kinds of
pointers, interior and exterior.
   Sometimes the same C code must be understood in two different ways depending on whether a
pointer is interior or exterior. For example, in line 3 of Listing 22, the variable va receives the value
stored at the memory location pointed to by p. To prove correctness of this line of code, there must
be a spatial maps-to predicate in the precondition, giving access to the resource p. If p is an interior
pointer (i.e., a field of a record in the graph g), we can derive that resource from the graph_rep g
predicate. If p is exterior, we can derive it from the set of roots—ultimately, from the frames_rep
predicate that describes the stack-of-frames. But the formal specification of forward should not
need to know the details of how the stack-of-frames is organized, since it is passed the address of
one root (or one field of a graph record) at a time.
   Thus, in our specification of the forward function we describe the pointer p with two cases:
Definition forward_p_type :=
    (∗ exterior ∗) (Z + GC_Pointer + VType)
 + (∗ interior ∗) VType∗Z
The first case indicates the three possible content types of exterior pointers (unboxed integer, outlier
pointer, or graph-vertex) and the second case indicates an interior pointer as the 𝑖th field of graph-
vertex 𝑣. Then we need predicate forward_p_compatible (not shown) to indicate compatibility of 𝑝
with the graph, in either of those cases.
   The separation logic representation-predicate forward_p_rep reflects this distinction: it repre-
sents a one-word resource for exterior pointers, and is emp for interior ones, whose memory is
already covered by graph_rep.
Definition forward_p_rep (sh: share) (p: forward_p_type) addr g :=
 match p, addr with
 | FwdPntIntr _ , _ ⇒ emp
 | FwdPntExtr extr , Some v ⇒ data_at sh int_or_ptr_type (exterior2val g extr) v
 | _ , _ ⇒ emp (∗ this case cannot occur ∗)
Verification of a Generational Garbage Collector                                                                              23


  end.

5.3    Specification of the forward function
The forward function can be used in a wide variety of garbage collectors. In fact, the OCaml g.c. has
a very similar function that was almost unchanged6 in a radical overhaul of the collector between
OCaml 4 and OCaml 5 [Sivaramakrishnan et al. 2020]. Furthermore, though both OCaml 4 and
OCaml 5 have 2-generation collectors with the older generation using mark-and-sweep, almost the
same forward function can be used in a multi-generation collection in which all generations use
copying collection.
   To support this claim that forward is usable in many different kinds of garbage collectors, we
will show its specification and proof without (yet) describing the specification of other components
of the g.c.
   Listing 24 shows the VST separation logic function specification of the forward function. It takes
graph g compatible with heap h in the precondition, and produces g' compatible with h' in the
postcondition.
   Beyond the distinctions arising from exterior and interior pointers—which lead to case-based def-
initions of forward_p_type, forward_p_compatible, and forward_p_rep—there are a few additional
subtleties in the specification.
      • The from-space must be one space in the heap and the to-space must be a different one;
         that is we are forwarding from heapfrom to heapto , where from ≠ to.
      • The precondition forward_condition g h from to is defined as this conjunction:
         enough_space_to_copy g t_info from to
         ∧ graph_has_gen g from ∧ graph_has_gen g to
         ∧ copy_compatible g ∧ no_dangling_dst g
        and the postcondition assures this of the new graph g'. “Enough space to copy” means
        that the available part of the to-space is at least as large as the unmarked part of the from-
        space. “Graph has gen" means that the generation numbers from and to are legitimate in g.
        “Copy compatible” means that every ★ marked vertex in the graph (as in Figure 21) has a
        forwarding pointer           installed that points to a graph vertex in a different generation.
        “No dangling destination" means that every edge in the graph points to a legitimate vertex.
      • The parameter 𝑝 is the address of a location containing a pointer 𝑞 that’s possibly into the
        from-space. If 𝑞 doesn’t point into the from-space, then it should be left alone (as per the
        if-statement on line 6 of Listing 22), because the space containing 𝑞 is not currently being
        forwarded (or 𝑞 is an outlier).
      • The postcondition establishes that the new graph and heap (g',h') are calculated as forward_
        graph_and_heap applied to (g,h) and some other arguments. This is essentially the func-
        tional model of the C program, defined by case analysis on the four cases: unboxed, outlier,
        exterior (root) pointer, interior (edge) pointer. Our verification employs a common pattern
        in proving correctness of low-level imperative programs: prove that the C program refines a
        functional model of an algorithm (a function or inductive relation in Rocq), and then prove
6 Three changes: (1) In the OCaml5 collector, checking the mark on an object (as at lines 7-8 of Listing 22) must be a

compare-and-swap synchronized operation, to ensure that two threads do not both copy the object; and this must be
properly synchronized with reading the forwarding pointer (as at line 9). (2) OCaml5 has a new “continuation” tag, related
to stacks of other threads. (3) The depth-first “to-do list” of nodes remaining to forward is now in a per-thread state structure
rather than in a global variable. Our forward function does not have a to-do list in the style of OCaml 4 or OCaml 5.
24                                                       Shengyi Wang, Kathrin Stark, and Andrew W. Appel


                             Listing 24. Funspec of the forward function
DECLARE _forward
WITH rsh: share, sh: share, gv: globals, g: LGraph, h: heap, hp: val,
     outlier: outlier_t, from: nat, to: nat, depth: Z, forward_p: forward_p_type,
     fwd_addr: forward_addr_type
PRE [tptr int_or_ptr_type,         (∗ value ∗from_start ∗)
     tptr int_or_ptr_type,          (∗ value ∗from_limit ∗)
     tptr (tptr int_or_ptr_type), (∗ value ∗∗next ∗)
     tptr int_or_ptr_type,          (∗ value ∗p ∗)
     tint]                         (∗ int depth ∗)
  PROP (readable_share rsh; writable_share sh;
          graph_heap_compatible g h;
          outlier_compatible g outlier;
          forward_p_compatible forward_p outlier g from;
          forward_p_addr_match forward_p fwd_addr;
          forward_condition g h from to;
          0 <= depth <= Int.max_signed;
          from <> to)
  PARAMS (gen_start g from;                             (∗ from_start ∗)
            limit_address g h from;                        (∗ from_limit ∗)
            heap_next_address hp to;                        (∗ next ∗)
            forward_p_address forward_p fwd_addr g; (∗ p ∗)
            Vint (Int.repr depth))                       (∗ depth ∗)
  SEP (outlier_rep outlier;
         forward_p_rep sh forward_p fwd_addr g;
         graph_rep g;
         heap_rep sh h hp)
POST [tvoid]
  EX g': LGraph, EX h': heap,
  PROP ((g', h') = forward_graph_and_heap from to (Z.to_nat depth)
                             (forward_p2forward_t forward_p g) g h)
  RETURN ()
  SEP (outlier_rep outlier;
         forward_p_rep sh (upd_fwd from to g forward_p) fwd_addr g';
         graph_rep g';
         heap_rep sh h' hp).


       that the algorithm accomplishes the high-level goal (graph isomorphism). We defer the
       functional model proof to section 7.
   Correctness proof(s) of the forward function. In this paper we do not show Rocq proofs such as the
proof that forward satisfies the funspec in Listing 24. These proofs are available in the CertiGraph
github repo (see Appendix A), and the proof scripts can be quite long.
Verification of a Generational Garbage Collector                                                         25


                                         Listing 25. Forwarding the roots
void forward_roots (value ∗from_start,                /∗ beginning of from−space ∗/
                         value ∗from_limit,          /∗ end of from−space ∗/
                         value ∗∗next,              /∗ next available spot in to−space ∗/
                         struct stack_frame ∗frames) /∗ list of frames ∗/
  { struct stack_frame ∗frame = frames;
     value ∗start;
     size_t i, limit;
     while (frame != NULL) {
        start = frame→ root;
        limit = frame→ next − start;
        frame = frame→ prev;
        for (i=0; i<limit; i++)
           forward(from_start, from_limit, next, start+i, DEPTH);
     }
}


   The correctness proof of forward is doubly long. In effect, that funspec is really the disjunction
of two different specifications, because of the disjunction in the definition of forward_p_type. We
have two different proofs of the same C code, depending on whether the p parameter is interior
or exterior, and it would not be trivial to refactor those into a single proof. In subsection 5.2 we
mentioned the disadvantage of treating roots as nonvertices—and needing two proofs of the same
C function is a significant disadvantage indeed. But it is justified by the way it eases the proof of
every client of the g.c., as explained in subsection 5.2.
   The forward function is called from three sites:
     • From forward_roots (as in Figure 21B,C), where the argument p is always exterior;
     • From do_scan, (as in Figure 21D,E), where p is always interior;
     • From forward_remset, which handles the remembered set of mutable locations that have
        been stored into (as in Figure 8, which shows the mutation but not the remembered set). In
        this case (see subsection 6.1) the stored-into location may be either interior or exterior (i.e., an
        outlier). The line of forward_remset that calls forward needs two different separation-logic
        proofs to handle these two cases.
This concludes our discussion of the forward function; now let’s consider other parts of the collector.

5.4   Forwarding the roots
The first step in a typical copying g.c. is to forward the roots, as illustrated in Figure 21B–C. As
illustrated in Figure 4, the roots are contained in a linked list of records, where each record describes
the bounds of an array of root-pointers. The forward_roots function simply traverses this data
structure (Listing 25).
   The specification of forward_roots (not shown) is similar to that of forward, except that instead
of the conjunct forward_p_rep for a single root, the precondition contains frames_rep sh fr for the
entire stack of root-frames. The proposition forward_condition g h from to appears in the precon-
dition, and forward_condition g' h' from to is in the postcondition, meaning that forward_roots
preserves this important invariant.
     26                                                         Shengyi Wang, Kathrin Stark, and Andrew W. Appel


                                         Listing 26. Scanning the to-space
 1   void do_scan(value ∗from_start, /∗ beginning of from−space ∗/
 2                  value ∗from_limit, /∗ end of from−space ∗/
 3                  value ∗scan,      /∗ start of unforwarded part of to−space ∗/
 4                  value ∗∗next)    /∗ next available spot in to−space ∗/
 5   { while(scan < ∗next) {
 6       header_t hd = ∗((header_t∗)scan);
 7       mlsize_t sz = Wosize_hd(hd);
 8       int tag = Tag_hd(hd);
 9       if (!No_scan(tag)) {
10          int j;
11          for(j = 1; j <= sz; j++)
12            forward (from_start, from_limit, next, &Field(scan, j), DEPTH);
13       }
14       scan += 1+sz;
15     }
16   }


     5.5   Scanning the to-space
       In a typical copying g.c., after the roots are forwarded, the next step is to scan the to-space (as
     shown in Figure 21D–G). The region between start and scan contains pointers that have already
     been forwarded (none of them point into from-space), and between scan and next they have been
     copied verbatim, so may point into from-space. The goal of scanning is to make sure all those
     pointers are forwarded into to-space (or left alone, if they already pointed to other spaces). Listing 26
     implements this simple algorithm.
       No-scan objects. The OCaml data format has an 8-bit tag field in each object’s descriptor, and
     tag values ≥ 251 indicate that the fields of the object do not contain pointers regardless of their
     low-order bits. This is useful for representing string values. The test (at line 9) for No_scan(tag)
     skips the forwarding of the fields of those objects.
        Bug, found by verification. The if-statement at line 9 of Listing 26 is to avoid scanning the
     fields of string objects. It would be incorrect to scan those fields, because even numbers would be
     misinterpreted as pointers.
        Listing 22, line 22 contains a similar if-statement for the same reason. However, in the original C
     code, line 22 was missing—which was a bug—and the program was proved correct! [Wang et al.
     2019] Furthermore, the bug was never detected in testing. How is that possible?
        The original correctness proof of the collector [Wang et al. 2019] was done to a specification that
     was inadvertently too weak: it permitted string objects only if every eighth byte was odd. That is,
     every field of a no-scan object had to be tagged as an unboxed value, which is not the intent of the
     no-scan tag (and would render no-scan objects useless in practice). The reason the bug was never
     detected is that no test case simultaneously exercised depth>0 and no-scan objects.
        It was not until we tried to verify a client program that used packed bytestrings [Korkut et al.
     2025] that the weakness of the specification was detected: our client program could not be proved
     correct, because it used bytestrings that might contain even numbers at any position. When we
Verification of a Generational Garbage Collector                                                      27


strengthened the g.c. specification, we found that the forward function could not be verified until
we fixed the bug.
   Garbage collectors are notorious for “heisenbugs," that is, bugs that are very difficult to diagnose.
This would have been one of those heisenbugs, except that we never had to diagnose it by running
a program. Program verification did exactly the job that it should have. But it could only do so
because we verified the adequacy of the specification by proving a client program correct.
  Funspec of do_scan. We will not show the function spec of do_scan, which is mostly straightfor-
ward, except to remark:
    • The parameter scan must point to an address in the to-space that holds a well-formatted
       record. That is, there must be some vertex 𝑣 of the graph whose label is the pair (to, 𝑖)
       where scan = start(to) + 𝑖 · WORD_SIZE.
    • The vertex 𝑣 must not be ★ marked.
    • A standard theorem about Cheney’s algorithm is that scan will catch up with next before we
       run out of space. Informally, that’s because the original graph did fit in the from-space, and
       the available part of the to-space is at least as big as the from-space. We express this formally
       with a predicate forward_condition; the proposition forward_condition g h from to appears
       in the precondition of do_scan, and forward_condition g' h' from to is in the postcondition,
       and it appears in every loop invariant of the proof, meaning that do_scan preserves this
       important invariant.
    • The postcondition of do_scan contains the proposition, do_scan_relation from to 𝑣 g g'.
       Thus the VST proof establishes that the C code of do_scan implements the functional model
       defined as a relation in Rocq (Listing 27). The proof in section 7 uses this relation as part of
       the one-generation correctness argument, together with remembered-set forwarding, root
       forwarding, and reset.

6   Generational garbage collection
The programs and proofs in section 5 are modular, in the sense that they can be repurposed
without change in a variety of different g.c. organizations. In this section we describe our specific
multi-generation collector.
   Assume, for the moment, that there are no assignments into mutable references or arrays, that
objects are immutable.
   We have up to 𝑁ℎ spaces, called generations, numbered from generation 0, the nursery. Objects
are created and initialized in the nursery; it is trivial that all the fields of nursery objects point to
objects in generations at least as old as the object itself. That is: Objects in generation 𝑔𝑖 point only
into generations 𝑔 𝑗 for 𝑗 ≥ 𝑖).
   A garbage collection entails: use Cheney’s algorithm to copy all the objects from 𝑔0 into the
available space at the end of 𝑔1 (at which point 𝑔0 is empty); and then either stop, or copy all the
objects from 𝑔1 into the available space of 𝑔2 , and so on. Clearly this will preserve the invariant
that an object in generation 𝑔𝑖 will point only to objects in generations 𝑔 𝑗 such that 𝑗 ≥ 𝑖.
   This is more efficient than Cheney’s original two-space scheme because:
     • Generation 𝑖 is smaller than generation 𝑖 + 1, so there are fewer objects to examine than if
        the entire live graph is copied, and usually the collector will stop after the 𝑖 = 0 iteration;
     • The infant mortality hypothesis (more commonly known as the weak generational hypothesis)
        is that young objects are likely to die sooner than objects that have stayed reachable for a
        long time already [Lieberman and Hewitt 1983], so it’s worth concentrating the effort on
        the youngest objects;
28                                                          Shengyi Wang, Kathrin Stark, and Andrew W. Appel


Listing 27. Functional model of do_scan. Compare with the C code in Listing 26 and note that it’s a close
transcription into Rocq of what the C program does.
Inductive scan_vertex_for_loop (from to: nat) (v: VType):
   list nat → LGraph → LGraph → Prop :=
| svfl_nil: ∀ g, scan_vertex_for_loop from to v nil g g
| svfl_cons: ∀ g1 g2 g3 i il,
      forward_relation
         from to O (interior2forward (InteriorVertexPos v (Z.of_nat i)) g1) g1 g2 →
      scan_vertex_for_loop from to v il g2 g3 →
      scan_vertex_for_loop from to v (i :: il) g1 g3.

Definition no_scan (g: LGraph) (v: VType): Prop :=
                NO_SCAN_TAG <= (vlabel g v).(raw_tag).

Inductive scan_vertex_while_loop (from to: nat):
   list nat → LGraph → LGraph → Prop :=
| svwl_nil: ∀ g, scan_vertex_while_loop from to nil g g
| svwl_no_scan: ∀ g1 g2 i il,
      gen_has_index g1 to i → no_scan g1 (to, i) →
      scan_vertex_while_loop from to il g1 g2 →
      scan_vertex_while_loop from to (i :: il) g1 g2
| svwl_scan: ∀ g1 g2 g3 i il,
      gen_has_index g1 to i → ∼no_scan g1 (to, i) →
      scan_vertex_for_loop
         from to (to, i)
         (nat_inc_list (length (vlabel g1 (to, i)).(raw_fields))) g1 g2 →
      scan_vertex_while_loop from to il g2 g3 →
      scan_vertex_while_loop from to (i :: il) g1 g3.

Definition do_scan_relation (from to to_index: nat) (g1 g2: LGraph) : Prop :=
 ∃ n, scan_vertex_while_loop from to (seq to_index n) g1 g2 ∧
            ∼gen_has_index g2 to (to_index + n).


      • The nursery can fit into the CPU cache, since it is all a contiguous region of about that size,
         so its allocation and nursery-collection are efficient [Gonçalves and Appel 1995].
To perform Cheney’s algorithm on just a portion of memory, i.e., generation 𝑔𝑖 , we must be able to
find all the roots of 𝑔𝑖 . Because younger objects point only to older objects, there will be no roots
in generations > 𝑖; and all generations < 𝑖 are empty when we are collecting 𝑔𝑖 ; so the only roots
of 𝑔𝑖 are the local and global variables of the program—that is, the stack of frames.
   Now let us remove the assumption that objects are immutable. If field 𝑓𝑘 of an object in generation
𝑔𝑖 is stored into, this may create a back pointer, a pointer from an older generation into a younger
generation. Upon assigning to 𝑓𝑘 , we keep the address of 𝑓𝑘 in a remembered set associated with 𝑔0 .
When collecting any generation < 𝑖, we must treat 𝑓𝑘 as one of the roots of the Cheney copying
collection. When collecting 𝑔 𝑗 into 𝑔 𝑗+1 , if the remembered-set item points within 𝑔 𝑗 we promote
Verification of a Generational Garbage Collector                                                                       29


                                           Listing 28. Funspec of do_scan
DECLARE _do_scan
WITH rsh: share, sh: share, gv: globals, g: LGraph, h: heap, hp: val,
     outlier: outlier_t, from: nat, to: nat, to_index: nat
PRE [tptr int_or_ptr_type,
     tptr int_or_ptr_type,
     tptr int_or_ptr_type,
     tptr (tptr int_or_ptr_type)]
  PROP (readable_share rsh; writable_share sh;
          graph_heap_compatible g h;
          outlier_compatible g outlier;
          forward_condition g h from to;
          from <> to; closure_has_index g to to_index;
          0 < available_size h to; gen_unmarked g to)
  PARAMS (gen_start g from;
            limit_address g h from;
            (vertex_address g (to, to_index)) + (− WORD_SIZE)
            heap_next_address hp to)
  SEP (all_string_constants rsh gv;
         outlier_rep outlier;
         graph_rep g;
         heap_rep sh h hp)
POST [tvoid]
  EX g': LGraph, EX h': heap,
  PROP (graph_heap_compatible g' h';
          outlier_compatible g' outlier;
          forward_condition g' h' from to;
          do_scan_relation from to to_index g g';
          heap_relation h h')
  RETURN ()
  SEP (all_string_constants rsh gv;
         outlier_rep outlier;
         graph_rep g';
         heap_rep sh h' hp).


it into the remembered set of 𝑔 𝑗+1 . If 𝑓𝑘 pointed into 𝑔 𝑗 ′ for 𝑗 ′ > 𝑗, then the copy of 𝑓𝑘 that’s now
in 𝑔 𝑗+1 is no longer a back-pointer, it is a “normal" pointer to an object in the same generation or
older, so it no longer needs a remembered-set item.7
    Let spaces[ ] be an array of struct space records (Listing 19). We will keep the remembered set
of 𝑔𝑖 in the region between spaces[𝑖].limit and spaces[𝑖].rem_limit; each word in that region will
be the address of a field that has been stored into. Thus, the operation mutable_update can be
7 The criteria for promoting a remembered-set item are simple but nontrivial enough that we had a bug in the program until

verification revealed it.
30                                                                      Shengyi Wang, Kathrin Stark, and Andrew W. Appel



Fig. 29. Each generation must have enough free space (between alloc and limit) for all the allocated+allocable
objects in all younger generations. To maintain that invariant, if it is violated for 𝑔𝑘 , one can move (i.e.,
forward) all objects from 𝑔0 to 𝑔1 , then forward 𝑔1 to 𝑔2 , etc., up to 𝑔𝑘 into 𝑔𝑘+1 . The likelihood of reaching
large 𝑘 is exponentially small, since each generation is twice the size of the preceding, and most objects do
not survive this copying because they are not reachable. If 𝑔𝑘+1 doesn’t exist, it is created from the system
malloc. If that fails, the program must abort.

      The remembered set of gen-                                                     start
      eration 𝑔𝑖 contains point-                                                               s
      ers to fields of objects that                                                            t
      might contain pointers from                                                                        alloc
      older generations into 𝑔𝑖 .
      For example, the 𝑔0 remem-                                start                alloc
                                                                             u
      bered set contains two en-                                             v
      tries: the address of the 𝑦
      field and of the 𝑤 field. It is      start                            w
                                                      x
      unnecessary but harmless to                               alloc
      have 𝑦 in the 𝑔0 remembered                     y
                                           alloc
      set. The purpose of 𝑤 in the
      remembered set is that dur-          limit
      ing a collection of just gener-
                                                                limit                                    limit
      ation 𝑔0 , this will serve as a
                                           end                                       limit
                                                     go          end
                                                                            g1        end                end
                                                                                               g2                  g3
      root of Cheney’s algorithm.



                                    Listing 30. Storing into a mutable reference
void mutable_update(struct thread_info ∗ti, value ∗p, value q) {
  ∗p = q;
  if (is_ptr(q))
     ∗(value ∗∗)(−−ti→ limit) = p;
}


implemented as shown in Listing 30. This works because ti→ limit is the boundary between the
nursery’s available region and its remembered set. If 𝑞 is an unboxed value (nonpointer) then it
cannot cause a back-pointer and does not need to be added to the remembered set.
   The stored-into address p may be the field of a graph object, or it may be an outlier. The same C
function mutable_update works in either case, but we need two different specifications of it; this is
a consequence of the design decision discussed in subsection 5.2, that outliers are not graph nodes.
Storing into an outlier is one way that the mutator can register a root-pointer that is not a local
variable in the stack of frames.8

6.1     Forwarding the remembered set
With a generational garbage collector, the assignment a→field=q could create a back pointer, that
is, a pointer from an older object a to a younger object q. If q is in a younger generation than a,
8 However, if roots are registered in that way, there’s no effective way to unregister a root. One can store an unboxed

integer into it, so that no graph nodes are retained, but the address itself cannot be freed because there will always be a
remembered-set item pointing to it. An alternate way for the mutator to register global roots, such that the global address
itself can be freed when no longer needed, is to make special frames at the bottom of the stack of frames. When a global
root is no longer needed, its special frame can be removed or cleared. See https://github.com/jpaykin/certicoq-set-library
     Verification of a Generational Garbage Collector                                                   31


                      Listing 31. Forwarding the remembered set from one generation to the next
 1   void forward_remset (struct space ∗from, /∗ descriptor of from−space ∗/
 2                            struct space ∗to, /∗ descriptor of to−space ∗/
 3                            value ∗∗next) /∗ next available spot in to−space ∗/
 4   { value ∗from_start = from→ start, ∗from_limit=from→ limit,
 5              ∗from_rem_limit=from→ rem_limit, ∗q;
 6      for (q=from_limit; q != from_rem_limit; q++) {
 7        value ∗p = (value∗)int_or_ptr_to_ptr(∗q);
 8        if (!Is_from(from_start, from_limit, p)) {
 9           forward(from_start, from_limit, next, p, DEPTH);
10           ∗(−−to→ limit) = (value)p;
11        }
12      }
13   }


     then when collecting (only) q’s generation it will be necessary to use a→field as a root. The way
     generational collectors handle this is to put address &a→field into a remembered set. There are
     many ways of representing the remembered set as a data structure; Reppy’s collector (and ours)
     uses the space in each generation between limit and rem_limit.
        Listing 31 shows how to use a remembered set as roots for forwarding, as well as the criteria for
     promoting remembered-set items to the next generation’s remembered set. Let p be the address of
     &a→ field; in general, p may be a mutable reference, a mutable field of a record, an array element,
     or an outlier address. To store q into address p, the mutator calls mutable_update(ti,p,q), passing
     also the thread-info pointer ti. This is illustrated in Figure 8, which shows that limit is decreased,
     stealing one word from the allocation arena to be used in the heap-management data structure.
     The implementation of mutable_update (Listing 30) shows what has happened: we consider the
     space (in every generation) between limit and rem_limit to be part of the heap-management data
     structure, and mutable_update simply stores the address p into the generation-0 part of that data
     structure (increasing its size by decrementing limit). However, if q is an unboxed integer, there is
     no need to remember it because this store cannot possibly create a back-pointer.
        Later, when the garbage collector forwards generation 𝑖 into generation 𝑖 + 1, generation 𝑖’s
     remembered set must be processed, by the function forward_remset (Listing 31). The loop body
     in that function is rather simple (just four short lines), but reasoning about its correctness is
     remarkably complex.
        Informal explanation of forward_remset. We can assume that from is generation 𝑖, to is generation
     𝑖 + 1, and all the generations 0 to 𝑖 − 1 are empty (because they would have to be collected before
     the generational collector would consider forwarding generation 𝑖). In Listing 31, lines 4–5 load the
     description of from-space boundaries into local variables for convenient access. The for-loop at line
     6 processes each element of the remembered set. We know all of those elements are pointers, not
     unboxed integers, since they were the destination arguments of calls to mutable_update. Therefore
     line 7 can use int_or_ptr_to_ptr to cast the value to type value∗ (see Listing 34). The pointer, a
     member of the remembered set, p is the address of some field that has been stored into.
           • If that field is in the current from-space (generation 𝑖), where could that field point to?
             It must point to generation ≥ 𝑖, since all the younger generations are empty at present.
             Therefore it cannot be a back-pointer, and we can ignore it.
32                                                        Shengyi Wang, Kathrin Stark, and Andrew W. Appel


     • If that field is not in the current from-space, then it must be in a generation > 𝑖 or be an
       outlier. Either way, it’s possible that it points into generation 𝑖, in which case it would be a
       back-pointer. We forward the pointer, which has no effect unless the field does indeed point
       into generation 𝑖 (and is harmless otherwise). On the other hand, perhaps that field points
       into generation 𝑖 + 𝑘; in that case, this call to forward does nothing, but we must preserve p
       for later consideration when collecting generations > 𝑖. Line 10 does that by copying p into
       the remembered set of generation 𝑖 + 1.
  Verification Complexity. The simplicity of lines 4–7 in forward_remset belie the complexity of
verifying them. Some of the issues that complicate the reasoning are:
     • The test Is_from(from_start,from_limit,p) is exactly the comparison from_start≤p<from_limit.
        Our axiom for range comparisons (see Appendix C) requires us to prove that from_start
        and from_limit are allocated and in the same block, and that p is allocated. VST supports
        the ability to do such proofs, but it still requires several lines of Rocq proof script.
     • Pointer arithmetic in the loop test condition (in the semantics of CompCert and Verifiable
        C) involves arithmetic modulo 2word_size , for which we do not have good proof automation.
     • Our g.c. proof maintains many invariants about the state of the graph and heap, and about
        the start, limit, and rem_limit of each generation. Reestablishing these invariants takes
        several lines of proof script.
     • Recall from subsection 5.2 that the specification of the forward function is split into two
        cases, one for forwarding an interior pointer and one for an exterior pointer, and calls to
        forward for these cases have nontrivially different proof obligations—different treatments
        of memory layout and separation-logic framing. The call to forward from forward_remset
        could be in either case; that is, p could be an outlier (exterior) or in a generation (interior).
        Essentially, we need two proofs of the same loop body, one for each such case.
  Consequently, we find that the four-line loop body requires 452 lines of Rocq/VST proof script.

6.2 Proof of generational garbage collection
   Bug fixed in verification. Our original implementation of forward_remset had a bug at line 13:
there was q instead of p. This was not found in testing, because we had not yet had test cases with
enough generations and with the right pattern of mutable-ref updates. Instead, we found it (and
fixed it) while proving the correctness of the algorithm.
   The do_generation function. With all of that established, we can present the do_generation
function for copying the live objects from 𝑔𝑖 to 𝑔𝑖+1 , using both the remembered set and the
stack-of-frames as roots (Listing 32).
   The garbage_collect function. Listing 33 embodies our policy for managing the generations. To
match the size of the a typical CPU cache, we set nursery_size=216 words or 216·𝑊 bytes, where
𝑊 = 8 is the word size in bytes. We let generation 𝑔𝑖+1 be twice the size of generation 𝑔𝑖 . Since all
the generations must fit in an address space of 2𝑊 ∗8 bytes, one can calculate the maximum number
of generations that could ever be usable:
                    MAX_SPACES = (8𝑊 − (2 + log2 (𝑊 · NURSERY_SIZE)))
which is 43 when 𝑊 = 8.
  For every 𝑖, we want to guarantee the enough space to copy property between 𝑔𝑖 and 𝑔𝑖+1 . That
means there must be enough available space in 𝑔𝑖+1 for the entire size of 𝑔𝑖 . If that not the case
immediately after a copying collection into the available space of 𝑔𝑖 , we perform Cheney’s algorithm
Verification of a Generational Garbage Collector                                                      33


                    Listing 32. Copying one generation into the available space of another
void do_generation (struct space ∗from, /∗ descriptor of from−space ∗/
                       struct space ∗to, /∗ descriptor of to−space ∗/
                       struct stack_frame ∗fr) /∗ where are the roots? ∗/
{ value ∗p = to→ next;
   forward_remset(from, to, &to→ next);
   forward_roots(from→ start, from→ limit, &to→ next, fr);
   do_scan(from→ start, from→ limit, p, &to→ next);
   from→ next=from→ start;
   from→ limit=from→ rem_limit;
}


to copy all the records out of 𝑔𝑖 into 𝑔𝑖+1 . If that (momentarily) violates enough space to copy between
𝑔𝑖+1 and 𝑔𝑖+2 , then we copy all records out of 𝑔𝑖+1 , and so on.
   If, in the process, we come to a generation 𝑔𝑘 that has not yet been created (where 𝑘 <
MAX_SPACES), then the g.c. creates that generation by calling malloc. If malloc returns 0 (failing
to find enough virtual memory), the entire program (collector and mutator) must abort.
   We will never reach line 30 (𝑘 ≥ MAX_SPACES), because malloc cannot ever find more virtual
memory than the size of the 64-bit (or 8𝑊 -bit) address space, so instead it will abort at line 13.
That’s obvious, but we have not actually proved it.
   If the mutator wants to create a very large object, an array or string larger than the size of the
nursery, it will set ti→ nalloc to that large size and call garbage_collect, which will abort at line 24.
A more sophisticated implementation would avoid aborting by collecting all generations whose size
is less than nalloc, and then allocating the large object directly into one of the older generations.
  Correctness of garbage_collect. The VST specifications and proofs of the mutable_update, do_generation,
and garbage_collect are expressed in similar manner to that of the funspecs shown earlier in this
section 5. Like those proofs, we prove that the C programs implement functional models of al-
gorithms expressed as functions and inductive relations in Rocq. Then we prove the algorithms
correct.

7   Correctness of the functional model
In Sections 5 and 6, the VST proofs establish that the C code implements functional models written
in Rocq: for example, forward implements forward_graph_and_heap, and do_scan implements
do_scan_relation. This section shows how the functional models of all the C functions are proved
to satisfy top-level specification: that they preserve the graph structure visible to the mutator, up
to isomorphism.
   To establish this result, we first state the graph-isomorphism property used as the mutator-facing
conclusion. We then prove it for one-generation copying and present the remembered-set invariant
needed for mutable update. Finally, we lift the one-generation result to the full garbage_collect
loop.
   In the theorem below, roots1 and roots2 are the ordinary, mutator-visible root lists extracted
from the stack of frames described in section 2. The additional roots used internally during a
one-generation collection are introduced in subsection 7.2.
     34                                                       Shengyi Wang, Kathrin Stark, and Andrew W. Appel


                                    Listing 33. The garbage_collect function
 1   void garbage_collect(struct thread_info ∗ti) {
 2     struct heap ∗h = ti→ heap;
 3     int i;
 4     h→ spaces[0].limit = ti→ limit;
 5     h→ spaces[0].next = ti→ alloc;
 6     for (i=0; i<MAX_SPACES−1; i++) {
 7          struct space ∗r = h→ spaces+i;
 8          struct space ∗s = h→ spaces+(i+1);
 9          if (s.start==NULL) {
10             int n = 2 ∗ r→ rem_limit−r→ start;
11             value ∗p = (value ∗)malloc(n ∗ sizeof(value));
12             if (p==NULL) abort_with ("Could␣not␣create␣the␣next␣generation\n");
13             s→ start=p;
14             s→ next=p;
15             s→ limit = p+n;
16             s→ rem_limit = s→ limit;
17          }
18          do_generation(h→ spaces+i, h→ spaces+(i+1), ti→ fp);
19          if (r→ rem_limit − r→ start <= s→ limit − s→ next) {
20              value ∗lo = h→ spaces[0].start;
21              value ∗hi = h→ spaces[0].limit;
22              if (hi−lo < ti→ nalloc)
23                 abort_with ("Nursery␣is␣too␣small␣for␣function's␣num_allocs\n");
24              ti→ alloc = lo;
25              ti→ limit = hi;
26              return;
27          }
28       }
29     abort_with("Ran␣out␣of␣generations\n");
30   }


     7.1   Graph isomorphism for the root-reachable subgraph
     The predicate gc_graph_iso formalizes the graph-isomorphism property stated informally in sec-
     tion 3. Root boxes themselves are not vertices of the graph, as discussed in subsection 5.2. Therefore
     the definition first extracts from each root list the roots that actually point to graph vertices,
     restricts each graph to the subgraph reachable from those vertices, and then requires an explicit
     label-preserving graph isomorphism between the two reachable subgraphs.
     Definition gc_graph_iso (g1: LGraph) (roots1: roots_t)
                                 (g2: LGraph) (roots2: roots_t): Prop :=
      let vertices1 := filter_proj exterior_proj_vertex roots1 in
      let vertices2 := filter_proj exterior_proj_vertex roots2 in
      let sub_g1 := reachable_sub_labeledgraph g1 vertices1 in
Verification of a Generational Garbage Collector                                                  35


  let sub_g2 := reachable_sub_labeledgraph g2 vertices2 in
  ∃ vmap12 vmap21 emap12 emap21,
    roots2 = map (exterior_map vmap12) roots1 ∧
    label_preserving_graph_isomorphism_explicit
          sub_g1 sub_g2 vmap12 vmap21 emap12 emap21.
  The map on roots accounts for copying. A root that points to a graph vertex before collection may
point to a different vertex afterwards, namely the copy in another generation. The exterior_map
function maps graph-vertex roots through vmap12 and leaves unboxed integers and outlier pointers
unchanged.
  The main graph-isomorphism theorem has the following form:
Theorem garbage_collect_isomorphism:
 ∀ roots1 roots2 g1 h1 rh1 rmst1 g2 h2 rh2 rmst2,
    graph_unmarked g1 →
    no_unrecorded_backward_edge g1 rh1 →
    no_dangling_dst g1 →
    roots_graph_compatible roots1 g1 →
    sound_gc_graph g1 →
    remset_graph_state g1 O rmst1 rh1 →
    remset_heap_covers_graph g1 rh1 →
    garbage_collect_relation roots1 roots2 g1 h1 rh1 rmst1 g2 h2 rh2 rmst2 →
    gc_graph_iso g1 roots1 g2 roots2.
   Here g1 and g2 are the pre- and post-collection graphs, and h1 and h2 are the corresponding
abstract heaps. The variables rh1 and rh2 are the remembered-set heaps, while rmst1 and rmst2 are
the remembered-set states used to relate those heaps to the graph. These components are needed
to state the collector’s internal invariants, but they do not occur in the conclusion. The conclusion
mentions only the two graphs and the two root lists.
   The theorem also assumes standard graph well-formedness conditions. In particular, sound_gc_
graph says that the graph’s validity predicates agree with its represented vertex and edge sets,
and that each edge’s source and label agree with the two components of its representation. More
explicitly, graph_unmarked requires all graph vertices to be unmarked, no_dangling_dst requires
every represented edge to have a valid destination, and roots_graph_compatible requires every
vertex-valued root to denote a valid graph vertex. The hypotheses no_unrecorded_backward_edge,
remset_graph_state, and remset_heap_covers_graph express the remembered-set discipline dis-
cussed in subsection 7.3. Separate preservation lemmas show that the graph operations used by the
collector maintain these properties.
   The hypotheses of garbage_collect_isomorphism are deliberately stated as separate graph-level
facts rather than through the bundled VST predicates used at the function boundary. In the full
current funspec, bridge lemmas derive these facts from full_gc and remembered_set_ok, together
with facts supplied by the spatial representation predicates. The full VST precondition is stronger:
it also contains heap-layout and copying-safety conditions needed to verify the C implementation
but not used directly by the graph-isomorphism argument.
   For readability, the funspec displayed in Listing 11 is abridged: it suppresses the remembered-set
component of the precondition and the heap and remembered-set arguments of garbage_collect_
relation. The full relation used by the correctness theorem threads the abstract heap, remembered-
set heap, and remembered-set state through the collection. These additional arguments are needed
36                                                       Shengyi Wang, Kathrin Stark, and Andrew W. Appel


for the collector’s internal invariants; the resulting gc_graph_iso conclusion remains the graph-
isomorphism property described in section 3.

7.2   Copying one generation
The proof is first developed for one generation. The C function do_generation, shown in Listing 32,
copies live objects from generation 𝑔𝑖 into the available space of generation 𝑔𝑖+1 . The functional-
model relation follows the same sequence as the C program:
                       forward_remset; forward_roots; do_scan; reset.
   The pointer p saved at the beginning of Listing 32 marks the start of the part of the to-space
that must later be scanned. The calls to forward_remset and forward_roots may copy objects into
that to-space and advance to→ next. Then do_scan performs the Cheney closure by scanning the
objects copied between p and the final value of to→ next. Finally, the from-generation is reset by
restoring from→ next and from→ limit, making the generation available for future allocation.
   We call the local and global variables represented by the stack of frames described in section 2
the ordinary roots. In the immutable case, one could explain the one-generation proof using only
these roots. With mutable update, that is not enough. As section 6 explains, a stored-into field in an
older object may point into the generation currently being collected. That older object is not itself
in the from-space, and therefore it will not be scanned during this collection. The remembered set
records the address of such a field, and forward_remset uses that address as an additional root-like
source for this collection step.
   The proof makes this distinction explicit by considering an augmented root list. At the C
level, forward_remset processes remembered-set locations. At the graph level, the corresponding
additional roots are the target vertices currently stored at those locations. The augmented list is
obtained by prefixing the ordinary-root list with the targets of the entries that forward_remset
processes for generation 𝑔𝑖 : entries whose source locations are outside the current from-space
and whose current targets lie in 𝑔𝑖 . Thus these remembered-set targets form the prefix, while the
ordinary stack-of-frames roots form the suffix.
   The one-generation argument first establishes the graph-isomorphism property for this aug-
mented root list. This corresponds to the algorithmic role of forward_remset: before the collector
forwards the ordinary roots and scans the to-space, it accounts for the additional root-like sources
represented by the remembered set.
   The main technical step relates reachability from the augmented roots in the original graph to
the reachable-or-marked vertices after remembered-set forwarding. After the ordinary roots have
been forwarded and the to-space has been scanned, every vertex in generation 𝑔𝑖 reachable from
the augmented roots has been forwarded and is marked, and no edge in the scanned graph points
into 𝑔𝑖 . These two facts justify resetting the collected generation and yield the graph-isomorphism
property for the augmented root list.
   The graph-isomorphism result for the augmented root list is only an intermediate statement.
The one-generation result used by the outer garbage_collect loop is stated for the ordinary stack-
of-frames roots. To obtain it, the proof restricts the augmented-root isomorphism back to the
ordinary roots. This uses a general property of gc_graph_iso: an isomorphism between root lists
with corresponding equal-length prefixes can be restricted to the suffixes consisting of the ordinary
roots. After rewriting the post-collection root list so that the mapped remembered-set roots form
the corresponding prefix, these additional roots no longer appear in the gc_graph_iso conclusion
used by the top-level collection theorem.
   This restriction does not undo forwarding or discard any object reachable from the ordinary
roots. It changes only the root set from which the two graphs are observed. A target vertex that is
Verification of a Generational Garbage Collector                                                    37


reachable from an ordinary root remains in the ordinary root-reachable subgraph, even if it is also
reached through a remembered-set location. Other target vertices may be reached only through
the additional remembered-set roots; they lie outside the restricted subgraph and therefore do not
affect this particular gc_graph_iso conclusion.
   Thus, once the reachability bridge and the loop invariants have been established—including graph
soundness, root compatibility, the remembered-set invariants, and the fact that all generations
younger than 𝑔𝑖 are already empty—the functional-model relation for copying generation 𝑔𝑖 into
𝑔𝑖+1 preserves gc_graph_iso for the ordinary roots. The remembered set is used internally to make
the copying step complete, but it does not appear in the resulting root-reachable graph-isomorphism
conclusion.

7.3   Remembered sets and recorded back pointers
The main proof invariant added for mutable update is a precise version of the remembered-set
discipline described in section 6. A back pointer into generation 𝑔𝑖 need not already be recorded
in the remembered set of 𝑔𝑖 . The write barrier first records the source field in the remembered
set of generation 𝑔0 , and the collector moves such remembered-set entries into 𝑔1 , then 𝑔2 , etc.,
as it proceeds through the generations. Thus the invariant must describe not just where an entry
ultimately matters, but where it may be in the collector’s current remembered-set pipeline.
   In the graph model, pointer-bearing object fields are represented as graph edges. An edge
𝑒 = (𝑣, 𝑗) identifies the 𝑗-th field of source vertex 𝑣; its destination is the vertex currently stored
in that field. Thus, remset_heap_records_edge rh k e means that the location of this source field
occurs in the 𝑘-th component of rh. The remembered set records the source location, not the
destination vertex:
Definition remset_heap_records_edge (rh: remset_heap) (k: nat) (e: EType): Prop :=
 In (RemSetInterior (InteriorVertexPos (fst e) (Z.of_nat (snd e)))) (nth_remset_space rh k).
   The indexed recorded-back-pointer invariant is:
Definition no_unrecorded_backward_edge_from (from: nat) (g: LGraph) (rh: remset_heap): Prop :=
 ∀ e, graph_has_e g e →
      egeneration e > vgeneration (dst g e) →
      ∃ k, from ≤ k ≤ vgeneration (dst g e) ∧ remset_heap_records_edge rh k e.

Definition no_unrecorded_backward_edge (g: LGraph) (rh: remset_heap): Prop :=
 no_unrecorded_backward_edge_from O g rh.
   The comparison egeneration e > vgeneration (dst g e) selects a pointer from an older gener-
ation to a younger one. If the destination of the edge is in generation 𝑔𝑖 , then no_unrecorded_
backward_edge_from from g rh says that the source field of that edge is recorded in some remember-
ed-set component 𝑔𝑘 , where from ≤ 𝑘 ≤ 𝑖. At the public entry point of garbage_collect, the col-
lection starts from 𝑔0 , so the unindexed name no_unrecorded_backward_edge is the special case
with from = 0.
   This predicate concerns graph-internal edges, whose source locations are represented by RemSet-
Interior. Remembered-set locations in outlier objects are not graph edges; they are covered sepa-
rately by the remembered-set compatibility conditions used at the VST interface.
   This condition replaces the simpler invariant available in the immutable setting. Without mu-
table update, once an object is created in the nursery, its fields point only to objects in the same
or older generations, and older objects cannot later acquire pointers to younger objects. With
mutable_update, that statement is false. The right invariant is not that back pointers do not exist,
38                                                         Shengyi Wang, Kathrin Stark, and Andrew W. Appel


nor that their source fields are already recorded in the destination generation’s remembered set. In-
stead, every graph-internal old-to-young edge must be recorded somewhere in the remembered-set
pipeline between the generation currently being collected and the edge’s destination generation.
   The recorded-back-pointer condition is kept separate from ordinary graph/heap compatibility.
Ordinary compatibility predicates say that the graph is represented in the heap, that roots and
outliers are compatible with the graph, and that edges do not dangle. The remembered-set condition
talks about the heap-management data structure, which is opaque to the mutator. Keeping these
conditions separate makes the specification boundary clearer: remembered sets are essential to
the collector’s internal correctness argument, but they are not part of the graph structure that the
mutator sees.
   The augmented-root isomorphism described above is already stated for the graph after generation
𝑔𝑖 has been reset. A separate obligation, needed by the next iteration of the collector loop, concerns
resetting the corresponding component of the remembered-set heap. This reset must advance
the indexed recorded-back-pointer invariant: before collecting 𝑔𝑖 , pending entries may live in
remembered-set components 𝑔𝑘 with 𝑖 ≤ 𝑘 ≤ 𝑑, where 𝑔𝑑 is the destination generation of the edge;
after 𝑔𝑖 has been collected and its remembered-set component reset, the next loop iteration starts
at 𝑔𝑖+1 , so pending entries must live in components 𝑔𝑘 with 𝑖 + 1 ≤ 𝑘 ≤ 𝑑.
   Intuitively, every target vertex in 𝑔𝑖 reached from a relevant remembered-set location has already
been forwarded before the graph is reset. Any remaining old-to-young edge into a later generation
either already had a witness in a remembered-set component above 𝑔𝑖 , or had a witness in 𝑔𝑖 ’s
remembered set and is promoted to the remembered set of 𝑔𝑖+1 . Edges whose destinations would
be in generations below 𝑔𝑖+1 are ruled out by the invariant that those generations have already
been cleared, together with the no-dangling-destination property. Formally, under the graph and
remembered-set invariants maintained by the collector loop, do_generation_relation advances
no_unrecorded_backward_edge_from i to no_unrecorded_backward_edge_from (S i) when the
remembered-set component for 𝑔𝑖 is reset.
   This preservation theorem is used for the next iteration of the collector, not just for the current
graph-isomorphism result. The one-generation isomorphism proof shows that the current collection
preserves what the mutator can observe through the ordinary roots. The recorded-back-pointer
preservation proof shows that the resulting graph and remembered sets are a valid starting point
for later generation collections.

7.4   The garbage-collection loop
The top-level relation garbage_collect_relation follows the C loop shown in Listing 33. The collector
starts at generation 𝑔0 . At each iteration, it ensures that the next generation exists, creating it with
malloc if necessary. It then calls do_generation to copy the current generation into the next one.
If the next generation has enough remaining space, the collector restores the nursery allocation
pointers in the thread_info structure and returns. Otherwise, it proceeds to the next generation.
   The proof of garbage_collect_isomorphism is by induction over this functional loop. The base
case is reflexivity of gc_graph_iso. Besides graph isomorphism, the induction maintains that all
generations younger than the one currently being collected have already been cleared. This auxiliary
invariant holds initially for generation 𝑔0 , and each one-generation collection advances it to the
next generation. In the inductive case, the proof has three steps.
   First, ensuring that the next generation exists is graph-isomorphism neutral. If it already exists,
the graph and heap are unchanged; otherwise, an empty graph generation and its corresponding
unused heap space are added. In either case, the graph and remembered-set invariants needed by
later steps are preserved.
Verification of a Generational Garbage Collector                                                     39


   Second, the roots-isomorphism result for one-generation collection gives the graph-isomorphism
property for the ordinary roots after forward_remset, forward_roots, do_scan, and reset. A separate
reset-preservation result advances the indexed recorded-back-pointer invariant from generation 𝑔𝑖
to generation 𝑔𝑖+1 , for the remembered-set heap passed to the next iteration.
   Third, if the collector loop continues, the induction hypothesis gives graph isomorphism for
the remaining generations. Transitivity of gc_graph_iso then composes the isomorphisms from
ensuring that the next generation exists, collecting the current generation, and executing the
remaining iterations.
   Finally, the theorem garbage_collect_spec_preconditions_imply_isomorphism connects the VST
funspec to the graph-level theorem. Unfolding full_gc and remembered_set_ok provides the
compatibility, collector-entry, and remembered-set facts from which most of the hypotheses of
garbage_collect_isomorphism are derived. The spatial predicate remset_rep entails remset_nodup,
while sound_gc_graph is maintained as a separate semantic invariant. The VST body proof estab-
lishes garbage_collect_relation. Together, these facts yield gc_graph_iso for the mutator’s ordinary
roots.
   Consequently, the C collector may update its internal heap and remembered sets while preserving,
up to isomorphism, the object graph reachable from the mutator’s roots. This is the mutator-facing
property stated in section 3.

8   Future work
   Allocation of large objects. When the mutator wants to allocate a very large array (or immutable
string object), if it is larger than the size of the nursery then the call to garbage_collect can never
satisfy the nalloc requirement (enough headroom in the nursery to allocate the object). What the g.c.
should do in this case is collect all generations smaller than the requested nalloc, and (temporarily)
use generation 𝑘 as the nursery. This would be just a few lines of code, but it is easy to imagine
getting it wrong; hence the utility of formal verification.
   Safe points. Multithreaded garbage-collected systems (including OCaml) need a way to synchro-
nize or suspend threads at safe points in their executions—that is, points where the thread’s set of
live roots is understandable by the collector [Jones et al. 2023, §9.6]. Line 4 of Listing 14 is such a
point: the root pointers have all been stored into the stack-of-frames. If a thread were to be inter-
rupted at some other point, e.g. for the purpose of synchronizing the start of a concurrent garbage
collection, there is no guarantee that the g.c. could accurately find the roots in local variables.
   The mechanism that ML compilers (including SML/NJ and OCaml) use, when it’s desired to
stop some or all threads at safe points, is to set the ti→ limit pointers of those threads (in each
of their thread_info structs) to the start point of their respective allocation spaces. That way, the
next time the thread reaches an available check, it will fail; the root pointers will be stored into the
stack-of-frames (as in Listing 14) and garbage_collect will be called. At that point, garbage_collect
must properly interpret the reason for its invocation: either because the allocation space is truly
exhausted, or because an interrupt is requested.
   For best results, the mutator should perform only a bounded amount of computation between
available checks.
   For correct results, when the mutator fetches ti→ limit, it must do so by an atomic load, i.e., a
machine instruction that has the right semantics to interact with stores that come from another
thread. Other mutator operations need not be atomic (because they operate on a per-thread nursery
not shared with other threads), except for the load or store of a mutable reference.
40                                                        Shengyi Wang, Kathrin Stark, and Andrew W. Appel


  Parallel shared-memory clients in the style of OCaml4 would be straightforward to implement
and mostly straightforward to verify, though it would require using the features of VST for reasoning
about concurrent memory [Mansky and Du 2024].
  Verifying a high-performance parallel collector. A more ambitious project would be to verify the
OCaml5 collector [Sivaramakrishnan et al. 2020]. One of the design goals of that collector was to
be compatible with the OCaml’s legacy mutator/collector interface. So it would be interesting to
see which changes would be needed to the specification interface that we described in section 3.
   Tracing in and out of external objects. Our theory of external objects is sufficient for (1) code
blocks of closures, (2) abstract objects totally managed by the runtime system, and (3) external root
pointers (into the heap) managed by the runtime system. But we have not demonstrated that one
can reason effectively about traversable data structures that span between the g.c.-managed heap
and the runtime-system-managed malloc/free arena.
   The OCaml5 forward function is called oldify_one, and it supports some features that we don’t
support:
     • OCaml (4 or 5) has special support for lazy objects, which have their own tag.
     • OCaml objects can be nested within other objects; these are called Infix objects with a
        special tag value, and the surrounding object must be found and forwarded.
     • The queue of objects that have been copied and whose fields have not yet been forwarded,
        which Cheney’s algorithm keeps in the (contiguous) to-space between scan and next, cannot
        be kept in that way, because the to-space is not organized that way. Instead, a “to-do list” is
        linked through all the objects that have been copied and not yet scanned. The to-do list is
        kept depth-first, but (unlike the system we described in section 5) this does not necessarily
        improve cache locality because the to-space is not a series of consecutive blocks.
        The following items are specific to OCaml 5.
     • Reading the header is done by an acquire-mode atomic load, to synchronize in case some
        other shared-memory thread already started forwarding this object.
     • To allocate the destination block, where our forward function can simply add
        (1 + 𝑛) · WORD_SIZE to next, OCaml5 must find a block of the right size in a local pool of
        free blocks within the shared major generation.
     • When the destination block has been allocated, the function must check again whether
        some other thread is forwarding this object (and if so, abandon the newly allocated block as
        garbage).
     • Continuations (pointers to the stacks of “fibers” (lightweight threads within an operating-
        system thread) are tagged with Cont_tag, and must be handled specially.
     • The “to-do list” is kept in a per-thread state structure, rather than in a global variable.
Verifying the OCaml5 collector would be quite challenging because of the sophisticated techniques
used to deal with concurrency.

9    Conclusion
We set out to verify a “real-world” garbage collector, in the sense that it is a separate and portable
C program with a standard API usable by multiple client systems; and where that API could be
formalized into a specification strong enough to prove client programs (mutators) correct.
   The proof required significantly more effort than we expected, perhaps for several reasons:
     • As described by Appel and Naumann [2020]:
            VST proofs are typically rather verbose (an order of magnitude more lines of proof
            than lines of code), but in this case the proof is particularly lengthy (compared
Verification of a Generational Garbage Collector                                                                     41


               to the C code). We believe the reason for this is that a malloc/free program is
               particularly abusive of the C type system: casting undifferentiated memory into
               linked data structures, returning pointers that are one past the header word,
               making sure that those pointers are double-word aligned, and so on. All this abuse
               is legal in C11, but needs formal justification. In contrast, the proofs of more “well
               behaved” C code are a bit more automated by VST’s proof tactics.
         The particularly high ratio of proof to code that they described in verifying a malloc/free
         memory manager also applies to an automatic garbage collector, for some of the same
         reasons.
      • Garbage collectors manipulate graphs with sharing and (sometimes) cycles; to fit this
         into separation logic (where separation is the antithesis of sharing) required a graph-
         reasoning system such as CertiGraph. Such reasoning also increases the proof-to-code ratio.
         (Malloc/free systems may represent graphs with sharing but the verification of malloc/free
         itself does not require reasoning about those graphs.)
      • Adding mutable_update—and in general the handling of remembered sets in each generation—
         required changes to many of the invariants that we had designed for the generational
         collector without mutable update.
      • Handling outliers, pointers from outside the heap into it, and vice versa, significantly
         complicated our reasoning in some places. Most other garbage-collector proofs prohibit
         outliers (or are not sound for the semantics of C pointer comparison). But many real-life
         clients need them, for interaction with runtime systems, so we chose to provide them.
      • Adjusting the specification of the collector to be usable in correctness proofs of clients (that
         call the collector) required careful refactoring.
Clients, too, need to reason about graphs with sharing. An important part of the (informal) spec-
ification of systems such as OCaml, Haskell, SML/NJ is that they do not duplicate objects. That
is, let y : int→ int = f x in (y,y) does not compile to (f x, f x) with two function closures, there
is a single function closure with two pointers to it. So our g.c. specification also provides the
graph-reasoning theory directly usable in client-compiler proofs.
   We chose a multigeneration copying collector because its implementation is simple and rea-
sonably efficient. But a more common modern arrangement (not only in OCaml) is a hybrid
two-generation collector, with copying collection for the nursery and mark-sweep for the older
generation. Parts of our collector (and proof) should be reusable in such a scenario, but (as we have
explained) there are some significant differences.

Acknowledgments
This work was funded in part by National Science Foundation grant CCF-2005545.

References
Abhishek Anand, Andrew Appel, Greg Morrisett, Zoe Paraskevopoulou, Randy Pollack, Olivier Savary Belanger, Matthieu
  Sozeau, and Matthew Weaver. 2017. CertiCoq: A verified compiler for Coq. In CoqPL: Third International Workshop on
  Coq for Programming Languages. CoqPL, Paris, France, 2 pages. https://www.cs.princeton.edu/~appel/papers/certicoq-
  coqpl.pdf
Andrew W. Appel. 1990. A Runtime System. Lisp and Symbolic Computation 3, 4 (1990), 343–80. doi:10.1007/BF01807697
Andrew W. Appel, Robert Dockins, Aquinas Hobor, Lennart Beringer, Josiah Dodds, Gordon Stewart, Sandrine Blazy, and
  Xavier Leroy. 2014. Program Logics for Certified Compilers. Cambridge, Cambridge, UK. doi:10.1017/CBO9781107256552
Andrew W. Appel and David A. Naumann. 2020. Verified Sequential Malloc/Free. In International Symposium on Memory
  Management (ISMM). Association for Computing Machinery, New York, NY, USA, 48–59. doi:10.1145/3381898.3397211
Michaël Armand, Benjamin Grégoire, Arnaud Spiwack, and Laurent Théry. 2010. Extending Coq with Imperative Features
  and Its Application to SAT Verification. In Interactive Theorem Proving, Matt Kaufmann and Lawrence C. Paulson (Eds.).
42                                                                  Shengyi Wang, Kathrin Stark, and Andrew W. Appel


   Springer, Berlin, Heidelberg, 83–98.
Qinxiang Cao, Lennart Beringer, Samuel Gruetter, Josiah Dodds, and Andrew W. Appel. 2018. VST-Floyd: A Separation Logic
   Tool to Verify Correctness of C Programs. J. Autom. Reasoning 61, 1-4 (2018), 367–422. doi:10.1007/s10817-018-9457-5
Edsger W. Dijkstra. 1968. Cooperating Sequential Processes. In Programming Languages, F. Genuys (Ed.). Academic Press,
   New York, NY, 43–112.
Marcelo J. R. Gonçalves and Andrew W. Appel. 1995. Cache Performance of Fast-Allocating Programs. In Proc. 7th Int’l Conf.
   on Functional Programming and Computer Architecture. ACM Press, New York, 293–305.
Armaël Guéneau, Magnus O. Myreen, Ramana Kumar, and Michael Norrish. 2017. Verified Characteristic Formulae for
   CakeML. In Programming Languages and Systems: 26th European Symposium on Programming. Springer, Berlin, Heidelberg,
   584–610. doi:10.1007/978-3-662-54434-1_22
Richard Jones, Antony Hosking, and Eliot Moss. 2023. The Garbage Collection Handbook (2nd ed.). Chapman and Hall/CRC,
   Boca Raton, FL. doi:10.1201/9781003276142
Joomy Korkut. 2024. Foreign Function Verification Through Metaprogramming. Ph. D. Dissertation. Princeton University.
   http://arks.princeton.edu/ark:/88435/dsp01k930c143z
Joomy Korkut, Kathrin Stark, and Andrew W. Appel. 2025. A Verified Foreign Function Interface between Coq and C. Proc.
   ACM Program. Lang. 9, POPL, Article 24 (Jan. 2025), 31 pages. doi:10.1145/3704860
Xavier Leroy, Andrew W. Appel, Sandrine Blazy, and Gordon Stewart. 2014. The CompCert Memory Model. See [Appel
   et al. 2014], Chapter 32, 237–271. doi:10.1017/CBO9781107256552
Henry Lieberman and Carl Hewitt. 1983. A Real-Time Garbage Collector Based on the Lifetimes of Objects. Commun. ACM
   26, 6 (1983), 419–429. doi:10.1145/358141.358147
William Mansky and Ke Du. 2024. An Iris Instance for Verifying CompCert C Programs. Proc. ACM on Programming
   Languages 8, POPL, Article 6 (Jan. 2024), 27 pages. doi:10.1145/3632848
Andrew McCreight, Tim Chevalier, and Andrew Tolmach. 2010. A certified framework for compiling and executing garbage-
   collected languages. In ICFP’10: 15th ACM SIGPLAN International Conference on Functional programming. Association for
   Computing Machinery, New York, NY, USA, 273–284. doi:10.1145/1863543.1863584
Andrew McCreight, Zhong Shao, Chunxiao Lin, and Long Li. 2007. A general framework for certifying garbage collectors
   and their mutators. In PLDI’07: 28th ACM SIGPLAN Conference on Programming Language Design and Implementation.
   Association for Computing Machinery, New York, NY, USA, 468–479.
Yaron Minsky and Anil Madhavapeddy. 2022. Real World OCaml. Cambridge University Press, Cambridge, UK. doi:10.1017/
   9781009129220
Zoe Paraskevopoulou, John M. Li, and Andrew W. Appel. 2021. Compositional optimizations for CertiCoq. Proc. ACM
   Program. Lang. 5, ICFP, Article 86 (Aug. 2021), 30 pages. doi:10.1145/3473591
John H. Reppy. 1993. A High-Performance Garbage Collector for Standard ML. Technical Memorandum. AT&T Bell
   Laboratories, Murray Hill, NJ. https://people.cs.uchicago.edu/~jhr/papers/1993/tm-gc.pdf
Adam Sandberg Ericsson, Magnus O. Myreen, and Johannes Åman Pohjola. 2019. A Verified Generational Garbage Collector
   for CakeML. J. Automated Reasoning 63 (2019), 463–488. doi:10.1007/s10817-018-9487-z
Sheera Shamsu, Dipesh Kaphle, Dhruv Maroo, Kartik Nagar, Karthikeyan Bhargavan, and KC Sivaramakrishnan. 2024. A
   Mechanically Verified Garbage Collector for OCaml. doi:10.21203/rs.3.rs-4674167/v1 preprint.
KC Sivaramakrishnan, Stephen Dolan, Leo White, Sadiq Jaffer, Tom Kelly, Anmol Sahoo, Sudha Parimala, Atul Dhiman, and
   Anil Madhavapeddy. 2020. Retrofitting parallelism onto OCaml. Proc. ACM Program. Lang. 4, ICFP, Article 113 (Aug.
   2020), 30 pages. doi:10.1145/3408995
Shengyi Wang. 2026. AI-Assisted Completion of CertiGC Proofs: An Experience Report. arXiv:2606.21167 https://arxiv.org/
   abs/2606.21167
Shengyi Wang, Qinxiang Cao, Anshuman Mohan, and Aquinas Hobor. 2019. Certifying Graph-Manipulating C Programs
   via Localizations within Data Structures. Proc. ACM Program. Lang. 3, OOPSLA, Article 171 (Oct. 2019), 30 pages.
   doi:10.1145/3360597
Albert Mingkun Yang and Tobias Wrigstad. 2022. Deep Dive into ZGC: A Modern Garbage Collector in OpenJDK. ACM
   Trans. Program. Lang. Syst. 44, 4, Article 22 (Sept. 2022), 34 pages. doi:10.1145/3538532
Verification of a Generational Garbage Collector                                                       43


A    Open-source Rocq proof
Our Rocq proofs are available open-source at https://github.com/CertiGraph/CertiGraph/releases/
tag/v2.0, in the CertiGC directory of that repo, organized as follows:
     GC_Source/gc_stack.{h,c}: C source code (including Listings 1, 22, 25, 26, 30, 32, 34).
     gc_spec.v: Function specifications of all the C functions (Listings 11, 16, 28, 35).
     verif_forward.v, verif_forward{1,2}.v: Correctness proof of the forward function.
     verif_do_scan.v: Correctness proof of the do_scan function.
     verif_forward_remset.v: Correctness proof of forward_remset.
     verif_forward_roots.v: Correctness proof of forward_roots.
     verif_do_generation.v: Correctness proof of do_generation.
     verif_garbage_collect.v: Correctness of the client-facing function garbage_collect().
     gc_correct.v: Proof of correctness of the functional model (see section 7).
     verif_mutable_update.v: Proof of correctness of mutable_update.
  To build the garbage collector proof, run make certigc. To execute the Rocq Print Assumptions
command that verifies that there are no unexpected axioms or unproved lemmas, run
make CertiGC/assumptions.vo.
  The “top-level specification” or “main theorem” is, effectively, the specification contract between
the mutator and the g.c. We described this (informally) in section 2 and (formally) in section 3. To
see the complete specification, one would examine in particular,
     • In gc_spec.v, the function specs garbage_collect_spec and int_mutable_update_spec (which
        allows the client to update a mutable reference that’s in the g.c.-managed heap).
     • In spatial_gc_graph.v, the definitions of predicates referenced from those two funspecs.
     • In gc_correct.v, Theorem garbage_collect_isomorphism states that the functional model
        (which the C function garbage_collect is proved to implement) correctly produces the
        appropriate isomorphic subgraph; Theorem mutable_update_gc_ready states that mutable-
        ref-update produces the appropriate relation on graphs.

B    The C semantics of tag bits
Most implementations of ML (e.g., OCaml, Standard ML of New Jersey) use the low-order-bit tagged
representation described above: even numbers are pointers, odd numbers are non-pointer data.
Both the mutator and the g.c. must test the low-order bit of a value to determine how to handle it.
But in the official semantics of C, this test is undefined behavior! That is, taking a pointer value and
doing a bitwise-and (or by other means such as modulo) is not permitted in portable C programs.
When we prove C programs correct, we use the VST program logic that is proved sound w.r.t. the
formal semantics of C, and it would be impossible to prove such a program correct.
   But such programs are correct, in the sense that they work correctly in any standard implemen-
tation of C (such as gcc, clang, CompCert). So we axiomatize an extension to the C standard that
permits just enough nonstandard (but commonly supported) operations to implement a garbage
collector.
   Each of the functions in Listing 34 has a simple implementation. Their specifications in List-
ing 35, in the VST format, are straightforward. For example, test_int_or_ptr_spec says that the
test_int_or_ptr function has no spatial footprint (SEP()), that the C function’s sole parameter has
the C type which VST calls int_or_ptr_type, and that the CompCert value x passed in that parameter
is a valid_int_or_ptr—meaning that if it’s a pointer, then its low-order bit is 0, and if it’s an integer,
then 1.
44                                                           Shengyi Wang, Kathrin Stark, and Andrew W. Appel


                            Listing 34. Pointer/integer testing and conversion
int test_int_or_ptr (value x) /∗ 1 if int, 0 if aligned ptr ∗/ { return (int)(((int)x)&1); }

int int_or_ptr_to_int (value x) /∗ precondition: is int ∗/ { return (int)x; }

void ∗ int_or_ptr_to_ptr (value x) /∗ precond: is aligned ptr ∗/ { return (void ∗)x; }

value int_to_int_or_ptr(int x) /∗ precondition: is odd ∗/ { return (value)x; }

value ptr_to_int_or_ptr(void ∗x) /∗ precondition: is aligned ∗/ { return (value)x; }

                   Listing 35. Specifications for pointer/integer testing and conversion
Definition test_int_or_ptr_spec :=
 DECLARE _test_int_or_ptr
 WITH x : val
 PRE [int_or_ptr_type] PROP (valid_int_or_ptr x) PARAMS (x) SEP ()
 POST [ tint ]
   PROP() RETURN(Vint (Int.repr (match x with Vlong _ ⇒ 1 | _ ⇒ 0 end))) SEP().

Definition int_or_ptr_to_int_spec :=
 DECLARE _int_or_ptr_to_int
 WITH x : val
 PRE [int_or_ptr_type ] PROP (is_int I32 Signed x) PARAMS (x) SEP ()
 POST [ tlong ] PROP() RETURN (x) SEP().

Definition int_or_ptr_to_ptr_spec :=
 DECLARE _int_or_ptr_to_ptr
 WITH x : val
 PRE [int_or_ptr_type ] PROP (isptr x) PARAMS (x) SEP ()
 POST [ tptr tvoid ] PROP() RETURN (x) SEP().

Definition int_to_int_or_ptr_spec :=
 DECLARE _int_to_int_or_ptr
 WITH x : val
 PRE [ tlong ] PROP (valid_int_or_ptr x) PARAMS (x) SEP ()
 POST [ int_or_ptr_type ] PROP() RETURN (x) SEP().

Definition ptr_to_int_or_ptr_spec :=
 DECLARE _ptr_to_int_or_ptr
 WITH x : val
 PRE [tptr tvoid ] PROP (valid_int_or_ptr x) PARAMS (x) SEP()
 POST [ int_or_ptr_type ] PROP() RETURN (x) SEP().
Verification of a Generational Garbage Collector                                                       45


   Then the specification of int_or_ptr_to_int has a precondition that its input value 𝑥 is an integer
value, not a pointer value. To satisfy that precondition, the C program could call test_int_or_ptr
before calling either int_or_ptr_to_int or int_or_ptr_to_ptr.
   In the standard C semantics (provided by VST), it would be impossible to prove that test_int_or_ptr
satisfies its specification. But its specs are consistent with the C standard, i.e., they are a refinement
of the standard. So we can safely axiomatize it, as a way of claiming that the C compilers we care
about (gcc, clang, CompCert) guarantee this extension to the standard.
   The C specification permits casting an integer to a pointer, provided that no pointer operations
are performed on it before it is cast back to an integer—and vice versa. Thus, the C semantics does
permit holding an integer in a variable of type void∗. So the remaining functions can be proved
correct using the C semantics, though at present we have axiomatized them as well.
   VST’s separation logic assumes that a value of type void∗ is a pointer value, not an integer value.
To indicate to VST that our value type can hold either a pointer or an integer (which VST calls
int_or_ptr_type) we mark the void∗ type with a special attribute (see Listing 1). The attribute we
use is does not alter the C semantics, but serves as a hint to VST about how to treat variables and
fields of this type.

C    The C semantics of range testing
The forward function (Listing 22, line 6) tests whether a pointer v points within the from-space,
using the Is_from function defined as follows:
int Is_from(value∗ from_start, value ∗ from_limit, value ∗ v)
  { return (from_start <= v && v < from_limit); }
Pointer range testing is a standard operation in many garbage collectors, but it is illegal in the
standard C semantics! The pointer comparisons 𝑝 < 𝑞 or 𝑝 ≤ 𝑞 in the official semantics of C
require that 𝑎 and 𝑏 both be pointers into (or at the end of) the same allocated block, otherwise the
comparison is undefined behavior. C requires this to avoid situations such as,
     p = (char ∗)malloc(n);
     if (...) free(p);
     q = (char ∗)malloc(n);
     if (p<=q) {...}
If free(p) is executed, this will have different behavior depending on whether malloc re-uses the
same block. If free(p) is not executed, this tests whether malloc chooses to place the new block
before or after the old block. The designers of the C semantics wanted to prevent (legal) programs
from depending on such implementation choices in malloc. Similar considerations apply when p
or q are pointers to stack-allocated local variables.
   However, to test whether p points within the from-space, we need the range comparison
from_start≤p<from_limit, where it is guaranteed that from_start and from_limit are in the same
malloc’ed block and that p points within some malloc’ed block (i.e., generation). This comparison
is illegal in the standard C semantics, but essentially all garbage collectors must do it and it is
assured to work properly in all C compilers—and it cannot inappropriately test the behavior of
malloc. Therefore it is safe to extend the semantics of C to axiomatize the behavior of this range
comparison.
   For the comparison 𝑝 <= 𝑞 && 𝑞 < 𝑟 , our axiom has the precondition that 𝑝 and 𝑟 are in (or point
just past) the same malloc’ed block, and that 𝑞 points within (or just past) some allocated block.
We can express these conditions as predicates in the Verifiable C separation logic.
