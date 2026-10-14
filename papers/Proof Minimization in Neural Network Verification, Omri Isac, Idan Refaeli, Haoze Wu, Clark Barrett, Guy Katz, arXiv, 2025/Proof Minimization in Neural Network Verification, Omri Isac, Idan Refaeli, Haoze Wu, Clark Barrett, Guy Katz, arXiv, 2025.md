                                                 Proof Minimization in Neural Network
                                                             Verification

                                                Omri Isac1 , Idan Refaeli1 , Haoze Wu2 , Clark Barrett3 , Guy Katz1
                                                             1
                                                                 The Hebrew University of Jerusalem, Israel
                                                                        2                                                ble          R
                                                                          Amherst College, USA




                                                                                                                   la




                                                                                                                                         eu
                                                                                                                  Avai




                                                                                                                                            sa
                                                                      3                                                  VMCAI’26




                                                                                                                                           b le
                                                                         Stanford University, USA                          Artifact
                                                                                                                          Evaluated
arXiv:2511.08198v1 [cs.LO] 11 Nov 2025




                                                                                                                         Fu
                                                                                                                              nctional



                                                Abstract. The widespread adoption of deep neural networks (DNNs)
                                                requires efficient techniques for verifying their safety. DNN verifiers are
                                                complex tools, which might contain bugs that could compromise their
                                                soundness and undermine the reliability of the verification process. This
                                                concern can be mitigated using proofs: artifacts that are checkable by an
                                                external and reliable proof checker, and which attest to the correctness
                                                of the verification process. However, such proofs tend to be extremely
                                                large, limiting their use in many scenarios. In this work, we address
                                                this problem by minimizing proofs of unsatisfiability produced by DNN
                                                verifiers. We present algorithms that remove facts which were learned
                                                during the verification process, but which are unnecessary for the proof
                                                itself. Conceptually, our method analyzes the dependencies among facts
                                                used to deduce UNSAT, and removes facts that did not contribute. We
                                                then further minimize the proof by eliminating remaining unnecessary
                                                dependencies, using two alternative procedures. We implemented our
                                                algorithms on top of a proof producing DNN verifier, and evaluated them
                                                across several benchmarks. Our results show that our best-performing
                                                algorithm reduces proof size by 37% − 82% and proof checking time by
                                                30% − 88%, while introducing a runtime overhead of 7% − 20% to the
                                                verification process itself.


                                         1    Introduction
                                         Deep neural networks (DNNs) have made great strides in recent years, becoming
                                         the state-of-the-art solution for a variety of tasks in medicine [55], autonomous
                                         driving [12], natural language processing [53], and many other domains. How-
                                         ever, DNNs lack structure that humans can readily interpret, rendering them
                                         opaque and potentially jeopardizing their trustworthiness [19]. One prominent
                                         example is the sensitivity of DNNs to small input perturbations, which can lead
                                         to significant and undesirable changes to the networks’ outputs. This sensitivity
                                         can be exploited maliciously [64], possibly leading to catastrophic results.
                                             The pervasiveness of DNNs, combined with their potential vulnerability, has
                                         made DNN verification a growing research field within the verification com-
                                         munity [2, 5, 6, 15, 16, 32, 34, 38, 52, 54, 58, 62, 66, 68, 72]. Modern DNN verifiers
                                         typically use techniques such as SMT solving [1, 9, 25, 45], abstract interpre-
                                         tation [32, 34, 52, 62, 69], LP solving [65], and combinations thereof. Many such
verifiers are available [15,16], and some tools have even been applied to industrial
case studies [4, 31, 49]. Given a DNN and a property over its input and outputs,
DNN verifiers will typically attempt to either find an input to the network that
violates the property or conclude that so such input exists.
    Despite this success, one significant issue that the DNN verification com-
munity faces is related to the reliability of verifiers. One concern is that even
state-of-the-art verifiers may contain implementation bugs. A second concern is
that verifiers typically use floating-point arithmetic, which is crucial for scala-
bility but could lead to rounding errors and numerical instability issues. These
issues might be exploited to compromise a verifier’s soundness [41, 74], thus un-
dermining user trust in these tools.
    Due to their complexity, verifying the correctness of DNN verifiers themselves
is typically infeasible. Instead, DNN verifiers can produce proofs for their verifi-
cation results, as is commonly done in SAT [37] and SMT [8]. These proofs, which
serve as witnesses of correctness of the verification result, constitute a mathe-
matical object and can be checked by an external, trusted proof checker [26, 27].
When a violation of the property is discovered, the returned counter-example
may serve as a proof of correctness. However, proving the absence of a violation
is less straightforward, due to the NP-hardness of the problem [40, 45, 57].
    So far, only a handful of attempts have been made to enable DNN verifiers
to produce proofs [39]. These approaches typically include eager bookkeeping of
many intermediate lemmas deduced during verification [39]. Therefore, the re-
sulting proofs tend to be extremely large, increasing the memory consumption of
the verifier and harming the performance of proof checkers [26]. These problems
limit the applicability of proof-producing verifiers, and call for further analysis
to minimize proof sizes.
    In this work, we address this problem by minimizing the proof objects con-
structed using the framework of Isac et al. [39]. Our proof reduction method
involves two main steps. First, we apply a dependency analysis procedure that
recursively examines the dependencies of each lemma on previously learned lem-
mas. This helps to identify and remove lemmas that were eagerly learned and
stored during the verification process, but are not actually required in the final
proof. Second, we apply two alternatives for dependency minimization proce-
dures, which further refine the proof by removing unnecessary lemma dependen-
cies, keeping only a minimal subset of dependencies for each lemma. This results
in additional lemmas being classified as unused, leading to a smaller proof.
    After the termination of the dependency analysis and minimization, the
unused lemmas can be safely removed from the proof, without needing to be
checked. Furthermore, our method allows lemma deletion on-the-fly, thus avoid-
ing accumulation of unused lemmas and minimizing the memory consumption
during the verification process. This, in turn, increases the scalability of proof
producing DNN verifiers.
    We evaluated our method across multiple benchmarks, using [39] as a base-
line. We measured the effectiveness of our algorithms along two axes: the size of
the resulting proof, and the time overhead for applying our algorithms. The re-
sults for our best-performing algorithm indicate reduction of proof size of 37%–
82% on average and of proof checking time by 30%–88% on average. The re-
duction incurs a overhead of 7%–20% to the verifier’s runtime, where for some
benchmarks the average verification time was slightly improved, possibly due to
the use of more efficient data structures.
    Our contributions are summarized as follows: (i) an algorithm for analyzing
the dependencies of each lemma learned within proof objects, removing unused
lemmas; (ii) two algorithms for further detecting a minimal subset of dependen-
cies; and (iii) a demonstration of a substantial reduction of the proof size over
several benchmarks, while adding a reasonable overhead in performance speed.
    The rest of this paper is organized as follows: In Section 2 we provide the
necessary background on DNNs and their verification, and on proof production.
In Section 3 we explain our method to reduce the proof size. Section 4 is dedicated
to evaluation of our method over several benchmarks, with respect to both proof
size and verification speed. In Section 5 we discuss related work, and lastly, we
conclude and outline ideas for future research in Section 6.


2     Background
2.1   Deep Neural Networks and their Verification

Deep Neural Networks (DNNs) [33]. Formally, a DNN N : Rn → Rm is
a sequence of k layers L0 , ..., Lk−1 where each layer Li consists of si ∈ N nodes
vi1 , ..., visi and si biases bji ∈ Q. Each directed edge in the DNN is of the form
   l
(vi−1    , vij ) and is labeled with a weight wi,j,l ∈ Q. The assignment to the nodes
in the input layer is defined by v0j = xj , where x ∈ Rn is the input vector.
The assignment
             si−1      for the j th node in the 1 ≤ i < k − 1 layer is computed as
vij = fi                     l
                                 + bji for some activation function fi : R → R. Neurons
                 P
                   wi,j,l · vi−1
          l=1
in the output layer are computed similarly, where fk−1 is the identity function.
    One of the most common activation functions is the rectified linear unit
(ReLU), defined as ReLU(x) := max(x, 0). The function has two linear phases:
if the input is non-negative, the functions is active; otherwise, the function is
inactive. For simplicity, we focus on DNNs with ReLU activations, though our
work can be extended to support any piecewise-linear activation (e.g., maxpool ).

Example 1 A simple DNN with four layers appears in Figure 1. For simplicity,
all biases are set to 0 and are omitted. For input ⟨2, 1⟩, the node in the second
layer evaluates to ReLU(2 · 1 + 1 · (−1)) = ReLU(1) = 1; the nodes in the third
layer evaluate to ReLU(1 · (−2)) = 0 and ReLU(1 · 1) = 1; and the node in the
output layer evaluates to 0 + 1 · 2 = 2.

The DNN Verification Problem. Consider a DNN N : Rn → Rm where
x ∈ Rn , y ∈ Rm denote the network’s inputs and outputs. The DNN verification
problem is the problem of deciding whether there exist (x, y) ∈ Rn+m such that
                                                        ReLU
                        x1                                  v2
                              1                    −2            1
                                    ReLU
                                        v1                           y
                                                        ReLU
                             −1                    1             2
                        x2                                  v3


                   Fig. 1: A toy DNN with ReLU activations.
(N (x) = y) ∧ φI (x) ∧ φO (y) for some property φI ∧ φO . If such x, y exist, we say
the problem is satisfiable, denoted SAT. Otherwise, we say that it is unsatisfiable,
denoted UNSAT. In this work, we consider quantifier-free linear properties, i.e.,
formulas without quantifiers whose atoms are linear equations and inequalities.
Example 2 Consider the DNN from Figure 1, the input property

               φI (x) := (1 ≤ x1 ) ∧ (1 ≤ x2 ) ∧ (x1 ≤ 2) ∧ (x2 ≤ 2)
and the output property
                                  φO (y) := (y ≤ −1).
This instance is UNSAT, as the output is a sum of two non-negative components
with positive weights.
Linear Programming (LP) [24] and DNN Verification. In LP we seek
an assignment to a set of variables that satisfies a set of linear constraints,
while maximizing a given objective function. As is common in the context of
DNN verification, we assume here that the objective function is constant and
                                               ⊺
