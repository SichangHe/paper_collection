                                          Annals of Formalized Mathematics
                                          Volume 1 (2025), 57–102
                                          DOI: https://doi.org/10.46298/afm.13477




                                         Derandomization with pseudorandomness

                                         Emin Karayel
arXiv:2404.16614v4 [cs.LO] 25 Jun 2025




                                              Abstract. Derandomization techniques are often used within advanced randomized
                                               algorithms. In particular, pseudorandom objects, such as hash families and expander
                                               graphs, are key components of such algorithms, but their verification presents a challenge.
                                              This work shows how such algorithms can be expressed and verified in Isabelle and
                                               presents a pseudorandom objects library that abstracts away the deep algebraic/analytic
                                               results involved. Moreover, it presents examples that show how the library eases and
                                               enables the verification of advanced randomized algorithms. Highlighting the value of
                                               this framework is that it was recently used to verify the space-optimal distinct elements
                                               algorithm by Błasiok from 2018, which relies on the combination of many derandomization
                                               techniques to achieve its optimality.




                                            © 2025 Emin Karayel
                                            This is an open access article licensed under the CC BY 4.0.
                                            To view a copy of the license, visit https://creativecommons.org/licenses/by/4.0/.
                                            MSC 2020: 03B35,68W20
                                            Keywords: Randomized Algorithms, Derandomization, Expander Graphs, Hash Families, Formal Verification

                                            Contact information:
                                              Emin Karayel: Technical University of Munich, School of Computation, Information and Technology,
                                              Germany. me@eminkarayel.de


                                            Received: April 26, 2024
                                            Final form: May 8, 2025
                                            Accepted: May 13, 2025
                                                 Emin Karayel

1       Introduction


        Computer scientists are familiar with pseudorandom number generators (PRNGs), func-
tions that consume a small sequence of seed bits and output a much larger sequence of
pseudorandom bits. Well-known examples are the Lehmer random number generator [O’N14;
PRB69], Blum Blum Shub [BBS83], and the Mersenne-Twister [MN98]. The randomness of
these functions can only be verified empirically [BMD22; SSK20]. But there are no mathemat-
ical, in particular, probability-theoretic theorems about them that would make them useful in
the design of provably correct randomized algorithms.1
        On the other hand, there are pseudorandom objects2 , such as k-independent hash families
and expander graphs, satisfying such theorems, for example, limited independence or Chernoff-
type tail bounds. They are often critical components of advanced randomized algorithms.
Similar to PRNGs, they are functions taking a small sequence of seed bits and returning a
much larger sequence of output bits. Often, the result is represented as a function or a vector.
        Pseudorandom objects are used as a derandomization technique and thus improve the
randomness usage of simpler algorithms. This is especially interesting in cases where the
saving in coin-flips translates into a reduction of space usage because the algorithm needs to
preserve the coin-flips during its operation. But, as we will see in this work, the construction
of pseudorandom objects relies on advanced mathematical foundations, such as finite fields
and spectral graph theory. This makes their formalization in proof assistants a challenge, as
well as the verification of randomized algorithms relying on them. This work shows how
advanced randomized algorithms can be expressed and verified in Isabelle/HOL [NPW02]
(and in general in every proof assistant), through the use of a composable pseudorandom
objects library.



A motivating example: To illustrate the utility of pseudorandom objects, let us look into
the following simple randomized streaming algorithm. For readers less familiar with Isabelle
syntax: It is possible to skip these. There is always a precise description of these algorithms
in the surrounding text.


    1
     There are conditional results, e.g., with the assumption of the difficulty of factoring. Moreover, there are
rigorous results about the period of some PRNGs, but they are usually not helpful with respect to the correctness
of algorithms using such PRNGs.
   2
     The term was coined by Vadhan [Vad12] but it is applied here more generally than he does.


                                                                                                              58
                                          Derandomization with pseudorandomness


       fun example_1 :: nat ⇒ nat list ⇒ real pmf
        where example_1 n xs =
         do {
             h ← prod_pmf {0..<n} (λ_. pmf_of_set {−1,1});
             return_pmf (( x ← xs. h x)2 )
                          P

         }


This is a randomized approximation algorithm for the second-frequency moment3 F2 of a
sequence x 1 , . . . , x m where the sequence values are assumed to be in the set U := {0, . . . , n−1}.
       In the first step, the algorithm randomly chooses a function h from U (the set containing
the sequence values) into the two-element set {−1, 1}, i.e., it assigns each element of U a
random signed unit. The algorithm then returns the square of the sum of the signed units
                                          Pm
assigned to each sequence element, i.e.: ( i=1 h(x i ))2 . It is effortless to verify that the
algorithm returns an approximation of F2 . Indeed, the expected result is:
              m          2                           2
              X                         X                        XX                                X
        E           h(x i )    =E             c(u)h(u)       =             c(u)c(v) E h(u)h(v) =         c(u)2 .   (1.1)
              i=1                       u∈U                      u∈U v∈U                           u∈U


Here, c(u) denotes the occurrence count of u in the stream x 1 , . . . , x m . The key step in the
above derivation is the third equality, where the expectation E h(u)h(v) is 0 if u ̸= v and 1
                                                 P
otherwise. The second frequency moment F2 is u∈U c(u)2 which corresponds to the right
hand side of the equation chain. A similar argument can be used to derive:
                                                         m          2
                                                         X
                                                  Var          h(x i )     ≤ 2F22 .                                (1.2)
                                                         i=1


The algorithm above is, however, not very efficient: It requires O(n + ln m) bits of memory. At
least n bits are required to store the function h and another O(ln m) bits for the accumulation
register while evaluating the sum. As promised, it can be improved using the “magic of pseu-
dorandomness”. Instead of choosing the function h completely randomly, which necessarily
requires O(n) bits of storage space, it can be selected using a pseudorandom object with a
small seed space. To achieve that, the function has to be stored implicitly using the seed
instead of as a dictionary.
   3
     The second frequency moment is the square sum of the occurrence counts of each value in the stream. It is
useful in assessing the skew of the stream, which can, for example, be needed in monitoring applications or
query optimization [DeW+92; Guf+11]. The algorithm [AMS99] is very concise, which makes it useful as an
illustrative example.


                                                                                                                     59
                                              Emin Karayel

   Let us recall that a set of random variables are k-wise independent if any k subset of them
are independent. And note that the expectation of a product of independent random variables
is the product of their expectations. Indeed, a careful examination of Eq. 1.1, shows that the
values of the function h only have to be pair-wise independent. In Eq. 1.1 in the last step, we
evaluate the product of only pairs of the random variables h(u), h(v). A similar observation
can be made for Eq. 1.2, where 4-wise independence is sufficient.
   This means that the pseudorandom object we want is required to form a 4-wise independent
family of functions. The following example is the formalization of the updated algorithm:

   fun example_2 :: nat ⇒ nat list ⇒ real pmf
    where example_2 n xs =
      do {
          h ← sample_pro (H 4 n (L [1,−1]))
          return_pmf (( x ← xs. h x)2 )
                       P

      }


The new algorithm has the same properties as example_1 (i.e., satisfying Eq. 1.1 and 1.2)
but requires only O(ln n + ln m) bits of memory. The only difference is in Line 4, where h
is now obtained using the pseudorandom object specified by the term H 4 n (L [1,−1]),
which requires O(ln n) bits of input as seed and returns a function from {0, . . . , n − 1} to
{−1, 1} (which is stored implicitly using the O(ln n) bits of space, instead of as a dictionary).
If the seed is chosen uniformly at random, then the evaluation of the function at any point
in {0, . . . , n − 1} forms a random variable. Crucially, the family of all n random variables is
4-wise independent, and each is distributed uniformly on {−1, 1}. The operation sample_pro
interprets a pseudorandom object as a probability space. It uniformly chooses a random seed
from the seed space of the pseudorandom object and evaluates the object at that seed.
   The expression H 4 n (L [1,−1]) from above represents a combined pseudorandom object.
It is defined using two constructs: The expression L [1,−1] describes a pseudorandom object
with a single-bit input that outputs −1 or 1 depending on the bit. The construct H k n P is a
k-independent hash family, with domain {0, . . . , n − 1}, and the range P, where P is another
pseudorandom object. This means it is easy to construct application-specific pseudorandom
objects from a small set of primitives. The presented ones are part of the libraries [Kar22f;
Kar23d] (available in the AFP [Afp] for Isabelle.)
   The step from example_1 to example_2 demonstrates derandomization with pseudorandom
objects. The above is just a teaser example and will be further expanded on in Section 7, where


                                                                                              60
                                    Derandomization with pseudorandomness

combinations of multiple types of pseudorandom objects, in particular, including expander
graphs, will take the stage.


Contributions: The main novel results presented in this work are:

    • A novel approach to constructing pseudorandom objects based on simple primitives
          and the introduction of notation for them that allows a succinct representation within
          algorithms using them.
    • Formal verification of an efficient and effective library for computations in both prime
          and non-prime finite fields, i.e., GF (p n ) for p prime and any n ≥ 1. Prior work in proof
          assistants [Div+20; Div+16] focused on the much simpler case of prime finite fields,
          i.e., the n = 1 case. This is the basis for the first pseudorandom object—k-independent
          hash families—detailed out in Section 5.
    • Formal verification of expander graphs and a construction of a strongly explicit family
          for every degree and spectral bound and the verification of tail bounds for random walks
          in expander graphs. This is the basis for the second pseudorandom object—random
          walks in expander graphs—detailed out in Section 6.

It should be noted that the examples are verified [Kar22b, Tutorial_Pseudorandom_Objects]
in Isabelle. The supporting libraries require more than 16300 lines of code4 because the
construction of the pseudorandom objects builds on mathematical foundations such as (non-
prime) finite fields and spectral graph theory. However, the libraries can be used easily based
on high-level results that abstract away implementation details.
        The following sections will discuss related work and additional important background.
The formalization of pseudorandom objects in an abstract way is detailed out in Section 4,
followed by the concrete pseudorandom objects k-independent hash families (in Section 5)
and expander graphs (in Section 6). Section 7 presents an application of the framework,
where multiple types of pseudorandom objects are going to combine to improve the previous
introductory example. Section 8 concludes with a summary and future research opportunities.


2       Related work

2.1       Derandomization with pseudorandomness

        As mentioned in the abstract, an exciting use case for this framework is the distinct
elements problem—estimating the number of distinct elements in a stream in a single pass
    4
        Appendix A provides a comprehensive list of the formalizations mentioned here.


                                                                                                  61
                                           Emin Karayel

with limited mutable state. The research on the problem started in 1985 by Flajolet [FN85],
followed by successive improvements [AMS99; BY+02; KNW10a] until an optimal solution
was found by Błasiok in 2018 [Bł18; Bł20]. In 2023 [Kar23b; Kar23c; Kar23a], I wrote about
its formalization using the framework for pseudorandom objects presented here. It is an
improved version of Błasiok’s solution. It has smaller implementation complexity, because
it uses fewer kinds of pseudorandom objects, and supports a merge operation making the
algorithm parallelizable, while still maintaining the optimal space-complexity. The concrete
pseudorandom object used there is an expander random walk chained with a second expander
random walk chained with a product of pseudorandom objects for k-independent hash families.
Indeed, the formalization of this algorithm was a big part of the motivation for the design of
the library presented in this work. At the current state of research, pseudorandom objects are
essential for the distinct elements problem. A notable exception is the solution by Chakraborty
et al. [CVM22] that does not require pseudorandom objects, but its space complexity is
asymptotically worse than the optimal solution.
       There are, of course, many further randomized algorithms that rely on pseudorandom
objects, such as heavy hitters [CCFC04], frequency moments [AMS99] and other stream statis-
tics [Bla+17], graph matching [Che+21], graph sparsification [CDP21] and low-distortion-
embeddings [HT23].
       Another motivating influence for this work is Goldreich’s chapter [Gol11a] on samplers:
Algorithms that probe a function at select points and obtain an estimate for the average of the
function. The performance of samplers is measured with respect to the number of probing
points, the number of random bits consumed, and the quality of the estimate. Goldreich
also relies mainly on the two fundamental pseudorandom objects mentioned here: expander
graphs and hash families. In contrast to this work, he does not treat pseudorandom objects as
first-class objects but the samplers, which use pseudorandom objects as a component. However,
that viewpoint prevents some of the applications I describe here, including the example from
the introduction. Conversely, samplers are easily represented with the framework presented
here.
       An ancestor of the notation developed here for pseudorandom objects was the work of
Kane et al. [KNW10a], who introduced a notation for hash families and forming products.
However, they do not consider chaining pseudorandom objects, for which there is no prior
art.
       Vadhan [Vad12] wrote a monograph and survey on pseudorandomness. As far as I can tell,
he coined the term pseudorandom object, and his work stands out by covering a large number


                                                                                            62
                             Derandomization with pseudorandomness

