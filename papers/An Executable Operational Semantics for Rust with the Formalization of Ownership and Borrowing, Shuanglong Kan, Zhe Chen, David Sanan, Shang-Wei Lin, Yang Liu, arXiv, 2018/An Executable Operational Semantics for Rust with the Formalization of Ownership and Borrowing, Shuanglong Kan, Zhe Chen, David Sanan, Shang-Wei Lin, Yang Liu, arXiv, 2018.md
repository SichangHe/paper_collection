                                                                                                                                                                 1

                                         An Executable Operational Semantics for Rust with the
                                         Formalization of Ownership and Borrowing

                                         SHUANGLONG KAN, TU Kaiserslautern, Germany
                                         ZHE CHEN, NUAA, China
arXiv:1804.07608v2 [cs.PL] 24 Jul 2020




                                         DAVID SANÁN, NTU, Singapore
                                         SHANG-WEI LIN, NTU, Singapore
                                         YANG LIU, NTU, Singapore
                                         Rust is an emergent systems programming language highlighting memory safety by its Ownership and
                                         Borrowing System (OBS). The existing formal semantics for Rust only covers limited subsets of the major
                                         language features of Rust. Moreover, they formalize OBS as type systems at the language-level, which can
                                         only be used to conservatively analyze programs against the OBS invariants at compile-time. That is, they are
                                         not executable, and thus cannot be used for automated verification of runtime behavior.
                                            In this paper, we propose RustSEM, a new executable operational semantics for Rust. RustSEM covers a
                                         much larger subset of the major language features than existing semantics. Moreover, RustSEM provides
                                         an operational semantics for OBS at the memory-level, which can be used to verify the runtime behavior
                                         of Rust programs against the OBS invariants. We have implemented RustSEM in the executable semantics
                                         modeling tool K-Framework. We have evaluated the semantics correctness of RustSEM wrt. the Rust compiler
                                         using around 700 tests. In particular, we have proposed a new technique for testing semantic consistency
                                         to ensure the absence of semantic ambiguities on all possible execution selections. We have also evaluated
                                         the potential applications of RustSEM in automated runtime and formal verification for both functional and
                                         memory properties. Experimental results show that RustSEM can enhance the memory safety mechanism of
                                         Rust, as it is more powerful than OBS in detecting memory errors.

                                         Additional Key Words and Phrases: Rust, Operational Semantics, Ownership, Borrowing

                                         ACKNOWLEDGMENTS
                                         This material is based upon work supported by the National Science Foundation under Grant
                                         No. nnnnnnn and Grant No. mmmmmmm. Any opinions, findings, and conclusions or recommen-
                                         dations expressed in this material are those of the author and do not necessarily reflect the views
                                         of the National Science Foundation.

                                         1   INTRODUCTION
                                         Developing a formal semantics for a programming language could provide a mathematical founda-
                                         tion for the language. The semantics can be used as a reference model, and more importantly, used
                                         for proving language-level properties and constructing automated verification tools.
                                            Rust [Rust-Team 2016] is an emergent systems programming language aiming at providing
                                         memory safety guarantees with its Ownership and Borrowing System (OBS). One of the most
                                         important guarantees maintained by the OBS invariants is the exclusive mutation capability for
                                         memory locations, which can avoid a variety of memory errors such as dangling pointers and data
                                         races.

                                         Authors’ addresses: Shuanglong Kan, Department of Computer Science, TU Kaiserslautern, Germany, kanshuanglong@
                                         outlook.com; Zhe Chen, College of Compute Science and Technology, NUAA, China; David Sanán, NTU, Singapore;
                                         Shang-wei Lin, NTU, Singapore; Yang Liu, NTU, Singapore.


                                         2018. 2475-1421/2018/1-ART1 $15.00
                                         https://doi.org/


                                                                        Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:2                                             Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


   Several formal semantics for Rust has been developed. Unfortunately, they only cover limited
subsets of the major language features of Rust, and most of them formalize either a variant or an
outdated version of Rust. For instance, Patina [Reed 2015] only captures the key features related to
memory safety, e.g., unique pointers and references, in an early version of Rust. RustBelt [Jung
et al. 2018a] formalizes a variant λ Rust of Rust in Coq, to prove in Coq that the type system of Rust
can guarantee the memory and thread safe of λ Rust programs.
   Furthermore, most of the existing semantics for Rust is not executable, and thus cannot be used
for automated verification of runtime behavior. For instance, Patina [Reed 2015] and RustBelt
[Jung et al. 2018a] formalize OBS as type systems at the language-level, which can only be used to
conservatively analyze programs against the OBS invariants at compile-time. But this may reject
some execution traces satisfying the OBS invariants. As a result, automated verification tools for
Rust have to translate programs into the input languages of general-purpose verifiers, which may
hurt expressiveness and make potential verification optimizations impossible. For instance, Prusti
[Astrauskas et al. 2019] translates a subset of safe constructs into the input language of Viper
[Müller et al. 2016]. To support direct verification of Rust programs, a new executable semantics
should be developed for automated verification.
   In this paper, we propose RustSEM, a new executable operational semantics for Rust. RustSEM
consists of three levels:
      (1) A sequential consistency memory model, which defines the memory layout of stacks and
          heaps, and a collection memory operations. More importantly, we formalize an operational
          semantics of OBS in the memory model for dynamically checking the OBS invariants. Unlike
          the existing semantics of OBS, which is formalized as type systems at the language-level and
          bound to a specific language, our semantics is language-independent and thus can be reused
          for other languages since most languages have similar memory operations. Moreover, we
          also propose a high-level abstraction of OBS and prove the refinement relation between the
          abstraction and the memory model, ensuring the semantics correctness of the OBS refinement.
      (2) An operational semantics for the Core Language (CL), an intermediate representation (IR) for
          reducing redundant semantics definitions. Recall that Rust also has an IR, namely Mid-level
          Intermediate Representation (MIR) [Matsakis 2016]. But the gap between Rust and CL is
          much smaller than MIR, facilitating the translation semantics from Rust to CL.
      (3) A translation semantics from Rust to CL, which automatically translates Rust programs into
          the corresponding CL programs.
To execute a Rust program, RustSEM first translates the program into a CL program, and then
executes the CL program wrt. the CL semantics, in which all memory accesses are carried out by
invoking the interfaces of the memory model.
   RustSEM distinguishes from the existing semantics in the following aspects.
   Firstly, RustSEM directly formalizes Rust, instead of a variant, and covers a much larger subset
of the major language features than existing semantics. For instance, RustSEM supports both safe
and unsafe constructs, concurrency, dynamic OBS, closures, pattern matching and polymorphism.
   Secondly, RustSEM provides an operational semantics for OBS at the memory-level, whilst other
existing semantics formalizes OBS as type systems at the language-level. The operational semantics
of OBS is useful in two aspects. (1) It can be used to verify the runtime behavior of Rust programs
against the OBS invariants, i.e., reject the programs violating the OBS invariants. Compared with
the type systems, it provides a more flexible OBS invariant checking that accepts a larger set of
correct programs. (2) It can be used to detect undefined behavior of the programs mixing safe and
unsafe operations, by noting that unsafe constructs can escape from OBS and make programs prone
to bugs [Davidoff 2018].

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                    1:3


   Thirdly, RustSEM is an executable semantics, which means that RustSEM can execute a Rust
program with respect to its semantics. We have implemented RustSEM in the executable semantics
modeling tool K-Framework (K) [Roşu and Şerbănuţă 2010]. K is based on rewriting-logic and has
a builtin parser that enables the semantics being defined on the abstract syntax tree. K has been
successfully applied in formalizing the semantics of real-world programming languages, such as
Java [Bogdănaş and Roşu 2015] and C [Ellison and Rosu 2012; Hathhorn et al. 2015]. K’s execution
and verification engines enable testing RustSEM and constructing automated verifiers.
   We have evaluated the semantics correctness of RustSEM wrt. the Rust compiler using around
700 tests for the three levels, which mainly come from the Rust benchmarks [Rust-Benchmark
2020], the Rust libraries and the Rust text book [Rust-Team 2018]. Note that two semantics rules
sometimes can be applied to the same construct at the same time, causing semantic ambiguities.
Although one of them should be avoided, the execution engine of K always selects one rule to
execute, leaving such ambiguities undetected. Thus, we have proposed a new technique for testing
semantic consistency to ensure the absence of semantic ambiguities on all possible execution
selections, by exploiting the verification engine of K. Our new technique has discovered more than
36 semantic ambiguities. We also created tests for investigating what kinds of programs are rejected
by the Rust compiler but accepted by RustSEM due to the compiler’s conservation, and the reverse
due to mixed safe and unsafe operations.
   We have also evaluated the potential applications of RustSEM in automated runtime and formal
verification for both functional and memory properties. Runtime verification with RustSEM is
evaluated on 118 programs for detecting memory errors. Formal verification with RustSEM is
evaluated on a collection of benchmarks, including Vec_Deque in the Rust library implementing a
ring buffer. Experimental results show that RustSEM can enhance the memory safety mechanism
of Rust, as it is more powerful than OBS in detecting memory errors.
   In summary, we make the following contributions:
    (1) We propose a new executable operational semantics for Rust that supports a larger subset of
        the major language features, compared with all existing works.
    (2) We propose a high-level abstraction of OBS and an operational semantics of OBS in the
        memory model. We also prove the refinement relation between them.
    (3) We formalize the semantics of unsafe pointers and the semantics of the executions mixing
        both safe and unsafe pointers.
    (4) We propose a novel testing technique based on K’s verification engine to detect semantic
        ambiguities.
    (5) We show that RustSEM can be applied to both runtime and formal verification against both
        functional and memory properties.
   This paper is organized as follows: Section 2 recalls the OBS of Rust. Section 3 presents a high-
level abstraction of OBS. Section 4 defines the operational semantics of the memory model, while
Section 5 presents the basic idea of the semantics of CL and the translation semantics for Rust.
Section 6 evaluates the proposed semantics. Section 7 compares related work. Section 8 concludes.

2     OWNERSHIP AND BORROWING SYSTEM
In this section, we recall the OBS of Rust and the related OBS invariants.

2.1    Ownership
A variable can declare the unique ownership of a memory block using a binding or an assignment.
If the ownership is declared as mutable with the mut keyword, then the owner can be used to both
read and write the block, otherwise it is read-only. A read-only (resp. mutable) owner is called

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:4                                             Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


a shared (resp. mutable) alias of the block. We denote by x →o B that variable x is the owner of
block B, i.e., x owns B. For instance, in Listing 1, the binding “let mut v = vec![1,2]" at Line 1.1
first allocates a block B in the memory to store the vector [1,2], and then the owner v obtains the
ownership of B, denoted by v →o B.
                                                      An ownership can be moved from one variable to
                        Listing 1.                 another. Moving an ownership from variable x to
1.1 let mut v = vec![1,2];                         another variable y means that the ownership now
1.2 {                                      v       belongs to y and x no longer owns it. For instance,
1.3      let v1 = v;                               in Listing 1, the binding “let v1 = v” at Line 1.3
1.4      let t = v1[0];                            moves the ownership of the vector from v to v1, i.e.,
                                   v1
1.5      v1[1] = 3;                                v1 becomes the new owner of the vector and v can
1.6 }                                              no longer be used to access it. Indeed, the vector
                                                   is read and written through v1 at Lines 1.4 and 1.5,
                                                   respectively.
   The lifetime of an owner begins from the timestamp at which it obtains the ownership and ends
at the timestamp at which it loses the ownership, e.g., when the ownership is moved or it goes out
of the program scope (i.e., curly braces). Timestamps are a way to distinguish the execution order
of program statements. In this section, we use line numbers as timestamps. The block is deallocated
through its owner when the owner goes out of scope. For instance, in Listing 1, the lifetime of
owner v begins at Line 1.1 and ends at Line 1.3, whilst the lifetime of owner v1 begins at Line 1.3
and ends at Line 1.6. The vector is deallocated through v1 at Line 1.6 as v1 goes out of scope.

2.2   Borrowing and Reborrowing
Borrowing is a way to create references to the owner of a memory block. There are two kinds
of references: shared references (read-only, created by &) and mutable references (readable and
writable, created by &mut). A shared (resp. mutable) reference is also called a shared (resp. mutable)
alias of the block. A borrowing creating a shared (resp. mutable) reference is called a shared (resp.
mutable) borrowing. We denote by x →s y (resp. x →m y) that x is a shared (resp. mutable)
reference to y, i.e., x borrows y. For instance, in Listing 2, the borrowing “let b1 = &v1" at Line
2.3 creates a shared reference b1 to v1, denoted by b1 →s v1, where b1 can only be used to read the
block owned by v1. The borrowing “let b2 = &mut v2" at Line 2.4 creates a mutable reference,
denoted by b2 →m v2, where b2 can be used to both read and write the block owned by v2.

                          Listing 2.                                                     Listing 3.
2.1 let v1 = vec![1,2];                                        3.1 let mut v = vec![1,2];
2.2 let mut v2 = vec![1,2];                                    3.2 let b1=&mut v;
2.3 let b1=&v1;                                                3.3 let b2=&(*b1);
                                                                                    b1 →m v
2.4 let b2=&mut v2;                                            3.4 let z=(*b2)[0];
                     b1 →s v1
2.5 let t1=(*b1)[0];                                           3.5 (*b1)[0] = 2;
                                                b2 →m v2                                    b2 →s b1
2.6 let t2=(*b1)[1];                                               /*b1 should be
2.7 (*b2)[1] = 2;                                                  disabled by b2*/
                                                               3.6 let t = (*b2)[1];

  Reborrowing is a way to create references from another reference, instead of an owner. For
instance, in Listing 3, b1 borrows the owner v at Line 3.2 and b2 reborrows b1 with the referent
∗b1 at Line 3.3, denoted by the link b2 →s b1 →m v. To access the first element of the vector, we
can use v[0], (*b1)[0] or (*b2)[0], where v, *b1 and *b2 are three paths to access the vector.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                    1:5


Each path uses an alias as the entry to access the block. For instance, the paths v, *b1 and *b2 use
the alias entries v, b1 and b2, respectively.
  As borrowing and reborrowing are similar, we define unified relations for them.
   Definition 2.1 (Unified borrowing relation). Let x and y be two variables, where y can be either
an owner or a reference. x borrows or reborrows y is denoted by x →b y. The borrowing relation
→b contains two sub-relations: shared borrowing →s and mutable borrowing →m , i.e., x →b y ⇔
(x →s y) ∨ (x →m y).
   The lifetime of a reference begins from the timestamp of its creation and ends at the last timestamp
at which it is used (read, written, or borrowed), according to the definition of Non-Lexical Lifetimes
(NLL) [Rust-Team 2018]. Unlike the lifetime of owner, which can be easily decided by the program
scope, the lifetime of reference is decided by the last use of it. For instance, in Listing 2, the lifetime
of b1 is from Line 2.3 to 2.6, while the lifetime of b2 is from Line 2.4 to 2.7.

