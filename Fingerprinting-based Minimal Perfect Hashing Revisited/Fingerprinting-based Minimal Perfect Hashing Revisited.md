# Fingerprinting-Based Minimal Perfect Hashing Revisited

PIOTR BELING, Faculty of Mathematics and Computer Science, University of Łódź, Poland In this paper we study a fingerprint-based minimal perfect hash function (*FMPH* for short). While FMPH is not as space-efficient as some other minimal perfect hash functions (for example RecSplit, CHD, or PTHash), it has a number of practical advantages that make it worthy of consideration. FMPH is simple and quite fast to evaluate. Its construction requires very little auxiliary memory, takes a short time and, in addition, can be parallelized or carried out without holding keys in memory.

In this paper, we propose an effective method (called **FMPHGO**) that reduces the size of FMPH, as well as a number of implementation improvements. In addition, we experimentally study FMPHGO performance and find the best values for its parameters. Our benchmarks show that with our method and an efficient structure to support the rank queries on a bit vector, the FMPH size can be reduced to about 2.1 bits/key, which is close to the size achieved by state-of-the-art methods and noticeably larger only compared to RecSplit. FMPHGO
preserves most of the FMPH advantages mentioned above, but significantly reduces its construction speed.

However, FMPHGO's construction speed is still competitive with methods of similar space efficiency (like CHD or PTHash), and seems to be good enough for practical applications.

CCS Concepts: - Theory of computation → **Data structures design and analysis**; - **Information systems** → Data structures; Additional Key Words and Phrases: Minimal perfect hashing, data structures, algorithms ACM Reference format:
Piotr Beling. 2023. Fingerprinting-based Minimal Perfect Hashing Revisited. *ACM J. Exp. Algor.* 28, 1, Article 1.4 (June 2023), 16 pages.

https://doi.org/10.1145/3596453

## 1 Introduction And Related Work

A **minimal perfect hash function (MPHF)** is a bijection from a key set K to the set {0, 1,... |K|−
1}. Such function can be constructed for any set K (given in advance) and represented using (the theoretical lower bound) 1.44 bits per key [1, 9, 16]. The best known practical methods are: **Recursive Splitting (RecSplit)** [7] (whose representation sizes is about 1.8 bits/key), Compress, Hash and Displace (CHD) [1] (about 2.1 bits/key), **Pibiri-Trani Hash (PTHash)** [15] (about 2.2 bits/key), **Genuzio, Ottaviano, Vigna (GOV)** [10] (about 2.2 bits/key), BDZ [3, 4] (about 2.6 bits/key), and fingerprint-based MPHF [5, 12, 13] (about 3 bits/key). All of them are fast. Their expected construction and evaluation times are O(|K|) (slightly higher in the case of PTHash) and O(1), respectively.

In this paper, we present an improvement to fingerprint-based MPHF (*FMPH* for short).

FMPH was proposed in [5], independently in [13], revisited in [12], and described in Section 3.

Author's address: P. Beling, Faculty of Mathematics and Computer Science, University of Łódź, 90-238, Banacha 22, Łódź, Poland; email: piotr.beling@wmii.uni.lodz.pl. Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

© 2023 Copyright held by the owner/author(s). Publication rights licensed to ACM.

1084-6654/2023/06-ART1.4 $15.00 https://doi.org/10.1145/3596453 While FMPH is not as space-efficient as the other methods mentioned, it is simple and can be quickly constructed with almost no auxiliary memory. As shown in [12], the construction can also be carried out using multiple threads and without keeping the keys in memory. Thanks to the aforementioned features, the authors of [12] constructed FMPH for a huge set of 1012 keys (using 637 GB of RAM during construction). As far as we know, no other MPHF has yet been constructed for such a large set. Moreover, benchmarks presented in [7, 12, 15] and in Section 7 suggest that FMPH is quite fast to evaluate (admittedly slower than PTHash, but faster than RecSplit, which is in turn faster than CHD). Additionally, as the benchmarks in Sections 6 and 7 show, the improvements we propose in Section 4 allow FMPH to have a size close to state-of-the-art methods and be noticeably larger only in comparison to RecSplit.

We describe FMPH in detail in Section 3, and summarize other practical MPHFs in Section 2.

Our contribution begins in Section 4 where we describe the improvement (called **Fingerprint**
based perfect hashing with group optimization (FMPHGO)) of FMPH which can reduce its size. Section 5 provides implementation notes on FMPH and FMPHGO. In Sections 6 and 7, we experimentally study FMPHGO performance, find the best values for its parameters, and compare it to other MPHFs. Section 8 contains conclusions and potential directions for further work. Our implementations of FMPH and FMPHGO are available at https://github.com/beling/bsuccinct-rs.

## 2 Related Work - Practical Minimal Perfect Hash Functions

RecSplit [7] is based on an observation that for very small sets an MPHF can be efficiently found simply by brute-force searching for a bijection in a family of fully random independent hash functions h0,h1,... with suitable codomain. (In fact, we use similar fact in Section 4 to improve FMPH.)
To build an MPHF for a larger input set of keys, RecSplit splits this set into smaller ones, using random hash functions. First, one of these functions distributes keys randomly into buckets of average size b. Next, buckets are recursively split (by finding a function that splits it into approximately equal parts) until they reach a target size  on which it is feasible to find an MPHF by bruteforce. The resulting rooted trees of splittings (defined by indices of hash functions that provide appropriate splits in interior nodes and bijections in leaves) are stored using integer compression techniques. As a result, RecSplit offers excellent size efficiency, but at the cost of being complex and an evaluation time overhead (caused by the tree traversal and integer decompression). Its b and parameters affect the trade-off between its size and the speed of its construction and evaluation.

CHD [1] and PTHash [15] use *hash and displace* technique originally introduced by Fox, Chen, and Heath [8]. Similar to RecSplit, they first distribute the keys into buckets. However, PTHash does so in a way that results in a more uneven expected distribution. Next, the buckets are sorted and processed by decreasing size. For each bucket, a function is found that maps the keys contained in the bucket to indices 0,...,n − 1 (where n ≥ |K|), without causing collisions with other keys from the current and previous buckets. The MPHF is determined by the indices describing the functions found. Additionally, if n > |K| (which is always the case for CHD), then some of the indices 0,...,n − 1 are left unused and a description of the mapping of the used indices to 0,..., |K| −1 (which are the final values that MPHF assigns to the keys) is also stored. Again, integer compression is used to make MPHF compact. CHD and PTHash differ in details. In contrast to CHD, PTHash is designed with great concern for evaluation speed. Benchmarks in [15] (as well as those in Section 7) show that occupying only about 10% more space, PTHash can be around four times faster than CHD.

BDZ [3, 4] findsw0,...,wn−1 (wi ∈ {0, 1, 2} for all i) such that hj(k) (k) is different for each k ∈ K
and j(k) = wh0 (k) +wh1 (k) +wh2 (k) mod 3, where h0, h1, h2 are random hash functions that map K
to {0,...,n − 1}. (It is also possible to use a different number of hash functions, but 3 is optimal.)
For n ≈ 1.23|K|, BDZ is able to almost always solve the above linear system (if not, it tries again

![2_image_0.png](2_image_0.png)

Fig. 1. Example construction of a fingerprint-based minimal perfect hash function for the following keys:

![2_image_1.png](2_image_1.png)

a,b,c,d, e, f ,д. First, all members of the input set K0 = {a,b,c,d, e, f ,д} are mapped by h0 to indices of A0.

Only the bits of A0 assigned to f , b, and e are set to 1, as these keys are the only ones which do not collide with any other key (i.e., which are mapped to unique indices of A0). The other keys (K1 = {a,c,d,д}) are hashed by h1 to indices of A1. Keys д and d are uniquely placed and thus the bits of A1 assigned to them are set to 1. Since keys a and c collide, K2 = {a,c}. Because h2 assigns them distinct indices of A2, the process ends. Figure 2 shows an example of determining a value of the constructed function.
Fig. 2. Calculating H(д), where H is the fingerprint-based minimal perfect hash function whose construction is shown in Figure 1. A is the concatenation of A0, A1, and A2. First, the algorithm checks if A0[h0 (д)] = 1.

As it is not, the algorithm tests if A1[h1 (д)] = 1. Since this is true, the process ends. H(д) is calculated as the number of ones in A that precede the position corresponding to the position h1 (д) of A1.

with different hash functions) in linear time using hypergraph peeling. Having w0,...,wn−1, BDZ
can map each k ∈ K to unique index hj(k) (k) of {0,...,n−1}. However, since n > |K|, some indices are left unused and a description of the mapping of the used indices to 0,..., |K| − 1 (which are the final values that MPHF assigns to the keys) is also stored. GOV [10] is similar to BDZ, but uses Gaussian elimination technique (with many practical improvements) to solve the linear system for n ≈ 1.01|K|. However, since Gaussian elimination is much slower than graph peeling, GOV
distributes the keys into buckets and solves a number of smaller systems separately.

