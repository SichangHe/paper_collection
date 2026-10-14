                                          Synthesis Benchmarks for Automated Reasoning⋆

                                                         Márton Hajdu1 , Petra Hozzová2 , Laura Kovács1 ,
                                              Andrei Voronkov3,4, Eva Maria Wagner1( ) , and Richard Steven Žilinčík1
                                                                         1
                                                                           TU Wien, Vienna, Austria
                                                                        eva.maria.wagner@tuwien.ac.at
                                                                2
                                                                   Czech Technical University, Prague, Czechia
arXiv:2507.19827v3 [cs.LO] 14 Aug 2025




                                                                 3
                                                                    University of Manchester, Manchester, UK
                                                                         4
                                                                           EasyChair, Manchester, UK



                                                  Abstract. Program synthesis is the task of constructing a program con-
                                                  forming to a given speciﬁcation. We focus on deductive synthesis, and in
                                                  particular on synthesis problems with speciﬁcations given as ∀∃-formulas,
                                                  expressing the existence of an output corresponding to any input. So far
                                                  there has been no canonical benchmark set for deductive synthesis using
                                                  the ∀∃-format and supporting the so-called uncomputable symbol restric-
                                                  tion. This work presents such a data set, composed by complementing
                                                  existing benchmarks by new ones. Our data set is dynamically growing
                                                  and should motivate future developments in the theory and practice of
                                                  automating synthesis.

                                                  Keywords: Synthesis · Induction · Recursion · Automated Reasoning


                                         1      Introduction

                                         Program synthesis constructs code that is correct by design [6], meaning that the
                                         synthesized code satisﬁes its given requirements. For the purpose of automating
                                         synthesis, such requirements are typically expressed in fragments of ﬁrst-order
                                         logic (FOL) with theories, extending the use of automated reasoning engines to-
                                         wards deriving programs from the correctness proofs of program requirements.
                                         This paper focuses on program synthesis using speciﬁcations given as ∀∃-formulas,
                                         expressing the existence of a program output corresponding to any input.5
                                         Related work. The automation of this instance of program synthesis has been
                                         recently addressed by means of satisﬁability modulo theory (SMT) solving [9, 14]
                                         and/or ﬁrst-order theorem proving [7, 8, 11, 12]. The approaches of [7–9, 14] sup-
                                         port diﬀerent formats of program speciﬁcations with additional syntactic restric-
                                         tions on the sought program: either (i) the syntax-guided synthesis (SyGuS) for-
                                         mat [13], which supplies a context-free grammar used to construct the program, or
                                         (ii) speciﬁcations given as ﬁrst-order logic ∀∃-formulas, supplemented by a list of
                                         so-called uncomputable symbols that are forbidden to occur in the program [7, 8].
                                          ⋆
                                              This is the version of the paper accepted for CICM’25.
                                          5
                                              This speciﬁcation class allows to specify single-invocation functions.
2        Hajdu, Hozzová, Kovács, Voronkov, Wagner, Žilinčík

These format diﬀerences are signiﬁcant enough that SyGuS benchmarks cannot
be expressed using the uncomputable framework of (ii), and further, dropping the
context-free grammar often results in trivial benchmarks. On the other hand, while
the format of (ii) allows to use speciﬁcations in full FOL combined with various the-
ories, the SyGuS format does not support uninterpreted function/predicate sym-
bols within FOL, limiting the expressivity of the SyGuS deductive synthesis bench-
marks from the SyGuS competitions [1]. Overall, there is a lack of synthesis bench-
marks requiring reasoning with theories, quantiﬁers and induction, which would
facilitate scaling deductive synthesis approaches. This paper aims to bridge the
synthesis formats of (i) and (ii), and introduces a dataset of synthesis problems that
can be used both with uncomputable symbols and within extensions of SyGuS.
Our dataset. We collect 37 benchmarks from [7–9], and complement them with
253 new problems. State of the art currently solves 140 benchmarks out of the 290
(see Section 4). Our benchmarks are available online at:
    https://github.com/vprover/vampire_benchmarks/tree/cicm2025/synthesis
Our dataset is continuously growing and invites contributions from the commu-
nities of computer mathematics, automated reasoning, program veriﬁcation, and
others.
Input. Problems in our dataset use program speciﬁcations given as a pair of the
speciﬁcation formula and a set of uncomputable symbols ui , namely
            h∀x1 ∈ S1 ,...,xn ∈ Sn ∃y1 ∈ T1 ,...,ym ∈ Tm .ϕ[x̄,ȳ], {u1 ,...,uk }i,     (1)
             |                       {z                         } | {z }
                             speciﬁcation formula              uncomputable symbols

