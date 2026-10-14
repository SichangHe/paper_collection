Logical Methods in Computer Science
Volume 18, Issue 3, 2022, pp. 26:1–26:28                                                       Submitted        Sep. 02, 2021
https://lmcs.episciences.org/                                                                  Published        Aug. 31, 2022




 COUNTEREXAMPLE-GUIDED PROPHECY FOR MODEL CHECKING
           MODULO THE THEORY OF ARRAYS ∗

                               a
            MAKAI MANN             , AHMED IRFAN a , ALBERTO GRIGGIO                 b
                                                                                         , ODED PADON c ,
                                         AND CLARK BARRETT a

   a
        Stanford University, Stanford, USA
        e-mail address: {makaim,irfan,barrett}@cs.stanford.edu
    b
        Fondazione Bruno Kessler, Trento, Italy
        e-mail address: griggio@fbk.eu
    c
        VMware Research, Palo Alto, USA
        e-mail address: oded.padon@gmail.com


           Abstract. We develop a framework for model checking infinite-state systems by auto-
           matically augmenting them with auxiliary variables, enabling quantifier-free induction
           proofs for systems that would otherwise require quantified invariants. We combine this
           mechanism with a counterexample-guided abstraction refinement scheme for the theory of
           arrays. Our framework can thus, in many cases, reduce inductive reasoning with quantifiers
           and arrays to quantifier-free and array-free reasoning. We evaluate the approach on a wide
           set of benchmarks from the literature. The results show that our implementation often
           outperforms state-of-the-art tools, demonstrating its practical potential.




                                                 1. Introduction
Model checking is a widely-used and highly-effective technique for automated property
checking. While model checking finite-state systems is a well-established technique for
hardware and software systems, model checking infinite-state systems is more challenging.
One challenge, for example, is that proving properties by induction over infinite-state systems
often requires the use of universally quantified invariants. While some automated reasoning
tools can reason about quantified formulas, such reasoning is typically not very robust.
Furthermore, just discovering these quantified invariants remains very challenging.
     Previous work (e.g., [McM18]) has shown that prophecy variables can sometimes play
the same role as universally quantified variables, making it possible to transform a system
that would require quantified reasoning into one that does not. However, to the best of
our knowledge, there has been no automatic method for applying such transformations. In
this paper, we introduce a technique we call counterexample-guided prophecy. During the
refinement step of an abstraction-refinement loop, our technique automatically introduces

   Key words and phrases: Model Checking, Prophecy Variables, Quantified Invariant, Satisfiability Modulo
Theories, Theory of Arrays.
 ∗
   This is an extended version of work presented in [MIG+ 21].



l       LOGICAL METHODS
        IN COMPUTER SCIENCE           DOI:10.46298/LMCS-18(3:26)2022
                                                                       ©
                                                                       CC
                                                                            M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett
                                                                             Creative Commons
26:2               M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett             Vol. 18:3




prophecy variables, which both help with the refinement step and may also reduce the
need for quantified reasoning. We demonstrate the technique in the context of model
checking for infinite-state systems with arrays, a domain which is known for requiring
quantified reasoning. We show how a standard abstraction for arrays can be augmented with
counterexample-guided prophecy to obtain an algorithm that reduces the model checking
problem to quantifier-free, array-free reasoning. The paper makes the following contributions:
   i) we introduce an algorithm called Prophecize that uses history and prophecy variables
      to target a specific term at a specific time step of an execution, producing a new
      transition system that can effectively reason universally about that term;
  ii) we develop an automatic abstraction-refinement procedure for arrays, which leverages
      the Prophecize algorithm during the refinement step, and show that it is sound and
      produces no false positives;
 iii) we develop a prototype implementation of our technique; and
 iv) we evaluate our technique on four sets of model checking benchmarks containing arrays
      and show that our implementation outperforms state-of-the-art tools on a majority of
      the benchmark sets.
     The rest of the paper is organized as follows. We start by providing relevant background
information in Section 2. We then motivate the use of prophecy variables with an example and
introduce the Prophecize algorithm in Section 3. We describe our abstraction-refinement
framework for arrays in Section 4 and discuss its expressiveness and limitations in Section 5.
In Section 6, we describe our prototype along with some implementation details. We evaluate
our approach empirically in Section 7, cover related work in Section 8, and finally conclude
in Section 9.
     This paper is an extended version of work presented in [MIG+ 21]. Notable changes
include the proofs, a self-comparison with different options in Section 7, and Section 6, which
discusses implementation details of the prototype.


                                       2. Background
We assume the standard many-sorted first-order logical setting with the usual notions of
signature, term, formula, and interpretation. A theory is a pair T = (Σ, I) where Σ is a
signature and I is a class of Σ-interpretations, the models of T . A Σ-formula ϕ is satisfiable
(resp., unsatisfiable) in T if it is satisfied by some (resp., no) interpretation in I. Given
an interpretation M, a variable assignment s over a set of variables X is a mapping that
assigns each variable x ∈ X of sort σ to an element of σ M , denoted xs . We write M[s] for
the interpretation that is equivalent to M except that each variable x ∈ X is mapped to
xs . Let x be a variable, t a term, and φ a formula. We denote with φ{x 7→ t} the formula
obtained by replacing every free occurrence of x in φ with t. We extend this notation to
sets of variables and terms in the usual way. If f and g are two functions, we write f ◦ g to
mean functional composition, i.e., f ◦ g(x) = f (g(x)). We use ] to refer to set union.
     Let TA be the standard theory of arrays [Mcc62] with extensionality, extended with
constant arrays. Concretely, we assume sorts for arrays, indices, and elements, and function
symbols read , write, and constarr . Here and below, we use a and b to refer to arrays, i and
j to refer to array indices, and e and c to refer to array elements, where c is also restricted
to be an interpreted constant. The theory contains the class of all interpretations satisfying
the following axioms:
Vol. 18:3                     COUNTEREXAMPLE-GUIDED PROPHECY                                  26:3




                   ∀ a, i, j, e. i = j =⇒ read (write(a, j , e), i ) = e ∧
                                                                                          (write)
                              i 6= j =⇒ read (write(a, j , e), i ) = read (a, i )
                        ∀ a, b. (∀ i. read (a, i ) = read (b, i )) =⇒ a = b                (ext)
                                   ∀ i. read (constarr (c), i ) = c                      (const)

2.1. Symbolic Transition Systems and Model Checking. For generality, assume a
background theory T with signature Σ. We will assume that all terms and formulas are
Σ-terms and Σ-formulas, that entailment is entailment modulo T , and interpretations are
T -interpretations. A symbolic transition system (STS) S is a tuple S := hX, I, T i, where X
is a finite set of state variables, I(X) is a formula denoting the initial states of the system,
and T (X, X 0 ) is a formula expressing a transition relation. Here, X 0 is the set obtained by
replacing each variable x ∈ X with a new variable x0 of the same sort. Let prime(x) = x0
be the bijection corresponding to this replacement. We say that a variable x is frozen if
T |= x0 = x. When the state variables are obvious, we will often drop X.
     A state s of S is a variable assignment over X. An execution of S of length k is a
pair hM, πi, where M is an interpretation and π := s0 , s1 , . . . , sk−1 is a path of length k, a
sequence of states such that M[s0 ] |= I(X) and M[si ][si+1 ◦ prime −1 ] |= T (X, X 0 ) for all
0 ≤ i < k − 1. When reasoning about paths, it is often convenient to have multiple copies of
the state variables X. We use X@n to denote the set of variables obtained by replacing each
variable x ∈ X with a new variable called x@n of the same sort. We refer to these as timed
variables. A state s is reachable in S if it appears in a path of some execution of S. We
say that a formula P (X) is an invariant of S, denoted by S |= P (X), if P (X) is satisfied
in every reachable state of S (i.e., for every execution hM, πi, M[s] |= P (X) for each s
in π). The invariant checking problem is, given S and P (X), to determine if S |= P (X).
A counterexample is an execution hM, πi of S of length k such that M[sk−1 ] 6|= P (X). If
I(X) |= φ(X) and φ(X) ∧ T (X, X 0 ) |= φ(X 0 ), then φ(X) is an inductive invariant. Every
inductive invariant is an invariant (by induction over path length). In this paper we focus
on model checking problems where I, T and P are quantifier-free. However, a quantified
inductive invariant might still be necessary to prove a property of the system.
     Bounded Model Checking (BMC) is a bug-finding technique which attempts to find a
counterexample for a property, P (X), of length k for some finite k [BCCZ99]. A single
BMC query at bound k for an invariant property uses a constraint solver to check the
satisfiability of the following formula: BM C(S, P, k) := I(X@0) ∧ ( k−2
                                                                            V
                                                                              i=0 T (X@i, X@(i +
1))) ∧ ¬P (X@(k − 1)). If the query is satisfiable, there is a bug.

2.2. Counterexample-Guided Abstraction Refinement (CEGAR). CEGAR is a
general technique in which a difficult conjecture is tackled iteratively [Cla03]. Algorithm 1
shows a simple CEGAR loop for checking an invariant P for an STS S. It is parameterized
by three functions. The Abstract function produces an initial abstraction of the problem.
It must satisfy the contract that if hS, b Pbi = Abstract(S, P ), then Sb |= Pb =⇒ S |= P .
The next function is the Prove function. This can be any (unbounded) model-checking
algorithm that can return counterexamples. It checks whether a given property P is an
invariant of a given STS S. If it is, it returns with proven set to true. Otherwise, it returns
a bound k at which a counterexample exists. The final function is Refine. It takes the
abstracted STS and property together with a bound k at which a known counterexample
26:4                M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                Vol. 18:3




Algorithm 1 STS-CEGAR(S := hX, I, T i, P )
 1: hhX, b Tbi, Pbi ← Abstract(S, P )
      b I,
 2: while true do
 3:   hk, proveni ← Prove(hX,       b Tbi, Pb)
                                  b I,                                            // try to prove
 4:   if proven then return true                                             // property proved
 5:   hhX,  b Tbi, Pb, refined i ← Refine(hX,
         b I,                                    b Tbi, Pb, k)
                                               b I,                              // try to refine
 6:   if ¬refined then return false                                     // found counterexample
 7: end while


for the abstract STS exists. Its job is to refine the abstraction until there is no longer a
counterexample of size k. If it succeeds, it returns the new STS and property. It fails if
there is an actual counterexample of size k for the concrete system. In this case, it sets the
return value refined to false.

2.3. Auxiliary variables. We finish this section with relevant background on auxiliary
variables, a crucial part of the refinement step described in Section 4. Auxiliary variables
are new variables added to the system which do not influence its behavior (i.e., a state is
reachable in the old system iff it is a reduct [Hod93] to the old set of variables of a reachable
state in the new system). There are two main categories of auxiliary variables we consider:
history and prophecy. History variables, also known as ghost state, preserve a value, making
its past value available in future states [OG76]. Prophecy variables are the dual of history
variables and provide a way to refer to a value that occurs in a future state. Abadi and
Lamport formally characterized soundness conditions for the introduction of history and
prophecy variables [AL88]. Here, we consider a simple, structured form of history variables.
Definition 2.1. Let S = hX, I, T i be an STS, t a term whose free variables are in X, and
n > 0, then Delay(S, t, n) returns a tuple hhX h , I h , T h i, htn i, containing a new STS and
                                                                                  0              0
