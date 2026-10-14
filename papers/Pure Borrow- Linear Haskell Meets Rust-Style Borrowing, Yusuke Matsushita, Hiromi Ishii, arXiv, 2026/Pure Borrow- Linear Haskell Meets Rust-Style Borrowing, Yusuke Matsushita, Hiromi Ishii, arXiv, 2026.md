                                        Pure Borrow: Linear Haskell Meets Rust-Style Borrowing∗
                                        YUSUKE MATSUSHITA, Kyoto University, Japan
                                        HIROMI ISHII, JIJ Inc., Japan
                                        A promising approach to unifying functional and imperative programming paradigms is to localize mutation
                                        using linear or affine types. Haskell, a purely functional language, was recently extended with linear types by
                                        Bernardy et al., in the name of Linear Haskell. However, it remained unknown whether such a pure language
                                        could safely support non-local borrowing in the style of Rust, where each borrower can be freely split and
                                        dropped without direct communication of ownership back to the lender.
arXiv:2604.15290v4 [cs.PL] 5 Jun 2026




                                           We answer this question affirmatively with Pure Borrow, a novel framework that realizes Rust-style borrow-
                                        ing in Linear Haskell with purity. Notably, it features parallel state mutation with affine mutable references
                                        inside pure computation, unlike the IO and ST monads and existing Linear Haskell APIs. It also enjoys purity,
                                        lazy evaluation, first-class polymorphism and leak freedom, unlike Rust. We implement Pure Borrow simply
                                        as a library in Linear Haskell and demonstrate its power with a case study in parallel computing. We formalize
                                        the core of Pure Borrow and build a metatheory that works toward establishing safety, leak freedom and
                                        confluence, with a new, history-based model of borrowing.
                                        CCS Concepts: • Theory of computation → Type theory; • Software and its engineering → Functional
                                        languages.
                                        Additional Key Words and Phrases: Linear Haskell, Rust-style borrowing, purity, safety, parallelism

                                        1    Introduction
                                        Software is the art of embodying human ideals on finite physical machines. This tension naturally
                                        leads to two major programming paradigms. One is functional programming, more on the side
                                        of humans. It offers high-level abstractions and safety for smooth human reasoning. The other
                                        is imperative programming, more geared toward machines. It offers low-level stateful operations,
                                        enabling great performance. Unifying these two programming paradigms has been a long-standing,
                                        central topic in programming language research.
                                           Functional programming favors purity, or the property that the result of the computation is
                                        always the same regardless of the timing and context. Purity allows one to safely forget the
                                        physical machine state and reason about behaviors just as in mathematics. It enables safe lazy
                                        evaluation, safe concurrency, and deep program optimizations such as fusion. Moreover, a number
                                        of languages—e.g., Haskell [Hudak et al. 1992], F★[Swamy et al. 2016], and Lean [de Moura et al.
                                        2015]—rigorously ensure that every computation is pure, unless marked otherwise. Especially in the
                                        presence of concurrency, purity is really helpful because it eliminates tricky, subtle concurrency
                                        bugs that occur only with low probability depending on thread scheduling.
                                           Purity is thus desired, but naïvely it causes significant runtime overhead to keep all data persis-
                                        tently. This calls for unifying pure functional programming with performative, stateful imperative
                                        programming. A long-known baseline approach to this is the ST monad [Launchbury and Pey-
                                        ton Jones 1994]. The monad ST s a allows efficient stateful computation, but its result can still be
                                        taken out into pure computation, unlike the IO monad [Peyton Jones and Wadler 1993].
                                            ∗ This is an extended version of the PLDI 2026 paper [Matsushita and Ishii 2026b] with an appendix on the formal

                                            calculus and metatheory.

                                        Authors’ Contact Information: Yusuke Matsushita, Kyoto University, Kyoto, Japan, ymat@fos.kuis.kyoto-u.ac.jp; Hiromi
                                        Ishii, JIJ Inc., Tokyo, Japan, konn.jinro@gmail.com.



                                        This work is licensed under a Creative Commons Attribution 4.0 International License.
2                                                                         Yusuke Matsushita and Hiromi Ishii


Table 1. High-level comparison of our Pure Borrow with existing approaches. Yes / No #. Mutate: Supports
destructive mutation. Pure: The result can be safely taken out in pure computation. Parallel: Supports safe
                                                                   # for droppable but copyable mutable
parallel execution. Aff. mut.: Supports affine mutable references (G
references). Leak-free: Guarantees the absence of resource leaks.

                                                         Mutate Pure Parallel Aff. mut. Leak-free
                           Pure computation only          #                        -        -
        IO monad [Peyton Jones and Wadler 1993]                  #               #
                                                                                 G         #
    ST monad [Launchbury and Peyton Jones 1994]                        #         #
                                                                                 G         #
                   Rust [Matsakis and Klock 2014]                #                         #
         Pure Linear Haskell [Bernardy et al. 2018]                              #
                 RIO monad [Bernardy et al. 2018]                #               #
                                                                                 G
                  Our Pure Borrow: BO monad



   Another promising approach to this goal is to localize mutation using linear or affine types
[Wadler 1990; Turner et al. 1995; Wansbrough and Peyton Jones 1999], requiring resources to be
used exactly once (linear) or up to once (affine), inspired by Girard [1987]’s linear logic. Linear
or affine types can localize the effect of state mutation, especially for safety. Also, linearity can
prevent resource leaks. Haskell, a purely functional language, was recently extended with linear
types by Bernardy et al. [2018], in the name of Linear Haskell. It achieves safe state mutation inside
pure computation, while supporting concurrency and ensuring leak freedom unlike the ST monad.
It also introduced a leak-free variant of the IO monad, called the RIO monad.
   However, it remained unknown whether such a pure language as Linear Haskell could safely
support borrowing in the sophisticated style of Rust [Matsakis and Klock 2014], a highly successful
imperative language with affine types. While Rust-style borrowing originates from the long line of
work on region types [Tofte and Talpin 1994; Fähndrich and DeLine 2002; Grossman et al. 2002;
Fluet et al. 2006; Haller and Odersky 2010], it features a distinct form of non-locality: each borrower
can be freely split and dropped (i.e., affine), and its ownership is non-locally returned to the lender
without direct communication. This flexibility offers an advantage over the existing Linear Haskell
APIs, which require direct threading of ownership.
   We answer the question above affirmatively with this work, Pure Borrow. Our contributions are
summarized as follows:
      • We develop Pure Borrow, a novel framework that realizes Rust-style borrowing in Linear
        Haskell with purity. (§3). Table 1 shows a high-level comparison with existing approaches.
        Notably, Pure Borrow features parallel state mutation with affine mutable references inside
        pure computation, unlike the IO and ST monads and existing Linear Haskell APIs. It also
        enjoys purity, lazy evaluation, first-class polymorphism and leak freedom, unlike Rust.
      • We implement Pure Borrow simply as a library in Linear Haskell and demonstrate its power
        by a case study on parallel quicksort (§4). Notably, our implementation compiles with the
        current Haskell compiler GHC 9.10+, without any modification to the compiler.
      • We formalize the core of Pure Borrow and build a metatheory that works toward establishing
        safety, leak freedom and confluence, with a new, history-based model of borrowing (§5).
We also explain the background (§2), compare Pure Borrow with existing approaches (§6), and
discuss related and future work (§7). Our Haskell implementation of Pure Borrow and our benchmark
suite are archived at [Matsushita and Ishii 2026a], and the latest version is maintained at https:
//github.com/SoftwareFoundationGroupAtKyotoU/pure-borrow.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                          3


2     Background
Before diving deeply into our work, Pure Borrow, we briefly review prior approaches to local state
mutation inside pure computation in Haskell, namely the ST monad and Linear Haskell.

2.1     ST Monad
The classical approach to achieve local mutation in Haskell is the ST monad [Launchbury and
Peyton Jones 1994], as mentioned in §1.

data ST s a                                                    example :: (Int, [Int])
instance Monad ST s                                            example = runST do
runST :: (∀s. ST s a) → a                                        vec ← newVectorST [0, 1, 2]
                                                                 modifyAtST 0 (+ 3) vec; modifyAtST 2 (+ 5) vec
data VectorSTs a
                                                                 modifyAtST 0 (× 4) vec; n ← readAtST 0 vec
newVectorST :: [a] → ST s (VectorST
                                  s a)
                   s a → ST s [a]                                pure (n, elemsST vec)
elemsST :: VectorST
                              s a → ST s ()
writeAtST :: Int → a → VectorST                                modifyAtST i f vec = do
readAtST :: Int → VectorST a → ST s a
                         s                                      a ← readAtST i vec; writeAtST i (f a) vec

                                      Fig. 1. ST monad APIs and an example usage.


   Figure 1 summarizes APIs and an example usage of the ST monad. The monad ST s a is param-
eterized with a region parameter s. In the ST monad, one can freely use mutable state such as a
vector VectorSTs a1 , bound to some region s. In other words, a region s represents memory locations

that are allocated and kept during ST s . Most notable is the function runST, which can strip off the
ST monad into a pure computation. Its key trick is to use rank-2 polymorphism over the region
variable s (technically working as a skolem). This aptly encapsulates a fresh region s for mutable
state inside ST s and prohibits it from leaking outside.
   Although the ST monad is widely used in Haskell, it has a major limitation: it does not support
parallelism. The ST monad allows shared mutable state like VectorST     s a. Parallelism would allow

multiple threads to mutate such state. The result of computation could nondeterministically depend
on thread scheduling, making runST, the embedding to pure computation, unsound.

2.2     Linear Haskell Before Pure Borrow
A recent groundbreaking take on purity and mutation is Linear Haskell [Bernardy et al. 2018],
which retrofits a linear type system [Wadler 1990] onto Haskell. Notably, it is implemented as a
practical, stable extension called LinearTypes in the Glasgow Haskell Compiler (GHC).
   Linear Haskell simply adds the linear arrow type a ⊸ b, along with the original unrestricted
arrow type a → b. Roughly speaking, the linear arrow a ⊸ b enforces that the argument a is used
exactly once in b.2 This linearity is the key to safely introducing mutable state.
   Figure 2 shows core APIs and an example usage of Linear Haskell. We feature here the linear
mutable vector type Vector a. Most notable is the modifyAt_ operator. A call modifyAt_ i f vec
performs an in-place mutation of the vector vec, applying f to the i-th element, and outputs the
updated vector. Notably, unlike the traditional purely functional style, the old value of the vector
can be safely lost. This is because there is no other alias to the original vec, thanks to the linearity
1   The term ‘vector’ is commonly used in Haskell for a slice to an array. It amounts to the slice type [T] in Rust.
2   Due to lazy evaluation, this is actually more subtle. Bernardy et al. [2018] describe the condition more precisely as follows:
    whenever the output b is consumed exactly once, the input a is consumed exactly once.
4                                                                                       Yusuke Matsushita and Hiromi Ishii


data Ur a where Ur :: a → Ur a                                                   example :: Ur (Int, [Int])
class Linearly; linearly :: (Linearly =◦ Ur a) ⊸ Ur a                            example = linearly do◦
class Movable a where move :: a ⊸ Ur a                                             vec ← newVector [0, 1, 2]
data Vector a                                                                      vec ← modifyAt_ 0 (+ 3) vec
newVector :: Linearly =◦ [a] ⊸ Vector a                                            vec ← modifyAt_ 2 (+ 5) vec
freeVector :: Vector a ⊸ [a]                                                       vec ← modifyAt_ 0 (× 4) vec
modifyAt_ :: Int → (a ⊸ a) ⊸ Vector a ⊸ Vector a                                   (Ur n, vec) ← readAt_ 0 vec
readAt_ :: Movable a ⇒ Int → Vector a ⊸ (Ur a, Vector a)                           move (n, freeVector vec)

class Consumable a where consume :: a ⊸ ()
class LinearOnly a; withLinearly :: LinearOnly a ⇒ a ⊸ (Linearly =◦ a ⊸ r) ⊸ r
par :: a ⊸ b ⊸ (a, b)

                   Fig. 2. Core Linear Haskell APIs and an example usage before Pure Borrow.


of Vector a. Technically, this is guaranteed by the linear constraint Linearly =◦ in the type of the
newVector operator creating a new vector, as we explain later.
   Pure do-notation. Throughout the paper, we use do◦ -notation for pure computations, analogous
to the usual do-notation for monads. Roughly speaking, the monadic binding . . . ← . . . in do◦
works like the let-binding let . . . = . . . in, but the former is often a better fit in Linear Haskell,
because it supports shadowing and adopts strict pattern matching, unlike the latter.3 Practically, we
can use this kind of custom do-notation by the QualifiedDo extension.
  Opting out linearity. We introduce a special data type Ur a (‘Ur’ stands for ‘Unrestricted’). It
means that its content a can be used any number of times (i.e., be freely shared and dropped) even
under linear binding, analogous to the !-modality in linear logic. The type class Movable a abstracts
data types that can be moved to an unrestricted context, i.e., put under Ur. Some primitive types
such as (), Bool and Int are Movable. Also, containers such as the list [a] and the pair (a, b) are
Movable if the component types a, b are Movable. The type class Consumable a abstracts data
types that can be consumed (but not necessarily be shared) under linear binding.
    Linearly. In this paper, we use a special type class called Linearly, proposed by Spiwack et al.
[2022]. It is introduced as a linear constraint Linearly =◦ , which is a linear version of a usual type
class constraint such as Ord a ⇒ . Essentially, =◦ is just a variant of ⊸ where the argument is
managed implicitly (just like ⇒ is a variant of → with an implicit argument).
    The type class Linearly serves as a witness of linearity, or a guarantee that the current computation
is inside a linear thunk introduced by a special operator linearly. Functions that create new mutable
state, such as newVector for Vector a, typically take Linearly, because the output mutable state
captures Linearly and thus is used linearly. At a high level, the operator linearly is analogous to the
ST monad’s runST: it embeds computation with mutable state into a pure context. It also introduces
Linearly, somewhat like how runST introduces s.
    To see how Linearly serves for safety, first imagine a fake API newVector :: [a] ⊸ Vector a
without Linearly constraint. We can weaken the linear arrow of newVector to a usual arrow to
3   In Linear Haskell, shadowing is useful because it is common to thread through the same resource linearly, and strict
    pattern matching is often required to satisfy linearity. The let-binding in Haskell disallows shadowing to allow recursion
    such as let ones = 1 :: ones, just like let rec in ML, and adopts lazy pattern matching.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                       5


get newVector :: [a] → Vector a.4 Combined with freeVector :: Vector a → [a], it easily causes a
dangerous double free, violating memory safety. The linearity witness Linearly solves this. The only
way to (newly) introduce Linearly is by calling linearly :: (Linearly =◦ Ur a) ⊸ Ur a. It requests a
linear function Linearly =◦ Ur a that linearly takes Linearly. By letting newVector take Linearly =◦ ,
the resulting Vector a captures a linear resource Linearly and thus will not be shared unrestrictedly.
See [Spiwack et al. 2022, 2026] for more details.
   For utility, we also have the LinearOnly type class, which abstracts over data types that can be
introduced only inside linear contexts, such as Vector a. In the presence of such data types, we can
safely get Linearly, using the withLinearly operator.
   The type class Linearly is treated very specially as a linear constraint =◦ : it can be freely finitely
duplicated or discarded (but not unrestrictedly shared), automatically by the type system.5
   Parallelism. Pure Linear Haskell supports parallel execution, like pure non-linear Haskell. For
example, par a b evaluates a and b in parallel and combines their outputs. The point is that the
linear arrow ⊸ of par ensures that the mutable resources owned by a and b are disjoint. This is
unlike the ST monad, which does not support parallelism lacking such knowledge of disjointness.
  On the example. The example in Fig. 2 corresponds to that of Fig. 1. As expected, it type-checks
and evaluates to Ur (12, [12, 1, 7]). Still, threading of vec is quite in the way. Although the order of
updates to the 0th element matters and they cannot be swapped, updates to the 0th element and
the 2nd element can be swapped and should be able to be parallelized. Reads can also be swapped.
Threading of the whole vector vec interrupts such natural swapping. This motivates our work,
Pure Borrow, and we come back to this point later in §3.1.

3     Overview of Pure Borrow
We now provide an overview of our Pure Borrow framework. We first give a taste of it (§ 3.1),
showing how it can parallelize the previous example Fig. 2, and then present its details (§3.2).

3.1    Taste of Pure Borrow
   Rust-style borrowing. Pure Borrow features Rust-style borrowing [Fähndrich and DeLine 2002;
Grossman et al. 2002; Fluet et al. 2006; Haller and Odersky 2010; Matsakis and Klock 2014] safely
and purely achieved in Linear Haskell. But what makes Rust-style borrowing so special?
   Figure 3 illustrates the concept of Rust-style borrowing. An original owner T can be mutably
borrowed to create a mutable borrower Mut𝛼 T and a lender Lend𝛼 T for a time period called the
lifetime 𝛼.6 A mutable borrower can freely mutate the data during the lifetime 𝛼. Notably, borrowers
are affine: they can be freely split (e.g., Mut𝛼 T into borrowers Mut𝛼 U1 , Mut𝛼 U2 of subregions)
and dropped at any time before the end of 𝛼. After the lifetime 𝛼 ends, the lender can reclaim full
ownership of T. One might wonder how this happens non-locally, without direct communication
of ownership from borrowers to the lender. Intuitively, ownership thrown away by borrowers
is collected behind the scenes and finally returned to the lender once the lifetime 𝛼 ends. This
non-local handling of ownership and data is the distinct feature of Rust-style borrowing.
4 Recall that the linear arrow ⊸ is a promise by the callee to use the argument once, not a request to the caller.
5 As of now, linear constraints and Linearly have not yet landed in GHC. Still, we can already get the same functionality by
  introducing Linearly as a linear type (using Linearly ⊸ instead of Linearly =◦ ), manually handling instances of Linearly.
  Our Haskell implementation of Pure Borrow does this, and thus it compiles with GHC 9.10+. Our metatheory (§5) also
  follows this style for simplicity. In this paper, we use linear constraints and Linearly in (informal) Haskell code just as a
  useful automation just for the brevity of presentation.
6 In Rust, a mutable borrower (our Mut𝛼 T) is typed &'a mut T, but lending is only implicitly managed, lenders not being

  first-class citizens. Please see §6 for more detailed discussion.
6                                                                                       Yusuke Matsushita and Hiromi Ishii


                                                                                       Lifetime 𝛼
                                          Lender Lend𝛼 T
          Owner T

                                             Borrow
                                                                        Mut𝛼 U1                         ↑ Reclaim T

      Mutable borrower
                                 Mut𝛼 T
                                                                        Mut𝛼 U2
Fig. 3. Rust-style borrowing illustrated. Each Ferris corresponds to a borrower. Ferris illustrations by Karen
Rustad Tölva, CC0, via https://rustacean.net.


    Core of Pure Borrow. Now let’s see how Rust-style borrowing works in Pure Borrow.

type BO𝛼 a; type End𝛼                                               1 example :: Ur (Int, [Int])
type Mut𝛼 a; type Share𝛼 a; type Lend𝛼 a                            2 example = linearly do◦
                                                                    3   vec ← newVector [0, 1, 2]
runBO :: Linearly =◦
                                                                    4   runBO do
  (∀𝛼. BO𝛼 (End𝛼 → a)) ⊸ a
                                                                    5     let !(mvec, lend) = borrow vec
borrow :: Linearly =◦ a ⊸ (Mut𝛼 a, Lend𝛼 a)
                                                                    6     mvec ← modifyAt 0 (+ 3) mvec
share :: Mut𝛼 a ⊸ Ur (Share𝛼 a)
                                                                    7     mvec ← modifyAt 2 (+ 5) mvec
reclaim :: Lend𝛼 a ⊸ End𝛼 → a
                                                                    8     mvec ← modifyAt 0 (× 4) mvec
modifyAt :: Int → (a ⊸ a) ⊸                                         9     let !(Ur svec) = share mvec
  Mut𝛼 (Vector a) ⊸ BO𝛼 (Mut𝛼 (Vector a))                          10     Ur n ← copyAt 0 svec
copyAt :: Copyable a ⇒ Int →                                       11     pure λ end → move
  Share𝛼 (Vector a) → BO𝛼 (Ur a)                                   12        (n, freeVector $ reclaim lend end)

                              Fig. 4. Core APIs of Pure Borrow and an example usage.


  Figure 4 shows the core APIs and an example usage, implementing the same logic as Figs. 1 and 2.7
At first, it proceeds similarly to Fig. 2 by allocating a linear mutable vector vec with newVector.
But then we run a computation with borrowing using runBO (Line 4). Crucially, runBO can run
BO𝛼 inside a pure computation, with a guard by rank-2 polymorphism over the lifetime 𝛼. The
BO monad BO𝛼 is a novel monad we introduce in Pure Borrow, and it denotes a computation that
can be run during the lifetime 𝛼. The mechanism of runBO and BO𝛼 is akin to runST and the ST s
monad (recall Fig. 1, §2.1). Now we borrow the vector vec under 𝛼, obtaining a mutable borrower
mvec :: Mut𝛼 (Vector Int) and a lender lend :: Lend𝛼 (Vector Int) (Line 5). We can do mutations
over the vector using mvec (Lines 6 to 8). Then we share the affine mutable borrower mvec to
get a shared borrower svec :: Share𝛼 (Vector Int) (Line 9) and read the value at the index 0 with
copyAt (Line 10). Notably, svec is wrapped in Ur, so we can use it arbitrarily many times, especially
for reading with copyAt. We are reading only once in this example, but we could add more reads
without any rebinding of svec. Finally, we can reclaim the lender (Line 12) to retrieve Vector Int,
once given by runBO a dead lifetime token end :: End𝛼 , asserting that the lifetime 𝛼 has ended.

7   The bang ! makes a pattern strict, not lazy, and here serves to pass type checking. The reader can safely ignore it.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                   7


  Parallelism. With Pure Borrow, we can go further: mutations on different elements can be
performed in parallel. Such safe parallel mutation in pure computation is a central benefit of Pure
Borrow, practically demonstrated later in §4.

                                                         let !(mvec1 , mvec2 ) = splitAt 1 mvec
parBO :: BO𝛼 a ⊸ BO𝛼 b ⊸ BO𝛼 (a, b)
                                                         (mvec, ()) ← parBO
                                                            (do mvec1 ← modifyAt 0 (+ 3) mvec1
splitAt :: Int → Borrow𝛼k (Vector a) ⊸
                                                                modifyAt 0 (× 4) mvec1 )
  (Borrow𝛼k (Vector a), Borrow𝛼k (Vector a))
                                                            (consume <$> modifyAt 1 (+ 5) mvec2 )

      Fig. 5. Pure Borrow APIs for parallelism and an example usage, modifying Lines 6 to 8 of Fig. 4.


   Figure 5 shows a parallel variant of the mutation part (Lines 6 to 8) of Fig. 4. First, we split
with splitAt the mutable borrower mvec at the index 1 into two disjoint mutable borrowers mvec1
and mvec2 . Then we use our key API, parBO, for parallel composition of BO monads. Here, the
first thread mutates the 0th element twice through mvec1 and the second thread mutates the 2nd
element (of mvec) once through mvec2 . Linearity ⊸ plays a vital role in the safety of parBO: thanks
to linearity, the ownership held by the two BO monads is mutually disjoint, which ensures that
their mutations can safely be performed in parallel, while retaining purity.
  Reborrowing. There was one thing we glossed over in the previous example Fig. 5. The new mvec
obtained from parBO is actually mvec1 in disguise. Can we do better?
  Reborrowing solves this kind of situation. It creates a borrower that borrows ownership from an
existing mutable borrower for a shorter lifetime.
                                                         ((), mvec) ← reborrowing mvec λ mvec →
                                                            let !(mvec1 , mvec2 ) = splitAt 1 mvec in
reborrowing ::
                                 ′                          consume <$> parBO
  Mut𝛼 a ⊸ (∀ 𝛽. Mut𝛽∧𝛼 a ⊸ BO𝛽∧𝛼 r) ⊸
       ′                                                       (do mvec1 ← modifyAt 0 (+ 3) mvec1
  BO𝛼 (r, Mut𝛼 a)
                                                                   modifyAt 0 (× 4) mvec1 )
                                                               (modifyAt 1 (+ 5) mvec2 )

              Fig. 6. Reborrowing API and an example usage, modifying Lines 6 to 8 of Fig. 4.


  Figure 6 shows an API, reborrowing, and an example usage of it. The function reborrowing
creates a mutable reference mvec :: Mut𝛽∧𝛼 (Vector a) that only lives during the execution of the
function. Using this new mvec, we can perform parallel mutation just like in Fig. 5. Finally, the
function restores the original mutable reference mvec :: Mut𝛼 , which has access to the whole vector.
To obtain a shorter lifetime than 𝛼, we use the intersection 𝛽 ∧ 𝛼 of 𝛼 with a fresh lifetime 𝛽.

