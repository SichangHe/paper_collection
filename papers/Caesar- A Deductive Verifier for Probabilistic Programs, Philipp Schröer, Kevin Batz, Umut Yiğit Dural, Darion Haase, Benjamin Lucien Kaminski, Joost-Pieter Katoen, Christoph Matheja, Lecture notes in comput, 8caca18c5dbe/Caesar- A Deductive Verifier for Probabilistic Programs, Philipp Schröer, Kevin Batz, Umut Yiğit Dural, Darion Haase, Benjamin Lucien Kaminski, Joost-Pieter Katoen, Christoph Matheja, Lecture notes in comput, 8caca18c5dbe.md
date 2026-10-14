                                                            Caesar: A Deductive Verifier
                                                             for Probabilistic Programs

                                             Philipp Schröer(B)1 , Kevin Batz2 , Umut Yiğit Dural1 , Darion Haase1 ,
                                               Benjamin Lucien Kaminski4,5 , Joost-Pieter Katoen1 , and Christoph
                                                                            Matheja3,6
                                                                  1
                                                                   RWTH Aachen University, Germany
arXiv:2605.15827v1 [cs.PL] 15 May 2026




                                                         {phisch, darion.haase, katoen}@cs.rwth-aachen.de
                                                                      umut.dural@rwth-aachen.de
                                                                        2
                                                                          Cornell University, USA
                                                                           k.batz@ucl.ac.uk
                                                                       3
                                                                          DTU Compute, Denmark
                                                                    4
                                                                       Saarland University, Germany
                                                                     kaminski@cs.uni-saarland.de
                                                                   5
                                                                      University College London, UK
                                                                 6
                                                                    University of Oldenburg, Germany
                                                                      christoph.matheja@uol.de



                                                 Abstract. Caesar is a deductive verifier for probabilistic programs. At
                                                 its core lies HeyVL, a quantitative intermediate verification language
                                                 based on the real-valued logic HeyLo. HeyVL allows users to express a
                                                 probabilistic program, its specifications, and proof rules in a programming-
                                                 language style, so that new proof rules can be easily integrated into the
                                                 verifier. Caesar translates HeyVL programs into verification conditions,
                                                 which are then checked using the Z3 SMT solver. It also includes a back-
                                                 end based on probabilistic model checking for a subset of HeyVL. We
                                                 report on the results of five years of development of Caesar, highlight-
                                                 ing its main features and architecture. In particular, we describe recent
                                                 improvements such as additional proof rules, a model-checking backend,
                                                 and better diagnostics.


                                         1      Introduction

                                         We present Caesar7 , an open-source deductive verifier for probabilistic programs,
                                         written in Rust. It is designed as verification infrastructure for a variety of prop-
                                         erties of probabilistic programs.

                                         Probabilistic programs. Probabilistic programs incorporate random choices whose
                                         outcomes can influence the control flow of loops and conditionals. For exam-
                                         ple, Figure 1 shows the bounded retransmission protocol [26] (BRP) with a
                                         noisy transmission channel, repeatedly trying to submit a number of packets with
                                         7
                                             https://www.caesarverifier.org
2        P. Schröer et al.


    1  @wp coproc brp ( packets : UInt , maxTries : UInt )
    2          -> ( sent : UInt , fail : UInt , totalFail : UInt )
     3     pre 1 - exp (1 - exp (0.01 , maxTries ) , packets )
     4     post [ fail == maxTries ]
     5 {

     6   sent = 0; fail = 0; totalFail = 0
     7   @invariant (...)
     8   while ( sent < packets && failed < maxTries ) {
     9     var transmit : Bool = flip (0.99)
    10     if transmit {
    11       sent = sent + 1; failed = 0
    12     } else {
    13       fail = fail + 1; totalFail = totalFail + 1 } } }


Fig. 1: Excerpt of HeyVL code modeling the bounded retransmission protocol.


maxTries attempts per packet before aborting. The program is written in HeyVL,
a quantitative verification-aware programming language, explained below.
    Design and verification objectives for probabilistic programs go beyond clas-
sical safety and liveness, and are quantitative rather than Boolean. For the
BRP, one may bound the failure probability, lower-bound successful transmis-
sions, or analyze expected runtime. Figure 1 checks the first: it specifies that
fail == maxTries holds on termination with probability at most 1 − (1 −
0.01maxTries )packets . The coproc keyword requests verification of an upper bound
(given by the pre) on the expected value of the postexpectation. Here, this post
is the condition fail == maxTries. To reason about the expected number of
failures instead, one would use the post fail. To obtain the expected value, we
use the weakest pre-expectation semantics [61], selected with the @wp annotation.
The while-loop needs a proof rule; here Park induction (@invariant(. . .)).

The Intermediate Verification Language HeyVL. To tackle the diversity of veri-
fication objectives and proof rules, Caesar uses the intermediate verification lan-
guage (IVL) HeyVL [73]. Similar to other IVLs such as Boogie [55], Why3 [31],
or Viper [66], it serves as a common language to express programs, specifica-
tions, and proof rules. HeyVL uses the real-valued logic HeyLo to express quanti-
tative specifications and verification conditions. Quantitative verification state-
ments such as assert and assume generalize classical Hoare-style assertions and
assumptions to the setting of expected values.

The Caesar Verifier. Main aspects of Caesar’s design are: (1) Probabilistic pro-
grams with R∞≥0 -valued specifications, (2) quantitative verification statements to
encode a range of proof rules (e.g., inductive rules for reasoning about loops),
and (3) duality of constructs for reasoning about lower and upper bounds of
expected values. Prior work has formalised this perspective [73].
                                                                        Caesar          3

                                                               Caesar
                                 Quantifier                                ✓ Verified
                                Elimination
 Probabilistic
  Program                                                               × Counterexample
                   Slicing          HeyLo            SMT-LIB    Z3
                                G            VC
                             VC                                            ? Unknown
 Specification                              valid?
                   HeyVL
                                                                        Expected Values
 Proof Rules                                          JANI     Storm


                 Fig. 2: Logical architecture of the Caesar verifier.


    Figure 2 shows the logical architecture of Caesar. The input to Caesar is a
HeyVL program consisting of a probabilistic program, a specification (quantita-
tive pre- and post-conditions), and proof rules to be used during verification,
e.g., loop invariants for while-loops. Specific diagnostics about either success-
ful or failed verification attempts are based on the HeyVL program, and will be
provided by the slicing component (Section 5.4).
    The verification condition generator (VCG) generates expressions in the
HeyLo logic, whose validity implies correctness of the HeyVL program w.r.t. its
specifications. For dispatching the validity check to a solver, an important opti-
mization is the quantifier elimination component which tries to remove (quan-
titative) quantifiers in the verification conditions. Finally, validity is checked by
translating the HeyLo validity problem into an input to the SMT solver Z3 [27],
following the SMT-LIB standard [12]. Outputs may be either successful verifi-
cation, a counterexample, or an unknown result if the solver cannot decide the
validity. We give more details on these components in Section 4.1.
    Caesar also includes a translation from a subset of HeyVL to the JANI mod-
eling language [23] for probabilistic models, which can be used to calculate ex-
pected values of probabilistic programs via the Storm model checker [37]. More
details on this backend are given in Section 4.2.

