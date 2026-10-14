                                         Chapter 1
                                        Craig Interpolation in Program Verification
                                        Philipp Rümmer 
                                        University of Regensburg, Germany
                                        Uppsala University, Sweden

                                              Abstract
arXiv:2602.08532v1 [cs.LO] 9 Feb 2026




                                        Craig interpolation is used in program verification for automating key tasks such as the inference of
                                        loop invariants and the computation of program abstractions. This chapter covers some of the most
                                        important techniques that have been developed in this context over the last years, focusing on two
                                        aspects: the derivation of Craig interpolants modulo the theories and data types used in verification
                                        and the basic design of verification algorithms applying interpolation.


                                              Contents
                                        1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .             2
                                          1.1 Informal Overview: Invariant Inference using Craig Interpolation . . . . . . .               3
                                          1.2 Organization of the Chapter . . . . . . . . . . . . . . . . . . . . . . . . . . . .          7
                                        2 Satisfiability and Interpolation Modulo Theories . . . . . . . . . . . . . .                     7
                                          2.1 Basic Definitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        7
                                               2.1.1 First-Order Logic and Theories . . . . . . . . . . . . . . . . . . . . . .            8
                                               2.1.2 Craig Interpolation Modulo Theories . . . . . . . . . . . . . . . . . . .             9
                                               2.1.3 Extended Forms of Craig Interpolation . . . . . . . . . . . . . . . . . .            11
                                          2.2 Interpolation Modulo Linear Arithmetic . . . . . . . . . . . . . . . . . . . . .            13
                                               2.2.1 Linear Real Arithmetic (LRA) . . . . . . . . . . . . . . . . . . . . . .             14
                                               2.2.2 Beyond Conjunctions of Non-strict Inequalities . . . . . . . . . . . . .             17
                                               2.2.3 Linear Integer Arithmetic (LIA) . . . . . . . . . . . . . . . . . . . . .            19
                                          2.3 Further Interpolation Approaches . . . . . . . . . . . . . . . . . . . . . . . . .          23
                                               2.3.1 Proof-Based Interpolation . . . . . . . . . . . . . . . . . . . . . . . . .          23
                                               2.3.2 Graph-Based Interpolation . . . . . . . . . . . . . . . . . . . . . . . .            24
                                               2.3.3 Interpolation by Reduction . . . . . . . . . . . . . . . . . . . . . . . .           24
                                        3 Verification Algorithms Based on Interpolation . . . . . . . . . . . . . . .                    25
                                          3.1 BMC: Bounded Model Checking . . . . . . . . . . . . . . . . . . . . . . . . .               25
                                          3.2 IMC: Interpolation and SAT-Based Model Checking . . . . . . . . . . . . . .                 26

                                                    © 2025 Copyright for this paper by its authors
                                                    DRAFT
                                        Final version to appear in Balder ten Cate, Jean Christoph Jung, Patrick Koopmann, Christoph Wernhard
                                        and Frank Wolter, editors. Theory and Applications of Craig Interpolation, chapter XXXCHAPTER,
                                        pages XXXPFROM–XXXPTO. Ubiquity Press, 2026. XXXDOI.
2    Craig Interpolation in Program Verification

            3.2.1 The IMC Algorithm . . . . . . . . . . . . . . . . . . . . . . . . . . . .      26
            3.2.2 Related Interpolation-Based Algorithms . . . . . . . . . . . . . . . . .       28
     3.3    CEGAR: Counterexample-Guided Abstraction Refinement . . . . . . . . . . .            29
            3.3.1 Existential Abstractions . . . . . . . . . . . . . . . . . . . . . . . . . .   29
            3.3.2 Predicate Abstraction . . . . . . . . . . . . . . . . . . . . . . . . . . .    30
            3.3.3 Counterexample-Guided Abstraction Refinement . . . . . . . . . . . .           30
            3.3.4 Variants of Predicate Abstraction and CEGAR . . . . . . . . . . . . .          31
     3.4    CHC: Craig Interpolation and Constrained Horn Clauses . . . . . . . . . . . .        32
            3.4.1 Definitions and Basic Properties . . . . . . . . . . . . . . . . . . . . .     32
            3.4.2 Encoding of Recursive Programs using CHCs . . . . . . . . . . . . . .          34
4 Conclusions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            35
Acknowledgments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            36
References . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         36


 1         Introduction

In program verification, the question is considered how it can be shown (effectively or even
automatically) whether a given software program is consistent with its specification. The
study of program verification is as old as computer science and has over the years led to a
plethora of different techniques, studying the question from various angles and developing
approaches that have found widespread application in both academia and industry.
    Craig interpolation found its way to the field of verification when it was discovered
that interpolation can be used to infer invariants [49], resulting in a new paradigm for
automating one of the key tasks in verification. The discovery gave rise to a number of new
verification algorithms, initially focusing on the verification of hardware circuits, for which
mainly interpolation in propositional logic was used, and later extending the methods to
the analysis of software programs and other classes of systems. The newly discovered use of
Craig interpolation initiated the development of more effective interpolation algorithms and
tools for many different logics, including propositional logic, first-order logic, and the theories
relevant in verification, and was an inspiring factor for the application of Craig interpolation
also in fields other than verification. Many automated verification tools today apply Craig
interpolation for tasks such as reasoning about control flow or data, inferring invariants and
other program annotations, or automatically computing program abstractions.
    This chapter focuses on two main aspects related to Craig interpolation in verification:
techniques for computing Craig interpolants modulo some of the theories used in program
verification and the basic design of verification algorithms applying interpolation. Given the
huge amount of research in the field, the chapter does not attempt to provide a complete survey
of all results, but rather introduces some of the main approaches in detail and with examples
and provides a starting point for exploring the world of interpolation-based verification.
Introduction                                                                                    3

1.1    Informal Overview: Invariant Inference using Craig Interpolation
We first illustrate the use of Craig interpolation for inferring loop invariants using an example.
The Fibonacci sequence [25] is defined by the equations

   F0 = 0,    F1 = 1,   Fi+2 = Fi + Fi+1

and is computed by the function shown in Fig. 1a. After the ith iteration of the loop, the
program variable a stores the Fibonacci number Fi and the variable b the number Fi+1 .
The function has the precondition n >= 0, stated as a requires clause, and the postcondi-
tion \result >= 0 expressing that the result Fn returned by the function is not negative
(“ensures”).
    The aim of formal verification is to construct a rigorous mathematical proof that a program
is consistent with its specification. In order to verify the partial correctness [10] of fib, it
has to be proven that the function, whenever it terminates for a non-negative argument n
with some result a, ensures the postcondition a ≥ 0. Partial correctness proofs are commonly
carried out by an induction over the number of loop iterations executed by the program.
To streamline this reasoning process, the notion of inductive loop invariants (or just loop
invariants) has been introduced [10], which capture properties that cannot be violated during
program execution. More precisely, an inductive loop invariant for a loop is a formula I over
the program variables that are in scope in the loop body, satisfying:
    Initiation: whenever the loop is entered, the invariant I holds.
    Consecution: whenever the loop body is executed starting in a state in which the invariant I
    and the loop condition hold, the invariant I also holds after executing the loop body.
    Sufficiency: whenever the loop terminates in a state satisfying the loop invariant I, the
    rest of the program executes without errors and the postcondition is established.

    For our example program, the three conditions are captured formally on the right-hand
side of Fig. 1 using the program instructions assert and assume [21]. The semantics of
assert(ϕ) is to evaluate a condition ϕ in the current program state and raise an error if ϕ is
violated; if ϕ holds, assert(ϕ) has no effect and program execution continues. The semantics
of assume(ϕ) is similar, but instead of raising an error in case ϕ is violated, the statement
will instead suspend the program execution, preventing the rest of the program from being
executed. A statement assume(false), in particular, stops further program execution and
has similar effect as a non-terminating loop. To deal with assert and assume, we generalize
our notion of partial correctness and say that a program is partially correct if no assert
statement in the program can fail, regardless of the program inputs and the initial state. In
the example, the sufficient inductive invariants are exactly the formulas I for which the three
programs in Figs. 1b to 1d are partially correct.
    We can observe that all three conditions are satisfied by the formula I = a ≥ 0 ∧ b ≥ 0.
This formula I is therefore a loop invariant and represents a witness for the partial correctness
of fib. The simpler formula a ≥ 0, although it is a property that holds throughout any
4       Craig Interpolation in Program Verification

    1    /**                                             1   assume(n >= 0); // requires
    2     * requires n >= 0;                             2   int a = 0; int b = 1; int t;
    3     * ensures \result >= 0;                        3   int i = 0;
    4     */                                             4   assert(I);
    5    int fib(int n) {                              (b) Initiation
    6      int a = 0;
    7      int b = 1;                                    1   assume(I);
    8      int t;                                        2   assume(i < n);
    9                                                    3   t = b;
10           for (int i = 0; i < n; ++i) {               4   b = a + b;
11             t = b;                                    5   a = t;
12             b = a + b;                                6   ++i;
13             a = t;                                    7   assert(I);
14           }
                                                       (c) Consecution
15
16           return a;                                   1   assume(I);
17       }                                               2   assume(!(i < n));
                                                         3   assert(a >= 0); // ensures
(a) Program computing the nth element of the
Fibonacci sequence.                                    (d) Sufficiency

        Figure 1 Fibonacci program and the conditions for inductive loop invariants.


execution of the program as well, does not satisfy the consecution condition and is therefore
not a correct inductive invariant. More precisely, when substituting a ≥ 0 for I in Fig. 1c, we
obtain a program that is not partially correct, an assertion failure occurs when the program
is run starting in the state a = 0, b = −1, i = 0, n = 1.


    Coming up with inductive loop invariants, like the formula a ≥ 0 ∧ b ≥ 0, is a known
challenge in verification, for the same reasons as it is not easy to find induction formulas
in proofs. Craig interpolation is a useful and widely applied technique for finding invariant
candidates. To identify the connection between Craig interpolation and loop invariants,
consider the unwinding of the Fibonacci program in Fig. 2a, which is obtained by listing
the statements on the execution path that executes the loop body twice. The assumptions
added to the program capture the status of the loop condition, which is true for two loop
iterations and false after that, and ensure that the executions of the program in Fig. 2a
correspond exactly to the executions of the original program in Fig. 1a with two loop iterations.
Unwinding loops to obtain loop-free programs is a common technique in verification.
    Consider then possible intermediate assertions K0 , K1 , K2 that enable us to decompose
the program in Fig. 2a into multiple parts at the marked locations. We say that a formula A is
an intermediate assertion for a partially correct program P ;Q if the programs P ;assert(A)
Introduction                                                                                5

                                                      1   assume(n >= 0); // requires
  1    assume(n >= 0);                                2   int a = 0; int b = 1; int t;
  2    int a = 0;                                     3   int i = 0;
  3    int b = 1;                                     4   assert(K0 );
  4    int t;
  5    int i = 0;                                   (b) Sub-program 1
  6
                                                      1   assume(K0 );
  7    // Intermediate assertion K0
                                                      2   assume(i < n);
  8
                                                      3   t = b; b = a + b; a = t; ++i;
  9    assume(i < n); // 1st iteration
                                                      4   assert(K1 );
 10    t = b; b = a + b; a = t; ++i;
 11                                                 (c) Sub-program 2
 12    // Intermediate assertion K1
                                                      1   assume(K1 );
 13
                                                      2   assume(i < n);
 14    assume(i < n); // 2nd iteration
                                                      3   t = b; b = a + b; a = t; ++i;
 15    t = b; b = a + b; a = t; ++i;
                                                      4   assert(K2 );
 16
 17    // Intermediate assertion K2                 (d) Sub-program 3
 18
 19    assume(!(i < n)); // Loop exit                 1   assume(K2 );
 20    assert(a >= 0);                                2   assume(!(i < n));
                                                      3   assert(a >= 0); // ensures
(a) Unwinding of the loop.
                                                    (e) Sub-program 4

      Figure 2 Unwinding two iterations of the loop in the Fibonacci program.


and assume(A);Q are both partially correct as well; in other words, if A is a postcondition
that is ensured by the first sub-program P , but that is also precondition ensuring error-free
execution of the second sub-program Q. The three intermediate assertions in Fig. 2a similarly
split the program into four sub-programs, shown on the right-hand side of Fig. 2, each of
which needs to be partially correct for the intermediate assertions to be suitable.

    The use of Craig interpolants for finding inductive loop invariants is based on two key
observations:
  (i) intermediate assertions are a relaxation of inductive loop invariants, and
 (ii) intermediate assertions are a case of Craig interpolants.
To see point (i), we can compare the conditions in Fig. 1 with the conditions given in Fig. 2.
Conditions 1b and 2b correspond to each other, as do conditions 1d and 2e, whereas the
consecution condition 1c is only approximated by conditions 2c and 2d. Therefore, any
formula I satisfying the conditions in Fig. 1, when substituted for K0 , K1 , K2 , will also
satisfy the conditions in Fig. 2 and give rise to a correct decomposition of the program.
6       Craig Interpolation in Program Verification


                                                          n0 ≥ 0 ∧
                                                                                                     
    1    assume(n >= 0);                                                                             
                                                                                                     
    2    int a = 0, b = 1;                                a0 = 0 ∧ b0 = 1 ∧ i0 = 0 ∧                 
                                                                                                     
                                                                                                     
    3    int t, i = 0;                                    i0 < n0 ∧                                      A
         assume(i < n);                                   t1 = b0 ∧ b1 = a0 + b0 ∧ a1 = t1 ∧
    4
                                                                                                     
                                                                                                     
                                                                                                     
                                                                                                     
                                                                                                     
    5    t = b; b = a + b; a = t; ++i;                    i1 = i0 + 1
    6
                                                          ∧
    7    // Intermediate assertion K
                                                          i1 < n0 ∧
                                                                                                     
    8
                                                                                                     
                                                                                                     
                                                          t2 = b1 ∧ b2 = a1 + b1 ∧ a2 = t2 ∧         
                                                                                                     
         assume(i < n);
    9
                                                                                                     
                                                          i2 = i1 + 1 ∧                                  C
 10      t = b; b = a + b; a = t; ++i;
                                                          i2 ̸< n0
                                                                                                     
                                                                                                     
                                                                                                     
 11      assume(!(i < n));                                                                           
                                                                                                     
 12      assert(a >= 0);                                  → a2 ≥ 0

(a) Computation of a single intermediate assertion.
                                                      (b) Verification condition for partial correctness.

        Figure 3 Intermediate assertions.


Vice versa, not all possible intermediate assertions K0 , K1 , K2 are correct loop invariants,
since intermediate assertions will in general not satisfy consecution 1c. Given a method to
explore possible intermediate assertions K0 , K1 , K2 , however, we can generate candidates for
inductive loop invariants. We survey some of the algorithms that have been proposed for
generating and refining invariant candidates in this way in Section 3.
    To see point (ii), we focus on the case of just a single intermediate assertion to be computed
for the unwound Fibonacci program, shown in Fig. 3a. The partial correctness of the program
can be checked by translating the program, including the assert and assume statements, to
a verification condition [10], which is in this case a formula over linear integer arithmetic.
The verification condition is shown in Fig. 3b and is constructed in such a way that the
condition is valid if and only if the program is partially correct. For this, the condition lists
all assumptions made in the program, includes the assignments to variables in the form of
equations, and states the assertion as the last inequality a2 ≥ 0. Since the program variables
can change their values during program execution, a program variable can correspond to
multiple symbols in the verification condition: for instance, program variable a turns into the
logical constants a0 , a1 , a2 .
    By comparing the verification condition in Fig. 3b with our definition of intermediate
