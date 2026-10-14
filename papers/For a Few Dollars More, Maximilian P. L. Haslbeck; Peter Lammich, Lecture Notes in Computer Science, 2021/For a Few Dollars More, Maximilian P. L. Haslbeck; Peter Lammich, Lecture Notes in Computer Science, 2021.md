                       For a Few Dollars More
Veriﬁed Fine-Grained Algorithm Analysis Down to LLVM


                         Maximilian P. L. Haslbeck1 () ID
                                and Peter Lammich2 ID
                1
                  Technische Universität München, München, Germany
                                haslbema@in.tum.de
                2
                  The University of Manchester, Manchester, England
                          peter.lammich@manchester.ac.uk



        Abstract. We present a framework to verify both, functional correct-
        ness and worst-case complexity of practically eﬃcient algorithms. We
        implemented a stepwise reﬁnement approach, using the novel concept of
        resource currencies to naturally structure the resource analysis along the
        reﬁnement chain, and allow a ﬁne-grained analysis of operation counts.
        Our framework targets the LLVM intermediate representation. We ex-
        tend its semantics from earlier work with a cost model. As case study, we
        verify the correctness and O(n log n) worst-case complexity of an imple-
        mentation of the introsort algorithm, whose performance is on par with
        the state-of-the-art implementation found in the GNU C++ Library.

        Keywords: Algorithm Analysis · Program Veriﬁcation · Reﬁnement


1     Introduction

In general, not only correctness, but also the complexity of algorithms is im-
portant. While it is obvious that the performance observed during experiments
is essential to solve practical problems eﬃciently, also the theoretical worst-case
complexity of algorithms is crucial: a good worst-case complexity avoids timing
regressions when hitting worst-case input, and, even more important, prevents
denial of service attacks that intentionally produce worst-case scenarios to over-
load critical computing infrastructure.
    For example, the C++ standard requires implementations of std::sort to have
worst-case complexity O(n log n) [7]. Note that this rules out quicksort [12],
which is very fast in practice, but has quadratic worst-case complexity. Never-
theless, some standard libraries, most prominently LLVM’s libc++ [20], still use
sorting algorithms with quadratic worst-case complexity.3
    A practically eﬃcient sorting algorithm with O(n log n) worst-case complex-
ity is Musser’s introsort [22]. It combines quicksort with the O(n log n) heap-
sort algorithm, which is used as fallback when the quicksort recursion depth
3
    See, e.g., https://bugs.llvm.org/show_bug.cgi?id=20837.
c The Author(s) 2021
N. Yoshida (Ed.): ESOP 2021, LNCS 12648, pp. 292–319, 2021.
https://doi.org/10.1007/978-3-030-72019-3_11
                                                     For a Few Dollars More     293

exceeds a certain threshold. It allows to implement standard-compliant, prac-
tically eﬃcient sorting algorithms. Introsort is implemented by, e.g., the GNU
C++ Library (libstdc++) [8].
    In this paper, we present techniques to formally verify both, correctness and
worst-case complexity of practically eﬃcient implementations. We build on two
previous lines of research by the authors.
    On one hand, we have the Isabelle Reﬁnement Framework [19], which allows
for a modular top-down veriﬁcation approach. It utilizes stepwise reﬁnement to
separate the diﬀerent aspects of an eﬃcient implementation, such as algorith-
mic idea and low-level optimizations. It provides a nondeterminism monad to
formalize programs and reﬁnements, and the Sepref tool to automate canonical
data reﬁnement steps. Its recent LLVM back end [15] allows to verify algo-
rithms with competitive performance compared to (unveriﬁed) highly optimized
C/C++ implementations. The Reﬁnement Framework has been used to verify
the functional correctness of an implementation of introsort that performs on
par with libstdc++’s implementation [17].
    On the other hand, we already have extended the Reﬁnement Framework to
reason about complexity [11]. However, this only supports the Imperative/HOL
back end [16]. It generates implementations in functional languages, which are
inherently less eﬃcient than highly optimized C/C++ implementations. This
paper combines and extends these two approaches. Our main contributions are.
    • We present a generalized nondeterminism monad with resource cost, apply it
      to resource functions to model ﬁne-grained currencies (Section 2) and show
      how they can be used to naturally structure reﬁnement.
    • We extend the LLVM back end [15] with a cost model, and amend its basic
      reasoning infrastructure (Section 3).
    • We extend the Sepref tool (Section 4) to synthesize executable imperative
      code in LLVM, together with a proof of correctness and complexity. Our
      approach seamlessly supports imperative and amortized data structures.
    • We extend the veriﬁcation of introsort to also show a worst-case complexity of
      O(n log n), thus meeting the C++11 stdlib speciﬁcation [7] (Section 5). The
      performance of our implementation is still on par with libstdc++. We believe
      that this is the ﬁrst time that both, correctness and complexity of a sorting
      algorithm have been formally veriﬁed down to a competitive implementation.
   Our formalization is available at https://www21.in.tum.de/~haslbema/
llvm-time.

2      Speciﬁcation of Algorithms With Resources
We use the formalism of monads [24] to elegantly specify programs with resource
usage. We ﬁrst describe a framework that works for a very generic notion of
resource, and then instantiate it with resource functions, which model resources
of diﬀerent currencies. We then describe a reﬁnement calculus and show how
currencies can be used to structure stepwise reﬁnement proofs. Finally, we report
on automation and give some examples.
294      P. M. L. Haslbeck and P. Lammich

2.1     Nondeterministic Computations With Resources
Let us examine the features we require for our computation model.
    First, we want to specify programs by their desired properties, without having
to ﬁx a concrete implementation. In general, those programs have more than one
correct result for the same input. Consider, e.g., sorting a list of pairs of numbers
by the ﬁrst element. For the input [(1, 2), (2, 2), (1, 3)], both [(1, 2), (1, 3), (2, 2)]
and [(1, 3), (1, 2), (2, 2)] are valid results. Formally, this is modelled as a set of
possible results. When we later ﬁx an implementation, the set of possible results
may shrink. For example, the (stable) insertion sort algorithm always returns
the list [(1, 2), (1, 3), (2, 2)]. We say that insertion sort reﬁnes our speciﬁcation
of sorting.
    Second, we want to deﬁne recursion by a standard ﬁxed-point construction
over a ﬂat lattice. The bottom of this lattice must be a dedicated element, which
we call fail. It represents a computation that may not terminate.
    Finally, we want to model the resources required by a computation. For
nondeterministic programs, these may vary depending on the nondeterministic
choices made during the computation. As we model computations by their pos-
sible results, rather than by the exact path in the program that leads to the
result, we also associate resource cost with possible results. When more than
one computation path leads to the same result, we take the supremum of the
used resources. The notion of reﬁnement is now extended to a subset of results
that are computed using less resources.
    We now formalize the above intuition: The type
      (α,γ) NREST = fail | res (α → γ option)
models a nondeterministic computation with results of type α and resources of
type γ.4 That is, a computation is either fail, or res M, where M is a partial
function from possible results to resources.
     We deﬁne spec Φ T as a computation of any result r that satisﬁes Φ r us-
ing T r resources: spec Φ T = res (λr. if Φ r then Some (T r) else None).
By abuse of notation, we write spec x T for spec (λr. r=x) (λ . T).
     Based on an ordering on the resources γ, we deﬁne the reﬁnement ordering on
NREST, by ﬁrst lifting the ordering to option with None as the bottom element,
then pointwise to functions and ﬁnally to (α,γ) NREST, setting fail as the top
element. This matches the intuition of reﬁnement: m ≤ m reads as m reﬁnes m,
i.e., m has less possible results than m, computed with less resources.
     We require the resources γ to have a complete lattice structure, such that
we can form suprema over the (possibly inﬁnitely many) paths that lead to the
same result. Moreover, when sequentially composing computations, we need to
add up the resources. This naturally leads to a monoid structure (γ, 0, +), where
0, intuitively, stands for no resources.
     We call such types γ resource types, if they have a complete lattice and monoid
structure. Note that, in an earlier iteration of this work [11], the resource type
4
    The name NREST abbreviates Nondeterministic RESult with Time, and has been
    inherited from our earlier formalizations.
                                                      For a Few Dollars More       295

was ﬁxed to extended natural numbers (enat=N ∪ {∞}), measuring the resource
consumption with a single number. Also note that (α,unit) NREST is isomorphic
to our original nondeterministic result monad without resources [19].
    If γ is a resource type, so is η → γ. Intuitively, such resources consist of coins
of diﬀerent resource currencies η, the amount of coins being measured by γ.

Example 1. In the following we use the resource type ecost = string → enat, i.e.,
we have currencies described by a string, whose amount is measured by extended
natural numbers, where ∞ models arbitrary resource usage. Note that, while the
resource type string→enat guides intuition, most of our theory works for general
resource types of the form η → γ or even just γ.
    We deﬁne the function $s n to be the resource function that uses n :: enat
coins of the currency s :: string, and write $s as shortcut for $s 1.
    A program that sorts a list in O(n2 ) can be speciﬁed by:
     sortspec xs = spec (λxs. sorted xs ∧ mset xs = mset xs) ($q |xs|2 + $c )
that is, a list xs can result in any sorted list xs with the same elements, and
the computation takes (at most) quadratically many q coins in the list length,
and one c coin, independently of the list length. Intuitively, the q and c coins
represent the constant factors of an algorithm that implements that speciﬁcation
and are later elaborated by exchanging them into several coins of more ﬁne-
grained currencies, corresponding to the concrete operations in the algorithm,
e.g., comparisons and memory accesses. Abstract currencies like q and c only
“have value” if they can be exchanged to meaningful other currencies, and ﬁnally
pay for the resource costs of a concrete implementation.


