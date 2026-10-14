                                        Incorporating Data Dependencies and Properties
                                            in Difference Verification with Conditions
                                                        (Technical Report)

                                                       Marie-Christine Jakobs1,2       and Tim Pollandt1
                                              1
                                                  Technical University of Darmstadt, Department of Computer Science
arXiv:2309.01585v1 [cs.LO] 4 Sep 2023




                                                                           2
                                                                             LMU Munich



                                              Abstract. Software changes frequently. To efficiently deal with such fre-
                                              quent changes, software verification tools must be incremental. Most of
                                              today’s approaches for incremental verification consider one specific veri-
                                              fication approach. One exception is difference verification with conditions
                                              recently proposed by Beyer et al. Its underlying idea is to determine an
                                              overapproximation of those modified execution paths that may cause a
                                              new property violation, which does not exist in the unchanged program,
                                              encode the determined paths into a condition, and use the condition to
                                              restrict the verification to the analysis of those determined paths. To de-
                                              termine the overapproximation, Beyer et al. propose a syntax-based dif-
                                              ference detector that adds any syntactical path of the modified program
                                              that does not exist in the original program into the overapproximation.
                                              This paper provides a second difference detector diffDP, which computes
                                              a more precise overapproximation by taking data dependencies and pro-
                                              gram properties into account when determining the overapproximation of
                                              those modified execution paths that may cause a new property violation.
                                              Our evaluation indeed shows that our more precise difference detector
                                              improves the effectiveness and efficiency of difference verification with
                                              condition on several tasks.

                                              Keywords: Incremental verification · Regression verification · Differ-
                                              ence verification · Conditional model checking · Software verification.


                                        1   Introduction
                                        Software is omnipresent and in many cases we expect it to work reliably. Mean-
                                        while, bug fixes, change requests, or the addition of new features, etc. cause
                                        frequent software changes and each of these changes may introduce new bugs
                                        and, thus, may lower the software’s reliability. One countermeasure for this is
                                        to use software verification [13,24] to prove the absence or detect the existence
                                        of software bugs. Performing the verification on the complete modified program
                                        after each change is typically too costly, but often also not necessary because a
                                        modification rarely has the potential to introduce new bugs in all parts of the
                                        software. This observation is leveraged by many incremental software verification
                                        techniques, which aim to speed up the reverification of modified software. For
2         M.-C. Jakobs, T. Pollandt

 modified program P ′

        Difference   DG(P,P’)   Condition    condition
                                                         Conditional Verifier
        Detector                Generator
    Difference Condition Extractor                             residual
                                                     Reducer   program    Verifier
    original program P                         Reducer-based Conditional Verifier [7]

                      Fig. 1: Construction of a difference verifier


example, there exist techniques that update previously computed state space
descriptions [2,39,35,18,27,38], reuse intermediate results [42,1,9,36,16,46,20], or
skip the analysis of unchanged behavior [43,34,37,44,29,12,28,6]. However, most
approaches are tailored to and coupled with one specific verification approach.
    Recently, Beyer et al. suggested difference verification with conditions [6], an
incremental verification approach agnostic to the verifier. Difference verification
with conditions allows one to build a difference verifier (see Fig. 1) from an ar-
bitrary (conditional) verifier3 and let the difference verifier explore that part of
the state space that may contain new bugs introduced by the software modifica-
tion. The respective difference verifier first runs a difference condition extractor.
The difference condition extractor detects an overapproximation of all execution
paths of the modified program that may cause a regression bug, i.e., execution
paths that may violate the property and that are triggered by inputs that may
not cause a property violation in the original program, and then encodes the
detected paths into a condition, an automata-based exchange format used in
conditional model checking [5]. In a second step, the difference verifier feeds the
condition and the modified program into its conditional verifier to restrict the
verification to those paths of the modified program that were determined and
encoded into the condition by the extractor in the previous step.
    In their proof-of-concept, Beyer et al. used a syntax-based difference condi-
tion extractor [6] that determines exactly those syntactic paths of the modified
program that syntactically changed, i.e., all syntactic paths that do not occur in
the original program. The overapproximation computed by their syntax-based
difference condition extractor is rather coarse. For instance, consider the modi-
fication of the program in Fig. 2. The modification deletes the minus sign in the
first statement (shown in red) to fix a bug in the computation of the negated
absolute value of x. Despite the modification, due to a missing data dependency
between the change and the property (i.e., the assertion), the property is not
affected. To take this into account, this paper introduces a new, more complex
difference condition extractor. The paper proves the soundness of the new dif-
ference condition extractor and experimentally applies it in various difference

3
    We can use the reducer-based approach [7] to conditional model checking to turn an
    arbitrary verifier into a condiitonal verifier.
    Incorporating Data Dependencies and Properties in Difference Verification             3


                                 ℓ0                              ℓ′0
r =-x ;                     r=-x;                            r=x;
                                    x>0                              x>0 ′
if (x >0) {                      ℓ1     ℓ2                       ℓ′1     ℓ2
    r=-x;                  !(x>0)         r=-x;            !(x>0)           r=-x;
    assert (r <=0);              ℓ4     ℓ3      ℓerr             ℓ′4     ℓ′3      ℓ′err
}
                                    r<=0;    !(r<=0)                 r<=0;   !(r<=0)
Fig. 2: Program code of original program (left) as well as the CFA of original pro-
gram (middle) and modified program (right). The modified program is derived
from the original program by deleting the underlined parts in red.

verifiers, which are compared to verification without the difference extractor
and difference verification with the syntax-based extractor.
    This technical report is an extension of our conference paper [21] and en-
hances our conference paper with the soundness proofs. To be self-contained,
the technical report presents all contributions of the conference paper [21].


2    Foundations of Difference Verification with Conditions

We present difference verification with conditions in the context of an imperative
programming language that operates on assume operations and assignments. We
assume that a set Ops contains all these operations. Furthermore, we restrict our
properties to the unreachability of certain program locations. Note that our im-
plementation supports C programs and many safety properties can be encoded
by the unreachability of an error location. Formally, we represent programs in-
cluding their properties by control-flow automata.
Definition 1. A control-flow automaton (CFA) P = (L, ℓ0 , G, ℓerr ) consists of

 – a set L of program locations with initial location ℓ0 ∈ L and error location
   ℓerr ∈ L, which when reached reflects a property violation, and
 – a set G ⊆ L × Ops × L of control-flow edges.

P is deterministic if for all control-flow edges (ℓ, op1 , ℓ1 ), (ℓ, op2 , ℓ2 ) ∈ G either
op1 = op2 and ℓ1 = ℓ2 , or op1 and op2 are assume operations with op1 ≡ ¬op2 .
For the explanation throughout the paper, we use the original and modified pro-
gram shown Figure 2. On the left of the figure, we show the code of our original
program, which should compute the negated absolute value −|x| of variable x.
However, the red, underlined minus sign in the first statement causes a bug and
is removed in the modified program, whose CFA is shown on the right of Fig. 2.
The middle of Fig. 2 presents the CFA of the original, which only differs from
the CFA of modified program in the first edge (highlighted in red and blue).
Both CFAs use one edge per assignment and two edges for the condition in the
if statement as well the assertion, namely one per condition evaluation. In ad-
dition any violation of the assertion leads to the error location represented by
double circles.
4         M.-C. Jakobs, T. Pollandt

     CFAs define the program syntax. The semantics of a CFA P = (L, ℓ0 , G, ℓerr )
is defined by a standard operational semantics. Therefore, we represent a pro-
gram state as as pair of a program location ℓ ∈ L and a concrete data state c
that assigns to each variable a concrete value. Based on the notion of pro-
gram states, we define the executable program paths. An executable program
                     g1              g2    gn
path π = (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓn , cn ) always begins in the initial loca-
tion ℓ0 and an arbitrary concrete data state. Thereafter, it executes n transition
steps with n ≥ 0. Thereby, it ensures that each of the n transition steps i,
i.e., 1 ≤ i ≤ n, respects the control-flow, i.e., gi = (ℓi−1 , ·, ℓi ), and that it ad-
heres to the operation semantics, i.e., (a) for of assume operations, ci−1 |= opi
and ci−1 = ci and (b) for assignments, ci = SPopi (ci−1 ), where SP denotes
the strongest-post operator of the semantics. Next to semantics, we define the
set wrt(op) that contains the variables written by an operation, i.e., the variables
whose value may be changed by operation op. Similarly, we define the set rd(op)
that contains all variables necessary to execute the operation op, i.e., if two data
states c, c′ agree on the values of the variables in rd(op), then for assume opera-
tions c |= op ⇔ c′ |= op and for assignments, SPop (c) and SPop (c′ ) agree on the
values of the variables in wrt(op).
     Based on the notion of execution paths, we now charachterize those paths
violate the program’s property. A path violates the program’s property when-
ever it reaches the error location, i.e., ∃0 ≤ i ≤ n : ℓi = ℓerr . We write
pathserr (P ) to denote the set of all execution paths of program P that violate
a property and use it to characterize all execution paths of a modified pro-
gram P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) that cause a regression bug. More concretely, these
are all paths from pathserr (P ′ ) whose initial concrete data state c′0 does not
trigger a property violation in the the original program P = (L, ℓ0 , G, ℓerr ). For-
                                 g′           g′     g′
mally, a path π ′ = (ℓ′0 , c′0 ) →
                                 1
                                   (ℓ′1 , c′1 ) →
                                                2     n
                                                  ... → (ℓ′n , c′n ) ∈ pathserr (P ′ ) causes a
                                                                        g1            g2     gm
regression bug if there does not exist a path π = (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . →
(ℓm , cm ) ∈ pathserr (P ) with c′0 = c0 . We use the set pathsrb (P, P ′ ) to describe
all paths with regression bugs.
    In most cases, one fails to precisely compute the paths with regression bugs.
Thus, one needs to compute an overapproximation of it and then analyze the
paths in the overapproximation. To analyze the paths in the overapproxima-
tion, difference verification with conditions applies the idea of conditional model
checking (CMC) [5,7]. CMC steers a conditional verifier (see right of Fig. 1) with
a condition to restrict the verification to the subset of the program paths that
are not covered by the condition. Following CMC [5,7], we represent a condition
by an automaton and use accepting states to identify covered paths.
Definition 2. A condition A = (Q, δ, q0 , F ) consists of
    – a finite set Q of states including the initial state q0 ∈ Q and a set F ⊆ Q of
      accepting states and
    – a transition relation δ ⊆ Q × G × Q4 ensuring ∀(q, op, q ′ ) ∈ δ : q ∈
                                                                           /F.
4
    In general [5,7], the transition relation of a condition also specifies assumptions on the
    program states, which we omit because they are irrelevant in difference verification.
   Incorporating Data Dependencies and Properties in Difference Verification                 5

As already mentioned, CMC analyzes at least all paths that are not covered by
the condition. Formally, a condition covers a path if the condition accepts any
prefix of the path.
Definition 3. A condition A = (Q, δ, q0 , F ) covers an executable program path
               g1           g2      gn
π = (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓn , cn ), i.e., π ∈ cover(A), if there exists a run
       g1       g2     gk
ρ = q0 → q1 → . . . → qk , 0 ≤ k ≤ n, in A, s.t. qk ∈ F .
In difference verification with conditions, the difference verifier (see Fig. 1) first
uses a difference condition extractor that generates an appropriate condition,
which must not accept any path from pathsrb (P, P ′ ), and then applies CMC. We
consider difference condition extractors that follow the procedure of the existing
syntax-based extractor [6] and, thus, generate the condition in two steps.
    In the first step, a difference detector analyzes the modified program together
with the original program to determine an overapproximation of pathsrb (P, P ′ ).
The resulting overapproximation is described by a difference graph DG(P, P ′ ).
Paths in the difference graph refer to program paths of the modified program.
In particular, paths in the difference graph that reach nodes from a set ∆ of
regression bug indicator nodes characterize program paths that should be ana-
lyzed because they may cause regression bugs (like paths in pathsrb (P, P ′ )). To
ensure this relation and to avoid that paths in the difference graph are misclassi-
fied after reaching a node from ∆, a difference graph DG(P, P ′ ) guarantees that
all of its paths p that relate to (a prefix of) a path with a regression bug must
be extendable to a path p′ in the difference graph that ends in a node from ∆.
Formally, we model difference graphs DG(P, P ′ ) as follows.
Definition 4. A DG(P, P ′ ) = (N, E, n0 , ∆) for original CFA P = (L, ℓ0 , G, ℓerr )
and modified CFA P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) consists of
 – a set N of nodes including the initial node n0 ∈ N as well as the set ∆ ⊆ N
   of regression bug indicator nodes,
 – and edges E ⊆ N × G′ × N . It must ensure the soundness property
                        g′           g′      g′
       ∀π ′ = (ℓ′0 , c′0 ) →
                           1
                             (ℓ′1 , c′1 ) →
                                          2     n
                                            ... → (ℓ′n , c′n ) ∈ pathsrb (P, P ′ ), 0≤k≤n,
         g′      g′     g′                              ·       ·
         1
      n0 →    2
           n1 →     k
                ... → nk ∈ DG(P, P ′ ) : ∃nk → . . . → nk+m : nk+m ∈ ∆ .

   In the second step of the difference condition extractor, the condition gener-
ator converts the difference graph resulting from the first step into a condition.
Algorithm 1 performs that conversion. To this end, it generates a condition that
accepts a path as soon as a prefix has been seen for which it knows that any
extension of a path in the difference graph that is related to the prefix cannot
reach a node from ∆, i.e., due to the assumption on a difference graph the prefix
cannot be extended to a path from pathsrb (P, P ′ ). Due to the requirements on
the difference graph, the relevant paths in the difference graph start in n0 , end in
a node that cannot reach a node from ∆, and all other nodes on the paths may
reach a node from ∆. Using these insights, Alg. 1 performs a backward search
from ∆ to the initial node n0 (lines 1–5) to detect the non-accepting condition
6        M.-C. Jakobs, T. Pollandt

