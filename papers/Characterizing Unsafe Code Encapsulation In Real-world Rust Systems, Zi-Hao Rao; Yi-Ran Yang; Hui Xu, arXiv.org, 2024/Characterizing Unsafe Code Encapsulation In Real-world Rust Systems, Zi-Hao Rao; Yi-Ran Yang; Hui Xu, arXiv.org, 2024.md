                                             Characterizing Unsafe Code Encapsulation In Real-world Rust
                                                                      Systems
                                                              Zihao Rao                                   Yiran Yang                                   Hui Xu∗
                                                   School of Computer Science,                   School of Computer Science,                 School of Computer Science,
                                                        Fudan University                              Fudan University                            Fudan University
                                                              China                                         China                                       China
                                         ABSTRACT                                                                 are investigations (e.g., [4, 6, 21]) into soundness verification or
                                         Interior unsafe is an essential design paradigm advocated by the         detecting unsoundness bugs. However, these studies provide very
                                         Rust community in system software development. However, there            limited insights for developers in designing their code. To the best
arXiv:2406.07936v1 [cs.SE] 12 Jun 2024




                                         is little official guidance or few best practices regarding how to       of our knowledge, there are no systematic studies on how to design
                                         encapsulate unsafe code and achieve interior unsafe. The prob-           interior unsafe code and how interior unsafe is implemented in
                                         lem is critical because the Rust compiler is incapable of verifying      real-world projects.
                                         the soundness of a safe function containing unsafe code. Falsely            In this paper, we aim to study how interior unsafe is achieved
                                         declaring an interior unsafe function as safe may undermine the          in practice and identify best practices for interior unsafe code de-
                                         fundamental memory-safety guarantee of Rust. To address this             sign. The problem is challenging because Rust has a complicated
                                         issue, this paper studies how interior unsafe is achieved in prac-       type system with structs and traits. Developers may have to con-
                                         tice, aiming to identify best practices to guide Rust code design        sider multiple functions to examine the soundness of an interior
                                         concerning unsafe code encapsulation. Specifically, we propose a         unsafe function. For example, an interior unsafe method of a struct
                                         novel unsafety isolation graph to model the essential usage and en-      may depend on its constructor to be safe, and the struct may have
                                         capsulation of unsafe code. Based on the graph, we further propose       several different constructors and interior unsafe methods. Such
                                         four major isolation types and nine structural patterns to split a       dependencies can create a strong coupling relationship among mul-
                                         graph into several small self-contained subgraphs. These subgraphs       tiple interior unsafe code. Additionally, some interior unsafe code
                                         can serve as useful audit units for examining the soundness of           may rely on global states or external functions to avoid undefined
                                         unsafe code encapsulation. We applied our approach to four real-         behaviors, which further complicates the soundness verification.
                                         world Rust projects. The experimental results demonstrate that              To address this challenge, we propose a novel unsafety isolation
                                         our method is effective in characterizing their encapsulation code.      graph to track the propagation of unsafe code and identify functions
                                         Additionally, we identified two common issues in these projects          responsible for isolating unsafety. The graph captures the essential
                                         that could complicate soundness verification or incur unsoundness        relationships among constructors, methods, and functions regard-
                                         issues.                                                                  ing unsafe code encapsulation. Given that the graph can become
                                                                                                                  very large and complex in some projects, we further propose four
                                         1    INTRODUCTION                                                        isolation types and nine structural patterns to divide the graph
                                                                                                                  into smaller, manageable subgraphs. Each subgraph acts as a self-
                                         The Rust programming language has two parts: safe Rust and un-
                                                                                                                  contained audit unit for unsafety encapsulation and verification.
                                         safe Rust [15]. Leveraging novel designs like ownership and borrow
                                                                                                                  We have developed an audit formula for each pattern to guide devel-
                                         checking, the Rust compiler can ensure memory safety as long
                                                                                                                  opers in examining the soundness of their interior unsafe code. Our
                                         as developers do not use unsafe code [13, 17]. However, avoiding
                                                                                                                  approach is systematic and comprehensive, considering all possible
                                         the use of unsafe code is generally impossible for system software
                                                                                                                  scenarios of dependencies and isolation responsibilities involving
                                         development, which requires low-level operations involving raw
                                                                                                                  structs and traits.
                                         pointer arithmetic and dereferencing. Consequently, interior un-
                                                                                                                     We applied our approach to four renowned operating system
                                         safe has become an essential design paradigm advocated by the
                                                                                                                  projects written in Rust. Experiment results show that our approach
                                         Rust community [22, 24]. This paradigm suggests that developers
                                                                                                                  is very useful for auditing interior unsafe code. In particular, we
                                         should strive to encapsulate unsafe code within safe functions or
                                                                                                                  find two common issues in unsafe code encapsulation. Firstly, de-
                                         methods whenever possible. Meanwhile, since unsafe code can lead
                                                                                                                  velopers may forget to specify the safety requirements for unsafe
                                         to undefined behaviors, developers must ensure the soundness of
                                                                                                                  constructors, complicating the verification of the soundness of
                                         their encapsulated interior unsafe functions themselves, as the com-
                                                                                                                  dynamic methods associated with these constructors. Secondly,
                                         piler is unable to verify this. Unsoundness issues in interior unsafe
                                                                                                                  developers may ignore the literal constructor of a struct, which can
                                         functions are common and represent a typical type of bug unique
                                                                                                                  bypass the safety requirements of its unsafe constructor, leading to
                                         to Rust [22, 27].
                                                                                                                  unsound interior unsafe code.
                                            Despite the importance of interior unsafe, there is little guidance
                                                                                                                     In short, our paper makes the following contributions.
                                         from the Rust community on how to achieve sound encapsulation.
                                         Prior to this work, several empirical studies (e.g., [5, 13]) have
                                                                                                                       • We propose a novel approach for auditing unsafe code encap-
                                         focused on how developers employ unsafe code, rather than how
                                                                                                                         sulation in Rust projects. Our method decomposes complex
                                         to encapsulate it or achieve interior unsafe. Additionally, there
                                                                                                                         interior unsafe code into nine structural patterns and pro-
                                         ∗ Corresponding author.                                                         vides an audit formula for each pattern. This approach offers
    arXiv, 2024,                                                                                                                              Rao et al.


            valuable guidance for developers in designing robust interior    5    }
            unsafe code.
          • We conducted experiments on four real-world Rust projects
                                                                                        Listing 2: Interior unsafe Rust code with struct.
            and identified two common issues that may lead to unsound
            interior unsafe code design. We believe our findings and         1    struct MyStruct<T> {
                                                                             2        x: *T,
            suggestions will be valuable to the Rust community.              3        n: i32,
                                                                             4    }
    2     PRELIMINARY                                                        5    impl struct MyStruct<T> {
                                                                             6        fn new(x: *T) -> Self { ... }
    In this section, we present the background of unsafe Rust and            7        unsafe fn deref(&self) -> T { ... }
                                                                             8        fn foo(&self) { unsafe{...} }
    interior unsafe code.                                                    9        fn bar(&self) { unsafe{...} }
                                                                            10    }
    2.1      Overview of Rust
    Rust has two parts: safe Rust and unsafe Rust.                                  Currently, the soundness check of interior unsafe code primarily
                                                                                 relies on developers. While this task may be manageable for small-
    2.1.1 Safe Rust. Safe Rust guarantees developers that if a program           scale projects with only a few unsafe code snippets, it becomes
    without unsafe code compiles, it will not exhibit undefined behavior.        challenging in real-world Rust projects as the number of unsafe code
    Rust achieves this through several innovative features, including            snippets grows. Real-world Rust projects often involve complex
    ownership and lifetimes. In safe Rust, each value has an owner,              structs and traits, requiring developers to consider all combinations
    and ownership can be borrowed either mutably or immutably. The               of member functions to ensure soundness. Listing presents a struct
    Rust compiler tracks ownership and enforces the rule of exclusive            MyStruct with a safe constructor new, an unsafe member function
    mutability: if a value has a mutable reference at a given point, it          deref(), and two safe methods foo() and bar(). Developers must
    cannot have other mutable or immutable aliases at that same point.           not only verify that new(), foo(), and bar() are individually sound
    However, safe Rust has its limitations. For instance, implementing           but also ensure that their combinations in different orders are sound.
    a doubly linked list is challenging because each node needs to have          Additionally, the safety requirements for unsafe code may not be
    two aliases, and the node itself must be mutable.                            explicit or well-documented, and validity checks might involve
                                                                                 complex logic, such as external functions or global variables. These
    2.1.2 Unsafe Rust. To enhance usability, Rust defines five types of
                                                                                 challenges can lead to unsoundness in interior unsafe code.
    unsafe code: raw pointer dereference, calling an unsafe function
    or method, accessing a static mutable variable, accessing fields of
    unions, and implementing an unsafe trait. Because the Rust com-
                                                                                 3 CHARACTERIZING UNSAFETY ISOLATION
    piler cannot guarantee memory safety for unsafe code, such code              3.1 Problem Setting
    must be used within an unsafe block (i.e., annotated with an unsafe          In this paper, we aim to study how interior unsafe code is encapsu-
    marker), indicating that developers should be responsible for the            lated and to identify best practices for its safe usage. Safety encap-
    risks incurred by unsafe code. Otherwise, the Rust compiler will             sulation is relatively straightforward for interior unsafe functions
    reject the code. Unsafe Rust complements safe Rust by providing              that are not part of any structs or traits, as they only depend on the
    necessary low-level memory control and flexible interoperability             function’s internal logic. However, the complexity increases when
    for many system software development scenarios.                              dealing with structs and traits. In this section, we clarify several
                                                                                 key terminologies and mechanisms related to Rust.
    2.2      Interior Unsafe and Challenges
                                                                                 3.1.1 Structs and Traits. A struct in Rust is a data structure that
    Since unsafe code is sometimes unavoidable in Rust programming, it
                                                                                 contains data fields, constructors, dynamic methods, and static
    is crucial to prevent the uncontrolled propagation of unsafety risks.
                                                                                 methods. Each struct has a default literal constructor that can cre-
    Interior unsafe is an essential design paradigm to mitigate these
                                                                                 ate an instance by directly specifying the value of each data field.
    risks. This paradigm involves a safe function or method containing
                                                                                 Dynamic methods are different from static methods in that their
    unsafe code, where all potential undefined behaviors caused by the
                                                                                 first parameter is self [1]. Dynamic methods differ from static
    unsafe code are properly managed within the function itself [24, 25].
                                                                                 methods in that their first parameter is self. A dynamic method
    For example, Listing 1 demonstrates an interior unsafe function
                                                                                 can only be used after an instance of the struct has been created and
    foo() that contains a call to the unsafe function doUnsafe(x). The
                                                                                 is called using the syntax object.foo(), where &self points to the
    unsafe code in foo() is only executed if x passes a validity check.
                                                                                 instance. In contrast, static methods do not require an instance to be
    Developers ensure that regardless of the argument passed to foo(),
                                                                                 created and are called directly using the syntax MyStruct::zoo().
    the function does not produce any undefined behaviors. Thus, inte-
                                                                                 A trait is a collection of methods that can be implemented by structs
    rior unsafe is an effective strategy to prevent the propagation of
                                                                                 or shared among them. Traits define common behaviors that structs
    unsafety risks and is widely used in Rust libraries.
                                                                                 can adopt, enabling polymorphism and code reuse in Rust.
               Listing 1: A simple interior unsafe function.
                                                                                 3.1.2 Unsafe Marker. There are two primary ways to use unsafe
