                                                Building Shor’s Algorithm in Lean:
                                                An Agentic Formalization of Quantum
                                                Attacks on RSA-2048 and P-256


                                                                        Lei Zhang∗1,2 , Yusheng Zhao1 , Hongshun Yao1,2 , and Xin Wang†2
                                                                                   1
                                                                                     QudeLeap Research, Shanghai 200030, China
                                                          2
                                                              The Hong Kong University of Science and Technology (Guangzhou), Guangdong 511453, China

                                                                                        github.com/QudeLeap/Lean-QuantumAlg


                                                                                                      Abstract
                                                          Large language models are increasingly assisting with demanding formal theorem-proving tasks,
                                                      particularly when grounded in machine-checked libraries such as Lean. Agentic systems further amplify
arXiv:2607.14082v1 [quant-ph] 15 Jul 2026




                                                      this process by searching, reusing, and extending existing formal developments to uncover new discoveries.
                                                      In quantum computing, Shor’s algorithm and its variants present such a demanding case for Lean
                                                      formalization. In this work, we formalize this algorithm family in Lean through agentic formalization:
                                                      software agents analyze sources, write Lean code and repair proofs, with human review of the scientific
                                                      claims and machine checking of the resulting formal proofs. Our formalization develops the mathematical
                                                      foundations for analyzing quantum attacks in two cryptographic settings: a 2048-bit modulus in the
                                                      RSA-2048 and the standardized elliptic curve over a 256-bit prime field (P-256). To support these analyses,
                                                      the formalization ranges from quantum algorithms for order finding to reversible quantum circuits for
                                                      modular and elliptic-curve arithmetic. Based on [Quantum 5, 433] and [ASIACRYPT 2017, 241–270],
                                                      we formalize the logical resource estimates for RSA-2048 and P-256, respectively, and provide additional
                                                      estimates of classical operations. We expect the results pave the way for broader machine-checked quantum
                                                      cryptanalysis and represent a step toward AI-assisted design and verification of quantum algorithms.


                                                1 Introduction
                                                Formalizing quantum algorithms is important because their application-level claims connect mathematical
                                                guarantees, circuit behavior, success probabilities, classical post-processing, and resource estimates. The field
                                                spans algebraic algorithms and search [1, 2, 3], as well as quantum simulation and scientific computation [4].
                                                In each area, abstract arguments interact with choices of representation, subroutines, measurement, and
                                                repetition that determine what an algorithm returns and how its cost scales. A machine-checked development
                                                records these links as explicit definitions and theorems, giving researchers a precise basis for comparing
                                                constructions and extending them.
                                                    Shor’s algorithm [5] is a demanding test case for this proof chain because it gives polynomial-time quantum
                                                procedures for integer factorization and discrete logarithms. Factorization underlies the Rivest–Shamir–
                                                Adleman (RSA) cryptosystem [6]; factoring a 2048-bit public modulus exposes the prime factors needed to
                                                derive the RSA-2048 private key. The elliptic-curve discrete-logarithm problem asks for the private scalar that
                                                maps a public base point to a public key [7]. P-256 [8] is the 256-bit prime-field curve standardized by the
                                                National Institute of Standards and Technology. Both problems admit a hidden-subgroup interpretation [9, 10].
                                                Their cryptographic instances connect quantum sampling with number theory, reversible arithmetic, classical
                                                recovery, probability analysis, and resource accounting.
                                                    Existing formal verification results establish increasingly broad portions of Shor’s algorithm. Ref. [11]
                                                presents Qbricks and uses it to verify a parameterized order-finding circuit, a success bound, and asymptotic
                                                circuit resources. Ref. [12] verifies a hybrid factorization program with classical and quantum variables,
                                                including a lower bound on factor-recovery success, while representing controlled modular exponentiation as an
                                                abstract unitary. Ref. [13] presents Qafny and verifies Shor order finding, continued-fraction post-processing,
                                                and its probability calculation under a specified modular-multiplication behavior. Ref. [14] certifies a factoring
                                            ∗   leizhang116.4@gmail.com
                                            †   felixxinwang@hkust-gz.edu.cn
Lean-QuantumAlg                                                                                 QudeLeap Research



implementation that connects reversible modular multiplication, quantum phase estimation, measurement,
continued fractions, classical factor recovery, success probability, and gate counts.
    These developments also motivate a reusable mathematical layer for studying new quantum algorithms
and variants. For Shor’s algorithm, that layer includes reductions from cryptographic problems, distributions
of quantum measurement outcomes, probability bounds for recoverable events, reversible arithmetic, classical
recovery, and resource formulas. Stable names and module locations make the assumptions and conclusions of
each component visible. Researchers can then retrieve an intermediate theorem, inspect its dependencies,
compare related formulations, and assemble the checked components into another analysis while retaining a
trace from the final claim to its mathematical premises.
    Lean provides a common language for executable definitions, mathematical structures, and checked proofs.
Its libraries place general mathematics and computer-science foundations in Mathlib [15] and CSLib [16].
Lean-QIT [17] extends this ecosystem with finite-dimensional quantum information theory, supplying a
foundation for formal quantum developments. LeanDojo [18] gives agents programmatic access to Lean
repositories and proof states. Together, checked libraries and repository interfaces allow agents to locate
relevant statements, retrieve their assumptions, and reuse verified components. This combination supports
a quantum-algorithm library in which mathematical arguments, circuit properties, probability claims, and
resource formulas share one proof language.
    In this work, we formalize mathematical reductions and selected quantum circuit components used to
analyze RSA-2048 factorization and P-256 scalar recovery in Lean. The RSA branch develops order finding,
factor recovery, reversible modular arithmetic, and the Ekerå–Håstad route [19]. The P-256 branch develops
discrete logarithms in finite cyclic groups, prime-field arithmetic, elliptic-curve operations, and scalar recovery.
These branches expose reusable statements for number theory, probability, reversible circuits, classical post-
processing, and resource accounting. To the best of our knowledge, this is the first Lean development to give a
machine-checked P-256 scalar-recovery statement with a quantitative success bound and logical resource values.
We constructed the library through agentic formalization [20]: agents researched sources, decomposed claims,
wrote Lean code, and repaired proofs; human review covered scientific statements and source alignment; and
machine checking verified the resulting formal proofs. The resulting organization provides a Lean foundation
for further machine-checked studies of quantum algorithms and their cryptographic applications.


2 Main Results
This section presents the two application-level results of the formalization. The first concerns factorization
of the public modulus used by the 2048-bit Rivest–Shamir–Adleman system, called RSA-2048. The second
concerns recovery of the private scalar associated with a public point on P-256. In each case, we begin with
the public cryptographic data, formulate the computational problem, and follow the quantum and classical
stages that lead to the requested output. The resulting theorem states the success guarantee and resource
profile, and the accompanying table places that result beside earlier analyses. The later sections on formalizing
RSA-2048 and P-256 develop the number-theoretic reductions, reversible arithmetic, and recovery procedures
used along these two routes.
    Both results use a logical-circuit resource model. The resource profiles count logical qubits, Toffoli gates,
and the depth quantity reported by the corresponding source. For P-256, Ref. [7] reports maximal Toffoli-gate
depth. For one RSA-2048 run, Ref. [21] reports measurement depth. Circuit noise, quantum error correction,
scheduling, and physical resources require additional models beyond these logical profiles. Each success
probability refers to recovery of the output specified by the relevant problem, and each classical-operation
count records the abstract arithmetic steps in the associated recovery procedure.

2.1 RSA-2048
The RSA cryptosystem [6] publishes a modulus N = pq formed from two secret primes p and q. RSA-2048
fixes the binary length of N to 2048 bits. The attacker receives N and seeks a value d equal to either p or q;
division by d then gives the other prime. Recovering this factorization provides the secret number-theoretic
data needed to derive the corresponding private key. The application-level input and output are therefore
captured by the following problem.

Problem 1 (Integer Factorization) Let p and q be unknown distinct primes, and let N = pq be known.
Given N , find d ∈ {p, q}.
   Problem 1 gives the finish line for the algorithm: one nontrivial factor of N . Shor’s factoring algorithm [5]
reaches this output through order finding. For a selected residue a coprime to N , the quantum stage determines
the period of repeated multiplication by a modulo N . A suitable even period makes the powers immediately


                                                         2
Lean-QuantumAlg                                                                                 QudeLeap Research




Table 1: A comparison of some results that estimate the logical resources required to solve the integer-
factorization problem for RSA-2048, without considering circuit noise. Here n denotes the bit length of the
RSA-2048 modulus.

   Result                          Logical resources                              Success probability
   Asymptotic analysis [5]         O(n) qubits                                    High probability after repe-
                                   O(n3 ) elementary gates                        tition
   Gate-level estimate [21]        6.19 × 103 qubits                              ≥ 99% classical recovery
                                   2.7 × 109 Toffoli gates                        conditional on a correct
                                   2.14 × 109 measurement depth per run           quantum run
   Lean-formalized                 6.19 × 103 qubits                              ≥ 2/3
   (Ours; Theorem 1)               8.1 × 109 Toffoli gates
                                   6.42 × 109 maximal circuit depth
                                   3.69×104 classical arithmetic operations


before the return to 1 reveal two candidates whose greatest common divisors with N yield the prime factors.
Reversible modular addition, multiplication, and exponentiation implement the periodic action coherently,
and the classical stage converts a recoverable measurement result into the requested value d.
    One factoring attempt follows this reduction as a sequence of transformations. A superposition of exponents
controls modular exponentiation, so exponents separated by the unknown period produce the same modular
value. Measuring the quantum registers then provides numerical information from which continued fractions
reconstruct a candidate period. The classical stage validates that candidate by checking the modular power
relation and tests the associated greatest common divisors. A recoverable candidate yields d; another outcome
starts a new attempt. This data flow links the public modulus to a periodic circuit, the circuit to a candidate
order, and the candidate order to a prime factor.
    The formalization follows two routes to this common factoring goal. The textbook Shor route supplies