of derandomization techniques and highlighting connections and differences. Important to
note is that in this work, the term pseudorandom object is used more broadly than in Vadhan’s
monograph.

2.2   Verification of foundational libraries in proof Assistants

   Vilhena and Paulson [VP20] formalized foundational results on field theory, in particular,
that every field admits an algebraically closed extension. Although their work does not touch
on finite fields, and, in particular, there is no emphasis on efficient implementation of the
field operations. The efficient and effective finite fields library in this work [Kar22a] builds
on the theoretical results and framework developed by Vilhena and Paulson. The mathlib
library [Com20] in Lean has a proof of existence for both prime and non-prime finite fields.
However, in contrast to this work, they show the existence in a non-constructive way, without
providing and verifying algorithms that allow efficient computations in these fields. A similar
non-efficient existence proof has been verified in Mizar [Sch24].
   There is work on the formalization of Markov Chains, for example the Perron–Frobenius
theorem [Thi21; Thi17], and Markov decision processes [Höl17; SA23]. I could not find any
work on the formalization of expander graphs.

2.3   Randomized Algorithms in Proof Assistants

   The best way for the verification of randomized algorithms in Isabelle/HOL is based on the
Giry monad [Gir82], which is the method applied in this work. Eberl et al. [EHN20; EHN15]
have done foundational research and verified several randomized algorithms demonstrating
the feasibility of the approach. It should however be noted that this is still an active research
area [APM09; Bao+22; Cha+18; Höl16; Loc16; Sun+23]. Similarly there is work towards
transferring the approach to other proof assistants [TH18; Tas+21].
   There is, however, not yet much research on derandomization techniques (even k-
independent hash families). The only research I know of is the formalization of an approxi-
mate model counting algorithm that relies on the construction of a 3-universal XOR-based
hash-family by Tan et al. [TY24; Tan+24] in Isabelle/HOL. Their work uses some libraries
I developed during this work. Conversely, Yong Kiam Tan made several, much appreciated,
improvements to my AFP entry on the median method [Kar22e].
   In 2021 [Kar22c], I presented the formalization of randomized algorithms for frequency
moments. It only uses hash families (and only based on prime finite fields) and does not use
other pseudorandom objects or combinations of these. Moreover, the focus of this work is on
derandomization techniques, as opposed to the verification of concrete algorithms.


                                                                                              63
                                                 Emin Karayel

2.4       Other derandomization methods

        Besides the use of pseudorandom objects, there are also other derandomization methods.
The two most prominent are:

    • Non-uniform (non-constructive) derandomization
    • Method of conditional expectations (or probabilities)

The first—non-uniform derandomization—is based on Adleman’s theorem [Adl78], who
showed that any randomized algorithm with a finite set S of possible inputs can be derandom-
                                                                                                1
ized entirely. This works by first amplifying it until the failure probability is smaller than |S| .
For such an algorithm it is possible to show that there must exist a fixed choice of coin flips,
for which the algorithm must succeed for every input. This follows from a union-bound. The
result is sometimes abbreviated as: RP ⊆ P/poly. The theorem does not provide a way to find
such a sequence of coin-flips. The topic is less relevant for formal verification: Constructing
such an algorithm would require a brute-force search, and it is trivial to verify the correctness
of an algorithm with a finite input set.
        The second—method of conditional expectations [AS00; Vad12]—can be applied in some
specific cases. Given a randomized algorithm, it is sometimes possible to derive a deterministic
algorithm that performs at least as well as the randomized algorithm on average. This requires
that the probability space can be decomposed recursively into a search tree, where conditional
expectations can be computed for each node. I have formalized two algorithms based on
this technique [Kar24], but it turned out that it is straightforward to verify such algorithms.
This contrasts pseudorandom objects, which require large foundational libraries to work with
them.


3       Background on randomized algorithms

        This section provides a very small introduction, into the representation of (randomized)
algorithms in Isabelle.
        Isabelle is a meta-logic for which several instantiations exist [Pau94, Part III]. The most
prominent, and the framework used in this work, is HOL. Other instantiations are, for example,
First-order logic (FOL) or Zermelo–Fraenkel Set Theory (ZF). HOL can be described as a
typed version of classical mathematical logic.5
    5
    In my opinion HOL is actually closer to informal mathematics used today than, e.g., Isabelle/ZF. For example
a textbook proof would never consider the equality of a group and a neighborhood basis of a topology; they are,
informally, considered different types of objects, even though formally everything is a set.


                                                                                                             64
                               Derandomization with pseudorandomness

   The type system is similar to that of many functional programming languages, such as
Haskell or ML. The primitives nat, real represent natural (resp. real) numbers. It is also
possible to construct more complex types from simple ones, for example nat ⇒ real represents
a function from natural to real numbers. A bit unexpected is that type constructors are written
post-fix, e.g., nat list represents a list of natural numbers. Type variables are denoted using
primed letters, e.g.: ′a, ′b. The double colon is used to signify membership of an expression
or name in a particular type, e.g.: n :: nat.

   Isabelle’s expressions resemble standard mathematical notation closely, but there are
sometimes slight deviations. The following table summarizes such cases:




 Description                                Isabelle Term    Classical Math

 Cardinality of a set S                     card S           |S|
                                                             Pm
 Summation over a list xs = [x1 ,..,x m ]   ( x ← xs. f x)            f (x i )
                                             P
                                                              i=1
                                                             Pn−1
                                            ( i < n. f i)             f (i)
                                             P
 Summation over indices                                         i=0
 Interval with strict bounds                {a<..<b}         {x | a < x < b}
 Interval with inclusive bounds             {a..b}           {x | a ≤ x ≤ b}
 Strictly upper bounded set                 {..<b}           {x | x < b}




The interval notation is flexible. The above are just examples, but any combination of
unbounded, strict or inclusive lower and upper bounds are possible.

   An important type constructor for this work is the one describing probability mass functions
(PMFs): pmf. They are used to represent finite/discrete probability spaces and form a special
class of general probability spaces, with the condition that the σ-algebra is the powerset
of the universe of the type. Eberl [EHN20] provides a more thorough introduction. This
greatly reduces the difficulty of working with them because measurability becomes trivial.
Because distributions of randomized algorithms will always be supported on a countable
set, the condition on the σ-algebra is not a restriction. For example real pmf represents a
discrete probability space whose elements are real numbers. The following table provides a
brief overview of the terms that can be used to construct PMFs.


                                                                                            65
                                               Emin Karayel


 Term                     Description

 pmf_of_set S             For a finite set S, the uniform probability space on S. (Every
                          element of S is equiprobable.)
 pmf_of_multiset S        For a multiset S, the probability space on the elements of S,
                          with the probability of elements being proportional to their
                          multiplicity.
 pair_pmf A B             Given probability spaces A and B, the probability space sup-
                          ported on the product of the supports of A and B. (With each
                          pair (x, y) having the probability of the product of the probabil-
                          ities of x and y.)
 prod_pmf I M             Finite product of multiple probability spaces. The elements
                          are maps with a domain I, the index set, and values in M (i)
                          (depending on the index).
 map_pmf f A              The probability space representing the distribution of the ran-
                          dom variable f over the probability space A.
 return_pmf x             The probability space of the singleton {x}.
 bind_pmf p f             This represents algorithmically the composition of two ran-
                          domized algorithms p and f , where f is executed using the
                          result of p. Mathematically, bind_pmf p f is the probability
                          space for which an event E has the probability Pbind_pmf p f E :=
                            P f x (E) d p(x).
                          R

                          Note also that: map_pmf f p = bind_pmf p (return_pmf ◦ f )

The functions bind_pmf and return_pmf form the Giry monad for probability mass functions,
because of that, randomized algorithms can be represented more intuitively using the do-
notation. As an example bind_pmf p (λx. return_pmf (q x)) can be written as:


   do {
       x ← p;
       return_pmf (q x)
   }



which represents the distribution of a randomized algorithm that obtains x from the probability
space p and returns q x.


                                                                                               66
                              Derandomization with pseudorandomness

4   Pseudorandom objects

    This section is less exciting, but it is nevertheless necessary to tackle the basic definitions
before discussing the advanced objects. Let us take a brief look at the representation of
pseudorandom objects in Isabelle [Kar22f, Pseudorandom_Objects]. This is done using a
record:
    record ′a pseudorandom_object =
     pro_last :: nat
     pro_select :: nat ⇒ ′a

Note that the record type pseudorandom_object is parameterized over the type of the elements
of the pseudorandom object ′a. A record in Isabelle can be thought of as a tuple type, but
with the advantage that the components can be accessed using named selectors. In this case,
these are: pro_last, pro_select.
    The selector pro_last represents the object’s size minus 1. The selector pro_select is a
function that returns an element from the object, given an index between 0 and pro_last
(inclusive). Note that this means that pseudorandom objects always have at least one element.
Effectively, a pseudorandom object is just a non-empty multiset from which it is easy to
sample. The fact that empty pseudorandom objects are disallowed comes in handy because
this means that we can associate with any pseudorandom object: a probability space. The
function sample_pro does exactly that. It is defined as:

    sample_pro P = map_pmf (pro_select P) (pmf_of_set {0..pro_last P})

While we will keep explicitly using the term sample_pro, it is actually defined as a coercion.
Whenever a pseudorandom object is used in a place that requires a probability space, Isa-
belle would automatically convert it to a probability space by introducing an application of
sample_pro. This is similar to the automatic coercion of integers to real numbers.
    Note that the function pro_select is not required to be injective. Such a condition would
incur a performance cost for the more complex pseudorandom objects, such as expander
graphs. For an element x of a pseudorandom object, we call the count of indices in {0..pro_size
P} mapped to x the multiplicity of x.
    The following are trivial pseudorandom objects and combinators defined in the AFP
library [Kar22f, Pseudorandom_Objects]:

    • If xs is a non-empty list, then L xs is a pseudorandom object. The multiplicity of
      an element is its occurrence count in the list. In particular: sample_pro (L xs) =
      pmf_of_multiset (mset xs).


                                                                                                67
                                             Emin Karayel

    • If n > 0, then N n is the pseudorandom object for the natural numbers {0, . . . , n − 1}
      (each with multiplicity 1). In particular: sample_pro (N n) = pmf_of_set {0..<n}.
    • If P and Q are pseudorandom objects, then P × P Q denotes the product pseudorandom
      object. Its size is the product of the sizes of P and Q and consists of pairs whose first
      component is from P and whose second component is from Q. The multiplicity of a pair
      (x, y) is the product of the multiplicities of x in P and y in Q.
      In particular: sample_pro (P × P Q) = pair_pmf (sample_pro P) (sample_pro P).

In the following two sections, we will dive into the more exciting pseudorandom objects. The
following section is dedicated to k-independent hash families and Section 6 to random walks
in expander graphs.


5   Hash families

    The textbook [Vad12, page 3.31] definition of k-independent hash families is as a family
of functions from a finite domain D to a finite range R. For any domain element d ∈ D, we
can associate a random variable X d —the evaluation of the function at the point d, where the
probability space is the hash family. The key condition k-independent hash families satisfy is
that the random variables X d are k-wise independent and uniformly distributed in the range
R. More formally, the condition can be expressed as:
                                            
                                  ^                 Y                      |As |
                             P         X s ∈ As =         P(X s ∈ As ) =
                                 s∈S                s∈S
                                                                            |R|

for all subsets S ⊆ D with at most k elements and arbitrary sets As ⊆ R.
    The classic construction for such families is due to Wegman and Carter [WC81], where
the hash functions are just polynomials (with degrees strictly smaller than k) over finite fields.
It is straightforward to verify the k-independence, which follows from the algebraic fact that
there is exactly one polynomial (of degree smaller than k) interpolating a given set of k points.
(See also Figure 1.)
    In particular, using the Galois field GF(q), where q is a prime power, we obtain a family of
functions on [q] → [q]. Here, the notation [n] stands for the set of the first n natural numbers,
ie, [n] := {0, . . . , n − 1}. The seed space for the hash family is [q k ], which is converted to the
coefficients of a degree k polynomial.
    It is straightforward to construct k-independent hash families with different domains and
ranges; for example, if m divides q, then composition with x 7→ x mod m does not affect


                                                                                                   68
                                  Derandomization with pseudorandomness


                                     4




                           f(x)
                                     2




                                     0
                                         0    1     2       3    4        5
                                                        x

Figure 1: There is exactly one polynomial of degree less than 3 interpolating 3 points on the
real line. The same is true in finite fields.

the k-wise independence or uniform distribution property. This allows us to construct hash
families from [q] to [m], if m divides q and q is a prime power using the Galois field GF(q).
Note that m must itself be a prime power, since any divisor of a prime power is again a prime
power. Moreover, we of course do not have to use the entire domain [q], i.e., we can regard
the hash family from [q] to [m] as a hash family from [n] to [m], if [n] ⊆ [q] or equivalently
n ≤ q. This means we can construct a k-independent family for functions between any domain
of size n and range of size m, where n is arbitrary, and m must be a prime power. This works
by choosing q as p j where j := max(log p n, log p m) and p is the unique prime dividing m.
   The approach taken in the formalization [Kar22f, Pseudorandom_Objects_Hash_Families]