1    fn foo(x: MyType) {                                                         code in Rust. One declares the entire function as unsafe, allowing
2        if (IsValid(x)) {
3            unsafe { doUnsafe(x); }                                             the use of unsafe code anywhere within it. This makes calling the
4        }                                                                       function itself unsafe, indicating that the caller must ensure safety
Characterizing Unsafe Code Encapsulation In Real-world Rust Systems                                                                     arXiv, 2024,




                                                 Figure 1: A sample UPG for the Asterinas project.


when using this function. The other way only marks a specific block            Definition 3.1 (Unsafety Propagation Graph). A UPG G(S, U, C, E)
within a function as unsafe, while the function itself can be declared      is a directed graph that tracks the propagation of unsafe code
as either safe or unsafe. The Rust compiler can verify that unsafe          through function calls and objects in a Rust program.
code is used only within the designated unsafe scope. However,
it cannot ensure that a function declared as safe but containing                                      S = 𝑆 𝑓 ∪ 𝑆𝑚
unsafe code within such a scope is truly safe in all scenarios.
                                                                                                     U = 𝑈 𝑓 ∪ 𝑈𝑚
3.1.3 Namespace and Visibility. In Rust, a crate is the smallest                                      C = 𝐶𝑠 ∪ 𝐶𝑢 ∪ 𝐶𝑙
compilation unit used to build targets, such as executables and                                       E = 𝐸𝑜𝑏 𝑗 ∪ 𝐸𝑐𝑎𝑙𝑙
libraries. A crate can contain multiple modules, each representing            where
a different namespace. Modules can be further divided into sub-
                                                                               • 𝑆 𝑓 is a set of safe functions and safe static methods.
modules. By default, all program components (e.g., functions and
                                                                               • 𝑆𝑚 is a set of safe dynamic methods.
global variables) within a module are private, meaning they are
                                                                               • 𝑈 𝑓 is a set of unsafe functions and unsafe static methods.
accessible only within that module. However, developers can make
                                                                               • 𝑈𝑚 is a set of unsafe dynamic methods.
these components public by using the pub keyword, allowing them
                                                                               • 𝐶𝑠 is a set of safe constructors.
to be accessed from outside the module.
                                                                               • 𝐶𝑢 is a set of unsafe constructors.
                                                                               • 𝐶𝑙 is a set of literal constructors.
3.2     Modeling Unsafety with Graphs                                          • 𝐸𝑜𝑏 𝑗 represents object flows between constructors and dy-
                                                                                 namic methods.
This section introduces a novel approach for modeling essential
                                                                               • 𝐸𝑐𝑎𝑙𝑙 represents function calls with an unsafe callee.
program components to facilitate unsafe code encapsulation. Tradi-
tional call graphs fall short of our requirements because they do not          Note that in the UPG, we are interested in two kinds of function
distinguish between safe functions, unsafe functions, and interior          calls: a safe caller and an unsafe callee, or an unsafe caller with an
unsafe functions. Consequently, they do not provide the necessary           unsafe callee. Additionally, we treat static methods in the same way
information to identify suitable functions for encapsulating unsafe         as general functions because they can be invoked directly without
code based on call graphs alone. To address this limitation and             creating an instance of the struct, and hence do not affect other
enhance our research on interior unsafe code, we propose a novel            methods. However, dynamic methods cannot be invoked without a
graph called the Unsafety Propagation Graph (UPG).                          struct instance. Therefore, we should also consider the relationship
arXiv, 2024,                                                                                                                               Rao et al.


 Algorithm 1: Unsafety Property Graph Generation                          dynamic method with a generic instance type, it implies the po-
    Input: 𝑐𝑟𝑎𝑡𝑒: The source code of a Rust crate                         tential for multiple method implementations. In such cases, the
    Output: 𝑈 𝑃𝐺: Unsafety Property Graph                                 method must belong to a trait that bounds the generic parame-
 1 𝑈 𝑃𝐺 ← ∅ ;                                                             ter, and the algorithm searches for all implementations of the trait
 2 𝑁 𝑜𝑑𝑒𝑠 ← FilterByUnsafeMarker(𝑐𝑟𝑎𝑡𝑒);                                  method, adding corresponding edges. Similarly, if an unsafe callee
 3 𝑈 𝑃𝐺.AddNode(𝑁 𝑜𝑑𝑒𝑠);                                                  originates from a function argument, the algorithm considers all
 4 foreach 𝑛𝑜𝑑𝑒 in 𝑁 𝑜𝑑𝑒𝑠 do                                              possible functions with the same signature in the UPG.
  5    if 𝑛𝑜𝑑𝑒.Type == DynMethod then                                        While a UPG can visualize unsafety propagation, it may contain
  6         𝐶𝑜𝑛𝑠𝑡𝑟𝑢𝑐𝑡𝑜𝑟𝑠 = FindConstructors(𝑛𝑜𝑑𝑒);                        redundant elements concerning safe encapsulation. To address this,
  7         foreach 𝑐𝑜𝑛𝑠 in 𝐶𝑜𝑛𝑠𝑡𝑟𝑢𝑐𝑡𝑜𝑟𝑠 do                               we proceed to remove all unsafe nodes that have no callers in the
  8              𝑈 𝑃𝐺.AddObjFlow(𝑐𝑜𝑛𝑠, 𝑛𝑜𝑑𝑒);                             UPG, resulting in the creation of an Unsafety Isolation Graph (UIG).
  9         end
10     end
11     CallSites ← FindAllUnsafeCallSites(𝑛𝑜𝑑𝑒);
12     foreach 𝑠𝑖𝑡𝑒 in 𝐶𝑎𝑙𝑙𝑆𝑖𝑡𝑒𝑠 do                                         Definition 3.2 (Unsafety Isolation Graph). An UIG is an unsafety
13          𝐶𝑎𝑙𝑙𝑒𝑒𝑠 ← ∅;                                                  propagation graph that has no 𝑈 𝑓 or 𝑈𝑚 without callers.
14          if 𝑠𝑖𝑡𝑒.calleeType == DynMethod then
15               𝑖𝑛𝑠𝑇 𝑦𝑝𝑒 ← GetInstanceType(𝑠𝑖𝑡𝑒.𝑐𝑎𝑙𝑙𝑒𝑒);
16               if 𝑖𝑛𝑠𝑇 𝑦𝑝𝑒 == Generic then
 17                   𝐶𝑎𝑙𝑙𝑒𝑒𝑠 ← FindAllImpls(𝑠𝑖𝑡𝑒.𝑐𝑎𝑙𝑙𝑒𝑒)
                                                                             Within each UIG, every unsafe node carries specific safety re-
18               end
                                                                          quirements that must be met [12]. For instance, the unsafe method
                 else
19
                                                                          vec::set_len from the Rust standard library specifies that be-
 20                   𝐶𝑎𝑙𝑙𝑒𝑒𝑠 ← 𝑠𝑖𝑡𝑒.𝑐𝑎𝑙𝑙𝑒𝑒
                                                                          fore calling, the argument new_len must be less than or equal to
21               end
                                                                          self.capacity, and the elements from index old_len to new_len
22          end
                                                                          must be initialized. We use the term required safety property set
23          else if 𝑠𝑖𝑡𝑒.calleeType == FnParam then
                                                                          (RS) to denote such requirements. Correspondingly, each safe caller
24               𝑓 𝑛𝑆𝑖𝑔𝑛 ← GetFnSign(𝑠𝑖𝑡𝑒.𝑐𝑎𝑙𝑙𝑒𝑒);
                                                                          on a UIG must ensure that it satisfies its callee’s RS to avoid un-
25               𝐶𝑎𝑙𝑙𝑒𝑒𝑠 ← FindAllFns(𝑓 𝑛𝑆𝑖𝑔𝑛)
                                                                          defined behaviors. We refer to the safety ensured by the caller as
26          end
                                                                          the verified safety property set (VS). For instance, a safe caller to
27          else
28               𝐶𝑎𝑙𝑙𝑒𝑒𝑠 ← 𝑠𝑖𝑡𝑒.𝑐𝑎𝑙𝑙𝑒𝑒                                    vec::set_len must assert that new_len is less than vec.capacity
29          end                                                           and guarantee that the extended content is well-initialized.
30          foreach 𝑐𝑎𝑙𝑙𝑒𝑒 in 𝐶𝑎𝑙𝑙𝑒𝑠𝑠 do                                     On a UIG, we do not consider safe callers with safe callees be-
31               𝑈 𝑃𝐺.AddEdge(𝑠𝑖𝑡𝑒.𝑐𝑎𝑙𝑙𝑒𝑟 , 𝑐𝑎𝑙𝑙𝑒𝑒);                      cause the responsibility for ensuring soundness lies with the safe
32          end                                                           callee regardless of the caller. This approach eliminates the need
33     end                                                                to account for various call sequences. Specifically, if a safe method
34 end
                                                                          contains unsafe code, we do not have to consider different combi-
                                                                          nations of their methods.




between constructors and dynamic methods, denoted as 𝐸𝑜𝑏 𝑗 . Since        3.3    Structural Patterns of Unsafety Isolation
the objective of a UPG is to track unsafety propagation, we do not        While an unsafety isolation graph (UIG) can capture the essential
need to consider unrelated function calls among safe functions.           components for unsafe code encapsulation, it may become too large
   Figure 1 illustrates a sample UPG for the real-world Rust project      (e.g., Figure 1) for effective auditing. In this section, our objective is
Asterinas. To better visualize unsafe code propagation paths, we          to propose a method for splitting a UIG into multiple self-contained
use different colors and shapes to represent various functions and        subgraphs for auditing purposes.
relations. Specifically, red-colored nodes indicate unsafe functions.         In our approach, each audit unit consists of a pair comprising
Additionally, we distinguish between functions, methods, and con-         a safe caller with an unsafe callee, along with their constructors
structors using rectangle, oval, and circle shapes, respectively. Solid   if they are dynamic methods. We categorize all audit units into
lines represent function calls, while dashed lines indicate object        four major folds based on their structural patterns and verification
flows between dynamic methods and their constructors.                     considerations.
   Algorithm 1 demonstrates the process of UPG extraction. It be-
gins by identifying all functions and methods with unsafe markers
and adds them to the UPG as nodes. For each dynamic method,
the algorithm locates its constructors and adds object-flow edges         3.3.1 Direct Isolation. This is a straightforward pattern that only
between them. Next, it searches for all unsafe call sites within the      the safe function itself is responsible for encapsulating the unsafe
nodes and adds corresponding call edges. If a callee is an unsafe         code. This type includes two subtypes.
Characterizing Unsafe Code Encapsulation In Real-world Rust Systems                                                                          arXiv, 2024,


                                                                           3.3.3 Half Isolation. This type is similar to the previous two types
                                                                           but also depends on the safety requirements of an unsafe construc-
                                                                           tor to ensure soundness. Because the unsafe constructor’s practical
                                                                           usage is unpredictable, we refer to this type as half isolation. There
                                                                           are four subtypes within this category.


            (a) Type I                                (b) Type II

                      Figure 2: Direct Isolation

     • 𝑠 𝑓 → 𝑢 𝑓 ||𝑐𝑢 : A safe function 𝑠 𝑓 calls either an unsafe func-
       tion 𝑢 𝑓 or an unsafe constructor 𝑐𝑢 . It is the responsibility
       of 𝑠 𝑓 to ensure that all the safety requirements of 𝑢 𝑓 can be                (a) Type I                               (b) Type II
       satisfied when reaching 𝑢 𝑓 . It’s important to note that since
       constructors are also static functions, 𝑢 𝑓 can also represent
       an unsafe constructor 𝑐𝑢 . Audit formula:
                                𝑅𝑆𝑢 𝑓 ⊆ 𝑉 𝑆𝑠 𝑓
     • 𝑠 𝑓 ||𝑐𝑠 → 𝑢𝑚 (𝑐𝑠 ): A safe function 𝑠 𝑓 calls an unsafe method
       𝑢𝑚 , and the constructor 𝑐𝑠 associated with 𝑢𝑚 is safe. Since
       𝑢𝑚 has specific safety requirements, 𝑠 𝑓 must ensure that all
       these requirements are satisfied. Audit formula:                              (c) Type III                              (d) Type IV

                               𝑅𝑆𝑢𝑚 ⊆ 𝑉 𝑆𝑠 𝑓
                                                                                                   Figure 4: Half Isolation


                                                                               • 𝑠𝑚 (𝑐𝑢 ) → 𝑢 𝑓 ||𝑐𝑢 : In this scenario, a safe method 𝑠𝑚 calls an
                                                                                 unsafe function 𝑢 𝑓 , and the constructor 𝑐𝑢 of 𝑠𝑚 is defined as
                                                                                 unsafe. In such cases, both 𝑐𝑢 and 𝑠𝑚 share the responsibility
                                                                                 for satisfying the safety requirements of 𝑢 𝑓 . Additionally,
                                                                                 since 𝑐𝑢 is unsafe and also has safety property requirements
                                                                                 𝑅𝑆 (𝑐𝑢 ), it is assumed that these requirements can be satisfied.
                                                                                 Audit formula:
              (a) Type I                            (b) Type II
                                                                                             𝑅𝑆𝑢 𝑓 ⊆ (𝑉 𝑆𝑠𝑚 ∪ 𝑅𝑆𝑐𝑢 ∪ 𝑉 𝑆𝑐𝑢 )
                     Figure 3: Indirect Isolation                              • 𝑠 𝑓 ||𝑐𝑠 → 𝑢𝑚 (𝑐𝑢 ): A safe function 𝑠 𝑓 calls an unsafe method
                                                                                 𝑢𝑚 , and the constructor 𝑐𝑢 of 𝑢𝑚 is unsafe. In such cases, it is
3.3.2 Indirect Isolation. This type indicates a scenario where a                 considered that 𝑢𝑚 should have its own safety requirements
safe method contains unsafe code, and its constructor is safe. Since             independent of 𝑐𝑢 . This approach allows the verification
the constructor is a necessary precondition for executing the safe               chains of 𝑢𝑚 and 𝑐𝑢 to be decoupled from each other. Audit
method, both the constructor and the method share the responsibil-               formula:
ity for handling any potential undefined behaviors. There are two                                      𝑅𝑆𝑢𝑚 ⊆ 𝑉 𝑆𝑠 𝑓
subtypes within this category.                                                 • 𝑠𝑚 (𝑐1𝑠 ) → 𝑢𝑚 (𝑐2𝑢 ): A safe method 𝑠𝑚 calls an unsafe
     • 𝑠𝑚 (𝑐𝑠 ) → 𝑢 𝑓 ||𝑐𝑢 : A safe method 𝑠𝑚 calls an unsafe function           method 𝑢𝑚 , with the constructors of 𝑠𝑚 and 𝑢𝑚 being safe
        𝑢 𝑓 , and the constructor 𝑐𝑠 associated with 𝑠𝑚 is safe. In such         and unsafe, respectively. Audit formula:
        cases, both 𝑐𝑠 and 𝑠𝑚 bear the responsibility for ensuring the
                                                                                                    𝑅𝑆𝑢𝑚 ⊆ (𝑉 𝑆𝑠𝑚 ∪ 𝑉 𝑆𝑐1𝑠 )
        safety requirements of 𝑢 𝑓 are met. Audit formula:
                           𝑅𝑆𝑢 𝑓 ⊆ (𝑉 𝑆𝑠𝑚 ∪ 𝑉 𝑆𝑐𝑠 )                            • 𝑠𝑚 (𝑐1𝑢 ) → 𝑢𝑚 (𝑐2𝑠 ): A safe method 𝑠𝑚 calls an unsafe
                                                                                 method 𝑢𝑚 , with the constructors of 𝑠𝑚 and 𝑢𝑚 being unsafe
     • 𝑠𝑚 (𝑐1𝑠 ) → 𝑢𝑚 (𝑐2𝑠 ):A safe method 𝑠𝑚 calls an unsafe method             and safe, respectively. Audit formula:
       𝑢𝑚 , and the constructors for both 𝑠𝑚 and 𝑢𝑚 are safe. In this
       case, the constructor of 𝑠𝑚 (denoted as 𝑐1𝑠 ) and 𝑠𝑚 itself                          𝑅𝑆𝑢𝑚 ⊆ (𝑉 𝑆𝑠𝑚 ∪ 𝑅𝑆𝑐1𝑢 ∪ 𝑉 𝑆𝑐1𝑢 )
       share the responsibility for ensuring that the safety require-      3.3.4 Open Isolation. This type of audit unit relies on the safety
       ments of 𝑢𝑚 are met. Audit formula:                                 requirements of two unsafe constructors for verification. It has only
                         𝑅𝑆𝑢𝑚 ⊆ (𝑉 𝑆𝑠𝑚 ∪ 𝑉 𝑆𝑐1𝑠 )                          one form in our approach.
arXiv, 2024,                                                                                                                           Rao et al.




                     Figure 5: Open Isolation


   𝑠𝑚 (𝑐1𝑢 ) → 𝑢𝑚 (𝑐2𝑢 ): A safe method 𝑠𝑚 calls an unsafe method
𝑢𝑚 , with both 𝑠𝑚 and 𝑢𝑚 having unsafe constructors. The safety of
the execution heavily depends on how the objects are constructed.
Audit formula:
                  𝑅𝑆𝑢𝑚 ⊆ (𝑉 𝑆𝑠𝑚 ∪ 𝑅𝑆𝑐1𝑢 ∪ 𝑉 𝑆𝑐1𝑢 )                       Figure 6: Cumulative distribution of graph sizes based on
                                                                         number of edges in connected subgraphs across four projects.
  The structural patterns provide clear guidance for further safety
property verification. This allows our approach to successfully de-
couple the complicated relationships between safety requirements
                                                                             The Asterinas OS [9], developed by Ant Group, features the
and verification duties within a Rust crate.
                                                                         Framekernel architecture which emphasizes modularity and secu-
                                                                         rity, dividing it into the OS Framework and OS Services. rCore [10]
3.4      Types of Safety Checks                                          is an educational operating system kernel developed in Rust, demon-
In addition to structural factors, we are also interested in the loca-   strating Rust’s capabilities in system programming. Theseus [7] is
tions and types of mechanisms that ensure code safety. Intuitively,      an innovative operating system that uses language-level mecha-
if unsafe code is encapsulated within a safe function, that func-        nisms to enforce safety and correctness, shifting key responsibilities
tion should perform safety verification operations to safeguard          from the OS to the compiler. The Aero [2] is a lightweight Unix-
the safety of unsafe blocks. We regard these operations as safety        like kernel written in Rust. This OS embraces a monolithic kernel
checks. We categorize safety checks into two types, direct check         architecture, drawing inspiration from the Linux Kernel.
and no check, based on the behavior of the unsafe callee’s parame-
ters within the safe caller. Our classification does not rely on the     4.1.2 Experimental Procedure. Our experimental methodology em-
specific logic of the project but simply categorizes based on the        ploys Algorithm 1 to construct each project’s unsafe propagation
characteristics of the data flow.                                        graphs. Following this, we derive unsafe isolation graphs from these
   Direct Check: (1) obtained through a global variable, a hardcoded     UPGs. To validate the applicability and effectiveness of our methods,
variable, or a global static function returning a fixed value; (2)       we implement our audit formulas to each audit unit within the UIGs.
validated using if or assert statements                                  This process involves a meticulous manual code review within each
   No Check: (1) dependent on safe caller’s input parameters; (2)        unit to detect and categorize instances of unsafe encapsulation and
lacking any validation of the unsafe callee’s input parameters           safety checks. The experimental tasks are primarily executed by
                                                                         the first author, with the second author providing a critical review
4     EXPERIMENTS                                                        of the statistical outcomes to ensure accuracy. Any discrepancies
                                                                         are resolved through discussion with the third author.
In this section, we design experiments to examine the applicability
and usefulness of our approach for real-world Rust project analysis.
                                                                         4.2    Characteristics of Unsafety Encapsulation
4.1      Experimental Setting                                            4.2.1 Overview of Four Projects. We implemented our analytical
                                                                         methodology on these four projects, constructing UPGs and de-
4.1.1 Rust Project Selection. For our study, we established two
                                                                         riving UIGs from them. An overview of our statistical findings on
fundamental criteria for selecting projects:
                                                                         audit units within the UIGs is presented in Table 1.
      • Maturity and Popularity: Projects must have been under              A notable trend across all projects is the prevalent use of both Di-
        active development for over two years and maintained within      rect Isolation and Indirect Isolation, which do not incorporate unsafe
        the last year, with a minimum of 1,000 GitHub stars.             constructors. On average, unsafe methods constituted 57.8% of the
      • Extensive Use of Unsafe Code: Projects should contain more       total audit units, underscoring the necessity for meticulous consid-
        than 300 instances of unsafe code.                               eration of several factors, including their constructors, as elaborated
   Given these criteria, our research predominantly targets operat-      in Section 3.2. Variations were observed among the projects: rCore,
ing system projects due to their extensive engagement with low-          Theseus, and Aero primarily utilize safe constructors for methods
level operations and critical focus on safety. This environment is       involving unsafe code, whereas Asterinas prominently employs
particularly conducive to studying the management and encapsula-         unsafe constructors. This is attributed to Asterinas’s design, which
tion of interior unsafe code. We selected four renowned operating        integrates a high degree of isolation by encapsulating unsafe code
system projects within the Rust community:: Asterinas, rCore, The-       within the initialization phases of structures to establish secure
seus, and Aero.                                                          interfaces, as confirmed by a developer from Asterinas.
Characterizing Unsafe Code Encapsulation In Real-world Rust Systems                                                                               arXiv, 2024,


                    Table 1: Distribution of unsafe structural types and unsafety checks in four Rust-based projects.

              Direct Isolation          Indirect Isolation                                   Half Isolation                         Open Isolation
  Project                                                                                                                                             Total
             sf-uf sf-um(sc)         sm(sc)-uf sm(sc)-um(sc)          sm(uc)-uf       sf-um(uc) sm(sc)-um(uc)    sm(uc)-um(sc)      sm(uc)-um(uc)
 Asterinas     96         7               43             5               11              5             1               19                  1           188
  rCore       94         14              114             51              0               0             0               0                   0           273
 Theseus       98        47               79             36               1              0             0               0                   0           261
   Aero       158        66               82             18               4              1             0               0                   4           333


   Furthermore, we analyzed each connected subgraph within the                        verifications. In listing 3, the safety of safe method read, ensured by
UPGs of these projects, with each subgraph delineating the influ-                     its constructor, is contingent on the known integrity of the I/O port.
ence scope of the unsafe code it contains. We used the number of                      If the I/O port’s identity is unclear, it may pose significant memory
edges in each connected graph to reflect the scale of its influence                   safety risks. Within this audit unit, we cannot judge how its unsafe
scope. Figure 6 illustrates the cumulative distribution of graph sizes,               constructor is used, making it challenging to ensure the validity of
highlighting differences across projects. In Theseus and Aero, the                    its field port. This introduces a complexity in verification that re-
graphs predominantly reach complete distribution with fewer edges,                    quires examining another audit unit, where another caller invokes
indicating a direct encapsulation of unsafe code within safe callers                  IoPort::new, to verify its safety before confirming the safety of
and minimal propagation chains. In contrast, Asterinas and rCore                      the read method. This necessitates a two-hop verification for Half
respectively have 20.5% and 7.6% of their connected graphs contain-                   Isolation. Similarly, Open Isolation may demand two or three hops
ing more than five edges, involving 53.0% and 35.0% of all nodes.                     for thorough verification, depending on the interconnectedness of
This suggests extensive unsafety propagation involving multiple                       the components and their respective constructors.
unsafe nodes and dependencies on constructors in these projects,
highlighting a complex landscape of unsafe code management.                                  Listing 3: Half Isolation: sm(uc)-uf from Asterinas
   In summary, The deployment of interior unsafe code in real-                    1    impl<T, A> IoPort<T, A> {
world projects is characterized by a high level of complexity, par-               2        /// # Safety: creating an I/O port is a privileged operation.
                                                                                  3        pub const unsafe fn new(port: u16) -> Self {
ticularly due to the significant involvement of constructors. This                4            Self { port, ... }
often leads to intricate and interdependent call relationships.                   5        }
                                                                                  6        pub fn read(&self) -> T {
                                                                                  7            unsafe { PortRead::read_from_port(self.port) }
4.2.2 Complexity of Different Audit Unit. This subsection illus-                  8        }
trates the complexity involved in verifying different types of audit              9    }
units through specific cases encountered within these projects. We
will also demonstrate the powerful decoupling capability of our                           Listing 4: Indirect Isolation: sm(sc)-uf from Asterinas
method for validating the encapsulation of interior unsafe code.               1       pub struct XApic {
   For Direct Isolation, the encapsulation of unsafe code is relatively        2           mmio_region: &'static mut [u32],
explicit. Developers and code auditors must identify all precon-               3       }
                                                                               4       impl XApic {
ditions and postconditions associated with the unsafe code. The                5           pub fn new() -> Option<Self> {
main verification task is to ensure these safety prerequisites are             6               ...
comprehensively addressed within the internal logic of the safe                7               let address = vm::paddr_to_vaddr(get_apic_base_address());
                                                                               8               let region: &'static mut [u32] =
caller, thereby affirming the soundness of the encapsulation.                  9                    unsafe { &mut *(address as *mut [u32; 256]) };
   In Indirect Isolation, the safe caller is available following con-         10               Some(Self { mmio_region: region })
                                                                              11           }
struction by a safe constructor. Our audit formula stipulates that            12           fn read(&self, offset: u32) -> u32 {
the combined safety guarantees from both the safe caller and its              13               assert!(offset as usize % 4 == 0);
constructor must encompass the immediate safety needs of the                  14               let index = offset as usize / 4;
                                                                              15               unsafe { ptr::read_volatile(&self.mmio_region[index]) }
unsafe callee. For instance, as detailed in Listing 4, the unsafe callee      16           }
read_volatile from the standard library mandates that its pa-                 17       }
rameters should be valid and aligned at the syntactic level. These
requirements are proactively managed in XApic’s constructor new,                      4.2.3 Discussion of Struct with Both Safe and Unsafe Constructors.
which performs essential initialization to ensure the mmio_region                     In our previous discussions, we examined scenarios where structs
field is correctly prepared. Subsequently, the safe method caller                     were characterized by either a single safe or unsafe constructor. A
read can only conduct project-specific validations and then di-                       significant advantage of the UIG model we propose is its flexibility
rectly use this field as a parameter to invoke the unsafe callee                      in managing complex structures, particularly those equipped with
read_volatile.                                                                        multiple constructors. This capability is crucial as it allows a large
   The verification challenges of Half Isolation and Open Isolation                   struct to be systematically decomposed into several audit units,
lies in their reliance on comprehensive encapsulation across multi-                   thereby facilitating the meticulous handling of scenarios involving
ple audit units. Unlike Direct Isolation and Indirect Isolation, which                multiple constructors.
encapsulate the safety of unsafe code through the behavior of a sin-                     When a struct incorporates both safe and unsafe constructors,
gle audit unit, Half Isolation and Open Isolation necessitate multi-hop               the analysis involves segregating these constructors into distinct
arXiv, 2024,                                                                                                                               Rao et al.


                                                                              guarantees provided by both constructors according to our audit
                                                                              formula. Consequently, labeling it as ’safe’ may lead to unsound
                                                                              problems. This concern is corroborated by developer comments.
                                                                              Listing 5: case sf-um that has both safe and unsafe construc-
                                                                              tor from Aero
                                                                          1    impl PhysAddr {
                                                                          2        /// # Safety: Bits in the range 52 to 64 have requirements.
                                                                          3        //unsafe constructor
                                                                          4        pub const unsafe fn new_unchecked(addr: u64) -> PhysAddr {
                                                                          5            PhysAddr(addr)
                                                                          6        }
                                                                          7        //safe constructor
                                                                          8        pub fn new(addr: u64) -> PhysAddr {
                                                                          9            assert_eq!( addr.get_bits(52..64), 0,
                                                                         10                "Can not have any bits in the range 52 to 64 set"
                                                                         11            );
Figure 7: Decomposition of a large structure with both safe              12            unsafe { PhysAddr::new_unchecked(addr) }
                                                                         13        }
and unsafe constructors into multiple audit units.                       14        //safe method
                                                                         15        pub fn as_hhdm_virt(&self) -> VirtAddr {
                                                                         16            // TODO: Make `PHYSICAL_MEMORY_OFFSET` an atomic usize
audit units. This allows for two primary pathways to utilize this        17            // instead of making it a mutable static and spamming
                                                                         18            // `unsafe` everywhere; where its not even required.
method. No matter which way is taken, the usage of the methods           19            unsafe { crate::PHYSICAL_MEMORY_OFFSET + self.as_u64() }
should be sound. If a struct is instantiated via its safe constructor,   20        }
the methods that use interior unsafe code should be directly us-         21    }
able. Otherwise, they must be marked as unsafe. This is also the
reason we discussed in Chapter 3 for why the modeling of audit
unit is considered reasonable. As for the construction utilizing an           Table 2: Status of safety annotations for custom unsafe func-
unsafe constructor, if its safety annotations are strictly satisfied,         tions within the projects. The table presents the comparison
then the program state should be consistent with that obtained                of functions lacking annotations to the total number of un-
through a safe constructor. Consequently, the scope of safety cov-            safe functions.
ered by an unsafe constructor, when combined with its specific
safety requirements, must align with the safety coverage provided
                                                                                                        Annotation(lack/total)
by the safe constructor. This alignment ensures that regardless of                     Project
                                                                                                   Constructor Function Method
the construction method used, the structural integrity and safety
standards remain consistent and reliable. That means:                                 Asterinas        1/20           9/27         12/24
                                                                                       rCore           10/10          58/58        30/30
                            𝑉 𝑆𝑐𝑠 ≡ 𝑉 𝑆𝑐𝑠 ∪ 𝑅𝑆𝑐𝑠                                      Theseus           8/8           83/95        23/37
   Therefore, for every safe method 𝑚𝑖 in it, if 𝑚𝑖 calls an unsafe                     Aero            4/7           53/57        36/47
function 𝑢 𝑓 or unsafe method 𝑢𝑚 , audit formula can be expressed
as follows:
               𝑅𝑆𝑢 𝑓 𝑜𝑟 𝑢𝑚 ⊆ (𝑉 𝑆𝑐𝑠 ∩ (𝑉 𝑆𝑐𝑢 ∪ 𝑅𝑆𝑐𝑢 )) ∪ 𝑉 𝑆𝑚𝑖
                                                                              5 ISSUES AND FINDINGS
   In our experiments, we have identified several potentially prob-
lematic examples through our methodology. Listing 5 displays                  5.1 Lack of Safety Annotations
a code snippet from Aero. The PhysAddr struct incorporates a                  Issue 1: Many unsafe functions or methods lack safety requirement
safe constructor new, which performs necessary checks on the                  annotations, which, while not strictly necessary, are very useful for
parameter addr through assert_eq!, and an unsafe constructor                  achieving safety encapsulation.
new_unchecked, which directly invokes PhysAddr to generate a                     Within the Rust community, it is a common practice to annotate
physical address. Therefore, based on their program behaviors, we             custom unsafe functions with required safety requirements imme-
can construct their verified safety sets: 𝑉 𝑆𝑛𝑒𝑤 = { Init_State }, and        diately after developing them [16]. This practice ensures that the
𝑉 𝑆𝑛𝑒𝑤_𝑢𝑛𝑐ℎ𝑒𝑐𝑘𝑒𝑑 = ∅. To maintain object consistency, the unsafe              safety implications of using such functions are clear to all devel-
constructor should be annotated to indicate that parameter checks             opers involved. However, our empirical findings reveal that this
are still necessary. So we get its required safety set 𝑅𝑆𝑛𝑒𝑤_𝑢𝑛𝑐ℎ𝑒𝑐𝑘𝑒𝑑        paradigm is not universally adhered to, primarily because it is not a
= { Init_State }. This demonstrates the equivalence between the two           mandatory requirement. In Table 2, we have listed the safety anno-
construction methods. These sets facilitate the application of our au-        tation status of all custom unsafe functions in these four projects.
dit formula to evaluate the safety of methods within PhysAddr. For            Asterinas, developed by a company, exhibits a higher density of
example, the safe method as_hhdm_virt employs a global mutable                safety annotations compared to other projects with a 31% absence
static variable, which requires an unsafe marker as this could lead           rate. However, this rate in the other three projects reaches as high
to data races and other thread safety issues. These issues primarily          as 87%, as they are presumably with less stringent development
arise from the global program state, which falls outside the safety           protocols.
     Characterizing Unsafe Code Encapsulation In Real-world Rust Systems                                                                      arXiv, 2024,


        For Direct Isolation and Indirect Isolation, the lack of safety anno-
     tations within their functions and methods necessitates that devel-
     opers and code reviewers need to manually audit and extract the
     safety requirements of the unsafe callee, and then assess whether
     the safe caller’s encapsulation behavior satisfies these safety re-
     quirements.
        However, the absence of safety annotations on unsafe construc-
     tors can significantly undermine the auditing principle that typi-
     cally focuses only on the nodes within one single audit unit. This
     shortfall is critical because unsafe constructors often fail to provide
     explicit safety requirements in their code. Consequently, these con-
     structors necessitate a broader examination that extends beyond
     their immediate context to include the behavior of their callers in
     other audit units. Listing 6 provides an example of Half Isolation
     from Theseus. To confirm that this unsafe encapsulation is sound,
     the sets 𝑅𝑆𝑖𝑛𝑛𝑒𝑟 and 𝑅𝑆𝑛𝑒𝑤 are necessary. While the construction
     logic in line 6 obscures the clarity of its safety requirements to build
     the 𝑅𝑆𝑛𝑒𝑤 . This complexity underscores the need for a broader in-
     vestigation of its safety. Additionally, as unsafe constructors serve
     as boundaries in the audit unit of Half Isolation and Open Isolation,
     the absence of their safety can impact multiple other audit units.
        Another case from Asterinas provides a best practice in Figure 8.
     In the example, the 𝑅𝑆 set of the unsafe callee get_page_frame can
                                                                                Figure 8: An example of a half isolation case: Annotating the
     be easily obtained from annotations: page number (1) is a physical
                                                                                unsafe constructor with safety requirements can simplify
     page number, and (2) is identically mapped. Meanwhile, code re-
                                                                                verification by treating it as two independent audit units.
     viewers only need to focus on the code within the PageTableCreator
     to obtain sets 𝑅𝑆𝑛𝑒𝑤 and 𝑉 𝑆𝑛𝑒𝑤 . In our method, within this audit
     unit, 𝑅𝑆𝑛𝑒𝑤 is assumed to always be met. Its assurance of safety           5.2    Unsoundness Concerning Visibility
     is evaluated within a distinct audit unit. Therefore, even if the 𝑉 𝑆
                                                                                Issue 2: Developers may overlook the soundness issues in certain
     of the safe caller allocate is not sufficient to cover all safety of
                                                                                internal module scenarios, such as bypassing unsafe constructors
     get_page_frame, the 𝑅𝑆𝑛𝑒𝑤 can assist in confirming the validity of
                                                                                via literal constructors or directly invoking some safe methods that
     the PageNumber object.
                                                                                lack safety checks.
            Listing 6: Half isolation: sm(uc)-uf from Theseus
                                                                                5.2.1 Literal Construction. Rust’s literal construction can bypass
 1    pub struct LocalKey<T: 'static> {                                         necessary safety assurances in constructors, which may potentially
 2        inner: unsafe fn() -> T,
 3    }                                                                         compromise the methods’ soundness. In Rust, structs can be instan-
 4    impl<T: 'static> LocalKey<T> {                                            tiated in two primary ways: using literal syntax and constructors.
 5        pub const unsafe fn new(inner: unsafe fn()->T) -> LocalKey<T> {
 6            LocalKey { inner }
                                                                                Literal syntax directly sets a structure’s fields if they are accessible.
 7        }                                                                     Constructors, on the other hand, aim for uniform initialization of
 8        pub fn try_with<F, R>(&'static self, f: F){                           the structure’s fields. Previously, we discussed that objects created
 9            unsafe { let thread_local = (self.inner)();}
10        }                                                                     via safe or annotated unsafe constructors must maintain a consis-
11    }                                                                         tent program state for predictable behaviors. However, using literal
                                                                                construction can jeopardize this consistency, as it allows direct field
        In summary, audit units help identify critical areas in the de-
                                                                                manipulation.
     velopment of unsafe code, streamlining the verification process
                                                                                    We model the behavior associated with literal constructors as an
     with structured audit formulas. However, our findings highlight a
                                                                                issue in Figure 9. In this scenario, developers in a team have three
     significant shortfall in safety annotations across major Rust-based
                                                                                paths to access a struct’s method. If the unsafe constructor’s safety
     operating system projects, complicating verification and increasing
                                                                                annotations are sufficient, path one is a viable choice since devel-
     the risk of safety oversights.
                                                                                opers can recognize potential safety issues. Choosing path 2 means
        Based on the issue 1 we have identified, we propose the following
                                                                                the safe constructor inherently encapsulates the unsafety. However,
     suggestions for project developers:
                                                                                literal construction obscures these details. If other developers in
        Suggestion 1: Developers should annotate each unsafe function
                                                                                the team attempt to use the struct’s safe_method interface via lit-
     and method with explicit safety requirements. The Rust compiler
                                                                                eral construction, they might not establish a comprehensive VS for
     could enforce such checks, regardless of their semantic correctness.
                                                                                this method. This could result in the safe_method triggering an
                                                                                unsoundness issue. Although this issue might be partly attributed
                                                                                to non-standard development practices, we want to emphasize that
                                                                                this is a potential flaw in Rust’s current development of interior
    arXiv, 2024,                                                                                                                            Rao et al.


                                                                                    Table 3: Statistics of cases with no safety checks.

                                                                                                   Asterinas    rCore      Theseus      Aero
                                                                                  Isolation Type
                                                                                                   No Yes      No Yes      No Yes      No Yes
                                                                                        sf-uf      28    74    15    94    31    69    28   161
                                                                                     sf-um(sc)      2    4      2    14     7    40    18    71
                                                                                     sm(sc)-uf     23    20    49    88    37    43    18    79
                                                                                   sm(sc)-um(sc)    0     5    14    47    16    26    15    71
                                                                                     sm(uc)-uf     11     0     0     0     0     1     0    5
                                                                                     sf-um(uc)      1     4     0     0     0     0     0    2
                                                                                   sm(sc)-um(uc)    1     0     0     0     0     0     4     3
                                                                                   sm(uc)-um(sc)    9    13     0     0     0     0     0     0
                                                                                   sm(uc)-um(uc)    0    1      0     0     0    0      0     5
    Figure 9: A model depicting the potential unsoundness in-                          Total       75   121    80   241    91   179    83   397

    troduced by literal construction in Rust, which may bypass
    safety guarantees provided by constructors.
                                                                              6   RELATED WORK
                                                                              In this section, we discuss and compare with investigations on
    unsafe code. In real-world projects, numerous instances exist where       unsafe Rust code previous to our work to show the significance of
    constructors encapsulate methods’ unsafety, yet literal construction      our approach.
    could potentially leave a vulnerability in such code, thus becoming          Researches in unsafe code isolation focus on strategies that lever-
    a possible form of attack against Rust’s safety guarantees.               age both programming language features [8, 23] and system-level
       Regarding this issue, we would like to make suggestions to the         controls [3, 20, 26] to secure memory and data flow. These methods
    developers of the Rust compiler:                                          consider the isolation of unsafe code from a runtime perspective,
       Suggestion 2: The Rust compiler may consider disabling literal         rather than during development and auditing.
    constructors in the future to better support unsafe constructors             Formal verification [18, 21] is a robust yet complex method for
    and ensure soundness.                                                     validating the safety of Rust’s unsafe code, but it can only verify
                                                                              programs at the language level. In contrast, our method also ef-
    5.2.2 Functions with No Safety Check. In the development practices,       fectively aids developers in auditing the logical safety of custom
    developers may opt to designate code that lacks safety checks as          unsafe functions.
    non-public.                                                                  Static analysis methods leverage Rust’s strong type system and
        In our experiment results, a counterintuitive observation was         ownership model to provide precise and accessible bug detection.
    the presence of no blot data, where safe callers employ unsafe code       They aim to identify common bug patterns in unsafe Rust code,
    without any safety checks on the input parameters. As detailed in         such as memory deallocation violations [11, 19], panic safety bugs,
    Table 3, the data of no safety checks, on average, 69.0% are related      higher-order invariant bugs, and Send/Sync variance bugs [6].
    to methods. In Section 4.2, our discussions on the structural prop-          Empirical studies give insights into the unsafe Rust usage sta-
    erties of audit units can explain why it is reasonable for methods        tus [14, 22, 28] and point out why and how to write unsafe code
    to exhibit no blot interior unsafe code, as their constructors can        in real-world programs [5, 13]. Researchers also classify the un-
    provide a layer of safety assurance. However, the scenario for static     safe APIs in standard libraries based on safety descriptions [12].
    functions proved perplexing. Some examples may ensure safety              However, they focus more on the unsafe code itself and don’t take
    through global states or parameters, while others still have safety       a deeper look at how to securely encapsulate unsafe code in safe
    issues to be addressed, such as the code case in listing 5. Our further   Rust.
    analysis showed that 41.9% of the function’s no blot occurrences
    are related to visibility. Listing 7 from Theseus illustrates that a      7   CONCLUSION
    static function directly dereferences a raw pointer after accepting       In this paper, our research aimed to identify common patterns and
    it as an input parameter. When the parameter is a null pointer or         potential vulnerabilities in the encapsulation of unsafe code in Rust.
    other invalid values, this action may trigger an exception. Since         We developed graph-based models called the unsafety propagation
    this function’s usage is confined within its module, it is controllable   graph and the unsafety isolation graph to systematically analyze
    to ensure the soundness of its parameters among its limited callers.      and characterize unsafe coding practices. We further identified nine
    This may be a common development practice, yet it somewhat                categories of audit units. Then we applied our methodologies to
    contradicts the principle of encapsulating interior unsafe code.          four Rust-based operating system projects. The experiment results
        Suggestion 3: Developers should double-check that their interior      confirmed the complexity of unsafe code encapsulation and demon-
    unsafe code, which lacks safety checks, is sound. The Rust compiler       strated the applicability and effectiveness of our method in auditing
    might issue a warning in such cases.                                      interior unsafe code. Moreover, we also identified two types of is-
    Listing 7: A sample case with no safety checks from Theseus               sues prevalent in current Rust projects: the lack of annotations on
                                                                              custom unsafe functions and the soundness problems introduced