## 3 Fingerprint-Based Minimal Perfect Hash Function (Fmph)

Let h0,h1,... be independent, not necessarily perfect hash functions that can map keys to natural numbers in the range from 0 to a desired value and (at least approximately) satisfy the uniform hashing assumption. The following algorithm constructs a fingerprint-based minimal perfect hash function for a given key set K (Figure 1 shows an example):
Let K0 = K. For successive level numbers l = 0, 1,...:
(1) Use hash function hl : Kl → [0, |Al | − 1] to map all keys from Kl to indices of bit array Al .

Set i-th ∈ {0,..., |Al | − 1} bit of Al to 1 if and only if hl (k) = i for exactly one k ∈ Kl (i.e.,
when k does not collide with any other key).

|Al | should be greater or equal to |Kl |.

(2) Calculate the set of keys to be hashed at the next levels: Kl+1 = {k ∈ Kl : Al[hl (k)] = 0}.

(3) Stop if Kl+1 = ∅. The result is defined by the sequence A0,A1,...,Al .

LetA be the bit array which is the concatenation ofA0,A1,...,Al . By construction,A has exactly |K| bits set to 1, and each such bit corresponds to exactly one key in K. The evaluation (Figure 2 shows an example, and Figure 3 shows pseudocode) for any argument k starts with finding the Fig. 3. Pseudo-code of FMPH (see Section 3) and FMPHGO (see Section 4) evaluation. FMPHGO uses (in step 1) a specific hl function whose pseudocode is shown in Figure 5.

index i of the bit corresponding to k, i.e., it starts with finding the lowest level numberl, such that Al[hl (k)] = 1 or, equivalently, such that A[i] = 1, where i = -l−1 p=0 |Ap | + hl (k). Next, rank(A,i) is returned, where rank(A,i) = -i−1 b=0 A[b] is the number of ones in A, up to position i, excluded.

The final representation of the constructed hash function consists of: either A or A0,A1,...,Al and the auxiliary structure to support fast rank queries on A (possible implementations of such a structure are discussed for example in [11, 19]).

Based on the reasoning given in [5], the authors of [12] prove that if γ ≥ 1 and |Al | = γ |Kl | at each level l, then the expected number of keys which do not collide at level l is |Kl |e−1/γ . Then |Kl | = |Kl−1 |(1 − e−1/γ ) and |Al | = γ |Kl | = γ |Kl−1 |(1 − e−1/γ ) = γ |K0 |(1 − e−1/γ )
l. Finally, the expected length of A is -l |Al | = γ |K|-l (1 − e−1/γ )
l = γ |K| 1 1−(1−e−1/γ ) = γ e1/γ |K| bits (note that 0 < 1 − e−1/γ < 1 for γ ≥ 1). It is minimal when |Al | = |Kl | at each level l [5, 12]. However, one can use larger Al arrays to reduce the total number of levels and therefore speed-up expected construction and evaluation times.

Since the sizes of subsequent levels are expected to decrease at a geometric rate, the expected number of levels (and thus the maximum number of levels visited during the evaluation) is Θ(log |K|), the expected average (over all keys) number of levels visited during evaluation is O(1), and the expected construction time is Θ(|K|). Note that many implementations do not allow level sizes to drop below a certain threshold, for example [5] recommends the threshold of about 1000, while our implementation rounds up the sizes of all levels to multiples of 64.

The construction algorithm is fast and requires very little auxiliary memory (which is especially true for our implementation), as confirmed by both ours (see Section 7) and previous studies, such as those presented in [12]. To build the l-th level, an auxiliary arrayCl (indicating which Al indices are subject to collision) of size |Al | bits is often sufficient (additional memory may be needed to represent the sets K1,K2,..., which is discussed in Section 5.2). Moreover, theCl array can be freed as soon as the level is constructed and the memory can be reused for the next levels. Furthermore, the keys can be distributed among multiple threads, which can populate the Al and Cl arrays in parallel, using the atomic memory access instructions available on modern CPUs. Such a parallelization method is used by the authors of [12] and also by the implementations tested in Section 7.

## 4 Fingerprint Based Perfect Hashing With Group Optimization (Fmphgo)

The size of the minimal perfect hash function described in Section 3 can be reduced by optimizing the hash functions h0,h1,.... To do this efficiently, we propose to divide the levels into groups and for each group choose a hash function (one of several) that minimizes the number of collisions
(Figure 4 shows an example). At each level l, each group covers b consecutive bits of Al (b is a parameter of our construction) and the l-th level consists of nl groups (so |Al | = nlb; note that it is reasonable to choose nl = |Kl |/b, as then |Al |≥|Kl | and |Al |≈|Kl |). The function hl which assigns an index of Al to any key k is of the form hl (k) = bд + dl,д (k),

![4_image_0.png](4_image_0.png)

Fig. 4. Example construction of a fingerprint based perfect hash function with group optimization (with groups of size b = 2 bits and r = 2s = 21 = 2) for the following keys: a,b,c,d, e, f ,д. First, the function д0 assigns the following group numbers to the keys in the set K0 = {a,b,c,d, e, f ,д}: д0 (a) = д0 (d) = 0, д0 (f ) = 1, д0 (c) = д0 (д) = 2, д0 (b) = д0 (e) = 3. Next, functions f0,0 and f0,1 map the keys to indices inside the groups. In group 0, the function f0,0 performs better than f0,1 (in contrast to f0,1, f0,0 maps both keys, a and d, without collisions). That is whyG0[0] = 0 and the A0 bits in group 0 are set according to f0,0. In group 1, both functions f0,0 and f0,1 work equally well. G0[1] might as well be 0 or 1. In the example, G[1] = 0 and the A0 bits in group 1 are set according to f0,0. In groups 2 and 3, function f0,1 performs better than f0,0.

Therefore, G[2] = G[3] = 1 and the A0 bits in both these groups are set according to f0,1. The function д0 together with the functions indicated byG assign distinct indices of A0 to all keys contained in K0. Therefore, further levels are not needed and the construction process ends.
Fig. 5. Pseudocode for calculating hl (k) during FMPHGO evaluation, in step 1 of the pseudocode shown in Figure 3.

where:
- д = дl (k) is the number of the group assigned to key k at level l (by the function дl : K →
{0,...,nl − 1}; д0,д1,... are independent hash functions),
- and dl,д (k) is the index of k inside the group (dl,д : K → {0,...,b − 1}).

For each level l and group д, the function dl,д is selected from the family of independent hash functions fl,0,..., fl,r−1 (where r = 2s , and s is a parameter of our construction) in such a way as to minimize the number of collisions in group д at level l. The selection of the optimal function among fl,0,..., fl,r−1 is done by examining them all. The index of the selected function (0, or 1,...,
or r − 1) is kept under the index д of the array Gl , i.e., dl,д = fl,Gl[д]. The array Gl consists of nl s-bit integers, so its total size is nls bits. The arrays G0,G1,... (or their concatenation) are part of the final representation of the constructed minimal perfect hash function. These arrays are read during evaluation, as can be seen in pseudocode shown in Figures 3 and 5.

Although selecting the optimal dl,д functions requires examining r hash functions fl,0,..., fl,r−1, we do not expect the total construction time to increase as much asr times. The reason is that many other operations are still performed only once (for example, building the structure to support rank queries), or once per level (for example, removing elements from the set of remaining keys). Moreover, thanks to the optimization, the sizes of successive sets of keys K1,K2,...,
and thus the amount of work, should drop faster. The number of levels built may decrease too.

## 5 Fmph/Fmphgo Implementation Notes 5.1 Efficient Hash Function And Structure To Support The Rank Queries 5.2 Storing A Subset Of Keys 5.3 Pre-Hashing In Fmphgo, Hash Caching In Fmph And Fmphgo

Our FMPH and FMPHGO implementations use the very fast *wyhash* [18] algorithm initialized with different seeds as a family of random hash functions. The same algorithm is used by Patrick Marks in his FMPH implementation called *boomphf*.

To support fast rank queries, our FMPH and FMHGO implementations use a very compact structure based on the ideas described in [19]. Its memory overhead is only about 3.2%. In contrast, boomphf uses the same structure as authors of [12], which is simpler but adds about 12.5% memory overhead.

One aspect of the implementation of FMPH and FMPHGO is how to represent the sets of remaining keys K0,K1,.... Of course, when the algorithm is allowed to modify the input set of keys K, it can simply remove the keys assigned without collisions at successive levels, transforming K = K0 into K1, K1 into K2, and so on. However, all the algorithms benchmarked in Section 7 accept and are given read-only access to the vector of keys K. Even with this assumption, it is possible to build FMPH(GO) without using additional memory by verifying (in expected constant time) the membership of any key to Kl using arrays A0,...,Al−1 (the key is in Kl if and only if it has no corresponding one in any of the arrays A0,...,Al−1). However, iterating over all |K| keys at each level, increases the expected construction time to Θ(|K| log |K|) (as we expect Θ(log |K|) levels).

