                                                                       Fuzz Driver Synthesis for Rust Generic APIs
                                                             Yehong Zhang                                                        Jun Wu                                         Hui Xu∗
                                               School of Computer Science, Fudan                             School of Computer Science, Fudan                  School of Computer Science, Fudan
                                                           University                                                    University                                         University
                                                            China                                                         China                                              China
                                                yehongzhang23@m.fudan.edu.cn                                       junwu@fudan.edu.cn                                   xuh@fudan.edu.cn

                                         ABSTRACT                                                                                      ACM Reference Format:
                                         Fuzzing is a popular bug detection technique achieved by testing                              Yehong Zhang, Jun Wu, and Hui Xu. 2018. Fuzz Driver Synthesis for Rust
                                                                                                                                       Generic APIs. In Proceedings of arxiv pre-print versions (arxiv 2023). ACM,
                                         software executables with random inputs. This technique can also
                                                                                                                                       New York, NY, USA, 11 pages. https://doi.org/XXXXXXX.XXXXXXX
arXiv:2312.10676v2 [cs.SE] 19 Dec 2023




                                         be extended to libraries by constructing executables that call library
                                         APIs, known as fuzz drivers. Automated fuzz driver synthesis has
                                         been an important research topic in recent years since it can facili-                         1    INTRODUCTION
                                         tate the library fuzzing process. Nevertheless, existing approaches                           Fuzzing is an automated technique for bug detection [12]. It tests
                                         generally ignore generic APIs or simply treat them as normal APIs.                            a target executable program with random input and mutates the
                                         As a result, they cannot generate effective fuzz drivers for generic                          input according to the feedback information, such as code coverage.
                                         APIs.                                                                                         The technique can also be applied to library code by constructing
                                            This paper studies the automated fuzz driver synthesis prob-                               executables that call the APIs of the library, known as fuzz drivers or
                                         lem for Rust libraries with generic APIs. The problem is essential                            fuzz targets. Due to its effectiveness and practicability, fuzzing has
                                         because Rust emphasizes security, and generic APIs are widely                                 been widely employed by both industries [7, 20] and open-source
                                         employed in Rust crates. Each generic API can have numerous                                   communities [13, 22].
                                         monomorphic versions as long as the type constraints are satis-                                  In this paper, we investigate library fuzzing for Rust libraries,
                                         fied. The critical challenge to this problem lies in prioritizing these                       with a specific focus on addressing the automated fuzz driver syn-
                                         monomorphic versions and providing valid inputs for them. To                                  thesis problem for generic APIs. The problem is important because
                                         address the problem, we extend existing API-dependency graphs to                              Rust is a system programming language that places a strong empha-
                                         support generic APIs. By solving such dependencies and type con-                              sis on security and robustness. Bugs within Rust libraries have the
                                         straints, we can generate a collection of candidate monomorphic                               potential to impact all downstream code. Generic APIs are widely
                                         APIs. Further, we apply a similarity-based filter to prune redundant                          employed in Rust libraries, offering developers a viable means to
                                         versions, particularly if multiple monomorphic APIs adopt the iden-                           avoid repetitively implementing the same API for different types.
                                         tical trait implementation. Experimental results with 29 popular                              A generic API generally has one or multiple parameters of generic
                                         open-source libraries show that our approach can achieve promis-                              types e.g., T, which will be monomorphized to concrete types upon
                                         ing generic API coverage with a low rate of invalid fuzz drivers.                             invocation. However, existing work on fuzz driver synthesis (e.g.,
                                         Besides, we find 23 bugs previously unknown in these libraries,                               RULF [10]) often neglects generic APIs or treats them merely as
                                         with 18 bugs related to generic APIs.                                                         non-generic APIs. As a result, it either falls short in generating
                                                                                                                                       valid fuzz drivers for generic APIs or fails to produce diversified
                                         CCS CONCEPTS                                                                                  monomorphic versions for the same generic API.
                                         • Software and its engineering → Software defect analysis;                                       A prevailing approach to automated fuzz driver synthesis in-
                                         Automated static analysis; • Security and privacy → Software                                  volves traversing API-dependency graphs [10]. However, when
                                         security engineering.                                                                         attempting to apply the method to generic APIs, two significant
                                                                                                                                       challenges emerge. Firstly, the type system of Rust is very powerful
                                         KEYWORDS                                                                                      if not Turing-complete [11], leading to intricate dependencies for
                                                                                                                                       generic APIs and the difficulty of synthesizing valid API calls. In
                                         Fuzzing, Program Synthesis, Rust
                                                                                                                                       particular, one generic API may involve several type parameters
                                                                                                                                       (e.g., T, U, G), and each type parameter could be employed by
                                         ∗ Corresponding author.                                                                       several generic arguments (e.g., a:T, b:Vec<T>) of the function.
                                                                                                                                       To choose a concrete type (e.g., i32) for the generic type T, we
                                                                                                                                       should ensure that all these required concrete types (e.g., a:i32,
                                         Permission to make digital or hard copies of all or part of this work for personal or
                                         classroom use is granted without fee provided that copies are not made or distributed         b:Vec<i32>) can be produced by other APIs. Besides, these generic
                                         for profit or commercial advantage and that copies bear this notice and the full citation     parameters should satisfy trait bounds, which may either bound
                                         on the first page. Copyrights for components of this work owned by others than ACM            the type parameters or generic parameters. Secondly, there could
                                         must be honored. Abstracting with credit is permitted. To copy otherwise, or republish,
                                         to post on servers or to redistribute to lists, requires prior specific permission and/or a   be numerous or even an infinite number of monomorphic APIs for
                                         fee. Request permissions from permissions@acm.org.                                            a generic API. Fuzzing all these variations is impractical due to the
                                         arxiv 2023, ,                                                                                 time-intensive nature of the process. Note that it may take several
                                         © 2018 Association for Computing Machinery.
                                         ACM ISBN 978-1-4503-XXXX-X/18/06. . . $15.00                                                  hours or days to fuzz one monomorphic API. Therefore, we need
                                         https://doi.org/XXXXXXX.XXXXXXX                                                               to prioritize these monomorphic APIs and select a feasible number
arxiv 2023, ,                                                                                                      Yehong Zhang, Jun Wu, and Hui Xu


of APIs for fuzzing. To the best of our knowledge, no existing work       interfaces declared in the trait. Based on the concept of trait, Rust
has tackled these challenges.                                             provides a type constraint mechanism for the generic API called
   This paper introduces a novel approach to automatically syn-           trait bounds[17]. A type parameter can specify the trait bounds to
thesize fuzz drivers for generic APIs. To tackle the first challenge,     require the concrete type for this type parameter must implement
we carefully model the type constraint of generic types and extend        the specific traits. If the type for the type parameter unsatisfies the
the classic API dependency graph with generic APIs and types. By          requirement, the compiler will report a compilation error. On the
traversing the graph and solving type constraints, we can find all        other hand, as the compiler only accepts the type implementing
potential monomorphic APIs for creating fuzz drivers. In address-         these traits, the developer can safely invoke the interface of the
ing the second challenge, we design a similarity-based pruning            traits for this type parameter in generic API. Trait bounds in Rust are
method to reduce the number of monomorphic APIs for fuzzing.              composable, meaning if you want to specify that a type parameter
Specifically, our method considers two concrete types as similar if       T must implement both trait A and B, you can use the syntax T:A +
they share the same trait implementation, indicating congruence           B to express this requirement. Rust also provides a "where" clause,
in the behavior of the generic API.                                       which allows programmers to declare trait bounds on any type or
   We have implemented a prototype, named RULF+, building upon            associated types[15]. This feature empowers Rust programmers to