1    fn panic_callback(data_ptr: *mut u8, ...) {
2        let data = unsafe { &mut *(data_ptr as *mut TryIntrinsicArg) };      by literal constructions and non-public functions. Through these
3        ...                                                                  efforts, we believe our method will promote the standardization of
4    }
                                                                              unsafe code development and auditing within the Rust community.
Characterizing Unsafe Code Encapsulation In Real-world Rust Systems                                                                                              arXiv, 2024,


REFERENCES                                                                                       Language Design and Implementation. 763–779.
 [1] 2024. Functions - The Rust Programming Language. https://doc.rust-lang.org/            [26] Elijah Rivera, Samuel Mergendahl, Howard Shrobe, Hamed Okhravi, and Nathan
     reference/items/functions.html [Accessed: 2024-06-03].                                      Burow. 2021. Keeping safe rust safe with galeed. In Proceedings of the 37th
 [2] Aero Contributors. 2024. Aero. https://github.com/Andy-Python-Programmer/                   Annual Computer Security Applications Conference. 824–836.
     aero [Accessed: 2024-05-20].                                                           [27] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R Lyu. 2021.
 [3] Hussain MJ Almohri and David Evans. 2018. Fidelius charm: Isolating unsafe rust             Memory-safety challenge considered solved? An in-depth study with all Rust
     code. In Proceedings of the Eighth ACM Conference on Data and Application                   CVEs. ACM Transactions on Software Engineering and Methodology (TOSEM)
     Security and Privacy. 248–255.                                                              31, 1 (2021), 1–25.
 [4] Vytautas Astrauskas, Aurel Bílỳ, Jonáš Fiala, Zachary Grannan, Christoph Math-        [28] Zeming Yu, Linhai Song, and Yiying Zhang. 2019. Fearless concurrency? un-
     eja, Peter Müller, Federico Poli, and Alexander J Summers. 2022. The prusti project:        derstanding concurrent programming safety in real-world rust software. arXiv
     Formal verification for rust. In NASA Formal Methods Symposium. Springer, 88–               preprint arXiv:1902.01906 (2019).
     108.
 [5] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexan-
     der J Summers. 2020. How do programmers use unsafe Rust? Proceedings of the
     ACM on Programming Languages 4, OOPSLA (2020), 1–27.
 [6] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021.
     Rudra: Finding memory safety bugs in rust at the ecosystem scale. In Proceedings
     of the ACM SIGOPS 28th Symposium on Operating Systems Principles. 84–99.
 [7] Kevin Boos, Namitha Liyanage, Ramla Ijaz, and Lin Zhong. 2020. Theseus: an
     experiment in operating system structure and state management. In 14th USENIX
     Symposium on Operating Systems Design and Implementation (OSDI 20). 1–19.
 [8] Anton Burtsev, Dan Appel, David Detweiler, Tianjiao Huang, Zhaofeng Li, Vikram
     Narayanan, and Gerd Zellweger. 2021. Isolation in Rust: What is Missing?. In
     Proceedings of the 11th Workshop on Programming Languages and Operating
     Systems. 76–83.
 [9] Asterinas Contributors. 2024. Asterinas - A Rust-based operating system. https:
     //github.com/asterinas/asterinas [Accessed: 2024-05-20].
