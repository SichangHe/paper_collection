                                         TensorRight: Automated Verification of Tensor Graph
                                         Rewrites
                                         JAI ARORA, University of Illinois Urbana-Champaign, USA
                                         SIRUI LU, University of Washington, USA
                                         DEVANSH JAIN, University of Illinois Urbana-Champaign, USA
                                         TIANFAN XU, University of Illinois Urbana-Champaign, USA
                                         FARZIN HOUSHMAND, Google, USA
arXiv:2511.17838v1 [cs.PL] 21 Nov 2025




                                         PHITCHAYA MANGPO PHOTHILIMTHANA, Google DeepMind, USA
                                         MOHSEN LESANI, University of California, Santa Cruz, USA
                                         PRAVEEN NARAYANAN, Google, USA
                                         KARTHIK SRINIVASA MURTHY, Google, USA
                                         RASTISLAV BODIK, Google DeepMind, USA
                                         AMIT SABNE, Google, USA
                                         CHARITH MENDIS, University of Illinois Urbana-Champaign, USA
                                         Tensor compilers, essential for generating efficient code for deep learning models across various applications,
                                         employ tensor graph rewrites as one of the key optimizations. These rewrites optimize tensor computational
                                         graphs with the expectation of preserving semantics for tensors of arbitrary rank and size. Despite this
                                         expectation, to the best of our knowledge, there does not exist a fully automated verification system to prove
                                         the soundness of these rewrites for tensors of arbitrary rank and size. Previous works, while successful in
                                         verifying rewrites with tensors of concrete rank, do not provide guarantees in the unbounded setting.
                                            To fill this gap, we introduce TensorRight, the first automatic verification system that can verify tensor
                                         graph rewrites for input tensors of arbitrary rank and size. We introduce a core language, TensorRight DSL,
                                         to represent rewrite rules using a novel axis definition, called aggregated-axis, which allows us to reason about
                                         an unbounded number of axes. We achieve unbounded verification by proving that there exists a bound on
                                         tensor ranks, under which bounded verification of all instances implies the correctness of the rewrite rule
                                         in the unbounded setting. We derive an algorithm to compute this rank using the denotational semantics of
                                         TensorRight DSL. TensorRight employs this algorithm to generate a finite number of bounded-verification
                                         proof obligations, which are then dispatched to an SMT solver using symbolic execution to automatically verify
                                         the correctness of the rewrite rules. We evaluate TensorRight’s verification capabilities by implementing
                                         rewrite rules present in XLA’s algebraic simplifier. The results demonstrate that TensorRight can prove the
                                         correctness of 115 out of 175 rules in their full generality, while the closest automatic, bounded-verification
                                         system can express only 18 of these rules.

                                         Authors’ Contact Information: Jai Arora, University of Illinois Urbana-Champaign, USA, jaia3@illinois.edu; Sirui Lu,
                                         University of Washington, USA, siruilu@cs.washington.edu; Devansh Jain, University of Illinois Urbana-Champaign,
                                         USA, devansh9@illinois.edu; Tianfan Xu, University of Illinois Urbana-Champaign, USA, tianfan3@illinois.edu; Farzin
                                         Houshmand, Google, USA, farzinh@google.com; Phitchaya Mangpo Phothilimthana, Google DeepMind, USA, mangpo@
                                         google.com; Mohsen Lesani, University of California, Santa Cruz, USA, mlesani@ucsc.edu; Praveen Narayanan, Google,
                                         USA, pravnar@google.com; Karthik Srinivasa Murthy, Google, USA, ksmurthy@google.com; Rastislav Bodik, Google
                                         DeepMind, USA, rastislavb@google.com; Amit Sabne, Google, USA, asabne@google.com; Charith Mendis, University of
                                         Illinois Urbana-Champaign, USA, charithm@illinois.edu.


                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
                                         the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses,
                                         contact the owner/author(s).
                                         © 2025 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2025/1-ART29
                                         https://doi.org/10.1145/3704865


                                                                           Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:2                                                                                                Arora et al.


CCS Concepts: • Theory of computation → Semantics and reasoning; Logic and verification; Auto-
mated reasoning; • Software and its engineering → Compilers; Formal methods.
Additional Key Words and Phrases: Unbounded Verification, Tensor Compilers, Denotational Semantics
ACM Reference Format:
Jai Arora, Sirui Lu, Devansh Jain, Tianfan Xu, Farzin Houshmand, Phitchaya Mangpo Phothilimthana, Mohsen
Lesani, Praveen Narayanan, Karthik Srinivasa Murthy, Rastislav Bodik, Amit Sabne, and Charith Mendis. 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites. Proc. ACM Program. Lang. 9, POPL, Article 29
(January 2025), 61 pages. https://doi.org/10.1145/3704865

1      Introduction
Deep learning frameworks, such as TensorFlow [1], PyTorch [31], and JAX [8], along with their
backend optimizing tensor compilers, such as XLA [11] and TorchInductor [2], have been instru-
mental in enabling machine learning (ML) practitioners to experiment, train, and deploy various
neural network architectures. These tensor compilers manipulate computations with tensors as
first-class objects, utilizing tensor computational graphs as their intermediate representation (IR).
The nodes in these graphs represent tensor operators, while the edges denote input/output tensors.
Examples include XLA’s High Level Operators (XLA-HLO) [12], PyTorch’s torch.fx operators [33],
and ONNX’s tensor operators [10]. Middle-end tensor compiler optimizations often transform
these tensor graphs to produce more efficient variants. A key optimization which has attracted
significant research [20, 38, 41] is tensor graph rewrites. This optimization is a common pass in
industrial tensor compilers such as XLA1 .
   Tensor graph rewrites transform a subgraph of the original tensor graph to an equivalent version
that is more efficient. For example, consider the dot (einsum) operator that takes two tensors and
a set of contraction and batch axes as input and performs sum-of-products over the specified
contraction axes. If the batch and contraction axes are empty (precondition), an expensive dot
operation may be decomposed into a simpler composition of element-wise multiplication and
expand operations (represented as dot(A,B) ⇒𝐶 binary(∗, expand(A), expand(B)) in our notation,
with precondition 𝐶). In general, these rewrite rules are expected to be correct for tensors of
arbitrary rank (number of axes) and size (individual axis sizes). We term this property as the rewrite
rules being rank- and size-polymorphic. We found that most tensor graph rewrites in XLA’s algebraic
simplifier have this property. Hence, it is important that compiler developers ascertain that the
rules are indeed correct for input tensors of arbitrary rank and size.
   There have been multiple efforts at formally proving the correctness of these rewrites. However,
automatically verifying tensor graph rewrites for tensors of arbitrary rank and size has remained
challenging. Previous automatic verification techniques instantiate fixed-ranked, concrete-sized
tensors with symbolic values as a part of their verification process. As a result, their proofs do not
generalize to the unbounded setting, where input tensors can be of arbitrary rank and size. Further,
existing verification systems do not support preconditions on rules, which we find abundant
in compilers such as XLA. For example, TASO [20] proposes an axiomatic approach to verify
tensor graph rewrites. The rewrite rules they synthesize from their axiom pool are rank- and
size-polymorphic. However, the axioms themselves are only verified on small, concrete-sized input
tensors. TENSAT [41] improves the search efficiency of TASO, but relies on TASO’s rewrite rule
synthesis and verification process. PET [38] uses statistical testing to give rigorous guarantees on
more expressive rewrites for tensor computational graphs of concrete-rank and concrete-sized
tensors. Successful works that have verified tensor graph rewrites in the unbounded setting have
been manual verification efforts with proof assistants like Coq [25, 26].
1 https://github.com/openxla/xla/blob/main/xla/hlo/transforms/simplifiers/algebraic_simplifier.cc



Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                      29:3


   In this paper, we introduce the first automatic, push-button verification system, TensorRight,
that allows users to succinctly express and verify tensor graph rewrite rules for input tensors of
arbitrary rank and size. Further, in order to aid tensor compiler developers, we develop TensorRight
to be able to handle the complexities of rewrite rules found in the XLA compiler. We have to overcome
several key challenges in realizing these goals.
   Representation. First, we need to succinctly represent tensor graph rewrite rules in a way that
allows reasoning about their correctness in the unbounded setting. Second, we need to model the
highly parameterized operators in XLA-HLO. For example, XLA-HLO’s conv operator works with
arbitrary batch, contraction, and spatial axes specifications and has rich padding and dilation
attributes. Further, XLA rewrite rules can be guarded by complicated preconditions.
   We overcome these challenges by designing a rewrite rule specification language, called Ten-
sorRight DSL, with tensor operators closely resembling those in XLA-HLO. TensorRight DSL
introduces a novel axis definition called aggregated-axis that represents a possibly unbounded set
of axes, rather than capturing one axis at a time. A tensor in TensorRight DSL consists of a finite
number of aggregated-axes, where they can potentially be instantiated to any number of axes. This
allows us to reason about how input tensors are mutated by tensor operators, treating similar axes
collectively. All TensorRight DSL operators are defined to work with aggregated-axes, making the
rewrite specifications rank- and size-polymorphic. Additionally, the representation with aggregated-
axes is general enough to support a sizable subset of tensor operators and their parameterizations,
as defined in XLA-HLO (e.g. conv). However, the representation cannot support layout-sensitive
operators, such as reshape and bitcast. We implemented the most common operators appearing
in XLA’s rewrite rules to demonstrate TensorRight DSL’s expressivity. Rewrite specifications in
TensorRight DSL accept preconditions, which can also be rank- and size-polymorphic. Finally,
we provide denotational semantics of these operators, which we use to verify these rules.
   Verification. The next major challenge that we need to overcome is: given specifications in the
TensorRight DSL, how can we automatically verify that the rewrites are correct? This requires
proving them correct in the unbounded setting. Instantiating unbounded tensors is not feasible,
while using symbolic tensors of concrete-rank and size during automatic verification can result in
proofs that only hold for input tensors of that particular rank and size, as shown in §2.3.
   To handle unbounded sizes, we leverage the capabilities of SMT solvers to perform unbounded
reasoning using uninterpreted functions and unbounded integers. For unbounded ranks, we over-
come the challenge by proving that there exists a bound on the ranks, such that if we prove the rule
correct for all possible ranks within the bound, then the rule is also correct for arbitrary ranks and
sizes. This allows us to reduce the unbounded verification problem to a set of bounded verification
cases, which can be dispatched to an automatic verification engine. We derive a bound inference
algorithm using the denotational semantics of TensorRight DSL. Given these theoretical founda-
tions, TensorRight automatically verifies a given rewrite rule written in TensorRight DSL in two
steps. First, it uses the bound inference algorithm to find a sufficient rank for each aggregated-axis.
Next, for all ranks equal to or below this bound, TensorRight instantiates concrete-ranked input
tensors for each aggregated-axis. It then uses big-step operational semantics, derived from the
denotational semantics of TensorRight DSL, to create proof obligations as SMT queries using
symbolic execution. If all of these bounded cases are proven by an SMT solver, TensorRight then
concludes that the rewrite rule is correct.
   We implement the TensorRight system in Haskell and use Grisette [29] as the symbolic evalua-
tion engine. We further provide a TensorRight Frontend that abstracts away some core Tensor-
Right DSL constructs to make developing rewrite rules easier. TensorRight dispatches all SMT
queries to the Z3 [15] SMT solver to ascertain the soundness of a given rewrite rule. To evaluate

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:4                                                                                           Arora et al.


TensorRight’s capabilities in representation and verification, we assessed it using a comprehensive
set of rules incorporated within XLA’s algebraic simplifier. We successfully represented 121 of these
rules and verified 115 of them in TensorRight. Almost all rules were verified in the unbounded
setting within a second. Comparatively, other bounded-verification systems, such as TASO [20] and
PET [38], could only express 14 and 18 rules and verify 6 and 16 rules, respectively, exemplifying
TensorRight’s representation and verification capabilities. Further, we show case studies where
TensorRight helps generalize rewrites with complicated preconditions, showcasing its usefulness
during compiler development.
   In summary, this paper makes the following contributions.
    • We present a language, TensorRight DSL (§4) to specify tensor graph rewrites with (1) a
       novel axis construct called aggregated-axes, allowing representation of operators and rewrite
       rules that are rank- and size-polymorphic (2) operator specifications that closely resemble
       XLA-HLO (3) precondition specifications on rewrite rules.
    • We provide denotational semantics for TensorRight DSL (§5). To the best of our knowledge,
       this is the first formalization of a sizable subset of operators in a production-quality tensor IR.
    • We provide the first automatic verification strategy (§6) that can reason about the correctness
       of tensor graph rewrites that are rank- and size-polymorphic.
    • We develop TensorRight that implements this verification strategy and evaluate it (§8) by
       representing and verifying tensor graph rewrites present in XLA’s algebraic simplifier.
TensorRight is open-source, publicly available at https://github.com/ADAPT-uiuc/TensorRight

2      Background and Motivation
We first provide background on tensors and related concepts before motivating the need for
automatic and unbounded verification of tensor graph rewrites. We then describe a key insight of
our unbounded-verification methodology.

2.1     Preliminaries
Tensors are a generalization of scalars (0-dimensional tensors), vectors (1-dimensional tensors), and
matrices (2-dimensional tensors) to 𝑛-dimensional objects. A popular implementation of a tensor is
multi-dimensional arrays. An axis of a tensor (also commonly known as a dimension) represents a
direction across which the tensor’s data can be traversed. The rank of a tensor (also commonly
known as its dimensionality) refers to the number of axes the tensor has. The shape of a tensor
describes the size of each axis, i.e., the number of elements that exist along each axis. The size of a
tensor refers to the total number of elements in the tensor, calculated as the product of individual
axis-sizes. The axes of an 𝑛-dimensional tensor are numbered from 0 up to 𝑛 − 1. Each element of a
tensor is uniquely identified by a list of positional indices, with one index for each axis.
    For example, a 2-dimensional tensor 𝑚, containing 3 groups of elements along axis 0 and 4 groups
of elements along axis 1, has a rank of 2, a shape of 3 × 4, and a size of 12. Such a tensor can be
accessed by a pair of positional indices: 𝑚[𝑖, 𝑗] denotes the value at the 𝑖 th position along axis 0 and
𝑗 th position along axis 1. Another way to implement tensors, called named tensors, assigns explicit
names to the axes of a tensor, referred to as named-axes. TensorRight adopts the latter approach,
which we describe in detail in §4.1.
   Tensor Graph Rewrites. A tensor operator refers to any operation that takes tensors as input and
returns tensors as output. A tensor computational graph is a directed acyclic graph that represents
a sequence of tensor operations. The nodes in the graph represent tensor operators, while the
edges indicate the flow of data (tensors) between these operators. Tensor graph rewriting is a key
optimization employed by tensor compilers, which replaces a subgraph of the input graph with

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                      29:5


another, equivalent subgraph, subject to certain preconditions. This optimization is governed by a
set of rules, called tensor graph rewrite rules.
   The algebraic simplifier of the XLA compiler contains hundreds of tensor graph rewrites, executed
during program compilation. Given that XLA consistently executes this simplifier, it is crucial to
ensure the correctness of these rewrite rules. However, currently the rewrite rules are not verified.
Therefore, the developers rely on unit tests and limit the generality of the rules to alleviate concerns
of introducing compiler bugs.
   We aim to automatically verify tensor graph rewrites deployed in XLA, which work with tensors
of arbitrary ranks and sizes. Existing verified tensor graph rewrite systems are either not automatic,
lack support for complex XLA-HLO operators and preconditions, or cannot verify rewrite rules in the
unbounded setting . We now demonstrate the importance of automatic and unbounded verification
of tensor graph rewrites and discuss a key insight that enables us to achieve these goals.

2.2   Need for Automatic Verification
The algebraic simplifier in XLA contains complex rewrite rules whose correctness is not intuitive.
Developers often limit the generality of these rewrite rules by imposing preconditions. For instance,
consider the FoldConvInputPad rule shown in Fig. 1.
   The idea behind the FoldConvInputPad rule is simple:
fold the padding operator into the convolution operator. It             FoldConvInputPad :
folds the edge padding, i.e., the lower and higher padding (𝑆𝑙𝑝            let 𝑆𝑜𝑙 = 𝑆𝑙 + 𝑆𝑙𝑝 in
                                                                           let 𝑆𝑜ℎ = 𝑆ℎ + 𝑆ℎ𝑝 in
and 𝑆ℎ𝑝 ) into the convolution padding (𝑆𝑙 and 𝑆ℎ ), but does
                                                                              conv(pad(𝑡, 0, 𝑆𝑙𝑝 , 𝑆ℎ𝑝 , 𝑆𝑖𝑝 ), 𝑡 ′,
not fold the interior padding (𝑆𝑖𝑝 ) into the base dilation (𝑆𝑖 ).                  𝐵, 𝐹, 𝑂,
The precondition of this rule requires zero interior padding                        𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 , 𝑆𝑖′ )
(𝑆𝑖𝑝 = 0) and a base dilation of one (𝑆𝑖 = 1). The XLA repository                        =⇒𝑆𝑖𝑝 =0 ∧ 𝑆𝑖 =1
contains the following comment2 on the preconditions:                         conv(𝑡, 𝑡 ′, 𝐵, 𝐹, 𝑂,
       Edge padding composes with itself in the straight-                           𝑆𝑜𝑙 , 𝑆𝑜ℎ , 𝑆𝑖 , 𝑆𝑖′ )
       forward way, but composing interior padding is
       nontrivial, and we cowardly refuse to think about              Fig. 1. FoldConvInputPad rule taken
       it. If we see interior padding in either the kPad or           from XLA’s Algebraic Simplifier.
       conv, bail if there’s any sort of padding in the other.
   Developers restrict the rule because the general case is non-trivial. Existence of an automatic
verification system would allow incremental refinement of the rule and provide counterexamples
during development. As a consequence, it would enable developers to build more general rewrite
rules and be confident that the rewrite rules are valid for arbitrary ranks and sizes. For example,
TensorRight can prove a more general version of the FoldConvInputPad rule with interior
padding, as discussed in §8.3. The generalization involves removing the precondition and computing
the folded padding and dilation attributes as: 𝑆𝑜𝑙 = 𝑆𝑙 +𝑆𝑖 ×𝑆𝑙𝑝 , 𝑆𝑜ℎ = 𝑆ℎ +𝑆𝑖 ×𝑆ℎ𝑝 , and 𝑆𝑜𝑖 = 𝑆𝑖 +𝑆𝑖 ×𝑆𝑖𝑝 .
This folding of attributes is non-trivial to come up with, but TensorRight can prove the rewrite
rule to be valid. With the aid of TensorRight, we believe that compiler engineers will be able
to quickly iterate through complex rewrite rules and get feedback on their correctness through
counterexamples, thereby increasing productivity.

2.3   Need for Unbounded Verification
We demonstrate with an example that verifying a tensor graph rewrite for a certain rank may not
be sufficient to guarantee correctness in the unbounded setting, where input tensors can be of
2 https://github.com/openxla/xla/blob/ac380bb187abdb3efbbac776141e3a2300209232/xla/service/algebraic_simplifier.cc#

L8764-L8767


                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:6                                                                                                           Arora et al.


arbitrary ranks and sizes. Consider the SliceDyUpSlice rule shown in Equation 1, where 𝑆 denotes
the shape of the input tensor Y, zero denotes a tensor with all values as 0, and 𝑣 denotes a vector
with all values as 𝑣. Other operator inputs like start, end, and stride are called operator attributes.
                               start          end              stride              start end stride
                                                      
                                              𝑆 +1
             dyup-slice(slice(Y, 0,                 , 1), zero, 1) =⇒ dyup-slice(slice(Y, 0, S, 2), zero, 1)           (1)
                                                2
                                                   update offset                             update offset
    The left-hand side (LHS) expression first applies the slice operator, which extracts a sub-tensor
                                                                       th
from Y by picking elements from the 0th index (start) up to the ⌊ 𝑆+1
                                                                    2 ⌋ index (end) along each axis.
It is then followed by the dyup-slice operator, which zeroes (update) out all the points whose axes
indices are greater than or equal to 1 (offset). The right-hand side (RHS) expression first applies
the slice operator, which extracts a sub-tensor from Y by picking every 2𝑛𝑑 element (stride) along
each axis. It is then followed by the dyup-slice operator, which zeroes out all the points whose axes
indices are greater than or equal to 1.

                                 Rank-1 input                                     Rank-2 input

                                  slice       dyup-slice                            slice     dyup-slice
       LHS                 Y                               0            Y                                  0   0

                                                           0                                               0   0




                                  slice       dyup-slice                            slice     dyup-slice
       RHS                 Y                               0            Y                                  0   0

                                                           0                                               0   0




Fig. 2. Illustration for SliceDyUpSlice rule depicting various regions in the input tensor for ranks 1 and 2.
The leftmost element is shown as crossed out. The green and blue regions indicate the elements extracted by
slice in LHS and RHS, respectively. The zeroed out region after the dyup-slice is indicated by 0-elements.


   Fig. 2 illustrates the rule applied to input tensors of rank 1 and 2. The crossed-out element
corresponds to the point with all indices as 0. We refer to this as the leftmost element. The leftmost
element is left untouched throughout the computation in both LHS and RHS. The green region,
along with the leftmost element, corresponds to the sub-tensor obtained after the slice in LHS. The
blue region, along with the leftmost element, corresponds to the sub-tensor obtained after the slice
in RHS. The zeroed out region after the dyup-slice is represented using 0-elements.
   As we can observe for the 1-dimensional case, the final LHS and RHS expressions are equal
since the green and blue regions get zeroed out completely. Meanwhile, for the 2-dimensional case,
the green and blue regions are not completely zeroed out, so the LHS and RHS expressions have
regions that do not match. Therefore, the rule is valid for rank 1 but is invalid for rank 2. In fact,
the rule is invalid for any rank higher than 2. This example demonstrates that verifying the rule for
a certain rank, in this case 1, does not guarantee correctness at other ranks, making it important to
verify the rule for all possible ranks.

2.4    Key Observation
A rewrite rule is valid if the LHS and RHS expressions are equal for input tensors of any rank.
Otherwise, the rule is invalid and would exhibit a counterexample. A counterexample contains a

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                                      29:7


valuation of all the variables in the rule (including tensors and operator attributes) and an access 𝐴
(list of positional indices), such that LHS[𝐴] and RHS[𝐴] do not match.
   Verifying a rule for each rank separately is infeasible since there are a denumerable number of
such ranks. However, we make an observation that there exists a sufficient rank 𝑘, such that if the
rule is valid for rank 𝑘, then it can be proven valid for any rank greater than 𝑘. This insight allows
us to avoid verifying the rewrite rule for ranks greater than 𝑘. A more intuitive way to understand
this is through its contraposition, i.e., if a counterexample exists at a rank greater than 𝑘, then
a counterexample exists at rank 𝑘. We demonstrate with the same example rule from §2.3 that
verifying the rule for rank 2 is sufficient to ensure correctness for all higher ranks.



        Y                          LHS[0,0,1]                                  Y             RHS[0,0,1]




                   slice           dyup-slice                                      slice     dyup-slice
                                                                      axis 2




                                                                                                                                axis 2
                                                           0      0                                                  0      0
                                                           0      0                                                  0      0
                                                axis 0




                                                                                                          axis 0
                                                           0      0                                                  0      0
                                                           0      0                                                  0      0

                                                         axis 1                                                    axis 1


                (a) LHS for rank-3 input                              (b) RHS for rank-3 input
Fig. 3. The SliceDyUpSlice specialized for rank-3 inputs. The LHS and RHS expressions are presented using
2-dimensional cross-sections along axis 2. The access 𝐴3 = [0, 0, 1] is highlighted in LHS and RHS.


   Consider the SliceDyUpSlice rule applied to input tensors of rank 3, as shown in Fig. 3. Clearly,
the LHS (Fig. 3a) and RHS (Fig. 3b) have regions (green and blue) that do not match. Therefore
the rule is invalid for rank 3 and exhibits a counterexample. The counterexample would contain
an access 𝐴3 at which LHS and RHS do not match. This access can correspond to any location in
the green and blue regions. Without loss of generality, we consider the case when 𝐴3 = [0, 0, 1],
highlighted as a sketched-out location in Fig. 3a and Fig. 3b.
   Given this counterexample at rank 3, we try to construct a counterexample at rank 2, which
would contain an access 𝐴2 . An obvious counterexample construction involves projecting out one of
the axes. There are 3 choices for the axis to project out: axis 0, axis 1, and axis 2, as shown in Fig. 3.
If we project out axis 2, then the resulting counterexample access 𝐴2 would be [0, 0], but LHS[0, 0]
and RHS[0, 0] have to always match since it is the leftmost element. Therefore, this projection does
not lead to a counterexample. We instead observe that projecting out any of axis 0 or axis 1 results
in a counterexample at rank 2. In fact, any counterexample at rank 3 for the SliceDyUpSlice rule
can be lowered to a counterexample at rank 2. Moreover, it can be shown that any counterexample
at a higher rank can be lowered to a counterexample at rank 2. Therefore, if the SliceDyUpSlice
rule is valid for rank 2, then it is valid for any higher-rank. Note that the same does not hold for
rank 1: given a counterexample at rank 2, we cannot construct a counterexample at rank 1. Based
on these observations, we conclude that 2 is a sufficient rank for this rule and verifying the rule for
ranks 1 and 2 ensures correctness in the unbounded setting.
   In TensorRight, we extend these observations to any arbitrary rule by first partitioning the
axes of a tensor into “groups”, where all axes in a group share the same “role” and are treated
uniformly by the operators. We then present an algorithm to compute a sufficient rank for each
group, allowing us to avoid verifying the rule for ranks beyond these sufficient ranks.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:8                                                                                                    Arora et al.


3      Overview
Our goal is to automatically verify rewrite rules for arbitrary tensors and operator attributes.
Handling arbitrary tensors requires reasoning about tensor values, axis sizes, and ranks, all of
which could be arbitrary. We illustrate the challenges in representing and verifying rewrite rules
with the help of an example and present TensorRight, that helps us overcome these challenges.

3.1     TensorRight Rewrite Rules
Similar to many other tensor graph rewrite systems, TensorRight rewrites are modeled as rewriting
an LHS tensor expression to an RHS tensor expression, subject to certain preconditions. The users
use the constructs provided by TensorRight DSL to write tensor expressions and preconditions.
We use the notation LHS ⇒𝐶 RHS to represent a generic tensor graph rewrite, where LHS and
RHS are tensor expressions and 𝐶 is the precondition under which the rewrite rule is supposedly
correct, which is verified by our system.
  Example. Consider the DysliceToSlice rule shown in Equation 2, extracted from XLA’s algebraic
simplifier, which desugars the dy-slice operator to the more efficient slice operator.
                          dy-slice(Y, 𝐵, 𝐿) =⇒𝐸−𝐵 ′ =𝐿 ∧ 𝑃 =1 ∧ 𝐵 ′ =𝐵 slice(Y, 𝐵 ′, 𝐸, 𝑃)                      (2)
 Fig. 4 depicts the DysliceToSlice rule visually. The dy-slice operator extracts a sub-tensor from
the input tensor Y, where the start-index for each axis is specified in 𝐵 and the length of the slice
along each axis is passed in 𝐿. Meanwhile, the slice operator also extracts a sub-tensor from within a
bounding box in the input tensor Y. The start-indices for the bounding box are specified in 𝐵 ′ , while
the end-indices (exclusive) are specified in 𝐸. 𝑃 specifies the stride for each axis, which determines
the step size between elements in the bounding box.
   The DysliceToSlice rule is generally not cor-                                                  end
rect, unless 𝐸 − 𝐵 ′ (the size of the bounding box      start         length            start       stride
in slice) is equal to 𝐿 (the length in dy-slice). The
other requirements are that slice should skip no
elements, i.e., 𝑃 = 1, and the start indices in slice
and dy-slice must be the same, i.e., 𝐵 ′ = 𝐵. Since
these are specified in the precondition, the RHS
expression is equivalent to the LHS expression.
Our goal is to represent and verify this rule for
arbitrary tensors and operator attributes. We now          dy-slice(start, length)        slice(start, end, stride)

discuss each challenge individually and explain
how our system addresses them.                        Fig. 4. Illustration of dy-slice and slice operators. The
                                                              shaded regions denote the operator outputs.
3.2     Representation in TensorRight DSL
   Challenges in representation. First, since the DysliceToSlice rule should be correct for all instan-
tiations of the tensor Y, our system should allow representing a tensor of arbitrary rank and size.
Second, it should allow specifying arbitrary operator attributes like start, end, stride, and length,
to ensure that the rule is correct for all possible operator attributes. It should also allow performing
operations on attributes, like doing arithmetic on end and start while specifying the precondition.
Third, the operators provided by the system should model those that are found in XLA-HLO. Last, it
should allow defining preconditions on a rule (e.g., stride values being 1).
  TensorRight Frontend. We present a frontend language in which users can express abstract
