                                                       C-rusted: The Advantages of Rust, in C,
                                                              without the Disadvantages
                                                                 (Extended Abstract)
                                                      Roberto Bagnara                           Abramo Bagnara                            Federico Serafini
                                             BUGSENG & University of Parma                        BUGSENG                         BUGSENG & University of Parma
                                                       Parma, Italy                               Parma, Italy                              Parma, Italy
                                              Email: name.surname@unipr.it             Email: name.surname@bugseng.com           Email: name.surname@bugseng.com
arXiv:2302.05331v3 [cs.PL] 26 Aug 2023




                                                               I. T HE P ROBLEM                               3) The reason why C allows writing terse programs is
                                            The C programming language is a crucial foundation of all            the same reason why C code that is (intentionally or
                                         current applications of information technology. It is, by far,          unintentionally) obscure is so common.
                                         the most used language when access to hardware is essential,
                                                                                                             These negative sides of C compound when memory handling
                                         even for critical safety-related and/or security-related systems.
                                                                                                             is concerned, as memory handling is fully under the program-
                                            There are very strong economic reasons behind the use of
                                                                                                             mers’ responsibility:
                                         the C programming language, namely:
                                           1) C compilers exist for almost any processor;                     1) memory references in C are (unless special care is taken)
                                           2) C compiled code is very efficient and without hidden               raw pointers that bring with themselves no information
                                               costs;                                                            about the associated memory block or its intended use;
                                           3) C allows writing compact code thanks to the many built-         2) no run-time checks are made to ensure the safety of
                                               in operators and the limited verbosity of its constructs;         pointer arithmetic, memory accesses, and memory deal-
                                           4) C is defined by an ISO standard [1];                               location;
                                           5) C, possibly with extensions, allows easy access to the          3) code involving memory addressing with pointers can be
                                               hardware;                                                         particularly opaque to peer review.
                                           6) C has a long history of use, including in critical systems;
                                           7) C is widely supported by all sorts of tools.                     Some of the most common C memory issues are:
                                            In fact, the C programming language is so widespread that
                                         it has no equals as far as the following criteria are considered:     • dereferencing invalid pointers, including null point-
                                            • number of developers in low-level, safety-related and
                                                                                                                 ers, dangling pointers (pointers to deallocated memory
                                               security-related industry sectors;                                blocks), and misaligned pointers;
                                                                                                               • use of uninitialized memory;
                                            • number of qualified tools for compilation, analysis, test-
                                                                                                               • memory leaks;
                                               ing, coverage, documentation, code generation and any
                                                                                                               • invalid deallocation (including double free and free with
                                               other code manipulation;
                                            • number and range of supported architectures.
                                                                                                                 invalid argument);
                                                                                                               • buffer overflow.
                                            On the other hand, several of C’s strong points have negative
                                         counterparts, e.g.:                                                    Even though various coding standards (with MISRA C
                                           1) The fact that C code can efficiently be compiled to            being the most authoritative one) and lots of “bug finders”
                                               machine code for almost any architecture is due to the        exist, there is no verification tool that can guarantee, in a
                                               fact that, whenever this is possible and convenient, high-    strong sense, the absence of a large class of software defects
                                               level constructs are mapped directly to a few machine         in a consistent, effective and repeatable way. In fact:
                                               instructions: given that instructions sets differ from one
                                               architecture to the other, this is why the behavior of C        • MISRA C [2] provides guidelines for writing software
                                               programs is not fully defined.                                    that is on average much safer;
                                           2) The reason why the maximum execution time of C                   • bug finders find some recognizable instances of possible
                                               programs can be estimated with good precision by expert           defects;
                                               programmers is because there is nothing happening under         • systems based on deductive methods, like Frama-C [3],
                                               the hood and, in particular, there is no built-in run-time        require programmers that are highly skilled in mathemati-
                                               error detection.                                                  cal logic and, even when such programmers are available,
     development time is multiplied by a factor from 2 to 4;1                                c) nominal types and nominal subtypes compatible with
   • deep semantic analysis based on abstract interpretation                                     any standard C data type.
     only covers a small set of program properties and is                                 2) As far as the compiler is concerned, all C-rusted annota-
     affected by non-repeatable results due to the heuristics                                 tions are macros expanding to nothing (with the exception
     that are used to throttle the computational complexity of                                of global annotations, which expand to something that
     the analysis.                                                                            obeys ISO C syntax and is ignored by the compiler). The
   Of course, all this is not new. C criticism for the facility with                          (partially) annotated C programs being fully compatible
which memory handling programming mistakes are committed                                      with all versions of ISO C, can be translated with
date back to shortly after the language was made available to                                 unmodified versions of any compilation toolchain capable
the public [4]. However, apparently the measure is full if the                                of processing ISO C code.
idea of rewriting (parts of) Linux in Rust —where committing                              3) In contrast to (2), a static analyzer can interpret the
such mistakes is significantly more difficult— is being taken                                 annotations and validate the program: if the static analysis
seriously [5], [6], [7], [8], [9], [10], [11], [12]. It is not yet clear                      flags no error, then the annotations are provably coherent
whether a global move to Rust is possible or even desirable.                                  among themselves and with respect to annotated C code,
The main issues are:                                                                          in which case said annotated program is provably exempt
   • Legacy: there is too much legacy code written in C;                                      from a large class of logic, security, and run-time errors.
     the costs and risks involved in rewriting existing code                              4) It is important to note that it is not only the presence of
     bases (a good part of which has a more-than-honorable                                    annotations that expresses information: even the absence
     operational history and may be in perfectly good shape)                                  of annotations has a definite meaning that is checked
     are enormous.                                                                            by the static analyzer so that any possible oversight or
   • Personnel: retraining millions of developers to Rust                                     inconsistency is flagged. This characteristic is used, for
     would take time and lots of resources.                                                   example, to “reverse” some dangerous defaults of the C
   • Portability: for many MCUs used in the development of                                    programming language: whereas in C an object of type
     embedded systems, no implementation of Rust currently                                    pointer can be a null pointer, in C-rusted a pointer can
     exists.                                                                                  be null only if it is annotated as such.
   • Tools: while all sort of tools are available for C, the same                        As a result:
     thing cannot be said for Rust.                                                        • Legacy code can be reused as-is: for code that is safety-
   So, what does the current ferment about Rust tell us?                                      critical, annotations can be added in order to obtain proofs