the state-of-the-art tool RULF, which lacks support for generic           write type constraints flexibly and expressively.
APIs. Our tool consists of 3K+ lines of Rust code, excluding the             Figure 1 gives an example showing the usage of the generic API
original RULF code. To assess the effectiveness of our approach,          and the type in Rust. map_vec is a generic API with two type param-
we conduct experiments with 29 open-source libraries, including           eters T and U. It receives an input with Vec<T> type, converts T to U,
10 libraries randomly selected from Trophy-case[2] and 19 other           and returns Vec<U>. The API declares a trait bound U: From<T> to
libraries randomly chosen from GitHub with 100+ stars and 5+              ensure that the type of T is capable of converting to the type of U.
generic APIs. Experimental results show that our approach can             This trait bound also allows us to invoke the U::from(item) API
achieve promising generic API coverage if the library does not            to convert an item of type T to U. Line 8-9 shows the compiler ac-
depend on other third-party libraries. Furthermore, it generates a        cepts map_vec::<u8,i32> and rejects map_vec::<i32,u8>, since
limited number of fuzz drivers, and most of the drivers are valid.        i32 implements From<u8> but u8 does not implement From<i32>.
Subsequently, we employ AFL++ to fuzz these drivers and find
23 bugs, including 18 bugs related to generic APIs. These results
demonstrate that despite we have pruned numerous monomorphic               1    fn map_vec<T, U: From<T>>(vec: Vec<T>) -> Vec<U> {
APIs for efficiency, our approach is still able to discover bugs with      2        let mut ret=Vec::new();
                                                                           3        for item in vec.into_iter(){
carefully selected monomorphic APIs.                                       4            ret.push(U::from(item));
   We summarize our contributions as follows.                              5        }
      • This paper serves as the first attempt to study the fuzz driver    6        ret
                                                                           7    }
        synthesis problem for Rust generic APIs. We systematically         8    let _ = map_vec::<u8,i32>(vec![0u8]); // accept
        model the type constraints and API dependencies of generic         9    let _ = map_vec::<i32,u8>(vec![0i32]); // compile fail
        APIs. Moreover, we propose a novel algorithm to solve these
        constraints and dependencies in order to generate valid fuzz
                                                                                     Figure 1: Example of generic usage in Rust.
        drivers. Experimental results show that our approach can
        achieve promising generic API coverage with a high rate of
        valid cases.
                                                                             The paradigm of generic programming is immensely powerful,
      • We propose a novel similarity-based approach to prune re-
                                                                          yet it introduces a new security issue during the process of soft-
        dundant monomorphic APIs. Experimental results show that
                                                                          ware development. To support generic programming, compilers
        the remaining APIs are still able to discover bugs, although
                                                                          implicitly generate multiple monomorphic APIs for a generic API
        their numbers are limited.
                                                                          based on the needed type in the process of monomorphization. An
      • We have developed a tool, RULF+, and open-source released
                                                                          elusive bug can hide on a certain monomorphic API and cannot be
        it to the community.
                                                                          detected in other monomorphic APIs. Due to the transparency of
                                                                          the monomorphization process to programmers, it is difficult for
2 PROBLEM                                                                 them to discover and test such bugs.
2.1 Generic Type and Generic API
Rust provides three types of generic parameters: type, constant, and      2.2     Fuzz Driver Synthesis with Generic API
lifetime[15]. However, in this paper, the term "generic" primarily        2.2.1 Generic API Dependency Graph. We extend the API depen-
refers to type generic parameters. This is because identifying type       dency graph to a generic API dependency graph so that we can
parameters is crucial for testing generic APIs. In Rust, type param-      model all APIs, including generic APIs and dependencies among
eters can be used in the definitions of types, enums, and traits as       them.
substitutes for a specific type.
    Rust provides trait[18] to describe an abstract interface that           Definition 2.1 (generic API dependency graph). A generic API
types can implement. Trait can be regarded as a set of interface          dependency graph is defined as a directed graph G = (𝑁𝐴 , 𝑁𝑇 , 𝐸)
declarations. A type can implement a trait by implementing all            that:
Fuzz Driver Synthesis for Rust Generic APIs                                                                                             arxiv 2023, ,


                                                                                Figure 3 demonstrates a generic API dependency graph for an
                                                                             example library. The library source code is shown in figure 2. The
                              𝑁𝐴 = 𝐴 ∪ A
                                                                             graph contains 2 non-generic nodes and 3 generic nodes. There
                              𝑁𝑇 = 𝑇 ∪ T                                     are 2 concrete types Ty1, Ty2 and 2 generic types T and Vec<T>.
                                 𝐸 =𝐶 ∪𝑃 ∪𝑀                                  The consumer and producer edges are constructed by the input
      where:                                                                 types and return types for each API. Finally, there are two match
                                                                             edges(Ty1→ T, Ty2→ T) that represent both Ty1 and Ty2 can match
       • 𝐴 is the set of non-generic API nodes.
                                                                             with generic type T.
       • A is the set of generic API nodes.
       • 𝑇 is the set of non-generic type nodes.                             2.2.2 The Challenges of Fuzz Driver Synthesis. A fuzz driver for a
       • T is the set of generic type nodes.                                 library can be viewed as a sequence of library API calls. Thus, we
       • 𝐶 is the set of consumer edges, where 𝐶 ⊆ 𝑁𝐴 × 𝑁𝑇 .                 model the task of fuzz driver synthesis as the task of API sequence
       • 𝑃 is the set of producer edges, where 𝑃 ⊆ 𝑁𝑇 × 𝑁𝐴 .                 generation.
       • 𝑀 is the set of match edges, where 𝑀 ⊆ 𝑇 × T .
                                                                               Definition 2.2 (API Sequence). An API sequence is a list of APIs.
   The definition of 𝐴, A, 𝑇 , T is obvious. We distinguish three            For example, 𝑆 = [𝑎𝑝𝑖 1, 𝑎𝑝𝑖 2, · · · , 𝑎𝑝𝑖𝑛 ] is an API sequence.
types of edges in the generic API dependency graph. The consumer                Definition 2.3 (Reachable API). An API in the API sequence is said
edge 𝑡 → 𝑎 represents API 𝑎 requires an instance of type 𝑡. The pro-         to be reachable if each of its input satisfy any one of the following
ducer edge 𝑎 → 𝑡 represents API 𝑎 produce(or return) an instance             criteria:
of type 𝑡. Note that for consumer and producer edges, if 𝑎 ∈ 𝐴, then
                                                                                  • The type of this input is primitive.
we have 𝑡 ∈ 𝑇 , since the non-generic API cannot consume or pro-
                                                                                  • The type of input is non-generic, and there exists a producer
duce a generic type. The match edge 𝑡 1 → 𝑡 2 represents a concrete
                                                                                     edge from any previous API in the API sequence to this input
type 𝑡 1 that can match the generic type 𝑡 2 , that is, type 𝑡 1 may serve
                                                                                     type.
as an instance of type 𝑡2. For example, Box<i32> can match Box<T>,
                                                                                  • The type of input is generic, and there exists a concrete type
but Vec<i32> cannot match Box<T>. The match edges serve as a
                                                                                    𝑡 that exists a producer edge from any previous API in the
bridge between the concrete type and the generic type, and it is
                                                                                    API sequence to type 𝑡 and exists a match edge from 𝑡 to this
