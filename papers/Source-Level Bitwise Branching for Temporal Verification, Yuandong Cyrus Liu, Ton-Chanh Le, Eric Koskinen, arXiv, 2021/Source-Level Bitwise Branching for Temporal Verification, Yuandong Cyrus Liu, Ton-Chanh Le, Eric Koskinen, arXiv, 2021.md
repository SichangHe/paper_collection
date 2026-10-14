                                                  Source-Level Bitwise Branching for Temporal
                                                                  Verification
                                                                             Yuandong Cyrus Liu, Ton-Chanh Le, Eric Koskinen
                                                                             Stevens Institute of Technology, Hoboken, NJ 07030 USA


                                           Abstract—There is increasing interest in applying verification       Example (1) involves a simple loop, in which a is decre-
                                        tools to programs that have bitvector operations. SMT solvers,          mented, but the loop condition is on variable x, whose value
                                        which serve as a foundation for these tools, have thus increased        is a bitvector expression over a.
arXiv:2111.02938v1 [cs.PL] 4 Nov 2021




                                        support for bitvector reasoning through bit-blasting and linear
                                        arithmetic approximations. Still, verification tools are limited on        Critical to verifying termination of this program are (1)
                                        termination and LTL verification of bitvector programs.                 proving the invariant(I) x > 0 ∧ a > 0 within the body of
                                           In this work, we show that similar linear arithmetic approx-         the loop and (2) synthesizing a rank function. To prove the
                                        imation of bitvector operations can be done at the source level         invariant, tools must show that it holds after a step of the
                                        through transformations. Specifically, we introduce new paths           loop’s transition relation T = x>0 ∧ a′ =a−1 ∧ x′ =x&a′ ,
                                        that over-approximate bitvector operations with linear condi-
                                        tions/constraints, increasing branching but allowing us to better
                                                                                                                which requires reasoning about the bitwise-& operation be-
                                        exploit the well-developed integer reasoning and interpolation of       cause if we simply treat the & as an uninterpreted function,
                                        verification tools. We present two sets of rules, namely rewriting      I ∧ T ∧ x′ >0 =⇒  6   I ′.
                                        rules and weakening rules, that can be implemented as bitwise              The bitwise branching strategy we introduce in Sec. II helps
                                        branching of program transformation, the branching path can             the verifier infer these invariants (and later synthesize rank
                                        facilitate verification tools widen verification tasks over bitvector
                                        programs. Our experiment shows this exploitation of integer
                                                                                                                functions) by transforming the bitvector assignment to x into
                                        reasoning and interpolation enables competitive termination             linear constraint x ≤ a, but only under the condition that
                                        verification of bitvector programs and leads to the first effective     x ≥ 0 and a ≥ 0.               a = *; assume(a > 0);
                                        technique for LTL verification of bitvector programs.                      In this case, bitwise       while (x > 0) {
                                                                                                                branching translates the         { x > 0 ∧ a > 0 }
                                                                                                                                                 a--;
                                                               I. I NTRODUCTION                                 loop in Example (1) as            if (x >= 0 && a >= 0)
                                                                                                                depicted in the gray box          then { x = *; assume(x <= a); }
                                           In many case, verification tools(e.g. U ltimate [1]) fail in
                                                                                                                to the right. This trans-         else { x = x & a; }
                                        termination and LTL verification tasks over bitvector pro-
                                                                                                                formation changes the          }
                                        grams, due to complex bitvector reasoning. In this work,
                                                                                                                transition relation of the loop body from T (the original
                                        we introduce two sets of program transforming rules namely
                                                                                                                program) to T ′ :
                                        bitwise branching, which transform a bitwise program to an
                                        over-approximated version by adding linear constraints, this                   T ′ = x>0 ∧ a′ =a−1 ∧ ((x≥0 ∧ a′ ≥0 ∧ x′ ≤a′ )
                                        enable verification tools verify bitvector programs in integer                        ∨(¬(x≥0 ∧ a′ ≥0) ∧ x′ =x&a′ ))
                                        domain.
                                           For example, while ranking functions synthesis is critical in        Importantly, when I holds, the else branch with the & is
                                        proving termination and temporal properties of programs, it is          infeasible, and thus we can treat the & as an uninterpreted
                                        challenging to synthesize ranking functions over the domain             function and yet still prove that I ∧ T ′ ∧ x′ >0 =⇒ I ′ .
                                        of bitvectors due to the complexity of bitvector logics [2].            With the proof of I a tool can then move to the next step
                                        U ltimate, a state-of-the-art verifier for LTL verification, over-      and synthesizing a ranking function R(x, a) that satisfies
                                        approximates bitwise operators as uninterpreted functions,              I ∧ T′      =⇒ R(x, a)≥0 ∧ R(x, a)>R(x′ , a′ ), namely,
                                        and returns U nknown results for the following bitvector                R(x, a) = a.
                                        programs:                                                                  Bitwise branching also enables LTL verification of bitvector
                                                                                                                programs. We also examine the bitwise behavior of programs
                                             (1) Termination            (2) LTL ϕ = (♦(n < 0))                 such as Example (2) above, with the LTL property (♦(n <
                                                                        while(1) {                              0)). Our experiments show that with bitwise branching, our
                                                                          n = *; x = *; y = x-1;
                                                 a = *; assume(a>0);      while (x>0 && n>0) {
                                                                                                                implementation can prove LTL property of this program in
                                                 while (x>0){               n++;                                8.04s.
                                                  a--;                      y = x | n;
                                                  x = x & a;                x = x - y;                                            II. B ITWISE - BRANCHING
                                             }                            }
                                                                          n = -1;                                  We build our bitwise-branching technique on the known
                                                                        }
                                                                                                                strategy of transforming bitvector operations into integer ap-
                                          In this work, we show that the key benefits of bitwise                proximations [3], [4] but explore a new direction: source-
                                        branching arise when concerned with termination and LTL.                level transformations to introduce new conditional paths that
                                        e1 = 0           ⊢E   e1 &e2       0           TABLE I: LTL Verification over Bitvector programs resutls
                    (e1 = 0 ∨ e1 = 1) ∧ e2 = 1           ⊢E   e1 &e2       e1
         (e1 = 0 ∨ e1 = 1) ∧ (e2 = 0 ∨ e2 = 1)           ⊢E   e1 &e2       e1 &&e2
                                                                                                                     (i)BitHacks                 (ii)LT LBit
                               e1 ≥ 0 ∧ e2 = 1           ⊢E   e1 &e2       e1 %2
                                        e2 = 0           ⊢E   e1 |e2       e1                                   U ltimate     w.BwB        U ltimate     w.BwB
                    (e1 = 0 ∨ e1 = 1) ∧ e2 = 1           ⊢E   e1 |e2       1
                                        e2 = 0           ⊢E   e1 ˆe2       e1          ✔                           3             10             -           21
                    e1 = e2 = 0 ∨ e1 = e2 = 1            ⊢E   e1 ˆe2       0           ✗                            -             7             -           20
         (e1 = 1 ∧ e2 = 0) ∨ (e1 = 0 ∧ e2 = 1)           ⊢E   e1 ˆe2       1           ?(Unknown)                  21             5            42            -
  e1 ≥ 0 ∧ e2 = CHAR_BIT * sizeof(e1 ) − 1               ⊢E   e1 >>e2      0
  e1 < 0 ∧ e2 = CHAR_BIT * sizeof(e1 ) − 1               ⊢E   e1 >>e2      −1          T (TimeOut)                 1              1             -            1
                                                                                       M (Out of Memory)           1              3             -            -
                   (a) Rewriting rules for arithmetic expressions.
                                                                                         The rules in Fig. 1a and Fig. 1b were developed empirically,
                       e1 ≥ 0 ∧ e2 ≥ 0   ⊢S   r ople e1 &e2   r<=e1 && r<=e2
                                                                                      from the reachability/termination/LTL benchmarks, especially,
                       e1 < 0 ∧ e2 < 0
                       e1 ≥ 0 ∧ e2 < 0
                                         ⊢S
                                         ⊢S
                                              r ople e1 &e2
                                              r opeq e1 &e2
                                                              r<=e1 && r<=e2 && r<0
                                                              0<=r && r<=e1
                                                                                      based on patterns found in decompiled binaries(enable us to
 (e1 = 0 ∨ e1 = 1) ∧ (e2 = 0 ∨ e2 = 1)   ⊢S   (e1 |e2 )==0    e1 ==0 && e2 ==0        verify properties over binaries). We then generalized these
              e1 ≥ 0 ∧ is_const(e2 )     ⊢S   r opge e1 |e2   r>=e2
                       e1 ≥ 0 ∧ e2 ≥ 0   ⊢S   r opge e1 |e2   r>=e1 && r>=e2          rules to expand coverage, proofs for each rule were done with
                       e1 < 0 ∧ e2 < 0   ⊢S   r opeq e1 |e2   r>=e1 && r>=e2 && r<0
                       e1 ≥ 0 ∧ e2 < 0   ⊢S   r opeq e1 |e2   e2 <=r && r<0           Z3.
                       e1 ≥ 0 ∧ e2 ≥ 0   ⊢S   r opge e1 ˆe2   r>=0
                       e1 < 0 ∧ e2 < 0   ⊢S   r opge e1 ˆe2   r>=0
                       e1 ≥ 0 ∧ e2 < 0   ⊢S   r ople e1 ˆe2   r<0                                    III. E XPERIMENTS & C ONCLUSION
                                e1 ≥ 0   ⊢S   r ople ∼e1      r<0
                                e1 < 0   ⊢S   r opge ∼e1      r>=0
                                                                                         We implemented bitwise branching via a translation algo-
