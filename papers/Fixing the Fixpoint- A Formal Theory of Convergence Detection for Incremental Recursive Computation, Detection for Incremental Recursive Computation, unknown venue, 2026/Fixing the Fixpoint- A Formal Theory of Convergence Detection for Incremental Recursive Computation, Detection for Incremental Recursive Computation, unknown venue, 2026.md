                                         Fixing the Fixpoint: A Formal Theory of Convergence
                                         Detection for Incremental Recursive Computation
                                         CHENGXI YANG∗ , University of Wisconsin–Madison, USA and Shanghai Jiao Tong University, China
                                         TEJ CHAJED† , University of Wisconsin–Madison, USA
                                         THOMAS REPS, University of Wisconsin–Madison, USA
                                         Modern incremental computation theories like DBSP have enabled efficient incrementalization of general
                                         recursive computations. To do so, they require a runtime Fixpoint Detection (FPD) mechanism to detect
arXiv:2610.00530v1 [cs.PL] 30 Sep 2026




                                         whether an iterative computation has reached the fixpoint and thus should terminate. However, we show that
                                         the commonly suggested “FirstZero” strategy is unsound even in naturally arising cases, and that exact FPD is
                                         impossible for arbitrary DBSP circuits with expressive primitive nodes. This issue reveals a fundamental gap
                                         between the mathematical specification and implementations of such theories. To fill this gap, using DBSP as
                                         a core calculus, we develop a formal theory of convergence detection. Within this theory, we define internal
                                         convergence (IntConv) as a declarative criterion corresponding to the internal-state-stability strategy used by
                                         practical implementations, and prove that IntConv is a sufficient condition for external convergence. We then
                                         define the state fixpoint (StFP) predicate and a sound and complete StFP detector. Combining the StFP detector
                                         with fixed-input and zero-output checks yields a sound and complete IntConv detector. Moreover, for a large
                                         class of useful circuits (programs) including Datalog queries, nested while queries, and their incrementally
                                         optimized versions, we show that IntConv is not only sound but also complete (meaning any convergence in
                                         the theory implies the convergence in our criterion). As a result, our theory provides semantic guarantees for
                                         convergence detection on all these circuits. Our results are formally verified in Lean, with the formalization
                                         available at https://github.com/Arcadia-Y/fixing-the-fixpoint/.
                                         CCS Concepts: • Software and its engineering → Incremental compilers; • Theory of computation →
                                         Streaming models; Database query processing and optimization (theory).
                                         Additional Key Words and Phrases: fixpoint detection, stream-based computing, incremental recursive compu-
                                         tation

                                         1   Introduction
                                         Incremental computation [23, 29] is a cornerstone of efficient software systems. Its fundamental
                                         premise is straightforward: when the input to a computation changes, the system should update
                                         the output by processing only the small changes (or “deltas”), rather than recomputing the entire
                                         result from scratch. This principle finds its most classical application in databases in the form of
                                         Incremental View Maintenance (IVM) [10, 20], as shown in Fig. 1(a). For standard relational queries,
                                         IVM is well-understood and widely deployed, allowing systems to maintain up-to-date views with
                                         significantly reduced cost compared to recomputation.
                                            However, modern data analysis has evolved beyond simple relational queries. Applications
                                         ranging from graph analytics to machine learning rely heavily on algorithms that are iterative or
                                         recursive in nature. As a simple example, consider the simple recursive query 𝑄 for computing the
                                         transitive closure of a finite directed graph, expressed in Datalog as follows:
                                         // Edge relation with head and tail
                                         input relation E ( h : Node , t : Node )
                                         // Reach relation with source s and sink t
                                         ∗ Now at University of California, Berkeley. This work was done while an undergraduate at Shanghai Jiao Tong University

                                         and a research intern at UW-Madison.
                                         † Now at Google DeepMind. Work done while at UW-Madison.


                                         Authors’ Contact Information: Chengxi Yang, chengxi@berkeley.edu, University of California, Berkeley; Tej Chajed,
                                         chajed@wisc.edu, Google DeepMind; Thomas Reps, reps@cs.wisc.edu, University of Wisconsin–Madison.
2                                                                                                                  Yang et al.


                      𝑄
         𝐷𝐵 0                    𝑉0
                                                         𝐹              𝐹                𝐹             𝐹
                      𝑄Δ                        𝐷𝐵              𝑉1             𝑉2             ...              𝑉
             Δ𝐷𝐵 1         Δ𝑉1                                                                      fixpoint

         𝐷𝐵 1                    𝑉1                                          𝑄 = fix 𝐹


     Fig. 1. (a) Incremental view maintenance; (b) iterative fixpoint computation for a recursive query.

output relation R ( s : Node , t : Node )
R (x , y ) : - E (x , y ).
R (x , y ) : - E (x , z ) , R (z , y ).

   The semantics of this recursive query is defined in terms of the non-recursive query 𝐹𝐸 (𝑅) :=
𝐸 ∪ (𝐸 ◦ 𝑅). The result of the recursive query, 𝑄, is defined as the least fixpoint of the equation
𝑥 = 𝐹𝐸 (𝑥). In this case, the process of finding the least fixpoint can be understood in terms of
shortest distances: if 𝑅𝑛 consists of pairs of nodes for which the length of the shortest connecting
path is ≤ 𝑛, then 𝐹𝐸 (𝑅𝑛 ) = 𝑅𝑛+1 consists of pairs of nodes whose shortest distance is ≤ 𝑛 + 1;
consequently, the least fixpoint is the transitive closure of the graph. This intuition corresponds to
the following iterative computation strategy: repeatedly apply 𝐹𝐸 to the accumulated result until a
fixpoint is reached, as shown in Fig. 1(b) (often called Kleene iteration).
   It is challenging, however, to combine incremental computation with recursion to efficiently in-
crementalize recursive queries—that is, in our example, to update the graph and efficiently recompute
the new transitive closure. Luckily, frameworks such as DBSP [6] and Differential Dataflow [26]
give elegant theories for efficient incrementalization of general recursive queries. However, we find
that there is a fundamental gap between their mathematical specification and implementations
of such frameworks, having to do with detecting fixpoints. The Fixpoint Detection (FPD) problem
actually involves two issues:
    (1) If the choice of primitive nodes makes DBSP Turing-complete, exact FPD for arbitrary
        circuits is impossible: there is a fixed level-1 circuit with no computable detector that is both
        sound and complete (§4.2).
    (2) In the DBSP paper [6], the authors suggest that for many practical queries, including Datalog
        queries, a key primitive for fixpoint detection can be implemented by an iterative procedure
        that can be stopped when the first “0” is encountered (e.g., the first ∅ when working with
        sets), which intuitively implies that there is no change in two adjacent results. We call
        this the FirstZero strategy. However, in §2.1 (and formalized in §4.1), we show that the
        FirstZero strategy is unsound, including in naturally arising cases; that is, using it in the
        implementation results in output that does not match the mathematical specification.
   These issues are not confined to DBSP; as discussed in §9, similar problems exist in other frame-
works supporting incrementalization of general recursive queries, such as Differential Dataflow [26].
   To fill in this gap, we develop a formal theory of convergence detection using DBSP as a core
calculus. Within this theory, we define internal convergence (IntConv) as a declarative convergence
criterion corresponding to the internal-state-stability strategy used by practical implementations
such as Feldera [14]. We show that IntConv is a sound criterion, so it never produces an incorrect
answer (§5).1 At the end of §5, we give a theoretical data-dependency example in which relying
only on external convergence can require recursive trace-backs and additional retained state. This
example motivates an implementation benefit of IntConv. To connect this declarative criterion to
1 Because exact FPD for arbitrary circuits is impossible, IntConv is not complete for general circuits. Consequently, there

can be computations that mathematically converge, but convergence is not detected by the IntConv criterion.
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation                  3


runtime state, we define the State Fixpoint (StFP) predicate and provide a sound and complete StFP
detector (§6). StFP and the StFP detector give semantic and algorithmic formalizations, respectively,
of the internal-state-stability strategy in our denotational model. The global IntConv detector
combines the StFP detector with fixed-input and zero-output checks across all bracketed sub-
circuits, yielding sound and complete IntConv detection. Because the predicate and StFP detector are
structural, our formulation applies compositionally to nested recursive computations; §9 compares
this capability with the Feldera implementation [14]. Moreover, we show that IntConv is complete—
i.e., it detects convergence whenever the theoretical specification does—for a large class of useful
circuits (§7). In particular, we use regular circuits as a name for the standard DBSP recursive
sublanguage generated by lifted scalar circuits, composition, Datalog queries, and while queries.
We then show that IntConv is complete for regular circuits and their incrementally optimized
versions.2 As a result, sound and complete convergence detection is possible for all these useful
circuits.
   Our key results are formally verified in Lean 4 [11]. Our Lean 4 development is described in §8;
all mechanized proofs are available as anonymous supplementary material.
   In summary, our contributions are as follows:
      • We identify and formalize the Fixpoint Detection (FPD) problem in DBSP, showing that the
        commonly used FirstZero criterion is unsound in general and that exact FPD is impossible
        for arbitrary expressive circuits.
      • We define internal convergence (IntConv) as a declarative criterion corresponding to the
        internal-state-stability strategy used by Feldera-style implementations, and prove that it is a
        sound and sufficient condition for convergence. We define the State Fixpoint (StFP) predicate
        and a sound and complete StFP detector, giving semantic and algorithmic formalizations
        of this strategy. Combining the StFP detector with fixed-input and zero-output checks
        across all bracketed sub-circuits yields a sound, complete, and compositional global IntConv
        detector.
      • We show that IntConv is a complete criterion for a large class of useful circuits, including
        all regular circuits and their incrementally optimized forms. As a result, exact convergence
        detection is possible for these circuits despite its impossibility for the full language.
      • We formally verify our key results in Lean.

2     Overview
2.1    DBSP and the Unsoundness of the FirstZero Strategy
To lay the groundwork for the problems that we address, we first discuss how DBSP implements
and incrementalizes the Datalog query for transitive closure (§1) in three steps. DBSP uses circuits
to express computations. It first compiles the query into a “naive” circuit, then optimizes it into a
“semi-naive” circuit, and finally optimizes it further into a “delta-of-deltas” circuit. What matters for
our purposes is what is computed incrementally in these circuits; Figure 2 depicts the intermediate
results of the evaluation for one graph and one update to it. In the figure, the vertical dimension
represents changes to the input, i.e., the outer iterations for incremental computation (e.g., we
add a green edge to the first input 𝐺 0 to get the second input 𝐺 1 ), while the horizontal dimension
represents the inner iterations for fixpoint computation (e.g., we apply the single-step query 𝐹 to
𝐺 0 to get 𝐺 01 ). The goal after each outer iteration 𝑚 is to obtain the transitive-closure “view” for
graph 𝐺𝑚 .

2 I.e., if a computation of such a circuit mathematically converges, convergence will always be detected by the IntConv

criterion.
4                                                                                                     Yang et al.


            Inner

    Outer




                    Naive                          Semi-naive                       Delta-of-deltas

Fig. 2. Intermediate-evaluation results arising in the three DBSP strategies for incrementalizing a transitive-
closure query.

    The naive strategy is not optimized for incremental computation at all: for each outer iteration,
it re-runs the entire fixpoint computation from scratch; on each inner iteration, it merely applies
the non-recursive query 𝐹 to intermediate results (until the inner-iteration fixpoint is obtained).
Its intermediate result in the 𝑛 th inner iteration of the 𝑚 th outer iteration 𝐺𝑚  𝑛 is the set of pairs of

nodes whose distance is within 𝑛 + 1 in 𝐺𝑚 .
    The semi-naive strategy optimizes the naive strategy along the horizontal dimension (inner
iterations). The name comes from the Datalog semi-naive evaluation strategy (Algorithm 2 from the
book [18]). It computes inner-iteration deltas of the intermediate results of the naive strategy (e.g.,
𝐺 0Δ1 = 𝐺 01 −𝐺 0 contains only the blue edge). The intermediate result 𝐺𝑚 Δ𝑛 , for 𝑛 ≥ 1, consists of pairs

of nodes whose distance is exactly 𝑛 + 1 in 𝐺𝑚 . In each outer iteration, when the inner-fixpoint is
reached, the intermediate results can be collected—e.g., 𝐺 1 ∪ 𝐺 1Δ1 ∪ 𝐺 1Δ2 —to obtain the final result.
    The delta-of-deltas strategy further incrementalizes the semi-naive strategy along the outer
iterations by computing outer-iteration deltas of the inner-iteration deltas (e.g., Δ𝐺 1Δ1 = 𝐺 1Δ1 − 𝐺 0Δ1
contains only the yellow edge). For each outer iteration, it accepts the delta of the input graph
(e.g., Δ𝐺 1 ), and upon obtaining the inner fixpoint, the inner-iteration intermediate results can be
collected to obtain the delta of the transitive-closure view. For instance, for outer iteration 1, the
delta of the view is the three pairs in Δ𝐺 1 ∪ Δ𝐺 1Δ1 ∪ Δ𝐺 1Δ2 . Note that this value equals 𝐺 12 − 𝐺 02 .
    To produce correct answers, all three strategies need a common component we call Fixpoint
Detection (FPD): a runtime mechanism to detect whether an inner-iteration computation has
already reached a fixpoint, at which point, it can terminate the current inner iteration, collect the
intermediate results (for the semi-naive and delta-of-deltas strategies), and proceed to the next
outer iteration.
    In the DBSP theory, FPD and inner-iteration collection is encapsulated in a mathematical operator