Algorithm 1 Condition generator extracting condition from difference graph
Input: difference graph DG(P,P’) = (N, E, n0 , ∆)
Output: extracted condition
 1: Q = {n0 } ∪ ∆; waitlist = {n0 } ∪ ∆;
 2: while (waitlist ̸= ∅) do
 3:   pop ns from waitlist
 4:   for each (np , (ℓ, op, ℓ′ ), ns ) ∈ E with np ∈
                                                    / Q do
 5:     Q = Q ∪ {np }; waitlist = waitlist ∪ {np };
 6: F = {ns | ∃(np , g, ns ) ∈ E ∧ np ∈ Q ∧ ns ∈   / Q};
 7: return (Q ∪ F, E ∩ (Q × G′ × (Q ∪ F )), n0 , F );



states (intermediate nodes of the paths, which may reach a node from ∆). Then,
it adds the accepting states (line 6), the end nodes of these paths, and copies all
edges of the difference graph induced by the accepting and non-accepting states.
    Next we show that difference condition extractors based on the above pro-
cess and requirements, generate appropriate conditions and, thus, ensure that
difference verifiers using them analyze all paths with regression bugs. Therefore,
we need to show that the generated condition A does not accept paths causing
regression bugs, i.e., cover(A) ∩ pathsrb (P, P ′ ) = ∅.

Theorem 1. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be two CFAs.
Difference condition extractors that sequentially compose a difference detector
with Alg. 1 compute conditions A that do not cover paths that cause regression
bugs, i.e., cover(A) ∩ pathsrb (P, P ′ ) = ∅.

Proof. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be arbitrary CFAs,
DG(P, P ′ ) a difference graph computed by an arbitrary difference detector, and
A = (Q, δ, q0 , F ) the condition computed by Alg. 1 for input DG(P, P ′ ). Con-
                                       g′           g′       g′
sider arbitrary path π ′ = (ℓ′0 , c′0 ) →
                                        1
                                          (ℓ′1 , c′1 ) →
                                                       2     n
                                                         ... → (ℓ′n , c′n ) ∈ cover(A). By
                                            1 g′ 2     kg′       g′
definition of coverage, there exists ρ = q0 → q1 → ... → qk , 0 ≤ k ≤ n, in A, such
                                                                             1         g′
that qk ∈ F . Due to the construction of A in Alg. 1, there exists a path n0 →
    g′    g′                                        ·        ·
n1 →2     k
      ... → nk ∈ DG(P, P ′ ) such that ¬∃nk → . . . → nk+m : nk+m ∈ ∆ (other-
wise nk would have been added to Q in lines 1–5 and, thus, not to F in line 6).
Due to the soundness property of the difference graph, π ′ ∈
                                                           / pathsrb (P, P ′ ). ⊔
                                                                                ⊓

Beyer et al. [6] use the two step process from above to define a syntax-based
difference condition extractor diffCond. Their difference detector explores orig-
inal and modified program in synch and stops exploration in a node from ∆ as
soon as a syntactical difference between original and modified program occurs
on the path. In the following section, we describe a second difference detector,
which goes beyond syntactical differences and takes data dependencies and error
locations into account.
    Incorporating Data Dependencies and Properties in Difference Verification              7

3     Difference Detector diffDP

The crucial point to make difference verification with conditions efficient is to let
the verifier explore a (small) subset of the program paths. Since for soundness the
verifier needs to explore at least all paths with regression bugs pathsrb (P, P ′ ), it
is crucial that the difference detector, which is responsible for determining the
subset of programs to be explored, computes a (small) overapproximation of the
paths with regression bugs. In this section, we present a new difference detec-
tor diffDP that takes data dependencies and program properties to compute
a more precise overapproximation of pathsrb (P, P ′ ) than the existing, syntax-
based difference detector [6].
    While the set of all execution paths of the modified program is a proper
overapproximation of pathsrb (P, P ′ ), difference detectors aim to be more precise
and remove program paths that do not violate a property or for which they
can determine that the violation already exists in the original program, i.e., it
is not a path with a regression bug. To determine that a path π ′ violating the
property is not a path with a regression bug, one needs to ensure the existence
of what we call a witness path, namely a path of the original program that starts
with the same input as π ′ and also violates a property. The existing syntax-based
difference detector [6] only considers witness paths that are identical to π ′ except
for location naming. The difference detector diffDP presented in this section
takes additional witness paths into account. In general, it considers witness paths
that have a similar branching structure as π ′ , i.e., execute a similar sequence of
assume operations, and violate properties no later than π ′ .5
    Since the number of execution paths is at least large and may be even infinite,
we cannot detect witnesses per execution path. Instead diffDP groups execution
paths following the same syntactic path and considers all paths of a group at
once. More concretely, for each syntactical path p′ of the modified program
diffDP tries to detect a syntactic (witness) path p in the original program that
(1) has a similar branching structure, that (2) is executable whenever p′ is
executable (thus, ensuring executability of path p for all inputs of interest), and
(3) in which an error location does not occur later than in p. For example when
                                             r=x;       x>0      r=−x;      !(r<=0)
considering the syntactic path p′ := ℓ′0 −−−→ ℓ′1 −−−→ ℓ′2 −−−−→ ℓ′3 −−−−−→ ℓ′err of
our modified program in Fig. 2, difference detector diffDP detects the syntactic
                          r=−x;       x>0       r=−x;         !(r<=0)
witness path p := ℓ0 −−−−→ ℓ1 −−−→ ℓ2 −−−−→ ℓ3 −−−−−→ ℓerr . Note that p is
executable whenever p′ is executable because the changes (first assignment) do
not affect the assume statements on the paths.
    Algorithm 2 shows how our difference detector diffDP works. It gets the
original program P and the modified program P ′ as inputs. We assume that
both programs are given as deterministic CFAs. When Alg. 2 finishes, it outputs
its computed overapproximation of pathsrb (P, P ′ ) as a difference graph. The
returned difference graph provides a witness path for each execution path of the
modified program that is not contained in the overapproximation.
5
    All identical witness paths also fulfill the criterion of a similar branching structure.
8        M.-C. Jakobs, T. Pollandt

Algorithm 2 Difference detector diffDP (P, P ′ )
Input: deterministic CFAs P = (L, ℓ0 , G, ℓerr ), P ′ = (L′ , ℓ′0 , G′ , ℓ′err )
Output: difference graph DG(P, P ′ )
 1: waitlist := {(ℓ0 , ℓ′0 )}; N≀ := {(ℓ0 , ℓ′0 )}; E≀ := ∅; ∆ := ∅; Vδ := λ((ℓ1 , ℓ′1 )).∅;
 2: while waitlist ̸= ∅ do
 3:    pop (ℓ1 , ℓ′1 ) from waitlist
 4:    for each g ′ = (ℓ′1 , op′ , ℓ′2 ) ∈ G′ do
 5:       if op′ is assignment then
 6:          if ∃(ℓ1 , op′ , ℓ2 ) ∈ G then
 7:             if Vδ ((ℓ1 , ℓ′1 )) ∩ rd(op′ ) ̸= ∅ then Vdiff := Vδ ((ℓ1 , ℓ′1 )) ∪ wrt(op′ );
 8:             else Vdiff := Vδ ((ℓ1 , ℓ′1 )) \ wrt(op′ );
 9:             process(((ℓ1 , ℓ′1 ), g ′ , (ℓ2 , ℓ′2 )), Vdiff )
10:          else process(((ℓ1 , ℓ′1 ), g ′ , (ℓ1 , ℓ′2 )), Vδ ((ℓ1 , ℓ′1 )) ∪ wrt(op′ ))
11:       else // op′ assume
12:          ℓp := ℓ1 ; Vdiff := Vδ ((ℓ1 , ℓ′1 ));
13:          while ℓp ̸= ℓerr ∧ ∃(ℓp , opa , ℓs ) ∈ G : opa is assignment do
14:             ℓp := ℓs ; Vdiff := Vdiff ∪ wrt(opa );
15:          if ℓp ̸= ℓerr ∧ (∃(ℓp , op, ℓ2 ) ∈ G : op = op′ ∨ ((op′ ⇒ op) ∧ op′ ̸≡ f alse)) then
16:             if Vdiff ∩ (rd(op) ∪ rd(op′ )) ̸= ∅ then process(((ℓ1 , ℓ′1 ), g ′ , ℓ′2 ), ∅)
17:             else process(((ℓ1 , ℓ′1 ), g ′ , (ℓ2 , ℓ′2 )), Vdiff )
18:          else process(((ℓ1 , ℓ′1 ), g ′ , (ℓp , ℓ′2 )), Vdiff )
19: if ℓ′0 ∈ ∆ ∨ (ℓ′0 = ℓ′err ∧ ℓ0 ̸= ℓerr ) then return ({ℓ′0 }, ∅, ℓ′0 , {ℓ′0 })
20: E :={(n, g ′ , n′ ) ∈ N≀ ×G′ ×(N≀ ∪∆) | (n, g, n′ ) ∈ E≀ ∨(n′ ∈ ∆∧∃(n, g, (·, n′ )) ∈ E≀ )};
21: return (N≀ ∪ ∆, E, (ℓ0 , ℓ′0 ), ∆)

22: process((pred, g ′ , succ), Vdiff )
23: if succ ∈ L′ then
24:    ∆ := ∆ ∪ {succ}; E≀ := E≀ ∪ {(pred, g ′ , succ)};
25:    N≀ := N≀ \ {(·, succ) ∈ N≀ }; waitlist := waitlist \ {(·, succ) ∈ waitlist};
26: else
27:    if succ ∈ (L \ {ℓerr }) × {ℓ′err } then process((pred, g ′ , ℓ′err ), ∅)
28:    else
29:       if succ ∈/ L × ∆ ∧ succ ∈  / {ℓerr } × L′ ∧ (succ ∈
                                                            / N≀ ∨ Vdiff ̸⊆ Vδ (succ)) then
30:          waitlist := waitlist ∪ {succ};
31:       if succ ∈/ L × ∆ then
32:          N≀ := N≀ ∪ {succ}; Vδ (succ) := Vδ (succ) ∪ Vdiff ;
33:       E≀ := E≀ ∪ {(pred, g ′ , succ)};




    The outer while loop of Alg. 2 represents the algorithm’s main part, which
detects and simultaneously records witness paths p. To this end, Alg. 2 it per-
forms a step-by-step exploration of the paths of the modified program. The
step-by-step exploration also aims to align the paths to witness paths of the
original program. Thereby, it uses pairs (ℓ, ℓ′ ) ∈ L × L′ of program locations
as alignment points that describe where p and p′ align. Algorithm 2 stores the
detected alignment points in N≀ and their connection in E≀ . Furthermore, it uses
  Incorporating Data Dependencies and Properties in Difference Verification        9

data structure waitlist to keep track of which alignment points need to be ex-
plored and, thus, organizes the path exploration. If a witness path p aligned to
a prefix of a path p′ of the modified program cannot be extended to that step
of path p′ that follows after the prefix, i.e., no witness path can be constructed
for p′ , Alg. 2 stops the exploration of p′ and stores its next location in ∆. The
set ∆ represents the set of regression bug indicator nodes of the difference graph,
which characterize paths of the overapproximation. To detect (dis)agreements
on executability between paths and witness path extensions, data structure Vδ
tracks for all aligned locations (ℓ, ℓ′ ) the change affected variables, i.e., those
variables which may have different values at alignment point (ℓ, ℓ′ ).
    When the detection and recording of witness paths has finished, lines 19–
21 of Alg. 2 build the difference graph. The algorithm distinguishes two cases.
First, if ℓ′0 is contained in ∆ or ℓ′0 is a new error location, no witness paths were
detected because the alignment of the initial locations already failed. Hence, all
execution paths of the modified program may cause regression bugs. Therefore,
the difference graph returned in line 19 consists of a single regression bug in-
dicator node. Second, we consider all other cases, in which Alg. 2 computed at
least some witness paths. To encode the witness paths into a difference graph,
Alg. 2 uses the data structures N≀ , ∆ and E≀ , in which it records for each syn-
tactic path either the information about its witness path or that no witness
path has been detected. During the construction of the difference graph, Alg. 2
basically copies the information of paths with and without witness paths into
the difference graph. Hence, set ∆ becomes the regression bug indicator nodes.
The graph’s nodes are the union of the determined aligned locations N≀ and the
regression bug indicator nodes ∆. The graph edges are derived from the connec-
tion between determined aligned locations and regression bug indicator nodes,
thereby considering that aligned locations may be replaced by regression bug
indicator nodes, which are not explored, i.e., they must not have successors.
    Next, let us have a closer look at the path exploration with integrated wit-
ness path alignment. It starts in line 1, aligning the initial location of the two
programs (initial alignment point of any path and its witness path) and with
an empty set of connections (E≀ := ∅;). Also at the initial locations no modifi-
cations have been seen yet, i.e., we have not detected that any path for which
the construction of a witness path failed (∆ := ∅) nor have we obtained knowl-
edge about change affected variables (i.e., Vδ does not track any change affected
variable). Thereafter, each iteration of the outer while loop explores one aligned
pair (ℓ1 , ℓ′1 ) that has not yet been explored or whose change affected variables
altered. Thereby, it computes one successor per outgoing CFA edge g ′ in the
modified program. The successor and the update of its change affected variables
depend on g ′ ’s operation.
    In case of an assignment (lines 5–10), we ignore executability (assignments
are always executable) and only check whether an outgoing edge with an iden-
tical assignment exists in the original program. If an identical edge exists, we
explore in lockstep and update the change affected variables according to the
data dependencies. For example, given aligned pair (ℓ2 , ℓ′2 ) and outgoing CFA
10      M.-C. Jakobs, T. Pollandt

