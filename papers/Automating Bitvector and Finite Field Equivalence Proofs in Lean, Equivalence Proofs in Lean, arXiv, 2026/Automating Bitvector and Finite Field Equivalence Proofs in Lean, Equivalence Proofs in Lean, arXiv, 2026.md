                                                   Automating Bitvector and Finite Field
                                                       Equivalence Proofs in Lean

                                             Elizaveta Pertseva1 , Valentin Robert2 , Clark Barrett1 , and James Parker2
                                                           1
                                                               Stanford University (pertseva@stanford.edu)
                                                                                   2
                                                                                     Galois
                                                Abstract. Efforts to verify Zero-Knowledge Proof circuit encodings have
arXiv:2605.15163v1 [cs.LO] 14 May 2026




                                                highlighted the challenge of proving the correctness of quantifier-free
                                                statements that make use of both bitvector and finite field operations.
                                                Existing verification workflows are either manual or rely on SMT solvers,
                                                which scale poorly on some classes of problems for reasons that include
                                                difficulties with conversion operators and challenges reasoning about in-
                                                equalities. To address these limitations, we present a novel Lean tactic
                                                BitModEq that leverages range lemmas and case analysis to produce veri-
                                                fied translations from finite fields to bitvectors. Our approach, combined
                                                with bit-blasting, outperforms state-of-the-art SMT solvers, solving 19%
                                                more ZKP arithmetization benchmarks.


                                         1     Introduction
                                         Recent advances in Zero-Knowledge Proofs (ZKPs) have led to the utilization
                                         of ZKPs in critical applications such as cryptocurrencies [17], post-quantum
                                         signature schemes [7], voting systems [23], proofs of vulnerabilities [10, 11], and
                                         image authentication [12]. ZKPs are cryptographic algorithms that enable one
                                         party (the prover) to convince another party (the verifier) that some secret data
                                         satisfies a property ϕ without revealing any information about the data.
                                            ZKP statements use the language of finite fields, where operations such as
                                         addition and multiplication are performed modulo a prime. However, real-world
                                         systems operate over concrete machine integers, using arithmetic modulo some
                                         power of two, also known as the theory of bitvectors. As a result, ZKP statements
                                         often require arithmetizations which encode bitvector operations as finite field
                                         operations. The correctness of these arithmetizations is crucial for the soundness
                                         of ZKP systems, but constructing them can be error-prone.
                                            Prior work on verifying ZKP arithmetizations has followed two main ap-
                                         proaches: manual and automatic. The manual approach typically works by em-
                                         bedding entire ZKP systems in interactive theorem provers (ITPs), as seen in
                                         formalizations of SP1 Hypercube and Cairo [3, 38]. While these efforts provide
                                         strong correctness guarantees, they require substantial human effort. Further,
                                         because ZKP optimizations evolve rapidly, arithmetizations frequently change,
                                         requiring significant portions of the verification effort to be revisited.
                                            The automatic approach reduces verification to solving Satisfiability Modulo
                                         Theories (SMT) queries [30, 37]. While this approach enables greater automa-
                                         tion, it poses two fundamental challenges that limit what can be done automat-
                                         ically. First, arithmetizations simultaneously involve bitvectors and finite fields,
2                                   E. Pertseva et al.

                    x0 y0    x0 + y0 x0 · y0   20 · (x0 + y0 − x0 · y0 )
                     0   0      0       0                 0
                     1   0      1       0                 1
                     0   1      1       0                 1
                     1   1      2       1                 1
Table 1: Evaluation table for the finite field polynomial encoding (1) of bvor
(bitwise OR) in the Jolt zkVM for 1-bit inputs [2].

requiring the use of theory conversion operators that create performance prob-
lems for SMT solvers. Second, SMT solvers contain a much larger trusted code
base (TCB) than ITPs, which increases the probability of missed bugs.3
   To address these challenges, we present BitModEq, a Lean tactic that trans-
lates finite field operations to bitvectors and solves the resulting goals via bit-
blasting [8]. BitModEq retains the guarantees of ITPs and outperforms existing
automatic methods. Our approach is guided by two main insights.
   First, the majority of ZKP arithmetizations do not inherently rely on field-
specific behavior (e.g., inverses or field division). Instead, they simulate bit-level
operations inside the field, producing large numbers of inequality constraints
that overwhelm the finite field reasoning engines. To remedy this, we propose
automatically translating field elements back to bitvectors during verification,
enabling efficient reasoning over the original bit-level semantics.
   Our second insight is that the effectiveness of the translation primarily relies
on range analysis. With tighter bounds, we can more frequently eliminate modulo
operations, creating bitvectors of smaller widths. While Lean already has built-
in lemmas for reasoning about equation ranges, they do not consider variable
dependencies, which are crucial in bitvector operations simulating arithmetic. To
remedy this, we design a Lean-specific range analysis that mixes Lean lemmas
with targeted case reasoning. Our main contributions are as follows:

 1. A Lean tactic BitModEq that translates from finite fields to bitvectors.
 2. A proof-of-concept bounded verification of two real-world ZKP encodings
    that increases the bounds achieved by previous techniques.
 3. A Lean range analysis tactic for proving goals resulting from the translation.

   The remainder of the paper is organized as follows. We first present a motivat-
ing example (Section 2) and relevant background (Section 3). We then describe
our translation algorithm (Section 4.2), range analysis tactic (Section 4.3), and
Lean implementation (Section 4.4). We conclude with an evaluation (Section 5),
related work (Section 6), and a discussion of future work (Section 7).

2     Motivating Example
Consider the polynomial shown in (1) over a finite field of order P , where P
is larger than 2B . The polynomial is an encoding of the bvor (bitvector OR)
3
    Work on emitting proof certificates from SMT solvers is one approach for addressing
    this [5], but proof support for the theory of finite fields remains ongoing research.
                    Automating Bitvector and Finite Field Equivalence Proofs in Lean                            3

operation used in the Jolt zkVM [2]. In this encoding, xi represents the i-th bit
of one operand, and yi represents the i-th bit of the other. We show all possible
values for the polynomial and its subexpressions for the case B = 1 in Table 1.

                                        B−1
                                        X
                                              2 i xi + y i − x i · y i
                                                                         
                                                                                                          (1)
                                        i=0

To verify that (1) correctly encodes the bvor operation, we must encode the
relationship between the bitvector operation and the finite field polynomial (1).
Inspired by prior work [30], we rely on a predicate ff2bv(bv , e) (read as bv is
the bitvector encoding of the finite field element e) that encodes an equivalence
between a bitvector bv of bit width N and a finite field term e. While the exact
definition of ff2bv varies across systems [2, 27, 38], it most often includes a range
check. In Jolt, ff2bv(bv , e) is defined if and only if the value of e is smaller than
the target bitvector size, 2N ; otherwise, the operation is undefined.4 Let bv 1 , bv 2
be bitvectors of bit width B, and let xi , yi be finite field elements from field P ,
for i ∈ {0, . . . , B − 1}. Our full verification query becomes:
      V                                                  V
          i∈{0...B−1}   ff2bv(bv 1 [i], xi )                 i∈{0...B−1}     ff2bv(bv 2 [i], yi )
                                                PB−1                                                     (2)
                                                             i
                 ff2bv(bvor bv 1 bv 2 ,            i=0   2 (xi + yi − xi · yi ))

   One of the main focuses of this paper is the question of how to efficiently
embed the ff2bv operator. Previous SMT-based approaches are bottlenecked
by the ff2bv embedding for two main reasons. First, since SMT solvers do not
support direct conversion from finite fields to bitvectors, the encoding must use
bit splitting, which adds a large number of variables. Second, since current SMT
theories of finite fields do not support inequalities directly [15], the SMT encoding
                                             Q2N −1
must use a finite field polynomial f (e) = i=0 (e − i) for range checks,5 which
slows down the solver. The full SMT encoding of ff2bv is as follows:
                                   N
                                  2Y −1                                               N
                                                                                      X −1
    ff2bvSMT (bv , e) ⇐⇒                (e − i) = 0 ∧ ∃ e0 · · · eN −1 . e =                 2i ei
                                  i=0                                                  i=0
                                                                                                          (3)
                             −1
                            N^                             −1
                                                          N^
                        ∧         ei (ei − 1) = 0 ∧                bv [i] = ite(ei = 0, 0[1] , 1[1] ),
                            i=0                              i=0


where c[B] denotes a bitvector constant with value c and bit width B, and 2N is
smaller than the order of the finite field, as is the case for Jolt. A weaker SMT
encoding can omit the range check polynomial, assuming instead that no overflow
occurs during the conversion. If this assumption is correct, bit splitting already
constrains the values of e appropriately. We refer to this as the weak encoding,
4
    Other systems may apply a modulo operation or return zero when e is too large.
5
    f (e) is zero on and only on {0, . . . , 2N − 1} and thus fixes the possible values of e
    to the interval {0, . . . , 2N − 1} [30].
4                               E. Pertseva et al.

as it relies on an unproved assumption. However, even the weak version of ff2bv
remains challenging for SMT solvers, as bit splitting is still present.
   In contrast, ITPs have richer semantics than SMT solvers, enabling direct con-