goes beyond that because hash families may be used to select the seed of another pseudoran-
dom object. This is key to the compositionality of the pseudorandom objects library. Instead
of selecting a finite set for the range, in the formalization, the range space can be any other
pseudorandom object (if its seed space’s size is a prime power). Internally, this just represents
composition with the selection function of the new pseudorandom object. Notationally, this is
represented by the expression H k n P where P must be a pseudorandom object with a seed
space whose size is a prime power. The above is not a restriction because we can, of course,
just write: H k n (N m) to obtain a family from [n] to [m] (if m is a prime power.)
   Note that the seed space of the Carter–Wegman hash family is always a prime power. This
means it is possible to chain hash families.
   The defining property of k-independent hash families is expressed in the following
way:

   map_pmf (restrict J) (sample_pro (H k n P)) = prod_pmf J (λ_. sample_pro P)


                                                                                              69
                                                        Emin Karayel

under the condition that J ⊆ {0..<n} and card J ≤ k. I.e., if the domains are restricted to any
k element set, the functions from the pseudorandom object behave as if they are random
functions. More precisely, they behave as if they are sampled independently using the inner
pseudorandom object P.
    The fact that the right-hand side is expressed with respect to the probability space of the
chained pseudorandom object sample_pro P permits the derivation of results in the case of
more complex combined pseudorandom objects. For interested readers, Section 7 contains a
step-by-step proof using combinations of pseudorandom objects.


5.1   Construction of finite fields


    Critical to the construction of the Carter–Wegman hash families is the construction of finite
fields. For any prime p, the factor ring GF(p) := Z/pZ is a finite field, but not all finite fields
can be constructed in this way. The finite fields of order p k , where k > 1, can be constructed
using factors of polynomial rings. In particular, if f is an irreducible polynomial of degree k
with coefficients in a finite field F , then the factor ring F [X ]/ f F [X ] becomes a finite field
of order |F |k . This means the construction of the finite field GF(p k ) reduces to finding an
irreducible polynomial of degree k with coefficients in GF(p).
    The latter is helped by the fact that the probability of a random polynomial of degree
                                    1
k ≥ 1 being irreducible is at least 2k —a consequence of Gauss’s formula counting the number
of irreducible polynomials of a given degree over a finite field GF(p):
                                                                       !
                                                    1 X
                                                          µ(d)p k/d
                                                    k d|k

In the above formula µ(d) denotes the Möbius function, whose value is 0 if d has a square
factor, and otherwise it is 1 (resp. −1) if d has an even (resp. odd) number of prime factors.
The formula follows from a deep result by Gauss, showing that in a finite field F an irreducible
                             n                                                                                n
polynomial divides X |F | − X if its degree divides n, as well as the fact that X |F | − X is
square-free.
    Another consequence of the above is Rabin’s irreducibility test [Rab80]; a polynomial f is
                                 deg( f )                                    deg( f )/k
irreducible if it divides X |F |            − X , but is coprime w.r.t. X |F |            − X for any prime k dividing
deg( f ).
    The latter suggests a practical algorithm to obtain irreducible polynomials by sampling
polynomials randomly and checking for irreducibility. And indeed, this is a practical strategy.


                                                                                                                   70
                                  Derandomization with pseudorandomness

The algorithm’s expected iteration count is O(k). As far as I know, there are no deterministic
algorithms that have a similar performance [AL86; Sho88].
   The AFP entry [Kar22a] contains a formalization of these results, in particular, a complete
characterization of the finite fields, i.e., that every finite field is of prime power order and finite
fields with the same order are isomorphic [IR82; LN86; MP13], Gauss formula, the Frobenius
homomorphism and Rabin’s irreducibility test. It also introduces efficient algorithms for field
operations, e.g., computing the inverse using the extended Euclidean algorithm, as well as
long division and fast binary modular exponentiation.
   For interested readers, the following code fragment is the sampling algorithm for irre-
ducible polynomials [Kar22a, Find_Irreducible_Poly]:

   partial_function (smpf ) sample_irreducible_poly :: nat ⇒ nat ⇒ (nat list × nat)
     where sample_irreducible_poly p n =
      do {
          k ← spmf_of_set {..<p^k};
          let poly = enum_monic_poly (mod_ring p) n k;
          if rabin_test (mod_ring p) poly
           then return_spmf (poly,1)
           else tick_spmf (sample_irreducible_poly p n)
      }


Note that the algorithm does not terminate unconditionally, but only almost surely, i.e., the
probability that it does not terminate is 0. This is why the sampling algorithm is represented as
a partial function in the SPMF monad. Such functions have a different semantics. In particular
ordinary induction proofs can not be applied but must be replaced with a probabilistic
convergence proof. This relies on the framework by Lochbihler [Loc17]. The entry also
contains several illustrative examples.
   The algorithm example_2 from the introduction used a deterministic construction of the
finite fields. (Internally, it chooses the lexicographically smallest irreducible polynomial of a
given degree.) However, as we just saw, a randomized selection of the irreducible polynomial
is more efficient. To use that version, the example needs to be modified slightly:




                                                                                                    71
                                                      Emin Karayel


        fun example_3 :: nat ⇒ nat list ⇒ real pmf
         where example_3 n xs =
          do {
              h ← sample_pro =<< H P 4 n (L [1,−1])
              return_pmf (( x ← xs. h x)2 )
                           P

          }

I.e., we replace function applications with monadic applications =<< and use the constructor
H P instead of the deterministic version H. Note that =<< is just the flipped version of the
more classical bind operator >>=.
        This actually increases the number of coin flips, but the expected number of coin flips
remains the same asymptotically.



6       Expander graphs

        The next pseudorandom object is based on random walks in expander graphs [Alo86;
Chu97]. They are complementary to hash families. While k-independent hash families
approximate independent sampling, in the sense that any k element set form independent
variables, random walks in expander graphs form a more analytic approximation of indepen-
dence: An l-step random walk in an expander graph satisfies Chernoff-bounds similar to that
of an l-wise independent product. What this exactly means will be explored at the end of this
section.
        In the example in Section 7, we will see how the combination of these two types of
pseudorandom objects can lead to impressive results. Let us first briefly review the concept of
expander graphs before presenting the notion of strongly explicit expander graphs, concluding
with the construction of the pseudorandom object as random walks in them.
        A family of expander graphs is an infinite sequence G1 , G2 , . . . of undirected d-regular
graphs6 satisfying a common expansion property (detailed below). The size of the graphs
increases monotonically but not too fast. Hoory et al. require |Gi | < |Gi+1 | ≤ |Gi |2 [HLW06,
Def 2.3], which we follow here, but note that the growth condition is by no means standard.
Moreover, it is essential to note that parallel edges and self-loops are allowed. Mathematically,
such a graph can be modeled as a pair of finite sets (V, E), where E is a subset of V × V × L
and L is an arbitrary space of labels for the edges. An alternative would be to use the more
classical E ⊆ V × V but allow E to be a multiset.
    6
        A graph is d-regular if all of its nodes have degree d.


                                                                                                72
                                    Derandomization with pseudorandomness




Figure 2: A 3-regular graph with expansion properties: λa (G) ≤ 0.85, λ2 (G) ≤ 0.71, h(G) ≤
0.72.


       For each graph, we can associate an adjacency matrix. Given an ordering of the vertices,
each cell of the adjacency matrix A = (ai j ) denotes the number of edges between the i-th
vertex and the j-th vertex. The fact that the graphs must be undirected and regular, i.e., the
degree of all nodes being the same, means that the matrix is symmetric, and each row and
column has the same sum corresponding to the degree of the nodes. The normalized matrix,
i.e., scaling the adjacency matrix by the inverse degree of the graph, is called the stochastic
matrix. It corresponds to the transition matrix of a random walk in the graph. Because the
matrix is symmetric the eigenvalues of both the stochastic and adjacency matrices are all
on the real line. We denote the |G| eigenvalues (taking multiplicities into account) of the
stochastic matrix in decreasing order by λ1 , . . . , λ|G| , i.e., λ1 ≥ λ2 ≥ · · · ≥ λ|G| , and the second
largest magnitude of the eigenvalues by λa , i.e., λa := max(|λ2 |, |λ|G| |).7 Different authors
use different definitions; commonly, one of the following expansion conditions is employed:


 (1) The second largest absolute eigenvalues of the stochastic matrices of all the graphs in
         the family is bounded by a common value c < 1, i.e., λa (Gi ) < c for all i.
 (2) The second largest eigenvalues of the stochastic matrices are bounded by a value c < 1,
         i.e., λ2 (Gi ) < c for all i.
 (3) There is a common strictly positive lower bound on the edge expansions h(Gi ), where
         h(G) is the minimum ratio between the number of edges crossing a cut and the (smaller)
                                                         E(S,G\S)
         size of the cut, i.e., h(G) = min0<|S|<|G| min(|S|,|G\S|) .


   The definition is consistent with the description because λ1 = 1 and λ|G| ≥ −1 for symmetric stochastic
   7

matrices.


                                                                                                       73
                                                 Emin Karayel

See also Figure 2 for an example graph with its expansion properties. Property (1) of course
implies Property (2). The converse is not true. The Cheeger inequality shows that Property (2)
and (3) are qualitatively equivalent:

                                d                        Æ
                                  (1 − λ2 (G)) ≤ h(G) ≤ d 2(1 − λ2 (G)).
                                2

For interested readers, it is straightforward to conclude that random walks in these graphs are
rapidly mixing Markov chains [Chu+12; Gol11b; Gur16]. There is a unique stationary state,
which is the uniform distribution, i.e., the probability of each node is equal in the stationary
state of the chain. The corresponding stochastic matrix has an eigenvalue 1 with multiplicity
1 with a corresponding eigenvector with all components identical and non-zero. This is the
Perron–Frobenius eigenvalue. Moreover we can automatically conclude the graphs must be
connected.
   There are the following alternative variational definitions for λa (G), λ2 (G), which are
useful:

                                λa (G) :=     max |x ⊺Ax| =       max ∥Ax∥                (6.1)
                                            ∥x∥=1,x⊥u           ∥x∥=1,x⊥u

                                λ2 (G) :=     max       x ⊺Ax                             (6.2)
                                            ∥x∥=1,x⊥u


where u is the eigenvector (ui := |G|−1/2 ) corresponding to the uniform distribution, which
for expander graphs represents the unique stationary state.
   The reason we are interested in expander graphs is that random walks in them approximate
independent sampling, satisfying Chernoff bounds similar to ones for independent random
variables.
   For example, let us assume a µ-fraction of the vertices of an expander graph with n vertices
are marked by 1, while the other vertices are marked by 0, i.e., let f : G → {0, 1} such that
µ = 1n |{x ∈ G | h(x) = 1}|. If we choose l vertices independently, then the number of vertices
hitting the µ-fraction will be concentrated around µn, with a sharp tail bound satisfying:
                                  l
                                                     
                                1X
                  P v∈G l             f (vi ) − µ ≥ c ≤ 2 exp(−lc 2 ) for    c ≥ 0.       (6.3)
                                l i=1

Note that this follows from the classic Hoeffding inequality. Instead of choosing the vertices
independently, we can start at a random vertex and perform a random walk, where each edge
of the walk is chosen uniformly from those that are incident to the current vertex. As alluded


                                                                                             74
                                             Derandomization with pseudorandomness



                     1                                                          1
      probability




                                                                 probability
                    0.5                                                        0.5 ← λa →




                     0                                                          0
                          0         1          2             3                      0       1          2         3
                                deviation from mean                                     deviation from mean

Figure 3: Comparison of tail bounds for independent vs. random walk sampling (for l = 5).


to above, this will satisfy a similar Chernoff bound:
                                          l
                                                                        
                                        1X
                    P v∈Walk(G,l)             f (vi ) − µ ≥ (c + λa (G)) ≤ 2 exp(−lc 2 ) for            c ≥ 0.       (6.4)
                                        l i=1

The key advantage of random walks in expander graphs, compared to choosing vertices
randomly, is that the number of coin flips necessary to select such a walk is only O(ln |G| +
l ln d)—as opposed to O(l ln |G|), i.e., we can reduce the number of coin flips, paying with
the additional additive term λa (G) in Eq. 6.4. (See also Figure 3.)


6.1   Formalization

   Because of the many possible definitions, the formalization [Kar23d] is as flexible as
possible. It introduces regular graphs as a specialization of general graphs, introduced in
the AFP-library for Isabelle by Noschinski [Nos13; Nos14]. For such graphs all three types
of expansion conditions are introduced. As well as theorems such as the Cheeger inequality,
Eq. 6.1 or 6.2, and the previously mentioned Chernoff bound for random walks (Eq. 6.4.)
   The proofs rely heavily on matrix algebra. Note that Isabelle has two major representations