To speed up construction (to Θ(|K|)), the algorithm can store copies or indices of the remaining keys, starting at K1 or (to save memory at the expense of speed) later (for example, starting at K2).

Boomphf as well as our FMPH and FMPHGO implementations store the indices, beginning at K1.

However, boomphf does this naively, using 64 bits per index on a 64-bit machine.

In contrast, our implementations divide the indices into segments. Each segment covers indices with the same integer part of division by 256. The remainders from division (by 256) of consecutive indices, of consecutive segments, are stored in a vector of 8-bit integers I. The information about which segments are related to successive parts of I is stored in a separate vector S. Each S entry describes a non-empty segment and consists of two (64-bit) indices, kb and ib , which show the beginnings of the segment in K and I, respectively (kb is always a multiple of 256). So the segment contains the following keys: K[kb +I[ib +0]],K[kb +I[ib +1]],... (the segment in I ends with the end of I or at the index immediately preceding the beginning of the next segment).

For example, the set of K indices [19, 183, 513] is represented by I = [19 mod 256, 183 mod 265, 513 mod 256] = [19, 183, 1] and S = [(0, 0), (512, 2)]. S entries refer to two non-empty segments.

The first contains the indices (of K) 0 + I[0 + 0] = 19 and 0 + I[0 + 1] = 183, while the second 512 + I[2 + 0] = 513.

Our structure has the advantage of being particularly effective when it is needed most, that is, right after it is built, when the segments are densely filled with indices. Then the size of S
is negligible compared to I and the structure uses just over 8 bits per index. For example, K1 is described with about 9 bits per its element (4.5 bits per K element), assuming that it contains half of K elements.

All the necessary operations, such as removing the indices of selected keys, are as fast and almost as straightforward on our structure as on a regular vector of indices, and can usually be done with a single pass over I and S.

Our implementation of FMPHGO avoids hashing the key k twice for the purpose of determining дl (k) and dl,д (k). Instead, it first determines the 64-bit hash h = h64l (k) (using wyhash - see Section 5.1), and then calculates дl (k) and dl,д (k) using h instead of k. This method speeds up both evaluation and construction.

Construction can be sped up even more by calculating the h64 values for all keys included in Kl only once and caching them until the l-th level is constructed. In this way, all functions fl,0,..., fl,r−1 can be examined without hashing each key r times. Additionally, the hash cache avoids hashing the keys while checking if they are assigned ones in Al and should thus be removed from Kl when transforming Kl into Kl+1 (see step 2 of the construction algorithm shown in Section 3). To speed up transforming Kl into Kl+1, building an analogous cache is also reasonable for FMPH without group optimization. In this case, however, the cache should contain the values of the hl function, which in our implementation are also represented with 64 bits.

Storing 64-bit hashes for all keys increases memory consumption and is therefore optional in our FMPH and FMPHGO implementations. In Section 7 we benchmark both variants, with and without hash caching.

Even though 64 bits/key is a lot compared to the remaining memory used to build the level
(which, for FMPHGO, is about 3γ bits/key including the memory occupied by the Al itself, but excluding the cost described in Section 5.2), it still seems less than what non-fingerprint-based methods need. An exact comparison is difficult since publications on most of these methods do not contain enough information in this regard. But, for example, the RecSplit implementation described by its authors in [7] starts the construction by calculating (and caching) 128-bit unique hashes of all keys. And the PTHash [15] implementation developed by the method's authors contains an estimate_num_bytes_for_construction function that returns the predicted amount of memory needed during the construction (excluding memory occupied by the keys). This function returns values between 173 and 188 bits/key for the configurations tested in Section 7. Section 7 also contains measurements of actual memory consumption, which confirm our assumption.

## 5.4 Multi-Threaded Fmphgo Construction

Our FMPH and FMPHGO implementations employ the method mentioned in Section 3 (and described in [12]) that uses atomic memory accesses to parallelize the construction process.

However, FMPHGO can use an alternative parallelization method. Since the functions fl,0,..., fl,r−1 are examined independently of each other, they can be tried by separate threads.

This approach requires virtually no communication between threads and can therefore be faster.

But it also consumes more memory because each thread holds and fills its own arrays. Our initial tests showed that the described method is faster, but only for small sets of keys. Therefore, we abandoned it for the sake of simplifying our FMPHGO implementation. We recommend limiting the possible use of the method to constructing only small levels (when |Al | is below a certain threshold).

## 6 Benchmarks: Fmphgo Performance And Optimal Parameters

In this section, we check how fingerprint based perfect hashing with group optimization
(*FMPHGO* for short) performs in practice. Tables 1 and 2 show its performance for all combinations of s from 1 to 9, some even1 b, and γ equal to 1 and 2 (see Section 4 for the definition of these parameters). The results contained in these tables are obtained for 108 64-bit integer keys, but they are not expected to be noticeably dependent on either the number or type/size of keys.

The results show the high effectiveness of the optimization proposed in Section 4. The constructed function can occupy around as little as 2.1 bits per key (for example when γ = 1, s = 8, and b = 32). Both the sizes and the average numbers of levels visited during the evaluation (and thus the evaluation times) decrease with increasing s.

1Odd b are omitted for readability as small changes in b have limited effect on performance.
Table 1. Performance of FMPHGO for γ = 1 and Different Values of b and s
b s 123456789 2 3.27 2.13 3.77 1.85 4.49 1.77 5.35 1.76 6.22 1.76 7.10 1.76 7.98 1.76 8.86 1.76 9.74 1.76 4 2.68 2.09 2.71 1.77 2.84 1.59 3.03 1.49 3.28 1.44 3.59 1.42 3.93 1.41 4.27 1.41 4.61 1.41 6 2.56 2.14 2.48 1.82 2.50 1.63 2.56 1.51 2.66 1.43 2.79 1.37 2.93 1.33 3.10 1.31 3.30 1.30 8 2.52 2.18 2.40 1.88 2.37 1.68 2.38 1.55 2.42 1.46 2.49 1.40 2.57 1.35 2.66 1.31 2.77 1.28 10 2.51 2.22 2.37 1.93 2.31 1.73 2.29 1.60 2.31 1.51 2.34 1.43 2.38 1.38 2.44 1.33 2.51 1.30 12 2.51 2.25 2.36 1.97 2.28 1.78 2.25 1.65 2.24 1.55 2.25 1.47 2.28 1.41 2.32 1.36 2.36 1.33 14 2.51 2.28 2.36 2.01 2.27 1.82 2.22 1.69 2.21 1.59 2.21 1.51 2.22 1.45 2.24 1.40 2.27 1.35 16 2.52 2.30 2.36 2.04 2.26 1.86 2.21 1.73 2.19 1.63 2.18 1.55 2.18 1.48 2.19 1.43 2.21 1.39 18 2.52 2.32 2.36 2.07 2.26 1.89 2.21 1.76 2.17 1.66 2.16 1.58 2.15 1.52 2.16 1.46 2.17 1.42 20 2.53 2.34 2.37 2.09 2.27 1.92 2.21 1.79 2.17 1.69 2.15 1.61 2.14 1.55 2.13 1.49 2.14 1.44 22 2.53 2.35 2.37 2.11 2.27 1.94 2.21 1.82 2.16 1.72 2.14 1.64 2.13 1.57 2.12 1.52 2.12 1.47 24 2.54 2.37 2.38 2.13 2.28 1.97 2.21 1.84 2.16 1.75 2.14 1.67 2.12 1.60 2.11 1.55 2.11 1.50 26 2.54 2.38 2.38 2.15 2.28 1.99 2.21 1.87 2.17 1.77 2.14 1.69 2.11 1.63 2.10 1.57 2.10 1.52 28 2.55 2.39 2.39 2.17 2.29 2.01 2.22 1.89 2.17 1.79 2.14 1.71 2.11 1.65 2.10 1.59 2.09 1.55 30 2.55 2.40 2.40 2.18 2.29 2.03 2.22 1.91 2.17 1.81 2.14 1.74 2.11 1.67 2.10 1.61 2.09 1.57 32 2.56 2.41 2.40 2.20 2.30 2.04 2.23 1.93 2.18 1.83 2.14 1.76 2.11 1.69 2.10 1.64 2.08 1.59 34 2.56 2.41 2.41 2.21 2.30 2.06 2.23 1.94 2.18 1.85 2.14 1.77 2.12 1.71 2.10 1.65 2.08 1.61 36 2.57 2.42 2.41 2.22 2.31 2.07 2.24 1.96 2.18 1.87 2.15 1.79 2.12 1.73 2.10 1.67 2.08 1.62 38 2.57 2.43 2.42 2.23 2.31 2.08 2.24 1.97 2.19 1.88 2.15 1.81 2.12 1.74 2.10 1.69 2.08 1.64 The first value in each cell is the size in bits per key. The second (gray) value is the number of levels visited during the evaluation, averaged over all keys. The minimum value in each column is underlined. Figure 6 plots the values for s = 4.

