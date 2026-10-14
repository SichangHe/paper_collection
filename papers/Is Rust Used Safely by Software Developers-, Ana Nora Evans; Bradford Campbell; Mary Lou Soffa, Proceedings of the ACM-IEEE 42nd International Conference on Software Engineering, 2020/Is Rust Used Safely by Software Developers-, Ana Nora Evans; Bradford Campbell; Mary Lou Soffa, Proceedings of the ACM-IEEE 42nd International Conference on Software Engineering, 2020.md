                            Is Rust Used Safely by Software Developers?
                 Ana Nora Evans                               Bradford Campbell                                           Mary Lou Soffa
            AnaNEvans@virginia.edu                             bradjc@virginia.edu                                       soffa@virginia.edu
             University of Virginia                            University of Virginia                                   University of Virginia

Abstract                                                                        Therefore, Rust includes an “escape hatch” with the unsafe key-
Rust, an emerging programming language with explosive growth,                   word1 that allows programmers to deactivate some (but not all) of
provides a robust type system that enables programmers to write                 the Rust compiler’s checks for certain regions of code. This function-
memory-safe and data-race free code. To allow access to a machine’s             ality was originally described as “pragmatic safety” [14] when Rust
hardware and to support low-level performance optimizations, a                  was first introduced, and allows developers to use their own discre-
second language, Unsafe Rust, is embedded in Rust. It contains                  tion when writing Rust code. Part of the justification for allowing
support for operations that are difficult to statically check, such             Unsafe Rust code is that uses of unsafe would be easy to locate and
as C-style pointers for access to arbitrary memory locations and                audit, and that developers can decide how much unchecked code
mutable global variables. When a program uses these features, the               they are willing to accept in their software.
compiler is unable to statically guarantee the safety properties                   Modern software development leverages and builds upon li-
Rust promotes. In this work, we perform a large-scale empirical                 braries, which often use yet other libraries. Auditing software for
study to explore how software developers are using Unsafe Rust in               uses of unsafe requires auditing all dependent libraries, a poten-
real-world Rust libraries and applications. Our results indicate that           tially cumbersome task. This overhead is mitigated, however, if
software engineers use the keyword unsafe in less than 30% of Rust              usage of unsafe is scarce and easy to locate in the Rust software
libraries, but more than half cannot be entirely statically checked             ecosystem, or if making a determination about the validity of the
by the Rust compiler because of Unsafe Rust hidden somewhere                    unsafe usage is typically straightforward. Therefore, understand-
in a library’s call chain. We conclude that although the use of the             ing how developers are actually using unsafe is necessary to eval-
keyword unsafe is limited, the propagation of unsafeness offers                 uate whether “pragmatic safety” is valid and if Rust provides a safe
a challenge to the claim of Rust as a memory-safe language. Fur-                programming environment in practice.
thermore, we recommend changes to the Rust compiler and to the                     Our study is further motivated by recent interest in Rust as a
central Rust repository’s interface to help Rust software developers            safe alternative to C for systems software [3, 6, 8, 20, 21, 24, 33] and
be aware of when their Rust code is unsafe.                                     by the development of formal definitions for Rust’s type system
                                                                                (including Unsafe Rust). For example, the Rust Belt project [18]
ACM Reference Format:                                                           proposes formal tools for verifying Unsafe Rust, and Oxide [39]
Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust            presents a formalization of a language very similar to Rust. The
Used Safely by Software Developers?. In Proceedings of 42nd International       Rust open source community recently formed a new Rust working
Conference on Software Engineering (ICSE ’20). ACM, New York, NY, USA,
                                                                                group to create a “Unsafe Code Guideline Reference” to help guide
12 pages. https://doi.org/10.1145/3377811.3380413
                                                                                developers [36]. These are encouraging steps, and understanding
                                                                                how Unsafe Rust is being used by developers will help guide the
1    Introduction                                                               successful formation of these strategies.
Programming languages directly impact the reliability, safety, and                 To acquire this understanding, we perform a large-scale study
correctness of software, and their features impact the prevalence of            and an analysis of publicly available Rust libraries and application
bugs in actual software. A relatively new programming language,                 code. We first determine how frequently the unsafe keyword is
Rust, is explicitly designed to help programmers write more reli-               used. Then we analyze the call graph of every function in our data
able software by using the compiler to help reduce memory and                   set to identify if at any point the function may use code that is
data race errors. Rust is referred to as a “safe” systems program-              not safe and not checked by the compiler. This analysis enables us
ming language, indicating that its type system, ownership model,                to find code that looks safe, but is actually Unsafe Rust. To better
automatic memory management without garbage collection, and                     understand how developers are using unsafe, we also identify the
static compiler make it well suited for writing lower-level or core             underlying code behavior that necessitates the use of Unsafe Rust
software without the common bugs that can plague code written                   to analyze the frequency of the various unsafe operations. Further,
in C and C++ [15, 29, 30].                                                      we observe the use of Unsafe Rust over time to see if there are
   The design aspects that make Rust safe, such as no arbitrary                 evolving changes in the community.
pointers or arbitrary type casting, however, would also make writ-                 To perform this analysis, we developed and implemented an
ing most or all low-level code impossible. Operations such as config-           algorithm for constructing an extended call graph of Rust functions
uring hardware or reading a network socket involve manipulating                 that uses the type information to increase the call graph precision.
memory in ways that the compiler cannot guarantee to be safe.                   Building a call graph for Rust is difficult, however, as Rust’s run-
                                                                                time polymorphism and higher order functions complicate statically
                                                                                building a call graph without missing edges or adding extra edges. In
ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea
2020. ACM ISBN 978-1-4503-7121-6/20/05. . . $15.00
https://doi.org/10.1145/3377811.3380413                                         1 Rust keywords are green and bolded while the safe and unsafe conditions are italicized.

                                                                            1
ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea                                  Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa


our approach, we identify these ambiguities, and build two versions          2   Background
of the call graph by applying both a conservative (assume the call           First, we provide a working example that will be referenced through-
will be to unsafe code) and an optimistic (assume the call we be             out the paper. We then describe the key features of Safe Rust and
to code statically checked to be safe) analysis to help bound the            Unsafe Rust that are relevant to our study. Next, we define terms
use of Unsafe Rust in Rust libraries. We then traverse and analyze           that we use to categorize Rust code. Finally, we provide some back-
the resulting extended call graph to determine how unsafeness                ground information about the general Rust software ecosystem.
propagates in real-world Rust code.
    After analyzing over 85% of the valid Rust libraries available           2.1 Working Example
at the start of our study, we find that 29% contain at least one             Figure 1(a) shows a set of functions in pseudocode from several
explicit use of unsafe. When considering the dependency tree,                libraries selected to illustrate how unsafety can propagate in a code-
however, that number increases to around 50%, meaning half of                base. We will use these functions to explain concepts throughout
Rust libraries use Unsafe Rust or rely on other libraries that use           the paper.
Unsafe Rust. Narrowing down to just the most used and downloaded                The functions are organized in five different libraries. The start-
libraries increases the use of Unsafe Rust, as around 60% of popular         ing point is function foo() in Library1, which calls the function
crates include Unsafe Rust. The majority of unsafe uses in the               bar() in Library2. The symbol :: separates the library name from
Rust ecosystem are to call other Rust functions that are marked              the function called from that library. In function bar() from Li-
unsafe. We find that only 22% of these unsafe functions are to               brary2, the call to my_object.baz() is a run-time polymorphic
external libraries implemented in C, suggesting that a majority              call to the method baz() of an instance implementing the interface
of the Unsafe Rust is actually from Rust code where the software             HasBaz. The interface HasBaz has two implementations in Library3
developer decided to disable the compiler checks. Finally, we see            and Library5.
negligible increases in the frequency of unsafe used over the past              Figure 1(b) shows the resulting library dependency graph from
ten months.                                                                  the example functions. A library depends on other libraries if it
    Based on these findings, we propose several recommendations              uses functions from those libraries, and therefore requires the other
