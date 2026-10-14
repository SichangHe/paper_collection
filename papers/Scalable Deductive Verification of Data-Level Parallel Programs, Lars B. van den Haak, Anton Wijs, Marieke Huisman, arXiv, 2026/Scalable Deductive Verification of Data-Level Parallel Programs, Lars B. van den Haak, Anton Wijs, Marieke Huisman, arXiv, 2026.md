                                             Scalable Deductive Verification of Data-Level
                                                          Parallel Programs

                                         Lars B. van den Haak1[0000−0002−0330−5016] , Anton Wijs1[0000−0002−2071−9624] ,
                                                         and Marieke Huisman2[0000−0003−4467−072X]
                                                       1
                                                           Eindhoven University of Technology, The Netherlands
                                                                  {l.b.v.d.haak, a.j.wijs}@tue.nl
arXiv:2605.13616v1 [cs.SE] 13 May 2026




                                                                2
                                                                  University of Twente, The Netherlands
                                                                        m.huisman@utwente.nl



                                               Abstract. This paper introduces several techniques that improve the
                                               scalability of the deductive verification of data-level programs working
                                               on arrays and matrices. First of all, we introduce a technique to rewrite
                                               expressions with (nested) quantifiers, so suitable triggers can be gener-
                                               ated for these expressions. We have proven this rewrite technique correct
                                               in a theorem prover. Second, we make reasoning about potentially over-
                                               lapping arrays easier, by providing specification constructs to indicate
                                               and verify that two arrays are not aliases, or that they are immutable, so
                                               they can be modelled as mathematical sequences. All our techniques are
                                               implemented in the VerCors program verifier. We illustrate how our
                                               techniques improve scalability through a large number of experiments.
                                               Using our techniques on a set of typical GPU kernels, we achieve a re-
                                               duction of verification time by, on average, a factor of 9, with outliers
                                               being up to 150 times faster. Additionally, applying these techniques to
                                               earlier experiments and an earlier case study of a radio telescope pipeline
                                               permitted the verification of results which were previously unobtainable
                                               and significantly reduced the verification time.

                                               Keywords: Deductive Verification · Separation Logic · Parallel · GPU
                                               · GPGPU · Quantifiers


                                         1   Introduction

                                         Data (or Data-level ) parallel programming is an approach to parallel program-
                                         ming in which multiple threads concurrently perform the same operations on
                                         different data elements [11]. Over the years, this approach to parallel program-
                                         ming has become increasingly popular, in particular in the form of the Single
                                         Instruction, Multiple Data (SIMD) paradigm. Modern Graphics Processing Units
                                         (GPUs) offer a prominent way of SIMD programming, but also Central Process-
                                         ing Units (CPUs) support SIMD instructions. GPU computing, and therefore
                                         data parallel programming, has had a major impact on scientific computing in
                                         fields such as computational biology (e.g., genomics) [24], statistics [15], and
                                         physics (e.g., fluid dynamics) [2]. Furthermore, GPUs effectively accelerate com-
2       L. B. van den Haak, A.J. Wijs and M. Huisman

putations involving matrix-vector and matrix-matrix multiplications [9,25], and
they made an enormous impact on Artificial Intelligence with deep learning [12].
     Due to this success, these days, there is a plethora of programming languages
supporting this paradigm, such as SYCL, OpenCL, CUDA and OpenMP. Typical
data structures that are used in these programs are arrays and matrices.
     However, deductive verification of these programs, i.e., verifying that they
satisfy formal contracts, often runs into scalability issues. Verification of a com-
putation quickly takes (too) long or becomes unfeasible. Bottlenecks are in the
reasoning at the SMT level: the deductive verification tool applies program logics
that create SMT proof obligations. We have identified multiple causes for this:
  – Generated proof obligations often contain (multiple) nested quantifier ex-
     pressions, and SMT solvers have difficulty reasoning about them as they
     often involve triggers, i.e., patterns, that are not suitable for actually trig-
     gering an instantiation of the quantifiers.
  – If a program uses multiple arrays, matrices, or higher dimensional array
     structures, then these could potentially be aliases of each other. This needs
     to be verified, as it may influence program correctness, but that leads to
     many additional proof obligations.
     We introduce multiple solutions to address these causes, all of which are
implemented in the deductive program verifier VerCors [1]. VerCors uses
permission-based separation logic as its specification language, which means that
for all shared memory, the user needs to specify permission annotations that
capture whether a thread has read or write access at a certain moment. Moreover,
all functional properties are framed, i.e. one can only state something about that
part of the memory to which one has access.
     First of all, after the background has been explained in Section 2, we pro-
pose a rewriting procedure in Section 3 to flatten expressions with nested quan-
tifiers into equivalent expressions with single quantifiers, for which triggers can
be generated that make the verification process efficient. We have proven the
correctness of this procedure using Lean.
     Second, in Section 4, we propose a mechanism to indicate that arrays (and
other data structures) are not aliases of each other. For this, we use uniqueness
types. This helps to significantly reduce the reasoning about potential aliases.
     Sometimes, multiple arrays may be aliases of each other, but they are never
updated in the program. For this case, we propose to indicate that the arrays
are immutable. By doing so, the deductive verifier can reason about them as if
they are sequences.
     Furthermore, in Section 5, we discuss a large number of experiments that
demonstrate how these features together speed up verification and verify previ-
ously unverifiable cases of a Radio Telescope Pipeline case study, including an
implementation of the Padre algorithm [23].
     Finally, related work is discussed in Section 6, and conclusions are drawn in
Section 7. The data for the experiments (Section 5), the Lean proof (Section 3),
and the version of the VerCors tool used in this paper can be found in an
              Scalable Deductive Verification of Data-Level Parallel Programs                3


Listing 1: An OpenCL GPU kernel to swap the contents of two arrays, inspired
by the Xswap kernel from CLBlast [19].
 1   /*@ ...
 2       context (∀ int i; 0 ≤ i ∧ i < n/get_global_size(0);
 3         Perm(ygm[\gtid + i*get_global_size(0)], write)) ∧
 4         Perm(xgm[\gtid + i*get_global_size(0)], write));
 5       ensures (∀ int i; 0 ≤ i ∧ i < n/get_global_size(0);
 6         ygm[\gtid + i*get_global_size(0)] ≡ \old(xgm[\gtid + i*get_global_size(0)]) ∧
 7         xgm[\gtid + i*get_global_size(0)] ≡ \old(ygm[\gtid + i*get_global_size(0)]));
 8   @*/
 9   // Swap the contents of two arrays in parallel.
10   __kernel void XswapFast(const int n, __global float* xgm, __global float* ygm) {
11     /*@ loop_invariant \gtid ≤ id ∧ id < n + get_global_size(0);
12         loop_invariant (∀ int i; 0 ≤ i ∧ i < n/get_global_size(0);
13           Perm(ygm[\gtid + i*get_global_size(0)], write)) ∧
14           Perm(xgm[\gtid + i*get_global_size(0)], write));
15         loop_invariant (∀ int i; id/get_global_size(0) ≤ i ∧ i < n/get_global_size(0);
16           ygm[\gtid + i*get_global_size(0)] ≡ \old(ygm[\gtid + i*get_global_size(0)]) ∧
17           xgm[\gtid + i*get_global_size(0)] ≡ \old(xgm[\gtid + i*get_global_size(0)]));
18         loop_invariant (∀ int i; 0 ≤ i ∧ i < id/get_global_size(0);
19           ygm[\gtid + i*get_global_size(0)] ≡ \old(xgm[\gtid + i*get_global_size(0)]) ∧
20           xgm[\gtid + i*get_global_size(0)] ≡ \old(ygm[\gtid + i*get_global_size(0)]));
21     @*/
22     for (int id = get_global_id(0); id < n; id += get_global_size(0)) {
23       float temp = xgm[id];
24       xgm[id] = ygm[id];
25       ygm[id] = temp;
26     }
27   }




accompanying artefact at http://github.com/cav2026-anonymous/Scalabl
e-Deductive-Verification-of-Data-Level-Parallel-Programs.


2    Background

Deductive verification tools use formal contracts, consisting of pre- and post-
conditions, written as requires and ensures statements, respectively, to formally
verify a program. To support concurrent programs, the VerCors [1] tool uses
first-order logic, enhanced with (concurrent) separation logic concepts [5]. For
each memory location (or heap location) a, one needs to specify a permission to
access it: Perm(a, p), with p a fractional number between 0 and 1, where p≡1
indicates that we can write to location a and 0<p<1 indicates read permission. A
permission of 1 is often written as write. Correct permission annotations allow
VerCors to prove memory safety. To verify a program, VerCors translates
it into Viper’s [18,8] intermediate verification language. In turn, Viper queries
SMT solvers to solve the proof obligations.
    Listing 1 presents an example of an OpenCL GPU kernel that can be used
