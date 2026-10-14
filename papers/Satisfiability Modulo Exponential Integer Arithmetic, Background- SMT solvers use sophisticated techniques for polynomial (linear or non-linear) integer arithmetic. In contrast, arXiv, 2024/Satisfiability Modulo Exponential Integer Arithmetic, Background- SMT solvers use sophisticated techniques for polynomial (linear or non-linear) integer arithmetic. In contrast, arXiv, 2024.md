                                         Satisfiability Modulo Exponential Integer Arithmetic
                                         FLORIAN FROHN, RWTH Aachen University, Germany
                                         JÜRGEN GIESL, RWTH Aachen University, Germany
                                         Background: SMT solvers use sophisticated techniques for polynomial (linear or non-linear) integer arithmetic. In contrast,
                                         non-polynomial integer arithmetic has mostly been neglected so far. However, in the context of program verification,
                                         polynomials are often insufficient to capture the behavior of the analyzed system without resorting to approximations. In
                                         particular, exponentials are often required to facilitate precise reasoning (without approximations).
                                         Objectives: We introduce EIA, an SMT theory for integer arithmetic with exponentiation, as well as a technique to analyze
arXiv:2402.01501v4 [cs.LO] 28 Aug 2025




                                         satisfiability of EIA problems. Moreover, we provide a set of EIA benchmarks and an implementation of our approach.
                                         Methods: In the last years, incremental linearization has been applied successfully to satisfiability modulo real arithmetic
                                         with transcendental functions. We adapt this approach to an extension of polynomial integer arithmetic with exponential
                                         functions. Here, the key challenge is to compute suitable lemmas that eliminate the current model from the search space if it
                                         violates the semantics of exponentiation. We implemented our approach in the novel tool SwInE.
                                         Results: We evaluate our approach empirically on several sets of benchmarks from different domains: Most of them stem
                                         from program verification, and one set stems from recurrence solving. On all sets, our approach is highly effective in practice.
                                         Conclusions: We develop a novel approach for satisfiability modulo exponential integer arithmetic. With SwInE, we provide
                                         an SMT-LIB compliant open-source solver for EIA that demonstrates that our approach is effective in practice. In this way, we
                                         hope to attract users with applications that give rise to challenging benchmarks, and we hope that other solvers with support
                                         for integer exponentiation will follow, with the ultimate goal of standardizing EIA.

                                         1   Introduction
                                         Traditionally, automated reasoning techniques for integers focus on polynomial arithmetic. This is not only true
                                         in the context of SMT, but also for program verification techniques, since the latter often search for polynomial
                                         invariants that imply the desired properties. As invariants are over-approximations, they are well suited for
                                         proving “universal” properties like safety, termination, or upper bounds on the worst-case runtime that refer to
                                         all possible program runs. However, proving dual properties like unsafety, non-termination, or lower bounds
                                         requires under-approximations, so that invariants are of limited use here.
                                            For lower bounds, an infinite set of witnesses is needed, as the runtime w.r.t. a finite set of (terminating) program
                                         runs is always bounded by a constant. Thus, to prove non-constant lower bounds, symbolic under-approximations
                                         are required, i.e., formulas that describe an infinite subset of the reachable states. However, polynomial arithmetic
                                         is often insufficient to express such approximations. To see this, consider the program
                                                                  𝑥 ← 1; 𝑦 ← nondet(0, ∞); while 𝑦 > 0 do 𝑥 ← 3 · 𝑥; 𝑦 ← 𝑦 − 1 done
                                         where nondet(0, ∞) returns a natural number non-deterministically. Here, the set of reachable states after
                                         execution of the loop is characterized by the formula
                                                                                               ∃𝑛 ∈ N. 𝑥 = 3𝑛 ∧ 𝑦 = 0.                                                       (1)
                                         In recent work, acceleration techniques have successfully been used to deduce lower runtime bounds automatically
                                         [18, 22]. While they can easily derive a formula like (1) from the code above, this is of limited use, as most1 SMT
                                         solvers cannot handle terms of the form 3𝑛 . Besides lower bounds, acceleration has also successfully been used
                                         1 CVC5 uses a dedicated solver for integer exponentiation with base 2.


                                         Authors’ Contact Information: Florian Frohn, orcid: http://orcid.org/0000-0003-0902-1994, florian.frohn@informatik.rwth-aachen.de, RWTH
                                         Aachen University, Aachen, Germany; Jürgen Giesl, orcid: http://orcid.org/0000-0003-0283-8520, giesl@informatik.rwth-aachen.de, RWTH
                                         Aachen University, Aachen, Germany.
2   • F. Frohn, J. Giesl


for proving non-termination [16, 22, 23] and (un)safety [4, 7, 8, 19, 32, 34], where its strength is finding long
counterexamples that are challenging for other techniques.
   Importantly, exponentiation is not just “yet another function” that can result from applying acceleration
techniques. There are well-known, important classes of loops where polynomials and exponentiation always
suffice to represent the values of the program variables after executing a loop [17, 30]. Thus, the lack of support
for integer exponentiation in SMT solvers is a major obstacle for the further development of acceleration-based
verification techniques.
   In this work, we first define a novel SMT theory for integer arithmetic with exponentiation. Then we show
how to lift standard SMT solvers to this new theory, resulting in our novel tool SwInE (SMT with Integer
Exponentiation).
   Our technique is inspired by incremental linearization, which has been applied successfully to real arithmetic
with transcendental functions, including the natural exponential function exp𝑒 (𝑥) = 𝑒 𝑥 , where 𝑒 is Euler’s number
[12]. In this setting, incremental linearization considers exp𝑒 as an uninterpreted function. If the resulting SMT
problem is unsatisfiable, then so is the original problem. If it is satisfiable and the model that was found for exp𝑒
coincides with the semantics of exponentiation, then the original problem is satisfiable. Otherwise, lemmas about
exp𝑒 that rule out the current model are added to the SMT problem, and then its satisfiability is checked again.
The name “incremental linearization” is due to the fact that these lemmas only contain linear arithmetic.
   The main challenge for adapting this approach to integer exponentiation is to generate suitable lemmas, see
Sect. 4.2. Except for monotonicity lemmas, none of the lemmas of Cimatti et al. easily carry over to our setting. In
contrast to Cimatti et al., we do not restrict ourselves to linear lemmas, but we also use non-linear, polynomial
lemmas. This is due to the fact that we consider a binary version 𝜆𝑥, 𝑦. 𝑥 𝑦 of exponentiation, whereas Cimatti
et al. fix the base to 𝑒. Thus, in our setting, one obtains bilinear lemmas that are linear w.r.t. 𝑥 as well as 𝑦, but may
contain multiplication between 𝑥 and 𝑦 (i.e., they may contain the subterm 𝑥 · 𝑦). More precisely, bilinear lemmas
arise from bilinear interpolation, which is a crucial ingredient of our approach, as it allows us to eliminate any
model that violates the semantics of exponentiation (Thm. 27). Therefore, the name “incremental linearization”
does not fit to our approach, which is rather an instance of “counterexample-guided abstraction refinement”
(CEGAR, [14]).
   A preliminary shorter version of this paper appeared at IJCAR 2024 [24]. The current paper contains the
following, yet unpublished contributions:
      • We present two new kinds of lemmas, called prime lemmas and induction lemmas.
      • We present a new technique called phasing, which alternates between a sat-phase where the solver
        searches for a model within a restricted part of the search space, and an unsat-phase where the solver
        aims for proving unsatisfiability.
      • While Frohn and Giesl [24] did not give any proofs, we now present proofs for all lemmas and theorems.
      • We present a reimplementation of SwInE, called SwInE-Z3 in the sequel, which directly builds on top of
        the API of the SMT solver Z3 [38]. In contrast, the original implementation of Frohn and Giesl [24] was
        built on top of SMT-Switch [36], a library that offers a unified interface for various SMT solvers. However,
        the evaluation of Frohn and Giesl [24] showed that Z3 performs best in our setting, so that using its API
        directly allows for improving robustness.2
      • We present a novel collection of challenging unsatisfiable benchmarks, which were obtained from verifying
        solutions for recurrence relations.


2 For example, SwInE uses the parser of SMT-Switch, which strictly adheres to the SMT-LIB standard. In contrast, Z3 (and thus SwInE-Z3) can

often also parse inputs that violate the SMT-LIB standard in a way that does not introduce ambiguity.
                                                                      Satisfiability Modulo Exponential Integer Arithmetic   •   3


     • We improve and extend our evaluation by including our novel benchmarks and the tools SwInE-Z3 and
       Z3. In order to use Z3 for integer exponentiation, we axiomatize the semantics of exponentiation via
       universally quantified assertions.
To summarize, our contributions are as follows: We first propose the new SMT theory EIA for integer arithmetic
with exponentiation (Sect. 3). Then, based on novel techniques for generating suitable lemmas, we develop a
CEGAR approach for EIA (Sect. 4). Next, we show how to improve our approach via phasing (Sect. 5). After
discussing related work (Sect. 6), we discuss two open-source implementations of our approach, one on top of
SMT-Switch [26], and one on top of Z3 [27], and we present an experimental evaluation on several collections of
EIA benchmarks that we synthesized from verification problems and from recurrence solving. Our experiments
show that our approach is highly effective in practice (Sect. 7). We refer to App. A for those (parts of the) proofs
that were omitted from the main part of the paper.

2   Preliminaries
We are working in the setting of SMT-LIB logic [5], a variant of many-sorted first-order logic with equality. We
now introduce a reduced variant of SMT-LIB logic, where we only explain those concepts that are relevant for
our work.
   In SMT-LIB logic, there is a dedicated Boolean sort Bool, and hence formulas are just terms of sort Bool.
Similarly, there is no distinction between predicates and functions, as predicates are simply functions with results
of sort Bool.
   So in SMT-LIB logic, a signature Σ = (Σ𝑆 , Σ𝐹 , Σ𝑅 ) consists of a set Σ𝑆 of sorts, a set Σ𝐹 of function symbols,
and a ranking function Σ𝑅 : Σ𝐹 → (Σ𝑆 ) + . The meaning of Σ𝑅 (𝑓 ) = (𝑠 1, . . . , 𝑠𝑘 ) is that 𝑓 is a function which
maps arguments of the sorts 𝑠 1, . . . , 𝑠𝑘 −1 to a result of sort 𝑠𝑘 . We write 𝑓 : 𝑠 1 . . . 𝑠𝑘 instead of “𝑓 ∈ Σ𝐹 and
Σ𝑅 (𝑓 ) = (𝑠 1, . . . , 𝑠𝑘 )” if Σ is clear from the context. We always allow to implicitly extend Σ with arbitrarily many
constant function symbols (i.e., function symbols 𝑥 where |Σ𝑅 (𝑥)| = 1). Note that SMT-LIB logic only considers
closed terms, i.e., terms without free variables, and we are only concerned with quantifier-free formulas, so in
our setting, all formulas are ground. Therefore, we refer to these constant function symbols as variables to avoid
confusion with other, predefined constant function symbols like true, 0, 1, . . ., see below.
   Every SMT-LIB signature is an extension of ΣBool where Σ𝑆Bool = {Bool} and Σ𝐹Bool consists of the following
function symbols:

                   true, false : Bool       ¬ : Bool Bool        ∧, ∨, =⇒ , ⇐⇒ : Bool Bool Bool

Note that SMT-LIB logic only considers well-sorted terms. A Σ-structure A consists of a universe 𝐴 = 𝑠 ∈Σ𝑆 𝐴𝑠 and
                                                                                                              Ð
an interpretation function that maps each function symbol 𝑓 : 𝑠 1 . . . 𝑠𝑘 to a function J𝑓 KA : 𝐴𝑠1 × . . . ×𝐴𝑠𝑘 −1 → 𝐴𝑠𝑘 .
SMT-LIB logic only considers structures where 𝐴Bool = {true, false} and all function symbols from ΣBool are
interpreted as usual.
   A Σ-theory is a class of Σ-structures. For example, consider the extension ΣInt of ΣBool with the additional sort
Int and the following function symbols:

                                𝑐 : Int                             for all 𝑐 ∈ N
                  +, −, ·, div, mod: Int Int Int
                  <, ≤, >, ≥, =, ≠: Int Int Bool
                       divisible𝑐 : Int Bool                        for all 𝑐 ∈ N>0 = {𝑛 ∈ N | 𝑛 > 0}
4 •    F. Frohn, J. Giesl