2.2    Atomic Operations and Control Flow

In order to conveniently model actual computations, we deﬁne some combinators.
The elapse m t combinator adds the (constant) resources t to all results of m:
     elapse :: (α,γ) NREST → γ → (α,γ) NREST
     elapse fail t = fail
     elapse (res M) t = res (λx. case M x of None ⇒ None
                                        | Some t ⇒ Some (t + t ))
The program5 return x computes the single result x without using any resources:
     return :: α → (α,γ) NREST
     return x = res [ x → 0 ]
The combinator bind m f models the sequential composition of computations m
and f , where f may depend on the result of m:
5
    Note that our shallow embedding makes no formal distinction between syntax and
    semantics. Nevertheless, we refer to an entity of type NREST, as program to em-
    phasize the syntactic aspect, and as computation to emphasize the semantic aspect.
296       P. M. L. Haslbeck and P. Lammich

      bind :: (α,γ) NREST → (α → (β,γ) NREST) → (β,γ) NREST
      bind fail f = fail
      bind (res M) f = Sup { elapse (f x) t |x t. M x = Some t }
If the ﬁrst computation m fails, then also the sequential composition fails. Oth-
erwise, we consider all possible results x with resources t of m, invoke f x, and
add the cost t for computing x to the results of f x. The supremum aggregates
the cases where f yields the same result, via diﬀerent intermediate results of m,
and also makes the whole expression fail if one of the f x fails.
Example 2. We now illustrate an eﬀect that stems from our decision to aggregate
the resource usage of diﬀerent computation paths that lead to the same result.
Consider the program
      res (λn::nat. Some ($c n)); return 0
It ﬁrst chooses an arbitrary natural number n consuming n coins of currency c,
and then returns the result 0. That is, there are arbitrarily many paths that lead
to the result 0, consuming arbitrarily many c coins. The supremum of this is ∞,
such that the above program is equal to elapse (return 0) ($c ∞). Note that
none of the computation paths actually attains the aggregated resource usage.
We will come back to this in Section 4.4.
   Finally, we use Isabelle/HOL’s if-then-else and deﬁne a recursion combinator
rec via a ﬁxed-point construction [13], to get a complete set of basic combinators.
As these combinators also incur cost in the target LLVM, we deﬁne resource
aware variants. Furthermore we also derive a while combinator:
      ifc b then c1 else c2 = elapse (r ← b; if r then c1 else c2 ) $if
      recc F x = elapse (rec (λD x. F (λx. elapse (D x) $call ) x) x) $call
      whilec b f s = recc (λD s. ifc b s then s ← f s; D s else return s) s
Here, the guard of ifc is a computation itself, and we consume an additional
if coin to account for the conditional branching in the target model. Similarly,
every recursive call consumes an additional call coin.
   Assertions fail if their condition is not met, and return unit otherwise:
      assert P = if P then return () else fail
They are used to express preconditions of a program. A Hoare-triple for program
m, with precondition P, postcondition Q and resource usage t is written as a
reﬁnement condition: m ≤ assert P; spec Q (λ . t)
Example 3. Comparison of two list elements at a cost of t can be speciﬁed by:
      idxs cmpspec xs i j (t) = assert (i<|xs| ∧ j<|xs|); spec (xs!i < xs!j) (λ . t)
where xs!i is the ith element of list xs. Instead of ﬁxing the cost for speciﬁcations,
we pass them as parameter t. This allows us to reﬁne diﬀerent instances of ab-
stract data types (here lists) by diﬀerent concrete data structures with diﬀerent
costs. To make bigger programs more readable, we note the cost parameter in
parenthesis at the end of the line, as, e.g., in Example 4.
                                                   For a Few Dollars More     297

2.3   Reﬁnement on NREST

We have used the reﬁnement ordering to express Hoare triples. Two other ap-
plications of reﬁnement are data reﬁnement and currency reﬁnement.

Data Reﬁnement A typical use-case of reﬁnement is to implement an abstract
data type by a concrete data type. For example, we could implement (ﬁnite) sets
of numbers by sorted lists. We deﬁne a reﬁnement relation R between sorted
lists and sets. A concrete computation m† that yields sorted lists then reﬁnes
an abstract computation m that yields sets, if every possible concrete result is
related to a possible abstract result. Formally, m† ≤ ⇓D R m, where the operator
⇓D is deﬁned, for arguments R and m, by the following two rules.
   ⇓D R (res M) = res (λc. Sup {M a | a. (c,a) ∈ R})         ⇓D R fail = fail
Again, we use the supremum to aggregate the costs of all abstract results that
are related to a concrete result. As in Example 2, this leads to the possibility
that the supremum cost is not attained, which we discuss in Section 4.4.

Currency Reﬁnement Consider we want to reﬁne Example 3 into a program that
ﬁrst accesses the elements and then compares them.

Example 4. We reﬁne idxs cmpspec ($idxs cmp ) from Example 3 as follows:
   idxs cmp xs i j =
         assert (i<|xs| ∧ j<|xs|);
         xsi ← list getspec xs i;  ($lookup )
         xsj ← list getspec xs j;  ($lookup )
         return (xsi < xsj)        ($less )
where list getspec xs i (T) = assert (i < |xs|); spec (xs!i) T and return x (T)
returns the result x incurring cost T.
   Note that idxs cmp and idxs cmpspec use diﬀerent, incompatible currency
systems. To compare them, we need to exchange coins: one idxs cmp coin will
be traded for two lookup coins and one less coin.

    To make that happen we introduce the currency reﬁnement ⇓C E m. Here,
the exchange rate E :: ηa → ηc → γ speciﬁes for each abstract currency ca :: ηa
how many of the coins of the concrete currency cc :: ηc are needed. Note that,
in general, one abstract coin may be exchanged into multiple coins of diﬀerent
currencies. For a resource type γ that provides a multiplication operation (∗) we
deﬁne the operator ⇓C with the following two rules.

                                      None ⇒ None |
   ⇓C E (res M) = res (λ r. case M r of
                Some t ⇒ Some (λcc . ca t ca ∗ E ca cc ))
   ⇓C E fail = fail
The reﬁned computation has the same results as the original. To get the amount
of a concrete coin cc for some result r with resource function t, we sum, over all
298       P. M. L. Haslbeck and P. Lammich

abstract coins ca , the amount of abstract coins needed in the original computa-
tion (t ca ) weighted by the exchange rate (E ca cc ).
    For the sum to make sense, there must be only ﬁnitely many abstract coins ca
with t ca ∗ E ca cc = 0. This can be ensured by restricting the resource functions
t of the computation to use ﬁnitely many diﬀerent coins, or by restricting the
exchange rate E accordingly. The latter can be checked syntactically in practice.

Example 5. For reﬁning the speciﬁcation idxs cmpspec we can use the exchange
rate E1 = 0(idxs cmp:= $lookup 2 + $less ), which does the correct exchange for
idxs cmp and is zero everywhere else. Here, + and 0 are lifted to functions in a
pointwise manner, and f(·:=·) denotes a function update. We can now prove:
      idxs cmp xs i j ≤ ⇓C E1 (idxs cmpspec xs i j ($idxs cmp ))


2.4     Reﬁnement Patterns
In practice, we encounter certain recurring patterns of reﬁnement, which we
describe in this section.

Reﬁnement of Speciﬁcations Instead of only asking whether a program m satisﬁes
a speciﬁcation res M, we also ask how much it satisﬁes the speciﬁcation, i.e.
what is the diﬀerence of the resources speciﬁed and actually used, denoted by
gwp m M.6 We have the following equality: m ≤ res M ⇔ Some 0 ≤ gwp m M.
    To get some intuition let us ﬁx the resource to be time. Then, gwp m M is
the latest feasible time at which we can start m to still match the deadline M.
If there is no feasible starting time (gwp m M = None), m does not fulﬁll the
speciﬁcation M. If it has some value t, this is the latest feasible starting time of
all computation paths in m.
    Using gwp, we can implement a syntax driven veriﬁcation condition genera-
tor, as already described in [11].

Lockstep Reﬁnement We often reﬁne a compound program by reﬁning some of
its components. Let A and C be two structurally equal programs (i.e., they have
the same structure of combinators ifc , recc , bind, etc.), and let Ai and Ci be the
pairs of corresponding basic components, for i∈{0,. . . ,n}. Provided with reﬁne-
ment lemmas Φi x ∧ (x† ,x) ∈ Ri =⇒ Ci x† ≤ ⇓D Ri (⇓C E (Ai x)) for each of
those pairs,7 an automatic procedure walks through the program and establishes
a reﬁnement C ≤ ⇓D Rn (⇓C E A). This process generates veriﬁcation conditions
for ensuring the preconditions Φi , which can be discharged automatically or, if
required, via interactive proof.
6
  The deﬁnition of gwp requires γ to provide a diﬀerence operator, dual to its +
  operator. It is a straightforward generalization of the concept deﬁned in [11], and
  thus omitted here. We only note that the resource types unit, enat, and ecost provide
  a suitable diﬀerence operator.
7
  The reﬁnement relations Ri and Ri relate the parameters and respectively the result
  of those components.
                                                    For a Few Dollars More     299

    Note that, while the data reﬁnements Ri can be diﬀerent for each component
