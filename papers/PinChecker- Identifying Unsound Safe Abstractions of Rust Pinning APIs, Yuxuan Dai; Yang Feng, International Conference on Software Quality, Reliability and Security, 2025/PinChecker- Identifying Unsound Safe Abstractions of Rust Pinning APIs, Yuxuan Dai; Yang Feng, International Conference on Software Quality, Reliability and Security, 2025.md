                                                  PinChecker: Identifying Unsound Safe Abstractions of Rust Pinning APIs

                                                                                             Yuxuan Dai, Yang Feng∗
                                                       State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, 210023, China
                                                                                yxdai@smail.nju.edu.cn, fengyang@nju.edu.cn
                                                                                           *corresponding author


                                         Abstract—The pinning APIs of Rust language guarantee mem-            To help developers in using unsafe and creating safe abstrac-
                                         ory location stability for self-referential and asynchronous         tions correctly, the Rust community has compiled documents
                                         constructs, as long as used according to the pinning API con-        such as Rust’s Unsafe Code Guidelines Reference [3], pro-
                                         tract. Rust ensures violations of such contract are impossible       viding practical recommendations on how to avoid common
                                         in regular safe code, but not in unsafe code where unsafe            errors. For instance, library developers are encouraged to docu-
arXiv:2504.14500v2 [cs.SE] 20 Jun 2025




                                         pinning APIs can be used. Library authors can encapsulate            ment the safety conditions of their safe abstraction functions to
                                         arbitrary unsafe code within regular library functions. These        guide proper usage [4], although many libraries still lack such
                                         can be freely called in higher-level code without explicit           non-mandatory declarations [5]. Additionally, both academia
                                         warnings. Therefore, it is crucial to analyze library functions to   and industry have introduced various analysis tools [6], [7],
                                         rule out pinning API contract violations. Unfortunately, such        [8] that identify potential safety issues. Nevertheless, most
                                         testing relies on manual analysis by library authors, which is       projects continue to rely heavily on manual inspection to verify
                                         ineffective. Our goal is to develop a methodology that, given        edge cases related to unsafe code [9], [10]. In this context,
                                         a library, attempts to construct programs that intentionally         we focus on a particular standard library feature known
                                         breach the pinning API contract by chaining library function         as the pinning API [11], [12]. We investigate whether safe
                                         calls, thereby verifying their soundness. We introduce RPIL,         abstractions built around this Pin mechanism in user-created
                                         a novel intermediate representation that models functions’           Rust libraries might violate the pinning API contract [12].
                                         critical behaviors pertaining to pinning APIs. We implement          The Pin mechanism ensures memory location stability for self-
                                         PinChecker, a synthesis-driven violation detection tool guided       referential structures through the type system, serving as a
                                         by RPIL, which automatically synthesizes bug-revealing pro-          cornerstone for Rust’s asynchronous programming implemen-
                                         grams. Our experiments on 13 popular Rust libraries from             tation [11]. When developers implement asynchronous tasks
                                         crates.io found 2 confirmed bugs.                                    through the Future trait, the compiler constructs a state-
                                                                                                              machine data structure containing self-referential pointers,
                                         Keywords–rust; static analysis; program synthesis; constraint        which must rely on Pin’s pinning constraint semantics to
                                         solving; relational programming; software reliability                prevent self-referential pointer invalidation due to memory
                                                                                                              moves. Although the standard library documentation [12] pro-
                                         1. I NTRODUCTION                                                     vides warnings about avoiding improper encapsulation in each
                                                                                                              method’s “Safety” section, there remains a lack of specialized
                                         Rust has gained widespread attention and adoption across             automated detection tools for pinning API contract violations.
                                         multiple domains including operating systems, embedded de-           The challenge lies in that pinning API contract violations
                                         vices, and high-performance web frameworks, thanks to its            (henceforth referred to as pin violations) often remain latent
                                         efficient compiler and strict type system. In practice, Rust         within library functions. The violations manifest only when
                                         strictly controls memory access through core mechanisms such         users compose these functions into complete programs. This
                                         as ownership and borrowing checks, combined with lifetime            makes it necessary to generate test programs incorporating the
                                         inference to avoid common issues like dangling pointers and          library’s functions to verify the soundness of safe abstractions
                                         data races, thereby enhancing program safety. However, this          for pinning APIs. While existing program generation tools
                                         safety mechanism can restrict flexibility in scenarios that re-      such as JCrasher [13], Randoop [14], and RESTler [15] are
                                         quire low-level operations or custom memory management. To           available, they primarily rely on random or feedback-driven
                                         accommodate such demands, Rust allows the use of unsafe              mutation strategies and are designed specifically for languages
                                         to bypass certain compiler safety checks. Moreover, Rust             like Java. These tools lack understanding of Rust’s pinning
                                         permits encapsulating unsafe code inside regular non-unsafe          APIs and their semantics; direct adaptation would result in the
                                         functions, a practice known as creating a safe abstraction [1].      generation of test cases irrelevant to pinning API verification,
                                         The encapsulating functions can be freely called in higher-          rendering them ineffective for our purpose.
                                         level code without explicit warnings. An empirical study             To address these limitations, we present a constraint solving
                                         on open-source projects reveals that approximately 42.8%             based automated program synthesis tool specifically designed
                                         of safety-related patches revolve around the unsafe key-             for Rust pinning APIs. Our approach first translates library
                                         word [2], indicating latent security risks in the use of unsafe      functions’ critical behaviors into a novel lightweight interme-
                                         and safe abstractions.                                               diate representation RPIL, which precisely models operations
 Pin<&mut T>            Pin::new_unchecked                          pub struct SelfRef {
                                                           &mut T
                        Pin::get_unchecked_mut                        field1: i32,
                                                                      field2: Option<*const i32>,
      &mut T                                                          _marker: std::marker::PhantomPinned,
                        Pin::get_ref                         &T     }
                                                                    impl SelfRef {
                                                                      fn new() -> Self {
             Figure 1. Basic usage of Rust pinning APIs.                Self {
                                                                          field1: 42,
                                                                          field2: None,
                                                                          _marker: std::marker::PhantomPinned,
affecting values’ pinning states and reference relationships. A         }
                                                                      }
reversible interpreter implemented in Prolog then leverages
                                                                        fn init(&mut self) {
RPIL to synthesize minimal programs that trigger pin vio-                 self.field2 = Some(&self.field1 as *const i32);
lations through constraint solving.                                     }
We implemented the proposed techniques in PinChecker, an                fn validate(self: Pin<&mut Self>) {
extensible, synthesis-driven violation detection tool for Rust            let addr = &self.as_ref().field1 as *const i32;
                                                                          let stored_addr = self.as_ref().field2.unwrap();
libraries encapsulating unsafe pinning APIs. We evaluated                 assert_eq!(addr, stored_addr);
                                                                        }
PinChecker on 13 popular Rust libraries from crates.io and          }
discovered 2 pin soundness bugs. Our experimental results
demonstrate that PinChecker can effectively identify unsound
safe abstractions of pinning APIs with reasonable time cost.                Figure 2. Example self-referential struct implementation.
Furthermore, our evaluation shows that the reversible in-
terpreter design significantly improves detection efficiency
compared to conventional forward-only approaches. We make           calls. Consequently, any behavior that may violate the pin
the following key contributions:                                    API contract can only occur within unsafe contexts, ensuring
   • We introduce RPIL, a novel intermediate representation
                                                                    that the pinning API contract cannot be violated in ordinary
      that models functions’ critical behaviors pertaining to       contexts without unsafe code.
      pinning APIs.                                                 To demonstrate the definition of self-referential structures
   • Based on RPIL, we implement a violation detection tool         and related pin API contract violations, Figure 2 presents an
      called PinChecker for Rust libraries encapsulating unsafe     example of a self-referential struct, showing its definition and
      pinning APIs.                                                 implementation. The struct contains two data members: one
   • We evaluate PinChecker on popular Rust libraries and           stores concrete data, while the other holds a pointer pointing
      demonstrate that it can generate minimal pin violation        to the former. The struct includes three operations: 1) Creation
      programs that expose bugs.                                    (new): creates an instance of the struct and assigns a concrete
                                                                    value to member field1; 2) Initialization (init): assigns a
