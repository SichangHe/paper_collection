             A Formally Verified IEEE 754
       Floating-Point Implementation of Interval
                  Iteration for MDPs

    Bram Kohlen1(B) , Maximilian Schäﬀeler2 , Mohammad Abdulaziz2,3 ,
                 Arnd Hartmanns1 , and Peter Lammich1
                  1
                   University of Twente, Enschede, The Netherlands
                                b.kohlen@utwente.nl
                 2
                   Technical University of Munich, Munich, Germany
                          maximilian.schaeffeler@tum.de
                       3
                          King’s College London, London, UK



       Abstract. We present an eﬃciently executable, formally veriﬁed imple-
       mentation of interval iteration for MDPs. Our correctness proofs span the
       entire development from the high-level abstract semantics of MDPs to a
       low-level implementation in LLVM that is based on ﬂoating-point arith-
       metic. We use the Isabelle/HOL proof assistant to verify convergence of
       our abstract deﬁnition of interval iteration and employ step-wise reﬁne-
       ment to derive an eﬃcient implementation in LLVM code. To that end,
       we extend the Isabelle Reﬁnement Framework with support for reasoning
       about ﬂoating-point arithmetic and directed rounding modes. We exper-
       imentally demonstrate that the veriﬁed implementation is competitive
       with state-of-the-art tools for MDPs, while providing formal guarantees
       on the correctness of the results.


1     Introduction
Probabilistic model checking (PMC) [4, 5] is a formal veriﬁcation technique for
randomized systems and algorithms like wireless communication protocols [36],
network-on-chip (NoC) architectures [51], and reliability and performance mod-
els [6]. Typical properties checked by means of PMC relate to reachability prob-
abilities: What is the probability that a ﬁle will eventually be transmitted suc-
cessfully [18]? Is the probability that a NoC router’s queue will overﬂow within c
clock cycles below 10−5 ? What is the maintenance strategy that minimizes ser-
vice outages within a given cost budget [52, 53]? The system models that PMC is
applied to are speciﬁed in higher-level modeling languages such as Modest [12, 24]
or JANI [15] with a formal semantics in terms of (extensions of) Markov chains
and Markov decision processes (MDPs) [11, 48].
    PMC delivers results with formal guarantees, typically that the computed
and (unknown) true probabilities diﬀer by at most a user-speciﬁed ε. PMC is
thus well-suited for the design and evaluation of safety- and performance-critical
systems. Over the past decade, however, we have witnessed several threats to
 c The Author(s) 2025
R. Piskac and Z. Rakamarić (Eds.): CAV 2025, LNCS 15932, pp. 122–146, 2025.
https://doi.org/10.1007/978-3-031-98679-6_6
         Formally Veriﬁed Floating-Point Implementation of Interval Iteration   123

the validity of PMC results. First and foremost, the most-used PMC algorithm,
value iteration (VI), was shown to be unsound with an absolute- or relative-error
stopping criterion, i.e. produce arbitrarily wrong results for certain inputs [22].
Standard VI terminates whenever two successive iterates are suﬃciently close
in value. However, at this point, the distance to the actual reachability prob-
ability may be arbitrarily oﬀ, no matter the error threshold [23, Example 1].
Several sound replacements for VI were subsequently developed [23, 30, 49], yet
their soundness proofs have so far been pen-and-paper style with room for human
error. For example, the pseudocode for the sound VI algorithm as stated in [49]
contains a subtle omission that only surfaces on 1 of the 78 models of the Quan-
titative Veriﬁcation Benchmark Set (QVBS) [31].
    This calls for formal specifications of the algorithms accompanied by
machine-checked correctness proofs. Even correct algorithms, however, may
be incorrectly implemented in today’s manually-coded PMC tools. As a case
in point, the implementation of the interval iteration algorithm for expected
rewards [8] in the mcsta model checker of the Modest Toolset [28] diverges
on some inputs. We thus need correct-by-construction implementations, too.
    VI-based algorithms are iterative numeric approximation schemes that need
to be implemented via machine-precision ﬂoating-point arithmetic to obtain
acceptable performance [16, 29]. This introduces approximation and rounding
errors that in turn may lead to incorrect Boolean outputs [61]. An eﬃcient solu-
tion is to carefully use the directed rounding modes provided by standard IEEE
754 ﬂoating-point implementations on modern CPUs [27], which, however, needs
careful reasoning about floating-point errors and rounding in all formal proofs
and correctness-preserving implementation strategies.

Our Contribution. We present a solution to all of the above challenges based on
the interval iteration (II) algorithm [23] for sound PMC on MDP models and the
interactive theorem prover (ITP) Isabelle/HOL [47] with its Isabelle Reﬁnement
Framework (IRF) [42]:
– We formalize (i.e. model) II in Isabelle/HOL’s logic and formally prove its
  correctness using Isabelle/HOL (Sect. 3), making II the ﬁrst sound PMC algo-
  rithm for MDPs with machine-checked correctness.
– We extend the IRF with support for ﬂoating-point arithmetic, including
  directed rounding modes (Sect. 4.2), introducing the ﬁrst ITP-based algo-
  rithm reﬁnement approach suitable for II and similar algorithms.
– Using the IRF, we reﬁne the formalization of II into eﬃcient LLVM bytecode
  (Sects. 4.3 and 4.4), delivering the ﬁrst correct-by-construction implementa-
  tion of a PMC algorithm.
– In Sect. 5, we embed the code into mcsta, a competitive probabilistic model
  checker. We experimentally evaluate the performance using the QVBS, show-
  ing that the veriﬁed implementation is eﬃcient. Our formal proofs and the
  benchmark setup are available online.1

1
    https://doi.org/10.4121/bf0fef24-4f0f-4de6-a58d-07b9ba601804.
124    B. Kohlen et al.

State-of-the-Art: Verification of Algorithms for MDPs. A probabilistic model
checker like mcsta performs preprocessing and transformation steps for both
correctness and performance. Previously, the strongly connected component [32]
and maximal end component decomposition [33] algorithms have been veriﬁed
down to LLVM, replacing their previous unveriﬁed implementations inside mcsta
by veriﬁed ones of comparable performance. These were fully discrete graph algo-
rithms, however, that neither required reasoning about numerical convergence
in their correctness proofs nor ﬂoating-point arithmetic in their reﬁnement to
an eﬃcient implementation. With this work, we contribute an essential piece for
the incremental replacement of unveriﬁed by veriﬁed algorithms for probabilistic
reachability in mcsta’s MDP model checking core.
    Other work relevant to our setting is the veriﬁcation of iteration algorithms
for MDPs: In Coq by Vajjha et al. [59] and in Isabelle/HOL by Schäﬀeler and
Abdulaziz [54, 55]. These works contribute formalizations of the classical version
of value iteration and policy iteration that optimize the expected discounted val-
ues, and a modiﬁed policy iteration algorithm for solving large, factored MDPs.
We note that only Schäﬀeler and Abdulaziz [54, 55] also veriﬁed practical imple-
mentations. However, since their implementations used inﬁnite-precision arith-
metic, they could not compete with state-of-the-art ﬂoating-point implementa-
tions. Thus, the work we present here is the ﬁrst, to our knowledge, where a full
formal mathematical analysis of an algorithm, involving heavy usage of a formal
mathematical probabilities library, is performed and a competitive ﬂoating-point
implementation is also veriﬁed. Furthermore, from a formalization-methodology
perspective, we note that the correctness argument of II involves a substantial
element of graph-theoretic reasoning, in addition to the reasoning about ﬁxed
points that is present in II and other veriﬁed MDP algorithms. This includes rea-
soning about connected components, acyclicity, and levels in a directed acyclic
graph (DAG), further complicating II’s veriﬁcation compared to other veriﬁed
iteration algorithms.

State-of-the-Art: Verification of Floating-Point Algorithms. It is widely recog-
nized as a problem that ﬂoating-point implementations often deviate from the
mathematical models of the underlying algorithms. Bugs with potentially seri-
ous consequences were noted in the hardware and aerospace industry [26, 46].
Due to the complexity of ﬂoating-point algorithms’ behavior, and the failure
of testing to reliably catch bugs in those algorithms, there is a long tradition
of applying formal methods to the veriﬁcation of ﬂoating-point algorithms. This
was done in veriﬁcation systems like Z [10], HOL Light [25, 26], PVS [14, 45], and
Coq [13, 20]. Most of that previous work, however, focused on proving correct-
ness of basic algorithms implemented in ﬂoating-point arithmetic, such as foun-
dational linear algebra operations [37]. In contrast, we aim to do the correctness
proofs on algorithms using real numbers, which we implement as ﬂoating-point
numbers with directed rounding. This keeps our correctness proofs manageable
while preserving interesting properties, even for complex programs.
    A related line of work aims to prove correctness by providing error bounds.
Tools like PRECiSA [58], VCFloat2 [3], FPTaylor [56], Real2Float [44], and
        Formally Veriﬁed Floating-Point Implementation of Interval Iteration        125

Fluctuat [21] analyze the ﬂoating-point error propagation. They focus on deter-
mining the worst-case roundoﬀ error. While more expressive than our approach,
these tools have limited to no support for programs with complex control ﬂow
like the nested loops in the implementation of II.
    The static analysis tool Astrée [17] is used in the aviation and automotive