history variable, where X h = X ] {ht1 , . . . , htn }, I h = I, and T h = T ∧ ht1 = t ∧ ni=2 hti =
                                                                                        V

hti−1 .
    The Delay operator makes the current value of a term t available for the next n states in
a path. This is accomplished by adding n new history variables and creating an assignment
chain that passes the value to the next history variable at each state. Thus, htk contains the
value that t had k states ago. The initial value of each history variable is unconstrained.
Theorem 2.2 [AL88]. Let S = hX, I, T i be an STS, P a property, and Delay(S, v, n) =
hS h , hvn i. Then S |= P iff S h |= P .
We refer to [AL88] for a general proof that subsumes Theorem 2.2. In contrast to the general
approach for history variables, we use a version of prophecy that only requires a single frozen
variable. The motivation for this is that a frozen variable can be used in place of a universal
quantifier, as the following theorem adapted from [McM18] shows.
Theorem 2.3 [McM18]. Let S = hX, I, T i be an STS, y a variable in formula P (X ∪ {y}),
and v a fresh variable (i.e., not in X ∪ {y} or X 0 ). Let S p = hX ∪ {v}, I, T ∧ v 0 = vi. Then
S |= ∀ y. P (X ∪ {y}) iff S p |= P (X ∪ {y}){y 7→ v}.
Proof Sketch. We prove the equivalent statement S 6|= ∀ y. P (X ∪ {y}) ↔ S p 6|= P (X ∪
{y}){y 7→ v}.
Vol. 18:3                     COUNTEREXAMPLE-GUIDED PROPHECY                                 26:5




→: Suppose there is a counterexample trace demonstrating that S 6|= ∀ y. P (X ∪ {y}). In
the last step of the trace, the property is violated. There is a specific value of y for which
P (X ∪ {y}) does not hold. We can reconstruct the same counterexample trace for S p and
P (X ∪ {y}){y 7→ v} by assigning v this same value in every step of the trace.
←: If there is a counterexample trace for S p 6|= P (X ∪ {y}){y 7→ v}, we can construct
a counterexample for S and ∀ y. P (X ∪ {y}) by using the same trace but dropping the
assignment to the frozen variable, v. Finally, the value of y that violates the property in the
last step of the trace will be the same value v was assigned.                                

Theorem 2.3 shows that a universally quantified variable in a property can be replaced with
a fresh symbol in a process similar to Skolemization. The intuition is as follows. The frozen
variable has the same value in all states, but it is uninitialized by I. Thus, for each path in
S, there is a corresponding path (i.e., identical except at v) in S p for every possible value
of v. This proliferation of paths plays the same role as the quantified variable in P . We
mention here one more theorem from [McM18]. This one allows us to introduce a universal
quantifier.
Theorem 2.4 [McM18]. Let S = hX, I, T i be an STS, P (X) a formula, and t a term. Then,
S |= P (X) iff S |= ∀ y.(y = t =⇒ P (X)), where y is not free in P (X).
Proof Sketch. P (X) and ∀ y.(y = t =⇒ P (X)) for y 6∈ X are equivalent in first order logic.
Intuitively, when y = t, it simplifies to P (X) and all other values of y render the formula
trivially true.                                                                           

Theorems 2.3 and 2.4 are special cases of Theorems 3 and 4 of [McM18], which handle
temporal logic [Pnu77] formulas. Another notable difference is that Theorem 3 of [McM18]
uses a fresh background symbol to replace the universally quantified variable. Note that it
does not change as the system evolves because it is not a state variable of the transition
system. Rather than allowing background symbols, we simulate this with a frozen variable
that maintains its value in Theorem 2.3.


                 3. Using Auxiliary Variables to Assist Induction
We can use Theorem 2.4 followed by Theorem 2.3 to introduce frozen prophecy variables
that predict the value of a term t when the property P is being checked. We refer to t as
the prophecy target and the process as universal prophecy. If we also use Delay, we can
target a term at some finite number of steps before the property is checked. This is captured
by Algorithm 2, which takes a transition system, property P (X), term t, and n ≥ 0. If
n = 0, it introduces a universal prophecy variable for t. Otherwise, it first introduces history
variables for t and then applies universal prophecy to the delayed t. In either case it returns
the augmented system, augmented property, and the prophecy variable.
      We will use the STS shown in Fig. 1(a) as a running example throughout the paper
(it is inspired by the hardware example from [Bje08]). We assume the background theory
T includes integer arithmetic and arrays of integers indexed by integers. The variables in
this STS include an array and four integer variables, representing the read index (ir ), write
index (iw ), read data (dr ), and write data (dw ), respectively. The system starts with an
array of all zeros. At every step, if the write data is less than 200, it writes that data to the
array at the write index. Otherwise, the array stays the same. Additionally, the read data
26:6                M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                        Vol. 18:3




Algorithm 2 Prophecize(hX, I, T i, P (X), t, n)
 1: if n = 0 then
 2:    return hhX ] {pt }, I, T ∧ p0t = pt i, pt = t =⇒ P (X), pt i
 3: else
 4:    hhX h , I h , T h i, htn i := Delay(hX, I, T i, t, n)
                                             0
 5:    return hhX h ] {pnt }, I, T ∧ pnt = pnt i, pt = htn =⇒ P (X), pnt i
 6: end if


         I := a = constarr (0 ) ∧ dr < 200             I := a = constarr (0 ) ∧ dr < 200
         T := a0 = ite(dw < 200,                       T := a0 = ite(dw < 200,
                         write(a, iw , dw ), a)∧                        write(a, iw , dw ), a)∧
                                                                                 0             0
              dr0 = read (a, ir )                       dr0 =read (a, ir ) ∧ p1ir = p1ir ∧ hi1r = ir
        P := dr < 200                                  P := p1ir = hi1r =⇒ dr < 200
                         (a)                                               (b)

        Figure 1. (a) Running example. (b) Running example with prophecy variable.


is updated with the current value of a at ir . This effectively introduces a one-step delay
between when the value is read from a and when the value is present in dr . The property
is that dr < 200. This property is clearly true, but it is not straightforward to prove with
standard model checking techniques because it is not inductive. Note that it is also not
k-inductive for any k [SSS00]. The primary issue is that the property does not constrain the
value of a at all, so in an inductive proof, the value of a could be anything in the induction
hypothesis.
      One way to prove the property is to strengthen it with the quantified invariant:
∀ i. read (a, i ) < 200. Remarkably, observe that by augmenting the system using Prophe-
cize, it is possible to prove the property using only a quantifier-free invariant. In this
case, the relevant prophecy target is the value of ir one step before checking the property.
We run Prophecize(hX, I, T i, P, ir , 1) and it returns the system and property shown in
Fig. 1(b), along with the prophecy variable p1ir . This augmented system has a simple,
quantifier-free invariant which can be used to strengthen the property, making it inductive:
read (a, pir ) < 200. This formula holds in the initial state because of the constant array, and
if we start in a state where it holds, it still holds after a transition.
      Notice that the invariant learned over the prophecy variable has the same form as the
original quantified invariant. However, we have instantiated that universal quantifier with
a fresh, frozen prophecy variable. Intuitively, the prophecy variable captures a proof by
contradiction: assume the property does not hold, consider the value of ir one step before the
first failure of the property, and then use this value to show the property holds. This example
shows that auxiliary variables can be used to transform an STS without a quantifier-free
inductive invariant into an STS with one. However, it is not yet clear how to identify good
targets for history and prophecy variables. In the next section, we show how this can be
done as part of an abstraction refinement scheme for symbolic transition systems over the
theory of arrays.
Vol. 18:3                    COUNTEREXAMPLE-GUIDED PROPHECY                               26:7




                         Ib := b     \ ∧ dr < 200
                               a = constarr0
                               a0 = ite(dw < 200, write(b
                         Tb := b                  [ a, iw , dw ), b
                                                                  a)∧
                                                          0
                              dr0 = read
                                     d (ba, ir ) ∧ constarr0
                                                     \       = constarr0
                                                                 \
                         Pb := dr < 200

             Figure 2. Result of calling Abstract on the example from Fig. 1(a)


                       4. Abstraction Refinement for Arrays
We now introduce our main contribution. Given a background theory TB and a model
checking algorithm for STSs over TB , we use an instantiation of the CEGAR loop in
Algorithm 1 to check properties of STSs over the theory that combines TB and the theory of
arrays, TA . The key idea is to abstract all array operators and then add array lemmas as
needed during refinement.

4.1. Abstract and Prove. We use a standard abstraction for the theory of arrays, which
we denote Abstract-Arrays. Every array sort is replaced with an uninterpreted sort, and
the array variables are abstracted accordingly. Each constant array is replaced by a fresh
abstract array variable, which is then constrained to be frozen (because constant arrays
do not change over time). Additionally, we replace the read and write array operations
with uninterpreted functions. Note that if the system contains multiple array sorts, we
need to introduce separate read and write functions for each uninterpreted abstract array
sort. Using uninterpreted sorts and functions for abstracting arrays is a common technique
in Satisfiability Modulo Theories [BT18] (SMT) solvers [GKF08]. Intuitively, our initial
abstraction starts with memoryless arrays, i.e., the array axioms are not initially enforced
on the abstraction. We then incrementally refine the arrays’ memory as needed by adding
prophecy variables to be used in array axioms. Intuitively, a prophecy variable keeps track
of an index of the array that will faithfully store values. Fig. 2 shows the result of running
Abstract-Arrays on the example from Fig. 1(a). Prove can be instantiated with any
(unbounded) model checker that can accept expressions over the background theory TB
combined with the theory of uninterpreted functions. In particular, due to our abstraction,
the model checker does not need to support the theory of arrays.

4.2. Refine. Here, we explain the refinement approach for our array abstraction. At a high
level, the algorithm solves a BMC problem over the abstract STS at bound k. It identifies
violations of array axioms in the returned abstract counterexample, and instantiates each
violated axiom (this is essentially the same as the lazy array axiom instantiation approach
used in SMT solvers [BMS06, BB08, CH15, dB09]). We then lift these axioms to the STS-
level by modifying the STS. It is this step that may require introducing auxiliary variables.
The details are shown in Algorithm 3.
     Line 1 computes an index set I of index terms with ComputeIndices — this set is used
in the lazy axiom instantiation step below. The procedure adds to I every term that appears
as an index in a read
                  d or write
                          [ operation (recall that these appear as uninterpreted functions
in the abstracted STS and property) in BM C(S,    b Pb, k). Furthermore, it adds a witness
index for every array equality — the witness corresponds to a Skolemized existential variable
26:8                   M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                           Vol. 18:3




Algorithm 3 Refine-Arrays (Sb := hX, b Tbi, Pb, k)
                                  b I,

 1: I ← ComputeIndices(S,           b Pb, k)
 2: loop
 3:   ρ ← BMC(S,       b Pb, k)
 4:   if ρ = ⊥ then return hhX,                b I,b Tbi, Pb, truei            // Property holds up to bound k
 5:   hca, ncai ← CheckArrayAxioms(ρ, I)
 6:   if ca = ∅ ∧ nca = ∅ then return hhX,                   b I,b Tbi, Pb, f alsei        // True counterexample
 7:   // Go through non-consecutive array axiom instantiations
 8:   for hax, i@ni i ∈ nca do
 9:      let nmin := min(τ (ax)\{ni })
10:      hhX p , I p , T p i, P p , pk−n
                                     i
                                            i
                                              i ← Prophecize(hX,       b I,b Tbi, Pb, i, k − ni )
                                        k−ni
11:      axc ← ax{i@ni 7→ pi                    @nmin }
12:      ca ← ca ] {axc @nmin }                                             // add consecutive version of axiom
13:      I ← I ] {pk−n    i
                               i
                                 @0,   . . . , p k−ni
                                                 i    @k}
