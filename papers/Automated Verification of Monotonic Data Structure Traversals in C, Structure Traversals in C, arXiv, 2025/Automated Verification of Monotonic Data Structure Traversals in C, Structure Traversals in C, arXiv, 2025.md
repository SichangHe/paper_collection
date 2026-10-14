                                                Automated Verification of Monotonic Data
                                                       Structure Traversals in C

                                                                            Matthew Sotoudeh

                                                                            Stanford University
                                                                          sotoudeh@stanford.edu
arXiv:2505.18818v1 [cs.PL] 24 May 2025




                                                 Abstract. Bespoke data structure operations are common in real-world
                                                 C code. We identify one common subclass, monotonic data structure
                                                 traversals (MDSTs), that iterate monotonically through the structure.
                                                 For example, strlen iterates from start to end of a character array un-
                                                 til a null byte is found, and a binary search tree insert iterates from
                                                 the tree root towards a leaf. We describe a new automated verification
                                                 tool, Shrinker, to verify MDSTs written in C. Shrinker uses a new
                                                 program analysis strategy called scapegoating size descent, which is de-
                                                 signed to take advantage of the fact that many MDSTs produce very
                                                 similar traces when executed on an input (e.g., some large list) as when
                                                 executed on a ‘shrunk’ version of the input (e.g., the same list but with
                                                 its first element deleted). We introduce a new benchmark set containing
                                                 over one hundred instances proving correctness, equivalence, and mem-
                                                 ory safety properties of dozens of MDSTs found in major C codebases
                                                 including Linux, NetBSD, OpenBSD, QEMU, Git, and Musl. Shrinker
                                                 significantly increases the number of monotonic string and list traversals
                                                 that can be verified vs. a portfolio of state-of-the-art tools.

                                                 Keywords: Verification · Data Structures · Small Model Property.


                                         1     Introduction
                                         The C language’s lack of generics and focus on performance encourages bespoke,
                                         application-specific data structures. Bugs in these data structures can threaten
                                         safety and correctness of the entire codebase. Hence, we desire a tool to auto-
                                         matically prove the correctness of such data structure code written in C.
                                             This paper focuses on a subclass of data structure code we call monotonic
                                         data structure traversals (MDSTs). MDSTs are programs that take finitely many
                                         monotonic sweeps through the structure, where each sweep starts at some root
                                         or head element and moves forward on each loop iteration1 . Examples of MDSTs
                                         include classic implementations of strlen (start at the first character and iterate
                                         forward until a null byte is found), list-search (start at the head and iterate
                                         forward until the desired element is found), and bst-insert (start at the root
                                         and iterate down until a null pointer is found, then insert the new node).
                                         1
                                             We give no strict definition of MDST; it is merely intuition guiding the design of our
                                             analysis. Our tool remains sound (but incomplete) when applied to any C program.
2       Matthew Sotoudeh

Benchmarks and Empirical Results Existing benchmarks sets are either
not focused on MDSTs, or involve crafted benchmarks that are not necessarily
representative of real-world code. Hence, we constructed a new program verifi-
cation benchmark consisting of over one hundred instances verifying temporal
memory safety, spatial memory safety, and correctness properties of dozens of
MDSTs extracted from major C projects. For example, one instance checks that
the Linux and OpenBSD implementations of strcmp return numbers with the
same sign for every pair of input strings; another checks that appending to a
GNOME list increases its length by one.
    Our tool, Shrinker, nearly triples the number of string instances solved
(58 vs. 20) and more than doubles the number of list instances solved (20 vs. 9)
compared to the second-best solver. Shrinker solves the second-most number of
tree instances among the tools evaluated, including one not solved by any other
tool. Our results indicate Shrinker would make a strong addition to a portfolio
solver and can significantly improve the state-of-the-art in verifying string and
list MDSTs.


Scapegoating Size Descent Shrinker is based on our new scapegoating size
descent technique for verifying safety properties, i.e., that no execution trace of
a given input program crashes (dereferences null, makes a false assertion, etc.).
    Traditional program verifiers execute the program on all possible inputs at
once, tracking sets of possible program execution traces. If fixedpoint is reached
without any of the sets containing a crashing trace, the verifier can conclude that
the program is safe. Because most programs have infinitely many possible traces,
to ensure termination the verifier must overapproximate the set of possible traces.
E.g., rather than record that there are traces where a certain variable might have
values 0, or 2, or 4, . . . , the verifier might track only that the value is nonnegative.
While needed to make the verifier terminate, this overapproximation can make
the abstract interpreter think a crash might be possible even when it is not.
    Scapegoating size descent gives the verifier a new option: when it finds an
overapproximated trace that might crash, instead of giving up and reporting a
potential error, it is allowed to instead prove that, if there is a reachable crashing
trace of this form, then there also exists some strictly smaller reachable trace
that also crashes. In other words, the verifier establishes that, for every possible
program execution trace either: (1) the trace does not crash, or (2) if the trace
crashes, then there exists some smaller trace that crashes as well. Together, these
facts constitute a proof by infinite descent that no trace crashes.
    Our verification tool, Shrinker, is based on these ideas. Instead of running
the program on a single abstract input, it runs two (or more) copies of the pro-
gram side-by-side, one on an abstract input x and another on a shrunk version x′
of that input. For example, x might be a nonempty linked list, and x′ might be
formed by dropping the first node in x. Any time the abstract trace executing
on x potentially crashes (reaches a failure state), Shrinker merely needs to
prove that the ‘scapegoat trace’ executing on x′ also crashes and is smaller.
        Automated Verification of Monotonic Data Structure Traversals in C           3

Why Does It Work for MDSTs? The basic difficulty in automated verifi-
cation of heap-manipulating programs is that the heap can be arbitrarily large,
so the verifier must track facts involving an unknown number of values. Scape-
goating size descent can sidestep this problem because many MDSTs do almost
the same thing when run on an input x as when run on a shrunk version of that
input x′ . Consider a loop over a linked list: other than the very first iteration,
every subsequent iteration does exactly the same thing when run on a list x as
when run on the tail list x′ = x.next formed by dropping the first element in the
list. Thus, Shrinker only needs to track precise facts about the finitely many
memory locations that actually differ between the executions on x and x′ .

Contributions and Outline We make the following contributions:
 1. Scapegoating size descent framework for program analysis (Section 4).
 2. Shrinker tool for automated verification of C programs (Section 5).
 3. Evaluation of Shrinker and multiple baseline verifiers on our new bench-
    mark set of MDSTs extracted from major C projects (Section 6).
Section 2 gives preliminaries, Section 3 works through a motivating example,
and Section 7 describes related work. Appendix C describes limitations, future
work, and a motivating connection to the small scope hypothesis. The Shrinker
homepage is located at https://lair.masot.net/shrinker/ and an archival
version is located at https://doi.org/10.5281/zenodo.15225947.

2     Preliminaries and Traditional Abstract Interpretation
We now formalize our notion of a program and what it means for a program
to be safe, then describe a variant of abstract interpretation, which Section 4
builds on to form scapegoating size descent as used by Shrinker. In addition to
distinguishing names, we use blue for concrete states/traces and red for abstract.

2.1   Preliminary Definitions
We model the program to be verified as a transition relation on uninterpreted
states. We make no formal assumption about what a state is, but in practice it
represents the state of the registers and heap at a given point during program
execution. For the duration of this paper we assume a single, fixed program.
Definition 1. We assume the program to be verified is defined by a transition
relation → on states: s1 → s2 means “state s1 can transition to state s2 in
one program step.” A trace s1 , . . . , sn is a sequence of states. We assume the
verification conditions are specified by a (possibly infinite) set of initial traces I,
each of length 1, and a (possibly infinite) set of failure traces F .
Shrinker automatically extracts the program relation →, initial traces I, and
failure traces F from C code. We use the terms ‘fails’ and ‘crashes’ equivalently in
this paper. We distinguish between traces (any sequence of states) and reachable
traces (those that can actually result from an execution of the program).
4       Matthew Sotoudeh

Definition 2. A trace s1 , . . . , sn is a reachable trace if every step is a valid
program transition (i.e., s1 → s2 → · · · → sn ) and the singleton prefix of the
trace (i.e., just s1 ) is in the set of initial traces I. We use R to notate the set of
reachable traces. The program to be verified is safe if R ∩ F = ∅.

Finally, we introduce notation for executing the program for one additional
timestep, i.e., extending traces by one state. We allow nondeterminism, so the
result will be a set of possible subsequent traces.

Definition 3. Given a trace t = (s1 , s2 , . . . , sn ), Step(t) is the possible traces
reachable after one timestep, i.e., Step(t) = {(s1 , s2 , . . . , sn , sn+1 ) | sn → sn+1 }.


2.2   Trace Abstractions

Real computers are finite, but abstract interpreters must reason about a po-
tentially infinite number of possible program traces. Hence, we need a finite
representation of infinite sets of traces. This representation is formalized as an
abstract domain [Cousot and Cousot(1977)]. This paper only uses abstract do-
mains as a representation of infinite sets, and we do not place many requirements
on our abstract domain (e.g., we do not require a Galois connection).

Definition 4. An abstract trace domain AT is a set of abstract traces along
with a concretization function γ T that maps abstract traces to sets of traces.

The concretization function is merely used for the theoretical results: it need not
be implemented or even implementable. We make no other formal assumption
about the abstract traces. In practice, they usually contain constraints about
states in the trace, e.g., “the value of variable i at the last state in the trace is
positive,” and the concretization function γ T gives the set of all traces satisfying
those constraints. For the abstract interpreter to construct, manipulate, and
reason about abstract domain elements, the analysis designer must implement:

 1. I ♯ : overapproximates the possible initial traces, i.e., I ⊆ γ T (I ♯ )
 2. CanFail(a): tests for possible failure traces; must be true if γ T (a) ∩ F ̸= ∅.
 3. Step♯ (a): applies Step to all of the represented traces, i.e., for any t ∈ γ T (a)
    and t′ ∈ Step(t), we have t′ ∈ γ T (Step♯ (a)).
 4. MorePrecise(a, b): true only when γ T (a) ⊆ γ T (b).
 5. Widen(a): introduces overapproximations to ensure termination; it can re-
    turn anything as long as MorePrecise(a, Widen(a)).
 6. Split(a): splits a set of traces into subsets, often to introduce flow-, path-,
    or context-sensitivity into the analysis;            it returns a list of abstract traces
    a′1 , a′2 , . . . , a′n such that γ T (a) ⊆ i γ T (a′i ).
                                               S

The tool designer can instantiate this framework with different choices to reach
different points on the completeness–performance–termination tradeoff curve,
but as long as the above constraints are met soundness is guaranteed.
        Automated Verification of Monotonic Data Structure Traversals in C           5

   Data: A program (Section 2.1) and an abstract trace domain (Section 2.2).
   Result: Safe if the program is definitely safe, or Unknown.
                  ♯
 1 worklist ← {I },     seen ← {};
 2 while worklist is not empty do
 3    a ← worklist.pop();
 4    if CanFail(a) then return Unknown ;
 5    seen.add(a);
 6    foreach a′i ∈ Split(Step♯ (a)) do
 7        a′i ← Widen(a′i );
 8        if there exists b ∈ seen ∪ worklist with MorePrecise(a′i , b) then
 9             continue;
10        worklist ← (worklist \ {b ∈ worklist | MorePrecise(b, a′i )}) ∪ {a′i };
11 return Safe;
       Algorithm 1: Variant of Traditional Abstract Interpretation



2.3   Variant of Traditional Abstract Interpretation

Algorithm 1 shows an automated verification algorithm based on the traditional
abstract interpretation framework. It repeatedly calls Step♯ to explore the set of
reachable traces. If CanFail reports that any one might involve a failure trace,
it reports a possible error. Otherwise, once fixedpoint is reached, the program
is guaranteed to be safe. Widen and MorePrecise are used to encourage conver-
gence, while Split is used to case split abstract traces to improve precision.
    The key Lemma 1 guarantees that every reachable trace is represented by
some abstract trace processed on an iteration of the main loop in Algorithm 1.

Lemma 1. If the algorithm returns Safe, then for any reachable trace t there
exists some abstract trace a ∈ seen with t ∈ γ T (a).

Proof. Induct on the length of t = (s1 , s2 , . . . , sn ). The first iteration handles
everything with n = 1. Otherwise, by inductive hypothesis, the prefix t′ =
(s1 , . . . , sn−1 ) was added to seen on line 5 during some iteration. On that it-
eration, one of the a′i s must have t ∈ γ T (a′i ), which gets added to the worklist
on line 10, hence processed and added to seen in a future iteration. Alterna-
tively, a less-precise b might have been found already (line 9), but then t ∈ γ T (b)
already, as desired. Finally, a′i might be removed from the worklist in a future
execution of line 10, but that only occurs if something less precise (hence also
containing t in its concretization set) is added to replace it.                      ⊔
                                                                                     ⊓

Theorem 1. If Algorithm 1 reports Safe, then the program is safe.

Proof. Otherwise there must be a reachable trace t ∈ F , hence by Lemma 1 there
is a a ∈ seen with t ∈ γ T (a). But everything added to seen passed the check
on line 4, i.e., CanFail(a) is false, contradicting the definition of CanFail. ⊔
                                                                               ⊓
6         Matthew Sotoudeh

3       Motivating Example
This section works through a concrete example showing how traditional abstract
interpretation (Section 2.3) with a precise enough abstract domain can prove
correctness of a simple heap manipulating program. We then describe some issues
that make this difficult to do reliably and sketch how our technique, scapegoating
size descent (Section 4), would approach the same verification task. Consider the
code below, where we want to prove the __VERIFIER_fail() call is unreachable.
    1   struct arr { int *data; int n_data; };
    2   void test(struct arr arr) {
    3       for (int i = 0; i < arr.n_data; i++)
    4           arr.data[i] = 0;
    5       for (int i = 0; i < arr.n_data; i++)
    6            if (arr.data[i] != 0)
    7                __VERIFIER_fail(); }
The example is simplified for expository purposes, ignoring techniques like loop
fusion that can solve this instance but do not generalize as well. For space reasons
we are somewhat informal; see Appendix B for a more complete worked example.