i, the exchange rate E must be the same for all components. Currently, we align
the exchange rates by manually deriving specialized versions of the component
reﬁnement lemmas. However, we believe that this can be automated in many
practical cases, by collecting constraints on the exchange rate during the lockstep
reﬁnement, which are solved afterwards to obtain a uniﬁed exchange rate. We
leave the implementation of this idea to future work.

Separating Analysis of Resource Usage and Correctness We can disregard re-
source usage and only focus on reﬁnement of functional correctness, and then
add resource usage analysis later. This is useful to separate the concerns of func-
tional correctness and resource usage proof. We will describe a practical example
later (Section 5.5), and only present an alternative way to prove the reﬁnement
in Example 4 here:
    First, for functional correctness, we use the speciﬁcation idxs cmpspec (∞)
and a program idxs cmp∞ similar to idxs cmp but with all the costs replaced
by ∞. Proving the reﬁnement idxs cmp∞ xs i j ≤ idxs cmpspec xs i j (∞) only
requires showing veriﬁcation conditions that correspond to functional prop-
erties and termination. In particular, assertions and annotated invariants in
the concrete program have to be proved. Proof obligations on resource us-
age, however, collapse into the trivial t ≤ ∞. For the same reason, we get
idxs cmp xs i j ≤ idxs cmp∞ xs i j, and by transitivity obtain
    idxs cmp xs i j ≤ idxs cmpspec xs i j (∞)
Next, we prove idxs cmp xs i j ≤n spec (λ .True) ($lookup 2 + $less ). Here, the
reﬁnement relation m ≤n m = m = fail =⇒ m ≤ m assumes that the con-
crete program does not fail. This has the eﬀect that, during the reﬁnement proof,
assertions and annotated invariants in the concrete program can be assumed to
hold, and we can focus on the resource usage proof.
    Finally, the two reﬁnements can be combined to obtain
    idxs cmp xs i j ≤ idxs cmpspec xs i j ($lookup 2 + $less )


3     LLVM With Cost Semantics
The NREST-monad allows to specify programs with their resource usage in
abstract currencies. Those currencies only have a meaning when they ﬁnally
can be exchanged for the costs of concrete computations. In the following we
present such a concrete computation model, namely a shallow embedding of
the LLVM semantics into Isabelle/HOL. The embedding is an extension of our
earlier work [15] to also account for costs. In Section 4 we then report on linking
the LLVM back end with the NREST front end.

3.1   Basic Monad
At the basis of our LLVM formalization is a monad that provides the notions of
non-termination, failure, state, and execution costs.
300      P. M. L. Haslbeck and P. Lammich

      α mres = NTERM | FAIL | SUCC α cost state
      α M = state → α mres
Here, cost is a type for execution costs, which forms a monoid with operation +
and neutral element 0, and state is an arbitrary type.8
    The type α M describes a program that, when executed on a state, either
does not terminate (NTERM), fails (FAIL), or returns a result of type α, its
execution costs, and a new state (SUCC).
    It is straightforward to deﬁne the monad operations return and bind, as well
as a recursion combinator rec over M. Thanks to the shallow embedding, we can
also use Isabelle HOL’s if-then-else to get a complete set of basic operations. As
an example, we show the deﬁnition of the bind operation, in the case that both
arguments successfully compute a result:
      Assume m s = SUCC x c1 s1 and f x s1 = SUCC r c2 s2
      then we have bind m f s = SUCC r (c1 +c2 ) s2
That is, the result x and state s1 after the ﬁrst operation m is passed into the
second operation f, and the result and state after the bind is what emerges from
f. The cost for the bind is the sum of the costs for both operations.
    The basic monad operations do not cost anything. To account for execution
costs, we deﬁne an explicit operation consume c s = SUCC () c s.9


3.2     Shallowly Embedded LLVM Semantics

The formalization of the LLVM semantics is organized in layers. At the bot-
tom, there is a memory model that stores deeply embedded values, and comes
with basic operations for allocation/deallocation, loading, storing, and pointer
manipulation. Also the basic arithmetic operations are deﬁned on deeply em-
bedded integers. These operations are phrased in the basic monad, but consume
no costs. This way, we could take them unchanged from our original LLVM for-
malization without cost [15]. For example, the low-level load operation has the
signature raw load :: raw ptr → val M. Here, raw ptr is the pointer type of our
memory model, consisting of a block address and an oﬀset, and val is our value
type, which can be an integer, a pointer, or a pair of values.
    On top of the basic layer, we deﬁne operations that correspond to the actual
LLVM instructions. Here, we map from deeply embedded values to shallowly
embedded values, and add the execution costs.
    For example, the semantics of LLVM’s load instruction is deﬁned as follows:
8
  Note that this diﬀers from the NREST monad in Section 2.1: it is deterministic,
  and provides a state. Because of determinism, we never need to form a supremum,
  and thus can base our cost model on natural numbers rather than enats. We leave
  a uniﬁcation of the two monads to future work.
9
  For NREST, we deﬁned a higher-order operation elapse, while we use the ﬁrst-
  order operation consume here. This is for historical reasons. Note that elapse can
  be deﬁned in terms of consume, and vice versa.
                                                        For a Few Dollars More        301

     ll load :: α ptr → α M
     ll load p =
       consume $load ;
       r ← raw load (the raw ptr p);
       checked from val r

It consumes the cost10 for the operation, and then forwards to the raw load
operation of the lower layer, where the raw ptr and checked from val convert
between the shallow and deep embedding of values.
    Like in the original formalization11 , an LLVM program is represented by a
set of monomorphic constant deﬁnitions of the shape def, deﬁned as follows:

     def = proc name var∗ ≡ block
     block = var ← cmd; block | return var
     cmd = ll <opcode> arg∗ | ll call proc name arg∗ | llc if arg block block
           | llc while block block
     arg = var | number | null | init

The code generator checks that the set of deﬁnitions is complete and adheres
to the required shape. It then translates them into LLVM code, which merely
amounts to pretty printing and translating the structured control ﬂow by if
and while12 statements to the unstructured control ﬂow of LLVM. A powerful
preprocessor can convert a more general class of terms to the restricted shape
required by the code generator. This conversion is done inside the logic, i.e.,
the processed program is proved to be equal to the original. Preprocessing steps
include monomorphization of polymorphic constants, extraction of ﬁxed-point
combinators to recursive function deﬁnitions, and conversion of tuple construc-
tors and destructors to LLVM’s insertvalue and extractvalue instructions.
    In summary, the layered architecture of our LLVM formalization allowed for
a smooth integration of the cost aspect, reusing most of the existing formaliza-
tion nearly unchanged. Note that we opted to integrate the cost aspect into the
existing top layer, which converts between deep and shallow embedding. Alter-
natively, we could have added another layer on top of the shallow embedding.
While the latter would have been the cleaner design, we opted for the former
approach to avoid the boilerplate of adding a new layer. This was feasible as the
original top layer was quite thin, such that adding another aspect there did not
result in excessive complexity.

10
   See Section 3.3 for an explanation of our cost model.
11
   Actually, the only change to the original formalization is the introduction of the
   ll call instruction, to make the costs of a function call visible.
12
   Primitive while loops are not strictly required, as they can always be replaced by tail
   recursion. Indeed, our code generator can be conﬁgured to not accept while loops, and
   our preprocessor can automatically convert while loops to tail-recursive functions.
   However, the eﬃciency of the generated code then relies on LLVM’s optimization
   pass to detect the tail recursion and transform it to a loop again.
302    P. M. L. Haslbeck and P. Lammich

3.3   Cost Model

As a cost model for running time, we chose to count how often each instruction is
executed. That is, we set cost = string → nat, where the string encodes the name
of an instruction. It is straightforward to deﬁne 0 and + such that (cost,0,+)
forms a monoid. It is thus a valid cost model for our monad.
    But how realistic is our cost model, counting LLVM instructions? During
compilation, LLVM text will be transformed by LLVM’s optimizer, and ﬁnally,
the LLVM’s back end will translate LLVM instructions to machine instructions.
Moreover, the actual running time of a machine program does not only depend
on the number of executed instructions, but eﬀects like pipeline ﬂushes and cache
misses also play an important role. Thus, without factoring in the details of the
optimization passes and the target machine architecture, our cost model can, at
best, be a rough approximation of the actual running time.
    However, we can sensibly assume that a single instruction in the original
LLVM text will result in at most a (small) constant number of machine instruc-
tions, and that each machine instruction has a constant worst-case execution
time. Thus, the steps counted by our model linearly correlate to an upper bound
of the actual execution time, though the exact correlation depends on the actual
program, optimizer passes, and target architecture. Hence, while our cost model
cannot be used for precise statements about execution time, it can be used to
prove worst-case complexity. That is, a program that we have proved eﬃcient
will be compiled to an eﬃcient machine program. Moreover, we can hope that
the constant factors in the proved complexity are related to the actual constant
factors in the machine program, i.e., an LLVM program with small constant
factors will compile to a machine program with small constant factors.
    The above discussion justiﬁes the following design choices: The insertvalue
and extractvalue instructions, which are used to construct and destruct tuple
values, have no associated costs. The main reason for this design is to enable
transparent use of tupled values, e.g., to encode the state of a while loop. We
expect LLVM to translate the members of the tuple to separate registers anyway,
such that no real costs are associated with tupling/untupling.
    We deﬁne the malloc instruction to take cost proportional to the number
of allocated elements. Note that LLVM itself does not provide memory man-
agement, and our code generator forwards memory management instructions to
the libc implementation of the target platform. We use the calloc function here,
which is supposed to initialize the allocated memory with zeros. While the exact
costs of that are implementation dependent, they certainly will depend on the
size of the allocated block.
    Charguéraud and Pottier [6, §2.7] discuss the adequacy of abstract cost mod-