crucial when we try to infer the generic API dependency.
                                                                                     input type.

 1     struct Ty1;                                                              Definition 2.4 (Valid API Sequence). An API sequence is said to
 2     struct Ty2;                                                           be valid if all APIs in this sequence are reachable.
 3     trait A{}
 4     trait B{}                                                                To synthesize valid fuzz drivers, we have to generate correspond-
 5     impl A for Ty1 {}                                                     ing valid API sequences. A valid API sequence ensures that all APIs
 6     impl A for Ty2 {}                                                     can obtain instances of their input types from previous APIs or the
 7     impl B for Ty2 {}                                                     fuzzer so that the fuzz driver can be compiled successfully. However,
 8     fn f1() -> Ty1;
 9     fn f2() -> Ty2;
                                                                             the generic APIs in a valid API sequence should be replaced with
 10    fn f3<T:A>(a1:T)->T;                                                  specific monomorphic APIs so that we can determine the exact data
 11    fn f4<T> (a1:T)->Vec<T>;                                              dependencies. In other words, we should determine the concrete
 12    fn f5<T:A+B> (a1:Vec<T>);                                             types for every type parameter in the generic API and ensure the
                                                                             type combination for type parameters can satisfy the trait bounds
           Figure 2: Source code for an example library.                     of the generic API.
                                                                                This process contains several challenges to the API sequence
                                                                             generation that no previous work has tackled. We summarize two
                                                                             fundamental challenges as follows:
                                                                                Selecting monomorphic APIs for generic APIs. The type sys-
                                                                             tem of Rust is very powerful, leading to the difficulties of selecting
                                                                             a reachable and valid monomorphic API for a generic API. In partic-
                                                                             ular, the generic API dependency graph is not steadfast but keeps
                                                                             changing during the monomorphization process. The number of
                                                                             type nodes t would continuously grow because there could be a
                                                                             number of new types generated if the return type of a generic API
                                                                             is generic. For example, in the example library of Figure 3, calling
                                                                             f1,f4 sequentially can produce type Vec<Ty1>, which have not
                                                                             appeared in the graph before. This constructs two new match edges
                                                                             Vec<Ty1>→Vec<T> and Vec<Ty1>→T.
                                                                                Furthermore, there could be complicated trait bounds. The trait
                                                                             bounds can either be applied to type parameters (e.g., T:Bound1) or
      Figure 3: Generic API dependency graph for figure 2.                   generic parameter types (e.g., where Vec<T>:Bound1). One generic
arxiv 2023, ,                                                                                                       Yehong Zhang, Jun Wu, and Hui Xu




                                                   Figure 4: Overview of our approach.


API may have multiple generic parameters and trait bounds, and          3.2    Reachable Monomorphic API Search
these bounds could be related to each other. Searching valid concrete   We start by defining several concepts to introduce our algorithm.
types based on the generic API dependency graph and satisfying
all bounds is not easy.                                                    Definition 3.1 (Monomorphic solution). A monomorphic solution
                                                                        of a generic API refers to a specific substitution scheme for all type
   Monomorphic API explosion. The number of valid monomor-              parameters in the generic API. Formally, we present a monomorphic
phic APIs can be large or even infinite, making it impractical to       solution as a tuple (𝑡 1, 𝑡 2, . . . ), where 𝑡𝑖 represents the concrete type
cover all monomorphic APIs in fuzzing. Supposing a generic API          to replace the i-th type parameter. The type parameter is ordered
has 𝑚 generic parameters, and each type parameters has 𝑛 valid          by the declared order.
monomorphic versions, the number of valid monomorphic versions             Example. A monomorphic solution for API foo<T,U>(T)->U can
for the API is exponential to 𝑚, i.e., 𝑛𝑚 . Besides, a generic API      be (f32,i32), which means to substitute T with concrete type f32
returning a generic type can produce an infinite number of new          and U with i32. This monomorphic solution also corresponds to a
types. Taking Figure 3 as an instance, repeatedly passing the return    monomorphic API foo(f32)->i32.
type of f4 as an input to itself, we can produce type Vec<Ty1>,
Vec<Vec<Ty1>>, etc.                                                        Definition 3.2 (Top and bottom). We use ⊤ to represent an arbi-
                                                                        trary type for a type parameter, and ⊥ to represent a bottom type
3 APPROACH                                                              for a type parameter.

3.1 Overview                                                               Example. For function foo<T,U>(T,U), (⊤,⊤) represents ar-
                                                                        bitrary type combination for type parameters is valid. For func-
Figure 4 overviews our approach. We propose a two-stage approach
                                                                        tion foo<T:A,U:A>(T,U), (⊥,⊥) represents no type combination
to tackle two challenges. To tackle the first challenge, we apply
                                                                        for parameters is valid. The merge and union operation for the
the reachable monomorphic API search to resolve all valid and
                                                                        monomorphic solution set with ⊤ is also similar, by treating ⊤ as
reachable monomorphic APIs. Our reachable monomorphic API
                                                                        an arbitrary type that can match any type. For instance, {(⊤, 𝑖32)}∩
search infers the possible monomorphic APIs from the match edge
                                                                        {(𝑓 32, 𝑖32)} = {(𝑓 32, 𝑖32)}, {(⊤, 𝑖32)} ∪ {(𝑓 32, 𝑖32)} = {(⊤, 𝑖32)}.
from the reachable concrete type to the generic arguments of the
                                                                        For ⊥, we regard ⊥ can not matching with any type. For instance,
generic API. This is crucial to our approach since it ensures the
                                                                        {(⊥, ⊥)} ∩ {(𝑖32, 𝑓 32), (𝑓 8, 𝑖8)} = {(𝑖32, 𝑓 32), (𝑓 8, 𝑖8)}.
reachability of generated monomorphic APIs and avoids enumer-
ations of all possible type combinations. We also apply the trait           Definition 3.3 (Match function). we define function Match(𝑡 1 ,𝑡 2 ),
bounds check in the reachable monomorphic API search to ensure          where 𝑡 1 ∈ 𝑇 , 𝑡 2 ∈ T and 𝑡 is a generic argument for a generic API
all generated monomorphic APIs are valid. After searching, the          𝑔𝑎𝑝𝑖. If 𝑡 1 → 𝑡 2 ∉ 𝑀, then the match function returns (⊥, ⊥). If
generic API dependency graph is transformed into a monomorphic          𝑡 1 → 𝑡 2 ∈ 𝑀, the match function returns a possible monomorphic
API dependency graph. To tackle the second challenge, we apply          solution for 𝑔𝑎𝑝𝑖 regarding 𝑡 1 as the concrete type of 𝑡 2 .
similarity pruning to reduce the number of monomorphic APIs.
                                                                           Example. for function foo<T,U>(Vec<T>,U), Match(Vec<i32>,
We identify similar behaviors among monomorphic APIs. If two
                                                                           Vec<T>) returns (i32,⊤), and Match(Box<i32>,Vec<T>) re-
monomorphic APIs share the same implementation, we consider
                                                                        turns (⊥,⊥), as Vec<T> and Box<i32> has different outer type.
them similar. Based on this assumption, we prune monomorphic
APIs to reduce redundant testing of similar behaviors. We obtain        3.2.1 Algorithm. To meet the requirement of validity and reacha-
a refined monomorphic API dependency graph after this stage. Fi-        bility, We propose an iterative algorithm for obtaining reachable
nally, we do API sequence generation and fuzz driver synthesis          monomorphic solution sets for all generic APIs by utilizing the
based on RULF. We introduce this stage in the next section.             reachable information from type dependencies. our algorithm first
Fuzz Driver Synthesis for Rust Generic APIs                                                                                      arxiv 2023, ,


  Algorithm 1: reachabable monomorphic API search                       set. Since type in 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 can be instantiated in some API
   Input : Set of non-generic API nodes: 𝐴,                             sequences, for all monomorphic solutions in this set, it must be
            Set of generic API nodes: A,                                reachable in some API sequences. However, some monomorphic
            Set of producer edges: 𝑃,                                   solutions may only be reachable for partial generic arguments in a
            Set of consumer edges: 𝐶,                                   generic API. Consequently, we merge the monomorphic solution
            Depth limit of nested type: 𝑚𝑎𝑥𝐷𝑒𝑝𝑡ℎ                        sets for each generic API, yielding the largest common monomor-
   Output : Set of reachable monomorphic solutions for each             phic solution set (line 13).
            generic API: 𝑀𝑂 (𝑔𝑎𝑝𝑖)                                         Figure 5 offers an example to better illustrate the union and
 1 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 = ∅;
                                                                        merge processes of monomorphic solution sets. Step 1 initiates the
 2 repeat
                                                                        largest common monomorphic set 𝑠. Steps 2-7 perform match for
 3    for 𝑎𝑝𝑖 ∈ 𝐴 do                                                    𝑝1 and all types in 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒𝑠 and perform a union opera-
 4        if IsReachable(api) then                                      tion. Steps 8-11 and step 12-15 repeat the same logic as steps 2-7
 5            for 𝑎𝑝𝑖 → 𝑟𝑒𝑡𝑢𝑟𝑛𝑇𝑦𝑝𝑒 ∈ 𝑃 do                               for 𝑝2 and 𝑝3, respectively. In step 15 we obtain the final largest
 6                𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 =                                       common monomorphic solution set 𝑠 = {(u8,i32)}, meaning only
                                                                        (u8,i32) is a valid and reachable monomorphic API for the generic
                   𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 ∪ 𝑟𝑒𝑡𝑢𝑟𝑛𝑇𝑦𝑝𝑒;
                                                                        API.
 7    for 𝑔𝑎𝑝𝑖 ∈ A do
 8        𝑠 = {(⊤, ⊤, · · · )};
 9        for 𝑝 → 𝑔𝑎𝑝𝑖 ∈ 𝐶 do