of matrices and vectors with different approaches.
   Thiemann et al. [TY16; TY15] developed a tuple-based representation, where vectors
and matrices are functions paired with their dimension. This approach is especially useful
when performing induction over the dimension of the vector or matrix, e.g., verifying an
algorithm that computes the Jordan normal form. The main drawback is that they require
explicit proofs of dimensional consistency. For example to apply associativity A(BC) = (AB)C,


                                                                                                                       75
                                           Emin Karayel

we need to check that the row count of A equals the column count of B and that the row count
of B matches the column count of C. This has a detrimental influence on proof automation.
    The alternative representation—the one I chose—is part of the HOL-Library and relies on
numeral types. Vectors are represented as functions from a finite type with a size corresponding
to the dimension of the vector space to the real/complex numbers. This representation has
the advantage of enabling type-level verification of dimensional consistency, which works
seamlessly. Indeed, it often helps avoid type annotations as they can be inferred automatically.
The approach was developed by Harrison [Har05].
    To be able to use the type-based representation, it was necessary to rely on the types-to-set
mechanism [Kun16; KP16]. This works by introducing an assumption that a type exists,
whose size matches the vertex set of the graph. With the assumption it is possible to define
the stochastic matrix, and perform algebraic arguments. The assumption for the existence
of the type can then be discharged for theorems that do not refer to it. This means that the
non-algebraic results about expander graphs are available even without such an assumption.
A trick I employed is to introduce λa (G), λ2 (G) using the variational definitions (Eq. 6.1 and
6.2), i.e., without referring to the stochastic matrix, and show they are equivalent to the
spectral definition, i.e., with respect to the multiset of eigenvalues. This allows the expression
of all the relevant theorems, without explicit reference to the stochastic matrix, and hence
the type pre-condition could be discharged for them.


6.2   Diagonalization

    We will not go into all of the proofs. Nevertheless, the following is an interesting proof
technique [Kar23d, Expander_Graphs_Eigenvalues] that highlights some of the fine issues
when formalizing textbook proofs. Let us recall Eq. 6.1:

                                    λa (G) =     max |x ⊺Ax|                                (6.5)
                                               ∥x∥=1,x⊥u


where A is the stochastic matrix of a regular graph G, and u is the vector whose components
are all |G|−1/2 .
    Note that this is true, whether or not G is connected. Even though expander graphs are
connected, it is useful to establish Eq. 6.5 unconditionally, because in the formalization it is
used as an introduction rule to establish that a graph is an expander by proving the expansion
condition. This then spares us from having to separately verify the connectedness of the
graph, since it follows implicitly, if we can establish λa (G) < 1 (or λ2 (G) < 1).


                                                                                               76
                                  Derandomization with pseudorandomness

      The easiest way to see that Eq. 6.5 is true is to consider the diagonalization of A, i.e.,
there exists a unitary matrix U s.t. A = U ⊺DU where D is a diagonal matrix consisting of the
eigenvalues (with their respective multiplicities) of A. The rows of U consist of eigenvectors
of A. More precisely, the i-th row is the eigenvector, corresponding to the i-th eigenvalue in
the diagonal matrix D. This means the right-hand side of Eq. 6.5 equals max∥ y∥=1, y⊥Uu | y ⊺D y|.
One of the diagonal elements of D (e.g., dii ) must be a 1 for which the corresponding row in
U should be the stationary eigenvector u. And Uu will be the i-th basis vector. From this, we
can derive that the right-hand side is indeed λa (G), the second largest eigenvalue of A.
      Unfortunately, that argument fails, in general, if the multiplicity of the eigenvalue 1 is
larger than 1. However, there always exists a decomposition of the above form, where one of
the rows of U is the eigenvector u, but that is not something we can immediately derive from
the classical decomposition theorem.
      The best strategy to solve this problem is to use simultaneous diagonalization. For that,
observe that A commutes with the matrix J, whose entries are all |G|−1 . This follows from
the regularity property. On the other hand, for J, the multiplicity of the eigenvalue 1 is
1. The only other eigenvalue of J is 0 with a multiplicity of |G| − 1. Now let us obtain a
simultaneous diagonalization of A and J (this is possible because both are symmetric, real,
and they commute with each other [HJ13, Th. 1.3.12, Th. 2.5.3])8 :

                                                A = U ⊺DU
                                                J = U ⊺EU

Now, there is an index i s.t. eii = 1, corresponding to the u in U, because of the decomposition
of J. Thus, we obtain a sequence of eigenvectors of A, which necessarily contains the
eigenvector u.
      It should be noted that the same result could be obtained by introducing a correction to
the diagonalization of A since the span of the eigenspace for the eigenvalue 1 will contain the
eigenvector u. However, the approach above is much more elegant.

6.3     Strongly explicit expander graphs

      The class of expander graphs that are needed for derandomization are strongly explicit
expander graphs. For such a graph, it is possible to sample a random vertex uniformly and
compute the edges incident to a given vertex algorithmically, i.e., it is possible to sample
a random walk without having to represent the graph in memory. This makes them very
  8
      The result has been formalized by Echenim [Ech22].


                                                                                               77
                                           Emin Karayel

useful for the application in space-constrained settings. This is in contrast to randomized
constructions of expander graphs [Alo86; McK81], which is much easier but would require
the representation of the graph in memory.
   The first strongly explicit construction was by Margulis [Mar73], who could show for a
family of graphs that they have a spectral bound strictly smaller than 1, but the bound itself
was unknown. A few years later, Gabber and Galil [GG81] managed to show, for a slightly
                                                                    p
different family of graphs, a concrete spectral bound: λa (Gn ) ≤ 58 2 ≈ 0.884.
   The description of their family of graphs—now usually called the Margulis–Gaber–Galil
family—is pretty elementary. For every n > 0, the graph Gn has n2 vertices, which we label
with the elements of Z/nZ × Z/nZ. Then each vertex (x, y) ∈ Gn is connected to the vertices:

    (x + 1, y), (x − 1, y)(x, y + 1), (x, y − 1), (x, y + x), (x, y − x), (x + y, y), (x − y, y)

The elementary description is, however, quite deceiving because the derivation of the spectral
bound is far from it. There were multiple efforts towards reducing the complexity of the proof.
Indeed, the initial proof by Gabber and Galil was improved by Jimbo and Marouka [JM85] in
1985. Ravi Boppana further improved it in his lectures. Hoory et al. [HLW06, §8] present a
version of his proof. But even for that last version, the authors admit that it is “subtle and
mysterious.” It heavily relies on the discrete Fourier transform on the torus Z/nZ × Z/nZ,
followed by a number of careful decoupling steps, a partial order, many case splits, and
symmetry arguments.
   After that, there was more research. For example, Lee [Lee24] shows a weaker spectral
bound for the same family but with a less complex proof.
   The formalized proof [Kar23d, Expander_Graphs_MGG] obtains the best-known spectral
        p
bound 58 2 and follows the previously mentioned proof by Hoory et al. (although I could
improve on their proof slightly by using one more symmetry argument to reduce the number
of case splits).
   After Margulis’s discovery, many more constructions have been found [ASS08; MSS15]. An
interesting solution was discovered by Reingold et al. [RVW00] called the zig-zag construction,
which works by starting with small fixed expander graphs and performing various graph
operations to construct a family of larger expander graphs. This would be easy to formalize,
although the Margulis construction is much more elegant. Moreover, the fact that the vertex
counts of successive Margulis graphs do not grow by more than a factor of two is helpful, as
we will see later in this section.


                                                                                                   78
                                Derandomization with pseudorandomness

    Other constructions rely on the Cayley graph of non-abelian groups [KLN06; Lub11]. The
proofs heavily rely on representation theory, which would require much more groundwork in
Isabelle/HOL. In particular, constructions of Ramanujan graphs [LPS88], which are expander
graphs with the best-possible spectral bound (with respect to their degree.), belong to this
group. I believe the formalization of such a construction is a significant open problem.

6.4    Graph operations

    The Margulis–Gabber–Galil family consists of graphs for all vertex counts that are square.
Using a method described by Murtagh et al. [Mur+19], it is possible to obtain expander
graphs for every vertex count. This works by vertex identification, specifically given an
expander graph G with degree d, a spectral bound λa and n vertices v0 , . . . , vn−1 , we identify
distinct vertices (e.g., vertex v0 with vm , v1 with vm+1 etc. and vn−m−1 with vn−1 ) for some m
s.t. 2n ≤ m ≤ n. Note that edges are preserved, even if this introduces parallel edges. If there
is an edge between identified vertices, the edge becomes a self-loop. To preserve regularity,
we introduce d self-loops for vertices that have not been paired (i.e. for vn−m , . . . , vm−1 ). This
means the resulting contracted graph will have degree 2d.
                                                                                         λa (G)+1
    Then, the resulting graph will have a spectral bound of at most                          2    .
    While the idea is due to Murtagh et al., they only show that contracting a graph with a spec-
tral bound of at most 14 results in a graph with a spectral bound of at most 12 . Note that the result
stated above, which is part of the formalization [Kar23d, Expander_Graphs_Strongly_Explicit],
is a generalization.
    Let us go through the proof, which can be verified using a generalization of Eq. 6.1.

                       |x ⊺Ax| ≤ λa (G)∥x∥2 + (1 − λa (G))(x ⊺u)2                  for all   x.        (6.6)

where u is defined as in Eq. 6.1.
    Let x ∈ Rm , x =
                   ̸ 0 and x ⊥ u′ and let A denote the stochastic matrix of G and A′ be the
stochastic matrix of the contracted graph G ′ . Similarly u ∈ Rn , ui = n−1/2 and u′ ∈ Rm , u′i =
                                                         Pm−1
m−1/2 . Moreover let y ∈ Rn s.t. yi := x i mod m and β =        x 2 . Then:
                                                          i=n−m i



                                   n−1
                                   X                                     m−1
                                                                         X
      2|x ⊺A′ x|        =                   x i mod m ai j x j mod m +           x i2 ≤ | y ⊺Ay| + β
                                   i, j=0                                i=n−m

                        ≤         λa (G)∥ y∥ + (1 − λa (G))( y ⊺u)2 + β
                                                   2

                    Eq. 6.6
                        =         λa (G)(∥ y∥2 + β) + (1 − λa (G))(( y ⊺u)2 + β)


                                                                                                         79
                                            Emin Karayel
                                                                    n−1                     2        !
                                                                    X
                       =          2λa (G)∥x∥2 + (1 − λa (G))               x i mod m n−1/2        +β
                                                                     i=0
                                                                    n−1                     2        !
                                                                    X
                       =          2λa (G)∥x∥2 + (1 − λa (G))               x i mod m n−1/2        +β
                           ′
                     x ⊥u                                           i=m
                                                                n−1                    n−1            
                                                                 X                        X1
                       ≤          2λa (G)∥x∥2 + (1 − λa (G))               x i2mod m             +β
                Cauchy–Schwarz                                      i=m                   i=m
                                                                                              n
                                                                           n−m−1             
                                                             n−m              X
                       =          2λa (G)∥x∥2 + (1 − λa (G))                            x i2 + β
                                                              n                 i=0
                       ≤          2λa (G)∥x∥ + (1 − λa (G))∥x∥ .
                                              2                     2

                 (n − m)/n ≤ 1

   Using the Margulis construction and the fact that there is a square between any n and
2n (inclusive), it follows that there is a strongly explicit expander graph with spectral bound
  p
(5 2 + 8)/16 and degree 16 for every vertex count.
   Another graph operation is the power operation, which can be used to improve the spectral
bound [Kar23d, Expander_Graphs_Power_Construction]. Let G be a graph, then the k-th
power of G is a graph—denoted as G k —consisting of the same set of vertices, where the
number of edges between two vertices v and w in G k is the number of paths of length k
between v and w in G. Note that algebraically the stochastic matrix of G k is Ak if A is the
stochastic matrix of G. It is easy to verify that λa (G k ) ≤ λa (G)k .
   The previous two observations, in combination, imply that there exists a strongly explicit
expander graph for every vertex count and any spectral bound λa > 0 with a degree satisfying:
ln d ∈ O(ln(λ−1
             a
                )) as λa → 0 [Kar23d, Expander_Graphs_Strongly_Explicit]. At this point, we
are finally at a stage where we can introduce the second pseudorandom object, denoted by E
l Λ P. It first selects the strongly explicit expander graph constructed above with a number of
vertices n, matching the size of the seed space of P and a spectral bound of at most Λ. Then,
it samples random walks in that graph of length l. Note that because of the regularity of the
graph, there are exactly nd l−1 random walks, and given a number between {0, . . . , nd l−1 − 1},
we can output the vertices representing that path algorithmically. Here, it is important that
multiplicities are taken into account, which is also the reason some vertex tuples may have a
multiplicity higher than 1.
   Note that, for the users of the library, it is possible to ignore the complex internal structure