2.3   The OBS Invariants
Because a memory block can be accessed by multiple aliases, OBS should fulfill the following OBS
guarantees in order to avoid memory errors.
    • Each alias only accesses (reads or writes) one valid block. For owners, they should own the
      block. For references, their owners should be in their lifetimes to ensure validity.
    • At any time in an execution, each block can be accessed by either multiple shared aliases
      (but no mutable alias) or exclusively accessed by a unique mutable alias.
  In order to meet these two guarantees, OBS maintains the following invariants. We will prove
that these invariants exactly ensure the guarantees in Section 3.
  Definition 2.2 (The OBS invariants). The following invariants must be satisfied:
  (1) Unique owner invariant: Each block has a unique owner.
  (2) Lifetime inclusion invariant: If x →b y then the lifetime of x should always be within the
      lifetime of y in order to avoid dangling pointers.
  (3) Lifetime disjoint invariant: There are no two references to the same referent such that their
      lifetimes intersect and one of them is a mutable reference.
  (4) Writing permission invariant: If x →s y then the writing permission of y should be disabled
      until the end of x’s lifetime.
  (5) Reading and writing permission invariant: If x →m y then both the reading and writing
      permissions of y should be disabled until the end of x’s lifetime.
   We now illustrate the above invariants by examples. The unique owner invariant is obvious. The
move operation preserves the invariant. Listing 4 violates Invariant (2). The lifetime of owner v is
from Line 4.3 to 4.6 and the lifetime of reference b is from Line 4.4 to 4.7. Therefore the reference’s
lifetime is not within the owner’s lifetime.

                         Listing 4.                                                 Listing 5.
 4.1 let mut b;                                               struct PT{x:i32,y:i32}
 4.2 {                                                    5.1 let mut v=PT{x:1,y:2};
 4.3   let mut v = vec![1,2];                             5.2 let b1=&v;
 4.4   b = & mut v;                                       5.3 let b2=&mut(v.x); b1 →s v
                                                 v
 4.5   let t = (*b)[1];                                   5.4 let t=(*b1).x;            b2 →m v.x
                        b →s v
 4.6 }                                                    5.5 (*b2) = 2;
 4.7 (*b)[1] = 2;


                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:6                                             Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


   Listing 5 violates Invariant (3). It is a more interesting example as b2 borrows the field x of v
instead of v. Rust also enables fine-grained borrowings for struct types. Let ST be a struct type
with fields d 1 , . . . , dn and x be the owner of a block of the type ST. We can create borrowings
for both x (e.g. y →b x) and the fields of x (e.g. y →b x.di ) . The relation between them is:
y →b x ⇒ y →b x.d 1 ∧ . . . ∧ y →b x.dn . This means that if x is borrowed then all its fields are
borrowed. It also means that an alias can not only be a variable but also be fields of variables.
Moreover, a block could be divided into “sub-blocks” corresponding fields. The lifetime of b1 →b v
is from Line 5.2 to 5.4. We can also infer that b1 →s v.x from b1 →s v. The lifetime of b2 →m v.x
is from Line 5.3 to 5.5. The intersection of the lifetimes of b1 →s v.x and b2 →m v.x is not empty
and one of them is a mutable reference. Listing 3 violates Invariant (4). The lifetime of shared
reference b2 is from Line 3.3 to 3.6. Since b2 reborrows b1, b1’s writing permission should be
disabled within the lifetime of b2. Thus, the writing through b1 at Line 3.5 is illegal.
   Both owners and references are safe pointers. But Rust also supports raw pointers, which are
unsafe pointers that can escape from OBS checking. We formalize raw pointers in the memory
model in Section 4. Besides raw pointers, Rust also has other unsafe features including unsafe
scopes and unsafe functions, which are statement scopes and functions wherein raw pointers are
read or written. We model these unsafe features in CL and the translation semantics in Section 5.

3      HIGH-LEVEL ABSTRACTION OF OBS
This section presents a high-level formalization of OBS by graphs, in which we only focus on the
ownership and borrowing relations among aliases and blocks. At the end of this section, we prove
that the OBS invariants exactly ensure the OBS guarantees.
    Definition 3.1 (Lifetimes). Let Tim be an infinitely countable set of timestamps. (Tim, ≤) is a
totally ordered set. A strict order < over Tim is defined as t < t ′ iff t ≤ t ′ ∧ t , t ′. The function
Su : Tim → Tim is the successor function of timestamps, such that Su(t) = t ′ iff t < t ′ ∧ ∄t ′′ .t <
t ′′ < t ′. A lifetime t 1 ∼ t 2 (where t 1 , t 2 ∈ Tim), defined as {t | t 1 ≤ t ≤ t 2 }, is a subset of Tim.
  Let LT denotes the set of all lifetimes. Because a lifetime is a set of timestamps, we can use set
operations on lifetimes.
  Blocks, aliases, and their relations constitute an OBS graph, defined as follows:
      Definition 3.2 (OBS graph of a block). An OBS graph is defined as G = (B, V , E, F ), where
       • B is a memory block,
       • V is a set of aliases of B, e.g., owners and references,
       • E : V → {o, s, m} × ({B} ∪V ) is a set of edges, i.e., a total mapping from aliases to the product
         of {o, m, s} and {B} ∪ V . E(a) = (o, B) iff a →o B, i.e. a owns B. E(a) = (s, a ′) iff a →s a ′, i.e.,
         a is a shared reference to a ′. E(a) = (m, a ′) iff a →m a ′, i.e., a is a mutable reference to a ′.
       • F : E → LT is the lifetimes of edges.
   Note that E is a total mapping as each alias holds exactly one value. In the sequel, E(a) = (∗, a ′)
and (a →∗ a ′) ∈ E are used interchangeably, where ∗ ∈ {o, s, m}. We also inherit the notation →b
in Section 2 to denote either →m or →s . Fig. 1 is an example of OBS graphs. On the left is a Rust
program and right is its two OBS graphs, in which one is for B and another one is for B.0. The
symbol B denotes the block that stores the vector PT{x:1,y:2} and B.0 is the offset storing the
value of the field x and is a sub-block of B.
   We first explain the OBS graph for B. In the graph, an edge is labeled by the mutability of the
borrowing and its lifetime. For instance, the edge from b2 to b1 is labeled by s[3-4], it denotes
b2 →s b1 and F (b2 →s b1) = {3, 4}. The notation [3-4] denotes the range from 3 to 4. The second

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                    1:7


    struct PT {x:i32,y:i32}                                           s[3-4]        m[2-5]         o[1-7]
                                                                 b2            b1             v             B
  1 let mut v = PT{x:1,y:2};
  2 let b1 = & mut v;
  3 let b2 = & (* b1);                                                s[3-4]
                       b2 →s b1 b1 →m v                          b2            b1    m[2-5]
  4 let z = (*b2).x;                                                                               o[1-7]
  5 (*b1).y = 2;                                                                             v.x            B.0
  6 let b3 = &mut (v.x);                                                       b3    m[6-7]
                          b3 →m v.x
  7 (*b3) = 3;


                                      Fig. 1. An example of OBG graphs


OBS graph of B.0 is for the field x, since b3 directly borrows v.x. The dashed arrow in the OBS
graph is inferred from the borrowing b1 →m v.
  To formalize the OBS invariants (1), (2) and (3), we define well-formedness for OBS graphs.
   Definition 3.3 (Well-formed OBS graphs). Let G = (V , B, E, F ) be an OBS graph. It is well-formed
if and only if it satisfies
  (1) There is a unique a ∈ V such that E(a) = (o, B).
  (2) ∀a, a ′, a ′′ ∈ V ∪ {B}. E(a) = (∗, a ′) ∧ E(a ′) = (∗, a ′′) =⇒ F (a →∗ a ′) ⊂ F (a ′ →∗ a ′′).
  (3) ∀a, a ′, a ′′ ∈ V . E(a ′) = (b, a) ∧ E(a ′′) = (m, a) =⇒ F (a ′ →b a) ∩ F (a ′′ →m a) = ∅.
  In Fig. 1, the two OBS graphs are well-formed. For instance, the block B.0 is uniquely pointed by
v.x. The lifetime of b2 →s b1 is within the lifetime of b1 →m v.x. The lifetimes of b1 →m v.x and
b3 →m v.x do not intersect. One important property for the well-formed OBS graphs is acyclic.
The proof is in Appendix A.
  Lemma 3.4. A well-formed OBS graph is acyclic.
  To formalize the OBS invariants (4) and (5), we define reading and writing permission functions.
An alias is permitted to read or write at a specific timestamp if the reading or writing permission
function returns true, respectively.
   Definition 3.5 (Permission functions). Let G = (B, V , E, F ) be an OBS graph. The reading permis-
sion function RG : V × Tim → B is defined as
                     true if (∃a ′ .a →∗ a ′ ∈ E ∧ t ∈ F (a →∗ a ′)) ∧ (∄a ′′ .t ∈ F (a ′′ →m a))
                   
      RG (a, t) =
                     false otherwise
where the condition t ∈ F (a →∗ a ′) denotes that t is in the lifetime of the relation. Note that the
condition ∄a ′′ .t ∈ F (a ′′ →m a) ensures that a’s reading permission is not disabled at t.
  The writing permission function WG : V × Tim → B is defined as
                  true if (∃a ′ .a → {o,m } a ′ ∈ E ∧ t ∈ F (a → {o,m } a ′)) ∧ (∄a ′′ .t ∈ F (a ′′ →b a))
             
 WG (a, t) =
                  false otherwise
where a → {o,m } a ′ denotes a →o a ′ or a →m a ′.
   In Fig. 1, at timestamp 3, WG (b1, 3) = false as there exists b2 such that 3 ∈ F (b2 →s b1). At
timestamp 7, RG (b3, 7) = true as 7 ∈ F (b3 →m v.x) and ∄a ′ .a ′ →b b3 ∈ E.
   In the following theorem, we show that a well-formed OBS graph satisfies exclusive mutation
guarantee with respect to the permission functions. The proof is in Appendix B.

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:8                                           Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


  Theorem 3.6. Let G = (V , B, E, F ) be an OBS graph and t be a timestamp. If G is well-formed then
we have either (1) ∀a ∈ V ,WG (a, t) = false or (2) ∃!a ∈ V ,WG (a, t) = true∧(∀a ′ .a , a ′ ⇒ RG (a ′, t) =
WG (a ′, t) = false). The notation ∃! denotes unique existential quantification.

    Theorem 3.6 shows that for a block or a sub-block, if all readings or writings by the aliases in its
OBG graph are executed at the timestamps that the corresponding permission functions return
true then the readings and writings respect exclusive mutation guarantee.
    Compared with the OBS of Rust compiler, our formalization relaxes some restrictions. For
instance, in Rust compiler, an alias a could write a block owned by a ′ if all the borrowings in the
path from a to a ′ in the OBS graph are all mutable borrowings and a ′ is declared as mutable. In
the high-level abstraction, we have no such restriction. But in the memory model (Section 4) of
RustSEM, we still respect this restriction.
    In Rust, there is another definition of the lifetimes for references, called two-phase borrowing
[Matsakis 2017], in which the lifetime of a mutable reference is from the timestamp that we start to
use it instead of the timestamp that it is created. Our high-level abstraction is also compatible with
it. We only need to reconsider the lifetimes of references, For instance, in Fig. 1 F (b3 →m v.x) is
{7} now. Definition 3.3 and 3.5 keep unchanged and Theorem 3.6 is still true.

4     MEMORY MODEL
In this section, we introduce our memory model, which is the core of RustSEM that formalizes
OBS. The memory model supports the dynamic checking of OBS invariants. It can be viewed as an
implementation or a refinement of the high-level abstraction of OBS. Moreover, it also supports
sequential consistency checking for concurrent access.
   We first illustrate our basic idea, especially the dynamic lifetime extension, with a motivation
example in Fig. 2. There are 7 lines of code in the figure. Line 1 creates a block B for vec![1,2],
whose address is b. The symbol v 7→ own(b) means that the variable v starts to own the block b. It
denotes v →o B. The value own(b) indicates that the ownership of B belongs to v. Line 2 creates a
borrowing relation b1 →m v. We introduce mut(2 ∼ 2, v) as a value to denote a reference value to v
in the memory model, where 2 ∼ 2 is a timestamp span from Line 2 to 2 in which b1 is used, since
we only scan the code to Line 2 until now. When we scan Line 3, b1 is used to write the vector, the
timestamp span of the reference b1 should be extended since it is used here. The new span is 2 ∼ 3.
This treatment for lifetimes is called the dynamic lifetime extension. Line 4 writes the vector by its
owner v. Note that b1 does not disable v here since its lifetime is not extended to Line 4. Line 5
creates a relation b2 →s v. We introduce the value shr(5 ∼ 5, v) to denote a shared reference value
to v, whose lifetime is from Line 5 to 5 at the moment. Line 6 writes the vector by its owner, this is
allowed at the moment since the existing two references cannot disabled it until now. But at Line 7,
since b2 is used to read, the lifetime of the reference b2 should be extended to 7. Now, an error
arises, i.e, the writing at Line 6 is within the lifetime of the shared reference, thus it is illegal.
   From the motivation example,
in order to support dynamic OBS 1 let mut v=vec![1,2]; v 7! own(b)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




invariant checking without look-
ing backward, we select to store 2 let b1 = & mut v;             b1 7! mut(2 ⇠ 2, v)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="gRjAgPc7KYIb10S8zYN5gxE0rYA=">AAAB7XicbZC7SgNBFIbPeo3xFi+dzWAQrMJuLLQzYKFlBHOBJITZyWwyZi7LzKwQl7yDjYUitnZWPomdpW/i5FJo4g8DH/9/DnPOCWPOjPX9L29hcWl5ZTWzll3f2Nzazu3sVo1KNKEVorjS9RAbypmkFcssp/VYUyxCTmth/2KU1+6oNkzJGzuIaUvgrmQRI9g6q1psGiaK7VzeL/hjoXkIppA//7j/vnzfT8vt3Gezo0giqLSEY2MagR/bVoq1ZYTTYbaZGBpj0sdd2nAosaCmlY6nHaIj53RQpLR70qKx+7sjxcKYgQhdpcC2Z2azkflf1khsdNZKmYwTSyWZfBQlHFmFRqujDtOUWD5wgIlmblZEelhjYt2Bsu4IwezK81AtFoKTQnAd5Es+TJSBAziEYwjgFEpwBWWoAIFbeIAnePaU9+i9eK+T0gVv2rMHf+S9/QAjhpJ/</latexit>




lifetimes for references. Moreover, 3 (*b1)[0] = 2;              b1 7! mut(2 ⇠ 3, v), b1 is used for writing at 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               <latexit sha1_base64="uDXTcT/AVSF9qlDNC8bjm6yV4oA=">AAAB7nicbZC7SgNBFIbPxluMt3jpbAaDYBV2kyJ2Biy0jGAukCxhdjKbDJmZXWZmhbjkIWwsFLG1svJJ7Cx9EyeXQhN/GPj4/3OYc04Qc6aN6345mZXVtfWN7GZua3tndy+/f9DQUaIIrZOIR6oVYE05k7RumOG0FSuKRcBpMxheTvLmHVWaRfLWjGLqC9yXLGQEG2s1Sx3NBCp38wW36E6FlsGbQ+Hi4/776v0orXXzn51eRBJBpSEca9323Nj4KVaGEU7HuU6iaYzJEPdp26LEgmo/nY47RqfW6aEwUvZJg6bu744UC61HIrCVApuBXswm5n9ZOzHhuZ8yGSeGSjL7KEw4MhGa7I56TFFi+MgCJorZWREZYIWJsRfK2SN4iysvQ6NU9MpF78YrVF2YKQvHcAJn4EEFqnANNagDgSE8wBM8O7Hz6Lw4r7PSjDPvOYQ/ct5+AHxvkqo=</latexit>