3.2   Details of Pure Borrow
Now that we know the taste of Pure Borrow, let’s take a closer look at it. Figures 7 to 14 present
the central APIs of Pure Borrow. One beautiful aspect is that high-level APIs can be derived from
simpler primitives, thanks to Haskell’s expressivity.
   Lifetimes. Figure 7 summarizes APIs for lifetimes. A lifetime 𝛼 :: Lifetime is an atomic lifetime
Al ι for some id ι, the static lifetime Static that lives forever ('static in Rust), or an intersection
∧ of lifetimes. As we saw above, lifetime intersection plays a key role in reborrowing. Lifetime
inclusion 𝛼 ≤ 𝛽 is the partial order naturally induced, regarding ∧ as the greatest lower bound and
8                                                                                     Yusuke Matsushita and Hiromi Ishii


data Lifetime = Al ι | (𝛼 :: Lifetime) ∧ (𝛽 :: Lifetime) | Static
class (𝛼 :: Lifetime) ≤ (𝛽 :: Lifetime)
data Now 𝛼 ::Lifetime ; data End 𝛼 ::Lifetime ; instance LinearOnly Now𝛼 ; instance Movable End𝛼
newLifetime :: Linearly =◦ (∀ι, NowAl ι ⊸ a) ⊸ a; endLifetime :: NowAl ι ⊸ Ur EndAl ι

                                             Fig. 7. Core APIs for lifetimes.


newtype BO 𝛼 ::Lifetime a; pure :: a ⊸ BO𝛼 a
(≫=) :: BO𝛼 a ⊸ (a ⊸ BO𝛼 b) ⊸ BO𝛼 b; parBO :: BO𝛼 a ⊸ BO𝛼 b ⊸ BO𝛼 (a, b)
execBO :: Now𝛼 ⊸ BO𝛼 a ⊸ (Now𝛼 , a)                       sexecBO :: Now𝛽 ⊸ BO𝛽∧𝛼 a ⊸ BO𝛼 (Now𝛽 , a)
runBO :: Linearly =◦                                      srunBO :: Linearly =◦
  (∀𝛼. BO𝛼 (End𝛼 → a)) ⊸ a                                  (∀ 𝛽. BO𝛽∧𝛼 (End𝛽 → a)) ⊸ BO𝛼 a
runBO bo = newLifetime λ now → do◦                        srunBO bo = newLifetime λ now → do
  (now, f) ← execBO now bo                                  (now, f) ← sexecBO now bo
  Ur end ← endLifetime now; f end                           Ur end ← pure (endLifetime now); pure (f end)

                                         Fig. 8. Core APIs for the BO monad.


Static as the maximum element. We introduce two basic tokens for lifetimes, the live lifetime token
Now𝛼 and the dead lifetime token End𝛼 .8 The former exclusively asserts that 𝛼 is ongoing, and the
latter persistently asserts that 𝛼 has ended. With newLifetime, we can get NowAl ι for a fresh id ι.
Then with endLifetime, we can consume that to get EndAl ι . The idea of these tokens comes from
RustBelt’s lifetime logic [Jung et al. 2018a], as we discuss later.
   BO monad. Figure 8 shows the APIs for our BO monad. At runtime, BO𝛼 a is just a thunk for a,
just like ST s a, but the APIs for it are quite new. The key primitive is execBO, which takes a pure
value out of BO𝛼 using the live lifetime token Now𝛼 . Actually, a high-level combinator runBO
we used above (Fig. 4) is derived from execBO together with newLifetime and endLifetime, using
rank-2 polymorphism. Also, we have a primitive sexecBO and a derived combinator srunBO for
scoped execution of the BO monad for sub-lifetimes introduced through intersection ∧. It is used to
derive the reborrowing combinator we used above (Fig. 6), as shown soon (Fig. 14).
   Borrowing. Figure 9 lists the APIs for borrowing. We feature Mut𝛼 a for a mutable borrower,
Share𝛼 a for a shared borrower, and Lend𝛼 a for a lender. Notably, they are just newtype wrappers
over the body type a, i.e., they have the same runtime representation as a.9 Also, any Haskell type a
can be a target of borrowing. For utility, Mut𝛼 and Share𝛼 are unified into a general type Borrow𝛼k .
The following are the core primitives: we can borrow an object to create a mutable borrower and a
lender, then we can share a mutable borrower to get an unrestricted shared borrower, and finally
we can reclaim the ownership from a lender once the lifetime has ended.
   Vectors. Figure 10 shows the functions for accessing vectors through borrowers. The primitive
getAt i vec takes a borrower to the i-th element of vec. The primitive swapAt i j vec swaps the i-th
and j-th elements of vec. The primitive updateAt i k vec updates the i-th element of vec using k; it
is quite expressive, allowing access to the BO monad inside k.
8   To enhance automation, our Haskell implementation actually introduces a type class for End𝛼 .
9   We exploit this fact to implement various borrowing operations in the subsequent APIs (e.g., borrow, share and reclaim)
    by internally using unsafe zero-cost type coercion (i.e., a representationally identity function).
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                   9



     newtype Borrow 𝛼k::BorrowKind
                       ::Lifetime  a                  instance LinearOnly (Mut𝛼 a)
     data BorrowKind = Mut | Share                    instance Consumable (Mut𝛼 a)
                                                      instance Movable (Share𝛼 a)
     type Mut𝛼 = Borrow𝛼Mut
     type Share𝛼 = Borrow𝛼Share                       borrow :: Linearly =◦ a ⊸ (Mut𝛼 a, Lend𝛼 a)
                                                      reclaim :: Lend𝛼 a ⊸ End𝛼 → a
     newtype Lend 𝛼 ::Lifetime a                      share :: Mut𝛼 a ⊸ Ur (Share𝛼 a)

                                            Fig. 9. Core APIs for borrowing.


 getAt :: 𝛽 ≤ 𝛼 ⇒ Int →
                                                                modifyAt :: 𝛽 ≤ 𝛼 ⇒ Int → (a ⊸ a) ⊸
   Borrow𝛼k (Vector a) ⊸ BO𝛽 (Borrow𝛼k a)
                                                                 Mut𝛼 (Vector a) ⊸ BO𝛽 (Mut𝛼 (Vector a))
 swapAt :: 𝛽 ≤ 𝛼 ⇒ Int → Int →
                                                                modifyAt i f mvec = do
   Mut𝛼 (Vector a) ⊸ BO𝛽 (Mut𝛼 (Vector a))
                                                                 ((), mvec) ← updateAt i
 updateAt :: 𝛽 ≤ 𝛼 ⇒ Int →
                                                                    (λ a → pure ((), f a)) mvec
   (a ⊸ BO𝛽 (b, a)) ⊸ Mut𝛼 (Vector a) ⊸
                                                                 pure mvec
   BO𝛽 (b, Mut𝛼 (Vector a))
                            Fig. 10. Core APIs for accessing vectors through borrowers.


class Copyable a; copy :: Copyable a ⇒ Share𝛼 a → a
instance Copyable Int; instance Copyable End𝛼 ; instance Copyable (Share𝛼 a)
copyAt :: (Copyable a, 𝛽 ≤ 𝛼) ⇒ Int → Share𝛼 (Vector a) → BO𝛽 (Ur a)
copyAt i svec = do Ur s ← move <$> getAt i svec; pure $ Ur (copy s)

                                             Fig. 11. Core APIs for copying.


splitPair :: Borrow𝛼k (a, b) ⊸ (Borrow𝛼k a, Borrow𝛼k b)
splitEither :: Borrow𝛼k (Either a b) ⊸ Either (Borrow𝛼k a) (Borrow𝛼k b)
splitAt     :: Int → Borrow𝛼k (Vector a) ⊸ (Borrow𝛼k (Vector a), Borrow𝛼k (Vector a))

                                                Fig. 12. APIs for splitting.


   Copying. We provide a mechanism called copying, as shown in Fig. 11. We can copy the body
a out of a shared reference Share𝛼 a if Copyable a holds. It holds roughly when a is a persistent
data type, such as Int, under a condition similar to but different from Movable a; Copyable does
not take ownership, while Movable does. More specifically, any persistent data types (i.e., those
without any mutable states or linear resources) can be Copyable.10
   Splitting. Figure 12 shows primitives for splitting borrowers. Our Haskell implementation in-
cludes a generic mechanism for deriving a split∗ primitive for various data types, not only the ones
shown here. We also have a splitting primitive for a vector. Notably, these splits can be performed
even outside the BO monad, because the information required for them is all persistent.11

10 The class Copyable roughly corresponds to Rust’s Copy, but further allows immutable boxing (like Rust’s Box<T> but

  immutable) unlike it. Notably, this enables recursive data types to be Copyable (e.g., [a] is Copyable under Copyable a).
11 Note that the length of Vector a is immutable, as the type represents a fixed-size slice of an array.
10                                                                            Yusuke Matsushita and Hiromi Ishii



class a ≼ b;   upcast :: a ≼ b ⇒ a ⊸ b           instance (𝛽 ≤ 𝛼, a ≼ b) ⇒ BO𝛼 a ≼ BO𝛽 b
                                                 instance (𝛽 ≤ 𝛼, a ≼ b, b ≼ a) ⇒ Mut𝛼 a ≼ Mut𝛽 b
instance a ≼ b ⇒ Vector a ≼ Vector b             instance (𝛽 ≤ 𝛼, a ≼ b) ⇒ Share𝛼 a ≼ Share𝛽 b
instance 𝛽 ≤ 𝛼 ⇒ End𝛼 ≼ End𝛽                     instance (𝛼 ≤ 𝛽, a ≼ b) ⇒ Lend𝛼 a ≼ Lend𝛽 b

                                    Fig. 13. Core APIs for subtyping.


                                             𝛽                          𝛽∧𝛼
                         joinMut :: Borrowk (Mut𝛼 a) ⊸ Borrowk                a
reborrow :: Mut𝛼 a ⊸                        reborrow mut = withLinearly mut λ mut →
  (Mut𝛽∧𝛼 a, Lend𝛽 (Mut𝛼 a))                  let !(mut′ , lend) = borrow mut in
reborrowing :: Mut𝛼 a ⊸                       (joinMut mut′ , lend)
                        ′
  (∀ 𝛽. Mut𝛽∧𝛼 a ⊸ BO𝛽∧𝛼 r) ⊸
       ′                                    reborrowing mut ko = withLinearly mut λ mut →
  BO𝛼 (r, Mut𝛼 a)
                                              srunBO do
sharing :: Mut𝛼 a ⊸                              let !(mut′ , lend) = reborrow mut; r ← ko mut′
                          ′
  (∀ 𝛽. Share𝛽∧𝛼 a → BO𝛽∧𝛼 r) ⊸                  pure λ end → (r, reclaim lend (upcast end))
       ′
  BO𝛼 (r, Mut𝛼 a)
                                            sharing mut ko = reborrowing mut λ mut →
copyAtMut :: (Copyable a, 𝛽 ≤ 𝛼) ⇒            let !(Ur shr) = share mut in ko shr
  Int → Mut𝛼 (Vector a) →
  BO𝛽 (Ur a, Mut𝛼 (Vector a))               copyAtMut i mvec = sharing mvec $ copyAt i

                        Fig. 14. Primitive and derived operators for reborrowing.



   Subtyping. We introduce subtyping a ≼ b as a type class, as shown in Fig. 13. Subtyping is crucial,
especially for modifying the lifetime information. Note that the mutable vector type Vector a is
covariant, because it is used linearly. On the other hand, the mutable borrower type Mut𝛼 a is
invariant over the body type a, because the body is mutably shared between the borrower and the
lender. This aspect is identical to Rust’s subtyping.

   Reborrowing. Figure 14 shows the primitive and derived combinators for reborrowing. Interest-
ingly, the core primitive for reborrowing is joinMut, which flattens a borrower over a mutable
borrower, taking the intersection lifetime. The key case is when it is instantiated for Mut, with
type Mut𝛽 (Mut𝛼 a) ⊸ Mut𝛽∧𝛼 a. A simple operator reborrow can be derived from that, simply
by borrowing a mutable borrower and joining that. Now we can derive the useful combinator
reborrowing used above (Fig. 6) for reborrowing a mutable borrower, using a delimited scope of
a sub-lifetime introduced by srunBO. We can then derive sharing from reborrowing, which can
temporarily share a mutable borrower within a scope. For example, from it we can immediately
derive a useful function copyAtMut for reading an element from a mutable borrower.

   RustBelt and Pure Borrow. Jung et al. [2018a] developed RustBelt, a semantic soundness proof
of Rust’s ownership type system, by building the lifetime logic, a library for modeling Rust-style
borrowing in the separation logic Iris [Jung et al. 2015]. Some of Pure Borrow’s design ideas originate
from RustBelt’s lifetime logic [Jung et al. 2018a]. These include lifetime tokens Now𝛼 and End𝛼 and
the use of joinMut for reborrowing. Nevertheless, designing Pure Borrow safely required careful
thought because the lifetime logic (or Iris in general) does not guarantee purity or leak freedom.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                     11


   Expressivity compared to Rust. Notably, Pure Borrow supports non-lexical lifetimes [The Rust
Community 2017] to some extent. Although our high-level combinators runBO and srunBO offer
lexically scoped lifetimes, we also provide more primitive APIs, execBO, sexecBO, newLifetime
and endLifetime, for managing lifetimes manually with lifetime tokens Now𝛼 and End𝛼 . This is
similar to what RustBelt [Jung et al. 2018a] does to model Rust’s lifetime-based type system using
lifetime tokens. Still, Pure Borrow lacks a highly automated borrow checker like Rust has, and such
smooth automation in Pure Borrow is left for future work.
   Some advanced borrowing patterns available in Rust are not supported in Pure Borrow, on the
other hand. For example, let us consider the following Rust code:
enum Sum<A, B> { Left(A), Right(B) }
fn test<A, B>(mut s: Sum<A, B>, newb: B) → Option<Sum<A, B>> {
  match s { Sum::Left(a) ⇒ { drop(a); None }
              Sum::Right(ref mut b) ⇒ { ∗b = newb; Some(s) } } }
This is a mixture of moving and borrowing, enabled by Rust’s ref pattern.12 Pure Borrow does not
support this kind of advanced borrowing pattern because it requires pattern matching to be tightly
coupled with borrowing.

4     Case Study and Evaluation
We have implemented the Pure Borrow APIs presented in §3 as a pure-borrow package in Haskell,
which compiles with the current Haskell compiler GHC 9.10+. In this section, we demonstrate its
power with a case study: parallel quicksort [Hoare 1961] implemented in our library.13

4.1     Parallel Quicksort Implementations
We have two implementations of parallel quicksort: a naïve version and a work-stealing version. In
what follows, we present these implementations and discuss the expressiveness of our APIs.
   Naïve parallel quicksort. Figure 15 shows our naïve implementation of parallel quicksort. The
function qsort is the main part. It creates a spark (lightweight thread) for each partitioned sub-
vector, as illustrated in the figure. Its budget upper-bounds the number of sub-vectors, and it falls
back to sequential execution if the budget is exhausted. The function proceeds as follows. If the size
of the vector is more than one, it selects a pivot value from the middle of the vector (Line 6) with
copyAtMut—recall that it is implemented with reborrowing, as shown in Fig. 14. Then it calls divide,
which we explain soon, to partition the mutable borrower mvec into low and high parts (Line 8).
Finally, it recurses on the sub-vectors with halved budgets (Line 10). The calls are combined using
the parIf combinator, which invokes parBO (Fig. 8) to evaluate both arguments in parallel if the
budget remains, or otherwise executes them sequentially.
   Division. Figure 16 shows the divide function that partitions the given vector into low and high
parts according to the pivot value. This is an almost literal translation of the partitionBy function
from vector-algorithms package [Doel and de Castro Lopo 2025] with our API. The function
works in two modes: partUp and partDown, which scan and grow the lower and upper ends of the
active interval, respectively. When an out-of-place element is found, it swaps the elements at the
two indices and switches mode with swapAt (Line 12). When the two indices meet, it splits the
vector into two parts with splitAt (Lines 8 and 13) and returns them.
12 In the Left case, the body a: A of s is moved out and dropped, whereas in the Right case, the body of s is mutably borrowed

    as b: &mut B. Therefore, s is partially moved out only in the first case and mutably borrowed only in the second case.
13 Our implementation and benchmark suite are archived at [Matsushita and Ishii 2026a], and the latest version is available

    at https://github.com/SoftwareFoundationGroupAtKyotoU/pure-borrow.
12                                                                         Yusuke Matsushita and Hiromi Ishii


1  qsort :: (Ord a, Copyable a, 𝛽 ≤ 𝛼) ⇒ Int → Mut𝛼 (Vector a) ⊸ BO𝛽 ()
 2 qsort budget mvec = case size mvec of

 3   (Ur n, mvec) | n ≤ 1 → pure $ consume mvec
                                                                                        budget = 4
 4                  | otherwise → do
 5      let i = quot n 2
                                                                                        budget = 2
 6      (Ur pivot, mvec) ← copyAtMut i mvec
 7      (mlo, mhi) ← divide pivot mvec 0 n                                              budget = 1
 8      let budget′ = quot budget 2
 9      consume <$> parIf (budget′ > 0)                    Each    depicts a lightweight thread
                         ′                   ′             spawned by parBO. Ferris: Tölva, CC0.
10         (qsort budget mlo) (qsort budget mhi)
11   where
12      parIf b = if b then parBO else λ l r → do l ← l; r ← r; pure (l, r)

     qsort′ :: (Ord a, Copyable a, Movable a) ⇒ Int → [a] → Ur [a]
     qsort′ budget xs = linearly do◦
       vec ← newVector xs
       runBO do (mvec, lend) ← borrow vec; qsort budget mvec
                   pure $ move . freeVector . reclaim lend

                 Fig. 15. A naïve parallel implementation of quicksort and an illustration.


1  divide :: (Ord a, Copyable a, 𝛽 ≤ 𝛼) ⇒
2    Int → Mut𝛼 (Vector a) ⊸ Int → Int → BO𝛽 (Mut𝛼 (Vector a), Mut𝛼 (Vector a))
 3 divide pivot = partUp

 4   where
 5      partUp mvec l u
 6         | l < u = do (Ur a, mvec) ← copyAtMut l mvec
 7                      if a < pivot then partUp mvec (l + 1) u else partDown mvec l (u − 1)
 8         | otherwise = pure $ splitAt l mvec
 9      partDown mvec l u
10         | l < u = do (Ur a, mvec) ← copyAtMut u mvec
11                      if pivot < a then partDown mvec l (u − 1)
12                                   else do mvec ← swapAt mvec l u; partUp mvec (l + 1) u
13         | otherwise = pure $ splitAt l mvec

                             Fig. 16. The implementation of divide function.


   Work-stealing parallel quicksort. While the previous implementation is concise, it is rather naïve
because parBO is a structural parallel composition that waits for both arguments to finish, which
can lead to extra waiting time and degraded performance.
   To address this issue, we develop a general, modular, safe, and efficient API for work-stealing
parallelization of divide-and-conquer algorithms, as shown in Fig. 17a. Although the work-stealing
API is designed to be used with our Pure Borrow APIs and is mostly implemented using them,
it also uses some unsafe data structures, such as concurrent queues mutated by multiple threads
under the hood. Hence, this API should be interpreted as a proof-of-concept demonstrating that
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                    13


data DivideConquer𝛼 a = DivideConquer { divide :: ∀ 𝛽. 𝛽 ≤ 𝛼 ⇒ Mut𝛽 a ⊸ BO𝛽 (Result𝛽 a) }
data Result𝛽 a = Done | Continue [Mut𝛽 a]
divideAndConquer :: 𝛽 ≤ 𝛼 ⇒ Int → DivideConquer𝛼 a → Mut𝛼 a ⊸ BO𝛽 (Mut𝛼 a)
                                    (a) General API for work-stealing parallelism.

qsortDC :: (Ord a, Copyable a, 𝛽 ≤ 𝛼) ⇒                               steal

  Int → Int → Mut𝛼 (Vector a) ⊸ BO𝛽 (Mut𝛼 (Vector a))
qsortDC nwork thresh = divideAndConquer nwork $                                  (empty)
  DivideConquer λ mvec → case size mvec of
                                                                          pop
     (Ur n, mvec)
       | n ≤ 1 → let () = consume mvec in pure Done
                                                            push
       | n ≤ thresh → Done <$> qsort 0 mvec
       | otherwise → let i = quot n 2 in do
            (Ur pivot, mvec) ← copyAtMut i mvec
            (mlo, mhi) ← divide pivot mvec 0 n        (c) Each worker       owns a deque. It
                                                      pushes/pops at the top (near-side). An
            pure $ Continue [mlo; mhi]                idle worker   steals from another’s bot-
                   (b) Quicksort implementation.                            tom. Ferris: Tölva, CC0.

                                          Fig. 17. Work-stealing parallelism.


Pure Borrow can provide good basic building blocks for more sophisticated APIs, and we do not
claim that it is the best API for work-stealing parallelism. DivideConquer wraps a function for
each step of divide-and-conquer, which takes a mutable borrower, executes in the BO monad, and
returns Result, which is either Done or Continues with divided parallelized pieces of work. Given
DivideConquer, divideAndConquer parallelizes the whole divide-and-conquer algorithm with a
work-stealing scheduler. As illustrated in Fig. 17c, each worker owns a local double-ended queue of
jobs, and whenever a thread finishes a job, its sub-jobs are pushed to the top. Then an idle worker
first tries to pop another piece of work from the top of its own deque, and tries to steal from the
bottom of another’s queue when its own queue is empty. We also allocate a condition variable for
each piece of work for synchronization. We carefully design divideAndConquer so that concurrent
mutation is safely encapsulated, keeping the observed behavior pure.
   Figure 17b gives a more sophisticated implementation of parallel quicksort with this work-
stealing scheduler. It retains almost the same logic as the naïve implementation Fig. 15, but returns
“divided” pieces of work instead of recursing on the sub-vectors. If the size of the vector is less than
a given threshold, it falls back to sequential quicksort.
   Notably, this is efficiently parallelized thanks to the absence of post-processing, which benefits
greatly from affine mutable borrowers in Pure Borrow. Traditional move-based APIs would require
post-processing to join vectors (see Splitting with reversion in §6 for a detailed discussion).

4.2    Benchmark Results
To evaluate performance, we measured the runtime and memory allocation for randomly generated
integer vectors of varying sizes. We compared our two implementations with the introsort14
implementation in the vector-algorithms package [Doel and de Castro Lopo 2025], widely used
in industry. More concretely, we compare the following implementations: Introsort, industrial-
level sequential introsort from the vector-algorithms package; Sequential, sequential quicksort,
14 Introsort [Musser 1997] is a variant of quicksort that cleverly switches to heap or insertion sort to improve performance.
14                                                                                                        Yusuke Matsushita and Hiromi Ishii


                         15                                                                    80
 Wall Clock Time [ms]




                                                                             Allocation [MB]
                                                                                               60
                         10
                                                                                               40
                          5
                                                                                               20

                          0                                                                     0
                                 0        1           2         3 ·104                              0      1           2         3 ·104
                                                  𝑁                                                               𝑁
                         Intro       Sequential       Naïve 4     Naïve 16                     Naïve 32   WS 4        WS 8      WS 10

                                         Fig. 18. The performance of parallel quicksort implementations.


i.e., our naïve quicksort in Fig. 15 with budget = 0, serving as the baseline; Naïve 𝑁 , our naïve
parallel quicksort (Fig. 15) with budget = 𝑁 , dividing the whole vector into at most 𝑁 pieces; and
WS 𝑁 , our work-stealing parallel quicksort (Fig. 17) with thresh = 16 and 𝑁 worker threads. The
benchmarks were run with the tasty-bench framework [Lelechenko 2021] on a MacBook Pro
2024 with an Apple M3 chip (4 performance cores and 6 efficiency cores) and 16 GB of RAM. All
cases were run with the +RTS -N10 option, enabling parallelism on 10 cores.
   Figure 18 shows the benchmark results. Overall, our parallel quicksort implementations have
considerably faster runtimes than the sequential quicksort, and our work-stealing versions largely
outperform the naïve ones in runtime. These results are promising and demonstrate the eligibility
of our Pure Borrow APIs as building blocks for sophisticated parallelism. Although our current
parallel quicksort implementations do not outperform the industrial-level introsort, we believe that
more sophisticated implementations can further improve performance.

4.3                      Summary
Our Pure Borrow framework enables writing safe, pure, and efficient algorithms with parallelized
mutation concisely in Linear Haskell. Our parallel quicksort implementations written in our Pure
Borrow APIs showed promising performance.

5                       Formal Calculus and Metatheory
We have seen above that our Pure Borrow framework is powerful, providing safe, rich abstraction
for efficient mutation. But is this powerful extension to Linear Haskell really safe?
   To answer this question, we formalize Linear Haskell extended with Pure Borrow (§5.1, §5.2) and
establish a metatheory for its safety, leak freedom and confluence (§5.5). For purity, we develop
two operational semantics, one for physical behavior and the other for mathematical modeling (§
5.3), and formulate a type-based relation between the two (§5.4).

5.1                      Program Syntax
Figure 19 shows the program syntax.15 We keep the language minimal while supporting the core
functionalities of borrowing. Values of the BO monad are constructed with monad constructors mo.
15 The small numbers (e.g., 2 in (+) 2) show the arity. For simplicity, we don’t have partial application to op, mo, and C.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                               15


                            Variable       Var ∋ x, y, z          Data constructor            C
 Integer operation        iop F (+) 2 | (×) 2 | · · ·                   Integer relation          irel F (≤) 2 | · · ·
   Operator      op F iop | irel | par 2 | consume 1 | move 1 | linearly 1 | withLinearly 1
                     | newRef 2 | freeRef 1 | newLifetime 2 | endLifetime 1
                     | borrow 2 | share 1 | copy 1 | joinMut 1 | reclaim 2 | execBO 2
 Monad constr.       mo F pure 1 | (≫=) 2 | sexecBO 2 | parBO 2 | deref 1 | updateRef 2

               Term      Term ∋ 𝑡, 𝑢 F x | let x = 𝑡 in 𝑢 | λ x→ 𝑡 | 𝑡 𝑢 | seq x 𝑡 | 𝑛
                                      | C 𝑡¯ | case 𝑡 of { C x̄→ 𝑢 } | op 𝑡¯ | mo 𝑡¯
                                               Fig. 19. Program syntax.


 Lifetime variable α, β               Lifetime id ι          Lifetime 𝛼, 𝛽 F al ι | static | 𝛼 ∧ 𝛽 | α
                                                                                       Î
                Multiplicity variable π, μ                 Multiplicity 𝜋, 𝜇 F 1 | ω |    π
                       Type variable 𝑋, 𝑌                  Variable 𝑥 F α | ι | π | 𝑋
               Type constructor        F          Borrower constructor 𝐵 F Mut | Share
            Type     Type ∋ 𝑇 , 𝑈 F ∀𝑥 . 𝑇 | 𝑋 | 𝑇 →𝜋 𝑈 | F 𝑇¯ | Int | Linearly
                                   | Ref 𝑇 | Now𝛼 | End𝛼 | 𝐵𝛼 𝑇 | Lend𝛼 𝑇 | BO𝛼 𝑇
                               𝑇 ⊸ 𝑈 ≜ 𝑇 →1 𝑈                   𝑇 → 𝑈 ≜ 𝑇 →ω 𝑈

Data type declaration         data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯                   Typing context          𝛤, 𝛥 F x ::𝜋 𝑇
                                        Fig. 20. Syntax for the type system.


  The biggest difference from §3 is that, for mutable state, our language supports only references
Ref and omits vectors Vector for simplicity. Note that we can still emulate the functionality of
Vector a by a list of references [Ref a].

5.2   Type System
We also formalize the type system. This is largely straightforward, following the approach of
Bernardy et al. [2018]. Figure 20 presents the syntax for it.16 The function type →𝜋 is parameterized
by the multiplicity 𝜋, representing linear (1) or unrestricted (ω) binding. For simplicity, we do
not introduce type classes, and the linearity witness Linearly is just a linear data type. Notably,
we support first-class polymorphism, including rank-2 polymorphism. Typing rules are quite
straightforward formalization of §3.2. Please see Appendix A.1 for the details.

5.3   Two Operational Semantics
Why is Linear Haskell extended with Pure Borrow still pure, while supporting flexible mutation
with Rust-style borrowing?
   To answer this question, we introduce two execution models for our formal calculus. A natural one
is mutative operational semantics, which explicitly owns the global memory state and destructively
mutates the state as the computation progresses. What is notable is the other one, denotational
16 For each type constructor F , we assume a data type declaration, which can be recursive.
16                                                                                    Yusuke Matsushita and Hiromi Ishii


                                      Value 𝑣 F λ x→ 𝑡 | 𝑛 | C x̄ | mo x̄
        Evaluation context 𝐾 F [·] | [·] x | seq [·] x | case [·] of { C x̄→ 𝑡 } | op x̄ [·] ȳ
                                                  (a) Common things.

     Location ℓ            Memory 𝑀 F ℓ ↦→ x                     Borrower constr. 𝐵¤ F Mut𝑝¯ | Share

      Extra value 𝑑ˆ F ∅ | Ref ℓ | Done x                         Extra value 𝑑¤ F ∅ | ∅𝐻 | Ref x
                                                                                  | Lendδ x | Done𝐻 x
              Extra operator        ˆ F ···
                                   op
                                                                                         ¤ F ···
                                                                         Extra operator op
             Term 𝑡ˆ, 𝑢ˆ F 𝑡 | 𝑑ˆ | op
                                     ˆ x̄
                                                                     Term 𝑡¤, 𝑢¤ F 𝑡 | 𝑑¤ | op
                                                                                             ¤ x̄ | 𝐵¤ 𝑡¤
                       ˆ 𝑤ˆ F 𝑣 | 𝑑ˆ
                 Value 𝑣,                                               Value 𝑣,¤ 𝑤¤ F 𝑣 | 𝑑¤ | 𝐵¤ 𝑣¤
     Evaluation context 𝐾ˆ F 𝐾 | op
                                  ˆ x̄ [·] ȳ                 Evaluation ctx. 𝐾¤ F 𝐾 | op
                                                                                        ¤ x̄ [·] ȳ | 𝐵¤ 𝐾¤
  Env. 𝐸ˆ F x = 𝑡ˆ                         ˆ 𝑀; x
                              Config. 𝐺ˆ F 𝐸;                   Env. 𝐸¤ F x = 𝑡¤, δ           Config. 𝐺¤ F 𝐸;
                                                                                                           ¤ x
                (b) For mutative semantics.                     (c) For denotational semantics. Also see Fig. 22.

                                Fig. 21. Core syntax for the two operational semantics.


operational semantics. It is free of the global memory state and instead locally manages information
about each part of the state according to ownership. This localizes mutation and executes much like
purely functional languages. Indeed, denotational operational semantics is designed to be strongly
confluent (Theorem 5.1, §5.5), and thus serves as the witness for the purity of our Pure Borrow.
Later, we establish an association system (§5.4), or a type-based relation between the two execution
models, and state that the relation is actually a bisimulation (Conjecture 5.5, §5.5), which entails
that well-typed programs behave the same way in the two execution models. This overall scheme
largely follows the purity proof for original Linear Haskell by Bernardy et al. [2018],17 but further
introduces a new mechanism for justifying Rust-style borrowing: histories.
   Histories for borrowing. As explained in §3.1 (and illustrated in Fig. 3), Rust-style borrowing is
great in that no direct communication is needed for borrowers to return ownership to the lender.
However, this poses a challenge in building a pure execution model. How can the lender know the
final result of mutation by the borrowers, when it reclaims the ownership?
   To solve this, we propose a new approach: recording the history of updates on borrowed data.18
More concretely, our denotational operational semantics goes as follows. Because each mutation
to borrowed data (more specifically, updateRef) happens inside the BO monad, executed with
execBO/sexecBO threading live lifetime tokens Now𝛼 , we can record the mutation history to the
tokens. The history can then be inherited by dead lifetime tokens End𝛼 at endLifetime. When the
lender reclaims the ownership, we can restore the final version of the borrowed content from the
history saved in the dead lifetime token. This successfully models global communication from the
borrowers to the lender in a local way.
  Overview. Now that we have a big picture, let’s dive into the two operational semantics. Figures 21
and 22 present the syntax for them. More details are presented in Appendix A.2.
17 The ordinary and denotational dynamic semantics of Bernardy et al. [2018] correspond to our mutative and denotational

     operational semantics, respectively.
18 Other studies used different methods, such as prophecies, to model mutable borrowing functionally. Please refer to §7 for

     a comparison of our history-based approach with these existing methods.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                   17


               Borrow id       BorId ∋ δ             Borrow path         BorPath ∋ 𝑝, 𝑞 F δ | 𝑝.𝑖
                                          History     Hist ∋ 𝐻 F 𝑝 ←x
                              Fig. 22. Syntax for histories in denotational semantics.

                     𝐸    ≜    x = 3, main = execBO now (modifyRef (λ x→ x + 4) ref )
                    𝐸′    ≜    x = 3, y = 7, main = (now ′, ref ′ )
         ref = Ref ℓ, now = ∅, 𝐸; ℓ ↦→ x; main                           ref = Mutδ (Ref x), now = ∅∅, 𝐸; main
 →∗ ref ′ = Ref ℓ, now ′ = ∅, 𝐸 ′ ; ℓ ↦→ y; main              →∗ ref ′ = Mutδ (Ref y), now ′ = ∅δ←y , 𝐸 ′ ; main
                      Fig. 23. Reduction example in mutative and denotational semantics.


   To model Haskell’s lazy, call-by-need evaluation, both semantics are formulated in the style of
Launchbury [1993], where the environment consists of variable-term bindings. Notably, the opera-
tional semantics has a nondeterministic evaluation order, as clarified by the syntax of evaluation
contexts (𝐾 etc.), where the arguments of the operators (op etc.) are evaluated in parallel. Despite
this freedom, our language satisfies the confluence and behavior uniqueness, as discussed later
(Theorem 5.1 and Corollary 5.8, §5.5).
   One major difference between the two semantics is that mutative semantics is equipped with the
global memory 𝑀, while denotational semantics lacks it. A reference Ref is modeled as the location
ℓ in the former and the content x in the latter.
   To support borrowing, denotational semantics handles the history 𝐻 , which is defined in Fig. 22.
A borrow id δ uniquely identifies a borrow created with each borrow. A borrow path 𝑝 represents a
sub-component of a borrowed object. A history 𝐻 records updates 𝑝 ←x of the content of a reference
at 𝑝 into x (by updateRef).19 In denotational semantics, live and dead lifetime tokens are models as
∅𝐻 with a history 𝐻 , and each mutable borrower puts on Mut𝑝¯ , where 𝑝¯ is initially set to the borrow
id δ just after borrow. Notably, we can freely handle nested borrowers (i.e., borrowers that contain
borrowers), thanks to the multiple paths 𝑝¯ in the constructor Mut𝑝¯ (each path 𝑝𝑗 corresponds to a
different layer of borrowing). Arbitrary (possibly recursive) algebraic data types within borrowers
are also supported, using field accesses .𝑖 in borrow paths 𝑝 for splitting (Fig. 12).20
   Based on this syntax, we introduce the small-step reduction relations 𝐺ˆ → 𝐺ˆ ′ and 𝐺¤ → 𝐺¤ ′ for
the two operational semantics. The reduction rules are rather straightforward, with the big picture
in mind. Please refer to Appendix A.2 for the details. Figure 23 presents a reduction example in
mutative and denotational semantics,21 showcasing how mutation works.

5.4    Association System
Mutative and denotational operational semantics are designed so that their execution is parallel and
related, as informally observed in Fig. 23. We formalize this idea into what we dub the association
system. Roughly speaking, it is a variant of the type system that is dynamic—i.e., considering
intermediate execution steps—and relational—i.e., associating the two execution models.
19 A history only records the latest update for each borrow path 𝑝. So a history can have at most one item of the form 𝑝 ←x

  for each borrow path 𝑝. The order of items in a history is ignored. We write ∅ for the empty history.
20 As for functions, our calculus does not offer special operations on mutable borrowers over functions. Extending Pure

  Borrow with a feature like Rust’s FnMut is left for future work.
21 Here, modifyRef is a function derived from updateRef, just like modifyAt in Fig. 10, §3.2. For readability, we omit some

  irrelevant variables in the environments. For both semantics, the variables ref and now are actually included in the final
  environment, with the same binding as the initial environment.
18                                                                         Yusuke Matsushita and Hiromi Ishii


   The high-level association judgment we provide is 𝐺ˆ ∝𝑇 𝐺,         ¤ stating that the mutative and
denotational configurations 𝐺, ˆ 𝐺¤ are related, under the return type 𝑇 . To define this, we introduce
a term-level association judgment 𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚ , which is defined compositionally much like the
typing judgment 𝛤 ⊢ 𝑡 :: 𝑇˚ . Here, 𝛤˚ and 𝑇˚ are an extended version of 𝛤 and 𝑇 , where 𝛤˚ can contain
some ‘ghost resources’ that account for advanced types (e.g., mut𝑝¯ for Mut𝛼 𝑇 ). The design of our
association system is highly subtle, primarily due to lazy evaluation, first-class polymorphism, and
the complex nature of Rust-style borrowing. Please refer to Appendix B for the details.

5.5     Metatheory
Finally, we introduce our metatheory for Pure Borrow, which works toward establishing memory
safety, leak freedom and confluence (or behavior uniqueness). With properly designed formalization,
especially denotational operational semantics and the association system, we can aim for the desired
properties. Please refer to Appendix C for the omitted details.

  Strong confluence of denotational operational semantics. Remarkably, by design, our denotational
operational semantics is strongly confluent, i.e., satisfies the diamond property:

Theorem 5.1 (Strong confluence of denotational operational semantics). For any deno-
                         ¤ 𝐺¤ 1 and 𝐺¤ 2 such that 𝐺¤ 1 ≠ 𝐺¤ 2 , 𝐺¤ → 𝐺¤ 1 and 𝐺¤ → 𝐺¤ 2 , there exists a
tational configurations 𝐺,
configuration 𝐺 + such that 𝐺¤ 1 → 𝐺¤ + and 𝐺¤ 2 → 𝐺¤ + .
               ¤

     On the association system. Crucially, well-typedness implies association:

Theorem 5.2 (Well-typedness implies association). If ⊢ 𝑡 :: 𝑇 , then (x = 𝑡; ; x) ∝𝑇 (x = 𝑡; x).

  We use the term safety on configurations for the existence of an association. More concretely, a
mutative configuration 𝐺ˆ is safe if 𝐺ˆ ∝𝑇 𝐺¤ for some 𝐺¤ and 𝑇 , and a denotational configuration 𝐺¤ is
safe if 𝐺ˆ ∝𝑇 𝐺¤ holds for some 𝐺ˆ and 𝑇 .
  Remarkably, safety ensures leak freedom for a mutative configuration:

Theorem 5.3 (Safety ensures leak freedom). If x = 𝑣, ˆ 𝑀; x is safe, then 𝑀 is empty.
                                                  ˆ 𝐸;

   Progress and bisimulation. Crucially, we expect the association system to satisfy progress and
bisimulation. This is a relational version of the well-known progress and preservation, the syntactic
approach to type soundness [Wright and Felleisen 1994].
   We carefully designed our formalization to satisfy these properties and wrote rough proof
sketches for them. That said, they are currently conjectures, whose rigorous proofs are left as future
work and possibly require minor fixes to the association system.

Conjecture 5.4 (Safety ensures progress). For any safe configuration 𝐺ˆ that is not a normal
form, there exists 𝐺ˆ ′ such that 𝐺ˆ → 𝐺ˆ ′ . Also, for any safe configuration 𝐺¤ that is not a normal form,
there exists 𝐺¤ ′ such that 𝐺¤ → 𝐺¤ ′ .

Conjecture 5.5 (Association is a bisimulation). For any type 𝑇 , the relation ∝𝑇 is a bisimulation
with respect to mutative and denotational operational semantics.

     Bisimulation clearly implies preservation of safety:

Corollary 5.6 (Preservation of safety). Assume Conjecture 5.5. If 𝐺ˆ is safe and 𝐺ˆ → 𝐺ˆ ′ holds,
then 𝐺ˆ ′ is safe. Analogously, if 𝐺¤ is safe and 𝐺¤ → 𝐺¤ ′ holds, then 𝐺¤ ′ is safe.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                  19


   Behavior uniqueness. Finally, with the bisimulation (Conjecture 5.5) and the confluence of deno-
tational operational semantics (Theorem 5.1), we can establish the behavior uniqueness of mutative
operational semantics under safety.22

Definition 5.7 (Behavior in mutative operational semantics). We say 𝐺ˆ may be non-terminating
                                                    ˆ We say 𝐺ˆ may terminate if there exists a
if there exists an infinite reduction sequence from 𝐺.
reduction sequence from 𝐺 to some normal form. We say 𝐺ˆ may return 𝑛 if there exists a reduction
                            ˆ
sequence from 𝐺ˆ to some configuration of the form x = 𝑛, 𝐸;
                                                          ˆ 𝑀; x.

Corollary 5.8 (Behavior uniqeness in mutative operational semantics). Assume Conjec-
ture 5.5. Take any safe configuration 𝐺.
                                      ˆ It is not the case that 𝐺ˆ may be non-terminating and also
may terminate. If 𝐺 may return 𝑛 and 𝑚, then 𝑛 = 𝑚.
                   ˆ

Proof. By Conjecture 5.5 and Theorem 5.1.                                                                               □

6   Comparison with Existing Approaches
We compare our Pure Borrow with other existing approaches to borrowing and related mechanisms
for flexible resource management.

   Programmable lifetime control. Rust’s borrow checker is highly automated but is largely a black
box hard to intervene with. In contrast, Pure Borrow provides programmers with great control of
lifetimes. A core idea is to use lifetime tokens Now𝛼 , End𝛼 that represent lifetime state, inherited
from the semantic model of RustBelt [Jung et al. 2018a]. Thanks to Haskell’s advanced features,
such as first-class polymorphism, programmers can build abstractions as observed in §3. That said,
more automation in Pure Borrow would also be helpful, which is left for future work.

   First-class lenders. In Rust, lenders are not first-class citizens and cannot be passed as arguments
to or returned from functions. This imposes practical limitations, e.g., in handling self-borrowing
data types. In contrast, our Pure Borrow treats lenders as first-class citizens, providing the first-
class lender type Lend𝛼 T. First-class lenders are quite underexplored so far,23 and it would be
interesting to explore their practical usage. For example, Pure Borrow can represent an integer
vector self-borrowing some element of it as ∃𝛼. (Mut𝛼 Int, Lend𝛼 (Vector Int), Now𝛼 ).

   Leak freedom. In Rust, types are affine, not linear. One can accidentally cause leaks in Rust, for
example by constructing cyclic references under reference-counting GC [Ben-Yehuda 2015]—a
finding nicknamed as Leakpocalypse. A possible improvement is to keep track of leakable types
with a special trait T: Leak,24 but this has not been adopted so far for technical reasons [Matsakis
2025]. In contrast, our Pure Borrow is carefully designed to guarantee leak freedom.25

22 One may wonder if the strong confluence of mutative operational semantics under safety derives from Conjecture 5.5

   and Theorem 5.1. Unfortunately, that is not the case, because the association ∝𝑇 is not left-unique. Indeed, the strong
   confluence does not hold in a usual sense; for example, two reductions of distinct newRefs may unfortunately allocate
   the same location ℓ. So instead, we establish the uniqueness of behavior.
23 First-class lenders were partly supported by Nakayama et al. [2024] in the context of type-based automated verification,

   but they did not even support nested references.
24 For example, integers i32 and mutable references &mut U satisfy Leak. Leak freedom would then be guaranteed by

   imposing T: Leak on smart pointer types under reference-counting GC such as Rc<T> and Arc<T>.
25 To be fair, Rust appears to be leak-free when restricted to the subset of features currently supported by Pure Borrow.

   Still, we are not aware of any existing work that formally establishes the leak freedom of Rust for such a subset, and
   we conjecture that Pure Borrow could be safely extended to features like reference-counting GC with leak freedom by
   introducing a type class for leakable types.
20                                                                      Yusuke Matsushita and Hiromi Ishii


                  comonad                                        comonad
     Linearity     many ≤        once              Ur a ⊸ a                  Ur a ⊸ Ur (Ur a)

 Uniqueness       unique ≤ aliased          a ⊸ (Mut𝛼 a, Lend𝛼 a)      Mut𝛼 (Mut𝛽 a) ⊸ Mut𝛼∧𝛽 a
                                monad                           monad-like
                   Fig. 24. Linearity and uniqueness axes in OxCaml and Pure Borrow.



   Purity. A crucial design choice of our Pure Borrow is that it focuses on a pure fragment. As a
result, unlike Rust, it does not support mutable state shared across threads such as a mutex, because
the result of concurrent mutation depends on nondeterministic thread scheduling. Still, this does
not preclude sequentially shared mutable state, like VectorST s a in the ST monad (§2.1). Indeed, we

observe that Pure Borrow can support shared mutable state by requiring a non-shareable token for
each mutation to such state, an approach akin to linear constraints in Haskell [Spiwack et al. 2022,
2026] and GhostCell in Rust [Yanovski et al. 2021].

   Oxidized OCaml. Recently, inspired by the success of Rust, there is a movement to “oxidize”
OCaml, i.e., strengthen OCaml with resource-related information for better safety and performance
[Lorenzen et al. 2024; Georges et al. 2025]. This idea has been embodied as a practical language
extension, OxCaml [Jane Street 2025], already in use for production code.
   While this has a similar spirit to our Pure Borrow, their goal is quite different. First, they do not
care much about rigorous purity, as OCaml allows side effects anywhere, unlike Haskell. Also, they
aim to keep annotations for resources very lightweight, even maintaining backward compatibility
with legacy OCaml. They add coarse-grained labels about resources, called modes. We note that
their lifetime-related modes are very coarse-grained: just local and global. They provide an API for
temporarily using a global object locally, which is somewhat like simple borrowing but without
fine-grained scoping. Rust-style borrowing of our Pure Borrow is much more expressive and
fine-grained, especially with the support of reborrowing.
   An interesting high-level comparison between our approach and theirs can be made in the view
of linearity and uniqueness, as summarized in Fig. 24. As clarified by Marshall et al. [2022], linearity
is the inability to create (and drop) an alias, and uniqueness is the absence of aliases. OxCaml
introduces modes many vs. once for linearity and unique vs. aliased for uniqueness. Lorenzen
et al. [2024] point out that many is a comonad and aliased is a monad. Linear Haskell has the
linearity axis, with Ur being a comonad and an exact counterpart of many. Notably, Rust-style
borrowing of our Pure Borrow can be understood as a mechanism for allowing aliases, akin to
aliased, but with access separated by lifetimes. Borrowers Mut𝛼 /Share𝛼 and lenders Lend𝛼 assert
a possible presence of lifetime-delimited aliases—a lender for Mut𝛼 , borrowers for Lend𝛼 , and a
lender and shared borrowers for Share𝛼 . Roughly speaking, borrowing borrow is like monadic
introduction, and borrower joining joinMut is like monadic joining. Still, Mut𝛼 is not exactly an
(indexed) monad, because it is not a functor, being invariant in subtyping (Fig. 13, §3.2). This view
of borrowing as aliasing provides an exciting perspective for future work.

  Splitting with reversion. Spiwack et al. [2022] proposed an approach to splitting ownership with a
mechanism for reverting that. They introduce, for example, a vector type Vector a n with a phantom
parameter n for an abstract address. In their API, the vector can be split into two vectors Vector a l
and Vector a r for some l and r under a peculiar constraint Slices n l r, and they can be later joined
back under that constraint. The core drawback of this approach is that the structure of a split
should be statically determined and tracked, so that phantom post-processing can be performed
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                         21


later to revert the split and join tokens. In contrast, our Rust-style borrowing enables dynamic,
flexible splitting of ownership, without post-processing for reversion.

   Destination passing. Destination passing [Minamide 1998] is a long-known idea for achieving
efficient mutation in functional languages, and its type-safe formulation has been recently explored
[Bagrel 2024; Bagrel and Spiwack 2025]. At a high level, destination passing works like borrowing:
the type 𝑆 ⋉ ( ⌊𝑇1 ⌋ ⊗ · · · ⊗ ⌊𝑇𝑛 ⌋) roughly denotes an object 𝑆 lending its components 𝑇1, . . . ,𝑇𝑛 as
holes. Its core difference from our Pure Borrow is that one should directly modify the lender type
(on the right-hand side of ⋉) each time one returns ownership to fill a hole.

   Rust-style borrowing in functional languages. Wagner et al. [2025] presented how to augment
a linear type system of an ML-style functional language to support Rust-style borrowing. They
also proved the soundness of the resulting type system semantically using a new separation logic
that supports borrowing. This work is interesting, and their high-level goal is relevant to ours.
However, they did not clarify the purity of Rust-style borrowing, as their calculus is impure and
their metatheory does not account for functional behavior. Also, they developed a new type system
with special typing rules for borrowing and lifetimes, whereas our Pure Borrow works in existing
Linear Haskell without modification.

   Monadic regions. Some studies on monadic regions [Fluet and Morrisett 2004, 2006; Kiselyov
and Shan 2008] introduced an extension of the ST monad with region inclusion for better resource
management. While they lack leak freedom, parallelism and borrowing, their monad is, at a high
level, akin to our BO monad, with region inclusion corresponding to (the dual of) lifetime inclusion.

7     Related and Future Work
   Pure model of mutable borrowing. Our use of histories for purely modeling mutable borrowing is
simple but novel, and interestingly different from existing known approaches.
   A notable existing technique proposed by RustHorn [Matsushita et al. 2020, 2021] is to model
Rust’s mutable borrowing functionally by prophecies [Abadi and Lamport 1988]. Prophecies are
a kind of dual of histories and allow getting information about the future, instead of the past, in
advance. In RustHorn, each mutable borrower is modeled using a prophecy that ‘foresees’ the
final value of the borrowed content. Prophecies can model mutable borrowing in a compact way
and thus are useful in automated functional verification, as demonstrated by RustHorn and its
descendant Creusot [Denis et al. 2022]. However, prophecies are not suitable for our denotational
operational semantics, because they require nondeterminism and a precise analysis of the time
point at which the ownership is released.
   Another existing approach is to translate Rust programs into purely functional languages. This
has been explored by Electrolysis [Ullrich 2016] and Aeneas [Ho and Protzenko 2022; Ho 2024].
However, they are quite restrictive in terms of the supported patterns of mutable borrowing.26
Unlike such existing approaches, our model of mutable borrowing using histories can purely model
arbitrary borrowing patterns.

   Type soundness proof of Rust-style borrowing. Our metatheory works toward proving type sound-
ness using an association system, a binary version of a type system, and establishes progress and
bisimulation (a variant of preservation) in the style of Wright and Felleisen [1994]. At a high level,
this strategy is similar to the correctness proof of RustHorn [Matsushita et al. 2020, 2021], which

26 Aeneas cannot handle nested mutable borrowers (e.g., &mut &mut i32) as inputs or outputs of functions [Ho 2024,

    Chapter 10]. Electrolysis also has this restriction [Ullrich 2016, §6.2].
22                                                                                     Yusuke Matsushita and Hiromi Ishii


proved the equivalence of Rust programs and their prophecy-based semantics through a bisimula-
tion. Still, technically, our proof strategy is quite different from theirs. We deal with histories instead
of prophecies, and also tackle advanced features of Haskell, such as first-class polymorphism and
lazy evaluation, unlike for Rust.
   RustBelt [Jung et al. 2018a] and its descendants [Dang et al. 2020; Matsushita et al. 2022; Gäher
et al. 2024; Matsushita and Tsukada 2025] give a semantic, extensible soundness proof for Rust’s
ownership type system extended with some APIs based on the technique of semantic typing, or
logical relations [Timany et al. 2024], using the separation logic Iris [Jung et al. 2015, 2018b]. Finding
such a semantic soundness proof for our Pure Borrow framework is a major challenge left for
future work. All known separation logics that support borrowing, including Iris, are fundamentally
affine and do not guarantee leak freedom. There exists a leak-free separation logic that supports
invariants [Bizjak et al. 2019], but not yet one that supports borrowing. Also, little exploration has
been done on separation logic supporting lazy evaluation.
   Proving purity. Our metatheory §5.5 works toward proving the behavior uniqueness of the phys-
ical execution model, mutative operational semantics, via a bisimulation with a special execution
model, denotational operational semantics, which is designed to be strongly confluent. However, it
does not completely establish purity in a strict sense, because denotational operational semantics
has a subtle side effect: generation of a fresh borrow id δ. The effect of id generation has been
theoretically studied for 𝜈-calculus [Pitts and Stark 1993], exploring non-trivial program equations
(contextual equivalences) as well as game semantics [Abramsky et al. 2004]. As for Pure Borrow,
we conjecture that purity holds despite id generation, thanks to access to each id δ being restricted
to the mutable borrowers and the lender, which can live only inside the linear thunk for the borrow.
A significant challenge for future work is to formulate what purity under linearity is in the first
place and prove that Pure Borrow indeed satisfies it.
   Equational theory. One benefit of the purity of computation is strong support for an equational
theory, which establishes non-trivial contextual equivalences between programs. It is left for future
work to develop a good equational theory for our Pure Borrow framework, prove its soundness,
and explore optimization and verification based on the theory.
   One challenge is that the denotations of programs naïvely induced from our denotational oper-
ational semantics §5.3 (or the denotational dynamic semantics of Bernardy et al. [2018]) do not
satisfy full abstraction (i.e., contextually equivalent programs can have different denotations), due
to linearity constraints on well-typed contexts.27
   Composability with other linear effects. It is interesting to explore what kind of linear effects
our BO monad can compose with. This is non-trivial, especially because BO supports a parallel
execution primitive parBO. We conjecture that the monad is composable with the Reader r monad
for a duplicable type. Further exploration is left for future work.

Acknowledgments
We would like to express our sincere gratitude to Yudai Tanabe, Taro Sekiyama and Atsushi Igarashi
for their valuable feedback and suggestions during the early stages of this work. We heartily
thank Arnaud Spiwack for his insightful and encouraging feedback. We also thank the anonymous
reviewers for their valuable feedback. This research was supported in part by the Hakubi Project
27 For example, let us consider two functions f :: λ !_ → 0 and g :: λ !_ → 42 of the type Vector () → Int. They would have

     different denotations naïvely in our denotational semantics. However, they are contextually equivalent under the linear
     type system, because the type system disallows sharing a linear vector Vector () under an unrestricted arrow → (rather
     than ⊸), making it impossible to call f and g to distinguish them.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                    23


at Kyoto University and JSPS KAKENHI Grant Numbers JP24KJ0133 and JP20H00582 for the first
author, who is also hosted by MPI-SWS as a JSPS Overseas Research Fellow.

Data Availability Statement
Our Haskell implementation of Pure Borrow and our benchmark suite are archived on Zenodo
at [Matsushita and Ishii 2026a]. The latest version is maintained as a public repository at https:
//github.com/SoftwareFoundationGroupAtKyotoU/pure-borrow.

References
Martín Abadi and Leslie Lamport. 1988. The Existence of Refinement Mappings. In Proceedings of the Third Annual
   Symposium on Logic in Computer Science (LICS ’88), Edinburgh, Scotland, UK, July 5-8, 1988. IEEE Computer Society,
   165–175. doi:10.1109/LICS.1988.5115
Samson Abramsky, Dan R. Ghica, Andrzej S. Murawski, C.-H. Luke Ong, and Ian David Bede Stark. 2004. Nominal Games
   and Full Abstraction for the Nu-Calculus. In 19th IEEE Symposium on Logic in Computer Science (LICS 2004), 14-17 July
   2004, Turku, Finland, Proceedings. IEEE Computer Society, 150–159. doi:10.1109/LICS.2004.1319609
Thomas Bagrel. 2024. Destination-passing style programming: a Haskell implementation. In 35es Journées Francophones des
   Langages Applicatifs (JFLA 2024). Saint-Jacut-de-la-Mer, France. https://inria.hal.science/hal-04406360
Thomas Bagrel and Arnaud Spiwack. 2025. Destination Calculus: A Linear 𝜆-Calculus for Purely Functional Memory Writes.
   Proc. ACM Program. Lang. 9, OOPSLA1 (2025), 253–279. doi:10.1145/3720423
Ariel Ben-Yehuda. 2015. std::thread::JoinGuard (and scoped) are unsound because of reference cycles — Rust Issue #24292.
   https://github.com/rust-lang/rust/issues/24292
Jean-Philippe Bernardy, Mathieu Boespflug, Ryan R. Newton, Simon Peyton Jones, and Arnaud Spiwack. 2018. Linear
   Haskell: Practical Linearity in a Higher-Order Polymorphic Language. Proc. ACM Program. Lang. 2, POPL (2018), 5:1–5:29.
   doi:10.1145/3158093
Ales Bizjak, Daniel Gratzer, Robbert Krebbers, and Lars Birkedal. 2019. Iron: Managing Obligations in Higher-Order
   Concurrent Separation Logic. Proc. ACM Program. Lang. 3, POPL (2019), 65:1–65:30. doi:10.1145/3290378
Hoang-Hai Dang, Jacques-Henri Jourdan, Jan-Oliver Kaiser, and Derek Dreyer. 2020. RustBelt Meets Relaxed Memory. Proc.
   ACM Program. Lang. 4, POPL (2020), 34:1–34:29. doi:10.1145/3371102
Nils Anders Danielsson and Thorsten Altenkirch. 2010. Subtyping, Declaratively. In Mathematics of Program Construction, 10th
   International Conference, MPC 2010, Québec City, Canada, June 21-23, 2010. Proceedings (Lecture Notes in Computer Science,
   Vol. 6120), Claude Bolduc, Josée Desharnais, and Béchir Ktari (Eds.). Springer, 100–118. doi:10.1007/978-3-642-13321-3_8
Leonardo Mendonça de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer. 2015. The Lean
   Theorem Prover (System Description). In Automated Deduction - CADE-25 - 25th International Conference on Automated
   Deduction, Berlin, Germany, August 1-7, 2015, Proceedings (Lecture Notes in Computer Science, Vol. 9195), Amy P. Felty and
   Aart Middeldorp (Eds.). Springer, 378–388. doi:10.1007/978-3-319-21401-6_26
Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022. Creusot: A Foundry for the Deductive Verification of Rust
   Programs. In Formal Methods and Software Engineering - 23rd International Conference on Formal Engineering Methods,
   ICFEM 2022, Madrid, Spain, October 24-27, 2022, Proceedings (Lecture Notes in Computer Science, Vol. 13478), Adrián Riesco
   and Min Zhang (Eds.). Springer, 90–105. doi:10.1007/978-3-031-17244-1_6
Dan Doel and Erik de Castro Lopo. 2025. vector-algorithms: Efficient algorithms for vector arrays. https://hackage.haskell.
   org/package/vector-algorithms
Manuel Fähndrich and Robert DeLine. 2002. Adoption and Focus: Practical Linear Types for Imperative Programming. In
   Proceedings of the 2002 ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), Berlin,
   Germany, June 17-19, 2002, Jens Knoop and Laurie J. Hendren (Eds.). ACM, 13–24. doi:10.1145/512529.512532