industry to check the absence of runtime errors. While it supports ﬂoating-point
arithmetic, it cannot verify general correctness properties. Frama-C [38] has sim-
ilar functionality but also features deductive veriﬁcation. However, the properties
supported are limited to, e.g., proving that outputs lie in a given interval [40].
The situation is similar with other deductive veriﬁers such as KeY [2], which can
verify the absence of exceptional ﬂoating-point values like NaN and infinity [1].


2     Preliminaries

We now present the necessary background for the rest of the paper: we introduce
Isabelle and the Isabelle Reﬁnement Framework, followed by IEEE 754 ﬂoating-
point numbers and Markov decision processes in Isabelle/HOL.

2.1   Isabelle/HOL

An interactive theorem prover (ITP) is a program that implements a formal
mathematical system in which a user writes deﬁnitions and theorem statements,
and constructs proofs from a set of axioms. To prove a theorem in an ITP, the
user provides high-level steps, and the ITP ﬁlls in the details at the axiom-level.
    We perform our formalization using the ITP Isabelle/HOL [47], which is a
proof assistant for higher-order logic (HOL). Roughly speaking, HOL can be
seen as a combination of functional programming with logic. Isabelle is designed
to be highly trustworthy: a small, trusted kernel implements the inference rules
of the logic. Outside the kernel, a large set of tools implement proof automation
and high-level concepts like algebraic data types. Bugs in these tools cannot lead
to inconsistent theorems being proved, as the kernel refuses ﬂawed proofs.
    We aim to represent our formalization as faithfully as possible, but we have
optimized the presentation for readability. The notation in Isabelle/HOL is sim-
ilar to functional programming languages like ML or Haskell mixed with math-
ematical notation. Function application is written as juxtaposition: we write
f x1 . . . xn instead of the standard notation f (x1 , . . . , xn ). Recursive functions
are deﬁned using the fun keyword and pattern matching. For partial functions,
we use the notation f = (λx ∈ X. g x), to explicitly restrict the domain of the
function to X. Where required, we annotate types as x :: type.
    Isabelle/HOL provides a keyword locale to deﬁne a named context with
assumptions, e.g. an MDP with well-formedness assumptions [9]. Locales can
be interpreted and extended in diﬀerent contexts, e.g., a locale for MDPs can be
instantiated for a speciﬁc MDP, which yields all theorems from that locale.
126    B. Kohlen et al.

2.2   Isabelle Refinement Framework
Our veriﬁcation of II spans the mathematical foundations of MDPs, the imple-
mentation of optimized algorithms and data structures, and the low-level LLVM
intermediate language [43]. To keep the veriﬁcation eﬀort manageable, we use a
stepwise reﬁnement approach: starting with an abstract speciﬁcation, we incre-
mentally add implementation details, proving that each addition preserves cor-
rectness, e.g., computing a ﬁxed point by iteration, or implementing MDPs by a
sparse-matrix data structure. The former speciﬁes the control ﬂow of a program,
but the data type remains the same. The latter we call data refinement.
    This approach is supported by the Isabelle Reﬁnement Framework (IRF) [42].
In the IRF, we deﬁne algorithms in the nondeterministic result (nres) monad,
where a program either fails or produces a set of results. The notation a ≤R c
denotes that every (non-deterministic) output of abstract program a is related to
an output of concrete program c via the refinement relation R. In other words, c
is an implementation of a. If a reﬁnement step does not involve data reﬁnement,
then we use ≤ := ≤Rid where Rid is the identity relation.
    We target LLVM for our code generation, for which the IRF provides seman-
tics, so that we can perform reﬁnements to LLVM in a veriﬁed way. LLVM is an
intermediate representation, meaning that programming languages like C and
Rust can be compiled to LLVM. The LLVM compiler framework can then be
used to compile to bytecode and apply optimizations. In our formalization, the
reﬁnement chain starts with a high-level speciﬁcation of the algorithm and ends
with an eﬃcient LLVM program. The sepref [41] tool can automatically reﬁne
a program to LLVM and prove a reﬁnement theorem, given that we have pro-
vided compatible data structures (sepref can automatically reﬁne HOL lists to
arrays, nats to 64-bit integers, etc.). Due to transitivity of reﬁnement, the LLVM
program satisﬁes the speciﬁcation.

2.3   Floating-Point Arithmetic
Our work builds on a formalization of the IEEE 754 ﬂoating-point standard
in Isabelle/HOL [62]. This library provides a generic type (e,f) float resem-
bling scientiﬁc notation: e is the number of bits for the exponent, and f is
the number of bits for the fraction (also known as mantissa). We use the type
double = (11,52) float which is the standard double precision format.
    The ﬂoating-point format contains positive and negative numbers, as well
as designated special values for ±∞ and not a number (NaN). The function
valof :: (e,f) float → ereal maps non-NaN ﬂoating-point numbers to extended
real numbers, i.e. R ∪˙ {−∞, +∞}. Finally, the formalization provides standard
ﬂoating-point instructions like addition, multiplication, and comparisons as well
as intuitive predicates to identify special cases (e.g. is nan).

2.4   Markov Decision Processes
Markov decision processes (MDPs) are widely used to model probabilistic sys-
tems with nondeterministic choices [48], e.g., in PMC, planning, operations
       Formally Veriﬁed Floating-Point Implementation of Interval Iteration    127

research and reinforcement learning [7, 57]. Intuitively, an agent interacts with
an environment by choosing actions that, together with random elements, inﬂu-
ence the state of the system. The agent has an objective, e.g., to reach certain
states, and aims to choose actions that optimize the probability to achieve the
objective. The important concepts introduced in this section are illustrated in
Example 1.
    Formally, a ﬁnite MDP is a pair M = (S, K) where S is a ﬁnite, non-empty
set of states, and K : S → 2P(S) is the transition kernel. It maps every state to
a ﬁnite, non-empty set of actions in the form of transition probabilities. P(S)
denotes the set of probability measures on S, i.e. functions p : S → [0, 1] where
   s∈S p(s) = 1. Furthermore K is closed under S: Actions from S lead to S.
    Our formalization of II extends the Markov Models [34, 35] formalization from
archive of formal proofs (AFP)—a collection of Isabelle libraries. MDPs are mod-
eled with a generic type s mdpc and a locale Finite MDP that, in combination,
contain the states, the transition kernel and well-formedness conditions (Locale
2.1). In the following, we abbreviate the projections states M and actions M as
S and K. The type of the states is s, and the type of probability distributions
over s is s pmf. For a distribution p :: s pmf, set pmf p denotes its support, i.e.
the set of states with non-zero probability.
locale Finite MDP =                                           (Locale 2.1)
  fixes M :: s mdpc and S and K
  defines S = states M and K = actions M
  assumes S = ∅ and finite S and ∀s. K s = ∅ and ∀s ∈ S. finite (K s)
  assumes ∀s ∈ S. a ∈ K s. set pmf a ⊆ S
     At every state, the agent chooses an action
based on the current state and the history of
visited states. The agent’s choices are cap-
tured by a scheduler (aka policy, strategy,
or adversary), which is a function that maps
histories to actions. The MDP formalization
works with configurations, which are pairs of
states and strategies. A conﬁguration is valid
if the strategy selects only enabled actions and Fig. 1. A simple MDP with four
the state of the conﬁguration is in S. valid cfg states and ﬁve actions.
denotes the set of all valid conﬁgurations. Given a conﬁguration and an MDP,
the probability space of inﬁnite traces T cfg is constructed from the induced
Markov chain, where each state is a conﬁguration.
     MDP subcomponents play an important role in the analysis of II. A sub-
MDP M = (S , K ) consists of a subset of states S ⊆ S and a restricted kernel
K where ∀s ∈ S . K (s) ⊆ K(s). A sub-MDP is strongly connected if all states
are connected via a sequence of actions. A closed, strongly connected sub-MDP
is an end component (EC). A maximal end component (MEC) is an EC that is
not a sub-MDP of another EC. Finally, trivial MECs are MECs with one state
and no actions, and bottom MECs are MECs without an exit.
128     B. Kohlen et al.

Reachability. In our PMC setting, the objective is to minimize or maximize the
long-term reachability probabilities of a set of target states U ⊆ S. The value
function Pcfg :: s ⇒ real gives the probability of reaching U in the Markov chain
induced by the conﬁguration cfg. Minimal and maximal reachability probabilities
are denoted by Pinf and Psup respectively. Pinf is deﬁned as the inﬁmum of
Pcfg over all valid conﬁgurations, Psup is deﬁned using the supremum. We also
introduce the Bellman optimality operators Finf and Fsup (Deﬁnition 2.1, Fsup
omitted). For a state s ∈ S and a value vector v, Finf v s denotes the minimal
expected value of v after taking a single step from s. The symbol denotes the
inﬁmum.
definition Finf v = (λs ∈ S.                                              (Def. 2.1)
 if s ∈ U then 1
 else a ∈ K s. t ∈ set pmf a. v t · pmf a t)
    The least fixed point (lfp) of Finf is Pinf . In other words, repeatedly applying