ignore it. Formally, let V = [x1 , . . . , xn ] ∈ Rn denote variables, A ∈ Mm×n (R)
denote a constraint matrix and l, u ∈ (R ∪ {±∞})n denote vectors of bounds.
The LP problem is to decide the satisfiability of (A · V = 0) ∧ (l ≤ V ≤ u).
Throughout the paper, we use l(xi ) and u(xi ), to refer to the lower and upper
bounds (respectively) of xi ∈ V , and denote l ≤ u to indicate that for each
element i, l(xi ) ≤ u(xi ).
    A DNN verification query can be encoded as a tuple Q = ⟨V, A, l, u, R⟩, where
⟨V, A, l, u⟩ constitutes a linear program [24, 45] that represents the property and
the affine transformations within N , and where R is the set of ReLU activation
constraints of the form fi = ReLU(bi ), for variables bi , fi ∈ V . In addition, a
fresh auxiliary variable ai is added for each ReLU constraint, representing the
non-negative difference of its output and input. The variable is added to V , with
an equation ai = fi −bi added to A, and the bounds l(ai ) = 0, u(ai ) = u(fi )−l(bi )
added to l, u respectively.
Example 3 We demonstrate this encoding with the example presented in Fig-
ure 1 and the property from Example 2. Let x1 , x2 denote the network’s inputs
and y denote its output, and let bi , fi ( i ∈ {1, 2, 3}) denote the input and output
of neuron vi , respectively. The affine transformations of the network are reduced
to the equations:                 x −x −b =0
                                    1          2        1
                                             2f1 + b2 = 0
                                              f1 − b3 = 0
                                   f2 + 2f3 − y = 0
accompanied by fi − bi − ai = 0 for i ∈ {1, 2, 3}. The property is encoded using
the inequalities: (1 ≤ x1 ), (1 ≤ x2 ), (x1 ≤ 2), (x2 ≤ 2), (y ≤ −1). We also
add the inequalities (0 ≤ fi ) (for i ∈ {1, 2, 3}) to express the non-negativity of
ReLUs, and (0 ≤ ai ) as described. The aforementioned constraints form the LP
part of the query; and its piecewise-linear portion is comprised of the constraints
fi = ReLU(bi ) for i ∈ {1, 2, 3}.

     Using this encoding, the verification query can be dispatched through a se-
ries of invocations of an LP solver, combined with case splitting to handle the
piecewise-linear constraints [45]. Schematically, the DNN verifier begins by in-
voking the LP solver over the linear part of the query. An UNSAT result of the
LP solver implies the overall query is UNSAT. Otherwise, the LP solver finds an
assignment that satisfies the linear part of the query. If this assignment satisfies
the piecewise-linear part of the query, the DNN verifier may conclude SAT. If
neither case applies, the DNN verifier splits the query into two subqueries, by
deciding the phase of a single ReLU constraint fi = ReLU(bi ). One subquery is
augmented with the bounds bi ≥ 0 and ai ≤ 0 corresponding to the active phase;
the other is augmented with bi ≤ 0 and fi ≤ 0, corresponding to the inactive
phase. Then, the LP solver is invoked again over each subquery, and the pro-
cess is repeated. Note that the introduction of auxiliary variables is intended to
reduce case splitting to bound updates, without needing to add new equations;
empirically, this is known to improve performance [70].
     This splitting approach creates an abstract tree structure, where each node
represents a case split. If the LP solver deduces UNSAT for each leaf of the tree,
then the original query is UNSAT as well. If not, then due to the completeness of
LP solvers, it finds a satisfying assignment for one of the subqueries.
     The search tree may be exponentially large in the number of piecewise linear
constraints (i.e., the number of neurons). Therefore, it is common to use case
splitting rarely, and apply algorithms to deduce tighter bounds of variables.
These algorithms may conclude in advance that some neurons’ phases are fixed,
i.e., they are always active or inactive, avoiding the need to split on them [45].


2.2   Proof Production for DNN Verification

When DNN verification is regarded as a satisfiability problem, a satisfying as-
signment is an efficient proof of SAT: one can simply run it through the network
and observe that it satisfies the given property. The UNSAT case is more complex,
and requires producing a proof certificate. The first method for proof production
in DNN verification performed via LP solving and case splitting was introduced
in [39]. These proof certificates consist of a proof tree that replicates the search
tree created by the verifier, and is constructed during the verification process.
Recall that for an UNSAT query, all leaves of the search tree represent UNSAT
subqueries. Thus, each internal node of the proof tree represents a case split
performed by the verifier, and each leaf corresponds to a subquery for which the
verifier has deduced UNSAT. Therefore a proof checker for these proofs is required
to traverse the tree, check its structural correctness (i.e., all splits are correct),
and certify the unsatisfiability of each leaf.
    In each leaf of the search tree, the verifier was able to conclude UNSAT using
solely the available linear constraints. Thus, a proof for the leaf’s unsatisfiability
can be described as a vector, according to the Farkas lemma [21], which combines
the linear constraints to derive an evident, easily-checkable, contradiction [39].
More formally:

Theorem 1 (Farkas Lemma Variant (From [39])). Observe the constraints
A · V = 0̄ and l ≤ V ≤ u, where A ∈ Mm×n (R) and l, V, u ∈ Rn . The constraints
                                                                  n
are UNSAT if and only if ∃w ∈ Rm such that for w⊺ · A · V :=
                                                                 P
                                                                    ci · xi , we have
                                                                 i=1
                         ci · l(xi ) < 0 whereas w⊺ · 0̄ = 0. Thus, w is a proof of
      P                P
that     ci · u(xi ) +
     ci >0           ci <0
the constraints’ unsatisfiability, and can be constructed during LP solving.

Example 4 We demonstrate this theorem with our example. Consider the query
based on the DNN in Figure 1 and the property in Example 2. Assume, for
simplicity, that all lower and upper bounds not explicitly stated are −1 or 1,
respectively. Further assume that both v2 , v3 are inactive (i.e. f2 = f3 = 0 and
b2 , b3 ≤ 0). The linear part of the query yields the LP instance:
                            
   1 −1 −1 0 0 0 0 0 0 0 0 0
  0 0 0 1 0 2 0 0 0 0 0 0                                                        ⊺
  
  0 0 0 0 −1 1 0 0 0 0 0 0 
                                            u = 2 2 1 0 0 1 0 0 2 1 1 −1
                                                                                 ⊺
  0 0 0 0 0 0 1 2 0 0 0 −1
A=                                          V = x1 x2 b1 b2 b3 f1 f2 f3 a1 a2 a3 y
                             
  0 0 −1 0 0 1 0 0 −1 0 0 0                                                      ⊺
                                            l = 1 1 −1 −1 −1 0 0 0 0 0 0 −1
  0 0 0 −1 0 0 1 0 0 −1 0 0 
   0 0 0 0 −1 0 0 1 0 0 −1 0

Note that in A the first four rows corresponds to the affine transformations of
the DNN, and the latter three rows are introduced with the auxiliary variables.
Consider the vector                            ⊺
                            w = 0 0 −1 −2 0 0 0 .
The product w⊺ · A · V yields the equation −f1 + b3 − 2f2 − 4f3 + 2y = 0. The left
hand side of the equation is at most: −l(f1 )+u(b3 )−2·l(f2 )−4·l(f3 )+2·u(y) =
−2 < 0. Therefore, according to Theorem 1, w is a proof of UNSAT. Note that
there may be multiple proofs of this result. An overall proof of UNSAT for the
query consists of a proof tree, where each leaf has a proof vector proving UNSAT
for the corresponding subquery.

Bound Tightening Lemmas. DNN verifiers often employ bound tightening
procedures that deduce bounds using the non-linear activations, called bound
tightening lemmas. Each bound tightening lemma consists of a ground bound
and a learned bound, which replaces a bound currently in l or u. As opposed
to deduction of bounds using linear equations, proving such lemmas generally
cannot be captured by the Farkas vector described above, and require separate
proofs [39]. For example, given f = ReLU(b) and present bounds f ≤ 5 and
b ≤ 7, it is possible to deduce that b ≤ 5. The lemma can be proven using a
Farkas vector that proves f ≤ 5, and another proof rule that captures this form
of bound derivation.

Example 5 Consider the query Q in Example 4. We can use the equation b2 =
−2f1 , which is equivalent to 2f1 + b2 = 0, to deduce that u(b2 ) = −2 · l(f1 ) = 0.
Then, based on the ReLU constraint, we deduce that the neuron v2 is inac-
tive, i.e., that u(f2 ) = 0. A lemma with a ground bound u(b2 ) = 0, learned
bound   u(f2 ) = 0 and a proof vector for generating b2 = −2f1 (the vector
                ⊺
 0 −1 0 0 0 0 0 ) is learned at the root of the proof tree, without any case splits.
Similarly, we can deduce that v3 is inactive. Observe that f3 = 21 y − 12 f2 , and
thus u(f3 ) = 21 u(y) − 12 l(f2 ) = −0.5. Then a lemma with a ground bound
                                                                                 ⊺
u(f3 ) = −0.5, learned bound u(b3 ) = 0 and a proof vector 0 0 0 −0.5 0 0 0
is learned. Combined with Example 4, we get a proof of UNSAT for Q that con-
sists of a single node with two lemmas, as illustrated in Figure 2.

                                                      Q

               u(b2 ) = 0 → u(f2 ) = 0                         u(f3) = −0.5 → u(b3) = 0
                                    ⊺                                                  ⊺
                   0 −1 0 0 0 0 0                                     0 0 0 −0.5 0 0 0
                                                                ⊺
                                               0 0 −1 −2 0 0 0


Fig. 2: A proof tree example with a single node (orange). Given the query Q,
two lemmas (blue) are learned before deriving UNSAT (red).

   To avoid ambiguity in the definition of the bound vectors l, u, unless stated
otherwise, l, u denote the tightmost bound vectors, while linput , uinput denote
the original bound vectors, given as inputs.