14:      Xb ← X p ; Ib ← I p ; Tb ← T p ; Pb ← P p
15:   end for
16:   // Go through consecutive array axiom instantiations
17:   for ax ∈ ca do
18:      let nmin := min(τ (ax)), nmax := max (τ (ax))
19:      assert(nmax = nmin ∨ nmax = nmin + 1)
20:      if k = 0 then
21:         Ib ← Ib ∧ ax{X@nmin 7→ X}
22:      else if nmin = nmax then
23:         Tb ← Tb ∧ ax{X@nmin 7→ X} ∧ ax{X@nmin 7→ X 0 }
24:      else
25:         Tb ← Tb ∧ ax{X@nmin 7→ X}{X@(nmin + 1) 7→ X 0 }
26:      end if
27:   end for
28: end loop


in the contrapositive of axiom (ext). For soundness, it must also add an extra variable λσ
for each index sort σ and constrain it to be different from all the other index variables of the
same sort (this is based on the approach in [BMS06]). Intuitively, this variable represents
an arbitrary index different from those mentioned in the STS. We assume that the index
sorts are from an infinite domain so that a distinct element is guaranteed. For simplicity of
presentation, we also assume from now on that there is only a single index sort (e.g., integers).
Otherwise, I must be partitioned by sort. For the abstract STS in Fig. 2, with k = 1, the
index set would be I := {ir @0, iw @0, w0 @0, w1 @0, λInt @0, ir @1, iw @1, w0 @1, w1 @1, λInt @1},
where w0 and w1 are witness indices.
     After computing indices, the algorithm enters the main loop. Line 3 dispatches a
bounded model checking query, BM C(S,    b Pb, k). The result ρ is either a counterexample, or
the distinguished value ⊥, indicating that the query is unsatisfiable. If it is the latter, then
it returns the refined STS and property, as the property now holds on the STS up to bound
k. Otherwise, the algorithm continues. The next step (line 5) is to find violations of array
axioms in the execution ρ based on the index set I.
Vol. 18:3                       COUNTEREXAMPLE-GUIDED PROPHECY                                   26:9




     CheckArrayAxioms takes two arguments, a counterexample and an index set, and
returns instantiated array axioms that do not hold over the counterexample. This works as
follows. It first looks for occurrences of write
                                           [ in the BMC formula. For each such occurrence,
it instantiates the (write) axiom so that the write   [ term in the axiom matches the term
in the formula (i.e., we use the write term as a trigger). This instantiates all quantified
                                     [
variables except for i. Next it instantiates i once for each variable in the index set. Each
of the instantiated axioms are evaluated using the values from the counterexample and all
instantiations that reduce to false are saved. The procedure does the same thing for the
(const) axiom, using each constant array term in the BMC formula as a trigger. Finally,
for each array equality a@m = b@n in the BMC formula, it checks an instantiation of the
contrapositive of (ext): a@m =    6 b@n → read (a@m, wi @n) 6= read (b@n, wi @n). The saved
instantiated formulas that do not hold in ρ are added to the set of violated axioms.
     CheckArrayAxioms sorts the collected, violated axiom instantiations into two sets based
on which timed variables they contain. The consecutive set contains formulas with timed
variables whose timing differs by at most one; whereas the timed variables in the formulas
contained in the non-consecutive set may differ by more. Formally, let τ be a function
which takes a single timed variable and returns its time (e.g., τ (i@2) = 2). We lift this to
formulas by having τ (φ) return the set of all time-steps for variables in φ. A formula φ is
consecutive iff max (τ (φ)) − min(τ (φ)) ≤ 1. Note that instantiations of (ext) are consecutive
by construction. Additionally, because constant arrays have the same value in all time steps,
the algorithm can always choose a representative time-step for instantiations of (const) that
results in a consecutive formula. However, instantiations of (write) may be non-consecutive,
because the variable from the index set may be from a time-step that is different from
that of the trigger term. CheckArrayAxioms returns the pair hca, ncai, where ca is a set
of consecutive axiom instantiations and nca is a set of pairs — each of which contains a
non-consecutive axiom instantiation and the index-set term that was used to create that
instantiation. We assume that the index-set term used in a non-consecutive axiom is not
an auxiliary variable. Since auxiliary variables only record or predict the value of another
index, it does not make sense to target one of these for prophecy.
     Line 6 checks if the returned sets are empty. If so, then there are no array axiom
violations and ρ is a concrete counterexample. In this case, the system, property, and false
are returned. Otherwise, the non-consecutive formulas are processed in lines 8–15. Given a
non-consecutive formula ax together with its index-set variable i@ni , line 9 computes the
minimum time-step of the axiom’s other variables, nmin . Then line 10 calls the Prophecize
method to create a prophecy variable pk−n   i
                                                 i
                                                   , that is effectively a way to refer to i@ni at
time-step nmin (line 10). This allows the algorithm to create a consecutive formula axc that
is semantically equivalent to ax (line 11). This new consecutive formula is added to ca in
line 12, and in line 13 the introduced prophecy variables (one for each time-step) are added
to the index set. Then, line 14 updates the abstraction.
     At line 17, the algorithm is left with a set of consecutive formulas to process. For
each consecutive formula ax, line 18 computes the minimum and maximum time-step of its
variables, which must differ by no more than 1 (line 19). There are three cases to consider:
i) when k = 0, the counterexample consists of only the initial state — then the initial state
is refined by adding the untimed version of ax to Ib (line 21); ii) if ax contains only variables
from a single time step, then the untimed version of ax is added as a constraint for both X
and X 0 , ensuring that it will hold in every state (line 23); iii) finally, if ax contains variables
26:10               M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                 Vol. 18:3




from two adjacent time steps, it can be translated directly into a transition formula to be
added to Tb (line 25). The loop then repeats with the newly refined STS.