called stream elimination, denoted by ∫ , which takes an infinite stream 𝑠 ∈ (S𝐴 := N → 𝐴)
representing the intermediate results of an unbounded iterative computation, and produces a scalar
value 𝑎 ∈ 𝐴 representing the integrated final result. Intuitively, ∫ (𝑠) is defined to return the sum of
all non-zero elements in 𝑠. ∫ can only be defined as a partial function: it only produces an answer for
streams that have a finite number of non-zero elements (in which case we say that ∫ (𝑠) converges).
When ∫ (𝑠) diverges, the implementation can simply run forever or terminate after a timeout. Either
is semantically consistent: DBSP is designed to be Turing-complete [6] due to unbounded loops.
The question that really matters is “how can the system detect when a stream 𝑠 is all zeros beyond
some point?” in which case ∫ (𝑠) indeed converges, and the semantics demands that the answer
be produced. The challenge is that the implementation has only a finite prefix of 𝑠 at run time,
and it must concretely decide all subsequent values of 𝑠 are zero, but there are infinitely many of
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation                            5


                                         1                4         1        6       4




                                         2                3         2        5       3



Fig. 3. A pair of input graphs that demonstrate that the FirstZero criterion applied to the delta-of-
deltas strategy computes an incorrect answer. Instead of the correct transitive closure of 𝐺 1 , namely,
{(1, 5), (2, 6), (5, 3), (6, 4), (1, 3), (2, 4)}, we would obtain {(1, 5), (2, 6), (5, 3), (6, 4), (1, 3), (2, 4), (1, 4)}.

them. Finding a way to establish 𝑠 has finitely many non-zero values based on a finite prefix is the
essence of the FPD problem in DBSP.
    In the DBSP paper [6], the authors suggest that for many practical queries including the Datalog
queries, ∫ can be “approximated without loss of precision by integrating until it encounters the first
0”. We call this criterion for deciding convergence the FirstZero criterion (or FirstZero strategy).
    For the naive and the semi-naive strategies,3 the FirstZero criterion is indeed a sound criterion,
because the first zero in the delta stream (𝐺𝑚          Δ𝑛 = 0) implies that the fixpoint of the original stream

has been reached (𝐺𝑚      𝑛 = 𝐹 (𝐺 𝑛−1 ) = 𝐺 𝑛−1 ), so 𝐺 Δ𝑝 , for 𝑝 ≥ 𝑛 must all be zero.
                                     𝑚          𝑚          𝑚
    However, for the delta-of-deltas strategy, the FirstZero criterion is, in general, incorrect. That is,
if a runtime executes the stream elimination operator ∫ in a DBSP operator by summing until the
first zero, it produces an incorrect result on some inputs where there are more non-zero elements
that should be summed; there is a convergence point in the input, but it is further ahead in the
stream than the first zero.
    For a concrete example where FirstZero produces an incorrect answer, consider the two graphs
𝐺 0 and 𝐺 1 shown in Fig. 3. In DBSP, the delta between two databases can have negative quantities,
representing deletions. For 𝐺 0 and 𝐺 1 , the delta Δ𝐺 1 consists of negative edges {(1, 2), (2, 3), (3, 4)}
and positive edges {(1, 5), (2, 6), (5, 3), (6, 4)}. Note that after the first step of the semi-naive strategy,
𝐺 0Δ1 and 𝐺 1Δ1 are exactly the same (the positive red edges {(1, 3), (2, 4)}). Consequently, after the
first step of the delta-of-deltas strategy, 𝐺 0Δ1 consists of {(1, 3), (2, 4)} and Δ𝐺 1Δ1 = 𝐺 1Δ1 − 𝐺 0Δ1 = ∅
(because subtraction operates over Z-sets, elements with identical positive counts cancel out)—i.e.,
it is the first zero, so the FirstZero criterion would say, incorrectly, that the inner-iteration fixpoint
for Δ𝐺 1 has been reached.
    When the delta-of-deltas strategy is properly performed, Δ𝐺 1Δ1 is ∅, but the subsequent Δ𝐺 1Δ2 is
not ∅: 𝐺 0Δ2 consists of the blue edge {(1, 4)}, and thus Δ𝐺 1Δ2 consists of the negative blue edge {(1, 4)}.
Only when we get to 𝐺 0Δ3 and Δ𝐺 1Δ3 do we have ∅ at corresponding inner-iteration spots of both outer
iterations. The collected inner-iteration intermediate results are Δ𝐺 1 ∪ Δ𝐺 1Δ1 ∪ Δ𝐺 1Δ2 ∪ Δ𝐺 1Δ3 , which
has negative edges {(1, 2), (2, 3), (3, 4), (1, 4)} and positive edges {(1, 5), (2, 6), (5, 3), (6, 4)}. When
combined with the transitive closure of 𝐺 0 , i.e., positive edges {(1, 2), (2, 3), (3, 4), (1, 3), (2, 4), (1, 4)},
we obtain the transitive closure of 𝐺 1 , {(1, 5), (2, 6), (5, 3), (6, 4), (1, 3), (2, 4)}.
    In contrast, the FirstZero criterion produces an incorrect result. The collected inner-
iteration intermediate results are Δ𝐺 1 ∪ Δ𝐺 1Δ1 , which has negative edges {(1, 2), (2, 3), (3, 4)}
and positive edges {(1, 5), (2, 6), (5, 3), (6, 4)}. When combined with the transitive closure of
𝐺 0 , i.e., positive edges {(1, 2), (2, 3), (3, 4), (1, 3), (2, 4), (1, 4)}, we obtain the incorrect result
{(1, 5), (2, 6), (5, 3), (6, 4), (1, 3), (2, 4), (1, 4)}, which has the extra positive edge (1, 4).



3 In the DBSP circuit for the naive strategy, the intermediate results are in fact first differentiated to become deltas and then

sent to ∫ , so the input to ∫ is the same in the circuits for the naive and semi-naive strategies.
6                                                                                                                                      Yang et al.



                    Global Convergence Detection                  Local Fixpoint Detection
                        for the whole circuit                   for   bracketed sub-circuits        All Circuits
        Theory                                        iff                ExtFP
                            ExtConv                                                                      Conv-complete Circuits
      Specification                                               (with the fixed output 0)
                                                                                                                                   plift,
                                    implies                                      implies                     Regular Circuits     incOpt

          Our                                      defined by             IntFP
        Criterion            IntConv                              (with the fixed output 0)              Incremental Optimized
                                                                                                             Regular Circuits
                                    detects                                      detects

      Our Detection         IntConv                  calls          StFP Detector
       Algorithm            Detector                              (State Fixpoint Detector)



                      (a) Overview of the IntConv theory.                                      (b) Overview of the Conv-complete circuits.

                                    Fig. 4. Overview of the concepts that play a role in our theory.

2.2     Overview of Our Theory
The counter example to the soundness of FirstZero as a convergence criterion in §2.1, together
with the impossibility result in §4.2, reveals a gap between the mathematical theory of DBSP and
its practical implementation. Our theory addresses this gap through a simple progression: specify
convergence mathematically, strengthen that specification to require internal stability, and turn
internal stability into a runtime check. This progression operates at two scales—locally for one
iterative computation and globally for a complete circuit.
   To express these two scales uniformly, we define a core calculus of well-formed DBSP circuits
(§3.2). In this calculus, 𝛿 0 initiates an unbounded iterative computation and ∫ integrates its result; we
call the circuit between them a bracketed circuit. The Fixpoint Detection (FPD) problem asks when
one such bracketed circuit reaches a fixpoint. A complete circuit may contain multiple, potentially
nested bracketed circuits, so the global Convergence Detection problem asks when every bracketed
sub-circuit reaches a fixpoint. We formalize both problems and show that exact FPD is impossible
for arbitrary circuits with expressive primitive nodes (§4). The result does not apply to Datalog or
regular circuits, for which our later completeness theorems yield exact detection.
   Fig. 4a organizes the local and global problems into three layers. At the specification layer, external
fixpoint (ExtFP) says that a circuit’s input and output are fixed after a specified iteration; when
the fixed output is 0, ExtFP is equivalent to the original FPD specification. Its global counterpart,
external convergence (ExtConv), requires every bracketed sub-circuit to converge. At the criterion
layer, inspired by the internal-state-stability criterion used in Feldera [14], internal fixpoint (IntFP)
strengthens ExtFP by requiring every internal node to reach an external fixpoint, and internal
convergence (IntConv) requires the inner circuit of every bracketed sub-circuit to satisfy IntFP
with fixed output 0. Consequently, IntFP implies ExtFP and IntConv implies ExtConv (§5). At the
detection layer, state fixpoint (StFP) connects the internal criterion to the state-oriented check
performed at runtime.
   The distinction between external and internal convergence also provides theoretical evidence
for implementation benefits of IntConv. At the end of §5, we give a data-dependency example in
which an evaluation that relies only on ExtConv can require recursive trace-backs and additional
retained state. This example is a qualitative example, not an empirical performance evaluation or a
general lower bound.
   We show that IntConv is indeed detectable using StFP and a high-level detector (§6). Although
our denotational semantics treats circuits as pure functions, implementations maintain state; StFP
asks whether the circuit would be at an internal fixpoint if its observed input remained fixed. We
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation           7


give a structural StFP detector that is sound and complete for StFP. Together with a fixed-input
check, it yields a local IntFP detector. The sound and complete global IntConv detector applies this
local detector to every bracketed sub-circuit and checks that the fixed output is 0. Because the StFP
detector follows circuit structure, it also applies uniformly to nested bracketed circuits. We will
compare this capability with the Feldera implementation in §9.
   Finally, we identify useful classes of circuits on which the internal and external specifications
coincide, as shown in Fig. 4b. We call a circuit convergence-complete (Conv-complete) when its
ExtConv implies IntConv for every input. On these circuits, the implementable internal criterion
exactly matches the mathematical external convergence specification. We use regular circuits as a
name for the standard DBSP recursive sublanguage generated by lifted scalar circuits, sequential
and parallel composition, Datalog queries, and while queries, including their nested uses. We prove
that regular circuits are Conv-complete. We also formalize DBSP’s incremental optimization as the
syntax-directed transformations plift and incOpt and prove that both preserve Conv-completeness,
yielding the classes summarized in Fig. 4b (§7).

3     Preliminary: A Formal Language for DBSP
In this section, we first introduce the core concepts of DBSP that are necessary to understand the
FPD problem and our solution (§3.1), then present our formal language for DBSP well-formed
circuits (§3.2), and finally show how the Datalog query from §1 is implemented and incrementalized
as an example (§3.3).

3.1    Streams and Operators in DBSP
In this section, we introduce the core DBSP theory, which forms the universe for our language’s
semantics.
Definition 3.1 (Stream). Given an Abelian group (𝐴, +, 0𝐴 , −), a stream of values from 𝐴, or an
𝐴-stream, is a function 𝑠 : N → 𝐴. We denote the set of all 𝐴-streams by S𝐴 = {𝑠 | 𝑠 : N → 𝐴}. We
write 𝑠 [𝑡] for the 𝑡-th element of stream 𝑠.
   Streams inherit the group structure pointwise: (𝑠 1 + 𝑠 2 ) [𝑡] = 𝑠 1 [𝑡] + 𝑠 2 [𝑡], so (S𝐴 , +, 0 S𝐴 , −) is
itself an Abelian group.
Definition 3.2 (Stream Operator). A stream operator is a function 𝑇 : S𝐴1 × · · · × S𝐴𝑛 → S𝐵 .
   In circuit diagrams, we depict stream operators as blocks and streams as arrows.
Definition 3.3 (Lifting). Given a function 𝑓 : 𝐴 → 𝐵, its lifting ↑𝑓 : S𝐴 → S𝐵 applies 𝑓 pointwise
in time: (↑𝑓 ) (𝑠) [𝑡] = 𝑓 (𝑠 [𝑡]). Lifting distributes over composition: ↑(𝑓 ◦ 𝑔) = (↑𝑓 ) ◦ (↑𝑔).
Definition 3.4 (Delay). The delay operator 𝑧 −1 : S𝐴 → S𝐴 shifts a stream by one time step,
inserting zero at 𝑡 = 0: 𝑧 −1 (𝑠) [𝑡] = 0𝐴 if 𝑡 = 0, and 𝑠 [𝑡 − 1] for 𝑡 ≥ 1.
Definition 3.5 (Feedback Cycle). For certain operators 𝑇 : (S𝐴 × S𝐵 ) → S𝐵 and 𝐹 : S𝐵 → S𝐵 , the
equation 𝑄 (𝑠) = 𝑇 (𝑠, 𝐹 (𝑄 (𝑠))) has a unique solution 𝑄 : S𝐴 → S𝐵 , denoted as 𝜆𝑠. fix 𝛼 . 𝑇 (𝑠, 𝐹 (𝛼)).4
Feedback cycles can be represented as Fig. 5a.
   DBSP uses feedback cycles mainly for two purposes: express iterative computation and construct
integration operator I, as we will show in the following.
Definition 3.6 (Integration and Differentiation). The integrationÍoperator I : S𝐴 → S𝐴 is
I (𝑠) = fix 𝛼 . (𝑠 + 𝑧 −1 (𝛼)), computing the running sum: I (𝑠) [𝑡] = 𝑖 ≤𝑡 𝑠 [𝑖], as shown in Fig. 5b.
The differentiation operator D : S𝐴 → S𝐴 is D (𝑠) = 𝑠 − 𝑧 −1 (𝑠), as shown in Fig. 5c.
   I and D are inverses (I ◦ D = D ◦ I = id). Given a stream operator 𝑄 : S𝐴 → S𝐵 , its