10            if IsGeneric(𝑝) then
11                𝑚𝑜 ={(⊥, ⊥, · · · )};
12                for 𝑡𝑦 ∈ 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 do
13                    𝑚𝑜 = 𝑚𝑜∪ Match(ty,p);
14                𝑠 = 𝑠 ∩ 𝑚𝑜;
15        for 𝑚𝑜 ∈ 𝑠 do
16            if SatisfyTraitBounds(𝑚𝑜, 𝑔𝑎𝑝𝑖) then
17                𝑚𝑎𝑝𝑖 =MonoAPI(𝑚𝑜, 𝑔𝑎𝑝𝑖);
18                if IsReachable(mapi) then
19                    𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 =
                        𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 ∪ 𝑚𝑎𝑝𝑖.𝑟𝑒𝑡𝑢𝑟𝑛𝑇𝑦𝑝𝑒;
20                    𝑀𝑂 (𝑔𝑎𝑝𝑖) = 𝑀𝑂 (𝑔𝑎𝑝𝑖) ∪ 𝑚;
                                                                        Figure 5: Example of applying algorithm 1. All ⊤ notions are
21 until 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 remains unchanged;
                                                                        marked red.

                                                                           To ensure the validity of the monomorphic solutions, we em-
searches the set of monomorphic solutions for each generic ar-          ploy a trait bounds check for each monomorphic solution (line
gument for generic APIs. Then our algorithm merges all sets of          15). Note that we still need to check the reachability for each
monomorphic solutions for a generic API, getting the largest com-       monomorphic API, since the non-generic argument in the API may
mon monomorphic solutions set. The monomorphic solutions in             be unreachable. To ensure the algorithm will not generate infinite
this set ensure the reachability of each generic input. We then check   monomorphic solutions for some generic APIs, we set a maximum
trait bounds to ensure the validity of monomorphic solutions. We        threshold 𝑚𝑎𝑥𝐷𝑒𝑝𝑡ℎ for type nested and prohibit generating the
discuss the details of the algorithm below.                             monomorphic solution containing types that exceed this thresh-
    Algorithm 1 introduces our algorithm. We define 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒       old. It is reasonable for generating fuzz drivers, as overly complex
as the set of reachable types that our algorithm has found. Once        monomorphic APIs typically do not increase code coverage.
we find a new reachable API (non-generic API or monomorphic
API), we add the return type of the API to 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒. The main      3.3    Similarity Pruning
loop (line 2-21) continues to run until 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒 remains un-       Intuitively, the total number of codes(or implementations) is lim-
changed. In each iteration, the algorithm tries to find new reachable   ited, so that there may be some monomorphic APIs share the same
APIs for non-generic API and generic API, respectively. First, the      implementation. Thus, their behavior may be similar in a generic
algorithm checks all non-generic APIs whether it is reachable now.      API with certain trait bounds. We analyzed real-world libraries
If an API is reachable, then we add the return type of this API to      and identified two common practices that lead to similar behaviors:
the 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒𝑠 (line 3-5).                                          blanket implementation and default implementation. Figure 6 is
    Then the algorithm checks whether a new monomorphic solu-           an example of how these common practices create similar behav-
tion for a generic API is reachable. We check each argument for         iors. Trait Foo provides a default implementation for method foo.
each generic API. If the argument is generic, we perform Match          When type A and B implement Foo, they do not provide a specific
between this generic argument and all types in 𝑟𝑒𝑎𝑐ℎ𝑎𝑏𝑙𝑒𝑇𝑦𝑝𝑒𝑠           implementation for foo, resulting in sharing the same default im-
and we union the returning set from Match (line 8-13) to a larger       plementation. On the other hand, the example employs a blanket
arxiv 2023, ,                                                                                                    Yehong Zhang, Jun Wu, and Hui Xu


implementation that provides the implementation of Bar for both             Algorithm 2: Similarity Pruning
A and B, resulting in similar behaviors.                                     Input : Set of non-generic API nodes: 𝐴,
                                                                                      Set of generic API nodes: A,
  1   struct A;                                                                       Set of producer edges: 𝑃,
  2   struct B;                                                                       Set of reachable monomorphic solutions for each
  3   trait Foo{
                                                                             generic API: 𝑀𝑂 (𝑔𝑎𝑝𝑖)
  4       fn foo()->&'static str { "default impl for Foo" }
  5   }                                                                      Output : Set of reserved API 𝑅
  6   trait Bar{                                                           1 𝑟𝑒𝑞𝑢𝑖𝑟𝑒𝑇𝑦𝑝𝑒 = ∅, 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑇𝑦𝑝𝑒 = ∅;
  7       fn bar()->&'static str;
  8   }                                                                    2  for 𝑔𝑎𝑝𝑖 ∈ A do
  9   // Situation 1: similar behavior by default implementation           3      GetMinimalSetCover(gapi);
 10   impl Foo for A {}                                                     4 repeat
 11   impl Foo for B {}
                                                                            5     for 𝑎𝑝𝑖 ∈ 𝐴 do
 12   // Situation 2: similar behavior by blanket implementation
 13   impl<T:Foo> Bar for T{                                                6         TryReserveAPI(api, requireType, produceType);
 14       fn bar() -> &'static str { "blanket impl for Bar" }               7     for 𝑔𝑎𝑝𝑖 ∈ A do
 15   }                                                                     8         for 𝑚𝑜 ∈ 𝑀𝑂 (𝑔𝑎𝑝𝑖) do
                                                                            9            𝑚𝑎𝑝𝑖 =MonoAPI(mo, gapi);
Figure 6: Example of how default and blanket implementa-                   10             TryReserveAPI(mapi, requireType,
tion create similar behaviors.                                                             produceType);
                                                                           11 until reserveType and produceType remain unchanged;

   In the context of fuzzing, repeatedly testing similar behaviors         12 Function GetMinimalSetCover(gapi):
can lead to low efficiency. Therefore, we propose a novel prun-            13    𝑐𝑜𝑣𝑒𝑟𝑒𝑑 = ∅, 𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑 = ∅;
ing algorithm to remove similar monomorphic APIs, reducing the             14    repeat
number of generated drivers and improving fuzzing efficiency.              15        𝑠𝑒𝑙𝑒𝑐𝑡𝑀𝑜𝑛𝑜 =MaxUncover(𝑀𝑔𝑎𝑝𝑖 − 𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑,
3.3.1 Algorithm. The idea of our algorithm is to cover all imple-                      covered, gapi);
mentations with the minimum number of monomorphic solutions,               16        𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑 = 𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑 ∪ 𝑠𝑒𝑙𝑒𝑐𝑡𝑀𝑜𝑛𝑜;
since testing the same implementation across multiple fuzz drivers         17        𝑐𝑜𝑣𝑒𝑟𝑒𝑑 = 𝑐𝑜𝑣𝑒𝑟𝑒𝑑 ∪ 𝐼𝑚𝑝𝑙𝑠 (𝑔𝑎𝑝𝑖, 𝑠𝑒𝑙𝑒𝑐𝑡𝑀𝑜𝑛𝑜)
may be inefficient. The algorithm initially treats all APIs as non-        18    until no monomorphism is selected;
preserved APIs, subsequently selecting the minimum number of               19    if 𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑 ⊆ ∅ then
monomorphic APIs for each generic API to cover all implementa-             20        𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑 = 𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑∪RandomSelectOne(𝑀𝑔𝑎𝑝𝑖 );
tions under the generic API trait bounds. To maintain the reach-           21    for 𝑚 ∈ 𝑠𝑒𝑙𝑒𝑐𝑡𝑒𝑑 do
ability of reserved monomorphic APIs, we also reserve APIs that            22        AddReserveAPI(MonoAPI(m,gapi));
can produce instances for the argument of reserved APIs, until all
                                                                           23 Function TryReserveAPI(api):