Example. Consider again the example from Fig. 2, and suppose Refine-Arrays is called
on Sb and Pb with k = 3. At this unrolling, one possible abstract counterexample violates the
following nonconsecutive axiom instantiation:
           (ir @2 = iw @0 =⇒ read
                              d (write(
                                  [ a@0,d iw @0, dw @0), ir @2) = dw @0) ∧

           (ir @2 6= iw @0 =⇒ read
                               d (write(
                                   [ a@0,d iw @0, dw @0), ir @2) = read
                                                                    d (a@0,
                                                                        d ir @2))

To make this nonconsecutive axiom consecutive, it introduces a prophecy variable. The
target will be the instantiated index, ir @2. The relevant value to predict is one step before
a possible property violation (i.e., the end of a finite path), because k = 3, and τ (ir @2) = 2,
thus k − τ (ir @2) = 1. This corresponds to the k − ni at line 10 of Algorithm 3. Calling
Prophecize(S,  b Pb, ir , 1) returns the new STS hhX                  b Tb ∧ h 1 0 = ir ∧ p10 = p1 i
                                                     b ] {h 1 , p1 }, I,
                                                            ir   ir           ir           ir    ir
and the new property p1ir = hi1r =⇒ dr < 200. The history variable hi1r makes the previous
value of ir available at each time-step, and the prophecy variable p1ir predicts the value of ir
one step before a possible property violation. The axiom will be updated by replacing ir @2
with the prophecy variable which has the same value. Since the prophecy variable is frozen,
it is the same at every step. Thus, it can choose the prophecy variable at a time-step that
makes the axiom consecutive. In this case, the algorithm substitutes p1ir @0 for ir @2. This
results in the following consecutive axiom:
          (p1ir @0 = iw @0 =⇒ read
                               d (write(
                                   [ a@0,d iw @0, dw @0), p1 @0) = dw @0) ∧
                                                           ir

          (p1ir @0 6= iw @0 =⇒ read
                                d (write(
                                    [ a@0,d iw @0, dw @0), p1 @0) = read
                                                            ir
                                                                         d p1 @0))
                                                                     d (a@0,
                                                                             ir

     The untimed version (and a primed version) of this consecutive axiom would be added
to the transition relation at line 23 of Algorithm 3.
     We stress that processing nonconsecutive axioms using Prophecize is how Algorithm 3
automatically discovers the universal prophecy variable p1ir , and it is exactly the universal
prophecy variable that was needed in Section 3 to prove correctness of the running example.
An alternative approach could avoid nonconsecutive axioms using Craig interpolants [Cra57]
so that only consecutive axioms are found [BCS20]. However, quantifier-free interpolants
are not guaranteed to exist for the standard theory of arrays [KMZ06, BGR12], and the
auxiliary variables found using nonconsecutive axioms are needed to improve the chances of
finding a quantifier-free inductive invariant. It is thus extremely important to start with a
weak abstraction that allows us to examine spurious counterexamples in the BMC unrolling
and find nonconsecutive axiom instantiations, which are then used to identify good prophecy
targets.

4.3. Correctness. We now state two important correctness theorems.
Theorem 4.1. Algorithm 1, instantiated with Abstract-Arrays, a sound model-checker
Prove as described above, and Refine-Arrays is sound, i.e., if it returns true then the
property does hold.
Proof Sketch. Algorithm 1 only returns true if Prove succeeds in proving the property.
Our initial abstraction only removes the array theory semantics, but leaves every other
theory intact, so it is a sound abstraction. The refinement performed by Refine-Arrays is
Vol. 18:3                    COUNTEREXAMPLE-GUIDED PROPHECY                             26:11




also sound. Prophecize first optionally applies Delay depending on the input arguments,
then introduces a prophecy variable. Theorem 2.2 guarantees that Delay preserves the
invariance of the property. Furthermore, introducing a prophecy variable is accomplished
by directly applying Theorem 2.4, followed by Theorem 2.3, which additionally guarantee
that the resulting system and property are invariant if and only if the original property is
invariant on the original system. Thus, the entire Prophecize procedure produces a new
system and property that preserve invariance with respect to the initial query. Finally, each
axiom instantiation is, by definition, valid in the theory of arrays, and lifting them simply
requires them to hold in every state of a path. Furthermore, this does not rule out any true
counterexamples, as the interpretations in true counterexamples must be TA -interpretations.
Therefore, if at any point Prove is able to prove the property, it follows that the original
property holds on the original concrete system, S.                                         
Theorem 4.2. If Algorithm 1, instantiated with Abstract-Arrays, Prove as described
above, and Refine-Arrays, returns false, there is a counterexample in the concrete transition
system.
Proof Sketch. Theorems 2.2, 2.3, and 2.4 ensure that invariance of the property is preserved
when adding auxiliary variables. Algorithm 1 returns false only when Refine-Arrays
returns false in line 6 of Algorithm 3. This occurs if the refinement procedure is unable to
find any array axioms that are violated in the BMC formula (ρ from line 3 of Algorithm 3).
It suffices to prove that if all enumerated axioms hold, then the BMC formula is satisfiable
in TA and there is a length k counterexample.
     The array property fragment [BMS06, BM07, KS16] is a fragment of the theory of
arrays that allows some universal quantification while staying decidable. It is defined for
an extensional theory of arrays with read and write functions with the semantics given by
(write) and (ext). The fragment is of the form ∀~i . φI (~i) → φV (~i), for a vector of bound
index variables ~i, index guard φI , and value constraint φV . Both φI and φV are constrained
by a grammar. Our BMC queries are quantifier-free which falls within the array property
fragment. The only universal quantifiers are hidden by the (const) axiom (because constant
arrays are not explicitly included in the array property fragment theory of arrays). However,
this simple form of universal quantification is contained in the fragment. Thus, our queries
are a strict subset of the more general array property fragment.
     Our axiom enumeration is based on a reduction technique [BMS06, BM07, KS16] for
the array property fragment that is sound and complete. Because the technique is complete,
if the abstract formula is satisfiable and all enumerated axioms are true, then the original
TA formula is satisfiable.                                                                  



                          5. Expressiveness and Limitations


5.1. Expressiveness. We now address the expressiveness of counterexample-guided prophecy
with regard to the introduction of auxiliary variables. For simplicity, we ignore the array
abstraction, relying on the correctness theorems. An inductive invariant using auxiliary
variables can be converted to one without auxiliary variables by first universally quantifying
over the prophecy variables, then existentially quantifying over the history variables. The
details are captured by this theorem:
26:12                M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                  Vol. 18:3




Theorem 5.1. Let S := hX, I, T i be an STS, and P (X) be a property such that S |= P (X).
Let H be the set of history variables, and P be the set ofVprophecy variables introduced by
Refine-Arrays. Let S̃ := hX ∪ H ∪ P, I, T̃ i and P̃ := ( p∈P p = t̃(p)) =⇒ P (X) be the
system and property with auxiliary variables. The function t̃ maps prophecy variables to
their target term from Prophecize. If Inv (X, H, P) is an inductive invariant for S̃ and
entails P̃ , then ∃H∀PInv(X, H, P) is an inductive invariant for S and entails P , where ∃H
and ∀P bind each variable in the set with the corresponding quantifier.
Proof. We assume that Inv (X, H, P) is an inductive invariant that guarantees P̃ . Equiva-
lently, it meets the following conditions:

                                          I˜ |= Inv (X, H, P)                            (initiation)
                                                                0    0   0
                               Inv (X, H, P) ∧ T̃ |= Inv (X , H , P )                 (consecution)
                                     Inv (X, H, P) |= P̃                                 (safety)
We must show that ∃H∀PInv (X, H, P) is an inductive invariant of S and entails P . We
accomplish this by demonstrating that each of the three conditions must hold.
    Initiation: I |= ∃H∀PInv (X, H, P). This holds trivially because I is unchanged, i.e.,
no auxiliary variables appear in the initial state constraint.
    Consecution: ∃H∀PInv (X, H, P) ∧ T |= ∃H 0 ∀P 0 Inv (X 0 , H 0 , P 0 ). This is equivalent to
the following formula (manipulated into negation normal form) being unsatisfiable:
                      ∃H∀PInv (X, H, P) ∧ T ∧ ∀H 0 ∃P 0 ¬Inv (X 0 , H 0 , P 0 )                 (5.1)
     To complete this part of the proof, we introduce the function σ̃ which maps primed
history variables to their next state update term from Delay. For example, suppose we
                                                       0                0
called Delay(S, x, 2) for state variable x, then σ̃(h1x ) = x and σ̃(h2x ) = h1x . Crucially, the
terms in the range of σ̃ do not contain variables from P , because prophecy variables are not
targeted by Prophecize. With this notation, the consecution of Inv (X, H, P) for T̃ means
that the following formula is unsatisfiable:
                                             !              
                              ^                    ^
       Inv (X, H, P) ∧ T ∧       h0 = σ̃(h0 ) ∧       p0 = p ∧ ¬Inv (X 0 , H 0 , P 0 )    (5.2)
                               h∈H                       p∈P

We now show that the fact that (5.2) is unsatisfiable entails that (5.1) is unsatisfiable. First,
observe that (5.2) is equisatisfiable with
                            Inv (X, H, P 0 ) ∧ T ∧ ¬Inv (X 0 , σ̃(H 0 ), P 0 )                  (5.3)
Next, if (5.1) is satisfiable, then the following formula is satisfiable, where we drop the
quantifiers over H and replace them with fresh uninterpreted constants (for convenience,
we simply drop the quantifiers and treat the free variables as uninterpreted constants):
∀PInv (X, H, P) ∧ T ∧ ∀H 0 ∃P 0 ¬Inv (X 0 , H 0 , P 0 ). If this formula is satisfiable, then the
following formula is also satisfiable, where we instantiate the universal quantifier over
H 0 with σ̃(H 0 ): ∀PInv (X, H, P) ∧ T ∧ ∃P 0 ¬Inv (X 0 , σ̃(H 0 ), P 0 ). Finally, if this formula is
satisfiable, then we can drop the existential quantifiers for P 0 and instantiate the universal
quantifier for P with P 0 , which gives that (5.3) is satisfiable. Since (5.3) is unsatisfiable,
then (5.1) must be unsatisfiable as well.
     Safety: ∃H∀PInv (X, H, P) |= P (X). This holds when ∃H∀PInv (X, H, P) ∧ ¬P (X) is
unsatisfiable. To show this, we construct quantifier instantiations such that the resulting
Vol. 18:3                        COUNTEREXAMPLE-GUIDED PROPHECY                                        26:13




formula must be unsatisfiable. We first instantiate all the variables in H with fresh constants
by dropping the existential quantification. Next, we instantiate each of the universally
quantified p ∈ P with their target term t̃(p). Note that this target term might be a
history variable from H which is now instantiated. We allow t̃ to be applied to sets in the
straightforward way. A model for the resulting formula, Inv (X, H, P){P 7→ t̃(P)} ∧ ¬P (X),
would be a counterexample for assumption (safety). Thus it must be unsatisfiable.
     We have shown that initiation holds trivially, and that consecution and safety hold using
quantifier instantiations. Thus, ∃H∀PInv (X, H, P) must be an inductive invariant for S
and P (X).
     Although the invariants found using counterexample-guided prophecy correspond to
∃∀ invariants over the unmodified system, we must acknowledge that the existential power
is very weak. The existential quantifier is only used to remove history variables. While
history variables can certainly be employed for existential power in an invariant [PHM+ 21],
these specific history variables are introduced solely to target a term for prophecy and
only save a term for some fixed, finite number of steps. Thus, we do not expect to gain
much existential power in finding invariants on practical problems. This use of history and
prophecy variables can be thought of as quantifier instantiation at the model checking level,
where the instantiation semantically uses a term appearing in an execution of the system.
Consequently, our technique performs well on systems where there is only a small number of
instantiations needed over terms that are not too distant in time from a potential property
violation that must be disproved (i.e., not many history variables are required). This appears
to be a common situation for invariant-finding benchmarks, as we show empirically in
Section 7.

5.2. Limitations. If our CEGAR loop terminates, it either terminates with a proof or
with a true counterexample. However, it is possible that the procedure may not terminate.
In particular, while we can always refine the abstraction for a given bound k, there is
no guarantee that this will eventually result in a refinement that rules out all spurious
counterexamples (of any length).
     This failure mode occurs, for instance, when no finite number of calls to Prophecize
can capture all the relevant indices of the array. Consider an example system with I := a =
constarr (0 ), T := a0 = write(a, i0 , read (a, i1 ) + 1 ), and P := read (a, ir ) ≥ 0. The array a is
initialized with 0 at every index, and at every step, a is updated at a single index by reading
from an arbitrary index of a and adding 1 to the result.1 Note that the index variables
are unconstrained: they can range over the integers freely at each time step. The property
is that reading from a at ir returns a positive value. This property holds because of a
quantified invariant maintained by the system: ∀i . read (a, i ) ≥ 0.
     However, the initial abstraction is a memoryless array which can easily violate the
property by returning negative values from reads. Since the array is updated in each step
at an arbitrary index based on a read from another arbitrary index, no finite number of
prophecy variables (of the form used in Prophecize) can capture all the relevant indices.
It will successively rule out longer finite spurious counterexamples, but will never be refined
enough to prove the property unboundedly. Note that this is related to our abstraction
and choice to limit prophecy to predicting values a fixed, finite number of steps before a
   1An even simpler system which does not add 1 in the update would already be problematic; however, for
that case, it is straightforward to extend our algorithm to have it learn that the array does not change.
26:14              M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett           Vol. 18:3




potential property violation. Another form of prophecy variable could be used to prove this
property. For example, a prophecy variable that predicts the first index value that stores a
negative value in a could be used to show that this cannot happen.
    We believe that this issue can be circumvented in an automated fashion with future work.
In fact, an approach introduced since the conference version [MIG+ 21] of this paper uses
prophecy variables with a different refinement loop for verifying parameterized protocols,
which cannot be handled by our technique due to this limitation [CGR21].
    A related, but less fundamental issue is that the index set might not contain the best
choice of targets for prophecy. While the index set is sufficient for ruling out bounded
counterexamples, it is possible there is a better target for universal prophecy that does not
appear in the index set. However, based on the evaluation in Section 7, it appears that the
index set does work well in practice.


                               6. Implementation Details
We will now describe our prototype of counterexample-guided prophecy along with some prac-
tical implementation details. Recall that Algorithm 1 can use any unbounded model checking
technique for Prove. In our prototype, we choose to instantiate it with ic3ia [Gri20] (down-
loaded Apr 27, 2020), an open-source C++ implementation of IC3 via Implicit Predicate
Abstraction (IC3IA) [CGMT16], which is itself a CEGAR loop that uses implicit predicate
abstraction to perform IC3 [Bra11, BBW14] on infinite-state systems and uses interpolants
to find new predicates. ic3ia uses MathSAT [CGSS13] (version 5.6.3) as the backend SMT
solver and interpolant producer. We call our prototype prophic3 [MI].



6.1. Engineering Heuristics and Options.

Weak and Strong Abstraction. It is important to have enough prophecy variables to assist in
constructing inductive invariants. We found that we could often obtain a larger, richer set
of prophecy variables by weakening our array abstraction. We do this by replacing equality
between arrays by an uninterpreted predicate, and also checking the congruence axiom, the
converse of (ext). Since more axioms are checked, there are more opportunities to introduce
auxiliary variables. We call this weak abstraction (WA) as opposed to strong abstraction
(SA), which uses regular equality between abstract arrays and guarantees congruence through
UF axioms. Our default configuration uses weak abstraction.


Lemma and Auxiliary Variable Filtering. Although the algorithm depends on introducing
auxiliary variables, an excessive number of unnecessary auxiliary variables could overwhelm
the Prove step. Thus, an improvement not shown in Algorithm 3 is to check consecutive
axioms first and only add nonconsecutive ones when necessary. This is the motivation behind
the custom array solver implementation CheckArrayAxioms based on [BMS06]. In principle,
we could have used an SMT solver to find array axioms, but it would give no preference to
consecutive axioms. Even when enumerating consecutive axioms first, we can still end up
with more auxiliary variables than necessary. We use an unsat-core based procedure to prune
nonconsecutive refinement axioms. In particular, we attempt to remove nonconsecutive
axioms that target indices at times further from the end of the trace, because they would
Vol. 18:3                   COUNTEREXAMPLE-GUIDED PROPHECY                              26:15




   int N ;
   assume ( N > 0 );

   int a [ N ];
   int c ;
   for ( int i = 0 ; i < N ; i ++ ) {
     a[i] = c;
   }

   for ( int j = 0 ; j < N ; j ++ ) {
     assert ( a [ j ] == c );
   }

                                Figure 3. Initialize Array.


introduce more history variables. In practice, this can substantially reduce the number of
added auxiliary variables.
    Similarly, we could overwhelm the algorithm with unnecessary consecutive axioms.
CheckArrayAxioms can still produce hundreds or even thousands of (consecutive) axiom
instantiations. Once these are lifted to the transition system, some may be redundant. To
mitigate this issue, when the BMC check returns ⊥ and we are about to return (line 4 of
Algorithm 3), we keep only axioms that appear in the unsat core of the BMC formula [CGS11].

Abstract Values Refinement Loop. In our implementation, we also include a simple abstraction-
refinement wrapper which abstracts large constant integers and refines them with the actual
values if that fails. This is especially useful for verifying software benchmarks with large
constant loop bounds. Otherwise, the system might need to be unrolled to a very large bound
to reach an abstract counterexample. This was only necessary for a handful of benchmarks
in the first benchmark set.

Assume Property in Pre-State. As long as we are only interested in the first violation of a
property, we can assume that the property was not violated in the past. This observation is
formalized in Theorem 5 of [McM18]. It is common to achieve this for invariant checking by
assuming the property over current state variables in the transition relation, so that every
transition starts in a state satisfying the property.
     In the context of counterexample-guided prophecy, this strategy may prove useful
because the property is weakened with each call to Algorithm 2 (the original property
becomes the consequent of an implication). We can assume the original (stronger) property
in all previous states which can help the algorithm converge.
     Consider the C program shown in Fig. 3, based on one of the benchmarks evaluated
in Section 7. The example populates an array of arbitrary size N , with an arbitrary, fixed,
value c. Fig. 4 shows one possible encoding of this program as an STS. This encoding is
carefully chosen to illustrate a case where assuming the property in the pre-state is needed
for counterexample-guided prophecy to converge. Other possible encodings could avoid this
issue entirely.
26:16               M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett               Vol. 18:3




                     I := i = 0 ∧ j = 0 ∧ ¬err
                     T := i < N → i0 = i + 1 ∧
                          i < N → a0 = write(a, i , c) ∧
                          i < N → j0 = j ∧
                          i < N → err 0 = err ∧
                          (i ≥ N ∧ j < N ) → i0 = i ∧
                          (i ≥ N ∧ j < N ) → a0 = a ∧
                          (i ≥ N ∧ j < N ) → j 0 = j + 1 ∧
                          (i ≥ N ∧ j < N ∧ read (a, j ) = c ∧ ¬err ) → ¬err 0 ∧
                          (i ≥ N ∧ j ≥ N ) → ⊥
                    P := ¬err

                          Figure 4. Possible STS encoding of Fig. 3.

     In this encoding, if we do not assume the original property in the pre-state, we observed
that prophic3 would diverge and introduce an increasing number of prophecy variables.
Consider a case where N is assigned a specific value, 5. Since the array abstraction starts
memoryless, the algorithm needs to add 5 prophecy variables to refine the memory. However,
since N is arbitrary, this results in an infinite chain of new prophecy variables as longer traces
are considered. Furthermore, each time a prophecy variable is introduced, the underlying
IC3IA algorithm is restarted with a weaker property. This means that the original property,
¬err , cannot be assumed in the pre-state. Note, the new property produced by Prophecize
is an implication that will be trivially true in most of the path. The most important part
of the transition relation in Fig. 4 to consider is the second-to-last line of T . Let that be
the error rule. Since we do not assume ¬err , the error rule might be trivially satisfied.
Intuitively, without this assumption, we need to justify the assertion for the value of index j
at every time-step.
     However, we know it is safe to assume the original property in the pre-state for counter-
example guided prophecy. If we do so, the algorithm converges. This is because that
assumption coupled with predicting a single j, one step before a potential property violation,
is sufficient to enforce the error rule which ensures ¬err holds in the next state.


Important Variables. In many implementations of IC3IA, including ic3ia, new predicates
are obtained by mining interpolants from an unsatisfiable spurious counterexample trace
conjoined with the concrete unrolled transitions. Typically not all of these predicates are
necessary, so they are often reduced using unsatisfiable cores. However, in the context of
counterexample-guided prophecy, we might prefer certain predicates. In particular, predicates
involving prophecy variables are good candidates, since we know the prophecy variable was
necessary to rule out a spurious counterexample. Note that there are two levels of abstraction
refinement in this context: the array abstraction and refinement for counterexample-guided
prophecy, and the predicate abstraction in IC3IA. Here, we are focused on the latter. One
heuristic we tried is always keeping predicates that use a prophecy variable.
Vol. 18:3                     COUNTEREXAMPLE-GUIDED PROPHECY                                  26:17




Finite-domain Indices. In this paper, we have assumed that the index sort has an infinite
domain. This fits our domain of problems that require quantified invariants. If the sort is
finite, a universal quantifier could in principle be enumerated by instantiating it with every
possible value. Although, it is certainly possible that a quantifier is much more efficient
than this enumeration.
     The restriction to infinite domain indices is also a technical limitation of the array solving
technique of [BMS06], which our approach is based on. This restriction is shared by many
SMT solvers, particularly when there are chains of equalities between writes on constant
arrays with different bases, e.g., a = constarr (08 ) ∧ b = constarr (18 ) ∧ write(a, i2 , e8 ) =
write(b, j2 , d8 ), where cw is a bitvector variable or value c with width w. An infinite domain
allows us to assume that there is always an index value that has not been used in the array
formula. This is crucial for the λ index, which has the primary goal of referring to indices
initialized by the constant array axiom that were never overwritten. In a finite domain, we
cannot make this assumption. See [BMS06, BM07] for more information on the λ index.
     This limitation is only with regards to the array axiom enumeration. The other contribu-
tions of this paper, including using prophecy variables in place of universal quantification, are
entirely applicable over finite domains. One low-effort approach for applying counterexample-
guided prophecy over finite-domain indices is to give up completeness. By simply not
including axioms over a λ index for finite-domain sorts, the array solving procedure might
conclude the query is satisfiable when it is actually unsatisfiable. Thus, the overall algorithm
could return spurious counterexamples, but would still soundly return proofs. A given
spurious counterexample is finite and would be straightforward to analyze, either with a
dedicated checker or an SMT solver without this limitation.

                                       7. Experiments

7.1. Setup. We evaluate our tool against three state-of-the-art tools for inferring universally
quantified invariants over linear arithmetic and arrays: freqhorn, quic3, and gspacer. All
these tools are Constrained Horn Clause (CHC) solvers built on Z3 [dMB08]. The algorithm
implemented in this version of freqhorn [Fedb] is a syntax-guided synthesis [ABD+ 15]
approach for inferring universally quantified invariants over arrays [FPMG19]. quic3 is
built on Spacer [KGC14], the default CHC engine in Z3, and extends IC3 over linear
arithmetic and arrays to allow universally quantified frames (frames are candidates for
inductive invariants maintained by the IC3 algorithm) [GSV18]. It also maintains a set
of quantifier instantiations which are provided to the underlying SMT solver. quic3 was
recently incorporated into Z3. We used Z3 version 4.8.9 with parameters suggested by the
quic3 authors.2 Finally, gspacer is an extension of Spacer which adds three new inference
rules for improving local generalizations with global guidance [KCSG20]. While this last
technique does not specifically target universally quantified invariants, it can be used along
with the quic3 options in Spacer and potentially executes a much different search. The
gspacer submission [KG20] won the arrays category in CHC-COMP 2020 [R2̈0b]. We use
the same configuration entered in the competition. We also include ic3ia and the default
configuration of Spacer in our results, neither of which can produce universally quantified
invariants. Our default configuration of prophic3 uses weak abstraction. We chose to
   2fp.spacer.q3.use qgen=true fp.spacer.ground pobs=false
fp.spacer.mbqi=false fp.spacer.use euf gen=true
26:18              M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett           Vol. 18:3




build our prototype on ic3ia instead of Spacer, in part because we needed uninterpreted
functions for our array abstraction, and Spacer does not handle them in a straightforward
way, due to the semantics of CHC [BGMR15].
     We compare these solvers on four benchmark sets: i) freqhorn — all benchmarks
containing arrays in [Feda] from the freqhorn paper [FPMG19]; ii) quic3 — benchmarks
from the quic3 paper [GSV18] (these were C programs from SV-COMP [Bey17] that were
modified to require universally quantified invariants); iii) vizel — additional benchmarks
provided to us by the authors of [GSV18]; and iv) chc-comp-2020 — the array category
benchmarks of CHC-COMP 2020 [R2̈0a] (as explained below, these contain a translation
of the quic3 benchmarks). Additionally, we sort the benchmarks into four categories: 1)
Q — safe benchmarks solved by some tool supporting quantified invariants but none of the
solvers that do not; 2) QF — those solved by at least one of the tools that do not support
quantified invariants, plus any unsafe benchmarks; 3) US — unsafe benchmarks and 4)
UK — unknown (i.e., unsolved) benchmarks. Because not all of the benchmark sets were
guaranteed to require quantifiers, this is an approximation of which benchmarks required
quantified reasoning to prove safe.
     Both prophic3 and ic3ia take a transition system and property specified in the