That the industry is ready to accept that programmers take                                    of safety, but no rewriting is required, thereby avoiding
a more disciplined approach by embracing strong data typing                                   all risks that this would entail.
enhanced with program annotations. This is the real change                                 • There is no need to retrain the developers, apart from
of perspective: the technology to assist this new attitude in the                             those that, working on safety-critical components, would
creation of C code with unprecedented integrity guarantees is                                 have to get familiarity with the annotations.
available, in its essence, since decades.                                                  • Existing C compilers can be used without any change,
                                                                                              thereby ensuring maximum portability.
                      II. F ROM C TO C- RUSTED
                                                                                           • All sort of tools, in addition to compilers, can also be
   In this paper, we propose an alternative approach as a reply                               used without any change.
to the temptation of abandoning C in favor of other languages
offering stronger guarantees in terms of safety and security.                                            III. C- RUSTED AT A G LANCE
The idea is to take some concepts that have been proven to                                  Even though the C programming language is (for the sake of
work well in other languages, such as “the ownership model”                              efficiency only) statically typed, types only define the internal
of Rust, into C, in order to define C-rusted: a safe, secure and                         representation of data and little more: types in C do not offer
energy-efficient flavor of C. The key points of our approach                             programmers a way of expressing non-trivial data properties
are the following:                                                                       that are bound to the program logic. For instance:
  1) C-rusted is based on annotations with which the program-                               • an open file has the same type as a closed file;
      mer can express:                                                                      • a resource or a transaction has the same type indepen-
     a) ownership, exclusivity and shareability of language,                                   dently from its state;
        system and user-defined resources;                                                  • an exclusive reference and a shared reference to a re-
     b) properties of resources and the way they evolve during                                 source are indistinguishable;
        program execution;                                                                  • an integer with special values that represent error condi-

   1 The reported factor comes from the personal experience of the first author,               tions is indistinguishable from an ordinary integer.
who has been trained extensively in mathematical logic up to and including                  In C-rusted all these differences can be expressed incre-
the Ph.D. level. The same author has also used Frama-C in computer science               mentally, resulting in increased documentation, readability and
courses for several years and found that the learning process is particularly
difficult for students at the bachelor’s and master’s level, despite the fact that       reusability of the code. Most importantly, this enables the
Floyd-Hoare logic played a fundamental role in such courses.                             C-rusted Analyzer, which is based on the ECLAIR Software



                                                                                     2
 1   #include <fcntl.h>
 2   #include <unistd.h>
 3   #include <stdlib.h>
 4

 5   extern void process(char *string);
 6

 7   int foo(const char *fname, size_t bufsize) {
 8     int fd = open(fname, O_RDONLY);
 9     char *buf = (char *) malloc(bufsize);
10     ++fd;
11     ssize_t bytes = read(fd, buf, bufsize - 1U);
12     buf[bytes] = '\0';
13     process(buf);
14     return 0;
15   }

                         Fig. 1. A C program compiling with no warnings with gcc -c -std=c18 -Wall -Wextra -Wpedantic


 1   #include <fcntl.h>
 2   #include <unistd.h>
 3   #include <stdlib.h>
 4

 5   extern void process(char *string);
 6

 7   int foo(const char *fname, size_t bufsize) {
 8     int fd = open(fname, O_RDONLY);
 9     char *buf = (char *) malloc(bufsize);
10     ++fdw1 ;
11     ssize_t bytes = read(fdw2 , bufw3 , bufsize - 1U);
12     buf[bytes]w4 w5 = '\0';
13     process(bufw6 );
14     return 0w7 w8 ;
15   }

     w1 : After receiving the return value of open(), fd contains a file descriptor or the erroneous value −1: fd cannot be
           incremented.
     w2 , w3 , w4 , w5 : fd is not a valid file descriptor, bytes may be −1, buf may be NULL.
     w6 : Does process() take ownership, i.e., can it or must it deallocate its argument?
     w7 : The open file description possibly obtained from open() is leaked here.
     w8 : The block of memory possibly pointed to by buf is leaked here.
                                     Fig. 2. The C-rusted Analyzer gives several warnings on the same C program



     Verification Platform, to verify correctness on any platform,           and allows us making some observations: while fd is declared
     with any architecture, and for each compiler.                           having type int, the value of fd has properties that change
        Consider the program in Figure 1, which the GNU C                    throughout the function body; similarly for buf and bytes.
     compiler compiles without any warning even at a very high               In other words, the C-rusted type system is able to track how
     warning level. The program contains a lot of likely mistakes,           properties of resources change depending on the considered
     including the meaningless —but in C perfectly valid— numer-             program point. The large part of the result is obtained without
     ical increment of a file descriptor.                                    any annotation at all, thanks to the fact that the C Standard
        When given to the C-rusted Analyzer the very same program            Library and the POSIX Library have been annotated once
     triggers several diagnostic messages, summarized in Figure 2,           and for all (and the same can be done with any frequently
     where the notation wn decorating a program point means that             used library). Moreover, annotations are not heavy and do not
     the indicated applicable warning is given at that program point.        clutter the code; type qualifiers, such as e_hown(), can also be
        A much saner version of the program is depicted in Figure 3          embedded in typedefs and a proper choice of typedef names



                                                                         3
 1   #include <fcntl.h>
 2   #include <unistd.h>
 3   #include <stdlib.h>
 4   #include <crusted.h> // Include C-rusted declarations, e.g., for e_hown().
 5

 6   // The actual parameter must be a valid (hence, non-null) pointer
 7   // to a char array in the heap of which process() will take ownership:
 8   // the caller must have ownership for otherwise it would be unable to pass it on.
 9   extern void process(char * e_hown() string);
10

