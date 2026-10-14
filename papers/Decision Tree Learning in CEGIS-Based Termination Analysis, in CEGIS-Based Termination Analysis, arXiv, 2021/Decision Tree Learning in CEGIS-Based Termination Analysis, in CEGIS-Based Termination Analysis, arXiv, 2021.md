                                                      Decision Tree Learning
                                                in CEGIS-Based Termination Analysis

                                                       Satoshi Kura1,2 , Hiroshi Unno3,4 , and Ichiro Hasuo1,2
                                                          1
                                                            National Institute of Informatics, Tokyo, Japan
                                                  2
                                                      The Graduate University for Advanced Studies (SOKENDAI),
                                                                          Kanagawa, Japan
arXiv:2104.11463v3 [cs.LO] 5 Jul 2021




                                                              3
                                                                University of Tsukuba, Ibaraki, Japan
                                                                   4
                                                                      RIKEN AIP, Tokyo, Japan




                                              Abstract. We present a novel decision tree-based synthesis algorithm
                                              of ranking functions for verifying program termination. Our algorithm is
                                              integrated into the workflow of CounterExample Guided Inductive Syn-
                                              thesis (CEGIS). CEGIS is an iterative learning model where, at each
                                              iteration, (1) a synthesizer synthesizes a candidate solution from the
                                              current examples, and (2) a validator accepts the candidate solution if
                                              it is correct, or rejects it providing counterexamples as part of the next
                                              examples. Our main novelty is in the design of a synthesizer: building
                                              on top of a usual decision tree learning algorithm, our algorithm detects
                                              cycles in a set of example transitions and uses them for refining decision
                                              trees. We have implemented the proposed method and obtained promis-
                                              ing experimental results on existing benchmark sets of (non-)termination
                                              verification problems that require synthesis of piecewise-defined lexico-
                                              graphic affine ranking functions.



                                        1   Introduction

                                        Termination Verification by Ranking Functions and CEGIS Termination verifi-
                                        cation is a fundamental but challenging problem in program analysis. Termina-
                                        tion verification usually involves some well-foundedness arguments. Among them
                                        are those methods which synthesize ranking functions [16]: a ranking function
                                        assigns a natural number (or an ordinal, more generally) to each program state,
                                        in such a way that the assigned values strictly decrease along transition. Exis-
                                        tence of such a ranking function witnesses termination, where well-foundedness
                                        of the set of natural numbers (or ordinals) is crucially used.
                                            We study synthesis of ranking functions by CounterExample Guided Induc-
                                        tive Synthesis (CEGIS) [28]. CEGIS is an iterative learning model in which a
                                        synthesizer and a validator interact to find solutions for given constraints. At
                                        each iteration, (1) a synthesizer tries to find a candidate solution from the cur-
                                        rent examples, and (2) a validator accepts the candidate solution if it is correct,
                                        or rejects it providing counterexamples. These counterexamples are then used
                                        as part of the next examples (Fig. 1).
2

                                       a candidate solution σ                    constraints C
            Synthesizer:
            find a candidate                                          Validator:
            solution σ that is                                        Is σ a solution for C?
            consistent with E
                                       No: a set E of examples
                                                                                 Yes: answer σ
         No solution             (Validator adds new examples to E)


                                 Fig. 1: the CEGIS architecture


    CEGIS has been applied not only to program verification tasks (synthesis of
inductive invariants [17, 18, 24, 25], that of ranking functions [19], etc.) but also
to constraint solving (for CHC [12, 14, 27, 35], for pwCSP(T ) [29, 30], etc.). The
success of CEGIS is attributed to the degree of freedom that synthesizers enjoy.
In CEGIS, synthesizers receive a set of individual examples that synthesizers
can use in various creative and speculative manners (such as machine learning).
In contrast, in other methods such as [5–8, 23, 26], synthesizers receive logical
constraints that are much more binding.

Segmented Synthesis in CEGIS-Based Termination Analysis The choice of a
candidate space for candidate solutions σ is important in CEGIS. A candidate
space should be expressive: by limiting a candidate space, the CEGIS architec-
ture may miss a genuine solution. At the same time, complexity should be low:
a larger candidate space tends to be more expensive for synthesizers to handle.
    This tradeoff is also in the choice of the type of examples: using an expressive
example type, a small number of examples can prune a large portion of the can-
didate space; however, finding such expressive examples tends to be expensive.
    In this paper, we use piecewise affine functions as our candidate space for
ranking functions. Piecewise affine functions are functions of the form
                                      
                                        a ·x  e + b1 xe ∈ L1
                                       1
                                      
                                       e
                                           ..
                         f (e
                            x) =            .                                    (1)
                                      
                                      
                                      ea ·x  e+bn    e∈L
                                                      x     n             n

where {L1 , . . . , Ln } is a partition of the domain of f (e
                                                            x) such that each Li is a
polyhedron (i.e. a conjunction of linear inequalities). We say segmented synthesis
to emphasize that our synthesis targets are piecewise affine functions with case
distinction. Piecewise affine functions stand on a good balance between expres-
siveness and complexity: the tasks of synthesizers and validators can be reduced
to linear programming (LP); at the same time, case distinction allows them to
model a variety of situations, especially where there are discontinuities in the
function values and/or derivatives.
    We use transition examples as our example type (Table 1). Transition exam-
ples are pairs of program states that represent transitions; they are much cheaper
to handle compared to trace examples (finite traces of executions until termi-
nation) used e.g. in [15, 32]. The current work is the first to pursue segmented
synthesis of ranking functions with transition examples; see Table 1.
                                                                                           3


                      Table 1: ranking function synthesis by CEGIS
       candidate space \ example type trace examples                 transition examples
           affine ranking functions       [15, 32]                            [19]
      piecewise affine ranking functions  [15, 32]                       our method


                           e+
                            2
                                                               e1               h1
                                     h1                                    e2
             e+
              1
                                e−    e−                       e4
                                 4     5
                                                                     e3
                                                                                h2
                      e+
                       3             h2

                                                                    h1
                       h1
                                                      f1 (e
                                                          x)
            +                                                             h2
                                h2                    {e1 }
         {e+    +
           1 , e2 }                                             f2 (e
                                                                    x)           f3 (e
                                                                                     x)
                     −                     +
                                                                {e2 }            {e3 }
                  {e−    −
                    4 , e5 }              {e+
                                            3 }
                                                      (b) For ranking functions
               (a) For invariants

                                 Fig. 2: Decision tree learning


Decision Tree Learning for CEGIS-Based Termination Analysis: a Challenge In
this paper, we represent piecewise affine functions (1) by the data structure of
decision trees. The data structure suits the CEGIS architecture (Fig. 1): iterative
refinement of candidate solutions can be naturally expressed by growing decision
trees. The main challenge of this paper is the design of an effective synthesizer
for decision trees—such a synthesizer learns decision trees from examples.
    In fact, decision tree learning in the CEGIS architecture has already been
actively pursued, for the synthesis of invariants as opposed to ranking func-
tions [12, 14, 18, 22, 35]. It is therefore a natural idea to adapt the decision tree
learning algorithms used there, from invariants to ranking functions. However,
we find that a naive adaptation of those algorithms for invariants does not suffice:
they are good at handling state examples that appear in CEGIS for invariants;
but they are not good at handling transition examples.
    More specifically, when decision tree learning is applied to invariant syn-
thesis (Fig. 2a), examples are given in the form of program states labeled as
positive or negative. Decision trees are then built by iteratively selecting the
best halfspaces—where “best” is in terms of some quality measures—until each
leaf contains examples with the same label. One common quality measure used
here is an information-theoretic notion of information gain.
    We extend this from invariant synthesis to ranking function synthesis where
examples are given by transitions instead of states (Fig. 2b). In this case, a
major challenge is to cope with examples that cross a border of the current
segmentation—such as the transition e4 crossing the border h1 in Fig. 2b. Our
decision tree learning algorithm should handle such crossing examples, taking
4

into account the constraints imposed on the leaf labels affected by those examples
(the affected leaf labels are f1 (e
                                  x) and f3 (e
                                             x) in the case of e4 ).

Our Algorithm: Cycle-Based Decision Tree Learning for Transition Examples
We use what we call the cycle detection theorem (Theorem 17) as a theoretical
tool to handle such crossing examples. The theorem claims the following: if
there is no piecewise affine ranking function with the current segmentation of
the domain (such as the one in Fig. 2b given by h1 and h2 ), then this must be
caused by a certain type of cycle of constraints, which we call an implicit cycle.
    In our decision tree learning algorithm, when we do not find a piecewise affine
ranking function with the current segmentation, we find an implicit cycle and
refine the segmentation to break the cycle. Once all the implicit cycles are gone,
the cycle detection theorem guarantees the existence of a candidate piecewise
affine ranking function with the segmentation.
    We integrate this decision tree learning algorithm in the CEGIS architecture
