                                        Beyond k-induction: Learning from Counterexamples to
                                               Bidirectionally Explore the State Space

                                                   Mikhail R. Gadelha1 , Felipe R. Monteiro2 , Enrico Steffinlongo1 ,
                                                               Lucas C. Cordeiro3 , and Denis Nicole1
                                                                1
                                                                 University of Southampton, United Kingdom
                                                                   2
                                                                     Federal University of Amazonas, Brazil
                                                                 3
                                                                   University of Manchester, United Kingdom
                                                                       esbmc@googlegroups.com
arXiv:1904.02501v1 [cs.LO] 4 Apr 2019




                                               Abstract. We describe and evaluate a novel k-induction proof rule called bidi-
                                               rectional k-induction (bkind), which substantially improves the k-induction bug-
                                               finding capabilities. Particularly, bkind exploits the counterexamples generated
                                               by the over-approximation step to derive new properties and feed them back to
                                               the bounded model checking procedure. We also combine an interval invariant
                                               generator and bkind to significantly improve the number of correct verification
                                               results. Experimental results show that bkind can considerably reduce the verifi-
                                               cation time compared to the naı̈ve k-induction proof rule, since it only requires
                                               half the number of steps to find a given safety property violation in an unsafe pro-
                                               gram. The bkind algorithm outperforms 2LS, another state-of-the-art k-induction
                                               verifier, and produces more than twice correct proofs and about 35% more correct
                                               alarms than when analysing a large set of public available benchmarks.


                                        1   Introduction
                                        Software model checking has experienced significant progress in the last two decades,
                                        however, one major bottleneck for its practical applications is scalability. In particular,
                                        Bounded Model Checking (BMC) is a promising approach to software verification [1],
                                        but its application to verify and refute properties in large code bases is limited by the re-
                                        source requirements of the technique [2]. This happens when BMC techniques unwind
                                        all loops and recursive functions up to their given maximum bound or completeness
                                        threshold [3], which is typically infeasible for checking realistic programs.
                                             In contrast, a variant called k-induction applied to unbounded programs uses BMC
                                        as a “component” to prove partial correctness [4]; it has been successfully combined
                                        with continuously-refined invariants [5] and to prove that ANSI-C programs do not
                                        contain data races [6,7] or that design-time constraints are respected [8]. Additionally,
                                        k-induction is a well-established technique in hardware verification, where it is applied
                                        due to the transition relation present in hardware designs [8,9,10]. Although we can
                                        prove partial correctness via induction without fully unwinding a program, state-of-
                                        the-art k-induction procedures still waste time and resources to falsify properties in
                                        programs since they unwind loops and recursion up to the depth that exposes a bug.
                                             Here we describe and evaluate a bidirectional k-induction (bkind) algorithm, which
                                        is an extension of the original k-induction [10] that improves its bug-finding capabili-
                                        ties, reducing the number of iterations to find a property violation in half. In practice,
the bkind algorithm performs a bidirectional search for bugs in the program state space
to quickly refute properties. Given the current knowledge in software model check-
ing, our extension has not previously been described or evaluated in the literature,
but we have already provided preliminary results of this approach on a limited num-
ber of small benchmarks [11]. Similar techniques do exist, however, in other domains:
Bischoff et al. [12] describe a technique called “target enlargement” which combines
binary decisions diagrams (BDDs) and Boolean Satisfiability (SAT) solvers to reduce
the time to find property violations in hardware verification, and Bradley et al. intro-
duced “property-directed reachability” (or IC3) procedure for safety verification of sys-
tems [13] and have shown that IC3 can scale on certain benchmarks, where k-induction
fails to succeed. Jovanović et al. [14] describe a technique called “Property-Directed
k-induction” to generate stronger invariants for programs written in the SALLY input
language.
    In summary, this paper makes the following original contributions. Firstly, we ex-
ploit the counterexamples generated by the k-induction proof rule to derive new prop-
erties and feed them back to the BMC procedure. Secondly, we combine an interval
invariant generator and bkind to significantly improve the number of correct verifica-
tion results. Lastly, our experimental results show that bkind can considerably reduce
the verification time compared to the naı̈ve k-induction proof rule, since it only requires
half the number of steps to find a given safety property violation in an unsafe program.
Compared to other state-of-the-art k-induction verifier (2LS), bkind produces more than
twice correct proofs and about 35% more correct alarms, when analysing a large set of
public available benchmarks.


2      Naı̈ve k-Induction Proof Rule

The first version of the k-induction proof rule was proposed by Sheeran et al. [10]. They
used BMC algorithms to prove correctness by induction. Consider a program P with a
loop and a safety property φ(s). BMC algorithms can only show that no counterexample
exists for a k loop unwindings but not that longer counterexamples do not exist1 . The
k-induction proof rule tries to prove by induction that if φ holds for any given iteration
through the loop then φ holds for the next iteration. In particular, the base case tries to
find a counterexample where φ does not hold and the inductive step tries to prove that
there exists no counterexamples. k-induction extends induction by assuming the safety
property k − 1 times before checking its satisfiability [5], as described in Eq. 1.
                 k−1                  k−1
                                                        !            !!
                 ^                    ^
                       φ(i) ∧ ∀n :           φ(n + i)       ⇒ φ(n + k)    ⇒ ∀n : φ(n).            (1)
                 i=0                   i=0

    Since k-induction assumes the safety property φ more than once, a less general case
is checked after each iteration, thus it is more likely to succeed [16]. In a previous
work [17,18], we extended the k-induction proof rule to check program completeness
in a separate step and defined it as an iterative deepening algorithm [19], consisting of
three independent checks: base case, forward condition and inductive step.
 1
     Note that Craig interpolants can be used to exploit the SAT/SMT solvers’ ability to produce
     refutations, i.e., proofs that there is no counterexample of depth less than or equal to k [15].
    We describe the algorithms in this paper by assuming that a given program P under