Finf to a lower bound of Pinf converges to Pinf in the limit. For II, we preprocess
the MDP such that the greatest fixed point (gfp) of Finf also equals Pinf , and then
iterate Finf on both a lower and an upper bound until they closely approximate
Pinf . The same holds for Fsup and Psup .

Example 1. Figure 1 shows an MDP with four states, S = {0, 1, 2, 3}. The outgo-
ing transitions from each state represent the actions in the MDP. Each transition
leads to a black dot and branches into the successor states with corresponding
probabilities. For example in state 0, K 0 = {α, β}. The agent can choose action
α to move to state 2, or β to have a 10% chance to move to state 1.
    Let the target states U = {3}. The reachability probabilities are Pinf 2 = 0.5
and Psup 2 = 1. The MDP has a single bottom MEC {3} with action { }, and
a single trivial MEC {2}. The states {0, 1} form a MEC with actions β and γ.


3     Interval Iteration in Isabelle/HOL

The interval iteration (II) algorithm for MDPs is an iterative solution method
for reachability problems based on value iteration. In contrast to standard value
iteration applied to PMC, II provides a simple and sound stopping criterion.
    We present our Isabelle/HOL formalization of deﬁnitions and correctness
proofs for II and its preprocessing routines. Our formalization is based on the
proofs in [23]: We highlight the challenges encountered during formalization and
point out diﬀerences in our formal proofs to their pen-and-paper equivalents.
In particular, we present a more elegant and much more precise proof of [22,
Proposition 3]. Moreover, we simplify the deﬁnitions of the preprocessing steps
signiﬁcantly. In the following, all statements preﬁxed with lemma or theorem
are formally veriﬁed in Isabelle/HOL. All theorems and deﬁnitions for Psup that
are analogous to the ones for Pinf are omitted here for brevity.
        Formally Veriﬁed Floating-Point Implementation of Interval Iteration     129

3.1   The Interval Iteration Algorithm

The idea of the II algorithm is to start with a lower and an upper bound on
the true reachability probabilities and then iterate the Bellman optimality oper-
ator Finf (or Fsup ) on both. Since the optimality operators are monotone, both
sequences converge to a ﬁxed point. On arbitrary MDPs, these ﬁxed points are
not necessarily the same. However, if the MDP is preprocessed to only con-
tain MECs that are trivial or bottom MECs, both ﬁxed points are equal to the
optimal reachability probabilities.
    For now, assume an arbitrary MDP with a single target state s+ and an
avoid state s− , that are both sinks. As the initial lower bound lb0 , we take the
function that assigns 1 to s+ and 0 to all other states. The initial upper bound
ub0 assigns 0 to s− and 1 to all other states. The II algorithm computes the
sequences lbinf n and ubinf n, deﬁned as the n-fold application of Finf to either
lb0 or ub0 :
definition lbinf n = (Finf )n lb0 and ubinf n = (Finf )n ub0              (Def. 3.1)
It is an immediate consequence of the monotonicity of the Bellman optimality
operators that the lower (upper) bounds are monotonically increasing (decreas-
ing). Clearly, lb0 is a lower bound and ub0 is an upper bound of Pinf . Additionally,
we formally derive that the Bellman optimality operators preserve upper and
lower bounds in Lemma 3.1. These two properties of the abstract II algorithm
are required for the reﬁnement proof in Sect. 4.
lemma assumes v ≤ Pinf shows Finf v ≤ Pinf                             (Lemma 3.1)
lemma assumes v ≥ Pinf shows Finf v ≥ Pinf


3.2   Reduced MDPs

II is only guaranteed to converge if the MDP only contains trivial or bottom
MECs. We therefore need to preprocess the MDP before applying II. The pre-
processing steps diﬀer for Pinf and Psup , they are called min-reduction and
max-reduction. In a ﬁrst step, we extend the existing MDP formalization [34]
with strongly connected components (SCCs) and bottom MECs (Deﬁnition 3.2).
The states of an MDP that form trivial or bottom MECs are called trivials or
bottoms respectively. We follow the original presentation of II [23] and call an
MDP reduced if all of its MECs are either trivial or bottom MECs.
definition bmec M b =                                                     (Def. 3.2)
   mec M b ∧ (∀s ∈ states b. actions b s = K s)


Min-Reduction. The min-reduction for MDPs transforms an arbitrary MDP into
a reduced MDP whilst Pinf remains unchanged. Observe that we may assign a
minimal reachability of 0 to all non-trivial MECs (except s+ ): There exists a
strategy that stays in the MEC forever and therefore never reaches s+ . Hence,
all such MECs may be collapsed into a single absorbing state s− . To formalize
130      B. Kohlen et al.

this transformation, we ﬁrst deﬁne a function red inf (Deﬁnition 3.3) to map single
states, and then apply it to the MDP M to obtain the reduced MDP Minf (Deﬁ-
nition 3.4). Our formal deﬁnition is a substantial simpliﬁcation compared to the
pen-and-paper version [23, Def. 4].
    The function map mdpc (deﬁned by Hölzl [35]) applies a function to every
state of an MDP. If the function merges states, map mdpc merges the action sets.
Finally, fix loop s− replaces the actions at s− with a single self-loop. Figure 2
displays the min-reduced version of the MDP from Fig. 1.
definition red inf s = if s ∈ trivials M ∪ {s+ } then s else s−          (Def. 3.3)

definition Minf = fix loop s− (map mdpc red inf M)                       (Def. 3.4)




      Fig. 2. Min-reduced MDP derived         Fig. 3. Max-reduced MDP derived
      from the MDP in Fig. 1.                 from the MDP in Fig. 1.

    Our formal proof of the fact that Minf is in fact a reduced MDP follows the
original proof [22]. Next, we also need to show that the transformation preserves
Pinf . To distinguish the reachability probabilities of the original and the reduced
MDP, we use the notation Pinf for the original MDP and Minf .Pinf for the reduced
MDP. Our correctness proof of the transformation is based on the fact that min-
                                                         ≤
reduction preserves the ﬁnite-horizon probabilities Pinf    n (Lemma 3.2), i.e., the
reachability probability in n steps. Now, the main claim (Theorem 3.1, [23,
Proposition 3]) is a direct consequence. Note that our proof is simpler and more
precise than the original: Haddad and Monmege [23] only claim without details
that for every strategy in the reduced MDP, there exists a strategy in the original
MDP with the same Pinf and vice versa.
                            ≤                ≤
lemma assumes s ∈ S shows Pinf n s = Minf .Pinf n (red inf s) (Lemma 3.2)

theorem assumes s ∈ S shows Pinf s = Minf .Pinf (red inf s)             (Thm. 3.1)

Max-Reduction. The Psup case can be handled similarly with a max-reduction.
Yet the procedure is more involved, as not all non-trivial MECs can be collapsed
while preserving Psup —a maximizing strategy might choose to leave a non-trivial
MEC. We can, however, ﬁrst collapse each MEC into a single state to obtain
an MDP MMEC . This step keeps the reachability probabilities unchanged. In a
second step, we map the bottom MECs to s− . Finally, we remove self-loops at
all states except s+ and s− . Our formalization decomposes max-reduction [23,
Def. 5] into multiple steps, which in turn simpliﬁes both deﬁnitions and proofs.
       Formally Veriﬁed Floating-Point Implementation of Interval Iteration     131

    Collapsing the MECs into a single state is performed by the function the mec,
the transformation preserves Psup (Theorem 3.2). Our proof resembles the proof
of [19, Theorem 3.8], however we have to work around the fact that the MDP
formalization [34] only supports deterministic policies. Note that every state of
MMEC now forms its own MEC. The correctness proof of the second phase of
the reduction is similar to min-reduction. See Fig. 3 for the max-reduced version
of the MDP from Fig. 1.
theorem                                                                 (Thm. 3.2)
   assumes s ∈ S
   shows Psup s = MMEC .Psup (the mec M s)

Proof. (≤) As collapsing MECs only shortens paths in the MDP, the proof pro-
ceeds similarly to the one for min-reduction via ﬁnite-horizon probabilities.
   (≥) Consider an optimal strategy πMEC in MMEC , we need to show that
there exists a strategy in M with the same reachability probability. Every MEC
m of M contains a state sπm , where the action selected by πMEC is enabled.
Moreover, within a MEC, we can obtain a deterministic, memoryless strategy
πm that reaches this state with probability 1. Thus, we can construct a strategy
in M that behaves like πm within each MEC until sπm is reached and then follows
πMEC . The reachability probability of this strategy in M is the same as the one
achieved by πMEC in MMEC .

3.3   Reachability in Reduced MDPs

From now on, we assume that we are working with a reduced, ﬁnite MDP M,
where each state is either a trivial or a bottom MEC. We show that in such an
MDP, over time, any strategy reaches a bottom MEC almost surely. This is the
key property that will then allow us to prove the convergence of II.