(Fig. 1) and use it as a synthesizer. Our implementation of this framework gives
promising experimental results on existing benchmark sets.

Contribution Our contribution is summarized as follows.
    – We provide a decision tree-based synthesizer for ranking functions integrated
      into the CEGIS architecture. Our synthesizer uses transition examples to
      find candidate piecewise affine ranking functions. A major challenge here,
      namely handling constraints arising from crossing examples, is coped with
      by our theoretical observation of the cycle detection theorem.
    – We implement our synthesizer for ranking functions implemented in Mu-
      Val and report the experience of using MuVal for termination and non-
      termination analysis. The experiment results show that MuVal’s perfor-
      mance is comparable to state-of-the-art termination analyzers [7, 10, 13, 21]
      from Termination Competition 2020, and that MuVal can prove (non-)ter-
      mination of some benchmarks with which other analyzers struggle.

Organization. Section 2 shows the overview of our method via examples. Sec-
tion 3 explains our target class of predicate constraint satisfaction problems and
how to encode (non-)termination problem into such constraints. In Section 4, we
review CEGIS architecture, and then explain simplification of examples into pos-
itive/negative examples. Section 5 proposes our main contribution, our decision
tree-based ranking function synthesizer. Section 6 shows our implementation and
experimental results. Related work is discussed in Section 7, and we conclude in
Section 8.


2      Preview by Examples
We present a preview of our method using concrete examples. We start with an
overview of the general CEGIS architecture, after which we proceed to our main
contribution, namely a decision tree learning algorithm for transition examples.
                                                                                                   5

2.1   Termination Verification by CEGIS

Our method follows the usual workflow of termination verification by CEGIS.
It works as follows: given a program, we encode the termination problem into
a constraint solving problem, and then use the CEGIS architecture to solve the
constraint solving problem.

Encoding the termination problem. The first step of our method is to encode the
termination problem as the set C of constraints.

Example 1. As a running example, consider the following C program.
while ( x != 0) { if ( x < 0) { x ++; } else { x - -; } }

The termination problem is encoded as the following constraints.

                          x < 0 ∧ x0 = x + 1 =⇒ R(x, x0 )                                      (2)
                       ¬(x < 0) ∧ x0 = x − 1 =⇒ R(x, x0 ).                                     (3)

Here, R is a predicate variable representing a well-founded relation, and term
variables x, x0 are universally quantified implicitly.

    The set C of constraints claims that the transition relation for the given
program is subsumed by a well-founded relation. So, verifying termination is now
rephrased as the existence of a solution for C. Note that we omitted constraints
for invariants for simplicity in this example (see Sect. 3 for the full encoding).

Constraint solving by CEGIS.             synthesizer                                   validator
The next step is to solve C by
                                                                E =∅
CEGIS.                                     (i)
                                                             R(x, x0 ) = ⊥
    In the CEGIS architecture, a                                                            (ii)
                                                            E = {R(1, 0)}
synthesizer and a validator iter-         (iii)
                                                    R(x, x0 ) = x > x0 ∧ x ≥ 0
                                                                                            (iv)
atively exchange a set E of ex-                     E = {R(1, 0), R(−2, −1)}
                                          (v)
amples and a candidate solution                    R(x, x0 ) = |x| > |x0 | ∧ |x| ≥ 0        (vi)
R(x, x0 ) for C. At the moment, we
present a rough sketch of CEGIS,         Fig. 3: An example of CEGIS iterations
leaving the details of our imple-
mentation to Sect. 2.2.

Example 2. Fig. 3 shows how the CEGIS architecture solves the set C of con-
straints shown in (2) and (3). Fig. 3 consists of three pairs of interactions (i)-(vi)
between a synthesizer and a validator.

 (i) The synthesizer takes E = ∅ as a set of examples and returns a candidate
     solution R(x, x0 ) = ⊥ synthesized from E. In general, candidate solutions
     are required to satisfy all constraints in E, but the requirement is vacuously
     true in this case.
6

 (ii) The validator receives the candidate solution and finds out that the can-
      didate solution is not a genuine solution. The validator finds that the as-
      signment x = 1, x0 = 0 is a counterexample for (3), and thus adds R(1, 0)
      to E to prevent the same candidate solution in the next iteration.
(iii) The synthesizer receives the updated set E = {R(1, 0)} of examples, finds
      a ranking function f (x) = x for E (i.e. for the transition from x = 1 to
      x0 = 0), and returns a candidate solution R(x, x0 ) = x > x0 ∧ x ≥ 0.
(iv) The validator checks the candidate solution, finds a counterexample x =
      −2, x0 = −1 for (2), and adds R(−2, −1) to E.
 (v) The synthesizer finds a ranking function f (x) = |x| for E and returns
      R(x, x0 ) = |x| > |x0 | ∧ |x| ≥ 0 as a candidate solution. Note that the
      synthesizer have to synthesize a piecewise affine function here, but details
      are deferred to Sect. 2.2.
(vi) The validator accepts the candidate solution because it is a genuine solution
      for C.


2.2   Handling Cycles in Decision Tree Learning

We explain the importance of handling cy-
cles in our decision tree-based synthesizer                                y ≥ 0?
of piecewise affine ranking functions.                              ≥               <
    In what follows, we deal with such de-
cision trees as shown in Fig. 4: their inter-                 x − 1 ≥ 0?        f (x, y) = −y
nal nodes have affine inequalities (i.e. half-            ≥                <
spaces); their leaves have affine functions;
and overall, such a decision tree expresses      f (x, y) = x − 1   f (x, y) = 1 − x
a piecewise affine function (Fig. 4). When
we remove leaf labels from such a decision          f (x, y) =
tree, then we obtain a template of piecewise        
functions where condition guards are given          x − 1 y ≥ 0 ∧ x − 1 ≥ 0
                                                    
but function bodies are not. We shall call             1−x y ≥0∧x−1<0
                                                    
the latter a segmentation.                             −y      y<0
                                                    

                                                 Fig. 4: An example of a decision
Input and output of our synthesizer.
                                                 tree that represents a piecewise
The input of our synthesizer is a set
                                                 affine ranking function f (x, y)
E of transition examples (e.g. E =
{R(1, 0), R(−2, −1)}) as explained in Sect. 2.1. The output of our synthesizer
is a well-founded relation R(e    e0 ) := f (e
                               x, x                  x0 ) ∧ f (e
                                             x) > f (e         x) ≥ 0 where x
                                                                            e is a se-
quence of variables and f (ex) is a piecewise affine function, which is represented
by a decision tree (Fig. 4). Therefore our synthesizer aims at learning a suitable
decision tree.

Refining segmentations and handling cycles. Roughly speaking, our synthesizer
learns decision trees in the following steps.
                                                                                  7


                               f (x)
       −2    −1     0     1     2               −2    −1     0     1     2
            (a) Good (x ≥ 0)                         (b) Bad (x ≥ −2)

Fig. 5: Selecting halfspaces. Transition examples are shown by red arrows.
Boundaries of halfspaces are shown by dashed lines.


1. Generate a set H of halfspaces from the given set E of examples. This H
   serves as the vocabulary for internal nodes. Set the initial segmentation to
   be the one-node tree (i.e. the trivial segmentation).
2. Try to synthesize a piecewise affine ranking function f for E with the current
   segmentation—that is, try to find suitable leaf labels. If found, then use this
   f in a candidate well-founded relation R(e    e0 ) = f (e
                                              x, x                 x0 ) ∧ f (e
                                                           x) > f (e         x) ≥ 0.
3. Otherwise, refine the current segmentation with some halfspace in H, and
   go to Step 2.

The key step of our synthesizer is Step 3. We show a few examples.

Example 3. Suppose we are given E = {R(1, 0), R(−2, −1)} as a set of ex-
amples. Our synthesizer proceeds as follows: (1) Our synthesizer generates the
set H := {x ≥ 1, x ≥ 0, x ≥ −2, x ≥ −1} from the examples in E. (2) Our
synthesizer tries to find a ranking function of the form f (x) = ax + b (with
the trivial segmentation), but there is no such ranking function. (3) Our syn-
thesizer refines the current segmentation with (x ≥ 0) ∈ H because x ≥ 0
“looks good”. (4) Our synthesizer tries to find a ranking function of the form
f (x) = if x ≥ 0 then ax + b else cx + d, using the current segmentation. Our
synthesizer obtains f (x) = if x ≥ 0 then x else − x and use this f (x) for a
candidate solution.
    How can we decide which halfspace in H “looks good”? We use quality mea-
sure that is a value representing the quality of each halfspace and select the
halfspace with the maximum quality measure.
    Fig. 5 shows the comparison of the quality of x ≥ 0 and x ≥ −2 in this
