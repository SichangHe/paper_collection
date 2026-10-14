                                            PBLean: Pseudo-Boolean Proof Certificates for Lean 4
                                                                                   Stefan Szeider
                                                                          Algorithms and Complexity Group
                                                                              TU Wien, Vienna, Austria
                                                                         www.ac.tuwien.ac.at/people/szeider/



                                                                                       Abstract
arXiv:2602.08692v2 [cs.LO] 2 Apr 2026




                                                   We present PBLean, a method for importing VeriPB pseudo-Boolean (PB) proof cer-
                                              tificates into Lean 4. Key to our approach is reflection: a Boolean checker function whose
                                              soundness is fully proved in Lean and executed as compiled native code. Our method scales
                                              to proofs with tens of thousands of steps that would exhaust memory under explicit proof-
                                              term construction. Our checker supports all VeriPB kernel rules, including cutting-plane
                                              derivations, proof-by-contradiction subproofs, and redundance-based reasoning for symme-
                                              try breaking. In contrast to external verified checkers that produce verdicts, our integration
                                              yields Lean theorems that can serve as composable lemmas in larger formal developments.
                                              To derive theorems about the original combinatorial problems rather than about PB con-
                                              straints alone, we support verified encodings. This closes the trust gap between solver output
                                              and problem semantics since the constraint translation and its correctness proof are both
                                              formalized in Lean. We demonstrate the approach on various combinatorial problems.


                                        1    Introduction
                                        Pseudo-Boolean (PB) solvers handle linear constraints over Boolean variables and have become
                                        prominent tools for combinatorial optimization and verification [11]. Since these solvers carry
                                        out sophisticated derivations, independent verification of their results is particularly desirable.
                                        However, PB reasoning involves cutting-planes proof steps that resolution-based formats cannot
                                        capture efficiently.
                                            Haken’s classical result [15] shows that the pigeonhole principle requires exponential-size reso-
                                        lution proofs, whereas polynomial-size cutting-plane proofs exist [6]. Beyond pigeonhole, cutting
                                        planes also efficiently capture XOR/parity constraints [14] and certified symmetry breaking [4],
                                        which are reasoning methods that lack efficient resolution-based proof logging. This motivated
                                        the VeriPB proof format [10, 4], based on cutting planes and now used by solvers such as
                                        RoundingSat for certified PB solving.
                                            The LRAT format [16] enables SAT solvers to produce clausal certificates that can be checked
                                        in theorem provers. Lean’s FromLRAT module [23] imports such certificates and produces kernel-
                                        checked theorems. Heule and Scheucher [17] established the empty hexagon theorem using SAT
                                        solving with verified certificate checking; Subercaseaux et al. [25] subsequently formalized this
                                        encoding in Lean and verified the reduction from geometry to SAT. A similar integration for
                                        pseudo-Boolean reasoning has been missing.
                                            Why not compile PB reasoning to clausal proofs and reuse LRAT? Bryant et al. [5] showed
                                        that this is possible via BDD compilation, and their approach handles classical hard cases such
                                        as pigeonhole and parity efficiently. However, the compilation requires coordinating a PB solver
                                        with a BDD-based clausal proof generator, and whether it preserves efficiency for all PB reasoning
                                        remains open. Direct VeriPB import avoids this detour.
                                            The CakePB project [13] provides a verified checker extracted from HOL4 via CakeML,
                                        producing a standalone binary that outputs verdicts. The main advantage of CakePB is its
small, trusted computing base enabled by verified compilation. However, the verified result (a
binary verdict) cannot serve as a lemma in larger formal developments.
    A proof certificate establishes that certain PB constraints are unsatisfiable, but says nothing
about whether those constraints correctly model the intended problem. An encoding bug can
produce unsatisfiable constraints even when solutions exist. We address this gap with verified
encodings: both the constraint translation and its correctness proof are entirely in Lean, so that
certificate import yields theorems about the original problem, not merely about PB constraints.
    We present PBLean, a VeriPB integration for Lean 4 that parses kernel-format proofs and
verifies them via reflection. Instead of building Lean proof terms for each derivation step, we
define a Boolean checker function and prove its soundness once; Lean’s native_decide then
runs the checker as compiled code. This follows the pattern of Lean’s bv_decide tactic [21]
and scales to instances that would exhaust memory under explicit proof construction. Our
implementation covers all VeriPB kernel rules, including proof-by-contradiction subproofs for
optimization reasoning and redundance/dominance rules for symmetry breaking. We apply the
verified encoding workflow to independence numbers of Paley graphs and other combinatorial
theorems to obtain end-to-end-verified results.


2    Background
                                                    Pn
A pseudo-Boolean (PB) constraint has the form i=1 ai ℓi ≥ d, where ai , d ∈ N are non-negative
coefficients, and each ℓi is a literal (a variable xi or its negation xi ). Under an assignment σ, a
literal evaluates to 1 if satisfied and 0 otherwise. The constraint is satisfied when the weighted
sum reaches the degree d. For example, 3x1 + 5x2 ≥ 4 is satisfied by σ(x1 ) = σ(x2 ) = 1 (sum
= 8 ≥ 4) but not by σ(x1 ) = 1, σ(x2 ) = 0 (sum = 3 < 4). Clauses are a special case: x1 ∨ x2 ∨ x3
corresponds to x1 + x2 + x3 ≥ 1.
    Cutting-planes reasoning derives new constraints via: (1) addition of constraints, (2) scalar
