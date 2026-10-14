                                             Overapproximation of Non-Linear Integer Arithmetic for
                                                         Smart Contract Verification
                                             Petra Hozzová1 , Jaroslav Bendı́k2 , Alexander Nutz2 , and Yoav Rodeh2
                                                                                       1
                                                                                           TU Wien
                                                                                       2
                                                                                            Certora
arXiv:2402.10174v1 [cs.LO] 15 Feb 2024




                                                                                       Abstract
                                                   The need to solve non-linear arithmetic constraints presents a major obstacle to the
                                               automatic verification of smart contracts. In this case study we focus on the two overap-
                                               proximation techniques used by the industry verification tool Certora Prover: overapproxi-
                                               mation of non-linear integer arithmetic using linear integer arithmetic and using non-linear
                                               real arithmetic. We compare the performance of contemporary SMT solvers on verifica-
                                               tion conditions produced by the Certora Prover using these two approximations against
                                               the natural non-linear integer arithmetic encoding. Our evaluation shows that the use of
                                               the overapproximation methods leads to solving a significant number of new problems.


                                         1    Introduction
                                         Smart contracts [19] are an ideal target for automated program verification in many ways: Their
                                         source code is often relatively small. Due to high execution costs (also known as gas consump-
                                         tion), they contain few loops or recursive methods. Finally, since the underlying applications
                                         are often financial in nature, there is a large incentive to detect bugs early, and hacks that lead
                                         to a loss of money in the tens of millions of US dollars are not rare. However, a major pain
                                         point is that the verification conditions of smart contracts often contain non-linear arithmetic,
                                         which makes them undecidable in general and sometimes intractable in practice.
                                             In this case study, we evaluate two methods to prove verification conditions stemming from
                                         smart contract verification that were previously intractable due to their use of non-linear integer
                                         arithmetic (NIA). The methods are based on the observation that the integer inequalities that
                                         occur in the smart contract verification conditions can often be effectively reasoned about at
                                         lower precision than the one demanded by the standard NIA semantics, thus allowing for a
                                         precision-complexity trade-off. We evaluate two techniques to overapproximate a NIA formula,
                                         one using linear integer arithmetic (LIA) and one using nonlinear real arithmetic (NRA).
                                             The motivation leading to this case study was to augment the portfolio of methods that the
                                         Certora Prover, a leading industrial tool for automatic verification of smart contracts, uses for
                                         verifying properties of Ethereum [20] smart contracts containing NIA. To verify a smart contract
                                         property, the Certora Prover builds a logical formula, called a verification condition (VC), such
                                         that the VC is satisfiable iff the specification can be violated by the contract. Moreover, every
                                         model of the VC corresponds to a particular counter-example, i.e., an execution of the smart
                                         contract violating the specification. To check the VC satisfiability, the Certora Prover converts
                                         the VC to an SMT formula and passes it to an SMT solver, such as cvc5 [1] or Z3 [11].
                                             The smart contract VC is encoded in a fragment of first-order logic with theories, uninter-
                                         preted sorts, and uninterpreted function symbols. Depending on the smart contract, specifi-
                                         cation, and tool configuration, the VC may contain quantifiers, datatypes, LIA or NIA, and
                                         bitwise operations. This study focuses on the cases with quantifier-free VC using NIA. Since
                                         satisfiability of formulas with NIA is undecidable [18] it is not too surprising that SMT solvers
Overapproximation of NIA for Smart Contract Verification                                       Hozzová et al.


often struggle with proving such VCs. Our evaluation shows this difficulty, as well as a signifi-
cant number of benchmarks being newly solved using the two overapproximation techniques.
    The idea to overapproximate the underlying non-linearity was developed in the Certora
Prover already from its conception with a simple LIA overapproximation, which was then grad-
ually refined by adding axioms specialized for the domain of smart contracts. Motivated by
empirical success of the LIA-based method, we recently implemented another overapproxima-
tion based on NRA. Both methods are designed for proving the VC unsatisfiability, not finding
counter-examples: overapproximation unsatisfiability implies unsatisfiability of the original VC,
but not vice versa. Interestingly, contemporary SMT solvers also internally apply various over-
approximation techniques while solving NIA instances [8, 16, 17]. As our results show, these
techniques seem to be largely complementary to the overapproximations we investigate in this
paper.

Contributions. The main focus of this paper is on experimental evaluation of two SMT-
based overapproximation techniques for smart contract verification, employed by the Certora
Prover. Namely, we compare the performance of contemporary SMT solvers on the natural NIA
encoding against the LIA and NRA overapproximations. Using the two overapproximations,
we are able to verify 39% new examples in our benchmark suite, which could not be verified
using the NIA encoding. These benchmarks are real-world benchmarks: they stem from actual
customer contracts that were under verification by Certora, and are made available online.
Secondary contributions of this paper are (brief) descriptions of the LIA and NRA encodings.

Outline. Section 2 lays out the preliminaries and introduces an illustrative example. Sec-
tion 3 presents the overapproximation methods and demonstrates one of them on our example.
Section 4 reports on the experiment setup and results. Section 5 briefly reviews related work.


2     Preliminaries and Example
We assume familiarity with standard first-order logic with equality and the theories of integer
and real arithmetic (for details see [4, 14]). We use the theories of linear integer arithmetic,
and non-linear arithmetic for integers and reals in accordance with SMT-LIB definitions [3],
denoted by LIA, NIA and NRA, respectively. These theories define the predicates less, less
equal, greater, greater equal, and the functions of addition, subtraction, (only NIA and NRA)
multiplication, division, (only NIA) absolute value1 , modulo. We respectively denote these
predicate and function symbols for integers by <I , ≤I , >I , ≥I , +I , −I , ∗I , divI , absI , modI and for
reals by <R , ≤R , >R , ≥R , +R , −R , ∗R , /R . We use −I and −R to denote both the unary and binary
minus. Further, we use the same symbols 0, 1, −1, . . . for both integer and real constants.
    In this paper we work with the quantifier-free fragment of first-order logic, denoted by the
