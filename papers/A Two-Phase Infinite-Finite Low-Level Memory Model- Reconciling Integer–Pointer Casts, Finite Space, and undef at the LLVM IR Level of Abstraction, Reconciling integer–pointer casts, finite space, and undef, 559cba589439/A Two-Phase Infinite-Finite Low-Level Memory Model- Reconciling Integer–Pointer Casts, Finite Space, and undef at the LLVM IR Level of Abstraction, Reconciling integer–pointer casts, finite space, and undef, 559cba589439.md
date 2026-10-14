                                         A Two-Phase Infinite/Finite Low-Level Memory Model
                                         Reconciling integer–pointer casts, finite space, and undef at the LLVM IR level of abstraction
arXiv:2404.16143v1 [cs.PL] 24 Apr 2024




                                         CALVIN BECK, University of Pennsylvania, USA
                                         IRENE YOON, University of Pennsylvania, USA
                                         HANXI CHEN, University of Pennsylvania, USA
                                         YANNICK ZAKOWSKI, Inria & LIP (UMR CNRS/ENS Lyon/UCB Lyon1/INRIA), France
                                         STEVE ZDANCEWIC, University of Pennsylvania, USA
                                         This paper provides a novel approach to reconciling complex low-level memory model features, such as
                                         pointer–integer casts, with desired reﬁnements that are needed to justify the correctness of program trans-
                                         formations. The idea is to use a “two-phased” memory model, one with and unbounded memory and corre-
                                         sponding unbounded integer type, and one with a ﬁnite memory; the connection between the two levels is
                                         made explicit by our notion of reﬁnement that handles out-of-memory behaviors. This approach allows for
                                         more optimizations to be performed and establishes a clear boundary between the idealized semantics of a
                                         program and the implementation of that program on ﬁnite hardware.
                                            To demonstrate the utility of this idea in practice, we instantiate the two-phase memory model in the con-
                                         text of Zakowski et al.’s VIR semantics [38], yielding inﬁnite and ﬁnite memory models of LLVM IR, including
                                         low-level features like undef and bitcast. Both the inﬁnite and ﬁnite models, which act as speciﬁcations,
                                         can provably be reﬁned to executable reference interpreters. The semantics justify optimizations, such as
                                         dead-alloca-elimination, that were previously impossible or diﬃcult to prove correct.
                                         Additional Key Words and Phrases: low-level memory model, integer–pointer casts, semantics

                                         1   INTRODUCTION
                                         After 50 years the memory model for a programming language like C should be well understood!
                                         Unfortunately, memory models for low-level languages like C and LLVM IR are quite subtle and
                                         complex, especially when considered in the context of optimizations and program transforma-
                                         tions [2–5, 12, 17–19, 21, 24, 25, 30, 31]. Why? These languages provide an abstract view of mem-
                                         ory to justify a wide range of “high-level” optimizations—often pretending that available memory
                                         is unbounded and that allocations yield disjoint blocks, where a pointer to one allocated block can
                                         never be used to access adjacent blocks from diﬀerent allocations—but these languages also allow
                                         for low-level access to the memory, yielding a high degree of control and performance. Unfortu-
                                         nately, these two extremes are at odds, and it is diﬃcult to ensure that the semantics of low-level
                                         memory operations preserve the invariants expected by the high-level optimizations.
                                            This tension between low-level memory operations and high-level optimizations is evident in
                                         pointer arithmetic operations. Pointer arithmetic operations allow programmers to manipulate
                                         memory addresses as integer values, which exposes the underlying concrete memory layout. When
                                         the concrete memory layout is exposed, the behavior of a program can depend upon where values
                                         are allocated in memory, which can severely limit which optimizations can be performed. For
                                         instance, the assignment a[i] = 2 could overwrite any other value in memory if a[i] is out of
                                         bounds of the array a (the underlying pointer arithmetic is hidden by the array index notation).
                                         That sounds reasonable when considering how this program would execute on a speciﬁc machine
                                         at a low level, but it is disastrous from the perspective of an optimizing compiler! Even if a is
                                         dead (i.e., never read from again), the compiler can’t remove this store because it might alias with

                                         Authors’ addresses: Calvin Beck, University of Pennsylvania, Philadelphia, PA, USA, hobbes@seas.upenn.edu; Irene Yoon,
                                         University of Pennsylvania, USA, euisuny@cis.upenn.edu; Hanxi Chen, University of Pennsylvania, USA, hanxic@seas.
                                         upenn.edu; Yannick Zakowski, Inria & LIP (UMR CNRS/ENS Lyon/UCB Lyon1/INRIA), Lyon, France, yannick.zakowski@
                                         inria.fr; Steve Zdancewic, University of Pennsylvania, USA, stevez@cis.upenn.edu.
2                                        Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


something that is live. To justify removing a (seemingly) dead store, the compiler would also have
to prove that i is in bounds, but because i can be the result of an arbitrary computation this can
be diﬃcult, if not impossible. What is a compiler (or compiler implementor) to do?
   Programming languages like C and LLVM use the notion of “undeﬁned behavior” (or “UB”) to
justify the correctness of “high-level” optimizations without the need for complicated reasoning
(like determining whether a[i] is in bounds). The compiler assumes that the program doesn’t
exhibit undeﬁned behavior. For instance, by declaring that out-of-bounds accesses are UB, the
compiler only needs to determine that a isn’t read from again to justify deleting the dead a[i] = 2
store—the compiler assumes that a[i] is in bounds, so we don’t need to worry about it aliasing
with anything except elements of a. Programs given to the compiler must not exhibit UB or the
optimizations it performs won’t be valid, potentially leading to unexpected results, but, in return,
the compiler is able to perform much more aggressive optimizations.
   While UB can be a very powerful tool, it can, unfortunately, be diﬃcult to deﬁne the semantics
of a programming language and its memory model such that situations that impact optimizations
are classiﬁed as UB. This is particularly challenging in the context of more realistic memory mod-
els, such as those involving ﬁnite memory, in which seemingly pure operations may have visible
side eﬀects, like exhausting memory. For instance Lee, et al. [21] note that, in the case of ﬁnite
memory, there is a side-channel that can be used to accurately guess the physical address of other
blocks, making it diﬃcult to rule out pointer aliasing brought about by casting arbitrary integers
to pointers. Similarly (but perhaps counter-intuitively) in a ﬁnite memory model, it is, in general,
unsound to remove a dead allocation operation: allocating less memory can turn a program that
always runs out of space into one that makes more progress, thereby introducing more behaviors
after optimization—to justify removing the allocation, the compiler would have to also prove that
the allocation always succeeds! (This is the strategy taken in CompCertS [4].)
   These situations may seem unimportant: Who cares if a program can determine the physical
address of a block without directly observing it through a pointer–integer cast? Isn’t the goal of
removing an allocation to save memory, potentially allowing the program to make more progress?
However, properly accounting for such semantics is essential for ensuring that the compiler makes
consistent assumptions—inconsistency can lead to end-to-end miscompilation bugs and subtle er-
roneous interactions between optimization passes.1 It is also vital in the context of formal veriﬁca-
tion, which aims for optimizations to be “provably correct.” For example, if the memory model does
not rule out the possibility that a program can determine the physical address of some block, it can
be impossible to justify an optimization that depends on memory locations being unaliased. Ulti-
mately, an incoherent memory model leads to buggy software, and complicates formally verifying
optimization passes.
   Pointer–integer casts are a major sticking point for memory models [4, 17]. These casts expose
the bare bones of the memory layout, which complicates alias analysis and can invalidate many
optimizations, but these casts also bring a more subtle and sinister issue into play: cardinality. Most
programming languages at this level of abstraction have integers with ﬁnite bitwidths; however,
compilers and programmers pretend that there is no limit to the number of pointers a program can
allocate, as doing so greatly simpliﬁes reasoning (see the discussion in Lee, et al. [21]). This dis-
crepancy between ﬁnitary integers and inﬁnitary pointers means that one of the following design
choices must be made: (1) a cast from a pointer to an integer can fail, (2) casting from a pointer
to an integer and back does not necessarily yield the original pointer, and thus causes unexpected
1 There   are numerous discussions about such semantics problems on the LLVM IR github issue tracker
https://github.com/llvm/llvm-project/issues/. A few examples particularly germane to our focus are 54002, 55061,
52930, 33896, and, especially, 34577: LLVM Memory Model needs more rigor to avoid undesired optimization results, which
has been open since 2017.




©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                 3


aliasing, or, (3) we must admit that memory is ﬁnite and make the pointer types ﬁnite as well. All of
these options have implications for program transformations: (1) means that pointer–integer casts
are eﬀectful, instead of being (pure) no-ops, which means they can’t easily be removed, (2) means
that any code using a cast may result in pointers being truncated, which means it could cause
aliasing, thereby invalidating many optimizations, and, (3) has many complicated consequences,
including being unable to remove dead allocations (as mentioned above).
   The big(int) idea. This paper proposes a new way to reconcile the desired features mentioned
above. In particular, we present a semantics for low-level languages that provides an account of
pointer–integer casts, while dealing with ﬁnite memory and justifying many desirable optimiza-
tions. The key insight is that, for such a language, there are really two memory models in play: one
that assumes an unbounded amount of memory and the presence of an “unbounded integer type”
(akin to bigint) for which there can be an injection from pointers to these unbounded integers,
and a second that assumes a ﬁnite memory and in which all pointers and integer types have ﬁnite
bitwidths. The advantage of this is that many optimizations, such as dead allocation elimination,
are always valid in the inﬁnite memory model without any additional reasoning (though some
optimizations are valid in both). Optimizations should primarily be performed with respect to the
inﬁnite memory model, and then the program should be translated safely to the ﬁnite memory
model for subsequent lowering to machine code. This explicit translation step that converts the
program from the inﬁnite model to the ﬁnite one is (almost) just the identity translation on syntax.
Semantically, it may introduce new out-of-memory behaviors, but otherwise, the translated code
retains a precisely speciﬁed connection to its inﬁnitary behavior. The upshot is that we can rea-
son about the impact of a compiler’s optimizations in phases, but still have end-to-end guarantees
about a program’s behaviors that are suﬃcient to ensure correct compilation. In contrast, existing
models for languages like LLVM IR don’t separate these phases, which muddles the semantics and
makes the assumptions unclear. While our focus is on languages that straddle the barrier between
low-level memory accesses and high-level optimizations like LLVM IR and C, these ideas should
be relevant to all higher-level languages that assume there is inﬁnite memory and must ultimately
be compiled to run on machines with ﬁnite memory.
   Although this idea seems simple at ﬁrst blush, working through all of the many details turned
out to be highly nontrivial—for instance, in the inﬁnite phase, one must address2 what it means
to store an “inﬁnitely wide” pointer into a data structure that is serialized into a form stored in
memory. To handle that, we observe that the inﬁnite model’s behaviors in such cases are always
(eventually) lowered to the ﬁnite model’s, which gives us a degree of wiggle room: in the inﬁnite
memory model, reading such an inﬁnitely wide pointer “atomically” from memory can be loss-
less, but—even in the inﬁnite model—reading such a stored pointer byte-by-byte can truncate the
pointer. So long as the ﬁnite model reﬁnes these behaviors, it will behave “as expected.”
   In summary, this paper makes the following contributions:
      • We explain the design rationale of this two-phase inﬁnite/ﬁnite memory model in the con-
        text of related state-of-the-art memory models for languages that support integer–pointer
        casts. See Section 2.
      • We formalize the proposed memory model in the Coq theorem prover. The axiomatic de-
        scription allows for many possible implementations, and we use Coq’s module features to
        share the deﬁnitions common to the inﬁnite and ﬁnite models. Each model is parameterized
        by a few basic abstractions (symbolic bytes and addresses) that should be relevant in any
        low-level programming language. The basic interface is given by just seven byte-oriented

2 Pun intended!




©2024 Copyright held by the owner/author(s).
4                                        Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


        operations, which can be used to build methods for working with aggregate data such as
        vectors or structs. See Section 3.
      • We deﬁne the relevant notions of simulation in both the inﬁnite and ﬁnite models and prove
        that the translation from the inﬁnite to the ﬁnite phase is a suitable reﬁnement, introducing
        only new out-of-memory behaviors.
      • To demonstrate the suitability of these ideas for modeling “real world” languages, we in-
        stantiate the memory models in the context of an existing formal semantics VIR, for LLVM
        IR, based on the work by Zakowski, et al. [38]. The VIR semantics aims to be a speciﬁ-
        cation for a large, practically applicable subset of LLVM IR, but its prior memory models
        suﬀered from the deﬁciencies with respect to optimization correctness mentioned above.
        We choose this setting because VIR (and LLVM IR) supports a rich, C-like structured mem-
        ory model, including integer–pointer casts; it also includes undef and poison values that
        interact non-trivially with the speciﬁcation because they introduce nondeterminism and
        aﬀect the notion of Undeﬁned Behavior. Our instantiation handles a superset of the fea-
        tures supported by previous versions of VIR, giving us conﬁdence that our memory model
        scales to realistic features sets. See Section 4.
      • Besides the speciﬁcation of the memory models, which is intended to be a logical (and
        hence nondeterministic) characterization of the set of allowed behaviors, we also deﬁne ex-
        ecutable implementations for the VIR semantics (for both inﬁnite and ﬁnite memories). We
        formally prove that these implementations reﬁne the corresponding speciﬁcations. These
        executable semantics let us both test VIR against other LLVM IR implementations (specif-
        ically clang) and use Quickchick-style [11] randomized testing to probe the behaviors of
        our model.
      • We further demonstrate the utility of this semantics for formal veriﬁcation by proving the
        correctness of instances of dead-alloca elimination and dead ptrtoint cast elimination,
        which are representative of the reasoning needed to prove full-scale compiler optimizations
        such as register promotion and global-value numbering. We brieﬂy describe these results
        in Section 5.
   Although our proposal provides a piece of the puzzle for deﬁning a “full” memory model for