multiplication by k ∈ N+ , (3) division by k with the degree rounded up, and (4) saturation,
which caps each coefficient at the degree. These rules strictly generalize resolution [6]: resolution
corresponds to addition with complementary literal cancellation. The power of cutting planes
stems from the interplay of multiplication and division, which derives constraints unreachable by
resolution alone [26].
    The VeriPB proof format [10, 4] provides two modes: an augmented mode with high-level
rules (symmetry breaking, redundance-based strengthening) and a kernel mode (version 3.0) with
only primitive operations. The kernel format’s small rule set of just eight rule types enables a
rigorous soundness proof and makes it well-suited for theorem prover integration. It supports:
pol (polynomial operations including all cutting-planes rules), rup (reverse unit propagation
with conflict hints), pbc (proof by contradiction with explicit subproofs), red/dom (redundance
and dominance, adding equisatisfiable constraints via a substitution witness), del (constraint
deletion, sound by monotonicity), weaken (coefficient weakening), sol/soli (solution logging),
and conclusion (UNSAT/SAT/BOUNDS verdict). Solvers such as RoundingSat produce aug-
mented proofs; veripb –elaborate translates them to kernel format.
    Lean 4 [7] provides a metaprogramming framework where tactics run in monads such as MetaM.
Code in MetaM constructs Expr values (Lean’s internal representation of proof terms), and, upon
type-checking, Lean’s kernel verifies their correctness. Our approach builds Expr values from
VeriPB proofs; the parser and proof-term constructor are untrusted code, as in FromLRAT. The
trusted base consists of Lean’s kernel and the soundness lemmas presented in Section 3.


3    Lean Formalization
For constraint representation, we use natural number arithmetic throughout. A Literal is pos i
or neg i, and a Term is a pair (a, ℓ) ∈ N × Literal ; a Constr is a term list plus degree. Given


                                                 2
aPvaluation v : N → Bool , we define evalLit(v, ℓ) ∈ {0, 1} (1 if satisfied) and evalSum(v, P       T) =
   (a,ℓ)∈T a · evalLit(v, ℓ) recursively to support structural induction; coeffSum(T    ) =   (a,ℓ)∈T a is
 the sum of coefficients. A constraint (T, d) is satisfied when d ≤ evalSum(v, T ).
     Our 15 soundness lemmas are summarized in Table 1; every lemma is proved in Lean and
 verified by the kernel. Two details matter for matchingPVeriPB’s semantics:
                                                                          P           normalization
                                                                                      P             must
 precede saturation and division, and the negation of        ai ℓi ≥ d is   ai ℓ̄i ≥ ( ai ) − d + 1.


                    Table 1: Soundness lemmas for VeriPB kernel operations.

   Operation                          Lean Type
   Cutting planes
   add_sat                            c1 .sat v → c2 .sat v →
                                      (c1 .terms ++ c2 .terms, c1 .deg + c2 .deg).sat v
   mul_sat                            c.sat v → (map (λ(a, ℓ). (k · a, ℓ)) c.terms, k · c.deg).sat v
   div_sat                            0 < k → c.sat v →
                                      (map (λ(a, ℓ). (⌈a/k⌉, ℓ)) c.terms, ⌈c.deg/k⌉).sat v
   saturate_sat                       c.sat v →
                                      (map (λ(a, ℓ). (min(a, c.deg), ℓ)) c.terms, c.deg).sat v
   Normalization
   cancel_pair_sat                    min(a, b) ≤ d → (. . . (a, ℓ) . . . (b, ℓ̄) . . . , d).sat v →
                                      (. . . (a−m, ℓ) . . . (b−m, ℓ̄) . . . , d−m).sat v
   remove_zero_sat                    (pre ++ (0, ℓ)::post, d).sat v → (pre ++ post, d).sat v
   merge_terms_sat                    (. . . (a, ℓ) . . . (b, ℓ) . . . , d).sat v → (. . . (a+b, ℓ) . . . , d).sat v
   Axioms and contradiction
   lit_axiom_pos/neg                  ∀v. ([(1, ℓ)], 0).sat v
   contra_unsat                       coeffSum(c) < c.deg → ¬ c.sat v
   Negation and proof by contradiction
   negate_sat_of_not              c.deg ≤ coeffSum(c) → ¬ c.sat v → c.negate.sat v
   propagation_forces             (T, d).sat v → coeffSum(T \ {(a, ℓ)}) < d → evalLit(v, ℓ) =
                                  1
   pbc_sound                      (∀v. F.allSat v → C.negate.sat v → ⊥) → F.proof C
   Redundance (red/dom)
   applySubstConstr_sat_rev           C|ω .sat v → C.sat (ω(v))
   constr_sat_noSubst                 unaffected (ω, C) → C.sat v → C.sat (ω(v))

   We give two verification approaches with complementary trade-offs.