edge (ℓ′2 , r = −x; , ℓ′3 ), Alg. 2 detects the edge (ℓ2 , r = −x; , ℓ3 ) of the original
program, which has an identical assignment, aligns the successors (ℓ3 , ℓ′3 ), and
propagates that variable r is no longer affected by a modification. If no identical
edge exists, we detect a modification. Since it is non-trivial to detect a good
alignment of original and modified program [32], we decided to (a) always han-
dle the modification like a new assignment (i.e., no step in the original program
and all variables wrt(op′ ) become change affected) and (b) if this assumption was
wrong to postpone resynchronization to the beginning of assume operations.6 As
an example for a modification, let us consider the aligned pair (ℓ0 , ℓ′0 ) and cor-
responding outgoing edge (ℓ′0 , r = x; , ℓ′1 ). Algorithm 2 detects the modification
and only steps forward in the modified program, thus, aligns (ℓ0 , ℓ′1 ). Addition-
ally, it propagates that variable r is affected by the modification. In case of a
match as well as a modification, procedure process updates the data structures
based on the suggested alignment and determined change affected variables.
    In case of an assume operation (lines 11–18), we account for the mismatch
of assignments and first perform any postponed synchronization (lines 12–14).
Thereby, we explore all assignments in the original program until we hit the
next assume operation or an error location (i.e., no regression bug possible).
Explored assignments are treated like modifications, i.e., we add their modified
variables to the changed affected variables Vdiff of the alignment. After resyn-
chronization, line 15 checks whether both programs provide matching assume
operations. Assume operations match if they are identical or the original assume
is more general7 . If a matching assume operation is found, we continue with
the executability check (line 16). We can only safely guarantee executability if
the assume operations are affected by the modification. If the matching check
fails, we consider the assume of the modified program as a new operation. Note
that the assume operation may restrict the executability of the modified path
and, thus, the relevant inputs. However, it does not restrict the executability
of the witness path on relevant inputs. Hence, only if matching assumes are
affected by the modification (line 16), we failed to detect a witness path and
stop the alignment. To this end, we let the alignment end in the location of the
modified path, which describes a regression bug indicator node and for which
change affected variables are irrelevant. In all other cases (lines 17 and 18), we
align original and modified program accordingly and since assume operations
do not change the data state, forward the already determined change affected
variables Vdiff . Again, procedure process updates the data structures. As an
example, let us consider aligned pair (ℓ0 , ℓ′1 ), outgoing CFA edge (ℓ′1 , x > 0, ℓ′2 )
and Vδ ((ℓ0 , ℓ′1 )) = {r}. Algorithm 2 first explores the edge (ℓ0 , r = −x; , ℓ1 ) of
the original when performing resynchronizes and thereby adds r to the change
affected variables Vdiff . Then, it finds a matching assume edge (ℓ1 , x > 0, ℓ2 ) in
the original program. Since both assume operation do not consider any change
affected variables (Vdiff = {r}), Alg. 2 aligns (ℓ2 , ℓ′2 ) and propagates Vdiff .

6
  To be more precise, our implementation also keeps the alignment if an assignment
  exists that changes the same variables (left out for simplicity of Alg. 2).
7
  To get deterministic difference graphs for our proofs, op′ must be satisfiable, too.
    Incorporating Data Dependencies and Properties in Difference Verification     11

                      {}               {r}             {r}
                                r=x;             x>0
                    (ℓ0 , ℓ′0 )      (ℓ0 , ℓ′1 )     (ℓ2 , ℓ′2 )
                                 !(x>0)                    r=-x;
                              {r} (ℓ4 , ℓ′4 )    (ℓ3 , ℓ′3 ) (ℓerr , ℓ′err ) {}
                                            r<=0; {} !(r<=0)

    Fig. 3: Difference graph of Alg. 2 for original and modified CFA from Fig. 2


    Lastly, let us have a look at the procedure process, which is responsible for
updating the data structures. To perform the update, it gets the proposed suc-
cessor (edge) and the determined change affected variables. In case the witness
path extension failed (lines 22–24), we stop exploration, add the successor to ∆,
add the successor edge, and remove any aligned locations considering the succes-
sor’s location form N≀ and waitlist. The edges are adapted later in line 19. In case
alignment (extension) has been proposed (lines 26–32), we first need to account
for violations by paths of the modified program. If only the path of the modified
program violates the property, we recursively call process, but now exchanging
the alignment with the location of the modified path, a regression bug indicator
node.8 Otherwise, line 28–29 mark the successor for (re)exploration if we neither
end in a regression bug indicator node (difference already established), nor align
with an error location of the original program (regression bug impossible), nor
the successor and all change affected variables are known (information already
considered for exploration). If we do not end in a regression bug indicator node,
we need to ensure that successor information and the detected change affected
variables are available for exploration and graph construction. Hence, lines 30–31
add them to N≀ and Vδ . Finally, line 32 adds the corresponding edge to E≀ .
    Next, we demonstrate Alg. 2 on our example from Fig. 2. Figure 3 shows
the computed difference graph. Algorithm 2 starts with the pair of initial lo-
cations (ℓ0 , ℓ′0 ) and no change affected variables. Next, it detects the modified
assignment, which is handled as a new statement, and, thus, only moves forward
in the modified program assuming the the assigned variable r to be affected.
Thereafter, Alg. 2 explores the first two assume operations of the modified pro-
gram. For both assume operation, it first performs the resynchronization that
takes the first assignment of the original program into and adds its assigned vari-
able r to the changed affected variables Vdiff = {r}. Then, it detects the identical
assume operations in the original program, which do not consider any changed
affected variables. Hence, Alg. 2 propagates the changed affected variables {r},
and continues exploration. Afterwards, it explores the second assignment of the
modified program. It detects an identical assignment in the original program
and removes r from the change affected variables because r is redefined and no
longer affected. Finally, Alg. 2 explores the assume operations resulting from the

8
    To further exclude non-regression bugs, our implementation first searches for an
    error location of the original program in its follow-up sequence of assignments.
12      M.-C. Jakobs, T. Pollandt

assertion. For both, there exists an identical assume operation in the original
program, which is not affected by the modification. Thus, the assumptions are
explored in lockstep and the change affected variables are forwarded.
    Our goal is to use Alg. 2 as a difference detector for difference detection with
conditions. To keep soundness of difference detection, we hence need to show that
Alg. 2 constructs proper difference graphs. Theorem 2, whose proof is available
in the appendix, claims this.
Theorem 2. Algorithm 2 returns a difference graph.


4     Evaluation

In our evaluation, we aim to compare difference verification with our difference
condition extractor (diffDP plus Alg. 1) against a full verification and against
difference verification with the syntax-based difference condition extractor diff-
Cond from [6] in terms of efficacy (i.e., number of solved verification tasks) and
efficiency (i.e., CPU time).


4.1   Experimental Setup

Verification Tasks. We use two sets of verification tasks in our evaluation: a
set of combination tasks and a set of regression tasks. Each task in any of the two
sets consist of a original and modified program, which both consider the property
that the function reach_error() is never called. Furthermore, at most one of
the two programs in each task may actually call the function reach_error()
and, thus, violate the property. This is important to ensure that verification and
difference verification can only detect regression bugs.
    The set of combination tasks contains the 10 426 tasks already utilized in
Beyer et al.’s evaluation of difference verification with conditions [6] The tasks
of this set are organized in five categories (1) eca05+token, (2) gcd+newton,
(3) pals+eca12, (4) sfifo+token, (5) square+softflt and their programs are
the result of combining two verification tasks.
    The set of regression tasks were derived by Beyer et al. [9] from revisions
of 62 Linux device drivers and used to evaluate their incremental verification
technique. Each program in the task set relates to one revision of a device driver
and examines one of six API usage rules. The rule examination is woven into
the program s.t. a rule violation leads to a call of the function reach_error().
Furthermore, original and modified program examine the same rule and the
modified program stems from the next revision available for which the ground
truth is known Nevertheless, original and modified program typically differ in
several hundred lines. and the ground truth for the modified program is known.
The resulting task set contains 3 936 so-called regression tasks.
    Verifiers. For our experiments, we select two different off-the-shelf verifiers
from the SV-COMP 2022 participants based on the performance of the SV-
COMP 2022 participants in the categories ReachSafety-Combinations and
   Incorporating Data Dependencies and Properties in Difference Verification          13

SoftwareSystems-DeviceDriversLinux64-ReachSafety, the categories clos-
est to our tasks. More concretely, we select the best tool CPAchecker 2.1
and ESBMC, the next best tool that uses a different verification platform.
CPAchecker 2.1 runs a feature-based strategy selection [4] to select the most
suitable combination of sequential analyses. These combination may e.g., ap-
ply bounded, explicit, or predicate model checking or k-induction. ESBMC [14]
applies k-induction enhanced with invariants. We add to these two off-the-shelf
verifiers, which are no conditional verifiers, i.e., their difference verifiers will need
to use reducer-based conditional verifier approach [7], the native conditional
verifier Predicate [5] that combines predicate model checking with adjustable
block-encoding [8], abstracts at loop heads and applies counterexample-guided
abstraction refinement with lazy refinement [17] to compute relevant predicates.
     We use all three verifiers V standalone for full verification, i.e., they verify
the complete modified program, and as verifier component in difference ver-
ifiers. For the difference verifiers, we use reducer-based CMC [7] to combine
every verifier V with the syntax-based difference condition extractor diffCond
              red                                                 red
from [6] (V ∆syn ) and our difference condition extractor (V ∆DP ). Also, we natively
combine the conditional verifier Predicate with the syntax-based extractor diff-
                     nat                                      nat
Cond (Predicate∆syn ) and our extractor (Predicate∆DP ).
     For the two off-the-shelf verifiers, we use their SV-COMP 2022 [3] version,
while for Predicate, the reducer, and the two difference condition extractors
we use the more recent CPAchecker version 40 843, which includes all four
components.
     Computing Environment. We run our experiments on machines with an
Intel Xeon E3-1230 v5 CPU (frequency of 3.4 GHz, 8 processing units) and 33 GB
of memory. All machines run an Ubuntu 20.04 (Linux kernel 5.4.0). Furthermore,
we restrict each verifier runto 4 processing units, 15 min of CPU time, and 15 GB
of memory using BenchExec [10] version 3.11.

4.2   Experimental Results
RQ 1 Is Difference Verification with Our Extractor Better Than a
Complete Verification? The evaluation of Beyer et al. [6] revealed that for
a significant number of tasks difference verification with the syntax-based dif-
ference condition extractor diffCond is more effective or more efficient than
verifying the complete modified program of the task. With our first research
question we want to find out if these results carry over to difference verification
with our new difference condition extractor.
    We start with examining effectiveness. Table 1 shows per task category the
number of correctly proved (✓) and disproved (✗) tasks as well as the number
of incorrectly solved tasks (✓ ) by a verifier and its difference verifier that uses
our difference condition extractor. Note that all incorrectly solved tasks are
false proofs. The total number of tasks with and without property violations in
category are shown at the top of the table.
    When comparing the number of correctly proved tasks (✓), we observe that
for each verifier, there exist categories for which the difference verifier (high-
14      M.-C. Jakobs, T. Pollandt


Table 1: Number of correct proofs (✓), of correct alarms (✗), and of incorrectly
solved tasks (✓ ) detected by each verifier and their related difference verifiers,
which use our difference condition extractor
                          eca05+token      gcd+newton      pals+eca12      sfifo+token    square+softflt   regression
                          (2 340+1 300)    (1 352+572)    (1 700+1 050)   (1 206+663)       (165+75)       (3 936+0)
                          ✓      ✗    ✓   ✓     ✗   ✓   ✓     ✗    ✓   ✓      ✗   ✓    ✓     ✗ ✓      ✓     ✗ ✓
 Predicate                 912 1040 0  0 520 0   0              50      0 558 507 0 22 51              0 2595 0 0
             nat
 Predicate∆DP            1400 985 0 156 520 0 125               75      0 594 488 0 115 75             0 2663 0 0
         ∆red
 PredicateDP              1390 955 0 156 572 0 125              50      0 639 456 0 135 60             0 2685 0 0
 CPAchecker               633 1296 0    0 494 0   0 100                 0 434 510 0   0 75             0 3931 0 0
                   red
 CPAchecker∆DP 1119            1252 0 156 520 0 671 500                 0 480 638 0 117 60             0 3618 0 0
 ESBMC                        0 1125 0 570 572 0 198 530 0   0 663 0 165 75                            0       0 0 0
         red
 ESBMC∆DP                     0 900 0 880 572 0    0 70 10 101 618 0 156 75                            0       0 0 0




lighted in yellow) has a higher number, i.e., correctly proves more tasks. Often
there, also exist categories in which the difference verifier correctly finds more
property violations (✗). In some cases, the difference verifier succeeds while
the full verification runs out of resources. In other cases, difference verifica-
tion excludes paths with program features not supported by the underlying
verifier. In summary, difference verification with our difference condition ex-
tractor can be more effective than a full verification but it does not dominate
the full verification. For Predicate and CPAchecker our difference verification
approach is rarely less and often more effective. However, for ESBMC the differ-
ence verifier only performs better in some cases and even misses 10 bugs. Since
                 red
CPAchecker∆DP correctly detected those 10 bugs, the bugs seem to be an issue
of ESBMC. One important reason for a worse performance of the difference ver-
ifier, which Beyer et al. [6] also reported, is the residual program. The residual
program is generated and then verified by the reducer-based conditional veri-
fier and often changes the program structure. For example, we observed that the
residual programs may contain deeply nested branching structures that regularly
exceeded the maximum bracket nesting level of the ESBMC parser. Also, resid-
ual programs heavily use goto statements, but no while or for loop constructs,
which makes loop detection more difficult for ESBMC. However, the issues with
the residual program are orthogonal to difference verification with conditions. In
particular, they do not stem from difference verification with conditions, but how
the reducer is implemented and how non-conditional verifiers are transformed
into conditional verifiers.
     Next, we continue our study with the examination of efficiency. To this end,