incremental version is defined as 𝑄 Δ = D ◦ 𝑄 ◦ I. The operator 𝑄 Δ consumes a stream of changes
and produces a stream of changes: if 𝑄 (𝑠 1 ) = 𝑠 2 , then 𝑄 Δ (D (𝑠 1 )) = D (𝑠 2 ). The DBSP theory
4 Our formal language guarantees that all feedback cycles are well-defined.
8                                                                                                                  Yang et al.


                                                 𝑠        +           I (𝑠)                𝑠                 +      D (𝑠)
         𝑠       𝑇          𝛼
                 𝐹                                       𝑧 −1                                      𝑧 −1      −

        (a) Feedback cycle                           (b) Integration I                         (c) Differentiation D

                       Fig. 5. Some core DBSP operators represented as circuit diagrams.

establishes compositional properties for 𝑄 Δ , such as the chain rule (𝑄 1 ◦ 𝑄 2 ) Δ = 𝑄 1Δ ◦ 𝑄 2Δ . This
leads to a syntax-guided incrementalization algorithm, which we will formalize as incOpt in §3.2.
   To incrementalize iterative computations (like recursive Datalog queries), we need to introduce a
new “inner” time dimension for iterative fixpoint computation besides the “outer” time dimension
for incremental computation, as §2.1 shows. DBSP implements this via two specific operators and
nested streams.
Definition 3.7 (Stream Introduction). The stream introduction operator 𝛿 0 : 𝐴 → S𝐴 produces a
stream from a scalar value 𝑣: 𝛿 0 (𝑣) [0] = 𝑣 and 𝛿 0 (𝑣) [𝑡] = 0 for 𝑡 > 0.
Definition 3.8 (Stream Elimination). The stream elimination operator ∫ : S𝐴 → 𝐴 aggregates
a stream that is zero almost everywhere (i.e., ∃𝑡 0 ∈ N. ∀𝑡 ≥ 𝑡 0 . 𝑠 [𝑡] = 0𝐴 ) into a scalar value:
        Í
∫ (𝑠) = 𝑡 ≥0 𝑠 [𝑡].
   As we mentioned in §2.2, 𝛿 0 takes a scalar input and outputs a stream and initiates a new
unbounded iterative computation. ∫ integrates the intermediate results of the inner computation
back into a single scalar output. If the input stream of ∫ is not zero almost everywhere, the
summation diverges. This potential for divergence leads to the FPD problem that we address in
this paper.
   A nested stream (or stream of streams) has type SS𝐴 = N → (N → 𝐴). It can be viewed as an
infinite 2D matrix where (𝑡 0, 𝑡 1 ) index the outer time and inner time, respectively, and each row is
an inner stream.
   We call an operator 𝑆 : SS𝐴 → SS𝐵 a nested operator. Just as we lift scalar functions to operators,
we can lift operators to nested operators. If 𝑆 : S𝐴 → S𝐵 , then ↑𝑆 : SS𝐴 → SS𝐵 applies 𝑆 to each
row of the nested stream: (↑𝑆) (𝑠) [𝑡 0 ] = 𝑆 (𝑠 [𝑡 0 ]). For a scalar function 𝑓 : 𝐴 → 𝐵, we lift it twice to
get ↑↑𝑓 : SS𝐴 → SS𝐵 , defined as (↑↑𝑓 ) (𝑠) [𝑚] [𝑛] = 𝑓 (𝑠 [𝑚] [𝑛]).
   For nested streams, delay 𝑧 −1 shifts values along the outer time dimension, delaying “rows” of
the matrix, while lifted delay ↑𝑧 −1 shifts values along the inner time dimension, delaying “columns”
of the matrix. The integration I operates along the outer time dimension, summing up rows of
the matrix, while the lifted integration ↑I operates along the inner time dimension, summing up
columns of the matrix.

3.2    A Formal Language for DBSP Well-Formed Circuits
We now formalize a language of DBSP well-formed circuits (which we simply abbreviate as circuits
from now on) that serves as the core calculus for our theory. This circuit language is an inductive
grammar as shown in Table 1.
   A circuit 𝑐 : 𝐴 → 𝐵 transforms an input stream of type 𝐴 to an output stream of type 𝐵. Types
are built from base types (Abelian groups) and binary products 𝐴 × 𝐵. Each circuit is annotated with
a stream level ℓ ∈ {1, 2},5 representing whether the circuit’s input and output are streams (level 1)
or nested streams (level 2). For instance, a bracket node must wrap a level-2 circuit and output a
level-1 circuit.

5 This restriction to the stream level is mainly for formalization convenience without loss of expressiveness. See §8 for more

discussion on this point.
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation                                   9


   The primitive node construct (node) lifts a user-defined scalar function to a stream operator,
providing a generic extension point for core computations. Commonly used generic operations
(like identity, tuple projections, and group arithmetic) are separated into a class of standard nodes.
Table 1. Circuit syntax and denotational semantics. Constructs are polymorphic over stream level ℓ unless
indicated.

 Construct 𝑐    Type          Level        ⟦𝑐⟧                                plift(𝑐 )                     incOpt(𝑐 )
 Primitive nodes
 node( 𝑓 )       𝐴→𝐵          ℓ            ↑ℓ 𝑓                               node( 𝑓 )                     incOpt(node( 𝑓 ) )
 Standard nodes
 const(𝑥 )      𝐴→𝐵           ℓ            ↑ℓ (𝜆_. 𝑥 )                        const(𝑥 )                     const(𝑥 ) ▷ D
 id             𝐴→𝐴           ℓ            id                                 id                            id
 fst            𝐴×𝐵 →𝐴        ℓ            ↑ℓ 𝜋 1                             fst                           fst
 snd            𝐴×𝐵→𝐵         ℓ            ↑ℓ 𝜋 2                             snd                           snd
 add            𝐴×𝐴→𝐴         ℓ            ↑ℓ (+)                             add                           add
 sub            𝐴×𝐴→𝐴         ℓ            ↑ℓ (−)                             sub                           sub
 Temporal nodes
 delay          𝐴→𝐴           ℓ            𝑧 −1                               ↑delay                        delay
 ↑delay         𝐴→𝐴           2            ↑𝑧 −1                              −                             ↑delay
 Structural combinators
 𝑐1 ▷ 𝑐2        𝐴 →𝐶          ℓ            ⟦𝑐 2 ⟧ ◦ ⟦𝑐 1 ⟧                    plift(𝑐 1 ) ▷ plift(𝑐 2 )     incOpt(𝑐 1 ) ▷ incOpt(𝑐 2 )
 𝑐1 | | 𝑐2      𝐴 → 𝐵 ×𝐶      ℓ            𝜆𝑥 . (⟦𝑐 1 ⟧(𝑥 ), ⟦𝑐 2 ⟧(𝑥 ) )     plift(𝑐 1 ) | | plift(𝑐 2 )   incOpt(𝑐 1 ) | | incOpt(𝑐 2 )
 Feedback loops
 loop(𝑐 )       𝐴→𝐵           ℓ            𝜆𝑥 . fix 𝛼 . ⟦𝑐⟧(𝑥, 𝑧 −1 (𝛼 ) )    ↑loop(plift(𝑐 ) )             loop(incOpt(𝑐 ) )
 ↑loop(𝑐 )      𝐴→𝐵           2            𝜆𝑥 . fix 𝛼 . ⟦𝑐⟧(𝑥, ↑𝑧 −1 (𝛼 ) )   −                             ↑loop(incOpt(𝑐 ) )
 Level adapters
 lifting(𝑐 )    𝐴→𝐵           2 (𝑐 at 1)   ↑⟦𝑐⟧                               −                             Δ(lifting(𝑐 ) )
 bracket(𝑐 )    𝐴→𝐵           1 (𝑐 at 2)   ↑ ∫ ◦⟦𝑐⟧ ◦ ↑𝛿 0                    lifting(bracket(𝑐 ) )         bracket(incOpt(𝑐 ) )

   Several important circuits can be defined compositionally:
Definition 3.9 (Derived Circuit Constructs). The integration circuit I = loop(add) computes I,
and the differentiation circuit D = (id || delay) ▷ sub computes D. The unoptimized incremental
form of a circuit 𝑐 is given by Δ(𝑐) = I ▷ 𝑐 ▷ D.
   The denotational semantics ⟦𝑐⟧ of a circuit 𝑐 : 𝐴 → 𝐵 at stream level ℓ is a stream operator. For
level 1, it is an operator S𝐴 → S𝐵 . For level 2, it is SS𝐴 → SS𝐵 . Here ↑1 𝑓 = ↑𝑓 denotes single
lifting, and ↑2 𝑓 = ↑↑𝑓 denotes double lifting.
   Due to the bracket construct, which relies on the stream elimination operator ∫ , the denotational
semantics ⟦·⟧ is a partial function. Whether it converges on a given input is the convergence
detection problem we mentioned in §2.2.
   We can now formalize the incremental optimization algorithm of DBSP as the following two
syntactic functions:
Definition 3.10. plift lifts a level-1 circuit and pushes the lifting operator onto individual nodes.
Its definition is in Table 1.
Definition 3.11. incOpt transforms a circuit into its optimized incremental version following the
DBSP’s syntax-guided algorithm. Its definition is in Table 1.
   Note that for primitive nodes, incOpt(node(𝑓 )) is a customizable incremental form, which makes
this algorithm quite extensible. The theory has provided an incremental form for a wide class of
10                                                                                                                           Yang et al.


functions. For example, for a linear function 𝑓 , the incremental form can be node(𝑓 ) itself. Even in
the worst case, the incremental form can fall back to the unoptimized form Δ(node(𝑓 )).
  Another thing to notice is that incOpt(lifting(𝑐)) is the unoptimized form, as the incremental
operator Δ cannot go across lifting into the inner circuit. That’s why we need the function plift to
push the lifting operator into the inner circuit.

3.3    Example: Implementing and Incrementalizing the Datalog Query in DBSP
In this section, we present how DBSP expresses and incrementalizes the Datalog query example
from §1 and §2.1 in three steps (corresponding to the three strategies in §2.1).
   DBSP uses Z-sets [19] (or simply Zsets) as the underlying Abelian group to represent sets and
relations. It can be simply understood as sets where each element has an integer count, which can
be negative to represent deletion. In this paper, we will simply treat Zsets as their underlying sets
for most cases.
                                                                                                                 Δ
 𝑖    𝛿0     I     ↑𝐹          D    ∫      𝑜   𝑖    𝛿0     (↑𝐹 ) Δ          ∫   𝑜   𝑖®      ↑𝛿 0   (↑(↑𝐹 ) Δ )               ↑∫     𝑜®

                        𝑧 −1                                         𝑧 −1                                            ↑𝑧 −1

         (a) The naive strategy.               (b) The semi-naive strategy.              (c) The delta-of-deltas strategy.

Fig. 6. The three circuits that arise when DBSP implements and incrementalizes a Datalog recursive query.

    Recall that the recursive query is defined via a non-recursive query 𝐹𝐸 (𝑅), or 𝐹 (𝐸, 𝑅) (which we
will simply write as 𝐹 ). DBSP will first compile it into some circuit and lift it to get a level-1 circuit
𝑐 0 whose denotation is ↑𝐹 . The recursive query 𝑄 asks for the fixpoint of iterative application of
𝐹 on an input 𝑖. 𝑄 can be expressed as a circuit shown in Fig. 6a. The query body (the bracketed
sub-circuit) can be expressed in our formal language as6
                                            datalogBody(𝑐 0 ) = loop(Δ(𝑐 0 ))                                                       (1)
We use the stream introduction operator 𝛿 0 (Def. 3.7) and the integration operator I (Def. 3.6)
to convert the input 𝑖 into a constant stream of 𝑖 and then feed it into ↑𝐹 . The feedback loop
implements the iterative fixpoint computation we need. Its output stream 𝛼 looks like following:
                           𝛼 [0] = 𝐹 (𝑖, 0), 𝛼 [1] = 𝐹 (𝑖, 𝛼 [0]), 𝛼 [2] = 𝐹 (𝑖, 𝛼 [1]), . . .
If 𝛼 is fixed after some point, then the differentiation operator D (Def. 3.6) converts it into a stream
that is zero almost everywhere, which can then be aggregated by the stream elimination operator
∫ (Def. 3.8) to produce the final output 𝑜. This corresponds to the naive strategy in §2.1.
   Note that we can optimize ↑𝐹 between I and D into (↑𝐹 ) Δ by applying the DBSP’s incremental
optimization algorithm, naturally leading to the circuit implementing the semi-naive strategy
shown in Fig. 6b. Its query body can be expressed as
                                        semiNaiveBody(𝑐 0 ) = loop(incOpt(𝑐 0 ))                                                    (2)
   We can further lift the whole circuit, push the lifting operator and apply the incremental opti-
mization to transform it into the circuit shown in Fig. 6c, which implements the delta-of-deltas
strategy. Its query body can be expressed as
                                                                            
                    deltaOfDeltasBody(𝑐 0 ) = ↑loop incOpt plift incOpt(𝑐 0 )                   (3)

6 Technically, we cannot express the whole level-0 circuit itself in our formal language because of our syntactic restriction

(see §8), but it suffices to express the query body as it encodes sufficient information.
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation                         11


and the whole circuit can be expressed as
                        deltaOfDeltasQuery(𝑐 0 ) = bracket(deltaOfDeltasBody(𝑐 0 ))                                        (4)

4   The Fixpoint-Detection Problem and the Convergence-Detection Problem
As introduced in §3.1, the stream-elimination operator ∫ is inherently a partial function: it is
well-defined only if its input stream is zero almost everywhere. With standard Zset-based relational
operators, DBSP is Turing-complete [6], meaning it is acceptable that some circuits containing ∫
never converge to zero. However, the core challenge is at run time: even if ∫ ’s input does eventually
converge to zero, how can the system safely detect this convergence by observing only a finite
prefix of the stream? Determining this zero-almost-everywhere property at run time is the essence
of the Fixpoint Detection (FPD) problem. In this section, we formalize the FPD problem and the
soundness and completeness of fixpoint detectors.
   Furthermore, in our language (§3.2), ∫ operators are packaged inside bracketed circuits, and a