version between different types, including from finite fields to natural numbers
and from natural numbers to bitvectors. Inspired by manual proofs [3, 38], we
rely on a toNat(e) function (present in most ITPs [25]) that maps a finite field
term to its underlying natural number value. Then, the f (e) polynomial becomes
a simple range check over the natural numbers: toNat(e) ≤ 2N − 1. Similarly,
instead of bit splitting, we can use toBV(N, t), a function that converts a natural
number term t to a bitvector of size N . Our ff2bv encoding is thus:

        ff2bvITP (bv , e) ⇐⇒ toNat(e) < 2N ∧ bv = toBV(N, toNat(e)).           (4)

Decoding ff2bv in (2) yields:
        V
                        bv1[i] = toBV(1, toNat(xi )) ∧ toNat(xi ) ≤ 1
        Vi∈{0,...,B−1}
          i∈{0,...,B−1} bv2[i] = toBV(1, toNat(yi )) ∧ toNat(yi ) ≤ 1
                                      P                                 (5)
                                           B−1
      (bvor bv1 bv2) = toBV B, toNat i=0 2i (xi + yi − xi · yi )
                               P                         
                                  B−1
                       ∧ toNat i=0 2i (xi + yi − xi · yi ) ≤ 2B − 1

While more compact, the ITP encoding raises the following question: to discharge
the two goals, how can one relate the conversions appearing in the goal to those
applied to variables in the premises?
  Our solution is an algorithm that soundly distributes the operators toNat
and toBV over finite field and natural number operations using range analysis.
On the Jolt OR example, our approach, combined with bit-blasting, is able to
automatically verify inputs with widths of up to 32 bits within five minutes and
8GB of memory. Under the same limits, the cvc5 SMT solver only verifies inputs
with widths up to 9 bits under the weak encoding and up to 3 under the full
encoding.

3     Background
In this section, we introduce the notation and logical frameworks used through-
out the paper. We first describe the different arithmetic domains we will reason
about [13, 22]; we then discuss the logical setting we use [14]; and we con-
clude with an overview of Lean [25] and some existing Lean automation tech-
niques [6, 8, 24]. More details can be found in the cited work.
3.1   Arithmetic Domains
We reason about expressions over three arithmetic domains: natural numbers,
finite fields, and bitvectors. We write N for the natural numbers (including 0) and
N>0 for strictly positive naturals. In N, subtraction is truncated: for A, B ∈ N,
the term A − B is defined as usual unless B > A, in which case it is 0. We use
[i, j] to represent the set {n ∈ N | i ≤ n ≤ j} and [n] to abbreviate [1, n].
                 Automating Bitvector and Finite Field Equivalence Proofs in Lean         5


              Signature     Sort                  Set of Symbols

                 ΣFP        FP                   {·FP , +FP , −FP }
                 ΣN          N            {·N , +N , −N , mod N , ≤N , ≥N }
                 ΣBV        BVN     {·[N ] , +[N ] , −[N ] , mod [N ] ≤[N ] , ≥[N ] }
              ΣF P ∪ Σ N   FP , N                     {toNat}
              ΣN ∪ ΣBV     N, BVN            {toBV[N ] , bvToNat[N ] }

Table 2: Relevant symbols from the theories referenced in this paper. For ΣBV ,
symbols are parameterized by N ∈ N>0 , which represents the bit width.

  We use FP , with P ∈ N>0 prime, to denote a finite field of order P (we consider
only prime-ordered fields). The field FP is isomorphic to the natural numbers
modulo P . We use the function toNat : FP → N to return the representative in
N of an element of FP .
  We use BVN with N ∈ N>0 to denote a bitvector of width N . Bitvectors can
be viewed as finite sequences of bits, and we write b[i] to denote the i-th bit of
a bitvector b. Bitvectors have a canonical natural number representation in the
range [0, 2N − 1]. We use the function bvToNat : BVN → N to map a bitvector
to its natural number representation and the function toBV : N × N → BVN to
map a natural number to its N -bit encoding.

3.2   Logical Setting & Notation
Logic We work in the logical setting of many-sorted quantifier-free first-order
logic with equality, using standard terminology throughout. We use Σ to denote
a many-sorted signature with a finite set of sorts, including Bool. We also assume
a family of equality symbols =σ : σ × σ → Bool for each σ ∈ Σ. We assume the
usual definitions of well-sorted terms and formulas (terms of sort Bool). We
use v, w to denote variables, t to denote an arbitrary terms, and γ to denote
an arbitrary formula. A theory consists of a signature together with a fixed
interpretation of some subset of its symbols.
   We consider three base theories, each with a corresponding signature. The
most relevant symbols are shown in Table 2. The finite field signature ΣFP
includes the finite field sort, which we also denote FP , and the standard finite field
operators [15]. The natural number signature ΣN includes the natural number
sort, which we also denote N, and the usual arithmetic operators. The bitvector
signature ΣBV includes, for each N ∈ N>0 , the bitvector sort for bitvectors of
size N , which we also denote BVN and the SMT-LIB bitvector operators [33].
For all signatures, when the intended sorts of operators are clear from context,
we write operators without explicit sort annotations.
   We allow theory combination in the standard way. When working in the com-
bined theory, we additionally assume the signature is extended with three con-
version operators matching the three conversion functions (toNat, toBV, and
bvToNat) mentioned above. For convenience, we refer to both the functions
themselves and the operators with the same notation.
6                                E. Pertseva et al.

Notation For a formula γ and terms s and t, we write s ⪯ γ to denote that s
occurs as a subterm of γ. We write γ[s/t] for the formula obtained by replacing
all occurrences of s in γ with t. We lift this notation pointwise to sets of formulas
and tuples of sets of formulas. For a set S of formulas, S[s/t] denotes the set
obtained by replacing all occurrences of s in S with t. Similarly, for a tuple
T = (S1 , S2 ) of sets of formulas, we define T [s/t] = (S1 [s/t], S2 [s/t]). We also
lift set membership to tuples of sets, using γ ∈ T to denote γ ∈ S1 ∪ S2 . We
write S \ γ to abbreviate set S \ {γ} and S, γ to abbreviate S ∪ {γ}. Finally, we
write S := S ′ to denote assignment of S to S ′ and S |= γ to indicate that γ is
logically implied by S.

3.3   Lean & SMT
Lean Lean [25] is an interactive theorem prover (ITP) that allows users to me-
chanically verify mathematical theorems, including those about properties of
software. Lean provides a tactic language that enables users to interactively con-
struct proofs by transforming proof states, which consist of a goal together with
a local hypothesis context. Lean’s type checker automatically verifies proofs for
users and throws errors during compilation if a proof is not valid. This provides
high confidence that the proof is correct, as it shrinks the trusted computing base
(TCB) to Lean’s small trusted kernel. Lean is based on higher-order logic and
is therefore more expressive than the first-order setting described above. Our
tactic operates on Lean goals but reasons in the restricted first-order setting,
which is typically sufficient for ZKP arithmetizations. We thus use the notation
of many-sorted first-order logic in this paper, with the understanding that we
are working with a corresponding logical fragment within Lean.

SMT Satisfiability Modulo Theories (SMT) solvers allow users to automati-
cally verify theorems expressed in the language of many-sorted first-order logic
with theories. Some commonly supported theories include uninterpreted func-
tions, integer and real arithmetic, and arrays and bitvectors [6]. SMT solvers are
more automated but less expressive than ITPs. To solve queries over multiple
theories, SMT solvers employ dedicated theory solvers and theory combination
mechanisms such as the Nelson-Oppen framework [26]. Since each theory solver
operates independently, conversion operators are typically challenging to support
and expensive for the solvers to reason about.
   There are two main approaches for integrating SMT-like reasoning with Lean.
The first involves translating Lean proof obligations into SMT queries, sending
them to an external SMT solver, and then reconstructing the proof in Lean to
convince the kernel of the result [24]. The reconstruction approach only supports
a subset of SMT theories, not including (at the time of writing) finite fields and
bitvectors. The second approach is to implement SMT-like decision procedures
directly in Lean, which keeps the reasoning inside the proof assistant but may
lead to increased solving times due to the need to perform the proof search within
Lean. In this paper, we follow the second approach and rely on bv_decide, a
bit-blasting decision procedure implemented in Lean [8].
                          Automating Bitvector and Finite Field Equivalence Proofs in Lean                                7

                      ΣFP ∪ ΣN ineqs. from to_N


ΣFP ∪ ΣN ∪ ΣBV                  to_N                 ΣN ∪ ΣBV               to_BV                ΣBV          bit_blast

      ΣN ineqs.
      from goal


 rng_analyze        ΣN ineqs.           diff. rule              ΣN ineqs.           diff. rule

           ∃ un-
           solved
           ineqs.

    unknown ✗               rng_analyze                                 rng_analyze               unknown ✗   valid ✓


Fig. 1: BitModEq workflow. The tactic accepts terms over ΣFP and ΣBV , and
terms originating from toNat and bvToNat operators. It first converts FP terms
to N terms and then converts N terms to BVN terms. Inequalities are discharged
by rng_analyze. If rng_analyze cannot prove an inequality from the original
goal, the tactic returns unknown; if it cannot prove a premise from a translation
rule, a different rule is applied. Once only ΣBV goals and hypotheses remain, the
goals are discharged via bit-blasting. valid is returned if and only if bit-blasting
solves the problem and no inequalities remain.

4      BitModEq
In this section, we describe the BitModEq algorithm. We begin with a high-level
overview and then examine its core elements: conversion and range analysis.