rewrite rules along with preconditions. TensorRight will build internal representations (§4) of
rewrite rules from the specification, which can be instantiated to arbitrary ranks.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                                                      29:9

  1   rule = do
  2       rcls <- newRClass "rcls"
  3       [size, start, start', length, end, stride] <-
  4           newMaps ["size", "start", "start'", "length", "end", "stride"] rcls
  5       Y <- newTensor @TensorInt "Y" [rcls --> size]
  6       lhs <- dynamicSlice Y [rcls --> start] [rcls --> length]
  7       rhs <- slice Y [rcls --> start'] [rcls --> end] [rcls --> stride]
  8       precondition [end, start', length] $ \[end, start', length] -> end - start' .== length
  9       precondition [stride] $ \[stride] -> stride .== 1
 10       precondition [start, start'] $ \[start, start'] -> start' .== start
 11       rewrite "DynamicSlice(Y) => Slice(Y)" lhs rhs
 12
 13   verifyDSL rule
                            Listing 1. The DysliceToSlice rule represented in TensorRight DSL.


   Listing 1 illustrates the DysliceToSlice rule implemented in the TensorRight Frontend. Instead
of using fixed-rank tensors, the tensors in TensorRight DSL are represented with aggregated-axes,
that can be instantiated to any number of axes. All axes in an aggregated-axis share the same “role”
and are treated uniformly by all the operators, allowing us to reason about an unbounded number
of axes compactly. There might be multiple aggregated-axes in a rule to capture different roles of
axes. Some of them must be instantiated to the same rank in a correct rule and this constraint is
represented by a rank class (RClass) as discussed in §6.
   On line 2 in Listing 1, we declare a new RClass and we refer to it by rcls. In TensorRight DSL, we
can refer to the aggregated-axis with the RClass itself, if an RClass has exactly one aggregated-axis.
On lines 3-4, we declare multiple abstract-maps on rcls. These abstract-maps can be instantiated
to concrete-maps, whose domain is the same as the axes in the aggregated-axis represented by rcls.
When instantiated, they map axes in rcls to symbolic values, which can represent axes sizes, start
indices, end indices etc. On line 5, we declare a new tensor containing integer elements, with the
shape {rcls ↦→ size}. Similarly, the created tensor can also be instantiated with any number of
axes (all of which behave in the same way) and symbolic sizes. We then construct the LHS and RHS
expressions on lines 6 and 7, respectively. On line 8, we specify the precondition that the difference
of the end and start indices should be equal to the length. On line 9, we specify that the stride
values should be 1 for all axes. On line 10, we specify that the start indices should be same on both
sides. Finally, we construct the rewrite rule on line 11.
   This example demonstrates how we can represent tensors with arbitrary rank and sizes, specify
arbitrary operator attributes, construct tensor expressions, and specify complex preconditions in
TensorRight DSL. We now discuss our verification methodology built on top of this representation.

3.3    Verification


                 Frontend                         Analysis                                  Bounded Verification
                                                                                      Instance0
                                                Aggregated
                                                                                   {rclass0: 1, ...}
                                               Representation                                             Symbolic
                                                                                                         Evaluation                 Induction
  Rewrite Rules in                                                                    Instance1                           All
    TensorRight
                      Type/RClass Check                            Instantiation
                                                                                   {rclass0: 1, ...}                    Verified?
                                                                                                                                                Valid
                                                                                                         SMT-based
                                               Bound Inference                                           Verification
                                               {rclass0: 3, ...}                      Instance2
                                                                                   {rclass0: 2, ...}
                                                                                                                        Invalid



                                           Fig. 5. TensorRight Overview and Workflow.


                                          Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:10                                                                                         Arora et al.


   Fig. 5 describes our approach to verifying rules with tensors of arbitrary rank and sizes. With the
aggregated representation created in §3.2, the system infers a bound for each RClass and instantiates
them to all the ranks within the bound. Each instance can then be proven with symbolic evaluation
by SMT solvers. This is based on a crucial theorem (§6.3) that for all RClasses in a rule, there exists
a mechanically derivable bound on the ranks, such that proving all instances within the bound
implies that the rule is correct for all ranks. With this bound, we convert the unbounded-verification
proof obligation to a finite number of bounded-verification proof obligations. The correctness of the
rule with ranks beyond the bound is then established with induction.
   On line 13 in Listing 1, we call
verifyDSL on the constructed rule,           1 ruleLowered = do
which is our main verification rou-          2       # Instiate rcls to a concrete set
tine. First, it infers a bound for every     3        ○S <- rcls
RClass in the rule. The bound infer-         4       #  Define concrete maps on rcls
ence algorithm collects the number           5       size  <- Map ○S SymInteger
of unique boolean conditions and ten-        6       #  Maps for other attributes like start, length
                                             7       Y <- newTensor @TensorInt "tensor" [rcls --> size]
sor accesses in the rewrite rule. In         8       lhsSym <- [[...]] # Symbolic Representation of LHS
this case, there is only one RClass,         9       rhsSym <- [[...]] # Symbolic Representation of RHS
no boolean conditions, and a single 10               pre <- ... # Precondition of the rule
unique access to the tensor. We infer 11             # Axes and Shape Checks
the bound to be 1. This means that if       12       assert $ lhsShape .== rhsShape
                                            13       A <- generalAccess(lhs, rhs)
the rule is correct for all rank-1 ten- 14           verify $ pre && lhsValid -> lhsSym[A] .== rhsSym[A]
sors, then the rule is correct for ten-
                                             Listing 2. Frontend Rewrite Rule lowered to our core syntax.
sors containing any number of axes.
We discuss these conditions and ac-
cesses in detail in §6.
   Second, it specializes the rule for these ranks, ending up with fixed-rank but arbitrary-sized
tensors. Listing 2 shows some details of the lowered code in our core TensorRight DSL. On line 3,
we instantiate rcls with a known-rank (1 in this case) and get the set of concrete-axes in ○.   S On line
5, we declare concrete-maps corresponding to the abstract maps in Listing 1. These maps now have
a concrete-domain, same as ○.     S In lines 7-10, we create concrete-ranked input tensors, generate
symbolic representations of LHS and RHS with symbolic evaluation, and specify preconditions.
We make an initial assertion on line 12 that both expressions have the same symbolic shape. One
line 14, we express one of the main verification conditions, i.e., the equality between LHS and RHS
expressions under a general access A, which is discharged to an SMT solver. The solver decides
that the proof obligation is a tautology and the rule is deemed verified in the unbounded setting.
   The example demonstrates how we take the abstract specification of a rewrite rule expressed
in TensorRight Frontend, infer a bound for each RClass, instantiate every aggregated-axis, and
discharge bounded-verification proof obligations. We describe the TensorRight DSL in §4, the
denotational semantics in §5, and our verification methodology in detail in §6.

4   Rewrite Rule Representation
In this section, we show our rank- and size-polymorphic rewrite rule representation constructed
by the TensorRight Frontend introduced in §3.2. We take a set of operators from XLA-HLO and
model them in TensorRight. We show a subset of the modeled operators in Fig. 6 for discussion
(more modeled operators can be found in §A). We can extend the set to other layout-insensitive
operators, whose semantics do not depend on the particular physical layout of the operands. Some
operators that do not fall into this category include reshape and bitcast.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                      29:11


   The key distinction of our DSL from XLA-HLO is that we group axes into aggregated-axes, where
all the axes in the same group share the same “role” and are treated uniformly by the operators.
This allows us to describe rewrite rules with tensors containing any number of axes in a compact
manner. In §6, we extend this representation by tagging the aggregated-axes with rank classes to
help us with the instantiation of aggregated-axes into concrete-axes for verification purposes.

4.1     Named Axes
Following named-tensors in Py-
Torch [13] and named-axes 𝜏                 ≔ Int | Bool | Real                    Type
in JAX [4], we give explicit      𝑎         ∈   A                                  Named-axes
names to the axes of a tensor 𝑥             ∈ X = P (A)                            Aggregated-axes
and call them named-axes. We      𝑓         ∈   list[Int]   →    Int               Map  function
can treat the named-axes of       𝑚         ≔   M     | fmap(𝑓     , 𝑚+)           Maps
a tensor as an unordered set 𝑋              ∈ P (X)                                Set of aggregated-axes
                                            ∈      X                               Shapes and indices
for layout-insensitive operators  𝑆, 𝐼          𝑚
                                            ∈   X   X                              Relabel maps
and express tensor shapes as      𝑅
mappings from names to sizes.     𝑣         ≔   𝑖 : Int  | 𝑏 : Bool     | 𝑟 : Real Scalar literal
For example, we may give the      𝑒         ≔   T   (Literal)                      Tensor  expression
names ℎ and 𝑣 to the horizontal             |   V (Variable)
and vertical axes respectively              |   const(𝑣, 𝑆)
of a 2 × 3 tensor 𝑡 and the shape           |   iota(𝑆, 𝑥)
of this tensor would be the map-            |   expand(𝑒, 𝑆)
ping {ℎ ↦→ 3, 𝑣 ↦→ 2}. Such                 |   binary(⊕, 𝑒𝑙 , 𝑒𝑟 )
a tensor can be accessed with               |   pad(𝑒, 𝑣, 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 )
an access map, which is a map-              |   slice(𝑒, 𝐼𝑠 , 𝐼𝑒 , 𝐼𝑝 )
ping from named-axes to in-                 |   dy-slice(𝑒, 𝐼, 𝑆)
dices. We then have 𝑡 [{ℎ ↦→                |   dyup-slice(𝑒, 𝑒𝑢 , 𝐼 )
1, 𝑣 ↦→ 1}] = 𝑤, given the                  |   reduce(⊕, 𝑒, 𝑋 )
domain of the access map is                 |   relabel(𝑒, 𝑅)
exactly the set of the named-               |   concat(𝑒𝑙 , 𝑒ℎ , 𝑥)
axes, there’s no out-of-bounds 𝑔            ∈ list[Int] → Bool                     Predicate function
access, and 𝑤 is the value at 𝑃             ≔ fold(𝑔, 𝑚+)                          Precondition
that access.                      𝑅𝑢𝑙𝑒 ≔ 𝑒𝑙ℎ𝑠 ⇒𝑃∗ 𝑒𝑟ℎ𝑠                             Rewrite rule
    An operator that works on
multiple tensors will need to        Fig. 6. Core rewrite rule representation with selected operators.
match them by the named-axes, as shown in the following examples.
      • binary(+, 𝑡 1, 𝑡 2 ), where 𝑡 1 , 𝑡 2 have the shapes {𝑎 1 ↦→ 2, 𝑎 2 ↦→ 3} and {𝑎 1 ↦→ 2, 𝑎 2 ↦→ 3}, respec-
        tively. The two shapes match as they have the same set of named-axes and the corresponding
        named-axes have the same sizes.
      • dot(𝑡 1, 𝑡 2, {𝑎 2, 𝑎 3 }, {𝑎 4 }), where the shapes of 𝑡 1 and 𝑡 2 are {𝑎 1 ↦→ 2, 𝑎 2 ↦→ 3, 𝑎 3 ↦→ 4, 𝑎 4 ↦→ 5}
        and {𝑎 5 ↦→ 6, 𝑎 2 ↦→ 3, 𝑎 3 ↦→ 4, 𝑎 4 ↦→ 5}, respectively. For the dot operator, we need to match
        the contraction and batch axes, in this case {𝑎 2, 𝑎 3 } and {𝑎 4 }, respectively. The resulting
        tensor has the shape {𝑎 1 ↦→ 2, 𝑎 4 ↦→ 5, 𝑎 5 ↦→ 6}.
  Note that sometimes, we need to rename the axes to avoid name clashes. For example, with the
dot operator, if the two tensors share some spatial named-axes (neither contraction nor batch axes),
we need to rename them before applying the operator to make sure that the named-axes in the
resulting tensor are unique.

                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:12                                                                                                Arora et al.


4.2     Aggregated Axes
As we’ve shown in the dot example in §4.1, we have matched some set of axes between the two
tensors. This partitions the named-axes in a tensor into sets of axes that have the same “role” in
the expression. For example, 𝑎 2 and 𝑎 3 have the same roles as contraction axes. Based on this
observation, we introduce aggregated-axes, which is a set of named-axes.
   We can partition the set of named-axes of a tensor into disjoint aggregated-axes and write
expressions directly using uninterpreted aggregated-axes. The aggregated-axes can be instantiated
to some concrete set of named-axes, and the number of instantiated named-axes is called the rank
of an aggregated-axis. This allows us to write expressions with an arbitrary number of named-axes
in a uniform and simple way.
   For example, in the expression dot(𝑡 1, 𝑡 2, {𝑥 2, 𝑥 3 }, {𝑥 4 }), if we assume that the set of named-axes
in 𝑡 1 and 𝑡 2 are 𝑥 1 ∪ 𝑥 2 ∪ 𝑥 3 ∪ 𝑥 4 and 𝑥 5 ∪ 𝑥 2 ∪ 𝑥 3 ∪ 𝑥 4 , respectively, then the resulting tensor has
{𝑥 1, 𝑥 4, 𝑥 5 } as the set of aggregated-axes. It’s easy to see that we can get back the dot example shown
in §4.1 by instantiating all aggregated-axes to singleton sets. This instantiation is not arbitrary, and
we elaborate on how to specify the constraints on the instantiations with rank classes in §6.
   We can then lift the tensor semantics to aggregated semantics: shapes or indices can be expressed
with, or instantiated from aggregated-axes. Instead of being a mapping from named-axes to integers,
we now need a nested mapping that maps aggregated-axes to another map from names in the
aggregated-axes to integers. As a convention, we will refer to the inner mappings as a map and the
outer mapping as an aggregated-map. For example, the following is valid aggregated-map:
                               {{𝑖 1, 𝑖 2 } ↦→ {𝑖 1 ↦→ 2, 𝑖 2 ↦→ 3}, {𝑖 3 } ↦→ {𝑖 3 ↦→ 4}}
Definition 1. An aggregated-map 𝑀 is valid if it is a nested mapping from aggregated-axes to
maps from named-axes to integers such that:
   • ∀𝑥 1, 𝑥 2 ∈ dom(𝑀), 𝑥 1 ≠ 𝑥 2 → 𝑥 1 ∩ 𝑥 2 = ∅, and
   • ∀𝑥 ∈ dom(𝑀), dom(𝑀 [𝑥]) = 𝑥.
  Note that 𝑀 [𝑥] represents the value mapped to 𝑥 in 𝑀. Shape and indices are aliases for
aggregated-maps in specific contexts and they have their additional validity conditions, depending
on the context. Here, we give the validity conditions for tensor shapes and access indices:
Definition 2. A valid tensor shape 𝑆 is a valid aggregated-map, such that ∀𝑥 ∈ dom(𝑆), ∀𝑎 ∈
𝑥, 𝑆 [𝑥] [𝑎] ≥ 0. The shape of a tensor 𝑡 is denoted as Shape(𝑡).
Definition 3. A valid access 𝐴 (used for accessing tensors) with respect to a valid tensor shape 𝑆,
is a valid aggregated-map such that
     • dom(𝐴) = dom(𝑆), and
     • ∀𝑥 ∈ dom(𝐴), ∀𝑎 ∈ 𝑥, 0 ≤ 𝐴[𝑥] [𝑎] < 𝑆 [𝑥] [𝑎].
The set of all valid accesses given a tensor shape 𝑆, is denoted by Access(𝑆). A tensor 𝑡 is then
viewed as a mapping from the set Access(Shape(𝑡)) to elements, and the element at the access 𝐴 is
denoted as 𝑡 [𝐴]. The set of all aggregated-axes of a tensor 𝑡 is denoted as Axes(𝑡).
     Operator attributes are also expressed using aggregated-maps, with each operator having its own
validity conditions. For example, the pseudo operator pad-low, which only does low-padding, can
pad a tensor with 𝑙 1 , followed by 𝑙 2 , for the axes in 𝑥 1 using the expression: pad-low(pad-low(𝑡, {𝑥 1 ↦→
𝑙 1 }), {𝑥 1 ↦→ 𝑙 2 }). The validity condition for pad-low allows padding with negative shapes but disal-
lows creating a tensor with a negative shape (more details in §5). Assuming 𝑡 has the shape 𝑠 0 in the
aggregated-axis 𝑥 1 , the resulting shape in the pad-low expression will be 𝑠 0 + 𝑙 1 + 𝑙 2 . Note that we
are doing an element-wise combination of maps, where the maps must have the same named-axes

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                      29:13


and the resulting map contains the sum of the corresponding axis sizes. Element-wise combination
(fmap) is the only allowed operation on the maps to combine them, as we define aggregated-axes
as set of named axes that have the same “role” in the expression. Note that we may also combine a
map with scalars by lifting the scalar to a constant map.

4.3    Rewrite Rule
Similar to many other tensor graph rewrite systems, TensorRight models rewrite rules as rewriting
an LHS expression to an RHS expression, subject to certain preconditions. See the following example:
      pad-low(pad-low(𝑡, 0, {𝑥 1 ↦→ 𝑙 1 }), 0, {𝑥 1 ↦→ 𝑙 2 }) ⇒𝑙1 ≥0 ∧ 𝑙2 ≥0 pad-low(𝑡, 0, {𝑥 1 ↦→ 𝑙 1 + 𝑙 2 })
In this rule, we aggregated all the named-axes in the tensor 𝑡 into the aggregated-axis 𝑥 1 . 𝑙 1 and 𝑙 2
are two maps from named-axes in 𝑥 1 to padding sizes. In the RHS, the two maps are combined in
an element-wise way. Similarly, our preconditions are predicates lifted to operate on the maps in
an element-wise way. The condition 𝑙 1 ≥ 0 here means that the padding sizes in 𝑙 1 must be greater
than or equal to 0 for all named-axes.

5     Denotational Semantics
We give the denotational semantics of the XLA-HLO operators in Fig. 7. We will use denotational
semantics notations for deriving a bound on the ranks, but note that since our semantics map from
our language to computable tensor objects, we can easily derive a big-step operational semantics
and perform symbolic evaluation. Due to space limitations, we will only show the semantics of
some selected operators. More operators are available in §A. They are usually simple or can be
expressed using existing operators or the techniques introduced here.
   The domain of our denotational semantics are tensors, which map accesses to elements. The
elements can be boolean, integers, or real numbers. There is also a special type of element called a
Reduction Element, denoted as Red𝐼⊕0,𝐼1,··· 𝑓 ({dom(𝐼 0 ) ↦→ 𝐼 0, dom(𝐼 1 ) ↦→ 𝐼 1, · · · }). Here, ⊕ is a binary
operator and 𝐼 0, 𝐼 1, · · · are called reduction indices. We may sometimes omit the indices and write
Red𝑋⊕ 𝑓 (𝑋 ), where 𝑋 = {dom(𝐼 0 ), dom(𝐼 1 ), · · · } is the set of aggregated-axes being reduced.
   The introduction of a reduction element is based on pragmatic reasons. As the sizes of reduced
axes are unbounded, we cannot expand the reduction to sum all the values being reduced. Thus, we
leave the sum uninterpreted and provide special treatment for such elements during verification.
   Fig. 7 shows the denotational semantics of some selected operators. We overload some functions
for convenience: Shape(𝑒) means Shape(⟦𝑒⟧), Access(𝑒) means Access(Shape(𝑒)), and Axes(𝑒)
means Axes(⟦𝑒⟧). We also introduce some helper functions on valid aggregated-maps. Given a
comparison operator ⊙ and a binary operator ⊕, we lift them to aggregated-maps as
                                               Û Û
                                𝑀1 ⊙ 𝑀2 =                  𝑀1 [𝑥] [𝑎] ⊙ 𝑀2 [𝑥] [𝑎]
                                            𝑥 ∈dom(𝑀1 ) 𝑎∈𝑥
             𝑀1 ⊕ 𝑀2 = {𝑥 ↦→ {𝑎 ↦→ 𝑀1 [𝑥] [𝑎] ⊕ 𝑀2 [𝑥] [𝑎] | 𝑎 ∈ 𝑀1 [𝑥]} | 𝑥 ∈ dom(𝑀1 )}
  All these binary operations implicitly introduce the assumption that the two aggregated-maps
are valid and the domain of the two aggregated-maps are the same. We will omit these from our
rules. Sometimes, we may overload the notations to operate with constants. This is treated as
operating with a nested map where the inner map are constant maps.
  In our rules, we introduce bindings with let 𝑛𝑎𝑚𝑒 = · · · notation. Some rules like Iota and
Concat require that an aggregated-axis is singleton. In these rules, we use the syntax let {𝑎} = 𝑥 to
say that 𝑥 is singleton and bind the singleton element in 𝑥 to 𝑎. We use the notation 𝑆 |𝐾 to denote
the mapping restriction of 𝑆 to 𝐾, where 𝑆 is any map and 𝐾 is a subset of keys from 𝑆.

                                Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:14                                                                                                                        Arora et al.

                                                                                             Const
                                      ⟦const(𝑣, 𝑆 )⟧ = {𝐴 ↦→ 𝑣 | 𝐴 ∈ Access(𝑆 ) }

                                                 let {𝑎} = 𝑥      𝑥 ∈ dom(𝑆 )
                                                                                                  Iota
                                    ⟦iota(𝑆, 𝑥 )⟧ = {𝐴 ↦→ 𝐴[𝑥 ] [𝑎] | 𝐴 ∈ Access(𝑆 ) }

                                                 dom(𝑆 ) ∩ Axes(𝑒 ) = ∅
                                                                                                            Expand
                    ⟦expand(𝑒, 𝑆 )⟧ = {𝐴 ↦→ ⟦𝑒⟧ [𝐴| Axes(𝑒 ) ] | 𝐴 ∈ Access(Shape(𝑒 ) ∪ 𝑆 ) }

                                                  Shape(𝑒 ) = Shape(𝑒 ′ )
                                                                                                           BinOp
                          ⟦binary(⊕, 𝑒, 𝑒 ′ )⟧ = {𝐴 ↦→ ⟦𝑒⟧ [𝐴] ⊕ ⟦𝑒 ′ ⟧ [𝐴] | 𝐴 ∈ Access(𝑒 ) }

                     let 𝑆 = Shape(𝑒 )         let 𝑆 ′ = 𝑆 + 𝑆𝑙 ≥ 0      let 𝑛𝑜𝑡 -𝑝𝑎𝑑 = 𝜆𝐴.𝐴 ≥ 𝑆𝑙
                                                                                                                        PadLow
           ⟦pad-low(𝑒, 𝑣, 𝑆𝑙 )⟧ = {𝐴 ↦→ if 𝑛𝑜𝑡 -𝑝𝑎𝑑 (𝐴) then ⟦𝑒⟧ [𝐴 − 𝑆𝑙 ] else 𝑣 | 𝐴 ∈ Access(𝑆 ′ ) }

                                                0 ≤ 𝐼𝑠 ≤ 𝐼𝑒 ≤ Shape(𝑒 )    𝐼𝑝 > 0
                                                                                       l       m              Slice
                         slice(𝑒, 𝐼𝑠 , 𝐼𝑒 , 𝐼𝑝 ) = {𝐴 ↦→ ⟦𝑒⟧ [𝐼𝑠 + 𝐴 × 𝐼𝑝 ] | 𝐴 ∈ Access( 𝐼𝑒𝐼−𝐼
                                                                                             𝑝
                                                                                               𝑠
                                                                                                   )}

                                         𝐼 + 𝑆 ≤ Shape(𝑒 )         𝑆>0        𝐼 ≥0
                                                                                                      DySlice
                              dy-slice(𝑒, 𝐼, 𝑆 ) = {𝐴 ↦→ ⟦𝑒⟧ [𝐴 + 𝐼 ] | 𝐴 ∈ Access(𝑆 ) }

                  let 𝑆𝑢 = Shape(𝑒𝑢 )     𝐼 + 𝑆𝑢 ≤ Shape(𝑒 )     𝑆𝑢 > 0        𝐼 ≥0
                 let 𝑎𝑐𝑐 = 𝜆𝐴.if 𝐴 ≥ 𝐼 ∧ 𝐴 < 𝐼 + 𝑆𝑢 then ⟦𝑒𝑢 ⟧ [𝐴 − 𝐼 ] else ⟦𝑒⟧ [𝐴]
                                                                                                        DyUpdateSlice
                          dyup-slice(𝑒, 𝑒𝑢 , 𝐼 ) = {𝐴 ↦→ 𝑎𝑐𝑐 (𝐴) | 𝐴 ∈ Access(𝑒 ) }

                              let 𝑆 = Shape(𝑒 )           let {𝑥 0 · · · 𝑥𝑘 } = 𝑋 ⊆ Axes(𝑒 )
                            let 𝑎𝑐𝑐 = 𝜆𝐴.Red𝐼⊕0 ,··· ,𝐼 ⟦𝑒⟧ [ {𝑥 0 ↦→ 𝐼 0 , · · · , 𝑥𝑘 ↦→ 𝐼𝑘 } ∪ 𝐴]
                                                      𝑘
                                                                                                        Reduce
                            ⟦reduce(⊕, 𝑒, 𝑋 )⟧ = {𝐴 ↦→ 𝑎𝑐𝑐 (𝐴) | 𝐴 ∈ Access(𝑆 \ 𝑆 |𝑋 ) }

                     ∀𝑥 1 , 𝑥 2 ∈ dom(𝑅), 𝑥 1 ≠ 𝑥 2 → 𝑅 [𝑥 1 ] ≠ 𝑅 [𝑥 2 ]        dom(𝑅) = Axes(𝑒 )
                                                                                                           Relabel
                           ⟦relabel(𝑒, 𝑅)⟧ = {𝐴 ↦→ ⟦𝑒⟧ [𝐴 ◦ 𝑅 ] | 𝐴 ∈ Access(𝑆 ◦ 𝑅 −1 ) }

            let {𝑎} = 𝑥     𝑥 ∈ Axes(𝑒 )       𝑥 ∈ Axes(𝑒 ′ )     let 𝑆 = Shape(𝑒 )         let 𝑆 ′ = Shape(𝑒 ′ )
                                      ∀𝑥 ′ ∈ Axes(𝑒 ), 𝑥 ′ ≠ 𝑥 → 𝑆 [𝑥 ′ ] = 𝑆 ′ [𝑥 ′ ]
                let 𝑆 ′′ = {𝑥 ′ ↦→ if 𝑥 ′ = 𝑥 then 𝑆 ′ [𝑥 ] else {𝑎 ′ ↦→ 0 | 𝑎 ′ ∈ 𝑥 ′ } | 𝑥 ′ ∈ Axes(𝑒 ) }
                            let 𝑎𝑐𝑐 = 𝜆𝐴.if 𝐴 ≥ 𝑆 ′′ then ⟦𝑒 ′ ⟧ [𝐴 − 𝑆 ′′ ] else ⟦𝑒⟧ [𝐴]
                                                                                                                        Concat
                              concat(𝑒, 𝑒 ′ , 𝑥 ) = {𝐴 ↦→ 𝑎𝑐𝑐 (𝐴) | 𝐴 ∈ Access(𝑆 + 𝑆 ′′ ) }


                                Fig. 7. Denotational Semantics of some core operators.


   Tensor operators. Next, we explain the semantics of some select operators:
    • Const: The const operator outputs a tensor with the desired shape 𝑆, with all accesses being
      mapped to the same constant element 𝑣.
    • Iota: The iota operator projects the access-index for a specific singleton aggregated-axis 𝑥.
      The resulting tensor holds values starting at 0, incrementing by 1 along that axis.
    • Expand: The expand operator introduces new aggregated-axes to a tensor by duplicating
      the data in the tensor. It takes a shape containing the sizes of the new axes and the resulting
      tensor is accessed as if we are accessing the input tensor after removing these new axes from
      the access. The set of new axes must be disjoint from the original set of axes.
      Fig. 8a demonstrates the expand operator with an example. The input tensor contains two
      aggregated-axes 𝑥ℎ and 𝑥 𝑤 , each instantiated with 1 named-axes. We refer to the correspond-
      ing named-axes by ℎ and 𝑤, respectively. The input shape is {{ℎ} ↦→ {ℎ ↦→ 5}, {𝑤 } ↦→
      {𝑤 ↦→ 5}}. We expand it by adding a new aggregated-axis 𝑥𝑑 , containing 1 named-axis

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:15


      𝑑. The resulting tensor duplicates data across this new named-axis and has a shape of
      {{ℎ} ↦→ {ℎ ↦→ 5}, {𝑤 } ↦→ {𝑤 ↦→ 5}, {𝑑 } ↦→ {𝑑 ↦→ 3}}.
    • BinOp: The binary operator performs an element-wise operation on two identically-shaped
      tensors.
    • PadLow: We present a restricted version of the pad operator, pad-low, which pads only on
      the low-ends of each axis. The semantics test whether the access is in the padded region. If
      so, return the padded value, or access the original tensor, offset by the padding shape.
      Fig. 8b demonstrates the pad-low operator with an example. The input tensor contains two
      aggregated-axes 𝑥ℎ and 𝑥 𝑤 , each instantiated with 1 named-axes. We refer to the correspond-
      ing named-axes by ℎ and 𝑤, respectively. The input shape is {{ℎ} ↦→ {ℎ ↦→ 4}, {𝑤 } ↦→ {𝑤 ↦→
      4}}. We perform zero-padding on ℎ and 𝑤 with padding attributes of 2 and 1 respectively.
      The zero-padding values are all present at the lower-ends of the axes. The resulting tensor a
      shape of {{ℎ} ↦→ {ℎ ↦→ 6}, {𝑤 } ↦→ {𝑤 ↦→ 5}}.
    • Slice: The slice operator extracts a sub-tensor, which has the same named-axes as the input
      tensor and contains the values inside a bounding box within the input. The indices for the
      bounding box are given by the starting indices 𝐼𝑠 , limit indices 𝐼𝑒 (exclusive), and the positive
      strides 𝐼𝑝 . The slice picks every 𝐼𝑝 [𝑥] [𝑎] element along each named-axis 𝑎 ∈ 𝑥 ∈ dom(𝐼𝑝 ).
    • DySlice: The dy-slice operator extracts a sub-tensor from the input tensor. The indices for
      the bounding box are given by the starting indices 𝐼 and size of the bounding box 𝑆. The sizes
      must be positive and should not cause out-of-bounds accesses. Note that this is different from
      the XLA semantics, where our starting indices are not represented as a tensor, but as a map.
      We are then only able to express rewriting rules where the indices are used in an opaque
      way, or as a constant, or computed with element-wise operations, e.g., binary. We found that
      this change does not affect the effectiveness of TensorRight for verification purposes, and
      our approximation is able to express all rewrite rules involving dy-slice.
    • DyUpdateSlice: The dyup-slice operator generates a result with a slice overwritten by 𝑒𝑢 ,
      starting at indices 𝐼 . Our dyup-slice operator follows the same approximation as dy-slice.
    • Reduce: The reduce operator takes a tensor and a set of aggregated-axes 𝑋 as inputs, then
      returns a tensor mapping to uninterpreted reduction elements as the result. The resulting
      tensor has the shape 𝑆 \ 𝑆 |𝑋 , essentially removing all the aggregated-axes in 𝑋 . We extend
      the semantics of reduce to make verification easier in §A.
    • Relabel: In TensorRight, as we take an unordered view of the axes, we no longer need
      transpose. However, we still need to re-match the axes, for example, when we want to describe
      some expressions such as 𝑡 + transpose(𝑡). The relabel operator is introduced for this axes-
      matching operation. It renames aggregated-axes and does not change tensor contents.
    • Concat: The concat operator is another example where we introduce the singleton constraint
      on an aggregated-axis. The two tensors should have the same shape on other axes. For the
      concatenating axis, the resulting size will be the sum of the operand sizes. The resulting
      tensor will then compute which operand tensor the access belongs to and perform the access.

  Handling reduction elements. In real-world XLA rewrite rules, the reduction might not always
be the top-level operation and a reduction of a tensor may be performed in several steps. For
instance, in the rewrite rule reduce(concat(reduce(A), reduce(B))) = reduce(concat(A, B)), the
reduction in LHS is done in two steps. To handle rules like this, we provide a limited set of arithmetic
rules for reduction elements in Fig. 9. If no known rule applies, TensorRight will report an error,
indicating that the rule isn’t supported. The equivalence of two reduction elements is currently
verified by a stronger condition, where we view them as sets and verify that there is a one-one
mapping between them. Note that not all correct rules meet the strengthened condition, but we

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:16                                                                                                            Arora et al.


                                                                       w                             0   0   0      0    0
             w

                                                                                                     0   0   0      0    0

                                                                                                     0
                          expand                              h                       pad-low
h                                                                                                    0
                         {d → 3}                                                 0, {h → 2, w → 1}
                                                                                                     0

                                                                                                     0

                                   d
                                                            (b) pad-low: {ℎ ↦→ 2, 𝑤 ↦→ 1} denotes the padding
    (a) expand: {𝑑 → 3} denotes the expansion shape             attributes and 0 denotes the padding value
           Fig. 8. Illustration of (a) expand and (b) pad-low operators. ℎ, 𝑤, and 𝑑 denote named-axes.

find that it covers most rewrite rules with reductions. Additionally, user-provided hints are needed
for verifying the set equivalence, as discussed in §6.5. This is the only manual hint from the user
during our verification. Providing better mechanisms for handling reductions is a future work.

         𝑣 ∗ Red𝑋+ 𝑓 (𝑋 ) → Red𝑋+ 𝑣 ∗ 𝑓 (𝑋 )             Red𝑋+ 𝑓 (𝑋 ) ∗ Red𝑌+ 𝑔(𝑌 ) → Red𝑋+ ,𝑌 𝑓 (𝑋 ) ∗ 𝑔(𝑌 )
                                       Red𝑋⊕ (Red𝑌⊕ 𝑓 (𝑋, 𝑌 )) → Red𝑋⊕ ,𝑌 𝑓 (𝑋, 𝑌 )

                                          Fig. 9. Rules on reduction elements.

6       Verification of Rewrite Rules
After defining the representation of rewrite rules in §4 and its denotational semantics in §5, this
section describes how TensorRight verifies the rewrite rules given the semantics. We will first
overview our verification approach, which is based on 𝑘-induction [36], then provide proof sketches
for our induction steps.

6.1      Overview of the Verification
To prove that a rewrite rule is correct, intuitively, we need to verify that the two expressions have
the same denotation, possibly under some assumptions. Given a rule LHS ⇒𝐶 RHS, we prove that
                            ∀𝑣 ∈ 𝑣𝑎𝑟𝑠, 𝐶 ∧ valid-expr(LHS) → ⟦LHS⟧ = ⟦RHS⟧                                               (3)
Here, 𝑣𝑎𝑟𝑠 is the set of all variables appearing in the rule. It contains all possible tensor variables
and operator attributes, such as slice attributes and expand shapes. Note that we only consider the
case where the term prior to rewriting is valid, i.e., when LHS is valid.
   The challenge here is that a rewrite rule can usually be applied to tensors with arbitrary number
of axes and arbitrary sizes in each axis. To handle arbitrary number of axes, as discussed in §4, we
express rewrite rules with a finite number of aggregated-axes and each of them may be instantiated
to arbitrary ranks. The equivalence of the two expressions then boils down to verifying that they
are equivalent under all valid instantiations 𝐼 , where the LHS is valid:
 Û
    valid(𝐼 ) where valid(𝐼 ) = ∀𝑣 ∈ 𝑣𝑎𝑟𝑠 (𝐼 ), 𝐶 ∧ valid-expr(LHS(𝐼 )) → ⟦LHS(𝐼 )⟧ = ⟦RHS(𝐼 )⟧
    𝐼
   For a given instantiation, we now have concrete ranks but unbounded sizes. To handle arbitrary
sizes, we model each tensor as an uninterpreted function and use unbounded integers to model
the indices and sizes in each named-axis. This is supported natively by SMT solvers with good
performance. We then leverage a symbolic execution approach to convert the rewrite rule into a
set of constraints. We call this a bounded-verification proof obligation, which is used to verify a
given instantiation of our rewrite rule. This is described in detail in §6.4.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:17


   We still need to answer two questions: (1) what does it mean for an instantiation to be valid
and (2) how to verify the rule for a possibly infinite number of instantiations? Our approach
to these questions is to introduce a new concept called rank class (RClass). A rank class is a
(required) property of an aggregated-axis, such that all the aggregated-axes with the same RClass
are always instantiated to the same rank. An instantiation of a rewrite rule can then be expressed
as instantiating these RClasses to some rank. We then derive a sufficient rank for each RClass, such
that any instantiation with higher ranks could be proven inductively, given that we have verified
all instances within the rank. This approach follows the 𝑘-induction technique [36].
   To show the intuition for an RClass, consider the rewrite rule (𝐴 + 𝐴⊤ ) ⊤ = 𝐴 + 𝐴⊤ , where 𝑡 has
the shape {𝑥 1 ↦→ 𝑚 1, 𝑥 2 ↦→ 𝑚 2 }. Note that transpose is a no-op with unordered axes semantics,
and relabel is provided for renaming and matching axes.
            relabel(binary(+, 𝑡, relabel(𝑡, {𝑥 1 ↦→ 𝑥 2, 𝑥 2 ↦→ 𝑥 1 })), {𝑥 1 ↦→ 𝑥 2, 𝑥 2 ↦→ 𝑥 1 }) ⇒
                                binary(+, 𝑡, relabel(𝑡, {𝑥 1 ↦→ 𝑥 2, 𝑥 2 ↦→ 𝑥 1 }))
It is easy to see that we must instantiate 𝑥 1 , 𝑥 2 with the same number of axes to make sure that
both LHS and RHS are valid. In other words, 𝑥 1 and 𝑥 2 must have the same rank, in which case we
say that these two aggregated axes are in the same rank class (RClass) and the RClass constraints
the possible instantiations. When we instantiate a rule with relabeling, we also need to be able to
establish a consistent mapping between the named-axes of 𝑥 1 and 𝑥 2 . These facts are expressed in
the following two definitions.
Definition 4. A rank class (RClass) 𝑐 is a property of a family of aggregated-axes, such that
   • Each aggregated-axis 𝑥 is in exactly one RClass 𝑐, written as 𝑥 : 𝑐.
   • For all 𝑥 0 : 𝑐, 𝑥 1 : 𝑐, 𝑥 0 and 𝑥 1 are instantiated to the same rank 𝑟 in a valid instantiation. In
     such an instantiation, the rank of the RClass 𝑐 is defined to be 𝑟 .
Definition 5. An RClass 𝑐 provides a canonical bijection mapping between each pair of the
aggregated axes associated with it. We denote such a mapping that maps from the named axes in
𝑥 0 : 𝑐 to 𝑥 1 : 𝑐, as MapAxes(𝑐, 𝑥 0, 𝑥 1 ). The canonical mapping must satisfy:
      • MapAxes(𝑐, 𝑥 0, 𝑥 1 ) ◦ MapAxes(𝑐, 𝑥 1, 𝑥 0 ) = id, and
      • MapAxes(𝑐, 𝑥 1, 𝑥 2 ) ◦ MapAxes(𝑐, 𝑥 0, 𝑥 1 ) = MapAxes(𝑑, 𝑥 0, 𝑥 2 ).
   where ◦ refers to function composition. Such a mapping can be trivially constructed during
the instantiation as the aggregated axes of the same rank class are instantiated to the same rank.
In practice, without loss of generality, to instantiate an aggregated axis 𝑥𝑖 : 𝑐 to rank 𝑟 , we can
instantiate it to the set of axes 𝑎𝑖,0, · · · , 𝑎𝑖,𝑟 −1 . The canonical mapping between two aggregated axes
𝑥𝑖 : 𝑐 and 𝑥 𝑗 : 𝑐 can then be established as {𝑎𝑖,𝑘 ↦→ 𝑎 𝑗,𝑘 | 𝑘 ∈ {0 · · · 𝑟 − 1}}, and the semantics of
relabel follows this mapping to relabel the instantiated axes.
   We can then reduce our problem to verifying the rule for all possible RClass instantiations:
                                                Û
                                                       valid({𝑐𝑖 ↦→ 𝑟𝑖 })                                (4)
                                            𝑟 1 ,𝑟 2 ,···

where {𝑐𝑖 ↦→ 𝑟𝑖 } is a map containing the ranks for all RClasses 𝑐 1, 𝑐 2, · · · in the rule. valid({𝑐𝑖 ↦→ 𝑟𝑖 })
denotes the proof obligation for a concrete-ranked instance, where the RClass 𝑐𝑖 is instantiated to
rank 𝑟𝑖 , for all 𝑖 ∈ {1 · · · 𝑝}. We still need to verify the rule for all possible ranks of all RClasses.
   Our Approach: To simplify the discussion, let’s assume that the rule only has one aggregated-axis
𝑥, with RClass 𝑐 (i.e., 𝑥 : 𝑐). We can then rewrite Equation 4 as
                                              Û
                                                  valid(𝑖)                                       (5)
                                                            𝑖

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:18                                                                                              Arora et al.


where valid(𝑖) (short for valid({𝑐 ↦→ 𝑖})) is true if and only if the rule is valid when rank of 𝑐 (and
𝑥) is 𝑖. We observe that for every RClass in a rule, there exists a bound corresponding to a sufficient
rank required for unbounded verification, i.e., there exists a rank 𝑘, such that,
                                        ∀𝑖 ≥ 𝑘, valid(𝑖) → valid(𝑖 + 1)                                    (6)
This means that for all 𝑖 ≥ 𝑘, if the rule is valid when 𝑐 has rank 𝑖, then the rule is valid when 𝑐 has
rank 𝑖 + 1. Given such a 𝑘, we can do unbounded verification for the rule using 𝑘-induction:
    • Basis: Use bounded verification to prove that the rule is valid for all ranks until 𝑘:
                                                Û
                                                     valid(𝑖)
                                                   𝑖=1···𝑘
      • Induction case: Use induction on the rank of 𝑐, with Equation 6 as induction hypothesis:
                                                                     Û
                    valid(𝑘) ∧ [∀𝑖 ≥ 𝑘, valid(𝑖) → valid(𝑖 + 1)] ⇒       valid(𝑖)
                                                                                   𝑖 ≥𝑘
This would imply that the rule is correct for an arbitrary number of named-axes in 𝑐. Now what
remains is finding a sufficient rank 𝑘 for any RClass in a rule. We show how to derive such a bound
with the help of an example rewrite rule.

6.2     Bound Computation Example
Consider an input tensor Y which has one aggregated-axis, say 𝑥, having the RClass 𝑐 (i.e. 𝑥 : 𝑐).
The rewrite rule PadLowCombine is shown below:
                  pad-low(pad-low(Y, 0, 𝐿1 ), 0, 𝐿2 ) ⇒𝐿1 ≥0 ∧ 𝐿2 ≥0 pad-low(Y, 0, 𝐿1 + 𝐿2 )               (7)
where 𝐿1 = {𝑥 ↦→ 𝑙 1 } and 𝐿2 = {𝑥 ↦→ 𝑙 2 }, for some maps 𝑙 1 and 𝑙 2 .
  The PadLowCombine rule merges two pad-low operators into a single pad-low operator. The
precondition requires that both padding attributes should be non-negative. For this rule, the
precondition also implies that the LHS expression is valid. The variables appearing in this rule are
the padding attributes 𝐿1, 𝐿2 and the input tensor Y. Using Equation 3, we can express the validity
condition for this rewrite rule as
                              ∀ Y, 𝐿1, 𝐿2, 𝐿1 ≥ 0 ∧ 𝐿2 ≥ 0 → ⟦LHS⟧ = ⟦RHS⟧                                 (8)
  It is easy to see that both LHS and RHS have the same shape, i.e., they have the same domain of
accesses. Thus, we can rewrite ⟦LHS⟧ = ⟦RHS⟧ by interpreting the tensors under a general, valid
access to these tensors. Let 𝐴 ∈ Access(LHS) be an arbitrary access from the domain of the output
tensors. It has the form 𝐴 = {𝑥 ↦→ 𝑎}, where 𝑎 maps named-axes in 𝑥 to (symbolic) indices. We use
the denotational semantics of pad-low described in §5, to symbolically execute these expressions.
                ⟦LHS⟧ = ⟦RHS⟧
            ⇔ ∀𝐴, ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴]
            ⇔ ∀𝐴, ⟦pad-low(pad-low(Y, 0, 𝐿1 ), 0, 𝐿2 )⟧ [𝐴] = ⟦pad-low(Y, 0, 𝐿1 + 𝐿2 )⟧ [𝐴]
            ⇔ ∀𝐴, if 𝐴 ≥ 𝐿2 then (if 𝐴 − 𝐿2 ≥ 𝐿1 then Y[𝐴 − 𝐿1 − 𝐿2 ] else 0) else 0 =
                                 if 𝐴 ≥ 𝐿1 + 𝐿2 then Y[𝐴 − 𝐿1 − 𝐿2 ] else 0
            ⇔ ∀𝑎, if 𝑎 ≥ 𝑙 2 then (if 𝑎 − 𝑙 2 ≥ 𝑙 1 then Y[𝑥 ↦→ 𝑎 − 𝑙 1 − 𝑙 2 ] else 0) else 0 =
                                 if 𝑎 ≥ 𝑙 1 + 𝑙 2 then Y[𝑥 ↦→ 𝑎 − 𝑙 1 − 𝑙 2 ] else 0                       (9)
In the last step, we made use of the fact that the aggregated maps like 𝐴, 𝐿1, 𝐿2 contain only one
aggregated-axis 𝑥. Equation 9 holds for any number of named-axes in 𝑥.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                        29:19


  Observation. We can syntactically partition the above equation as follows:
                ∀𝑎, if 𝑎 ≥ 𝑙 2 then (if 𝑎 − 𝑙 2 ≥ 𝑙 1 then Y[𝑥 ↦→ 𝑎 − 𝑙 1 − 𝑙 2 ] else 0) else 0 =
                                       if 𝑎 ≥ 𝑙 1 + 𝑙 2 then Y[𝑥 ↦→ 𝑎 − 𝑙 1 − 𝑙 2 ] else 0
We explain each part below:
  Y[_]: represents accesses to the tensor Y.
  𝑥 ↦→ 𝑎 − 𝑙 1 − 𝑙 2 : represents an access expression for a tensor access. In this case, 𝑎 − 𝑙 1 − 𝑙 2 is the
access map for the aggregated-axis 𝑥. The rank of this access map depends on the number of
named-axes in 𝑥. We observe that we can rewrite this expression as follows:
                                                                              df
                       𝑎 − 𝑙 1 − 𝑙 2 = fmap(𝑒, 𝑎, 𝑙 1, 𝑙 2 )      where 𝑒 = 𝜆𝑣, 𝑝, 𝑝 ′ .(𝑣 − 𝑝 − 𝑝 ′ )
where fmap takes a function and applies it to a list of maps. For instance, if 𝑚 = {𝑖 ↦→ 𝑣𝑖 , 𝑗 ↦→ 𝑣 𝑗 }
and 𝑓 = 𝜆𝑣 .(𝑣 + 1), then fmap(𝑓 , 𝑚) = {𝑖 ↦→ 𝑣𝑖 + 1, 𝑗 ↦→ 𝑣 𝑗 + 1}. Here, 𝑒 is independent of the
rank of 𝑥 and only 𝑎, 𝑙 1, 𝑙 2 change as the rank of 𝑥 changes. Thus, we are able to capture all the
rank-independent information in the function 𝑒. We call such a function an index transformer
because it transforms output index-values to input index-values.
  𝑎 ≥ 𝑙 1 + 𝑙 2 : these are boolean values, referred to as conditions, occurring inside if-then-else blocks.
They capture the dependency of the output tensor value on the input tensor values, based on
the value of the access. They originate from the operator semantics. For instance, 𝑛𝑜𝑡-𝑝𝑎𝑑 in the
pad-low semantics takes an access 𝐴 and tells if it lies in the padded area or not. We observe that
we can rewrite this condition as follows:
                                                                              df
                   𝑎 ≥ 𝑙 1 + 𝑙 2 = fold(𝑔1, 𝑎, 𝑙 1, 𝑙 2 )        where 𝑔1 = 𝜆𝑣, 𝑝, 𝑝 ′ .(𝑣 ≥ 𝑝 + 𝑝 ′ )
where fold takes a boolean valued function, applies it to a list of maps, and returns true if all values
are true, false otherwise. fold can be defined as:
                                                    Û
                        fold(𝑔, 𝑚 1, 𝑚 2, · · · ) =      𝑔(𝑚 1 (𝑖), 𝑚 2 (𝑖), · · · )
                                                               𝑖 ∈dom(𝑚 1 )

                                                                               df
Similarly, we can write 𝑎 ≥ 𝑙 2 as fold(𝑔2, 𝑎, 𝑙 2 ), where 𝑔2 = 𝜆𝑣, 𝑝.(𝑣 ≥ 𝑝). Here, 𝑔1 and 𝑔2 are
independent of the rank of 𝑥 and only 𝑎, 𝑙 1, 𝑙 2 change as the rank of 𝑥 changes. We capture all the
rank-independent information in the functions 𝑔1 and 𝑔2 .
   if _ then (if _ then _ else 0) else 0 = if _ then _ else 0: this is a function which returns a boolean,
denoting if the values of LHS and RHS at the access 𝐴 are equal or not. We call this scalarf since
it contains the core, scalar computation in the expressions and may consist of arithmetic and
conditionals. For this rule, we can define scalarf as
                                  df
          scalarf (𝑦, 𝑏 1, 𝑏 2 ) = (if 𝑏 2 then (if 𝑏 1 then 𝑦 else 0) else 0) = (if 𝑏 1 then 𝑦 else 0)
                  df                                             df                        df
               𝑦 = Y[𝑥 ↦→ fmap(𝑒, 𝑎, 𝑙 1, 𝑙 2 )]          𝑏 1 = fold(𝑔1, 𝑎, 𝑙 1, 𝑙 2 ) 𝑏 2 = fold(𝑔2, 𝑎, 𝑙 2 )
Based on the arguments to scalarf, we say scalarf has 1 access to Y and 2 conditions. Note that
there are 2 occurrences each of 𝑦 and 𝑏 1 in the scalarf but we only care about distinct accesses and
conditions. Just like index transformers, scalarf is also independent of the rank of 𝑥. This property
will be crucial for our bound computation algorithm. We use this observation to write Equation 9
in terms of scalarf and substitute it back in Equation 8 to get the validity condition of the rule:
              ∀ Y, 𝑙 1, 𝑙 2, 𝑙 1 ≥ 0 ∧ 𝑙 2 ≥ 0 →
                       ∀𝑎, scalarf (Y[𝑥 ↦→ fmap(𝑒, 𝑎, 𝑙 1, 𝑙 2 )], fold(𝑔1, 𝑎, 𝑙 1, 𝑙 2 ), fold(𝑔2, 𝑎, 𝑙 2 ))        (10)

                                   Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:20                                                                                                                             Arora et al.


  Bound Computation. We first look at the validity condition of the rule when 𝑥 is instantiated with
some rank 𝑖, i.e., valid(𝑖). We instantiate the aggregated-axis 𝑥 to 𝑥 𝑖 , which contains 𝑖 named-axes,
say {1, · · · , 𝑖}. We also instantiate the input tensor, padding attributes, and the general access map.
Thus, we can rewrite valid(𝑖) as

               ∀ Y𝑖 , 𝑙 1𝑖 , 𝑙 2𝑖 , 𝑙 1𝑖 ≥ 0 ∧ 𝑙 2𝑖 ≥ 0 →
                      ∀𝑎𝑖 , scalarf (Y𝑖 [𝑥 𝑖 ↦→ fmap(𝑒, 𝑎𝑖 , 𝑙 1𝑖 , 𝑙 2𝑖 )], fold(𝑔1, 𝑎𝑖 , 𝑙 1𝑖 , 𝑙 2𝑖 ), fold(𝑔2, 𝑎𝑖 , 𝑙 2𝑖 ))          (11)

As noted before, scalarf, 𝑒, 𝑔1 , and 𝑔2 are independent of the rank of 𝑥, so they remain unchanged
irrespective of the value of 𝑖. We want to find a 𝑘 such that Equation 6 holds. The idea is to start
with [valid(𝑘) → valid(𝑘 + 1)] and try to find a 𝑘 which satisfies the induction hypothesis. We
instead work with its contrapositive,

                               valid(𝑘) → valid(𝑘 + 1) ⇔ ¬valid(𝑘 + 1) → ¬valid(𝑘)

   Intuitively, ¬valid(𝑖) is true if there is a counterexample for the rule at rank 𝑖. We want to find
a sufficient 𝑘 such that we can lower a counterexample at rank 𝑘 + 1 (and all higher ranks) to a
counterexample at rank 𝑘. On expanding the validity conditions using Equation 11, we get:
                                                Û
∃ Y𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1, 𝑙 1𝑘+1 ≥ 0 ∧ 𝑙 2𝑘+1 ≥ 0   ∃𝑎𝑘+1,
        ¬scalarf (Y𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒, 𝑎𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1 )], fold(𝑔1, 𝑎𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1 ), fold(𝑔2, 𝑎𝑘+1, 𝑙 2𝑘+1 ))
                                                                     y
                                                                     
                                           Û