prefix “QF ”. Free variables are implicitly assumed to be existentially quantified, hence the
(SMT) variables correspond to first-order constants. We denote the SMT variables by a, b;
first-order variables by x, y, z, w; terms by t, s, u, v; formulas by f ; all possibly with indices. We
use t <I u ≤I v as an abbreviation for t <I u ∧ u ≤I v, and similarly with other comparison
predicate symbols. We use the standard notions of position in a formula and of (sub)formula
polarity. We denote the position in a formula by a sequence of positive integers. We write ϵ

    1 In SMT-LIB, only NIA defines the absolute value function. However, since abs does not occur in the VCs
                                                                                  I
produced by the Certora Prover, and since its counterpart for LIA and NRA could be straightforwardly defined
as abs(x) = if x > 0 then x else − x, we do not consider it in the overapproximations described in this paper.


2
Overapproximation of NIA for Smart Contract Verification                                       Hozzová et al.


for the empty sequence denoting the top-most position in a formula. When f ′ is a subformula
of a formula f at position π, where the top-level logical connective of f ′ is n-ary, then the
subformula of f at position π.i for any i ∈ {1, . . . , n} is the ith argument of f ′ . We denote the
                                                                                                       def
polarity of a (sub)formula of f at position π by pf (π). Let f be a formula and let pf (ϵ) = 1.
Then, for each (sub)formula f ′ at position π of f : If f ′ has the form f1 ∧ · · · ∧ fn or f1 ∨ · · · ∨ fn ,
then ∀i ∈ {1, . . . , n} : pf (π.i) = pf (π). If f ′ has the form ¬f1 , then pf (π.1) = −pf (π). If f ′ has
the form f1 → f2 , then pf (π.1) = −pf (π) and pf (π.2) = p(π). If f ′ has the form f1 ↔ f2 , then
pf (π.1) = pf (π.2) = 0. We say that the (sub)formula of f at position π has positive polarity if
pf (π) = 1 and negative polarity if pf (π) = −1.
    We use the model domains of integers Z and real numbers R, and we consider Z ⊂ R, i.e.,
we consider e.g. 1 and 1.0 to denote the same number. We use m, n to denote numbers from
either Z or R. The theory predicate and function symbols are interpreted in the standard way,
and we denote their interpretations by <, ≤, >, ≥, +, −, ∗, div, abs, mod, /, respectively.2
Example 1. We illustrate the verification problem by a simplified Ethereum smart contract
verification example. Assume assets in the form of shares and money. We model all the smart
contract and specification variables, typically of type uint256, as non-negative integer variables.
     Let there be a total supply of tS shares, altogether having the total monetary value of tM ,
where tS ̸= 0 and tM ̸= 0. If we withdrew wS shares, these shares would be sold and we would
obtain the monetary value wM = (wS ∗ tM ) div tS . Note that div is the integer division: since
the smart contract works with uint256s, we might get a little less money for the shares than
the real value that they have. Now, assume that nS new shares are added to the total supply
tS , having the same per-share value as the old shares (with precision up to the precision of
div). We obtain new total supply of shares t′S = tS + nS and the new total monetary value
t′M = tM + ((nS ∗ tM ) div tS ). If we now withdrew the same number wS of shares from the new
                                                       ′
total supply, we would obtain the monetary value wM       = (wS ∗ t′M ) div t′S . Given this scenario,
we would like to prove the following property: the monetary value from the original withdrawal
                                                                                          ′
is greater or equal to the monetary value from the second withdrawal, i.e., wM ≥ wM          .
     We encode this example in QF NIA. We construct the verification condition for the example
as a conjunction of all the assumptions and a negation of the conjecture:
        tS >I 0 ∧ tM >I 0 ∧ wS ≥I 0 ∧ wM ≥I 0 ∧ nS ≥I 0 ∧ t′S ≥I 0 ∧ t′M ≥I 0 ∧ wM
                                                                                 ′
                                                                                   ≥I 0
        ∧ wM = (wS ∗I tM ) divI tS ∧ t′S = tS +I nS ∧ t′M = tM +I ((nS ∗I tM ) divI tS )                  (1)
                               ′
                            ∧ wM = (wS ∗I t′M ) divI t′S ∧ ¬(wM ≥I wM
                                                                    ′
                                                                      )
   If the formula (1) is unsatisfiable, the property holds. If (1) is satisfiable, its model consti-
tutes a counterexample to the property. In this case, the formula (1) is indeed unsatisfiable (it
has no integer model), as will be later confirmed using the NRA overapproximation. However,
none of the SMT solvers we considered3 can prove the unsatisfiability of its NIA encoding within
a 5-minute time limit. The SMT-LIB2 encoding of formula (1) is displayed in Appendix A.1.
Further, the smart contract verification problem this example is based on is also displayed in
Appendix A.3.
   The Certora Prover uses formulas similar in character to (1), and encodes them in the
SMT-LIB2 [3] format. Wraparound semantics for uint256s are modelled by computing all
operations that potentially under- or overflow modulo 2256 . In addition to NIA, the Certora
Prover also utilizes uninterpreted function symbols (UF) and the theory of datatypes (DT),
resulting in the logic QF UFDTNIA.
   2 For positive m, n div m is defined as ⌊n/m⌋, for negative m as ⌈n/m⌉.
   3 cvc5 v1.0.2 [1], MathSAT v5.6.8 [9], Yices2 v2.6.4 [12], and Z3 v4.11.0 [11]



                                                                                                             3
Overapproximation of NIA for Smart Contract Verification                                       Hozzová et al.