we also need to record at which
timestamps an alias is used to read 4 v[0] = 1;                  v is used for writing at 4
or write. For instance, in Fig. 2 the 5 let b2 = & v;
                                                                 b27! shr(5 ⇠ 5, v)
owner v is recorded to be used to
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          <latexit sha1_base64="wbaNb9b1W+xAEAYTPOjFHl+I/go=">AAAB7nicbZC7SgNBFIbPxluMt3jpbAaDYBV2DUE7AxZaRjAXSJYwO5lNhszMLjOzQlzyEDYWithaWfkkdpa+iZNLoYk/DHz8/znMOSeIOdPGdb+czNLyyupadj23sbm1vZPf3avrKFGE1kjEI9UMsKacSVozzHDajBXFIuC0EQwux3njjirNInlrhjH1Be5JFjKCjbUa5bZmApU7+YJbdCdCi+DNoHDxcf999X6QVjv5z3Y3Iomg0hCOtW55bmz8FCvDCKejXDvRNMZkgHu0ZVFiQbWfTsYdoWPrdFEYKfukQRP3d0eKhdZDEdhKgU1fz2dj87+slZjw3E+ZjBNDJZl+FCYcmQiNd0ddpigxfGgBE8XsrIj0scLE2Avl7BG8+ZUXoX5a9EpF78YrVFyYKguHcAQn4MEZVOAaqlADAgN4gCd4dmLn0XlxXqelGWfWsw9/5Lz9AIQVkq8=</latexit>




write at Line 4 and 6. Here we use 6 v[1] = 2;                   v is used for writing at 6

                                           7 let t = (*b2)[1];           b2 7! shr(5 ⇠ 7, v)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    <latexit sha1_base64="PlPnD1A27AvzmXNMCskQidesvDM=">AAAB7nicbZC7SgNBFIbPxluMt3jpbAaDYBV2DRI7AxZaRjAXSJYwO5lNhszMLjOzQlzyEDYWithaWfkkdpa+iZNLoYk/DHz8/znMOSeIOdPGdb+czNLyyupadj23sbm1vZPf3avrKFGE1kjEI9UMsKacSVozzHDajBXFIuC0EQwux3njjirNInlrhjH1Be5JFjKCjbUaZ23NBCp38gW36E6EFsGbQeHi4/776v0grXbyn+1uRBJBpSEca93y3Nj4KVaGEU5HuXaiaYzJAPdoy6LEgmo/nYw7QsfW6aIwUvZJgybu744UC62HIrCVApu+ns/G5n9ZKzHhuZ8yGSeGSjL9KEw4MhEa7466TFFi+NACJorZWRHpY4WJsRfK2SN48ysvQv206JWK3o1XqLgwVRYO4QhOwIMyVOAaqlADAgN4gCd4dmLn0XlxXqelGWfWsw9/5Lz9AIcdkrE=</latexit>




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
                                           A error is detected until line 7, since b2 should disable v
                                               during its lifetime 5 ⇠ 7, but v is used to write at 6
                                                                 <latexit sha1_base64="Cl9LxwXrqujAh0LUiyovMFivu64=">AAAB7XicbZC7SgNBFIbPxluMt3jpbAaDYBV2FYmdAQstI5gLJEuYncwmY2Zml5lZIS55BxsLRWztrHwSO0vfxMml0MQfBj7+/xzmnBPEnGnjul9OZmFxaXklu5pbW9/Y3Mpv79R0lChCqyTikWoEWFPOJK0aZjhtxIpiEXBaD/oXo7x+R5Vmkbwxg5j6AnclCxnBxlq105ZmotTOF9yiOxaaB28KhfOP++/L97200s5/tjoRSQSVhnCsddNzY+OnWBlGOB3mWommMSZ93KVNixILqv10PO0QHVqng8JI2ScNGru/O1IstB6IwFYKbHp6NhuZ/2XNxIRnfspknBgqyeSjMOHIRGi0OuowRYnhAwuYKGZnRaSHFSbGHihnj+DNrjwPteOid1L0rr1C2YWJsrAPB3AEHpSgDFdQgSoQuIUHeIJnJ3IenRfndVKacaY9u/BHztsPL7WShw==</latexit>
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                    1:9



           Natural number          n, m ∈ N
           Types                      t∈T
           Time stamps           ts ∈ Tim
           Local Lifetimes          lt ∈ LT    ::=   ts1 ∼ ts2
           Stack locations            s ∈ Ls         (Ls , ≤s ) is a partially ordered set
           Block locations           b ∈ Lb          (Lb , ≤b ) is a totally ordered set and Ls ∩ Lb = ∅
           Heap locations       (b, n) ∈ Lh          L h ≜ Lb × N
           Mem locations             l ∈ Lm    ::=   s | (b, n)
           Paths                           p   ::=   s | *p | p.n
           Alias                      a∈A      ::=   s | a.n
           Pointer Values                 pv   ::=   own(b) | shr(lt, p) | shr(p)
                                                 |   mut(lt, p) | mut(p) | raw(l)
           Primitive Values        sv ∈ SV     ::=   i ∈ Int | str ∈ Str | c ∈ Char
                                                 |   f ∈ Float | bv ∈ Bool
           Values                  v ∈ Val     ::=   ⊥ | pv | sv


           Mem Operations              mop     ::=   alloc(n,t) | free(b)
                                                 |   lv(p) | read(p) | write(p, v)
                                                 |   rawRead(l) | rawRead ′ (l)
                                                 |   rawWrite(l, v) | rawWrite ′ (l, v)
                                                 |   aRead(l) | aWrite(l, v)


                                  Fig. 3. The grammar of the memory model
lines to denote timestamps for il-
lustration. In the memory model,
timestamps are generated by se-
mantics rules. Fig. 3 illustrates the
grammar of the memory model.
We detail them in the following
subsections.

4.1   Memory Configuration
A memory configuration is defined as a 4-tuple mem = (S, H, P, ms), where S is for stacks, H is for
a heap, P stores the latest timestamps at which an alias is used to read or write as we explained in
the motivation example, ms is used for sequential consistency checking of concurrent access. We
elaborate them as follows.
                                                              fin
   The stacks are modeled as a finite partial map S : Ls −−⇀ (Val × T ) from stack locations in the
set Ls (“Stack locations” in Fig. 3) to typed values, denoted as v : t, where v ∈ Val is a value and
t ∈ T is its type. Different stacks have disjoint location spaces in Ls to ensure that the stacks are
local to their corresponding threads. Ls is partial order under ≤s since only stack locations in the
same thread are ordered to denote the creation order of local variables. Various strategies could
be selected to implement Ls . For instance, a stack location could be a pair (tid, n), where tid is a
thread id and n is a natural number to denote a local stack location of tid.
   The heap is defined as a set of blocks H = {B 1 , . . . , Bn }. A block Bi is 4-tuple (bi , ni , mi , ti ),
where bi ∈ Lb , Lb is a set of block locations (“Block locations” in Fig. 3) and each block has a unique
block location, ni ∈ N is the size of the block, mi : [0, ni − 1] → Val × T is a map from the offsets in

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            Stack                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Heap
   1. struct T {x:i32,y:B}
   2. enum B {Empty,L([i32:3])}
   3. let a = [1,2,3];
   4. let b = B::L(a);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      b1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            3 [i32:3]
   5. let t = T{x:1,y:b};                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               …                  0 7! 1:i32
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           1 7! 2:i32
                             a   s0 7! own(b1):[i32:3]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           2 7! 3:i32
                                 <latexit sha1_base64="b93Nc0cC9mqsfToEBt//bm2EOug=">AAAB8nicbZC7SgNBFIZnEy8x3qJiZTMYBKuwq4WWARvLCOYCyRJmJ7PJkLksM2eFsOQxbCwUsfUlfAULwcpH0cml0MQfBj7+/xzmnBMlglvw/U8vl19ZXVsvbBQ3t7Z3dkt7+w2rU0NZnWqhTSsilgmuWB04CNZKDCMyEqwZDa8mefOOGcu1uoVRwkJJ+orHnBJwVtt2fdyRJLGgu6WyX/GnwssQzKFczX98vx1+sVq39N7paZpKpoAKYm078BMIM2KAU8HGxU5qWULokPRZ26Eiktkwm448xifO6eFYG/cU4Kn7uyMj0tqRjFylJDCwi9nE/C9rpxBfhhlXSQpM0dlHcSowaDzZH/e4YRTEyAGhhrtZMR0QQyi4KxXdEYLFlZehcVYJzivBTVCu+mimAjpCx+gUBegCVdE1qqE6okije/SInjzwHrxn72VWmvPmPQfoj7zXH37WlRo=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                             b   s1 7! own(b3):B
                                 <latexit sha1_base64="s2qenLJynf1sEfQf8VAx1kJ2MJw=">AAAB8nicbZC7SgNBFIZnEy8x3qJiZTMYBKuwq4WWARvLCOYCyRJmJ7PJkLksM2eFsOQxbCwUsfUlfAULwcpH0cml0MQfBj7+/xzmnBMlglvw/U8vl19ZXVsvbBQ3t7Z3dkt7+w2rU0NZnWqhTSsilgmuWB04CNZKDCMyEqwZDa8mefOOGcu1uoVRwkJJ+orHnBJwVtt2A9yRJLGgu6WyX/GnwssQzKFczX98vx1+sVq39N7paZpKpoAKYm078BMIM2KAU8HGxU5qWULokPRZ26Eiktkwm448xifO6eFYG/cU4Kn7uyMj0tqRjFylJDCwi9nE/C9rpxBfhhlXSQpM0dlHcSowaDzZH/e4YRTEyAGhhrtZMR0QQyi4KxXdEYLFlZehcVYJzivBTVCu+mimAjpCx+gUBegCVdE1qqE6okije/SInjzwHrxn72VWmvPmPQfoj7zXH4BilRs=</latexit>




                             t                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    s2 7! own(b4):T
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            b3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             2     B
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  <latexit sha1_base64="QBlkXWNEtP5oUk5iSikmeSPi0v0=">AAAB8nicbZC7SgNBFIZnjZcYb1GxshkMglXYjYWWARvLCOYCmyXMTibJkLksM2eFsOQxbCwUsfUlfAULwcpH0cml0MQfBj7+/xzmnBMnglvw/U9vJbe6tr6R3yxsbe/s7hX3DxpWp4ayOtVCm1ZMLBNcsTpwEKyVGEZkLFgzHl5N8uYdM5ZrdQujhEWS9BXvcUrAWaHtVHBbksSC7hRLftmfCi9DMIdSNffx/Xb0xWqd4nu7q2kqmQIqiLVh4CcQZcQAp4KNC+3UsoTQIemz0KEiktkom448xqfO6eKeNu4pwFP3d0dGpLUjGbtKSWBgF7OJ+V8WptC7jDKukhSYorOPeqnAoPFkf9zlhlEQIweEGu5mxXRADKHgrlRwRwgWV16GRqUcnJeDm6BU9dFMeXSMTtAZCtAFqqJrVEN1RJFG9+gRPXngPXjP3susdMWb9xyiP/JefwCB7pUc</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    b2   1   L
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        …                  0 7! 1:i32
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0 7! own(b1):[i32:3]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           1 7! own(b2):L
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            b4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             2     T
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           0 7! 1:i32
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           1 7! own(b3):B
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="bbG2XjbIiLWXJPraZ6QzEa74wJ4=">AAAB7nicbZC5TgMxEIZnOUO4wtHRWERIVNEuFNARiQLKIJFDSlaR1/EmVuy1ZXuRwioPQUMBQrRUVDwJHSVvgnMUkPBLlj79/4w8M5HizFjf//IWFpeWV1Zza/n1jc2t7cLObs3IVBNaJZJL3YiwoZwltGqZ5bShNMUi4rQe9S9Hef2OasNkcmsHioYCdxMWM4Kts+otgZWxsl0o+iV/LDQPwRSKFx/331fv+1mlXfhsdSRJBU0s4diYZuArG2ZYW0Y4HeZbqaEKkz7u0qbDBAtqwmw87hAdOaeDYqndSywau787MiyMGYjIVQpse2Y2G5n/Zc3UxudhxhKVWpqQyUdxypGVaLQ76jBNieUDB5ho5mZFpIc1JtZdKO+OEMyuPA+1k1JwWgpugmLZh4lycACHcAwBnEEZrqECVSDQhwd4gmdPeY/ei/c6KV3wpj178Efe2w+qFJNw</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Fig. 4. An example of the stacks and heap

the range [0, ni − 1] to the corresponding typed values ([n1 , n2 ] denotes the set of natural numbers
n1 , n1 + 1, . . . , n2 ), and ti ∈ T is the block’s type. A heap location is defined as a pair (b, m) (“Heap
locations” in Fig. 3), where b is a block location and m is the offset within the block b.
   The definitions of stacks and heaps are capable of storing values of various types, such as