3   Proof Dependency Analysis and Minimization

In this section, we elaborate on our algorithms for proof minimization. Recall
that each lemma and each leaf within the proof includes a proof vector; and
that all these vectors have the same dimension, since the number of rows in
A is constant. As proving UNSAT of all leaves in the proof tree is necessary for
proving UNSAT for the whole query, proof minimization is achieved by reducing
the number of lemmas used within the proof. The minimization algorithms are
applied upon deducing UNSAT on each proof tree leaf, thus enabling on-the-fly
minimization and preventing the accumulation of unnecessary lemmas. We begin
by describing our algorithm for dependency analysis in Section 3.1 and two algo-
rithms for dependency minimization in Section 3.2. We conclude in Section 3.3,
by introducing an additional minimization technique, which can be used in both
algorithms, by explaining the procedure for removing the unused lemmas and
by introducing engineering optimizations to improve performance speed.
Algorithm 1 proofDeps(): Construct the dependency list of a proof vector
Input: A DNN verification subquery Q = ⟨V, A, l, u, R⟩, a list of learned lemmas Lem,
and a proof of UNSAT w
Output: A list of lemmas sufficient to deduce UNSAT
           n
              ci · xi denote the linear combination w⊺ · A · V
           P
   // Let
           i=1
 1: Deps ← ∅                                                 ▷ An empty list of lemmas
 2: for i ∈ [n] do
 3:    if ci > 0 and u(xi ) is learned by ℓui ∈ Lem then
 4:           Deps ← Deps ∪ ℓui
 5:    else if ci < 0 and l(xi ) is learned by ℓli ∈ Lem then
 6:           Deps ← Deps ∪ ℓli
 7:    end if
 8: end for
 9: for lem ∈ Deps do                                              ▷ Repeat recursively
10:     lem.includeInP roof ← true
11:     l′ , u′ ← bounds with ID at most lem.getID()
12:     w′ ← lem.getP roof ()
13:     Deps′ ← proof Deps(⟨V, A′ , l′ , u′ , R⟩, Lem, w′ )
14:     Deps ← Deps ∪ Deps′
15: end for
16: return Deps



3.1   Analyzing Proof Dependencies

We now describe our algorithm for minimizing proof-trees by dependency analy-
sis. Given a proof vector — either a proof of unsatisfiability for a search-tree leaf,
or a proof for a bound tightening lemma — our analysis identifies which bound
tightening lemmas are involved in its proof checking process. Our approach for
analyzing the dependencies of a given proof vector w appears as Algorithm 1.
     Conceptually, Algorithm 1 reconstructs the linear combination w⊺ · A · V ,
             n
             P
denoted as     ci · xi . Then, as the proof only uses the bounds l(xi ) for variables
            i=1
with a negative coefficients, and u(xi ) for variables with a positive coefficient,
their corresponding lemmas form the dependency list for w. The dependency list
provides a sufficient set of lemmas for proving the unsatisfiability of w — and
this set can potentially be minimized. Then, the algorithm further analyses the
dependencies of the discovered lemmas, only after we know they are used in the
proof. Recall that each lemma has its own proof vector, and thus this analysis
is carried out through a recursive call on each lemma’s proof.
    To expedite the algorithm, we store for every bound l(xi ), u(xi ), the lemma
or split that was used to deduce it. In addition, to avoid cycles and ensure the
completeness of our algorithms, each lemma is given a unique, chronological
ID. Whenever a lemma with ID k is analyzed, only lemmas with ID l < k are
considered in the analysis.
Example 6 Recall that in Example 4 and Example 5, after       learning two  ⊺lemmas
we are able to derive UNSAT from a proof vector w = 0 0 −1 −2 0 0 . Using
this vector generates the equation −f1 + b3 − 2f2 − 4f3 + 2y = 0, which uses the
bounds l(f1 ), u(b3 ), l(f2 ), l(f3 ), u(y) to prove UNSAT. As u(b3 ) is deduced using
one of the lemmas in Example 5, this lemma forms the dependency list of w.
Then, the algorithm recursively generates the dependency list of the proof vector
of the lemma in a similar manner. As shown in Example 5, that lemma is not
dependent on u(f2 ). Thus, the lemma for deducing u(f2 ) is not actually used in
the proof of UNSAT, and can then be removed from the proof tree. An illustration
of this example appears in Figure 3.
                                                       Q

                u(b2 ) = 0 → u(f2 ) = 0                         u(f3) = −0.5 → u(b3) = 0
                                     ⊺                                                  ⊺
                    0 −1 0 0 0 0 0                                     0 0 0 −0.5 0 0 0
                                                                 ⊺
                                                0 0 −1 −2 0 0 0


Fig. 3: Using Algorithm 1 over the proof vector used to derive UNSAT (red) shows
that a single lemma (blue) is used during the proof process, and the other (gray)
is not. All proof vectors use information in the root query Q (orange)


3.2   Minimizing the Number of Proof Dependencies
We now elaborate on our two alternatives of algorithms for minimizing the de-
pendency list of a proof vector. By doing so, we aim to increase the number of
lemmas that do not appear in any dependency list, i.e., are unused. Such lemmas
can then be omitted from the proof, further reducing its overall size.
   Let w be a proof vector proving the unsatisfiability of a search-tree leaf. Our
algorithm focuses on minimizing the number of bound tightening lemmas that
participate in the refutation. Recall that a refutation is checked by computing
                                  n
the upper bound of w⊺ · A · V =
                                  P
                                     ci · xi , i.e.,
                                            i=1
                                    X                         X
                            ∆ :=            ci · u(xi ) +              ci · l(xi )
                                    ci >0                    ci <0

and ensuring it is negative. The idea of our algorithm lies in the fact that ∆
can be very far from zero. In this case, we can relax some of the bounds derived
from the participating bound lemmas, without altering the sign of ∆, and thus
maintain the proof’s correctness. Analyzing the dependencies of a proof vector
ŵ, used to prove a bound tightening lemmas, is performed similarly. In this case,
∆ represents the difference between the bound it is used to prove and the actual
bound achieved with ŵ⊺ · A · V .

Proof Minimization. The first algorithm for proof minimization is greedy,
and removes the maximal number of unnecessary dependencies for each proof
vector separately. To do so, we first define for each lemma its contribution to
w, which can be seen as its effect on ∆. More formally, given the input bound
vectors linput , uinput , and the bound vectors l, u with bounds derived by a set
of bound lemmas and case splits. For each cj > 0, the contribution of u(xj ) to
w⊺ · A · V is defined as:

                      cont(uj , w) := cj · (u(xj ) − uinput (xj ))

For each cj < 0, the contribution of l(xj ) to w⊺ · A · V is:

                       cont(lj , w) := cj · (linput (xj ) − l(xj ))

Note that in all cases the contribution is non-positive, as linput ≤ l ≤ u ≤ uinput .
     These definitions naturally give rise to Algorithm 2, which sorts the various
lemmas according to their contributions to the proof, from small to large. Those
lemmas with only a small contribution could potentially be omitted from the
proof, without altering the sign of ∆. Attempting to remove lemmas in this order
ensures the removal of the maximum number of lemmas from the dependency
list, and consequently the minimality of the output, as we prove in Theorem 2.
Algorithm 2 can be used within Algorithm 1, before any recursive application of
the algorithm. By that, Algorithm 2 reduces the time overhead of Algorithm 1,
by reducing the number of the latter’s recursive calls.
Theorem 2. Given ⟨V, A, l, u, R⟩, a proof vector w, a list of its lemma depen-
dencies D, and the input bound vectors linput , uinput , Algorithm 2 returns a
dependency subset of Deps that is minimal in size.
Proof. Assume towards contradiction that there exists D′ , which constitutes a
dependency list of w, with |D′ | < |D|. First, observe that if D′ ⊊ D, then there
is some lemma ℓ ∈ D \ D′ that can be removed from D when considered in line
6, this contradicts the definition of the algorithm.
    Therefore, D \ D′ and D′ \ D are not empty. Let ℓ ∈ D \ D′ , with the
minimal contribution δ, and let ℓ′ ∈ D′ \ D with the minimal contribution δ ′ .
Since Algorithm 2 is greedy, we must have that δ ′ ≤ δ, as otherwise the algorithm
would have removed ℓ from D before removing ℓ′ . This means that we can replace
ℓ′ with ℓ in D′ without increasing the overall contribution removed from Deps.
We can repeat the process until saturation, i.e., when D′ ⊊ D, which leads to a
contradiction. □
                                                                          ⊺
Example 7 In Example 6 we saw that the proof vector w = 0 0 −1 −2 0 0 ,
presented in Example 4, is dependent on only one of the two lemmas learned as
in Example 5. In addition, the analysis in Example 4 shows that ∆ = −2, and
that the proof vector w is dependent on the lemma used to deduce u(b3 ) = 0,
whose input bound is u(b3 ) = 1. Therefore, the contribution of the lemma is
1 · (0 − 1) = −1, indicating this lemma can be removed from the dependency list
as well. Observe that indeed, given the input bounds, we have:

          −l(f1 ) + uinput (b3 ) − 2 · l(f2 ) − 4 · l(f3 ) + 2 · u(y) = −1 < 0
Algorithm 2 proofMin(): Minimize the dependency list of a proof vector
Input: A DNN verification subquery Q = ⟨V, A, l, u, R⟩, a proof vector w, a list of its
lemma dependencies Deps, and the input bound vectors linput , uinput
Output: A minimial dependency list of w
            n
               ci · xi denote the linear combination w⊺ · A · V
           P
    // Let
          Pi=1              P
 1: ∆ ←       ci · u(xi ) +    ci · l(xi )
         ci >0              ci <0
 2: Deps ← Deps.sortByContribution()
 3: δ ← 0
 4: for dep ∈ Deps do
 5:    δ+ = |cont(dep.getBoundT ype(), w)|                                   ▷ Use A, V, l, u, linput , uinput
 6:    if δ ≤ |∆| then
 7:        Deps.remove(dep)
 8:    else return Deps
 9:    end if