∃ Y𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 , 𝑙 1𝑘 ≥ 0 ∧ 𝑙 2𝑘 ≥ 0       ∃𝑎𝑘 ,
        ¬scalarf (Y𝑘 [𝑥 𝑘 ↦→ fmap(𝑒, 𝑎𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 )], fold(𝑔1, 𝑎𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 ), fold(𝑔2, 𝑎𝑘 , 𝑙 2𝑘 ))

This means:
     • We are given a tensor Y𝑘+1 which has 𝑘 + 1 named-axes in 𝑥 𝑘+1 , and whose shape is of the
       form Shape(Y) = {𝑥 𝑘+1 ↦→ 𝑚}, where 𝑚 = {1 ↦→ 𝑛 1, · · · , 𝑘 + 1 ↦→ 𝑛𝑘+1 }
     • We are given padding attributes 𝑙 1𝑘+1 and 𝑙 2𝑘+1 such that the precondition is satisfied.
     • We are given a map 𝑎𝑘+1 such that output tensors do not match at the access {𝑥 𝑘+1 ↦→ 𝑎𝑘+1 }.
     • We then need to construct a tensor Y𝑘 which has 𝑘 named-axes in 𝑥 𝑘 . We also need to
       construct padding attributes 𝑙 1𝑘 and 𝑙 2𝑘 such that the precondition is still satisfied, and a map
       𝑎𝑘 such that the output tensors do not match at the access {𝑥 𝑘 ↦→ 𝑎𝑘 }.

     Counterexample Construction. Our counterexample construction algorithm involves projecting the
(𝑘 +1)-ranked RClass to a 𝑘-ranked RClass, i.e., we would choose 𝑘 named-axes from {1, · · · , 𝑘 + 1}.
There are 𝑘 + 1 such projections but all projections may not lead to a counterexample. We express
our construction through a set of equations and derive constraints on the projection.
     Let Γ ⊂ {1, · · · , 𝑘 + 1} be a projection of size 𝑘. The named-axes in Γ are currently unknown.
We can then express the 𝑘-ranked attributes as follows: Shape(Y𝑘 ) = {𝑥 𝑘 ↦→ 𝑚| Γ }, 𝑎𝑘 = 𝑎𝑘+1 | Γ ,
𝑙 1𝑘 = 𝑙 1𝑘+1 | Γ , and 𝑙 2𝑘 = 𝑙 2𝑘+1 | Γ . These are unknown as well. To construct a 𝑘-ranked counterexample,
we first make sure that the arguments to scalarf have the same values in both ranks. We equate
scalarf arguments in the 𝑘-ranked counterexample to the corresponding arguments in the (𝑘 + 1)-
ranked counterexample and collect constraints on Γ. A constraint is a named-axis that needs to be
in the projection for the 𝑘-ranked counterexample to exist. Thus,

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                       29:21


      • fold(𝑔1, 𝑎𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 ) and fold(𝑔1, 𝑎𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1 ) need to be equisatisfiable. Let 𝐶 1 be the set of
        constraints we get from this equation. We first expand the definition of fold,
                                                                  𝑘+1
                                                                  Û
                           fold(𝑔1, 𝑎𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1 ) =             𝑎𝑘+1 (𝑖) ≥ 𝑙 1𝑘+1 (𝑖) + 𝑙 2𝑘+1 (𝑖)
                                                                  𝑖=1
                                                                  Û
                                  fold(𝑔1, 𝑎𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 ) =          𝑎𝑘 ( 𝑗) ≥ 𝑙 1𝑘 ( 𝑗) + 𝑙 2𝑘 ( 𝑗)
                                                                  𝑗 ∈Γ


        Let 𝑏 = fold(𝑔1, 𝑎𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1 ), which contains 𝑘 + 1 clauses, and 𝑏 ′ = fold(𝑔1, 𝑎𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 ),
        which contains 𝑘 clauses. The value of 𝑏 is known since it depends entirely on the (𝑘 + 1)-
        ranked counterexample. Let 𝑟 be the number of clauses in 𝑏 which evaluate to true. The
        remaining (𝑘 + 1) − 𝑟 clauses evaluate to false. We do a case analysis on 𝑟 :
        – 𝑟 < 𝑘: 𝑏 is false for this case. We want 𝑏 ′ to be false as well. We can see that for any
          projection Γ, 𝑏 ′ will be false. There are no constraints in this case, so 𝐶 1 = ∅.
        – 𝑟 = 𝑘: 𝑏 is false for this case. We want 𝑏 ′ to be false as well. There is exactly one named-axis,
          say 𝑙, for which 𝑎𝑘+1 (𝑙) ≥ 𝑙 1𝑘+1 (𝑙) + 𝑙 2𝑘+1 (𝑙) is false. 𝑙 needs to be in the projection for 𝑏 ′ to
          be false. Leaving out 𝑙 will make 𝑏 ′ true, which is not desirable. For this case, 𝐶 1 = {𝑙 }
        – 𝑟 = 𝑘 + 1: 𝑏 is true for this case, so we want 𝑏 ′ to be true as well. We can see that for any
          projection Γ, 𝑏 ′ will be true. There are no constraints in this case, so 𝐶 1 = ∅.
        As seen above, we get at most one constraint from this equation, so |𝐶 1 | ≤ 1.
      • fold(𝑔2, 𝑎𝑘 , 𝑙 2𝑘 ) and fold(𝑔2, 𝑎𝑘+1, 𝑙 2𝑘+1 ) need to be equisatisfiable. Let 𝐶 2 be the set of constraints
        we get from this equation. We do a similar analysis and get at most one constraint from this
        equation, so |𝐶 2 | ≤ 1. The named-axes in 𝐶 2 may or may not be same as named-axes in 𝐶 1 .
      • Y𝑘 [𝑥 𝑘 ↦→ fmap(𝑒, 𝑎𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 )] needs to be set to Y𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒, 𝑎𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1 )]. This
        does not introduce any constraint, irrespective of the projection. There could have been
        constraints introduced if the scalarf had more than 1 access to Y. We discuss more about the
        general case in §6.3.
   The final set of constraints is computed as 𝐶 = 𝐶 1 ∪ 𝐶 2 . If |𝐶 | > 𝑘, then we cannot get a
valid projection. Thus, we need |𝐶 | ≤ 𝑘 for a valid counterexample lowering. We know that
|𝐶 | = |𝐶 1 ∪ 𝐶 2 | ≤ |𝐶 1 | + |𝐶 2 | ≤ 2. From this, we get 2 ≤ 𝑘 as a sufficient condition for a valid
counterexample lowering. Finally, we can fully construct the 𝑘-ranked counterexample as follows:
      • Projection: The named-axes in 𝐶 need to be a part of the projection Γ, but the other axes
        are unspecified. To get the final projection Γ, extend 𝐶 by any 𝑘 − |𝐶 | named-axes from
        {1, · · · , 𝑘 + 1} 𝐶.
      • Tensor shapes and attributes: Compute the 𝑘-ranked attributes as follows: Shape(Y𝑘 ) =
        {𝑥 𝑘 ↦→ 𝑚| Γ }, 𝑎𝑘 = 𝑎𝑘+1 | Γ , 𝑙 1𝑘 = 𝑙 1𝑘+1 | Γ , and 𝑙 2𝑘 = 𝑙 2𝑘+1 | Γ . This ensures that the shape and the
        access map are valid and the precondition is satisfied in the 𝑘-ranked counterexample.
      • Tensor values: Let 𝑣 = Y𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒, 𝑎𝑘+1, 𝑙 1𝑘+1, 𝑙 2𝑘+1 )]. We only require Y𝑘 to have the
        value 𝑣 at the access {𝑥 𝑘 ↦→ fmap(𝑒, 𝑎𝑘 , 𝑙 1𝑘 , 𝑙 2𝑘 )} and the values at other points are unspecified.
  Therefore, for all 𝑘 ≥ 2, valid(𝑘) implies valid(𝑘 + 1). This allows us to reduce the unbounded-
verification proof obligation to two bounded-verification proof obligations: valid(1) and valid(2).

6.3     Bound Computation for the General Case
In §6.2, we derived a bound for the PadLowCombine rule and reduced the unbounded-verification
proof obligation to bounded-verification proof obligations. This section first presents a theorem
for unbounded verification for a general rewrite rule and an algorithm to compute a bound in the

                                  Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:22                                                                                         Arora et al.


general case. We then briefly discuss how we handle the complexities of the general case. The
detailed proof is in §E. The InferBound routine is described in Algorithm 1.
Lemma 1. Let 𝑅 be any rewrite rule written in our DSL. Let 𝑚 be a map containing ranks of
RClasses in 𝑅. For any RClass 𝑐 in the rule, if 𝑘 = InferBound(𝑅, 𝑐), then
                              ∀𝑖 ≥ 𝑘, valid(𝑚[𝑐 ↦→ 𝑖]) → valid(𝑚[𝑐 ↦→ 𝑖 + 1])
  Here, 𝑚[𝑐 ↦→ 𝑗] denotes the map where the rank of 𝑐 is updated to 𝑗, while all other ranks are
unchanged. In other words, for all 𝑖 ≥ 𝑘 and for any ranks of the other RClasses, if the rule is valid
when 𝑐 has rank 𝑖, then it implies that the rule is valid when 𝑐 has rank 𝑖 + 1. Lemma 1 allows us to
use 𝑘-induction on the RClass ranks to verify the rule for arbitrary ranks of all RClasses.
Theorem 2. Let 𝑅 be any rewrite rule written in our DSL. If 𝑐 1 · · · 𝑐 𝑝 are the RClasses appearing
in the rule and 𝑘𝑖 = InferBound(𝑅, 𝑐𝑖 ) for all 𝑖 ∈ {1 · · · 𝑝}, then 𝑅 is a valid rule in the unbounded
setting if and only if
                          Û         Û
                              ···          valid({𝑐 1 ↦→ 𝑟 1, · · · , 𝑐 𝑝 ↦→ 𝑟 𝑝 })
                              1≤𝑟 1 ≤𝑘 1   1≤𝑟 𝑝 ≤𝑘𝑝

This follows from using Lemma 1 as induction hypothesis for all RClasses.
  The InferBound routine in Algorithm 1 takes a rewrite rule 𝑅 and RClass 𝑐 as input. On line 3, we
use the TensorsWithRClass subroutine to get all the input tensors which have an aggregated-axis
having the RClass 𝑐. We iterate through all the tensors in lines 4-9. For each tensor, we use the
NumTensorAccess subroutine to get the number of distinct accesses to that tensor and add its
contribution to the bound. On line 10, we use the NumConds subroutine to get the number of
conditions having an aggregated-axis with the RClass 𝑐 and add it to the bound. We also make sure
that the computed bound is at least 1 since we do not want empty aggregated-axes.
  We now briefly discuss the complexities that we encounter while tackling a general rewrite rule
and how the bound computed by this algorithm is sufficient.
  Arbitrary Operator Compositions. For
any rule written in our DSL, we can sym-
                                             Algorithm 1: Computing the bound for an
bolically evaluate both LHS and RHS ex-
                                             RClass
pressions under a general, valid access.
                                              Inputs : Rewrite rule 𝑅 & RClass 𝑐
We observe that the result can be ex-
                                              Output : 𝑏𝑜𝑢𝑛𝑑, i.e., a sufficient rank for 𝑐
pressed in terms of a scalarf function,
                                            1 Function InferBound (𝑅, 𝑐) :
which could have any number of accesses
                                            2    𝑏𝑜𝑢𝑛𝑑 ← 0;
and conditions, similar to the PadLow-
                                            3    𝑡𝑒𝑛𝑠𝑜𝑟𝑠 ← TensorsWithRClass(𝑅, 𝑐);
Combine rule. Therefore, we need to ap-
propriately handle arbitrary number of      4    for 𝑡 ∈ 𝑡𝑒𝑛𝑠𝑜𝑟𝑠 do
accesses and conditions.                    5        𝑛 ← NumTensorAccess(𝑅, 𝑡);
                                            6        if 𝑛 > 1 then
   Arbitrary Number of Conditions. In gen- 7             𝑏𝑜𝑢𝑛𝑑 ← 𝑏𝑜𝑢𝑛𝑑 + 𝑛2 ;
                                                                                
eral, a rule could have an arbitrary num- 8          end
ber of conditions, say 𝑚. Similar to the
                                            9    end
PadLowCombine rule, we observe that
                                           10    𝑏𝑜𝑢𝑛𝑑 ← 𝑏𝑜𝑢𝑛𝑑 + NumConds(𝑅, 𝑐);
any condition introduces at most 1 con-
straint. We assume that all 𝑚 conditions   11    return Max(𝑏𝑜𝑢𝑛𝑑, 1)
are independent and we get 𝑚 constraints   12 End Function
in the worst case.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:23


   Arbitrary Number of Tensor Accesses. In general, a rule could have an arbitrary number of accesses,
say 𝑛, to a tensor. We need to make sure that during the projection, accesses containing unequal
values do not get projected down to the same point in the tensor,
                                                                      since a point cannot have two
different values. We do a pairwise analysis of the accesses ( 𝑛2 such pairs) and each pair can give at
                                   
most 1 constraint. Thus, we get 𝑛2 constraints from the accesses in the worst case.
   Arbitrary Number of RClasses. In general, a rule could have any number of aggregated-axes
and RClasses. This would require computing the minimum rank for each RClass. We do so by
analyzing each RClass in isolation, i.e., finding a sufficient 𝑘 for which we can do a (𝑘 + 1) to 𝑘
counterexample projection
                           while keeping the ranks of other RClasses unchanged. The bound for
this case would be 𝑛2 + 𝑚, where 𝑛 is the number of accesses and 𝑚 is the number of conditions
in which the RClass appears. The computed bound is independent of the ranks of the other
RClasses. Therefore, to ensure correctness in the unbounded setting in presence of multiple
RClasses, bounded-verification instances corresponding to all possible combinations of RClass
ranks within the bounds need to be verified. This means that if 𝑐 1 · · · 𝑐 𝑝 are the RClasses appearing
                                                                                         Î𝑝
in a rule 𝑅 and 𝑘𝑖 = InferBound(𝑅, 𝑐𝑖 ) for all 𝑖 ∈ {1 · · · 𝑝}, then we need to verify 𝑖=1 𝑘𝑖 number
of bounded-verification instances.
   Arbitrary Number of Input Tensors. In general, a rule could have any number of input tensors. We
still analyze each RClass in isolation, but while counting the number of accesses, we only consider
accesses to the tensors which contain that RClass. We also make the observation that accesses
across tensors do not lead to any constraints, which allows us to do a pairwise analysis of accesses
per tensor. We then add the contribution of each tensor to the bound. This is necessary since we
take the union of all constraints from all tensors.

6.4   Bounded Verification of Rewrite Rules
We reduced the unbounded-verification proof obligation to a finite set of bounded-verification
proof obligations in §6.3. TensorRight infers a sufficient rank for every RClass and instantiates
them with all ranks up to that bound, so we end up with fixed-rank but arbitrary-sized tensors.
We handle tensors of unbounded size using uninterpreted functions from accesses to values. For
any rewrite rule, TensorRight symbolically executes the LHS and RHS tensor expressions using
operator semantics and interprets them under a general access with symbolic indices, chosen
from the domain of accesses of the two expressions. During the symbolic execution, TensorRight
decomposes the verification into two kinds of checks below.
  Checks performed during symbolic execution. Each tensor operator constructs the shape of the
output tensor using the shapes of the input tensor(s). TensorRight checks that the final LHS and
RHS tensors have the same rank and the same named-axes, i.e., (= (axes lhs) (axes rhs)).
This check is performed entirely by the symbolic execution engine, rather than by the solver.
   Checks delegated to the SMT solver. During symbolic execution, TensorRight collects assertions
which are then sent to an SMT solver as verification conditions. These assertions check that the
axes sizes for LHS and RHS are the same; that accesses fall within axes sizes; and that the values
stored in tensor expressions are the same. These verification conditions are described below:
    • Assertions related to axes sizes: under the precondition, assuming LHS is valid, assert that
      the LHS shape and RHS shape are the same. This can be represented as (=> (&& precond
      lhsValid) (= (shape lhs) (shape rhs))). Asserting the equality of two shapes involves
      checking if the shapes have the same named-axes and the corresponding axes have the same
      sizes. As discussed, the former check is done entirely by the symbolic execution engine.
      However, the solver is needed for the latter check.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:24                                                                                            Arora et al.


      • Assertions related to access ranges: under the precondition, assuming LHS is valid, all valid
        accesses to LHS lead to valid accesses to RHS. This can be represented as (=> (&& precond
        lhsValid lhsAccessValid) rhsAccessValid).
      • Assertions related to final tensor expressions: under the precondition, assuming that LHS is
        valid, RHS should be valid and they contain the same values under a general access. This can
        be represented as (=> (&& precond lhsValid) (&& rhsValid rewriteEquivalent)).
    If the symbolic execution and SMT checks succeed, the rule is deemed verified for that rank.

6.5     Verifying Rules with Reduction Operators
As discussed in §5, automatically verifying expressions with reductions is challenging because:
      • The sizes of reduced axes are unbounded.
      • Reductions can be performed in multiple steps, such as when tiling the tensors or distribut-
        ing reduction over concatenation. One such example is the rule reduce(concat(A, B)) ⇒
        reduce(concat(reduce(A), reduce(B))).
   In TensorRight, the key idea to verify rewrite rules with reductions is to represent the reduction
results as uninterpreted reduction elements, Red𝑋 𝑓 (𝑋 ) (see §5). We observe that the equivalence of
two reduction elements Red𝑋 𝑓 (𝑋 ) and Red𝑌 𝑔(𝑌 ), can often be proven by showing that the LHS
and RHS are sums of the same values, i.e., 𝑓 (𝑋 ) and 𝑔(𝑌 ) represent the same (multi-)set.
   One way to prove set equivalence is to establish a bijection between 𝑋 and 𝑌 and show each
pair of values in 𝑓 (𝑋 ) and 𝑔(𝑌 ) are equal, regardless of tensor instantiation and operator attributes.
In TensorRight, the user provides a relation between 𝑋 and 𝑌 as a hint. We then use an SMT
solver to verify that it is a bijection: (1) for all valid 𝑥 ∈ 𝑋 , a unique 𝑦 ∈ 𝑌 exists under the relation,
and vice versa and (2) the relation can take on all valid 𝑥 ∈ 𝑋 and 𝑦 ∈ 𝑌 . After establishing the
bijection, we prove each pair of elements 𝑓 (𝑥) and 𝑔(𝑦) are always the same, regardless of tensor
instantiation. Successfully passing the checks reduces our proof to the case discussed in §6.4.
   A majority of rules with reductions (13 out of 17) in our system can be proven by establishing
the bijection with user-provided hints. However, there are rules where bijectivity cannot be proven
due to limitations of SMT solvers on quantified formulas (1 out of 17), or no such bijection relation
exists due to the fact that the cardinalities of the sets of valid reduction indices in LHS and RHS
are different (3 out of 17). In these cases, it is up to the user to further complete the proof of set
equivalence based on the verifier output. Note that this is generally much easier than proving full
correctness from scratch.

7     Discussion
   Choice of Tensor Compiler. We chose XLA since it is a production quality compiler and is integrated