2. BACKGROUND AND M OTIVATING E XAMPLE                              raw pointer to member field2, whose value is the address of
In Rust, the standard library’s pin module provides a series        the instance’s member field1; 3) Validation (validate):
of API functions for creating and manipulating Pin pointers.        verifies whether the address of member field1 matches the
These functions are categorically divided into regular functions    address stored in member field2. The validation operation’s
and unsafe functions. As shown in Figure 1, function names          method SelfRef::validate accepts a Pin pointer rather
in green represent ordinary APIs that can be invoked in non-        than an ordinary mutable reference as its parameter; conse-
unsafe contexts, such as Pin::get_ref which extracts an             quently, this function must be called on a Pin pointer. Such
immutable version (&T) of the reference encapsulated by a Pin       design is common in practice to ensure that mutable references
pointer. Since immutable references cannot trigger memory           cannot be obtained within the function, thereby protecting the
moves, there is no risk of pinning API contract violations.         integrity of self-referential data.
In contrast, functions names in red represent unsafe APIs,          To further illustrate the design of Pin APIs and how unsound
such as Pin::new_unchecked for creating Pin pointers                safe abstractions can lead to pinning API contract violations,
and Pin::get_unchecked_mut for extracting mutable                   suppose we are developing a Rust library named mylib,
references (&mut T) from Pin pointers. These functions in-          with the above self-referential struct as part of it. The typical
tentionally include “unchecked” in their names and must             workflow is: creating an instance of the struct, calling init
be called within unsafe contexts. Because they manipulate           to establish a self-reference, then creating a Pin pointer to the
unrestricted mutable references, they can be directly used          struct and calling validate via that Pin pointer to verify
in memory move operations like mem::swap, which may                 the validity of the self-reference.
introduce risks of pinning API contract violations [11].            For user convenience in creating Pin pointers, we might
The core principle of the pin contract is to encapsulate mutable    define a pin_new function that directly accepts a &mut T
references (&mut T) so that only immutable references can           to produce a Pin<&mut T>, effectively providing a safe
be freely obtained, while mutable references can only be            abstraction over the originally unsafe Pin function. Such safe
acquired in unsafe contexts through specific unsafe function        abstraction is risky as it overlooks the fact that the pin
A safe abstraction function introduced in mylib:                      is as follows: Given the Cargo.toml file path of a target
pub fn pin_new<T>(r: &mut T) -> Pin<&mut T> {                         Rust library, the MIR2RPIL component first extracts the RPIL
  unsafe { Pin::new_unchecked(r) }
}                                                                     representations of all public functions in the library. It then
                                                                      hands these representations to the PinChecker detection tool,
Erroneous usage example:                                              which attempts to construct counterexample Rust programs
let mut v1 = SelfRef::new();                                          that cause a pin violation, and finally returns them back to
v1.init();                                                            the user for verification. The core idea of this process is to
let v2 = mylib::pin_new(&mut v1);
v2.validate();                                                        abstract away the parts of the Rust program that are directly
mem::swap(&mut v1, ...);
                                                                      related to the pinning API contract, thereby reducing analysis
Expected usage example:                                               complexity and enabling detection of pin violations through
let mut v1 = SelfRef::new();
                                                                      automated means.
v1.init();                                                            On Program Structure. We abstracted the Rust programs by
let v1 = mylib::pin_new(&mut v1);
v1.validate();                                                        transforming them into linear sequences of single-line function
                                                                      calls. Specifically, each line of code calls a single function and
      Figure 3. An unsound safe abstraction function and its usage.   assigns its result to a new variable. Figure 5 shows the linear
                                                                      single-line function call form corresponding to the erroneous
                                                                      usage example shown in Figure 3. This linearized format
contract’s effectiveness relies on restricting the acquisition        makes it easier to split the program into multiple steps and
of mutable references to unsafe contexts only. Specifically,          track the evolution of variables and the program context at
although this function constructs a Pin pointer, it doesn’t           each step, facilitating subsequent formal analysis.
prevent the acquisition of mutable references. As shown in            On Aggregate Value Structure. To precisely describe how
the erroneous usage example in Figure 3, although Pin pointer         composite types (such as structs, enums, and arrays) are used
v2 is created, one can still obtain a regular &mut v1, use it         in programs, we introduced a sequential index based labeling
to perform memory-moving operations, and ultimately violate           scheme to uniquely number each substructure within an aggre-
the pinning API contract.                                             gate value. Specifically, struct fields are numbered according
One possible correct usage is shown in the expected usage             to their declaration order, enum variants and their internal
example in Figure 3. By shadowing the original variable which         fields are numbered similarly, and array elements are marked
employs variable shadowing to override the original variable,         as different substructures based on their index positions. In
the new Pin pointer becomes the sole medium through which             this way, any deep access into an aggregate value can be
one accesses the underlying value, thereby preventing the             represented with a notation like “variableName[substructure
possibility of pinning API contract violations. However, as           index]”, facilitating subsequent formal analysis. For instance,
the above analysis shows, mylib’s pin_new safe abstraction            consider the composite type definitions in Figure 6, deep
function conceals a security flaw: its correctness depends on         access expressions like my_var.unwrap().ptr are rep-
callers following a strict and error-prone usage pattern. Once        resented in the form my_var[1][2].
the caller fails to shadow the original variable, a direct mutable    On Variable and Value States. We employ the concept of
reference can still be acquired, which may enable memory              program context, to maintain state descriptions for all variables
move operations that threat pin soundness.                            and their substructures at each line of program execution.
Hence, if a library function provides a seemingly safe but            The context consists of three components (V, R, S), where
actually unsound abstraction of an unsafe Pin operation, it can       the variable set V records currently live variables and their
enable constructing programs that violate pinning API con-            type information, directed graph R represents the reference
tract, leading to severe safety vulnerabilities. This is precisely    relationship graph, using directed edge p ⇝ q to indicate
the risk our work aims to identify and address.                       value p references value q, and the state space S tracks state
                                                                      changes each value (including substructures within composite
3. C ONSTRAINT-BASED D ETECTION OF P IN V IOLATION
                                                                      types) undergoes during execution, such as whether it has
According to the Rust documentation, pinning contract vio-            been pinned or forgotten for destruction. For instance, a value
lations manifest in two ways: (1) moving values that have             in its initial state transitions to pinned state after being
already been pinned, and (2) failing to guarantee that pinned         pinned. Further state transitions are described in detail in
objects will eventually be dropped (the requirement that pinned       in Section 3.2.3. This approach enables precise tracking of
objects must be dropped is also referred to as the Drop               variable availability, value reference relationships, and value
Guarantee [11]).                                                      states required for pin violation checking.
In this study, we propose a constraint solving based approach         On Function Behavior. We divide a function call into two
for detecting pin API contract violations in Rust libraries.          components: static behavior and dynamic behavior. Static
This approach automatically synthesizes minimal counterex-            behavior is reflected by type inference information carried
ample programs that expose unsound safe abstractions, thereby         in function signatures, which determine the types of new
helping developers to uncover vulnerabilities that may lead to        variables created and added to variable set V after each
pin violations. As illustrated in Figure 4, the overall process       function call. Dynamic behavior is captured by an inter-
                      MIR2RPIL                                      PinChecker                                                          ×          !
                                                                                                                                  Move        ¬Drop
                                                                                                 typing
                                                                                                                               pin-violating
                             rustc                                                               borrowing
                          compilation           RPIL                                                                           program state
                                                                                                   pinning
                                                                                                    liveness                    let · = f1()
                                                                                                                                let · = f2(·) ← pin
                             MIR             translation                                                                        let · = f3(·, ·)
library function                                                     library functions          constraint                      let · = f4(·) ← move!
                                    extracts pin-relevant
   definitions                                                            encoded                 rules                          pin violation
                                         behaviors
                                                                                                                                   program
                                              Figure 4. The workflow of PinChecker’s components.


                                                                          Table 1. Semantics and State Impact of RPIL Instructions.