we compare the runtime of the complete verification with the runtime of the
difference verifier. We measure runtime in CPU time. Figure 4 shows a scatter
plot that compares for all verifiers the CPU time the verifier uses to analyze
task t (x-axis) with the CPU time the respective difference verifier requires to
inspect the same task t (y-axis). In case a task is not solved, we use the max-
imum CPU time of 900 s. Note that for ESBMC we exclude the 10 tasks that
the difference verifier solved incorrectly, i.e., the scatter plot does not consider
   Incorporating Data Dependencies and Properties in Difference Verification                     15




                                            DP
                       CPU time of difference verifiers VD
                                                     100




                                                             10




                                                              1




                                                             0.1
                                                               0.1   1         10          100
                                                                     CPU time of verifiers V


Fig. 4: CPU time for verification (x-axis) vs. CPU time for difference verification
with our extractor (y-axis)


times of incorrectly solved tasks. We observe that a significant number of data
points (40%) in the scatter plot are below the diagonal, i.e., for those task-
verifier pairs the difference verification is faster than the complete verification of
the modified program. In further cases (about 20%), the conditional verifier is
still faster than complete verification, but conditional verification plus difference
condition extracting takes longer than the complete verification. A detailed in-
spection reveals that for some tasks categories like square+softflt the costs of
the extractor can be compensated by the saved time of the conditional verifier,
while this hardly the case for tasks of the pals+eca12 category. We also observe
differences between verifiers.

 To sum up, our results confirm the observations of Beyer et al [6]. Also,
 difference verification with our condition extractor may be more effective and
 efficient than complete verification.

    RQ 2 Do diffCond and Our Difference Condition Extractor Differ?
The previous research question has shown that difference verification with our
extractor can be beneficial. Since this is also true for difference verification with
the syntax-based extractor diffCond [6], we may speculate that this is only
because there is no difference in the extractors. This research question investigate
whether this hypothesis is true.
    Difference condition extractors may affect the performance of the difference
verifier in two ways, namely if they (a) generate different conditions or (b) dif-
fer in performance. We start with examining whether the generated conditions
differ. We forego a semantic difference and focus on a syntactical difference of
conditions, which is easier to investigate. Note that this is possible because all
our difference verifiers unroll the program along the condition. Hence, a differ-
ence in syntax, especially in structure, already affects the performance of the
difference verifier. As a proxy for structural difference, we use the number of
states in the condition. Figure 5a shows a scatter plot that compares for each
16                                             M.-C. Jakobs, T. Pollandt

                                   1x106                                                                                 1000




                                                                                             CPU time for generating conditionDDP
Number of states in conditionDDP
                   100000


                              10000                                                                                                 100


                                   1000


                                    100                                                                                              10


                                     10


                                      1                                                                                               1
                                           1     10     100    1000   10000 100000   1x106                                                1            10             100             1000
                                                 Number of states in conditionDsyn                                                            CPU time for generating conditionDsyn


(a) #condition states generated by                                                           (b) CPU time of syntax-based differ-
syntax-based (x-axis) and by our (y-                                                         ence condition extractor (x-axis) and
axis) difference condition extractor                                                         of our difference condition extractor (y-
                                                                                             axis)

                                                Fig. 5: Comparison of the two difference condition extractors

task (except for 286 regression tasks for which our extractor failed mostly due
to timeout) the number of states in the condition generated by the syntax-based
difference condition extractor diffCond (∆syn , x-axis) with the number of states
in the condition produced by our difference condition extractor (∆DP , y-axis).
We note that most data points in Fig. 5a are above or below the diagonal, i.e.,
the conditions differ in the number of states. A detailed inspection of our data
reveals that only for 317 tasks (<5% of all tasks) the condition size is the same.
In addition, the conditions generated by our extractor are larger for While for
82% of the combination tasks (blue data points) and for 55% of the regression
tasks (orange data points). We note that the generated conditions may be larger
by several magnitudes. However,there also exist 1 676 data points on the x-axis,
i.e., our extractor generates conditions with a single accepting state and, hence,
proved the absence of regression bugs. In contrast, the syntax-based difference
verification extractor only generates conditions with a single accepting state for
75 tasks, for which our extractor produces the same condition. In summary, we
conclude that our extractor produces more precise conditions than diffCond.
     We continue to investigate the performance difference (b) in terms of runtime
of the difference condition extractors. As in the previous research question, we
compare runtime measured in CPU time. Figure 5b shows a scatter plot that
compares for each task the CPU time taken by diffCond (∆syn , x-axis) with
the CPU time needed by our extractor (∆DP , y-axis). We note that most of the
data points are above the diagonal, i.e., our extractor takes longer. An analysis
of the data revealed that our extractor takes up to 5-times longer with a median
and mean increase between 8-40% per category. Furthermore, it even times out
for 285 regression tasks. The increase could have been expected considering that
our constructor produces larger and more precise conditions. Nevertheless, the
runtime of our difference condition extractor remains mostly reasonable, i.e., it
typically takes less than 10% of the runtime limit of the difference verifier (900 s).
   Incorporating Data Dependencies and Properties in Difference Verification                                             17


Table 2: Number of correct proofs (✓), of correct alarms (✗), and of incorrectly
solved tasks (✓ ) detected by each verifier and their related difference verifiers
                           eca05+token      gcd+newton      pals+eca12      sfifo+token    square+softflt   regression
                          (2 340+1 300)     (1 352+572)    (1 700+1 050)   (1 206+663)       (165+75)       (3 936+0)
                           ✓       ✗   ✓   ✓     ✗   ✓   ✓     ✗    ✓   ✓      ✗   ✓    ✓     ✗ ✓      ✓     ✗ ✓
         ∆nat
 Predicatesyn             1395     987 0 48 520 0 10             52      0 589 481 0 61 75              0 2599 0 0
             nat
 Predicate∆DP            1400      985 0 156 520 0 125           75      0 594 488 0 115 75             0 2663 0 0
         ∆red
 Predicatesyn            1394      975 0 48 474 0 10             95      0 642 468 0 81 45              0 2639 0 0
             red
 Predicate∆DP             1390     955 0 156 572 0 125           50      0 639 456 0 135 60             0 2685 0 0
               ∆red
 CPAchecker     syn      1000 1282 0 48 469 0 41 140                     0 480 663 0 61 45              0 3906 0 0
                   red
 CPAchecker∆DP 1119            1252 0 156 520 0 671 500                  0 480 638 0 117 60             0 3618 0 0
        ∆red
 ESBMC   syn                   0     0 0 333 572 0           0    0 0    0 78 0 105 75                  0       0 0 0
         red
 ESBMC∆DP                      0   900 0 880 572 0           0   70 10 101 618 0 156 75                 0       0 0 0




 In summary, our extractor computes more precise conditions, but is slower.
 Hence, we confirm the difference of the two difference condition extractors.

    RQ 3 Does Difference Verification with Our Extractor Improve
over Difference Verification with the Syntax-Based Extractor diff-
Cond? Based on the results of the previous research question, we can expect
a performance difference when exchanging the syntax-based difference condition
extractor with our extractor. However, we do not yet know whether the difference
results in an improvement with respect to effectiveness or efficiency. Therefore,
we investigate these two aspects in this research question.
    Again, we start with studying the effectiveness. For all difference verifiers con-
sidered in our experiments, Tab. 2 shows the number of correctly proved (✓) and
disproved (✗) tasks as well as the number of incorrectly solved tasks (✓ ). The
structure of the table is similar to the one of Tab. 1. The only difference is that
we exchanged the rows for the complete verification by the results for the differ-
ence verifiers using the syntax-based difference condition extractor. Now, let us
compare the results of those difference verifiers that only differ in their difference
condition extractor (∆red         red     nat      nat
                         syn vs. ∆DP or ∆syn vs. ∆DP ). When comparing the differ-
ence verifiers using the native approach for difference verification with Predicate
(first two rows), difference verification with our difference condition extractor
               nat
(Predicate∆DP ) mostly solves more tasks correctly than difference verification
                                                              nat
with the syntax-based extractor diffCond (Predicate∆syn ). A more detailed
study revealed that using our difference condition extractor, which computes a
more precise overapproximation of the paths with regression bugs, enables the
difference verifier to solve additional tasks and only for the regression tasks there
                                                        nat                         nat
exist several hundred tasks solvable by Predicate∆syn for which Predicate∆DP
fails due to timeout in the extractor. When using the reducer-based approach for
Predicate, results are more diverse. For some categories, difference verification
                                    red
with our extractor (Predicate∆DP ) detects significantly fewer alarms (✗) and
                                                                                red
sometimes also a slightly smaller number of proofs (✓), which Predicate∆syn de-
18                                                     M.-C. Jakobs, T. Pollandt



                     DP




                                                                                                             DP




                                                                                                                                                                                                     DP
                                               eca05+token                                                                              regression                                                                               square+softflt



CPU time of difference verifiers VD




                                                                                        CPU time of difference verifiers VD




                                                                                                                                                                                CPU time of difference verifiers VD
                                                 sfifo+token                                                                           gcd+newton                                                                                  pals+eca12


                              100                                                                                     100                                                                                     100




                                      10                                                                                      10                                                                                      10




                                       1                                                                                       1                                                                                       1
                                           1               10            100                                                       1                 10          100                                                       1             10             100
                                                CPU time of difference verifiers VD                                                     CPU time of difference verifiers VD                                                    CPU time of difference verifiers VD
                                                                                  syn                                                                                     syn                                                                                    syn




Fig. 6: Comparing CPU times of difference verifiers with syntax-based condition
extractor (x-axis) and with our condition extractor (y-axis)

                                                                                                                                                                                                                                                                       nat
tects close to timeout. Since most of these alarms are detected by Predicate∆DP ,
we think the structure of the residual program is responsible for the decrease
in performance and not our extractor. More importantly, there exist categories
like gcd+newton and square+softflt in which our extractor enables the dif-
                                                             red
ference verifier to solve all tasks solved by Predicate∆syn plus some additional
tasks. Also, in case of the verifier CPAchecker, the difference verifier using our
                             red
extractor (CPAchecker∆DP ) typically detects additional proofs, but sometimes
                                                                     red
detects fewer alarms than the difference verifier CPAchecker∆syn based on the
syntax-based extractor. While the decrease in category regression is caused by
the timeout of our extractor, a decrease of detected alarms occurs only in cate-
                                  red
gories for which Predicate∆DP also performs worse, and is, thus, likely caused
by the residual program. For ESBMC, difference verification with our extractor
            red                                     red                      red
(ESBMC∆DP ) always improves over ESBMC∆syn . Typically, ESBMC∆DP solves
                                 red
the same tasks as ESBMC∆syn as well as some additional tasks. Note that both
          ∆red               ∆ red
ESBMC syn and ESBMC DP do not solve any regression task because the entry
function for analysis is not main, and, therefore not supported by ESBMC.
    Next, we look at the efficiency in terms of CPU time. For each category
(column in Tab. 2), we compare the efficiency of all pairs (V ∆syn , V ∆DP ) of dif-
ference verifiers that use the same conditional verifier, but vary in the difference
condition extractor, the scatter plots Figure 6 shows scatter plots that compare
the CPU times V ∆syn (x-axis) and V ∆DP (y-axis) needed to solve a task. Again,
we use the maximum CPU time of 900 s if a task is not solved. For ESBMC,
we also exclude the results of the 10 incorrectly tasks. Once again, the scatter
plot does not consider CPU times of incorrectly solved tasks. Studying the three
scatter plots, we notice that for each category there exists data points in the
lower right half, i.e., the difference verifier V ∆DP with our extractor is faster. For
categories eca05+token and sfifo+token (left scatter plot), the extra effort of
our extractor rarely pays off. Computing a more precise condition does not pay
off and often causes a slow down of the difference verifier because all paths with
syntactical changes are already easy to verify. For categories regression and
gcd+newton (middle scatter plot), the extra effort sometimes pay off. While for
category gcd+newton in particular native Predicate and ESBMC profit from
our more precise extractor, for regression all verifiers benefit for some tasks
and for the categories square+softflt and pals+eca12 (right scatter plot) all
verifiers often benefit from our extractor.
    Incorporating Data Dependencies and Properties in Difference Verification     19


 We summarize that difference verification with our extractor is not always
 better than difference verification with the syntax-based difference condition
 extractor, but our extractor is more effective and efficient for several tasks.


4.3    Threats to Validity

Threats to Internal Validity. Implementation bugs in one of the extractors,
the residual program generator, or the verifiers may threaten the validity of our
results. We think that implementation bugs are unlikely and have at most little
impact on our results. On the one hand, we would expect that bugs in extractors
or residual program generator result in (many) false results, in particular false
proofs. However, only ESBMC reported false results for ten tasks, for which an-
other verifier succeeds. On the other hand, the verifiers themselves participate in
SV-COMP, therefore aiming to reduce the number of false results. Furthermore,
the verifiers may have benefited from the (structure of the) residual program
instead of the condition extractors. We think this is unlikely because we also
observe positive effects when using a native conditional verifier, which does not
use a residual program. In addition, our experience from the past and this paper
is that residual programs are often more difficult to verify.
    Threats to External Validity. Our results may not generalize to arbitrary
programs. Our combination tasks were artificially constructed by Beyer et al. [6]
and are the result of the combination of two tasks, i.e., have a particular structure
and differences may only occur in one of the combined tasks. While the the
regression tasks stem from real world tasks they only focus on the particular
domain of Linux device drivers. Also, our observations may not carry over to
different verifiers and extractors. Nevertheless, we confirmed the finding of Beyer
et al. [6] for our new extractor.


5     Related Work

A broad range of approaches exist that aim to protect modified programs against
regression bugs. One line of work, deals with regression testing [45]. Other ap-
proaches (dis)prove behavior preservation, e.g., [40,25,22,15,19], Also, there exist
a variety of incremental verification approaches. Like us, several of the incremen-
tal approaches skip the analysis of unchanged behavior [43,34,37,44,29,12,28,6].
Some incremental verification approaches adapt previous analysis results includ-
ing fixed points [2,39,35] or the explored state space [18,27,38] while others reuse
intermediate results like constraint solutions [42,1], abstraction details [9,36,20],
or annotations [16,46].
    Next, let us have a closer look of what unchanged parts of a program are