primitive types (integers, boolean values, among others), pointers, arrays, product types, and sum
types. Heap blocks storing values of primitive types or pointers have size 1. Blocks storing arrays
or values of product types have size greater or equal than 1, according to the number of elements
the types are composed of, and two elements in the case of sum types: one for the value itself and
another to indicate the constructor that the sum type selects to construct the value. Fig. 4 illustrates
the stacks and heap created by the program on the left in the figure. Three variables a, b, t created
at lines 3, 4, 5 have the corresponding stack locations s 0 , s 1 , s 2 , respectively. Line 1 and 2 define a
struct type and an enum type, respectively. Line 3 creates a block to store an array of the type
[i32:3] (a 32 bits integer array of the size 3). The location, size, and type of the block are b1, 3,
and [i32:3] respectively. The offsets 0, 1, 2 store the values 1, 2, 3 of type i32, respectively. Line 4
creates two blocks b2 and b3. The block b2 stores the value of the type L defined by the constructor
L in the enumeration type B. The symbol own(b1) denotes a value storing the address of the block
b1. The block b3 stores the value of the type B, which has two constructors: Empty and L. The value
“1” at the offset 0 in the block b3 indicates the constructor L is selected, otherwise if it is 0 then the
constructor Empty is selected. Line 5 creates the block b4 storing the value of type T.
   In order to access memory locations, paths and aliases are introduced (Paths, Aliases in Fig.
3). A path could be a stack location, a dereference, or a field. It can be used to access a memory
block with an alias that refers to the block. Consider the following code “struct P{x:i32,y:i32}
let v = P{x:1,y:2}; let z = & v; ”, if we want to access the field x of v with the alias
z then the path is (∗z).x. Assume the stack location of b is s and the field x corresponds to the
offset 0. The path     ( in the memory model is (* s).0. Each path p has an alias, which is defined
                         p           p = s or p = s.n1 . . . nm
as: alias(p) ≜                                                  . Roughly speaking, the alias of a path is the
                         alias(p ′) p = ∗p ′ or p = (∗p ′).n
term innermost the path without dereferences. An alias of a block itself is also a memory location.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                    1:11


For instance, s 1 .1 corresponds to the heap location (b3, 1) in Fig. 4, which refers to the block b2. We
define a predicate des(a′, a) for two aliases as des(a′, a) ≜ ∃m ≥ 0.a′ = a.n1 . . . . .nm . It means that
a′ is a field or nested field of a. For instance, in Fig. 4, s2 .1 is a field of s2 , s2 .1.1 if a field of s2 .1 and
the nested field of s2 . Note that, des(a, a) = true. This is introduced for fine-grained borrowings.
For a borrowing relation a →b a′, if des(a′′, a′) then a →b a′′.
                                                                                             fin
   The third element in the configuration mem is a finite partial map P : A −−⇀ Tim × Tim from
aliases to pairs of timestamps, which stores the latest timestamps at which an alias was used to
read and write, respectively. For instance, s 7→ (ts1 , ts2 ) ∈ P means that the latest reading and
writing using s happened at ts1 and ts2 , respectively. This information is used to check whether a
reading or writing is disabled by other references.
                      f in
   Finally, ms : Lm −−−⇀ N × N is a finite partial map from memory locations (“Memory locations” in
Fig. 3) to pairs of natural numbers, used to detect data races with respect to sequential consistency,
where l 7→ (n1 , n2 ) ∈ ms represents that there are n1 and n2 reading and writing simultaneous
accesses from/to the location l. The idea is inspired by Jung and others [Jung et al. 2018a].
   At the end of this subsection, we introduce some notations for mem = (S, H, P, ms). For a
partial map M, M(k) denotes value of the key k in the map. If k has no value in M then M(k) is
undefined. The notation M[k ← v] denotes a new(map obtained from M by replacing the value
                                                        v      k = k′
of k with v, which is defined as: M[k ← v](k ′) ≜                     . Let B = (b, n, m, t) be a block
                                                        M[v] k , k ′
in H and l = (b, n′), 0 ≤ n′ < n. H (l) ≜ m(n′) denotes the value stored in the heap location l.
H [l ← v] ≜ (H \{B}) ∪ {(b, n, m[n′ ← v], t)} denotes a new heap by replacing the value in l with
v. Moreover, we use mem(l) = v to denote S(l) = v ∨ H (l) = v and mem[l ← v] to denote a new
memory configuration in which S is replaced with S[l ← v] or H is replaced with H [l ← v] when
l is a stack or a heap location, respectively.

4.2   Values of Memory Model
We now introduce the kinds of values used in the memory. Generally speaking, there are three
kinds of values: primitive values, pointers, and ⊥ denoting the uninitialization of a memory location.
Primitive values include integers, floating-pointer values, boolean values, characters, and strings,
which are standard. Here we focus on the elaboration of pointer values (“Pointer Values” in Fig. 3).
Pointer values consist of the following 3 kinds:
     • Own pointers (own(b)) to indicate the ownership of a block b, an alias holds an own pointer
        means it owns the block.
     • Shared and mutable reference values. The shared (resp. mutable) reference values have two
        forms shr(lt, p) and shr(p) (resp. mut(lt, p) and mut(p)). The reason is that lifetimes are
        transparent for users using the model, whilst in the memory, a reference should be attached
        a lifetime for OBS checking.
     • Unsafe pointers (raw(l)), which are raw pointers to memory locations. Unsafe pointers belong
        to the unsafe features of Rust.
Own pointers, shared and mutable reference values are safe pointers. Rust distinguishes safe and
unsafe pointers to decide whether to carry out OBS invariant checking.
   The values shr(p) and mut(p) create references to alias(p). For instance, we can write a bor-
rowing like “let x = & (*v); ” in Rust. Assume the stack location of v is s then the reference
value to be assigned to x is shr(∗s). Here the path is ∗s and its alias is s. For two aliases a and
a′, if a holds a shared (resp. mutable) reference value to a′, i.e., shr(lt, p) ∧ alias(p) = a′ (resp.
mut(lt, p) ∧ alias(p) = a′) in mem, then we also write a →s a′ ∈ mem (resp. a →m a′ ∈ mem)

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:12                                            Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


and the notation lifetime(a, mem) denotes lt in the values. Moreover the notation a1 →b∗ an ∈ mem
denotes that there exists a sequence a1 , a2 , . . . , an−1 , an for n ≥ 1 such that ai →b ai+1 ∈ mem, 1 ≤
i < n, where →b denotes either →m or →s . Note that a →b∗ a ∈ mem.
   The lifetime ts1 ∼ ts2 in a reference value indicates that the reference is created at the timestamp
ts1 and the last timestamp it is used to read or write is ts2 . Note that, In Fig. 3, the meta-variable lt
is called local lifetimes. The reason is that for a reference a, it is in use if it is used to read, write, or
borrowed by other references. The local lifetime is the span only from its creation to the timestamp
that it is used to read or write. Therefore the exact lifetime of a reference in mem, denoted as
L(a, mem), is defined as L(a, mem) = a′ ∈ {a′′ |a′′ →∗ a∈mem } lifetime(a′, mem). It is the union of all
                                           Ð
                                                           b
local lifetimes of a ′ such that a ′ →b∗ a ∈ mem.

4.3     Lifetime-Free Memory Operation Interfaces
The memory operation interfaces (“Memory Operations” in Fig. 3) are lifetime-free, which means
that the parameters of memory operations have no lifetimes. This design aims at abstracting lifetime
information from the memory interfaces to enable reusability, since other languages may not have
the notion of lifetimes. Memory operations include:
       • Allocation (alloc(n, t)), allocates a new memory block of size n for storing the value of the
         type t. Free (free(b)), deallocates the memory block b.
       • Raw reading and writing (rawRead(l), rawWrite(l, v)) provide non-atomic reading and writ-
         ing without integrating OBS invariant checking.
       • Atomic reading and writing (aRead(l), aWrite(l, v)) provide atomic reading and writing
         without integrating OBS invariant checking.
       • Reading and Writing (read(p), write(p, v)) provide reading and writing with the integration
         of OBS invariant checking.
       • Lvalue (lv(p)), computes the Lvalue of the path p. Lvalue of a path is the memory location
         identified by the path and Rvalue is the value stored in the Lvalue of the path.
   Here we need to restrict that if the parameter v in either rawWrite, aWrite, or write is a
reference value then it can only be shr(l) or mut(l), i.e., no lifetimes. Actually, lifetime computation
is hidden in the implementation of memory operations, which will be introduced in the following.
   The semantics is defined by two kinds of transition relations. The first one is ⟨mem, tm⟩ ts ⇝m
                ′
⟨mem ′, tm ′⟩ ts . tm and tm ′ are terms that can be a value, a memory operation, or “.” indicating that
the operation is consumed. The symbols ts and ts′ are the timestamps of the pairs and satisfying
ts ≤ ts′. The second one is ⟨mem, tm⟩ ts ⇝m stuck indicating the semantics gets stuck. Some of
S, H , P, ms can be omitted in rules if they are not used to make rules more concise.

4.3.1 Operational Semantics for Allocation and Free. Rule Allocation defines the semantics for
alloc(n, t), where n and t are the size and type of the new block, respectively. It creates a new
block with a fresh block location (fresh(H )) and adds the new block to the heap H . Moreover,
it also initializes ms for the new block. initBlk(n) denotes the map {0 7→ ⊥, . . . , n − 1 7→ ⊥}.
initMS(b,n) = {(b,0) 7→ (0, 0), . . . , (b,n-1) 7→ (0, 0)}. Free removes a block from H . The
set bLoc(H ) denotes all the block locations used in H , i.e., for any b ∈ bLoc(H ), there is a block
(b, n, m, t) in H . “_” matches anything. The timestamps are increased by Su(ts).

   Allocation:                                                        Free:
        b = fresh(H ) H ′ = H ∪ (b, n, initBlk(n), t)                  b ∈ bLoc(H ) H ′ = H \{(b, n, _, _)} n ≥ 0
                  ms ′ = ms ∪ initMS(b,n)                              ms ′ = ms\{(b,0) 7→ _, . . . , (b,n-1) 7→ _}
   ⟨(H, ms), alloc(n, t)⟩ ts ⇝m ⟨(H ′, ms ′ ), own(b)⟩ Su(ts)         ⟨(H, ms), free(b)⟩ ts ⇝m ⟨(H ′, ms ′ ), .⟩ Su(ts)

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                      1:13


4.3.2 Operational Semantics for Non-Atomic Raw Reading and Writing. The rules for rawWrite
and rawRead are non-atomic writing and reading that are directly applied to raw pointers. The
execution of a raw operation will get stuck under data races. For a location l and l 7→ (n1 , n2 ) ∈ ms,
data races are defined as (1) (n1 + n2 ≥ 2) ∧ (n2 ≥ 1), i.e., there are at least two threads accessing the
location and at least one of them writes the location. In order to simulate non-atomic operations,
both raw reading and writing are decomposed into two steps that can be interleaved.
   The raw writing is defined by Rule RawWrite and RawWrite′. It is a two step operation where
the first step modifies ms and translates rawWrite(l, v) to rawWrite′(l, v) and ms(l) = (0, 0) ensures
that the writing will not cause a data race. The second step writes v in the heap location l, and
resets ms. The two steps can be interrupted by other threads. The semantics of raw reading is
similar to the raw writing, which is defined by Rule RawRead and RawRead′. Timestamps are
not increased, since they are not for safe pointers. We still need the semantics for detecting race
conditions. Rule Race-RawRead defines the semantics for the race conditions of the reading. It
evolves into the stuck state. The race semantics for other operations are similar.

  RawWrite:                                                     RawWrite ′ :
     ms(l) = (0, 0) ms ′ = ms[l ← (0, 1)]                                ms(l) = (0, 1) H ′ = H [l ← v]
     ⟨(H, ms), rawWrite(l, v)⟩ ts                                             ms ′ = ms[l ← (0, 0)]
           ⇝m ⟨(H, ms ′ ), rawWrite ′ (l, v)⟩ ts                ⟨(H, ms), rawWrite ′ (l, v)⟩ ts ⇝m ⟨(H ′, ms ′ ), .⟩ ts
  RawRead:                                                          RawRead ′ :
  ms(l) = (n, 0) n ≥ 0 ms ′ = ms[l ← (n + 1, 0)]                          ms(l) = (n, 0) H (l) = v v , ⊥
         ⟨(H, ms), rawRead(l)⟩ ts                                         n ≥ 1 ms ′ = ms[l ← (n − 1, 0)]
                ⇝m ⟨(H, ms ′ ), rawRead ′ (l, v)⟩ ts                ⟨(H, ms), rawRead ′ (l)⟩ ts ⇝m ⟨(H, ms ′ ), v⟩ ts
  Race-RawRead:                                              Concur-Stuck:
  mem = (S, H, P, ms) ms(l) = (n1 , n2 ) ∧ n2 > 0            ⟨mem, t 1 ⟩ ts ⇝m stuck or ⟨mem, t 2 ⟩ ts ⇝m stuck
        ⟨mem, rawRead(l)⟩ ts ⇝m stuck                                       ⟨mem, t 1 || t 2 ⟩ ;c stuck
                 Concur-1:                                    Concur-2:
                   ⟨mem, t 1 ⟩ ts ⇝m ⟨mem ′, t⟩ ts              ⟨mem, t 2 ⟩ ts ⇝m ⟨mem ′, t⟩ ts
                 ⟨mem, t 1 || t 2 ⟩ ;c ⟨mem ′, t || t 2 ⟩     ⟨mem, t 1 || t 2 ⟩ ;c ⟨mem ′, t 1 || t⟩
   For instance, we consider the concurrent execution of two operations rawRead(l) and rawWrite(l, v)
under a concurrent semantics based on interleaving, whose grammar is con ::= tm || tm, where tm
can be a memory operation, a value, or “.” The semantics is defined by the Rule Concur-1, Concur-2,
and Concur-Stuck, with the relation ;c (The concurrent semantics is only for illustration here.
RustSEM concurrent semantics is implemented in CL level.
   Assume the initial memory configuration satisfies ms(l) = (0, 0) and H (l) , ⊥, there are 4
possible execution sequences as follows:
   (Sequence 1) rawRead(l); rawRead′(l); rawWrite(l, v); rawWrite′(l, v);
   (Sequence 2) rawWrite(l, v); rawWrite′(l, v); rawRead(l); rawRead′(l);
   (Sequence 3) rawRead(l); rawWrite(l, v); stuck;
   (Sequence 4) rawWrite(l, v); rawRead(l); stuck.
   Sequences (1) and (2) are safe, but Sequence (3) and (4) are unsafe. For instance, in Sequence
(4), after executing rawWrite(l, v), we have that ms(l) = (0, 1), which makes rawRead(l) get stuck
(Rule Race-RawRead). We will not present atomic reading and writing without OBS invariant
checking as their semantics rules are trivial.
4.3.3 Operational Semantics for Reading and Writing with OBS Checking. The reading and writing
operations for the safe pointers need to maintain the invariants of OBS. The invariants correspond
to the well-formed memory configurations, which are defined as follows.

                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:14                                            Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


  Definition 4.1 (Well-formed memory configurations). Let mem = (S, H, P, ms) be a memory
configuration. It is well-formed, denoted as wellform(mem), iff it satisfies the following invariants.
   (1) ∀b, l, l ′ .(mem(l) = mem(l ′) = own(b)) =⇒ l = l ′.
   (2) ∀a, a1 , a2 .a1 →m a ∈ mem∧a2 →b a′ ∈ mem∧des(a, a′) =⇒ L(a1 , mem) ∩ L(a2 , mem) = ∅.
   (3) ∀a, a′ .a →s a′ ∈ mem =⇒ (∀a1 .des(a1 , a′) ∧ P(a1 ) = (ts, ts′) =⇒ ts′ < L(a, mem)).
   (4) ∀a, a′ .a →m a′ ∈ mem =⇒ (∀a1 .des(a1 , a′) ∧ P(a1 ) = (ts, ts′) =⇒ ts < L(a, mem) ∧ ts′ <
       L(a, mem).
   (5) ∀l .ms(l) = (n 1 , n 2 ) =⇒ ¬((n 1 + n 2 ≥ 2) ∧ (n 2 > 1)).
   Invariant (1) ensures that no block is owned by more than one locations. Invariant (2) ensures
that an alias cannot be borrowed by two references simultaneously with one of them being mutable.
Invariant (3) ensures if an alias is borrowed by a shared reference then its latest writing timestamp
cannot be in the lifetime of the reference. Invariant (4) ensures if an alias is borrowed by a mutable
reference then both its latest reading and writing timestamps cannot be in the lifetime of the
reference. The last invariant ensures no data race.
   Compared with well-formed OBS graphs, well-formed memory configurations also contain
unique owner and lifetime disjoint invariants, but no lifetime inclusion invariant. Lifetime inclusion
invariant will be maintained by the semantics rules directly. Invariants (4) and (5) of well-formed
memory configurations correspond to the permission functions, but not exactly since it only disable
the latest reading and writing. We will prove that it enforces memory operations to follow the
permission functions in Subsection 4.4. Data race is not considered in the well-formed OBS graphs,
since OBS graphs only consider about safe pointers
   The semantics of Lvalue. The lvalue of a path is the location identified by the path that is to
be written or read. The lifetimes of references accessed during the computation of lv should be
extended since the references are used. The result of lv(p) is pair (l, wp) where l is the Lvalue and
wp is a boolean value indicates whether p is permitted to write. A path is permitted to write iff
the borrowing links “alias(p) →m a . . . a′ →m x” from the alias alias(p) to the owner x are all
mutable borrowings.
   The first rule for Lvalue is Lv-Deref, which computes the Lvalue of ∗p, where p is a path. We
use ref(p ′) (resp. ref(lt, p ′)) to denote a reference, which can be either a shared reference shr(p ′)
(resp. shr(lt, p ′)) or a mutable reference mut(p ′) (resp. mut(lt, p ′)).
       • Premise (1) computes the Lvalue of p, which is l. Lvalue semantics does not increase the
         timestamp as it is one of the sub-steps for reading and writing.
       • Premise (2) checks whether the location is being written by a non-atomic operation. Jmem 1 K.ms
         denotes the element ms in the memory configuration mem 1 . It requires that the number of
         writings is 0 and the number of readings is greater than or equal to 0. Therefore it could be
         used to check the data races that a non-atomic writing is carrying out but interleaved by safe
         operations.
       • Premise (3) requires that the location l must be a shared or mutable reference, since we can
         only dereference a reference. It is a shorthand for ∃p ′, lt .mem 1 (l) = ref(lt, p ′).
       • As the reference l is used, its lifetime is extended to the timestamp ts (Premise (4)) by the
         function extLT, which is defined as follows.
                                    mem[l ← shr(ts1 ∼ ts, p ′ )] mem(l) = shr(ts1 ∼ ts2 , p ′ )
                                   
               extLT(mem, l, ts)≜
                                       mem[l ← mut(ts1 ∼ ts, p )] mem(l) = mut(ts1 ∼ ts2 , p )
                                                             ′                                 ′

       • Since the referent p ′ is a path, its Lvalue needs to be further computed (Premise (5)).
       • Premise (6) ensures the memory configuration is still well-formed after the computation.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                    1:15


    • Premise (7) checks whether l is a mutable reference (The notation e?v 1 , v 2 denotes that if e is
      true then v 1 otherwise v 2 ).
   The resulting permission is decided by wp ∧ wp1 ∧ wp2 , i.e., whether all references accessed by
the semantics rule are mutable references. Rule Lv-Location and Lv-Field compute the Lvalues
of a location (which is itself) and a field, respectively.
 Lv-Deref:
                (1) ⟨mem, lv(p)⟩ ts ⇝m ⟨mem 1 , (l, wp1 )⟩ ts (2) Jmem 1 K.ms(l) = (n, 0) ∧ n ≥ 0
 (3) mem 1 (l) = ref(lt, p ′ ) (4) mem 2 = extLT(mem 1 , l, ts) (5) ⟨mem 2 , lv(p ′ )⟩ ts ⇝m ⟨mem 3 , (l ′, wp2 )⟩ ts
                      (6) wellform(mem 3 ) (7) wp = (mem 1 (l) = mut(lt, p ′ )?true : false)
                               ⟨mem, lv(∗p)⟩ ts ⇝m ⟨mem 3 , (l ′, wp ∧ wp1 ∧ wp2 )⟩ ts

                                                          Lv-Field:
        Lv-Location:                                        (1) ⟨mem, lv(p)⟩ ts ⇝m ⟨mem 1 , (l, wp)⟩ ts
        ⟨mem, lv(l)⟩ ts ⇝m ⟨mem ′, (l, true)⟩ ts           (2) mem 1 (l) = own(b) (3) b ∈ bLoc(mem 1 )
                                                          ⟨mem, lv(p.n)⟩ ts ⇝m ⟨mem 1 , ((b, n, ), wp)⟩ ts
   For instance, assume in the memory, we have s1 7→ mut(1 ∼ 2, s2 ), s2 7→ own(b) and ms(s1 ) =
(0, 0), ms(s2 ) = (0, 0). If we try to compute lv(∗s1 ), Rule Lv-Deref works as follows.
    • Premise (1) computes ⟨mem, lv(s1 )⟩ and gets (s1 , true) by Rule Lv-Location.
    • Premise (2) and (3) are true as ms(s1 ) = (0, 0) and s1 holds mut(1 ∼ 2, s2 ).
    • Premise (4) extends its lifetime to the current timestamp (assume it is 4). Thus value of s1 is
      updated as mut(1 ∼ 4, s2 ) now.
    • Premise (5) further computes the lvalue of lv(s2 ), which is (s2 , true). Therefore lv(∗s1 ) is s2 .
    • The writing permission is true as s1 a mutable reference and the writing permission of both
      lv(s1 ) and lv(s2 ) are true.
  The semantics of writing. The semantics of write(p, v), writes the value v to the Lvalue of p. Rule
Write-Ref defines the semantics for writing a reference value ref(p ′) to the Lvalue of the path p.
The semantics is elaborated as follows.
    • Premise (1) computes the Lvalue of the path p by lv(p) and requires the permission to write.
    • Premise (2) ensures no reading or writing to the location l,
    • Premise (3) writes the value v to the location l. The reference value should be attached with
      the local lifetime ts ∼ ts, i.e., the reference starts to have a lifetime.
    • Premise (4) updates the latest writing timestamp of p’s alias by the function addWrite.
      Assume mem = (S, H , P, ms), addWrite is defined as: addWrite(mem, a, ts) ≜ (S, H, P[a ←
      (ts1 , ts)], ms) if P(a) = (ts1 , ts2 ).
    • Premise (5) ensures that the memory configuration is well-formed after the writing.

 Write-Ref:
                      (1) ⟨mem, lv(p)⟩ ts ⇝m ⟨mem 1 , (l, true)⟩ ts (2) Jmem 1 K.ms(l) = (0, 0)
 (3) mem 2 = mem 1 [l ← ref(ts ∼ ts, p ′ )] (4) mem 3 = addWrite(mem 2 , alias(p), ts) (5) wellform(mem 3 )
                                 ⟨mem, write(p, ref(p ′ ))⟩ ts ⇝m ⟨mem 3 , .⟩ Su(ts)
    Write-Own:
                                                                  Write-Primitive:
      (1) ⟨mem, lv(p)⟩ ts ⇝m ⟨mem 1 , (l, true)⟩ ts
                                                                  (1) ⟨mem, lv(p)⟩ ts ⇝m ⟨mem 1 , (l, true)⟩ ts
                 (2) Jmem 1 K.ms(l) = (0, 0)
                                                                     (2) v ∈ SV (2) Jmem 1 K.ms(l) = (0, 0)
             (3) mem 2 = mem 1 [l ← own(b)]
                                                                            (3) mem 2 = mem 1 [l ← v]
      (4) mem 3 = addWrite(mem 2 , alias(p), ts)
                                                                  (4) mem 3 = addWrite(mem 2 , alias(p), ts)
       (5) wellform(mem 3 ) (6) b ∈ bLoc(mem)
                                                                  ⟨mem, write(p, v)⟩ ts ⇝m ⟨mem 3 , .⟩ Su(ts)
    ⟨mem, write(p, own(b))⟩ ts ⇝m ⟨mem 3 , .⟩ Su(ts)

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:16                                            Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


  Rule Write-Own is the semantics for writing an owner to a memory location. Rule Write-
Primitive is the semantics for writing primitive values, such as integers and boolean values.
  .
  The semantics of reading. The operation read(p) reads a value from the Lvalue of a path p.
Read-Ref defines the semantics for reading a reference.
       • Premise (1) computes the Lvalue of p, which is l and Premise (3) reads the value from l,
       • Premise (2) ensures no writing to the location. Premise (4) requires the value stored in l
         should be a shared or mutable reference.
       • Premise (5) updates the latest timestamp, at which the alias of p is read, by the function
         addRead, which is similar to addWrite.
       • Premise (6) extends the lifetime of l as it is used and Premise (7) checks well-formedness..
         Read-Ref:
         (1) ⟨mem, lv(p)⟩ ts ⇝m ⟨mem 1 , (l, _)⟩ ts (2) Jmem 1 K.ms(l) = (n, 0) ∧ n ≥ 0 (3) v = mem 1 (l)
                         (4) v = ref(lt, p ′ ) (5) mem 2 = addRead(mem 1 , alias(p), ts)
                              (6) mem 3 = extLT(mem 1 , l, ts) (7) wellform(mem 3 )
                                     ⟨mem, read(p)⟩ ts ⇝m ⟨mem 3 , v⟩ Su(ts)
         Read-Non-Reference:
         (1) ⟨mem, lv(p)⟩ ts ⇝m ⟨mem 1 , (l, _)⟩ ts (2) Jmem 1 K.ms(l) = (n, 0) ∧ n ≥ 0 (3) v = mem 1 (l)
                   (4) v is not a reference (5) v , ⊥ (7) if v = own(b) then b ∈ bLoc(mem)
                                     (6) mem 2 = addRead(mem 1 , alias(p), ts)
                                      ⟨mem, read(p)⟩ ts ⇝m ⟨mem 2 , v⟩ Su(ts)
  Rule Read-Non-Reference defines the semantics of reading non-reference values.
  Compared with weak memory models [Jung et al. 2018b; Podkopaev et al. 2019], RustSEM only
concerns about sequential consistency and lies in higher abstraction level without bridging the gap
between OBS and specific hardware architectures. We could further refine our memory model by
incorporating weak memory consistency in the future to strengthen its usability.

4.4     Refinement Relation between High-Level OBS and Memory Model
In this subsection, we prove the refinement relation between high-level abstraction of OBS and the
memory model. We begin with the definition of safe sequences.
  Definition 4.2. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be
an alternating sequence of memory configurations with timestamps and operations. For each pair
(mem, ts), mem is a memory configuration and ts is the timestamp reaching mem. π is a safe
sequence iff
   (1) mem 0 is an empty configuration, i.e., S, P, ms are empty maps and H is an empty set,
   (2) opi , 1 ≤ i ≤ n, is one of the memory operations: alloc(n, t), read(p), write(p, v), free(b),
   (3) ⟨memi , opi+1 ⟩ tsi ⇝m ⟨memi+1 , re⟩ tsi +1 , for all 0 ≤ i < n, where re can only be a value if
       opi+1 is read or alloc, otherwise consumed “.”.
 The memory configurations are the data refinement of the high-level OBS graphs. For each
memory configuration, it has an underlying OBS graph.
   Definition 4.3. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be
a safe sequence and B be a block in memi , (0 ≤ i ≤ n), whose location is b. The OBS graph
(V , B, E, F ) of memi is defined as:
       • V is a set of aliases in memi that can access B,

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                   1:17

                                  
                                  
                                   (o, B)   if mem(a) = own(b)
    • for any node a in V , E(a) = (s, a ) if a →s a ′′ ∈ memi ∧ des(a ′, a ′′)
                                  
                                  
                                         ′

                                   (m, a ′) if a →m a ′′ ∈ memi ∧ des(a ′, a ′′)
                                  
                                  
    • F (a →b a ′) = L(a, memi ). F (a →o B) = tsj ∼ tsi where for all j ≤ k ≤ i, memk (a) =
                                  

      own(b) and mem j−1 (a) , own(b).
  It is now sufficient to present Theorem 4.4, which specifies the refinement relation between the
high-level abstraction and the memory model.
   Theorem 4.4. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be
a safe sequence and B be a block. Assume the OBS graph of B in memi (0 ≤ i ≤ n) is G = (V , B, E, F )
then we have
   (1) (Data refinement) G is well-formed.
   (2) (Operation refinement) For any two nodes a, a ′ ∈ V ∪ {B} such that F (a →∗ a ′) = lt, for any
       operation opk (0 < k ≤ n), which is executed at the timestamp ts ∈ lt,
       • if opk is an operation that reading B by the alias a then RG (a, ts) = true,
       • if opk is an operation that writing B by the alias a then WG (a, ts) = true.
  The proof is in Appendix C. Theorem 4.4 shows that all operations by an alias a follow the
permission functions of memi ’s OBS graph for B.


5   CL LANGUAGE AND TRANSLATION SEMANTICS
In this section, we present the basic idea of CL language and the translation semantics, the supported
features of Rust, and the efforts of developing RustSEM. The semantics rules are not presented due
to page limitation. Actually, the core of RustSEM, OBS, is already formalized in the memory model.
   The design of CL is to reduce Rust grammar to a simple core in order to avoid redundant
formalization. Table 1 illustrates the Rust features supported by RustSEM (Column “Rust features”)
and the corresponding grammars in CL (Column “CL grammar”) for implementing the Rust features
on the same row.
   In CL, all constructs are expressions e that can be evaluated to values. The notion of variables (x),
values (v), dereferences (∗e), fields (e.e ′), arithmetic and boolean expressions, print, skip (clskip),
and assertions are standard. Shared (&e) and mutable (& mut e) references are the same as in Rust.
   Functions in CL are defined as expressions that can be evaluated and assigned to variables. This is
designed to represent Rust closures, which are anonymous functions with environments. There are
two forms of function calls: call and pcall. The former just calls the function f with a sequence of
arguments, whilst the latter is a polymorphic call pcall(e ′, f , e®) implementing dynamic dispatchs.
For instance, in Rust there are expressions like e ′ .f (e 1 , . . . , en ), for which we only know that e ′ is
an object implementing a trait (traits are like interfaces) containing f . Since there may be more
than one type implementing the trait, the concrete function f to be invoked depends on the type
of e ′ at runtime. As we modeled the memory as typed, i.e. each memory location stores both values
and their types, the type of e ′ at runtime can be obtained by reading the memory. Branches in CL
are defined by the case construct. Each case e → e ′ is a guarded action such that e ′ can be executed
only if e evaluates to be true. The constructs of threads (thread), bindings (bindinдs), assignment
(assiдn), and sequence (seq) are standard. The memory operations mop are also constructs in CL. It
means that the memory access in CL invokes the memory operations in Section 4. As the OBS is
formalized in the memory model, CL semantics does not need to concern about it.
   The translation semantics translates a Rust program to a CL program. Table 1 shows that most
features in Rust can be translated to corresponding CL constructs. We explain the last two rows

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:18                                              Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


                              Table 1. Correspondence between Rust and CL features

                       Rust features                                                 CL grammar
    • primitive values • shared and mutable references        e ::= v | x | ∗e | e.e ′ | allocInit(n, e®, t)
    • casting pointers • arithmetic expressions                    | e 1 + e 2 | e 1 < e 2 | e 1 &&e 2 | . . .
    • print • assertion • move semantics • dereference             | move(e) | &e | & mut e
    • field access • array access                                  | print(e) | clskip | assert(e)
    • binding • execution block                               bindinд ::= let x = e in {e ′ }
    • assignment                                              assiдn ::= e:=e ′
    • function • impl block • trait definition • trait impl   f un ::= fun f (®  x){e} | call(f , e®) | pcall(e ′, f , e®)
    • function call • method call • dynamic dispatch
    • polymorphism • closure
                                                                                −−−−−→
    • branch • pattern matching                               branch ::= case{e → e ′ }
    • loop • sequential                                       loop ::= loop e {e ′ } | break | continue
                                                              seq ::= e;e ′
    • concurrency                                             thread ::= fork(e) | wait(e)
    • raw pointers • intrinsic function                       e ::= mop
    • struct and enum types • generic types                   supported by the translation
    • Box • Array • Vector                                    −

in the table. For struct and enum types (user-defined types), in CL, the definitions of user-defined
types are not stored. When a Rust program tries to create an object of a user-defined type, the
translation generates an allocation in memory block with size of the type in CL. Translation
semantics records the information of types, therefore it knows the memory block size for each type.
Three data structures: Box, Array, and Vector are not hard-coded in the semantics, since they are
just a collection of Rust programs.
   Although RustSEM models a considerably large subset of Rust, it is not complete. Rust has no
standard and evolves very fast, which makes it hard or almost impossible to some extent to build a
complete semantics for it. We do not model module definitions, #[derive] attributes, among others.
   Developing a formal semantics for real world languages always requires huge efforts. RustSEM
is formalized in K and consists of around 1100 semantics rules, taking two and a half man-years.

6      EVALUATION OF SEMANTICS CORRECTNESS AND APPLICATIONS
In this section, we evaluate the semantics correctness of RustSEM (Subsection 6.1) and its applica-
tions in verification (Subsection 6.2).

6.1      Semantics Correctness
We have evaluated RustSEM in the following three aspects: (1) Functional correctness. For each
input of a program, we compare the execution output of RustSEM and the machine code generated
by the Rust compiler. (2) OBS checking evaluation. For each program, we check whether RustSEM
maintains the OBS invariants. It is compared with the compilation result of the Rust compiler. (3)
Semantic consistency, i.e., the absence of semantic ambiguities.
   We elaborate semantic ambiguities by an example. Consider the if-construct: “if e B1 else
B2 ” where e is an expression and Bi is an execution block for i = 1, 2. The semantics for the construct
could be:
                                                       (C, e) ; (C ′, v)
                        Branch:
                                    (C, if e B 1 else B 2 ) ; (C ′, if v B 1 else B 2 )


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                   1:19


           True:                                                 False:
                            v = true
           (C, if v B 1 else B 2 ) ; (C, B 1 )            (C, if v B 1 else B 2 ) ; (C, B 2 )
  The semantics is a transition relation (C, m) ; (C , m ), where C, C ′ are configurations and m, m ′
                                                    ′   ′

are terms, where a term could be a program or a value. Rule Branch evaluates the expression e to
a value v under the configuration C and C evolves into a new configuration C ′ since the evaluation
may have side effects. The if-construct is reduced to another if-construct with e replaced by
its value v. Rule True is for the case that v equals true, in which the first block should be executed.
Rule False is for the case that v equals false, in which the second block should be executed. Here
we deliberately remove the checking v = false from the premise of Rule False, which will lead to
ambiguity. Both Rule True and Rule False can match the if-construct with v being true. This is
called semantic ambiguity, i.e., more than one semantics rules could be applied to the same pair
of configuration and term. If K always tries to match Rule True first then the execution has no
problem. But if K matches Rule False first then the semantics is not correct. This bug could be
fixed by adding v = false to the premises of False.
   There is another semantic ambiguity in the example. If we do not distinguish values from
expressions in the semantics then the construct “if true B 1 else B 2 ” can match both Rule
Branch and True, since true is also an expression. Rule Branch could match it infinitely many
times, which should be avoided in our semantics.
   Now we formally define the semantics correctness and explain our testing methods.
   Definition 6.1 (Semantics rules and semantics). Let C be a set of configurations and M be a set
of terms. A semantics rule is a partial function: Ru : C × M ⇀     − C × M, i.e., mapping (or reducing) a
pair (c, m) of configuration c and term m to a new pair (c ′, m ′) of configuration c ′ and term m ′. A
semantics is a set of semantics rules: SL = {Ru 0 , . . . , Run }.
   Definition 6.2 (Execution traces of semantics). Let SL be a semantics for a language. A finite execu-
tion trace of SL is a sequence π = (c 0 , m 0 )(c 1 , m 1 ) . . . (c n , mn ), such that for each 0 ≤ i < n, ∃Ru ∈
SL.Ru(c i , mi ) = (c i+1 , mi+1 ). The trace π is called terminated if for all rule Ru ∈ SL, Ru((c n , mn )) is
undefined. An infinite or divergence trace is an infinite sequence π = (c 0 , m 0 )(c 1 , m 1 ) . . ., such that
for each 0 ≤ i, ∃Ru ∈ SL.Ru(c i , mi ) = (c i+1 , mi+1 ).
   Definition 6.3 (Semantics Correctness). Let m be a program in a language, whose semantics is SL,
the subset of configurations prem ⊆ C be the precondition of m, the relation postm ⊆ C × (C ∪ {∞})
be the postcondition of m, where ∞ denotes that the computation is diverge. The semantics SL
is called partially correct iff for all program m and for all c ∈ prem , either there is a terminating
trace (c, m) . . . (c ′, m ′) in SL satisfying ((c, m), (c ′, m ′)) ∈ postm or there is an infinite trace starting
from (c, m) satisfying ((c, m), ∞) ∈ postm . The semantics SL is called completely correct iff for
all program m and for all c ∈ prem , every terminating traces (c, m) . . . (c ′, m ′) in SL satisfying
((c, m), (c ′, m ′)) ∈ postm and if there is an infinite trace starting from (c, m) then ((c, m), ∞) ∈ postm .
   Let SL be a semantics, c be a configuration and m be a term. We denote by TraceS L (c, m) the set
of all terminating or infinite traces with (c, m) as the initial pair. K’s execution engine selects one
of the traces in TraceS L (c, m) for execution, whilst K’s verification engine searches for all possible
execution traces in TraceS L (c, m).
   An ambiguous semantics might be partially correct but not completely correct. Thus, we need
to detect semantic ambiguities to ensure complete correctness. Unlike Coq or Isabelle, K is not a
theorem prover that can be used to prove some properties of RustSEM. Instead, we can use its
execution engine for testing. However, only using its execution engine is not enough for detecting
semantic ambiguities if it always selects the right trace for execution. Therefore, we also use its

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:20                                            Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


verification engine for testing. Note that this is still called testing because test cases are used and
the input of each test case is fixed. For each test case, the following three steps are carried out.
   (1) Running the execution engine on the test case to detect bugs quickly.
   (2) Running the verification engine to detect semantic ambiguities.
   (3) Appending assert(False) to the end of each test case and run the verification engine again.
Note that Step (3) is used to detect semantic ambiguities missed by Steps (1) and (2). If a test case is
not properly selected, it will be correct under all possible execution traces. Thus K only outputs
“sat” and some semantic ambiguities are missed. If we append assert(False) at the end of the test
case then the verification engine can report all execution traces to assert(False) as the program
always fails.
   This testing strategy is efficient and effective. It is efficient because the test cases are small and
the inputs are fixed, thus no state explosion exists. It is effective because it can detect seman-
tic ambiguities, even with very simple test cases. For instance, the following test case with the
if-construct could detect the two semantic ambiguities in Rules Branch, True, and False by
running the verification engine.
                      if (true) { assert(true) } else { assert(false) }
                      if (false) { assert(false) } else { assert(true) }
   We have used 400 test cases for the memory operations and CL semantics, 300 test cases for the
translation semantics. These test cases mainly come from the Rust benchmark [Rust-Benchmark
2020], the Rust libraries and the Rust text book [Rust-Team 2018]. Besides, we have also created
new test cases for testing our new grammars of the memory operations and CL. The execution
result of each test in RustSEM is compared with the execution result and compilation result of the
Rust compiler version 1.4.5. All experiments are conducted on a computer with an Intel Xeon(R)
CPU E5-1650 v3 @ 3.50GHz × 12 and 16GB DDR4 RAM. The semantics of one construct in Rust
is usually formalized with a collection of K rules, and thus one test case can cover a collection of
rules.
   The experimental results show that:
   (1) Some correct tests are accepted by RustSEM but rejected by the Rust compiler, due to the
       conservative analysis of the compiler.
   (2) Some incorrect tests are rejected by RustSEM but accepted by the Rust compiler, showing
       that RustSEM is more powerful in detecting memory errors, especially in the programs mixed
       with safe and unsafe operations. For example, after the ownership of a block has been moved
       away from a variable by a safe operation, a raw pointer reads the block through the reference
       to the variable.
   (3) More than 36 semantic ambiguities are detected, showing that our testing technique for
       ambiguities is effective.
   (4) For a collection of tests with memory errors, RustSEM can successfully detect all errors. More
       details are discussed in the application in runtime verification (Subsection 6.2).

6.2    Applications in Verification
Runtime Verification for Detecting Memory Errors. RustSEM provides a runtime checker for detecting
memory errors, since the memory model integrates checkings for invalid memory accesses as
explained in Section 4. It is based on semantics instrumentation rather than most of the existing
runtime checkers, such as [Chen et al. 2019], which are based on code instrumentation. RustSEM
detects: (1) accessing uninitialized locations, (2) reading dangling pointers, (3) double frees, (4) data
races and deadlocks, (5) ownership and borrowing errors, (6) buffer overflows.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                    1:21


   Table 2 shows the evaluation result                Table 2. Results for runtime verification.
for runtime verification. “TC”, “IN”,
“Avg. Time(s)”, and “Avg. Mem(KB)” de- Memory errors                  TC IN        Avg.        Avg.
note the number of test cases, the num-                                            Time(s) Mem(KB)
ber of inputs for each test case, average   read uninit. values       22     10    6.16        387240
execution time and average memory read dangling pointers 11                  10    5.89        390356
consumption, respectively. For each         double frees              10     10    5.73        346096
kind of detectable memory errors, a         data races                14     10    7.36        394152
collection of test cases is created. All    ownership & borrowing 40         10    6.64        344088
the memory errors in the test cases         index overflows           21     10    7.16        379788
can be detected with the inputs that
can trigger the errors. Data races are not always detected in an execution, since executions are
non-deterministic.
   Compared with other runtime checkers, RustSEM is less efficient and depends on the efficiency
of K execution engine. In order to execute a program , K first constructs its abstract syntax tree
and searches the corresponding semantics rules for the tree at each execution step. The advantage
of RustSEM is that the memory checking is based on semantics instrumentation instead of code
instrumentation. The biggest test case is around 210 LOC with the execution time of around 10
seconds, including both translation and execution time.
   Formal Verification for both Memory and Functional Properties. K has a verification engine, which
can be used to construct a program verifier for a language by instantiating it with an operational
semantics of that language. The basic idea of the infrastructure could be explained as follows.
K verification engine takes an operational semantics given in K and generates queries to a theorem
prover (for example, Z3 [de Moura and Bjørner 2008]). The program correctness properties are
given as reachability rules between matching patterns in K semantics rules. Internally, the verifier
uses the operational semantics to perform symbolic execution. Also, it has an internal matching
logic prover for reasoning about implication between patterns (states), which reduces to SMT
reasoning (refer to K verification infrastructure [Ştefănescu et al. 2016] for more details).
   For the verification, it is necessary to specify a pre- and post-condition similar to Hoare logic,
and loops need to be annotated with invariants. For simplicity, we show the verified properties
as a pair {Precondition}{Postcondition}, indicating that if the input of the program satisfies the
precondition then the result satisfies the postcondition. Thanks to the memory access check-
ing formalized in RustSEM, we can uniformly specify a memory property, such as data races,
buffer overflows, or borrowing errors, as {T rue}{¬stuck}, which means that for any input, the
program cannot get stuck. For other kinds of properties, such as functional properties, the pro-
gram should satisfy both the memory guarantees of RustSEM and the properties being specified.

   Table 3 shows the verification results of                   Table 3. Results for formal verification
a number of programs verified in RustSEM
using the K verifier, where LOC, Time(s)                     Programs              LOC Time(s) Mem(KB)
and Mem(KB) denote the lines of code, ex-                     sum(N )                15       44.65        698240
ecution time, and memory consumption,                       sumvec(V )               18       63.92       1470880
respectively. “sum(N )" is a function that           insertion_sort(V )              43      125.43       8736592
computes the sum from 1 to the input                      polymorphism               60       42.20        678992
N , verifying {N ≥ 1}{N × (N + 1)/2}.                         closure                22       36.45        663268
“sumvec(V )" computes the sum of all el-                        trait                50       39.22        654672
ements in V , and we verify {[v 1 , . . . , vn ] ∈          concur-race              58       47.25        647328
                                                           concur-order              57       60.82       2931760
                                                                   new                        76.90       1160640
                                Proc. ACM Program. Lang.,          push_front
                                                          Vol. 1, No. CONF, Article 210      115.33       1667140
                                                                                    1. Publication date: January 2018.
                                                    VecDeque
                                                                   push_back                 140.70       2025244
                                                                   reserve                     85         1859304
1:22                                            Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


vec<i32>}{Σ1≤i ≤nvi }, with the precondi-
tion being a vector of n random integers,
and the postcondition the sum of its ele-
ments. “insertion_sort" implements an
insertion sort algorithm, where we verify
{V ∈ vec<i32>}{V ′ ∈ vec<i32> s.t . sameElem(V , V ′)∧order(V ′)}. The precondition is an integer
vector and the postcondition is new vector with the same elements (checked by sameElem) and the
vector is ordered (checked by order). The program “concur-race" is a multi-threaded program
with a data race bug where we verify {T rue}{¬stuck}, that is the program finishes without going
into a stuck state. The program has a data race, and the verification can successfully detect it, going
to a stuck state thanks to the invalid access checking in the memory model, hence the property is
invalid. The program “concur-order" is a multi-thread program without data races. The property
is the same as for “concur-race". The verifier explores all possible interleavings in the concurrent
programs to detect bugs. In RustSEM, we optimized the semantics to allow interleaving only if the
rules access some shared resources.
   The program “VecDeque" is a module from the Rust standard library, for which a previous
version [issue 44800 2017] contained a bug. We verify this old version implementation of VecDeque
to rediscover the error by verifying the functions new, push_front, push_back, and reserve. The
property is: {0 ≤ head < cap ∧ 0 ≤ tail < cap}{0 ≤ head′ < cap′ ∧ 0 ≤ tail′ < cap′ }.
VecDeque has a head to indicate the memory location for push_front and and a tail to indicate
the memory location for push_back. The variable cap is the capacity of the VecDeque. The property
requires that the head and tail of a VecDeque have to be within the range [0, cap) before and after
executing any of its methods. The primed variables denote the variables’ values after executing
the methods. The bug [issue 44800 2017] can be rediscovered by RustSEM in the method reserve
resulting in a buffer overflow. RustSEM does not support infinite heap structure specification and
verification now. For the verification we use an approach similar to bounded model checking,
setting a bound in the maximum capacity of vecDeque to 16, limiting the state space exploration.
The benchmarks polymorphism, closure, and trait are programs using polymorphism, closures,
and traits, respectively and we verify some functional properties.
   Now, we discuss the limitations of formal verification. Firstly, the property specification language
in K needs to specify pre- and post-conditions and loop invariants for each memory locations,
which needs a lot of efforts. We only give an abstract description of the properties being verified
here. More details of specification languages could be found in K verification infrastructure [Ştefă-
nescu et al. 2016]. Secondly, we cannot specify infinite heap data structures, such as trees. K has
the capability to reason about infinite heap data structures, such as binary search trees, which is
shown in K verification infrastructure [Ştefănescu et al. 2016]. The challenge is that K verifica-
tion infrastructure uses a memory model different from RustSEM, as RustSEM incorporates OBS.
Therefore, we cannot directly inherit the framework from it. Actually, more work needs to be done
to define a language that could be used to inductively define infinite data structures in RustSEM.
One solution is to discover the relations between RustSEM’s memory model and separation logic
[Ishtiaq and O’Hearn 2001][Reynolds 2002]. In this paper, we focus on the semantics of Rust. A
more user-friendly and powerful verifier is our future work.

7   RELATED WORK
   Rust semantics. Table 4 compares the existing semantics for Rust on their target languages
(lang), the support of major features including safe and unsafe constructs, concurrency (concur),
dynamic OBS (D-OBS) and type system, as well as their verification capabilities, i.e., whether
support automated verification (AV) and machine-checked manual verification (MV).

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                     1:23


                           Table 4. The comparison with related semantics works

                                                                      features                         Verification
                                          lang

                                                                                                               !
                                                     safe   unsafe    type D-OBS         concur        AV     MV
  RustBelt [Jung et al. 2018a]          λ Rust     #
                                                   H          #
                                                              H
  Patina [Reed 2015]                  old Rust     #
                                                   H                    #
                                                                        H
                                                   #
                                                   H                    #
                                                                        H
                                                                                                       !
  Oxide [Weiss et al. 2019]             Oxide
                                                   #
                                                   H
                                                                                                       !
  KRust [Wang et al. 2018]               Rust
                                     core-lang #   H                    #
                                                                        H
                                                                                                       !
  K-Rust[Kan et al. 2018]
  RustSEM                                Rust
                                 #
                                 H partially supported             fully supported



   RustSEM and KRust are the only two that directly formalize the Rust language, whereas all the
remaining semantics, i.e., RustBelt, Oxide, Patina and K-Rust, formalizes either a variant or an
outdated version of Rust.
   RustSEM covers more major features than exiting semantics. Indeed, RustSEM fully supports
both safe and unsafe constructs and concurrency. In contrast, existing semantics only partially
supports them. For instance, RustBelt does not formalize some advanced features such as trait
objects, as it is for a variant of Rust, while Oxide, Patina, K-Rust and KRust only support a subset
of safe constructs without concurrency. Furthermore, RustSEM is the only one supporting dynamic
OBS. RustSEM focuses the operational semantics of OBS, thus the type system is not included.
   RustSEM, K-Rust and KRust can be used for automated verification. Although RustBelt, im-
plemented in the Coq theorem prover, can verify λ Rust programs using Coq, the verification
is interactive and needs expertise and manual inspection. Patina and Oxide have not yet been
implemented in any tool. Thus they provide neither automated nor machine-checked verification.

   Rust verification. CRust [Toman et al. 2015], SMACK-Rust [Baranowski et al. 2018] and Viper-
based Prusti [Astrauskas et al. 2019] can verify Rust programs by translating them into the input
languages of existing verification tools, instead of building formal semantics for Rust. For instance,
SMACK-Rust compiles Rust programs into the LLVM code which can be verified by SMACK [Carter
et al. 2016]. Prusti translates a subset of safe constructs to the intermediate language of Viper
[Müller et al. 2016] to construct core proofs. Note that these tools cover less features than RustSEM.
   Stackborrow [Jung et al. 2020] presents an alias model to regulate the use of unsafe pointers,
and checks borrowings by creating a stack for each memory location, instead of explicitly using
lifetimes. Moreover, Stackborrow does not support concurrency. Stackborrow is implemented in
Miri [Olson 2016], which is not a formal implementation.

   Ownership and Borrowing. The concept of ownership has been proposed for many years
and most of related works exploit type systems to enforce various ownership disciplines. Cyclone
[Jim et al. 2002] is designed to be a safe dialect of the C language by using region based memory
management [Tofte and Talpin 1994]. Mezzo [Balabonski et al. 2016] and Alms [Tov and Pucella
2011] follow ML-tradition and employ substructural type systems for managing ownership. There
are also many type systems associating reading and writing permissions to aliases [Boyland et al.
2001], such as Mezzo [Balabonski et al. 2016], Pony [Clebsch et al. 2015] and AEminium [Stork
et al. 2014]. All these works have different technique details with Rust and exploit types systems to
enforce memory safety. Our work aims at explaining the techniques of Rust from an operational
aspects instead of type systems in order to provide a new insight of OBS.

                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:24                                                Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


8      CONCLUSION
We have proposed a high-level abstraction of OBS and an executable operational semantics for Rust.
Compared with existing works, it covers a larger subset of the major language features of Rust. The
core of the semantics is the memory model with the operational semantics of OBS, which can be
potentially reused by other languages to improve memory safety. We have proved the refinement
relation between the high-level abstraction of OBS and the operational semantics in the memory
model. Moreover, we proposed a technique for testing semantic consistency in order to detect
semantic ambiguities and provide completely correct semantics. We have shown that RustSEM can
be applied in automated runtime and formal verification.
   As future works, we are working on two directions. The first one is to extend the verification
infrastructure of K to support infinite heap structure verification for the memory model of RustSEM.
The second one is to reuse our memory model for the K semantics of the C programming language
to improve C memory safety by checking the preservation of the OBS invariants.

REFERENCES
V. Astrauskas, P. Müller, F. Poli, and A. J. Summers. 2019. Leveraging Rust Types for Modular Specification and Verification.
   In to appear in Object-Oriented Programming Systems, Languages, and Applications (OOPSLA). ACM. https://doi.org/10.
   1145/3360573
Thibaut Balabonski, François Pottier, and Jonathan Protzenko. 2016. The Design and Formalization of Mezzo, a Permission-
   Based Programming Language. ACM Trans. Program. Lang. Syst. 38, 4 (2016), 14:1–14:94. http://dl.acm.org/citation.cfm?
   id=2837022
Marek S. Baranowski, Shaobo He, and Zvonimir Rakamaric. 2018. Verifying Rust Programs with SMACK. In Automated
   Technology for Verification and Analysis - 16th International Symposium, ATVA 2018, Los Angeles, CA, USA, October 7-10,
   2018, Proceedings (Lecture Notes in Computer Science), Shuvendu K. Lahiri and Chao Wang (Eds.), Vol. 11138. Springer,
   528–535. https://doi.org/10.1007/978-3-030-01090-4_32
Denis Bogdănaş and Grigore Roşu. 2015. K-Java: A Complete Semantics of Java. In Proceedings of the 42nd Symposium on
   Principles of Programming Languages (POPL’15). ACM, 445–456. https://doi.org/10.1145/2676726.2676982
John Boyland, James Noble, and William Retert. 2001. Capabilities for Sharing: A Generalisation of Uniqueness and
   Read-Only. In ECOOP 2001 - Object-Oriented Programming, 15th European Conference, Budapest, Hungary, June 18-
   22, 2001, Proceedings (Lecture Notes in Computer Science), Jørgen Lindskov Knudsen (Ed.), Vol. 2072. Springer, 2–27.
   https://doi.org/10.1007/3-540-45337-7_2
Montgomery Carter, Shaobo He, Jonathan Whitaker, Zvonimir Rakamaric, and Michael Emmi. 2016. SMACK software
   verification toolchain. In Proceedings of the 38th International Conference on Software Engineering, ICSE 2016, Austin, TX,
   USA, May 14-22, 2016 - Companion Volume, Laura K. Dillon, Willem Visser, and Laurie Williams (Eds.). ACM, 589–592.
   https://doi.org/10.1145/2889160.2889163
Zhe Chen, Junqi Yan, Shuanglong Kan, Ju Qian, and Jingling Xue. 2019. Detecting memory errors at runtime with
   source-level instrumentation. In Proceedings of the 28th ACM SIGSOFT International Symposium on Software Testing
   and Analysis, ISSTA 2019, Beijing, China, July 15-19, 2019., Dongmei Zhang and Anders Møller (Eds.). ACM, 341–351.
   https://doi.org/10.1145/3293882.3330581
Sylvan Clebsch, Sophia Drossopoulou, Sebastian Blessing, and Andy McNeil. 2015. Deny capabilities for safe, fast actors. In
   Proceedings of the 5th International Workshop on Programming Based on Actors, Agents, and Decentralized Control, AGERE!
   2015, Pittsburgh, PA, USA, October 26, 2015, Elisa Gonzalez Boix, Philipp Haller, Alessandro Ricci, and Carlos Varela (Eds.).
   ACM, 1–12. https://doi.org/10.1145/2824815.2824816
Andrei Ştefănescu, Daejun Park, Shijiao Yuwen, Yilong Li, and Grigore Roşu. 2016. Semantics-Based Program Verifiers for All
   Languages. In Proceedings of the 31th Conference on Object-Oriented Programming, Systems, Languages, and Applications
   (OOPSLA’16). ACM, 74–91. https://doi.org/10.1145/2983990.2984027
Sergey "Shnatsel" Davidoff. 2018. How RustâĂŹs standard library was vulnerable for years and nobody noticed. https:
   //medium.com/@shnatsel/how-rusts-standard-library-was-vulnerable-for-years-and-nobody-noticed-aebf0503c3d6.
Leonardo Mendonça de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Tools and Algorithms for the
   Construction and Analysis of Systems, 14th International Conference, TACAS 2008, Held as Part of the Joint European
   Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings
   (Lecture Notes in Computer Science), C. R. Ramakrishnan and Jakob Rehof (Eds.), Vol. 4963. Springer, 337–340. https:
   //doi.org/10.1007/978-3-540-78800-3_24


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                       1:25


Chucky Ellison and Grigore Rosu. 2012. An Executable Formal Semantics of C with Applications. In Proceedings of the
   39th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL’12). ACM, 533–544. https:
   //doi.org/10.1145/2103656.2103719
Chris Hathhorn, Chucky Ellison, and Grigore Roşu. 2015. Defining the Undefinedness of C. In Proceedings of the 36th
   ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI’15). ACM, 336–345. https:
   //doi.org/10.1145/2813885.2737979
Samin S. Ishtiaq and Peter W. O’Hearn. 2001. BI as an Assertion Language for Mutable Data Structures. In Conference Record
   of POPL 2001: The 28th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, London, UK, January
   17-19, 2001, Chris Hankin and Dave Schmidt (Eds.). ACM, 14–26. http://dl.acm.org/citation.cfm?id=360204
VecDeque issue 44800. 2017. https://github.com/rust-lang/rust/issues/44800.
Trevor Jim, J. Gregory Morrisett, Dan Grossman, Michael W. Hicks, James Cheney, and Yanling Wang. 2002. Cyclone: A Safe
   Dialect of C. In Proceedings of the General Track: 2002 USENIX Annual Technical Conference, June 10-15, 2002, Monterey,
   California, USA, Carla Schlatter Ellis (Ed.). USENIX, 275–288. http://www.usenix.org/publications/library/proceedings/
   usenix02/jim.html
Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2020. Stacked Borrows: An Aliasing Model for Rust. In to
   appear in POPL 2020. ACM.
Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2018a. RustBelt: Securing the Foundations of the
   Rust Programming Language. Proc. ACM Program. Lang. 2, POPL, Article (Jan. 2018). https://doi.org/10.1145/3158154
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018b. Iris from the
   ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
   https://doi.org/10.1017/S0956796818000151
Shuanglong Kan, David Sanán, Shang-Wei Lin, and Yang Liu. 2018. K-Rust: An Executable Formal Semantics for Rust. CoRR
   abs/1804.07608 (2018). arXiv:1804.07608 http://arxiv.org/abs/1804.07608
Niko Matsakis. 2016. Introducing MIR. https://blog.rust-lang.org/2016/04/19/MIR.html.
Niko Matsakis. 2017. Nested method calls via two-phase borrowing. http://smallcultfollowing.com/babysteps/blog/2017/03/
   01/nested-method-calls-via-two-phase-borrowing/.
Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A Verification Infrastructure for Permission-Based
   Reasoning. In Verification, Model Checking, and Abstract Interpretation - 17th International Conference, VMCAI 2016,
   St. Petersburg, FL, USA, January 17-19, 2016. Proceedings (Lecture Notes in Computer Science), Barbara Jobstmann and
   K. Rustan M. Leino (Eds.), Vol. 9583. Springer, 41–62. https://doi.org/10.1007/978-3-662-49122-5_2
Scott Olson. 2016. Miri. https://github.com/solson/miri.
Anton Podkopaev, Ori Lahav, and Viktor Vafeiadis. 2019. Bridging the gap between programming languages and hardware
   weak memory models. Proc. ACM Program. Lang. 3, POPL (2019), 69:1–69:31. https://doi.org/10.1145/3290382
Eric Reed. 2015. Patina: A Formalization of the Rust Programming Language. Technical Report. University of Washington.
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In 17th IEEE Symposium on Logic
   in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings. IEEE Computer Society, 55–74.
   https://doi.org/10.1109/LICS.2002.1029817
Grigore Roşu and Traian Florin Şerbănuţă. 2010. An Overview of the K Semantic Framework. Journal of Logic and Algebraic
   Programming 79, 6 (2010), 397–434. https://doi.org/10.1016/j.jlap.2010.03.012
Rust-Benchmark. 2020. Rust Benchmark. https://github.com/rust-lang/rust/tree/master/src/test.
Rust-Team. 2016. The Rust Language Homepage. https://www.rust-lang.org/en-US/.
Rust-Team. 2018. Non-lexical lifetimes. https://doc.rust-lang.org/edition-guide/rust-2018/ownership-and-lifetimes/non-
   lexical-lifetimes.html.
Rust-Team. 2018. The Rust Programming Language. Mozilla Research. https://doc.rust-lang.org/book/foreword.html.
Sven Stork, Karl Naden, Joshua Sunshine, Manuel Mohr, Alcides Fonseca, Paulo Marques, and Jonathan Aldrich. 2014.
   Æminium: a permission based concurrent-by-default programming language approach. In ACM SIGPLAN Conference on
   Programming Language Design and Implementation, PLDI ’14, Edinburgh, United Kingdom - June 09 - 11, 2014, Michael
   F. P. O’Boyle and Keshav Pingali (Eds.). ACM, 26. https://doi.org/10.1145/2594291.2594344
Mads Tofte and Jean-Pierre Talpin. 1994. Implementation of the Typed Call-by-Value lambda-Calculus using a Stack of
   Regions. In Conference Record of POPL’94: 21st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
   Portland, Oregon, USA, January 17-21, 1994, Hans-Juergen Boehm, Bernard Lang, and Daniel M. Yellin (Eds.). ACM Press,
   188–201. https://doi.org/10.1145/174675.177855
John Toman, Stuart Pernsteiner, and Emina Torlak. 2015. Crust: A Bounded Verifier for Rust (N). In 30th IEEE/ACM
   International Conference on Automated Software Engineering, ASE 2015, Lincoln, NE, USA, November 9-13, 2015, Myra B.
   Cohen, Lars Grunske, and Michael Whalen (Eds.). IEEE Computer Society, 75–80. https://doi.org/10.1109/ASE.2015.77
Jesse A. Tov and Riccardo Pucella. 2011. Practical affine types. In Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium
   on Principles of Programming Languages, POPL 2011, Austin, TX, USA, January 26-28, 2011, Thomas Ball and Mooly Sagiv


                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:26                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  m
                                 a                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    a1 … a2
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="ESi7EYfCyrdz3EDAm5k4AbPH0s4=">AAAB6nicbZDLSgMxFIbP1FttvVRddhMsgqsyUaguCy50WdFeoB1KJpNpQzOZIckIZegjuHGhFLe+ii/gzrcxvSy09YfAx/+fQ845fiK4Nq777eQ2Nre2d/K7heLe/sFh6ei4peNUUdaksYhVxyeaCS5Z03AjWCdRjES+YG1/dDPL209MaR7LRzNOmBeRgeQhp8RY64H0cb9UcavuXGgd8BIq9eLttPzZCRr90lcviGkaMWmoIFp3sZsYLyPKcCrYpNBLNUsIHZEB61qUJGLay+ajTtCZdQIUxso+adDc/d2RkUjrceTbyoiYoV7NZuZ/WTc14bWXcZmkhkm6+ChMBTIxmu2NAq4YNWJsgVDF7ayIDoki1NjrFOwR8OrK69C6qOLLKr7HlXoNFspDGU7hHDBcQR3uoAFNoDCAZ3iFN0c4L87UeV+U5pxlzwn8kfPxA6BSkEQ=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <latexit sha1_base64="M+YkODB1m+5I+m3KryttSKzyoL0=">AAAB6nicbZDLSgMxFIbP1FttvVRddhMsgqsyqaAuCy50WdFeoB1KJpNpQzOZIckIZegjuHGhFLe+ii/gzrcxvSy09YfAx/+fQ845fiK4Nq777eQ2Nre2d/K7heLe/sFh6ei4peNUUdaksYhVxyeaCS5Z03AjWCdRjES+YG1/dDPL209MaR7LRzNOmBeRgeQhp8RY64H0a/1Sxa26c6F1wEuo1Iu30/JnJ2j0S1+9IKZpxKShgmjdxW5ivIwow6lgk0Iv1SwhdEQGrGtRkohpL5uPOkFn1glQGCv7pEFz93dHRiKtx5FvKyNihno1m5n/Zd3UhNdexmWSGibp4qMwFcjEaLY3Crhi1IixBUIVt7MiOiSKUGOvU7BHwKsrr0OrVsUXVXyPK/VLWCgPZTiFc8BwBXW4gwY0gcIAnuEV3hzhvDhT531RmnOWPSfwR87HD6HWkEU=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          b
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              a3 b
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              <latexit sha1_base64="HSA1+9riaqlaeEVC2WzkTG5au/M=">AAAB6nicbZDLSgMxFIbP1FttvVRddhMsgqsysaAuCy50WdFeoB1KJpNpQzOZIckIZegjuHGhFLe+ii/gzrcxvSy09YfAx/+fQ845fiK4Nq777eQ2Nre2d/K7heLe/sFh6ei4peNUUdaksYhVxyeaCS5Z03AjWCdRjES+YG1/dDPL209MaR7LRzNOmBeRgeQhp8RY64H0a/1Sxa26c6F1wEuo1Iu30/JnJ2j0S1+9IKZpxKShgmjdxW5ivIwow6lgk0Iv1SwhdEQGrGtRkohpL5uPOkFn1glQGCv7pEFz93dHRiKtx5FvKyNihno1m5n/Zd3UhNdexmWSGibp4qMwFcjEaLY3Crhi1IixBUIVt7MiOiSKUGOvU7BHwKsrr0ProoprVXyPK/VLWCgPZTiFc8BwBXW4gwY0gcIAnuEV3hzhvDhT531RmnOWPSfwR87HD6NakEY=</latexit>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       …   b   x   o
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       B
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0   m                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   0
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               a01 … a2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   b
                                 a
                                 <latexit sha1_base64="/5PfXXzTgjk1x7o7xvwmfwOTwwA=">AAAB63icbZDLSgMxFIbP1Futt6orcRMsQt2UmQrqzoIblxXsBdqhZNJMG5pkhiQjlKGvoAsXirj1LVz5CO58EPeml4W2/hD4+P9zyDkniDnTxnW/nMzS8srqWnY9t7G5tb2T392r6yhRhNZIxCPVDLCmnElaM8xw2owVxSLgtBEMrsZ5444qzSJ5a4Yx9QXuSRYygo21AsDooJMvuCV3IrQI3gwKl+/F74+H9km1k/9sdyOSCCoN4VjrlufGxk+xMoxwOsq1E01jTAa4R1sWJRZU++lk1hE6tk4XhZGyTxo0cX93pFhoPRSBrRTY9PV8Njb/y1qJCS/8lMk4MVSS6UdhwpGJ0Hhx1GWKEsOHFjBRzM6KSB8rTIw9T84ewZtfeRHq5ZJ3WvJuvELlDKbKwiEcQRE8OIcKXEMVakCgD/fwBM+OcB6dF+d1WppxZj378EfO2w/mEpEs</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               <latexit sha1_base64="1emhRUXE+sJOYlPLsXv6L/IQwBg=">AAAB73icbZDLSgMxFIbP1Futt6ogiJtgEVyViYK6LLgpuKlgL9AOJZPJtKGZzJhkhDL0Jdy4UMSt7+LKnY/hG5heFtr6Q+Dj/88h5xw/EVwb1/1yckvLK6tr+fXCxubW9k5xd6+h41RRVqexiFXLJ5oJLlndcCNYK1GMRL5gTX9wPc6bD0xpHss7M0yYF5Ge5CGnxFgrAAJdwOiwWyy5ZXcitAh4BqXKQfXG+6DftW7xsxPENI2YNFQQrdvYTYyXEWU4FWxU6KSaJYQOSI+1LUoSMe1lk3lH6MQ6AQpjZZ80aOL+7shIpPUw8m1lRExfz2dj87+snZrwysu4TFLDJJ1+FKYCmRiNl0cBV4waMbRAqOJ2VkT7RBFq7IkK9gh4fuVFaJyV8XkZ3+JS5QKmysMRHMMpYLiEClShBnWgIOARnuHFuXeenFfnbVqac2Y9+/BHzvsPmNyRWg==</latexit>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                <latexit sha1_base64="k4x58wIDW8ZI3Lb3ULG46D3HGNI=">AAAB73icbZDLSgMxFIbPeK31VhUEcRMsgqsyU0FdFtwU3FSwF2iHkslk2tBMMiYZoQx9CTcuFHHru7hy52P4BqaXhbb+EPj4/3PIOSdIONPGdb+cpeWV1bX13EZ+c2t7Z7ewt9/QMlWE1onkUrUCrClngtYNM5y2EkVxHHDaDAbX47z5QJVmUtyZYUL9GPcEixjBxlohYOhCGR11C0W35E6EFsGbQbFyWL3xP8h3rVv47ISSpDEVhnCsddtzE+NnWBlGOB3lO6mmCSYD3KNtiwLHVPvZZN4ROrVOiCKp7BMGTdzfHRmOtR7Gga2Msenr+Wxs/pe1UxNd+RkTSWqoINOPopQjI9F4eRQyRYnhQwuYKGZnRaSPFSbGnihvj+DNr7wIjXLJOy95t16xcgFT5eAYTuAMPLiEClShBnUgwOERnuHFuXeenFfnbVq65Mx6DuCPnPcfmmKRWw==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Fig. 5. The proof idea of Theorem 3.6


   (Eds.). ACM, 447–458. https://doi.org/10.1145/1926385.1926436
Feng Wang, Fu Song, Min Zhang, Xiaoran Zhu, and Jun Zhang. 2018. KRust: A Formal Executable Semantics of Rust. CoRR
   abs/1804.10806 (2018). arXiv:1804.10806 http://arxiv.org/abs/1804.10806
Aaron Weiss, Daniel Patterson, Nicholas D. Matsakis, and Amal Ahmed. 2019. Oxide: The Essence of Rust. CoRR
   abs/1903.00982 (2019). arXiv:1903.00982 http://arxiv.org/abs/1903.00982

A      PROOF OF LEMMA 3.4
    Proof. Assume there is a cycle in a well-formed OBS graph, there must exist a →b a ′ and a ′ →b
a 1 . . . a 2 →b a. We can infer that F (a →b a ′) ⊂ F (a 2 →b a) and F (a 2 →b a) ⊂ F (a →b a ′) by
the condition (2) of Definition 3.3, which cannot be true,
                                                                                                   □

B      PROOF OF THEOREM 3.6
   Proof. This theorem specifies that exclusive mutation guarantee are maintained in a well-formed
OBS graph with respect to the permission functions.
   If the owner and all references are shared aliases then the theorem is trivially proved. If there is
a mutable alias enabled at the timestamp t then it is proved by two cases.
   Case 1: Assume the owner is the mutable alias. We can infer that there is no reference that has
the writing or reading permission to the memory location at t. Otherwise the reference should
disable the owner according to the definition of the permission functions and the unique owner
invariant of well-formed OBS graphs.
   Case 2: Assume there is a mutable reference a to the memory block enabled at t, and the owner
of the memory block is x, we have that there exists a link a →m a 1 . . . x →o B. The owner and
all other references in the link should be disabled by a and thus their writing permissions are not
enabled.
   Now assume there is another reference a ′ , a enabled at t. It should not be in the link from a
to x. We have that there exists another link a ′ →m a 1′ . . . x→o B. Then there must exists a 2 , a 2′ , a 3
such that a →m a 1 . . . a 2 →b a 3 . . . x →o B and a ′ →m a 1′ . . . a 2′ →b a 3 . . . x →o B (See Fig.
5). According to Invariant (3) of the definition for well-formed OBS graphs (Definition 3.3), the
lifetimes of a 2 →b a 3 and a 2′ →b a 3 should not intersect. According to Invariant (2) of Definition
3.3, the lifetime of a →m a 1 should be within the lifetime of a 2 →b a 3 and the lifetime of a ′ →m a 1′
should be within the lifetime of a 2′ →b a 3 . Thus the lifetimes of a →m a 1 and a ′ →m a 1′ cannot
intersect. Therefore the lifetime of a ′ →m a 1′ does not contain the current timestamp t and a ′ is
not permitted to write.                                                                                    □

C      PROOF OF THEOREM 4.4
The first claim that G is a well-formed OBS graph is proved by Lemma C.1 and C.3. Lemma C.1
proves that each memory configuration in a safe sequence is a well-formed configuration and
Lemma C.3 proves the lifetime inclusion variant for well-formed configurations. The second claim
is proved by Lemma C.4 and C.5.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
An Executable Operational Semantics for Rust with the Formalization of Ownership and Borrowing                   1:27


   Lemma C.1. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be a
safe sequence. Then all memi , 0 ≤ i ≤ n, are well-formed.
  Proof. Since m 0 is an empty configuration, it is trivially well-formed. The allocation operation
does not change the well-formedness of a memory layout. The free operation also does not change
the well-formedness of a memory configuration, since it only removes a block from the heap.
For reading and writing operations, the semantics rules always ensure the resulting memory
configurations are well-formed.                                                                   □
   Lemma C.2. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be a
safe sequence. Let memi , 0 ≤ i ≤ n be a memory configuration.. We have:
  (1) For any a →s a′ ∈ memi , there is no writing by a′ during the lifetime of a in memi .
  (2) For any a →m a′ ∈ memi , there is no reading or writing by a′ during the lifetime of a in memi .
  Proof. We first prove the claim (1). Assume a’s lifetime is tsb ∼ tse in memi (i.e., L(a, memi ) =
tsb ∼ tse ) and ts is a timestamp at which a′ is used to write and ts ∈ tsb ∼ tse .
  The writing by a′ at ts should not be the latest writing in memi , that is, if memi = (S, H, P, ms)
and P(a′) = (_, ts′) then ts , ts′, otherwise it should be disabled according to Definition 4.1.
Therefore we have ts′ > tse .
  Without loss of generality, we assume there is no writing by a′ during ts ∼ tse . Then we have
that the memory configuration memk in (memk , tsk ) with tsk = tse is not a well-formed memory
configuration as the writing by a′ at ts is the lasting writing by a′ in memk but the lifetime of a in
memk is tsb ∼ tse . The writing should be disabled according to Definition 4.1. This contradicts to
Lemma C.2.                                                                                           □
  Lemma C.3. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be a
safe sequence. Let memi , 0 ≤ i ≤ n be a memory configuration and B be a block with the location b.
Let the OBS graph of B in memi be G = (V , B, E, F ). We have that G is well-formed.
   Proof. From Lemma C.1, memi is well-formed, which ensures that G satisfies the unique owner
invariant and no intersection invariant. We still need to prove the lifetime inclusion invariant.
   For references, according the definition of L(a, mem), we know that the lifetime of a will always
include the lifetime of a′, where a′ →b∗ a ∈ mem.
   We need to consider the owner. If an owner’s writing permission is always disabled by its
references then the ownership cannot be moved. In this case, its lifetime always includes it’s
references’ lifetimes. From Lemma C.2, we know that the owner is always disabled.                 □
   Lemma C.4. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be a
safe sequence. Let G = (V , B, E, F ) be the OBS graph of B in memi , 0 ≤ i ≤ n, we have for any two
nodes a, a ′ ∈ V ∪ {B}, if a reading operation read(p), where alias(p) = a, is carried out at the
timestamp ts ∈ F (a →∗ a ′) then RG (a, ts) = true.
  Proof. The key to prove the lemma is to ensure that during the lifetime of a, the reading by a at
ts is not disabled. Actually it is proved by Lemma C.2.
                                                                                                 □
   Lemma C.5. Let π = (mem 0 , ts0 ), op1 , (mem 1 , ts1 ), . . . , (memn−1 , tsn−1 ), opn , (memn , tsn ) be a
safe sequence. Let G = (V , B, E, F ) be the OBS graph of B in memi , 0 ≤ i ≤ n, we have for any two
nodes a, a ′ ∈ V ∪ {B}, if a writing operation write(p, v), where alias(p) = a, is carried out at the
timestamp ts ∈ F (a →∗ a ′) then WG (a, ts) = true.
  Proof. Proof is similar to Lemma C.4.                                                                            □

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:28                                            Shuanglong Kan, Zhe Chen, David Sanán, Shang-wei Lin, and Yang Liu


   Theorem 4.4 is proved by Lemma C.1, C.3, C.4, and C.5.




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