Contributions. In this tool paper, we report on the current state of Caesar and
focus on application and implementation aspects and features. Compared to the
first publication with Caesar [73], new features presented here include additional
built-in proof rules (Section 2.3), support for limited functions and much im-
proved quantifier handling (Section 4.1), a model checking backend via JANI/S-
torm (Section 4.2), a novel Visual Studio Code extension (Section 5.2), semantic
guardrails to prevent unsound combinations of proof rules (Section 5.3), and
better diagnostics via program slicing (Section 5.4, [74]).


2    Verifying Probabilistic Programs

Caesar’s input language HeyVL supports different program models and verifica-
tion objectives and allows specifying proof rules that should be applied to enable
automated verification.
4         P. Schröer et al.

2.1     Objectives

HeyVL is designed with reasoning about expected values (random variables) of
probabilistic programs as the core primitive. Verification is structured around
(co-)procedures. Each unit of verification, either a proc or a coproc, can be
specified with quantitative analogues of pre- and post-conditions (pre and post
for short) – generalizing classical Hoare logic specifications. A proc is used to
verify lower bounds (LB) on expected values and checks whether the expected
value of the post after termination is at least the pre’s value before execution.
Dually, a coproc verifies upper bounds (UB) on expected values, i.e., whether the
expected value of the post after termination is at most the pre’s value before
execution.
    Focusing on expected values makes HeyVL versatile, as many quantitative
objectives can be reduced to expected value reasoning, including:

    – Probabilities of events and cumulative distribution functions (CDFs) can be
      encoded as expected values of indicator functions.
    – Almost-sure termination (AST) is defined as termination with probability 1.
    – Expected runtimes and positive almost-sure termination (PAST) can be han-
      dled by verifying that the expected runtime is finite.

The above includes partial- and total correctness of probabilistic programs. Cae-
sar also supports reasoning about discounted expected values, as well as quanti-
tative reachability properties including the number of visits, time to first visit,
and return times to designated locations [75]. Some relational properties, like
probabilistic sensitivity [4] (the change in expected output value w.r.t. a change
in input value), are also expressible.


2.2     Models

HeyVL can express a wide range of probabilistic programs with infinite state
spaces. Program variables can be of various types, including Booleans, (un)bound-
ed integers, (extended, un)bounded reals, and lists. User-defined types can be
specified using domain declarations with uninterpreted functions and axioms.
   HeyVL is an imperative language that supports sampling from discrete distri-
butions, and binary (and unbounded) angelic (maximizing) and demonic (min-
imizing) non-determinism. Both kinds of non-determinism can be mixed in the
same program, allowing users to encode simple/two-player stochastic games [59].
Possibly unbounded loops, recursion and conditioning are not part of the core
of HeyVL, but users can analyze them via proof rules.


2.3     Proof Rules

Users specify their models and objectives w.r.t. a reference semantics. A ref-
erence (expectation-based) semantics for loops or recursion is defined using
least or greatest fixed points (lfp/gfp) and specified using an annotation on
                                                                       Caesar         5

                                         Verification
           Lower Bound (proc)                              Under-approximation
                                            Refutation

                                             Refutation
          Upper Bound (coproc)                              Over-approximation
                                         Verification

Fig. 3: Overview of which approximation of the reference semantics to use when
aiming to verify/refute a lower/upper bound.


the proc/coproc (Caesar supports weakest pre (@wp), weakest liberal pre (@wlp)
(cf. [43]), expected runtimes (@ert) [46], or conditional weakest pre (@cwp) [69]).
     To automatically verify properties of probabilistic programs, users are re-
quired to approximate the semantics through proof rules. Caesar includes a range
of rules for loops that are used by adding loop annotations. Proof rules are clas-
sified as under-approximating (Under) or over-approximating (Over) w.r.t. the
reference semantics.8 This allows Caesar to support both sound proofs (verifying
that a property holds) and sound refutations (verifying that a property does
not hold). The various combinations of approximations and lower/upper bounds
give rise to different soundness guarantees for proofs and refutations, as summa-
rized in Figure 3. Unsound results due to invalid combinations of proof rules are
marked by Caesar. Table 1 summarizes proof rules applied with Caesar so far.
     For example, in Figure 1 we Over-approximate the (lfp-based) wp semantics
with the @invariant(· · ·) proof rule, i.e., the failure probability computed by
Caesar is at most the actual failure probability of the BRP. By using the proof
rule in a coproc, the upper bound given as pre holds for the BRP if Caesar proves
this upper bound on the computed failure probability (sound proofs). Dually, if
one wants to refute an upper bound, one needs to use an Under-approximating
proof rule, e.g., @unroll(· · ·) . Then, a counterexample provided by Caesar is
valid for the original program too (sound refutations).


3     Embedding Verification Techniques in Caesar via HeyVL

HeyVL [73] is a quantitative intermediate verification language tailored to prob-
abilistic programs. This allows users to extend Caesar’s applicability beyond the
natively supported language features by manually encoding approximations of
the original semantics via verification statements. For instance, Caesar has been
applied in this manner to programs with continuous distributions [20] and dis-
tributed randomized algorithms [28].
8
    A proof rule is Under-approximating if the expected value obtained from the proof
    rule is at most the expected value obtained from the reference semantics, and dually
    for Over-approximating proof rules.
6          P. Schröer et al.


Table 1: Overview of proof rules in Caesar. The syntactic sugar for built-in proof
rules is given in parentheses.
    Semantics        Approx.      Applicable Proof Rule
    lfp              Over         Park induction [70, 43] (@invariant(. . .))
                                  Latticed k-induction [17] (@k induction(. . .))
                                  Positive almost-sure termination [24, 32, 43] (@past(. . .))
                     Under        Finite loop unrolling [17] (@unroll(. . .))
                                  ω-invariants [43] (@omega invariant(. . .))
                                  Optional stopping theorem [36] (@ost(. . .))
                                  Almost-sure termination [60] (@ast(. . .))
                                  Lower bounds for possibly divergent loops [29]
                                  Weakly-fair AST [28]
    gfp              Over         Finite loop unrolling [17] (@unroll(. . .))
                                  ω-invariants [43] (@omega invariant(. . .))
                     Under        Park induction [70, 43] (@invariant(. . .))
                                  Latticed k-induction [17] (@k induction(. . .))
    both             Over/Under   Riemann sums for continuous distributions [20]



3.1       HeyVL as a Quantitative Intermediate Verification Language

HeyVL provides verification statements such as assert and assume, which gen-
eralize classical Hoare-style assertions and assumptions to quantitative reasoning
about expected values. The core language of HeyVL deliberately excludes loops
and recursion; instead, these constructs are supported by encoding proof rules
using verification statements. This design makes the verifier extensible, enables
compositional use of proof rules, and allows front-ends to benefit directly from
improvements in the verification backends.

Expectation Transformer Semantics. HeyVL’s verification pre-expectation (vp)
semantics is defined as a syntactic transformation of quantitative formulas in the
real-valued logic HeyLo. The vp semantics is a backwards-moving denotational
semantics in the style of weakest pre-expectation semantics [61, 43]. Through
quantitative assertions and assumptions Caesar also encodes the program’s spec-
ification (pre and post) in the generated formula. The (Boolean) verification
condition, i.e., the formula representing the correctness of a HeyVL program
w.r.t. its specification, is the condition that the HeyLo formula from the vp com-
putation is valid. This is the basis for Caesar’s SMT backend (Section 4.1).