low-level languages like C or LLVM IR, we deliberately do not consider some features in this paper,
leaving them to other (future) work. In particular, we omit concurrency altogether because there
has already been much research on concurrent memory models, especially for relaxed-memory
semantics, for such languages like C and the LLVM IR [1, 8, 16, 23, 33, 34]. Our treatment of inﬁnite–
ﬁnite reﬁnement should be orthogonal to those proposals, but we expect it would take non-trivial
engineering eﬀort to combine them. We also elide and/or simplify some details of LLVM IR that
are not really relevant or that we expect to be straight forward to implement using this model;
Section 4 describes the features we do consider.
   Our formal semantics speciﬁcation, the VIR implementations, and the claimed theorems are fully
implemented and proved in the Coq interactive theorem prover. However, the full development is
very large, relies heavily on Coq-speciﬁc details, and is a bit more general than what we need here.
Thus, for the purposes of this paper, we have liberally simpliﬁed and streamlined the presentation,
in-lining, renaming, and sharing some deﬁnitions when compared to the Coq code.3


3 For reviewers: we have submitted an anonymized version of the repository for evaluation with the paper and, should

the paper be accepted, we plan to submit a (cleaned up and better documented) version of the development for artifact
evaluation. We will try to make the correspondence between the claims in this paper and the Coq code as transparent and
accessible as we can, despite the simpliﬁcations made for the sake of presentation.




©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                        5


    Model             PtoI           ItoP            Finite        Ext.   Optimizations
                                                                   Mem.
    Concrete          No-Op          No-Op           Yes           No     Bad
    Logical Blocks    Unsupported    Unsupported     No            No     Good
    Quasi-Concrete    Eﬀectful       Yes             No, awkward   No     Good when no PtoI casts, can-
                                                                          not remove PtoI casts if con-
                                                                          crete memory is ﬁnite
    Twin-Allocation   No-Op          No-Op           Yes           Yes    Cannot remove dead alloca-
                                                                          tions
    CompCertS         No-Op          No-Op           Only Finite   Yes    Have to prove optimizations
                                                                          use less memory
    Ours              No-Op          No-Op           2-Stages      No     Staged between inﬁnite + ﬁ-
                                                                          nite compilation allow more
                                                                          optimizations
Fig. 1. Comparison of various low-level memory models. Columns PtoI and ItoP describe pointer–to-int
and int-to-pointer support, column Finite indicates support for finite memory, and Ext. Mem. describes
whether the memory model requires extra memory.


2     REMEMBERING LOW-LEVEL MEMORY MODELS
To put our work in context, this section provides an overview of some basic memory models,
focusing on which kinds of optimizations they allow, especially in the context of pointer arithmetic,
pointer–integer casts, and ﬁnite memory. We’ll start by reviewing a basic concrete memory model,
compare it to a logical memory model (which does not support low level memory operations,
but supports more optimizations), and then look at several memory models that bridge the gap
between these two extremes, namely, the Quasi-Concrete model [17], the Twin-Allocation model
[21], and the CompCertS ﬁnite memory model [4]. The summary of the comparison is given in
Figure 1.

2.1 Fully Concrete
One of the simplest memory models is a completely concrete one where memory is modeled by an
array of bytes. Each allocation is assigned its own unique physical pointer which is just an integer
index into the memory array. Modeling pointer–integer casts under this memory model is trivial
as pointers really are just integer indices, making the casts noops. Furthermore, ﬁnite memory can
easily be modiﬁed by simply restricting the size of the array.
   This model of memory is perfectly reasonable, and is
quite similar to how the memory in a physical computer ac- int main(int argc, char *argv[]) {
tually works; unfortunately, these memory models are too              char *a = malloc(4);
concrete. The physical memory layout is not abstract at all,          char *b = malloc(4);
                                                                      *b = 1;
making it diﬃcult to justify high level optimizations. For ex-
                                                                      char *c = a + f(0);
ample, consider the program shown to the right.                       *c = 2;
   It looks like *b is not modiﬁed after initialization, so           // What can this print?
it’s sensible to use store forwarding to optimize away the            printf("%d\n", *b);
extra load from *b, and replace the call to printf with               // optimized: printf("%d\n", 1)
                                                                      return 0
printf("%d\n", 1) (which would enable further optimiza-
                                                                  }
tions as b would now be dead). Unfortunately, the sim-
ple concrete memory model can’t justify this optimization
when c == a + f(0) == b, as this would mean that the write to *c overwrites the value stored
in *b, and so it should print 2 instead of 1. If we want to perform this optimization, we’ll now have



©2024 Copyright held by the owner/author(s).
6                                  Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


to know where a and b can be allocated in memory, and what the function call f(0) evaluates to.
This is a lot of work for the compiler to justify a simple optimization, especially when the only
reason it won’t work is in the kind of degenerate case where you use a to generate a pointer to b,
which should be out of bounds of a.
   Undeﬁned behavior. This is where undeﬁned behavior (UB) comes into play. Language designers
may decide that certain behaviors are “undeﬁned,” leaving the language semantics unspeciﬁed in
such cases. The presence of UB justiﬁes more aggressive compiler optimizations. For instance, in C
the example program above is considered to have UB whenever c is a pointer outside of the region
of memory allocated for a. The language implementation does not necessarily check for this UB;
the compiler simply assumes that pointers constructed using pointer arithmetic stay in bounds of
the original allocation, and thus c could never alias with b, because b was allocated with a diﬀerent
call to malloc. Compilers only need to preserve deﬁned behavior, and so any case where UB occurs
need not be considered when performing a program transformation. In the example above, we can
perform store forwarding to have printf("%d\n", 1) instead—the only way that this program
could print anything besides 1 is if c aliases with b, which would make the store to *c UB.
   Unfortunately, this concrete memory model cannot justify such optimizations—the model is
too well deﬁned, giving a speciﬁc behavior to the program in the degenerate cases where out-of-
bounds pointer arithmetic is used to overwrite arbitrary memory locations. We shouldn’t be able
to use a pointer from one allocation to derive an alias to a separate allocation. To address this we’d
like to keep track of which pointers are allowed to access which regions of memory.

2.2 CompCert: Provenance
One way to solve the aliasing problem from the previous section is to give pointers provenance. The
provenance of a pointer determines which block in memory that pointer is allowed to access. This
provenance can be preserved throughout pointer arithmetic operations, so the pointer c should
have the same provenance as a, and thus c should only be able to modify the block of memory
associated with a, and cannot access the disjoint block of memory from the separate allocation b.
   One example of a memory model that takes provenance into account is CompCert’s [25, 26].
CompCert is a formally veriﬁed C compiler with an abstract-block-based memory model. Memory
is no longer deﬁned as a concrete array; instead memory is a map of blocks, and each allocation
creates a block with a unique id b in the memory map. Pointers can then be represented by a tuple
(b, o), where b is the block id that serves as the provenance, and o is the oﬀset into the block.
   With this model, it’s not possible for a pointer to be created that indexes into another block, as
pointer arithmetic modiﬁes only the oﬀset and block ids never change. This is good news for the
optimization in the example: c will never be able to alias with b. Unfortunately, it’s not clear how
we could handle casts between pointers and integers in this model because there is no longer a
physical address for a block! Furthermore, because there is no physical memory layout, it is not
clear how to implement ﬁnite memory in this case (one could limit the total size of the allocations,
but without a physical layout of memory, it is diﬃcult to take fragmentation into account).

2.3 Bringing Back Casting
There have been a couple of proposals for how to handle pointer–integer casting. The main two
points of comparison are the quasi-concrete [17] and twin allocation [21] memory models.
2.3.1 Quasi-concrete memory model. The quasi-concrete memory model is an extension of Comp-
Cert’s abstract-block style of memory models. The memory is split into two parts: logical, and
concrete. The logical memory is the block/oﬀset model described in Section 2.2, and, if no pointer–
integer casts occur, the quasi-concrete memory is eﬀectively identical to this model.



©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                                           7


   To support casts, the quasi-concrete memory model glues a concrete memory on top of the
logical block model. This concrete layer represents the physical layout of the blocks in memory.
Whenever a pointer is cast to an integer, a physical block is allocated in the concrete layer, repre-
senting where the logical block is actually allocated in physical memory. Delaying the allocation
of a physical block until cast time can rule out situations where an address of a block might be
guessed4 . If the physical address of a block has never been observed through a integer cast, then a
program should not be able to guess where that block is allocated (the block exists only in logical
memory). Of course, while an actual program running on a real computer will allocate a physi-
cal address for every block immediately, the delayed allocation of physical blocks allows abstract
pointers5 to be completely isolated, such that physical addresses can never alias with them. Thus,
even in the presence of complex casting between pointers and integers, more optimizations involv-
ing purely abstract pointers are justiﬁed, as are simpler heuristics for aliasing.
   The downside of the delayed allocation of physical blocks is that pointer–integer casts have the
side eﬀect, within the semantics, of allocating a physical block in concrete memory. We cannot
erase any pointer to integer casts, even if they’re dead, which in turn further restricts other opti-
mization passes. For instance, an otherwise dead block of code or function call may need to remain
in the program, because removing a cast will change the memory layout, impacting the behavior
of the program. Removing the cast may mean the block is no longer accessible via integers cast to
pointers, and may change where other blocks are allocated in concrete memory.
   Furthermore, the story for ﬁnite memory is awkward in the quasi-concrete memory model.
We can allocate as many logical blocks as we want, but, if there are a ﬁnite number of physical
addresses, a cast from a pointer to an integer can cause an Out Of Memory (OOM) error. Ultimately,
there are still all of the problems that we have with reasoning about ﬁnite programs, but they arise
only in programs that perform pointer to integer casts.
2.3.2 Twin Allocation. Twin allocation [21] takes a diﬀerent approach to handling pointer–integer
casts, and does so while taking ﬁnite memory into account. Twin allocation gives every pointer a
physical address immediately, but uses nondeterminism to rule out address guessing. Upon alloca-
tion, this memory model actually reserves two (or more) blocks instead of just one. One block is
a “trap”, and accessing it will raise UB; the other will be used as normal 6 . The model tracks two
executions for the program nondeterministically, with the only diﬀerence between the executions
being which of the two blocks is real and which is the trap. Then, if address guessing occurs, UB
will be observed in one of the executions, as the guessed block will instead be a trap block in the
alternate execution—and in that case, the program as a whole is considered to exhibit UB.
   This model addresses some of the problems of the quasi-concrete memory model. Casts between
pointers and integers aren’t eﬀectful and can thus be erased, as every block gets a physical address
immediately. However, this model introduces some additional constraints on program transforma-
tions. Most importantly, allocations, even dead ones, cannot be removed! This issue is fundamental
to the nature of ﬁnite memory models: when performing any allocation7 in a ﬁnite model, the pro-
gram may run out of memory, and, if it is removed, the program will behave diﬀerently—it might
4 An address is “guessed” if we construct a pointer to a block without deriving it directly from the allocation. This is mostly

done via integer–pointer casts. For instance, casting an arbitrary integer to a pointer could give you an alias to any region
of memory. Aliasing is problematic for optimizations, so we want to avoid it.
5 Pointers whose physical address has never been observed via pointer–integer casts.
6 Both blocks really do need to be allocated! If we just considered two executions, one where the block is allocated at p1

and one where the block is allocated at p2, then it’s plausible for something else to be allocated in the other slot for each
of the executions, so you might not be able to swap p1 for a trapped p2.
7 Assuming the bound on memory size is not known in advance, which is the usual assumption. If the size is known, then

one could prove that some allocations will always succeed, but that poses other complications.




©2024 Copyright held by the owner/author(s).
8                                  Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


continue to execute instead of running out of memory. This situation isn’t very satisfying, though,
as programmers want the compiler to remove dead allocations! Section 3 will discuss our solution
to this seemingly impossible conundrum.
   Furthermore the twin-allocation model requires additional memory allocation to ensure that
there’s enough nondeterminism for address guessing to be detected. It should be possible for the
extra allocation to be removed at run time, as that should also yield a valid execution of the program
(the “trap” blocks can only cause UB to be raised sooner, or OOM), but it’s awkward that we have
to reason about programs with double (or more) of their actual memory usage. Section 6 of [30]
makes the observation that it should be possible to instead reserve space for the largest allocation
that the program can possibly make, instead of duplicating every allocation, which makes a slightly
diﬀerent reasoning trade-oﬀ. Using this strategy, one would have to prove that a program never
performs an allocation larger than this pre-allocated trap block in order to guarantee that addresses
are not guessed, which is an additional burden on the compiler, or on the programmer if such large
allocations would be considered UB instead.

2.4    CompCertS: A Finite Symbolic Memory Model
CompCertS [4] extends the classic CompCert memory model with symbolic values (as in [2] and
[3]), and allows for pointers to be treated as integers — our memory model takes a very similar
approach with respect to the abstract bytes stored in memory as discussed in Section 4.2.2.
   For our purposes, the most relevant aspect of CompCertS is how it handles ﬁnite memory. Com-
pCertS makes the assumption that programs do not run out of memory, and any program trans-
formation that CompCertS performs must be shown to either preserve, or decrease the amount of
memory allocated by the program. These are perfectly reasonable design decisions, but this means
that (1) to ensure correct compilation of a program, that program must be proven to not run out
of memory, (2) any program transformations must be shown to not use additional memory, and
(3) the ﬁnite memory address guessing side-channel discussed in Section 2.3.2 is present.
   The constraints introduced by (2) can be mitigated somewhat by “pre-allocating” some unused