where x̄ denotes the set of input variables x1 ,...,xn of sorts S1 ,...,Sn ; ȳ denotes the
set of output variables y1 ,...,ym of sorts T1 ,...,Tm ; ϕ is a many-sorted FOL formula,
possibly using theories and recursive deﬁnitions, with the only free variables x̄,ȳ;
and u1 ,...,uk are uncomputable symbols. Intuitively, speciﬁcation (1) states the
existence of m functions with input variables x̄, conforming to the speciﬁcation
formula, each independent of all of u1 ,...,uk . If the speciﬁcation formula ϕ has the
form ψ → ϕ′ [x̄,ȳ], where ψ is a closed formula, then ϕ can equivalently be written as
                 ψ → ∀x1 ∈ S1 ,...,xn ∈ Sn ∃y1 ∈ T1 ,...,ym ∈ Tm .ϕ′ [x̄,ȳ],           (2)
and in this case we call ψ the background axioms and deﬁnitions.
Output. A solution for speciﬁcation (1) is a tuple of terms hr1 [x̄],...,rm [x̄]i, where
∀x1 ∈ S1 ,...,xn ∈ Sn .ϕ[x1 ,...,xn ,r1 [x̄],...,rm [x̄]] is valid in the underlying theory,
and ri [x̄] does not contain uj for all i ∈ {1,...,m}, j ∈ {1,...,k}. We leave the output
format up to individual synthesizers. However, we note that the solution may use
the if−then−else term constructor: for a formula F and terms s,t of the same
sort the term if F then s else t denotes the term s if F is true and t otherwise.
Illustrative example. Let N denote the sort of natural numbers, and ψ be the stan-
dard background deﬁnitions of ≤,+,· on N. Consider the problem from our dataset,
                    hψ → ∀x1 ∈ N, x2 ∈ N ∃y ∈ N. x1 +x2 ≤ y, {+}i,                      (3)
                               Synthesis Benchmarks for Automated Reasoning             3

specifying a (possibly loose) upper bound on the sum of input variables x1 ,x2 . A
possible solution for (3), where 2 is an abbreviation for s(s(0)), is:

                          hif x1 ≤ x2 then x2 ·2 else x1 ·2i.                         (4)


2      Benchmark Format

We base our benchmark format on the SMT-LIB 2.7 syntax [3]. As SMT-LIB is
widely used by automated reasoners, our format makes automated reasoning nat-
urally applicable to synthesis. Our format, dubbed SMT-LIB-SYNU (SMT-LIB
for synthesis with uncomputables), extends SMT-LIB with the following features:

1. Command assert-synth deﬁning a synthesis speciﬁcation formula of (1) as
        (assert-synth ((x1 S1)...(xn Sn)) ((y1 T1)...(yn Tm)) (φ)),
   where x1,...,xn are the input variables, y1,...,ym are the output variables, and φ is
   the standard SMT-LIB encoding of the formula ϕ, with variables xi ,yj and sorts
   Si ,Tj encoded as xi, yj and Si, Tj, respectively, for all i ∈ {1,...,n},j ∈ {1,...,m}.
2. Command assert-claim, asserting auxiliary lemmas, similarly to SMT-LIB’s
   command assert. The automated reasoner may decide to use these lemmas as
   axioms, or only use them after proving them as subgoals [5] (see also Section 3).
3. Option uncomputable to annotate uncomputable symbols u1 , ... , un of (1)
   as
                  (set-option :uncomputable (u1 ... un)).


Complementary format: SyGuS. All of our benchmarks have been translated
into the SyGuS 2.1 syntax [13] using a Python script written by the authors.6 We
deﬁne computable recursive functions using the non-standard yet recommended
command define-fun-rec, already supported by some SyGuS solvers. Since Sy-
GuS does not allow declarations of uninterpreted functions, we encode functions
that are declared but not deﬁned, as well as uncomputable symbols, as follows.
We replace each declared function symbol and each uncomputable symbol by a
(possibly higher-order) universally quantiﬁed variable of the same sort. SMT-LIB
assertions over the symbols are encoded as SyGuS assumptions over the variables.
We add these variables as arguments to the signatures of the to-be-synthesized
functions, and also pass the variables as function arguments in the constraint
statement. This allows the solver to use the variables corresponding to computable
uninterpreted symbols in the solution.
   The only uncomputable symbols in our benchmarks are uninterpreted. To ex-