complete circuit can contain multiple bracketed sub-circuits, much like a standard program can
contain multiple while loops. Therefore, a circuit mathematically converges if and only if every
bracketed sub-circuit reaches a fixpoint. We refer to this global detection problem as the Convergence
Detection problem.
   To formalize the FPD problem within our formal language, we introduce the following definition
to characterize when a stream has converged to zero at a specific index:
Definition 4.1 (ZeroAfter). A stream 𝑠 ∈ S𝐴 is zero after an outer index 𝑛 ∈ N if:
                                      ZeroAfter1 (𝑠, 𝑛) := ∀𝑚 ≥ 𝑛, 𝑠 [𝑚] = 0𝐴
A nested stream 𝑠 ∈ SS𝐴 is zero after a 2D-index (𝑚, 𝑛) ∈ N × N if:
                                    ZeroAfter2 (𝑠, 𝑚, 𝑛) := ZeroAfter1 (𝑠 [𝑚], 𝑛)
We also say that a nested stream 𝑠 ∈ SS𝐴 is zero after an upper-bound stream b ∈ SN if:
                                ZeroAfter2 (𝑠, b) := ∀𝑖 ∈ N, ZeroAfter2 (𝑠, 𝑖, b[𝑖])
   An important fact is that ZeroAfter is a level-indexed predicate with the following properties:
     • ZeroAfter1 applies to any stream (i.e., stream of level ℓ ≥ 1), and accepts a 1D-index.
     • ZeroAfter2 is defined in terms of ZeroAfter1 . It applies only to nested streams (i.e., streams
        of level ℓ ≥ 2), and accepts a 2D-index or a stream of 1D-indices.
This inductive7 structure is a natural result of the stream-level hierarchy of a well-defined circuit.
We will soon see more examples of such level-indexed definitions.
   We also need to introduce another predicate to capture the first true value of a stream of Booleans.
Definition 4.2 (FirstTrue). A stream of Booleans 𝑠 ∈ SB encounters its first true value at index
𝑛 ∈ N, denoted FirstTrue1 (𝑠) = 𝑛, if 𝑠 [𝑛] = true and ∀𝑚 < 𝑛, 𝑠 [𝑚] = false. Similarly, we define
FirstTrue2 (𝑠) = b for 𝑠 ∈ SSB and b ∈ SN as ∀𝑖 ∈ N, FirstTrue1 (𝑠 [𝑖]) = b[𝑖].
   We can now formally state the FPD problem. Intuitively, the FPD problem is a matter of providing
a fixpoint detector that specifies a runtime fixpoint-detection mechanism for a level-1 bracketed
circuit 𝑐 (as shown in Fig. 7a) or a level-2 bracketed circuit 𝑐 (as shown in Fig. 7b). A fixpoint
detector accepts a circuit 𝑐 and an input to this circuit (which is either 𝛿 0 (𝑥) or ↑𝛿 0 (𝑥)), and returns
a Boolean value for each entry of the input. When a fixpoint detector returns true for the first time
in an iteration, the output of 𝑐 should have converged to 0 in the corresponding iteration (recall
that 𝑐 should produce changes to the output that are integrated by ∫ until convergence). We call
7 One might consider Def. 4.1 to not be inductive because it only refers to levels 1 and 2. However, this choice was deliberate

because of the syntactic restriction we placed on stream level (see §3.2 and §8). If the stream level is generalized to any
natural number, Def. 4.1 would be a standard inductive definition.
12                                                                                                      Yang et al.


          𝑥      𝛿0        𝑐        ∫                                    𝑥      ↑𝛿 0       𝑐    ↑∫

     (a) The FPD problem for a level-1 circuit 𝑐                    (b) The FPD problem for a level-2 circuit 𝑐

                               Fig. 7. The FPD problem for level-1 and level-2 circuits.

this property soundness (see Eqns. (5) and (7) below). When the output has converged to 0, the
fixpoint detector should eventually return true. We call this property completeness (see Eqns. (6)
and (8) below).
Definition 4.3 (The FPD problem). Given a level-1 circuit 𝑐, a function 𝑓𝑐 : S𝐴 → SB is a fixpoint
detector for 𝑐 if for any 𝑥 ∈ 𝐴 and 𝑛 ∈ N:
                       FirstTrue1 (𝑓𝑐 (𝛿 0 (𝑥))) = 𝑛 =⇒ ZeroAfter1 (⟦𝑐⟧(𝛿 0 (𝑥)), 𝑛) and                          (5)

                       ZeroAfter1 (⟦𝑐⟧(𝛿 0 (𝑥)), 𝑛) =⇒ ∃𝑚, FirstTrue1 (𝑓𝑐 (𝛿 0 (𝑥))) = 𝑚                          (6)
Similarly, given a level-2 circuit 𝑐, a function 𝑓𝑐 : SS𝐴 → SSB is a fixpoint detector for 𝑐 if for any
𝑥 ∈ S𝐴 and b ∈ SN :
                      FirstTrue2 (𝑓𝑐 (↑𝛿 0 (𝑥))) = b =⇒ ZeroAfter2 (⟦𝑐⟧(↑𝛿 0 (𝑥)), b) and                         (7)

                      ZeroAfter2 (⟦𝑐⟧(↑𝛿 0 (𝑥)), b) =⇒ ∃b′, FirstTrue2 (𝑓𝑐 (↑𝛿 0 (𝑥))) = b′                       (8)
   By changing FirstZero to another fixpoint specification or criterion (like our IntFP to be introduced
in §5), Def. 4.3 can be adapted to formalize other FPD problems. Note that the FPD for a level-1
circuit 𝑐 on some input 𝑥 can be simply reduced to the FPD for the level-2 circuit ↑𝑐 on stream
input 𝜆_. 𝑥. Consequently, level-2 FPD is a harder problem than level-1 FPD.
   For the theory’s global convergence specification, we define it as follows:
Definition 4.4 (External convergence (ExtConv)). For any circuit 𝑐 and input 𝑥, we say 𝑐 externally
converges, denoted ExtConv(𝑐, 𝑥), if ⟦𝑐⟧(𝑥) mathematically converges. Or equivalently, for any sub-
circuit in the form of bracket(𝑐 0 ) and its corresponding input 𝑥 0 , ∃b, ZeroAfter2 (⟦𝑐 0 ⟧(↑𝛿 0 (𝑥 0 )), b).
   It is easy to see why the external-convergence problem is just the global version of the FPD
problem. Once we have a fixpoint detector for any circuit 𝑐, we immediately get a convergence
detector for ExtConv by applying the fixpoint detector to every bracketed sub-circuit. Therefore,
we will only focus on the FPD problem in what follows.

4.1     Example: The FirstZero Strategy and Its Limitation
We have already introduced the FirstZero strategy in Section 2.1, which is merely to stop when the
first 0 value is encountered. We can formalize FirstZero by instantiating the 𝑓𝑐 fixpoint-detector
function from Def. 4.3. For a level-1 circuit 𝑐, it maps an input stream 𝑥 to a Boolean stream:
𝑓𝑐 (𝑥) = 𝜆𝑛. (⟦𝑐⟧(𝑥) [𝑛] = 0). For a level-2 circuit 𝑐, it maps an input nested stream 𝑥 to a nested
Boolean stream: 𝑓𝑐 (𝑥) = 𝜆𝑖. 𝜆𝑛. (⟦𝑐⟧(𝑥) [𝑖] [𝑛] = 0).
    Following the intuitive idea in §2.1, we have established the following theorems for the soundness
and completeness of FirstZero for the naive and semi-naive strategy, and the unsoundness of
FirstZero for the delta-of-deltas strategy.
Theorem 4.5. The FirstZero strategy is a sound and complete fixpoint detector for the naive query
body datalogBody(𝑐 0 ) (Eqn. (1)) and the semi-naive query body semiNaiveBody(𝑐 0 ) (Eqn. (2)),
where 𝑐 0 can represent any circuit implementing a lifted scalar query.
Theorem 4.6. The FirstZero strategy is not a sound fixpoint detector for the delta-of-deltas
query body deltaOfDeltasBody(𝑐 0 ) (Equation 3), where 𝑐 0 is the circuit implementing the lifted
non-recursive query 𝐹𝐸 (𝑅) from §1.
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation                          13


4.2    Impossibility of Exact Fixpoint Detection
Can another strategy overcome FirstZero’s failure and solve FPD exactly for every circuit? The
following theorem shows the answer is no. We assume the choice of primitive nodes makes
DBSP Turing-complete: DBSP circuits can express arbitrary partial-recursive scalar functions. This
assumption is mild in practice: standard Zset primitive nodes together with DBSP’s recursive
constructs suffice [6, §7.2]. Without loss of generality, we also assume the base type is Z.
Theorem 4.7. If the choice of primitive nodes makes DBSP Turing-complete, there exists a fixed
level-1 circuit 𝑐 with no computable sound and complete fixpoint detector.

   Proof. We show that a computable sound and complete detector would recognize8 the com-
plement of the halting problem, which is not recursively enumerable. We construct a fixed circuit
whose output is eventually zero exactly for inputs that encode nonhalting programs. Let ℎ(𝑒, 𝑘) be
1 if the program that 𝑒 encodes halts on input 0 within 𝑘 steps of a fixed universal evaluator, and 0
otherwise. Since ℎ is total and primitive recursive [7, §5.2], Turing-completeness
                                                                                    ensures there is a
level-1 circuit 𝐸 with ⟦𝐸⟧ = ↑ℎ. Define 𝑐 := I || (const(1) ▷ I) ▷ 𝐸. On 𝛿 0 (𝑒), the two branches
supply 𝑒 and 𝑛 + 1, giving ⟦𝑐⟧(𝛿 0 (𝑒)) [𝑛] = ℎ(𝑒, 𝑛 + 1). Assume there is a computable sound and
complete detector for 𝑐 and run the detector on 𝛿 0 (𝑒) until its first true output. By completeness,
this procedure terminates if 𝑒 does not halt; by soundness, it runs forever if 𝑒 halts. This would
recognize the complement of the halting problem, a contradiction.                                    □

   The theorem only rules out exact fixpoint detection for arbitrary circuits, but it does not rule
out sound and complete detectors for certain circuit subclasses of interest.9 It motivates the sound
sufficient criterion IntConv developed in the next section. In §7, we prove that IntConv is also
complete for regular circuits, including Datalog and while queries, and then extend this guarantee
to their incrementally optimized forms.

5     A Sound Convergence Criterion: IntConv
In this section, we introduce internal convergence (IntConv) as a sound sufficient condition for
ExtConv. (In §6, we give an implementable detector for the IntConv criterion.) Following the “local-
global” structure of the problem, we will first define internal fixpoint (IntFP) as a sound sufficient
condition for an external fixpoint, and then apply it to all bracketed sub-circuits to formulate the
IntConv criterion. At the end of this section, we give a qualitative data-dependency example in
which relying on ExtConv without IntConv requires recursive trace-backs or additional retained
state. The example provides a theoretical argument for an implementation benefit of IntConv.
   Before introducing IntFP, we first introduce a natural generalization of ZeroAfter called FixAfter,
which indicates that a stream becomes fixed to a constant value rather than to 0𝐴 .
Definition 5.1 (FixAfter). Like ZeroAfter, FixAfter is a level-indexed predicate defined identically
in its level-1, level-2, and vectorized forms, except that its base case FixAfter1 (𝑠, 𝑛) requires ∀𝑚 ≥
𝑛, 𝑠 [𝑚] = 𝑠 [𝑛]. Note that if 𝑠 is a nested stream SS𝐴 , this means repeating the exact same inner
stream 𝑠 [𝑛] from the outer index 𝑛 onwards.
   Then, we reframe the FPD problem using a new level-indexed predicate called external fixpoint
(ExtFP). Intuitively, ExtFP characterizes that a circuit reaches an external fixpoint at a given index,
without looking into the internal circuit structure. Formally,

8 In computability theory, an algorithm recognizes a set if the algorithm eventually accepts every input in the set and never

accepts inputs outside it; on those other inputs, it may run forever.
9 For example, this construction does not establish an impossibility result for incrementalizations of total computable queries,

because the query ∫ (⟦𝑐⟧(𝛿 0 (𝑒 ) ) ) is defined exactly for nonhalting programs.
14                                                                                               Yang et al.


Definition 5.2 (External fixpoint (ExtFP)). Given any circuit 𝑐 (either level-1 or level-2), an input
stream 𝑥, and an index 𝑛 ∈ N, we say that 𝑐 reaches an external fixpoint across the first time
dimension at 𝑛, denoted by ExtFP1 (𝑐, 𝑥, 𝑛), if both the input and the denoted output of 𝑐 are fixed
after the outer index 𝑛:
                       ExtFP1 (𝑐, 𝑥, 𝑛) := FixAfter1 (𝑥, 𝑛) ∧ FixAfter1 (⟦𝑐⟧(𝑥), 𝑛)
  For a level-2 circuit 𝑐, a nested input stream 𝑥 ∈ SS𝐴 , an outer index 𝑚 ∈ N, and an inner index
𝑛 ∈ N, the external fixpoint across the second time dimension is defined as:
                 ExtFP2 (𝑐, 𝑥, 𝑚, 𝑛) := FixAfter2 (𝑥, 𝑚, 𝑛) ∧ FixAfter2 (⟦𝑐⟧(𝑥), 𝑚, 𝑛)