However, it is important to properly choose the optimal group size b depending on s. In general, the largers, the larger b is worth using. However, for each s, there is a range of reasonable values of b, with different trade-offs between size and evaluation speed (as illustrated by the plot in Figure 6).

The lowest average numbers of levels visited, and therefore the best evaluation times, are achieved for relatively small values of b. Then the sizes |A0 |, |A1 |,... decrease rapidly, there are few levels and |A| is small. However, small b also lead to relatively large |G0 |, |G1 |,... (the size of Gl equals nls = |Al | b s, which increases as b decreases). Therefore, the entire representation is smallest for larger b than that which minimizes only |A| (and therefore the average time consumed by the evaluation).

Increasing γ (with unchanged s and b), in turn, increases |Al | = γ |Kl |, nl = |Al |/b, and decreases the average number of keys assigned to each group (|Kl |/nl). These changes can be compensated for by increasing b and thus |Kl |/nl . This reasoning suggests that larger b is worth using for larger γ , as confirmed by comparing Tables 1 and 2. Fortunately, as γ increases, so does the range of optimal choices of b. Thus, the possibly largest s that is optimal for γ = 1 is also optimal for larger, reasonable values of γ .

From a practical point of view, the most important are those among reasonable parameter values that divide the size of any of the available machine words without remainder, which facilitates efficient implementation. Examples of such values are: s = 1 b = 8; s = 2 b = 16; s = 4 b = 16; s = 8 b = 32. This is why we report the results for these parameters in Section 7 and compare them with the results obtained by other methods.

## 7 Benchmarks: Comparison Of Minimum Perfect Hash Functions

7.1 Experiment Methodology and Methods Tested Tables 3, 4, and 5 compare the performance of the following implementations of minimal perfect hash functions:

Fingerprinting-based Minimal Perfect Hashing Revisited 1.4:9

| Table 2. Performance of FMPHGO for γ = 2 and Different Values of b and s                                                    |      |      |      |      |      |      |      |      |      |      |      |      |       |      |       |      |       |      |
|-----------------------------------------------------------------------------------------------------------------------------|------|------|------|------|------|------|------|------|------|------|------|------|-------|------|-------|------|-------|------|
| b                                                                                                                           | s    |      |      |      |      |      |      |      |      |      |      |      |       |      |       |      |       |      |
| 1                                                                                                                           | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    |      |      |      |      |       |      |       |      |       |      |
| 2                                                                                                                           | 4.29 | 1.40 | 5.14 | 1.26 | 6.22 | 1.23 | 7.43 | 1.23 | 8.65 | 1.23 | 9.88 | 1.23 | 11.11 | 1.23 | 12.33 | 1.23 | 13.56 | 1.23 |
| 4                                                                                                                           | 3.45 | 1.35 | 3.68 | 1.20 | 4.03 | 1.13 | 4.44 | 1.09 | 4.90 | 1.07 | 5.41 | 1.07 | 5.94  | 1.07 | 6.48  | 1.07 | 7.01  | 1.07 |
| 6                                                                                                                           | 3.23 | 1.35 | 3.28 | 1.20 | 3.44 | 1.12 | 3.68 | 1.08 | 3.95 | 1.06 | 4.24 | 1.04 | 4.55  | 1.03 | 4.87  | 1.03 | 5.21  | 1.03 |
| 8                                                                                                                           | 3.15 | 1.36 | 3.10 | 1.21 | 3.18 | 1.13 | 3.32 | 1.08 | 3.50 | 1.06 | 3.71 | 1.04 | 3.93  | 1.03 | 4.16  | 1.02 | 4.39  | 1.02 |
| 10                                                                                                                          | 3.10 | 1.37 | 3.01 | 1.22 | 3.03 | 1.14 | 3.12 | 1.09 | 3.25 | 1.06 | 3.40 | 1.04 | 3.57  | 1.03 | 3.75  | 1.02 | 3.93  | 1.02 |
| 12                                                                                                                          | 3.08 | 1.38 | 2.96 | 1.24 | 2.95 | 1.15 | 3.00 | 1.10 | 3.09 | 1.07 | 3.20 | 1.05 | 3.33  | 1.03 | 3.48  | 1.02 | 3.62  | 1.02 |
| 14                                                                                                                          | 3.08 | 1.39 | 2.93 | 1.25 | 2.89 | 1.16 | 2.92 | 1.11 | 2.98 | 1.07 | 3.07 | 1.05 | 3.17  | 1.04 | 3.29  | 1.03 | 3.41  | 1.02 |
| 16                                                                                                                          | 3.07 | 1.40 | 2.92 | 1.26 | 2.86 | 1.17 | 2.86 | 1.12 | 2.90 | 1.08 | 2.97 | 1.05 | 3.05  | 1.04 | 3.15  | 1.03 | 3.25  | 1.02 |
| 18                                                                                                                          | 3.07 | 1.41 | 2.91 | 1.27 | 2.84 | 1.18 | 2.82 | 1.13 | 2.84 | 1.09 | 2.89 | 1.06 | 2.96  | 1.04 | 3.04  | 1.03 | 3.13  | 1.02 |
| 20                                                                                                                          | 3.08 | 1.42 | 2.91 | 1.28 | 2.82 | 1.19 | 2.79 | 1.13 | 2.80 | 1.09 | 2.84 | 1.07 | 2.89  | 1.05 | 2.96  | 1.03 | 3.04  | 1.02 |
| 22                                                                                                                          | 3.08 | 1.43 | 2.90 | 1.29 | 2.81 | 1.20 | 2.78 | 1.14 | 2.77 | 1.10 | 2.80 | 1.07 | 2.84  | 1.05 | 2.89  | 1.04 | 2.96  | 1.03 |
| 24                                                                                                                          | 3.08 | 1.44 | 2.91 | 1.30 | 2.81 | 1.21 | 2.76 | 1.15 | 2.75 | 1.11 | 2.77 | 1.08 | 2.80  | 1.06 | 2.84  | 1.04 | 2.90  | 1.03 |
| 26                                                                                                                          | 3.09 | 1.44 | 2.91 | 1.31 | 2.81 | 1.22 | 2.75 | 1.16 | 2.74 | 1.12 | 2.74 | 1.09 | 2.76  | 1.06 | 2.80  | 1.05 | 2.85  | 1.03 |
| 28                                                                                                                          | 3.09 | 1.45 | 2.91 | 1.32 | 2.81 | 1.23 | 2.75 | 1.17 | 2.72 | 1.13 | 2.72 | 1.09 | 2.74  | 1.07 | 2.77  | 1.05 | 2.81  | 1.04 |
| 30                                                                                                                          | 3.10 | 1.45 | 2.92 | 1.33 | 2.81 | 1.24 | 2.75 | 1.18 | 2.71 | 1.13 | 2.71 | 1.10 | 2.72  | 1.07 | 2.74  | 1.06 | 2.77  | 1.04 |
| 32                                                                                                                          | 3.10 | 1.46 | 2.92 | 1.34 | 2.81 | 1.25 | 2.75 | 1.19 | 2.71 | 1.14 | 2.70 | 1.11 | 2.70  | 1.08 | 2.72  | 1.06 | 2.74  | 1.05 |
| 34                                                                                                                          | 3.11 | 1.46 | 2.93 | 1.34 | 2.81 | 1.26 | 2.75 | 1.19 | 2.71 | 1.15 | 2.69 | 1.11 | 2.69  | 1.09 | 2.70  | 1.06 | 2.72  | 1.05 |
| 36                                                                                                                          | 3.11 | 1.47 | 2.93 | 1.35 | 2.82 | 1.26 | 2.75 | 1.20 | 2.70 | 1.16 | 2.68 | 1.12 | 2.68  | 1.09 | 2.68  | 1.07 | 2.70  | 1.05 |
| 38                                                                                                                          | 3.11 | 1.47 | 2.94 | 1.35 | 2.82 | 1.27 | 2.75 | 1.21 | 2.70 | 1.16 | 2.68 | 1.13 | 2.67  | 1.10 | 2.67  | 1.08 | 2.68  | 1.06 |
| 40                                                                                                                          | 3.12 | 1.48 | 2.94 | 1.36 | 2.83 | 1.28 | 2.75 | 1.22 | 2.70 | 1.17 | 2.67 | 1.13 | 2.66  | 1.10 | 2.66  | 1.08 | 2.67  | 1.06 |
| 42                                                                                                                          | 3.12 | 1.48 | 2.95 | 1.37 | 2.83 | 1.28 | 2.75 | 1.22 | 2.70 | 1.18 | 2.67 | 1.14 | 2.66  | 1.11 | 2.65  | 1.09 | 2.66  | 1.07 |
| 44                                                                                                                          | 3.13 | 1.48 | 2.95 | 1.37 | 2.84 | 1.29 | 2.76 | 1.23 | 2.71 | 1.18 | 2.67 | 1.14 | 2.65  | 1.11 | 2.65  | 1.09 | 2.65  | 1.07 |
| 46                                                                                                                          | 3.13 | 1.49 | 2.96 | 1.38 | 2.84 | 1.30 | 2.76 | 1.24 | 2.71 | 1.19 | 2.67 | 1.15 | 2.65  | 1.12 | 2.64  | 1.10 | 2.64  | 1.08 |
| 48                                                                                                                          | 3.13 | 1.49 | 2.96 | 1.38 | 2.85 | 1.30 | 2.77 | 1.24 | 2.71 | 1.19 | 2.67 | 1.16 | 2.65  | 1.13 | 2.64  | 1.10 | 2.63  | 1.08 |
| 50                                                                                                                          | 3.14 | 1.49 | 2.97 | 1.38 | 2.85 | 1.31 | 2.77 | 1.25 | 2.71 | 1.20 | 2.68 | 1.16 | 2.65  | 1.13 | 2.64  | 1.11 | 2.63  | 1.09 |
| 52                                                                                                                          | 3.14 | 1.49 | 2.97 | 1.39 | 2.85 | 1.31 | 2.77 | 1.25 | 2.72 | 1.21 | 2.68 | 1.17 | 2.65  | 1.14 | 2.63  | 1.11 | 2.63  | 1.09 |
| 54                                                                                                                          | 3.14 | 1.50 | 2.97 | 1.39 | 2.86 | 1.32 | 2.78 | 1.26 | 2.72 | 1.21 | 2.68 | 1.17 | 2.65  | 1.14 | 2.63  | 1.12 | 2.62  | 1.09 |
| 56                                                                                                                          | 3.15 | 1.50 | 2.98 | 1.40 | 2.86 | 1.32 | 2.78 | 1.26 | 2.72 | 1.22 | 2.68 | 1.18 | 2.65  | 1.15 | 2.63  | 1.12 | 2.62  | 1.10 |
| 58                                                                                                                          | 3.15 | 1.50 | 2.98 | 1.40 | 2.87 | 1.32 | 2.79 | 1.27 | 2.73 | 1.22 | 2.68 | 1.18 | 2.65  | 1.15 | 2.63  | 1.13 | 2.62  | 1.10 |
| 60                                                                                                                          | 3.15 | 1.50 | 2.99 | 1.40 | 2.87 | 1.33 | 2.79 | 1.27 | 2.73 | 1.23 | 2.69 | 1.19 | 2.66  | 1.16 | 2.63  | 1.13 | 2.62  | 1.11 |
| 62                                                                                                                          | 3.15 | 1.51 | 2.99 | 1.41 | 2.88 | 1.33 | 2.80 | 1.28 | 2.74 | 1.23 | 2.69 | 1.19 | 2.66  | 1.16 | 2.63  | 1.14 | 2.62  | 1.11 |
| The first value in each cell is the size in bits per key. The second (gray) value is the number of levels visited during th | e    |      |      |      |      |      |      |      |      |      |      |      |       |      |       |      |       |      |