4.1       Overview
Figure 1 illustrates the BitModEq workflow, which operates in four phases:

 1. Convert all terms of sort FP in the proof context to terms of sort N.
 2. Discharge any inequalities over N in the original goal using range analysis.
 3. Convert any remaining terms of sort N to bitvector terms.
 4. Discharge the final bitvector equality goal via the bv_decide tactic.

Since finite field elements do not admit a canonical bitvector representation, we
must select an intermediary domain. Two natural candidates are the integers and
the natural numbers. We choose the natural numbers for two reasons. Primarily,
in the majority of the ZKP arithmetizations, finite field variables are used to
simulate bits and therefore do not represent negative values. Second, converting
integers to bitvectors requires reasoning about both lower and upper bounds,
whereas conversion from natural numbers requires reasoning only about upper
bounds, eliminating a significant portion of the proof obligations.
   Both conversion passes, steps (1) and (3), traverse the input term from the root
and push conversion operators through arithmetic operators toward variables
and constants. If we can show that no modular wraparound is possible for an
operand, we do not have to account for overflow or underflow and thus end up
with much simpler resulting terms.
8                                    E. Pertseva et al.

  For example, consider the bvor example from Section 2. For B = 1, when we
are pushing toNat inward in toNat(x0 + y0 − x0 · y0 ), if we can show that
                           toNat(x0 · y0 ) ≤ toNat(x0 + y0 ),                           (6)
we know the expression won’t become negative (which would result in wraparound)
and thus can soundly drop the modulus, executing the transformation:
            toNat(x0 + y0 − x0 · y0 ) → toNat(x0 + y0 ) − toNat(x0 · y0 ).              (7)
If we cannot prove Equation (6), we have to account for possible wraparound,
and our transformation becomes:
    toNat(x0 + y0 − x0 · y0 ) → (toNat(x0 + y0 ) + P − toNat(x0 · y0 )) mod P, (8)
which results in much larger bit widths that take longer to bit-blast. Therefore,
we use different translation transformations (Section 4.2) for cases where mod-
ular wraparound must be accounted for and cases where it can be ruled out. To
prove the absence of wraparound, we rely on range analysis.
   A natural design choice would have been to rely on Lean’s existing automation,
such as ring_nf, omega, or aesop, to discharge inequality goals. However, initial
experiments showed that these tactics are often overwhelmed by large coefficients
or struggle to handle variable dependencies and bound information arising in
ZKP arithmetizations. We therefore design a dedicated range analysis algorithm.
   Similar to the conversion passes, our range analysis, described in (Section 4.3),
is syntax-directed: it traverses the formula from the root toward variables and
constants, introducing symbolic bounds for intermediate subterms. Leaf goals are
discharged using bounds from the hypothesis context,6 and the resulting informa-
tion is propagated back toward the root. We additionally incorporate specialized
patterns that capture common bit-specific variable dependencies. While incom-
plete, our range analysis is largely independent of numeric magnitude and can
be more efficient than bit-blasting for large bit widths. Thus, we also use range
analysis to discharge ΣN -inequalities present in the original goals in step (2).
   The theorem is proven once range analysis discharges all inequalities and bit-
blasting discharges the final bitvector equality. Otherwise, we return unknown.
4.2     Translating from Finite Fields to Bitvectors
In this section, we present our translation calculus, which contains two types
of rules: rules that convert from finite fields to natural numbers (Figure 2) and
rules that convert from natural numbers to bitvectors (Figure 3).
   We follow the common practice of presenting rules that modify configura-
tions [32, 36]. In our calculus, a configuration is a proof context Γ , represented
as a tuple (G, H), where G is a set of goals and H is a set of global hypotheses
shared across all goals. When a rule modifies only G or only H we omit the
unchanged component. Rules are presented in guarded assignment form, where
the premises describe the configurations to which the rule can be applied, and
the conclusion describes the modification to the configuration. A sequence of
applications is called a derivation. We now present the two types of rules.
6
    All variables have bounds as they are either finite field or bitvector variables.
                    Automating Bitvector and Finite Field Equivalence Proofs in Lean           9

                                         t1 , t 2 , t 3 : F P γ ∈ Γ t1 − t 2 + t 3 ⪯ γ
                   mvZModSub
                                            Γ := Γ [t1 − t2 + t3 /(t1 + t3 ) − t2 ]

                                            t1 , t 2 : F P t1 = t 2 ∈ Γ
                      injNat
                                    Γ := Γ [t1 = t2 /toNat(t1 ) = toNat(t2 )]

                        t1 , t 2 : F P     γ∈Γ       ▷◁ ∈ {+, ·}     toNat(t1 ▷◁FP t2 ) ⪯ γ
       distNat
                     Γ := Γ [toNat(t1 ▷◁FP t2 )/(toNat(t1 ) ▷◁N toNat(t2 )) mod P ]

         dist  t1 , t2 : FP t3 : Bool γ ∈ Γ toNat(ite(t3 , t1 , t2 )) ⪯ γ
        NatIte Γ := Γ [toNat(ite(t3 , t1 , t2 )/ite(t3 , toNat(t1 ), toNat(t2 ))]

    dist      t1 , t 2 : F P   γ ∈ Γ toNat(t1 − t2 ) ⪯ γ H |= toNat(t1 ) ≥ toNat(t2 )
   NatSub                      Γ := Γ [toNat(t1 − t2 )/toNat(t1 ) − toNat(t2 )]

      distNat             t1 , t2 : FP γ ∈ Γ toNat(t1 − t2 ) ⪯ γ
     SubOvrflw Γ := Γ [toNat(t1 − t2 )/(toNat(t1 ) + P − toNat(t2 )) mod P ]

                 v1 : FP       v1 ⪯ γ       γ ∈ Γ toNat(v1 ) ≤ N ∈/ H for N ∈ [0, P − 1]
     addBds
                                          H := H ∪ {toNat(v1 ) ≤ P − 1})

            t1 , t2 , t3 : N γ ∈ Γ ▷◁ ∈ {+, ·} (t1 mod t3 ▷◁ t2 mod t3 ) mod t3 ⪯ γ
   mvMod
                       Γ := Γ [(t1 mod t3 ▷◁ t2 mod t3 ) mod t3 /(t1 ▷◁ t2 ) mod t3 ]

                      P ∈ N>0            t1 : N t1 mod P ⪯ γ γ ∈ Γ           H |= t1 ≤ P − 1
      dropMod
                                                Γ := Γ [t1 mod P/t1 ]

                                             t1 : FP t1 · t1 = t1 ∈ Γ
                          sqrBds
                                         Γ := Γ [t1 · t1 = t1 /toNat(t1 ) ≤ 1]

Fig. 2: Translation rules from FP to N. Γ = {G, H} denotes the proof context,
where G is the set of goals and H is the global set of shared hypotheses.

Finite Fields to Natural Numbers mvZModSub groups additions before subtrac-
tions to accumulate positive values and ensure minimal underflow cases. injNat
replaces finite field equations with natural number equations. distNat distributes
the toNat operator over addition and multiplication and adds mod for sound-
ness. Similarly distNatIte distributes the operator over if/then/else.
   distNatSub distributes the toNat operator over subtraction when no negative
values are possible. The mod operator can be soundly dropped as toNat(t1 )
ensures the starting expression is less than P and subtraction by another natural
number will only lower the final value. In cases where the premises of distNatSub
cannot be discharged, we rely on distNatSubOvrflw, which ensures soundness
by eliminating the possibility of negative values by adding P and then ensuring
the result is in bounds by applying mod P . addBds adds bounds for finite field
variables present in the proof context to ensure equisatisfiability of the natural
number constraints. mvMod simplifies the term by factoring out mod. When the
term is smaller than the modulus, we apply dropMod to remove the modulus.
10                                     E. Pertseva et al.


              N ∈ N>0    t1 , t2 : N t1 = t2 ∈ Γ H |= t1 ≤ 2N − 1 H |= t2 ≤ 2N − 1
  injBV
                              Γ := Γ [t1 = t2 /toBV(N, t1 ) = toBV(N, t2 )]

                          N ∈ N>0     t1 , t 2 : N   ▷◁ ∈ {≤, ≥}   t1 ▷◁N t2 ∈ H
injBV         toBV(N, t1 ) ▷◁[N ] toBV(N, t2 ) ∈
                                               /H     H |= t1 ≤ 2N − 1 H |= t2 ≤ 2N − 1
LeqHyp                        H := H ∪ {toBV(N, t1 ) ▷◁[N ] toBV(N, t2 )}

                N ∈ N>0 t1 , t2 : N γ ∈ Γ ▷◁ ∈ {+, ·} toBV(N, t1 ▷◁N t2 )) ⪯ γ
     distBV
                     Γ := Γ [toBV(N, t1 ▷◁N t2 )/toBV(N, t1 ) ▷◁[N ] toBV(N, t2 )]

     distBV N ∈ N>0 t1 , t2 : N t3 : Bool γ ∈ Γ toBV(N, ite(t3 , t1 , t2 )) ⪯ γ
       Ite    Γ := Γ [toBV(N, ite(t3 , t1 , t2 ))/ite(t3 , toBV(N, t1 ), toBV(N, t2 ))]

                           N ∈ N>0     t1 , t 2 : N γ ∈ Γ    toBV(N, t1 − t2 ) ⪯ γ
            distBVSub                  N
                          H |= t1 ≤ 2 − 1 H |= toBV(N, t1 ) ≥ toBV(N, t2 ))
                          Γ := Γ [toBV(N, t1 − t2 )/toBV(N, t1 ) − toBV(N, t2 )]

                      C, N ∈ N>0 t1 : N γ ∈ Γ C ≤ 2N − 1 H |= t1 ≤ 2N − 1
       distBVMod
                       Γ := Γ [toBV(N, t1 mod C)/toBV(N, t1 ) mod toBV(N, C)]

                         Fig. 3: Translation rules from N to BVN .

   While the majority of ZKP arithmetizations only use finite field variables