press their uncomputability, it is suﬃcient to leave their corresponding higher-
order variables out of the list of inputs for the function(s) to be synthesized. We
note that uncomputability of interpreted symbols can be expressed via SyGuS
syntactic restriction – by specifying a grammar allowing all computable symbols
of the suitable sort.
 6
     Translation script synthesis/tools/smt2-to-sygus.py in our benchmark repository.
4        Hajdu, Hozzová, Kovács, Voronkov, Wagner, Žilinčík

3     Benchmark Categories

Our dataset currently contains 290 benchmarks. It consists of (i) 180 non-recursive
problems and (ii) 110 recursive problems over algebraic data types. We call bench-
marks recursive if they contain recursively deﬁned functions, as proving their
speciﬁcations may require induction, leading to synthesizing recursive programs.
   For selected benchmarks, we provide two versions, denoted by the ﬁle suﬃxes
original and assisted. The original benchmarks only contain the necessary
axioms, while the assisted ones include auxiliary lemmas (using assert-claim),
which we found to be helpful for proving the existence of a solution.


3.1     Non-Recursive Benchmarks
Our non-recursive benchmarks are sub-categorized similarly to SMT-LIB logics,
denoted with the preﬁx NR_. For example, NR_UF uses only uninterpreted functions
and no theories, while NR_LIA uses linear integer arithmetic.7 The following NR_UF
example reasons over group theory.

  Example of a NR_UF benchmark (group-3-square_commutativity_assisted.smt2)
(set-logic UF)
(declare-sort s 0)
(declare-fun inv (s) s)
(declare-fun op (s s) s)
(declare-const e s)
; Group axioms: left inverse, left identity, associativity
(assert (forall ((x s)) (= (op (inv x) x) e)))
(assert (forall ((x s)) (= (op e x) x)))
(assert (forall ((x s) (y s) (z s))
   (= (op x (op y z)) (op (op x y) z))))
; Additional axiom to aid the solvers: right identity
(assert (forall ((x s)) (= (op x e) x)))
; Synthesis task
(assert-synth ((x s) (y s)) ((z s))
   (=> (distinct (op x y) (op y x)) (distinct (op z z) e)))

The problem uses a group with binary operation op, inverse element function inv,
and neutral element e. It speciﬁes a function with two inputs x and y, such that
when op is not commutative on x, y, then the square of the output is not e. In
mathematical notation this is ∀x,y ∃z. x∗y 6= y∗x → z∗z 6= e.


3.2     Recursive Benchmarks
Our recursive benchmarks, denoted R_UFDT, use the inductive datatypes nat of
natural numbers; list of lists; and tree of binary trees. In some benchmarks,
7
    see our benchmark repo for all our problems and their categorizations.
                            Synthesis Benchmarks for Automated Reasoning            5

list and tree use nat as the element type; in others, they use arbitrary types.
The following recursive benchmark encodes example (3) of Section 1, using the
nat datatype:

  Example of a R_UFDT benchmark (nat-upper_bound_of_sum.smt2)
(set-logic UFDT)
; Datatype declarations
(declare-datatype nat ((zero) (s (s0 nat))))
; Function definitions
(define-fun-rec add ((x nat) (y nat)) nat
   (match y ((zero x) ((s y0) (s (add x y0))))))
(define-fun-rec mult ((x nat) (y nat)) nat
   (match y ((zero zero) ((s y0) (add (mult x y0) x)))))
(define-fun leq ((x nat) (y nat)) Bool (exists ((k nat))(= (add x k) y)))
; Synthesis task
(assert-synth ((x1 nat) (x2 nat)) ((y nat)) (leq (add x1 x2) y))
(set-option :uncomputable (add))

The inductive datatype nat has constructors zero and s. The recursive functions
add and mult are deﬁned over nat. The function leq is deﬁned over nat using add.
The speciﬁcation asks for an upper bound on the sum of two inputs wrt leq.

   We give an additional example input ﬁle from our R_UFDT category that reasons
over mixed datatypes: a list containing nat elements.
  Example of a R_UFDT benchmark (list-max_elem.smt2)
(set-logic UFDT)
; Datatype declarations
(declare-datatype nat ((s (s0 nat)) (zero)))
(declare-datatype lst ((nil) (cons (cons0 nat) (cons1 lst))))
; Function definitions
(define-fun-rec add ((x nat) (y nat)) nat
   (match y ((zero x)
           ((s y0) (s (add x y0))))))