els in a functional setting. In their classiﬁcation, our abstraction is on Level 2.


3.4   Reasoning Setup

Once we have deﬁned the semantics, we need to set up some basic reasoning
infrastructure. The original Isabelle-LLVM already comes with a quite generic
                                                       For a Few Dollars More       303

separation logic and veriﬁcation condition generation framework. Here, we report
on our extensions to resources using time credits.

Separation Logic with Time Credits Our reasoning infrastructure is based on
separation logic with time credits [1,6,10]. We follow the algebraic approach of
Calcagno et al. [3], using an earlier extension [15] of Klein et al. [18].
    A separation algebra on type α induces a separation logic on assertions that
are predicates over α. To guide intuition, elements of α are called heaps here. We
use the following separation logic operators: The assertion ↑Φ holds for an empty
heap if Φ holds, =↑True describes the empty heap, and ∃A is the existential
quantiﬁer lifted to assertions. The separating conjunction P  Q describes a heap
comprised from two disjoint parts, one described by P and the other described
by Q, and entailment P  Q states that Q holds for every heap described by P.
    Separation algebras naturally extend over product and function types, i.e., for
separation algebras α, β, and any type γ, also α × β and γ → α are separation
algebras, where the operations are lifted pointwise.
    Note that enat forms a separation algebra, where elements, i.e. time credits,
are always disjoint. Hence, also ecost = string → enat, and amemory × ecost are
separation algebras, where amemory is the separation algebra that we already
used in [15] to describe the abstract memory of LLVM. Thus, amemory × ecost
induces a separation logic with time credits that match our cost model. The
time credit assertion $ c = (λa. a=(0,c)) describes an empty memory (0) and
precisely the time c. The primitive assertions on amemory are lifted analogously
to describe no time credits.

Weakest Precondition and Hoare Triples We start by deﬁning a concrete state
cstate that describes the memory content and the available resources:
   cstate = memory × ecost
where memory is the memory type from our original LLVM formalization. Based
on this, we deﬁne the weakest precondition predicate:
 wp :: α M → (α → cstate → bool) → cstate → bool
 wp m Q (s,cc) = (∃r c s. m s = SUCC r c s ∧ c≤cc ∧ Q r (s, cc−c)).
Intuitively, the costs cc stored in the state is the credit available to the program.
The weakest precondition holds if the program runs with real costs c that are
within the available credit, and Q holds for the result r, the new memory s, and
the new credit, cc−c, which is the old credit reduced by the actually required
costs. Note that actual costs have type cost = string → nat, i.e., are always
ﬁnite, while the credits have type ecost = string → enat, i.e., there can be inﬁnite
credits. Setting the credit to be inﬁnite for all instruction types yields the classical
weakest precondition that requires termination, but enforces no time limit.
    Our concrete state type, in particular the memory, does not form a separation
algebra, as the natural memory model of LLVM has no natural notion of partial
memories. Thus, we deﬁne an abstraction function that maps a concrete state
to an abstract state astate, which forms a separation algebra:
304       P. M. L. Haslbeck and P. Lammich

      astate = amemory × ecost                 abs (m, c) = (absm m, c)
Again, amemory and absm is the abstract state and abstraction function from
the original LLVM formalization. The costs already form a separation algebra,
so we do not abstract them further.
    With this, we can instantiate a generic VCG infrastructure: let cstate be
concrete states, wp :: α M → (α → cstate → bool) → cstate → bool be a weak-
est precondition predicate, and astate an abstract state, linked to concrete states
via an abstraction function abs :: cstate → astate. Further, assume that wp dis-
tributes over conjunctions, i.e.,
      wp c Q1 s ∧ wp c Q2 s =⇒ wp c (λr s. Q1 r s ∧ Q2 r s) s
Finally, let 
              be an aﬃne top [5], i.e., an assertion with   
                                                                and 
                                                                     
                                                                       =   ,
which captures resources that can be safely discarded. We deﬁne the Hoare triple
{P} c {Q} to hold iﬀ:
      ∀F s. (PF) (abs s) =⇒ wp c (λr s. (Q r  
                                                   F) (abs s)) s
Intuitively, {P} c {Q} holds if, for all states that contain a part described by
assertion P, command c terminates with result r and a state where that part
is replaced by a part described by Q r    , and the rest of the state has not
changed. Here, Q r is the postcondition of the Hoare triple, and     describes
resources that may be left over and can be discarded.
    In our case, we set 
                         to describe the empty memory and any amount of time
credits. This matches the intuition that a program must free all its memory, but
may run faster than estimated, i.e., leave over some time credits. Note that our
wp distributes over conjunctions.
    The generic VCG infrastructure now provides us with a syntax driven VCG
with a simple frame inference heuristics.


3.5     Primitive Setup

Once we have deﬁned the basic reasoning infrastructure, we have to prove Hoare
triples for the basic LLVM instructions and control ﬂow combinators. As we have
added the cost aspect only at the top level of our semantics, we can reuse most of
the material from our original LLVM formalization without time. Technically, we
instantiate our reasoning infrastructure with a weakest precondition predicate
wpn, which only holds for programs that consume no costs. We deﬁne:
      wpn m Q s = wp m (FST ◦ Q) (s,0) where FST P = λ(s,c). P s ∧ c=0
    The resulting reasoning infrastructure is identical with the one of our original
formalization, most of which could be reused. Only for the topmost level, i.e., for
those functions that correspond to the functional semantics of the actual LLVM
instructions, we lift the Hoare triples over wpn to Hoare triples over wp:
      {P} c {Q}wpn = {FST P} c {FST ◦ Q}
                                                    For a Few Dollars More         305

Example 6. Recall the low-level raw load and the high-level ll load instruction
from Section 3.2. The raw load instruction consumes no costs, and our original
LLVM formalization provides the following Hoare triple:
    {raw pto p x} raw load p {λr. ↑(r=x)  raw pto p x}wpn
This can be transferred to a Hoare triple over wp:
    {FST (raw pto p x)} raw load p {λr. ↑(r=x)  FST (raw pto p x)}
which is then used to prove the Hoare triple for the program ll load
    { $ $load  pto p x} ll load p {λr. ↑(r=x)  pto p x}
where pto p x = FST (raw pto (the raw ptr p) (to val x)).

Using the VCG and the Hoare triples for the LLVM instructions, we can now de-
ﬁne and prove correct data structures and algorithms. While this works smoothly
for simple data structures like arrays, it does not scale to more complex develop-
ments. In contrast, NREST does scale, but lacks support for the low-level pointer
reasoning required for basic data structures. In the next section, we show how to
combine both approaches, with the LLVM level providing basic data structures
and the NREST level using them as building blocks for larger algorithms.


4     Automatic Reﬁnement
In this section we describe a tool to synthesize a concrete program in the LLVM-
monad from an abstract algorithm in the NREST-monad. It can automatically
reﬁne abstract functional data structures to imperative heap-based ones. We
will describe the synthesis predicate hnr that connects the two monads, the
synthesis tool, and a way to extract Hoare triples from hnr predicates. Finally,
we will discuss an eﬀect that prevents combining hnr with data reﬁnements in
the NREST-monad in the general case.

4.1   Heap nondeterminism reﬁnement
The heap nondeterminism reﬁnement predicate hnr Γ m† Γ  R m intuitively ex-
presses that the concrete program m† computes a concrete result that relates, via
the reﬁnement assertion R, to a result in the abstract program m, using at most
the resources speciﬁed by m for that result. A reﬁnement assertion describes
how an abstract variable is reﬁned by a concrete value on the heap. It can also
contain time credits. The assertions Γ and Γ  constitute the heaps before and
after the computation and typically are a separating conjunction of reﬁnement
assertions for the respective parameters of m† and m. Formally, we deﬁne:
    hnr Γ m† Γ  R m = m = fail =⇒
     (∀F s c. (Γ  F) (absm s,c) =⇒
        (∃ra ca . elapse (return ra ) ca ≤ m
          ∧ wp m† (λr (s,c). (Γ   R r ra  F  
                                                   ) (absm s,c)) (s, c+ca )))
306       P. M. L. Haslbeck and P. Lammich

The predicate holds if either the abstract program fails or if, for all heaps and
resources (s,c) that satisfy the pre-assertion Γ with some frame F, there exists an
abstract result and cost (ra ,ca ) that reﬁne m, and m† terminates with concrete
result r in a state s where Γ  with the frame holds, and r relates to the abstract
result via assertion R. The execution costs of m† and the time credits c required
by the post-assertion Γ  are paid for by the speciﬁed cost ca and the time credits
c described by the pre-assertion Γ . Thus, the real costs are paid by a combination
of the advertised costs in the abstract program and the potential diﬀerence of
Γ  and Γ , allowing to seamlessly model amortized computation costs.
     Using the aﬃne top  , it is possible for the program to throw away portions
of the heap. Note that our     can only discard time credits. Memory must be
explicitly freed by the concrete program m† .
     Also note that hnr is not tied to the LLVM semantics speciﬁcally. It actually
is a general pattern for combining the NREST-monad with any other program
semantics that provides a weakest precondition and a separation algebra for data
and resources.


4.2     The Sepref Tool

The Sepref tool [14,15] automatically synthesizes a concrete program in the
LLVM-monad from an abstract algorithm in the NREST-monad. It symbolically
executes the abstract program while maintaining reﬁnements for the abstract
variables to a concrete representation and generates a concrete program as well
as a valid hnr predicate. Proof obligations13 that occur during this process are
discharged automatically, guided by user-provided hints where necessary.
    The synthesis requires rules for all abstract combinators. For example, bind