to help realize the original vision of “pragmatic safety” in Rust, in-       libraries to completely compile a binary.
cluding programmer-assisted automated checks, additional tooling                For functions with run-time polymorphism we generate two
to help developers identify uses of unsafe, and more visible code            call graphs: conservative and optimistic (see Figure 1(b)). We will
reviews to audit uses of unsafe. These changes would allow devel-            explain this further in Section 4.
opers to better exploit the benefits of Unsafe Rust while managing
its risks to overall software reliability.                                   2.2 Safe Rust
    The contributions of this paper are:                                     Rust includes a few basic concepts that enable the compiler to en-
                                                                             force safety guarantees. The ownership mechanism in Safe Rust
    • A large-scale study and analysis of unsafe use in the Rust             requires that a unique variable is the owner for every memory lo-
      software ecosystem.                                                    cation. Memory locations are immutable unless explicitly declared
    • A call graph construction algorithm which handles generic              otherwise. Variable assignment results in a copy or a transfer of
      polymorphism.                                                          ownership, and once the variable loses ownership of the memory
    • Findings that indicate that a majority of crates are not guar-         location, that variable becomes unusable. To enable sharing, the
      anteed by the compiler be memory-safe and data-race free.              borrow mechanism allows creating memory aliases which permit
    • Highlights of our findings indicate that unsafe function calls         any number of read-only references and exactly one mutable one.
      are the most common use of unsafeness, which is caused                 The foo() function in Figure 1(a) shows an example borrow oper-
      through library dependencies rather than the use of the                ation. Together, the ownership and borrow mechanisms prevent a
      unsafe keyword, and the most downloaded crates have more               large class of memory-safety errors and data races.
      unsafe code than other other crates;                                      The definition of memory-safety used by Rust is similar to the
    • Recommendations to enhance the Rust compiler and its                   one proposed by Szekeres et al. [30]. A Rust program is memory-
      ecosystem to help developers understand when they are                  safe if it is free of any memory errors such as dereferencing a null
      using Unsafe Rust in their software.                                   or dangling pointer, reading or writing unaligned pointers, and
                                                                             reading uninitialized memory [34]. Memory leaks are explicitly
   Section 2 contains a brief introduction to Rust, Unsafe Rust (see         considered defined behavior, and thus not memory errors.
Section 2.3), the Rust software ecosystem (see Section 2.6), and the            For instances where program operation requires violating these
terms we define to facilitate discussion throughout of paper (see            constraints, Unsafe Rust allows developers to assert to the com-
Section 2.5). In Section 3 we present the research questions that            piler that they are manually implementing the necessary checks to
guided our experiment and the selection criteria for the Rust code           preserve memory-safety and data-race freedom.
that comprises our data set. Section 4 contains the approach to
answering the research questions. In Section 5 we define the data            2.3 Unsafe Rust
set we used in the experiments, and the answers to the research              Unsafe Rust provides the necessary operations for low-level systems
questions based on the experimental results. We conclude with our            programming, such as arbitrary memory accesses with C-style
recommendations (see Section 6), threats to validity (see Section 7),        pointers, invoking system calls, calling foreign functions (usually C
related work (see Section 8) and conclusions (see Section 9).                functions), executing inline assembly instructions, eliding bounds
                                                                         2
     Is Rust Used Safely by Software Developers?                                                              ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea


            library1                                                   library4       declared unsafe
            fn foo() {                                                 unsafe fn qux(b) {
              x = MyObject::new() // x owns the object                   my_obj = (Obj) b                                                                                foo
              y = x               // Borrow occurs here




                                                                                                                                                  Optimistic
                                                                         return my_obj
              …                                                        }                                                                                             library2::bar
              library2::bar()
            }                                                                                                                                                     HasBaz::baz [Safe]
                                                                       library5             possibly unsafe                 Library1
                                                                       Impl HasBaz {
            library2                             library3     safe
                                                                         fn baz() {
            fn bar() {                          Impl HasBaz {                                                               Library2                                     foo
                                                                           unsafe {




                                                                                                                                                  Conservative
              // my_obj implements                fn baz() {                 my_global = 4                                                                           library2::bar
              // “HasBaz”                           a += 1                   qux()                               Library3              Library5
              HasBaz my_obj                       }                        }                                                                                     HasBaz::baz [Unsafe]
              my_obj.baz()                      }                        }
                                                                       }                                                               Library4
            }
                                      (a) Working example functions.                                          (b)  Library1        dependency(c) foo() extended call
                                                                                                              graph.                         graph.


           Figure 1: Working example of Rust functions in multiple libraries that are either safe, unsafe, or only appear safe.


     checks for performance, and accessing global static memory. To                          (5) Accessing a field of a union type.
     use any of these features, developers must mark the code with the                       Function baz() in Library5 contains an example of Unsafe Rust
     unsafe keyword. In Listing 1, unsafe is necessary for casting an                     operation: an assignment to a global variable my_global, enclosed
     address to a Rust struct for memory-mapped IO, and to use global                     in an unsafe block.
     variables to reference unique resources (e.g., COM1 port).                              An example of a possibly dangerous unsafe function call is the
                                                                                          mem::transmute() function used to coerce the contents of an ar-
 1   impl SerialPort {
 2       pub unsafe fn new(base: usize)                                                   bitrary memory location into a specific Rust type. This is necessary
 3               -> &'static mut SerialPort {                                             when raw data (such as from a network socket), but can easily vio-
             &mut *(base as *mut Self)
 4
 5       }
                                                                                          late type-safety if used improperly. Further, the mem::transmute
 6   }                                                                                    function also makes use-after-free memory errors possible when it
 7   pub static COM1: Mutex<SerialPort> =                                                 is used to extend the compiler calculated code bounds where the
 8       Mutex::new(SerialPort::new(0x3F8));
 9   pub unsafe fn init() {                                                               variable is live.
10       COM1.lock().init();
11   }                                                                                1   let mut hello = String::new();
                                                                                      2   let hello_ref: &mut String =
                                                                                      3       {let r: *mut String = &mut hello;
                           Listing 1: Transmute                                       4       unsafe { &mut *r }}; //Undefined Behavior! A second mutable reference
        Within an unsafe region, the compiler still checks the Safe Rust              5   hello.push_str("Hello ");
     types, but the operations listed above are permitted as well. Unsafe             6   hello_ref.push_str("world!");
                                                                                      7   println!("{:?}", hello);
     Rust does not grant the programmer complete freedom, but sub-
     verting overall system safety is certainly possible. Programmers
                                                                                                       Listing 2: Multiple Mutable References
     using Unsafe Rust are responsible for writing code free of safety
                                                                                             Using unsafe also makes mutable reference aliasing possible,
     violations and undefined behavior; however, what constitutes un-
                                                                                          leading to undefined behavior. In the Rust Listing 2, using simplified
     defined behavior is currently not well specified and can change
                                                                                          Rust syntax, two mutable references (hello and ref1) are created
     with different versions of the compiler. This situation makes safely
                                                                                          to the same memory location using an unsafe block. Different
     using Unsafe Rust difficult.
                                                                                          Rust versions are free to handle this differently, and do, as the
     2.4 Sources of Unsafe Rust                                                           Rust compiler version 1.36.0 and the Rust Mid-Level Intermediate
     There are several sources of Unsafe Rust, including unsafe opera-                    Representation Interpreter (Miri) version 0.1.0 handle code with
     tions, unsafe functions, and unsafe traits.                                          multiple mutable references to the same string differently. If the
                                                                                          code is compiled and executed, the output the programmer may
     2.4.1 Unsafe Operations A developer may directly use Unsafe                          expect ("Hello world!") is printed. However, when interpreted
     Rust by creating a code block labeled with the keyword unsafe,                       by Miri an error is displayed, as Miri also includes numerous checks
     which is required for the following operations:                                      of memory safety and that the aliasing rules for references are not
        (1) Calling a function marked unsafe, non-Rust external func-                     violated [17]. This suggests extensive care is required to use unsafe
            tion, or a compiler intrinsic (a function whose implementa-                   with maintainable and reliable code.
            tion is handled specially by the compiler).                                      If a block of code is marked unsafe, but does not actually contain
        (2) Dereferencing a C-style pointer.                                              any unsafe operations, the the compiler emits a warning message.
        (3) Accessing a mutable global variable.                                          We assume that the Rust developers remove necessary unsafe block
        (4) Using inline assembly instructions.                                           labels as a result.
                                                                                  3
ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea                                   Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa


                               Possibly Unsafe
                                                                              2.6 Rust Software Ecosystem
                      Safe                                                    Crates are the unit of compilation in Rust, meaning they compile
                                  Declared
                                  Unsafe                                      individually and the build output may be a software library or an
                                                                              binary application, depending on if the crate includes a main()
                                                                              function. Crate compilation is managed by Rust’s build and pack-
          Figure 2: Function annotation taxonomy.                             age manager cargo. Crates typically rely on cargo, making the build
                                                                              process standard in the Rust ecosystem and easing large-scale au-
                                                                              tomated analysis. Publicly available Rust crates, either libraries or