10: end for
11: return ∅



Together with Example 6, we conclude that both lemmas from Example 5 can be
removed from the proof tree. An illustration for this example appears in Figure 4.



                                                        Q

                 u(b2 ) = 0 → u(f2 ) = 0                         u(f3) = −0.5 → u(b3) = 0
                                      ⊺                                                  ⊺
                     0 −1 0 0 0 0 0                                     0 0 0 −0.5 0 0 0
                                                                  ⊺
                                                 0 0 −1 −2 0 0 0


Fig. 4: Using Algorithm 2 over the proof vector used to derive UNSAT (red) shows
that both lemmas (gray) are unnecessary for proving UNSAT.


Global Heuristic for Proof Minimization. Although Algorithm 2 guaran-
tees achieving the minimum number of dependencies for each proof vector, this
does not necessarily ensure achieving the global minimum across the entire proof
tree. To incorporate global considerations, we adjust the order in which lemmas
are considered for removal, prioritizing those with more dependencies and whose
elimination is likely to trigger the removal of additional downstream lemmas.
    Specifically, before applying the minimization algorithm, we recursively ap-
ply the dependency analysis procedure to each lemma and compute its total
number of dependencies, including those discovered through the recursive appli-
cations of the minimization procedure. The lemmas are then sorted in decreasing
order by their overall dependency count (i.e., lemmas with more dependencies
are considered for removal first). In case of ties, we fall back on the previous
contribution score. We apply the analysis until saturation, meaning no further
reduction of dependencies is possible. This ensures minimality of the subset of
dependencies, though it does not guarantee the resulting subset is smallest. This
can occur if Algorithm 3 diverges significantly from Algorithm 2, for example,
when lemmas with high dependency counts contribute heavily. In such cases, the
former algorithm may remove these lemmas first, while the latter will instead
remove many more lemmas with a lower dependency count. To maintain the
applicability of the algorithm during proof generation, we apply it each time an
UNSAT leaf is detected, considering all lemmas learned globally up to that point.
    This intuition is formalized in Algorithm 3, and it opens up possibility to
explore additional heuristics for prioritizing lemmas for removal, e.g., by con-
sidering different combinations of each lemma’s number of dependencies and its
contribution.
    Note that introducing global considerations for proof minimization involves
dependency analysis for many lemmas, and thus might incur a relatively large
time overhead.


3.3   Additional Improvements and Lemma Deletion


Further Reduction of Proof Size. Both minimization algorithms presented
above consider the dependencies for each proof vector separately. However, it
is possible that minimizing dependencies at the proof-vector level leads to re-
dundant dependencies at the proof-tree level. Consider the case where two proof
vectors w1 , w2 depend on a lemma ℓ, and that the dependencies of w1 are mini-
mized before those of w2 . If the dependency minimization of w1 indicates that ℓ
is retained in the proof, then removing it from the dependencies of w2 will not
lead to the removal of ℓ from the overall proof, and will unnecessarily increase
the contributions counter δ Algorithm 2 (line 5). Therefore, a straightforward
improvement to both minimization algorithms is to consider removing depen-
dencies only from lemmas that are not currently used in the proof. This approach
allows us to skip lemmas that are already essential and would be retained re-
gardless.

Example 8 Consider a lemma ℓ1 with ∆1 = −1. Suppose that proof analysis
of Algorithm 1 determines that ℓ1 is dependent on ℓ2 , ℓ3 with respective contri-
butions of −0.5 and −0.6. Suppose also that other lemmas depend on ℓ2 , so it is
retained in the proof, but none depend on l3 yet. In this case, Algorithm 2 would
first remove the dependency of ℓ1 in ℓ2 and then stop as | − 0.5| + | − 0.6| > | − 1|.
Therefore, this application of Algorithm 2 will keep both ℓ2 and ℓ3 in the proof.
Alternatively, by ignoring ℓ2 as it is already used in the proof, and removing the
dependency on ℓ3 instead, we may reduce the overall number of lemmas required
for the proof.

Avoiding Duplicate Computations. Recall that Algorithm 1 recursively it-
erates through lemmas and analyzes their dependencies. Since multiple lemmas
Algorithm 3 globProofMin(): Minimize the dependency list of a proof vector
Input: A DNN verification subquery Q = ⟨V, A, l, u, R⟩, a proof vector w, a list of its
lemma dependencies Deps, the input bound vectors linput , uinput , and the overall list
of learned lemmas Lem
Output: A minimial dependency list of w
             n
                ci · xi denote the linear combination w⊺ · A · V
            P
     // Let
           Pi=1              P
 1: ∆ ←        ci · u(xi ) +    ci · l(xi )
         ci >0           ci <0
 2: Deps ← Deps.sortByDepsLength(Q, Deps, Lem)
 3: δ ← 0
 4: saturation ← f alse
 5: while !saturation do
 6:    saturation ← true
 7:    for dep ∈ Deps do
 8:       δ+ = |cont(dep.getBoundT ype(), w)|             ▷ Use A, V, l, u, linput , uinput
 9:       if δ ≤ |∆| then
10:           Deps.remove(dep)
11:           saturation ← f alse
12:        else
13:           δ− = |cont(dep.getBoundT ype(), w)|                                ▷ Revert
14:        end if
15:    end for
16: end while
17: return Deps

   sortByDepsLength(Q, Deps, Lem):
1: for ℓ ∈ Deps do
2:     if !ℓ.wasAnalyzed then
3:         ℓ.score ← proof Deps(Q, Lem, ℓ.getP roof ()).size()
4:         ℓ.tieBreaker ← ℓ.getContribution()
5:         ℓ.wasAnalyzed ← true
6:     end if
7: end for
8: return Deps.sortByScore()



can depend on the same lemma, it is useful to avoid redundant or repeated anal-
ysis. To address this, we add a flag to each lemma indicating whether it has
already been analyzed. This ensures that each lemma is analyzed at most once.
Unused Lemma Deletion. To reduce the memory consumption of the DNN
verifier during the verification process, we propose to remove unused lemmas as
early as possible. Since each lemma is applicable only in the search state S where
it was deduced and in all descendant states of S, it becomes irrelevant once the
sub-tree rooted at S has been fully explored. At that point, any lemma in S that
was not involved in any dependency analysis can be safely deleted.
Supporting Additional Constraints. Although so far we focused on DNNs
with ReLU constraints, our minimization algorithms can be applied to additional
kinds of constraints in a straightforward manner. Therefore, assuming the under-
lying verifier supports proof production for additional kinds of piecewise-linear
constraints, the minimization algorithms are readily applicable.


4     Implementation and Evaluation
To assess the effectiveness of our proposed proof minimization techniques, we
conducted an empirical evaluation across six benchmark suites in neural net-
work verification (ordered alphabetically): (i) the Acas-Xu drone collision avoid-
ance networks [42]; (ii) the cersyve benchmark [71] for verification of neural
safety certificate in control systems; (iii) a subset of the Cora benchmark [15,
48], where disjuncts from the original queries where separated into different
queries; (iv) MaxLeaky, a fresh benchmark that includes simple queries over
a newly-trained DNN employing Maxpool and LeakyRelu [28] activation func-
tions; (v) a robotic navigation system benchmark [3]; and, (vi) the SafeNLP
benchmark [17, 18]. These benchmarks were selected due to their relevance to
safety-critical applications their diversity in size and activation functions, and
their established use in previous work or at the DNN verification competition
(VNNCOMP) [15, 16]. Notably, we included all VNNCOMP benchmarks for
which the proof-producing version of Marabou reasonably scales.

4.1   Experimental Setup and Implementation
Experiments were conducted on machines running Debian 12 Linux, each on
a single CPU. We divided the benchmarks into two sets according to network
sizes, with Acas-Xu and Cora consisting of larger DNNs, and the remaining
benchmarks consisting of smaller DNNs. Memory and time configurations de-
pended on category: for the larger benchamrks we used 16GB RAM and a 5-hour
Timeout, and for the smaller ones — 2GB RAM and a 2.5-hour Timeout.
     Our implementation is based on the proof-producing version of the Marabou
DNN verifier [39, 47, 70], into which we integrated our proof minimization al-
gorithms and which we used as a baseline. The key metrics evaluated include
(i) Proof size: the number of proof vectors (for both lemmas and leaves) in the
produced proofs of UNSAT queries; (ii) Total Runtime: the total runtime of the
verification process, for all queries; and (iii) Total Proof-Checking time: the to-
tal proof-checking time for the UNSAT queries, using the native Marabou proof
checker. Note that a partial proof object is constructed during verification in sat-
isfiable queries as well (before concluding SAT); and thus, measuring verification
time for all queries offers a more comprehensive comparison.

4.2   Evaluation
We begin by presenting a summary of the experimental results in Table 1,
which reports the average proof size generated during proof production, the
average total verification time, and the average total proof-checking time, for
each benchmark and proof minimization technique. In this table, averaging was
conducted with respect to queries solved by all methods. Furthermore, we pro-
vide a visual summary in Figure 5, which compares the proof sizes of all UNSAT
queries, and overall runtime across all queries. We evaluated three variants of our
method: (i) Dependency Analysis (Dep. Analysis), as described in Algorithm 1;
(ii) Dependency Minimization (Dep. Min.), which includes the implementation
of Algorithm 2 on top of Algorithm 1; and (iii) Global Dependency Minimiza-
tion (Dep. Min. Glob.), which replaces Algorithm 2 with Algorithm 3. For a
deeper study of the effect on the total runtime, we consider an additional run-
ning configuration, Min. Baseline, which includes all data structures used for
implementing our algorithms as exemplified in Section 3.1, but without actually
executing Algorithm 1. By running this version, we are able to separate the run-
ning time effect of the changes in data structures, from the effect of the analysis
and minimization algorithms themselves. All methods were implemented with
the optimizations detailed in Section 3.3.
     The results demonstrate a clear reduction in average proof size, achieving a