3     Overapproximation Methods
In this section, we describe the techniques for constructing the LIA and NRA overapproxima-
tions fLI , fNR of the formula fNI using QF NIA (and possibly other theories). Formula f is an
overapproximation of fNI , if from unsatisfiability of f follows that fNI is also unsatisfiable. We
say that f2 is a tighter overapproximation of fNI than f1 if both f1 , f2 are overapproximations
of fNI , and the set of models of f1 is a superset of models of f2 . There is a trade-off between
the overapproximation tightness and the practical complexity. The overapproximation f could
precisely capture fNI – but that would essentially force the solvers proving f to reason with
NIA instead of LIA or NRA. Rather, we construct formulas fLI , fNR which can be solved using
LIA, NRA, respectively, yet are typically unsatisfiable if fNI was unsatisfiable. To construct an
overapproximation of fNI , we rewrite the original formula. We denote rewriting of the term t
to the term s, i.e., replacing all occurrences of t in a given formula by s, by t ⇝ s.

3.1     Linear Integer Arithmetic Overapproximation
The LIA-based overapproximation proceeds in two steps. First, it replaces nonlinear operations
in fNI by replacing the NIA function symbols by uninterpreted function symbols as follows:

         t ∗I s ⇝ umul(t, s)            t divI s ⇝ udiv(t, s)             t modI s ⇝ umod(t, s)

The resulting formula f1 is a very coarse overapproximation of fNI .
     Second, to tighten the overapproximation, the transformation adds axioms constraining
umul, udiv, umod to the formula. To retain the overapproximation property, the axioms must
correspond to valid properties of integer arithmetic – e.g., an axiom regarding umul must only
state valid properties of ∗I . We do not add quantified axioms, but rather we instantiate axioms
with selected terms occurring in f1 . Due to space limitations we do not explicitly list all axioms,
nor the instantiation strategy. We rather list the axiomatized properties: (i) arithmetic axioms:
commutativity, neutral and absorbing element with respect to umul, udiv and umod, ranges of
udiv and umod results; (ii) relating umul to the linear multiplication ∗I if one operand is an
interpreted constant; (iii) overflow-related: multiplicative inverse property only holding if the
multiplication did not overflow modulo 2256 ;4 (iv) twos-complement related: certain standard
identities regarding twos-complement multiplications in a modular ring; (v) relating pairs of
multiplications: monotonicity and distributivity.
     These axioms are instantiatiated over single applications of the operators, as well as pairs
of multiplications that lie on a common program path. They are not instantiated recursively,
i.e., if an axiom produces a new multiplication, we don’t generate an axiom for that.
     Adding the axioms to f1 results in a formula fLI as a ground formula using the theories UF
and LIA in addition to any theories that fNI used except for NIA. E.g., if fNI is in QF DTNIA,
fLI will be in QF UFDTLIA.

3.2     Non-Linear Real Arithmetic Overapproximation
We construct the NRA overapproximation fNR of fNI in three steps. The first two steps
are similar to the LIA overapproximation: we replace the function symbols and add axioms.
Then we tighten the overapproximation by rewriting selected inequalities. Similarly to fLI , the


    4 The formula f                                                 256 (because 2256 − 1 is the maximal value
                    NI usually contains many occurrences of t modI 2
of the integer type uint256), and might also contain 0 ≤I t and t <I 2256 as the encoding of overflow checks.


4
Overapproximation of NIA for Smart Contract Verification                                Hozzová et al.


formula fNR is ground and uses UF and NRA in addition to any theories that fNI used except
for NIA.
    In contrast to the LIA overapproximation, NRA overapproximation uses the real sort.
Hence, we change the sorts of all variables and functions from integers to reals. We replace all in-
terpreted integer constants by their real counterparts, and the symbols +I , −I , ∗I by +R , −R , ∗R .
We replace NIA function symbols divI , modI , which do not correspond to any interpreted func-
tion in NRA, using freshly added function symbols ufrac, umod, obtaining formula f1 :
                t divI s ⇝ t/R s −R ufrac(t, s)                 t modI s ⇝ umod(t, s)
Intuitively, we subtract ufrac(t, s) from t/R s to make sure that any integer model of t divI s
will also be a model of its real translation.
    Next we axiomatize the new function symbols. We provide a definition for the function umod,
two axioms partially constraining ufrac, and an axiom constraining all the real variables:
                                        
                                         x              if 0 ≤R x <R y
                                        
                                          x −R y         if y ≤R x <R 2 ∗R y
                                        
                                    def
                        umod(x, y) =                                                        (2)
                                          x+ y           if −R y ≤R x <R 0
                                         R
                                        
                                        
                                            y ∗R ufrac(x, y)   else
                                      def
              ax frac bound(x, y) = (y >R 0 → 0 ≤R ufrac(x, y) <R 1) ∧
                                                                                                   (3)
                                             (y <R 0 → 0 ≥R ufrac(x, y) >R −1)
                                      def
          ax frac zero(x, y, z, w) = (x = z∗R w ∧ (y = z ∨ y = w)) → ufrac(x, y) = 0               (4)
                                      def
                 ax int approx(x) = x ≤R −1 ∨ x = 0 ∨ x ≥R 1                                       (5)
The definition (2) is tailored to the occurrences of modI in fNI produced by the Certora Prover,
as described in Footnote 4. Axioms (3), (4) constrain ufrac(x, y) to be between 0 and 1 (or 0
and −1 for negative y), and to be 0 when y is known to be a divisor of x. We instantiate them by
selected terms occurring as arguments of /R , umod and ∗R in f1 . Finally, we add an instance of (5)
for each real variable in f1 , to ensure that for all non-zero values n, m both abs(n ∗ m) ≥ abs(n)
and abs(n ∗ m) ≥ abs(m) hold, and for all n and non-zero m also abs(n/m) ≤ abs(n) holds, as
it would for integer n, m. We obtain the formula f2 from f1 by adding the definitions (2)-(5),
and instances of axioms (3)-(5) as described above. Intuitively, f2 is an overapproximation of
fNI , because any model of fNI can be extended to a model of f2 by interpreting ufrac(n, m) as
n/m − (n div m) for integers n, m. The instances of axioms (3)-(5) hold in this model, because
they are only instantiated for terms from f1 , which are in the considered model interpreted by
integer values.
    The third step of the NRA overapproximation method is based on the following observation:
If we want to prove the conjecture a ≤I b in NIA, we can do it by proving a −R 1 <R b in NRA.
From the proof-by-refutation point of view, ¬(a−R 1 <R b) is an overapproximation of ¬(a ≤I b).
Thus, to tighten the overapproximation f2 of fNI , we relax some of the inequalities in f1 (not
the inequalities in the axiom and function definitions (2)-(5)). We first replace each inequality
t <R s or t >R s occurring in the f1 part of f2 with positive polarity by an equivalent inequality
adding one more negation to obtain an inequality using ≥R or ≤R with negative polarity:
                          t <R s ⇝ ¬(t ≥R s)               t >R s ⇝ ¬(t ≤R s)
Then we relax each inequality t ≤R s and t ≥R s occurring in the f1 part of f2 with negative
polarity, obtaining the formula fNR :
                       t ≤R s ⇝ t −R 1 <R s                t ≥R s ⇝ t +R 1 >R s

                                                                                                     5
Overapproximation of NIA for Smart Contract Verification                                             Hozzová et al.


Example 2. Using the method of this subsection on the formula (1) from Example 1, we obtain
the formula consisting of the axiom definitions (3)-(5) (since (1) does not use umod, we omit
the definition (2)) and the following:
    ¬(tS −R 1 <R 0) ∧ ¬(tM −R 1 <R 0) ∧ wS ≥R 0 ∧ wM ≥I 0 ∧ nS ≥R 0 ∧ t′S ≥R 0 ∧ t′M ≥R 0 ∧ wM
                                                                                             ′
                                                                                               ≥R 0
    ∧ wM = (wS ∗R tM )/R tS −R ufrac(wS ∗R tM , tS ) ∧ t′M = tM +R ((nS ∗R tM )/R tS −R ufrac(nS ∗R tM , tS ))
        ∧ t′S = tS +R nS ∧ wM
                            ′
                              = (wS ∗R t′M )/R t′S −R ufrac(wS ∗R t′M , t′S ) ∧ ¬(wM +R 1 >R wM
                                                                                              ′
                                                                                                )
∧ax frac bound(wS ∗R tM , tS )∧ax frac zero(wS ∗R tM , tS , wS , tM )∧ax frac zero(wS ∗R tM , tS , nS , tM )
∧ax frac zero(wS ∗R tM , tS , wS , t′M )∧ax frac bound(nS ∗R tM , tS )∧ax frac zero(nS ∗R tM , tS , wS , tM )
∧ax frac zero(nS ∗R tM , tS , nS , tM )∧ax frac zero(nS ∗R tM , tS , wS , t′M )∧ax frac bound(wS ∗R t′M , t′S )
      ∧ ax frac zero(wS ∗R t′M , t′S , wS , tM ) ∧ ax frac zero(wS ∗R t′M , t′S , nS , tM ) ∧ ax int approx(tS )
 ∧ax frac zero(wS ∗R t′M , t′S , wS , t′M )∧ax int approx(tM )∧ax int approx(wS )∧ax int approx(wM )
            ∧ax int approx(nS )∧ax int approx(t′S )∧ax int approx(t′M )∧ax int approx(wM
                                                                                       ′
                                                                                         )

When encoded in the SMT-LIB2 syntax, this formula is proved unsatisfiable by the SMT solvers
Yices2 and cvc5. Its SMT-LIB2 encoding is displayed in Appendix A.2.


4       Experimental Evaluation
Experimental setup. Our experimental setup mirrors the setup used by the Certora Prover.
We considered the NIA encoding of 792 verification problems stemming from customer contracts
that were under verification by Certora, and compared the performance of four SMT solvers on
these benchmarks against overapproximated versions of the benchmark set.
    The LIA overapproximation method was implemented directly in the Certora Prover. The
Certora Prover hence produces both the natural NIA encoding of the problems and their LIA
overapproximations. In order to prototype the NRA overapproximation, we implemented the
method as a formula-to-formula transformation in Python using the tokenizer of PySMT [15].
The formulas produced by the Certora Prover and our artifact are in SMT-LIB2 format [4].
All benchmarks are available at https://github.com/Certora/PublicBenchmarks/tree/master/
Sep2022. The artifact for NRA overapproximation is available at https://github.com/hzzv/
scripts/tree/main/real relaxation.
    The 792 benchmarks originate from two different encodings of 396 problems: one encoding in
QF UFNIA, one in QF UFDTNIA. The encodings differ in how they model hash functions used
by smart contracts for memory addressing. The QF UFNIA encoding represents the hash func-
tions using uninterpreted functions while the QF UFDTNIA encoding uses inductive datatypes.
Since the hash functions are only used for memory layout, the hash function representation
mostly does not interact with non-linear arithmetic. Thus, there is in general no interplay of
datatypes and NIA in the QF UFDTNIA benchmark set. Out of both benchmark sets, we
excluded 300 benchmarks found to be satisfiable in QF UFNIA or QF UFDTNIA during our
experiments, resulting in 246 benchmarks in each set. For these benchmarks we generated the
overapproximation sets QF UFLIA, QF UFDTLIA, and QF UFNRA, QF UFDTNRA. In the
sequel we refer to the sets QF UFNIA, QF UFLIA, QF UFNRA together as QF UF+, and to
the sets QF UFDTNIA, QF UFDTLIA, QF UFDTNRA together as QF UFDT+.
    We compared the performance of cvc5 v1.0.2 [1], MathSAT v5.6.8 [9], Yices2 v2.6.4 [12],
and Z3 v4.11.0 [11] on the original and the overapproximated benchmarks. These are all the
non-portfolio and non-wrapper SMT solvers that competed in SMT-COMP 2022 [2] in the
single query track of division QF NonLinearIntArith. We ran all the experiments on comput-
ers with 32 cores (AMD Epyc 7502, 2.5 GHz) and 1 TB RAM using the benchmarking tool