11   int foo(const char *fname, unsigned bufsize) {
12     int fd; // (The value of) `fd` is indeterminate.
13     fd = open(fname, O_RDONLY);
14     // `fd` is either the erroneous value -1 or an owning reference to an open file description.
15     if (fd == -1)
16       return 1;
17     // `fd` is definitely an owning reference to an open file description.
18

19       char *buf = (char *) malloc(bufsize);
20       // `buf` is either NULL or an owning reference to a heap-allocated char array.
21       if (buf == NULL || bufsize == 0U) {
22         (void) close(fd);
23         // Ownership of the open file description moved from the actual parameter
24         // to the formal parameter of close(), which will close it:
25         // no open file description leak; `fd` cannot be used anymore but it can be overwritten.
26         return 1;
27       }
28       // `buf` is definitely an owning reference to a heap-allocated char array.
29

30       ssize_t bytes = read(fd, buf, bufsize - 1U); // No ownership move, resources are borrowed.
31       // `bytes` is either the erroneous value -1 or the number of bytes read into `buf`.
32       if (bytes == -1) {
33         free(buf);
34         // Ownership of the heap-allocated memory moved from the actual parameter
35         // to the formal parameter of free(), which will deallocate it:
36         // no memory leak, `buf` cannot be used anymore but it can be overwritten.
37         (void) close(fd); // Ownership moved from actual to formal parameter, as in line 22.
38         return 1;
39       }
40       // `bytes` is definitely the number of bytes read into `buf`.
41       buf[bytes] = '\0';
42

43       process(buf);
44       // Ownership of the heap-allocated memory moved from the actual parameter
45       // to the formal parameter of process(), which will deallocate it:
46       // no memory leak, `buf` cannot be used anymore but it can be overwritten.
47

48       if (close(fd) != 0) // Ownership moved from actual to formal parameter, as in line 22.
49         return 1;
50

51       return 0;
52   }

                                   Fig. 3. The C-rusted Analyzer gives no warning on this version




                                                                 4
also helps readability and understandability.                                     non-optional values, the ordinary values. A clear example of
                                                                                  optional types are pointer types, having NULL as the optional
                          IV. R EFERENCES
                                                                                  value, which encodes the peculiar, though common condition
   The annotation language allows expressing constraints on                       of a pointer pointing to nothing. The purposes of null pointers
the use of resources via references. A resource is anything that                  are essentially the following:
a C program has to manage. Generally speaking, resources                             • initialization of a pointer-type resource to a known and
need to be allocated or reserved, need to be manipulated                               comparable value;
by operations that have to be performed in some predefined                           • encoding of the fact that a certain condition involving a
ordering, and need to be destroyed or deallocated or unre-                             pointer-type resource has occurred (often, but not always,
served. C-rusted supports different kinds of resources: memory                         an error condition);
resources and any language-defined, system-defined or user-                          • allowing the definition of recursive data structures.
defined abstraction with a definite lifecycle. A reference is any
                                                                                     As programs grow, the proper handling of optional values
C expression that is able to refer to a resource. A valid pointer
                                                                                  and their encoded conditions becomes increasingly difficult.
and a file descriptor are example of references.
                                                                                  Some programming languages, such as OCaml and Rust,
A. Owning, Exclusive and Shared References                                        include syntactic constructs allowing the explicit declaration
  C-rusted distinguishes between different kinds of references:                   and management of optional types supported by automatic
                                                                                  checks performed statically and/or dynamically. As far as C-
Owning references: An owning reference to a resource has a
                                                                                  rusted is concerned, support for the handling of optional types
    special association with it. In a safe C-rusted program,2
                                                                                  at compile time is offered via e_opt(...) annotations.
    every resource subject to dynamic release (as opposed
    to automatic release, as in the case of stack variables
    going out of scope), must be associated to one and only                        1   #define e_opt_hown() e_opt(NULL) e_hown()
    one owning reference. Through the program evolution,                           2

    the owner of a resource might change, due to a mecha-                          3   void * e_opt_hown() e_uninit()
    nism called ownership move, but at any given time said                         4   malloc(size_t size);
    resource will have exactly one owner. The association                          5

    between the owner and the owned resource only ends                             6   void * e_opt_hown()
    when a designated release function is called using the                         7   calloc(size_t nmemb, size_t size);
    owner as parameter. Note that an owning reference is a                         8

    kind of exclusive reference.                                                   9   void
Exclusive references: As the name suggests, an exclusive                          10   free(void * e_opt_hown() e_release() ptr);
    reference grants exclusive access to a resource and, as
    such, both read and write operations are allowed through                           Fig. 4. Ownership and optionality in C Standard Library functions
    the exclusive reference. As a consequence of this fact,
    no more than one usable exclusive reference to the same                          Figure 4 illustrates the concepts discussed so far by showing
    resource can exist at any given time; moreover, the                           the C-rusted interpretation of some of the C Standard Library
    existence of a usable exclusive reference is incompatible                     functions that deal with ownership of heap-allocated memory
    with the existence of any other usable reference to the                       resources. The e_opt_hown() annotation for the return type
    same resource. Note that the referred resource cannot be                      of malloc() and calloc() encodes the following informa-
    released via an exclusive non-owning reference (only an                       tion:
    owning reference allows that).                                                  1) e_opt(NULL), denoting the fact that an optional value,
Shared references: A shared reference to a resource can be                              i.e., a null pointer, is returned in case of allocation failure;
    used to access the resource without modifying it. As                            2) e_hown(), denoting the fact that an owning reference,
    read-only access via multiple references is well defined,                           i.e., a valid pointer, to a heap-allocated resource is re-
    there may exist several usable shared references to a                               turned in case of allocation success.
    single resource. However, during the existence of a shared                    Summarizing, the value returned from malloc() and
    reference, no exclusive references to the same resource                       calloc() is an optional owning reference to a heap-allocated
    can be used.                                                                  resource.3 This information is used by the C-rusted Analyzer
B. Optionality                                                                    to diagnose all occurrences of:
                                                                                     • a dereferencing operation on an optional reference un-
   In C-rusted an optional type is any type having a subset
                                                                                        less guarded by a suitable optionality check (typically
of its values that are “reserved” for encoding the occurrence
                                                                                        encoded by an if statement);
of some special condition. We refer to these special values as
optional values so that they can be distinguished from others                        3 Note that the C code in Figure 4 is for illustration purposes only: the C-
                                                                                  rusted Analyzer automatically interprets the C Standard Library functions as
  2 We call a C-rusted program safe if the C-rusted Analyzer does not issue       if they were declared with suitable C-rusted annotations and does not require