2.4.2 Unsafe Functions A Rust function definition may be la-                  applications, are typically published in crates.io, a central repository
beled with the unsafe keyword (for example the qux() function in              of Rust software.
Figure 1(a)) to signal to a caller that preconditions must be satisfied
or memory-safety errors may occur. Thus, an unsafe function may
contain only Safe Rust operations but still be marked unsafe and              3   Research Methodology
the compiler will not emit an warning because it is unable to dis-            In this section, we present the research questions that guide our
tinguish between programmer’s intent and a mistake. For example,              study and the selection criteria for the Rust code we explore.
a function that sets the length of a vector, Vector.set_length(),
will be marked unsafe despite only setting an internal field because          3.1 Research Questions
if it is called with a parameter larger than the capacity of the inter-       The main goal of our study is to gain insights on the practical use
nal buffer, future vector operations may access unallocated memory.           of Unsafe Rust by software engineers and the consequences for the
This example also demonstrates how memory safety errors may                   static safety guarantees of typical Rust code. The Rust compiler
occur in Safe Rust code after any use of Unsafe Rust.                         generates some code with unsafe operations (e.g., the PartialEq
    Conversely, a function containing unsafe operations may pro-              trait implementation of enumerations). Our analyses do not include
vide a safe interface. For example, array operations are commonly             compiler generated unsafe and consider only code written by a
implemented using C-style pointers and include their own safety               developer.
checks. In these cases Rust developers are expected to analyze the               RQ1: How much do developers use Unsafe Rust?
code manually to ensure safety is preserved.                                  We count the uses of the unsafe keyword for each of the four
                                                                              abstractions (block, function, trait, and trait implementation). The
2.4.3 Unsafe Traits A Rust trait [34] describes an abstract in-               motivation of RQ1 is to understand how often Rust developers
terface that types may implement. A trait may be declared unsafe              explicitly use unsafe in their code, and, thus, lose the static safety
if it contains any unsafe method or its implementations must sat-             guarantees.
isfy an invariant. An example from the Rust standard library is                  RQ2: How much of the Rust code is Unsafe Rust?
the trait Send, and any type that implements Send declares that               Unsafe Rust is necessary, but undermines the memory-safety and
it is safe to change the ownership of the type to another thread.             data-race freedom guarantees. Since Unsafe Rust may modify an
An implementation of an unsafe trait, must be marked unsafe.                  arbitrary memory location, any use of Unsafe Rust in any depen-
The programmer must ensure that the implementation satisfies the              dency compromises the static guarantees of the whole library. Rust
trait’s invariant, as the compiler cannot automatically check this.           libraries that do not contain Unsafe Rust operations, but call func-
                                                                              tions from external libraries that do, appear Safe Rust, but, in fact,
2.5   Function Taxonomy                                                       are not statically guaranteed safe. The goal of RQ2 is to determine
To explain our analysis procedure and results, we clarify terms that          what percentage of the Rust libraries lack full safety compiler guar-
we use to label Rust code with regards to its safety of functions.            antees.
Declared unsafe: A Rust function whose declaration includes                      RQ3: What Unsafe Rust operations are used in practice?
the unsafe keyword is declared unsafe. In Figure 1(a) the qux()               We locate and count the different types of Unsafe Rust operations in
function in Library4 is explicitly declared unsafe. A call to such a          unsafe blocks and declared unsafe functions separately. The moti-
function must be in an unsafe block or another declared unsafe                vation for RQ3 is to understand if interactions with C are the main
function. In our working example, the function baz() in Library5              source of Unsafe Rust. If yes, then most Unsafe Rust can be elimi-
calls qux() from an unsafe block.                                             nated by implementing the libraries in Rust. If not, then the reason
Possibly unsafe: A Rust function that may execute Unsafe Rust.                for Unsafe Rust lies within Rust code itself, and may be necessary
A function may be possibly unsafe if: (1) it is declared unsafe; (2) it       for achieving the desired performance or for implementing low-
contains an unsafe block; or (3) it calls a possibly unsafe function.         level libraries that interact with the operating system or directly
In Figure 1(a), the foo() function in Library1 is possibly unsafe             with hardware.
because it may use the baz() implementation from Library5.                       RQ4: What abstract binary interfaces (programming languages)
Safe: A Rust function with compile-time guarantees of memory-                 are used in the declared unsafe functions?
safety and data-race freedom is a safe function. The baz() function           The motivation for RQ4 is to understand if most called unsafe
in Library3 of Figure 1(a) is safe.                                           functions are from external libraries implemented in C or from
   The relationship among the different sets is presented in Figure 2.        other Rust libraries.
All Rust functions are either safe or possibly unsafe, and all declared          RQ5: Does the use of Unsafe Rust change over time?
unsafe functions are possibly unsafe.                                         The motivation for RQ5 is to understand if the increased attention
                                                                          4
Is Rust Used Safely by Software Developers?                                                  ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea


in the past year from the research community and the efforts by               order functions, as Rust does. Several algorithms for call graph con-
Rust language team to define and develop guidelines for use of                struction for other languages which have these features have been
unsafe changed the habits of the Rust developers.                             proposed with different trade-offs between precision and running
   RQ6: Why do Rust developers use unsafe?                                    time [5, 11, 25]. Our approach is similar to the one by Petrashko et
We surveyed Rust developers to understand their reasons for using             al. [25] in using the type information available at call site of not
unsafe.                                                                       only the Self type, but also of the static types of the parameters.
                                                                              Each node of the call graph is extended to contain not only the func-
3.2 Data Selection                                                            tion, but a list of generic type parameters and type substitutions
To understand unsafety in Rust, we analyze real-world, publicly               for those when available.
available Rust code. As the Rust tool chain provides robust sup-                  To generate a call graph, we use the Rust compiler to compile
port for libraries, Rust software extensively leverages community-            the crate to an intermediate representation of Rust known as MIR
provided libraries to create larger projects. As such, we target              (Middle Intermediate Representation). We then use the "control flow
our analysis towards the libraries that comprise the Rust software            graphs" of functions obtained directly from the MIR representation
ecosystem.                                                                    to run a context-sensitive analysis which uses type inference to
   To provide as wide of an analysis as possible, we include as many          find the precise functions that can be called. This analysis starts at
libraries (Rust crates) in our study as possible. However, as with any        the leaf terminal nodes of the control flow graph of a function. For
open ecosystem, there exists a “long-tail” of crates in Rust that are         each terminal leaf node of the type “function call” we use the type
small, largely unused projects, and these may not be representative           inference to determine the function call, given the type substitutions
of the ecosystem at large. Therefore, we also perform our analysis            in the calling context. If the method has no Self type or has a
on only the “popular” crates in our data set as defined as having             Self (this) type that it is statically known, then only one edge is
the most downloads from the central Rust repository to identify               introduced in the call graph in the actual implementation. If a node
any differences between the entire data set and the subset that is            with the calculated substitutions for generics of the called function
more frequently used.                                                         does not exist in the call graph, then we apply the substitutions
   Additionally, to compare crates contributed by the larger Rust             recursively and introduce new nodes in the call graph as needed. If
community with those developed by members of the core Rust                    the Self type (i.e., this) is still unknown, then an edge to a node
development team and Mozilla Research [32], we analyze the appli-             parameterized by the Self type is introduced. In building the call
cation Servo [3], a web browser engine from Mozilla. Servo, endemic           graph, when we encounter functions with generic type parameters,
of the larger Rust ecosystem, itself is implemented as a collection           we parameterize the call graph based on the generic type parameters
of about fifty discrete crates, and together with all its dependencies,       and instantiate a call with actual types available at the call site. The
compiling Servo involves compiling almost 400 different crates.               nodes in our call graph are functions together with a set of type
   We include all Servo crates and their external dependencies in             substitutions of the generic type parameters when statically known.