memory that can be utilized by future program transformations, and it should also be possible to
reclaim memory that is no longer needed. Program transformations that decrease memory usage
should always be applicable (assuming the source program does not run out of memory), but trans-
formations that increase memory usage may only apply conditionally. This approach to handling
ﬁnite memory is honest and yields strong guarantees about the memory usage of the target pro-
gram, but the restrictions on which optimizations can be performed are not ideal—ideally, we want
to let our compiler hand-wave reasoning about memory altogether (in a semantically consistent
way).

3     A TWO-PHASED MEMORY MODEL
To address the limitations of the memory models described in Section 2, our proposal is to use two
phases of compilation to get the best of all worlds: an inﬁnite memory model where high-level
abstract optimizations can be performed with ease, and a ﬁnite memory model that more closely
represents the ﬁnite architecture of the compilation target. In our inﬁnite model, both allocations
and casts between pointers and integers can be removed (if they’re dead) or added at will, so the
presence of these operations doesn’t block optimizations. Nearly all optimizations should be done
under the inﬁnite semantics, as optimizations that are valid under the ﬁnite model are also valid
under the inﬁnite model. Once optimizations are performed, there is an explicit translation to the
ﬁnite model. That compilations step preserves the semantics of the original inﬁnite program, but
potentially introduces points where the program can halt early because it ran out of memory.




©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                          9


                                                           m ∈ Memory       ,    Addr ↩→ (SByte × Prov)
                                                              h ∈ Heap     ,    Addr ↩→ P (Ptr)
                     
                      mem       : Memory,
                     
                      heap
                                                                p ∈ Ptr    ,    {a : Addr; pr : Prov}
                                 : Heap,
  𝜎 ∈ Conf      ,                                             f ∈ Frame     ,    P (Ptr)
                     
                      stack     : FrameStack,
                     
                      used      : P (Prov)             fs ∈ FrameStack     ,    list Frame
                                                              pr ∈ Prov    ,    option(N)
        Fig. 2. Datatype of memory configurations, where Addr and SByte are abstract parameters
   At a high level, the design of our two-phased memory model resembles the concrete memory
models from Section 2.1 and Section 2.4. The only real diﬀerence between our inﬁnite and ﬁnite
models is the type of the pointers and the iptr type that we introduce in Section 4.2 in order
to handle pointer / integer casts appropriately. The inﬁnite model uses Coq’s big-integer Z type
for physical addresses, and the ﬁnite versions use an implementation of 64-bit integers (limiting
the size of memory to the 64-bit address space). The iptr type matches the type of the physical
addresses in the respective memory model.
   The semantics for our memory model is nondeterministic, allowing us to accurately model the
behavior of the program under the diﬀerent memory layouts that arise from nondeterministic allo-
cations. This nondeterminism can also be used to prevent address guessing in the inﬁnite memory
model, as there will always be an execution where a guessed block could be allocated somewhere
else instead (akin to swapping blocks in the twin-allocation model, except no pre-allocation of
these “trap blocks” is necessary because inﬁnite memory means we always have unallocated space
to swap blocks to).

3.1   Notations
We write m : 𝐴 ↩→ 𝐵 when m is a partial map from 𝐴 to 𝐵. We write m[𝑎] = 𝑏 to assert that 𝑎
belongs to the domain of m and maps to 𝑏, m{a := b} for updating a in m with value b, possibly
extending the domain of 𝑚 in the process, and m \ a to remove a from the domain of m. When r is
an element of a record type, we write r.f for the content of its ﬁeld f . We use the notation P (𝐴)
for the set of all subsets of elements of 𝐴. Given a list, l, we write |l| for its length, l [i] to access its
i-th element, assuming it is within bounds, and coerce it into a set implicitly when needed. Finally,
we conﬂate equality and extensional equality over ﬁnite maps.

3.2   Memory Configurations
Figure 2 describes the datatype Conf of memory conﬁgurations. It is parameterized by two types:
Addr, the representation of concrete addresses, and SByte, the representation of (symbolic) bytes,
in memory. The former is straightforward: addresses are represented as unbounded integers at
the inﬁnite level, and bounded integers at the ﬁnite level—we assume an operation + : Addr →
N → OOM + Addr, which performs arithmetic on addresses returning OOM in the case where an
overﬂow occurs in the ﬁnite model. We will leave the representation of symbolic bytes abstract,
as their implementation is language dependent, but we will give a full description of them in our
LLVM semantics in Section 4.2.2; we invite the reader to think of them as concrete bytes until then.
   A conﬁguration 𝜎 has four ﬁelds. The memory itself, 𝜎.mem, is a ﬁnite map from addresses
to bytes with an associated provenance. The provenance is an optional natural number, where
the None constructor is used as a wildcard during integer–pointer casts. We introduce notations
to access the memory via pointers, i.e., addresses tagged with provenance information. We write
𝑚[p] =¤ b for the partial allowed SByte lookup operation: it asserts both that p.a is in the domain
of m, and performs a provenance check by ensuring that it maps to the pair (b, p.pr). We simply
write p ∈¤ m as a shortcut to ∃b, m[p] =¤ b to state that a pointer is accessible in memory. Conversely,



©2024 Copyright held by the owner/author(s).
10                                  Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