to swap the contents of two arrays xgm and ygm, both of size n, in parallel.
The special comments /*@ and @*/ indicate annotations. The contract for this
function addresses that the array contents are indeed swapped: at lines 2–4 (l.2–
4), the context is given that the kernel has write permission for both arrays
4       L. B. van den Haak, A.J. Wijs and M. Huisman

(context refers to the fact that this holds both before and after executing the
kernel), and at l.5–7, the postcondition is given that the array contents have
been swapped, with \old referring to the old contents of the arrays before the
kernel was launched. A number of keywords and functions are used to refer to
the thread hierarchy on a GPU. Using CUDA terminology, threads are executed
in blocks of a predefined size, and a predefined number of blocks make up a grid.
Both blocks and grids can be one-, two-, or three-dimensional. In this example,
we use only one dimension. We use the following functions, with i referring to
a dimension (0 ≤ i ≤ 2):
  – get_local_size(i) returns the size of a thread block in the i-dimension.
  – get_num_blocks(i) returns the total number of blocks in the i-dimension.
  – get_local_id(i) returns the (block-local) ID of the current thread in the
    i-dimension. Note that 0 ≤ get_local_id(i) < get_local_size(i).
  – get_block_id(i) returns the ID of the block in which the thread resides in
    the i-dimension. Note that 0 ≤ get_block_id(i) < get_num_blocks(i).
  – get_global_id(i) returns the global ID of the thread in the i-dimension,
    defined as get_local_size(i) · get_block_id(i) + get_local_id(i).
  – get_global_size(i) returns the total number of threads in the i-dimension,
    defined as get_num_blocks(i) · get_local_size(i).
    Finally, \gtid is equal to get_global_id(0) for the one dimensional case.
    Note that these functions are used to divide the work among the threads:
Initially, every thread accesses those elements in xgm and ygm located at in-
dex get_global_id(0). As the arrays can be larger than the total number of
threads, the for-loop at l.22–26 is actually a grid-stride loop, which is very com-
mon in GPU kernels: after accessing their initial element, every thread jumps
get_global_size(0) positions ahead in the arrays to access the next elements,
and this continues until the end of the arrays has been reached. To reason about
the loop, note the loop invariants at l.11–21 that also use the functions men-
tioned above. These are essential for VerCors to prove the contract of the
kernel.
    VerCors encodes parallel functions, such as GPU kernels, using parallel
blocks. To verify a GPU kernel, one needs to quantify over all thread blocks in
a grid and all threads in each thread block [4], resulting in two nested parallel
blocks. We have made this explicit in Listing 2, using VerCors’ intermediate
language Pvl. For convenience, the grid-stride loop has been removed. Note that
the contract for the parallel block labelled blocks quantifies over all threads in
a block, and that the contract for the kernel in turn quantifies over all threads in
the grid. Although given here explicitly, VerCors typically derives these con-
tracts automatically from a given contract for a thread block, which is possible
due to the very structured way in which GPU threads operate. For the kernel
in Listing 1, VerCors would also internally generate these contracts, given the
contract at l.1–8.

Triggers. Contracts for deductive verification frequently involve quantifiers, for
instance in a statement such as ∀int i; 0≤i<n; A[i]≡0. During verification,
a deductive verification tool needs to apply such a statement whenever appli-
               Scalable Deductive Verification of Data-Level Parallel Programs              5


Listing 2: A GPU PVL kernel to swap the contents of two arrays, with the
number of threads being at least as large as the number of elements.
 1   /*@ ...
 2       ensures ∀ int i; 0 ≤ i ∧ i < n*m; xgm[i] ≡ \old(ygm[i]) ∧ ygm[i] ≡ \old(xgm[i]);
 3   @*/
 4   void XswapFastSmallArrays(const int n, float* xgm, float* ygm, int nb, int nt) {
 5     par blocks (int bid = 0 .. nb)
 6     {
 7       /*@ ...
 8           ensures ∀ int i; 0 ≤ i ∧ i < n; xgm[bid*nt + i] ≡ \old(ygm[bid*nt + i]);
 9           ensures ∀ int i; 0 ≤ i ∧ i < n; ygm[bid*nt + i] ≡ \old(xgm[bid*nt + i]); @*/
10       par threads (int tid = 0 .. nt)
11         /*@ ...
12             ensures xgm[bid*nt + tid] ≡ \old(ygm[bid*nt + tid]);
13             ensures ygm[bid*nt + tid] ≡ \old(xgm[bid*nt + tid]); @*/
14       {
15         float temp = xgm[bid*nt + tid];
16         xgm[tid] = ygm[bid*nt + tid];
17         ygm[tid] = temp;
18       }
19     }
20   }




Listing 3: A PVL function example to illustrate triggers. Here f is some unin-
terpreted side-effect free function.
1    /*@ requires x>0 ∧ y>0;
2        requires (∀ int k; 0≤k ∧ k≤x ; {: f(k, y) :} ≡ 0);
3        requires (∀ int k, int i; 0≤k ∧ k≤x ∧ 0≤i ∧ i≤y; f(k*i, z) ≡ 0); @*/
4    void bar(int x, int y, int z) {
5        assert f(x, y) ≡ 0; // this verifies, as "f(x,y)" triggers the first quantifier
6        assert f(10, z) ≡ 0; // this assertion fails, as no quantifier is triggered
7    }




cable, for instance when encountering the ground term A[1] in the code: the
quantifier must be instantiated. Mapping 1 on i is straightforward, but for more
complex expressions, heuristics are typically required, although they often lead to
incompleteness of the verification. Therefore, VerCors relies on pattern-based
quantifier instantiation [7] (or E-matching): the user should indicate that an ex-
pression in an annotation should serve as a trigger (or pattern) for quantification,
by enclosing it in {: and :}. This trigger (or possibly a set of triggers) should
mention all quantified variables. Furthermore, Viper’s intermediate verification
language does not allow triggers to involve arithmetic expressions.
    For instance, consider the code and contract in Listing 3. At l.2, f(k,y) is
marked as a trigger. The assertion at l.5 verifies, as f(x,y) matches the trigger
at l.2. However, the assertion at l.6 fails to verify, as in order to match f(10,z)
needs the information of the quantifier in l.3. However, it is not allowed to specify
f(k*i,y) as a trigger, as it contains arithmetic. Even if we introduce a helper
function for *, such that it can be used as a trigger, it cannot match suitable
instances for i and k when given f(10), as this would need to be written as
f(5*2), f(2*5), f(1*10) or f(10*1).
6       L. B. van den Haak, A.J. Wijs and M. Huisman

3   Triggers for Nested Quantifiers
As data-level parallel programs typically involve data stored in arrays, their
contracts usually contain annotations that quantify over the data elements. To
reason about these, the underlying automated solver used by a deductive veri-
fication tool needs to automatically find instantiations of those quantifiers. To
illustrate this, consider Listing 1 again, in particular, the postcondition given at
l.5–6. We indicate that the index expression for ygm should be used as a trigger:
    ∀ int i; 0 ≤ i < n/get_global_size(0); {:ygm[\gtid + i*get_global_size(0)]:} ≡
      \old(xgm[\gtid + i*get_global_size(0)])

When trying to verify the kernel, the solver tries to find suitable instantiations
of the quantified variables in the given postcondition, but is not able to do this,
as the index expression contains arithmetic operations.
    The solution that we develop here is to automatically rewrite the quantifier
expression in such a way that the arithmetic operations are removed from the
trigger. We do this by defining a bijective mapping from a linear arithmetic
expression containing quantified variables to a single quantified variable, and
adding suitable conditions, such that the validity of the expression remains un-
changed. For this concrete example, assuming for the moment that \gtid is a
given value instead of one calculated using several values, this gives the following
rewritten quantifier.
    ∀ int x; (abs(x-\gtid))%get_global_size(0)≡0 ∧ 0 ≤ x-\gtid < get_global_size(0)*(n/
      get_global_size(0)); ygm[x] ≡ \old(xgm[x]);

After the rewriting, ygm[x] can be used as a trigger. In this section, we explain
our rewriting procedure. In general, if an index is computed injectively, then
we can apply this rewriting by determining an inverse function. If we have an
indexing function and its inverse, we can translate between the original and the
rewritten quantifier.

Rewriting quantifiers. In general, the quantifiers we wish to rewrite are of the
following form, with A an array.
    ∀ int x1 , ..., xk ; X(x1 , ..., xk ); R(A[ak *xk + ... + a1 *x1 + b], (x1 , ..., xk ))

    The predicate X(x1 , ..., xk ) determines the domain of the quantifier, i.e.,