verification is a state transition system M . In M , a state s ∈ S is a tuple (m, c), where
m is the state variable data, c is the state constraint data. A predicate initP (s) denotes
that s is an initial state, trp (si , sj ) ∈ T is a transition relation from si to sj , φ(s) is the
formula encoding for states satisfying a safety property, and ψ(s) is the formula encod-
ing for states satisfying a completeness threshold [3], which is equal to the maximum
number of loop iterations occurring in P . For convenience, we define an error state ,
reachable if there is a property violation in the program P . A counterexample π k is a
sequence of states of length k from the initial state s1 to .

  Algorithm 1.1: The base case.
  1   Function base case(P ):
          if initP (s1 ) ∧ j−1
                            V                          Wj
  2                             i=1 trP (si , si+1 ) ∧  i=1 ¬φ(si ) then
  3             Let  = si such that ¬φ(si );
  4             return [s1 , . . . , ];
  5       else
  6             return ∅;
  7       end


Lemma 1 (Base case). If the function base case(P) returns a sequence of states,
then the program is unsafe and the sequence of states is a counterexample.
     Proof. The execution path returned in line 4 of the Algorithm 1.1 is a counterex-
ample since it is an execution path (ensured by the transition relation trP in line 2)
that starts with the first state of the program (ensured by initP (s1) in line 2) and ends
with an error state (in line 3); this follows the definition of a counterexample. This is
also a non-spurious counterexample because the base case is a precise check: it encodes
all reachable states up to k and checks for satisfiability. If the base case returns a real
counterexample then the program is unsafe.

  Algorithm 1.2: The forward condition.
  1   Function forward condition(P ):
          if initP (s1 ) ∧ j−1
                            V
  2                             i=1 trP (si , si+1 ) ∧ ¬ψ(sj ) then
  3             return [s1 , . . . , sj ];
  4       else
  5             return ∅;
  6       end


Lemma 2 (Forward condition). If the function forward condition(P) returns
an empty sequence of states then the program is safe.
    Proof. The forward condition checks if the completeness threshold was reached in
current unwound program P , i.e., all loops were completely unwound. This is encoded
as the completeness threshold property check in line 2 of Algorithm 1.2. In practice,
these checks are encoded as unwinding assertions and they check if the termination
condition of all loops are satisfiable for the current number of unwindings. This step can
prove partial correctness if the base case did not find any bug for the current unwinding
since no safety property is checked. We guarantee this precedence in k-induction by
checking the base case before checking the forward condition. We conclude that if no
bug was found by the base case and the completeness threshold holds for the current
number of unwindings, all states were explored and the program is safe.
  Algorithm 1.3: The inductive step.
  1   Function inductive step(P ):
          if ∃n ∈ N+ . n+j−1
                        V
  2                       i=n         (φ(si ) ∧ trP (si , si+1 )) ∧ ¬φ(sn+j ) then
  3             Let  = sn+j such that ¬φ(sn+j );
  4             return [sn , . . . , ];
  5       else
  6             return ∅;
  7       end


Lemma 3 (Inductive step). If the function inductive step(P) returns an empty
sequence of states, then the program is safe.

    Proof. Similarly to the forward condition check, the program is safe up to k loop
unwindings because the base case did not find any reachable error state. This is guar-
anteed in the k-induction proof rule by running the base case before the inductive step.
The inductive step then tries to find any counterexample of length k in the state space
by first assuming that there was no property violation in k − 1 iterations. The inductive
step over-approximates the state space so if no counterexample is found then this is
sufficient to prove that there is no reachable bug in the program.

  Algorithm 1.4: Naı̈ve k-induction.
  1   Function kind(P , kmax , k):
  2       if k > kmax then return unknown;
  3        Pk := unwinding(P, k);
  4        π := base case(Pk );
  5       if π 6= ∅ then return π;
  6        π := forward condition(Pk );
  7       if π = ∅ then return ∅;
  8        π := inductive step(Pk );
  9       if π = ∅ then return ∅;
 10        return kind(P, kmax , k + 1);


     The naı̈ve version of the k-induction proof rule (shown in Algorithm 1.4) tries to find
a property violation or to prove partial correctness for an increasing number of k loop
unwindings. The pre-condition of the algorithm is k = 1. The unwinding function
unwinds the program P , k times; the function preserves the program behaviour up to k
loop unwindings; if a bug in P is reachable in k unwindings, it will be reachable in Pk .
If it reaches a maximum number of iterations kmax , the algorithm terminates with an
unknown answer.

Theorem 1 (Soundness of the k-induction proof rule). If the k-induction proof rule
returns: (i) a sequence of states [si , . . . , sj ]: the program is unsafe and the sequence is
a non-spurious counterexample; (ii) ∅: the program is safe; (iii) unknown: the program
is safe up to kmax iterations.

    Proof. The first item is ensured by Lemma 1, if there is a property violation reach-
able after k unwindings, the program is unsafe and the algorithm terminates returning
the counterexample (line 5). The second item is ensured by Lemmas 2 and 3, if no coun-
terexample is found then the program is safe and an empty execution path is returned
in lines 7 and 9. Finally, the third item is ensured in line 2, if the algorithm reached
the maximum number of defined iterations without terminating, an unknown answer
is given. We can then conclude that the k-induction proof rule always terminates ei-
ther with a counterexample (if the program is unsafe), an empty execution path (if the
program is safe), or with an unknown answer otherwise.

Theorem 2 (Partial completeness of the k-induction algorithm). If ∃ k : 1 ≤ k ≤
                                                k
kmax such that the shortest counterexample is πmin   = [s1 , . . . , sk ] and sk =  then the
k-induction proof rule will find the counterexample in at least k iterations.

    Proof. This is ensured by always starting the k-induction algorithm as defined in
Algorithm 1.4 with one loop unwinding; it always increments the number of loop un-
windings by one (line 10). Furthermore, if the program is unsafe, neither the forward
condition nor the inductive step will terminate the verification before the counterex-
ample is found. Also note that, if a property violation requires zero loop unwindings
(e.g., a property violation before a loop), the k-induction proof rule will still unwind the
program once but the base case will find the property violation since it checks all states
reachable with one loop unwinding (line 2).


2.1   Why is the k-induction proof rule naı̈ve?

