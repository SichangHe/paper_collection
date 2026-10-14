                                          Towards verifying unsafe Rust programs against
                                                Rust’s pointer-aliasing restrictions

                                          Wannes Tas1 [0009-0008-5519-761X] and Bart Jacobs1 [0000-0002-3605-249X]

                                                         Department of Computer Science, Leuven, Belgium
                                                                firstname.lastname@kuleuven.be
arXiv:2603.28326v1 [cs.PL] 30 Mar 2026




                                               Abstract. The Rust programming language is famous for its strong
                                               ownership regime: at each point, each value is either exclusively owned,
                                               exclusively borrowed through a mutable reference, or borrowed as read-
                                               only through one or more shared references. These rules, known as Rust’s
                                               pointer-aliasing rules, are exploited by the Rust compiler to generate
                                               more efficient machine code, and enforced by Rust’s static type sys-
                                               tem, except inside unsafe blocks. In this paper, we present our work
                                               in progress towards the first program logic for modularly verifying that
                                               Rust programs that use unsafe blocks comply with the pointer-aliasing
                                               rules.

                                               Keywords: Rust · Formal verification · Pointer-aliasing



                                         1   Introduction

                                         The Rust programming language is famous for its strong ownership regime: at
                                         each point, each value is either exclusively owned, exclusively borrowed through
                                         a mutable reference, or borrowed as read-only through one or more shared refer-
                                         ences. These rules, known as Rust’s pointer-aliasing rules, are exploited by the
                                         Rust compiler to generate more efficient machine code, and enforced by Rust’s
                                         static type system, except inside unsafe blocks. An example of a program that
                                         does not comply with Rust’s aliasing restrictions can be found in Listing 1 (L).
                                         The compiler should reject the second attempt to write through y, as the lifetime
                                         of y would have to be ended to write through x in the line before it. In order to
                                         verify that code in unsafe blocks is also compliant with Rust’s pointer-aliasing
                                         rules, external tools and techniques are needed. To this end, we present our work
                                         in progress towards the first program logic capable of modularly verifying that
                                         Rust programs using unsafe blocks are compliant with the pointer-aliasing rules.
                                             As verifying arbitrary programs written in Rust’s full surface syntax would
                                         be quite cumbersome, a smaller toy language is introduced in §2, which should
                                         be sufficient to convey the core ideas. Afterwards in §3, we present our program
                                         logic. Finally, a number of planned extensions of the program logic are discussed
                                         in §4, along with the most important related work.
2              Wannes Tas and Bart Jacobs


    1 let mut x = 42;                                1 let x = new(42) in
    2 let y = &mut x as *mut i32;                    2 let y = &mut *x in
    3 unsafe { *y = 43; }                            3 *y := 43;

    4 x = 44;                                        4 *x := 44;

    5 unsafe { *y = 5; } // UB!                      5 *y := 5



Listings 1. An example of a Rust program that does not satisfy Rust’s pointer-aliasing
restrictions (L), and its translation to λPA (R).


        pr ∈     Provenances        ≜    OwningProv ∪ MutRefProv ∪ SharedRefProv
         p∈      Pointers          ::=   {prov : Provenance, address : N}
    pown ∈       OwningPointers     ≜    {p | p.prov ∈ OwningProv }
    p&mut ∈      MutRefs            ≜    {p | p.prov ∈ MutRefProv }
        p& ∈     SharedRefs         ≜    {p | p.prov ∈ SharedRefProv }
         v∈      Values            ::=   p | z                                       z∈Z
         x∈      Variables
         ε∈      PureExprs         ::=   v | x
         e∈      Exprs             ::=   v | new(ε) | free(ε) | &*ε | &mut *ε | *ε
                                     |   *ε := v | let x := e1 in e2 | e1 ; e2

                   Fig. 1. The λPA syntax, inspired by λRust [6] and λTB [11].


2        The mini-language λPA