the order-finding and factor-recovery analysis used to express success under repetition. The Ekerå–Håstad
short-discrete-logarithm construction analyzed in Ref. [21] supplies the concrete RSA-2048 logical-circuit
baseline. One run uses 6190 live logical qubits, 2.7 × 109 Toffoli gates, and 2.14 × 109 measurement depth,
and its classical post-processing recovers the factors with probability above 99% conditional on a correct
quantum run. The three-trial calculation assigns each factoring attempt failure probability at most one half.
Independence then reduces the joint failure probability to at most 1/8, which meets the target of at most 1/3.
Sequential execution preserves the live-qubit footprint and triples both the Toffoli count and the reported
depth.
    The resulting success event is the return of a value d ∈ {p, q}. The repeated-trial calculation gives
probability at least 2/3. Applying the one-run values reported in Ref. [21] to the same three attempts
preserves the peak logical-qubit count and triples the Toffoli count and depth. The recovery bookkeeping
adds an exact count of abstract classical arithmetic operations. Theorem 1 collects the resulting values.

Theorem 1 (RSA-2048) Suppose an RSA-2048 public key has known public modulus N , whose private
prime factors are unknown distinct primes p and q. There exists a quantum algorithm that returns d ∈ {p, q}
with probability at least 2/3, using 6.19 × 103 logical qubits, 8.1 × 109 Toffoli gates, 6.42 × 109 maximal circuit
depth, and 3.69 × 104 classical arithmetic operations.

    Theorem 1 combines the cryptographic output in Problem 1 with an explicit success threshold and a
concrete resource profile. Its quantum resources describe three sequential attempts, and its classical count
describes the arithmetic recovery steps recorded for those attempts. The later section on formalizing RSA-2048
starts from the period-finding reduction, builds the reversible modular-arithmetic path, and then presents the
Shor and Ekerå–Håstad recovery procedures that support this application-level statement.
    Table 1 shows the progression from an asymptotic factoring algorithm to an RSA-2048 gate-level estimate
and then to the application statement in Theorem 1. The first two rows establish the algorithmic scaling
and the concrete one-run circuit baseline. The final row adds an explicit repeated-run success threshold, the
corresponding aggregate logical resources, and a classical recovery count in one machine-checked result.




                                                         3
Lean-QuantumAlg                                                                                QudeLeap Research



2.2 P-256
P-256 [8] is a standardized elliptic curve E over a 256-bit prime field Fp . Its public domain parameters include
a base point P that generates a subgroup of prime order r. A private scalar m ∈ Zr determines the public
point Q = [m]P , where [m]P denotes scalar multiplication on the curve. The attacker receives the curve
parameters, P , Q, and r, and seeks the scalar m that links the two public points. This input-output relation
gives the P-256 instance of the elliptic-curve discrete-logarithm problem.

Problem 2 (Elliptic-Curve Discrete Logarithm) Let E/Fp be an elliptic curve, let P ∈ E(Fp ) have
prime order r, and let Q = [m]P for an unknown m ∈ Zr . Given (E, p, P, Q, r), find m.
    Problem 2 asks the algorithm to invert the scalar action that produced Q. The elliptic-curve construction
described in Ref. [22] begins by placing pairs of candidate scalars in superposition and coherently evaluating
the corresponding combinations of P and Q. Different pairs can produce the same curve point because Q
already contains the hidden multiplier m. Quantum interference concentrates the subsequent measurement
outcomes on relations determined by this multiplier. Classical post-processing reads a recoverable relation
and solves for m, turning information exposed by the quantum stage into the output required by the problem.
    The useful measurement information comes from entire families of scalar pairs that reach the same curve
point. Coherent point evaluation preserves the relation among these pairs until the point register is measured.
The two scalar registers then retain a shared dependence on the hidden multiplier, and their interference makes
this dependence visible as correlated measurement values. Classical recovery checks whether the observed
relation can be solved and performs the required modular arithmetic when it can. The algorithm therefore
moves from public curve data to a coherent group action, from that action to correlated measurement values,
and from those values to the private scalar.
    The coherent group evaluation becomes a circuit through three layers of arithmetic. Reversible operations
in Fp implement the additions, multiplications, squarings, and inversions used by affine curve formulas. These
field operations compose into controlled point additions, and schedules of controlled additions implement
scalar multiplication from the two superposed index registers. Ref. [7] analyzes this gate-level construction for
P-256 and reports 2330 logical qubits, 1.26 × 1011 Toffoli gates, and maximal Toffoli-gate depth 1.16 × 1011 .
After a recoverable measurement outcome is obtained, the direct scalar-recovery bookkeeping uses seven
abstract classical operations.
    For the P-256 result, success means that the returned value equals the scalar m in the public relation
Q = [m]P . The quantitative profile assigns this event probability at least 2/3 and records one run of the
logical circuit together with the direct classical recovery. The following theorem packages that application-level
output, probability, and resource statement.

Theorem 2 (P-256) Suppose a P-256 instance has known base point P of prime order r and known public
key point Q = [m]P for unknown private scalar m. There exists a quantum algorithm that returns m with
probability at least 2/3, using 2.33×103 logical qubits, 1.26×1011 Toffoli gates, 1.16×1011 maximal Toffoli-gate
depth, and 7 classical operations.
    Theorem 2 connects the public-point relation in Problem 2 to a quantitative scalar-recovery guarantee. Its
resource tuple follows the reversible circuit from prime-field arithmetic through controlled curve operations,
and its classical count begins when the quantum measurement has supplied a recoverable relation. The later
section on formalizing P-256 develops these layers in order: the generic discrete-logarithm argument, reversible
prime-field arithmetic, elliptic-curve point operations, scalar multiplication, and final recovery.
    Table 2 moves from an approximate elliptic-curve construction to a simulated gate-level P-256 estimate
and finally to Theorem 2. The comparison shows how success and resource accounting become progressively
more explicit across the three levels. The final row collects the concrete logical-circuit profile, the stated
recovery probability, and the direct classical-operation count in the formalized application result.


3 Formalizing Quantum Algorithm Proofs
3.1 Agentic Formalization
Agentic formalization is a workflow in which software agents conduct substantive source research and proof
development, human review examines the mathematical claims and their alignment with cited sources, and
machine checking verifies the resulting formal proofs. Software agents may propose definitions, theorem
statements, proofs, and revisions, while authors decide which claims and changes enter the project. Machine
checking establishes that a proof has the stated Lean type under the imported definitions and assumptions.
We use the term only for this supervised division of work.


                                                        4
Lean-QuantumAlg                                                                               QudeLeap Research




Table 2: A comparison of some results that estimate the resources required to solve the elliptic-curve discrete-
logarithm problem for P-256, without considering circuit noise.

   Result                         Logical resources                             Success probability
   Approximate analysis [22]      ≈ 1.5 × 103 qubits                            Close to 1
                                  ≈ 1.81 × 1010 Toffoli gates
   Gate-level estimate [7]        2.33 × 103 qubits                             Close to 1
                                  1.26 × 1011 Toffoli gates
                                  1.16 × 1011 maximal Toffoli-gate depth
   Lean-formalized                2.33 × 103 qubits                             ≥ 2/3
   (Ours; Theorem 2)              1.26 × 1011 Toffoli gates
                                  1.16 × 1011 maximal Toffoli-gate depth
                                  7 classical operations


    The workflow begins when authors select a scientific question and the sources that should support it.
Software agents retrieve the relevant source passages, separate a claim into mathematical and computational
obligations, and construct Lean declarations for those obligations. The Lean kernel then checks the proof
terms. Authors inspect the formal assumptions, compare the checked statement with the source, and review
the corresponding manuscript language before accepting a change. The accepted declarations, source locations,
review decisions, and manuscript claims form the artifacts passed to the next stage. Figure 1 in Appendix A
summarizes this sequence, marks the trust boundary, and assigns responsibility for each artifact.
    Stable names and module locations make a formal library usable by software agents. An agent can locate
a statement, retrieve its dependencies and assumptions, compare its conclusion with a cited claim, and reuse
the checked result in a later construction. This organization also gives reviewers a path from manuscript prose
to a precise theorem and from that theorem to the definitions on which it depends. Appendix B maps the
RSA-2048 and P-256 claims to their final theorems and states each theorem’s assumptions and conclusion.

3.2 Formal Verification Results
Table 3 compares selected formal developments of Shor’s factoring algorithm. The first column identifies
the development. The remaining columns ask whether the formal scope reaches factor recovery, whether the
development proves a quantitative success bound for the endpoint it formalizes, whether it analyzes quantum
and classical resources, and whether it constructs the quantum computation at gate level. The oracle column
records an implementation boundary: it names any arithmetic operation left as an abstract oracle and reports
“None” when the arithmetic is constructed. The check marks describe properties established inside the formal
development. A check mark denotes complete coverage of the stated field, a partial mark denotes coverage of
part of that field, and a cross denotes absent coverage.
    In the order shown, Ref. [11] presents Qbricks and uses it to construct and verify the order-finding circuit,
prove a lower bound on the phase measurement probability, and derive symbolic gate and width formulas.
The Qbricks formal result ends before continued fractions and factor recovery, and it constructs the required
modular arithmetic. Ref. [12] verifies the hybrid control flow and factor recovery success using quantum
Hoare logic [23] for programs with classical and quantum variables, with controlled modular exponentiation
represented as an abstract unitary. Ref. [24] extends this program logic with quantum arrays and parameterized
gates. Ref. [13] presents Qafny and uses it to verify the order-finding state evolution, continued-fraction
post-processing, and probability calculation, while modular multiplication remains at an abstract arithmetic
boundary in the verified Shor chain. Coq [25] provides the proof-assistant setting for the final row among
the prior developments, and CoqQ [26] supplies a deeply embedded quantum programming language with a
machine-checked soundness proof. Ref. [14] constructs a reversible modular multiplier that overwrites its input
register. A verified generic control transformation supplies the controlled instances used by phase estimation,
so the oracle column records “None.” The Coq development connects measurement, continued fractions, factor
recovery, repetition, and quantum gate bounds. Its classical resource analysis bounds continued-fraction
iterations and repeated trials. The Lean row has declarations checked by the Lean kernel in every table
category and constructs modular arithmetic circuits, so its oracle column records “None.” The checks in this
row record category coverage. Local arithmetic results connect gate-level behavior and resource counts for
the same circuit. At the terminal RSA-2048 statement, the success bound, the repository count of classical
arithmetic steps, and the quantum resource tuple reported in Ref. [21] enter through separate certificates. A
future integration step will derive all terminal fields from a circuit execution whose input consists only of the


                                                       5