p ∉¤ m states that a pointer cannot be accessed in memory, either because p.a is not in the domain
of m, or because the associated provenance is diﬀerent from p.pr. Finally, we write m1 ≡\→ −p m2 to
express that memories m1 and m2 agree on content and provenance at all addresses except those
in the list of pointers →
                        −p :

                             ′          →− ′                     ′
                                                                    ¤ b ↔ m2 [p′ ] =¤ b)
                   −p m2 , ∀p , b, (∀p ∈ p , p .a ≠ p.a) → (m1 [p ] =
              m1 ≡\→

   The heap 𝜎.heap tracks information about heap allocation units. Via malloc, a contiguous region
of memory can be allocated in blocks of sequentially consecutive pointers: p1, . . . , p𝑛 . Each p𝑖 : Ptr
in the block is associated with its root address p1 .a, which is the address returned by the allocation
operation. Freeing the root deallocates the whole block. (Freeing a non-root address will be unde-
ﬁned behavior.) The stack, 𝜎.stack, keeps track of the call stack by maintaining a stack of frames,
where each frame consists of a list of pointers. Fresh addresses, allocated via alloca, are added
to the top frame of the stack, referred to as 𝜎.stack.top. Finally, a conﬁguration keeps track of a
set of used provenances, 𝜎.used in order to ensure that fresh provenances can be assigned to new
allocations.

3.3     The Specification Monad
Memory models for compiler IRs are naturally nondeterministic semantic objects: they must de-
scribe all legal implementations architectures may commit to, and allocations, in particular, are
left unconstrained, leading to nondeterminism. We provide a speciﬁcation for each operation via
a speciﬁcation monad:
     MemSpec(𝑋 ) , Conf → P (Result (Conf × 𝑋 )) where Result (𝐴) , UB + OOM + FAIL + ok(𝐴)
   MemSpec(𝑋 ) is stateful and nondeterministic, relating initial conﬁgurations to a set of possible
conﬁgurations that could result from executing a memory operation. These sets are speciﬁed in
a propositional way; we describe them either via inference rules, or by composing them via the
usual ret and bind monadic operations. Finally, the result type, Result (), allows us to characterize
the four possible acceptable behaviors of an operation. We write (c 𝜎) ∋ beh to state that beh is a
valid behavior of a memory speciﬁcation c at initial conﬁguration 𝜎.
   An operation may simply succeed, yielding ok(𝜎, x), returning a new conﬁguration 𝜎 and a
resulting value x. It may also raise one of three exceptional behaviors. The ﬁrst is Undeﬁned Be-
havior, UB, which arises from run-time situations that invalidate assumptions the compiler makes
to justify optimizations; semantically, these are modeled as computations that can be reﬁned into
anything. The second is an out of memory exception, OOM. This behavior captures all the situa-
tions in which the computation may preemptively halt as a consequence of the representation of
addresses; semantically it is modeled as a behavior that reﬁnes anything. Lastly, operations may
FAIL, representing cases in our semantics that we intend to be statically checked and ruled out. This
exception also corresponds to language features that have not been implemented in our model. In
the remainder of the paper, we therefore elide this case by providing partial speciﬁcations instead.
A key distinction between failure and UB is that failure is not “time-traveling” in our semantics.
   The monadic speciﬁcation is particularly useful for maintaining very similar structures between
the memory model and the executable interpreter (See Section 6), which simpliﬁes maintenance
and the proof that the executable implementations of the memory model respect the speciﬁcations.

3.4     Low level memory operations
Signatures of the low level primitives interacting with the memory model are described in Figure 3.
The operations are reads and writes of single bytes, allocations of blocks (a contiguous sequence



©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                          11


            read𝑏 (p : Ptr)     :     MemSpec(SByte)                →
                                                                    −
                                                           alloca ( b : list SByte)     :   MemSpec(Ptr)
write𝑏 (p : Ptr) (b : SByte)    :     MemSpec(unit)                 →
                                                                    −
                      pushf     :     MemSpec(unit)        malloc ( b : list SByte)     :   MemSpec(Ptr)
                       popf     :     MemSpec(unit)                   free (p : Ptr)    :   MemSpec(unit)
                                    Fig. 3. Memory model: low level operations


             p ∉¤ 𝜎.mem                        𝜎.mem[p] =¤ b                         p ∉¤ 𝜎.mem
         (read𝑏 p 𝜎) ∋ UB                  (read𝑏 p 𝜎) ∋ ok(𝜎, b)                (write𝑏 p b 𝜎) ∋ UB

                     𝜎1 .heap = 𝜎2 .heap 𝜎1 .stack = 𝜎2 .stack 𝜎1 .used = 𝜎2 .used
                      p ∈¤ 𝜎1 .mem 𝜎2 .mem[p] =¤ b         𝜎1 .mem ≡\{p} 𝜎2 .mem
                                          (write𝑏 p b 𝜎1 ) ∋ ok(𝜎2, tt)
                        Fig. 4. Memory model: byte-level read and write operations


                         p ∉ 𝜎.used                               ∀i, 0 ≤ i < n, 𝜎.mem[a + i] = None
      (fresh 𝜎) ∋ ok(𝜎 {used := {p} ∪ 𝜎.used}, p)                        (find_bk n 𝜎) ∋ ok(𝜎, a)

         𝜎1 .heap = 𝜎2 .heap 𝜎1 .used = 𝜎2 .used 𝜎2 .stack = 𝜎1 .stack.top ⊎ →
                                                                             −p :: 𝜎 .stack.𝑡𝑙
                                                                                    1
            →−     →−                →−             →
                                                    −         →−
           | p | = | b | ∀i, 0 ≤ i < | p |, 𝜎2 .mem[ p [i]] =¤ b [i] 𝜎1 .mem ≡\→−p 𝜎2 .mem

                                    (alloca_post 𝑏𝑠 𝑝𝑡𝑟𝑠 𝑚 1 ) ∋ ok(𝑚 2, tt)

             𝜎1 .stack = 𝜎2 .stack 𝜎1 .used = 𝜎2 .used 𝜎2 .heap = 𝜎1 .heap{→
                                                                           −p [0].a := →
                                                                                       −p }
                     →
                     −                                       →−
            |→
             −p | = | b | ∀0 ≤ i < |→
                                    −p |, 𝜎 .mem[→
                                               2
                                                   −p [i]] =¤ b [i] 𝜎 .mem ≡ →
                                                                             1  − 𝜎 .mem
                                                                                       \p   2
                                                 →− −
                                     (malloc_post b →
                                                    p 𝜎1 ) ∋ ok(𝜎2, tt)

  𝜎1 .stack = 𝜎2 .stack 𝜎1 .used = 𝜎2 .used 𝜎1 .heap [p.a] = Some →
                                                                  −p 𝜎 .heap = 𝜎 .heap \ {p.a}
                                                                        2          1
                   →
                   −
            ∀p′ ∈ p , (p′ ∈¤ 𝜎1 .mem ∧ 𝜎2 .mem[p′ .a] = 𝑁𝑜𝑛𝑒)      𝜎1 .mem ≡\→
                                                                             −p 𝜎2 .mem

                                            (free p 𝜎1 ) ∋ ok(𝜎2 , tt)
                          Fig. 5. Memory model: memory management primitives


       𝜎1 .heap = 𝜎2 .heap     𝜎1 .used = 𝜎2 .used     𝜎1 .mem = 𝜎2 .mem 𝜎2 .stack = ∅ :: 𝜎1 .stack
                                            (pushf 𝜎1 ) ∋ ok(𝜎2, tt)

                  𝜎1 .heap = 𝜎2 .heap 𝜎1 .used = 𝜎2 .used 𝜎1 .stack = →
                                                                      −p :: 𝜎 .stack
                                                                             2
                   →−
               ∀p ∈ p , (p ∈¤ 𝜎1 .mem ∧ 𝜎2 .mem[p.a] = 𝑁𝑜𝑛𝑒) 𝜎1 .mem ≡\→     −p 𝜎2 .mem

                                             (popf 𝜎1 ) ∋ ok(𝜎2, tt)
                               Fig. 6. Memory model: frame stack management


of bytes) on the stack and heap, operations for freeing heap allocated blocks, pushing stack frames,
and popping the most recent stack frame in order to free stack allocated blocks.



©2024 Copyright held by the owner/author(s).
12                                        Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


   Out Of Memory behavior. Perhaps surprisingly we always allow operations to halt preemptively
with an out-of-memory behavior. One of our goals was for the speciﬁcations to encompass a large
number of possible implementations for memory, and we’ve seen instances of memory models that
might “run out of memory” in counter-intuitive situations (for instance a quasi-concrete memory
model with a ﬁnite concrete memory may run out of memory when a concrete block is allocated for
a pointer–integer cast), as such we’ve been very lenient with allowing out-of-memory behaviors
throughout or semantics. One could tighten the speciﬁcations if desired, though when comparing
the inﬁnite and ﬁnite memory models in Section 3.5 our reﬁnement relations allow for out-of-
memory anywhere in the ﬁnite memory model anyway. Since out-of-memory is omnipresent, we
work under the convention that all speciﬁcations 𝑐 : MemSpec(𝑋 ) may run out of memory, i.e.,
(𝑐 𝑚) ∋ OOM is satisﬁed for any initial memory 𝑚. This makes OOM a kind of reﬁnement dual
to UB. While UB can always be reﬁned into any computation, any computation may be reﬁned by
OOM, as we purposefully do not want to reason about programs that run out of memory.
   Reading and writing bytes (Figure 4). The operation read𝑏 p 𝜎 speciﬁes the possible behaviors
when dereferencing a pointer in memory. Dereferencing boils down to looking up the memory,
with the additional provenance check introduced in Section 3.2. If the lookup fails, or is illegal,
UB may be raised. Writing a byte b to memory 𝜎1 .mem at a pointer p may trigger UB in similar
cases to reading. A successful write must furthermore specify the resulting conﬁguration 𝜎2 —the
statement is made slightly more complex to account for provenance, but hides no surprise. Only
the memory component of the conﬁguration is modiﬁed. A pointer p accessible in 𝜎1 .mem will
be remapped to the byte b in 𝜎2 .mem. Finally, all addresses distinct from p.a are unchanged in
memory.
   Memory management (Figure 5). Specifying allocation is a more involved and less atomic task, so
we leverage the speciﬁcation monad to describe it in a more programmatic style. Utility speciﬁca-
tions help generate a fresh provenance pr (fresh), and retrieve an available contiguous sequence
of n addresses in memory (find_bk n). 8 Note that find_bk uses 𝑎 + 𝑖 to compute contiguous
addresses, should this overﬂow in the ﬁnite model the allowed behavior will only be OOM.
   Stack and heap allocations of a list of bytes are speciﬁed very similarly, retrieving a fresh prove-
nance, an available range of addresses, constraining the resulting memory, and ﬁnally returning
the ﬁrst allocated address:
         →
         −                                                               →
                                                                         −
 alloca ( b : list SByte) : MemSpec(Ptr) :=                      malloc ( b : list SByte) : MemSpec(Ptr) :=
    pr ← fresh;;                                                    pr ← fresh;;
                    →
                    −                                                               →
                                                                                    −
    a ← find_bk (| b |);;                                           a ← find_bk (| b |);;
                  →
                  −                      →−                                       →
                                                                                  −                      →−
    alloca_post b [(a, pr), . . . , (a + | b | − 1, pr)] ;;         malloc_post b [(a, pr), . . . , (a + | b | − 1, pr)] ;;
    ret (a, pr)                                                     ret (a, pr)
These speciﬁcations only diﬀer in how the conﬁgurations are constrained as depicted on Figure 5.
                                    →
                                    − −
For stack allocation, alloca_post b →   p ensures that (1) the new pointers are added to the current
stack frame, (2) the addresses are written with the corresponding bytes, all sharing the provenance
                                                                                  →− −
pr, and (3) nothing else in memory is altered. For heap allocation, malloc_post b →   p enforces (2)
and (3) similarly, but, instead of manipulating the stack, it ensures that the returned address is a
root in the heap associated with the set of newly allocated pointers.
   Given a pointer p, free p 𝜎1 ensures that p.a is a valid root in 𝜎1 .mem, associated with a set of
pointers →
         −p accessible in 𝜎 .mem. Under this assumption, it simply reclaims the pointers and severs
                            1


8 In line with LLVM, allocating no bytes (i.e. an empty list) may return any address. Its fresh provenance, which no data is

equipped with, will, however, ensure we cannot do anything with this address without triggering UB.




©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                            13


 𝜎 inf & 𝜎 ﬁn     := 𝜎 inf = ⌈𝜎 ﬁn ⌉                                                    Inﬁnite to ﬁnite reﬁnement

                        
                        
                         mem        = {𝑧 ↦→ ( ⌈𝑏⌉, 𝑝) | 𝜎 ﬁn .mem[𝑧] = (𝑏, 𝑝)}
                        
                         heap
                                    = {𝑧 ↦→ map ⌈−⌉ blk | 𝜎 ﬁn .heap [𝑧] = blk}
     ⌈𝜎 ﬁn ⌉      :=                                                                    Conﬁguration Lifting
                        
                         stack      = map (𝜆blk · map ⌈−⌉blk) 𝜎 ﬁn .stack
                        
                         used
                                    = 𝜎 ﬁn .used
                  ⌈p⌉     := (int_to_Z(p.a), p.pr)
                  ⌈𝑏⌉     := lift_sbyte(𝑏) (lifting symbolic bytes, language speciﬁc)
Fig. 7. Infinite-to-finite refinement defined by lifting of finite memory configurations into infinite memory
configuration. Here, lift_sbyte is a language-specific lifting of finite SByteﬁn into SByteinf . We omit implicit
int_to_Z() casts when the integer is known to be within finite bounds.


p.a from the heap. Though not shown in the Figure, UB occurs in the complementary cases—when
the pointer is not a root in the heap or if the block was not actually allocated in memory.
  Stack management (Fig 6). Pushing a new frame, pushf, is trivial, simply adding the emptyset
on top of the stack. The speciﬁcation of popf is very close to free: we ensure all pointers in the
top frame are accessible in the original memory, reclaim them, and pop the stack.

3.5 Relating the Infinite and Finite Memory Models
We now consider two instances of the memory model, based on two representations of addresses:
an inﬁnite memory model with unbounded integers, and a ﬁnite one with 64-bit integers. We will
distinguish between these models with inf and ﬁn superscripts for the inﬁnite and ﬁnite memory
models respectively.
   Our overarching goal is to be able to reason about programs in the inﬁnite memory model,
performing program transformations under the inﬁnite semantics. We will then convert these
inﬁnite memory programs to ﬁnite memory programs that will eventually be compiled to native
assembly code for a concrete architecture. In order to ensure that this process is sound, we must
relate the behavior of memory operations under the inﬁnite model with the behavior of the same
operations under the ﬁnite model.
   The rough idea is to consider the execution of programs under the inﬁnite model when their
allocations happen to ﬁt within the ﬁnite memory model’s range of memory addresses—executions
that don’t ﬁt will exhibit OOM behavior. We then ensure that operations on these ﬁnite memory
slices agree between the inﬁnite and ﬁnite memory models. Essentially, the ﬁnite memory model
should be able to simulate the inﬁnite memory model, as long as all the addresses stay in bounds!
3.5.1 Relating Configurations. We start by relating conﬁgurations at both levels. As described
in Figure 7, a ﬁnite 𝜎 ﬁn : Conf ﬁn is a reﬁnement of an inﬁnite 𝜎 inf , written 𝜎 inf & 𝜎 ﬁn , when
𝜎 inf coincides with the lifting ⌈𝜎 ﬁn ⌉. Lifting a Conf ﬁn is fairly straightforward, both domains of
conﬁgurations having similar concrete representations. The lifting therefore simply maps over the
structure the trivial injection of ﬁnite addresses into Z, as well as the lifting of symbolic bytes.9
3.5.2 Relating Operations. We can now capture the intuitive expected behavior of the memory
operations: if the memory conﬁguration can ﬁt in the ﬁnite representation, then the same behav-
ior can be observed. In practice, we prove a reﬁnement lemma for each low-level operation. For
instance, in the case of reads:
9We delay this description to Section 4.2.2.




©2024 Copyright held by the owner/author(s).
14                                        Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


   Lemma 3.1 (read_byte_spec refinement).
   • 𝜎 inf & 𝜎 ﬁn , and                                                   inf    ﬁn
If • ptr inf = ⌈ptr ﬁn ⌉, and                    then ∃ 𝑏 ﬁn such that • 𝑏 = ⌈𝑏 ﬁn⌉, and
                                                                       • (read𝑏 𝜎 ptr ﬁn ) ∋ ok(𝜎 ﬁn , 𝑏 ﬁn ).
   • (read𝑏 𝜎 inf ptr inf ) ∋ ok(𝜎 inf , 𝑏 inf )

     The lemmas for the other operations are similar in shape, so we omit them for conciseness.

4     INTEGRATING THE MEMORY MODEL INTO AN LLVM LIKE LANGUAGE
The inﬁnite and ﬁnite models above provide general semantics that are parameterized by addresses
and symbolic bytes, as these parameters could vary depending on the programming language. To
ensure that it is suﬃciently expressive for use in practice, we have instantiated the framework in
the context of an existing formal semantics, VIR [38]. VIR aims to be a speciﬁcation for a large,
practically applicable subset of (sequential) LLVM IR. It supports a rich, C-like structured memory
model, including integer–pointer casts; it also includes undef and poison values that interact non-
trivially with the memory model speciﬁcation because they aﬀect the notion of UB. The prior VIR
memory models were based on the CompCert and quasi-concrete semantics, and so they suﬀered
from the deﬁciencies with respect to optimization correctness mentioned in Section 2. The new
memory model rectiﬁes those problems and is also more faithful to LLVM IR’s intended semantics
with respect to undef. This Section describes the VIR instantiation of the framework and, along the
way, addresses some challenges of formalizing LLVM IR semantics. As in the general framework,
this instantiation yields both an inﬁnite memory and a ﬁnite memory version of the VIR semantics.
Most of the development is parametric with respect to that choice, but we diﬀerentiate them as
VIRinf and VIRﬁn where necessary.

4.1 Layered interpreters
VIR is structured as a series of layered in-
                                                                                   VIR
terpreters, as shown in Figure 8, each of
which speciﬁes some aspects of the LLVM
                                                                              itree 𝐸 0 V
IR semantics. These interpreters are built                                      intrinsics
on top of interaction trees [35, 37], which
                                                                              itree 𝐸 1 V
are a Coq datatype of potentially inﬁnite                                 global environment
trees (used to model diverging programs)
                                                                       stateT𝐸𝑛𝑣𝐺 itree 𝐸 2 V
whose nodes are uninterpreted events, in-                                  local environment
dicated by 𝐸 0 –𝐸 5 in the Figure. Each layer                        stateT𝐸𝑛𝑣𝐿∗𝐸𝑛𝑣𝐺 itree 𝐸 3 V
handles some subset of the events, deﬁn-                          memory model spec exec memory
ing their semantics, and leaving the rest stateT𝑀𝑒𝑚∗𝐸𝑛𝑣𝐿∗𝐸𝑛𝑣𝐺 itree 𝐸4 V → P               stateT𝑀𝑒𝑚∗𝐸𝑛𝑣𝐿∗𝐸𝑛𝑣𝐺 itree 𝐸 4 V
for later layers to handle.                             model undef                                  exec undef
   For the purposes of this paper, the most stateT𝑀𝑒𝑚∗𝐸𝑛𝑣𝐿∗𝐸𝑛𝑣𝐺 itree 𝐸5 V → P             stateT𝑀𝑒𝑚∗𝐸𝑛𝑣𝐿∗𝐸𝑛𝑣𝐺 itree 𝐸 5 V
important parts of the interpretation stack               model UB
are the handlers for memory events, nonde- stateT𝑀𝑒𝑚∗𝐸𝑛𝑣𝐿∗𝐸𝑛𝑣𝐺 itree 𝐸5 V → P
terminism, undeﬁned behavior, and out-of-               model OOM
memory exceptions. The memory events, stateT𝑀𝑒𝑚∗𝐸𝑛𝑣𝐿∗𝐸𝑛𝑣𝐺 itree 𝐸5 V → P
M, correspond to LLVM IR operations
that interact with the memory model and Fig. 8. Levels of interpretation. Each box shows the type of
each of those events is parameterized by the semantic definitions at that layer. Arrows are labeled
appropriate input values and a return type with the events they define.
Vor V𝑢 (indicated as a superscript), as




©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                                     15


shown below—these types, describing dynamic values, are explained in the next Subsection. The
other kinds of events are similarly annotated.10

     Memory model interaction events                                                   Undeﬁned Behavior event
     M , MPush ( ) | MPop ( ) | Load V𝑢 (𝜏, 𝑎) | Store ( ) (𝑎, 𝑢𝑣)                     U , UB ∅
         | Alloca V (𝜏)
     Nondeterminism events                                                             OOM event
      P , Pick V (𝑢𝑣) | PickUnique V (𝑢𝑣) | PickNonPoison V (𝑢𝑣)                       O , O∅
   With respect to the memory model, the main work of a VIR semantics is to implement a handler
for the M events in terms of the primitive operations described in Section 3. That handler is
plugged into the stack of Figure 8 to interpret M ∈ 𝐸 3 into stateful operations that manipulate
the memory. As shown in the left-hand-path of the interpretation stack, the speciﬁcation of the
memory model is deﬁned propositionally in Coq to account for the nondeterminism of possible
implementations, including nondeterminism introduced by the memory model. The right-hand
path implements the executable version of the semantics. On the speciﬁcation side, the handlers
for U, P and O events interact with the notion of reﬁnement for the behaviors of VIR programs
(see Section 4.4). There are no equivalent handlers for U and O on the executable side, because
the OCaml framework for executing VIR ITrees simply raises an exception when those events are
encountered.
   If 𝑝 is a VIR program, we write, e.g., J𝑝K3 to mean interpretation down to the 3𝑟𝑑 layer (i.e., just
before the split). We write J𝑝KVIR for the “fully interpreted” semantics of 𝑝, i.e., at the bottom of
the left branch, and we write interpret 𝑝 for the executable version, at the bottom right branch.
That the executable semantics is a valid implementation of the speciﬁcation is one of the main
theorems about the VIR development (see Theorem 6.1).

4.2 VIR Values
4.2.1 Dynamic values and iptr. The semantics of VIR relies upon the domain Vof dynamic values
that the language can manipulate. The core of these dynamic values are the deﬁned values.
               𝑑𝑣 ∈ V ::= none | 𝑎 | [list V] | 𝑖 1 | 𝑖 8 | 𝑖 16 | 𝑖 32 | 𝑖 64 | 𝑖 ptr | poison𝜏
The void value, none, is a placeholder for operations with no meaningful return values. Memory
addresses (𝑎), of type Addr, are implemented either as positive integers, Addr inf = Z, or 64-bit
values 𝐴𝑑𝑑𝑟 ﬁn = i64, depending on whether we are instantiating the inﬁnite or ﬁnite memory
model. VIR supports all of LLVM IR’s structured values, including records, but here we present
only arrays, noted as [𝑑𝑣 1, . . . , 𝑑𝑣 𝑛 ].
   VIR supports i1, i8, i16, i32 and i64-bit integers11 ranged over by 𝑖 1 , 𝑖 8 , etc., but it also includes
integers of type iptr, which are in bijection with memory addresses, 12 and ranged over by 𝑖 ptr .
iptr has the same cardinality as the Addr type, i.e., iptrinf , Z and iptrﬁn , i64. The iptr type
acts mostly like the other integer types, supporting all of the same instructions, which allows for
programs to perform arbitrary arithmetic on physical addresses without forcing a cast to a type
of a ﬁxed ﬁnite size. Because iptr has the same cardinality as Addr, pointer–integer casts can
eﬀectively be pure no-ops, allowing these casts to be removed to make way for other optimizations,
10 Note that the superscript ∅ for UB ∅ and O ∅ means that these events do not return any value; they simply terminate the

computation. The PickUniqueV (𝑢𝑣) and PickNonPoison V (𝑢𝑣) events technically return constrained types that guaran-
tee uniqueness or a non-poison value, respectively, but we elide those details here.
11We use CompCert’s ﬁnite integers in our development. VIR also supports ﬂoating-point values (omitted here for

simplicity).
12 The iptr type is missing from the LLVM IR, but there is precedent for it in C, via intptr_t, uintptr_t and size_t [13]




©2024 Copyright held by the owner/author(s).
16                                        Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


and ensuring a round-trip property where a pointer cast to an integer and back yields the same
pointer13 . In order to preserve this round-trip property for casts, arithmetic on iptr values in
VIRﬁn may provoke OOM, as discussed in Section 4.3.3.
  VIR also includes poisoned values (poison) representing a deferred undeﬁned behavior [22].
Deferred UB is instrumental for aggressive optimizations, but a semantic subtlety. The poison
value is a tainting mark: it propagates to all values that depend on it, so equivalences such as
poison + poison ≡ 2 ∗ poison ≡ poison hold true.
4.2.2 Undef Values and Symbolic Bytes. LLVM represents uninitialized memory through unde-
ﬁned values, which represent the set of possible values of a given type, and operations on them
manipulate a those sets. Reasoning about undeﬁned values is subtle; each time an undef value is
used within an LLVM program, it may take on a diﬀerent concrete value. For instance, undefi64 +
undefi64 ≡ undefi64 , whereas undefi64 + undefi64 . 2 ∗ undefi64 , because the value on the right
hand side of the equation cannot be an odd number.
   In VIR, “uvalues” or under-deﬁned values, written uv : V𝑢 , model these sets. They are given by:

                     uv ∈ V𝑢 ::= ↑ V | [list V𝑢 ] | undef𝜏 | op V𝑢 V𝑢 | [list SB]𝜏
                     sb ∈ SB ::= sbyte𝜏 (𝑢𝑣, 𝑖, 𝑠𝑖𝑑)
   Under-deﬁned values include deﬁned (i.e. concrete) values—we write ↑ for the corresponding
injection—as well as arrays of uvalues. They also include undef𝜏 , which stands for the set of all
possible concrete values of the type 𝜏 (we omit 𝜏 when it is unimportant). V𝑢 also includes “delayed”
operations, where op ranges over VIR’s arithmetic, bit-logic, and other computation primitives.
Such a uvalue lifts the set semantics of undef to nondeterministic computations, as we explain
below. The uvalues also contain (type-annotated) concatenations of symbolic bytes [4], sb : SB,
explained next.
   Serializing under-deﬁned values. Values in VIR is stored to memory as list of bytes. An undeﬁned
value is serialized as symbolic bytes, given by the type SB. A sbyte𝜏 (𝑢𝑣, 𝑖, 𝑠𝑖𝑑) represents the 𝑖 𝑡ℎ
byte of the value 𝑢𝑣 with a store-ID 𝑠𝑖𝑑, whereas [list SB]𝜏 concatenates a series of symbolic
bytes into a under-deﬁned value of type 𝜏.
   To enable optimizations like store-forwarding, the semantics must precisely preserve nondeter-
minism when serializing and deserializing under-deﬁned values to and from bytes. For example,
the event handler for Store serializes a 𝑢𝑣 ∈ V𝑢 into an array of symbolic bytes matching the size
of the type (written |𝜏 |), with each byte containing the appropriate index into the under-deﬁned
value. This serialization operation is deﬁned as:
                    serialize(𝑢𝑣, 𝜏)       =   𝑠𝑖𝑑 ← fresh_sid; ;
                                               ret [sbyte𝜏 (𝑢𝑣, 0, 𝑠𝑖𝑑), . . . , sbyte𝜏 (𝑢𝑣, |𝜏 |, 𝑠𝑖𝑑)]𝜏
Each of these symbolic bytes contains that same “store id” (𝑠𝑖𝑑), which is uniquely generated for
every Store event, to preserve “entangled” undef values within the semantics. This 𝑠𝑖𝑑 is assigned
to the serialized bytes and it is used to prevent the introduction of too much nondeterminism
when reading bytes written by multiple stores. For example, the program in Figure 9 illustrates
the scenario in which the ﬁrst two bytes and ﬁnal two bytes of z are entangled together, so there
are only two possible values for each of these two byte chunks. Note that, if two symbolic bytes
13 Note that there are concerns about provenance for such casts that we do not tackle in this paper [24]. Our implementation

does not track provenance through integers, so our integer–pointer casts will always yield a pointer with a wildcard
provenance, which is safe, but can limit optimizations in rare cases (see the discussion in [30]). This provenance tracking
is largely orthogonal to the design of our memory model, however, our memory model can be integrated with a language
regardless of whether it tracks provenance through integer computations.




©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                                              17


%x = i16 select i1 undef, i16 0x1234, i16 0x0000
%y = i16 select i1 undef, i16 0x5678, i16 0x0000
store i16 %x, ptr %ptr
store i16 %y, ptr (inttoptr (add iptr (ptrtoint %ptr) 2)
%z = load i32, ptr %ptr
Fig. 9. Entangled bytes. Here the select instruction chooses between two values nondeterministically due
to undef, but the load should read (assuming big-endianess for simplicity) one of 0x00000000, 0x00005678,
0x12340000, or 0x12345678, but never something like 0x00345600.
have the same 𝑠𝑖𝑑, they must have come from the same store, and thus agree on their underlying
𝑢𝑣 too.
  Conversely, the handler for the Load instruction deserializes the symbolic bytes:
 deserialize ([𝑠𝑏 1 , . . . , 𝑠𝑏𝑛 ]𝜏 , 𝜏 ′ ) =
 if 𝜏 = 𝜏 ′ ∧ [𝑠𝑏 1 , . . . , 𝑠𝑏𝑛 ]𝜏 = [sbyte𝜏 (𝑢𝑣, 0, 𝑠𝑖𝑑), . . . , sbyte𝜏 (𝑢𝑣, |𝜏 |, 𝑠𝑖𝑑)]𝜏 then 𝑢𝑣 else [𝑠𝑏 1, . . . , 𝑠𝑏𝑛 ]𝜏 ′
In the simple case where the value is loaded with the same type, the deserialization for Load can
simply extract the original 𝑢𝑣 14 (a property which makes store forwarding optimizations easy
to justify). In more complex cases, where bytes are read at a diﬀerent type from what they are
stored at (possibly reading a portion of the bytes from diﬀerent under-deﬁned values) the resulting
under-deﬁned value is left as the concatenation of symbolic bytes but with the updated type—their
concrete bit patterns will be resolved via “concretization,” as explained next.

4.3    Concretization: Refinement and Evaluation of LLVM Values
As we saw above, an under-deﬁned value 𝑢𝑣 denotes a set of “concrete” dynamic values—that is,
it is a speciﬁcation of the set of allowed bit patterns a compliant implementation can use to reﬁne
𝑢𝑣. We write J−K𝐶 : V𝑢 → P (Result (V)) to denote the (monadic) function that computes a set of
concretizations of 𝑢𝑣. We write 𝑑𝑣 ∈ J𝑢𝑣K𝐶 , deﬁned as J𝑢𝑣K𝐶 ∋ ok(𝑑𝑣) to indicate that (concrete)
dynamic value 𝑑𝑣 is a legal reﬁnement of 𝑢𝑣. The concretization function is implemented in a
similar fashion to the prior VIR semantics [38]. It essentially implements an interpreter for all of
the computational instructions “lifting” them to work on sets of values. One important base case is
that undef𝜏 concretizes to the set of all legal values of type 𝜏, that is: Jundef𝜏 K𝐶 = {𝑑𝑣 |𝑑𝑣 : 𝜏, 𝑑𝑣 ≠
poison}. For example, we have 2 ∈ Jmul i64 2, i64 1K𝐶 and also 2 ∈ Jmul i64 1, undefi64 K𝐶 but
2 ∉ Jmul i64 3, undefi64 K𝐶 . As you can see, due to the presence of arithmetic (and other non-
trivial) LLVM IR operations, and the fact that under-deﬁned values include ordinary values as a
special case, the reﬁnement relationship acts as an evaluation relation—in the case that 𝑢𝑣 has no
occurrences of undef (i.e., it is deﬁned), then 𝑑𝑣 ∈ J𝑢𝑣K𝐶 simply means that 𝑢𝑣 evaluates to 𝑑𝑣
according to the ordinary rules of LLVM IR computations, as in the ﬁrst example above.
    Note that concretization can fail with UB (in case of, for example, division by 0) or with OOM
(when working with iptr values, as described below).
4.3.1 Concretizing symbolic bytes. New to this work is the treatment of symbolic bytes. Recall
that symbolic bytes represent byte-sized fragments of (possibly) under-deﬁned values and that a
Load event might read a sequence of such bytes that were written by (several) diﬀerent Stores.
Series of symbolic bytes are concretized as shown below:
              J[sbyte𝜏1 (𝑢𝑣 1 , 0, 𝑠𝑖𝑑 1 ), . . . , sbyte𝜏𝑛 (𝑢𝑣 𝑛 , 𝑛, 𝑠𝑖𝑑𝑛 )]𝜏 K𝐶 =
                𝑑𝑣 0 ← J𝑢𝑣 0 K𝐶 ;; . . . ;; 𝑑𝑣 𝑛 ← J𝑢𝑣 𝑛 K𝐶 ;;
                {ok(bitcast𝜏 (𝑑𝑣 1 [1]𝑑𝑣 2 [2] . . . 𝑑𝑣 𝑛 [𝑛])) | ∀𝑗𝑘, 𝑠𝑖𝑑 𝑗 = 𝑠𝑖𝑑𝑘 → 𝑑𝑣 𝑗 = 𝑑𝑣 𝑘 }
14 There is a corner case for types where |𝜏 | = 0 (such as an array of length zero); in that case the correct 𝑢𝑣 is uniquely

determined by 𝜏.




©2024 Copyright held by the owner/author(s).
18                                   Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


This works by recursively concretizing the 𝑢𝑣 𝑖 ’s, each of which yields a set of concrete dynamic
values J𝑢𝑣 𝑖 K𝐶 (or an error, in which case the whole concretization is an error). Then, from each
𝑑𝑣 𝑖 ∈ J𝑢𝑣 𝑖 K𝐶 we can extract the (concrete) 𝑖 𝑡ℎ byte, written as 𝑑𝑣 𝑖 [𝑖]. The resulting set of concrete
values is then obtained by concatenating the individual bytes combinatorially; however, if two
symbolic bytes share a 𝑠𝑖𝑑 (and hence come from the same store) they are “entangled” and must
be concretized in the same way.
   The resulting sequence of bytes is converted to a dynamic value of type 𝜏 by the bitcast𝜏 (−)
operation. It might need to truncate or pad the sequence, depending on the size of values of type
𝜏 and the number, 𝑛, of available bytes. This bitcast operation is, ultimately, what allows the
conversion between values of distinct types. For instance, it could convert an array value of type
[8 × i8] into a value of type i64, even though such values have diﬀerent representations in the
semantics. Altogether, this treatment of symbolic bytes properly ensures “entanglement” of values
as illustrated in Figure 9.
4.3.2 Concretizing iptrinf values. For the inﬁnite memory model, in which iptr is taken to be
(unbounded) integers, concretization works in essentially the same fashion as the other integer
types. This is the easy case, because in VIRinf iptr values are just Z values, so no overﬂow or
underﬂow can occur, and all of the operations work straightforwardly as expected.
4.3.3 Concretizing iptrﬁn values. The ﬁnite memory model deﬁnes iptr to be unsigned 64-bit
integers. However, unlike for ordinary i64 arithmetic operations, in which LLVM IR’s nuw and
nsw (“No un/signed wrap”) ﬂags cause overlow/underﬂow to be treated as introducing undeﬁned
behavior, for iptr, such errors instead introduce OOM. This diﬀerence from “ordinary” integers
is crucial to maintaining the connection between the inﬁnite and ﬁnite semantics. To see why,
consider the following program (written using C-like notation that is easy to express as VIR code):
iptr i = 1;
while (0 < i) { ++i; printf("%zd\n", i); }
do_evil();
   In the inﬁnite language the iptr addition can never overﬂow, so this program will count up
indeﬁnitely, never calling the do_evil function. If we naïvely “convert” this program to a ﬁnite
program by simply using 64-bit arithmetic, which can wrap, the value of i will overﬂow to the
value 0, terminating the loop and thus calling do_evil, which is not an allowed reﬁnement. From
this example we can see that it’s clearly not safe to allow iptrﬁn values to wrap in general, as that
can change the meaning of the program. LLVM’s nuw ﬂag also does the wrong thing—it introduces
undeﬁned behavior, so translating the inﬁnite program to a ﬁnite program in this way would cause
the target program to have UB while the source program does not!
   Ultimately, the only reasonable solution is to add bounds checks to integer operations on iptr
values and to halt the program with OOM when the checks fail (intuitively, such an arithmetic
operation has run out of bits in which to store the result). The VIRﬁn semantics incorporates these
bounds checks directly into the speciﬁcation of arithmetic on iptr values, as part of concretization,
but these bounds checks could be added explicitly on top of regular i64 values if desired.

4.4   Behavioral Refinement within VIR𝑋
If we ﬁx our attention on just one of VIRinf or VIRﬁn —call it VIR𝑋 —and consider the interpretation
stacks as shown in Figure 8, there are several notions of behavioral reﬁnement that are useful for
reasoning about the semantics. First, there is reﬁnement at each successive layer of interpretation—
that is, we can think of interpretation down to each layer as deﬁning a program semantics with its
own notion of reﬁnement. Following [38], a key result about of the VIR development shows that



©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                  19


reﬁnement at one layer implies reﬁnement at the next layer, which allows reasoning at one stage
of the interpretation stack to be used to prove results about the “full” semantic interpretation.
   Up until the interpretation of memory events, reﬁnement is built on stateful variants of the
eutt𝑅 bisimulation relation as deﬁned previously [38]. For instance, after interpreting the local
and global environments at layer 2, we would have the following top-level reﬁnement relation
between the behaviors of programs under a given environment represented by the itrees 𝑃 and 𝑄
of type itree 𝐸 2 (𝐸𝑛𝑣𝐿 × (𝐸𝑛𝑣𝐺 × V)):
                                      𝑃 ⊒2 𝑄     :=    eutt≈𝑒𝑛𝑣2 (𝑃, 𝑄)
Typically, we instantiate the reﬁnement relation by using it on the interpretations of program
syntax, i.e., by taking 𝑃 = J𝑝K2 𝑔 𝑙 and 𝑄 = J𝑞K2 𝑔 𝑙, where 𝑔 and 𝑙 are global and local environments.
The relation ≈𝑒𝑛𝑣2 acts as a postcondition on the results computed by the 𝑃 and 𝑄; in this case, it
states that the returned values are equivalent, ignoring the global and local environments.
   Once memory events are interpreted the semantics is nondeterministic, as the handler for M
events (which deﬁnes the meanings of MPush, MPop, Load, Store, and Alloca) is implemented
using the nondeterministic primitives of the general memory model framework operations from
Figure 3, along with the serialize and deserialize mechanisms described above. The interpre-
tation of P events also introduces further nondeterminism due to the treatment of undef values.
The reﬁnement relation after interpreting memory and pick events is given by a set inclusion
relation between sets of itrees 𝑃 and 𝑄 of type P (itree 𝐸 4 𝑀𝑒𝑚 × (𝐸𝑛𝑣𝐿 × (𝐸𝑛𝑣𝐺 × V))):
                             𝑃 ⊒4 𝑄     :=     ∀𝑡 ′ ∈ 𝑄, ∃𝑡 ∈ 𝑃, eutt≈𝑒𝑛𝑣4 (𝑡, 𝑡 ′ )
The sets of itrees are generally taken to be those given by the interpretation of program syntax
using the propositional semantics, so 𝑃 = J𝑝K4 𝑔 𝑙 𝑠𝑖𝑑 𝑚 and 𝑄 = J𝑞K4 𝑔 𝑙 𝑠𝑖𝑑 𝑚, where 𝑔 and 𝑙 are
the initial global and local environments as before, 𝑠𝑖𝑑 is the initial high watermark for store ids,
and 𝑚 is the initial state of the memory.
   Finally, we would like to take UB and OOM into account. The semantics of UB ∅ provides “time
traveling” undeﬁned behavior semantics [10]. Intuitively, any program, here represented as an
interaction tree, that may reach a UB ∅ event is considered to be ill-deﬁned. We write this predicate
as hasUB(𝑡), and, in that case, any other behavior is allowed in its set of reﬁnements. Dually,
the treatment of O events says that an out-of-memory event reﬁnes any behavior (but not in a
“time-traveling” fashion—the programs must agree up until the O ∅ occurs). That notion is deﬁned
via a modiﬁed version of the ordinary eutt𝑅 relation, which we write as eutt_oom𝑅 . Like eutt,
eutt_oom is a weak simulation relation, but it additionally allows eutt_oom𝑅 (𝑡, trigger O ∅ ) for
any interaction tree 𝑡—this is the sense in which “out-of-memory” reﬁnes everything.
   Taken altogether, these deﬁnitions lead to the following top-level, deﬁnition of semantic reﬁne-
ment for two sets of behaviors 𝑃 and 𝑄:
                 𝑃 ⊒VIR 𝑄     :=    ∀𝑡 ′ ∈ 𝑄, ∃𝑡 ∈ 𝑃, hasUB(𝑡) ∨ eutt_oom≈𝑒𝑛𝑣VIR (𝑡, 𝑡 ′ )
Once again, we can deﬁne reﬁnement for VIR programs 𝑝 and 𝑞 by taking 𝑃 = J𝑝KVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚
and 𝑄 = J𝑞KVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚.
4.4.1 Refinement Theorems for VIR𝑋 . As mentioned above, the VIR development proves that re-
ﬁnement at lower levels in the interpretation stack of Figure 8 imply reﬁnement at later levels
(these are, intuitively, easy to prove because the less interpretation that has been done, the stronger
the notion of reﬁnement is). That means we can prove:
  Theorem 4.1 (Level refinement). For interpretations levels ℓ ≤ ℓ ′ and for any behaviors 𝑃 and
𝑄, if 𝑃 ⊒ℓ 𝑄 then 𝑃 ⊒ℓ ′ 𝑄. In particular, for any ℓ, we have 𝑃 ⊒ℓ 𝑄 implies 𝑃 ⊒VIR 𝑄.



©2024 Copyright held by the owner/author(s).
20                                      Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


Equally important is the ability to serially compose program reﬁnements within a level of interpretation—
as is needed to prove a pipeline of program optimizations correct. To this end, we prove:

   Theorem 4.2 (Transitivity of refinement). At every level ℓ, if 𝑃 ⊒ℓ 𝑄 and 𝑄 ⊒ℓ 𝑅 then it is
also the case that 𝑃 ⊒ℓ 𝑅.

4.5 Lowering VIRinf to VIRﬁn
The main idea in this paper is to separate compilation into two distinct phases—there is an ex-
plicit transition from a source language such as VIRinf , with semantics using inﬁnite memory, to
a “target” language such as VIRﬁn , which uses a ﬁnite memory. Intuitively, when we convert an
inﬁnite program to a ﬁnite program the only diﬀerence in their behavior should be that the ﬁnite
program can halt with an out-of-memory event at any point, instead of continuing execution. The
semantics of VIRﬁn is more constrained than that of VIRinf because the ﬁnite address size and iptr
size means that programs which allocate too much memory or compute addresses outside of the
bounds of the ﬁnite memory cannot continue execution and must halt and trigger OOM instead.
   We can express this connection as (yet another!) reﬁnement. This relation is deﬁned in terms of
orutt𝑅 (similar to how eutt_oom𝑅 is used to deﬁne the single-language reﬁnements in Section 4.4).
orutt𝑅 is a heterogeneous version of eutt_oom𝑅 , based on the rutt𝑅 relation between ITrees
with diﬀerent event structures instead of eutt𝑅 , which operates on ITrees with the same event
types. This is necessary as VIRinf and VIRﬁn have events which are parameterized by the types of
addresses and iptr values.
   The correspondence between memory conﬁgurations is given the (overloaded) & relation shown
in Figure 7. To express the relationship between VIRinf under-deﬁned values and VIRﬁn ones, we
also need to instantiate the lift_sbyte function required in that Figure. To do so, we simply lift
the ⌈𝑝⌉ operation (which injects pointers) to all of the 𝑢𝑣 cases—the resulting relation is an injec-
tion that lifts a ﬁnite 𝑢𝑣 to its inﬁnite counterpart, ⌈𝑢𝑣⌉. That deﬁnition allow us to deﬁne the &
relation for environments too.
   Putting all the pieces together, yields the following deﬁnition:

              𝑃 &VIR 𝑄 :=         ∀𝑡 ′ ∈ 𝑄, ∃𝑡 ∈ 𝑃. hasUB(𝑡) ∨ orutt (&𝑚𝑒𝑚 ⊗&𝑒𝑛𝑣 ) (𝑡, 𝑡 ′ )

  This deﬁnition says that for every behavior exhibited by the ﬁnite semantics, 𝑄 (as represented
by the ITree 𝑡 ′ ), we can ﬁnd a corresponding behavior, 𝑡 ′ in the inﬁnite semantics, 𝑃. The ITrees
that represent the behaviors should agree with each other, either continuing indeﬁnitely, or until
both ITrees terminate in lock-step (by raising an error or returning a value successfully), or until
the ﬁnite ITree raises an out-of-memory event. Finally this relation considers UB∅ , if any ITree in
𝑃 contains UB the relation holds.

     Theorem 4.3 (Infinite-to-finite Top-level Refinement). For every VIR program 𝑝,
                      inf   inf   inf      inf    inf           ﬁn    ﬁn   ﬁn      ﬁn    ﬁn
                   J𝑝KVIR 𝑔𝑖𝑛𝑖𝑡 𝑙𝑖𝑛𝑖𝑡 𝑠𝑖𝑑𝑖𝑛𝑖𝑡 𝑚𝑖𝑛𝑖𝑡 &VIR J𝑝KVIR 𝑔𝑖𝑛𝑖𝑡 𝑙𝑖𝑛𝑖𝑡 𝑠𝑖𝑑𝑖𝑛𝑖𝑡 𝑚𝑖𝑛𝑖𝑡

   This guarantees that our translation does not add any new behaviors, and that the ﬁnite program
will behave identically to the inﬁnite one until the programs terminate in lock-step, or the ﬁnite
program runs out of memory. Despite the apparent simplicity, this is a very technically challenging
theorem to prove for several reasons. First, because it quantiﬁes over all programs, it touches the
full semantics of both VIRinf and VIRﬁn , which, for LLVM IR, involves dozens of arithmetic, bitwise,
logic, and datatype manipulation instructions—there are literally hundreds of cases to consider.



©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                                     21

 define void @alloca_code() {                define void @ptoi_code() {                    define void @ret_code() {
   %ptr = alloca i64                           %ptr = alloca i64                             ret void
   ret void                                    %i = ptrtoint ptr %ptr to iptr              }
 }                                             ret void
                                             }
                                      Fig. 10. Example code for optimizations.


   Second, it is asking us to prove an existential claim. Digging into the proof, we end up needing
a lemma roughly of the form:
                                                ﬁn          ﬁn         inf             inf                 inf    ﬁn
      ∀𝑡 inf 𝑡 ﬁn , orutt𝑅1 (𝑡 inf , 𝑡 ﬁn ) → ∀𝑡 2 J𝑡 ﬁn K ∋ 𝑡 2 → ∃𝑡 2 , J𝑡 inf K ∋ 𝑡 2     ∧ orutt𝑅2 (𝑡 2 , 𝑡 2 )
                                                     inf                                                         ﬁn
   That is, we need to ﬁnd a VIRinf tree, 𝑡 2 , whose behaviors agree with the VIRﬁn tree 𝑡 2 except
for OOM. Ideally we would be able to use coinduction to walk through the orutt𝑅1 (𝑡 inf , 𝑡 ﬁn ) rela-
                inf
tion to build 𝑡 2 , because that would give us the appropriate relationships between continuations
nodes in corresponding parts of the ITrees. Unfortunately, existentials are inductive in Coq, so we
cannot use coinduction to extract information from this relation until the existential is already
instantiated... which is too late! We therefore have to deﬁne a coinductive function that lifts the
        ﬁn                 inf
ﬁnite 𝑡 2 to the inﬁnite 𝑡 2 , and then re-derive the relationship between them.
   Finally, because the semantic interpretations on both sides are deﬁned by layers of monadic in-
terpreters (as in Figure 8), the proof itself proceeds by establishing the connection between inﬁnite
and ﬁnite semantics at each layer, leading to many reﬁnement lemmas, that together imply this
theorem. (There are other technical hurdles too—the orutt relation used here and earlier is itself
a non-trivial variant of the ITrees rutt mixed inductive-coinductive deﬁnition, which requires a
signiﬁcant amount of metatheory, for instance to prove transitivity, to be useful.)

5 OPTIMIZATIONS UNDER THE MEMORY MODEL
This section explores some important program transformations enabled by our memory model
using the code examples shown in Figure 10. We have veriﬁed reﬁnement relations between these
blocks of code, in both the inﬁnite language and in the ﬁnite language (where applicable). Though
we have not (yet) veriﬁed full-blown optimization passes based on these transformations15 , the
semantic reasoning used in the following reﬁnement proofs is representative of the key ideas
needed for the general case. A notable aspect of these examples is that the inﬁnite memory model
allows for dead allocation removal while the ﬁnite memory model does not.
   The main results, each veriﬁed in Coq, are as follows:
Optimization 1. Dead allocation removal (only allowed in the inﬁnite model):

               ∀𝑔 𝑙 𝑠𝑖𝑑 𝑚.J@alloca_codeKVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚 ⊒VIR J@ret_codeKVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚
  Note that the twin-allocation model and CompCertS models described in Section 2 are not able to
perform this transformation in general, unless they can verify that the allocation always succeeds—
otherwise, removing the allocation may cause the program to continue executing instead of halting.
This is not a problem in our two-phased model because allocations in the inﬁnitary semantics
always succeed, so we never have to worry about failed allocations hiding extra behaviors of the
program.
Optimization 2. Removing a ptrtoint cast (only allowed in inﬁnite model):
15 In general, doing that would require static analysis and non-trivial manipulation of VIR syntax, which, while certainly

doable, is beyond the scope of this paper.




©2024 Copyright held by the owner/author(s).
22                                Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic




             ∀𝑔 𝑙 𝑠𝑖𝑑 𝑚.J@ptoi_codeKVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚 ⊒VIR J@ret_codeKVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚
   The twin-allocation and CompCertS models would be able to remove the ptrtoint cast in this
example, but still would not be able to remove the alloca (as in the previous example). The quasi-
concrete model cannot justify this reﬁnement, because casting a pointer to an integer impacts the
layout of the concrete memory and, in a ﬁnite setting, that could potentially result in the program
halting (and thus removing the cast could change the behavior of the program). Again, this is
something that the two-phased model is able to handle gracefully, as pointer to integer casts are
essentially no-ops. The cast could be removed in both the ﬁnite and inﬁnite models, but as per the
previous example, the allocation can only be removed in the inﬁnite.
Optimization 3. Adding an alloca (allowed in both the inﬁnite and ﬁnite model):

            ∀𝑔 𝑙 𝑠𝑖𝑑 𝑚.J@ret_codeKVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚 ⊒VIR J@alloca_codeKVIR 𝑔 𝑙 𝑠𝑖𝑑 𝑚
   Finally, we may wish to add an allocation to a program (certain optimizations may wish to cache
a result, for instance). This proves tricky for the approach taken by CompCertS, which maintains
an invariant that memory usage never increases after a program transformation. Both our inﬁnite
and ﬁnite models allow this, however, thanks to the out-of-memory reﬁnement relations we’ve
developed.

5.1   Bounds Checking Overhead
Our two-phased memory model ensures that pointer–integer casts never have an external eﬀect,
which allows them to be removed when performing program transformations. One might reason-
ably wonder, however, about the bounds checks on iptr arithmetic in VIRﬁn and whether these
would impact possible optimizations. They do, but we believe the impact should be fairly minimal
for the following reasons.
   Firstly, nearly all optimizations should be performed under VIRinf semantics, prior to lowering
the program into the ﬁnitary semantics. Under the inﬁnitary semantics, iptr arithmetic is just
arithmetic on Z, and expressions involving iptr can be optimized in the inﬁnite world using these
unbounded integers as a model without bounds checks. Any iptr computations that happen to
be dead can be removed prior to lowering the program into the ﬁnite world.
   All normal optimizations can occur at the inﬁnite level, and thus the only optimizations nec-
essary to do on ﬁnite programs would involve removing the bounds checks required to trigger
OOM that are added by the inﬁnite to ﬁnite translation. These bounds checks can, naturally, have
a performance impact; however, we believe that they will not be a signiﬁcant impediment to the
performance of real-world programs, and, in many cases, optimizations on ﬁnitary LLVM pro-
grams should be able to remove these bounds checks entirely. Consider the following possible use
cases for ptrtoint casts iptr arithmetic, which cover many real-world use cases:
    (1) Pointers cast to integers to use as a hash.
    (2) XOR doubly-linked lists.
    (3) Using the least-signiﬁcant-bit of a pointer as a ﬂag.
    (4) Indexing into allocated blocks.
   For (1), pointers can be cast to simple integer types, like i64, instead. The truncation does not
matter in these use cases, as the program will not cast the value back to a pointer. This will, how-
ever, require programmers to make a choice to cast to the appropriate integer type.
   Doubly-linked lists using xor (2) are an interesting use of pointer arithmetic, however the ﬁnite
iptr values will be 64-bit values, and performing a bitwise xor cannot yield an out of bounds value.



©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                      23


         read𝑏run (p : Ptr)     :   MemExec(SByte)               →
                                                                 −
     run                                              allocarun ( b : list SByte)   :   MemExec(Ptr)
write𝑏 (p : Ptr) (b : SByte)    :   MemExec(unit)                →
                                                                 −
                  pushfrun      :   MemExec(unit)     mallocrun ( b : list SByte)   :   MemExec(Ptr)
                     popfrun    :   MemExec(unit)              freerun (p : Ptr)    :   MemExec(unit)

                          Fig. 11. Executable memory model: low level operations



Similarly, bitwise operations that use unused bits in pointers as ﬂags (3) cannot cause an overﬂow
either, so bounds checking will not be necessary for these operations.
   And, of course, another important case to consider is the use of iptr arithmetic to index into
an allocated block. However, this use case should be covered by the LLVM IR’s getelementptr
operation instead, where bounds checks are unnecessary. If getelementptr is used to compute an
out of bounds pointer, using that pointer to perform a memory access will cause UB∅ in the inﬁnite
semantics anyway due to mismatched provenances.
   Finally, existing programming languages like Rust can achieve a great deal of performance, de-
spite requiring bounds checking for array accesses [29]. We’re optimistic that 1) most situations
where iptr arithmetic will be used will fall into these cases and not require bounds checking, 2)
in rarer circumstances, other LLVM optimizations may be able to remove the bounds checks, and
3) for any remaining bounds checks the costs will be minimal. We believe that the ﬂexibility our
memory model allows for optimizations prior to the ﬁnite language level will outweigh these rare
costs.