assertions, we can see that the correct intermediate assertions K correspond to the formulas ϕ
for which the implications A → ϕ and ϕ → C are valid, with A, C as marked in Fig. 3b.
Indeed, K has to be a formula that is entailed by the program statements prior to the
respective point in the program, which is expressed by the implication A → ϕ, and it has to
be strong enough to ensure that the rest of the program executes correctly, hence ϕ → C.
This already indicates that the intermediate assertions correspond to the Craig interpolants
Satisfiability and Interpolation Modulo Theories                                                  7

for the implication A → C, as interpolants have to satisfy the same implication conditions.
    To bridge the gap between intermediate assertions and Craig interpolants further, we
have to consider which symbols are allowed to occur in the intermediate assertion K. The
formula K is supposed to be an expression over the program variables n, a, b, t, i. In
the verification condition, those variables have been replaced with different indexed versions;
at the point where K is supposed to be evaluated (line 7 of Fig. 3a), the most recent versions
are named n0 , a1 , b1 , t1 , i1 . Naturally, those are exactly the symbols that occur in both A and
C, as all the older previous versions of the variables will be present only in A, while future
versions can only occur in C. Craig interpolants for the implication A → C therefore range
over exactly the right set n0 , a1 , b1 , t1 , i1 of symbols. To derive intermediate assertions for
our program, we can first compute a Craig interpolant ϕ for A → C, and then rename the
symbols to obtain the intermediate assertion K = ϕ[n0 7→ n, a1 7→ a, b1 7→ b, t1 7→ t, i1 7→ i].
    We will return to the Fibonacci example later in this chapter, when it is discussed how we
can compute Craig interpolants modulo the theories relevant for the program. One possible
interpolant we will then derive is the formula ϕ = (b1 ≥ 1), which can be translated to the
intermediate assertion K = (b ≥ 1).



1.2    Organization of the Chapter

The rest of the chapter consists of two main parts. In Section 2, we introduce the required
background in logic and formally define several notions of Craig interpolation. We then
introduce some of the techniques that have been developed in the verification field for
computing Craig interpolants, focusing on interpolants for arithmetic formulas that are
essential for verification. In Section 3, the second part, we put the interpolation procedures
to use by exploring several interpolation-based verification algorithms.



 2     Satisfiability and Interpolation Modulo Theories

2.1    Basic Definitions

Automatic approaches in verification often work in a setting of quantifier-free theories in
first-order logic, where the theories are chosen to reflect the data types found in programming
languages, while the restriction to quantifier-free formulas is motivated by the desire to stay
in a decidable language. For reasoning about quantifier-free formulas modulo theories, the
Satisfiability Modulo Theories (SMT) paradigm [5] has been developed, in which SAT solvers
are combined with theory solvers to obtain efficient decision procedures. Similarly, much
of the research on Craig interpolation in verification has focused on methods to compute
quantifier-free Craig interpolants modulo theories.
8   Craig Interpolation in Program Verification

2.1.1     First-Order Logic and Theories
We assume a setting of multi-sorted (classical) first-order logic, see for instance [32]. Slightly
extending the notation introduced in Chapter 2, a signature Σ is now a collection of relation
symbols, constant and function symbols, as well as sorts, where each predicate R is endowed
with a uniquely defined rank α(R) = (σ1 , . . . , σn ) of argument sorts, and each constant
and function symbol f with a rank α(f ) = (σ1 , . . . , σn , σ0 ) consisting of the argument
sorts σ1 , . . . , σn and the result sort σ0 . Formulas ϕ and terms t are defined by the following
grammar:

    ϕ ::= R(t, . . . , t) | t = t | ⊤ | ϕ ∧ ϕ | ¬ϕ | ∃x : σ. ϕ ,     t ::= x | f (t, . . . , t) .

In the grammar, R ranges over relation symbols, f over function symbols, x over variables,
and σ over sorts. Constants are identified with nullary functions. We generally assume that
terms and formulas are well-typed, which means that relation and function symbols are only
applied to terms of the right sort, and that = is only used to compare terms of the same
sort. We also use the short-hand notations ⊥, ϕ ∨ ϕ, ϕ → ϕ, and ∀x : σ. ϕ, all with the usual
definition. Given a formula ϕ or term t, we denote the sets of occurring relation and function
symbols by sig(ϕ) ⊆ Σ and sig(t) ⊆ Σ, respectively.
    A closed formula or sentence is a formula in which all variables are bound. A ground
formula is a formula that does not contain any variables (and, therefore, no quantifiers).
Note that ground formulas can still contain constant symbols. A quantifier-free formula is a
formula that does not contain quantifiers, but that might contain variables.
    The semantics of formulas is defined, as is usual, in terms of Σ-structures S that map each
sort σ in Σ to some non-empty domain Dσ , each relation symbol in Σ to a set-theoretical
relation over the argument domains, and each function symbol in Σ to a set-theoretical
function from the argument domains to the result domain. To define the satisfiability of a
formula modulo theories, we need the notion of extensions of signatures and structures. We
say that a signature Ω is an extension of Σ, denoted Σ ⊆ Ω, if Ω contains more sorts, relation
symbols, or function functions than Σ, without changing the rank α(R) or α(f ) of symbols
that already exist in Σ. If Σ ⊆ Ω, then a Σ-structure SΣ is extended by an Ω-structure SΩ
if SΩ interprets the sorts and symbols already present in Σ in the same way as SΣ , while
adding interpretations for the new sorts and symbols in Ω.
▶ Definition 1 (Theory). A theory T is defined by a signature ΣT and a set ST of structures
over ΣT . A sentence ϕ over the signature ΣT is called T -satisfiable (or T -sat) if it evaluates to
true for some structure in ST . A sentence ϕ over an extension Ω ⊇ ΣT is called T -satisfiable
if it evaluates to true in some extension of a structure in ST to Ω.
    For sentences in some signature Ω that is larger than ΣT , this means that additional sorts
and relation or function symbols can be interpreted arbitrarily. As a special case, we say that
a sentence ϕ is simply satisfiable if it is T∅ -satisfiable in the empty theory T∅ . Sentences that
are not T -satisfiable are called T -unsatisfiable (or T -unsat), and sentences whose negation is
Satisfiability and Interpolation Modulo Theories                                                  9

T -unsatisfiable are called T -valid. We also speak of a set M of sentences being T -satisfiable
if there is a common structure satisfying all sentences in M .
    We write Γ |=T ψ if the set Γ of sentences entails the sentence ψ modulo T : whenever an
extension of a structure in ST satisfies all sentences in Γ, it also satisfies ψ. As a special case,
we write ϕ |=T ψ if sentence ϕ entails sentence ψ modulo T , which is equivalent to {ϕ} |=T ψ
and to the conjunction ϕ ∧ ¬ψ being T -unsatisfiable. We write ϕ ≡T ψ for two sentences
being T -equivalent, defined as ϕ |=T ψ and ψ |=T ϕ, and leave out the T when it is clear from
the context.

2.1.2     Craig Interpolation Modulo Theories
Since algorithms in verification (just like in automated reasoning) are usually formulated in
terms of satisfiable or unsatisfiable formulas, instead of valid or counter-satisfiable formulas,
it is common in the area to also define Craig interpolation in the “reversed” way. The
relationship between standard Craig interpolants and separators has already been discussed
in Chapter 1, clarifying that the difference between the two notions is mostly superficial,
at least in classical logic. In order to avoid confusion with the definition in the literature,
we mostly stick to this reversed version of interpolation throughout the chapter, but also
introduce the standard version for completeness reasons.
▶ Definition 2 (Craig interpolant modulo theory). Suppose that T is a theory and A → C a
sentence. A sentence I is called a Craig interpolant modulo T for A → C if the following
conditions hold:
   A |=T I and I |=T C, and
   sig(I) ⊆ (sig(A) ∩ sig(C)) ∪ ΣT .
    Compared to the definition of Craig interpolants in first-order logic from Chapter 2, we
now consider entailment |=T modulo the theory T , and we allow the interpolant I to include
arbitrary interpreted symbols from the theory signature ΣT . As a further, more technical
difference, we only consider closed formulas (sentences) in our definition; this restriction could
be lifted easily but is usually unproblematic, since free variables can be replaced with constant
symbols. The definition in Chapter 2 otherwise corresponds to our definition for the special
case of the empty theory T∅ .
▶ Example 3. Consider the implication A → C, with A, C defined as in Fig. 3b over the
theory of linear integer arithmetic (LIA). Correct Craig interpolants modulo LIA include
I1 = b1 ≥ 1 and I2 = a1 ≥ 0 ∧ b1 ≥ 0.                                                  ⌟
    As discussed in Chapter 1, an interpolation problem A → C can equivalently be expressed
as a conjunction, leading to the alternative reverse notion of interpolation:
▶ Definition 4 (Separator, reverse Craig interpolant). Suppose that T is a theory and A ∧ B a
sentence. A sentence I is called a T -separator or reverse Craig interpolant modulo T for
A ∧ B if the following conditions hold:
10     Craig Interpolation in Program Verification

     A |=T I and I ∧ B |=T ⊥, and
     sig(I) ⊆ (sig(A) ∩ sig(B)) ∪ ΣT .
▶ Theorem 5 (Existence of T -separators [44]). Suppose that T is a theory and A∧B a sentence
that is T -unsatisfiable. Then there is a T -separator for A ∧ B; more precisely, there are
T -separators I1 , I2 such that:
    A |=T I1 and I1 ∧ B |= ⊥,
    A |= I2 and I2 ∧ B |=T ⊥,
    sig(I1 ) ⊆ (sig(A) ∪ ΣT ) ∩ sig(B), and
    sig(I2 ) ⊆ sig(A) ∩ (sig(B) ∪ ΣT ).
    The theorem provides a stronger result about the existence of separators than required
by Definition 4. The sentences I1 , I2 in the theorem are both T -separators according to
Definition 4, but we are even at liberty to assume that one of the two entailment conditions is
general entailment |=, and only the other entailment is modulo the theory T . Similarly, the
theorem provides stronger guarantees about the signature used in I1 , I2 , as the formulas only
have to refer to interpreted symbols from ΣT that also occur in one of the two formulas A, B.
    Although it provides a general guarantee for the existence of reverse interpolants, Theorem 5
is usually not strong enough for applications in verification, as the theorem does not make
any statement about the occurrence of quantifiers in I1 and I2 . In general, even if the
formulas A, B are quantifier-free, there might only be T -separators containing quantifiers,
which is usually less desirable for applications.
▶ Example 6. McCarthy proposed a theory of functional arrays that is today widely used
in program verification [48]. The theory provides functions select(M, a) for reading from an
array M at index a, and store(M, a, x) for updating an array M at index a to the new value x.
In the theory of arrays, the conjunction

     M ′ = store(M, a, x) ∧ b ̸= c ∧ select(M, b) ̸= select(M ′ , b) ∧ select(M, c) ̸= select(M ′ , c)
     |        {z        } |                                   {z                                     }
               A                                                 B

is unsatisfiable, but all reverse interpolants contain quantifiers [51]. Indeed, interpolants
can only refer to the symbols M ′ , M , which occur in both A and B, as well as the array
functions select and store. A quantified interpolant is ∃a, x. M ′ = store(M, a, x).        ⌟
▶ Definition 7 (General quantifier-free interpolation [14]). A theory T admits general quantifier-
free interpolation if for every T -unsatisfiable conjunction A ∧ B there is a quantifier-free
T -separator.
    As the example illustrates, the standard theory of arrays does not admit general quantifier-
free interpolation, while many other theories (for instance, Linear Real Arithmetic, LRA,
Section 2.2.1) have this property. It is possible to extend the theory of arrays, however, to
obtain quantifier-free interpolation [13, 62, 36] (also see Section 2.3.1).
    It is often useful to consider a somewhat weaker criterion for quantifier-free interpolation:
Satisfiability and Interpolation Modulo Theories                                                11

▶ Definition 8 (Plain quantifier-free interpolation [14]). A theory T admits plain quantifier-free
interpolation if for every T -unsatisfiable conjunction A ∧ B that only contains symbols from
ΣT and constant symbols there is a quantifier-free T -separator.

    The difference between “general” and “plain” is that the former demands quantifier-free
interpolants even for conjunctions A ∧ B that contain relation or function symbols that are
not part of T , whereas the latter is happy with only additional constant symbols.

▶ Example 9. The theory of linear integer arithmetic (LIA) admits plain quantifier-free
                                                                                              N
interpolants, provided that the theory includes divisibility statements k | · for every k ∈ ; a
formula k | t is read “k divides t” and asserts that t is a multiple of k. Plain quantifier-free
interpolation follows thanks to the observation that weakest and strongest interpolants in
LIA can be computed using quantifier elimination [32], in exactly the same way as was shown
for propositional logic in Chapter 1. Whether LIA admits general quantifier-free interpolation
depends on the exact signature of the theory that is assumed. To see this, consider the
unsatisfiable conjunction

   x = 2 · y ∧ p(y) ∧ x = 2 · z ∧ ¬p(z)
   |      {z      } |         {z      }
           A                  B

where p is a relation symbol that is not in the signature of LIA. A separator for the
conjunction A ∧ B is the formula I = p(x ÷ 2), where ÷ denotes division with remainder. If
the function ÷ is not included in the signature of LIA, no quantifier-free separators exist [11],
and the theory loses the general quantifier-free interpolation property.                       ⌟

2.1.3     Extended Forms of Craig Interpolation
The notion of separators (or reverse Craig interpolants) defined in the previous section is
sometimes called binary interpolation, as only two formulas A, B are involved. It is possible
to define corresponding n-ary versions, in which an arbitrary number of formulas can be
separated, which is often advantageous in verification. The two main extended notions of
interpolation that are used today, and that are commonly supported by SMT solvers, are
sequence and tree interpolation.

▶ Definition 10 (Sequence interpolant [34, 52]). Suppose T is a theory and A1 ∧ · · · ∧ An a
sentence. A sequence interpolant modulo T or inductive sequence of interpolants modulo T
for A1 ∧ · · · ∧ An is a sequence I0 , I1 , . . . , In of sentences such that:
    I0 = ⊤, In = ⊥,
    for all i ∈ {1, . . . , n}: Ii−1 ∧ Ai |=T Ii , and
    for all i ∈ {0, . . . , n}: sig(Ii ) ⊆ (sig(A1 ∧ · · · ∧ Ai ) ∩ sig(Ai+1 ∧ · · · ∧ An )) ∪ ΣT .

   It is easy to see that a separator I for A1 ∧ A2 corresponds to the sequence inter-
polant ⊤, I, ⊥, so that sequence interpolation strictly extends binary interpolation. It should
12    Craig Interpolation in Program Verification