into leading ML frontend-frameworks like TensorFlow, PyTorch, and JAX. The XLA compiler takes
model graphs from these frontends and converts them into XLA-HLO, which is much more expressive
than these frameworks. Operators in these frameworks either have direct counterparts in XLA-HLO
(e.g., concat, expand, slice), or can be expressed using existing XLA-HLO operators (e.g., squeeze,
shrink, split). Some XLA-HLO operators are more general than their counterparts in other frameworks.
For instance, tf.tensordot in TensorFlow allows specifying only the contracting axes, whereas
DotGeneral in XLA-HLO allows specifying both contracting and batch axes. tf.pad in TensorFlow
and Pad in ONNX allow specifying only low and high padding attributes, whereas pad in XLA-HLO
allows specifying interior padding as well. Moreover, many operators in the jax.lax module [9] are
thin wrappers around equivalent XLA-HLO operators. As for other IR frameworks like ONNX [10],
their operators also are either similar to XLA-HLO operators, or can be expressed using XLA-HLO
operators. Therefore, XLA-HLO supports a more general set of operators than other frameworks.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:25


    Minimum vs Sufficient Rank for Unbounded Verification. §6.3 shows how we can use the Infer-
Bound routine to compute a bound for every RClass in a rewrite rule and get a set of bounded-
verification instances. These bounded-verification instances are sufficient to imply correctness in
the unbounded setting. It is worth noting that this computed bound is only a sufficient rank and not
the minimum rank required for such a property to hold. For instance, in §6.2, we compute a bound
for the PadLowCombine rule by calculating the number of conditions and the number of accesses.
We assume the two conditions to be independent, each contributing 1 constraint in the worst case,
hence getting 2 as the final bound. However, we observe that given the precondition, the condition
𝑏 1 implies the condition 𝑏 2 , which reduces the bound to 1. In general, the conditions may have
dependencies and such insights can help us derive a smaller, or maybe even the minimum bound.

8     Evaluation
We evaluated the TensorRight verification framework on the following aspects:
      • Q1: How expressive is TensorRight DSL compared to other automatic tensor graph rewrite
        verification systems? (§8.1)
      • Q2: How good is TensorRight at performing unbounded verification? (§8.2)
      • Q3: Can TensorRight be used to aid compiler developers in rapid development? (§8.3)
  To answer these questions, we selected all rules from the XLA’s Algebraic Simplifier (AS) for
evaluation. The AS rewrite pass has 175 rules. These rules are implemented to speed up execution
and allow further optimizations like fusion in other compiler passes.

8.1    Expressiveness of TensorRight DSL
We compared the expressiveness of TensorRight with two other automatic tensor graph rewrite
engines, TASO [20] and PET [38], across all the 175 rules. These rules are categorized into 5 classes,
as shown in Table 1. We assessed whether each system can represent rules from these classes.
While TASO and PET do not support automatic, unbounded verification, we evaluated whether
they can express these rules. We found that TASO can represent 14 rules, and PET can represent 18
rules. Comparatively, TensorRight can represent 121 rules.
  We also checked whether TASO and PET can perform bounded verification on the rules they
can represent. TASO and PET can prove 6 and 16 rules, respectively. In contrast, TensorRight
verified 115 rules in the unbounded setting. Verification statistics are detailed in §8.2.
   Categories. Table 1 categorizes all the rules into 5 classes and summarizes representable rules
in the systems. Numbers in parentheses indicate verifiable rules, with TensorRight supporting
unbounded verification and others using bounded verification strategies. There are two high-level
classes: element-wise and non-element-wise rules. Element-wise rules are expressed with element-
wise arithmetic operations. They are further divided into rules with basic operators (e.g., +, ∗,
div, rem) and rules with advanced operators without good support by solvers (e.g., exp, power).
Non-element-wise rules involve operators that change axes sizes or perform reductions. This
category is further divided into reductions (e.g., conv, dot, and reduce), layout-sensitive operators
(e.g., reshape, bitcast), and others. We separately categorized rules with preconditions. Note that
rules with preconditions usually perform non-element-wise operations.
   TensorRight. We implemented TensorRight in Haskell using the Grisette [29] symbolic evalu-
ation engine. We represented 121 rules in TensorRight and verified 115 of them in the unbounded
setting, using Z3 [15] for most verifications and cvc5 [6] for one advanced element-wise rule.
   Table 1 shows that TensorRight was able to represent 46 element-wise simple rules and verified
45 of them. In the advanced element-wise class, TensorRight was able to verify only one rule

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:26                                                                                                Arora et al.


Table 1. Number of supported rules per disjoint category. The numbers in parentheses indicate rules that
have been implemented and verified. † means verified using cvc5 solver.

                                                                Number of Supported Rules
                                  Category (disjoint)
                                                          XLA    TensorRight TASO       PET
                                 Elementwise: simple       56       46 (45)       11 (5)   11 (11)
                              Elementwise: advanced        10        1 (1† )       0 (0)    0 (0)
                         Non-elementwise: reductions       22       20 (17)        0 (0)    2 (0)
                     Non-elementwise: layout-sensitive     29        0 (0)         0 (0)    2 (2)
                             Non-elementwise: others       58       54 (52)        3 (1)    3 (3)
                              Rules with Preconditions     61       40 (34)       0 (0)     0 (0)
                                                  Total   175      121 (115)      14 (6)   18 (16)



involving exp with cvc5. The limitations are due to unsupported operators in Z3 or cvc5 (e.g., log,
power) and the inability to reason about precision of floating point expressions efficiently.
  Among non-element-wise rules, TensorRight was able to represent 74 and verified 69 rules.
For reduction rules, 20 rules were represented, with 3 unproven due to insufficient normalization
lemmas and handling cases with extra zeroes. TensorRight DSL cannot represent layout-sensitive
rules. We further discuss this in §10. The unsupported rules in the other category are due to
unimplemented operators (e.g., scatter, gather), while two rules failed to verify due to timeouts.

   Comparison to Prior Works. We compared TensorRight with TASO and PET, which use axiomatic
and statistical proof mechanisms, respectively. Table 1 shows that TensorRight was able to support
significantly more rules than TASO and PET. The main hurdles for TASO and PET were unsupported
operators, too strict operator definitions (e.g., not supporting all the attributes for dot and conv),
and inability to handle preconditions. Unlike TensorRight, TASO and PET cannot express rules
requiring preconditions, precluding them from supporting 61 XLA rules.
   The axiomatic approach requires axioms to prove equivalence of tensor expressions. Out of the
14 representable rules, 8 rules needed new axioms in TASO. It can be even more cumbersome for
an axiomatic approach like TASO when we need new axioms with preconditions.
   The statistical approach in PET has benefits and drawbacks. It does not need verification con-
ditions proven by SMT solvers, making it potentially more flexible for operations not modeled
in SMT. However, PET can only verify linear expressions, which limits its scope. It is potentially
feasible to add support for preconditions by only generating test inputs meeting the precondition.

8.2     Verification Capabilities of TensorRight
   Experimental Setup. All evaluations were conducted on a system equipped with an Intel Core
i9-13900K processor and 128 GB of RAM. We supported boolean, integer, and real-valued tensors
in our DSL, and we verified the rules for all valid tensor types for that rule. The timeout per SMT
solver query was set to 10 seconds.
   Out of the 121 rules that we can express in our DSL, we implemented 118 rules and verified 115
rules in the unbounded setting. Fig. 10a shows cumulative distribution of total verification times for
the 115 verified rules. TensorRight was able to verify 108 rules under 1 second, with verification
times ranging from a minimum of 0.023 s to a maximum of 23.33 s. Fig. 10b shows the number of
bounded-verification proof obligations (tasks) discharged for the verified rules. The number of
tasks is simply the product of the computed bounds of all RClasses in a rule. 110 of the rules only
required 1 task to guarantee correctness in the unbounded setting.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                         29:27

            1.0
                                                                                           110




                                                                   Number of Rules
            0.8
                                                                                     100
            0.6
      CDF




            0.4                                                                      50
            0.2
                                                                                                         3      2
            0.0                                                                       0
                    0.1         1         10                                               1           2         4
                  Total Verification Time (s)                                                    Number of Tasks

                          (a)                                                                      (b)

Fig. 10. (a) The cumulative distribution of total verification time and (b) the number of tasks (bounded-
verification proof obligations) discharged.



  TensorRight was unable to verify 6 rules. This included 3 timeouts, mainly due to those rules
having operators like div and rem, which solvers are slow at handling. The remaining 3 rules (not
implemented) cannot be proven correct due to missing rules on reduction elements.

8.3    Generalizing Rewrite Rules
Using TensorRight, we found that some XLA rewrite rules are overly constrained. Compiler
engineers intentionally impose these constraints to avoid reasoning about cases where spurious
bugs might be introduced. We used TensorRight to generalize the following rule by relaxing its
precondition.
   Fig. 11 (top) presents the FoldConvInputPad rule as
it exists in XLA using the TensorRight DSL notation.           FoldConvInputPad(XLA):
The goal of the rule is to fold the pad operator into the        let 𝑆𝑜𝑙 = 𝑆𝑙 + 𝑆𝑙𝑝 in
operand arguments of conv itself (XLA-HLO convolutions           let 𝑆𝑜ℎ = 𝑆ℎ + 𝑆ℎ𝑝 in
support padding as operands). This rule does not support             conv(pad(𝑡, 0, 𝑆𝑙𝑝 , 𝑆ℎ𝑝 , 𝑆𝑖𝑝 ), 𝑡 ′,
internal padding in the input tensor and gives up if                       𝐵, 𝐹, 𝑂, 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 , 𝑆𝑖′ )
this constraint is violated. This is largely because it is                      =⇒
                                                                                       𝑆𝑖𝑝 = 0 ∧ 𝑆𝑖 = 1
non-trivial to think about how the internal padding gets             conv(𝑡, 𝑡 ′, 𝐵, 𝐹, 𝑂,
folded into the dilation attribute. TensorRight was able                   𝑆𝑜𝑙 , 𝑆𝑜ℎ , 𝑆𝑖 , 𝑆𝑖′ )
to prove a more general version of this rule as shown in
Fig. 11 (bottom). The differences are put in boxes.            FoldConvInputPad(Generalized):
   The key to generalizing the rule is to calculate the           let 𝑆𝑜𝑙 = 𝑆𝑙 + 𝑆𝑖 × 𝑆𝑙𝑝 in
padding arguments that get fed into the conv operator.
                                                                  let 𝑆𝑜ℎ = 𝑆ℎ + 𝑆𝑖 × 𝑆ℎ𝑝 in
This is a function of the pad operator’s interior, high,
and low padding, as well as padding that may already              let 𝑆𝑜𝑖 = 𝑆𝑖 + 𝑆𝑖 × 𝑆𝑖𝑝 in
exist in the conv operator. Fig. 11 (bottom) shows how to           conv(pad(𝑡, 0, 𝑆𝑙𝑝 , 𝑆ℎ𝑝 , 𝑆𝑖𝑝 ), 𝑡 ′,
calculate the maps 𝑆𝑜𝑙 , 𝑆𝑜ℎ , 𝑆𝑜𝑖 for the rule to be general.            𝐵, 𝐹, 𝑂, 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 , 𝑆𝑖′ )
These maps are more complicated than the non-general                           =⇒
version, but this allows the compiler writer to get rid             conv(𝑡, 𝑡 ′, 𝐵, 𝐹, 𝑂,
of the precondition of the rule shown in Fig. 11 (bot-                    𝑆𝑜𝑙 , 𝑆𝑜ℎ , 𝑆𝑜𝑖 , 𝑆𝑖′ )
tom). It is not immediately clear why this formulation
might be correct. Therefore, we encode it in our Grisette        Fig. 11. Fold input pad into conv.
implementation and successfully prove that the generalized rule with these calculations is valid.

                                Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:28                                                                                       Arora et al.


9   Related Works
TensorRight is inspired by prior works on representing and verifying compiler transformations.
   Tensor Language Formalisms. Glenside [37] formalizes the syntax and provides a composable
abstraction to represent tensor graph rewrites in a purely functional form. TASO [20] uses s-
expression based representations to functionally model tensor operators. It does not provide
semantics for tensor operators and mostly relies on axioms built around the operators to perform
verification related tasks. Such an axiomatic approach would not scale with addition of new tensor
operators, as it requires axioms describing operator properties and how the operators interact
with each other. TensorRight on the other hand only requires the users to specify operator
semantics for every new operator once. PET [38] verifies rewrites rule via a statistical approach.
PET symbolically infers the bounding boxes of the output tensor, where each box contains elements
represented by the same linear expression of its input elements. Leveraging the linear property,
PET statistically verifies the equivalence of the corresponding boxes by checking 𝑚 + 1 specific
positions in the box, where 𝑚 is the number of axes of the output tensor.
   There have been many works providing semantics for hardware instructions [14, 19] or general
purpose compiler IRs such as LLVM IR [42]. ATL [25] is among the first works to provide denota-
tional semantics to model a tensor language. It is closely modeled after the widely adopted Halide
language [32]. In contrast, TensorRight models its core language around the production XLA
compiler’s High Level Operators. To the best of our knowledge, it is the first formalism supporting
XLA-HLO’s operators in their full generality, modeling all the parameterizations of operators. Similar
to ATL, TensorRight provides denotational semantics of tensor operators with arbitrary rank and
size, which is key to the proof that reduces unbounded verification into a bounded setting.
  Verification of Rewrites with Proof Assistants. ATL [25] is among the first works to successfully
prove correctness of tensor graph rewrites with input tensors of arbitrary shape using the Coq proof
assistant. Comparatively, TensorRight does automatic verification given the rewrite specification
and accepts preconditions which are prevalent in practical rewrite rules developed by compiler
engineers. We note that ATL’s Coq based approach supports layout-sensitive rewrites such as those
that involve reshapes, which TensorRight does not cover currently. We provide a methodology to
support those operators in §10. There are examples from other domains on mechanized proofs on
rewrite systems, covering relational algebra [7, 16] and compiler construction tools [18].
   Automated Verification of Rewrites. We take inspiration from many successful works focusing on
automatically verifying rewrites for different program representations, mainly with the aid of SMT
solvers. Alive [28] focuses on verifying rewrite rules in LLVM’s Instruction Combiner pass, which
is LLVM’s peephole optimization. They mainly focus on scalar LLVM IR instructions. Many works
on superoptimization use automated verification of rewrites as part of their synthesis process.
For example, the STOKE project [35] and others [5] verify rewrites expressed in x86 instructions,
Souper [34] verifies rewrites expressed in LLVM IR instructions, Minotaur [27] extends this to
vector LLVM IR instructions and [30] proves rewrite rules in Halide IR. TASO [20], PET [38],
and TENSAT [41] are examples of systems that automatically synthesize tensor graph rewrites.
TensorRight is influenced by the success of these systems and for the first time proposes an
automated process for verifying tensor graph rewrites on input tensors of arbitrary ranke and size.
Further, TensorRight is the first system to incorporate preconditions in its verification process.
  Compiler Verification. There is a lot of work in building verified general-purpose compilers.
CompCert [24] is a formally verified C compiler with many verification efforts and extensions [17,
22, 39, 40]. CakeML [23] is a formally verified ML compiler. There are works on building associated
verified transformations [21, 42, 43]. Comparatively, less works have explored verifying compiler

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:29


transformations in tensor compilers. ATL [25, 26] is one of the first successes on this front that builds
upon a proof-assistant-aided verification process. To the best of our knowledge, TensorRight
is one of the first efforts at automatically verifying tensor graph rewrites closely resembling the
industrial strength XLA tensor compiler.

10   Limitations and Future Work
Currently, TensorRight does not support layout-sensitive rules with operators like reshape or
bitcast, which change operand layouts or do not respect element boundaries. The reshape operator
is particularly challenging to verify because it can collapse or flatten an arbitrary number of axes,
complicating the representation and verification of rank-polymorphic rules. This complexity arises
because reshape changes the interpretation of the input tensor by linearizing and de-linearizing
its accesses, depending on the rank of input. However, some reshape rules in XLA do not use the
operator’s full generality. This suggests a pragmatic approach to extend TensorRight to support
these simpler cases, addressing much of its practical usage in XLA. The exploration of reshape’s full
generality is left as potential future work.
   As shown in §6.5, TensorRight can currently verify a subset of reduction rules. Users need
to provide hints to establish relations between reduction indices, satisfying assumptions like no
duplicate values being reduced or 1-1 relations. However, there are limitations, such as handling
cases with extra zeroes being reduced, difficulty in proving bijectivity due solver limitations, and
instances where no bijection relation exists. In these cases, users need to complete the proof of
set equivalence based on verifier output, which is generally easier than proving full correctness
from scratch. Future work may explore better proof strategies for reduction rules, possibly using a
𝑘-induction approach to establish bounds and finitize sizes for reduction axes.

11   Conclusion
In this paper, we presented TensorRight, the first automatic verification system that allows users to
succinctly express and verify tensor graph rewrite rules in their full generality. To do so, we designed
TensorRight DSL, which allows specification of rank- and size-polymorphic rewrite rules using a
novel axis definition, called aggregated-axes. TensorRight DSL consists of highly parameterized
tensor operators, closely resembling those in XLA-HLO. We also provided denotational semantics
for TensorRight DSL and used them to convert the unbounded-verification proof obligation to
a finite set of bounded-verification proof obligations. To the best of our knowledge, this is the
first time a sizable subset of tensor operators from a production-quality tensor IR (XLA-HLO) was
formalised. We demonstrated that TensorRight can verify the majority of complex rewrite rules
from the production XLA compiler’s algebraic simplifier in the unbounded setting, vastly surpassing
the closest automatic, bounded-verification technique.

12   Data-Availability Statement
An artifact [3] associated with this paper was evaluated and is freely available.

Acknowledgments
We thank the anonymous reviewers for their constructive feedback. We would also like to thank
Wanyu Zhao for her feedback on early drafts of this paper. This work was supported in part by
ACE, one of the seven centers in JUMP 2.0 and the CONIX Research Center, one of the six centers
in JUMP, which are Semiconductor Research Corporation (SRC) programs sponsored by DARPA;
by NSF under grants CCF-2338739, CCF-2122950, ITE-2132318, and CCF-2437238; by DARPA under
grants FA8750-16-2-0032 and D22AP00146-00 as well as gifts from Adobe, Facebook, and Intel.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:30                                                                                                           Arora et al.


References
 [1] Martín Abadi, Paul Barham, Jianmin Chen, Zhifeng Chen, Andy Davis, Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat,
     Geoffrey Irving, Michael Isard, Manjunath Kudlur, Josh Levenberg, Rajat Monga, Sherry Moore, Derek G. Murray,
     Benoit Steiner, Paul Tucker, Vijay Vasudevan, Pete Warden, Martin Wicke, Yuan Yu, and Xiaoqiang Zheng. 2016.
     TensorFlow: A System for Large-Scale Machine Learning. In 12th USENIX Symposium on Operating Systems Design and
     Implementation (OSDI 16). USENIX Association, Savannah, GA, 265–283. https://www.usenix.org/conference/osdi16/
     technical-sessions/presentation/abadi
 [2] Jason Ansel, Edward Yang, Horace He, Natalia Gimelshein, Animesh Jain, Michael Voznesensky, Bin Bao, Peter
     Bell, David Berard, Evgeni Burovski, Geeta Chauhan, Anjali Chourdia, Will Constable, Alban Desmaison, Zachary
     DeVito, Elias Ellison, Will Feng, Jiong Gong, Michael Gschwind, Brian Hirsh, Sherlock Huang, Kshiteej Kalambarkar,
     Laurent Kirsch, Michael Lazos, Mario Lezcano, Yanbo Liang, Jason Liang, Yinghai Lu, C. K. Luk, Bert Maher, Yunjie
     Pan, Christian Puhrsch, Matthias Reso, Mark Saroufim, Marcos Yukio Siraichi, Helen Suk, Shunting Zhang, Michael
     Suo, Phil Tillet, Xu Zhao, Eikan Wang, Keren Zhou, Richard Zou, Xiaodong Wang, Ajit Mathews, William Wen,
     Gregory Chanan, Peng Wu, and Soumith Chintala. 2024. PyTorch 2: Faster Machine Learning Through Dynamic
     Python Bytecode Transformation and Graph Compilation. In Proceedings of the 29th ACM International Conference on
     Architectural Support for Programming Languages and Operating Systems, Volume 2 (La Jolla, CA, USA) (ASPLOS ’24).
     Association for Computing Machinery, New York, NY, USA, 929–947. https://doi.org/10.1145/3620665.3640366
 [3] Jai Arora, Sirui Lu, Devansh Jain, Tianfan Xu, Farzin Houshmand, Phitchaya Mangpo Phothilimthana, Mohsen Lesani,
     Praveen Narayanan, Karthik Srinivasa Murthy, Rastislav Bodik, Amit Sabne, and Charith Mendis. 2024. Artifact for
     "TensorRight: Automated Verification of Tensor Graph Rewrites". https://doi.org/10.5281/zenodo.14159871
 [4] The JAX Authors. 2024. Named axes and easy-to-revise parallelism with xmap. https://web.archive.org/web/
     20240320140219/https://jax.readthedocs.io/en/latest/notebooks/xmap_tutorial.html archived 2024-03-20.
 [5] Sorav Bansal and Alex Aiken. 2006. Automatic generation of peephole superoptimizers. SIGOPS Oper. Syst. Rev. 40, 5
     (oct 2006), 394–403. https://doi.org/10.1145/1168917.1168906
 [6] Haniel Barbosa, Clark Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt, Makai Mann, Abdalrhman Mohamed,
     Mudathir Mohamed, Aina Niemetz, Andres Nötzli, Alex Ozdemir, Mathias Preiner, Andrew Reynolds, Ying Sheng,
     Cesare Tinelli, and Yoni Zohar. 2022. cvc5: A Versatile and Industrial-Strength SMT Solver. In Tools and Algorithms for
     the Construction and Analysis of Systems, Dana Fisman and Grigore Rosu (Eds.). Springer International Publishing,
     Cham, 415–442.
 [7] Véronique Benzaken and Évelyne Contejean. 2019. A Coq mechanised formal semantics for realistic SQL queries:
     formally reconciling SQL and bag relational algebra. In Proceedings of the 8th ACM SIGPLAN International Conference
     on Certified Programs and Proofs (Cascais, Portugal) (CPP 2019). Association for Computing Machinery, New York, NY,
     USA, 249–261. https://doi.org/10.1145/3293880.3294107
 [8] James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula,
     Adam Paszke, Jake VanderPlas, Skye Wanderman-Milne, and Qiao Zhang. 2018. JAX: composable transformations of
     Python+NumPy programs. http://github.com/google/jax
 [9] JAX Contributors. 2024. jax.lax module. https://jax.readthedocs.io/en/latest/jax.lax.html
[10] ONNX Contributors. 2024. ONNX. https://onnx.ai/onnx/operators/
[11] OpenXLA Contributors. 2024. OpenXLA Project. https://web.archive.org/web/20241009145043/https://openxla.org/xla
[12] OpenXLA Contributors. 2024. XLA-HLO Operation Semantics. https://openxla.org/xla/operation_semantics
[13] PyTorch Contributors. 2024. Named Tensors. https://web.archive.org/web/20240703124627/https://pytorch.org/docs/
     stable/named_tensor.html archived 2024-07-03.
[14] Sandeep Dasgupta, Daejun Park, Theodoros Kasampalis, Vikram S. Adve, and Grigore Roşu. 2019. A complete formal
     semantics of x86-64 user-level instruction set architecture. In Proceedings of the 40th ACM SIGPLAN Conference on
     Programming Language Design and Implementation (Phoenix, AZ, USA) (PLDI 2019). Association for Computing
     Machinery, New York, NY, USA, 1133–1148. https://doi.org/10.1145/3314221.3314601
[15] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: an efficient SMT solver. In Proceedings of the Theory and Practice of
     Software, 14th International Conference on Tools and Algorithms for the Construction and Analysis of Systems (Budapest,
     Hungary) (TACAS’08/ETAPS’08). Springer-Verlag, Berlin, Heidelberg, 337–340.
[16] Benjamin Delaware, Clément Pit-Claudel, Jason Gross, and Adam Chlipala. 2015. Fiat: Deductive Synthesis of Abstract
     Data Types in a Proof Assistant. In Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles
     of Programming Languages (Mumbai, India) (POPL ’15). Association for Computing Machinery, New York, NY, USA,
     689–700. https://doi.org/10.1145/2676726.2677006