reduction rate of 37%–82%. The incurred verification time overhead is 5%–24%
for Dep. Min. and 7%–20% for Dep. Min. Glob.. In addition, the results
indicate a reduction in proof checking time of up to 88%. We observe that this
reduction is not necessarily correlated with the reduction rate of proof sizes; and
we hypothesize that this stems from the fact that checking time of each lemma is
dependent on its sparsity, and that our approach retains sparser lemmas in the
proof tree. Comparing the minimization algorithms, the results show that Algo-
rithm 1 is responsible for most of the removed lemmas, and both Algorithm 2
and Algorithm 3 improve it further with generally similar impact, except for the
Cora benchmarks. However, both algorithms incur a small overhead comparing
to using Algorithm 1 alone. Analyzing Min. Baseline indicates that changes
in data structures contributed to a minor improvement in both verification time
and proof-checking time, for most benchmarks. This has moderated the time
overhead of the minimization algorithms. As expected, bookeeping more infor-
mation slightly increased the number of overall Memouts of Min. Baseline
compared to Baseline. When applying the minimization algorithms however,
the number of Memouts decreases significantly, due to the reduction of proof
size (see subsections below).
     In the subsequent subsections, we provide a more detailed analysis of the
results for each benchmark suite.


Acas-Xu Benchmark. The Acas-Xu suite consists of fully connected feed-
forward networks trained to support drone collision avoidance decision-making.
We ran experiments on a set of 45 networks, each comprised of 6 hidden layers,
each of which contained 50 neurons with ReLU activation functions. For each
network we verified 4 different specifications [45]. This results in a total of 180
queries. The comparison in Table 1 was conducted on 82 UNSAT and 39 SAT
queries solved by all methods. Notably, a single query was either solved with a
failure during proof certification, or terminated due to memory out. This result
                                                    Acas-Xu                                                                                                                 Cersyve                                                                                                                             Cora
                                     1e7
                                             All Vectors                                                                                                                  All Vectors                                                                                                                 All Vectors




                                                                                                                                                                                                                                            Proof Size with Minimization
                                                                                                                                                                                                                                                                           500000
Proof Size with Minimization




                                                                                                                       Proof Size with Minimization
                               2.0
                                             Baseline                                                                                                 400000              Baseline                                                                                                                    Baseline
                                             Min. Baseline                                                                                                                Min. Baseline                                                                                                               Min. Baseline
                               1.5           Dep. Analysis                                                                                                                Dep. Analysis
                                                                                                                                                                                                                                                                           400000                     Dep. Analysis
                                             Dep. Min.
                                                                                                                                                      300000
                                                                                                                                                                          Dep. Min.                                                                                                                   Dep. Min.
                                             Dep. Min. Glob.                                                                                                              Dep. Min. Glob.                                                                                  300000                     Dep. Min. Glob.
                               1.0
                                                                                                                                                      200000
                                                                                                                                                                                                                                                                           200000

                               0.5                                                                                                                    100000                                                                                                               100000

                               0.0                                                                                                                             0                                                                                                                  0
                                      0.0            0.5              1.0                   1.5           2.0                                                                                                                                                                           0              100000     200000        300000          400000    500000
                                             Proof Size without Minimization                                     1e7                                               0        100000          200000
                                                                                                                                                                         Proof Size without Minimization
                                                                                                                                                                                                            300000            400000
                                                                                                                                                                                                                                                                                                 Proof Size without Minimization
                                                 Baseline                                                                                                                                                                                                                  120                   Baseline
Number of Solved Queries




                                                                                                                                                                                                                                            Number of Solved Queries
                                                                                                                                                                       Baseline
                                                                                                                       Number of Solved Queries




                               140
                                                 Min. Baseline                                                                                        10               Min. Baseline                                                                                                             Min. Baseline
                               120               Dep. Analysis                                                                                                         Dep. Analysis
                                                                                                                                                                                                                                                                           100                   Dep. Analysis
                               100
                                                 Dep. Min.                                                                                             8               Dep. Min.                                                                                                                 Dep. Min.
                                                                                                                                                                                                                                                                            80
                                                 Dep. Min. Glob                                                                                                        Dep. Min. Glob.                                                                                                           Dep. Min. Glob.
                                80
                                                                                                                                                       6                                                                                                                    60
                                60
                                                                                                                                                                                                                                                                            40
                                40                                                                                                                     4

                                20                                                                                                                                                                                                                                          20
                                                                                                                                                       2
                                 0                                                                                                                                                                                                                                           0
                                            21       23        25           27         29         211    213                                                                                                                                                                           26        27        28      29         210         211     212    213         214
                                                         Runtime (seconds)                                                                                         23      21        21
                                                                                                                                                                             Runtime (seconds)
                                                                                                                                                                                                  23        25         27          29
                                                                                                                                                                                                                                                                                                           Runtime (seconds)
                                                  Maxleaky                                                                                                                Robotics                                                                                                                     SafeNLP
                                     1e6                                                                                                              100000                                                                                                                     1e6
                               2.5                                                                                                                                       All Vectors                                                                                       3.5
                                                                                                                                                                                                                                                                                             All Vectors
                                                                                                                       Proof Size with Minimization




                                             All Vectors
                                                                                                                                                                                                                                            Proof Size with Minimization


                                                                                                                                                                         Baseline
Proof Size with Minimization




                                             Baseline                                                                                                 80000                                                                                                                3.0               Baseline
                               2.0                                                                                                                                       Min. Baseline                                                                                                       Min. Baseline
                                             Min. Baseline                                                                                                               Dep. Analysis
                                             Dep. Analysis
                                                                                                                                                                                                                                                                           2.5               Dep. Analysis
                                                                                                                                                      60000              Dep. Min.                                                                                                           Dep. Min.
                               1.5           Dep. Min.                                                                                                                   Dep. Min. Glob.                                                                                   2.0
                                             Dep. Min. Glob.                                                                                                                                                                                                                                 Dep. Min. Glob.
                                                                                                                                                      40000                                                                                                                1.5
                               1.0
                                                                                                                                                                                                                                                                           1.0
                                                                                                                                                      20000
                               0.5                                                                                                                                                                                                                                         0.5

                               0.0                                                                                                                             0                                                                                                           0.0
                                                                                                                                                                   0       20000          40000         60000         80000        100000                                         0.0            0.5        1.0         1.5         2.0         2.5      3.0          3.5
                                      0.0          0.5          1.0
                                             Proof Size without Minimization
                                                                                 1.5               2.0           2.5
                                                                                                                1e6                                                     Proof Size without Minimization                                                                                      Proof Size without Minimization                                          1e6


                               120                                                                                                                                                                                                                                         800
                                                                                                                       Number of Solved Queries




                                                                                                                                                                                                                                            Number of Solved Queries




                                                 Baseline
Number of Solved Queries




                                                                                                                                                                                                                                                                           700
                               100               Min. Baseline                                                                                        2000
                                                 Dep. Analysis                                                                                                                                                                                                             600
                                80               Dep. Min.                                                                                            1500                                                                                                                 500
                                                 Dep. Min. Glob.
                                                                                                                                                                                                                                                                           400
                                60
                                                                                                                                                      1000
                                                                                                                                                                                                                 Baseline                                                  300                                                                  Baseline
                                40                                                                                                                                                                               Min. Baseline                                             200
                                                                                                                                                                                                                                                                                                                                                Min. Baseline
                                                                                                                                                       500                                                       Dep. Analysis                                                                                                                  Dep. Analysis
                                20                                                                                                                                                                               Dep. Min.                                                 100                                                                  Dep. Min.
                                                                                                                                                           0                                                     Dep. Min. Glob.                                             0                                                                  Dep. Min. Glob.
                                 0
                                                                                                                                                                   27       25        23               21        21           23                                                            24            21            22          25            28           211
                                            24            21          22
                                                         Runtime (seconds)
                                                                                  25              28       211
                                                                                                                                                                                Runtime (seconds)                                                                                                          Runtime (seconds)

                                       Fig. 5: Proof size and runtime comparison across all benchmarks and methods.
Table 1: Average proof size (number of leaves and lemmas), verification time
for all queries and proof-checking time for UNSAT queries, using Marabou across
benchmarks. Lower values indicate more compact proofs. Each non-baseline en-
try includes both reported numbers, and percentage of change with respect to
baseline. Best results among our three algorithms are marked in bold.
                               Avg. Proof Size [±% of Baseline]
  Benchmark            Avg. Verification Time (Sec.) [±% of Baseline]
                         Avg. Checking Time (Sec.) [±% of Baseline]
           Baseline [39] Min. Baseline Dep. Analysis Dep. Min. Dep. Min. Glob.
                           302021.14       59231.07    52890.17      53144.84
            302021.14
                               0%           -80.4%     -82.5%          -82.4%
                             269.42         299.96       294.58        288.42
  Acas-Xu      265.98
                             +1.2%         +12.8%      +10.7%         +8.4%
                              46.58           8.67        7.78           8.15
               66.37
                             -29.8%         -86.9%     -88.3%          -87.7%
                            163592.4       60764.6     51283.6        51492.6
             163592.4
                               0%           -62.9%     -68.6%          -68.5%
                              84.84          96.90       93.02         104.57
   cersyve     86.99
                              -2.5%        +11.4%      +6.9%          +20.2%
                              13.66           3.14        2.62           2.77
               13.77
                              -0.8%         -77.2%       -81%          -79.9%
                            49202.05       15199.58    8819.75       11549.88
             49202.05
                               0%           -69.1%     -82.1%          -76.5%
                             1231.5        1262.87      1583.02       1405.65
    Cora      1277.88
                              -3.6%         -1.2%      +23.9%           +10%
                             1572.66        455.88      266.17         365.32
              1633.47
                              -3.7%         -72.1%     -83.7%          -77.6%
                            55342.88       42224.96    34852.52     34847.12
             55342.88
                               0%           -23.7%        -37%          -37%
                              56.34          59.01         59.7         60.01
  MaxLeaky     60.85
                              -7.4%           -3%        -1.9%          -1.4%
                               2.63           2.07        1.89           1.89
                2.67
                              -1.5%         -22.5%     -29.2%         -29.2%
                            25549.65       11981.7     8016.64        8026.99
             25549.65
                               0%           -53.1%     -68.6%          -68.6%
                               0.53           0.57         0.58          0.59
  Robotics      0.55
                              -3.6%         +3.6%       +5.4%          +7.3%
                               0.31           0.15        0.11           0.11
                0.32
                              -3.1%         -53.1%     -65.6%         -65.6%
                            55066.71       17135.91    10118.98     10062.95
             55066.71
                               0%           -68.9%      -81.6%         -81.7%
                              14.27          14.73       14.94          15.88
  SafeNLP      14.69
                              -2.8%         +0.3%       +1.7%          +8.1%
                               7.78           1.59        0.96           0.97
                5.89
                              +32%           -73%      -83.7%          -83.5%