Matthew Fluet and Greg Morrisett. 2004. Monadic Regions. In Proceedings of the Ninth ACM SIGPLAN International Conference
   on Functional Programming, ICFP 2004, Snow Bird, UT, USA, September 19-21, 2004, Chris Okasaki and Kathleen Fisher
   (Eds.). ACM, 103–114. doi:10.1145/1016850.1016867
Matthew Fluet and Greg Morrisett. 2006. Monadic regions. J. Funct. Program. 16, 4-5 (2006), 485–545. doi:10.1017/
   S095679680600596X
Matthew Fluet, Greg Morrisett, and Amal J. Ahmed. 2006. Linear Regions Are All You Need. In Programming Languages and
   Systems, 15th European Symposium on Programming, ESOP 2006, Held as Part of the Joint European Conferences on Theory
   and Practice of Software, ETAPS 2006, Vienna, Austria, March 27-28, 2006, Proceedings (Lecture Notes in Computer Science,
   Vol. 3924), Peter Sestoft (Ed.). Springer, 7–21. doi:10.1007/11693024_2
Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer. 2024. RefinedRust: A Type System for
   High-Assurance Verification of Rust Programs. Proc. ACM Program. Lang. 8, PLDI (2024), 1115–1139. doi:10.1145/3656422
24                                                                                     Yusuke Matsushita and Hiromi Ishii