(define-fun leq ((x nat) (y nat)) Bool (exists ((k nat))(= (add x k) y)))
(define-fun-rec inlst ((x nat) (y lst)) Bool
   (match y ((nil false)
           ((cons y0 y1) (or (= x y0) (inlst x y1))))))
; Synthesis task
(assert-synth ((l lst)) ((n nat))
   (and (inlst n l) (forall ((k nat)) (=> (inlst k l) (leq k n)))))

The datatype list is deﬁned containing elements of type nat with constructors
nil and cons. The recursive function inlst is deﬁned over lists. The speciﬁcation
asks for a program that takes a list as input and returns the biggest element.
6        Hajdu, Hozzová, Kovács, Voronkov, Wagner, Žilinčík

4     Evaluation and Experiments
To provide an insight into how challenging our benchmarks are, we ran cvc5 [2,14],
Synthesiz3 [4, 9], and Vampire [7, 8, 10]. We used a time limit of 1 minute per
benchmark, and ran the benchmarks on an Apple M1 Pro CPU with 32 GB mem-
ory. We ran the solvers in the following conﬁgurations:
– cvc5: version 1.2.18 , using the command cvc5 <benchmark.sl>
– Synthesiz3: default conﬁguration9 , using the command
  python run_synthesiz3.py <benchmark.smt2>
– Vampire: synthesis-recursive branch10 , using the command
  vampire -ind struct -qa synthesis -alasca off -tgt off -erd off -updr
  off -indc goal -nm 0 -ep off <benchmark.smt2>

   The individual solvers solved the following numbers of benchmarks in each
category:11
    Category     Total        cvc5       Synthesiz3      Vampire       Total Solved
    NR_LIA        60           29            32            13              37
    NR_LRA        60           28            32            13              36
    NR_NIA         8            3            2              2               6
    NR_NRA         8            0            2              3               5
    NR_UF         20            4            4             20              20
    NR_UFLIA       12           5            10             3              10
    NR_UFLRA       12           7            8              2               9
    R_UFDT        110           3            0             17              17
    altogether    290          80            90            73              140

   Given the expected growth of our benchmark set, as well as the agile develop-
ment of state-of-the-art solvers, we emphasize that our experimental results only
depict the current capabilities of the respective synthesis tools. We are conﬁdent
that the solvers’ performance will continue improving.

5     Conclusions
We describe our program synthesis dataset where program speciﬁcations are given
as ∀∃ ﬁrst-order formulas. Our dataset can be used for evaluating both the proving
and synthesis abilities of automated reasoners in ﬁrst-order logic, including rea-
soning with theories and induction. Our dataset is planned to be further expanded
by users and developers of reasoning tools, for example by extending our input for-
mat and considering benchmarks with multiple-invocation functions and function
composition benchmarks, and with benchmarks using interpreted uncomputable
symbols.
8
   https://github.com/cvc5/cvc5/releases/
9
   https://doi.org/10.5281/zenodo.16436706
10
   https://github.com/vprover/vampire/tree/synthesis-recursive
11
   The per-problem breakdown of the results is displayed in the appendix.
                             Synthesis Benchmarks for Automated Reasoning            7

Acknowledgements. This research was funded in whole or in part by the
ERC Consolidator Grant ARTIST 101002685, the ERC Proof of Concept Grant
LEARN 101213411, the TU Wien Doctoral College SecInt, the FWF SpyCoDe
Grant 10.55776/F85, the WWTF grant ForSmart 10.47379/ICT22007, the Ama-
zon Research Award 2023 QuAT, and by the European Union under the project
ROBOPROX (reg. no. CZ.02.01.01/00/22_008/0004590).

Disclosure of Interests. The authors have no competing interests to declare
that are relevant to the content of this article.