all values of (x1 , ..., xk ) for which the quantifier holds. Furthermore, R is a
predicate with free variables x1 , . . . , xk that may involve conditions on the xi ,
besides the definition of their domains and the index expression. Based on the
index expression in the quantifier form given above, we define a function for
array indexing:
                                                                      k
                                                                      X
             f (x1 , . . . , xk ) = ak · xk + · · · + a1 · x1 + b =         ai · xi + b
                                                                      i=1

Reversing this indexing would mean that we could use a statement such as A[x]
as a trigger, and map x back to the corresponding (x1 , ..., xk ) that satisfies
              Scalable Deductive Verification of Data-Level Parallel Programs             7

f (x1 , . . . , xk ) = x. To achieve this, we need to define the inverse function f −1 . For
this to work, it must be that each xi has an (inclusive) lower bound min i defined
in the domain X. When the domain also has an (exclusive) upper bound for an
xi , we denote this by max i . The upper bound max k for xk must be defined, to
bound the overall quantification. With nk = max k − min k , we refer to the size
of the xk -dimension. All in all, this means that X(x1 ,...,xk ) should be defined
as follows.
                                                     k
                                                     ^
             X(x1 , ..., xk ) = C(x1 , ..., xk ) ∧       (min i ≤ xi ) ∧ xk < max k
                                                     i=1

Here, C(x1 ,..., xk ) is a predicate expressing additional constraints on the
variables, besides the constraints for the bounds. With X as above, we wish to
rewrite the original quantifier to an equivalent quantifier with a single variable,
of the following form.
    ∀ int x; Y(x); R(A[x], f −1 (x))

    Here, the predicate Y(x) determines the domain of the new quantifier. To
define f −1 , we first define an offset off and a helper function base i . Intuitively,
off is the value where we start indexing array A, which is the position related
to the case where each xi has its lowest possible value. The function base i maps
x back to ai · xi , meaning that we can retrieve xi by computing base i (x)/|ai |.
                                 k
                                 X
                         off =         ai · min i + b
                                 i=1
                                 (
                                     |x − off |                   if i = k,
                  base i (x) =
                                     base i+1 (x) mod ai+1        if 1 ≤ i < k.
   Next, we can define the function f −1 as follows.
            f −1 (x) = (base 1 (x)/|a1 | + min 1 , . . . , base k (x)/|ak | + min k )
This rewriting is correct, provided that
                                             nk > 0                                      (1)
and the following conditions hold for all ai (1 ≤ i ≤ k).
                       ai ̸= 0                                                           (2)
             i < k ⇒ ai ≥ 0 ⇐⇒ ai+1 ≥ 0                                                  (3)
                                                i
                                                X
             i < k ⇒∀(x1 , . . . , xk ) ∈ X,           |aj | · (xj − min j ) < |ai+1 |   (4)
                                                j=1

   Finally, we define Y(x) as follows.
   Y(x) = C(f −1 (x)) ∧ base 1 (x) mod a1 = 0 ∧
          (a1 > 0 ⇒ 0 ≤ x − off < ak · nk ) ∧ (a1 < 0 ⇒ ak · nk < x − off ≤ 0)
   The following theorem states the correctness of our rewriting.
8        L. B. van den Haak, A.J. Wijs and M. Huisman

Theorem 1. Given a quantifier of the form ∀ int x1 , ..., xk ; X(x1 , ...
, xk ); R(A[ak *xk + ... + a1 *x1 + b], (x1 , ..., xk )), with k > 0. If equa-
tions 1–4 hold, then
       ∀(x1 , . . . , xk ) ∈ Zk .X(x1 , . . . , xk ) ⇒ R(A[f (x1 , . . . , xk )], (x1 , . . . , xk ))
                                                    =
                                  ∀x ∈ Z.Y(x) ⇒ R(A[x], f −1 (x))
with f and f −1 as defined above.

Proof sketch. A full proof has been written in about 2500 lines of Lean 4 [16]
code, and can be found in the accompanying artefact of the current paper. For
details on this, see Appendix A. Here, we provide a sketch of how this proof is
structured. With X and Y , we refer to the domains determined by predicates
X(x1 ,...,xk ) and Y(x), respectively. Initially, the theorem can be proven for
the case that C(x1 ,...,xk ) = true, min i = 0 for all i and b = 0. This implies
that off = 0. In this case, it can be proven that ∀x ∈ Y.f (f −1 (x)) = x and that
∀(x1 , . . . , xk ) ∈ X.f −1 (f (x1 , . . . , xk )) = (x1 , . . . , xk ). This proves that f and f −1
are inverses on X and Y .
    Next, we prove that the image of f under X is contained in Y , and vice
versa for f −1 . This, together with the first part of the proof, proves that f is a
bijection between X and Y .
    Subsequently, this is generalised to the case where b, off and the min i have
arbitrary values. We prove that the definitions of f and f −1 can be constructed
from the simpler ones used at the start of the proof, using function composition.
Then, we prove that the function compositions are also inverses and bijections.
    Then, we prove that the theorem is still correct for an arbitrary predicate
C(x1 ,...,xk ). As this predicate introduces the same constraints for both X and
Y , both domains are restricted in the same way.
    Finally, we prove that f and f −1 being inverses and f being a bijection be-
tween X and Y implies the equality of the two quantifiers.                                          ⊓
                                                                                                    ⊔

    Next, we revisit the example taken from Listing 1.
Example 1. Consider again the following quantifier.
     ∀ int i; 0 ≤ i < n/get_global_size(0); {:ygm[\gtid + i*get_global_size(0)]:} ≡
       \old(xgm[\gtid + i*get_global_size(0)])

Note that it matches the linear quantifier pattern, with b = \gtid, x1 = i,
a1 =get_global_size(0), min 1 = 0 and max 1 =n/get_global_size(0). Fur-
thermore, there is no C-predicate. From this, we can derive that off = \gtid
and base 1 (x) = |x − \gtid| and n1 =n/get_global_size(0), leading to Y(x) =
|x−\gtid| mod get_global_size(0) = 0∧0 ≤ x−\gtid < get_global_size
(0) · (n/get_global_size(0)). As previously stated, this produces the follow-
ing new quantifier.
     ∀ int x; (abs(x-\gtid))%get_global_size(0)≡0 ∧ 0 ≤ x-\gtid < get_global_size(0)*(n/
       get_global_size(0)); ygm[x] ≡ \old(xgm[x]);
              Scalable Deductive Verification of Data-Level Parallel Programs     9

                                              x3
                                      x1               x1
                                0 1 2 3    10111213
                             x2 4 5 6 7 x2 14151617
                                8 9        1819


                    0 1 2 3 4 5 6 7 8 9 1011121314151617 1819
                                               x

     Figure 1: An example of storing two matrices together in one array.


The second condition may be confusing, but note that with integer division,
get_global_size(0)*(n/get_global_size(0)) is not necessarily equal to n
. Furthermore, note that x represents the original index expression \gtid+
i*get_global_size(0), hence x - \gtid equals i*get_global_size(0). From
this, we can derive that 0 ≤i*get_global_size(0)<get_global_size(0)* (
n/get_global_size(0)), which implies 0 ≤i <n/get_global_size(0), i.e.,
the condition for i in the original quantifier.

    Besides the use of block and thread IDs for array accessing, another cause for
quantifier issues is the flattening of multi-dimensional arrays, such as matrices.
To achieve regular memory access patterns, it is generally a good strategy to
store matrices in one-dimensional arrays, sometimes even multiple matrices in a
single array. In the following example, we address such a situation.

Example 2. Consider Figure 1, with two matrices stored into a single, one-
dimensional array. A quantifier suitable for the original, non-flattened matrices
is the following.
    ∀ int x1 , int x2 , int x3 ; 0≤x1 <4 ∧ 0≤x2 <3 ∧ 0≤x3 <2 ∧ 4*x2 +x1 <10;
      A[10*x3 +4*x2 +x1 ]>x2 ;

Note the constraint 4*x2 +x1 <10, which ensures that the grey cells are not ac-
cessed. It serves as the C-constraint in the definition of X(x1 ,...,xk ). Note also
that every time x2 is incremented, we jump four elements ahead in the flattened
array, corresponding to the upper-bound of x1 , and when x3 is incremented, we
jump ahead ten elements, due to the constraint 4*x2 +x1 <10. To rewrite this
quantifier, first note that a1 = 1, a2 = 4, and a3 = 10. Furthermore, we have
off = 10·0+4·0+0+0 = 0, base 3 (x) = x−0 = x, base 2 (x) = base 3 (x) mod 10 =
x mod 10, and base 1 (x) = base 2 (x) mod 4 = (x mod 10) mod 4. This means that
Y(x) is defined as 4 · ((x mod 10)/4) + ((x mod 10) mod 4)/1 < 10 ∧ ((x mod
10) mod 4) mod 1 = 0∧0 ≤ x < 10·2. Note that ((x mod 10) mod 4) mod 1 = 0
is always true, and so is 4 · ((x mod 10)/4) + ((x mod 10) mod 4)/1 < 10 (remem-
ber that ‘/’ refers to integer division that discards any remainder). This leads to
the following new quantifier.
    ∀ int x; 0≤x<2*10; A[x]>((x%10)/4);
10      L. B. van den Haak, A.J. Wijs and M. Huisman

     Sometimes, the rewriting procedure may result in nonlinear subexpressions.
For example, consider the following quantifier, with positive integers n1 , n2 : ∀int
  x1 , int x2 ; 0≤x1 <n1 ∧0≤x2 <n2 ∧x1 %2≡0; A[x1 +n1 *x2 ]>0. This is rewrit-
ten to ∀int x; 0≤x<n1 *n2 ∧(x%n1 )%2≡0; A[x]>0. This quantifier contains
subexpressions x%n1 and n1 *n2 , which are both nonlinear. It depends on the
capabilities of the underlying SMT solver whether this poses a problem. One
could alternatively add additional lemmas to resolve this.
     Other verifiers, such as Dafny [14] and Viper, often introduce additional
structure as a way to circumvent the restriction that arithmetic is not allowed
in triggers. With this approach, one could define, for instance, acc(int x,
int b, int a)= x*a + b allowing you to write A[acc(x, b, a)] as a trigger.
One issue is that you must modify the code to be verified to always use this
indexing. Furthermore, some programs will access arrays in various ways. For
example, performing a reduction in a GPU kernel or applying loop-tiling will lead
to different access patterns. In those cases, your quantifier will not instantiate
anymore. For successful verification, one needs to add complicated verification
lemmas relating the different access functions to properly trigger the quantifiers
again.
     However, the quantifier rewrite method of this section can be combined with
this additional structure, which is what we have done for the GPU experiments
of Section 5. We use the function int acc1d(int x, int b, int n, int a)=
x*a + b to add additional structure. Therefore, an example trigger used in the
complete version of Listing 1 has the following structure: xgm[acc1d(\gtid+
  i*get_global_size(0), x_offset, n, x_inc)]. The benefit is twofold: (1)
we can easily access the array in other ways since less structure is present, and (2)
we can add additional nonlinear information to the contract of the acc1d. This
additional information helps in dealing with potential incompleteness caused by
nonlinearity.

Implementation in VerCors. The rewriting procedure described in this section
has been implemented in VerCors. To check whether the conditions are met
for a quantifier marked as a trigger by the user, VerCors needs to take into
account the context of surrounding annotations and statements. Often, equations
1–3 can be derived with basic reasoning. Equation 4, however, tends to be harder
to determine. For this reason, we identified Lemma 1, found in the Appendix,
that simplifies checking this condition. We added a straightforward symbolic
evaluator to VerCors to verify whether all conditions are satisfied.
    Finally, even though the rewriting procedure is described for an index expres-
sion consisting of a single linear pattern ak *xk + ... + a1 *a1 + b, our imple-
mentation contains a generalisation of this, supporting the detection of multiple
linear patterns in an expression. By recursively replacing such patterns with sin-
gle variables using the rewriting procedure, the complete expression is simplified
such that it can be used as a trigger.
             Scalable Deductive Verification of Data-Level Parallel Programs    11

4   Unique and Immutable Types for Arrays

Data-level parallel programs tend to work with data stored in arrays, often more
than one. Unfortunately, as this number of arrays increases, the verification time
tends to grow quadratically [23], making programs often unverifiable. A major
cause for this is that permission quantifiers, as used in separation logic [17],
require numerous internal checks for completeness, and these quantifiers are
essential for verifying parallel programs. For instance, Listing 1 uses permission
quantifiers at l.2–4, to indicate that a thread executing the kernel is allowed to
write to particular array cells. The internal checks are needed, since permissions
could be combined in case the arrays overlap in memory, and program correctness
may depend on this. Over time, the heuristics used in deductive verifiers to
reason about arrays possibly overlapping, and the effects of that happening,
have improved, but for complex programs, this problem has not been solved.
    However, we observe that in the case of data-level parallel programs, often
(1) the contents of some arrays remain constant throughout the program, and
(2) different arrays typically do not overlap in memory. To exploit this, we intro-
duce the type qualifiers immutable and unique to reduce the number of required
verification checks.
    Before discussing the type qualifiers, we address why verification times tend
to grow rapidly as the number of arrays increases, at least with the symbolic
execution technique for quantified permissions used by Viper [17].
    A permission quantifier is, internally in Viper, modelled as a quantified heap
chunk, i.e., a function that takes a memory reference r.f, with r a quantified
(reference-typed) receiver and f a field, and returns a tuple (v(r), p(r)), con-
sisting of a symbolic value v(r) and a (symbolic) permission p(r) ∈ ⟨0, 1]. For
example, before processing quantifier ∀int i; 0≤i<9 ⇒Perm(xs[i], 1\2), a
new chunk is produced mapping each of the first nine elements of xs to a symbolic
field value and a 1\2 permission. Subsequent quantifiers for the same array(s)
produce additional chunks, as opposed to updated existing ones. Whenever an
assertion is processed, a snapshot is created, which contains the chunks that are
relevant for the assertion, i.e., that contain the symbolic values referred to in
the assertion [21]. To avoid inconsistencies, Viper needs to periodically com-
pare snapshots to check if they are the same. This is because a function call to
a side-effect-free function is considered equal if all the arguments are the same,
including heap-dependent arguments. This involves comparing all the chunks of
one snapshot with all the chunks of the other snapshot, causing the quadratic
execution time.