is consistent with the original evaluation of the Acas-Xu benchmark in [39], and
we hypothesize that for this particular verification instance, the proof-producing
Marabou is numerically unstable.
    To assess robustness under resource constraints, we also report the number
of queries that were successfully solved within the 5-hour timeout and 16GB
memory limit. Table 2 summarizes the number of solved queries for each method.
As shown, all three minimization methods outperform the baseline, solving more
queries by avoiding memory blowup during proof construction.


cersyve Benchmark. The cersyve suite consists of fully connected feedfor-
ward networks serving as neural certificates for control systems. We ran experi-
ments on a set of 12 networks, with 65 to 198 ReLU neurons. For each network
we verified a single property, as in the VNNCOMP 2025 benchmark [67]. This
Table 2: Number of Acas-Xu SAT queries solved, UNSAT queries solved, timed
out, and failed due to memory exhaustion, out of 180 queries.
             Method         #SAT #UNSAT #Timeout #Memout
             Baseline        41    82      0       57
             Min. Baseline   39    82      0       59
             Dep. Analysis   44   107      29       0
             Dep. Min.       44   104      21      11
             Dep. Min. Glob. 44    96      20      20
results in a total of 12 queries, out of which 6 are UNSAT. For this benchmark,
all methods successfully verified 11 queries, whereas a single UNSAT query fails
due to memory restrictions when tested on all methods.

Cora Benchmark. The Cora benchmark consists of local adversarial robust-
ness queries for image classifiers trained on several datasets. For our experiments,
we used a subset of these queries on a feedforward DNN with seven layers of 250
ReLU neurons each, trained on the MNIST dataset. To extend the benchmark
and improve scalability, each query was further divided into nine sub-queries,
each corresponding to a single possible misclassification option. In total, this
yields 189 queries. The comparison in Table 1 was conducted on 104 UNSAT
queries solved by all methods.
    In Table 3, we report the number of instances verified under a time limit of
5 hours and a memory limit of 16GB. As previously observed, the analysis and
minimization algorithms increase the total number of solved queries, this time
primarily due to improvements in overall running time. Since the reduction in
proof-checking time is more significant than the reduction in verification time
(as shown in Table 1), we conclude that the overall improvement is mainly
attributable to the reduced time of proof-checking.
Table 3: Number of Cora SAT queries solved, UNSAT queries solved, timed out,
and failed due to memory exhaustion, out of 189 queries.
             Method         #SAT #UNSAT #Timeout #Memout
             Baseline        1    107      81       0
             Min. Baseline   1    106      81       1
             Dep. Analysis   1    118      70       0
             Dep. Min.       0    122      67       0
             Dep. Min. Glob. 1    119      69       0


MaxLeaky Benchmark. The MaxLeaky benchmark includes a single DNN
trained to classify wine types based on chemical composition [23]. To test our
approach over a DNN which employs various activation functions, we trained a
fresh DNN with 64 ReLU, 32 LeakyReLU, and 16 Maxpool neurons, to classify
the dataset. We then generated a single adversarial robustness query for 133 train
and 44 test data points. This results in a total of 177 queries. The comparison
in Table 1 was conducted on 99 UNSAT and 12 SAT queries solved by all methods.
    Table 4 includes the number of instances verified under the limitation of
2.5-hour time and 2GB memory. The results indicate a minor reduction in the
number of solved queries when introducing the minimization algorithms. This
result is unique, and is likely a result of the relatively moderate reduction of
proof size (see Table 1), combined with the small overhead introduced when
keeping additional information for each lemma (see Section 3.1).
Table 4: Number of MaxLeaky SAT queries solved, UNSAT queries solved, timed
out, and failed due to memory exhaustion, out of 177 queries.
             Method         #SAT #UNSAT #Timeout #Memout
             Baseline        12   163      1        1
             Min. Baseline   12   160      0        5
             Dep. Analysis   12   160      1        4
             Dep. Min.       12   162      0        3
             Dep. Min. Glob. 12   160      0        5

Robotics Navigation Benchmark. The robotic navigation benchmark [3]
involves DNN controllers for obstacle avoidance. We tested our approach on
2340 queries from this benchmark, where 2126 of them are SAT queries, and 214
are UNSAT. Each query includes a DNN with the ReLU activation only. The DNN
is comprised of an input layer with 9 neurons, two hidden layers with 16 neurons
each, and an output layer of 3 neurons. For this benchmark, all methods were
able to verify all queries and produce proofs in the time and memory limitations.

SafeNLP Benchmark. The safeNLP benchmark [17, 18] examines robust-
ness to word- and sentence-level perturbations in the embedding space of several
sentences over two fully-connected DNNs. Both DNNs have the same architec-
ture, which is comprised of an input layer of 30 nodes, a single hidden layer
of 128 nodes with ReLU activation functions, and an output layer of 2 nodes.
The benchmark consists of 1080 queries in total. The comparison in Table 1 was
conducted on 149 UNSAT and 599 SAT queries solved by all methods.
    Table 5 reports the number of queries successfully verified within the resource
limits (2.5 hours and 2GB RAM). Here again, our minimization methods demon-
strate improved performance, reducing memory exhaustion and increasing the
number of successful verification queries compared to the baseline.
Table 5: Number of safeNLP SAT queries solved, UNSAT queries solved, timed
out, and failed due to memory exhaustion, out of 1080 queries.
             Method         #SAT #UNSAT #Timeout #Memout
             Baseline        599  196      13      272
             Min. Baseline   599  194      7       280
             Dep. Analysis   599  214      36      231
             Dep. Min.       599  219      54      208
             Dep. Min. Glob. 599  215      42      224


5   Related Work
Producing proofs as witnesses of correctness is a common practice in both SMT
and SAT solving. In both communities, the proof size tends to be significant, lim-
iting their applicability [7,8,37,63]. Our work builds on concepts inspired by lazy
proofs [46], where proof objects are constructed gradually, using only necessary
lemmas. In DNN verification, proof production has been studied only recently,
and in a handful of works [39, 61]. The authors of [61] consider a symbolic ap-
proach for increasing the reliability of DNN verifiers, which reduces the problem
to an additional SMT query. Our approach is then not directly applicable to [61].
     The study of dependencies analysis of UNSAT results has been explored in
various contexts [14, 36, 43, 44, 50] often using the name UNSAT core. To the best
of our knowledge, ours is the first to investigate this in the context of DNN
verification. In DNN verification, previous studies have attempted to analyze
dependencies between the phases of neurons as part of the DNN verification
process [13]. As fixing neuron phases could be captured by proof lemmas, it
would be interesting to study the synergies between that approach and ours.
     In linear programming, the well-established concept of Irreducible Infeasible
Systems [20] is defined as a minimal set of constraints that maintain unsatisfi-
ablity. The method to detect IISs from [20] has been used in DNN verifiers [30],
and is implemented in the Gurobi linear optimizer [35] often used in DNN ver-
ifiers. Although IIS detection algorithms typically rely on repeated LP solver
invocations, which can be computationally expensive, it presents a compelling
direction for future exploration in this work’s context.


6   Conclusion and Future Work

In this work, we developed methods to reduce the size of UNSAT proofs generated
by DNN verifiers, as presented in [39]. These proofs can be checked by a trusted,
external proof checker in order to improve reliability of the DNN verifier. Im-
portantly, DNN verifiers currently assume ideal mathematical implementation
of the DNN itself, and modeling any specific DNN implementations remains a
challenge for the DNN verification community in general [22]. Our goal here is
to improve memory consumption in proof-producing verifiers and reduce proof
checking time, thereby enhancing the practicality of reliable DNN verification.
    To this end, we designed an algorithm that analyzes, for each lemma in the
proof, its dependencies on previously derived lemmas. This enables us to elim-
inate lemmas that are eagerly learned but are ultimately irrelevant for proving
UNSAT. In addition, we designed an algorithm to minimize the number of such
dependencies, with two variants. All algorithms have been implemented on top
of the proof-producing version of the Marabou DNN verifier [70].
    Our results show that Algorithm 1 reduces proof size by an order of mag-
nitude across multiple benchmarks. The dependency minimization algorithms
further reduces proof size, though more moderately. When comparing the two
variants of the minimization algorithm, both versions achieve similar results on
almost all benchmarks. Moreover, the performance overhead introduced by our
methods is reasonable, especially when considering improvements in proof check-
ing time. Notably, the time overhead from the dependency analysis is reduced
due to the use of some alternative data structures.
Future Work. Moving forward, we intend to continue this work along sev-
eral paths. First, we aim to explore different variants of proof minimization.
In particular, our current algorithms consider a fixed proof vector w, which we
could try to alter in order to reduce the number of dependencies even further.
Additionally, it would be interesting to explore additional alternatives to the
minimization algorithm, attempting to remove dependencies according to other
heuristics, e.g., by their stage of deduction. Furthermore, it would also be inter-
esting to consider the sparsity of the proof vectors and prioritize removing dense
vectors, as they (heuristically) depend on many other bound lemmas.
     Second, we aim to extend the proof checker as in [26], to support checking
proofs of bound tightening lemmas. We will then evaluate the reduction of proof-
checking time for this version of the checker as well.
     A third direction for future research is extending our work to support ad-
ditional subroutines commonly used in DNN verifiers, particularly abstract in-
terpretation. This integration is inherently more complex, as it requires proving
linear relaxations of non-linear constraints. However, once this support is estab-
lished, we believe our proof minimization approach and technique could also be
useful in this context.
     Fourth, our work’s analysis method paves the way for a conflict analysis