Operational Semantics. An operational semantics in terms of refereed stochastic
games has been defined for HeyVL [59]. It provides a small-step, game-based
ground truth that validates the intuition behind the verification statements and
proves equivalence to the weakest pre-expectation style semantics. For a subset
of HeyVL, the semantics yield finite-state Markov Decision Processes (MDPs),
amenable to probabilistic model checking (Section 4.2).
                                                                         Caesar         7

3.2     HeyLo: An Assertion Language for Probabilistic Programs
HeyLo [73] is a real-valued logic for the verification of probabilistic programs. It
generalizes (Boolean) first-order logic to the non-negative extended reals (R∞  ≥0 ).
We use it (1) as a quantitative assertion language to express specifications, and
(2) to reduce many verification problems to validity checking in this logic. For (1),
HeyLo was designed as an extension of the assertion language by Batz et al. [19],
which is relatively complete for the verification of probabilistic programs. For (2),
HeyLo is a first-order logic to simplify automation using SMT solvers, and quan-
titative implications and their dual coimplications allow encoding inequalities
between expected values.


4     Verification Backends
4.1     Verification Condition Generation
Caesar’s main backend is based on encoding verification conditions into HeyLo
and checking them using the SMT solver Z3 [27]. At the top level, the verification
condition generator (VCG) generates a HeyLo formula based on the backwards-
moving vp semantics (Section 3.1).
Lazy Unfolding. We use a representation with explicit substitutions and shared
references to sub-expressions to avoid exponential blow-up in the size of the
generated formula. Caesar unfolds this formula lazily: it is traversed while keep-
ing track of currently true Boolean conditions and pruning unreachable sub-
expressions.9 The required satisfiability checks are discharged by a number of
lightweight SMT queries. The result is an equivalent HeyLo formula that is often
much smaller than the naively generated one. This is an important optimization,
since the generated formulas can be very large due to (non-)deterministic, and
probabilistic branching in the program.
Optimizations. Afterwards, Caesar applies quantifier elimination (QE) on HeyLo
formulas, where HeyLo quantifiers correspond to infima and suprema over non-
negative extended reals. QE shifts quantifiers outwards as much as possible, and
then eliminates top-level quantifiers while preserving validity. Removing a quan-
tifier introduces new fresh variables. This procedure is not complete and may fail
to eliminate some quantifiers, but is crucial for practical performance. Fragments
of HeyLo and corresponding HeyVL programs have been identified where QE is
complete [71, Section 4.2]. Various other optimizations are implemented, such
as replacing quantitative logical operators with Boolean ones where possible.
SMT Encoding. The HeyLo formula is translated into an input formula for Z3,
making heavy use of Z3’s support for real arithmetic. To encode an expression
of type R∞ ≥0 , we represent it as a pair (r, isInfty), where r is a real number and
9
    This can be seen as a form of (forwards-moving) symbolic execution, as in KeY [5],
    cf. [35, Section 6.3.4]. In particular, we enjoy (Boolean) forwards reasoning without,
    e.g., a probabilistic strongest post-expectation semantics, which has been shown to
    be impossible to define for probabilistic programs [42, p. 135].
8       P. Schröer et al.

isInfty is a Boolean flag that is true if and only if the represented number is equal
to ∞. We add constraints r ≥ 0 to ensure that r is non-negative. All operations
on R∞ ≥0 are then defined over such pairs.
     Caesar supports a number of different encodings for recursive uninterpreted
functions declared in domains, which can be selected based on the verification
task at hand [21]. We support the naive axiomatic encoding, where axioms spec-
ify the function’s behavior, as well as SMT-LIB’s define-fun-rec definitions.
The decreasing encoding uses patterns on quantifiers to guide Z3’s e-matching
algorithm for quantifier reasoning. Built on this, we have different variants of
fuel ed function encodings, which limit the depth of recursion during SMT solv-
ing by tracking a fuel value that bounds the allowed recursive unfoldings of the
function. These different implementations allow users to trade off soundness of
proofs and refutations, as well as completeness of verification.
Slice Solvers. Diagnostics in Caesar (Section 5.4) are based on computing slices of
a HeyVL program [74]. To this end, Caesar implements the first semantic slicing
engine for probabilistic programs through dedicated slice solvers that operate
directly on the generated HeyLo verification condition. These solvers repeatedly
invoke the SMT solver to search for slices that either still verify or admit a coun-
terexample. Caesar additionally supports minimization of slices. We implement
a variant of the algorithm by Liffiton and Malik [57] for computing minimum
unsatisfiable subsets (MUSes), sped up by exploiting polarity-like information
such as whether one slices assertions (positive), assumptions (negative), or as-
signments (mixed).
Completeness. No verifier can be complete for all probabilistic programs. For in-
stance, deciding almost-sure termination is known to be even more undecidable
than the Halting Problem for classical programs [44]. However, we obtain spe-
cific completeness results. For so-called linear programs and linear expectations,
with the @unroll(· · ·), @invariant(· · ·) and @k induction(· · ·) proof rules, ver-
ification is decidable for similar reasons as in [17, Section 7].

4.2   Probabilistic Model Checking
Caesar includes a probabilistic model checking backend that compiles a subset
of HeyVL with loops, called executable HeyVL, to Markov Decision Processes
(MDPs). In contrast to the VCG backend, this translation ignores proof rule
annotations and instead encodes the program’s operational semantics directly as
an MDP with rewards. The resulting model is expressed in the JANI format [23]
and expected values can be calculated with probabilistic model checkers such
as Storm [37]. Since Storm operates on finite-state MDPs, infinite-state HeyVL
programs require techniques like partial exploration [22] to obtain lower or upper
bounds on expected values.

5     UI/UX: Design Principles and Tool Support
Quantitative deductive verification poses distinct usability challenges: verifica-
tion pre-expectations are non-Boolean, failures may be approximation-induced,
                                                                     Caesar          9




(a) Identifying a non-inductive invariant.     (b) Inline verification conditions.

     Fig. 4: Caesar’s VSCode extension providing diagnostics and explanations.


and counterexamples can be semantically spurious. Caesar’s UI/UX is designed
to make these issues explicit, guide users away from unsound reasoning, and
shorten the verification feedback loop. Features are explained in detail in the
extensive documentation10 .


5.1     Installation and Command-Line Interface

Caesar is distributed as a single binary for Windows, Mac, and Linux. This makes
installation and usage easy, as no dependencies need to be installed separately.
The command-line interface contains many options to customize verification
runs. In particular, users can configure the backends extensively, e.g., adjusting
different SMT encoding aspects. These options and flags along with their chosen
defaults make design choices explicit to users, while still allowing for experimen-
tation when new features are added.


5.2     Interactive Verification Environment