References
 1. Alur, R., Fisman, D., Padhi, S., Reynolds, A., Singh, R., Udupa, A.: SyGuS-Comp
    2019 (2019), https://sygus.org/comp/2019/
 2. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann,
    M., Mohamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A.,
    Preiner, M., Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A Ver-
    satile and Industrial-Strength SMT Solver. In: TACAS. pp. 415–442 (2022).
    https://doi.org/10.1007/978-3-030-99524-9_24
 3. Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB Standard: Version 2.7.
    Tech. rep., Department of Computer Science, The University of Iowa (2025),
    https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-02-05.pdf
 4. De Moura, L., Bjørner, N.: Z3: An Eﬃcient SMT Solver. In: TACAS. LNCS, vol. 4963,
    pp. 337–340. Springer (2008). https://doi.org/10.1007/978-3-540-78800-3_24
 5. Einarsdóttir, S.H., Hajdu, M., Johansson, M., Smallbone, N., Suda, M.:
    Lemma Discovery and Strategies for Automated Induction. In: IJCAR (2024).
    https://doi.org/10.1007/978-3-031-63498-7_13
 6. Gulwani, S., Polozov, O., Singh, R.: Program synthesis. Foundations and Trends® in
    Programming Languages 4(1-2), 1–119 (2017). https://doi.org/10.1561/2500000010
 7. Hozzová, P., Amrollahi, D., Hajdu, M., Kovács, L., Voronkov, A., Wagner,
    E.M.: Synthesis of Recursive Programs in Saturation. In: Benzmüller, C., Heule,
    M.J., Schmidt, R.A. (eds.) Automated Reasoning. pp. 154–171. Springer Nature
    Switzerland, Cham (2024). https://doi.org/10.1007/978-3-031-63498-7_10
 8. Hozzová, P., Kovács, L., Norman, C., Voronkov, A.: Program Synthesis in Saturation.
    In: CADE. pp. 307–324 (2023). https://doi.org/10.1007/978-3-031-38499-8_18
 9. Hozzová, P., Bjørner, N.: Synthesiz3 This: an SMT-Based Approach for Synthesis
    with Uncomputable Symbols (2025), https://arxiv.org/abs/2504.16536, to appear
    in proceedings of FMCAD 2025.
10. Kovács, L., Voronkov, A.: First-Order Theorem Proving and Vampire. In: CAV. pp.
    1–35 (2013)
11. Manna, Z., Waldinger, R.: A Deductive Approach to Program Synthesis. ACM Trans.
    Program. Lang. Syst. 2(1), 90–121 (1980). https://doi.org/10.1145/357084.357090
12. Manna, Z., Waldinger, R.J.: Toward automatic program synthesis. Commun. ACM
    14(3), 151–165 (Mar 1971). https://doi.org/10.1145/362566.362568
13. Padhi, S., Polgreen, E., Raghothaman, M., Reynolds, A., Udupa, A.: The SyGuS
    Language Standard Version 2.1 (2021), https://sygus-org.github.io/language/
14. Reynolds, A., Kuncak, V., Tinelli, C., Barrett, C.W., Deters, M.: Refutation-
    based synthesis in SMT. Formal Methods Syst. Des. 55(2), 73–102 (2019).
    https://doi.org/10.1007/S10703-017-0270-2
8       Hajdu, Hozzová, Kovács, Voronkov, Wagner, Žilinčík

A     Appendix

Here we show the per-benchmark results for cvc5, Synthesiz3, and Vampire:




                                                                     am iz3
                                                                          re
                                                                           s
                                                                         he

                                                                       pi
                                                                      nt
                                                               c5
    Benchmark




                                                                    Sy
                                                             cv




                                                                    V
                                      NR_LIA
    lower_bound2                                               X     X   X
    lower_bound5                                               X     X   X
    lower_bound10                                              X     X   -
    lower_bound15                                              X     X   -
    lower_bound20                                              X     -   -
    lower_bound25                                              -     -   -
    lower_bound30                                              -     -   -
    lower_bound50                                              -     -   -
    lower_bound100                                             -     -   -
    lower_bound150                                             -     -   -
    lower_strict2                                              X     X   X
    lower_strict5                                              X     X   -
    lower_strict10                                             X     X   -
    lower_strict15                                             X     -   -
    lower_strict20                                             X     -   -
    lower_strict25                                             -     -   -
    lower_strict30                                             -     -   -
    lower_strict50                                             -     -   -
    lower_strict100                                            -     -   -
    lower_strict150                                            -     -   -
    max2                                                       X     X   X
    max5                                                       X     X   X
    max10                                                      X     X   X
    max15                                                      X     X   X
    max20                                                      X     X   -
    max25                                                      -     X   -
    max30                                                      -     X   -
    max50                                                      -     X   -
    max100                                                     -     X   -
    max150                                                     -     -   -
    min2                                                       X     X   X
    min5                                                       X     X   X
    min10                                                      X     X   X
    min15                                                      X     X   X
    min20                                                      X     X   -
    min25                                                      -     X   -
    min30                                                      -     X   -
    min50                                                      -     X   -
    min100                                                     -     X   -
    min150                                                     -     -   -
                  Synthesis Benchmarks for Automated Reasoning       9




                                                        am iz3
                                                             re
                                                              s
                                                            he

                                                          pi
                                                         nt
                                                  c5