arguments of reserved APIs are reachable.
                                                                           24    if 𝑎𝑝𝑖 ∉ 𝑅 then return;
    Definition 3.4 (Trait implementation set). We define 𝐼𝑚𝑝𝑙𝑠 (𝑔𝑎𝑝𝑖, 𝑚)   25    𝑠𝑢𝑐𝑐𝑒𝑠𝑠 = 𝐹𝑎𝑙𝑠𝑒;
as the set of trait implementations of the monomorphic solution 𝑚          26    for 𝑡𝑦 ∈ 𝑟𝑒𝑞𝑢𝑖𝑟𝑒𝑇𝑦𝑝𝑒 do
for the generic API 𝑔𝑎𝑝𝑖. A trait implementation 𝑖 ∈ 𝐼𝑚𝑝𝑙𝑠 (𝑔𝑎𝑝𝑖, 𝑚)       27        if 𝑡𝑦 ∉ 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑇𝑦𝑝𝑒 then
if the corresponding trait is declared within the trait bounds of the      28            if 𝑎𝑝𝑖 → 𝑡𝑦 ∈ 𝑃 then
generic API.                                                               29                𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑇𝑦𝑝𝑒 = 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑇𝑦𝑝𝑒 ∪ 𝑡𝑦;
   For example, consider API fn foo<T:Tr1,U>(T,U), and 𝑚 1 =               30                𝑠𝑢𝑐𝑐𝑒𝑠𝑠 = 𝑇𝑟𝑢𝑒;
(𝐴, 𝐵), 𝑚 2 = (𝐶, 𝐷). The 𝐼𝑚𝑝𝑙𝑠 (𝑔𝑎𝑝𝑖, 𝑚 1 ) = { A’s implementation        31    if 𝑠𝑢𝑐𝑐𝑒𝑠𝑠 then AddReserveAPI(api) ;
of Tr1}, while 𝐼𝑚𝑝𝑙𝑠 (𝑔𝑎𝑝𝑖, 𝑚 2 ) = ∅. If two monomorphic solutions        32 Function AddReserveAPI(api):

share the same implementation 𝑖, then 𝑖 ∈ 𝐼𝑚𝑝𝑙𝑠 (𝑔𝑎𝑝𝑖, 𝑚 1 ) ∧ 𝑖 ∈         33    𝑅 = 𝑅 ∪ 𝑎𝑝𝑖;
𝐼𝑚𝑝𝑙𝑠 (𝑔𝑎𝑝𝑖, 𝑚 2 ).                                                        34    for 𝑝 ∈ 𝑎𝑝𝑖.𝑎𝑟𝑔𝑠 do
   Algorithm 2 introduces our algorithm. The algorithm starts with         35        𝑟𝑒𝑠𝑒𝑟𝑣𝑒𝑇𝑦𝑝𝑒 = 𝑟𝑒𝑠𝑒𝑟𝑣𝑒𝑇𝑦𝑝𝑒 ∪ 𝑝.𝑡𝑦𝑝𝑒;
an empty reserved API set 𝑅.
   The algorithm first performs GetMinimalSetCover to initialize
𝑅 for each generic API 𝑔𝑎𝑝𝑖 (line 2-3). GetMinimalSetCover re-             that is NP-hard[6], so we use a simple greedy algorithm to select
ceives an generic API 𝑔𝑎𝑝𝑖, select a set cover 𝑆 from 𝑀𝑂 (𝑔𝑎𝑝𝑖)            monomorphic solutions for 𝑔𝑎𝑝𝑖 (line 14-17). In each turn, we select
and add {𝑀𝑜𝑛𝑜𝐴𝑃𝐼 (𝑚𝑜)|𝑚𝑜 ∈ 𝑆 } to the 𝑅. 𝑆 is a set cover that the         𝑚𝑜 with maximum uncovered implementations until all implemen-
union of 𝐼𝑚𝑝𝑙 (𝑚, 𝑔𝑎𝑝𝑖) for all 𝑚 ∈ 𝑆 is equal to the universal set of     tations are covered.
𝑚 ∈ 𝑀𝑂 (𝑔𝑎𝑝𝑖).                                                                As we initialize all APIs as non-reserved, it is possible that
   To reduce the size of the initial 𝑅, we wish to select the mini-        the arguments of these APIs cannot be produced by 𝑎𝑝𝑖 ∈ 𝑅
mal subset of monomorphic solutions that cover a universal set of          temporarily. We conduct an iterative search across all APIs to
implementations. This is known as the set cover problem (SCP)              propagate the reserved types through the backward of producer
Fuzz Driver Synthesis for Rust Generic APIs                                                                                         arxiv 2023, ,


edges (line 4-11). We add all arguments of initial reserved APIs         4.1     Library Information Extraction
to a set 𝑟𝑒𝑞𝑢𝑖𝑟𝑒𝑇𝑦𝑝𝑒, representing the types that we need to find        We collect and process several types of information from the target
other APIs to produce an instance for (line 21-22). To prevent an        library. For non-generic API, we simply collect the API signature.
excessive number of reserved APIs, we add types that have al-            For generic API, we collect the generic API signature, with the
ready found the producer to the 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑇𝑦𝑝𝑒𝑠. During each it-            type parameter declaration and trait bounds declaration. While
eration, if an API or a monomorphic API can produce a type 𝑡𝑦            collecting API information, we regard the implementation of the
that 𝑡𝑦 ∈ 𝑟𝑒𝑞𝑢𝑖𝑟𝑒𝑇𝑦𝑝𝑒𝑠 ∧ 𝑡𝑦𝑝𝑒 ∉ 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑇𝑦𝑝𝑒𝑠, we add this API            same trait for various types as separate APIs. For instance, if A and
to the set of reserved APIs 𝑅 (line 23-31). The iteration runs until     B both implement foo in trait Bar, we regard A::foo and B::foo
𝑟𝑒𝑠𝑒𝑟𝑣𝑒𝑇𝑦𝑝𝑒 and 𝑝𝑟𝑜𝑑𝑢𝑐𝑒𝑇𝑦𝑝𝑒 remain unchanged.                            as two unique APIs. Moreover, we excluded certain common imple-
                                                                         mentations of standard library(std) traits which used for common
4    IMPLEMENTATION                                                      purposes, e.g. Debug and Display traits, as these traits are typically
We implement a prototype called RULF+, since we implement our            unrelated to the primary objectives of the library.
approach based on the codebase of RULF. RULF is a tool that au-             The trait implementation information we collect can be repre-
tomatically generates fuzz drivers for the Rust library. It leverages    sented as a tuple (𝑡𝑦𝑝𝑒, 𝑡𝑟𝑎𝑖𝑡, 𝑖𝑚𝑝𝑙_𝑖𝑑), meaning that 𝑡𝑦𝑝𝑒 imple-
rustdoc[19] to extract all API information from the library, then con-   ments 𝑡𝑟𝑎𝑖𝑡 with 𝑖𝑚𝑝𝑙_𝑖𝑑. 𝑖𝑚𝑝𝑙_𝑖𝑑 is a unique id we extract from
struct an API dependency graph and generate fuzz drivers. However,       rustdoc. If two types share the same implementation as we mention
RULF only extracts non-generic APIs and generates fuzz drivers for       in 3.3, they will get the same 𝑖𝑚𝑝𝑙_𝑖𝑑.
them, without any consideration of generic APIs. We integrate our           As the limitation of rustdoc, we can only gather information
approach with RULF by transforming the generic API dependency            that should be documented. As a result, the third-party API infor-
graph into the refined monomorphic API dependency graph so that          mation, including std API information can not be obtained by our
RULF can work without any type parameter. Besides, we update             tool. However, some std APIs are widely used in public libraries,
the compiler version used by RULF to 1.66.0-dev, enabling our tool       e.g. std::Vec and std::String. To alleviate this situation, we em-
to analyze the latest versions of libraries. We write about 3K+ lines    ployed the re-exports technique[16] in Rust, inserting a small code
of Rust code to implement our approach.                                  snippet to allow us to obtain the std API information. Figure 8 shows
                                                                         the code snippet we insert into the target library. During our exper-
                                                                         iments, we observed that employing this technique substantially
                                                                         enhances API coverage in certain libraries.

                                                                          1    pub use std::vec::Vec;
                                                                          2    pub use std::string::String;
                                                                          3    pub use std::collections::hash_map::DefaultHasher;
                                                                          4    pub use std::io::Write;
                                                                          5    pub use std::io::Read;


                                                                                        Figure 8: Re-exports code snippets.


                                                                         4.2     API Graph Monomorphization
                                                                         Once we collect all the needed information from the target li-
           Figure 7: Workflow of our implementation.                     brary, we start transforming the generic API dependency graph
                                                                         into a monomorphic API dependency graph by applying reachable
                                                                         monomorphic API search and similarity pruning. The approach
   The figure 7 overviews the workflow of our implementation. Our
                                                                         has been fully covered in the previous section, so we only discuss