FMPH, FMPHGO are our implementation of fingerprint-based minimal perfect hash functions without and with group optimization, respectively.2 Section 5 gives details of these implementations and their differences from boomphf.

boomphf is the implementation of fingerprint-based minimal perfect hash function developed by Patrick Marks.3 PTHash is an implementation of the method described in [15], with the multi-threading construction capability described in [14], developed by the authors of the method and the papers.4 We use the same designations and values for the parameters as used in the paper [15]
(in particular, the abbreviations C-C, D-D, EF indicate the integer compression methods used).

2The implementation source code is available at https://github.com/beling/bsuccinct-rs. 3Its source code is available at https://github.com/10XGenomics/rust-boomphf. We use its version 0.5.9, slightly modified
(and available at https://github.com/beling/rust-boomphf) to measure the number of levels visited during a key search and the size of the structure.

4Its source code is available at https://github.com/jermp/pthash.

![9_image_0.png](9_image_0.png)

Fig. 6. The plot of size (red) and average number of levels visited during the evaluation (blue) against parameter b for FMPHGO γ = 1 s = 4. The dots at b = 4 and b = 20 indicate minimum values. Values of b in the range [4, 20] provide various optimal trade-offs between size and evaluation speed. Decreasing b below 4 as well as increasing above 20, increases size and average evaluation time simultaneously.
RecSplit is an implementation of the method described in [7], developed by the authors of the method and the paper.5 We use the same designations and values for the parameters as used in the paper [7].

CHD is an implementation of the method described in [1], included in CMPH (C Minimal Perfect Hashing Library).6 We test it with all λ (the average number of keys per bucket)
values that lead to reasonable construction times.

FMPH, FMPHGO, and boomphf are written in the Rust language. We use our own program to benchmark them. This program, along with instructions for compiling and reproducing our entire experiment, is available at https://crates.io/crates/mphf_benchmark (and also at https://github.

com/beling/bsuccinct-rs).

PTHash and RecSplit are written in C++, while CMPH (CHD) is in C. We benchmark them using a C++ program developed by Giulio Ermanno Pibiri and Roberto Trani, available at https:// github.com/roberto-trani/mphf_benchmark. The authors have accepted our modifications to their program, which, among other things, ensure that both benchmark programs can generate exactly the same keys for testing MPHFs.

The results in the tables are obtained for different sets of keys. Table 3 uses a collection of URLs from the .uk domain, collected in 2005 by UbiCrawler [2] and available at https://law.di.unimi.it/
webdata/uk-2005/. This collection consists of 39,459,925 strings with an average length of 71.4 bytes and is used to test MPHF performance also in [14, 15]. To see the effect of key type/size on the results, Table 4 uses a set that has the same number (39,459,925) of keys, but consists of 64-bit integers generated uniformly at random. A similar, but larger, set of 5 · 108 64-bit integers is used in Table 5.

5Its source code is available at https://github.com/vigna/sux. 6CMPH with its source code is freely available at http://cmph.sourceforge.net/.

## Fingerprinting-Based Minimal Perfect Hashing Revisited 1.4:11

