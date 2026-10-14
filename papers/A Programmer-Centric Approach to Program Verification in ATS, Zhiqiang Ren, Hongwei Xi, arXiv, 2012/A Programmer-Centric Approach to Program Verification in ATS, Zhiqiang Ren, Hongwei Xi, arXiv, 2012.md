                                                   A Programmer-Centric Approach to
                                                      Program Verification in ATS⋆

                                                                 Zhiqiang Ren1 and Hongwei Xi1

                                                                          Boston University
arXiv:1203.6102v1 [cs.PL] 27 Mar 2012




                                              Abstract. Formal specification is widely employed in the construction
                                              of high-quality software. However, there is often a huge gap between for-
                                              mal specification and actual implementation. While there is already a vast
                                              body of work on software testing and verification, the task to ensure that
                                              an implementation indeed meets its specification is still undeniably of
                                              great difficulty. ATS is a programming language equipped with a highly
                                              expressive type system that allows the programmer to specify and imple-
                                              ment and then verify within the language itself that an implementation
                                              meets its specification. In this paper, we present largely through examples
                                              a programmer-centric style of program verification that puts emphasis on
                                              requesting the programmer to explain in a literate fashion why his or her
                                              code works. This is a solid step in the pursuit of software construction
                                              that is verifiably correct according to specification.



                                        1   Introduction

                                        In order to be precise in building software systems, we need to specify what such
                                        a system is expected to accomplish. In the current day and age, software speci-
                                        fication, which we use in a rather loose sense, is often done in forms of varying
                                        degree of formalism, ranging from verbal discussions to pencil/paper drawings
                                        to various diagrams in modeling languages such as UML [RHCF05] to formal
                                        specifications in specification languages such as Z [Spi92], etc. Often the main
                                        purpose of software specification is to establish a mutual understanding among a
                                        team of developers. After the specification for a software system is done, either
                                        formally or informally, we need to implement the specification in a programming
                                        language. In general, it is exceedingly difficult to be reasonably certain whether
                                        an implementation actually meets its specification. Even if the implementation
                                        coheres well with its specification initially, it nearly inevitably diverges from the
                                        specification as the software system evolves. The dreadful consequences of such
                                        a divergence are all too familiar; the specification becomes less and less reliable
                                        for understanding the behavior of the software system while the implementation
                                        gradually turns into its own specification; for the developers, it becomes increas-
                                        ingly difficult and risky to maintain and extend the software system; for the users,
                                        it requires extra amount of time and effort to learn and use the software system.
                                        ⋆
                                            This work is partially supported by NSF grants No. CCF-0702665.
    The design of ATS [Xi04,Xi08] was largely inspired by Martin-Löf’s construc-
tive type theory [Mar85], which was originally developed for the purpose of es-
tablishing a foundation for mathematics. Within ATS, there are a static com-
ponent (statics) and a dynamic component (dynamics). Intuitively, the statics
and dynamics are each for handling types and programs, respectively. In par-
ticular, specification is done in the statics and implementation in the dynamics.
Given a specification, how can we effectively ensure that an implementation of
the specification indeed implements according to the specification? We expect
that the programmer who does the implementation also constructs a proof in the
theorem-proving subsystem of ATS to demonstrate it. This is a style of program
verification that puts its emphasis on requesting the programmer to explain in a
literate fashion why his or her code works, and thus we refer to it as a programmer-
centric approach to program verification. The primary contribution of the paper
lies in our effort identifying such a style of program verification as well as putting
it into practice.
    In theorem-proving systems such as Coq [The03] and NuPrl [C+ 86], a spec-
ification is encoded as a type; if a proof inhabiting the type is made available,
then a program guaranteed to meet the specification can be automatically ex-
tracted out of the proof. Alternatively, formal annotations can be developed for
a program logic such as Hoare logic [Hoa69] or separation logic [Rey02]; a pro-
gram interspersed with annotations for a chosen property can be passed to a
tool that generates proof obligations according to the underlying program logic,
and the generated proof obligations can often be discharged through automated
theorem-proving. For instance, KML [TGK09] is a system of this kind for pro-
gram verification. The approach to program verification in ATS somewhat lies in
between the two aforementioned ones: It cohesively combines programming with
theorem-proving.
    We organize the rest of the paper as follows. In Section 2, we give a brief
overview of ATS. We then present in Section 3 a typical style of program verifi-
cation in ATS that combines programming with theorem-proving. In Section 4,
we employ some examples to illustrate that ATS is well-equipped with features to
support program verification that is both flexible and effective for practical use.
Last, we mention some related work in Section 5 and then conclude.



          sorts            σ ::= b | σ1 → σ2
          static terms     s ::= a | sc[s1 , . . . , sn ] | λa : σ.s | s1 (s2 )
          static var. ctx. Σ ::= ∅ | Σ, a : σ
          dyn. terms       d ::= x | dc(d1 , . . . , dn ) | lam x.d | app(d1 , d2 ) | . . .
          dyn. var. ctx. ∆ ::= ∅ | ∆, x : s


             Fig. 1. Some formal syntax for statics and dynamics of ATS