be noted, as well, that the individual formulas of a sequence interpolant depend on each other,
as each formula Ii−1 has to be strong enough to imply, together with Ai , the next formula Ii .
Sequence interpolants can be derived by repeatedly computing binary interpolants: we set
I0 = ⊤ and then compute each formula Ii , for i = {1, . . . , n}, by computing a separator
for the conjunction (Ii−1 ∧ Ai ) ∧ (Ai+1 ∧ · · · ∧ An ). For reasons of efficiency, this iterative
computation of sequence interpolants is rarely used, however, SMT solvers instead implement
interpolation procedures that can compute the whole sequence interpolant in one go.

▶ Example 11. As we observed in Section 1.1 and Fig. 3b, a single intermediate assertion
for a program can be derived using a binary interpolant by translating the statements on
a program path to an implication A → C. We can use sequence interpolants to derive
multiple consecutive assertions in a program. For this, consider again the version of the
Fibonacci example shown in Fig. 2, in which the loop was unwound two times with the goal of
finding intermediate assertions K0 , K1 , K2 . The locations of the intermediate assertions in the
program indicate that we should now group together the program statements to obtain four
conjuncts; the assertion a >= 0 is negated to state that we are interested in runs violating
the assertion:
                           i0 < n0 ∧ t1 = b0 ∧     i1 < n0 ∧ t2 = b1 ∧
     n0 ≥ 0 ∧ a 0 = 0 ∧
                         ∧ b1 = a0 + b0 ∧        ∧ b2 = a1 + b1 ∧        ∧ i2 ̸< n0 ∧ a2 ̸≥ 0
     b0 = 1 ∧ i 0 = 0
                           a1 = t1 ∧ i1 = i0 + 1   a2 = t2 ∧ i2 = i1 + 1
     |       {z        }   |        {z         }   |        {z         }   |       {z       }
             A1                     A2                        A3                     A4

The conjunction A1 ∧ A2 ∧ A3 ∧ A4 is unsatisfiable, and a sequence interpolant is given by
the formulas

     ⊤, a0 + b0 ≥ 1, b1 ≥ 1, a2 ≥ 1, ⊥ .

The formulas in the sequence interpolant can be translated to intermediate program assertions:
K0 = a + b >= 1, K1 = b >= 1, K2 = a >= 1.                                                  ⌟

    Tree interpolants generalize inductive sequences of interpolants, and are designed with
inter-procedural program verification in mind. In this context, the tree structure of the
interpolation problem corresponds to the call graph of a program. Tree interpolants make it
possible to derive not only intermediate assertions in programs, but also annotations that
relate multiple program states, for instance postconditions [33, 30] (also see Section 3.4.2).

▶ Definition 12 (Tree interpolant [33, 59, 31]). Suppose T is a theory and G = (V, E) a finite
rooted tree, writing E(v, w) to express that the node w is a direct child of v. Further, suppose
that each node n ∈ V of the tree is labeled with a sentence A(n). A function I that labels
every node n ∈ V with a sentence I(n) is called a tree interpolant modulo T (for G and A)
if the following properties hold:
     (i) for the root node v0 ∈ V , it is the case that I(v0 ) = ⊥,