skipped in the different incremental verification approaches. iCoq [12] addresses
proofs in the theorem prover Coq and only reverifies Coq proofs that are affected
by the modification. The deductive verifier Dafny[29] only reverifies methods af-
fected by the modification and reuses unaffected verification conditions obtained
20      M.-C. Jakobs, T. Pollandt

in previous verification runs. In contrast, regression property selection (RPS) [28]
restricts runtime verification to properties that are related to classes that are
affected by the modification. Furthermore, DiSE [34,37] is an incremental tech-
nique for symbolic execution that directs symbolic execution towards program
statements that are affected by the modification. There also exist approaches
that stop exploration as soon as a path cannot reach a change. For instance,
RMC [43] stops DFS exploration in this case, while Memoise [44] stops symbolic
execution of states that cannot reach any modification and disables constraint
solving on unchanged paths. Originally, difference verification with condition [6]
stops if a path cannot reach a syntactic difference. We extend the framework of
difference verification with conditions with a new difference condition extractor
that stops if no modification can be reached or we can show based on data- and
control-flow that the modifications seen cannot affect the property of interest,
and, thus, cannot cause a regression bug.
    After we compared what is skipped, we now look into which information is
used to determine what is affected. Dafny [29] relies on checksums and iCoq [12]
relies on timestamps and checksums to determine affected components. In con-
trast, the syntax-based difference condition extractor from [6], Memoise [44],
and RMC [43] treat all syntactically changed paths as affected. Going beyond
pure syntactic differences, RPS [28] uses class dependencies to compute affected
classes. In contrast, our difference condition extractor mainly relies on data de-
pendencies. Similarly, DiSE [34,37] considers control and data dependencies to
detect change affected program statements and Jana et al. [23] use them to detect
which properties are affected by the modification at which locations. Finally, we
want to state that there exist approaches that use abstract interpretation [26,31]
or symbolic execution [33,11,41,30] to determine the inputs and, thus, the paths
for which the behavior of original and modified programs differ functionally. So
far, they have not been used to skip unaffected paths in reverification.


6    Conclusion

Every software modification may introduce new bugs and, thus, threaten soft-
ware reliability. When software verification is used to establish software reliabil-
ity, the software verifiers need to keep up with the frequent software changes.
Verifying the complete modified program after each change is typically too costly.
Therefore, we require incremental verifiers that rely on the insight that changes
do not introduce regression bugs everywhere in the software.
    One incremental and also verifier agnostic approach is difference verification
with conditions. It uses the idea of conditional model checking to restrict the
verification to those program parts which may contain new bugs introduced by
the change. To this end, it precedes the conditional model checker with a differ-
ence condition extractor that performs a change analysis to detect the program
paths relevant for reverification. Like the verifier, also the difference condition
extractor can be exchanged. While the proof-of-concept implementation, uses
a syntax-based difference condition extractor, we suggest a more complex dif-
   Incorporating Data Dependencies and Properties in Difference Verification        21

ference condition extractor that also considers data dependencies and program
properties during extraction. We prove its soundness and experimentally show
for various verifiers that this new difference detector improves the effectiveness
and efficiency of difference verification with condition on some tasks.


References
 1. Aquino, A., Bianchi, F.A., Chen, M., Denaro, G., Pezzè, M.: Reusing constraint
    proofs in program analysis. In: Proc. ISSTA. pp. 305–315. ACM (2015), https:
    //doi.org/10.1145/2771783.2771802
 2. Arzt, S., Bodden, E.: Reviser: Efficiently updating IDE-/IFDS-based data-flow
    analyses in response to incremental program changes. In: Proc. ICSE. pp. 288–
    298. ACM (2014), https://doi.org/10.1145/2568225.2568243
 3. Beyer, D.: Progress on software verification: SV-COMP 2022. In: Proc.
    TACAS. pp. 375–402. LNCS 13244, Springer (2022), https://doi.org/10.1007/
    978-3-030-99527-0_20
 4. Beyer, D., Dangl, M.: Strategy selection for software verification based on Boolean
    features - A simple but effective approach. In: Proc. ISoLA. pp. 144–159.
    LNCS 11245, Springer (2018), https://doi.org/10.1007/978-3-030-03421-4_11
 5. Beyer, D., Henzinger, T.A., Keremoglu, M.E., Wendler, P.: Conditional model
    checking: A technique to pass information between verifiers. In: Proc. FSE. p. 57.
    ACM (2012), https://doi.org/10.1145/2393596.2393664
 6. Beyer, D., Jakobs, M., Lemberger, T.: Difference verification with conditions. In:
    Proc. SEFM. pp. 133–154. LNCS 12310, Springer (2020), https://doi.org/10.1007/
    978-3-030-58768-0_8
 7. Beyer, D., Jakobs, M., Lemberger, T., Wehrheim, H.: Reducer-based construction
    of conditional verifiers. In: Proc. ICSE. pp. 1182–1193. ACM (2018), https://doi.
    org/10.1145/3180155.3180259
 8. Beyer, D., Keremoglu, M.E., Wendler, P.: Predicate abstraction with adjustable-
    block encoding. In: Proc. FMCAD. pp. 189–197. IEEE (2010), https://ieeexplore.
    ieee.org/document/5770949/
 9. Beyer, D., Löwe, S., Novikov, E., Stahlbauer, A., Wendler, P.: Precision reuse for
    efficient regression verification. In: Proc. FSE. pp. 389–399. ACM (2013), https:
    //doi.org/10.1145/2491411.2491429
10. Beyer, D., Löwe, S., Wendler, P.: Reliable benchmarking: Requirements and solu-
    tions. STTT 21(1), 1–29 (2019), https://doi.org/10.1007/s10009-017-0469-y
11. Böhme, M., d. S. Oliveira, B.C., Roychoudhury, A.: Partition-based regression
    verification. In: Proc. ICSE. pp. 302–311. IEEE (2013), https://doi.org/10.1109/
    ICSE.2013.6606576
12. Çelik, A., Palmskog, K., Gligoric, M.: iCoq: Regression proof selection for large-
    scale verification projects. In: Proc. ASE. pp. 171–182. IEEE (2017), https://doi.
    org/10.1109/ASE.2017.8115630
13. D’Silva, V.V., Kroening, D., Weissenbacher, G.: A survey of automated techniques
    for formal software verification. IEEE TCAD 27(7), 1165–1178 (2008), https://
    doi.org/10.1109/TCAD.2008.923410
14. Gadelha, M.Y.R., Monteiro, F.R., Cordeiro, L.C., Nicole, D.A.: ESBMC v6.0:
    Verifying C programs using k-induction and invariant inference - (competition
    contribution). In: Proc. TACAS. pp. 209–213. LNCS 11429, Springer (2019),
    https://doi.org/10.1007/978-3-030-17502-3_15
22      M.-C. Jakobs, T. Pollandt

15. Godlin, B., Strichman, O.: Regression verification. In: Proc. DAC. pp. 466–471.
    ACM (2009), https://doi.org/10.1145/1629911.1630034
16. He, F., Yu, Q., Cai, L.: Efficient summary reuse for software regression verification.
    TSE 48(4), 1417–1431 (2022), https://doi.org/10.1109/TSE.2020.3021477
17. Henzinger, T.A., Jhala, R., Majumdar, R., Sutre, G.: Lazy abstraction. In: Proc.
    POPL. pp. 58–70. ACM (2002), https://doi.org/10.1145/503272.503279
18. Henzinger, T.A., Jhala, R., Majumdar, R., Sanvido, M.A.A.: Extreme model check-
    ing. In: Verification: Theory and Practice, Essays Dedicated to Zohar Manna on
    the Occasion of His 64th Birthday. pp. 332–358. LNCS 2772, Springer (2003),
    https://doi.org/10.1007/978-3-540-39910-0_16
19. Jakobs, M.: PEQcheck: Localized and context-aware checking of functional equiv-
    alence. In: Proc. FormaliSE. pp. 130–140. IEEE (2021), https://doi.org/10.1109/
    FormaliSE52586.2021.00019
20. Jakobs, M.: Reusing predicate precision in value analysis. In: Proc. IFM. pp. 63–85.
    LNCS 13274, Springer (2022), https://doi.org/10.1007/978-3-031-07727-2_5
21. Jakobs, M.C., Pollandt, T.: diffDP: Using data dependencies and properties in
    difference verification with conditions. In: Proc. iFM. Springer (2023)
22. Jakobs, M., Wiesner, M.: PEQtest: Testing functional equivalence. In: Proc.
    FASE. pp. 184–204. LNCS 13241, Springer (2022), https://doi.org/10.1007/
    978-3-030-99429-7_11
23. Jana, A., Khadsare, A., Chimdyalwar, B., Kumar, S., Ghime, V., Venkatesh, R.:
    Fast change-based alarm reporting for evolving software systems. In: Proc. ISSRE.
    pp. 546–556. IEEE (2021), https://doi.org/10.1109/ISSRE52982.2021.00062
24. Jhala, R., Majumdar, R.: Software model checking. ACM CSUR 41(4), 21:1–21:54
    (2009), https://doi.org/10.1145/1592434.1592438
25. Jin, W., Orso, A., Xie, T.: Automated behavioral regression testing. In: Proc.
    ICST. pp. 137–146. IEEE (2010), https://doi.org/10.1109/ICST.2010.64
26. Kawaguchi, M., Lahiri, S.K., Rebelo, H.: Conditional equivalence. Tech. Rep. MSR-
    TR-2010-119, Microsoft Research (2010), https://www.microsoft.com/en-us/
    research/publication/conditional-equivalence/
27. Lauterburg, S., Sobeih, A., Marinov, D., Viswanathan, M.: Incremental state-space
    exploration for programs with dynamically allocated data. In: Proc. ICSE. pp. 291–
    300. ACM (2008), https://doi.org/10.1145/1368088.1368128
28. Legunsen, O., Zhang, Y., Hadzi-Tanovic, M., Rosu, G., Marinov, D.: Techniques for
    evolution-aware runtime verification. In: Proc. ICST. pp. 300–311. IEEE (2019),
    https://doi.org/10.1109/ICST.2019.00037
29. Leino, K.R.M., Wüstholz, V.: Fine-grained caching of verification results. In:
    Proc. CAV. pp. 380–397. LNCS 9206, Springer (2015), https://doi.org/10.1007/
    978-3-319-21690-4_22
30. Palikareva, H., Kuchta, T., Cadar, C.: Shadow of a doubt: Testing for divergences
    between software versions. In: Proc. ICSE. pp. 1181–1192. ACM (2016), https:
    //doi.org/10.1145/2884781.2884845
31. Partush, N., Yahav, E.: Abstract semantic differencing for numerical programs. In:
    Proc. SAS. pp. 238–258. LNCS 7935, Springer (2013), https://doi.org/10.1007/
    978-3-642-38856-9_14
32. Partush, N., Yahav, E.: Abstract semantic differencing via speculative correlation.
    In: Proc. OOPSLA. pp. 811–828. ACM (2014), https://doi.org/10.1145/2660193.
    2660245
33. Person, S., Dwyer, M.B., Elbaum, S.G., Pasareanu, C.S.: Differential symbolic exe-
    cution. In: Proc. FSE. pp. 226–237. ACM (2008), https://doi.org/10.1145/1453101.
    1453131
   Incorporating Data Dependencies and Properties in Difference Verification          23

34. Person, S., Yang, G., Rungta, N., Khurshid, S.: Directed incremental symbolic
    execution. In: Proc. PLDI. pp. 504–515. ACM (2011), https://doi.org/10.1145/
    1993498.1993558
35. der Plas, J.V., Stiévenart, Q., Es, N.V., Roover, C.D.: Incremental flow analysis
    through computational dependency reification. In: Proc. SCAM. pp. 25–36. IEEE
    (2020), https://doi.org/10.1109/SCAM51674.2020.00008
36. Rothenberg, B., Dietsch, D., Heizmann, M.: Incremental verification using trace
    abstraction. In: Proc. SAS. vol. LNCS 11002, pp. 364–382. Springer (2018), https:
    //doi.org/10.1007/978-3-319-99725-4_22
37. Rungta, N., Person, S., Branchaud, J.: A change impact analysis to characterize
    evolving program behaviors. In: Proc. ICSM. pp. 109–118. IEEE (2012), https:
    //doi.org/10.1109/ICSM.2012.6405261
38. Sery, O., Fedyukovich, G., Sharygina, N.: Incremental upgrade checking by means
    of interpolation-based function summaries. In: Proc. FMCAD. pp. 114–121. IEEE
    (2012), http://ieeexplore.ieee.org/document/6462563/
39. Szabó, T., Erdweg, S., Voelter, M.: IncA: A DSL for the definition of incremental
    program analyses. In: Proc. ASE. pp. 320–331. ACM (2016), https://doi.org/10.
    1145/2970276.2970298
40. Taneja, K., Xie, T., Tillmann, N., de Halleux, J.: eXpress: Guided path exploration
    for efficient regression test generation. In: Proc. ISSTA. pp. 1–11. ACM (2011),
    https://doi.org/10.1145/2001420.2001422
41. Trostanetski, A., Grumberg, O., Kroening, D.: Modular demand-driven analysis of
    semantic difference for program versions. In: Proc. SAS. pp. 405–427. LNCS 10422,
    Springer (2017), https://doi.org/10.1007/978-3-319-66706-5_20
42. Visser, W., Geldenhuys, J., Dwyer, M.B.: Green: Reducing, reusing, and recycling
    constraints in program analysis. In: Proc. FSE. pp. 58:1–58:11. ACM (2012), https:
    //doi.org/10.1145/2393596.2393665
43. Yang, G., Dwyer, M.B., Rothermel, G.: Regression model checking. In: Proc. ICSM.
    pp. 115–124. IEEE (2009), https://doi.org/10.1109/ICSM.2009.5306334