Explicit proof terms. The first approach builds Lean Expr terms by composing soundness
lemmas. For pol steps, each token in the reverse Polish notation (RPN) expression produces an
application: ID lookups retrieve earlier proofs, addition applies add_sat, multiplication applies
mul_sat, and so on. For rup steps, we negate the target, run PB unit propagation to find a
conflicting hint, and then build a proof accumulator. For pbc subproofs, we extend the context
with the negated assumption and verify inner steps recursively. The resulting Expr is then type-
checked by Lean’s kernel, producing a theorem. Its trusted base consists of just the kernel and
the soundness lemmas. This approach has the disadvantage that the accumulated proof terms
exhaust memory for instances with thousands of constraints.

Reflection. To overcome this limitation, our second approach follows the pattern of Lean’s
bv_decide [21]. We define a Boolean function check (F, π) that takes a constraint set F and


                                                       3
a proof string π, replays all derivation steps, and returns true iff a contradictory constraint is
derived. We then prove a soundness theorem: if check (F, π) = true then F is unsatisfiable.
This theorem is fully proved in Lean without custom axioms. Lean’s native_decide runs the
checker as compiled code, yielding a kernel proof term consisting solely of the soundness theorem
applied to the computation witness. The resulting theorem has the same trust basis as bv_decide
and omega—namely, Lean’s standard axioms (propext, Classical.choice, Quot.sound) plus
Lean.trustCompiler, and scales to proofs with thousands of steps.

Trust model. The reflection-based checker relies on Lean.trustCompiler, the axiom that
Lean’s compiled native code agrees with its kernel evaluator. This is the same trust assump-
tion underlying bv_decide, native_decide, and omega. Lean’s kernel does not verify native
compilation; a bug in the compiler could in principle produce an incorrect evaluation result.
In practice, the Lean compiler is mature and widely used, and the alternative—explicit proof-
term construction—does not scale beyond small instances. The explicit proof-term approach
(our first method above) avoids this axiom entirely, providing a fallback for instances where
Lean.trustCompiler is unacceptable.


4      Implementation
PBLean is a standalone Lean 4 project (v4.28.0-rc1) with no Mathlib dependency. The kernel
layer (PseudoBoolean.lean, ∼900 lines) consists of types and 15 soundness lemmas. The code
is available on GitHub.1
    The reflection-based checker (Reflect.lean, ∼2500 lines) uses a line-by-line tokenizer to con-
vert VeriPB proofs into an abstract syntax tree, handling nested pbc subproofs recursively.
It maintains a constraint database organized as a hash map, with an @[implemented_by] an-
notation providing an array-based runtime replacement for performance without weakening the
proof. Each rule updates or queries this database: pol evaluates the RPN expression, rup derives
a conflict by negating the target and applying PB unit propagation, pbc saves the database, adds
the negated assumption, verifies inner steps recursively, then restores the snapshot, and red/dom
verify coverage of affected constraints and process subproofs for each proof goal before adding the
equisatisfiable constraint. The checker returns true only when a contradictory constraint arises,
and we establish soundness by induction over proof steps, connecting the Boolean computation
to the kernel lemmas.
    To exploit the integration, one provides an OPB file and a kernel-format proof file. The
command veripb_reflect parses both, runs the checker via native_decide, and registers the
resulting unsatisfiability theorem under a given name. For domain-specific applications, wrapper
commands such as independent_set_reflect additionally generate the encoding from a problem
instance and compose the bridge theorem automatically.
    We demonstrate our approach on a problem where the encoding is also formalized in Lean,
closing a trust gap. For SAT, encoding correctness was only recently formalized [25]; for PB
reasoning, no such formalization existed. Figure 1 shows the overall workflow.
    A verified encoding consists of three components: (1) an encode function translating problem
instances to PB constraints, (2) a soundness theorem proving that unsatisfiability of the encoding
implies non-existence of solutions, and (3) a bridge theorem composing encoding correctness with
the imported VeriPB certificate to yield a theorem about the original problem.
    As an example, we consider the independence number (the size of a largest independent set)
of Paley graphs. For a prime p ≡ 1 (mod 4), the Paley graph Paley(p) is defined as the graph
with the vertex set Zp and edges (i, j) whenever j − i is a nonzero quadratic residue. These
                                                                               √
graphs are self-complementary with an independence number α of at most p by the Hoffman
    1 https://github.com/leansolving/pblean




                                                4
                                                               bridge

                                                   untrusted

                Problem             Trusted       PB Solver             Reflection         Lean
                Instance           Encoding       + VeriPB               Checker          Theorem


                                     OPB          Kernel Proof


Figure 1: End-to-end workflow for trusted encodings. OPB is the standard input format for
PB solvers. Solid boxes are verified in Lean; the dashed box is untrusted. The dotted arrow
represents the bridge theorem composing encoding correctness with the PB refutation.


eigenvalue bound. The encoding for “does G have an independent set of size ≥ k?” uses

                           ∀(u, v) ∈ E(G) : x̄u + x̄v ≥ 1        (independence)
                                              : x1 + · · · + xn ≥ k       (cardinality)

   The Lean formalization establishes that if these constraints are unsatisfiable, then G has no
independent set of size ≥ k. Combining the VeriPB certificate with this result yields a theorem
about the graph. The independent_set_decide command automates the whole pipeline: given
a graph and a target size k, it produces a Lean theorem of the form ¬hasIndependentSet(G, k).


