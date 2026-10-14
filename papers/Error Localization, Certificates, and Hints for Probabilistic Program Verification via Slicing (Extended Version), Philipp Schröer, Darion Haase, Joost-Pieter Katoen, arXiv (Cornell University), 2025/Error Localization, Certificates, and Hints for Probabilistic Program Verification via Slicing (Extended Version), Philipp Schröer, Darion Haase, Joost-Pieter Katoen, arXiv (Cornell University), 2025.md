                                             Error Localization, Certificates, and Hints for
                                             Probabilistic Program Verification via Slicing
                                                          (Extended Version)

                                         Philipp Schröer1 [0000-0002-4329-530X] , Darion Haase1 [0000-0001-5664-6773] ,
                                                       and Joost-Pieter Katoen1 [0000-0002-6143-1926]
arXiv:2512.20214v2 [cs.PL] 24 Dec 2025




                                                                RWTH Aachen University, Germany
                                                        {phisch, darion.haase, katoen}@cs.rwth-aachen.de



                                                Abstract. This paper focuses on effective user diagnostics generated
                                                during the deductive verification of probabilistic programs. Our key prin-
                                                ciple is based on providing slices for (1) error reporting, (2) proof sim-
                                                plification, and (3) preserving successful verification results. By formally
                                                defining these different notions on HeyVL, an existing quantitative inter-
                                                mediate verification language (IVL), our concepts (and implementation)
                                                can be used to obtain diagnostics for a range of probabilistic program-
                                                ming languages. Slicing for error reporting is a novel notion of error
                                                localization for quantitative assertions. We demonstrate slicing-based di-
                                                agnostics on a variety of proof rules such as quantitative versions of
                                                the specification statement and invariant-based loop rules, and formally
                                                prove the correctness of specialized error messages and verification hints.
                                                We implemented our user diagnostics into the deductive verifier Caesar.
                                                Our novel implementation — called Brutus — can search for slices which
                                                do or do not verify, corresponding to each of the three diagnostic notions.
                                                For error reporting (1), it exploits a binary search-based algorithm that
                                                minimizes error-witnessing slices. To solve for slices that verify (2 and 3),
                                                we empirically compare different algorithms based on unsatisfiable cores,
                                                minimal unsatisfiable subset enumeration, and a direct SMT encoding of
                                                the slicing problem. Our empirical evaluation of Brutus on existing and
                                                new benchmarks shows that we can find slices that are both small and
                                                informative.


                                         1     Introduction

                                         1.1   Verification of Probabilistic Programs

                                         Probabilistic Programs. Probabilistic programs are programs that contain ran-
                                         dom assignments and may contain conditioning. They have been used to reason
                                         about randomized algorithms or models of real-world systems that deal with
                                         uncertainty. Recently, probabilistic programs have gained popularity in the con-
                                         text of machine learning as a way to formally reason about the behavior of AI
                                         models [12, 51, 13].
2       P. Schröer et al.

Deductive Verification. Typically, probabilistic programs are analyzed using ad-
vanced simulation techniques such as Markov Chain Monte Carlo [5]. This pro-
vides only statistical guarantees and has certain limitations, e.g., possible non-
termination of the simulation method for programs with an infinite expected
runtime. To obtain hard guarantees, formal verification of probabilistic programs
has received quite some attention [40, 37, 15, 14, 30]. This paper considers deduc-
tive verification of discrete probabilistic programs based on weakest precondition
reasoning à la Dijkstra. The program is associated with a specification, consisting
of (quantitative) pre- and postconditions, with the verification task to establish
that the program fulfills the specification.
     As an example, Figure 1 shows a              1 let s0choice = flip 0.5 in
Dice [23] program P representing a net-           2 if s0choice then true else
work packet delivery problem, adapted             3 let drop = flip 0.0005 in
from [20, Fig. 12]. The goal is to analyze        4      ¬drop
the delivery reliability of a packet sent      Goal    Pr(result  = true) ≥ 99%
from host s0 to s3 in a network with dia-
                                               Fig. 1: Dice program P modelling the
mond topology. Host s0 uses probabilistic
                                               packet delivery reliability problem.
load balancing to forward the packet to
s1 or s2 with equal probability, modeled through a fair coin flip for s0choice
in P . Host s1 has a perfectly reliable channel to s3 , while the channel from s2
to s3 has a probability of 0.05% to drop the message. In P , a biased coin is
flipped to determine whether the message gets dropped, if it is transmitted over
s2 . Finally, the program returns whether the transmission to the destination s3
is successful. The objective for verification: checking that the probability of a
successful transmission is at least 99%.

Automation. Reasoning about probabilistic programs is challenging because of
possible undesirable behaviors that only occur with low (or even zero) probabil-
ities. Classical program verification would falsely reject probability zero failures,
while many analyses of probabilistic programs often allow a certain leeway, e.g.
by allowing errors with probability zero. In addition to verifying that a program
has the correct output in expectation, properties such as expected runtimes, ex-
pected energy consumption, or expected privacy leakage can be of interest too. A
shift to quantitative verification approaches can account for these properties. In-
stead of using Boolean-valued conditions, the specification is expressed through
quantitative expectations.
    To formally reason about probabilistic programs, we use a quantitative in-
termediate verification language (IVL) named HeyVL, the basis of the deductive
verifier Caesar [49]. An IVL allows to decouple the verification process from dif-
ferent possible input languages, and is a common approach in classical deductive
program verification, as done by e.g. Dafny with Boogie [32, 33], or Prusti with
Viper [6, 43]. HeyVL is expressive enough to encode a wide range of probabilistic
programs and their properties. It features quantitative verification statements
that generalize classical ones, i.e. assume and assert statements, to represent
quantitative properties. In addition, an extendable catalogue of proof rules en-
ables different ways to reason about loops.
                           Diagnostics for Probabilistic Program Verification      3

    HeyVL’s semantics is based on weakest pre-expectation transformers, i.e. ba-
sically non-negative real (or ∞)-valued random variables [38, 28]. The intuition
is that assume statements introduce proof obligations on the expected value of
expressions provided in assert statements. Verification queries about lower and
upper bounds result in a verification condition, typically an inequality between
expectations, that needs to be proven.
    For verification with Caesar, the program is 1 assume 0.99
first encoded into HeyVL. The identified pre- and 2 s0choice :≈ flip(0.5)
post-expectation are added with initial assume, 3 if (⊓) {
resp. final assert statements. The program is fur-
                                                        4     assume ?(s0choice)
ther annotated with information on the proof rules
used to reason about, e.g., invariants for loops.       5     delivered := true
    The encoding of the network delivery problem        6   } else  {
from Figure 1 is given in Figure 2. The auxiliary 7           assume ?(¬s0choice)
variable delivered represents the output value of 8           drop :≈ flip(0.0005)
P . The specification is encoded as a verification 9          delivered := ¬drop
condition, highlighted in red. It states that the 10 }
probability of the final value of delivered meets
                                                       11 assert [delivered]
the lower bound of 99%. Iverson brackets [· · ·] are
used to map a Boolean result to the real values 0
                                                       Fig. 2: HeyVL encoding of
or 1. The if-then-else statement is encoded us-
                                                       the verification query for P
ing a demonic choice if (⊓) and two assumptions,
                                                       from Figure 1.
highlighted in blue. Boolean values are embedded
with ?(· · ·) to 0 or ∞, with the effect that the assume-statements effectively dis-
card any proof obligations on the expected value of the branch if the condition
is false, and keeping it unaffected otherwise.

1.2   Focus of this Paper
Deductive program verification is an iterative process where the user writes and
refines (1) the specification, (2) the proof and proof rules, or (3) even the program
under consideration. Understanding the behavior of probabilistic programs often
requires intricate reasoning about the probabilities of different events and even
simple programs can require mathematical reasoning about series, exponentials,
or limits. Ideally, the verification process is guided by feedback from the verifier
to assist with this complexity.
    While existing tools provide automated ways to confirm that a proof is cor-
rect, there is a lack of assistance during the verification phase. For instance,
Caesar translates the generated verification condition into an SMT-formula that
is discharged to an SMT solver. In case the query fails, the solver only provides
limited information by a counterexample, which corresponds to an initial state.
In the presence of quantitative control flow, it is unclear how this information
can result in insightful diagnostic feedback to the user.
    This paper is focused on aiding users in the verification of probabilistic pro-
grams through appropriate diagnostic messages. More specifically, we tackle the
following three questions:
4       P. Schröer et al.

 1. Error Localization: If a program’s quantitative verification fails, how can we
    identify and localize errors to provide meaningful error messages?
 2. Verification Certificates: If a program’s verification succeeds, how can we
    reduce and simplify proofs to convince the user through understandable,
    small certificates?
 3. Hints: If a program’s verification succeeds, can we distill the program’s core
    that makes the specification true?
    Our central contribution is to (a) formally define appropriate concepts to
capture these issues, (b) develop algorithms to compute these diagnostics, and
(c) implement and experimentally validate these. The development of our frame-
work in a quantitative intermediate verification language enables us to apply our
techniques to a range of probabilistic programming languages, such as Dice [23]
(with loops [50]) or pGCL ([38]).

1.3   Approach
Slicing. Our approach is based on program slicing [54, 56]. Slicing refers to
methods that, through removal of statements, extract a subprogram from a pro-
gram while preserving certain properties of interest. We introduce three kinds of
slices: error-witnessing, verification-witnessing, and verification-preserving slices.
Depending on the presence or absence of statements in the slice, appropriate di-
agnostics can be deduced and presented to the user. Let us explain the different
types of slices and how they are used to produce useful diagnostics through a
series of examples.
                                                           1 {b0 := 0} [1/2] {b0 := 1}
Error Localization. Figure 3, including the                2 {b1 := 0} [1/2] {b1 := 1}
striked-out code, shows a program that sam-                3 r := b0 + 2 ∗ b1
ples a uniform two-bit integer r by flipping two       Goal   Pr(r ≥ 2) ̸≤ 1/3
fair coins b0 and b1. Our goal is to show an up-
per bound of 1/3 on the probability of r ≥ 2. Fig. 3: Uniform 2-bit integer
Obviously, this bound is too tight. Which parts sampling using two coins.
of the program cause the verification to fail? We observe that the two traces
sampling b0 = 0, b1 = 1 and b0 = 1, b1 = 1 result in r ≥ 2 and together have
probability 21 · 21 + 12 · 12 = 12 > 31 . Importantly, this counterexample makes no
use of the assignment b1 := 0.
    Leaving out this assignment (strike-out) results in an error-witnessing slice:
any error in the slice is also present in the original program. This allows to
localize the verification failure to a subprogram by isolating the statements that
introduce responsible proof obligations.

Verification Certificates. Reconsider the network packet delivery problem from
Figures 1 and 2, for which we want to successfully verify that the probabil-
ity to correctly receive a message is at least 99%. While we can consider the
combined distribution of the (two) paths to the target host via s1 and s2 , no-
tice that we can also check the probability bound independently for each path.
                           Diagnostics for Probabilistic Program Verification     5

 If we have a lower bound for every path, the fun send(s0choice : : bool) {
least of those bounds gives a lower bound on       if s0choice then true else
the combined probability, thus completing the      let drop = flip 0.0005 in
proof. This corresponds to replacing the prob-        ¬drop
abilistic choice between s1 and s2 by a non- }
deterministic choice. In the HeyVL-encoding
(Figure 2) this corresponds to the removal of Fig. 4: A Dice program rep-
the blue assume-statements (and the proba- resenting           the     verification-
bilistic assignment of s0choice).                witnessing  slice of Figure  2.
    The resulting program is a verification-witnessing slice: if the slice verifies,
then the original program verifies as well. These slices contain all the necessary
information to conclude that the original program can be verified. They can
be employed to simplify proofs and as verification certificates. For the present
example, the slice can be represented by making s0choice an input parame-
ter (Figure 4), as Dice [23] does not include nondeterminism.

Hints. Figure 5 is a buggy version of Al-          1 c := 0
gorithm R [52] to uniformly sample an el-          2 i := 1
ement c from a stream of size n via reser-         3 while if i ≤ n {
voir sampling. In the correct algorithm,           4      {c := i} [1/n] {skip}
the probabilistic choice in (l. 4) is weighted     5      i := i + 1
with 1/i instead of 1/n. Nevertheless, the         6 }
(correct) upper bound of 1/n for the prob- Goal Pr(c = X) ≤ 1/n for X ∈ N
ability of terminating with c = X can be
verified for all X ∈ N. In fact, the loop Fig. 5: Faulty reservoir sampling.
itself is not required to establish the spec-
ification. It can be replaced by a single loop iteration.
    The resulting program is an (amorphous) verification-preserving slice: if the
original program verifies, then the slice verifies as well. In general, we can use
such slices to give hints, such as suggesting a new program that still satisfies the
specification but is easier to grasp, more efficient, or alerting the programmer of
the fact that the specification does not adequately capture the intended behavior
of the program.

Implementation. Figure 6 shows a flowchart of how and when we obtain the
different kinds of slices. After encoding a probabilistic program and a speci-
fication into HeyVL, the resulting program is verified and sliced. If the pro-
gram does not verify, we slice to obtain an error-witnessing slice. We do this by
selecting assert-like statements to slice. If the program verifies, we can either
aim for verification-witnessing or verification-preserving slices. For verification-
witnessing slices, we select assume-like statements and search for a slice that
still verifies. For verification-preserving slices, we can select any statements and
search for a slice that still verifies. These steps ensure that we obtain meaning-
ful slices that do not vacuously satisfy the definitions, such as a verification-
witnessing slice of a program that does not verify in the first place.
6         P. Schröer et al.

     Probabilistic Program P in Dice, pGCL, . . .              Property/Specification φ

         HeyVL Program S = assume · · ·; encode(P ); assert · · ·


                                 Does S verify?                    yes
                       no                         yes
     Select assert-like stmts.       Select assume-like stmts.      Select any stmts.

               Slice                           Slice                       Slice

      Error-witnessing slice           Ver.-witnessing slice       Ver.-preserving slice

Fig. 6: Flowchart of the verification process leading to the various kinds of slices.


1.4      Contributions and Outline

In Section 2, we explain the necessary background for the syntax and semantics
of HeyVL, which supports reasoning about lower and upper bounds of expected
values of non-deterministic, probabilistic programs that include recursion and
loops. To summarize, the main contributions of this work are:

    – Section 3.1: Formal notion of error-witnessing slices for error localization and
      simple sufficient conditions for soundness (removal of assert-like statements).
    – Section 3.2: Formal notion of verification-witnessing slices for verification
      certificates and simple sufficient conditions for their soundness (removal of
      assume-like statements).
    – Section 3.3: Formal notion of verification-preserving slices for hints and pro-
      gram optimization.
    – Section 4: Theorems of correctness of error localization and hints based on
      slicing for specific proof rule encodings as case studies.
    – Section 5: The first implementation of specification-based slicing for proba-
      bilistic programs which supports all of the above notions of slicing, integrated
      into the Caesar verifier. All outputs of the slicing methods are integrated
      into its Visual Studio Code plugin and are visualized as error messages or
      warnings.
    – Section 5: We evaluate the implementation on a set of representative bench-
      marks and show that we can quickly obtain user diagnostics for interactive
      feedback during the verification process.

Finally, Section 6 surveys related work, putting existing notions into the context
of our kinds of slices. We refute claims in the literature that finding optimal slices
requires both forward and backward reasoning and show that our approach can
handle these cases. Proofs of all results can be found in Section A.
                                Diagnostics for Probabilistic Program Verification           7