6
Overapproximation of NIA for Smart Contract Verification                              Hozzová et al.


         QF UF+        NIA     LIA (new)     NRA (new)
              cvc5      8        7 (7)       13 (13)
        MathSAT        10        1 (1)       40 (31)
           Yices2       0        7 (7)       34 (34)
                Z3     47        25 (9)        20 (7)
virtual best solver    52       34 (11)       42 (14)
      QF UFDT+         NIA     LIA (new)     NRA (new)
              cvc5      9        8 (6)       43 (39)
                Z3     55       49 (19)       25 (13)
virtual best solver    57       52 (19)       47 (16)


Figure 1: Numbers of solved problems in the respec-
tive benchmark sets. Columns “LIA” and “NRA”
refer to the benchmark overapproximations. In the
parentheses is the number of problems solved in the        Figure 2: Comparison of the runtimes
respective overapproximated benchmark set, but             on original and overapproximated bench-
not in the original NIA benchmark set. The “vir-           mark sets. We compare runtimes for the
tual best solver” row corresponds to the best result       virtual best solver – for each problem
for each benchmark – i.e., the numbers in this row         we consider the best runtime achieved by
are the counts of benchmarks solved by any solver.         any of the four solvers.


BenchExec [5]. We used the time limit of 300 seconds and the memory limit of 16 GB per
problem, corresponding to the time limits used in practice by the Certora Prover.

Experimental results. From the 492 benchmarks, 482 use integer division and 490 use mod-
ulo. Multiplication is used on average 83 times per problem, division 37 times per problem,
and modulo 47 times per problem. Both overapproximations therefore added many instances
of axioms related to multiplication, division and modulo. Further, since the Certora Prover
internally converts the smart contracts to a static-single-assignment form and hence introduces
many auxiliary variables (the average number of variables in a problem is 1361), the NRA
overapproximation also added many instances of the axiom (5). Consequently, the LIA and
NRA benchmarks were on average 70% and 243% larger in file size, respectively, than the orig-
inal benchmarks. We note that even though instantiating the axioms increases the benchmark
size significantly, in our experience it leads to better solver performance than using quantified
axioms instead.
    We say that a benchmark was solved to convey that it was proved unsatisfiable. The main
goal of using the overapproximations is to verify smart contracts that were not verified in the
NIA encoding. The key metric is therefore the number of newly solved problems, i.e., problems
solved in an overapproximation but not solved in the NIA encoding, no matter which solver
solves them. Hence in the result analysis, we use the concept of a virtual best solver (VBS) –
a hypothetical solver which solves each problem as fast as the fastest solver we ran. E.g., if we
have two benchmarks, one benchmark solved by cvc5 in 1 second and by Z3 in 2 seconds, and
another benchmark solved only by Z3 in 1 second, then the VBS is considered to have solved
both benchmarks with the runtime of 1 second for each of them.
    We ran all four SMT solvers on the benchmarks in QF UF+, but since MathSAT and
Yices2 do not support datatypes, only the solvers cvc5 and Z3 on the benchmarks in
QF UFDT+. The results are displayed in Figure 1. Both the LIA and NIA overapproximations

                                                                                                   7
Overapproximation of NIA for Smart Contract Verification                                         Hozzová et al.


led to 30 newly solved benchmarks compared to the original benchmark set (28% increase). If
we combined the results for both overapproximations, the VBS solved 50 and 59 benchmarks
in at least one of the overapproximations originating from QF UFNIA and QF UFDTNIA, re-
spectively. 19 and 23 benchmarks were newly solved in at least one of the overapproximations
of QF UFNIA and QF UFDTNIA, respectively, corresponding to a 39% increase in the number
of smart contracts we were able to verify compared to the NIA encoding.
    Interestingly, the NRA overapproximation significantly increased the number of solved
benchmarks for all solvers except for Z3. A large majority of these benchmarks were newly
solved, suggesting that the techniques used by the solvers for NIA are orthogonal to our NRA
overapproximation, and that the solvers might potentially benefit from using a similar method.
    Figure 2 displays a comparison of the runtimes for the VBS for all the problems in the
original and the two overapproximated benchmark sets. We used the actual best runtime for
problems solved as unsatisfiable, but for problems with only non-unsatisfiable results we set the
runtime to 300 seconds to convey that none of the solvers was able to solve the problem in the
given time limit. There were 56 problems solved as unsatisfiable in both the original and the LIA
overapproximated set, and 59 such problems for the original and the NRA overapproximated
set. 40 problems were solved faster in the original set compared to LIA overapproximations,
and 35 faster in the original set compared to NRA overapproximations.

Measuring the Overapproximation Tightness. In order to measure how tight are both
overapproximations, we look at the numbers of problems solved as unsatisfiable in the original
set, but either solved as satisfiable or not solved at all in the overapproximated set. Out of the
109 originally unsatisfiable problems, in the LIA overapproximation no problems were solved
as satisfiable, while 53 were not solved at all. In the NRA overapproximation, 24 originally
unsatisfiable problems were solved as satisfiable and 26 were not solved at all. We thus conclude
that the LIA overapproximation is quite tight and is unlikely to benefit from adding more
axioms. On the other hand, the NRA overapproximation could be tightened.5

Applications in Other Domains. We also tried running our NRA overapproximation tool
on the QF NIA and QF UFNIA sets of the SMT-LIB benchmark library [3]. However, the
QF NIA set only contains a small number of problems using either division or modulo, and the
QF UFNIA set only contains non-linear operations in function definitions, for which the method
does not add any axiom instances. Hence, it is not surprising that the SMT solvers were in gen-
eral less successful on the overapproximated benchmarks compared to the original benchmarks.
The only notable exception was the performance of Yices on the QF NIA benchmarks, where
out of 10343 total problems it solved 5243 in the original set, but 5992 benchmarks in the over-
approximated set. Therefore, we conclude that for successful application of overapproximation
methods, it is crucial to fine-tune the methods for the specific domain.