our analysis of Servo because they are implicitly vetted by the Servo             If the precise functions of the call graph cannot be resolved at
team to be included in one of the flagship Rust applications.                 compile-time (due to virtual dispatch and higher order functions),
                                                                              we split into two approximations, and create two versions of the
                                                                              call graph. We create a call graph of a conservative approximation
4   Approach                                                                  assuming that the unknown function is unsafe, and an optimistic
Our approach to answer the research questions is to identify all oc-          approximation of a call graph that assumes the potential function
currences of unsafe in Rust codebases, and then determine how the             is safe.
unsafeness propagates to caller functions. First, we parse Rust code              For efficiency, our call graph construction for a function termi-
from libraries to identify the keyword unsafe in blocks, functions,           nates when any unsafe usage is found, as the original function
traits, and trait implementations in a single crate, which can be ana-        must now be marked possibly unsafe and further calls will have no
lyzed independently of other crates. Next, we develop two versions            impact. Similarly, we stop when we reach a virtual call or a function
of an extended call graph for each library; one that is optimistic            pointer as our two approximations cover the two possible cases.
and one that is conservative in terms of whether a polymorphic                    We generate extended call graphs for every function in every
function is safe or unsafe. Finally, we develop an algorithm to an-           crate, enabling this approach to work even for libraries which do
alyze the extended call graph to propagate the unsafe condition               not contain a main function. These extended call graphs are for
through the call graph to determine if a function is safe or possibly         individual libraries, and function calls to other libraries are explicitly
unsafe. In this way, we can identify libraries that appear safe but           marked. In our analysis, we can then combine the extended call
actually have potentially unsafe conditions that have propagated              graphs as needed without having to generate the call graph multiple
up the call chain. Sources of imprecision in our analysis include             times. Note, we stop our call graph construction at calls into the
potential inclusion of dead code.                                             Rust standard library. If the functions are declared unsafe we mark
                                                                              them as unsafe; however, we consider the standard library trusted
4.1 Extended Call Graph                                                       and consider all other functions safe, even if their implementations
In general, a program call graph [28] is a directed graph with a              contain uses of unsafe.
node for each program function and an edge (f , д) for one or more                To aid future reproducibility studies and extensions of our work,
potential calls of д from the function f . This simple construction           we publish all the code used for this paper at https://github.com/
needs to be expanded if the language has polymorphism and high
                                                                          5
ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea                                 Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa


ananevans/icse2020, including the call graph construction available         assumes it is unsafe. To determine unsafety in the conservative
in the unsafe-analysis/src/implicit_unsafe/rta.rs folder.                   case, we start with the unknown function HasBaz::bar() in our
                                                                            worklist since it is marked possibly unsafe. We then find all callers, in
4.2   Analysis on the Call Graph                                            this case library2::bar(), mark them as possibly unsafe, and add
                                                                            them to the worklist. Iterating, we determine foo() calls bar()
  Data: call graph                                                          and mark foo() possibly unsafe. This tells us that even though
  Result: list of possibly unsafe functions                                 foo() appears safe, in a conservative analysis it may in fact call
  for all function definitions do                                           code which is not statically checked by the compiler.
      if function has unsafe in body then
           add function to possibly unsafe list;                            5   Experiments and Results
           add function’s call graph node to worklist
                                                                            We start with describing the experimental setup in Section 5.1
      end
                                                                            and continue with the detailed description of the data sets used
  end
                                                                            in our experiments (Section 5.2). We conclude with the results in
  reverse the call graph;                                                   Section 5.3.
  while worklist not empty do
      current_func = pop the first element of the worklist for              5.1 Experimental Setup
       each neighbor of current_func do                                     We execute the experiments using version “nightly-2018-09-11” of
           if neighbor not in possibly unsafe list then                     the Rust compiler on Ubuntu 18.04. The 2019 version of the most
               add function to possibly unsafe list;                        downloaded data set is compiled with version “nightly-2019-07-01”.
               add neighbor to worklist
           end                                                              5.2 Data Sets
      end                                                                   Our data selection criteria are presented in Section 3.2. Here we
  end                                                                       present the libraries actually included in our study and describe
            Algorithm 1: Analysis on Call Graph                             reasons why we are unable to include all Rust crates in our data
                                                                            set.
   After the extended call graphs are constructed, we use them                 At the start of our study, September, 2018, there were a total of
to identify potentially unsafe functions in the Rust libraries. Our         18,478 crates registered with the central Rust software repository.
approach starts at the bottom of the call graph with all functions          We eliminated all of the crates that could not compile or was no
that contain unsafe blocks. We then work back up the call graph             longer available. Note that Rust is under active development, and
to identify functions that may call any of these initial functions.         a particular crate may compile with one version of the compiler
Our goal is to mark every function as either safe or possibly unsafe.       but not another. Afterwards, our data set contains 15,097 crates,
   We start with a worklist initialized with all functions that con-        which represent 81% of the total registered crates, and 97% of the
tain an unsafe block in their body. Note that we do not need to             registered crates that contain some Rust code and are syntactically
consider the declared unsafe functions because they will necessarily        correct.
be called from within an unsafe block in another function. We iter-            To obtain a “popular” subset, we fetch the per-crate downloads
atively remove a function from the worklist, and perform a reverse          numbers from crates.io and select the most downloaded crates that
propagation on the extended call graph to mark all of its callers as        account for ninety percent of the downloads from crates.io. These
possibly unsafe, and then add them to the worklist. The algorithm           500 or so crates form a group we call most downloaded. From these
completes when the worklist is empty, and all functions that have           most downloaded crates we were able to compile 473 crates.
not been marked possibly unsafe are deemed safe.                               To create a group of perhaps “higher quality” crates, we use the
                                                                            crates that comprise the application Servo, a web browser engine
4.3 Example                                                                 from Mozilla, as another group. Servo is implemented as a collection
Consider our working example from Figure 1 and assume we are                of approximately fifty crates and together with all its dependencies,
analyzing the safety of Library1. The library dependency graph              it comprises almost four hundred crates. As Servo is created by
is given in Figure 1(b) and shows the order of compilation and              many of the same developers actively developing the Rust language
analysis in building the extended call graph. Function foo() in             itself, we posit that it represents a more expertly developed piece of
Library1 calls a function bar() in Library2 and thus an edge is             Rust software. Note that the crates in this group do overlap partially
placed between Library1 and Library2. Library2 specifies libraries          with the most downloaded and complete groups.
3 and 5 as dependencies, making the call to polymorphic function               Finally, our fourth group contains the same crates as in the most
baz() ambiguous. Finally, Library5 contains a call to qux() and             downloaded group, but with the crate’s contents as it existed in
therefore Library4 is a dependency of Library5.                             June 2019 on crates.io, approximately ten months after the first
   The extended call graph with external libraries merged is shown          analysis.
in Figure 1(c). Because bar() calls the polymorphic function baz(),
we cannot precisely determine the exact call graph and split into an        5.3 Results
optimistic call graph that assumes the unknown implementation of            We provide answers the research questions from Section 3.1 based
HasBaz::baz() is in fact safe, and a conservative call graph that           on the results of our experiments.
                                                                        6
Is Rust Used Safely by Software Developers?                                                                  ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea

                     crates.io       Most        Servo
                                                                                                    100.0%
   Abstraction          (%)    Downloaded (%)     (%)
   Any                 29.4           52.5        54                                                95.0%




                                                                                Percent of Crates
   Blocks              27.5           47.7        51.7
   Declared Unsafe                                                                                  90.0%
                       17.1           47.7        39.7
   Functions                                                                                        85.0%
   Traits                1.2           4.2         4.4
   Trait                                                                                            80.0%
                         5.9          14.8        18.2
   Implementations
                                                                                                    75.0%
Table 1: Percentage of Rust crates with Unsafe Rust based
on abstraction type.                                                                                70.0%
                                                                                                    68.1%




                                                                                                               0
                                                                                                              10
                                                                                                              20
                                                                                                              30
                                                                                                              40
                                                                                                              50
                                                                                                              60
                                                                                                              70
                                                                                                              80
                                                                                                              90
                                                                                                             100
                                                                                                             110
                                                                                                             120
                                                                                                             130
                                                                                                             140
                                                                                                             150

                                                                                                                                                            167
                                                                                                                     Declared Unsafe Functions
                    100.0%
                    95.0%
                                                                                Figure 4: RQ1: Cumulative Distribution of Declared Unsafe
                    90.0%