let v1 = SelfRef::new();        // ;
let v2 = borrow_mut(v1);        // BORROW(v2, v1);                        Instruction        Description                  Context Impact
let v3 = SelfRef::init(v2);     // BORROW(v2[2][1], v2[1]);
let v4 = mylib::pin_new(v2);    // DEREF-PIN(v2);                         BORROW(r, p)       Record that r references p   Adds an r ⇝ p relation-
let v5 = SelfRef::validate(v4); // ;                                                                                      ship
let v6 = deref_move(v2);        // DEREF-MOVE(v2);
-----------------------------------------------------------               BIND(p, q)         Binds q to p                 Transfers references as-
line 1: { }                                                                                                               sociated with q to p
line 2: { v2->v1 }
line 3: { v2->v1, v2[2][1]->v2[1] }                                       DEREF-PIN(r) Pin the referenced target          Sets p to pinned state∗
line 4: { v2->v1, v2[2][1]->v2[1], v1:pinned }
line 5: { v2->v1, v2[2][1]->v2[1], v1:pinned }                                         if r ⇝ p ∈ R
line 6: { v2->v1, v2[2][1]->v2[1], v1:pinned_moved }
                                                                          DEREF-MOVE(r)Memory move the refer-             If p is now in pinned
                                                                                       enced target if r ⇝ p ∈ R          state, transition it into
                                                                                                                          pinned_moved state∗
Figure 5. The linear form of a program and the RPIL
                                                                          FORGET(p)          Suppresses the invocation    Sets p to forgotten
instruction sequence corresponding to each function (above),                                 of p’s destructor            state∗
the program context after executing the current line (below).             ∗ For detailed behavior, see Section 3.2.


struct SelfRef {
  data: i32,             // "data" labeled as [1]
  ptr: *const i32,       // "ptr" labeled as [2]                        tion and analysis of pin-related behaviors in Rust programs,
}                                                                       providing a clear, operational formal foundation for subsequent
enum Option<T> {                                                        static analysis and program synthesis.
  None,
  Some(T), // content of "Some" labeled as [1]                          1. Extracting Function Behaviors: MIR2RPIL
}
let my_var = Option::Some(SelfRef { ... } );                            To accurately capture the low-level operations in Rust that are
                                                                        related to Pin, we chose MIR [16] as the basis for representing
            Figure 6. Example composite type definitions.               function behaviors. MIR is the intermediate representation
                                                                        generated during Rust compilation process. On the one hand,
                                                                        as a lower-level IR, MIR clearly reflects memory operations
mediate representation called RPIL (Reference Provenance                in a program, including critical behaviors like memory moves.
Intermediate Language), defined in this study. RPIL refines all         On the other hand, MIR preserves Rust’s higher-level seman-
operations related to reference creation, assignment, pinning           tics, making Pin-related operations identifiable. Due to these
constraints, and memory moves into atomic-level instructions,           two characteristics, MIR not only serves as the foundation
including BORROW, BIND, DEREF-PIN, DEREF-MOVE, and                      for ownership and borrowing checks in the Rust compiler
FORGET. Figure 5 demonstrates through an example the RPIL               itself, but is also employed in analysis tools like Miri [17].
instruction sequences corresponding to each function call and           However, MIR representation contains many implementation
how the program context updates with each instruction’s                 details irrelevant to pin violation analysis. More importantly,
execution. For example, in line 4, since v2 ⇝ v1 ∈ R, meaning           it lacks the ability to directly express key properties like
v2 references v1 , the DEREF-PIN(v2 ) instruction causes the            pinning states, which limits its application in our pin violation
referenced target value v1 to enter pinned state. Table 1               detection work.
provides a more detailed explanation of the semantics for each          To overcome these limitations, we propose RPIL (Refer-
RPIL instruction and its impact on the program context.                 ence Provenance Intermediate Language), a specialized in-
These four aspects of abstraction, by removing nonessential             termediate representation language designed for pin violation
language features and focusing on core semantics directly               detection to represent function behaviors. RPIL eliminates
related to the pin API contract, together form a complete in-           nonessential details from MIR while adding capabilities to
termediate representation model. that enables accurate descrip-         track reference targets and pinning state transitions, providing
     a more suitable foundation for subsequent violation analysis.       pub fn store_refs<’a, T>(          store_refs(_1, _2)
                                                                           ref1: &’a mut T,                 bb0: [
     Based on this, we provide a deterministic translation algorithm       ref2: &’a mut T                    _3 = Option::Some(copy _1),
     from MIR to RPIL that precisely extracts and converts the           ) -> RefStore<’a, T> {               _4 = Option::Some(copy _2),
                                                                           RefStore {                         _0 = RefStore::<’_, T> {
     behaviors of library functions.                                         store1: Some(ref1),
                                                                             store2: Some(ref2),
                                                                                                                store1: move _3,
                                                                                                                store2: move _4
                                                                           }                                  } -> return
                                                                         }                                  ]
   Algorithm 1: Translation of MIR to RPIL
   Input: MIR representation of a library function F                     _0: RefStore<T> = store_refs(_1: &mut T, _2: &mut T)
   Output: A set of RPIL variants T                                        BIND(_0[1][1], _1);
                                                                           BIND(_0[2][1], _2);
 1 Initialize translation context ctx ;
 2 Push (⟨F, bb0 ⟩, ctx ) onto worklist Q;
                                                                                Figure 7. Rust code (left), MIR (right) and RPIL (bottom).
 3 while Q is not empty do
 4      Pop (⟨fn, bb⟩, ctx ) from Q;
 5      foreach stmt ∈ bb.statements do                                  RPIL variants. A single function’s MIR may yield multiple
 6          Interpret stmt based on its MIR kind, update ctx ;           RPIL variants by enumerating all possible control-flow paths.
 7      switch bb.terminator do                                          To illustrate the translation process of the MIR2RPIL module,
 8         case Call(fn ′ ) do                                           let us consider function store_refs as a typical case for
 9             Prepare a new call stack frame in ctx ;                   MIR to RPIL translation. Figure 7 compares the function’s
10             Push (⟨fn ′ , bb 0 ⟩, ctx ) onto Q;                       Rust code and its MIR representation (simplified for presen-
11         case Return do                                                tation).
12             Retract the top call stack frame from ctx ;               This function takes two mutable reference parameters and
                                                                         constructs a RefStore structure that encapsulates these two
13      if call stack is empty then                                      references. From the function’s MIR, we can see it contains
14          Finalize ctx to extract an RPIL sequence, add it             three basic operations: First, it wraps the first parameter as an
             to T ;                                                      Option::Some value and store it in temporary variable _3;
15      if bb.terminator has successors then                             Second, it wraps the second parameter as an Option::Some
16          foreach successor basic block bb next do                     value and store it in _4; Third, it combines _3 and _4 into
17              Push (⟨fn, bb next ⟩, ctx ) onto Q;                      a RefStore instance and assign it to the return value (_0).
                                                                         When handling assignments whose right-hand side is a