3.1     Traditional Abstract Interpretation (Algorithm 1)
Recall that Algorithm 1 explores sets of possible program traces (each set repre-
sented by an abstract trace ai ) and checks that none includes a failing trace (i.e.,
one reaching line 7). On termination, Lemma 1 guarantees that every reachable
trace lies in the concretization set of one of those abstract traces added to seen.
The exact behavior depends on the abstraction used, but below we have visual-
ized one possible result. Each node represents an abstract trace in the final seen
set. An edge ai → aj means aj was added to the worklist while processing ai ,
i.e., applying Step to a trace in γ T (ai ) might result in a trace in γ T (aj ).
                             a2           a4            a5


             a1 = I ♯        a3           a6            a7            a8


Below, we describe each abstract trace as a set of constraints. The concretization
set consists of every trace satisfying those constraints. We assume executing
lines 3 and 5 checks the corresponding loop condition and either executes the
loop body or exits the loop.
    – a1 : About to execute line 3. arr.data points to arr.n_data integers, i=0
    – a2 : About to execute line 5. arr.n_data=0, i=0
    – a3 : About to execute line 3. arr.n_data>=1, arr.data[0]=0, i=1
    – a4 : About to execute line 5. arr.n_data=1, arr.data[0]=0, i=0
    – a5 : About to execute line 5. arr.n_data=1, arr.data[0]=0, i=1
        Automated Verification of Monotonic Data Structure Traversals in C          7

 – a6 : About to execute line 3. arr.n_data>1, 2<=i<=arr.n_data,
   arr.data[0]=0, . . . , arr.data[i-1]=0
 – a7 : About to execute line 5. arr.n_data>1, i=0,
   arr.data[0]=0, . . . , arr.data[arr.n_data-1]=0
 – a8 : About to execute line 5. arr.n_data>1, 1<=i<=arr.n_data,
   arr.data[0]=0, . . . , arr.data[arr.n_data-1]=0

    Algorithm 1 can prove that traces represented by a8 never reach the crash on
line 7, because all of those traces satisfy arr.data[0] = arr.data[1] = ...
= arr.data[arr.n_data-1] = 0, so the if condition is never taken. This anal-
ysis, however, requires the abstract domain to reason about constraints
involving an unknown number of memory locations, specifically the con-
straints asserting that some subset of arr.data entries are zero (the “. . . ”s in the
above constraints for a6 , a7 , and a8 ). If the abstract domain used was not able
to represent such constraints, the analyzer would report a false positive because
it would not be able to guarantee that the if condition on line 6 is not taken.
    Some abstract domains can handle constraints like this [Piskac et al.(2013)],
but the larger search space makes automatically synthesizing useful invariants
harder than when restricted to only constraints that involve a finite number of
memory locations. By contrast, the abstract traces for a1 through a5 , which only
constrain the values of finitely many memory locations, tend to be simpler to
reason about and synthesize. The key goal of scapegoating size descent is
to avoid having to track precise constraints about an unknown number
of memory locations. Instead, we want to only track constraints about the
(often finitely many) memory locations that differ when executing on a full input
vs. some related, smaller input.


3.2   Scapegoating Size Descent

At a high level, our scapegoating size descent approach also explores sets of pro-
gram traces that together account for every possible reachable trace and checks
whether they reach failure. In fact, its handling of the traces with inputs of size 0
or 1 (i.e., a1 through a5 ) is essentially identical to traditional abstract interpre-
tation: we track constraints on the finitely many memory locations arr.n_data,
arr.data[0], and i to verify that line 7 is never reached on any such small-
sized input. The difference comes in handling a6 through a8 , which represent
traces that go through the loops an arbitrary (larger than 1) number of times
and which, in traditional abstract interpretation, required an abstract domain
capable of handling constraints on an unknown number of memory locations.
    Instead of directly proving that line 7 can never be reached on such traces,
scapegoating size descent tries to prove that it can only be reached if some
smaller trace reaches it as well. This conditional proof is often easier to synthesize
and can avoid needing to track precise constraints on arbitrarily many memory
locations, as in a6 , a7 , a8 above. We do this by associating each such abstract
trace with a scapegoat trace that has very closely related behavior to the primary
trace we are concerned with. Usually, the scapegoat trace is the result of running
8         Matthew Sotoudeh

the program on a shrunk version of the input for one fewer iteration of each
loop: if a trace is the result of running the program on input array [3, 4, 10, 8],
the scapegoat trace might result from running the program on [4, 10, 8]. For
example, the equivalent of a6 , a7 , and a8 are the following:
    – a6 : About to execute line 3. arr.n_data>1, 2<=i<=arr.n_data, arr.data[0]=0.
      For any reachable trace satisfying those constraints, there exists another
      reachable trace (the scapegoat) where the last state is identical except: arr.data[0]
      was removed, and both arr.n_data and i were decremented by 1.
    – a7 : About to execute line 5. arr.n_data>1, i=0, arr.data[0]=0.
      For any reachable trace satisfying those constraints, there exists another
      reachable trace where the last state is identical except: arr.data[0] was
      removed and arr.n_data was decremented by 1.
    – a8 : About to execute line 5. arr.n_data>1, 1<=i<=arr.n_data, arr.data[0]=0.
      For any reachable trace satisfying those constraints, there exists another
      reachable trace where the last state is identical except: arr.data[0] was
      removed, and both arr.n_data and i were decremented by 1.
Crucially, the constraints for a8 imply that if some trace satisfying the con-
straints of a8 were to fail (reach line 7) on the next iteration, its corresponding
scapegoat trace would also fail. So we have actually proved: if some input of size
arr.n_data leads to a failing execution, then there is another input of strictly
smaller size arr.n_data - 1 that also reaches failure. In this way, because the
size is nonnegative, we can apply proof by infinite descent (Theorem 2, essentially
induction on input size) to conclude that no input causes a failure.


4      Scapegoating Size Descent
This section formalizes our scapegoating size descent variant of abstract inter-
pretation, as used in Shrinker. Traditional abstract interpretation tracks a set
of possible traces. Scapegoating size descent modifies this framework to track a
set of herds of traces; each herd is a primary trace t1 along with a number of
scapegoat traces t2 , t3 , . . . resulting from different inputs or different nondeter-
ministic choices2 . When the abstract interpreter thinks it might be possible for
the primary trace to have crashed, scapegoating size descent allows the abstract
interpreter to avoid giving up by transferring the blame onto one of the scape-
goat traces. To blame a scapegoat trace, it must prove that, if the primary trace
has crashed, then the scapegoat trace has also crashed and is smaller than the
primary trace (for some definition of size; see Section 4.1). In this way, scape-
goating size descent proves that every reachable trace either does not crash, or,
if it does crash, then there is some strictly smaller reachable trace that also
crashes. If the size measure is well-founded (e.g., natural numbers), proof by
infinite descent (Theorem 2) ensures that no traces crash, i.e., the program is
safe. A detailed worked example is provided in Appendix B.
2
    Apparently, some call a group of goats a ‘trip’ or a ‘tribe,’ but unfortunately ‘t’-
    starting names overload with ‘trace.’
          Automated Verification of Monotonic Data Structure Traversals in C                 9

4.1     Trace Sizes and Infinite Descent

We assume the tool designer provides a measure of the size of a trace.
Definition 5. A trace size function ⟨·⟩ maps traces t to a size ⟨t⟩ ∈ N.
Shrinker currently uses a measure of size that essentially counts the number of
allocated items on the heap. But Shrinker is fairly robust to the exact measure
of size; we expect that the number of bytes allocated or even the length of the
trace itself would work as well (see Appendix A.9 for further discussion). The
choice of trace size affects only completeness, not soundness. Since our trace sizes
are natural numbers, we can use proof by infinite descent.
Theorem 2. (Proof by Infinite Descent) Let P (n) be any statement parameter-
ized by n ∈ N. Suppose that whenever P (n) is false, there exists m ∈ N such that
m < n and P (m) is also false.3 Then, P (n) is true for all n ∈ N.
In fact, our results generalize to any measure of size as long as the comparison
relation admits no infinite descending chains, i.e., there exists no infinite sequence
of traces ⟨t1 ⟩ > ⟨t2 ⟩ > . . ..


4.2     Trace Herds and Abstract Trace Herds

Rather than tracking sets of traces, scapegoating size descent tracks sets of herds
of traces. In addition to distinguishing names, we will color herds in teal and
abstract herds in purple.
Definition 6. A herd is an ordered tuple of traces. If h is a herd, then |h| is
the size of h and h[1], . . . , h[|h|] are all traces. We use h = (h[1], . . . , h[n]) to
indicate a herd of size |h| = n. We call h[1] the primary trace of the herd, and
h[2], . . . , h[n] the scapegoat traces of the herd.
The size |h| of a herd is just the number of traces in it; there is no relation to
the size of an individual trace in the herd. The first trace in the herd plays the
role of the primary trace we are trying to prove things about; in fact, scape-
goating size descent restricted to size-1 herds is identical to traditional abstract
interpretation (Algorithm 1). HSingle constructs a singleton herd from a trace:


Definition 7. Given a trace t, we define HSingle(t) = (t) to be the herd of size
1 consisting of only the primary trace t and no scapegoats. Given a set of traces
T , we overload HSingle(T ) to mean the set {HSingle(t) | t ∈ T }.
Given a herd, we need notation for modifying individual traces in the herd.
Definition 8. Given a herd h, index i, and trace t, we define the update-index
function HUpdate(h, i, t) = (h[1], . . . , h[i − 1], t, h[i + 1], . . . , h[n]). We also define
the drop-index function HDrop(h, i) = (h[1], . . . , h[i − 1], h[i + 1], . . . , h[n]).
3
    Inparticular, this implies P (0) is not false, as 0 has no predecessor in N.
10       Matthew Sotoudeh

Finally, we need to be able to extend traces in the herd by executing the program
on that trace for one timestep.
Definition 9. Given a herd h, we define the function HStep(h, i) = {HUpdate(h, i, t) |
t ∈ Step(h[i])}, or HStep(h, i) = h if i is not between 1 and |h|.

4.3    Herd Abstractions
As with Algorithm 1, the tool designer must provide an abstract domain to
represent sets of herds along with a number of abstract domain operations.
Definition 10. An abstract herd domain AH is a set of abstract herds along
with a concretization function γ H that maps abstract herds to sets of herds.
Once again, we make no assumptions about what the abstract herds are, and
the concretization function is only needed for the theoretical results; it does not
need to be implementable. The tool designer does still need to provide a number
of operations for working with abstract herds.
    The following operations are essentially lifting ones we used in Section 2.2 to
abstract herds rather than abstract traces:
 1. I H♯ : represents all herds where the primary trace is a starting trace, i.e.,
    HSingle(I) ⊆ γ H (I H♯ ).
 2. HCanFail(a): must be true if any of the herds has a failing primary trace,
    i.e., true whenever there exists h ∈ γ H (a) with h[1] ∈ F .
 3. HStep♯ (a): runs the primary trace in each herd forward, i.e., for every h ∈
    γ H (a) and h′ ∈ HStep(h, 1), we have h′ ∈ γ H (HStep♯ (a)).
 4. HMorePrecise(a, b): true only when γ H (a) ⊆ γ H (b).
 5. HWiden(a): returns anything as long as HMorePrecise(a, HWiden(a)).
 6. HSplit(a): returns abstract herds a′1 , a′2 , . . . , a′n such that γ H (a) ⊆ i γ H (a′i ).
                                                                                 S

The following are new operations only used in scapegoating size descent:
 1. MaybeAddScapegoats(a) adds candidate scapegoat traces to the herd. These
    candidate scapegoat traces must be reachable traces whenever the primary
    trace is reachable. In practice, the scapegoat traces are constructed by mod-
    ifications to the input in the main trace, e.g., dropping the first node in a
    linked list input argument. Formally, for every herd h ∈ γ H (a), either
    (a) h[1] is not a reachable trace, or
    (b) there exists h′ ∈ γ H (MaybeAddScapegoats(a)) extending h, i.e., where
         h′ = (h[1], . . . , h[|h|], t1 , . . . , tn ) and t1 , . . . , tn are all reachable traces.
 2. HStep♯∃ (a, i) runs the ith trace in the herd (must be a scapegoat, i.e., i > 1)
    forward for one timestep. If multiple subsequent states are possible, e.g.,
    because a nondeterministic choice was made by the program, it may pick
    any one of the choices (we only need to guarantee the existence of at least
    one scapegoat trace, not analyze all possible scapegoat traces). Alternatively,
    it may drop a scapegoat trace, e.g., if no successors exist. Formally, for
    any h ∈ γ H (a), either:
        Automated Verification of Monotonic Data Structure Traversals in C           11

   Data: A program (Section 2.1) and an abstract herd domain (Section 4.3).
   Result: Safe if the program is definitely safe, or Unknown.
                  H♯
 1 worklist ← {I     }, seen ← {};
 2 while worklist is not empty do
 3    a ← worklist.pop();
 4    if HCanFail(a) and there is no i > 1 with CanBlame(a, i) then
 5        return Unknown;
 6    seen.add(a);
 7    for a′i ∈ HSplit(HStep♯ (a)) do
 8        a′i ← MaybeAddScapegoats♯ (a′i );
 9        for j ← StepperHeuristic() with j > 1 do a′i ← HStep♯∃ (a′i , j) ;
10        a′i ← HWiden(a′i );
11        if there exists b ∈ seen ∪ worklist with HMorePrecise(a′i , b) then
12             continue;
13        worklist ← (worklist \ {b ∈ worklist | HMorePrecise(b, a′i )}) ∪ {a′i };
14 return Safe;
 Algorithm 2: Scapegoating size descent. For soundness, StepperHeuristic
 may return any sequence of numbers greater than 1.


   (a) there exists a h′ ∈ HStep(h, i) such that h′ ∈ γ H (HStep♯∃ (a, i)), or
   (b) HDrop(h, i) ∈ γ H (HStep♯∃ (a, i)).
3. CanBlame(a, i) determines whether we can blame the ith scapegoat in the
   herd, i.e., whether it represents a trace that reached failure on a strictly
   smaller input. Formally, returns true only if for every h ∈ γ H (a) both:
   (a) ⟨h[i]⟩ < ⟨h[1]⟩, and
   (b) h[i] ∈ F .


4.4   Algorithm