[17] Delphine Demange, David Pichardie, and Léo Stefanesco. 2015. Verifying Fast and Sparse SSA-Based Optimizations in
     Coq. In Compiler Construction, Björn Franke (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 233–252.
[18] Jason Gross, Andres Erbsen, Jade Philipoom, Miraya Poddar-Agrawal, and Adam Chlipala. 2022. Accelerating Verified-
     Compiler Development with a Verified Rewriting Engine. In 13th International Conference on Interactive Theorem


Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                         29:31


     Proving (ITP 2022) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 237), June Andronick and Leonardo
     de Moura (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 17:1–17:18. https://doi.org/
     10.4230/LIPIcs.ITP.2022.17
[19] Stefan Heule, Eric Schkufza, Rahul Sharma, and Alex Aiken. 2016. Stratified synthesis: automatically learning the
     x86-64 instruction set. In Proceedings of the 37th ACM SIGPLAN Conference on Programming Language Design and
     Implementation (Santa Barbara, CA, USA) (PLDI ’16). Association for Computing Machinery, New York, NY, USA,
     237–250. https://doi.org/10.1145/2908080.2908121
[20] Zhihao Jia, Oded Padon, James Thomas, Todd Warszawski, Matei Zaharia, and Alex Aiken. 2019. TASO: optimizing deep
     learning computation with automatic generation of graph substitutions. In Proceedings of the 27th ACM Symposium on
     Operating Systems Principles (Huntsville, Ontario, Canada) (SOSP ’19). Association for Computing Machinery, New
     York, NY, USA, 47–62. https://doi.org/10.1145/3341301.3359630
[21] Theodoros Kasampalis, Daejun Park, Zhengyao Lin, Vikram S. Adve, and Grigore Roşu. 2021. Language-Parametric
     Compiler Validation with Application to LLVM. In Proceedings of the 26th ACM International Conference on Architectural
     Support for Programming Languages and Operating Systems (Virtual, USA) (ASPLOS ’21). Association for Computing
     Machinery, New York, NY, USA, 1004–1019. https://doi.org/10.1145/3445814.3446751
[22] Jérémie Koenig and Zhong Shao. 2021. CompCertO: Compiling Certified Open C Components. In Proceedings of the 42nd
     ACM SIGPLAN International Conference on Programming Language Design and Implementation (Virtual, Canada) (PLDI
     2021). Association for Computing Machinery, New York, NY, USA, 1095–1109. https://doi.org/10.1145/3453483.3454097
[23] Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens. 2014. CakeML: a verified implementation
     of ML. In Proceedings of the 41st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (San
     Diego, California, USA) (POPL ’14). Association for Computing Machinery, New York, NY, USA, 179–191. https:
     //doi.org/10.1145/2535838.2535841
[24] Daniel Kästner, Ulrich Wünsche, Jörg Barrho, Marc Schlickling, Bernhard Schommer, Michael Schmidt, Christian
     Ferdinand, Xavier Leroy, and Sandrine Blazy. 2018. CompCert: Practical experience on integrating and qualifying a
     formally verified optimizing compiler. In ERTS 2018: Embedded Real Time Software and Systems. SEE. http://xavierleroy.
     org/publi/erts2018_compcert.pdf
[25] Amanda Liu, Gilbert Bernstein, Adam Chlipala, and Jonathan Ragan-Kelley. 2022. Verified Tensor-Program Optimization
     Via High-level Scheduling Rewrites. In POPL’22: Proceedings of the 49th ACM SIGPLAN-SIGACT Symposium on Principles
     of Programming Languages (Philadelphia, PA, USA). http://adam.chlipala.net/papers/AtlPOPL22/
[26] Amanda Liu, Gilbert Bernstein, Adam Chlipala, and Jonathan Ragan-Kelley. 2024. A Verified Compiler for a Functional
     Tensor Language. In PLDI’24: Proceedings of the 45th ACM SIGPLAN Conference on Programming Language Design and
     Implementation (Copenhagen, Denmark). http://adam.chlipala.net/papers/AtlPLDI24/
[27] Zhengyang Liu, Stefan Mada, and John Regehr. 2023. Minotaur: A SIMD-Oriented Synthesizing Superoptimizer.
     arXiv:2306.00229 [cs.PL] https://arxiv.org/abs/2306.00229
[28] Nuno P. Lopes, David Menendez, Santosh Nagarakatte, and John Regehr. 2015. Provably correct peephole optimizations
     with alive. In Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation
     (Portland, OR, USA) (PLDI ’15). Association for Computing Machinery, New York, NY, USA, 22–32. https://doi.org/10.
     1145/2737924.2737965
[29] Sirui Lu and Rastislav Bodík. 2023. Grisette: Symbolic Compilation as a Functional Programming Library. Proc. ACM
     Program. Lang. 7, POPL, Article 16 (jan 2023), 33 pages. https://doi.org/10.1145/3571209
[30] Julie L. Newcomb, Andrew Adams, Steven Johnson, Rastislav Bodik, and Shoaib Kamil. 2020. Verifying and improving
     Halide’s term rewriting system with program synthesis. Proc. ACM Program. Lang. 4, OOPSLA, Article 166 (nov 2020),
     28 pages. https://doi.org/10.1145/3428234
[31] Adam Paszke, Sam Gross, Soumith Chintala, Gregory Chanan, Edward Yang, Zachary DeVito, Zeming Lin, Alban
     Desmaison, Luca Antiga, and Adam Lerer. 2017. Automatic differentiation in PyTorch. In NIPS-W.
[32] Jonathan Ragan-Kelley, Connelly Barnes, Andrew Adams, Sylvain Paris, Frédo Durand, and Saman Amarasinghe.
     2013. Halide: a language and compiler for optimizing parallelism, locality, and recomputation in image processing
     pipelines. In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and Implementation
     (Seattle, Washington, USA) (PLDI ’13). Association for Computing Machinery, New York, NY, USA, 519–530. https:
     //doi.org/10.1145/2491956.2462176
[33] James Reed, Zachary DeVito, Horace He, Ansley Ussery, and Jason Ansel. 2022. torch.fx: Practical Program Cap-
     ture and Transformation for Deep Learning in Python. In Proceedings of Machine Learning and Systems, D. Mar-
     culescu, Y. Chi, and C. Wu (Eds.), Vol. 4. 638–651. https://proceedings.mlsys.org/paper_files/paper/2022/file/
     7c98f9c7ab2df90911da23f9ce72ed6e-Paper.pdf
[34] Raimondas Sasnauskas, Yang Chen, Peter Collingbourne, Jeroen Ketema, Gratian Lup, Jubi Taneja, and John Regehr.
     2018. Souper: A Synthesizing Superoptimizer. arXiv:1711.04422 [cs.PL] https://arxiv.org/abs/1711.04422



                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:32                                                                                                          Arora et al.


[35] Eric Schkufza, Rahul Sharma, and Alex Aiken. 2013. Stochastic superoptimization. SIGPLAN Not. 48, 4 (mar 2013),
     305–316. https://doi.org/10.1145/2499368.2451150
[36] Mary Sheeran, Satnam Singh, and Gunnar Stålmarck. 2000. Checking Safety Properties Using Induction and a SAT-
     Solver. In Formal Methods in Computer-Aided Design, Warren A. Hunt and Steven D. Johnson (Eds.). Springer Berlin
     Heidelberg, Berlin, Heidelberg, 127–144.
[37] Gus Henry Smith, Andrew Liu, Steven Lyubomirsky, Scott Davidson, Joseph McMahan, Michael Taylor, Luis Ceze, and
     Zachary Tatlock. 2021. Pure tensor program rewriting via access patterns (representation pearl). In Proceedings of the
     5th ACM SIGPLAN International Symposium on Machine Programming (Virtual, Canada) (MAPS 2021). Association for
     Computing Machinery, New York, NY, USA, 21–31. https://doi.org/10.1145/3460945.3464953
[38] Haojie Wang, Jidong Zhai, Mingyu Gao, Zixuan Ma, Shizhi Tang, Liyan Zheng, Yuanzhi Li, Kaiyuan Rong, Yuanyong
     Chen, and Zhihao Jia. 2021. PET: Optimizing Tensor Programs with Partially Equivalent Transformations and
     Automated Corrections. In 15th USENIX Symposium on Operating Systems Design and Implementation (OSDI 21).
     USENIX Association, 37–54. https://www.usenix.org/conference/osdi21/presentation/wang
[39] Yuting Wang, Pierre Wilke, and Zhong Shao. 2019. An Abstract Stack Based Approach to Verified Compositional
     Compilation to Machine Code. Proc. ACM Program. Lang. 3, POPL, Article 62 (jan 2019), 30 pages. https://doi.org/10.
     1145/3290375
[40] Yuting Wang, Ling Zhang, Zhong Shao, and Jérémie Koenig. 2022. Verified Compilation of C Programs with a Nominal
     Memory Model. Proc. ACM Program. Lang. 6, POPL, Article 25 (jan 2022), 31 pages. https://doi.org/10.1145/3498686
[41] Yichen Yang, Phitchaya Phothilimthana, Yisu Wang, Max Willsey, Sudip Roy, and Jacques Pienaar. 2021. Equal-
     ity Saturation for Tensor Graph Superoptimization. In Proceedings of Machine Learning and Systems, A. Smola,
     A. Dimakis, and I. Stoica (Eds.), Vol. 3. 255–268.       https://proceedings.mlsys.org/paper_files/paper/2021/file/
     cc427d934a7f6c0663e5923f49eba531-Paper.pdf
[42] Jianzhou Zhao, Santosh Nagarakatte, Milo M.K. Martin, and Steve Zdancewic. 2012. Formalizing the LLVM Intermediate
     Representation for Verified Program Transformations. In Proceedings of the 39th Annual ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages (Philadelphia, PA, USA) (POPL ’12). Association for Computing
     Machinery, New York, NY, USA, 427–440. https://doi.org/10.1145/2103656.2103709
[43] Jianzhou Zhao, Santosh Nagarakatte, Milo M.K. Martin, and Steve Zdancewic. 2013. Formal Verification of SSA-Based
     Optimizations for LLVM. In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and
     Implementation (Seattle, Washington, USA) (PLDI ’13). Association for Computing Machinery, New York, NY, USA,
     175–186. https://doi.org/10.1145/2491956.2462164




Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                       29:33


A    Extended Operator Semantics
We provide the denotational semantics for the following additional operators:
    • Pad: The pad operator performs low (𝑆𝑙 ), interior (𝑆𝑖 ), and high (𝑆ℎ ) padding on the input
      tensor.
                           let 𝑆 = Shape(𝑒)                          𝑆𝑖 ≥ 0
                let 𝐼 = 𝑆 + (𝑆 − 1) × 𝑆𝑖       let 𝐿 = 𝐼 + 𝑆𝑙    let 𝑆𝑜 = 𝐿 + 𝑆ℎ ≥ 0
                              𝐴 − 𝑆𝑙
               let 𝐴′ = 𝜆𝐴.             let 𝑛𝑜𝑡-𝑖𝑛𝑡-𝑝𝑎𝑑 = 𝜆𝐴. (𝐴 − 𝑆𝑙 ) % (𝑆𝑖 + 1) = 0
                              𝑆𝑖 + 1
                    let 𝑛𝑜𝑡-𝑝𝑎𝑑-𝑎𝑟𝑒𝑎 = 𝜆𝐴. 𝐴 ≥ 𝑆𝑙 ∧ 𝐴 < 𝐿 ∧ 𝑛𝑜𝑡-𝑖𝑛𝑡-𝑝𝑎𝑑 (𝐴)
                                                                                                        Pad
                                           ⟦pad(𝑒, 𝑣, 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 )⟧ =
              {𝐴 ↦→ if 𝑛𝑜𝑡-𝑝𝑎𝑑-𝑎𝑟𝑒𝑎(𝐴) then ⟦𝑒⟧ [𝐴′ (𝐴)] else 𝑣 | 𝐴 ∈ Access(𝑆𝑜 )}

    • Dot: The dot operator performs sum-of-products over the specified set of contracting
      aggregated-axes (𝑋𝑐 ). 𝑋𝑏 denotes the set of batch aggregated-axes that stay independent
      across the computation. For this operation to be valid, 𝑋𝑐 and 𝑋𝑏 must be disjoint, and 𝑋𝑐 ∪𝑋𝑏
      is the set of exactly those aggregated-axes which are common in the input tensors 𝑒 1 and 𝑒 2 .
      For verification purposes, we describe the semantics of the dot operator by first expanding
      the two tensors to the same shape, followed by an element-wise multiplication, and then
      reducing on the contracting aggregated-axes. The remaining set of aggregated-axes in 𝑒 1 ,
      i.e., 𝑆 1 \ 𝑆 1 |𝑋𝑐 ∪𝑋𝑏 , and in 𝑒 2 , i.e., 𝑆 2 \ 𝑆 2 |𝑋𝑐 ∪𝑋𝑏 , also called the spatial-axes, need to be disjoint.
      This condition is implicit in the expand operator below.

                let 𝑆 1 = Shape(𝑒 1 )                               let 𝑆 2 = Shape(𝑒 2 )
               𝑋𝑐 ∪ 𝑋𝑏 = Axes(𝑒 1 ) ∩ Axes(𝑒 2 )                             𝑋𝑐 ∩ 𝑋𝑏 = ∅
    let 𝑡 = ⟦reduce(+, binary(×, expand(𝑒 1, 𝑆 2 \ 𝑆 2 |𝑋𝑐 ∪𝑋𝑏 ), expand(𝑒 2, 𝑆 1 \ 𝑆 1 |𝑋𝑐 ∪𝑋𝑏 )), 𝑋𝑐 )⟧
                                                                                                                  Dot
                                          ⟦dot(𝑒 1, 𝑒 2, 𝑋𝑐 , 𝑋𝑏 )⟧ = 𝑡

    • Conv: We first model a basic convolution operator without padding and dilation. This can be
      expressed on top of slice (for extracting the window) and dot (dot product of the window
      and the kernel) operators. Then we express the general convolution operator by using the
      base operator with the pad operator. In the inference rules, the subscript 𝑖 relates to the
      input and the subscript 𝑤 relates to the weights. 𝑋𝑏 , 𝑋𝑜 , 𝑋 𝑓 , and 𝑋𝑠𝑝 are the sets of batch,
      output-feature, input-feature, and spatial aggregated-axes, respectively.

          let 𝑆𝑖 = Shape(𝑒𝑖 )                 let 𝑆 𝑤 = Shape(𝑒 2 )           let 𝑋𝑖 = Axes(𝑒𝑖 )
            let 𝑋 𝑤 = Axes(𝑒 𝑤 )                    𝑋𝑏 = 𝑋𝑖 \ 𝑋 𝑤               𝑋𝑜 = 𝑋 𝑤 \ 𝑋 𝑖
           𝐹 ⊆ 𝑋𝑖 ∩ 𝑋 𝑤                let 𝑋𝑠𝑝 = 𝑋𝑖 \ (𝑋𝑏 ∪ 𝑋 𝑓 )               dom(𝐼𝑝 ) = 𝑋𝑠𝑝
                                                           𝑆𝑖 |𝑋𝑠𝑝 − 𝑆 𝑤 |𝑋𝑠𝑝
                                                                                
                         let 𝑆 ′ = 𝑆𝑖 |𝑋𝑏 ∪ 𝑆 𝑤 |𝑋𝑜 ∪                         +1
                                                                  𝐼𝑝                            
      let 𝑠𝑢𝑏 = 𝜆𝐴𝑠𝑝 . dot(slice(𝑒𝑖 , 𝐴𝑠𝑝 × 𝐼𝑝 , 𝐴𝑠𝑝 × 𝐼𝑝 + 𝑆 𝑤 |𝑋𝑠𝑝 , 1), 𝑒 𝑤 , 𝑋 𝑓 ∪ 𝑋𝑠𝑝 , ∅)
                                                                                                            ConvBase
     conv-base(𝑒𝑖 , 𝑒 𝑤 , 𝑋𝑏 , 𝑋 𝑓 , 𝑋𝑜 , 𝐼𝑝 ) = {𝐴 ↦→ 𝑠𝑢𝑏 (𝐴|𝑋𝑠𝑝 ) [𝐴|𝑋𝑏 ∪𝑋𝑜 ] | 𝐴 ∈ Access(𝑆 ′ )}

       The conv operator uses the conv-base operator by padding its operands with the specified
       arguments. Note that the inputs 𝑆𝑖 and 𝑆𝑖′ to the conv operator denote dilations, which are
       the actual padding amounts incremented by 1. Therefore, we appropriately subtract 1 from

                                Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:34                                                                                                         Arora et al.


        these attributes before passing them to the pad operator.
                                                                                                   
           conv-base(pad(𝑒 1, 0, 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 − 1), pad(𝑒 2, 0, 0, 0, 𝑆𝑖′ − 1), 𝑋𝑏 , 𝑋 𝑓 , 𝑋𝑜 , 𝐼𝑝 ) = 𝑡
                                                                                                           Conv
                            conv(𝑒𝑖 , 𝑒 𝑤 , 𝑋𝑏 , 𝑋 𝑓 , 𝑋𝑜 , 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 , 𝑆𝑖′, 𝐼𝑝 ) = 𝑡
    • Reverse: The reverse operator reverses the order of elements in the input tensor along the
      specified set of aggregated-axes 𝑋𝑟 .
                                let 𝑆 = Shape(𝑒)       𝑋𝑟 ⊆ Axes(𝑒)
                             let 𝐴′ = 𝜆𝐴. (𝐴 𝐴|𝑋𝑟 ) ∪ (𝑆 |𝑋𝑟 − 𝐴|𝑋𝑟 − 1)
                                                                                              Reverse
                     ⟦reverse(𝑒, 𝑋𝑟 )⟧ = {𝐴 ↦→ ⟦𝑒⟧ [𝐴′ (𝐴)] | 𝐴 ∈ Access(𝑆)}
    • Select: The select operator constructs an output tensor from elements of two input tensors
      𝑒 1 and 𝑒 2 , based on the values of a predicate tensor 𝑒𝑏 . This operator is only valid if 𝑒𝑏 contains
      elements of type Bool and 𝑒 1, 𝑒 2 contain elements of the same type.
                               Shape(𝑒𝑏 ) = Shape(𝑒 1 ) = Shape(𝑒 2 )
                            DType(𝑒𝑏 ) = Bool  DType(𝑒 1 ) = DType(𝑒 2 )
                                                                                                    Select
                                            ⟦select(𝑒𝑏 , 𝑒 1, 𝑒 2 )⟧ =
                {𝐴 ↦→ if ⟦𝑒𝑏 ⟧ [𝐴] then ⟦𝑒 1 ⟧ [𝐴] else ⟦𝑒 2 ⟧ [𝐴] | 𝐴 ∈ Access(𝑒)}
    • Clamp: The clamp operator clamps the input tensor (𝑒) to within the range specified by the
      minimum (𝑒𝑚𝑖𝑛 ) and maximum (𝑒𝑚𝑎𝑥 ) tensors.
                              Shape(𝑒𝑚𝑖𝑛 ) = Shape(𝑒) = Shape(𝑒𝑚𝑎𝑥 )
                            ⟦binary(min, binary(max, 𝑒, 𝑒𝑚𝑖𝑛 ), 𝑒𝑚𝑎𝑥 )⟧ = 𝑡
                                                                                          Clamp
                                        ⟦clamp(𝑒𝑚𝑖𝑛 , 𝑒, 𝑒𝑚𝑎𝑥 )⟧ = 𝑡
    • ReduceSI: The reduce operator takes a tensor and a set of aggregated-axes 𝑋 as inputs and
      returns a tensor which contains uninterpreted reduction elements. The resulting tensor has
      the shape 𝑆 \ 𝑆 |𝑋 , essentially removing all the aggregated-axes in 𝑋 . This results in the
      following semantics:
                    let 𝑆 = Shape(𝑒)            let {𝑥 0 · · · 𝑥𝑘 } = 𝑋 ⊆ Axes(𝑒)
                  let 𝑎𝑐𝑐 = 𝜆𝐴.Red𝐼⊕0,··· ,𝐼𝑘 ⟦𝑒⟧ [{𝑥 0 ↦→ 𝐼 0, · · · , 𝑥𝑘 ↦→ 𝐼𝑘 } ∪ 𝐴]
                                                                                             ReduceOrig
                  ⟦reduce(⊕, 𝑒, 𝑋 )⟧ = {𝐴 ↦→ 𝑎𝑐𝑐 (𝐴) | 𝐴 ∈ Access(𝑆 \ 𝑆 |𝑋 )}
        The indices 𝐼 0, · · · , 𝐼𝑘 in the function 𝑎𝑐𝑐 are symbolic reduction indices, hence making the
        reduction element uninterpreted. The term ⟦𝑒⟧ [{𝑥 0 ↦→ 𝐼 0, · · · , 𝑥𝑘 ↦→ 𝐼𝑘 } ∪ 𝐴] represents a
        (multi-)set containing elements obtained by instantiating the indices 𝐼 0, · · · , 𝐼𝑘 with concrete-
        maps. As the sizes of reduced axes are unbounded, we cannot compute this set of elements
        and hence cannot expand the reduction to sum all the elements being reduced. Thus, we leave
        the sum uninterpreted and provide special treatment for such elements during verification.
        Verifying rules with reductions would involve proving equivalence of reduction elements.
        Proving the equivalence of two reduction elements Red𝑋 𝑓 (𝑋 ) and Red𝑌 𝑔(𝑌 ) can often be
        done by showing that the LHS and RHS are sums of the same values, i.e., 𝑓 (𝑋 ) and 𝑔(𝑌 )
        represent the same (multi-)set. One way to prove set equivalence is to establish a bijection
        between 𝑋 and 𝑌 and show each pair of values in 𝑓 (𝑋 ) and 𝑔(𝑌 ) are equal, regardless of
        tensor instantiation and operator attributes.
        In TensorRight, the user provides a relation between 𝑋 and 𝑌 as a hint. As we see in
        ReduceOrig, 𝑋 and 𝑌 contain symbolic indices. The current semantics suggest that we have
        to generate fresh symbolic variables for each invocation of reduce. However, this precludes

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:35


       the user from defining hints as they cannot refer to these indices. To solve this problem, we
       provide the symbolic reduction indices as input to the operator semantics. One can think of
       these extra arguments as symbolic names, based on which we can define relations between
       them. The modified semantics are shown below.
                   let 𝑆 = Shape(𝑒)     let {𝑥 0 ↦→ 𝑆𝐼 0, · · · , 𝑥𝑘 ↦→ 𝑆𝐼𝑘 } = 𝑆𝐼
                                  let 𝑋 = dom(𝐼 ) ⊆ Axes(𝑒)
                                              ⊕
                            let 𝑎𝑐𝑐 = 𝜆𝐴.Red𝑆𝐼  0 ,··· ,𝑆𝐼𝑘
                                                            ⟦𝑒⟧ [𝑆𝐼 ∪ 𝐴]
                                                                                            ReduceSI
                  ⟦reduce(⊕, 𝑒, 𝑆𝐼 )⟧ = {𝐴 ↦→ 𝑎𝑐𝑐 (𝐴) | 𝐴 ∈ Access(𝑆 \ 𝑆 |𝑋 )}
       The reduce operator now takes an aggregated-map 𝐼 as input, instead of the set of aggregated-
       axes to reduce. 𝐼 contains the symbolic reduction indices 𝑆𝐼 0, · · · , 𝑆𝐼𝑘 , which are used the
       construct the uninterpreted reduction element. For any rewrite rule with reductions, the user
       can now use these supplied reduction indices from LHS and RHS to define hints, also called
       si-relations (symbolic-index relations).

B   Validity of Rewrite Rules
Given the semantics of TensorRight DSL, we now define what it means for a rewrite rule to
be valid. Fig. 12 lists all the tensor operators supported in TensorRight DSL. As a part of our
verification methodology, we symbolically execute all operator semantics and generate symbolic
representations of the LHS and RHS expressions. The validity condition of a rewrite rule is simply
the assertion of equality between the LHS and RHS expressions, under the specified precondition.
We now formalize this notion.
Definition 6 (Valid Rewrite Rule). A rewrite rule LHS ⇒𝐶 RHS is valid if and only if
                          ∀𝑣 ∈ 𝑣𝑎𝑟𝑠, 𝐶 ∧ valid-expr(LHS) → ⟦LHS⟧ = ⟦RHS⟧                                         (12)
where 𝑣𝑎𝑟𝑠 is the set of all variables appearing in the rewrite rule, such as tensor variables and
operator attributes. The predicate valid-expr takes a tensor expression and returns a condition
under which the expression is valid. It is defined inductively on the structure of tensor expressions,
collecting all assertions from the operator semantics, as shown in Fig. 13.
   Definition 6 states that a rewrite rule must be valid for all valuations of all the variables appearing
in a rewrite rule. Note that we only consider valuations where the term prior to rewriting is valid,
i.e., when LHS is valid. The inner equality ⟦LHS⟧ = ⟦RHS⟧ asserts that, once all the variables are
instantiated, the resulting tensors on both sides are equal. §G extends this definition to account for
validity of the RHS expression.
   Based on the denotational semantics of operators in TensorRight DSL, we can symbolically
compute the shape of any tensor expression as a function of the shapes of input tensors and
operator attributes. We only consider rewrite rules where under the precondition, the LHS and
RHS expressions have the same shape, since the rule would be invalid if the shapes do not match.
Under this assumption, semantic validity reduces to a pointwise equality of tensor values:
          ∀𝑣 ∈ 𝑣𝑎𝑟𝑠, 𝐶 ∧ valid-expr(LHS) → ∀𝐴 ∈ Access(LHS), ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴]                               (13)
Definition 7 (Invalid Rewrite Rule). A rewrite rule LHS ⇒𝐶 RHS is invalid if and only if
          ∃𝑣 ∈ 𝑣𝑎𝑟𝑠, 𝐶 ∧ valid-expr(LHS) ∧ ∃𝐴 ∈ Access(LHS), ⟦LHS⟧ [𝐴] ≠ ⟦RHS⟧ [𝐴]
where 𝑣𝑎𝑟𝑠 is the set of variables appearing in the rewrite rule.
  Definition 7 states that if a rewrite rule is invalid, then there exists some valuation of all variables
and an access 𝐴, such that (1) the precondition is true, (2) LHS is valid, and (3) LHS and RHS do

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:36                                                                                                           Arora et al.


              𝜏        ≔    Int | Bool | Real                                          Type
              𝑎        ∈    A                                                          Named-axes
              𝑥        ∈    X = P (A)                                                  Aggregated-axes
              𝑓        ∈    list[Int] → Int                                            Map function
              𝑚        ≔    M | fmap(𝑓 , 𝑚+)                                           Maps
              𝑋        ∈    P (X)                                                      Set of aggregated-axes
              𝑆, 𝐼     ∈    𝑚X                                                         Shapes and indices
              𝑅        ∈    XX                                                         Relabel maps
              𝑣        ≔    𝑖 : Int | 𝑏 : Bool | 𝑟 : Real                              Scalar literal
              𝑒        ≔    T (Literal)                                                Tensor expression
                       |    V (Variable)
                       |    const(𝑣, 𝑆)
                       |    iota(𝑆, 𝑥)
                       |    expand(𝑒, 𝑆)
                       |    binary(⊕, 𝑒𝑙 , 𝑒𝑟 )
                       |    pad(𝑒, 𝑣, 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 )
                       |    slice(𝑒, 𝐼𝑠 , 𝐼𝑒 , 𝐼𝑝 )
                       |    dy-slice(𝑒, 𝐼, 𝑆)
                       |    dyup-slice(𝑒, 𝑒𝑢 , 𝐼 )
                       |    reduce(⊕, 𝑒, 𝐼 )
                       |    relabel(𝑒, 𝑅)
                       |    concat(𝑒𝑙 , 𝑒ℎ , 𝑥)
                       |    conv-base(𝑒𝑖 , 𝑒 𝑤 , 𝑋𝑏 , 𝑋 𝑓 , 𝑋𝑜 , 𝐼𝑝 )
                       |    conv(𝑒𝑖 , 𝑒 𝑤 , 𝑋𝑏 , 𝑋 𝑓 , 𝑋𝑜 , 𝑆𝑙 , 𝑆ℎ , 𝑆𝑖 , 𝑆𝑖′, 𝐼𝑝 )
                       |    dot(𝑒 1, 𝑒 2, 𝑋𝑐 , 𝑋𝑏 )
                       |    clamp(𝑒𝑚𝑖𝑛 , 𝑒, 𝑒𝑚𝑎𝑥 )
                       |    select(𝑒𝑏 , 𝑒 1, 𝑒 2 )
                       |    reverse(𝑒, 𝑋𝑟 )
              𝑔        ∈    list[Int] → Bool                                           Predicate function
              𝑃        ≔    fold(𝑔, 𝑚+)                                                Precondition
              𝑅𝑢𝑙𝑒     ≔    𝑒𝑙ℎ𝑠 ⇒𝑃 ∗ 𝑒𝑟ℎ𝑠                                             Rewrite rule

                      Fig. 12. Core rewrite rule representation with extended operators.


not match at the access 𝐴. Such a valuation of variables and the access 𝐴 together comprise a
counterexample for the rule.

C Preliminaries
In §B, we defined what it means for a rewrite rule to be valid (Equation 12). A key challenge is
that rewrite rules must apply to tensors with arbitrary ranks and arbitrary sizes along each axis.
Thus, we must verify rewrite rules in the unbounded setting, where both the number of axes (rank)
and the size along each axis are unbounded. To handle arbitrary number of axes, we partition the
named-axes of a tensor into finite groups or classes, called aggregated-axes, where each aggregated-
axis can be instantiated to any rank. Once the aggregated-axes in a rewrite rule are instantiated, we
obtain a concrete-rank instantiation of the rule, though the sizes along each axis remain unbounded.
Verifying the rewrite rule in the unbounded setting therefore reduces to verifying the rule for all
valid instantiations of the aggregated-axes. In this section, we present our key observation (§C.2),

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:37

Basis:
                     valid-expr(𝑡) ≔ true                                                 𝑡∈T
                     valid-expr(𝑣𝑎𝑟 ) ≔ Shape(𝑣𝑎𝑟 ) ≥ 0                               𝑣𝑎𝑟 ∈ V
                     valid-expr(const(𝑣, 𝑆)) ≔ 𝑆 ≥ 0
                     valid-expr(iota(𝑆, 𝑥)) ≔ 𝑆 ≥ 0 ∧ 𝑥 ∈ 𝑆


Induction Step:
        valid-expr(expand(𝑒, 𝑆)) ≔ valid-expr(𝑒) ∧ 𝑆 ≥ 0 ∧ dom(𝑆) ∩ Axes(𝑒) = ∅
        valid-expr(binary(⊕, 𝑒𝑙 , 𝑒𝑟 )) ≔ valid-expr(𝑒𝑙 ) ∧ valid-expr(𝑒𝑟 ) ∧ Shape(𝑒𝑙 ) = Shape(𝑒𝑟 )
        valid-expr(slice(𝑒, 𝐼𝑠 , 𝐼𝑒 , 𝐼𝑝 )) ≔ valid-expr(𝑒) ∧ 0 ≤ 𝐼𝑠 ≤ 𝐼𝑒 ≤ Shape(𝑒) ∧ 𝐼𝑝 > 0
        valid-expr(dy-slice(𝑒, 𝐼, 𝑆)) ≔ valid-expr(𝑒) ∧ 𝐼 + 𝑆 ≤ Shape(𝑒) ∧ 𝑆 > 0 ∧ 𝐼 ≥ 0
                                     ..
                                      .

Fig. 13. The predicate valid-expr is defined inductively over the structure of tensor expressions. Other cases
follow similarly, derived from the operator semantics.


and in §D we show how TensorRight verifies any rewrite rule for a possibly infinite number of
instantiations.

C.1      Assumptions
To simplify the discussion, we make the following assumptions, which will be relaxed later. Let
LHS ⇒𝐶 RHS be a rewrite rule such that:
      • The rewrite rule contains only one input tensor, denoted X
      • X contains exactly one aggregated-axis, say 𝑥, which has the RClass 𝑐, i.e. 𝑥 : 𝑐.
      • The rewrite rule does not contain any reduce, relabel, expand, dot, conv-base, and conv
        operators: these operators can add, remove or rename aggregated-axes. For now, we keep
        the discussion restricted to a single aggregated-axis.

C.2      Observation
We can symbolically execute any rewrite rule LHS ⇒𝐶 RHS under a general access 𝐴 using the
operator semantics. We observe that the equality ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] (the inner equality in
Equation 13) can always be expressed in the following canonical form:
                      scalarf (X[𝑥 ↦→ fmap(𝑒 1, M1 )], · · · , X[𝑥 ↦→ fmap(𝑒𝑛 , M𝑛 )],
                               fold(𝑔1, N1 ), · · · , fold(𝑔𝑚 , N𝑚 ))                                            (14)
   We now illustrate, through examples, how symbolic evaluation of rewrite rules results in expres-
sions of this form.

C.3      Symbolic Evaluation Examples
C.3.1     Pad-Low.
  Setting. Let 𝑥 : 𝑐 be an aggregated-axis with RClass 𝑐. It can be instantiated to an arbitrary
number of named-axes. Let X be a tensor with shape {𝑥 ↦→ 𝑠}, where 𝑠 contains sizes of named-axes

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:38                                                                                         Arora et al.


in 𝑥. Let the rewrite rule in consideration be,

                                     pad-low(X, 0, 𝑆𝑙 ) ⇒ pad-low(X, 1, 𝑆𝑙 )

where 𝑆𝑙 = {𝑥 ↦→ 𝑠𝑙 } and 𝑠𝑙 contains padding sizes of named-axes in 𝑥. The difference between
LHS and RHS is that the former is padded with a value of 0, while the latter is padded with a value
of 1. Therefore, this rewrite rule is invalid.

   Shape of the Output Tensors. We compute the shape of the LHS (same as RHS) as follows:

                              Shape(pad-low(X, 0, 𝑆𝑙 )) = Shape(X) + 𝑆𝑙
                                                             = {𝑥 ↦→ 𝑠} + {𝑥 ↦→ 𝑠𝑙 }
                                                             = {𝑥 ↦→ 𝑠 + 𝑠𝑙 }

  Therefore, an arbitrary, valid access 𝐴 on the output tensors has the form 𝐴 = {𝑥 ↦→ 𝑎}, where
𝑎 contains the index-values for the named-axes in 𝑥. We symbolically evaluate the expression
⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] under the access 𝐴:

                           ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴]
                       ⇔ (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴) then X[𝑥 ↦→ (𝑎 − 𝑠𝑙 )] else 0) =
                                          (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴) then X[𝑥 ↦→ (𝑎 − 𝑠𝑙 )] else 1)

   We express the above in the canonical form given by Equation 14, as follows:
                                             df
                                     𝑒 (𝑣, 𝑙) = 𝑣 − 𝑙
                                             df
                                          𝑦 = X[𝑥 ↦→ fmap(𝑒, [𝑎, 𝑠𝑙 ])] = X[𝑥 ↦→ 𝑎 − 𝑠𝑙 ]
                                             df
                                     𝑔(𝑣, 𝑙) = 𝑣 ≥ 𝑙
                                             df
                                           𝑏 = 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴) = 𝐴 ≥ 𝑆𝑙
                                             = 𝑎 ≥ 𝑠𝑙 = fold(𝑔, [𝑎, 𝑠𝑙 ])
                                             df
                             scalarf (𝑦, 𝑏) = (if 𝑏 then 𝑦 else 0) = (if 𝑏 then 𝑦 else 1)
                                             df
             ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] = scalarf (X[𝑥 ↦→ fmap(𝑒, [𝑎, 𝑠𝑙 ])], fold(𝑔, [𝑎, 𝑠𝑙 ]))

C.3.2    Slice.

   Setting. Let 𝑥 : 𝑐 be an aggregated-axis with RClass 𝑐. It can be instantiated to an arbitrary
number of named-axes. Let X be a tensor with shape {𝑥 ↦→ 𝑠}, where 𝑠 contains sizes of named-axes
in 𝑥. Let the rewrite rule in consideration be,

                                  slice(pad-low(X, 0, 𝑆𝑙 ), 𝑆𝑙 , 𝑆 + 𝑆𝑙 , 𝑆𝑝 ) ⇒ X

where 𝑆 = Shape(X), 𝑆𝑙 = {𝑥 ↦→ 𝑠𝑙 }, and 𝑆𝑝 = {𝑥 ↦→ 1}.
    The LHS first pads the input tensor by 0 with padding sizes 𝑠𝑙 . It then slices the resulting tensor
by removing 𝑠𝑙 elements from the beginning along every named-axis, while skipping no elements
till the end. It is easy to see that the LHS is a no-op since it adds padding values and then removes
them. The RHS is simply the input tensor. Therefore, this rewrite rule is valid.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                          29:39


  Shape of the output tensors. We compute the shape of the LHS (same as RHS) as follows:
                        Shape(slice(pad-low(X, 0, 𝑆𝑙 ), 𝑆𝑙 , 𝑆 + 𝑆𝑙 , 𝑆𝑝 ) = 𝑆 + 𝑆𝑙 − 𝑆𝑙
                                                                                =𝑆
                                                                                = {𝑥 ↦→ 𝑠}
  Therefore, an arbitrary, valid access 𝐴 on the output tensors has the form 𝐴 = {𝑥 ↦→ 𝑎}, where
𝑎 contains the index-values for the named-axes in 𝑥. We symbolically evaluate the expression
⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] under the access 𝐴:
                          ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴]
                      ⇔ ⟦pad(X, 0, 𝑆𝑙 )⟧ [𝑆𝑙 + 𝐴] = X[𝐴]
                      ⇔ (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝑆𝑙 + 𝐴) then X[(𝐴 + 𝑆𝑙 ) − 𝑆𝑙 ] else 0) = X[𝐴]
                      ⇔ (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝑆𝑙 + 𝐴) then X[𝐴] else 0) = X[𝐴]
  We express the above in the canonical form given by Equation 14, as follows:
                                             df
                                       𝑒 (𝑣) = 𝑣
                                             df
                                          𝑦 = X[𝑥 ↦→ fmap(𝑒, [𝑎])] = X[𝑥 ↦→ 𝑎]
                                             df
                                     𝑔(𝑣, 𝑙) = 𝑣 + 𝑙 ≥ 𝑙
                                             df
                                          𝑏 = 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴 + 𝑆𝑙 ) = 𝐴 + 𝑆𝑙 ≥ 𝑆𝑙
                                             = 𝑎 + 𝑠𝑙 ≥ 𝑠𝑙 = fold(𝑔, [𝑎, 𝑠𝑙 ])
                                             df
                              scalarf (𝑦, 𝑏) = (if 𝑏 then 𝑦 else 0) = 𝑦
                                             df
              ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] = scalarf (X[𝑥 ↦→ fmap(𝑒, [𝑎])], fold(𝑔, [𝑎, 𝑠𝑙 ]))
C.3.3   Multiple RClasses.
  Setting. Let 𝑥 1 : 𝑐 1 and 𝑥 2 : 𝑐 2 be aggregated-axes with RClasses 𝑐 1 and 𝑐 2 respectively. They can
be instantiated to an arbitrary number of named-axes. Let X be a tensor with shape {𝑥 1 ↦→ 𝑠 1 },
where 𝑠 1 contains sizes of named-axes in 𝑥 1 .
  Let the rewrite rule rule in consideration be,
           pad-low(expand(X, {𝑥 2 ↦→ 𝑠 2 }), 0, 𝑆𝑙1 ) ⇒ expand(pad-low(X, 0, 𝑆𝑙2 ), {𝑥 2 ↦→ 𝑠 2 })
   where 𝑆𝑙1 = {𝑥 1 ↦→ 𝑠𝑙 , 𝑥 2 ↦→ 0}, 𝑆𝑙2 = {𝑥 1 ↦→ 𝑠𝑙 }, and 𝑠𝑙 contains padding sizes for named-axes
in 𝑥 1 . The LHS first expands the tensor X with a new aggregated-axis 𝑥 2 and then low-pads 𝑥 1
with 𝑠𝑙 and leaves 𝑥 2 unchanged. The RHS first low-pads 𝑥 1 with 𝑠𝑙 and then expands with a new
aggregated-axis 𝑥 2 . This is a valid rewrite rule since LHS does not pad 𝑥 2 after the expansion, while
RHS simply replicates the data across 𝑥 2 .
  Shape of the output tensors. We compute the shape of the LHS (same as RHS) as follows:
     Shape(pad-low(expand(X, {𝑥 2 ↦→ 𝑠 2 }), 0, 𝑆𝑙1 )) = Shape(expand(X, {𝑥 2 ↦→ 𝑠 2 })) + 𝑆𝑙1
                                                               = Shape(X) ∪ {𝑥 2 ↦→ 𝑠 2 } + 𝑆𝑙1
                                                               = {𝑥 1 ↦→ 𝑠 1, 𝑥 2 ↦→ 𝑠 2 } + {𝑥 1 ↦→ 𝑠𝑙 , 𝑥 2 ↦→ 0}
                                                               = {𝑥 1 ↦→ 𝑠 1 + 𝑠𝑙 , 𝑥 2 ↦→ 𝑠 2 }

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:40                                                                                                   Arora et al.


     Therefore, an arbitrary, valid access 𝐴 on the output tensors has the form 𝐴 = {𝑥 1 ↦→ 𝑎 1, 𝑥 2 ↦→
𝑎 ! }, where 𝑎 1 and 𝑎 2 contain the index-values for the named-axes in 𝑥 1 and 𝑥 2 respectively. We
symbolically evaluate the expression ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] under the access 𝐴:
                     ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴]
                 ⇔ (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴) then ⟦expand(X, {𝑥 2 ↦→ 𝑠 2 })⟧ [𝐴 − 𝑆𝑙1 ] else 0) =
                                             ⟦pad-low(X, 0, 𝑆𝑙2 )⟧ [𝐴|𝑥 1 ]
                 ⇔ (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴) then X[(𝐴 − 𝑆𝑙1 )|𝑥 1 ] else 0) =
                                             (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴|𝑥 1 ) then X[𝐴|𝑥 1 − 𝑆𝑙2 ] else 0)
                 ⇔ (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴) then X[𝑥 1 ↦→ 𝑎 1 − 𝑠𝑙 ] else 0) =
                                             (if 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴|𝑥 1 ) then X[𝑥 1 ↦→ 𝑎 1 − 𝑠𝑙 ] else 0)
    We express the above in the canonical form given by Equation 14, as follows:
                                       df
                               𝑒 (𝑣, 𝑙) = 𝑣 − 𝑙
                                       df
                                     𝑦 = X[𝑥 1 ↦→ fmap(𝑒, [𝑎 1, 𝑠𝑙 ])] = X[𝑥 1 ↦→ 𝑎 1 − 𝑠𝑙 ]
                                       df
                              𝑔1 (𝑣, 𝑙) = 𝑣 ≥ 𝑙
                                       df
                              𝑔2 (𝑣, 𝑙) = 𝑣 ≥ 0
                                       df
                                    𝑏 1 = 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴) = 𝐴 ≥ 𝑆𝑙1
                                       = 𝑎 1 ≥ 𝑠𝑙 ∧ 𝑎 2 ≥ 0 = fold(𝑔1, [𝑎 1, 𝑠𝑙 ]) ∧ fold(𝑔2, [𝑎 2 ])
                                       df
                                    𝑔3 = true
                                       df
                                    𝑏 2 = 𝑛𝑜𝑡-𝑝𝑎𝑑 (𝐴|𝑥 1 ) = 𝑎 1 ≥ 𝑠𝑙
                                       = 𝑎 1 ≥ 𝑠𝑙 ∧ true = fold(𝑔1, [𝑎 1, 𝑠𝑙 ]) ∧ fold(𝑔3, [])
                                       df
                   scalarf (𝑦, 𝑏 1, 𝑏 2 ) = (if 𝑏 1 then 𝑦 else 0) = (if 𝑏 2 then 𝑦 else 0)
                                       df
         ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] = scalarf (fmap(𝑒, [𝑎 1, 𝑠𝑙 ]), fold(𝑔1, [𝑎 1, 𝑠𝑙 ]) ∧ fold(𝑔2, [𝑎 2 ]),
                                                        fold(𝑔1, [𝑎 1, 𝑠𝑙 ]) ∧ fold(𝑔3, []))
   Here, the condition 𝑏 2 has been “padded” with a trivial fold over the aggregated-axis 𝑥 2 , using