5    Evaluation
We evaluate PBLean by measuring wall-clock time on an Apple M2 with cached .olean files.
Measured times include parsing, checker execution via native_decide, and kernel verification.
We use RoundingSat for solving and veripb –elaborate to produce kernel-format proofs.
    Table 2 shows results for independence numbers of Paley(p) for primes p ≡ 1 (mod 4) from
13 to 101.
    The proofs rely on cutting-planes (pol) and reverse unit propagation (rup) steps; the largest
instance (2526 edges, about 63 000 proof lines) verifies in about 3.5 minutes. The pigeonhole
example in Table 3 additionally exercises the red rule for symmetry breaking.


Table 2: Independent set on Paley graphs. p: prime, α: independence number. Vars: PB
variables, Cstrs: PB constraints. Direct: explicit proof-term construction. Reflect: reflection-
based checker. TO = timeout at 60 000 ms.
        p   α    Vars      Cstrs    Solve (ms)    Elab (ms)       Lines      Direct (ms) Reflect (ms)
       13   3      13         40            59              12     35                 1 150             802
       17   3      17         69            38               4     66                 2 310             802
       29   4      29        204            53               5    233                19 922             926
       37   4      37        334           105               6    554                   TO            1 314
       41   5      41        411           131               6    704                   TO            1 536
       53   5      53        690           421              13 1 848                    TO            3 494
       61   5      61        916           850              24 4 151                    TO            6 743
       73   5      73      1 315         3 145              64 9 808                    TO           20 616
       89   5      89      1 959        17 166             234 36 795                   TO           96 234
       97   6      97      2 329        21 673             272 43 214                   TO          115 197
      101   5     101      2 526        29 267             385 62 924                   TO          200 460


                                                       5
   A noteworthy byproduct of this evaluation is a formally verified proof that α(Paley(p)) is
not monotone in p: α(Paley(97)) = 6 > 5 = α(Paley(101)). Here, each equality combines the
VeriPB upper bound with a lower bound from an explicit witness verified by native_decide.

theorem paley_alpha_not_monotone :
    $\exists$ p q : Nat, p < q $\wedge$ $\exists$ a b : Nat,
      independenceNumber (paley p) a $\wedge$
      independenceNumber (paley q) b $\wedge$ a > b

    As noted in Section 3, the explicit proof-term approach does not scale: the Direct column
shows that Paley(29) already takes 20 s, and all instances with p ≥ 37 exceed the 60 s timeout.
In contrast, the reflection-based checker verifies Paley(53) in 3.5 s and Paley(101) in 200 s. The
bottleneck appears to be the compiled checker execution rather than Lean’s kernel, which only
checks the soundness theorem application.
    Beyond independence numbers of Paley graphs, we provide trusted encodings for seven ad-
ditional combinatorial problems. These applications demonstrate the generality of the verified
encoding approach. The underlying theorems are well known; the contribution lies in the end-
to-end formal verification within Lean. Table 3 reports the same pipeline metrics as Table 2.


Table 3: Additional verified combinatorial results, using the reflection-based checker. Column
headers as in Table 2. Dashes indicate a hand-crafted proof (no solver call).

     Problem                      Vars   Cstrs   Solve (ms)    Elab (ms)   Lines   Reflect (ms)
     Langford ¬L(2, 6)             72      463           152         12    223           1 221
     Langford ¬L(2, 9)            162    1 867        12 000        180 44 342         155 000
     Schur S(2) = 4                 6       12            35          4     17             843
     Schur ¬S3 (14)                42      161         <100           4    209             880
     VdW W (2, 3) = 9              10       32            37          4     19             867
     VdW ¬W4 (35)                  36      374         <100           4    429             870
     Ramsey R(3, 3) = 6            15       40            37          4     31             894
     Ramsey ¬R(3, 4) on K9         36      210         3 000         30 25 194          26 000
     Eq. col. χeq (K3,3,1 ) = 5    28      117            72          5    490             957
     PHP ¬PHP(3, 2)                 6        7            —          —      22             815
     Bin packing 12/5/14           60       17         <100           4    687             843



Langford pairing. A Langford pairing of order n places each integer k ∈ {1, . . . , n} into a
sequence of length 2n such that the two occurrences of k are exactly k + 1 positions apart.
Langford pairings exist if and only if n ≡ 0 or 3 (mod 4).
theorem langford6_impossible : $\lnot$hasLangfordPairing 6
theorem langford9_impossible : $\lnot$hasLangfordPairing 9

The impossibility of L(2, 6) is proved from a 223-line kernel proof. The larger instance L(2, 9)
(162 variables, 1 867 constraints) requires a 44 342-line proof and takes about 155 s to verify,
demonstrating that the approach scales to proofs with tens of thousands of steps.

Schur number. A 2-coloring of {1, . . . , n} is Schur-free if no monochromatic triple (a, b, a+b)
exists. The Schur number S(2) is the largest n for which there exists such a coloring.
theorem schur_number_2 : schurNumber 4
theorem schur14_impossible : $\lnot$hasKSchurFreeColoring 3 14



                                                  6
The S(2) lower bound uses the witness coloring {1, 4} 7→ true, {2, 3} 7→ false. The upper
bound ({1, . . . , 5} has no Schur-free coloring) is verified from a 17-line kernel proof. For S(3) =
13, the encoding generalizes to k-colorings using a one-hot representation: k binary variables
per element plus at-least-one and no-monochromatic-triple constraints per color. The resulting
instance (42 variables, 161 constraints) is verified from a 209-line proof.