workflow contains the following steps:
                                                                         several details in this section.
   (1) Library information extraction. We extract API signa-                To apply the reachable monomorphic API search, we need to
        tures, type specifications, and trait implementations from       match types for each generic argument with current reachable types.
        the target library.                                              We predefined a set of transformation rules to increase the success
   (2) API graph monomorphization. We perform reachable                  rate of this process. We first analyze whether 𝑡𝑦 can be matched
        monomorphic API search and similarity pruning to trans-          with 𝑎𝑟𝑔 by applying one or multiple predefined transformation
        form the generic API dependency graph into a refined generic     rules. If so, we first apply these transformation rules and then
       API dependency graph in this stage.                               perform 𝑚𝑎𝑡𝑐ℎ(𝑎𝑟𝑔, 𝑡𝑦). We list all predefined transformation rules
   (3) API Sequence Generation and fuzz driver synthesis.                in table 1.
       We integrate our approach with RULF, feeding the refined             To check the trait bounds, We implement a trait bounds checker
        monomorphic API dependency graph to generate API se-             in our tool. However, due to the limitation of rustdoc, we can only
        quences and synthesize the fuzz drivers.                         obtain a subset of the trait implementation and part of the associated
   We discuss the details of each step in our implementation in the      item[14] information in traits. As we intend to reach a high generic
rest of the section.                                                     API coverage as much as possible, the trait bounds checker we
arxiv 2023, ,                                                                                                    Yehong Zhang, Jun Wu, and Hui Xu


                Table 1: Predefined transformation rules.                these libraries, the number of APIs ranges from 16 to 1511, and the
                                                                         number of generic APIs ranges from 9 to 448.
           Borrow Rules     Pointer Rules   Wrapper Rules
                                                                         5.1.3 fuzz driver synthesis. We generate all fuzz drivers by our
           T→&T             T→ ∗const T     Result<T ,E> →T              approach. As we mention in section 4.3, all generated fuzz drivers
           T→&mut T         T→ ∗mut T       Option<T> →T                 contain at least one generic API. We build all fuzz drivers with the
                                                                         command cargo afl build.

implement is unsound, meaning that it may produce false positive         5.1.4 Fuzzing Configuration. We determined our fuzzing configu-
results in some cases. However, it can cover more APIs in most           ration by referencing RULF. We fuzz all the selected libraries with
of the cases. The experimental results also demonstrate that the         afl.rs[1], which is a Rust binding for AFL++. We set two environ-
number of generated invalid fuzz drivers is actually quite low in        ment variables, AFL_EXIT_WHEN_DONE=1 and AFL_NO_AFFINITY=1.
real-world libraries.                                                    AFL_EXIT_WHEN_DONE leads to an early termination for the fuzz
                                                                         drivers which cannot discover new finds, while AFL_NO_AFFINITY
4.3      API Sequence Generation                                         enables us to run more fuzzing instances than the actual number
After we transform the generic API dependency graph into a refined       of CPUs. Each fuzz driver is configured with a maximum runtime
monomorphic API dependency graph, we utilize RULF to gener-              of 24 hours.
ate API sequences and synthesize the fuzz drivers. The sequence
generation of RULF ensures that each API will be covered in fuzz         5.2    RQ1: Can our approach generate valid fuzz
drivers at least once, as long as there exist valid API sequences to            drivers to cover generic APIs?
invoke the API. Since our method ensures that all monomorphic            Table 2 shows the main results of our experiments. We answer this
APIs are reachable, each one can be ultimately covered by the API        research question from validity and generic API coverage.
sequences.
   To prevent an excessive number of API sequences, we limit the         5.2.1 Validity of generated fuzz drivers. The results show our tool
number of API sequences to 300. To test generic functions, we            reaches a high rate of validity. We generate 2 to 300 fuzz drivers
impose a constraint that the API sequence must include at least          for each library. The total number of generated fuzz drivers by
one monomorphic API. By removing this constraint, our tool can           our tool is 2566, with 103 invalid fuzz drivers. The ratio of valid
generate API sequences for all possible APIs in the library.             fuzz drivers to invalid fuzz drivers is 0.04. After an analysis of all
                                                                         invalid drivers, we have discovered the main cause of invalidity is
5     EVALUATION                                                         the unsound trait bounds check. As we mention in section 4.2, to
We evaluate our approach with three research questions:                  reach a higher generic API coverage, we implement an unsound
                                                                         trait bounds checker. Thus, a few invalid usages of APIs can pass
    • RQ1: Can our approach generate valid fuzz drivers for generic
                                                                         the trait bounds checker and cause the generation of invalid fuzz
      APIs?
                                                                         drivers. This issue can be fixed by more engineering effort or by
    • RQ2: Does our pruning algorithm improve efficiency?
                                                                         using the official trait bounds checker in the Rust compiler.
    • RQ3: What kinds of bugs our approach can find in the real-
      world libraries?                                                   5.2.2 Coverage of our approach. Table 2 presents the coverage for
                                                                         API and generic API in each library. Our approach can achieve 0.7+
5.1      Experiment Setting                                              API coverage for 14 libraries and 0.6+ generic API coverage for
5.1.1 Platform. We conduct all fuzzing experiments on a server           libraries. However, it does not work well for some libraries, and
machine with 2 Intel Xeon Gold 6242R 3.10GHz 20-core CPUs and            the coverage of our tool varies among different libraries. Across all
256GB memory with the Ubuntu 20.04 operating system.                     libraries, the API coverage spans from 0.01 to 0.96, and the generic
                                                                         API coverage ranges from 0.01 to 0.75. The total API coverage is
5.1.2 Library Selection. We select the target libraries based on         0.66, while the total generic API coverage is 0.27. To understand
three criteria:                                                          the culprits of the low generic API coverage, We study the library
     • The repository must have received at least 100 stars.             with the lowest generic API coverage (axum-core). We have 72
     • The repository should have recent commits within the past         uncovered generic APIs, and we find that 68 of them are caused
        six months.                                                      by using the types or traits of third-party libraries in the generic
     • The repository must contain a minimum of five generic APIs.       API signature in this library. Figure 9 shows an example of this
   We randomly select 29 libraries from crates.io and GitHub, with       situation. The axum-core declares a trait FromRequest with an
10 libraries from the Trophy-case repository. Trophy-case is a repos-    interface from_request. However, the first argument of this inter-
itory that records the bugs found by fuzzing in the libraries. All       face is a third-party type http::Request. Since we lack the API
libraries mentioned in the Trophy-case have records that have            information from http, we can not instantiate a http::Request.
previously been discovered to contain bugs by fuzzing. Fuzzing           As a result, all APIs related to this trait are uncovered. This issue is
repositories from the Trophy-case with our tool can reveal whether       difficult to resolve since we implement our tool based on rustdoc,
our tool can cover APIs that other automated generated fuzz dri-         which is designed for documenting a single library. It takes a lot of
vers or handcraft fuzz drivers do not cover, and identify any bugs       engineering effort to adopt our tool to extract the API information
they contain. All libraries satisfy the criteria claimed above. Within   from third-party libraries. The reason for the rest of the 4 uncovered
Fuzz Driver Synthesis for Rust Generic APIs                                                                                              arxiv 2023, ,