a constant predicate function 𝑔3 = true. This notational convention ensures that each condition
contains exactly one fold per aggregated-axis, some of which may be trivial. Such trivial folds are
introduced for uniformity and can be safely removed during postprocessing.
C.3.4 Key Takeaway. The observation that rewrite rules in TensorRight DSL can be symbolically
evaluated and expressed in the form given by Equation 14, extends to all rewrite rules in the
language. This generalization can be formally proven by induction on the structure of tensor
expressions. We omit the proof, as the structure of the argument follows directly from the operator
semantics.

D       Scalar Function Explained
In §C.3, we illustrated through examples how any rewrite rule LHS ⇒𝐶 RHS in TensorRight
DSL can be symbolically evaluated under a general access 𝐴 using the operator semantics. The
assumptions from §C.1 still apply here and will be incrementally relaxed in later sections. The

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:41


equality ⟦LHS⟧ [𝐴] = ⟦RHS⟧ [𝐴] can be expressed in the following form:
                      scalarf (X[𝑥 ↦→ fmap(𝑒 1, M1 )], · · · , X[𝑥 ↦→ fmap(𝑒𝑛 , M𝑛 )],
                               fold(𝑔1, N1 ), · · · , fold(𝑔𝑚 , N𝑚 ))
  We explain each component below:
   • X[_]: this represents an access to the tensor X.
   • 𝑥 ↦→ fmap(𝑒𝑖 , M𝑖 ): this represents the access expression for the 𝑖 th access to X. Since X has
     only one aggregated-axis 𝑥, the access expression contains the same aggregated-axis, with
     the access map fmap(𝑒𝑖 , M𝑖 ).
     The fmap construct takes a function and applies it pointwise to a list of maps with the same
     domain. It as defined a follows:
                  fmap(𝑓 , [𝑚 1, 𝑚 2, · · · ]) = {𝑖 ↦→ 𝑓 (𝑚 1 (𝑖), 𝑚 2 (𝑖), · · · ) | 𝑖 ∈ dom(𝑚 1 )}
       For example, if M = [{𝑖 ↦→ 𝑣𝑖 , 𝑗 ↦→ 𝑣 𝑗 }, {𝑖 ↦→ 𝑙𝑖 , 𝑗 ↦→ 𝑙 𝑗 }] and 𝑓 = 𝜆𝑣, 𝑙 .(𝑣 − 𝑙), then
       fmap(𝑓 , M) = {𝑖 ↦→ 𝑣𝑖 − 𝑙𝑖 , 𝑗 ↦→ 𝑣 𝑗 − 𝑙 𝑗 }.
       Here, M𝑖 is the list of maps used in the 𝑖 th access, which include access maps, attribute
       maps, etc. Each function 𝑒𝑖 is independent of the rank of 𝑥, and only the maps in M𝑖 vary
       with the rank of 𝑥. Thus, we are able to capture all the rank-independent information in the
       function 𝑒𝑖 . We refer to 𝑒𝑖 as an index transformer because it transforms output index-values
       to input index-values. For the fmap construct to be well-formed, the arity of 𝑒𝑖 must match
       the number of maps in M𝑖 .
       When X has multiple aggregated-axes, each access must have separate access maps for each
       aggregated-axis. For example, if Axes(X) = {𝑥 1, · · · , 𝑥 𝑝 }, then the 𝑖 th access to X has the
       following form:
                          X[𝑥 1 ↦→ fmap( 1𝑒𝑖 , 1 M𝑖 ), · · · , 𝑥 𝑝 ↦→ fmap(𝑝 𝑒𝑖 , 𝑝 M𝑖 )]
      where 𝑗 𝑒𝑖 denotes the index transformer for 𝑥 𝑗 in the 𝑖 th access, and 𝑗 M𝑖 is the corresponding
      list of maps. Each 𝑗 𝑒𝑖 may vary across different aggregated-axes. However, it is applied to all
      named-axes uniformly in a given aggregated-axis.
    • fold(𝑔 𝑗 , N𝑗 ): these represent boolean values, referred to as conditions, that appear within
      if-then-else blocks. These conditions capture the dependency of output tensor values on the
      input tensor values and originate directly from the operator semantics. For instance, 𝑛𝑜𝑡-𝑝𝑎𝑑
      in the pad semantics (Pad) takes an access 𝐴 and determines if it lies in the padded area or
      not.
      The fold construct takes a predicate and applies it pointwise to a list of maps with the same
      domains. It returns true if all predicate values are true, and false otherwise. It is defined as:
                                                        Û
                          fold(𝑔, [𝑚 1, 𝑚 2, · · · ]) =    𝑔(𝑚 1 (𝑖), 𝑚 2 (𝑖), · · · )
                                                       𝑖 ∈dom(𝑚 1 )

       For example, if N = [{𝑖 ↦→ 𝑣𝑖 , 𝑗 ↦→ 𝑣 𝑗 }, {𝑖 ↦→ 𝑙𝑖 , 𝑗 ↦→ 𝑙 𝑗 }] and 𝑔 = 𝜆𝑣, 𝑙 .(𝑣 ≥ 𝑙), then
       fold(𝑔, N ) = 𝑣𝑖 ≥ 𝑙𝑖 ∧ 𝑣 𝑗 ≥ 𝑙 𝑗 .
       Here, N𝑗 is the list of maps used in the 𝑗 th condition, which include access maps, attribute
       maps, etc. Each function 𝑔 𝑗 is independent of the rank of the aggregated-axis 𝑥, and only the
       maps in N𝑗 vary with the rank of 𝑥. Thus, we are able to capture all the rank-independent
       information in the function 𝑔 𝑗 . For the fold construct to be well-formed, the arity of 𝑔 𝑗 must
       match the number of maps in N𝑗 .
       In case where the rewrite rule has multiple aggregated-axes, we observe that all such con-
       ditions can be expressed as a conjunction of folds, one for each aggregated-axis. More

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:42                                                                                            Arora et al.


        specifically, if 𝑥 1 · · · 𝑥 𝑝 are the aggregated-axes appearing in a rule, then the 𝑗 th condition
        has the form:                             Û
                                                      fold(𝑖 𝑔 𝑗 , 𝑖 N𝑗 )
                                                𝑖=1···𝑝
                              th
        where 𝑖 𝑔   𝑗 is the 𝑗 condition for the aggregated-axis 𝑥𝑖 , and N𝑗 is the corresponding list of
                                                                         𝑖

       maps. Some important observations:
      – Some of the 𝑖 𝑔′𝑗 𝑠 may be trivial, i.e., they return true for all inputs. In that case, the corre-
         sponding fold always evaluates to true and does not contribute to the actual condition.
      – Introducing trivial folds serves a notational purpose: every condition is uniformly repre-
         sented as a conjunction of one fold per aggregated-axis, regardless of whether that axis
         contributes meaningful conditions. This convention simplifies the representation and such
         trivial folds can be removed once they’re no longer needed.
         §C.3.3 illustrates an example where a condition only involving 𝑥 1 was extended with a
         trivial fold over 𝑥 2 to maintain uniformity.
      – Each 𝑖 𝑔 𝑗 may vary across different aggregated-axes. However, it is applied to all named-axes
         uniformly in a given aggregated-axis.
    • scalarf: this is a scalar function which returns a boolean value, indicating whether the values
       of LHS and RHS tensors match at a given access 𝐴. We refer to it as scalarf since it captures the
       core, scalar computation in the expression, typically consisting of arithmetic and conditionals
       over scalars.
       Based on the arguments to scalarf, we say: scalarf comprises n accesses to X and m conditions.
       Just like index transformers, scalarf is independent of the rank of 𝑥.
  We now rewrite Equation 13 in terms of the scalarf function, accesses, and conditions, to get the
validity condition of a rewrite rule:
                     ∀𝑣 ∈ 𝑣𝑎𝑟𝑠, 𝐶 ∧ valid-expr(LHS) → ∀𝐴 ∈ Access(LHS),
                          scalarf (X[𝑥 ↦→ fmap(𝑒 1, M1 )], · · · , X[𝑥 ↦→ fmap(𝑒𝑛 , M𝑛 )],
                                   fold(𝑔1, N1 ), · · · , fold(𝑔𝑚 , N𝑚 ))                               (15)

D.1     Verification Methodology
Definition 8 (RClass-rank Map). Let 𝑅 be a rewrite rule with RClasses 𝑐 1, · · · , 𝑐 𝑝 . An RClass-rank
map is a mapping {𝑐 1 ↦→ 𝑟 1, · · · , 𝑐 𝑝 ↦→ 𝑟 𝑝 }, that assigns a concrete rank 𝑟𝑖 to each RClass 𝑐𝑖 ,
representing a specific rank instantiation of the rule 𝑅.
Definition 9 (Validity for Concrete RClass Ranks). Let 𝑅 be a rewrite rule and 𝑚 be an
RClass-rank map for 𝑅. Then the predicate valid(𝑅, 𝑚) holds if and only if:
               valid(𝑅, 𝑚) ⇔ 𝑅 is valid for the number of named-axes as specified by 𝑚
This corresponds to a concrete, bounded verification instance: the ranks of all RClasses (and thus of
all aggregated-axes) are fixed according to 𝑚, while the sizes of the named-axes remain arbitrary.
  Let 𝑅 = LHS ⇒𝐶 RHS be the rewrite rule that we wish to verify in the unbounded setting. For
simplicity, the assumptions from §C.1 still apply. We identify a sufficient rank 𝑘 such that:
                             ∀ 𝑖 ≥ 𝑘, valid(𝑅, {𝑐 ↦→ 𝑖}) → valid(𝑅, {𝑐 ↦→ 𝑖 +1})                        (16)
   This means that for all 𝑖 ≥ 𝑘, if the rule is valid when the RClass 𝑐 has rank 𝑖, then it is also
valid when 𝑐 has rank 𝑖 +1. Given such a sufficient rank 𝑘, we can verify the rule in the unbounded
setting using induction on tensor ranks:

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:43


    • Basis: Use bounded verification to prove that the rule is valid for all ranks up to 𝑘:
                                       Û
                                            valid({𝑐 ↦→ 𝑖})
                                             𝑖=1···𝑘
    • Induction Step: Use induction on the rank of 𝑐 with Equation 16 as induction hypothesis:
                                                                         Û
     valid({𝑐 ↦→ 𝑘 }) ∧ [∀𝑖 ≥ 𝑘, valid({𝑐 ↦→ 𝑖}) → valid({𝑐 ↦→ 𝑖 +1})] ⇒   valid({𝑐 ↦→ 𝑖})
                                                                                         𝑖 ≥𝑘
In other words, the rule is valid for any number of named-axes in the RClass 𝑐. What remains is to
determine a sufficient rank 𝑘 for each RClass in a given rule.
   We begin by analyzing the validity condition of the rule when the aggregated-axis 𝑥 is instantiated
with a concrete rank 𝑖, i.e., when valid({𝑐 ↦→ 𝑖}) holds. We first instantiate 𝑥 to 𝑥 𝑖 , a concrete
aggregated-axis containing 𝑖 distinct named-axes, namely {1, · · · , 𝑖}. We similarly instantiate the
precondition 𝐶, input tensor X, list of maps M 𝑗 and N𝑗 , operator attributes, and tensor expressions.
Thus, we can expand the validity valid({𝑐 ↦→ 𝑖}) by rewriting Equation 15 as:
                ∀𝑣 𝑖 ∈ 𝑣𝑎𝑟𝑠 𝑖 , 𝐶 𝑖 ∧ valid-expr(LHS𝑖 ) → ∀𝐴𝑖 ∈ Access(LHS𝑖 ),
                        scalarf (X𝑖 [𝑥 𝑖 ↦→ fmap(𝑒 1, M1𝑖 )], · · · , X𝑖 [𝑥 𝑖 ↦→ fmap(𝑒𝑛 , M𝑛𝑖 )],
                                 fold(𝑔1, N1𝑖 ), · · · , fold(𝑔𝑚 , N𝑚𝑖 ))                                        (17)
As noted previously, the scalar function scalarf, the index transformers 𝑒 𝑗 , and the condition
predicates 𝑔 𝑗 are independent of the rank of 𝑥. The only components that vary with the rank 𝑖 are
the variables 𝑣𝑎𝑟𝑠 𝑖 , access 𝐴𝑖 , and list of maps M𝑖𝑗 and N𝑗𝑖 .
   To compute a sufficient rank 𝑘, we start from the inductive goal [valid({𝑐 ↦→ 𝑘 }) → valid({𝑐 ↦→
𝑘 +1})]. We instead work with its contrapositive,
         valid({𝑐 ↦→ 𝑘 }) → valid({𝑐 ↦→ 𝑘 +1}) ⇔ ¬valid({𝑐 ↦→ 𝑘 +1}) → ¬valid({𝑐 ↦→ 𝑘 })
  Intuitively, ¬valid({𝑐 ↦→ 𝑖}) holds if there exists a counterexample to the rewrite rule at rank 𝑖.
Our goal is to find a sufficient rank 𝑘 such that any counterexample at rank 𝑘 +1 (or higher) can be
lowered to a counterexample at rank 𝑘.
  On expanding the validity condition using Equation 17, the contrapositive becomes:
      ∃ 𝑣 𝑘+1 ∈ 𝑣𝑎𝑟𝑠 𝑘+1, 𝐶 𝑘+1 ∧ valid-expr(LHS𝑘+1 ) ∧ ∃𝐴𝑘+1 ∈ Access(LHS𝑘+1 ),
                ¬scalarf (X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒 1, M1𝑘+1 )], · · · , X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒𝑛 , M𝑛𝑘+1 )],
                           fold(𝑔1, N1𝑘+1 ), · · · , fold(𝑔𝑚 , N𝑚𝑘+1 ))
                                     y
                                     
           ∃ 𝑣 𝑘 ∈ 𝑣𝑎𝑟𝑠 𝑘 , 𝐶 𝑘 ∧ valid-expr(LHS𝑘 ) ∧ ∃𝐴𝑘 ∈ Access(LHS𝑘 ),
                ¬scalarf (X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒 1, M1𝑘 )], · · · , X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒𝑛 , M𝑛𝑘 )],
                           fold(𝑔1, N1𝑘 ), · · · , fold(𝑔𝑚 , N𝑚𝑘 ))


  This means that we are given a counterexample at rank 𝑘 +1, which comprises:
   • A tensor X𝑘+1 with 𝑘+1 named-axes in 𝑥 𝑘+1 , having the shape {𝑥 𝑘+1 ↦→ 𝑚}, where 𝑚 = {1 ↦→
     𝑛 1, · · · , 𝑘 +1 ↦→ 𝑛𝑘+1 },
   • A valuation of variables 𝑣𝑎𝑟𝑠 𝑘+1 such that the precondition 𝐶 𝑘+1 is satisfied and the expression
     LHS𝑘+1 is valid, and
   • An access 𝐴𝑘+1 ∈ Access(LHS𝑘+1 ), where the output tensors do not match.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:44                                                                                         Arora et al.


   To lower this counterexample from rank 𝑘 +1 to rank 𝑘, we must construct:
    • A tensor X𝑘 with 𝑘 named-axes in 𝑥 𝑘 ,
    • A valuation of variables 𝑣𝑎𝑟𝑠 𝑘 such that the precondition 𝐶 𝑘 is satisfied and the expression
      LHS𝑘 is valid, and
    • An access 𝐴𝑘 ∈ Access(LHS𝑘 ), where the output tensors do not match.
  Our goal is to derive lower bounds on 𝑘 while ensuring that any (𝑘 +1)-ranked counterexample
can be lowered to a 𝑘-ranked counterexample. This lower bound serves as a sufficient rank for the
inductive argument.
D.1.1 Counterexample Construction. Our counterexample construction algorithm involves pro-
jecting the (𝑘 +1)-ranked aggregated-axis 𝑥 𝑘+1 to a 𝑘-ranked aggregated-axis 𝑥 𝑘 by choosing 𝑘
named-axes from {1, · · · , 𝑘 +1}. There are 𝑘 +1 such projections in total, but not all of them neces-
sarily yield a valid counterexample at rank 𝑘. We express this construction using a set of equations
and use them to derive constraints on valid projections.
  Projection Notation. Let Γ ⊂ 𝑥 be any projection of the aggregated-axis 𝑥. We define projection
operations on different constructs as follows:
    • Map Projection: Given a map 𝑚 defined on an aggregated-axis 𝑥 (i.e., dom(𝑚) = 𝑥), its
      projection to Γ is defined as:
                                                df
                                           𝑚|𝑥Γ = { 𝑗 ↦→ 𝑚( 𝑗) | 𝑗 ∈ Γ}
                                                                                    df
      If 𝑚 is defined on a different aggregated-axis 𝑥 ′ ≠ 𝑥, then 𝑚|𝑥Γ = 𝑚.
    • Aggregated-Map Projection: Given an aggregated-map 𝑀 that contains the aggregated-axis
      𝑥, its projection to Γ is defined as:
                                      df
                                 𝑀 |𝑥Γ = (𝑀 {𝑥 ↦→ 𝑀 (𝑥)}) ∪ {Γ ↦→ 𝑀 (𝑥)|𝑥Γ }
                                                 df
      If 𝑀 does not contain 𝑥, then 𝑀 |𝑥Γ = 𝑀.
    • Tensor Projection: Given a tensor X, its projection is a tensor with shape Shape(X)|𝑥Γ . The
      projected tensor X|𝑥Γ has unspecified values (unless determined by other constraints).
    • Valuation Projection: Given a set of variable valuations 𝑣𝑎𝑟𝑠, its projection is defined pointwise
      as:
                                                       df
                                            𝑣𝑎𝑟𝑠 |𝑥Γ = {𝑣 |𝑥Γ | 𝑣 ∈ 𝑣𝑎𝑟𝑠}
    • Map List projection: Given a list of maps M = [𝑚 1, · · · , 𝑚𝑟 ], its projection is defined elemen-
      twise as:
                                                      df
                                            M |𝑥Γ = [𝑚 1 |𝑥Γ , · · · , 𝑚𝑟 |𝑥Γ ]
    • Bijection Projection: Given a bijection 𝜇 : 𝑥 ↔ 𝑦, its projection is defined as:
                                                 df
                                            𝜇|𝑥Γ = {Γ(𝑖) ∈ 𝑦 | 𝑖 ∈ 𝑥 }

      The resulting function 𝜇|𝑥Γ : Γ ↔ Γ(𝑥) is also a bijection.
    • Successive Projections: For any construct 𝛼 which can be projected (map, aggregated map,
      tensor, valuation, bijection, etc.), successive projections are defined as:
                                                 𝑥 ···𝑥     df               𝑥
                                              𝛼 | Γ11···Γ𝑝𝑝 = 𝛼 |𝑥Γ11 · · · | Γ𝑝𝑝

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:45


   Map-List Notation. Let M = [𝑚 1, 𝑚 2, · · · ] be a list of maps sharing a common domain, and let
𝑖 ∈ dom(𝑚 1 ) be a named-axis. We write M (𝑖) for the list obtained by applying each map to 𝑖:
                                                 df
                                         M (𝑖) = [𝑚 1 (𝑖), 𝑚 2 (𝑖), · · · ]
   Let Γ ⊂ {1, · · · , 𝑘 +1} be a projection of size 𝑘, representing a selection of 𝑘 named-axes from
𝑥 𝑘+1 . Note that Γ is same as 𝑥 𝑘 , and we use them interchangeably. At this point, the named-axes in Γ
are unknown. As part of constructing a 𝑘-ranked counterexample from a rank 𝑘+1 counterexample,
we define the 𝑘-ranked components by projecting their (𝑘 +1)-ranked counterparts using Γ:
      • Tensors: X𝑘 = X𝑘+1 |𝑥Γ ,
      • Variable Valuations: 𝑣𝑎𝑟𝑠 𝑘 = 𝑣𝑎𝑟𝑠 𝑘+1 |𝑥Γ ,
      • Output Counterexample Access: 𝐴𝑘 = 𝐴𝑘+1 |𝑥Γ ,
      • Access Map Lists: for all 𝑖 ∈ {1 · · · 𝑛}, M𝑖𝑘 = M𝑖𝑘+1 |𝑥Γ , and
      • Condition Map Lists: for all 𝑗 ∈ {1 · · · 𝑚}, N𝑗𝑘 = N𝑗𝑘+1 |𝑥Γ
In all of the projections listed above, we omit the superscript from the aggregated-axis for brevity,
                                  𝑘+1
i.e., 𝛼 |𝑥Γ as shorthand for 𝛼 |𝑥Γ .
   Note that each entry in the map lists M𝑖 and N𝑗 also appears within the variable valuations
𝑣𝑎𝑟𝑠, so projecting them separately is consistent with projecting 𝑣𝑎𝑟𝑠. At this point, the 𝑘-ranked
components are also unknown.
   To complete the construction of a valid 𝑘-ranked counterexample, we require that the arguments
passed to scalarf in the 𝑘-ranked setting match those in the (𝑘 +1)-ranked setting. This imposes a
set of constraints on the projection Γ. These constraints play a key role in computing a lower bound
on the rank 𝑘 for which counterexample lowering is valid, as described in §E.
D.1.2 Handling Generalizations. All the assumptions from §C.1 can be relaxed and the verification
methodology can be extended accordingly. To do so, we simply assume a more general symbolic
form of the rule, i.e., the general form of scalarf, accesses, and conditions. More concretely, suppose
the rule has RClasses 𝑐 1, · · · , 𝑐 𝑝 :
    • Consider any RClass-rank map 𝑚 = {𝑐 1 ↦→ 𝑟 1, · · · , 𝑐 𝑝 ↦→ 𝑟 𝑝 } for the rewrite rule.
    • For each RClass 𝑐𝑙 , compute a rank 𝑘𝑙 such that
                         ∀𝑖 ≥ 𝑘𝑙 , valid(𝑅, 𝑚[𝑐𝑙 ↦→ 𝑖]) → valid(𝑅, 𝑚[𝑐𝑙 ↦→ 𝑖 +1]).
       Similar to the single-aggregated-axis case, we reason using the contrapositive:
                           ¬valid(𝑅, 𝑚[𝑐𝑙 ↦→ 𝑘𝑙 +1]) → ¬valid(𝑅, 𝑚[𝑐𝑙 ↦→ 𝑘𝑙 ])
       This states that, given a counterexample at rank 𝑘𝑙 +1 for all aggregated-axes of RClass 𝑐𝑙 ,
       we must construct a counterexample at rank 𝑘𝑙 for all those aggregated-axes. Importantly, all
       aggregated-axes with the same RClass must have the same rank in any valid instantiation,
       so we project all such aggregated-axes together. The ranks of all other RClasses remain fixed
       throughout the lowering.
       Expanding the validity condition using Equation 17, we obtain:
   ∃ 𝑣 𝑘𝑙 +1 ∈ 𝑣𝑎𝑟𝑠 𝑘𝑙 +1, 𝐶 𝑘𝑙 +1 ∧ valid-expr(LHS𝑘𝑙 +1 ) ∧ ∃𝐴𝑘𝑙 +1 ∈ Access(LHS𝑘𝑙 +1 ), ¬ scalarf ( · · · )
                                       y
                                       
        ∃ 𝑣 𝑘𝑙 ∈ 𝑣𝑎𝑟𝑠 𝑘𝑙 , 𝐶 𝑘𝑙 ∧ valid-expr(LHS𝑘𝑙 ) ∧ ∃𝐴𝑘𝑙 ∈ Access(LHS𝑘𝑙 ), ¬ scalarf ( · · · )                (18)
      We observe that the computed rank 𝑘𝑙 is independent of the ranks of other RClasses in 𝑚.
    • After computing this sufficient rank for each RClass, we obtain the RClass-rank map {𝑐 1 ↦→
      𝑘 1, · · · , 𝑐 𝑝 ↦→ 𝑘𝑝 }.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:46                                                                                                  Arora et al.


      • Finally, we verify the rewrite rule for all concrete instantiations within these bounds:
                            Û          Û
                                 ···         valid(𝑅, {𝑐 1 ↦→ 𝑟 1, · · · , 𝑐 𝑝 ↦→ 𝑟 𝑝 })
                            1≤𝑟 1 ≤𝑘 1   1≤𝑟 𝑝 ≤𝑘𝑝

         If this conjunction is a tautology, then the rewrite rule 𝑅 is verified in the unbounded setting.

E     Proof and Helper Lemmas
In this section, we compute a sufficient rank for each RClass in any rewrite rule. We begin under
the assumptions listed in §C.1 and incrementally relax them to handle more general settings. Our
approach is to reason from Equation 18: we begin with a counterexample at rank 𝑘+1 and construct
a corresponding counterexample at rank 𝑘. In each case, we assume a particular form for the scalar
function scalarf, the accesses, and the conditions, and then derive a sufficient rank for that form.

E.1      Sufficient Rank for Arbitrary Number of Conditions
Lemma 3. Let 𝑅 = LHS ⇒𝐶 RHS be a rewrite rule such that:
    (1) 𝑅 contains at most one input tensor, denoted X,
    (2) X has exactly one aggregated-axis 𝑥 : 𝑐,
    (3) 𝑅 does not contain any of the following operators: reduce, expand, dot, conv, conv-base,
        relabel, and
    (4) The scalar function scalarf comprises one access to X and 𝑚 conditions.
Then, the following holds:
                     max(𝑚, 1) ≤ 𝑘 =⇒ valid(𝑅, {𝑐 ↦→ 𝑘 }) → valid(𝑅, {𝑐 ↦→ 𝑘 +1})
   Proof. The scalarf of 𝑅 has the following canonical form, comprising one access and 𝑚 condi-
tions:
                      scalarf (X[𝑥 ↦→ fmap(𝑒, M)], fold(𝑔1, N1 ), · · · , fold(𝑔𝑚 , N𝑚 ))
where 𝑒 is an index transformer and 𝑔1, · · · , 𝑔𝑚 are condition predicates.
   Our goal is to find a sufficient rank 𝑘 such that any counterexample at rank 𝑘 +1 can be lowered
to a counterexample at rank 𝑘. Let 𝑥 𝑘+1 = {1, · · · , 𝑘 +1} denote a (𝑘 +1)-ranked instantiation of 𝑥.
Let Γ ⊂ 𝑥 𝑘+1 be a projection of size 𝑘.
   Starting from Equation 18, we have:
∃ 𝑣 𝑘+1 ∈ 𝑣𝑎𝑟𝑠 𝑘+1, 𝐶 𝑘+1 ∧ valid-expr(LHS𝑘+1 ) ∧ ∃𝐴𝑘+1 ∈ Access(LHS𝑘+1 ),
                           ¬scalarf (X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒, M 𝑘+1 )], fold(𝑔1, N1𝑘+1 ), · · · , fold(𝑔𝑚 , N𝑚𝑘+1 ))
                                              y
                                              
        ∃ 𝑣 𝑘 ∈ 𝑣𝑎𝑟𝑠 𝑘 , 𝐶 𝑘 ∧ valid-expr(LHS𝑘 ) ∧ ∃𝐴𝑘 ∈ Access(LHS𝑘 ),
                           ¬scalarf (X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒, M 𝑘 )], fold(𝑔1, N1𝑘 ), · · · , fold(𝑔𝑚 , N𝑚𝑘 ))
    We define the 𝑘-ranked components via projection with Γ:
      • X𝑘 = X𝑘+1 |𝑥Γ ,
      • 𝑣𝑎𝑟𝑠 𝑘 = 𝑣𝑎𝑟𝑠 𝑘+1 |𝑥Γ ,
      • 𝐴𝑘 = 𝐴𝑘+1 |𝑥Γ ,
      • M 𝑘 = M 𝑘+1 |𝑥Γ , and
      • for all 𝑗 ∈ {1 · · · 𝑚}, N𝑗𝑘 = N𝑗𝑘+1 |𝑥Γ

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                       29:47


   Since 𝐶 𝑘+1 ⇒ 𝐶 𝑘 and valid-expr(LHS𝑘+1 ) ⇒ valid-expr(LHS𝑘 ), the precondition remains satis-
fied and the LHS expression remains valid in the 𝑘-ranked counterexample (Theorem 9). What
remains is ensuring equivalence of scalarf arguments in both counterexamples and deriving con-
straints on Γ:
    • Conditions: For all 𝑙 ∈ {1 · · · 𝑚}, we require that fold(𝑔𝑙 , N𝑙𝑘 ) and fold(𝑔𝑙 , N𝑙𝑘+1 ) must have
      the same truth value. Let N𝑙𝑘+1 = [𝑚𝑘+1 1 , 𝑚 2 , · · · ]. Then:
                                                    𝑘+1


                          N𝑙𝑘 = N𝑙𝑘+1 |𝑥Γ = [𝑚𝑘+1 𝑥    𝑘+1 𝑥                𝑘     𝑘
                                              1 | Γ , 𝑚 2 | Γ , · · · ] = [𝑚 1 , 𝑚 2 , · · · ]

       Let 𝐶𝑙 be the set of constraints we get from this equation. We expand the definition of fold:
                                                                          𝑘+1
                                                                          Û
              fold(𝑔𝑙 , N𝑙𝑘+1 ) = fold(𝑔𝑙 , [𝑚𝑘+1  𝑘+1
                                              1 , 𝑚 2 , · · · ]) =               𝑔𝑙 (𝑚𝑘+1     𝑘+1
                                                                                      1 (𝑖), 𝑚 2 (𝑖), · · · )
                                                                          𝑖=1
                                                                          Û
                    fold(𝑔𝑙 , N𝑙𝑘 ) = fold(𝑔𝑘 , [𝑚𝑘1 , 𝑚𝑘2 , · · · ]) =          𝑔𝑙 (𝑚𝑘1 ( 𝑗), 𝑚𝑘2 ( 𝑗), · · · )
                                                                          𝑗 ∈Γ

      Let 𝑏 = fold(𝑔𝑙 , N𝑙𝑘+1 ), which contains 𝑘 +1 clauses, and 𝑐 = fold(𝑔𝑙 , N𝑙𝑘 ), which contains 𝑘
      clauses. The value of 𝑏 is known since it depends entirely on the (𝑘+1)-ranked counterexample.
      Let 𝑟 be the number of clauses in 𝑏 which evaluate to true. The remaining (𝑘 +1) − 𝑟 clauses
      evaluate to false. We perform a case analysis on 𝑟 :
      – 𝑟 < 𝑘: Then 𝑏 = false. We require 𝑐 = false. We can see that for any size-𝑘 projection Γ, at
        least one false clause will be included. Hence, 𝑐 = false always. There are no constraints
        on Γ, i.e., 𝐶𝑙 = ∅.
      – 𝑟 = 𝑘: Then 𝑏 = false. We require 𝑐 = false. There exists exactly one 𝑗 ∈ 𝑥 𝑘+1 , for which
        the corresponding clause is false. To ensure 𝑐 = false, Γ must include the named-axis 𝑗.
        Leaving out this named-axis will lead to 𝑐 being true. Therefore, 𝐶𝑙 = { 𝑗 }.
      – 𝑟 = 𝑘 +1: Then 𝑏 = true. We require 𝑐 = true. We can see that for any size-𝑘 projection Γ, 𝑐
        will be true. There are no constraints on Γ, i.e., 𝐶𝑙 = ∅.
      We get at most one constraint for each 𝑔𝑙 , i.e., |𝐶𝑙 | ≤ 1. The set of all constraints from the
      conditions is given by:
                                                   𝑚
                                                   Ø
                                              𝐶=      𝐶𝑙
                                                           𝑙=1
    • Accesses: We require the following,
                        X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒, M 𝑘 )] = X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒, M 𝑘+1 )]
       This can always be satisfied since we can just assign the value of X𝑘+1 at the access {𝑥 𝑘+1 ↦→
       fmap(𝑒, M 𝑘+1 )} to X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒, M 𝑘 )], irrespective of the projection. Therefore, no
       constraints on Γ are introduced by this equation.
   The final set of constraints is 𝐶. To construct a valid projection of size 𝑘, we require |𝐶 | ≤ 𝑘.