Caesar comes with a dedicated extension for Visual Studio Code (VSCode) based
on the Language Server Protocol (LSP). This extension provides syntax high-
lighting, code snippets, and the ability to verify HeyVL files directly from the
editor on file save or on command. It also supports automatic installation and
updates of the Caesar binary. Verification results are shown in the gutter line
and inline in the editor (Figure 4a), and with diagnostics such as errors and
warnings displayed in the code and in the ”Problems” menu in VSCode. The
extension also provides inline explanations of computed verification conditions
(Figure 4b), helping users understand the verification process.
10
     https://www.caesarverifier.org/docs/
10      P. Schröer et al.

5.3   Semantic Guardrails

While Caesar allows arbitrary combinations of procedure kinds, original seman-
tics, and proof rules, not all combinations are sound (Section 2.3). We imple-
mented diagnostics called semantic guardrails that help users avoid unsound
combinations, and give diagnostics about guaranteed soundness of proofs and
refutations.


5.4   Diagnostics: Localization and Hints

Caesar tracks source-level provenance throughout the verification pipeline, allow-
ing failed verification conditions in HeyLo to be mapped back to the originating
HeyVL statements. In the probabilistic setting, a single counterexample may re-
quire multiple assertions along different execution paths. Due to the QE, we often
obtain sound counterexamples from Z3 for the verification condition. Therefore,
Caesar soundly localizes sets of contributing verification statements.
    A diagnostic then might indicate that an invariant is not inductive (seen
in Figure 4a) or that a pre is too weak. In addition, Caesar can give hints for
verifying programs, e.g., that a loop can be replaced with a simple if statement.
This might alert the user to potential issues such as dead code or that the
specification is too weak to require a loop. Diagnostics are based on computing
slices of a HeyVL program [74] that either preserve verification or refutation of
the original program.


5.5   User Experiences and Evaluation

In addition to the applications in academic research mentioned above, Caesar
was used at the Summer School on Formal Techniques in 2025 with ≈ 60 stu-
dents, as well as two iterations of a Probabilistic Programming lecture with ≈ 80
students each in the years 2024 and 2025. Students informally reported that
Caesar’s UI was helpful for learning probabilistic verification concepts and that
the diagnostics helped them understand verification failures.
    Caesar was successfully applied to a number of case studies, showing its useful-
ness and versatility as a probabilistic verification platform. For Rabin’s mutual
exclusion protocol [52], Caesar can refute bounds on success probabilities via
bounded model checking, or prove exact success probabilities through a combi-
nation of proof rules [73]. On a parametrized version of the bounded retrans-
mission protocol [26], symbolic bounds on quantitative properties were shown
in [41]. Almost-sure termination of random walks was shown with the built-in
proof rule of [60], while bounds on their expected runtime are obtained using
an encoding of the expected runtime calculus ert [46]. Bounds on the expected
value of a variable sampled from the Irwin-Hall distribution are shown in [20].
The almost-sure termination of, e.g., Ben-Or’s distributed consensus protocol
under weakly-fair scheduling was shown with Caesar in [28] by encoding the
application of their new proof rule.
                                                                    Caesar        11

    A quantitative evaluation was given in [73], comparing different programs
and features and showing, e.g., runtimes of Caesar. An evaluation of the slicing
component was done in [74], reporting on the overhead introduced by slicing to
obtain diagnostics. On most of the considered test cases, verification is almost
instant, indicating that Caesar is suitable for probabilistic program verification in
an interactive setting. However, since the complexity of the verification problem
highly depends on the program, specification, and proof rule at hand, perfor-
mance of deductive verification is highly problem-specific and thus difficult to
usefully compare in a comprehensive way. Due to the lack of a stable benchmark
suite for deductive probabilistic verification, we therefore do not include another
empirical evaluation. Establishing a suitable benchmark set is an important step
for future work.


6   Related Work

Deductive Verification. Classical IVLs like Boogie [55], Why3 [31], or Viper [66]
focus on verification of lower bounds on Boolean predicates. They are the foun-
dation for various verifiers, such as Dafny [54], Frama-C [49], or Prusti [8],
which reason about partial correctness of loops with invariants and allow termi-
nation proofs through variants. In comparison, Caesar has a variety of built-in
proof rules for probabilistic loop analysis, supporting expectation-based reason-
ing about upper and lower bounds.
    Dafny-VMC [78] adds distribution-based reasoning about probabilistic sam-
plers to Dafny by encoding probabilistic computations as transformations of
random bitstreams. Building on Why3, StatWhy [48] verifies programs that
perform statistical hypothesis testing using a program logic with modal operators
to represent beliefs. In contrast, Caesar uses a quantitative logic that natively
allows reasoning about expected values. As stated in [15], a detailed comparison
of these approaches is difficult.

Probabilistic Program Verification. Probabilistic model checkers like Storm [37]
and PRISM [53] provide automated verification for finite state probabilistic
models through exhaustive state-space exploration, whereas Caesar’s deductive
approach can provide symbolic guarantees on unbounded domains.
    Different expectation-based verification approaches [50, 51, 61, 45] have been
formalized by [40, 38] in Isabelle/HOL [68]. Their focus lies on individual for-
malizations of the calculi’s meta theory, while Caesar aims to provide a unifying
infrastructure for many verification techniques.
    The theorem prover EasyCrypt [13] is tailored to the verification of crypto-
graphic algorithms. It has been extended with several program logics, including
an assertion-based logic Ellora [15] with predicates over (sub)distributions,
and an expectation-based logic eHL [9] for upper bounds. They do not support
recursion, conditioning and general non-determinism. Existing formalizations of
probabilistic program semantics by [2] in the theorem prover Rocq, and by [76]
in Lean also do not support non-determinism or unbounded iteration.
12      P. Schröer et al.

    There is a wide range of automatic analysis tools which focus on certain pro-
gram properties, e.g., inferring bounds on (moments of) final distributions [33,
65, 77, 39, 34], bounding expected runtimes [62, 10, 56, 67] or proving (positive)
almost-sure termination [64, 63, 58, 1]. These methods often work on restricted
language fragments. An integration with Caesar, analogous to the Storm back-
end, could be useful to reduce the manual verification effort (where applicable).
Similarly, synthesis approaches like [11, 16, 7, 30, 25, 47, 14, 6, 18, 3] that auto-
matically find, e.g., invariants, can be used to instantiate proof rules and verify
programs with Caesar.



7    Conclusion and Future Work

Caesar is a deductive verifier for probabilistic programs based on the intermediate
verification language HeyVL. HeyVL supports reasoning about both lower and up-
per bounds on expected values, and through quantitative verification statements
enables users to encode a wide range of proof rules. The verification condition
generator translates HeyVL programs into verification conditions in the HeyLo
logic, which are then checked by the SMT solver Z3. Caesar also includes a proba-
bilistic model checking backend that translates a subset of HeyVL programs into
MDPs for expected value computation via probabilistic model checking. Caesar
includes several usability features, including diagnostics for error localization,
hints, and to prevent unsound reasoning.
    In future work, we plan to incorporate invariant synthesis approaches into
Caesar to ease the verification process. This includes classical approaches de-
scribed in Section 6 and LLM-assisted invariant discovery. Transpiling code from
other probabilistic programming languages for verification with Caesar, or tran-
spiling verified HeyVL code to obtain executable, correct programs, are further
efforts that will expand the tool’s applicability and allow usage within existing
software projects. To apply Caesar in larger software projects (in particular in
machine learning), we foresee challenges due to the heavy reliance on sampling
from continuous distributions. Therefore, we plan to develop an extended stan-
dard library of (continuous) distributions and data structures. Finally, establish-
ing a standard benchmark suite for deductive probabilistic program verification
will allow for comparisons across tools and techniques.