Satisfiability and Interpolation Modulo Theories                                                13

   (ii) for every node v ∈ V , the following entailment holds:
             ^
                     I(w) ∧ A(v) |=T I(v) ,
             w∈V
           (v,w)∈E



  (iii) for every node v ∈ V , it is the case that:
                               [                          [                  
           sig(I(v)) ⊆                    sig(A(w)) ∩                sig(A(w)) ∪ ΣT
                               w∈V                        w∈V
                              E ∗ (v,w)                 ¬E ∗ (v,w)


        where E ∗ is the reflexive transitive closure of E.

    Like in the case of sequence interpolants, also tree interpolants can be derived by repeatedly
computing binary interpolants [59], although SMT solvers usually provide native support for
tree interpolants as well.
    Tree interpolation generalizes all of the more specialized forms of interpolation we have
encountered so far. To see that tree interpolation subsumes sequence interpolation, note that
an n-ary conjunction A1 ∧ · · · ∧ An can be translated to a tree G1 = ({1, . . . , n}, {(i, i − 1) |
2 ≤ i ≤ n}) in which each node i is the child of node i + 1 and is labeled with the formula Ai .
The root of the tree is the node n. Similarly, we can reduce parallel interpolants [43, 54], as
introduced in Chapter 1, to tree interpolants by arranging an implication φ1 ∧ · · · ∧ φn → ψ
as a tree G2 = ({0, 1, . . . , n}, {(0, i) | 1 ≤ i ≤ n}) in which the root 0 is labeled with ¬ψ and
each child i with the formula φi . Parallel interpolants are related to the notion of symmetric
interpolants [39], which can be similarly reduced to tree interpolation.
    Tree interpolants can be generalized further to disjunctive interpolants [58], which have,
however, not found wider adoption in verification. It has also been observed that the
different variants of interpolation correspond to solving particular recursion-free fragments of
constrained Horn clauses [59], which is a connection that we return to in Section 3.4.


2.2    Interpolation Modulo Linear Arithmetic
We now survey some of the techniques that have been developed for constructing quantifier-free
interpolants modulo a theory T , focusing on the case of linear arithmetic that is ubiquitous
in verification. For arithmetic formulas, interpolants are commonly extracted from proofs in
some suitable proof system, resembling the approaches that were discussed in earlier chapters.
For verification, extracting interpolants from proofs is attractive, since proofs tend to focus on
the relevant information in a verification condition. When computing intermediate assertions
(as discussed in Section 1.1) using proof-based interpolation, only the program variables will
be mentioned that were important for the SMT solver to prove the correctness of the program.
Interpolants from proofs are therefore a useful tool when computing program abstractions.
14       Craig Interpolation in Program Verification

2.2.1          Linear Real Arithmetic (LRA)
One of the most common theories supported by interpolating SMT solvers is linear arithmetic
over real numbers or the integers [61, 20]. In the theory of Linear Real Arithmetic, LRA,
we consider formulas that contain linear inequalities 0 ≤ α1 x1 + · · · + αk xk + α0 , where
                    Q
α0 , α1 , . . . , αk ∈ are rational numbers and x1 , . . . , xk are constant symbols of sort Real.
The semantics of scaling with some rational number αx, addition +, and the relation
symbol ≤ is as expected. We initially only consider formulas that are conjunctions of positive
inequalities 0 ≤ α1 x1 + · · · + αk xk + α0 . Equations s = t between real-valued terms can be
translated to a conjunction 0 ≤ s − t ∧ 0 ≤ t − s of two inequalities, while the handling of
strict inequalities 0 < s, disjunctions, and negated equations is discussed in Section 2.2.2.
     To interpolate linear inequalities, we rely on a classical result in linear programming:
                                               R
▶ Lemma 13 (Farkas’ lemma [61]). Let A ∈ m×n be a real-valued matrix and b ∈ m be a     R
                                                R
column vector. There is a column vector x ∈ n such that Ax ≤ b if and only if for every
                    R
row vector y ∈ m with y ≥ 0 and yA = 0 it is the case that yb ≥ 0.
    The lemma implies a simple uniform representation of witnesses for the unsatisfiability of
                                                           V
linear inequalities over the reals: whenever a conjunction i 0 ≤ ti of linear inequalities is
                                                                 P
unsatisfiable, we can form a non-negative linear combination 0 ≤ i αi ti of the inequalities
                               P
in which the right-hand side i αi ti simplifies to a constant negative value β < 0. If the
matrix A and the vector b in the lemma only contain rational numbers, then also the vector y
can be chosen to be rational.
▶ Lemma 14 (Interpolants for linear inequalities [55, 51]). Suppose that
   ^          ^
     0 ≤ ti ∧   0 ≤ sj
     i                  j
     |    {z    }   |           {z   }
          A                     B
                                                                         P           P
is a conjunction of linear inequalities, and that the linear combination
                                                           P              i αi ti +  j βj sj ,
with αi , βj ≥ 0, is constant and negative. Then I = 0 ≤ i αi ti , after simplification and
removing terms with coefficient 0, is an LRA-separator for A ∧ B.
▶ Example 15. We first illustrate this result using an example. Consider the conjunction

     0 ≤ y − 1 ∧ 0 ≤ z − x − 2y − 2 ∧ 0 ≤ x ∧ 0 ≤ −z + 2 .
     |             {z             }   |       {z       }
                            A                    B

This sentence is unsatisfiable, since we can form a non-negative contradictory linear combina-
tion of the inequalities:

     0 ≤ 2 · (y − 1) + (z − x − 2y − 2) + x + (−z + 2) ≡ 0 ≤ −2 .

We can therefore construct an LRA-separator I by considering the corresponding linear
combination of the inequalities in A. Note that the linear combination, before simplification,
Satisfiability and Interpolation Modulo Theories                                              15

still contained the symbol y that is not common to A and B. After simplification, this symbol
has disappeared:

   0 ≤ 2 · (y − 1) + (z − x − 2y − 2) ≡ 0 ≤ z − x − 4 .
                                        |     {z    }
                                                  I

                                                                                                ⌟

Proof of Lemma 14. The properties A |=LRA I and I ∧ B |=LRA ⊥ hold by construction. To
see that sig(I) ⊆ (sig(A) ∩ sig(B)) ∪ ΣLRA , note that I can only contain constant symbols
                                                                      P
that occur in A. Suppose now that some constant symbol x occurs in i αi ti with non-zero
                       P           P
coefficient. Because i αi ti + j βj sj is constant, the symbol x then also has to occur in
P
  j βj sj , and x is therefore in sig(A) ∩ sig(B).                                      ◀

    It is common to define this method of computing LRA-separators in terms of proof rules.
For this, we can first consider the proof rules shown in Table 1a, which form a calculus for
deriving the unsatisfiability of a set of inequalities [51]. The proof rules are defined in terms
of sequents Γ ⊢ ϕ, in which Γ is a finite set of sentences (in our case, set of inequalities), and
ϕ is a single sentence. The semantics of a sequent is that the conjunction of the formulas in Γ
entails ϕ. The proof rules express that the sequent underneath the bar (the conclusion) can
be derived from the sequents above the bar (the premises).
    The rules Hyp and Comb enable the derivation of positive linear combinations of the given
inequalities Γ. Rule Con detects unsatisfiable inequalities, i.e., constant inequalities with a
negative constant term. The rule Simp simplifies inequalities with the help of a rewriting
relation ⇝, which can be implemented by sorting the terms in an inequality and removing all
terms with coefficient 0 [57]. An example proof is given in Fig. 4.
    It follows from Lemma 13 that the calculus in Table 1a is sound and complete for
showing LRA-unsatisfiability: the sequent Γ ⊢ ⊥ can be derived if and only if Γ is a finite
LRA-unsatisfiable set of inequalities.
    To derive interpolants, we augment the proof rules with annotations that reduce, in the
root of a proof tree, to an LRA-separator. The resulting interpolation proof rules are similar
in spirit to the interpolating proof rules for propositional logic introduced in Chapter 1; like
the rules for propositional logic, interpolants are constructed bottom-up, starting at the leaves
of a proof. We follow the style of interpolating proof rules in [51, 27], but streamline the
formulation as we do not consider the combination with other theories at the moment. The
interpolating LRA proof rules are given in Table 1b. For each of the proof rules in Table 1a,
there are one or multiple interpolating rules, now reasoning about two kinds of sequents.
The simpler kind of sequent has the shape (A, B) ▶ I and contains two finite sets A, B of
sentences, as well as a single sentence I. A sequent (A, B) ▶ I is considered valid if and only
                                V       V
if I is an LRA-separator for A ∧ B according to Definition 4. Validity of (A, B) ▶ I
implies that A ∪ B is LRA-unsatisfiable.
16     Craig Interpolation in Program Verification


        Hyp                  (0 ≤ t ∈ Γ)                 Γ ⊢ 0≤s     Γ ⊢ 0≤t
               Γ ⊢ 0≤t                        Comb                                         (α, β > 0)
                                                            Γ ⊢ 0 ≤ αs + βt
                Γ ⊢ 0≤α                                          Γ ⊢ 0≤s
         Con                   (α < 0)                    Simp                   (s ⇝ t)
                 Γ ⊢ ⊥                                           Γ ⊢ 0≤t
 (a) Proof rules for linear real arithmetic. The arrow ⇝ denotes simplification of an expression.


        Hyp-AI                             (0 ≤ t ∈ A)       Hyp-BI                               (0 ≤ t ∈ B)
                   (A, B) ⊢ 0 ≤ t [ t ]                                  (A, B) ⊢ 0 ≤ t [ 0 ]
                              (A, B) ⊢ 0 ≤ s [ s′ ]        (A, B) ⊢ 0 ≤ t [ t′ ]
                     CombI                                                           (α, β > 0)
                                    (A, B) ⊢ 0 ≤ αs + βt [ αs′ + βt′ ]
                   (A, B) ⊢ 0 ≤ α [ t′ ]                                 (A, B) ⊢ 0 ≤ s [ s′ ]     (s ⇝ t,
               I                            (α < 0)                  I
          Con                                                 Simp                                  s′ ⇝ t′ )
                     (A, B) ▶ 0 ≤ t′                                     (A, B) ⊢ 0 ≤ t [ t′ ]

 (b) Interpolating proof rules for linear real arithmetic.


                   (A ∪ {K1 }, B) ▶ I      (A ∪ {K2 }, B) ▶ J
        Disj-AI
                          (A ∪ {K1 ∨ K2 }, B) ▶ I ∨ J
                   (A, B ∪ {K1 }) ▶ I      (A, B ∪ {K2 }) ▶ J
        Disj-BI
                           (A, B ∪ {K1 ∨ K2 }) ▶ I ∧ J

 (c) Interpolating proof rules for disjunctions.


               Γ ∪ {0 ≤ n − x} ⊢ ⊥           Γ ∪ {0 ≤ x − n − 1} ⊢ ⊥
        BnB                                                                   (x ∈ sig(Γ), n ∈ Z)
                                          Γ ⊢ ⊥
                        Γ ∪ {t = 0} ⊢ ⊥      Γ ∪ {0 ≤ t − 1} ⊢ ⊥
        Strengthen
                                    Γ ∪ {0 ≤ t} ⊢ ⊥
                   Γ ⊢ 0 ≤ α1 x1 + · · · + αk xk + α0
        Div                                                          (β = gcd(α1 , . . . , αk ), β > 0)
              Γ ⊢ 0 ≤ (α1 /β)x1 + · · · + (αk /β)xk + ⌊α0 /β⌋

 (d) Proof rules for linear integer arithmetic.


              (A ∪ {0 ≤ n − x}, B) ▶ I      (A ∪ {0 ≤ x − n − 1}, B) ▶ J
 BnB-AI                                                                                 (x ∈ sig(A), n ∈ Z)
                                    (A, B) ▶ I ∨ J

              (A, B ∪ {0 ≤ n − x}) ▶ I      (A, B ∪ {0 ≤ x − n − 1}) ▶ J
 BnB-BI                                                                                (x ∈ sig(B), n ∈ Z)
                                    (A, B) ▶ I ∧ J
                   (A, B) ⊢ 0 ≤ α1 x1 + · · · + αk xk + α0 [ t′ ]
 DivI                                                                           (β = gcd(α1 , . . . , αk ), β > 0)
         (A, B) ⊢ 0 ≤ (α1 /β)x1 + · · · + (αk /β)xk + ⌊α0 /β⌋ [ t′ ÷ β ]

 (e) Interpolating proof rules for linear integer arithmetic.

     Table 1 Proof rules for linear real arithmetic (LRA) and linear integer arithmetic (LIA).
Satisfiability and Interpolation Modulo Theories                                                17


    Hyp                          Hyp
        Γ ⊢ 0 ≤ z − x − 2y − 2         Γ ⊢ 0≤x
   Comb
              Γ ⊢ 0 ≤ (z − x − 2y − 2) + x
         Simp                                         Hyp
                   Γ ⊢ 0 ≤ z − 2y − 2                       Γ ⊢ 0≤y−1
            Comb
                               Γ ⊢ 0 ≤ (z − 2y − 2) + 2(y − 1)
                         Simp
                                       Γ ⊢ 0≤z−4
                                             P
                                         Hyp
                                    P         Γ ⊢ 0 ≤ −z + 2
                              Comb
                                    Γ ⊢ 0 ≤ (z − 4) + (−z + 2)
                               Simp
                                          Γ ⊢ 0 ≤ −2
                                      Con
                                             Γ ⊢ ⊥

   Figure 4 Proof of unsatisfiability for Γ = {0 ≤ y − 1, 0 ≤ z − x − 2y − 2, 0 ≤ x, 0 ≤ −z + 2} in
Example 15.


    The second kind of sequent (also called inequality interpolation [51]) has the shape
(A, B) ⊢ 0 ≤ t [ t′ ], again containing two sets A, B of sentences, one inequality 0 ≤ t, and
one term t′ forming the annotation. The intuition is that a sequent of this kind corresponds
to a non-interpolating sequent A ∪ B ⊢ 0 ≤ t, but in addition it records the contribution to
0 ≤ t from A. A sequent (A, B) ⊢ 0 ≤ t [ t′ ] is valid if the following conditions hold:
    A |=LRA 0 ≤ t′ ,
    B |=LRA 0 ≤ t − t′ , and
    sig(t′ ) ⊆ sig(A) ∪ ΣLRA and t − t′ ⇝ s with sig(s) ⊆ sig(B) ∪ ΣLRA .
The last condition expresses that t′ is a term only containing symbols from A, while the
difference t − t′ can be simplified to a term only containing symbols from B (ignoring symbols
in ΣLRA ). In other words, the annotation splits the inequality 0 ≤ t into an A-part and
a B-part. The proof rules in Table 1b are formulated in such a way that every sequent
that can be derived is valid; for this, Hyp-AI and Hyp-BI record whether an inequality
comes from A or from B, CombI propagates this information, and SimpI simplifies the
annotation t′ along with the derived formula 0 ≤ t. The rule ConI concludes the derivation
of an LRA-separator: if an unsatisfiable inequality 0 ≤ t has been derived, the annotation t′
gives rise to a separator 0 ≤ t′ . The interpolating version of the proof in Fig. 4 is given in
Fig. 5 and produces the same separator 0 ≤ z − x − 4 as the reasoning in Example 15.

2.2.2    Beyond Conjunctions of Non-strict Inequalities
Our discussion so far was restricted to conjunctions of non-strict inequalities 0 ≤ t and
equations s = t. The formulation in terms of interpolating proof rules leads to a flexible
framework, however, that can be extended to include further operators:
18     Craig Interpolation in Program Verification


     Hyp-AI                                                       Hyp-BI
               ΓI ⊢ 0 ≤ z − x − 2y − 2 [ z − x − 2y − 2 ]                      ΓI ⊢ 0 ≤ x [ 0 ]
      CombI
                         ΓI ⊢ 0 ≤ (z − x − 2y − 2) + x [ (z − x − 2y − 2) + 0 ]
                SimpI
                                  ΓI ⊢ 0 ≤ z − 2y − 2 [ z − x − 2y − 2 ]
                                                  P1

                                          Hyp-AI
                                P1                  ΓI ⊢ 0 ≤ y − 1 [ y − 1 ]
          CombI     I
                   Γ    ⊢ 0 ≤ (z − 2y − 2) + 2(y − 1) [ (z − x − 2y − 2) + 2(y − 1) ]
           SimpI
                                          ΓI ⊢ 0 ≤ z − 4 [ z − x − 4 ]
                                                     P2

                                             Hyp-BI
                                     P2                ΓI ⊢ 0 ≤ −z + 2 [ 0 ]
                    CombI
                               ΓI ⊢ 0 ≤ (z − 4) + (−z + 2) [ (z − x − 4) + 0 ]
                       SimpI
                                            ΓI ⊢ 0 ≤ −2 [ z − x − 4 ]
                                  ConI
                                               ΓI ▶ 0 ≤ z − x − 4

    Figure 5 Interpolating version of the proof in Fig. 4. We use the abbreviation ΓI = (A, B) =
({0 ≤ y − 1, 0 ≤ z − x − 2y − 2}, {0 ≤ x, 0 ≤ −z + 2}).


     Boolean structure in formulas can be handled by introducing further proof rules according
     to the principles developed in Chapter 5. For completeness, we show the interpolating
     proof rules for splitting disjunctions in the A- and B-sets in Table 1c. The rules introduce
     a disjunction or conjunction in the interpolant, depending on whether a formula from A
     or from B is considered. Similar rules can be defined for conjunctions and negations.
     It is also generally possible to combine an interpolation procedure for a theory T with
     the propositional methods from Chapter 1, resulting in interpolation procedures that
     can handle arbitrary quantifier-free formulas [51]. This is the approach implemented in
     interpolating SMT solvers, which combine a SAT solver for efficient propositional reasoning
     with theory solvers that only see conjunctions of theory literals [5].
     Strict inequalities 0 < t in formulas can be handled by replacing Farkas’ lemma with
     Motzkin’s transposition theorem [61], which gives a complete criterion for the unsatisfia-
     bility of a conjunction of strict and non-strict inequalities. Based on the transposition
     theorem, it is possible to formulate a lemma similar to Lemma 14 for interpolation in
     the presence of both strict and non-strict inequalities [60]. An alternative path is to add
     separate proof rules for equations and uninterpreted functions [51], which can then be used
     to reason about strict inequalities 0 < t by rewriting them to a conjunction 0 ≤ t ∧ 0 ̸= t.
     Negated equations s ̸= t can be replaced by disjunctions 0 < s − t ∨ 0 < t − s, which can
     then be handled by the rules for disjunctions and strict inequalities.
Satisfiability and Interpolation Modulo Theories                                                   19

2.2.3     Linear Integer Arithmetic (LIA)
The computation of Craig interpolants becomes a bit more involved when moving from real
numbers to the integers. The good news is that the proof rules presented in the previous
section remain sound also for integer arithmetic; as a result, also any LRA-separator derived
using the rules in Table 1b is a correct LIA-separator [51]. Initial software verification tools
based on Craig interpolation therefore resorted to pure LRA reasoning, even for programs
operating on integers or bounded machine integers. The LRA proof rules are not complete
for integer reasoning, of course, since there are formulas that are satisfiable over the reals
but unsatisfiable over integers. To prove or interpolate such formulas, SMT solvers augment
the LRA rules with additional LIA-specific rules, which are, however, harder to turn into
interpolating rules.
    For linear integer arithmetic, LIA, we consider formulas that can contain linear inequali-
                                                                Z
ties 0 ≤ α1 x1 + · · · + αk xk + α0 , where α0 , α1 , . . . , αk ∈ are now integers and x1 , . . . , xk
are constant symbols of sort Int, as well as divisibility statements k | · for every k ∈ (see  N
Example 9). The semantics of such formulas is as expected.

▶ Example 16. Consider the following families of formulas (where n ∈            N, n > 1) [45]:
  An = 0 ≤ y + 2nx + n − 1 ∧ 0 ≤ −y − 2nx,            Bn = 0 ≤ y + 2nz − 1 ∧ 0 ≤ −y − 2nz + n .

Using more intuitive notation, the formulas can be written as An ≡ −n < y + 2nx ≤ 0 and
Bn ≡ 0 < y + 2nz ≤ n, and it is easy to see that An ∧ Bn is satisfiable over the reals, but
unsatisfiable over the integers (for any n > 1). Up to equivalence, the only LIA-separator for
An ∧ Bn is the sentence:

   In = (2n | y) ∨ (2n | y + 1) ∨ (2n | y + 2) ∨ · · · ∨ (2n | y + n − 1) .                        (1)

Given a LIA signature providing only inequalities and divisibility statements, the size of
separators is linear in n and therefore exponential in the size of An , Bn .             ⌟

   There are three different kinds of LIA proof rules commonly implemented in solvers, in
addition to the LRA rules that we have already seen in the previous section:
   Branch-and-bound (BnB) [61]: a solver first checks the satisfiability of a formula ϕ over
   the reals instead of the integers, an approach known as relaxation. If ϕ is found to be
   LRA-unsatisfiable, it is necessarily also LIA-unsatisfiable; if, on the other hand, a solution
   over the real numbers is found, the solver checks whether there are any symbols x that
                                              R Z
   were assigned a non-integer value α ∈ \ . When such an x exists, the search branches
   and continues separately for the two cases x ≤ ⌊α⌋ and x ≥ ⌈α⌉. The proof rule BnB
   representing the branch-and-bound strategy is shown in Table 1d.
   While branch-and-bound is an important proof rule used in solvers, and tends to perform
   well on many formulas, it does not give rise to a complete calculus for LIA. This can be seen
   when considering the formulas in Example 16, which have LRA-solutions of unbounded
20     Craig Interpolation in Program Verification


      Hyp                           Hyp
          Γ ⊢ 0 ≤ y + 2nx + n − 1         Γ ⊢ 0 ≤ −y − 2nz + n
     Comb
               Γ ⊢ 0 ≤ (y + 2nx + n − 1) + (−y − 2nz + n)
          Simp
                       Γ ⊢ 0 ≤ 2nx − 2nz + 2n − 1
                  Div
                            Γ ⊢ 0≤x−z+0
                      Simp
                              Γ ⊢ 0≤x−z
                                  P1
                     Hyp                    Hyp
                         Γ ⊢ 0 ≤ −y − 2nx         Γ ⊢ 0 ≤ y + 2nz − 1
                    Comb
                              Γ ⊢ 0 ≤ (−y − 2nx) + (y + 2nz − 1)
                         Simp
                                    Γ ⊢ 0 ≤ 2nz − 2nx − 1
                               Div
                                       Γ ⊢ 0≤z−x−1
                                             P2

                                        P1     P2
                         Comb
                               Γ ⊢ 0 ≤ (x − z) + (z − x − 1)
                          Simp
                                      Γ ⊢ 0 ≤ −1
                                 Con
                                         Γ ⊢ ⊥

   Figure 6 Schematic cutting planes proof of unsatisfiability for the formulas Γ = {0 ≤ y + 2nx +
n − 1, 0 ≤ −y − 2nx, 0 ≤ y + 2nz − 1, 0 ≤ −y − 2nz + n} in Example 16.


     size, but no LIA-solutions. Regardless of how often the BnB rule is applied, there are still
     proof branches left in which the formulas in Γ are LRA-satisfiable but LIA-unsatisfiable.
     Strengthening [56, 57]: similarly as with branch-and-bound, inequalities 0 ≤ t to be solved
     can be used to split the search into the cases t = 0 and 1 ≤ t, expressing the fact that an
     integer term t cannot have a value strictly between 0 and 1. Strengthening is the core rule
     used by the Omega test [56], in which the boundary case t = 0 is also called a “splinter”.
     By suitably restricting the number of splinters that are introduced, the Omega test uses
     strengthening for quantifier elimination in LIA.
     The corresponding rule Strengthen is shown in Table 1d. Strengthening can be used
     to obtain a complete calculus for LIA, but it requires a separate set of rules to solve the
     equations that stem from the splinters [56, 57]; such rules for equations are not shown
     here. In Example 16, the Strengthen rule can be applied n times to the first inequality
     in An to obtain an LRA-unsatisfiable set of inequalities, which can be proven using the
     rules in Table 1a, as well as n splinters that can be handled using equational reasoning.
     Cuts [61, 20] allow solvers to round the constant term in inequalities in such a way
     that no integer solutions are lost. Cuts can be seen as a targeted application of the
     strengthening rule, restricting application to cases in which the introduced equation t = 0
     is immediately unsatisfiable. There are different strategies available for cuts, including
Satisfiability and Interpolation Modulo Theories                                            21

   Gomory cuts [61, 20] and the cuts-from-proofs method [17], both often used in solvers.
   A general rule Div implementing cuts is shown as the third rule in Table 1d. The rule Div
   is applicable if the coefficients of the non-constant terms in an inequality have some
   factor β > 0 in common. In this case, all coefficients in the inequality can be divided by β
   while rounding down the constant term α0 /β, strengthening the inequality. Cuts give rise
   to a complete calculus for LIA and have the advantage that no branching is needed; proofs
   including cuts are also called cutting planes proofs. To obtain even better performance in
   practice, many solvers combine cuts with the branch-and-bound method.
   We show a cutting planes proof for the formulas in Example 16 in Fig. 6. The proof
   works for any positive value n and requires two applications of the Div rule, after which a
   contradiction can be derived using Comb.

    All three kinds of proof rules can be made interpolating. We show the interpolating
versions of branch-and-bound and cuts in Table 1e, using the same sequent notation as for
the interpolating LRA rules in Table 1b. Interpolating versions of the strengthening rule
are somewhat more involved, due to the need to introduce also interpolating rules for linear
equations [38], but can be derived as well [12, 27].
    The simplest rule to interpolate is branch-and-bound, since the branching performed by
BnB can be seen as the splitting of a disjunction 0 ≤ n − x ∨ 0 ≤ x − n − 1 (which is a
valid formula in LIA). The two interpolating rules corresponding to BnB are BnB-AI and
BnB-BI : depending on whether the constant x is a symbol from A or from B, one or the
other rule has to be used. The rules BnB-AI and BnB-BI correspond to the rules Disj-AI
and Disj-BI for splitting disjunctions; like the rules for disjunctions, they derive the overall
interpolant for (A, B) by combining the sub-interpolants I, J using either a disjunction or
a conjunction. If x occurs in both A and B, either rule can be used, but the rules will, in
general, lead to different interpolants.
    Interpolating cutting planes proofs is more involved, since the inequalities tightened in
a proof using the rule Div might contain some symbols that only occur in A, and some
symbols that only occur in B, and therefore cannot be associated uniquely with either side.
It is possible, however, to extend the annotation approach for LRA interpolation to LIA by
allowing the annotation t′ in a sequent (A, B) ⊢ 0 ≤ t [ t′ ] to contain the operator ÷ for
integer division with remainder, provided that the denominator is an integer constant [27, 55].
We use the Euclidean definition of division with remainder [46], in which a ÷ b for a, b ∈ , Z
b=                                              Z
  ̸ 0 is defined to be the unique number q ∈ such that a = b · q + r with 0 ≤ r < |b|. To
handle integer division, it is also necessary to generalize the SimpI rule by adding a case for
pulling terms out of the scope of ÷, namely (αs + t) ÷ β ⇝ (α/β)s + (t ÷ β) whenever β | α.
This rewrite is correct, since the equation (βx + y) ÷ β = x + (y ÷ β) holds for Euclidian
division, provided that β ̸= 0.
    The rule DivI in Table 1e is deceivingly simple and uses ÷ to divide the annotation t′ in
a sequent by the same number β as the main inequality. The effect of DivI is best illustrated
using an example. Fig. 7 shows the interpolating version of the proof in Fig. 6, proving that
                                                                                                                                                                                                                       22




                                                                                                       Hyp-AI                                                                  Hyp-BI
                                                                                                                 ΓI ⊢ 0 ≤ y + 2nx + n − 1 [ y + 2nx + n − 1 ]                            ΓI ⊢ 0 ≤ −y − 2nz + n [ 0 ]
                                                                                                            I
                                                                                                       Comb
                                                                                                                                ΓI ⊢ 0 ≤ (y + 2nx + n − 1) + (−y − 2nz + n) [ (y + 2nx + n − 1) + 0 ]
                                                                                                                 SimpI
                                                                                                                                            ΓI ⊢ 0 ≤ 2nx − 2nz + 2n − 1 [ y + 2nx + n − 1 ]
                                                                                                                                    DivI
                                                                                                                                                   ΓI ⊢ 0 ≤ x − z + 0 [ (y + 2nx + n − 1) ÷ 2n ]
                                                                                                                                    SimpI
                                                                                                                                                      ΓI ⊢ 0 ≤ x − z [ x + (y + n − 1) ÷ 2n ]
                                                                                                                                                                        P1

                                                                                                                 Hyp-AI                                                     Hyp-BI
                                                                                                                                 ΓI ⊢ 0 ≤ −y − 2nx [ −y − 2nx ]                       ΓI ⊢ 0 ≤ y + 2nz − 1 [ 0 ]
                                                                                                                  CombI                        I
                                                                                                                                           Γ       ⊢ 0 ≤ (−y − 2nx) + (y + 2nz − 1) [ (−y − 2nx) + 0 ]
                                                                                                                                  SimpI




0 ≤ −y − 2nx}, {0 ≤ y + 2nz − 1, 0 ≤ −y − 2nz + n}).
                                                                                                                                                         ΓI ⊢ 0 ≤ 2nz − 2nx − 1 [ −y − 2nx ]
                                                                                                                                                                                                                       Craig Interpolation in Program Verification




                                                                                                                                               DivI
                                                                                                                                                        ΓI ⊢ 0 ≤ z − x − 1 [ (−y − 2nx) ÷ 2n ]
                                                                                                                                           SimpI
                                                                                                                                                        ΓI ⊢ 0 ≤ z − x − 1 [ −x + (−y) ÷ 2n ]
                                                                                                                                                                        P2

                                                                                                                                                               P1      P2
                                                                                                            CombI           I
                                                                                                                        Γ        ⊢ 0 ≤ (x − z) + (z − x − 1) [ (x + (y + n − 1) ÷ 2n) + (−x + (−y) ÷ 2n) ]
                                                                                                                SimpI
                                                                                                                                                   ΓI ⊢ 0 ≤ −1 [ (y + n − 1) ÷ 2n + (−y) ÷ 2n ]
                                                                                                                                     ConI
                                                                                                                                                      ΓI ▶ 0 ≤ (y + n − 1) ÷ 2n + (−y) ÷ 2n




   Figure 7 Interpolating proof for the formulas in Example 16: ΓI = (A, B) = ({0 ≤ y + 2nx + n − 1,
Satisfiability and Interpolation Modulo Theories                                            23

the formulas in Example 16 are unsatisfiable for any positive n. The two applications of
DivI introduce a division ÷ 2n in the annotation term. The annotations are subsequently
simplified by applying the rule SimpI , which reduces the terms 2nx and −2nx to x and
−x, respectively, removing the symbol x from the scope of ÷. Since x and −x cancel each
other out, the final LIA-separator is the formula 0 ≤ (y + n − 1) ÷ 2n + (−y) ÷ 2n that only
contains the symbol y that is common to A and B. The reader can verify that this separator
is equivalent to In in Example 16 but exponentially more succinct thanks to the use of ÷.
    The interesting question, of course, is why the rule DivI always produces correct in-
terpolants. Adapted to the case of LIA, the conditions to be satisfied by an interpolating
sequent (A, B) ⊢ 0 ≤ t [ t′ ] are:
    A |=LIA 0 ≤ t′ ,
    B |=LIA 0 ≤ t − t′ , and
    sig(t′ ) ⊆ sig(A) ∪ ΣLIA and t − t′ ⇝ s with sig(s) ⊆ sig(B) ∪ ΣLIA .
We can check, using purely arithmetic reasoning, that the first two conditions hold in any
sequent (A, B) ⊢ 0 ≤ t [ t′ ] derived using the rules in Table 1b and rule DivI . To see that
the last conditions are preserved by DivI , note that the ability to rewrite t − t′ to a term s
with sig(s) ⊆ sig(B) ∪ ΣLIA implies that whenever a term αx occurs in t, for some x that is
not present in B, there has to be a corresponding term αx in t′ canceling out αx. When
applying DivI , it then has to be the case that α is a multiple of the denominator β. An
application of the rule SimpI can therefore simplify the annotation (· · · + αx + · · · ) ÷ β to
(α/β)x + (· · · ) ÷ β.
    More generally, after applying SimpI , it will never be the case that symbols that do not
occur in B are in the scope of the ÷ operator in the annotation t′ . Despite the use of ÷ in
the annotations, the interpolating proof rules are able to eliminate symbols that are present
in A but not in B from annotations in more or less the same way as for LRA, and the derived
interpolants are correct.

2.3     Further Interpolation Approaches
2.3.1    Proof-Based Interpolation
The extraction of (quantifier-free) T -separators from proofs is possible not only for LRA and
LIA, but also for many other theories. The interpolating proof rules for LRA can be extended to
handle also the theory of Equality and Uninterpreted Functions (EUF) [51]. The LRA calculus
can also be extended to non-linear arithmetic (Non-linear Real Arithmetic, NRA), replacing
the witnesses produced by Farkas’ lemma by Sum-Of-Squares (SOS) witnesses [16, 65]. NRA
interpolants can also be computed with the help of the model-constructing satisfiability
calculus MCSAT [40].
    Several interpolating calculi have been presented for the theory of arrays [13, 62, 36]. As
illustrated in Example 6, one difficulty to be solved with arrays is the fact that the standard
version of arrays does not admit (plain or general) quantifier-free interpolation. This problem
24     Craig Interpolation in Program Verification

can be addressed by extending the theory by a function symbol diff satisfying the following
axiom:

     ∀M, M ′ . M ̸= M ′ → select(M, diff (M, M ′ )) ̸= select(M ′ , diff (M, M ′ )) .
                                                                                   


The axiom implies extensionality of arrays, i.e., two arrays are equal if and only if they have
the same contents. In Example 6, we can then construct the quantifier-free reverse interpolant

     M ′ = store M, diff (M, M ′ ), select(M ′ , diff (M, M ′ )) .
                                                                


2.3.2      Graph-Based Interpolation
In the context of SMT, the special case of the satisfiability of a formula in the empty theory T∅
is commonly called satisfiability modulo Equality and Uninterpreted Functions (EUF). EUF is
in SMT solvers usually handled with the help of the congruence closure algorithm [2], which
decides whether a given equation s = t follows from a finite set E of ground equations, i.e.,
E |=T∅ s = t. For this, congruence closure constructs an equality graph (the e-graph) in
which the terms and sub-terms of E are the nodes, the equations E and inferred equalities
are edges, and a second set of edges is used to represent the sub-term relation. Congruence
closure can show the unsatisfiability of a formula ϕ by inferring that some equation s = t
follows from the equations present in ϕ, while ϕ also contains the negated equation s ̸= t.
The e-graph represents the proof explaining the unsatisfiability of a formula.
    In case of an unsatisfiable conjunction A ∧ B of equations, separators can be extracted
from the e-graph [22]. This is done by summarizing paths in the graph; if a path is created
only by equations from the formula A, it can be represented by a single equation that is
entailed by A, and similarly for equations from B. Reasoning in terms of congruences (s = t
implies f (s) = f (t)) gives rise to implications in the computed separators.

2.3.3      Interpolation by Reduction
A further paradigm for computing Craig interpolants is reduction [41]. Reduction is applicable
whenever direct interpolation of a conjunction A ∧ B in some theory T is difficult, but it is
possible to translate A ∧ B to a conjunction A′ ∧ B ′ in a theory T ′ in which interpolants can
be computed. The T ′ -separator I ′ then has to be translated back to obtain a T -separator I for
the original conjunction A∧B; in the special case that T is an extension of T ′ , back-translation
is unnecessary, since I ′ is already a correct T -separator for A ∧ B.
    The reduction approach can be applied to a wide range of theories. The theory of
arrays and the theory of sets with finite cardinality constraints can be reduced to EUF,
while the theory of multisets can be reduced to the combined theory of EUF and LIA [41].
Since reduction can introduce quantifiers, however, it is in general necessary to post-process
interpolants using a quantifier elimination procedure for quantifier-free interpolation. In
follow-up work, it was shown that the theory of algebraic data types with size constraints can
Verification Algorithms Based on Interpolation                                                                 25

be reduced to the combined theory of EUF and LIA [37], and that the theory of bit-vectors
can be reduced to LIA [3]. The latter reduction happens lazily with the help of tailor-made
proof rules that successively translate bit-vector formulas to LIA formulas.


 3       Verification Algorithms Based on Interpolation
We now introduce some of the main verification algorithms based on Craig interpolation,
starting with the SAT-based model checking algorithm proposed by McMillan in 2003 [49]. We
present the algorithms in our setting of quantifier-free interpolation in a theory T , although
the earlier papers focus on propositional interpolation.

3.1      BMC: Bounded Model Checking
Interpolation-based verification algorithms were inspired by Bounded Model Checking (BMC),
in which the behavior of a system during the first k execution steps is analyzed with the help
of SAT or SMT solvers [7]. The insight that led to interpolation-based algorithms is that
interpolants can be extracted for the formulas considered in BMC, this way turning bounded
into unbounded model checking.
     To introduce BMC, we fix a theory T and assume that states of the system to be verified
are described by a vector x̄ = (x1 , . . . , xn ) of constants; in the original SAT-based formulation,
x̄ is a vector of propositional variables. We use the notation x̄′ = (x′1 , . . . , x′n ) for a fresh
primed copy of the constants, and similarly x̄i for copies indexed by i. BMC operates on
transition systems represented using formulas that model, for instance, sequential hardware
circuits. A transition system (B, TR) is given by two sentences B[x̄] and TR[x̄, x̄′ ] defining
the initial states and the transition relation, respectively. The notation B[x̄] expresses that
the constants x̄ can occur in B, and B[ȳ] that the constants x̄ are replaced by another vector ȳ
of terms. Intuitively, any valuation of x̄ satisfying B[x̄] is considered an initial state of the
system, and valuations of x̄, x̄′ that satisfy TR[x̄, x̄′ ] represent a transition from x̄ to x̄′ .
     A further sentence E[x̄] is introduced to represent error states. The goal of verification
is to decide whether any error states are reachable from the initial states. The verification
of partial correctness properties, such as the ones discussed in Section 1.1, can be reduced
to this form, modeling the states in which postconditions or assertions are violated using
the formula E. In BMC, the reachability of error states is characterized by unfolding the
transition relation a bounded number of times: error states are reachable if and only if there
                               N
is a natural number k ∈ so that the sentence
                                                                                                               
     B[x̄0 ] ∧ TR[x̄0 , x̄1 ] ∧ TR[x̄1 , x̄2 ] ∧ · · · ∧ TR[x̄k−1 , x̄k ] ∧ E[x̄0 ] ∨ E[x̄1 ] ∨ · · · ∨ E[x̄k ] (2)

is T -satisfiable. As it turns out, applying SAT or SMT solvers to (2) is a very effective way to
discover systems in which errors can occur, thanks to the performance of such solvers. If the
formula (2) is T -unsatisfiable, in contrast, it is not (at least not in the general case) possible
26       Craig Interpolation in Program Verification

to tell whether the system can indeed not encounter any errors, or whether the chosen k was
simply too small to find an error.

3.2       IMC: Interpolation and SAT-Based Model Checking
3.2.1       The IMC Algorithm
The first interpolation-based model checking algorithm extends BMC with the computation
of inductive invariants through Craig interpolation, making it possible to tell conclusively
                                                                           N
that (2) is T -unsatisfiable for every value of k ∈ . We refer to the algorithm as the IMC
algorithm, following the name given in [6]. To prove that the formula (2) is unsatisfiable for
             N
every k ∈ , it is enough to find a sentence R[x̄], the inductive invariant, with the properties
discussed in Section 1.1:
    Initiation:    B[x̄] |=T R[x̄];
    Consecution: R[x̄] ∧ TR[x̄, x̄′ ] |=T R[x̄′ ];
    Sufficiency: R[x̄] ∧ E[x̄] |=T ⊥.

    Indeed, assuming that formula (2) holds, due to Initiation and Consecution it follows that
R is true for all states x̄0 , . . . , x̄i , and due to Sufficiency a contradiction with the disjunction
of E-formulas follows.
    For reasons of presentation, we make the simplifying assumption that the relation TR
is total, i.e., ∀ȳ. ∃z̄. TR[ȳ, z̄] is valid. To obtain candidates for the inductive invariant R[x̄],
the IMC algorithm constructs a sequence R0 , R1 , R2 , . . . of sentences, in such a way that
each Ri is an over-approximation of the states that are reachable in at most i steps from
the initial states. Naturally, we can set R0 = B. To construct the other sentences, we fix
                       N
constants j, k ∈ with j ≤ k, which are the parameters of IMC. Each formula Ri+1 is then
derived from Ri by considering the following conjunction:
                                    k−1
                                    ^                              k
                                                                   _
     Ri [x̄0 ] ∧ TR[x̄0 , x̄1 ] ∧         TR[x̄l , x̄l+1 ] ∧             E[x̄l ] .                  (3)
                                    l=1                            l=j
     |          {z          }       |                 {z                       }
            A[x̄0 ,x̄1 ]                        B[x̄1 ,...,x̄k ]


Formula (3) corresponds to the BMC query (2), with the difference that the initial states B
have been replaced with the ith approximation Ri , and that the range of the disjunction of
the E[x̄l ] is parameterized in j. Three cases are possible:
   Case (i): Formula (3) is satisfiable and i = 0. This implies that Ri = R0 = B and error
   states are reachable in the transition system. Formula (2) is then satisfiable as well for
   the same k.
   Case (ii): Formula (3) is satisfiable and i > 0. This can happen either because error
   states are reachable (like in (i)), or because the approximation Ri is too imprecise. Nothing
   can be said in this situation and the algorithm has to abort.
Verification Algorithms Based on Interpolation                                                         27

    Case (iii): Formula (3) is unsatisfiable. We can then extract a T -separator Ii [x̄1 ] from
    the conjunction A[x̄0 , x̄1 ] ∧ B[x̄1 , . . . , x̄k ], since x̄1 are the constants that occur in both
    A[x̄0 , x̄1 ] and B[x̄1 , . . . , x̄k ]. By renaming x̄1 to x̄, we obtain a sentence Ii [x̄] that is an
    over-approximation of the states that can be reached in one step from Ri . The next
    approximation is set to Ri+1 [x̄] = Ri [x̄] ∨ Ii [x̄], weakening Ri to take one further step of
    the transition system into account.

    It turns out that the sequence R0 , R1 , R2 , . . . often contains some Ri , for small values of i,
that are inductive invariants. Intuitively, this is because the sentences Ri are constructed to
approximate the reachable states of the transition system. The use of Craig interpolation has
the effect of accelerating the fixed-point construction, focusing on properties of the states that
are sufficient to stay inconsistent with the B-part of (3) (i.e., not reaching any error states
within k steps) and ignoring other details that might be part of the formulas B, TR, E but
irrelevant for ruling out errors. This effect of acceleration is achieved by obtaining interpolants
from proofs, utilizing the fact that a proof is likely to only refer to those facts and constraints
that are necessary to show the unsatisfiability of (3), which are exactly the properties needed
to avoid error states.
    By construction, the sentences R0 , R1 , R2 , . . . all satisfy the Initiation condition of inductive
invariants. To check whether any of the sentences Ri satisfies Consecution, this condition can
be verified explicitly (Ri [x̄] ∧ TR[x̄, x̄′ ] |=T Ri [x̄′ ]); alternatively, as a sufficient condition, it
can also be checked whether it is ever the case that Ri+1 ≡T Ri , which implies Consecution
thanks to the definition of T -separators. Sufficiency of a sentence Ri can similarly be
verified explicitly (Ri [x̄] ∧ E[x̄] |=T ⊥). IMC can also be set up in such a way that all
constructed formulas Ri satisfy Sufficiency: for this, it has to be verified that none of the
initial states R0 = B are error states, and j must have value 1 [49]. (At this point, the
assumption that T is total is required as well.)
    To make the approach effective, it is common to require the formulas B, TR, E to be
quantifier-free and the considered theory T to admit plain quantifier-free interpolation; this
ensures that also the sentences R0 , R1 , R2 , . . . are quantifier-free and the required checks
remain decidable. The original IMC algorithm [49] made use of Craig interpolants extracted
from propositional resolution proofs (see Chapter 1).

    The parameters j, k can be used to control the behavior of the algorithm. Bigger values
of k and smaller values of j lead to more precise over-approximations, since the B-part of
(3) ensures that no error states are reachable from the separator Ii [x̄1 ] in at least j − 1 and
at most k − 1 steps. Increasing k, in particular, will lead to stronger formulas Ii [x̄1 ] being
computed, which will reduce the probability of ending up in Case (ii) in later iterations. It
can be shown that IMC is even complete for computing inductive invariants under certain
assumptions [49]:
    The transition system has bounded reverse depth, which means that there is a number d ∈             N
    such that whenever E is reachable from some state, then there is also a path from the
28    Craig Interpolation in Program Verification

     state to E that has length at most d.
    The sequence of computed invariant candidates R0 , R1 , . . . is guaranteed to become
                                       N
    stationary, i.e., there is some i ∈ such that Ri ≡T Ri′ for every i′ ≥ i.
If the first assumption is satisfied, it is enough to choose a large enough k and set j to 1 to
prevent the algorithm from failing due to Case (ii). If, moreover, the second assumption is
satisfied, there will be some Ri such that Ri ≡T Ri+1 , which is then guaranteed to pass the
Consecution condition and give rise to an inductive invariant.
    Both assumptions are satisfied by transition systems and invariants in propositional
logic. For the second condition, observe that each Ri entails the next Ri+1 , so that the
candidates R0 , R1 , . . . form an ascending chain. Since there are only finitely many propositional
formulas Ri (up to equivalence), every chain R0 , R1 , . . . eventually becomes stationary. In
contrast, for systems with infinite state space, which are modeled using theories T that allow
infinite universes, the conditions are typically violated. Empirically, the IMC algorithm tends
to perform well even for such systems [6].


3.2.2     Related Interpolation-Based Algorithms
Many different versions and improvements of the SAT-based model checking algorithm IMC
have been proposed. In the original formulation, IMC was defined for transition systems and
interpolation in propositional logic [49]. IMC was later extended to theories and the setting
of software verification [6], a setting that we adopted for this chapter as well.
    The interpolation sequence-based model checking algorithm ISB uses a similar fixed-
point loop as IMC, but applies sequence interpolants (Definition 10) instead of binary
interpolants [63]. The key difference between IMC and ISB is in the way how interpolation
queries are defined: while IMC includes the previous approximation Ri in the query (3) used
to compute the next Ri+1 , the queries applied by ISB only refer to the sentences B, TR, E
defining the transition system and the error states, but ISB increases the considered number
of transitions (copies of TR) in each iteration.
    Verification algorithms for software programs often take the control structure of a program
into account. Instead of a monolithic transition system (B, TR), we would then start from
a program described by a set of transition relations arranged by a control-flow automaton.
This setting leads to smaller interpolation queries, since only one program path at a time has
to be considered. The Impact algorithm follows this strategy, using sequence interpolants to
obtain invariant candidates for particular program paths [52].
    The IC3 algorithm is even more local and analyzes individual system states instead of the
whole transition relation to obtain invariant candidates [9]. While IC3 has similarities with
the IMC and ISB algorithms, IC3 does not rely on Craig interpolation anymore but directly
infers clauses that are inductive invariants. The Spacer algorithm, which is an extension of
IC3, uses interpolation as an optional abstraction step [42].
Verification Algorithms Based on Interpolation                                                      29

3.3     CEGAR: Counterexample-Guided Abstraction Refinement
Predicate abstraction [24, 4] and Counterexample-Guided Abstraction Refinement (CE-
GAR) [15] provide another perspective on the use of Craig interpolation for verifying systems.
Both notions predate the IMC algorithm and the use of interpolation in verification but
turned out to be very suitable for a combination with interpolation [34, 50].

3.3.1     Existential Abstractions
We again fix a theory T . For the sake of presentation, we assume that the theory comes with
a uniquely defined structure ST , i.e., that the set ST = {ST } in Definition 1 is a singleton set.
As the states of a system are described by a vector x̄ = (x1 , . . . , xn ) of constants with sorts σ̄ =
(σ1 , . . . , σn ), the state space of the system is the Cartesian product D = Dσ1 × · · · × Dσn .
Since the theory has a unique structure ST , with slight abuse of notation we can write B[s] to
express that a state s ∈ D satisfies the sentence B, i.e., that s is an initial state, and similarly
state by TR[s, s′ ] that there is a transition from s to s′ .
     To verify properties of the transition system (B, TR), for instance the reachability of
error states E, it is frequently useful to consider an abstract version of the transition system
with a smaller number of states. We can define abstractions by choosing a non-empty set D̂
as the abstract state space, together with an abstraction function h : D → D̂ that induces
the abstract transition system in terms of a set B̂ of abstract initial states and an abstract
transition relation TR:    ˆ

     B̂ = {ŝ ∈ D̂ | there is s ∈ D with h(s) = ŝ and B[s]} ,
     ˆ
    TR = {(ŝ, ŝ′ ) ∈ D̂2 | there are s, s′ ∈ D with h(s) = ŝ, h(s′ ) = ŝ′ and TR[s, s′ ]} .

This construction is known as existential abstraction [28]. It is useful since non-reachability
of states in existential abstractions implies non-reachability also in the concrete system:
whenever M ⊆ D and the abstract states h(M ) are not reachable from initial states in
      ˆ
(B̂, TR),  the concrete states M are not reachable from the initial states in (B, TR) either.
More generally, existential abstractions can be used to prove ACTL* properties of the concrete
system [28].
     Existential abstractions are illustrated in Fig. 8a. Black states and edges represent the
concrete transition system (B, TR), with initial states marked with a further incoming edge.
The concrete states are grouped together to red abstract states by the function h. Abstract
states are connected by transitions whenever any of the included concrete states are, leading
to over-approximation of the behavior. For instance, the concrete transition system in Fig. 8a
does not contain any transitions of a state to itself, while the abstract transition system has
such transitions.
                                                      ˆ does not imply the reachability of the
     As a result, the reachability of states in (B̂, TR)
corresponding states in (B, TR), since the abstract transition system can contain spurious
paths that have no equivalent paths in (B, TR). For instance, in Fig. 8a there is an abstract
30      Craig Interpolation in Program Verification




                                                e                                                          e

     (a) Initial abstraction.                               (b) Abstraction after refinement.

     Figure 8 A transition system (black) and two existential abstractions (red).


path from the left-most initial to the right-most state, but there is no concrete path from an
initial state to the right-most state e.

3.3.2       Predicate Abstraction
A convenient way to define existential abstractions is predicate abstraction [24]. For this,
we assume a finite set P = {P1 [x̄], . . . , Pk [x̄]} of sentences that can refer to the constants x̄
representing system states. The transition system defined using Boolean abstraction [4], one
of multiple different versions of predicate abstraction, groups together states that cannot
be distinguished by the predicates in P. Abstract states can be represented as bit-vectors,
D̂ = {0, 1}k , storing for each of the predicates in P whether the predicate holds for some
concrete state s ∈ D or not:
                                               (
                                                  1 if Pi [s]
   h(s) = (p1 (s), . . . , pk (s)), pi (s) =                         for i ∈ {1, . . . , k} .
                                                  0 otherwise

    For an abstraction with k predicates, this results in a transition system (B̂, TR)     ˆ with
 k
2 abstract states, which can also be constructed explicitly in terms of the sentences B, TR
defining the concrete transition system. For this, we define p−1 (ŝ)[x̄] as the conjunction of
the (positive or negative) predicates corresponding to an abstract state ŝ = (b1 , . . . , bk ) ∈ D̂:
                      k
                      ^
     p−1 (ŝ)[x̄] =         (Pi [x̄] ↔ bi ) .
                      i=1

The abstract transition system is then given by:

             B̂ = {ŝ ∈ D̂ | B[x̄] ∧ p−1 (ŝ)[x̄] is T -satisfiable} ,
             ˆ = {(ŝ, ŝ′ ) ∈ D̂2 | p−1 (ŝ)[x̄] ∧ TR[x̄, x̄′ ] ∧ p−1 (ŝ′ )[x̄′ ] is T -satisfiable} .
            TR

3.3.3       Counterexample-Guided Abstraction Refinement
The key idea of the CEGAR algorithm is to refine abstractions when they are too coarse
to prove some desired property of the concrete transition system; this way, the verification
Verification Algorithms Based on Interpolation                                                        31

of some system can start with a very small, imprecise abstract transition system (e.g., the
system obtained for an empty set P0 = ∅ of predicates) and gradually refine the abstraction
until it is possible to prove the property [15]. Refinement can be seen as sub-dividing the
states of an abstract transition system, so that spurious paths are eliminated. For instance,
in Fig. 8b, the abstract state in the middle has been split into two states, this way removing
abstract paths and making the abstract state containing e unreachable from the initial state.
In general, multiple abstract states have to be split to remove paths in the abstract transition
system. Abstraction refinement can be achieved with the help of Craig interpolation [34].
       For this, suppose E[x̄] is a sentence representing error states, and Ê = {ŝ ∈ D̂ | there is s ∈
D with h(s) = ŝ and E[s]} is the corresponding abstract set. Suppose that abstract anal-
ysis with the predicates Pl has identified a path ŝ1 , ŝ2 , . . . , ŝm of states such that ŝ1 ∈ B̂,
                  ˆ for all i ∈ {1, . . . , m − 1}, and ŝm ∈ Ê, but no corresponding path exists in
(ŝi , ŝi+1 ) ∈ TR
the concrete transition system. The latter assumptions means that the formula

    B[x̄1 ] ∧ TR[x̄1 , x̄2 ] ∧ TR[x̄2 , x̄3 ] ∧ · · · ∧ TR[x̄m−1 , x̄m ] ∧ E[x̄m ]
    | {z } | {z } | {z }                                |    {z       } | {z }
      A1           A2              A3                       Am            Am+1


is T -unsatisfiable. The path ŝ0 , ŝ1 , . . . , ŝm is also called a “spurious counterexample” that can
be eliminated by adding further predicates, increasing the precision of predicate abstraction.
Let I0 , I1 , . . . , Im+1 be a sequence interpolant for the conjunction A1 ∧ · · · ∧ Am+1 . By
definition, each Ii for i ∈ {1, . . . , m} only refers to the symbols x̄i , so that we obtain m
new sentences I1 [x̄], . . . , Im [x̄] by renaming; those sentences give rise to the refined abstract
transition system, defined by Pl+1 = Pl ∪ {I1 [x̄], . . . , Im [x̄]}.
    In the refined abstract system, the spurious counterexample does not exist any more, in
the sense that there is no abstract path ŝ′1 , ŝ′2 , . . . , ŝ′m of length m to an error state. This
is due to the new predicates: in every initial state ŝ ∈ B̂, the bit corresponding to the new
predicate I1 has to be 1; therefore, in every state reachable in one step from an initial state,
the bit for I2 has to be 1, etc. Finally, the predicate Im , which is present in every state
reachable in m − 1 steps, is inconsistent with the sentence E defining error states, implying
that no paths of length m to error states are possible. There might be, of course, paths of
different length to error states, which can be removed by further refinement steps.


3.3.4      Variants of Predicate Abstraction and CEGAR
The explicit construction of abstract transition systems tends to be a time-consuming step and
is often avoided in newer implementations of CEGAR using the lazy abstraction paradigm [35].
Instead of working explicitly with abstract states, lazy abstraction constructs a reachability
graph in which every node is labeled with a Boolean combination of predicates in P, summariz-
ing a whole set of abstract states. An edge from a node n to n′ implies that the formulas ϕ, ϕ′
labeling n, n′ , respectively, satisfy ϕ[x̄] ∧ TR[x̄, x̄′ ] |=T ϕ′ [x̄′ ]. The reachability graph is built
on-the-fly during exploration, starting from the initial states, and refined when error states
32     Craig Interpolation in Program Verification

are encountered. The Impact algorithm does not even store and reuse predicates, but instead
generates new predicates (using Craig interpolation) each time a new path is considered [52].
    A further optimization, utilized in most papers on CEGAR, is to take again the control
structure of software programs into account (e.g., [35, 52, 33]). Besides leading to smaller
interpolation queries, since only one path is considered at a time, sensitivity to control flow
enables verification tools to maintain a separate set of predicates for each control location. The
even more general framework of constrained Horn clauses, described in the next section, can
handle many different kinds of control structure, including procedure calls and concurrency.


3.4     CHC: Craig Interpolation and Constrained Horn Clauses
The framework of Constrained Horn Clauses (CHCs) rephrases program verification in terms
of model construction in an extension of a theory T with additional predicates [26, 8]. CHCs
can be seen as an intermediate language that lets verification front-ends communicate in a
standardized way with verification back-ends. CHCs also subsume the extended versions of
Craig interpolation (parallel interpolants, sequence interpolants, tree interpolants) that were
defined in Section 2.1.3 and let us state a corresponding, more general result.


3.4.1      Definitions and Basic Properties
▶ Definition 17 (Constrained Horn Clause [59]). Suppose T is a theory and R a set of
relation symbols disjoint from the signature ΣT of T . A Constrained Horn Clause (CHC) is a
sentence ∀x̄. C ∧ B1 ∧ · · · ∧ Bn → H in which:
     C is a formula over ΣT that can refer to the variables x̄;
     each Bi is an application p(t1 , . . . , tk ) of a relation symbol p ∈ R to terms over ΣT and x̄;
     H is either ⊥ or an application p(t1 , . . . , tk ) of p ∈ R to terms over ΣT and x̄.

     We call C the constraint, H the head, and C ∧ B1 ∧ · · · ∧ Bn the body of the clause.
Constraints C = ⊤ are usually left out. When modeling the partial correctness of a program,
the relation symbols R are used to represent verification artifacts like inductive invariants
or contracts, while the clauses model conditions those artifacts have to satisfy. Verification
is carried out by constructing a model of the clauses, which then includes all the necessary
artifacts witnessing the correctness of the program. The algorithms we have encountered in
Section 3.2 and Section 3.3 can be adapted to work on sets of CHCs.
     This process is formalized using two notions of solvability of clauses. For the sake of
presentation, we focus again on theories T that come with a uniquely defined structure ST ,
i.e., for which the set ST = {ST } in Definition 1 is a singleton set. A set of CHCs is
called semantically solvable if the structure ST can be extended to a structure over the
signature ΣT ∪ R that satisfies all clauses, i.e., if the set of CHCs is T -satisfiable according
Verification Algorithms Based on Interpolation                                                        33

to Definition 1.1 A set of CHCs is called syntactically solvable if all clauses can be made
T -valid by uniformly substituting formulas over the signature ΣT for the relation symbols
from R [59]. Syntactic solvability is related to the classical solution problem in logic [64].

▶ Example 18. We model the Fibonacci example from Fig. 1a using CHCs. For this, we
introduce a relation symbol loop that represents the loop invariant of the function fib and
formulate clauses for the Initiation, Consecution, and Sufficiency conditions. Clause (4) tells
that the invariant should hold when entering the loop, i.e., for any value n with n ≥ 0 and
a = 0, b = 1, i = 0. Clause (5) ensures that the invariant is preserved by the loop body:
whenever loop holds for values n, a, b, i and the loop condition i < n is satisfied, loop should
also hold for the state after one loop iteration. Clause (6) ensures that whenever loop holds for
values n, a, b, i and the loop terminates due to i ≥ n, the postcondition a ≥ 0 is not violated.

                                     ∀n. n ≥ 0 → loop(n, 0, 1, 0)                                     (4)
             ∀n, a, b, i. i < n ∧ loop(n, a, b, i) → loop(n, b, a + b, i + 1)                         (5)
    ∀n, a, b, i. i ≥ n ∧ a ̸≥ 0 ∧ loop(n, a, b, i) → ⊥                                                (6)

Every syntactic solution of the clauses corresponds to an inductive loop invariant. The
existing CHC solvers, which are often interpolation-based, can easily compute such solutions;
one possible solution is the assignment {loop(n, a, b, i) 7→ a ≥ 0 ∧ b ≥ 0}, proving that the
program is partially correct. Note that a ≥ 0 ∧ b ≥ 0 coincides with the inductive invariant
that was discovered in Section 1.1.                                                         ⌟

    If a set of CHCs is syntactically solvable, then it is also semantically solvable. The converse
is not true in general, because a set of CHCs could only have models that cannot be defined
explicitly in the theory T [59]. For the fragment of recursion-free CHCs, however, the notions
of semantic and syntactic solvability coincide thanks to the Craig interpolation theorem. To
illustrate the relationship between CHCs and T -separators, consider formulas A[x̄, ȳ], B[x̄, z̄]
that only have the variables x̄ and symbols from ΣT in common, while ȳ, z̄ are local variables
that only occur in A[x̄, ȳ] or B[x̄, z̄], respectively. Consider then the CHCs ∀x̄, ȳ. A[x̄, ȳ] → I(x̄)
and ∀x̄, z̄. B[x̄, z̄] ∧ I(x̄) → ⊥. By definition, any syntactic solution of the two clauses is a
T -separator2 for the conjunction A[x̄, ȳ] ∧ B[x̄, z̄], and vice versa, implying that the two CHCs
are syntactically solvability if and only if A[x̄, ȳ] ∧ B[x̄, z̄] is T -unsatisfiable. In a similar way,
sequence interpolants and tree interpolants can be represented using sets of CHCs.


1
  For the general case of theories T with multiple structures, two definitions of semantic solvability are
  commonly used. In loose semantics [59, 8], a set of CHCs is considered semantically solvable if every
  T -structure can be extended to a structure satisfying all clauses. Existing CHC solvers more commonly
  apply the strict semantics also used by SMT solvers, which asks whether there exists some T -structure
  that can be extended to a structure satisfying all clauses. CHCs are often formulated in such a way that
  both notions of semantics lead to the same result.
2
  We consider the free variables x̄, ȳ, z̄ as constant symbols at this point.
34     Craig Interpolation in Program Verification

   To state this result more generally, for a set C of CHCs over the relation symbols R
we introduce a dependence relation →C ⊆ R2 , defining p →C q if there is a CHC in C that
contains p in the head and q in the body. The set C is called recursion-free if →C is acyclic,
and recursive otherwise.

▶ Theorem 19 (Solvability of CHCs [59]). Let C be a finite and recursion-free set of CHCs
over a theory T . Then C is semantically solvable3 if and only if it is syntactically solvable.

    To prove the direction “⇒” of this result, the recursion-free CHCs can be expanded to
obtain a disjunctive interpolation problem [58], which can be translated further to a tree
interpolation problem; the syntactic solution can be extracted from the tree interpolant
modulo T . Recursion-free CHCs are exponentially more succinct than tree interpolation
problems, however. The problem of determining whether a recursion-free set of CHCs over
the theory LIA has solutions is co-NEXPTIME-complete, while checking whether a formula
is LIA-unsatisfiable (and interpolants exist) is only co-NP-complete.
    The relationship between semantic and syntactic solvability also holds in the quantifier-free
setting, provided that the theory T admits quantifier-free interpolation:

▶ Lemma 20 (Quantifier-free solvability of CHCs). Suppose T is a theory that admits plain
quantifier-free interpolation. Let C be a finite and recursion-free set of CHCs over T in which
the constraints do not contain quantifiers. Then C is semantically solvable4 if and only if it is
syntactically solvable, with a solution that does not contain quantifiers.

3.4.2       Encoding of Recursive Programs using CHCs
Constrained Horn clauses can be used also for
                                                     1 int fibR(int n) {
inference tasks beyond just inductive invariants,
making it possible, among others, to automati-       2    if (n == 0)
                                                     3      return 0;
cally verify recursive or concurrent programs [26].
                                                     4    else if (n == 1)
Consider the program in Fig. 9, which is a re-
                                                     5      return 1;
cursive implementation of the Fibonacci function
                                                     6    else
from Section 1.1. Properties of the recursive im-
                                                     7      return fibR(n-1) + fibR(n-2);
plementation can be verified by applying the prin-
                                                     8 }
ciple of Design by Contract [53], describing the
behavior of the function using pre- and postcondi-     Figure 9 Recursive program computing
tions that serve a similar purpose as an inductive the nth element of the Fibonacci sequence.
loop invariant: every recursive call to the function
has to satisfy the precondition and can then rely on the postcondition being established by
the function upon return.


3
    For theories with multiple models, applying loose semantics as discussed in Footnote 1.
4
    As in Theorem 19, for theories with multiple models, applying loose semantics as discussed in Footnote 1.
Conclusions                                                                                   35

   We illustrate how this style of reasoning can be used to prove a property about the Fibonacci
implementation: whenever n ≥ 3, the result of the function is a number fibR(n) ≥ 2. There
are several possible ways to formulate CHCs for this recursive function [8]. Choosing an
encoding that is close to the classical Design by Contract methodology, we can reason about
the function by introducing two relation symbols pre and post, representing the pre- and
postcondition of fibR, respectively. The precondition pre(n) is a formula about the function
argument n, whereas the postcondition post(n, r) is a relation between the argument n and
the result r. We then formulate CHCs that state the properties those symbols have to satisfy:

                                                             ∀n. n ≥ 3 → pre(n)               (7)
                                                    ∀n. n = 0 ∧ pre(n) → post(n, 0)           (8)
                                           ∀n. n ̸= 0 ∧ n = 1 ∧ pre(n) → post(n, 1)           (9)
                                           ∀n. n ̸= 0 ∧ n ̸= 1 ∧ pre(n) → pre(n − 1)         (10)
                                           ∀n. n ̸= 0 ∧ n ̸= 1 ∧ pre(n) → pre(n − 2)         (11)
     ∀n, r, s. n ̸= 0 ∧ n ̸= 1 ∧ pre(n) ∧ post(n − 1, r) ∧ post(n − 2, s) → post(n, r + s)   (12)
                                      ∀n, r. n ≥ 3 ∧ r ̸≥ 2 ∧ post(n, r) → ⊥                 (13)

Clause (7) states that the contract to be derived should include inputs n ≥ 3, while (13)
expresses that the result r for an input n ≥ 3 should not be less than 2. The other clauses
encode the recursive function itself. Clauses (8) and (9) model the return statements in
lines 3 and 5 by stating that the postcondition has to hold for the result 0 and 1, respectively.
The third return statement in line 7 performs two recursive calls and gives rise to somewhat
more complicated clauses: clauses (10) and (11) ensure that the recursive calls satisfy the
precondition of the function, while (12) states that the computed sum r + s has to satisfy
the postcondition, assuming that the values r, s produced by the recursive calls satisfy the
postcondition. A solution of the clauses is given by the assignment {pre(n) 7→ n ≥ 0,
post(n, r) 7→ n ≥ 0 ∧ r ≥ 0 ∧ (r < 2 → n = 0 ∨ (n = 1 ∧ r = 1) ∨ (n = 2 ∧ r = 1))}.
    The clause (12) is called a non-linear clause, since its body contains three atoms
pre(n), post(n − 1, r), post(n − 2, s), whereas all other clauses are linear and have at most
one body atom. Non-linear clauses naturally occur when translating recursive or concurrent
programs to CHCs and are handled by CHC solvers with the help of tree interpolation.


 4      Conclusions

The chapter has explored the use of Craig interpolation in program verification, as well as
some of the techniques that have been developed for effectively computing Craig interpolants
in SMT solvers. Craig interpolation is today a standard method applied in verification tools
and there are many more directions that could be discussed, but which are beyond the scope
of the chapter, including:
36     Craig Interpolation in Program Verification

     Techniques for deriving Craig interpolants in combined theories, for instance in the
     (signature-disjoint) combination of arrays and LRA. As a sufficient criterion for quantifier-
     free interpolation in combined theories, the notion of theories being equality interpolating
     has been identified [66]. Equality interpolation was later shown to be equivalent to the
     model-theoretical notion of strong sub-amalgamation [14].
     The use of uniform interpolants in program verification, which are in this context also
     called covers [29, 23]. Uniform interpolation can be used to define a model checking
     algorithm that is similar in spirit to the IMC algorithm (Section 3.2), but in which the
     computed invariant candidates Ri are exact.
     Methods for controlling the result of Craig interpolation. In applications like verification,
     not all interpolants work equally well, and the ability of algorithms like IMC to compute
     inductive invariants strongly depends on the right interpolants being found by the applied
     interpolation procedure. To address this, methods have been developed to control the
     logical strength [19, 31], size [1], or the vocabulary [18, 47] of interpolants.


Acknowledgments
The author would like to thank Jean Christoph Jung, Sibylle Möhle-Rotondi, and Christoph
Wernhard for the careful proof-reading and helpful discussions while preparing this chap-
ter. The work on the chapter been supported by the Swedish Research Council (VR)
under grant 2021-06327, the Wallenberg project UPDATE, the Ethereum Foundation under
grant FY25-2124, and the EuroProofNet COST action.


       References
 1     Leonardo Alt, Grigory Fedyukovich, Antti E. J. Hyvärinen, and Natasha Sharygina. A proof-
       sensitive approach for small propositional interpolants. In Arie Gurfinkel and Sanjit A. Seshia,
       editors, Verified Software: Theories, Tools, and Experiments (VSTTE), volume 9593 of LNCS,
       pages 1–18. Springer, 2015. doi:10.1007/978-3-319-29613-5_1.
 2     Leo Bachmair, Ashish Tiwari, and Laurent Vigneron. Abstract congruence closure. J. Autom.
       Reason., 31(2):129–168, 2003. doi:10.1023/B:JARS.0000009518.26415.49.
 3     Peter Backeman, Philipp Rümmer, and Aleksandar Zeljic. Interpolating bit-vector formulas
       using uninterpreted predicates and Presburger arithmetic. Formal Methods Syst. Des., 57(2):121–
       156, 2021. doi:10.1007/S10703-021-00372-6.
 4     Thomas Ball, Andreas Podelski, and Sriram K. Rajamani. Boolean and Cartesian abstraction
       for model checking C programs. In Tiziana Margaria and Wang Yi, editors, Tools and Algorithms
       for the Construction and Analysis of Systems (TACAS), volume 2031 of LNCS, pages 268–283.
       Springer, 2001. doi:10.1007/3-540-45319-9_19.
 5     Clark W. Barrett, Roberto Sebastiani, Sanjit A. Seshia, and Cesare Tinelli. Satisfiability
       modulo theories. In Armin Biere, Marijn Heule, Hans van Maaren, and Toby Walsh, editors,
       Handbook of Satisfiability - Second Edition, volume 336 of Frontiers in Artificial Intelligence
       and Applications, pages 1267–1329. IOS Press, 2021. doi:10.3233/FAIA201017.
References                                                                                       37

 6   Dirk Beyer, Nian-Ze Lee, and Philipp Wendler. Interpolation and SAT-based model checking
     revisited: Adoption to software verification. J. Autom. Reason., 69(1):5, 2025. doi:10.1007/
     S10817-024-09702-9.
 7   Armin Biere, Alessandro Cimatti, Edmund M. Clarke, and Yunshan Zhu. Symbolic model
     checking without BDDs. In W. Rance Cleaveland, editor, Tools and Algorithms for the
     Construction and Analysis of Systems (TACAS), volume 1579 of LNCS, pages 193–207. Springer,
     1999. doi:10.1007/3-540-49059-0_14.
 8   Nikolaj S. Bjørner, Arie Gurfinkel, Kenneth L. McMillan, and Andrey Rybalchenko. Horn clause
     solvers for program verification. In Lev D. Beklemishev, Andreas Blass, Nachum Dershowitz,
     Bernd Finkbeiner, and Wolfram Schulte, editors, Fields of Logic and Computation II, volume
     9300 of LNCS, pages 24–51. Springer, 2015. doi:10.1007/978-3-319-23534-9_2.
 9   Aaron R. Bradley. SAT-based model checking without unrolling. In Ranjit Jhala and David
     Schmidt, editors, Verification, Model Checking, and Abstract Interpretation (VMCAI), volume
     6538 of LNCS, pages 70–87. Springer, 2011. doi:10.1007/978-3-642-18275-4_7.
10   Aaron R. Bradley and Zohar Manna. The calculus of computation - decision procedures with
     applications to verification. Springer, 2007. doi:10.1007/978-3-540-74113-8.
11   Angelo Brillout, Daniel Kroening, Philipp Rümmer, and Thomas Wahl. Beyond quantifier-free
     interpolation in extensions of Presburger arithmetic. In Ranjit Jhala and David A. Schmidt,
     editors, Verification, Model Checking, and Abstract Interpretation (VMCAI), volume 6538 of
     LNCS, pages 88–102. Springer, 2011. doi:10.1007/978-3-642-18275-4_8.
12   Angelo Brillout, Daniel Kroening, Philipp Rümmer, and Thomas Wahl. An interpolating
     sequent calculus for quantifier-free Presburger arithmetic. J. Autom. Reason., 47(4):341–367,
     2011. doi:10.1007/S10817-011-9237-Y.
13   Roberto Bruttomesso, Silvio Ghilardi, and Silvio Ranise. Rewriting-based quantifier-free
     interpolation for a theory of arrays. In Manfred Schmidt-Schauß, editor, Rewriting Techniques
     and Applications (RTA), volume 10 of LIPIcs, pages 171–186. Schloss Dagstuhl - Leibniz-
     Zentrum für Informatik, 2011. doi:10.4230/LIPICS.RTA.2011.171.
14   Roberto Bruttomesso, Silvio Ghilardi, and Silvio Ranise. Quantifier-free interpolation in
     combinations of equality interpolating theories. ACM Trans. Comput. Log., 15(1):5:1–5:34,
     2014. doi:10.1145/2490253.
15   Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. Counterexample-
     guided abstraction refinement for symbolic model checking. J. ACM, 50(5):752–794, 2003.
     doi:10.1145/876638.876643.
16   Liyun Dai, Bican Xia, and Naijun Zhan. Generating non-linear interpolants by semidef-
     inite programming. In Natasha Sharygina and Helmut Veith, editors, Computer Aided
     Verification (CAV), volume 8044 of LNCS, pages 364–380. Springer, 2013. doi:10.1007/
     978-3-642-39799-8_25.
17   Isil Dillig, Thomas Dillig, and Alex Aiken. Cuts from proofs: a complete and practical technique
     for solving linear inequalities over integers. Formal Methods Syst. Des., 39(3):246–260, 2011.
     doi:10.1007/S10703-011-0127-Z.
18   Vijay D’Silva. Propositional interpolation and abstract interpretation. In Andrew D. Gordon,
     editor, European Symposium on Programming (ESOP), volume 6012 of LNCS, pages 185–204.
     Springer, 2010. doi:10.1007/978-3-642-11957-6_11.
38   Craig Interpolation in Program Verification

19   Vijay Victor D’Silva, Daniel Kroening, Mitra Purandare, and Georg Weissenbacher. Interpolant
     strength. In Gilles Barthe and Manuel V. Hermenegildo, editors, Verification, Model Checking,
     and Abstract Interpretation (VMCAI), volume 5944 of LNCS, pages 129–145. Springer, 2010.
     doi:10.1007/978-3-642-11319-2_12.
20   Bruno Dutertre and Leonardo Mendonça de Moura. A fast linear-arithmetic solver for DPLL(T).
     In Thomas Ball and Robert B. Jones, editors, Computer Aided Verification (CAV), volume
     4144 of LNCS, pages 81–94. Springer, 2006. doi:10.1007/11817963_11.
21   Cormac Flanagan and James B. Saxe. Avoiding exponential explosion: generating compact
     verification conditions. In Chris Hankin and Dave Schmidt, editors, Principles of Programming
     Languages (POPL), pages 193–205. ACM, 2001. doi:10.1145/360204.360220.
22   Alexander Fuchs, Amit Goel, Jim Grundy, Sava Krstic, and Cesare Tinelli. Ground interpolation
     for the theory of equality. Log. Methods Comput. Sci., 8(1), 2012. doi:10.2168/LMCS-8(1:
     6)2012.
23   Alessandro Gianola. Uniform interpolation for the automated verification of data-aware business
     processes. In Luca Geatti, Guido Sciavicco, and Alessandro Umbrico, editors, Workshop on
     Artificial Intelligence and Formal Verification, Logic, Automata, and Synthesis, volume 3311 of
     CEUR Workshop Proceedings, pages 73–79. CEUR-WS.org, 2022.
24   Susanne Graf and Hassen Saïdi. Construction of abstract state graphs with PVS. In Orna
     Grumberg, editor, Computer Aided Verification (CAV), volume 1254 of LNCS, pages 72–83.
     Springer, 1997. doi:10.1007/3-540-63166-6_10.
25   Ronald L. Graham, Donald E. Knuth, and Oren Patashnik. Concrete Mathematics: A
     Foundation for Computer Science, 2nd Ed. Addison-Wesley, 1994.
26   Sergey Grebenshchikov, Nuno P. Lopes, Corneliu Popeea, and Andrey Rybalchenko. Synthe-
     sizing software verifiers from proof rules. In Jan Vitek, Haibo Lin, and Frank Tip, editors,
     Programming Language Design and Implementation (PLDI), pages 405–416. ACM, 2012.
     doi:10.1145/2254064.2254112.
27   Alberto Griggio, Thi Thieu Hoa Le, and Roberto Sebastiani. Efficient interpolant generation
     in satisfiability modulo linear integer arithmetic. Log. Methods Comput. Sci., 8(3), 2010.
     doi:10.2168/LMCS-8(3:3)2012.
28   Orna Grumberg. Abstraction and refinement in model checking. In Frank S. de Boer,
     Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever, editors, Formal Methods
     for Components and Objects (FMCO), volume 4111 of LNCS, pages 219–242. Springer, 2005.
     doi:10.1007/11804192_11.
29   Sumit Gulwani and Madan Musuvathi. Cover algorithms and their combination. In Sophia
     Drossopoulou, editor, European Symposium on Programming (ESOP), volume 4960 of LNCS,
     pages 193–207. Springer, 2008. doi:10.1007/978-3-540-78739-6_16.
30   Ashutosh Gupta, Corneliu Popeea, and Andrey Rybalchenko. Solving recursion-free Horn
     clauses over LI+UIF. In Hongseok Yang, editor, Programming Languages and Systems (APLAS),
     volume 7078 of LNCS, pages 188–203. Springer, 2011. doi:10.1007/978-3-642-25318-8_16.
31   Arie Gurfinkel, Simone Fulvio Rollini, and Natasha Sharygina. Interpolation properties and
     SAT-based model checking. In Dang Van Hung and Mizuhito Ogawa, editors, Automated
     Technology for Verification and Analysis (ATVA), volume 8172 of LNCS, pages 255–271.
     Springer, 2013. doi:10.1007/978-3-319-02444-8_19.
References                                                                                       39

32   John Harrison. Handbook of Practical Logic and Automated Reasoning. Cambridge University
     Press, 2009.
33   Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. Nested interpolants. In Manuel V.
     Hermenegildo and Jens Palsberg, editors, Principles of Programming Languages (POPL), pages
     471–482. ACM, 2010. doi:10.1145/1706299.1706353.
34   Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Kenneth L. McMillan. Abstractions
     from proofs. In Neil D. Jones and Xavier Leroy, editors, Principles of Programming Languages
     (POPL), pages 232–244. ACM, 2004. doi:10.1145/964001.964021.
35   Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Grégoire Sutre. Lazy abstraction.
     In John Launchbury and John C. Mitchell, editors, Principles of Programming Languages
     (POPL), pages 58–70. ACM, 2002. doi:10.1145/503272.503279.
36   Jochen Hoenicke and Tanja Schindler. Efficient interpolation for the theory of arrays. In Didier
     Galmiche, Stephan Schulz, and Roberto Sebastiani, editors, Automated Reasoning (IJCAR),
     volume 10900 of LNCS, pages 549–565. Springer, 2018. doi:10.1007/978-3-319-94205-6_36.
37   Hossein Hojjat and Philipp Rümmer. Deciding and interpolating algebraic data types by
     reduction. In Tudor Jebelean, Viorel Negru, Dana Petcu, Daniela Zaharie, Tetsuo Ida,
     and Stephen M. Watt, editors, Symbolic and Numeric Algorithms for Scientific Computing
     (SYNASC), pages 145–152. IEEE Computer Society, 2017. doi:10.1109/SYNASC.2017.00033.
38   Himanshu Jain, Edmund M. Clarke, and Orna Grumberg. Efficient Craig interpolation for
     linear Diophantine (dis)equations and linear modular equations. Formal Methods Syst. Des.,
     35(1):6–39, 2009. doi:10.1007/S10703-009-0069-X.
39   Ranjit Jhala and Kenneth L. McMillan. Interpolant-based transition relation approximation.
     Log. Methods Comput. Sci., 3(4), 2007. doi:10.2168/LMCS-3(4:1)2007.
40   Dejan Jovanovic and Bruno Dutertre. Interpolation and model checking for nonlinear arithmetic.
     In Alexandra Silva and K. Rustan M. Leino, editors, Computer Aided Verification (CAV),
     volume 12760 of LNCS, pages 266–288. Springer, 2021. URL: https://doi.org/10.1007/
     978-3-030-81688-9_13, doi:10.1007/978-3-030-81688-9_13.
41   Deepak Kapur, Rupak Majumdar, and Calogero G. Zarba. Interpolation for data structures.
     In Michal Young and Premkumar T. Devanbu, editors, Foundations of Software Engineering
     (FSE), pages 105–116. ACM, 2006. doi:10.1145/1181775.1181789.
42   Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. SMT-based model checking for recursive
     programs. Formal Methods Syst. Des., 48(3):175–205, 2016. doi:10.1007/S10703-016-0249-4.
43   George Kourousias and David Makinson. Parallel interpolation, splitting, and relevance in
     belief change. Journal of Symbolic Logic, 72(3):994–1002, 2007. doi:10.2178/jsl/1191333851.
44   Laura Kovács and Andrei Voronkov. Interpolation and symbol elimination. In Renate A.
     Schmidt, editor, Automated Deduction (CADE), volume 5663 of LNCS, pages 199–213. Springer,
     2009. doi:10.1007/978-3-642-02959-2_17.
45   Daniel Kroening, Jérôme Leroux, and Philipp Rümmer. Interpolating quantifier-free Presburger
     arithmetic. In Christian G. Fermüller and Andrei Voronkov, editors, Logic for Programming,
     Artificial Intelligence, and Reasoning (LPAR), volume 6397 of LNCS, pages 489–503. Springer,
     2010. doi:10.1007/978-3-642-16242-8_35.
46   Serge Lang. Algebra (3. ed.). Addison-Wesley, 1993.
40   Craig Interpolation in Program Verification

47   Jérôme Leroux, Philipp Rümmer, and Pavle Subotic. Guiding Craig interpolation with
     domain-specific abstractions. Acta Informatica, 53(4):387–424, 2016. doi:10.1007/
     S00236-015-0236-Z.
48   John McCarthy. Towards a mathematical science of computation. In C. M. Popplewell, editor,
     Information Processing 1962: Proceedings IFIP Congress 62, pages 21–28, Amsterdam, 1963.
     North Holland.
49   Kenneth L. McMillan. Interpolation and SAT-based model checking. In Warren A. Hunt Jr.
     and Fabio Somenzi, editors, Computer Aided Verification (CAV), volume 2725 of LNCS, pages
     1–13. Springer, 2003. doi:10.1007/978-3-540-45069-6_1.
50   Kenneth L. McMillan. Applications of Craig interpolants in model checking. In Nicolas
     Halbwachs and Lenore D. Zuck, editors, Tools and Algorithms for the Construction and
     Analysis of Systems (TACAS), volume 3440 of LNCS, pages 1–12. Springer, 2005. doi:
     10.1007/978-3-540-31980-1_1.
51   Kenneth L. McMillan. An interpolating theorem prover. Theor. Comput. Sci., 345(1):101–121,
     2005. doi:10.1016/J.TCS.2005.07.003.
52   Kenneth L. McMillan. Lazy abstraction with interpolants. In Thomas Ball and Robert B.
     Jones, editors, Computer Aided Verification (CAV), volume 4144 of LNCS, pages 123–136.
     Springer, 2006. doi:10.1007/11817963_14.
53   Bertrand Meyer. Applying “Design by Contract”. IEEE Computer, 25(10):40–51, 1992.
     doi:10.1109/2.161279.
54   Rohit Parikh. Beth definability, interpolation and language splitting. Synth., 179(2):211–221,
     2011. doi:10.1007/S11229-010-9778-3.
55   Pavel Pudlák. Lower bounds for resolution and cutting plane proofs and monotone computations.
     J. Symb. Log., 62(3):981–998, 1997. doi:10.2307/2275583.
56   William Pugh. The Omega test: a fast and practical integer programming algorithm for
     dependence analysis. In Joanne L. Martin, editor, Supercomputing (SC), pages 4–13, New York,
     NY, USA, 1991. ACM.
57   Philipp Rümmer. A constraint sequent calculus for first-order logic with linear integer arithmetic.
     In Iliano Cervesato, Helmut Veith, and Andrei Voronkov, editors, Logic for Programming,
     Artificial Intelligence, and Reasoning (LPAR), volume 5330 of LNCS, pages 274–289. Springer,
     2008. doi:10.1007/978-3-540-89439-1_20.
58   Philipp Rümmer, Hossein Hojjat, and Viktor Kunčak. Disjunctive interpolants for Horn-clause
     verification. In Computer Aided Verification (CAV), volume 8044 of LNCS, pages 347–363.
     Springer, 2013. doi:10.1007/978-3-642-39799-8_24.
59   Philipp Rümmer, Hossein Hojjat, and Viktor Kunčak. On recursion-free Horn clauses and Craig
     interpolation. Formal Methods Syst. Des., 47(1):1–25, 2015. doi:10.1007/S10703-014-0219-7.
60   Andrey Rybalchenko and Viorica Sofronie-Stokkermans. Constraint solving for interpolation.
     J. Symb. Comput., 45(11):1212–1233, 2010. doi:10.1016/J.JSC.2010.06.005.
61   Alexander Schrijver. Theory of linear and integer programming. John Wiley & Sons, 1998.
62   Nishant Totla and Thomas Wies. Complete instantiation-based interpolation. In Roberto
     Giacobazzi and Radhia Cousot, editors, Principles of Programming Languages (POPL), pages
     537–548. ACM, 2013. doi:10.1145/2429069.2429132.
References                                                                                   41

63   Yakir Vizel and Orna Grumberg. Interpolation-sequence based model checking. In Armin Biere
     and Carl Pixley, editors, Formal Methods in Computer-Aided Design (FMCAD), pages 1–8.
     IEEE, 2009. doi:10.1109/FMCAD.2009.5351148.
64   Christoph Wernhard. The Boolean solution problem from the perspective of predicate logic. In
     Clare Dixon and Marcelo Finger, editors, Frontiers of Combining Systems (FroCoS), volume
     10483 of LNCS, pages 333–350. Springer, 2017. doi:10.1007/978-3-319-66167-4_19.
65   Hao Wu, Jie Wang, Bican Xia, Xiakun Li, Naijun Zhan, and Ting Gan. Nonlinear Craig inter-
     polant generation over unbounded domains by separating semialgebraic sets. In André Platzer,
     Kristin Yvonne Rozier, Matteo Pradella, and Matteo Rossi, editors, Formal Methods (FM),
     volume 14933 of LNCS, pages 92–110. Springer, 2024. doi:10.1007/978-3-031-71162-6_5.
66   Greta Yorsh and Madanlal Musuvathi. A combination method for generating interpolants.
     In Robert Nieuwenhuis, editor, Automated Deduction (CADE), volume 3632 of LNCS, pages
     353–368. Springer, 2005. doi:10.1007/11532231_26.