| 39,459,925 Unique Strings (URLs from uk2005 Collection) with an Average Length of 71.4 bytes construction   |            |          |                  |          |          |             |             |        |       |      |    |    |
|-------------------------------------------------------------------------------------------------------------|------------|----------|------------------|----------|----------|-------------|-------------|--------|-------|------|----|----|
| method                                                                                                      | parameters | size     | evaluation speed | time [s] | memory   |             |             |        |       |      |    |    |
|  bits key                                                                                                             | [levels]   | [ns]     | single           | +hash    | multiple | +hash       |             |        |       |      |    |    |
|                                                                                                             | thread     | cache    | threads          | cache    |  bits key          | +hash cache |             |        |       |      |    |    |
| FMPHGO                                                                                                      | s = 1      | b = 8    | γ = 1            | 2.52     | 2.18     | 83          | 10.93       | 4.10   | 1.77  | 1.03 | 8  | 70 |
| γ = 2                                                                                                       | 3.15       | 1.36     | 72               | 8.15     | 3.02     | 1.13        | 0.63        | 7      | 70    |      |    |    |
| s = 2                                                                                                       | b = 16     | γ = 1    | 2.36             | 2.04     | 79       | 15.93       | 4.39        | 2.72   | 1.20  | 7    | 70 |    |
| γ = 2                                                                                                       | 2.92       | 1.26     | 63               | 12.92    | 3.97     | 1.71        | 0.75        | 6      | 70    |      |    |    |
| s = 4                                                                                                       | b = 16     | γ = 1    | 2.21             | 1.73     | 70       | 40.56       | 6.56        | 7.57   | 2.27  | 6    | 69 |    |
| γ = 2                                                                                                       | 2.86       | 1.12     | 54               | 39.93    | 10.18    | 4.73        | 1.60        | 7      | 71    |      |    |    |
| s = 8                                                                                                       | b = 32     | γ = 1    | 2.10             | 1.64     | 64       | 555.01      | 59.15       | 107.32 | 27.98 | 6    | 69 |    |
| γ = 2                                                                                                       | 2.72       | 1.06     | 46               | 570.58   | 138.09   | 64.20       | 18.89       | 7      | 71    |      |    |    |
| FMPH                                                                                                        | γ = 1      | 2.80     | 2.72             | 79       | 8.48     | 4.35        | 1.45        | 0.98   | 8     | 71   |    |    |
| γ = 2                                                                                                       | 3.40       | 1.65     | 74               | 5.86     | 2.59     | 0.87        | 0.56        | 7      | 70    |      |    |    |
| boomphf                                                                                                     | γ = 1      | 3.06     | 2.72             | 84       | 9.36     | 1.57        | 85 (mt: 97) |        |       |      |    |    |
| γ = 2                                                                                                       | 3.71       | 1.65     | 72               | 6.77     | 1.09     | 46 (mt: 56) |             |        |       |      |    |    |
| C-C                                                                                                         | α = 0.99   | c = 7    | 3.25             | 38       | 10.03    | 5.19        | 201         |        |       |      |    |    |
| PTHash                                                                                                      | D-D        | α = 0.88 | c = 11           | 4.09     | 50       | 6.01        | 4.82        | 238    |       |      |    |    |
| EF                                                                                                          | α = 0.99   | c = 6    | 2.28             | 53       | 13.34    | 6.19        | 213         |        |       |      |    |    |
| D-D                                                                                                         | α = 0.94   | c = 7    | 3.11             | 41       | 8.41     | 4.69        | 201         |        |       |      |    |    |
| 𝓁 = 5                                                                                                      | b = 5      | 2.95     | 100              | 6.03     | 182      |             |             |        |       |      |    |    |
| RecSplit                                                                                                    | 𝓁 = 8     | b = 100  | 1.79             | 107      | 39.35    | 132         |             |        |       |      |    |    |
| 𝓁 = 12                                                                                                     | b = 9      | 2.23     | 80               | 232.14   | 159      |             |             |        |       |      |    |    |
| CHD                                                                                                         | λ = 1      | 3.56     | 173              | 9.30     | 201      |             |             |        |       |      |    |    |
| λ = 2                                                                                                       | 2.54       | 146      | 9.78             | 238      |          |             |             |        |       |      |    |    |
| λ = 3                                                                                                       | 2.27       | 144      | 13.01            | 213      |          |             |             |        |       |      |    |    |
| λ = 4                                                                                                       | 2.17       | 139      | 24.04            | 201      |          |             |             |        |       |      |    |    |
| λ = 5                                                                                                       | 2.07       | 140      | 62.53            | 201      |          |             |             |        |       |      |    |    |
| λ = 6                                                                                                       | 2.01       | 141      | 241.04           | 238      |          |             |             |        |       |      |    |    |
| See Section 7.1 for more details.                                                                           |            |          |                  |          |          |             |             |        |       |      |    |    |

Table 3. Performance Comparison of Minimal Perfect Hash Functions for a Set of Keys Consisting of 39,459,925 Unique Strings (URLs from uk2005 Collection) with an Average Length of 71.4 bytes Successive columns of the tables show the following measured performance characteristics of the tested MPHFs:
- size in bits per key.

- evaluation speed averaged over all input keys and given both in nanoseconds and (in the case of boomphf, FMPH, and FMPHGO) as the number of levels visited during the evaluation. Note that the average numbers of levels visited during the evaluation is equal to the average number of levels on which a key was processed (before they were assigned without collision) during construction.

- construction time (in seconds) when using single and (for algorithms with adequate capabilities) multiple threads.

Additionally, the "+ hash cache" columns give construction times for FMPH and FMPHGO
that cache 64-bit hashes, as described in Section 5.3.

- peak heap7 memory consumption (in bits per key) during construction, excluding the memory occupied by the (read-only vector of) keys.

We measured memory consumption both when single and multiple threads were used. In the case of FMPH, FMPHGO, and PTHash, we obtained almost the same results in both cases

7We ensured that the stack memory consumption is negligible.

| 39,459,925 Unique 64-bits Integers Generated Uniformly at Random construction   |            |          |                  |          |             |             |             |       |       |      |    |    |
|---------------------------------------------------------------------------------|------------|----------|------------------|----------|-------------|-------------|-------------|-------|-------|------|----|----|
| method                                                                          | parameters | size     | evaluation speed | time [s] | memory      |             |             |       |       |      |    |    |
|  bits key                                                                                 | [levels]   | [ns]     | single           | +hash    | multiple    | +hash       |             |       |       |      |    |    |
| thread                                                                          | cache      | threads  | cache            |  bits key          | +hash cache |             |             |       |       |      |    |    |
| FMPHGO                                                                          | s = 1      | b = 8    | γ = 1            | 2.52     | 2.18        | 41          | 1.88        | 1.52  | 0.53  | 0.58 | 8  | 70 |
| γ = 2                                                                           | 3.15       | 1.36     | 32               | 1.86     | 1.58        | 0.35        | 0.39        | 7     | 70    |      |    |    |
| s = 2                                                                           | b = 16     | γ = 1    | 2.36             | 2.04     | 40          | 2.63        | 2.01        | 0.81  | 0.79  | 7    | 70 |    |
| γ = 2                                                                           | 2.92       | 1.26     | 28               | 3.15     | 2.67        | 0.54        | 0.54        | 6     | 70    |      |    |    |
| s = 4                                                                           | b = 16     | γ = 1    | 2.21             | 1.73     | 37          | 6.34        | 4.50        | 2.32  | 1.92  | 6    | 69 |    |
| γ = 2                                                                           | 2.86       | 1.12     | 25               | 10.32    | 9.03        | 1.62        | 1.41        | 7     | 71    |      |    |    |
| s = 8                                                                           | b = 32     | γ = 1    | 2.10             | 1.64     | 34          | 84.21       | 56.60       | 33.54 | 27.91 | 6    | 69 |    |
| γ = 2                                                                           | 2.72       | 1.06     | 23               | 156.31   | 136.18      | 22.47       | 18.82       | 7     | 71    |      |    |    |
| FMPH                                                                            | γ = 1      | 2.80     | 2.72             | 34       | 1.23        | 1.02        | 0.33        | 0.41  | 8     | 71   |    |    |
| γ = 2                                                                           | 3.40       | 1.65     | 32               | 1.03     | 0.79        | 0.20        | 0.26        | 7     | 70    |      |    |    |
| boomphf                                                                         | γ = 1      | 3.06     | 2.72             | 31       | 1.88        | 0.47        | 85 (mt: 97) |       |       |      |    |    |
| γ = 2                                                                           | 3.71       | 1.65     | 28               | 1.49     | 0.34        | 46 (mt: 56) |             |       |       |      |    |    |
| C-C                                                                             | α = 0.99   | c = 7    | 3.25             | 14       | 9.36        | 4.99        | 201         |       |       |      |    |    |
| PTHash                                                                          | D-D        | α = 0.88 | c = 11           | 4.09     | 25          | 5.51        | 4.82        | 238   |       |      |    |    |
| EF                                                                              | α = 0.99   | c = 6    | 2.28             | 27       | 12.61       | 6.01        | 213         |       |       |      |    |    |
| D-D                                                                             | α = 0.94   | c = 7    | 3.11             | 18       | 7.84        | 4.61        | 201         |       |       |      |    |    |
| 𝓁 = 5                                                                          | b = 5      | 2.95     | 82               | 5.44     | 182         |             |             |       |       |      |    |    |
| RecSplit                                                                        | 𝓁 = 8     | b = 100  | 1.80             | 87       | 38.80       | 132         |             |       |       |      |    |    |
| 𝓁 = 12                                                                         | b = 9      | 2.23     | 58               | 231.44   | 159         |             |             |       |       |      |    |    |
| CHD                                                                             | λ = 1      | 3.56     | 125              | 6.33     | 257         |             |             |       |       |      |    |    |
| λ = 2                                                                           | 2.54       | 107      | 6.83             | 209      |             |             |             |       |       |      |    |    |
| λ = 3                                                                           | 2.27       | 109      | 9.92             | 193      |             |             |             |       |       |      |    |    |
| λ = 4                                                                           | 2.17       | 108      | 21.61            | 185      |             |             |             |       |       |      |    |    |
| λ = 5                                                                           | 2.07       | 108      | 64.33            | 180      |             |             |             |       |       |      |    |    |
| λ = 6                                                                           | 2.01       | 108      | 255.13           | 177      |             |             |             |       |       |      |    |    |
| See Section 7.1 for more details.                                               |            |          |                  |          |             |             |             |       |       |      |    |    |

Table 4. Performance Comparison of Minimal Perfect Hash Functions for a Set of Keys Consisting of 39,459,925 Unique 64-bits Integers Generated Uniformly at Random
(maximum difference of less than 0.1 bits/key). Therefore, for the sake of readability, we decided to put only the values for single-threaded calculations in the tables. However, for boomphf, the values for multiple threads are noticeably larger, so we report them additionally in parentheses.

In the "+ hash cache" column, we report the memory consumption (in bits per key) of FMPH and FMPHGO with the hash caching, which, as we predicted in Section 5.3, significantly increases this consumption.