Percent of Crates




                                                                                Functions
                    85.0%
                    80.0%
                    75.0%                                                       Functions: Figure 4 shows the cumulative distribution of declared
                    70.0%                                                       unsafe functions per crate for the crates.io set (in black) and most
                    65.0%                                                       downloaded crates (in dark grey), capped at 99%. A very small
                    60.0%                                                       number of crates have thousands of declared unsafe functions. These
                    55.0%                                                       crates are typically low-level support crates for embedded devices
                    50.0%                                                       or C library bindings.
                                                                                    As in the unsafe blocks case, the per-crate number of declared
                             0

                                 50

                                      100

                                              150

                                                    200

                                                          250

                                                                300




                                                                      389




                                            Unsafe Blocks                       unsafe functions is small with 90% of the crates containing fewer
                                                                                than two declared unsafe functions.
                                                                                    While there is a compiler warning if a block is unsafe without
       Figure 3: RQ1: Cumulative Distribution of Unsafe Blocks
                                                                                using any unsafe operation, no such warning is generated for func-
                                                                                tions. One use of an unsafe function is to warn the library user
                                                                                that preconditions must be satisfied, otherwise memory corruption
5.3.1 RQ1: How much do developers use Unsafe Rust? Ta-                          or a data-race may occur. We performed an additional analysis on
ble 1 shows the percentages of the crates use unsafe, broken down               the declared unsafe functions to determine if the function uses an
by the type of abstraction. Overall, 29% of crates directly include             unsafe operation. From all the crates with at least one declared
some sort of Unsafe Rust in them. More popular crates are more                  unsafe function, 84% of all crates.io and 71% of most downloaded
likely to use unsafe as 52.5% of the most downloaded crates contain             crates, all the declared unsafe functions are entirely Safe Rust. We
Unsafe Rust. Of these, only a few crates (about 15-17%) explicitly              identity two possible reasons for which a declared unsafe function
mark functions as unsafe (which then propagate the unsafe to                    executes no unsafe operations: (1) the library developer performed
other portions of code). The unsafe trait and trait implementations             a careful analysis and determined that preconditions are necessary
are used by only a relatively small number of crates. Compared to               to prevent memory corruption and data races; or (2) the unsafe
the larger ecosystem, the crates that comprise the Servo project are            attribute was incorrectly placed.
more likely to use Unsafe Rust.                                                 Traits: Declaring an unsafe trait is rare in the Rust ecosystem, with
Blocks: Figure 3 shows the cumulative distribution of unsafe blocks             only a little over one percent of crates making use the feature.
per crate, with crates.io set in black and the most downloaded crates           Implementations: As seen in Table 1, only six percent of all crates
in grey, and the maximum value capped at 99.5% of the crates for                provide an implementation of an unsafe trait. Almost 40% of those
clarity. The long tail of the CDF (Cumulative Distribution Function)            are of two traits from the Rust standard library: Send (28%) and
exists primarily because of autogenerated code, either from C to                Sync (13%). These traits are fundamental for Rust’s concurrency.
Rust translators, hardware description files, or “safe” Rust wrappers           They do not have any declared methods, and they are used as a
around C library functions.                                                     declaration by the programmer that the objects implementing them
   The number of unsafe blocks per crate is small for the majority              are safe to change ownership to another thread (Send) or can be
of the crates, more than 90% of the crates have fewer than ten                  shared between threads (Sync).
unsafe blocks. The most downloaded crates use unsafe more often                 Summary: Unsafe Rust is used in a little more than a quarter of
than all crates. This occurs because these crates are more likely to            all crates, but the number of explicit unsafe uses per crate is small
use unsafe to extract performance optimizations, and they often                 for most crates. Despite the potential issues with using unsafe, the
exist to help interface with existing C libraries.                              most downloaded crates are more likely to use unsafe than the
                                                                            7
ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea                                   Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa

                                 crates.io      Most                                              Dependencies           No Unsafe in
                  Analysis          (%)    Downloaded (%)                                         With Unsafe (%)       Dependencies (%)
                  Conservative       44.8        38.9                               Crate With
                  Optimistic         53.8        43.9                                 Unsafe            23                12
           Table 2: Percentage of Crates With Only Safe Functions                   No Unsafe
                                                                                     in Crate           38                27
                                                                                       Table 3: Unsafe in Crate and Dependencies

average crate. In general, developers tend to avoid exposing the
unsafety to other code by rarely marking functions as unsafe and                                     crates.io        Most             Servo
typically avoiding unsafe traits. However, the crates for Servo use                                     (%)       Downloaded (%)        (%)
unsafe functions and unsafe traits two or three times as frequently               Unsafe
as general crates, which is consistent with the growing preference                                  79.3          66.9         74.9
                                                                                  Function Call
in the Rust community that unsafe is encapsulated at a higher                     Dereference
level than individual functions. That is, exposing unsafe functions                                 16.2          19.5         21.5
                                                                                  C-Style Pointer
is acceptable as long they are eventually enclosed within a safe                  Global Variable    3.7          11.1          0.21
interface.
                                                                                     Table 4: Unsafe Operations in Unsafe Blocks
5.3.2 RQ2: How much of the Rust code is Safe Rust? Table 2
presents the percentage of crates containing only safe functions,
when the unsafe generated by compiler is ignored and the standard                                    crates.io        Most             Servo
Rust library is considered entirely safe.                                                               (%)       Downloaded (%)        (%)
   Figure 5 shows the cumulative distribution of the possibly unsafe              Unsafe
functions for all crates, capped at 95%. The optimistic analysis is                                 89.2           64.0        78.2
                                                                                  Function Call
shown in light grey and the conservative analysis is shown in black.
                                                                                  Dereference
The difference between the results of the two analyses is about 10%                                  6.7           26.0        19.1
                                                                                  C-Style Pointer
for crates with a small number of possibly unsafe functions, and gets
                                                                                  Global Variable    3.9            9.8         1.1
smaller than 1% for crates with tens of possibly unsafe functions.
                                                                                    Table 5: Unsafe Operations in Unsafe Functions

                    100.0%

                    90.0%                                                     Summary: While only less then one third of crates directly use
Percent of Crates




                                                                              unsafe, over half of crates include Unsafe Rust somewhere in the
                    80.0%
                                                                              aggregate source code once dependencies are considered. This illus-
                    70.0%                                                     trates the difference between Rust’s perceived safety and what is
                                                                              actually statically guaranteed. This also burdens developers trying
                    60.0%                                                     to understand their software’s exposure to Unsafe Rust as 38% of
                                                                              crates appear to avoid unsafe, yet contain it in their dependencies.
                    50.0%
                    47.3%                                                     5.3.3 RQ3: What Unsafe Rust operations are used? Table 4
                                                                              and Table 5 present the most frequent Unsafe Rust operations in
                    38.9%
                                                                              unsafe blocks and declared unsafe functions, respectively. Only
                             0

                                 10

                                       20

                                            30

                                                 40

                                                      50

                                                           60

                                                                70



                                                                     86




                                                                              the Unsafe Rust operations present in more than 1% of crates are
                                      Possibly Unsafe Functions               displayed.
                                                                                 Primarily, a function may be declared unsafe because it contains
Figure 5: RQ2: Declared Safe and Possibly Unsafe Functions                    Unsafe Rust operations that are not enclosed in an unsafe block.
Distribution                                                                  Other reasons for declaring a function unsafe are: it is imposed by
                                                                              a trait, it has a precondition that must be satisfied, and it has a
   To better understand the difference between the perceived safety           C-Style pointer argument that can be invalid. These cases are not
(more than two thirds of the crates do not contain an unsafe ab-              directly using any Unsafe Rust operations, and thus were excluded
straction, Table 1) and the static safety guarantees (less one third of       from the analysis.
crates are entirely Safe Rust) of Rust, we inspected crate dependen-             We observe that calls to declared unsafe functions are a majority
cies. On average, across all crates in our dataset, a crate depends on        of the Unsafe Rust operations used. The most downloaded crates
twelve other crates. As shown in Table 3, only 27% of total crates            and Servo use C-style pointers with greater frequency. One possible
contain no Unsafe Rust and only use dependencies which contain                explanation is that these applications interface with C libraries for
no Unsafe Rust. Importantly, 38% of crates include no unsafe in               speed or because those libraries are not yet available in Rust.
their own implementation, but rely on dependencies which do use               Summary: Calls to unsafe functions are the majority of the Unsafe
unsafe.                                                                       Rust operations. We need to understand if the functions are unsafe
                                                                          8