44. Yang, G., Păsăreanu, C.S., Khurshid, S.: Memoized symbolic execution. In: Proc.
    ISSTA. pp. 144–154. ACM (2012), https://doi.org/10.1145/2338965.2336771
45. Yoo, S., Harman, M.: Regression testing minimization, selection and prioritization:
    A survey. STVR 22(2), 67–120 (2012), https://doi.org/10.1002/stvr.430
46. Yu, Q., He, F., Wang, B.: Incremental predicate analysis for regression verification.
    TOPLAS 4(OOPSLA), 184:1–184:25 (2020), https://doi.org/10.1145/3428252
24         M.-C. Jakobs, T. Pollandt

A      Proving Soundness of diffDP

In the following, we write paths(P ) for the set of executable program paths of
program P = (L, ℓ0 , G, ℓerr ) and c =|V − c′ to denote that concrete data states
c, c′ map all variables except for the variables from the set V to the same value.


A.1      Helper Lemmas for Proving Theorem 2

We start with a set of lemmas that simplify the proof of Theorem 2. First, we
show that each prefix of any path with a regression bug, which is a path of the
modified program, can be related to at most one path in the difference graph
produced by our difference detector diffDP.

Lemma 1. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be two determinis-
                                                   g′               g′     g′
tic programs. For all π ′ = (ℓ′0 , c′0 ) →
                                         1
                                           (ℓ′1 , c′1 ) →
                                                        2     n
                                                          ... → (ℓ′n , c′n ) ∈ pathsrb (P, P ′ )
                           g′       g′        g′                                             g′        g′       g′
and 0≤k≤n if n0 → 1
                    n1 → 2
                           ... → k
                                   nk ∈ diffDP(P, P ′ ) and n′0 →
                                                                1
                                                                  n′1 →
                                                                      2     k
                                                                        ... →
 ′              ′              ′                            ′
nk ∈ diffDP(P, P ) such that n0 = n0 , then ∀0≤i≤k : ni = ni .

Proof. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be arbitrary determinis-
                                         g′             g′     g′
tic programs, π ′ = (ℓ′0 , c′0 ) →
                                 1
                                   (ℓ′1 , c′1 ) →
                                                2     n
                                                  ... → (ℓ′n , c′n ) ∈ pathsrb (P, P ′ ) be arbi-
                            ′
trary and diffDP (P, P ) = (N, E, n0 , ∆). Choose arbitrary k ∈ N with 0≤k≤n
                 g′       g′        g′                                              g′        g′        g′
and let n0 →1
              n1 → 2     k
                     ... →  nk ∈ diffDP(P, P ′ ) and n′0 →
                                                         1
                                                           n′1 →
                                                               2
                                                                  ... → k
                                                                          n′k ∈
            ′                                                          ′
diffDP(P, P ) be arbitrary, but both starting at the root node, i.e., n0 = n0 .
Proof by induction that ∀0≤i≤k : ni = n′i .

Base case (i = 0) Follows from assumption.
Step case (i − 1 → i, i ≤ k) By induction hypothesis, ∀0≤j≤i − 1 : nj = n′j .
   We need to show that ni = n′i . By construction N = N≀ ∪ ∆, for each
   ℓ′ ∈ L′ not exists (·, ℓ′ ) ∈ N≀ or ℓ′ ∈                  / ∆, and E ⊆ N≀ × G′ × (N≀ ∪ ∆).
   Also, ∀1≤i≤k : gi = (ℓi−1 , ·, ℓi ) ⇒ ni−1 = (·, ℓ′i−1 ) ∧ n′i−1 = (·, ℓ′i−1 ) ∧
                                ′          ′          ′

   (ni = (·, ℓ′i ) ∧ n′i = (·, ℓ′i ) ∨ ni = ℓ′i = n′i ∧ i = k). Let gi′ = (ℓ′i−1 , op′i , ℓ′i ).
   Hence, ni = ℓ′i = n′i or there exists ℓ, ℓ1 , ℓ2 ∈ L such that ni−1 = n′i−1 =
   (ℓ, ℓ′i−1 ), ni = (ℓ1 , ℓ′i ), n′i = (ℓ2 , ℓ′i ), (ni−1 , (ℓ′i−1 , op′i , ℓ′i ), (ℓ1 , ℓ′i )) ∈ E, and
   (n′i−1 , (ℓ′i−1 , op′i , ℓ′i ), (ℓ2 , ℓ′i )) ∈ E. Since P, P ′ are deterministic, all computed
   edges ((ℓp , ℓ′p ), g ′ , (ℓs , ℓ′s )) that Alg. 2 adds to E≀ are deterministic. Due to
   construction of E, we know that ((ℓ, ℓ′i−1 ), (ℓ′i−1 , opi , ℓ′i ), (ℓ1 , ℓ′i )) ∈ E and
   ((ℓ′ , ℓ′i−1 ), (ℓ′i−1 , opi , ℓ′i ), (ℓ2 , ℓ′i )) ∈ E if ((ℓ, ℓ′i−1 ), (ℓ′i−1 , opi , ℓ′i ), (ℓ1 , ℓ′i )) ∈ E≀ ,
   ((ℓ′ , ℓ′i−1 ), (ℓ′i−1 , opi , ℓ′i ), (ℓ2 , ℓ′i )) ∈ E≀ . We conclude ℓ1 = ℓ2 . Thus, ni = n′i .
                                                                                                                 ⊔
                                                                                                                 ⊓

    Next, we show that the difference detector diffDP properly extends any
alignment constructed for a real prefix of a path with regression bug if it does
not end in a regression bug indicator node.
   Incorporating Data Dependencies and Properties in Difference Verification                                            25

Lemma 2. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be arbitrary de-
terministic programs, diffDP (P, P ′ ) = (N, E, n0 , ∆), and Vδ in the state as at
                                                                            g′                g′          g′
the end of diffDP (P, P ′ ). For all π ′ = (ℓ′0 , c′0 ) →
                                                        1
                                                          (ℓ′1 , c′1 ) →
                                                                       2     n
                                                                         ... → (ℓ′n , c′n ) ∈
                                           g′                g′        g′
pathsrb (P, P ′ ) and 0≤k<n if n0 →       1
                                            n1 →2      k
                                                   ... → nk ∈ diffDP(P, P ′ ) and there
                  g1           g2      gm
exists (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓm , cm ) ∈ paths(P ) with c0 = c′0 , and there
exists total, monotonously increasing function f : {0, . . . , k} → {0, . . . , m} with
f (k) = m and ∀0≤i≤k : ni = (ℓf (i) , ℓ′i ) ∧ c′i =|V (n )− cf (i) , then there ex-
                                                                                 δ        i
            ′                                                                                             g1            g2
ists (nk , gk+1 , nk+1 ) ∈ E with nk+1 ∈ ∆ or there exist (ℓ0 , c0 ) → (ℓ1 , c1 ) →
    gm                   gm+t
. . . → (ℓm , cm ) . . . → (ℓm+t , cm+t ) ∈ paths(P ) and total, monotonously in-
creasing function f ′ : {0, . . . , k + 1} → {0, . . . , m + t} with f ′ (k + 1) = m + t and
∀0≤i≤k + 1 : ni = (ℓf ′ (i) , ℓ′i ) ∧ c′i =|V (n )− cf ′ (i) .
                                                    δ    i


Proof. Let P = (L, ℓ0 , G, ℓerr ) and P = (L′ , ℓ′0 , G′ , ℓ′err ) be arbitrary determinis-
                                                    ′

tic programs, diffDP (P, P ′ ) = (N, E, n0 , ∆), and Vδ in the state as at the end
                                                g′                 g′            g′
of diffDP (P, P ′ ). Let π ′ = (ℓ′0 , c′0 ) →
                                            1
                                              (ℓ′1 , c′1 ) →
                                                           2     n
                                                             ... → (ℓ′n , c′n ) ∈ pathsrb (P, P ′ ),
                                         g′             g′        g′
k ∈ N such that 0≤k<n and n0 →      1
                                      n1 →2
                                             ... → k
                                                      nk ∈ diffDP(P, P ′ ) be arbitrary
                                      g1           g2       gm
such that there exists π = (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓm , cm ) ∈ paths(P ) with
         ′
c0 = c0 and there exists total, monotonously increasing function f : {0, . . . , k} →
{0, . . . , m} with f (k) = m and ∀0≤i≤k : ni = (ℓf (i) , ℓ′i )∧c′i =|V (n )− cf (i) . In the
                                                                         δ i
                                                          ′
following, we need to show that there exists (nk , gk+1        , nk+1 ) ∈ E s.t. nk+1 ∈ ∆
                                   g1                   g2        gm                          gm+t
or there exists πn = (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓm , cm ) . . . → (ℓm+t , cm+t ) ∈
paths(P ) and total, monotonously increasing function f ′ : {0, . . . , k + 1} →
{0, . . . , m + t} with f ′ (k + 1) = m + t and ∀0≤i≤k + 1 : ni = (ℓf ′ (i) , ℓ′i ) ∧
c′i =|V (n )− cf ′ (i) . Since π ′ ∈ pathsrb (P, P ′ ), π ∈ paths(P ), and c0 = c′0 , we
         δ   i
know ∀0 ≤ i ≤ m : ℓi ̸= ℓerr . Hence, by construction for all 0 ≤ i ≤ k, ni ∈
(L \ {ℓerr }) × (L′ \ ({ℓ′err } ∪ ∆)) and Alg. 2 ensures that its while loop explores
nk with Vδ (nk ). Furthermore, nk = (ℓf (k) , ℓk ) = (ℓm , ℓk ). Due to semantics and
                           ′
k < n, there exists gk+1       = (ℓ′k , op′k+1 , ℓ′k+1 ) for some op′k+1 ∈ Ops. We distin-
guish between the operation type of op′k+1 .
Case 1: op′k+1 assignment Due to the semantics, c′k =|wrt(op′                                            )−
                                                                                                               c′k+1 . Now,
                                                                                                   k+1
    consider two cases.
     1. Assume there exists ℓm+1 ∈ L with gk+1 = (ℓm , op′k+1 , ℓm+1 ) ∈ G.
                                                                                                   gk+1
         Due to semantics, there exists transition step (ℓm , cm ) → (ℓm+1 , cm+1 )
         and cm =|wrt(op′ )− cm+1 . From c′k =|V ((ℓ ,ℓ′ ))− cm , we conclude that
                             k+1                                        δ    m        k
         c′k+1 =|(V ((ℓ ,ℓ′ ))∪wrt(op′        ))−
                                                        cm+1 . Furthermore, we conclude that if
                     δ   m   k          k+1
         Vδ ((ℓm , ℓ′k )) ∩ rd(op′k+1 ) = ∅, from the semantics it then follows that
         c′k+1 =|(V ((ℓ ,ℓ′ ))\wrt(op′ ))− cm+1 . Let Vdiff = Vδ ((ℓm , ℓ′k )) \ wrt(op′k+1 )
                     δ   m   k       k+1
         if Vδ ((ℓm , ℓ′k )) ∩ rd(op′k+1 ) = ∅ and Vdiff = Vδ ((ℓm , ℓ′k )) ∪ wrt(op′k+1 )
         otherwise. Then, we can derive c′k+1 =|V − cm+1 . Also, Alg. 2 ei-
                                                                             diff
         ther (a) adds((ℓm , ℓ′k ), gk+1
                                     ′
                                         , ℓ′k+1 ) to E≀ and adds ℓ′k+1 to ∆, (b) adds
26       M.-C. Jakobs, T. Pollandt

         ((ℓm , ℓ′k ), gk+1
                        ′
                            , (ℓm+1 , ℓ′k+1 )) to E≀ and already added ℓ′k+1 to ∆, or (c) it
                          ′      ′
         adds ((ℓm , ℓk ), gk+1      , (ℓm+1 , ℓ′k+1 )) to E≀ , (ℓm+1 , ℓ′k+1 ) to N≀ , and Vdiff
                            ′
         to Vδ ((ℓm+1 , ℓk+1 )). Due to construction of E and never deleting from
         ∆, E≀ , Vδ , there either exists ((ℓm , ℓ′k ), gk+1′
                                                                 , ℓ′k+1 ) ∈ E with ℓ′k+1 ∈ ∆ or
         ((ℓm , ℓk ), gk+1 , (ℓm+1 , ℓk+1 )) ∈ E with Vdiff ⊆ Vδ ((ℓm+1 , ℓ′k+1 )). In the
                  ′     ′                ′
                                                                                   g1         g2
         latter case, we set f ′ = f ∪{(k +1, m+1)} and πn = (ℓ0 , c0 ) → (ℓ1 , c1 ) →
               gm               g  m+1
         . . . → (ℓm , cm ) → (ℓm+1 , cm+1 ). Since Vdiff ⊆ Vδ ((ℓm+1 , ℓ′k+1 )), also
           ′
         ck+1 =|V ((ℓ         ,ℓ′   ))−
                                         cm+1 . From f being total and monotonously in-
                        δ   m+1      k+1
         creasing with largest value m, we conclude f ′ is total and monotonously
         increasing. By construction of f ′ , we get ∀0≤i≤k + 1 : ni = (ℓf ′ (i) , ℓ′i ) ∧
         c′i =|V (n )− cf ′ (i) .
                δ  i
      2. Assume there does not exit ℓm+1 ∈ L s.t. gk+1 = (ℓm , op′k+1 , ℓm+1 ) ∈
         G. From c′k =|V ((ℓ ,ℓ′ ))− cm and c′k =|wrt(op′ )− c′k+1 , we get that
                                     δ     m   k                                  k+1
         c′k+1 =|( V ((ℓ ,ℓ′ ))∪wrt(op′              ))−
                                                           cm . Also, Alg. 2 either (a) adds ℓ′k+1 to ∆
                        δ    m   k             k+1
         and((ℓm , ℓ′k ), gk+1
                             ′
                                  , ℓ′k+1 ) to E≀ , (b) adds ((ℓm , ℓ′k ), gk+1
                                                                            ′
                                                                                , (ℓm , ℓ′k+1 )) to E≀
         and already added ℓ′k+1 to ∆, or (c) it adds ((ℓm , ℓ′k ), gk+1            ′
                                                                                         , (ℓm , ℓ′k+1 ))
         to E≀ , (ℓm , ℓ′k+1 ) to N≀ , and Vdiff to Vδ ((ℓm , ℓ′k+1 )). Due to construc-
         tion of E and never deleting elements from ∆, E≀ , Vδ , there either exists
         ((ℓm , ℓ′k ), gk+1
                        ′
                            , ℓ′k+1 ) ∈ E with ℓ′k+1 ∈ ∆ or ((ℓm , ℓ′k ), gk+1  ′
                                                                                      , (ℓm , ℓ′k+1 )) ∈
         E with (Vδ ((ℓm , ℓ′k ))∪wrt(op′k+1 )) ⊆ Vδ ((ℓm , ℓ′k+1 )). In the latter case, set
         πn = π and f ′ = f ∪{(k +1, m)}. Then, we conclude from (Vδ ((ℓm , ℓ′k ))∪
         wrt(op′k+1 )) ⊆ Vδ ((ℓm , ℓ′k+1 )) that also c′k+1 =|( V ((ℓ ,ℓ′ ))∪wrt(op′ ))−
                                                                                              δ   m   k+1         k+1
         cm . From f being total and monotonously increasing with largest value
         m, we infer f ′ is total and monotonously increasing. By construction of
         f ′ , we get ∀0≤i≤k + 1 : ni = (ℓf ′ (i) , ℓ′i ) ∧ c′i =|V (n )− cf ′ (i) .
                                                                                  δ       i