Immutable qualifier. With the immutable qualifier for (a pointer to) an array, for
instance in immutable int* xs, we propose to indicate that the pointer refers
to data that does not change throughout execution of the program. For such
pointers, in VerCors, the data can be encoded using an immutable sequence,
as opposed to a mutable pointer block. Elements of a sequence are not stored
on the heap.
12        L. B. van den Haak, A.J. Wijs and M. Huisman


     Listing 4: Examples of unique type modifier used on pointers and structs.
 1    /*@unique<1>@*/ int* xs1; // The pointer points to integers with uniqueness number 1
 2    int /*@unique<1>@*/* xs2; // The same type as above
 3    xs1 = xs2; // Allowed: both have the same uniqueness number for their integers
 4    int /*@unique<2>@*/* xs3; // This involves integers with uniqueness number 2
 5    xs1 = xs3; // Not allowed: the pointers have different uniqueness numbers
 6    /*@unique<1>@*/ int a; // Uniqueness not relevant, as integers are not stored on heap
 7    xs1 = &a; // Address of a is tracked as heap variable, hence uniqueness number matters
 8    int* /*@unique<1>@*/ * zs; // The zs pointer has uniqueness number 1
 9    xs1 = *zs; // Not allowed: *zs values do not have a uniqueness number
10    struct v { int n; int* xs; /*@unique<2>@*/ int* ys; }; // Uniqueness used in a struct
11    struct v a; // A struct stored in variable a with uniqueness numbers as defined for v
12    /*@unique_field<n,1>@*/ struct v b; // Member n has uniqueness number 1
13    /*@unique_pointer_field<xs,1>@*/ struct v c; // Type of xs member is unique<1> int *
14    a.xs = xs1; // Not allowed: a.xs* values do not have a uniqueness number
15    c.xs = xs1; // Allowed: the uniqueness numbers match
16    xs1 = &(b.n); // Allowed: the uniqueness numbers match
17    void sort(int* xs, int len){...} // A previously defined sorting function
18    int f(/*@unique<1>@*/int* xs, int n){
19      sort(xs, n);
20    }




   With this new qualifier, functions can be defined with immutable pointer
parameters. However, when called, the given pointer argument may not be im-
mutable. To allow this, the mutable pointer needs to be coerced to an immutable
one. Once this has happened, the pointer cannot be changed anymore. This is
achieved by requiring that the mutable pointer releases a positive amount of
permission for each of its elements when coerced.