Lean-QuantumAlg                                                                                 QudeLeap Research




Table 3: A comparison of some formal verification results for Shor’s factoring algorithm. Here “Oracle
assumption” lists an arithmetic oracle left unimplemented; ✓and −indicate complete and partial coverage,
respectively; ✗ indicates a property not established.

                                         Success     Quantum     Classical   Gate-level
  Formal development     End-to-end                                                         Oracle assumption
                                       probability   resource    resource     circuit
  Qbricks [11]               ✗             ✓            ✓           ✗            ✓                None
  Hoare logic [12]           −             ✓            ✗           ✗            ✗        Modular exponentiation
  Qafny [13]                 ✗             ✓            ✗           ✗            ✗        Modular multiplication
  Coq [14]                   ✓             ✓            ✓           −            ✓                None
  Lean (Ours)                ✓             ✓            ✓           ✓            ✓                None



public modulus.
    Our organizational target is a library in which mathematical reductions, probability bounds, reversible
circuits, classical recovery, and resource statements can be located and reused independently. The RSA-2048
branch provides declarations in each of these categories and makes their current points of assembly explicit.
The same organization extends beyond factoring: the P-256 branch combines discrete-logarithm recovery in
a finite cyclic group with prime-field arithmetic, elliptic-curve operations, and a logical resource statement.
The next two sections present these branches from their computational problems through their quantitative
application results.


4 Formalizing RSA-2048
4.1 Order Finding
Write N = pq for the modulus in Problem 1, and choose a residue a with 1 < a < N . Computing gcd(a, N )
already returns a factor when the greatest common divisor exceeds one. Otherwise, a is a unit modulo N ,
and its multiplicative order r is the least positive integer satisfying ar ≡ 1 (mod N ). Shor’s reduction [5] asks
the quantum subroutine to recover this period. The reduction thereby replaces an unstructured search for p
or q with the periodic action of multiplication by a on residues modulo N .
    Suppose that r is even. The identity ar − 1 = (ar/2 − 1)(ar/2 + 1) implies that N divides the product on the
right. Minimality of r gives ar/2 ̸≡ 1 (mod N ), while the additional condition ar/2 ̸≡ −1 (mod N ) prevents
either factor from vanishing modulo N . Consequently, at least one of gcd(ar/2 − 1, N ) and gcd(ar/2 + 1, N ) is
a nontrivial factor of the semiprime. This is the classical conversion used after the order has been recovered.
    A good base is a sampled residue a with gcd(a, N ) = 1, even order r, and ar/2 ̸≡ −1 (mod N ). At least
one half of the units modulo a product of two distinct odd primes are good [5]. For a uniformly sampled base,
this path contributes at least the probability of sampling a good base multiplied by the conditional probability
that the quantum measurement and continued-fraction step recover the relevant order. Independent repetitions
then amplify the resulting success probability.
    Hadamard gates make the phase register range uniformly over exponents x, and controlled modular
multiplication computes ax mod N coherently in the work register. Quantum phase estimation and the inverse
quantum Fourier transform [27, 2, 4, 28] convert this periodicity into a phase-register measurement near a
multiple of 2t /r. Continued fractions turn the measured ratio j/2t into a candidate denominator, and modular
exponentiation retains it only if the corresponding power returns to one. Algorithm 1 gives the complete
schedule. The candidate is exact when it equals the least positive period r.
    The work register decomposes into eigenstates of modular multiplication, with eigenphases s/r for
numerators s ∈ {0, . . . , r − 1}. Phase estimation concentrates a measured integer j near 2t s/r [5]. The register
window N 2 ≤ 2t < 2N 2 and the inequality r < N make recoverable outcomes satisfy |j/2t − s/r| < 1/(2r2 ).
For r > 0 and gcd(s, r) = 1, this approximation makes s/r a continued-fraction convergent whose reduced
denominator is r. Exact recovery therefore uses outcomes whose numerators are coprime to r; a different
sample may produce a multiple of the order or fail the validation check.
    There are φ(r) numerators in {0, . . . , r − 1} that are coprime to r, where φ is Euler’s totient function.
Summing their recoverable measurement events and averaging over the eigenphases in the work register yields
the lower bound φ(r)/(3r) for one order-finding sample. Success means that continued-fraction validation
returns the least positive exponent r. Reaching a failure probability of at most one half requires repeated
samples. The RSA-2048 totals still require a specified number of samples and the corresponding cost within



                                                        6
Lean-QuantumAlg                                                                              QudeLeap Research



 Algorithm 1: Quantum order finding with continued-fraction validation [5]
   Input : Modulus N > 1, residue a with gcd(a, N ) = 1, phase width t satisfying N 2 ≤ 2t < 2N 2
   Output : An accepted positive candidate r′ , or failure
                                           ⊗t
 1 Prepare a t-qubit phase register in |0⟩    and a work register in |1⟩;
 2 Apply a Hadamard gate to every phase qubit;
 3 Index the phase qubits by significance, with i = 0 least significant;
 4 for i ← 0 to t − 1 do
                                                                      i
 5    Controlled on phase qubit i, multiply the work register by a2 mod N ;
 6 Apply the inverse quantum Fourier transform to the phase register;
 7 Measure the phase register as j ∈ {0, . . . , 2t − 1};
                                                     t
 8 Inspect continued-fraction convergents of j/2 in increasing denominator order;
                                             ′         r′
 9 return the first positive denominator r with a ≡ 1 (mod N ), or failure;




each factoring attempt. The probability bound concerns the measurement distribution, while the inverse
quantum Fourier transform contributes separately to the circuit cost.

4.2 Reversible Modular Arithmetic
Phase estimation applies modular exponentiation to a superposition of exponents. Temporary values left
behind by one exponent would reveal branch information and weaken the interference used to recover the
period. When the input registers hold x and y and the scratch space starts at zero, the desired transformation
is |x⟩|y⟩|0⟩ 7→ |x⟩|ax y mod N ⟩|0⟩. Reversible arithmetic achieves this transformation by computing an
intermediate value, copying or accumulating the required result, and running the temporary computation
backward [29].
    Here n denotes the word width. Reversible addition retains u and replaces v by u + v in Z2n ; running the
same network backward subtracts u. A carry flag may be used during the calculation, but it returns to zero
before the next operation. The Vedral–Barenco–Ekert network [29] supplies this basic addition pattern, which
later stages reuse for comparison, conditional correction, and uncomputation.
    For canonical residues 0 ≤ u, v < N , first compute the ordinary sum and compare it with N . If the sum
reaches N , subtract N once; otherwise leave the sum unchanged. Reversing the comparison erases the decision
flag while preserving the corrected value, so the target holds (u + v) mod N and can immediately feed another
arithmetic step. Ref. [29] gives a reversible network for this sequence.
  PLet c ibe a known   constant modulo N , and let yi be the bits of y. Controlled modular additions accumulate
    i yi (2 c mod N )   mod N = cy mod N in a second register [29]. When gcd(c, N ) = 1, the inverse c−1 makes
this multiplication reversible. After swapping the input and product registers, multiplication by c−1 runs
backward to erase the old value. The remaining register holds cy mod N , and the scratch space is ready for
the next controlled power.
    Algorithm 2 describes controlled modular exponentiation. Let ℓ denote the exponent width, so x =
                                                        2i
Pℓ−1        i
   i=0 xi 2 . The classically precomputed constant a mod N is applied exactly when xi = 1. The selected
constants therefore multiply to ax , yielding |x⟩|y⟩ 7→ |x⟩|ax y mod N ⟩. Reversing each multiplier’s temporary
computation restores the work register.
    Each controlled multiplication is followed by the inverse operations needed to clear its temporary values.
The peak logical-qubit count is set by the data and work registers that must coexist, while Toffoli count and
                                                                                          i
depth accumulate over the controlled multipliers executed in sequence. The powers a2 mod N are computed
classically before the quantum circuit begins. The primitive addition and multiplication costs are based on
the Vedral–Barenco–Ekert construction [29].

4.3 Ekerå–Håstad Route
Ref. [19] recasts factoring as a short discrete logarithm problem. For this route, let n denote the bit length
of N = pq, choose a unit g ∈ Z∗N of order r, and compute y = g N +1 mod N . Since N + 1 − (p + q) = φ(N )
and r divides φ(N ), the relation y = g p+q holds in the subgroup generated by g; when r > p + q, the short
logarithm is d = p + q. The resource presentation in Ref. [21] uses exponent registers of widths 2m and m,
where p + q < 2m and m = n/2 + O(1). The two exponent registers have combined width 3m = 1.5n + O(1),
compared with the 2n phase register in the textbook order-finding route. The width is determined from
the public bit length of N . The hidden factors appear only in the identity that explains why the recovered
logarithm equals p + q.



                                                       7
Lean-QuantumAlg                                                                               QudeLeap Research



 Algorithm 2: Controlled modular exponentiation for the phase-estimation oracle [5]
   Input : Modulus N , unit a mod N , exponent width ℓ with bits x0 , . . . , xℓ−1 , target y ∈ ZN , clean
             work register
   Output : Unchanged exponent, target ax y mod N , clean work register
                             2i
 1 Classically compute ui ← a mod N for i = 0, . . . , ℓ − 1;
 2 for i ← 0 to ℓ − 1 do
 3    Controlled on exponent qubit xi , multiply the target by ui modulo N ;
 4    Uncompute all temporary values produced by the controlled multiplier;
 5   return x, ax y mod N , and the restored work register;


    The 2017 Ekerå–Håstad formulation [19] computes x = g (N −1)/2 and recovers the short secret δ =