5     Related Work
Contemporary SMT solvers implement a range of methods for reasoning with QF NIA, such
as bit-blasting [13] (AProVe [13], cvc5 [1], Z3 [11], and SMT-RAT [10]), linearization [7]
(Barcelogic [6]), incremental linearization [8] (MathSAT [9], cvc5, and Z3), and NRA over-
approximation combined with branch-and-bound [16, 17] (SMT-RAT, Z3, and Yices2 [12]).
   5 We tried using a modification of the axiom (3) bounding ufrac(x, y) to be at most 1 − 1/ y for y > 0
                                                                                           R    R           R
and at least −1 −R 1/R y for y <R 0. However, compared to (3), this tightening did not increase the number of
newly solved problems, nor decrease the number of originally unsatisfiable problems being solved as satisfiable.


8
Overapproximation of NIA for Smart Contract Verification                                  Hozzová et al.


    The overapproximations we evaluate in this case study are similar in spirit to that of [8,16,17]
(not [7], since that is geared towards finding models, while the overapproximations we focused on
aim for preservation of unsatisfiability). However, all these approaches use iterative refinements
of the overapproximation, while the overapproximation methods we compared work on top of
SMT solvers: they only create one overapproximation and pass it to a solver supporting LIA
or NRA. Further, the overapproximation methods we focused on are specialized for the domain
of smart contract verification (e.g., using a specialized definition of umod).


6     Conclusions
In this case study we focused on overapproximation methods for verification of smart contracts
using NIA. We described and evaluated two overapproximation methods using LIA and NRA.
Our results show that both methods lead to solving a large number of industry benchmarks
that were not solved in their natural NIA encoding, emphasizing the benefit of domain-specific
verification methods. Further, our evaluation indicates that the NRA overapproximation can
be further refined. Finally, our results also suggest that the NRA overapproximation method
could be combined with existing methods for real overapproximation used by SMT solvers.

Acknowledgements. We thank Ján Hozza, Laura Kovács, and Gereon Kremer for fruitful
discussions. We also thank Shelly Grossman, Jochen Hoenicke, and Mooly Sagiv. This work was
partially funded by the ERC CoG ARTIST 101002685, and the FWF grants LogiCS W1255-N23
and LOCOTES P 35787.


References
 [1] Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mohamed, A.,
     Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M., Reynolds, A., Sheng, Y., Tinelli,
     C., Zohar, Y.: cvc5: A versatile and industrial-strength SMT solver. In: Fisman, D., Rosu, G.
     (eds.) Tools and Algorithms for the Construction and Analysis of Systems - 28th International
     Conference, TACAS 2022, Held as Part of the European Joint Conferences on Theory and Practice
     of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part I. Lecture Notes
     in Computer Science, vol. 13243, pp. 415–442. Springer (2022). https://doi.org/10.1007/978-3-
     030-99524-9 24, https://doi.org/10.1007/978-3-030-99524-9 24
 [2] Barbosa, H., Bobot, F., Hoenicke, J.: 17th International Satisfiability Modulo Theories Competi-
     tion (SMT-COMP 2022). https://smt-comp.github.io/2022/ (2022)
 [3] Barrett, C., Fontaine, P., Tinelli, C.: The Satisfiability Modulo Theories Library (SMT-LIB).
     www.SMT-LIB.org (2016)
 [4] Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB Standard Version 2.6. Tech. rep. (2021)
 [5] Beyer, D., Löwe, S., Wendler, P.: Reliable benchmarking: requirements and solutions. Interna-
     tional Journal on Software Tools for Technology Transfer 21(1), 1–29 (2019)
 [6] Bofill, M., Nieuwenhuis, R., Oliveras, A., Rodrı́guez-Carbonell, E., Rubio, A.: The barcelogic
     SMT solver. In: International Conference on Computer Aided Verification. pp. 294–298. Springer
     (2008)
 [7] Borralleras, C., Lucas, S., Oliveras, A., Rodrı́guez-Carbonell, E., Rubio, A.: SAT modulo linear
     arithmetic for solving polynomial constraints. Journal of Automated Reasoning 48(1), 107–131
     (2012)
 [8] Cimatti, A., Griggio, A., Irfan, A., Roveri, M., Sebastiani, R.: Experimenting on solving nonlinear
     integer arithmetic with incremental linearization. In: Beyersdorff, O., Wintersteiger, C.M. (eds.)

                                                                                                       9
Overapproximation of NIA for Smart Contract Verification                                Hozzová et al.


     Theory and Applications of Satisfiability Testing – SAT 2018. pp. 383–398. Springer International
     Publishing, Cham (2018)
 [9] Cimatti, A., Griggio, A., Schaafsma, B., Sebastiani, R.: The MathSAT5 SMT Solver. In: Piterman,
     N., Smolka, S. (eds.) Proceedings of TACAS. LNCS, vol. 7795. Springer (2013)
[10] Corzilius, F., Kremer, G., Junges, S., Schupp, S., Ábrahám, E.: SMT-RAT: an open source
     C++ toolbox for strategic and parallel SMT solving. In: International Conference on Theory and
     Applications of Satisfiability Testing. pp. 360–368. Springer (2015)
[11] De Moura, L., Bjørner, N.: Z3: An Efficient SMT Solver. In: Ramakrishnan, C.R., Rehof, J. (eds.)
     Proc. of TACAS. LNCS, vol. 4963, pp. 337–340. Springer (2008). https://doi.org/10.1007/978-3-
     540-78800-3 24
[12] Dutertre, B.: Yices 2.2. In: Biere, A., Bloem, R. (eds.) Computer-Aided Verification (CAV’2014).
     Lecture Notes in Computer Science, vol. 8559, pp. 737–744. Springer (July 2014)
[13] Fuhs, C., Giesl, J., Middeldorp, A., Schneider-Kamp, P., Thiemann, R., Zankl, H.: SAT solving
     for termination analysis with polynomial interpretations. In: Marques-Silva, J., Sakallah, K.A.
     (eds.) Theory and Applications of Satisfiability Testing – SAT 2007. pp. 340–354. Springer Berlin
     Heidelberg, Berlin, Heidelberg (2007)