Table 2: Experiment results of 29 libraries. The first 18 are from GitHub, the last 11 are from Trophy-case. "#Mono APIs"
represent the number of monomorphic APIs obtained by reachable monomorphic API search.

                                                     #Generic     API      Generic API    #Mono    #Reserved    Fuzz targets
          Library            Version      #APIs                                                                                Crashes    Bugs
                                                       APIs     Coverage    Coverage       APIs      APIs         (invalid)
        serde_json           1.0.103          586      317        0.49        0.10         110         95         300 (33)       103         0
           base64             0.21.4           40      22         0.60        0.64         16          16          17 (4)         0          0
            uuid              1.4.1           133       9         0.94        0.22          2           2             7           1          0
     form_urlencoded          1.2.0            16       9         0.81        0.67         12          12            10           4          1
           flate2             1.0.28          274      228        0.54        0.50         622        296          147 (3)       66          0
        http-body             0.4.5           156      143        0.17        0.09         404         19           6 (4)         0          0
           subtle             2.5.0           107      19         0.96        0.79         730        110           300          17          0
        prost-type            0.12.1          453      17         0.95        0.12         76           6            23           0          0
        axum-core             0.3.4            95      73         0.01        0.01          3           3           3 (2)         0          0
          monero              0.19.0          469      148        0.66        0.32         104         88           105          554         3
          dlopen              0.1.8            55      48         0.29        0.25         620         12             2           0          0
          lofty-rs            0.17.1          1186     144        0.73        0.15         220         68          27 (2)        30          2
         html2text            0.6.0           145      78         0.72        0.67         162        151          182 (6)      8515         5
             neli             0.7.0           1511     448        0.61        0.04         269         51            10          10          4
          odoh-rs             1.0.2            39      15         0.74        0.80         16          16            21           6          2
        xorfilter-rs          0.5.1            48      35         0.85        0.80         92          56            56          70          3
         genmesh              0.6.0            31      30         0.13        0.13         304          9             6           0          0
            term              0.7.0            42      19         0.26        0.11          2           2             4           0          0
         chrono               0.4.31          639      202        0.88        0.73          500       433          300           347         0
          cookie              0.18.0          116      34         0.78        0.44          605        21         22 (13)         0          0
        cssparser             0.33.0          148      49         0.72        0.41          56         40         201 (2)         0          0
           regex              1.8.3           207      16         0.93        0.69          109        59           57           258         2
             tui              0.19.0          366      71         0.82        0.42         1034        44         45 (22)        47          1
             url              2.4.1           113      12         0.90        0.75          12         11         67 (2)          0          0
            toml              0.8.2           239      161        0.38        0.14          32         32         300 (8)        22          0
           prost              0.12.1          282      183        0.37        0.13          40         40          127            0          0
            num               0.4.1            56      56         0.36        0.36          204       204          204           265         1
         fontdue              0.8.0            54      12         0.39        0.17          10         10         12 (2)          0          0
      cpp_demangle            0.4.3           104      11         0.17        0.27           5          5            5            0          0
           Total               N/A            7710    2609        0.66        0.27         6371      1911        2566 (103)     10319       23


APIs is that there are no types that implement the trait required by            5.3      RQ2: Does our pruning algorithm improve
the trait bounds of the generic API. Since we generate monomor-                          efficiency?
phic API from all existing types in the library, our approach can
                                                                                We report the number of monomorphic APIs and reserved APIs for
not cover this situation.
                                                                                each library in table 2. The total number of monomorphic APIs is
   Note that our approach is bound to outperform RULF, as our
                                                                                6371, while the total number of reserved APIs is 1911. As a conclu-
method essentially extends the API dependency graph utilized by
                                                                                sion, the number of monomorphic APIs is reduced to 30% of their
RULF. Consequently, the covered APIs by our tool is a superset of
                                                                                original count after similarity pruning. In the best situation, the
RULF’s.
                                                                                number of reserved APIs is only 2% of the number of monomorphic
 1   use crate::body::Body;                                                     APIs (in dlopen library). We also observe that our pruning algo-
 2   pub type Request<T = Body> = http::Request<T>;                             rithm is generally more effective in cases with a larger number of
 3   pub trait FromRequest<S, M = private::ViaRequest>: Sized {                 monomorphic APIs. Figure 10 shows the comparison between the
 4       type Rejection: IntoResponse;
                                                                                number of monomorphic APIs and the number of reserved APIs
 5       async fn from_request(req: Request, state: &S)
 6       -> Result<Self, Self::Rejection>;                                      in libraries, ordered by the number of monomorphic APIs in the
 7   }                                                                          library. As the number of monomorphic APIs increased, the pro-
                                                                                portion of monomorphic APIs reduced by the pruning algorithm
Figure 9: The generic API in axum-core use a third-party type                   also gradually increased. This is understandable, as a higher count
from http.                                                                      of monomorphic APIs is often a result of similar behaviors.
arxiv 2023, ,                                                                                                      Yehong Zhang, Jun Wu, and Hui Xu


                                                                        9-10) is an arithmetic overflow bug and can be triggered when
                                                                        render receives a RenderTree parsed from certain data and an
                                                                        instance of type RichDecorator. The second bug (line 11-12) is
                                                                        an infinite loop bug and can be triggered when render receives
                                                                        a RenderTree parsed from certain data and an instance of type
                                                                        TrivialDecorator. Any other type implemented TextDecorator
                                                                        cannot trigger this bug. Since RichDecorator and TextDecorator
                                                                        implement trait TextDecorator independently, our approach gen-
                                                                        erates and reserves these two monomorphic APIs for API render,
                                                                        has the capability to detect both bugs. However, other previous work
                                                                        can only detect one of these bugs since they neglect the generic
                                                                        API or simply consider the generic API as a non-generic API. This
                                                                        case study shows the fuzz drivers generated by RULF are diverse
                                                                        and can detect various bugs hidden in different monomorphic APIs.

                                                                            1   /* API Signatures:
                                                                            2   fn parse(mut input: impl io::Read) -> RenderTree
                                                                            3   fn render<D: TextDecorator>(self: RenderTree, width: usize,
Figure 10: Comparison between # of monomorphic APIs and
                                                                            4   decorator: D) -> RenderedText<D> */
# of reserved APIs. The libraries are ordered by # of monomor-              5   use html2text::render::text_renderer::RichDecorator;
phic APIs.                                                                  6   use html2text::render::text_renderer::TrivialDecorator;
                                                                            7   let data: &[u8] = get_data();
                                                                            8   let render_tree = html2text::parse(&data);
5.4      RQ3: What kinds of bugs our approach can                           9   // RichDecorator triggers an overflow bug
                                                                                let _ = render_tree.render( 1, RichDecorator{});
         find in the real-world libraries?                               10
                                                                         11     // TrivialDecorator triggers an infinite loop bug
5.4.1 Overview. We distinguish bugs by the crash message and             12     let _ = render_tree.render( 1, TrivialDecorator::new());
stack trace. If two crashes have the same crash message, and the
stack trace implies the crash happened in the same API, we regard               Figure 11: Example of diverse bugs in a generic API.
them as the same bugs. We manually review all crash reports and
filter out duplicate bugs. All bugs we found are submitted to the
GitHub issue of the library. Table 2 shows the bugs we found in
                                                                        6       RELATED WORK