Aïna Linn Georges, Benjamin Peters, Laila Elbeheiry, Leo White, Stephen Dolan, Richard A. Eisenberg, Chris Casinghino,
   François Pottier, and Derek Dreyer. 2025. Data Race Freedom à la Mode. Proc. ACM Program. Lang. 9, POPL (2025),
   656–686. doi:10.1145/3704859
Jean-Yves Girard. 1987. Linear Logic. Theor. Comput. Sci. 50 (1987), 1–102. doi:10.1016/0304-3975(87)90045-4
Dan Grossman, Greg Morrisett, Trevor Jim, Michael W. Hicks, Yanling Wang, and James Cheney. 2002. Region-Based
   Memory Management in Cyclone. In Proceedings of the 2002 ACM SIGPLAN Conference on Programming Language Design
   and Implementation (PLDI), Berlin, Germany, June 17-19, 2002, Jens Knoop and Laurie J. Hendren (Eds.). ACM, 282–293.
   doi:10.1145/512529.512563
Philipp Haller and Martin Odersky. 2010. Capabilities for Uniqueness and Borrowing. In ECOOP 2010 - Object-Oriented
   Programming, 24th European Conference, Maribor, Slovenia, June 21-25, 2010. Proceedings (Lecture Notes in Computer
   Science, Vol. 6183), Theo D’Hondt (Ed.). Springer, 354–378. doi:10.1007/978-3-642-14107-2_17
Son Ho. 2024. Formal Verification of Rust Programs by Functional Translation. (Vérification formelle de programmes Rust par
   traduction fonctionnelle). Ph. D. Dissertation. PSL University, France. https://tel.archives-ouvertes.fr/tel-05004605
Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust Verification by Functional Translation. Proc. ACM Program. Lang. 6,
   ICFP (2022), 711–741. doi:10.1145/3547647
C. A. R. Hoare. 1961. Algorithm 64: Quicksort. Commun. ACM 4, 7 (1961), 321. doi:10.1145/366622.366644
Paul Hudak, Simon L. Peyton Jones, Philip Wadler, Brian Boutel, Jon Fairbairn, Joseph H. Fasel, María M. Guzmán, Kevin
   Hammond, John Hughes, Thomas Johnsson, Richard B. Kieburtz, Rishiyur S. Nikhil, Will Partain, and John Peterson.
   1992. Report on the Programming Language Haskell, A Non-strict, Purely Functional Language. ACM SIGPLAN Notices
   27, 5 (1992), 1. doi:10.1145/130697.130699
Jane Street. 2025. OxCaml. https://oxcaml.org/
Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2018a. RustBelt: Securing the Foundations of the
   Rust Programming Language. Proc. ACM Program. Lang. 2, POPL (2018), 66:1–66:34. doi:10.1145/3158154
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018b. Iris from the
   ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
   doi:10.1017/S0956796818000151
Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
   Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning. In Proceedings of the 42nd Annual ACM
   SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2015, Mumbai, India, January 15-17, 2015,
   Sriram K. Rajamani and David Walker (Eds.). ACM, 637–650. doi:10.1145/2676726.2676980
Oleg Kiselyov and Chung-chieh Shan. 2008. Lightweight Monadic Regions. In Proceedings of the 1st ACM SIGPLAN Symposium
   on Haskell, Haskell 2008, Victoria, BC, Canada, 25 September 2008, Andy Gill (Ed.). ACM, 1–12. doi:10.1145/1411286.1411288
John Launchbury. 1993. A Natural Semantics for Lazy Evaluation. In Conference Record of the Twentieth Annual ACM
   SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Charleston, South Carolina, USA, January 1993,
   Mary S. Van Deusen and Bernard Lang (Eds.). ACM Press, 144–154. doi:10.1145/158511.158618
John Launchbury and Simon L. Peyton Jones. 1994. Lazy Functional State Threads. In Proceedings of the ACM SIGPLAN’94
   Conference on Programming Language Design and Implementation (PLDI), Orlando, Florida, USA, June 20-24, 1994, Vivek
   Sarkar, Barbara G. Ryder, and Mary Lou Soffa (Eds.). ACM, 24–35. doi:10.1145/178243.178246
Andrew Lelechenko. 2021. tasty-bench: Featherlight benchmark framework. https://hackage.haskell.org/package/tasty-bench
Anton Lorenzen, Leo White, Stephen Dolan, Richard A. Eisenberg, and Sam Lindley. 2024. Oxidizing OCaml with Modal
   Memory Management. Proc. ACM Program. Lang. 8, ICFP (2024), 485–514. doi:10.1145/3674642
Danielle Marshall, Michael Vollmer, and Dominic Orchard. 2022. Linearity and Uniqueness: An Entente Cordiale. In
   Programming Languages and Systems - 31st European Symposium on Programming, ESOP 2022, Held as Part of the European
   Joint Conferences on Theory and Practice of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings (Lecture
   Notes in Computer Science, Vol. 13240), Ilya Sergey (Ed.). Springer, 346–375. doi:10.1007/978-3-030-99336-8_13
Nicholas D. Matsakis. 2025. Move, Destruct, Forget, and Rust. https://smallcultfollowing.com/babysteps/blog/2025/10/21/
   move-destruct-leak/
Nicholas D. Matsakis and Felix S. Klock, II. 2014. The Rust Language. In Proceedings of the 2014 ACM SIGAda annual
   conference on High integrity language technology, HILT 2014, Portland, Oregon, USA, October 18-21, 2014, Michael B.
   Feldman and S. Tucker Taft (Eds.). ACM, 103–104. doi:10.1145/2663171.2663188
Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: A Semantic Foundation
   for Functional Verification of Rust Programs with Unsafe Code. In PLDI ’22: 43rd ACM SIGPLAN International Conference
   on Programming Language Design and Implementation, San Diego, CA, USA, June 13 - 17, 2022, Ranjit Jhala and Isil Dillig
   (Eds.). ACM, 841–856. doi:10.1145/3519939.3523704
Yusuke Matsushita and Hiromi Ishii. 2026a. Artifact for PLDI 2026 "Pure Borrow: Linear Haskell Meets Rust-Style Borrowing".
   doi:10.5281/zenodo.19622061
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                       25


Yusuke Matsushita and Hiromi Ishii. 2026b. Pure Borrow: Linear Haskell Meets Rust-Style Borrowing. Proc. ACM Program.
   Lang. 10, PLDI (2026). doi:10.1145/3808259
Yusuke Matsushita and Takeshi Tsukada. 2025. Nola: Later-Free Ghost State for Verifying Termination in Iris. Proc. ACM
   Program. Lang. 9, PLDI (2025), 98–124. doi:10.1145/3729250
Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2020. RustHorn: CHC-based Verification for Rust Programs.
   In Programming Languages and Systems - 29th European Symposium on Programming, ESOP 2020, Held as Part of the
   European Joint Conferences on Theory and Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings
   (Lecture Notes in Computer Science, Vol. 12075), Peter Müller (Ed.). Springer, 484–514. doi:10.1007/978-3-030-44914-8_18
Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021. RustHorn: CHC-based Verification for Rust Programs.
   ACM Trans. Program. Lang. Syst. 43, 4 (2021), 15:1–15:54. doi:10.1145/3462205
Yasuhiko Minamide. 1998. A Functional Representation of Data Structures with a Hole. In POPL ’98, Proceedings of the 25th
   ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Diego, CA, USA, January 19-21, 1998,
   David B. MacQueen and Luca Cardelli (Eds.). ACM, 75–84. doi:10.1145/268946.268953
David R. Musser. 1997. Introspective Sorting and Selection Algorithms. Softw. Pract. Exp. 27, 8 (1997), 983–993.
Takashi Nakayama, Yusuke Matsushita, Ken Sakayori, Ryosuke Sato, and Naoki Kobayashi. 2024. Borrowable Fractional
   Ownership Types for Verification. In Verification, Model Checking, and Abstract Interpretation - 25th International
   Conference, VMCAI 2024, London, United Kingdom, January 15-16, 2024, Proceedings, Part II (Lecture Notes in Computer
   Science, Vol. 14500), Rayna Dimitrova, Ori Lahav, and Sebastian Wolff (Eds.). Springer, 224–246. doi:10.1007/978-3-031-
   50521-8_11
Simon L. Peyton Jones and Philip Wadler. 1993. Imperative Functional Programming. In Conference Record of the Twentieth
   Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Charleston, South Carolina, USA,
   January 1993, Mary S. Van Deusen and Bernard Lang (Eds.). ACM Press, 71–84. doi:10.1145/158511.158524
Andrew M. Pitts and Ian David Bede Stark. 1993. Observable Properties of Higher Order Functions that Dynamically Create
   Local Names, or: What’s new?. In Mathematical Foundations of Computer Science 1993, 18th International Symposium,
   MFCS’93, Gdansk, Poland, August 30 - September 3, 1993, Proceedings (Lecture Notes in Computer Science, Vol. 711), Andrzej M.
   Borzyszkowski and Stefan Sokolowski (Eds.). Springer, 122–141. doi:10.1007/3-540-57182-5_8
Arnaud Spiwack, Csongor Kiss, Jean-Philippe Bernardy, Nicolas Wu, and Richard A. Eisenberg. 2022. Linearly Qualified Types:
   Generic Inference for Capabilities and Uniqueness. Proc. ACM Program. Lang. 6, ICFP (2022), 137–164. doi:10.1145/3547626
Arnaud Spiwack, Csongor Kiss, Jean-Philippe Bernardy, Nicolas Wu, and Richard A. Eisenberg. 2026. Linear Constraints.
   CoRR (2026). arXiv:2604.21467 [cs.PL] https://arxiv.org/abs/2604.21467
Nikhil Swamy, Catalin Hritcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon Forest, Karthikeyan Bharga-
   van, Cédric Fournet, Pierre-Yves Strub, Markulf Kohlweiss, Jean Karim Zinzindohoue, and Santiago Zanella-Béguelin.
   2016. Dependent Types and Multi-monadic Effects in F★ . In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT
   Symposium on Principles of Programming Languages, POPL 2016, St. Petersburg, FL, USA, January 20 - 22, 2016, Rastislav
   Bodík and Rupak Majumdar (Eds.). ACM, 256–270. doi:10.1145/2837614.2837655
The Rust Community. 2017. 2094-nll - The Rust RFC Book. https://rust-lang.github.io/rfcs/2094-nll.html
Amin Timany, Robbert Krebbers, Derek Dreyer, and Lars Birkedal. 2024. A Logical Approach to Type Soundness. J. ACM
   71, 6 (2024), 40:1–40:75. doi:10.1145/3676954
Mads Tofte and Jean-Pierre Talpin. 1994. Implementation of the Typed Call-by-Value 𝜆-calculus using a Stack of Regions. In
   Conference Record of POPL’94: 21st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Portland,
   Oregon, USA, January 17-21, 1994, Hans-Juergen Boehm, Bernard Lang, and Daniel M. Yellin (Eds.). ACM Press, 188–201.
   doi:10.1145/174675.177855
David N. Turner, Philip Wadler, and Christian Mossin. 1995. Once Upon a Type. In Proceedings of the seventh international
   conference on Functional programming languages and computer architecture, FPCA 1995, La Jolla, California, USA, June
   25-28, 1995, John Williams (Ed.). ACM, 1–11. doi:10.1145/224164.224168
Sebastian Ullrich. 2016. Simple Verification of Rust Programs via Functional Purification. Master’s thesis. Karlsruhe Institute
   of Technology.
Philip Wadler. 1990. Linear Types can Change the World!. In Programming concepts and methods: Proceedings of the IFIP
   Working Group 2.2, 2.3 Working Conference on Programming Concepts and Methods, Sea of Galilee, Israel, 2-5 April, 1990,
   Manfred Broy and Cliff B. Jones (Eds.). North-Holland, 561.
Andrew Wagner, Olek Gierczak, Brianna Marshall, John M. Li, and Amal Ahmed. 2025. From Linearity to Borrowing. Proc.
   ACM Program. Lang. 9, OOPSLA2, Article 415 (Oct. 2025), 27 pages. doi:10.1145/3764117
Keith Wansbrough and Simon L. Peyton Jones. 1999. Once Upon a Polymorphic Type. In POPL ’99, Proceedings of the 26th
   ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Antonio, TX, USA, January 20-22, 1999,
   Andrew W. Appel and Alex Aiken (Eds.). ACM, 15–28. doi:10.1145/292540.292545
Andrew K. Wright and Matthias Felleisen. 1994. A Syntactic Approach to Type Soundness. Inf. Comput. 115, 1 (1994), 38–94.
   doi:10.1006/INCO.1994.1093