of the pseudorandom object. Let us consider the classic Hoeffding bound for independent
{0, 1}-valued random variables:



                                                                                                               80
                               Derandomization with pseudorandomness


    theorem classic_chernoff_bound:
      assumes AE x in measure_pmf p. f x ∈ {0,1}
      defines µ = expectation p f
      shows P(w in prod_pmf {0..<l} (λ_. p). |       j<l. f (w j)−l∗µ|≥l∗c)≤2∗exp(−n∗c^2)
                                                 P


If we instead wanted to choose expander random walks, we can substitute the sampling space
and use the Chernoff bound for these [Kar23d, Pseudorandom_Objects_Expander_Walks]:

    theorem expander_chernoff_bound:
      assumes AE x in sample_pro P. f x ∈ {0,1}
      defines µ = expectation (sample_pro P) f
      shows P(w in sample_pro (E l Λ P). | j<l. f (w j)−l∗µ|≥l∗(c+Λ))≤2∗exp(−n∗c^2)
                                          P


    Like before, the theorem is expressed with respect to the probability space of the chained
pseudorandom object: sample_pro P, which allows the derivation of results with respect to
more complex combined pseudorandom objects seamlessly. As mentioned before Section 7
will demonstrate this on a concrete example.

6.5    Efficiency

    The pseudorandom objects presented are implemented in an effective and efficient way.
This means that the algorithms can be exported into executable efficient code [HN10] in
various languages such as Haskell, Scala or SML. For example, the field inversion operation is
implemented using Euclid’s algorithm. Large powers are computed using the exponentiation
by squaring technique.
    Here, it is essential to note that, for randomized algorithms, this does not work directly
because they are represented in Isabelle using the Giry monad. However, there is a frame-
work introduced by Eberl and myself [KE23], which enables exporting code for randomized
algorithms. This works by externalizing the source of randomness using a lazy stream of
coin flips and establishing a Scott-continuous monad-morphism between the Giry monad
representation and the representation as a randomness consumer. The resulting code can
then be executed in the target language using any source of randomness (for example, a
hardware random number generator).


7     Combining pseudorandom objects

    This section presents a concrete example where a combination of multiple pseudorandom
objects are used to improve an algorithm’s space complexity. To achieve that, we are going


                                                                                            81
                                              Emin Karayel

to start with example_2 from the introduction and improve its accuracy (relative error with
respect to the correct value) and its probability of success, i.e., the probability with which the
algorithm returns a result with the desired accuracy. To make the presentation accessible, we
will do this step-by-step and also briefly point to the main points of the correctness proofs.
The examples are all also available in the AFP [Kar22b, Tutorial_Pseudorandom_Objects].
Let us recall:

   fun example_2 :: nat ⇒ nat list ⇒ real pmf
    where example_2 n xs =
      do {
          h ← sample_pro (H 4 n (L [1,−1]))
          return_pmf (( x ← xs. h x)2 )
                       P

      }


We had already established that the result has the expectation F2 and a variance of at most
2F22 . A standard technique to improve the accuracy of such an algorithm is to run it in parallel
multiple times and obtain the average.

   fun example_4 :: nat ⇒ nat list ⇒ real pmf
    where example_4 n xs =
      do {
          let s = ⌈8/ϵ^2⌉;
          h ← prod_pmf {0..<s} (λ_. sample_pro (H 4 n (L [1,−1])));
          return_pmf (( j<s. ( x ← xs. h j x)2 )/s)
                       P      P

      }


It is possible to show that the above algorithm returns an estimate of F2 with relative error ϵ
with probability at least 34 , or equivalently the probability that the result does not have the
desired accuracy is at most 41 .

   lemma example_4_correct:
    assumes set xs ⊆ {0..<n}
    shows P(ω in example_4. |ω − F2 xs| > ϵ ∗ F2 xs) ≤ 1/4


Usually the first step of the verification is to express the result in terms of random variables
over the probability space of the pseudorandom object(s):



                                                                                               82
                                   Derandomization with pseudorandomness


       define s where s = ⌈8/ϵ^2⌉
       define R where R h = ( j<s. ( x ← xs. h x)2 )/s
                             P      P



       let ?q = prod_pmf {0..<s} (λ_. sample_pro (H 4 n (L [1,−1])))


With these definition it is now straightforward to check that the left-hand-side of the lemma
equals:

       measure ?q {h. |R h − F2 xs| > ϵ ∗ F2 xs}


which can be shown to be at most 14 using Chebyshev’s inequality and the facts that:

   • The expectation of R is F2 xs.
   • The variance is at most ϵ^2 ∗ F2 xs^2/4.

Both results follow using the previously mentioned result about the expectation and variance of
example_2. The first one follows directly using linearity of expectations. The second condition
requires the application of Bienaymé’s identity, i.e., the variance of the sum of pairwise
independent random variables equals the sum of the variances of the random variables:

      lemma bienaymes_identity_pairwise_indep_2:9
       fixes f :: ′b ⇒ ′a ⇒ real
       assumes finite I
       assumes i. i ∈ I =⇒ f i ∈ borel_measurable M
               V

       assumes i. i ∈ I =⇒ integrable M (λω. f i ω^2)
               V

       assumes J. J ⊆ I =⇒ card J = 2 =⇒ indep_vars (λ_. borel) f J
               V

       shows variance (λω. ( i ∈ I. f i ω)) = ( i ∈ I. variance (f i))
                            P                  P



The above solution requires O(ϵ −2 (ln n+ln m)) bits of space. However, it is possible to improve
on that considerably because Bienaymé’s identity only requires pairwise independence, some-
thing we already know how to handle. Instead of choosing the seeds of the hash functions
independently, it is enough to choose them pairwise independently, which can again be done
using hash families. The following is the improved version, where we replaced the product
construction with the pseudorandom object for 2-independent hash families:


  9
      [KT23, Bienaymes_Identity]


                                                                                              83
                                            Emin Karayel


   fun example_5 :: nat ⇒ nat list ⇒ real pmf
     where example_5 n xs =
      do {
          let s = ⌈8/ϵ^2⌉;
          h ← sample_pro (H 2 s (H 4 n (L [1,−1])));
          return_pmf (( j<s. ( x ← xs. h j x)2 )/s)
                       P      P

      }

The correctness proof for example_5 and example_4 are, of course, very similar. The additional
lemmas [Kar22f, Pseudorandom_Objects_Hash_Families] needed in the proof include the fact
that the outer hash family is pairwise independent:

   lemma hash_pro_pmf_k_indep:
     assumes is_prime_power (pro_size S)
     shows prob_space.k_wise_indep_vars (sample_pro (H k n S)) k (λ_. discrete) (λi ω. ω i) {..<n}

and the fact that mapping to a specific component is like sampling directly from the inner
pseudorandom object.

   lemma hash_pro_pmf_component:
     assumes is_prime_power (pro_size S)
     assumes i < n
     assumes k > 0
     shows map_pmf (λf . f i) (sample_pro (H k n S)) = sample_pro S

The latter theorem illustrates a common approach when working with composed pseudoran-
dom objects. First a result is established for the inner pseudorandom object, then a theorem
like the above can be used to lift it to a statement for the combined object. Indeed, the
theorems about pseudorandom objects are specifically designed in a way that makes this
possible.
   Note that the resulting algorithm now requires only O(ln n + ϵ −2 ln m) bits. This algorithm
has a failure probability of 14 . In the next step, we would like to improve the failure probability.
   A straightforward method would be to increase the parameter s (the number of repetitions),
i.e., to obtain a mean of a larger sample. Indeed, by setting s = ⌈2ϵ −2 δ−1 ⌉, the algorithm
would return an ϵ-approximation with a probability of at least (1 − δ). However, there is a
much more efficient strategy.
   Let us first observe that the median of a sequence will be an ϵ-approximation if more
than half of the sequence elements are. (Note that under the assumption, when we sort


                                                                                                  84
                                Derandomization with pseudorandomness

the sequence, the sequence elements that are ϵ-approximations will form a consecutive
subsequence, whose length would be longer than half the length of the sequence. Thus,
the subsequence would necessarily include the median.) This is reflected in the following
theorem [Kar22e]:


   lemma median_est:
    assumes interval I
    assumes 2∗card {k. k < n ∧ f k ∈ I} > n
    shows median n f ∈I


In proofs the converse is more applicable:


   lemma median_est_rev: interval I =⇒ median n f ∈I
                                                  / =⇒ 2∗card {k. k<n∧f k ∈
                                                                          / I}≥n


Now, what we can do is to repeat the algorithm example_5 ⌈8 ln(δ−1 )⌉ times independently
and obtain the median:

   fun example_6 :: nat ⇒ nat list ⇒ real pmf
    where example_6 n xs =
     do {
         let s = ⌈8/ϵ^2⌉; let t = ⌈8∗ln (1/δ)⌉;
         h ← prod_pmf {0..<t} (λ_. sample_pro (H 2 s (H 4 n (L [1,−1]))));
         return_pmf (median t (λi. ( j<s. ( x ← xs. h i j x)2 )/s))
                                    P      P

     }


Because the failure probability of example_5 was 14 , the probability that more than half of
the t independent repetitions will fail (and hence the median) is at most exp(− 8t ) ≤ δ. This
follows from the one-sided version of Hoeffding’s inequality for {0, 1}-valued independent
random variables.
   The above leads to an algorithm with the space usage O(ln(δ−1 )(ln n+ϵ −2 ln m)). However,
even the above can be improved using the second pseudorandom object discussed in Section 6:
Random walks in expander graphs. In Section 6, we pointed out that they satisfy a similar
Chernoff bound. Hence, we can again replace the independent sampling with a pseudorandom
object. The result is the following algorithm:



                                                                                           85
                                               Emin Karayel


   fun example_7 :: nat ⇒ nat list ⇒ real pmf
    where example_7 n xs =
      do {
          let s = ⌈8/ϵ^2⌉; let t = ⌈8∗ln (1/δ)⌉;
          h ← sample_pro (E t (1/8) (H 2 s (H 4 n (L [1,−1]))));
          return_pmf (median t (λi. ( j<s. ( x ← xs. h i j x)2 )/s))
                                     P      P

      }

for which we can show:

   lemma example_7_correct:
    assumes set xs ⊆ {0..<n}
    shows P(ω in example_7. |ω − F2 xs| > ϵ ∗ F2 xs) ≤ δ

Let us briefly go through the main parts of the formalized proof:

   proof −

We set s, t as it is in the algorithm and introduce I the interval for the result:

    define s t where s_def : s = ⌈8/ϵ^2⌉ and t_def : t = ⌈32 ∗ ln (1/ δ)⌈
    define I where I = {ω. |ω − F2 xs| ≤ ϵ ∗ F2 xs}
    define R where R h = ( j<s. ( x ← xs. h x)2 )/s
                           P      P


   The random variable R represents the estimates from example_5 over the pseudorandom
object: H 2 s (H 4 n (L [1,−1])). Based on our previous observation, the random variable R
will be outside the desired interval with probability at most 14 .

    have measure (H 2 s (H 4 n (L [1,−1]))) {h. R h ∈
                                                    / I} ≤ 1/4