Is Rust Used Safely by Software Developers?                                                             ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea


                                   All       Most Downloaded                                                     Same Increase Decrease
                                                                                                    Abstraction
                                         66.6%
                                                                                                                  (%)      (%)       (%)
                                                                                                  Blocks           82       10         8
                                                                              53.6%
                                                                                                  Functions        87        7         6
Percentage




                                                      42.2%                                     Table 6: Unsafe Use in Most Downloaded Crates

                21.4%




                            4.2%
                                                                  8.7%
                                                                                          5.3.5 RQ5: Does the use of Unsafe Rust change over time?
                                                                                          To answer RQ5, we count the number of unsafe blocks and func-
                                                                                          tions in the same set of most downloaded crates at two different




                                                                         ic
                        C




                                                  t
                                                 us




                                                                      ns
                                                                                          time points: September 2018 and June 2019. Since the Rust compiler
                                            R




                                                                   tri
                                                                  tIn
                                                              us
                                                              R                           API changes frequently, we modified the Rust plugin to be able to
                              Abstract Binary Interface                                   compile updated crates. However, unsafe is counted in the same
                                                                                          way, despite using two different versions of the tool.
                                                                                             A majority of crates (over 80%) contained the same number of
             Figure 6: RQ4: Calls of Declared Unsafe Functions
                                                                                          unsafe blocks and functions in both versions. Of the crates that
                                                                                          did change their unsafe usage, approximately half increased while
                                                                                          the other half decreased.
                                                                                          Summary: We conclude that there are no significant trends in
because they are implemented in C or they are Rust functions. This                        the use of unsafe over a period of ten months, with only a small
is investigated in the next research question.                                            increase in the use of unsafe.

5.3.4 RQ4: What type of unsafe functions are called? Fig-                                 5.4 RQ6: Why do Rust developers use unsafe?
ure 6 presents the distribution of the abstract binary interface of                       To answer the RQ6 research question, we created a survey and
the declared unsafe functions called from both declared unsafe func-                      posted it on the Rust Subreddit [1], and collected data from twenty
tions and unsafe blocks.                                                                  respondents. The survey asked why they use unsafe and how they
   Among all crates from crates.io the most frequent calls are to                         ensure correctness when using unsafe.
Rust unsafe functions (65%), followed by calls to C functions (22.5%)                        The first question asked Rust developers to select one or more
and Rust intrinsics (special functions made available by the Rust                         reasons for why they use unsafe in their code. A majority (55%) in-
compiler). Among the Rust unsafe calls, 47.6% are calls to the Rust                       dicated the use Unsafe Rust for higher performance, with Safe Rust
Core Library. Of these unsafe functions in Core, 36.4% are of func-                       being too restrictive as the next most common reason (40%). The
tions in the ptr module used to manually manage memory through                            other reasons selected include: the Safe Rust alternative is too ver-
C-style(raw) pointers and 40% are calls of functions that are unsafe                      bose or complicated (25%), needed to make the code compile (10%),
wrappers to SIMD instructions and architecture-specific intrinsics.                       and faster to write code with Unsafe Rust (5%). Further, respondents
Thus, a significant source of Unsafe Rust is caused by the defini-                        provide other reasons, including: implementing fundamental data
tion and use of C-style pointers, either by direct dereferencing or                       structures, custom concurrency primitives and system calls, inter-
by calling unsafe functions from the core::ptr module that allow                          action with specialized hardware, and integration with C or other
pointer arithmetic and access to the values stored at the pointer                         languages.
location.                                                                                    To expand on the general reasons for using Unsafe Rust, the next
   The most downloaded crates use the Rust intrinsics much more                           question asked what operations the developers use that require the
frequently because intrisics provide operations used for I/O mem-                         unsafe keyword. Of the respondents, 45% report using unsafe to
ory access and common atomic operations. The most downloaded                              call a non-syscall external C function, 25% to call an unsafe Rust
crates include more libraries that extend Rust with I/O access and                        function, 25% to work with C-style pointers, and 5% to work with
concurrency primitives. The very small number of C-style calls                            SIMD intrinsics. No respondents selected to perform a system call
in most downloaded crates is explained by the fact that the most                          or to access a static variable.
downloaded crates are more likely to contain crates that are wrap-                           The final question asked the Rust developers for the steps they
pers for commonly used libraries. From all the calls to Rust unsafe                       take to increase their confidence that their Unsafe Rust code is
functions, 47.2% are to function from the Rust Core Library of which                      correct. Most respondents (65%) indicated they read the code very
27% are to core::ptr functions. The wrappers to SIMD instructions                         carefully, until they convince themselves that the code is correct.
are significantly used, as the calls to Rust intrinsics are much higher.                  Another frequently used technique (55% selected this option) is
Summary: Calls to C functions are not the majority of the calls                           adding runtime checks to prevent memory corruption. Half of the
to unsafe functions. Implementing some C libraries in Rust, will                          respondents write more unit tests for the function or method that
remove some Unsafe Rust operations, but the majority of unsafe                            uses unsafe Rust. Other steps developers take to increase confidence
function calls are to Rust functions and Rust intrinsics. We conclude                     in the correctness of their unsafe code include: having discussions
that the unsafe code is not encapsulated behind the public interface                      with experienced Rust developers in person or online, reading the
and the developers use the unsafe function when available.                                documentation and Rust books, creating theoretical proofs, using
                                                                                      9
ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea                                     Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa


available test generation, running fuzzing and analysis tools, and                  The Rust library ecosystem tool, crates.io, should also help alert
using Miri [17].                                                                developers to uses of unsafe. Anecdotally, over 100 unsound uses
Summary: We conclude that the Rust developers use Unsafe Rust                   of unsafe in a popular Rust web framework, Actix [31], were only
mostly because Safe Rust is too restrictive and to achieve better per-          discovered and partially fixed by the Rust community after an
formance, but they are aware of the potential challenges when using             online post by a concerned user [37]. Even a year later, the library
unsafe and they use more care, test more thoroughly, and deploy                 still contains uses of unsafe, with soundness concerns still present.
tools and analysis to increase confidence in their code correctness.            Motivated by this example, we propose the following changes to
                                                                                the crates.io interface: i) a new tag or badge for crates that include
                                                                                Unsafe Rust; ii) a dependency tree for each library with the crates
6   Towards a Safer Rust                                                        that use Unsafe Rust clearly marked; and iii) a list of code reviews
                                                                                for any Unsafe Rust. Previous research established that code review
Our analysis shows that while publicly available Rust libraries rarely          in open source software communities is common and successful in
use the unsafe keyword (even very popular libraries), most of them              eliminating a large number of errors [7, 26, 27]. Alami et al. [2] find
are still not Safe Rust, because of unsafe use in dependencies.                 that open source software developers develop a mature attitude
    For Rust users that require more robust and reliable checking               to negative feedback and improve their code through a cycle of
of their code, future improvements to the Rust compiler or the                  review, rejection, and improvement.
associated tool infrastructure are required. A particularly ambitious               The implementation of our proposals will help the community
mechanism would be to require an automatic correctness proof (in                inspect libraries and help guide new Rust developers on what Unsafe
the style of Verifiable C [4]) for every use of unsafe. Jung et al. [18]        Rust code to trust.
used this approach to formally prove the correctness of a handful
of Rust functions. The Rust functions were manually translated
to a simplified version of the language, called λ Rust and using                7   Threats To Validity
the Iris framework [19] the authors provided machine-checked                    The internal validity threats we identify are confounding factors
proofs of correctness of several libraries and uncovered a previously           and sampling bias. The Unsafe Rust segments we identify may be
unknown soundness bug in Rust. This approach is unlikely to scale               in unreachable or dead code that may not ever be executed for a
to all Rust code, but may be feasible for the standard library or other         particular library. Future work can use additional static analysis
commonly used libraries to help minimize the amount of code that                tools to identify uses of unsafe that reside in unreachable code.
is not checked for safety.                                                      Sampling bias is also a possibility. We intended to be inclusive in the
    Another more feasible short-term approach is to address only                libraries we analyze, and we believe the way we segmented crates