2   Overview of ATS
We give some formal syntax of ATS in Figure 1. The language ATS has a static
component (statics) and a dynamic component (dynamics). The statics includes
types, props and type indexes while the dynamics includes programs and proofs.
The statics itself is a simply typed language and a type in it is referred as a sort.
For instance, we have the following base sorts in ATS: addr , bool , int , prop, type,
etc; we use L, B and I for static addresses, booleans and integers of the sorts
addr , bool and int , respectively; we use T for static terms of the sort type, which
are types assigned to programs; we use P for static terms of the sort prop, which
are props assigned to proofs.
    Types and props may depend on one or more type indexes of static sorts. A
special case of such indexed types is singleton types, which are each a type for
only one specific value. For instance, bool(B) is a singleton type for the boolean
value equal to B, and int(I) is a singleton type for the integer equal to I, and
ptr(L) is a singleton type for the pointer that points to the address (or location)
L. Also, we can quantify over type index variables universally and existentially to
form quantified types and props.
    We use proving-types of the form (P | T ) for combining proofs with programs,
where P and T stand for a prop and a type, respectively. One may think of the
proving-type (P | T ) as a refinement of the type T because P often constrains
some of the indexes appearing in T . For example, the following type:
                      (ADD(m, n, p) | int(m), int(n), int(p))
is a proving-type of the sort type for a tuple of integers (m, n, p) along with a
proof of the prop ADD(m, n, p) which encodes m + n = p. Given a static boolean
term B and a type T , we can form two special forms of types: guarded types of
the form B ⊃ T and asserting types of the form B ∧ T . Following is an example
involving singleton, guarded and asserting types:
             ∀a : int .a ≥ 0 ⊃ (int(a) → ∃a ′ : int .(a ′ < 0 ∧ int(a ′ )))
The meaning of this type should be clear: Each value that can be assigned this
type represents a function from nonnegative integers to negative integers.


3   Overview of Program Verification in ATS
We now use a simple example to illustrate the idea of programming with theo-
rem proving. Suppose we want to compute Fibonacci numbers, which are defined
inductively as follows:
     fib(0) = 0     fib(1) = 1     fib(n + 2) = fib(n) + fib(n + 1) for n >= 0
A direct implementation of the function fib in ATS can be done as follows:
fun fib (n:int): int =
  if n = 0 then 0 else (if n = 1 then 1 else fib (n-1) + fib (n-2))
// end of [fib]
where the syntax is ML-like. This is a terribly impractical implementation of
exponential time-complexity. In C, we can give an implementation as follows that
is of O(n) time-complexity:

int fibc (int n) {
  int tmp, f0 = 0, f1 = 1 ;
  while (n-- > 0) { tmp = f1 ; f1 = f0 + f1 ; f0 = tmp ; } ;
  return f0 ;
} // end of [fibc]

There is obviously a logic gap between the definition of fib and its implementation
fibc in C.1 In ATS, we can give an implementation of fib that completely bridges
this gap. First, we need a way to encode the definition of fib into ATS, which is
fulfilled by the declaration of the following dataprop:

dataprop FIB (int, int) =
  | FIB0 (0, 0) | FIB1 (1, 1)
  | {n:nat} {r0,r1:int}
    FIB2 (n+2, r0+r1) of (FIB (n, r0), FIB (n+1, r1))
// end of [FIB]