The inductive step assumption of all possible sequences of k iterations is what makes
the k-induction proof rule naı̈ve; these sequences often include large unreachable re-
gions of the state space. Safety properties might not hold in these regions of the state
space but they are irrelevant for the safety of the program. For example, when verify-
ing the safe program in Fig. 1a using k-induction, the inductive step will try to prove
that the program is safe for all possible values that both input and s variables can
assume; this will result in a series of spurious counterexamples since these variables
only assume a small range of values. In fact, the version of the k-induction proof rule as
presented in Algorithm 1.4 assumes that all counterexamples produced by the inductive
step are spurious, even if they are not.
    Let us use an illustrative example to show the verification process using k-induction.
First, consider the safe program in Fig. 1a. The property violation is reachable if the
transition condition [input = 5 ∧ s > 5] holds and, since the state space is over-
approximated, there are several states that will satisfy this condition. In this case, the
k-induction as defined in Algorithm 1.4 will eventually reach the maximum number of
loop unwindings and terminate with an unknown answer because the base case will not
find a property violation (the program is safe), the completeness threshold will never
be reached since the program contains an infinite loop and the inductive step will keep
finding spurious counterexamples. Now, let us consider the unsafe program in Fig. 1b.
The k-induction as defined in Algorithm 1.4 will need at least five iterations until a
counterexample is found by the base case. During these iterations, both the forward
condition and the inductive step are executed and any reasoning performed in these steps
are discarded but what if the inductive step finds an actual partial counterexample?
This useful information (a partial counterexample) is ignored as all counterexamples
found by the inductive step are assumed to be spurious.
    When using the naı̈ve k-induction to verify the programs in Fig. 1, it will either
produce an unknown result or will discard useful information.
 1   unsigned i n t s = 1 ;                                1   unsigned i n t s = 1 ;
 2   i n t main ( ) {                                      2   i n t main ( ) {
 3       while ( 1 ) {                                     3       while ( 1 ) {
 4         unsigned i n t i n p u t =                      4         unsigned i n t i n p u t =
                     VERIFIER nondet int ( ) ;                                 VERIFIER nondet int ( ) ;
 5         i f ( input > 5) {                              5         i f ( input > 5) {
 6            return 0;                                    6            return 0;
 7         } e l s e i f ( i n p u t == 1 && s == 1 ) {    7         } e l s e i f ( i n p u t == 1 && s == 1 )   {
 8            s = 2;                                       8            s = 2;
 9         } e l s e i f ( i n p u t == 2 && s == 2 ) {    9         } e l s e i f ( i n p u t == 2 && s == 2 )   {
10            s = 3;                                      10            s = 3;
11         } e l s e i f ( i n p u t == 3 && s == 3 ) {   11         } e l s e i f ( i n p u t == 3 && s == 3 )   {
12            s = 4;                                      12            s = 4;
13         } e l s e i f ( i n p u t == 4 && s == 4 ) {   13         } e l s e i f ( i n p u t == 4 && s == 4 )   {
14            s = 5;                                      14            s = 5;
15         } e l s e i f ( i n p u t == 5 && s > 5 ) {    15         } e l s e i f ( i n p u t == 5 && s >= 5 )   {
16            // unsatisfiable                            16            // satisfiable
17            / / property violation                      17            / / property violation
18               VERIFIER error ( ) ;                     18               VERIFIER error ( ) ;
19         }                                              19         }
20      }                                                 20      }
21   }                                                    21   }


              (a) Simplified safe program.                             (b) Simplified unsafe program.

     Fig. 1: Simplified illustrative examples extracted from SV-COMP’18 encoding an
     event-condition-action (ECA) system [20]. The program in Fig. 1a is safe since the
     property violation is unreachable while the program in Fig. 1b is unsafe since the prop-
     erty violation is reachable after at least 5 iterations.


     3     Learning from Counterexamples to Bidirectionally Explore the
           State Space
     The k-induction proof rule can be applied to solve various verification problems [6,7,8],
     but it can be further improved by taking advantage of two important observations: (1)
     partial counterexamples are ignored: useful counterexamples may be generated by the
     inductive step and they are ignored by the algorithm; (2) unconstrained state space: the
     inductive step may find spurious counterexamples if the over-approximation is uncon-
     strained. Several authors address the later by generating program invariants to rule out
     unreachable regions of the state space, either as a pre-processing step where invariants
     are introduced in the program before [21,22] or during the verification [5,23,24]. Our
     algorithm is the first to address the former in the context of software verification.

     3.1    Bidirectional bug-finding using k-induction
     The bkind algorithm extends the bug-finding capabilities of the k-induction proof rule
     by performing two alternating bug searches, one forward (i.e., from the initial state s1 )
     and one backward (i.e., from any error state ) and stopping if the forward search finds
     a state in a counterexample produced by the backward search. Our proposed algorithm
     is similar to the bidirectional search algorithm from the graph theory field [25]. This
     new algorithm relies on two checks from the k-induction proof rule to implement the
     searches. The base case is the forward search, since it tries to find a counterexample
     π k = [s1 , . . . , ], while the inductive step is the backward search and tries to find any
partial counterexample π k = [si , . . . , ]. We shall refer to the base case and inductive
step as forward and backward searches, respectively.
    To perform the forward search we need to extend the base case as shown in Al-
gorithm 1.5. First we define a new function starts counterexample that given
a state s and a counterexample π, returns true if s ∈ π otherwise returns f alse; this
function will be used to perform the bidirectional search. The first condition in the new
algorithm (line 10) is the same condition in the base case from the original k-induction
proof rule and returns a counterexample if a bug was found in k iterations. The second
(and new) condition (line 13) uses the function starts counterexample to check
if any of the states reachable by the base case start the counterexample πback found
by the backward search. If this holds, the new base case function returns the execution
path found by the forward search concatenated with the counterexample found by the
backward search (line 14). The “·” operator concatenates two sequences. If no bug is
found, the algorithm returns an empty sequence.


  Algorithm 1.5: The base case used in the bkind algorithm.
  1   Function starts counterexample(s, π):
  2       if π 6= ∅ ∧ s ∈ π then
  3             return true;
  4       else
  5             return false;
  6       end
  7
  8   Function bkind base case(P , πback ):
                                   Vj−1
  9       BC := initP (s1 ) ∧ i=1         trP (si , si+1 );
                   Wj
 10       if BC ∧ i=1 ¬φ(si )) then
 11             Let  = si such that ¬φ(si );
 12             return [s1 , . . . , ];
 13       else if BC ∧ ∃ i : 1 ≤ i ≤ k ∧ starts counterexample(si , πback ) then
 14             return [s1 , . . . , si − 1] · πback ;
 15       else
 16             return ∅;
 17       end