Data-Availability Statement

The tool Caesar, its VSCode extension, as well as benchmark programs that
were submitted for the artifact evaluation are publicly available on Zenodo [72].
We also develop our tools as open-source software at https://github.com/
moves-rwth/caesar.
                                                                      Caesar        13

Acknowledgments

This work was partially supported by the ERC POC Grant VERIPROB (grant
no. 101158076), the Research Training Group 2236 UnRAVeL (project number
282652900), DFF-1 project AuRoRa, and by the European Union’s Horizon 2020
research and innovation programme under the Marie Sklodowska-Curie grant
agreement MISSION (grant no. 101008233). We thank Emil Beothy-Elo, Franka
van Jaarsveld, and Se Rin Yang for their contributions to Caesar. We thank
Alexander Bork and Tobias Winkler for their feedback on an early draft.


Disclosure of Interests. The authors have no competing interests to declare
that are relevant to the content of this article.


References
1. Abate, A., Giacobbe, M., Roy, D.: Learning Probabilistic Termination Proofs.
   In: Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification - 33rd Interna-
   tional Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part
   II. LNCS, vol. 12760, pp. 3–26. Springer, Heidelberg (2021). https://doi.org/
   10.1007/978-3-030-81688-9_1
2. Affeldt, R., Cohen, C., Saito, A.: Semantics of Probabilistic Programs Using s-
   Finite Kernels in Dependent Type Theory. ACM Trans. Probab. Mach. Learn.
   1(3) (2025). https://doi.org/10.1145/3732291
3. Agrawal, S., Chatterjee, K., Novotný, P.: Lexicographic ranking supermartingales:
   an efficient approach to termination of probabilistic programs. Proc. ACM Pro-
   gram. Lang. 2(POPL), 34:1–34:32 (2018). https://doi.org/10.1145/3158122
4. Aguirre, A., Barthe, G., Hsu, J., Kaminski, B.L., Katoen, J., Matheja, C.: A
   pre-expectation calculus for probabilistic sensitivity. Proc. ACM Program. Lang.
   5(POPL), 1–28 (2021). https://doi.org/10.1145/3434333
5. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H., Ulbrich, M. (eds.):
   Deductive Software Verification - The KeY Book - From Theory to Practice.
   Springer (2016)
6. Amrollahi, D., Bartocci, E., Kenison, G., Kovács, L., Moosbrugger, M., Stankovic,
   M.: Solving Invariant Generation for Unsolvable Loops. In: Singh, G., Urban, C.
   (eds.) Static Analysis - 29th International Symposium, SAS 2022, Auckland, New
   Zealand, December 5-7, 2022, Proceedings. LNCS, vol. 13790, pp. 19–43. Springer,
   Heidelberg (2022). https://doi.org/10.1007/978-3-031-22308-2_3
7. Andriushchenko, R., Ceska, M., Junges, S., Katoen, J., Stupinský, S.: PAYNT:
   A Tool for Inductive Synthesis of Probabilistic Programs. In: Silva, A., Leino,
   K.R.M. (eds.) Computer Aided Verification - 33rd International Conference, CAV
   2021, Virtual Event, July 20-23, 2021, Proceedings, Part I. LNCS, pp. 856–869.
   Springer, Heidelberg (2021). https://doi.org/10.1007/978-3-030-81685-8_40
8. Astrauskas, V., Müller, P., Poli, F., Summers, A.J.: Leveraging Rust Types for
   Modular Specification and Verification. In: Object-Oriented Programming Sys-
   tems, Languages, and Applications (OOPSLA), 147:1–147:30. ACM (2019). https:
   //doi.org/10.1145/3360573
14      P. Schröer et al.

 9. Avanzini, M., Barthe, G., Grégoire, B., Moser, G., Vanoni, G.: Hopping Proofs of
    Expectation-Based Properties: Applications to Skiplists and Security Proofs. Proc.
    ACM Program. Lang. 8(OOPSLA1), 784–809 (2024). https://doi.org/10.1145/
    3649839
10. Avanzini, M., Moser, G., Schaper, M.: A modular cost analysis for probabilistic
    programs. Proc. ACM Program. Lang. 4(OOPSLA), 172:1–172:30 (2020). https:
    //doi.org/10.1145/3428240
11. Avanzini, M., Moser, G., Schaper, M.: Automated Expected Value Analysis of Re-
    cursive Programs. Proc. ACM Program. Lang. 7(PLDI), 1050–1072 (2023). https:
    //doi.org/10.1145/3591263
12. Barrett, C., Fontaine, P., Tinelli, C.: The Satisfiability Modulo Theories Library
    (SMT-LIB), (2016). https://smt-lib.org
13. Barthe, G., Dupressoir, F., Grégoire, B., Kunz, C., Schmidt, B., Strub, P.: Easy-
    Crypt: A Tutorial. In: Aldini, A., López, J., Martinelli, F. (eds.) Foundations of
    Security Analysis and Design VII - FOSAD 2012/2013 Tutorial Lectures. LNCS,
    pp. 146–166. Springer, Heidelberg (2013). https://doi.org/10.1007/978-3-319-
    10082-1_6
14. Barthe, G., Espitau, T., Fioriti, L.M.F., Hsu, J.: Synthesizing Probabilistic In-
    variants via Doob’s Decomposition. In: Chaudhuri, S., Farzan, A. (eds.) Com-
    puter Aided Verification - 28th International Conference, CAV 2016, Toronto,
    ON, Canada, July 17-23, 2016, Proceedings, Part I. LNCS, vol. 9779, pp. 43–61.
    Springer, Heidelberg (2016). https://doi.org/10.1007/978-3-319-41528-4_3
15. Barthe, G., Espitau, T., Gaboardi, M., Grégoire, B., Hsu, J., Strub, P.: An Assertion-
    Based Program Logic for Probabilistic Programs. In: Ahmed, A. (ed.) Program-
    ming Languages and Systems - 27th European Symposium on Programming, ESOP
    2018, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings.
    LNCS, pp. 117–144. Springer, Heidelberg (2018). https://doi.org/10.1007/978-
    3-319-89884-1_5
16. Batz, K., Chen, M., Junges, S., Kaminski, B.L., Katoen, J., Matheja, C.: Prob-
    abilistic Program Verification via Inductive Synthesis of Inductive Invariants. In:
    TACAS (2). LNCS, vol. 13994, pp. 410–429. Springer, Heidelberg (2023). https:
    //doi.org/10.1007/978-3-031-30820-8_25
17. Batz, K., Chen, M., Kaminski, B.L., Katoen, J., Matheja, C., Schröer, P.: Latticed
    k-Induction with an Application to Probabilistic Programs. In: Silva, A., Leino,
    K.R.M. (eds.) Computer Aided Verification - 33rd International Conference, CAV
    2021, Virtual Event, July 20-23, 2021, Proceedings, Part II. LNCS, vol. 12760,
    pp. 524–549. Springer, Heidelberg (2021). https://doi.org/10.1007/978- 3-
    030-81688-9_25