We measure memory consumption using the *memusage* profiler, which is written by Ulrich Drepper and is part of the GNU C library. This tool tracks all memory allocations and deallocations
(calls to malloc, calloc, free, etc.) made by the program and provides accurate and reproducible measurements. More information can be found in [6, 17].

All times are measured on a computer with an AMD Ryzen 5600G @3.9GHz (6 cores, 12 threads, 384KB/3MB/16MB of level 1/2/3 cache) processor and are averaged over 30 runs (except for the construction times in Table 5, which are averaged over 5 runs). Multithreaded calculations use 12 threads (with 6 threads all methods run slightly slower). Note that conclusions drawn from measured times should be treated with some caution, as they are dependent on the details of the implementation, compiler, hardware, and so on.

| 5 · 108 Unique 64-bits Integers Generated Uniformly at Random construction   |            |          |                  |          |          |             |               |      |      |    |    |    |
|------------------------------------------------------------------------------|------------|----------|------------------|----------|----------|-------------|---------------|------|------|----|----|----|
| method                                                                       | parameters | size     | evaluation speed | time [s] | memory   |             |               |      |      |    |    |    |
|  bits key                                                                              | [levels]   | [ns]     | single           | +hash    | multiple | +hash       |               |      |      |    |    |    |
|                                                                              | thread     | cache    | threads          | cache    |  bits key          | +hash cache |               |      |      |    |    |    |
| FMPHGO                                                                       | s = 1      | b = 8    | γ = 1            | 2.52     | 2.18     | 126         | 80            | 69   | 19   | 18 | 8  | 70 |
| γ = 2                                                                        | 3.15       | 1.36     | 89               | 53       | 47       | 14          | 13            | 7    | 70   |    |    |    |
| s = 2                                                                        | b = 16     | γ = 1    | 2.36             | 2.04     | 120      | 123         | 109           | 31   | 28   | 7  | 70 |    |
| γ = 2                                                                        | 2.92       | 1.26     | 82               | 83       | 75       | 22          | 20            | 6    | 70   |    |    |    |
| s = 4                                                                        | b = 16     | γ = 1    | 2.21             | 1.73     | 113      | 352         | 310           | 96   | 82   | 6  | 69 |    |
| γ = 2                                                                        | 2.86       | 1.12     | 73               | 251      | 232      | 69          | 59            | 6    | 70   |    |    |    |
| s = 8                                                                        | b = 32     | γ = 1    | 2.10             | 1.64     | 104      | 5037        | 4448          | 1383 | 1158 | 6  | 69 |    |
| γ = 2                                                                        | 2.72       | 1.06     | 65               | 3600     | 3288     | 1013        | 853           | 6    | 70   |    |    |    |
| FMPH                                                                         | γ = 1      | 2.80     | 2.72             | 103      | 46       | 35          | 11            | 11   | 8    | 71 |    |    |
| γ = 2                                                                        | 3.40       | 1.65     | 78               | 31       | 23       | 8           | 7             | 7    | 70   |    |    |    |
| boomphf                                                                      | γ = 1      | 3.06     | 2.72             | 101      | 55       | 19          | 106 (mt: 111) |      |      |    |    |    |
| γ = 2                                                                        | 3.72       | 1.65     | 70               | 39       | 13       | 57 (mt: 64) |               |      |      |    |    |    |
| C-C                                                                          | α = 0.99   | c = 7    | 3.10             | 36       | 440      | 159         | 229           |      |      |    |    |    |
| PTHash                                                                       | D-D        | α = 0.88 | c = 11           | 4.05     | 53       | 134         | 65            | 225  |      |    |    |    |
| EF                                                                           | α = 0.99   | c = 6    | 2.19             | 71       | 718      | 249         | 214           |      |      |    |    |    |
| D-D                                                                          | α = 0.94   | c = 7    | 3.01             | 44       | 300      | 111         | 229           |      |      |    |    |    |
| 𝓁 = 5                                                                       | b = 5      | 2.95     | 232              | 75       | 182      |             |               |      |      |    |    |    |
| RecSplit                                                                     | 𝓁 = 8     | b = 100  | 1.80             | 188      | 497      | 132         |               |      |      |    |    |    |
| 𝓁 = 12                                                                      | b = 9      | 2.23     | 180              | 3003     | 159      |             |               |      |      |    |    |    |
| CHD                                                                          | λ = 1      | 3.56     | 351              | 139      | 257      |             |               |      |      |    |    |    |
| λ = 2                                                                        | 2.54       | 341      | 177              | 209      |          |             |               |      |      |    |    |    |
| λ = 3                                                                        | 2.27       | 330      | 332              | 193      |          |             |               |      |      |    |    |    |
| λ = 4                                                                        | 2.17       | 324      | 857              | 185      |          |             |               |      |      |    |    |    |
| λ = 5                                                                        | 2.07       | 323      | 2821             | 180      |          |             |               |      |      |    |    |    |
| λ = 6                                                                        | 2.01       | 322      | 11187            | 177      |          |             |               |      |      |    |    |    |
| See Section 7.1 for more details.                                            |            |          |                  |          |          |             |               |      |      |    |    |    |

Table 5. Performance Comparison of Minimal Perfect Hash Functions for a Set of Keys Consisting of 5 · 108 Unique 64-bits Integers Generated Uniformly at Random
7.2 Discussion of the Results The sizes (in bits/key) of the tested MPHFs depend on neither the type nor the number (except for PTHash) of keys. Therefore, we can compare the sizes using any of the tables. Comparing Tables 3 and 4, we can see that increasing the size of keys (and therefore the times needed to hash them) slows down both evaluation and construction of all the MPHFs tested. This is especially true for the fingerprint-based MPHFs, since they hash the keys multiple times (but, understandably, hash caching significantly reduces build slowdowns). Comparing Tables 4 and 5, we can see that increasing the number of keys also slows down all the MPHFs tested. Interestingly, the slowdown in evaluation is caused only by the increased number of CPU cache misses, not by the increased number of operations performed (the tested MPHFs have constant expected evaluation complexity, which for the fingerprint-based MPHFs is confirmed by the lack of differences between the tables in the "evaluation speed [levels]" column).

By using a more succinct structure to support rank queries (see Section 5.1), FMPH is about 8.5% smaller than boomphf with the same parameters. FMPHGO reduces the size further, but at the cost of longer construction time. The difference increases with increasing s. For instance, for γ = 1, FMPHGO is smaller than FMPH by about: 10% fors = 1, 16% fors = 2, 21% fors = 4, and 25%
for s = 8. At the same time, assuming no hash caching, its build time is longer by about: 1.2–1.8 times for s = 1, 1.8–2.8 times for s = 2, 5–8 times for s = 4, and 65–122 times for s = 8. With hash caching, the differences are smaller. Admittedly, caching reduces the build time of both functions, but FMPHGO benefits from it more than FMPH, which is as expected. The greatest benefit of hash caching is obviously seen in Table 3, where it results in avoiding multiple hashing of large keys.

In this case, the differences in construction times between FMPH and FMPHGO (with caching) are relatively smallest, for s = 1 even negligible. This is because FMPHGO reduces the size of successive levels faster and, as a result, performs less expensive key hashing than FMPH (from the
"evaluation speed [levels]" column, we can read that for γ = 1, FMPH hashes each key 2.72 times on average, while FMPHGO s = 1 b = 8, 2.52 times).

Multithreading reduces FMPH and FMPHGO build times more than hash caching does. Unfortunately, multithreading does not speed up variants with hash caching as much as those without it. In a few cases, the combination of both techniques even leads to longer construction times than multithreading alone (see FMPHGOs = 1 b = 8 and FMPH in Table 4). Without caching, FMPH and FMPHGO benefit more from multithreading than PTHash. With caching, the benefit comparison is no longer so clear-cut.

FMPHGO is more space efficient than PTHash and about on par with CHD. Only RecSplit can achieve a significantly smaller size. Compared to PTHash and CHD variants of similar sizes, FMPHGO typically takes less time to build, especially when it caches hashes (which is important for large keys) or uses multiple threads. As an example, please compare variants with sizes around 2.2 bits/key, that is, FMPHGO s = 4 b = 16 γ = 1 with PTHash EF α = 0.99 c = 6, and with CHD
λ = 3 or λ = 4.

In terms of evaluation speed, FMPHGO, FMPH, and boomphf perform more or less similarly and are generally fast, faster than RecSplit, much faster than CHD, and slower only than PTHash. For the same γ , compared to FMPH (or boomphf), FMPHGO visits fewer levels on average during the evaluation, and therefore hashes the key fewer times. The difference increases with s. However, FMPHGO performs additional operations at each level, including reading from the Gl array (see pseudocode in Figure 5) that can cause a CPU cache miss. The small difference in evaluation speeds is therefore not surprising, especially since both algorithms also use about the same amount of time to perform a rank query. In our tests for 64-bit keys (Tables 4 and 5), FMPH (as well as boomphf) is slightly faster than FMPHGO with the same γ , but the advantage decreases with increasing s.