We define a minimal language that captures the essence of pointer-aliasing in
Rust: λPA . The full syntax of λPA can be found in Figure 1. While only the
address is retained at run time, compilers take into account a pointer’s prove-
nance [14] for optimisations; hence our logic must account for it. For instance a
pointer x points to the same memory as a borrow like &x or &mut x, but each
would have a different provenance, since it consists, among other information,
of the mutability permisions of the pointer. Note that e1 ; e2 is just syntactic
sugar for let _ := e1 in e2 . Separate operational semantics for λPA are not
provided, but the proof rules of the program logic introduced in the next section
serve as axiomatic semantics.


3        The program logic

We define the assertions of our logic semantically as predicates over fractional
heaps (fractional multisets of resources). When it is clear from context whether
                                                                                1
the assertion or the resource is meant, p 7→ v will be used as shorthand for p 7→ v,
                                     1
and p′ ⇑ p as shorthand for p′ ⇑ p. We define the correctness judgment inductively
by the proof rules shown.
          Towards verifying Rust programs against pointer-aliasing restrictions                        3

       Resources      r            ::=    p 7→ v | p1 ⇑ p2
       Heaps          h             ∈     Resources → [0, 1]
       Assertions     a             ∈     P(Heaps)
                      a1 ∗ a2       ≜     {h | ∃h1 ∈ a1 , h2 ∈ a2 . h1 + h2 = h}
                      emp           ≜     {λr. 0}
                      ownq r        ≜     {(λr′ . 0)[r := q]}                                  q ∈ (0, 1]
                         q
                      p 7→ v       ≜      ownq p 7→ v
                         q
                      p′ ⇑ p       ≜      ownq p′ ⇑ p

                    H-frame                                  H-exists
                         {P } e {Q}                          ∀x. { P (x) } e { Q }
                     {R ∗ P } e {Q ∗ R}                      { ∃x. P (x) } e { Q }



                                                                      free
      new                                                                p ∈ OwningPointers
      { emp } new(v) { r. r 7→ v ∗ r ∈ OwningPointers }
                                                                      { p 7→ v } free(p) { emp }

             write                                       read
                                                             q                 q
             { p 7→ vo } *p := v { p 7→ v }              { p 7→ v } *p { r. p 7→ v ∗ r = v }

                         let
                         { P } e1 { r. R(r) }    ∀v.{ R(v) } e2 [v/x] { Q }
                                   { P } let x := e1 in e2 { Q }


Above definitions and proof rules introduce a fairly straightforward separation
logic [10, 12] with a fractional heap [3, 2]. The more interesting proof rules,
namely those for mutable and shared borrows, are given separately in the follow-
ing two subsections. These proof rules are each introduced alongside an example
program with proof outline.


3.1     Mutable references



              mutable-borrow
              { p 7→ v } &mut *p { r. r 7→ v ∗ r ⇑ p }
                                                                           1 let x := new(42) in
                                                                           2 { x 7→ 42 }
    Creating a mutable reference in our language re-                       3 let y := &mut *x in

quires the full points-to resource of the lending ref-                     4 { y 7→ 42 ∗ y ⇑ x }

erence, and produces a full points-to resource to the                      5 *y := 43;

                                                                           6 { y 7→ 43 ∗ y ⇑ x }
same memory for the borrowing pointer. Addition-
                                                                           7 ⇛{ x 7→ 43 }
ally, a reference-ending resource is produced to allow
                                                                           8 *x := 44;
the proof author to transfer (full or partial) ownership
                                                                           9 { x 7→ 44 }
of the memory from the borrowing reference back to
                                                                          10 free(x)
the lending reference, using a view shift [8]:
4        Wannes Tas and Bart Jacobs

    H-view-shift-consequence                         VS-transitive                   VS-frame
    P ⇛ P′     {P′ } e {Q}          Q ⇛ Q′           P ⇛R           R⇛Q                P ⇛Q
               { P } e { Q′ }                                   P ⇛Q                 R∗P ⇛ Q∗R

                     VS-subset                           reference-end
                     P ⊆Q                                   q        q        q
                     P ⇛Q                                p′ 7→ v ∗ p′ ⇑ p ⇛ p 7→ v

Of course, the goal is for this to be sound with respect to Rust’s aliasing rules.
The Rust Reference states the following about mutable references1 : “&mut T must
point to memory that is not read or written by any pointer not derived from the
reference and that no other reference points to while they are live.” 2