Van der Waerden number. A 2-coloring of {1, . . . , n} is AP-free if no monochromatic 3-
term arithmetic progression (a, a+d, a+2d) exists. The Van der Waerden number W (2, 3) is the
largest n for which there exists such a coloring.
theorem vdw_number_2_3 : vanDerWaerdenNumber 8
theorem vdw35_impossible : $\lnot$hasKAPFreeColoring 4 35
The W (2, 3) lower bound uses the witness RRBBRRBB; the upper bound ({1, . . . , 9} has no AP-
free coloring) is verified from a 19-line kernel proof. The generalized encoding supports k-term
arithmetic progressions. For W (2, 4) = 35, the upper bound ({1, . . . , 35} has no 2-coloring
avoiding monochromatic 4-APs) is verified from a 429-line proof over 36 variables.

Ramsey number. A 2-coloring of the edges of the complete graph Kn is Ramsey-free if it
contains no monochromatic triangle. The Ramsey number R(3, 3) is the smallest n such that
every 2-coloring of Kn contains a monochromatic triangle.
theorem ramsey_3_3 : ramseyNumber 5
theorem ramsey9_34_impossible :
    $\lnot$hasAsymRamseyFreeColoring 9 3 4

The R(3, 3) lower bound uses the pentagon (C5 ) coloring of K5 . The upper bound—that K6
admits no Ramsey-free coloring—is verified from a 31-line kernel proof. The generalized encod-
ing supports asymmetric Ramsey numbers R(s, t): forbid red Ks and blue Kt separately. For
R(3, 4) ≤ 9, the instance has 36 edge variables and 210 constraints (84 triangle and 126 K4
constraints); the 25 194-line proof verifies in about 26 s.

Equitable chromatic number. A proper k-coloring of a graph G is equitable if all color
classes have size in {⌊n/k⌋, ⌈n/k⌉}. The equitable chromatic number χeq (G) is the smallest
such k. The balance constraints are natively pseudo-Boolean: they express cardinality bounds
as linear inequalities, which would require auxiliary encoding variables in pure SAT.
theorem k331_eq_chromatic : equitableChromaticNumber k331 5

The complete tripartite graph K3,3,1 (7 vertices, 15 edges) has standard chromatic number χ = 3
but equitable chromatic number χeq = 5, demonstrating a gap of 2. The upper bound uses an
explicit 5-coloring witness; the lower bound (¬hasEquitableColoring K3,3,1 4) is verified via the
reflection checker from a 490-line kernel proof with 96 proof-by-contradiction subproofs.

Pigeonhole principle. The pigeonhole principle PHP(m, n) states that m pigeons cannot be
placed into n holes with at most one pigeon per hole when m > n. The proof of ¬PHP(3, 2) uses
the red rule to add a symmetry-breaking constraint (without loss of generality, pigeon 1 goes to
hole 1) via a cyclic substitution witness. This is the only example exercising the redundance rule.
theorem php32_red_reflect : formulaUnsat


Bin packing. Given n items with sizes s0 , . . . , sn−1 and m bins of capacity C, the bin packing
problem asks
           P whether all items can be assigned to bins without exceeding capacity. The capacity
constraint   i si · xi,j ≤ C is a single PB inequality; in CNF it requires a sequential weight
counter encoding [24] with O(n · C) auxiliary variables per bin. Our instance has 12 items


                                                 7
(sizes [10, 9, 8, 8, 6, 5, 4, 4, 4, 4, 4, 4]), 5 bins, and C = 14. The total size equals 5 × 14 = 70, so
total weight alone does not refute feasibility. The instance is not AMO-reducible: pairs like
10 + 4 = 14 and triples like 4 + 4 + 4 = 12 fit in a single bin. Unsatisfiability follows from a
rounding argument: dividing each capacity constraint by 4 shows that each bin holds at most
3 “slots,” heavy items (≥ 8) consume 2 slots and light items (≥ 4) consume 1 slot, giving a total
demand of 2 × 4 + 8 = 16 > 15 = 3 × 5. The PB encoding consists of just 17 constraints over
60 variables; the VeriPB kernel proof has 687 lines. A CNF encoding of the same instance via the
standard sequential weight counter [24] requires 960 variables (900 auxiliary) and 2 617 clauses,
and this encoding overhead grows linearly with the capacity C.
theorem bp12_5_impossible : $\lnot$hasPacking inst12_5



6    Related Work
CakePB [13] provides end-to-end verified subgraph solving in HOL4/CakeML, including both
a PB proof checker and verified graph-problem encoders compiled to a standalone binary. As
discussed in Section 1, the approaches are complementary: CakePB targets standalone verifica-
tion with a small trusted computing base, while PBLean yields Lean theorems that can serve
as lemmas in larger formal developments. Running CakePB on our Paley instances, it checks
Paley(101) in under 1 s; PBLean takes about 200 s. This roughly 200× overhead is the cost of
producing a Lean theorem rather than a standalone verdict. Several extensions of the VeriPB
framework are known, certifying MaxSAT preprocessing [18], solution-improving search [1], dy-
namic programming and decision diagrams [8], and pseudo-Boolean optimization [19].
    An alternative to native PB proof checking is to compile PB reasoning to clausal proofs.