is processed by the following rule:
1          hnr Γ m† Γ  Rx m;
2           (∀x x† . hnr (Rx x† x  Γ  ) (f† x† ) (Rx x† x  Γ  ) Ry (f x));
3           MK FREE Rx free  =⇒
4         hnr Γ (x† ← m† ; r† ← f† x† ; free x† ; return r† ) Γ  Ry (x ← m; f x)
To reﬁne x ← m; f x, we ﬁrst execute m, synthesizing the concrete program
m† (line 1). The state after m is Rx x† x  Γ , where x is the result created
by m. From this state, we execute f x and synthesize f† x† (line 2). The new
state is Rx x† x  Γ   Ry y† y, where y is the result of f x. Now, the inter-
mediate variable x goes out of scope and has to be deallocated. The predicate
MK FREE Rx free (line 3) states that free is a deallocator for data structures
implemented by reﬁnement assertion Rx . Note that free can only use time credits
that are stored in Rx . Typically, these are payed for during creation of the data
structure. This way amortization can be used eﬀectively to hide the necessary
free operation and its costs in the abstract program.
    All other combinators (recc , ifc , whilec , etc.) have similar rules that are
used to decompose an abstract program into parts, synthesize corresponding con-
13
     E.g. from implementing mathematical integers with ﬁxed-bit machine words.
                                                    For a Few Dollars More     307

crete parts recursively and combine them afterwards with the respective combi-
nators from LLVM. At the leaves of this decomposition, atomic operations need
to be provided with suitable synthesis predicates.
    An example is a list lookup that is implemented by an array:
   hnr (arrayA p xs  snatA i† i)
      (array nth p i† )
    (arrayA p xs  snatA i† i) idA (list getspec xs i (λ . array getcost ))
where arrayA , snatA and idA relate a list with an array, an unbounded natural
number with a bounded signed word and identical elements respectively. With
an array at address p holding the list xs and an index i† that is a bounded
signed word representing an unbounded natural number i, array nth leaves the
parameters unchanged and extracts the element speciﬁed by list getspec incurring
costs array getcost =$of s ptr + $load .
    Ideally, each operation has its own currency (e.g. list get). However, as our
deﬁnition of hnr does not support currency reﬁnement, the basic operations must
use the currencies of the LLVM cost model. To still obtain modular hnr rules,
we encapsulate speciﬁcations for data structures with their cost, e.g. by deﬁning
array getspec =list getspec (λ . array getcost ). These can easily be introduced in
an additional reﬁnement step. Automating this process, and possibly integrating
currency reﬁnement into hnr is left to future work.

4.3   Extracting Hoare Triples
Note that hnr predicates cannot always be expressed as Hoare triples, as the
running time bound of the abstract program may depend on the result, which
we cannot refer to in the precondition of a Hoare triple, where we have to express
the allowed running time as time credits. However, if the running time bound
does not depend on the result, we can write hnr as a Hoare triple:
hnr Γ m† Γ  R (spec Φ (λ .T)) = {$T Γ }m† {λr. Γ ∃A ra . R r ra  ↑(Φ ra )}
While intermediate components might not be of this form, ﬁnal algorithms typ-
ically are. At the end of a development, this rule allows to extract a Hoare triple
in the underlying LLVM semantics, cutting out the NREST-monad. For validat-
ing the correctness claim of an algorithm, only the ﬁnal Hoare triple needs to be
inspected, which only uses concepts of the underlying semantics.
    Note that the above rule is an equivalence. Thus, it can also be used to obtain
synthesis rules from Hoare triples provided by the basic VCG infrastructure.

4.4   Attain Supremum
We comment on a problem that arises when composing hnr predicates and data
reﬁnement in the NREST monad. Consider the following programs and relations:
   m = res [x → $a , y → $b ]                        RR = {(z,a),(z,b)}
   m = res [z → $a + $b ]                              RA = idA
   m† = consume ($a + $b ); return z
308       P. M. L. Haslbeck and P. Lammich

Data reﬁnement deﬁnes the resource bound for a concrete result (here z) as
the supremum over all bounds of related results (here x, y). Thus, we have
m ≤ ⇓C RR m. Moreover, we trivially have hnr  m†  RA m. Intuitively, we
want to compose these two reﬁnements, to obtain hnr  m†  (RA ◦ RR ) m.
However, as our deﬁnition of hnr does not form a supremum, this would require
$a + $b ≤ $a or $a + $b ≤ $b , which obviously does not hold.
    We have not yet found a way to deﬁne hnr or ⇓D in a form that does not
exhibit this eﬀect. Instead, we explicitly require that the supremum of the data
reﬁnement has a witness. The predicate attains sup m m RR characterizes that
situation: it holds, if for all results r of m the supremum of the set of all ab-
stractions (r,r)∈RR applied to m is in that set. This trivially holds if RR is
single-valued, i.e. any concrete value is related with at most one abstract value,
or if m is one-time, i.e. assigns the same resource bound to all its results.
    In practice we do encounter non-single-valued relations14 , but they only oc-
cur as intermediate results where the composition with an hnr predicate is not
necessary. Also, collapsing synthesis predicates and reﬁnements in the NREST-
monad typically is performed for the ﬁnal algorithm whose running time does
not depend on the result, thus is one-time, and ultimately attains sup.


5      Case Study: Introsort
In this section, we apply our framework to the introsort algorithm [22]. We build
upon the veriﬁcation of its functional correctness [17] to verify its running time
analysis and synthesize competitive eﬃcient LLVM code for it. Following the
“top-down” mantra, we use several intermediate steps to reﬁne a speciﬁcation
down to an implementation.

5.1      Speciﬁcation of Sorting
We start with the speciﬁcation of sorting a slice of a list:
      slice sortspec xs0 l h (T) =
        assert (l≤h ∧ h≤length xs0 );
        spec (λxs. slice sort aux xs0 l h xs) (λ . T)
where slice sort aux xs0 l h xs states that xs is a permutation of xs0 , xs is sorted
between l and h and equal to xs0 anywhere else.

5.2      Introsort’s Idea
The introsort algorithm is based on quicksort. Like quicksort, it ﬁnds a pivot
element, partitions the list around the pivot, and recursively sorts the two par-
titions. Unlike quicksort, however, it keeps track of the recursion depth, and if it
14
     The relation oarr, described in earlier work [17, 4.2] by one of the authors, is used
     to model ownership of parts of a list on an abstract level and is an example for a
     relation that is not single-valued.
                                                            For a Few Dollars More   309