Level Graph. First, we build a level graph of the MDP, starting at the bottom
MECs (Deﬁnition 3.5). At level n + 1, we add all those states where every action
has a successor on level n or below. We deﬁne I to be the greatest non-empty
level of the level graph G, so I is the number of steps that allows us to reach a
bottom MEC from every state. We formally show that G has the desired prop-
erties, i.e. it is acyclic and contains every state at exactly one level. The proofs
in Isabelle/HOL require substantial reasoning about graph-theoretic properties,
e.g., we need to show that every MDP contains a bottom MEC.
fun G where                                                              (Def. 3.5)
  G 0 = bottoms M
  G (n + 1) = let G≤n = i ≤ n. G i in
   {s ∈ S \ G≤n . ∀a ∈ K s. G≤n ∩ a = ∅}
132     B. Kohlen et al.

Reachability of BMECs. We now show that, intuitively, every strategy eventually
descends through the levels of G. The rate at which a bottom MEC is encoun-
tered is bounded in terms of η, the smallest probability of any transition in the
MDP. At every step, the probability of descending a level with respect to G is
at least η. Hence, we can show that for any valid conﬁguration, the probability
to reach the bottom MECs in I steps is no less than η I (Lemma 3.3).
                                           ≤
lemma assumes cfg ∈ valid cfg shows η I ≤ Pcfg I                       (Lemma 3.3)
                 ≤
    The value Pcfg  n denotes the ﬁnite-horizon reachability probability of the
bottom MECs in n steps under conﬁguration cfg. Note that the lemma was
originally stated for safety instead of reachability problems. We transform it
using the well-known equivalence P≤n                   ≤n
                                     cfg (♦U ) = 1 − Pcfg ( ¬U ). For n multiples
of I, we obtain the stronger lower bound 1 − (1 − η I )n (Theorem 3.3, [23,
                                                                      ≤
Proposition 1]). As n increases, (1 − η I )n converges to 0 and thus Pcfg nI tends
towards 1. Since we chose cfg arbitrarily, we almost surely reach a bottom MEC
in the limit.
                                                         ≤
theorem assumes cfg ∈ valid cfg shows 1 − (1 − η I )n ≤ Pcfg nI (Thm. 3.3)


3.4   Convergence of Interval Iteration

We assume a special form of reduced MDPs, where the only bottom MECs are
the target state s+ and avoid state s− , that are both absorbing (Locale 3.1).
The reduced MDPs from Sect. 3.2 are instances of this locale.
locale MDP Reach = Finite MDP M +                                       (Locale 3.1)
  assumes s− ∈ S and s+ ∈ S and
   ∀s ∈ S \ {s+ , s− }. s ∈ trivials M and
   K s− = {return pmf s− } and K s+ = {return pmf s+ }
   Towards a convergence proof of II, we show that the lower and upper bound
sequences are equal to the ﬁnite-horizon reachability probabilities towards s+ and
s− respectively (Lemma 3.4, [23, Lemma 4]). For improved clarity, we indicate
target sets explicitly in this section.
lemma                                                           (Lemma 3.4)
  assumes s ∈ S
                      ≤                                 ≤
  shows lbinf n s = Pinf {s+ } n s and ubinf n s = 1 − Psup {s− } n s
Combining the above result with Theorem 3.3, we can bound the distance
between the sequences (Theorem 3.4). Note that convergence is in general only
guaranteed if all computations are carried out with arbitrary precision arith-
metic. In a ﬂoating-point setting, the convergence to a unique ﬁxed point is not
guaranteed. Still, this theoretical result motivates the usage of the II algorithm to
optimally solve reachability problems on MDPs. In practice, on most instances
the algorithm converges much faster than the theoretical bound suggests (see
Sect. 5 for experimental results).
       Formally Veriﬁed Floating-Point Implementation of Interval Iteration     133

    Finally, the theorem does not apply if all probabilities in the MDP are equal
to 1, i.e. no branching occurs after action selection [23]. In this case, the MDP
is deterministic and is better solved with qualitative solution methods.
theorem                                                                  (Thm. 3.4)
 assumes s ∈ S and > 0 and η = 1 and n                      log(1−ηI )     I
 shows ubinf n s − lbinf n s ≤

Proof. As a ﬁrst step, we show for all i that
                                 ≤                ≤
ubinf iI s − lbinf iI s = 1 − Psup {s− } iI s − Pinf {s+ } iI s       (Lemma 3.4)
             ≤                 ≤                                         ≤      ≤
 ≤ 1 − (Pinf {s− } iI s + Pinf {s+ } iI s)                            (Pinf ≤ Psup )
            ≤
 = 1 − Pinf    {s− , s+ } iI s                                     (Disjoint events)
 ≤ (1 − η I )i .                                                         (Thm. 3.3)
Set i = log(1−ηI )   and the theorem follows from monotonicity.


4     Refinement Using Floating-Point Arithmetic

In the next step, we use the IRF to reﬁne II to an eﬃcient LLVM implemen-
tation, reﬁning real numbers to IEEE 754 double precision ﬂoating-point num-
bers (ﬂoats). While our framework can be used to reﬁne to ﬂoats of any precision,
we focus on the widely-adopted double precision variant here for smaller round-
ing errors than single-precision ﬂoats.
    To avoid complex reasoning about error bounds, we propose a safe rounding
approach that reﬁnes reals to upper bounding or lower bounding ﬂoats. As the
name suggests, upper bounding ﬂoats are always greater than or equal to the
real value they reﬁne, while lower bounding ﬂoats are always less than or equal.
    We ﬁrst introduce the sepref tool for reﬁnement to LLVM, after which we
present our extension of the IRF and sepref for ﬂoats. This new reasoning infras-
tructure for ﬂoating-point implementations serves as the framework to obtain
correct-by-construction LLVM code for II.

4.1   The Sepref Tool

We use sepref [41] to automatically reﬁne algorithms to LLVM programs. The
sepref tool provides a library of veriﬁed, reusable data structures. Since LLVM
maintains a heap, we need to be able to deal with memory allocation and dis-
posal. We use assertions from separation logic [50] which are reﬁnement relations
extended with a heap. Formally A :: a ⇒ c ⇒ h ⇒ bool where a and c is the
abstract and concrete data and h is the heap. The assertion holds if a:: a reﬁnes
c:: c and c is encoded in heap h:: h. sepref uses separation logic to ensure memory
correctness, e.g., correct disposal and preventing dangling pointers.
134      B. Kohlen et al.

Example 2. The following example demonstrates how to employ sepref for auto-
matic reﬁnements to LLVM code.
1     definition ls app x xs = xs @ [x] and half nat n = n div 2
2     definition app half n xs = do { let n = half nat n; return ls app n xs }
3     lemma (rshift1, half nat) :: Asize → Asize
4     lemma (arl app, ls app) :: [λn xs. length xs < 263 -1] Asize → Adarl → Aarl
5     lemma (arl app half, app half) :: [λn xs. length xs < 263 -1] Asize → Adarl → Aarl

    Line 1 deﬁnes ls app (insert an element at the end of a list) and half nat
(divide a natural number in half). Both are used in the deﬁnition of app half
in Line 2. The standard library of sepref has LLVM assertions for lists as array
lists (Aarl ), and natural numbers as 64-bit signed words (Asize ).
    Now, half nat can be reﬁned to the LLVM program rshift1, which performs
an eﬃcient right bit shift. sepref represents reﬁnements using parametric functor
notation as in Line 3. The lemma states that rshift1 and half nat are related as
follows: If the inputs of half nat (type nat) and rshift1 (type size) are related via
Asize , then the outputs are related via Asize .
    Line 4 provides a reﬁnement of the append operation following the same prin-
ciple, only now with two inputs. Moreover, the precondition length xs < 263 − 1
 limits the length of the input list xs. The reﬁnement relation only holds for suf-
ﬁciently small lists. Finally, the superscript d indicates that the input is destruc-
tively updated. With these two rules registered to sepref, we can automatically
reﬁne app half. We provide a signature to instruct sepref to use the desired data
structures:
                   [λn xs. length xs < 263 − 1] Asize → Adarl → Aarl .
sepref can now automatically synthesize the LLVM program arl app half based
on rshift1 and arl app. Moreover, it proves the reﬁnement relation in Line 5.

4.2     Floating-Point Extension of the Isabelle Refinement Framework

We extend the IRF with data reﬁnements to ﬂoats. While we can achieve this
with error-bound estimation, the existing frameworks are cumbersome to use.
Instead, we propose to reﬁne real numbers to lower bounding (lb) or upper
bounding (ub) ﬂoats by employing safe rounding techniques [27]. This allows us
to perform a correctness proof on an algorithm that uses real numbers, and in
a subsequent reﬁnement replace them with lb/ub ﬂoats, implemented through
AVX512 rounding modes. We eliminate the need to compute error-bounds a-
priori while still retaining the information relevant to proving the desired cor-
rectness properties.
    Since the ub case is mostly symmetric to the lb case, we focus on lb ﬂoats.
We aim to construct a reﬁnement relation that never produces NaN for the
operations we support. The main motivation here is that NaN is incomparable,
rendering it incompatible with a framework that reasons about bounds. Further-
more, the operations we support must preserve upper or lower bounds: the ﬂoat
       Formally Veriﬁed Floating-Point Implementation of Interval Iteration    135