example. Intuitively, x ≥ 0 is better than x ≥ −2 because we can obtain a
simple ranking function if x ≥ 0 then x else − x with x ≥ 0 (Fig. 5a) while we
need further refinement of the segmentation with x ≥ −2 (Fig. 5b). In Sect. 5,
we introduce a quality measure for halfspaces following this intuition.
    Our synthesizer iteratively refines segmentations following this quality mea-
sure, until examples contained in each leaf of the decision tree admit an affine
ranking function. This approach is inspired by the use of information gain in the
decision tree learning for invariant synthesis.

   Example 3 showed a natural extension of a decision tree learning method for
invariant synthesis. However, this is not enough for transition examples, for the
reasons of explicit and implicit cycles. Here are their examples.
8




          −2          −1           0            1           2           3

Fig. 6: Two examples R(−1, 1) and R(1, 0) make an implicit cycle between x ≥ 1
and ¬(x ≥ 1).


Example 4. Suppose we are given E = {R(1, 0), R(0, 1)}. In this case, there
is no ranking function because E contains a cycle 1 → 0 → 1 witnessing non-
termination. We call such a cycle an explicit cycle.

Example 5. Let E = {R(−1, 1), R(1, 0), R(−1, −2), R(2, 3)} (Fig. 6). Our syn-
thesizer proceeds as follows. (1) Our synthesizer generates the set H := {x ≥
1, x ≥ 0, . . . } of halfspaces. (2) Our synthesizer tries to find a ranking function
of the form f (x) = ax + b (with the trivial segmentation), but there is no such.
(3) Our synthesizer refines the current segmentation with (x ≥ 1) ∈ H because
x ≥ 1 “looks good” (i.e. is the best with respect to a quality measure).
    We have reached the point where the naive extension of decision tree learn-
ing explained in Example 3 no longer works: although all constraints contained
in each leaf of the decision tree admit an affine ranking function, there is no
piecewise affine ranking function for E of the form f (x) = if x ≥ 1 then ax +
b else cx + d.
    More specifically, in this example, the leaf representing x ≥ 1 contains R(2, 3),
and the other leaf representing ¬(x ≥ 1) contains R(−1, −2). The example
R(2, 3) admits an affine ranking function f1 (x) = −x + 2, and R(−1, −2) ad-
mits f2 (x) = x + 1, respectively. However, the combination f (x) = if x ≥
1 then f1 (x) else f2 (x) is not a ranking function for E. Moreover, there is no
ranking function for E of the form f (x) = if x ≥ 1 then ax + b else cx + d.
    It is clear that this failure is caused by the crossing examples R(−1, 1) and
R(1, 0). It is not that every crossing example is harmful. However, in this case,
the set {R(−1, 1), R(1, 0)} forms a cycle between the leaf for x ≥ 1 and the leaf
for ¬(x ≥ 1) (see Fig. 6). This “cycle” among leaves—in contrast to explicit
cycles such as {R(1, 0), R(0, 1)} in Example 4—is called an implicit cycle.
    Once an implicit cycle is found, our synthesizer cuts it by refining the current
segmentation. Our synthesizer continues the above steps (1–3) of decision tree
learning as follows. (4) Our synthesizer selects (x ≥ 0) ∈ H and cuts the im-
plicit cycle {R(−1, 1), R(1, 0)} by refining segmentations. (5) Using the refined
segmentation, our synthesizer obtains f (x) = if x ≥ 1 then − x + 2 else if x ≥
0 then 0 else x + 3 as a ranking function for E.

    As explained in Example 4,5, handling (explicit and implicit) cycles is crucial
in decision tree learning for transition examples. Moreover, our cycle detection
theorem (Theorem 17) claims that if there is no explicit or implicit cycle, then one
can find a ranking function for E without further refinement of segmentations.
                                                                                          9

3    (Non-)Termination Verification as Constraint Solving

We explain how to encode (non-)termination verification to constraint solving.
    Following [30], we formalize our target class pwCSP of predicate constraint
satisfaction problems parametrized by a first-order theory T .

Definition 6. Given a formula φ, let ftv (φ) be the set of free term variables
and fpv (φ) be the set of free predicate variables in φ.

Definition 7. A pwCSP is defined as a pair (C, R) where C is a finite set of
clauses of the form
                        `
                                  !     m
                                                     !
                        _               _
                    φ∨    Xi (ti ) ∨
                              e             ¬Xi (ti )
                                                 e                       (4)
                               i=1               i=`+1


and R ⊆ fpv (C) is a set of predicate variables that are required to denote well-
founded relations. Here, 0 ≤ ` ≤ m. Meta-variables t and φ range over T -terms
and T -formulas, respectively, such that ftv (φ) = ∅. Meta-variables x and X
range over term and predicate variables, respectively.

A pwCSP (C, R) is called CHCs (constrained Horn clauses, [9]) if R = ∅ and
` ≤ 1 for all clauses c ∈ C. The class of CHCs has been widely studied in the
verification community [12, 14, 27, 35].

Definition 8. A predicate substitution σ is a finite map from predicate variables
X to closed predicates of the form λx1 , . . . , xar(X) .φ. We write dom(σ) for the
domain of σ and σ(C) for the application of σ to C.

Definition 9. A predicate  V substitution σ is a (genuine) solution for (C, R) if (1)
fpv (C) ⊆ dom(σ); (2) |= σ(C) holds; and (3) for all X ∈ R, σ(X) represents
a well-founded relation, that is, sort(σ(X)) = (e        s, se) → • for some sequence se of
sorts and there is no infinite sequence ve1 , ve2 , . . . of sequences vei of values of the
sorts se such that |= ρ(X)(evi , vei+1 ) for all i ≥ 1.


Encoding termination. Given a set of initial state ι(e  x) and a transition relation
τ (e  e0 ), the termination verification problem is expressed by the pwCSP (C, R)
   x, x