6 EXECUTABLE REFERENCE INTERPRETERS
A formal speciﬁcation of a language should be useful, in that it allows for validating optimizations
of interest, but also faithful to existing implementations and informal speciﬁcations. Where useful-
ness is the realm of formal veriﬁcation, faithfulness sends us back to a more traditional software
engineering consideration: testing. This need for validation is well identiﬁed among contributors
of formal semantics, and has even led to the development of dedicated tools and techniques to
alleviate the pain: ad-hoc usage of big-step semantics [6, 9], the K framework [32], and skeletal
semantics [7] all notably contribute in this direction.

6.1 Executable Memory Models
The ITree framework [35], on which we base our work, is extremely helpful for validating such
large scale semantics as ITrees can be extracted to executable code. In our case, the memory model
presented in Section 3 is not deterministic —a crucial necessity to faithfully characterize memory
for LLVM. Therefore it’s intrinsically non-executable, as we implement in Coq the speciﬁcation
monad propositionally, representing sets P (𝐴) as predicates A -> Prop.
   To facilitate testing (see below), we provide proven-correct, executable versions of the memory
model. To lighten the induced development burden, we maintain the implementation as monadic
code as parallel as possible to the speciﬁcation, which helps, in particular, with mirroring of
changes between them.
   Figure 11 describes the executable memory model interface: it precisely mimics the speciﬁcation,