(b) Weakening rules for relational expressions and assignments.
ople ∈ {<,<=,==,:=}, opge ∈ {>,>=,==,:=}, and opeq ∈ {==,:=}                          rithm, in a fork of U ltimate, which is the state-of-the-art
                                                                                      LTL prover and the only mature LTL verifier that supports
Fig. 1: Rewriting rules. Commutative closures omitted for                             bitvector programs, we denote our branch U ltimateBwB. To
brevity.                                                                              our knowledge, there are no available bitwise benchmarks with
approximate many (but not all) behaviors of a bitvector                               LTL properties so we create new benchmarks for this purpose:
program. These new paths through the program have linear                              (i) New hand-crafted benchmarks called LT LBit of 42 C
input conditions and linear output constraints and frequently                         programs with LTL properties, in which bitwise operations are
cover all of the program’s behavior (with respect to the goal                         heavily used in assignments, loop conditions, and branching
property), but otherwise fall back on the original bitvector                          conditions. There are 22 programs in which the provided LTL
behavior when none of the input conditions hold. We provide                           properties are satisfied (✔) and 20 programs in which the LTL
two sets of bitwise-branching rules:                                                  properties are violated (✗). (ii) Benchmarks adapted from the
   1. Rewriting rules of the form C ⊢E ebv           eint in Fig.                     BitHacks programs [5], consisting of 26 programs with LTL