18   return T ;                                                          composite data structure, such as in the third step above,
                                                                         MIR2RPIL breaks down the assignment statement into mul-
     During the translation process, the system first runs the           tiple atomic assignments, processing one assignment at a
     Rust compiler with the target library’s Cargo.toml as a             time. For example, when translating _0 = Refstore {
     parameter. Once the compiler has generated MIR, the process         store1: _3, store2: _4 }, it splits it into two as-
     intercepts the execution. It begins by enumerating all public       signments: _0[1] = _3 and _0[2] = _4. The mod-
     functions, then for each function, starts sequential translation    ule then deduces via the mapping relationships, and gen-
     from the first statement of its first basic block. When reaching    erates two RPIL instructions: BIND(_0[1][1], _1);
     a basic block’s terminator, if encountering a function call, it     BIND(_0[2][1], _2);.
     enters the first basic block of the called function and continues   This algorithm and example highlight three core strategies in
     translation from its first statement; after the function returns,   the MIR2RPIL module: 1) Control flow linearization: using
     it goes back to the the terminator of the original basic block.     depth-first traversal of basic blocks to enumerate possible
     If multiple jump targets exist at the end of the current basic      control flow paths, converting branch structures into sequential
     block, the translation will attempt each as the next block. The     execution paths; 2) Structured decomposition during assign-
     translation continues until encountering a return marker.           ment: breaking down assignments with composite right-hand
     Throughout the translation process, the system maintains map-       sides into atomic assignment operations, ensuring each RPIL
     ping relationships between local labels (i.e., MIR locals [16]      instruction operates on only a single label; 3) Tracking of
     such as _1, _2, _3) within the function and state change            state changes: capturing the functions’ modifications to values’
     operations on local labels. Algorithm 1 presents the overall        states, accurately recording key state-changing operations like
     flow for translating MIR to RPIL.                                   DEREF-PIN and DEREF-MOVE. These strategies effectively
     MIR and RPIL differ in their models. MIR divides function           extract critical function behaviors from MIR, providing an
     bodies into multiple basic blocks connected by jump state-          accurate behavior model for subsequent constraint solving in
     ments, with the execution path determined dynamically at            detecting pin violations.
     runtime. In contrast, RPIL linearizes all basic blocks during
     translation, flattening one possible control flow path into one     2. Synthesizing Pin Violations: PinChecker
     large basic block. Different execution paths yield different        The PinChecker detection tool is the core component in our
     RPIL representations, we refer to these different outputs as        work for detecting pin API contract violations. Its fundamental
                                   Table 2. Core predicates in PinChecker’s implementation.
 Signature                                      Description                                                         Directionality    Nature
 typeof(Prgm,V,T)                               Variable V in program Prgm is of type T                             Bidirectional    Synthetic
 liveness(Prgm,V,L)                             Variable V in program Prgm is L (alive/dead)                        Bidirectional    Synthetic
 borrows(Prgm,R,P)                              Reference relationship R ⇝ P exists in program Prgm                 Bidirectional    Synthetic
 state(Prgm,P,St)                               Value P in program Prgm is in state St                              Bidirectional    Synthetic
 fn_type(Fn,[Ty1,Ty2,...],RetTy)                Function Fn’s type signature is Ty1 × Ty2 × · · · → RetTy           Bidirectional    Inherited
 fn_rpil(Fn,[Ret,Arg1,Arg2,...],Rpil)           Gets the RPIL of function Fn, replacing placeholders for return     Forward-only     Inherited
                                                value (_0) and arguments (_1, _2, . . . ) with concrete variables



idea is to construct a program by composing multiple library         ?- Prgm = [
functions, such that the program reaches a pin violation state         v1 = SelfRef::new(),     // ;
                                                                       v2 = borrow_mut(v1),     // BORROW(v2, v1);
after execution (e.g., when a pinned value undergoes a memory          v3 = mylib::pin_new(v2), // DEREF-PIN(v2);
                                                                       v4 = deref_move(v2),     // DEREF-MOVE(v2);
move). To achieve this goal, PinChecker implements a special         ], borrows(Prgm, v2, X), state(Prgm, v1, Y).
reversible interpreter, that supports both forward execution of      X = v1,
                                                                     Y = pinned_moved.
programs to determine their final state and reverse execution
that that performs backward reasoning from a desired state to        ?- length(Prgm, 2), borrows(Prgm, v2, v1).
                                                                     Prgm = [
synthesize a program capable of reaching that state.                   v1 = SelfRef::new(),
                                                                       v2 = borrow(v1),
                                                                     ];
1) Overview                                                          Prgm = [
                                                                       v1 = SelfRef::new(),
                                                                       v2 = borrow_mut(v1),
PinChecker synthesizes pin-violating programs by establishing        ].
a many-to-one mapping between programs and their post-
                                                                     ?- length(Prgm, 4), state(Prgm, X, pinned_moved).
execution contexts. It takes as input the signatures and RPIL        Prgm = [
                                                                       v1 = SelfRef::new(),
instructions of library functions, then employs a Prolog-              v2 = borrow_mut(v1),
based reversible interpreter to perform bidirectional reasoning.       v3 = mylib::pin_new(v2),
                                                                       v4 = deref_move(v2),
PinChecker leverages this property by querying the interpreter       ],
to derive programs that result in contexts exhibiting pin            X = v1.
violations. When such a program is successfully synthesized,
it confirms that the provided set of library functions can be        Figure 8. Usage examples of PinChecker’s Prolog predicates
composed to violate the pin contract.                                (marked green). The top example demonstrates forward inter-
PinChecker is implemented as a suite of utility predicates that      pretation, while the bottom two illustrate backward interpre-
together capture the correlation between a program and its exe-      tation for program synthesis.
cution context. Each predicate is designed to address a specific
aspect of the analysis; for example, borrow/3 encodes the
reference relationships between values, and status/3 tracks            2. Fn’s type signature Ty1 × · · · × Tyk → RetTy is
values’ pin/forget states.                                                satisfiable;
Figure 8 presents examples of PinChecker’s predicates in
                                                                     Rule 1 establishes the typing requirements for function calls.
use. The top example demonstrates forward interpretation,
                                                                     It ensures that all arguments are properly typed and available
while the latter two illustrate backward interpretation for
                                                                     at the point of function invocation.
program synthesis. Because multiple programs can satisfy the
same constraints, backward interpretation may yield multiple         Rule 2 (Variable Liveness). Let the last line in program
solutions, as shown in the middle example.                           be Ret = Fn(Arg1,. . .,Argk). The variable V’s liveness
Table 2 lists the core predicates used in PinChecker. The            will be changed by the last line, if any of the following
predicates work cohesively to guide the synthesis process,           conditions is satisfied.
pruning the search space of candidate programs.                        1. Variable V turns alive, when V = Ret and Ret is
                                                                          well-typed;
2) Constraint Rules Guiding PinChecker                                 2. Variable V turns dead, when V is one of Arg1, . . . ,
PinChecker implements a set of formal rules, capturing key                Argk, and function Fn can consume V;
aspects of the type system, variable liveness, reference re-         Rule 2 manages variable lifetimes by tracking value con-
lationships, and state transitions. These rules ensure correct       sumption. A variable becomes alive when assigned a well-
interaction between predicates during program synthesis.             typed return value, and becomes dead after being used in
Rule 1 (Variable Well-typedness). Let the last line in program       function arguments. The only two exceptions are borrow and
be Ret = Fn(Arg1,. . .,Argk). The variable Ret is well-              borrow_mut, which create references without consuming
typed (i.e., clause typeof(Prgm, Ret, _) is satisfiable),            their arguments.
if all of the following conditions are satisfied.                    Rule 3 (Reference Introduction). Let Rpil denote the RPIL
 1. Variables Arg1, . . . , Argk are well-typed and are alive;       sequence of the function that the last program line calls. The
          start            p            DEREF-PIN(r),                pinned_forgotten especially represent pin violating
     FORGET(p′ ),                       r⇝p ∈ R                      states.
     p′ ⊐ p                                         DEREF-MOVE(r),   3) Synthesizing Pin Violations
         p : forgotten           p : pinned         r ⇝ p′ ∈ R,      The two categories of pin violations correspond to
                                                    p′ ⊐ p           pinned_moved and pinned_forgotten. When any
DEREF-PIN(r),          FORGET(p′ ),                                  value in the program’s execution context enters either of these
r⇝p ∈ R                p′ ⊐ p       p : pinned moved                 states, it indicates that the program has exhibited behavior that
     p : pinned forgotten                                            violates the pin API contract.
                                                                     PinChecker’s program synthesis mechanism is based on con-
                                                                     straint solving: it searches for function call sequences that
                Figure 9. State transition of a value.
                                                                     satisfy specific constraint conditions by running the interpreter
                                                                     in reverse. Specifically, the target state is defined as a program