18. Batz, K., Junges, S., Kaminski, B.L., Katoen, J., Matheja, C., Schröer, P.: PrIC3:
    Property Directed Reachability for MDPs. In: CAV (2). LNCS, vol. 12225, pp. 512–
    538. Springer, Heidelberg (2020). https://doi.org/10.1007/978-3-030-53291-
    8_27
19. Batz, K., Kaminski, B.L., Katoen, J., Matheja, C.: Relatively complete verification
    of probabilistic programs: an expressive language for expectation-based reasoning.
    Proc. ACM Program. Lang. 5(POPL), 1–30 (2021). https://doi.org/10.1145/
    3434320
20. Batz, K., Katoen, J., Randone, F., Winkler, T.: Foundations for Deductive Ver-
    ification of Continuous Probabilistic Programs: From Lebesgue to Riemann and
                                                                    Caesar        15

    Back. Proc. ACM Program. Lang. 9(OOPSLA1), 421–448 (2025). https://doi.
    org/10.1145/3720429
21. Beothy-Elo, E.: Effective quantifier-based reasoning for quantitative deductive ver-
    ification. MA thesis, RWTH Aachen University, Aachen (2025). https://doi.org/
    10.18154/RWTH-2025-07050. https://publications.rwth-aachen.de/record/
    1016969.
22. Brázdil, T., Chatterjee, K., Chmelik, M., Forejt, V., Kretı́nský, J., Kwiatkowska,
    M., Meggendorfer, T., Parker, D., Ujma, M.: Learning Algorithms for Verification
    of Markov Decision Processes. TheoretiCS 4 (2025). https://doi.org/10.46298/
    THEORETICS.25.10
23. Budde, C.E., Dehnert, C., Hahn, E.M., Hartmanns, A., Junges, S., Turrini, A.:
    JANI: Quantitative Model and Tool Interaction. In: Legay, A., Margaria, T. (eds.)
    Tools and Algorithms for the Construction and Analysis of Systems - 23rd Interna-
    tional Conference, TACAS 2017, Held as Part of the European Joint Conferences
    on Theory and Practice of Software, ETAPS 2017, Uppsala, Sweden, April 22-29,
    2017, Proceedings, Part II. LNCS, vol. 10206, pp. 151–168. Springer, Heidelberg
    (2017). https://doi.org/10.1007/978-3-662-54580-5_9
24. Chakarov, A., Sankaranarayanan, S.: Probabilistic Program Analysis with Mar-
    tingales. In: Sharygina, N., Veith, H. (eds.) Computer Aided Verification - 25th
    International Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013.
    Proceedings. LNCS, vol. 8044, pp. 511–526. Springer, Heidelberg (2013). https:
    //doi.org/10.1007/978-3-642-39799-8_34
25. Chen, Y., Hong, C., Wang, B., Zhang, L.: Counterexample-Guided Polynomial
    Loop Invariant Generation by Lagrange Interpolation. In: Kroening, D., Pasare-
    anu, C.S. (eds.) Computer Aided Verification - 27th International Conference,
    CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceedings, Part I. LNCS,
    vol. 9206, pp. 658–674. Springer, Heidelberg (2015). https://doi.org/10.1007/
    978-3-319-21690-4_44
26. D’Argenio, P.R., Katoen, J., Ruys, T.C., Tretmans, J.: The Bounded Retrans-
    mission Protocol Must Be on Time! In: Brinksma, E. (ed.) Tools and Algorithms
    for Construction and Analysis of Systems, Third International Workshop, TACAS
    ’97, Enschede, The Netherlands, April 2-4, 1997, Proceedings. LNCS, vol. 1217,
    pp. 416–431. Springer, Heidelberg (1997). https://doi.org/10.1007/BFB0035403
27. de Moura, L., Bjørner, N.: Z3: An Efficient SMT Solver. In: Ramakrishnan, C.R.,
    Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis of Systems.
    Lecture Notes in Computer Science. Springer, Berlin, Heidelberg (2008). https:
    //doi.org/10.1007/978-3-540-78800-3_24
28. Enea, C., Majumdar, R., Motwani, H.J., Sathiyanarayana, V.R.: Verifying Almost-
    Sure Termination for Randomized Distributed Algorithms. Proc. ACM Program.
    Lang. 10(POPL) (2026). https://doi.org/10.1145/3776691
29. Feng, S., Chen, M., Su, H., Kaminski, B.L., Katoen, J., Zhan, N.: Lower Bounds for
    Possibly Divergent Probabilistic Programs. Proc. ACM Program. Lang. 7(OOPSLA1),
    696–726 (2023). https://doi.org/10.1145/3586051
30. Feng, Y., Zhang, L., Jansen, D.N., Zhan, N., Xia, B.: Finding Polynomial Loop
    Invariants for Probabilistic Programs. In: D’Souza, D., Kumar, K.N. (eds.) Au-
    tomated Technology for Verification and Analysis - 15th International Sympo-
    sium, ATVA 2017, Pune, India, October 3-6, 2017, Proceedings. LNCS, vol. 10482,
    pp. 400–416. Springer, Heidelberg (2017). https://doi.org/10.1007/978-3-319-
    68167-2_26
16      P. Schröer et al.

31. Filliâtre, J., Paskevich, A.: Why3 - Where Programs Meet Provers. In: ESOP.
    LNCS, vol. 7792, pp. 125–128. Springer, Heidelberg (2013). https://doi.org/10.
    1007/978-3-642-37036-6_8
32. Fioriti, L.M.F., Hermanns, H.: Probabilistic Termination: Soundness, Complete-
    ness, and Compositionality. In: Rajamani, S.K., Walker, D. (eds.) Proceedings of
    the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Program-
    ming Languages, POPL 2015, Mumbai, India, January 15-17, 2015, pp. 489–501.
    ACM (2015). https://doi.org/10.1145/2676726.2677001
33. Gehr, T., Misailovic, S., Vechev, M.T.: PSI: Exact Symbolic Inference for Prob-
    abilistic Programs. In: Chaudhuri, S., Farzan, A. (eds.) Computer Aided Verifi-
    cation - 28th International Conference, CAV 2016, Toronto, ON, Canada, July
    17-23, 2016, Proceedings, Part I. LNCS, pp. 62–83. Springer, Heidelberg (2016).
    https://doi.org/10.1007/978-3-319-41528-4_4
34. Haase, D., Batz, K., Gallus, A., Kaminski, B.L., Katoen, J., Klinkenberg, L., Win-
    kler, T.: Generating Functions Meet Occupation Measures: Invariant Synthesis for
    Probabilistic Loops. In: Krebbers, R. (ed.) Programming Languages and Systems
    - 35th European Symposium on Programming, ESOP 2026, Held as Part of the
    International Joint Conferences on Theory and Practice of Software, ETAPS 2026,
    Turin, Italy, April 11-16, 2026, Proceedings, Part I. LNCS, pp. 314–343. Springer,
    Heidelberg (2026). https://doi.org/10.1007/978-3-032-22720-1_12