where R = {R}, and C consists of the following clauses.

 ι(e
   x) =⇒ I(e
           x)          τ (e  e0 ) ∧ I(e
                          x, x                x0 )
                                      x) =⇒ I(e          τ (e  e0 ) ∧ I(e
                                                            x, x        x) =⇒ R(e  e0 )
                                                                                x, x

We use φ =⇒ ψ as syntax sugar for ¬φ ∨ ψ, so this is a pwCSP. The well-
founded relation R asserts that τ is terminating. We also consider an invariant
I for τ to avoid synthesizing ranking functions on unreachable program states.
10

Encoding non-termination. We can also encode a problem of non-termination
verification to pwCSP via recurrent sets [20]. For simplicity, we explain the
encoding for the case of only one program variable x. We consider a recurrent
set R satisfying the following conditions.

                              ι(x) =⇒ R(x)                                            (5)
                                               0       0      0
                             R(x) =⇒ ∃x .τ (x, x ) ∧ R(x )                            (6)

To remove ∃ from (6), we use the following constraint that is equivalent to (6).

          R(x) =⇒ E(x, 0)                                                             (7)
             0                0        0
                                           
       E(x, x ) =⇒     τ (x, x ) ∧ R(x )
                 ∨ S(x0 , x0 − 1) ∧ E(x, x0 − 1) ∨ S(x0 , x0 + 1) ∧ E(x, x0 + 1) (8)
                                                                               

    The intuition is as follows. Given x in the recurrent set R, the relation E(x, x0 )
searches for the value of ∃x0 in (6). The search starts from x0 = 0 in (7), and
x0 is nondeterministically incremented or decremented in (8). The well-founded
relation S asserts that the search finishes within finite steps. As a result, we
obtain a pwCSP for non-termination defined by (C, R) where R = {S} and C is
given by (5), (7), and (the disjunctive normal form of) (8).
Example 10. Consider the following C program.
       while ( x > 0) { x = -2 * x + 9; }
The non-termination problem is encoded as the pwCSP (C, R) where R = {S},
and C consists of

       x > 0 =⇒ R(x)                               R(x) =⇒ E(x, 0)
     E(x, x0 ) =⇒ x0 = −2x + 9 ∧ R(x0 )
                   ∨ (S(x0 , x0 − 1) ∧ E(x, x0 − 1)) ∨ (S(x0 , x0 + 1) ∧ E(x, x0 + 1)).

The program is non-terminating when x = 3. This is witnessed by a solution σ for
(C, R), which is given by σ(R)(x) := x = 3, σ(E)(x, x0 ) := x = 3∧0 ≤ x0 ∧x0 ≤ 3,
and σ(S)(x0 , x00 ) := x00 = x0 + 1 ∧ x00 ≤ 3.


4      CounterExample-Guided Inductive Synthesis (CEGIS)
We explain how CounterExample-Guided Inductive Synthesis [28] (CEGIS for
short) works for a given pwCSP (C, R) following [30]. Then, we add the extraction
of positive/negative examples to the CEGIS architecture, which enables our
decision tree-based synthesizer to use a simplified form of examples.
    CEGIS proceeds through the iterative interaction between a synthesizer and
a validator (Fig. 1), in which they exchange examples and candidate solutions.
                                                                    V
Definition 11. A formula φ is an example of C if ftv (φ) = ∅ and C |= φ hold.
Given a set E of examples of C, a predicate substitution σ is a candidate solution
for (C, R) that is consistent with E if σ is a solution for (E, R).
                                                                                   11

Synthesizer. The input for a synthesizer is a set E of examples of C collected from
previous CEGIS iterations. The synthesizer tries to find a candidate solution
σ consistent with E instead of a genuine solution for (C, R). If the candidate
solution σ is found, then σ is passed to the validator. If E is unsatisfiable, then
E witnesses unsatisfiability of (C, R). Details of our synthesizer is described in
Sect. 5.

Validator. A validator checks whether the candidate solution σ from the synthe-
         a genuine solution of (C, R)
sizer is V                         V by using SMT solvers. That is, satisfiability
of |= ¬ σ(C) is checked. If |= ¬ σ(C) is not satisfiable, then σ is a genuine so-
lution of the original pwCSP (C, R), so the validator accepts this. Otherwise, the
validator adds new examples to the set E of examples. Finally, the synthesizer
is invoked Vagain with the updated set E of examples.
    If |= ¬ σ(C) is satisfiable, new examples are constructed as follows. Using
SMT solvers, the validator obtains an assignment θ to term variables such that |=
¬θ(ψ) holds for some ψ ∈ σ(C). By (4), |= ¬θ(ψ) is a clause of the form |= ¬θ(φ)∧
  V`                      Vm                    
    i=1 ¬σ(Xi )(θ(ti )) ∧    i=`+1 σ(Xi )(θ(ti )) . To prevent this counterexample
                   e                        e
from being found in the next CEGIS iteration again, the validator adds the
following example to E.
                          `
                          _                      m
                                                 _
                                      ti )) ∨
                                Xi (θ(e                 ¬Xi (θ(e
                                                               ti ))              (9)
                          i=1                   i=`+1

    The CEGIS architecture repeats this interaction between the synthesizer and
the validator until a genuine solution for (C, R) is found or E witnesses unsatis-
fiability of (C, R).

Extraction of positive/negative examples. Examples obtained in the above ex-
planation are a bit complex to handle in our decision tree-based synthesizer:
each example in E is a disjunction (9) of literals, which may contain multiple
predicate variables.
                                                                         +       −
    To simplify the form of examples, we extract from E the sets EX         and EX of
positive examples (i.e., examples of the form X(e    v )) and negative examples (i.e.,
examples of the form ¬X(e   v )) for each X ∈ fpv (E). This allows us to synthesize a
predicate σ(X) for each predicate variable X ∈ fpv (E) separately. For simplicity,
               +             −                        +                 −
we write ve ∈ EX and ve ∈ EX    instead of X(ev ) ∈ EX   and ¬X(ev ) ∈ EX .
    The extraction is done as follows. We first substitute for each predicate vari-
able application X(e v ) in E a boolean variable bX(ev) to obtain a SAT problem
SAT(E). Then, we use SAT solvers to obtain an assignment η that is a solution
for SAT(E). If a solution η exists, then we construct positive/negative examples
from η; otherwise, E is unsatisfiable.
Definition 12. Let η be a solution for SAT(E). For each predicate variable
                                +                                     +
X ∈ fpv (E), we define the set EX of positive examples and the set EX   of negative
                                       +                                  −
examples under the assignment η by EX := {e   v | η(bX(ev) ) = true} and EX := {e
                                                                                v|
η(bX(ev) ) = false}.
12

Note that some of predicate variable applications X(e          v ) may not be assigned true
nor false because they do not affect the evaluation of SAT(E). Such predicate
                                                      +    −
variable applications are discarded from {(EX           , EX )}X∈fpv (E) .
     Our method uses the extraction of positive and negative examples when the
validator passes examples to the synthesizer. If X ∈ fpv (E) ∩ R, then we apply
                                            +     −
our ranking function synthesizer to (EX        , EX  ). If X ∈ fpv (E) \ R, then we apply
an invariant synthesizer.
                                                                      +     −
     We say a candidate solution σ is consistent with {(EX               , EX )}X∈fpv (E) if |=
         +                    −
σ(X)(e  v ) and |= ¬σ(X)(e   v ) hold for each predicate variable X ∈ fpv (E), ve+ ∈
  +              −                                                           +    −
EX  , and ve− ∈ EX . If a candidate solution σ is consistent with {(EX         , EX )}X∈fpv (E) ,
then σ is also consistent with E.
                                       +    −
     Note that unsatisfiability of {(EX  , EX  )}X∈fpv (E) does not immediately implies
                                                  +     −
unsatisfiability of E nor (C, R) because {(EX       , EX  )}X∈fpv (E) depends on the choice
of the assignment η. Therefore, the CEGIS architecture need to be modified: if
                                            +     −
synthesizers find unsatisfiability of {(EX    , EX  )}X∈fpv (E) , then we add the negation
of an unsatisfiability core to E to prevent using the same assignment η again.
     Note that some restricted forms of (9) have also been considered in previous
work and are called implication examples in [17] and implication/negation con-
straints in [12]. Our extraction of positive and negative examples is applicable
to the general form of (9).


5     Ranking Function Synthesis

In this section, we describe one of the main contributions, that is, our decision
tree-based synthesizer, which synthesizes a candidate well-founded relation σ(R)
                   +
from a finite set ER of examples. We assume that only positive examples are given
because well-founded relations occur only positively in pwCSP for termination
analysis (see Sect. 3). The aim of our synthesizer is to find a piecewise affine
                                                         +
lexicographic ranking function fe(ex) for the given set ER of examples. Below, we
                                                           +
fix a predicate variable R ∈ R and omit the subscript ER     = E +.


5.1    Basic Definitions

To represent piecewise affine lexicographic ranking functions, we use decision
trees like the one in Figure 4. Let x
                                    e = (x1 , . . . , xn ) be the program variables
where each xi ranges over Z.

Definition 13. A decision tree D is defined by D := ge(e        x) | if h(e
                                                                          x) ≥ 0 then D
else D where ge(e x) = (gk (e
                            x), . . . , g0 (e
                                            x)) is a tuple of affine functions and h(ex)
is an affine function. A segmentation tree S is defined as a decision tree with
undefined leaves ⊥: that is, S := ⊥ | if h(e         x) ≥ 0 then S else S. For each
decision tree D, we can canonically assign a segmentation tree by replacing the
label of each leaf with ⊥. This is denoted by S(D). For each decision tree D, we
denote the corresponding piecewise affine function by feD (e       x) : Zn → Zk+1 .
                                                                                           13

Each leaf in a segmentation tree S corresponds to a polyhedron. We often identify
the segmentation tree S with the set of leaves of S and a leaf with the polyhedron
corresponding to the leaf. For example, we say something like “for each L ∈ S,
ve ∈ L is a point in the polyhedron L”.
    Suppose we are given a segmentation tree S and a set E + of examples.
Definition 14. For each L1 , L2 ∈ S, we denote the set of example transitions
from L1 to L2 by EL+1 ,L2 := {(e       v , ve0 ) ∈ E + | ve ∈ L1 , ve0 ∈ L2 }. An example
       0     +
 v , ve ) ∈ E is crossing w.r.t. S if (e
(e                                           v , ve0 ) ∈ EL+1 ,L2 for some L1 6= L2 , and non-
                            +
crossing if (e v , ve0 ) ∈ EL,L for some L.

Definition 15. We define the dependency graph G(S, E + ) for S and E + by the
graph (V, E) where vertices V = S are leaves, and edges E = {(L1 , L2 ) | L1 6=
       v , ve0 ) ∈ EL+1 ,L2 } are crossing examples.