reference relationship R ⇝ P is introduced, if any of the            context exhibiting a pin violation, described with a clause like
following conditions is satisfied.                                   state(Prgm, _, pinned_moved) (where the wildcard
  1. BORROW(Lhs, Rhs) is one instruction in Rpil,                    “_” is a Prolog feature denoting existential constraint), re-
     where Lhs evaluates to R, and Rhs evaluates to P;               quiring at least one value to be in this anomalous state
  2. BIND(Lhs, Rhs) is one instruction in Rpil, where                after program Prgm’s execution. Given the target context,
     reference relationship RepLhs→Rhs (R) ⇝ P holds;                the interpreter uses a constraint-based backward interpretation
                                                                     strategy to synthesize program Prgm line by line from back
Repv′ →v (·) is an operator to replace a value’s belonging
                                                                     to front, searching for all possible programs that can reach
variable v ′ with v.
                                                                     this state. If at least one program is successfully generated,
Rule 4 (Reference Retraction). The reference relationship            it demonstrates that the combination of related functions in
R ⇝ P does not hold any more, when the variable that R               the target library can give rise to a pin violation, proving the
belongs to turns dead, or when the variable that P belongs           existence of safe abstraction defects in the library.
to turns dead.                                                       PinChecker is guaranteed to terminate. If the constraint solving
                                                                     space is exhausted without finding a feasible solution, the
Rules 3 and 4 form the core mechanism for tracking ref-
                                                                     system will terminate and return an empty result set, ensuring
erence relationships. These rules implement the semantics
                                                                     the analysis will not run indefinitely.
of RPIL instructions BORROW and BIND. The BORROW in-
struction introduces a new reference relationship, while BIND        4. I MPLEMENTATION AND E VALUATION
transfers existing references between values. For example,           We have implemented PinChecker, a tool that automatically
if v2[1] ⇝ v1 holds, then executing BIND(v3, v2)                     detects pin contract violations caused by improper safe ab-
introduces v3[1] ⇝ v1. The BORROW operation supports                 stractions in Rust libraries through constraint solving based
dereferencing through existing relationships: BORROW(v4,             program synthesis. To systematically evaluate PinChecker, we
(*v2[1])) would first resolve *v2[1] to v1 via the                   conducted experiments on real Rust crates from crates.io,
existing reference, then introduce v4 ⇝ v1.                          focusing on the following three research questions:
Rule 5 (State Transition of Values). A value can be in initial       RQ1. Can PinChecker detect pin contract violations in real-
state, or one of pinned, forgotten, pinned_moved and                         world Rust libraries?
pinned_forgotten. The state transitions for a value are              RQ2. How does PinChecker perform in synthesizing pin
shown in Figure 9, with transition conditions labeled on the                 violation programs for libraries of various scales and
arrows.                                                                      complexities?
                                                                     RQ3. How expressive is PinChecker’s linear program form in
Take the transition from pinned to pinned_moved as an                        capturing real-world pinning API usage?
example, the transition requires a DEREF-MOVE(r) instruc-
tion, along with the conditions that r ⇝ p′ ∈ R and p′ ⊐ p           1. Implementation of MIR2RPIL
hold, meaning a reference relation from r to p′ exists in the        MIR2RPIL extends the Rust compiler through the
program context’s reference relationship graph, and p′ is a sub-     rustc_private interface to extract and convert MIR
location of p. For instance, if v1 [1] is in pinned state and        representations of all public (pub) functions into RPIL. The
v2 holds a reference to v1 , then executing DEREF-MOVE(v2 )          implementation operates in two stages:
will cause v1 [1]’s state to transition to pinned_moved.             In the first stage, it obtains the compilation context by invoking
This corresponds to using mem::swap through a reference              Cargo commands [18] with the target crate’s Cargo.toml, then
to a value causes that referenced value and its internal sub-        identifies the arguments to the last rustc command, the
places to undergo a memory move.                                     command that compiles the target crate itself.
Rule 5 forms the core mechanism for tracking val-                    In the next stage, MIR2RPIL replaces rustc to execute the
ues’ states pertaining Rust’s pinning APIs, especially pin           last command, using the same command-line arguments iden-
violations. The latter two states, pinned_moved and                  tified in the previous stage. MIR2RPIL injects its logic during
  (a) Eager liveness check                                               2. Pin-related Safe Abstraction Functions. Libraries contain
                                                      Entry
                                                                             public functions that provide safe abstractions over unsafe
                                                                             pinning APIs.
   Rule 1        Rule 3       Rule 5         Pin violation constraints
                                                                         3. Pinnable Data Structures Implementing the Drop Trait.
                                                                             Libraries contain pinnable (types which are not Unpin)
   Rule 2        Rule 4                             Violation                data type definitions that implement the Drop trait.
                                                    program
                                                                         Following these criteria, we ultimately selected 13 qualifying
  (b) Lazy liveness check                                                libraries. For each library, we first run MIR2RPIL to list the
                                                      Entry
                                                                         paths, names, and type signatures of all public (pub) functions
                                                                         along with their RPIL translation results. PinChecker allows
   Rule 1        Rule 3       Rule 5         Pin violation constraints
                                                                         for the selection of up to 10 functions to be analyzed. To
                                                                         ensure comprehensive coverage, the public functions listed by
   Rule 2        Rule 4                          Liveness check
                                                                         the MIR2RPIL module are sorted, prioritizing safe abstraction
                                                                         functions containing internal unsafe blocks. The selection
                                                    Violation
                                                                         strategy is: prioritize safe abstraction functions (i.e., the first
                                                    program
                                                                         10 functions) for testing, while allowing users to adjust se-
                                                                         lections based on testing requirements, such as when users
 Figure 10. Comparison between PinChecker’s implementation strategies.   want to test specific modules. In addition to library functions,
                                                                         we added 4 default functions to each library’s function set,
the AfterAnalysis phase, traversing the crate to filter public           including 2 for supporting Rust borrowing operations: & and
function definitions. For each function, it applies Algorithm 1          &mut, 1 for memory move operations: deref_move (such
to translate their MIR into RPIL.                                        as mem::swap or mem::replace), and 1 for the “drop-
                                                                         forgetting” operation: forget.
2. Implementation of PinChecker
PinChecker is implemented in Prolog as a reversible                      4. Experiment Setup
interpreter-based violation detection tool using the core predi-         PinChecker attempts to automatically synthesize potential pin
cates listed in Table 2 and auxiliary predicates that enforce            violation triggering cases within a time limit. For efficiency
the five constraint rules in Section 3.2.2. We use SICStus               and comprehensiveness, we ran experiments in parallel in a
Prolog [19] for execution. Our initial “monolith” implemen-              server environment to reduce both individual library detection
tation, integrated all five rules, but we found that liveness            time and overall detection time. During the experiments,
rules (Rule 2 and Rule 4) were time-consuming to evaluate.               we used the following hardware and software environment.
We therefore developed a variant with lazy liveness check                Hardware environment: We used a server equipped with an
that defers liveness verification. Figure 10 compares the two            Intel Xeon Gold 6326 processor and 256GB of memory. Soft-
implementation strategies. We evaluate their performance in              ware environment: Ubuntu 23.10 operating system. The Rust
Section 5.2.                                                             compiler version was 1.87.0-nightly to ensure compatibility
The synthesis procedure in PinChecker requires pre-                      with the latest language features and library versions. We
determining the target program length. Accordingly,                      used SICStus Prolog 4.9.0 to run PinChecker. During the
PinChecker begins by synthesizing 1-line programs. If                    experiments, the server ran all analysis tasks concurrently in
no violation program is generated at the current length, the             containers.
synthesis length limit is iteratively increased by one. Upon             For each crate, we first ran the MIR2RPIL module to extract
finding the first violation program, PinChecker reports the              the RPIL representations of the selected functions from the
result and terminates further exploration.                               library; these representations were then incorporated into a
                                                                         PinChecker code template to form a complete Prolog program.
3. Selection of Libraries and API Functions
                                                                         Next, we ran PinChecker to analyze the combinations of these