26                                                                                      Yusuke Matsushita and Hiromi Ishii


                             𝑇 ≼ 𝑇 ′ 𝑇 ′ ≼ 𝑇 ′′                                      𝑥 is fresh in 𝑈    𝑈 ≼𝑇
            𝑇 ≼𝑇                                         (∀𝑥 . 𝑇 ) ≼ 𝑇 [𝑎/𝑥]
                                  𝑇 ≼ 𝑇 ′′                                                   𝑈 ≼ ∀𝑥 . 𝑇
 𝑇′ ≼ 𝑇 𝑈 ≼ 𝑈′ 𝜋 ≤ 𝜇                   ∀𝑖. 𝑇𝑖 [𝑈/𝑋 ] ≼ 𝑇𝑖 [𝑈 ′/𝑋 ]       data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                                                                                                        subty-data
  𝑇 →𝜋 𝑈 ≼ 𝑇 ′ →𝜇 𝑈 ′                                                F 𝑈 ≼ F 𝑈¯′
                                                                       ¯
                          𝑇 ≼𝑈                    𝛽 ≤𝛼          𝛽 ≤𝛼    𝑇 ≼𝑈   𝑈 ≼𝑇
                      Ref 𝑇 ≼ Ref 𝑈            End𝛼 ≼ End𝛽         Mut𝛼 𝑇 ≼ Mut𝛽 𝑈
                      𝛽 ≤𝛼     𝑇 ≼𝑈                  𝛼 ≤𝛽 𝑇 ≼𝑈            𝛽 ≤𝛼    𝑇 ≼𝑈
                    Share 𝑇 ≼ Share𝛽 𝑈
                         𝛼                         Lend 𝑇 ≼ Lend 𝑈
                                                       𝛼        𝛽         BO 𝑇 ≼ BO𝛽 𝑈
                                                                            𝛼

                                                  Fig. 25. Subtyping rules.

                             𝛤 ≼ 𝛤 ′ 𝛤 ′ ≼ 𝛤 ′′                 𝜇≤𝜋       𝑇 ≼𝑈
           𝛤 ≼𝛤                                                                                  x ::ω 𝑇 , 𝛤 ≼ 𝛤
                                 𝛤 ≼ 𝛤 ′′                   x ::𝜋 𝑇 , 𝛤 ≼ x ::𝜇 𝑈 , 𝛤
                                      Fig. 26. Rules for typing context inclusion.


Joshua Yanovski, Hoang-Hai Dang, Ralf Jung, and Derek Dreyer. 2021. GhostCell: Separating Permissions from Data in Rust.
   Proc. ACM Program. Lang. 5, ICFP (2021), 1–30. doi:10.1145/3473597


A      Formal Calculus
We present the omitted details of our formal calculus introduced in §5.

A.1       Type System
We present the omitted details of our type system introduced in §5.2.
  Basics. The typing context 𝛤 consists of items of the form x ::𝜋 𝑇 , with the multiplicity 𝜋.28
Î We Î       Î multiplicity product 𝜋 · 𝜇 naturally, i.e., 1 · 𝜋 ≜ 𝜋 · 1 ≜ 𝜋, ω · 𝜋 ≜ 𝜋 · ω ≜ ω,
      define the
  π · μ ≜ (π, μ). This is introduced
                                Î         to define the typing context multiplication 𝜋𝛤 (Fig. 27).
The formal product of variables π is introduced for the multiplicity product.29
   Inclusion and subtyping. The lifetime inclusion 𝛼 ≤ 𝛽 is the partial order over lifetimes generated
by the rules 𝛼 ≤ static, 𝛼 0 ∧ 𝛼 1 ≤ 𝛼 𝑖 and “if 𝛽 ≤ 𝛼 0 and 𝛽 ≤ 𝛼 1 , then 𝛽 ≤ 𝛼 0 ∧ 𝛼 1 ”. The multiplicity
inclusion 𝜋 ≤ 𝜇 is the partial order over multiplicities generated by the rules 1 ≤ 𝜋, 𝜋 ≤ ω,
𝜋𝑖 ≤ 𝜋0 · 𝜋 1 , and “if 𝜋 0 ≤ 𝜇 and 𝜋 1 ≤ 𝜇, then 𝜋 0 · 𝜋 1 ≤ 𝜇”.
   Our type system introduces subtyping natively, without a function like upcast (Fig. 13, §3.2) in
our Haskell implementation. The rules for the subtyping 𝑇 ≼ 𝑈 are listed in Fig. 25. To be precise,
we use mixed induction (i.e., coinduction over induction) to reason about recursive data types,
following the approach of Danielsson and Altenkirch [2010]. More specifically, the subtyping rule
subty-data for the user-defined data type F can be applied coinductively, whereas the other rules
can only be applied inductively. Overall, the subtyping relation is defined as the greatest fixpoint
over the least fixpoint.
   We also introduce the typing context inclusion 𝛤 ≼ 𝛥, which is inductively defined by the rules
listed in Fig. 26. We can weaken the type of a variable by subtyping. A variable of the unrestricted
multiplicity ω can be forgotten and also turned into the multiplicity 1.

28 The order of items in a typing context 𝛤 is ignored. For each variable x, a typing context 𝛤 can contain at most one item

   of the form x ::𝜋 𝑇 . We write ∅ for the empty typing context. The domain dom 𝛤 is defined as { x | x ::𝜋 𝑇 ∈ 𝛤 }.
29 In Î π, the sequence π should be non-empty, and its order is ignored. The substitution ( Î π) [𝜇/μ] is defined by the

     multiplicity product.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                            27


                       𝜋∅ ≜ ∅                𝜋 (x ::𝜇 𝑇 , 𝛤 ) ≜ x ::𝜋 ·𝜇 𝑇 , 𝜋 𝛤               ∅+𝛥 ≜ 𝛥
                                                                                             x ∉ dom 𝛥
     (x ::ω 𝑇 , 𝛤 ) + (x ::ω 𝑇 , 𝛥) ≜ x ::ω 𝑇 , (𝛤 + 𝛥)
                                                                             (x ::𝜋 𝑇 , 𝛤 ) + 𝛥 ≜ x ::𝜋 𝑇 , (𝛤 + 𝛥)
                                           Fig. 27. Operations on typing contexts.


              data () where () :: ()                     data Bool where True:: Bool, False:: Bool
     data Ur 𝑋 where Ur :: 𝑋 → Ur 𝑋                                 data (𝑋, 𝑌 ) where (,) :: 𝑋 ⊸ 𝑌 ⊸ (𝑋, 𝑌 )
                                           Fig. 28. Default data type declarations.

     𝛥 ≼ 𝛤 𝛤 ⊢ 𝑡 :: 𝑇                𝛤 ⊢ 𝑡 :: 𝑇 𝑇 ≼ 𝑈               𝑥 is fresh in 𝛤       𝛤 ⊢ 𝑡 :: 𝑇
                                                                                                               x ::𝜋 𝑇 ⊢ x :: 𝑇
        𝛥 ⊢ 𝑡 :: 𝑇                       𝛤 ⊢ 𝑡 :: 𝑈                         𝛤 ⊢ 𝑡 :: ∀𝑥 . 𝑇
            ∀𝑖. 𝛤𝑖 ⊢ 𝑡 :: 𝑇𝑖     x ::𝜋 𝑇 , 𝛥 ⊢ 𝑢 :: 𝑈              ∀𝑖. x ::ω 𝑇 , 𝛤 ⊢ 𝑡𝑖 :: 𝑇𝑖 x ::ω 𝑇 , 𝛥 ⊢ 𝑢 :: 𝑈
                               let x = 𝑡 in 𝑢 :: 𝑈                          ω𝛤 + 𝛥 ⊢ let x = 𝑡 in 𝑢 :: 𝑈
              Í
                𝑖 𝜋 𝛤𝑖 + 𝛥   ⊢
         x ::𝜋 𝑇 , 𝛤 ⊢ 𝑡 :: 𝑈                 𝛤 ⊢ 𝑡 :: 𝑇 →𝜋 𝑈        𝛥 ⊢ 𝑢 :: 𝑇                x ∈ dom 𝛤      𝛤 ⊢ 𝑡 :: 𝑇
       𝛤 ⊢ λ x→ 𝑡 :: 𝑇 →𝜋 𝑈                           𝛤 + 𝜋 𝛥 ⊢ 𝑡 𝑢 :: 𝑈                           𝛤 ⊢ seq x 𝑡 :: 𝑇
                                        ∀𝑖. 𝛤𝑖 ⊢ 𝑡𝑖 :: 𝑇 𝑗,𝑖 [𝑈/𝑋 ]     data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                      ⊢ 𝑛:: Int                                Í
                                                                 𝑖 𝑗,𝑖 𝑖 ⊢ C 𝑗 𝑡¯ :: F 𝑈
                                                                   𝜋  𝛤                ¯
                                                                                     𝛼
                          𝛤 ⊢ 𝑡 :: F 𝑈¯                                  𝛤 ⊢ 𝑡 :: 𝐵 (F 𝑈¯ )
         ∀ 𝑗 . x ::𝜋 𝑗 𝑇 𝑗 [𝑈/𝑋 ], 𝛥 ⊢ 𝑢 𝑗 :: 𝑈 ′           ∀ 𝑗 . x ::𝜋 𝑗 𝐵𝛼 (𝑇 𝑗 [𝑈/𝑋 ]), 𝛥 ⊢ 𝑢 𝑗 :: 𝑈 ′
         data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯                       data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                                                                                                            ty-case-bor
        𝛤 + 𝛥 ⊢ case 𝑡 of { C x̄→ 𝑢 }:: 𝑈 ′                  𝛤 + 𝛥 ⊢ case 𝑡 of { C x̄→ 𝑢 }:: 𝑈 ′
        𝑎 :: 𝑇¯ ; 𝑈    ∀𝑖. 𝛤𝑖 ⊢ 𝑡𝑖 :: 𝑇𝑖
               Í                                 iop :: Int; Int          irel :: Int; Bool            par :: 𝑇 , 𝑈 ; (𝑇 , 𝑈 )
                   𝛤
                  𝑖 𝑖 ⊢ 𝑎 𝑡¯ :: 𝑈
    𝑇 is Linearly or Mut𝛼 𝑈           𝑇 is Int, End𝛼 or Share𝛼 𝑈
                                                                           linearly :: Linearly ⊸ Ur 𝑇 ; Ur 𝑇
        consume :: 𝑇 ; ()                    move :: 𝑇 ; Ur 𝑇
         𝑇 is Linearly, Ref 𝑈 , Now𝛼 or Mut𝛼 𝑈
                                                           newRef :: 𝑇 ; Ref 𝑇         freeRef :: Ref 𝑇 ; 𝑇
             withLinearly :: 𝑇 ; (Linearly, 𝑇 )
                       newLifetime :: (∀ι. Now al ι ⊸ 𝑇 ); 𝑇              endLifetime :: Now al ι ; End al ι
                 borrow :: Linearly, 𝑇 ; (Mut𝛼 𝑇 , Lend𝛼 𝑇 )                share :: Mut𝛼 𝑇 ; Ur (Share𝛼 𝑇 )
     𝑇 is Int, End𝛽 or Share𝛽 𝑈
                                              joinMut :: 𝐵𝛼 (Mut𝛽 𝑇 ); 𝐵𝛼∧𝛽 𝑇                 reclaim :: Lend𝛼 , 𝑇 End𝛼 ; 𝑇
         copy :: Share𝛼 𝑇 ; 𝑇
    execBO :: Now𝛼 , BO𝛼 𝑇 ; (Now𝛼 ,𝑇 )                 pure :: 𝑇 ; BO𝛼 𝑇           (≫=) :: BO𝛼 𝑇 , 𝑇 ⊸ BO𝛼 𝑈 ; BO𝛼 𝑈
           sexecBO :: Now𝛼 , BO𝛼∧𝛽 𝑈 ; BO𝛽 (Now𝛼 , 𝑈 )                      parBO :: BO𝛼 𝑇 , BO𝛼 𝑈 ; BO𝛼 (𝑇 , 𝑈 )
                                                                            𝛽 ≤𝛼
  deref :: 𝐵𝛼 (Ref 𝑇 ); BO𝛼 (𝐵𝛼 𝑇 )
                                              updateRef :: 𝑇 ⊸ BO𝛽 (𝑈 ,𝑇 ), Mut𝛼 (Ref 𝑇 ); BO𝛽 (𝑈 , Mut𝛼 (Ref 𝑇 ))
                                                    Fig. 29. Typing rules.


  Operations on typing contexts. Following Bernardy et al. [2018], we introduce the multiplication
𝜋𝛤 and the sum 𝛤 + 𝛥 over typing contexts, defined in Fig. 27. Intuitively, 𝛤 + 𝛥 allows sharing
unrestricted variables between 𝛤 and 𝛥.
28                                                                                    Yusuke Matsushita and Hiromi Ishii


   Typing rules. The typing rules are listed in Fig. 29. For this, we assume the default data type
declarations listed in Fig. 28. The typing judgment has the form 𝛤 ⊢ 𝑡 :: 𝑇 . For operators op and
monad constructors mo, we introduce an auxiliary judgment 𝑎:: 𝑇¯ ; 𝑈 (where 𝑎 is either op or mo
and the length of 𝑇¯ is the arity of 𝑎), meaning that 𝑎 linearly inputs arguments of the type 𝑇¯ and
outputs an object of the type 𝑈 .
   We have two typing rules for typing the case term. The latter ty-case-bor is for the case where
the pattern-matched term is a borrower 𝐵𝛼 (F 𝑈¯ ). We distribute the borrower constructor 𝐵𝛼 to
the components x̄ of the data. This is an idealized version of the API functions such as splitPair
(Fig. 12, §3.2) in our Haskell implementation.

A.2       Two Operational Semantics
We present the omitted details of our two operational semantics introduced in §5.3.
   Basics. In denotational operational semantics, we use a borrower constructor 𝐵,    ¤ where a mutable
                 ¯
borrower Mut is marked with borrow paths 𝑝¯ , representing which part of which lenders the
                 𝑝

borrower refers to. Here, we can have multiple borrow paths due to the reborrowing caused by
joinMut, as clarified by the reduction rule dred-join-bor shown later in Fig. 36b. We use a borrower
context 𝐵¤̄ for a composite of borrower constructors. We write 𝐵¤̄ 𝑎 instead of 𝐵¤̄ [𝑎] for readability.
   In both semantics, an environment 𝐸,    ˆ 𝐸¤ assigns a term 𝑡ˆ, 𝑡¤ to each variable x. A denotational
environment 𝐸¤ additionally manages the borrow ids δ¯ that have been created.30 The memory 𝑀
appears only in mutative semantics.31 A configuration has the form 𝐸;       ˆ 𝑀; x in mutative semantics
and 𝐸;¤ x in denotational semantics, where x is the top-level variable.32 We say that 𝐸;      ˆ 𝑀; x is a
normal form if 𝐸 has an item of the form x = 𝑣. Likewise, we say that 𝐸; x is a normal form if 𝐸¤ has
                   ˆ                             ˆ                           ¤
an item of the form x = 𝑣.¤
   Strictness works as follows in this language. For simplicity, all the arguments of operators are
made strict. In particular, par 𝑡 𝑢 forces the evaluation of 𝑡 and 𝑢 before returning the pair of their
results. Also, we introduce a special term seq x 𝑡 that forces the evaluation of the variable x before
returning 𝑡; it amounts to do◦ !x ← x; t in Haskell, and we introduce seq as a primitive for the
bang ! pattern. The usual function application is lazy. Pattern matching of case is strict.
   Figure 30 shows additional syntax for the two operational semantics, omitted in Fig. 21.
   The denesting context 𝑁 is used for turning a nested term into an unnested one, by binding
subterms to fresh variables (see mred-denest and dred-denest later shown in Fig. 33).33 Denesting
is a dynamic version of conversion to the A-normal (or K-normal) form.
   We introduce extra values 𝑑,  ˆ 𝑑¤ and extra operators op,
                                                            ˆ op¤ for the two semantics. For monadic
                                  ◦
extra operators such as execBO , the superscript ◦ indicates post-processing, + pre-processing, and
• pre-processing before post-processing. The value ∅/∅𝐻 represents the value of linearity witness
tokens Linearly and lifetime tokens Now𝛼 , End𝛼 ; in denotational semantics, the lifetime tokens
carry the history 𝐻 .
  Composing histories. We define the parallel 𝐻 · 𝐻 ′ and sequential 𝐻 /𝐻 ′ compositions of histories,
as defined in Fig. 31. The parallel composition 𝐻 · 𝐻 ′ treats both histories equally (and thus is
                                        ˆ 𝐸¤ is ignored. An environment 𝐸,
30 The order of items in an environment 𝐸,                              ˆ 𝐸¤ can have at most one item of the form x = 𝑎
     for each variable x. Also, a denotational environment 𝐸¤ can have at most one occurrence of each borrow id δ.
31 The order of items in a memory 𝑀 is ignored. A memory 𝑀 can have at most one item of the form ℓ ↦→ x for each location

     ℓ.
32 We assume alpha-equivalence over mutative configurations 𝐸;
                                                            ˆ 𝑀; x with respect to variable names x bound in the
                ˆ and assume alpha-equivalence over denotational configurations 𝐸;
   environment 𝐸,                                                                  ¤ x with respect to variable names x
   and borrow id names δ bound in the environment 𝐸.  ¤
33 We impose left-to-right order in denesting to avoid unnecessary nondeterminism.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                     29


              Denesting context         𝑁 F [·] 𝑡 | x [·] | seq x [·] | C x̄ [·] 𝑡¯
                                           | case [·] of { C x̄→ 𝑡 } | op x̄ [·] 𝑡¯ | mo x̄ [·] 𝑡¯
                                                 (a) Common things.

 Extra operator opˆ F linear 1 | exeBO 1                           Borrower context 𝐵¤̄ F [·] | 𝐵¤ 𝐵¤̄
    | execBO 1 | (≫=◦ ) 2 | sexecBO+ 2
             ◦                                              Extra operator op ¤ F linear 1 | exeBO𝐻 1
    | sexecBO◦ 1 | parBO◦ 2 | deref◦ 1                         | execBO◦ 1 | (≫=◦ ) 2 | sexecBO𝐻+
                                                                                                   2
                                                                         ◦              ◦          ◦
                                                               | sexecBO𝐻 ;𝐻 ′ 1 | parBO𝐻 2 | deref𝐻 1
    | updateRef+ 2 | updateRefℓ• 1                                         +               •
                                                               | updateRef𝐻   2 | updateRef𝑝¯ 1
    | updateRefℓ◦ 1                                                        ◦
                                                               | updateRef𝑝;𝐻
                                                                           ¯    1
             (b) For mutative semantics.                                (c) For denotational semantics.

                              Fig. 30. More syntax for the two operational semantics.

                                                      (𝑝 ←x, 𝐻 ) / (𝑝 ←y, 𝐻 ′ ) ≜ 𝑝 ←y, (𝐻 /𝐻 ′ )
                          ′
      dom 𝐻 ∩ dom 𝐻 = ∅
        𝐻 · 𝐻 ′ ≜ 𝐻, 𝐻 ′                                    𝑝 ∉ dom 𝐻 ′
                                                                                                 ∅/𝐻 ≜ 𝐻
                                                (𝑝 ←x, 𝐻 ) / 𝐻 ′ ≜ 𝑝 ←x, (𝐻 /𝐻 ′ )
                     Fig. 31. Parallel 𝐻 · 𝐻 ′ and sequential 𝐻 /𝐻 ′ composition of histories.


                x = 𝐾ˆ [y] ∈ 𝐸ˆ     ˆ 𝑀; y loop
                                    𝐸;                               x = 𝐾¤ [y] ∈ 𝐸¤     ¤ y loop
                                                                                         𝐸;
                           ˆ 𝑀; x loop
                           𝐸;                                                   ¤ x loop
                                                                                𝐸;
        Fig. 32. The coinductive rule of the forcing loop predicate 𝐺ˆ loop, 𝐺¤ loop for each semantics.


commutative), while the sequential composition 𝐻 /𝐻 ′ overwrites older records 𝐻 with newer
ones 𝐻 ′ . The domain dom 𝐻 is defined as {𝑝 | 𝑝 ←x ∈ 𝐻 }.
   Reduction rules. Now we inductively define the small-step reduction relations 𝐺ˆ → 𝐺ˆ ′ and
𝐺¤ → 𝐺¤ ′ for mutative and denotational operational semantics, respectively.
   The basic reduction rules for the two semantics are listed in Fig. 33.34 The rules mred-loop and
dred-loop use the forcing loop predicate 𝐺ˆ loop, 𝐺¤ loop, meaning that the environment contains
variables that circularly forcing one another, coinductively defined by the rules in Fig. 32. The two
semantics are mostly the same in these rules, but there are some notable differences due to borrower
constructors 𝐵,¤ appearing only in denotational semantics. The rule dred-var for a variable term
carries the borrower context 𝐵. ¤̄ Also, the rule dred-case-bor distributes the borrower constructor
 ¤
𝐵 over the data components (recall the typing rule ty-case-bor in Fig. 29).
   The reduction rules for basic operators for denotational semantics are listed in Fig. 34. The rules
for mutative semantics are just analogous to them. The operator linearly allows binding the result
of a linear computation to an unrestricted variable. We use an extra operator linear to clarify that
boundary for our association system Appendix B.
   The basic reference-related reduction rules for the two semantics are presented in Fig. 35. In
mutative semantics, a reference is modeled as Ref ℓ with a location ℓ, whose content x is separately
stored as ℓ ↦→ x in the global memory 𝑀; in denotational semantics, a reference is modeled as Ref x,
where the body content x is locally stored in the value. The ownership justifies this.
34 The function asBool maps the truth and falsehood to True and False, respectively.
30                                                                                       Yusuke Matsushita and Hiromi Ishii


                   x = 𝐾ˆ [y] ∈ 𝐸ˆ     ˆ 𝑀; y → 𝐸ˆ′ ; 𝑀 ′ ; y
                                      𝐸;                                       𝐺ˆ loop
                                                                mred-ktx               mred-loop
                              ˆ 𝑀; x → 𝐸ˆ′ ; 𝑀 ′ ; x
                              𝐸;                                               𝐺ˆ → 𝐺ˆ
     x = let y = 𝑡 in 𝑢, 𝐸;ˆ 𝑀; x →                                    𝑡 ∉ Var
                                                                                                 mred-denest
                     y = 𝑡, x = 𝑢, 𝐸;
                                   ˆ 𝑀; x           x = 𝑁 [𝑡], 𝐸;
                                                               ˆ 𝑀; x → y = 𝑡, x = 𝑁 [y], 𝐸;
                                                                                          ˆ 𝑀; x
                           y = 𝑣ˆ ∈ 𝐸ˆ                                             f = λ y→ 𝑡 ∈ 𝐸ˆ
                                                     mred-var
                     ˆ 𝑀; x → x = 𝑣,
              x = y, 𝐸;              ˆ 𝑀; x
                                  ˆ 𝐸;                                            ˆ 𝑀; x → x = 𝑡, 𝐸;
                                                                         x = f y, 𝐸;               ˆ 𝑀; x
                  y = 𝑣ˆ ∈ 𝐸
                           ˆ                                                  y = C𝑖 z ′ ∈ 𝐸ˆ
 x = seq y z, 𝐸;
              ˆ 𝑀; x → x = z, 𝐸;
                              ˆ 𝑀; x                   x = case y of { C z̄→ 𝑡 }, 𝐸;
                                                                                  ˆ 𝑀; x → z 𝑖 = z ′, x = 𝑡𝑖 , 𝐸;
                                                                                                               ˆ 𝑀; x
                                         (a) For mutative operational semantics.
                      x = 𝐾¤ [y] ∈ 𝐸¤         ¤ y → 𝐸¤′ ; y
                                              𝐸;                                      𝐺¤ loop
                                                                 dred-ktx                      dred-loop
                                    ¤ x → 𝐸¤ ; x
                                    𝐸;        ′                                       𝐺¤ → 𝐺¤
         x = let y = 𝑡 in 𝑢, 𝐸;¤ x →                                           𝑡 ∉ Var
                                            ¤ x                                                        dred-denest
                            y = 𝑡, x = 𝑢, 𝐸;                            ¤ x → y = 𝑡, x = 𝑁 [y], 𝐸;
                                                             x = 𝑁 [𝑡], 𝐸;                         ¤ x
                                y = 𝑣¤ ∈ 𝐸¤                                           f = λ y→ 𝑡 ∈ 𝐸¤
                                                          dred-var
                   x = 𝐵¤̄ y, 𝐸;
                              ¤ x → x = 𝐵¤̄ 𝑣,      ¤ x
                                                 ¤ 𝐸;                                    ¤ x → x = 𝑡, 𝐸;
                                                                                x = f y, 𝐸;             ¤ x
                     y = 𝑣¤ ∈ 𝐸   ¤                                                         ′
                                                                                  y = C𝑖 z ∈ 𝐸  ¤
          x = seq y z, 𝐸;
                        ¤ x → x = z, 𝐸;   ¤ x              x = case y of { C z̄→ 𝑡 }, 𝐸;  ¤ x → z 𝑖 = z ′, x = 𝑡𝑖 , 𝐸;
                                                                                                                    ¤ x
                                                                 
                       y = 𝐵¤ (C𝑖 z ′ ) ∈ 𝐸¤       ∀ 𝑗 . 𝐵¤ ′𝑗 = Mut
                                                                         𝑝.𝑗 𝐵¤ = Mut  ¯
                                                                                       𝑝
                                                                   Share 𝐵¤ = Share
                                                                                            dred-case-bor
                     x = case y of { C z̄→ 𝑡 }, 𝐸;    ¤ x → z 𝑖 = 𝐵¤ ′ z ′, x = 𝑡𝑖 , 𝐸;
                                                                                      ¤ x
                                      (b) For denotational operational semantics.
                                              Fig. 33. Basic reduction rules.


     The borrow-related reduction rules for the two semantics are listed in Fig. 36. Here we clearly see