[14] Gallier, J.H.: Logic for computer science: foundations of automatic theorem proving. Courier
     Dover Publications (2015)
[15] Gario, M., Micheli, A.: PySMT: a solver-agnostic library for fast prototyping of SMT-based
     algorithms. In: SMT Workshop 2015 (2015)
[16] Jovanović, D.: Solving nonlinear integer arithmetic with MCSAT. In: International Conference on
     Verification, Model Checking, and Abstract Interpretation. pp. 330–346. Springer (2017)
[17] Kremer, G., Corzilius, F., Ábrahám, E.: A generalised branch-and-bound approach and its ap-
     plication in SAT modulo nonlinear integer arithmetic. In: International Workshop on Computer
     Algebra in Scientific Computing. pp. 315–335. Springer (2016)
[18] Matiyasevich, Y.V.: Hilbert’s Tenth Problem. MIT Press, Cambridge, MA, USA (1993)
[19] Szabo, N.: Smart contracts (1994)
[20] Wood, G., et al.: Ethereum: A secure decentralised generalised transaction ledger. Ethereum
     project yellow paper 151(2014), 1–32 (2014)




10
Overapproximation of NIA for Smart Contract Verification                              Hozzová et al.


A      Appendix
A.1     SMT-LIB Encoding of Example 1
To encode our running example into SMT-LIB2, we rename the variables tS , t′S , tM , t′M , wM , wM
                                                                                                 ′
                                                                                                   ,
nS , wS to ts1, ts2, tm1, tm2, wm1, wm2, ns, ws, respectively.
    The encoding of the formula (1) from Example 1:

( set - logic QF_NIA )                                     ( >=   wm1 0)
                                                           ( >=   ns 0)
( declare - const   ts1 Int )                              ( >=   ts2 0)
( declare - const   ts2 Int )                              ( >=   tm2 0)
( declare - const   tm1 Int )                              ( >=   wm2 0)
( declare - const   tm2 Int )                         ))
( declare - const   wm1 Int )
( declare - const   wm2 Int )                        ( assert (= wm1 ( div (* ws tm1 ) ts1 )))
( declare - const   ns Int )                         ( assert (= ts2 (+ ts1 ns )))
( declare - const   ws Int )                         ( assert
                                                        (= tm2 (+ tm1 ( div (* ns tm1 ) ts1 ))))
( assert ( and                                       ( assert (= wm2 ( div (* ws tm2 ) ts2 )))
   ( > ts1 0)                                        ( assert ( not ( >= wm1 wm2 )))
   ( > tm1 0)
   ( >= ws 0)                                        ( check - sat )



A.2     SMT-LIB Encoding of Example 2
We overapproximated the SMT-LIB2 formula above using our script. The script considers
relaxing each inequality individually, resulting in the inequalities tS −R 1 ≥ 0 and tM −R 1 ≥ 0
instead of the equivalent ¬(tS −R 1 <R 0) and ¬(tM −R 1 <R 0) from formula (2). We also
added comments annotating parts of the encoding. Otherwise the resulting formula matches
the complete relaxed formula from Example 2:

( set - logic QF_UFNRA )                             )

;; Newly added functions                             ;; Translated declarations
( declare - fun ufrac ( Real Real ) Real )           ( declare - const ts1 Real )
( define - fun ax_frac_bound                         ( declare - const ts2 Real )
   (( x Real ) ( y Real )) Bool                      ( declare - const tm1 Real )
   ( and                                             ( declare - const tm2 Real )
      (= > ( > y 0) ( and                            ( declare - const wm1 Real )
           ( <= 0.0 ( ufrac x y ))                   ( declare - const wm2 Real )
           ( < ( ufrac x y ) 1.0)))                  ( declare - const ns Real )
      (= > ( < y 0) ( and                            ( declare - const ws Real )
           ( >= 0.0 ( ufrac x y ))
           ( > ( ufrac x y ) ( - 1.0))))             ;; Newly added axiom instances :
))                                                   ( assert ( ax_frac_bound (* ws tm2 )    ts2 ))
( define - fun ax_frac_zero                          ( assert
   (( x Real ) ( y Real ) ( z Real ) ( w Real ))        ( ax_frac_zero (* ws tm2 ) ts2 ws    tm2 ))
   Bool                                              ( assert
   (= > ( and (= x (* z w ))                            ( ax_frac_zero (* ws tm2 ) ts2 ns    tm1 ))
               ( or (= y z ) (= y w )))              ( assert
         (= ( ufrac x y ) 0))                           ( ax_frac_zero (* ws tm2 ) ts2 ws    tm1 ))
)                                                    ( assert ( ax_frac_bound (* ns tm1 )    ts1 ))
( define - fun ax_int_approx                         ( assert
   (( x Real )) Bool                                    ( ax_frac_zero (* ns tm1 ) ts1 ws    tm2 ))
   ( or (= x 0) ( >= x 1) ( <= x ( - 1)))            ( assert


                                                                                                  11
Overapproximation of NIA for Smart Contract Verification                                                 Hozzová et al.


   ( ax_frac_zero (* ns tm1 ) ts1 ns                   tm1 ))         ( >=   ( - tm1 1) 0)
( assert                                                              ( >=   ws 0)
   ( ax_frac_zero (* ns tm1 ) ts1 ws                   tm1 ))         ( >=   wm1 0)
( assert ( ax_frac_bound (* ws tm1 )                   ts1 ))         ( >=   ns 0)
( assert                                                              ( >=   ts2 0)
   ( ax_frac_zero (* ws tm1 ) ts1 ws                   tm2 ))         ( >=   tm2 0)
( assert                                                              ( >=   wm2 0)
   ( ax_frac_zero (* ws tm1 ) ts1 ns                   tm1 ))    ))
