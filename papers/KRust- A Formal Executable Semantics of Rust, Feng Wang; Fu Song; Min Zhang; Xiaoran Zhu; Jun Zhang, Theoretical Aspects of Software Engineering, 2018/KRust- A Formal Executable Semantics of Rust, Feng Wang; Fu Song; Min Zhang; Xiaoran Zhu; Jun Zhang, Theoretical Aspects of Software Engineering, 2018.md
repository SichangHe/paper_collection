                                              KRust: A Formal Executable Semantics of Rust
                                                                        Feng Wang∗, Fu Song∗, Min Zhang† , Xiaoran Zhu† and Jun Zhang∗
                                                             ∗ School of Information Science and Technology, ShanghaiTech University, Shanghai, China
                                                      † Shanghai Key Laboratory of Trustworthy Computing, East China Normal University, Shanghai, China




                                            Abstract—Rust is a new and promising high-level system            object is a variable binding. When a variable goes out of its
                                         programming language. It provides both memory safety and             scope, Rust will free the bound resources. The ownership of
                                         thread safety through its novel mechanisms such as ownership,        an object can be transferred, after which the object cannot
                                         moves and borrows. Ownership system ensures that at any point
arXiv:1804.10806v1 [cs.PL] 28 Apr 2018




                                         there is only one owner of any given resource. The ownership of      be accessed via the outdated owner. This ensures that there
                                         a resource can be moved or borrowed according to the lifetimes.      is exactly one binding to any object. Instead of transferring
                                         The ownership system establishes a clear lifetime for each value     ownership, Rust provides borrows which allows an object to
                                         and hence does not necessarily need garbage collection. These        be shared by multiple references. There are two kinds of
                                         novel features bring Rust high performance, fine low-level control   borrows in Rust: mutable references and immutable references.
                                         of C and C++, and unnecessity in garbage collection, which
                                         differ Rust from other existing prevalent languages. For formal      A mutable reference can mutate the borrowed object if the
                                         analysis of Rust programs and helping programmers learn its          object is mutable, while an immutable reference cannot mutate
                                         new mechanisms and features, a formal semantics of Rust is           the borrowed object even the object itself is mutable. The basic
                                         desired and useful as a fundament for developing related tools. In   ownership discipline enforced by Rust is that an object shared
                                         this paper, we present a formal executable operational semantics     by multiple references is immutable. This property eliminates
                                         of a realistic subset of Rust, called KRust. The semantics is
                                         defined in K, a rewriting-based executable semantic framework        a wide range of common low-level programming errors, such
                                         for programming languages. The executable semantics yields           as use-after-free, data races, and iterator invalidation. These
                                         automatically a formal interpreter and verification tools for Rust   specific semantic rules are unusual, and hence the semantics
                                         programs. KRust has been thoroughly validated by testing with        of other modern programming languages such as C/C++, Java
                                         hundreds of tests, including the official Rust test suite.           and Javascript cannot be directly adapted to Rust.
                                            Index Terms—Formal operational semantics, Rust program-
                                         ming language, K framework                                              To remedy this situation, a formal semantics of Rust is de-
                                                                                                              sired and useful as a fundament for reasoning about Rust pro-
                                                                     I. Introduction                          grams in a formal way and developing related computer-aided
                                            Recently, a new system programming language Rust was              tools. To our knowledge, the formal semantics of Rust has not
                                         designed and implemented by Mozilla [1], aiming at achieving         yet been well studied, which impedes further developments of
                                         both high-level safety and low-level control in developing           formal analysis and verification tools for Rust programs. In this
                                         system software, such as operating systems, device drivers,          paper, we make a major step toward rectifying this situation
                                         game engines and web browsers. Like most modern high-                by giving the first formal operational semantics of a realistic
                                         level languages, Rust guarantees memory safety and thread            subset of Rust. We design a formal operational semantics of
                                         safety, and meanwhile it supports zero-cost abstractions for         Rust capturing ownership, ownership moves and borrows. To
                                         many common system programming idioms and provides fine              avoid our semantics to be just “paper work”, we formalize
                                         low-level control over the use of memory, without needing a          the semantics in K framework [6] (http://kframework.org),
                                         garbage collector. One key to meeting all these promises is          a scalable semantic framework for programming languages
                                         Rust’s novel system of ownership, moves and borrows. The             which has been successfully applied to C [7] and Java [8].
                                         ownership system establishes a clear lifetime for each value,        We call the K definition of the semantics KRust. 2 To the
                                         making garbage collection unnecessary in the core language.          best of our knowledge, it is the first formal executable
                                         Moreover, it also prevents data-races at compile-time. The           semantics for Rust.
                                         three mechanisms are checked at compile time and carefully              There are several benefits from the formal semantics defined
                                         designed to complement its static linear type system. Rust has       in K framework. Firstly, the semantics defined in K is both
                                         been used to implement operating system [2], parallel browser        machine readable and executable, from which an interpreter
                                         engine [3], Intel SGX Enclave [4], etc. (organizations running       of Rust is generated automatically. Being executable, the
                                         Rust in production refers to 1 )                                     semantics has been thoroughly tested with hundreds of tests,
                                            The new features make the semantics of Rust different from        including the official Rust test suite. Secondly, K provides a
                                         other common languages, which brings new difficulties in             simple notation for modular semantics of languages, making
                                         reasoning about Rust programs. The difficulty constantly baf-        the semantics easy to define and extensible. The semantics
                                         fles developers and has become a common topic of question-           offers a formal reference and a correctness definition for
                                         and-answer websites (for instance, [5]). The ownership of an
                                                                                                                 2 KRust and all the related sample examples are available for downloading
                                           1 https://www.rust-lang.org/en-US/friends.html.                    from: http://sist.shanghaitech.edu.cn/faculty/songfu/Projects/KRust.
implementers of tools such as parsers, compilers, interpreters        function definition with return type (). Furthermore, Rust has
and debuggers, which would greatly facilitate developers’             no restriction on the order of function definitions, namely that
understanding, freeing them from lengthy, ambiguous, elusive          Rust programs can invoke functions which are defined later.
Rust documentations. Moreover, the semantics could automat-           These features are unusual and introduce tricky corner cases.
ically yield formal analysis tools such as state-space explorer   1     f n f o o ( x : i3 2 , y : i 3 2 ) −> i 3 2 {
for reachability, model-checker, symbolic execution engine,       2        x+y / / r e t u r n x+y ;
deductive program verifier by the language-independent tools      3     }
provided in K [9].                                                       The above program defines a function foo which takes two
Organization. Section II gives a brief overview of Rust. In           32-bit integers x and y as arguments and returns x+y. This
Section III, after introducing the basic notations of K, we           function behaves the same as the function which replaces the
present the formal semantics KRust of Rust in K. Confor-              last expression x+y in foo with the return statement return
mance testing and applications of KRust are described in              x+y;.
Section IV. Section V discusses related work. Finally, we
conclude the work with a discussion in Section VI.                    C. Ownership
                                                                         Ownership is the key feature of Rust, which guarantees
                           II. A Tour of Rust
                                                                      memory safety and thread safety without garbage collection.
   In this section, we give a brief overview of Rust. Rust is         The basic form of ownership is exclusive ownership, namely
a C-like programming language which contains common con-              that each object has a unique owner at any time. This ensures
structs from modern programming languages such as if/else             that at most one reference is allowed to mutate a given
branches, while/for loops, functions, compound data                   location. When an object is created and assigned to a variable
structures, etc. We will mainly point out distinct features of        x, the variable x becomes the owner of the object. If the object
Rust, compared with other well-known modern programming               is reassigned (as well as parameter passing, etc.) to another
languages such as C/C++ and Java.                                     variable y, the ownership of the object is transferred from the
A. Mutability                                                         variable x to the variable y, namely that y becomes the owner
                                                                      of the object and x is not the owner of the object. This is
  Variables are declared using let statements. In default,
                                                                      so-called move semantics in Rust. This ownership discipline
variable is immutable, which means that its value cannot be
                                                                      rules out aliasing entirely, and thus prevents from data race.
mutated. To declare a mutable variable, mut is required in the
                                                                      Moveover, if the owner of the object goes out of scope, the
declaration statement.
                                                                      object is destroyed automatically without garbage collection.
1   f n main ( ) {                                                    This is implemented by the Rust compiler which inserts a
2      l e t x =9;
3      x =10; / / E r r o r !                                         call to a destructor at the end of the owner’s scope, called
4      l e t mut y = 0 ;                                              drop in Rust. This ownership discipline enforces automatic
5      l e t mut z : b o o l ;                                        memory management and prevents other errors commonplace
6   }
                                                                      in low-level pointer-manipulating programs, like use-after-free
   For instance, the above code declares an immutable variable        or double-free. To see this principle in practice, consider the
x at Line 2 and a mutable variable y at Line 4 whose types            following sample program.
are inferred at compile-time. The type can also be explicitly
                                                          1             struct Point {
specified in the program like the mutable variable z at Line
                                                          2                  x : i3 2 ,
5. The Rust compiler will issue an error at Line 3, as the3                  y : i3 2 ,
                                                          4             }
immutable variable x is reassigned. This is different from5             f n main ( ) {
other modern programming languages like C/C++ and Java.   6                l e t p = Point { x :1 , y : 2 } ;
                                                          7
The semantic rules of Rust should take into the mutability of              {
                                                          8                    l e t mut q = p ; / / q becomes t h e owner
variables into account.                                   9                    q . x = 2;
                                                         10                    println !( ” {} ” ,p . x) ;     / / Error !
B. Functions                                             11                }
  Functions are declared with the keyword fn and each of 12                println !( ” {} ” ,q.x) ;       / / Error !
                                                         13             }
them should return exactly one value. There are two ways
to return a value if the function definition declares a return        Point is a compound data structure consisting of two 32-bit
type. The first one returns a value in the body of the function       integer fields x and y. At Line 6, a Point object is created
explicitly using the return statement, which is similar to            and assigned to the mutable variable p. The Rust compiler
existing prevalent languages. The another one returns the             will issue an error at Line 10 which accesses the x field of
value of the last expression in the body of the function, if          the Point object via the reference p, as the ownership of the
there is no explicit return statement. However, if the function       Point object was already transferred from p to q at Line 8.
definition does not declare a return type, Rust will implicitly       Moreover, the Rust compiler will also issue another error at
returns the unit type (). Indeed, a function definition without       Line 12 which accesses the x field of the Point object via the
declaring a return type is just syntactic sugar for the same          reference q, as the owner q went out of its scope and the Point



                                                                  2
 object was already destroyed. These scenarios rarely happen                      lifetimes can be elided in general, which is why they did not
 in existing prevalent programming languages, thus makes the                      show up in the above examples. Rust also supports named
 Rust semantics unusual.                                                          lifetimes which helps the Rust compiler to aggressively infer
                                                                                  lifetimes and makes sure all borrows are valid.
 D. Borrowing
                                                                              1      f n main ( ) {
    The ownership discipline is a fairly straightforward mecha-               2          l e t mut x ;
 nism for guaranteeing memory safety and thread safety. How-                  3          {
 ever, it is also too restrictive to develop industry programs. To            4              l e t y = 1;
                                                                              5              x = &y ;     / / Error !
 address this issue, Rust provides a mechanism used to handle                 6          }
 references, called borrowing. There are two different borrow-                7          l e t z = 1;
 ing (i.e., reference types) in Rust: mutable references and                  8          l e t p = &z ; / / OK!
                                                                              9      }
 immutable references. A mutable reference grants temporary
 exclusive read and write access to the object, i.e., each object                    The above example illustrates intuition behind lifetime.
 has at most one mutable reference (without any immutable                         There is an error at Line 5 as the lifetime of x is not included
 references). This ensures that mutable references are always                     in the lifetime of y. Instead, it is fine to borrow z at Line 8,
 unique pointers. A mutable reference can be reborrowed to                        as the lifetime of p is included in the lifetime of z. Therefore,
 someone else. Contrary to mutable references, an immutable                       Rust’s variable context is substructural.
 reference grants temporary read-only access to the object and
                                                                                          III. KRust: The Formal Semantics of Rust in K
 it is allowed that multiple immutable references refer to the
 same object. The design of borrowing in Rust also guarantees                       In this section, we first introduce the basic notations of K,
 memory safety and thread safety.                                                 and then define the addressed formal syntax of Rust. Finally,
                                                                                  we define the configurations and formal semantics KRust of
 1   f n main ( ) {
 2       l e t x1 = 1 ;                                                           Rust in K.
 3       l e t p1 = &x1 ; / / x1 i s b o r r o w ed i m m u t a b l y
 4       l e t q1 = &x1 ; / / x1 i s b o r r o w ed i m m u t a b l y             A. K Framework
 5       ∗ p1 = 2 ; / / E r r o r !
 6       l e t y = &mut x1 ; / / E r r o r !
                                                                                     K Framwork is a rewrite-based executable semantic frame-
 7                                                                                work. Operational semantics of a programming language can
 8       l e t mut x2 = 1 ;                                                       be formally defined with the state of an executing program
 9       l e t p2 = &x2 ; / / x2 i s b o r r o w ed i m m u t a b l y
10       l e t q2 = &x2 ; / / x2 i s b o r r o w ed i m m u t a b l y
                                                                                  being represented as a configuration and the semantics of each
11       ∗ p2 = 2 ; / / E r r o r !                                               program statement being defined as K rules. With the defined
12                                                                                operational semantics, K automatically generates an interpreter
13       l e t mut x3 = 1 ;
14       l e t p3 = &mut x3 ;       / / x3 i s b o r r o w ed m u t a b l y
                                                                                  which can execute programs of the language. Besides, K
15       x3 = 2 ; / / E r r o r !                                                 also provides formal analysis functionalities such as model
16       ∗ p3 = 2 ; / / OK!                                                       checking, symbolic execution, and theorem proving [6]. A
17       l e t p4 = &mut x3 ;        / / Error !
18   }
                                                                                  number of programming languages have been formalized using
                                                                                  K, such as C [7], Python [10], PHP [11] and Java [8].
    We can see borrowing in action in the above example. In                          In this section, we briefly introduce the mechanism of
 this example, the variable x1 is immutable which is immutably                    how to define operational semantics in K with an example.
 borrowed twice at Lines 3 and 4. The compiler will issue an                      Basically, the syntax of a language is defined using BNF with
 error at Line 5 which tries to mutate the value of x1. It also                   semantic attributes, and the operational semantics is defined
 issues another error at Line 6, as immutable variable x1 cannot                  by a set of K rules which describe the effect of atomic
 be mutably borrowed. The code at Lines 8-11 shows that the                       program statements over K configurations. A K configuration
 mutable variable x2 can also be immutably borrowed multiple                      is essentially a nested cell defined in XML style, which
 times, but cannot be mutated by an immutable reference.                          specifies a state of an executing program.
 Line 15 demonstrates that the mutable variable x3 cannot be                         For better understanding K, let us consider the following
 mutated via x3 once it is borrowed. Instead, it can be mutated                   semantic rule for lookup function in Rust, which is used to
 via the mutable reference p3 at Line 16. Line 17 shows that                      lookup the value of a name (e.g., variable) when a statement
 the mutable variable x3 cannot be mutably borrowed more                          which contains that name is being executed.
 than once.                                                                                 X       
                                                                                                · · · h· · · X 7→ L · · · ienv h· · · L 7→ V · · · istore
 E. Lifetime                                                                                 V         k

    Borrowing grants temporary access to the object. Rust                            There are three cells related to the lookup function. The cell
 associates to each reference with a lifetime to specify how long                 k (i.e., the cell labeled with k) is used to store the computations
 is temporary. Intuitively, lifetimes are effectively just names                  of a program to be executed. In this example, X is the next
 for scopes somewhere in the program, but they are not same.                      expression/statement to evaluate/execute, where X is a K label
 The lifetime of a reference should be included in the lifetime                   representing a program name. Both env and store cells are
 of the borrowed variable. Rust provides a convention so that                     Map type to store key-value pairs, where env is used to store



                                                                              3
                                                                        TABLE I
                                                                   The syntax of KRust

     Syntax                                                                                                               Description
     Id ::= [a-zA-Z ][a-zA-Z0-9 ]*                                                                                        Identifier
     Type ::= i8 | u8 | i16 | u16 | i32 | u32 | i64 | u64 | f32 | f64 | isize | usize | char
             | &str | bool | Id | () | [Type;Exp] | fn (Types) -> Type
     Types ::= Type*                                                                                                      Variable Types
     TypedId ::= Id : Type
     TypedIds ::= TypedId*                                                                                                Auxiliary types
     ConstAndStatic ::= const Id : Type = Exp ; | static mut ? Id : Type = Exp ;
     DeclExp ::= let mut ? Id [: Type] ? [= Exp] ? | ConstAndStatic;                                                      Variable declaration
     Op ::= “+” | “-” | “*” | “/” | “%” | “|” | “&” | “>>” | “<<” | “<” | “<=” | “>” | “>=” | “==” | “!=” | “||” | “&&”
     Exp ::= Int | Bool | Float | String | Char | Id | *Id | [Exps] | [Exp;Exp] | vec![Exps] | (Exp) | Exp[Exp]
             | {Exp} | Ref Exp | Id { StructValues } | Exp(Exp) | -Exp | ! Exp | Exp Op Exp
     Exps ::= Exp*                                                                                                        Expressions
     AssignOp ::= “=” | “+=” | “-=” | “*=” | “/=”
     AssignmentStmt ::= Id AssignOp Exp ; | Id[Exp] AssignOp Exp ; | *Id AssignOp Exp; | Id . Id AssignOp Exp ;           Assignment statement
     If ::= if Exp else ? Block
     While ::= while Exp Block
     Loop ::= loop Block | If | While                                                                                     If, while and loop statement
     Block ::= { } | { Stmts } | { Stmts Exp }                                                                            Block
     Ref ::= & | &mut                                                                                                     Two types of references
     Struct ::= struct Id { TypedIds }
     StructValue ::= Id : Exp
     StructValues ::= StructValue*
     StructInstance ::= Id { StructValues }                                                                               Struct
     For ::= for Id in Int..Int Block                                                                                     For statement
     Function ::= fn Id (TypedIds) [-> Type] ? Block                                                                      Function
     Stmts ::= DeclExp | AssignStmt | Block | Exp ; | return ; | return Exp ; | Loop ; | Loop | Function | Struct | For   Statements



the mapping from program names to locations in the form of
                                                                                      *    hKik hMapienv hhListifstack icontrol hMapigenv +
X 7→ L, and store is used to store the mapping from locations
to values in the form of L 7→ V. The dots “· · · ” in the cells are                       hMapitypeEnv hMapistore hMapimutType h0inextLoc
structural frames, denoting irrelevant pairs or computations.                             hMapiborrow hMapiref hMapirefType hMapimoved T
   For instance, given the following two statements:
                                                                                       Fig. 1. The K configuration for the states of KRust programs
1   l e t a = 1;
2   let b = a; / / b = 1

   Variable a should be first evaluated to 1 using the lookup
rule when the second statement is being executed.                                   The cell T is the top one in K which contains all the cells.
B. Syntax                                                                        As aforementioned, the k cell contains the computations of
                                                                                 a program. The env cell is the local environment, recording
   Table I presents the syntax of a realistic subset of Rust                     the map from variables to their locations. Inside control cell,
defined in KRust. The syntax is described by a dialect of Ex-
                                                                                 there is a fstack cell which encodes the stack frame. The
tended Backus-Naur Form (EBNF) according to the grammar                          fstack cell is a list, in which each element contains an env
of Rust [12]. We use two repetition forms in the definition of                   cell, some computations and a return type. The genv cell
the syntax, where “?” means zero or one repetition. “*” means
                                                                                 represents global environment. The typeEnv cell records the
zero or more repetitions. The option is represented through                      type of a given variable’s location. The values of all the defined
squared brackets [ ... ] followed with “?”. For instance, in                     variables are stored in the store cell.
syntax for function declaration, “[-> Type] ?” means that “-
> Type” maybe present just once, or not at all. Since Rust                          Since a variable is either mutable or immutable in Rust, we
shares many common conventions with prevalent functional                         add mutType cell to record whether the variable is mutable
and imperative programming languages, most of its syntax                         or immutable. When a new variable is declared, a new loca-
are easy to understand and hence we omit corresponding                           tion that is an integer value is allocated from nextLoc cell.
explanations. We remark that Table I is not a full syntax                        After that, integer value in nextLoc is increased by one. The
of Rust, e.g., traits and pattern matching are excluded (c.f.                    borrow cell keeps the record whether a variable is mutably
Section VI).                                                                     or immutably borrowed if there exists an alive reference to
                                                                                 it. The ref cell records reference relations. The refType cell
C. Configuration                                                                 contains the types of references, including immutable and
  A K configuration is represented by nested multisets of la-                    mutable references. The moved cell is a map from locations
beled cells. Figure 1 shows the 13 main cells in a configuration                 of variables to {0, 1}, where 1 denotes that the variable has
for the representation of the state of KRust programs.                           been moved, otherwise not.



                                                                             4
                                                                              TABLE II
                                                                 The partial semantic rules of KRust


 Variable declaration     and assignment                                                                                                                                    
  D let X : T ; E  hX ⇒ Lienv           hL ⇒ ⊥istore       hL ⇒ T itypeEnv  
                                                                                          D let mut X : T ; E  hX ⇒ Lienv             hL ⇒ ⊥istore       hL ⇒ T itypeEnv 
                                                                                                                                                                               
                        hL ⇒ 0imutType hL ⇒ ⊥iborrow hL ⇒ ⊥iref                                                     hL ⇒ 1imutType hL ⇒ ⊥iborrow hL ⇒ ⊥iref
                                                                                                                                                                              
         .       k
                                                                                
                                                                                                    .        k 
                                                                                                                                                                              
                                                                                                                                                                               
                      hL ⇒ ⊥i              hL ⇒ 0imoved hL + 1inextLoc                                             hL ⇒ ⊥irefType hL ⇒ 0imoved hL + 1inextLoc 
                                                                                
                                                                                                                 
                                                                                                                                                                              
                                 refType
                                           [Declaration-of-Immutable-Variable]                                                             [Declaration-of-Mutable-Variable
                                                                                                                                                                              ]
  D E ( hX 7→ Li             )     D X=V; E ( hX 7→ Li                                   )        D let mut X: [T ;N]; E  hX ⇒ Lienv            hL ⇒ [T ; N]itypeEnv 
    X                  env                                 env       hL →
                                                                        7  T itypeEnv
                                                                                                                                                                           
                                                                                                                                                                           
                                                                                                                                hL ⇒ 1imutType hL + NinextLoc
                                                                                                                                                                           
    V k    hL 7→ Vistore                .    k   hL 7→ 1imutType hL 7→ ( ⇒ V)istore                         .           k
                                                                                                                            
                                                                                                                             hL . . . L + N − 1 ⇒⊥i
                                                                                                                                                                          
                                                                                                                                                                           
                                                                                                                                                                           
                                                                                                                                                                           
                                                                                                                                                       store
      [Lookup-of-Variable]                      when T = getT ype(V)           [Assignment]                                               [Declaration-of-Mutable-Array]
        D X[I] = V; E ( hX 7→ Li                 hL 7→ [T ; N]itypeEnv
                                                                            )                                       D X[I] E ( hX 7→ Li                  hL 7→ [T ; N]itypeEnv
                                                                                                                                                                               )
                                       env                                                                                                    env
               .        k    hL 7→ 1imutType hL + I 7→ ( ⇒ V)istore                                                    V      k    hL + I 7→ Vistore
  when 0 ≤ I < N and T = getT ype(V) [Updating-of-Array-Element]                                                    when 0 ≤ I < N               [Evaluation-of-Array-Element]
 Borrow, reference, lifetime and dereference                                                                                                                         
                                                                                             D X = &Y; E  hX 7→ L1 , Y 7→ L2 ienv   hL1 7→ 1, L2 7→ 1imutType 
                                                                             
  D X = &mut Y; E  hX 7→ L1 , Y 7→ L2 ienv     hL1 7→ 1, L2 7→ 1imutType                                                                                        
                                                                                                                                                                      
                                                                                                              hL1 7→ 0, L2 7→ 0imoved hL1 7→ ( ⇒ L2 )iref
                                                                                                                                                                     
                        hL1 7→ 0, L2 7→ 0imoved hL1 7→ ( ⇒ L2 )iref
                                                                              
          .       k
                                                                                                .     k
                                                                                                            
                                                                                                                                                                     
                                                                                                                                                                      
                                                                                                              hL1 7→ 0irefType          hL2 7→ 0iborrow
                      hL1 7→ ( ⇒ 1)irefType                                                                                                                        
                                                   hL2 7→ (⊥⇒ 1)iborrow
                                                                             
                                                                                                                                                                    
                       when L1 > L2                      [Mutable-Reference]                                      when L1 > L2             [Immutable-Reference]
  D E ( hX 7→ L i              hL1 7→ L2 iref
                                               )
    ∗X               1 env
    V k     hL1 7→ 0imoved hL2 7→ Vistore
                                  [Dereference]
 Function definition and( function call                  )
  D fn F(TIDs) ->T{S} E hF ⇒ Li hL + 1i                       D mkDecls((X : T, TIDs), (V,Vs)) E     D         λ(TIDs,S,T)(Vs) K
                                                                                                                                         E ( h(Env, K, T)i            )
                                      env       nextLoc                                                                                                        fstack
            .           k    hL ⇒ λ(TIDs, S, T)istore           let X : T =V; mkDecls(TIDs, Vs) k      mkDecls(TIDs,Vs) S return (); k         hEnv ←⊥ienv
                [Function-Definition-with-Return-Type]                [mkDecls-Helper-Function]                                                     [Function-Call    ]
                     D fn F(TIDs) {S} E                                  D fn F(TIDs) -> T {S E} E                                      (
                                                                                                                       D return V; − E h(Env, K, T)i             )
                                                                                                                                                        fstack
                       fn F(TIDs) -> () {S} k                              fn F(TIDs) -> T {S return E;} k                   V K      k   h ← Envienv
  [Function-Definition-without-Return-Type]                [Function-Definition-Return-by-Last-Expression]                   when T = getT ype(V)      [Return]
 Struct and ownership(                                  )
  D struct Z {TIDs} E        hZ ⇒ Lienv hL + 1inextLoc
                                                                       D let mut X = Z {Vs}; E ( hX ⇒ L , Z 7→ L i           hL1 ⇒ 1imutType          hL1 ⇒ 0imoved
                                                                                                                                                                      )
                                                                                                               1         2 env
            .           k    hL ⇒ F1 (TIDs)istore                         F2 (F1 (TIDs),X,Vs)  k    hL1 ⇒ ZitypeEnv          hL2 7→ F1 (TIDs)istore hL + 1inextLoc
                                      [Struct-Definition
                                                       ]                                                                             [Declaration-of-Struct-Instance]
  D F (F ((Y : T, TIDs), X, (Y : V), Vs) E  hX.Y ⇒ Lienv             D          X = Y;
                                                                                                     E ( hX 7→ L , Y 7→ L , Z 7→ L i        hL1 7→ Z, L2 7→ ZitypeEnv
                                                                                                                                                                      )
     2 1                                                                                                         1        2        3 env
             F2 (F1 (TIDs), X, Vs)
                                                 hL ⇒ Vistore                 F3 (X, Y, TIDs) F4 (Y) k
                                            k
                                              
                                              
                                               hL + 1inextLoc 
                                                                                                        hL1 7→ 1imutType                   hL3 7→ F1 (TIDs)istore
                                       [F1 -F2 -Helper-Function]                                                                                    [Ownership-Move]
  D       F3 (X,Y,((P:T ),TIDs))
                                   E                           D F (X) E ( hX 7→ Li                )                     D E ( hX.Y 7→ L , X 7→ L i                   )
                                                                  4                    env                                 X.Y                 1          2 env
      X.P = Y.P;       F3 (X,Y,TIDs) k                              .   k   hL 7→ (0 ⇒ 1)imoved                             V k      hL1 7→ Vistore hL2 7→ 0imoved
              [F3 -Helper-Function]                                           [F4 -Helper-Function]                                        [Evaluation-of-Struct-Field]
                                                                                                        D X.Y = V; E ( hX.Y 7→ L , X 7→ L i         hL2 7→ 1imutType
                                                                                                                                                                      )
                                                                                                                                   1         2 env
                                                                                                              .     k   hL1 7→ ( ⇒ V)istore         hL2 7→ 0imoved
                                                                                                                                             [Updating-of-Struct-Field]



D. Formalization of the semantics                                                       the k cell, where X is a variable and T is a primitive type. A
   In this section, we present the formal semantics KRust in                            new pair L : ⊥ is added to store, where ⊥ indicates that X
K, emphasizing on key features of Rust such as: mutability,                             is uninitialized. The pair L : 0 is added to mutType, where
borrows and ownership. Table II shows the partial semantic                              0 means that X is immutable. The next available location
rules of KRust, which specify the semantics of Rust statements                          becomes L + 1 since X has consumed the location L. Some
by modifying the content of relevant cells. In the semantic                             other initialization operations are made in the relevant cells as
rules, operator ⇒ is used to add a new pair to its corresponding                        shown in the rule. The rule for the declaration of a mutable
cell. For instance, hX ⇒ Lienv means inserting a new pair X : L                         integer variable is defined likewise with a modification of the
into the env cell. The operator ⊥ denotes undefined value. Dot                          mutType cell.
· is a special character in K, representing the identity element                           The semantic rule [Assignment] is defined for the ordinary
in list and map structures. Note that curly braces are used only                        assignment, e.g., assigning a new value to an integer variable.
for the compactness of the rules, where we leave out all the                            It says that the assignment could be successfully executed only
dots “· · · ” in cells. The complete semantic rules of KRust can                        if X is mutable and the type of V is T , where getT ype is a pre-
be found in its source code.                                                            defined function to get the type of V. The execution updates
   1) Variable declaration and assignment: The semantic rule                            the value in store using L 7→ ( ⇒ V), where denotes that
[Declaration-of-Immutable-Variable] specifies how cells are                             the current value of L can be any. The notation A 7→ (B ⇒ C)
affected after the execution of the statement let X : T ; in                            will be used regularly in this work, which stands for replacing



                                                                                    5
the pair A : B by A : C in a cell. A declaration with an                   Type] handles the corner case that the function definition does
initial value can be handled similarly by combining the above              not have a return type, for which, the unit type () is added
semantic rules.                                                            as the return type. The semantic rule [Function-Definition-
   The semantic rule [Declaration-of-Mutable-Array] is de-                 Return-by-Last-Expression] handles another corner case that