Lemma 4 (Base case). If Algorithm 1.5 returns a sequence of states [si , . . . , sj ], this
is a non-spurious counterexample.


    Proof. The first condition in the new base case (line 10) is identical to the condition
in the original base case and Lemma 1 ensures that this is a real counterexample. We
only need to prove that the execution path returned in line 14 is a counterexample.
The returned sequence is a counterexample since it is a concatenation of an execution
path starting from the initial state in the state space with a counterexample. We know
that the sequence of states in the concatenation is an execution path because of the
transition relation and initP (s1 ) ensures that it starts from the initial state in the state
space (both in line 9). Lemma 5 guarantees that πback is a partial counterexample.
Finally, this is a non-spurious counterexample because of the partial order property of
the state space: this is sufficient to allow the concatenation of the execution path and
the counterexample.
  Algorithm 1.6: The bkind algorithm.
  1   Function bkind(P , kmax , k, πback ):
  2       if k > kmax then return unknown;
  3        Pk := unwinding(P, k);
  4        π := bkind base case(Pk , πback );
  5       if π 6= ∅ then return π;
  6        π := forward condition(Pk );
  7       if π = ∅ then return ∅;
  8        π := inductive step(Pk );
  9       if π = ∅ then return ∅;
 10        return bkind(P, kmax , k + 1, π);

     The bkind algorithm is shown in Algorithm 1.6. Similarly to the naı̈ve k-induction
algorithm, the bkind algorithm tries to either find a property violation or to prove par-
tial correctness for an increasing number of k unwindings. The pre-conditions of the
algorithm are π = ∅ and k = 1. If it reaches a maximum number of iterations kmax ,
the algorithm terminates with an unknown answer. The novel contribution in the new
bkind algorithm is the bidirectional bug-finding technique. We use the counterexample
produced by the backward search in the previous iteration, and check if it is reachable
by the forward search in the next iteration (line 4).
Lemma 5 (Partial counterexample from the inductive step). If Algorithm 1.3 re-
turns a sequence of states [si , . . . , sj ], this is a partial counterexample of length k.
Proof. This is a partial counterexample because it is an execution path (the transition
relation in line 2 ensures that) and the last state in the path is an error state (ensured
in line 3). Finally, the counterexample has length k because the inductive step always
tries to find a counterexample of length k; this is performed by checking if the property
violation is reachable in k iterations, assuming that it holds for k − 1 iterations.
Theorem 3 (Partial completeness of the bkind algorithm). If ∃ k : 1 ≤ k ≤ kmax
                                             k
such that the shortest counterexample is πmin    = [s1 , . . . , sk ] and sk =  then the
k-induction proof rule will find the counterexample in at least b k2 c + 1 iterations.
    Proof. In order to prove this theorem, we assume that the inductive step always
returns the same non-spurious partial counterexample for every k; we will show how to
give partial guarantees to this assumption in Sec. 3.2.
    First, we show that no more than b k2 c + 1 iterations are required to find a property
violation. By contradiction, assume that the number of iterations required to find the
property violation is greater than b k2 c + 1.
                       k
    Let us assume a πmin     where k is even. In the iteration k2 , the new base case will
have explored all states up to k2 and the inductive step will have provided a partial
                        k
counterexample πback
                 2
                     . In the iteration k2 + 1, the new base case will not reach any state
       k
in πback
     2
         if either the counterexample πback is spurious (i.e., contradicting our initial
assumption) or the counterexample πback is not spurious and there is at least one state
                                                               k
       k               k                                           +1
su ∈ πmin  such that πmin  = [s1 , . . . , s k +1 ]·[su , . . .]·πback
                                                                   2
                                                                       , which has a length greater
                                             2
                                                                     k
than k contradicting our assumption about the length of πmin .
                      k
    Now, assume a πmin    where k is odd. The proof is similar to the one where k is
even, except that we consider the sequences at iteration k−1          2 . If the counterexample is
not found in the iteration k−12 +1, then either the counterexample is spurious or a greater
number of iterations is required to find the property violation, contradicting our initial
assumptions. We then generalize and conclude that no more than b k2 c + 1 iterations are
required to find a property violation.
    Now we show that at least b k2 c + 1 iterations are required to find a property viola-
tion. By contradiction, assume that the number of iterations required to find the property
violation is less than b k2 c + 1. This means that either there exists a smaller counterex-
ample that was not found the base case, which violates Lemma 4, or there is a state
        k                 k
sv ∈ πmin    such that πmin    = [s1 , . . . , sv ] · [sv+1 , . . . , sk ] which has a length smaller
than k contradicting our assumption about the length of πmin           k
                                                                           . Given that at least b k2 c+1
iterations are needed to find the property violation and no more than b k2 c + 1 iterations
are needed to find the property violation, we can conclude that the bkind algorithm will
find a counterexample πmin  k
                                in exactly b k2 c + 1 iterations.
Theorem 4 (Soundness of the bkind algorithm). If the bkind algorithm returns: (i)
a sequence of states [si , . . . , sj ]: the program is unsafe and the sequence is a non-
spurious counterexample; (ii) ∅: the program is safe; (iii) unknown: the program is safe
up to kmax iterations.
    Proof. The proof follows the same proof as the Theorem 2, except that the first item
is ensured by Lemma 4 instead of Lemma 1.

3.2     Constraint Generation Using Interval Analysis
Here we use invariants to constraint the state and rule out unreachable states evaluated
by the inductive step [5,22,23,24]. Fig. 2 shows an example of the usage of invariants
(dashed line) to constraint the state space. The invariants reduce the number of states
explored by the backward search by constraining the over-approximation. Similarly to
Rocha et al. [22], we perform a static program analysis prior to loop unwinding and
estimate the intervals that a variable can assume. In contrast to Rocha et al., we do
not rely on external tools and implement the invariant generation as a pre-processing
step of the verification. In particular, we use the abstract interpretation component from
CProver [26]. The invariant generation algorithm uses an abstract domain based on
expressions over intervals, such that every constraint c in a state s is a map var →
2128 × 2128 that maps interval constraints to every variable var.
    In order to use the invariants, we need to extend the inductive step as shown in Al-