exceeds a certain value (typically '2 log n(), it falls back to heapsort to sort the
current partition. Intuitively, quicksort’s worst-case behaviour can only occur
when unbalanced partitioning causes a high recursion depth, and the introsort
algorithm limits the recursion depth, falling back to the O(n log n) heapsort al-
gorithm. This combines the good practical performance of quicksort with the
good worst-case complexity of heapsort.
    Our implementation of introsort follows the implementation of libstdc++,
which includes a second optimization: a ﬁrst phase executes quicksort (with
fallback to heapsort), but stops the recursion when the partition size falls below
a certain threshold τ . Then, a second phase sorts the whole list with one ﬁnal
pass of insertion sort. This exploits the fact that insertion sort is actually faster
than quicksort for almost-sorted lists, i.e., lists where any element is less than
τ positions away from its ﬁnal position in the sorted list. While the optimal
threshold τ needs to be determined empirically, it does not inﬂuence the worst-
case complexity of the ﬁnal insertion sort, which is O(τ n) = O(n) for constant
τ . The threshold τ will be an implicit parameter from now on.
    While this seems like a quite concrete optimization, the two phases are al-
ready visible in the abstract algorithm, which is deﬁned as follows in NREST:
     introsort xs l h =
       assert(l ≤ h);
       n ← return h−l;                    ($sub )
       ifc n > 1 then                     ($lt )
         xs ← almost sortspec xs l h;     ($almost sort )
         xs ← ﬁnal sortspec xs l h        ($f inal sort )
         return xs
       else return xs
where almost sortspec (T) speciﬁes an algorithm that almost-sorts a list, con-
suming at most T resources and ﬁnal sortspec (T) speciﬁes an algorithm that
sorts an almost-sorted list, consuming at most T resources.
    The program introsort leaves trivial lists unchanged and otherwise executes
the ﬁrst and second phase. Its resource usage is bounded by the sum of the
ﬁrst and second phase and some overhead for the subtraction, comparison, and
if-then-else. Using the veriﬁcation condition generator we prove that introsort is
correct, i.e., reﬁnes the speciﬁcation of sorting a slice:
     introsort xs l h ≤ ⇓C Eis (slice sortspec xs l h ($sort ))
where Eis = 0(sort:=introsortcost ) is the exchange rate used at this step and
introsortcost = $sub + $if + $lt + $almost sort + $f inal sort is the total allotted
cost for introsort.


5.3    Quicksort Scheme

The ﬁrst phase can be implemented in the following way:
 1        introsort aux μ xs l h =
310       P. M. L. Haslbeck and P. Lammich

 2          d ← depthspec l h;                     ($depth )
 3          recc (λintrosort rec (xs,l,h,d).
 4            assert (l ≤ h);
 5            n ← h−l;                             ($sub )
 6            ifc n > τ then                       ($lt )
 7              ifc d = 0 then                     ($eq )
 8               slice sortspec xs l h             ($sortc (μ (h-l)))
 9              else
10               (xs,m) ← partitionspec xs l h;    ($partitionc (h-l))
11               d ← d − 1;                       ($sub )
12               xs ← introsort rec (xs,l,m,d);
13               xs ← introsort rec (xs,m,h,d);
14               return xs
15            else return xs
16          ) (xs,l,h,d)
where partitionspec partitions a slice into two non-empty partitions, returning
the start index m of the second partition, and depthspec speciﬁes '2 log(h − l)(.
     Let us ﬁrst analyze the recursive part: if the slice is shorter than the threshold
τ , it is simply returned (line 15). Unless the recursion depth limit is reached,
the slice is partitioned using h − l partitionc coins, and the procedure is called
recursively for both partitions (lines 10-14). Otherwise, the slice is sorted at a
price of μ (h−l) sortc coins (line 8). The function μ here represents the leading
term in the asymptotic costs of the used sorting algorithm, and the sortc coin
can be seen as the constant factor. This currency will later be exchanged into
the respective currencies that are used by the sorting algorithm. Note that we
use currency sortc to describe costs per comparison of a sorting algorithm, while
currency sort describes the cost for a whole sorting algorithm.
     Showing that the procedure results in an almost-sorted list is straightforward.
The running time analysis, however, is a bit more involved. We presume a func-
tion μ that maps the length of a slice to an upper bound on the abstract steps
required for sorting the slice. We will later use heapsort with μnlogn n = n log n.
     Consider the recursion tree of a call in introsort rec: We pessimistically as-
sume that for every leaf in the recursion tree we need to call the fallback sorting
algorithm. Furthermore, we have to partition at every inner node. This has cost
linear in the length of the current slice. For each following inner level the lengths
of the slices add up to the current one’s, and so do the incurred costs. Finally
we have some overhead at every level including the ﬁnal one. The cost of the
recursive part of introsort aux is:
      introsort reccost μ (n,d) = $sortc (μ n) + $partitionc d ∗ n
        + ((d+1)∗n)∗($if 2 + $call 2 + $eq + $lt + $sub 2)
The correctness of the running time bound is proved by induction over the
recursion of introsort rec. If the recursion limit is reached (d=0), the ﬁrst sum-
mand pays for the fallback sorting algorithm. If d>0, part of the second sum-
mand pays for the partitioning of the current slice, then the list is split into
                                                            For a Few Dollars More         311

two and the recursive costs are payed for by parts of all three summands. To
bound the costs for the fallback sorting algorithm, μ needs to be superadditive:
μ a + μ b ≤ μ (a+b). In both cases, the third summand pays for the overhead
in the current call.
    For d='2 log n( and an O(n log n) fallback sorting algorithm (μ=μnlogn ),
introsort reccost μnlogn is in O(n log n).15 In fact, any d∈O(log n) would do.
    Before executing the recursive method, introsort aux calculates the depth
limit d. The correctness theorem then reads:
introsort aux μnlogn xs l h ≤ ⇓C (Eisa (h−l))(almost sortspec xs l h $almost sort )
with Eisa n = 0(almost sort:= $depth + introsort reccost μnlogn (n, '2 log n()).
    Note that speciﬁcations typically use a single coin of a speciﬁc currency for
their abstract operation, which is then exchanged for the actual costs, usually
depending on the parameters.
    This concludes the interesting part of the running time analysis of the ﬁrst
phase. It is now left to plug in an O(n log n) fallback sorting algorithm, and a
linear partitioning algorithm.

Heapsort Independently of introsort, we have proved correctness and worst-case
complexity of heapsort, yielding the following reﬁnement lemma:
      heapsort xs l h ≤ ⇓C (Ehs (h−l)) (slice sortspec xs l h ($sort ))
where Ehs n = 0(sort:= c1 + log n ∗ c2 + n ∗ c3 + (n ∗ log n) ∗ c4 ) for some
constants ci :: ecost.
    Assuming that n ≥ 2,16 we can estimate Ehs n sort ≤ μnlogn n ∗ c, for c =
c1 + c2 + c3 + c4 , and thus get, for Ehs = 0(sortc := c):
      ⇓C (Ehs (h−l)) (slice sortspec xs l h ($sort ))
      ≤ ⇓C Ehs (slice sortspec xs l h ($sortc (μnlogn (h−l))))
and, by, transitivity
      heapsort xs l h ≤ ⇓C Ehs (slice sortspec xs l h ($sortc (μnlogn (h−l))))
Note that our framework allowed us to easily convert the abstract currency from
a single operation-speciﬁc sort coin to a sortc coin for each comparison operation.

Partition and Depth Computation We implement partitioning with the Hoare
partitioning scheme using the median-of-3 as the pivot element. Moreover, we
implement the computation of the depth limit (2'log(h − l)() by a loop that
counts how often we can divide by two until zero is reached. This yields the
following reﬁnement lemmas:
     pivot partition xs l h ≤ ⇓C Epp (partitionspec xs l h ($partitionc (h−l)))
      calc depth l h ≤ ⇓C (Ecd (h−l)) (depthspec l h ($depth ))

15
     More precisely, the sum over all (ﬁnitely many) currencies is in O(n log n).
16
     Note that this is a valid assumption, as heapsort will never be called for trivial slices.
312       P. M. L. Haslbeck and P. Lammich

Combining the Reﬁnements We replace slice sortspec , partitionspec and depthspec
by their implementations heapsort, pivot partition and calc depth. We call the
resulting implementation introsort aux2 , and prove
      introsort aux2 xs l h ≤ ⇓C (Eaux (h−l)) (introsort aux μnlogn xs l h)
where the exchange rate Eaux combines the exchange rates Ehs , Epp and Ecd
for the component reﬁnements.
    Transitive combination with the correctness lemma for introsort aux then
yields the correctness lemma for introsort aux2 :
  introsort aux2 xs l h ≤ ⇓C (Eisa2 (h−l)) (almost sortspec xs l h ($almost sort ))
where Eisa2 n = 0(almost sort:=↓C (Eaux n) (introsort auxcost n)) and the op-
eration ↓C E t applies an exchange rate to a resource function.

Reﬁning Resources The stepwise reﬁnement approach allows to structure an
algorithm veriﬁcation in a way that correctness arguments can be conducted
on a high level and implementation details can be added later. Resource cur-
rencies permit the same for the resource analysis of algorithms: they summa-
rize compound costs, allow reasoning on a higher level of abstraction and can
later be reﬁned into ﬁne-grained costs. For example, in the resource analysis
of introsort aux the currencies sortc and partitionc abstract the cost of the re-
spective subroutines. The abstract resource argument is independent from their
implementation details, which are only added in a subsequent reﬁnement step,
via the exchange rate Eaux .

5.4     Final Insertion Sort
The second phase is implemented by insertion sort, repeatedly calling the sub-
routine insert. The speciﬁcation of insert for an index i captures the intuition
that it goes from a slice that is sorted up to index i−1 to one that is sorted up
to index i. Insertion is implemented by moving the last element to the left, as
long as the element left of it is greater (or the start of the list has been reached).
Moving an element to its correct position takes at most τ steps, as after the
ﬁrst phase the list is almost sorted, i.e., any element is less than τ positions
away from its ﬁnal position in the sorted list. Moreover, elements originally at
positions greater τ will never reach the beginning of the list, which allows for the
unguarded optimization. It omits the bounds check for those elements, saving
one index comparison in the innermost loop. Formalizing these arguments yields
the implementation ﬁnal insertion sort that satisﬁes
  ﬁnal insertion sort xs l h ≤ ⇓C (Ef is (h−l)) (ﬁnal sortspec xs l h ($f inal sort ))
where Ef is n = 0(ﬁnal sort:=ﬁnal insertioncost n), and ﬁnal insertioncost n is
linear in n.
    Note that ﬁnal insertion sort and introsort aux2 use the same currency sys-
tem. Plugging both reﬁnements into introsort yields introsort2 and the lemma
  introsort2 xs l h ≤ ⇓C (Eis2 (h−l)) (introsort xs l h)
where the exchange rate Eis2 combines the rates Eisa2 and Ef is .
                                                       For a Few Dollars More    313

5.5     Separating Correctness and Complexity Proofs

A crucial function in heapsort is sift down, which restores the heap property
by moving the top element down in the heap. To implement this function, we
ﬁrst prove correct a version sift down1 , which uses swap operations to move the
element. In a next step, we reﬁne this to sift down2 , which saves the top element,
then executes upward moves instead of swaps, and, after the last step, moves
the saved top element to its ﬁnal position. This optimization spares half of the
memory accesses, exploiting the fact that the next swap operation will overwrite
an element just written by the previous swap operation.
    However, this reﬁnement is not structural: it replaces swap operations by
move operations, and adds an additional move operation at the end. At this
point, we chose to separate the functional correctness and resource aspect, to
avoid the complexity of a combined non-structural functional and currency
reﬁnement. It turns out that proving the complexity of the optimized ver-
sion sift down2 directly is straightforward. Thus, as sketched in Section 2.4, we
ﬁrst prove17 sift down2 ≤ sift down1 ≤ sift downspec (∞), ignoring the resource
aspect. Separately, we prove sift down2 ≤n spec (λ . True) sift downcost , and
combine the two statements to get sift down2 ≤ sift downspec sift downcost .


5.6     Reﬁning to LLVM

The above abstract programs implicitly come with a ﬁxed type and comparison
operator for the elements of the list to be sorted. Those programs use abstract
operations and currencies for arithmetic operations on indexes, control ﬂow,
comparisons and read/write of a random-access iterator (abstracted by lists with
update and lookup operations).
   When we further assume an LLVM program that reﬁnes the comparison
operator in LLVM, and specify how the random-access data structure should be
implemented — we choose arrays — we can automatically synthesize an LLVM
program introsort impl that reﬁnes introsort2 , i.e., satisﬁes the theorem:
      hnr (arrayA p xs  snatA l† l  snatA h† h)
         (introsort impl p l† h† )
       (snatA l† l  snatA h† h) arrayA (introsort2 xs l h)
Combination with the reﬁnement lemmas for introsort2 and introsort, followed
by conversion to a Hoare triple, yields our ﬁnal correctness statement:
l ≤ h ∧ h < length xs0 =⇒
{$(introsort implcost (h−l))  arrayA p xs0  snatA l† l  snatA h† h}
   introsort impl p l† h†
{λr. ∃A xs. arrayA r xs  ↑(slice sort aux xs0 l h xs)  snatA l† l  snatA h† h}
where introsort implcost :: nat → ecost is the cost bound obtained from applying
the exchange rates Eis and then Eis2 to $sort .
17
     Note that we have omitted the function parameters for better readability.
314       P. M. L. Haslbeck and P. Lammich

    Note that this statement is independent of the Reﬁnement Framework. Thus,
to believe in its meaningfulness, one has to only check the formalization of Hoare
triples, separation logic, and the LLVM semantics.
    To formally prove the statement “introsort impl has complexity O(n log n)”,
we observe that introsort implcost uses only ﬁnitely many currencies, and only
ﬁnitely many coins of each currency. We deﬁne the overall number of coins as
      introsort implallcost n = Σc. introsort implcost n c
which expands to
      introsort implallcost n = 4693 + 5 ∗ log n + 231 ∗ n + 455 ∗ (n ∗ log n)
which, in turn, is routinely proved to be in O(n log n).
   As a last step, we instantiate the element type to 64-bit unsigned integers and
the comparison operation to LLVM’s icmp ult instruction, to obtain a program
that sorts integers in ascending order. Our code generator can export this to
actual LLVM text and a corresponding header ﬁle for interfacing our sorting
algorithm from C or C++.
   As LLVM does not support generics, we cannot implement a replacement for
C++’s generic std::sort<T>. However, by repeating the last step for diﬀerent
types and compare operators, we can implement a replacement for any ﬁxed T.

5.7     Benchmarks
In this section we present benchmarks comparing the code extracted from our
formalization with the real world implementation of introsort from the GNU
C++ Library (libstdc++). Also, as a regression test, we compare with the code
extracted from an earlier formalization of introsort [17] that did not verify the
running time complexity and used an earlier iteration of the Sepref framework
and LLVM semantics without time.
    The results are shown in Figure 1. As expected, all three implementations
have similar running times. Note that the small diﬀerences are well within the
noise of the measurements. We conclude that adding the complexity proof to our
introsort formalization, and the time aspect to our reﬁnement process has not
introduced any timing regressions in the generated code. Note, however, that the
code generated by our current formalization is not identical to what the original
formalization generated. This is mainly due to small changes in the formalization
introduced when adding the timing aspect.


6      Conclusions
We have presented a reﬁnement framework for the simultaneous veriﬁcation of
functional correctness and complexity of algorithm implementations with com-
petitive practical performance.
   We use stepwise reﬁnement to separate high-level algorithmic ideas from
low-level optimizations, enabling convenient veriﬁcation of highly optimized al-
gorithms. The novel concept of resource currencies also allows structuring of the
                                                                           For a Few Dollars More                 315


                                                                              Isabelle-LLVM
               10                                                             Isabelle-LLVM (notime)

                                                                              libstdc++
      Time/s




                5



                0
                                                           l
                        10 -1 .1 50 n pe 10 a .1 ed -1 10 m .1 ed -1 .1 10 -1 10 .1 -1 10
                   n d--endendt-ed- olena-pi nd- equdles-ortddledle- ndoteds-ortddledlet-ed-rteddle-end--endup-
                 e                   o           e     d - i d a r m i i d or so i d d - e d - d
              d - t e d e d - sor - b r g a d -     mi ev -m i r -so         - m s - rte r t o m
          rte-sorsortost-dom o orte ted- rteded-m ost tedted-ost- osted-m                        o d
     -  o
       s ev                n         s          r       r    t           r r      m t -so sran
  rev r           alm r a                  - so       o
                                                     s -so r   al v - s s o alm al s o r r e v
                                                                 m     o
                                      rev          rev            re


Fig. 1. Comparison of the running time measured for the code generated by the formal-
ization described in this paper (Isabelle-LLVM), the original formalization from [17]
(notime), and the libstdc++ implementation. Arrays with 108 uint64s with various
distributions were sorted, and we display the smallest time of 10 runs. The programs
were compiled with clang-10 -O3, and run on an Intel XEON E5-2699 with 128GiB
RAM and 256K/55M L2/L3 cache. See [17] for details of the benchmarking method.


complexity proofs along the reﬁnement chain. Our framework reﬁnes down to
the LLVM intermediate representation, such that we can use a state-of-the-art
compiler to generate performant programs.
    As a case-study, we have proved the functional correctness and complexity
of the introsort sorting algorithm. Our veriﬁed implementation performs on par
with the (unveriﬁed) state-of-the-art implementation from the GNU C++ Li-
brary. It also provably meets the C++11 standard library [7] speciﬁcation for
std::sort, which in particular requires a worst-case time complexity of O(n log n).
We are not aware of any other veriﬁed real-world implementations of sorting al-
gorithms that come with a complexity analysis.
    Our work is a combination and substantial extension of an earlier reﬁnement
framework for functional correctness [15] which also comes with a veriﬁcation
of introsort [17], and a reﬁnement framework for a single enat-valued currency
[11]. In particular, we have generalized the reﬁnement framework to arbitrary
resources, introduced currencies that help organizing reﬁnement proofs, extended
the LLVM semantics and reasoning infrastructure with a cost model, connected
it to the reﬁnement framework via a new version of the Sepref tool, and, ﬁnally,
added the complexity analysis for introsort.


6.1            Related Work

Nipkow et al. [23, §4.1] collect veriﬁcation eﬀorts concerning sorting algorithms.
We add a few instances verifying running time: Wang et al. use TiML [25] to
verify correctness and asymptotic time complexity of mergesort automatically.
316     P. M. L. Haslbeck and P. Lammich

Zhan and Haslbeck [26] verify functional correctness and asymptotic running
time analysis of imperative versions of insertion sort and mergesort. We build
on earlier work by Lammich [17] and provide the ﬁrst veriﬁcation of functional
correctness and asymptotic running time analysis of heapsort and introsort.
    The idea to generalize the nres monad [19] to resource types originates
from Carbonneaux et al. [4]. They use potential functions (state → enat) in-
stead of predicates (state → bool), present a quantitative Hoare logic and extend
the CompCert compiler to preserve properties of stack-usage from programs in
Clight to compiled programs.
    We see our paper in the line of research concerning simultaneously verifying
functional correctness and worst-case time complexity of algorithms. Atkey [1]
pioneered resource analysis with separation logic, Guéneau et al. [9] present a
framework that uses time credits in Coq and apply it to involved algorithms and
data structures [10,6]. We further develop their work in three ways: First, while
time credits usually are natural numbers [1,9,26,21,6] or integers [10], we gener-
alize to an abstract resource type and speciﬁcally use resource currencies for a
ﬁne-grained analysis. Second, we use stepwise reﬁnement to structure the veri-
ﬁcation and make the resource analysis of larger use-cases manageable. Third,
we provide facilities to automatically extract eﬃcient competitive code from the
veriﬁcation. The following are the most complex algorithms and data structures
with veriﬁed running time analysis using time credits and separation logic we are
aware of: a linear time selection algorithm [26], an incremental cycle detection
algorithm [10], Union-Find [6], Edmonds-Karp and Kruskal’s algorithm [11].


6.2   Future Work

A veriﬁed compiler down to machine code would further reduce the trusted code
base of our approach. While that is not expected to be available soon for LLVM in
Isabelle, the NREST-monad and the Sepref tool are general enough to connect
to a diﬀerent back end. Formalizing one of the CompCert C semantics [2] in
Isabelle, connecting it to the NREST-monad and then processing synthesized C
code with CompCert’s veriﬁed compiler would be a way to go.
    In this paper we apply our framework to verify an involved algorithm that
only uses basic data structures, i.e. arrays. A next step is to verify more involved
data structures, e.g. by porting existing veriﬁcations of the Imperative Collec-
tions Framework [16] to LLVM. We do not yet see how to reason about the
running time of data structures like hash maps, where worst-case analysis would
be possible but not useful. In general, extending the framework to average-case
analysis and probabilistic programs are exciting roads to take.
    We plan to implement more automation, saving the user from writing boil-
erplate code when handling resource currencies and exchange rates.
    Neither the LLVM nor the NREST level of our framework is tied to running
time. Applying it to other resources like maximum heap space consumption
might be a next step.
                                                       For a Few Dollars More       317

References
 1. Atkey, R.: Amortised resource analysis with separation logic. In: Gordon, A.D. (ed.)
    European Symposium on Programming, ESOP 2010. Lecture Notes in Computer
    Science, vol. 6012, pp. 85–103. Springer (2010). https://doi.org/10.1007/978-3-642-
    11957-6 6, https://doi.org/10.1007/978-3-642-11957-6_6
 2. Blazy, S., Leroy, X.: Mechanized semantics for the Clight subset of the C lan-
    guage. J. Autom. Reason. 43(3), 263–288 (2009). https://doi.org/10.1007/s10817-
    009-9148-3, https://doi.org/10.1007/s10817-009-9148-3
 3. Calcagno, C., O’Hearn, P.W., Yang, H.: Local action and abstract separation
    logic. In: Symposium on Logic in Computer Science (LICS 2007). pp. 366–378.
    IEEE Computer Society (2007). https://doi.org/10.1109/LICS.2007.30, https:
    //doi.org/10.1109/LICS.2007.30
 4. Carbonneaux, Q., Hoﬀmann, J., Ramananandro, T., Shao, Z.: End-to-end veri-
    ﬁcation of stack-space bounds for C programs. In: O’Boyle, M.F.P., Pingali, K.
    (eds.) ACM SIGPLAN Conference on Programming Language Design and Imple-
    mentation, PLDI ’14, Edinburgh, United Kingdom - June 09 - 11, 2014. pp. 270–
    281. ACM (2014). https://doi.org/10.1145/2594291.2594301, https://doi.org/
    10.1145/2594291.2594301
 5. Charguéraud, A.: Separation logic for sequential programs (functional
    pearl). Proc. ACM Program. Lang. 4(ICFP), 116:1–116:34 (2020).
    https://doi.org/10.1145/3408998, https://doi.org/10.1145/3408998
 6. Charguéraud, A., Pottier, F.: Verifying the correctness and amortized complex-
    ity of a union-ﬁnd implementation in separation logic with time credits. J. Au-
    tom. Reason. 62(3), 331–365 (2019). https://doi.org/10.1007/s10817-017-9431-7,
    https://doi.org/10.1007/s10817-017-9431-7
 7. cppreference: C++ standard library speciﬁcation of sort. https://en.
    cppreference.com/w/cpp/algorithm/sort, accessed: 2020-10-12
 8. The GNU C++ library, https://gcc.gnu.org/onlinedocs/libstdc++/, version
    7.4.0
 9. Guéneau, A., Charguéraud, A., Pottier, F.: A ﬁstful of dollars: Formalizing
    asymptotic complexity claims via deductive program veriﬁcation. In: Ahmed,
    A. (ed.) Programming Languages and Systems - 27th European Symposium on
    Programming, ESOP 2018. Lecture Notes in Computer Science, vol. 10801, pp.
    533–560. Springer (2018). https://doi.org/10.1007/978-3-319-89884-1 19, https:
    //doi.org/10.1007/978-3-319-89884-1_19
10. Guéneau, A., Jourdan, J., Charguéraud, A., Pottier, F.: Formal proof and analysis
    of an incremental cycle detection algorithm. In: Harrison, J., O’Leary, J., Tolmach,
    A. (eds.) 10th International Conference on Interactive Theorem Proving, ITP 2019.
    LIPIcs, vol. 141, pp. 18:1–18:20. Schloss Dagstuhl - Leibniz-Zentrum für Informatik
    (2019). https://doi.org/10.4230/LIPIcs.ITP.2019.18, https://doi.org/10.4230/
    LIPIcs.ITP.2019.18
11. Haslbeck, M.P.L., Lammich, P.: Reﬁnement with time - reﬁning the run-time
    of algorithms in Isabelle/HOL. In: Harrison, J., O’Leary, J., Tolmach, A. (eds.)
    10th International Conference on Interactive Theorem Proving, ITP 2019. LIPIcs,
    vol. 141, pp. 20:1–20:18. Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2019).
    https://doi.org/10.4230/LIPIcs.ITP.2019.20, https://doi.org/10.4230/LIPIcs.
    ITP.2019.20
12. Hoare, C.A.R.: Algorithm 64: Quicksort. Commun. ACM 4(7), 321– (Jul
    1961). https://doi.org/10.1145/366622.366644, http://doi.acm.org/10.1145/
    366622.366644
318     P. M. L. Haslbeck and P. Lammich

13. Krauss, A.: Recursive deﬁnitions of monadic functions. In: Bove, A., Komen-
    dantskaya, E., Niqui, M. (eds.) Proceedings Workshop on Partiality and Re-
    cursion in Interactive Theorem Provers, PAR 2010, Edinburgh, UK, 15th July
    2010. EPTCS, vol. 43, pp. 1–13 (2010). https://doi.org/10.4204/EPTCS.43.1,
    https://doi.org/10.4204/EPTCS.43.1
14. Lammich, P.: Reﬁnement to Imperative/HOL. In: Urban, C., Zhang,
    X. (eds.) Interactive Theorem Proving - 6th International Conference,
    ITP 2015. Lecture Notes in Computer Science, vol. 9236, pp. 253–269.
    Springer (2015). https://doi.org/10.1007/978-3-319-22102-1 17, https://doi.
    org/10.1007/978-3-319-22102-1_17
15. Lammich, P.: Generating veriﬁed LLVM from Isabelle/HOL. In: Harrison, J.,
    O’Leary, J., Tolmach, A. (eds.) 10th International Conference on Interactive Theo-
    rem Proving, ITP 2019. LIPIcs, vol. 141, pp. 22:1–22:19. Schloss Dagstuhl - Leibniz-
    Zentrum für Informatik (2019). https://doi.org/10.4230/LIPIcs.ITP.2019.22,
    https://doi.org/10.4230/LIPIcs.ITP.2019.22
16. Lammich, P.: Reﬁnement to Imperative HOL. J. Autom. Reason. 62(4), 481–503
    (2019). https://doi.org/10.1007/s10817-017-9437-1, https://doi.org/10.1007/
    s10817-017-9437-1
17. Lammich, P.: Eﬃcient veriﬁed implementation of introsort and pdqsort. In: Peltier,
    N., Sofronie-Stokkermans, V. (eds.) IJCAR 2020. Lecture Notes in Computer Sci-
    ence, vol. 12167, pp. 307–323. Springer (2020). https://doi.org/10.1007/978-3-030-
    51054-1 18, https://doi.org/10.1007/978-3-030-51054-1_18
18. Lammich, P., Meis, R.: A Separation Logic Framework for Imperative HOL.
    Archive of Formal Proofs (Nov 2012), http://isa-afp.org/entries/Separation_
    Logic_Imperative_HOL.html, Formal proof development
19. Lammich, P., Tuerk, T.: Applying data reﬁnement for monadic programs to
    Hopcroft’s algorithm. In: Beringer, L., Felty, A.P. (eds.) Interactive Theorem Prov-
    ing - Third International Conference, ITP 2012. Lecture Notes in Computer Sci-
    ence, vol. 7406, pp. 166–182. Springer (2012). https://doi.org/10.1007/978-3-642-
    32347-8 12, https://doi.org/10.1007/978-3-642-32347-8_12
20. ”libc++” c++ standard library, https://libcxx.llvm.org/
21. Mével, G., Jourdan, J., Pottier, F.: Time credits and time receipts in Iris. In:
    Caires, L. (ed.) Programming Languages and Systems - 28th European Symposium
    on Programming, ESOP 2019. Lecture Notes in Computer Science, vol. 11423,
    pp. 3–29. Springer (2019). https://doi.org/10.1007/978-3-030-17184-1 1, https:
    //doi.org/10.1007/978-3-030-17184-1_1
22. Musser, D.R.: Introspective sorting and selection algorithms. Softw. Pract. Exp.
    27(8), 983–993 (1997)
23. Nipkow, T., Eberl, M., Haslbeck, M.P.L.: Veriﬁed textbook algorithms - A biased
    survey. In: Hung, D.V., Sokolsky, O. (eds.) Automated Technology for Veriﬁcation
    and Analysis - 18th International Symposium, ATVA 2020. Lecture Notes in Com-
    puter Science, vol. 12302, pp. 25–53. Springer (2020). https://doi.org/10.1007/978-
    3-030-59152-6 2, https://doi.org/10.1007/978-3-030-59152-6_2
24. Wadler, P.: Comprehending monads. In: Proceedings of the 1990 ACM Conference
    on LISP and Functional Programming. p. 61–78. LFP ’90, Association for Comput-
    ing Machinery, New York, NY, USA (1990). https://doi.org/10.1145/91556.91592,
    https://doi-org.manchester.idm.oclc.org/10.1145/91556.91592
25. Wang, P., Wang, D., Chlipala, A.: TiML: a functional language for practical
    complexity analysis with invariants. Proc. ACM Program. Lang. 1(OOPSLA),
    79:1–79:26 (2017). https://doi.org/10.1145/3133903, https://doi.org/10.1145/
    3133903
                                                        For a Few Dollars More        319

26. Zhan, B., Haslbeck, M.P.L.: Verifying asymptotic time complexity of im-
    perative programs in Isabelle. In: Galmiche, D., Schulz, S., Sebastiani,
    R. (eds.) Automated Reasoning - 9th International Joint Conference, IJ-
    CAR 2018. Lecture Notes in Computer Science, vol. 10900, pp. 532–548.
    Springer (2018). https://doi.org/10.1007/978-3-319-94205-6 35, https://doi.
    org/10.1007/978-3-319-94205-6_35




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/
4.0/), which permits use, sharing, adaptation, distribution and reproduction in any
medium or format, as long as you give appropriate credit to the original author(s) and
the source, provide a link to the Creative Commons license and indicate if changes
were made.
    The images or other third party material in this chapter are included in the chapter’s
Creative Commons license, unless indicated otherwise in a credit line to the material. If
material is not included in the chapter’s Creative Commons license and your intended
use is not permitted by statutory regulation or exceeds the permitted use, you will need
to obtain permission directly from the copyright holder.