to represent bits, the restriction that a variable must be 0 or 1 relies on finite
field reasoning (finite fields’ not having zero divisors), because finite fields do not
naturally support comparisons or the Boolean operator or. Thus, we add sqrBds
to detect bit encodings and translate them to natural number inequalities.

Natural Numbers to Bitvectors As long as both sides of the expression fit into a
bitvector of width N without overflow, injBV replaces natural number equalities
with bitvector equalities of bit width N . While there might be inequalities, in
our goal we leave them to range analysis and do not translate them. For hypoth-
esis inequalities, we use injBVLeqHyp to maintain both the natural number and
bitvector representations, so the inequalities can be used by the range analysis al-
gorithm and by bit-blasting. distBV distributes the toBV operator over addition
and multiplication. Unlike distNat there is no need to add a mod operator, as
we remain in the mod 2N space. distBVIte distributes the toBV operator over
if/then/else. distBVSub distributes the toNat operator over subtraction when
no negative values are possible. Unlike distNatSub, we add a second check that
t1 ≤ 2N − 1 because t1 is not naturally a bitvector and might overflow, while
in distNatSub, t1 is a ZMod P and is thus constrained to be less than or equal
to P − 1. We do not include a rule for cases where negative values are possible,
since this case will never arise from the finite field to natural number translation
rules. Last but not least, both dropMod and distBVMod handle cases where the
natural number encoding contains the mod operator. In cases where we cannot
prove that the term is smaller than the modulus (dropMod does not apply) we
                  Automating Bitvector and Finite Field Equivalence Proofs in Lean         11

   In: Proof context Γ = (G, H)                In: Proof context Γ = (G, H)
   Out: Modified Γ                             Out: Modified Γ
 1 def to_N(Γ ):                             1 def to_BV(Γ ):
 2     progress ← True                       2     b←2
 3     while progress do                     3     for γ ∈ Γ do
 4        progress ← (sqrBds ||              4         for t ⪯ γ do
            injNat || mvZModSub ||           5             b ← max(clcBVWdth(t),b)
            distNat || distNatIte ||         6     progress ← True
            distNatSub ||                    7     while progress do
            distNatSubOvrflw ||              8         progress ← injBVLeqHyp(b)
            mvMod || dropMod ||              9     progress ← True
            addBds)                         10     while progress do
                                            11         progress ← (injBV(b)||
             (a) Strategy to_N                          distBV || distBVIte ||
                                                        distBVSub || distBVMod)

                                                        (b) Strategy to_BV

       Fig. 4: Strategies for applying translation rules from Figures 2 and 3.

apply distBVMod and distribute toBV as long as both the modulus and the term
are smaller than 2 to the power of the bit width.
Strategy Figure 4 presents our strategy, shown as pseudocode in which we assume
that each translation rule returns True iff it applies and changes Γ . We also
assume that injBV and injBVLeqHyp take as input the target bit width. (s1 ∥
· · · ∥ sk ) is evaluated from left to right, stopping after the first True result.
We first execute calculus rules according to Strategy to_N and then Strategy
to_BV. clcBVWdth(t) is a function that overapproximates the maximum possible
bit width needed to ensure t can be represented without overflow.7
- to_N The strategy consists of a while loop, where a rule is only attempted
once the previous rule no longer applies. We begin with sqrBds to translate any
bit encodings to bounds in case other rules rely on them. We then apply injNat
and use mvZModSub to minimize underflow cases. Then, while one of distNat,
distNatIte, distNatSub, or distNatSubOvrflw applies, we continue pushing
toNat inward. We always attempt distNatSub before distNatSubOvrflw to
ensure the final translation is as simple as possible. Once we reach saturation,
we factor out the mod operations that came from distribution. Once no more
mod operations can be factored we attempt to drop all mod operators (line 4).
- to_BV We begin by setting the maximum bit width b for the conversion to 2
(line 2). Then, for each hypothesis and goal we update b if any subterm requires
a larger bit width (line 5). We calculate the maximum bit width across all of
the terms to have a higher chance of proving the goal. For example, let x ∈ N,
and suppose we translate a hypothesis x ≤ 1 to toBV(2, x) ≤ 1[2] but then use
toBV(4, x) in the goal. The goal then no longer follows from the hypothesis. A
7
    In our implementation, the bit width is calculated per variable, but we use a global
    bit width here to keep the presentation simple.
12                                        E. Pertseva et al.

                   t1 , t 2 : N     ▷◁ ∈ {≤, ≥} γ ∈ G origOnly(t1 ▷◁ t2 ) t1 ▷◁ t2 ≡ γ
     introPVar
                                   G := (G \ γ) ∪ {t1 ▷◁ w, t2 ({≤, ≥}\ ▷◁) w}

               t1 , t2 : N    ▷◁ ∈ {+, ·} γ ∈ G origOnly(t1 ▷◁ t2 ) t1 ▷◁ t2 ≤ w ≡ γ
leqAddMul
                              G := (G \ γ) ∪ {t1 ≤ w1 , t2 ≤ w2 , w1 ▷◁ w2 ≤ w}

                     t1 , t2 : N      γ ∈ G origOnly(t1 − t2 )    t1 − t 2 ≤ w ≡ γ
          leqSub
                                          G := (G \ γ) ∪ {t1 ≤ w}

                    t1 , t2 : N γ ∈ G origOnly(t1 mod t2 ) t1 mod t2 ▷◁ w ≡ γ
          leqMod
                                      G := (G \ γ) ∪ {t2 ≤ w}

leq      t3 : B t1 , t2 : N γ ∈ G origOnly(t1 ) origOnly(t2 ) ite(t3 , t1 , t2 ) ≤ w ≡ γ
If                      G := (G \ γ) ∪ {t1 ≤ w1 , t2 ≤ w2 , max(w1 , w2 ) ≤ w}

Fig. 5: Range analysis rules for inequality decomposition. We use w and wi for
placeholder variables and assume that any new placeholder variables in the con-
clusion are fresh. Other notation follows Figure 2.

possible counterexample could include x = 3[4] as (3[4] )[2] = 2[1] . However, the
value 3 would not have been permitted by the original hypothesis.
   Upon establishing a maximum bit width, we use it to convert all natural num-
bers to bitvectors. We first apply injBVLeqHyp to saturation (to avoid applying
it again if the converted inequalities are later modified, line 8), then cast goals
to bitvectors using injBV, and then push toBV inward until saturation (line 11).
   We state soundness and termination results below.8

Theorem 1. Termination: For any context Γ , no infinite derivation is possible
using strategies to_N and to_BV.

Theorem 2. Soundness: For any context Γ , the bitvector translation Γ ′ pro-
duced by to_N and to_BV from Γ is valid if and only if Γ ′ is valid.

4.3      Range Analysis
We now describe the range analysis algorithm that handles ΣN inequalities. The
algorithm is presented as a calculus in Figures 5-7. At a high level, the algorithm
introduces new placeholder variables and applies lemmas to rewrite goals to
formulas that can be inferred from the hypotheses. It also detects cases where
variable dependencies influence these bounds and enumeration is feasible, and
discharges the resulting goals by enumeration. We first show how the algorithm
works on a simple modulus removal goal that arises during translation of the
example from Section 2 and then explain the rules in more detail.
Motivating Example Revisited Recall that our hypothesis state includes the for-
mulas {toNat(x0 ) ≤ 1, toNat(y0 ) ≤ 1}. One goal that arises when processing
8
     Due to space constraints, the proofs of these and later theorems have been moved to
     the appendix, which also includes a discussion of strategy limitations and tradeoffs.
                   Automating Bitvector and Finite Field Equivalence Proofs in Lean                                 13

                                            C∈N           t1 : N             ▷◁ ∈ {≤, ≥}
                         γ∈G            origOnly(t1 )             t1 ▷◁ w ≡ γ                   t1 ▷◁ C ∈ H
       ineqHyp
                    G := (G \ {γ |γ ∈ G ∧ w ⪯ γ }) ∪ {γ [w/C] | γ ′ ∈ G \ γ}
                                        ′       ′                        ′              ′


                           v : FP           v∈
                                             / pVars           toNat(v) ≤ w ≡ γ γ ∈ G
     leqZMod
                  G := (G \ {γ ′ |γ ′ ∈ G ∧ w ⪯ γ ′ }) ∪ {γ ′ [w/P − 1] | γ ′ ∈ G \ γ}

               N ∈ N>0       v : BV[N ]              v∈
                                                      / pVars bvToNat(v) ≤ w ≡ γ                           γ∈G
      leqBV
                               ′    ′                         ′                ′            N          ′
               G := (G \ {γ |γ ∈ G ∧ w ⪯ γ }) ∪ {γ [w/2                                         − 1] | γ ∈ G \ γ}

                           t1 : N           origOnly(t1 )            t1 ≥ w ≡ γ                  γ∈G
          geNat
                   G := (G \ {γ |γ ∈ G ∧ w ⪯ γ }) ∪ {γ [w/0] | γ ′ ∈ G \ γ}
                                    ′       ′                        ′              ′


                              C∈N                   ▷◁ ∈ {≤, ≥}              γ∈G            C ▷◁ w ≡ γ
                               ∀ γ ′ ∈ G.(w ̸⪯ γ ′ ∨ ∀ v ⪯ γ ′ . v ∈
                                                                   / origVars)
      ineqConst
                     G := (G \ {γ ′ |γ ′ ∈ G ∧ w ⪯ γ ′ }) ∪ {γ ′ [w/C] | γ ′ ∈ G \ γ }