the libraries. Experimental results indicate that our approach can
identify bugs within generic APIs. After fuzzing 29 libraries, we       Fuzz driver synthesis can roughly be divided into two categories
found 23 bugs, with 10 bugs confirmed by the library maintainer         based on their strategies. The first kind of approach leverages the
before we submitted the paper. We manually investigate the culprit      consumer code for libraries and synthesizes fuzz drivers with the
of all bugs, and present a taxonomy as follows.                         call graph. The representative work includes Fudge[3], FuzzGen[9]
                                                                        and RUBICK[23]. Another kind of approach leverages the API spec-
     • Utf-8 encoding. 2 bugs are caused by this reason.
                                                                        ification from the source code and synthesizes fuzz drivers. The
     • Arithmetic overflow. 9 bugs are caused by this reason.
                                                                        representative work includes RULF[10], GraphFuzz[8]. Some works,
     • Out of memory. 6 bugs are caused by this reason.
                                                                        such as APICraft[24], Hopper[5] explore the hybrid approach to
     • Index out of bounds. 2 bugs are caused by this reason.
                                                                        leverage both API specification and consumer code. There are also
     • Other. The program crashed for miscellaneous reasons, in-
                                                                        other tools to test library API. Rudra[4] is a static analyzer that
        cluding unreachable code, option unwrap, infinite loop, and
                                                                        analyzes Rust code and detects three types of bugs. SyRust[21]
        unexpected panic. 4 bugs are caused by this reason.
                                                                        synthesizes the Rust program by modeling the Rust type system.
    We also examine all bugs to ascertain how many bugs are related     However, the program synthesized by SyRust cannot serve as a
to the generic API. A bug is considered generic API-related if it is    fuzz driver since it cannot receive the input.
either caused by a generic API or requires the invocation of at least
one generic API. Out of 23 bugs, we found 18 bugs are related to        7       CONCLUSION
generic APIs.
                                                                        In this paper, we propose a novel fuzz driver synthesis approach for
5.4.2 Case Study. We do a further case study to understand how          libraries with generic APIs. We analyze the challenges and propose
bugs in generic API are triggered. The figure 11 shows an example       a two-stage approach to generate valid fuzz drivers with generic
derived from our experiment, where we merge and reformat two            APIs. We implement a prototype of our approach called RULF+ and
fuzz drivers to make it more readable. These two fuzz drivers find      evaluate our approach on 29 real-world open-source Rust libraries.
different bugs on the same API. parse and render are both generic       Experimental results and case studies support that RULF+ can reach
APIs. parse requires a type implemented io::Read trait and re-          a high rate of valid cases and promising generic API coverage. Our
turn a RenderTree instance. render requires a type implemented          pruning approach can improve the efficiency of fuzzing while still
TextDecorator trait, and receive RenderTree instance from parse.        keeping the capability of finding elusive and diverse bugs in generic
render is a buggy API and contains two bugs. The first bug (line        APIs.
Fuzz Driver Synthesis for Rust Generic APIs                                                                                                                        arxiv 2023, ,


REFERENCES                                                                               [12] Björn Mathis, Rahul Gopinath, and Andreas Zeller. 2020. Learning input tokens
 [1] Rust Fuzzing Authority. 2023. afl.rs. Retrieved Dec 16, 2023 from https://github.        for effective fuzzing. In ISSTA ’20: 29th ACM SIGSOFT International Symposium on
     com/rust-fuzz/afl.rs                                                                     Software Testing and Analysis, Virtual Event, USA, July 18-22, 2020. ACM, 27–37.
 [2] Rust Fuzzing Authority. 2023. Trophy Case. Retrieved Dec 16, 2023 from              [13] Zalewski Michal. 2015. American Fuzzy Lop. Retrieved Dec 22, 2020 from
     https://github.com/rust-fuzz/trophy-case                                                 https://lcamtuf.coredump.cx/afl/
 [3] Domagoj Babic, Stefan Bucur, Yaohui Chen, Franjo Ivancic, Tim King, Markus          [14] Rust official team. 2023. Associated Items. Retrieved Dec 16, 2023 from https:
     Kusano, Caroline Lemieux, László Szekeres, and Wei Wang. 2019. FUDGE: fuzz               //doc.rust-lang.org/reference/items/associated-items.html
     driver generation at scale. In Proceedings of the ACM Joint Meeting on European     [15] Rust official team. 2023. Generic parameters. Retrieved Dec 16, 2023 from
     Software Engineering Conference and Symposium on the Foundations of Software             https://doc.rust-lang.org/reference/items/generics.html
     Engineering, ESEC/SIGSOFT FSE 2019, Tallinn, Estonia, August 26-30, 2019. ACM,      [16] Rust official team. 2023. Re-exports. Retrieved Dec 16, 2023 from https://doc.rust-
     975–985.                                                                                 lang.org/nightly/rustdoc/write-documentation/re-exports.html
 [4] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021.           [17] Rust official team. 2023. Trait and lifetime bounds. Retrieved Dec 16, 2023 from
     RUDRA: finding memory safety bugs in Rust at the ecosystem scale. In Proceedings         https://doc.rust-lang.org/reference/trait-bounds.html
     of the ACM SIGOPS 28th Symposium on Operating Systems Principles. 84–99.            [18] Rust official team. 2023. Traits. Retrieved Dec 16, 2023 from https://doc.rust-
 [5] Peng Chen, Yuxuan Xie, Yunlong Lyu, Yuxiao Wang, and Hao Chen. 2023. Hopper:             lang.org/reference/items/traits.html
     Interpretative Fuzzing for Libraries. In Proceedings of the 2023 ACM SIGSAC         [19] Rust official team. 2023. What is rustdoc? Retrieved Dec 16, 2023 from https:
     Conference on Computer and Communications Security. 1600–1614.                           //doc.rust-lang.org/rustdoc/what-is-rustdoc.html
 [6] M. R. Garey and David S. Johnson. 1979. Computers and Intractability: A Guide to    [20] Kostya Serebryany. 2017. OSS-Fuzz - Google’s continuous fuzzing service for
     the Theory of NP-Completeness. W. H. Freeman.                                            open source software. https://www.usenix.org/conference/usenixsecurity17/
 [7] Google. 2020. Honggfuzz. Retrieved Dec 22, 2020 from https://github.com/                 technical-sessions/presentation/serebryany
     google/honggfuzz                                                                    [21] Yoshiki Takashima, Ruben Martins, Limin Jia, and Corina S. Pasareanu. 2021.
 [8] Harrison Green and Thanassis Avgerinos. 2022. GraphFuzz: library API fuzzing             SyRust: automatic testing of Rust libraries with semantic-aware program synthe-
     with lifetime-aware dataflow graphs. In Proceedings of the 44th International            sis. In PLDI ’21: 42nd ACM SIGPLAN International Conference on Programming
     Conference on Software Engineering. 1070–1081.                                           Language Design and Implementation, Virtual Event, Canada, June 20-25, 2021.
 [9] Kyriakos K. Ispoglou, Daniel Austin, Vishwath Mohan, and Mathias Payer. 2020.            ACM, 899–913.
     FuzzGen: Automatic Fuzzer Generation. In 29th USENIX Security Symposium,            [22] LLVM team. 2020. libFuzzer – a library for coverage-guided fuzz testing. Re-
     USENIX Security 2020, August 12-14, 2020. USENIX Association, 2271–2287.                 trieved Dec 22, 2020 from https://llvm.org/docs/LibFuzzer.html
[10] Jianfeng Jiang, Hui Xu, and Yangfan Zhou. 2021. RULF: Rust library fuzzing via      [23] Cen Zhang, Yuekang Li, Hao Zhou, Xiaohan Zhang, Yaowen Zheng, Xian Zhan,
     API dependency graph traversal. In 2021 36th IEEE/ACM International Conference           Xiaofei Xie, Xiapu Luo, Xinghua Li, Yang Liu, et al. [n. d.]. Automata-Guided
     on Automated Software Engineering (ASE). IEEE, 581–592.                                  Control-Flow-Sensitive Fuzz Driver Generation. ([n. d.]).
[11] Shea Leffler. 2017. Rust’s Type System is Turing-Complete. Retrieved Dec 12,        [24] Cen Zhang, Xingwei Lin, Yuekang Li, Yinxing Xue, Jundong Xie, Hongxu Chen,
     2023 from https://sdleffler.github.io/RustTypeSystemTuringComplete/                      Xinlei Ying, Jiashui Wang, and Yang Liu. 2021. { APICraft } : Fuzz Driver Gener-
                                                                                              ation for Closed-source { SDK } Libraries. In 30th USENIX Security Symposium
                                                                                              (USENIX Security 21). 2811–2828.