method, as a part of Conflict-Driven Clause Learning [10, 59, 60] scheme, which
is commonly used in SAT and SMT solving [9,11]. Conceptually, in search-based
solving, CDCL identifies subspaces of the search space which are “similar” to
subspaces already traversed, and which were shown not to contain any satisfy-
ing assignment. This similarity guarantees that the new subspaces also do not
contain any such assignment, and they can be safely skipped by the verifier. A
core component in CDCL is the generation of conflict clauses, a representation
of an UNSAT subspaces, that guide the solver not to search in other subspaces
that are also guaranteed to be UNSAT. Naturally, the algorithm for deriving con-
flict clauses is a key to a successful CDCL framework. Our work can serve as
a basis for the derivation of potentially useful conflict clauses for DNN verifiers
— leading to a significant improvement in their performance. Although several
DNN verifiers employ CDCL or similar algorithms [29, 30, 51, 73], to the best of
our knowledge, none of these use UNSAT proofs for deriving conflict clauses.
Data Availability. The implementation and scripts used for the experiments
in Section 4 are publicly available [56].
Acknowledgments. The work of Isac, Refaeli and Katz was supported by the
Binational Science Foundation (grant numbers 2020250 and 2021769), the Is-
raeli Science Foundation (grant number 558/24) and the European Union (ERC,
VeriDeL, 101112713). Views and opinions expressed are however those of the au-
thor(s) only and do not necessarily reflect those of the European Union or the
European Research Council Executive Agency. Neither the European Union nor
the granting authority can be held responsible for them.
    The work of Barrett was supported in part by the Binational Science Founda-
tion (grant number 2020250), the National Science Foundation (grant numbers
1814369 and 2211505), and the Stanford Center for AI Safety.
References
 1. E. Abraham and G. Kremer. SMT Solving for Arithmetic Theories: Theory and
    Tool Support. In Proc. 19th Int. Symposium on Symbolic and Numeric Algorithms
    for Scientific Computing (SYNASC), pages 1–8, 2017.
 2. M. Akintunde, A. Kevorchian, A. Lomuscio, and E. Pirovano. Verification of RNN-
    Based Neural Agent-Environment Systems. In Proc. 33rd AAAI Conf. on Artificial
    Intelligence (AAAI), pages 197–210, 2019.
 3. G. Amir, D. Corsi, R. Yerushalmi, L. Marzari, D. Harel, A. Farinelli, and G. Katz.
    Verifying Learning-Based Robotic Navigation Systems. In Proc. 29th Int. Conf.
    on Tools and Algorithms for the Construction and Analysis of Systems (TACAS),
    pages 607–627, 2023.
 4. G. Amir, Z. Freund, G. Katz, E. Mandelbaum, and I. Refaeli. veriFIRE: Verify-
    ing an Industrial, Learning-Based Wildfire Detection System. In Proc. 25th Int.
    Symposium on Formal Methods (FM), pages 648–656, 2023.
 5. G. Avni, R. Bloem, K. Chatterjee, T. Henzinger, B. Konighofer, and S. Pranger.
    Run-Time Optimization for Learned Controllers through Quantitative Games. In
    Proc. 31st Int. Conf. on Computer Aided Verification (CAV), pages 630–649, 2019.
 6. T. Baluta, S. Shen, S. Shinde, K. Meel, and P. Saxena. Quantitative Verification
    of Neural Networks And its Security Applications. In Proc. 26th ACM Conf. on
    Computer and Communication Security (CCS), 2019.
 7. H. Barbosa, C. Barrett, B. Cook, B. Dutertre, G. Kremer, H. Lachnitt, A. Niemetz,
    A. Nötzli, A. Ozdemir, M. Preiner, A. Reynolds, C. Tinelli, and Y. Zohar. Gen-
    erating and Exploiting Automated Reasoning Proof Certificates. Communications
    of the ACM, 66(10):86–95, 2023.
 8. C. Barrett, L. de Moura, and P. Fontaine. Proofs in Satisfiability Modulo Theories.
    All about Proofs, Proofs for All, 55(1):23–44, 2015.
 9. C. Barrett and C. Tinelli. Satisfiability Modulo Theories. In E. Clarke, T. Hen-
    zinger, H. Veith, and R. Bloem, editors, Handbook of Model Checking, pages 305–
    343. Springer International Publishing, 2018.
10. R. Bayardo Jr and R. Schrag. Using CSP Look-Back Techniques to Solve Real-
    World SAT Instances. In Proc. 14th Nat. Conf. on Artificial Intelligence (AAAI),
    pages 203–208, 1997.
11. A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks, and F. Pollitt. CaDiCaL 2.0.
    In Proc. 36th Int. Conf. on Computer Aided Verification (CAV), pages 133–152,
    2024.
12. M. Bojarski, D. Del Testa, D. Dworakowski, B. Firner, B. Flepp, P. Goyal,
    L. Jackel, M. Monfort, U. Muller, J. Zhang, X. Zhang, J. Zhao, and K. Zieba.
    End to End Learning for Self-Driving Cars, 2016. Technical Report. http:
    //arxiv.org/abs/1604.07316.
13. E. Botoeva, P. Kouvaros, J. Kronqvist, A. Lomuscio, and R. Misener. Efficient
    Verification of ReLU-Based Neural Networks via Dependency Analysis. In Proc.
    34th AAAI Conf. on Artificial Intelligence (AAAI), pages 3291–3299, 2020.
14. A. Bradley and Z. Manna. Property-Directed Incremental Invariant Generation.
    Formal Aspects of Computing, 20:379–405, 2008.
15. C. Brix, S. Bak, T. Johnson, and H. Wu. The Fifth International Verification of
    Neural Networks Competition (VNN-COMP 2024): Summary and Results, 2024.
    Technical Report. http://arxiv.org/abs/2412.19985.
16. C. Brix, M. Müller, S. Bak, T. Johnson, and C. Liu. First Three Years of the
    International Verification of Neural Networks Competition (VNN-COMP). Int.
    Journal on Software Tools for Technology Transfer, pages 1–11, 2023.
17. M. Casadio, L. Arnaboldi, M. Daggitt, O. Isac, T. Dinkar, D. Kienitz, V. Rieser,
    and E. Komendantskaya. ANTONIO: Towards a Systematic Method of Generating
    NLP Benchmarks for Verification. In Proc. 6th Workshop on Formal Methods for
    ML-Enabled Autonomous Systems (FoMLAS), volume 16, pages 59–70, 2023.
18. M. Casadio, T. Dinkar, E. Komendantskaya, L. Arnaboldi, M. L. Daggitt, O. Isac,
    G. Katz, V. Rieser, and O. Lemon. NLP Verification: Towards a General Method-
    ology for Certifying Robustness. European Journal of Applied Mathematics, page
    1–58, 2025.
19. C.-H. Cheng, F. Diehl, G. Hinz, Y. Hamza, G. Nührenberg, M. Rickert, H. Ruess,
    and M. Truong-Le. Neural Networks for Safety-Critical Applications — Challenges,
    Experiments and Perspectives. In Proc. Int. Conf. on Design, Automation and Test
    in Europe (DATE), pages 1005–1006. IEEE, 2018.
20. J. Chinneck and E. Dravnieks. Locating Minimal Infeasible Constraint Sets in
    Linear Programs. ORSA Journal on Computing, 3(2):157–168, 1991.
21. V. Chvátal. Linear Programming. W. H. Freeman and Company, 1983.
22. L. C. Cordeiro, M. L. Daggitt, J. Girard-Satabin, O. Isac, T. T. Johnson, G. Katz,
    E. Komendantskaya, A. Lemesle, E. Manino, A. Šinkarovs, and H. Wu. Neural Net-
    work Verification is a Programming Language Challenge. In Proc. 34th European
    Symposium on Programming (ESOP), pages 206–235, 2025.
23. P. Cortez, A. Cerdeira, F. Almeida, T. Matos, and J. Reis. Modeling Wine Prefer-
    ences by Data Mining from Physicochemical Properties. Decision Support Systems,
    47(4):547–553, 2009.
24. G. Dantzig. Linear Programming and Extensions. Princeton University Press,
    1963.
25. L. de Moura and N. Bjørner. Satisfiability Modulo Theories: Introduction and
    Applications. Communications of the ACM, 54(9):69–77, 2011.
26. R. Desmartin, O. Isac, E. Komendantskaya, K. Stark, G. Passmore, and G. Katz.
    A Certified Proof Checker for Deep Neural Network Verification in Imandra. In
    Proc. 16th Int. Conf. on Interactive Theorem Proving (ITP), pages 1–21, 2025.
27. R. Desmartin, O. Isac, G. Passmore, K. Stark, E. Komendantskaya, and G. Katz.
    Towards a Certified Proof Checker for Deep Neural Network Verification. In
    Proc. 33rd Int. Symposium on Logic-Based Program Synthesis and Transforma-
    tion (LOPSTR), pages 198–209, 2023.
28. S. Dubey, S. Singh, and B. Chaudhuri. Activation Functions in Deep Learning: A
    Comprehensive Survey and Benchmark. Neurocomputing, 2022.
29. H. Duong, T. Nguyen, and M. Dwyer. A DPLL(T) Framework for Verifying Deep
    Neural Networks, 2023. Technical Report. http://arxiv.org/abs/2307.10266.
30. R. Ehlers. Formal Verification of Piece-Wise Linear Feed-Forward Neural Net-
    works. In Proc. 15th Int. Symp. on Automated Technology for Verification and
    Analysis (ATVA), pages 269–286, 2017.
31. Y. Elboher, R. Elsaleh, O. Isac, M. Ducoffe, A. Galametz, G. Povéda, R. Bouma-
    zouza, N. Cohen, and G. Katz. Robustness Assessment of a Runway Object Clas-
    sifier for Safe Aircraft Taxiing. In Proc. 43rd Int. Digital Avionics Systems Conf.
    (DASC), 2024.