Unique type qualifier. We propose the unique<i> type qualifier to distinguish
non-overlapping data, allowing for a more efficient encoding in Viper. Here, i
is a uniqueness number : only pointers of the same type and that have the same
uniqueness number can potentially alias. Unique type qualifiers are applicable
for all heap locations, such as arrays, pointers, members of structs, and fields of
classes. In Listing 4, we show several examples of how this qualifier can be used,
including some restrictions. For instance, xs1 (l.1) and xs3 (l.4) have the same
type, but different uniqueness numbers, making the assignment at l.5 illegal. At
l.7, the address of a is queried, resulting in the variable being stored on the heap
as an integer with uniqueness number 1 (l.6).
     Like const in C, the unique type qualifier associates to the left, and pointer
markers (*) denote uniqueness at different levels. For example, at l.8, the content
of zs, of integer pointer type, has uniqueness number 1. Yet, the inner pointer
of zs has no uniqueness number, so the assignment at l.9 is not allowed.
     Unique types can also be applied to struct members, see l.10. Sometimes, it
may be known that different struct instances do not overlap their internal data.
For this purpose, we propose the type qualifier annotations unique_field and
unique_pointer_field. These features are demonstrated at l.11–16.
     Heap locations in Viper are encoded using fields, with all memory locations
of the same type using the same field. When using the unique type qualifiers,
types with different uniqueness numbers use different fields. When comparing
             Scalable Deductive Verification of Data-Level Parallel Programs    13

snapshots, as mentioned earlier, only chunks that refer to the same field are
compared. Therefore, by separating non-overlapping arrays into different fields,
significant verification time improvements can be achieved. For more on the
practical impact of this, see Section 5.
    Finally, previously defined functions, as, for instance, provided in libraries,
should be usable in combination with unique type qualifiers. For instance, con-
sider l.19, where the integer array xs with uniqueness number 1 is given as
parameter to a predefined sorting function (l.17), in which uniqueness num-
bers are not given. This will not type check, as sort accepts only non-unique
arrays. However, such function calls should be supported regardless of the ex-
act uniqueness number, as long as uniqueness between arrays is respected We
consider a function call consistent if the type signature of a call partitions the
parameters in the same way as the called function. For example, a function f
(unique<0>int* x, unique<0>int* y) can be called with both arguments of
type unique<1>int*, but not if one has type unique<0>int* and the other
has type unique<1>int*.


5   Experiments

In this section, we evaluate the effectiveness of the techniques proposed in Sec-
tions 3 and 4 to verify data-level parallel programs. Regarding the rewrite pro-
cedure of Section 3, the conclusion is clear: none of the experiments we report on
in this section were verifiable without the use of this procedure. Using the type
qualifiers unique and immutable further improves the verification of data-level
parallel programs that contain multiple arrays.
     We chose three representative sets of experiments that heavily rely on quan-
tifiers and flattened multi-dimensional arrays. The first set contains the GPU
kernels from the CLBlast library [19], consisting of OpenCL kernels that im-
plement the Basic Linear Algebra Subprograms (BLAS). These experiments are
conducted to evaluate whether our proposed techniques are applicable to typical
GPU kernels. The next two sets of experiments were chosen from [22,23], among
which is an implementation of the Padre algorithm, as part of the software for a
Radio Telescope Pipeline [23]. In these papers, the authors ran into limitations
of the underlying verifiers due to the many arrays and quantifiers present. These
works contain optimised parallel CPU programs generated from the Domain Spe-
cific Language Halide [20]. The HaliVer [22] tool adds verification annotations
to these programs such that they can be verified by VerCors.

Set-up. We used a machine with an 11th Gen Intel Core i7-11800H @ 2.30GHz
and 32GB of RAM running Ubuntu 23.04. We ran each experiment ten times
and reported the average of these. The VerCors version used is included in the
accompanying artefact. We ran VerCors with the options --silicon-quiet
--dev-time-backend --dev-total-timeout=3600 --dev-assert-timeout 60
--target x86_64-linux-gnu, and used the Silicon verifier of Viper, which is
based on symbolic execution. Additionally, the experiments from [22,23] were
14                                                 L. B. van den Haak, A.J. Wijs and M. Huisman


                                                                                                                                                                Variant
                                             160                                                                                                                 Base
                                                                                                                                                                 Unique
     Backend verification time (% of Base)   140                                                                                                                 Immutable
                                                                                                                                                                 Extract
                                             120                                                                                                                 All

                                             100




                                                                                                                            8s
                                                   34s

                                                               20s

                                                                           62s




                                                                                                 20s




                                                                                                                    21s




                                                                                                                                        66s
                                                                                   101s




                                                                                                         581s




                                                                                                                                                  912s
                                              80
                                              60
                                              40
                                              20
                                               0
                                                                                9 9    8                     8




                                                                                                                                                         l
                                                       x


                                                                   m




                                                                                                    ot




                                                                                                                        2




                                                                                                                                                        a
                                                     ma




                                                                                                                     rm
                                                                                                           ad




                                                                                                                               al
                                                                              y

                                                                                      py




                                                                                                                                           ap


                                                                                                                                                    Tot
                                                                   su




                                                                                                  xd
                                                                            xp




                                                                                                                            xsc
                                                                                                         xh


                                                                                                                    xn
                                                                                   xco




                                                                                                                                        xsw
                                                               xa
                                                   xa




                                                                          xa




                                                                                                         (a) Level 1
                                             175                                                                                                                 Variant
                                                                                                                                                                   Base
                                                                                                                                                                   Unique
                                             150                                                                                                                   Const
     Backend verification time (% of Base)




                                                                                                                                                                   Extract
                                             125                                                                                                                   All

                                             100
                                                                                          778s
                                                   1760s



                                                                        2121s




                                                                                                           1030s



                                                                                                                            1825s



                                             75                                                                                                 7513s

                                             50

                                             25

                                              0
                                                           6       9             953             3 95               24              8     9
                                                                                                                                                          l
                                                               v




                                                                                                                                                            a
                                                        em




                                                                                                                                   sv
                                                                                                                  e r2
                                                                                               er
                                                                              er




                                                                                                                                                        Tot
                                                                                             xh




                                                                                                                               xtr
                                                                            xg
                                                      xg




                                                                                                                xh




                                                                                                         (b) Level 2

Figure 2: Verification of CLBlast kernels, normalized so Base=100%. Base is
compared against versions with unique type qualifiers (Unique), immutable
arrays (Immutable), extracted kernel bodies (Extract), and All which enables
all these features. Below the bars: number of successful runs (✓= 10/10, ✗ 0/10).
Next to base bars: average time of the 10 base runs in seconds. The † indicates
we (try to) prove functional correctness in addition to memory safety.


also run with --no-infer-heap-context-into-frame as these options were
also used in the original experiments.

GPU body extraction. Verifying monolithic functions can be more costly than
verifying code that is functionally the same but is divided into several func-
tions. The slowdown mainly occurs because the underlying SMT solver has too
much information. Additionally, as mentioned in Section 4, too many program
               Scalable Deductive Verification of Data-Level Parallel Programs                           15


          Table 1: Reverification of the experiments presented in [22].
                         Base    Qualifiers                                        Base   Qualifiers
Name       V Result #      T σ # T σ Speedup        Name             V Result #      T σ # T σ Speedup
blur       0 ✓      10     13 1 10 9      1 1.4     blur             0 ✓      10     13 1 10 10    1 1.3
           1 ✓      10     14 1 10 10     1 1.4                      1 ✓      10     13 1 10 10    1 1.3
           2 ✓      10     18 1 10 13     1 1.4                      2 ✓      10     17 1 10 14    3 1.2
           3 ✓      10     20 1 10 20     7 1.0                      3 ✓      10     14 1 10 11    1 1.4
hist       0 ✓      10     25 1 10 26     7 1.0     hist             0 ✓      10     22 1 10 15    1 1.5
           1 ✓      10     30 1 10 17     1 1.7                      1 ✓      10     27 1 10 20    2 1.4
           2 ✓      10     42 1 10 23     1 1.8                      2 ✓      10     36 1 10 32 10   1.1
           3 ✓      10     79 3 10 32     2 2.5                      3 ✓      10     46 1 10 29    2 1.6
conv_layer 0 ✓      10    153 1 10 53     1 2.9     conv_layer       0 ✓      10    144 2 10 60    6 2.4
           1 ✓      10    171 1 10 72     6 2.4                      1 ✓      10    162 1 10 65    1 2.5
           2 ✓      10    246 3 10 71     1 3.5                      2 ✓      10    220 3 10 74    5 3.0
           3 ✓      10    227 2 10 68     1 3.3                      3 ✓      10    201 2 10 72    5 2.8
gemm       0 ✓      10     61 1 10 22     1 2.8     gemm             0 ✓      10     56 1 10 21    1 2.6
           1 ✓      10    133 1 10 45     4 2.9                      1 ✓      10    110 1 10 35    1 3.2
           2 ✓      10    250 11 10 131 18  1.9                      2 ✓      10    152 8 10 53    6 2.9
           3 Error 10            10                                  3 Error 10           10