Fig. 6: Range analysis rules for placeholder variable elimination. Notation follows
that of Figure 5.

                                   C1 , C 2 ∈ N γ ∈ Γ C 1 ≤ C 2 ≡ γ
                        eval
                                         G := (G \ γ) ∪ {eval(γ)}

                                    t1 , t 2 , t 3 , v 1 , v 2 : N           ▷◁ ∈ {≤, ≥}
                       γ∈G          t1 ▷◁ t2 ≡ γ            v1 , v2 ⪯ γ             twoOrigVars(γ)
  ineq     hasSub(γ) ∨ origOnly(t1 ) ∧ origOnly(t2 ) v1 ≤ 1 ∈ H v2 ≤ 1 ∈ H
  Cases    G := (G \ γ) ∪ {γ[v1 , v0 /0, 0], γ[v1 , v0 /1, 0], γ[v1 , v0 /0, 1], γ[v1 , v0 /1, 1]}

                                   N ∈ N>0              v1 , t1 , t2 : N           ▷◁ ∈ {≤, ≥}
                     γ ∈ G v1 ·N t1 + (1 − v1 ) ·N t2 ▷◁ w ≡ γ     v1 ≤ 1 ∈ H
          ineqXOR
                           G := (G \ γ) ∪ {ite(v1 = 0, t2 , t1 ) ▷◁ w}

Fig. 7: Range analysis rules for constant and bit reasoning. Notation follows that
of Figure 5.


the conclusion is: toNat(x0 ) + toNat(y0 ) ≤ P − 1. To prove such goals, we in-
troduce placeholder variables, which are implicitly existentially quantified. We
then obtain formulas that can be unified with hypotheses by instantiating the
placeholder variables. The evolution of the goal state is shown below.

    G1 = { toNat(x0 ) + toNat(y0 ) ≤ w1 , P − 1 ≥ w1 }
    G2 = { toNat(x0 ) ≤ w2 , toNat(y0 ) ≤ w3 , w2 + w3 ≤ w1 , P − 1 ≥ w1 }
    G3 = { 1 + 1 ≤ w1 , P − 1 ≥ w1 }
    G4 = { 1 + 1 ≤ P − 1 }
14                              E. Pertseva et al.

   The transition from G2 to G3 uses the hypotheses in H to match the pattern
in the goal, resulting in the concrete bounds obtained in G3 .
   To automate the inequality reasoning we formulate a calculus made up of three
types of rules: Rules that decompose inequalities using placeholder variables
(Figure 5), rules that remove placeholder variables (Figure 6), and rules that
reason about bits and constants (Figure 7).
   To help describe the rules, we introduce additional notation and helper func-
tions. We use original variables, denoted by the set origVars, to describe vari-
ables that exist in the proof context before starting range analysis, and place-
holder variables, denoted by the set pVars, to describe implicitly existentially
quantified variables introduced by the range analysis. origOnly(t) is true iff
all variables occurring in t (of which there must also be at least one) are not in
pVars. twoOrigVars(t) is true iff a term contains exactly 2 distinct variables not
in pVars. hasSub(t) is true iff t contains at least one subtract (−N ) operator.
Inequality Decomposition introPVar introduces a placeholder variable into any
inequality that contains at least one original variable and no placeholder vari-
ables. We ensure that placeholder variables are on the right-hand side of inequal-
ities when original variables or constants are present in the expression, to make
decomposition and elimination easier. leqAddMul and leqIf rely on standard
interval arithmetic [16] to introduce additional placeholder variables into the
context. leqSub strengthens the goal by ignoring t2 , which is reasonable since in
practice t2 rarely has a lower bound other than zero. Finally, leqMod similarly
strengthens the goal by keeping only the modulus.
Placeholder Variable Elimination After decomposition, we eliminate placeholder
variables by instantiating them with bounds derived from the context. The rule
ineqHyp instantiates placeholder variables using inequalities present in the hy-
potheses. The rule leqZMod uses the fact that finite field values are bounded
from above by the field modulus, leqBV uses the fact that N -bit bitvectors are
bounded above by 2N − 1, and geNat relies on the fact that natural numbers
are always greater than or equal to zero. If a placeholder variable occurs in an
inequality with a constant, we instantiate the placeholder variable with the con-
stant itself using ineqConst, but only if all other occurrences of the placeholder
variable do not include original variables. The check ensures we do not get into
a rule application cycle.
Constant and Bit Reasoning Once all placeholder and original variables are
eliminated from a goal, we can use eval to check if the derived constant term is
true. Since the inequality decomposition rules are intentionally syntax-directed
and do not account for dependencies between variables, we add rules that detect
and resolve common dependency patterns in ZKP arithmetizations. ineqCases
identifies potential dependence between two bit-simulating variables v0 and v1 .
We restrict this rule to the setting when only two variables are present to keep
the case analysis manageable. We conservatively flag a dependency when either
(i) the goal contains a subtraction operator, or (ii) both sides of the inequality
contain variables. When a potential dependency is detected, ineqCases performs
                Automating Bitvector and Finite Field Equivalence Proofs in Lean     15

explicit case analysis over the four possible assignments to v0 and v1 . ineqXOR
handles encodings that simulate XORs; if a bit-simulating variable is used as
guard, the goal can be turned into an if/then/else expression.
  Due to its inability to detect and solve all variable dependencies and the fact
that our range analysis sometimes strengthen goal, it is not complete (e.g., eval
might return False for a valid inequality) but it is terminating and sound. We
state the theorems below and include the proofs in Appendix B due to space
constraints.

Theorem 3. Termination: For any context Γ , there is no infinite derivation
from the range analysis calculus.

Theorem 4. Soundness: For any context Γ , if a derivation from Γ reaches a
context where the set of goals is empty, then all goals in Γ hold.

4.4   Implementation
We implement BitModEq in Lean v4.23.0. We use bv_decide [8] for bit-blasting
and mathlib [21] for key lemmas. The majority of our translation and range
analysis rules are implemented using existing lemmas in mathlib. We proved ad-
ditional lemmas for the rules: distNatIte, distNatSubOvrflw, addBds, sqrBds,
injBVLeqHyp, distBVIte, distBVSub, distBVMod, leqSub, and ineqXOR (Fig-
ures 2, 3, 5 and 7). To reliably pattern match and apply lemmas, we require
formulas to be in a normalized form. We rely on Lean’s simp, split_ifs, and
split_ands to simplify the syntax of formulas and add rewrites for commuta-
tivity, associativity and the negation operator. When doing range analysis, we
always first try to apply ineqCases, ineqXOR, ineqHyp and ineqConst to have a
better chance of proving the goal. geNat is only used when no other rules apply.
   We rely on Lean’s metavariable mechanism (introduced as part of lemma
hypothesis) to represent placeholder variables and on Lean’s kernel to eliminate
them throughout the proof context when applying placeholder elimination rules
(Figure 6). The pipeline of BitModEq can involve proving similar inequalities
(e.g., when P ≥ 2N , one way to prove t1 mod P ≤ 2N is to prove t1 ≤ P ∧ t1 ≤
2N ). Thus, to prove the soundness of the bitvector conversion step, when P ≥ 2N
we prove t1 ≤ 2N and use it to solve both goals.

5     Evaluation
Our experiments answer two key empirical questions: (1) How does BitModEq
compare to the state of the art on ZKP arithmetization benchmarks? (2) How
critical is the proposed range analysis algorithm to BitModEq’s effectiveness? All
experiments are run on a cluster with Intel Xeon E5-2637 v4 CPUs.
5.1   Benchmarks
To evaluate the effectiveness of BitModEq, we verify ZKP arithmetizations ex-
tracted from two real-world systems described below. The evaluated systems are
representative of the types of arithmetizations commonly used in many modern
ZKP frameworks, including Cheesecloth and Ligetron [10, 11, 40].
16                                       E. Pertseva et al.


        Solver              Lasso T&S
                                                              Solver       Lasso T&S
        BitModEq             24     12
        cvc5 weak            21      5                        BitModEq      0    0
        cvc5-split weak      10      2                        SMT weak      0     0
        cvc5 strong           4      0                        SMT strong    9    15
        cvc5-split strong     3      0
                                                              # Bench.      24   15
        # Bench.             24     15
                                                       (b) Statement generation timeouts
             (a) Solved instances

     Table 3: BitModEq and cvc5 comparison for Lasso and T&S benchmarks.




          (a) Jolt (Lasso and T&S)                               (b) Sampled CirC

    Fig. 8: Cactus plots across benchmark suites comparing BitModEq and cvc5