−2f (the subscript f denotes ﬂoats) is a lower bound of 1, yet −2f × −2f = 4f
is not a lower bound of 1 × 1 = 1. To ensure this property, we restrict ourselves
to non-negative ﬂoats.
    We deﬁne Rlb = {(fl,r). valof fl ≤ r ∧ ¬is nan fl ∧ valof fl ≥ 0}, the reﬁne-
ment relation that relates reals to lb ﬂoats, e.g. (2f , 3) ∈ Rlb , but (−2f , −1)
Rlb , as −2f is negative. Floats are pure, e.g. they do not need to allocate memory
on the heap. This means that the assertion Alb is Rlb when provided an empty
heap.
    We now present a non-exhaustive set of operations supported by our frame-
work, where we focus on the operations required for our use-case.

Fused Multiply-Add. The ternary operator fma a b c = a × b + c (fused
multiply-add) yields a smaller ﬂoating-point rounding error compared to per-
forming the two operations separately. We name the AVX512 operation for fma
that rounds towards negative inﬁnity fma avx lb and prove the following reﬁne-
ment:
lemma (fma avx lb, fma) :: Alb → A>0
                                  lb → Alb → Alb                     (Lemma 4.1)
This lemma states that if the inputs are lb, not NaN and non-negative, the
output is also lb, not NaN and non-negative. Note that the result of 0f ∗ ∞f is
NaN. We resolve this with the stricter assertion A>0
                                                  lb that only allows positive
ﬁnite ﬂoats for the second argument. In the case of II, the second argument is
the transition probability of the MDP model, which is always positive.

Comparison. Comparing two lb ﬂoats does not provide any information about
comparing their real counterparts. We can preserve information partially by
implementing them as mixed operations, e.g., comparing lb to ub.
definition leq sound a b = spec (λr. r −→ a ≤ b)                     (Lemma 4.2)
lemma (leq double, leq sound) :: Alb → Alb → Abool
We use spec to introduce non-determinism as follows: the operation must return
False if the comparison returns False, but can return anything otherwise. For
illustration of the latter case, consider the following 2 cases when comparing
2 ≤ 5. Case 1: 4f is a ub of 2, and 3f is an lb of 5, we have 4f 3f ; Case 2: 3f is
a ub of 2, and 4f is an lb of 5, we have 3f ≤ 4f . So both outcomes are possible
after the reﬁnement.
    We use the comparison operation to implement the stopping criterion of II,
in which case this partial information is suﬃcient. For similar reasons, we also
implement subtraction as a mixed operator (omitted here).

Min and Max. It is possible to reﬁne the minimum (min) and maximum (max)
operations directly using comparisons. We deﬁne the following reﬁnement:
definition min double fl1 fl2 = if fl1 ≤ fl2 then fl1 else fl2       (Lemma 4.3)
lemma (min double, min) :: Alb → Alb → Alb
136    B. Kohlen et al.

    This reﬁnement holds despite the fact that a comparison does not reveal any-
thing about the bounding ﬂoat number. Consider the following case: 4f is a lower
bound of 5 and 3f is a lower bound of 6. Also, min double 4f 3f = 3f is a lower
bound of min 5 6 = 5, even though the ﬂoating-point implementation returns
the ﬁrst argument, while the deﬁnition on reals returns the second argument.
The reﬁnement works analogously for all combinations of lb/ub and min/max.

Constants. We provide trivial reﬁnements for the real number constants 0 and
1, which can be exactly represented as ﬂoating-point numbers.

4.3   Refinement of Interval Iteration

Using our ﬂoating-point extension to the IRF, we derive an implementation of
II using ﬂoats and directed rounding from the abstract speciﬁcation in Sect. 3.
The IRF allows us to reuse the correctness proofs of the abstract speciﬁcation,
and reason about the correctness of the implementation in isolation. Through
this separation of concerns we avoid directly proving the ﬂoating-point imple-
mentation correct.
    The plot in Fig. 4 shows a ﬁc-
tive run of II on both reals and their
reﬁnement to bounding ﬂoats. In the
long run, II on reals converges to
the dashed red line Pinf . The yellow
lines denote the valuations of an MDP
state using reals, lb starting from lb0
and ub from ub0 .
    Implementing lb with lower-bounding
ﬂoats (Alb ) yields the purple line
lbf (similarly for ub using upper- Fig. 4. The valuation of an MDP state
bounding ﬂoats). Note that the devi- over successive iterations: reals (yellow) vs.
ations are exaggerated on purpose in ﬂoats with safe rounding (purple). (Color
this example.                           ﬁgure online)
    Formally, the following speciﬁcation states soundness of II, i.e. the outputs
are lower and upper bounds of the actual reachability probabilities:
definition ii inf spec M =                                              (Def. 4.1)
   spec (λ(x, y). ∀s ∈ states M. x s ≤ Pinf M s ∧ Pinf M s ≤ y s)
   Convergence follows from Theorem 3.4, but we do not include this in our
correctness proof. With our framework, this statement would be void: The ﬂoat
implementations of x and y are further apart than x and y, which are less than
ε apart. As a ﬁrst step towards the reﬁnement to LLVM, we deﬁne II in the
nres-monad (the sup case is analogous):
       Formally Veriﬁed Floating-Point Implementation of Interval Iteration            137

 1 definition ii gs inf M L =                                                  (Def. 4.2)
 2    x ← lb0 M; y ← ub0 M; i ← 0; flag ← True;
 3    while (i++ < L ∧ flag) (
                    gs
 4       (x,y) ← Finf  Mxy
 5       flag ← spec(λx. True))
 6    return (x,y)
    We deﬁne ii gs inf in Line 1. It takes as inputs an MDP M, and a max-
imal iteration count L to guarantee termination. Line 2 initializes variables,
most importantly the lower bounds lb and upper bounds ub. The flag non-
deterministically decides whether to abort the loop. This is sound, because
ii inf spec is satisﬁed after any number of iterations. In each iteration, we ﬁrst
update the valuations according to a Gauss-Seidel variant of Finf (Line 4): We
update lb and ub in-place, thereby we use the updated values already in the
current iteration and converge faster.
    The algorithm is now in a format ready for reﬁnement proofs to LLVM. Using
the setup from Sect. 3 and Lemma 3.1, it is straightforward to prove that the
algorithm reﬁnes the speciﬁcation:
theorem ii gs inf M L ≤ ii inf spec M                                         (Thm. 4.1)


4.4   Refinement of the mcsta Data Structure

The motivation behind reﬁning II to LLVM code is to embed it into the model
checker mcsta from the Modest Toolset [28]. mcsta is an explicit-state proba-
bilistic model checker that also supports quantitative model checking of MDPs.
To avoid costly conversions of the MDP representation at runtime, we reﬁne
the mdpc data structure to the MDP data structure of mcsta. This is a two-step
process: First, we do a data reﬁnement from mdpc to the sparse-matrix represen-
tation used by mcsta based on HOL lists. Then, we use sepref to reﬁne this data
structure to LLVM. The sparse-matrix representation that we use is a 6-tuple:


      (St::nat list, Tr::nat list, Br::nat list, Pr::real list, ua ::nat, ut ::nat).

For each state, St contains an index to Tr, pointing to the ﬁrst transition (action)
of the state. Similarly, for each transition, Tr contains its ﬁrst index Br and Pr,
pointing to the ﬁrst branch of the transition and its probability. Finally, Br
contains the target of the branch, pointing to St. Additionally, ua and ut are the
avoid and target states respectively. Example 3 illustrates this data structure.

Example 3. A possible representation of the MDP from Fig. 1 is St = [0,2,3,4,5],
Tr = [0,1,3,4,6,7], Br = [2,0,1,0,1,3,3], Pr = [1.0,0.9,0.1,1,0.5,0.5,1.0]. The
index of the avoid and target state are stored in ua and ut . State 0 has two
actions: α and β (transitions 0 and 1). Transition 1 (action β) has two branches,
1 and 2, that lead to state 0 and 1 with probability 0.9 and 0.1 respectively.
138     B. Kohlen et al.

Refinement Relation. We relate the abstract MDP type mdpc to the concrete
data structure of mcsta with the reﬁnement relation RM (deﬁnition omitted).
For example, RM contains a tuple of the MDP of Fig. 1 and Example 3 as well as
with each other instance of the data structure in Sect. 4.4 along with the MDP
it represents. These lists present in the Isabelle/HOL model of the data structure
can be directly reﬁned to arrays of 64-bit integers (signed for compatibility with
mcsta). Through composition we obtain the assertion AM from abstract MDP
to LLVM.
                                                                                  gs
Refinement of Operations. We use sepref to reﬁne the functions lb0 , ub0 , Finf
and flag that are used by II. Reﬁning lb0 and ub0 to the concrete data structure
is straightforward: we initialize an array and set entries to constants 0f or 1f .
                                    gs                                    gs
The ﬂoating-point reﬁnement of Finf    builds on fma and min (max for Fsup   ) from
Sect. 4.2. Finally, we implement flag as follows: We compare the upper and lower
bound, and set the ﬂag if the diﬀerence is less than ε, speciﬁed by the user. Using
the above reﬁnements for all operations in ii gs inf, we use sepref to obtain an
LLVM algorithm ii gs inf llvm within Isabelle/HOL.