(p + q − 2)/2. This parameterization satisfies d = 2δ + 2 for the sum d = p + q used above. Setting c = δ + 1
gives 2c = p + q, so a candidate root q ′ is accepted when q ′ (2c − q ′ ) = N . The two equations, together with
the requirement that the accepted root lie strictly between one and the modulus, make it a proper divisor of
N . Completing the RSA-2048 analysis requires the probability of obtaining the short secret, the repetitions
used to amplify that probability, and the total cost of those repetitions for the Ekerå–Håstad circuit.
    Ref. [21] reports more than 99% classical recovery conditional on a correct short discrete logarithm run.
The analysis in Ref. [5] combines the probability of sampling a good base with repeated order finding to
reach high success probability. The success figure used here assumes that each factoring attempt fails with
probability at most one half and that three attempts are independent. Their joint failure probability is then
at most 1/8 ≤ 1/3, giving success probability at least 2/3. Deriving the assumed one-half rate from the
one-sample bound above requires an explicit number of order-finding samples and would increase the quantum
cost. Ref. [21] gives 6190 live logical qubits, 2.7 × 109 Toffoli gates, and 2.14 × 109 measurement depth for one
run. Applying these source figures to three sequential attempts gives 8.1 × 109 Toffoli gates and measurement
depth 6.42 × 109 . We separately report a budget of 36906 abstract classical recovery operations; deriving that
budget from Algorithm 3 remains open. In the source terminology, the value 2.14 × 109 is a measurement
depth. Table 1 and the RSA-2048 statement call the tripled value a maximal circuit depth, and relating
the two quantities requires an additional argument. This success figure and the reported quantum resources
therefore summarize different calculations. A complete analysis must establish both for the Ekerå–Håstad
circuit whose resources are reported.


5 Formalizing P-256
5.1 Elliptic-Curve Discrete Logarithms
Problem 2 fixes an elliptic curve E over Fp , a point P ∈ E(Fp ) of prime order r, and a point Q = [m]P for an
unknown scalar m ∈ Zr . This section works inside the cyclic subgroup G = ⟨P ⟩. Its computational goal is to
recover the unique residue class m represented by the relation Q = [m]P .
    The underlying discrete logarithm problem is independent of the coordinate representation of the curve.
Write the operation of a finite cyclic group additively, let P generate a group G of known order r, and write
[a]R for the action of a ∈ Zr on R ∈ G. An instance consists of (G, r, P, Q) together with the proposition that
some m ∈ Zr satisfies Q = [m]P . The success event is that the classical output equals this m in Zr .
    Shor’s discrete-logarithm algorithm [5] uses two exponent registers, a coherent group evaluation, Fourier
transforms, and classical post-processing. It is an instance of the abelian hidden-subgroup framework [1, 10].
For the algebraic derivation, we use the exact order presentation in Ref. [22]; its registers are indexed by Zr
and its elliptic-curve group action consists of scalar multiplication and point addition. Algorithm 4 states this
version; later subsections refine its group action step into reversible field and curve circuits.
    The coherent map sends (k, ℓ) to [k]P + [ℓ]Q = [k + mℓ]P . Measuring a group element therefore leaves a
uniform superposition over one affine fiber of the function (k, ℓ) 7→ k + mℓ. The two inverse Fourier transforms
map that fiber to frequency pairs satisfying

                                              v ≡ mu       (mod r).                                           (1)

Lean expresses the same relation with the action [a]P − [b]Q. Writing its left and right frequencies as u and
w, respectively, gives w ≡ −mu (mod r). The substitutions b = −ℓ and w = −v identify this convention with
the additive map in Algorithm 4.
   For a valid sample with invertible u, the relation gives m = vu−1 in Zr . In the exact prime-order
construction presented in Ref. [22], the first frequency is uniform. Since r is prime, every nonzero frequency is


                                                       8
Lean-QuantumAlg                                                                                 QudeLeap Research



 Algorithm 3: Ekerå–Håstad RSA factorization through a short discrete logarithm [19, 21]
   Input : Public RSA modulus N , random unit g ∈ Z∗N , width m chosen from the public bit length of
             N
   Output : The factors of N , or failure
                              N +1
 1 Classically compute y ← g       mod N ;
 2 Prepare uniform exponent registers of widths 2m and m, together with a clean group register;
               e −e
 3 Compute g 1 y 2 mod N in the group register over the exponent superposition;
 4 Apply the two Fourier transforms and measure a frequency pair;
                                                          m
 5 Use lattice post-processing to recover d with 0 < d < 2  and verify g d ≡ y (mod N );
                    2
 6 Compute ∆ ← d − 4N and fail unless ∆ is a nonnegative square;
                 √                √
 7 return (d +     ∆)/2 and (d − ∆)/2;


invertible, and these values occupy a fraction (r − 1)/r of the frequency space. Our formal proof derives the
secret deterministically from a valid linear relation and an invertible frequency. The probability argument is
supplied separately: it assumes nonnegative outcome weights and a set of good events whose total weight is at
least 2/3.
    To apply the argument for a cyclic group to P-256, we identify the abstract group order, generator,
target, and scalar action with their elliptic-curve counterparts. Under these identifications, every certified
recoverable measurement outcome gives a candidate for the curve scalar. The current theorem combines three
separately provided ingredients: this algebraic identification, correctness and resource bounds for the circuit
that evaluates scalar multiples, and the total probability assigned to recoverable measurement outcomes. The
formalization appendix maps these ingredients to their Lean declarations. The field and curve circuits needed
for the scalar action are developed next.

5.2 Reversible Prime-Field Arithmetic
Affine elliptic-curve formulas reduce point operations to arithmetic in the prime field Fp . Let n denote the
register width; P-256 has n = 256. We encode a field element by its canonical integer representative in the
range 0 ≤ x < p. We prove that canonical integers and P-256 field elements encode one another consistently.
Each reversible operation preserves its source operands, adds its result to a designated target, and returns
flags and scratch registers to their clean values. These properties give point addition a common contract for
encoded states.
    For field elements represented by integers 0 ≤ a, b < p, modular addition implements (a, b) 7→ (a, a + b),
with the second component reduced modulo p. Ref. [7] realizes this map by ordinary addition, conditional
subtraction of p, and a comparison that erases the reduction flag; reversing the circuit gives subtraction. The
corresponding doubling circuit acts on one residue register and uses the oddness of p to recover the reduction
decision from the least significant output bit. We prove that the addition and subtraction circuits are mutual
inverses on canonical inputs and restore their ancillas. Sequential resource composition takes the maximum
workspace and adds Toffoli counts, other gate counts, and depth. Parallel composition adds workspace, Toffoli
counts, and other gate counts and takes the maximum depth.
    Field multiplication takes two quantum residues and writes their product into a separate target. For the
source circuit, set R = 2n and write ā = aR mod p and b̄ = bR mod p for the Montgomery representatives of
a and b. The construction in Ref. [7] maps ā and b̄ to āb̄R−1 = ab, retains one history bit per round recording
whether p was added, copies the product, and reverses the computation to erase those bits. The corresponding
squaring circuit identifies the two multiplicands, removes the second n-qubit input, and adds one copying
ancilla, saving n − 1 qubits. The present P-256 division result uses separately verified circuits for this product,
inversion, and target addition. Its correctness and resource bounds depend on all three components.
    Ref. [7] uses 2n Montgomery–Kaliski rounds to map a nonzero representative ā to a−1 . The extended
binary Euclidean state (u, v, r, s) maintains the Bézout relation p = rv + su. Each active round retains one
selector bit and reconstructs the other from the parity invariant. A flag switches from Euclidean updates
to padding rounds, while a counter records their number ℓ. The final coefficient is an almost inverse. The
correction −2ℓ r mod p produces a representative b̄ satisfying b̄ā = R2 mod p, and hence b̄ = a−1 . Algorithm 5
adds this value to the target and reverses the recorded computation to restore the workspace.
    For a unit denominator a and numerator b, modular division adds ba−1 to a target. We compose verified
circuits for inversion, multiplication, and addition to the target, and then reverse the temporary computations.
Under these assumptions, the circuit has a clean quotient action on the P-256 encoding and inherits the
component resource bounds. For affine points (x1 , y1 ) and (x2 , y2 ), generic addition divides by x1 − x2 , while
point doubling divides by 2y1 . The mathematical group law handles identity inputs separately. When x1 = x2 ,


                                                        9
Lean-QuantumAlg                                                                               QudeLeap Research



 Algorithm 4: Shor’s elliptic-curve discrete-logarithm algorithm [5, 22]
   Input : Generator P of a cyclic group of known prime order r, target point Q ∈ ⟨P ⟩
   Output : The scalar m ∈ Zr satisfying Q = [m]P , or failure
                                                  2
 1 Prepare a uniform superposition over (k, ℓ) ∈ Zr and a clean group register;
 2 Coherently compute [k]P + [ℓ]Q into the group register;
 3 Measure and discard the group register;
 4 Apply the inverse Fourier transform over Zr to each index register;
                                      2
 5 Measure a frequency pair (u, v) ∈ Zr ;
 6 if u = 0 then
 7     return failure;
 8   return vu−1 mod r;


equal points use the doubling formula and inverse points sum to the point at infinity; doubling with y1 = 0
also returns the point at infinity. The generic division result applies after its nonzero denominator has been
established.
    The current field results therefore cover target addition, inversion, and division under the component
assumptions above. They prove clean actions on computational basis inputs and combine the supplied resource
bounds. Connecting the concrete Montgomery–Kaliski construction to the assumed P-256 inversion circuit
remains a formalization obligation. The formalization appendix gives the corresponding declaration details.
The next subsection composes these field operations into elliptic-curve formulas.