Jolt Jolt [2] is a zkVM that relies on lookup tables to encode RISC-V instructions
as finite field polynomials. The original Jolt design uses Lasso [35] to perform
8-bit input lookup tables, while subsequent work, Twist&Shout [34], extends this
approach to 32-bit input tables. We extract the lookup table arithmetizations
from both systems and verify their semantic equivalence to corresponding Lean
bitvector operations.9 We include a breakdown of benchmark size and complexity
in Appendix E.
CirC CirC [27] is a zkVM compiler whose arithmetization passes were previ-
ously verified using cvc5 [30]. We implement a Lean backend for arithmetiza-
tion verification in CirC and generate benchmarks at larger bit-widths than those
considered in prior work.
5.2     State of the Art Comparison
Baselines Since there is no prior automation in Lean that works on ZKP arithme-
tizations, we compare BitModEq against cvc5’s [4] two main finite field decision
procedures, one based on full Gröbner bases [28] and the other on split Gröbner
bases [29] (v.1.3.2), on benchmarks encoded in the SMT finite field and bitvector
theories. For Jolt we evaluate the weak and strong SMT encodings, as discussed
9
     We omit three Twist&Shout instructions which depend on external assumptions.
                 Automating Bitvector and Finite Field Equivalence Proofs in Lean    17


  Solver                                Bit width                           All
             0   2   4    6   8 10 12 14 16 18 20 22 24 26 28 30 32
  BitModEq 34 50 51 50 49 50 47 43 41 42 40 42 44 38 41 40 35 737
  cvc5       40 78 71 54 38 35 33 34 30 27 26 25 27 26 27 27 23 621
  cvc5-split 40 74 61 47 32 31 28 27 22 21 20 20 21 20 20 21 17 522
  # Bench. 40 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 78 1318

Table 4: BitModEq and cvc5 comparison on CirC benchmarks (0–6 arguments;
0–32 bits), sampling up to two benchmarks per even bit width and operation (i.e.,
min(2, n) where n is the number of benchmarks available). Extraction checks are
not generated at 32 bits, as this is the base width for the operator.



                 Solver                             Jolt T&S CirC
                 BitModEq w/ full range analysis    24   12   737
                 BitModEq w/o case splits           21    8    720
                 BitModEq w/ lean tactics            7    4   434
                 # Bench.                           24   15   1318

Table 5: Ablation study of the BitModEq range analysis procedure and compar-
ison against existing Lean automation tactics.

in Section 2. For CirC benchmarks, we rely on the existing SMT backend, where
the overflow checks are checked by the compiler [30]. In contrast, our Lean en-
coding always maintains the stronger guarantees. If generation of a benchmark
for any encoding takes more than a minute we consider it a timeout.
Jolt We run the Jolt benchmarks with a 20 minute timeout and 16GB memory
limit. As summarized in Table 3a, BitModEq solves three more benchmarks than
the weak cvc5 encoding for the 8-bit lookup tables, and seven more for the
32-bit lookup tables. Table 3b shows that the strong SMT encoding times out
during generation for 24 benchmarks, all of which involve range checks with large
constants (232 ). The weak encoding does not timeout as it avoids the range check.
   The cactus plot in Figure 8a shows that while cvc5 solves simpler benchmarks
faster (e.g., msb, lsb arithmetization), BitModEq significantly outperforms cvc5
on larger benchmarks while also producing kernel-checked proofs, and despite
operating under a stronger encoding.
CirC Using the pipeline from prior work [30], we generate CirC benchmarks
covering arithmetization passes with 0 to 6 arguments using bit widths from 0 to
32. Due to the large number of benchmarks, we focus on even bit widths, sample
up to two benchmarks per arithmetization per bit width, and run with a five
minute timeout and 8GB memory limit. As shown in Table 4, cvc5 outperforms
BitModEq on lower bit widths but scales poorly to the larger ones. BitModEq
solves more benchmarks for 13 out of the 17 bit widths.
18                                   E. Pertseva et al.


                         BitModEq Stage            Runtime (%)
                         Range analysis                   52
                         Translation                      23
                         bv_decide                        21
                         Lean kernel checking              4

Table 6: Average runtime breakdown of BitModEq on solved Jolt benchmarks.
We use type checking as a proxy for Lean kernel checking.
   In general, BitModEq performs well on constraints that simulate bit-level se-
mantics with tightly bounded variables but is less effective on constraints with
unbounded variables or heavy use of field-specific operations (e.g., inverses, nega-
tion). Using large field constants, multiplicative inverse constraints (e.g., equa-
tions of the form x · y = 1), and field negation as an overapproximation, we
estimate that 42% of the CirC benchmarks contain some field-specific behav-
ior.10 These behaviors include arithmetizations corresponding to bitvector oper-
ators such as bvnot and bvsle. Although cvc5’s theory combination approach
is more general and performs better when field-specific operations are present,
its bit-splitting strategy introduces a large number of auxiliary variables, which
significantly degrades performance at higher bit widths.
   Across the benchmark suite, 130 SMT instances timeout during encoding gen-
eration. We include the breakdown in Appendix D. Similarly to the Jolt bench-
marks, as seen in Figure 8b, BitModEq is slower on simpler benchmarks but
outperforms cvc5 on larger ones.
5.3      Range Analysis Evaluation
To evaluate the effectiveness of our range analysis we substitute the algorithm for
a portfolio of existing Lean automation tactics : ring_nf, linarith, nlinarith,
aesop, grind, and omega. We additionally evaluate the impact of disabling case
splitting (ineqCases and ineqXOR). Table 5 shows the results. BitModEq with the
full range analysis solves substantially more benchmarks across all benchmark
sets. Case splits play a more significant role for the Jolt benchmarks because
they tend to contain more variable dependencies.
5.4      Runtime breakdown
To understand the bottlenecks of BitModEq, we measure the time spent in each
stage of the pipeline on the solved Jolt benchmarks. Table 6 shows the results.
Although essential for the success of BitModEq, range analysis accounts for more
than half of the total runtime. This is expected, since the pipeline attempts to
prove range bounds for every operator encountered during translation.
5.5      Discovered bugs
During CirC evaluation, we identified a soundness bug in the 32-bit arithmetic
right shifts (bvashr) related to integer overflow in CirC’s Rust implementation.
10
     In contrast, none of the Jolt benchmarks rely on field-specific behavior.
                Automating Bitvector and Finite Field Equivalence Proofs in Lean       19

The issue was uncovered via SMT-based verification during tool comparison, did
not occur at smaller bit widths, and shows the importance of verification beyond
toy sizes. The CirC developers have been notified and have fixed the issue.

6   Related work
Prior work on verifying ZKP arithmetizations broadly falls into two categories:
manual verification in ITPs and automatic verification using SMT solvers. Man-
ual approaches provide strong end-to-end correctness guarantees but require
substantial proof engineering effort. For example, [38] proves the correctness of
the SP1 Hypercube zkVM instruction chips with respect to Sail’s RISC-V seman-
tics [1], and [3] verifies that Cairo’s AIR correctly constrains execution traces.
Automatic approaches aim to reduce manual effort by relying on SMT solvers.
Özdemir et al. [30] verify CirC’s finite-field-blasting pipeline using cvc5, check-
ing all compiler arithmetizations from 0 to 4 arguments and 0 to 4 bits. While
automated, this approach maintains large encodings and struggles to scale.
   Beyond arithmetization pipelines, a large body of work focuses on the verifica-
tion of ZK circuits themselves. On the proof-assistant side, Liu et al. [20] present
CODA, a circuit language based on refinement types for specifying and proving
circuit properties, while the CIVER tool [18] defines transformation and deduc-
tion rules for verifying Circom circuits. On the SMT side, QED2 [31] detects
underconstrained circuits using finite field reasoning, and Zequal [37] checks con-
sistency between circuits and witness generation. Complementary fuzzing-based
approaches have also been effective at uncovering bugs in ZK circuits and com-
pilers [9, 39, 41]. While valuable for improving security, these techniques focus
on circuit-level properties and do not establish end-to-end correctness guaran-
tees. As demonstrated by bounded verification of CirC’s finite field blasting
passes [30], correctness issues can occur at the level of arithmetization rules
themselves, independent of the generated circuit. Another closely related work
is the verification of Lasso lookup tables by Kwan et al. [19] in ACL2, which
also relies on bit-blasting. Unlike our work, this work relies on ACL2’s existing
correspondence between finite fields and bitvectors and represents lookup tables
as bits instead of finite field elements.
   Finally, our approach connects to prior work on SMT theory translations.
Zohar et al. [42] translate bitvector constraints to integers, while Pertseva et
al. [32] lift and lower constraints between integers and modular arithmetic using
range analysis. However, these works do not produce kernel-checked proofs in an
ITP and do not simultaneously reason across finite field and bitvector theories,
which is essential for verifying ZKP arithmetizations.

7   Conclusion and Future Work
This paper presents BitModEq, a Lean tactic for automatically proving equiv-
alence between finite field and bitvector encodings present in ZKP arithme-
tizations. By combining translation, range analysis, and bit-blasting in Lean,
BitModEq produces kernel-checked proofs and outperforms state-of-the-art solvers
20                              E. Pertseva et al.