Verification Modulo Theories (VMT) format [CRGI11], which is a transition system format
built on SMT-LIB [BFT16]. All other solvers read the CHC format. We translated benchmark
sets freqhorn and chc-comp-2020 from CHC to VMT using the horn2vmt program which is
distributed with ic3ia. For benchmark sets quic3 and vizel, we started with the C programs
and generated both VMT and CHC using Kratos2 (an updated version of Kratos [CGM+ 11]).
We note that chc-comp-2020 includes another translation of the quic3 benchmarks to CHC
by SeaHorn [GKKN15]. We ran all experiments on a 3.5GHz Intel Xeon E5-2637 v4 CPU
with a timeout of 2 hours and a memory limit of 32GB.


7.2. Results. The results are shown in Fig. 6 as a table. Fig. 5 shows cactus plots
demonstrating the number of solved benchmarks over time.We first observe that prophic3
solves the most benchmarks in the freqhorn, quic3, and vizel benchmark sets, both overall
and in category Q. The quic3 (and most of the freqhorn) benchmarks require quantified
invariants; thus, ic3ia and Spacer cannot solve any of them. On solved instances in the Q
category, prophic3 introduced an average of 1.2 prophecy variables and a median of 1. This
makes sense because, upon inspection, most benchmarks only require one quantifier and we
are careful to only introduce prophecy variables when needed. On benchmarks it cannot
solve, ic3ia either times out or fails to compute an interpolant. This is expected because
quantifier-free interpolants are not guaranteed over the standard theory of arrays. Even
without arrays, it is also possible for prophic3 to fail to compute an interpolant, because
MathSAT’s interpolation procedure is incomplete for combinations with non-convex theories
such as integers. However, this was rarely observed in practice.
     We further observe that prophic3 does not perform as well on unsafe benchmarks. This