[10] rCore Contributors. 2024. rCore operating system. https://github.com/rcore-
     os/rCore [Accessed: 2024-05-20].
[11] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: Detect-
     ing memory deallocation bugs of rust programs via static data-flow analysis. ACM
     Transactions on Software Engineering and Methodology 32, 4 (2023), 1–21.
[12] Mohan Cui, Shuran Sun, Hui Xu, and Yangfan Zhou. 2024. Is unsafe an Achilles’
     Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Pro-
     gramming. In Proceedings of the IEEE/ACM 46th International Conference on
     Software Engineering. 1–13.
[13] Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust used safely
     by software developers?. In Proceedings of the ACM/IEEE 42nd International
     Conference on Software Engineering. 246–257.
[14] Kelsey R Fulton, Anna Chan, Daniel Votipka, Michael Hicks, and Michelle L
     Mazurek. 2021. Benefits and drawbacks of adopting a secure programming
     language: Rust as a case study. In Seventeenth Symposium on Usable Privacy
     and Security (SOUPS 2021). 597–616.
[15] Rust Group. 2024. How Safe and Unsafe Interact. https://doc.rust-lang.org/
     nomicon/safe-unsafe-meaning.html [Accessed: 2024-06-07].
[16] Rust Group. 2024. Unsafe Rust. https://doc.rust-lang.org/book/ch19-01-unsafe-
     rust.html [Accessed: 2024-06-07].