warnings for it.                                                                  touching the header files provided by the underlying C implementation.




                                                                              5
   •  a function call using an optional reference as actual pa-                        1       #include <crusted.h>
      rameter unless the call is guarded by a suitable optionality                     2
      check or the callee’s formal parameter is declared to be                         3       typedef int T;
      an optional reference as well;                                                   4
   • a return of an optional reference from a function unless
                                                                                       5       typedef Node_t {
      the return statement is guarded by a suitable optionality                        6         T elem;
      check or the function return type is declared to be an                           7         struct Node_t * e_opt_hown() nextp;
      optional reference as well;                                                      8       } Node_t;
   • an (optional or non-optional) owning reference going out-
                                                                                       9
      of-scope.                                                                       10       // Shared reference.
The diagnostic messages require the programmers to con-                               11       void node_print(const Node_t *nodep);
centrate on the intended program logic and take appropriate                           12       // Exclusive reference.
actions, such as filtering out optional values and/or adding or                       13       bool node_insert_after(Node_t *nodep, T elem);
amending the annotations. When user-defined functions are                             14       // Owning reference.
involved, diagnostics may be resolved:                                                15       Node_t * e_opt_hown() node_ctor(T elem);
   • in the function call, by providing suitable actual param-
      eters and destination for the return value;                                                       Fig. 5. Different kinds of references
   • in the function declaration, by adjusting the annotations
      of the formal parameters and return type and making sure
      the function body is coherent with the declaration.
In all cases, this results in increases program readability thanks                    manipulation functions. The node_print() function, which
to the expressive power of annotations, in particular as far as                       only needs to read the resource “node” in order to print it,
function interfaces are concerned. And, when all diagnostic                           correctly takes as parameter a reference to a const-qualified
messages by the C-rusted Analyzer have been addressed, the                            resource: in C-rusted, this is interpreted as an implicit shared
effort is rewarded by strong safety and security guarantees by                        reference. Note that the concept of shared reference is stronger
construction. For instance, optional types are a complete and                         than const-qualification: while in C the constness only affects
effective method for tracking the generation and propagation                          the directly-referred node, in C-rusted the “shareability” (and
of null pointers: together with the ownership model, the avoid-                       the constness property) is recursively propagated down to the
ance of invalid pointer dereferencing and invalid deallocations                       last node of the list. Another crucial aspect is that while
is guaranteed.                                                                        in C the constness of an object can be easily bypassed,
   Another important aspect of C-rusted is that, unless oth-                          e.g., using pointer casts, in a safe C-rusted program this is
erwise specified, all references must refer to initialized re-                        not allowed. Going on with the analysis of Figure 5, the
sources, thus avoiding uninitialized memory reads. This is the                        first parameter of node_insert_after() function (which
purpose of the e_uninit() annotation on the return type of                            modifies the list inserting a new node after the referred one)
malloc() in Figure 4. As calloc() returns zero-initialized                            is an example of implicit exclusive reference, whereas the
memory, no such annotation is used for its return type.                               return type of node_ctor(), whose purpose is the acquisition
   As can be seen in Figure 4, free() is the designated func-                         of a new node, is an optional owning reference. As a final
tion for the release of heap-allocated memory resources: this                         note on Figure 5, note the inclusion of crusted.h, whose
is expressed by the e_release() annotation. In combination                            purpose is simply to ensure all annotations are removed during
with e_opt_hown(), this means that all calls to free() must                           the preprocessing translation phase and do not affect the
be performed by passing either                                                        compilation of the program.
   • a null pointer (upon which the free() function will do                              All this has an unmistakable Rust taste, of course, gener-
      nothing, as guaranteed by the C Standard), or                                   alized to all kinds of resources (not just memory blocks) and
                                                                4
   • an owning reference to a releasable memory resource.                             all kinds of references (not just pointers).
   Even though C-rusted supports explicit annotations for
                                                                                           C-rusted annotations allow expressing much more:
exclusive and shared references (via the e_excl(...) and
e_shar(...) annotations, respectively), in many cases such                                 • The fact that library and user-defined functions may
annotations are not needed and relying on “const correctness”                                encode different information in the same C object. For
is sufficient. Namely, the C-rusted Analyzer infers the shared                               instance, the return value of POSIX’s open() is encoded
or exclusive nature of a reference from the presence or absence                              into an int, which is either −1, in case of error, or it is
of the const qualifier on the referred resource, respectively.                               a file descriptor.
This is illustrated in Figure 5, which contains declarations for a                         • Other instances of nominal typing fully under control of
node (the basic building block of a singly-linked list) and some                             the programmer.
   4 In C-rusted parlance, a resource is “releasable” when it has been properly            • The way in which functions modify the properties of
finalized and/or it does not contain any valuable or sensible information.                   resources.



                                                                                  6
                    V. N OMINAL T YPING                                 Figure 7, four different nominal types related to temperature
   Nominal typing is a restriction placed by strong type systems        scales are defined: Celsius, Kelvin, ∆C and ∆K, all of
whereby two types are compatible only if they have the same             them having double as underlying type. This shows how
name, independently from their underlying representation. In            nominal typing can prevent accidentally mixing different
the C world this concept is already present in the MISRA C              temperature scales, independently of the underlying C data
essential type model [2]: a Boolean is not an integer, even             types. Therefore, value of nominal types have been con-
when it is represented by an int, as it may be the case                 strained within the proper ranges and the admitted operations
in C90 implementations [13], [14]. Similarly, an object of              upon them have been made explicit through e_bop(...)
enumerated type is not an integer, despite being represented by         (for binary operations) and e_uop(...) (for unary opera-
an implementation-defined integer type. Generally speaking,             tions), so that only meaningful operations are allowed. For
nominal typing allows imposing a clear separation between the           instance, while celsius_t - celsius_t is admissible as
C data type representation and the semantics of the particular          is kelvin_t - kelvin_t, and these give dltcelsius_t
type, preventing unwanted and often dangerous operations on             and dltkelvin_t, respectively, celsius_t / celsius_t
nominal types, such as conversions, arithmetic and bitwise              must be flagged because it has no physical meaning due
manipulation.                                                           to the fact that Celsius is not an absolute scale, whereas
                                                                        kelvin_t / kelvin_t makes perfect sense.