gorithm 1.7. The algorithm is similar to the inductive step as defined in Algorithm 1.3,
but it now takes an extra argument: a set of invariants ϕ. These invariants will constraint
the state space and filter unreachable states from the inductive step check, thus reducing
the number of spurious path that might be explored.

  Algorithm 1.7: The new inductive step with invariants.
  1   Function inductive step invariants(P , ϕ):
          if ∃n ∈ N+ . ϕ(sn ) n+j−1
                                   V
  2                                   i=n (φ(si ) ∧ trP (si , si+1 )) ∧ ¬φ(sn+j ) then
  3             Let  = sn+j such that ¬φ(sn+j );
  4             return [sn , . . . , ];
  5       else
  6             return ∅;
  7       end
                                                  𝑠"




                  ϵ
               Spurious
            counterexample



                                                                           ϵ
                                                                    Spurious counterexample
                             ϵ
                                           Reachable state space
                 Spurious counterexample


Fig. 2: Visual representation of the state space of a program, where the states inside
the dashed line are the reachable states and the ones outside are unreachable states.
An unconstrained over-approximation of the program assumes that all the states are
reachable which might contain spurious counterexamples (counterexamples that lead
to unreachable error states). An invariant is a filter of states: a strong enough invariant
will remove unreachable error states from reasoning, allowing the inductive step to
prove the program correctness or to find non-spurious partial counterexamples.


Lemma 6 (Inductive step with invariants). If inductive step invariants(P)
returns an empty sequence of states the program is safe.
    Proof. This follows the same reasoning of the Lemma 3. The program is safe up to k
iterations because the base case did not find any property violation and that the inductive
step over-approximates the state space when it tries to find a property violation. The new
inductive step with invariants will constraint the over-approximation to be closer to the
reachable state space of the program. Lemma 6 ensures that the k-induction proof rule
can use the new inductive step with invariants. Theorem 1 must change if invariants are
used to prove partial correctness; Lemmas 2 and 6 ensure the theorem is sound.
Lemma 7 (Partial counterexample from the inductive step with invariants). If Al-
gorithm 1.7 returns a sequence of states [si , . . . , sj ], this is a partial counterexample of
length k.
    Proof. This follows the same reasoning of the Lemma 5. We know this is a coun-
terexample because of the sequence of transitions defined by trP and that the last state is
an error state. Again, the invariants here will only constraint the state space so the over-
approximation is closer to the set of reachable states of the program. The Lemma 7
is defined so the new inductive step with invariants can be used with the bkind algo-
rithm. Theorem 4 needs to be changed if invariants are used to prove correctness to use
Lemma 7 instead of Lemma 3.
 3.3   Why is the bkind algorithm more efficient than k-induction?

 First, consider that we wish to verify the safe program in Fig. 1a using the bkind algo-
 rithm. The state transition system is analyzed and the following intervals are estimated
 based on the assignments: ϕ = (input ≥ 0, input ≤ UINT MAX, s ≥ 1, s ≤ 5).
 The invariants are introduced in the program and are sufficient to prove that the pro-
 gram is safe safe with two loop unwindings: there will be no counterexample of size
 two that leads to a property violation. Now, consider that we wish to verify the unsafe
 program in Fig. 1b. Here, the same set of constraints are introduced in the program but
 now the inductive step will find a counterexample that satisfies input ≥ 0 ∧ input ≤
 UINT MAX ∧ s ≥ 1 ∧ s ≤ 5 ∧ input = 5 ∧ s ≥ 5, which is input = 5 ∧ s = 5. This
 is the program state prior to the error state; the reachability of this state is introduced
 in the program as a new property and checked in the base case. This is then extended
 further back for every loop iteration, effectively performing the backward search. In
 conclusion, bkind can correctly verify both programs in Fig. 1: the program in Fig. 1a
 can be proven to be safe and the program in Fig. 1b requires fewer number of steps to
 find the property violation.


 4     Experimental Evaluation
 The experimental evaluation of the bkind algorithm and the invariant generation in our
 software model checker (ESBMC [27,28]) consists of three parts. In Sec. 4.1, we de-
 scribe the experimental objectives and present the benchmarks used to evaluate the
 bkind algorithm. In Sec. 4.2 we compare our bkind algorithm and the invariant genera-
 tion with the naı̈ve k-induction, while in Sec. 4.3 we compare the bkind algorithm with
 invariants against another state-of-the-art BMC tool that uses k-induction and invariant
 generation to verify ANSI-C programs, 2LS [23]. The tools are compared in terms of
 number of refuted bugs and verification time. We provide a virtual machine with all the
 binaries and scripts to reproduce our results in www.esbmc.org.


 4.1   Experimental Objectives and Setup
 Our experimental evaluation aims to answer three research questions:

RQ1 (soundness) Does our approach provide correct results?
RQ2 (performance I) Does our approach improve results compared to the naı̈ve k-induction?
RQ3 (performance II) How does our approach compare against other k-induction verifiers?

      We use 5591 benchmarks from SV-COMP’18 to evaluate the algorithms described in this
 paper. The benchmarks were extracted from the subcategories Arrays, BitVectors, ControlFlow,
 ECA, Floats, Heap, Loops, ProductLines, Sequentialized and Systems DeviceDriversLinux64.
 The remaining categories were excluded because they use features that our k-induction does not
 support (e.g., termination, recursion, and concurrency). When verifying those programs, ESBMC
 disables the inductive step and uses only the base case and the forward condition, thus they are
 not included here. Out of the 5591 benchmarks, 4134 are safe while 1457 are unsafe programs.
      All experiments were conducted on IRIDIS4, the supercomputer from the University of
 Southampton [29]. The computer nodes used are equipped with Intel Sandybridge processors
 running at 2.6GHz and 24GB of RAM. We used Boolector as the SMT backend for all the ver-
 ification tasks. For each benchmark, we set time and memory limits of 900 seconds and 15GB,