35. Hähnle, R.: Dijkstra’s Legacy on Program Verification. In: Edsger Wybe Dijkstra:
    His Life, Work, and Legacy. Ed. by K.R. Apt and T. Hoare, pp. 105–140. ACM /
    Morgan & Claypool (2022). https://doi.org/10.1145/3544585.3544593
36. Hark, M., Kaminski, B.L., Giesl, J., Katoen, J.: Aiming low is harder: induction
    for lower bounds in probabilistic program verification. Proc. ACM Program. Lang.
    4(POPL), 37:1–37:28 (2020). https://doi.org/10.1145/3371105
37. Hensel, C., Junges, S., Katoen, J., Quatmann, T., Volk, M.: The probabilistic
    model checker Storm. Int. J. Softw. Tools Technol. Transf. 24(4), 589–610 (2022).
    https://doi.org/10.1007/S10009-021-00633-Z
38. Hölzl, J.: Formalising Semantics for Expected Running Time of Probabilistic Pro-
    grams. In: Blanchette, J.C., Merz, S. (eds.) Interactive Theorem Proving - 7th
    International Conference, ITP 2016, Nancy, France, August 22-25, 2016, Proceed-
    ings. LNCS, vol. 9807, pp. 475–482. Springer, Heidelberg (2016). https://doi.
    org/10.1007/978-3-319-43144-4_30
39. Huang, Z., Dutta, S., Misailovic, S.: AQUA: Automated Quantized Inference for
    Probabilistic Programs. In: Hou, Z., Ganesh, V. (eds.) Automated Technology
    for Verification and Analysis - 19th International Symposium, ATVA 2021, Gold
    Coast, QLD, Australia, October 18-22, 2021, Proceedings. LNCS, pp. 229–246.
    Springer, Heidelberg (2021). https://doi.org/10.1007/978-3-030-88885-5_16
40. Hurd, J., McIver, A., Morgan, C.: Probabilistic Guarded Commands Mechanized
    in HOL. Theoretical Computer Science 346(1), 96–112 (2005). https://doi.org/
    10.1016/j.tcs.2005.08.005
41. Jaarsveld, F.v.: Practical Probabilistic Program Verification using Caesar. Thesis,
    University of Twente, Enschede (2025). https : / / purl . utwente . nl / essays /
    106318.
42. Jones, C.: Probabilistic non-determinism. PhD thesis, University of Edinburgh, UK
    (1990). https://hdl.handle.net/1842/413.
43. Kaminski, B.L.: Advanced Weakest Precondition Calculi for Probabilistic Pro-
    grams. PhD thesis, RWTH Aachen University (2019). https : / / doi . org / 10 .
    18154/RWTH-2019-01829.
                                                                        Caesar        17

44. Kaminski, B.L., Katoen, J., Matheja, C.: On the hardness of analyzing probabilistic
    programs. Acta Informatica 56(3), 255–285 (2019). https://doi.org/10.1007/
    S00236-018-0321-1
45. Kaminski, B.L., Katoen, J.-P., Matheja, C., Olmedo, F.: Weakest Precondition
    Reasoning for Expected Run–Times of Probabilistic Programs. In: Thiemann, P.
    (ed.) Programming Languages and Systems. Lecture Notes in Computer Science.
    Springer, Berlin, Heidelberg (2016). https : / / doi . org / 10 . 1007 / 978 - 3 - 662 -
    49498-1_15
46. Kaminski, B.L., Katoen, J., Matheja, C., Olmedo, F.: Weakest Precondition Rea-
    soning for Expected Runtimes of Randomized Algorithms. J. ACM 65(5), 30:1–
    30:68 (2018). https://doi.org/10.1145/3208102
47. Katoen, J., McIver, A., Meinicke, L., Morgan, C.C.: Linear-Invariant Generation
    for Probabilistic Programs: - Automated Support for Proof-Based Methods. In:
    Cousot, R., Martel, M. (eds.) Static Analysis - 17th International Symposium, SAS
    2010, Perpignan, France, September 14-16, 2010. Proceedings. LNCS, vol. 6337,
    pp. 390–406. Springer, Heidelberg (2010). https://doi.org/10.1007/978- 3-
    642-15769-1_24
48. Kawamoto, Y., Kobayashi, K., Suenaga, K.: StatWhy: Formal Verification Tool
    for Statistical Hypothesis Testing Programs. In: Piskac, R., Rakamaric, Z. (eds.)
    Computer Aided Verification - 37th International Conference, CAV 2025, Zagreb,
    Croatia, July 23-25, 2025, Proceedings, Part II. LNCS, pp. 216–230. Springer,
    Heidelberg (2025). https://doi.org/10.1007/978-3-031-98679-6_10
49. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-C:
    A software analysis perspective. Formal Aspects Comput. 27(3), 573–609 (2015).
    https://doi.org/10.1007/S00165-014-0326-7
50. Kozen, D.: A Probabilistic PDL. In: STOC, pp. 291–297. ACM (1983). https :
    //doi.org/10.1145/800061.808758
51. Kozen, D.: A Probabilistic PDL. J. Comput. Syst. Sci. 30(2), 162–178 (1985).
    https://doi.org/10.1016/0022-0000(85)90012-1
52. Kushilevitz, E., Rabin, M.O.: Randomized Mutual Exclusion Algorithms Revisited.
    In: Hutchinson, N.C. (ed.) Proceedings of the Eleventh Annual ACM Symposium
    on Principles of Distributed Computing, Vancouver, British Columbia, Canada,
    August 10-12, 1992, pp. 275–283. ACM (1992). https : / / doi . org / 10 . 1145 /
    135419.135468
53. Kwiatkowska, M.Z., Norman, G., Parker, D.: PRISM 4.0: Verification of Proba-
    bilistic Real-Time Systems. In: Gopalakrishnan, G., Qadeer, S. (eds.) Computer
    Aided Verification - 23rd International Conference, CAV 2011, Snowbird, UT, USA,
    July 14-20, 2011. Proceedings. LNCS, pp. 585–591. Springer, Heidelberg (2011).
    https://doi.org/10.1007/978-3-642-22110-1_47
54. Leino, K.R.M.: Dafny: An Automatic Program Verifier for Functional Correctness.
    In: Clarke, E.M., Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence,
    and Reasoning. Lecture Notes in Computer Science. Springer, Berlin, Heidelberg
    (2010). https://doi.org/10.1007/978-3-642-17511-4_20
55. Leino, K.R.M.: This is Boogie 2, (2008). https : / / www . microsoft . com / en -
    us/research/publication/this-is-boogie-2-2/
56. Leutgeb, L., Moser, G., Zuleger, F.: Automated Expected Amortised Cost Anal-
    ysis of Probabilistic Data Structures. In: CAV (2). LNCS, vol. 13372, pp. 70–91.
    Springer, Heidelberg (2022). https://doi.org/10.1007/978-3-031-13188-2_4
57. Liffiton, M.H., Malik, A.: Enumerating Infeasibility: Finding Multiple MUSes Quickly.
    In: Gomes, C.P., Sellmann, M. (eds.) Integration of AI and OR Techniques in
18      P. Schröer et al.

    Constraint Programming for Combinatorial Optimization Problems, 10th Interna-
    tional Conference, CPAIOR 2013, Yorktown Heights, NY, USA, May 18-22, 2013.
    Proceedings. LNCS, vol. 7874, pp. 160–175. Springer, Heidelberg (2013). https:
    //doi.org/10.1007/978-3-642-38171-3_11