The scapegoating size descent algorithm is presented in Algorithm 2. It is almost
identical to Algorithm 1, except (1) the verifier can add and step forward scape-
goat traces arbitrarily, i.e., according to the heuristics MaybeAddScapegoats and
StepperHeuristic; and (2) the verifier can ignore a possibly failing herd if one
of the scapegoat traces can be successfully blamed.


Correctness Proof In traditional abstract interpretation, Lemma 1 guaranteed
that every reachable trace was in the concretization set of some seen abstract
trace. But in scapegoating size descent, the abstract elements represent sets of
herds, not sets of traces, so we need to be more precise about what we mean
when we say an abstract herd seen by the algorithm accounts for a given trace.
We will say that an abstract herd a accounts for a trace t if there is some herd
in the concretization set of a where (i) t is the primary, and (ii) everything in
the herd is reachable. The following definition makes this precise.
12      Matthew Sotoudeh

Definition 11. An abstract herd a accounts for a trace t if there exists some
herd h ∈ γ H (a) with h[1] = t and all of the traces in h are reachable. In that
case, we say h witnesses that a accounts for t.
Lemma 2 observes that none of the new, scapegoat-only operations that Algo-
rithm 1 performs can decrease the set of traces accounted for.
Lemma 2. Let a be an abstract herd and suppose t is a trace accounted for
by a. Then, after computing a′ = HWiden(a), a′ = MaybeAddScapegoats(a), or
a′ = HStep♯∃ (a, i) for any i > 1, t is still accounted for by a′ .
Proof. Let h ∈ γ H (a) be the herd witnessing that a accounts for t (Definition 11).
We must show there exists some h′ witnessing that a′ accounts for t as well. For
a′ = HWiden(a), the definition guarantees that γ H (a) ⊆ γ H (a′ ) so in particular
we can take h′ to be h. For a′ = MaybeAddScapegoats(a), we know that a valid h′
exists by the requirements on case (b) of the definition of MaybeAddScapegoats
in Section 4.3. For a′ = HStep♯∃ (a, i) with i > 1, we know that there exists some
h′ ∈ γ H (a′ ) such that either (i) a h′ ∈ HStep(h, i), or (ii) h′ ∈ HDrop(h, i). In
either case, h′ satisfies the desired conditions.                                  ⊔
                                                                                   ⊓
We can now prove the equivalent of Lemma 1 in almost exactly the same way
as Section 2.3, except replacing “t ∈ γ T (a)” with “a accounts for t.”
Lemma 3. If Algorithm 2 returns Safe, then for any reachable trace t there
exists an abstract herd a ∈ seen accounting for t.
Proof. Induct on the length of t = (s1 , s2 , . . . , sn ). For the base case, if n = 1 then
it is accounted for by a when line 6 is reached on the first iteration. Otherwise, by
inductive hypothesis, the prefix t′ = (s1 , . . . , sn−1 ) was accounted for by some a
added to seen on line 6 during some iteration. On that iteration, one of the a′i s
must account for t and get added to the worklist, and hence processed and added
to seen in a future iteration (Lemma 2 guarantees that it still accounts for t even
after executing MaybeAddScapegoats, HStep♯∃ , and HWiden in the inner loop).
Alternatively, a less-precise b might have been found already (line 12), but then
t will be accounted for by b already, as desired. Notably, it is possible for a′i to be
removed from the worklist in a future execution of line 13 but that only occurs
if something less precise (hence also accounting for t) is added to replace it. ⊔          ⊓
Lemma 4. If Algorithm 2 reports Safe, then for every reachable trace t ei-
ther t ̸∈ F or there is another reachable trace t′ ∈ F with ⟨t′ ⟩ < ⟨t⟩.
Proof. From Lemma 3 an abstract herd a was added to seen with some herd h ∈
γ H (a) having primary trace t = h[1] and reachable scapegoats h[2], . . . ,
h[n]. But for Algorithm 2 to return Safe, it must have passed the HCanFail
and CanBlame check on line 4, i.e., either t ̸∈ F or some scapegoat t′ = h[i] is
smaller and also fails, i.e., t′ ∈ F and ⟨t′ ⟩ < ⟨t⟩ as desired.              ⊔
                                                                              ⊓
Theorem 3. If Algorithm 2 reports Safe, then the program is safe.
Proof. Using Lemma 4 we can apply proof by infinite descent (Theorem 2) to
the claim “no reachable trace of size n is in F ” and conclude that no reachable
trace (of any size) is in F , i.e., the program is safe.
        Automated Verification of Monotonic Data Structure Traversals in C        13

5     The Shrinker Tool
This section describes our scapegoating size descent implementation Shrinker.
The Shrinker homepage is located at https://lair.masot.net/shrinker/
and an archival version with benchmarks and baseline tools is located at https:
//doi.org/10.5281/zenodo.15225947.

5.1   User Interface
Verification goals are provided by the user to Shrinker as a C file defining a spe-
cial test function. This function may take parameters, and it may call the spe-
cial methods __VERIFIER_ignore() and __VERIFIER_fail(). Shrinker tries
to prove that no input to test produces a trace that calls __VERIFIER_fail()
without first calling __VERIFIER_ignore(). It is useful to wrap those methods
in assume(X) and assert(X) macros that check a condition before ignoring or
failing. This lets the user express program-specific correctness properties without
requiring the user to learn a complicated logical notation. Shrinker automati-
cally instruments pointer operations to check memory safety properties. Optional
overflow checking can also be implemented by instrumentation. We also support
__VERIFIER_nondet_type() methods to get nondeterministic values. We do not
support VLAs or explicit C array types, but the user can specify that an input
pointer points to an arbitrarily sized array of items (Appendix A.11).

Subset of C Supported Shrinker supports a usable subset of C including structs,
pointers, loops, nonrecursive and tail-recursive function calls, and the standard
integer types. We throw an error immediately upon seeing unsupported parts of
C, such as union types, function pointers, and array types.

Assumption that Inputs Point to Disjoint Heaps For linked structures, Shrinker
verifies the correctness condition under the additional assumption that the inputs
to the function point to disjoint, acyclic heaps, i.e., we only consider tree-shaped
input structures. This only affects inputs to the function; the function can itself
modify the input into any form it wishes and call other functions with cyclic
inputs. This is how, e.g., we verify doubly and cyclicly linked structures: the
test harness first rewrites the acyclic input into a cyclic list and only then is the
relevant operation performed. See Appendix A.10 for more details.

Array and String Inputs Array inputs are specified by a struct type having
two fields, one integer length field named n_X and one pointer field named X
(see Appendix A.11 for an example). Shrinker verifies the program under the
assumption that all instances of such structs reachable from the input arguments
are initialized with a nonnegative value for the n_X field and an allocated memory
region of exactly n_X items pointed to be the X field. String inputs can be specified
by declaring an array-of-chars input, then having the test harness iterate over
it at the start of the test harness and call __VERIFIER_ignore() if it is not a
properly formatted string.
14     Matthew Sotoudeh

5.2   Tool Organization and Trusted Code Base

Shrinker is unusually small, having fewer than 7 thousand lines total of C
and Python code, with no runtime dependence on third-party libraries. A small
trusted codebase can improve maintainability and confidence in its soundness.
    Shrinker includes a parser written in Python that lowers C code to a sim-
ple intermediate representation. Each operation in this intermediate represen-
tation has corresponding implementations of abstract transformers (i.e., HStep♯
and HStep♯∃ ) that together encode the semantics of the program. To keep the
implementation manageable, we do not support array types, unions, or function
pointers. We also inline all function calls, hence we only support nonrecursive
and tail-recursive function calls. When unsupported syntax is encountered, we
provide a line number and descriptive error message to the user.
    The remainder of the tool is organized as described in Section 4, using an
abstract domain we wrote with core operations implemented in C for efficiency.
One other major optimization was to parallelize the tool (see Appendix A.8).


5.3   Abstract Herd Domain

We represent abstract herds as constraints on the values of memory locations
in different states in each trace. Constraints can relate valuess across different
states, memory locations, and traces in the herd. They can also constrain the
possible values of trace metadata, e.g., what the ‘program counter’ (next instruc-
tion to be executed) is. Examples of constraints include:

 – “The value of i in the first state of trace 1 is one less than the value of i in
   the first state of trace 2,”
 – “The value of j in the last state of trace 5 is positive,”
 – “If x is positive in the second-to-last state of trace 1, then the program
   counter in the last state of trace 1 is instruction 10 in the intermediate
   representation of the program; otherwise it is instruction 20.”

The abstraction can be queried, e.g., to ask questions like:

 – “Can j be nonzero in the last state of trace 5?”
 – “What are the possible program counter values in the last state of trace 1?”


Memory Abstraction The above informal examples refer to local variables in
the program. But to verify heap-manipulating code, we need the ability to refer
to locations in the heap. This is done using heap addresses, i.e., constraints can
refer to a term representing “the value at memory address X in the ith state of
trace j.” We use a memory abstraction inspired by the three-valued logic ana-
lyzer [Sagiv et al.(1999)]. We track facts about two types of locations in memory:
either concrete locations that represent a specific address in memory (e.g., the
first node in a linked list), or a summary location that represents multiple ad-
dresses in memory (e.g., all of the remaining nodes in the list). We implement
        Automated Verification of Monotonic Data Structure Traversals in C         15

this with a two-level memory abstraction: every memory location has both a
major and minor address, and summary locations refer to a group of memory
locations that share the same major address. We implement linked structures of
arbitrary size by adding a summary node to represent all nodes beyond a certain
depth. We prevent this addressing scheme from leaking into the program, e.g., by
disallowing the casting of non-NULL pointers into integers. We implement arrays
by giving all entries in the array a single major address, introducing concrete
nodes for the first few entries in the array, and then introducing a summary node
to represent the remainder of the array (the number of entries to make concrete
nodes for is a user-configurable parameter).

Numerical Reasoning Shrinker only adds a small number of constraints,
e.g., applying HStep to a program about to execute a line i=j; will add a con-
straint saying that i in the last state has the same value as j in the second-to-last
state (along with other constraints asserting that no other memory location has
changed). These often imply additional implicit constraints, e.g., if we also know
that j>k in the second-to-last state, we can infer i>k in the last state (after
applying i=j). To make such inferences, we wrote a standard integer difference
logic (IDL) solver to determine all relations implied by constraints of the form
x−y ≤ c where x and y are terms and c is a constant offset [Cormen et al.(2009)].
All terms in the state (even nonnumerical ones) are represented in the IDL solver;
boolean terms can be encoded as 0 for false and 1 for true. Additional rules infer
basic numerical and logical properties, e.g., when a = b and some fact F (a) is
true, the fact F (b) can be deduced. Additional checks are added to properly
model unsigned int overflow and casting behavior according to the C standard,
even though the underlying solver treats all variables as mathematical integers.

5.4   Widening (HWiden)
HWiden(a) is implemented by dropping constraints in a heuristically. Shrinker
only widens at loop iteration points, and only once the loop has been unwound
for a certain (user-controlled) number of times or a summary region has been
accessed during an earlier iteration of that loop. We first remove all constraints
referring to anything other than the very first and last states in the trace. We
then search through the seen and worklist lists for other abstract trace herds
with the same abstract path (essentially, about to execute the same line; see Ap-
pendix A.1 for more details), and weaken any constraints that are not shared
by all of those herds to just store the sign of the difference (e.g., if one im-
plies a − b < −4 and another implies a − b < −7, we weaken to the constraint
a − b < 0). Because there are only finitely many major addresses in our memory
abstraction, we exempt constraints describing the major address portion of a
pointer and instead try to track the precise list of all possibilities (a threshold is
used to overapproximate if even this gets too large).

Scapegoating and Other Heuristics For space reasons, details of our other
heuristics, e.g., for adding and stepping scapegoats, are deferred to Appendix A.
16      Matthew Sotoudeh

Briefly stated, we keep the analysis precise up to a certain unrolling depth for
each loop. Then, we add scapegoats corresponding to traces formed by dropping
elements from the input structure (e.g., the first element of an array or list).
We step those scapegoats forward until the two loops come in-sync, i.e., pointers
to input nodes point to the same thing in the primary and the scapegoat, and
integer loop indices into arrays differ by one. Then we step the scapegoats in
lockstep with the primary trace until the loop is exited.

6     Evaluation
This section describes our benchmark set and empirical evaluation. Experiments
were run on a Debian 12 virtual machine on an Intel i9-13900. Benchexec was
used to limit RAM to 32GB and wallclock to 3 hours per instance–tool pair.

6.1   Benchmarks
We collected a set of benchmarks verifying correctness, memory safety, and
equivalence properties of dozens of MDSTs from major real-world C projects.
The full list of projects we extracted data structure traversals from are: Linux [lin(2023)],
NetBSD [net(2024)], OpenBSD [ope(2025)], Musl [mus(2025)], GLib [gli(2025)],
QEMU [qem(2025)], Redis [red(2025)], Zsh [zsh(2025)], Git [git(2025)], and GLibC [gli(2023)].
We divided the benchmarks into three classes: strings, lists, and trees. Our set
is more heavily weighted towards string benchmarks because all the operations
shared a standard string representation so we could construct many benchmark
instances by cross-checking them. Examples of instances include checking:
1. The Linux and NetBSD implementations of strcmp agree on all inputs.
2. After inserting into an instance of Redis’ linked list, using Redis’ list-search
   routine to search for the item just inserted always succeeds.
3. If a search for x in the glibc implementation of red-black trees succeeds,
   then after rotating a node in the tree, a subsequent search for x still succeeds.
We tried to specialize the test harnesses to the tools’ preferred format. E.g.,
Shrinker expects the input to the operation to be taken as an argument to
the test harness, while the baseline tools expect this input to be constructed
by the harness itself. Meanwhile, one of the baseline tools does not support tail
recursion, so for the benchmarks using recursion we provided it versions that
were manually transformed into a loop. We also performed some tuning of the
encodings, e.g., finding that the baseline tools performed better when strings
were allocated using malloc rather than as VLAs on the stack, so we used those
encodings. We configured all tools to check only memory safety and user assertion
properties. We have provided the full benchmark set with this submission.

6.2   Baseline Tools
We report comparisons against the baseline tools VeriAbsL [Darke et al.(2023)],
PredatorHP [Soková et al.(2023)], and 2LS [Malík et al.(2018)]. We tried to rep-
resent the state-of-the-art in verification of heap-manipulating C code, excluding
          Automated Verification of Monotonic Data Structure Traversals in C    17