respectively, as per the competition definitions. Finally, given the large amount of data involved
in the experiments, we used four groups to present the results: Correct proofs is the number of
correct positive results (i.e., the tool reports SAFE correctly), Correct alarms is the number of
correct negative results (i.e., the tool reports UNSAFE correctly), Incorrect proofs is the num-
ber of incorrect positive results (i.e., the tool reports SAFE incorrectly), Incorrect alarms is the
number of incorrect false results (i.e., the tool reports UNSAFE incorrectly).


4.2       Comparison of k-induction-based approaches
Here, we evaluate five different k-induction proof rules: “original naı̈ve k-induction” (the first
version implemented in ESBMC [18]), “naı̈ve k-induction” (the k-induction proof rule described
in Sec. 2), “naı̈ve k-induction + invariants” (the k-induction algorithm described in Sec. 2 and the
invariants described in Sec. 3.2), “bkind” (the bkind algorithm described in Sec. 3.1) and “bkind
+ invariants” (the bkind algorithm described in Sec. 3.1 and the invariants described in Sec. 3.2).


 2500




 2000




 1500


                         2311          2305
                  2158          2148
 1000
           1630


  500
                                                     841 827 836 832
                                               684

                                                                            118    10   38    10     38      57    5     5     8     11
      0
                  Correct proofs                     Correct alarms               Incorrect proofs                Incorrect alarms
           Original naïve k-induction         naïve k-induction   naïve k-induction + invariants     bkind    bkind + invariants


Fig. 3: Results of the k-induction-based algorithms in ESBMC for all SV-COMP’18
benchmarks with different configurations.


    Fig. 3 shows the results of using the k-induction-based approaches to verify the benchmarks
from SV-COMP. First, let us compare the results of the original naı̈ve k-induction [18] and the
current naı̈ve k-induction: the number of correct proofs and correct alarms increased by 25% and
20%, respectively, while the number of incorrect proofs and incorrect alarms decreased by 91%
and 92%, respectively. Most of the wrong results in the original k-induction came from the fact
the original algorithm (1) could not reason about early loop exits (e.g., a break inside a loop)
and (2) would assume wrong safety conditions in the inductive step due to implementation bugs.
Furthermore, the original k-induction did not support floating-point encoding which resulted in
45 incorrect alarms in the Floats category and did not have the clang frontend, thus it could not
verify about 500 benchmarks due to parsing errors.
    Now let us compare the current k-induction proof rule against the new bkind algorithm (with
and without invariants). First, we notice that the invariants increase the number of correct proofs
for both the k-induction and bkind in about 7%. This, however, comes at a cost: due to bugs in
our implementation, the number of incorrect proofs are almost 4 times higher when invariants
are used in combination with the algorithms (from 10 to 38). In particular, our algorithm does
not track intervals of variables changed through pointers and neither if the intervals are defined
in terms of other variables. The number of incorrect results, however, is still low: we only report
incorrect proofs in about 2.5% of the 1457 incorrect benchmarks.
     Note that all the approaches report similar correct alarms with or without invariants; this
is expected in the k-induction proof rule since the invariants are supposed to only improve the
correctness proof. The bkind verification results could have found a larger number of bugs than
the k-induction proof rule. Indeed, bkind finds bugs in benchmarks that could not be found by the
k-induction algorithm but in the end it reported a slightly fewer number of correct alarms and a
larger number of incorrect alarms. An in-depth analysis of the wrong results showed that (1) when
the invariants are incorrect, the bkind algorithm ends up finding an incorrect counterexample
and (2) when the program contains arrays, the algorithm ends up generating incomplete partial
counterexamples, which also lead to incorrect alarms. Despite the number of incorrect results,
however, the wrong alarms only amount to 0.1% of the 4134 correct benchmarks analysed by the
k-induction approaches. These numbers allow us to partially affirm our research question RQ1:
the new bkind algorithm provides correct results for a large set of benchmarks. There are some
programs where bkind will provide incorrect results but it is due to bugs in our implementation.
     The total verification time is 1, 253, 015s for “original naı̈ve k-induction”, 1, 654, 147s for
“naı̈ve k-induction”, 1, 522, 851s for “naı̈ve k-induction + invariants”, 1, 664, 357s for “bkind”,
and 1, 504, 208s for “bkind + invariants”. First, let us evaluate the original and the current naı̈ve
k-induction: the original one is 25% faster the current k-induction; this can be easily explained
due to the limitations in the program: a number of benchmarks are not parsed by the tool and
the greater number of incorrect results allow the original k-induction to finish the analysis faster.
Regarding the k-induction and bkind without invariants, the latter is slightly slower (0.6%): this is
expected since the inductive step is most likely to find spurious counterexamples. The slowdown
in bkind is the impact of introducing spurious verification conditions and it is negligible.
     The results when invariants are used, however, are much better. The verification time de-
creases considerably in these benchmarks, making both algorithms 10% faster. The naı̈ve k-
induction algorithm takes 1, 654, 147s to verify all the programs which is equivalent to 19.1
days of continuous processing, while the bkind algorithm with invariants takes 1, 504, 208s or
17.4 days. The bkind algorithm with invariants speeds up the verification by almost two full days
in our experiments. These results allow us to affirm our RQ2: the bkind algorithm with invariants
improves the performance over the naı̈ve k-induction by giving more correct results in less time.


4.3   Comparison to a state-of-the-art k-induction verifier 2LS
We now compare the bkind algorithm with invariants against 2LS v0.6.0, another state-of-the-
art bounded model checker with support for k-induction. In particular, 2LS uses the kIkI algo-
rithm [23] and combines the k-induction proof rule with continuous invariant generation. We
used the same configuration from SV-COMP’18 in which 2LS is configured to generated interval
constraints similar to the ones generated by ESBMC.
     As shown in Fig. 4, ESBMC with the bkind algorithm and invariants produces more than two
times the number of correct proofs and about 35% more correct alarms compared to 2LS when
analysing the same set of benchmarks. An in-depth analysis of the results show that 2LS aborts
the verification of various benchmarks in the Systems DeviceDriversLinux64 category with the
message “Irreducible control flow not supported”. Alternatively, ESBMC is able to prove the
correctness of 1249 benchmarks in this category, greatly improving our results. 2LS provides
much fewer incorrect results when compared to ESBMC in this set of benchmarks. 2LS always
had a strong focus in invariant generation since its first version; their last version in SV-COMP18
2500