We know that |𝐶 | ≤ 𝑚, as each condition results in at most one constraint. We also require 1 ≤ 𝑘
to avoid empty aggregated-axes. Therefore, max(𝑚, 1) ≤ 𝑘 is a sufficient condition for a valid
counterexample lowering.
   Finally, we fully construct the 𝑘-ranked counterexample as follows:
    • Projection: The named-axes in 𝐶 must be a part of the projection Γ, but the other axes
      are unspecified. To get the final projection Γ, extend 𝐶 by any (𝑘 − |𝐶 |) named-axes from
      {1, · · · , 𝑘 +1} 𝐶.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:48                                                                                               Arora et al.


   • Construct all 𝑘-ranked components as described above using Γ. Performing a projection
      ensures that the tensor shapes, access maps, and attributes are valid and the precondition is
      satisfied in the 𝑘-ranked counterexample (Theorem 9).
   • Tensor values: Let 𝑣 = X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒, M 𝑘+1 )]. We only require X𝑘 to have the value 𝑣
      at the access {𝑥 𝑘 ↦→ fmap(𝑒, M 𝑘 )}, and the values at other accesses are unspecified.
Thus, 𝑘 = max(𝑚, 1) is a sufficient rank for verifying the rewrite rule 𝑅.                       □

E.2     Sufficient Rank for Arbitrary Number of Accesses
Lemma 4. Let 𝑅 = LHS ⇒𝐶 RHS be a rewrite rule such that:
  (1) 𝑅 contains at most one input tensor, denoted X,
  (2) X has exactly one aggregated-axis 𝑥 : 𝑐,
  (3) 𝑅 does not contain any of the following operators: reduce, expand, dot, conv, conv-base,
      relabel, and
  (4) The scalar function scalarf comprises 𝑛 accesses to X and 𝑚 conditions.
Then, the following holds:
                          
                          𝑛
                max(𝑚 +      , 1) ≤ 𝑘 ⇒ valid(𝑅, {𝑐 ↦→ 𝑘 }) → valid(𝑅, {𝑐 ↦→ 𝑘 +1})
                           2
   Proof. The scalarf of 𝑅 has the following canonical form, comprising 𝑛 accesses and 𝑚 condi-
tions:
                       scalarf (X[𝑥 ↦→ fmap(𝑒 1, M1 )], · · · , X[𝑥 ↦→ fmap(𝑒𝑛 , M𝑛 )],
                                fold(𝑔1, N1 ), · · · , fold(𝑔𝑚 , N𝑚 ))
where 𝑒 1, · · · , 𝑒𝑛 index transformers and 𝑔1, · · · , 𝑔𝑚 are condition predicates.
   Our goal is to find a sufficient rank 𝑘 such that any counterexample at rank 𝑘 +1 can be lowered
to a counterexample at rank 𝑘. Let 𝑥 𝑘+1 = {1, · · · , 𝑘 +1} denote a (𝑘 +1)-ranked instantiation of 𝑥.
Let Γ ⊂ 𝑥 𝑘+1 be a projection of size 𝑘.
   Starting from Equation 18, we have:
        ∃ 𝑣 𝑘+1 ∈ 𝑣𝑎𝑟𝑠 𝑘+1, 𝐶 𝑘+1 ∧ valid-expr(LHS𝑘+1 ) ∧ ∃𝐴𝑘+1 ∈ Access(LHS𝑘+1 ),
                  ¬scalarf (X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒 1, M1𝑘+1 )], · · · , X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒𝑛 , M𝑛𝑘+1 )],
                              fold(𝑔1, N1𝑘+1 ), · · · , fold(𝑔𝑚 , N𝑚𝑘+1 ))
                                                           y
                                                           
        ∃ 𝑣 𝑘 ∈ 𝑣𝑎𝑟𝑠 𝑘 , 𝐶 𝑘 ∧ valid-expr(LHS𝑘 ) ∧ ∃𝐴𝑘 ∈ Access(LHS𝑘 ),
                  ¬scalarf (X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒 1, M1𝑘 )], · · · , X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒𝑛 , M𝑛𝑘 )],
                              fold(𝑔1, N1𝑘 ), · · · , fold(𝑔𝑚 , N𝑚𝑘 ))
  We define the 𝑘-ranked components via projection with Γ:
   • X𝑘 = X𝑘+1 |𝑥Γ ,
   • 𝑣𝑎𝑟𝑠 𝑘 = 𝑣𝑎𝑟𝑠 𝑘+1 |𝑥Γ ,
   • 𝐴𝑘 = 𝐴𝑘+1 |𝑥Γ ,
   • for all 𝑖 ∈ {1 · · · 𝑛}, M𝑖𝑘 = M𝑖𝑘+1 |𝑥Γ , and
   • for all 𝑗 ∈ {1 · · · 𝑚}, N𝑗𝑘 = N𝑗𝑘+1 |𝑥Γ
   Since 𝐶 𝑘+1 ⇒ 𝐶 𝑘 and valid-expr(LHS𝑘+1 ) ⇒ valid-expr(LHS𝑘 ), the precondition remains satis-
fied and the LHS expression remains valid in the 𝑘-ranked counterexample (Theorem 9). What

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:49


remains is ensuring equivalence of scalarf arguments in both counterexamples and deriving con-
straints on Γ:
    • Conditions: For all 𝑙 ∈ {1 · · · 𝑚}, we require that fold(𝑔𝑙 , N𝑙𝑘 ) and fold(𝑔𝑙 , N𝑙𝑘+1 ) must have
      the same truth value. We assume the conditions to beÐ        independent of the accesses in the
      worst case. Therefore, the constraints as given by 𝐶 1 = 𝑚     𝑙=1 𝐶𝑙 still hold (Lemma 3).
    • Accesses: For all 𝑙 ∈ {1 · · · 𝑛}, we require:
                       X𝑘 [𝑥 𝑘 ↦→ fmap(𝑒𝑙 , M𝑙𝑘 )] = X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒𝑙 , M𝑙𝑘+1 )]
      Let 𝑣𝑙 be the value of the tensor 𝑋 𝑘+1 at the access {𝑥 𝑘+1 ↦→ fmap(𝑒𝑙 , M𝑙𝑘+1 )}. The projection
      Γ should not lead to any inconsistency with respect to the elements of X𝑘 .
      For example, if 𝑣 1 ≠ 𝑣 2 , then these values correspond to different accesses in the tensor X𝑘+1 ,
      i.e., fmap(𝑒 1, M1𝑘+1 ) ≠ fmap(𝑒 2, M2𝑘+1 ). Therefore, there exists some 𝑗 ∈ {1 · · · (𝑘 +1)} such
      that 𝑒 1 (M1𝑘+1 ( 𝑗)) ≠ 𝑒 2 (M2𝑘+1 ( 𝑗)), i.e., the access indices are unequal.
      We require that fmap(𝑒 1, M1𝑘 ) and fmap(𝑒 2, M2𝑘 ) are different accesses in X𝑘 , otherwise the
      same access in X𝑘 would be assigned two different values 𝑣 1 and 𝑣 2 in the counterexample
      lowering. Selecting 𝑗 as one of the named-axes in the projection will make sure that elements
      of X𝑘 are consistent.
      Consider any arbitrary pair of values 𝑣𝑟 and 𝑣𝑠 , where 𝑟, 𝑠 ∈ {1 · · · 𝑛} and 𝑟 ≠ 𝑠. These
      correspond to two accesses in X𝑘+1 . There are 𝑛2 such access pairs. Let 𝐶𝑟,𝑠 be the set of
      constraints we get from this pair. The following cases arise:
      – 𝑣𝑟 = 𝑣𝑠 : Then any projection will result in a valid counterexample since the lowering will
         not lead to any inconsistency. For this case, 𝐶𝑟,𝑠 = ∅
      – 𝑣𝑟 ≠ 𝑣𝑠 : Then these values correspond to different accesses in X𝑘+1 , i.e.,
                                     fmap(𝑒𝑟 , M𝑟𝑘+1 ) ≠ fmap(𝑒𝑠 , M𝑠𝑘+1 )
         We require that they also correspond to different accesses in X𝑘 , i.e.,
                                       fmap(𝑒𝑟 , M𝑟𝑘 ) ≠ fmap(𝑒𝑟 , M𝑠𝑘 )                                         (19)
       Let 𝐸 = {𝑙 ∈ 𝑥 𝑘+1 | 𝑒𝑟 (M𝑟𝑘+1 (𝑙)) = 𝑒𝑠 (M𝑠𝑘+1 (𝑙))} denote the set of named-axes having the
       same index value in accesses 𝑟 and 𝑠. The following cases arise:
       ∗ |𝐸| < 𝑘: Then any size-𝑘 projection will ensure that Equation 19 holds, since there exists
          at least one named-axis with different index values. Therefore, 𝐶𝑟,𝑠 = ∅.
       ∗ |𝐸| = 𝑘: Then there exists exactly one 𝑙 ∈ 𝑥 𝑘+1 for which 𝑒𝑟 (M𝑟𝑘+1 (𝑙)) ≠ 𝑒𝑠 (M𝑠𝑘+1 (𝑙)).
          To make sure that Equation 19 holds, 𝑙 needs to be in the projection. If we leave this
          named-axis, then the accesses 𝑟 and 𝑠 will be the same in the tensor X𝑘 , but would be
          assigned two different values 𝑣𝑟 and 𝑣𝑠 . Therefore, 𝐶𝑟,𝑠 = {𝑙 }.
       ∗ |𝐸| = 𝑘 +1: This means that the accesses 𝑟 and 𝑠 are the same in X𝑘+1 . This implies that
          𝑣𝑟 = 𝑣𝑠 , which is a contradiction. Therefore, such a case cannot arise.
  The set of all constraints from accesses is given by:
                                                  Ø
                                            𝐶2 =       𝐶𝑟,𝑠
                                                        (𝑟,𝑠 )
                              
  We know that |𝐶 2 | ≤ 𝑛2 , as each access pair results in at most one constraint. The final set of
constraints is 𝐶 = 𝐶 1 ∪ 𝐶 2 . The set of constraints 𝐶 is bounded by:
                                                                                 
                                                                                 𝑛
                                  |𝐶 | = |𝐶 1 ∪ 𝐶 2 | ≤ |𝐶 1 | + |𝐶 2 | ≤ 𝑚 +
                                                                                 2

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:50                                                                                                 Arora et al.


  To construct a valid projection of size 𝑘, we require |𝐶 | ≤ 𝑘. We also require 1 ≤ 𝑘 to avoid empty
aggregated-axes. Therefore, max(𝑚 + 𝑛2 , 1) ≤ 𝑘 is a sufficient condition for a valid counterexample
lowering.
  Finally, we fully construct the 𝑘-ranked counterexample as follows:
   • Projection: The named-axes in 𝐶 must be a part of the projection Γ, but the other axes
      are unspecified. To get the final projection Γ, extend 𝐶 by any (𝑘 − |𝐶 |) named-axes from
      {1, · · · , 𝑘 +1} 𝐶.
   • Construct all 𝑘-ranked components as described above using Γ. Performing a projection
      ensures that the tensor shapes, access maps, and attributes are valid and the precondition is
      satisfied in the 𝑘-ranked counterexample (Theorem 9).
   • Tensor values: Let 𝑣𝑙 = X𝑘+1 [𝑥 𝑘+1 ↦→ fmap(𝑒𝑙 , M𝑙𝑘+1 )] be the value at the 𝑙 th access to X𝑘+1 .
      We only require X𝑘 to have the value 𝑣𝑙 at the access {𝑥 𝑘 ↦→ fmap(𝑒𝑙 , M𝑙𝑘 )}, and the values
      at other accesses are unspecified. This should hold for all 𝑙 ∈ {1 · · · 𝑛}.
                         
Thus, 𝑘 = max(𝑚 + 𝑛2 , 1) is a sufficient rank for verifying the rewrite rule 𝑅.                     □

E.3     Sufficient Rank for Arbitrary Number of Aggregated-Axes
Lemma 5. Let 𝑅 = LHS ⇒𝐶 RHS be a rewrite rule such that:
  (1) 𝑅 contains at most one input tensor, denoted X,
  (2) All aggregated-axes appearing in the rule have the same RClass, denoted 𝑐,
  (3) 𝑅 does not contain any of the following operators: reduce, dot, conv, conv-base, and
  (4) The scalar function scalarf comprises 𝑛 accesses to X and 𝑚 conditions.
Then, the following holds:
                          
                          𝑛
               max(𝑚 +       , 1) ≤ 𝑘 ⇒ valid(𝑅, {𝑐 ↦→ 𝑘 }) → valid(𝑅, {𝑐 ↦→ 𝑘 +1})
                           2
   Proof. Let 𝑥 1, · · · , 𝑥 𝑝 denote all the aggregated-axes that appear in the rewrite rule 𝑅, each
belonging to the same RClass 𝑐 by assumption. Among these, let 𝑥 1, · · · , 𝑥ℎ be the aggregated-axes
that index the input tensor X. The remaining aggregated-axes 𝑥ℎ+1, · · · , 𝑥 𝑝 occur as arguments to
operators such as expand but do not index X directly. Since all aggregated-axes belong to the same
class 𝑐, they are instantiated to the same rank in any valid instantiation of the rule.
   The scalarf of 𝑅 has the following canonical form, comprising 𝑛 accesses and 𝑚 conditions:
                   scalarf (X[𝑥 1 ↦→ fmap( 1𝑒 1, 1 M1 ), · · · , 𝑥ℎ ↦→ fmap(ℎ 𝑒 1, ℎ M1 )], · · · ,
                                X[𝑥 1 ↦→ fmap( 1𝑒𝑛 , 1 M𝑛 ), · · · , 𝑥ℎ ↦→ fmap(ℎ 𝑒𝑛 , ℎ M𝑛 )],
                                     𝑝
                                     Û                                   𝑝
                                                                         Û
                                           fold( 𝑗 𝑔1, 𝑗 N1 ), · · · ,         fold( 𝑗 𝑔𝑚 , 𝑗 N𝑚 ))
                                     𝑗=1                                 𝑗=1

where each 𝑗 𝑒   𝑖 is an index transformer and each 𝑔𝑖 is a condition predicate.
                                                    𝑗

   Our goal is to find a sufficient rank 𝑘 for the RClass 𝑐, such that any counterexample at rank 𝑘+1
can be lowered to a counterexample at rank 𝑘. Let 𝑥𝑖𝑘+1 = {1𝑖 , · · · , 𝑘 +1𝑖 } denote a (𝑘 +1)-ranked
instantiation of each aggregated-axis 𝑥𝑖 . Since all aggregated-axes belong to the same RClass 𝑐, for
all 𝑖, 𝑗 ∈ {1 · · · 𝑝}, there exists a canonical bijection:
                                 𝑘+1
                                𝜇𝑖,𝑗 = MapAxes(𝑐, 𝑥𝑖𝑘+1, 𝑥 𝑘+1    𝑘+1
                                                           𝑗 ) : 𝑥𝑖   ↔ 𝑥 𝑘+1
                                                                          𝑗

  To construct a valid counterexample, we project each aggregated-axis 𝑥𝑖 since they all have the
same RClass and are instantiated to the same rank. Let Γ𝑖 ⊂ 𝑥𝑖𝑘+1 be a projection of size 𝑘 for 𝑥𝑖 .

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                             29:51


These projections must be pairwise disjoint and must respect the canonical bijections:
                                                ∀𝑖, 𝑗 ∈ {1 · · · 𝑝},         𝑘+1
                                                                            𝜇𝑖,𝑗 (Γ𝑖 ) = Γ𝑗                               (20)
  Starting from Equation 18, we have:
                ∃ 𝑣 𝑘+1 ∈ 𝑣𝑎𝑟𝑠 𝑘+1, 𝐶 𝑘+1 ∧ valid-expr(LHS𝑘+1 ) ∧ ∃𝐴𝑘+1 ∈ Access(LHS𝑘+1 ),
                                     ¬scalarf (𝑣 1, · · · , 𝑣𝑛 , 𝑏 1, · · · , 𝑏𝑚 )
                                                        y
                                                        
                       ∃ 𝑣 𝑘 ∈ 𝑣𝑎𝑟𝑠 𝑘 , 𝐶 𝑘 ∧ valid-expr(LHS𝑘 ) ∧ ∃𝐴𝑘 ∈ Access(LHS𝑘 ),
                                     ¬scalarf (𝑤 1, · · · , 𝑤𝑛 , 𝑐 1, · · · , 𝑐𝑚 )
where,
   • For each 𝑙 ∈ {1 · · · 𝑛}, 𝑣𝑙 denotes the 𝑙 th access to X𝑘+1 in the (𝑘 +1)-ranked counterexample:
                  𝑣𝑙 = X𝑘+1 [𝑥 1𝑘+1 ↦→ fmap( 1𝑒𝑙 , 1 M𝑙𝑘+1 ), · · · , 𝑥ℎ𝑘+1 ↦→ fmap(ℎ 𝑒𝑙 , ℎ M𝑙𝑘+1 )]
    • For each 𝑙 ∈ {1 · · · 𝑛}, 𝑤𝑙 denotes the 𝑙 th access to X𝑘 in the 𝑘-ranked counterexample:
                         𝑤𝑙 = X𝑘 [𝑥 1𝑘 ↦→ fmap( 1𝑒𝑙 , 1 M𝑙𝑘 ), · · · , 𝑥ℎ𝑘 ↦→ fmap(ℎ 𝑒𝑙 , ℎ M𝑙𝑘 )]
    • For each 𝑙 ∈ {1 · · · 𝑚}, 𝑏𝑙 denotes the 𝑙 th condition in the (𝑘 +1)-ranked counterexample:
                                                            𝑝
                                                            Û
                                                     𝑏𝑙 =         fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘+1 )
                                                            𝑗=1

    • For each 𝑙 ∈ {1 · · · 𝑚}, 𝑐𝑙 denotes the 𝑙 th condition in the 𝑘-ranked counterexample:
                                                              𝑝
                                                              Û
                                                       𝑐𝑙 =         fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘 )
                                                              𝑗=1

  We define the 𝑘-ranked components via projections with Γ1, · · · , Γ𝑝 :
                     𝑥 ,··· ,𝑥
    • X𝑘 = X𝑘+1 | Γ11,··· ,Γ𝑝𝑝 ,
                                 𝑥 ,··· ,𝑥
    • 𝑣𝑎𝑟𝑠 𝑘 = 𝑣𝑎𝑟𝑠 𝑘+1 | Γ11,··· ,𝑥𝑝𝑝 ,
                      𝑥 ,··· ,𝑥
    • 𝐴𝑘 = 𝐴𝑘+1 | Γ11,··· ,Γ𝑝𝑝 ,
    • for all 𝑙 ∈ {1 · · · 𝑛}, 𝑖 ∈ {1 · · · ℎ}, 𝑖 M𝑙𝑘 = 𝑖 M𝑙𝑘+1 |𝑥Γ𝑖𝑖 ,
                                                                  𝑥
    • for all 𝑙 ∈ {1 · · · 𝑚}, 𝑗 ∈ {1 · · · 𝑝}, 𝑗 N𝑙𝑘 = 𝑗 N𝑙𝑘+1 | Γ𝑗𝑗 , and
                                                           𝑘 = MapAxes(𝑐, Γ , Γ ) is simply 𝜇 𝑘+1 |𝑥𝑖 . The
    • for all 𝑖, 𝑗 ∈ {1 · · · 𝑝}, the canonical bijection 𝜇𝑖,𝑗                 𝑖 𝑗              𝑖,𝑗 Γ𝑖
      resulting canonical bijections must satisfy:
      – 𝜇𝑖,𝑗
          𝑘 ◦ 𝜇 𝑘 = id, and
                  𝑗,𝑖
      – 𝜇𝑘𝑗,𝑙 ◦ 𝜇𝑖,𝑗
                  𝑘 = 𝜇𝑘 .
                          𝑖,𝑙
      To ensure that these properties hold, we must ensure that Equation 20 is satisfied.
   Since 𝐶 𝑘+1 ⇒ 𝐶 𝑘 and valid-expr(LHS𝑘+1 ) ⇒ valid-expr(LHS𝑘 ), the precondition remains satis-
fied and the LHS expression remains valid in the 𝑘-ranked counterexample (Theorem 9). What
remains is ensuring equivalence of scalarf arguments in both counterexamples and deriving con-
straints on Γ1, · · · , Γ𝑝 :
                                                    Ó𝑝                               Ó𝑝
    • Conditions: For all 𝑙 ∈ {1 · · · 𝑚}, 𝑐𝑙 = 𝑗=1 fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘 ) and 𝑏𝑙 = 𝑗=1 fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘+1 )
      must have the same truth value. Let 1𝐶𝑙 , · · · , 𝑝 𝐶𝑙 be the set of constraints we get on Γ1, · · · , Γ𝑝
      from this equation, respectively.

                                        Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:52                                                                                                   Arora et al.


        The value of 𝑏𝑙 is known since it depends entirely on the (𝑘 +1)-ranked counterexample.
        Both 𝑏𝑙 and 𝑐𝑙 contain 𝑝 folds. Let 𝑟 be the number of folds in 𝑏𝑙 that evaluate to true. The
        remaining 𝑝 − 𝑟 folds evaluate to false. We perform a case analysis on 𝑟 :
        – 𝑟 = 𝑝: Then 𝑏𝑙 = true. We require 𝑐𝑙 = true. We can see that for any size-𝑘 projections
          Γ1, · · · , Γ𝑝 , all folds in 𝑐𝑙 will be true. Therefore, 1𝐶𝑙 = · · · = 𝑝 𝐶𝑙 = ∅.
        – 𝑟 < 𝑝: Then 𝑏𝑙 = false. We require 𝑐𝑙 = false. This implies that there exists some aggregated-
          axis, say 𝑥𝑖𝑘+1 , whose fold evaluates to false in 𝑏𝑙 , i.e., fold(𝑖 𝑔𝑙 , 𝑖 N𝑙𝑘+1 ) = false. We ensure
          that the fold of 𝑥𝑖𝑘 , i.e., fold(𝑖 𝑔𝑙 , 𝑖 N𝑙𝑘 ) also evaluates to false, resulting in 𝑐𝑙 = false. This is
          similar to Lemma 3, and we get at most one constraint on Γ𝑖 in 𝑖 𝐶𝑙 and no constraints on
          other projections. Therefore, |𝑖 𝐶𝑙 | ≤ 1 and 𝑗 𝐶𝑙 = ∅ for all 𝑗 ≠ 𝑖.
        Each condition contributes at most one constraint to exactly one projection. The set of all
        constraints through the conditions is given by, where 𝑖 𝐶 denotes the constraints on Γ𝑖 :
                                                  𝑚
                                                  Ø                       𝑚
                                                                          Ø
                                            1         1
                                             𝐶=        𝐶𝑙 , · · · , 𝑝 𝐶 =   𝑝
                                                                              𝐶𝑙
                                               𝑙=1                    𝑙=1
        Since we get at most 𝑚 constraints partitioned into these 𝑝 sets, we conclude that the total
        number of constraints is bounded by:
                                              | 1𝐶 | + · · · + |𝑝 𝐶 | ≤ 𝑚
    • Accesses: For all 𝑙 ∈ {1 · · · 𝑛}, 𝑤𝑙 must be the same as 𝑣𝑙 . The projections Γ1, · · · , Γ𝑝 should
      not lead to inconsistencies with respect to the elements of X𝑘 .
      Consider any arbitrary pair of values 𝑣𝑟 and 𝑣𝑠 , where 𝑟, 𝑠 ∈ {1 · · · 𝑛} and 𝑟 ≠ 𝑠. These
      correspond to two accesses to X𝑘+1 . There are 𝑛2 such access pairs. Let 1 𝐷𝑟,𝑠 , · · · , ℎ 𝐷𝑟,𝑠 be the
      constraints we get on Γ1, · · · , Γℎ from this equation, respectively. We exclude ℎ+1 𝐷𝑟,𝑠 , · · · , 𝑝 𝐷𝑟,𝑠
      from the analysis because the corresponding aggregated-axes do not index the tensor X,
      and hence do not introduce any inconsistencies. Thus, their constraints are equal to ∅. The
      following cases arise:
      – 𝑣𝑟 = 𝑣𝑠 : Then any projection will result in a valid counterexample since the lowering will
        not lead to any inconsistency. For this case, 𝑖 𝐷𝑟,𝑠 = ∅ for all 𝑖.
      – 𝑣𝑟 ≠ 𝑣𝑠 : Then these values correspond to different accesses in X𝑘+1 , i.e.,
                     {𝑥 1𝑘+1 ↦→ fmap( 1𝑒𝑟 , 1 M𝑟𝑘+1 ), · · · , 𝑥ℎ𝑘+1 ↦→ fmap(ℎ 𝑒𝑟 , ℎ M𝑟𝑘+1 )} ≠
                        {𝑥 1𝑘+1 ↦→ fmap( 1𝑒𝑠 , 1 M𝑠𝑘+1 ), · · · , 𝑥ℎ𝑘+1 ↦→ fmap(ℎ 𝑒𝑠 , ℎ M𝑠𝑘+1 )}
          We require that they also correspond to different accesses in X𝑘 , i.e.,
                          {𝑥 1𝑘 ↦→ fmap( 1𝑒𝑟 , 1 M𝑟𝑘 ), · · · , 𝑥ℎ𝑘 ↦→ fmap(ℎ 𝑒𝑟 , ℎ M𝑟𝑘 )} ≠
                             {𝑥 1𝑘 ↦→ fmap( 1𝑒𝑠 , 1 M𝑠𝑘 ), · · · , 𝑥ℎ𝑘 ↦→ fmap(ℎ 𝑒𝑠 , ℎ M𝑠𝑘 )}                 (21)
          Since the accesses do not match in X𝑘+1 , there exists some aggregated-axis, say 𝑥𝑖𝑘+1 , for
          𝑖 ∈ {1 · · · ℎ}, such that its corresponding access maps in the two accesses are unequal:
                                    fmap(𝑖 𝑒𝑟 , 𝑖 M𝑟𝑘+1 ) ≠ fmap(𝑖 𝑒𝑠 , 𝑖 M𝑠𝑘+1 )
          We ensure that the access maps of 𝑥𝑖𝑘 are unequal in the two accesses, to ensure that
          Equation 21 holds:
                                fmap(𝑖 𝑒𝑟 , 𝑖 M𝑟𝑘 ) ≠ fmap(𝑖 𝑒𝑠 , 𝑖 M𝑠𝑘 )
          This is similar to Lemma 4, and we get at most one constraint on Γ𝑖 in 𝑖 𝐷𝑟,𝑠 and no constraints
          on other projections. Therefore, |𝑖 𝐷𝑟,𝑠 | ≤ 1 and 𝑗 𝐷𝑟,𝑠 = ∅ for all 𝑗 ≠ 𝑖.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                       29:53


       Each access pair contributes at most one constraint to exactly one projection. The set of all
       constraints through the accesses is given by, where 𝑖 𝐷 denotes the constraints on Γ𝑖 :

                                             Ø                                   Ø
                                    1                 1
                                        𝐷=                𝐷𝑟,𝑠 , · · · , 𝑝 𝐷 =            𝑝
                                                                                              𝐷𝑟,𝑠
                                             (𝑟,𝑠 )                              (𝑟,𝑠 )


                              
       Since we get at most 𝑛2 constraints partitioned into these 𝑝 sets, we conclude that the total
       number of constraints is bounded by:

                                                                                  
                                                                                  𝑛
                                             | 1 𝐷 | + · · · + |𝑝 𝐷 | ≤
                                                                                  2


  We now define the combined set of constraints (from both conditions and accesses) on each
projection Γ𝑖 as 𝐹𝑖 = 𝑖 𝐶 ∪ 𝑖 𝐷. The total number of constraints across all projections is bounded by:


                       |𝐹 1 | + · · · + |𝐹𝑝 | = | 1𝐶 ∪ 1 𝐷 | + · · · + |𝑝 𝐶 ∪ 𝑝 𝐷 |
                                              ≤ | 1𝐶 | + | 1 𝐷 | + · · · + |𝑝 𝐶 | + |𝑝 𝐷 |
                                              = | 1𝐶 | + · · · + |𝑝 𝐶 | + | 1 𝐷 | + · · · + |𝑝 𝐷 |
                                                        
                                                        𝑛
                                              ≤𝑚+
                                                        2

                                                                  
Thus, the total number of constraints is at most 𝑚 + 𝑛2 , partitioned across the 𝑝 constraint sets.
                                     
This implies that max𝑖 |𝐹𝑖 | ≤ 𝑚 + 𝑛2 (the maximum possible constraints on any projection). For all
the projections to be valid, we require |𝐹 1 | ≤ 𝑘, · · · , |𝐹𝑝 | ≤ 𝑘, or equivalently,
                                                                                       max𝑖 |𝐹𝑖 | ≤ 𝑘. We also
need 1 ≤ 𝑘 to avoid empty aggregated-axes. Therefore, max(𝑚 + 𝑛2 , 1) ≤ 𝑘 is a sufficient condition
for a valid counterexample lowering.
   Finally, we fully construct the 𝑘-ranked counterexample as follows:

    • Projection: For all 𝑗 ∈ {1 · · · 𝑝}, the named-axes in 𝐹 𝑗 must be a part of the projection Γ𝑗 .
      Additionally, the projections should respect the canonical bijections of the (𝑘 +1)-ranked
      counterexample. We compute the final projections using the ComputeProjections routine
      described in Algorithm 2. It takes the final constraints 𝐹 1, · · · , 𝐹𝑝 as input and returns the
      projections Γ1, · · · , Γ𝑝 . In lines 4-9, we expand each 𝐹 𝑗 using the canonical bijection images
      of other constraint sets.
      After line 9, the sets 𝐹 1′, · · · , 𝐹𝑝′ are of the same size. In fact, there exists a bijection between
      all the sets: the bijection between 𝐹𝑖′ and 𝐹 𝑗′ is simply 𝜇𝑖,𝑗  𝑘+1 |𝑥𝑖 . This ensures that all 𝐹 ′ contain
                                                                            𝐹𝑖′                         𝑖
      the exact same number of elements, since their elements are simply relabelings of each other
      via the bijections.
      We also prove that the size of the sets 𝐹 1′, · · · , 𝐹𝑝′ is bounded by 𝑘, the projection size. For
                                                                                                         Ø 𝑝
                                       𝑘+1 is a bijection. For all 𝑗 ∈ {1 · · · 𝑝}, the set 𝐹 ′ is 𝐹 ∪
      all 𝑖, 𝑗, |Δ𝑖,𝑗 | = |𝐹𝑖 | since 𝜇𝑖,𝑘                                                    𝑗     𝑗         Δ𝑖,𝑗 ,
                                                                                                         𝑖=1,𝑖≠𝑗


                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:54                                                                                             Arora et al.


  Algorithm 2: ComputeProjections
   Input: Constraint sets 𝐹 1, · · · , 𝐹𝑝
   Output: Final projections Γ1, · · · , Γ𝑝
 1 for 𝑖 ∈ {1 · · · 𝑝} do
 2     𝐹𝑖′ ← 𝐹𝑖 ;
 3 end
 4 for 𝑗 ∈ {1 · · · 𝑝} do
 5     for 𝑖 ∈ {1 · · · 𝑝}, 𝑖 ≠ 𝑗 do
 6         Δ𝑖,𝑗 ← 𝜇𝑖,𝑗  𝑘+1 (𝐹 ) ;
                              𝑖
 7         𝐹 𝑗 ← 𝐹 𝑗 ∪ Δ𝑖,𝑗 ;
             ′        ′

 8     end
 9 end
10 𝑅 ← Choice(𝑥 1
                      𝑘+1 𝐹 ′ , 𝑘 − |𝐹 ′ |);
                              1       1
11 for 𝑖 ∈ {1 · · · 𝑝} do
12     Γ𝑖 ← 𝐹𝑖′ ∪ 𝜇𝑘+1 1,𝑖 (𝑅);
13 end
14 return Γ1, · · · , Γ𝑝



        whose size is bounded by:
                                                  𝑝
                                                  Ø
                               |𝐹 𝑗′ | = 𝐹 𝑗 ∪             Δ𝑖,𝑗
                                                 𝑖=1,𝑖≠𝑗
                                                    𝑝
                                                   ∑︁
                                    ≤ |𝐹 𝑗 | +              |Δ𝑖,𝑗 |
                                                  𝑖=1,𝑖≠𝑗
                                                    𝑝                  𝑝        
                                                   ∑︁                 ∑︁        𝑛
                                    = |𝐹 𝑗 | +         |𝐹𝑖 | =     |𝐹𝑖 | ≤ 𝑚 +     ≤𝑘
                                               𝑖=1,𝑖≠𝑗         𝑖=1
                                                                                2
      Therefore, the number of constraints in each set does not exceed the projection size 𝑘. On
      line 10, we add any (𝑘 − |𝐹 1′ |) named-axes from 𝑥 1𝑘+1 𝐹 1′ to complete the projection Γ1 . In
      lines 11-13, we add their bijection images to complete the other projections.
    • Construct all 𝑘-ranked components as described above using Γ. Performing a projection
      ensures that the tensor shapes, access maps, and attributes are valid and the precondition is
      satisfied in the 𝑘-ranked counterexample (Theorem 9).
    • Tensor values: For all 𝑖 ∈ {1 · · · 𝑛}, we require 𝑤𝑖 , the value of X𝑘 at the 𝑖 th access, to be same
      as 𝑣𝑖 , the value of X𝑘+1 at the 𝑖 th access. The values at other accesses in X𝑘 are unspecified.
                           
   Thus, 𝑘 = max(𝑚 + 𝑛2 , 1) is a sufficient rank for verifying the rewrite rule 𝑅.
                                                                                                           □

E.4     Arbitrary Number of RClasses
Lemma 6. Let 𝑅 = LHS ⇒𝐶 RHS be a rewrite rule such that
  (1) 𝑅 contains at most one input tensor, denoted X,
  (2) 𝑅 does not contain any of the following operators: reduce, dot, conv, and conv-base,
  (3) 𝑀 is an RClass-rank map for 𝑅 and 𝑐 is an RClass appearing in the rule,
  (4) The scalar function scalarf comprises: (1) 𝑛 accesses to X and (2) 𝑚 conditions.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                     29:55