is expected, because our array solving procedure is enumeration-based and should be slower
than the array theory solvers within an SMT solver. However, we believe that a dedicated
array solving procedure is important for performance of the overall algorithm and especially
safe benchmarks. We tried minimal experiments with obtaining array lemmas directly from
the SMT solver and did not achieve comparable performance. This is likely because our
array solver is aware of the ultimate goal to run Prophecize with a small delay and can
Vol. 18:3                   COUNTEREXAMPLE-GUIDED PROPHECY                          26:19




                 Figure 5. Number of solved benchmarks over time (sorted).


enumerate array axioms in a corresponding order, starting with index instantiations that
would require the fewest history variables.
     There was one discrepancy in our experiments. On chc-LIA-lin-arrays 381 gspacer
disagrees with quic3, Spacer, and prophic3. This is the same discrepancy mentioned in the
CHC-COMP 2020 report [R2̈0b]. prophic3 proved this benchmark safe without introducing
any auxiliary variables and we used both CVC4 [BCD+ 11] and MathSAT to verify that the
solution was indeed an inductive invariant for the concrete system. We are confident that
this benchmark is safe and thus do not count it as a solved instance for gspacer.
26:20               M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                 Vol. 18:3




solver                 freqhorn (81) quic3 (43) vizel (33) chc-comp-2020 (501)         total
prophic3                   66/5/0       41/0/0      22/3/1          42/159/56      171/167/57
freqhorn                   65/4/0        0/0/0      0/1/0             4/46/1         69/51/1
quic3                      55/4/0       34/0/0      15/4/1          74/137/75      178/145/76
gspacer                    34/5/0       27/0/0      18/3/1          66/139/94      145/147/95
Spacer                     0/5/0        0/0/0       0/4/1           0/134/77        0/143/78
ic3ia                      0/4/0        0/0/0       0/3/1           0/158/60        0/165/61

          Figure 6. Experimental results. They are reported as # Q / # QF / # US.


solver                 freqhorn (81) quic3 (43) vizel (33) chccomp2020 (501)          total
prophic3                  66/5/0        41/0/0      22/3/1          42/159/56      171/167/57
prophic3 sa               62/5/0        38/0/0      20/3/1          41/159/65      161/167/66
prophic3 nav              57/4/0        42/0/0      21/3/1          43/160/55      163/167/56
prophic3 na               68/4/0        41/0/0      18/3/1          44/159/56      171/166/57
prophic3 npr              66/4/0        42/0/0      20/3/1          45/159/56      173/166/57
prophic3 ntp              66/4/0        40/0/0      20/3/1          33/159/56      159/166/57
prophic3 nur              66/5/0        42/0/0      20/3/1          40/159/55      168/167/56
prophic3 nhp              68/4/0        41/0/0      22/3/1          42/159/56      173/166/57
prophic3 nar              64/4/0        42/0/0      21/3/1          42/159/55      169/166/56
prophic3 noheur           65/5/0        38/0/0      13/3/1          28/158/57      144/166/58

         Figure 7. Self-comparison with different options, reported as # Q / # QF / # US.



    Some of the tools are sensitive to the encoding. Since it is syntax-guided, freqhorn is
sensitive to the encoding syntax. The freqhorn benchmarks were hand-written in CHC to be
syntactically simple; this simplicity is maintained by horn2vmt and also benefits prophic3.
However, prophic3 can be sensitive to other encodings. For example, the quic3 benchmarks
translated by SeaHorn and included in chc-comp-2020 are much harder for prophic3 to
solve (after translation by horn2vmt) compared to the direct C to VMT translation using
Kratos2. We found that prophic3 solves 6 benchmarks when translated by horn2vmt ◦
SeaHorn, versus 41 when translated directly by Kratos2. We stress that the CHC solvers
performed similarly on both encodings: our experiments showed that quic3 and freqhorn
solved exactly the same number in both translations, and gspacer solved 27 when translated
with Kratos2 and 34 when translated with SeaHorn. Importantly, prophic3 on the Kratos2
encoding solved more benchmarks than any other tool and encoding pair.
    There are two main reasons why prophic3 fails on the SeaHorn encodings. First, due
to the LLVM-based encoding, some of the SeaHorn translations have index sets which are
insufficient for finding the right prophecy variable. This has to do with the memory encoding
and the way that fresh variables and guards are used. SeaHorn also splits memories into
ranges which is problematic for our technique. Second, the SeaHorn translation is optimized
for CHC, not for transition systems. For example, it introduces many new variables, and
the argument order between different predicates may not match. In the transition system,
this essentially has the effect of interchanging the values of variables between each loop.
Vol. 18:3                     COUNTEREXAMPLE-GUIDED PROPHECY                                  26:21




SeaHorn has options that address some of these issues, and these helped prophic3 solve
more benchmarks, but none of these options produce encodings that work as well as the
Kratos2 encodings. The difference between good CHC and transition system encodings
could also explain the overall difference in performance on chc-comp-2020 benchmarks, most
of which were translated by SeaHorn. Both of these issues are practical, not fundamental,
and we believe they can be resolved with additional engineering effort.


7.3. Self Comparison. Next, we run a self-comparison using different options in prophic3.
We accomplish this by starting with the configuration used above, and dropping a single
feature to obtain a new configuration. This serves as a metric of how important each
heuristic is to the overall performance of prophic3. Each configuration has a unique string
identifying it as follows:
(1) sa: with strong abstraction;
(2) nav: no outer CEGAR loop that abstracts large values;
(3) na: no assuming property in pre-state;
(4) npr: no attempting to reduce the number of prophecy variables introduced;
(5) ntp: no tracking prophecy variables as important variables to guide IC3IA to useful
     predicates;
(6) nur: no unsat-core based reduction when enumerating timed axioms;
(7) nhp: no seeding IC3IA with predicates obtained from equalities between history variables
     and targets over current state variables, e.g., if h10
                                                         t = t is in the transition relation, would
     add h1x = t as a predicate;
(8) nar: no additional reduction of consecutive axioms (differs from nur in that the consec-
     utive axioms are lifted first);
(9) noheur: a combination of 2-8.
     Fig. 7 shows the results in a table and Fig. 8 plots the number of solved benchmarks over
time. We observe that prophic3 sa solves fewer benchmarks in the freqhorn, quic3, and vizel
sets. However, it is faster on commonly solved instances. This makes sense because it needs
to check fewer axioms (it uses built-in equality and thus does not check equality axioms). We
suspect that it solves fewer benchmarks in the first three sets because it was unable to find the
right prophecy variable. For example, for the standard find true-unreach-call ground
benchmark in the quic3 set, a prophecy variable is needed to find a quantifier-free invariant.
However, because of the stronger reasoning power of SA, the system can be sufficiently
refined without introducing auxiliary variables. ic3ia is then unable to prove the property
on the resulting system without the prophecy variable, instead timing out. Interestingly,
notice that prophic3 sa solves the most benchmarks in the QF category overall, suggesting
that there are practical performance benefits of the CEGAR approach even when quantified
reasoning is not needed.
     Feature nav is the additional CEGAR loop for abstracting large values. The results
show that this primarily affects the freqhorn benchmarks. This is expected because those
contained several examples with large, constant loop bounds. This means a quantifier was
not strictly necessary, but was needed in practice. Without abstracting the loop bound,
Algorithm 3 would take far too long to reach spurious counterexamples due to the large
unrolling bound before an error state is reached.
     Based on these results, each of the other heuristics alone do not make a big difference
for these benchmarks. However, the noheur experiments demonstrates that dropping all
26:22              M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett             Vol. 18:3




         Figure 8. Number of solved benchmarks in self-comparison over time (sorted)




of them simultaneously does negatively impact performance. It is slower overall in the
cactus plots of Fig. 8, and solves markedly less in the vizel and chc-comp-2020 benchmark
sets. The core algorithm performs well alone, but the heuristics interact to further improve
performance.
Vol. 18:3                    COUNTEREXAMPLE-GUIDED PROPHECY                              26:23




                                    8. Related Work
We refer often to McMillan’s work in [McM18]. In that paper, McMillan reduces infinite-state
model checking problems to finite-state problems that can be checked with a SAT-based
model checking algorithm by eagerly instantiating axioms. Not all possible axioms are
instantiated, which is why this is an eager abstraction. This process requires introducing
auxiliary variables. We use several of the same theorems, but for a different goal. Rather
than reducing infinite-state to finite-state systems, we are interested in reducing problems
with quantified inductive invariants to ones with quantifier-free ones. Furthermore, while
the approach of [McM18] is a very general framework that is primarily applied manually, we
focused on infinite arrays and provided a fully automated algorithm.
     There are two important related approaches for abstracting arrays in horn clauses [MG16]
and memories in hardware [Bje08]. Both make a similar observation that arrays can be
abstracted by modifying the property to maintain values at only a finite set of symbolic
indices. We differ from the former by using a refinement loop that automatically adjusts
the precision and targets relevant indices. The latter is also a refinement loop that adjusts
precision, but differs in the domain and the refinement approach, which uses a multiplexor
tree. Although neither paper uses the term prophecy variable, their refinement approaches
can be viewed as prophecy-variable based. We differ from both approaches in our use of
array axioms to automatically find and add auxiliary variables.
     A similar lazy array axiom instantiation technique is proposed in [BCS20]. However,
their technique utilizes interpolants for finding violated axioms and cannot infer univer-
sally quantified invariants. The work of [CGI+ 18] also uses lazy axiom-based refinement,
abstracting non-linear arithmetic with uninterpreted functions. We differ in the domain and
the use of auxiliary variables. In [PHM+ 21], prophecy variables defined by temporal logic
formulas are used for liveness and temporal proofs, with the primary goal of increasing the
power of a temporal proof system. In contrast, we use prophecy variables here for a different
purpose, and we also find them automatically. The work of [CN09] includes an approach
for synthesizing auxiliary variables for modular verification of concurrent programs. Our
approach differs significantly in the domain and details.
     There is a substantial body of work on automated quantified invariant generation for
arrays using first-order theorem provers [KV13, CKR16, KV09, McM08]. These include
extensions to saturation-based theorem proving to analyze specific kinds of predicates, and
an extension to paramodulation-based theorem proving to produce universally quantified
interpolants. In [LTZZ16], the authors propose an abstract interpretation approach to
synthesize universally quantified array invariants. Our method also uses abstraction, but in
a CEGAR framework.
     Two other notable approaches capable of proving properties over arrays that require