2000




1500


             2305
1000




 500                1031
                                     832
                                            615

                                                                   38      3          11      4
    0
            Correct proofs         Correct alarms               Incorrect proofs   Incorrect alarms
                                           bkind + invariants   2LS


         Fig. 4: Results of ESBMC with bkind algorithm with invariants and 2LS.


extended it even further by introducing invariant generation for termination proofs and pointer
safety. The invariant generation in ESBMC is still in its first version and needs improvements.
     The total verification time is 1, 266, 890s for 2LS and 1, 504, 208s for ESBMC with “bkind
+ invariants”. Here, 2LS is about 15% faster than ESBMC even if we do not consider the Sys-
tems DeviceDriversLinux64 category where 2LS would abort early in the verification. In particu-
lar, 2LS was more than 10 times faster in two categories, Arrays and Heap, most likely due to the
stronger invariants generated by the tool which allowed it to prove correctness faster; ESBMC
would simply run out of time in a large number of benchmarks in these categories. ESBMC with
bkind and invariants is not the fastest verification tool using k-induction but it is the one with the
highest number of correct results. These results allow us to answer the RQ3: our novel contribu-
tion is a improvement over the state-of-the-art verification using k-induction, which can report
more correct results for a large number of different benchmarks than other existing approaches.


5       Related Work
The k-induction method is gaining popularity in the software verification community. Donald-
son et al. described a verification tool called Scratch to detect data races during Direct Memory
Access (DMA) in the CELL BE processor from IBM [7], using k-induction. Properties are auto-
matically inserted in the program to model the behaviour of the memory control-flow and the al-
gorithm tries to find violation of those properties or prove that they hold indefinitely. The method
also requires the code to be manually annotated with loop invariants, whereas our approach au-
tomatically generates and adds them to the program. Finally, the tool is able to prove the absence
of data races, but it is restricted to verify that specific class of problems for a particular type of
hardware, while our approach is evaluated over a more general class of programs.
     Donaldson further described two tools for proving correctness of programs: K-Boogie and
K-Inductor [6]. The former is an extension of the Boogie language, aimed to prove correctness
(using k-induction) of programs written in a number of languages (e.g., Boogie and Spec), while
the latter is a BMC tool for C programs. Both K-Boogie and K-Inductor use a k-induction proof
rule; the completeness threshold is not separately checked and relies only on the inductive step to
prove correctness. Their k-induction has a pre-processing step, but while we introduce invariants
during the pre-processing, their approach removes all nested loops leaving only non-nested loops.
They compare the results of K-inductor with Scratch and show that the new approach maintains
the same number of correctly verified programs while being faster. Similar to the prior work [7],
the programs need to be manually changed to add loop invariants while we do it automatically.
     Malı́k et al. [23] describe 2LS, a C/C++ SAT-based BMC. 2LS is a tool developed using
the CProver framework [30] and combines a k-induction proof rule with abstract interpretation
(AI). As CBMC [30], 2LS uses SAT solvers but instead of a fixed unwind approach, 2LS uses an
incremental BMC approach, where it first checks for property violations for a given bound, then
tries to generate (and refine) invariants using AI and then builds a proof using k-induction. Their
k-induction, called kIkI [24], is similar to the one implemented in ESBMC, but adds an extra
step to generate and refine invariants. In contrast to our invariant generation that only supports
interval domains, 2LS supports several abstract domains for numerical values and a shape domain
for pointers. 2LS offers approaches to prove non-termination, while ESBMC has no algorithm to
prove non-termination and can only prove termination by checking the unwinding assertions.
     Bischoff et al. [12] propose a methodology to use BDDs and SAT solvers for the verification
of programs in a bidirectional form similar to our bkind algorithm. In their work, they refer to
the technique as target enlargement: the property violation is “enlarged” by checking if the states
around the property violation are reachable. The BDDs are responsible for the target enlargement,
collecting the under-approximate reachable state sets, followed by the SAT-based verification
with the newly computed sets. They implemented the technique in the Intel BOolean VErifier
and showed that the verification time of a set of public benchmarks was up to five times smaller.
Compared to this work, we only use k-induction and SMT solvers; the inductive step in the k-
induction is responsible for enlarging the target and the SMT solver checks for satisfiability.
     Jovanović et al. [14] present a reformulation of IC3, separating the reachability checking
from the inductive reasoning. They further replace the regular induction proof rule by the k-
induction and show that it provides more concise invariants. The authors implemented the al-
gorithm in the SALLY model checker using Yices2 to do the forward search and MathSAT5 to
do the backward search. They showed that the new algorithm can solve a number of real-world
benchmarks at least as fast as other approaches. Compared to this work, our bkind uses consecu-
tive BMC calls to find a solution. We implement our approach independent of solvers and it can
be used with any SMT solver supported by ESBMC; both searches are done with the same solver.


6    Conclusions
We have described the k-induction proof rule and a novel contribution that extended its bug-
finding capabilities. The new algorithm, called bidirectional k-induction or bkind, was imple-
mented in ESBMC and evaluated in a large set of benchmarks. k-induction is a powerful veri-
fication technique implemented in several different tools and was successfully used to verify a
large number of different programs and properties. Here, we proposed and evaluated a novel way
to exploit the k-induction proof rule, where useful information can be extracted from the various
checks in the algorithm and can be used to improve the results of the algorithm.
     In particular, the bkind algorithm uses information extracted from the inductive step to shorten