auto_viz 0 ✓        10     19 1 9 21      2 0.9     auto_viz         0 ✓      10     18 1 10 21    4 0.9
             ✗       0            1 15    -                          1 ✓       9     34 1 10 45 10   1.3
           1 ✓       8     63 1 10 52     1 2.1                        ✗       1    266 - 0
             ✗       2    290 1 0                                    2 ✓      10     36 1 10 39 10   0.9
           2 ✓      10     67 1 10 55     1 1.2                      3 ✓      10     34 1 10 28    1 1.2
           3 ✓      10     49 1 10 36     1 1.4     bilateral_grid     ✓      10     48 1 10 39    1 1.2
Total                    1722 33   774   22   2.2   camera_pipe        ✓      10    205 7 10 122 14  1.7
                                                    depthwise_         ✓      10    201 2 10 143   1 1.4
                                                    separable_conv
(a) Functional correctness & Memory Total                                          1831 26   956   26   1.9
safety
                                                                 (b) Memory safety only




statements increase the number of quantified chunks, which harms performance.
Strategies for decomposing large programs into smaller functions for verification
have been previously explored in Dafny [14] and Gobra [26]. For GPU kernels, we
observed major improvements when the kernel body is extracted into a separate
function with its own contract and verified in isolation. Since these contracts are
almost identical to standard VerCors GPU-kernel contracts, we added an op-
tion to perform this extraction automatically via the extract_body annotation
for GPU kernels. We also evaluated this feature in our GPU experiments.



Results. The results are shown in Figure 2 and the Tables 1 and 2. All times
are in seconds, and we set a time out of 1 hour. We only report the backend
verification time (T ) and the standard deviation of the mean times (σmean ). For
the tables, we compare using unique and immutable type qualifiers (Qualifiers)
with not using them (Base). In all configurations, however, the rewriting pro-
cedure was applied, as this was essential to make the experiments succeed. The
verification result can be successful (✓), fail (✗), or time out (T.O.). With #,
we indicate how many times an experiment yielded a certain result, summing
up to 10 for each experiment. Speed-up is calculated by dividing T of the Base
version by T of the specific version for all results (✓, ✗ and T.O).
16      L. B. van den Haak, A.J. Wijs and M. Huisman


         Table 2: Reverification of the experiments presented in [23].
                Base Qualifiers                                 Base   Qualifiers
Version Result # T σ # T      σ Speedup       Version Result #    T σ # T σ Speedup
CB      ✓      10 56 1 10 48  1      1.2      CB      ✓      10 466 9 10 142 4    3.3
NCB     ✓      10 56 1 10 50  1      1.1      NCB     ✓       0         1 901   - 1.3
                                                      ✗      10 1028 58 9 780 89

                (a) step
                                                         (b) sub_direction
                  Base     Qualifiers                          Base     Qualifiers
Version Result #   T     σ #   T σ Speedup    Version Result #   T σ #       T σ Speedup
CB      ✓      0           10 961 14    3.4   CB      ✓      0          10 2799 38    1.2
        ✗      2 2086 1404 0                          ✗      6 3146 101 0
        T.O.   8    -    - 0                          T.O.   4    -   - 0
NCB     ✗      9 1139 131 6 1211 468          NCB     ✗      1 3589   - 0
        T.O.   1    -    - 4     -   -                T.O.   9    -   - 10     - -

          (c) solve_direction                         (d) perform_iteration



Evaluation of Section 4. The CLBlast experiments (Figure 2) cover the level 1
and level 2 subroutines of BLAS. Level 1 covers vector operations only, while
level 2 covers matrix–vector operations, which are more complicated. Kernels
with no immutable pointers (xswap, xscal) are not evaluated for immutable,
and kernels with only one pointer (xscal) are not evaluated for unique. In both
these cases, those versions would be the same as the Base version. We fixed
the thread block sizes of these experiments to a concrete value, as otherwise
verification of these kernels could run into incompleteness due to nonlinearity.
    These experiments show that applying type qualifiers is always a good idea
and can be up to 10 times faster. Similarly, extracting the body of a kernel is
always a good idea and speeds up verification (for ‘xscal’, the difference is not
statistically relevant). However, the combination of the techniques shows the
most impressive results, being up to 150 times faster for ‘xger’. Especially for
the more complex level 2 kernels, this leads to the results being less brittle (all
have ten out of ten successful verifications) or even being able to verify ‘xger’
and ‘xher2’ at all. In total, the combination of features (All) is 8.5 times faster
for the total time of level 1 and 10.8 times faster for level 2.
    For the experiments taken from [22] (Table 1), V indicates that each program
has up to four different Halide schedules that explore different optimisations that
influence parallelisation and the ordering of computations. Qualifiers combines
the use of the immutable and unique encodings.
    These experimental results demonstrate that using the immutable and unique
 qualifiers mostly has a positive influence. In total, the verification time is reduced
by a factor of more than 1.9. Again, this is a speedup achieved after having made
the benchmarks verifiable to begin with, by using the rewriting procedure.
    For the experiments taken from [23] (Table 2), we make a distinction between
versions with concrete bounds (CB) and non-concrete bounds (NCB). The NCB
versions contain nonlinear arithmetic, which can lead to incompleteness. The au-
             Scalable Deductive Verification of Data-Level Parallel Programs      17

thors of [23] tried to address this by adding verification lemmas about nonlinear
arithmetic, which only led to successful verification in some cases. In the original
experiments, the complete algorithm (perform_iteration) was not included as
it could not be verified. We, however, have been able to verify the CB version.
    The experimental results demonstrate that when successful verification is
possible, use of the encodings of Section 4 always speeds up the verification. In
addition, more importantly, it allows three cases to be verified that cannot be
verified without using the type qualifier encodings.

Evaluation of Section 3. All experiments above rely on the rewrite method of
Section 3. Without it, the benchmarks cannot be verified as they are. A similar
quantifier rewriter, in a rudimentary form, had been implemented in VerCors
before, but that approach had not been formally proven correct, nor described
in the literature. However, for the experiments in [22,23], the authors depended
on this rewriter for their results. The current paper proposes a more generally
applicable rewriter, involving better symbolic checks to detect patterns in quan-
tifiers, the first that enables complete verification of the Padre algorithm used in
the software of a Radio Telescope Pipeline. In addition, this rewriting procedure
is described in full detail, and refers to a Lean correctness proof.
     In principle, most quantifiers could be rewritten manually, but not those that
VerCors must introduce automatically for parallel blocks and GPU kernels,
which occur in most benchmarks. Among all experiments, gemm_3 is the only one
we could not verify. The rewriting procedure currently fails because its contract
uses a linear pattern with the modulo (%) operator, which is not yet supported.

Conclusion. In conclusion, the rewriting procedure is highly effective and allows
us to automatically find triggers for most of the data-level parallel programs we
considered. Additionally, the qualifiers of Section 4, especially when used in com-
bination with the kernel extraction method discussed in the current section, are
effective: they significantly reduce verification time and allow for the verification
of otherwise unverifiable results.


6   Related Work

We divide our related work into two parts. First, we discuss some other ap-
proaches to support reasoning about quantifiers. Dafny [14] defines symbolic
equivalent functions for several arithmetic operators, which can be used in trig-
ger patterns. This increases the expressiveness of trigger patterns. However, when
an array is accessed in a different way than the precise arithmetic form given
in the trigger, it will not instantiate. To achieve successful verification in these
cases, further complex reasoning about triggers is needed. Nonetheless, in the
special case where arrays are always accessed in the exact same way, this is
a valid alternative. Further, Dafny also supports a technique to automatically
identify suitable triggers [13] In this paper our focus is complementary, as we try
to increase the chances to find a matching pattern by rewriting the quantified
18      L. B. van den Haak, A.J. Wijs and M. Huisman

expressions so that they can be matched with a larger number of terms in the
specifications.
    Second, we look at related work that identifies special restrictions, such as
non-aliasing or immutability, by using types. Charguéraud and Pottier [6] pro-
pose ‘temporary read-only permissions’, an extension to standard separation-
logic permissions that can mark memory locations as temporarily read-only with-
out extra verification or specification overhead. This is similar to our immutable
type modifier, except that once an array is marked immutable, it stays that way.
In SYMPLAR [3], Bierhoff introduces symbolic permissions as an alternative
to fractional permissions. Users annotate types with @Excl (exclusive) or @Imm
(immutable), and SYMPLAR checks these annotations. Our approach is similar
but we integrate it with fractional permissions and still allow arrays with the
same uniqueness type to alias, capturing a wider range of behaviours. Haack and
Poll [10] present a type system for object immutability in Java. Our immutable
reference corresponds to their RdWr type qualifier. The idea is the same, how-
ever we work in a verification setting. They also describe ‘Read-only references’,
where the object’s state cannot be modified through this reference, analogous to
const pointers in C. A different encoding for read-only pointers seems feasible,
but would still require permission bookkeeping in a separation-logic setting.