Bryant et al. [5] showed that this is possible via BDD conversion, and their approach efficiently
handles pigeonhole and parity instances via extension variables. Direct VeriPB import provides
a simpler pipeline that works with the native proof format of PB solvers.
    Approaches for SAT certificate checking in theorem provers include Heule et al.’s verified
LRAT checker in ACL2 [16], Lammich’s GRAT in Isabelle/HOL [20], and Lean’s FromLRAT [23],
whose architecture our integration closely follows. Heule and Scheucher [17] established the
empty hexagon theorem via SAT solving with verified proof checking; Subercaseaux et al. [25]
formalized the encoding in Lean and verified the reduction from geometry to SAT.
    Rather than checking proof certificates, one can verify the solver itself. Blanchette et al. [3]
formalized CDCL in Isabelle/HOL as a chain of refinements from abstract calculus to executable
code; Fleury and Lammich [12] extended this to IsaSAT, a verified SAT solver. SMTCoq [9]
imports SMT witnesses into Coq. Besson’s micromega [2] uses reflexive certificate checking for
linear arithmetic in Coq, based on Farkas’ Lemma rather than cutting planes, and does not
import external PB proofs. A related project [22] formalizes general CSP definitions in Lean 4
with verified translations to MiniZinc and SMT-LIB solver formats. PBLean extends verified
PB checking to Lean 4, complementing existing SAT checking in Isabelle and PB checking in
HOL4.


7    Conclusion
We propose a Lean 4 integration for VeriPB pseudo-Boolean proof certificates. The key to
PBLean’s scalability is reflection: a Boolean checker with a fully proved soundness theorem,
evaluated natively by the kernel. As demonstrated in Section 5, this verifies proofs with tens of
thousands of steps that would exhaust memory under explicit proof construction. Our largest
instance, Paley(101) with about 63 000 proof lines, verifies in about 3.5 minutes.
    With trusted encodings, users obtain end-to-end verified combinatorial results: the indepen-
dence number of Paley(101) is a Lean proposition, not an external verdict. This composability,


                                                   8
not directly available with standalone verified checkers, enables PB reasoning to serve as a build-
ing block in larger formalizations.
    Future work includes a veripb tactic for proof automation and integration with other Lean
formalizations.


Acknowledgments
Research was carried out within the Cluster of Excellence Bilateral AI (10.55776/COE12) of the
Austrian Science Funds (FWF).


References
 [1] Jeremias Berg, Bart Bogaerts, Jakob Nordström, Andy Oertel, Tobias Paxian, and Dieter
     Vandesande. Certifying without loss of generality reasoning in solution-improving maximum
     satisfiability. In Paul Shaw, editor, 30th International Conference on Principles and Practice
     of Constraint Programming, CP 2024, Girona, Spain, September 2-6, 2024, volume 307 of
     LIPIcs, pages 4:1–4:28. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2024. URL:
     https://doi.org/10.4230/LIPIcs.CP.2024.4, doi:10.4230/LIPICS.CP.2024.4.
 [2] Frédéric Besson. Fast reflexive arithmetic tactics the linear case and beyond. In Thorsten
     Altenkirch and Conor McBride, editors, Types for Proofs and Programs, International
     Workshop, TYPES 2006, Nottingham, UK, April 18-21, 2006, Revised Selected Papers,
     volume 4502 of Lecture Notes in Computer Science, pages 48–62. Springer, 2006. doi:
     10.1007/978-3-540-74464-1\_4.
 [3] Jasmin Christian Blanchette, Mathias Fleury, Peter Lammich, and Christoph Weidenbach.
     A verified SAT solver framework with learn, forget, restart, and incrementality. J. Autom.
     Reason., 61(1-4):333–365, 2018. URL: https://doi.org/10.1007/s10817-018-9455-7,
     doi:10.1007/S10817-018-9455-7.
 [4] Bart Bogaerts, Stephan Gocht, Ciaran McCreesh, and Jakob Nordström. Certified symmetry
     and dominance breaking for combinatorial optimisation. In Thirty-Sixth AAAI Conference
     on Artificial Intelligence, AAAI 2022, Thirty-Fourth Conference on Innovative Applications
     of Artificial Intelligence, IAAI 2022, The Twelveth Symposium on Educational Advances
     in Artificial Intelligence, EAAI 2022 Virtual Event, February 22 - March 1, 2022, pages
     3698–3707. AAAI Press, 2022. URL: https://doi.org/10.1609/aaai.v36i4.20283, doi:
     10.1609/AAAI.V36I4.20283.
 [5] Randal E. Bryant, Armin Biere, and Marijn J. H. Heule. Clausal proofs for pseudo-boolean
     reasoning. In Dana Fisman and Grigore Rosu, editors, Tools and Algorithms for the Con-
     struction and Analysis of Systems - 28th International Conference, TACAS 2022, Held as
     Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2022,
     Munich, Germany, April 2-7, 2022, Proceedings, Part I, volume 13243 of Lecture Notes in
     Computer Science, pages 443–461. Springer, 2022. doi:10.1007/978-3-030-99524-9\_25.
 [6] William J. Cook, Collette R. Coullard, and György Turán. On the complexity of cutting-
     plane proofs. Discret. Appl. Math., 18(1):25–38, 1987. doi:10.1016/0166-218X(87)
     90039-4.
 [7] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming
     language. In André Platzer and Geoff Sutcliffe, editors, Automated Deduction - CADE 28
     - 28th International Conference on Automated Deduction, Virtual Event, July 12-15, 2021,
     Proceedings, volume 12699 of Lecture Notes in Computer Science, pages 625–635. Springer,
     2021. doi:10.1007/978-3-030-79876-5\_37.


                                                9
 [8] Emir Demirovic, Ciaran McCreesh, Matthew J. McIlree, Jakob Nordström, Andy Oertel,
     and Konstantin Sidorov. Pseudo-boolean reasoning about states and transitions to cer-
     tify dynamic programming and decision diagram algorithms. In Paul Shaw, editor, 30th
     International Conference on Principles and Practice of Constraint Programming, CP 2024,
     Girona, Spain, September 2-6, 2024, volume 307 of LIPIcs, pages 9:1–9:21. Schloss Dagstuhl -
     Leibniz-Zentrum für Informatik, 2024. URL: https://doi.org/10.4230/LIPIcs.CP.2024.
     9, doi:10.4230/LIPICS.CP.2024.9.
 [9] Burak Ekici, Alain Mebsout, Cesare Tinelli, Chantal Keller, Guy Katz, Andrew Reynolds,
     and Clark W. Barrett. Smtcoq: A plug-in for integrating SMT solvers into coq. In Rupak
     Majumdar and Viktor Kuncak, editors, Computer Aided Verification - 29th International
     Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017, Proceedings, Part II, volume
     10427 of Lecture Notes in Computer Science, pages 126–133. Springer, 2017. doi:10.1007/
     978-3-319-63390-9\_7.