3.2     Shared References

                            shared-borrow
                                                                       q
                                                 q              q
                                q                                      2
                                                   2        2
                            { p 7→ v } &*p { r. p 7→ v ∗ r 7→ v ∗ r ⇑p}

Creating a shared reference is somewhat similar to creating a mutable one, except
that the lending pointer only needs to have partial ownership of its memory, and
both the lending and borrowing references are read-only afterwards. This satisfies
Rust’s aliasing rules for shared pointers, which are as follows3 : “&T must point
to memory that is not mutated while they are live (except for data inside an
UnsafeCell<U>)” 4 . Given that shared-borrow only gives partial ownership to
the lending pointer, and offers no way to acquire full ownership, it can never be
possible to apply write using this pointer, and thus mutation is not possible
while the shared reference is live. Note that in the current system only the
memory directly behind a shared reference is immutable; memory that can be
reached transitively through the reference is not. See §4 for more on this.

    1 let x := new(42) in
    2 { x 7→ 42 }
    3 let y := &*x in
                                      1
          1             1             2
           2          2
    4 { x 7→ 42 ∗ (y 7→ 42 ∗ y ⇑ x) }
    5 let z := &*x in
                                      1                              1
          1             1             2              1               4
           4          2                   4
    6 { x 7→ 42 ∗ (y 7→ 42 ∗ y ⇑ x) ∗ (z 7→ 42 ∗ z ⇑ x)}
    7 *y;




1
  https://doc.rust-lang.org/reference/behavior-considered-undefined.html#r-
  undefined.alias
2
  Interpreted literally, a choice of q ̸= 1 in reference-end would not be allowed by
  the Rust Reference. On the other hand, p′ can never be mutated again, and Tree
  Borrows [16] allows it, so it is unclear whether this is actually an issue or not.
3
  https://doc.rust-lang.org/reference/behavior-considered-undefined.html#r-
  undefined.alias
4
  UnsafeCell<T> is not yet considered in our program logic, see §4.
          Towards verifying Rust programs against pointer-aliasing restrictions       5

                                    1
            3            1          4
          4           4
   ⇛{ x 7→
    8        42 ∗ (z 7→ 42 ∗ z ⇑ x)}
 9 *z;

10 ⇛{ x 7→ 42 }

11 *x := 43

12 { x 7→ 43 }

13 free(x)




4       Conclusion
In this paper we propose a logic that captures the core of Rust’s pointer aliasing
rules. In a technical report [13], we present an extended version of our logic that
additionally supports two-phase borrowing [16], and the following features:

Functions Rust’s aliasing rules note an extra constraint for references that are
passed as function arguments: “When a reference (but not a Box!) is passed to a
function, it is live at least as long as that function call, again except if the &T con-
tains an UnsafeCell<U>.” Additionally, it must be verified on function entrance
that mutable reference arguments are not aliasing, which is not guaranteed by
Rust in the presence of unsafe code at the call-site. To this end, we reborrow mu-
table references on function entrance, and make the reference-ending resources
of reference arguments inaccessible for the duration of the function call.

Interior Mutability While in most cases the memory behind a shared refer-
ence should be immutable, sometimes it is desirable to allow mutation through
shared references, e.g. so multiple threads can mutate some shared memory. For
this reason Rust has the type UnsafeCell<T>, which is in essence just the type
T except for the fact that it can be mutated through shared pointers. In or-
der to integrate this feature into the proposed logic, care must be taken such
that taking a mutable or shared borrow of a type that contains or points to an
UnsafeCell<T>, always leaves the full points-to resource intact.

Boxes According to Rust’s aliasing rules, Box<T> should be treated similarly
to a &’static mut T for aliasing purposes, except for the fact that a Box passed
as a function argument is not required to remain live for the duration of the
function execution.
    Additionally, the following extensions are left as future work:

Structs Another important feature that is currently missing is the ability
to define and use structs. One significant aspect of structs is that it allows pro-
grammers to introduce abstractions, so that client code can use e.g. a Coordinate
struct without having to worry about its internal workings. Similarly, an addition
of structs to our program logic should allow modular reasoning and verification
of client code against a separately verified specification of that struct, rather
than worrying about its internals.
6        Wannes Tas and Bart Jacobs