L2 , ∃(e

   We denote the set of start points ve and end points ve0 of examples (e
                                                                        v , ve0 ) ∈ E +
     + :=             0     +      0         0     +
by E      {e
           v | (e
                v , ve ) ∈ E } ∪ {e
                                  v | (e
                                       v , ve ) ∈ E }.


5.2    Segmentation and (Explicit and Implicit) Cycles:
       One-Dimensional Case

For simplicity, we first consider the case where fe(e   x) = f (e  x) : Zn → Z is a one-
dimensional ranking function. Our aim is to find a ranking function f (e        x) for E + ,
                         0     +               0               0      +
which satisfies ∀(ev , ve ) ∈ E . f (e        v ) and ∀(e
                                     v ) > f (e          v , ve ) ∈ E . f (e
                                                                           v ) ≥ 0. If our
ranking function synthesizer finds such a ranking function f (e      x), then a candidate
well-founded relation Rf is constructed as Rf (e       e0 ) := f (e
                                                    x, x           x) ≥ 0 ∧ f (e       x0 ).
                                                                               x) > f (e
     Our synthesizer builds a decision tree D to find a ranking function fD (e       x) for
E + . The main question in doing so is “when and how should we refine partitions
of decision trees?” To answer this question, we consider the case where there
is no ranking function fD (e   x) for E + with a fixed segmentation S, and classify
reasons for this into three cases as follows.

Case 1: explicit cycles in examples. We define an explicit cycle in E + as a cycle in
the graph (Zn , E + ). An explicit cycle witnesses that there is no ranking function
for E + (see e.g., Example 4).

Case 2: non-crossing examples are unsatisfiable. The second case is when there
is a leaf L ∈ S such that no affine (not piecewise affine) ranking function for the
      +
set EL,L  of non-crossing examples exists. This prohibits the existence of piecewise
                    x) for E + with segmentation S = S(D) because the restriction