where the concrete syntax {...} is for universal quantification in ATS. This
declaration introduces a type (or more precisely, a type constructor) FIB for
proofs. Such a type is referred to as a prop (or prop-type) in ATS. Intuitively, if
a proof can be assigned the type FIB(n, r) for some integers n and r, then fib(n)
equals r. In other words, FIB(n, r) encodes the relation fib(n) = r. There are
three constructors FIB0 , FIB1 and FIB2 associated with FIB, which are given
the following types corresponding to the three equations in the definition of fib:

              FIB0 : () → FIB(0, 0)
              FIB1 : () → FIB(1, 1)
              FIB2 : ∀n : nat.∀r0 : int.∀r1 : int.
                        (FIB(n, r0 ), FIB(n, r1 ) → FIB(n + 2, r0 + r1 )

For instance, FIB2 (FIB0 (), FIB1 ()) is a term of the type FIB(2, 1), attesting to
fib(2) = 1. In Figure 2, the implemented function fibats is assigned the following
type:
              fibats : ∀n : nat. int(n) → ∃r : int.(FIB(n, r) | int(r))
where | is just a separator (like a comma) for separating a proof from a value.
For each integer I, int(I) is a singleton type for the only integer whose value is
I. When fibats is applied to an integer of value n, it returns a pair consisting of a
proof and an integer value r such that the proof, which is of the type FIB(n, r),
asserts fib(n) = r. Therefore, fibats is a verified implementation of fib. Note that
the loop function in Figure 2 directly corresponds to the while-loop in the body
of fibc. Also, we emphasize that proofs are completely erased after typechecking.
In particular, there is no proof construction at run-time.
1
    We do not address the issue of possible arithmetic overflow here.
//
// the syntax [...] is for existential quantification
//
fun fibats {n:nat} (n: int n)
  : [r:int] (FIB (n, r) | int r) = let
  fun loop
    {n,i:nat | i <= n} {r0,r1:int} (
    pf0: FIB (i, r0), pf1: FIB (i+1, r1)
  | r0: int (r0), r1: int (r1), ni: int(n-i)
  ) : [r:int] (FIB (n, r) | int (r)) =
  if ni > 0 then
    loop {n,i+1} (pf1, FIB2 (pf0, pf1) | r1, r0+r1, ni-1)
  else (pf0 | r0)
in
  loop (FIB0(), FIB1() | 0, 1, n)
end // end of [fibats]


                    Fig. 2. A verified implementation of fib in ATS


4     Programmer-Centric Verification
By programmer-centric verification, we mean a verification approach that puts
the programmer at the center of the verification process. The programmer is
expected to explain in a literate fashion why his or her implementation meets a
given specification. The programmer may rely on external knowledge when doing
verification, but such knowledge should be expressed in a format that is accessible
to other programmers. We will employ some examples in this section to elaborate
on programmer-centric verification.

4.1   Example: Insertion Sort on Generic Lists
In Figure 3, we give a standard implementation of insertion sort written in ATS
that takes a generic list and a comparison function and returns a generic list that
is sorted according to the comparison function. Note that the use of generic lists
clearly indicates our strive for practicality. In the literature, a similar presentation
would often use integer lists (instead of generic lists), revealing the difficulty in
handling polymorphism and thus weakening the argument for practical use of
verification. We have no such difficulty. The implementation we present guarantees
based on the types that the output list is of the same length as the input list. We
also give a verified implementation of insertion sort in Figure 4 that guarantees
based on the types that the output list is a sorted permutation of the input list.
The fact that this verified implementation can be done in such a concise manner
should yield strong support for the underlying verification approach.
    Suppose that a programmer did the implementation in Figure 3. Obviously,
the programmer did not do the implementation in a random fashion; he or she
did it based on some kind of (informal) logic reasoning. We will see that ATS
provides programming features such as abstract props and external lemmas for
//
// list(a, n) is the type for a list of length n
// in which each element is of the type T.
//
fun{a:type} insort {n:nat}
  (xs: list (a, n), lte: (a, a) -> bool): list (a, n) = let
  fun ins {n:nat}
    (x: a, xs: list (a, n), lte: (a, a) -> bool): list (a, n+1) =
    case xs of
    | list_cons (x1, xs1) =>
        if lte (x, x1) then
          list_cons (x, xs) else list_cons (x1, ins (x, xs1, lte))
        // end of [if]
    | list_nil () => list_cons (x, list_nil ())
  // end of [ins]
in
  case xs of
  | list_cons (x, xs1) => ins (x, insort (xs1, lte), lte)
  | list_nil () => list_nil ()
end // end of [insort]


                  Fig. 3. A standard implementation of insertion sort


turning such informal reasoning into formal verification. In particular, we can turn
the implementation of insertion sort in Figure 3 into the verified one in Figure 4
by following a verification process.
    In Figure 5, we first introduce an abstract type constructor E. Given a type
T and an integer I, E(T, I) is a singleton type for a value of the type T with an
(imaginary) integer name I. In ATS, the user-defined sorts (datasorts) can be in-
troduced in a manner similar to the introduction of user-defined types (datatypes)
in a ML-like language. We introduce a datasort ilist for representing sequences of
(static) integers. We may simply write nil and cons for ilist nil and ilist cons, re-
spectively, if there is no potential confusion. Note that there is no mechanism
for defining recursive functions in the statics, and this is a profound restric-
tion that give rise to a unique style of verification in ATS. We lastly define a
datatype glist: Given a list of values of types E(T, I1 ), . . . , E(T, In ), the type
glist(T, cons(I1 , . . . , cons(In , nil))) can be assigned to this particular list. We may
also simply write nil and cons for glist nil and glist cons, respectively, if there is
no potential confusion. Please note that glist is in the dynamics while ilist is in
the statics.
    To verify insertion sort, we first introduce an abstract prop as follows such
that SORT(xs, ys) means that ys is a sorted permutation of xs:
absprop SORT (xs:ilist, ys:ilist)
Let lte(a) be a shorthand for the following type:

         ∀a : type∀x1 : int ∀x2 : int .(E(a, x1 ), E(a, x2 )) → bool(x1 ≤ x2 )
fun{a:type} insort
  {xs:ilist} (xs: glist (a, xs), lte: lte(a))
  : [ys:ilist] (SORT (xs, ys) | glist (a, ys)) = let
  fun ins {x:int} {ys1:ilist} (
    pford: ORD (ys1) |
    x: E (a, x), ys1: glist (a, ys1), lte: lte(a)
  ) : [ys2:ilist] (SORT (cons (x, ys1), ys2) | glist (a, ys2)) =
    case ys1 of
    | glist_cons (y1, ys10) =>
        if lte (x, y1) then let
          prval pford = ORD_ins {x} (pford)
          prval pfperm = PERM_refl ()
          prval pfsrt = ORDPERM2SORT (pford, pfperm)
        in
          (pfsrt | cons (x, ys1))
        end else let
          prval pford1 = ORD_tail (pford)
          val (pfsrt1 | ys20) = ins (pford1 | x, ys10, lte)
          prval pfsrt2 = SORT_ins {x} (pford, pfsrt1)
        in
          (pfsrt2 | cons (y1, ys20))
        end // end of [if]
    | glist_nil () => (SORT_sing () | cons (x, nil ()))
  // end of [ins]
in
  case xs of
  | glist_cons (x, xs1) => let
      val (pfsrt1 | ys1) = insort (xs1, lte)
      prval pford1 = SORT2ORD (pfsrt1)
      prval pfperm1 = SORT2PERM (pfsrt1)
      prval pfperm1_cons = PERM_cons (pfperm1)
      val (pfsrt2 | ys2) = ins (pford1 | x, ys1, lte)
      prval pford2 = SORT2ORD (pfsrt2)
      prval pfperm2 = SORT2PERM (pfsrt2)
      prval pfperm3 = PERM_tran (pfperm1_cons, pfperm2)
      prval pfsrt3 = ORDPERM2SORT (pford2, pfperm3)
    in
      (pfsrt3 | ys2)
    end // end of [intlist_cons]
  | glist_nil () => (SORT_nil () | nil ())
end // end of [insort]


               Fig. 4. A verified implementation of insertion sort
abstype E (a:type, x:int) // abstract type constructor
datasort ilist = ilist_nil of () | ilist_cons of (int, ilist)
datatype glist (a:type, ilist) =
  | {x:int} {xs:ilist}
    glist_cons (a, cons (x, xs)) of (E (a, x), glist (a, xs))
  | glist_nil (a, nil) of ()


          Fig. 5. A generic list type indexed by the names of list elements


If we can assign the following type to insort:

       ∀a : type∀xs : ilist .
         (glist(a, xs), lte(a)) → ∃ys : ilist .(SORT(xs, ys) | glist(a, ys))

then insort is verified as the type simply states that the output list is a sorted
permutation of the input list.
   For the purpose of verification, we also introduce the following two abstract
props:

absprop ORD (xs:ilist)
absprop PERM (xs:ilist, ys:ilist)

Given xs and ys, ORD(xs) means that xs is ordered according to the ordering
≤ on integers and PERM(xs, ys) means that ys is a permutation of xs.



      SORT2ORD         : ∀xs : ilist∀ys : ilist. SORT(xs, ys) → ORD(ys)
     SORT2PERM         : ∀xs : ilist∀ys : ilist. SORT(xs, ys) → PERM(xs, ys)
  ORDPERM2SORT         : ∀xs : ilist∀ys : ilist.
                           (ORD(ys), PERM(xs, ys)) → SORT(xs, ys)
           SORT nil    : () → SORT(nil, nil)
          SORT sing    : ∀x : int. () → SORT(cons(x , nil ), cons(x , nil ))
           ORD tail    : ∀y : int∀ys : ilist. ORD(cons(y, ys)) → ORD(ys)
            ORD ins    : ∀x : int∀y : int∀ys : ilist. x ≤ y ⊃
                           ORD(cons(y, ys)) → ORD(cons(x, cons(y, ys)))
         PERM refl     : ∀xs : ilist. () → PERM(xs, xs)
         PERM tran     : ∀xs : ilist∀ys : ilist∀zs : ilist.
                           (PERM(xs, ys), PERM(ys, zs)) → PERM(xs, zs)
         PERM cons     : ∀x : int∀xs1 : ilist∀xs2 : ilist.
                           PERM(xs1 , xs2 ) → PERM(cons(x, xs1 ), cons(x, xs2 ))
           SORT ins    : ∀x : int∀y : int∀ys1 : ilist∀ys2 : ilist. x > y ⊃
                           (ORD(cons(y, ys1 )), SORT(cons(x, ys1 ), ys2 )) →
                           SORT(cons(x, cons(y, ys1 )), cons(y, ys2 ))


          Fig. 6. Some external lemmas needed for verifying insertion sort
 – SORT2ORD: If ys is a sorted version of xs, then ys is ordered
 – SORT2PERM: If ys is a sorted version of xs, then ys is a permutation of xs
 – ORDPERM2SORT: if ys is ordered and is also a permutation of xs, then ys is a
   sorted version of xs.
 – SORT nil: The empty list is a sorted version of itself.
 – SORT sing: A singleton list is a sorted version of itself.
 – ORD tail: If a non-empty list is ordered, then its tail is also ordered.
 – ORD ins: If x ≤ y holds and cons(y, ys) is ordered, then cons(x, cons(y, ys)) is also
   ordered.
 – PERM refl: Each list is a permutation of itself
 – PERM tran: The permutation relation is transitive.
 – PERM cons: If xs2 is a permutation of xs1 , then cons(x, xs2 ) is a permutation of
   cons(x, xs1 ).
 – SORT ins: If x > y holds, cons(y, ys1 ) is ordered and ys2 is a sorted version of
   cons(x, ys1 ), then cons(y, ys2 ) is a sorted version of cons(x, cons(y, ys1 )).


                 Fig. 7. Some explanation for the lemmas in Figure 6



    When verifying insort, we essentially try to justify each step in the code pre-
sented in Figure 3. This justification process may introduce various external lem-
mas. For instance, the code presented in Figure 4 makes use of the lemmas listed
in Figure 6.
    In order to prove these lemmas, we need to define SORT, ORD and PERM
explicitly, and we can indeed do this in the theorem-proving subsystem of ATS.
However, this style of verifying everything from basic definitions can be too great a
burden in practice. Suppose that we try to construct a mathematical proof and we
need to make use of the proposition in the proof that the standard permutation
relation is transitive. It is unlikely that we provide an explicit proof for this
proposition as it sounds so evident to us. To put it from a different angle, if
constructing mathematical proofs required that every single detail be presented
explicitly, then studying mathematics would unlikely to be feasible. Therefore, we
strongly advocate a style of theorem-proving in ATS that models the way we do
mathematics.
    The implementation of insertion sort on generic lists in Figure 3, which can
be obtained from erasing proofs in Figure 4, is guaranteed to be correct if all of
the lemmas in Figure 6 are true. Some explanation of these lemmas is given in
Figure 7. It is probably fair to say that these lemmas are all evidently true except
the last one: SORT ins. If we are unsure whether the lemma SORT ins is true or
not, we can construct a proof in ATS or elsewhere to validate it. For instance, we
can even give an informal proof as follows: Note that PERM(cons(x, ys1 ), ys2 )
holds as ys2 is a sorted version of cons(x, ys1 ). Hence, cons(y, ys2 ) is a permu-
tation of cons(x, cons(y, ys1 )). Since cons(y, ys1 ) is ordered, y is a lower bound
for the elements in ys1 . Hence, y is a lower bound for elements in ys2 as x > y
holds, and thus, cons(y, ys2 ) is ordered. Therefore, cons(y, ys2 ) is a sorted version
of cons(x, cons(y, ys1 )).
    What is of crucial importance is that SORT ins is a lemma that is manually
introduced and can be readily understood by any programmer with adequate
training. This is a direct consequence of programmer-centric verification in which
the programmer explains in a literate fashion why his or her implementation meets
a given specification.


fun{a:type}
qsrt {n:nat}
  (xs: list (a, n), lte: lte a) : list (a, n) =
  case+ xs of
  | list_cons (x, xs) => part (x, xs, lte, list_nil (), list_nil ())
  | list_nil () => list_nil ()

and part {p:nat} {q,r:nat} (
  x0: a, xs: list (a, p), lte: lte(a), ys: list (a, q), zs: list (a, r)
) : list (a, p+q+r+1) =
  case+ xs of
  | list_cons (x, xs) =>
      if lte (x, x0) then
        part (x0, xs, lte, list_cons (x, ys), zs)
      else
        part (x0, xs, lte, ys, list_cons (x, zs))
      // end of [if]
  | list_nil () => let
      val ys = qsrt (ys, lte) and zs = qsrt (zs, lte)
    in
      append (ys, list_cons (x0, zs))
    end // end of [list_nil]


                   Fig. 8. A standard implementation of quicksort




4.2   Example: Quicksort on Generic Lists

We give a standard implementation of quicksort on generic lists in Figure 8. The
reason that we use lists instead of arrays is solely for simplifying the presentation.
As far as verification is concerned, there is really not much difference between
lists and arrays. Note that we have already made various verification examples
available on-line that involve arrays.
     The implementation in Figure 8 guarantees based on the types that the output
list is of the same length as the input list. We also give a verified implementation
of quicksort in Figure 9 that guarantees based on the types that the output list is
a sorted permutation of the input list. The verified implementation is essentially
obtained from the process to explain why the function qsrt in Figure 8 always
returns a list that is the sorted version of the input list.
fun{a:type}
qsrt {xs:ilist} (
  xs: glist (a, xs), lte: lte a
) : [ys:ilist] (SORT (xs, ys) | glist (a, ys)) =
  case+ xs of
  | glist_cons (x, xs) => let
      val (pford, pfuni | res) =
        part (UB_nil (), LB_nil () | x, xs, lte, nil (), nil ())
      prval pfperm = UNION4_perm (pfuni)
    in
      (ORDPERM2SORT (pford, pfperm) | res)
    end
  | glist_nil () => (SORT_nil () | nil ())

and part
  {x0:int} {xs:ilist} {ys,zs:ilist} (
  pf1: UB (x0, ys), pf2: LB (x0, zs)
| x0: E (a, x0), xs: glist (a, xs), lte: lte(a)
, ys: glist (a, ys), zs: glist (a, zs)
) : [res:ilist] (
  ORD (res), UNION4 (x0, xs, ys, zs, res) | glist (a, res)
) =
  case+ xs of
  | glist_cons (x, xs) =>
      if lte (x, x0) then let
         prval pf1 = UB_cons (pf1)
         val (pford, pfuni | res) =
           part (pf1, pf2 | x0, xs, lte, cons (x, ys), zs)
         prval pfuni = UNION4_mov1 (pfuni)
      in
         (pford, pfuni | res)
      end else let
         prval pf2 = LB_cons (pf2)
         val (pford, pfuni | res) =
           part (pf1, pf2 | x0, xs, lte, ys, cons (x, zs))
         prval pfuni = UNION4_mov2 (pfuni)
      in
         (pford, pfuni | res)
      end // end of [if]
  | glist_nil () => let
      val (pfsrt1 | ys) = qsrt (ys, lte)
      val (pfsrt2 | zs) = qsrt (zs, lte)
      val (pfapp | res) = append (ys, cons (x0, zs))
      prval pford1 = SORT2ORD (pfsrt1)
      prval pford2 = SORT2ORD (pfsrt2)
      prval pfperm1 = SORT2PERM (pfsrt1)
      prval pfperm2 = SORT2PERM (pfsrt2)
      prval pf1 = UB_perm (pfperm1, pf1)
      prval pf2 = LB_perm (pfperm2, pf2)
      prval pford = APPEND_ord (pf1, pf2, pford1, pford2, pfapp)
      prval pfuni = APPEND_union4 (pfperm1, pfperm2, pfapp)
    in
      (pford, pfuni | res)
    end // end of [glist_nil]
// end of [part]


                 Fig. 9. A verified implementation of quicksort
           LB nil   : ∀x : int. () → LB(x , nil )
           UB nil   : ∀x : int. () → UB(x , nil )
          LB cons   : ∀x0 : int∀x : int∀xs : ilist. x0 ≤ x ⊃
                      LB(x0 , xs) → LB(x0 , cons(x, xs))
         UB cons    : ∀x0 : int∀x : int∀xs : ilist. x0 ≥ x ⊃
                      UB(x0 , xs) → UB(x0 , cons(x, xs))
         LB perm    : ∀x : int∀xs1 : ilist∀xs2 : ilist.
                      (PERM(xs1 , xs2 ), LB(x, xs1 )) → LB(x, xs2 )
         UB perm    : ∀x : int∀xs1 : ilist∀xs2 : ilist.
                      (PERM(xs1 , xs2 ), UB(x, xs1 )) → UB(x, xs2 )
   UNION4 perm      : ∀x : int∀xs : ilist∀res : ilist.
                       UNION4(x, xs, nil, nil, res) → PERM(cons(x, xs), res)
   UNION4 mov1      : ∀x0 : int∀x : int∀xs : ilist∀ys : ilist∀zs : ilist∀res : ilist.
                       UNION4(x0, xs, cons(x, ys), zs, res) →
                       UNION4(x0, cons(x, xs), ys, zs, res)
   UNION4 mov2      : ∀x0 : int∀x : int∀xs : ilist∀ys : ilist∀zs : ilist∀res : ilist.
                       UNION4(x0, xs, ys, cons(x, zs), res) →
                       UNION4(x0, cons(x, xs), ys, zs, res)
    APPEND ord      : ∀x : int∀ys : ilist∀zs : ilist∀res : ilist.
                       (UB(x, ys), LB(x, zs), ORD(ys), ORD(zs),
                        APPEND(ys, cons(x, zs), res)) → ORD(res)
 APPEND union4      : ∀x : int∀ys : ilist∀ys1 : ilist∀zs : ilist∀zs1 : ilist∀res : ilist.
                       (PERM(ys, ys1 ), PERM(zs, zs1 ),
                        APPEND(ys1 , cons(x, zs1 ), res)) →
                       UNION4(x, nil, ys, zs, res)


          Fig. 10. Some external lemmas needed for verifying quicksort



– LB perm: If x is a lower bound for xs1 and xs1 is a permutation of xs2 , then x is
  also a lower bound for xs2 .
– UB perm: If x is an upper bound for xs1 and xs1 is a permeation of xs2 , then x is
  also a upper bound for xs2 .
– UNION4 perm: If |res| = {x} ∪ |xs|, then res is a permutation of cons(x, xs).
– UNION4 mov1: If |res| = {x0 } ∪ |xs| ∪ |cons(x, ys)| ∪ |zs|, then |res| = {x0 } ∪
  |cons(x, xs)| ∪ |ys| ∪ |zs|.
– UNION4 mov2: If |res| = {x0 } ∪ |xs| ∪ |ys| ∪ |cons(x, zs)|, then |res| = {x0 } ∪
  |cons(x, xs)| ∪ |ys| ∪ |zs|.
– APPEND ord: If x is an upper bound for ys and a lower bound for zs, both ys
  and zs are ordered and res is the concatenation of ys and cons(x, zs), then res is
  ordered.
– APPEND union4: If ys1 is a permutation of ys, zs1 is a permutation of zs and res
  is the concatenation of ys1 and cons(x, zs1 ), then |res| = {x} ∪ |ys| ∪ |zs|.


              Fig. 11. Some explanation for the lemmas in Figure 10
   We now explain that the verified implementation of quicksort can be trusted.
The function append in the implementation is given the following type:

               ∀a : type.∀xs1 : ilist ∀xs2 : ilist .
                (glist(a, xs1 ), glist(a, xs2 )) →
                ∃res : ilist .(APPEND(xs1 , xs2 , res) | glist(a, res))

where APPEND is an abstract prop. Given lists xs1 , xs2 and res, the intended
meaning of APPEND(xs1 , xs2 , res) is obvious: it states that the concatena-
tion of xs1 and xs2 is res. Both LB and UB are introduced as abstract props:
LB(x, xs)/UB(x, xs) means that x is a lower/upper bound for the elements in
xs. Another introduced abstract prop is UNION4: Given x, xs, ys, zs and res,
UNION4(x, xs, ys, zs, res) means that the following equation holds

                           |res| = {x} ∪ |xs| ∪ |ys| ∪ |zs|

where | · | turns an integer list into a multiset. The external lemmas in Figure 9
are listed in Figure 10 and some explanation are given in Figure 11 for some of
these lemmas.


4.3    Many Other Examples
There are also a variety of examples available on-line2 which can further illus-
trate a style of programmer-centric verification in ATS that combines program-
ming with theorem-proving cohesively. In particular, there are examples involving
arrays, heaps, balanced trees, etc.


5     Related Work and Conclusion
Given the vastness of the field of program verification, we can only mention some
closely related work in this section.
    In the Coq theorem-proving system [DFH+ 93], programs can be extracted
from proofs [PM89]. In [FM99], the authors specified the orderedness property as
well as the permutation relation on the array structure and gave verification for
three sorting algorithms. However, Coq is primarily designed for theorem-proving
instead of programming, and its use as a programming language is a bit unwieldy
and limited.
    Ynot [CMM+ 09] is an axiomatic extension of the Coq proof assistant for spec-
ifying and verifying properties of imperative programs. The programmer can en-
code a new domain by providing key lemmas in an ML-like embedded language.
Relying on Coq to do theorem-proving, Ynot mixes the automated proof genera-
tion with manual proof construction, attempting to relieve the programmer from
the heavy burden that would otherwise be necessary.
    In the specification language KML [TGK09], the programmer can add anno-
tations such as preconditions, postconditions and invariants into Java programs,
2
    Please see http://www.ats-lang.org/EXAMPLE/PCPV
and a tool is provided for generating proof obligations automatically from the
annotated source file, which are to be discharged by various automatic provers.
Permutation can be specified based on the natural concept of multiset. Often, ex-
ternal assertions need to be provided along together with the code so as to make
the program verifiable by existing theorem provers.
    The work on extended static checking (ESC) [Det96] also puts emphasis on
employing formal annotations to capture program invariants. These invariants
may be verified through (light-weighted) theorem proving. ESC/Java [FRL+ 02]
generates verification-conditions based on annotated Java code and uses an auto-
matic theorem-prover to reason about the semantics of the programs. It can catch
many basic errors such as null dereferences, array bounds errors, type cast errors,
etc. With more emphasis on usefulness, soundness is sacrificed in certain cases to
reduce annotation cost or to improve checking speed.
    VeriFast [JSP10] is another system for verifying program properties through
source code annotation. It supports direct insertion of simple proof steps into the
source code while allowing rich and complex properties to be specified through
inductive datatypes and fixed-point functions. VeriFast provides a program verifier
for C and Java that supports interactive insertion of annotations into source code.
    The paradigm of programming with theorem-proving as is supported in the
ATS programming language system is a novel invention. In particular, this pro-
gramming paradigm is fundamentally different from program extraction (from
proofs) as is supported in theorem-proving systems such as Coq. In this paper,
we have argued for a style of program verification that puts emphasis on request-
ing the programmer to formally explain in a literate fashion why the code he or
she implements actually meets its specification. Though external lemmas intro-
duced during a verification process can be discharged by formally proving them
in ATS, doing so is often expensive in terms of effort and time. One possibility is
to characterize such lemmas into different categories and then employ (external)
theorem-provers specialized for a particular category to prove lemmas in that
category. Another possibility we advocate for discharging lemmas is through a
peer-review process, which mimics the practice of (informally) verifying math-
ematical proofs. Obviously, the precondition for such an approach is that the
lemmas to be verified can be expressed in a format that is easily accessible to a
(trained) human being. This is where the programmer-centric verification as is
presented in this paper can fit very well.


References

[C+ 86]   Robert L. Constable et al. Implementing Mathematics with the NuPrl Proof
          Development System. Prentice-Hall, Englewood Cliffs, New Jersey, 1986.
          ISBN 0-13-451832-2. x+299 pp.
[CMM+ 09] Adam Chilpala, Gregory Malecha, Gregory Morrisett, Avraham Shinnar,
          and Ryan Wisnesky. Effective Interactive Support for Higher-Order Im-
          perative Programs. In Proceedings of the 14th ACM SIGPLAN Inter-
          national Conference on Functional Programming (ICFP’09), pages 79–90.
          ACM, 2009.
[Det96]   David Detlefs. An overview of the extended static checking system. In
          Workshop on Formal Methods in Software Practice, 1996.
[DFH+ 93] Gilles Dowek, Amy Felty, Hugo Herbelin, Gérard Huet, Chet Murthy, Cather-
          ine Parent, Christine Paulin-Mohring, and Benjamin Werner. The Coq
          proof assistant user’s guide. Rapport Technique 154, INRIA, Rocquencourt,
          France, 1993. Version 5.8.
[FM99]    Jean-Christophe Filliâtre and Nicolas Magaud. Certification of sorting al-
          gorithms in the coq system. In Theorem-Proving in Higher-Order Logics:
          Emerging Trends, 1999.
[FRL+ 02] Cormac Flanagan, Rustan, Mark Lillibridge, Greg Nelson, James B. Saxe,
          and Raymie Stata. Extended static checking for Java. SIGPLAN Notice, 37:
          234–245, May 2002.
[Hoa69]   C. A. R. Hoare. An axiomatic basis for computer programming. Communi-
          cations of the ACM, 12(10):576–580 and 583, October 1969.
[JSP10]   Bart Jacobs, Jan Smans, and Frank Piessens. Verifast: Imperative programs
          as proofs. Available at:
          http://people.cs.kuleuven.be/ bart.jacobs/verifast/, 2010.
[Mar85]   Per Martin-Löf. Constructive mathematics and computer programming. In
          C. R. A. Hoare, editor, Mathematical Logic and Programming Languages.
          Prentice-Hall, 1985.
[PM89]    Christine Paulin-Mohring. Extraction de programmes dans le Calcul des
          Constructions. Thèse de doctorat, Université de Paris VII, Paris, France,
          1989.
[Rey02]   John Reynolds. Separation Logic: a logic for shared mutable data structures.
          In Proceedings of 17th IEEE Symposium on Logic in Computer Science (LICS
          ’02), 2002.
[RHCF05] Manny Rayner, Beth A. Hockey, Nikos Chatzichrisafis, and Kim Farrell.
          OMG Unified Modeling Language Specification. In Version 1.3, c 1999
          Object Management Group, Inc, 2005.
[Spi92]   J. M. Spivey. The Z Notation: A Reference Manual. Prentice Hall Interna-
          tional Series in Computer Science, 2nd edition, 1992. ISBN 013-978529-9.
          £18.99 ($32.00) paperback. URL http://www.afm.sbu.ac.uk/zbook/.
[TGK09] Elena Tushkanova, Alain Giorgetti, and Olga Kouchnarenko. Specifying and
          proving a sorting algorithm. Technical report, University of Franche-Comte,
          2009.
[The03]   The Coq Development Team. The Coq proof assistant reference manual,
          2003. Version 7.4.
[Xi04]    Hongwei Xi. Applied Type System (extended abstract). In post-workshop
          Proceedings of TYPES 2003, pages 394–408. Springer-Verlag LNCS 3085,
          2004.
[Xi08]    Hongwei Xi. The ATS Programming Language System, 2008. Available at:
          http://www.ats-lang.org/.