the differences between the two semantics. In denotational semantics, for each new borrow, a fresh
borrow id δ is created, and the lender is modeled as Lendδ x, where the x represents the original
version of the borrowed object. Notably, when the lender reclaims the ownership of the borrowed
object by dred-reclaim, the latest version of the object is restored from the history. For this, we
introduce the restoration-by-history predicate restore𝐻 𝑝 𝐸¤ x ;y 𝐸¤′ , inductively defined by the
rules listed in Fig. 36c. The predicate adds new items to the environment 𝐸¤ to get 𝐸¤′ , reflecting
updates recorded in the history 𝐻 on the borrow path 𝑝 for the variable x, returning a new variable
x ′ . The predicate does nothing and just returns 𝐸¤ and x if the history does not contain any relevant
update, while the predicate takes a fresh variable x ′ for the new version of x otherwise.
     Basic monadic reduction rules for denotational semantics are listed in Fig. 37. The rules for
mutative semantics are just analogous to them, just without the history information 𝐻 . We internally
use the extra operator exeBO/exeBO𝐻 , a utility variant of execBO, to execute a monad without
carrying around the live lifetime token. It returns Done x/Done𝐻 x for the result of the computation.
What is important is how to handle histories. The scoped execution sexecBO executes the monad bo
with the empty history, whose resulting history 𝐻 0 is then sequentially composed with the original
histories 𝐻 , 𝐻 ′ . The parallel execution parBO executes the monads bo0 , bo1 respectively with the
empty history and then composes the resulting histories 𝐻 0 , 𝐻 1 in parallel, whose composite is
sequentially composed with the original history 𝐻 .
     Reference-related monadic reduction rules for the two semantics are listed in Fig. 38. Like in
Fig. 35, mutative operational semantics accesses the memory 𝑀 while denotational operational
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                  31


      y = 𝑛 ∈ 𝐸ˆ 𝑚 = iop 𝑛¯                y = 𝑛 ∈ 𝐸ˆ        𝑏 = asBool(irel 𝑛)
                                                                             ¯                   ˆ z = 𝑤ˆ ∈ 𝐸ˆ
                                                                                            y = 𝑣,
                ˆ 𝑀; x →
    x = iop ȳ, 𝐸;                                       ˆ 𝑀; x →
                                            x = irel ȳ, 𝐸;                                        ˆ 𝑀; x →
                                                                                      x = par y z, 𝐸;
                   x = 𝑚, 𝐸;
                          ˆ 𝑀; x                              x = 𝑏, 𝐸;
                                                                     ˆ 𝑀; x                        x = (y, z), 𝐸;
                                                                                                               ˆ 𝑀; x

                        y = 𝑣ˆ ∈ 𝐸ˆ                                                  y = 𝑣ˆ ∈ 𝐸ˆ
                        ˆ 𝑀; x → x = (), 𝐸;
         x = consume y, 𝐸;               ˆ 𝑀; x                                 ˆ 𝑀; x → x = Ur y, 𝐸;
                                                                    x = move y, 𝐸;                 ˆ 𝑀; x

                           f = 𝑣ˆ ∈ 𝐸ˆ                                                        y = 𝑣ˆ ∈ 𝐸ˆ
 x = linearly f , 𝐸; 𝑀; x → li = ∅, y = f li, x = linear y, 𝐸;
                  ˆ                                         ˆ 𝑀; x            x = linear y, 𝐸; 𝑀; x → x = 𝑣,
                                                                                            ˆ                ˆ 𝑀; x
                                                                                                          ˆ 𝐸;
                                                        y = 𝑣ˆ ∈ 𝐸ˆ
                                                  ˆ 𝑀; x → li = ∅, x = (li, y), 𝐸;
                              x = withLinearly y, 𝐸;                            ˆ 𝑀; x
                                        (a) For mutative operational semantics.
    y = 𝑛 ∈ 𝐸¤ 𝑚 = iop 𝑛¯                 y = 𝑛 ∈ 𝐸¤ 𝑏 = asBool(irel 𝑛) ¯                  y = 𝑣,¤ z = 𝑤¤ ∈ 𝐸¤
             ¤ x → x = 𝑚, 𝐸;
 x = iop ȳ, 𝐸;           ¤ x                          ¤             ¤
                                          x = irel ȳ, 𝐸; x → x = 𝑏, 𝐸; x                      ¤                  ¤ x
                                                                                  x = par y z, 𝐸; x → x = (y, z), 𝐸;
                            y = 𝑣¤ ∈ 𝐸¤                                         y = 𝑣¤ ∈ 𝐸¤
                                ¤ x → x = (), 𝐸;
                 x = consume y, 𝐸;            ¤ x                               ¤ x → x = Ur y, 𝐸;
                                                                    x = move y, 𝐸;              ¤ x

                    f = 𝑣¤ ∈ 𝐸¤                            y = 𝑣¤ ∈ 𝐸¤                        y = 𝑣¤ ∈ 𝐸¤
                      ¤ x →
     x = linearly f , 𝐸;                                          ¤ x →
                                                    x = linear y, 𝐸;                                     ¤ x →
                                                                                    x = withLinearly y, 𝐸;
                                           ¤ x
           li = ∅, y = f li, x = linear y, 𝐸;                             ¤ x
                                                                       ¤ 𝐸;
                                                                   x = 𝑣,                                         ¤ x
                                                                                             li = ∅, x = (li, y), 𝐸;
                                      (b) For denotational operational semantics.
                                     Fig. 34. Reduction rules for basic operators.

                         li = ∅, y = 𝑣ˆ ∈ 𝐸ˆ                                         li = ∅, y = 𝑣¤ ∈ 𝐸¤
                      ˆ 𝑀; x → x = Ref ℓ, 𝐸;
     x = newRef li y, 𝐸;                   ˆ ℓ ↦→ y, 𝑀; x                                  ¤ x → x = Ref y, 𝐸;
                                                                          x = newRef li y, 𝐸;                ¤ x
                          y = Ref ℓ ∈ 𝐸
                                      ˆ                                                y = Ref z ∈ 𝐸 ¤
                       ˆ ℓ ↦→ z, 𝑀; x → x = z, 𝐸;
        x = freeRef y, 𝐸;                       ˆ 𝑀; x                                       ¤ x → x = z, 𝐸;
                                                                             x = freeRef y, 𝐸;            ¤ x
                   (a) For mutative semantics.                                (b) For denotational semantics.
                                   Fig. 35. Basic reference-related reduction rules.


semantics locally operates on the body of Ref. Crucially, in denotational semantics, the reference
update updateRef records the update 𝑝 ←y to the history 𝐻 for each borrow path 𝑝 of the mutable
borrower. Also, the dereference deref distributes the borrower constructor, modifying the borrow
path, just like in dred-case-bor.

B     Association System
We present the omitted details of our association system introduced in §5.4.

B.1     Overview
     Syntax. The syntax for the association system is shown in Fig. 39.
     A lifetime path 𝜌 = ι.𝑖 represents a part of an atomic lifetime al ι. We introduce extended types
𝑇˚ , which include Done𝜌¯ 𝑇 to represent the result of exeBO/exeBO𝐻 and the skeleton type Skel 𝑇
to represent a borrower whose lender has already reclaimed. The resource context 𝛤˚ extends the
typing context 𝛤 with more information about the dynamic ownership.35 A variable-type binding
35 The order of items in a resource context 𝛤˚ is ignored.
32                                                                                      Yusuke Matsushita and Hiromi Ishii


                         li = ∅, f = 𝑣ˆ ∈ 𝐸ˆ                                   now = ∅ ∈ 𝐸ˆ
                                     ˆ 𝑀; x →
              x = newLifetime li f , 𝐸;                                                 ˆ 𝑀; x →
                                                                  x = endLifetime now, 𝐸;
                          now = ∅, x = f now, 𝐸;
                                              ˆ 𝑀; x                                  x = Ur now, 𝐸;
                                                                                                  ˆ 𝑀; x
                       li = ∅, y = 𝑣ˆ ∈ 𝐸ˆ                                       y = 𝑣ˆ ∈ 𝐸ˆ
                            ˆ 𝑀; x →
           x = borrow li y, 𝐸;                                                 ˆ 𝑀; x → x = Ur y, 𝐸;
                                                                  x = share y, 𝐸;                 ˆ 𝑀; x
                         ˆ yl = 𝑣,
                   ym = 𝑣,      ˆ x = (ym, yl ), 𝐸;
                                                 ˆ 𝑀; x

          y = 𝑣ˆ ∈ 𝐸ˆ                              y = 𝑣ˆ ∈ 𝐸ˆ                               end = ∅, y = 𝑣ˆ ∈ 𝐸ˆ
             ˆ 𝑀; x →
 x = copy y, 𝐸;                                           ˆ 𝑀; x →
                                          x = joinMut y, 𝐸;                                             ˆ 𝑀; x →
                                                                                     x = reclaim y end, 𝐸;
                 x = 𝑣, ˆ 𝑀; x
                     ˆ 𝐸;                                  x = 𝑣, ˆ 𝑀; x
                                                               ˆ 𝐸;                                        x = y, 𝐸;
                                                                                                                  ˆ 𝑀; x
                                        (a) For mutative operational semantics.
                   li = ∅, f = 𝑣¤ ∈ 𝐸¤                                         now = ∅𝐻 ∈ 𝐸¤
                               ¤ x →
        x = newLifetime li f , 𝐸;                                                   ¤ x → x = Ur now, 𝐸;
                                                               x = endLifetime now, 𝐸;                ¤ x
                                             ¤ x
                        now = ∅∅, x = f now, 𝐸;
                     li = ∅, y = 𝑣¤ ∈ 𝐸¤                                          y = Mut𝑝¯ 𝑣¤ ∈ 𝐸¤
                       ¤ x → ym = Mutδ 𝑣,
     x = borrow li y, 𝐸;                   ¤                                   ¤ x → y ′ = Share 𝑣,
                                                                  x = share y, 𝐸;                               ¤ x
                                                                                                    ¤ x = Ur y, 𝐸;
                                                      ¤ x
                      yl = Lendδ y, x = (ym, yl ), δ, 𝐸;
                                                                                 
                                                                                 ¯ 𝑞¯ ¤
                                               y = 𝐵¤ (Mut𝑞¯ 𝑣)
                                                             ¤ ∈ 𝐸¤        Mut𝑝,
                                                                        𝐵¤ ′ =         𝐵 = Mut𝑝¯
            y = Share 𝑣¤ ∈ 𝐸¤                                              Share 𝐵¤ = Share
                                                                                                 dred-join-bor
                 ¤ x → x = 𝑣,
     x = copy y, 𝐸;             ¤ x
                              ¤ 𝐸;                                   ¤ x → x = 𝐵¤ ′ 𝑣,
                                                      x = joinMut y, 𝐸;             ¤ 𝐸;¤ x
                                                                         ′
                        end = ∅𝐻 , y = Lendδ z ∈ 𝐸¤   restore𝐻 δ 𝐸¤ z ;z 𝐸¤′
                                                                             dred-reclaim
                                                  ¤ x → x = z ′, 𝐸¤′ ; x
                               x = reclaim y end, 𝐸;
                                      (b) For denotational operational semantics.
                                                                                                     ′
                ∀𝑖¯. 𝑝.𝑖 ∉ dom 𝐻              𝑝 ←y ∈ 𝐻          x = Ref z ∈ 𝐸¤   restore𝐻 𝑝.0 𝐸¤ y ;y 𝐸¤′
                                                                               ′
              restore𝐻 𝑝 𝐸¤ x ;x 𝐸¤                         restore𝐻 𝑝 𝐸¤ x ;x x ′ = Ref y ′, 𝐸¤′
                𝑝 ∉ dom 𝐻    𝑝.𝑗 ∈ dom 𝐻                        𝑝 ∉ dom 𝐻     𝑝.𝑗 ∈ dom 𝐻       x = 𝐵¤̄ (C ȳ 𝑛 ) ∈ 𝐸¤
                                                  ′                                                       ′
     x = 𝐵¤̄ (Ref y) ∈ 𝐸¤ restore𝐻 𝑝.0 𝐸¤ y ;y 𝐸¤′                  𝐸¤0 = 𝐸¤  ∀𝑖. restore𝐻 𝑝.𝑖 𝐸¤𝑖 y𝑖 ;y𝑖 𝐸¤𝑖+1
         restore 𝑝 𝐸¤ x ;x x ′ = 𝐵¤̄ (Ref y), 𝐸¤′                     restore 𝑝 𝐸¤ x ;x x ′ = 𝐵¤̄ (C y¯′ ), 𝐸¤
                           ′                                                             ′
                  𝐻                                                            𝐻                               𝑛

                           (c) The restoration-by-history predicate restore𝐻 𝑝 𝐸¤ x ;y 𝐸¤′ .
                                        Fig. 36. Borrow-related reduction rules.


x ::𝑃𝜋 𝑇˚ in a resource context is marked with the set of borrow paths 𝑃 that the variable may be
able to update (we omit the superscript 𝑃 if it is empty). This information is vital to justify parBO,
ensuring that the borrow paths updated by the two monad arguments are mutually disjoint. A
resource context also contains borrow ids δ, variable-term bindings x = 𝑡ˆ ∝ 𝑡¤, x = 𝑣,
                                                                                      ¤ and points-to
tokens ℓ ↦→ x from the environments and memory. Importantly, bindings x = 𝑣ˆ ∝ 𝑣,        ¤ x = 𝑣¤ over
values are shareable. A captured points-to token ℓ ↦→ ¤ x represents a usual points-to token captured
inside linear (please see assoc-linear shown later).
    Interestingly, a resource context can even contain polymorphic resource contexts ∀𝑥 . 𝛤˚ to reason
about first-class polymorphism of Haskell. For example, we can create a polymorphic reference
∀𝑋 . Ref [𝑋 ] to a list of any type from the nil list [] :: ∀𝑋 . [𝑋 ], and then borrow it to create a
polymorphic pair ∀α, 𝑋 . (Mutα (Ref [𝑋 ]), Lendα (Ref [𝑋 ])) of a borrower and a lender. Because
the variables α, 𝑋 are instantiated dynamically, we have to keep the polymorphism over α, 𝑋 in
creating the ghost state for the borrow.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                  33


                      now = ∅, bo = 𝑣ˆ ∈ 𝐸ˆ                                  res = Done y ∈ 𝐸ˆ
        x = execBO now bo, 𝐸;ˆ 𝑀; x →                               x = execBO◦ res, 𝐸;
                                                                                     ˆ 𝑀; x →
               res = exeBO bo, x = execBO◦ res, 𝐸;
                                                ˆ 𝑀; x                     now = ∅, x = (now, y) , 𝐸;
                                                                                                   ˆ 𝑀; x

                 bo = pure y ∈ 𝐸ˆ                                       bo = bo′ ≫= ko ∈ 𝐸ˆ
                      ˆ 𝑀; x →
        x = exeBO bo, 𝐸;                                                 ˆ 𝑀; x →
                                                          x = exeBO bo, 𝐸;
                         x = Done y, 𝐸;
                                     ˆ 𝑀; x                      res = exeBO bo′, x = res ≫=◦ ko, 𝐸;
                                                                                                  ˆ 𝑀; x

                      res = Done𝐻 y ∈ 𝐸ˆ                            bo = sexecBO now bo′ ∈ 𝐸ˆ
            x = res ≫=◦ ko; 𝐸;
                             ˆ 𝑀; x →                                         ˆ 𝑀; x →
                                                               x = exeBO bo, 𝐸;
                    bo = ko y, x = exeBO bo, 𝐸;
                                             ˆ 𝑀; x                   x = sexecBO+ now bo′, 𝐸;
                                                                                            ˆ 𝑀; x

                    now = ∅, bo′ = 𝑣ˆ ∈ 𝐸ˆ                                     res = Done y ∈ 𝐸ˆ
      x = sexecBO now bo′, 𝐸;
                    +         ˆ 𝑀; x →                               x = sexecBO◦ res, 𝐸;
                                                                                       ˆ 𝑀; x →
             res = exeBO bo , x = sexecBO◦ res, 𝐸;
                            ′                   ˆ 𝑀; x                                x = Done res, 𝐸;
                                                                                                    ˆ 𝑀; x

                  bo = parBO bo0 bo1 ∈ 𝐸ˆ                               res0 = Done y, res1 = Done z ∈ 𝐸ˆ
                   ˆ 𝑀; x → res0 = exeBO bo0,
    x = exeBO bo, 𝐸;                                                 x = parBO◦ res0 res1 ; 𝐸;
                                                                                             ˆ 𝑀; x →
         res1 = exeBO bo1, x = parBO◦ res0 res1, 𝐸;
                                                 ˆ 𝑀; x                      pr = (y, z), x = Done pr, 𝐸;
                                                                                                       ˆ 𝑀; x

                                      (a) For mutative operational semantics.
                      now = ∅𝐻 , bo = 𝑣¤ ∈ 𝐸¤                               res = Done𝐻 y ∈ 𝐸¤
                              ¤ x →
          x = execBO now bo, 𝐸;                                     x = execBO◦ res, 𝐸;
                                                                                     ¤ x →
                 res = exeBO𝐻 bo, x = execBO◦ res, 𝐸;
                                                   ¤ x                                               ¤ x
                                                                           now = ∅𝐻 , x = (now, y) , 𝐸;
                  bo = pure y ∈ 𝐸¤                                         bo = bo′ ≫= ko ∈ 𝐸¤
                     ¤ x → x = Done𝐻 y, 𝐸;
      x = exeBO𝐻 bo, 𝐸;                 ¤ x                   x = exeBO𝐻 bo, 𝐸;¤ x →
                                                                     res = exeBO𝐻 bo′, x = res ≫=◦ ko, 𝐸;
                                                                                                       ¤ x

                      res = Done𝐻 y ∈ 𝐸¤                            bo = sexecBO now bo′ ∈ 𝐸¤
             x = res ≫=◦ ko; 𝐸;
                              ¤ x →                            x = exeBO𝐻 bo, 𝐸;¤ x →
                                                                                    +
                                               ¤ x
                     bo = ko y, x = exeBO𝐻 bo, 𝐸;                        x = sexecBO𝐻 now bo′, 𝐸;
                                                                                               ¤ x

              now = ∅𝐻 ′ , bo′ = 𝑣¤ ∈ 𝐸¤                                     res = Done𝐻 0 y ∈ 𝐸¤
               +
  x = sexecBO𝐻   now bo′, 𝐸;¤ x →                                       ◦
                                                             x = sexecBO𝐻           ¤
                                                                          ;𝐻 ′ res, 𝐸; x → now = ∅𝐻 ′ /𝐻 0 ,
      res = exeBO∅ bo′, x ′ = sexecBO𝐻 ◦           ¤
                                         ;𝐻 ′ res, 𝐸; x
                                                                                                              ¤ x
                                                                            pr = (now, y), x = Done𝐻 /𝐻 0 pr, 𝐸;

                 bo = parBO bo0 bo1 ∈ 𝐸¤                             res0 = Done𝐻 0 y, res1 = Done𝐻 1 z ∈ 𝐸¤
                    ¤ x → res0 = exeBO∅ bo0,                                 ◦              ¤ x →
   x = exeBO𝐻 bo, 𝐸;                                              x = parBO𝐻    res0 res1 ; 𝐸;
                                     ◦              ¤ x                                                           ¤ x
         res1 = exeBO∅ bo1, x = parBO𝐻   res0 res1, 𝐸;                   pr = (y, z), x = Done𝐻 / (𝐻 0 ·𝐻 1 ) pr, 𝐸;
                                   (b) For denotational operational semantics.
                                      Fig. 37. Basic monadic reduction rules.


   A resource context can contain ghost resources gho to represent various auxiliary information.
The meanings of ghost resources are as follows. A linearity witness linear is used for Linearly. A
                         ι.𝑖;𝑛
live lifetime token now𝐻    ;𝑃 owns the part .𝑖 of the lifetime al ι, asserting that it is alive with the
partial history 𝐻 , has 𝑛 children tokens, and has the right to perform updates of borrow paths
in 𝑃. A dead lifetime token end𝐻   ι asserts that the lifetime al ι has ended with the history 𝐻 . A
                                 δ
borrow lifetime token lifetime𝛼 asserts that the lifetime of the borrow of the id δ is 𝛼. A borrow
                     𝑝¯
path token borrowx;𝑇 ;𝑞¯ asserts that the borrow of the borrow path sequence 𝑝¯ owns an object of
34                                                                                   Yusuke Matsushita and Hiromi Ishii


                      bo = deref ref ∈ 𝐸ˆ                      ref = Ref ℓ ∈ 𝐸ˆ      ℓ ↦→ y ∈ 𝑀
                             ˆ 𝑀; x →
              x = exeBO bo, 𝐸;                               x = deref◦ ref , 𝐸;
                                                                              ˆ 𝑀; x →
                            x = deref◦ ref , 𝐸;
                                             ˆ 𝑀; x                    y ′ = y, x = Done y ′, 𝐸;
                                                                                              ˆ 𝑀; x
           bo = updateRef ko ref ∈ 𝐸ˆ                           ˆ ref = Ref ℓ ∈ 𝐸ˆ
                                                           ko = 𝑣,                       ℓ ↦→ y ∈ 𝑀
                      ˆ 𝑀; x →
       x = exeBO bo, 𝐸;                           x = updateRef+ ko ref , 𝐸;
                                                                          ˆ 𝑀; x → bo = ko y,
            x = updateRef+ ko ref , 𝐸;
                                    ˆ 𝑀; x                 res = execBO bo, x = updateRefℓ• res, 𝐸;
                                                                                                 ˆ 𝑀; x
                res = Done pr ∈ 𝐸ˆ                                     pr = (z, y) ∈ 𝐸ˆ
       x = updateRefℓ• res, 𝐸;
                            ˆ 𝑀; x →                   x = updateRefℓ◦ pr, 𝐸;
                                                                            ˆ 𝑀; x → ref = Ref ℓ,
                  x = updateRefℓ◦ pr, 𝐸;
                                      ˆ 𝑀; x                    pr ′ = (z, ref ), x = Done pr ′, 𝐸;
                                                                                                 ˆ 𝑀 {ℓ ←y}; x

                                    (a) For mutative operational semantics.
                                                                                                  
                                                          ref = 𝐵¤ (Ref y) ∈ 𝐸¤             Mut𝑝.0 𝐵¤ = Mut𝑝¯
                                                                                         𝐵¤ ′ =
                bo = deref ref ∈ 𝐸¤                                                         Share 𝐵¤ = Share
                    ¤ x → x = deref◦ ref , 𝐸;
     x = exeBO𝐻 bo, 𝐸;                     ¤ x                            ¤ x → y ′ = 𝐵¤ ′ y, x = Done𝐻 y ′, 𝐸;
                                                         x = deref◦ ref , 𝐸;                                 ¤ x
                                    𝐻                             𝐻

             bo = updateRef ko ref ∈ 𝐸¤                              ¤ ref = Mut𝑝¯ (Ref y) ∈ 𝐸¤
                                                               ko = 𝑣,
                         ¤ x →                                      +         ¤ x → bo = ko y,
         x = exeBO𝐻 bo, 𝐸;                            x = updateRef𝐻 ko ref , 𝐸;
                              +          ¤ x                                                          ¤ x
                x = updateRef𝐻  ko ref , 𝐸;                    res = exeBO𝐻 bo, x = updateRef𝑝•¯ res, 𝐸;

             res = Done𝐻 pr ∈ 𝐸¤                                            pr = (z, y) ∈ 𝐸¤
                            ¤ x →
      x = updateRef𝑝•¯ res, 𝐸;                               ◦
                                                x = updateRef𝑝;𝐻   ¤             → ref = Mut𝑝¯ (Ref y),
                                                             ¯ pr, 𝐸; x
                               ◦
                x = updateRef𝑝;𝐻
                               ¯
                                     ¤ x
                                 pr, 𝐸;                             ′
                                                                           pr = (z, ref ), x = Done𝐻 /𝑝 ←y pr ′, 𝐸;
                                                                                                                 ¤ x

                                  (b) For denotational operational semantics.
                              Fig. 38. Reference-related monadic reduction rules.



         Lifetime path     𝜌 F ι | 𝜌.𝑖            Extended type 𝑇˚ F 𝑇 | Done𝜌¯ 𝑇 | Skel 𝑇
                                                          𝜌;𝑛ι                                            𝑝¯
          Ghost resource     gho F linear | now𝐻 ;𝑃 | end𝐻     | lifetime𝛼δ | borrowx;𝑇 ;𝑞¯
                                  | mut𝑝¯ | share𝑝¯ | lendδx;𝑇 | depo𝑝¯ | gdepoδx;𝑇 ;𝐻
                                                                      𝑝¯            𝑝¯
                                     | hole𝑝¯ | relend𝐻 | ℓ Z⇒ x | ℓ ↦→ x | skel𝑇x | var𝑇x
                                                            𝑝¯


     Atomic resource     atom F x ::𝑃𝜋 𝑇˚ | δ | x = 𝑡ˆ ∝ 𝑡¤ | x = 𝑣¤ | ℓ ↦→ x | ℓ ↦→
                                                                                   ¤ x | ∀𝑥 . 𝛤˚ | gho
                                     Resource context       ˚ 𝛥˚ F atom
                                                            𝛤,
                                  Fig. 39. Syntax for the association system.