affine function fD (e
                                                               +
of fD (ex) to L ∈ S must be an affine ranking function for EL,L   .

Case 3: implicit cycles in the dependency graph. We define an implicit cycle by
a cycle in the dependency graph G(S, E + ). Case 3 is the case where an implicit
cycle prohibits the existence of piecewise affine ranking functions for E + with
the segmentation S (e.g., Example 5). If Case 1 and Case 2 do not hold but
14

no piecewise affine ranking function for E + with the segmentation S exists,
then there must be an implicit cycle by (the contraposition of) the following
proposition.
Proposition 16. Assume E + is a set of examples that does not contain explicit
cycles (i.e. Case 1 does not hold). Let S be a segmentation tree and assume
                                                                         +
that for each L ∈ S, there exists an affine ranking function fL (e
                                                                 x) for EL,L (i.e.
                                                        +
Case 2 does not hold). If the dependency graph G(S, E ) is acyclic, then there
exists a decision tree D with the segmentation S(D) = S such that fD (e   x) is a
ranking function for E + .
Proof. By induction on the height (i.e. the length of a longest path from a
vertex) of vertices in G(S, E + ). We construct a decision tree D as follows. If
the height of L ∈ S is 0, then we assign fL0 (e              x) := fL (e
                                                                       x) to the leaf L where
                                             +
fL (ex) is a ranking function for EL,L            . If the height of L ∈ S is n > 0, then we
assign fL0 (e  x) := fL (e  x) + c to the leaf L where c ∈ Z is a constant that satisfies
                +
∀(ev , ve0 ) ∈ EL,L         v ) + c > fL0 0 (e
                    0 , fL (e                v 0 ) for each cell L0 with the height less than
n.                                                                                          t
                                                                                            u
Note that the converse of Proposition 16 does not hold: the existence of implicit
cycles in G(S, E + ) does not necessarily imply that no piecewise affine ranking
function exists with the segmentation S.

5.3    Segmentation and (Explicit and Implicit) Cycles:
       Multi-Dimensional Lexicographic Case
We consider a more general case where fe(e    x) = (fk (e
                                                        x), . . . , f0 (e
                                                                        x)) is a multi-
dimensional lexicographic ranking function and k is a fixed nonnegative integer.
   Given a function fe(ex), we consider the well-founded relation Rfe(e      e0 ) defined
                                                                          x, x
inductively as follows.
 R() (e  e0 ) := ⊥
      x, x             R(fk ,...,f0 ) (e  e0 ) := fk (e
                                       x, x           x) ≥ 0 ∧ fk (e        x0 )
                                                                   x) > fk (e                   (10)
                                                                 0
                                                 ∨fk (e         x ) ∧ R(fk−1 ,...,f0 ) (e
                                                       x) = fk (e                          e0 )
                                                                                        x, x

   Our aim here is to find a lexicographic ranking function fe(e      x) for E + , i.e. a
                                    0                        0     +
function fe(e
            x) such that Rfe(e                         v , ve ) ∈ E . Our synthesizer
                              v , ve ) holds for each (e
does so by building a decision tree. The same argument as the one-dimensional
case holds for lexicographic ranking functions.
Theorem 17 (cycle detection). Assume E + is a set of examples that does not
contain explicit cycles. Let S be a segmentation tree and assume that for each L ∈
                                                                            +
                                        x) that satisfies ∀(e
S, there exists an affine function feL (e                      v , ve0 ) ∈ EL,L , RfeL (e v , ve0 ).
                                  +
If the dependency graph G(S, E ) is acyclic, then there exists a decision tree D
with the segmentation S(D) = S such that RfeD (e  v , ve0 ) holds for each (e   v , ve0 ) ∈ E + .

Proof. The proof is almost the same as Proposition 16. Here, note that if fe0 (e
                                                                               x) =
fe(e
   x) + e
        c where e
                c is a tuple of nonnegative integer constants, then Rfe0 (e      e0 )
                                                                              x, x
                  0
subsumes Rfe(e
             x, x
                e ).                                                               t
                                                                                   u
                                                                                              15

Algorithm 1 Building decision trees.
Input: a set E + of examples, an integer k ≥ 0
Output: a well-founded relation R such that ∀(e                 x, x e0 ) ∈ E + , R(e  e0 )
                                                                                    x, x
 1: if E has a cycle then
 2:     return unsatisfiable
 3: end if
 4: D := ResolveCase2(E)
 5: while true do
 6:     C := GetConstraints(D, E)
 7:     O := SumAbsParams(D)
 8:     ρ := Minimize(O, C)
 9:     if ρ is defined then
10:            x) := feρ(D) (e
            fe(e             x)
11:         return Rfe
12:     else
13:         get an unsat core in C
14:                                 v1 , ve10 ), . . . , (e
            find an implicit cycle (e                     vl , vel0 ) in the unsat core
15:         find a cell C and two distinct points vei0 , vei+1 ∈ C in the implicit cycle
16:         add a halfspace to separate vei0 and vei+1 and update D
17:     end if
18: end while



5.4    Our Decision Tree Learning Algorithm

We design a concrete algorithm based on Theorem 17. It is shown in Algorithm 1
and consists of three phases. We shall describe the three phases one by one.

Phase 1 Phase 1 (Line 1-3) detects explicit cycles in E + to exclude Case 1.
Here, we use a cycle detection algorithm for directed graphs.

Phase 2 Phase 2 (Line 4) detects and resolves Case 2 by using ResolveCase2
(Algorithm 2), which is a function that grows a decision tree recursively. Re-
solveCase2 takes non-crossing examples in a leaf, divides the leaf, and returns
a template tree that is fine enough to avoid Case 2. Here, template trees are
decision trees whose leaves are labeled by affine templates.
    Algorithm 2 shows the detail of ResolveCase2. ResolveCase2 builds a
template tree recursively starting from the trivial segmentation S = ⊥ and all
given examples. In each polyhedron, ResolveCase2 checks whether the set C
of constraints imposed by non-crossing examples can be satisfied by an affine
lexicographic ranking function on the polyhedron (Line 2-3). If the set C of
constraints is not satisfiable, then ResolveCase2 chooses a halfspace h(e             x) ≥ 0
(Line 6) and divides the current polyhedron by the halfspace.
    There is a certain amount of freedom in the choice of halfspaces. To guaran-
tee termination of the whole algorithm, we require that the chosen halfspace h
separates at least one point in E 0+ := {e     v , ve0 ) ∈ E 0+ } ∪ {e
                                          v | (e                     v 0 | (e
                                                                            v , ve0 ) ∈ E 0+ }
                            0+
from the other points in E . That is:
16

Algorithm 2 Resolving Case 2.
 1: function ResolveCase2(E 0+ )
 2:    fe := MakeAffineTemplate(k)
 3:    C := GetConstraints(fe, E 0+ )
 4:    ρ := GetModel(C)
 5:    if ρ is undefined then
 6:         h := ChooseQualifier(E 0+ )
 7:         D≥0 := ResolveCase2({(e           v , ve0 ) ∈ E 0+ | h(e           v 0 ) ≥ 0})
                                                                   v ) ≥ 0 ∧ h(e
                                                    0       0+
 8:         D<0  := ResolveCase2({(e          v , ve ) ∈ E | h(e               v 0 ) < 0})
                                                                   v ) < 0 ∧ h(e
 9:         return (if h(e  x) ≥ 0 then D≥0 else D<0 )
10:    else
11:         return fe
12:    end if
13: end function
14: function GetConstraints(D, E + )
15:    return {RfeD (e v , ve0 ) | (e
                                    v , ve0 ) ∈ E + } where feD is the tuple of piecewise affine
    functions corresponding to D
16: end function

Algorithm 3 A criterion for eager qualifier selection.
 1: function QualityMeasure(h, E 0+ )
 2:             v , ve0 ) ∈ E 0+ | h(e
       E++ := {(e                    v ) ≥ 0 ∧ h(e
                                                 v ) ≥ 0}
 3:             v , ve0 ) ∈ E 0+ | h(e
       E+− := {(e                    v ) ≥ 0 ∧ h(e
                                                 v ) < 0}
 4:             v , ve0 ) ∈ E 0+ | h(e
       E−+ := {(e                    v ) < 0 ∧ h(e
                                                 v ) ≥ 0}
 5:             v , ve0 ) ∈ E 0+ | h(e
       E−− := {(e                    v ) < 0 ∧ h(e
                                                 v ) < 0}
 6:    f := MakeAffineTemplate(k)
       e
 7:    C+ := GetConstraints(fe, E++ )                C− := GetConstraints(fe, E−− )
 8:    N+ := MaxSmt(C+ )                             N− := MaxSmt(C− )
 9:    return N+ + N− + (|E+− | + |E−+ |)(1 − entropy(|E+− |, |E−+ |))
10: end function



Assumption 18. If halfspace h(e     x) ≥ 0 is chosen in Line 6 of Algorithm 2, then
                e ∈ E 0+ such that h(e
there exist ve, u                    v ) ≥ 0 and h(e
                                                   u) < 0.
   We explain two strategies (eager and lazy) to choose halfspaces that can be
used to implement ChooseQualifier. Both of them are guaranteed to termi-
nate, and moreover, intended to yield simple decision trees.

Eager strategy. In the eager strategy, we eagerly generate a finite set H of
halfspaces from the set E + of all examples beforehand and choose the best one
from H with respect to a certain quality measure. To satisfy Assumption 18,
H are generated so that any two points u        e, ve ∈ E + can be separated by some
halfspace (h(e     x) ≥ 0) ∈ H.
    For example, we can use intervals H = {±(xi − ai ) ≥ 0 | i = 1, . . . , n ∧
(a1 , . . . , an ) ∈ E + } and octagons H = {±(xi − ai ) ± (xj − aj ) ≥ 0 | i 6=
                                     e = (x1 , . . . , xn ). For any input E 0+ ⊆ E + of
j ∧ (a1 , . . . , an ) ∈ E + } where x
                                                                                        17

ResolveCase2, intervals and octagons satisfy ∅ 6= H 0 := {h(e     x) ≥ 0 | ∃e  e∈
                                                                            v, u
E 0+ .h(e
        v ) ≥ 0 ∧ h(e
                    u) < 0}, so Assumption 18 is satisfied by choosing the best
halfspace with respect to the quality measure from H 0 .
     For each halfspace (h(ex) ≥ 0) ∈ H 0 , we calculate QualityMeasure in Al-
gorithm 3, and choose one that maximizes QualityMeasure(h, E 0+ ). Quali-
tyMeasure(h, E 0+ ) calculates the sum of the maximum number of satisfiable
constraints in each leaf divided by h(e  x) ≥ 0 plus an additional term (|E+− | +
                                                                x        x      y
|E−+ |)(1 − entropy(|E+− |, |E−+ |)) where entropy(x, y) = − x+y   log2 x+y − x+y
       y
log2 x+y . Therefore, the term (|E+− | + |E−+ |)(1 − entropy(|E+− |, |E−+ |)) is
close to |E+− | + |E−+ | if almost all examples in E+− ∪ E−+ cross h in the same
direction and close to 0 if |E+− | is almost equal to |E−+ |.

Lazy strategy. In the lazy strategy, we lazily generate halfspaces. We divide the
current polyhedron so that non-crossing examples in the cell point to almost the
same direction.
                                               +
     First, we label states that occur in EC,C     as follows. We find a direction that
most examples in C point to by solving the MAX-SMT ~a := max~a {(e              v , ve0 ) ∈
  +                 0                               +
EC,C | ~a · (e                         v , ve ) ∈ EC,C , we label two points ve, ve0 with
             v − ve ) > 0} . For each (e     0
                  0
+1 if ~a · (e
            v − ve ) > 0 and with −1 otherwise.
     Then we apply weighted C-SVM to generate a hyperplane that separates
most of the positive and negative points. To guarantee termination of Algo-
rithm 1, we avoid “useless” hyperplanes that classify all the points by the same
label. If we obtain such a useless hyperplane, then we undersample a majority
class and apply C-SVM again. By undersampling suitably, we eventually get
linearly separable data with at least one positive point and one negative point.
     Note that since coefficients of hyperplanes extracted from C-SVM are floating
point numbers, we have to approximate them by hyperplanes with rational coef-
ficients. This is done by truncating continued fraction expansions of coefficients
by a suitable length.

Phase 3 In Line 5-18 of Algorithm 1, we further refine the segmentation S(D)
to resolve Case 3. Once Case 2 is resolved by ResolveCase2, Case 2 never
holds even after refining S(D) further. This enables to separate Phases 2 and 3.
    Given a template tree D, we consider the set C of constraints on parameters
in D that claims feD (ex) is a ranking function for E + (Line 6).
    If C is satisfiable, we use an SMT solver to obtain a solution of C (i.e. an
assignment ρ of integers to parameters) while minimizing the sum of absolute
values of unknown parameters in D at the same time (Line 8). This minimization
is intended to give a simple candidate ranking function. The solution ρ is used
to instantiate the template tree D (Line 11).
    If C cannot be satisfied, there must be an implicit cycle in the dependency
graph G(S(D), E + ) by Theorem 17. The implicit cycle can be found in an un-
satisfiable core of C. We refine the segmentation of D to cut the implicit cycle in
Line 16. To guarantee termination, we choose a halfspace satisfying the following
assumption, which is similar to Assumption 18.
18

Assumption 19. If halfspace h(e     x) ≥ 0 is chosen in Line 16 of Algorithm 1,
                     e ∈ E + such that h(e
then there exist ve, u                   v ) ≥ 0 and h(e
                                                       u) < 0.
    We have two strategy (eager and lazy) to refine the segmentation of D.
    In eager strategy, we choose a halfspace (h(e      x) ≥ 0) ∈ H that separates two
distinct points vei0 and vei+1 in the implicit cycle. In doing so, we want to reduce
the number of implicit cycles in G(S(D), E + ), but adding a new halfspace may
                                                                +
introduce new implicit cycles if there exists (e   v , ve0 ) ∈ EC,C that crosses the new
                            0
border from the side of vei to the side of vei+1 . Therefore, we choose a hyperplane
that minimizes the number of new crossing examples.
    In lazy strategy, we use an SMT solver to find a hyperplane h(e         x) ∈ H that
separates vei0 and vei+1 and minimizes the number of new crossing examples.


Termination Assumption 18 and Assumption 19 guarantees that every leaf in
S(D) contains at least one point in the finite set E + . Because the number of
leaves in S(D) strictly increases after each iteration of Phase 2 and Phase 3,
we eventually get a segmentation S(D) where each L ∈ S(D) contains only one
point in E + in the worst case. Since we have excluded Case 1 at the beginning,
Theorem 17 guarantees the existence of ranking function with the segmentation
S(D). Therefore, the algorithm terminates within |E + | times of refinement.

Theorem 20. If Assumption 18 and Assumption 19 hold, then Algorithm 1
terminates. If Algorithm 1 returns a piecewise affine lexicographic function fe(e  x),
then the function satisfies Rfe(e  e0 ) for each (e
                                x, x                 e0 ) ∈ E + where E + is the input
                                                  x, x
of the algorithm.                                                                   t
                                                                                    u


5.5     Improvement by Degenerating Negative Values

There is another way to define well-founded relation from the tuple fe(e                           x) =
(fk (e
     x), . . . , f0 (ex)) of functions, that is, the well-founded relation Rf0e(e                e0 ) de-
                                                                                              x, x
                              0
fined inductively by R()        (e  e0 ) := ⊥ and R(f
                                 x, x                 0
                                                          k ,...,f0 )
                                                                      (e  e0 ) := fk (e
                                                                       x, x           x) ≥ 0 ∧ fk (ex) >
     0               0                          0     0
                                                                             e0 ).
                                                  
    x ) ∨ fk (e
fk (e             x ) < 0 ∨ fk (e x) = fk (e   x ) ∧ R(fk−1 ,...,f0 ) (e x, x
    In this definition, we loosen the equality fi (e             x) = fi (e   x0 ) (where i = 1, . . . , k)
                                                                    0
of the usual lexicographic ordering (10) to fi (e                x ) < 0 ∨ fi (e              x0 ). This
                                                                                     x) = fi (e
means that once fi (e      x) becomes negative, fi (e     x) must stay negative but the value
do not have to be the same, which is useful for the synthesizer to avoid complex
candidate lexicographic ranking functions and thus improves the performance.
    However, if we use this well-founded relation Rf0e(e                  x, xe0 ) instead of Rfe(ex, x e0 )
                                                        0         0
in (10), then Theorem 17 fails because Rfe(e                x, x e ) is not necessarily subsumed
       0
by Rfe+ec where e       c = (ck , . . . , c0 ) is a nonnegative constant (see the proof of
Proposition 16 and Theorem 17). As a result, there is a chance that no implicit
cycle can be found in line 14 of Algorithm 1. Therefore, when we use Rf0e(e                           e0 ),
                                                                                                   x, x
we modify Algorithm 1 so that if no implicit cycle can be found in line 14, then
we fall back on the former definition of Rfe(e            x, xe0 ) and restart Algorithm 1.
                                                                                  19

6     Implementation and Evaluation

Implementation. We implemented a constraint solver MuVal that supports in-
variant synthesis and ranking function synthesis. For invariant synthesis, we
apply an ordinary decision tree learning (see [12, 14, 18, 22, 35] for existing tech-
niques). For ranking function synthesis, we implemented the algorithm in Sect. 5
with both eager and lazy strategies for halfspace selection. Our synthesizer uses
well-founded relation explained in Sect. 5.5. Given a benchmark, we run our
solver for both termination and non-termination verification in parallel, and
when one of the two returns an answer, we stop the other and use the answer.
MuVal is written in OCaml and uses Z3 as an SMT solver backend. We used
clang and llvm2kittel [1] to convert C benchmarks to T2 [3] format files, which
are then translated to pwCSP by MuVal.

Experiments. We evaluated our implementation MuVal on C benchmarks from
Termination Competition 2020 (C Integer) [4]. We compared our tool with
AProVE [10, 13], iRankFinder [7], and Ultimate Automizer [21]. Experi-
ments are conducted on StarExec [2] (CentOS 7.7 (1908) on Intel(R) Xeon(R)
CPU E5-2609 0 @ 2.40GHz (2393 MHZ) with 263932744 kB main memory). The
time limit was 300 seconds.

Results. Results are shown in Ta- Table 2: Numbers of solved benchmarks
ble 2. Yes/No/TO/U means the
                                                              Yes No TO U
number of benchmarks that these
                                            MuVal (eager)     204 89 42 0
tools could verify termination/-
                                            MuVal (lazy)      200 84 51 0
could verify non-termination/could
                                               AProVE         216 100 16 3
not answer within 300 seconds and
                                            iRankFinder       208 925 0 34
timed out (TimeOut)/gave up be-
                                        Ultimate Automizer 180 83 2 70
fore 300 seconds (Unknown), respec-
tively. We also show scatter plots of runtime in Fig. 7.
    MuVal was able to solve more benchmarks than Ultimate Automizer.
Compared to iRankFinder, MuVal solved slightly fewer benchmarks, but was
faster in a large number of benchmarks: 265 benchmarks were solved faster by
MuVal, 68 by iRankFinder, and 2 were not solved by both tools within 300
seconds (here, we regard U (unknown) as 300 seconds). Compared to AProVE,
MuVal solved fewer benchmarks. However, there are several benchmarks that
MuVal could solve but AProVE could not. Among them is “TelAviv-Amir-
Minimum true-termination.c”, which does require piecewise affine ranking func-
tions. MuVal found a ranking function f (x, y) = if x − y ≥ 0 then y else x,
while AProVE timed out.
    We also observed that using CEGIS with transition examples itself showed
its strengths even for benchmarks that do not require piecewise affine ranking
functions. Notably, there are three benchmarks that MuVal could solve but the
5
    We removed one benchmarks from the result of iRankFinder because the answer
    was wrong.
20


             100                              100                                          100




     MuVal




                                      MuVal




                                                                                   MuVal
             10                               10                                           10




              1                                1                                            1




                   1      10    100                 1            10          100                 1        10          100
                       AProve                           irankfinder v1.3.2                       Ultimate Automizer


Fig. 7: Scatter plots of runtime. Ultimate Automizer and AProVE some-
times gave up before the time limit, and such cases are regarded as 300s.


other tools could not; they are examples that do not require segmentations. Fur-
ther analysis of these benchmarks indicates the following strengths of our frame-
work: (1) the ability to handle nonlinear constraints (to some extent) thanks to
the example-based synthesis and the recent development of SMT solvers; and
(2) the ability to find a long lasso-shaped non-terminating trace assembled from
multiple transition examples. See Appendix A for details.


7        Related Work
There are a bunch of works that synthesize ranking functions via constraint solv-
ing. Among them is a counterexample-guided method like CEGIS [28]. CEGIS
is sound but not guaranteed to be complete in general: even if a given constraint
has a solution, CEGIS may fail to find the solution. A complete method for
ranking function synthesis is proposed in [19]. They collect only extremal coun-
terexamples instead of arbitrary transition examples to avoid infinitely many
examples. A limitation of their method is that the search space is limited to
(lexicographic) affine ranking functions.
    Another counterexample-guided method is proposed in [32] and implemented
in SeaHorn. This method can synthesize piecewise affine functions, but their
approach is quite different from ours. Given a program, they construct a safety
property that the number of loop iterations does not exceed the value of a
candidate ranking function. The safety property is checked by a verifier. If it
is violated, then a trace is obtained as a counterexample and the candidate
ranking function is updated by the counterexample. The main difference from
our method is that their method uses trace examples while our method uses
transition examples (which is less expensive to handle). FreqTerm [15] also
uses the connection to safety property, but they exploit syntax-guided synthesis
for synthesizing ranking functions.
    Aside from counterexample-guided methods, constraint solving is widely stud-
ied for affine ranking functions [26], lexicographic affine ranking functions [5, 7,
23], and multiphase affine ranking functions [6,8]. Their implementation includes
RankFinder and iRankFinder. Farkas’ lemma or Motzkin’s transposition
theorem are often used as a tool to transform ∃∀-constraints to ∃-constraints.
                                                                                  21

However, when we apply this technique to piecewise affine ranking functions, we
get nonlinear constraints [23].
    Abstract interpretation is also applied to segmented synthesis of ranking
functions and implemented in FuncTion [31, 33, 34]. In this series of work,
decision tree representation of ranking functions is used in [34] for better handling
of disjunctions. Compared to their work, we believe that our method is more
easily extensible to other theories than linear integer arithmetic as long as the
theories are supported by SMT solvers (although such extensions are out of the
scope of this paper).
    Other state-of-the-art termination verifiers include the following. Ultimate
Automizer [21] is an automata-based method. It repeatedly finds a trace and
computes a termination argument that contains the trace until termination ar-
guments cover the set of all traces. Büchi automata are used to handle such
traces. AProVE [10, 13] is based on term rewriting systems.

8   Conclusions and Future Work
In this paper, we proposed a novel decision tree-based synthesizer for ranking
functions, which is integrated into the CEGIS architecture. The key observation
here was that we need to cope with explicit and implicit cycles contained in given
examples. We designed a decision tree learning algorithm using the theoretical
observation of the cycle detection theorem. We implemented the framework and
observed that its performance is comparable to state-of-the-art termination an-
alyzers. In particular, it solved three benchmarks that no other tool solved, a
result that demonstrates the potential of the current combination of CEGIS,
segmented synthesis, and transition examples.
    We plan to extend our ranking function synthesizer to a synthesizer of piece-
wise affine ranking supermartingales. Ranking supermartingales [11] are prob-
abilistic version of ranking functions and used for verification of almost-sure
termination of probabilistic programs.
    We also plan to implement a mechanism to automatically select a suitable
set of halfspaces with which decision trees are built. In our ranking function
synthesizer, intervals/octagons/octahedron/polyhedra can be used as the set of
halfspaces. However, selecting an overly expressive set of halfspaces may cause
the problem of overfitting [24] and result in poor performance. Therefore, apply-
ing heuristics that adjusts the expressiveness of halfspaces based on the current
examples may improve the performance of our tool.

Acknowledgement. We thank Andrea Peruffo and the anonymous referees for
many suggestions. This work was supported by JST ERATO HASUO Meta-
mathematics for Systems Design Project (No. JPMJER1603) and JSPS KAK-
ENHI Grant Numbers 20H04162, 20H05703, 19H04084, and 17H01720.

References
 1. llvm2KITTeL. https://github.com/hkhlaaf/llvm2kittel
22

 2. StarExec. https://www.starexec.org
 3. T2 temporal logic prover. https://github.com/mmjb/T2
 4. Termination Competition 2020: C Integer. https://termcomp.github.io/Y2020/
    job 41519.html
 5. Alias, C., Darte, A., Feautrier, P., Gonnord, L.: Multi-dimensional rankings, pro-
    gram termination, and complexity bounds of flowchart programs. In: SAS ’10. pp.
    117–133. Springer (2010)
 6. Ben-Amram, A.M., Doménech, J.J., Genaim, S.: Multiphase-linear ranking func-
    tions and their relation to recurrent sets. In: SAS ’19. pp. 459–480. Springer (2019)
 7. Ben-Amram, A.M., Genaim, S.: Ranking functions for linear-constraint loops.
    Journal of the ACM 61(4) (Jul 2014)
 8. Ben-Amram, A.M., Genaim, S.: On multiphase-linear ranking functions. In: CAV
    ’17. pp. 601–620. Springer (2017)
 9. Bjørner, N., Gurfinkel, A., McMillan, K.L., Rybalchenko, A.: Horn clause solvers
    for program verification. In: Fields of Logic and Computation II: Essays Dedicated
    to Yuri Gurevich on the Occasion of His 75th Birthday. LNCS, vol. 9300, pp. 24–51.
    Springer (2015)
10. Brockschmidt, M., Ströder, T., Otto, C., Giesl, J.: Automated detection of non-
    termination and NullPointerExceptions for Java bytecode. In: FoVeOOS ’11.
    LNCS, vol. 7421, pp. 123–141. Springer (2012)
11. Chakarov, A., Sankaranarayanan, S.: Probabilistic Program Analysis with Mar-
    tingales. In: Hutchison, D., Kanade, T., Kittler, J., Kleinberg, J.M., Mattern, F.,
    Mitchell, J.C., Naor, M., Nierstrasz, O., Pandu Rangan, C., Steffen, B., Sudan,
    M., Terzopoulos, D., Tygar, D., Vardi, M.Y., Weikum, G., Sharygina, N., Veith,
    H. (eds.) Computer Aided Verification, vol. 8044, pp. 511–526. Springer Berlin Hei-
    delberg, Berlin, Heidelberg (2013). https://doi.org/10.1007/978-3-642-39799-8 34
12. Champion, A., Chiba, T., Kobayashi, N., Sato, R.: ICE-based refinement type
    discovery for higher-order functional programs. In: TACAS ’18. LNCS, vol. 10805,
    pp. 365–384. Springer (2018)
13. Emmes, F., Enger, T., Giesl, J.: Proving non-looping non-termination automati-
    cally. In: IJCAR ’12. LNCS, vol. 7364, pp. 225–240. Springer (2012)
14. Ezudheen, P., Neider, D., D’Souza, D., Garg, P., Madhusudan, P.: Horn-ICE learn-
    ing for synthesizing invariants and contracts. Proceedings of the ACM on Program-
    ming Languages 2(OOPSLA), 131:1–131:25 (Oct 2018)
15. Fedyukovich, G., Zhang, Y., Gupta, A.: Syntax-guided termination analysis. In:
    CAV ’18. LNCS, vol. 10981, pp. 124–143. Springer (2018)
16. Floyd, R.W.: Assigning meanings to programs. Proceedings of Symposium on Ap-
    plied Mathematics 19, 19–32 (1967)
17. Garg, P., Löding, C., Madhusudan, P., Neider, D.: ICE: A robust framework for
    learning invariants. In: CAV ’14. pp. 69–87. Springer (2014)
18. Garg, P., Neider, D., Madhusudan, P., Roth, D.: Learning invariants using decision
    trees and implication counterexamples. In: POPL ’16. pp. 499–512. ACM (2016)
19. Gonnord, L., Monniaux, D., Radanne, G.: Synthesis of ranking functions using
    extremal counterexamples. In: PLDI ’15. pp. 608–618. ACM (2015)
20. Gupta, A., Henzinger, T.A., Majumdar, R., Rybalchenko, A., Xu, R.G.: Proving
    non-termination. In: POPL ’08. pp. 147–158. ACM (2008)
21. Heizmann, M., Hoenicke, J., Podelski, A.: Termination analysis by learning termi-
    nating programs. In: CAV ’14. pp. 797–813. Springer (2014)
22. Krishna, S., Puhrsch, C., Wies, T.: Learning invariants using decision trees. CoRR
    abs/1501.04725 (2015), http://arxiv.org/abs/1501.04725
                                                                                     23

23. Leike, J., Heizmann, M.: Ranking templates for linear loops. In: TACAS ’14. LNCS,
    vol. 8413, pp. 172–186. Springer (2014)
24. Padhi, S., Millstein, T.D., Nori, A.V., Sharma, R.: Overfitting in synthesis: Theory
    and practice. In: CAV ’19. LNCS, vol. 11561, pp. 315–334. Springer (2019)
25. Padhi, S., Sharma, R., Millstein, T.D.: Data-driven precondition inference with
    learned features. In: PLDI ’16. pp. 42–56 (2016)
26. Podelski, A., Rybalchenko, A.: A complete method for the synthesis of linear rank-
    ing functions. In: VMCAI ’04. LNCS, vol. 2937, pp. 239–251. Springer (2004)
27. Satake, Y., Unno, H., Yanagi, H.: Probabilistic inference for predicate constraint
    satisfaction. In: Proceedings of AAAI 2020 (2020)
28. Solar-Lezama, A., Tancau, L., Bodik, R., Seshia, S., Saraswat, V.: Combinatorial
    sketching for finite programs. In: ASPLOS XII. pp. 404–415. ACM (2006)
29. Unno, H., Satake, Y., Terauchi, T., Koskinen, E.: Program verification via predicate
    constraint satisfiability modulo theories. CoRR abs/2007.03656 (2020), https:
    //arxiv.org/abs/2007.03656
30. Unno, H., Terauchi, T., Koskinen, E.: Constraint-based relational verification. In:
    CAV ’21. Springer (2021)
31. Urban, C.: The abstract domain of segmented ranking functions. In: SAS ’13.
    LNCS, vol. 7935, pp. 43–62. Springer (2013)
32. Urban, C., Gurfinkel, A., Kahsai, T.: Synthesizing ranking functions from bits and
    pieces. In: TACAS ’16. p. 54–70. Springer (2016)
33. Urban, C., Miné, A.: An abstract domain to infer ordinal-valued ranking functions.
    In: ESOP ’14. pp. 412–431. Springer (2014)
34. Urban, C., Miné, A.: A decision tree abstract domain for proving conditional ter-
    mination. In: SAS ’14. pp. 302–318. Springer (2014)
35. Zhu, H., Magill, S., Jagannathan, S.: A data-driven CHC solver. In: PLDI ’18. pp.
    707–721. ACM (2018)
24


                                         int main () {
     int main () {                         int i = ?;
       int x = ?;                          int range = 20;
       int y = 2;                          while (0 <= i && i <= range ) {
       int res = 1;                          if (!(0 == i && i == range )) {
       if ( x < 0 || y < 1) { }                if ( i == range ) {
       else {                                     i = 0;
         while ( x > y ) {                        range = range -1;
            y = y*y;                           } else {
            res = 2* res ;                        i = i +1;
         }                                     }
       }                                     }
     }                                     }
                                         }

     (a) A benchmark containing a nonlin-
     ear operation.                       (b) A benchmark that requires a long
                                          lasso to prove non-termination

                         Fig. 8: Some of the benchmarks


A     Detailed Discussion of The Experiment

We show some of the benchmarks from Termination Competition 2020 that are
solved by MuVal but not by AProVE, Ultimate Automizer, and iRank-
Finder. We also discuss the strength of our method.

A benchmark containing a nonlinear operation. Fig. 8a shows one of the bench-
marks that contains a nonlinear operation y = y * y but admits a linear ranking
function. Although handling nonlinear operation is difficult in general, MuVal
was able to verify termination. The reason can be understood as follows. (1) Our
validator can find transition examples for this benchmark thanks to the recent
development of SMT solvers. (2) Our synthesizer can work as usual because it
is example-based.

A benchmark that requires a long lasso-shaped non-terminating trace to prove
non-termination. Fig. 8b is a benchmark that is non-terminating. To prove non-
termination of this benchmark, we need to find a long lasso-shaped trace that
ends in the self loop when i = range = 0. Finding such a long lasso is difficult
in general, but MuVal was able to find one in this benchmark: during CEGIS
iterations, MuVal found the self loop (i.e. explicit cycle) and then collected
transition examples that were needed to prove reachability of cycles.
    Our method can naturally collect transition examples “backward” from the
self loop (an explicit cycle). At the same time, our method collects transition
examples “forward” from an initial state (in the benchmark of Fig. 8b, the pair
of i = 10 and range = 20 is an initial state of the while loop). When transition
examples that are collected backward and forward form a trace to the self loop,
our method notice that the benchmark is non-terminating.