1a. These rules are applied to bitwise arithmetic expressions                         properties (18 satisfied and 8 violated).
ebv and specify a condition C for which one can use integer                              Table I summarizes the result of applying U ltimate
approximate behavior eint of ebv .                                                    and U ltimateBwB on these two bitvector benchmarks.
   In other words, rewriting rule C ⊢E ebv          eint can be                       U ltimateBwB outperforms U ltimate thanks to our newly
applied only when C holds and a bitwise arithmetic expression                         added abstraction of bitwise operations. U ltimateBwB can
e in the program structurally matches its ebv with a substitution                     successfully verify 41 of 42 programs in LT LBit and 18 of
δ. Then, e will be transformed into a conditional approxi-                            26 BitHacks programs while U ltimate can only handle a few
mation: Cδ ? eint δ : ebv . Note that, although modulo-2 is                           of them. Note that we have more out-of-memory results in
computationally more expensive, it is often more amenable                             BitHacks Benchmarks, perhaps due to memory consumption
to integer reasoning strategies. For conciseness, we omitted                          reasoning about the introduced paths.
variants that arise from commutative re-ordering of the rules                            In conclusion, bitwise branching appears to be the first
(in both Figs. 1a and 1b).                                                            effective technique for verifying LTL properties of bitvector
   2. Weakening rules of the form C ⊢S sbv            sint are in                     programs.
Fig. 1b. These rules are applied to relational condition ex-                                                       R EFERENCES
pressions (e.g., from assumptions) and assignment statements                          [1] M. Heizmann, J. Christ, D. Dietsch, J. Hoenicke, M. Lindenmann,
sbv , specifying an integer condition C and over-approximation                            B. Musa, C. Schilling, S. Wissert, and A. Podelski, “Ultimate program
transition constraint sint .                                                              analysis framework,” p. 1.
                                                                                      [2] G. Kovásznai, A. Fröhlich, and A. Biere, “Complexity of Fixed-Size Bit-
   When the rule is applied to a statement (as opposed                                    Vector Logics,” Theory of Computing Systems, vol. 59, pp. 323–376, Aug.
to a conditional), replacement sint can be implemented as                                 2016.
assume(sint ). When a weakening rule C ⊢S sbv                sint                     [3] M. Bozzano, R. Bruttomesso, A. Cimatti, A. Franzén, Z. Hanna, Z. Khasi-
                                                                                          dashvili, A. Palti, and R. Sebastiani, “Encoding RTL Constructs for
is applied to an assignment s with substitution δ, the trans-                             MathSAT: a Preliminary Report,” Electron. Notes Theor. Comput. Sci.,
formed statement is if Cδ assume(sint δ) else sbv . In                                    vol. 144, no. 2, pp. 3–14, 2006.
addition, when sbv of a weakening rule can be matched to the                          [4] Y. Zohar, A. Irfan, M. Mann, A. Niemetz, A. Notzli, M. Preiner,
                                                                                          A. Reynolds, C. Barrett, and C. Tinelli, “Bit-Precise Reasoning via Int-
condition c in an assume(c) of the original program via a                                 Blasting,” 2021.
substitution δ, then the assume(c) statement is transformed                           [5] S.          Anderson,            “Bit          twiddling          hacks,”
to if Cδ then assume(sint δ) else assume(c).                                              graphics.stanford.edu/∼ seander/bithacks.html.