invariants with alternating quantifiers are [GGK20, PS20]. The former proposes trace logic
for extending first-order theorem provers to software verification, and the latter takes a
counterexample-guided inductive synthesis approach. Our approach takes a model checking
perspective and differs significantly in the details. While these approaches are more general,
we compared against state-of-the-art tools that focus specifically on universally quantified
invariants.
     MCMT [GR10, GKLT12, CGK+ 17] and its derivatives [ABG+ 12, AGS14] are backward-
reachability algorithms for proving properties over “array-based systems,” which are typically
used to model parameterized protocols. These approaches target syntactically restricted
26:24              M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett             Vol. 18:3




functional transition systems with universally quantified properties, whereas our approach
targets general transition systems. Two other approaches for solving parameterized systems
modeled with arrays are [GSM16] and [MGJ+ 19]. The former iteratively fixes the number
of expected universal quantifiers, then eagerly instantiates them and encodes the invariant
search to nonlinear CHC. The latter first uses a finite-state model checker to discover an
inductive invariant for a specific parameterization and then applies a heuristic generalization
process. We differ from all these techniques in domain and the use of auxiliary variables.
Due to the limitations explained in Section 5, we do not expect our approach to work well
for parameterized protocol verification without improvements.
     In [LB04], heuristics are proposed for finding predicates with free indices that can
be universally quantified in a predicate abstraction-based inductive invariant search. Our
approach is counterexample-guided and does not utilize predicate abstraction directly
(although IC3IA does). The authors of [KKRS17] propose a technique for Java programs
that associates heap memory with the program location where it was allocated and generates
CHC verification conditions. This enables the discovery of invariants over all heap memory
allocated at that location, which implicitly provides quantified invariants. This is similar to
our approach in that it gives quantification power without explicitly using quantifiers and
in that their encoding removes arrays. However, we differ in that we focus on transition
systems and utilize a different paradigm to obtain this implicit quantification. Prophecy
variables have also been proposed for Hoare-style reasoning about concurrent programs.
In [ZFF+ 12], the authors formalize “structural” prophecy variables for Hoare logic, which
can only predict state within their own thread. The authors of [JLP+ 20] generalize this
approach for separation logic to allow predicting values between different threads. Our work
differs in the domain and level of automation.


                                       9. Conclusion
We presented a novel approach for model checking transition systems containing arrays. We
observed that history and prophecy variables can be extremely useful for reducing quantified
invariants to quantifier-free invariants. We demonstrated that an initially weak abstraction
in our CEGAR loop can help us to automatically introduce relevant auxiliary variables.
Finally, we evaluated our approach on four sets of interesting array-manipulating benchmarks.
In future work, we hope to improve performance, explore a tighter integration with the
underlying model checker, address the limitations described in Section 5, and investigate
applications of counterexample-guided prophecy to other theories.


                                     Acknowledgment
This work was supported by the National Science Foundation Graduate Research Fellowship
Program under Grant No. DGE-1656518. Any opinions, findings, and conclusions or
recommendations expressed in this material are those of the author(s) and do not necessarily
reflect the views of the National Science Foundation. Additional support was provided by
DARPA, under grant No. FA8650-18-2-7854. We thank these sponsors for their support.
We would also like to thank Alessandro Cimatti for his invaluable feedback on the initial
ideas of this paper.
Vol. 18:3                        COUNTEREXAMPLE-GUIDED PROPHECY                                      26:25




                                 Data Availability Statement
The experimental results and the necessary software (on the TACAS 2021 Ubuntu 20.04
virtual machine [HJN20]) for reproducing the results shown in Figure 6 are available in the
Figshare repository: https://doi.org/10.6084/m9.figshare.13619096.




                                             References
      +
[ABD 15] Rajeev Alur, Rastislav Bodı́k, Eric Dallal, Dana Fisman, Pranav Garg, Garvit Juniwal, Hadas
           Kress-Gazit, P. Madhusudan, Milo M. K. Martin, Mukund Raghothaman, Shambwaditya Saha,
           Sanjit A. Seshia, Rishabh Singh, Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa.
           Syntax-guided synthesis. In Dependable Software Systems Engineering, volume 40, pages 1–25.
           IOS Press, 2015.
[ABG+ 12] Francesco Alberti, Roberto Bruttomesso, Silvio Ghilardi, Silvio Ranise, and Natasha Sharygina.
           SAFARI: SMT-based abstraction for arrays with interpolants. In CAV, volume 7358 of Lecture
           Notes in Computer Science, pages 679–685. Springer, 2012.
[AGS14]    Francesco Alberti, Silvio Ghilardi, and Natasha Sharygina. Booster: An acceleration-based
           verification framework for array programs. In ATVA, volume 8837 of Lecture Notes in Computer
           Science, pages 18–23. Springer, 2014.
[AL88]     Martin Abadi and Leslie Lamport. The existence of refinement mappings. In Proceedings of the
           3rd Annual Symposium on Logic in Computer Science, pages 165–175, July 1988. LICS 1988 Test
           of Time Award. URL: https://www.microsoft.com/en-us/research/publication/the-existence-of-
           refinement-mappings/.
[BB08]     Robert Brummayer and Armin Biere. Lemmas on demand for the extensional theory of arrays.
           In Proceedings of the Joint Workshops of the 6th International Workshop on Satisfiability Modulo
          Theories and 1st International Workshop on Bit-Precise Reasoning, SMT ’08/BPR ’08, page 6–11,
           New York, NY, USA, 2008. Association for Computing Machinery. doi:10.1145/1512464.1512467.
[BBW14] Johannes Birgmeier, Aaron R. Bradley, and Georg Weissenbacher. Counterexample to induction-
           guided abstraction-refinement (CTIGAR). In CAV, volume 8559 of Lecture Notes in Computer
           Science, pages 831–848. Springer, 2014.
[BCCZ99] Armin Biere, Alessandro Cimatti, Edmund Clarke, and Yunshan Zhu. Symbolic model checking
           without BDDs. In W. Rance Cleaveland, editor, Tools and Algorithms for the Construction and
           Analysis of Systems, pages 193–207, Berlin, Heidelberg, 1999. Springer Berlin Heidelberg.
[BCD+ 11] Clark Barrett, Christopher L. Conway, Morgan Deters, Liana Hadarean, Dejan Jovanović, Tim
           King, Andrew Reynolds, and Cesare Tinelli. CVC4. In Ganesh Gopalakrishnan and Shaz Qadeer,
           editors, Proceedings of the 23rd International Conference on Computer Aided Verification (CAV
          ’11), volume 6806 of Lecture Notes in Computer Science, pages 171–177. Springer, July 2011.
           Snowbird, Utah. URL: http://www.cs.stanford.edu/∼barrett/pubs/BCD+11.pdf.
[BCS20]    Denis Bueno, Arlen Cox, and Karem Sakallah. EUFicient reachability for software with arrays.
           In Formal Methods in Computer Aided Design, 2020.
[Bey17]    Dirk Beyer. Software verification with validation of results - (report on SV-COMP 2017). In
          TACAS (2), volume 10206 of Lecture Notes in Computer Science, pages 331–349, 2017.
[BFT16]    Clark Barrett, Pascal Fontaine, and Cesare Tinelli. The Satisfiability Modulo Theories Library
          (SMT-LIB). www.SMT-LIB.org, 2016.
[BGMR15] Nikolaj Bjørner, Arie Gurfinkel, Kenneth L. McMillan, and Andrey Rybalchenko. Horn clause
           solvers for program verification. In Fields of Logic and Computation II, volume 9300 of Lecture
           Notes in Computer Science, pages 24–51. Springer, 2015.
[BGR12] Roberto Bruttomesso, Silvio Ghilardi, and Silvio Ranise. Quantifier-free interpolation of a theory
           of arrays. Logical Methods in Computer Science, 8, 04 2012. doi:10.2168/LMCS-8(2:4)2012.
[Bje08]    P. Bjesse. Word-level sequential memory abstraction for model checking. In 2008 Formal Methods
           in Computer Aided Design, pages 1–9, Nov 2008. doi:10.1109/FMCAD.2008.ECP.20.
[BM07]     Aaron R. Bradley and Zohar Manna. The calculus of computation - decision procedures with
           applications to verification. Springer, 2007.
26:26                M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                     Vol. 18:3




[BMS06]   Aaron R. Bradley, Zohar Manna, and Henny B. Sipma. What’s decidable about arrays? In
          E. Allen Emerson and Kedar S. Namjoshi, editors, Verification, Model Checking, and Abstract
          Interpretation, pages 427–442, Berlin, Heidelberg, 2006. Springer Berlin Heidelberg.
[Bra11]   Aaron R. Bradley. SAT-based model checking without unrolling. In VMCAI, volume 6538 of
          Lecture Notes in Computer Science, pages 70–87. Springer, 2011.
[BT18]    Clark W. Barrett and Cesare Tinelli. Satisfiability modulo theories. In Handbook of Model
          Checking, pages 305–343. Springer, 2018.
[CGI+ 18] Alessandro Cimatti, Alberto Griggio, Ahmed Irfan, Marco Roveri, and Roberto Sebastiani.
          Incremental linearization for satisfiability and verification modulo nonlinear arithmetic and
          transcendental functions. ACM Trans. Comput. Log., 19(3):19:1–19:52, 2018.
[CGK+ 17] Sylvain Conchon, Amit Goel, Sava Krstic, Rupak Majumdar, and Mattias Roux. FAR-cubicle -
          A new reachability algorithm for Cubicle. In FMCAD, pages 172–175. IEEE, 2017.
[CGM+ 11] Alessandro Cimatti, Alberto Griggio, Andrea Micheli, Iman Narasamdya, and Marco Roveri.
          Kratos - A software model checker for SystemC. In CAV, volume 6806 of Lecture Notes in
          Computer Science, pages 310–316. Springer, 2011.
[CGMT16] Alessandro Cimatti, Alberto Griggio, Sergio Mover, and Stefano Tonetta. Infinite-state invariant
          checking with IC3 and predicate abstraction. Formal Methods in System Design, 49(3):190–218,
          2016.
[CGR21] Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi. Universal invariant checking of
          parametric systems with quantifier-free SMT reasoning. In CADE, volume 12699 of Lecture Notes
          in Computer Science, pages 131–147. Springer, 2021.
[CGS11]   Alessandro Cimatti, Alberto Griggio, and Roberto Sebastiani. Computing small unsatisfiable
          cores in satisfiability modulo theories. J. Artif. Intell. Res., 40:701–728, 2011.
[CGSS13] Alessandro Cimatti, Alberto Griggio, Bastiaan Schaafsma, and Roberto Sebastiani. The Math-
          SAT5 SMT Solver. In Nir Piterman and Scott Smolka, editors, Proceedings of TACAS, volume
          7795 of LNCS. Springer, 2013.
[CH15]    Jürgen Christ and Jochen Hoenicke. Weakly equivalent arrays. In Carsten Lutz and Silvio Ranise,
          editors, Frontiers of Combining Systems, pages 119–134, Cham, 2015. Springer International
          Publishing.