1   typedef int e_type() e_val(e_geq(0)) fd_t;                                         VI. R ESOURCE M ANAGEMENT
2   typedef fd_t e_own() fd_own_t;
3   typedef fd_own_t e_opt(-1) fd_opt_own_t;                               In this section we discuss C-rusted ability to capture the
4                                                                       way in which functions modify the “properties” of resources:
5   fd_opt_own_t                                                        this includes user-defined properties and all sorts of resources.
6   open(const char *path, int oflag);
7                                                                       A. Initialization and Finalization
8   int e_val(e_range(-1, 0))                                              As already mentioned, in C-rusted all references must
9   close(fd_own_t fildes);                                             refer to initialized resources unless specified otherwise. This
                                                                        means that functions that deal with uninitialized resources
            Fig. 6. C-rusted view of open() and close()                 must be properly annotated using either e_init(...) or
                                                                        e_uninit(...). The former is used to annotate function
   Nominal typing is fully supported by C-rusted’s type sys-            parameters that are references whose purpose is the initial-
tem: as an example, file descriptors are recognized and treated         ization of the referred resource: upon entry to the function the
as nominal types. Figure 6 shows how some functions involv-             resource may be uninitialized, whereas upon exit the resource
ing file descriptors are interpreted within C-rusted: in addition       will be definitely initialized (inside the function body, the C-
to the optionality and ownership information conforming to              rusted Analyzer will flag all operations on the referred resource
the POSIX specification, the e_type() annotation is used                that precede initialization). The e_uninit(...) annotation is
to specify that fd_t and all the types derived from it are              used to annotate possibly uninitialized resources or references
nominal types. Resources of type fd_t are file descriptors              to possibly uninitialized resource, as in the case of malloc()’s
and, even if at a C level they are represented using integers,          return type.
they have nothing to do with integers. In particular, they cannot          An application of such concepts is presented in Fig-
be mixed converting the one to the other, and operations that           ure 8, where e_init() appears in the annotation of the
are permitted on integers are not permitted on file descriptors.        channel_ctor() function parameter. While the first call
Moreover, the e_val(...) annotation specifies that:                     to channel_send() is flagged by the C-rusted Analyzer
  1) file descriptors are represented by non-negative integers;         as use of an uninitialized resource, the second call to
  2) in case an error occur, open() returns the integer −1              channel_send() is perfectly legal as it takes place after a
      (which is not a file descriptor);                                 call to channel_ctor(). Figure 8 also shows the use of the
  3) close() returns an integer in the interval [−1, 0].                e_fini() annotation. In line 3, it means that resources of type
Note that C-rusted also supports annotations to express the file        channel_t, once initialized, need to be finalized before being
access mode according to the value of the actual parameter              released: failure to do so, as it happens in line 14, triggers a
oflag, which must be given as a compile-time constant. This             C-rusted Analyzer message. In line 7, e_fini() identifies the
allows C-rusted Analyzer checking the validity of operations            function in charge of the resource finalization.
involving a file descriptor (such as read() and write()).                  Note that, for some resources, finalization is crucial. As
In order to keep the example as short as possible, such                 an example, for resources storing confidential information it
annotations have been omitted.                                          is recommended to completely overwrite the used memory
   When the power of nominal typing is put into the hands               locations in order to ensure such information stays in memory
of programmers, a number of applications emerge that have               for the shortest possible time (a release of the resource memory
the potential of preventing many programming errors. In                 alone does not achieve that). Of course, in C-rusted a resource



                                                                    7
 1   #include <crusted.h>
 2

 3   typedef double e_type() e_val(e_geq(-273.15)) celsius_t;    // Celsius.
 4   typedef double e_type() e_val(e_geq(0))       kelvin_t;     // Kelvin.
 5   typedef double e_type()                       dltcelsius_t; // Delta Celsius.
 6   typedef double e_type()                       dltkelvin_t; // Delta Kelvin.
 7

 8   e_bop(dltcelsius_t, celsius_t, -, celsius_t); // ∆C = C − C.
 9   e_bop(dltkelvin_t, kelvin_t, -, kelvin_t);    // ∆K = K − K.
10   e_bop(double, kelvin_t, /, kelvin_t);
11

12   void bar(celsius_t c1, celsius_t c2, kelvin_t k1, kelvin_t k2) {
13     dltcelsius_t dltc = c1 - c2;
14     double c_ratio = c1 / c2; // Operation not allowed.
15     double k_ratio = k1 / k2;
16     // ...
17   }

                                                                Fig. 7. Nominal types


 1   #include <crusted.h>
 2

 3   typedef struct { /* ... */ } e_fini() Channel_t;
 4

 5   void channel_ctor(Channel_t * e_init() chanp);
 6   bool channel_send(Channel_t *chanp, const char *msg);
 7   void channel_dtor(Channel_t * e_fini() chanp);
 8

 9   int baz(void) {
10     Channel_t c;
11     channel_send(&c, "..."); // Use of uninitialized resource.
12     channel_ctor(&c);
13     if (!channel_send(&c, "Message"))
14       return -1;             // Missing finalization.
15     channel_dtor(&c);
16     return 0;
17   }

                                                  Fig. 8. Initialization and finalization of resources



     that has been finalized is not readable anymore: it can only be           specifies the preconditions that must hold on the referred mixer
     re-initialized or released.                                               to safely carry out the computation and the postconditions that
                                                                               must hold on the mixer when the function returns to the caller.
     B. Custom Properties                                                      In function qux() the contract specified by the annotation is
        Through annotations, C-rusted allows the programmer to                 violated on two accounts. In line 11 there is a violation of
     also express non-trivial data properties that are bound to the            mixer_on() preconditions because the door may be open:
     program logic: for example, the C-rusted Analyzer is capable              e_in(blade=off) states that it will take in input a reference
     of ensuring that a set of user-defined operations are performed           to a mixer having the blades turned off, no preconditions
     in the correct ordering. This is done through the e_in(...)               about the state of the door are present. Furthermore, function
     and e_out(...) annotations expressing preconditions and                   qux(), in line 16, is also violating the postconditions of its
     postconditions, respectively. An example of this facility is pre-         own signature: e_out(door=?) states that, upon return, the
     sented in Figure 9. There, an opaque type struct Mixer_t                  door of the passed mixer may be open or closed; nothing is
     (the kitchen tool) is declared along with functions that operate          said about the state of the blade upon return, which implies
     on a resource of type Mixer_t. Each function declaration                  the blade return state must be equal to the entry state, i.e., the



                                                                           8
 1   #include <crusted.h>
 2

 3   typedef struct Mixer Mixer_t;
 4

 5   void mixer_open(Mixer_t * e_in(blade=off) e_out(door=opened) mxp);
 6   void mixer_close(Mixer_t * e_out(door=closed) mxp);
 7   void mixer_on(Mixer_t * e_in(door=closed) e_out(blade=on) mxp);
 8   void mixer_off(Mixer_t * e_out(blade=off) mxp);
 9