a variable x typed 𝑇 . When 𝑞¯ is non-empty, it means that the object is also reborrowed under 𝑞¯ .
When 𝑞¯ is empty, we omit the last part ‘; 𝑞¯ ’ of the subscript. We have tokens for a mutable borrower
mut𝑝¯ , a shared borrower share𝑝¯ , and a lender lendδ𝑣;x  ˆ . We also have tokens for a (local) deposit
depo𝑝¯ and a global deposit gdepoδx;𝑇 ;𝐻 for the borrowed contents. The hole token hole𝑝¯ is used
                                                                                                                       𝑝¯
inside a global deposit to indicate a hole caused by a deposit depo𝑝¯ . The relender token relend𝐻
asserts that the relender of 𝑝¯ is under the updates of 𝐻 . We also have a shared-borrowed points-to
         𝑝¯                                           𝑝¯
token ℓ Z⇒ x and the evidence of the ownership ℓ ↦→ x. Also, we have a shareable token skel𝑇x for
the skeleton type Skel 𝑇 and a variable token var𝑇x providing skeletons with the witness that the
variable x is typed 𝑇 .
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                                           35


                                      ¤ y ′ = 𝑣ˆ ∝ 𝑣,
                            y = 𝑢ˆ ∝ 𝑢,            ¤ y ′ = 𝑣,    ¤ δ, 𝑀 ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇
                                                           ¤ z = 𝑤,
                                                                                             config-assoc
                   x = 𝑡ˆ, y = 𝑢,   ′
                               ˆ y = 𝑣, ˆ 𝐸; 𝑀; x ∝𝑇 x = 𝑡¤, y = 𝑢,
                                           ˆ                        ¤ y ′ = 𝑣,
                                                                            ¤ z = 𝑤,     ¤ x
                                                                                    ¤ δ, 𝐸;
                            𝛥˚ ≼ 𝛤˚   𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚                              𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇
                                                         assoc-≼                                               assoc-∀
                                 𝛥 ⊢ 𝑡 ∝ 𝑡¤ :: 𝑇˚
                                  ˚  ˆ                                          (∀𝑥 . 𝛤˚ ) ⊢ 𝑡ˆ ∝ 𝑡¤ :: ∀𝑥 . 𝑇

              ∀𝑖. 𝛤˚𝑖 real             ∀𝑖. x ::ω 𝑈˚ , 𝛤˚𝑖 + 𝛥˚ ⊢ 𝑢ˆ𝑖 ∝ 𝑢¤𝑖 :: 𝑈˚𝑖 x ::ω 𝑈˚ , 𝛥˚ ′ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚
                                                                                                                  assoc-var-ω
                                        x = 𝑢ˆ ∝ 𝑢¤ + 𝑖 𝛤𝑖 + ω 𝛥˚ + 𝛥˚ ′ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚
                                                          Í ˚

                                 𝛤˚ ′ real        𝛤˚ + 𝛤˚ ′ ⊢ 𝑢ˆ ∝ 𝑢¤ :: 𝑈˚   x ::𝜋BorPaths 𝛤 𝑈˚ , 𝛥˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚
                                                                                            ˚
               𝛤˚ valid
                                                                                                                      assoc-var
                                             x = 𝑢ˆ ∝ 𝑢¤ + 𝛤˚ ′ + 𝜋 𝛤˚ + 𝛥˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚
       𝛤˚ ghost, gvalid   𝛤,    ¤ x, 𝛥˚ ⊢ x ∝ x :: Ur 𝑇
                           ˚ ℓ ↦→
                                                        assoc-linear                                   linear ⊢ ∅ ∝ ∅ :: Linearly
              ¤ x, 𝛥 ⊢ linear x ∝ linear x :: Ur 𝑇
           ℓ ↦→    ˚
                                                                                                                         𝛼 ≤ al ι
   ¤ x, x ::𝑃1 𝑇 ⊢ Ref ℓ ∝ Ref x :: Ref 𝑇
ℓ ↦→                                                             ι;0
                                                              now𝐻 ;BorPath
                                                                            ⊢ ∅ ∝ ∅𝐻 :: Now al ι                     ι ⊢ ∅ ∝ ∅ :: End𝛼
                                                                                                                  end𝐻         𝐻
                             ∀𝑖. 𝑃 ′ ⊆ 𝑃 𝑖
                                                                                   𝜌;0        ′
                        ′                                                     now𝐻 ;𝑃 , x ::𝑃1 𝑇 ⊢ Done x ∝ Done𝐻 x :: Done𝜌¯ 𝑇
                                Ó
   now𝐻 ;𝑃 , bo ::𝑃1 BO al ⌊𝜌 ⌋ 𝑇 ⊢
        𝜌;0

             exeBO bo ∝ exeBO𝐻 bo :: Done𝜌¯ 𝑇
                                                                                                          𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: Skel 𝑇
                       Ó
                    𝛽 ≤ 𝑖 𝛼𝑖     𝑇 ≼𝑈 𝑈 ≼𝑇                                                      𝛼 ≤ al ι
                    ⌊𝑝 ⌋      𝑝¯
    mut𝑝¯ , lifetime𝛼 , borrowx;𝑇                   ⊢ x ∝ Mut𝑝¯ x :: Mut𝛽 𝑈                   end𝐻 + 𝛤 ⊢ 𝑡 ∝ Mut𝑝¯ 𝑡¤ :: Mut𝛼 𝑇
                                                                                                 ι     ˚ ˆ

                                                                                                                𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: Skel 𝑇
                                       Ó
                               𝛽 ≤        𝑖 𝛼𝑖    𝑇 ≼𝑈                                               𝛼 ≤ al ι
                  ⌊𝑝 ⌋      𝑝¯
share𝑝¯ , lifetime𝛼 , borrowx;𝑇                    ⊢ x ∝ Share x :: Share𝛽 𝑈                      end𝐻 + 𝛤 ⊢ 𝑡 ∝ Share 𝑡¤ :: Share𝛼 𝑇
                                                                                                     ι    ˚   ˆ

                                                                𝛼≤𝛽           𝑇 ≼𝑈
                                    lendδx;𝑇 , δ, lifetime𝛼δ , x = 𝑣ˆ ∝ 𝑣¤      ⊢ 𝑣ˆ ∝ Lendδ x :: Lend𝛽 𝑈

                            𝛤˚ ⊢ x ∝ x :: 𝑇         𝛥˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚                   𝛤˚ ⊢𝐻
                                                                                             δ x :: 𝑇      𝛥˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚
                                 𝑝¯
                  depo𝑝¯ , borrowx;𝑇 + 𝛤˚ + 𝛥˚              ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚          gdepoδx;𝑇 ;𝐻 , 𝛤˚ + 𝛥˚      ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚
            𝑝¯                                                            𝑝¯
        𝛤˚ ⊢𝐻 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚                                        𝛤˚ ⊢𝐻 𝑣¤ ; 𝑤¤                                            𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚
                     𝑝¯                                          ¯
                                                                 𝑝                        𝑝¯                                   𝑝¯
   x = 𝑡ˆ ∝ 𝑡¤ + 𝛤˚ ⊢𝐻         x :: 𝑇˚            hole𝑝¯ , borrowx;𝑇 ;𝑞¯ , x = 𝑣ˆ ∝ 𝑤,
                                                                                    ¤ 𝛤˚ ⊢𝐻 𝑣ˆ ∝ 𝑣¤ :: 𝑇                   𝛤 ⊢∅ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚
                                                                                                                           ˚

                                    𝑝.0                                                                                        𝑝.0
                                𝛤˚ ⊢𝐻 y :: 𝑇                                       ∀𝑖. 𝑝 𝑖 ∉ dom 𝐻              𝐻 ≠∅       𝛤˚ ⊢𝐻 x :: 𝑇
                   𝑝¯             𝑝¯                                                              𝑝¯       𝑝¯
        ¤ y, ℓ ↦→ y, 𝛤˚ ⊢𝑝←y,𝐻 Ref ℓ ∝ Ref x :: Ref 𝑇
     ℓ ↦→                                                                            ¤ x, ℓ ↦→ x, 𝛤˚ ⊢𝐻 Ref ℓ ∝ Ref x :: Ref 𝑇
                                                                                  ℓ ↦→

                                                     Fig. 40. Selected association rules.


   Assocaition rules. Selected rules for the association judgment are shown in Fig. 40.36 Appendix B.2
presents the omitted rules and formal definitions.
   The association relation over mutative and denotational configurations is 𝐺ˆ ∝𝑇 𝐺.   ¤ Its only rule
is config-assoc, which puts into the resource context the variable-term bindings, the borrow ids
of the environments, and the points-to tokens of the memory, discarding some old variables.
   The association judgment has the form 𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚ . The association judgment is closed under
resource context inclusion (assoc-≼), defined naturally similarly to the typing context inclusion
36 We define ⌊𝜌 ⌋ by ⌊ι.𝑖 ⌋ ≜ ι and ⌊𝑝 ⌋ by ⌊δ.𝑖 ⌋ ≜ δ.
36                                                                                            Yusuke Matsushita and Hiromi Ishii


Fig. 26. For polymorphic types, we use polymorphic resource contexts (assoc-∀). For variable
introduction, we use the condition 𝛤˚ real, meaning that every item in 𝛤˚ is of the form x = 𝑡ˆ ∝ 𝑡¤ or
ℓ ↦→ x.
    Unlike the unrestricted case (assoc-var-ω), introduction of a possibly linear variable (assoc-var)
is tricky, because the set of accessible borrow paths should be determined from the resource context
𝛤˚ , where we define BorPaths 𝛤˚ as the set of the subpaths of the borrow path of each mutable
borrower owned by 𝛤˚ . For this purpose, we introduce the validity side condition 𝛤˚ valid. For
example, it ensures that 𝛤˚ is free of a linear variable-type binding x ::𝑃1 𝑇 and of overlapping live
lifetime tokens. Also, to handle nested borrowing properly (which is much trickier than it might
look), the validity ensures that 𝛤˚ owns all the mutably borrowed objects accessible by 𝛤˚ .
    The key is the rule assoc-linear for linear, an intermediate state of linearly. Here, we can
capture some fragment 𝑀 of the memory and an arbitrary ghost resource context 𝛤˚ ,37 under the
global validity side condition 𝛤˚ gvalid, stronger than the usual validity valid. For example, the
global validity ensures that 𝛤˚ contains a borrowed object for each lender in 𝛤˚ . The association rule
for linear itself (shown next) is straightforward.
    A linearity token Linearly captures linear, a reference Ref 𝑇 captures a points-to token ℓ ↦→ x
and a body, and live and dead lifetime tokens Now𝛼 , End𝛼 capture now and end of the observed
history 𝐻 . The type Done𝜌¯ 𝑇 also captures now of the lifetime paths 𝜌.         ¯ A mutable borrower is
usually obtained from the token mut𝑝¯ accompanied with some shared information. A shared
borrower is similarly obtained using share𝑝¯ . Also, borrowers whose lifetime has ended can be
obtained through a skeleton Skel 𝑇 . A lender is obtained simply from the token lendδx;𝑇 .
    The content of a deposit depo𝑝¯ , gdepoδx;𝑇 ;𝐻 is owned by some variable. The tricky point is
which variable should own each deposit. We carefully design the validity condition (assoc-var)
so that the borrower or the lender with a sufficient lifetime token should own the deposit, so that
nested borrowers work properly in the presence of parBO. For deposits, we introduce an auxiliary
                𝑝¯
judgment 𝛤˚ ⊢𝐻 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚ , asserting that the object 𝑡ˆ ∝ 𝑡¤ deposited at 𝑝¯ becomes an object of type
                                                                                       𝑝¯
𝑇˚ after the updates of 𝐻 . Its rules are defined using an auxiliary judgment 𝛤˚ ⊢𝐻 𝑡¤ ; 𝑢,    ¤ meaning
that a term 𝑡¤ at 𝑝¯ turns into 𝑢¤ after the updates of 𝐻 .

B.2     Details
Here we present more details of the association system.

   Basics. The subtyping over extended types 𝑇˚ ≼ 𝑇˚ ′ extends the usual subtyping 𝑇 ≼ 𝑇 by the
following rules:
                                        𝑇 ≼𝑈                                𝑇 ≼𝑈
                                  Done𝛼 𝑇 ≼ Done𝛼 𝑈                    Skel 𝑇 ≼ Skel 𝑈
    We say an atomic resource atom is shareable and write atom shareable if atom is of the form
                                                          𝑝¯                𝑝¯
x ::𝑃ω 𝑇˚ , x = 𝑣ˆ ∝ 𝑣,
                     ¤ x = 𝑣,
                           ¤ δ, endι , lifetime𝛼δ , borrow
                                    𝐻                        , share𝑝¯ , ℓ Z⇒ x, or skelx .
                                                                    x;𝑇 ;𝑞¯                                   𝑇
     The resource context inclusion 𝛤˚ ≼ 𝛥˚ is inductively defined by the following rules:
                                        𝛤˚ ≼ 𝛤˚ ′    𝛤˚ ′ ≼ 𝛤˚ ′′                𝜇≤𝜋          𝑇 ≼𝑈
                        𝛤˚ ≼ 𝛤˚
                                               𝛤˚ ≼ 𝛤˚ ′′                     x ::𝑃𝜋 𝑇 , 𝛤˚ ≼ x ::𝑃𝜇 𝑈 , 𝛤˚

          atom shareable                                                      𝑎 is fresh in 𝛥˚ and 𝛥˚ ′     𝛥˚ ′ ≼ 𝛤,
                                                                                                                   ˚ 𝛥˚
                                   (∀𝑥 . 𝛤˚ ), 𝛥˚ ≼ 𝛤˚ [𝑎/𝑥], 𝛥˚
           atom, 𝛤˚ ≼ 𝛤˚                                                                  ˚ ′
                                                                                          𝛥 ≼ (∀𝑥 . 𝛤 ), 𝛥
                                                                                                        ˚ ˚

37 The condition 𝛤˚ ghost means that 𝛤˚ consists only of ghost resources gho after unfolding polymorphism.
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                                        37


  The multiplication 𝜋 𝛤˚ over a resource context is defined as follows:
                                      1 𝛤˚ ≜ 𝛤˚            𝜋 (x ::𝜇 𝑇 , 𝛤˚ ) ≜ x ::𝜋 ·𝜇 𝑇 , 𝜋 𝛤˚
                                                                        atom shareable
                 𝜋 ((∀𝑥 . 𝛤˚ ), 𝛥)
                                ˚ ≜ (∀𝑥 . 𝜋 𝛤˚ ), 𝜋 𝛥˚                                                         𝜋∅ ≜ ∅
                                                                 𝜋 (atom, 𝛤˚ ) ≜ atom, 𝜋 𝛤˚

  The addition 𝛤˚ + 𝛥˚ of resource contexts is defined as follows:
                 atom shareable                                          ¬ atom shareable
                                                                                                                           ∅ + 𝛥˚ ≜ 𝛥˚
    (atom, 𝛤 ) + (atom, 𝛥)
           ˚            ˚ ≜ atom, ( 𝛤˚ + 𝛥)
                                         ˚                       (atom, 𝛤˚ ) + 𝛥˚ ≜ atom, ( 𝛤˚ + 𝛥)
                                                                                                 ˚

  The predicate 𝛤˚ ghost is inductively defined by the following rules:
                                                                      ˚ 𝛥˚ ghost
                                                                     𝛤,
                                            gho ghost
                                                                   (∀𝑥 . 𝛤˚ ), 𝛥˚ ghost

  On histories. The set of borrow paths BorPaths 𝛤˚ for a resource context 𝛤˚ is inductively defined
by the following rules:
                                     mut𝑝¯ 𝑇 ∈ 𝛤˚                     𝑝 ∈ BorPaths ( 𝛤,
                                                                                     ˚ 𝛥)˚
                                  𝑝 𝑖 .𝑗 ∈ BorPaths 𝛤˚             𝑝 ∈ BorPaths ((∀𝑥 . 𝛤˚ ), 𝛥)
                                                                                             ˚

  The predicate Now𝜌 𝛤˚ ; 𝐻 , extracting the history 𝐻 for the lifetime path 𝜌 from the resource
context 𝛤˚ is inductively defined by the following rules:
                                                                                                                                ⌊𝜌 ⌋.𝑖;𝑛
           ∀𝑖 < 𝑛. Now𝜌.𝑖 𝛤˚𝑖 ; 𝐻 𝑖′                       Now𝜌 𝛤˚ ; 𝐻            atom is not of the form now𝐻 ′ ;𝑃

        Now𝜌 (now𝐻 ;𝑃 , 𝛤˚ ) ; 𝐻 / 𝑖 𝐻 𝑖′
                   𝜌;𝑛            Î                                           Now𝜌 (atom, 𝛤˚ ) ; 𝐻

Importantly, the predicate is right-unique (i.e., unique in the history 𝐻 ). We also use the shorthand
Now𝜌 𝛤˚ for ∃𝐻 . Now𝜌 𝛤˚ .
  The restriction 𝐻 |𝑝 of a history 𝐻 with respect to a borrow path 𝑝 is defined as follows:
                                                                  𝑞 is not of the form 𝑝.𝑖
                  (𝑝.𝑖 ←x, 𝐻 ) |𝑝 ≜ 𝑝.𝑖 ←x, (𝐻 |𝑝 )                                                           ∅|𝑝 ≜ ∅
                                                                   (𝑞 ←x, 𝐻 ) |𝑝 ≜ 𝐻 |𝑝

   Validity. The validity 𝛤˚ valid of a resource context is defined as the negation of the invalidity
𝛤˚ invalid, inductively defined by the following rules:
                                𝑥 is fresh in 𝛥˚         ˚ 𝛥˚ invalid
                                                        𝛤,
                                                                                 x ::𝑃1 𝑇 , 𝛤˚ invalid
                                        (∀𝑥 . 𝛤˚ ), 𝛥˚ invalid
        dom 𝐻 ⊈ 𝑃                                     𝑃′ ⊈ 𝑃                                     𝑖 ≠ 𝑖′       𝑃 ∩ 𝑃′ ≠ ∅
         𝜌;𝑛
     now , 𝛤˚ invalid                       𝜌;𝑛          𝜌.𝑖;𝑚                               𝜌.𝑖.𝑗;𝑛           𝜌.𝑖 ′ .𝑗 ′ ;𝑚
          𝐻 ;𝑃                        now𝐻 ;𝑃 , now𝐻 ′ ;𝑃 ′ , 𝛤˚ invalid                now𝐻 ;𝑃 , now𝐻 ′ ;𝑃 ′                  , 𝛤˚ invalid
                                    𝜌;𝑛       ⌊𝜌 ⌋                           ι      ι
                              now𝐻 ;𝑃 , end𝐻 ′ , 𝛤˚ invalid               end𝐻 , end𝐻 ′ , 𝛤 invalid
                                                                                          ˚
                                                                                 𝑝¯                𝑝¯
                     lifetime𝛼δ , lifetimeδ𝛽 , 𝛤˚ invalid             borrowx;𝑇 , borrowy;𝑈 , 𝛤˚ invalid

         mut𝑝¯ , mut𝑝¯ , 𝛤˚ invalid            mut𝑝¯ , share𝑝¯ , 𝛤˚ invalid               lendδx;𝑇 , lendδy;𝑈 , 𝛤˚ invalid

    depo𝑝¯ , depo𝑝¯ , 𝛤˚ invalid           gdepoδx;𝑇 ;𝐻 , gdepoδy;𝑈 ;𝐻 ′ , 𝛤˚ invalid                   hole𝑝¯ , hole𝑝¯ , 𝛤˚ invalid

          𝛼 ≤ al ι        Nowδ 𝛤˚ ; 𝐻 ′           𝐻 ≠ 𝐻 ′ |δ                          𝛼 ≤ al ι          𝐻 ≠ 𝐻 ′ |δ
             gdepoδx;𝑇 ;𝐻 , lifetime𝛼δ , 𝛤˚ invalid                                                  ι , 𝛤˚ invalid
                                                                      gdepoδx;𝑇 ;𝐻 , lifetime𝛼δ , end𝐻 ′
38                                                                                                          Yusuke Matsushita and Hiromi Ishii


           𝛼 ≤ al ι     Nowδ 𝛤˚ ; 𝐻 ′                𝐻 |𝑝𝑖 ≠ 𝐻 ′ |𝑝𝑖                            𝛼 ≤ al ι             𝐻 |𝑝𝑖 ≠ 𝐻 ′ |𝑝𝑖
                     𝑝¯          ⌊𝑝 ⌋                                                      𝑝¯          ⌊𝑝 ⌋
               relend𝐻 , lifetime𝛼 𝑖 , 𝛤˚ invalid                                                               ι , 𝛤˚ invalid
                                                                                     relend𝐻 , lifetime𝛼 𝑖 , end𝐻 ′

                                      Ó                Ó
                                         𝑗 al ⌊𝜌 𝑗 ⌋ ≤  𝑖 𝛼𝑖                              depo𝑝¯ ∉ 𝛤˚
                                                                 𝑝¯                ⌊𝑝 ⌋        𝜌;𝑛
                                           mut𝑝¯ , borrowx;𝑇 , lifetime𝛼 , now𝐻 ;𝑃 , 𝛤˚ invalid

             𝛼 ≤ al ι        ∀𝐻 . gdepoδx;𝑇 ;𝐻 ∉ 𝛤˚                         𝛼 ≤ al ι            Nowδ 𝛤˚               ∀𝐻 . gdepoδx;𝑇 ;𝐻 ∉ 𝛤˚
                                      ι , 𝛤˚ invalid
           lendδx;𝑇 , lifetime𝛼δ , end𝐻                                                    lendδx;𝑇 , lifetime𝛼δ , 𝛤˚ invalid
                                        ′


            𝛼 ≤ al ι     ⌊𝑝⌋ = δ       ¯
                                   depo𝑞,𝑝 ∉ 𝛤˚                                           𝛼 ≤ al ι       Nowδ 𝛤˚            ⌊𝑝⌋ = δ              depo𝑞,𝑝¯
                                                                                                                                                           ∉ 𝛤˚
                                        ¯
                                       𝑞,𝑝                                                                                             ¯
                                                                                                                                       𝑞,𝑝
                                            ′ , 𝛤 invalid                                                                                        ′ , 𝛤 invalid
lendδx;𝑇             δ      ι
           , lifetime𝛼 , end ′ , borrow         ˚                                          lendδx;𝑇 , lifetime𝛼δ , borrowx;𝑇 ;𝑞¯                     ˚
                                  𝐻                  x;𝑇 ;𝑞¯

   The global validity 𝛤˚ gvalid of a resource context is defined as the negation of the global invalidity