58. Majumdar, R., Sathiyanarayana, V.R.: Sound and Complete Proof Rules for Prob-
    abilistic Termination. Proc. ACM Program. Lang. 9(POPL), 1871–1902 (2025).
    https://doi.org/10.1145/3704899
59. Matheja, C.: A Game-Based Semantics for the Probabilistic Intermediate Verifi-
    cation Language HeyVL. In: Steffen, B. (ed.) Bridging the Gap Between AI and
    Reality - Second International Conference, AISoLA 2024, Crete, Greece, October
    30 - November 3, 2024, Proceedings. LNCS, vol. 15217, pp. 242–258. Springer,
    Heidelberg (2024). https://doi.org/10.1007/978-3-031-75434-0_17
60. McIver, A., Morgan, C., Kaminski, B.L., Katoen, J.: A new proof rule for almost-
    sure termination. Proc. ACM Program. Lang. 2(POPL), 33:1–33:28 (2018). https:
    //doi.org/10.1145/3158121
61. McIver, A., Morgan, C.C.: Abstraction, Refinement and Proof for Probabilistic
    Systems. Springer-Verlag, New York (2005)
62. Meyer, F., Hark, M., Giesl, J.: Inferring Expected Runtimes of Probabilistic In-
    teger Programs Using Expected Sizes. In: Groote, J.F., Larsen, K.G. (eds.) Tools
    and Algorithms for the Construction and Analysis of Systems - 27th International
    Conference, TACAS 2021, Held as Part of the European Joint Conferences on The-
    ory and Practice of Software, ETAPS 2021, Luxembourg City, Luxembourg, March
    27 - April 1, 2021, Proceedings, Part I. LNCS, vol. 12651, pp. 250–269. Springer,
    Heidelberg (2021). https://doi.org/10.1007/978-3-030-72016-2_14
63. Moosbrugger, M., Bartocci, E., Katoen, J., Kovács, L.: Automated Termination
    Analysis of Polynomial Probabilistic Programs. In: Yoshida, N. (ed.) Programming
    Languages and Systems - 30th European Symposium on Programming, ESOP
    2021, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2021, Luxembourg City, Luxembourg, March 27 - April 1,
    2021, Proceedings. LNCS, vol. 12648, pp. 491–518. Springer, Heidelberg (2021).
    https://doi.org/10.1007/978-3-030-72019-3_18
64. Moosbrugger, M., Bartocci, E., Katoen, J., Kovács, L.: The Probabilistic Termi-
    nation Tool Amber. In: Huisman, M., Pasareanu, C.S., Zhan, N. (eds.) Formal
    Methods - 24th International Symposium, FM 2021, Virtual Event, November 20-
    26, 2021, Proceedings. LNCS, vol. 13047, pp. 667–675. Springer, Heidelberg (2021).
    https://doi.org/10.1007/978-3-030-90870-6_36
65. Moosbrugger, M., Stankovic, M., Bartocci, E., Kovács, L.: This is the moment for
    probabilistic loops. Proc. ACM Program. Lang. 6(OOPSLA2), 1497–1525 (2022).
    https://doi.org/10.1145/3563341
66. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A Verification Infrastructure
    for Permission-Based Reasoning. In: Jobstmann, B., Leino, K.R.M. (eds.) Verifica-
    tion, Model Checking, and Abstract Interpretation - 17th International Conference,
    VMCAI 2016, St. Petersburg, FL, USA, January 17-19, 2016. Proceedings. LNCS,
    vol. 9583, pp. 41–62. Springer, Heidelberg (2016). https://doi.org/10.1007/978-
    3-662-49122-5_2
67. Ngo, V.C., Carbonneaux, Q., Hoffmann, J.: Bounded Expectations: Resource Anal-
    ysis for Probabilistic Programs. In: Proceedings of the 39th ACM SIGPLAN Con-
    ference on Programming Language Design and Implementation. PLDI 2018. Asso-
    ciation for Computing Machinery, New York, NY, USA (2018). https://doi.org/
    10.1145/3192366.3192394
                                                                         Caesar         19

68. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL - A Proof Assistant for
    Higher-Order Logic. Springer (2002)
69. Olmedo, F., Gretz, F., Jansen, N., Kaminski, B.L., Katoen, J., McIver, A.: Con-
    ditioning in Probabilistic Programming. ACM Trans. Program. Lang. Syst. 40(1),
    4:1–4:50 (2018). https://doi.org/10.1145/3156018
70. Park, D.: Fixpoint Induction and Proofs of Program Properties. Machine Intelli-
    gence 5 (1969)
71. Schroer, P.: A deductive verifier for probabilistic programs. MA thesis, RWTH
    Aachen University, Aachen (2024). https : / / doi . org / 10 . 18154 / RWTH - 2024 -
    11340. https://publications.rwth-aachen.de/record/998370.
72. Schröer, P., Batz, K., Dural, U.Y., Haase, D., Kaminski, B.L., Katoen, J.-P., Math-
    eja, C.: Caesar: A Deductive Verifier for Probabilistic Programs (CAV26 Artifact),
    Zenodo. (2026). https://doi.org/10.5281/zenodo.19838026
73. Schröer, P., Batz, K., Kaminski, B.L., Katoen, J., Matheja, C.: A Deductive Ver-
    ification Infrastructure for Probabilistic Programs. Proc. ACM Program. Lang.
    7(OOPSLA2), 2052–2082 (2023). https://doi.org/10.1145/3622870
74. Schröer, P., Haase, D., Katoen, J.: Error Localization, Certificates, and Hints for
    Probabilistic Program Verification via Slicing. In: Krebbers, R. (ed.) Programming
    Languages and Systems - 35th European Symposium on Programming, ESOP
    2026, Held as Part of the International Joint Conferences on Theory and Practice
    of Software, ETAPS 2026, Turin, Italy, April 11-16, 2026, Proceedings, Part II.
    LNCS, pp. 210–240. Springer, Heidelberg (2026). https://doi.org/10.1007/978-
    3-032-22723-2_8
75. Schröer, P., Katoen, J.: Highly Incremental: A Simple Programmatic Approach for
    Many Objectives. In: Formal Methods - 27th International Symposium, FM 2026,
    Tokyo, Japan, May 18–22, 2026, Proceedings. LNCS, Springer, Heidelberg (2026)
76. Tristan, J.-B.: SampCert : Verified Differential Privacy, version 1.0.0. (2024). https:
    / / github . com / leanprover / SampCert. https : / / doi . org / 10 . 5281 / zenodo .
    11204806
77. Zaiser, F., Murawski, A.S., Ong, C.L.: Guaranteed Bounds on Posterior Distribu-
    tions of Discrete Probabilistic Programs with Loops. Proc. ACM Program. Lang.
    9(POPL), 1104–1135 (2025). https://doi.org/10.1145/3704874
78. Zetzsche, S., Tristan, J.-B.: Dafny-VMC: a Library for Verified Monte Carlo Algo-
    rithms, Software. (2023). https://github.com/dafny-lang/Dafny-VMC