[10] Jan Elffers, Stephan Gocht, Ciaran McCreesh, and Jakob Nordström. Justifying all dif-
     ferences using pseudo-boolean reasoning. In The Thirty-Fourth AAAI Conference on Ar-
     tificial Intelligence, AAAI 2020, The Thirty-Second Innovative Applications of Artificial
     Intelligence Conference, IAAI 2020, The Tenth AAAI Symposium on Educational Ad-
     vances in Artificial Intelligence, EAAI 2020, New York, NY, USA, February 7-12, 2020,
     pages 1486–1494. AAAI Press, 2020. URL: https://doi.org/10.1609/aaai.v34i02.5507,
     doi:10.1609/AAAI.V34I02.5507.
[11] Jan Elffers and Jakob Nordström. Divide and conquer: Towards faster pseudo-boolean
     solving. In Jérôme Lang, editor, Proceedings of the Twenty-Seventh International Joint
     Conference on Artificial Intelligence, IJCAI 2018, July 13-19, 2018, Stockholm, Sweden,
     pages 1291–1299. ijcai.org, 2018. URL: https://doi.org/10.24963/ijcai.2018/180, doi:
     10.24963/IJCAI.2018/180.
[12] Mathias Fleury and Peter Lammich. A more pragmatic CDCL for isasat and targetting
     LLVM (short paper). In Brigitte Pientka and Cesare Tinelli, editors, Automated Deduction
     - CADE 29 - 29th International Conference on Automated Deduction, Rome, Italy, July
     1-4, 2023, Proceedings, volume 14132 of Lecture Notes in Computer Science, pages 207–219.
     Springer, 2023. doi:10.1007/978-3-031-38499-8\_12.
[13] Stephan Gocht, Ciaran McCreesh, Magnus O. Myreen, Jakob Nordström, Andy Oer-
     tel, and Yong Kiam Tan. End-to-end verification for subgraph solving. In Michael J.
     Wooldridge, Jennifer G. Dy, and Sriraam Natarajan, editors, Thirty-Eighth AAAI Con-
     ference on Artificial Intelligence, AAAI 2024, Thirty-Sixth Conference on Innovative Ap-
     plications of Artificial Intelligence, IAAI 2024, Fourteenth Symposium on Educational Ad-
     vances in Artificial Intelligence, EAAI 2024, February 20-27, 2024, Vancouver, Canada,
     pages 8038–8047. AAAI Press, 2024. URL: https://doi.org/10.1609/aaai.v38i8.28642,
     doi:10.1609/AAAI.V38I8.28642.
[14] Stephan Gocht and Jakob Nordström. Certifying parity reasoning efficiently using pseudo-
     boolean proofs. In Thirty-Fifth AAAI Conference on Artificial Intelligence, AAAI 2021,
     Thirty-Third Conference on Innovative Applications of Artificial Intelligence, IAAI 2021,
     The Eleventh Symposium on Educational Advances in Artificial Intelligence, EAAI 2021,
     Virtual Event, February 2-9, 2021, pages 3768–3777. AAAI Press, 2021. URL: https:
     //doi.org/10.1609/aaai.v35i5.16494, doi:10.1609/AAAI.V35I5.16494.
[15] Armin Haken. The intractability of resolution. Theor. Comput. Sci., 39:297–308, 1985.
     doi:10.1016/0304-3975(85)90144-6.



                                               10