on real-world benchmarks. Multiple directions remain for future work. An impor-
tant challenge is verifying systems along rarely exercised code paths, specifically
addressing cases where bit widths exceed the modulus, which will require more
scalable verification. It would also be valuable to characterize when translation
to bitvectors is most effective and when direct theory combination or finite-
field reasoning is preferable, as shown by CirC benchmarks. Finally, developing
stronger native automation for finite field reasoning in Lean, including proof sup-
port for existing SMT-based decision procedures, remains crucial, as bitvector
translation alone cannot capture all aspects of finite field semantics.
                              Bibliography


 [1] Alasdair Armstrong, Thomas Bauereiss, Brian Campbell, Alastair Reid,
     Kathryn E Gray, Robert M Norton, Prashanth Mundkur, Mark Wassell,
     Jon French, Christopher Pulte, et al. Isa semantics for armv8-a, risc-v, and
     cheri-mips. Proceedings of the ACM on Programming Languages, 3(POPL):
     1–31, 2019.
 [2] Arasu Arun, Srinath Setty, and Justin Thaler. Jolt: Snarks for virtual
     machines via lookups. In Annual International Conference on the Theory
     and Applications of Cryptographic Techniques, pages 3–33. Springer, 2024.
 [3] Jeremy Avigad, Lior Goldberg, David Levit, Yoav Seginer, and Alon Titel-
     man. A verified algebraic representation of cairo program execution. In
     Proceedings of the 11th ACM SIGPLAN International Conference on Cer-
     tified Programs and Proofs, pages 153–165, 2022.
 [4] Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna
     Lachnitt, Makai Mann, Abdalrhman Mohamed, Mudathir Mohamed, Aina
     Niemetz, Andres Nötzli, Alex Ozdemir, Mathias Preiner, Andrew Reynolds,
     Ying Sheng, Cesare Tinelli, and Yoni Zohar. cvc5: A versatile and industrial-
     strength SMT solver. In TACAS, 2022.
 [5] Haniel Barbosa, Clark Barrett, Byron Cook, Bruno Dutertre, Gereon Kre-
     mer, Hanna Lachnitt, Aina Niemetz, Andres Nötzli, Alex Ozdemir, Math-
     ias Preiner, Andrew Reynolds, Cesare Tinelli, and Yoni Zohar. Gen-
     erating and exploiting automated reasoning proof certificates. Commu-
     nications of the Association for Computing Machinery (CACM), 66(10):
     86–95, October 2023. https://doi.org/10.1145/3587692. URL http:
     //dx.doi.org/10.1145/3587692.
 [6] Clark Barrett and Cesare Tinelli. Satisfiability modulo theories. In Hand-
     book of model checking, pages 305–343. Springer, 2018.
 [7] Carsten Baum, Lennart Braun, Cyprien Delpech de Saint Guilhem, Michael
     Klooß, Christian Majenz, Shibam Mukherjee, Sebastian Ramacher, Chris-
     tian Rechberger, Emmanuela Orsini, Lawrence Roy, et al. Faest: algorithm
     specifications. Technical report, Technical report, National Institute of
     Standards and Technology, 2023.
 [8] Henrik Böving, Siddharth Bhat, Luisa Cicolini, Alex Keizer, Léon Frenot,
     Abdalrhman Mohamed, Léo Stefanesco, Harun Khan, Joshua Clune, Clark
     Barrett, et al. Interactive bitvector reasoning using verified bit-blasting.
     Proceedings of the ACM on Programming Languages, 9(OOPSLA2):3259–
     3285, 2025.
 [9] Stefanos Chaliasos, Imam Al-Fath, and Alastair Donaldson. Towards
     fuzzing zero-knowledge proof circuits (short paper). In Proceedings of the
     34th ACM SIGSOFT International Symposium on Software Testing and
     Analysis, pages 98–104, 2025.
[10] Santiago Cuéllar, Bill Harris, James Parker, Stuart Pernsteiner, and Eran
     Tromer. Cheesecloth:{Zero-Knowledge} proofs of real world vulnerabilities.
22                             E. Pertseva et al.

     In 32nd USENIX Security Symposium (USENIX Security 23), pages 6525–
     6540, 2023.
[11] Santiago Cuéllar Gempeler, Bill Harris, James Parker, Stuart Pernsteiner,
     Ian Sweet, and Eran Tromer. Cheesecloth: Zero-knowledge proofs of real-
     world vulnerabilities. ACM Transactions on Privacy and Security, 28(4):
     1–35, 2025.
[12] Trisha Datta, Binyi Chen, and Dan Boneh. Veritas: Verifying image trans-
     formations at scale. In 2025 IEEE Symposium on Security and Privacy
     (SP), pages 4606–4623. IEEE, 2025.
[13] David Steven Dummit and Richard M Foote. Abstract algebra, volume 3.
     Wiley Hoboken, 2004.
[14] Herbert B Enderton. A mathematical introduction to logic. Elsevier, 2001.
[15] Thomas Hader and Alex Ozdemir. An smt-lib theory of finite fields. 2024.
[16] Timothy Hickey, Qun Ju, and Maarten H Van Emden. Interval arithmetic:
     From principles to implementation. Journal of the ACM (JACM), 48(5):
     1038–1068, 2001.
[17] Daira Hopwood, Sean Bowe, Taylor Hornby, Nathan Wilcox, et al. Zcash
     protocol specification. GitHub: San Francisco, CA, USA, 4(220):32, 2016.
[18] Miguel Isabel, Clara Rodriguez-Nunez, and Albert Rubio. Scalable verifi-
     cation of zero-knowledge protocols. In 2024 IEEE Symposium on Security
     and Privacy (SP), pages 1794–1812. IEEE, 2024.
[19] Carl Kwan, Quang Dao, and Justin Thaler. Verifying jolt zkvm lookup
     semantics. In International Conference on Financial Cryptography and Data
     Security, pages 163–179. Springer, 2025.
[20] Junrui Liu, Ian Kretz, Hanzhi Liu, Bryan Tan, Jonathan Wang, Yi Sun,
     Luke Pearson, Anders Miltner, Işıl Dillig, and Yu Feng. Certifying zero-
     knowledge circuits with refinement types. In 2024 IEEE Symposium on
     Security and Privacy (SP), pages 1741–1759. IEEE, 2024.
[21] The mathlib Community. The lean mathematical library. In Proceedings
     of the 9th ACM SIGPLAN International Conference on Certified Programs
     and Proofs, CPP 2020, page 367–381, New York, NY, USA, 2020. Associa-
     tion for Computing Machinery. ISBN 9781450370974. https://doi.org/
     10.1145/3372885.3373824. URL https://doi.org/10.1145/3372885.
     3373824.
[22] Robert J McEliece. Finite fields for computer scientists and engineers,
     volume 23. Springer Science & Business Media, 2012.
[23] Yizhuo Miao. Secure and privacy-preserving voting system using zero-
     knowledge proofs. Applied and Computational Engineering, 8(1):328–333,
     2023.
[24] Abdalrhman Mohamed, Tomaz Mascarenhas, Harun Khan, Haniel Barbosa,
     Andrew Reynolds, Yicheng Qian, Cesare Tinelli, and Clark Barrett. Lean-
     smt: An smt tactic for discharging proof goals in lean. In International
     Conference on Computer Aided Verification, pages 197–212. Springer, 2025.
[25] Leonardo de Moura and Sebastian Ullrich.            The lean 4 theorem
     prover and programming language. In Automated Deduction – CADE
     28: 28th International Conference on Automated Deduction, Virtual
                 Automating Bitvector and Finite Field Equivalence Proofs in Lean       23

     Event, July 12–15, 2021, Proceedings, page 625–635, Berlin, Heidel-
     berg, 2021. Springer-Verlag. ISBN 978-3-030-79875-8. https://doi.
     org/10.1007/978-3-030-79876-5_37. URL https://doi.org/10.1007/
     978-3-030-79876-5_37.
[26] Greg Nelson and Derek C Oppen. Simplification by cooperating decision
     procedures. ACM Transactions on Programming Languages and Systems
     (TOPLAS), 1(2):245–257, 1979.
[27] Alex Ozdemir, Fraser Brown, and Riad S Wahby. CirC: Compiler infras-
     tructure for proof systems, software verification, and more. In IEEE S&P,
     2022.
[28] Alex Ozdemir, Gereon Kremer, Cesare Tinelli, and Clark Barrett. Satisfia-
     bility modulo finite fields. In CAV, 2023.
[29] Alex Ozdemir, Shankara Pailoor, Alp Bassa, Kostas Ferles, Clark Barrett,
     and Işil Dillig. Split gröbner bases for satisfiability modulo finite fields. In
     CAV, 2024.
[30] Alex Ozdemir, Riad S Wahby, Fraser Brown, and Clark Barrett. Bounded
     verification for finite-field-blasting in a compiler for zero knowledge proofs.
     Formal Methods in System Design, pages 1–28, 2025.
[31] Shankara Pailoor, Yanju Chen, Franklyn Wang, Clara Rodríguez, Jacob
     Van Geffen, Jason Morton, Michael Chu, Brian Gu, Yu Feng, and Işıl Dil-
     lig. Automated detection of under-constrained circuits in zero-knowledge
     proofs. Proceedings of the ACM on Programming Languages, 7(PLDI):1510–
     1532, 2023.