4.5    Correctness Statement
For the ﬁnal step in our proof, we combine all of our proofs into one theorem.
We use a Hoare triple format, as it allows us to present a concise correctness
statement of a program that is not cluttered by intermediary tools such as the
parametric functor notation. We show that our LLVM program ii gs inf llvm
satisﬁes the speciﬁcation ii inf spec (Deﬁnition 4.1, unfolded in Theorem 4.2).
The resulting triple transitively combines Theorem 4.1 with the reﬁnements from
Sect. 4.4:
 1    theorem llvm htriple                                    (Thm. 4.2)
 2     (Asize n ni  size L Li lb ε εf   M M Mi
 3          ↑(MDP Reach M ∧ n+1 < max size ∧ n = card (states M)))
 4     (ii gs inf llvm Li ni εf Mi )
 5     (λ(lbf ,ubf ). ∃lb ub. Aout
                               lb lb lbf Aout
                                          ub ub ubf
 6          ↑(∀s ∈ states M. lb s ≤ Pinf M s ∧ Pinf M s ≤ ub s)).
    Lines 2 and 3 specify the preconditions, where Line 2 concerns the input data:
n and L are natural numbers implemented as 64-bit words ni and Li ; ε is a real
number implemented as the ﬂoat εf and M is the MDP implemented as Mi . The
separation conjunction speciﬁes that these implementations do not overlap on
the heap. Line 3 is a boolean predicate lifted to separation logic using ↑. It states
that M satisﬁes locale MDP Reach (Locale 3.1) and limits the number of states
to the largest 64-bit number.
    If these preconditions hold, a run of the algorithm (Line 4) yields the arrays
lbf and ubf that satisfy the postconditions in Lines 5 and 6. These state that
lbf is a lower-bound implementation of lb, which is in turn a lower bound of Pinf
(similarly for ub). Note that the Hoare triple does not guarantee convergence
of lbf and ubf to a single ﬁxed point. However, our experiments show that our
implementation converges up to the limits of ﬂoating-point precision in practice.
       Formally Veriﬁed Floating-Point Implementation of Interval Iteration   139

5   Experimental Evaluation
The LLVM code generator of the IRF exports the LLVM program ii gs inf llvm
for use in the LLVM compiler pipeline. Additionally, it generates a C header
that facilitates embedding the program into other software, such as mcsta.

Integration with mcsta. We integrate our veriﬁed implementation with mcsta,
replacing the existing unveriﬁed interval iteration algorithm. This requires a
small amount of unveriﬁed glue code to convert the MDP’s probabilities into a
ﬂoating-point representation: mcsta stores the probabilities in the MDP as 128-
bit rationals (encoded as a pair of 64-bit integers representing the numerator
and denominator). Our MDP data structure Mi expects two ﬂoats per branch,
representing lower and upper bounds of the rational probability. We convert the
probabilities to 64-bit doubles by ﬁrst converting the numerator and denominator
to doubles and then performing two separate division operations, once rounding
up and once down. We assume that the input MDP as produced by the mcsta
pipeline is well-formed. If there were a bug in the parser that produces MDPs that
are not well-formed according to the precondition of the Hoare triple, we would
lose the formal guarantees. As long as parts of the toolchain remain unveriﬁed,
we rely on the correctness of the mcsta implementation for the preprocessing.

Evaluation Questions. We have formally veriﬁed in Isabelle/HOL that II with
precise arithmetic computes lower and upper bounds (lb and ub), and eventu-
ally converges to the reachability probability. However, two important questions
remain: First, veriﬁed implementations tend to be orders of magnitude slower
than unveriﬁed ones [54]. Since we veriﬁed an implementation with eﬃcient
numerics down to LLVM, we expect much faster runtimes. So how does our ver-
iﬁed implementation compare to state-of-the-art tools in terms of performance?
Second, the ﬂoating-point outputs (lbf and ubf ) provably provide conservative
bounds. Can we experimentally conﬁrm that the algorithm converges in practice?

Setup. For the ﬁrst question, we compare the runtime of our veriﬁed II imple-
mentation to its two unveriﬁed counterparts in mcsta: a C# implementation with
standard rounding (Modest implementation) and a C implementation with safe
rounding [27] (Safe implementation). The latter is similar to our veriﬁed LLVM
implementation, also using AVX512 instructions for safe rounding.
    We set the maximal iteration count to a high value (107 ) to ensure the compu-
tation is never terminated prematurely before convergence. While we anticipate
all benchmarks to converge within fewer iterations, this upper limit provides a
safeguard. We set the convergence threshold to ε = 10−6 . Once the lower and
upper bound diﬀer by less than ε, the Verified, Safe, and Modest implementa-
tions terminate. We use all DTMC, MDP and PTA models of the Quantitative
Veriﬁcation Benchmark Set (QVBS) [16] that contain 106 to 108 states and need
at least two iterations to converge to ε. For our benchmarks, we consider both
minimal and maximal reachability probabilities. In total, this yields a benchmark
set of 49 benchmark instances. We execute all benchmarks on an Intel i9-11900K
(3.5–5.3 GHz) system with 128 GB of RAM running Ubuntu Linux 22.04.
140     B. Kohlen et al.




      Fig. 5. Comparison of elapsed runtime for completing Interval Iteration



Results. Figure 5 compares the runtimes of the three implementations. Each
point x, y in a plot indicates that, on one benchmark instance, the implemen-
tation on the horizontal axis took x seconds while the Verified implementation
took y seconds. We note that none of our benchmark instances reached the time-
out of 10 min. We provide the runtimes for the II algorithm only. Other steps
are performed equally by mcsta such as state space exploration or min/max-
reduction.
    We see that the Verified implementation matches the unveriﬁed ones in terms
of performance. Thus, as far as this benchmark set can show, the answer to the
ﬁrst question is that we have achieved comparable performance to a state-of-the-
art unveriﬁed tool with a fully veriﬁed implementation. We also observed that
the Verified implementation does not reach the maximal iteration count on any
instance, i.e. it always converged up to ε, indicating that the second question
can also be answered aﬃrmatively.
    Additionally, we did not ﬁnd any signiﬁcant discrepancies in the raw data
output. The number of iterations to convergence is equal for all instances except
for the Haddad-Monmege model [23] between Verified and Modest. The excep-
tion is not surprising, as this model is designed to converge very slowly, increasing
the inﬂuence of ﬂoating-point errors. We also compared the computed results.
Due to using diﬀerent rounding modes, the results of Verified and Modest show
diﬀerences well within ε. Despite the fact that Verified and Safe both imple-
ment safe rounding, their outputs still diﬀer by minimal amounts on the order
of 10−20 . This may be caused by ﬂoating-point operations being non-associative,
so a diﬀerent order of operations may yield diﬀerent outputs.
    In terms of memory consumption, Verified and Safe use almost the same
amount of RAM, but use on average 20% more RAM than Modest. Since the
memory consumption is very similar for Verified and Safe, we suspect that these
diﬀerences come from garbage collection eﬀects caused by Verified and Safe
       Formally Veriﬁed Floating-Point Implementation of Interval Iteration     141

being native code called from within a tool otherwise running in the managed
C# runtime, as opposed to the purely-C# Modest implementation.


6   Discussion

We provide a framework to verify ﬂoating-point LLVM programs which exploits
the parametricity principle [60] of the IRF by consistently applying directed
rounding to ﬂoating-point values. Our approach eliminates complex reasoning
about error bounds to prove useful correctness properties of the implementation.
We are conﬁdent that our framework may be applied to other iterative algorithms
that compute lower and upper bounds. The latter is strictly necessary, as—with
our approach—we do not a-priori know the size of the error. However, if both
bounds converge to a single value, the ﬂoating-point error is guaranteed to be
smaller than the distance between the bounds. Thus we can determine an a-
posteriori error-bound.
    We applied our extension to the IRF to the formal veriﬁcation of the interval
iteration algorithm in Isabelle/HOL—all the way to a correct implementation.
Our developments formally prove that the algorithm computes lower and upper
bounds for the reachability probabilities (soundness) and converges to a single
ﬁxed point (completeness) when using real numbers. Furthermore, we show that
soundness is preserved if we implement the algorithm using ﬂoating-point arith-
metic with safe rounding. Our proofs culminate in a single statement, presented
as a Hoare triple, leaving no gaps in the link between the speciﬁcation and the
implementation in LLVM.
    Finally, we extract veriﬁed LLVM code from our formalization and embed
it in the mcsta model checker of the Modest toolset. We experimentally verify
that our implementation converges in practice and is competitive with manually
implemented, optimized, and unveriﬁed counterparts. This is an important step
towards a fully veriﬁed probabilistic model checking pipeline.
    We also present our approach as an alternative to the bottom-up approach of
building a veriﬁed model checker from scratch. With our top-down approach, the
full functionality of the model checker is available to the user, possibly in cross-
usage with veriﬁed components. Veriﬁed components are integrated with the
model checker incrementally as drop-in replacements for unveriﬁed components,
designed with competitive performance in mind.
    In a next step, we plan to complete the veriﬁed II backend for mcsta, the