[17] Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2019. Stacked
     borrows: an aliasing model for Rust. Proceedings of the ACM on Programming
     Languages 4, POPL (2019), 1–32.
[18] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. Rust-
     Belt: Securing the foundations of the Rust programming language. Proceedings
     of the ACM on Programming Languages 2, POPL (2017), 1–34.
[19] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John CS Lui. 2021. MirChecker:
     detecting bugs in Rust programs via static analysis. In Proceedings of the 2021
     ACM SIGSAC conference on computer and communications security. 2183–
     2196.
[20] Peiming Liu, Gang Zhao, and Jeff Huang. 2020. Securing unsafe rust programs
     with XRust. In Proceedings of the ACM/IEEE 42nd International Conference on
     Software Engineering. 234–245.
[21] Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer.
     2022. RustHornBelt: a semantic foundation for functional verification of Rust pro-
     grams with unsafe code. In Proceedings of the 43rd ACM SIGPLAN International
     Conference on Programming Language Design and Implementation. 841–856.
[22] Ian McCormack, Tomas Dougan, Sam Estep, Hanan Hibshi, Jonathan Aldrich, and
     Joshua Sunshine. 2024. " Against the Void": An Interview and Survey Study on
     How Rust Developers Use Unsafe Code. arXiv preprint arXiv:2404.02230 (2024).
[23] Vikram Narayanan, Tianjiao Huang, David Detweiler, Dan Appel, Zhaofeng Li,
     Gerd Zellweger, and Anton Burtsev. 2020. { RedLeaf } : isolation and commu-
     nication in a safe operating system. In 14th USENIX Symposium on Operating
     Systems Design and Implementation (OSDI 20). 21–39.
[24] Boqin Qin, Yilun Chen, Haopeng Liu, Hua Zhang, Qiaoyan Wen, Linhai Song,
     and Yiying Zhang. 2024. Understanding and Detecting Real-World Safety Issues
     in Rust. IEEE Transactions on Software Engineering (2024).
[25] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Under-
     standing memory and thread safety practices and issues in real-world Rust pro-
     grams. In Proceedings of the 41st ACM SIGPLAN Conference on Programming