except that it lives in a deterministic, executable monad: MemExec(𝑋 ) , Conf → Result (Conf ×𝑋 ).
   The implementations of each of these operations closely mirrors their speciﬁcation counterparts.
They syntactically diverge signiﬁcantly only when the speciﬁcation is nondeterministic, i.e., in the
fresh and find_bk utilities needed for alloca and malloc.



©2024 Copyright held by the owner/author(s).
24                                   Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


   On the executable side, fresh simply uses a trivial freshness monad, which increments a natu-
ral number to generate fresh provenance. Our current implementation of find_block is currently
quite elementary, but suﬃcient for our testing purpose: it looks up the largest addresses currently
allocated, and returns the range of the required size of following addresses. More clever allocation
strategies, such as those used by actual implementations of malloc to reduce memory fragmenta-
tion, could be implemented if relevant: the speciﬁcation only enforces that the allocated block is
contiguous, and disjoint from any other block.

6.1.1 Correctness of the executable memory models. We prove for each memory operation that
its executable implementation is valid with respect to its speciﬁcation counterpart. Since these
implementations are pure Coq functions, validity is almost deﬁned as point-wise set membership,
ensuring that, for any initial state, the computed result belongs to the speciﬁcation, or that the
speciﬁcation contains undeﬁned behavior:
A basic memory model computation (𝑠 : MemExec(𝑋 )) is valid with respect to a speciﬁcation
(S : MemSpec(𝑋 )) if:
                                    ∀𝜎, (S 𝜎) ∋ UB ∨ (S 𝜎) ∋ 𝑠 𝜎