missing part being an eﬃcient veriﬁed implementation of the transformations to
reduced MDPs. For this purpose, we aim to build on recent advancements that
provide a veriﬁed and eﬃciently executable MEC decomposition algorithm in
Isabelle/HOL [33].

Verification vs. Certification for II. An alternative to verifying II is to verify a
certifier that, given the result from an unveriﬁed implementation of II plus a
compact certificate, can eﬃciently check that the result is indeed correct. The
advantage of certiﬁcation is that the unveriﬁed implementation of II can be
142     B. Kohlen et al.

improved in an agile way independent of the certiﬁer. Also, since the certiﬁer is
(presumably) simpler than II, it should be easier to verify, including the veriﬁ-
cation of a high-performance implementation. One possible certiﬁcation scheme
for II is using the Park induction check of the optimistic value iteration algo-
rithm [30], i.e. performing one iteration of II and checking if the lower/upper
bound does not decrease/increase for any state. This could conﬁrm that some
ﬁxed point lies between the bounds computed by II. This certiﬁcation scheme
would require as input (1) the ﬁnal lower and upper bound for all states, (2) the
full MDP, and (3) a certificate that the MDP is reduced. Without the latter, one
can not be sure that the certiﬁed ﬁxed point corresponds to the reachability
probability, i.e. that it is the least ﬁxed point. One challenge with this scheme is
that, unlike our veriﬁed implementation of II, it cannot guarantee that all ﬁxed
points lie between the bounds. Also, since the entire reduced MDP is input to the
certiﬁcate checker, the certiﬁcate checking performance might be fundamentally
limited.

Data Availability Statement. Proofs and benchmarks presented in this paper are
archived and available at DOI 10.4121/bf0fef24-4f0f-4de6-a58d-07b9ba601804 [39].
Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.


References
 1. Abbasi, R., Schiﬄ, J., Darulova, E., Ulbrich, M., Ahrendt, W.: Deductive veriﬁ-
    cation of ﬂoating-point java programs in KeY. In: Tools and Algorithms for the
    Construction and Analysis of Systems - 27th International Conference, TACAS
    2021, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2021, Luxembourg City, Luxembourg, March 27 - April 1,
    2021, Proceedings, Part II. pp. 242–261 (2021). https://doi.org/10.1007/978-3-
    030-72013-1_13
 2. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H., Ulbrich, M. (eds.):
    Deductive Software Veriﬁcation - the KeY Book - from Theory to Practice (2016)
 3. Appel, A.W., Kellison, A.: Vcﬂoat2: Floating-point error analysis in Coq. In: CPP.
    pp. 14–29. ACM (2024)
 4. Baier, C.: Probabilistic Model Checking. In: Dependable Software Systems Engi-
    neering, pp. 1–23. IOS Press (2016). https://doi.org/10.3233/978-1-61499-627-9-
    1
 5. Baier, C., de Alfaro, L., Forejt, V., Kwiatkowska, M.: Model Checking probabilistic
    systems. In: Handbook of Model Checking, pp. 963–999. Springer (2018). https://
    doi.org/10.1007/978-3-319-10575-8_28
 6. Baier, C., Haverkort, B.R., Hermanns, H., Katoen, J.P.: Performance evaluation
    and Model Checking join forces. Commun. ACM 9, 76–85 (2010). https://doi.org/
    10.1145/1810891.1810912
 7. Baier, C., Katoen, J.P.: Principles of Model Checking. MIT Press (2008)
 8. Baier, C., Klein, J., Leuschner, L., Parker, D., Wunderlich, S.: Ensuring the relia-
    bility of your model checker: Interval iteration for Markov Decision Processes. In:
    29th International Conference on Computer Aided Veriﬁcation (CAV). pp. 160–180
    (2017). https://doi.org/10.1007/978-3-319-63387-9_8
        Formally Veriﬁed Floating-Point Implementation of Interval Iteration        143

 9. Ballarin, C.: Locales and locale expressions in Isabelle/Isar. In: TYPES. pp. 34–50
    (2003)
10. Barrett, G.: Formal methods applied to a ﬂoating-point number system. IEEE
    Trans. Software Eng. 5, 611–621 (1989). https://doi.org/10.1109/32.24710
11. Bellman, R.: A Markovian decision process. Journal of Mathematics and Mechanics
    5, 679–684 (1957)
12. Bohnenkamp, H.C., D’Argenio, P.R., Hermanns, H., Katoen, J.P.: MoDeST: A
    compositional modeling formalism for hard and softly timed systems. IEEE Trans.
    Software Eng. 10, 812–830 (2006). https://doi.org/10.1109/TSE.2006.104
13. Boldo, S., Melquiond, G.: Flocq: A uniﬁed library for proving ﬂoating-point algo-
    rithms in Coq. In: 2011 IEEE 20th Symposium on Computer Arithmetic. pp. 243–
    252 (2011). https://doi.org/10.1109/ARITH.2011.40
14. Boldo, S., Munoz, C.: A high-level formalization of ﬂoating-point number in PVS.
    Tech. rep. (2006)
15. Budde, C.E., Dehnert, C., Hahn, E.M., Hartmanns, A., Junges, S., Turrini, A.:
    JANI: Quantitative model and tool interaction. In: 23rd International Conference
    on Tools and Algorithms for the Construction and Analysis of Systems (TACAS).
    pp. 151–168 (2017). https://doi.org/10.1007/978-3-662-54580-5_9
16. Budde, C.E., Hartmanns, A., Klauck, M., Kretínský, J., Parker, D., Quatmann, T.,
    Turrini, A., Zhang, Z.: On correctness, precision, and performance in quantitative
    veriﬁcation (QComp 2020 competition report). In: 9th International Symposium on
    Leveraging Applications of Formal Methods (ISoLA). pp. 216–241 (2020). https://
    doi.org/10.1007/978-3-030-83723-5_15
17. Cousot, P., Cousot, R., Feret, J., Mauborgne, L., Miné, A., Monniaux, D., Rival, X.:
    The ASTREÉ analyzer. In: Programming Languages and Systems, 14th European
    Symposium on Programming, ESOP 2005, Held as Part of the Joint European
    Conferences on Theory and Practice of Software, ETAPS 2005, Edinburgh, UK,
    April 4-8, 2005, Proceedings. pp. 21–30 (2005). https://doi.org/10.1007/978-3-540-
    31987-0_3
18. D’Argenio, P.R., Jeannet, B., Jensen, H.E., Larsen, K.G.: Reachability analysis of
    probabilistic systems by successive reﬁnements. In: Joint International Workshop
    on Process Algebra and Probabilistic Methods, Performance Modeling and Ver-
    iﬁcation (PAPM-PROBMIV). pp. 39–56 (2001). https://doi.org/10.1007/3-540-
    44804-7_3
19. de Alfaro, L.: Formal veriﬁcation of probabilistic systems. Ph.D. thesis, Stanford
    University, USA (1997)
20. De Dinechin, F., Lauter, C., Melquiond, G.: Certifying the ﬂoating-point implemen-
    tation of an elementary function using Gappa. IEEE Trans. Comput. 2, 242–253
    (2010). https://doi.org/10.1109/TC.2010.128
21. Goubault, E., Putot, S.: Static analysis of ﬁnite precision computations. In: Ver-
    iﬁcation, Model Checking, and Abstract Interpretation - 12th International Con-
    ference, VMCAI 2011, Austin, TX, USA, January 23-25, 2011. Proceedings. pp.
    232–247 (2011). https://doi.org/10.1007/978-3-642-18275-4_17
22. Haddad, S., Monmege, B.: Reachability in MDPs: Reﬁning convergence of Value
    Iteration. In: 8th International Workshop on Reachability Problems (RP). pp. 125–
    137 (2014). https://doi.org/10.1007/978-3-319-11439-2_10
23. Haddad, S., Monmege, B.: Interval Iteration algorithm for MDPs and IMDPs.
    Theoretical Computer Science pp. 111–131 (2018). https://doi.org/10.1016/J.TCS.
    2016.12.003
144     B. Kohlen et al.

24. Hahn, E.M., Hartmanns, A., Hermanns, H., Katoen, J.P.: A compositional mod-
    elling and analysis framework for stochastic hybrid systems. Formal Methods Syst.
    Des. 2, 191–232 (2013). https://doi.org/10.1007/S10703-012-0167-Z
25. Harrison, J.: Formal veriﬁcation at Intel. In: 18th Annual IEEE Symposium of
    Logic in Computer Science, 2003. pp. 45–54 (2003). https://doi.org/10.1109/LICS.
    2003.1210044
26. Harrison, J.: A machine-checked theory of ﬂoating point arithmetic. In: Theorem
    Proving in Higher Order Logics. pp. 113–130 (1999). https://doi.org/10.1007/3-
    540-48256-3_9
27. Hartmanns, A.: Correct probabilistic Model Checking with ﬂoating-point arith-
    metic. In: TACAS (2). pp. 41–59 (2022). https://doi.org/10.1007/978-3-030-99527-
    0_3
28. Hartmanns, A., Hermanns, H.: The Modest Toolset: An integrated environment
    for quantitative modelling and veriﬁcation. In: 20th International Conference on
    Tools and Algorithms for the Construction and Analysis of Systems (TACAS). pp.
    593–598 (2014). https://doi.org/10.1007/978-3-642-54862-8_51