fined for the declaration of a mutable array, where a new pair             the function definition returns the value of the last expression,
X : L is added to env, i.e., allocates a location L for X. In              for which, the last expression E is rewritten as a return
typeEnv, [T ; N] is the array type. L . . . L + N − 1 in store             statement return E;.
denotes the locations L, · · · , L + N − 1 which are uninitialized.           The rule [Return] first checks the type of the return value
The integer in nextLoc cell is increased by N, as locations                V, then returns the value V and finally restores the local
L, · · · , L + N − 1 are used to store the content of the array. The       environment Env and the computations K from the top of the
rules for the evaluation and updating of an array are defined              fstack cell at the same time.
likewise, as depicted in the table.                                           4) Struct and ownership: The rule [Struct-Definition] is
   2) Borrowing, reference, lifetime and dereference: Both                 used for struct definition, which adds a new pair Z : L into
immutable references and mutable references for borrow-                    the env cell. The value of L in store is a helper function F1
ing are implemented in KRust. [Mutable-Reference] and                      that is used to record the fields of the struct.
[Immutable-Reference] are two of semantic rules for im-                       The rule [Declaration-of-Struct-Instance] is defined for the
mutable and mutable references respectively. The [Mutable-                 declaration of a mutable struct instance. It allocates a location
Reference] rule expresses that if both X and Y are mutable                 L1 for X (i.e., adds X : L1 into env) and sets the type of L1
and have not been moved, and Y has not been borrowed yet,                  as Z, which is a struct name (i.e., add L1 : Z into typeEnv).
then the value of L1 in ref cell is updated to L2 , which may              Other related cells are initialized accordingly. The declaration
be used for dereference, the reference type of L1 in refType               and initialization of fields are handled by the computation
is assigned by 1 denoting that the reference type of L1 is                 F2 (F1 (TIDs), X, Vs), which is defined by the [F1 -F2 -Helper-
mutable, the pair L2 :⊥ in cell borrow is updated to L2 : 1                Function] rule. This rule recursively allocates a location for
meaning that Y is now mutably borrowed, while the condition                each field, which is initialized with the corresponding value
L1 > L2 ensures that X has to be declared later than Y, i.e., the          from Vs.
lifetime of X is included in the lifetime of Y. The [Immutable-               The rule [Ownership-Move] specifies Rust’s move seman-
Reference] rule is defined likewise, except that Y is already              tics, in which the assignment statement is encoded as the
immutably borrowed and the reference type of L1 in refType                 computations of two helper functions F3 and F4 , if X and
is assigned by 0 denoting immutable. The intuition behind the              Y have same type and X is immutable. Notice that the pair
[Dereference] rule is straightforward, namely, the value of ∗X             L3 : F1 (TIDs) in store ensures that Y is a struct instance. The
is evaluated via the reference relation L1 7→ L2 in the ref cell.          semantics of the helper functions F3 and F4 are expressed
   3) Function definition and function call: The standard func-            by the rules [F3 -Helper-Function] and [F4 -Helper-Function]