( assert
   ( ax_frac_zero (* ws tm1 ) ts1 ws                   tm1 ))    ( assert (= wm1
( assert ( ax_int_approx wm2 ))                                     ( - (/ (* ws tm1 ) ts1 )
( assert ( ax_int_approx ts1 ))                                         ( ufrac (* ws tm1 ) ts1 ))))
( assert ( ax_int_approx ns ))                                   ( assert (= ts2 (+ ts1 ns )))
( assert ( ax_int_approx ws ))                                   ( assert (= tm2
( assert ( ax_int_approx wm1 ))                                     (+ tm1 ( - (/ (* ns tm1 ) ts1 )
( assert ( ax_int_approx tm1 ))                                                 ( ufrac (* ns tm1 ) ts1 )))))
( assert ( ax_int_approx tm2 ))                                  ( assert (= wm2
( assert ( ax_int_approx ts2 ))                                     ( - (/ (* ws tm2 ) ts2 )
                                                                        ( ufrac (* ws tm2 ) ts2 ))))
;; Relaxed assertions :                                          ( assert ( not ( > (+ wm1 1) wm2 )))
( assert ( and
   ( >= ( - ts1 1) 0)                                            ( check - sat )



A.3       A Sample Smart Contract Verification Problem
Example 1 corresponds to a part of a simplified version of the following smart contract verifica-
                                            ′
tion problem. The variables tS , tM , wM , wM , nS , wS correspond to variables elastic1, base1,
toBase1, toBase2, addAmount, someValue, respectively.
    The original specification in the Certora Verification Language syntax:6

methods {
  function getElastic () external                                     uint128 elastic1 = getElastic ();
    returns ( uint128 ) envfree ;                                     uint128 base1 = getBase ();
  function getBase () external                                        /** these cases are handled
    returns ( uint128 ) envfree ;                                      * separately */
  function toBaseFloor ( uint256 elastic )                            require base1 != 0;
    external returns ( uint256 ) envfree ;                            require elastic1 != 0;
  function addFloor ( uint256 elastic )
    external returns ( uint256 ) envfree ;                            uint256 toBase1 =
}                                                                       toBaseFloor ( someValue );

/** x and y are almost equal ; y may be                               /** using ~ Floor version so the
 * smaller than x up to epsilon */                                     * rounding error is in favour
definition o n l y _ s l i g h t l y _ l a r g e r _ t h a n (         * of the " bank " */
    uint x , uint y , uint epsilon )                                  uint256 addAmountBase =
    returns bool =                                                      addFloor ( addAmount );
  y <= x &&
    x <= r eq ui r e_ ui nt 2 56 ( y + epsilon );                     uint256 toBase2 =
                                                                        toBaseFloor ( someValue );
/** Check that adding some amount does
 * not impact the elastic / base                                      uint256 sum1 = re q ui re _u i nt 25 6 (
 * quotient beyond the given error                                      elastic1 + addAmount );
 * margin . */                                                        uint256 error_margin =
rule integrit yOnAdd {                                                  r eq ui r e_ ui nt 2 56 (
  uint128 addAmount ;                                                      ( someValue / sum1 ) + 1);
  uint128 someValue ;

     6 https://docs.certora.com/en/latest/docs/cvl/index.html



12
Overapproximation of NIA for Smart Contract Verification                                             Hozzová et al.


    assert o n l y _ s l i g h t l y _ l a r g e r _ t h a n (            result of toBaseFloor ( someValue )
      toBase1 , toBase2 , error_margin ) ,                                significantly ; but does so .";
        " addFloor (..) may not change the                       }



     The corresponding contract in Solidity:

pragma solidity 0.6.12;
pragma experimental ABIEncoderV2 ;                               /** from BoringMath . sol */

/** verification harness contract */                             /** @notice A library for performing
contract RebaseWrapper {                                          * over -/ underflow - safe math , updated
  using BoringMath for uint256 ;                                  * with awesomeness from DappHub
  using BoringMath128 for uint128 ;                               * https :// github . com / dapphub / ds - math
                                                                  */
    Rebase public rebase ;                                       library BoringMath {
                                                                   function mul ( uint256 a , uint256 b )
    function getElastic () public view                                 internal pure returns
        returns ( uint128 ) {                                          ( uint256 c ) {
      return rebase . elastic ;                                      require ( b == 0 ||
    }                                                                          ( c = a * b ) / b == a ,
                                                                       " BoringMath : Mul Overflow ");
    function getBase () public view                                }
        returns ( uint128 ) {
      return rebase . base ;                                         function to128 ( uint256 a ) internal
    }                                                                    pure returns ( uint128 c ) {
                                                                       require ( a <= uint128 ( -1) ,
    function toBaseFloor ( uint256 elastic )                             " BoringMath : uint128 Overflow ");
        public view returns                                            c = uint128 ( a );
        ( uint256 base ) {                                           }
      if ( rebase . elastic == 0) {                              }
        base = elastic ;
      } else {                                                   /** @notice A library for performing
        base = elastic . mul ( rebase . base ) /                   * over -/ underflow - safe addition
                rebase . elastic ;                                 * and subtraction on uint128 . */
      }                                                          library BoringMath128 {
    }                                                               function add ( uint128 a , uint128 b )
                                                                        internal pure returns
    function addFloor ( uint256 elastic )                               ( uint128 c ) {
      public returns ( uint256 base ) {                               require (( c = a + b ) >= b ,
      base = toBaseFloor ( elastic );                                   " BoringMath : Add Overflow ");
      rebase . elastic =                                            }
        rebase . elastic . add (                                 }
          elastic . to128 ());
      rebase . base =                                            /** from BoringRebase . sol */
        rebase . base . add ( base . to128 ());                  struct Rebase {
      return base ;                                                uint128 elastic ;
    }                                                              uint128 base ;
                                                                 }
}

Note that the code and comments above were edited for conciseness and clarity. The code
includes the smart contract written by Certora during the verification process, and the relevant
parts from libraries BoringMath.sol and BoringRebase.sol, version corresponding to commit
9f6d8707 .

   7 https://github.com/boringcrypto/BoringSolidity/tree/9f6d8708aa5df8b5d6cdad4a917e37b14c348684/

contracts/libraries


                                                                                                                 13