29. Hartmanns, A., Junges, S., Quatmann, T., Weininger, M.: A practitioner’s guide to
    MDP Model Checking algorithms. In: 29th International Conference on Tools and
    Algorithms for the Construction and Analysis of Systems (TACAS). pp. 469–488
    (2023). https://doi.org/10.1007/978-3-031-30823-9_24
30. Hartmanns, A., Kaminski, B.L.: Optimistic Value Iteration. In: 32nd International
    Conference on Computer Aided Veriﬁcation (CAV). pp. 488–511 (2020). https://
    doi.org/10.1007/978-3-030-53291-8_26
31. Hartmanns, A., Klauck, M., Parker, D., Quatmann, T., Ruijters, E.: The Quanti-
    tative Veriﬁcation Benchmark Set. In: 25th International Conference on Tools and
    Algorithms for the Construction and Analysis of Systems (TACAS). pp. 344–350
    (2019). https://doi.org/10.1007/978-3-030-17462-0_20
32. Hartmanns, A., Kohlen, B., Lammich, P.: Fast veriﬁed SCCs for probabilistic
    Model Checking. In: ATVA (1). pp. 181–202 (2023). https://doi.org/10.1007/978-
    3-031-45329-8_9
33. Hartmanns, A., Kohlen, B., Lammich, P.: Eﬃcient formally veriﬁed Maximal End
    Component decomposition for MDPs. In: FM (1). pp. 206–225 (2024). https://doi.
    org/10.1007/978-981-99-8664-4
34. Hölzl, J.: Markov Chains and Markov Decision Processes in Isabelle/HOL. J.
    Autom. Reason. 3, 345–387 (2017). https://doi.org/10.1007/S10817-016-9401-5
35. Hölzl, J., Nipkow, T.: Markov models. Arch, Formal Proofs (2012)
36. Kamali, M., Katoen, J.P.: Probabilistic Model Checking of AODV. In: 17th Inter-
    national Conference on the Quantitative Evaluation of Systems (QEST). pp. 54–73
    (2020). https://doi.org/10.1007/978-3-030-59854-9_6
37. Kellison, A.E., Appel, A.W., Tekriwal, M., Bindel, D.: LAProof: A library of formal
    proofs of accuracy and correctness for linear algebra programs. In: ARITH. pp. 36–
    43. IEEE (2023)
38. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-
    C: A software analysis perspective. Formal Aspects Comput. 3, 573–609 (2015).
    https://doi.org/10.1007/S00165-014-0326-7
39. Kohlen, B., Schäﬀeler, M., Abdulaziz, M., Hartmanns, A., Lammich, P.: Artifact
    for the paper “A Formally Veriﬁed IEEE 754 Floating-Point Implementation of
    Interval Iteration for MDPs”. 4TU.ResearchData (2025). https://doi.org/10.4121/
    bf0fef24-4f0f-4de6-a58d-07b9ba601804
40. Kosmatov, N., Prevosto, V., Signoles, J.: Guide to software veriﬁcation with Frama-
    C. Springer (2024)
        Formally Veriﬁed Floating-Point Implementation of Interval Iteration        145

41. Lammich, P.: Generating veriﬁed LLVM from Isabelle/HOL. In: 10th International
    Conference on Interactive Theorem Proving (ITP). pp. 22:1–22:19 (2019). https://
    doi.org/10.4230/LIPICS.ITP.2019.22
42. Lammich, P., Tuerk, T.: Applying data reﬁnement for monadic programs to
    Hopcroft’s algorithm. In: 3rd International Conference on Interactive Theorem
    Proving (ITP). pp. 166–182 (2012). https://doi.org/10.1007/978-3-642-32347-
    8_12
43. Lattner, C., Adve, V.: LLVM: A compilation framework for lifelong program anal-
    ysis and transformation. In: CGO. pp. 75–88 (2004)
44. Magron, V., Constantinides, G.A., Donaldson, A.F.: Certiﬁed roundoﬀ error
    bounds using Semideﬁnite Programming. ACM Trans. Math. Softw. (4), 34:1–
    34:31 (2017). https://doi.org/10.1145/3015465
45. Miner, P.S.: Deﬁning the IEEE-854 ﬂoating-point standard in PVS. Tech. rep.
    (1995)
46. Moscato, M., Titolo, L., Dutle, A., Muñoz, C.A.: Automatic estimation of veriﬁed
    ﬂoating-point round-oﬀ errors via Static Analysis. In: Computer Safety, Reliability,
    and Security. pp. 213–229 (2017). https://doi.org/10.1007/978-3-319-66266-4_14
47. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL – a proof assistant for Higher-
    Order Logic. Springer (2002)
48. Puterman, M.L.: Markov Decision Processes: Discrete stochastic Dynamic Pro-
    gramming. Wiley (1994). https://doi.org/10.1002/9780470316887
49. Quatmann, T., Katoen, J.P.: Sound Value Iteration. In: 30th International Con-
    ference on Computer Aided Veriﬁcation (CAV). pp. 643–661 (2018). https://doi.
    org/10.1007/978-3-319-96145-3_37
50. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    17th IEEE Symposium on Logic in Computer Science (LICS 2002), 22-25 July
    2002, Copenhagen, Denmark, Proceedings. pp. 55–74 (2002). https://doi.org/10.
    1109/LICS.2002.1029817 <error l="305" c="Invalid <error l="303" c="Invalid
    command: paragraph not started." /> command: paragraph not started." />
    <error l="305" c="Invalid
    command: paragraph not started." />
51. Roberts, R., Lewis, B., Hartmanns, A., Basu, P., Roy, S., Chakraborty, K., Zhang,
    Z.: Probabilistic veriﬁcation for reliability of a two-by-two network-on-chip sys-
    tem. In: 26th International Conference on Formal Methods for Industrial Critical
    Systems (FMICS). pp. 232–248 (2021). https://doi.org/10.1007/978-3-030-85248-
    1_16
52. Ruijters, E., Guck, D., Drolenga, P., Peters, M., Stoelinga, M.: Maintenance analy-
    sis and optimization via statistical Model Checking – evaluating a train pneumatic
    compressor. In: 13th International Conference on the Quantitative Evaluation of
    Systems (QEST). pp. 331–347 (2016). https://doi.org/10.1007/978-3-319-43425-
    4_22
53. Ruijters, E., Guck, D., van Noort, M., Stoelinga, M.: Reliability-centered main-
    tenance of the electrically insulated railway joint via fault tree analysis: A prac-
    tical experience report. In: 46th Annual IEEE/IFIP International Conference on
    Dependable Systems and Networks (DSN). pp. 662–669 (2016). https://doi.org/
    10.1109/DSN.2016.67
54. Schäﬀeler, M., Abdulaziz, M.: Formally veriﬁed solution methods for inﬁnite-
    horizon Markov Decision Processes. In: The 37th AAAI Conference on Artiﬁcial
    Intelligence (AAAI) (2023). https://doi.org/10.1609/aaai.v37i12.26759
55. Schäﬀeler, M., Abdulaziz, M.: Formally veriﬁed Approximate Policy Iteration. In:
    The 38th AAAI Conference on Artiﬁcial Intelligence (AAAI) (2025)
146     B. Kohlen et al.

56. Solovyev, A., Baranowski, M.S., Briggs, I., Jacobsen, C., Rakamaric, Z., Gopalakr-
    ishnan, G.: Rigorous estimation of ﬂoating-point round-oﬀ errors with symbolic
    Taylor expansions. ACM Trans. Program. Lang. Syst. (1), 2:1–2:39 (2019). https://
    doi.org/10.1145/3230733
57. Sutton, R.S., Barto, A.G.: Reinforcement Learning – an introduction. MIT Press
    (1998)
58. Titolo, L., Moscato, M., Feliu, M.A., Masci, P., Muñoz, C.A.: Rigorous Floating-
    Point Round-Oﬀ Error Analysis in PRECiSA 4.0. In: Formal Methods. pp. 20–38
    (2025). https://doi.org/10.1007/978-3-031-71177-0_2
59. Vajjha, K., Shinnar, A., Trager, B.M., Pestun, V., Fulton, N.: CertRL: Formalizing
    convergence proofs for value and policy iteration in Coq. In: The 10th International
    Conference on Certiﬁed Programs and Proofs (CPP). pp. 18–31 (2021). https://
    doi.org/10.1145/3437992.3439927
60. Wadler, P.: Theorems for free! In: Proceedings of the Fourth International Confer-
    ence on Functional Programming Languages and Computer Architecture, FPCA
    1989, London, UK, September 11-13, 1989. pp. 347–359 (1989). https://doi.org/
    10.1145/99370.99404
61. Wimmer, R., Kortus, A., Herbstritt, M., Becker, B.: Probabilistic Model Checking
    and reliability of results. In: 11th IEEE Workshop on Design & Diagnostics of
    Electronic Circuits & Systems (DDECS). pp. 207–212 (2008). https://doi.org/10.
    1109/DDECS.2008.4538787
62. Yu, L.: A formal model of IEEE ﬂoating point arithmetic. Arch, Formal Proofs
    (2013)




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