This can be stated as the expectation of an indicator variable:

                            / I) ∂ (H 2 s (H 4 n (L [1,−1]))) ≤ 1/4
            R
    hence ∗: h. of_bool(R h ∈


Let us introduce an abbreviation for the pseudorandom object of example_7. It represents
sampling using random walks from the pseudorandom object of example_5.

    let ?q = E t (1/8) (H 2 s (H 4 n (L [1,−1])))

Now we start an equation chain. First, we can express the left-hand-side as follows:


                                                                                       86
                             Derandomization with pseudorandomness


    have ?L = measure ?q {h. median t (λi. R (h i)) ∈
                                                    / I}

As mentioned earlier, the median can only be outside the interval if at least half of the
estimates are outside:
    also have ... ≤ measure ?q {h. ( j < t. of_bool(R (h j) ∈
                                                            / I))/t ≥ 1/2}
                                    P


The following step is critical. Using the Chernoff bound for expander walks, we can con-
clude that the probability that half of the estimates will be outside the interval is less than
exp(−2l(1/8)2 ). Here, we used the previous observation ∗.

    also have ... ≤ measure ?q {h. ( j < t. of_bool(R (h j) ∈
                                                            / I))/t − 1/4 ≥ 1/8 + 1/8}
                                    P

    also have ... ≤ exp(−2∗t∗(1/8)^2)

The right-hand side is less than δ, which concludes the proof.

    also have ... ≤ δ
    finally show ?thesis by simp
   qed

Note that the resulting algorithm has a space complexity of O(ln n + ϵ −2 ln(δ−1 ) ln m)for
n, m, δ−1 , ϵ −1 → ∞.
   In 1999, Alon et al. [AMS99, §2.2] presented a solution for the estimation of the second
frequency moment using O(ϵ −2 ln(δ−1 )(ln n+ln m)). That solution was relying only on a single
hash-family. This section demonstrates an asymptotically more space-efficient algorithm, and
its construction was possible simply by using additional pseudorandom objects. An optimal
solution, which also relies on k-independent hash families, for the above problem has been
found by Kane et al. [KNW10b], but only for a constant failure probability δ. Their solution
uses O(ln ln n + ϵ −2 ln m) bits, and even works for any (possibly fractional) frequency moment
Fk with 0 < k ≤ 2. It is possible to adapt their algorithm using the previously mentioned
median technique to achieve O(ln(δ−1 ) ln ln n + ln(δ−1 )ϵ −2 ln m) for non-constant δ. As far as
I know, an optimal solution with respect to all parameters ϵ, δ, n, m is not known. Note that,
it depends on the magnitude of n, δ, whether the algorithm we developed in this section is
preferable to the solution by Kane et al.
   The above was a minimal example to demonstrate how the library works and how com-
bining pseudorandom objects can be used to improve a randomized algorithm. In 2023,
I had presented the formalization of a space-optimal algorithm for the distinct elements
problem [Kar23b; Kar23c; Kar23a]. Since we are familiar with the notation, it makes sense
to replicate the pseudorandom object I used there:


                                                                                              87
                                             Emin Karayel


    E m α (E l Λ (H 2 n (G n_exp) × P H 2 n (N (C7 ∗b2 )) × P H k (C7 ∗b2 ) (N b)))


    A detailed explanation of all the parameters can be found in the source material [Kar23a].
However, this highlights that, depending on the algorithm, very different constructions may
be required and points out the importance of the flexibility of the library. The above uses
the pseudorandom primitive G n, which was not mentioned before. This primitive has a
geometric distribution, i.e., the probability of the value 0 is 12 , the probability of the value 1 is
1
4 etc.




8   Conclusion

    This work presents pseudorandom objects as versatile components in randomized algo-
rithms that can improve the asymptotic space and randomness complexity of randomized
algorithms. We discussed the mathematical foundations and the formal verification of two
such objects in depth: expander graphs and k-independent hash families.
    Novel in this work is the viewpoint that they can be represented as a composable library
that allows the construction of application-specific pseudorandom objects from primitive ones.
The notation introduced by this work allows the concise presentation of these algorithms
informally and formally in Isabelle/HOL. The high-level theorems provided by the library
allow small and easy proofs (even if complex pseudorandom objects are needed).
    Similarly, the formalization of a theory of efficient non-prime finite fields, or expander
graphs has—as far as I know—not been done before.
    The formalization of the space-optimal distinct elements problem [Kar23b; Kar23a]
highlights how this framework helps tackle advanced and complex randomized algorithms
(that required many decades of research to develop.)
    While this work has been done in Isabelle/HOL [NPW02], the approach is transferrable
to other theorem provers/checkers/proof assistants such as Agda, Rocq, Idris, Lean, etc.
However, depending on the proof assistant, this may require the development of additional
libraries for algebra, analysis, and probability theory.
    There is still much work that could be done in this field. In the context of expander graphs,
there are still important constructions that could be formalized. Another task is formalizing
Chernoff bounds for random walks in expander graphs for non-discrete functions [Gil98;
Lez98; RR17]. Beyond that, further pseudorandom objects, such as randomness extractors
and list-decodable codes, are open formalization tasks.


                                                                                                   88
                            Derandomization with pseudorandomness

Acknowledgements

   I would like to thank Tobias Nipkow, Yong Kiam Tan and the anonymous reviewers for
feedback and many insightful suggestions and remarks on earlier versions of this work.


References

[AL86]       L. M. Adleman and H. W. Lenstra. “Finding irreducible polynomials over fi-
             nite fields”. In: Proceedings of the Eighteenth Annual ACM Symposium on The-
             ory of Computing. STOC ’86. Berkeley, California, USA, 1986, 350–355. ISBN:
             0897911938. DOI: 10.1145/12130.12166.

[Adl78]      L. Adleman. “Two theorems on random polynomial time”. In: 19th Annual
             Symposium on Foundations of Computer Science (SFCS 1978). 1978, pages 75–83.
             DOI : 10.1109/SFCS.1978.37.

[Alo86]      N. Alon. “Eigenvalues and expanders”. In: Combinatorica 6 (1986), pages 83–96.
             DOI : 10.1007/BF02579166.

[AMS99]      N. Alon, Y. Matias, and M. Szegedy. “The Space Complexity of Approximating
             the Frequency Moments”. In: Journal of Computer and System Sciences 58.1
            (1999), pages 137–147. ISSN: 0022-0000. DOI: 10.1006/jcss.1997.1545.

[ASS08]      N. Alon, O. Schwartz, and A. Shapira. “An elementary construction of constant-
             degree expanders”. In: Combinatorics, Probability and Computing 17 (May 2008),
             pages 319–327. ISSN: 0963-5483. DOI: 10.1017/S0963548307008851.

[AS00]       N. Alon and J. H. Spencer. The Probabilistic Method. John Wiley & Sons, Ltd,
             2000.

[Afp]        Archive of Formal Proofs. https://isa-afp.org. Accessed: 2023-07-03.

[APM09]      P. Audebaud and C. Paulin-Mohring. “Proofs of randomized algorithms in Coq”.
             In: Science of Computer Programming 74.8 (2009). Special Issue on Mathematics
             of Program Construction (MPC 2006), pages 568–589. ISSN: 0167-6423. DOI:
             10.1016/j.scico.2007.09.002.

[Bao+22]     J. Bao, M. Gaboardi, J. Hsu, and J. Tassarotti. “A separation logic for negative
             dependence”. In: Proceedings of the ACM on Programming Languages 6 (2022),
             57:1–57:29. DOI: 10.1145/3498719.



                                                                                          89
                                       Emin Karayel

[BY+02]    Z. Bar-Yossef, T. S. Jayram, R. Kumar, D. Sivakumar, and L. Trevisan. “Counting
           Distinct Elements in a Data Stream”. In: Randomization and Approximation
           Techniques in Computer Science. Springer Berlin Heidelberg, 2002, pages 1–10.
           DOI : 10.1007/3-540-45726-7_1.

[BMD22]    K. Bhattacharjee, K. Maity, and S. Das. “A Search for Good Pseudo-random
           Number Generators: Survey and Empirical Studies”. In: Comput. Sci. Rev. 45
           (2022), page 100471. DOI: 10.1016/j.cosrev.2022.100471.

[Bł18]     J. Błasiok. “Optimal streaming and tracking distinct elements with high prob-
           ability”. In: Proceedings of the Twenty-Ninth Annual ACM-SIAM Symposium on
           Discrete Algorithms, SODA 2018. New Orleans, LA, USA, 2018, pages 2432–2448.
           DOI : 10.1137/1.9781611975031.156.

[Bł20]     J. Błasiok. “Optimal Streaming and Tracking Distinct Elements with High Prob-
           ability”. In: ACM Trans. Algorithms 16.1 (2020), 3:1–3:28. DOI: 10 . 1145 /
           3309193.

[Bla+17]   J. Blasiok, V. Braverman, S. R. Chestnut, R. Krauthgamer, and L. F. Yang. “Stream-
           ing symmetric norms via measure concentration”. In: Proceedings of the 49th
           Annual ACM SIGACT Symposium on Theory of Computing, STOC 2017, June
           19-23. Edited by H. Hatami, P. McKenzie, and V. King. Montreal, QC, Canada,
           2017, pages 716–729. DOI: 10.1145/3055399.3055424.

[BBS83]    L. Blum, M. Blum, and M. Shub. “Comparison of two pseudo-random number
           generators”. In: Advances in Cryptology: Proceedings of Crypto 82. Springer, 1983,
           pages 61–78. DOI: 10.1007/978-1-4757-0602-4_6.

[CVM22]    S. Chakraborty, N. V. Vinodchandran, and K. S. Meel. “Distinct Elements in
           Streams: An Algorithm for the (Text) Book”. In: 30th Annual European Sympo-
           sium on Algorithms (ESA 2022). Edited by S. Chechik, G. Navarro, E. Rotenberg,
           and G. Herman. Volume 244. Leibniz International Proceedings in Informatics
           (LIPIcs). Germany: Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 2022,
           34:1–34:6. ISBN: 978-3-95977-247-1. DOI: 10.4230/LIPIcs.ESA.2022.34.

[CCFC04]   M. Charikar, K. Chen, and M. Farach-Colton. “Finding frequent items in data
           streams”. In: Theoretical Computer Science 312.1 (2004). Automata, Languages
           and Programming, pages 3–15. ISSN: 0304-3975. DOI: 10.1016/S0304-3975(0
           3)00400-6.




                                                                                          90
                          Derandomization with pseudorandomness

[Cha+18]   K. Chatterjee, H. Fu, P. Novotný, and R. Hasheminezhad. “Algorithmic Analysis
           of Qualitative and Quantitative Termination Problems for Affine Probabilistic
           Programs”. In: ACM Trans. Program. Lang. Syst. 40.2 (May 2018). ISSN: 0164-
           0925. DOI: 10.1145/3174800.

[Che+21]   J. Chen, Q. Huang, I. Kanj, Q. Li, and G. Xia. “Streaming Algorithms for Graph
           k-Matching with Optimal or Near-Optimal Update Time”. In: 32nd International
           Symposium on Algorithms and Computation (ISAAC 2021). Edited by H.-K. Ahn
           and K. Sadakane. Volume 212. Leibniz International Proceedings in Informatics
           (LIPIcs). Germany: Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 2021,
           48:1–48:17. ISBN: 978-3-95977-214-3. DOI: 10.4230/LIPIcs.ISAAC.2021.48.

[Chu97]    F. R. K. Chung. Spectral Graph Theory. CBMS Regional Conference Series in
           Mathematics, 1997. DOI: 10.1090/cbms/092.

[Chu+12]   K.-M. Chung, H. Lam, Z. Liu, and M. Mitzenmacher. “Chernoff-Hoeffding Bounds
           for Markov Chains: Generalized and Simplified”. In: 29th International Sym-
           posium on Theoretical Aspects of Computer Science (STACS 2012). Edited by C.
           Dürr and T. Wilke. Volume 14. Leibniz International Proceedings in Informatics
           (LIPIcs). Germany: Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 2012,
           pages 124–135. ISBN: 978-3-939897-35-4. DOI: 10.4230/LIPIcs.STACS.2012.
           124.

[Com20]    T. mathlib Community. “The Lean mathematical library”. In: Proceedings of the
           9th ACM SIGPLAN International Conference on Certified Programs and Proofs.
           CPP 2020. New Orleans, LA, USA: Association for Computing Machinery, 2020,
           367–381. ISBN: 9781450370974. DOI: 10.1145/3372885.3373824.

[CDP21]    A. Czumaj, P. Davies, and M. Parter. “Graph Sparsification for Derandomizing
           Massively Parallel Computation with Low Space”. In: ACM Trans. Algorithms
           17.2 (June 2021). ISSN: 1549–6325. DOI: 10.1145/3451992.

[DeW+92]   D. J. DeWitt, J. F. Naughton, D. A. Schneider, and S. Seshadri. “Practical Skew
           Handling in Parallel Joins”. In: Proceedings of the 18th VLDB conference. Morgan
           Kaufmann Publishers Inc., 1992, pages 27–40. DOI: 10.5555/645918.672512.

[Div+20]   J. Divasón, S. J. C. Joosten, R. Thiemann, and A. Yamada. “A Verified Imple-
           mentation of the Berlekamp-Zassenhaus Factorization Algorithm”. In: J. Autom.
           Reason. 64.4 (2020), pages 699–735. DOI: 10.1007/S10817-019-09526-Y.



                                                                                        91
                                      Emin Karayel

[Div+16]   J. Divasón, S. J. C. Joosten, R. Thiemann, and A. Yamada. “The Factorization Al-
           gorithm of Berlekamp and Zassenhaus”. In: Archive of Formal Proofs (Oct. 2016).
           https://isa-afp.org/entries/Berlekamp_Zassenhaus.html, Formal proof
           development. ISSN: 2150-914x.

[EHN20]    M. Eberl, M. W. Haslbeck, and T. Nipkow. “Verified Analysis of Random Binary
           Tree Structures”. In: J. Autom. Reason. 64.5 (2020), pages 879–910. DOI: 10.
           1007/s10817-020-09545-0.

[EHN15]    M. Eberl, J. Hölzl, and T. Nipkow. “A Verified Compiler for Probability Density
           Functions”. In: Programming Languages and Systems. Springer Berlin Heidelberg,
           2015, pages 80–104. ISBN: 978-3-662-46669-8. DOI: 10.1007/978- 3- 662-
           46669-8_4.

[Ech22]    M. Echenim. “Simultaneous diagonalization of pairwise commuting Hermitian
           matrices”. In: Archive of Formal Proofs (July 2022). https://isa-afp.org/
           entries/Commuting_Hermitian.html, Formal proof development. ISSN: 2150-
           914x.

[FN85]     P. Flajolet and G. Nigel Martin. “Probabilistic counting algorithms for data
           base applications”. In: Journal of Computer and System Sciences 31.2 (1985),
           pages 182–209. ISSN: 0022-0000. DOI: 10.1016/0022-0000(85)90041-8.

[GG81]     O. Gabber and Z. Galil. “Explicit constructions of linear-sized superconcentra-
           tors”. In: Journal of Computer and System Sciences 22.3 (1981), pages 407–420.
           ISSN : 0022-0000. DOI : https://doi.org/10.1016/0022-0000(81)90040-4.

[Gil98]    D. Gillman. “A Chernoff Bound for Random Walks on Expander Graphs”. In:
           SIAM Journal on Computing 27.4 (1998), pages 1203–1220. DOI: 10.1137/
           S0097539794268765.

[Gir82]    M. Giry. “A categorical approach to probability theory”. In: Categorical Aspects
           of Topology and Analysis. Edited by B. Banaschewski. Springer Berlin Heidelberg,
           1982, pages 68–85. ISBN: 978-3-540-39041-1. DOI: 10.1007/BFb0092872.

[Gol11a]   O. Goldreich. “A Sample of Samplers: A Computational Perspective on Sam-
           pling", bookTitle = "Studies in Complexity and Cryptography. Miscellanea on
           the Interplay between Randomness and Computation: In Collaboration with
           Lidor Avigad, Mihir Bellare, Zvika Brakerski, Shafi Goldwasser, Shai Halevi, Tali
           Kaufman, Leonid Levin, Noam Nisan, Dana Ron, Madhu Sudan, Luca Trevisan,



                                                                                         92
                          Derandomization with pseudorandomness

           Salil Vadhan, Avi Wigderson, David Zuckerman”. In: edited by O. Goldreich.
           Springer Berlin Heidelberg, 2011, pages 302–332. ISBN: 978-3-642-22670-0.
           DOI : 10.1007/978-3-642-22670-0_24.

[Gol11b]   O. Goldreich. “Basic Facts about Expander Graphs”. In: Studies in Complexity
           and Cryptography. Miscellanea on the Interplay between Randomness and Compu-
           tation: In Collaboration with Lidor Avigad, Mihir Bellare, Zvika Brakerski, Shafi
           Goldwasser, Shai Halevi, Tali Kaufman, Leonid Levin, Noam Nisan, Dana Ron,
           Madhu Sudan, Luca Trevisan, Salil Vadhan, Avi Wigderson, David Zuckerman.
           Edited by O. Goldreich. Springer Berlin Heidelberg, 2011, pages 451–464. ISBN:
           978-3-642-22670-0. DOI: 10.1007/978-3-642-22670-0_30.

[Guf+11]   B. Gufler., N. Augsten., A. Reiser., and A. Kemper. “Handling data skew in MapRe-
           duce”. In: Proceedings of the 1st International Conference on Cloud Computing
           and Services Science - CLOSER. INSTICC. SciTePress, 2011, pages 574–583. DOI:
           10.5220/0003391105740583.

[Gur16]    V. Guruswami. Rapidly Mixing Markov Chains: A Comparison of Techniques (A
           Survey). 2016. arXiv: 1603.01512 [cs.DS].

[HN10]     F. Haftmann and T. Nipkow. “Code Generation via Higher-Order Rewrite Sys-
           tems”. In: Functional and Logic Programming, 10th International Symposium,
           FLOPS 2010, Sendai, Japan, April 19-21, 2010. Proceedings. Edited by M. Blume,
           N. Kobayashi, and G. Vidal. Volume 6009. Lecture Notes in Computer Science.
           Springer, 2010, pages 103–117. DOI: 10.1007/978-3-642-12251-4_9.

[Har05]    J. Harrison. “A HOL Theory of Euclidean Space”. In: Theorem Proving in Higher
           Order Logics. Edited by J. Hurd and T. Melham. Springer Berlin Heidelberg, 2005,
           pages 114–129. DOI: 10.1007/11541868_8.

[Höl16]    J. Hölzl. “Formalising Semantics for Expected Running Time of Probabilistic
           Programs”. In: Interactive Theorem Proving. Edited by J. C. Blanchette and S.
           Merz. Cham: Springer International Publishing, 2016, pages 475–482. ISBN:
           978-3-319-43144-4.

[Höl17]    J. Hölzl. “Markov chains and Markov decision processes in Isabelle/HOL”. In:
           Journal of Automated Reasoning 59.3 (2017), pages 345–387. DOI: 10.1007/
           s10817-016-9401-5.




                                                                                         93
                                      Emin Karayel

[HLW06]    S. Hoory, N. Linial, and A. Wigderson. “Expander Graphs and their Applications”.
           In: Bulletin of the American Mathematical Society 43.4 (2006), pages 439–561.
           DOI : 10.1090/s0273-0979-06-01126-8.

[HJ13]     R. A. Horn and C. R. Johnson. Matrix analysis. 2nd. Cambridge University Press,
           2013.

[HT23]     J. B. T. Houen and M. Thorup. “A Sparse Johnson-Lindenstrauss Transform Using
           Fast Hashing”. In: 50th International Colloquium on Automata, Languages, and
           Programming (ICALP 2023). Edited by K. Etessami, U. Feige, and G. Puppis.
           Volume 261. Leibniz International Proceedings in Informatics (LIPIcs). Germany:
           Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 2023, 76:1–76:20. ISBN:
           978-3-95977-278-5. DOI: 10.4230/LIPIcs.ICALP.2023.76.

[IR82]     K. Ireland and M. Rosen. A classical introduction to modern number theory.
           Volume 84. Graduate texts in mathematics. Springer, 1982. ISBN: 978-0-387-
           90625-6.

[JM85]     S Jimbo and A Maruoka. “Expanders obtained from affine transformations”.
           In: Proceedings of the Seventeenth Annual ACM Symposium on Theory of Com-
           puting. STOC ’85. Providence, Rhode Island, USA, 1985, pages 88–97. ISBN:
           0897911512. DOI: 10.1145/22145.22155.

[KNW10a]   D. M. Kane, J. Nelson, and D. P. Woodruff. “An Optimal Algorithm for the Distinct
           Elements Problem”. In: Proceedings of the Twenty-Ninth ACM SIGMOD-SIGACT-
           SIGART Symposium on Principles of Database Systems. PODS ’10. Indianapolis,
           Indiana, USA, 2010, pages 41–52. ISBN: 9781450300339. DOI: 10.1145/18070
           85.1807094.

[KNW10b]   D. M. Kane, J. Nelson, and D. P. Woodruff. “On the Exact Space Complexity
           of Sketching and Streaming Small Norms”. In: Proceedings of the Twenty-First
           Annual ACM-SIAM Symposium on Discrete Algorithms. SODA ’10. Austin, Texas:
           Society for Industrial and Applied Mathematics, 2010, pages 1161–1178. ISBN:
           9780898716986. DOI: 10.1137/1.9781611973075.93.

[Kar23a]   E. Karayel. An embarrassingly parallel optimal-space cardinality estimation algo-
           rithm. 2023. arXiv: 2307.00985 [cs.DS].




                                                                                         94
                          Derandomization with pseudorandomness

[Kar23b]   E. Karayel. “An Embarrassingly Parallel Optimal-Space Cardinality Estimation
           Algorithm”. In: Approximation, Randomization, and Combinatorial Optimization.
           Algorithms and Techniques (APPROX/RANDOM 2023). Edited by N. Megow and
           A. Smith. Volume 275. Leibniz International Proceedings in Informatics (LIPIcs).
           Germany: Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 2023, 35:1–35:22.
           ISBN : 978-3-95977-296-9. DOI : 10.4230/LIPIcs.APPROX/RANDOM.2023.35.

[Kar24]    E. Karayel. “Derandomization with Conditional Expectations”. In: Archive of
           Formal Proofs (Mar. 2024). https://isa- afp.org/entries/Derandomiza
           tion _ Conditional _ Expectations . html, Formal proof development. ISSN:
           2150-914x.

[Kar23c]   E. Karayel. “Distributed Distinct Elements”. In: Archive of Formal Proofs (Apr.
           2023). https://isa-afp.org/entries/Distributed_Distinct_Elements.
           html, Formal proof development. ISSN: 2150-914x.

[Kar23d]   E. Karayel. “Expander Graphs”. In: Archive of Formal Proofs (Mar. 2023). https:
           //isa-afp.org/entries/Expander_Graphs.html, Formal proof development.
           ISSN : 2150-914x.

[Kar22a]   E. Karayel. “Finite Fields”. In: Archive of Formal Proofs (June 2022). https:
           //isa-afp.org/entries/Finite _ Fields.html, Formal proof development.
           ISSN : 2150-914x.

[Kar22b]   E. Karayel. “Formalization of Randomized Approximation Algorithms for Fre-
           quency Moments”. In: Archive of Formal Proofs (Apr. 2022). https : / / isa -
           afp . org / entries / Frequency _ Moments . html, Formal proof development.
           ISSN : 2150-914x.

[Kar22c]   E. Karayel. “Formalization of Randomized Approximation Algorithms for Fre-
           quency Moments”. In: 13th International Conference on Interactive Theorem
           Proving (ITP 2022). Edited by J. Andronick and L. de Moura. Volume 237. Leib-
           niz International Proceedings in Informatics (LIPIcs). Germany: Schloss Dagstuhl
           – Leibniz-Zentrum für Informatik, 2022, 21:1–21:21. ISBN: 978-3-95977-252-5.
           DOI : 10.4230/LIPIcs.ITP.2022.21.

[Kar22d]   E. Karayel. “Interpolation Polynomials (in HOL-Algebra)”. In: Archive of Formal
           Proofs (Jan. 2022). https://isa-afp.org/entries/Interpolation_Polyno
           mials_HOL_Algebra.html, Formal proof development. ISSN: 2150-914x.




                                                                                        95
                                       Emin Karayel

[Kar22e]   E. Karayel. “Median Method”. In: Archive of Formal Proofs (Jan. 2022). https:
           //isa-afp.org/entries/Median _ Method.html, Formal proof development.
           ISSN : 2150-914x.

[Kar22f]   E. Karayel. “Universal Hash Families”. In: Archive of Formal Proofs (Feb. 2022).
           https://isa-afp.org/entries/Universal _ Hash _ Families.html, Formal
           proof development. ISSN: 2150-914x.

[KE23]     E. Karayel and M. Eberl. “Executable Randomized Algorithms”. In: Archive of
           Formal Proofs (June 2023). https://isa- afp.org/entries/Executable _
           Randomized_Algorithms.html, Formal proof development. ISSN: 2150-914x.

[KT23]     E. Karayel and Y. K. Tan. “Concentration Inequalities”. In: Archive of Formal
           Proofs (Nov. 2023). https://isa-afp.org/entries/Concentration_Inequa
           lities.html, Formal proof development. ISSN: 2150-914x.

[KLN06]    M. Kassabov, A. Lubotzky, and N. Nikolov. “Finite simple groups as expanders”.
           In: Proceedings of the National Academy of Sciences 103.16 (2006), pages 6116–
           6119. DOI: 10.1073/pnas.0510337103.

[Kun16]    O. Kunčar. “Types, abstraction and parametric polymorphism in higher-order
           logic”. PhD thesis. Technische Universität München, 2016. URL: https://nbn-
           resolving.org/urn:nbn:de:bvb:91-diss-20160408-1285267-1-5.

[KP16]     O. Kunčar and A. Popescu. “From Types to Sets by Local Type Definitions in
           Higher-Order Logic”. In: Interactive Theorem Proving. Edited by J. C. Blanchette
           and S. Merz. Cham: Springer International Publishing, 2016, pages 200–218.
           ISBN : 978-3-319-43144-4. DOI : 10.1007/978-3-319-43144-4_13.

[Lee24]    J. R. Lee. On expanders from the action of GL(2,Z). 2024. arXiv: 1301.6296
           [math.CO].

[Lez98]    P. Lezaud. “Chernoff-type bound for finite Markov chains”. In: The Annals of
           Applied Probability 8.3 (1998), pages 849–867. DOI: 10.1214/aoap/102890345
           3.

[LN86]     R. Lidl and H. Niederreiter. Introduction to Finite Fields and Their Applications.
           USA: Cambridge University Press, 1986. ISBN: 0521307066.




                                                                                          96
                          Derandomization with pseudorandomness

[Loc16]    A. Lochbihler. “Probabilistic Functions and Cryptographic Oracles in Higher
           Order Logic”. In: Programming Languages and Systems. Edited by P. Thiemann.
           Berlin, Heidelberg: Springer, 2016, pages 503–531. ISBN: 978-3-662-49498-1.
           DOI : 10.1007/978-3-662-49498-1_20.

[Loc17]    A. Lochbihler. “Probabilistic while loop”. In: Archive of Formal Proofs (May 2017).
           https://isa-afp.org/entries/Probabilistic_While.html, Formal proof
           development. ISSN: 2150-914x.

[Lub11]    A. Lubotzky. “Expander graphs in pure and applied mathematics”. In: Bulletin
           of the American Mathematical Society 49 (2011), pages 113–162. DOI: 10.1090/
           S0273-0979-2011-01359-3.

[LPS88]    A. Lubotzky, R. Phillips, and P. Sarnak. “Ramanujan graphs”. In: Combinatorica
           8.3 (1988), pages 261–277. DOI: 10.1007/BF02126799.

[MSS15]    A. W. Marcus, D. A. Spielman, and N. Srivastava. “Interlacing families I: Bipartite
           Ramanujan graphs of all degrees”. In: Annals of Mathematics 182.1 (2015),
           pages 307–325. ISSN: 0003486X. DOI: 10.4007/annals.2015.182.1.7. (Vis-
           ited on 04/04/2024).

[Mar73]    G. A. Margulis. “Explicit constructions of concentrators”. In: Problemy Peredachi
           Informatsii 9.4 (1973), pages 71–80.

[MN98]     M. Matsumoto and T. Nishimura. “Mersenne twister: a 623-dimensionally equidis-
           tributed uniform pseudo-random number generator”. In: ACM Trans. Model.
           Comput. Simul. 8.1 (Jan. 1998), 3–30. ISSN: 1049-3301. DOI: 10.1145/272991.
           272995.

[McK81]    B. D. McKay. “The expected eigenvalue distribution of a large regular graph”. In:
           Linear Algebra and its Applications 40 (1981), pages 203–216. ISSN: 0024-3795.
           DOI : 10.1016/0024-3795(81)90150-6.

[MP13]     G. L. Mullen and D. Panario. Handbook of Finite Fields. 1st. Chapman & Hall/CRC,
           2013. ISBN: 143987378X. DOI: 10.5555/2555843.

[Mur+19]   J. Murtagh, O. Reingold, A. Sidford, and S. Vadhan. “Deterministic Approxi-
           mation of Random Walks in Small Space”. In: Approximation, Randomization,
           and Combinatorial Optimization. Algorithms and Techniques (APPROX/RANDOM
           2019). Edited by D. Achlioptas and L. A. Végh. Volume 145. Leibniz Interna-
           tional Proceedings in Informatics (LIPIcs). Germany: Schloss Dagstuhl–Leibniz-


                                                                                           97
                                       Emin Karayel

          Zentrum fuer Informatik, 2019, 42:1–42:22. ISBN: 978-3-95977-125-2. DOI:
          10.4230/LIPIcs.APPROX-RANDOM.2019.42.

[NPW02]   T. Nipkow, L. C. Paulson, and M. Wenzel. Isabelle/HOL: A Proof Assistant for
          Higher-Order Logic. First. Volume 2283. Lecture Notes in Computer Science.
          Berlin, Heidelberg: Springer-Verlag, 2002. ISBN: 978-3540433767.
[Nos14]   L. Noschinski. “A Graph Library for Isabelle”. In: Mathematics in Computer Science
          9 (2014), pages 23–39. DOI: 10.1007/s11786-014-0183-z.
[Nos13]   L. Noschinski. “Graph Theory”. In: Archive of Formal Proofs (Apr. 2013). https:
          //isa- afp.org/entries/Graph _ Theory.html, Formal proof development.
          ISSN : 2150-914x.

[O’N14]   M. E. O’Neill. PCG: A Family of Simple Fast Space-Efficient Statistically Good
          Algorithms for Random Number Generation. Technical report HMC-CS-2014-
          0905. Claremont, CA: Harvey Mudd College, Sept. 2014. URL: https://www.
          cs.hmc.edu/tr/hmc-cs-2014-0905.pdf.

[Pau94]   L. C. Paulson. Isabelle: A Generic Theorem Prover. Berlin, Heidelberg: Springer-
          Verlag, 1994. ISBN: 978-3-540-48586-5. DOI: 10.1007/BFb0030541.
[PRB69]   W. H. Payne, J. R. Rabung, and T. P. Bogyo. “Coding the Lehmer pseudo-random
          number generator”. In: Commun. ACM 12.2 (Feb. 1969), 85–86. ISSN: 0001-
          0782. DOI: 10.1145/362848.362860.
[Rab80]   M. O. Rabin. “Probabilistic Algorithms in Finite Fields”. In: SIAM Journal on
          Computing 9.2 (1980), pages 273–280. DOI: 10.1137/0209024.
[RR17]    S. Rao and O. Regev. A Sharp Tail Bound for the Expander Random Sampler. 2017.
          arXiv: 1703.10205 [math.PR].
[RVW00]   O. Reingold, S. Vadhan, and A. Wigderson. “Entropy waves, the zig-zag graph
          product, and new constant-degree expanders and extractors”. In: Proceedings
          41st Annual Symposium on Foundations of Computer Science. 2000, pages 3–13.
          DOI : 10.1109/SFCS.2000.892006.

[Sch24]   C. Schwarzweller. “Finite Fields”. In: Formalized Mathematics 32.1 (2024),
          pages 289–302. DOI: 10.2478/forma-2024-0024.
[SA23]    M. Schäffeler and M. Abdulaziz. “Formally Verified Solution Methods for Markov
          Decision Processes”. In: Proceedings of the AAAI Conference on Artificial Intelligence
          37.12 (June 2023), pages 15073–15081. DOI: 10.1609/aaai.v37i12.26759.


                                                                                             98
                          Derandomization with pseudorandomness

[Sho88]    V. Shoup. “New algorithms for finding irreducible polynomials over finite fields”.
           In: [Proceedings 1988] 29th Annual Symposium on Foundations of Computer
           Science. 1988, pages 283–290. DOI: 10.1109/SFCS.1988.21944.

[SSK20]    M. Singh, P. Singh, and P. Kumar. “An Empirical Study of Non-Cryptographically
           Secure Pseudorandom Number Generators”. In: 2020 International Conference
           on Computer Science, Engineering and Applications (ICCSEA). 2020, pages 1–6.
           DOI : 10.1109/ICCSEA49143.2020.9132873.

[Sun+23]   Y. Sun, H. Fu, K. Chatterjee, and A. K. Goharshady. “Automated Tail Bound
           Analysis for Probabilistic Recurrence Relations”. In: Computer Aided Verifica-
           tion. Edited by C. Enea and A. Lal. Cham: Springer Nature Switzerland, 2023,
           pages 16–39. ISBN: 978-3-031-37709-9. DOI: 10.1007/978-3-031-37709-9_2.

[TY24]     Y. K. Tan and J. Yang. “Approximate Model Counting”. In: Archive of Formal
           Proofs (Mar. 2024). https://isa- afp.org/entries/Approximate _ Model _
           Counting.html, Formal proof development. ISSN: 2150-914x.

[Tan+24]   Y. K. Tan, J. Yang, M. Soos, M. O. Myreen, and K. S. Meel. “Formally Certified
           Approximate Model Counting”. In: Computer Aided Verification. Edited by A.
           Gurfinkel and V. Ganesh. Cham: Springer Nature Switzerland, 2024, pages 153–
           177. ISBN: 978-3-031-65627-9. DOI: 10.1007/978-3-031-65627-9_8.

[TH18]     J. Tassarotti and R. Harper. “Verified Tail Bounds for Randomized Programs”.
           In: Interactive Theorem Proving. Edited by J. Avigad and A. Mahboubi. Cham:
           Springer International Publishing, 2018, pages 560–578. ISBN: 978-3-319-94821-
           8. DOI: 10.1007/978-3-319-94821-8_33.

[Tas+21]   J. Tassarotti, K. Vajjha, A. Banerjee, and J.-B. Tristan. “A formal proof of PAC
           learnability for decision stumps”. In: Proceedings of the 10th ACM SIGPLAN
           International Conference on Certified Programs and Proofs. CPP 2021. Virtual,
           Denmark, 2021, pages 5–17. ISBN: 9781450382991. DOI: 10.1145/3437992.
           3439917. URL: https://doi.org/10.1145/3437992.3439917.

[Thi21]    R. Thiemann. “A Perron—Frobenius theorem for deciding matrix growth”. In:
           Journal of Logical and Algebraic Methods in Programming 123 (2021). ISSN:
           2352-2208. DOI: 10.1016/j.jlamp.2021.100699.




                                                                                          99
                                      Emin Karayel

[TY16]    R. Thiemann and A. Yamada. “Formalizing Jordan normal forms in Isabelle/HOL”.
          In: Proceedings of the 5th ACM SIGPLAN Conference on Certified Programs and
          Proofs. CPP 2016. St. Petersburg, FL, USA: Association for Computing Machinery,
          2016, 88–99. ISBN: 9781450341271. DOI: 10.1145/2854065.2854073.

[Thi17]   R. Thiemann. “Stochastic Matrices and the Perron-Frobenius Theorem”. In:
          Archive of Formal Proofs (Nov. 2017). https://isa-afp.org/entries/Stocha
          stic_Matrices.html, Formal proof development. ISSN: 2150-914x.

[TY15]    R. Thiemann and A. Yamada. “Matrices, Jordan Normal Forms, and Spectral
          Radius Theory”. In: Archive of Formal Proofs (Aug. 2015). https://isa-afp.
          org/entries/Jordan _ Normal _ Form.html, Formal proof development. ISSN:
          2150-914x.

[Vad12]   S. P. Vadhan. “Pseudorandomness”. In: Foundations and Trends® in Theoretical
          Computer Science 7.1-3 (2012), pages 1–336. ISSN: 1551-305X. DOI: 10.1561/
          0400000010.

[VP20]    P. E. de Vilhena and L. C. Paulson. “Algebraically Closed Fields in Isabelle/HOL”.
          In: Automated Reasoning: 10th International Joint Conference, IJCAR 2020, Paris,
          France, July 1–4, 2020, Proceedings, Part II. Paris, France: Springer-Verlag, 2020,
          204–220. ISBN: 978-3-030-51053-4. DOI: 10.1007/978-3-030-51054-1_12.

[WC81]    M. N. Wegman and J. L. Carter. “New hash functions and their use in authentica-
          tion and set equality”. In: Journal of Computer and System Sciences 22.3 (1981),
          pages 265–279. ISSN: 0022-0000. DOI: 10.1016/0022-0000(81)90033-7.




                                                                                         100
                             Derandomization with pseudorandomness

A   AFP entries

    The following list summarizes the AFP entries that contain the results and definitions for
pseudorandom objects, with a total of 16365 LoC.

Finite Fields [Kar22a]
 Formalization of finite fields and algorithms for efficient computations in and constructions
 of them. (7173 LoC)
Interpolation Polynomials (in HOL-Algebra) [Kar22d]
 Existence and count of interpolation polynomials for a given set of points and degree bound.
 This is used in the construction of hash families. (712 LoC)
Universal Hash Families [Kar22f]
 Formalization and construction of k-independent hash families as pseudrandom objects.
 Section 5 summarizes this AFP entry. (1435 LoC)
Expander Graphs [Kar23d]
 Formalization and construction of (strongly explicit) expander graphs. Section 6 summarizes
 this AFP entry. (7054 LoC)

The following list summarizes some AFP entries relevant for the verification of randomized
algorithms:

Median Method [Kar22e]
 Concept of the median (and order statistics in general) and their properties as a random
 variable. It verifies that order statistics are measurable. In particular, it contains the results
 about the median, we used in Section 7. (484 LoC)
Concentration Inequalities [KT23]
 Joint work with Yong Kiam Tan. Collection of advanced concentration inequalities, such as
 the Efron–Stein or Paley–Zygmund inequality. Includes also Bienaymé’s identity, which we
 used in Section 7. (2019 LoC)

The following entries are verifications of randomized algorithms that rely on pseudorandom
objects:

Distributed Distinct Elements [Kar23c]
 Verification of a space-optimal cardinality estimation algorithm [Kar23b; Kar23a]. (4981
 LoC)
Formalization of Randomized Approximation Alg. for Frequency Moments [Kar22b]
 Verification of several approximation algorithms for frequency moments on streams [Kar22c].
 (3791 LoC)


                                                                                               101
                                      Emin Karayel

Approximate Model Counting [TY24]
 By Yong Kiam Tan and Jiong Yang. Verification of a randomized approximation algorithm
 for the count of satisfying assignments to a boolean formula [Tan+24]. It relies on the
 construction of a 3-universal XOR-hash-family. (See also [TY24, RandomXORHashFamily].)
 (5890 LoC)




                                                                                    102