Benchmark




                                                       Sy
                                                cv




                                                       V
upper_bound2                                       X     X       X
upper_bound5                                       X     X       -
upper_bound10                                      X     X       -
upper_bound15                                      X     X       -
upper_bound20                                      -     -       -
upper_bound25                                      -     -       -
upper_bound30                                      -     -       -
upper_bound50                                      -     -       -
upper_bound100                                     -     -       -
upper_bound150                                     -     -       -
upper_strict2                                      X     X       X
upper_strict5                                      X     X       -
upper_strict10                                     X     X       -
upper_strict15                                     X     -       -
upper_strict20                                     X     -       -
upper_strict25                                     -     -       -
upper_strict30                                     -     -       -
upper_strict50                                     -     -       -
upper_strict100                                    -     -       -
upper_strict150                                    -     -       -
                           NR_LRA
lower_bound2                                       X     X       X
lower_bound5                                       X     X       -
lower_bound10                                      X     X       -
lower_bound15                                      X     X       -
lower_bound20                                      X     -       -
lower_bound25                                      -     -       -
lower_bound30                                      -     -       -
lower_bound50                                      -     -       -
lower_bound100                                     -     -       -
lower_bound150                                     -     -       -
lower_strict2                                      X     X       X
lower_strict5                                      X     X       -
lower_strict10                                     X     X       -
lower_strict15                                     X     -       -
lower_strict20                                     -     -       -
lower_strict25                                     -     -       -
lower_strict30                                     -     -       -
lower_strict50                                     -     -       -
lower_strict100                                    -     -       -
lower_strict150                                    -     -       -
max2                                               X     X       X
max5                                               X     X       X
max10                                              X     X       X
max15                                              X     X       X
10       Hajdu, Hozzová, Kovács, Voronkov, Wagner, Žilinčík




                                                                      am iz3
                                                                           re
                                                                            s
                                                                          he

                                                                        pi
                                                                       nt
                                                                c5
     Benchmark




                                                                     Sy
                                                              cv




                                                                     V
     max20                                                      X     X   -
     max25                                                      -     X   -
     max30                                                      -     X   -
     max50                                                      -     X   -
     max100                                                     -     X   -
     max150                                                     -     -   -
     min2                                                       X     X   X
     min5                                                       X     X   X
     min10                                                      X     X   X
     min15                                                      X     X   X
     min20                                                      X     X   -
     min25                                                      -     X   -
     min30                                                      -     X   -
     min50                                                      -     X   -
     min100                                                     -     X   -
     min150                                                     -     -   -
     upper_bound2                                               X     X   X
     upper_bound5                                               X     X   X
     upper_bound10                                              X     X   -
     upper_bound15                                              X     X   -
     upper_bound20                                              X     -   -
     upper_bound25                                              -     -   -
     upper_bound30                                              -     -   -
     upper_bound50                                              -     -   -
     upper_bound100                                             -     -   -
     upper_bound150                                             -     -   -
     upper_strict2                                              X     X   X
     upper_strict5                                              X     X   -
     upper_strict10                                             X     X   -
     upper_strict15                                             X     -   -
     upper_strict20                                             -     -   -
     upper_strict25                                             -     -   -
     upper_strict30                                             -     -   -
     upper_strict50                                             -     -   -
     upper_strict100                                            -     -   -
     upper_strict150                                            -     -   -
                                       NR_NIA
     abs                                                        X     -   -
     polynomial1                                                -     -   X
     polynomial1_3ord                                           -     -   -
     polynomial1_3vars                                          -     -   -
     polynomial2                                                -     -   X
     quotient-1                                                 -     X   -
     same-quotient                                              X     X   -
     signum                                                     X     -   -
                      Synthesis Benchmarks for Automated Reasoning       11




                                                            am iz3
                                                                 re
                                                                  s
                                                                he

                                                              pi
                                                             nt
                                                      c5
Benchmark




                                                           Sy
                                                    cv




                                                           V
                               NR_NRA