5.3 Reversible Elliptic-Curve Operations
The mathematical group E(Fp ) contains finite affine points and the point at infinity O. Its addition law
treats O as the identity, sends a pair of inverse points to O, uses a tangent formula when the two inputs
coincide, and uses a secant formula when their x-coordinates differ. The circuit representation stores only the
two coordinates of a finite affine point. Accordingly, the generic affine circuit in Ref. [7] takes finite points
                                            ̸ x2 . Identity, inverse, and doubling cases remain separate branches
P1 = (x1 , y1 ) and P2 = (x2 , y2 ) with x1 =
of the mathematical group law.
    For the generic branch, the formulas analyzed in Ref. [7] are
                            y1 − y2
                       λ=            ,    x3 = λ2 − x1 − x2 ,      y3 = λ(x1 − x3 ) − y1 .                    (2)
                            x1 − x 2
They require one field division for the slope, followed by multiplication, squaring, addition, and subtraction.
If the curve equation is y 2 = x3 + Ax + B, nonexceptional doubling replaces the slope by (3x21 + A)/(2y1 )
and requires 2y1 ̸= 0. The Lean mathematical layer proves that both coordinate formulas agree with the
corresponding elliptic-curve group operations under their stated denominator conditions. The structured
point circuit developed below uses the generic formula in Eq. (2).
    The controlled point addition circuit in Ref. [7] keeps P1 in a quantum accumulator and takes P2 as a
classically precomputed constant. A control bit selects whether the accumulator becomes P1 + P2 or returns
to P1 . Reversibility relies on recovering the slope from the output P3 = (x3 , y3 ) and the fixed addend:
                                             y1 − y 2    y3 + y 2
                                                      =−          .                                           (3)
                                             x1 − x 2    x3 − x 2
This identity lets the source circuit update the accumulator directly and erase the slope and coordinate
scratch afterward. Our current construction stores the result in separate target coordinates. The construction
preserves the input point, computes and writes the generic sum, and reverses the arithmetic to clean the slope
and coordinate workspace. Its correctness assumes verified circuits for division and the coordinate updates
used in these stages. P
                        h−1
    For a scalar k = i=0 ki 2i , the method for a fixed base in Ref. [22] classically precomputes Pi = [2i ]P
and applies one controlled addition of Pi for each bit ki . Thus every elliptic-curve doubling occurs during
classical precomputation; the quantum circuit executes only controlled additions of fixed points. Starting
from an affine point S, the accumulator after the schedule is S + [k]P . To verify this schedule, we specify the
accumulator before and after every addition controlled by a scalar bit. Every step must satisfy the generic
affine condition, including a step whose control bit is zero, and must use a separately verified point addition
circuit. Composing these steps proves the final scalar action, workspace cleanup, and accumulated resource
bound.


                                                       10
Lean-QuantumAlg                                                                                   QudeLeap Research



 Algorithm 5: Reversible Montgomery–Kaliski inversion with 2n rounds [7]
   Input : Odd n-bit prime p, R = 2n , nonzero Montgomery representative ā = aR mod p, target
                 representative z̄ = zR mod p, clean work registers
   Output : Unchanged ā, target z̄ + a−1 R mod p, and restored work registers
 1 Initialize (u, v, r, s) ← (p, ā, 0, 1), active flag f ← 1, padding counter ℓ ← 0, and clean history bits
    m0 , . . . , m2n−1 ;
 2 for i ← 0 to 2n − 1 do
 3     if f = 1 and v ̸= 0 then
 4           if u is even then
 5                Set (u, s) ← (u/2, 2s);
 6           else if v is even then
 7                Set (v, r) ← (v/2, 2r);
 8           else if u > v then
 9                Set (u, r, s) ← ((u − v)/2, r + s, 2s);
10           else
11                Set (v, r, s) ← ((v − u)/2, 2r, r + s);
12        Retain the branch selector in mi and erase the other selector from the parity of r or s;
13     else
14        Set f ← 0 and ℓ ← ℓ + 1;
15 Set k ← 2n − ℓ; then rā ≡ −2k (mod p);
                ℓ                       2                     −1
16 Set b̄ ← −2 r mod p, so that b̄ā ≡ R (mod p) and b̄ = a      R mod p;
17 Add b̄ to z̄ modulo p;
18 Reverse the correction and all 2n rounds to clean the scratch, counter, flag, and history bits;
                     −1
19 return ā, z̄ + a    R mod p, and the restored work registers;


    The coherent circuit in Ref. [7] initializes the accumulator to [a0 ]P , applies the controlled additions selected
by k, and then applies those selected by ℓ from the precomputed multiples of Q. Both exponent registers have
width h = n + 1, and measurement follows all 2h controlled additions. Algorithm 6 therefore maps each generic
basis input to [a0 + k]P + [ℓ]Q while preserving coherence across the exponent registers. The fixed offset
translates the group value and leaves the hidden period relation detected by the subsequent measurement
unchanged [22]. Instantiating two such step lists as a concrete P-256 double scalar circuit and connecting that
circuit to the measurement distribution used by scalar recovery remain formalization obligations.
    The rough valid-input analysis in Ref. [7] chooses a0 uniformly from the nonzero scalars and assumes that
the secret scalar is uniform. Under these conditions, the estimated fraction of pairs (k, ℓ) for which both
schedules avoid exceptional additions is at least (1 − n/2n )2 , which becomes (1 − 2−248 )2 for P-256. This
quantity measures the validity of the generic affine computation. The subsequent measurement and scalar
recovery have separate success conditions. Each controlled point addition in the resource analysis uses four
inversions, two squarings, and four multiplications [7], with intermediate registers cleaned after each call.
Algorithm 6 displays the coherent group action with two h-bit exponent registers. The 2330-qubit value
in Table 2 comes from the semiclassical construction, which measures and reuses one control qubit after
each controlled addition [7]. Its Toffoli count and maximal Toffoli-gate depth use the paper’s estimate of 2n
controlled additions. The current resource theorem sums the assumed cost of each controlled point addition
in this schedule. A separate probability argument supplies the measurement-outcome weights used for scalar
recovery.

5.4 Scalar Recovery
The P-256 standard of the National Institute of Standards and Technology [8] fixes the prime-field modulus,
curve coefficients, base point P , prime subgroup order r, and cofactor. The current formalization takes as
hypotheses the field, curve, and subgroup properties of these constants. The formalization also assumes a
correspondence between the generic cyclic group and the P-256 subgroup: their orders agree, their generators
and targets correspond to P and Q, and their scalar actions agree with elliptic-curve scalar multiplication.
Under these hypotheses, a recovered residue gives a candidate solution of Q = [m]P . Evidence about the
circuit that implements scalar multiplication and its resources is supplied separately from the weights assigned
to the full algorithm’s measurement outcomes. Deriving both from measurement of a concrete P-256 circuit
remains an integration task.
                                                     ̸ 0 and satisfies the relation v = mu in Zr from Algorithm 4.
    Every certified good frequency pair (u, v) has u =


                                                         11
Lean-QuantumAlg                                                                                QudeLeap Research



 Algorithm 6: Coherent double scalar evaluation [7, 22]
   Input : Curve E/Fp with n = ⌈log2 p⌉; point P of prime order r; point Q ∈ ⟨P ⟩; h-bit registers
              k = (ki ) and ℓ = (ℓi ) with h = n + 1; offset a0 sampled uniformly from Zr \ {0}; clean point
              and work registers
   Output : Unchanged k, ℓ; point register [a0 + k]P + [ℓ]Q when every current accumulator and fixed
              addend have distinct x-coordinates; clean work registers
                                     i               i
 1 Classically precompute Pi = [2 ]P and Qi = [2 ]Q for 0 ≤ i < h;
 2 Initialize the point register to [a0 ]P ;
 3 for i ← 0 to h − 1 do
 4     Coherently add the fixed point Pi under the control bit ki ;
 5     Erase the slope, coordinate scratch, and arithmetic work registers;
 6 for i ← 0 to h − 1 do
 7    Coherently add the fixed point Qi under the control bit ℓi ;
 8    Erase the slope, coordinate scratch, and arithmetic work registers;
 9   return k, ℓ, [a0 + k]P + [ℓ]Q, and the clean work registers;


Because r is prime, this nonzero u is invertible. The direct recovery rule in Ref. [22] returns m′ = vu−1 .
Multiplying the relation by u−1 proves m′ = m; the correspondence above then gives Q = [m′ ]P . The current
P-256 theorem begins with a scalar m satisfying 0 ≤ m < r and a proof of Q = [m]P . This theorem verifies
that every certified good output agrees with the same residue. An execution that receives only the public
curve data and computes m remains an integration task.
    The probability argument supplies nonnegative outcome weights, a finite set of recoverable outcomes,
and a lower bound showing that their total mass is at least 2/3. One run therefore meets the stated success
threshold. The resource analysis in Ref. [7] gives the corresponding baseline of 2330 logical qubits, 1.26 × 1011
Toffoli gates, and maximal Toffoli-gate depth 1.16 × 1011 . The seven classical operations in Table 2 form a
bookkeeping profile for direct recovery from one certified output: one gcd check, one extended Euclidean
run, one modular inversion, one modular addition and one multiplication for checking the relation, and a
final negation and multiplication. This count begins after the quantum measurement and excludes candidate
search, repeated experiments, Chinese remainder aggregation, and bit complexity. In the current proof route,
the measurement weights and resource equalities enter as separate premises.


6 Conclusion and outlook
This work develops a Lean formalization of the mathematical reductions and quantum circuit components
underlying attacks on RSA-2048 and P-256. For RSA-2048, the formal application layer combines a certified
factor, a success threshold of at least 2/3, and the logical resource values reported in Ref. [21]. For P-256, it
combines a certified private scalar, the same success threshold, and the logical resource values reported in
Ref. [7]. The two developments bring number theory, probability arguments, reversible arithmetic, quantum
circuits, classical recovery, and resource accounting into a common body of checked propositions. Software
agents assisted with source analysis, proof decomposition, Lean development, and manuscript maintenance
under human review. Machine checking verified every proof accepted into the formal development.
    Several connections at the application layer enter as explicit assumptions. The factorization model already