Benchmark Count Kind          Shrinker VeriAbsL PredatorHP 2LS Port. w/o Port. w/
strings       62    solved       58       20          0       0      20        58
                    unique       38       0           0       0
                    fastest      51       7           0       0
lists         26    solved       20        4          6       9      14        23
                    unique        9        1          0       1
                    fastest       9        2          6       6
trees         17    solved       13        0          0      16      16        17
                    unique       1         0          0       4
                    fastest      3         0          0      14
Table 1: Evaluation Table. For each benchmark, the ‘solved’ row shows how
many instances that tool solved, the ‘unique’ row shows how many instances
were solved only by that tool, and the ‘fastest’ row shows how many instances
that tool solved faster than any other tool. “Port. w/o” shows the number solved
by a virtual-best portfolio of all tools except Shrinker, while “Port. w/” shows
the number solved by a virtual-best portfolio including Shrinker.



tools like Astree [Blanchet et al.(2002)] without public executables, but includ-
ing tools like VeriAbsL that are publicly available only in binary form.
    We also considered MemCAD [Sotin and Rival(2012)] and Ultimate Taipan [Greitschus et al.(2017)].
Although it worked for small test programs, MemCAD threw many errors when
we tried to run it on our benchmark instances, apparently due to the use of C
features like initializing a struct pointer in a for loop. Because of this, we could
not run most of the benchmarks on MemCAD, and its errors/documentation
were not descriptive enough for us to adapt them in time for this submission.
While Ultimate Taipan did properly parse and begin verifying our benchmarks,
it timed out or returned Unknown on all of them. In both cases, we assume that
the tools are probably tuned for different classes of inputs and so we exclude
them from our experiments and do not report such negative results further.
    It is also important to note that VeriAbsL, PredatorHP, and 2LS are com-
petitors in the SV-COMP competition, which involves detecting unsafe programs
quickly in addition to verifying safe ones. Our evaluation considers only the ver-
ification of safe programs, as we suggest detecting unsafety using a dedicated
bounded model checking or fuzzing tool. Hence, it should be kept in mind that
these baseline models might perform better if optimized to our setting.


6.3     Results

Our results are summarized in Table 1 and visualized as cactus plots in Figure 1.
    For both the string and list benchmark classes, Shrinker is the single best
solver. It is able to solve more than double the number of instances compared
with the second-best solver. In fact, in both cases Shrinker is able to solve many
benchmarks that were not solved by any other baseline solver. Furthermore, it
18                                   Matthew Sotoudeh

                                                                                                                                            ·104
                                                                               300
                               800                                                              Shrinker         VeriAbsL
                                                                                                   2ls          predatorhp             2
                                                                                                  pwith          pwithout
     Total Time to Solve (s)   600
                                                                               200                                                   1.5

                               400
                                                                                                                                       1
                                                                               100
                               200                                                                                                   0.5


                                 0                                                  0                                                  0

                                     0   10     20    30     40      50   60                0         5     10        15       20              0            5          10           15
                                         Number of Problems (Strings)                             Number of Problems (Lists)                           Number of Problems (Trees)

                                                                                                                                    8,000
                               40
Marginal Time to Solve (s)




                                                                               30
                                                                                                                                    6,000
                               30
                                                                               20                                                   4,000
                               20

                                                                               10                                                   2,000
                               10

                                                                               0                                                       0
                                0
                                     0   10    20     30     40      50   60            0         5        10        15      20                    0         5          10          15
                                           Problem Index (Strings)                                 Problem Index (Lists)                                  Problem Index (Trees)



Fig. 1: Cactus plots. A point (n, t) on the top row indicates the tool can solve n
of the benchmarks in t total seconds. A point (i, t) on the bottom row indicates
the tool can solve the ith easiest (for it) benchmark in t seconds; prefix-summing
the bottom row gives the top row. In all cases, curves lower (faster) and to the
right (solving more problems) are better. We also give curve corresponding to the
virtual-best portfolio (i.e., assuming a perfect heuristic that picks the best solver
out of the four for that instance) both with (pwith) and without (pwithout)
Shrinker (for strings and trees, only one other tool solved any instances so the
“portfolio without” line is identical to the other tool’s curve). For both strings and
lists, Shrinker on its own always solves more instances than any other tool,
is within the same order of magnitude of time as the other tools (sometimes
faster), and leads to significant improvements in the portfolio performance. For
trees, Shrinker is considerably slower than the best tool (2ls), but its inclusion
in the portfolio results in solving one additional benchmark.



does so in a reasonably small (≤ 30s) amount of time per benchmark. There
remain only four string instances unsolved, all of which involve strcat, which
is implemented in a complicated way for Shrinker to follow (namely, the loop
iterates simultaneously from the middle of the destination array and the start
of the source array). On the whole, however, these results indicate Shrinker is
particularly good at solving monotonic string and list instances.
    On tree benchmarks, Shrinker performs quite well, solving over 75% of
the tree benchmarks while neither VeriAbsL nor PredatorHP solved any. How-
ever, 2LS performs surprisingly well (solving all but one), hence Shrinker takes
second-place when looking at individual solvers. Shrinker took longer to solve
the tree benchmarks than the string and list benchmarks because it performs
path splitting up to a certain unrolling depth, and tree-manipulating programs
        Automated Verification of Monotonic Data Structure Traversals in C      19

have an extra exponential blowup in the number of paths (because there is a
choice between left/right child during each traversal). This path splitting is not
strictly required by scapegoating size descent, but is needed for Shrinker to
increase precision in lieu of a more precise abstract domain (see Appendix C.5
for more discussion). Nonetheless, Shrinker was able to solve the one instance
left unsolved by 2LS.
    In fact, for all three classes of benchmarks we find that adding Shrinker
to a virtual-best portfolio solver would allow it to solve more benchmarks than
would be possible without Shrinker (compare the “Port. w/o” and “Port. w/”
columns in Table 1 and the ‘pwith’ and ‘pwithout’ curves in Figure 1). Hence, in
addition to being a compelling stand-alone solver for monotonic string and list
benchmarks, Shrinker could make a good addition to a portfolio like VeriAbsL.


7   Related Work

Induction on Input Size. [Chakraborty et al.(2020),Chakraborty et al.(2021)] (in-
tegrated into the VeriAbsL portfolio) use rules to rewrite array programs PN into
a tail recursive form PN = δPN ; PN −1 and prove correctness by inducting on the
size of the input. [Ish-Shalom et al.(2020)] describe a similar approach for array
verification. Scapegoating size descent generalizes these ideas to a framework
parameterized by data type, measure of size, and abstraction.

Cyclic Proof Systems. Proof by infinite descent also forms the basis of cyclic proof
systems [Brotherston(2005),Brotherston et al.(2012),Lucanu and Rosu(2007)]. Our
main contribution is scapegoating size descent, which is a general framework for
combining proof by infinite descent with abstract interpretation to form a param-
eterized, general method of automatically proving properties about imperative
programs.

Abstract Interpretation. Traditional static analysis is formalized by abstract in-
terpretation [Cousot and Cousot(1977),Brat et al.(2014),Blanchet et al.(2002)],
and we described one formulation of it in Section 2. Abstract interpreters use spe-
cial abstractions of the heap [O’Hearn et al.(2001),Sagiv et al.(1999),Calcagno et al.(2009)].
[Sagiv et al.(1999)] introduced the summary nodes idea we adapted in Section
5. Unfortunately, the space of such heap invariants is large, making discovering
them hard. Scapegoating size descent builds on this framework to verify mono-
tonic data structure traversals even without complicated heap abstractions.