To evaluate PinChecker’s effectiveness, we selected a repre-             functions. To control experiment scale and duration, we set a
sentative set of Rust libraries from crates.io for testing. We           runtime limit of 10 hours per crate.
primarily focused on libraries related to the Pin mechanism,             It is worth noting that while experiments were conducted on
as these libraries are widely used in asynchronous program-              a high-performance computer, this was primarily to enable
ming and self-referential data structures and have significant           parallel search and reduce runtime. For analyzing individual
influence on the Rust ecosystem. We initially performed a                libraries, the computational requirements are relatively low;
screening on crates.io with keywords including “pin”, “un-               an ordinary personal computer with lower computational re-
pin”, and “self-reference”. During the selection process, we             sources suffices.
followed these criteria:
1. Pure Rust Implementation. The selected libraries must                 5. E VALUATION R ESULTS
    be written in Rust, as our tool needs to extract MIR and             In this section, we analyze PinChecker’s detection results and
    transform it into RPIL for analysis.                                 performance to address RQ1–RQ3.
                          Table 3. Characteristics and pinning API usage patterns in evaluated Rust libraries.
                            # Pub Fn Definitions      # Unsafe Pin API calls   # Unsafe Lines      Unsafe
         Library                                                                                               All-time Downloads
                              / # Fn Definitions       + # Drop Trait Impls    / # Total Lines   Percentage
         moveit                    38 / 115                   26 + 6             407 / 1,211        33.61%                  741,454
         pin-init                   36 / 98                   17 + 5              101 / 880         11.48%                   23,625
         rio                        31 / 95                    0+7               187 / 2,143         8.71%                3,777,002
         pin-rc                     29 / 55                    3+0                 24 / 364          6.59%                    1,421
         owned-pin                 21 / 121                    5+2               154 / 1,030        14.95%                    9,406
         pin-queue                  20 / 49                    8+0                101 / 462         21.86%                    1,693
         pin-cell                   15 / 23                    2+0                 2 / 112           1.40%                   59,544
         recycle-box                11 / 46                    4+2                 81 / 491         16.50%                   28,414
         pin array                  9 / 22                     7+0                 11 / 199          5.53%                    2,822
         pinned vec                 8 / 24                     2+0                 2 / 202           0.99%                   11,797
         lazy-pinned                 7/8                      18 + 0               17 / 84          20.24%                    1,444
         pinus                      4 / 103                   26 + 2             564 / 1,185        47.59%                   12,993
         assert-unmoved             2 / 71                    11 + 1               12 / 619          1.72%                    7,100


    Table 4. PinChecker synthesis results for each crate.
        Library           Max. Length       # Synthesized               let mut v1 = Unmovable::new();
        moveit ⋆1               8              839,579∗                 let mut v2 = Box::pin(v1);
                                                                        let mut v3 = SlotDropper::new();
        pin-init                9           1,430,742,432               let mut v4 = &mut v3;
        rio ⋆2                  7              204,749∗                 let mut v5 = SlotDropper::new_unchecked_hygine_hack(v4);
        pin-rc                  9           1,033,101,237               let mut v6 = <_ as moveit::DerefMove>::deref_move(v2, v5);
                                                                        let mut v7 = &mut *v6;
        owned-pin               9            974,834,349                let mut v8 = mem::swap(v7, &mut Unmovable::new());
        pin-queue              10           12,710,367,475              ----------------------------------------------------------
        pin-cell                9           1,146,865,944               line 1: ;
                                                                        line 2: BIND(v2[1], v1); BORROW(v2, v2[1]); DEREF-PIN(v2);
        recycle-box             9           12,041,352,216              line 3: ;
        pin array               9           1,082,026,229               line 4: BORROW(v4, v3);
        pinned vec              9           1,566,995,155               line 5: BORROW(v5[1], (*v4)[1]);
                                                                        line 6: BORROW(v6[1], (*v2));
        lazy-pinned             9           10,666,622,602              line 7: BIND(v7, v6[1]);
        assert-unmoved          9           2,330,453,733               line 8: DEREF-MOVE(v7);
        ∗
          Exploration terminates upon finding the first bug-
          revealing program.
                                                                        Figure 11. Minimal violation program for moveit v0.5.1
               Table 5. Bugs caught by PinChecker.                      generated by PinChecker, with RPIL instructions for each line.
                             Min. Lines    Time to
    ⋆      Bug Type                                    Confirmed?
                             to Induce    Discovery
    ⋆1     Move-After-Pin             8        2.4s    Yes
    ⋆2     Pin-And-Leak               7        0.6s    Yes              the moveit library, where a value that has already been
                                                                        pinned is subsequently moved. The minimal violation program
                                                                        generated by the tool is shown in Figure 11. Through a
1. RQ1: Effectiveness in Detecting Pin Violations                       combination of eight function calls, the program gradually
To address RQ1, we evaluated PinChecker’s effectiveness in              bypasses Pin’s protection: First, line 2 creates Pin pointer
detecting pinning API contract violations in real-world Rust            v2, which pins its referent (v1), putting it in pinned state.
libraries. We selected a diverse set of libraries that are widely       Then, lines 3–6 construct intermediate variable v5, preparing
used and involve pinning APIs, as shown in Table 3. The                 parameters needed for line 6’s function call. Next, lines 6–7
dataset is sorted from the highest number of public function            transfer the reference relationship to v1 first into v6’s interior,
definitions to the lowest. All these libraries have significant         then extract it as v7. Finally, line 8 performs a memory move
numbers of downloads and exhibit high percentages of unsafe             on v7’s referent (v1) through mem::swap, causing it to enter
code. Even those with comparatively lower unsafe code per-              pinned_moved state, triggering a pin violation.
centages (less than 5%) primarily use unsafe pinning API calls          The vulnerability originates from the library function
within.                                                                 new_unchecked_hygine_hack, which exposes a means
We then executed PinChecker on each crate, with a maximum               of obtaining a mutable reference. After confirming the issue,
runtime limit of 10 hours per crate. Table 4 summarizes the             developers removed this function in v0.6.0.
detection results. The columns denote the library name, the             Bug ⋆2 is a second type of pin violation (Pin-And-Leak) in
maximum target synthesis length attempted, and the number of            the rio library, violating the Drop guarantee. The minimal
stub programs explored during synthesis. Libraries identified           violation program is shown in Figure 12. This issue arises from
with violations are marked with a ⋆ symbol.                             creating Pin pointers through rio::Completion struct’s
Table 5 presents a closer look at the bugs detected. We will            safe abstraction interface, then calling the standard library’s
discuss these bugs in detail below.                                     mem::forget to suppress drop execution. This vulnerability
Bug ⋆1 is a first type of pin violation (Move-after-Pin) in             can lead to use-after-free memory safety issues by accessing
                                                                                                            PinChecker (w/o lazy liveness check)                  PinChecker
let mut v1 = rio::new();
let mut v2 = io::Result::unwrap(v1);
                                                                                                                    100% relative time                          ~5% relative time
let mut v3 = &*v2;
let mut v4 = io::stdin();
let mut v5 = &v4;
let mut v6 = Default::default();                                                                           R1 (69.6%)                              R1 (86.3%)
let mut v7 = &v6;                                                                                          R2 (28.5%)                              R5 (11.2%)
let mut v8 = Default::default();                                                                           R5 (1.4%)                               R3 (2.5%)
let mut v9 = rio::Uring::read_at(v3, v5, v7, v8);                                                          R3 (0.3%)                               R2 (0.0%)
let mut v10 = &mut v9;                                                                                     R4 (0.3%)
let mut v11 = pin::Pin::new(v10);
let mut v12 = mem::forget(v9);



                              Figure 12. Minimal violation program for rio v0.9.4.                     Figure 14. Comparison between PinChecker variants’ rule composition.

                        104
Exploration Time (s)




                              PinChecker (without lazy liveness check)
                        102   PinChecker                                                                 Table 6. Expressiveness evaluation dataset composition.
                                                                                                          Crate Category              # Examples       # Linearizable          %
                        100
                                                                                                          Self-referential struct         15                 14              93%
                       10 2
                                                                                                          Async primitives                9                   8              89%
                              1            2             3               4       5        6   7   8       Pin-safe data structure         6                   5              83%
                                                                  Target Program Length
                                                                                                          Total                           30                 27              90%