includes the two prime factors; the final RSA-2048 proposition then receives factor recovery and success
evidence together with resource values imported from the literature. Connecting the formalized Ekerå–Håstad
algorithm directly to this proposition remains an integration goal. In the P-256 development, stronger
intermediate results use a bridge between the finite cyclic group and the curve, support for the expected
measurement outcomes, and facts about the scalar arithmetic circuit. The final P-256 proposition begins with
the recovered scalar, its probability bound, and the resource equalities as assumptions. A complete execution
beginning from a 2048-bit modulus or a P-256 public point remains to be constructed for each application.
The reported resources describe specific analyzed logical circuits; resource lower bounds and optimality remain
open questions. For RSA-2048, the source reports logical qubits, Toffoli gates, and measurement depth, while
the present proposition uses a general circuit-depth label for that last value. For P-256, the source reports
logical qubits, Toffoli gates, and maximal Toffoli-gate depth. The quantitative analysis also counts the stated
classical recovery operations. Circuit noise, quantum error correction, magic state production, scheduling,
runtime, and physical qubit requirements call for additional models and proofs.
    The next stage is to construct executions from public inputs and derive correctness, output probabilities, and
resource values from the same formal run. A complementary direction is to extend the resource analysis beyond


                                                       12
Lean-QuantumAlg                                                                              QudeLeap Research



logical circuits. Recent RSA-2048 estimates study approximate residue arithmetic with lower logical-qubit
requirements [30] and fault-tolerant architectures based on quantum low-density parity-check codes [31, 32];
formalizing them requires explicit noise, decoding, scheduling, and architecture assumptions. For elliptic-curve
discrete logarithms, Ref. [33] develops circuit families optimized separately for width, T -gate count, and
depth. Formalizing these tradeoffs would extend the single P-256 resource profile used here. Ref. [34] develops
space-efficient reversible inversion and arithmetic circuits together with a resource derivation. Formalizing
its arithmetic circuits and checking the resource derivation would extend the present elliptic-curve analysis.
These projects would support comparisons of new quantum cryptanalytic constructions through explicit
mathematical assumptions, formal circuit behavior, and mechanically checked resource formulas.


References
 [1] Andrew M. Childs. Lecture notes on quantum algorithms, 2021.
 [2] Ronald de Wolf. Quantum computing: Lecture notes, 2019.

 [3] Ashley Montanaro. Quantum algorithms: An overview. npj Quantum Information, 2(1):15023, 2016.
 [4] Lin Lin. Lecture notes on quantum algorithms for scientific computation, 2022.
 [5] Peter W. Shor. Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum
     computer. SIAM Journal on Computing, 26(5):1484–1509, 1997.

 [6] Ronald L. Rivest, Adi Shamir, and Leonard Adleman. A method for obtaining digital signatures and
     public-key cryptosystems. Communications of the ACM, 21(2):120–126, 1978.
 [7] Martin Roetteler, Michael Naehrig, Krysta M. Svore, and Kristin Lauter. Quantum resource estimates
     for computing elliptic curve discrete logarithms. In Advances in Cryptology – ASIACRYPT 2017, volume
     10625 of Lecture Notes in Computer Science, pages 241–270. Springer, 2017.

 [8] Lily Chen, Dustin Moody, Karen Randall, Andrew Regenscheid, and Angela Robinson. Recommendations
     for discrete logarithm-based cryptography: Elliptic curve domain parameters. Technical Report NIST
     Special Publication 800-186, National Institute of Standards and Technology, 2023.
 [9] Richard Jozsa. Quantum factoring, discrete logarithms, and the hidden subgroup problem. Computing in
     Science & Engineering, 3(2):34–43, 2001.
[10] Andrew M. Childs and Wim van Dam. Quantum algorithms for algebraic problems. Reviews of Modern
     Physics, 82(1):1–52, 2010.
[11] Christophe Chareton, Sébastien Bardin, François Bobot, Valentin Perrelle, and Benoît Valiron. An auto-
     mated deductive verification framework for circuit-building quantum programs. In Nobuko Yoshida, editor,
     Programming Languages and Systems, pages 148–177, Cham, 2021. Springer International Publishing.
[12] Yuan Feng and Mingsheng Ying. Quantum hoare logic with classical variables. ACM Transactions on
     Quantum Computing, 2(4):16:1–16:43, December 2021.
[13] Liyi Li, Mingwei Zhu, Rance Cleaveland, Alexander Nicolellis, Yi Lee, Le Chang, and Xiaodi Wu. Qafny: A
     quantum-program verifier. In Jonathan Aldrich and Guido Salvaneschi, editors, 38th European Conference
     on Object-Oriented Programming (ECOOP 2024), volume 313 of Leibniz International Proceedings in
     Informatics (LIPIcs), pages 24:1–24:31, Dagstuhl, Germany, 2024. Schloss Dagstuhl – Leibniz-Zentrum
     für Informatik.
[14] Yuxiang Peng, Kesha Hietala, Runzhou Tao, Liyi Li, Robert Rand, Michael Hicks, and Xiaodi Wu. A
     formally certified end-to-end implementation of shor’s factorization algorithm. Proceedings of the National
     Academy of Sciences, 120(21):e2218775120, May 2023.
[15] The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
     International Conference on Certified Programs and Proofs, CPP 2020, pages 367–381. Association for
     Computing Machinery, 2020.

[16] Clark Barrett, Swarat Chaudhuri, Fabrizio Montesi, Jim Grundy, Pushmeet Kohli, Leonardo de Moura,
     Alexandre Rademaker, and Sorrachai Yingchareonthawornchai. CSLib: The Lean computer science
     library, 2026.


                                                      13
Lean-QuantumAlg                                                                             QudeLeap Research



[17] Chengkai Zhu, Ziao Tang, Guocheng Zhen, Yimeng Cao, Yusheng Zhao, Ranyiliu Chen, Xuanqiang Zhao,
     Lei Zhang, and Xin Wang. Lean-QIT: Towards a formal infrastructure for quantum information theory,
     2026.
[18] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J.
     Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-augmented language
     models. In Advances in Neural Information Processing Systems, volume 36, 2023.
[19] Martin Ekerå and Johan Håstad. Quantum algorithms for computing short discrete logarithms and
     factoring RSA integers. In Post-Quantum Cryptography, volume 10346 of Lecture Notes in Computer
     Science, pages 347–363. Springer, 2017.

[20] Mingrui Jing, Lei Zhang, Yusheng Zhao, Hongshun Yao, and Xin Wang. An agentic formalization for
     certified quantum neural network design, 2026.
[21] Craig Gidney and Martin Ekerå. How to factor 2048 bit RSA integers in 8 hours using 20 million noisy
     qubits. Quantum, 5:433, 2021.

[22] John Proos and Christof Zalka. Shor’s discrete logarithm quantum algorithm for elliptic curves, 2004.
[23] Mingsheng Ying. Floyd–hoare logic for quantum programs. ACM Transactions on Programming Languages
     and Systems, 33(6):19:1–19:49, 2011.
[24] Mingsheng Ying. A practical quantum hoare logic with classical variables, I. Information and Computation,
     309:105417, 2026.

[25] The Coq Development Team. The Coq proof assistant (8.20), 2024.
[26] Li Zhou, Gilles Barthe, Pierre-Yves Strub, Junyi Liu, and Mingsheng Ying. CoqQ: Foundational
     verification of quantum programs. Proceedings of the ACM on Programming Languages, 7(POPL):833–
     865, 2023.

[27] Richard Cleve, Artur Ekert, Chiara Macchiavello, and Michele Mosca. Quantum algorithms revisited.
     Proceedings of the Royal Society of London. Series A: Mathematical, Physical and Engineering Sciences,
     454(1969):339–354, 1998.
[28] Michael A. Nielsen and Isaac L. Chuang. Quantum Computation and Quantum Information. Cambridge
     University Press, 10th anniversary edition edition, 2010.

[29] Vlatko Vedral, Adriano Barenco, and Artur Ekert. Quantum networks for elementary arithmetic
     operations. Physical Review A, 54(1):147–153, 1996.
[30] Craig Gidney. How to factor 2048 bit RSA integers with less than a million noisy qubits, 2025.
     arXiv:2505.15917.

[31] Paul Webster, Lucas Berent, Omprakash Chandra, Evan T. Hockings, Nouédyn Baspin, Felix Thomsen,
     Samuel C. Smith, and Lawrence Z. Cohen. The pinnacle architecture: Reducing the cost of breaking
     RSA-2048 to 100 000 physical qubits using quantum LDPC codes, 2026. arXiv:2602.11457.
[32] Madelyn Cain, Qian Xu, Robbie King, Lewis R. B. Picard, Harry Levine, Manuel Endres, John Preskill,
     Hsin-Yuan Huang, and Dolev Bluvstein. Shor’s algorithm is possible with as few as 10,000 reconfigurable
     atomic qubits, 2026. arXiv:2603.28627.
[33] Thomas Häner, Samuel Jaques, Michael Naehrig, Martin Roetteler, and Mathias Soeken. Improved
     quantum circuits for elliptic curve discrete logarithms. In Post-Quantum Cryptography, volume 12100 of
     Lecture Notes in Computer Science, pages 425–444. Springer, 2020.
[34] Han Luo, Ziyi Yang, Ziruo Wang, Yuexin Su, and Tongyang Li. Space-efficient quantum algorithm for
     elliptic curve discrete logarithms with resource estimation, 2026. arXiv:2604.02311.




                                                     14
Lean-QuantumAlg                                                                              QudeLeap Research