tion definition that has an explicit return type is handled by the         respectively. Intuitively, [F3 -Helper-Function] helps to copy
[Function-Definition-with-Return-Type] rule, which allocates               the fields from Y to X. [F4 -Helper-Function] is used to
a location L for the name F in the env cell and binds the                  update the move cell. We remark that hL1 7→ 0, L2 7→ 0imoved
location L with an auxiliary function λ() in store. The auxiliary          is not added in the [Ownership-Move] rule, as “X.P = Y.P;”
function λ() records the type and body of the function, which              in [F3 -Helper-Function] ensures that both variables are not
will be used for function call, i.e., the [Function-Call] rule.            moved yet. The semantic rules [Evaluation-of-Struct-Field]
   The function call is processed into two steps: first replacing          and [Updating-of-Struct-Field] are defined for evaluation and
the function name by its λ() function in store using the                   updating of a struct filed, in which it is required that the struct
[Lookup-of-Variable] rule, then applying the [Function-Call]               variable is not moved, i.e., the pair L2 : 0 should occur in
rule. The [Function-Call] rule first stores the current local              moved.
environment Env together with the return type T and the
remaining computations K into the fstack cell, reallocates a                                    IV. Testing and Applications
new empty local environment denoted by hEnv ← ⊥ienv in                       In this section, we validate our semantics KRust and show
the rule, and sets mkDecls(TIDs, Vs)            S     return (); as        some potential applications of KRust.
the computations. The latter firsts executes the helper function
mkDecls() which is used to declare formal parameters initial-              A. Conformance Testing
ized with actual parameters Vs recursively (c.f. the [mkDecls-                Following previous work [7], [11], [8], [13] which used test
Helper-Function] rule), then executes the function body S                  suite for validating executable language semantics, we tried to
followed by an additional return statement return ();. We                  do the same. We validated our semantics KRust by testing the
remark that return (); is added to handle the case that the                KRust interpreter (that was automatically generated from the
function definition does not have a return statement, and it               KRust semantics using K framework) against both the official
will be executed only if there is no return statement at the               test suite of Rust 3 and hand-crafted tests.
end of the function body S.
   The semantic rule [Function-Definition-without-Return-                    3 https://github.com/rust-lang/rust/tree/master/src/test.




                                                                       6
   The official test suite of Rust is used to test the Rust            As an example, we will verify the time complexity of the
compiler. It is already split into folders containing different        Euclidean algorithm by subtraction which computes greatest
categories of tests. We chose tests from the “run-pass” folder,        common divisor.
as others were designed for different purposes such as error       1     f n gcd ( a : i3 2 , b : i 3 2 ) −> i 3 2 {
message. There are 3119 tests in the “run-pass” folder: some of    2          i f a != b {
them can be compiled by the nightly version or stable version      3                  i f a>b { r e t u r n gcd ( a−b , b ) ; }
                                                                   4                  else    { r e t u r n gcd ( a , b−a ) ; }
of the compiler, and some may be ignored during compiler           5          } e l s e { return a ; }
testing, but it is unclear how these tests were used from the      6     }
official documents. Therefore, we parsed all 3119 and 195
of them are supported by our syntax. In 195 tests, there are              The Euclidean algorithm is implemented in Rust as
38 tests that either do not have a main function or call some          shown above. We will prove its time complexity is indeed
standard library functions. Therefore, we chose other 157 tests.       O(max(a, b)). To verify time complexity, an extra cell time is
   Because 157 tests might not cover all the supported con-            added to the configuration which increases a counter T each
structs, we hand-crafted 25 tests according to the syntax              time when gcd is called. The core part of the specification for
defined in Table I. 25 tests together cover all the primitive          proving is:
constructs.                                                        1      gcd (X : I n t , Y : I n t )
   We have tested the KRust interpreter against all these 182      2      <tim e > T1 => T2 </ tim e >
                                                                   3      requires X > 0 , Y > 0
tests. KRust successfully parsed all of them and the results       4      e n s u r e s T2 − T1 <= m ax I n t (X, Y)
produced by the interpreter are same as the one produced by
the compiled programs using the Rust compiler.                         where T1 and T2 respectively denote the value of the counter
   Remark that the semantic coverage of the test suite has not         T in pre-state and post-state of the function, requires and
been well-studied, we leave this to future work.                       ensures respectively denote pre-condition and post-condition,
                                                                       T2 - T1 denotes the number of calls to gcd, and maxInt is a
B. Applications                                                        built-in function which returns the larger one of two integers.
   One of the main goals of our semantics is to provide                The verifier outputs true which proves that T2 - T1 <=
a formal semantics for Rust. Beyond just giving a formal               maxInt(X,Y) holds, i.e., the time complexity is O(max(a, b)).
reference for the defined language, there are many applica-
tions of our formal semantics using the language-independent                                    V. Related work
tools provided by K. In this work, we demonstrate this by
                                                                          A multitude of formal semantics for real programming
showing two applications: debugging and verification, which
                                                                       languages have been proposed in the literature. Due to space
are automatically derived from the semantics KRust.
                                                                       restriction, we only discuss large semantics in K and other
Debugging. We can turn the K debugger into a debugger
                                                                       works related to Rust.
for Rust which allows users to inspect program states. We
demonstrate this by the following example.                             A. Other formal semantics in K
1   f n main ( ) {
2        l e t mut x : i 3 2 = 1 0 ;                                      Ellison and Rosu defined an executable formal semantics
3        while x > 0 {                                                 for C11, which has been extensively tested against the GCC
4              x = x − 1;                                              torture suite [7] and evaluated by debugging, monitoring,
5        }
6   }                                                                  and (LTL) model checking of C programs using the built-in
                                                                       capabilities of K. Hathhorn et al. defined undefined behavior
    We can debug this program using the command.                       in C11 [14], complementing the semantics of [7].
1   k r u n t e s t . r s −− d e b u g g e r                              Filaretti and Maffeis defined a formal semantics for PHP
                                                                       [11]. As there is no official language standard for PHP, they
   Users can step through one or more semantic rules individ-
                                                                       had to heavily rely on testing against the some test suite.
ually from the current point and print the current state. For
                                                                       Their semantics has been evaluated by model checking certain
instance, after executing Line 4 once, part of the state will
                                                                       properties of some programs.
look like below:
                                                                          Bogdanas and Rosu [8] gave a formal semantics for Java
1   <env > x | − > 1 </ env >                                          1.4, which is split into two phases: a static semantics and a
2   <typeEnv > 1 | − > i 3 2 </ typeEnv >
3   <mutType > 1 | − > 1 </ mutType >                                  dynamic semantic. The static semantics enriches the original
4   < s t o r e > 1 | − > 9 </ s t o r e >                             Java program by annotating statically inferred information,
                                                                       while the dynamic one gives the executable semantics. Their
Verification. A sound-by-construction program verifier for             semantics has been evaluated by model checking multi-
Rust can be automatically derived from KRust without ad-               threaded programs.
ditional effort. The verifier allows us to automatically check            Park et al. [13] presented a formal semantics for JavaScript
reachability properties including all Hoare-style functional           which has been tested against the ECMAScript 5.1 confor-
correctness claims and time complexity of a computation.               mance test and passes all core language tests.



                                                                   7
   Besides the above languages, the formal semantics of                  potential applications of KRust for debugging and verification
Python 3.3, Verilog, Scheme, LLVM IR and Esolangk were                   of Rust programs.
also defined in K [10], [15], [16], [17], [18].                             However, KRust does not cover the full features of Rust, as
   Compared to other language semantics in K, the most                   Rust is being actively developed and some of these features are
distinguished aspect of our semantics is the formalization               not stable so far. As a witness, although the Rust’s community
of the distinct features of Rust, namely ownership, borrow,              provides some syntax in EBNF [12], it is still far away from
lifetime, etc. To address these features, we had to redesign the         complete. This makes the formalization of Rust much difficult,
program state instead of just copying from the existing works.           as mentioned in [20]. The following is a list of features
Our semantics has been validated using the Rust standard test            that we haven’t implemented yet but plan to implement: (1)
suite as well as hand-crafted tests.                                     structs with reference fields, (2) pattern matching which can
                                                                         be seen as a generalization of switch-case, (3) trait objects
B. Works related to Rust                                                 which like interfaces in Java, (4) lifetime annotation which
   Rust has attracted some attention of researchers, and there           is used to mark explicit lifetime in functions or structs, (5)
are some works on the Rust type system and Rust program                  complex closures which use outside variables, (6) concurrency
verification.                                                            for writing multi-threading programs, (7) crates and modules
                                                                         which are used to call external library codes (8) unsafe which
   Reed presented a formal semantics for Rust that captures the
                                                                         is used to write code that the Rust compiler is unable to prove
key features relevant to memory safety, unique pointers and
                                                                         its safety, etc. A long-term program is to develop an almost
borrowed references, described the operation of the Borrow
                                                                         complete formal executable semantics for Rust and formally
Checker, and formalized the Rust type system [19]. The main
                                                                         verify Rust programs using formal analysis tools turned from
goal of this work is to provide a framework for borrow
                                                                         the semantics, towards which the work reported in this paper
checking. However, Rust has been evolved a lot since their
                                                                         is the first cornerstone.
work and their semantics has not been implemented yet,
hence not executable. Very recently, Jung et al. defined a                                              References
formal semantics and type system of a language λRust , which
                                                                          [1] N. D. Matsakis and F. S. Klock II, “The Rust language,” in ACM SIGAda
incorporates Rust’s notions [20]. Their work has been imple-                  Ada Letters, vol. 34, no. 3, 2014, pp. 103–104.
mented in Coq. The main goal of this work is to study Rust’s              [2] Redox, “Redox: a unix-like operating system written in rust,”
ownership discipline in the presence of unsafe code. However,                 https://www.redox-os.org, 2018.
                                                                          [3] B. Anderson, L. Bergstrom, M. Goregaokar, J. Matthews, K. McAllister,
the language λRust is close to Rust’s Mid-level Intermediate                  J. Moffitt, and S. Sapin, “Engineering the servo web browser engine
Representation (MIR) rather than the actual Rust language,                    using rust,” in ICSE’16, 2016, pp. 81–89.
and their semantics defines more behaviors than Rust does.                [4] Y. Ding, R. Duan, L. Li, Y. Cheng, Y. Zhang, T. Chen, T. Wei, and
                                                                              H. Wang, “POSTER: rust SGX SDK: towards memory safety in intel
Our semantics addresses to exact behavior of the actual Rust                  SGX enclave,” in CCS’17, 2017, pp. 2491–2493.
language and is executable.                                               [5] Stackoverflow, “https://stackoverflow.com/search?q=rust+,” 2018.
   Dewey et al. proposed a technique to fuzz type checker                 [6] G. Roşu and T. F. Şerbǎnuťǎ, “An overview of the k semantic frame-
                                                                              work,” The Journal of Logic and Algebraic Programming, vol. 79, no. 6,
implementations and applied to test Rust’s type checker [21].                 pp. 397–434, 2010.
It has identified 18 bugs. It is evident that formalization of the        [7] C. Ellison and G. Rosu, “An executable formal semantics of C with
Rust type system is important, while formalization of the Rust                applications,” in POPL’12, 2012, pp. 533–544.
                                                                          [8] D. Bogdanas and G. Roşu, “K-Java: a complete semantics of Java,” in
semantics is the first step toward this.                                      POPL’15, 2015, pp. 445–456.
   Two model checkers for verifying unsafe Rust programs                  [9] A. Ştefănescu, D. Park, S. Yuwen, Y. Li, and G. Roşu, “Semantics-based
have been proposed [22], [23], which verify Rust programs                     program verifiers for all languages,” in OOPSLA’16. ACM, 2016, pp.
                                                                              74–91.
by translating them into input languages of existing model               [10] D. Guth, “A formal semantics of Python 3.3,” Master’s thesis, University
checkers. Our semantics can be automatically turned into                      of Illinois at Urbana-Champaign, 2013.
formal analysis tools such as state-space explorer for reacha-           [11] D. Filaretti and S. Maffeis, “An executable formal semantics of PHP,”
                                                                              in ECOOP’14, 2014, pp. 567–592.
bility, model-checker and symbolic execution engine using the            [12] https://doc.rust-lang.org/grammar.html.
language-independent tools provided by K [9].                            [13] D. Park, A. Stefanescu, and G. Rosu, “KJS: a complete formal semantics
                                                                              of javascript,” in PLDI’15, 2015, pp. 346–356.
        VI. Conclusion, Limitations and Future Work                      [14] C. Hathhorn, C. Ellison, and G. Rosu, “Defining the undefinedness of
                                                                              C,” in PLDI’15, 2015, pp. 336–345.
   In this work, we proposed a formal executable semantics               [15] P. O. Meredith, M. Katelman, J. Meseguer, and G. Rosu, “A formal
                                                                              executable semantics of Verilog,” in MEMOCODE’10, 2010, pp. 179–
KRust for Rust using the K framework. KRust captures (1)                      188.
all the primitive types and their operations, (2) compound data          [16] P. Meredith, M. Hills, and G. Rosu, “A K definition of Scheme,”
types: struct, array and vector, (3) all the basic control                    University of Illinois at Urbana-Champaign, Tech. Rep., 2007.
                                                                         [17] LLVM IR in K, “http://github.com/davidlazar/llvm-semantics.”
flow constructs: for, while, loop, if, if/else, function                 [18] E. in K, “http://esolang-semantics.googlecode.com.”
definition/call and (4) three most distinct and important                [19] E. Reed, “Patina: A formalization of the rust programming language,”
features: ownership, borrow and lifetime. We tested Rust                      University of Washington, Tech. Rep., 2015.
                                                                         [20] R. Jung, J. Jourdan, R. Krebbers, and D. Dreyer, “RustBelt: securing
on many hand-crafted tests and Rust’s official tests suite. Tests             the foundations of the Rust programming language,” PACMPL, vol. 2,
in supported syntax are all passed. We also demonstrated                      no. POPL, pp. 66:1–66:34, 2018.




                                                                     8
[21] K. Dewey, J. Roesch, and B. Hardekopf, “Fuzzing the Rust typechecker               Rust,” in ASE’15, 2015, pp. 75–80.
     using CLP (T),” in ASE’15, 2015, pp. 482–493.                                 [23] F. Hahn, “Rust2viper: Building a static verifier for rust,” Master’s thesis,
[22] J. Toman, S. Pernsteiner, and E. Torlak, “Crust: A bounded verifier for            ETH Zürich, 2016.




                                                                               9