𝛤˚ ginvalid, inductively defined by the following rules:
                                                                                                                              ¬ Now ⌊𝜌 ⌋ 𝛤˚
                                                                                                         𝜌;𝑛
             𝑥 is fresh in 𝛥˚       ˚ 𝛥˚ ginvalid
                                    𝛤,                                   𝛤˚ invalid                  now𝐻 ′ ;𝑃 ∈ 𝛤˚
                    (∀𝑥 . 𝛤˚ ), 𝛥˚ ginvalid                             𝛤˚ ginvalid                              𝛤˚ ginvalid
                                                                                                                       𝑝¯
                        depo𝑝¯ ∉ 𝛤˚                                      hole𝑝¯ ∉ 𝛤˚                                 ℓ ↦→ x ∉ 𝛤˚
                         𝑝¯                                                                                     𝑝¯
                   borrow     , 𝛤˚ ginvalid
                                 x;𝑇 ;𝑞¯                              depo𝑝¯ , 𝛤˚ ginvalid                 ℓ Z⇒ x, 𝛤˚ ginvalid
                                                                                                         ⌊𝑝 ⌋
 ∀𝐻 . gdepoδx;𝑇 ;𝐻 ∉ 𝛤˚                           lendδx;𝑇 ∉ 𝛤˚                           ∀x,𝑇 . lendx;𝑇𝑖 ∉ 𝛤˚                         var𝑇x ∉ 𝛤˚
 lendδx;𝑇 , 𝛤˚ ginvalid                     gdepoδx;𝑇 ;𝐻 , 𝛤˚ ginvalid                     depo𝑝¯ , 𝛤˚ ginvalid                    skelx , 𝛤˚ ginvalid
                                                                                                                                             𝑇

   Association rules. The omitted rules for the association judgment 𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚ are as follows.
                                                   ¯
Here, we introduce an auxiliary judgment 𝑎 ∝:: 𝑇˚ ; 𝑈˚ for operators and monad constructors 𝑎. Also,
                     ˚ 𝛥˚ with the following side condition: for every item of the form x ::𝜋 𝑇˚ in 𝛤˚ , x
we write 𝛤˚ p 𝛥˚ for 𝛤,
            ˚
is fresh in 𝛥.
                                                                  x ::𝜋 𝑇˚ ⊢ x ∝ x :: 𝑇˚

  ∀𝑖. 𝛤˚𝑖 ⊢ 𝑡𝑖 ∝ 𝑡𝑖 :: 𝑇𝑖 y ::1 𝑇𝑖 p 𝛥˚ ⊢ 𝑢 ∝ 𝑢 :: 𝑈                         ∀𝑖. y ::ω 𝑇𝑖 , 𝛤˚ ⊢ 𝑡𝑖 ∝ 𝑡𝑖 :: 𝑇𝑖 y ::ω 𝑇𝑖 p 𝛥˚ ⊢ 𝑢 ∝ 𝑢 :: 𝑈
   𝑖 𝛤𝑖 + 𝛥 ⊢ let y = 𝑡 in 𝑢 ∝ let y = 𝑡 in 𝑢 :: 𝑈                               ω 𝛤 + 𝛥 ⊢ let y = 𝑡 in 𝑢 ∝ let y = 𝑡 in 𝑢 :: 𝑈
 Í ˚       ˚                                                                        ˚     ˚

     x ::𝜋 𝑇 , 𝛤˚ ⊢ 𝑡 ∝ 𝑡 :: 𝑈                         𝛤˚ ⊢ 𝑡 ∝ 𝑡 :: 𝑇 →𝜋 𝑈 𝛥˚ ⊢ 𝑢 ∝ 𝑢 :: 𝑇                             x ∈ dom 𝛤˚ 𝛤˚ ⊢ 𝑡 ∝ 𝑡 :: 𝑇
𝛤 ⊢ λ x→ 𝑡 ∝ λ x→ 𝑡 :: 𝑇 →𝜋 𝑈
˚                                                             𝛤˚ + 𝜋 𝛥˚ ⊢ 𝑡 𝑢 ∝ 𝑡 𝑢 :: 𝑈                                𝛤˚ ⊢ seq x 𝑡 ∝ seq x 𝑡 :: 𝑇

                                            ∀𝑖. 𝛤˚𝑖 ⊢ 𝑡𝑖 ∝ 𝑡𝑖 :: 𝑇 𝑗,𝑖 [𝑈/𝑋 ]        data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                 ⊢ 𝑛:: Int                                       Í
                                                                    𝑖 𝜋 𝑗,𝑖 𝛤𝑖 ⊢ C 𝑗 𝑡¯ ∝ C 𝑗 𝑡¯ :: F 𝑈
                                                                             ˚                        ¯

            𝛤˚ ⊢ 𝑡 ∝ 𝑡 :: F 𝑈¯             ∀ 𝑗 . x ::𝜋 𝑗 𝑇 𝑗 [𝑈/𝑋 ] p 𝛥˚ ⊢ 𝑢 𝑗 :: 𝑈 ′          data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                                 𝛤˚ + 𝛥˚ ⊢ case 𝑡 of { C x̄→ 𝑢 } ∝ case 𝑡 of { C x̄→ 𝑢 } :: 𝑈 ′

     𝛤˚ ⊢ 𝑡 ∝ 𝑡 :: 𝐵𝛼 (F 𝑈¯ )              ∀ 𝑗 . x ::𝜋 𝑗 𝐵𝛼 (𝑇 𝑗 [𝑈/𝑋 ]) p 𝛥˚ ⊢ 𝑢 𝑗 :: 𝑈 ′             data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                                 𝛤˚ + 𝛥˚ ⊢ case 𝑡 of { C x̄→ 𝑢 } ∝ case 𝑡 of { C x̄→ 𝑢 } :: 𝑈 ′
     𝑎 ∝ :: 𝑇¯ ; 𝑈    ∀𝑖. 𝛤˚𝑖 ⊢ 𝑡𝑖 ∝ 𝑡𝑖 :: 𝑇𝑖
            Í ˚                                                iop ∝ :: Int; Int          irel ∝ :: Int; Bool               par ∝ :: 𝑇 , 𝑈 ; (𝑇 , 𝑈 )
               𝑖 𝛤𝑖 ⊢ 𝑎 𝑡¯ ∝ 𝑎 𝑡¯ :: 𝑈
 𝑇 is Linearly, Now𝛼 or Mut𝛼 𝑈                          𝑇 is Int, End𝛼 or Share𝛼 𝑈
                                                                                                        linearly ∝ :: Linearly ⊸ Ur 𝑇 ; Ur 𝑇
        consume ∝ :: 𝑇 ; ()                                  move ∝ :: 𝑇 ; Ur 𝑇
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                                                   39

       𝑇 is Linearly, Ref 𝑈 , Now𝛼 or Mut𝛼 𝑈
                                                                           newRef ∝ :: 𝑇 ; Ref 𝑇                freeRef ∝ :: Ref 𝑇 ; 𝑇
         withLinearly ∝ :: 𝑇 ; (Linearly, 𝑇 )
                                                                                                   𝛼 ≤ al ι
                   newLifetime ∝ :: (∀ι. Now al ι ⊸ 𝑇 ); 𝑇
                                                                                         endLifetime ∝ :: Now al ι ; End𝛼
                            𝛼 ≤𝛽 𝑇 ≼𝑈                                                                  𝑇 ≼𝑈
              borrow ∝ :: Linearly, 𝑇 ; (Mut𝛼 𝑇 , Lend𝛽 𝑈 )                               share ∝ :: Mut𝛼 𝑇 ; Ur (Share𝛼 𝑈 )
                         𝑇 is Int, End𝛽 or Share𝛽 𝑈     𝑇 ≼ 𝑇′                             𝑇 is Int, End𝛽 or Share𝛽 𝑈
                                  copy ∝ :: Mut 𝑇 ; 𝑇
                                               𝛼      ′                                       copy ∝ :: Share𝛼 𝑇 ; 𝑇
                           𝛼′ ≤ 𝛼 ∧ 𝛽                                                        𝛼′ ≤ 𝛼 ∧ 𝛽 𝑇 ≼ 𝑈
                                               ′                                                                         ′
              joinMut ∝ :: Mut𝛼 (Mut𝛽 𝑇 ); Mut𝛼 𝑇                                   joinMut ∝ :: Share𝛼 (Mut𝛽 𝑇 ); Share𝛼 𝑈
                       reclaim :: Lend𝛼 𝑇 , End𝛼 ; 𝑇                      execBO ∝ :: Now𝛼 , BO𝛼 𝑇 ; (Now𝛼 ,𝑇 )
                               pure ∝ :: 𝑇 ; BO𝛼 𝑇                     (≫=) ∝ :: BO𝛼 𝑇 , 𝑇 ⊸ BO𝛼 𝑈 ; BO𝛼 𝑈

        sexecBO ∝ :: Now𝛼 , BO𝛼∧𝛽 𝑈 ; BO𝛽 (Now𝛼 , 𝑈 )                                    parBO ∝ :: BO𝛼 𝑇 , BO𝛼 𝑈 ; BO𝛼 (𝑇 , 𝑈 )
                    𝛽 ≤𝛼                                                                                 𝛽 ≤𝛼
     deref ∝ :: 𝐵𝛼 (Ref 𝑇 ); BO𝛽 (𝐵𝛼 𝑇 )                         updateRef ∝ :: 𝑇 ⊸ BO𝛽 (𝑈 ,𝑇 ), Mut𝛼 (Ref 𝑇 );
                                                                                                  BO𝛽 (𝑈 , Mut𝛼 (Ref 𝑇 ))
                                                                                                𝛼 ≤ al ⌊𝜌⌋
         execBO◦ ∝ :: Done𝜌 𝑇 ; (Now al ⌊𝛼 ⌋ , 𝑇 )
                                                                                (≫=◦ ) ∝ :: Done𝜌 𝑇 , 𝑇 ⊸ BO al ⌊𝜌 ⌋ 𝑈 ; BO𝛼 𝑈
                                                                     ∀𝑖. 𝑃 ′ ⊆ 𝑃 𝑖
        𝜌;0               ′′              ′         Ó
                                                        al ⌊𝜌 ⌋ ∧𝛼 𝑇                               + now bo :: Done𝜌¯ 𝑇
   now𝐻 ;𝑃 , now ::𝑃1 Now𝛼 , bo ::𝑃1 BO                                 ⊢ sexecBO+ now bo ∝ sexecBO𝐻
                                𝜌 ′ ;1         ′′                ′
         now𝐻 ;𝑃 , now𝐻 ′ ;𝑃 ′ , res ::𝑃1 Done𝜌.0,𝜌 .0 𝑇 ⊢ sexecBO◦ res ∝ sexecBO𝐻,𝐻
                                                                                 ◦
                 𝜌;1                                                                              𝜌¯
                                                                                     ′ res :: Done 𝑇

                                                                 ∀𝑖. 𝑃 ′, 𝑃 ′′ ⊆ 𝑃 𝑖
                                𝜌;2       𝑃′             𝜌.0,𝜌 ′.0                  ′′               ′
                         now𝐻 ;𝑃 , res0 ::1 Done     𝑇 , res1 ::𝑃1 Done𝜌.1,𝜌 .1 𝑈 ⊢
                                                 ◦                     ◦
                                            parBO res0 res1 ∝ parBO𝐻     res0 res1 :: Done𝜌¯ (𝑇 , 𝑈 )
                                                      Ó
                                                         al ⌊𝜌⌋ ≤ 𝛼
                               𝜌;0        ′                                 ◦ ref :: Done𝜌¯ (𝐵 𝛼 𝑇 )
                         now𝐻 ;𝑃 , ref ::𝑃1 𝐵𝛼 (Ref 𝑇 ) ⊢ deref◦ ref ∝ deref𝐻
                                                         Ó
                                                           al ⌊𝜌⌋ ≤ 𝛼
                                   ′′                                           ′
              now𝐻 ;𝑃 , ko ::𝑃1 𝑇 ⊸ BO al ⌊𝜌 ⌋ (𝑈 ,𝑇 ), ref ::𝑃1 Mut𝛼 (Ref 𝑇 ) ⊢
                   𝜌;0

                                 updateRef+ ko ref ∝ updateRef𝐻       +
                                                                        ko ref :: Done𝜌¯ (𝑈 , Mut𝛼 (Ref 𝑇 ))

                                                                 ∀𝑖. 𝑇𝑖′ ≼ Ref 𝑇      ∀𝑖. Ref 𝑇 ≼ 𝑇𝑖′
                     Ó                                                                              
                ∀𝑖.      al ⌊𝜌⌋ ≤ 𝛼 𝑖      ∀𝑖. 𝛽 ≤ 𝛼 𝑖
                                                                           ⌊𝑝 ⌋                 𝑝¯
    x = Ref ℓ ∝ Ref y, ℓ ↦→ y, mut𝑝¯ , depo𝑝¯ , lifetime𝛼 , borrowx;𝑇 , res ::𝑃1 Done𝜌¯ (𝑈 ,𝑇 ) ⊢
                                            updateRefℓ• res ∝ updateRef𝑝•¯ res :: Done𝜌¯ (𝑈 , Mut𝛽 (Ref 𝑇 ))

                                                           ∀𝑖. 𝑇𝑖′ ≼ Ref 𝑇        ∀𝑖. Ref 𝑇 ≼ 𝑇𝑖′
                  Ó                                                                            
              ∀𝑖.    al ⌊𝜌⌋ ≤ 𝛼 𝑖        ∀𝑖. 𝛽 ≤ 𝛼 𝑖
                                                                         ⌊𝑝 ⌋              𝑝¯            𝜌;0      ′
   x = Ref ℓ ∝ Ref y, ℓ ↦→ y, mut𝑝¯ , depo𝑝¯ , lifetime𝛼 , borrowx;𝑇 , now𝐻 ;𝑃 , res ::𝑃1 (𝑈 ,𝑇 ) ⊢
                                               updateRefℓ◦ pr ∝ updateRef𝑝;𝐻
                                                                         ◦                 𝜌¯       𝛽
                                                                         ¯ pr :: Done (𝑈 , Mut (Ref 𝑇 ))
40                                                                                                           Yusuke Matsushita and Hiromi Ishii

                     Ó                                                                                       Ó
              𝛽 ≤        𝑖 𝛼𝑖      𝑇 ≼𝑈             𝑈 ≼𝑇                                               𝛽 ≤      𝑖 𝛼𝑖         𝑇 ≼𝑈
                 ⌊𝑝 ⌋      𝑝¯                                                                      ⌊𝑝 ⌋      𝑝¯
 mut𝑝¯ , lifetime𝛼 , borrowx;𝑇 , x = 𝑣ˆ ∝ 𝑣¤              ⊢                      share𝑝¯ , lifetime𝛼 , borrowx;𝑇 , x = 𝑣ˆ ∝ 𝑣¤              ⊢
                                  𝑝¯
                                         𝑣ˆ ∝ Mut 𝑣¤ :: Mut𝛽 𝑈                                                         𝑣ˆ ∝ Share 𝑣¤ :: Share𝛽 𝑈

                   ∀𝑖. 𝛤˚𝑖 ⊢ x 𝑖 ∝ Share x 𝑖 :: Share𝛼 (𝑇 𝑗,𝑖 [𝑈/𝑋 ])      data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                                     Í
                                       𝑖 𝜋 𝑗,𝑖 𝛤𝑖 ⊢ C 𝑗 x̄ ∝ Share C 𝑗 x̄ :: Share (F 𝑈 )
                                                ˚                                 𝛼   ¯

                                                           𝛤˚ ⊢ x ∝ Share x :: Share𝛼 𝑇
                                            𝑝¯
                                          ℓ Z⇒ x + 𝛤˚ ⊢ Ref ℓ ∝ Share (Ref x) :: Share𝛼 (Ref 𝑇 )
      x ::𝑃𝜋 𝑇 , 𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚                                     𝑇 ≼𝑈                                                 𝑇 ≼𝑈
 varx       , x ::𝑃𝜋 𝑇 , 𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚                  skel𝑇x    ⊢ x ∝ x :: Skel 𝑈               skel𝑇x , x = 𝑣ˆ ∝ 𝑣¤    ⊢ 𝑣ˆ ∝ 𝑣¤ :: Skel 𝑈
     ∀𝑥 .𝑇

                                x ::𝑃ω 𝑇 ⊢ x ∝ x :: Skel 𝑇                  x ::𝑃ω 𝑇 , x = 𝑣ˆ ∝ 𝑣¤ ⊢ 𝑣ˆ ∝ 𝑣¤ :: Skel 𝑇

      𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: ∀𝑥 . Skel 𝑇                   ∀𝑖. 𝛤˚𝑖 ⊢ x 𝑖 ∝ x 𝑖 :: Skel (𝑇 𝑗,𝑖 [𝑈/𝑋 ])       data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
     𝛤 ⊢ 𝑡ˆ ∝ 𝑡¤ :: Skel (∀𝑥 . 𝑇 )
                                                                          Í
                                                                            𝑖 𝜋 𝑗,𝑖 𝛤𝑖 ⊢ C 𝑗 x̄ ∝ C 𝑗 x̄ :: Skel (F 𝑈 )
     ˚                                                                               ˚                              ¯
                                     𝑇 is 𝑈 →𝜋 𝑈 ′ , Linearly, Ref 𝑈 , Now𝛼 , Lend𝛼 𝑈 , or BO𝛼 𝑈
                                                           ⊢ 𝑣ˆ ∝ 𝑣¤ :: Skel 𝑇
                                    𝛤 ⊢ 𝑣ˆ ∝ 𝑣¤ :: Skel 𝑇
                                    ˚                                          𝛤˚ ⊢ 𝑣ˆ ∝ 𝑣¤ :: Skel 𝑇
                         𝛤˚ ⊢ 𝑣ˆ ∝ Mut𝑝¯ 𝑣¤ :: Skel (Mut𝛼 𝑇 )                    𝛤˚ ⊢ 𝑣ˆ ∝ Share 𝑣¤ :: Skel (Share𝛼 𝑇 )
                                                                    ¯ 𝑝¯
                                                                    𝑞,
                                                    𝑞¯ ≠ ∅      𝛤˚ ⊢𝐻 x :: 𝑇         𝛥˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚
                                                        𝑝¯              ¯ 𝑝¯
                                                                        𝑞,
                                         depo𝑝¯ , borrowx;𝑇 ;𝑞¯ + relend𝐻 + 𝛤˚ + 𝛥˚                ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚
                                                              𝑝¯                                                       𝑝.0
                    𝑝¯                                    𝛤˚ ⊢𝐻 𝑣¤ ; 𝑤¤                                         𝛤˚ ⊢𝐻 y ; z
          x = 𝑣¤   ⊢∅    𝑡¤ ; 𝑡¤
                                                                                                                  𝐵¤̄ (Ref x) ; 𝐵¤̄ (Ref z)
                                                                          𝑝¯                            𝑝¯
                                             x = 𝑣¤ + y = 𝑤¤ + 𝛤˚        ⊢𝐻    x ;y               𝛤˚   ⊢𝑝←y,𝐻
                                                       𝑝.0                                                             𝑝.𝑖
                    ∀𝑖. 𝑝 𝑖 ∉ dom 𝐻     𝐻 ≠ ∅ 𝛤˚ ⊢𝐻 x ; y                                  𝐻 ≠∅           ∀𝑖. 𝛤˚ ⊢𝐻 x 𝑖 ; y 𝑖
                            𝛤˚ ⊢ 𝐵¤̄ (Ref x) ; 𝐵¤̄ (Ref y)                                             ¤̄
                                                                                                 𝛤˚ ⊢ 𝐵 (C x̄) ; 𝐵¤̄ (C ȳ)
                                𝑝¯                                                                   ¯
                                                                                                     𝑝
                                     𝐻                                                                 𝐻
                                                     𝑝¯                                                    𝑝¯
                                𝛥˚ ≼ 𝛤˚          𝛤˚ ⊢𝐻 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚           𝑥 is fresh in 𝛤˚        𝛤˚ ⊢𝐻 𝑡ˆ ∝ 𝑡¤ :: 𝑇
                                          𝑝¯                                              𝑝¯
                                      𝛥˚ ⊢𝐻 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚                             𝛤˚ ⊢𝐻 𝑡ˆ ∝ 𝑡¤ :: ∀𝑥 . 𝑇

                                                                              data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                                               𝑝.𝑖
                         𝐻 ≠∅         ∀𝑖. 𝛤˚𝑖 ⊢𝐻 𝑖 x 𝑖 ∝ x 𝑖 :: 𝑇 𝑗,𝑖 [𝑈/𝑋 ]
                                                       Í ˚ 𝑝¯
                                                        𝑖 𝛤𝑖 ⊢𝐻 C 𝑗 x̄ ∝ C 𝑗 x̄ :: F 𝑈
                                                                                     ¯
                                                 Ó                                    𝑝¯
                                            𝛽 ≤ 𝑖 𝛼𝑖        𝑇 ≼𝑈          𝑈 ≼𝑇    𝛤˚ ⊢𝐻 𝑣¤ ; 𝑤¤
                                                   ⌊𝑞 ⌋           𝑞¯                        𝑝¯
                          mut𝑞¯ , lifetime𝛼 , borrowx;𝑇 ;𝑝¯ , x = 𝑣ˆ ∝ 𝑤,
                                                                       ¤ 𝛤˚ ⊢𝐻 𝑣ˆ ∝ Mut𝑞¯ 𝑣¤ :: Mut𝛽 𝑈
                                               𝑝¯                                                     𝑝.0
                         𝛼 ≤ al ι          𝛤˚ ⊢𝐻 𝑡ˆ ∝ 𝑡¤ :: Skel 𝑇                                𝛤˚ ⊢𝐻 x ; y
                        ι , 𝛤˚ ⊢     𝑝¯  𝑞¯ ¤                                          𝑝¯
                                𝐻 𝑡 ∝ Mut 𝑡 :: Mut 𝑇                               𝛤˚ ⊢𝐻 Ref ℓ ∝ Ref x :: Skel (Ref 𝑇 )
                     end𝐻         ˆ               𝛼


                                                                               data F 𝑋¯ where C :: 𝑇 →𝜋 F 𝑋¯
                                              𝑝.𝑖
                     𝐻 ≠∅            ∀𝑖. 𝛤˚𝑖 ⊢𝐻 𝑖 x 𝑖 :: Skel (𝑇 𝑗,𝑖 [𝑈/𝑋 ])
                                                  Í ˚ 𝑝¯
                                                     𝑖 𝛤𝑖 ⊢𝐻 C 𝑗 x̄ ∝ C 𝑗 x̄ :: Skel (F 𝑈 )
                                                                                        ¯
Pure Borrow: Linear Haskell Meets Rust-Style Borrowing                                                   41


C     Metatheory
We present the omitted details of our metatheory introduced in §5.5.

C.1    Strong Confluence of Denotational Operational Semantics
Proof of Theorem 5.1. We say that the target variable of a (derivation of a) reduction 𝐸;           ¤ x →
 ¤ ′
𝐸 ; x is y if, other than dred-ktx, the reduction applies a rule whose conclusion is of the form
 ¤ y → 𝐸¤′ ; y.
𝐸;
     Assume that the target variables of 𝐺¤ → 𝐺¤ 1 and 𝐺¤ → 𝐺¤ 2 are x and y, respectively. If x = y,
then 𝐺¤ 1 = 𝐺¤ 2 holds, which contradicts the assumption. So we have x ≠ y. By straightforward case
analysis, we can derive the reductions 𝐺¤ 1 → 𝐺¤ + and 𝐺¤ 2 → 𝐺¤ + for some 𝐺¤ + , choosing y as the target
variable of the former reduction and x for the latter. A notable case is where one reduction executes
reclaim dred-reclaim; the confluence holds in this case, because the structure of restoration by
history Fig. 36c does not get affected by the reduction of any variable.                                 □

C.2    Basics of the Association System
Technically, the association judgment does not have a rule for weakening the resulting type. Instead,
it is carefully designed so that it is closed under subtyping:
Lemma C.1 (∝ is closed under subtyping). If 𝑇˚ ≼ 𝑈˚ , then 𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑇˚ implies 𝛤˚ ⊢ 𝑡ˆ ∝ 𝑡¤ :: 𝑈˚ .
Proof. By straightforward induction over the derivation of subtyping and association.                    □
    For Theorem 5.2, we introduce the following lemma:
Lemma C.2. If a term 𝑡 satisfies 𝛤 ⊢ 𝑡 :: 𝑇 , then we have 𝛤 ⊢ 𝑡 ∝ 𝑡 :: 𝑇 .
Proof. By straightforward induction over the typing derivation.                                          □
Proof of Theorem 5.2. Immediately from Lemma C.2.                                                        □
Proof of Theorem 5.3. Straightforward by definition.                                                     □

C.3    Progress and Bisimulation
Proof sketch for Conjecture 5.4. By careful case analysis. In particular, we maintain an invari-
ant on histories to ensure progress for lender reclamation dred-reclaim in denotational operational
semantics.                                                                                       □
Proof sketch for Conjecture 5.5. By careful case analysis. There are a few tricky factors. First,
the variable that owns each local or global deposit for a borrow can drastically change, especially
when a lifetime ends by endLifetime; still, the variable always moves to either an ancestor or
new children (possibly splitting the deposit), which is crucial for maintaining the disjointness
invariant for parBO. Also, when copying a value by unrestrictedness or as a skeleton from a
variable polymorphically typed by assoc-∀, we re-type the variable to make it free of assoc-∀,
polymorphically re-typing the variables that the variable depends on.                            □