the number of steps required to find a property violation; with strong enough invariants the bkind
algorithm requires roughly half of the number of loop unwindings a BMC algorithm requires
to find a property violation. We have implemented an interval invariant generator that runs as
a pre-processing step: invariants are automatically introduced in the program and, although the
implementation has some bugs, it strengths the bkind algorithm results. Our results show that our
bkind with invariants can considerably reduce the verification time of a large number of bench-
marks: in our experiments this is equivalent to almost two days reduction in the verification time.
                                     References


 [1] Biere, A., Cimatti, A., Clarke, E., Zhu, Y.: Symbolic Model Checking Without BDDs. In:
     Tools And Algorithms For The Construction And Analysis Of Systems. Volume 1633 of
     LNCS. (1999) 193–207
 [2] Beyer, D.: Software Verification With Validation Of Results (Report On SV-COMP 2017).
     In: Tools And Algorithms For The Construction And Analysis Of Systems. Volume 10206
     of LNCS. (2017) 331–349
 [3] Kroening, D., Ouaknine, J., Strichman, O., Wahl, T., Worrell, J.: Linear Completeness
     Thresholds For Bounded Model Checking. In: Computer-Aided Verification. Volume 6806
     of LNCS. (2011) 557–572
 [4] Bradley, A.R., Manna, Z.: The Calculus Of Computation - Decision Procedures With Ap-
     plications To Verification. Springer (2007)
 [5] Beyer, D., Dangl, M., Wendler, P.: Boosting k-Induction With Continuously-Refined In-
     variants. In: Computer-Aided Verification. Volume 9206 of LNCS. (2015) 622–640
 [6] Donaldson, A., Haller, L., Kroening, D., Rümmer, P.: Software Verification Using k-
     Induction. In: Static Analysis Symposium. (2011) 351–368
 [7] Donaldson, A., Kroening, D., Rümmer, P.: SCRATCH: A Tool For Automatic Analysis Of
     DMA Races. In: Symposium On Principles And Practice Of Parallel Programming. (2011)
     311–312
 [8] Eén, N., Sörensson, N.: Temporal Induction By Incremental SAT Solving. Electronic Notes
     in Theoretical Computer Science 89(4) (2003) 543–560
 [9] Große, D., Le, H., Drechsler, R.: Induction-Based Formal Verification Of SystemC TLM
     Designs. In: Workshop On Microprocessor Test And Verification. (2009) 101–106
[10] Sheeran, M., Singh, S., Stålmarck, G.: Checking Safety Properties Using Induction And A
     SAT-Solver. In: Formal Methods In Computer-Aided Design. (2000) 108–125
[11] Gadelha, M.Y.R., Monteiro, F.R., Cordeiro, L.C., Nicole, D.A.: Towards Counterexample-
     guided k-Induction For Fast Bug Detection. In: ACM Joint European Software Engineering
     Conference And Symposium On The Foundations Of Software Engineering. (2018)
[12] Bischoff, G.P., Brace, K.S., Cabodi, G., Nocco, S.and Quer, S.: Exploiting Target En-
     largement And Dynamic Abstraction Within Mixed BDD And SAT Invariant Checking.
     Electronic Notes in Theoretical Computer Science 119(2) (2005) 33–49
[13] Hassan, Z., Bradley, A.R., Somenzi, F.: Better Generalization In IC3. In: Formal Methods
     In Computer-Aided Design, IEEE (2013) 157–164
[14] Jovanović, D., Dutertre, B.: Property-directed k-induction. In: Formal Methods In
     Computer-Aided Design. (2016) 85–92
[15] McMillan, K.L.: Interpolation And Model Checking. In: Handbook Of Model Checking.
     Springer (2018) 421–446
[16] Wahl, T.: The k-induction Principle. http://www.ccs.neu.edu/home/wahl/
     Publications/k-induction.pdf (2013) [Online; accessed September-2018].
[17] Morse, J., Cordeiro, L.C., Nicole, D.A., Fischer, B.: Handling unbounded loops with ES-
     BMC 1.20 - (competition contribution). In: TACAS
[18] Gadelha, M.Y.R., Ismail, H.I., Cordeiro, L.C.: Handling Loops In Bounded Model Check-
     ing Of C Programs Via k-induction. International Journal on Software Tools for Technology
     Transfer 19(1) (2017) 97–114
[19] Russell, S.J., Norvig, P.: Artificial Intelligence: A Modern Approach. 2nd edn. Pearson
     Education (2003)
[20] Cano, J., Delaval, G., Rutten, E.: Coordination Of ECA Rules By Verification And Control.
     In: Coordination Models And Languages, Berlin, Heidelberg, Springer Berlin Heidelberg
     (2014) 33–48
[21] Rocha, H., Ismail, H., Cordeiro, L.C., Barreto, R.S.: Model Checking Embedded C Soft-
     ware Using k-Induction And Invariants. In: SBESC. (2015) 90–95
[22] Rocha, W., Rocha, H., Ismail, H., Cordeiro, L.C., Fischer, B.: DepthK: A k-Induction
     Verifier Based On Invariant Inference For C Programs - (Competition Contribution). In:
     Tools And Algorithms For The Construction And Analysis Of Systems. (2017) 360–364
[23] Malı́k, V., Martiček, Š., Schrammel, P., Srivas, M., Vojnar, T., Wahlang, J.: 2LS: Memory
     Safety And Non-termination. In: Tools And Algorithms For The Construction And Analysis
     Of Systems, Cham, Springer International Publishing (2018) 417–421
[24] Brain, M., Joshi, S., Kroening, D., Schrammel, P.: Safety Verification And Refutation By
     k-Invariants And k-Induction. In: Static Analysis. (2015) 145–161
[25] Sturtevant, N.R., Felner, A.: A Brief History And Recent Achievements In Bidirectional
     Search. In: Conference On Artificial Inteligence, AAAI Press (2018)
[26] Kroening, D.: CProver Manual. http://www.cprover.org/cprover-manual/
     (2018) [Online; accessed September-2018].
[27] Cordeiro, L.C., Fischer, B., Marques-Silva, J.: SMT-Based Bounded Model Checking For
     Embedded ANSI-C Software. IEEE Transactions on Software Engineering 38(4) (2012)
     957–974
[28] Gadelha, M.R., Monteiro, F.R., Morse, J., Cordeiro, L.C., Fischer, B., Nicole, D.A.: ES-
     BMC 5.0: An Industrial-Strength C Model Checker. In: Automated Software Engineering,
     ACM (2018) 888–891
[29] of Southampton, U.: The Iridis Compute Cluster. https://www.southampton.ac.
     uk/isolutions/staff/iridis.page (2018) [Online; accessed September-2018].
[30] Clarke, E., Kroening, D., Lerda, F.: A Tool For Checking ANSI-C Programs. In: Tools
     And Algorithms For The Construction And Analysis Of Systems. Volume 2988 of LNCS.
     (2004) 168–176