[16] Marijn Heule, Warren A. Hunt Jr., Matt Kaufmann, and Nathan Wetzler. Efficient, verified
     checking of propositional proofs. In Mauricio Ayala-Rincón and César A. Muñoz, editors,
     Interactive Theorem Proving - 8th International Conference, ITP 2017, Brasília, Brazil,
     September 26-29, 2017, Proceedings, volume 10499 of Lecture Notes in Computer Science,
     pages 269–284. Springer, 2017. doi:10.1007/978-3-319-66107-0\_18.

[17] Marijn J. H. Heule and Manfred Scheucher. Happy ending: An empty hexagon in ev-
     ery set of 30 points. In Bernd Finkbeiner and Laura Kovács, editors, Tools and Al-
     gorithms for the Construction and Analysis of Systems - 30th International Conference,
     TACAS 2024, Held as Part of the European Joint Conferences on Theory and Practice
     of Software, ETAPS 2024, Luxembourg City, Luxembourg, April 6-11, 2024, Proceedings,
     Part I, volume 14570 of Lecture Notes in Computer Science, pages 61–80. Springer, 2024.
     doi:10.1007/978-3-031-57246-3\_5.
[18] Hannes Ihalainen, Andy Oertel, Yong Kiam Tan, Jeremias Berg, Matti Järvisalo, Mag-
     nus O. Myreen, and Jakob Nordström. Certified MaxSAT preprocessing. In Christoph
     Benzmüller, Marijn J. H. Heule, and Renate A. Schmidt, editors, Automated Reasoning -
     12th International Joint Conference, IJCAR 2024, Nancy, France, July 3-6, 2024, Proceed-
     ings, Part I, volume 14739 of Lecture Notes in Computer Science, pages 396–418. Springer,
     2024. doi:10.1007/978-3-031-63498-7\_24.
[19] Wietze Koops, Daniel Le Berre, Magnus O. Myreen, Jakob Nordström, Andy Oertel,
     Yong Kiam Tan, and Marc Vinyals. Practically feasible proof logging for pseudo-boolean
     optimization. In Maria Garcia de la Banda, editor, 31st International Conference on
     Principles and Practice of Constraint Programming, CP 2025, Glasgow, Scotland, Au-
     gust 10-15, 2025, volume 340 of LIPIcs, pages 21:1–21:27. Schloss Dagstuhl - Leibniz-
     Zentrum für Informatik, 2025. URL: https://doi.org/10.4230/LIPIcs.CP.2025.21,
     doi:10.4230/LIPICS.CP.2025.21.
[20] Peter Lammich. The GRAT tool chain - efficient (UN)SAT certificate checking with formal
     correctness guarantees. In Serge Gaspers and Toby Walsh, editors, Theory and Applica-
     tions of Satisfiability Testing - SAT 2017 - 20th International Conference, Melbourne, VIC,
     Australia, August 28 - September 1, 2017, Proceedings, volume 10491 of Lecture Notes in
     Computer Science, pages 457–463. Springer, 2017. doi:10.1007/978-3-319-66263-3\_29.
[21] Lean Contributors. bv_decide: Verified bitvector reasoning in Lean 4. https://github.
     com/leanprover/lean4, 2024. Std.Tactic.BVDecide.
[22] Pablo Manrique Merchan and Stefan Szeider. LeanCSP: Verified constraint satisfaction in
     Lean 4. https://github.com/leansolving/leancsp, 2025.
[23] Mathlib Contributors. FromLRAT: LRAT proof checking in Lean 4. https://github.com/
     leanprover-community/mathlib4, 2024. Mathlib.Tactic.Sat.FromLRAT.

[24] Tobias Philipp and Peter Steinke. PBLib – A library for encoding pseudo-boolean constraints
     into CNF. In Theory and Applications of Satisfiability Testing – SAT 2015, Lecture Notes
     in Computer Science, pages 9–16. Springer, 2015. doi:10.1007/978-3-319-24318-4\_2.
[25] Bernardo Subercaseaux, Wojciech Nawrocki, James Gallicchio, Cayden R. Codel, Mario
     Carneiro, and Marijn J. H. Heule. Formal verification of the empty hexagon number. In
     Yves Bertot, Temur Kutsia, and Michael Norrish, editors, 15th International Conference on
     Interactive Theorem Proving, ITP 2024, Tbilisi, Georgia, September 9-14, 2024, volume 309
     of LIPIcs, pages 35:1–35:19. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2024. URL:
     https://doi.org/10.4230/LIPIcs.ITP.2024.35, doi:10.4230/LIPICS.ITP.2024.35.



                                              11
[26] Marc Vinyals, Jan Elffers, Jesús Giráldez-Cru, Stephan Gocht, and Jakob Nordström. In
     between resolution and cutting planes: A study of proof systems for pseudo-boolean SAT
     solving. In Olaf Beyersdorff and Christoph M. Wintersteiger, editors, Theory and Applica-
     tions of Satisfiability Testing - SAT 2018 - 21st International Conference, SAT 2018, Held as
     Part of the Federated Logic Conference, FloC 2018, Oxford, UK, July 9-12, 2018, Proceed-
     ings, volume 10929 of Lecture Notes in Computer Science, pages 292–310. Springer, 2018.
     doi:10.1007/978-3-319-94144-8\_18.




                                               12