7    Conclusions and Future Work
To improve the capabilities of deductive verifiers to verify data-level parallel
programs, first of all, we introduced a rewriting procedure for nested quantifiers,
which improves trigger matching, and thereby greatly contributes to more effi-
cient verification. We also introduced two special type qualifiers, to indicate that
arrays are immutable or are not aliases of each other. The use of these qualifiers
can be verified with type checking, and tend to greatly reduce verification time.
The experimental results demonstrate the advantages of our optimisations. With
these optimisations, we could significantly reduce verification times and verify
previously unverifiable cases of a Radio Telescope Pipeline case study [23]. In
addition, employing all the suggested encoding optimisations makes the verifi-
cation, on average, 9 times faster for the CLBlast GPU kernels, with maximum
improvements of up to 150 times faster.
    For future work, we see several possibilities for further improvements. For
instance, we could add our rewriting procedure directly to Viper, allowing it to
query the SMT solver immediately when Equations 1–4 need to be checked. This
has the advantage that the program state is already modelled at that point, and
it enables other Viper front-ends to reuse our rewriting technique.
    In addition, it would be interesting to investigate whether the unique type
qualifier can be automatically applied in a program based on the results of some
static analysis. This would grant the programmer the benefits of this qualifier
without burdening them with the annotation task.
             Scalable Deductive Verification of Data-Level Parallel Programs        19

References
 1. Armborst, L., Bos, P., van den Haak, L.B., Huisman, M., Rubbens, R., Şakar, Ö.,
    Tasche, P.: The VerCors Verifier: A Progress Report. In: Gurfinkel, A., Ganesh,
    V. (eds.) Computer Aided Verification. Lecture Notes in Computer Science, vol.
    14682, pp. 3–18. Springer Nature Switzerland, Cham (2024). https://doi.org/
    10.1007/978-3-031-65630-9_1
 2. Bertolli, C., Betts, A., Mudalige, G., Giles, M., Kelly, P.: Design and Performance
    of the OP2 Library for Unstructured Mesh Applications. In: In Proceedings of the
    1st Workshop on Grids, Clouds and P2P Programming (CGWS). Lecture Notes
    in Computer Science, vol. 7155, pp. 191–200. Springer (2011). https://doi.org/
    10.1007/978-3-642-29737-3_22
 3. Bierhoff, K.: Automated program verification made SYMPLAR: Symbolic per-
    missions for lightweight automated reasoning. In: Proceedings of the 10th SIG-
    PLAN Symposium on New Ideas, New Paradigms, and Reflections on Program-
    ming and Software. pp. 19–32. ACM, Portland Oregon USA (Oct 2011). https:
    //doi.org/10.1145/2048237.2048242
 4. Blom, S., Huisman, M., Mihelčić, M.: Specification and verification of GPGPU
    programs. Science of Computer Programming 95, 376–388 (Dec 2014). https:
    //doi.org/10.1016/j.scico.2014.03.013
 5. Brookes, S.: A Semantics for Concurrent Separation Logic. In: Gardner, P.,
    Yoshida, N. (eds.) CONCUR 2004 - Concurrency Theory. pp. 16–34. Springer,
    Berlin, Heidelberg (2004). https://doi.org/10.1007/978-3-540-28644-8_2
 6. Charguéraud, A., Pottier, F.: Temporary Read-Only Permissions for Separation
    Logic. In: Yang, H. (ed.) Programming Languages and Systems, vol. 10201, pp.
    260–286. Springer Berlin Heidelberg, Berlin, Heidelberg (2017). https://doi.or
    g/10.1007/978-3-662-54434-1_10
 7. Detlefs, D., Nelson, G., Saxe, J.B.: Simplify: A theorem prover for program check-
    ing. Journal of the ACM 52(3), 365–473 (May 2005). https://doi.org/10.1145/
    1066100.1066102
 8. Eilers, M., Schwerhoff, M., Summers, A.J., Müller, P.: Fifteen Years of Viper. In:
    Computer Aided Verification (CAV) (2025)
 9. Grewe, D., Lokhmotov, A.: Automatically Generating and Tuning GPU Code for
    Sparse Matrix-Vector Multiplication from a High-Level Representation. In: Pro-
    ceedings of the 4th Workshop on General Purpose Processing on Graphics Process-
    ing Units (GPGPU). ACM (2011). https://doi.org/10.1145/1964179.1964196
10. Haack, C., Poll, E.: Type-Based Object Immutability with Flexible Initializa-
    tion. In: Drossopoulou, S. (ed.) ECOOP 2009 – Object-Oriented Programming,
    vol. 5653, pp. 520–545. Springer Berlin Heidelberg, Berlin, Heidelberg (2009).
    https://doi.org/10.1007/978-3-642-03013-0_24
11. Hillis, W.D., Steele, G.L.: Data parallel algorithms. Commun. ACM 29(12), 1170–
    1183 (Dec 1986). https://doi.org/10.1145/7902.7903
12. Le, Q., Ngiam, J., Coates, A., Lahiri, A., Prochnow, B., Ng, A.: On Optimization
    Methods for Deep Learning. In: Proceedings of the 28th International Conference
    on Machine Learning (ICML). pp. 265–272. Omnipress (2011)
13. Leino, K.R.M., Pit-Claudel, C.: Trigger selection strategies to stabilize program
    verifiers. In: Chaudhuri, S., Farzan, A. (eds.) Computer Aided Verification. pp.
    361–381. Springer International Publishing, Cham (2016)
14. Leino, K.R.M.: Dafny: An Automatic Program Verifier for Functional Correctness.
    In: Clarke, E.M., Voronkov, A. (eds.) Logic for Programming, Artificial Intelli-
20      L. B. van den Haak, A.J. Wijs and M. Huisman

    gence, and Reasoning, vol. 6355, pp. 348–370. Springer Berlin Heidelberg, Berlin,
    Heidelberg (2010). https://doi.org/10.1007/978-3-642-17511-4_20
15. Liu, X., Tan, S., Wang, H.: Parallel Statistical Analysis of Analog Circuits by
    GPU-Accelerated Graph-Based Approach. In: Proceedings of the 2012 Conference
    and Exhibition on Design, Automation & Test in Europe (DATE). pp. 852–857.
    IEEE Computer Society (2012). https://doi.org/10.1109/DATE.2012.6176615
16. de Moura, L., Ullrich, S.: The Lean 4 Theorem Prover and Programming Language.
    In: Platzer, A., Sutcliffe, G. (eds.) Automated Deduction – CADE 28. pp. 625–635.
    Springer International Publishing, Cham (2021). https://doi.org/10.1007/97
    8-3-030-79876-5_37
17. Müller, P., Schwerhoff, M., Summers, A.J.: Automatic Verification of Iterated Sep-
    arating Conjunctions Using Symbolic Execution. In: Chaudhuri, S., Farzan, A.
    (eds.) Computer Aided Verification, vol. 9779, pp. 405–425. Springer International
    Publishing, Cham (2016). https://doi.org/10.1007/978-3-319-41528-4_22
18. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A Verification Infrastructure
    for Permission-Based Reasoning. In: Jobstmann, B., Leino, K.R.M. (eds.) Verifi-
    cation, Model Checking, and Abstract Interpretation. pp. 41–62. Springer, Berlin,
    Heidelberg (2016). https://doi.org/10.1007/978-3-662-49122-5_2
19. Nugteren, C.: CLBlast: A Tuned OpenCL BLAS Library. In: Proceedings of the
    International Workshop on OpenCL. pp. 1–10. IWOCL ’18, Association for Com-
    puting Machinery, New York, NY, USA (May 2018). https://doi.org/10.1145/
    3204919.3204924
20. Ragan-Kelley, J., Adams, A., Sharlet, D., Barnes, C., Paris, S., Levoy, M., Ama-
    rasinghe, S., Durand, F.: Halide: Decoupling algorithms from schedules for high-
    performance image processing. Communications of the ACM 61(1), 106–115 (Dec
    2017). https://doi.org/10.1145/3150211
21. Schwerhoff, M.H.: Advancing Automated, Permission-Based Program Verification
    Using Symbolic Execution. Doctoral Thesis, ETH Zurich (2016). https://doi.or
    g/10.3929/ethz-a-010835519