ExtFP2 (𝑐, 𝑥, b) for b ∈ SN is naturally defined as ∀𝑖 ∈ N, ExtFP2 (𝑐, 𝑥, 𝑖, b[𝑖]).
   With this definition, the FPD problem for a level-1 circuit 𝑐 on input 𝑥 essentially asks to detect
an index 𝑛 where ExtFP1 (𝑐, 𝛿 0 (𝑥), 𝑛) holds and the fixed output is 0. Similarly, the FPD problem
for a level-2 circuit 𝑐 on nested input 𝑥 asks to detect a bound stream b where ExtFP2 (𝑐, ↑𝛿 0 (𝑥), b)
holds and the fixed outputs are 0.
   As we proved in §4.2, exact FPD is impossible for sufficiently expressive circuits, and hence
so is detecting ExtFP in full generality. The Feldera implementation of DBSP [14] uses internal-
state stability to detect fixpoints. Each runtime operator provides a scope-indexed fixed-point
check intended to report whether its output will remain stable if its input does, and the circuit
combines the checks of its operators. Thus, the operational idea of detecting internal-state stability
is established implementation practice rather than a novel contribution of this paper. The cited
implementation specifies and tests this runtime contract, but does not provide a formal proof that
the circuit-wide check implies denotational convergence. To bridge the gap between this runtime
strategy and the denotational DBSP theory, we give the strategy a rigorous, declarative account
through a criterion called internal fixpoint (IntFP). This formal criterion allows us to prove precisely
this soundness connection, and later establish completeness for a large class of circuits. We discuss
the relationship with the Feldera implementation further in §9.
Definition 5.3 (Internal fixpoint (IntFP)). Intuitively, IntFP means that all internal nodes (i.e.,
individual components) of a circuit have reached an ExtFP at a specific index. Formally, for any
circuit 𝑐, an input stream 𝑥, and an index 𝑛 ∈ N, IntFP1 (𝑐, 𝑥, 𝑛) is defined by structural induction
on 𝑐 over the categories in Table 1:
      • Primitive, Standard and Temporal Nodes: Inherit the ExtFP1 condition. That is, for any
        such node 𝑐, IntFP1 (𝑐, 𝑥, 𝑛) := ExtFP1 (𝑐, 𝑥, 𝑛).
      • Structural Combinators: Require IntFP1 for all sub-circuits. That is
                   IntFP1 (𝑐 1 ▷ 𝑐 2, 𝑥, 𝑛) := IntFP1 (𝑐 1, 𝑥, 𝑛) ∧ IntFP1 (𝑐 2, ⟦𝑐 1 ⟧(𝑥), 𝑛)
       and
                       IntFP1 (𝑐 1 || 𝑐 2, 𝑥, 𝑛) := IntFP1 (𝑐 1, 𝑥, 𝑛) ∧ IntFP1 (𝑐 2, 𝑥, 𝑛)
       .
     • Feedback Loops: Require IntFP1 for the loop body on the input tuple containing the
       delayed output. That is
                    IntFP1 (loop(𝑐), 𝑥, 𝑛) := IntFP1 (𝑐, (𝑥, 𝑧 −1 (⟦loop(𝑐)⟧(𝑥))), 𝑛)
       and similarly
                  IntFP1 (↑loop(𝑐), 𝑥, 𝑛) := IntFP1 (𝑐, (𝑥, ↑𝑧 −1 (⟦↑loop(𝑐)⟧(𝑥))), 𝑛)
     • Level Adapters: For bracket(𝑐), IntFP1 delegates to the level-2 internal circuit 𝑐:
                            IntFP1 (bracket(𝑐), 𝑥, 𝑛) := IntFP1 (𝑐, ↑𝛿 0 (𝑥), 𝑛)
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation   15


        For the level-1 circuit lifting(𝑐), because it models an inner circuit that lacks states across
        outer iterations, the internal fixpoint naturally degenerates into the external fixpoint:
                             IntFP1 (lifting(𝑐), 𝑥, 𝑛) := ExtFP1 (lifting(𝑐), 𝑥, 𝑛)
The predicate IntFP2 (𝑐, 𝑥, 𝑚, 𝑛) for the second time dimension is defined for level-2 circuits only. It
is mostly defined by uniformly replacing ExtFP1 with ExtFP2 and IntFP1 with IntFP2 , with a notable
exception. For the nested lifting circuit lifting(𝑐), IntFP relies on the first dimension predicate
IntFP1 of the underlying level-1 circuit:
                              IntFP2 (lifting(𝑐), 𝑥, 𝑚, 𝑛) := IntFP1 (𝑐, 𝑥 [𝑚], 𝑛)
The vectorized version is naturally defined as IntFP2 (𝑐, 𝑥, b) := ∀𝑖 ∈ N, IntFP2 (𝑐, 𝑥, 𝑖, b[𝑖]).
  The definition of IntFP is both structural and level-indexed. For a bracketed circuit, it applies
IntFP to the enclosed circuit, adapting the input to its stream level. Because the same rules apply
recursively to sub-circuits, the definition also handles nested brackets.
  One of the most important properties of IntFP is that it is a sound sufficient condition for ExtFP.
That is, if a circuit reaches an internal fixpoint, it must have also reached an external fixpoint.
Theorem 5.4 (Soundness of IntFP). For any well-formed circuit 𝑐, input 𝑥, and index 𝑛, we have:
                                     IntFP1 (𝑐, 𝑥, 𝑛) =⇒ ExtFP1 (𝑐, 𝑥, 𝑛)
Similarly, for any level-2 circuit 𝑐, nested input 𝑥, and indices 𝑚, 𝑛:
                                  IntFP2 (𝑐, 𝑥, 𝑚, 𝑛) =⇒ ExtFP2 (𝑐, 𝑥, 𝑚, 𝑛)
   Proof. We first prove the property for the level index 1, and then prove the property for the level
2 based on that for level 1. This can also be seen as induction on the level index of the predicate. □
   Finally, by applying the local IntFP criterion to all bracketed sub-circuits, and adding that the
fixed output is 0, we define our global convergence criterion called internal convergence (IntConv).
Definition 5.5 (Internal convergence (IntConv)). We say that a circuit 𝑐 internally converges on
input 𝑥, denoted IntConv(𝑐, 𝑥), if for any sub-circuit in the form of bracket(𝑐 0 ) and its input 𝑥 0 ,
                       ∃b, IntFP2 (𝑐 0, ↑𝛿 0 (𝑥 0 ), b) ∧ ∀𝑖, ⟦𝑐 0 ⟧(↑𝛿 0 (𝑥 0 )) [𝑖] [b[𝑖]] = 0
  By Theorem 5.4, the definition of IntConv will be equivalent with ∀𝑖, ⟦𝑐 0 ⟧(↑𝛿 0 (𝑥 0 )) [𝑖] [b[𝑖]] =
0 replaced by ZeroAfter2 (⟦𝑐 0 ⟧(↑𝛿 0 (𝑥 0 )), b). This immediately implies that IntConv is a sound
sufficient condition for ExtConv.
Theorem 5.6 (Soundness of IntConv). For any well-formed circuit 𝑐 and input 𝑥, we have
                                     IntConv(𝑐, 𝑥) =⇒ ExtConv(𝑐, 𝑥)
   These soundness implications are one-way in general: ExtFP need not imply IntFP, and ExtConv
need not imply IntConv. In §7, we identify circuit classes for which the corresponding converse
does hold.
   Why use IntConv rather than a weaker sound criterion for the theoretical specification ExtConv?
The following example isolates one implementation benefit. For this circuit, an evaluator that relies
only on ExtConv lacks a guarantee that earlier internal values have stabilized. It must therefore
either recompute a recursive dependency chain or retain the historical values needed to answer
later demands. IntConv supplies the missing stability guarantee.
   Consider such a circuit satisfying ExtConv but not IntConv, with an integration operator I
inside a bracketed sub-circuit, as shown in Fig. 8. Its input 𝑋 and output 𝑌 are both nested streams.
Assume ExtConv is detected soundly. Suppose that evaluation is currently at (4, 3) (we use 1-based
indexing)—namely, the third inner iteration of the fourth outer iteration—and that the first three
16                                                                                              Yang et al.



                                                           previous
                                                            nodes




(a) An I operator inside a bracketed sub-circuit. The   (b) Data dependency in this example. An arrow from
red ? is the value we want to evaluate.                 𝑎 to 𝑏 denotes that computing 𝑎 requires 𝑏.

     Fig. 8. A data-dependency cost that can arise when evaluation relies on ExtConv without IntConv.

outer iterations reached external convergence after two inner iterations, while the fourth did not.
Now 𝑋 [4] [3] = 12 is ready.
   Fig. 8b shows the data dependency in this example. To evaluate 𝑌 [4] [3] correctly, we need
𝑌 [4] [3] = 𝑌 [3] [3] + 𝑋 [4] [3]. But because the circuit satisfies ExtConv without satisfying IntConv,
external convergence does not guarantee internal convergence. Consequently, we cannot directly
conclude what 𝑌 [3] [3] is. Computing 𝑌 [3] [3] may require 𝑌 [2] [3] and 𝑋 [3] [3], both unknown;
computing 𝑋 [3] [3] can recursively force upstream re-evaluation, potentially all the way back to
↑𝛿 0 , which initiated the iterative computation.
   Thus, under a strategy that does not retain all of this history, a later outer iteration that needs
more inner iterations than earlier ones can trigger recursive recomputation. Retaining the history
instead trades that recomputation for additional state, potentially across an unbounded number of
outer iterations.
   For this example, IntConv avoids that tradeoff. Because IntConv guarantees that all internal
nodes reach an internal fixpoint, values like 𝑌 [3] [3] are mathematically guaranteed to be stabilized
values (e.g., 𝑌 [3] [3] = 𝑌 [3] [2] in this example), which should already be stored in the state. No
recursive trace-back is needed, and state management stays simple: in this example, I only needs
to store its output list (all output until convergence) from the last outer iteration. This analysis is
qualitative: it neither establishes a general lower bound for every criterion weaker than IntConv
nor measures the overhead of a concrete implementation.


6    The StFP Detector and the Global IntConv Detector
According to Def. 5.5, the global IntConv detector checks every bracketed sub-circuit with a local
IntFP detector and also checks that its fixed output is 0. We construct the local detector in two
steps: the StFP detector checks local state stability, and a fixed-input check turns its result into
IntFP detection. Thus, the global IntConv detector combines the StFP detector with fixed-input and
zero-output checks across all bracketed sub-circuits.
   To detect the IntFP, the Feldera implementation for the DBSP runtime uses a scope-indexed
internal-state-stability strategy that we call “FirstStateStable”, as opposed to FirstZero. The idea in
our core calculus is as follows: most nodes are stateless, and only 𝑧 −1 and ↑𝑧 −1 are stateful. For
stateless nodes, their output is solely determined by their input. For stateful 𝑧 −1 and ↑𝑧 −1 , their
output in an execution step is solely determined by their state and unrelated to the input of the
current step, which means we can predict all stateful nodes’ outputs at the end of the previous step.
Therefore, at the end of a step, if we can tell that the outputs of all stateful nodes of a circuit are
the same as the previous step, and that the input to the whole circuit is fixed after this step (which
is easily decidable for input like 𝛿 0 (𝑥)), then we can conclude that the circuit has reached an IntFP.
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation   17


   To formalize this idea, a challenge is that for simplicity, our theory only specifies the denotational
semantics of DBSP circuits as pure mathematical functions, and has no formal concepts of “states”.
After all, although we have some model in mind of how states are implemented, ultimately it is a
representation choice in the implementation. Luckily, there is an important assumption that holds
for any reasonable implementation of states: a circuit’s state at a given point is determined by its
input up to that point. Therefore, we can always formalize properties of a circuit’s state in terms of
its input up to that point.
   Following this idea, we first make precise how to continue an observed input by holding it fixed.