Fig 1: An overview of the agentic formalization workflow and its trust boundary. The two rows follow artifacts
from claim selection and source evidence through formal obligations, Lean development, machine checking,
human review, and manuscript integration. The framed stages lie within the proof-term trust boundary; the
return arrow denotes revision after human review.


A Agentic Workflow and Reproducibility
A.1 Responsibilities and Trust Boundary
Figure 1 follows each artifact from a scientific question to the manuscript. Authors first specify the claim
and the sources that should support it. Software agents retrieve passages, source locations, and metadata,
then separate the claim into mathematical, algorithmic, circuit, and resource obligations. They trace relevant
dependencies and construct Lean statements and proof terms for those obligations. The kernel accepts a
declaration when its proof term checks against the stated type. The accepted theorem type records its explicit
hypotheses, while the development preserves imported dependencies for later inspection. Authors receive these
checked statements alongside the source evidence and decide which claims, citations, and formal references
enter the manuscript. The responsibility of software agents covers evidence retrieval, claim decomposition,
dependency tracing, construction of Lean statements and proofs, and an explicit account of the assumptions
used at each stage.
    Authors retain responsibility for the scientific decisions throughout this flow. They approve the question
and source scope, inspect each source passage in context, and decide whether its interpretation supports the
proposed mathematical statement. They choose the models and assumptions, compare manuscript prose
with the exact checked conclusion, and verify the provenance, units, and scope of quoted resource values.
This review also covers citation placement and the prominence given to limitations. A change produced by
an agent enters the repository only after an author accepts the corresponding source interpretation, formal
statement, and manuscript wording.
    The Lean kernel’s trust boundary covers the checking of proof terms under the definitions, assumptions,
and imported results in the formal environment. Kernel acceptance establishes that a proof term has its
declared type. Once accepted, the theorem can be used in later proofs. Source fidelity, model selection,
resource inputs drawn from the literature, and the interpretation of a theorem in prose lie in the surrounding
research process. Authors review those items by comparing source locations with formal assumptions, checking
resource records against their cited analyses, and matching each manuscript claim to the conclusion that the
kernel accepted. This division identifies the precise guarantee supplied by formal checking and the evidence
that still requires scientific judgment.

A.2 Positive Collaboration Cases
For RSA-2048, software agents divided the argument into order finding, reversible modular arithmetic, classical
factor recovery, success amplification, and resource accounting for the application claim. They located the


                                                      15
Lean-QuantumAlg                                                                                      QudeLeap Research



source passages and formal declarations for each layer, traced direct dependencies within each branch, and
identified the certificates assembled by the terminal theorem. This division let the authors inspect the
number-theoretic reduction separately from the circuit construction. The authors also reviewed the success
certificate and the literature resource tuple as separate inputs, checking the provenance and scope of each
before accepting the application statement. The declaration roadmap records where every component enters
the endpoint.
    For P-256, software agents mapped the generic recovery argument for a finite cyclic group alongside the
reversible prime-field and elliptic-curve circuit results. They recorded the equations and certificates required
to assemble the application endpoint, including the curve bridge, sampling support, certificate for the scalar
oracle, and resource equalities. Authors checked the endpoint’s output equality against the stored private
scalar and separately checked the provenance and scope of the logical resource tuple. The terminal theorem
receives these correctness and resource facts as explicit inputs. Appendix B gives a reviewable account of
their mathematical roles and current connections.

A.3 Reproducibility
A reader can start from the two theorem environments in Sec. 2 and follow Appendix B to the declaration
roadmap and terminal signatures in Listings 3 and 4. The exact source versions and locators are recorded
in registry/sources.jsonl. For RSA-2048, Shor’s construction [5] supports the factoring route, while
Ref. [21] supplies the quoted quantum resource tuple. The success certificate and classical operation count
are separate repository inputs. These inputs, the assumptions and conclusion of the final Lean theorem, the
RSA-2048 theorem, and Table 1 must agree. For P-256, National Institute of Standards and Technology
Special Publication 800-186 [8] supplies the domain parameters, while Ref. [7] supplies the quoted quantum
resource tuple. The success certificate and the count of seven classical operations are separate repository
inputs. These inputs must agree with the assumptions and conclusion of the final Lean theorem, the P-256
theorem, and Table 2. Agreement among the source records, checked propositions, and manuscript claims is
the reproducibility criterion for each application result.


B Lean Formalization
B.1 Formalization Roadmap
This appendix maps the mathematical development to selected Lean declarations. Figure 2 separates
implemented dependency paths from interfaces that accept an explicit bridge or certificate. The branch for
a 2048-bit Rivest–Shamir–Adleman (RSA) modulus joins reversible arithmetic with probability and factor
recovery at a generic factoring certificate. The P-256 branch joins discrete logarithms in finite cyclic groups,
field and curve arithmetic, and scalar multiplication at a witness in the application layer. The two terminal
propositions record the returned value, a rational success bound, and logical resource values derived from the
literature. A solid arrow means that a declaration directly constructs or consumes the preceding object. A
dashed arrow means that the receiving theorem asks its caller to provide the stated relation as a hypothesis
or certificate field.
    Typed circuits carry an encoding, a state transformation, and resource fields through composition. Modular
addition is a representative foundation: on a clean basis state it preserves the left register, replaces the right
register by its sum modulo the declared modulus, and returns the flag to zero. Listing 1 gives this semantic
statement; the proof body and the accompanying resource witness are available in the repository.
    Listing 1: The clean basis state semantics of reversible modular addition. The proof body is omitted.
 theorem addCircuit_apply_clean_ket (N n : N) [NeZero N]
     (params : ResourceParameters) (a b : ZMod N) :
     Circuit.apply (addCircuit N n params)
       (PureState.ket (R := register N)
         ({ left := a, right := b, flag := false } : Data N) :
           StateVector (register N)) =
       (PureState.ket (R := register N)
         ({ left := a, right := a + b, flag := false } : Data N) :
           StateVector (register N)) := by
   -- proof omitted

   The listing also illustrates how local semantic and resource claims are organized. Its state equality describes
the behavior visible to a caller, including cleanup of the ancillary flag. A companion witness refers to this


                                                          16
Lean-QuantumAlg                                                                               QudeLeap Research




Fig 2: A dependency map of the Lean development used for the RSA-2048 and P-256 results. Solid arrows
show implemented dependency paths, with intermediate helpers omitted; dashed arrows show interface or
certificate boundaries. The terminal nodes are the public RSA-2048 and P-256 theorems.


same circuit when it projects qubits, gates, depth, and query depth. Composition preserves this association as
addition feeds multiplication and exponentiation. At the ends of the graph, a broader proposition collects
such circuit results with probability and number-theoretic certificates. The declaration tables below give a
compact route from each part of this narrative to the relevant namespace.

B.2 RSA-2048 Declarations
The factorization development starts from a semiprime model that stores two distinct prime factors, their
product, and the consequences needed to recognize a nontrivial divisor. Order finding uses the multiplicative
order supplied by Mathlib [15]. For a sampled unit, the Chinese remainder decomposition relates this order
to the orders modulo the two prime factors. Their powers of two determine the event needed by classical
factor recovery. Under the stated premise on the prime factors, a counting theorem shows that at least half
of the units satisfy that condition. The probability layer assigns an exact weight to every pair of phase and
orbit outcomes. It then restricts the sum to measurements whose continued-fraction candidate equals the true
order and proves a rational lower bound for this event. The generic factoring certificate receives the resulting
success data and selects a returned divisor from the pair carried by the semiprime model.
    The arithmetic path composes reversible addition, multiplication by a fixed unit, and controlled modular
exponentiation. The Vedral–Barenco–Ekert construction [29] supplies the reference progression from addition
to modular exponentiation. In Lean, multiplication by a fixed unit first accumulates a scaled input, swaps
the two data registers, and subtracts a scaled value using the inverse unit. On a clean input, this sequence
leaves the product in the multiplicand register and clears the accumulator and flag. A schedule for modular
exponentiation applies controlled powers of the fixed base, with an inverse step available for cancellation and
cleanup. Correctness, inverse behavior, control branches, and resource projections refer to the selected circuit
objects. Listing 2 records the semantics on a clean input that underlie the certified multiplication circuit. The
complete circuit action and its resource witness are separate declarations.




                                                       17
Lean-QuantumAlg                                                                                         QudeLeap Research



    Listing 2: The semantics on a clean input that underlie the certified multiplication circuit. The definition and theorem
    statement are shown, and the proof is omitted. The complete Circuit.apply theorem lies outside this excerpt.
 def macSwapUncompute {N : N} (u : (ZMod N)× )
     (x : ModularMultiplyAccumulate.Data N) :
     ModularMultiplyAccumulate.Data N :=
   (swapMacRegisters (x.addScaled (u : ZMod N))).subScaled
     ((u−1 : (ZMod N)× ) : ZMod N)

 theorem macSwapUncompute_cleanInput_multiplyByUnit {N : N}
     (u : (ZMod N)× ) (x : ZMod N) :
     macSwapUncompute u (cleanInput x) =
       ({ multiplicand := multiplyByUnit u x,
          accumulator := 0,
          flag := false } : ModularMultiplyAccumulate.Data N) := by
   -- proof omitted

    The Ekerå–Håstad route [19] has its own short discrete logarithm certificate. The certificate accepts the
mass of the recovery event and a bounded classical search witness. The classical layer recovers a half sum,
checks the associated quadratic relation, and proves that the returned value belongs to the stored factor pair.
Its packaged theorem exposes correctness, success, repetition, and resource statements for this route. The
public RSA-2048 endpoint selects the Shor route factoring certificate, fixes three trials, and attaches a logical
resource record. Evaluating and rounding the formulas and table in Ref. [21] gives the values for one run:
6190 logical qubits, 2.7 × 109 Toffoli gates, and 2.14 × 109 measurement depth.
    The public RSA proposition expands these inputs in Listing 3. Its input includes the semiprime factor