Table 1: Operators on expectations. inf and sup are taken on R∞   ≥0 . X[x 7→ v]
denotes the expectation with the value for x replaced by v, i.e. X[x 7→ v] =
λσ. X(σ[x 7→ v]), with σ[x 7→ v](y) = v if x = y and σ[x 7→ v](y) = σ(y) else.
      Z            Z(σ)                           Z           Z(σ)
                                                              (
                                                               ∞, if b(σ) = true
      a            a(σ)                           ?(b)
                                                               0,  otherwise
      X ⊓Y         min { X(σ), Y (σ) }            X ⊔Y        max { X(σ), Y (σ) }
      J x : τ. X   inf { X(σ[x 7→ v]) | v ∈ τ }   Sx : τ. X   sup { X(σ[x 7→ v]) | v ∈ τ }
                   (                                          (
                     ∞,      if X(σ) ≤ Y (σ)                    0,     if X(σ) ≥ Y (σ)
      X→Y                                         X⇝Y
                     Y (σ), otherwise                           Y (σ), otherwise



2     HeyVL – A Quantitative Intermediate Verification
      Language
In this section, we briefly explain the syntax and semantics of HeyVL, an inter-
mediate language to encode quantitative verification problems. HeyVL is based
on HeyLo, a syntax for expectation-based reasoning. HeyLo is used as HeyVL’s
assertion language, and is used to define HeyVL’s formal semantics. A more de-
tailed exposition of both can be found in [49].

2.1       Expectation-Based Reasoning
Reasoning about probabilistic programs generalizes Boolean to expectation-based
reasoning [38], i.e. about quantities such as expected values assigned to every
program state. In the following, we introduce the basic notions of logical reason-
ing about expectations.

Variables and Program States. Given a countably infinite set of typed vari-
ables Vars = {x, y, . . .}, we denote by x : τ that x has type τ . Typical types
are Booleans B = {true, false}, integers Z, or extended unsigned reals R∞  ≥0 =
R≥0 ∪ {∞}. A program state σ maps every variable x : τ to a value σ(x) ∈ τ .

Expectations. Generalizing logical predicates, expectations map program states
to values in R∞≥0 . Expectations form a complete lattice (E, ⪯) with X ∈ E for
all X : States → R∞ ≥0 and where X ⪯ Y iff for all σ ∈ States: X(σ) ≤ Y (σ).
Table 1 shows the syntax for expectations Z and their semantics [49, Section 2].

Basic expectations. We use r to represent the expectation λσ. r for some r ∈ R∞≥0 .
For arithmetic expressions a of type R∞  ≥0 , we  simply write a to mean λσ. a(σ),
e.g. 2 · x + 5 represents the expectation λσ. 2 · σ(x) + 5. The embedding operator
?(·) embeds a Boolean expression b into expectations: ?(b)(σ) maps to ∞ if b
evaluates to true in σ and to 0 otherwise. The minimum and maximum between
two expectations is denoted by the symbols ⊓ and ⊔, respectively.
8        P. Schröer et al.

Quantifiers. The infimum quantifier J and the supremum quantifier S are the
quantitative analogues of the universal ∀ and the existential ∃ quantifier from
predicate logic. Intuitively, the J quantifier minimizes a quantity, just like the
∀ quantifier minimizes a predicate’s truth value. Further, we can embed ∀ as
follows: (J x : τ. ?(b))(σ) = ∞ if and only if σ |= ∀x : τ. b. Dually, S maximizes
a quantity, and we have (Sx : τ. ?(b))(σ) = ∞ if and only if σ |= ∃x : τ. b.

Implications and Coimplications. The implication → generalizes the Boolean
implication to expectations. For a state σ, the implication X → Y evaluates to
∞ if X(σ) ≤ Y (σ), and to Y (σ) otherwise. Its dual coimplication ⇝ generalizes
the converse nonimplication, defined for propositions P and Q as ¬(P ← Q).
On expectations, X ⇝ Y evaluates to 0 if X(σ) ≥ Y (σ), and to Y (σ) otherwise.
    The implications have two important applications. The implication X → Y
can be used to encode a comparison, as X → Y = ∞ iff X ⪯ Y . They can also
simplify proof obligations: The inequality X ⪯ (Y → Z) can be transformed
into the equivalent (X ⊓ Y ) ⪯ Z by the adjointness property.1 This tells us that
introducing assumptions can only make the proof obligations simpler. The coim-
plication satisfies the dual properties and is used for upper bounds reasoning.

Validations. In the verification of probabilistic programs, one often needs to
“cast” quantities X into a quality. For every state σ, the validation △(X) eval-
uates to △(X) (σ) = ∞ if and only if X(σ) = ∞. Otherwise, △(X) (σ) = 0.
Thus, it “pulls down” every value different from the maximal value ∞. The cov-
alidation ▽(X) is dual and “pulls up” every value that differs from the minimal
value 0. Turning quantitative implications into qualitative comparisons is now
△(X → Y ), and we have △(X → Y ) (σ) = ∞ iff X(σ) ≤ Y (σ). The dual is
▽(X ⇝ Y ), which evaluates to 0 iff X(σ) ≥ Y (σ).


2.2    The Intermediate Verification Language HeyVL

HeyLo expressions denote quantitative properties about probabilistic programs.
The intermediate verification language HeyVL encodes quantitative verification
problems for probabilistic programs. It extends standard (probabilistic) con-
structs such as assignments, probabilistic sampling, and sequencing with quan-
titative verification statements that are used to transform and approximate the
expected values. With these verification statements, HeyVL generalizes classical
(Boolean) IVLs such as Boogie [33].

Syntax of Statements. The syntax of HeyVL statements S is given in the first
and third columns in Table 2. Here, x ∈ Vars is a variable of type τ , a is an
arithmetic expression, X and Y are expectation expressions, and µ is a distri-
bution expression of type τ representing a finite-support probability distribu-
tion. Let µ = p1 · ⟨t1 ⟩ + . . . + pn · ⟨tn ⟩ denote a probability distribution with
1
    With this implication, expectations form a Heyting algebra. The name “HeyLo”
    stands for a logic over Heyting algebras.
                              Diagnostics for Probabilistic Program Verification           9


Table 2: Syntax and semantics of HeyVL statements. Here µ = p1 · ⟨t1 ⟩ + . . . + pn ·
⟨tn ⟩ and X[x 7→ ti ] is the formula obtained from substituting every occurrence
of x in X by ti in a capture-avoiding manner.
S                vpJSK(X)                        S                vpJSK(X)

                 p1 · X[x 7→ t1 ]                reward a         X +a
var x : τ :≈ µ                                                                         
                    + . . . + pn · X[x 7→ tn ]   S1 ; S2          vpJS1 K vpJS2 K(X)
if (⊓) { S1 }                                    if (⊔) { S1 }
                 vpJS1 K(X) ⊓ vpJS2 K(X)                          vpJS1 K(X) ⊔ vpJS2 K(X)
 else { S2 }                                      else { S2 }
assert Y         Y ⊓X                            coassert Y       Y ⊔X
assume Y         Y →X                            coassume Y       Y ⇝X
havoc x          J x. X                          cohavoc x        Sx. X
validate         △(X)                            covalidate       ▽(X)



probability expressions p1 , . . . , pn for each value t1 , . . . , tn , respectively. We use
flip(p) to denote a Bernoulli distribution with probability expression p, i.e.
flip(p) = p · ⟨true⟩ + (1 − p) · ⟨false⟩. Let us briefly explain each statement. The
probabilistic assignment var x : τ :≈ µ assigns to the variable x of type τ a value
sampled from the distribution µ. When x is already declared, we just write x :≈ µ
for probabilistic assignments and x := v for deterministic assignments (with the
Dirac distribution µ = δv = 1 · ⟨v⟩). The statement reward a adds a reward
of a to the expected value of X. It can be used to model time progression or a
more general resource consumption of the program. The statement S1 ; S2 repre-
sents a sequence of programs S1 and S2 . The statement if (⊓) {S1 } else {S2 }
is a demonic nondeterministic choice between S1 and S2 . Nondeterminism is
resolved by minimizing the expected value. The statement assert Y quantita-
tively generalizes assertions from classical IVLs. Similarly, assume Y generalizes
assumptions. The havoc x statement forgets the current value of x and intro-
duces a minimizing nondeterministic branching for every possible value of x. The
validate statement introduces a quantitative validation.
    A distinguishing feature of HeyVL compared to IVLs for non-probabilistic
programs is that its verification-related statements have dual versions. There
is a dual maximizing (aka: angelic) nondeterministic choice if (⊔), as well as
coassert, coassume, cohavoc, and covalidate statements. Whereas the non-
co statements are used to reason about lower bounds (“the expected value is at
least some value”), the co statements allow reasoning about upper bounds (“the
expected value is at most some value”).

Semantics of Statements. The semantics of HeyVL is based on weakest pre-
expectation-style reasoning [38, 28]. The verification pre-expectation transformer
vpJSK : E → E transforms an expectation X by going backwards through the
10      P. Schröer et al.

statement S. We define vp by induction on S in Table 2. Given a state σ, the
result vpJSK(X)(σ) can be intuitively understood as the expected value of X on
termination of S when starting in σ.
    Let X be an expectation. We call it the post(-expectation). The expectation
vpJSK(X) is the verification pre-expectation with respect to post X. For a ran-
dom assignment S = var x : τ :≈ µ, vpJSK(X) is the weighted sum p1 · X[x 7→
t1 ]+. . .+pn ·X[x 7→ tn ], corresponding to the expected value of X after assigning
x sampled from µ. A statement reward a increases the post X by a, therefore
vpJreward aK(X) = X + a. For S = if (⊓) {S1 } else {S2 }, vpJSK(X) is the
minimum of vpJS1 K(X) and vpJS2 K(Y ). For if (⊔), we take the maximum.
    The semantics of S = assert Y generalizes the classical definition with
a Boolean conjunction. In our quantitative setting, vpJSK(X) = Y ⊓ X. This
corresponds to the least truth value between the post X and the assertion Y .
The statement S = assume Y introduces a quantitative implication: vpJSK(X) =
Y → X. Following the definition of →, introducing an assume statement lowers
the threshold at which an expected value is considered absolutely true. In a
state σ where Y (σ) ≤ X(σ), we have vpJassume Y K(X)(σ) = ∞. Otherwise, the
semantics is a no-op. The semantics of the statement havoc x generalizes the
classical ∀ semantics with an infimum: vpJhavoc xK(X) = J x. X. The validation
statement validate has semantics that translate the post into either 0 or ∞
using the △(·) operator, such that vpJvalidateK(X)(σ) = ∞ iff X(σ) = ∞.
    The dual statements have a dual semantics. The coassert statement gen-
erates the maximum of the post and the assertion instead of a minimum. For
coassume, we use the coimplication ⇝ so that vpJcoassume Y K(X)(σ) = 0 if
and only if Y (σ) ≥ X(σ) holds. Otherwise, the semantics is a no-op. For the
cohavoc statement, we get the supremum. Finally, covalidate has semantics
such that vpJcovalidateK(X)(σ) = 0 if and only if X(σ) = 0, and ∞ otherwise.

Specifications. We define a shorthand notation resembling Hoare triples for quan-
titative specifications. Because we reason both about lower and upper bounds,
we define two kinds of triples: |= ⟨X⟩⪯ S ⟨Y ⟩ if and only if X ⪯ vpJSK(Y ), and
dually |= ⟨X⟩⪰ S ⟨Y ⟩ if and only if X ⪰ vpJSK(Y ). We say a statement S veri-
fies if |= ⟨∞⟩⪯ S ⟨∞⟩. Dually, we say S co-verifies if |= ⟨0⟩⪰ S ⟨0⟩.

Conservativity. HeyVL is a conservative extension of Boolean IVLs. This means
that we can embed Boolean reasoning in HeyVL using the embedding operator
?(·) and obtain the same results as in the Boolean setting. For example, the
classical encoding of the conditional choice statement if (b) {S1 } else {S2 } can
be generalized: if (⊓) {assume ?(b); S1 } else {assume ?(¬b); S2 }. We will use
the former as shorthand for the encoding in the rest of this paper.

Monotonicity. The vp transformer is monotonic, which means that if the post
X is replaced by X ′ such that X ⪯ X ′ , then we retain the same inequality on
the vp semantics. This property is crucial for some of our soundness theorems.
Theorem 1 (Monotonicity of vp, [49, Thm. 3.2]). For all HeyVL state-
ments S and X, X ′ ∈ E, X ⪯ X ′ implies vpJSK(X) ⪯ vpJSK(X ′ ).
                            Diagnostics for Probabilistic Program Verification       11

3     Error Localization, Certificates, and Hints

We will now introduce the different kinds of slices of HeyVL programs that enable
the identification of error locations when verification fails (Section 3.1), the con-
struction of witnesses for the validity of a verifying program (Section 3.2), and
the tailoring of probabilistic programs to fulfil a given specification (Section 3.3).
For simplicity, we will focus this exposition on HeyVL programs encoding lower
bound verification tasks. Similar results can be stated for the dual case of upper
bound verification. Further, the slice notions defined for HeyVL programs can be
lifted to any (probabilistic) language encodable into HeyVL.


3.1    Error Localization

In nonprobabilistic systems, safety properties can be refuted by a single path
in the system. Providing counterexamples for specifications for probabilistic sys-
tems is inherently more complex. In the area of probabilistic model checking, the
extraction of counterexamples for Markov models has been extensively studied,
e.g. by [25, 1, 27]. There, counterexamples are sub-Markov chains which violate
the specification at hand. For probabilistic programs, a natural definition arises
from the negation of the verification task, i.e. a counterexample is a state where
the specification is violated.

Definition 2. A counterexample of HeyVL program S w.r.t. X, Y ∈ E is a state
σ ∈ States with X(σ) ̸≤ vpJSK(Y )(σ). We write σ ̸|= ⟨X⟩⪯ S ⟨Y ⟩.

    Inspired by [55, 19], we consider sub-programs as the counterpart of sub-
Markov chains at the program level. Here, we formalize this as a slicing problem.
Slicing aims to find a subprogram S ′ that preserves certain semantic properties,
in this case, that S ′ fails to satisfy the specification just like the original program
S did. S ′ witnesses the error.

Definition 3 (Error-witnessing slice). A subprogram S ′ of program S is an
error-witnessing slice w.r.t. X, Y ∈ E if

1. ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩, and
2. ∀σ ′ . (σ ′ ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩ =⇒ σ ′ ̸|= ⟨X⟩⪯ S ⟨Y ⟩).

   The first requirement ensures that the slice S ′ has at least one counterex-
ample state. The second requirement states that all counterexamples of S ′ are
counterexamples of S too.

Example 4. Consider the HeyVL program S in Figure 7 which flips a fair coin and
tries to establish that the probability of the result being non-negative and exactly
1 is at least 75%. We have vpJSK(∞) = 0.75 → (0.5·(1⊓0⊓∞)+0.5·(1⊓1⊓∞)) =
0.75 → 0.5 = 0.5 ̸= ∞. Therefore, the program fails to verify. In fact, the
set of counterexamples consists of all states. The subprogram S1′ obtained by
erasing (l. 3) (assert [x ≥ 0]) is an error-witnessing slice of S w.r.t. (∞, ∞),
12       P. Schröer et al.


     1   assume 0.75             1   assume 1                  1   assume 1/2
     2   x :≈ flip(0.5)          2   x := true                 2   assume [x ≥ 1]
     3   assert [x ≥ 0]          3   x :≈ flip(0.5)            3   assume [x ≤ 10]
     4   assert [x = 1]          4   assert [x]                4   y :≈ flip(0.5)
                                                               5   y := y + x
                                                               6   assert [y ≥ 2]
Fig. 7: HeyVL program        Fig. 8: HeyVL program
which does not verify.       which does not verify.
Removing (l. 3) results      Removing (l. 2) results       Fig. 9: HeyVL program
in an error-witnessing       in an error-witnessing        which verifies. Remov-
slice. However, remov-       slice, even though the        ing (l. 3) results in a
ing (l. 4) would result in   assignment is not reduc-      verification-witnessing
a verifying program.         tive.                         slice.



because any state is a valid counterexample: vpJS1′ K(∞) = 0.75 → 0.5 = 0.5 ̸=
∞. The subprogram S2′ obtained by erasing (l. 4) (assert [x = 1]) verifies, as
vpJS2′ K(∞) = 0.75 → 1 = ∞. Hence, it is not an error-witnessing slice. We
conclude that the requirement that x = 1 holds at the end of program S with
at least 75% probability is violated.

The example showed that removing assertions can help to turn a non-verifying
program into a verifying one. Conversely, adding assert-statements to a pro-
gram that fails to verify will not yield fewer counterexamples. Statements that
always strengthen proof obligations are called reductive.2

Definition 5. A statement S is reductive if vpJSK(X) ⪯ X for all X ∈ E.

Equivalently, one may use upper bound Hoare triples, saying that |= ⟨X⟩⪰ S ⟨X⟩
holds for all X ∈ E. Various verification statements in HeyVL are reductive, most
notably assert-statements. We will also call such statements assert-like.

Lemma 6. Statements assert, coassume, havoc, and validate are reductive.3

    From Lemma 6 and the monotonicity of vp, it follows that erasing reductive
statements in a program S ′ can never decrease the vp of program S in which S ′
is embedded. This suggests:

Theorem 7. Let S ′ be a subprogram obtained from program S by only erasing
reductive statements. If ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩, then S ′ is an error-witnessing slice of
S w.r.t. (X, Y ) for all X, Y ∈ E. In particular, we have vpJSK(X) ⪯ vpJS ′ K(X)
for all X ∈ E.
2
  This terminology is based on nomenclature for closure operator definitions [16, Sec-
  tion 11.7].
3
  These are all atomic HeyVL statements that are reductive in their general form.
  Specific instances of other statements, e.g. assume ∞, are also reductive.
                            Diagnostics for Probabilistic Program Verification     13

   The next example shows that error-witnessing slices can also result from
erasing non-reductive statements.
Example 8. Consider the HeyVL program S in Figure 8. It does not verify, as
the final assertion is required to always hold but is only fulfilled in 50% of the
runs. Let S ′ be obtained by removing (l. 2) (x := true). Even though x := true
is not reductive, e.g. vpJx := trueK(?(x)) = ?(true) = ∞ ̸⪯ ?(x), it holds that
vpJSK(∞) ⪯ vpJS ′ K(∞). As S ′ also fails to verify, S ′ is an error-witnessing slice
of S w.r.t. (∞, ∞).
    Removing assert-like statements allows pinpointing the error location: after
removal of the irrelevant assert-like statements, only the ones necessary for the
error remain. We do want to trace down a path leading to the error; e.g., if a cer-
tain branch of an if-else-statement results in an error, this can help to identify
the program’s problem. Observe that a demonic choice if (⊓) {S1 } else {S2 }
exhibits a property similar to the reductivity of assert-like statements: replacing
S1 (or S2 ) by the demonic choice between S1 and S2 introduces more constraints.
Lemma 9. For all S1 and S2 , the demonic choice S = if (⊓) {S1 } else {S2 }
fulfills: vpJSK(X) ⪯ vpJS1 K(X) and vpJSK(X) ⪯ vpJS2 K(X), for all X ∈ E.
Example 10. Consider Figure 3, which
uses upper bounds. We desugar the 1 coassume 1/3
conditional choices into explicit an- 2 c :≈ flip(0.5)
gelic choices.4 The result and error- 3 if (⊔) {coassume ?(¬c); b0 := 0}
witnessing slice are shown in Fig- 4 else {coassume ?(c); b0 := 1}
ure 10, applying the dual version 5 c :≈ flip(0.5)
of Lemma 9. In the error-witnessing 6 if (⊔) { coassume ?(¬c); b1 := 0}
slice, the angelic choice in (l. 5) is re- 7 else {coassume ?(c); b1 := 1}
placed by the second branch. Thus, 8 r := b0 + 2 ∗ b1
the resulting counterexample slice 9 coassert [r ≥ 2]
consists of both branches in (l. 3) and
the second branch of (l. 5). These cor-
                                           Fig. 10: Error-witnessing slice of the uni-
respond to the two traces that are
                                           form 2-bit integer sampling using two
needed to show the violation of the
                                           coins.
probability bound.

3.2    Certificates
Dual to finding a subprogram that witnesses an error, we consider the problem of
finding a subprogram that witnesses the validity of a verifying program. Instead
of identifying the source of an error, we are now interested in identifying the
parts of the program that are essential for the verification to succeed.
    Again, we phrase this as a slicing problem: We want to find a subprogram
S ′ whose verification guarantees that the program S verifies. In that sense, S ′
4
    As is standard in HeyVL, the Boolean embeddings inside the co-verification state-
    ments are negated (c.f. [49, Example 2.3]).
14       P. Schröer et al.

contains the necessary parts to witness the verification of S. Any parts that are
non-essential to the verification are erased.
Definition 11 (Verification-witnessing slice). A subprogram S ′ of a pro-
gram S is called a verification-witnessing slice w.r.t. X, Y ∈ E if

                    |= ⟨X⟩⪯ S ′ ⟨Y ⟩   implies   |= ⟨X⟩⪯ S ⟨Y ⟩ .

Subprograms that fail to verify trivially become verification-witnessing slices. As
these slices are not very helpful, we exclude them in the following.
Example 12. Consider the verifying HeyVL program S in Figure 9 and the sub-
program S ′ obtained by removing (l. 3) (assume [x ≤ 10]). Due to the assumption
[x ≥ 1], the final assertion holds in ≥ 50% of the states. Thus, S ′ is a verification-
witnessing slice of S, showing that [x ≤ 10] is unnecessary for ∞ ⪯ vpJSK(∞).
   As in the previous example, proof assumptions are commonly expressed
through assume-statements. Indeed, introducing additional assumptions can only
simplify the proof. Formally, these statements have a dual property to reductive-
ness, called extensiveness:
Definition 13. A statement S is extensive if vpJSK(X) ⪰ X for all X ∈ E.
    In terms of lower bound Hoare triples, one may require |= ⟨X⟩⪯ S ⟨X⟩ for all
X ∈ E. assume statements are extensive, and we will call extensive verification
statements assume-like.
Lemma 14. assume, coassert, cohavoc, covalidate, reward are extensive.
      We obtain the dual of Theorem 7:
Theorem 15. Let S ′ be a subprogram obtained from S by only removing exten-
sive statements. Then, S ′ is a verification-witnessing slice of S w.r.t. (X, Y ) for
all X, Y ∈ E. In particular, we have vpJSK(X) ⪰ vpJS ′ K(X) for all X ∈ E.

3.3     Hints
The verification-witnessing slices are based on the idea to obtain a slice which
relies on fewer assumptions. However, often the complications in a proof do not
lie in the too specific assumptions, but rather in the sequence of steps taken to
reach the conclusion. These steps usually correspond to intermediate statements
like assignments.
     This view motivates a third type of slicing, aimed at shrinking a program
while still being able to verify it. Intuitively, this can be seen as tailoring the
program to the specification. The result is a slice that only contains statements
required to preserve verification.
Definition 16 (Verification-preserving slice). A subprogram S ′ of a pro-
gram S is called a verification-preserving slice w.r.t. X, Y ∈ E if

                    |= ⟨X⟩⪯ S ⟨Y ⟩     implies   |= ⟨X⟩⪯ S ′ ⟨Y ⟩ .
                              Diagnostics for Probabilistic Program Verification     15


       1   {b0 := 0} [0.5] {b0 := 1}                1   c :≈ flip(0.5)
                                                    2   if (c) {b0 := 0} else {b0 := 1}
       2   {b1 := 0} [0.5] {b1 := 1}                3   c :≈ flip(0.5)
                                                    4   if (c) {b1 := 0} else {b1 := 1}
       3   r := b0 + 2 ∗ b1                         5   r := b0 + 2 ∗ b1
    Goal   Pr(r ≥ 2) ≥ 1/2                       Goal   Pr(r ≥ 2) ≥ 1/2

           (a) pGCL program.                              (b) HeyVL encoding.

Fig. 11: Uniform 2-bit integer sampling using two fair coin flips and its
verification-preserving slice w.r.t. (1/2, [r ≥ 2]).


    Such slices are known as specification-based slices. They were introduced
by [8] and subsequently extended to probabilistic programs by [44]. The contra-
position of being a verification-preserving slices reads: ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩ implies
̸|= ⟨X⟩⪯ S ⟨Y ⟩. This resembles our definition of error-witnessing slice as ex-
 pressed by the following lemma.

Lemma 17. For subprogram S ′ of program S: If S ′ is an error-witnessing slice
of S w.r.t. (X, Y ), then S ′ is a verification-preserving slice of S w.r.t. (X, Y ).

   In particular, it follows from Theorem 7 that slicing reductive statements
results in a verification-preserving slice. But as shown in the following example,
we can also slice sampling statements to obtain a verification-preserving slice.

Example 18. Figure 11 shows a program in the pGCL language and its HeyVL
encoding S, with corresponding slices. The original program in Figure 11a sam-
ples a two-bit integer by performing two coin flips, inspired by [44, Example 4.3].
It should generate an integer that is at least 2 with probability at least 50%.
Therefore, we fix pre X = 21 and post Y = [r ≥ 2]. A verification-preserving slice
of S can now be tailored to (X, Y ), e.g. by removing any sampling of the least
significant bit b0, yielding the slice in Figure 11b. Notice that S has no error-
witnessing slices w.r.t. (X, Y ), as such a slice would contradict |= ⟨X⟩⪯ S ⟨Y ⟩.


4   Slicing on Proof Rule Encodings

High-level language constructs are either encoded or reasoned about using proof
rules. For example, loops are typically analyzed using proof rules that provide
sufficient conditions for lower or upper bounds of the meaning of the loop. In
this section, we consider the HeyVL encodings to embed specifications, as well
as specification statements [41] that encode “placeholders” and can be used to
encode procedure calls.
    We will apply slicing to the HeyVL encodings of high-level program language
features to obtain diagnostic information. We demonstrate how a HeyVL slice
16        P. Schröer et al.

can be interpreted to obtain information about the original program, by apply-
ing slicing to different proof rules encoded in HeyVL. To indicate which part
of the proof rule has been violated when verification fails, our implementation
includes support for annotations on statements.5 We explain the diagnostics for
the verification of specifications, specification statements, and the Park induction
rule to reason about loops. nostics.

4.1     Verifying Specifications
A standard code verification approach [42] is to convert a triple of pre, program,
and post into one IVL program. This program is then checked against a fixed
pre and post pair (classically true and true) and is said to verify if this check
succeeds. A similar approach can be taken with quantitative pre and post in
HeyVL [49]. Let S be a HeyVL program and X, Y ∈ E. Then:

               |= ⟨X⟩⪯ S ⟨Y ⟩   iff   assume X; S; assert Y verifies.

A dual encoding works for upper bounds using the dual statements coassume
and coassert. We can now slice the specification itself by slicing the encoding
w.r.t. pre ∞ and post ∞, using that assert is reductive and assume is extensive:

Theorem 19. Let S = assume X; S ′ ; assert Y .
1. Removing the assert statement shows unverifiability with any post.
   If assume X; S ′ is an error-witnessing slice of S, then ̸|= ⟨X⟩⪯ S ′ ⟨Z⟩ for
   Z ∈ E.
2. Removing the assume statement shows verifiability with any pre.
   If S ′ ; assert Y is a verifying verification-witnessing slice of S, then |=
   ⟨Z⟩⪯ S ′ ⟨Y ⟩ for Z ∈ E.

    Both results indicate possible issues within the program or specification. An
always failing verification hints at contradicting requirements, while an always
successful verification might indicate that the program is ineffective in establish-
ing the post, which is possibly too weak.

4.2     Specification Statements
Specification statements [41] are useful during incremental development. They
are used as placeholders in a program, and explicitly state the requirements and
guarantees required from the parts that are omitted (program “holes”). Addi-
tionally, one can specify a collection of variables v which is allowed to change in
the “hole”. All other variables are assumed to remain unchanged.
    The specification statement v : [X, Y ] is a placeholder for all statements
which have pre of at least X(σ) when executed with post Y (σ) in state σ, i.e.,
5
     The user can write e.g. @error_msg(msg) assert X to add a custom error message
     to an assertion, or write @success_msg(msg) assume X to add a custom hint to an
     assumption, which are based on an erroring or verifying slice, respectively.
                               Diagnostics for Probabilistic Program Verification        17

it satisfies |= ⟨X⟩⪯ (v : [X, Y ]) ⟨Y ⟩. The specification statement v : [X, Y ] is
encoded in HeyVL as [49, Section 3.5]:

            v : [X, Y ] = assert X; havoc v; validate; assume Y .

The encoding closely mirrors the intuition of the classical specification statement:
we ensure (assert) that the pre X holds. Then, we abstract from the modifying
variables (with the havoc statement) and assume the post Y holds. In HeyVL,
we are not limited to predicates and can reason about expectations. The only
difference is that an additional validate statement is necessary for correctness.
Theorem 20. Let C = v : [X, Y ] and its HeyVL encoding be SC .

1. Pre does not entail specification’s pre. If S ′ is a minimal error-witnessing
   slice of SC w.r.t. (X ′ , Y ′ ) which contains assert X, then X ′ (σ ′ ) ̸≤ X(σ ′ )
   for some σ ′ .
2. Specification statement can be removed. If S ′ is a verification-witnessing
   slice of SC w.r.t. (X ′ , Y ′ ) which verifies and does not contain assume Y , then
   X ′ ⪯ Y ′ holds.

4.3     Park Induction for Loop Reasoning
Park induction is an effective proof rule in probabilistic program verification [47,
28]. It can be seen as a generalization of the classical Hoare logic proof rule for
loops: an invariant is inductive, if whenever it holds at the start of the loop, it
also holds at its end. For weakest liberal pre semantics (wlp)6 , the quantitative
version of Park induction for a loop while (b) {C} and invariant I for post Y
reads:

I ⪯ (?(b) → wlpJCK(I)) ⊓ (?(¬b) → Y )          implies    I ⪯ wlpJwhile (b) {C}K(Y ) .
|                {z                 }                     |          {z            }
          I is an inductive invariant                    I underapproximates the loop’s wlp

Thus, it can be used to establish lower bounds on the weakest liberal pre-
expectation of a loop. Dually, for weakest pre-expectation semantics it enables
establishing upper bounds. Again, we focus on lower bounds. Figure 12 shows
the encoding P ark(b, C, I) of the proof rule in HeyVL. Its correctness was shown
in [49]. We use slicing to justify each statement in this HeyVL encoding.
Theorem 21. Let S ′ be a slice of S = P ark(b, C, I) as in Lemma 27 and be
minimal such that σ ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩ for some state σ.

1. Pre does not entail invariant. If S ′ includes 1 , then X(σ ′ ) ̸≤ I(σ ′ ) for
   some state σ ′ .
6
    For an expectation X ∈ E where X ⪯ 1, the weakest liberal pre-expectation
    wlpJSK(X)(σ) is the expected value of X after executing S when starting in state
    σ ∈ States, assigning 1 to those executions which do not terminate. Dually, the weak-
    est pre-expectation semantics wpJSK(X)(σ) assigns 0 to diverging executions, and is
    defined for all expectations X ∈ E. A detailed exposition is given in [28].
18         P. Schröer et al.


                                                  1   x := init_x;
      1      1   assert I;                        2   cont := true;
             2   havoc variables;                 3   @invariant(I)
             3   validate;                        4   while (cont) {
       I     4   assume I;                        5      prob_choice :≈ flip(0.5);
             5   if (b) {                         6      if (prob_choice) {
             6     C;                             7        cont := false
      2      7     assert I;                      8      } else {
      II     8     assume ?(false)                9        x := x + 1
             9   } else { } // Y                 10      }
                                                 11   }


Fig. 12: Encoding P ark(b, C, I) of            Fig. 13: Geometric loop S with dif-
Park induction to underapproxi-                ferent loop invariants I to verify |=
mate wlpJwhile (b) {C}K(Y ).                   ⟨init_x + 1⟩⪰ S ⟨x⟩.


2. Invariant not inductive. If S ′ includes the assertion 2 , then there is a
   state σ ′ where the loop guard b is true and σ ′ ̸|= ⟨I⟩⪯ C ⟨I⟩.
3. Invariant does not entail post. If S ′ includes neither assertion 1 nor
    2 , and C contains neither assert nor coassume statements, then there is
   a state σ ′ for which the loop guard b does not hold and I(σ ′ ) ̸≤ Y (σ ′ ).
    These three error messages closely correspond to error messages in qualitative
verification. Dually, assumptions can be analyzed to find out how they influence
the final proof obligation. Here, we obtain diagnostics from removed assumptions,
as opposed to the remaining assertions in the above theorem.
Theorem 22. Let S = P ark(b, C, I) as in Figure 12 and S ′ be obtained by
removing any subset of the assumptions I or II , and let S ′ verify, i.e. |=
⟨X⟩⪯ S ′ ⟨Y ⟩. Then:

1. Assuming the invariant is not necessary. If S ′ does not include I ,
   then S verifies with invariant I = ∞, i.e. |= ⟨X⟩⪯ P ark(b, C, ∞) ⟨Y ⟩.
2. While loop could be an if statement. If S ′ does not include the assump-
   tion II , then |= ⟨X⟩⪯ if (b) {C} else {} ⟨Y ⟩ holds.
    In case (1), the loop verification can be generalized to not require the invariant
so that the loop can be used in a larger context. In case (2), the specification
might be too weak to require a loop, indicating a possible bug in the specification
or the loop. An example is the buggy reservoir sampling algorithm from Figure 5,
annotated with the invariant 1/n · [i ≤ X ∧ X ≤ n] + [c = X].
Example 23. Consider the HeyVL program S in Figure 13. It models a geometric
loop counting the number of coin flips until the first success in x. To upper bound
the expected value of x at the end by the initial value of x increased by one, we
use pre init_x + 1 and post x, and annotate the loop using the Park induction
                             Diagnostics for Probabilistic Program Verification       19

proof rule with invariant I. The choice of I gives different diagnostic messages
from Theorems 21 and 22, dualized for the upper bound scenario. With I = x+1
verification fails with ’Invariant not inductive.’ With I = ite(cont, x + 1, x)
verification succeeds with ’While loop could be an if statement,’ i.e., performing
a single flip establishes the upper bound, as this increases x by at most one.


5     Implementation and Evaluation

We realized our three types of slices in the quantitative deductive verifier Cae-
sar [49]. The slicer is called Brutus.7 The results of Brutus are used in Language
Server Protocol [39] support of Caesar and are shown as errors or suggestions in
the Visual Studio Code editor.
     In this section, we will briefly explain how we implemented the search for
suitable slices, compare the approaches on a set of selected benchmarks, and
explore how helpful the resulting user diagnostics are during the verification
process. More extensive information can be found in Section B.
     At a high level, Brutus operates in three steps. First, it selects suitable state-
ments that can be sliced. Following Figure 6 on page 6, if the original program
does not verify, Brutus selects reductive statements. If the original program ver-
ifies, Brutus selects extensive statements to obtain verification-witnessing slices.
The user can manually mark statements for slicing, which can be used to obtain
verification-preserving slices. The second step is a HeyVL program transforma-
tion that instruments the program with Boolean input variables to enable or
disable the selected statements. Finally, Brutus uses an SMT solver to search for
suitable or optimal slices.8 Let us explain the latter two steps in more detail.

Program Transformation for Slicing. We first transform the input HeyVL pro-
gram S with a set of sub-statements S1 , . . . , Sn that we try to slice. Intuitively, a
Boolean input variable enabledSi is inserted for each potentially sliceable state-
ment Si and we replace Si by if (enabledSi ) {Si } else {}. To avoid an exponen-
tial blow-up of the vp size, we use a transformation which ensures that for each
statement Si , its transformation S̃i contains the post X in its vpJS̃i K(X) exactly
as often as in vpJSi K(X). For example, x := a and assert Y are transformed to
x := ite(enabledS , a, x) and assert ite(enabledS , Y , ∞), respectively. The full
list of transformations is given in Table 3 in Section A.
    The generated verification conditions of the HeyVL encoding are similar to
the ones in Boogie [34]. However, our encoding is done on the program level
instead of by defining a modified program semantics. Furthermore, our encoding
is not limited to error messages, but is also used in the same way when we slice
for verification.
7
    Caesar with slicing support is available online at https://www.caesarverifier.org.
8
    In general, the SMT queries to check whether a HeyVL program verifies are not
    necessarily decidable. It embeds HeyLo, which contains a language expressive enough
    to describe the termination probability of arbitrary programs ([10]), and termination
    with probability 1 is undecidable (c.f. [29]).
20      P. Schröer et al.

Searching for Erroring Slices. After the program transformation, Brutus finds
slices that fail verification with a counterexample. We find error-witnessing slices
by selecting reductive statements in a program that does not verify. The task of
finding (minimal) slices involves considering (all) combinations of enabled and
disabled statements and checking whether the modified HeyVL program verifies.
We solve this task using SMT solving. To find an erroring slice, we check:

         ∃enabledS1 , . . . , enabledSn . (∃σ ∈ States. vpJSK(∞)(σ) ̸= ∞) .     (1)

As this query does not contain a quantifier alternation, it is well-suited for SMT
solving. For our strategy first, we simply ask the SMT solver for a model.
    However, the result may not be minimal. Trivially, assigning true to all
enabledS variables also yields a slice. Our implementation uses the Z3 SMT
solver [18] which can sometimes return models where some variables are marked
as irrelevant for the counterexample. We found that with irrelevant variables set
to false, the counterexamples for our benchmarks are almost minimal slices.
    To find minimal error-preserving slices, we have the strategy opt which runs
a modified binary search in which we repeatedly ask the SMT solver for solutions
with at most n enabled statements. Due to incompleteness of the SMT solver, not
all queries have a yes/no answer. Our algorithm marks these cases unacceptable
and checks the other values. We observed that the search needs a lot fewer steps
when irrelevant variables information is used.

Searching for Verifying Slices. For both verification-witnessing and verification-
preserving slices, we search for slices that verify. The SMT query is:

         ∃enabledS1 , . . . , enabledSn (∀σ ∈ States. vpJSK(∞)(σ) = ∞) .        (2)

In contrast to Equation (1), this query contains a quantifier alternation. We
implemented four strategies to solve this query. The exists-forall strategy
simply encodes the query directly as a quantified formula and discharges it to
the SMT solver. The core strategy uses unsatisfiable cores as provided by Z3.
In our setting, unsatisfiable cores represent a subset of the enabledS variables
that are set to true such that there is no counterexample (i.e. the program
verifies). Our third strategy (mus) is based on enumerating minimal unsatisfiable
subsets (MUS) of assertions [35]. Each such MUS corresponds to a set of enabled
statements that are necessary for the program to verify. The resulting slice is
minimal, i.e. there is no subprogram of the slice which is also a valid slice. The
fourth strategy (sus) finds the globally smallest unsatisfiable subset (SUS) of
the query by enumerating all MUS and thus finds a verifying slice with the least
number of statements.

Evaluation and Setup. Our goal is to provide useful diagnostics to a user during
the verification process. From a theoretical perspective, we have argued in Sec-
tions 3 and 4 how to obtain useful diagnostics with formal guarantees, by finding
(minimal) slices. To compare the different slicing methods we seek to answer the
following evaluation questions (EQ):
                             Diagnostics for Probabilistic Program Verification    21

EQ 1 Is the time needed for slicing acceptable for an interactive setting, i.e. ≤ 1
     second?
EQ 2 What is the ratio between what is actually sliced and what is sliced in a
     minimal slice?

We collected benchmarks for both error-witnessing and verifying slices based
on the literature and extended them with new examples. Our evaluation fo-
cuses on benchmarks verifiable with automated deductive probabilistic program
verification, as we focus on their diagnostics reporting. Testing our algorithms
implemented inside classical verifiers like Boogie [33] is out of scope of this pa-
per. In absence of a benchmark suite for slicing of probabilistic programs, our
benchmarks capture a variety of language features. We have 11 purely Boolean
programs and 21 probabilistic programs. They have explicit nondeterminism (1
program), loops (24 programs), recursion (1 program), conditioning (1 program),
and continuous sampling (3 programs). The experiments were conducted on a
2021 Apple MacBook with an M1 Pro chip and 16 GB of RAM, and a timeout
of 30 s. The detailed results from our benchmarks are included in Section B. In
the following, we summarize the results of our evaluation separately for error-
witnessing and verifying slices.

Evaluation for Error-Witnessing Slices. We considered 16 example programs
(Table 5 in Section B). The benchmark set includes a broader set of examples
aimed to demonstrate that error localization through slicing effectively identifies
the problematic statement in verification tasks, including Figure 3 and examples
producing every diagnostic for Park induction (Figure 15 and table 4 in Sec-
tion B). From the literature on error localization, we include a (non-probabilistic)
simple list access error from [34]. We also include 7 modified probabilistic exam-
ples from [49] where we added errors, failing verification of expected runtimes
of loops. One example involves reasoning about conditioning, utilizing the de-
composition of conditioning into wp and wlp as described by [26]9 . We did the
same for 3 programs modeling sampling from continuous distributions [11]. The
benchmarks range from 7 to 57 lines of code, and our theory narrows this to at
most 5 sliceable statements, 3 on average.
    Search for error slices is fast with both first and opt, usually with times
below 20 milliseconds (EQ 1). For 10 (out of 16) benchmarks, the first found slice
is already optimal (EQ 2). In general, the time to find a guaranteed optimal slice
is not significantly higher (≤ +20 ms) than using the first slice. As minimal slices
are required to accurately report errors (cf. e.g. Theorem 21), this makes our
implementation opt viable to provide user diagnostics with formal guarantees in
an interactive environment.
 9
     For an expectation X ∈ E, the conditional expected value cwpJSK(X) is given by
     cwpJSK(X) = wpJSK(X)/wlpJSK(1) (when wlpJSK(1) ̸= 0). Proving an upper bound
     cwpJSK(X) ⪯ Y /Z is split into two tasks, wpJSK(X) ⪯ Y and Z ⪯ wlpJSK(1). An
     observe statement is encoded into assert statements. Details are provided in [49,
     Section 4.1]
22         P. Schröer et al.


     TO
     104
     103
     102
      10


     0%

     50%

 100%
   TO
            na

            ge ro

            na 8_ pag

            na ro

            na ro ex4

            na ro ex4

            na ro ex5

            2d ro fig

            ba lk fig 7

            pr ia

            rd

            rd

            sp

            un al

            bu

            pa ar wlp

            pa 1

            pa 5

            al 6

            bn it
               va

               hr 20

               va 1

               va 20

               va 20

               va 20

               va 20

               rw

               ye

               sp n_

               sp

               wa

               rd

              if k

               rg n4

               rk _a

               rk

               rk

               go

               _p hm
                  r

                  1

                  r

                  r

                  r

                  r

                  r

                  a

                  s

                  ee ne

                  ee

                  lk

                  w

                  _g

                  l

                  _

                  _

                  _

                  r

                  as _r
                     d

                     d




                     e




                     si
                       2 0_ ur




                        fi
                          _



                          _

                          _

                          _

                          _




                          _

                          la




                            ed
                             tw




                             rm
                                e3



                                _3

                                _5

                                _8



                                ur



                                or




                                _w
                                   1




                                   e

                                   e8



                                   k




                                   p
Fig. 14: Dual bar chart showing run-time (positive y-axis, log-scaled) and per-
centage of removed sliceable statements (negative y-axis, linear scale). TO indi-
cates timeout (30s). We show only 20 of our 30 verifying slices for readability.
The bars are grouped by benchmark. Methods: core (■), mus (■), sus (■),
exists-forall (■).


    One limitation of our current implementation is that it requires the SMT
solver being able to produce a consistent model (returning “SAT”), which is not
always possible due to incompleteness. We found that Boogie intentionally uses
potentially inconsistent models (from an “unknown” result of the SMT solver)
to generate error diagnostics10 . As these models do not carry any guarantees,
we did not follow this approach.

Evaluation for Verifying Slices. For verifying slices, we have 30 examples (Ta-
ble 6 in Section B). Of these, 25 are for verification-preserving slicing and five are
for verification-witnessing slicing. Eight are nonprobabilistic examples from [7],
the others are probabilistic examples based on the literature [52, 20, 49, 44]. We
include all applicable examples from the above sources. The number of poten-
tially sliceable statements ranges from 3 to 75.
    Regarding EQ 1, the results in Figure 14 show that the core strategy is very
fast, with instant results (≤ 5 ms) in most cases and never exceeding 105 ms
for any benchmark. The runtimes of exists-forall have an average of 16 ms
and low variance (96% in ≤ 25 ms), while mus and sus are slower and exhibit
a wide variance in the runtime. The slowest slice search is the sus strategy,
reaching the time-out of 30 seconds on some benchmarks. The search for a slice
of a while loop whose successful termination probability is verified ([44, Example
5.8]) uses the SMT theory of uninterpreted functions with axioms to specify an
10
     https://github.com/boogie-org/boogie/issues/1008
                            Diagnostics for Probabilistic Program Verification      23

exponential function and takes 3.7 seconds. On average, sus is 20% slower than
mus. We conclude that only the core and exists-forall strategies are usable
in interactive scenarios.
    For EQ 2, we empirically found that the core slices are often far from optimal,
as the unsatisfiable cores are not minimal. On 13 of the 30 benchmarks, core does
not slice any statements. In general, the other strategies are able to find (much)
smaller slices. For the benchmarks from the literature, our tool is able to find
optimal slices. Notably, on some examples from [44, 8] we find smaller slices than
their methods. Even though mus only does a local minimization, the resulting
slices match the globally optimal slices obtained by sus in size. exists-forall
does not explicitly minimize the slice, yet also finds results as good as the optimal
sus strategy in 12 cases. The figure shows that any minimization often improves
the results compared to the simple core strategy.
    The results indicate that using the core strategy has almost no perfor-
mance impact on Caesar. As minimal slices are not required for diagnostics
from verification-witnessing slices (c.f. Section 4), it is planned to enable core
by default. For optimal slices, the mus or sus strategies are needed, but require
a lot of extra time. While the exists-forall strategy is often competitive with
the mus and sus strategies, it is limited to reasoning about verification tasks
without uninterpreted functions. When applicable, the exists-forall strategy
is a good alternative to core to greatly improve the results.


6    Related Work

Syntactic Slicing of Probabilistic Programs. A recent overview of slicing tech-
niques for probabilistic programs is [46, 45]. The techniques are either syntac-
tic or semantic. There are two main lines of research for syntactic slicing of
probabilistic programs. [24] incorporate stochastic (in-)dependencies inspired by
d-separation criteria from Bayesian networks. [4, 3] generalize similar ideas to
probabilistic control flow graphs.

Semantic Slicing of Probabilistic Programs. Lifting the concepts from classical
programs by [8], the only prior work for semantic slicing on probabilistic pro-
grams is [44]. They consider specification-based slices, i.e. verification-preserving
slices in our terminology. To obtain minimal slices, they describe an algorithm
that checks between every pair of statements (Si , Sj ) in a sequence S1 ; · · · ; Sn
whether one can jump from one to the other and still establish the specification
with pre X and post Y . The check can be seen as a local reductiveness check for
                                                                                     ?
the specific propagated weakest pre: vpJSi ; · · · ; Sj−1 K(vpJSj ; · · · ; Sn K(Y )) ⪯
vpJSj ; · · · ; Sn K(Y ). These results are assembled into a slice graph in which a
weighted shortest path is searched to appropriately handle nested statements.
    We do not require reductiveness to obtain verification-preserving slices. Con-
sider the program x := 1; x := x · x w.r.t. pre 1 and post x. In contrast to
ours, their approach cannot remove any statement. We are able to find the same
24        P. Schröer et al.

minimal slices or even smaller slices (c.f. Section 5). For future work, local re-
ductiveness checks could be explored for finding error-witnessing slices.
   As their fairly intricate algorithm has not been implemented, experimental
comparison is not feasible. Scaling in the number of statements, our binary
search approaches require only a logarithmic amount of solver calls, while their
algorithm requires a quadratic number of calls to obtain the slice graph. We
achieve this by leveraging SMT solvers to explore many options efficiently.
   Finally, [44] only supports the verification of a loop’s partial correctness
through Park induction, and for its total correctness via a variant-based rule [38,
Lemma 7.5.1]. We slice on HeyVL, into which different proof rules can be encoded.
Thus, our method is independent of the proof rules used.

Forwards- and Backwards Reasoning. We disagree that “specification-based slic-
ing techniques require a combination of both backward propagation of post-
conditions and forward propagation of pre-conditions to yield minimal slices” [44,
Sec. 8]. A similar claim is made for classical program slicing in [7]. Our ap-
proach only uses backwards reasoning and finds minimal slices for their claimed
counterexamples (c.f. Section B.2). As our approach takes a global view of all
statements, including assume statements encoding the pre, the solver slices using
that as well. However, Caesar also supports forwards reasoning while generating
verification conditions as a performance optimization.11 In fact, this optimiza-
tion is necessary to handle the Bayesian network example, which suffers from
exponential blow-up due to branching.

Slicing of Intermediate Languages. For classical programs, slicing on IVLs is
tackled in [53]. Strengthening the definition of a specification-based slice as a
program refinement, they define a semi-refinement which must preserve the exact
behavior of the original program on all terminating states. However, it allows
slicing all assertions [53, Lemma 6.6], and they only present a syntactic slicing
algorithm. Our notions of error-witnessing and verification-witnessing slices are
less restrictive than the equivalence imposed by a semi-refinement.

Error Reporting. [31] extends slicing via program dependence graphs to classical
programs with assert statements, enabling error detection from failed asser-
tions [31, Thm. 6.2]. Localization of the erroring assertion is not done.
    The problem of error reporting for an IVL has been tackled in [34, 17] by
modifying the verification condition generation. In [34], labels (auxiliary Boolean
variables) are attached to subformulas and error locations can be extracted from
the counterexample produced by an SMT solver. The approach relies on the SMT
solver returning suitably small counterexamples. As shown in our evaluation, this
is not always the case without further minimization, which we implement. An
advantage of our approach is that it performs labeling directly on the level of
program statements, enabling further program optimizations.
    [48] defines syntactic slicing on an intermediate language. A failed verification
attempt yields a program trace which is used to find the statement causing
11
     For example, assignments are applied lazily, as in KeY [2], c.f. [21, Section 6.3.4].
                           Diagnostics for Probabilistic Program Verification     25

the failure. Then, a syntactic slice is constructed which is sufficient to produce
the same error. However, correctness guarantees on the obtained subprogram
w.r.t. a slicing definition are not given. Finally, [36] searches for verification-
witnessing slices using counterexamples of an SMT solver. For minimization,
minimal unsatisfiable cores are used. Statements which are deemed irrelevant are
not removed, but are replaced by abstractions to keep the program’s structure.
Hence, the result is not a subprogram.

Program Refinement. [38] define a program refinement relation for probabilistic
programs. Verification-witnessing and verification-preserving slices can be seen
as refinements. The original program refines a verification-witnessing slice and a
verification-preserving slice refines the original program. Slices are restricted to
be subprograms of the original program, while refinement does not impose any
syntactic constraints.

Counterexamples in Probabilistic Model Checking. Searching for (minimal) coun-
terexamples in probabilistic model checking has been studied extensively [25, 1,
27]. Han and Katoen defined evidences for property violation; for reachability
as a set of paths whose sum of probabilities exceed a given threshold [22]. Al-
ternatively, critical subsystems represented by high-level counterexamples on the
level of a PRISM program are used. Minimal counterexamples can be obtained
by solving a MaxSAT problem [19] or an MILP [55].


7   Conclusion and Future Work

In this paper, we formally defined the notions of error-witnessing, verification-
witnessing, and verification-preserving slices for probabilistic program verifica-
tion. These are aimed at localizing verification errors, extracting verification
certificates, and tailoring programs to a specification, respectively. We applied
error-witnessing and verification-witnessing slicing to encodings of proof rules for
probabilistic programs in the HeyVL intermediate verification language and gave
formal guarantees for user diagnostics for these encodings based on the slicing
results. Finally, we presented Brutus, the first tool for specification-based slicing
of probabilistic programs, which is integrated in the Caesar deductive verifier.
Our implementation supports different algorithms to compute these slices, and
we compared their trade-offs using a set of benchmarks.
    Future work includes the addition of slicing-based error messages and hints
to other proof rules, such as latticed k-induction [9], and the integration of
probabilistic model checking into the slicing process. We also want to investigate
making use of SMT solver results with fewer guarantees (“unknown” results) to
enable better diagnostics in the presence of SMT solver incompleteness. Further,
our implementation is limited by selecting only assert-like statements for error-
witnessing slicing. This could be improved by additional syntactic slicing, or
further investigating local reductiveness.
26     P. Schröer et al.

Acknowledgments
This work was partially supported by the ERC Advanced Research Grant FRAP-
PANT (grant no. 787914), the Research Training Group 2236 UnRAVeL (project
number 282652900), and by the European Union’s Horizon 2020 research and
innovation programme under the Marie Skłodowska-Curie grant agreement MIS-
SION (grant no. 101008233). We thank Alexander Bork for suggesting the name
Brutus.

References
1. Ábrahám, E., Becker, B., Dehnert, C., Jansen, N., Katoen, J., Wimmer, R.: Coun-
   terexample Generation for Discrete-Time Markov Models: An Introductory Survey.
   In: Bernardo, M., Damiani, F., Hähnle, R., Johnsen, E.B., Schaefer, I. (eds.) For-
   mal Methods for Executable Software Models - 14th International School on For-
   mal Methods for the Design of Computer, Communication, and Software Systems,
   SFM 2014, Bertinoro, Italy, June 16-20, 2014, Advanced Lectures. LNCS, vol. 8483,
   pp. 65–121. Springer, Heidelberg (2014). https://doi.org/10.1007/978-3-319-
   07317-0_3
2. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H., Ulbrich, M. (eds.):
   Deductive Software Verification - The KeY Book - From Theory to Practice.
   Springer (2016)
3. Amtoft, T., Banerjee, A.: A Theory of Slicing for Imperative Probabilistic Pro-
   grams. ACM Trans. Program. Lang. Syst. 42(2), 6:1–6:71 (2020). https://doi.
   org/10.1145/3372895
4. Amtoft, T., Banerjee, A.: A Theory of Slicing for Probabilistic Control Flow
   Graphs. In: Jacobs, B., Löding, C. (eds.) Foundations of Software Science and Com-
   putation Structures - 19th International Conference, FOSSACS 2016, Held as Part
   of the European Joint Conferences on Theory and Practice of Software, ETAPS
   2016, Eindhoven, The Netherlands, April 2-8, 2016, Proceedings. LNCS, vol. 9634,
   pp. 180–196. Springer, Heidelberg (2016). https://doi.org/10.1007/978-3-662-
   49630-5_11
5. Andrieu, C., de Freitas, N., Doucet, A., Jordan, M.I.: An Introduction to MCMC
   for Machine Learning. Mach. Learn. 50(1-2), 5–43 (2003). https://doi.org/10.
   1023/A:1020281327116
6. Astrauskas, V., Bílý, A., Fiala, J., Grannan, Z., Matheja, C., Müller, P., Poli,
   F., Summers, A.J.: The Prusti Project: Formal Verification for Rust. In: Desh-
   mukh, J.V., Havelund, K., Perez, I. (eds.) NASA Formal Methods - 14th Interna-
   tional Symposium, NFM 2022, Pasadena, CA, USA, May 24-27, 2022, Proceedings.
   LNCS, vol. 13260, pp. 88–108. Springer, Heidelberg (2022). https://doi.org/10.
   1007/978-3-031-06773-0_5
7. Barros, J.B., da Cruz, D.C., Henriques, P.R., Pinto, J.S.: Assertion-based Slic-
   ing and Slice Graphs. In: Fiadeiro, J.L., Gnesi, S., Maggiolo-Schettini, A. (eds.)
   8th IEEE International Conference on Software Engineering and Formal Meth-
   ods, SEFM 2010, Pisa, Italy, 13-18 September 2010, pp. 93–102. IEEE Computer
   Society (2010). https://doi.org/10.1109/SEFM.2010.18
8. Barros, J.B., da Cruz, D.C., Henriques, P.R., Pinto, J.S.: Assertion-based slicing
   and slice graphs. Formal Aspects Comput. 24(2), 217–248 (2012). https://doi.
   org/10.1007/S00165-011-0196-1
                            Diagnostics for Probabilistic Program Verification       27

 9. Batz, K., Chen, M., Kaminski, B.L., Katoen, J., Matheja, C., Schröer, P.: Latticed
    k-Induction with an Application to Probabilistic Programs. In: Silva, A., Leino,
    K.R.M. (eds.) Computer Aided Verification - 33rd International Conference, CAV
    2021, Virtual Event, July 20-23, 2021, Proceedings, Part II. LNCS, vol. 12760,
    pp. 524–549. Springer, Heidelberg (2021). https://doi.org/10.1007/978- 3-
    030-81688-9_25
10. Batz, K., Kaminski, B.L., Katoen, J., Matheja, C.: Relatively complete verification
    of probabilistic programs: an expressive language for expectation-based reasoning.
    Proc. ACM Program. Lang. 5(POPL), 1–30 (2021). https://doi.org/10.1145/
    3434320
11. Batz, K., Katoen, J., Randone, F., Winkler, T.: Foundations for Deductive Ver-
    ification of Continuous Probabilistic Programs: From Lebesgue to Riemann and
    Back. Proc. ACM Program. Lang. 9(OOPSLA1), 421–448 (2025). https://doi.
    org/10.1145/3720429
12. Bingham, E., Chen, J.P., Jankowiak, M., Obermeyer, F., Pradhan, N., Karaletsos,
    T., Singh, R., Szerlip, P.A., Horsfall, P., Goodman, N.D.: Pyro: Deep Universal
    Probabilistic Programming. J. Mach. Learn. Res. 20, 28:1–28:6 (2019). https :
    //jmlr.org/papers/v20/18-403.html
13. Carpenter, B., Gelman, A., Hoffman, M.D., Lee, D., Goodrich, B., Betancourt,
    M., Brubaker, M., Guo, J., Li, P., Riddell, A.: Stan: A Probabilistic Programming
    Language. Journal of Statistical Software 76(1), 1–32 (2017). https://doi.org/
    10.18637/jss.v076.i01. https://www.jstatsoft.org/index.php/jss/article/
    view/v076i01
14. Chakarov, A., Sankaranarayanan, S.: Probabilistic Program Analysis with Mar-
    tingales. In: Sharygina, N., Veith, H. (eds.) Computer Aided Verification - 25th
    International Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013.
    Proceedings. LNCS, vol. 8044, pp. 511–526. Springer, Heidelberg (2013). https:
    //doi.org/10.1007/978-3-642-39799-8_34
15. Chatterjee, K., Goharshady, A.K., Meggendorfer, T., Zikelic, D.: Quantitative
    Bounds on Resource Usage of Probabilistic Programs. Proc. ACM Program. Lang.
    8(OOPSLA1), 362–391 (2024). https://doi.org/10.1145/3649824
16. Cousot, P.: Principles of Abstract Interpretation. The MIT Press (2021)
17. Dailler, S., Hauzar, D., Marché, C., Moy, Y.: Instrumenting a weakest precondition
    calculus for counterexample generation. J. Log. Algebraic Methods Program. 99,
    97–113 (2018). https://doi.org/10.1016/J.JLAMP.2018.05.003
18. De Moura, L., Bjørner, N.: Z3: an efficient SMT solver. In: Proceedings of the
    Theory and Practice of Software, 14th International Conference on Tools and Al-
    gorithms for the Construction and Analysis of Systems. TACAS’08/ETAPS’08,
    pp. 337–340. Springer-Verlag, Budapest, Hungary (2008)
19. Dehnert, C., Jansen, N., Wimmer, R., Ábrahám, E., Katoen, J.: Fast Debugging
    of PRISM Models. In: Cassez, F., Raskin, J. (eds.) Automated Technology for
    Verification and Analysis - 12th International Symposium, ATVA 2014, Sydney,
    NSW, Australia, November 3-7, 2014, Proceedings. LNCS, vol. 8837, pp. 146–162.
    Springer, Heidelberg (2014). https://doi.org/10.1007/978-3-319-11936-6_11
20. Gehr, T., Misailovic, S., Tsankov, P., Vanbever, L., Wiesmann, P., Vechev, M.T.:
    Bayonet: probabilistic inference for networks. In: Foster, J.S., Grossman, D. (eds.)
    Proceedings of the 39th ACM SIGPLAN Conference on Programming Language
    Design and Implementation, PLDI 2018, Philadelphia, PA, USA, June 18-22, 2018,
    pp. 586–602. ACM (2018). https://doi.org/10.1145/3192366.3192400
28      P. Schröer et al.

21. Hähnle, R.: Dijkstra’s Legacy on Program Verification. In: Edsger Wybe Dijkstra:
    His Life, Work, and Legacy. Ed. by K.R. Apt and T. Hoare, pp. 105–140. ACM /
    Morgan & Claypool (2022). https://doi.org/10.1145/3544585.3544593
22. Han, T., Katoen, J.: Counterexamples in Probabilistic Model Checking. In: Grum-
    berg, O., Huth, M. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems, 13th International Conference, TACAS 2007, Held as Part of the Joint
    European Conferences on Theory and Practice of Software, ETAPS 2007 Braga,
    Portugal, March 24 - April 1, 2007, Proceedings. LNCS, vol. 4424, pp. 72–86.
    Springer, Heidelberg (2007). https://doi.org/10.1007/978-3-540-71209-1_8
23. Holtzen, S., den Broeck, G.V., Millstein, T.D.: Scaling exact inference for discrete
    probabilistic programs. Proc. ACM Program. Lang. 4(OOPSLA), 140:1–140:31
    (2020). https://doi.org/10.1145/3428208
24. Hur, C., Nori, A.V., Rajamani, S.K., Samuel, S.: Slicing probabilistic programs. In:
    O’Boyle, M.F.P., Pingali, K. (eds.) ACM SIGPLAN Conference on Programming
    Language Design and Implementation, PLDI ’14, Edinburgh, United Kingdom -
    June 09 - 11, 2014, pp. 133–144. ACM (2014). https : / / doi . org / 10 . 1145 /
    2594291.2594303
25. Jansen, N.: Counterexamples in probabilistic verification. PhD thesis, RWTH Aachen
    University, Germany (2015). http://publications.rwth- aachen.de/record/
    479827.
26. Jansen, N., Kaminski, B.L., Katoen, J., Olmedo, F., Gretz, F., McIver, A.: Condi-
    tioning in Probabilistic Programming. In: Ghica, D.R. (ed.) The 31st Conference on
    the Mathematical Foundations of Programming Semantics, MFPS 2015, Nijmegen,
    The Netherlands, June 22-25, 2015. Electronic Notes in Theoretical Computer Sci-
    ence, pp. 199–216. Elsevier (2015). https://doi.org/10.1016/J.ENTCS.2015.12.
    013
27. Jantsch, S., Harder, H., Funke, F., Baier, C.: Switss: Computing Small Witnessing
    Subsystems. In: 2020 Formal Methods in Computer Aided Design, FMCAD 2020,
    Haifa, Israel, September 21-24, 2020, pp. 236–244. IEEE (2020). https://doi.
    org/10.34727/2020/ISBN.978-3-85448-042-6_31
28. Kaminski, B.L.: Advanced weakest precondition calculi for probabilistic programs.
    PhD thesis, RWTH Aachen University, Germany (2019). http://publications.
    rwth-aachen.de/record/755408.
29. Kaminski, B.L., Katoen, J.: On the Hardness of Almost-Sure Termination. In:
    Italiano, G.F., Pighizzini, G., Sannella, D. (eds.) Mathematical Foundations of
    Computer Science 2015 - 40th International Symposium, MFCS 2015, Milan, Italy,
    August 24-28, 2015, Proceedings, Part I. LNCS, vol. 9234, pp. 307–318. Springer,
    Heidelberg (2015). https://doi.org/10.1007/978-3-662-48057-1_24
30. Kaminski, B.L., Katoen, J., Matheja, C., Olmedo, F.: Weakest Precondition Rea-
    soning for Expected Runtimes of Randomized Algorithms. J. ACM 65(5), 30:1–
    30:68 (2018). https://doi.org/10.1145/3208102
31. Léchenet, J., Kosmatov, N., Gall, P.L.: Cut branches before looking for bugs: certi-
    fiably sound verification on relaxed slices. Formal Aspects Comput. 30(1), 107–131
    (2018). https://doi.org/10.1007/S00165-017-0439-X
32. Leino, K.R.M.: Dafny: An Automatic Program Verifier for Functional Correctness.
    In: Clarke, E.M., Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence,
    and Reasoning - 16th International Conference, LPAR-16, Dakar, Senegal, April
    25-May 1, 2010, Revised Selected Papers. LNCS, vol. 6355, pp. 348–370. Springer,
    Heidelberg (2010). https://doi.org/10.1007/978-3-642-17511-4_20
                           Diagnostics for Probabilistic Program Verification      29

33. Leino, K.R.M.: This is Boogie 2, (2008). https : / / www . microsoft . com / en -
    us/research/publication/this-is-boogie-2-2/
34. Leino, K.R.M., Millstein, T.D., Saxe, J.B.: Generating error traces from verification-
    condition counterexamples. Sci. Comput. Program. 55(1-3), 209–226 (2005)
35. Liffiton, M.H., Malik, A.: Enumerating Infeasibility: Finding Multiple MUSes Quickly.
    In: Gomes, C.P., Sellmann, M. (eds.) Integration of AI and OR Techniques in
    Constraint Programming for Combinatorial Optimization Problems, 10th Interna-
    tional Conference, CPAIOR 2013, Yorktown Heights, NY, USA, May 18-22, 2013.
    Proceedings. LNCS, vol. 7874, pp. 160–175. Springer, Heidelberg (2013). https:
    //doi.org/10.1007/978-3-642-38171-3_11
36. Liu, T.: Efficient Verification of Programs with Complex Data Structures Using
    SMT Solvers. PhD thesis, Karlsruhe Institute of Technology, Germany (2018).
    https://publikationen.bibliothek.kit.edu/1000084545.
37. Majumdar, R., Sathiyanarayana, V.R.: Sound and Complete Proof Rules for Prob-
    abilistic Termination. Proc. ACM Program. Lang. 9(POPL), 1871–1902 (2025).
    https://doi.org/10.1145/3704899
38. McIver, A., Morgan, C.: Abstraction, Refinement and Proof for Probabilistic Sys-
    tems. Springer (2005)
39. Microsoft, Language Server Protocol Specification - 3.17, (2024). https://microsoft.
    github.io/language-server-protocol/specifications/lsp/3.17/specification/
    (visited on 09/09/2024)
40. Moosbrugger, M., Stankovic, M., Bartocci, E., Kovács, L.: This is the moment for
    probabilistic loops. Proc. ACM Program. Lang. 6(OOPSLA2), 1497–1525 (2022).
    https://doi.org/10.1145/3563341
41. Morgan, C.: The Specification Statement. ACM Trans. Program. Lang. Syst. 10(3),
    403–419 (1988). https://doi.org/10.1145/44501.44503
42. Müller, P.: Building Deductive Program Verifiers, (2018). https://pmpub.inf.
    ethz.ch/publications/Mueller19.pdf
43. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A Verification Infrastructure
    for Permission-Based Reasoning. In: Jobstmann, B., Leino, K.R.M. (eds.) Verifica-
    tion, Model Checking, and Abstract Interpretation - 17th International Conference,
    VMCAI 2016, St. Petersburg, FL, USA, January 17-19, 2016. Proceedings. LNCS,
    vol. 9583, pp. 41–62. Springer, Heidelberg (2016). https://doi.org/10.1007/978-
    3-662-49122-5_2
44. Navarro, M., Olmedo, F.: Slicing of probabilistic programs based on specifications.
    Sci. Comput. Program. 220, 102822 (2022). https://doi.org/10.1016/J.SCICO.
    2022.102822
45. Olmedo, F.: Slicing of Probabilistic Programs: A Review of Existing Approaches.
    ACM Comput. Surv. 58(3) (2025). https://doi.org/10.1145/3764581
46. Olmedo, F.: Static Slicing for Probabilistic Programs: An Overview. In: Principles
    of Verification: Cycling the Probabilistic Landscape: Essays Dedicated to Joost-
    Pieter Katoen on the Occasion of His 60th Birthday, Part I, pp. 155–178. Springer
    Nature Switzerland, Cham (2025). https://doi.org/10.1007/978-3-031-75783-
    9_7
47. Park, D.: Fixpoint Induction and Proofs of Program Properties. Machine Intelli-
    gence 5 (1969)
48. Ruskiewicz, J.N.: Localizing and Understanding Verification Errors. PhD thesis,
    ETH Zurich, Zürich, Switzerland (2012). https://doi.org/10.3929/ETHZ- A-
    007326234. https://hdl.handle.net/20.500.11850/56315.
30      P. Schröer et al.

49. Schröer, P., Batz, K., Kaminski, B.L., Katoen, J., Matheja, C.: A Deductive Ver-
    ification Infrastructure for Probabilistic Programs. Proc. ACM Program. Lang.
    7(OOPSLA2), 2052–2082 (2023). https://doi.org/10.1145/3622870
50. Torres-Ruiz, M., Piedeleu, R., Silva, A., Zanasi, F.: On Iteration in Discrete Prob-
    abilistic Programming. In: Rehof, J. (ed.) 9th International Conference on Formal
    Structures for Computation and Deduction, FSCD 2024, July 10-13, 2024, Tallinn,
    Estonia. LIPIcs, 20:1–20:21. Schloss Dagstuhl - Leibniz-Zentrum für Informatik
    (2024). https://doi.org/10.4230/LIPICS.FSCD.2024.20
51. Tran, D., Hoffman, M.D., Moore, D., Suter, C., Vasudevan, S., Radul, A.: Simple,
    Distributed, and Accelerated Probabilistic Programming. In: Bengio, S., Wallach,
    H.M., Larochelle, H., Grauman, K., Cesa-Bianchi, N., Garnett, R. (eds.) Advances
    in Neural Information Processing Systems 31: Annual Conference on Neural In-
    formation Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montréal,
    Canada, pp. 7609–7620 (2018). https://proceedings.neurips.cc/paper/2018/
    hash/201e5bacd665709851b77148e225b332-Abstract.html
52. Vitter, J.S.: Random Sampling with a Reservoir. ACM Trans. Math. Softw. 11(1),
    37–57 (1985). https://doi.org/10.1145/3147.3165
53. Ward, M.P., Zedan, H.: Slicing as a program transformation. ACM Trans. Program.
    Lang. Syst. 29(2), 7 (2007). https://doi.org/10.1145/1216374.1216375
54. Weiser, M.D.: Program Slicing. IEEE Trans. Software Eng. 10(4), 352–357 (1984).
    https://doi.org/10.1109/TSE.1984.5010248
55. Wimmer, R., Jansen, N., Vorpahl, A., Ábrahám, E., Katoen, J., Becker, B.: High-
    level Counterexamples for Probabilistic Automata. Log. Methods Comput. Sci.
    11(1) (2015). https://doi.org/10.2168/LMCS-11(1:15)2015
56. Xu, B., Qian, J., Zhang, X., Wu, Z., Chen, L.: A brief survey of program slicing.
    ACM SIGSOFT Softw. Eng. Notes 30(2), 1–36 (2005). https://doi.org/10.
    1145/1050849.1050865
                            Diagnostics for Probabilistic Program Verification       31

A     Proofs

Notation. We denote by skip the effectless statement with vpJskipK(X) = X
for all X ∈ E. Although not part of our formal syntax, we can express it via e.g.
skip ≡ assert ∞ ≡ assume ∞.


A.1    Slices from Refinement

We first formally state and prove how to obtain slices from refinement relations,
which will be used later in the proofs below. The second and third lemmas
correspond to our claims in the paragraph Program Refinement in Section 6:
Lemma 25 states that “the original program refines a verification-witnessing
slice” and Lemma 26 states that “a verification-preserving slice refines the original
program”.

Lemma 24 (Error-witnessing slice from refinement). Let S ′ be a sub-
program of S ∈ HeyVL. Assume S is refined by S ′ , i.e. vpJSK(Z) ⪯ vpJS ′ K(Z)
for all Z ∈ E. If S ′ does not verify w.r.t. X, Y ∈ E, i.e. X ̸⪯ vpJS ′ K(Y ), then S ′
is an error-witnessing slice of S w.r.t. X, Y .

Proof. Since S ′ does not verify w.r.t. X, Y , we satisfy condition (1) of Defini-
tion 3.
    Let σ ′ be a state such that σ ′ ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩ holds. This means X(σ) ̸≤
vpJS ′ K(Y )(σ). However, since S is refined by S ′ , we have vpJSK(Y )(σ) ≤ vpJS ′ K(Y )(σ).
Therefore, σ ′ ̸|= ⟨X⟩⪯ S ⟨Y ⟩ holds, satisfying condition (2) of Definition 3.

Lemma 25 (Verification-witnessing slice from refinement). Let S ′ be a
subprogram of S ∈ HeyVL. Assume S ′ is refined by S, i.e. vpJS ′ K(Z) ⪯ vpJSK(Z)
for all Z ∈ E. Then, for all X, Y ∈ E, S ′ is a verification-witnessing slice of S
w.r.t. X, Y .

Proof. Assume |= ⟨X⟩⪯ S ′ ⟨Y ⟩, i.e. X ⪯ vpJS ′ K(Y ). Since S ′ is refined by S,
we have X ⪯ vpJS ′ K(Y ) ⪯ vpJSK(Y ). Therefore, |= ⟨X⟩⪯ S ⟨Y ⟩ holds. On the
other hand, if |= ⟨X⟩⪯ S ′ ⟨Y ⟩ does not hold, the definition is satisfied trivially.
Therefore, Definition 11 is satisfied.

Lemma 26 (Verification-preserving slice from refinement). Let S ′ be a
subprogram of S ∈ HeyVL. Assume S is refined by S ′ , i.e. vpJSK(Z) ⪯ vpJS ′ K(Z)
for all Z ∈ E. Then, for all X, Y ∈ E, S ′ is a verification-preserving slice of S
w.r.t. X, Y .

Proof. Assume |= ⟨X⟩⪯ S ⟨Y ⟩, i.e. X ⪯ vpJSK(Y ). Since S is refined by S ′ ,
we have X ⪯ vpJSK(Y ) ⪯ vpJS ′ K(Y ). Therefore, |= ⟨X⟩⪯ S ′ ⟨Y ⟩ holds. On the
other hand, if |= ⟨X⟩⪯ S ⟨Y ⟩ does not hold, the definition is satisfied trivially.
Therefore, Definition 16 is satisfied.
32        P. Schröer et al.

A.2      Proofs for Section 3
Recall Lemma 6 from page 12:
Lemma 6. Statements assert, coassume, havoc, and validate are reduc-
tive.12
Proof. By Definition 5, a statement S is reductive if for all X ∈ E, vpJSK(X) ⪯ X
holds.

 – Let S = assert Y . Then, for all X ∈ E,

                              vpJassert Y K(X) = Y ⊓ X ⪯ X.

 – Let S = coassume Y . Then, for all X ∈ E,
                                         (
                                           0,            if Y (σ) ≥ X(σ)
     vpJcoassume Y K(X) = Y ⇝ X = λσ.                                    ⪯ X .
                                           X(σ),         otherwise

 – Let S = validate. Then, for all X ∈ E,
                                          (
                                           ∞, if X(σ) = ∞
             vpJvalidateK(X) = △(X) = λσ.                 ⪯ X .
                                           0, otherwise

Recall Theorem 7 from page 12:
Theorem 7. Let S ′ be a subprogram obtained from program S by only erasing
reductive statements. If ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩, then S ′ is an error-witnessing slice of
S w.r.t. (X, Y ) for all X, Y ∈ E. In particular, we have vpJSK(X) ⪯ vpJS ′ K(X)
for all X ∈ E.
Proof. Let S ′ be a subprogram of S obtained by only removing reductive state-
ments. We show by induction on the structure of S that the following refinement
holds for all X ∈ E:
                            vpJSK(X) ⪯ vpJS ′ K(X) .
    Let S ∈ HeyVL and S ′ be a subprogram of S. For each case, when S = S ′ , the
property holds trivially and we will omit them in the following. Assume therefore
that S ̸= S ′ .
    Base cases. These are the cases S ∈ {var x : τ :≈ µ, assert Y , assume Y ,
havoc x, validate, reward a, coassert Y , coassume Y , cohavoc x, covalidate}.
Either S is not reductive (in which case S = S ′ holds) or it is reductive.
If removed, we have S ′ = skip. By reductiveness, we obtain vpJSK(X) ⪯
vpJskipK(X).
    Induction hypothesis. Assume the property holds for all subprograms S1′ , S2′
of S1 , S2 , respectively.
    Induction step.
12
     These are all atomic HeyVL statements that are reductive in their general form.
     Specific instances of other statements, e.g. assume ∞, are also reductive.
                          Diagnostics for Probabilistic Program Verification     33

 – Case S = S1 ; S2 : We have S ′ = S1′ ; S2′ for subprograms S1′ , S2′ of S1 , S2 ,
   respectively. Then,

         vpJS1 ; S2 K(X) = vpJS1 K(vpJS2 K(X))
                         ⪯ vpJS1′ K(vpJS2 K(X))                                (IH)
                         ⪯ vpJS1′ K(vpJS2′ K(X))     (IH, monotonicity of vpJS1′ K)
                                ′
                         = vpJS K(X) .

 – Case S = if (⊓) {S1 } else {S2 }: We have S ′ = if (⊓) {S1′ } else {S2′ } for
   subprograms S1′ , S2′ of S1 , S2 , respectively.

             vpJif (⊓) {S1 } else {S2 }K(X) = vpJS1 K(X) ⊓ vpJS2 K(X)
                                               ⪯ vpJS1′ K(X) ⊓ vpJS2 K(X)      (IH)
                                               ⪯ vpJS1′ K(X) ⊓ vpJS2′ K(X)     (IH)
                                                      ′
                                               = vpJS K(X) .

 – Case S = if (⊔) {S1 } else {S2 }: We have S ′ = if (⊔) {S1′ } else {S2′ } for
   subprograms S1′ , S2′ of S1 , S2 , respectively.

             vpJif (⊔) {S1 } else {S2 }K(X) = vpJS1 K(X) ⊔ vpJS2 K(X)
                                               ⪯ vpJS1′ K(X) ⊔ vpJS2 K(X)      (IH)
                                               ⪯ vpJS1′ K(X) ⊔ vpJS2′ K(X)     (IH)
                                                      ′
                                               = vpJS K(X) .

    Thus, vpJSK(X) ⪯ vpJS ′ K(X) holds for all subprograms S ′ of S where S ′
was obtained by only removing reductive statements. By Lemma 24, S ′ is an
error-witnessing slice of S w.r.t. (X, Y ).
Recall Lemma 9 from page 13:
Lemma 9. For all S1 and S2 , the demonic choice S = if (⊓) {S1 } else {S2 }
fulfills: vpJSK(X) ⪯ vpJS1 K(X) and vpJSK(X) ⪯ vpJS2 K(X), for all X ∈ E.
Proof. Let X ∈ E. We have

          vpJif (⊓) {S1 } else {S2 }K(X) = vpJS1 K(X) ⊓ vpJS2 K(X).

By definition of ⊓, we obtain both

           vpJSK(X) ⪯ vpJS1 K(X)      and    vpJSK(X) ⪯ vpJS2 K(X) .□

    Although not stated explicitly in the main text, a dual statement to Lemma 9
exists for the angelic choice S = if (⊔) {S1 } else {S2 }, and can be shown
similarly. For all X ∈ E, we have

            vpJSK(X) ⪰ vpJS1 K(X)      and   vpJSK(X) ⪰ vpJS2 K(X) .

Recall Lemma 14 from page 14:
34      P. Schröer et al.

Lemma 14. assume, coassert, cohavoc, covalidate, reward are extensive.
Proof. By Definition 13, a statement S is extensive if for all X ∈ E, vpJSK(X) ⪰
X holds.
 – Let S = assume Y . Then, for all X ∈ E,
                                        (
                                                 ∞,        if Y (σ) ≤ X(σ)
       vpJassume Y K(X) = Y → X = λσ.                                      ⪰ X .
                                                 X(σ),     otherwise
 – Let S = coassert Y . Then, for all X ∈ E,
                            vpJcoassert Y K(X) = Y ⊔ X ⪰ X .
 – Let S = covalidate. Then, for all X ∈ E,
                                          (
                                            0, if X(σ) = 0
         vpJcovalidateK(X) = ▽(X) = λσ.                    ⪰ X .
                                            ∞, otherwise
 – Let S = reward Y . Then, for all X ∈ E,
               vpJreward Y K(X) = Y + X ⪰ X .                      (Y is non-negative)
Recall Theorem 15 from page 14:
Theorem 15. Let S ′ be a subprogram obtained from S by only removing exten-
sive statements. Then, S ′ is a verification-witnessing slice of S w.r.t. (X, Y ) for
all X, Y ∈ E. In particular, we have vpJSK(X) ⪰ vpJS ′ K(X) for all X ∈ E.
Proof. Let S ′ be a subprogram of S obtained by only removing extensive state-
ments. It can be shown that the following holds for all X ∈ E:
                                vpJSK(X) ⪰ vpJS ′ K(X) .
The proof is completely dual to the structural induction done for Theorem 7
(c.f. page 32): one simply replaces ⪯ by ⪰. By Lemma 25, we obtain the desired
result.
Recall Lemma 17 from page 15:
Lemma 17. For subprogram S ′ of program S: If S ′ is an error-witnessing slice
of S w.r.t. (X, Y ), then S ′ is a verification-preserving slice of S w.r.t. (X, Y ).
Proof. If S ′ is an error-witnessing slice of S w.r.t. (X, Y ), then by condition (2)
of Definition 3:
                ∀σ ′ . (σ ′ ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩ =⇒ σ ′ ̸|= ⟨X⟩⪯ S ⟨Y ⟩) .
Rewriting the implication:
                  ∀σ ′ . (σ ′ |= ⟨X⟩⪯ S ′ ⟨Y ⟩ ∨ σ ′ ̸|= ⟨X⟩⪯ S ⟨Y ⟩) .
Rewriting back to an implication, we get the desired result, equivalent to Defi-
nition 16:
               ∀σ ′ . (σ ′ |= ⟨X⟩⪯ S ⟨Y ⟩ =⇒ σ ′ |= ⟨X⟩⪯ S ′ ⟨Y ⟩) .□
                          Diagnostics for Probabilistic Program Verification      35

A.3   Proofs for Section 4
Recall Theorem 19 from page 16. In this context, we consider slices w.r.t. pre ∞
and post ∞.

Theorem 19. Let S = assume X; S ′ ; assert Y .
1. Removing the assert statement shows unverifiability with any post.
   If assume X; S ′ is an error-witnessing slice of S, then ̸|= ⟨X⟩⪯ S ′ ⟨Z⟩ for
   Z ∈ E.
2. Removing the assume statement shows verifiability with any pre.
   If S ′ ; assert Y is a verifying verification-witnessing slice of S, then |=
   ⟨Z⟩⪯ S ′ ⟨Y ⟩ for Z ∈ E.

Proof. (1) Let assume X; S ′ be an error-witnessing slice of S w.r.t. ∞, ∞. By
definition, we get ∞ ̸⪯ vpJassume X; S ′ K(∞). Applying adjointness of assume/→,
we get X ̸⪯ vpJS ′ K(∞). By monotonicity, we have vpJS ′ K(∞ ⊓ Z) ⪯ vpJS ′ K(∞)
for all Z ∈ E. By transitivity of ⪯, we get X ̸⪯ vpJS ′ K(Z), i.e. ̸|= ⟨X⟩⪯ S ′ ⟨Z⟩.
     (2) Let S ′ ; assert Y be a verifying verification-witnessing slice of S w.r.t.
∞, ∞. As program S ′ ; assert Y verifies, we know ∞ ⪯ vpJS ′ ; assert Y K(∞).
For all Z ∈ E, we have Z ⪯ ∞. Thus, Z ⪯ vpJS ′ ; assert Y K(∞) = vpJS ′ K(Y ),
i.e. |= ⟨Z⟩⪯ S ′ ⟨Y ⟩ for Z ∈ E.

Recall Theorem 20 from page 17:

Theorem 20. Let C = v : [X, Y ] and its HeyVL encoding be SC .

1. Pre does not entail specification’s pre. If S ′ is a minimal error-witnessing
   slice of SC w.r.t. (X ′ , Y ′ ) which contains assert X, then X ′ (σ ′ ) ̸≤ X(σ ′ )
   for some σ ′ .
2. Specification statement can be removed. If S ′ is a verification-witnessing
   slice of SC w.r.t. (X ′ , Y ′ ) which verifies and does not contain assume Y , then
   X ′ ⪯ Y ′ holds.

Proof. 1. Let S ′ = assert Y ; S̄ ′ . Since S ′ is an error-witnessing slice and
   minimal, and the only removed statement assert Y is reductive, S̄ ′ verifies.
   Hence,
                               X ′ ⪯ vpJS̄ ′ K(Y ′ ).
    If also X ′ ⪯ Y holds, we get

                         X ′ ⪯ Y ⊓ vpJS̄ ′ K(Y ′ ) = vpJS ′ K(Y ′ ),

    thus contradicting that S ′ is an error-witnessing slice with a counterexample
    state. Hence, we must have X ′ ̸⪯ Y .
 2. Notice that the only statements that might be present in S ′ are reductive.
    As S ′ verifies, we thus have

                               X ′ ⪯ vpJS ′ K(Y ′ ) ⪯ Y ′ .□
36       P. Schröer et al.

    The following lemma states how the assertions in the encoding contribute
to the final proof obligation. It lets us infer the error messages of Theorems 21
and 22.
Lemma 27 (Park Induction Error Components). Let S = P ark(b, C, I)
as in Figure 12 and S ′ be obtained by removing any subset of the assertions 1
and 2 in S. Then:

                    vpJS ′ K(Y ) = PIpre (S ′ ) ⊓ PIind (S ′ ) ⊓ PIpost (S ′ ),

     where for i ∈ { 1, 2 }:
                                                      a) PIpre (S ′ ) = A 1 ,
           (
                   if S ′ includes i , and
                                                                                                      
             I,                                       b) PIind (S ′ ) = J v. △ (I ⊓ ?(b)) → vpJCK(A 2 ) ,
     Ai =
             ∞, else,
                                                      c)PIpost (S ′ ) = J v. △((I ⊓ ?(¬b)) → Y ) .
Proof. First recall that for any Z ∈ E,

                             Z = ∞ ⊓ Z = vpJassert ∞K(Z).

Hence, omitting assertion 1 or 2 in S ′ corresponds to replacing the respective
statement by assert ∞. We obtain the result by simple rewriting:
                                                                                    
vpJS ′ K(Y ) = vpJassert A 1 K J v. △ I → ?(b) → vpJC; assert A 2 ; assume ?(false)K(Y )
                                                        
                                         ⊓ (?(¬b) → Y )
                                                                            
             = A 1 ⊓ J v. △ I → ?(b) → vpJCK(vpJassert A 2 K(∞)) ⊓ (?(¬b) → Y )
                                                                 
             = A 1 ⊓ J v. △ I → ?(b) → vpJCK(A 2 ) ⊓ (?(¬b) → Y )
                                                                        
             = A 1 ⊓ J v. △ I → ?(b) → vpJCK(A 2 ) ⊓ (I → (?(¬b) → Y ))
                                                     (→ and ⊓ commute in antecedent)
                                                                               
            = A 1 ⊓ J v. △            (I ⊓ ?(b)) → vpJCK(A 2 ) ⊓ ((I ⊓ ?(¬b)) → Y )
                                                   (collapse sequence of →)
                                                  
            = A 1 ⊓ J v. △ (I ⊓ ?(b)) → vpJCK(A 2 ) ⊓ J v. △((I ⊓ ?(¬b)) → Y ) .
              |{z}   |             {z              } |            {z
                                                                     ′
                                                                             }
                   ′
               PIpre (S )                                                         PIpost (S )
                                            PIind (S ′ )
                                                             (J /validate commute with ⊓)


We introduce an auxiliary lemma that will be used for the proof of Theorem 21.
Lemma 28. If S is a HeyVL program that contains neither assert nor coassume
statements, then S verifies, i.e. vpJSK(∞) = ∞. Dually, if S is a HeyVL pro-
gram that contains neither coassert nor assume nor reward statements, then
S co-verifies, i.e. vpJSK(0) = 0.
                           Diagnostics for Probabilistic Program Verification       37

Proof. Let S be a HeyVL program without assert nor coassume statements. A
simple induction on the structure of S shows that vpJSK(∞) = ∞ holds.
   Base cases.
 – Case S = var Px : τ :≈ µ: Let µ = p1 · ⟨t1 ⟩ + . . . + pn · ⟨tn ⟩. Since we consider
                    n
   distributions, i=1 pi = 1. Then we have

              vpJSK(∞) = p1 · ∞[x 7→ t1 ] + . . . + pn · ∞[x 7→ tn ] = ∞.

 – Case S = assert Y : Impossible.
 – Case S = assume Y : vpJSK(∞) = Y → ∞ = ∞.
 – Case S = havoc x vpJSK(∞) = J x. ∞ = ∞.
 – Case S = validate: vpJSK(∞) = △(∞) = ∞.
 – Case S = reward a: vpJSK(∞) = ∞ + a = ∞.
 – Case S = coassert Y : vpJSK(∞) = ∞ ⊔ Y = ∞.
 – Case S = coassume Y : Impossible.
 – Case S = cohavoc x: vpJSK(∞) = Sx. ∞ = ∞.
 – Case S = covalidate: vpJSK(∞) = ▽(∞) = ∞.
   Inductive step. Assume the property holds for S1 , S2 .
 – Case S = S1 ; S2 : vpJSK(∞) = vpJS1 K(vpJS2 K(∞)) = vpJS1 K(∞) = ∞.
 – Case S = if (⊓) {S1 } else {S2 }: vpJSK(∞) = vpJS1 K(∞) ⊓ vpJS2 K(∞) =
   ∞ ⊓ ∞ = ∞.
 – Case S = if (⊔) {S1 } else {S2 }: vpJSK(∞) = vpJS1 K(∞) ⊔ vpJS2 K(∞) =
   ∞ ⊔ ∞ = ∞.
   Therefore, S verifies. The proof for the dual case is analogous.

Recall Theorem 21 from page 17:

Theorem 21. Let S ′ be a slice of S = P ark(b, C, I) as in Lemma 27 and be
minimal such that σ ̸|= ⟨X⟩⪯ S ′ ⟨Y ⟩ for some state σ.

1. Pre does not entail invariant. If S ′ includes 1 , then X(σ ′ ) ̸≤ I(σ ′ ) for
   some state σ ′ .
2. Invariant not inductive. If S ′ includes the assertion 2 , then there is a
   state σ ′ where the loop guard b is true and σ ′ ̸|= ⟨I⟩⪯ C ⟨I⟩.
3. Invariant does not entail post. If S ′ includes neither assertion 1 nor
    2 , and C contains neither assert nor coassume statements, then there is
   a state σ ′ for which the loop guard b does not hold and I(σ ′ ) ̸≤ Y (σ ′ ).

    Note that the dual version of this theorem requires a modification in condi-
tion (3) that S ′ contains neither coassert nor assume nor reward statements,
corresponding to the dual case in Lemma 28.

Proof. 1. Assume that S ′ includes assertion 1 . By minimality of S ′ , S ′ ⊖ 1 does
   not have a counterexample, i.e. X ⪯ vpJS ′ ⊖ 1 K(Y ). Hence, by Lemma 27

      X ⪯ vpJS ′ ⊖ 1 K(Y ) = PIpre (S ′ ⊖ 1 ) ⊓ PIind (S ′ ⊖ 1 ) ⊓ PIpost (S ′ ⊖ 1 ).
38       P. Schröer et al.

     From this we can conclude
      X ⪯ PIind (S ′ ⊖ 1 ) = PIind (S ′ )       and    X ⪯ PIpost (S ′ ⊖ 1 ) = PIpost (S ′ ).
     If also X ⪯ PIpre (S ′ ) holds, we use Lemma 27 to get
                   X ⪯ PIpre (S ′ ) ⊓ PIind (S ′ ) ⊓ PIpost (S ′ ) = vpJS ′ K(Y ),
   thus contradicting that S ′ is an error-witnessing slice with a counterexample
   state.
   We must thus have X ̸⪯ PIpre (S ′ ) = A 1 = I, i.e. there exists a state σ ′ with
   X(σ ′ ) ̸≤ I(σ ′ ).
2. Assume that S ′ includes assertion 2 . Similar to the previous case, we can
   use minimality of S ′ to conclude that
                    X ̸⪯ PIind (S ′ ) = J v. △((I ⊓ ?(b)) → vpJCK(I)) .
     If for every state σ ′ , △((I ⊓ ?(b)) → vpJCK(I))[v 7→ ν](σ ′ ) = ∞ for all ν ∈ τ ,
     then X ⪯ ∞ = PIind (S ′ ), a contradiction. Hence, there must exist a state σ ′
     and valuation ν ∈ τ , such that △((I ⊓ ?(b)) → vpJCK(I))[v 7→ ν](σ ′ ) ̸= ∞.
     Applying the definition of validate yields
        ∞ ̸≤ ((I ⊓ ?(b)) → vpJCK(I)) [v 7→ ν](σ ′ )
           = ((I ⊓ ?(b)) → vpJCK(I)) (σ ′ [v 7→ ν]).           (apply substitution to state)
     Writing σ ′′ = σ ′ [v 7→ ν] and using the adjointness of → and ⊓ we immedi-
     ately get
                             ∞ ⊓ (I ⊓ ?(b))(σ ′′ ) ̸≤ vpJCK(I)(σ ′′ ).
     We have that σ ′′ fulfills b, or else (I ⊓ ?(b))(σ ′′ ) = 0 ≤ vpJCK(I)(σ ′′ ) leads to
     a contradiction. Hence, σ ′′ is the state witnessing that the loop invariant is
     not inductive:
                  I(σ ′′ ) = I(σ ′′ ) ⊓ ∞ = (I ⊓ ?(b))(σ ′′ ) ̸≤ vpJCK(I)(σ ′′ ).
3. Assume that S ′ includes neither assertion 1 nor 2 , and C contains neither
   assert nor coassume statements. By Lemma 27
                 X ̸⪯ PIpre (S ′ ) ⊓ PIind (S ′ ) ⊓ PIpost (S ′ )
                    = ∞ ⊓ PIind (S ′ ) ⊓ PIpost (S ′ )              (assertion 1 not in S ′ )
                                ′               ′
                    = PIind (S ) ⊓ PIpost (S )
                    = (J v. △((I ⊓ ?(b)) → vpJCK(∞))) ⊓ PIpost (S ′ )
                                                             (assertion 2 not in S ′ )
                    = (J v. △((I ⊓ ?(b)) → ∞)) ⊓ PIpost (S ′ )
                                                 (vpJCK(∞) = ∞ by Lemma 28)
                    = ∞ ⊓ PIpost (S ′ )                                       (simplification)
                    = PIpost (S ′ ) = J v. △((I ⊓ ?(¬b)) → Y ) .
                            Diagnostics for Probabilistic Program Verification        39

   Reasoning analogous to the previous case there exists a state σ ′ and valuation
   ν ∈ τ with

                         ∞ ̸≤ ((I ⊓ ?(¬b)) → Y ) [v 7→ ν](σ ′ ).

   Again, writing σ ′′ = σ ′ [v 7→ ν] and using the adjointness of → and ⊓ we
   immediately get (I ⊓ ?(¬b))(σ ′′ ) ̸≤ Y (σ ′′ ). σ ′′ does not fulfill b, or else (I ⊓
   ?(¬b))(σ ′′ ) = 0 ≤ Y (σ ′′ ) leads to a contradiction. Hence, σ ′′ is the state
   witnessing that the loop invariant does not entail the post:

                  I(σ ′′ ) = I(σ ′′ ) ⊓ ∞ = (I ⊓ ?(¬b))(σ ′′ ) ̸≤ Y (σ ′′ ).□

Recall Theorem 22 from page 18:

Theorem 22. Let S = P ark(b, C, I) as in Figure 12 and S ′ be obtained by
removing any subset of the assumptions I or II , and let S ′ verify, i.e. |=
⟨X⟩⪯ S ′ ⟨Y ⟩. Then:

1. Assuming the invariant is not necessary. If S ′ does not include I ,
   then S verifies with invariant I = ∞, i.e. |= ⟨X⟩⪯ P ark(b, C, ∞) ⟨Y ⟩.
2. While loop could be an if statement. If S ′ does not include the assump-
   tion II , then |= ⟨X⟩⪯ if (b) {C} else {} ⟨Y ⟩ holds.

Proof. First recall that for any Z ∈ E,

  Z = ∞ → Z = vpJassume ∞K(Z)              and    Z = ∞ ⊓ Z = vpJassert ∞K(Z).

Hence, omitting assumption I or II in S ′ corresponds to replacing the re-
spective statement by assume ∞. And assume ∞/assert ∞ statements can be
added without changing the program’s semantics. We write
       (                                        (
         I, if S ′ includes I ,                   ?(false), if S ′ includes II ,
AI =                             and    A II =
         ∞, else.                                 ∞,        else.

1. Assume that S ′ does not include assumption I . Then

   X ⪯ vpJS ′ K(Y )
      = vpJassert I; havoc variables; validate; if (b) {C; assert I; assume A II } else {}K(Y )
      ⪯ vpJhavoc variables; validate; if (b) {C; assume A II } else {}K(Y )
                                                        (remove reductive statements)
      = vpJassert ∞; havoc variables; validate; if (b) {C; assert ∞; assume A II } else {}K(Y )
      ⪯ vpJP ark(b, C, ∞)K(Y ).                  (add extensive statement assume ∞)

   Hence, ⟨X⟩⪯ P ark(b, C, ∞) ⟨Y ⟩ is valid.
40       P. Schröer et al.


        Table 3: HeyVL program transformations of statements for slicing.
S                         S̃
x := a                  x := ite(enabledS , a, x)
assert Y                assert ite(enabledS , Y , ∞)
assume Y                assume ite(enabledS , Y , ∞)
reward Y                reward ite(enabledS , Y , 0)
coassert Y              coassert ite(enabledS , Y , 0)
coassume Y              coassume ite(enabledS , Y , 0)
if (⊓) {S1 } else {S2 } if (⊓) {assume ?(enabledS1 ); S1 } else {assume ?(enabledS2 ); S2 }
if (⊔) {S1 } else {S2 } if (⊔) {coassume ?(¬enabledS1 ); S1 } else {coassume ?(¬enabledS2 ); S2 }



2. Assume that S ′ does not include assumption II . We have

       X ⪯ vpJS ′ K(Y )
          ⪯ vpJassert I; assume A I ; if (b) {C; assume A II } else {}K(Y )
                                                    (removing reductive statements)
          = vpJassert I; assume A I ; if (b) {C} else {}K(Y )   (A II = ∞)
                                                 
          = I ⊓ A I → vpJif (b) {C} else {}K(Y )
                                                      
          = I ⊓ A I ⊓ A I → vpJif (b) {C} else {}K(Y ) (I ⪯ A I ∈ { I, ∞ })
          ⪯ I ⊓ vpJif (b) {C} else {}K(Y )                         (Modus ponens)
          ⪯ vpJif (b) {C} else {}K(Y ).

     Hence, ⟨X⟩⪯ if (b) {C} else {} ⟨Y ⟩ is valid.                                □


A.4     Proofs for Section 5

For the implementation (Section 5), we introduced a program transformation
that introduces a new variable enabledS for each potentially sliceable statement
S in the HeyVL, executing S only if enabledS is true (and otherwise skipping it).
This transformation is logically equivalent to a conditional execution of S:

                               if (enabledSi ) {Si } else {}

In the implementation, we make use of better encodings to avoid potential ex-
ponential blow-up of the verification pre-expectation. As an example, consider a
program consisting of two assignments S = x := a; y := b. The naive transfor-
mation would yield

     S̃ = if (enabledS1 ) {x := a} else {}; if (enabledS2 ) {y := b} else {} ,
                            Diagnostics for Probabilistic Program Verification   41

so that the verification pre-expectation w.r.t. to post X would evaluate to the
following:

vpJS̃K(X) = ?(enabledS1 ) → (
                   (?(enabledS2 ) → X[y 7→ b][x 7→ a]) ⊓ (?(¬enabledS2 ) → X[x 7→ a])
              ) ⊓ ?(¬enabledS1 ) → (
                   (?(enabledS2 ) → X[y 7→ b]) ⊓ (?(¬enabledS2 ) → X)
              ).

This expression contains four occurrences of X, one for each possible combination
of the two boolean variables enabledS1 and enabledS2 . Instead, we use improved
transformations that avoid this blow-up by pushing the conditionals into the
statements themselves. The complete set of transformations is shown in Table 3.
For the above example, we obtain

       vpJS̃K(X) = X[y 7→ ite(enabledS2 , b, y)][x 7→ ite(enabledS1 , a, x)] .

This expression contains only one occurrence of X, compared to four in the naive
transformation.
   The following theorems state that these transformations, as well as the re-
spective duals (added explicitly here), are correct. The theorems are stated for
non-recursive transformations, and soundness of recursive transformations holds
by induction on the structure of the program.
   We begin with the soundness for the atomic statements.
Theorem 29 (Soundness of Atomic Program Transformations for Slic-
ing). Let S be an atomic HeyVL program, and let S̃ be the program obtained by
applying the transformations from Table 3. For all X ∈ E, the following holds:

          vpJif (enabledS ) {S} else {skip}K(X)           =    vpJS̃K(X) .

Proof. Case S = x := a.

            vpJS̃K(X) = vpJx := ite(enabledS , a, x)K(X)
                        = X[x 7→ ite(enabledS , a, x)]
                        = ite(enabledS , X[x 7→ a], X[x 7→ x])
                        = ite(enabledS , X[x 7→ a], X)              (X[x 7→ x] = X)
                        = vpJif (enabledS ) {S} else {skip}K(X)

   Case S = assert Y .

             vpJS̃K(X) = vpJassert ite(enabledS , Y , ∞)K(X)
                          = ite(enabledS , Y , ∞) ⊓ X
                          = ite(enabledS , Y ⊓ X, ∞ ⊓ X)
                          = ite(enabledS , Y ⊓ X, X)                   (∞ ⊓ X = X)
                          = vpJif (enabledS ) {S} else {skip}K(X)
42      P. Schröer et al.

     Case S = assume Y .

              vpJS̃K(X) = vpJassume ite(enabledS , Y , ∞)K(X)
                            = ite(enabledS , Y , ∞) → X
                            = ite(enabledS , Y → X, ∞ → X)
                            = ite(enabledS , Y → X, X)            (∞ → X = X)
                            = vpJif (enabledS ) {S} else {skip}K(X)

     Case S = reward a.

              vpJS̃K(X) = vpJreward ite(enabledS , a, 0)K(X)
                            = X + ite(enabledS , a, 0)
                            = ite(enabledS , X + a, X + 0)
                            = ite(enabledS , X + a, X)                (X + 0 = X)
                            = vpJif (enabledS ) {S} else {skip}K(X)

     Case S = coassert Y .

              vpJS̃K(X) = vpJcoassert ite(enabledS , Y , 0)K(X)
                            = ite(enabledS , Y , 0) ⊔ X
                            = ite(enabledS , Y ⊔ X, 0 ⊔ X)
                            = ite(enabledS , Y ⊔ X, X)                (0 ⊔ X = X)
                            = vpJif (enabledS ) {S} else {skip}K(X)

     Case S = coassume Y .

             vpJS̃K(X) = vpJcoassume ite(enabledS , Y , 0)K(X)
                            = ite(enabledS , Y , 0) ⇝ X
                            = ite(enabledS , Y ⇝ X, 0 ⇝ X)
                            = ite(enabledS , Y ⇝ X, X)             (0 ⇝ X = X)
                            = vpJif (enabledS ) {S} else {skip}K(X)□

   For the non-atomic statements, i.e. just the two nondeterminstic branches,
the tranformation introduces one variable for each branch. However, the case
where both branches are disabled (i.e. in a state σ where σ(enabledS1 ) = false
and σ(enabledS2 ) = false) does not correspond to a sub-program of the original
program. Therefore, our implementation explicitly keeps track of the additional
constraint that at least one branch must be enabled.

Theorem 30 (Soundness of Nondeterministic Choice Transformations
for Slicing). Let S̃ be the tranformed version of a HeyVL program S according
to Table 3. Let X ∈ E and σ be a program state. For the demonic choice S =
                          Diagnostics for Probabilistic Program Verification        43

if (⊓) {S1 } else {S2 }, we have:
                     
                     vpJS1 K(X)(σ)
                     
                     
                                        if σ(enabledS1 ) = true and σ(enabledS2 ) = false,
                     vpJS K(X)(σ)      if σ(enabledS1 ) = false and σ(enabledS2 ) = true,
                          2
vpJS̃K(X)(σ)   =
                     vpJSK(X)(σ)
                                       if σ(enabledS1 ) = true and σ(enabledS2 ) = true,
                     
                       ∞
                     
                                        if σ(enabledS1 ) = false and σ(enabledS2 ) = false.

Dually, for the angelic choice S = if (⊔) {S1 } else {S2 }, we have:
                     
                     
                      vpJS1 K(X)(σ)    if σ(enabledS1 ) = true and σ(enabledS2 ) = false,
                     
                     vpJS K(X)(σ)
                           2            if σ(enabledS1 ) = false and σ(enabledS2 ) = true,
vpJS̃K(X)(σ)   =
                     
                     
                      vpJSK(X)(σ)      if σ(enabledS1 ) = true and σ(enabledS2 ) = true,
                       0
                     
                                        if σ(enabledS1 ) = false and σ(enabledS2 ) = false.

Proof. Case S = if (⊓) {S1 } else {S2 }.

vpJS̃K(X) = vpJif (⊓) {assume ?(enabledS1 ); S1 } else {assume ?(enabledS2 ); S2 }K(X)
          = vpJassume ?(enabledS1 ); S1 K(X) ⊓ vpJassume ?(enabledS2 ); S2 K(X)
          = (?(enabledS1 ) → vpJS1 K(X)) ⊓ (?(enabledS2 ) → vpJS2 K(X))
          = ite(enabledS1 , vpJS1 K(X), ∞) ⊓ ite(enabledS2 , vpJS2 K(X), ∞) .

   Case S = if (⊔) {S1 } else {S2 }.

vpJS̃K(X) = vpJif (⊔) {coassume ?(¬enabledS1 ); S1 } else {coassume ?(¬enabledS2 ); S2 }K(X)
          = vpJcoassume ?(¬enabledS1 ); S1 K(X) ⊔ vpJcoassume ?(¬enabledS2 ); S2 K(X)
          = (?(¬enabledS1 ) ⇝ vpJS1 K(X)) ⊔ (?(¬enabledS2 ) ⇝ vpJS2 K(X))
          = ite(enabledS1 , vpJS1 K(X), 0) ⊔ ite(enabledS2 , vpJS2 K(X), 0) .□
44      P. Schröer et al.

B     Benchmarks
This section contains the detailed results of the benchmarks presented in Sec-
tion 5, and we also give sources and descriptions of the programs used in the
benchmarks. The benchmarks were executed on a 2021 Apple MacBook with an
M1 Pro chip and 16 GB of RAM.

Overview and Features. Erroring slices are handled in Section B.1 and verify-
ing (verification-witnessing and -preserving slices) are grouped in Section B.2.
Tables 5 and 6 show the results of different strategies for finding slices. For
each example program, we show a list of features that are present in the ex-
ample. Programs are either boolean (B) or probabilistic (P). We have programs
that reason about continuous sampling (C) taken from and using the technique
of [11]. Programs with recursion use the specification statement (S) as described
in Section 4.2. Programs with loops are marked by L, and here the Park in-
duction proof rule (Section 4.3) is used. Some examples make use of explicit
non-deterministic choices (N). Finally, we include programs that encode condi-
tioning/observations (O) using the definition of the conditional expected value
cwpJSK(X) = wpJSK(X)/wlpJSK(1) as described in [26].

Procs and Coprocs. In the examples below, we use Caesar’s syntax to declare
two kinds of procedures in HeyVL, proc and coproc. Both kinds of declarations
consist of a name, a list of input and output variables, and a pre X, a post Y , and
a body S. The only difference is that procs are required to verify (|= ⟨X⟩⪯ S ⟨Y ⟩)
and that coprocs are required to co-verify (|= ⟨X⟩⪰ S ⟨Y ⟩). These dual kinds
of specifications were introduced in Section 2.2.
    According to our theory, for slicing in procs, we select e.g. reductive state-
ments for slicing by default when slicing for errors. Dually, in coprocs, we select
extensive statements by default when slicing for errors. Similarly, we select ex-
tensive statements in procs by default when searching for verification-witnessing
slices, while dually in coproc we select reductive statements.

B.1   Results for Error-Witnessing Slices
The results for error-witnessing slices are shown in Table 5. list_access_error
is a simple boolean program to locate a possible out-of-bounds list access.
    The probabilistic program intro_error corresponds to Figure 3 and is based
on [44, Example 4.5]. The encoding has nondeterminism built-in to enable slicing
the branches of a probabilistic choice. We show the actual HeyVL code used for
our tool in Figure 16.
    The program leino05_1 is based on [34, Page 6]. The examples park_2,
park_3, and park_4 correspond to the first three rows of Table 4, all erroring
instances of a geometric loop instantiated from the template Figure 15.
    The examples condand, fcall, hyper, linear01, prdwalk, six_sided_die
and geo_recursive are examples of Park induction, conditioning, and recur-
sion from [49] and have been modified such that they do not verify anymore.
                               Diagnostics for Probabilistic Program Verification                 45


                              1   x := init_x;
                              2   cont := true;
                              3   @invariant(I)
                              4   while (cont) {
                              5      prob_choice :≈ flip(0.5);
                              6      if (prob_choice) {
                              7        cont := false
                              8      } else {
                              9        x := A
                             10      }
                             11   }


Fig. 15: Loop template S(A, I) with loop invariant I and assigning A to x in the
loop, which is verified against different upper bound specifications.


Table 4: Diagnostic messages on verifying different instantiations of the loop
template in Figure 15. The first two columns show whether the verification suc-
ceeds and the user diagnostics. Columns three and four contain the pre and post.
The final two columns give the invariant, and the assignment to x that is ap-
plied in every but the final loop iteration. The first case produces no diagnostic
messages as the program verifies and all assumptions are used.
  Diagnostic                              Pre X              Post Y    Invariant I            A
  Verified.                               ?(init_x ̸= 0) ⊔ 14 [x == 1] ite(cont, 12 [x == 1] + x + 1
                                                                      1
                                                                      4
                                                                        [x == 0] , [x == 1])
  Post is part of the error.               init_x + 1        x+1      ite(cont, x + 1, x) x + 1
  Pre might not entail the invariant.      0                 x        x                      1
  Invariant might not be inductive.        init_x + 1        x        x+1                    x+1
  While could be an if statement.          init_x + 1        x        ite(cont, x + 1, x) x + 1
  Invariant not necessary for inductivity. ?(true)           ?(¬cont) ?(cont)                x+1




The example six_sided_die is the erroring part of a (failing) two-part verifica-
tion of a program that simulates a fair six-sided die using conditioning, shown
in Figure 17. We show the example geo_recursive in Figure 18, whose re-
cursive procedure call is translated using the specification statement encoding
(Section 4.2).
    Finally, the examples irwin_hall16, monte_carlo_pi4, and tortoise_hare12
are HeyVL encodings of probabilistic programs with sampling from a continu-
ous distribution based on [11], modified to fail verification. All use the proof rule
of Park induction for a loop, and encode sampling statements from continuous
distributions as described in the above source. For the example irwin_hall16,
we show the HeyVL file used for our tool in Figure 19.
    In all of the above examples, our tool only selects reductive statements in
procs and dually extensive statements in coprocs for slicing (column 4, |S|). By
46     P. Schröer et al.




Table 5: Results of the two strategies for finding error-witnessing slices. The
column “LoC” shows the total lines of code in the program and |S| the num-
ber of potentially sliceable statements. For each strategy, the columns |S| and
t show the number of statements in the slice and the runtime in milliseconds,
respectively. Features: Boolean (B), Probabilistic (P), Continuous Sampling (C),
Specification statement/recursion (S), Loops (L), Non-determinism (N), and Ob-
servations/conditioning (O).
                                                    first     opt
             Program            Feat.    LoC |S|
                                                   |S|     t |S|   t
             list_access_error B           7   3     1     2 1     1
             intro_error       P, N       16   5     4     1 4     2
             leino05_1         B          13   2     1     1 1     1
             park_2            P, L       16   3     2     1 1     1
             park_3            P, L       16   3     2     1 1     1
             park_4            P, L       16   3     1     1 1     1
             condand           P, L       19   3     1     1 1     2
             fcall             P, L       21   3     2     1 1     2
             hyper             P, L       26   3     1     1 1     2
             linear01          P, L       18   3     1     1 0     1
             prdwalk           P, L       57   3     1     2 1     3
             six_sided_die     P, O       10   2     2     1 2     1
             geo_recursive     P, S       17   2     1     2 1     3
             irwin_hall16      P, L, C    13   3     1    22 1    24
             monte_carlo_pi4 P, L, C      16   3     2    11 1    24
             tortoise_hare12 P, L, C      31   4     2 10400 1 10400
                           Diagnostics for Probabilistic Program Verification   47

Theorem 7, we ensure that we obtain an error-witnessing slice. This behavior is
the default for programs that fail verification.


  1 coproc binary_sample_error () -> ( r : EUReal )
  2     pre 1/3
  3     post [ r >= 2]
  4 {

  5     var b0 : UInt
  6     var b1 : UInt
  7     var b2 : UInt
  8     var b3 : UInt
  9

 10         var choice : Bool = flip (0.5)
 11         if \ cup {
 12              coassume !?( choice ) ; b0 = 0
 13         } else {
 14              coassume !?(! choice ) ; b0 = 1
 15         }
 16

 17         choice = flip (0.5)
 18         if \ cup {
 19              coassume !?( choice ) ; b1 = 0 // the coassume is
                     sliced
 20         } else {
 21              coassume !?(! choice ) ; b1 = 1
 22         }
 23

 24         r = b0 + 2 * b1
 25   }


Fig. 16: HeyVL code for the probabilistic program intro_error, corresponding
to Figure 3. It does not verify, as 1/3 is not an upper bound for the probability
of r ≥ 2 on termination. Our tool slices the coassume statement in line 19, and
therefore it indicates that only the coassume statements in lines 12, 14, and 21
are relevant for the verification failure.




B.2       Results for Verifying Slices

Table 5 shows the results for verifying slices, separated by whether we are search-
ing for verification-preserving or -witnessing slices.

Verification-preserving slices. The first eight examples are from [8]. In particu-
lar, barros_program6 refutes the claim of theirs that forwards and backwards
reasoning is necessary to find minimal slices (their Program 6), as we explain in
48       P. Schröer et al.




    coproc die_wp () -> ( r :
     1                                       1 proc die_wlp () -> ( r :
        EUReal )                                   EUReal )
  2     pre 2.625                            2     pre 0.75
  3     post r                               3     post 1
  4 {                                        4 {

  5     var a : Bool = flip                  5     var a : Bool = flip
            (0.5)                                      (0.5)
  6     var b : Bool = flip                  6     var b : Bool = flip
            (0.5)                                      (0.5)
  7     var c : Bool = flip                  7     var c : Bool = flip
            (0.5)                                      (0.5)
  8     r = 4 * [a] + 2 * [b]                8     r = 4 * [a] + 2 * [b]
            + [c] + 1                                  + [c] + 1
  9     // changed from r <= 6               9      // changed from r <=
 10     assert ?( r <= 5)                               6
 11 }                                       10     assert ?( r <= 5)
                                            11 }

(a) HeyVL code to prove that wpJSK(r) ⪯
2.625. This verification succeeds, and    (b) HeyVL code to prove that
nothing is sliced.                        wlpJSK(r) ⪰ 0.75. This verification
                                          fails, and both the post and the assert
                                          statement are reported as part of the
                                          error.

Fig. 17: HeyVL code to check that cwpJSK(r) ⪯ 3.5 = 2.625/0.75 for the probabilis-
tic program six_sided_die, based on the decomposition of conditioning by [26].
The last assert statement models a conditioning statement, i.e. observe r ≤ 5
(changed from the correct r ≤ 6). The error report points to a failure of the wlp
part, and notices that both the post and the observe statement are relevant for
the failure.
                           Diagnostics for Probabilistic Program Verification      49




  1 coproc geo1 ( init_c : UInt , init_f : UInt ) -> ( c : UInt , f :
        UInt )
  2     pre [ init_f == 1] * ( init_c + 1) + [ init_f != 1] *
             init_c
  3     post c
  4 {

  5     var prob_choice : Bool
  6     c = init_c
  7     f = init_f
  8     if f != 1 { // it should be f == 1 in the verifying
             program
  9           prob_choice = flip (0.5)
 10           if prob_choice {
 11                f = 0
 12           } else {
 13                c = c + 1
 14           }
 15           c , f = geo1 (c , f ) // pre might not hold
 16     } else {}
 17 }




Fig. 18: HeyVL code for the probabilistic program geo_recursive, based on the
example from [49]. The procedure call in line 15 is encoded using a specification
statement, as described in Section 4.2. Our tool slices all but the coassume
statement in the specification statement encoding and therefore prints the error
message “pre might not hold”, located in line 15. In this case, slicing reveals that
the precondition of the recursive call is not satisfied, allowing the user to identify
a wrong conditional (line 8).
50       P. Schröer et al.




    coproc irwin_hall ( M : UReal ) -> ( x : UReal )
     1

     2  pre 0.531* M // changed pre so that pre might not
            entail invariant
  3     post x
  4 {

  5     x = 0
  6     var i : UReal = 1
  7     @invariant ( ite ( i <= M , ( x + 0.532*(( M - i ) + 1) ) , x ) )
  8     while i <= M {
  9         // var inc : UReal = unif [0 ,1]
 10         var inc : UReal ; var N : UInt = 16; var j : UInt
                = unif (0 , 15) ; cohavoc inc ; coassume ?!( j / N
                <= inc && inc <= ( j +1) / N )
 11         x = x + inc
 12         i = i + 1
 13     }
 14 }




Fig. 19: HeyVL code for the probabilistic program irwin_hall16, based on the
encoding of continuous sampling by [11]. Our tool reports that the “pre does not
entail the invariant”, based on slicing the encoding of Park induction (generated
by the @invariant annotation) and application of Theorem 21. This hints that
the invariant is correct, but that the pre is wrong (should be 0.532 · M instead
of 0.531 · M ).
                                   Diagnostics for Probabilistic Program Verification           51




Table 6: Results of the different strategies for finding verifying slices. The column
“LoC” shows the total lines of code in the program and |S| the number of po-
tentially sliceable statements. For each strategy, the columns |S| and t show the
number of statements in the slice and the runtime in milliseconds, respectively.
Features: Boolean (B), Probabilistic (P), Continuous Sampling (C), Specification
statement/recursion (S), Loops (L), Non-determinism (N).
                                                        core       mus       sus      e-f
                   Program           Feat. LoC |S|
                                                       |S|     t |S|     t |S|     t |S|    t


                   barros_program1 B        11     5    5 0 3 10            3 11 3 7
      preserving




                   barros_program2 B        11     4    4 0 2     9         2 10 3 6
                   barros_program3 B        11     5    5 0 3     9         3 11 5 7
                   barros_program4 B        17     8    5 0 2 10            2 14 4 6
                   barros_program5 B        16     7    4 0 2 10            2 13 3 7
                   barros_program6 B        10     4    3 0 1     9         1 10 3 6
                   barros_program7 B        9      3    2 0 2     9         2    9 2 6
                   barros_program8 B        14     4    3 0 3     9         3 10 4 7
                   navarro20_page31 B       18     7    4 0 2 10            2 12 3 6
                   gehr18_1          P      14     4    4 0 2     9         2    9 2 5
                   gehr18_2          P      14     4    4 0 2     9         2 12 2 6
                   gehr18_3          P      14     3    2 0 1     9         1    8 2 5
                   navarro20_ex4_3 P        12     3    3 0 1     8         1    9 2 5
                   navarro20_ex4_5 P        20    10   10 1 9 203           9 552 9 25
                   navarro20_ex5_8 P, L     32     5    5 20 5 3700         5 3690  -  -
                   navarro20_figure7 P      73    37   21 0 12 1370         -    - 13 21
                   navarro20_figure8 P      73    37   13 0 7 53            -    - 7 8
                   2drwalk           P, L   219   75   18 7 7 116           -    - 10 25
                   bayesian_network P, L    102   26    4 0 1 19            1 10 3 7
                   prspeed           P, L   40     9    6 1 6 25            6 67    -  -
                   rdspeed           P, L   43    11   10 2 8 61            8 226 8 15
                   rdwalk            P, L   19     5    4 0 3 11            3 12 3 11
                   sprdwalk          P, L   23     6    5 0 4 118           4 15 4 8
                   unif_gen4_wlp     P, L   123    7    5 58 3 1770         3 2560 3 191
                   burglar_alarm_wp P       35     4    4 0 1 10            1 11 2 6



                   park_1            P, L 16       3 3 0 3 11 3 10                    3 9
      witnessing




                   park_5            P, L 16       3 3 0 2        9 2     9           3 7
                   park_6            P, L 16       3 1 0 1        8 1     8           1 5
                   algorithm_r       P, L 16       4 4 105 3 125 3 132                3 18
                   bn_passified      P, N 47      25 17 370 10 3390 10 3810           -  -
52       P. Schröer et al.

Section 6. The HeyVL program used for the tool is shown in Figure 20. With
the same goal, program navarro20_page31 is based on the example from [44,
Page 31] and the HeyVL version is shown in Figure 21.
    The examples gehr18_1, gehr18_2, and gehr18_3 are based on Bayesian
networks encoded as probabilistic programs, from [20].
    The following examples 2drwalk, bayesian_network, prspeed, rdspeed,
rdwalk, sprdwalk, and unif_gen4_wlp are probabilistic programs from [49].
    All of the above examples have not been modified from their source, ex-
cept to add the necessary @slice_verify annotations to let our tool select the
assignments for slicing.

Verification-witnessing slices. The examples park_1, park_5, and park_6 cor-
respond to the instantiations of Figure 15 by the respective lines in Table 4.
algorithm_r corresponds to our Figure 5 and its HeyVL version is shown in
Figure 22. Finally, bn_passified is a simplified version of [44, Figure 7] with
the passification transformation applied, turning assignments into assumptions.
    For all of these examples, our tool automatically selects extensive statements
in procs and dually reductive statements in coprocs when slicing verifying pro-
grams. By Theorem 15, this ensures we obtain verification-witnessing slices.
Their number is reported in column 4, |S|.


    proc barros_program6 ( init_x : Int ) -> ( x : Int )
     1

     2  pre ?( true )
  3     post ?( x >= 100)
  4 {

  5     x = init_x
  6     @slice_verify {
  7         x = x * x
  8         x = x + 100
  9         x = x + 50 // this is sliced
 10     }
 11 }




Fig. 20: HeyVL code for the program barros_program6, corresponding to Fig-
ure 20 ([8, Program 6]). The @slice_verify annotation lets our tool select the
assignments for slicing. Our method can slice the last assignment, while the
forwards- or backwards-reasoning methods by Barros et al. cannot.
                         Diagnostics for Probabilistic Program Verification   53


  1 proc navarro_page31 ( init_x : Int , init_y : Int ) -> ( x : Int ,
         y : Int )
  2     pre ?( init_y > 0)
  3     post ?( x >= 0)
  4 {

  5     x = init_x
  6     y = init_y
  7     @slice_verify {
  8          if y > 0 {
  9                x = 100
 10                x = x + 50 // this is sliced
 11                x = x - 100 // this is sliced
 12          } else {
 13                x = x - 150 // this is sliced
 14                x = x - 100 // this is sliced
 15                x = x + 100 // this is sliced
 16          }
 17     }
 18 }




Fig. 21: HeyVL code for the program navarro20_page31 corresponding to the
example from [44, Page 31]. The @slice_verify annotation has Brutus select
the assignments for slicing. Our method can slice all marked statements, while
Navarro and Olmedo claim it needs both forwards and backwards reasoning.

  1 coproc algorithm_r_wrong ( n : UInt , x : UInt ) -> ( c : UInt )
  2     pre !?( n > 0 && n >= x && x >= 1)
  3     pre 1/ n
  4     post [ c == x ]
  5 {

  6     c = 0
  7     var i : UInt = 1
  8     @invariant ((1/ n ) * [ i <= x && x <= n ] + [ x == c ]) //
            while could be an if statement
  9     while i <= n {
 10         var prob_choice : Bool = flip (1/ n )
 11         if prob_choice {
 12              c = i
 13         } else {}
 14         i = i + 1
 15     }
 16 }




Fig. 22: HeyVL code for the program algorithm_r, corresponding to Figure 5.
After desugaring the annotated while loop according to the schema of Figure 12,
our tool determines the assumption (II) can be sliced. By Theorem 22, the tool
will print the message “While loop could be an if statement” to the user.
54                 P. Schröer et al.


                         core   mus                                                                   core    mus
                         sus    exists-forall                                                         sus     exists-forall


             OOR                                                                            OOR


              20                                                                            100%

                                                                                            80%
slice size




                                                                               slice size
              15
                                                                                            60%
              10
                                                                                            40%

               5
                                                                                            20%

               0                                                                             0%
                ≤1      101     102                      103     OOR                           ≤1     101     102     103        OOR

                          time in milliseconds                                                            time in milliseconds

(a) Absolute size of slices vs. computa-                                       (b) Relative size of slices, compared to
tion time.                                                                     total sliceable statements, vs. compu-
                                                                               tation time.

Fig. 23: Scatter plots showing the size of verifying slices computed by different
methods with the time needed (log scale). OOR represents computations that
did not finish within the timeout of 30 seconds.


                                                                  core   mus
                                                                  sus    exists-forall


                                                         OOR

                                                         100%
                                      relative removal




                                                         80%

                                                         60%

                                                         40%

                                                         20%

                                                          0%
                                                            ≤1    101    102           103          OOR

                                                                    time in milliseconds


Fig. 24: Scatter plot showing the ratio of statements removed from verifying slices
computed by different methods compared to the optimal slice computed by sus,
with the time needed (log scale). OOR represents computations that did not
finish within the timeout of 30 seconds.