10   void qux(Mixer_t * e_in(blade=off) e_out(door=?) mxp) {
11     mixer_on(mxp);    // Door may be open!
12     mixer_close(mxp);
13                        // Door closed.
14     mixer_on(mxp);
15                        // Blade on.
16     return;            // Blade still on!
17   }

                                                Fig. 9. Preconditions and postconditions for the safe use of a mixer



     blade must be turned off upon return. The problem is that this                     1   e_decl_props(FILE, e_unsafe("FILE"));
     is not happening: the programmer has probably forgotten to                         2   typedef FILE * fp_t;
     call mixer_off() before returning from the function. These                         3   typedef fp_t e_own() fp_own_t;
     mistakes are reported in the form of compile-time warnings                         4   typedef fp_own_t e_opt(NULL) fp_opt_own_t;
     by the C-rusted Analyzer.                                                          5

                VII. S AFE AND U NSAFE B OUNDARIES                                      6   fp_opt_own_t
        C-rusted allows enforcing information hiding and a                              7   fopen(const char * restrict filename,
     sharp separation between interface and implementation by                           8         const char * restrict mode);
                                                                                        9
     means of a flexible access restriction system based on the
     e_unsafe(...) annotation, which identifies data types, func-                      10   int e_val(e_eq(0) || e_eq(EOF))
     tions and operations that are “unsafe” on their own or are                        11   fclose(fp_own_t fp);
     considered unsafe because they encapsulate and/or use other
     unsafe entities: in this context “unsafe” means “requiring                                  Fig. 10. C-rusted view of fopen() and fclose()
     special care and knowledge in order to ensure safety.”
        An example where this is applied concerns the pointers to
     the FILE objects used to control the standard I/O streams. The                       For the implementation side, C-rusted provides two
     application programmer obtains such pointers by calling the                       annotations: e_unchecked(...) and e_checked(...).
     fopen() standard function, but these ought to be treated as if                    e_unchecked(...) marks a statement as not expected to
     they were not pointer at all: just atomic, unique identifiers                     conform to the C-rusted safety and security requirements:
     with a NULL special value. If they were implemented as                            every function containing unchecked statements must thus be
     opaque pointers some of the potential issues (e.g., copies                        annotated as unsafe. e_checked(...) also marks a state-
     of a FILE object may not give the same behavior as the                            ment as not expected to conform to the C-rusted syntax
     original) would be prevented, but there is no such a guar-                        and semantics, but its use is guaranteed to be safe by the
     antee. In fact, MISRA C has a mandatory rule that bans                            programmer under every aspect of C-rusted needed warranties.
     dereferencing pointers to FILE [2, Rule 22.5]. Figure 10                          An example is presented in Figure 11 where, in order to
     shows how the fopen() and fclose() functions are seen                             correctly implement the fclose() function, all the accesses
     by C-rusted: the e_unsafe("FILE") annotation ensures that,                        to a FILE object are encapsulated within the proper safety
     by default, all accesses to FILE objects are flagged by the                       annotation as it happens in Line 11. As a result, under the
     C-rusted Analyzer.5 Note that the string literal argument in                      responsibility of implementers, function fclose() will be
     e_unsafe("FILE") is arbitrary, which allows an unlimited                          considered as safe by the C-rusted Analyzer.
     number of “unsafety kinds.”                                                          This model is powerful, flexible and can be used to cover
        5 As in the case of open(), for brevity the annotation of fopen() shown
                                                                                       similar types, such as type sem_t of the POSIX Library, and
     in Figure 10 omits the specification of the file access mode encoded in the       user-defined entities, such as the type Channel_t of Figure 8.
     mode actual parameter, which must be given as a string literal.                   For the latter, this will ensure:



                                                                                   9
 1   #include <errno.h>                                                        supports annotations for pointers and array bounds and the
 2   #include <stdio.h>                                                        use of static analysis to validate existing annotations and to
 3   #include <stdlib.h>                                                       infer new ones. Note, though, that Checked C is a different
 4   #include "local.h"                                                        language than C: while the compilation of Checked C code
 5   #include <crusted.h>                                                      requires a special compiler, compilation of C-rusted code is
 6
                                                                               done with any C compiler.
 7   int e_val(e_eq(0) || e_eq(EOF))                                              Figure 12 places C-rusted in its context, between C and
 8   fclose(fp_own_t fp) {                                                     Rust, and summarizes the main elements for a comparison.
 9     // ...                                                                  Some of these points deserve further explanation.
10
                                                                                  First, C-rusted is not a new programming language, like
11       e_checked("FILE") {                                                   Rust and Zig: C-rusted code is standard ISO C code just
12         if (fp->flags == 0U) {                                              used in a peculiar way and in association with suitable static
13           errno = EBADF;                                                    analysis techniques.6 As such, C-rusted benefits from the
14           return EOF;                                                       huge investment the industry has made into C in terms of
15         }                                                                   compilers, tools, developers, coding standards and code bases.7
16       }                                                                     For instance, C-rusted is 100% compatible with MISRA C: a
17
                                                                               C program that is MISRA compliant can be rusted without
18       // ...                                                                negatively impacting MISRA compliance. Furthermore, an an-
19   }                                                                         notated C-rusted program validated by the C-rusted Analyzer
                                                                               has strong guarantees of compliance with respect to guidelines,
                                                                               such as those concerning the disciplined use of resources, error
 Fig. 11. Fragment of fclose() implementation with C-rusted annotations
                                                                               handling and possibly tainted inputs, for which compliance is
                                                                               much harder to achieve and argument in other ways.
  1) the use of the communication channel only through the                        Functional safety standards such as ISO 26262 [20] pre-
      safe interfaces;                                                         scribe the use of safe subsets of standardized programming
  2) the access to the (delicate) implementation details only                  languages used with qualifiable translation toolchains (see,
      by the channel implementers.                                             e.g., [21] and [22]). Insofar a C-rusted program is a standard