Case 2: op′k+1 assume operation Let r be the number of iterations of the
   while loop in lines 13–14, in which that while loop explores assignments
   (ℓpm+1 , opm+1 , ℓm+1 ),. . . ,(ℓpm+r
                                      S,r opm+r , ℓm+r ) and computes change affected
   variables Vdiff = Vδ ((ℓm , ℓ′k )) i=1 wrt(opm+i ). By construction, we get ℓpm+1 =
   ℓm and ∀2 ≤ i ≤ r : ℓm+i−1 = ℓpm+i . Due to semantics, there exists
               gm+1                                gm+2       gm+r
     (ℓm , cm ) → (ℓm+1 , cm+1 ) → . . . → (ℓm+r , cm+r ) s.t. for all 1 ≤ i ≤ r,
                                                                  g1           g2
     cm+i−1 =|Si            −
                              cm+i . Furthermore, πi = (ℓ0 , c0 ) → (ℓ1 , c1 ) →
                            wrt(opk+j )
                    j=1
         gm                  gm+1                            gm+2      gm+r
     . . . → (ℓm , cm ) → (ℓm+1 , cm+1 ) → . . . → (ℓm+r , cm+r ) ∈ paths(P )
     and after the while loop ℓp = ℓm+r . From c′k =|V ((ℓ ,ℓ′ ))− cm , we conclude
                                                                              δ       m       k
     c′k =|V − cm+r . Due to semantics, c′k+1 = c′k . Hence, c′k+1 =|V − cm+r .
            diff                                                            diff
     Now consider four cases.
      1. Assume ℓp ̸= ℓerr , there exists (ℓp , op′k+1 , ℓm+r+1 ) ∈ G, and rd(op′k+1 ) ∩
                                                ′
                                               gk+1
         Vdiff = ∅. Since (ℓ′k , c′k ) → (ℓ′k+1 , c′k+1 ) implies c′k |= op′k+1 and we know
         c′k =|V − cm+r and rd(op′k+1 ) ∩ Vdiff = ∅, also cm+r |= op′k+1 . Due to
                 diff
                                                                                                  (ℓm+r ,op′k+1 ,ℓm+r+1 )
         semantics and ℓp = ℓm+r , there exists (ℓm+r , cm+r ) −−−−−−−−−−−−−−→