model and a proof that the modulus lies in the declared 2048-bit interval. The existential output equals
one of the stored factors. One rational inequality records the lower bound of 2/3 after three trials, and a
second relates that probability to the final failure budget. The retry certificate sets the run count to three.
The resulting totals are 8.1 × 109 Toffoli gates and 6.42 × 109 units of the source measurement depth [21];
Lean stores the latter value in the general circuitDepth field. The proposition also records 36,906 classical
arithmetic operations and two readiness flags supporting the values summarized in Table 1.
    Listing 3: The RSA-2048 public proposition. It records factor recovery, rational success bounds, three-run accounting,
    and logical resources.
 def PublicTheoremShape (input : InputClass) : Prop :=
   ∃ d successNumerator successDenominator : N,
     0 < successDenominator ∧
       (d = input.model.leftFactor ∨
        d = input.model.rightFactor) ∧
       2 * successDenominator <= 3 * successNumerator ∧
       (failureBudget.failureDenominator -
           failureBudget.failureNumerator) * successDenominator <=
         failureBudget.failureDenominator * successNumerator ∧
       2 ^ (modulusBits - 1) <= input.modulus ∧
       input.modulus < 2 ^ modulusBits ∧
       retry.runCount = 3 ∧
       finalSuccessAccountedEnvelope.fields.logicalQubits = 6190 ∧
       finalSuccessAccountedEnvelope.fields.toffoliGates =
         retry.runCount * 2700000000 ∧
       finalSuccessAccountedEnvelope.fields.circuitDepth =
         retry.runCount * 2140000000 ∧
       classicalArithmeticOps = 36906 ∧
       retry.readyForFinalStatement = true ∧
       finalSuccessAccountedEnvelope.readyForFinalStatement = true



B.3 P-256 Declarations
The P-256 development fixes the field modulus, curve coefficients, base point, subgroup order, and cofactor
specified by the National Institute of Standards and Technology [8]. Field elements are residues modulo the
standardized prime, and finite points carry coordinates together with the curve equation. The application
carrier supplies a public key, a private scalar with a range proof, and an abstract scalar multiplication map



                                                            18
Lean-QuantumAlg                                                                                        QudeLeap Research




Table 4: A map from selected Lean declarations to the RSA construction in the manuscript. Here declarations
are grouped by namespace, and each entry in the first column omits the displayed namespace prefix.
 Declaration                            Role in the manuscript
OrderFinding.ShorSourceJoint
 main                                   Bounds the probability of recovering the true order from validated outcomes.
ShorFactoring.SemiprimeFactorModel
 crtGoodBaseCount_atLeastHalf      Counts bases that satisfy the factor recovery condition.
ModularExponentiation
 controlledPowerScheduleCircuit         Builds the controlled powers used by order finding.
Factoring.EkeraHastadStyle
 main_factorization                     Packages the short discrete logarithm factorization route.
Factoring.FormulaEnvelope.RSA2048
 retryAmplificationCertificate          Fixes the success accounting for three runs.
 finalLogicalResourceEstimate           Keeps the logical qubit count fixed and scales gates and depth to three runs.
 main                                   Proves the public RSA-2048 proposition.


that relates them. A bridge interprets this curve data as a discrete logarithm problem in a finite cyclic group.
It equates the relevant orders, maps the generator and target to the base point and public key, and preserves
scalar multiplication. Probability bounds are rational inequalities. The final resource record contains logical
qubits, Toffoli gates, maximal Toffoli depth, and classical operations.
    Shor’s discrete logarithm construction [5] uses two exponent registers. For exponents a and b, its group
action multiplies the workspace by the generator raised to a and the target raised to −b. Fourier readout of
both exponent registers produces a pair of frequencies. A source relation characterizes valid pairs by a linear
congruence, and the classical recovery step solves that congruence when the selected frequency is invertible.
Ref. [7] realizes this architecture with controlled elliptic-curve additions. In Lean, a support certificate supplies
the weight of each outcome, the selected recovery event, proofs that its outcomes satisfy the source relation,
and a rational lower bound on its total weight. The Fourier readout circuit and these outcome weights enter
through supplied fields. The bridge from the cyclic group to the curve and the scalar circuit are further inputs
to the recovery theorem.
    The arithmetic branch begins with witnesses for field addition, inversion, and division on clean inputs.
Each witness states the encoded result, cleanup of its work registers, and the resources of the supplied program.
Division also receives a multiplication program and a proof that it realizes the required field product. Affine
point addition then consumes coordinate programs under the nonexceptional condition for the selected formula.
The controlled version proves the identity action when its control is zero and the prescribed point addition
when the control is one. Scalar multiplication folds these controlled steps over a bit schedule. Its run object
carries the accumulator trace and the validity premise for every scheduled addition. The P-256 field bundle
and the point arithmetic witness occupy separate interfaces. The structured scalar endpoint associates its
action on basis states and resource profile with one folded circuit.
    At the application layer, the comprehensive recovery witness accepts the curve bridge, Fourier support,
scalar oracle certificate, output equalities, and public resources as supplied fields. The scalar oracle certificate
links its clean basis action and resources to one circuit object. The Fourier support supplies the probability
data used to choose and validate the classical output. The public carrier supplies the public point, the private
scalar, and the abstract scalar multiplication map; the endpoint identifies the returned natural number with
that carried scalar. A candidate proof checks the same value against the induced curve problem, and a range
proof places it below the subgroup order. Listing 4 expands this proposition. Its success inequality states a
lower bound of 2/3, and both run multipliers equal one. The resource tuple is 2330 logical qubits, 1.26 × 1011
Toffoli gates, and 1.16 × 1011 maximal Toffoli depth from Ref. [7]. Seven classical operations come from the
local recovery accounting. These fields correspond to Table 2, and the readiness flag marks the completed
numerical record consumed by the public proposition.
    Listing 4: The P-256 endpoint statement and its existential public proposition. They record scalar recovery, a rational
    success bound, and logical resources.
 namespace PublicEndpointWitness

 def Statement (I : P256DomainParameters.ScalarRecoveryInterface)
     (w : PublicEndpointWitness I) : Prop :=
   w.output = I.privateScalar.value ∧



                                                            19
Lean-QuantumAlg                                                                                   QudeLeap Research




Table 5: A map from selected Lean declarations to the P-256 construction in the manuscript. Here declarations
are grouped by namespace, and each entry in the first column omits the displayed namespace prefix.
 Declaration                           Role in the manuscript
P256PrimeFieldBridge.WitnessBundle
 inversionResourceCorrectWitness   Projects inversion semantics on clean inputs and resources.
 divisionResourceCorrectWitness    Projects division semantics on clean inputs and resources.
PrimeFieldShortWeierstrass.ControlledPointAddition
 DecomposedWitness                  Certifies controlled affine point addition.
PrimeFieldShortWeierstrass.ScalarMultiplication.
CertifiedEndpoint.ComposedEndpoint
 Witness                            Associates a scalar schedule with one circuit and its resources.
P256LogicalResources.SameCircuitScalarRecovery
 Witness                            Collects the supplied bridge, probability, circuit, and resource certificates.
P256LogicalResources.PublicTheoremShape
 main                               Constructs the public P-256 proposition.



      w.output < P256DomainParameters.subgroupOrder ∧
      I.toECDLPInstance.CandidateScalar
        (w.output : ZMod I.toECDLPInstance.subgroupOrder) ∧
      2 * w.successDenominator <= 3 * w.successNumerator ∧
      0 < w.successDenominator ∧
      w.resources.logicalQubits = 2330 ∧
      w.resources.toffoliGates = 126000000000 ∧
      w.resources.maximalToffoliDepth = 116000000000 ∧
      w.resources.classicalOps = 7 ∧
      w.resources.toffoliRunMultiplier = 1 ∧
      w.resources.depthRunMultiplier = 1 ∧
      w.resources.readyForFinalStatement = true

 end PublicEndpointWitness

 def PublicTheoremShape
     (I : P256DomainParameters.ScalarRecoveryInterface) : Prop :=
   ∃ witness, PublicEndpointWitness.Statement I witness


B.4 Main Result Assembly
The two branches use the same assembly pattern at their lower circuit layers: a correctness theorem and a
resource witness refer to one circuit object. Their public propositions operate at a higher layer. The RSA
wrapper receives a semiprime model and internally selects the factor and success certificate, retry accounting,
and numerical resource fields. Its values for three runs scale an estimate for one run derived from Ref. [21].
The factor already belongs to the semiprime model, and the probability is represented by exact ratios of
natural numbers. The P-256 wrapper receives a carrier that includes the private scalar, together with a
candidate proof, a rational success bound, and resource equalities. The comprehensive recovery witness can
collect the curve bridge, outcome support, scalar circuit, and resource record before this final step. Each
endpoint states exactly which evidence the application theorem consumes.
    The terminal statements certify conjunctions over mathematical and numerical evidence assembled in
the application layer. The circuit declarations prove local actions on basis states, cleanup, control behavior,
and resources. Number-theoretic certificates turn valid quantum outcomes into factors or scalars. Bridge
records connect finite cyclic groups to elliptic-curve scalar multiplication, and support records provide the
probability data used by classical recovery. This separation makes the input to each theorem visible in its
type and preserves the local association between circuit behavior and circuit resources.
    Readers can audit the construction at three levels. First, the arithmetic statements expose the action of
each circuit on a clean encoded state and the cleanup of work registers. Second, the probability and recovery
statements name the selected event and the algebraic condition that turns an outcome into a factor or scalar.
Third, the terminal propositions display every equality used to report success and resources. On the RSA
circuit branch, this path runs from modular addition through exponentiation to the factoring certificate. On


                                                         20
Lean-QuantumAlg                                                                             QudeLeap Research



the P-256 branch, it runs from field programs through controlled point addition and the scalar schedule to the
supplied recovery witness. The declaration tables locate both endpoints. Listings 3 and 4 make explicit the
certificate boundary behind the numerical claims reported in Sec. 2.




                                                     21