Figure 13. Comparison between PinChecker variants’ average
exploration time. The candlestick beside each data point shows
the 25th and 75th percentiles.                                                                        let ret = moveit::new::by_raw(unsafe |space| {
                                                                                                        let space = Pin::into_inner_unchecked(space).as_mut_ptr();
                                                                                                      });

freed buffers while kernel I/O operations are incomplete. This
                                                                                                                 Figure 15. An example involving a closure parameter.
issue has been recorded in vulnerability exposure databases as
RUSTSEC-2020-0021 [20].
2. RQ2: Performance in Pin Violation Synthesis
                                                                                                      can represent real-world Pin API usage patterns. We studied
To address RQ2, we further examine PinChecker’s perfor-                                               usage examples for the crates in our evaluation from two
mance, comparing both PinChecker variants (Section 4.2),                                              sources: 1) dependent crates using the target crates (18 ex-
running each on all libraries. For each library, we instructed                                        amples), and 2) the target crates’ official documentation and
them to search for violation programs with target synthesis                                           test cases (12 examples). Table 6 shows the distribution across
lengths ranging from 1 up to 8, and we recorded the time                                              libraries. Under this criterion, we collected a total of 30 distinct
taken for exploration until termination. Figure 13 presents the                                       usage examples. For each example, our analysis procedure
experimental results, illustrating the mean exploration times                                         involved three steps: 1) we identify invocations of the crate’s
along with the 25th and 75th percentile bounds for each target                                        pin-related APIs, forming a self-contained API call sequence;
program length. The results reveal that the lazy liveness check                                       2) we rewrite each API call sequence in linear form while
variant of PinChecker consistently outperforms the monolith                                           maintaining their original semantics; 3) we verify semantic
variant, and the performance advantage increases as the target                                        equivalence through MIR comparison and manual inspection.
program length increases.
                                                                                                      Our analysis revealed that 90% (27 out of 30) of the real-world
We further instrumented the program to analyze how much
                                                                                                      Pin-related API use cases could be successfully expressed in
time is spent on each of the five constraint rules. Specifically,
                                                                                                      PinChecker’s linear form without compromising semantics.
we ran both PinChecker variants on each library with target
                                                                                                      The 3 cases that could not be adequately expressed in linear
length set to 5, collected instrumentation data, and calculated
                                                                                                      form all involved closure-based APIs. Figure 15 shows a
the average time spent on each rule. The results are shown
                                                                                                      characteristic failure case involving closure parameters. These
in Figure 14. With lazy liveness checking, PinChecker is able
                                                                                                      APIs require function pointer types as input parameters, which
to perform ∼19.1 times as fast as the version without lazy
                                                                                                      would necessitate extending our model to support multiple
liveness checking, needing only ∼5% of runtime. Moreover,
                                                                                                      function definitions rather than the current single-line program
given the same amount of execution time, with lazy liveness
                                                                                                      flow approach.
checking, PinChecker is able to allocate higher proportion of
computation (11.2% compared to 1.4%) to evaluating Rule 5,                                            These findings suggest that PinChecker’s approach to program
which is the core rule that PinChecker relies on to detect pin                                        synthesis, while constrained to linear form, remains suffi-
violations.                                                                                           ciently expressive to model and analyze the vast majority
                                                                                                      of real-world Pin API usage patterns. This expressiveness
3. RQ3: Expressiveness of Linear Programs                                                             validates our design decision to employ a simplified program
To address RQ3, we evaluate the effectiveness of PinChecker’s                                         representation that facilitates efficient constraint solving while
linear program synthesis approach by examining how well it                                            maintaining practical applicability to real-world code.
4. Limitations                                                      space. Similarly, Takashima et al. [26] presented SyRust,
While PinChecker effectively detects pin API contract viola-        a framework for automatically synthesizing well-typed Rust
tions, some limitations remain that suggest areas for future        programs to test unsafe library APIs. SyRust draws inspiration
enhancement.                                                        from H+ [27] and SyPet [28], and extends their approaches by
                                                                    encoding Rust’s ownership system type constraints into logical
1) Extending Safety Feature Coverage                                forms, guiding the program synthesis.
The current implementation of PinChecker focuses primarily          Logic Programming Based Program Synthesis. Kosarev
on the Pin mechanism. A natural extension would be to               et al. [29] explored a declarative approach using relational
broaden the analysis scope to cover more Rust safety issues         programming to synthesize implementations of pattern match-
related to unsafe code usage. We believe that extending             ing constructs. By representing both high-level semantics and
RPIL’s instruction set and enhancing the interpreter’s semantic     intermediate implementation language semantics relationally,
rules would enable more safety analyses.                            they enabled extensible synthesis of new language feature
                                                                    implementations. Byrd et al. [30] demonstrated how to write
2) Supporting Macro-based Abstractions                              relational interpreters in logic programming languages, en-
While PinChecker successfully analyzes function-level pin-          abling both program execution and synthesis from execution
ning API safety abstractions, some Rust libraries implement         traces. In the context of Rust, Dewey et al. [31] applied
pinning API abstractions through procedural macros. The code        constraint logic programming (CLP) to generate well-typed
generation nature of macro expansion introduces additional          programs, with a focus on testing the Rust type checker.
complexity to static analysis. We believe that incorporating
                                                                    7. C ONCLUSION
post-macro-expansion code analysis will offer a more com-
prehensive coverage.                                                We have presented PinChecker, an automatic detection tool for
                                                                    unsound safe abstractions of Rust’s unsafe pinning APIs. Our
3) Optimizing Analysis Performance                                  approach extracts function behaviors into a novel intermediate
While most crates achieve satisfactory results within accept-       representation, RPIL, which accurately models references and
able time for analysis, complex API functions with numerous         pinning state transitions. By employing a reversible interpreter
parameters and libraries with intricate interactions can be time-   implemented in Prolog, PinChecker is able to both emulate
consuming. Future work could explore more sophisticated con-        forward program execution and perform backward synthesis
straint solving techniques, such as state pruning mechanisms,       to generate minimal counterexample programs that trigger pin
to further enhance analysis efficiency.                             contract violations. Our evaluation on real-world Rust libraries
                                                                    demonstrates PinChecker’s ability to generate counterexample
6. R ELATED W ORK                                                   programs and find 2 confirmed issues. In future work we plan
This research intersects multiple domains including safe en-        to extend PinChecker’s support to a broader subset of Rust’s
capsulation of unsafe Rust code and constraint solving based        unsafe functionalities. We also plan to improve the scalability
program synthesis. In this section, we review the related work      of our constraint solving through more advanced constraint
and discuss their connection to our research.                       solving techniques.
Sound Usage of Unsafe Rust Code. Ensuring the soundness
                                                                    ACKNOWLEDGMENT
of safe abstractions over unsafe code is crucial for maintaining
Rust’s safety guarantees. Rao [21] proposed unsafety isolation      This work was supported in part by the National Natural Sci-
graphs to model the usage and encapsulation of unsafe code,         ence Foundation of China (NSFC) under Grant No. 62272220.
facilitating soundness checking of unsafe code encapsulation.
                                                                    R EFERENCES