abs                                                    -     -       -
polynomial1                                            -     -       X
polynomial1_3ord                                       -     -       -
polynomial1_3vars                                      -     -       -
polynomial2                                            -     -       X
quotient-1                                             -     -       X
same-quotient                                          -     X       -
signum                                                 -     X       -
                               NR_UF
UF/fu_is_a                                             X     X       X
UF/u_is_a                                              X     X       X
field/1                                                -     -       X
field/2                                                -     -       X
group/ex1-right_inverse                                -     -       X
group/ex1-right_inverse_2                              -     -       X
group/ex1-right_inverse_5                              -     -       X
group/ex1-right_inverse_10                             -     -       X
group/ex1-right_inverse_15                             -     -       X
group/ex1-right_inverse_25                             -     -       X
group/ex2-inverse_of_ixopiy                            -     -       X
group/ex2-inverse_of_ixopiy_3                          -     -       X
group/ex2-inverse_of_ixopiy_5                          -     -       X
group/ex2-inverse_of_ixopiy_10                         -     -       X
group/ex2-inverse_of_ixopiy_15                         -     -       X
group/ex2-inverse_of_ixopiy_25                         -     -       X
group/ex3-square_commutativity_assisted                -     -       X
group/ex3-square_commutativity_original                -     -       X
workshop/1                                             X     X       X
workshop/2                                             X     X       X
                             NR_UFLIA
between1                                               X     X       X
between2                                               X     X       X
between_strict1                                        X     X       X
between_strict2                                        X     X       -
equation1                                              -     X       -
equation2                                              -     X       -
equation3                                              -     X       -
knapsack1                                              X     X       -
knapsack2                                              -     X       -
knapsack3                                              -     X       -
knapsack4                                              -     -       -
knapsack5                                              -     -       -
                             NR_UFLRA
12       Hajdu, Hozzová, Kovács, Voronkov, Wagner, Žilinčík




                                                                      am iz3
                                                                           re
                                                                            s
                                                                          he

                                                                        pi
                                                                       nt
                                                                c5
     Benchmark




                                                                     Sy
                                                              cv




                                                                     V
     between1                                                   X     X   X
     between2                                                   X     X   X
     between_strict1                                            X     -   -
     between_strict2                                            -     -   -
     equation1                                                  X     X   -
     equation2                                                  X     X   -
     equation3                                                  X     X   -
     knapsack1                                                  X     X   -
     knapsack2                                                  -     X   -
     knapsack3                                                  -     X   -
     knapsack4                                                  -     -   -
     knapsack5                                                  -     -   -
                                       R_UFDT
     tree/max-min-bound/max_elem                                -     -   -
     tree/max-min-bound/min_elem                                -     -   -
     tree/max-min-bound/upper_bound                             -     -   -
     tree/max-min-bound/lower_bound                             -     -   -
     tree/mirrored/1                                            -     -   -
     tree/mirrored/2                                            -     -   -
     tree/mirrored/3                                            -     -   -
     tree/mirrored/4                                            -     -   -
     list/assoc/left_4_vars                                     -     -   -
     list/assoc/left_5_vars                                     -     -   -
     list/assoc/left_minimal                                    -     -   X
     list/assoc/right_4_vars                                    -     -   X
     list/assoc/right_5_vars                                    -     -   X
     list/assoc/right_minimal                                   -     -   X
     list/len/concat_minimal                                    -     -   X
     list/len/concat_3_vars                                     -     -   -
     list/max-min-bound/max_elem                                -     -   -
     list/max-min-bound/min_elem                                -     -   -
     list/max-min-bound/upper_bound                             -     -   -
     list/max-min-bound/lower_bound                             -     -   -
     list/prefix-suffix/prefix-given-suffix_assisted            -     -   -
     list/prefix-suffix/prefix-given-suffix_original            -     -   -
     list/prefix-suffix/suffix-given-prefix_assisted            -     -   -
     list/prefix-suffix/suffix-given-prefix_original            -     -   -
     list/prime_fac                                             -     -   -
     list/prod_of_lists                                         -     -   -
     list/projection/first-elem_assisted                        -     -   X
     list/projection/first-elem_original                        X     -   X
     list/projection/kth_elem                                   -     -   -
     list/projection/last_elem                                  -     -   -
     list/rev/1_assisted                                        -     -   -
     list/rev/1_original                                        -     -   -
                      Synthesis Benchmarks for Automated Reasoning       13




                                                              am iz3
                                                                   re
                                                                    s
                                                                  he

                                                                pi
                                                               nt
                                                        c5