For a stream 𝑥 and an index 𝑛, let
                                                          (
                                                           𝑥 [𝑖] 𝑖 < 𝑛,
                                  letFixed1 (𝑥, 𝑛) [𝑖] :=
                                                           𝑥 [𝑛] 𝑖 ≥ 𝑛,
and, for a nested stream 𝑥 and indices 𝑚, 𝑛, let
                                                          (
                                                           𝑥 [𝑚] [𝑛]    𝑖 = 𝑚 ∧ 𝑗 ≥ 𝑛,
                          letFixed2 (𝑥, 𝑚, 𝑛) [𝑖] [ 𝑗] :=
                                                           𝑥 [𝑖] [ 𝑗]   otherwise.
Thus, letFixed2 leaves every row other than 𝑚 unchanged and replaces the suffix of row 𝑚 beginning
at 𝑛 with the value 𝑥 [𝑚] [𝑛].
   We can now define the notion of State Fixpoint (StFP) as a semantic counterpart of the circuit-state
property used by the FirstStateStable strategy.
Definition 6.1 (State Fixpoint (StFP)). For any circuit 𝑐, input 𝑥, and index 𝑛, define
                               StFP1 (𝑐, 𝑥, 𝑛) := IntFP1 (𝑐, letFixed1 (𝑥, 𝑛), 𝑛).
For any level-2 circuit 𝑐, nested input 𝑥, and indices 𝑚, 𝑛, define
                          StFP2 (𝑐, 𝑥, 𝑚, 𝑛) := IntFP2 (𝑐, letFixed2 (𝑥, 𝑚, 𝑛), 𝑚, 𝑛).
Finally, for a bound stream b ∈ SN , the vectorized predicate is defined pointwise:
                                StFP2 (𝑐, 𝑥, b) := ∀𝑖 ∈ N, StFP2 (𝑐, 𝑥, 𝑖, b[𝑖]).
   The fixed continuations agree with the observed input through the designated index and impose
a fixed future from that index onward. Therefore, StFP asks whether the circuit’s current state
would be at an internal fixpoint if its future input remained stable. The following theorem states its
precise connection to IntFP.
Theorem 6.2 (IntFP and StFP). For any circuit 𝑐,
                      ∀𝑥, 𝑛, IntFP1 (𝑐, 𝑥, 𝑛) ⇐⇒ (StFP1 (𝑐, 𝑥, 𝑛) ∧ FixAfter1 (𝑥, 𝑛))
and for any level-2 circuit 𝑐,
               ∀𝑥, 𝑚, 𝑛, IntFP2 (𝑐, 𝑥, 𝑚, 𝑛) ⇐⇒ (StFP2 (𝑐, 𝑥, 𝑚, 𝑛) ∧ FixAfter2 (𝑥, 𝑚, 𝑛))
The pointwise definitions immediately give the vectorized form
                     ∀𝑥, b, IntFP2 (𝑐, 𝑥, b) ⇐⇒ (StFP2 (𝑐, 𝑥, b) ∧ FixAfter2 (𝑥, b)).
   Because it is easy to detect whether ↑𝛿 0 (𝑥) (the input to the target bracketed circuit) is fixed
after any index (𝑚, 𝑛), it suffices to detect the StFP.
   We now give a high-level runtime algorithm to detect the StFP for any circuit 𝑐 and input 𝑥. While
StFP provides the semantic formalization of FirstStateStable in our denotational model, this detector
provides its algorithmic formalization. As before, we simulate computation of the state at some
point by computation of input up to that point. We will also explain what a natural implementation
would probably do for each case. See §9 for more discussion of the Feldera implementation.
18                                                                                                     Yang et al.


Definition 6.3 (StFP Detector). We define Detector1 , the level-1 StFP detector that accepts a circuit
𝑐, stream input 𝑥, and an index 𝑛, and returns a boolean, as follows:
     • Primitive and Standard Nodes: Return true because they are stateless.
                                           Detector1 (𝑐, 𝑥, 𝑛) := true
     • Temporal Nodes: For delay, it checks whether the new state (the current input) matches
       the stored state (the last input). Note that for level-2 delay, we technically need to compare
       two infinite streams. However, under IntConv, the stream of last input is always fixed after
       some point, so it can be stored in a finite state (see the example at the end of §5).
                                Detector1 (delay, 𝑥, 𝑛) := (𝑥 (𝑛) = 𝑧 −1 (𝑥) (𝑛))
        For ↑delay, because its states are only updated within the inner time dimension, it has no
        states across the outer time dimension, so we always return true.
                                        Detector1 (↑delay, 𝑥, 𝑛) := true
     • Structural Combinators: Call Detector1 for its sub-circuits. That is
                Detector1 (𝑐 1 ▷ 𝑐 2, 𝑥, 𝑛) := Detector1 (𝑐 1, 𝑥, 𝑛) ∧ Detector1 (𝑐 2, ⟦𝑐 1 ⟧(𝑥), 𝑛)
        and
                    Detector1 (𝑐 1 || 𝑐 2, 𝑥, 𝑛) := Detector1 (𝑐 1, 𝑥, 𝑛) ∧ Detector1 (𝑐 2, 𝑥, 𝑛)
     • Feedback Loops: For loop(𝑐), it calls the detector on the loop body and checks whether
       the new state of the 𝑧 −1 on the back edge (the current output) matches the stored state (the
       delayed output). 𝑜 denotes the loop output ⟦loop(𝑐)⟧(𝑥).
              Detector1 (loop(𝑐), 𝑥, 𝑛) := Detector1 (𝑐, (𝑥, 𝑧 −1 (𝑜)), 𝑛) ∧ (𝑜 (𝑛) = 𝑧 −1 (𝑜) (𝑛))
        For ↑loop(𝑐), the ↑𝑧 −1 on the back edge has no states across outer iterations, so it only calls
        the detector on the inner circuit. In the following, 𝑜 denotes ⟦↑loop(𝑐)⟧(𝑥).
                         Detector1 (↑loop(𝑐), 𝑥, 𝑛) := Detector1 (𝑐, (𝑥, ↑𝑧 −1 (𝑜)), 𝑛)
     • Level Adapters: For bracket(𝑐), it delegates to the internal circuit 𝑐:
                           Detector1 (bracket(𝑐), 𝑥, 𝑛) := Detector1 (𝑐, ↑𝛿 0 (𝑥), 𝑛)
        For lifting(𝑐), it lacks states across outer iterations:
                                       Detector1 (lifting(𝑐), 𝑥, 𝑛) := true
   Similarly, we define Detector2 as the level-2 StFP detector that accepts a level-2 circuit 𝑐, a nested
stream input 𝑥, an index (𝑚, 𝑛), and returns a boolean. For standard and primitive nodes and
structural combinators, it is defined by uniformly replacing Detector1 with Detector2 and the index
𝑛 with (𝑚, 𝑛). For other cases:
     • Temporal Nodes: For delay, it detects whether the delayed input from the last outer
       iteration has reached its fixpoint, which should have been stored in the state at the end of
       the last outer iteration (again, refer to the example at the end of §5):
                            Detector2 (delay, 𝑥, 𝑚, 𝑛) := FixAfter2 (𝑧 −1 (𝑥), 𝑚, 𝑛)
        For ↑delay, the condition drops to just checking the state along the inner dimension:
                         Detector2 (↑delay, 𝑥, 𝑚, 𝑛) := (𝑥 (𝑚, 𝑛) = ↑𝑧 −1 (𝑥) (𝑚, 𝑛))
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation        19


     • Feedback Loops: For loop(𝑐), similar to delay, it calls the detector on the internal circuit
       and checks whether the delayed output from the last outer iteration has reached its fixpoint.
       In the following, 𝑜 denotes ⟦loop(𝑐)⟧(𝑥).
       Detector2 (loop(𝑐), 𝑥, 𝑚, 𝑛) := Detector2 (𝑐, (𝑥, 𝑧 −1 (𝑜)), 𝑚, 𝑛) ∧ FixAfter2 (𝑧 −1 (𝑜), 𝑚, 𝑛)
        For ↑loop(𝑐), similar to ↑delay, it calls the detector on the internal circuit, and checks
        whether the current output matches the delayed output. In the following, 𝑜 denotes
        ⟦↑loop(𝑐)⟧(𝑥).
    Detector2 (↑loop(𝑐), 𝑥, 𝑚, 𝑛) := Detector2 (𝑐, (𝑥, ↑𝑧 −1 (𝑜)), 𝑚, 𝑛) ∧ (𝑜 (𝑚, 𝑛) = ↑𝑧 −1 (𝑜) (𝑚, 𝑛))
     • Level Adapters: For lifting(𝑐), it delegates to the level-1 detector:
                          Detector2 (lifting(𝑐), 𝑥, 𝑚, 𝑛) := Detector1 (𝑐, 𝑥 [𝑚], 𝑛)
   The FixAfter2 conditions in the level-2 delay and loop clauses do not require predicting the
future of the current outer iteration. Each is applied to a delayed stream, so its row at outer index
𝑚 comes from the already completed outer iteration 𝑚 − 1 (or is the zero row when 𝑚 = 0). Before
iteration 𝑚 begins, the runtime has stored that row through a convergence bound 𝐵. If 𝑛 ≥ 𝐵,
the bound immediately establishes FixAfter2 ; otherwise, the runtime decides it by comparing the
finitely many stored entries from 𝑛 through 𝐵, because all later entries equal the stored final value.
   Like the StFP predicate, the StFP detector is structural and level-indexed. Its clauses for structural
combinators recurse into sub-circuits, while its level-adapter clauses delegate across circuit levels.
Therefore, it applies compositionally to nested bracketed circuits rather than treating each recursive
component as an isolated case.
   We have proved the correctness of StFP via the following theorem:
Theorem 6.4 (Correctness of StFP Detector). For any circuit 𝑐,
                               ∀𝑥, 𝑛, Detector1 (𝑐, 𝑥, 𝑛) ⇐⇒ StFP1 (𝑐, 𝑥, 𝑛)
and for any level-2 circuit 𝑐,
                          ∀𝑥, 𝑚, 𝑛, Detector2 (𝑐, 𝑥, 𝑚, 𝑛) ⇐⇒ StFP2 (𝑐, 𝑥, 𝑚, 𝑛)
These immediately imply that the StFP detector is both sound and complete.
   The StFP detector should be read primarily as a correctness-oriented general fallback detector. It
establishes that StFP is decidable for arbitrary circuits in our core calculus. A fixed-input check
turns it into a local IntFP detector; applying that detector with zero-output checks across all
bracketed sub-circuits yields the sound and complete global IntConv detector and establishes
that IntConv is decidable as well. A practical implementation may optimize these checks or use a
specialized detector when one is justified. In particular, for Conv-complete classes, IntConv and
ExtConv coincide, so a sound and complete ExtConv detector also detects IntConv. FirstZero for
the naive and semi-naive circuits is one such specialized detector. Measuring the overhead of these
alternatives in a complete system is future work.

7   IntConv is Complete for Useful Circuits
By Thm. 5.6, IntConv is a sound sufficient condition for ExtConv. A natural question is: for what
circuits is IntConv complete? That is, when does mathematical convergence according to ExtConv
also imply IntConv? For such circuits, a system following the IntConv criterion faithfully implements
the theoretical specification. Moreover, because IntConv and ExtConv coincide on these circuits,
a sound and complete ExtConv detector also detects IntConv. This permits specialized detectors
such as FirstZero for the naive and semi-naive circuits instead of the general StFP detector from §6.
20                                                                                          Yang et al.


   To answer this question, we introduce a key property called convergence-complete (Conv-
complete) circuits. They are just the circuits mentioned above for which IntConv is complete.
In §7.1, we use regular circuits as a name for the fragment generated by the standard DBSP con-
structs for lifted scalar computation, composition, Datalog recursion, and while recursion. The
name lets us state a uniform completeness result for this existing recursive sublanguage: all regular
circuits are Conv-complete (Thm. 7.9). Moreover, in §7.2, we prove that the DBSP’s incremental
optimization (plift and incOpt) preserves Conv-completeness (Thm. 7.12 and Thm. 7.19). As a result,
all regular circuits and their incrementally optimized versions are Conv-complete.
   Along with Conv-completeness, its local version FP-completeness is important for us to establish
these results. We define them as follows:
Definition 7.1 (Conv-complete Circuit). A circuit 𝑐 is Conv-complete iff for every input 𝑥,
                                 ExtConv(𝑐, 𝑥) =⇒ IntConv(𝑐, 𝑥).
Definition 7.2 (FP-complete Circuit). Let 𝑐 be a well-formed circuit. We say 𝑐 is FP-complete if:
     • Level-1 completeness: for every input 𝑥 and index 𝑛, if ExtConv(𝑐, 𝑥) and ExtFP1 (𝑐, 𝑥, 𝑛)
        hold, then there exists 𝑛 ′ ∈ N such that IntFP1 (𝑐, 𝑥, 𝑛 ′ ) holds.
     • Level-2 completeness (for level-2 circuits): for every nested stream input 𝑥 and
        stream b, if ExtConv(𝑐, 𝑥) and ExtFP2 (𝑐, 𝑥, b) hold, then there exists a stream b′ such that
        IntFP2 (𝑐, 𝑥, b′ ) holds.
   We have established some compositional properties of Conv-completeness and FP-completeness.
In particular, Conv-completeness is closed under all circuit constructs except for bracket, while
FP-completeness is closed under all circuit constructs except for bracket and sequential composition
seq. These results are useful for us to establish the important results in this section.

7.1   Regular Circuits Are Conv-complete
Recall that we can use the DBSP circuit shown in Fig. 6a to express a Datalog-style recursive query.
We can express it in our formal language as follows.
Definition 7.3 (Datalog Recursive Query). For a level-1 circuit 𝑐 0 that represents a lifted scalar
query, the query body (the circuit between 𝛿 0 and ∫ ) of a Datalog-style recursive query is (the same
as Eqn. (1))
                                  datalogBody(𝑐 0 ) := Δ(loop(𝑐 0 ))
and the streaming query (the lifted version of the whole circuit) is
                   datalogQuery(𝑐 0 ) := bracket(lifting(datalogBody(𝑐 0 )))
  Beyond recursive relational queries, the following while program is used to show the Turing-
completeness of DBSP [6], where 𝑄 is an arbitrary scalar function:
x := i
while ( x != Q ( x ))
  x := Q ( x )
which can be implemented in DBSP as:
                            𝑖      𝛿0      +     ↑𝑄      D       ∫        𝑥

                                          𝑧 −1
In our formal language:
Definition 7.4 (While Loop Programs). For a level-1 circuit 𝑐 0 representing a lifted scalar function,
the query body of a while loop program is
                                whileBody(𝑐 0 ) := loop(add ▷ 𝑐 0 ) ▷ D
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation       21


and the streaming query is
                           whileQuery(𝑐 0 ) := bracket(lifting(whileBody(𝑐 0 )))
   Both query constructors above belong to the standard DBSP recursive sublanguage. Their
results are level-1 circuits representing lifted scalar functions, so they can be composed or placed
inside further recursive computations to form nested loops. We give the name regular circuits
to the sublanguage generated by these constructs so that we can state and prove FP- and Conv-
completeness uniformly. We use lifted scalar circuit for the base circuits that implement lifted scalar
or relational queries.
Definition 7.5 (Regular Circuit). Regular Circuits, denoted by RegularCkt, is the class of level-1
circuits defined inductively as follows:
      • Lifted Scalar Circuit: Any level-1 circuit composed (both sequentially and in parallel) of
        only primitive and standard nodes is a lifted scalar circuit, which is also a regular circuit.
      • Sequence and Parallel Composition: If 𝑐 1 and 𝑐 2 are regular circuits, their sequential
        composition 𝑐 1 ▷ 𝑐 2 and parallel composition 𝑐 1 || 𝑐 2 are regular circuits.
      • Datalog Query: Given a regular circuit 𝑐 0 , datalogQuery(𝑐 0 ) is a regular circuit.
      • While Loop: Given a regular circuit 𝑐 0 , whileQuery(𝑐 0 ) is a regular circuit.
   Using the inductive structure, it is easy to show that all regular circuits are FP-complete:
Lemma 7.6 (Regular Circuits are FP-complete). Any regular circuit 𝑐 is FP-complete. In particular,
for any 𝑥, 𝑛, ExtFP1 (𝑐, 𝑥, 𝑛) =⇒ IntFP1 (𝑐, 𝑥, 𝑛).
   We proceed to show that Datalog queries are Conv-complete. We first show that datalogBody
satisfies a variant of FP-completeness tailored for a recursive query body, whose input must be in
the form of 𝛿 0 (𝑥) and the fixed output is zero.
Lemma 7.7 (The iteration bound of datalogBody). If 𝑐 0 is a Conv-complete regular circuit, let
𝑐 := datalogBody(𝑐 0 ), for any scalar value 𝑥 and index 𝑛, we have
      ExtConv(𝑐, 𝛿 0 (𝑥)) ∧ ExtFP1 (𝑐, 𝛿 0 (𝑥), 𝑛) ∧ ⟦𝑐⟧(𝛿 0 (𝑥)) [𝑛] = 0 =⇒ IntFP1 (𝑐, 𝛿 0 (𝑥), 𝑛 + 1)
   This lemma gives the concrete upper bound 𝑛 + 1 on the iteration at which IntFP holds. It also
allows us to prove datalogQuery is Conv-complete.
Lemma 7.8. If 𝑐 0 is a Conv-complete regular circuit, then datalogQuery(𝑐 0 ) is Conv-complete.
   We have proved similar lemmas to establish the same iteration bound 𝑛 + 1 for whileBody and
the Conv-completeness of whileQuery. These lemmas allow us to prove that regular circuits are
Conv-complete by induction on the structure of regular circuits.
Theorem 7.9 (Regular Circuits are Conv-complete). Any regular circuit is Conv-complete.
   From the proof above, we can see that the class of regular circuits is highly extensible. We can
freely add more recursive circuit constructs similar to datalogBody and whileBody while preserving
Conv-completeness, as long as we can establish the variant of FP-completeness in Thm. 7.7 for the
new constructors.

7.2   Conv-complete Circuits Are Closed under Incremental Optimization
As we can see in our example, the standard incremental optimization of DBSP can be represented
by two syntactic transformations applied to a non-incremental circuit: plift to push the lifting
operator onto individual nodes and incOpt to apply compositional incremental rules. In this section,
we aim to show that plift and incOpt preserve Conv-completeness. To do this, we establish their
correctness theorems to show how they transform the denotation, the IntFP, and the IntConv of
the original circuit. The IntFP results track convergence bounds through these transformations;
they are semantic guarantees rather than measurements of runtime cost.
22                                                                                                    Yang et al.


  To formally state the correctness of plift, we introduce the notion of strong semantic equivalence
that requires the equivalence of both external denotation and internal convergence.
Definition 7.10 (Strong Semantic Equivalence). For any circuit 𝑐 1 and 𝑐 2 , we define the strong
semantic equivalence 𝑐 1 ≃ 𝑐 2 as follows:
                   ∀𝑥, ⟦𝑐 1 ⟧(𝑥) = ⟦𝑐 2 ⟧(𝑥) ∧ (IntConv(𝑐 1, 𝑥) ⇐⇒ IntConv(𝑐 2, 𝑥))
Note that this implicitly implies that ExtConv(𝑐 1, 𝑥) ⇐⇒ ExtConv(𝑐 2, 𝑥) because ⟦𝑐⟧ is partial.
     Based on this definition, we have re-established important equivalence lemmas in the DBSP
theory, such as the chain rule Δ(𝑐 1 ▷𝑐 2 ) ≃ Δ(𝑐 1 ) ▷ Δ(𝑐 2 ) and the lifting cycle rule lifting(loop(𝑐)) ≃
↑loop(lifting(𝑐)). Using these, we prove the correctness of plift as follows. It is a straightforward
induction on the structure of 𝑐.
Theorem 7.11 (Correctness of plift). For any level-1 circuit 𝑐,
      (1) (Denotation and IntConv) lifting(𝑐) ≃ plift(𝑐).
      (2) (IntFP1 ) For any 𝑥 and 𝑛, ExtFP1 (plift(𝑐), 𝑥, 𝑛) =⇒ IntFP1 (plift(𝑐), 𝑥, 𝑛).
      (3) (IntFP2 ) For any 𝑥 and 𝑚, 𝑛 ∈ N, IntFP1 (𝑐, 𝑥 [𝑚], 𝑛) =⇒ IntFP2 (plift(𝑐), 𝑥, 𝑚, 𝑛).
     This allows us to prove that plift preserves both Conv-completeness and FP-completeness.
Theorem 7.12 (plift preserves Conv-completeness and FP-completeness). For any level-1 circuit 𝑐,
if 𝑐 is Conv-complete, then plift(𝑐) is Conv-complete. If 𝑐 is FP-complete, then plift(𝑐) is FP-complete.
     For incOpt, the situation is more tricky. In particular, unlike lifting(𝑐) and plift(𝑐), Δ(𝑐) and
incOpt(𝑐) may have different IntConv behavior; just consider node(id) and Δ(node(id)). This
motivates us to introduce weak semantic equivalence, which only requires the equivalence of
external denotation but not internal convergence.
Definition 7.13 (Weak Semantic Equivalence). For any circuit 𝑐 1 and 𝑐 2 , we define the weak seman-
tic equivalence 𝑐 1 ≈ 𝑐 2 as ∀𝑥, ⟦𝑐 1 ⟧(𝑥) = ⟦𝑐 2 ⟧(𝑥). Note that this implies that ExtConv(𝑐 1, 𝑥) ⇐⇒
ExtConv(𝑐 2, 𝑥) since ⟦𝑐⟧ is a partial function.
     Besides denotation, how incOpt transforms IntFP is also tricky. To see this, consider the simplest
circuit id, whose optimized incremental form is itself. Although the two forms are the same circuit,
their corresponding input is different, because the input 𝑥 to the original form corresponds to the
input D (𝑥) to the incremental form. Because 𝑥 and D (𝑥) have different FixAfter indices in general,
the two forms have different IntFP in general. This observation suggests that the formulation of
the IntFP-preservation property that we desire for incOpt will be non-trivial.
     An important observation is that although 𝑥 and D (𝑥) may have different FixAfter indices, they
do have a connection as follows:
Proposition 7.14. For any stream 𝑠 and 𝑛 ∈ N, FixAfter1 (𝑠, 𝑛) ⇐⇒ ZeroAfter1 (D (𝑠), 𝑛 + 1),
and for any nested stream 𝑠 and b ∈ SN , FixAfter2 (𝑠, b) =⇒ FixAfter2 (D (𝑠), ↑ max(b, 𝑧 −1 (b))).
     Note that ZeroAfter implies FixAfter. This inspires us to raise a natural question: since input
streams of 𝑐 and incOpt(𝑐) have such FixAfter index relation, will all other intermediate streams share
the same relation? If so, as a result, IntConv should also be preserved. We formalize this idea as the
following preservation relation.
Definition 7.15 (IntFP and IntConv Preservation Relation). For any circuit 𝑐 1 and 𝑐 2 , we say that
𝑐 1 ’s IntFP1 is preserved by 𝑐 2 , denoted by 𝑐 1 ⇝1 𝑐 2 , if
                ∀𝑥, 𝑛, (ExtConv(𝑐 1, 𝑥) ∧ IntFP1 (𝑐 1, 𝑥, 𝑛)) =⇒ IntFP1 (𝑐 2, D (𝑥), 𝑛 + 1)
For level-2 circuit 𝑐 1 and 𝑐 2 , we say that 𝑐 1 ’s IntFP2 is preserved by 𝑐 2 , denoted by 𝑐 1 ⇝2 𝑐 2 , if
         ∀𝑥, b, (ExtConv(𝑐 1, 𝑥) ∧ IntFP2 (𝑐 1, 𝑥, b)) =⇒ IntFP2 (𝑐 2, D (𝑥), ↑ max(b, 𝑧 −1 (b)))
For any circuit 𝑐 1 and 𝑐 2 , we say that 𝑐 1 ’s IntConv is preserved by 𝑐 2 , denoted by 𝑐 1 ⇝𝐶 𝑐 2 , if
                               ∀𝑥, IntConv(𝑐 1, 𝑥) =⇒ IntConv(𝑐 2, D (𝑥))
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation   23


   These allow us to formally define what we expect from a “good” incremental optimization:
Definition 7.16 (Sound Incremental Form). For a circuit 𝑐 1 and 𝑐 2 , we say that 𝑐 2 is a sound
incremental form of 𝑐 1 if they satisfy the following four properties:
    (1) (Denotation) Δ(𝑐 1 ) ≈ 𝑐 2 .
    (2) (IntFP1 ) 𝑐 1 ⇝1 𝑐 2 .
    (3) (IntFP2 ) 𝑐 1 ⇝2 𝑐 2 if 𝑐 1 is a level-2 circuit.
    (4) (IntConv) 𝑐 1 ⇝𝐶 𝑐 2 .
  Another important challenge is that incOpt is a flexible and extensible algorithm, as different
primitive nodes can have different and custom incremental optimization. We deal with this via a
uniform assumption that incOpt transforms any primitive node into a sound incremental form.
This is a strong but still practical assumption, as we have established that the following common
incremental forms are all sound:
Proposition 7.17 (Common Sound Incremental Forms).
    (1) (Unoptimized) For any circuit 𝑐, Δ(𝑐) is a sound incremental form of 𝑐.
    (2) (Linear) For any linear function 𝑓 and 𝑐 = node(𝑓 ), 𝑐 is a sound incremental form of 𝑐.
    (3) (Bilinear) For any bilinear function 𝑓 and 𝑐 = node(𝑓 ), the DBSP’s bilinear incremental
        optimization [6] of 𝑐, denoted bilinearOpt(𝑐), is a sound incremental form of 𝑐.
   The unoptimized incremental form provides a general sound fallback for any primitive node,
ensuring the robustness of incOpt. From now on, we may assume that incOpt transforms all its
primitive nodes into a sound incremental form, and we can finally establish the correctness of
incOpt as follows:
Theorem 7.18 (Correctness of incOpt). For any circuit 𝑐, incOpt(𝑐) is a sound incremental form
of 𝑐.
   This allows us to show that incOpt preserves Conv-completeness.
Theorem 7.19 (incOpt preserves Conv-completeness). For any circuit 𝑐, if 𝑐 is Conv-complete,
then incOpt(𝑐) is Conv-complete.
   As a result, we can prove that the circuit implementing the delta-of-deltas strategy as shown in
Fig. 6c is Conv-complete.
Proposition 7.20. If 𝑐 0 is a regular circuit, then optDatalogQuery(𝑐 0 ) (Equation 4) is Conv-
complete.

8   Lean Formalization
All results in this paper have been formalized in Lean 4. We adapted the existing Lean 3 formalization
of the DBSP theory [8] to Lean 4 as a foundation, which accounts for 2,095 lines of code. On top of
this, we formalized our new theory in 11,748 additional lines of code, covering the core IntConv
theory, and its application such as a Hoare logic framework and several Zsets circuit case studies.
These counts use cloc and exclude blank lines and comments.
   The restriction of the stream level to ℓ ∈ {1, 2} in our formal language (§3.2) represents a
deliberate trade-off between formalization effort (especially with mechanized proofs) and theoretical
generality. This range is sufficient to express arbitrarily nested recursive queries and the delta-of-
deltas incremental optimization, while keeping the formal verification tractable. In principle, there
is no fundamental obstacle to generalizing ℓ to arbitrary natural numbers as our theory has already
been developed in an inductive style (the level-indexed predicate).
   Use of AI. AI is used to assist with Lean development and artifact preparation. The authors
carefully reviewed all definitions and theorem statements and take full responsibility for the paper,
formalization, and accompanying artifacts.
24                                                                                                    Yang et al.


9    Related Work
   Incremental computation. Incremental computing is a paradigm for computing based on the idea
of saving time by leveraging previous computational results. It has a long history, going back to the
1964 and 1967 papers of Lombardi [24, 25]. There have been contributions from many fields, includ-
ing theory (dynamic graph algorithms [4, 28] and dynamic data structures [5, 22]), databases (view
maintenance [10, 20]), programming languages (incremental lambda-calculus [15], incremental
parsing [17], interactive program-development environments [30], incremental dataflow analysis
[31], differential propagation in iterative fixpoint solvers [13], and finite-differencing transforma-
tions in optimizing compilers [27]), document-preparation systems [9], constraint solvers [16],
truth-maintenance systems [12], and no doubt many others. For a recent survey of incremental
computation, see [23].
   Some of the work described above is only for limited models of computation. DBSP is a Turing-
complete language. Because of its generality, DBSP could be applied to many of the application
areas addressed by previous work, although it would not necessarily provide the same runtime
guarantees of specialized results. However, many of these applications would need the ability to
detect fixpoints of nested computations. The work described in this paper contributes to realizing
the potential of DBSP by addressing an important semantic lacuna in the DBSP formalism.
   More specifically, prior work has studied incremental recursive and fixpoint computation from
complementary perspectives. Alvarez-Picallo et al. [3] develop a general theory of derivatives of
fixpoints for incremental evaluation of recursive computations and Datalog. Abo Khamis et al. [2]
characterize algebraic conditions under which Datalog over pre-semirings converges in finitely
many iterations and semi-naive evaluation applies. These works provide incremental fixpoint
constructions or convergence characterizations for particular Datalog semantics. Our contribution is
complementary: we formalize FPD as a finite-prefix runtime problem for incrementally transformed
circuits and establish its general limitations and its exact detectability for useful circuit classes.

   Feldera implementation of DBSP. As mentioned in §5 and §6, the Feldera implementation of
DBSP [14] uses internal-state stability to detect convergence. Its runtime gives each operator a
scope-indexed fixed-point check, intended to report whether the operator’s output will remain
stable under stable inputs, and declares a circuit stable when all of its operators report stability. Our
theory gives this established implementation strategy a declarative account: IntFP and IntConv
specify internal-state stability denotationally, StFP connects the declarative criterion to circuit state,
and the StFP detector gives an algorithmic formalization.
   The main novelty lies in the formal guarantees, especially the completeness result. We prove that
IntConv is sound and that the StFP detector is sound and complete. The global IntConv detector
combines the StFP detector with fixed-input and zero-output checks across all bracketed sub-circuits,
yielding sound and complete IntConv detection. We also prove that IntConv is complete for a large
class of useful circuits, including regular circuits and their incrementally optimized forms (§7). Thus,
for these circuits, the internal-state-stability criterion detects every convergence admitted by the
external specification. These results are machine-checked in Lean 4. Moreover, our level-indexed
predicates and detectors give a formal, compositional account of nested bracketed circuits, whereas
the Feldera SQL-to-DBSP compiler [14] rejects a nested recursive operator within recursive code.
Therefore, our theory may help guide future extended implementations.

   Differential Dataflow and its mathematical foundation. Differential Dataflow (DD) [26] also
incrementalizes recursive queries over versions 𝑇 × N, the DD counterpart of the delta-of-deltas
setting in our counterexample. At the collection level, Egress selects the first repeated collection,
at 𝑖 ∗ = min{𝑖 : 𝑊 (𝑡,𝑖 ) = 𝑊 (𝑡,𝑖 −1) }; its differential implementation instead operates on 𝛿𝑊 (𝑡,𝑖 ) . In this
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation                 25

                                                                                Í
setting, 𝛿𝑊 (𝑡,𝑖 ) = 0 does not imply a repetition, since 𝑊 (𝑡,𝑖 ) −𝑊 (𝑡,𝑖 −1) = 𝑠 ≤𝑡 𝛿𝑊 (𝑠,𝑖 ) . Thus, FirstZero
cannot soundly determine 𝑖 ∗ , and the paper defines differential Egress using 𝑖 ∗ without giving a
finite-prefix criterion for obtaining it from the differential trace. Similar to DBSP, this also turns
out to be a gap between the theory and the implementation of DD: its prototype instead reports
convergence when no outstanding differences remain in the dataflow, a global internal-quiescence
check similar in spirit to IntConv.
   A later developed mathematical foundation for DD by Abadi et al. [1], distinguishes fixed-iteration
egress from first-repetition egress, but formalizes only the fixed-iteration policy; it notes that first-
repetition egress would require partial streams. Consequently, its correctness theorem does not
provide a compositional denotational account of data-dependent first-repetition termination for
unbounded incremental iteration. Similarly, Flo [21], a semantic foundation for progressive stream
processing, requires bounded inner streams, leaving termination of unbounded inner iteration
outside its scope. Our theory instead gives a sound criterion for such unbounded computations and
identifies useful circuit classes for which that criterion is complete.

10   Conclusion
In this paper, we developed a formal theory of convergence detection to address the fundamental
gap between the mathematical specifications and practical implementations of Fixpoint Detection
(FPD) in modern incremental recursive computation frameworks like DBSP. We identified and
formalized the FPD problem, demonstrated that the commonly suggested “FirstZero” heuristic
is unsound for the “delta-of-deltas” incremental optimization for recursive computation, and
proved that exact FPD is impossible for arbitrary expressive circuits. Within our theory, we defined
internal convergence (IntConv) as a declarative criterion corresponding to the internal-state-stability
strategy used by practical implementations, and proved that it is a sound sufficient condition
for convergence. We also defined the State Fixpoint (StFP) predicate and a sound and complete
StFP detector, providing semantic and algorithmic formalizations of this strategy. The sound and
complete global IntConv detector combines the StFP detector with fixed-input and zero-output
checks across all bracketed sub-circuits. These predicates and detectors treat nested bracketed
circuits compositionally. Furthermore, we proved that IntConv is complete for a broad class of useful
circuits, including arbitrarily nested while loops, Datalog queries, and their incrementally optimized
versions. These results provide formal semantic guarantees for an existing implementation strategy,
and our results have been formalized in Lean 4.
   Our results are mainly theoretical, rather than an empirical performance evaluation. A natural
direction for future work is to implement and compare the global IntConv detector based on
the general StFP detector with specialized global detectors within a complete system. Such an
evaluation should measure detector overhead and compare end-to-end incremental execution with
non-incremental recomputation, since that comparison also depends on the query, workload, data
representation, and other system-level optimizations.

Data-Availability Statement
The Lean 4 formalization, including the impossibility result Theorem 4.7, is available with build
instructions at https://github.com/Arcadia-Y/fixing-the-fixpoint/. The repository also provides a
paper-to-Lean mapping that links the paper’s definitions and results to their formal declarations.
The development is described in §8.

References
 [1] Martín Abadi, Frank McSherry, and Gordon D. Plotkin. 2015. Foundations of Differential Dataflow. In Foundations of
     Software Science and Computation Structures. Springer, London, UK, 71–83. doi:10.1007/978-3-662-46678-0_5
26                                                                                                                  Yang et al.


 [2] Mahmoud Abo Khamis, Hung Q. Ngo, Reinhard Pichler, Dan Suciu, and Yisu Remy Wang. 2024. Convergence of
     Datalog over (Pre-) Semirings. J. ACM 71, 2 (2024), 8:1–8:55. doi:10.1145/3643027
 [3] Mario Alvarez-Picallo, Alex Eyers-Taylor, Michael Peyton Jones, and C.-H. Luke Ong. 2019. Fixing Incremental Com-
     putation: Derivatives of Fixpoints, and the Recursive Semantics of Datalog. In European Symposium on Programming
     (Lecture Notes in Computer Science, Vol. 11423). Springer, Prague, Czech Republic, 525–552. doi:10.1007/978-3-030-
     17184-1_19
 [4] Giorgio Ausiello, Umberto Nanni, and Giuseppe F Italiano. 1990. Dynamic maintenance of directed hypergraphs.
     Theoretical Computer Science 72, 2-3 (1990), 97–117.
 [5] Jon Louis Bentley and James B Saxe. 1980. Decomposable searching problems I. Static-to-dynamic transformation.
     Journal of Algorithms 1, 4 (1980), 301–358.
 [6] Mihai Budiu, Leonid Ryzhyk, Gerd Zellweger, Ben Pfaff, Lalith Suresh, Simon Kassing, Abhinav Gyawali, Matei Budiu,
     Tej Chajed, Frank McSherry, and Val Tannen. 2025. DBSP: automatic incremental view maintenance for rich query
     languages. The VLDB Journal 34, 4 (2025), 39. doi:10.1007/s00778-025-00922-y
 [7] Mario Carneiro. 2019. Formalizing Computability Theory via Partial Recursive Functions. In 10th International
     Conference on Interactive Theorem Proving (ITP 2019) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 141),
     John Harrison, John O’Leary, and Andrew Tolmach (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik,
     Dagstuhl, Germany, 12:1–12:17. doi:10.4230/LIPIcs.ITP.2019.12
 [8] Tej Chajed. 2022. DBSP Lean 3 Formalization. https://github.com/tchajed/database-stream-processing-theory.
 [9] Pehong Chen, Michael A Harrison, and Ikuo Minakata. 1988. Incremental document formatting. In Proceedings of the
     ACM conference on Document processing systems. ACM, Santa Fe, NM, USA, 93–100.
[10] Rada Chirkova and Jun Yang. 2012. Materialized views. Foundations and Trends in Databases 4, 4 (2012), 295–405.
     doi:10.1561/1900000020
[11] Leonardo Mendonça de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and Programming Language.
     In 28th International Conference on Automated Deduction (Lecture Notes in Computer Science, Vol. 12699). Springer,
     Virtual Event, 625–635. https://api.semanticscholar.org/CorpusID:235800962
[12] Jon Doyle. 1979. A truth maintenance system. Artificial intelligence 12, 3 (1979), 231–272.
[13] Christian Fecht and Helmut Seidl. 1998. Propagating differences: An efficient new fixpoint algorithm for distributive
     constraint systems. In European Symposium on Programming. Springer, Lisbon, Portugal, 90–104.
[14] Feldera      Inc.    2025.              Feldera     repository.               https://github.com/feldera/feldera/tree/
     ecac53677479a3bfdf12cd9551818fcd8fa246bc.           Commit ecac53677479a3bfdf12cd9551818fcd8fa246bc (Sep-
     tember 23, 2025).
[15] John Field and Tim Teitelbaum. 1990. Incremental reduction in the lambda calculus. In Proceedings of the 1990 ACM
     Conference on LISP and Functional Programming. ACM, Nice, France, 307–322.
[16] Bjorn N Freeman-Benson, John Maloney, and Alan Borning. 1990. An incremental constraint solver. Commun. ACM
     33, 1 (1990), 54–63.
[17] Carlo Ghezzi and Dino Mandrioli. 1979. Incremental parsing. ACM Transactions on Programming Languages and
     Systems (TOPLAS) 1, 1 (1979), 58–70.
[18] Sergio Greco and Cristian Molinaro. 2015. Datalog and Logic Databases. Springer, Cham, Switzerland. doi:10.1007/978-
     3-031-01854-1
[19] Todd J. Green, Zachary G. Ives, and Val Tannen. 2011. Reconcilable Differences. Theory of Computing Systems 49, 2
     (2011), 460–488. doi:10.1007/s00224-011-9323-x
[20] Ashish Gupta and Inderpal Singh Mumick (Eds.). 1999. Materialized Views: Techniques, Implementations, and Applications.
     The MIT Press, Cambridge, MA, USA.
[21] Shadaj Laddad, Alvin Cheung, Joseph M. Hellerstein, and Mae Milano. 2025. Flo: A Semantic Foundation for Progressive
     Stream Processing. Proceedings of the ACM on Programming Languages 9, POPL (2025), 241–270. doi:10.1145/3704845
[22] J van Leeuwen and Derick Wood. 1980. Dynamization of decomposable searching problems. Inform. Process. Lett. 10, 2
     (1980), 51–56.
[23] Yanhong A. Liu. 2024. Incremental Computation: What Is the Essence? (Invited Contribution). In Proceedings of the
     2024 ACM SIGPLAN International Workshop on Partial Evaluation and Program Manipulation, PEPM 2024, London, UK,
     16 January 2024, Gabriele Keller and Meng Wang (Eds.). ACM, London, UK, 39–52. doi:10.1145/3635800.3637447
[24] L.A. Lombardi and B. Raphael. 1964. LISP as the Language for an Incremental Computer. In The Programming Language
     LISP: Its Operation and Applications, Edmund C. Berkeley and Daniel G. Bobrow (Eds.). The MIT Press, Cambridge,
     MA, USA, 204–219.
[25] Lionello A. Lombardi. 1967. Incremental Computation: The Preliminary Design of a Programming System Which Allows
     for Incremental Data Assimilation in Open-Ended Man-Computer Information Systems. In Advances in Computers,
     Franz L. Alt and Morris Rubinoff (Eds.). Vol. 8. Academic Press, New York, NY, USA, 247–333. doi:10.1016/S0065-
     2458(08)60698-1
Fixing the Fixpoint: A Formal Theory of Convergence Detection for Incremental Recursive Computation                   27


[26] Frank McSherry, Derek Gordon Murray, Rebecca Isaacs, and Michael Isard. 2013. Differential Dataflow. In 6th Biennial
     Conference on Innovative Data Systems Research. CIDRDB, Asilomar, CA, USA, 12 pages. https://www.cidrdb.org/
     cidr2013/Papers/CIDR13_Paper111.pdf
[27] Robert Paige and Shaye Koenig. 1982. Finite differencing of computable expressions. ACM Transactions on Programming
     Languages and Systems (TOPLAS) 4, 3 (1982), 402–454.
[28] Ganesan Ramalingam and Thomas Reps. 1996. An incremental algorithm for a generalization of the shortest-path
     problem. Journal of Algorithms 21, 2 (1996), 267–305.
[29] G. Ramalingam and Thomas W. Reps. 1993. A Categorized Bibliography on Incremental Computation. In Conference
     Record of the Twentieth Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, Charleston,
     South Carolina, USA, January 1993, Mary S. Van Deusen and Bernard Lang (Eds.). ACM Press, Charleston, SC, USA,
     502–510. doi:10.1145/158511.158710
[30] Thomas Reps, Tim Teitelbaum, and Alan Demers. 1983. Incremental context-dependent analysis for language-based
     editors. ACM Transactions on Programming Languages and Systems (TOPLAS) 5, 3 (1983), 449–477.
[31] Barbara G Ryder and Marvin C Paull. 1988. Incremental data-flow analysis algorithms. ACM Transactions on
     Programming Languages and Systems (TOPLAS) 10, 1 (1988), 1–50.