Then the ΣInt -theory non-linear integer arithmetic (NIA)3 contains all ΣInt -structures A where 𝐴Int = Z,
                                                       (
                                                A        true if 𝑥 mod 𝑐 = 0
                                   Jdivisible𝑐 K (𝑥) =
                                                         false otherwise,

and all other symbols from ΣInt are interpreted as usual.4
   If A is a Σ-structure and Σ′ is a subsignature of Σ, then the reduct of A to Σ′ is the unique Σ′ -structure that
interprets its function symbols like A. So the theory linear integer arithmetic (LIA) consists of the reducts of all
elements of NIA to ΣLIA = ΣInt \ {·, div, mod}.5
   Given a Σ-structure A and a Σ-term 𝑡, the meaning J𝑡KA of 𝑡 results from interpreting all function symbols
according to A. For function symbols 𝑓 whose interpretation is fixed by a Σ-theory T , we denote 𝑓 ’s interpretation
by J𝑓 K T . Given a Σ-theory T , a Σ-formula 𝜑 (i.e., a Σ-term of sort Bool) is satisfiable in T if there is an A ∈ T
such that J𝜑KA = true. Then A is called a model of 𝜑, written A |= 𝜑. If every A ∈ T is a model of 𝜑, then 𝜑 is
T -valid, written |= T 𝜑. We write 𝜓 ≡ T 𝜑 for |= T 𝜓 ⇐⇒ 𝜑.
   We sometimes also consider uninterpreted functions. Then the signature may not only contain the function
symbols of the theory under consideration and variables, but also additional non-constant function symbols.
   We write “term”, “structure”, “theory”, . . . instead of “Σ-term”, “Σ-structure”, “Σ-theory”, . . . if Σ is irrelevant or
clear from the context. Similarly, we just write “≡” and “valid” instead of “≡ T ” and “T -valid” if T is clear from
the context. Moreover, we use unary minus and 𝑡 𝑐 (where 𝑡 is a term of sort Int and 𝑐 ∈ N) as syntactic sugar,
and we write binary function symbols in infix notation.
   In the sequel, we use 𝑥, 𝑦, 𝑧, . . . for variables, 𝑠, 𝑡, 𝑝, 𝑞, . . . for terms of sort Int, 𝜑,𝜓, . . . for formulas, and
𝑎, 𝑏, 𝑐, 𝑑, . . . for integers.

3     The SMT Theory EIA
We now introduce our novel SMT theory for exponential integer arithmetic. To this end, we define the signature
 exp
ΣInt , which extends ΣInt with
                                            exp : Int Int Int.
If the 2𝑛𝑑 argument of exp is non-negative, then its semantics is as expected, i.e., we are interested in structures A
such that JexpKA (𝑐, 𝑑) = 𝑐 𝑑 for all 𝑑 ≥ 0. However, if the 2𝑛𝑑 argument is negative, then we have to use different
semantics. The reason is that we may have 𝑐 𝑑 ∉ Z if 𝑑 < 0. Intuitively, exp should be a partial function, but all
functions are total in SMT-LIB logic. We solve this problem by interpreting exp(𝑐, 𝑑) as 𝑐 |𝑑 | . This semantics has
previously been used in the literature, and the resulting logic admits a known decidable fragment [6].
                                                                                                           exp
Definition 1 (EIA). The theory exponential integer arithmetic (EIA) contains all ΣInt -structures A with

                                                            JexpKA (𝑐, 𝑑) = 𝑐 |𝑑 |
whose reduct to ΣInt is in NIA.
3 As we only consider quantifier-free formulas, we omit the prefix “QF_” in theory names and write, e.g., NIA instead of QF_NIA. Barrett et al.

[5] call QF_NIA an SMT-LIB logic, which restricts the (first-order) theory of integer arithmetic to the quantifier-free fragment. For simplicity,
we do not distinguish between SMT-LIB logics and theories.
4 Note that all functions are total in SMT-LIB logic. So div and mod are interpreted as integer division and modulo, respectively, if their second

argument is non-zero. If the second argument is zero, then the interpretation of div and mod is arbitrary, i.e., 𝜆𝑥 . 𝑥 div 0 and 𝜆𝑥 . 𝑥 mod 0
are treated like uninterpreted functions.
5 Note that Σ
              LIA indeed contains the predicates divisible𝑐 , as LIA would not admit quantifier elimination without them. To see this, consider
the formula 𝜑 := ∃𝑦. 𝑥 = 𝑦 + 𝑦. It is equivalent to divisible2 (𝑥 ), but there is no quantifier-free LIA formula without divisibility predicates
which is equivalent to 𝜑.
                                                                   Satisfiability Modulo Exponential Integer Arithmetic   •    5


 Algorithm 1: CEGAR for EIA
              exp
   Input: a ΣInt -formula 𝜑
   // Preprocessing
 1 do
 2    𝜑′ ← 𝜑
 3    𝜑 ← FoldConstants(𝜑)
 4    𝜑 ← Rewrite(𝜑)
 5 while 𝜑 ≠ 𝜑
                ′

   // Refinement Loop
 6 while there is a NIA-model A of 𝜑
 7    if A is a counterexample then
 8        L←∅
 9        for k ∈ {Symmetry, Monotonicity, Bounding, Prime, Induction, Interpolation}
10             L ← L ∪ ComputeLemmas(𝜑, k)
                     Ó
11        𝜑 ← 𝜑 ∧ {𝜓 ∈ L | A ̸ |= 𝜓 }
12    else return sat
13 return unsat



   Alternatively, one could treat exp(𝑐, 𝑑) like an uninterpreted function if 𝑑 is negative. Doing so would be
analogous to the treatment of division by zero in SMT-LIB logic. Then, e.g., exp(0, −1) ≠ exp(0, −2) would be
satisfied by a structure A with JexpKA (𝑐, 𝑑) = 𝑐 𝑑 if 𝑑 ≥ 0 and JexpKA (𝑐, 𝑑) = 𝑑, otherwise. However, the drawback
of this approach is that important laws of exponentiation like
                                          exp(exp(𝑥, 𝑦), 𝑧) = exp(𝑥, 𝑦 · 𝑧)
would not be valid. Thus, we focus on the semantics from Def. 1.

4   Solving EIA Problems via CEGAR
We now explain our technique for solving EIA problems, see Alg. 1. Our goal is to (dis)prove satisfiability of 𝜑 in
EIA. The loop in Line 6 is a CEGAR loop which lifts an SMT solver for NIA (which is called in Line 6) to EIA. So
the abstraction consists of using NIA- instead of EIA-models. Hence, exp is considered to be an uninterpreted
function in Line 6, i.e., the SMT solver also searches for an interpretation of exp. If the model found by the SMT
solver is a counterexample (i.e., if JexpKA conflicts with JexpKEIA ), then the formula under consideration is refined
by adding suitable lemmas in Lines 9 – 11 and the loop is iterated again.
Definition 2 (Counterexample). We call a NIA-model A of 𝜑 a counterexample if there is a subterm exp(𝑠, 𝑡) of 𝜑
                                       A
such that Jexp(𝑠, 𝑡)KA ≠ (J𝑠KA ) | J𝑡 K | .
   In the sequel, we first discuss our preprocessings (first loop in Alg. 1) in Sect. 4.1. Then we explain our
refinement (Lines 8 – 11) in Sect. 4.2. Here, we first introduce the different kinds of lemmas that are used by
our implementation in Sect. 4.2.1 – 4.2.6. If implemented naively, the number of lemmas can get quite large, so
we explain how to generate lemmas lazily in Sect. 4.3. Finally, we conclude this section by stating important
properties of Alg. 1.
Example 3 (Leading Example). To illustrate our approach, we show how to prove
                        ∀𝑥, 𝑦. |𝑥 | > 2 ∧ |𝑦| > 2 =⇒ exp(exp(𝑥, 𝑦), 𝑦) ≠ exp(𝑥, exp(𝑦, 𝑦)).                                   (2)
6   • F. Frohn, J. Giesl


Here, we also consider negative values for 𝑥 and 𝑦 (i.e., we use the premise |𝑥 | > 2∧|𝑦| > 2 instead of 𝑥 > 2∧𝑦 > 2)
to illustrate how our techniques works when exp is used with negative arguments. To prove (2), we encode
absolute values suitably6 and prove unsatisfiability of its negation:

                                   𝑥 2 > 4 ∧ 𝑦 2 > 4 ∧ exp(exp(𝑥, 𝑦), 𝑦) = exp(𝑥, exp(𝑦, 𝑦))

4.1    Preprocessings
In the first loop of Alg. 1, we preprocess 𝜑 by alternating constant folding (Line 3) and rewriting (Line 4) until a
fixpoint is reached. Constant folding evaluates subexpressions without variables, where subexpressions exp(𝑐, 𝑑)
are evaluated to 𝑐 |𝑑 | , i.e., according to the semantics of EIA. Rewriting reduces the number of occurrences of exp
via the following (terminating) rewrite rules:

                                                    exp(𝑥, 𝑐) → 𝑥 |𝑐 |                   if 𝑐 ∈ Z
                                           exp(exp(𝑥, 𝑦), 𝑧) → exp(𝑥, 𝑦 · 𝑧)
                                       exp(𝑥, 𝑦) · exp(𝑧, 𝑦) → exp(𝑥 · 𝑧, 𝑦)

In particular, the 1𝑠𝑡 rule allows us to rewrite7 exp(𝑠, 0) to 𝑠 0 = 1 and exp(𝑠, 1) to 𝑠 1 = 𝑠. Note that the rule

                                               exp(𝑥, 𝑦) · exp(𝑥, 𝑧) → exp(𝑥, 𝑦 + 𝑧)

would be unsound, as the right-hand side would need to be exp(𝑥, |𝑦| + |𝑧|) instead.

Example 4 (Preprocessing). For our leading example, applying the 2𝑛𝑑 rewrite rule at the underlined position
yields:

                                      𝑥 2 > 4 ∧ 𝑦 2 > 4 ∧ exp(exp(𝑥, 𝑦), 𝑦) = exp(𝑥, exp(𝑦, 𝑦))
                                  → 𝑥 2 > 4 ∧ 𝑦 2 > 4 ∧ exp(𝑥, 𝑦 2 ) = exp(𝑥, exp(𝑦, 𝑦))                                       (3)

Lemma 5. We have 𝜑 ≡EIA FoldConstants(𝜑) and 𝜑 ≡EIA Rewrite(𝜑).

   Proof. For constant folding, the claim is trivial, so we only have to show 𝜑 ≡EIA Rewrite(𝜑). To this end, it
suffices to show JℓKA = J𝑟 KA for all rewrite rules ℓ → 𝑟 and all A ∈ EIA. Let A ∈ EIA be arbitrary but fixed and
let J. . .K denote J. . .KA .
                                                                                                    |𝑐 | times
                                                                                                    z }| {
    For the first rewrite rule exp(𝑥, 𝑐) → 𝑥 |𝑐 | , recall that 𝑥 |𝑐 | is syntactic sugar for 𝑥 · . . . · 𝑥, i.e., we have to show
                    |𝑐 | times
               z }| {
Jexp(𝑥, 𝑐)K = J𝑥 · . . . · 𝑥K. We obtain
                                                                            |𝑐 | times    |𝑐 | times
                                                                      z }| {             z }| {
                                                   | J𝑐 K |      |𝑐 |
                                 Jexp(𝑥, 𝑐)K = J𝑥K          = J𝑥K = J𝑥K · . . . · J𝑥K = J𝑥 · . . . · 𝑥K.

The proofs for the remaining rewrite rules are analogous. See App. A for the complete proofs.                                   □

6We tested several encodings, but surprisingly, this non-linear encoding worked best.
7 Note that we have Jexp(0, 0)KEIA = 00 = 1.
                                                                      Satisfiability Modulo Exponential Integer Arithmetic   •    7


4.2   Refinement
Our refinement (Lines 8 – 11 of Alg. 1) is based on the six kinds of lemmas named in Line 9: symmetry lemmas,
monotonicity lemmas, bounding lemmas, prime lemmas, induction lemmas, and interpolation lemmas. In the sequel,
we explain how we compute a set L of such lemmas. Then our refinement conjoins
                                                  {𝜓 ∈ L | A ̸ |= 𝜓 }
to 𝜑 in Line 11. As our lemmas allow us to eliminate any counterexample, this set is never empty, see Thm. 27.
To compute L, we consider all terms that are relevant for the formula 𝜑.
Definition 6 (Relevant Terms). A term exp(𝑠, 𝑡) is relevant if 𝜑 has a subterm of the form exp(±𝑠, ±𝑡).
Example 7 (Relevant Terms). For our leading example (3), the relevant terms are all terms of the form
exp(±𝑥, ±𝑦 2 ), exp(±𝑦, ±𝑦), or exp(±𝑥, ±exp(𝑦, 𝑦)).
   While the formula 𝜑 is changed in Line 11 of Alg. 1, we only conjoin new lemmas to 𝜑, and thus relevant terms
can never become irrelevant. Moreover, by construction our lemmas only contain exp-terms that were already
relevant before. Thus, the set of relevant terms is not changed by our CEGAR loop.
   As mentioned in Sect. 1, our approach may also compute lemmas with non-linear polynomial arithmetic.
However, our lemmas are linear if 𝑠 is an integer constant and 𝑡 is linear for all subterms exp(𝑠, 𝑡) of 𝜑.
4.2.1 Symmetry Lemmas. Symmetry lemmas encode the relation between terms of the form exp(±𝑠, ±𝑡). For
each relevant term exp(𝑠, 𝑡), the set L contains the following symmetry lemmas:
                                      divisible2 (𝑡) =⇒ exp(𝑠, 𝑡) = exp(−𝑠, 𝑡)                                           (sym1 )
                                     ¬divisible2 (𝑡) =⇒ exp(𝑠, 𝑡) = −exp(−𝑠, 𝑡)                                          (sym2 )
                                                            exp(𝑠, 𝑡) = exp(𝑠, −𝑡)                                       (sym3 )

Note that sym1 and sym2 are just implications, not equivalences, as, for example, 𝑐 |𝑑 | = (−𝑐) |𝑑 | does not imply
divisible2 (𝑑) if 𝑐 = 0.
Example 8 (Symmetry Lemmas). For our leading example (3), the following symmetry lemmas would be
considered, among others:
                sym1 :                   divisible2 (−𝑦) =⇒ exp(−𝑦, −𝑦) = exp(𝑦, −𝑦)                                             (4)
                sym2 :                 ¬divisible2 (−𝑦) =⇒ exp(−𝑦, −𝑦) = −exp(𝑦, −𝑦)                                             (5)
                sym3 :                                           exp(𝑥, exp(𝑦, 𝑦)) = exp(𝑥, −exp(𝑦, 𝑦))                          (6)
                sym3 :                                           exp(𝑦, 𝑦) = exp(𝑦, −𝑦)                                          (7)
Note that, e.g., (4) results from the term exp(−𝑦, −𝑦), which is relevant (see Def. 6) even though it does not occur
in 𝜑.
  To prove soundness of our refinement, we have to show that our lemmas are EIA-valid.
Lemma 9. Let 𝑠, 𝑡 be terms of sort Int. Then sym1 – sym3 are EIA-valid.

  Proof. Let A ∈ EIA again be arbitrary but fixed and let J. . .K denote J. . .KA . For sym1 , assume Jdivisible2 (𝑡)K =
true, i.e., assume that J𝑡K is even. Then it remains to show
                         Jexp(𝑠, 𝑡) = exp(−𝑠, 𝑡)K = true,     i.e.,   Jexp(𝑠, 𝑡)K = Jexp(−𝑠, 𝑡)K .
8   • F. Frohn, J. Giesl


We have:
                                         Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K |
                                                        = J−𝑠K | J𝑡 K |                                          (as J𝑡K, and thus also | J𝑡K |, is even)
                                                        = Jexp(−𝑠, 𝑡)K
The proofs for sym2 and sym3 are analogous, see App. A.                                                                                                □
4.2.2   Monotonicity Lemmas. Monotonicity lemmas are of the form
                       𝑠 2 ≥ 𝑠 1 > 1 ∧ 𝑡 2 ≥ 𝑡 1 > 0 ∧ (𝑠 2 > 𝑠 1 ∨ 𝑡 2 > 𝑡 1 ) =⇒ exp(𝑠 2, 𝑡 2 ) > exp(𝑠 1, 𝑡 1 ),                               (mon)
i.e., they prohibit violations of monotonicity of exp.
Example 10 (Monotonicity Lemmas). For our leading example (3), we obtain, e.g., the following lemmas:
                                     𝑥 > 1 ∧ exp(𝑦, 𝑦) > 𝑦 2 > 0 =⇒ exp(𝑥, exp(𝑦, 𝑦)) > exp(𝑥, 𝑦 2 )                                                  (8)
                                    𝑥 > 1 ∧ −exp(𝑦, 𝑦) > 𝑦 2 > 0 =⇒ exp(𝑥, −exp(𝑦, 𝑦)) > exp(𝑥, 𝑦 2 )                                                 (9)
  So for each pair of two different relevant terms exp(𝑠 1, 𝑡 1 ), exp(𝑠 2, 𝑡 2 ) where J𝑠 2 K ≥ J𝑠 1 K > 1 and J𝑡 2 K ≥ J𝑡 1 K > 0,
the set L contains mon. Here and in the sequel, unless mentioned otherwise, J. . .K means J. . .KA , where A is the
model from Line 6 of Alg. 1.
Lemma 11. Let 𝑠 1, 𝑠 2, 𝑡 1, 𝑡 2 be terms of sort Int. Then mon is EIA-valid.
    Proof. Let A ∈ EIA be arbitrary but fixed and let J. . .K denote J. . .KA . Assume
                                          J𝑠 2 ≥ 𝑠 1 > 1 ∧ 𝑡 2 ≥ 𝑡 1 > 0 ∧ (𝑠 2 > 𝑠 1 ∨ 𝑡 2 > 𝑡 1 )K = true,
i.e.,
                                    J𝑠 2 K ≥ J𝑠 1 K > 1, J𝑡 2 K ≥ J𝑡 1 K > 0, and (J𝑠 2 K > J𝑠 1 K or J𝑡 2 K > J𝑡 1 K).
Then it remains to prove
                             Jexp(𝑠 2, 𝑡 2 ) > exp(𝑠 1, 𝑡 1 )K = true,             i.e.,    Jexp(𝑠 2, 𝑡 2 )K > Jexp(𝑠 1, 𝑡 1 )K .
First note that 𝜆𝑥 . 𝑥 is strictly monotonically increasing on N>1 as J𝑡 1 K > 0, and 𝜆𝑦. J𝑠 1 K𝑦 is strictly monoton-
                           J𝑡 1 K

ically increasing on N>0 as J𝑠 1 K > 1. Since we have J𝑠 2 K ∈ N>1 and J𝑡 2 K ∈ N>0 , we get
                                              Jexp(𝑠 2, 𝑡 2 )K = J𝑠 2 K | J𝑡2 K | > J𝑠 1 K | J𝑡1 K | = Jexp(𝑠 1, 𝑡 1 )K
due to monotonicity, as we have J𝑠 2 K ≥ J𝑠 1 K and J𝑡 2 K ≥ J𝑡 1 K, where at least one of both inequations is strict.                                 □
4.2.3 Bounding Lemmas. Bounding lemmas provide bounds on relevant terms exp(𝑠, 𝑡) where J𝑠K and J𝑡K are
non-negative. Together with symmetry lemmas, they also give rise to bounds for the cases where 𝑠 or 𝑡 are
negative.
   For each relevant term exp(𝑠, 𝑡) where J𝑠K and J𝑡K are non-negative, the following lemmas are contained in L:
                                                                          𝑡 = 0 =⇒ exp(𝑠, 𝑡) = 1                                                 (bnd1 )
                                                                          𝑡 = 1 =⇒ exp(𝑠, 𝑡) = 𝑠                                                 (bnd2 )
                                                             𝑠 = 0 ∧ 𝑡 ≠ 0 ⇐⇒ exp(𝑠, 𝑡) = 0                                                      (bnd3 )
                                                                          𝑠 = 1 =⇒ exp(𝑠, 𝑡) = 1                                                 (bnd4 )
                                             𝑠 + 𝑡 > 4 ∧ 𝑠 > 1 ∧ 𝑡 > 1 =⇒ exp(𝑠, 𝑡) > 𝑠 · 𝑡 + 1                                                  (bnd5 )
                                                                          Satisfiability Modulo Exponential Integer Arithmetic   •   9


The cases 𝑡 ∈ {0, 1} are also addressed by our first rewrite rule (see Sect. 4.1). However, this rewrite rule only
applies if 𝑡 is an integer constant. In contrast, the first two lemmas above apply if 𝑡 evaluates to 0 or 1 in the
current model.

Example 12 (Bounding Lemmas). For our leading example (3), the following bounding lemmas would be
considered, among others:

                   bnd1 :                                   exp(𝑦, 𝑦) = 0 =⇒ exp(𝑥, exp(𝑦, 𝑦)) = 1
                   bnd2 :                                   exp(𝑦, 𝑦) = 1 =⇒ exp(𝑥, exp(𝑦, 𝑦)) = 𝑥
                   bnd3 :                           𝑥 = 0 ∧ exp(𝑦, 𝑦) ≠ 0 ⇐⇒ exp(𝑥, exp(𝑦, 𝑦)) = 0
                   bnd4 :                                              𝑥 = 1 =⇒ exp(𝑥, exp(𝑦, 𝑦)) = 1
                   bnd5 :                                              𝑦 > 2 =⇒ exp(𝑦, 𝑦) > 𝑦 2 + 1                              (10)
                   bnd5 :                                            −𝑦 > 2 =⇒ exp(−𝑦, −𝑦) > 𝑦 + 1      2
                                                                                                                                 (11)

Lemma 13. Let 𝑠, 𝑡 be terms of sort Int. Then bnd1 – bnd5 are EIA-valid.

  Proof. We only prove that bnd5 is EIA-valid and refer to App. A for the (simpler) proofs of bnd1 – bnd4 .
  Let A ∈ EIA again be arbitrary but fixed and let J. . .K denote J. . .KA . To show validity of bnd5 , assume

                   J𝑠 + 𝑡 > 4 ∧ 𝑠 > 1 ∧ 𝑡 > 1K = true,        i.e,     J𝑠 + 𝑡K > 4, J𝑠K > 1, and J𝑡K > 1.

Then it remains to show

                         Jexp(𝑠, 𝑡) > 𝑠 · 𝑡 + 1K = true,       i.e.,    Jexp(𝑠, 𝑡)K > J𝑠K · J𝑡K + 1.

We use induction on J𝑠K + J𝑡K. In the base case, we have either J𝑠K = 2 and J𝑡K = 3, or J𝑠K = 3 and J𝑡K = 2. In the
former case, we have:

                            Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = 2 |3| = 8 > 7 = 2 · 3 + 1 = J𝑠K · J𝑡K + 1

In the latter case, we have:

                            Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = 3 |2| = 9 > 7 = 3 · 2 + 1 = J𝑠K · J𝑡K + 1

For the induction step, assume J𝑠K + J𝑡K > 5. If J𝑡K > 2, then:

                       Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K |
                                     = J𝑠KJ𝑡 K
                                     = J𝑠KJ𝑡 K−1 · J𝑠K
                                     > (J𝑠K · (J𝑡K − 1) + 1) · J𝑠K                              (by the induction hypothesis)
                                     ≥ (J𝑠K · (J𝑡K − 1) + 1) · 2                                                       (as J𝑠K ≥ 2)
                                     = (J𝑠K · (J𝑡K − 1) + 1) + (J𝑠K · (J𝑡K − 1) + 1)
                                     ≥ (J𝑠K · (J𝑡K − 1) + 1) + (J𝑠K · 2 + 1)                                           (as J𝑡K > 2)
                                     > (J𝑠K · (J𝑡K − 1) + 1) + J𝑠K
                                     = J𝑠K · J𝑡K + 1
10 •    F. Frohn, J. Giesl


If J𝑡K = 2, then J𝑠K > 3. Now we have
                             Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K |
                                           = J𝑠K2
                                           = (J𝑠 − 1K + 1) 2
                                           = J𝑠 − 1K2 + 2 · J𝑠 − 1K + 1
                                           > J𝑠 − 1K · 2 + 1 + 2 · J𝑠 − 1K + 1                      (by the induction hypothesis)
                                           ≥ J𝑠 − 1K · 2 + 8                                     (as J𝑠K > 3 and thus, J𝑠 − 1K ≥ 3)
                                           = J𝑠K · 2 + 6
                                           = J𝑠K · J𝑡K + 6
                                           > J𝑠K · J𝑡K + 1
                                                                                                                                  □
   The reason why the bounding lemmas focus on lower bounds is that polynomials can only bound exp(𝑠, 𝑡)
from above for finitely many values of 𝑠 and 𝑡. The bounding lemmas are defined in such a way that they provide
lower bounds for exp(𝑠, 𝑡) for almost all non-negative values of 𝑠 and 𝑡: bnd1 –bnd4 provide tight bounds for all
cases where at least one argument of exp is 0 or 1, and bnd5 provides lower bounds for all other cases except for
exp(2, 2). To cover all cases, we could replace bnd5 by
                                                     𝑠 > 1 ∧ 𝑡 ≥ 0 =⇒ exp(𝑠, 𝑡) ≥ 𝑠 · 𝑡 .
However, in contrast to the alternative lemma above, bnd5 expresses that exp(𝑠, 𝑡) is strictly greater than 𝑠 · 𝑡.
The missing (lower and upper) bounds are provided by interpolation lemmas (see Sect. 4.2.6).
4.2.4   Prime Lemmas. Prime lemmas are of the form
                             divisible𝑑 (exp(𝑠, 𝑡)) ⇐⇒ divisible𝑑 (𝑠) ∧ 𝑡 ≠ 0               where 𝑑 is prime.              (prime)
So prime lemmas express that exp(𝑠, 𝑡) and 𝑠 have the same prime factors for 𝑡 ≠ 0.
Example 14 (Prime Lemmas). Consider the formula
                                                          𝑦 ≠ 0 ∧ exp(2, 𝑥) = exp(3, 𝑦),                                       (12)
which was used by Frohn and Giesl [24] (where prime lemmas were not yet integrated) to illustrate incompleteness
of our approach. Unsatisfiability of this formula can easily be proven with the prime lemmas
        divisible2 (exp(2, 𝑥)) ⇐⇒ divisible2 (2) ∧ 𝑥 ≠ 0 ≡ divisible2 (exp(2, 𝑥)) ⇐⇒ 𝑥 ≠ 0                             and
         divisible2 (exp(3, 𝑦)) ⇐⇒ divisible2 (3) ∧ 𝑦 ≠ 0 ≡ ¬divisible2 (exp(3, 𝑦)),
which rule out structures A with A |= 𝑥 ≠ 0. The reason is that 𝑥 ≠ 0 implies divisible2 (exp(2, 𝑥)) by the first
prime lemma, which, together with the second prime lemma, implies exp(2, 𝑥) ≠ exp(3, 𝑦). For the case 𝑥 = 0,
the following additional lemmas are needed:
                                                      𝑥 = 0 =⇒ exp(2, 𝑥) = 1                                                 (bnd1 )
                                                      𝑦 = 1 =⇒ exp(3, 𝑦) = 3                                                 (bnd2 )
                                                      𝑦 > 1 =⇒ exp(3, 𝑦) > 3 · 𝑦 + 1                                         (bnd5 )
                                                                   exp(3, 𝑦) = exp(3, −𝑦)                                    (sym3 )
                                                                                    Satisfiability Modulo Exponential Integer Arithmetic   • 11


Then we have exp(2, 𝑥) = 1 by the first bounding lemma and exp(3, 𝑦) > 1 for all 𝑦 > 0 by the second and third
bounding lemma. Together with the symmetry lemma, the latter also implies exp(3, 𝑦) > 1 for all 𝑦 < 0. As (12)
implies 𝑦 ≠ 0, this suffices to prove unsatisfiability.
  So for each relevant term exp(𝑠, 𝑡) where J𝑠K ≥ 2, Jexp(𝑠, 𝑡)K ≥ 2, and where the sets of prime factors of J𝑠K
and Jexp(𝑠, 𝑡)K differ, L contains prime, where 𝑑 is the smallest prime which divides J𝑠K or Jexp(𝑠, 𝑡)K, but not
both of them. To find 𝑑, we use wheel factorization [40].
Lemma 15. Let 𝑠, 𝑡 be terms of sort Int and let 𝑑 ∈ N be prime. Then prime is EIA-valid.
   Proof. Again, let A ∈ EIA be arbitrary but fixed and let J. . .K denote J. . .KA . We need to prove
                                        Jdivisible𝑑 (exp(𝑠, 𝑡))K = Jdivisible𝑑 (𝑠) ∧ 𝑡 ≠ 0K ,
i.e.,
                                 Jdivisible𝑑 (exp(𝑠, 𝑡))K            iff       Jdivisible𝑑 (𝑠)K and J𝑡K ≠ 0.
                                                          | J𝑡 K |         0
If J𝑡K = 0, then the claim holds since then J𝑠K              = J𝑠K = 1 is not divisible by the prime number 𝑑. Otherwise, if
J𝑡K ≠ 0, then we have to prove that J𝑠K and J𝑠K | J𝑡 K | have the same prime factors. If 𝑃 is the multiset of J𝑠K’s prime
                              Î | J𝑡 K | Î
                                           𝑃 = J𝑠K | J𝑡 K | , so the claim follows.
              Î
factors, i.e., 𝑃 = J𝑠K, then 𝑖=1                                                                                          □

4.2.5   Induction Lemmas. Induction lemmas are of the form
                    𝑠 1 = 𝑠 2 ∧ 𝑡 2 − 𝑑 = 𝑡 1 ≥ 0 =⇒ exp(𝑠 2, 𝑡 2 ) = exp(𝑠 1, 𝑡 1 ) · 𝑠 𝑑1             where 𝑑 ∈ N>0 .                    (ind)
So intuitively, ind results from exp(𝑠 2, 𝑡 2 ) by 𝑑 unrollings of the recursive definition
                                                      (
                                                        exp(𝑠, 𝑥 − 1) · 𝑠 if 𝑥 > 0
                                      exp(𝑠, 𝑥) =
                                                        1                 if 𝑥 = 0
as follows:
          exp(𝑠 2, 𝑡 2 ) = exp(𝑠 2, 𝑡 2 − 1) · 𝑠 2 = exp(𝑠 2, 𝑡 2 − 2) · 𝑠 22 = . . . = exp(𝑠 2, 𝑡 2 − 𝑑) · 𝑠 𝑑2 = exp(𝑠 1, 𝑡 1 ) · 𝑠 𝑑1

Example 16 (Induction Lemmas). We demonstrate the usefulness of induction lemmas by an example where
SMT solving is used to verify a solution for a recurrence relation. Consider the following recurrence relation
(where 𝑛 ranges over N>0 ):
                                            𝑓 (𝑛) = 2 · 𝑓 (𝑛 − 1) + 2𝑛                                     (13)
A possible solution (i.e., a function 𝑓 that satisfies (13)) is
                                                          𝑓 (𝑛) = (𝑓 (0) + 𝑛) · 2𝑛 .                                                        (14)
To verify that this function is indeed a solution, it suffices to replace 𝑓 with the definition from (14) and show
that the resulting equation holds for all 𝑛 ∈ N>0 and all 𝑓 (0) ∈ Z, i.e., to prove
                                 ∀𝑛 ∈ N>0, 𝑓0 ∈ Z. (𝑓0 + 𝑛) · 2𝑛 = 2 · (𝑓0 + 𝑛 − 1) · 2𝑛−1 + 2𝑛 .
To do so, it suffices to prove unsatisfiability of
                         𝑛 ≥ 1 ∧ (𝑓0 + 𝑛) · exp(2, 𝑛) ≠ 2 · (𝑓0 + 𝑛 − 1) · exp(2, 𝑛 − 1) + exp(2, 𝑛).                                       (15)
To this end, our implementation deduces the following induction lemma:
                                              𝑛 ≥ 1 =⇒ exp(2, 𝑛) = 2 · exp(2, 𝑛 − 1)
12 •    F. Frohn, J. Giesl


Then unsatisfiability can easily be proven without reasoning about exp: Assume 𝑛 ≥ 1. Then by the induction
lemma, we may substitute exp(2, 𝑛) with 2 · exp(2, 𝑛 − 1), resulting in
                             (𝑓0 + 𝑛) · 2 · exp(2, 𝑛 − 1) ≠ 2 · (𝑓0 + 𝑛 − 1) · exp(2, 𝑛 − 1) + 2 · exp(2, 𝑛 − 1)
                       ≡ (𝑓0 + 𝑛) · 2 · exp(2, 𝑛 − 1) ≠ 2 · (𝑓0 + 𝑛) · exp(2, 𝑛 − 1)
which is trivially unsatisfiable. Hence, (14) is a valid solution for (13).
  So for each pair of relevant terms exp(𝑠 1, 𝑡 1 ), exp(𝑠 2, 𝑡 2 ) where J𝑠 1 K = J𝑠 2 K and J𝑡 2 K − 𝑑 = J𝑡 1 K ≥ 0 for some
𝑑 ∈ N>0 , L contains ind.
Lemma 17. Let 𝑠 1, 𝑠 2, 𝑡 1, 𝑡 2 be terms of sort Int and let 𝑑 ∈ N>0 . Then ind is EIA-valid.
   Proof. Let A ∈ EIA be an arbitrary but fixed model of
                                                          𝑠1 = 𝑠2 ∧ 𝑡2 − 𝑑 = 𝑡1 ≥ 0
                                  A
and let J. . .K denote J. . .K . Then we have:
                                r                      z
                                  exp(𝑠 1, 𝑡 1 ) · 𝑠 𝑑1 = Jexp(𝑠 1, 𝑡 1 )K · J𝑠 1 K𝑑

                                                          = J𝑠 1 K | J𝑡1 K | · J𝑠 1 K𝑑
                                                          = J𝑠 1 K | J𝑡1 K+𝑑 |                              (as A |= 𝑡 1 ≥ 0 and 𝑑 ∈ N>0 )
                                                          = J𝑠 1 K | J𝑡2 K |                                         (as A |= 𝑡 2 − 𝑑 = 𝑡 1 )
                                                                     | J𝑡 2 K |
                                                          = J𝑠 2 K                                                       (as A |= 𝑠 1 = 𝑠 2 )
                                                          = Jexp(𝑠 2, 𝑡 2 )K
                                                                                                                                          □
4.2.6 Interpolation Lemmas. To provide bounds in cases where no bounding lemmas are violated, we use
interpolation lemmas that are constructed via bilinear interpolation. Here, we assume that the arguments of exp
are positive, as negative arguments are handled by symmetry lemmas, and bounding lemmas yield tight bounds
if at least one argument of exp is 0. The correctness of interpolation lemmas relies on the following observation.
As usual, [𝑤 1, 𝑤 2 ] and (𝑤 1, 𝑤 2 ) denote closed and open real intervals.
Lemma 18. Let 𝑐 ≥ 0, 𝑤 1, 𝑤 2 ∈ R>𝑐 ,8 𝑤 1 < 𝑤 2 , and let 𝑓 : R>𝑐 → R>0 be convex. Then
                                                              𝑓 (𝑤 2 ) − 𝑓 (𝑤 1 )
                             ∀𝑥 ∈ [𝑤 1, 𝑤 2 ]. 𝑓 (𝑥) ≤ 𝑓 (𝑤 1 ) +                 · (𝑥 − 𝑤 1 )                        and
                                                                  𝑤2 − 𝑤1
                                                              𝑓 (𝑤 2 ) − 𝑓 (𝑤 1 )
                   ∀𝑥 ∈ R>𝑐 \ (𝑤 1, 𝑤 2 ). 𝑓 (𝑥) ≥ 𝑓 (𝑤 1 ) +                     · (𝑥 − 𝑤 1 ).
                                                                  𝑤2 − 𝑤1
Note that the right-hand side of the inequations above is the linear interpolant of 𝑓 between 𝑤 1 and 𝑤 2 . Intuitively,
it corresponds to the secant of 𝑓 between the points (𝑤 1, 𝑓 (𝑤 1 )) and (𝑤 2, 𝑓 (𝑤 2 )), and thus the lemma follows
from convexity of 𝑓 .
   Proof of Lemma 18. For the first inequation, recall that a function 𝑓 : R>𝑐 → R>0 is convex if for all
𝑤 1, 𝑤 2 ∈ R>𝑐 and all 𝑣 ∈ [0, 1], we have
                                        𝑓 (𝑣 · 𝑤 2 + (1 − 𝑣) · 𝑤 1 ) ≤ 𝑣 · 𝑓 (𝑤 2 ) + (1 − 𝑣) · 𝑓 (𝑤 1 ).                               (16)
8 The lemma also holds for R
                                ≥𝑐 (and the proof is analogous).
                                                                                  Satisfiability Modulo Exponential Integer Arithmetic        • 13


Let 𝑥 ∈ [𝑤 1, 𝑤 2 ] and 𝑣 = 𝑤𝑥2−𝑤
                               −𝑤1 . Then we have 𝑣 ∈ [0, 1] and
                                 1



                             𝑓 (𝑥) = 𝑓 (𝑣 · 𝑤 2 + (1 − 𝑣) · 𝑤 1 )
                                    ≤ 𝑣 · 𝑓 (𝑤 2 ) + (1 − 𝑣) · 𝑓 (𝑤 1 )                                  (by convexity of 𝑓 and 𝑣 ∈ [0, 1])
                                                    𝑓 (𝑤 2 ) − 𝑓 (𝑤 1 )
                                    = 𝑓 (𝑤 1 ) +                        · (𝑥 − 𝑤 1 ),
                                                        𝑤2 − 𝑤1
as desired.
   For the second inequation, note that dually to (16), convex functions 𝑓 : R>𝑐 → R>0 satisfy
                                       𝑓 (𝑣 · 𝑤 2 + (1 − 𝑣) · 𝑤 1 ) ≥ 𝑣 · 𝑓 (𝑤 2 ) + (1 − 𝑣) · 𝑓 (𝑤 1 )
for all 𝑤 1, 𝑤 2 ∈ R>𝑐 and 𝑣 ∉ (0, 1) such that 𝑣 · 𝑤 2 + (1 − 𝑣) · 𝑤 1 ∈ R>𝑐 [39, 45]. Let 𝑥 ∈ R>𝑐 \ (𝑤 1, 𝑤 2 ) and
𝑣 = 𝑤𝑥2−𝑤
       −𝑤1 . Then we have 𝑣 ∉ (0, 1) and
         1



                              𝑓 (𝑥) = 𝑓 (𝑣 · 𝑤 2 + (1 − 𝑣) · 𝑤 1 )
                                    ≥ 𝑣 · 𝑓 (𝑤 2 ) + (1 − 𝑣) · 𝑓 (𝑤 1 )                                  (by convexity of 𝑓 and 𝑣 ∉ (0, 1))
                                                    𝑓 (𝑤 2 ) − 𝑓 (𝑤 1 )
                                     = 𝑓 (𝑤 1 ) +                       · (𝑥 − 𝑤 1 ),
                                                        𝑤2 − 𝑤1
as desired.                                                                                                                                      □

   Let exp(𝑠, 𝑡) be relevant, J𝑠K = 𝑐 > 0, J𝑡K = 𝑑 > 0, and JexpK(𝑐, 𝑑) ≠ 𝑐 𝑑 , i.e., we want to prohibit the current
interpretation of exp(𝑠, 𝑡).
  Interpolation Lemmas for Upper Bounds. First assume JexpK(𝑐, 𝑑) > 𝑐 𝑑 , i.e., to rule out this counterexample, we
need a lemma that provides a suitable upper bound for exp(𝑐, 𝑑). Let 𝑐 ′, 𝑑 ′ ∈ N>0 and:
           𝑐 − := min(𝑐, 𝑐 ′ )                𝑐 + := max(𝑐, 𝑐 ′ )                𝑑 − := min(𝑑, 𝑑 ′ )              𝑑 + := max(𝑑, 𝑑 ′ )
                                            [𝑐 ± ] := [𝑐 − .. 𝑐 + ]            [𝑑 ± ] := [𝑑 − .. 𝑑 + ]

Here, [𝑎 .. 𝑏] denotes a closed integer interval. Then we first use 𝑑 − , 𝑑 + for linear interpolation w.r.t. the 2𝑛𝑑
argument of 𝜆𝑥, 𝑦. 𝑥 𝑦 . To this end, let
                                                                +      −
                                           ±               −  𝑥𝑑 − 𝑥𝑑
                                      ip2[𝑑 ] (𝑥, 𝑦) := 𝑥 𝑑 +            · (𝑦 − 𝑑 − ),
                                                               𝑑+ − 𝑑 −
                                                                                        ±
where we define 𝑏𝑎 := 𝑏𝑎 if 𝑏 ≠ 0 and 𝑎0 := 0. So if 𝑑 − < 𝑑 + , then ip2[𝑑 ] (𝑥, 𝑦) corresponds to the linear interpolant
                                                          ±
of 𝑥 𝑦 w.r.t. 𝑦 between 𝑑 − and 𝑑 + . Then ip2[𝑑 ] (𝑥, 𝑦) is a suitable upper bound, as
                                                                                        ±
                                                 ∀𝑥 ∈ N>0, 𝑦 ∈ [𝑑 ± ]. 𝑥 𝑦 ≤ ip2[𝑑 ] (𝑥, 𝑦)                                                    (17)
follows from Lemma 18: If 𝑑 − = 𝑑 + , then (17) is trivial. Otherwise, let 𝑥 ∈ N>0 be arbitrary but fixed. Then (17)
follows by applying Lemma 18 to 𝑓 (𝑦) := 𝑥 𝑦 , which is clearly convex on R>0 .
   Hence, we could derive the following EIA-valid lemma:9
                                                                                              ±
                                            𝑠 > 0 ∧ 𝑡 ∈ [𝑑 ± ] =⇒ exp(𝑠, 𝑡) ≤ ip2[𝑑 ] (𝑠, 𝑡)                                                  (ip1 )
9 Strictly speaking, this lemma is not a Σexp -term if 𝑑 + > 𝑑 − , as the right-hand side makes use of (rational) division in this case. However, an
                                          Int
              exp
equivalent ΣInt -term can clearly be obtained by multiplying with the divisor.
14 •    F. Frohn, J. Giesl


Example 19 (Linear Interpolation w.r.t. 𝑦). Let Jexp(𝑠, 𝑡)K = JexpK(3, 9) > 39 , i.e., we have 𝑐 = 3 and 𝑑 = 9.
Moreover, assume 𝑐 ′ = 𝑑 ′ = 1, i.e., we get 𝑐 − = 1, 𝑐 + = 3, 𝑑 − = 1, and 𝑑 + = 9. Then
                                    ±                                             𝑥9 − 𝑥1                 𝑥9 − 𝑥
                         ip2[𝑑 ] (𝑥, 𝑦) = ip2[1..9] (𝑥, 𝑦) = 𝑥 1 +                        · (𝑦 − 1) = 𝑥 +        · (𝑦 − 1).
                                                                                   9−1                       8
Hence, ip1 corresponds to
                                                                                                          𝑠9 − 𝑠
                                                  𝑠 > 0 ∧ 𝑡 ∈ [1, 9] =⇒ exp(𝑠, 𝑡) ≤ 𝑠 +                          · (𝑡 − 1).
                                                                                                             8
This lemma would be violated by our counterexample, as we have
                  s                     {
                        𝑠9 − 𝑠                 39 − 3
                    𝑠+         · (𝑡 − 1) = 3 +        · 8 = 39 < JexpK(3, 9) = Jexp(𝑠, 𝑡)K .
                           8                      8
                                                  ±
  However, the degree of ip2[𝑑 ] (𝑠, 𝑡) depends on 𝑑 + , which in turn depends on the model that was found by the
                                                     ±
underlying SMT solver. Thus, the degree of ip2[𝑑 ] (𝑠, 𝑡) can get very large, which is challenging for the underlying
solver.
  So we next use 𝑐 − , 𝑐 + for linear interpolation w.r.t. the 1𝑠𝑡 argument of 𝜆𝑥, 𝑦. 𝑥 𝑦 , resulting in
                                        ±                       (𝑐 + ) 𝑦 − (𝑐 − ) 𝑦
                                   ip1[𝑐 ] (𝑥, 𝑦) := (𝑐 − ) 𝑦 +                     · (𝑥 − 𝑐 − ).
                                                                    𝑐+ − 𝑐 −
                                            ±
Then due to Lemma 18, ip1[𝑐 ] (𝑥, 𝑦) is also an upper bound on the exponentiation function, i.e., we have
                                                                                                      ±
                                                           ∀𝑦 ∈ N>0, 𝑥 ∈ [𝑐 ± ]. 𝑥 𝑦 ≤ ip1[𝑐 ] (𝑥, 𝑦).                                                 (18)

To see this, note that (18) is trivial if 𝑐 − = 𝑐 + . Otherwise, let 𝑦 ∈ N>0 be arbitrary but fixed. Then (18) follows by
applying Lemma 18 to 𝑓 (𝑥)      := 𝑥 𝑦 , which is clearly convex on R>0 .
                        𝑦−𝑑 −
  Note that we have 𝑑 + −𝑑 − ∈ [0, 1] for all 𝑦 ∈ [𝑑 ± ], and thus
                                                                𝑦 − 𝑑−            𝑦 − 𝑑−
                                                                        
                                     [𝑑 ± ]            𝑑−                      +
                                   ip2 (𝑥, 𝑦) = 𝑥 · 1 −                    + 𝑥𝑑 ·
                                                               𝑑+ − 𝑑 −           𝑑+ − 𝑑 −
                                                             −          +                                                  ±                       −
is monotonically increasing in both 𝑥 𝑑 and 𝑥 𝑑 . Hence, in the definition of ip2[𝑑 ] , we can approximate 𝑥 𝑑 and
   +                             ±                     ±
𝑥 𝑑 with their upper bounds ip1[𝑐 ] (𝑥, 𝑑 − ) and ip1[𝑐 ] (𝑥, 𝑑 + ) that can be derived from (18). Then (17) yields
                                                                                                  ±        ±
                                                         ∀𝑥 ∈ [𝑐 ± ], 𝑦 ∈ [𝑑 ± ]. 𝑥 𝑦 ≤ ip [𝑐 ] [𝑑 ] (𝑥, 𝑦)                                            (19)

where                                                                                 ±                            ±
                                                                 ±                ip1[𝑐 ] (𝑥, 𝑑 + ) − ip1[𝑐 ] (𝑥, 𝑑 − )
                                  [𝑐 ± ] [𝑑 ± ]
                             ip                   (𝑥, 𝑦) := ip1[𝑐 ] (𝑥, 𝑑 − ) +                                                · (𝑦 − 𝑑 − ).
                                                                                               𝑑+ − 𝑑 −
So the set L contains the lemma
                                                                                                               ±       ±
                                                   𝑠 ∈ [𝑐 ± ] ∧ 𝑡 ∈ [𝑑 ± ] =⇒ exp(𝑠, 𝑡) ≤ ip [𝑐 ] [𝑑 ] (𝑠, 𝑡),                                         (ip2 )
                                                                                                                                         ±     ±
which is valid due to (19), and rules out any counterexample with JexpK(𝑐, 𝑑) > 𝑐 𝑑 , as ip [𝑐 ] [𝑑 ] (𝑐, 𝑑) = 𝑐 𝑑 .

Lemma 20. Let 𝑐 + ≥ 𝑐 − > 0 and 𝑑 + ≥ 𝑑 − > 0. Then ip2 is EIA-valid.
                                                                           Satisfiability Modulo Exponential Integer Arithmetic   • 15


Example 21 (Bilinear Interpolation, Ex. 19 continued). In our example, we have:
                            ±                                    3𝑦 − 1𝑦                   3𝑦 − 1
                       ip1[𝑐 ] (𝑥, 𝑦) = ip1[1..3] (𝑥, 𝑦) = 1𝑦 +            · (𝑥 − 1) = 1 +          · (𝑥 − 1)
                                                                  3−1                         2
                        ±                                      3−1
                   ip1[𝑐 ] (𝑠, 𝑑 − ) = ip1[1..3] (𝑠, 1) = 1 +         · (𝑠 − 1) = 𝑠
                                                                 2
                        ±                                      3 −1
                                                                9
                   ip1[𝑐 ] (𝑠, 𝑑 + ) = ip1[1..3] (𝑠, 9) = 1 +          · (𝑠 − 1) = 1 + 9841 · (𝑠 − 1)
                                                                  2
Hence, we obtain the lemma
                                                                           1 + 9841 · (𝑠 − 1) − 𝑠
                    𝑠 ∈ [1, 3] ∧ 𝑡 ∈ [1, 9] =⇒ exp(𝑠, 𝑡) ≤ 𝑠 +                                    · (𝑡 − 1).
                                                                                     8
This lemma is violated by our counterexample, as we have
                      s                                             {
                             1 + 9841 · (𝑠 − 1) − 𝑠
                        𝑠+                                · (𝑡 − 1) = 39 < JexpK(3, 9) = Jexp(𝑠, 𝑡)K .
                                          8
                                                                ±   ±
    ip2 relates exp(𝑠, 𝑡) with the bilinear function ip [𝑐 ] [𝑑 ] (𝑠, 𝑡), i.e., this function is linear w.r.t. both 𝑠 and 𝑡, but
it multiplies 𝑠 and 𝑡. Thus, if 𝑠 is an integer constant and 𝑡 is linear, then the resulting lemma is linear, too.
    To compute interpolation lemmas, a second point (𝑐 ′, 𝑑 ′ ) is needed. In our implementation, we store all points
(𝑐, 𝑑) where interpolation has previously been applied and use the one which is closest to the current one. The
same heuristic is used by Cimatti et al. [12] to compute secant lemmas. For the 1𝑠𝑡 interpolation step, we choose
(𝑐 ′, 𝑑 ′ ) = (𝑐, 𝑑). In this case, ip2 simplifies to 𝑠 = 𝑐 ∧ 𝑡 = 𝑑 =⇒ exp(𝑠, 𝑡) ≤ 𝑐 𝑑 .
  Interpolation Lemmas for Lower Bounds. While bounding lemmas already yield lower bounds, the bounds
provided by bnd5 are not exact, in general. Hence, if JexpK(𝑐, 𝑑) < 𝑐 𝑑 , then we also use bilinear interpolation to
obtain a precise lower bound for exp(𝑐, 𝑑). Dually to (17) and (18), Lemma 18 implies:
                                               ∀𝑥, 𝑦 ∈ N>0 . 𝑥 𝑦 ≥ ip2[𝑑..𝑑+1] (𝑥, 𝑦)                                             (20)
                                                ∀𝑥, 𝑦 ∈ N>0 . 𝑥 𝑦 ≥ ip1[𝑐..𝑐+1] (𝑥, 𝑦)                                            (21)
To see this for (20), let 𝑥 ∈ N>0   be arbitrary but fixed. Then (20) follows by applying Lemma 18 to 𝑓 (𝑦) := 𝑥 𝑦 , which
is clearly convex on R>0 . While Lemma 18 implies the claim for 𝑦 ∈ R>0 \ (𝑑, 𝑑 +1), note that N>0 ⊆ R>0 \ (𝑑, 𝑑 +1),
since (𝑑, 𝑑 + 1) does not contain any integers. The proof of (21) works analogously by considering 𝑓 (𝑥) := 𝑥 𝑦 for
fixed 𝑦 ∈ N>0 .
   Additionally, we also obtain
                                ∀𝑥, 𝑦 ∈ N>0 . 𝑥 𝑦+1 − 𝑥 𝑦 ≥ ip1[𝑐..𝑐+1] (𝑥, 𝑦 + 1) − ip1[𝑐..𝑐+1] (𝑥, 𝑦)                           (22)
from Lemma 18. The reason is that for 𝑓 (𝑥) := 𝑥 𝑦+1 − 𝑥 𝑦 , the right-hand side of (22) is equal to the linear
interpolant of 𝑓 between 𝑐 and 𝑐 + 1. Moreover, 𝑓 is convex, as 𝑓 (𝑥) = 𝑥 𝑦 · (𝑥 − 1) where for any fixed 𝑦 ∈ N>0 ,
both 𝑥 𝑦 and 𝑥 − 1 are non-negative, monotonically increasing, and convex on R ≥1 . Thus, (22) follows by applying
Lemma 18 to 𝑓 (𝑥) := 𝑥 𝑦+1 − 𝑥 𝑦 , since N>0 ⊆ R ≥1 \ (𝑐, 𝑐 + 1).
    If 𝑦 ≥ 𝑑, then ip2[𝑑..𝑑+1] (𝑥, 𝑦) = 𝑥 𝑑 + (𝑥 𝑑+1 − 𝑥 𝑑 ) · (𝑦 − 𝑑) is monotonically increasing in the first occurrence of
𝑥 𝑑 , and in 𝑥 𝑑+1 − 𝑥 𝑑 . Thus, by approximating 𝑥 𝑑 and 𝑥 𝑑+1 − 𝑥 𝑑 with their lower bounds from (21) and (22), (20)
yields
                ∀𝑥 ∈ N>0, 𝑦 ≥ 𝑑. 𝑥 𝑦 ≥ ip1[𝑐..𝑐+1] (𝑥, 𝑑) + (ip1[𝑐..𝑐+1] (𝑥, 𝑑 + 1) − ip1[𝑐..𝑐+1] (𝑥, 𝑑)) · (𝑦 − 𝑑)
                                         = ip [𝑐..𝑐+1] [𝑑..𝑑+1] (𝑥, 𝑦).                                                           (23)
16 •   F. Frohn, J. Giesl


So dually to ip2 , the set L contains the lemma
                                          𝑠 ≥ 1 ∧ 𝑡 ≥ 𝑑 =⇒ exp(𝑠, 𝑡) ≥ ip [𝑐..𝑐+1] [𝑑..𝑑+1] (𝑠, 𝑡)                           (ip3 )
which is valid due to (23) and rules out any counterexample with JexpK(𝑐, 𝑑) < 𝑐 𝑑 , as ip [𝑐..𝑐+1] [𝑑..𝑑+1] (𝑐, 𝑑) = 𝑐 𝑑 .
Lemma 22. Let 𝑐, 𝑑 ∈ N>0 . Then ip3 is EIA-valid.
Example 23 (Interpolation, Lower Bounds). Let Jexp(𝑠, 𝑡)K = JexpK(3, 9) < 39 , i.e., we have 𝑐 = 3, and 𝑑 = 9.
Then
                                  ip1[3..4] (𝑥, 9) = 39 + (49 − 39 ) · (𝑥 − 3) = 19683 + 242461 · (𝑥 − 3)
                                 ip1[3..4] (𝑥, 10) = 310 + (410 − 310 ) · (𝑥 − 3) = 59049 + 989527 · (𝑥 − 3)
                            ip [3..4] [9..10] (𝑥, 𝑦) = ip1[3..4] (𝑥, 9) + (ip1[3..4] (𝑥, 10) − ip1[3..4] (𝑥, 9)) · (𝑦 − 9)
and thus we obtain the lemma
                  𝑠 ≥ 1 ∧ 𝑡 ≥ 9 =⇒ exp(𝑠, 𝑡) ≥ 747066 · 𝑠 · 𝑡 − 6481133 · 𝑠 − 2201832 · 𝑡 + 19108788.
It is violated by our counterexample, as we have
                            J747066 · 𝑠 · 𝑡 − 6481133 · 𝑠 − 2201832 · 𝑡 + 19108788K = 39 > JexpK(3, 9).

4.3    Lazy Lemma Generation
In practice, it is not necessary to compute the entire set of lemmas L. Instead, we can stop as soon as L contains
a single lemma which is violated by the current counterexample. However, such a strategy would result in a quite
fragile implementation, as its behavior would heavily depend on the order in which lemmas are computed, which
in turn depends on low-level details like the order of iteration over sets, etc. So instead, we use the following
precedence on our six kinds of lemmas:
                     symmetry ≻ monotonicity ≻ bounding ≻ prime ≈ induction ≈ interpolation
Then we compute all lemmas of the same kind, starting with symmetry lemmas, and we only proceed with
kinds of lower precedence if none of the lemmas computed so far is violated by the current counterexample. The
motivation for the order above is as follows: First, we prefer symmetry, monotonicity, and bounding lemmas, as
there are only finitely many of them for a finite set of relevant terms. In contrast, in principle there could be
infinitely many prime, induction, and interpolation lemmas, so they all get the same, lowest precedence. The
reason is that the natural numbers 𝑐, 𝑑, 𝑐 − , 𝑐 +, 𝑑 − , 𝑑 + that occur in these lemmas depend on the current NIA-model
A. Symmetry lemmas obtain the highest precedence, as other kinds of lemmas depend on them for restricting
exp(𝑠, 𝑡) in the case that 𝑠 or 𝑡 is negative. Moreover, we prefer monotonicity lemmas over bounding lemmas, as
monotonicity lemmas are linear (if the arguments of exp are linear), whereas bnd5 may be non-linear.
   The improved version of Alg. 1 is shown in Alg. 2. Note that the first inner loop in Line 9 breaks as soon as a
lemma that is violated by the current model A has been found, i.e., as soon as L is non-empty. Then due to the
check in Line 12, the second inner loop in Line 13 is only executed if the first inner loop failed to eliminate the
current counterexample. In contrast to the first inner loop, the second one in Line 13 does not break, as prime,
induction, and interpolation lemmas have the same precedence.
Example 24 (Leading Example Finished). We now finish our leading example which, after preprocessing, looks
as follows (see Ex. 4):
                                           𝑥 2 > 4 ∧ 𝑦 2 > 4 ∧ exp(𝑥, 𝑦 2 ) = exp(𝑥, exp(𝑦, 𝑦))                                (3)
                                                                        Satisfiability Modulo Exponential Integer Arithmetic   • 17


 Algorithm 2: CEGAR for EIA with Lazy Lemma Generation
              exp
   Input: a ΣInt -formula 𝜑
   // Preprocessing
 1 do
 2    𝜑′ ← 𝜑
 3    𝜑 ← FoldConstants(𝜑)
 4    𝜑 ← Rewrite(𝜑)
 5 while 𝜑 ≠ 𝜑
                ′

   // Refinement Loop
 6 while there is a NIA-model A of 𝜑
 7    if A is a counterexample then
 8        L←∅
 9        for k ∈ {Symmetry, Monotonicity, Bounding}
10             L ← {𝜓 ∈ ComputeLemmas(𝜑, k) | A ̸ |= 𝜓 }
11            if L ≠ ∅ then break
12        if L = ∅ then
13            for k ∈ {Prime, Induction, Interpolation}
14                 L ← L ∪ {𝜓 ∈ ComputeLemmas(𝜑, k) | A ̸ |= 𝜓 }
                     Ó
15        𝜑 ←𝜑∧ L
16    else return sat
17 return unsat




Then our implementation generates 12 symmetry lemmas, 4 monotonicity lemmas, and 17 bounding lemmas
before proving unsatisfiability, including
                                         (4), (5), (6), (7), (8), (9), (10), and (11).
These lemmas suffice to prove unsatisfiability for the case 𝑥 > 2 (the cases 𝑥 ∈ [−2 .. 2] or 𝑦 ∈ [−2 .. 2] are trivial).
For example, if 𝑦 < −2 and divisible2 (−𝑦), we get
                             (11)                            (4)
                     𝑦 < −2 ↷ exp(−𝑦, −𝑦) > 𝑦 2 + 1 ↷ exp(𝑦, −𝑦) > 𝑦 2 + 1
                              (7)                      (8)                                       (3)
                             ↷ exp(𝑦, 𝑦) > 𝑦 2 + 1 ↷ exp(𝑥, exp(𝑦, 𝑦)) > exp(𝑥, 𝑦 2 ) ↷ false
and for the cases 𝑦 > 2 and 𝑦 < −2 ∧ ¬divisible2 (−𝑦), unsatisfiability can be shown similarly. For the overall
proof, 5 more symmetry lemmas, 2 more monotonicity lemmas, and 4 more bounding lemmas are used. The
remaining lemmas that are deduced by our implementation are not used in the final proof of unsatisfiability.
  While our leading example can be solved without interpolation lemmas, in general, interpolation lemmas are a
crucial ingredient of our approach.
Example 25. Consider the formula
                                     1 < 𝑥 < 𝑦 ∧ 0 < 𝑧 ∧ exp(𝑥, 𝑧) < exp(𝑦, 𝑧).
Our implementation first rules out 7 counterexamples using 7 bounding lemmas, 15 prime lemmas, and 9
interpolation lemmas, before finding the model J𝑥K = 5, J𝑦K = 7, and J𝑧K = 3. Without interpolation lemmas, our
18 •   F. Frohn, J. Giesl


implementation keeps computing prime lemmas indefinitely, and without prime and interpolation lemmas, our
implementation returns unknown.10
  Our main soundness theorem follows from soundness of our preprocessings (Lemma 5) and the fact that all of
our lemmas are EIA-valid (Lemmas 9, 11, 13, 15, 17, 20, and 22).
Theorem 26 (Soundness of Alg. 2). If Alg. 2 returns sat, then 𝜑 is satisfiable in EIA. If Alg. 2 returns unsat, then 𝜑
is unsatisfiable in EIA.
   Another important property of Alg. 2 is that it can eliminate any counterexample, and hence it makes progress
in every iteration.
Theorem 27 (Progress Theorem). If A is a counterexample and L is computed as in Alg. 2, then
                                                      Û
                                               A ̸ |=   L.

  Proof. Let A ∈ EIA be arbitrary but fixed and let J. . .K denote J. . .KA . Since A is a counterexample, there is a
subexpression exp(𝑠, 𝑡) of 𝜑 such that Jexp(𝑠, 𝑡)K ≠ Jexp(𝑠, 𝑡)KEIA . We now show that A violates at least one of
our lemmas.
  First assume J𝑠K , J𝑡K ∈ N. Then
     • 𝑡 = 0 implies Jbnd1 K = false and
     • 𝑠 = 0 ∧ 𝑡 ≠ 0 implies Jbnd3 K = false.
Hence, assume J𝑠K , J𝑡K ∈ N>0 . Then
      • Jexp(𝑠, 𝑡)K > Jexp(𝑠, 𝑡)KEIA implies Jip2 K = false (as remarked after ip2 ), and
      • Jexp(𝑠, 𝑡)K < Jexp(𝑠, 𝑡)KEIA implies Jip3 K = false (as remarked after ip3 ).
Now assume J𝑠K < 0 and J𝑡K ≥ 0. Since exp(−𝑠, 𝑡) is relevant, the set L contains bounding and interpolation
lemmas for exp(−𝑠, 𝑡). Hence, if Jexp(−𝑠, 𝑡)K ≠ Jexp(−𝑠, 𝑡)KEIA , then one of these lemmas is violated by A, as
argued above. Thus, assume Jexp(−𝑠, 𝑡)K = Jexp(−𝑠, 𝑡)KEIA . Then
      • if J𝑡K is even, then Jsym1 K = false, and
      • if J𝑡K is odd, then Jsym2 K = false.
Next assume J𝑠K ≥ 0 and J𝑡K < 0. Since exp(𝑠, −𝑡) is relevant, the set L contains bounding and interpolation
lemmas for exp(𝑠, −𝑡). Hence, if Jexp(𝑠, −𝑡)K ≠ Jexp(𝑠, −𝑡)KEIA , then one of these lemmas is violated by A, as
argued above. Thus, assume Jexp(𝑠, −𝑡)K = Jexp(𝑠, −𝑡)KEIA . Then Jsym3 K = false.
   Finally, assume J𝑠 1 K < 0 and J𝑡 1 K < 0. Since exp(−𝑠, −𝑡) is relevant, the set L contains bounding and interpola-
tion lemmas for exp(−𝑠, −𝑡). Hence, if Jexp(−𝑠, −𝑡)K ≠ Jexp(−𝑠, −𝑡)KEIA , then one of these lemmas is violated by
A, as argued above. Thus, assume Jexp(−𝑠, −𝑡)K = Jexp(−𝑠, −𝑡)KEIA .
   We only consider the case that J𝑡K is even (the case that J𝑡K is odd works analogously). Assume Jsym1 K = true
and Jsym3 K = true. Then we get
                                Jexp(𝑠, 𝑡)KEIA = Jexp(−𝑠, 𝑡)KEIA                                                        (as 𝑡 is even)
                                                                    EIA
                                                 = Jexp(−𝑠, −𝑡)K                                        (by definition of JexpKEIA )
                                                 = Jexp(−𝑠, −𝑡)K
                                                 = Jexp(𝑠, −𝑡)K                                                                 (sym1 )
                                                 = Jexp(𝑠, 𝑡)K ,                                                                (sym3 )
10 Note that without interpolation lemmas, Alg. 2 may fail to eliminate a counterexample, as Thm. 27 does not hold without interpolation

lemmas. In such cases, our implementation returns unknown.
                                                                             Satisfiability Modulo Exponential Integer Arithmetic    • 19


which contradicts Jexp(𝑠, 𝑡)K ≠ Jexp(𝑠, 𝑡)KEIA . Thus, we have Jsym1 K = false or Jsym3 K = false.                                       □
  Despite Theorems 26 and 27, EIA is of course undecidable, and hence Alg. 2 is incomplete. For example, it does
not terminate for the input formula
                                       𝑥 ≥ 𝑦 ≥ 0 ∧ exp(2, 𝑥) ≠ exp(2, 𝑥 − 𝑦) · exp(2, 𝑦).                                             (24)
Here, to prove unsatisfiability,11 one would need a rewrite rule like
                                              exp(𝑥, 𝑦) · exp(𝑥, 𝑧) → exp(𝑥, 𝑦 + 𝑧),
but such a rule would be unsound in our setting, as the right-hand side would need to be exp(𝑥, |𝑦| + |𝑧|) instead.
However, to avoid introducing non-linear terms like |𝑦| and |𝑧|, we did not include such a rewrite rule. Thus,
Alg. 2 would refine the formula (24) infinitely often.
   Note that monotonicity, prime, and induction lemmas are important, even though they are not required to prove
Thm. 27. The reason is that all (usually infinitely many) counterexamples must be eliminated to prove unsat. For
instance, reconsider Ex. 24, where the monotonicity lemma (8) eliminates infinitely many counterexamples with
Jexp(𝑥, exp(𝑦, 𝑦))K ≤ Jexp(𝑥, 𝑦 2 )K. In contrast, Thm. 27 only guarantees that every single counterexample can
be eliminated. Consequently, our implementation does not terminate on our leading example if monotonicity
lemmas are disabled. Similarly, our implementation fails to solve Ex. 14 and Ex. 16 without prime and induction
lemmas, respectively.

5   Phasing
When investigating the behavior of our implementation for satisfiable examples where it failed to find a solution,
we frequently observed the following problem: Even though a “small” solution exists where the exponents
(i.e., the second arguments of the occurring exp-terms) have small absolute values, the underlying SMT solver
returned candidate models with exponents whose absolute values were quite large. Then interpolation lemmas
with huge coefficients were generated, as these coefficients grow exponentially w.r.t. the second argument of exp.
Afterwards, the underlying solver took too long when searching for a new candidate model.
    To counter this phenomenon, we developed phasing, a technique to prefer “small” over “large” solutions, see
Alg. 3. The idea of phasing is to alternate between a sat-phase and an unsat-phase. In the sat-phase, the goal is
to find small candidate models. To this end, we impose a bound on the absolute values of the exponents to block
large models (Line 9). If we fail to find a candidate model in the sat-phase, then we switch to the unsat-phase
(Line 25). In the unsat-phase, our goal is prove unsatisfiability, so we do not impose any bounds on the exponents
in Line 9. If we fail to prove unsatisfiability, we discard the found model (unless it can be lifted to an EIA-model)
in Line 12 and switch back to the sat-phase (Line 13), but with a higher bound (Line 14).
    Note that the bound grows exponentially w.r.t. the number of phase changes (Lines 9 and 14). Thus, if there are
no small models, then the size of the considered models grows rapidly, so that we can still find a solution quickly.

6   Related Work
The most closely related work applies incremental linearization to NIA, or to non-linear real arithmetic with
transcendental functions (NRAT). Like our approach, incremental linearization is an instance of the CEGAR
paradigm: An initial abstraction (where certain predefined functions are considered as uninterpreted functions)
is refined via linear lemmas that rule out the current counterexample.
   Our approach is inspired by, but differs significantly from the approach for linearization of NRAT by Cimatti et
al. [12]. There, non-linear polynomials are linearized as well, whereas we leave the handling of polynomials to the
11 Note that induction lemmas are not sufficient for proving unsatisfiability of (24), as the difference between the exponents in induction

lemmas is always a constant, whereas it is non-constant in (24).
20   • F. Frohn, J. Giesl


 Algorithm 3: CEGAR for EIA with Phasing
                exp
    Input: a ΣInt -formula 𝜑
    // Preprocessing
 1 do
 2     𝜑′ ← 𝜑
 3     𝜑 ← FoldConstants(𝜑)
 4     𝜑 ← Rewrite(𝜑)
 5 while 𝜑 ≠ 𝜑
                 ′

 6 phase ← sat
 7 𝑏 ←1
    // Refinement Loop
 8 while ⊤
 9     if phase = sat then 𝜉 ← 𝜑 ∧ {−2𝑏 ≤ 𝑡 ≤ 2𝑏 | exp(𝑠, 𝑡) is relevant} else 𝜉 ← 𝜑
10     if there is a NIA-model A of 𝜉 then
11         if A is a counterexample then
12             if phase = unsat then
13                  phase ← sat
14                  𝑏++
15             else
16                  for k ∈ {Symmetry, Monotonicity, Bounding, Prime}
17                      L ← {𝜓 ∈ ComputeLemmas(𝜑, k) | A ̸ |= 𝜓 }
18                      if L ≠ ∅ then break
19                  if L = ∅ then
20                      for k ∈ {Induction, Interpolation}
 21                         L ← L ∪ {𝜓 ∈ ComputeLemmas(𝜑, k) | A ̸ |= 𝜓 }
                              Ó
22                  𝜑 ←𝜑∧ L
23         else return sat
24     else if phase = unsat then return unsat
25     else phase ← unsat



backend solver. Moreover, Cimatti et al. use linear lemmas only, whereas we also use bilinear lemmas. Furthermore,
Cimatti et al. fix the base to Euler’s number 𝑒, whereas we consider a binary version of exponentiation.
   The only lemmas of Cimatti et al. [12] that easily carry over to our approach are monotonicity lemmas. While
Cimatti et al. also use symmetry lemmas, they express properties of the sine function, i.e., they are fundamentally
different from ours. Our bounding lemmas are related to the “lower bound” and “zero” lemmas of Cimatti
et al., but there, 𝜆𝑥 . 𝑒 𝑥 is trivially bounded by 0. Interpolation lemmas are related to the “tangent” and “secant
lemmas” of Cimatti et al. However, tangent lemmas make use of first derivatives, so they are not expressible with
                                                   𝜕 𝑦
integer arithmetic in our setting, as we have 𝜕𝑦     𝑥 = 𝑥 𝑦 · ln 𝑥. Secant lemmas are essentially obtained by linear
interpolation, so our interpolation lemmas can be seen as a generalization of secant lemmas to binary functions.
A preprocessing by rewriting, prime lemmas, or induction lemmas are not considered by Cimatti et al.
   Cimatti et al. [11] also applied incremental linearization to NIA. Here, they used similar lemmas as for NRAT
[12], so they differ again fundamentally from ours.
                                                                   Satisfiability Modulo Exponential Integer Arithmetic   • 21


   Further existing approaches for NRAT are based on interval propagation [15, 28]. As observed by Cimatti et al.
[12], interval propagation effectively computes a piecewise constant approximation, which is less expressive than
our bilinear approximations.
   In recent years, a novel approach for NRAT based on the topological degree test has been proposed [13, 35]. Its
strength is finding irrational solutions more often than other approaches for NRAT. Hence, this line of work is
orthogonal to ours.
   EIA could also be tackled by combining NRAT techniques with branch-and-bound, but the following example
shows that doing so is not promising.

Example 28. Consider the formula 𝑥 = exp(3, 𝑦) ∧ 𝑦 > 0. To handle it with existing solvers, we have to encode
it using the natural exponential function:
                                              𝑒 𝑧 = 3 ∧ 𝑥 = 𝑒 𝑦·𝑧 ∧ 𝑦 > 0                                                 (25)
Here 𝑥 and 𝑦 range over the integers and 𝑧 ranges over the reals. Any model of (25) satisfies 𝑧 = ln 3, where ln 3
is irrational. As finding such models is challenging, the leading tools MathSat [10] and CVC5 [3] fail for 𝑒 𝑧 = 3.

   MetiTarski [1] integrates decision procedures for real closed fields and approximations for transcendental
functions into the theorem prover Metis [31] to prove theorems about the reals. In a related line of work, iSAT3
[15] has been coupled with SPASS [46]. Clearly, these approaches differ fundamentally from ours.
   Recently, the complexity of decidable extensions of linear integer arithmetic with exponentiation has been
investigated [6, 9, 33]. Benedikt et al. [6] consider Semenov arithmetic, which extends LIA with a function 𝜆𝑥 .𝑐 |𝑥 |
for some fixed natural number 𝑐 > 1. Thus, it is equivalent to EIA with quantifiers, but without the functions “·”,
“div”, and “mod”, and where the first argument of all occurrences of exp must be the same constant. In contrast,
Chistikov et al. [9] consider only quantifier-free conjunctions of literals from Semenov arithmetic. Integrating
such decision procedures into our approach is an interesting direction for future work. The technique of Chistikov
et al. is more efficient than the one of Benedikt et al., but as it can only handle conjunctions of literals, it needs to
be implemented as a theory solver, i.e., within an SMT solver. In contrast, our approach can be implemented on
top of an SMT solver, which is easier, as it does not require detailed knowledge of the internals of the SMT solver.
Thus, the approach of Benedikt et al. seems to be a better fit for our framework.
   Karimov et al. [33] showed that decidability of the existential fragment of an extension of Semenov arithmetic
with a second function 𝜆𝑥 .𝑑 |𝑥 | (where 𝑐 and 𝑑 are multiplicatively independent) would lead to mathematical
breakthroughs. So as it stands, we cannot hope for a complete solver as soon as we go beyond Semenov arithmetic.
   An alternative way to solve SMT problems with exponentiation is to provide the recursive definition of exp as
universally quantified axioms. Then SMT solvers with support for quantifiers try to instantiate these axioms
suitably in order to derive a conflict. To find suitable instantiations, various heuristics have been proposed [37,
41, 42, 43, 44]. However, such approaches are only suitable for proving unsatisfiability, and for that purpose, our
evaluation shows that our approach outperforms quantifier instantiation techniques, see Sect. 7.3.

7   Implementation and Evaluation
We implemented our approach in our novel tool SwInE-Z3, which is based on Z3 4.14.1 [38]. For more information
on SwInE-Z3, including precompiled releases for all platforms, we refer to [25].
  We compare SwInE-Z3 with the default configuration of the original implementation of Frohn and Giesl [24],
called SwInE-Legacy in the sequel. In contrast to SwInE-Z3, SwInE-Legacy does not support prime lemmas,
induction lemmas, and phasing. While SwInE-Z3 directly uses the API of Z3, SwInE-Legacy is based on SMT-
Switch [36], a library that offers a unified interface for various SMT solvers. By default, SwInE-Legacy also uses
Z3. For more information on SwInE-Legacy, we refer to [25].
22    • F. Frohn, J. Giesl


7.1     Benchmarks
To evaluate our approach, we synthesized a large collection of EIA problems from verification benchmarks
for safety, termination, and complexity analysis. More precisely, we ran our verification tool LoAT [22] on the
benchmarks for linear Constrained Horn Clauses (CHCs) with linear integer arithmetic from the CHC Competitions
2022 and 2023 as well as on the benchmarks for Termination and Complexity of Integer Transition Systems from the
Termination Problems Database (TPDB), the benchmark set of the Termination and Complexity Competition [29],
and extracted all SMT problems with exponentiation that LoAT created while analyzing these benchmarks.
Afterwards, we removed duplicates.
  The resulting benchmark set consists of 4627 SMT problems (called LoAT Problems below), which are available
online [20]:
       • 669 problems that resulted from the benchmarks of the CHC Competition ’22 (called CHC Comp ’22
         Problems below)
       • 158 problems that resulted from the benchmarks of the CHC Competition ’23 (CHC Comp ’23 Problems)
       • 3146 problems that resulted from the complexity benchmarks of the TPDB (Complexity Problems)
       • 654 problems that resulted from the termination benchmarks of the TPDB (Termination Problems)
   Unfortunately, these sets do not contain challenging unsatisfiable benchmarks: As shown in the evaluation of
Frohn and Giesl [24], the unsatisfiable instances can mostly be solved without reasoning about exponentials at
all. More precisely, most of these benchmarks are not just unsatisfiable in EIA (where the interpretation of exp
is fixed), but they are also unsatisfiable in NIA, where exp is an uninterpreted function. To obtain challenging
unsatisfiable examples, we generated one more set of benchmarks by validating the results of the recurrence
solver PURRS [2]. More precisely, we considered all recurrence relations from PURRS’s test suite12 where both
the recurrence relation and its expected solution can be expressed with polynomials and exponentials. Consider
such a recurrence relation
                                                              𝑓 (𝑛) = 𝑡                                                 (26)
where 𝑓 is the inductively defined function, i.e., the term 𝑡 contains subterms of the form 𝑓 (𝑛 − 𝑐), 𝑐 ∈ N>0 . Let
𝑘 be the maximal natural number such that 𝑓 (𝑛 − 𝑘) is a subterm of 𝑡. As an example, consider the recurrence
relation (13) in Ex. 16 where 𝑡 is 2 · 𝑓 (𝑛 − 1) + 2𝑛 and thus, 𝑘 = 1. Moreover, let 𝑠 be the expected solution for
(26) given in the test suite. For such expected solutions, we always have 𝑛 ∈ V (𝑠) ⊆ V (𝑡), and for all subterms
𝑓 (𝑞) of 𝑠, we have 𝑞 ∈ {0, . . . , 𝑘 − 1}. Here, V (𝑠) and V (𝑡) denote the sets of variables occurring in 𝑠 and 𝑡,
respectively. For the solution (14) in Ex. 16, we have 𝑠 = (𝑓 (0) + 𝑛) · 2𝑛 , i.e., here the only 𝑓 -subterm of 𝑠 is 𝑓 (0).
To construct new benchmarks, we considered the following SMT problem:
                                  𝑛 ≥ 𝑘 ∧ 𝑠 exp ≠ 𝑡 exp [𝑓 (𝑛 − 𝑖)/𝑠 exp [𝑛/𝑛 − 𝑖] | 1 ≤ 𝑖 ≤ 𝑘]                         (27)
where 𝑠 exp and 𝑡 exp result from 𝑠 and 𝑡 by replacing all exponentials (i.e., all subterms of the form 𝑝 𝑞 where 𝑞 ∉ Z)
with exp(𝑝, 𝑞). Moreover, 𝑠 exp [𝑛/𝑛 − 𝑖] results from 𝑠 exp by replacing 𝑛 with 𝑛 − 𝑖 and 𝑡 exp [𝑓 (𝑛 − 𝑖)/𝑠 exp [𝑛/𝑛 − 𝑖] |
1 ≤ 𝑖 ≤ 𝑘] results from 𝑡 exp by replacing each subterm 𝑓 (𝑛 − 𝑖) with 𝑠 exp [𝑛/𝑛 − 𝑖], for all 1 ≤ 𝑖 ≤ 𝑘. In this way,
we obtained the formula (15) in Ex. 16. If (27) is unsatisfiable, then the given solution is correct. More precisely,
let 𝑥® = V (𝑠) \ {𝑛}. Then unsatisfiability of (27) implies that the equation (26) holds for all 𝑛 ∈ N, all 𝑥® ∈ Z∗ , and
all 𝑐 0, . . . , 𝑐𝑘 −1 ∈ Z when interpreting 𝑓 as
                                               (
                                                 𝑐𝑛                       if 𝑛 < 𝑘
                                          𝑛 ↦→
                                                 𝑠 [𝑓 (𝑖)/𝑐𝑖 | 0 ≤ 𝑖 < 𝑘] otherwise.

12 https://github.com/aprove-developers/LoAT-purrs/blob/master/tests/recurrences
                                                                 Satisfiability Modulo Exponential Integer Arithmetic   • 23


In this way, we obtained 37 hard unsatisfiable benchmarks (called PURRS Problems below), which are also
available online [20].

7.2    Evaluation on the LoAT Problems
We first report on our experiments on the LoAT Problems. To evaluate the impact of the different components
of our approach, we tested with configurations where we disabled rewriting, symmetry lemmas, monotonicity
lemmas, bounding lemmas, prime lemmas, induction lemmas, interpolation lemmas, or phasing. All experiments
were performed on the CLAIX-2023-HPC nodes of the RWTH University High Performance Computing Cluster13
with a memory limit of 10560 MiB (≈ 11GB) and a timeout of 10 s per example. We chose a small timeout, as
LoAT usually has to discharge many SMT problems to solve a single verification task. So in our setting, each
individual SMT problem should be solved quickly.
   The results can be seen in Figures 1, 3, 5 and 7. All but two of the 4627 benchmarks can be solved by SwInE-
Z3. Most configurations, including SwInE-Legacy, can solve all CHC Comp and Termination Problems. The
only exceptions are the configurations without bounding or interpolation lemmas, which clearly shows their
importance.
   The Complexity Problems (Fig. 5) are by far the hardest, and thus also the most interesting. Here, SwInE-Z3
clearly outperforms SwInE-Legacy (2 vs. 58 unsolved instances). Moreover, Fig. 5 shows that all components of our
approach except for monotonicity lemmas, prime lemmas, and induction lemmas are crucial for the performance
of SwInE-Z3 on this benchmark set. Thus, phasing is the main reason why SwInE-Z3 is superior to SwInE-Legacy
on the satisfiable instances from our benchmark suite.
   The fact that monotonicity lemmas are of little importance here is not surprising: Monotonicity lemmas were
already of little use when Z3 was used as backend solver in the evaluation of SwInE-Legacy of Frohn and Giesl
[24]. However, these lemmas significantly improved the performance of SwInE-Legacy with CVC5 [3] as backend
solver. Hence, the usefulness of monotonicity lemmas depends on the details of the underlying solver. Moreover,
recall that our leading example cannot be solved without monotonicity lemmas, see Ex. 24.
   It is also not surprising that induction lemmas do not contribute much to the performance of SwInE-Z3 on this
benchmark set, as their main purpose is proving unsatisfiability, see Sect. 7.3.
   However, it is slightly disappointing that prime lemmas are not needed for the LoAT problems. Nevertheless,
we believe that prime factorizations are of such fundamental relevance that prime lemmas are likely to be useful
for benchmarks from other sources in the future.
   The runtime of SwInE can be seen in Figures 2, 4, 6 and 8. Most instances can be solved in a fraction of a second,
as desired for our use case. On the CHC Comp ’23 and the Termination Problems, SwInE-Z3 and SwInE-Legacy
are equally efficient. On the CHC Comp ’22 and the Complexity Problems, SwInE-Z3 is slightly faster than
SwInE-Legacy. We refer to Frohn and Giesl [20] for more details on our evaluation.

7.3    Evaluation on the PURRS Problems
We continue with the evaluation on the PURRS Problems, where we used a wall clock timeout of 300s. All of them
are unsatisfiable (provided that the test cases from PURRS’s test suite are correct), and most of these problems
require inductive reasoning, so they are particularly suitable to illustrate the usefulness of induction lemmas.
Hence, we considered two configurations of SwInE-Z3: The default configuration (where all features are enabled),
and a configuration without induction lemmas.
  In contrast to those LoAT Problems that are unsatisfiable, the PURRS Problems require reasoning about exp for
proving unsatisfiability. An alternative approach to tackle such problems is to use standard SMT solvers, and to
add the (universally quantified) recursive definition of exp explicitly. Thus, we also considered Z3 4.14.1, where
13 https://help.itc.rwth-aachen.de/service/rhr4fjjutttf
   solver         configuration    sat    unsat   unknown
  SwInE-Z3                         296     373        0                         650
                     default
SwInE-Legacy                       296     373        0




                                                            solved instances
                  no rewriting     296     373        0
                                                                                600
                 no symmetry       296     373        0
                no monotonicity    296     373        0
 SwInE-Z3         no bounding      111     373      185                         550
                    no prime       296     373        0                                                                SwInE-Z3
                  no induction     296     373        0                                                              SwInE-Legacy
                no interpolation   252     373       44                         500
                                                                                       0      20        40      60       80   100
                   no phasing      296     373        0                                            runtime in 1/10 seconds


               Fig. 1. CHC Comp ’22, Results                                           Fig. 2. CHC Comp ’22, Runtime

   solver         configuration    sat    unsat   unknown                       160

  SwInE-Z3                         87      71         0
                     default
SwInE-Legacy                       87      71         0



                                                            solved instances
                                                                                140
                  no rewriting     87      71         0
                 no symmetry       87      71         0
                no monotonicity    87      71         0
                                                                                120
 SwInE-Z3         no bounding      79      71         8
                    no prime       87      71         0                                                                SwInE-Z3
                  no induction     87      71         0                                                              SwInE-Legacy
                no interpolation   38      71        49                         100
                                                                                       0      20        40      60       80   100
                   no phasing      87      71         0                                            runtime in 1/10 seconds


               Fig. 3. CHC Comp ’23, Results                                           Fig. 4. CHC Comp ’23, Runtime

                                                                               3,200
   solver        configuration      sat   unsat   unknown
  SwInE-Z3                         1355    1789       2                        3,000
                    default
SwInE-Legacy                       1299    1789      58
                                                            solved instances




                                                                               2,800
                  no rewriting     1195    1789     162
                 no symmetry       951     1789     406                        2,600
                no monotonicity    1355    1789       2
                                                                               2,400
 SwInE-Z3         no bounding      890     1789     467
                    no prime       1355    1789       2                        2,200                                   SwInE-Z3
                  no induction     1355    1789       2                                                              SwInE-Legacy
                no interpolation   1241    1788     117                        2,000
                                                                                       0      20        40      60       80   100
                   no phasing      1271    1789      86                                            runtime in 1/10 seconds


                Fig. 5. Complexity, Results                                                Fig. 6. Complexity, Runtime

   solver         configuration    sat    unsat   unknown
                                                                                650
  SwInE-Z3                         223     431       0
                     default
SwInE-Legacy                       223     431       0
                                                            solved instances




                  no rewriting     223     431       0                          600
                 no symmetry       223     431       0
                no monotonicity    223     431       0
                                                                                550
 SwInE-Z3         no bounding      190     429       35
                    no prime       223     431       0                                                                 SwInE-Z3
                  no induction     223     431       0                                                               SwInE-Legacy
                no interpolation   155     429       70                         500
                                                                                       0      20        40      60       80   100
                   no phasing      223     431       0                                             runtime in 1/10 seconds


                Fig. 7. Termination, Results                                               Fig. 8. Termination, Runtime
                                                                 Satisfiability Modulo Exponential Integer Arithmetic   • 25


we added the following assertions to each benchmark:
                                  ∀𝑥 ∈ Z. exp(𝑥, 0) = 1
                                ∀𝑥, 𝑦 ∈ Z. 𝑦 > 0 =⇒ exp(𝑥, 𝑦) = 𝑥 · exp(𝑥, 𝑦 − 1)
                                ∀𝑥, 𝑦 ∈ Z. 𝑦 < 0 =⇒ exp(𝑥, 𝑦) = 𝑥 · exp(𝑥, 𝑦 + 1)
Note that SMT solvers use quantifier instantiation to derive contradictions, but adding such quantified assertions
prevents them from proving satisfiability. Hence, we did not include Z3 in the evaluation on the LoAT problems
in Sect. 7.2.
   The results can be seen in Table 1. With induction lemmas, SwInE-Z3 solves all instances that Z3 can solve
as well as 6 additional instances, and it only fails for 3 instances. Regarding the benchmarks that are solved by
both tools, SwInE-Z3 is substantially faster in some cases (purrs07, purrs36), but sometimes it is the other way
around (purrs35), so there is no clear picture. Without induction lemmas, SwInE-Z3 is clearly not suitable for
this benchmark set.

8   Conclusion
We presented the novel SMT theory EIA, which extends the theory non-linear integer arithmetic with integer
exponentiation. Moreover, inspired by incremental linearization for similar extensions of non-linear real arithmetic,
we developed a CEGAR approach to solve EIA problems. The core idea of our approach is to regard exponentiation
as an uninterpreted function and to eliminate counterexamples, i.e., models that violate the semantics of exponen-
tiation, by generating suitable lemmas. Here, the use of bilinear interpolation turned out to be crucial for proving
satisfiability, both in practice (see our evaluation in Sect. 7) and in theory, as interpolation lemmas are essential
for being able to eliminate any counterexample (see Thm. 27). Finally, we evaluated the implementation of our
approach in our novel tool SwInE-Z3 on thousands of EIA problems that were synthesized from verification tasks
using our verification tool LoAT, and on challenging unsatisfiable benchmarks that result from the verification of
solutions for recurrence relations. Our evaluation shows that SwInE-Z3 is highly effective for both use cases.
In particular, it shows that induction lemmas are crucial for proving unsatisfiability, and that our new phasing
technique allows our novel implementation SwInE-Z3 to outperform its predecessor on satisfiable instances.
   Consequently, we integrated SwInE-Z3 into our verification tool LoAT, where it now serves as the default
solver for all techniques that require reasoning about exponentials [19, 21].
   With SwInE-Z3, we provide an SMT-LIB compliant open-source solver for EIA [25]. In this way, we hope to
attract users with applications that give rise to challenging benchmarks, and we hope that other solvers with
support for integer exponentiation will follow, with the ultimate goal of standardizing EIA.

Acknowledgments
This work has been funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) -
235950644 (Project GI 274/6-2).
     tool        SwInE-Z3        Z3        SwInE-Z3
configuration     default      default    no induction
   purrs01       ✓ 0.45      ✓     0.66          –
   purrs02       ✓ 0.40      ✓     0.66          –
   purrs03            –           –            –
   purrs04       ✓ 0.44      ✓     0.65          –
   purrs05       ✓ 0.43      ✓     0.44          –
   purrs06       ✓ 0.45      ✓     0.45          –
   purrs07       ✓ 0.60      ✓ 31.64      ✗      26.7
   purrs08       ✓ 0.58      ✓     0.46   ✓      0.49
   purrs09       ✓ 0.52      ✗ 104.58            –
   purrs10       ✓ 0.50      ✗ 108.85            –
   purrs11       ✓ 0.48      ✓     0.49          –
   purrs12       ✓ 3.12      ✓     2.17          –
   purrs13       ✓ 0.49      ✓     0.61          –
   purrs14       ✓ 0.52      ✓     0.52   ✓      0.42
   purrs15       ✓ 0.43            –            –
   purrs16       ✓ 1.35            –            –
   purrs17       ✓ 1.42            –            –
   purrs18       ✓ 0.54      ✓     0.48          –
   purrs19       ✓ 0.52      ✓     0.48          –
   purrs20       ✓ 0.53      ✓     0.49          –
   purrs21       ✓ 0.41      ✓     0.43          –
   purrs22       ✓ 0.43      ✓     0.46          –
   purrs23       ✓ 0.47      ✓     0.44          –
   purrs24       ✓ 0.46      ✓     0.45          –
   purrs25       ✓ 0.43      ✓     0.44          –
   purrs26       ✓ 0.43      ✓     0.42          –
   purrs27       ✓ 0.40      ✓     0.46          –
   purrs28       ✓ 0.44      ✓     0.51          –
   purrs29       ✓ 0.44      ✓     0.53   ✗    239.34
   purrs30       ✓ 2.21            –            –
   purrs31       ✗ 18.93           –     ✗     87.65
   purrs32       ✗ 77.34           –            –
   purrs33       ✓ 0.43      ✓     0.46          –
   purrs34       ✓ 0.50      ✓     0.51   ✓      0.38
   purrs35       ✓ 21.39     ✓     6.12          –
   purrs36       ✓ 4.65      ✓ 38.30             –
   purrs37       ✓ 1.36      ✓     1.11          –
    solved          34           28             3
         ✓: unsat, ✗: unknown, : timeout
                Table 1. PURRS Problems
                                                                                  Satisfiability Modulo Exponential Integer Arithmetic        • 27


References
 [1]   B. Akbarpour and L. C. Paulson. 2010. MetiTarski: an automatic theorem prover for real-valued special functions. J. Autom. Reason., 44,
       3, 175–205. doi: 10.1007/S10817-009-9149-2.
 [2]   R. Bagnara, A. Pescetti, A. Zaccagnini, and E. Zaffanella. 2005. PURRS: towards computer algebra support for fully automatic worst-case
       complexity analysis. CoRR, abs/cs/0512056. doi: 10.48550/arXiv.cs/0512056.
 [3]   H. Barbosa et al. 2022. CVC5: A versatile and industrial-strength SMT solver. In TACAS ’22, LNCS 13243 (LNCS 13243), 415–442. doi:
       10.1007/978-3-030-99524-9_24.
 [4]   S. Bardin, A. Finkel, J. Leroux, and L. Petrucci. 2008. FAST: Acceleration from theory to practice. Int. J. Softw. Tools Technol. Transf., 10,
       5, 401–424. doi: 10.1007/s10009-008-0064-3.
 [5]   C. Barrett, P. Fontaine, and C. Tinelli. 2016. The Satisfiability Modulo Theories Library (SMT-LIB). https://www.SMT- LIB.org.
       www.SMT-LIB.org. (2016).
 [6]   M. Benedikt, D. Chistikov, and A. Mansutti. 2023. The complexity of Presburger arithmetic with power or powers. In ICALP ’23, LIPIcs
       261 (LIPIcs 261), 112:1–112:18. doi: 10.4230/LIPIcs.ICALP.2023.112.
 [7]   M. Bozga, R. Iosif, and F. Konečný. 2010. Fast acceleration of ultimately periodic relations. In CAV ’10, LNCS 6174, 227–242. doi:
       10.1007/978-3-642-14295-6_23.
 [8]   M. Bozga, R. Iosif, and F. Konečný. 2012. Relational Analysis of Integer Programs. Tech. rep. TR-2012-10. VERIMAG. https://www-veri
       mag.imag.fr/TR/TR-2012-10.pdf.
 [9]   D. Chistikov, A. Mansutti, and M. R. Starchak. 2024. Integer linear-exponential programming in NP by quantifier elimination. In
       ICALP ’24, LIPIcs 297 (LIPIcs 297), 132:1–132:20. doi: 10.4230/LIPICS.ICALP.2024.132.
[10]   A. Cimatti, A. Griggio, B. J. Schaafsma, and R. Sebastiani. 2013. The MathSAT5 SMT solver. In TACAS ’13, LNCS 7795 (LNCS 7795),
       93–107. doi: 10.1007/978-3-642-36742-7_7.
[11]   A. Cimatti, A. Griggio, A. Irfan, M. Roveri, and R. Sebastiani. 2018. Experimenting on solving nonlinear integer arithmetic with
       incremental linearization. In SAT ’18, LNCS 10929 (LNCS 10929), 383–398. doi: 10.1007/978-3-319-94144-8_23.
[12]   A. Cimatti, A. Griggio, A. Irfan, M. Roveri, and R. Sebastiani. 2018. Incremental linearization for satisfiability and verification modulo
       nonlinear arithmetic and transcendental functions. ACM Trans. Comput. Log., 19, 3, 19:1–19:52. doi: 10.1145/3230639.
[13]   A. Cimatti, A. Griggio, E. Lipparini, and R. Sebastiani. 2022. Handling polynomial and transcendental functions in SMT via unconstrained
       optimisation and topological degree test. In ATVA ’22, LNCS 13505 (LNCS 13505), 137–153. doi: 10.1007/978-3-031-19992-9_9.
[14]   E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. 2000. Counterexample-guided abstraction refinement. In CAV ’00, LNCS 1855
       (LNCS 1855). Springer, 154–169. doi: 10.1007/10722167_15.
[15]   M. Fränzle, C. Herde, T. Teige, S. Ratschan, and T. Schubert. 2007. Efficient solving of large non-linear arithmetic constraint systems
       with complex Boolean structure. J. Satisf. Boolean Model. Comput., 1, 3-4, 209–236. doi: 10.3233/sat190012.
[16]   F. Frohn and J. Giesl. 2019. Proving non-termination via loop acceleration. In FMCAD ’19, 221–230. doi: 10.23919/FMCAD.2019.8894271.
[17]   F. Frohn and J. Giesl. 2019. Termination of triangular integer loops is decidable. In CAV ’19, LNCS 11562, 426–444. doi: 10.1007/978-3-0
       30-25543-5_24.
[18]   F. Frohn, M. Naaf, M. Brockschmidt, and J. Giesl. 2020. Inferring lower runtime bounds for integer programs. ACM Trans. Program.
       Lang. Syst., 42, 3, 13:1–13:50. doi: 10.1145/3410331.
[19]   F. Frohn and J. Giesl. 2023. ADCL: Acceleration Driven Clause Learning for constrained Horn clauses. In SAS ’23, LNCS 14284, 259–285.
       doi: 10.1007/978-3-031-44245-2_13.
[20]   F. Frohn and J. Giesl. 2025. Evaluation of “Satisfiability modulo exponential integer arithmetic”. https://aprove-developers.github.io/s
       wine-journal-eval.
[21]   F. Frohn and J. Giesl. 2024. Integrating loop acceleration into bounded model checking. In FM ’24, LNCS 14933 (LNCS 14933), 73–91.
       doi: 10.1007/978-3-031-71162-6_4.
[22]   F. Frohn and J. Giesl. 2022. Proving non-termination and lower runtime bounds with LoAT. In IJCAR ’22, LNCS 13385, 712–722. doi:
       10.1007/978-3-031-10769-6_41.
[23]   F. Frohn and J. Giesl. 2023. Proving non-termination by Acceleration Driven Clause Learning. In CADE ’23, LNCS 14132, 220–233. doi:
       10.1007/978-3-031-38499-8_13.
[24]   F. Frohn and J. Giesl. 2024. Satisfiability modulo exponential integer arithmetic. In IJCAR ’24, LNCS 14739 (LNCS 14739), 344–365. doi:
       10.1007/978-3-031-63498-7_21.
[25]   F. Frohn and J. Giesl. 2025. SwInE. https://ffrohn.github.io/swine.
[26]   F. Frohn and J. Giesl. 2025. SwInE on GitHub. https://github.com/ffrohn/swine.
[27]   F. Frohn and J. Giesl. 2025. SwInE-Z3 on GitHub. https://github.com/ffrohn/swine-z3.
[28]   S. Gao, J. Avigad, and E. M. Clarke. 2012. 𝛿-complete decision procedures for satisfiability over the reals. In IJCAR ’12, LNCS 7364
       (LNCS 7364), 286–300. doi: 10.1007/978-3-642-31365-3_23.
28     • F. Frohn, J. Giesl


[29]     J. Giesl, A. Rubio, C. Sternagel, J. Waldmann, and A. Yamada. 2019. The termination and complexity competition. In TACAS ’19, LNCS
         11429, 156–166. doi: 10.1007/978-3-030-17502-3_10.
[30]     M. Hark, F. Frohn, and J. Giesl. 2025. Termination of triangular polynomial loops. Form. Methods Syst. Des., 65, 1, 70–132. doi:
         10.1007/s10703-023-00440-z.
[31]     J. Hurd. 2003. First-order proof tactics in higher-order logic theorem provers. In STRATA ’03, Report NASA/CP-2003-212448 (Report
         NASA/CP-2003-212448), 56–68. https://apps.dtic.mil/sti/pdfs/ADA418902.pdf.
[32]     B. Jeannet, P. Schrammel, and S. Sankaranarayanan. 2014. Abstract acceleration of general linear loops. In POPL ’14, 529–540. doi:
         10.1145/2535838.2535843.
[33]     T. Karimov, F. Luca, J. Nieuwveld, J. Ouaknine, and J. Worrell. 2025. On the decidability of Presburger arithmetic expanded with
         powers. In SODA ’25, 2755–2778. doi: 10.1137/1.9781611978322.89.
[34]     D. Kroening, M. Lewis, and G. Weissenbacher. 2015. Under-approximating loops in C programs for fast counterexample detection.
         Formal Methods Syst. Des., 47, 1, 75–92. doi: 10.1007/s10703-015-0228-1.
[35]     E. Lipparini and S. Ratschan. 2023. Satisfiability of non-linear transcendental arithmetic as a certificate search problem. In NFM ’23,
         LNCS 13903 (LNCS 13903), 472–488. doi: 10.1007/978-3-031-33170-1_29.
[36]     M. Mann et al. 2021. SMT-Switch: A solver-agnostic C++ API for SMT solving. In SAT ’21, LNCS 12831 (LNCS 12831), 377–386. doi:
         10.1007/978-3-030-80223-3_26.
[37]     L. de Moura and N. Bjørner. 2007. Efficient E-matching for SMT solvers. In CADE ’07, LNCS 4603, 183–198. doi: 10.1007/978-3-540-735
         95-3_13.
[38]     L. de Moura and N. Bjørner. 2008. Z3: an efficient SMT solver. In TACAS ’08, LNCS 4963, 337–340. doi: 10.1007/978-3-540-78800-3_24.
[39]     P. Popescu, Díaz-Barrero, and J. Luis. 2006. Certain inequalities for convex functions. JIPAM, 7, 2. http://eudml.org/doc/128518.
[40]     P. Pritchard. 1981. A sublinear additive sieve for finding prime numbers. Commun. ACM, 24, 1, 18–23. doi: 10.1145/358527.358540.
[41]     A. Reynolds, C. Tinelli, A. Goel, S. Krstic, M. Deters, and C. W. Barrett. 2013. Quantifier instantiation techniques for finite model
         finding in SMT. In CADE ’24, LNCS 7898, 377–391. doi: 10.1007/978-3-642-38574-2_26.
[42]     A. Reynolds, C. Tinelli, and L. de Moura. 2014. Finding conflicting instances of quantified formulas in SMT. In FMCAD ’14, 195–202.
         doi: 10.1109/FMCAD.2014.6987613.
[43]     A. Reynolds, M. Deters, V. Kuncak, C. Tinelli, and C. W. Barrett. 2015. Counterexample-guided quantifier instantiation for synthesis in
         SMT. In CAV ’15, LNCS 9207, 198–216. doi: 10.1007/978-3-319-21668-3_12.
[44]     A. Reynolds, H. Barbosa, and P. Fontaine. 2018. Revisiting enumerative instantiation. In TACAS ’18, LNCS 10806, 112–131. doi:
         10.1007/978-3-319-89963-3_7.
[45]     P. M. Vasić and J. E. Pečarić. 1979. On the Jensen inequality. Publikacije Elektrotehničkog fakulteta. Serija Matematika i fizika, 634/677,
         50–54. https://www.jstor.org/stable/43668091.
[46]     C. Weidenbach, D. Dimova, A. Fietzke, R. Kumar, M. Suda, and P. Wischnewski. 2009. SPASS version 3.5. In CADE ’22, LNCS 5663
         (LNCS 5663), 140–145. doi: 10.1007/978-3-642-02959-2_10.

A Missing Proofs
A.1 Proof of Lemma 5
Lemma 5. We have 𝜑 ≡EIA FoldConstants(𝜑) and 𝜑 ≡EIA Rewrite(𝜑).
  Proof. In Sect. 4, we already showed the soundness of the first rewrite rule. For the second rewrite rule
exp(exp(𝑥, 𝑦), 𝑧) → exp(𝑥, 𝑦 · 𝑧), we have
                                                                          | J𝑧 K |
                Jexp(exp(𝑥, 𝑦), 𝑧)K = Jexp(𝑥, 𝑦)K | J𝑧 K | = J𝑥K | J𝑦 K |            = J𝑥K | J𝑦 K | · | J𝑧 K |
                                                 =       J𝑥K | J𝑦 K·J𝑧 K |   =       J𝑥K | J𝑦·𝑧 K |       =      Jexp(𝑥, 𝑦 · 𝑧)K .
     For the third rewrite rule exp(𝑥, 𝑦) · exp(𝑧, 𝑦) → exp(𝑥 · 𝑧, 𝑦), we have
            Jexp(𝑥, 𝑦) · exp(𝑧, 𝑦)K        = Jexp(𝑥, 𝑦)K · Jexp(𝑧, 𝑦)K =                J𝑥K | J𝑦 K | · J𝑧K | J𝑦 K |   =   (J𝑥K · J𝑧K) | J𝑦 K |
                                           =       J𝑥 · 𝑧K | J𝑦 K |    =                 Jexp(𝑥 · 𝑧, 𝑦)K .
                                                                                                                                                 □

A.2       Proof of Lemma 9
Lemma 9. Let 𝑠, 𝑡 be terms of sort Int. Then sym1 – sym3 are EIA-valid.
                                                                               Satisfiability Modulo Exponential Integer Arithmetic   • 29


  Proof. We already showed the soundness of sym1 in Sect. 4. For sym2 , assume Jdivisible2 (𝑡)K = false, i.e.,
assume that J𝑡K is odd. Then it remains to show
                         Jexp(𝑠, 𝑡) = −exp(−𝑠, 𝑡)K = true,           i.e.,      Jexp(𝑠, 𝑡)K = J−exp(−𝑠, 𝑡)K .
We have:
                               Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K |
                                             = − J−𝑠K | J𝑡 K |                                   (as J𝑡K, and thus also | J𝑡K |, is odd)
                                             = − Jexp(−𝑠, 𝑡)K
                                             = J−exp(−𝑠, 𝑡)K


   For sym3 , we have to show
                          Jexp(𝑠, 𝑡) = exp(𝑠, −𝑡)K = true,           i.e.,      Jexp(𝑠, 𝑡)K = Jexp(𝑠, −𝑡)K .
We have:
                                Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = J𝑠K | −J𝑡 K | = J𝑠K | J−𝑡 K | = Jexp(𝑠, −𝑡)K
                                                                                                                                        □

A.3    Proof of Lemma 13
Lemma 13. Let 𝑠, 𝑡 be terms of sort Int. Then bnd1 – bnd5 are EIA-valid.
   Proof. We already showed EIA-validity of bnd5 in Sect. 4. For bnd1 , assume
                                                J𝑡 = 0K = true,        i.e.,     J𝑡K = 0.
Then it remains to show
                                      Jexp(𝑠, 𝑡) = 1K = true,          i.e.,     Jexp(𝑠, 𝑡)K = 1.
We have
                                           Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = J𝑠K |0| = J𝑠K0 = 1.
   For bnd2 , assume
                                                J𝑡 = 1K = true,        i.e.,     J𝑡K = 1.
Then it remains to show
                                     Jexp(𝑠, 𝑡) = 𝑠K = true,         i.e.,      Jexp(𝑠, 𝑡)K = J𝑠K .
We have
                                    Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = J𝑠K |1| = J𝑠K1 = J𝑠K .
   For bnd3 , we first show the implication from left to right. So assume
                                   J𝑠 = 0 ∧ 𝑡 ≠ 0K = true,          i.e.,      J𝑠K = 0 and J𝑡K ≠ 0.
Then it remains to show
                                      Jexp(𝑠, 𝑡) = 0K = true,          i.e.,     Jexp(𝑠, 𝑡)K = 0.
We have
                                         Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = 0 | J𝑡 K | = 0
where the last equality holds as we have J𝑡K ≠ 0, and thus | J𝑡K | > 0.
  For the implication from right to left, assume
                                      Jexp(𝑠, 𝑡) = 0K = true,          i.e.,     Jexp(𝑠, 𝑡)K = 0.
30   • F. Frohn, J. Giesl


Then it remains to show
                                 J𝑠 = 0 ∧ 𝑡 ≠ 0K = true,       i.e.,   J𝑠K = 0 and J𝑡K ≠ 0.
We have
                                                Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = 0.
So as J𝑠K | J𝑡 K | ≠ 1, we get | J𝑡K | ≠ 0 and thus also J𝑡K ≠ 0. As a product is only 0 if one of its factors is 0, we also
get J𝑠K = 0.
  For bnd4 , assume
                                                J𝑠 = 1K = true, i.e., J𝑠K = 1.
Then it remains to show
                                        Jexp(𝑠, 𝑡) = 1K = true, i.e., Jexp(𝑠, 𝑡)K = 1.
We have
                                                Jexp(𝑠, 𝑡)K = J𝑠K | J𝑡 K | = 1 | J𝑡 K | = 1.
                                                                                                                           □