Other research has investigated how to safely use existing
unsafe code. Liu et al. [22] presented XRust, which mitigates        [1] Rust Community, “Unsafe Rust - The Rust Programming
security threats from unsafe code by ensuring the integrity of           Language,” 2025.
data flow from unsafe Rust code to safe Rust code. Almohri           [2] C. Zhang, Y. Feng, Y. Zhang, Y. Dai, and B. Xu, “Beyond
and Evans [23] introduced Fidelius Charm to protect desig-               memory safety: an empirical study on bugs and fixes of
nated memory data from unauthorized access through unsafe                rust programs,” in 24th IEEE International Conference
libraries. Lamowski et al. [24] presents a sandboxing solution           on Software Quality, Reliability and Security, QRS 2024,
that isolates unsafe C library code in separate processes,               Cambridge, United Kingdom, July 1-5, 2024, pp. 272–
protecting the main Rust program from memory corruption                  283, IEEE, 2024.
in unsafe code.                                                      [3] Rust Community, “Rust’s Unsafe Code Guidelines Ref-
Constraint Solving Based Program Synthesis. Fiala et                     erence,” 2025.
al. [25] introduced RusSOL, a tool for synthesizing pro-             [4] Rust Community, “Safety comments - Standard library
grams that satisfy functional specifications while conforming            developers Guide,” 2025.
to Rust’s type system. Their approach leverages Synthetic            [5] Z. Rao, Y. Yang, and H. Xu, “Characterizing unsafe
Ownership Logic to derive programs that comply with Rust’s               code encapsulation in real-world rust systems,” CoRR,
type system, benefiting from the type system to reduce search            vol. abs/2406.07936, 2024.
 [6] R. Jung, H. Dang, J. Kang, and D. Dreyer, “Stacked bor-      [22] P. Liu, G. Zhao, and J. Huang, “Securing unsafe rust
     rows: an aliasing model for rust,” Proc. ACM Program.             programs with xrust,” in ICSE ’20: 42nd International
     Lang., vol. 4, no. POPL, pp. 41:1–41:32, 2020.                    Conference on Software Engineering, Seoul, South Ko-
 [7] B. Qin, Y. Chen, Z. Yu, L. Song, and Y. Zhang, “Under-            rea, 27 June - 19 July, 2020 (G. Rothermel and D. Bae,
     standing memory and thread safety practices and issues            eds.), pp. 234–245, ACM, 2020.
     in real-world rust programs,” in Proceedings of the 41st     [23] H. M. J. Almohri and D. Evans, “Fidelius charm: Iso-
     ACM SIGPLAN International Conference on Program-                  lating unsafe rust code,” in Proceedings of the Eighth
     ming Language Design and Implementation, PLDI 2020,               ACM Conference on Data and Application Security and
     London, UK, June 15-20, 2020 (A. F. Donaldson and                 Privacy, CODASPY 2018, Tempe, AZ, USA, March 19-
     E. Torlak, eds.), pp. 763–779, ACM, 2020.                         21, 2018 (Z. Zhao, G. Ahn, R. Krishnan, and G. Ghinita,
 [8] H. Xu, Z. Chen, M. Sun, and Y. Zhou, “Memory-safety               eds.), pp. 248–255, ACM, 2018.
     challenge considered solved? an empirical study with all     [24] B. Lamowski, C. Weinhold, A. Lackorzynski, and
     rust cves,” CoRR, vol. abs/2003.03296, 2020.                      H. Härtig, “Sandcrust: Automatic sandboxing of unsafe
 [9] V. Astrauskas, C. Matheja, F. Poli, P. Müller, and A. J.         components in rust,” in Proceedings of the 9th Workshop
     Summers, “How do programmers use unsafe rust?,” Proc.             on Programming Languages and Operating Systems,
     ACM Program. Lang., vol. 4, no. OOPSLA, pp. 136:1–                Shanghai, China, October 28, 2017 (J. Lawall, ed.),
     136:27, 2020.                                                     pp. 51–57, ACM, 2017.
[10] A. N. Evans, B. Campbell, and M. L. Soffa, “Is rust used     [25] J. Fiala, S. Itzhaky, P. Müller, N. Polikarpova, and
     safely by software developers?,” in ICSE ’20: 42nd In-            I. Sergey, “Leveraging rust types for program synthesis,”
     ternational Conference on Software Engineering, Seoul,            Proc. ACM Program. Lang., vol. 7, no. PLDI, pp. 1414–
     South Korea, 27 June - 19 July, 2020 (G. Rothermel and            1437, 2023.
     D. Bae, eds.), pp. 246–257, ACM, 2020.                       [26] Y. Takashima, R. Martins, L. Jia, and C. S. Pasareanu,
[11] Rust Community, “Rust standard library documentation              “Syrust: automatic testing of rust libraries with semantic-
     for std::pin,” 2025.                                              aware program synthesis,” in PLDI ’21: 42nd ACM
[12] Rust Community, “Rust standard library documentation              SIGPLAN International Conference on Programming
     for std::pin::Pin,” 2025.                                         Language Design and Implementation, Virtual Event,
[13] C. Csallner and Y. Smaragdakis, “Jcrasher: an automatic           Canada, June 20-25, 2021 (S. N. Freund and E. Yahav,
     robustness tester for java,” Softw. Pract. Exp., vol. 34,         eds.), pp. 899–913, ACM, 2021.
     no. 11, pp. 1025–1050, 2004.                                 [27] Z. Guo, M. James, D. Justo, J. Zhou, Z. Wang, R. Jhala,
[14] C. Pacheco, S. K. Lahiri, M. D. Ernst, and T. Ball,               and N. Polikarpova, “Program synthesis by type-guided
     “Feedback-directed random test generation,” in 29th In-           abstraction refinement,” Proc. ACM Program. Lang.,
     ternational Conference on Software Engineering (ICSE              vol. 4, no. POPL, pp. 12:1–12:28, 2020.
     2007), Minneapolis, MN, USA, May 20-26, 2007, pp. 75–        [28] Y. Feng, R. Martins, Y. Wang, I. Dillig, and T. W.
     84, IEEE Computer Society, 2007.                                  Reps, “Component-based synthesis for complex apis,”
[15] V. Atlidakis, P. Godefroid, and M. Polishchuk, “Restler:          in Proceedings of the 44th ACM SIGPLAN Symposium
     stateful REST API fuzzing,” in Proceedings of the 41st            on Principles of Programming Languages, POPL 2017,
     International Conference on Software Engineering, ICSE            Paris, France, January 18-20, 2017 (G. Castagna and
     2019, Montreal, QC, Canada, May 25-31, 2019 (J. M.                A. D. Gordon, eds.), pp. 599–612, ACM, 2017.
     Atlee, T. Bultan, and J. Whittle, eds.), pp. 748–758, IEEE   [29] D. Kosarev, P. Lozov, and D. Boulytchev, “Relational
     / ACM, 2019.                                                      synthesis for pattern matching,” in Programming Lan-
[16] Rust Community, “The MIR (Mid-level IR) - Rust Com-               guages and Systems - 18th Asian Symposium, APLAS
     piler Development Guide,” 2025.                                   2020, Fukuoka, Japan, November 30 - December 2,
[17] Rust Community, “Miri: An interpreter for Rust’s mid-             2020, Proceedings (B. C. d. S. Oliveira, ed.), vol. 12470
     level intermediate representation,” 2025.                         of Lecture Notes in Computer Science, pp. 293–310,
[18] Rust Community, “cargo 1.86.0: The Cargo Book,” 2025.             Springer, 2020.
[19] RISE Research Institutes of Sweden AB, “SICStus Pro-         [30] W. E. Byrd, A. Ballantyne, G. Rosenblatt, and M. Might,
     log: Leading Prolog Technology,” 2024.                            “A unified approach to solving seven programming prob-
[20] Rust Secure Code Working Group, “rio allows a use-                lems (functional pearl),” Proc. ACM Program. Lang.,
     after-free buffer access when a future is leaked,” 2020.          vol. 1, no. ICFP, pp. 8:1–8:26, 2017.
[21] Z. Rao, “Semi-automated verification of interior unsafe      [31] K. Dewey, J. Roesch, and B. Hardekopf, “Fuzzing the
     code encapsulation in real-world rust systems,” in Pro-           rust typechecker using CLP (T),” in 30th IEEE/ACM
     ceedings of the 39th IEEE/ACM International Confer-               International Conference on Automated Software Engi-
     ence on Automated Software Engineering, ASE 2024,                 neering, ASE 2015, Lincoln, NE, USA, November 9-13,
     Sacramento, CA, USA, October 27 - November 1, 2024                2015 (M. B. Cohen, L. Grunske, and M. Whalen, eds.),
     (V. Filkov, B. Ray, and M. Zhou, eds.), pp. 2435–2437,            pp. 482–493, IEEE Computer Society, 2015.
     ACM, 2024.