unsafe function calls, which is the most common use of unsafe.                  is makes our analysis representative of the larger Rust ecosystem.
Here, programmers could annotate function calls with suitable pre-              The crates included in our study are the ones that could be compiled
and post-conditions they expect to hold when calling the func-                  on an Ubuntu operating system, and doe not include crates that
tion. Various static and dynamic checks then check the code to                  need Windows and MacOS libraries.
ensure the conditions are satisfied. This annotation would enable                  Rust is under active development and it is possible that program-
programmers to safely use functions that are intrinsically unsafe               ming style and use of Unsafe Rust changes in time. We identify this
(i.e., configuring a hardware peripheral) or optimize performance               as an external validity threat. The percentage of safe libraries may
with unsafe. However, this approach does add an additional burden               change when considering only “newer” libraries.
for programmers and, possibly, run time overhead.
    Another approach is to aid programmers in reasoning about
the safety of any external code they use. Rust already includes a               8   Related Work
compiler directive that generates an error if unsafe is used, yet               We present throughout the paper related work relevant to the mo-
we discovered a library that included the directive but still used              tivation and techniques used. In this section, we focus on related
unsafe by overriding it at the function-level. Strengthening tools              work that investigates how software engineers use various features
so programmers have automated checks on unsafe code in depen-                   in other programming languages.
dencies would significantly help programmers manually audit their                  C/C++ language features: Eyolfson et al. analyze the use of
codebase to better enable “pragmatic safety”. For example, the Rust             const annotations in seven medium and large open source C++
compiler should be able to identify functions in a given library that           projects and find that software developers use correct annotations
are implicit safe, and print a possible call chain that includes calls          in most cases, missing immutability labels in only 6% of the unanno-
to Unsafe Rust. Implementing this in the compiler would make this               tated methods [13]. In Rust, the variables are immutable by default,
tool easy to use, and it would remain up to date as the internal                and the programmers opt-in by labeling a variable as mutable. This
compiler API changes.                                                           study suggests that C++ programmers are using language features
    The development of the above mentioned tools requires a defini-             to write software with fewer errors. In our study, we observe the
tion of what Unsafe Rust actually means and which behaviors are                 same tendency as the majority of crates are free of direct uses of
undefined. Despite Rust 1.0 being around for four years, the guide-             Unsafe Rust.
lines on how to write unsafe Rust code are still preliminary [35].                 Casalnuovo et al. [9] studied many C/C++ projects to measure
As this effort progresses, developing tools around Unsafe Rust will             the programmers’ use of assert. They find that a majority of the
be more manageable and maintainable.                                            projects use more than a minimal number of assert statements.
                                                                           10
Is Rust Used Safely by Software Developers?                                                  ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea


The use increases with the length of time the developer is directly            on their dependencies. We conduct a number of experiments on Rust
involved with that function. If Rust developers behave similarly,              code, using the results to answer our research questions. Across our
then over time the number of assertion statements in Rust code                 dataset, we find that a majority of crates include functions which
should increase, helping to protect Unsafe Rust operations. However,           are possibly unsafe. We also find that unsafe function calls are the
developers may instead view assertions as not needed in Rust.                  most common use of unsafeness, and the unsafeness is through
   Undefined behavior can be particularly problematic in code as the           library dependencies rather than through the use of the keyword
compiler can correctly generate machine code that does not match               unsafe. Perhaps nonintuitively, we find that the most downloaded
the programmer’s expectations. As with the case of using undefined             crates have more unsafe code than other crates. From these results,
integer overflow to check a buffer’s length [12], undefined behavior           it is difficult for users to know if their code is safe, and thus we
can lead to security vulnerabilities. Wang et al. [38] implement a             present recommendations for helping users understand when they
tool to detect undefined behavior based on differences resulting               are using Unsafe Rust in their software.
from the compiler optimization level used. They find that 40% of
the 8,575 Debian Wheezy packages that contain C/C++ code exhibit
this behavior, and identify 160 real bugs in production open source
code.
   Further, understanding undefined behavior can be difficult, as
Memarian et al. [23] demonstrate by surveying over 200 experienced
C developers and asking 85 difficult questions about the semantics
of C. The researchers conclude that in many instances there was
no agreement among the participants on the actual code behavior.
As Unsafe Rust can easily introduce undefined behavior into Rust
code, these case studies suggest Unsafe Rust should be used very
cautiously.
   Java: Java is a safe language, but the runtime provides a “back-
door” that permits the circumvention of Java’s safety guarantees to
enable high-performance systems-level code. Mastrangelo et al. [22]
perform a large-scale analysis of Java bytecode to determine how
these unsafe capabilities are used in real world. The authors deter-
mine that 25% of the Java code analyzed depends on unsafe Java
code. One explanation for why the 25% of the analyzed Java code
lacks safety because of use of unsafe API may be that it is not an
integral part of the language, like in Rust, and it is not exposed by
the java standard libraries. Huang et al. [16] study unsafe crash
patterns and implement a bytecode-level transformation that intro-
duces runtime checks to help diagnose and prevent some memory
errors caused by the use of the unsafe API.
   Swift: Swift, introduced by Apple, is intended to replace Objective-
C, introduced a new error handling mechanism using exceptions
that is not present in Objective-C. Cassee et al. [10] execute a large-
scale study to identify if Swift developers switched to the new
mechanism. They find that about half of the projects do not use
the new error handling mechanism. Of the projects that do, some
follow some guidelines, but most do not follow the more complex
error-handling recommendations. This fallback to known patterns
may also exist in Rust systems code, as many Rust systems develop-
ers likely have experience writing C. That is, Rust developers may
use Unsafe Rust to enable using the C-style code patterns they are
familiar with. Further studies are required to understand if this is
the case.


9   Conclusions
In this research, we explore whether Rust is, in fact, being used to
ensure memory safety and avoid concurrency bugs. To answer a
number of research questions, we develop a technique to construct
an extended call graph for Rust and an analysis that determines
whether functions possibly include Unsafe Rust or not, depending
                                                                          11
ICSE ’20, May 23–29, 2020, Seoul, Republic of Korea                                                        Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa


References                                                                                            Conference on Object-Oriented Programming, Systems, Languages, and Applications
                                                                                                      (OOPSLA 2015). ACM, New York, NY, USA, 695–710.
 [1] 2020. Rust Subreddit. https://www.reddit.com/r/rust/. (2020).                               [23] Kayvan Memarian, Justus Matthiesen, James Lingard, Kyndylan Nienhuis, David
 [2] Adam Alami, Marisa Leavitt Cohn, and Andrzej Wasowski. 2019. Why Does                            Chisnall, Robert N. M. Watson, and Peter Sewell. 2016. Into the Depths of
     Code Review Work for Open Source Software Communities?. In Proceedings of                        C: Elaborating the De Facto Standards. SIGPLAN Not. 51, 6 (June 2016), 1–15.
     the 41st International Conference on Software Engineering (ICSE ’19). IEEE Press,                https://doi.org/10.1145/2980983.2908081
     Piscataway, NJ, USA, 1073–1083.                                                             [24] Aurojit Panda, Sangjin Han, Keon Jang, Melvin Walls, Sylvia Ratnasamy, and
 [3] Brian Anderson, Lars Bergstrom, Manish Goregaokar, Josh Matthews, Keegan                         Scott Shenker. 2016. NetBricks: Taking the V out of NFV. In Proceedings of the 12th
     McAllister, Jack Moffitt, and Simon Sapin. 2016. Engineering the Servo Web                       USENIX Conference on Operating Systems Design and Implementation (OSDI’16).
     Browser Engine Using Rust. In Proceedings of the 38th International Conference on                USENIX Association, Berkeley, CA, USA, 203–216.
     Software Engineering Companion (ICSE ’16). ACM, New York, NY, USA, 81–89.                   [25] Dmitry Petrashko, Vlad Ureche, Ondřej Lhoták, and Martin Odersky. 2016. Call
 [4] Andrew W. Appel, Robert Dockins, Aquinas Hobor, Lennart Beringer, Josiah                         Graphs for Languages with Parametric Polymorphism. In Proceedings of the 2016
     Dodds, Gordon Stewart, Sandrine Blazy, and Xavier Leroy. 2014. Program Logics                    ACM SIGPLAN International Conference on Object-Oriented Programming, Systems,
     for Certified Compilers. Cambridge University Press, New York, NY, USA.                          Languages, and Applications (OOPSLA 2016). ACM, New York, NY, USA, 394–409.
 [5] David F. Bacon and Peter F. Sweeney. 1996. Fast Static Analysis of C++ Virtual              [26] P. Rigby, B. Cleary, F. Painchaud, M. Storey, and D. German. 2012. Contemporary
     Function Calls. In Proceedings of the 11th ACM SIGPLAN Conference on Object-                     Peer Review in Action: Lessons from Open Source Development. IEEE Software
     oriented Programming, Systems, Languages, and Applications (OOPSLA ’96). ACM,                    29, 6 (Nov 2012), 56–61.
     New York, NY, USA, 324–341.                                                                 [27] P. Rigby, D. German, and M. Storey. 2008. Open source software peer review
 [6] Abhiram Balasubramanian, Marek S. Baranowski, Anton Burtsev, Aurojit Panda,                      practices. In 2008 ACM/IEEE 30th International Conference on Software Engineering.
     Zvonimir Rakamarić, and Leonid Ryzhyk. 2017. System Programming in Rust:                         541–550.
     Beyond Safety. In Proceedings of the 16th Workshop on Hot Topics in Operating               [28] B. G. Ryder. 1979. Constructing the Call Graph of a Program. IEEE Trans. Softw.
     Systems (HotOS ’17). ACM, New York, NY, USA, 156–161.                                            Eng. 5, 3 (May 1979), 216–226.
 [7] Moritz Beller, Alberto Bacchelli, Andy Zaidman, and Elmar Juergens. 2014. Mod-              [29] Dokyung Song, Julian Lettner, Prabhu Rajasekaran, Yeoul Na, Stijn Volckaert,
     ern Code Reviews in Open-source Projects: Which Problems Do They Fix?. In                        Per Larsen, and Michael Franz. 2018. SoK: Sanitizing for Security. CoRR
     Proceedings of the 11th Working Conference on Mining Software Repositories (MSR                  abs/1806.04355 (2018). arXiv:1806.04355 http://arxiv.org/abs/1806.04355
     2014). ACM, New York, NY, USA, 202–211.                                                     [30] L. Szekeres, M. Payer, T. Wei, and D. Song. 2013. SoK: Eternal War in Memory. In
 [8] Kevin Boos and Lin Zhong. 2017. Theseus: A State Spill-free Operating System.                    2013 IEEE Symposium on Security and Privacy. 48–62.
     In Proceedings of the 9th Workshop on Programming Languages and Operating                   [31] The Actix Team. 2018. Actix. https://github.com/actix/actix. (2018).
     Systems (PLOS’17). ACM, New York, NY, USA, 29–35.                                           [32] The Mozilla Research Team. 2020. Mozilla Research. https://research.mozilla.org/.
 [9] Casey Casalnuovo, Prem Devanbu, Abilio Oliveira, Vladimir Filkov, and Baishakhi                  (2020).
     Ray. 2015. Assert Use in GitHub Projects. In Proceedings of the 37th International          [33] The Redox Team. 2018. Redox. https://www.redox-os.org/. (2018).
     Conference on Software Engineering - Volume 1 (ICSE ’15). IEEE Press, Piscataway,           [34] The Rust Team. 2018. The Rust Language Reference. https://doc.rust-lang.org/
     NJ, USA, 755–766.                                                                                reference/index.html. (2018).
[10] Nathan Cassee, Gustavo Pinto, Fernando Castor, and Alexander Serebrenik. 2018.              [35] The Rust Team. 2018. Unsafe Code Guidelines Reference. https://rust-lang.github.
     How Swift Developers Handle Errors. In Proceedings of the 15th International                     io/unsafe-code-guidelines/. (2018).
     Conference on Mining Software Repositories (MSR ’18). ACM, New York, NY, USA,               [36] The Rust Team. 2019. Unsafe Code Guidelines. https://github.com/rust-lang/
     292–302. https://doi.org/10.1145/3196398.3196428                                                 unsafe-code-guidelines. (2019).
[11] Jeffrey Dean, David Grove, and Craig Chambers. 1995. Optimization of Object-                [37] tx4414. 2018. Unsafe Rust in actix-web, other libraries. https://www.reddit.com/
     Oriented Programs Using Static Class Hierarchy Analysis. In ECOOP’95 — Object-                   r/rust/comments/8s7gei/unsafe_rust_in_actixweb_other_libraries/. (2018).
     Oriented Programming, 9th European Conference, Åarhus, Denmark, August 7–11,                [38] Xi Wang, Nickolai Zeldovich, M. Frans Kaashoek, and Armando Solar-Lezama.
     1995, Mario Tokoro and Remo Pareschi (Eds.). Springer Berlin Heidelberg, Berlin,                 2013. Towards Optimization-safe Systems: Analyzing the Impact of Undefined
     Heidelberg, 77–101.                                                                              Behavior. In Proceedings of the Twenty-Fourth ACM Symposium on Operating
[12] C. R. Dougherty and R. C. Seacord. C. 2008. C compilers may silently discard                     Systems Principles (SOSP ’13). ACM, New York, NY, USA, 260–275. https://doi.
     some wraparound checks. https://www.kb.cert.org/vuls/id/162289/. (2008).                         org/10.1145/2517349.2522728
[13] Jonathan Eyolfson and Patrick Lam. 2019. How C++ Developers Use Immutabil-                  [39] Aaron Weiss, Daniel Patterson, Nicholas D. Matsakis, and Amal Ahmed. 2019.
     ity Declarations: An Empirical Study. In Proceedings of the 41st International                   Oxide: The Essence of Rust. CoRR abs/1903.00982 (2019). arXiv:1903.00982
     Conference on Software Engineering (ICSE ’19). IEEE Press, Piscataway, NJ, USA,                  http://arxiv.org/abs/1903.00982
     362–372.
[14] Patrick Gaydon. 2010. Project Servo, Technology from the past come to save the
     future from itself. http://venge.net/graydon/talks/intro-talk-2.pdf. (2010).
[15] David Gens, Simon Schmitt, Lucas Davi, and Ahmad-Reza Sadeghi. 2018. K-
     Miner: Uncovering Memory Corruption in Linux. In 25th Annual Network and
     Distributed System Security Symposium, NDSS 2018, San Diego, California, USA,
     February 18-21, 2018.
[16] Shiyou Huang, Jianmei Guo, Sanhong Li, Xiang Li, Yumin Qi, Kingsum Chow,
     and Jeff Huang. 2019. SafeCheck: Safety Enhancement of Java Unsafe API. In
     Proceedings of the 41st International Conference on Software Engineering (ICSE ’19).
     IEEE Press, Piscataway, NJ, USA, 889–899.
[17] Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2019. Stacked
     Borrows: An Aliasing Model for Rust. Proc. ACM Program. Lang. 4, POPL, Article
     Article 41 (Dec. 2019), 32 pages. https://doi.org/10.1145/3371109
[18] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017.
     RustBelt: Securing the Foundations of the Rust Programming Language. Proc.
     ACM Program. Lang. 2, POPL, Article 66 (Dec. 2017), 34 pages.
[19] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal,
     and Derek Dreyer. 2018. Iris from the ground up: A modular foundation for
     higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
[20] Amit Levy, Bradford Campbell, Branden Ghena, Daniel B. Giffin, Pat Pannuto,
     Prabal Dutta, and Philip Levis. 2017. Multiprogramming a 64kB Computer
     Safely and Efficiently. In Proceedings of the 26th Symposium on Operating Systems
     Principles (SOSP ’17). ACM, New York, NY, USA, 234–251.
[21] Yi Lin, Stephen M. Blackburn, Antony L. Hosking, and Michael Norrish. 2016.
     Rust As a Language for High Performance GC Implementation. In Proceedings of
     the 2016 ACM SIGPLAN International Symposium on Memory Management (ISMM
     2016). ACM, New York, NY, USA, 89–98.
[22] Luis Mastrangelo, Luca Ponzanelli, Andrea Mocci, Michele Lanza, Matthias
     Hauswirth, and Nathaniel Nystrom. 2015. Use at Your Own Risk: The Java
     Unsafe API in the Wild. In Proceedings of the 2015 ACM SIGPLAN International

                                                                                            12