Note how this approach leads to the correct propagation and,                   ISO C program where the presence of annotation does not
at the same time, the correct encapsulation of (possibly) unsafe               invalidate MISRA compliance, C-rusted fits the bill as C
operations within the proper safety checks.                                    does and more, due to the strong guarantees provided by
                                                                               annotations. Contrast this with Rust and Zig: they are not
                        VIII. D ISCUSSION                                      standardized and, as a matter of fact, they frequently change
   C-rusted is a pragmatic and cost-effective solution to up the               in a way that does not follow a rigorous process. This is
game of C programming to unprecedented integrity guarantees                    the main reason why qualifying a Rust or Zig compilation
without giving up anything that the C ecosystem offers today.                  toolchain according to major functional safety standards is,
That is, keep using C, exactly as before, using the same                       in the authors’ opinion, impossible today. In contrast, any
compilers and the same tools, the same personnel. . . but                      qualified C compiler is, as is, a qualified C-rusted compiler.
incrementally adding to the program the information required                      C-rusted has been conceived for incremental adoption: C
to demonstrate correctness, using a system of annotations                      programs can be (partly) annotated so as to express: own-
that is not based on mathematical logic (or other complex                      ership, exclusivity and shareability of language, system and
languages) and can be taught to programmers in a week of                       user-defined resources, as well as properties of resources and
training.                                                                      the way they evolve during program execution. The annotated
   This technique is not new: it is called gradual typing, and                 C-rusted program parts can be validated by static analysis:
consists in the addition of information that does not alter the                if the C-rusted Analyzer flags no error, then the annotations
behavior of the code, yet it is instrumental in the verification               are provably coherent among themselves and with respect
of its correctness. Gradual typing has been applied with                       to annotated code, in which case said annotated parts are
spectacular success in the past: Typescript has been created 10                provably exempt from a large class of logic, security, and
years ago, and in the last 6 years its diffusion in the community              run-time errors. C-rusted can thus prevent many resource
of JavaScript developers has increased from 21% to 69%. And                    management errors: missing allocation, missing initialization,
it will continue to increase: simply put, there is no reason for               missing deallocation (resource leak), use after deallocation,
writing more code in the significantly less secure and verifiable                 6 C-rusted is compatible with any version of the ISO C Standard and can
JavaScript language [15].                                                      be used with any C toolchain.
   For C, a similar approach is the one of Checked C [16].                        7 We note on passing that, in the authors’ opinion, C-to-Rust transpilation

There, gradual typing is used to extend C with static and                      [17], [18], [19] is not a real solution: transpiling well-written C code to
                                                                               unreadable and unmaintainable Rust code could possibly solve only a small
dynamic checking aimed at detecting or preventing buffer                       fraction of the problems at the cost of creating several new problems. This,
overflows and out-of-bounds memory accesses. Checked C                         however, goes beyond the scope of this paper.




                                                                          10
                                                                                   C                C-rusted                 Rust
 Standardized                                                                      Yes: ISO         Yes: it is ISO C         No: moving target
 Certifiable translators exist                                                     Yes              Yes: it is ISO C         No
 Portability                                                                       Absolute         Absolute                 Limited
 Tool availability                                                                 Very large       Very large               Scarce
 Developers’ availability                                                          Large            Large                    Scarce
 Coding standards for safety and security                                          Yes              Yes                      No
 Can reuse C legacy code                                                                            Yes                      Only in some cases
 Strong guarantees on memory resources for annotated programs                                       Yes                      Yes
 Strong guarantees on user-defined resources for annotated programs                                 Yes                      Yes
 Compatibility with unannotated code                                                                Yes                      Yes
 Incremental adoption                                                                               Yes                      No
 Cost of retraining C programmers for unannotated code                                              Zero                     Significant
 Cost of retraining C programmers for annotated code                                                Moderate                 Significant

                           Fig. 12. Advantages and disadvantages of C-rusted (along with its C inheritance) and Rust



multiple deallocation, race conditions due to sharing. And this            variable liveness and the tracking of numeric information
on all sorts of resources:                                                 through value range analysis based on constraint propagation
Language-defined resources: e.g., memory blocks, stream-                   over multi-intervals. In addition, there are several finite do-
      controlling objects, mutexes.                                        mains specifically conceived for C-rusted, which track the
System resources: e.g., open file descriptions, streams, sock-             state of resources and references as well as the evolution
      ets.                                                                 of dynamic semantic properties. Scalability is ensured by
User-defined resources: all sorts of transactions, anything                intraprocedurality.
      that requires allocation, deallocation and disciplined ex-              All the annotations of C-rusted are realized via macro
      clusive and/or shareable use.                                        invocations: the corresponding macros all expand to the empty
   Thanks to nominal typing/subtyping and to the tracking of               token sequence (with the exception of global annotations,
properties, C-rusted can also prevent other errors not related             which expand to something that obeys ISO C syntax and is
to the management of resources, such as the missing detection              ignored by the compiler) so that, as far as the compiler is
of erroneous or anomalous conditions, the use of possibly                  concerned, after translation phase 4 [1, Section 5.1.1.2] it is
tainted input data, and the unwanted disclosure of confidential            as if they never existed. Of course, the C-rusted Analyzer uses
information.                                                               all the information provided by the annotations before letting
   C-rusted has been conceived for incremental adoption: new               the preprocessor making them vanish.
code that is critical can be created with annotations from the
                                                                                                        R EFERENCES
outset, and this will speed up development because the C-
rusted Analyzer will immediately provide warnings about a                  [1] ISO/IEC, ISO/IEC 9899:2018: Programming Languages — C. Geneva,
                                                                               Switzerland: ISO/IEC, 2018.