[CKR16] Yuting Chen, Laura Kovács, and Simon Robillard. Theory-specific reasoning about loops with
          arrays using Vampire. In Vampire@IJCAR, volume 44 of EPiC Series in Computing, pages 16–32.
          EasyChair, 2016.
[Cla03]   Edmund M. Clarke. Counterexample-guided abstraction refinement. In TIME, page 7. IEEE
          Computer Society, 2003.
[CN09]    Ariel Cohen and Kedar S. Namjoshi. Local proofs for global safety properties. Formal Methods
          Syst. Des., 34(2):104–125, 2009.
[Cra57]   William Craig. Linear reasoning. A new form of the Herbrand-Gentzen theorem. J. Symb. Log.,
          22(3):250–268, 1957.
[CRGI11] Alessandro Cimatti, Marco Roveri, Alberto Griggio, and Ahmed Irfan. Verification Modulo
          Theories. http://www.vmt-lib.org, 2011.
[dB09]    L. de Moura and N. Bjørner. Generalized, efficient array decision procedures. In 2009 Formal
          Methods in Computer-Aided Design, pages 45–52, Nov 2009. doi:10.1109/FMCAD.2009.5351142.
[dMB08] Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In C. R. Ramakrishnan
          and Jakob Rehof, editors, Tools and Algorithms for the Construction and Analysis of Systems,
          pages 337–340, Berlin, Heidelberg, 2008. Springer Berlin Heidelberg.
[Feda]    Grigory Fedyukovich. Freqhorn benchmarks. URL: https://github.com/grigoryfedyukovich/aeval/
          tree/615f4c4abfd51550d939495841aa9a531d4f09e2/bench horn.
[Fedb]    Grigory Fedyukovich. Freqhorn implementation. URL: https://github.com/grigoryfedyukovich/
          aeval/commit/f5cc11808c1b73886a4e7d5a71daeffb45470b9a.
[FPMG19] Grigory Fedyukovich, Sumanth Prabhu, Kumar Madhukar, and Aarti Gupta. Quantified invariants
          via syntax-guided synthesis. In CAV (1), volume 11561 of Lecture Notes in Computer Science,
          pages 259–277. Springer, 2019.
[GGK20] Pamina Georgiou, Bernhard Gleiss, and Laura Kovács. Trace logic for inductive loop reasoning.
          In Formal Methods in Computer Aided Design, 2020.
Vol. 18:3                        COUNTEREXAMPLE-GUIDED PROPHECY                                      26:27




[GKF08]   Amit Goel, Sava Krstić, and Alexander Fuchs. Deciding array formulas with frugal axiom
          instantiation. In Proceedings of the Joint Workshops of the 6th International Workshop on
          Satisfiability Modulo Theories and 1st International Workshop on Bit-Precise Reasoning, SMT
          ’08/BPR ’08, page 12–17, New York, NY, USA, 2008. Association for Computing Machinery.
          doi:10.1145/1512464.1512468.
[GKKN15] Arie Gurfinkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A. Navas. The SeaHorn
          verification framework. In CAV (1), volume 9206 of Lecture Notes in Computer Science, pages
          343–361. Springer, 2015.
[GKLT12] Amit Goel, Sava Krstic, Rebekah Leslie, and Mark R. Tuttle. SMT-based system verification with
          DVF. In SMT@IJCAR, volume 20 of EPiC Series in Computing, pages 32–43. EasyChair, 2012.
[GR10]    Silvio Ghilardi and Silvio Ranise. MCMT: A model checker modulo theories. In Jürgen Giesl and
          Reiner Hähnle, editors, Automated Reasoning, pages 22–29, Berlin, Heidelberg, 2010. Springer
          Berlin Heidelberg.
[Gri20]   Alberto Griggio. Open-source IC3 modulo theories with implicit predicate abstraction.
          https://es-static.fbk.eu/people/griggio/ic3ia/index.html, Accessed 2020. URL: https:
          //es-static.fbk.eu/people/griggio/ic3ia/index.html.
[GSM16] Arie Gurfinkel, Sharon Shoham, and Yuri Meshman. SMT-based verification of parameterized
          systems. In SIGSOFT FSE, pages 338–348. ACM, 2016.
[GSV18]   Arie Gurfinkel, Sharon Shoham, and Yakir Vizel. Quantifiers on demand. In Shuvendu K. Lahiri
          and Chao Wang, editors, Automated Technology for Verification and Analysis, pages 248–266,
          Cham, 2018. Springer International Publishing.
[HJN20]   Sebastian Hjort Hyberts, Peter Gjøl Jensen, and Thomas Neele. Tacas 21 artifact evaluation vm -
          ubuntu 20.04 lts, September 2020. doi:10.5281/zenodo.4041464.
[Hod93]   Wilfrid Hodges. Model theory, volume 42 of Encyclopedia of mathematics and its applications.
          Cambridge University Press, 1993.
[JLP+ 20] Ralf Jung, Rodolphe Lepigre, Gaurav Parthasarathy, Marianna Rapoport, Amin Timany, Derek
          Dreyer, and Bart Jacobs. The future is ours: prophecy variables in separation logic. Proc. ACM
          Program. Lang., 4(POPL):45:1–45:32, 2020.
[KCSG20] Hari Govind Vediramana Krishnan, YuTing Chen, Sharon Shoham, and Arie Gurfinkel. Global
          guidance for local generalization in model checking. In CAV (2), volume 12225 of Lecture Notes
          in Computer Science, pages 101–125. Springer, 2020.
[KG20]    Hari Govind Vediramana Krishnan and Arie Gurfinkel. Spacer CHC-COMP 2020 Submission,
          2020. URL: https://www.starexec.org/starexec/secure/details/configuration.jsp?id=350966.
[KGC14] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. SMT-based model checking for recursive
          programs. In Armin Biere and Roderick Bloem, editors, Computer Aided Verification, pages
          17–34, Cham, 2014. Springer International Publishing.
[KKRS17] Temesghen Kahsai, Rody Kersten, Philipp Rümmer, and Martin Schäf. Quantified heap invariants
          for object-oriented programs. In LPAR, volume 46 of EPiC Series in Computing, pages 368–384.
          EasyChair, 2017.
[KMZ06] Deepak Kapur, Rupak Majumdar, and Calogero G. Zarba. Interpolation for data structures. In
          SIGSOFT FSE, pages 105–116. ACM, 2006.
[KS16]    Daniel Kroening and Ofer Strichman. Decision Procedures - An Algorithmic Point of View,
          Second Edition. Texts in Theoretical Computer Science. An EATCS Series. Springer, 2016.
[KV09]    Laura Kovács and Andrei Voronkov. Finding loop invariants for programs over arrays using a
          theorem prover. In FASE, volume 5503 of Lecture Notes in Computer Science, pages 470–485.
          Springer, 2009.
[KV13]    Laura Kovács and Andrei Voronkov. First-order theorem proving and Vampire. In CAV, volume
          8044 of Lecture Notes in Computer Science, pages 1–35. Springer, 2013.
[LB04]    Shuvendu K. Lahiri and Randal E. Bryant. Indexed predicate discovery for unbounded system
          verification. In CAV, volume 3114 of Lecture Notes in Computer Science, pages 135–147. Springer,
          2004.
[LTZZ16] B. Li, Z. Tang, J. Zhai, and J. Zhao. Automatic invariant synthesis for arrays in simple programs.
          In 2016 IEEE International Conference on Software Quality, Reliability and Security (QRS),
          pages 108–119, Aug 2016. doi:10.1109/QRS.2016.23.
26:28                  M. Mann, A. Irfan, A. Griggio, O. Padon, and C. Barrett                                               Vol. 18:3




[Mcc62]   J. Mccarthy. Towards a mathematical science of computation. In In IFIP Congress, pages 21–28.
          North-Holland, 1962.
[McM08] K. L. McMillan. Quantified invariant generation using an interpolating saturation prover. In C. R.
          Ramakrishnan and Jakob Rehof, editors, Tools and Algorithms for the Construction and Analysis
          of Systems, pages 413–427, Berlin, Heidelberg, 2008. Springer Berlin Heidelberg.
[McM18] Kenneth L. McMillan. Eager abstraction for symbolic model checking. In Hana Chockler and
          Georg Weissenbacher, editors, Computer Aided Verification, pages 191–208, Cham, 2018. Springer
          International Publishing.
[MG16]    David Monniaux and Laure Gonnord. Cell morphing: From array programs to array-free horn
          clauses. In SAS, volume 9837 of Lecture Notes in Computer Science, pages 361–382. Springer,
          2016.
[MGJ+ 19] Haojun Ma, Aman Goel, Jean-Baptiste Jeannin, Manos Kapritsos, Baris Kasikci, and Karem A.
          Sakallah. I4: incremental inference of inductive invariants for verification of distributed protocols.
          In SOSP, pages 370–384. ACM, 2019.
[MI]      Makai Mann and Ahmed Irfan. Prophic3 prototype. URL: https://github.com/makaimann/
          prophic3/commit/497e2fbfb813bcf0a2c3bcb5b55ad47b2a678611.
[MIG+ 21] Makai Mann, Ahmed Irfan, Alberto Griggio, Oded Padon, and Clark W. Barrett. Counterexample-
          guided prophecy for model checking modulo the theory of arrays. In TACAS (1), volume 12651
          of Lecture Notes in Computer Science, pages 113–132. Springer, 2021.
[OG76]    Susan S. Owicki and David Gries. An axiomatic proof technique for parallel programs I. Acta
          Informatica, 6:319–340, 1976.
[PHM+ 21] Oded Padon, Jochen Hoenicke, Kenneth L. McMillan, Andreas Podelski, Mooly Sagiv, and
          Sharon Shoham. Temporal prophecy for proving temporal properties of infinite-state systems.
          Formal Methods in System Design, Jul 2021. doi:10.1007/s10703-021-00377-1.
[Pnu77]   Amir Pnueli. The temporal logic of programs. In FOCS, pages 46–57. IEEE Computer Society,
          1977.
[PS20]    Elizabeth Polgreen and Sanjit A. Seshia. Synrg: Syntax guided synthesis of invariants with
          alternating quantifiers. CoRR, abs/2007.10519, 2020.
[R2̈0a]   Philipp Rümmer. CHC COMP 2020. https://chc-comp.github.io/, 2020.
[R2̈0b]   Philipp Rümmer. Competition Report: CHC-COMP-20, 2020. URL: https://arxiv.org/abs/
          2008.02939.
[SSS00]   Mary Sheeran, Satnam Singh, and Gunnar Stålmarck. Checking safety properties using induction
          and a SAT-solver. In FMCAD, volume 1954 of Lecture Notes in Computer Science, pages 108–125.
          Springer, 2000.
[ZFF+ 12] Zipeng Zhang, Xinyu Feng, Ming Fu, Zhong Shao, and Yong Li. A structural approach to prophecy
          variables. In TAMC, volume 7287 of Lecture Notes in Computer Science, pages 61–71. Springer,
          2012.




                                              This work is licensed under the Creative Commons Attribution License. To view a copy of this
                                              license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                              Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse 2,
                                              10777 Berlin, Germany