Incorporating Data Dependencies and Properties in Difference Verification                    27

     (ℓm+r+1 , cm+r+1 ) with cm+r+1 = cm+r and, thus, c′k+1 =|V                     −
                                                                                        cm+r+1 .
                                                                             diff
                            g1             g2         gm        gm+1                       gm+2
     Also, πn = (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓm , cm ) → (ℓm+1 , cm+1 ) →
         gm+r                    (ℓm+r ,op′k+1 ,ℓm+r+1 )
     . . . → (ℓm+r , cm+r ) −−−−−−−−−−−−−−→ (ℓm+r+1 , cm+r+1 ) ∈ paths(P ).
     Algorithm 2 either (a) adds ℓ′k+1 to ∆ and((ℓm , ℓ′k ), gk+1  ′
                                                                        , ℓ′k+1 ) to E≀ , (b)
     adds ((ℓm , ℓk ), gk+1 , (ℓm+r+1 , ℓk+1 ) to E≀ and already added ℓ′k+1 to ∆, or
                   ′    ′                ′

     (c) adds ((ℓm , ℓ′k ), gk+1
                             ′
                                 , (ℓm+r+1 , ℓ′k+1 )) to E≀ , (ℓm+r+1 , ℓ′k+1 ) to N≀ , and
                               ′
     Vdiff to Vδ ((ℓm+r+1 , ℓk+1 )). Due to construction of E and never deleting
     elements from ∆, E≀ , Vδ , there either exists ((ℓm , ℓ′k ), gk+1   ′
                                                                              , ℓ′k+1 ) ∈ E
             ′                        ′    ′                  ′
     with ℓk+1 ∈ ∆ or ((ℓm , ℓk ), gk+1 , (ℓm+r+1 , ℓk+1 )) ∈ E with Vdiff ⊆
     Vδ ((ℓm+r+1 , ℓ′k+1 )). In the latter case, consider πn and set f ′ = f ∪
     {(k + 1, m + r + 1)}. Since Vdiff ⊆ Vδ ((ℓm+r+1 , ℓ′k+1 )) and c′k+1 =|V −
                                                                                        diff
     cm+r+1 , also c′k+1 =|V ((ℓ          ,ℓ′   ))−
                                                    cm+r+1 . From f being total and
                                 δ   m+r+1      k+1
     monotonously increasing with largest value m, we infer f ′ is total and
     monotonously increasing. By construction of f ′ , we get ∀0≤i≤k + 1 :
     ni = (ℓf ′ (i) , ℓ′i ) ∧ c′i =|V (n )− cf ′ (i) .
                                 δ   i


  2. Assume ℓp ̸= ℓerr , there exists (ℓp , op′m+r+1 , ℓm+r+1 ) ∈ G s.t. opm+r+1 is
     satisfiable, op′k+1 =⇒ opm+r+1 , and (rd(op′k+1 ) ∪ rd(opm+r+1 )) ∩ Vdiff =
                           ′
                          gk+1
     ∅. Since (ℓ′k , c′k ) → (ℓ′k+1 , c′k+1 ) implies c′k |= op′k+1 and we know
     c′k =|V − cm+r and rd(op′k+1 ) ∩ Vdiff = ∅, also cm+r |= op′k+1 . Due
            diff
     to op′k+1 =⇒ opm+r+1 , furthermore cm+r |= opm+r+1 . Due to se-
                                                                  (ℓm+r ,opm+r+1 ,ℓm+r+1 )
     mantics and ℓp = ℓm+r , there exists (ℓm+r , cm+r ) −−−−−−−−−−−−−−−−→
     (ℓm+r+1 , cm+r+1 ) with cm+r+1 = cm+r and, thus, c′k+1 =|V − cm+r+1 .
                                                                             diff
                            g1             g2         gm        gm+1                       gm+2
     Also, πn = (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓm , cm ) → (ℓm+1 , cm+1 ) →
         gm+r                    (ℓm+r ,opm+r+1 ,ℓm+r+1 )
     . . . → (ℓm+r , cm+r ) −−−−−−−−−−−−−−−−→ (ℓm+r+1 , cm+r+1 ) ∈ paths(P ).
     Algorithm 2 either (a) adds ℓ′k+1 to ∆ and((ℓm , ℓ′k ), gk+1   ′
                                                                        , ℓ′k+1 ) to E≀ , (b)
     adds ((ℓm , ℓk ), gk+1 , (ℓm+r+1 , ℓk+1 ) to E≀ and already added ℓ′k+1 to ∆, or
                   ′    ′                ′

     (c) adds ((ℓm , ℓ′k ), gk+1
                             ′
                                 , (ℓm+r+1 , ℓ′k+1 )) to E≀ , (ℓm+r+1 , ℓ′k+1 ) to N≀ , and
                               ′
     Vdiff to Vδ ((ℓm+r+1 , ℓk+1 )). Due to construction of E and never deleting
     elements from ∆, E≀ , Vδ , there either exists ((ℓm , ℓ′k ), gk+1   ′
                                                                              , ℓ′k+1 ) ∈ E
             ′                        ′    ′                  ′
     with ℓk+1 ∈ ∆ or ((ℓm , ℓk ), gk+1 , (ℓm+r+1 , ℓk+1 )) ∈ E with Vdiff ⊆
     Vδ ((ℓm+r+1 , ℓ′k+1 )). In the latter case, consider πn and set f ′ = f ∪
     {(k + 1, m + r + 1)}. Since Vdiff ⊆ Vδ ((ℓm+r+1 , ℓ′k+1 )) and c′k+1 =|V −
                                                                                         diff
     cm+r+1 , also c′k+1 =|V ((ℓ          ,ℓ ′  ))−
                                                    c m+r+1  .  From  f  being     total  and
                                 δ   m+r+1      k+1
     monotonously increasing with largest value m, we infer f ′ is total and
     monotonously increasing. By construction of f ′ , we get ∀0≤i≤k + 1 :
     ni = (ℓf ′ (i) , ℓ′i ) ∧ c′i =|V (n )− cf ′ (i) .
                                 δ   i


  3. Assume ℓp ̸= ℓerr , there exists (ℓp , op′k+1 , ℓ2 ) ∈ G s.t. rd(op′k+1 )∩Vdiff ̸= ∅
     or there exists (ℓp , opm+r+1 , ℓ2 ) ∈ G with opm+r+1 being satisfiable,
     op′k+1 =⇒ opm+r+1 , and (rd(op′k+1 ) ∪ rd(opm+r+1 )) ∩ Vdiff ̸= ∅. Algo-
     rithm 2 adds ((ℓm , ℓ′k ), gk+1
                                 ′
                                     , ℓ′k+1 ) to E≀ and adds or already added ℓ′k+1
28       M.-C. Jakobs, T. Pollandt

         to ∆. Due to construction of E, there exists ((ℓm , ℓ′k ), gk+1         ′
                                                                                     , ℓ′k+1 ) ∈ E
                 ′
         with ℓk+1 ∈ ∆.
      4. Assume ℓp = ℓerr or there does not exist (ℓp , op′k+1 , ℓ2 ) ∈ G and there
         does not exist (ℓp , opm+r+1 , ℓ2 ) ∈ G with opm+r+1 being satisfiable and
         op′k+1 =⇒ opm+r+1 . Since ep = ℓm+r , Alg. 2 either (a) adds ℓ′k+1 to ∆
         and((ℓm , ℓ′k ), gk+1
                            ′
                                , ℓ′k+1 ) to E≀ , (b) adds ((ℓm , ℓ′k ), gk+1
                                                                          ′
                                                                              , (ℓm+r , ℓ′k+1 )) to
                                      ′                                   ′    ′
         E≀ and already added ℓk+1 to ∆, or (c) it adds ((ℓm , ℓk ), gk+1          , (ℓm+r , ℓ′k+1 ))
                              ′                                             ′
         to E≀ , (ℓm+r , ℓk+1 ) to N≀ , and Vdiff to Vδ ((ℓm+r , ℓk+1 )). Due to con-
         struction of E and never deleting elements from ∆, E≀ , Vδ , there ei-
         ther exists ((ℓm , ℓ′k ), gk+1′
                                           , ℓ′k+1 ) ∈ E with ℓ′k+1 ∈ ∆ or there exists
         ((ℓm , ℓk ), gk+1 , (ℓm+r , ℓk+1 )) ∈ E with Vdiff ⊆ Vδ ((ℓm+r , ℓ′k+1 )). In the
                  ′    ′                ′

         latter case, set πn = πi and f ′ = f ∪ {(k + 1, m + r)}. Since Vdiff ⊆
         Vδ ((ℓm+r , ℓ′k+1 )) and c′k+1 =|V − cm+r , also c′k+1 =|V ((ℓ            ,ℓ′    ))−
                                                                                              cm+r .
                                                 diff                                  δ   m+r    k+1
         From f being total and monotonously increasing with largest value m,
         we infer f ′ is total and monotonously increasing. By construction of f ′ ,
         we get ∀0≤i≤k + 1 : ni = (ℓf ′ (i) , ℓ′i ) ∧ c′i =|V (n )− cf ′ (i) .
                                                             δ  i
                                                                                ⊔
                                                                                ⊓

    Based on the previous lemmas, we now show that for any prefix of a path
with regression bug that can be aligned with a path in the graph constructed
by the difference detector diffDP that does not visit bug indicator nodes, there
exist an alignable path in the original program.

Lemma 3. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be arbitrary deter-
ministic programs, diffDP (P, P ′ ) = (N, E, n0 , ∆), and Vδ in the state as at the
                                                                   g′                 g′     g′
end of diffDP (P, P ′ ). For all π ′ = (ℓ′0 , c′0 ) →
                                                    1
                                                      (ℓ′1 , c′1 ) →
                                                                   2     n
                                                                     ... → (ℓ′n , c′n ) ∈
                                            g′           g′                 g′
pathsrb (P, P ′ ) and 0≤k≤n if n0 →     1
                                             n1 →2
                                                    ... →k
                                                             nk ∈ diffDP(P, P ′ ) and
                                          g1          g2      gm
∀0 ≤ i ≤ k : ni ∈  / ∆, then ∃(ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓm , cm ) ∈ paths(P ) :
c0 = c′0 ∧ ∃f : {0, . . . , k} → {0, . . . , m} : f total, monotonously increasing
∧f (k) = m ∧ ∀0≤j≤k : nj = (ℓf (j) , ℓ′j ) ∧ c′j =|V (n )− cf (j) .
                                                               δ        j


Proof. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be arbitrary determinis-
tic programs, diffDP (P, P ′ ) = (N, E, n0 , ∆), and Vδ in the state as at the end
                                            g′                g′                 g′
of diffDP (P, P ′ ). Let π ′ = (ℓ′0 , c′0 ) →
                                            1
                                              (ℓ′1 , c′1 ) →
                                                           2     n
                                                             ... → (ℓ′n , c′n ) ∈ pathsrb (P, P ′ ),
                                   g′      g′           g′
k ∈ N s.t. 0≤k≤n, and n0 → 1
                             n1 →2     k
                                   ... → nk ∈ diffDP(P, P ′ ) s.t. ∀0 ≤ j ≤
k : nj ∈
       / ∆ be arbitrary. Prove by induction, for all 0 ≤ i ≤ k there exists
          g1              g2     gm
(ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . →i (ℓmi , cmi ) ∈ paths(P ) with c0 = c′0 , and there
exists total monotonously increasing function f : {0, . . . , i} → {0, . . . , mi } with
f (i) = mi and ∀0≤j≤i : nj = (ℓf (j) , ℓ′j ) ∧ c′j =|V (n )− cf (j) .
                                                                   δ        j


Base case (i = 0) Define c′0 = c0 and f := {(0, 0)}. By definition, we get
   (ℓ0 , c0 ) ∈ paths(P ). Obviously, f (0) = 0. Furthermore, f is total, monotonously
   increasing. Since n0 ∈  / ∆, Alg. 2 sets n0 = (ℓ0 , ℓ′0 ). Furthermore, c0 = c′0 im-
            ′
   plies c0 =|V (n )− cf (0) .
                  δ   0
   Incorporating Data Dependencies and Properties in Difference Verification                                        29

                                                      g′          g′            g′
                                      1
Step case (i − 1 → i, i ≤ k) Since n0 →    2
                                        n1 →     k
                                             ... → nk ∈ diffDP(P, P ′ ), by
                                                            ′
                                     g′       g′           gi−1
                              1
    definition also prefix n0 →    2
                                n1 → . . . → ni−1 ∈ diffDP(P, P ′ ). By induc-
                                      g1               g2              gmi−1
    tion, there exists (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . → (ℓmi−1 , cmi−1 ) ∈ paths(P )
    with c0 = c′0 , and there exists total, monotonously increasing function f :
    {0, . . . , i − 1} → {0, . . . , mi−1 } with f (i − 1) = mi−1 and ∀0≤j≤i − 1 : nj =
    (ℓf (j) , ℓ′j ) ∧ c′j =|V (n )− cf (j) . Due to Lemma 2 and i − 1 < k ≤ n, there ex-
                            δ   j
                                                                                                    g1              g2
    ists (ni−1 , gi′ , ns ) ∈ E such that ns ∈ ∆ or there exists (ℓ0 , c0 ) → (ℓ1 , c1 ) →
            gmi−1                          gmi−1 +t
    . . . → (ℓmi−1 , cmi−1 ) . . . →   (ℓmi−1 +t , cmi−1 +t ) ∈ paths(P ) and to-
    tal, monotonously increasing function f ′ : {0, . . . , i} → {0, . . . , mi−1 + t}
    with f ′ (i) = mi−1 + t and ∀0≤j<i : nj = (ℓf ′ (j) , ℓ′j ) ∧ c′j =|V (n )− cf ′ (j)
                                                                                                    δ     j
                                                                                                                    ′
                                                                                          g1′            g2′       gi−1
    and ns = (ℓf ′ (i) , ℓ′i ) ∧ c′i =|V (n )−      cf ′ (i) . By definition, n0 → n1 → . . . →
                                        δ  s
             g′
    ni−1 →i ns ∈ diffDP(P, P ′ ). Due to Lemma 1, ns = ni , and, thus, ns ∈
                                                                          / ∆.
    Set mi = mi−1 + t. The hypothesis follows.
                                                                             ⊔
                                                                             ⊓


A.2     Proof of Theorem 2

Theorem 2. Algorithm 2 returns a difference graph.

Proof. Let P = (L, ℓ0 , G, ℓerr ) and P ′ = (L′ , ℓ′0 , G′ , ℓ′err ) be arbitrary determin-
istic programs and diffDP (P, P ′ ) = (N, E, n0 , ∆) the output of Alg. 2. By
construction, n0 ∈ N , ∆ ⊆ N , and E ⊆ N × G′ × N . It remains to be shown
                                g′           g′       g′
that for all π ′ = (ℓ′0 , c′0 ) →
                                1
                                  (ℓ′1 , c′1 ) →
                                               2     n
                                                 ... → (ℓ′n , c′n ) ∈ pathsrb (P, P ′ ) and 0≤k≤n
       g′         g′   g′                                                                       ·              ·
if n0 → 1
          n1 →2      k
                 ... → nk ∈ diffDP(P, P ′ ), then there exists nk → . . . → nk+m
with nk+m ∈ ∆.
    If Alg. 2 returns in line 19, the property is trivially fulfilled. We continue to
show that the property also yields if Alg. 2 does not return in line 19, i.e., it
                                               g′                 g′           g′
returns in line 21. Let π ′ = (ℓ′0 , c′0 ) →
                                           1
                                             (ℓ′1 , c′1 ) →
                                                          2     n
                                                            ... → (ℓ′n , c′n ) ∈ pathsrb (P, P ′ ),
                                     g′        g′          g′
k ∈ N s.t. 0≤k≤n, and n0 →  1
                              n1 →2
                                    ... →k
                                           nk ∈ diffDP(P, P ′ ) be arbitrary.
Furthermore, let Vδ be in the same state as at the end of diffDP (P, P ′ ). If
                                                             1      2     g′
                                                                           k         g′   g′
nk ∈ ∆, the existence claim follows from path n0 →             n1 →   ... →   nk . If nk ∈
                                                                                         / ∆,
                                     ′             ′
by construction N≀ ⊆ L × L , ∆ ⊆ L and by definition of E in line 20 no
edge leaves a node from ∆. Hence, also all ni with 0≤i≤k are no elements of
                                                       g1        g2       gm
∆. Due to Lemma 3, there exists (ℓ0 , c0 ) → (ℓ1 , c1 ) → . . . →k (ℓmk , cmk ) ∈
paths(P ) s.t. c0 = c′0 , and there exists total, monotonously increasing function
f : {0, . . . , k} → {0, . . . , mk } with f (k) = mk and ∀0≤i≤k : ni = (ℓf (i) , ℓ′i ) ∧
c′i =|V (n )− cf (i) . Since π ′ ∈ pathsrb (P, P ′ ), we conclude ∀0≤j≤mk : ℓj ̸= ℓerr .
       δ   i
Since Alg. 2 does not return in line 19 and ℓ0 ̸= ℓerr , also ℓ′0 ̸= ℓ′err . By construc-
tion, ℓ′0 ̸= ℓ′err , ∀0≤i≤k : ni = (ℓf (i) , ℓ′i ), and ∀0≤j≤mk : ℓj ̸= ℓerr , we know that
all ni with 0≤i≤k are from (L \ {ℓerr }) × (L′ \ {ℓ′err }). Now, let ie ∈ N be the
30          M.-C. Jakobs, T. Pollandt

smallest index such that 0 ≤ ie ≤ n and ℓ′ie = ℓ′err . Since π ′ ∈ pathsrb (P, P ′ )
such an ie exists. Furthermore, due to ni = (·, ℓ′i ) ∈ (L \ {ℓerr }) × (L′ \ {ℓ′err })
for all 0 ≤ i ≤ k, also ie > k. Show by induction that for all t ∈ N either
                                                           1    2     k                                   g′          g′   g′
k + t > ie or k + t ≤ ie and there exist 0 ≤ ts ≤ t and n0 → n1 → ... →
      ′            ′
     gk+1         gk+t
nk → . . . → s nk+ts ∈ diffDP(P, P ′ ) such that nk+ts ∈ ∆ or ts = t and
∀0 ≤ j ≤ ts : nk+j ∈
                   / ∆.

                                                                             g′      g′           g′
Base case (t = 0) Follows from ie > k, n0 →  1
                                               n1 →2     k
                                                     ... → nk ∈ diffDP(P, P ′ ),
   and nk ∈
          / ∆.
Step case (t − 1 → t) If k + t > ie or k + t ≤ ie and there exist 0 ≤ ts ≤ t − 1
                                                      ′                ′
                  g′         g′          g′          gk+1             gk+t
     and n0 →1
               n1 →2     k
                     ... → nk → . . . → s nk+ts ∈ diffDP(P, P ′ ) such that
     nk+ts ∈ ∆, nothing needs to be shown. Assume k + t ≤ ie and there do
                                                                                                    ′           ′
                                     1     2     k           g′              g′       g′           gk+1        gk+t
     not exist 0 ≤ ts ≤ t − 1 and n0 → n1 →  ... → nk → . . . → s nk+ts ∈
                 ′
     diffDP(P, P ) such that nk+ts ∈ ∆. By induction hypothesis, there exists
                                               ′             ′
            g′         g′         g′          gk+1          gk+t−1
     n0 → 1
            n1 → 2
                   ... → k
                           nk → . . . → nk+t−1 ∈ diffDP(P, P ′ ) such that
     ∀0 ≤ j ≤ t − 1 : nk+j ∈   / ∆. Since k + t ≤ ie ≤ n, also k + t − 1 < n.
     Furthermore, from before we know that ∀0 ≤ j ≤ k : nj ∈      / ∆. Hence,
     ∀0 ≤ j ≤ k + t − 1 : nj ∈
                             / ∆. Combining Lemma 3 and Lemma 2, we conclude
                             ′
     there exists (nk+t−1 , gk+t , nk+t ) ∈ E with nk+t ∈ ∆ ∨ nk+1 = (·, ℓ′k+t ).
     By construction of ∆, if nk+1 = (·, ℓ′k+t ), then nk+1 ∈
                                                            / ∆. By definition,
                                               ′             ′                        ′
            g′         g′         g′          gk+1          gk+t−1                   gk+t
     n0 →1
           n1 →2
                 ... →k
                        nk → . . . → nk+t−1 → nk+t ∈ diffDP(P, P ′ ) :
     nk+t ∈ ∆ ∨ ∀0 ≤ j ≤ t : nk+j ∈
                                  / ∆. The induction hypothesis follows.

Consider t = ie − k. Since ie > k, we know t > 0. Due to induction, there exist
                                                                          ′            ′
                                        g′       g′         g′           gk+1         gk+t
                       1
0 ≤ ts ≤ ie − k and n0 →    2
                         n1 →      k
                               ... → nk → . . . → s nk+ts ∈ diffDP(P, P ′ )
such that nk+ts ∈ ∆ or ts = ie − k and ∀0 ≤ j ≤ ts : nk+j ∈ / ∆. Show by
                                                             1    2     k                                 g′          g′   g′
contradiction that there do not exist 0 ≤ ts ≤ ie − k and n0 → n1 → ... →
      ′           ′
     gk+1        gk+t
nk → . . . → s nk+ts ∈ diffDP(P, P ′ ) such that ts = ie − k and ∀0 ≤ j ≤ ts :
nk+j ∈
     / ∆. Assume the contrary. From before we know that ∀0 ≤ j ≤ k : nj ∈/ ∆.
                                        g′           g′          g′
                                                                               ′
                                                                              gk+1          gi′
Hence, there exists n0 →      1
                                n1 →  2
                                         ... → k
                                                  nk → . . . →e nie ∈ diffDP(P, P ′ )
                                                                                           g1
s.t. ∀0 ≤ j ≤ ie : nj ∈      / ∆. Due to Lemma 3, there exists π = (ℓ0 , c0 ) →
           g2      gm
(ℓ1 , c1 ) → . . . → (ℓm , cm ) ∈ paths(P ) with c0 = c′0 and nie = (ℓm , ℓ′ie ). Since
π ′ ∈ pathsrb (P, P ′ ), we know π ∈ / pathserr . Hence, ℓm ̸= ℓerr and since ℓ′ie = ℓ′err ,
we conclude (ℓm , ℓ′ie ) ∈ (L \ {ℓerr }) × {ℓ′err }. Since ℓ′0 ̸= ℓ′err and by construction
nie = (ℓm , ℓ′err ) ∈ / ∆ implies (ℓm , ℓ′err ) ∈ N≀ , we conclude (ℓm , ℓ′err ) must be
added in line 32. To be added in line 32, (ℓm , ℓ′err ) ∈   / (L \ {ℓerr }) × {ℓ′err }, which
contradicts (ℓm , ℓ′ie ) ∈ (L \ {ℓerr }) × {ℓ′err }. Hence, there do not exist 0 ≤ ts ≤
                                                             ′                ′
                        g′         g′           g′          gk+1             gk+t
ie − k and n0 → 1
                  n1 →2
                        ... → k
                                nk → . . . → s nk+ts ∈ diffDP(P, P ′ ) with
ts = ie − k and ∀0 ≤ j ≤ ts : nk+j ∈
                                   / ∆. Thus, there exist 0 ≤ ts ≤ ie − k and
  Incorporating Data Dependencies and Properties in Difference Verification   31

                      ′       ′
   g′   g′     g′    gk+1    gk+t
   1
n0 →    2
     n1 →     k
          ... → nk → . . . → s nk+ts ∈ diffDP(P, P ′ ) such that nk+ts ∈ ∆.
                                                                          ⊔
                                                                          ⊓