Benchmark




                                                             Sy
                                                      cv




                                                             V
list/rev/2_assisted                                     -     -      -
list/rev/2_original                                     -     -      -
list/rev/3                                              -     -      -
list/rev/4                                              -     -      -
list/rev/5                                              -     -      -
list/rev/6                                              -     -      -
list/rev/7                                              -     -      -
list/sort/1                                             -     -      -
list/sort/2                                             -     -      -
list/sort/3                                             -     -      -
list/sort/4                                             -     -      -
list/sort/5                                             -     -      -
list/sum/1_assisted                                     -     -      -
list/sum/1_original                                     -     -      -
list/sum/2_assisted                                     -     -      -
list/sum/2_original                                     -     -      -
list/sum/3_assisted                                     -     -      -
list/sum/3_original                                     -     -      -
nat/assoc/left1                                         -     -      X
nat/assoc/left2                                         -     -      X
nat/assoc/right1                                        -     -      X
nat/assoc/right2                                        -     -      -
nat/bound_of_sum/lower_bound_of_sum_assisted            X     -      X
nat/bound_of_sum/lower_bound_of_sum_original            -     -      X
nat/bound_of_sum/strict_lower_bound_of_sum_assisted     -     -      X
nat/bound_of_sum/strict_lower_bound_of_sum_original     -     -      X
nat/bound_of_sum/strict_upper_bound_of_sum_assisted     -     -      -
nat/bound_of_sum/strict_upper_bound_of_sum_original     -     -      -
nat/bound_of_sum/upper_bound_of_sum_assisted            -     -      -
nat/bound_of_sum/upper_bound_of_sum_original            -     -      -
nat/dist/left1_assisted                                 -     -      -
nat/dist/left1_original                                 -     -      -
nat/dist/left2_assisted                                 -     -      -
nat/dist/left2_original                                 -     -      -
nat/dist/left3_assisted                                 -     -      -
nat/dist/left3_original                                 -     -      -
nat/dist/right1_assisted                                -     -      -
nat/dist/right1_original                                -     -      -
nat/dist/right2_assisted                                -     -      -
nat/dist/right2_original                                -     -      -
nat/dist/right3_assisted                                -     -      -
nat/dist/right3_original                                -     -      -
nat/division/assisted                                   -     -      -
nat/division/original                                   -     -      -
nat/divisor/1_assisted                                  -     -      -
nat/divisor/1_original                                  -     -      -
14       Hajdu, Hozzová, Kovács, Voronkov, Wagner, Žilinčík




                                                                      am iz3
                                                                           re
                                                                            s
                                                                          he

                                                                        pi
                                                                       nt
                                                                c5
     Benchmark




                                                                     Sy
                                                              cv




                                                                     V
     nat/divisor/2_assisted                                     -     -   -
     nat/divisor/2_original                                     -     -   -
     nat/double/1                                               -     -   X
     nat/double/2                                               -     -   X
     nat/double/3                                               -     -   -
     nat/double/4                                               -     -   -
     nat/factorial/1                                            -     -   -
     nat/factorial/2                                            -     -   -
     nat/fibonacci/1                                            -     -   -
     nat/fibonacci/2                                            -     -   -
     nat/gcd/1_assisted                                         -     -   -
     nat/gcd/1_original                                         -     -   -
     nat/gcd/2_assisted                                         -     -   -
     nat/gcd/2_original                                         -     -   -
     nat/gcd/3_assisted                                         -     -   -
     nat/gcd/3_original                                         -     -   -
     nat/predecessor                                            X     -   X
     nat/quo-rem/quo-rem_original                               -     -   -
     nat/quo-rem/quo_assisted                                   -     -   -
     nat/quo-rem/quo_original                                   -     -   -
     nat/quo-rem/rem_assisted                                   -     -   -
     nat/quo-rem/rem_original                                   -     -   -
     nat/root/assisted                                          -     -   -
     nat/root/original                                          -     -   -
     nat/subtraction/leq_left_assisted                          -     -   -
     nat/subtraction/leq_left_original                          -     -   -
     nat/subtraction/leq_right_assisted                         -     -   -
     nat/subtraction/leq_right_original                         -     -   -
     nat/subtraction/less_left_assisted                         -     -   -
     nat/subtraction/less_left_original                         -     -   -
     nat/subtraction/less_right_assisted                        -     -   -
     nat/subtraction/less_right_original                        -     -   -