Recursive Freezing In the current version of our logic, it is possible to write
through a pointer of type &&mut T by first reading from it to get a pointer of type
&mut T, and then writing through that one. However, the Rust Reference states
the following: “Moreover, the bytes pointed to by a shared reference, including
transitively through other references (both shared and mutable) and Boxes, are
immutable; transitivity includes those references stored in fields of compound
types.” To support this concept, the creation of a shared reference could re-
cursively freeze all memory behind it so that all transitively reachable memory
becomes read-only. Note that Tree Borrows5 does not require recursive freezing,
so it seems quite likely that this requirement might be relaxed in the future.
    Lastly, we plan on validating the logic extensively, by implementing it in
the VeriFast [5] tool for separation-logic-based modular formal verification of
Rust programs and proving compliance of some real world Rust programs, and
by proving soundness of the logic with respect to some formal model of Rust’s
aliasing rules like Tree Borrows.


4.1     Related Work

We are not aware of any existing logic for modularly verifying compliance with
Rust’s pointer aliasing rules. As far as we are aware, existing approaches for
modularly verifying unsafe Rust code, such as RefinedRust [4], Verus [9], and
Gillian-Rust [1], ignore these rules and are therefore unsound. Some non-modular
tools, however, like testing tool Miri [7] and bounded model checker Kani [15]
do check these rules to some extent.


Tree Borrows The official pointer-aliasing rules currently have two relevant
issues: they are not formally defined, so at best our program logic verifies com-
pliance with our interpretation of the aliasing rules, and secondly they are not
final. The current aliasing rules are an overapproximation of what the final offi-
cial aliasing rules will be, and are likely to be relaxed in some ways eventually.
A few candidate formal proposals for these have been made so far. A recent
proposal that has gained some traction is Tree Borrows [16], which keeps track
of all references to some block in memory via a tree-structure, where each node
represents a pointer to (a part of) that memory. Each node is also equipped with
a state machine that tracks what operations (read/write) the pointer should al-
low. A separation logic to verify compliance with Tree Borrows is currently in
development [11].

Acknowledgments. This research was partially funded by the Research Fund KU
Leuven, and by the Cybersecurity Research Program Flanders.
    We would also like to thank Johannes Hostert and Ralf Jung for their insight and
helpful interactions.

Disclosure of Interests. None
5
    See §4.1
        Towards verifying Rust programs against pointer-aliasing restrictions          7