32. T. Gehr, M. Mirman, D. Drachsler-Cohen, E. Tsankov, S. Chaudhuri, and
    M. Vechev. AI2: Safety and Robustness Certification of Neural Networks with
    Abstract Interpretation. In Proc. 39th IEEE Symposium on Security and Privacy
    (S&P), 2018.
33. I. Goodfellow, Y. Bengio, and A. Courville. Deep Learning. MIT Press, 2016.
34. E. Goubault, S. Palumby, S. Putot, L. Rustenholz, and S. Sankaranarayanan. Static
    Analysis of ReLU Neural Networks with Tropical Polyhedra. In Proc. 28th Int.
    Static Analysis Symposium (SAS), pages 166–190, 2021.
35. The Gurobi Optimizer. https://www.gurobi.com/.
36. O. Guthmann, O. Strichman, and A. Trostanetski. Minimal Unsatisfiable Core
    Extraction for SMT. In In Proc. 16th Int. Conf. on Formal Methods in Computer-
    Aided Design (FMCAD), pages 57–64, 2016.
37. M. J. Heule and A. Biere. Proofs for Satisfiability Problems. All about Proofs,
    Proofs for all, 55(1):1–22, 2015.
38. X. Huang, M. Kwiatkowska, S. Wang, and M. Wu. Safety Verification of Deep
    Neural Networks. In Proc. 29th Int. Conf. on Computer Aided Verification (CAV),
    pages 3–29, 2017.
39. O. Isac, C. Barrett, M. Zhang, and G. Katz. Neural Network Verification with
    Proof Production. In Proc. 22nd Int. Conf. on Formal Methods in Computer-
    Aided Design (FMCAD), pages 38–48, 2022.
40. O. Isac, Y. Zohar, C. Barrett, and G. Katz. DNN Verification, Reachability, and the
    Exponential Function Problem. In Proc. 34th Int. Conf. on Concurrency Theory
    (CONCUR), 2023.
41. K. Jia and M. Rinard. Exploiting Verified Neural Networks via Floating Point
    Numerical Error. In Proc. 28th Int. Static Analysis Symposium (SAS), pages 191–
    205, 2021.
42. K. Julian, M. Kochenderfer, and M. Owen. Deep Neural Network Compression for
    Aircraft Collision Avoidance Systems. Journal of Guidance, Control, and Dynam-
    ics, 42(3):598–608, 2019.
43. U. Junker. Quickxplain: Conflict Detection for Arbitrary Constraint Propagation
    Algorithms. In Proc. Workshop on Modelling and Solving Problems with Con-
    straints, 2001.
44. U. Junker. Quickxplain: Preferred Explanations and Relaxations for Over-
    Constrained Problems. In Proc. 19th Nat. Conf. on Artifical Intelligence (AAAI),
    pages 167–172, 2004.
45. G. Katz, C. Barrett, D. Dill, K. Julian, and M. Kochenderfer. Reluplex: a Calculus
    for Reasoning about Deep Neural Networks. Formal Methods in System Design
    (FMSD), 2021.
46. G. Katz, C. Barrett, C. Tinelli, A. Reynolds, and L. Hadarean. Lazy Proofs for
    DPLL(T)-Based SMT Solvers. In Proc. 16th Int. Conf. on Formal Methods in
    Computer-Aided Design (FMCAD), pages 93–100, 2016.
47. G. Katz, D. Huang, D. Ibeling, K. Julian, C. Lazarus, R. Lim, P. Shah, S. Thakoor,
    H. Wu, A. Zeljić, D. Dill, M. Kochenderfer, and C. Barrett. The Marabou Frame-
    work for Verification and Analysis of Deep Neural Networks. In Proc. 31st Int.
    Conf. on Computer Aided Verification (CAV), pages 443–452, 2019.
48. L. Koller, T. Ladner, and M. Althoff. Set-Based Training for Neural Network
    Verification, 2024. Technical Report. http://arxiv.org/abs/2401.14961.
49. P. Kouvaros, F. Leofante, B. Edwards, C. Chung, D. Margineantu, and A. Lomus-
    cio. Verification of Semantic Key Point Detection for Aircraft Pose Estimation. In
    Proc. 20th Int. Conf. on Principles of Knowledge Representation and Reasoning
    (KR), pages 757–762, 2023.
50. M. H. Liffiton and K. A. Sakallah. Algorithms for Computing Minimal Unsatisfiable
    Subsets of Constraints. Journal of Automated Reasoning, 40:1–33, 2008.
51. Z. Liu, P. Yang, L. Zhang, and X. Huang. DeepCDCL: A CDCL-based Neural
    Network Verification Framework. In Proc. 18th Int. Symposium on Theoretical
    Aspects of Software Engineering (TASE), pages 343–355, 2024.
52. Z. Lyu, C.-Y. Ko, Z. Kong, N. Wong, D. Lin, and L. Daniel. Fastened Crown:
    Tightened Neural Network Robustness Certificates. In Proc. 34th AAAI Conf. on
    Artificial Intelligence (AAAI), pages 5037–5044, 2020.
53. OpenAI. ChatGPT. https://chatgpt.com.
54. L. Pulina and A. Tacchella. An Abstraction-Refinement Approach to Verifica-
    tion of Artificial Neural Networks. In Proc. 22nd Int. Conf. on Computer Aided
    Verification (CAV), pages 243–257, 2010.
55. P. Rajpurkar, E. Chen, O. Banerjee, and E. J. Topol. AI in Health and Medicine.
    Nature Medicine, 28(1):31–38, 2022.
56. I. Refaeli and O. Isac. Proof Minimization in Neural Network Verification (Arti-
    fact), 2025. https://zenodo.org/doi/10.5281/zenodo.17169557.
57. M. Sälzer and M. Lange. Reachability Is NP-Complete Even for the Simplest
    Neural Networks. In Proc. 15th Int. Conf. on Reachability Problems (RP), pages
    149–164, 2021.
58. S. Sankaranarayanan, S. Dutta, and S. Mover. Reaching Out Towards Fully Verified
    Autonomous Systems. In Proc. 13th Int. Conf. on Reachability Problems (RP),
    pages 22–32, 2019.
59. J. Silva and K. Sakallah. GRASP-A New Search Algorithm for Satisfiability. In
    Proc. 15th Int. Conf. on Computer Aided Design (ICCAD), pages 220–227, 1996.
60. J. M. Silva and K. A. Sakallah. GRASP: A Search Algorithm for Propositional
    Satisfiability. IEEE Transactions on Computers, 48(5):506–521, 1999.
61. A. Singh, Y. C. Sarita, C. Mendis, and G. Singh. Automated Verification of Sound-
    ness of DNN Certifiers. Proc. ACM on Programming Languages, 9, 2025.
62. G. Singh, T. Gehr, M. Puschel, and M. Vechev. An Abstract Domain for Certifying
    Neural Networks. In Proc. 46th ACM SIGPLAN Symposium on Principles of
    Programming Languages (POPL), 2019.
63. N. Sörensson and A. Biere. Minimizing Learned Clauses. In Proc. 12th Int.
    Conf. on Theory and Applications of Satisfiability Testing (SAT), pages 237–243.
    Springer, 2009.
64. C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, and
    R. Fergus. Intriguing Properties of Neural Networks, 2013. Technical Report.
    http://arxiv.org/abs/1312.6199.
65. V. Tjeng, K. Xiao, and R. Tedrake. Evaluating Robustness of Neural Networks
    with Mixed Integer Programming, 2017. Technical Report. http://arxiv.org/
    abs/1711.07356.
66. H.-D. Tran, S. Bak, W. Xiang, and T. Johnson. Verification of Deep Convolutional
    Neural Networks Using ImageStars. In Proc. 32nd Int. Conf. on Computer Aided
    Verification (CAV), pages 18–42, 2020.
67. The VNNCOMP 2025 Benchmarks Repository. https://github.com/VNN-COMP/
    vnncomp2025_benchmarks, 2025.
68. S. Wang, K. Pei, J. Whitehouse, J. Yang, and S. Jana. Formal Security Analysis
    of Neural Networks using Symbolic Intervals. In Proc. 27th USENIX Security
    Symposium, pages 1599–1614, 2018.
69. S. Wang, H. Zhang, K. Xu, X. Lin, S. Jana, C.-J. Hsieh, and Z. Kolter. Beta-Crown:
    Efficient Bound Propagation with Per-Neuron Split Constraints for Neural Network
    Robustness Verification. In Proc. 35th Conf. on Neural Information Processing
    Systems (NeurIPS, 2021.
70. H. Wu, O. Isac, A. Zeljić, T. Tagomori, M. Daggitt, W. Kokke, I. Refaeli, G. Amir,
    K. Julian, S. Bassan, P. Huang, O. Lahav, M. Wu, M. Zhang, E. Komendantskaya,
    G. Katz, and C. Barrett. Marabou 2.0: A Versatile Formal Analyzer of Neural
    Networks. In Proc. 36th Int. Conf. on Computer Aided Verification (CAV), 2024.
71. Y. Yang, H. Hu, T. Wei, S. E. Li, and C. Liu. Scalable Synthesis of Formally
    Verified Neural Value Function for Hamilton-Jacobi Reachability Analysis. Journal
    of Artificial Intelligence Research, 83, 2025.
72. H. Zhang, M. Shinn, A. Gupta, A. Gurfinkel, N. Le, and N. Narodytska. Verification
    of Recurrent Neural Networks for Cognitive Tasks via Reachability Analysis. In
    Proc. 24th European Conf. on Artificial Intelligence (ECAI), pages 1690–1697,
    2020.
73. D. Zhou, C. Brix, G. A. Hanasusanto, and H. Zhang. Scalable Neural Network
    Verification with Branch-and-Bound Inferred Cutting Planes. In Proc. 38th Conf.
    on Neural Information Processing Systems (NeurIPS), 2024.
74. D. Zombori, B. Bánhelyi, T. Csendes, I. Megyeri, and M. Jelasity. Fooling a Com-
    plete Neural Network Verifier. In Proc. 9th Int. Conf. on Learning Representations
    (ICLR), 2021.