[32] Elizaveta Pertseva, Alex Ozdemir, Shankara Pailoor, Alp Bassa, Sorawee
     Porncharoenwase, Işil Dillig, and Clark Barrett. Integer reasoning modulo
     different constants in smt. In International Conference on Computer Aided
     Verification, pages 339–362. Springer, 2025.
[33] Silvio Ranise, Cesare Tinelli, and Clark Barrett.                          SMT
     fixed size bit-vectors theory.                https://smtlib.cs.uiowa.edu/
     theories-FixedSizeBitVectors.shtml, 2017.
[34] Srinath Setty and Justin Thaler. Twist and shout: Faster memory check-
     ing arguments via one-hot addressing and increments. Cryptology ePrint
     Archive, Paper 2025/105, 2025. URL https://eprint.iacr.org/2025/
     105.
[35] Srinath Setty, Justin Thaler, and Riad Wahby. Unlocking the lookup sin-
     gularity with lasso. In Annual International Conference on the Theory and
     Applications of Cryptographic Techniques, pages 180–209. Springer, 2024.
[36] Ying Sheng, Andres Nötzli, Andrew Reynolds, Yoni Zohar, David Dill,
     Wolfgang Grieskamp, Junkil Park, Shaz Qadeer, Clark Barrett, and Ce-
     sare Tinelli. Reasoning about vectors using an smt theory of sequences.
     In International Joint Conference on Automated Reasoning, pages 125–143.
     Springer International Publishing Cham, 2022.
[37] Jon Stephens, Shankara Pailoor, and Isil Dillig. Automated verification of
     consistency in zero-knowledge proof circuits. In International Conference
     on Computer Aided Verification, pages 315–338. Springer, 2025.
24                              E. Pertseva et al.

[38] Succinct.xyz Blog. Formal verification of sp1 hypercube. https://blog.
     succinct.xyz/nethermind-lean/, 2025. Accessed: 2025-12-07.
[39] Hideaki Takahashi, Jihwan Kim, Suman Jana, and Junfeng Yang. zkfuzz:
     Foundation and framework for effective fuzzing of zero-knowledge circuits.
     arXiv preprint arXiv:2504.11961, 2025.
[40] Ruihan Wang, Carmit Hazay, and Muthuramakrishnan Venkitasubrama-
     niam. Ligetron: Lightweight scalable end-to-end zero-knowledge proofs
     post-quantum zk-snarks on a browser. In 2024 IEEE Symposium on Se-
     curity and Privacy (SP), pages 1760–1776. IEEE, 2024.
[41] Dongwei Xiao, Zhibo Liu, Yiteng Peng, and Shuai Wang. Mtzk: Testing
     and exploring bugs in zero-knowledge (zk) compilers. In NDSS, 2025.
[42] Yoni Zohar, Ahmed Irfan, Makai Mann, Aina Niemetz, Andres Nötzli,
     Mathias Preiner, Andrew Reynolds, Clark Barrett, and Cesare Tinelli. Bit-
     precise reasoning via int-blasting. In International Conference on Verifica-
     tion, Model Checking, and Abstract Interpretation, pages 496–518. Springer,
     2022.


A    Proofs of Termination and Soundness of Translation
Theorem 1. Termination: For any context Γ , no infinite derivation is possible
using strategies to_N and to_BV.

Proof. Since we apply to_N and to_BV only once, it is sufficient to prove that
to_N and to_BV contain no infinite cycles. We will prove this by mapping each
of the rule applications in a while loop to a strictly descending sequence.
1. (Figure 4a lines 3-4: Consider the tuple ordering (number of ΣF -equalities
   in Γ , number of operators inside toNat, number of mod operators, number
   of +FP after −FP in all formulas, number of unbounded variables in Γ )
   sqrBds and injNat decrease the first entry. mvZModSub decreases the second
   to last entry without changing the first three. The next four rules decrease
   the second entry, without changing the first one. The dropMod and mvMod
   decrease the third entry, without changing those before it. Last but not least,
   addBds decreases the last by adding bounds. Since every entry is in this tuple
   is bounded below by 0, we will eventually reach termination.
2. Figure 4b lines 7-8: injBVLeqHyp decreases the number of ΣN hypotheses in
   Γ without a corresponding ΣBV hypothesis.
3. (Figure 4b, lines 10-11) Consider the tuple ordering (number of ΣN -equalities
   in Γ , number of operators inside toNat). injBV decreases the first entry, and
   all subsequent rules decrease the second without adding ΣN -terms.

Theorem 2. Soundness: For any context Γ , the bitvector translation Γ ′ pro-
duced by to_N and to_BV from Γ is valid if and only if Γ ′ is valid.

Proof. A careful analysis of the rules confirms that for each rule, the conclusion
is valid (i.e. H |= G) iff the premise is. For each rewrite rule in to_N and
to_BV, we have a proof of the corresponding lemma stating the equivalence
                Automating Bitvector and Finite Field Equivalence Proofs in Lean     25

of the premise and the conclusion in the Lean theorem prover. These lemmas
either already existed in Lean’s Mathlib [21] or were proven by us as part of our
implementation in Lean (see Section 4.4).

B    Proofs of Termination and Soundness of Range
     Analysis
Theorem 3. Termination: For any context Γ , there is no infinite derivation
from the range analysis calculus.

Proof. Let S be a sequence of rule applications. We will show that any S can
be mapped to a strictly descending sequence in a well-founded order. We do
this by showing how to construct a tuple from a goal state G in such a way
that every rule application reduces the tuple with respect to some well-founded
order. We begin by defining helper functions. Let V(G) denote the number of
occurrences of original variables in all goals in G. Let O(G) denote the number of
natural number arithmetic operators {·N , +N , −N , modN } and ite operators in
all of the goals in G that contain at least one original variable. Let E(G) denote
the number of goals in G with an original variable but without a placeholder
variable. Finally, let |G| denote the number of goals in G. Our tuple ordering
is (V(G), O(G), |G|). We define a total well-founded order <t on such tuples
as the lexicographic order with non-negative standard integer ordering on all
entries. We now show that every rule application decreases the tuple according to
<t . introPVar decreases E(G) by introducing placeholder variables. leqAddMul,
leqSub, leqMod, and leqIf, all decrease O(G) by splitting up and removing
an operator from a goal that contains at least one original variable. They do
this without increasing V(G). ineqHyp, leqZMod, leqBV, and geNat decrease
V(G), as they each remove a goal with at least one original variable from the
proof context. ineqConst decreases |G| by removing a goal. ineqCases decreases
V(G) by substituting constant values for the original variables in a goal. ineqXOR
decreases O(G) by replacing four arithmetic operators with one ite operator.

Theorem 4. Soundness: For any context Γ , if a derivation from Γ reaches a
context where the set of goals is empty, then all goals in Γ hold.

Proof. Each rewrite rule in the range analysis calculus either maintains the log-
ical equivalence of or strengthens the goals in the context. This was verified
by providing “only-if” Lean lemmas for each rule that either existed in Lean’s
Mathlib [21] or were proven in Lean during our implementation (Section 4.4).

C    Strategy Limitations
Applying mvMod prior to dropMod to saturation and then using an overapprox-
imation in clcBVWdth can overinflate bit widths. Consider cubing a variable
x ∈ F7 . Under our current encoding,

          x3 → (toNat(x)3 ) mod 7 → (toBV(9, toNat(x))3 mod (7[9] )           (9)
26                                          E. Pertseva et al.

A more bit-width-aware encoding would keep the mod in the second multipli-
cation and propagate the modulus bit width in clcBVWdth:

       → (((toNat(x)2 ) mod 7) · toNat(x)) mod 7                                               (10)
                                        2
       → ((toBV(6, toNat(x)) mod (7[6] )) · (toBV(6, toNat(x)) mod (7[6] )                     (11)

However, each mod operator requires additional range checks (to decide if either
dropMod or distBVMod applies). Since overflow in the field is rare for our appli-
cation, we consider the speedup gained from minimizing mod operators worth
the tradeoff, even if it results in some bit width inflation.

D      CirC Timeouts
We present the timeouts for CirC SMT benchmark generations below.


Solver                                          Bit width                           All
             0    2    4      6   8 10 12 14 16 18 20 22 24 26 28 30 32
BitModEq 0        0    0      0   0     0   0   0   0   0 0 0 0 0 0 0 0              0
SMT CirC 0        0    0      0   0     4   3   4   1   9 21 18 20 18 18 12 0       130
# Bench. 40 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 78 1318

           Table 7: CirC Statement generation timeouts after 1 minute

  It is worth noting that timeouts are generally concentrated at larger bit widths,
but are absent at bit width 32. Based on our inspection of CirC code, we hy-
pothesize that this occurs because the preprocessing and folding passes are sub-
stantially faster for powers of 2.

E      Benchmark Statistics
We summarize the sizes and complexity of the CirC and Jolt SMT benchmarks
below.


     Benchmarks        Var.  Var. Constr. Constr. Disj. Disj. Ops.                    Chars.
                      (avg) (max) (avg)   (max) (avg) (max) (avg)                     (avg)
     SMT CirC         15.44       198       2.77         5       0.33   26    87     567,64811
     SMT Jolt         67.38       103       128         199        0    0    1013     49,218

     Table 8: Statistics of the CirC and Jolt Lean and SMT benchmark suites.