References
 1. Ayoun, S.É., Denis, X., Maksimović, P., Gardner, P.: A Hybrid Approach to Semi-
    automated Rust Verification. Artifact: A Hybrid Approach to Semi-automated
    Rust Verification 9(PLDI), 186:970–186:992 (Jun 2025). https://doi.org/10.1145/
    3729289, https://dl.acm.org/doi/10.1145/3729289
 2. Bornat, R., Calcagno, C., O’Hearn, P., Parkinson, M.: Permission accounting in
    separation logic. SIGPLAN Not. 40(1), 259–270 (Jan 2005). https://doi.org/10.
    1145/1047659.1040327, https://dl.acm.org/doi/10.1145/1047659.1040327
 3. Boyland, J.: Fractional Permissions. In: Clarke, D., Noble, J., Wrigstad, T.
    (eds.) Aliasing in Object-Oriented Programming. Types, Analysis and Verifica-
    tion, pp. 270–288. Springer, Berlin, Heidelberg (2013). https://doi.org/10.1007/
    978-3-642-36946-9_10, https://doi.org/10.1007/978-3-642-36946-9_10
 4. Gäher, L., Sammler, M., Jung, R., Krebbers, R., Dreyer, D.: RefinedRust: A
    Type System for High-Assurance Verification of Rust Programs. Artifact for "Re-
    finedRust: A Type System for High-Assurance Verification of Rust Programs"
    8(PLDI), 192:1115–192:1139 (Jun 2024). https://doi.org/10.1145/3656422, https:
    //dl.acm.org/doi/10.1145/3656422
 5. Jacobs, B., Vogels, F., Piessens, F.: Featherweight VeriFast. Logical Methods in
    Computer Science Volume 11, Issue 3 (Sep 2015). https://doi.org/10.2168/
    LMCS-11(3:19)2015, https://lmcs.episciences.org/1595
 6. Jung, R.: Understanding and evolving the Rust programming language. doctor-
    alThesis, Saarländische Universitäts- und Landesbibliothek (2020). https://doi.
    org/10.22028/D291-31946, https://publikationen.sulb.uni-saarland.de/handle/20.
    500.11880/29647, accepted: 2020-09-09T07:57:28Z
 7. Jung, R., Kimock, B., Poveda, C., Muñoz, E.S., Scherer, O., Wang, Q.: Miri:
    Practical Undefined Behavior Detection for Rust. Artifact for Miri: Practical
    Undefined Behavior Detection for Rust 10(POPL), 48:1383–48:1411 (Jan 2026).
    https://doi.org/10.1145/3776690, https://dl.acm.org/doi/10.1145/3776690
 8. Jung, R., Swasey, D., Sieczkowski, F., Svendsen, K., Turon, A., Birkedal, L., Dreyer,
    D.: Iris: Monoids and Invariants as an Orthogonal Basis for Concurrent Reason-
    ing. SIGPLAN Not. 50(1), 637–650 (Jan 2015). https://doi.org/10.1145/2775051.
    2676980, https://dl.acm.org/doi/10.1145/2775051.2676980
 9. Lattuada, A., Hance, T., Cho, C., Brun, M., Subasinghe, I., Zhou, Y., Howell,
    J., Parno, B., Hawblitzel, C.: Verus: Verifying Rust Programs using Linear Ghost
    Types. Software Artifact (virtual machine, pre-built distributions) for "Verus: Veri-
    fying Rust Programs using Linear Ghost Types" 7(OOPSLA1), 85:286–85:315 (Apr
    2023). https://doi.org/10.1145/3586037, https://dl.acm.org/doi/10.1145/3586037
10. O’Hearn, P., Reynolds, J., Yang, H.: Local Reasoning about Programs that Alter
    Data Structures. In: Fribourg, L. (ed.) Computer Science Logic. pp. 1–19. Springer,
    Berlin, Heidelberg (2001). https://doi.org/10.1007/3-540-44802-0_1
11. Peterson, R.: A Program Logic for Tree Borrows. Master’s thesis, ETH Zurich (Sep
    2025), http://rudynicolop.github.io/files/thesis.pdf
12. Reynolds, J.: Separation logic: a logic for shared mutable data structures. In: Pro-
    ceedings 17th Annual IEEE Symposium on Logic in Computer Science. pp. 55–
    74 (Jul 2002). https://doi.org/10.1109/LICS.2002.1029817, https://ieeexplore.ieee.
    org/document/1029817
13. Tas, W., Jacobs, B.: Towards verifying unsafe Rust programs against Rust’s
    pointer-aliasing restrictions: Technical Report (Mar 2026). https://doi.org/10.
    5281/ZENODO.19254887, https://zenodo.org/doi/10.5281/zenodo.19254887
8       Wannes Tas and Bart Jacobs

14. The Rust teams: std::ptr - Rust, https://doc.rust-lang.org/std/ptr/index.html#
    provenance
15. VanHattum, A., Schwartz-Narbonne, D., Chong, N., Sampson, A.: Verifying dy-
    namic trait objects in rust. In: Proceedings of the 44th International Confer-
    ence on Software Engineering: Software Engineering in Practice. pp. 321–330.
    ICSE-SEIP ’22, Association for Computing Machinery, New York, NY, USA (Oct
    2022). https://doi.org/10.1145/3510457.3513031, https://dl.acm.org/doi/10.1145/
    3510457.3513031
16. Villani, N., Hostert, J., Dreyer, D., Jung, R.: Tree Borrows. Tree Borrows – Artifact
    9(PLDI), 188:1019–188:1042 (Jun 2025). https://doi.org/10.1145/3735592, https:
    //dl.acm.org/doi/10.1145/3735592