Relational Verification. Reasoning about pairs of traces is part of the broader
field of relational program verification [Beckert and Ulbrich(2018)] of hyperprop-
erties [Clarkson and Schneider(2010)]. The standard method for relational pro-
gram verification is to reduce it to nonrelational program verification on a product
program that simulates both traces together [Barthe et al.(2011),Lahiri et al.(2013),Zaks and Pnueli(2008)].
The approach taken in this paper is more similar to tools that verify relational
properties directly, without constructing a product program [Tiraboschi et al.(2023),Farina et al.(2019),Kolesar
20     Matthew Sotoudeh

Ordering States. Partial order reduction, abstraction, bisimulation, symmetry-
breaking, and state merging all involve establishing an order on program states [Abdulla et al.(1996),Ip and Dill(
These methods generally require much stronger orderings on the traces, and give
much stronger guarantees. E.g., [Abdulla et al.(1996)] guarantees completeness
when there is a well-ordering between reachable traces. In particular, ordering
traces according to their length, heap size, or input size does not meet their
requirements. As their results generally apply to temporal analyses, our scape-
goating size descent approach is orthogonal and complementary.

Completeness Thresholds and Small Model Properties. Our approach of reduc-
ing the size of crash traces is similar the goal of completeness thresholds re-
search [Clarke et al.(2004),Kroening et al.(2011),Bundala et al.(2012)]. Existing
work in that area does not immediately apply to heap-manipulating C pro-
grams. Small model properties are a similar notion in the automated reason-
ing community [Pnueli et al.(2002)] including some results for polymorphic pro-
grams [Bernardy et al.(2010),(Favonia) and Wang(2022)] and theories modeling
the heap [David et al.(2015),Ranise and Zarba(2006),Madhusudan et al.(2011)].

Non-Temporal Analyses. [Beckman et al.(2010)] use concrete tests to prove pro-
gram properties, where the tests are generated dynamically by a verification
engine. [An et al.(2011)] show how to soundly infer static types from finitely
many test executions. [Mathur et al.(2020),Mathur et al.(2019)] show that prov-
ing properties of a restricted class of heap-manipulating imperative programs is
decidable. [Kincaid et al.(2021)] translates the program to a set of recurrence re-
lations and tries to find a closed-form solution implying correctness properties.

Testing and BMC. Testing [Fioraldi et al.(2020),Li et al.(2018),George and Williams(2003),Howden(1991),Kin
cannot directly rule out the existence of bugs on inputs not tested. Ways to pick
test inputs are known [Kuhn et al.(2020),Ostrand and Balcer(1988),Grochtmann and Grimm(1993),Ivankovic e
and our work can be interpreted as a method for proving, for a particular pro-
gram, that the small scope hypothesis holds [Andoni et al.(2003),Jackson(2019)].
Bounded model checking tools can prove a property holds for every program
trace up to a certain length [King(1976),Khazem and Tautschnig(2019)]. When
used as a bug checker, scapegoating size descent tends to report bugs quicker
than BMC because it uses an abstraction, i.e., it is allowed to report false alarms.
But in practice BMC can usually detect buggy variants of our MDSTs in a few
seconds, and gives counterexamples. Hence the real challenge for these instances,
and benefit of Shrinker, is in proving safety.

Manual Program Analysis. Logics and tools for manually proving correctness ex-
ist [Floyd(1967),Hoare(1969),Cohen et al.(2009),Chen et al.(2015),Boutillier et al.(2014)].
In contrast to our fully automated approach, manual proof tools require the
programmer to annotate the code with loop invariants. [O’Hearn et al.(2001)],
[Piskac et al.(2013)], and [Itzhaky et al.(2013)] can express heap invariants.
        Automated Verification of Monotonic Data Structure Traversals in C        21

Acknowledgements I would like to thank the anonymous reviewers, whose
suggestions have dramatically improved the quality of the paper; Dawson Engler,
Alex Ozdemir, Clark Barrett, David K. Zhang, Geoff Ramseyer, Alex Aiken,
Martin Brain, and Aditya V. Thakur for extended discussions affecting and/or
significant feedback improving this work; as well as Zachary Yedidia, Akshay
Srivatsan, and attendees of the Stanford software lunch, who provided helpful
insights, conversations, and proofreading. This work was generously funded via
grants NSF DGE-1656518 and Stanford IOG Research Hub 281101-1-UDCPQ
298911.

Disclosure of Interests This work was generously funded via grants NSF
DGE-1656518 and Stanford IOG Research Hub 281101-1-UDCPQ 298911.


References
gli(2023). 2023. The GNU C Library (glibc). https://www.gnu.org/software/libc/.
lin(2023). 2023. The Linux Kernel Archives. https://kernel.org/.
net(2024). 2024. The NetBSD Project. https://www.netbsd.org/.
git(2025). 2025. Git. https://git-scm.com/.
gli(2025). 2025. GNOME / glib. https://gitlab.gnome.org/GNOME/glib.
mus(2025). 2025. musl libc. https://musl.libc.org/.
ope(2025). 2025. OpenBSD. https://www.openbsd.org/.
qem(2025). 2025. QEMU. https://www.qemu.org/.
red(2025). 2025. Redis - The Real-Time Data Platform. https://redis.io/.
zsh(2025). 2025. Zsh. https://www.zsh.org/.
Abdulla et al.(2014). Parosh Aziz Abdulla, Stavros Aronis, Bengt Jonsson, and Kon-
     stantinos Sagonas. 2014. Optimal dynamic partial order reduction. In The 41st
     Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
     guages, POPL ’14, San Diego, CA, USA, January 20-21, 2014, Suresh Jagan-
     nathan and Peter Sewell (Eds.). ACM, 373–384. https://doi.org/10.1145/
     2535838.2535845
Abdulla et al.(2009). Parosh Aziz Abdulla, Muhsin Atto, Jonathan Cederberg, and
     Ran Ji. 2009. Automated Analysis of Data-Dependent Programs with Dynamic
     Memory. In Automated Technology for Verification and Analysis, 7th International
     Symposium, ATVA 2009, Macao, China, October 14-16, 2009. Proceedings (Lecture
     Notes in Computer Science, Vol. 5799), Zhiming Liu and Anders P. Ravn (Eds.).
     Springer, 197–212. https://doi.org/10.1007/978-3-642-04761-9_16
Abdulla et al.(2008). Parosh Aziz Abdulla, Ahmed Bouajjani, Jonathan Cederberg,
     Frédéric Haziza, and Ahmed Rezine. 2008. Monotonic Abstraction for Programs
     with Dynamic Memory Heaps. In Computer Aided Verification, 20th International
     Conference, CAV 2008, Princeton, NJ, USA, July 7-14, 2008, Proceedings (Lecture
     Notes in Computer Science, Vol. 5123), Aarti Gupta and Sharad Malik (Eds.).
     Springer, 341–354. https://doi.org/10.1007/978-3-540-70545-1_33
Abdulla et al.(1996). Parosh Aziz Abdulla, Karlis Cerans, Bengt Jonsson, and Yih-
     Kuen Tsay. 1996. General Decidability Theorems for Infinite-State Systems. In
     Proceedings, 11th Annual IEEE Symposium on Logic in Computer Science, New
     Brunswick, New Jersey, USA, July 27-30, 1996. IEEE Computer Society, 313–321.
     https://doi.org/10.1109/LICS.1996.561359
22      Matthew Sotoudeh

Abdulla et al.(2016). Parosh Aziz Abdulla, Frédéric Haziza, and Lukás Holík. 2016.
    Parameterized verification through view abstraction. Int. J. Softw. Tools Technol.
    Transf. 18, 5 (2016), 495–516. https://doi.org/10.1007/s10009-015-0406-x
An et al.(2011). Jong-hoon (David) An, Avik Chaudhuri, Jeffrey S. Foster, and
    Michael Hicks. 2011. Dynamic inference of static types for ruby. In Proceedings
    of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of Programming
    Languages, POPL 2011, Austin, TX, USA, January 26-28, 2011, Thomas Ball
    and Mooly Sagiv (Eds.). ACM, 459–472. https://doi.org/10.1145/1926385.
    1926437
Andoni et al.(2003). Alexandr Andoni, Dumitru Daniliuc, Sarfraz Khurshid, and
    Darko Marinov. 2003. Evaluating the “small scope hypothesis”. In In Popl, Vol. 2.
    Citeseer.
Ball(2004). Thomas Ball. 2004. A Theory of Predicate-Complete Test Coverage and
    Generation. In Formal Methods for Components and Objects, Third International
    Symposium, FMCO 2004, Leiden, The Netherlands, November 2 - 5, 2004, Re-
    vised Lectures (Lecture Notes in Computer Science, Vol. 3657), Frank S. de Boer,
    Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever (Eds.). Springer,
    1–22. https://doi.org/10.1007/11561163_1
Barthe et al.(2011). Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2011. Re-
    lational Verification Using Product Programs. In FM 2011: Formal Methods -
    17th International Symposium on Formal Methods, Limerick, Ireland, June 20-
    24, 2011. Proceedings (Lecture Notes in Computer Science, Vol. 6664), Michael J.
    Butler and Wolfram Schulte (Eds.). Springer, 200–214. https://doi.org/10.
    1007/978-3-642-21437-0_17
Beckert and Ulbrich(2018). Bernhard Beckert and Mattias Ulbrich. 2018. Trends in
    Relational Program Verification. In Principled Software Development - Essays
    Dedicated to Arnd Poetzsch-Heffter on the Occasion of his 60th Birthday, Peter
    Müller and Ina Schaefer (Eds.). Springer, 41–58. https://doi.org/10.1007/
    978-3-319-98047-8_3
Beckman et al.(2010). Nels E. Beckman, Aditya V. Nori, Sriram K. Rajamani,
    Robert J. Simmons, SaiDeep Tetali, and Aditya V. Thakur. 2010. Proofs from
    Tests. IEEE Trans. Software Eng. 36, 4 (2010), 495–508. https://doi.org/10.
    1109/TSE.2010.49
Bernardy et al.(2010). Jean-Philippe Bernardy, Patrik Jansson, and Koen Claessen.
    2010. Testing Polymorphic Properties. In Programming Languages and Sys-
    tems, 19th European Symposium on Programming, ESOP 2010, Held as Part
    of the Joint European Conferences on Theory and Practice of Software, ETAPS
    2010, Paphos, Cyprus, March 20-28, 2010. Proceedings (Lecture Notes in Com-
    puter Science, Vol. 6012), Andrew D. Gordon (Ed.). Springer, 125–144. https:
    //doi.org/10.1007/978-3-642-11957-6_8
Blanchet et al.(2002). Bruno Blanchet, Patrick Cousot, Radhia Cousot, Jérôme Feret,
    Laurent Mauborgne, Antoine Miné, David Monniaux, and Xavier Rival. 2002. De-
    sign and Implementation of a Special-Purpose Static Program Analyzer for Safety-
    Critical Real-Time Embedded Software. In The Essence of Computation, Complex-
    ity, Analysis, Transformation. Essays Dedicated to Neil D. Jones [on occasion of
    his 60th birthday] (Lecture Notes in Computer Science, Vol. 2566), Torben Æ.
    Mogensen, David A. Schmidt, and Ivan Hal Sudborough (Eds.). Springer, 85–108.
    https://doi.org/10.1007/3-540-36377-7_5
Boonstoppel et al.(2008). Peter Boonstoppel, Cristian Cadar, and Dawson R. En-
    gler. 2008. RWset: Attacking Path Explosion in Constraint-Based Test Gener-
        Automated Verification of Monotonic Data Structure Traversals in C        23

    ation. In Tools and Algorithms for the Construction and Analysis of Systems,
    14th International Conference, TACAS 2008, Held as Part of the Joint Euro-
    pean Conferences on Theory and Practice of Software, ETAPS 2008, Budapest,
    Hungary, March 29-April 6, 2008. Proceedings (Lecture Notes in Computer Sci-
    ence, Vol. 4963), C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer, 351–366.
    https://doi.org/10.1007/978-3-540-78800-3_27
Boutillier et al.(2014). Pierre Boutillier, Stephane Glondu, Benjamin Grégoire, Hugo
    Herbelin, Pierre Letouzey, Pierre-Marie Pédrot, Yann Régis-Gianas, Matthieu
    Sozeau, Arnaud Spiwack, and Enrico Tassi. 2014. Coq 8.4 Reference Manual.
    Research Report. Inria. https://inria.hal.science/hal-01114602 The Coq
    Development Team.
Brat et al.(2014). Guillaume Brat, Jorge A. Navas, Nija Shi, and Arnaud Venet. 2014.
    IKOS: A Framework for Static Analysis Based on Abstract Interpretation. In Soft-
    ware Engineering and Formal Methods - 12th International Conference, SEFM
    2014, Grenoble, France, September 1-5, 2014. Proceedings (Lecture Notes in Com-
    puter Science, Vol. 8702), Dimitra Giannakopoulou and Gwen Salaün (Eds.).
    Springer, 271–277. https://doi.org/10.1007/978-3-319-10431-7_20
Brotherston(2005). James Brotherston. 2005. Cyclic Proofs for First-Order Logic
    with Inductive Definitions. In Automated Reasoning with Analytic Tableaux and
    Related Methods, International Conference, TABLEAUX 2005, Koblenz, Ger-
    many, September 14-17, 2005, Proceedings (Lecture Notes in Computer Science,
    Vol. 3702), Bernhard Beckert (Ed.). Springer, 78–92. https://doi.org/10.1007/
    11554554_8
Brotherston et al.(2012). James Brotherston, Nikos Gorogiannis, and Ras-
    mus Lerchedahl Petersen. 2012. A Generic Cyclic Theorem Prover. In Pro-
    gramming Languages and Systems - 10th Asian Symposium, APLAS 2012,
    Kyoto, Japan, December 11-13, 2012. Proceedings (Lecture Notes in Computer
    Science, Vol. 7705), Ranjit Jhala and Atsushi Igarashi (Eds.). Springer, 350–367.
    https://doi.org/10.1007/978-3-642-35182-2_25
Bundala et al.(2012). Daniel Bundala, Joël Ouaknine, and James Worrell. 2012. On
    the Magnitude of Completeness Thresholds in Bounded Model Checking. In Pro-
    ceedings of the 27th Annual IEEE Symposium on Logic in Computer Science, LICS
    2012, Dubrovnik, Croatia, June 25-28, 2012. IEEE Computer Society, 155–164.
    https://doi.org/10.1109/LICS.2012.27
Cadar et al.(2006). Cristian Cadar, Vijay Ganesh, Peter M. Pawlowski, David L. Dill,
    and Dawson R. Engler. 2006. EXE: automatically generating inputs of death.
    In Proceedings of the 13th ACM Conference on Computer and Communications
    Security, CCS 2006, Alexandria, VA, USA, October 30 - November 3, 2006, Ari
    Juels, Rebecca N. Wright, and Sabrina De Capitani di Vimercati (Eds.). ACM,
    322–335. https://doi.org/10.1145/1180405.1180445
Calcagno et al.(2009). Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and
    Hongseok Yang. 2009. Compositional shape analysis by means of bi-abduction.
    In Proceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of
    Programming Languages, POPL 2009, Savannah, GA, USA, January 21-23, 2009,
    Zhong Shao and Benjamin C. Pierce (Eds.). ACM, 289–300. https://doi.org/
    10.1145/1480881.1480917
Chakraborty et al.(2020). Supratik Chakraborty, Ashutosh Gupta, and Divyesh Un-
    adkat. 2020. Verifying Array Manipulating Programs with Full-Program In-
    duction. In Tools and Algorithms for the Construction and Analysis of Systems
    - 26th International Conference, TACAS 2020, Held as Part of the European
24      Matthew Sotoudeh

    Joint Conferences on Theory and Practice of Software, ETAPS 2020, Dublin, Ire-
    land, April 25-30, 2020, Proceedings, Part I (Lecture Notes in Computer Science,
    Vol. 12078), Armin Biere and David Parker (Eds.). Springer, 22–39. https:
    //doi.org/10.1007/978-3-030-45190-5_2
Chakraborty et al.(2021). Supratik Chakraborty, Ashutosh Gupta, and Divyesh Un-
    adkat. 2021. Diffy: Inductive Reasoning of Array Programs Using Difference Invari-
    ants. In Computer Aided Verification - 33rd International Conference, CAV 2021,
    Virtual Event, July 20-23, 2021, Proceedings, Part II (Lecture Notes in Computer
    Science, Vol. 12760), Alexandra Silva and K. Rustan M. Leino (Eds.). Springer,
    911–935. https://doi.org/10.1007/978-3-030-81688-9_42
Chen et al.(2015). Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala,
    M. Frans Kaashoek, and Nickolai Zeldovich. 2015. Using Crash Hoare logic for
    certifying the FSCQ file system. In Proceedings of the 25th Symposium on Oper-
    ating Systems Principles, SOSP 2015, Monterey, CA, USA, October 4-7, 2015,
    Ethan L. Miller and Steven Hand (Eds.). ACM, 18–37. https://doi.org/10.
    1145/2815400.2815402
Clarke et al.(1986). Edmund M. Clarke, Orna Grumberg, and Michael C. Browne.
    1986. Reasoning About Networks With Many Identical Finite-State Processes.
    In Proceedings of the Fifth Annual ACM Symposium on Principles of Distributed
    Computing, Calgary, Alberta, Canada, August 11-13, 1986, Joseph Y. Halpern
    (Ed.). ACM, 240–248. https://doi.org/10.1145/10590.10611
Clarke et al.(1994). Edmund M. Clarke, Orna Grumberg, and David E. Long. 1994.
    Model Checking and Abstraction. ACM Trans. Program. Lang. Syst. 16, 5 (1994),
    1512–1542. https://doi.org/10.1145/186025.186051
Clarke et al.(2004). Edmund M. Clarke, Daniel Kroening, Joël Ouaknine, and Ofer
    Strichman. 2004. Completeness and Complexity of Bounded Model Checking. In
    Verification, Model Checking, and Abstract Interpretation, 5th International Con-
    ference, VMCAI 2004, Venice, Italy, January 11-13, 2004, Proceedings (Lecture
    Notes in Computer Science, Vol. 2937), Bernhard Steffen and Giorgio Levi (Eds.).
    Springer, 85–96. https://doi.org/10.1007/978-3-540-24622-0_9
Clarkson and Schneider(2010). Michael R. Clarkson and Fred B. Schneider. 2010. Hy-
    perproperties. J. Comput. Secur. 18, 6 (2010), 1157–1210. https://doi.org/10.
    3233/JCS-2009-0393
Cohen et al.(2009). Ernie Cohen, Markus Dahlweid, Mark A. Hillebrand, Dirk Leinen-
    bach, Michal Moskal, Thomas Santen, Wolfram Schulte, and Stephan Tobies.
    2009. VCC: A Practical System for Verifying Concurrent C. In Theorem Proving
    in Higher Order Logics, 22nd International Conference, TPHOLs 2009, Munich,
    Germany, August 17-20, 2009. Proceedings (Lecture Notes in Computer Science,
    Vol. 5674), Stefan Berghofer, Tobias Nipkow, Christian Urban, and Makarius Wen-
    zel (Eds.). Springer, 23–42. https://doi.org/10.1007/978-3-642-03359-9_2
Cormen et al.(2009). Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and
    Clifford Stein. 2009. Introduction to Algorithms, Third Edition (3rd ed.). The MIT
    Press.
Cousot and Cousot(1977). Patrick Cousot and Radhia Cousot. 1977. Abstract Inter-
    pretation: A Unified Lattice Model for Static Analysis of Programs by Construction
    or Approximation of Fixpoints. In Conference Record of the Fourth ACM Sym-
    posium on Principles of Programming Languages, Los Angeles, California, USA,
    January 1977, Robert M. Graham, Michael A. Harrison, and Ravi Sethi (Eds.).
    ACM, 238–252. https://doi.org/10.1145/512950.512973
        Automated Verification of Monotonic Data Structure Traversals in C             25

Darke et al.(2023). Priyanka Darke, Bharti Chimdyalwar, Sakshi Agrawal, Shrawan
    Kumar, R. Venkatesh, and Supratik Chakraborty. 2023. VeriAbsL: Scalable Ver-
    ification by Abstraction and Strategy Prediction (Competition Contribution). In
    Tools and Algorithms for the Construction and Analysis of Systems - 29th Interna-
    tional Conference, TACAS 2023, Held as Part of the European Joint Conferences
    on Theory and Practice of Software, ETAPS 2022, Paris, France, April 22-27,
    2023, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 13994), Sri-
    ram Sankaranarayanan and Natasha Sharygina (Eds.). Springer, 588–593. https:
    //doi.org/10.1007/978-3-031-30820-8_41
David et al.(2015). Cristina David, Daniel Kroening, and Matt Lewis. 2015. Proposi-
    tional Reasoning about Safety and Termination of Heap-Manipulating Programs.
    In Programming Languages and Systems - 24th European Symposium on Program-
    ming, ESOP 2015, Held as Part of the European Joint Conferences on Theory
    and Practice of Software, ETAPS 2015, London, UK, April 11-18, 2015. Proceed-
    ings (Lecture Notes in Computer Science, Vol. 9032), Jan Vitek (Ed.). Springer,
    661–684. https://doi.org/10.1007/978-3-662-46669-8_27
Farina et al.(2019). Gian Pietro Farina, Stephen Chong, and Marco Gaboardi. 2019.
    Relational Symbolic Execution. In Proceedings of the 21st International Sympo-
    sium on Principles and Practice of Programming Languages, PPDP 2019, Porto,
    Portugal, October 7-9, 2019, Ekaterina Komendantskaya (Ed.). ACM, 10:1–10:14.
    https://doi.org/10.1145/3354166.3354175
(Favonia) and Wang(2022). Kuen-Bang Hou (Favonia) and Zhuyang Wang. 2022. Log-
    arithm and program testing. Proc. ACM Program. Lang. 6, POPL (2022), 1–26.
    https://doi.org/10.1145/3498726
Fioraldi et al.(2020). Andrea Fioraldi, Dominik Maier, Heiko Eißfeldt, and Marc
    Heuse. 2020. AFL++ : Combining Incremental Steps of Fuzzing Research. In
    14th USENIX Workshop on Offensive Technologies, WOOT 2020, August 11,
    2020, Yuval Yarom and Sarah Zennou (Eds.). USENIX Association.                 https:
    //www.usenix.org/conference/woot20/presentation/fioraldi
Flanagan and Godefroid(2005). Cormac Flanagan and Patrice Godefroid. 2005. Dy-
    namic partial-order reduction for model checking software. In Proceedings of the
    32nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
    guages, POPL 2005, Long Beach, California, USA, January 12-14, 2005, Jens
    Palsberg and Martín Abadi (Eds.). ACM, 110–121. https://doi.org/10.1145/
    1040305.1040315
Floyd(1967). Robert W Floyd. 1967. Assigning meanings to programs. American
    Mathematical Society (1967).
George and Williams(2003). Boby George and Laurie A. Williams. 2003. An Initial
    Investigation of Test Driven Development in Industry. In Proceedings of the 2003
    ACM Symposium on Applied Computing (SAC), March 9-12, 2003, Melbourne, FL,
    USA, Gary B. Lamont, Hisham Haddad, George A. Papadopoulos, and Brajendra
    Panda (Eds.). ACM, 1135–1139. https://doi.org/10.1145/952532.952753
Greitschus et al.(2017). Marius Greitschus, Daniel Dietsch, and Andreas Podelski.
    2017. Loop Invariants from Counterexamples. In Static Analysis - 24th Interna-
    tional Symposium, SAS 2017, New York, NY, USA, August 30 - September 1, 2017,
    Proceedings (Lecture Notes in Computer Science, Vol. 10422), Francesco Ranzato
    (Ed.). Springer, 128–147. https://doi.org/10.1007/978-3-319-66706-5_7
Grochtmann and Grimm(1993). Matthias Grochtmann and Klaus Grimm. 1993. Clas-
    sification Trees for Partition Testing. Softw. Test. Verification Reliab. 3, 2 (1993),
    63–82. https://doi.org/10.1002/stvr.4370030203
26      Matthew Sotoudeh

Hoare(1969). C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming.
    Commun. ACM 12, 10 (1969), 576–580.           https://doi.org/10.1145/363235.
    363259
Howden(1991). William E. Howden. 1991. Program Testing versus Proofs of Correct-
    ness. Softw. Test. Verification Reliab. 1, 1 (1991), 5–15. https://doi.org/10.
    1002/stvr.4370010103
Ip and Dill(1996). C. Norris Ip and David L. Dill. 1996. Better Verification Through
    Symmetry. Formal Methods Syst. Des. 9, 1/2 (1996), 41–75. https://doi.org/
    10.1007/BF00625968
Ish-Shalom et al.(2020). Oren Ish-Shalom, Shachar Itzhaky, Noam Rinetzky, and
    Sharon Shoham. 2020. Putting the squeeze on array programs: Loop verification
    via inductive rank reduction. In International Conference on Verification, Model
    Checking, and Abstract Interpretation. Springer, 112–135.
Itzhaky et al.(2013). Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Aleksan-
    dar Nanevski, and Mooly Sagiv. 2013. Effectively-Propositional Reasoning about
    Reachability in Linked Data Structures. In Computer Aided Verification - 25th In-
    ternational Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013.
    Proceedings (Lecture Notes in Computer Science, Vol. 8044), Natasha Shary-
    gina and Helmut Veith (Eds.). Springer, 756–772. https://doi.org/10.1007/
    978-3-642-39799-8_53
Ivankovic et al.(2019). Marko Ivankovic, Goran Petrovic, René Just, and Gordon
    Fraser. 2019. Code coverage at Google. In Proceedings of the ACM Joint Meeting
    on European Software Engineering Conference and Symposium on the Foundations
    of Software Engineering, ESEC/SIGSOFT FSE 2019, Tallinn, Estonia, August 26-
    30, 2019, Marlon Dumas, Dietmar Pfahl, Sven Apel, and Alessandra Russo (Eds.).
    ACM, 955–963. https://doi.org/10.1145/3338906.3340459
Jackson(2019). Daniel Jackson. 2019. Alloy: a language and tool for exploring software
    designs. Commun. ACM 62, 9 (2019), 66–76. https://doi.org/10.1145/3338843
Jeannet and Miné(2009). Bertrand Jeannet and Antoine Miné. 2009. Apron: A library
    of numerical abstract domains for static analysis. In International Conference on
    Computer Aided Verification. Springer, 661–667.
Khazem and Tautschnig(2019). Kareem Khazem and Michael Tautschnig. 2019.
    CBMC Path: A Symbolic Execution Retrofit of the C Bounded Model Checker
    - (Competition Contribution). In Tools and Algorithms for the Construction and
    Analysis of Systems - 25 Years of TACAS: TOOLympics, Held as Part of ETAPS
    2019, Prague, Czech Republic, April 6-11, 2019, Proceedings, Part III (Lecture
    Notes in Computer Science, Vol. 11429), Dirk Beyer, Marieke Huisman, Fabrice
    Kordon, and Bernhard Steffen (Eds.). Springer, 199–203. https://doi.org/10.
    1007/978-3-030-17502-3_13
Kincaid et al.(2021). Zachary Kincaid, Thomas W. Reps, and John Cyphert. 2021.
    Algebraic Program Analysis. In Computer Aided Verification - 33rd International
    Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part I (Lec-
    ture Notes in Computer Science, Vol. 12759), Alexandra Silva and K. Rustan M.
    Leino (Eds.). Springer, 46–83. https://doi.org/10.1007/978-3-030-81685-8_3
King(1976). James C. King. 1976. Symbolic Execution and Program Testing. Com-
    mun. ACM 19, 7 (1976), 385–394. https://doi.org/10.1145/360248.360252
Kolesar et al.(2022). John C. Kolesar, Ruzica Piskac, and William T. Hallahan. 2022.
    Checking equivalence in a non-strict language. Proc. ACM Program. Lang. 6,
    OOPSLA2 (2022), 1469–1496. https://doi.org/10.1145/3563340
        Automated Verification of Monotonic Data Structure Traversals in C           27

Kroening et al.(2011). Daniel Kroening, Joël Ouaknine, Ofer Strichman, Thomas
    Wahl, and James Worrell. 2011. Linear Completeness Thresholds for Bounded
    Model Checking. In Computer Aided Verification - 23rd International Conference,
    CAV 2011, Snowbird, UT, USA, July 14-20, 2011. Proceedings (Lecture Notes in
    Computer Science, Vol. 6806), Ganesh Gopalakrishnan and Shaz Qadeer (Eds.).
    Springer, 557–572. https://doi.org/10.1007/978-3-642-22110-1_44
Kuhn et al.(2020). Rick Kuhn, Raghu N. Kacker, Yu Lei, and Dimitris E. Simos. 2020.
    Input Space Coverage Matters. Computer 53, 1 (2020), 37–44. https://doi.org/
    10.1109/MC.2019.2951980
Lahiri et al.(2013). Shuvendu K. Lahiri, Kenneth L. McMillan, Rahul Sharma, and
    Chris Hawblitzel. 2013. Differential assertion checking. In Joint Meeting of the Eu-
    ropean Software Engineering Conference and the ACM SIGSOFT Symposium on
    the Foundations of Software Engineering, ESEC/FSE’13, Saint Petersburg, Rus-
    sian Federation, August 18-26, 2013, Bertrand Meyer, Luciano Baresi, and Mira
    Mezini (Eds.). ACM, 345–355. https://doi.org/10.1145/2491411.2491452
Li et al.(2018). Jun Li, Bodong Zhao, and Chao Zhang. 2018. Fuzzing: a survey. Cy-
    bersecur. 1, 1 (2018), 6. https://doi.org/10.1186/s42400-018-0002-y
Lucanu and Rosu(2007). Dorel Lucanu and Grigore Rosu. 2007. CIRC : A Circular
    Coinductive Prover. In Algebra and Coalgebra in Computer Science, Second In-
    ternational Conference, CALCO 2007, Bergen, Norway, August 20-24, 2007, Pro-
    ceedings (Lecture Notes in Computer Science, Vol. 4624), Till Mossakowski, Ugo
    Montanari, and Magne Haveraaen (Eds.). Springer, 372–378. https://doi.org/
    10.1007/978-3-540-73859-6_25
Madhusudan et al.(2011). P. Madhusudan, Gennaro Parlato, and Xiaokang Qiu. 2011.
    Decidable logics combining heap structures and data. In Proceedings of the 38th
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    POPL 2011, Austin, TX, USA, January 26-28, 2011, Thomas Ball and Mooly
    Sagiv (Eds.). ACM, 611–622. https://doi.org/10.1145/1926385.1926455
Malík et al.(2018). Viktor Malík, Martin Hruska, Peter Schrammel, and Tomás Voj-
    nar. 2018. Template-Based Verification of Heap-Manipulating Programs. In 2018
    Formal Methods in Computer Aided Design, FMCAD 2018, Austin, TX, USA, Oc-
    tober 30 - November 2, 2018, Nikolaj S. Bjørner and Arie Gurfinkel (Eds.). IEEE,
    1–9. https://doi.org/10.23919/FMCAD.2018.8603009
Mathur et al.(2019). Umang Mathur, P. Madhusudan, and Mahesh Viswanathan.
    2019. Decidable verification of uninterpreted programs. Proc. ACM Program.
    Lang. 3, POPL (2019), 46:1–46:29. https://doi.org/10.1145/3290359
Mathur et al.(2020). Umang Mathur, Adithya Murali, Paul Krogmeier, P. Madhusu-
    dan, and Mahesh Viswanathan. 2020. Deciding memory safety for single-pass heap-
    manipulating programs. Proc. ACM Program. Lang. 4, POPL (2020), 35:1–35:29.
    https://doi.org/10.1145/3371103
O’Hearn et al.(2001). Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang.
    2001. Local Reasoning about Programs that Alter Data Structures. In Com-
    puter Science Logic, 15th International Workshop, CSL 2001. 10th Annual Con-
    ference of the EACSL, Paris, France, September 10-13, 2001, Proceedings (Lecture
    Notes in Computer Science, Vol. 2142), Laurent Fribourg (Ed.). Springer, 1–19.
    https://doi.org/10.1007/3-540-44802-0_1
Ostrand and Balcer(1988). Thomas J. Ostrand and Marc J. Balcer. 1988. The
    Category-Partition Method for Specifying and Generating Functional Tests. Com-
    mun. ACM 31, 6 (1988), 676–686. https://doi.org/10.1145/62959.62964
28      Matthew Sotoudeh

Piskac et al.(2013). Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2013. Au-
    tomating Separation Logic Using SMT. In Computer Aided Verification - 25th In-
    ternational Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013.
    Proceedings (Lecture Notes in Computer Science, Vol. 8044), Natasha Shary-
    gina and Helmut Veith (Eds.). Springer, 773–789. https://doi.org/10.1007/
    978-3-642-39799-8_54
Pnueli et al.(2002). Amir Pnueli, Yoav Rodeh, Ofer Strichman, and Michael Siegel.
    2002. The Small Model Property: How Small Can It Be? Inf. Comput. 178, 1
    (2002), 279–293. https://doi.org/10.1006/inco.2002.3175
Ranise and Zarba(2006). Silvio Ranise and Calogero G. Zarba. 2006. A Theory of
    Singly-Linked Lists and its Extensible Decision Procedure. In Fourth IEEE In-
    ternational Conference on Software Engineering and Formal Methods (SEFM
    2006), 11-15 September 2006, Pune, India. IEEE Computer Society, 206–215.
    https://doi.org/10.1109/SEFM.2006.7
Sagiv et al.(1999). Shmuel Sagiv, Thomas W. Reps, and Reinhard Wilhelm. 1999.
    Parametric Shape Analysis via 3-Valued Logic. In POPL ’99, Proceedings of the
    26th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
    guages, San Antonio, TX, USA, January 20-22, 1999, Andrew W. Appel and
    Alex Aiken (Eds.). ACM, 105–118. https://doi.org/10.1145/292540.292552
Sen(2009). Koushik Sen. 2009. DART: Directed Automated Random Testing. In
    Hardware and Software: Verification and Testing - 5th International Haifa Ver-
    ification Conference, HVC 2009, Haifa, Israel, October 19-22, 2009, Revised Se-
    lected Papers (Lecture Notes in Computer Science, Vol. 6405), Kedar S. Namjoshi,
    Andreas Zeller, and Avi Ziv (Eds.). Springer, 4. https://doi.org/10.1007/
    978-3-642-19237-1_4
Soková et al.(2023). Veronika Soková, Petr Peringer, Tomás Vojnar, and Ondrej
    Kinst. 2023. PredatorHP (Version 3.1415). https://doi.org/10.5281/zenodo.
    10183805. https://doi.org/10.5281/ZENODO.10183805 Accessed on YYYY-
    MM-DD..
Sotin and Rival(2012). Pascal Sotin and Xavier Rival. 2012. Hierarchical Shape Ab-
    straction of Dynamic Structures in Static Blocks. In Programming Languages and
    Systems - 10th Asian Symposium, APLAS 2012, Kyoto, Japan, December 11-
    13, 2012. Proceedings (Lecture Notes in Computer Science, Vol. 7705), Ranjit
    Jhala and Atsushi Igarashi (Eds.). Springer, 131–147. https://doi.org/10.1007/
    978-3-642-35182-2_10
Tiraboschi et al.(2023). Ignacio Tiraboschi, Tamara Rezk, and Xavier Rival. 2023.
    Sound Symbolic Execution via Abstract Interpretation and Its Application to Se-
    curity. In Verification, Model Checking, and Abstract Interpretation - 24th Inter-
    national Conference, VMCAI 2023, Boston, MA, USA, January 16-17, 2023, Pro-
    ceedings (Lecture Notes in Computer Science, Vol. 13881), Cezara Dragoi, Michael
    Emmi, and Jingbo Wang (Eds.). Springer, 267–295. https://doi.org/10.1007/
    978-3-031-24950-1_13
Wesley et al.(2021). Scott Wesley, Maria Christakis, Jorge A. Navas, Richard J. Tre-
    fler, Valentin Wüstholz, and Arie Gurfinkel. 2021. Compositional Verification of
    Smart Contracts Through Communication Abstraction. In Static Analysis - 28th
    International Symposium, SAS 2021, Chicago, IL, USA, October 17-19, 2021,
    Proceedings (Lecture Notes in Computer Science, Vol. 12913), Cezara Dragoi,
    Suvam Mukherjee, and Kedar S. Namjoshi (Eds.). Springer, 429–452. https:
    //doi.org/10.1007/978-3-030-88806-0_21
       Automated Verification of Monotonic Data Structure Traversals in C   29

Zaks and Pnueli(2008). Anna Zaks and Amir Pnueli. 2008. CoVaC: Compiler Val-
   idation by Program Analysis of the Cross-Product. In FM 2008: Formal Meth-
   ods, 15th International Symposium on Formal Methods, Turku, Finland, May 26-
   30, 2008, Proceedings (Lecture Notes in Computer Science, Vol. 5014), Jorge
   Cuéllar, T. S. E. Maibaum, and Kaisa Sere (Eds.). Springer, 35–51. https:
   //doi.org/10.1007/978-3-540-68237-0_5
30      Matthew Sotoudeh

A     Additional Implementation Details
This section complements Section 5 with more details on the heuristics imple-
mented by Shrinker. Many of the subsections refer directly to the heuristics
and routines called in Algorithm 2; the reader should refer to Section 4.3 for
the requirements placed on each one. Below we use pc to refer to the program
counter, i.e., what the next instruction (line) to be executed is.

A.1    Abstract Paths
To assist in the heuristics we associate each abstract herd with a abstract path
indicating the sequence of instructions associated with selected states in the
primary trace. For example, an abstract herd having associated abstract path
p1, p3, *, p7, *, p8 indicates that every primary trace of every herd in its
concretization set has pc=p1 in its first state, then pc=p3 in its second, then zero
or more other states (e.g., many executions of a loop), then a state with pc=p7,
then zero or more other states, and finally a state with pc=p8. The abstract
path is used to control precision loss and widening in our heuristics; see below
for more details. We replace loop iterations after a certain unrolling level with
* to ensure that the set of possible abstract paths is bounded (we may also do
this before the unrolling level is reached if a summary node is accessed by the
program; see below). Our implementation of HWiden works by joining states that
share the same abstract path, hence having a larger unrolling level makes the
analysis significantly more precise.

A.2    Scapegoat Construction (MaybeAddScapegoats)
Recall that we need a way to add scapegoat traces to the trace. Our strategy
waits until enough steps and splits have occurred to guarantee that the program
input has size greater than some user-specified size bound k (in our evaluation,
we start this size bound at k = 1 and retry with incrementally higher bounds if
it fails). Once we know the input is large enough, we apply one of two shrinking
rules to the first state of the primary to construct a new initial trace for the
scapegoat:
 1. If the input is a linked structure, we construct a scapegoat trace formed
    by removing one of the first k reachable nodes in the structure (updating
    the other pointers to skip over it). When k > 1, i.e., multiple nodes are
    guaranteed to be reachable, we add separate scapegoats skipping over each
    of them.
 2. If the input is an array, and it has length at least 1, we add a scapegoat trace
    formed by removing exactly one of the first k elements from the array. To
    do so, we decrement the array’s length, increment the pointer to the array’s
    first element, update the base and bound values used for memory checking,
    and then move elements among the first k to simulate deleting the desired
    element. Once again, we add a separate scapegoat for each of the k array
    elements that we consider deleting.
        Automated Verification of Monotonic Data Structure Traversals in C        31

The resulting scapegoat traces start off with only one, length-1 trace. Since drop-
ping the head of an array or skipping a node in a linked structure still results in a
valid inital trace, these operations satisfy the constraints on MaybeAddScapegoats.
Notably, all of this happens in the abstract, i.e., rather than constructing a con-
crete trace we add all of the constraints that would result from such a construc-
tion to our list of constraints.

A.3    Abstract Herd Splitting (HSplit)
After a branch operation on the primary trace, HSplit is used to partition the
abstract trace herd into separate abstract trace herds representing each possible
branch outcome. For example, if we encounter a branch that goes to pc=p5 when
x = 0 or pc=p8 otherwise, we will duplicate the abstract trace herd a′ into (1)
a′1 with the additional constraints “x = 0 and pc=p5 in the most recent state”
and (2) a′2 with the additional constraints “x ̸= 0 and pc=p8 in the most recent
state.” In this way, we always know the exact next-to-be-executed instruction
before calling HStep♯ .
    Furthermore, if the next instruction will access a pointer in the program (e.g.,
by dereferencing it or comparing it against another pointer), we also split on the
possible memory locations that the pointer could point to. In this way, HStep♯
always knows exactly which memory location is being referred to on all pointer
operations.

A.4    Stepping Operations (HStep♯ , HStep♯∃ )
We implement HStep♯ and HStep♯∃ by adding new constraints that relate values
in a new last state of the trace to those in the previously last (now second-to-last)
state. Every constraint previously referring to, e.g., “the second-to-last state” is
updated to refer to “the third-to-last state,” and new constraints are added to
define the now-last state. For HStep♯∃ (which is used to advance the non-primary,
scapegoat traces) we drop any scapegoat traces where the pc on the final state
of the trace is unknown. Note that HSplit is used to enforce a similar behavior
for HStep♯ , i.e., the primary trace. Thus for every abstract trace herd in the
worklist, we know the next instruction to be executed for all of the traces in
every herd in the concretization set.
    We allow the user to request nondeterministic values. HStep♯ implements this
by asserting equality between the output register and a fresh (unconstrained
except for type bounds) variable. Recall, however, that HStep♯∃ is allowed to
guess nondeterministic values. To do so, it identifies the most similar state in
the primary trace (using a heuristic based on local variables described below)
and asserts that the output register in the scapegoat trace takes on the same
value that was returned in that step of the primary trace.

A.5    Stepper Heuristic
Recall at each step we must determine how far to advance each of the scapegoat
traces. We annotate all the loops with ‘entrance,’ ‘iteration,’ and ‘end’ instruc-
32      Matthew Sotoudeh

tions, and associate each loop with the set of ‘relevant local variables,’ i.e., those
that it may write to in the loop body (e.g., an array iteration might write to a
counter i, a list traversal might write to a pointer l, etc.). We only ever advance
scapegoat traces after the primary has executed an ‘iteration’ instruction. Then
we apply HStep♯∃ repeatedly to advance the scapegoat trace until we can prove
that it (1) reaches the same iteration instruction and (2) the relevant local vari-
ables in the primary trace have the same values as those in the scapegoat trace
(a difference of 1 is allowed for integer variables to account for the fact that
we have have shrunk the input’s size by one). If a scapegoat trace ever reaches
a branch instruction where the branch to be taken is not already implied by
existing constraints, we remove that scapegoat trace from the herd.

A.6    State Querying (HCanFail, CanBlame, HMorePrecise)
HCanFail and CanBlame are implemented by checking whether the set of con-
straints implies the conditions needed: HCanFail checks whether the program
counter on the final state could be a failure operation, while CanBlame checks
whether the constraints imply both that the scapegoat trace has a smaller size
and definitely has the same failing program counter. HMorePrecise(a, b) is im-
plemented by checking whether every constraint in b is also in a.

A.7    Dataflow Optimizations
To minimize the amount of analysis that needs to be done by our scapegoating
size descent-based analysis, we apply simple dataflow-based optimizations first
to, e.g., elide obviously duplicate checks, eliminate common subexpressions, and
delete dead code. These optimizations are carefully designed to ensure that they
never remove a bug from the program, i.e., we can only remove a pointer validity
check if we know that it would only fail if some earlier pointer validity check
would have failed before reaching it.

A.8    Parallelization
One major optimization we applied to Algorithm 2 was to parallelize the main
loop. We start with one worker process that is running the algorithm in a se-
quential manner as described in Section 4. When fewer than some user-specified
maximum number of worker processes are running, worker processes will attempt
to split their worklists in two to use the idle machine cores; the two resulting
workers perform Algorithm 2 as normal, but only on their own half of the orig-
inal worker’s worklist. This parallelization of the main loop is sound (Lemma 3
still holds, guaranteeing that at least one worker processed an abstract herd
accounting for any given reachable trace), but can introduce nondeterminism if
done naïvely (because HWiden may rely on the other elements in the worklist
when deciding how much to widen). To avoid this, we only split off work when
we can guarantee that HWiden in one partition would never use the elements in
the other partition; because HWiden joins only elements with the same abstract
path, this corresponds to checking that their paths all have disjoint prefixes.
          Automated Verification of Monotonic Data Structure Traversals in C   33

A.9       Measure of Trace Size
Scapegoating size descent requires the analysis designer to specify the mea-
sure of trace size. The tool is sound regardless of this choice; it only affects
completeness. Ideally, the measure ensures that scapegoat traces (as added by
MaybeAddScapegoats, which in Shrinker drops one item from the input struc-
ture) are smaller than their primary. Shrinker takes the size to be the number
of allocated memory regions reachable from the input arguments plus the num-
ber of elements in arrays reachable from the input arguments plus the number
of times malloc was called. This captures the number of items allocated on
the heap, and does indeed get smaller as we drop elements from input struc-
tures. Otherwise, not much thought went into this choice. We have every reason
to expect the tool could perform as well with many different notions of size,
such as the number of bytes allocated on the heap or the length of the trace.
One practical benefit of counting the number of allocation regions rather than
raw number of bytes allocated or number of IR instructions executed is that it
was more interpretable when debugging Shrinker: dropping a single node in a
linked list input structure only changes the number of allocated regions by 1, but
it changes the raw number of allocated bytes by the difficult-to-eyeball quantity
sizeof(struct list_node) and changes the number of executed instructions
by an even harder-to-predict number.

A.10       Disjoint Heaps Only Applies to Harness
In Section 5 we described how the program is verified under the assumption
that the test harness is called with inputs that point to disjoint heaps. But
this assumption does not apply to calls made by the test harness. For example,
the following program test harness is allowed by Shrinker and correctly checks
whether copy_ints correctly handles overlapping source and destination regions
(i.e., memmove vs. memcpy semantics).
 1    // ... eq_arrays, copy_ints assumed to be defined here ...
 2    struct array { int *data; unsigned n_data; }
 3    void test(struct array A, struct array B) {
 4        __VERIFIER_assume(eq_arrays(A, B));
 5        __VERIFIER_assume(A.n_data >= 2);
 6

 7          // The aliasing here is allowed by SHRINKER
 8          copy_ints(A.data + 1, A.data, A.n_data - 1);
 9

10          for (unsigned i = 1; i < B.n_data; i++)
11              __VERIFIER_assert(A.data[i] == B.data[i - 1]);
12    }

A.11       Array Types
To simplify parsing, Shrinker rejects programs that declare array-typed values
in C. In general, arrays are second-class types in C (e.g., they automatically
34      Matthew Sotoudeh

decay to pointers in most contexts) and can usually be replaced with pointers.
For example, Shrinker would reject the following program, which declares the
variable string having an explicit array type:

 1   void test(unsigned n) {
 2       char string[n];
 3       // ... "string" is an array of "n" chars ...
 4   }

Recall from Section 5 that parameters to the test harness having a struct type
with a pointer field X and integer field n_X are interpreted by Shrinker as
arrays. So the above program can instead be rewritten to use pointers as below,
which accomplishes the original intention and will be accepted by Shrinker.

 1   struct string { char *string; unsigned n_string; }
 2   void test(struct string string) {
 3       // ... "string.string" points to "string.n_string" chars ...
 4   }


A.12    Reasoning About Array Equality

In order to effectively perform scapegoating size descent, Shrinker needs to be
able to track that certain arrays are identical between the primary and scapegoat
traces (e.g., that an array in the sacpegoat trace is equal to the corresponding
array in the primary with its first element removed). We do this by encoding
arrays as uninterpreted objects, which allows us to track equality constraints
through the application of other uninterpreted functions like store and select.
For example, we might have the following constraint, stating that some array is
identical between states 10 of the primary and scapegoat traces:

array_1_in_primary_state_10 = array_1_in_scapegoat_state_10

Then, suppose we apply HStep♯ and HStep♯∃ to add new constraints stepping
each trace forward once. If this involves writing a value V to index K of each
array, the constraints would look like:

array_1_in_primary_state_10 = array_1_in_scapegoat_state_10
array_1_in_primary_state_11
    = store(array_1_in_primary_state_10, K, V)
array_1_in_scapegoat_state_11
    = store(array_1_in_scapegoat_state_10, K, V)

Then our abstract domain implementation, which propagates uninterpreted func-
tion equalities, can conclude from this that the array is still equal in state 11 of
the primary and scapegoats.

array_1_in_primary_state_11 = array_1_in_scapegoat_state_11
        Automated Verification of Monotonic Data Structure Traversals in C        35

B    Extended Worked Example

We now work through a small example showing how Shrinker can use Algo-
rithm 2 to prove correctness of a simple heap-manipulating program. In the below
we will say an abstract herd a “represents herds . . . ” to mean the concretization
set γ H (a) consists of such herds. Recall our running example from Section 3:

 1   struct arr { int *data; int n_data; };
 2   void test(struct arr arr) {
 3       for (int i = 0; i < arr.n_data; i++)
 4           arr.data[i] = 0;
 5       for (int i = 0; i < arr.n_data; i++)
 6            if (arr.data[i] != 0)
 7                __VERIFIER_fail(); }

Recall this is an unusually simple example for the sake of exposition; our actual
benchmark instances are more complicated. Furthermore, the actual execution
of Shrinker works at a very low level (essentially tracking the values of dozens
of registers in addition to base and bound arrays for memory checking instru-
mentation after lowering this code), so we have tried for exposition reasons to
present the intermediate states in a relatively succinct way. In particular, in the
example below we assume the program transition is very coarse-grained (e.g.,
processes the entirety of line 4 in a single step).
     Furthermore, instead of showing the intermediate steps of the algorithm,
we only show the resulting proof, i.e., a set of abstract herds that are closed,
i.e., if t is a trace accounted for by one of the abstract herds in the set, and
t′ ∈ Step(t), then t′ is also accounted for by some abstract herd in the set. In
other words, these abstract herds can be thought of as the contents of the seen
set in Algorithm 2. The relation can be visualized in the following graph, where
each node is one of the abstract herds, and if t is accounted for by some node
in the graph and t′ ∈ Step(t), then t′ is accounted for by one of the successor
nodes in the graph.

                     a2            a4            a5


     a1 = I H♯       a3            a6            a7            a8            a9



    Some structure of the program is visible in this graph, e.g., a2 corresponds
to the program exiting quickly if arr.n_data = 0, while a4 and a5 correspond
to the program exiting after only one iteration of each loop if arr.n_data =
1. The remaining abstract herds capture only traces where arr.n_data > 1: a6
captures subsequent iterations of the first loop, a7 captures the first iteration of
the second loop, a8 captures subsequent iterations of the second loop, and a9 cap-
tures any iterations of the second loop that might reach the __VERIFIER_fail()
statement. Notably, the analysis knows easily that it is not possible for a7 (first
36     Matthew Sotoudeh

iteration of the second loop) to reach failure because it tracks the possible val-
ues of arr.data[0]; but it does not do the same for a9 (subsequent iterations
of the second loop) because that would require tracking the arbitrarily many
possible values in the rest of arr.data[1:n]. Because of this, the analyzer was
not able to rule out the possibility of a9 without the use of scapegoating size
descent, which tells it that blame can be transferred onto the scapegoat trace in
a9 , hence no error need be reported there.
     We now describe each of the abstract herds. Recall that an abstract herd can
be expressed via constraints, where the concretization set is all of the herds that
satisfy those constraints. In the below, we assume every state has a pc indicating
the line that is about to execute next. Lines 3 and 5 indicate checking the i
< arr.n_data condition. Some constraints need to relate the values between
different traces; for this we write h[1](foo) to mean “the value of foo in the last
state of trace h[1].” We also use arr.data[i:j] to mean “the subarray pointed
to by arr.data from index i (inclusive) to index j (exclusive).”

 – a1 = I H♯ : (initial state)
     • h[1] has length 1:
           ∗ First state: arr.n_data >= 0, i = 0, pc = 3.
   Successors: a2 (empty), a3 (nonempty).
 – a2 : (empty array)
     • h[1] has length 2:
           ∗ First state: arr.n_data = 0, i = 0, pc = 3.
           ∗ Second state: identical except pc = 5.
   Successors: none (constraints imply the primary trace reaches exit immedi-
   ately after this state).
 – a3 : (finished first iteration of first loop)
     • h[1] has length 2:
           ∗ First state: arr.n_data >= 1, i = 0, pc = 3.
           ∗ Second state: identical except arr.data[0] = 0, i = 1.
     • h[2] has length 1:
           ∗ First state: arr.n_data = h[1](arr.n_data − 1), pc = 3, i = 0, and
             arr.data[0 : arr.n_data] = h[1](arr.data[1 : arr.n_data]).
   Successors: a4 (finished), a6 (unfinished).
 – a4 : (array size exactly 1)
     • h[1] has length 3:
           ∗ First state: arr.n_data = 1, i = 0, pc = 3.
           ∗ Second state: identical except arr.data[0] = 0, i = 1.
           ∗ Third state: identical except i = 0, pc = 5.
     • (h[2] gets dropped)
   Successors: a5
 – a5 : (array size exactly 1)
     • h[1] has length 4:
           ∗ First state: arr.n_data = 1, i = 0, pc = 3.
           ∗ Second state: identical except arr.data[0] = 0, i = 1.
           ∗ Third state: identical except i = 0, pc = 5.
       Automated Verification of Monotonic Data Structure Traversals in C    37

          ∗ Fourth state: identical except i = 1, pc = 5.
   Successors: (none; the program immediately exits after this.)
 – a6 : (>1 iterations of the first loop)
     • h[1] has length ≥ 3:
          ∗ (Earlier states unconstrained)
          ∗ Final state: arr.n_data >= 2, arr.data[0] = 0, i >= 2, pc = 3.
     • h[2] has length ≥ 2:
          ∗ (Early states unconstrained)
          ∗ Last state: arr.n_data = h[1](arr.n_data−1), pc = 3, i = h[1](i−
             1), and arr.data[0 : arr.n_data] = h[1](arr.data[1 : arr.n_data]).
   Successors: a7 (finished), a6 (unfinished).
 – a7 : (start of second loop, after >1 iterations of the first loop)
     • h[1] has length ≥ 3:
          ∗ (Earlier states unconstrained)
          ∗ Final state: arr.n_data >= 2, arr.data[0] = 0, i = 0, pc = 5.
     • h[2] has length ≥ 2:
          ∗ (Early states unconstrained)
          ∗ Last state: arr.n_data = h[1](arr.n_data − 1), pc = 5, i = 0, and
             arr.data[0 : arr.n_data] = h[1](arr.data[1 : arr.n_data]).
   Successors: a8 (only step the primary forward; failure not possible in the
   primary because we know arr.data[0] = 0)
 – a8 : (>1 iterations of second loop, after >1 iterations of the first loop)
     • h[1] has length ≥ 3:
          ∗ (Earlier states unconstrained)
          ∗ Final state: arr.n_data >= 2, arr.data[0] = 0, i >= 1, pc = 5.
     • h[2] has length ≥ 2:
          ∗ (Early states unconstrained)
          ∗ Last state: arr.n_data = h[1](arr.n_data−1), pc = 5, i = h[1](i−
             1), and arr.data[0 : arr.n_data] = h[1](arr.data[1 : arr.n_data]).
   Successors: a8 (no failure, unfinished), a9 (failure), (the final branch with
   i=arr.n_data results in immediate program exit, not shown).
 – a9 : (failure after >1 iterations of second loop)
     • h[1] has length ≥ 3:
          ∗ (Earlier states unconstrained)
          ∗ Final state: arr.n_data >= 2, arr.data[0] = 0, i >= 1, pc = 7.
     • h[2] has length ≥ 2:
          ∗ (Early states unconstrained)
          ∗ Last state: arr.n_data = h[1](arr.n_data−1), pc = 7, i = h[1](i−
             1), and arr.data[0 : arr.n_data] = h[1](arr.data[1 : arr.n_data]).
   Note that both have reached failure, so CanBlame is true and we do not need
   to report a potential failure.
   Successors: (none; after failure the program halts)


C    Limitations and Future Work
We now discuss some major limitations of and future work for scapegoating size
descent in general and Shrinker in particular.
38      Matthew Sotoudeh

C.1    Performance on non-MDST Instances
Shrinker and scapegoating size descent are designed to take advantage of the
fact that many real-world MDSTs do very similar things when run on an ar-
bitrary input as when run on a shrunk version of that input. When analyzing
programs that do not have such a property, the technique essentially reduces
to traditional abstract interpretation (Algorithm 1), where the analysis power
is controlled directly by the precision of the abstract domain. Shrinker does
not use a particularly precise abstraction, so we do not expect or claim it to
work well on such non-MDST programs. Determining whether the key insight of
scapegoating size descent can be useful in non-MDST settings is an interesting
area of future work.

C.2    Nested Loops
This paper only considered ‘singly nested’ MDSTs, excluding, e.g., lists-of-strings
that might also be traversed in a monotonic way, and we make no claims about
the performance of Shrinker on nested structures. To support such nested MD-
STs we would need to extend our heuristics for stepping and adding scapegoats
to handle such cases. Alternatively, we could try verifying them in a composi-
tional way, i.e., analyze just the inner structure first to determine lemmas about
its behavior that allow us to then analyze the outer structure independently.
These are interesting areas of future work but beyond the scope of this paper.

C.3    Skip Traversals
We have focused on MDSTs that iterate forward by a single element on each iter-
ation, but one could imagine MDSTs that move forward by a different constant
(or even variable) number of elements each iteration. For example, searching in
an array of integers where every pair of two adjacent integers are considered a
single key–value pair. To profitably apply Shrinker to such programs, we would
need to modify its implementation of MaybeAddScapegoats to drop more than
one entry when creating the scapegoat trace; in the earlier example, dropping
the first two entries (i.e., the first logical key–value pair) would suffice.

C.4    More Precise Memory Model
To simplify analyses, Shrinker currently rejects (reports unknown on) any pro-
gram that tries to reinterpret, say, a pointer to a struct as a pointer to a different
kind of struct or manipulate its byte value. This disallows generic operations like
memcpy that interpret arrays as byte pointers, and intrusive generic data struc-
tures where a pointer to a struct’s field is subtracted from to get a pointer to
the struct itself. This is not a fundamental limitation of scapegoating size de-
scent, and we believe that our memory abstraction can be extended to support
many such common operations. The simplest way to add some support for such
byte-level operations is to detect them and reinterpret them in terms of our
        Automated Verification of Monotonic Data Structure Traversals in C     39

higher level representation, e.g., we can detect when a constant number of bytes
is subtracted from a pointer and then interpret that as making it point to the
corresponding container element. With more engineering effort, a more complete
solution would involve modifying Shrinker to use a byte-level abstraction of the
heap, where every node in the heap is subdivided into individual bytes that can
be pointed to, read from, and written to individually. We believe that this would
not be too difficult to implement within Shrinker, although tracking relations
between individual bytes might slow down the numerical domain reasoning.


C.5   Performance on Tree Instances

In our evaluation we saw that tree instances were particularly slow for Shrinker
to verify. This is because Shrinker relies heavily on path splitting to keep the
trace herd abstractions precise, and tree traversals have an exponential blowup in
the number of possible paths because at each node you can go either left or right.
There is nothing in the theory of scapegoating size descent that requires such
aggressive path splitting; hypothetically, HWiden could even be implemented to
join the abstract trace herd with all previously seen abstract trace herds, at the
cost of precision.
    However, path splitting is required for the current version of Shrinker, with
its current heap abstraction and heuristics, to solve most the tree benchmarks.
This is because Shrinker needs relatively precise information about the tree
and the primary trace’s path in order to pick what scapegoats to add and prove
that they can be blamed (i.e., that they do “essentially the same thing” as the
primary). For example, consider verifying a BST search routine, and suppose we
know that the primary trace went down the rightmost branch of the tree:

                                B

                         A            D

                                C            F

                                      E             G
                                                     ..
                                                          .


With this information, Shrinker can determine that the scapegoat trace re-
sulting from an input tree formed by dropping the right child of the root (and
replacing it with its right child) results in similar enough behavior to complete
the scapegoating size descent-based verification. This is because it will take the
same traversal, just skipping over the iteration that would have touched the right
child of the root:
40      Matthew Sotoudeh

                                    B

                             A             F

                                    E             G
                                                   ..
                                                        .

Crucially, however, for herds where the primary trace takes a different path
through the tree, different scapegoats might be nedeed. If the primary instead
took the path B, D, C, . . . , we would instead have to replace D with its left
child C, not its right child F. For this reason, Shrinker relies on aggressive
path splitting so that for every abstract trace herd it processes, it knows enough
about the primary trace’s path to add the proper scapegoat and prove that its
trace is similar enough to guarantee it can accept blame if the primary fails.
    In theory, and with more engineering effort, a more precise abstract herd
domain might be developed that could obviate the need to do such aggressive
path splitting by representing parameterized constraints, e.g., that the scapegoat
trace is the result of dropping some node on the primary trace’s traversal path,
but keep which node exactly that is symbolic. Unfortunately, we believe such
an abstract domain would be significantly more complicated to implement, and
would work against the main benefit of scapegoating size descent, i.e., its ability
to use simpler abstract domains to represent the heap.

C.6    More Precise Numerical Domains
We used a custom integer difference logic (IDL) solver for the core of our nu-
merical abstraction (Section 5.3). We did this to keep the tool self-contained,
easy-to-build, and have a small trusted computing base (TCB). But there are
already implementations of many abstract domains, including octagons (similar
to IDL), in production quality libraries like APRON [Jeannet and Miné(2009)].
We could modify Shrinker to use a library like APRON, which would proba-
bly improve performance and let us opt-in to more precise abstract domains as
desired, at the cost of our TCB size and perhaps the ease-of-use issue of adding
dependencies.

C.7    Connections to the Small Scope Hypothesis
The original motivation of this work was to better understand the small scope
hypothesis. The observation is that many programs feel, intuitively, like they are
either correct, or they fail on some small input. It strains credibility that a tiny,
5-line linked list search-and-delete routine could be correct for all inputs up to
size 1007, but fail on an input of size 1008. But our understanding of program
verification says very little about why this feeling should be justified.
    The scapegoating size descent analysis technique sheds some light on this
mystery, because it works by proving that failure-inducing inputs are small.
        Automated Verification of Monotonic Data Structure Traversals in C         41

Essentially, it leads to an explanation of the small scope hypothesis for programs
that do ‘essentially the same thing’ on a smaller version of the input. Ultimately,
we would like to adapt the results in this paper into a syntactic result of the
form: any program in this syntactic class satisfies the small scope hypothesis,
i.e., is correct on all inputs if and only if it is correct on all inputs of a certain
size.