Our development proves these soundness lemmas for all of the memory model primitives.

6.2 Executable VIR
Section 4 describes the integration of our memory model into VIR, a formal model of LLVM IR. Fig-
ure 8 also shows the right-hand path of interpreters, which provide an executable implementation
by specializing the concretization operation of Section 4.3 to pick default values for each undef𝜏
(for instance undefi8 is 0). Let us call the resulting top-level executable program interpretVIR .
   Using the soundness lemmas for the memory-model base operations, it is straightforward to
show that the resulting deterministic interpretation function is a valid reﬁnement of the semantics:

     Theorem 6.1 (Interpreter is sound). For all programs 𝑝,

             J𝑝KVIR 𝑔𝑖𝑛𝑖𝑡 𝑙𝑖𝑛𝑖𝑡 𝑠𝑖𝑑𝑖𝑛𝑖𝑡 𝑚𝑖𝑛𝑖𝑡 ⊒VIR {interpretVIR 𝑝 } 𝑔𝑖𝑛𝑖𝑡 𝑙𝑖𝑛𝑖𝑡 𝑠𝑖𝑑𝑖𝑛𝑖𝑡 𝑚𝑖𝑛𝑖𝑡

  That is, the (singleton set) of behaviors deﬁned by the executable interpreter reﬁnes the semantic
speciﬁcation—in other words, the interpreter is “correct.”

6.2.1 Testing the VIR semantics. The resulting VIR interpreter, even with the somewhat complex
memory model that manipulates symbolic bytes, is performant enough to be able to run real LLVM
IR code. We use it on a suite of test cases consisting of several hundred hand-written unit tests
of LLVM IR semantic features, as well as on LLVM IR code generated by compiling source C
programs. We have also experimented with using QuickChick [11] to randomly generate LLVM
IR programs that stress-test the memory model, and we can use the ability to generate LLVM
IR to instantiate parts of the Alive2 [28] suite as executable tests. In all cases, we do diﬀerential
testing of the executable VIR model versus llc to look for problems on either side. In the process
of developing the memory model for this project, such testing was invaluable to debugging the
model. It also highlighted some ill-speciﬁed corner cases in the LLVM IR itself, for instance, it is
unclear what the getelementptr instruction should do when computing addresses for structures
and arrays whose data values are smaller than 8 bits and hence “share” an address in memory, and
extractelement seems to have similar problems when vector elements are smaller than 8 bits,
resulting in miscompilations.



©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                25


7 DISCUSSION
7.1 Additional related work
The individual phases in our two-phased memory model share a lot in common with the existing
state of the art in memory models—especially those already discussed in detail in Section 2—but
with the crucial distinction that our approach recognizes that the compilation pipeline for many
programming languages involves a phase-change from higher level programs with unbounded
memory semantics, to bounded machine code (a boundary which is awkwardly straddled by com-
piler IRs like LLVM, and lower level languages like C). Many projects have either an explicitly ﬁnite
size of memory [4, 21, 27], or utilize a parameterized ﬁnite pointer type [18, 20]. C memory models
[18, 20] often even have a uintptr_t type as a parameter, which is part of the inspiration for our
iptr extension to LLVM. These works generally consider a single ﬁnite parameterization of their
memory models, however, and do not relate diﬀerent parameterizations of the memory models.
This raises the question: how would the memory model with 32-bit pointers relate to its 64-bit
parameterization? We provide the answer with our out-of-memory reﬁnement relations, treating
the unbounded speciﬁcation as the ground truth, and ﬁnite parameterizations as reﬁnements.
   Our memory model is currently just a sequential one. Concurrent memory models [1, 8, 14, 16,
23, 27, 33, 34] are much more complex, but we believe the two-phased approach is orthogonal
and would apply to concurrent models as well. There are also other considerations for undeﬁned
behavior in memory models, which we don’t touch upon. In C, strict aliasing requirements are
important for ruling out pointer aliasing via the types of pointers, which some memory models
[18, 20] tackle. Languages like Rust have complex ownership rules for pointers that eliminate
pointer aliasing at the type level, the semantics of which is tackled by the RustBelt [14] project.