22. van den Haak, L.B., Wijs, A.J., Huisman, M., van den Brand, M.G.J.: HaliVer:
    Deductive Verification and Scheduling Languages Join Forces. In: Finkbeiner, B.,
    Kovács, L. (eds.) Tools and Algorithms for the Construction and Analysis of Sys-
    tems. Lecture Notes in Computer Science, vol. 14572, pp. 71–89. Springer Nature
    Switzerland, Cham (2024). https://doi.org/10.1007/978-3-031-57256-2_4
23. van den Haak, L.B., Wijs, A.J., Huisman, M., van den Brand, M.G.J.: Verify-
    ing a Radio Telescope Pipeline Using HaliVer: Solving Nonlinear and Quantifier
    Challenges. In: Haxthausen, A.E., Serwe, W. (eds.) Formal Methods for Industrial
    Critical Systems. Lecture Notes in Computer Science, vol. 14952, pp. 152–169.
    Springer Nature Switzerland, Cham (2024). https://doi.org/10.1007/978-3-0
    31-68150-9_9
24. Wienke, S., Springer, P., Terboven, C., Mey, D.: OpenACC - First Experiences
    with Real-World Applications. In: Proceedings of the 18th European Conference
    on Parallel and Distributed Computing (EuroPar). Lecture Notes in Computer
    Science, vol. 7484, pp. 859–870. Springer (2012). https://doi.org/10.1007/97
    8-3-642-32820-6_85
25. Wijs, A., Bošnački, D.: Improving GPU Sparse Matrix-Vector Multiplication for
    Probabilistic Model Checking. In: Proceedings of the 19th International SPIN
    Workshop on Model Checking of Software (SPIN). Lecture Notes in Computer
    Science, vol. 7385, pp. 98–116. Springer (2012). https://doi.org/10.1007/978-3
    -642-31759-0_9
             Scalable Deductive Verification of Data-Level Parallel Programs        21

26. Wolf, F.A., Arquint, L., Clochard, M., Oortwijn, W., Pereira, J.C., Müller, P.: Go-
    bra: Modular Specification and Verification of Go Programs. In: Silva, A., Leino,
    K.R.M. (eds.) Computer Aided Verification, vol. 12759, pp. 367–379. Springer In-
    ternational Publishing, Cham (2021). https://doi.org/10.1007/978-3-030-816
    85-8_17
22     L. B. van den Haak, A.J. Wijs and M. Huisman

A    Lean proof of Theorem 1

The complete Lean proof can be found in the accompanying artefact: https://
github.com/cav2026-anonymous/Scalable-Deductive-Verification-of-D
ata-Level-Parallel-Programs/tree/main/LeanProof. We have implemented
f, f_inv (f −1 ), base, off, starting domain X and resulting domain Y to closely
match the definitions given in this section in the file Definitions.lean. The
properties 1, 2, and 3 are modelled in the definition Props. The property 4 is
added to the definition of X.
    One important difference from our Lean proof is that we index slightly dif-
ferently, since we modelled (x1 , . . . , xk ) ∈ Z as vector xs (Vector Int k) and
it was easier to model everything reversed. Thus, x1 corresponds to the last el-
ement of the vector xs.get (k-1) and xk corresponds to xs.get 0. This also
means that the definition of base i is reversed.
    Eventually, the results can be found in the file Results.lean. Theorem
  f_inv_on’ proves that f and f −1 are inverses on the sets X and Y . Whilst
f_bij_on’ proves that f is a bijection between X and Y .
    Lastly, the result is in theorem equiv_quantifier’, which proves Theorem 1.


B    Determining the constraint of Equation 4

For clarity, we repeat the constraint again.
                                                   i
                                                   X
        ∀i, 1 ≤ i < k ⇒ ∀(x1 , . . . , xk ) ∈ X,         |aj | · (xj − min j ) < |ai+1 |
                                                   j=1


    Determining whether this equation holds is generally difficult, since most
quantifiers will not include this equation specifically as part of their domain.
Especially if an ai is not a concrete number, these are nonlinear equations that
we cannot easily solve. Therefore, we looked for additional components of the
quantifier for which we could solve (part) of this equation more easily.
    Internally in VerCors, we check equation 4 by starting at the lowest i = 1
and iterating up to k. Suppose that you know that up to i − 1 we have proven
the equation and now we want to prove that it holds for i.
    We consider two cases in which we can prove this. In both cases xi should
have an upper bound max i , such that ni is defined and ni > 0. The first case
is that ni · ai = ai+1 holds, the second is that |ai | · ni ≤ |ai+1 | holds. In the
following lemma, we prove that this is correct.

Lemma 1. Suppose that for any integers i and k, 1 ≤ i < k, and all
(x1 , . . . , xk ) ∈ X it is proven that
                                          ′
                                        i
                                        X
                 ′            ′
               ∀i ∈ Z, 1 ≤ i < i ⇒            |aj | · (xj − min j ) < |ai′ +1 |            (5)
                                        j=1
             Scalable Deductive Verification of Data-Level Parallel Programs        23

holds, we have that ai ̸= 0, ni > 0, all ai have the same sign, and we have either
that ni · ai = ai+1 or that |ai | · ni ≤ |ai+1 | holds. Then
                               i
                               X
                                     |aj | · (xj − min j ) < |ai+1 |               (6)
                               j=1

is true.

Proof. Case i = 1 and ni · ai = ai+1 :
We have x1 < max 1 , which implies that x1 − min 1 < max 1 − min 1 = n1 , which
in turn implies |a1 | · (x1 − min 1 ) < n1 · |a1 | = |n1 · a1 |.
    We have a1 · n1 = a2 . Thus, we then have |a1 | · (x1 − min 1 ) < |a2 |, which was
what we wanted to prove for 6.
Case i > 1 and ni · ai = ai+1 :
That is, we want to prove the following.
                               i
                               X
                                     |aj | · (xj − min j ) < |ai+1 |
                               j=1

   We have that xi < max i , which implies xi −min i ≤ max i −min i −1 = ni −1,
which in turn implies |ai | · (xi − min i ) ≤ (ni − 1) · |ai | = |ni · ai | − |ai |.
   We have ai · ni = ai+1 . Thus, we then have

                            |ai | · (xi − min i ) ≤ |ai+1 | − |ai |                (7)

We rewrite the proof goal.
                         i−1
                         X
                               |aj | · (xj − min j )
                         j=1
                                                  i−1
                                                  X
                      =|ai | · (xi − min i ) +          |aj | · (xj − min j )
                                                  j=1




Using equations 7, and 5 by filling in i′ = i − 1, we get
                i−1
                X
                      |aj | · (xj − min j ) < |ai+1 | − |ai | + |ai | = |ai+1 |
                j=1

This is exactly equation 6 which was the proof goal.
Case i = 1 and |ai | · ni ≤ |ai+1 |:
We have x1 < max 1 , which implies that x1 − min 1 < max 1 − min 1 = n1 , which
in turn implies |a1 | · (x1 − min 1 ) < |a1 | · n1 .
    We have |a1 |·n1 ≤ |a2 |. Thus, we then have |a1 |·(x1 −min 1 ) < |a1 |·n1 ≤ |a2 |,
which was what we wanted to prove for 6.
24      L. B. van den Haak, A.J. Wijs and M. Huisman

Case i > 1 and |ai | · ni ≤ |ai+1 |:
We have that xi < max i , which implies xi − min i ≤ max i − min i − 1 = ni − 1,
which in turn implies |ai | · (xi − min i ) ≤ (ni − 1) · |ai | = |ni · ai | − |ai |.
   We have |ai | · ni ≤ |ai+1 |. Thus, we then have

                             |ai | · (xi − min i ) ≤ |ai+1 | − |ai |              (8)

We rewrite the proof goal.
                         i
                         X
                               |aj | · (xj − min j )
                         j=1
                                                 i−1
                                                 X
                      =|ai | · (xi − min i ) +         |aj | · (xj − min j )
                                                 j=1




Using equations 8, and 5 by filling in i′ = i − 1 we get
               i
               X
                      |aj | · (xj − min j ) < |ai+1 | − |ai | + |ai | = |ai+1 |
                j=1

This is exactly equation 6 which was the proof goal.
   Since either i = 1 or i > 1 holds and either |ai | · ni ≤ |ai+1 | or ni · ai = ai+1
holds, we covered all the cases and proved in all cases that equation 6 holds.

   Thus, with the above lemma, it means that for each i we can first check if ni ·
ai = ai+1 or |ai |·ni ≤ |ai+1 | holds to determine the constraint of equation 4. Then
only in the third fallback case do we ask our symbolic evaluator if equation 4
holds directly for a specific i.