Let 𝑛 X = 𝑛 if an aggregated-axis of X has RClass 𝑐, and 𝑛 X = 0 otherwise. Then the following holds:
                         
                         𝑛X
               max(𝑚 +       , 1) ≤ 𝑘 ⇒ valid(𝑅, 𝑀 [𝑐 ↦→ 𝑘]) → valid(𝑅, 𝑀 [𝑐 ↦→ 𝑘 +1])
                          2
   Proof. Let 𝑥 1, · · · , 𝑥 𝑝 denote all the aggregated-axes of RClass 𝑐 that appear in the rewrite
rule 𝑅 . Among these, let 𝑥 1, · · · , 𝑥ℎ be the aggregated-axes that index the input tensor X. The
aggregated-axes 𝑥ℎ+1, · · · , 𝑥 𝑝 occur as arguments to operators such as expand but do not index X
directly. All other aggregated-axes in 𝑅 belong to RClasses other than 𝑐. The scalarf of 𝑅 has the
following canonical form, comprising 𝑛 X relevant accesses to X and 𝑚 conditions:
             scalarf (X[𝑥 1 ↦→ fmap( 1𝑒 1, 1 M1 ), · · · , 𝑥ℎ ↦→ fmap(ℎ 𝑒 1, ℎ M1 ) ∪ 𝑌1 ], · · · ,
                          X[𝑥 1 ↦→ fmap( 1𝑒𝑛X , 1 M𝑛X ), · · · , 𝑥ℎ ↦→ fmap(ℎ 𝑒𝑛X , ℎ M𝑛X ) ∪ 𝑌𝑛X ],
                                     𝑝
                                     Û                                        𝑝
                                                                              Û
                                                 𝑗    𝑗
                              𝜙1 ∧         fold( 𝑔1, N1 ), · · · , 𝜙𝑚 ∧             fold( 𝑗 𝑔𝑚 , 𝑗 N𝑚 ))
                                     𝑗=1                                      𝑗=1

where each 𝑗 𝑒𝑖 is an index transformer and each 𝑗 𝑔𝑖 is a condition predicate. The maps 𝑌𝑖 denote
the access maps for the remaining aggregated-axes (those whose RClass is not 𝑐), while formulas
𝜙𝑖 collect the fold-conditions for these remaining aggregated-axes.
   Our goal is to find a sufficient rank 𝑘 for the RClass 𝑐, such that any counterexample at rank 𝑘+1
can be lowered to a counterexample at rank 𝑘. Let 𝑥𝑖𝑘+1 = {1𝑖 , · · · , 𝑘 +1𝑖 } denote a (𝑘 +1)-ranked
instantiation of each aggregated-axis 𝑥𝑖 . Since all aggregated-axes 𝑥 1, · · · , 𝑥 𝑝 belong to the same
RClass 𝑐, there exists a canonical bijection between any pair:
                                𝑘+1
                               𝜇𝑖,𝑗 = MapAxes(𝑐, 𝑥𝑖𝑘+1, 𝑥 𝑘+1    𝑘+1
                                                          𝑗 ) : 𝑥𝑖   ↔ 𝑥 𝑘+1
                                                                         𝑗
  To construct a valid counterexample, we project each aggregated-axis 𝑥𝑖 since they all have the
same RClass and are instantiated to the same rank. Let Γ𝑖 ⊂ 𝑥𝑖𝑘+1 be a projection of size 𝑘 for 𝑥𝑖 .
These projections must be pairwise disjoint and must respect the canonical bijections:
                                        ∀𝑖, 𝑗 ∈ {1 · · · 𝑝},         𝑘+1
                                                                    𝜇𝑖,𝑗 (Γ𝑖 ) = Γ𝑗                               (22)
  Starting from Equation 18, we have:
              ∃ 𝑣 𝑘+1 ∈ 𝑣𝑎𝑟𝑠 𝑘+1, 𝐶 𝑘+1 ∧ valid-expr(LHS𝑘+1 ) ∧ ∃𝐴𝑘+1 ∈ Access(LHS𝑘+1 ),
                             ¬scalarf (𝑣 1, · · · , 𝑣𝑛X , 𝑏 1, · · · , 𝑏𝑚 )
                                                y
                                                
                    ∃ 𝑣 𝑘 ∈ 𝑣𝑎𝑟𝑠 𝑘 , 𝐶 𝑘 ∧ valid-expr(LHS𝑘 ) ∧ ∃𝐴𝑘 ∈ Access(LHS𝑘 ),
                             ¬scalarf (𝑤 1, · · · , 𝑤𝑛X , 𝑐 1, · · · , 𝑐𝑚 )
where,
   • For each 𝑙 ∈ {1 · · · 𝑛 X }, 𝑣𝑙 denotes the 𝑙 th access to X𝑘+1 in the (𝑘 +1)-ranked counterexample:
            𝑣𝑙 = X𝑘+1 [𝑥 1𝑘+1 ↦→ fmap( 1𝑒𝑙 , 1 M𝑙𝑘+1 ), · · · , 𝑥ℎ𝑘+1 ↦→ fmap(ℎ 𝑒𝑙 , ℎ M𝑙𝑘+1 ) ∪ 𝑌𝑙𝑘+1 ]
    • For all 𝑙 ∈ {1 · · · 𝑛 X }, 𝑤𝑙 denotes the 𝑙 th access to X𝑘 in the 𝑘-ranked counterexample:
                   𝑤𝑙 = X𝑘 [𝑥 1𝑘 ↦→ fmap( 1𝑒𝑙 , 1 M𝑙𝑘 ), · · · , 𝑥ℎ𝑘 ↦→ fmap(ℎ 𝑒𝑙 , ℎ M𝑙𝑘 ) ∪ 𝑌𝑙𝑘 ]
    • For each 𝑙 ∈ {1 · · · 𝑚}, 𝑏𝑙 denotes the 𝑙 th condition in the (𝑘 +1)-ranked counterexample:
                                                          𝑝
                                                          Û
                                        𝑏𝑙 = 𝜙𝑙𝑘+1 ∧            fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘+1 )
                                                          𝑗=1


                                Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:56                                                                                                     Arora et al.


    • For all 𝑙 ∈ {1 · · · 𝑚}, 𝑐𝑙 denotes the 𝑙 th condition in the 𝑘-ranked counterexample:
                                                          𝑝
                                                          Û
                                             𝑐𝑙 = 𝜙𝑙𝑘 ∧         fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘 )
                                                          𝑗=1

   We define the 𝑘-ranked components via projections with Γ1, · · · , Γ𝑝 :
                     𝑥 ,··· ,𝑥
    • X𝑘 = X𝑘+1 | Γ11,··· ,Γ𝑝𝑝 ,
                                 𝑥 ,··· ,𝑥
    • 𝑣𝑎𝑟𝑠 𝑘 = 𝑣𝑎𝑟𝑠 𝑘+1 | Γ11,··· ,𝑥𝑝𝑝 ,
                      𝑥 ,··· ,𝑥
    • 𝐴𝑘 = 𝐴𝑘+1 | Γ11,··· ,Γ𝑝𝑝 ,
    • for all 𝑙 ∈ {1 · · · 𝑛 X }, 𝑖 ∈ {1 · · · ℎ}, 𝑖 M𝑙𝑘 = 𝑖 M𝑙𝑘+1 |𝑥Γ𝑖𝑖 ,
                                                𝑥 ,··· ,𝑥
    • for all 𝑙 ∈ {1 · · · 𝑛 X }, 𝑌𝑙𝑘 = 𝑌𝑙𝑘+1 | Γ11,··· ,Γ𝑝𝑝 = 𝑌𝑙𝑘+1 , since 𝑌𝑙 is independent of the RClass 𝑐,
                                                                       𝑥
    • for all 𝑙 ∈ {1 · · · 𝑚}, 𝑗 ∈ {1 · · · 𝑝}, 𝑗 N𝑙𝑘 = 𝑗 N𝑙𝑘+1 | Γ𝑗𝑗 ,
                                              𝑥 ,··· ,𝑥
    • for all 𝑙 ∈ {1 · · · 𝑚}, 𝜙𝑙𝑘 = 𝜙𝑙𝑘+1 | Γ11,··· ,Γ𝑝𝑝 = 𝜙𝑙𝑘+1 , since 𝜙𝑙 is independent of the RClass 𝑐, and
                                                           𝑘 = MapAxes(𝑐, Γ , Γ ) is simply 𝜇 𝑘+1 |𝑥𝑖 . The
    • for all 𝑖, 𝑗 ∈ {1 · · · 𝑝}, the canonical bijection 𝜇𝑖,𝑗                     𝑖 𝑗              𝑖,𝑗 Γ𝑖
      resulting canonical bijections must satisfy:
      – 𝜇𝑖,𝑗
          𝑘 ◦ 𝜇 𝑘 = id, and
                  𝑗,𝑖
      – 𝜇𝑘𝑗,𝑙 ◦ 𝜇𝑖,𝑗
                  𝑘 = 𝜇𝑘 .
                           𝑖,𝑙
      To ensure that these properties hold, we must ensure that Equation 22 is satisfied.
To obtain the 𝑘-ranked counterexample, we project each component of the (𝑘 +1)-ranked coun-
terexample along the projections Γ𝑖 . Components not involving the RClass 𝑐 are unchanged.
   Since 𝐶 𝑘+1 ⇒ 𝐶 𝑘 and valid-expr(LHS𝑘+1 ) ⇒ valid-expr(LHS𝑘 ), the precondition remains satis-
fied and the LHS expression remains valid in the 𝑘-ranked counterexample (Theorem 9). What
remains is ensuring equivalence of scalarf arguments in both counterexamples and deriving con-
straints on Γ1, · · · , Γ𝑝 :
                                                                         Ó𝑝
    • Conditions: For all 𝑙 ∈ {1 · · · 𝑚}, we require 𝑐𝑙 = 𝜙𝑙𝑘 ∧ 𝑗=1 fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘 ) and 𝑏𝑙 = 𝜙𝑙𝑘+1 ∧
      Ó𝑝
         𝑗=1 fold( 𝑔𝑙 , N𝑙
                     𝑗    𝑗 𝑘+1 ) must have the same truth value.

      The value of 𝑏𝑙 is known since it depends entirely on the (𝑘 +1)-ranked counterexample. To
      make sure that 𝑐𝑙 and 𝑏𝑙 have the same truth value, it is sufficient to make the truth values
      of 𝑐𝑙′ = 𝑗=1 fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘 ) and 𝑏𝑙′ = 𝑗=1 fold( 𝑗 𝑔𝑙 , 𝑗 N𝑙𝑘+1 ) the same since 𝜙𝑙𝑘 = 𝜙𝑙𝑘+1 . This is
               Ó𝑝                                Ó𝑝
      similar to Lemma 5, and we get at most one constraint on exactly one projection.
      The set of all constraints through the conditions is given by, where 𝑖 𝐶 denotes the constraints
      on Γ𝑖 . Since we get at most 𝑚 constraints partitioned into these 𝑝 sets, we conclude that the
      total number of constraints is bounded by:
                                               | 1𝐶 | + · · · + |𝑝 𝐶 | ≤ 𝑚
    • Accesses: For all 𝑙 ∈ {1 · · · 𝑛 X }, 𝑤𝑙 must be the same as 𝑣𝑙 . The projections Γ1, · · · , Γ𝑝 should
      not lead to inconsistencies with respect to the elements of X𝑘 .
      Consider any arbitrary pair of values 𝑣𝑟 and 𝑣𝑠 , where 𝑟, 𝑠 ∈ {1 · · · 𝑛 X } and 𝑟 ≠ 𝑠. These
      correspond to two accesses to X𝑘+1 . There are 𝑛2X such access pairs. Let 1 𝐷𝑟,𝑠 , · · · , ℎ 𝐷𝑟,𝑠 be the
      constraints we get on Γ1, · · · , Γℎ from this equation, respectively. We exclude ℎ+1 𝐷𝑟,𝑠 , · · · , 𝑝 𝐷𝑟,𝑠
      from the analysis because the corresponding aggregated-axes do not index the tensor X,
      and hence do not introduce any inconsistencies. Thus, their constraints are equal to ∅. The
      following cases arise:
      – 𝑣𝑟 = 𝑣𝑠 : Then any projection will result in a valid counterexample since the lowering will
        not lead to any inconsistency. For this case, 𝑖 𝐷𝑟,𝑠 = ∅ for all 𝑖.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:57


      – 𝑣𝑟 ≠ 𝑣𝑠 : Then these values correspond to different accesses in X𝑘+1 , i.e.,
                {𝑥 1𝑘+1 ↦→ fmap( 1𝑒𝑟 , 1 M𝑟𝑘+1 ), · · · , 𝑥ℎ𝑘+1 ↦→ fmap(ℎ 𝑒𝑟 , ℎ M𝑟𝑘+1 )} ∪ 𝑌𝑟𝑘+1 ≠
                   {𝑥 1𝑘+1 ↦→ fmap( 1𝑒𝑠 , 1 M𝑠𝑘+1 ), · · · , 𝑥ℎ𝑘+1 ↦→ fmap(ℎ 𝑒𝑠 , ℎ M𝑠𝑘+1 )} ∪ 𝑌𝑠𝑘+1
         We require that they also correspond to different accesses in X𝑘 , i.e.,
                      {𝑥 1𝑘 ↦→ fmap( 1𝑒𝑟 , 1 M𝑟𝑘 ), · · · , 𝑥ℎ𝑘 ↦→ fmap(ℎ 𝑒𝑟 , ℎ M𝑟𝑘 )} ∪ 𝑌𝑟𝑘 ≠
                        {𝑥 1𝑘 ↦→ fmap( 1𝑒𝑠 , 1 M𝑠𝑘 ), · · · , 𝑥ℎ𝑘 ↦→ fmap(ℎ 𝑒𝑠 , ℎ M𝑠𝑘 )} ∪ 𝑌𝑠𝑘                  (23)
         Since the accesses do not match in X𝑘+1 , two cases arise: (1) 𝑌𝑟𝑘+1 ≠ 𝑌𝑠𝑘+1 . This implies
         𝑌𝑟𝑘 ≠ 𝑌𝑠𝑘 , ensuring that Equation 23 holds. This case results in no constraints on any
         projection, (2) there exists some aggregated-axis, say 𝑥𝑖𝑘+1 , for 𝑖 ∈ {1 · · · ℎ}, such that its
         corresponding access maps in the two accesses are unequal:
                                   fmap(𝑖 𝑒𝑟 , 𝑖 M𝑟𝑘+1 ) ≠ fmap(𝑖 𝑒𝑠 , 𝑖 M𝑠𝑘+1 )
         We ensure that the access maps of 𝑥𝑖𝑘 are unequal in the two accesses, to ensure that
         Equation 23 holds:
                                  fmap(𝑖 𝑒𝑟 , 𝑖 M𝑟𝑘 ) ≠ fmap(𝑖 𝑒𝑠 , 𝑖 M𝑠𝑘 )
         This is similar to Lemma 4, and we get at most one constraint on Γ𝑖 in 𝑖 𝐷𝑟,𝑠 and no constraints
         on other projections. Therefore, |𝑖 𝐷𝑟,𝑠 | ≤ 1 and 𝑗 𝐷𝑟,𝑠 = ∅ for all 𝑗 ≠ 𝑖.
       Each access pair contributes at most one constraint to exactly one projection. The set of all
       constraints through the accesses is given by, where 𝑖 𝐷 denotes the constraints on Γ𝑖 :
                                       Ø                           Ø
                                1          1
                                  𝐷=          𝐷𝑟,𝑠 , · · · , 𝑝 𝐷 =    𝑝
                                                                        𝐷𝑟,𝑠
                                           (𝑟,𝑠 )                     (𝑟,𝑠 )
                                 𝑛X 
       Since we get at most       2 constraints partitioned into these 𝑝 sets, we conclude that the total
       number of constraints is bounded by:
                                                                  
                                           1                𝑝     𝑛X
                                           | 𝐷| + · · · + | 𝐷| ≤
                                                                   2
  We now define the combined set of constraints (from both conditions and accesses) on each
projection Γ𝑖 as 𝐹𝑖 = 𝑖 𝐶 ∪ 𝑖 𝐷. The total number of constraints across all projections is bounded by:
                       |𝐹 1 | + · · · + |𝐹𝑝 | = | 1𝐶 ∪ 1 𝐷 | + · · · + |𝑝 𝐶 ∪ 𝑝 𝐷 |
                                            ≤ | 1𝐶 | + | 1 𝐷 | + · · · + |𝑝 𝐶 | + |𝑝 𝐷 |
                                        = | 1𝐶 | + · · · + |𝑝 𝐶 | + | 1 𝐷 | + · · · + |𝑝 𝐷 |
                                                   
                                                   𝑛X
                                        ≤𝑚+
                                                    2
                                             𝑛X 
  Similar to Lemma 5, we get max(𝑚 + 2 , 1) ≤ 𝑘 as a sufficient condition for a valid counterex-
ample lowering. Finally, we fully construct the 𝑘-ranked counterexample as follows:
   • Projection: For all 𝑗 ∈ {1 · · · 𝑝}, the named-axes in 𝐹 𝑗 must be a part of the projection Γ𝑗 .
     Additionally, the projections should respect the canonical bijections of the (𝑘 +1)-ranked
     counterexample. We compute the final projections using the ComputeProjections routine
     described in Algorithm 2.
   • Construct all 𝑘-ranked components as described above using Γ. Performing a projection
     ensures that the tensor shapes, access maps, and attributes are valid and the precondition is
     satisfied in the 𝑘-ranked counterexample (Theorem 9).

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:58                                                                                                Arora et al.


     • Tensor values: For all 𝑖 ∈ {1 · · · 𝑛 X }, we require 𝑤𝑖 , the value of X𝑘 at the 𝑖 th access, to be same
       as 𝑣𝑖 , the value of X𝑘+1 at the 𝑖 th access. The values at other accesses in X𝑘 are unspecified.
                             
    Thus, 𝑘 = max(𝑚 + 𝑛2X , 1) is a sufficient rank for the RClass 𝑐.
                                                                                                               □

E.5     Arbitrary Number of Tensors
Lemma 7. Let 𝑅 = LHS ⇒𝐶 RHS be a rewrite rule such that
  (1) 𝑅 does not contain any of the following operators: reduce, dot, conv, and conv-base,
  (2) 𝑀 is an RClass-rank map for 𝑅 and 𝑐 is an RClass appearing in the rule,
  (3) 𝑅 contains 𝑞 tensors X1, · · · , X𝑞 that have an aggregated-axis belonging to the RClass 𝑐,
  (3) The scalar function scalarf comprises: (1) 𝑛 X𝑖 accesses to X𝑖 and (2) 𝑚 conditions.
Then the following holds:
                      𝑞      
                     ∑︁  𝑛 X𝑖
          max(𝑚 +               , 1) ≤ 𝑘 ⇒ valid(𝑅, 𝑀 [𝑐 ↦→ 𝑘]) → valid(𝑅, 𝑀 [𝑐 ↦→ 𝑘 +1])
                     𝑖=1
                          2
   Proof. Only tensors that contain an aggregated-axis belonging to the RClass 𝑐 can introduce
constraints that on the sufficient rank for 𝑐. Accesses to any other tensors retain their values during
the counterexample lowering, and hence do not contribute to the bound. For each tensor X𝑖 that
contains an aggregated-axis with the RClass 𝑐, every pair of its accesses can introduce at most one
constraint to exactly one projection. Therefore, the total number of constraints through accesses of
X𝑖 is bounded by 𝑛2X𝑖 .
   The contributions from different tensors are summed independently because accesses across
tensors do not lead to any constraints (we assume that distinct tensors do not alias; more §G).
Consequently, the total number of constraints is simply bounded by sum of per-tensor contribu-
tions, together with the 𝑚 constraints from the conditions in the worst case. The counterexample
construction is similar to Lemma 6. We introduce a routine TensorsWithRClass which takes an
RClass 𝑐 and returns all the input tensors which have an aggregated-axis belonging to 𝑐. For each
tensor, we use the NumTensorAccess
                          Í𝑞            routine to get the number of distinct accesses to that tensor.
   Thus, 𝑘 = max(𝑚 + 𝑖=1 𝑛2X𝑖 , 1) is a sufficient rank for the RClass 𝑐 to verify the rewrite rule 𝑅,
where {X1, · · · , X𝑞 } = TensorsWithRClass(𝑐) and 𝑛 X𝑖 = NumTensorAccess(X𝑖 ).                       □

F     Preconditions
In this section, we prove that if the precondition holds in the (𝑘 +1)-ranked counterexample, then
the precondition holds in the 𝑘-ranked counterexample, i.e., 𝐶 𝑘+1 ⇒ 𝐶 𝑘 .

F.1     A Language for Preconditions
We first define a simple language for preconditions and a useful substitution lemma.
Definition 10 (Precondition language). Let A be a set of atomic propositions (atoms). We define a
language Φ∧,∨ by the grammar:
                                           𝜙 ≔ 𝑎 ∈ A | 𝜙 ∧𝜙 | 𝜙 ∨𝜙
Similarly, the language Φ∧ is defined by the grammar:
                                                𝜙 ≔ 𝑎 ∈ A | 𝜙 ∧𝜙
Note that Φ∧ ⊆ Φ∧,∨ .
   We write 𝜙 {𝑏/𝑎} for the formula obtained from 𝜙 by simultaneously replacing every occurrence
of atom 𝑎 by atom 𝑏 (also called a substitution).

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:59


Lemma 8 (Substitution Monotonicity). Let 𝜙 ∈ Φ∧,∨ and let 𝑎, 𝑏 ∈ A be atoms. If the implication
𝑎 ⇒ 𝑏 holds, then
                                       𝜙 ⇒ 𝜙 {𝑏/𝑎}
The same holds for Φ∧ .
  Proof. By structural induction on 𝜙.
Basis. If 𝜙 = 𝑎, then 𝜙 {𝑏/𝑎} = 𝑏, and the claim follows from the hypothesis 𝑎 ⇒ 𝑏. If 𝜙 = 𝑐 for
𝑐 ≠ 𝑎, then 𝜙 {𝑏/𝑎} = 𝑐 and 𝑐 ⇒ 𝑐 holds trivially.
Inductive step.
    • If 𝜙 = 𝜙 1 ∧ 𝜙 2 , then by the induction hypothesis, 𝜙𝑖 ⇒ 𝜙𝑖 {𝑏/𝑎} for 𝑖 = 1, 2. Since 𝜙 {𝑏/𝑎} =
      𝜙 1 {𝑏/𝑎} ∧ 𝜙 2 {𝑏/𝑎} and 𝜙 1 ∧ 𝜙 2 ⇒ 𝜙 1 {𝑏/𝑎} ∧ 𝜙 2 {𝑏/𝑎}, we obtain the desired implication.
    • If 𝜙 = 𝜙 1 ∨ 𝜙 2 , similarly the induction hypothesis yields 𝜙 1 ∨ 𝜙 2 ⇒ 𝜙 1 {𝑏/𝑎} ∨ 𝜙 2 {𝑏/𝑎}.
This completes the induction proof.                                                                   □

F.2   Conditions in TensorRight
The preconditions in TensorRight are drawn from the language Φ∧,∨ (Definition 10), whose atoms
A consist precisely of all fold-conditions. The expression validity conditions (such as those returned
by valid-expr) are drawn from Φ∧ .
  The fold construct takes a predicate and applies it pointwise to a list of maps with the same
domains. It returns true if all predicate values are true, and false otherwise. It is defined as:
                                                      Û
                        fold(𝑔, [𝑚 1, 𝑚 2, · · · ]) =      𝑔(𝑚 1 (𝑖), 𝑚 2 (𝑖), · · · )
                                                        𝑖 ∈dom(𝑚 1 )

Theorem 9. Let 𝐶 𝑘+1, 𝐶 𝑘 ∈ Φ  ∧,∨ be the preconditions obtained from the same symbolic precondi-
tion 𝐶 by instantiating every fold over a RClass 𝑐 at rank 𝑘 +1 and at rank 𝑘, respectively During
the counterexample construction, each (𝑘 +1)-fold is projected to the corresponding 𝑘-fold. Then,
                                                    𝐶 𝑘+1 ⇒ 𝐶 𝑘
Similarly, for any tensor expression 𝑒, valid-expr(𝑒 𝑘+1 ) ⇒ valid-expr(𝑒 𝑘 ).
  Proof. It suffices to show the implication for each atomic fold and then lift it to the whole
precondition using Lemma 8.
  Let 𝑓 𝑘+1 = fold(𝑔, N 𝑘+1 ) be one of the atomic folds in 𝐶 𝑘+1 , defined over an aggregated-axis in
RClass 𝑐. Let N𝑙𝑘+1 = [𝑚𝑘+1
                          1 , 𝑚 2 , · · · ]. It has the form:
                                 𝑘+1

                                                     𝑘+1
                                                     Û
                            fold(𝑔, N 𝑘+1 ) =                   𝑔(𝑚𝑘+1     𝑘+1
                                                                   1 (𝑖), 𝑚 2 (𝑖), · · · )
                                                 𝑖 ∈dom(𝑚 1 )

Let Γ be the chosen projection of size 𝑘 and let N 𝑘 = N 𝑘+1 |𝑥Γ denote the projected maps. Then:
                          N𝑙𝑘 = N𝑙𝑘+1 |𝑥Γ = [𝑚𝑘+1 𝑥    𝑘+1 𝑥                𝑘     𝑘
                                              1 | Γ , 𝑚 2 | Γ , · · · ] = [𝑚 1 , 𝑚 2 , · · · ]

The corresponding fold 𝑓 𝑘 = fold(𝑔, N 𝑘 ) in 𝐶 𝑘 has the form:
                                              Û
                             fold(𝑔, N 𝑘 ) =      𝑔(𝑚𝑘1 ( 𝑗), 𝑚𝑘2 ( 𝑗), · · · )
                                                      𝑗 ∈Γ

  Since 𝑓 𝑘+1 is a conjunction over a superset of indices, if the larger conjunction if true, then
sub-conjunction is true, i.e.:
                                                     𝑓 𝑘+1 ⇒ 𝑓 𝑘

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
29:60                                                                                      Arora et al.


   Thus every (𝑘 +1)-fold atom implies its projected 𝑘-fold atom. Applying Lemma 8 repeatedly to
substitute each (𝑘 +1)-fold atom by its projected counterpart in the whole precondition implies
𝐶 𝑘+1 ⇒ 𝐶 𝑘 , as required. The same holds for validity conditions returned by valid-expr.      □

G       Discussion
   Rewrite Rules with Reductions. So far, we have assumed that rewrite rules do not contain any
of the following operators: reduce, dot, conv, and conv-base. These operators share a common
characteristic: they perform reductions or accumulations over one or more axes. Because the axes
being reduced may have unbounded sizes, we cannot simply expand the reduction and operate
over all elements explicitly. Instead, we treat the reduction sum symbolically and provide special
handling for such elements during verification. Moreover, the user supplies a bijection between
the LHS and RHS reduction elements, which allows us to reason about them abstractly. Once this
is done, the rule can be symbolically evaluated as usual, and all of our previous results regarding
sufficient rank and counterexample lowering continue to hold.
   Counting Non-Trivial Conditions. We introduced a simplifying assumption (for notational ease)
in §D that every condition in a rule is uniformly represented as a conjunction of one fold per
aggregated-axis, regardless of whether that aggregated-axis contributes meaningful conditions. In
practice, some conditions may be trivial: their associated fold is degenerate and therefore impose
no constraints. Such conditions should not contribute to the sufficient rank computation.
   To account for this, we introduce a routine NumConds which takes an RClass 𝑐 and returns
the number of conditions having an aggregated-axis belonging to the RClass 𝑐 and whose fold is
non-trivial. Only these conditions are relevant and contribute to the sufficient rank of 𝑐.
   Putting it all Together. After relaxing all the assumptions from §C.1, we come up with the
following lemma:
Lemma 10. Let 𝑅 be any rewrite rule written in TensorRight DSL. Let 𝑚 be an RClass-rank map
for 𝑅 and 𝑐 be an RClass appearing in 𝑅. If 𝑘 = InferBound(𝑅, 𝑐), then
                              ∀𝑖 ≥ 𝑘, valid(𝑚[𝑐 ↦→ 𝑖]) → valid(𝑚[𝑐 ↦→ 𝑖 +1])
  In other words, for all 𝑖 ≥ 𝑘 and for any ranks of the other RClasses, if the rule is valid when 𝑐
has rank 𝑖, then it implies that the rule is valid when 𝑐 has rank 𝑖 +1. The InferBound routine is
described in Algorithm 3.
  RHS Expression Validity. Our definition of rewrite rule validity (Definition 6) states that the
LHS and RHS expressions should be equal for all variable valuations, given the precondition 𝐶
holds and the LHS expression is valid, i.e., valid-expr(LHS) holds. In reality, we require a stronger
postcondition that the RHS expression should be valid, i.e., valid-expr(RHS) holds. On taking
contrapositives and considering (𝑘 +1)- and 𝑘-ranked instantiations, we get:
                     ∃ 𝑣 𝑘+1 ∈ 𝑣𝑎𝑟𝑠 𝑘+1, 𝐶 𝑘+1 ∧ valid-expr(LHS𝑘+1 )
                                                                       
                                   ∧ LHS𝑘+1 ≠ RHS𝑘+1 ∨ ¬valid-expr(RHS𝑘+1 )
                                                     y
                                                     
                          ∃ 𝑣 𝑘 ∈ 𝑣𝑎𝑟𝑠 𝑘 , 𝐶 𝑘 ∧ valid-expr(LHS𝑘 )
                                                                 
                                   ∧ LHS𝑘 ≠ RHS𝑘 ∨ ¬valid-expr(RHS𝑘 )

    Thus there are two distinct kinds of counterexamples to lower from rank 𝑘 +1 to 𝑘:

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
TensorRight: Automated Verification of Tensor Graph Rewrites                                                    29:61


  Algorithm 3: Sufficient Rank for an RClass
   Inputs : Rewrite rule 𝑅 & RClass 𝑐
   Output : 𝑏𝑜𝑢𝑛𝑑, i.e., a sufficient rank for 𝑐
 1 Function InferBound (𝑅, 𝑐) :
 2    𝑏𝑜𝑢𝑛𝑑 ← 0;
 3    𝑡𝑒𝑛𝑠𝑜𝑟𝑠 ← TensorsWithRClass(𝑅, 𝑐);
 4    for 𝑡 ∈ 𝑡𝑒𝑛𝑠𝑜𝑟𝑠 do
 5        𝑛 ← NumTensorAccess(𝑅, 𝑡);
 6        if 𝑛 > 1 then              
 7            𝑏𝑜𝑢𝑛𝑑 ← 𝑏𝑜𝑢𝑛𝑑 + 𝑛2 ;
 8        end
 9    end
10    𝑏𝑜𝑢𝑛𝑑 ← 𝑏𝑜𝑢𝑛𝑑 + NumConds(𝑅, 𝑐);
11    return Max(𝑏𝑜𝑢𝑛𝑑, 1)
12 End Function



    • Mismatch counterexamples: If ⟦LHS⟧ ≠ ⟦RHS⟧ in rank 𝑘 +1, then we lower to a witness of
       ⟦LHS⟧ ≠ ⟦RHS⟧ in rank 𝑘. This is handled in §E: the sufficient rank given by Algorithm 3
       guarantees a counterexample lowering for this case.
    • RHS invalidity counterexamples: If ¬valid-expr(RHS) holds in rank 𝑘 +1, then we lower to a
       witness of ¬valid-expr(RHS) in rank 𝑘. The condition valid-expr(RHS) lies in the fragment
       Φ∧ , i.e., it is a conjunction of fold-atoms. As in the condition-analysis (Lemma 3), any (𝑘 +1)-
       ranked falsifying fold-conjunction contains at least one fold, say 𝑓 𝑘+1 , whose truth value if
       false. To ensure that valid-expr(RHS𝑘 ) is false, we ensure that 𝑓 𝑘 is false. This can be done
       by choosing an appropriate named-axis, giving a sufficient rank of 1.
   For worst–case bounds we take the maximum of the two cases. Since each branch is already at
least 1, the sufficient rank given by Algorithm 3 remains unchanged.
   Input Tensor Aliasing in Tensor Graph Rewrites. Our analysis in Lemma 7 assumes that distinct
input tensors do not alias. For example, in the tensor expression 𝑒 = binary(+, X, Y), we assume
that X and Y are different tensors. In such a case, during counterexample construction, accesses to
different tensors are treated as independent, and no cross-tensor constraints arise. Therefore, the
sufficient rank decomposes cleanly into the sum of per-tensor contributions.
   However, a compiler matching a symbolic expression 𝑒 inside a tensor computation graph, may
encounter a match such as binary(+, 𝑡, 𝑡), where both operands refer to the same concrete tensor.
This breaks the independence assumption: accesses that originate syntactically from different
tensors may in fact refer to the same underlying source, thereby introducing additional cross-
tensor interactions. To account for such cases, (1) one can verify a different rewrite capturing the
aliasing relation, or (2) adjust the sufficient rank to account for additional cross-tensor interactions
and constraints introduced from them. More specifically, for tensors X1Í, · · · , X𝑞 with 𝑛 X1 , · · · , 𝑛 X𝑞
                                                                                                          
number of accesses, respectively, the new constraints are bounded by 𝑖 2𝑛X𝑖 , instead of 𝑖 𝑛2X𝑖 .
                                                                                                Í




                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 29. Publication date: January 2025.