7.2   The two-phase memory model in the context of VIR
These improvements to the VIR semantics have been a substantial development eﬀort, expanding
the codebase by over three fold in terms of lines-of-Coq-code. We’ve aimed to keep things realistic
while encapsulating the many complications present in a substantial subset of LLVM. For instance,
undef is known to be incredibly complicated to reason about [22], and the under-deﬁned values
required to simulate undef contain over 30 constructors, making (proofs by) case analysis particu-
larly arduous. Furthermore, undef interacts with the memory model and semantics in non-trivial
ways, and many changes were made throughout the development to ﬁgure out precisely where
under-deﬁned values should undergo concretization and nondeterminism should be collapsed so
as to enable as many optimizations in the semantics as possible. The nondeterminism in the speciﬁ-
cation monads has also been a challenge to work with, as illustrated in the discussion surrounding
Theorem 4.3.
   The product of this painstaking work is a parameterized semantics for a substantial LLVM-like
language with an in-depth characterization of many intricate and interacting details like undef,
undeﬁned behavior, nondeterministic memory operations, and casts between pointers and inte-
gers. We have done so in an eﬀort to ease justifying optimizations in a compiler, without the com-
piler itself having to maintain complicated invariants in order to prove the validity of important
optimizations. Our veriﬁed two-phased compilation between memory models provides a novel ap-
proach to handling the complexities of low-level memory operations like casts between pointers
and integers in the presence of high-level optimizations, and demonstrates the semantic necessity
of considering ﬁnite memory when compiling programs to ﬁnite architectures, which is applicable
to many languages.
   Having put in this eﬀort, we are now in position to reap many rewards. For instance the Helix
project [39] is a veriﬁed compiler for a numerical programming language that targets VIR, and our



©2024 Copyright held by the owner/author(s).
26                                         Calvin Beck, Irene Yoon, Hanxi Chen, Yannick Zakowski, and Steve Zdancewic


interface should provide a more accurate view of LLVM memory which will lend more credence to
the compilation pipeline for Helix. Similarly, our memory model should be amenable to separation
logics built using Iris [15], which have been used in conjunction with VIR before [36, 37]. We
believe that our richer memory model and higher-ﬁdelity LLVM IR semantics will be a boon for
these and future projects that depend upon VIR.

REFERENCES
 [1] Mark Batty, Scott Owens, Susmit Sarkar, Peter Sewell, and Tjark Weber. 2011. Mathematizing C++ concur-
     rency. In Proceedings of the 38th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
     guages (Austin, Texas, USA) (POPL ’11). Association for Computing Machinery, New York, NY, USA, 55–66.
     https://doi.org/10.1145/1926385.1926394
 [2] Frédéric Besson, Sandrine Blazy, and Pierre Wilke. 2014. A precise and abstract memory model for C using symbolic
     values. In Asian Symposium on Programming Languages and Systems. Springer, 449–468.
 [3] Frédéric Besson, Sandrine Blazy, and Pierre Wilke. 2015. A concrete memory model for CompCert. In Interactive
     Theorem Proving: 6th International Conference, ITP 2015, Nanjing, China, August 24-27, 2015, Proceedings 6. Springer,
     67–83.
 [4] Frédéric Besson, Sandrine Blazy, and Pierre Wilke. 2019. CompCertS: a memory-aware veriﬁed C compiler using a
     pointer as integer semantics. Journal of Automated Reasoning 63 (2019), 369–392.
 [5] Frédéric Besson, Sandrine Blazy, and Pierre Wilke. 2019. A veriﬁed CompCert front-end for a memory model sup-
     porting pointer arithmetic and uninitialised data. Journal of Automated Reasoning 62, 4 (2019), 433–480.
 [6] Martin Bodin, Arthur Charguéraud, Daniele Filaretti, Philippa Gardner, Sergio Maﬀeis, Daiva Naudziuniene, Alan
     Schmitt, and Gareth Smith. 2014. A trusted mechanised JavaScript speciﬁcation. In The 41st Annual ACM SIGPLAN-
     SIGACT Symposium on Principles of Programming Languages, POPL ’14, San Diego, CA, USA, January 20-21, 2014,
     Suresh Jagannathan and Peter Sewell (Eds.). ACM, 87–100. https://doi.org/10.1145/2535838.2535876
 [7] Martin Bodin, Philippa Gardner, Thomas P. Jensen, and Alan Schmitt. 2019. Skeletal semantics and their interpreta-
     tions. Proc. ACM Program. Lang. 3, POPL (2019), 44:1–44:31. https://doi.org/10.1145/3290357
 [8] Soham Chakraborty and Viktor Vafeiadis. 2017. Formalizing the Concurrency Semantics of an LLVM Fragment. In
     Proceedings of the 2017 International Symposium on Code Generation and Optimization (Austin, USA) (CGO ’17). IEEE
     Press, 100–110. https://doi.org/10.5555/3049832.3049844
 [9] Arthur Charguéraud. 2013. Pretty-Big-Step Semantics. In Programming Languages and Systems - 22nd European
     Symposium on Programming, ESOP 2013, Held as Part of the European Joint Conferences on Theory and Practice of Soft-
     ware, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings (Lecture Notes in Computer Science, Vol. 7792), Matthias
     Felleisen and Philippa Gardner (Eds.). Springer, 41–60. https://doi.org/10.1007/978-3-642-37036-6_3
[10] Raymond Chen. 2014. Undeﬁned behavior can result in time travel (among other things, but time travel is the funkiest).
     https://devblogs.microsoft.com/oldnewthing/20140627-00/?p=633
[11] Maxime Dénès, Catalin Hritcu, Leonidas Lampropoulos, Zoe Paraskevopoulou, and Benjamin C Pierce. 2014. Quick-
     Chick: Property-based testing for Coq. In The Coq Workshop, Vol. 125. 126.
[12] Charles Ellison. 2012. A formal semantics of C with applications. Ph. D. Dissertation. University of Illinois at Urbana-
     Champaign.
[13] ISO 9899:1999 1999. Programming Languages — C. Standard. International Organization for Standardization.
[14] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the foundations of
     the Rust programming language. Proceedings of the ACM on Programming Languages 2, POPL (2017), 1–34.
[15] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
     ground up: A modular foundation for higher-order concurrent separation logic. Journal of Functional Programming
     28 (2018), e20.
[16] Jeehoon Kang, Chung-Kil Hur, Ori Lahav, Viktor Vafeiadis, and Derek Dreyer. 2017. A promising semantics
     for relaxed-memory concurrency. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Program-
     ming Languages (Paris, France) (POPL ’17). Association for Computing Machinery, New York, NY, USA, 175–189.
     https://doi.org/10.1145/3009837.3009850
[17] Jeehoon Kang, Chung-Kil Hur, William Mansky, Dmitri Garbuzov, Steve Zdancewic, and Viktor Vafeiadis. 2015. A
     formal C memory model supporting integer-pointer casts. ACM SIGPLAN Notices 50, 6 (2015), 326–335.
[18] Robbert Krebbers. 2013. Aliasing restrictions of C11 formalized in Coq. In International conference on certiﬁed programs
     and proofs. Springer, 50–65.
[19] Robbert Krebbers, Xavier Leroy, and Freek Wiedijk. 2014. Formal C semantics: CompCert and the C standard. In
     Interactive Theorem Proving: 5th International Conference, ITP 2014, Held as Part of the Vienna Summer of Logic, VSL
     2014, Vienna, Austria, July 14-17, 2014. Proceedings 5. Springer, 543–548.




©2024 Copyright held by the owner/author(s).
A Two-Phase Infinite/Finite Low-Level Memory Model                                                                    27


[20] Robbert Jan Krebbers. 2015. The C standard formalized in Coq. Ph. D. Dissertation. [Sl]:[Sn].
[21] Juneyoung Lee, Chung-Kil Hur, Ralf Jung, Zhengyang Liu, John Regehr, and Nuno P Lopes. 2018. Reconciling high-
     level optimizations and low-level code in LLVM. Proceedings of the ACM on Programming Languages 2, OOPSLA
     (2018), 1–28.
[22] Juneyoung Lee, Yoonseung Kim, Youngju Song, Chung-Kil Hur, Sanjoy Das, David Majnemer, John Regehr, and
     Nuno P. Lopes. 2017. Taming Undeﬁned Behavior in LLVM. In Proceedings of the 38th ACM SIGPLAN Conference on Pro-
     gramming Language Design and Implementation (PLDI 2017). ACM, 633–647. https://doi.org/10.1145/3140587.3062343
[23] Sung-Hwan Lee, Minki Cho, Anton Podkopaev, Soham Chakraborty, Chung-Kil Hur, Ori Lahav, and Viktor Vafeiadis.
     2020. Promising 2.0: global optimizations in relaxed memory concurrency. In Proceedings of the 41st ACM SIGPLAN
     Conference on Programming Language Design and Implementation (London, UK) (PLDI 2020). Association for Comput-
     ing Machinery, New York, NY, USA, 362–376. https://doi.org/10.1145/3385412.3386010
[24] Rodolphe Lepigre, Michael Sammler, Kayvan Memarian, Robbert Krebbers, Derek Dreyer, and Peter Sewell. 2022. VIP:
     verifying real-world C idioms with integer-pointer casts. Proc. ACM Program. Lang. 6, POPL, Article 20 (jan 2022),
     32 pages. https://doi.org/10.1145/3498681
[25] Xavier Leroy and Sandrine Blazy. 2008. Formal veriﬁcation of a C-like memory model and its uses for verifying
     program transformations. Journal of Automated Reasoning 41 (2008), 1–31.
[26] Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister, and Christian Ferdinand. 2016.
     CompCert-a formally veriﬁed optimizing compiler. In ERTS 2016: Embedded Real Time Software and Systems, 8th
     European Congress.
[27] Liyi Li and Elsa Gunter. 2020. K-LLVM: A Relatively Complete Semantics of LLVM IR. In 34rd European Conference
     on Object-Oriented Programming, ECOOP 2020, Berlin, Germany. https://doi.org/10.4230/LIPIcs.ECOOP.2020.7
[28] Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and John Regehr. 2021. Alive2: Bounded Translation
     Validation for LLVM. In Proceedings of the 42nd ACM SIGPLAN International Conference on Programming Language
     Design and Implementation (Virtual, Canada) (PLDI 2021). Association for Computing Machinery, New York, NY, USA,
     65–79. https://doi.org/10.1145/3453483.3454030
[29] Alana Marzoev. 2022.           How much does Rust’s bounds checking actually cost? — blog.readyset.io.
     https://blog.readyset.io/bounds-checks/. [Accessed 27-02-2024].
[30] Kayvan Memarian, Victor BF Gomes, Brooks Davis, Stephen Kell, Alexander Richardson, Robert NM Watson, and
     Peter Sewell. 2019. Exploring C semantics and pointer provenance. Proceedings of the ACM on Programming Languages
     3, POPL (2019), 1–32.
[31] Kayvan Memarian, Justus Matthiesen, James Lingard, Kyndylan Nienhuis, David Chisnall, Robert N. M. Watson, and
     Peter Sewell. 2016. Into the Depths of C: Elaborating the de Facto Standards. In Proceedings of the 37th ACM SIGPLAN
     Conference on Programming Language Design and Implementation (Santa Barbara, CA, USA) (PLDI ’16). Association
     for Computing Machinery, New York, NY, USA, 1–15. https://doi.org/10.1145/2908080.2908081
[32] Grigore Roşu and Traian Florin Şerbănută. 2010. An overview of the K semantic framework. The Journal of Logic and
     Algebraic Programming 79, 6 (2010), 397 – 434. https://doi.org/10.1016/j.jlap.2010.03.012 Membrane computing and
     programming.
[33] Jaroslav Ševčík, Viktor Vafeiadis, Francesco Zappa Nardelli, Suresh Jagannathan, and Peter Sewell.
     2013.     CompCertTSO: A Veriﬁed Compiler for Relaxed-Memory Concurrency.                  J. ACM 60, 3 (2013), 22.
     https://doi.org/10.1145/2487241.2487248
[34] Jaroslav Ŝevčik, Viktor Vafeiadis, Francesco Zappa Nardelli, Suresh Jagannathan, and Peter Sewell.
     2011.      Relaxed-memory concurrency and veriﬁed compilation.             SIGPLAN Not. 46, 1 (jan 2011), 43–54.
     https://doi.org/10.1145/1925844.1926393
[35] Li-yao Xia, Yannick Zakowski, Paul He, Chung-Kil Hur, Gregory Malecha, Benjamin C. Pierce, and Steve Zdancewic.
     2020. Interaction Trees. Proceedings of the ACM on Programming Languages 4, POPL (Jan. 2020).
[36] Euisun Yoon. 2023. MODULAR SEMANTICS AND METATHEORY FOR LLVM IR. Ph. D. Dissertation. Max Planck
     Institute for Software Systems.
[37] Irene Yoon, Yannick Zakowski, and Steve Zdancewic. 2022. Formal Reasoning About Layered Monadic Interpreters.
     Proceedings of the ACM on Programming Languages 6, ICFP (2022).
[38] Yannick Zakowski, Calvin Beck, Irene Yoon, Ilia Zaichuk, Vadim Zaliva, and Steve Zdancewic. 2021. Modular, Com-
     positional, and Executable Formal Semantics for LLVM IR. Proc. ACM Program. Lang. 5, ICFP, Article 67 (aug 2021),
     30 pages. https://doi.org/10.1145/3473572
[39] Vadim Zaliva, Ilia Zaichuk, and Franz Franchetti. 2020. Veriﬁed translation between purely functional and imperative
     domain speciﬁc languages in HELIX. In International Workshop on Numerical Software Veriﬁcation. Springer, 33–49.




©2024 Copyright held by the owner/author(s).