large class of mistakes. Legacy code can be annotated later,               [2] MISRA, MISRA C:2023 — Guidelines for the use of the C language
if there is value in doing so, or even left unannotated forever:               critical systems.      Norwich, Norfolk, NR3 1RU, UK: The MISRA
touching proven-in-use code with an honorable operational                      Consortium Limited, Apr. 2023, third edition, Second revision.
                                                                           [3] P. Baudin, F. Bobot, F. Bühler, L. Correnson, F. Kirchner, N. Kosmatov,
history makes no sense. Note that annotations are not intrusive:               A. Maroneze, V. Perrelle, V. Prevosto, J. Signoles, and N. Williams,
they can be embedded into typedefs and, for a large part, they                 “The dogged pursuit of bug-free C programs: The Frama-C software
are confined to function prototypes and declarations of structs                analysis platform,” Communications of the ACM, vol. 64, no. 8, pp.
                                                                               56–68, 2021.
containing references.                                                     [4] D. M. Ritchie, The Development of the C Programming Language.
                                                                               New York, NY, USA: Association for Computing Machinery, 1996, pp.
                      IX. I MPLEMENTATION                                      671–698. [Online]. Available: https://doi.org/10.1145/234286.1057834
   The implementation of the C-rusted Analyzer is based on                 [5] J. Salter, “Linus Torvalds weighs in on Rust language in
the ECLAIR Software Verification Platform.                                     the Linux kernel,” Ars Technica, Mar. 2021. [Online]. Avail-
                                                                               able: https://arstechnica.com/gadgets/2021/03/linus-torvalds-weighs-in-
   The static analysis component is formalized in terms of ab-                 on-rust-language-in-the-linux-kernel/
stract interpretation [23]. The analysis is rigorously intrapro-           [6] B. Cantrill, “Is it time to rewrite the operating system in Rust?” InfoQ,
cedural, i.e., it is done one function at a time, using only the               Jan. 2019. [Online]. Available: https://www.infoq.com/presentations/os-
                                                                               rust/
information available for that function in the translation unit            [7] J. Wallen, “Let the Linux kernel Rust,” TechRepublic, Jul. 2021.
defining it, which includes the annotations possibly provided                  [Online]. Available: https://www.techrepublic.com/article/let-the-linux-
in function declarations.                                                      kernel-rust/
                                                                           [8] S. J. Vaughan-Nichols, “Linus Torvalds on where Rust will fit into
   The analysis domains include a very precise flow-sensitive                  Linux,” ZDNet, Mar. 2021. [Online]. Available: https://www.zdnet.com/
and field-sensitive points-to analysis. Other analyses involve                 article/linus-torvalds-on-where-rust-will-fit-into-linux/




                                                                      11
 [9] ——, “Where Rust fits into Linux,” The Register, Nov. 2021.                       [17] N. Shetty, N. Saldanha, and M. N. Thippeswamy, “CRUST: A C/C++
     [Online]. Available: https://www.theregister.com/2021/11/10/where                     to Rust transpiler using a “nano-parser methodology” to avoid C/C++
     rust fits into linux/                                                                 safety issues in legacy code,” Emerging Research in Computing, Infor-
[10] L. Tung, “Google backs effort to bring Rust to the Linux kernel,” ZDNet,              mation, Communication and Applications, 2019.
     Apr. 2021. [Online]. Available: https://www.zdnet.com/article/google-            [18] M. Emre, R. Schroeder, K. Dewey, and B. Hardekopf, “Translating C
     backs-effort-to-bring-rust-to-the-linux-kernel/                                       to safer Rust,” Proceedings of the ACM on Programming Languages,
[11] M. Melanson, “Rust in the Linux kernel: ‘good enough’,” The New                       vol. 5, no. OOPSLA, pp. 1–29, 2021.
     Stack, Dec. 2021. [Online]. Available: https://thenewstack.io/rust-in-           [19] M. Ling, Y. Yu, H. Wu, Y. Wang, J. Cordy, and A. Hassan, “In Rust
     the-linux-kernel-good-enough/                                                         we trust — a transpiler from unsafe C to safer Rust,” in Proceedings of
[12] N. Elhage, “Supporting Linux kernel development in Rust,” LWN.net,                    the ACM/IEEE 44th International Conference on Software Engineering:
     Aug. 2020. [Online]. Available: https://lwn.net/Articles/829858/                      Companion Proceedings.         New York, NY, USA: Association for
[13] ISO/IEC, ISO/IEC 9899:1990: Programming Languages — C. Geneva,                        Computing Machinery, 2022, pp. 354–355.
     Switzerland: ISO/IEC, 1990.                                                      [20] ISO, ISO 26262:2018: Road Vehicles — Functional Safety. Geneva,
[14] ——, ISO/IEC 9899:1990/AMD 1:1995: Programming Languages — C.                          Switzerland: ISO, Dec. 2018.
     Geneva, Switzerland: ISO/IEC, 1995.                                              [21] ——, ISO 26262:2018: Road Vehicles — Functional Safety — Part 8:
[15] P.    Krill,    “TypeScript     usage    growing      by    leaps    and              Supporting processes. Geneva, Switzerland: ISO, Dec. 2018.
     bounds       —     report,”   InfoWorld,     Feb.     2022.     [Online].        [22] RTCA, SC-205, DO-330: Software Tool Qualification Considerations.
     Available: https://www.infoworld.com/article/3650513/typescript-usage-                RTCA, Dec. 2011.
     growing-by-leaps-and-bounds-report.html                                          [23] P. Cousot and R. Cousot, “Abstract interpretation: A unified lattice model
[16] A. Machiry, J. Kastner, M. McCutchen, A. Eline, K. Headley,                           for static analysis of programs by construction or approximation of
     and M. Hicks, “C to Checked C by 3c,” Proc. ACM Program.                              fixpoints,” in Proceedings of the Fourth Annual ACM Symposium on
     Lang., vol. 6, no. OOPSLA1, Apr. 2022. [Online]. Available:                           Principles of Programming Languages. Los Angeles, CA, USA: ACM
     https://doi.org/10.1145/3527322                                                       Press, 1977, pp. 238–252.




                                                                                 12