FMPHGO with s ≥ 2 is slightly faster than FMPH for large keys (Table 3). FMPHGO variants with larger γ values may provide a faster to evaluate but slower to build alternative to FMPH variants of similar size. For example, FMPHGO s = 8 b = 32 γ = 2 is significantly faster and at the same time slightly smaller than FMPH γ = 1.

The results shown in the "memory" column do not substantially depend on either the number or size of the keys, and are therefore similar in all tables. They confirm the observation in [12]
that fingerprint-based minimal perfect hash functions can be constructed with very limited memory. Group optimization does not change much in this regard. The measured peak memory consumption is almost the same for FMPH and FMPHGO (about 6–8 bits/key). At the same time, it is much lower than that for boomphf (about 46–111 bits/key), which is mainly thanks to the compact representation of key sets described in Section 5.2. As predicted in Section 5.3, caching hashes significantly increases memory consumption during the construction of FMPH and FMPHGO (to about 69–71 bits/key). This consumption is then similar to that for boomphf and is still noticeably lower than those for the other methods tested. Among them, RecSplit stands out positively.

For  = 8 b = 100 (that is, for the parameters that lead to the smallest size, 1.8 bits/key) it consumes 132 bits/key, which is only a little more than is occupied by the 128-bit hashes of the keys it uses during construction. The values measured for PTHash are slightly larger than those predicted (173–188 bits/key) by the estimate_num_bytes_for_construction function mentioned in Section 5.3.

## 8 Conclusions

Different minimal perfect hashing functions offer different trade-offs between the memory needed to build and represent them and the speed of evaluation and building. PTHash [15] is unbeatable in terms of evaluation speed, and RecSplit [7] in terms of size. *Fingerprint-based minimal perfect hash* function (*FMPH* for short) [5, 12, 13], which is the focus of this paper, is unrivaled in terms of memory consumption during construction, additionally offering quite fast evaluation. However, FMPH
takes about 3 bits per key, which is significantly more than the mentioned competitors and often makes it unattractive. Fortunately, we have been able to develop an enhancement called FMPHGO
(which we present in Section 4) that reduces the size of FMPH. In addition, we also empirically find the optimal parameters for FMPHGO (in Section 6) and discussed how to effectively implement FMPH and FMPHGO (in Section 5). Our benchmarks in Sections 6 and 7 show that with FMPHGO
and an efficient structure to support the rank queries, the FMPH size can be reduced to about 2.1 bits/key, which is close to the size achieved by state-of-the-art methods and noticeably larger only compared to RecSplit. FMPHGO retains many advantages of FMPH, such as good evaluation speed (only PTHash is faster in our benchmarks) and very low memory consumption during construction. Unfortunately, FMPHGO significantly increases the construction time, which, however, is still competitive with methods of similar space efficiency (like CHD or PTHash), and seems to be good enough for practical applications.

Nevertheless, accelerating FMPHGO may be a goal for further research. A potential avenue to achieve this goal is to improve the technique described in Section 5.3. Perhaps cached (64-bit) key hashes could be used at several subsequent levels. This could speed up not only construction, but also evaluation (which would no longer require hashing at each level). Another direction for further work could involve potentially applying the idea behind the method proposed in Section 4 to improve a different minimal perfect hash function.

## References

[1] Djamal Belazzougui, Fabiano C. Botelho, and Martin Dietzfelbinger. 2009. Hash, displace, and compress. In Algorithms
- ESA 2009, Amos Fiat and Peter Sanders (Eds.). Springer, Berlin, Berlin, 682–693.

[2] Paolo Boldi, Bruno Codenotti, Massimo Santini, and Sebastiano Vigna. 2004. UbiCrawler: A scalable fully distributed web crawler. *Software: Practice & Experience* 34, 8 (2004), 711–726.

[3] Fabiano C. Botelho, Yoshiharu Kohayakawa, and Nivio Ziviani. 2005. A practical minimal perfect hashing method. In Experimental and Efficient Algorithms, Sotiris E. Nikoletseas (Ed.). Springer, Berlin, Berlin, 488–500.

[4] Fabiano C. Botelho, Rasmus Pagh, and Nivio Ziviani. 2007. Simple and space-efficient minimal perfect hash functions.

In *Algorithms and Data Structures*, Frank Dehne, Jörg-Rüdiger Sack, and Norbert Zeh (Eds.). Springer, Berlin, Berlin, 139–150.

[5] Jarrod A. Chapman, Isaac Ho, Sirisha Sunkara, Shujun Luo, Gary P. Schroth, and Daniel S. Rokhsar. 2011. Meraculous:
De novo genome assembly with short paired-end reads. *PLOS ONE* 6, 8 (08 2011), 1–13. https://doi.org/10.1371/journal.

pone.0023501
[6] Ulrich Drepper. 2007. *What Every Programmer Should Know About Memory*.

[7] Emmanuel Esposito, Thomas Mueller Graf, and Sebastiano Vigna. *RecSplit: Minimal Perfect Hashing via Recursive Splitting*. 175–185. https://doi.org/10.1137/1.9781611976007.14 arXiv:https://epubs.siam.org/doi/pdf/10.1137/1.

9781611976007.14.

[8] Edward A. Fox, Qi Fan Chen, and Lenwood S. Heath. 1992. A faster algorithm for constructing minimal perfect hash functions. In Proceedings of the 15th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR'92). Association for Computing Machinery, New York, NY, USA, 266–273. https://doi.org/
10.1145/133160.133209
[9] Michael L. Fredman and János. Komlós. 1984. On the size of separating systems and families of perfect hash functions.

SIAM Journal on Algebraic Discrete Methods 5, 1 (1984), 61–68. https://doi.org/10.1137/0605009
[10] Marco Genuzio, Giuseppe Ottaviano, and Sebastiano Vigna. 2020. Fast scalable construction of ([compressed] static | minimal perfect hash) functions. *Information and Computation* 273 (2020), 104517. https://doi.org/10.1016/j.ic.2020.

104517 DCC (Data Compression Conference) 2018.

[11] Rodrigo González, Szymon Grabowski, Veli Mäkinen, and Gonzalo Navarro. 2005. Practical implementation of rank and select queries. In *Poster Proceedings Volume of 4th Workshop on Efficient and Experimental Algorithms (WEA'05)*
(Greece). 27–38.

[12] Antoine Limasset, Guillaume Rizk, Rayan Chikhi, and Pierre Peterlongo. 2017. Fast and scalable minimal perfect hashing for massive key sets. In *16th International Symposium on Experimental Algorithms (SEA 2017) (Leibniz International* Proceedings in Informatics (LIPIcs)), Vol. 75. Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik, Dagstuhl, Germany, 25:1–25:16. https://doi.org/10.4230/LIPIcs.SEA.2017.25
[13] Ingo Müller, Peter Sanders, Robert Schulze, and Wei Zhou. 2014. Retrieval and perfect hashing using fingerprinting.

In *Experimental Algorithms*, Joachim Gudmundsson and Jyrki Katajainen (Eds.). Springer International Publishing, Cham, 138–149.

[14] Giulio Ermanno Pibiri and Roberto Trani. 2021. Parallel and external-memory construction of minimal perfect hash functions with PTHash. *CoRR* abs/2106.02350 (2021). arXiv:2106.02350 https://arxiv.org/abs/2106.02350.

[15] Giulio Ermanno Pibiri and Roberto Trani. 2021. *PTHash: Revisiting FCH Minimal Perfect Hashing*. Association for Computing Machinery, New York, NY, USA, 1339–1348. https://doi.org/10.1145/3404835.3462849
[16] Jaikumar Radhakrishnan. 1992. Improved bounds for covering complete uniform hypergraphs. *Inform. Process. Lett.*
41, 4 (1992), 203–207. https://doi.org/10.1016/0020-0190(92)90181-T
[17] Peter Schiffer, Michael Kerrisk, and Jan Chaloupka. 2021. *memusage(1) Linux User's Manual* (5.13 ed.). [18] Yi Wang. [n. d.]. wyhash. https://github.com/wangyi-fudan/wyhash. [accessed 18 Jun. 2022].

[19] Dong Zhou, David G. Andersen, and Michael Kaminsky. 2013. Space-efficient, high-performance rank and select structures on uncompressed bit sequences. In *Experimental Algorithms, 12th International Symposium, SEA 2013, Rome, Italy,*
June 5–7, 2013. Proceedings (Lecture Notes in Computer Science), Vincenzo Bonifaci, Camil Demetrescu, and Alberto Marchetti-Spaccamela (Eds.), Vol. 7933. Springer, 151–163. https://doi.org/10.1007/978-3-642-38527-8_15 Received 14 July 2022; revised 7 January 2023; accepted 17 April 2023