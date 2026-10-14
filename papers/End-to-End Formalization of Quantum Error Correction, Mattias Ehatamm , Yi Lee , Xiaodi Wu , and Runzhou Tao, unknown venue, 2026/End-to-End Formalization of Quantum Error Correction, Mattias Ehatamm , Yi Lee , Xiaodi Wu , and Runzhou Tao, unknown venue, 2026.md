                                             End-to-End Formalization of Quantum Error Correction
                                                                Mattias Ehatamm , Yi Lee , Xiaodi Wu , and Runzhou Tao
                                                Joint Center for Quantum Information and Computer Science, University of Maryland,
                                                                                  College Park
                                                                 {mehatamm, ylee1228, xiaodiwu, rztao}@umd.edu
arXiv:2605.16523v1 [quant-ph] 15 May 2026




                                                                                                   Abstract
                                                      Quantum error-correcting codes (QECCs) sit between noisy quantum hardware and reliable computa-
                                                  tion, so the code parameters used in practice must be trustworthy. The single number that summarizes
                                                  a code’s strength is its distance, yet certifying a distance lower bound is NP-hard in general, placing it
                                                  beyond the reach of pen-and-paper proofs as well as direct proof-assistant scripting. As a result, distance
                                                  values in the literature come either from non-scaling hand proofs, or from unverified solvers that leave
                                                  a trust gap exactly where the code is supposed to provide a guarantee. We present Lean-QEC, the
                                                  first Lean 4 formalization of stabilizer-code theory that delivers end-to-end, machine-checked distance
                                                  certificates at industrial code sizes. Lean-QEC formalizes the linear algebra of qubit states, the Pauli
                                                  group, stabilizer codes, the binary symplectic representation, classical coding theory, and the CSS and
                                                  Bivariate Bicycle families. To break the combinatorial barrier, Lean-QEC translates the distance
                                                  condition into a Boolean satisfiability formula through a verified reduction. The pipeline scales through a
                                                  BitVec-flattened encoding that replaces Lean’s Matrix representation, and an error-location encoding
                                                  that reduces the variable count from n to k⌈log2 n⌉. With these, we obtain automatically-generated
                                                  Lean-checked distance proofs for a large range of industrially viable qLDPC codes within the Bivariate
                                                  Bicycle and Generalized Bicycle families, including J90, 8, 10K and J70, 6, 9K BB codes, with the formulation
                                                  scaling up to 144 qubits when performed outside the Lean kernel. The resulting library is reusable and is
                                                  designed to plug into broader Lean-based efforts toward end-to-end verification of fault-tolerant quantum
                                                  computation.


                                            1    Introduction
                                            Quantum computing promises asymptotic speedups on classically intractable problems in cryptography,
                                            simulation, optimization, and chemistry [26, 5, 20, 13]. Realizing those speedups on real hardware, however,
                                            is constrained by noise: every physical qubit decoheres and every physical gate is imperfect [25], so the only
                                            known route to scalable computation passes through a thick layer of quantum error correction (QEC). Recent
                                            experimental demonstrations of QEC on superconducting and trapped-ion platforms [1, 24, 2] have made this
                                            layer a load-bearing component of the quantum stack rather than a theoretical curiosity, and have accordingly
                                            raised the bar for the trust placed on it.
                                                The classical engineering response to such load-bearing code is testing, but testing is essentially unavailable
                                            for quantum programs. Output distributions are exponentially expensive to sample, intermediate measure-
                                            ments collapse the very state under inspection, and the noise that motivates correction also corrupts any
                                            would-be observation. The remaining option is to formally verify the QEC layer [10, 27]: state its guarantees
                                            as theorems and discharge them in a proof assistant whose kernel can be independently trusted.

                                            Why the distance number is hard to trust. The most informative single parameter of a stabilizer
                                            code is its distance d: the minimum Pauli weight of an undetectable error. A code with distance d corrects
                                            ⌊(d − 1)/2⌋ errors, so distance is the value most often quoted when codes are compared and the value on
                                            which fault-tolerance thresholds depend. Yet certifying a distance lower bound is computationally hard: even
                                            for classical linear codes the problem is NP-complete [29], and for stabilizer codes lacking strong symmetry


                                                                                                       1
the situation inherits the same intractability [17]. The values quoted in the literature therefore come from
one of two unsatisfying places:
 • Hand proofs inside a proof assistant. Existing developments such as the 9-qubit Shor-code verifica-
   tion [11] enumerate every Pauli error explicitly. The bookkeeping — 3n single-qubit error patterns plus
   all of their combinations — has so far prevented this style from scaling past nine qubits, well short of any
   code used in current experiments.
 • Unverified symbolic computation. ILP solvers, custom search routines, or computer-algebra scripts
   can in principle handle larger codes [30], but their outputs sit entirely outside the proof kernel. A distance
   value pasted from such a tool is the moral equivalent of a numerical constant trusted on faith.
Neither option is end-to-end: the first does not scale, and the second leaves a trust gap at exactly the point
the code is meant to provide a guarantee.

Why end-to-end matters. A pragmatic shortcut is to declare a stabilizer code by its binary symplectic
representation and treat distance as a property of that matrix. This makes the math tractable, but it
shifts the trust to an informal equivalence between two definitions — the matrix view and the original
quantum-theoretic view in which a stabilizer code is the simultaneous +1 eigenspace of a set of Pauli matrices.
A genuinely trustworthy artifact must close that loop inside the proof kernel: distance bounds proved over
the matrix view must transport, by a machine-checked theorem, to the eigenspace view.

Our approach. We present Lean-QEC, a Lean 4 library that builds the stabilizer-code stack end-to-end
and discharges distance certificates against industrial-scale codes by combining the proof assistant with an
external SAT solver. The library covers the linear algebra of qubit states, the Pauli group with phases, stabilizer
codes, the binary symplectic representation, classical coding theory, CSS codes, and the Bivariate Bicycle
(BB) family. Each abstraction layer is connected to the next by a machine-checked correspondence theorem,
so a distance bound established on a binary symplectic matrix is also a theorem about the corresponding
quantum code.
    For the computationally hard step, Lean-QEC reduces “distance ≥ d” to the unsatisfiability of a Boolean
formula via a Lean-verified translation, hands the formula to CaDiCaL through Lean’s bv_decide tactic, and
reconstructs the resulting LRAT certificate as a Lean proof term. The trusted base remains Lean’s kernel
plus the LRAT checker; the SAT solver itself is not trusted.
    Making this pipeline scale required two non-obvious design moves, both of which we present as contributions
in their own right:
1. Instantiating the Boolean formula directly through Mathlib’s Matrix type exhausts memory well before
   reaching the [[90, 8, 10]] BB code. We introduce a BitVec-flattened intermediate representation, prove it
   consistent with the Matrix-based reference, and use it to carry the encoding past the 90-qubit mark.
2. Even with an efficient encoding, a one-Boolean-per-qubit error variable produces a formula whose solver
   runs become intractable beyond about 90 qubits. We instead let the variables encode the locations of
   the (at most d − 1) nonzero error entries, shrinking the variable count from n to k⌈log2 n⌉. For the
   [[144, 12, 12]] BB code this is 88 variables versus 144 — a difference that makes 144 qubits tractable
   outside the kernel in minutes.

Contributions.      Our contributions are as follows.
1. An end-to-end Lean 4 formalization of stabilizer-code theory. We give a machine-checked
   development that connects qubit states, the Pauli group with phases, stabilizer codes, the binary
   symplectic representation, and classical coding theory, with explicit correspondence theorems between
   adjacent layers (Section 3).

2. A verified reduction from code distance to Boolean satisfiability. We formalize a translation from
   the stabilizer-theoretic distance condition to an UNSAT query, prove the reduction sound in Lean, and
   integrate it with Lean’s bv_decide tactic so the SAT certificate is reconstructed in the kernel (Section 4).


                                                        2
                                           Programmer
                   Verification
                  Infrastructure
                                            Quantum                         This Work
                   Algorithmic              Program
                                                                 End-to-End Lean Environment
                     Theory
                                        Compiler
                                            TextPasses
                                                                    Error
                                                                                   Quantum Info
                                                                  Correction
                                       Quantum Circuit                               Theory
                                                                   Theory

                                                                 Computer Verification of Code
                                                                          Properties

                            Error-Corrected
                                                                     Circuit Implementation
                            Quantum Circuit


                                Quantum
                                Hardware
                                      Noise + Error Correction
                                 Output
                               (Quantum)


Figure 1: Verification workflow for fault-tolerant quantum programs. Lean-QEC occupies the QEC layer of
this pipeline.


3. Two scalability techniques. A BitVec-based intermediate representation, verified consistent with
   the Matrix encoding, lets the formula instantiation reach industrial code sizes; a location-indexed error
   encoding cuts the SAT variable count from n to k⌈log2 n⌉ (Section 4.1).
4. Lean-checked distance certificates for practical codes. We instantiate the pipeline on industrially
   viable codes like the [[90, 8, 10]] Bivariate Bicycle code of [7] and the [[70, 6, 9]] BB code of [28], and report
   the resource envelope outside Lean for the Gross Code of size [[144, 12, 12]]. Each case study is between
   100 and 200 lines of Lean script and follows a uniform template (Section 5), which may be automatically
   generated by a Python script given the code description.

Comparison. Table 1 summarizes how Lean-QEC sits relative to the two existing options. Hand-written
ITP proofs of distance close the trust loop but stall well below twenty qubits; unverified solver pipelines
reach industrial codes but never enter the kernel. Lean-QEC closes the loop and reaches industrial codes by
paying for the solver call with a verified reduction and a reconstructed certificate.


                      Table 1: Comparison of verification approaches for QEC distance.
   Approach                            Theory verified?      Scales to large codes?      End-to-end checked?
   Hand-written ITP proofs                    Yes            No (n > 20 prohibitive)               Yes
   Unverified symbolic computation            No                      Yes                          No
   Lean-QEC (this work)                       Yes               Yes (∼240 cases)                   Yes



                                                         3
    The rest of the paper develops Lean-QEC in the order a quantum researcher would encounter the
abstractions: Section 2 introduces just enough Lean to follow the formalization; Section 3 builds the QEC
stack with explicit attention to the type-theoretic gaps that arise when formalizing standard quantum-
information arguments; Section 4 presents the SAT-assisted distance pipeline; Section 5 reports the case
studies; and Section 6 discusses related work and limitations.


2    Background
This section gives some background Lean and formal verification for Sections 3 and 4. We assume familiarity
with quantum error correction and standard linear algebra. For more details please refer to [4].

Lean 4 and Mathlib. Lean 4 [10] is an interactive theorem prover (ITP) and a dependently typed functional
programming language whose underlying logic is the Calculus of Inductive Constructions. Statements and
proofs are both first-class objects: a proof of a proposition P is a value whose type is P . Once Lean has
accepted a proof, the only assumptions a reader needs to discharge are (i) that the Lean statement faithfully
captures the intended informal claim and (ii) that Lean’s small, independently audited kernel is correct.
    The standard library Mathlib [27] now contains close to two million lines of formalized mathematics and
underpins large efforts such as the Prime Number Theorem [18] and Fermat’s Last Theorem [8] projects. We
rely on Mathlib for matrices, finite-dimensional vector spaces, group theory, unitary groups, and the Kronecker
product; conversely, our development is designed to be portable back into Mathlib as quantum-information
content matures there.

Formalizing Math with an ITP. A Lean proof is a sequence of tactics that incrementally transforms
the goal, and any informal pen-and-paper argument can be translated by spelling out the steps the human
reader would otherwise fill in. The friction sits in those omitted steps: edge cases that the prose dismisses
with “clearly,” implicit coercions between mathematically equivalent representations, and definitions whose
set-theoretic phrasing is awkward in type theory.

    Example: Proving Distance in Lean
    For a concrete Lean example we revisit a definitional edge case that arises in our own development.
    The distance of a quantum error-correcting code is the minimum Pauli weight of an undetectable error,
    but a minimum over the empty set is undefined; we must pick a convention for codes whose only valid
    codeword is 0n . We follow the standard “n + 1” convention, which makes the distance well-defined
    while reserving the literal value n + 1 as a sentinel for the trivial case.
    Definition: Given an error-correcting code C, let S ⊆ Pn be the set of undetectable Pauli errors. We
    then define the distance by           (
                                            minP ∈S (weight(P )) if S ̸= ∅
                                      d=                                                              (1)
                                            n+1                    if S = ∅
    The sentinel value makes the following sanity check immediate, but only after the case split is made
    explicit.
    Lemma: If the distance d of a code over n qubits satisfies d ≤ n, then its set S of undetectable errors
    is nonempty.

    Proof. Suppose S = ∅ for contradiction. By the definition of code distance, we have d = n + 1,
    contradicting d ≤ n.
    A corresponding Lean proof mirroring step-by-step the above informal argument would be written as:

        lemma BinSympMatrix.undetectable_set_nonempty {k n : N}
            (B : BinSympMatrix k n) (hk : 0 < k)
            (h_dist : B.distance hk ≤ n) :
          B.undetectable_set.Nonempty := by




                                                      4
             by_contra h_empty
             rw [Finset.not_nonempty_iff_eq_empty] at h_empty
             unfold BinSympMatrix.distance at h_dist
             rw [h_empty] at h_dist
             simp at h_dist

    This proof may be read as follows: by_contra introduces the contradiction hypothesis; Finset.
    not_nonempty_iff_eq_empty converts “non-emptiness” into a Finset-level equation that Mathlib has
    lemmas about; unfold and rw apply the definition and the empty-set hypothesis; simp discharges
    the residual arithmetic against d ≤ n. The mechanical overhead, which involves naming the empty-
    set lemma and finding the right lemmas to rewrite with, is representative of what formalizing a
    pen-and-paper QEC argument feels like in practice.



3     Formalization of Quantum Error Correction
This section builds the stack from Figure 2 bottom-up: qubit states, n-qubit unitaries, the Pauli group with
phases, the binary symplectic representation, abstract QEC codes, stabilizer codes, and finally the CSS
and Bivariate Bicycle families. For each layer we describe the formalization choice, the machine-checked
correspondence to the layer below, and the type-theoretic friction that distinguishes the Lean development
from a pen-and-paper account. The chain of correspondences ending at the binary symplectic matrix is what
makes the SAT-based distance pipeline of Section 4 end-to-end: a distance bound discharged at the bottom
transports, by a Lean theorem, to a bound on the quantum code at the top.

3.1        Qubit States
The SQIR development [14] and CoqQ [32] formalize quantum states in Rocq Prover, and the Lean-
QuantumInfo project [21] formalizes general finite-dimensional quantum states in Lean. None of these
specialize the state space to qubits in the way we need, so we start the stack ourselves.

Choice of index set. A textbook quantum researcher writes a pure state as |ψ⟩ = x∈{0,1}n αx |x⟩, i.e. as
                                                                                     P
                                                                                               n
an assignment of amplitudes to bit strings. A textbook formalizer writes it as an element of C2 . The two
views are isomorphic, but Lean represents a finite-dimensional vector by its function form

                                           Fn ∼
                                              = Fun(Nn , F),           Nn = {0, 1, . . . , n − 1},                                   (2)

and the choice of index set is a load-bearing design decision: every later definition is parametrized by it. We
                       n                                                         n
diverge from SQIR’s C2 convention and adopt Fun({0, 1}n , C), written C{0,1} with the usual normalization.


                                               Classical Error
                                                 Correction                                                  BB Codes

                                                                                                 CSS Codes              Automated SAT
             Tensor Products
 Mathlib                                                                                                                   Distance
                and Phase
                                                                                                                          Verification
                                Unitary                          Quantum Error-     Stabilizer
                                Matrices                         Correcting Codes   Formalism

                                                  Pauli
                 Lean-         Pure States       Operators
              QuantumInfo      and Qubits



                                                                                                                        Dependencies
                                                                                                                        Quantum Theory
                                                                                                                        Linear Algebra




Figure 2: Map of the formalized quantum-error-correction stack. Arrows are machine-checked correspondence
theorems; the rightmost layer feeds into the SAT-based distance pipeline of Section 4.


                                                                       5
The payoff is that tensor products on basis states become string concatenation, |101⟩ ⊗ |001⟩ = |101001⟩,
instead of an arithmetic identity on bit-shifts; this matters because Pauli operators are most naturally indexed
by which qubit they act on, not by a position in a flattened 2n -array.

3.2    Quantum Operators
For the purpose of QEC we do not need a full circuit DSL; we only need to compose states and operators
consistently. The single property we require is

                                (U1 ⊗ U2 )(|ϕ1 ⟩ ⊗ |ϕ2 ⟩) = (U1 |ϕ1 ⟩) ⊗ (U2 |ϕ2 ⟩),                         (3)

together with associativity of ⊗ on operators. The Lean development for a richer gate-level circuit calculus is
left to future work.

Tensor vs. Kronecker. Equation (3) hides a vocabulary issue. The product on states is a tensor product
of vectors; the product on operators is a Kronecker product of matrices. Mathlib distinguishes them as
two different functions, and the abstract isomorphism connecting the two passes through tensor-algebra
machinery we would otherwise have to drag through every proof. We sidestep this by formalizing every “⊗”
in our development as a Kronecker product, with vectors viewed as n × 1 matrices when needed. This makes
Equation (3) a direct corollary of a Mathlib lemma rather than a tour through Mathlib’s tensor-algebra
hierarchy.

Index alignment.      Matrices in Mathlib are functions on index pairs,

                                            Fm×n ∼
                                                 = Fun(Nm × Nn , F),                                         (4)

and Mathlib’s Kronecker product is defined accordingly: for M1 ∈ FI1 ×J1 and M2 ∈ FI2 ×J2 ,

                            (M1 ⊗ M2 )((i1 , i2 ), (j1 , j2 )) = M1 (i1 , j1 ) · M2 (i2 , j2 ).              (5)

For an n1 -qubit operator U1 and an n2 -qubit operator U2 , the index type produced by this definition is
{0, 1}n1 × {0, 1}n2 , whereas the index type of an (n1 + n2 )-qubit operator is {0, 1}n1 +n2 . The two are equal
up to the isomorphism {0, 1}n1 × {0, 1}n2 ∼= {0, 1}n1 +n2 that concatenates bit strings, but Lean’s dependent
type system does not coerce them implicitly. We discharge this gap by a one-time concatenation/splitting
bijection; every later lemma uses operators indexed by {0, 1}n uniformly.

Heterogeneous equality. Associativity of ⊗ on operators, (U1 ⊗ U2 ) ⊗ U3 = U1 ⊗ (U2 ⊗ U3 ), is well-formed
on paper but not in Lean: the LHS has type indexed by (n1 + n2 ) + n3 qubits and the RHS by n1 + (n2 + n3 ),
and N’s addition is not associative definitionally. Other formalizations work around this with explicit cast
functions sprinkled through every proof. Lean’s Mathlib provides a cleaner option, heterogeneous equality: the
equation is stated between values of provably-equal types, and the type checker accepts it once the type-level
equality has been discharged. We use this idiom throughout the development.

Unitarity. Mathlib already supplies the unitary-group structure on square matrices, and Lean-QuantumInfo
uses it as well; we inherit it directly. Wrapping our Kronecker-based operators in Mathlib’s unitary group
introduces no additional conceptual challenges, only boilerplate that we have written once.

3.3    Pauli Group
Quantum errors in our setting are decomposed into Pauli operators, so the Pauli group is the first non-trivial
structure in the QEC stack. The standard X x Z z shorthand — “apply X to qubits with xi = 1 and Z
to qubits with zi = 1” — is convenient for pen-and-paper arguments: the tensor product becomes string
concatenation, X x1 Z z1 ⊗ X x2 Z z2 = X x1 ∥x2 Z z1 ∥z2 , and the matrix product becomes qubit-wise. The same
shorthand also underlies the binary symplectic representation of Section 3.4.



                                                            6
                                        P, P ′                               P ⊗ P′

                                            unfold                                  unfold


                             (γ, {Pi }i ), (γ ′ , {Pi′ }i )        (γγ ′ , {Pi }i ++ {Pi′ }i )

                            Figure 3: Tensor product of unfolded Pauli operators


What the shorthand omits. Two gaps prevent us from using the X x Z z form directly as a Lean definition.
     • It describes a recipe for building a unitary one qubit at a time, not a single matrix in U{0,1}n . The
       Lean development needs the global matrix to state and prove e.g. commutation lemmas.
     • It ignores global phase. The standard Pauli group contains Y = −iXZ and the anticommutation
       identity ZX = −XZ depends on the sign; neither is expressible without phases. Restricting to the
       multiplicative subgroup ⟨X, Z⟩ does not recover Y .
We close both gaps explicitly. We start from the single-qubit Pauli matrices and define a folding function
that turns a phase factor and an n-tuple of single-qubit Paulis into a single n-qubit unitary. The Pauli group
is then the image of this function.
Definition 3.1 (Single-qubit Pauli gates). We define the following four unitary matrices (acting on the basis
{ |0⟩ , |1⟩ }) as the single-qubit Pauli gates.
                                                                            
                                 1 0             0 1         0 −i            1 0
                           I=             X=           Y =             Z=
                                 0 1             1 0         i 0             0 −1

    The folding step assembles an n-tuple of single-qubit Paulis together with one of the four phase factors
{1, i, −1, −i} into a single n-qubit unitary.
Definition 3.2 (Pauli folding). For each n ∈ N, define

                             PauliFoldn : {1, i, −1, −i} × {I, X, Y, Z}n → U{0,1}n

by                                                                       O
                                             PauliFoldn (γ, P⃗ ) = γ ·       Pi .                            (6)
                                                                         i

Definition 3.3. The n-qubit Pauli group is the image of PauliFoldn :

                                                 Pn = Image(PauliFoldn ).                                    (7)

    This is equivalent to the textbook definition. A common alternative is to quotient by global phase and
work with equivalence classes; we prefer the image-of-fold form because it lets us write down a single matrix
rather than a coset representative, which keeps later proofs computable.
    We verify three properties of PauliFold that drive the rest of the development.
    First, PauliFold is a bijection. Every Pauli operator therefore has a unique γ · X x Z z form. This matters
for the distance pipeline of Section 4.1: distance is defined as the minimum Pauli weight of an undetectable
error, which is only well-defined when each operator has a canonical decomposition.
    Second, PauliFold respects products. The diagram in Figure 3 commutes for ⊗ on operators, and an
analogous diagram commutes for ordinary matrix product once phase factors are collected. These commutation
theorems are what let later proofs argue at the γ · X x Z z level even though the underlying definition lives at
the matrix level. As a byproduct we also obtain closure under multiplication.
    Third, commutation reduces to a single bit. Whether two Paulis X x1 Z z1 and X x2 Z z2 commute or
anticommute is what determines whether an error is detectable by syndrome measurements (Section 4.1); we
formalize the local check on the single-qubit case first and then lift.



                                                              7
Lemma 3.4 (Characterization of single-qubit Pauli commutation). We define the anti-commutation indicator
function as                              (
                                            0 if P = I ∧ Q = I ∧ P = Q
                              ϕ(P, Q) =                                                              (8)
                                            1 otherwise
For all P, Q ∈ { I, X, Y, Z }, we then have

                                              P Q = (−1)ϕ(P,Q) QP.

   The n-qubit case is the XOR of the single-qubit indicators.
Lemma 3.5 (Characterization of Pauli commutation). Let P, Q ∈L  Pn , and let Pi , Qi ∈ {I, X, Y, Z} be the
                                                                 n
components acting on the i-th qubit. Then P Q = (−1)a QP for a = i=1 ϕ(Pi , Qi ).
    The commutation check is implemented as a computable function: ϕ is defined by a case split, not via an
existential quantifier, and the development avoids the axiom of choice. When the Lean elaborator encounters
a concrete pair of Paulis, ϕ reduces to a Boolean value automatically and downstream proofs simplify without
further work. This is the property that allows the SAT translation of Section 4 to discharge concrete distance
queries by unfolding rather than by a chain of rewrites.

3.4     Binary Symplectic Representation
The four single-qubit Pauli matrices are encoded in two bits via the standard isomorphism

                           I ↔ (0 | 0),   X ↔ (1 | 0),       Z ↔ (0 | 1),   Y ↔ (1 | 1),

under which phaseless Pauli multiplication becomes vector addition over F22 and commutation is detected by
the symplectic product
                                      (a | b) ⊙ (c | d) = ad − bc ∈ F2 ,
with 0 for commutation and 1 for anticommutation. Lifting to n qubits gives a representation in F2n
                                                                                                 2 and the
inner-product form
                                    (a | b) ⊙ (c | d) = a · d − b · c ∈ F2 ,
where a, b, c, d ∈ Fn2 . As a sanity check, X ⊗ X ⊗ I = (110 | 000) and Z ⊗ Y ⊗ I = (010 | 110) have symplectic
product 0, so they commute despite the two qubits on which they anticommute pairwise.

Two weight functions. The Binary Symplectic representation supports two distinct weight notions, and
confusing them silently changes which distance is being computed. The Pauli weight of a vector (x | z) counts
the qubits at which (xi , zi ) ̸= (0, 0), which is equivalently the number of qubits at which the encoded operator
is not I. The binary weight is the Hamming weight of x plus the Hamming weight of z and over-counts the Y
positions. Distance arguments require the Pauli weight; we expose both functions and prove the relationship
between them.

      abbrev BinSympPauli (n : N) := (Fin n → (ZMod 2)) × (Fin n → (ZMod 2))

      def union_weight (v1 v2 : Fin n → (ZMod 2)) : N := hammingNorm (fun i => ZMod2_or (v1 i) (v2
           i))

      def BinSympPauli.weight {n : N} (bsp : BinSympPauli n) : N := hammingNorm bsp.1 +
          hammingNorm bsp.2

      def symplecticProd {n : N} (bp1 bp2 : BinSympPauli n) : (ZMod 2) :=
        dotProduct bp1 .1 bp2 .2 + dotProduct bp1 .2 bp2 .1

    The correspondence between the Pauli group and its Binary Symplectic representation is built on top of a
single-qubit equivalence, which we then lift qubit-wise. The correspondence is exact in one direction — every
binary symplectic vector decodes to a definite phaseless Pauli — but loses phase in the other; we therefore
expose a backwards correctness statement that is itself quantified over an unknown phase.


                                                         8
      def Z2Z2_Pauli_equiv : ((ZMod 2) × (ZMod 2)) ≃ Pauli

      def BinSympPauli_toPauli {n : N} (bs : BinSympPauli n) : PauliGroup_group n :=
        let pm := fun n => Z2Z2_Pauli_equiv (bs.1 n, bs.2 n)
        foldPauli (pgphase_1, pm)

      def Pauli_toBinSymp {n : N} (P : PauliGroup_group n) : BinSympPauli n :=
        let pm := fun n => Z2Z2_Pauli_equiv.symm (P.map n)
        ⟨fun n => (pm n).1, fun n => (pm n).2⟩

      theorem Pauli_to_BinSymp_correct {n : N} (P1 P2 : PauliGroup_group n) :
        Pauli_toBinSympPauli (P1 * P2 ) = (Pauli_toBinSympPauli P1 ) + (Pauli_toBinSympPauli P2 ) :=
          sorry

      theorem BinSympPauli_to_Pauli_correct {n : N} {bp1 bp2 : BinSympPauli n} :
        ∃ p : (pgroup_phases), U_phase (BinSympPauli_toPauli (bp1 + bp2 )).1 p = ((
          BinSympPauli_toPauli bp1 ) : Un [n]) * (BinSympPauli_toPauli bp2 )

      theorem commutes_of_sympProd_zero {n : N} {bp1 bp2 : BinSympPauli n}
        (h_prod : symplecticProd bp1 bp2 = 0) : commute (BinSympPauli_toPauli bp1 ) (
          BinSympPauli_toPauli bp2 )

   The signature of BinSympPauli_to_Pauli_correct reflects this phase loss: the equality is quantified over
a phase p ∈ {±1, ±i} such that the two unitaries agree after p is applied. Commutation, in contrast, is
phase-insensitive, so commutes_of_sympProd_zero states the implication cleanly. This is the crucial property
we use later: distance arguments care only about commutation with stabilizers, so the loss of phase in the
symplectic encoding does not cost us any soundness.

3.5     Quantum Error Correction
A quantum error-correcting code can be defined at several levels of generality. We expose two and use
whichever is convenient at each layer of the development.
Definition 3.6 (Quantum Error-Correcting Code, [12]). A Quantum Error-Correcting Code is a pair
                                       k    n
(U, E) where U is a partial isometry C2 → C2 (an inner-product preserving map) and E is a set of linear
         n      m
maps C2 → C2 . U is the encoding function, while E is the set of correctable errors. This is a valid
QECC if:
                             m       k
                     ∃(D : C2 → C2 ), ∀E ∈ E, D(EU |ψ⟩ ⟨ψ| U † E † ) = c(E, |ψ⟩) |ψ⟩ ⟨ψ|
   Read informally: a decoder exists that returns the encoded state to its original form modulo an error-
and-state-dependent scalar. The definition is general but inconvenient in a formalized setting because it
bakes in both an encoder and a list of correctable errors. In Lean, we prefer to keep the code space, the
encoder, and the error set as separate objects and bundle them only when needed. The following equivalent
characterization makes this separation natural.
                                                             n                         n      m
Definition 3.7. Given (Q, E), where Q is a subspace of C2 , and E is a set of maps C2 → C2 , (Q, E) is a
QECC iff ∀ |ψ⟩ , |ϕ⟩ ∈ Q, ∀Ea , Eb ∈ E:

                                         ⟨ψ| Ea† Eb |ϕ⟩ = Cab ⟨ψ|ϕ|ψ|ϕ⟩
    Pen-and-paper QEC drops the encoder when the logical labeling is irrelevant and works with the code
space alone. The Lean development pays a real cost for keeping an encoder around: every lemma must thread
it as an explicit argument even when nothing in the lemma uses it. We therefore strip both the encoder and
the error set out of the core type and re-attach them only when needed. The result is a code space alone,
                                      n
which cannot be a Submodule of C{0,1} because our PState type already carries the normalization condition;
we use Set (PState n) instead.


                                                       9
      abbrev QCodeSpace (n : N) := Set (PState n)



3.6     Stabilizer Codes
Every code we care about in practice — and every code we verify in Section 5 — is a stabilizer code, the
specialization of the subspace definition where the code space is determined by a commuting subgroup of
the Pauli group. The rest of this subsection builds the stabilizer-code abstraction on top of the Pauli-group
infrastructure of the previous subsections.
                                             n
Definition 3.8. Given a subspace Q of C2 , the stabilizer S(Q) is:

                                   S(Q) = {A ∈ Pn : ∀ |ψ⟩ ∈ Q, A |ψ⟩ = |ψ⟩

   S(Q) is a subgroup: closure follows from U V |ψ⟩ = U |ψ⟩ = |ψ⟩, inverses are inherited from the Pauli
group, the subgroup is abelian, and −I ∈
                                       / S(Q) for any nontrivial Q. The map runs the other way as well: an
abelian subgroup of the Pauli group that does not contain −I determines a code space.
Definition 3.9. The Codespace corresponding to stabilizer subgroup S is:

                                      T (S) = {|ψ⟩ : ∀A ∈ S, A |ψ⟩ = |ψ⟩}
   Phaseless Pauli operators have eigenvalues ±1, so T (S) is exactly the simultaneous +1 eigenspace of S.
Definition 3.10. A stabilizer code is a QECC (Q, E) where T (S(Q)) = Q.

   Stabilization and its closure properties follow directly from the Pauli-group infrastructure of Section 3.4.

      def stabilizes (U : Un [n]) (ψ : PState n) := ψ.apply U = ψ

      theorem stab_prod {U1 : Un [n1 ]} {U2 : Un [n2 ]} {ψ 1 : PState n1 } {ψ 2 : PState n2 }
        (hs1 : stabilizes U1 ψ 1 ) (hs2 : stabilizes U2 ψ 2 ) :
        stabilizes (U1 ⊗n U2 ) (ψ 1 ⊗p ψ 2 )

      theorem inv_stab {U : Un [n]} {ψ : PState n} (hstab : stabilizes U ψ) : stabilizes U−1 ψ

      theorem mul_stab {n : N} {U1 U2 : Un [n]} {ψ : PState n} (hstab1 : stabilizes U1 ψ) (hstab2 :
           stabilizes U2 ψ) : stabilizes (U1 * U2 ) ψ

    On top of the abstract QECC definition, a stabilizer code bundles together (i) a code space, (ii) a
commuting subgroup of the Pauli group, and (iii) a proof that the subgroup stabilizes the code space.
Carrying the commutativity proof inside the structure makes downstream proofs shorter, avoiding re-deriving
it at every use site.

      structure StabCode (n : N) where
        space : QCodeSpace n
        stabs : Subgroup (@PauliGroup_group n)
        h_comm : IsMulCommutative stabs
        hstab : ∀ ψ ∈ space, ∀ S ∈ stabs, stabilizes S ψ

   The condition −I ∈/ stabs is derivable from this definition but we leave it implicit. Code constructions
almost always specify a stabilizer group by its generators rather than as a fully expanded subgroup, so
we provide two structures for the generators: StabSet for an arbitrary commuting set of generators, and
NormalizedStabSet for the common case where all generators have phase +1.

      structure StabSet (n : N) where
        stabs : Finset (PauliGroup_group n)
        comm : ∀ s1 ∈ stabs, ∀ s2 ∈ stabs, commute s1 s2


                                                       10
    structure NormalizedStabSet (n : N) extends StabSet n where
      norm: ∀ s ∈ stabs, PauliGroup.phase s = pgphase_1

    def StabCode_of_StabSet {n : N} (S : StabSet n)
     : StabCode n where
       space := {ψ | ∀ s ∈ S.stabs, stabilizes s ψ}
       stabs := Subgroup.closure (SetLike.coe S.stabs)
       h_comm := ...
       hstab := ...

    A stabilizer code corrects errors by projectively measuring the generators of its stabilizer group; the
eigenvalues observed form the syndrome. A simple-minded definition of “detectable” would require every
correctable error to have a unique syndrome, but the Shor [[9, 1, 3]] code shows this is too strong: as Table 2
indicates, Z on qubit 1 and Z on qubit 2 produce the same syndrome (both flip only M7 ), yet they correct
identically because their product lies in the stabilizer group. The right notion of “undetectable” must therefore
exclude errors that act trivially on the code space, not merely those with non-unique syndromes.


                          Table 2: Stabilizer Generators for the [[9, 1, 3]] Shor Code
                         Generator         Type        Operator String (Q1 . . . Q9 )
                              M1         Phase-Flip           ZZI III III
                              M2         Phase-Flip           IZZ III III
                              M3         Phase-Flip           III ZZI III
                              M4         Phase-Flip           III IZZ III
                              M5         Phase-Flip           III III ZZI
                              M6         Phase-Flip           III III IZZ
                              M7          Bit-Flip          XXX XXX III
                              M8          Bit-Flip          III XXX XXX


Definition 3.11. The normalizer of a stabilizer S is N (S) = {A ∈ Pn : ∀B ∈ S, AB = BA}.

   A Pauli error that commutes with every stabilizer is invisible to syndrome measurement and maps the code
space to itself. The stabilizer group is abelian, so its own elements always commute with all stabilizers; these
elements act trivially on the code space and must be excluded. The remaining elements are the normalizer
minus stabilizer, which are exactly the errors that escape detection while still changing the encoded state.

Definition 3.12. The undetectable set of a stabilizer code with stabilizer S is N (S) \ S. The distance is the
minimum Pauli weight over the undetectable set. A code of distance d corrects ⌊(d − 1)/2⌋ errors.
   These map directly into Lean.

    def StabCode.normalizer {n : N} (SC : StabCode n) : Finset (PauliGroup n) := {N | ∀ s ∈ SC.
        stabs, commute N s}

    def StabCode.undetectable {n : N} (SC : StabCode n) (E : PauliGroup n) : Prop := E ∈ SC.
        normalizer ∧ E ∈/ SC.stabs ∧ PauliGroup.normalized E

    def StabCode.undetectable_set {n : N} (SC : StabCode n) : Finset (PauliGroup n) := {E | SC.
        undetectable E}

    def StabCode.distance {n : N} (SC : StabCode n) (hnt : SC.nontrivial) : N := Finset.min’ (
        Finset.image (fun E => pauli_weight E) SC.undetectable_set)
     (Finset.image_nonempty.2 (StabCode.undetectable_set_nonempty SC hnt))




                                                       11
    Two details in the Lean definition deserve comment. The argument hnt to StabCode.distance establishes
that the undetectable set is nonempty, so the minimum is well-defined (cf. the sentinel discussion of Section 2).
And StabCode.undetectable restricts attention to phase-+1 Paulis; without this, −I would appear as an
undetectable element of every code — it commutes with all stabilizers, is not itself a stabilizer, yet acts
trivially on the code space. Because commutation is phase-insensitive, this restriction loses no genuine errors.

Binary symplectic matrix. Applying the binary symplectic representation to a minimal generating set of
a stabilizer code yields a binary symplectic matrix (BSM): two F2 matrices, one for the X-component and
one for the Z-component, with rows that are linearly independent and have pairwise symplectic product zero.
An undetectable error in this representation is a vector with symplectic product zero against every row that
does not itself lie in the row space.

      structure BinSympMatrix (k n : N) where
        X : Matrix (Fin k) (Fin n) (ZMod 2)
        Z : Matrix (Fin k) (Fin n) (ZMod 2)

      def BinSympMatrix.toStabSet {n k : N} (bsm : BinSympMatrix k n) (h_comm : bsm.isCommuting) :
          NormalizedStabSet n where
        stabs := Finset.image (fun i => BinSympPauli_toPauli (bsm.row i)) Finset.univ
        comm := --
        norm := --

      def BinSympMatrix.undetectable {k n : N} (B : BinSympMatrix k n) (bsp : BinSympPauli n) :
          Prop :=
        (∀ i, symplecticProd (B.row i) bsp = 0) ∧ bsp ∈
                                                      / B.rowSpace

      def BinSympMatrix.distance {k n : N} (B : BinSympMatrix k n) (hk : 0 < k) : N := Finset.min’
           (B.undetectable_set.image BinSympPauli.weight)
      (Finset.image_nonempty.2 (B.undetectable_set_nonempty hk))

  The end-to-end story rests on the following correspondence theorem, which is the bridge that transports
SAT-discharged distance bounds (at the BSM level) into theorems about the quantum stabilizer code.

      theorem BinSympMatrix.distance_eq_distance {k n : N} (B : BinSympMatrix k n) (h_comm : B.
          isCommuting) (hk : 0 < k) :
        (StabCode_of_BinSympMatrix B h_comm).distance (B.toStabCodeNontrivial_of_k_pos h_comm hk) =
        B.distance hk

    The BSR loses phase information. For distance arguments this loss is harmless. An error is an error
regardless of phase, and commutation against stabilizers is phase-insensitive, but other quantum-theoretic
claims (e.g. relations like XZ = iY ) become false at the BSR level. In Lean this means correspondence
theorems are stated carefully and we never accidentally lift a phase-dependent fact from one representation
to the other.

3.7     CSS and BB Codes
CSS codes are stabilizer codes whose BSM splits cleanly into an X-block and a Z-block, each derived from a
classical linear code. We follow the standard recipe: given classical linear codes C1 , C2 ⊆ Zn2 with C1⊥ ⊆ C2 ,
we build the BSM from their parity-check matrices. Recall that the dual code C ⊥ is the orthogonal subspace
under the dot product, a generator matrix has linearly independent rows that span C, and a parity-check
matrix is a generator matrix for C ⊥ .
Definition 3.13. Given classical linear codes C1 , C2 ⊆ Zn2 , where C1⊥ ⊆ C2 , a CSS Code is defined starting




                                                       12
from the following binary symplectic matrix:

                                                 X         Z
                                                  0         H1
                                                  H2        0


   Where H1 , H2 are parity-check matrices for the two codes.
    Linear independence of the BSM rows is immediate: each block inherits independence from its parity-check
matrix and the two blocks have disjoint X/Z support. The mutual symplectic-product-zero condition splits
into three cases. Two rows from the same block produce a dot product of a nonzero half against a zero half,
which is zero. A row from the H1 block paired with a row from the H2 block produces a sum of two dot
products, one of which is 0 · · = 0 and the other of which is between an element of C1⊥ and an element of C2⊥ ;
by C1⊥ ⊆ C2 this is also zero.

Classical coding theory in Lean. Mathlib does not yet contain a classical coding theory library, so
we built one. The core type is a subspace of Fnq ; we go from a finite generating set to a matrix via
Mathlib’s Submodule.span rather than the other direction, because Submodule.span is the side Mathlib’s inner-
product/dual machinery is wired up against. The dual code is then defined through Mathlib’s bilinear-form
orthogonal-complement machinery rather than re-derived from scratch.

    abbrev CodeSpace (n : N) := Submodule (ZMod 2) (Fin n → ZMod 2)

    abbrev CodeSpace (n : N) := Submodule (ZMod 2) (Fin n → ZMod 2)

    def codeFromGenerators (G : Finset (Fin n → ZMod 2)) : CodeSpace n :=
    Submodule.span (ZMod 2) G

    def Matrix.toCodeSpace {α : Type*} [Fintype α] (M : Matrix α (Fin n) (ZMod 2)) : CodeSpace n
         :=
      Submodule.span (ZMod 2) (Finset.univ.image (fun i => M i))

    def CodeSpace.dualCode (C : CodeSpace n) : CodeSpace n := (C.orthogonalBilin (dotProductBilin
         _ _))

   Generator and parity-check matrices are then characterized by predicates: row-wise linear independence
plus row-span equal to the code (resp. its dual).

    def CodeSpace.generatorMatrixOf (C : CodeSpace n) (G : Matrix α (Fin n) (ZMod 2))
      : Prop := (LinearIndependent (ZMod 2) G.row) ∧ Submodule.span (ZMod 2) (Finset.image (fun r
         => G r) Finset.univ) = C

    def CodeSpace.parityCheckMatrixOf (C : CodeSpace n) (G : Matrix α (Fin n) (ZMod 2))
      : Prop := C.dualCode.generatorMatrixOf G

   Two theorems anchor the classical layer: duality is an involution, (C ⊥ )⊥ = C, and dimensions add up,
dim C + dim C ⊥ = n. The latter is what Lemma 4.1 uses to certify an externally supplied parity-check kernel.

    theorem dual_dual_eq {C : CodeSpace n} : (C.dualCode).dualCode = C

    lemma dual_finrank_eq {C : CodeSpace n} : Module.finrank (ZMod 2) C.dualCode = n - (Module.
        finrank (ZMod 2) C)

   A CSS code is then a stabilizer code whose BSM is assembled from two parity-check matrices satisfying
the dual-containment condition.

    def CSS_BSM (H1 : Matrix (Fin k1 ) (Fin n) (ZMod 2))


                                                       13
        (H2 : Matrix (Fin k2 ) (Fin n) (ZMod 2)) : BinSympMatrix (k1 + k2 ) n where
          X := Fin.append (fun (_ : Fin k1 ) => (fun _ => 0)) H2
          Z := Fin.append H1 (fun (_ : Fin k2 ) => (fun _ => 0))

      theorem CSS_BSM_is_comm {C1 C2 : CodeSpace n} (H_dual : (C1 .dualCode : Set (Fin n → ZMod 2))
           ⊆ C2 ) {H1 : Matrix (Fin k1 ) (Fin n) (ZMod 2)}
        {H2 : Matrix (Fin k2 ) (Fin n) (ZMod 2)} (hpc1 : C1 .parity_checked_by H1 )
        (hpc2 : C2 .parity_checked_by H2 ) : (CSS_BSM H1 H2 ).isCommuting

    We take parity_checked_by (a row-span condition) rather than the strict parityCheckMatrixOf predicate
(row-span plus row-independence) for the parity-check arguments. The relaxation matters in practice: many
code constructions in the literature, including the [[90, 8, 10]] BB code we verify in Section 5, specify dependent
generator sets that fail strict independence. The independence can always be re-proved separately, but baking
the relaxation in keeps the CSS-code constructor modular.

Bivariate Bicycle codes. The CSS family we ultimately scale to is the Bivariate Bicycle (BB) family
— low-density parity-check codes with high rate and good distance, currently the leading candidate for
fault-tolerant computation on superconducting hardware. Let Sn be the n × n cyclic shift permutation matrix
and define
                                      x = Sℓ ⊗ Im ,    y = Iℓ ⊗ Sm .
A BB code is built from two trivariate polynomials in x and y:
Definition 3.14. A Bivariate Bicycle code is the CSS code with parity-check matrices HX = [A | B] and
HZ = [B T | AT ], where A = A1 + A2 + A3 and B = B1 + B2 + B3 , each Ai , Bi a monomial in x and y.
    Our case studies in Section 5 verify the [[90, 8, 10]] instance inside Lean and show that the same encoding
scales to [[144, 12, 12]] outside the kernel.


4      Solver-Assisted Distance Verification
This section presents the verified distance pipeline at the heart of Lean-QEC. The goal is to discharge a
statement of the form “the code defined by these parity-check matrices has distance at least d” inside Lean,
even when d and the code size place the underlying combinatorial check out of reach of any pen-and-paper or
direct ITP argument.

Why SAT, not ILP. The textbook formulation of distance is an integer program: minimize the Pauli
weight of an error subject to commutation with all stabilizers and exclusion from the row space. An ILP
front-end would be the most direct match. Unfortunately Lean has no verified ILP backend at present, so
we instead reduce to Boolean satisfiability, prove the reduction sound in Lean, and use the existing SAT
integration.

Trusted base. Lean’s bv_decide tactic [6] bitblasts a goal phrased in BitVec and Bool into CNF, sends the
formula to CaDiCaL, receives an LRAT [9] certificate, and reconstructs the certificate inside Lean’s kernel.
The solver itself does not enter the trusted base; only the LRAT checker and Lean’s kernel do. The LRAT
certificate is cached on disk, so future builds skip the SAT call and re-check the proof directly.

4.1     Reduction to Boolean Satisfiability
The stabilizer-code distance is
                           d = min wt(E) s.t. ∀S ∈ Stab, SE = ES and E ∈
                                                                       / Stab.
                               E∈Pn

The end-to-end correspondence theorems of Section 3.6 let us discharge this query at the BSR level: writing
R(B) for the rows of the binary symplectic matrix,
                  d = min2n wt(Ex ∪ Ez ) s.t. ∀S ∈ R(B), E ⊙ S = 0 and E ∈
                                                                         / rowspace(B).
                      E∈Z2



                                                        14
Everything in this query is a Boolean predicate except for “E ∈
                                                              / rowspace(B).” We replace it with the dual
formulation: row space equals the orthogonal complement of the kernel, so E ∈ / rowspace(B) holds exactly
when E · g = 1 for some generator g of ker B. With a finite generating set G for the kernel, the constraint
becomes a finite OR of F2 -dot-product equations.

CSS specialization. For CSS codes the search splits exponentially. It suffices to consider purely-X errors
(against Z-stabilizers) and purely-Z errors (against X-stabilizers); the code distance is then the minimum of
the two,
                                              d = min(dX , dZ ),
where dX is the minimum weight of an X-only error that commutes with all Z-stabilizers and is not generated
by the X-stabilizers, and symmetrically for dZ . Each side reduces to a SAT instance over F2 variables with a
Hamming-weight bound, exactly the shape bv_decide accepts.

   Worked example: Shor 9-qubit code. We trace the reduction on a small CSS code with
   parity-check matrices
                                                       
                                1 1 0 0 0 0 0 0 0
                              0 1 1 0 0 0 0 0 0
                                                       
                              0 0 0 1 1 0 0 0 0
                         HZ = 
                              0 0 0 0 1 1 0 0 0
                                                        
                                                       
                              0 0 0 0 0 0 1 1 0
                                0 0 0 0 0 0 0 1 1
                                                       
                                 1 1 1 1 1 1 0 0 0
                         HX =
                                 0 0 0 1 1 1 1 1 1
   The claim “distance at least 3” splits, by the CSS specialization, into two SAT queries: no weight-≤ 2
   error in the X-only sector and no weight-≤ 2 error in the Z-only sector. Each query uses a kernel
   basis for the opposite parity-check matrix (these are also generators of the underlying classical codes
   C1 and C2 ):
                                                                         
                                            1 1 0 0 0 0 0 0 0
                                           1 0 1 0 0 0 0 0 0
                                                                         
                                           0 0 0 1 1 0 0 0 0
                                                                         
                                   GX =   0 0 0 1 0 1 0 0 0
                                                                          
                                           1 0 0 1 0 0 1 0 0
                                                                         
                                           1 0 0 1 0 0 0 1 0
                                            1 0 0 1 0 0 0 0 1
                                                                         
                                            1 1 1 0 0 0 0 0 0
                                   GZ = 0 0 0 1 1 1 0 0 0
                                            0 0 0 0 0 0 1 1 1
   The X-sector query (commutation with the six Z-stabilizer rows of HZ , non-membership in the row
   space of HX , weight bound) instantiates to:

          E1 ⊕ E 2 = 0 ∧ E 2 ⊕ E 3 = 3 ∧ E 4 ⊕ E 5 = 0 ∧ E 5 ⊕ E 6 = 0 ∧ E 7 ⊕ E 8 = 0 ∧ E 8 ⊕ E 9 = 0
                                                       ∧
   E1 ⊕ E2 = 1 ∨ E2 ⊕ E3 = 3 ∨ E4 ⊕ E5 = 1 ∨ E4 ⊕ E6 = 1 ∨ E1 ⊕ E7 = 1 ∨ E1 ⊕ E8 = 1 ∨ E1 ⊕ E9 = 1


                                                    |E| < 3




                                                      15
4.2    Practical Verification for Larger Codes
The Shor example fits comfortably inside Lean with the straightforward encoding. Industrial-scale codes do
not. The solver-based pipeline has three stages:
1. Formula construction: translate the parity-check matrices and the distance bound into a propositional
   formula.
2. Solver dispatch: hand the formula to CaDiCaL and obtain either a satisfying assignment or an LRAT
   UNSAT certificate.
3. Proof reconstruction: re-check the certificate in Lean’s kernel.
Each stage breaks first for a different code size, and each demands its own optimization. We describe the
bottlenecks in the order they appear as code size grows.

Stage 1: Matrix-to-BitVec flattening. The naive encoding builds the formula directly out of Mathlib’s
Matrix (Fin k) (Fin n) (ZMod 2) type. Matrix is internally a function Fin k × Fin n → Z2 , so constructing
the formula requires materializing every entry as a separate Lean expression. The memory footprint blows up
before the [[90, 8, 10]] BB code instance even reaches the solver.
   We introduce a BitVec-flattened intermediate representation: a matrix of type Matrix (Fin k) (Fin n) (
ZMod 2) is encoded as a single BitVec (k * n), with vectors handled analogously. BitVec is the type Lean’s
program-verification stack is optimized for and the type bv_decide accepts natively; flattening once and
operating on the BitVec carries us comfortably past 90 qubits. The pipeline includes a proven equivalence
between the BitVec and Matrix representations, so the original quantum-theoretic distance statement still
applies.

Stage 2: location-based error encoding. With the encoding fixed, the next wall is the solver itself. A
one-variable-per-qubit error encoding produces formulas with as many independent variables as qubits, and
the SAT solver scales exponentially in this count. Empirically the 90-qubit BB instance is already at the
edge of practicality, and 144 qubits is intractable outside Lean under this encoding.
    We exploit the weight bound implicit in distance verification: an error witnessing distance < d has
Hamming weight at most d − 1, so it is uniquely described by a list of at most d − 1 locations rather than by
an n-bit vector. We replace the per-bit variables with (d − 1) location variables of width ⌈log2 n⌉, reducing
the independent-variable count from n to k⌈log2 n⌉ where k ≤ d − 1.
    The effect is concrete. For the [[144, 12, 12]] BB code, d = 12 means k ≤ 11 and ⌈log2 144⌉ = 8, so the
location encoding uses 88 variables versus 144 — a 56-variable reduction. The change does not literally
divide the search space by 256 (the constraints couple the variables non-trivially), but in practice it brings
the 144-qubit instance into the range CaDiCaL discharges in minutes outside Lean.
    A further search space reduction is performed through symmetry breaking. In addition to the location
constraints, we introduce a constraint enforcing that each location variable be less than or equal to the
succeeding variable. In the naive setting, this reduces the search space factorially with respect to the code
distance.

Stage 3: proof reconstruction. With Stages 1 and 2 in place, certificate reconstruction inside Lean’s
kernel has gone through smoothly through the [[90, 8, 10]] BB code. Beyond that size we expect Lean’s LRAT
replay to become the next bottleneck. Lean provides an option to trust the SAT solver’s output without
re-checking it; doing so would extend our scaling envelope at the cost of admitting CaDiCaL into the trusted
base, a trade-off we view as clean enough to be worth taking when the verification target is a code too large
for kernel replay.

4.3    Kernel Checking
The SAT translation requires a generating set for the kernel of each parity-check matrix. Outside Lean this is
a one-line linear-algebra call; inside Lean we need either a verified implementation of Gaussian elimination or
a way to certify that an externally-supplied basis really generates the kernel. We take the second route: we


                                                      16
accept the kernel as an opaque input and discharge a Lean-side correctness check by the following corollary
of rank-nullity, which avoids any need to formalize row-reduction.
Lemma 4.1. Let M1 , M2 be binary matrices with dimensions k1 ∗ n and k2 ∗ n respectively. Let r1 + r2 = n.
If every row of M1 is orthogonal to every row of M2 , and r1 ≤ rank M1 and r2 ≤ rank M2 , then the rowspace
of M2 is the kernel of M1 .
   The kernel-correctness obligation splits into two sub-obligations, each handled by its own technique below:
a rank lower bound on the parity-check matrix and on the supposed kernel (Section 4.3.1), and mutual
row-orthogonality between them (Section 4.3.2).

4.3.1    Rank and Independence Checking
Lemma 4.1 asks for a rank lower bound, not full row-independence. The relaxation matters in practice
because many codes specify dependent generator sets: the Toric code’s full stabilizer set is dependent, and
each parity-check matrix of the [[90, 8, 10]] BB code carries 4 dependent rows. A formalization that required
full independence would have to reject these specifications or silently drop rows — both unappealing.
    To certify rank(M ) ≥ r, it suffices to exhibit a row submatrix with r linearly independent rows. We
discharge the linear independence of that submatrix by another SAT query: the submatrix has full rank iff no
nontrivial F2 -coefficient vector annihilates its rows, which is a finite Boolean statement. The independence
query consistently runs much faster than the distance query for the same code — circumstantial evidence
that CaDiCaL is performing something like an internal Gaussian elimination over the smaller variable set.

4.3.2    Orthogonality
CSS codes additionally require the dual-containment condition C1⊥ ⊆ C2 , which on the parity-check matrices
is mutual row-orthogonality. The same condition couples the parity-check matrix to its supplied kernel basis
under Lemma 4.1. Both checks reduce to a polynomial number of F2 -dot-product evaluations between rows.
    We define bitvec_mutually_orth on a pair of BitVecs, verified consistent with the matrix-level statement,
and discharge concrete instances by evaluating the predicate down to a Boolean. Because every building block
is decidable — no use of the choice operator anywhere on the path — the goal reduces by unfolding. We use
Lean’s native_decide tactic rather than simp for this final reduction: it compiles the decision procedure to
native code and runs orders of magnitude faster than the kernel simplifier. The trade-off is that native_decide
extends the trusted base with Lean’s compiler; we accept this for orthogonality checks but not, e.g., for the
distance reduction itself.


5       Case Studies
This section instantiates the pipeline of Section 4 on three CSS codes of increasing size: the [[7, 1, 3]] Steane
code, the [[23, 1, 7]] Golay code, and the [[90, 8, 10]] Bivariate Bicycle code. Each case study follows the
same template — input matrices, kernel certification, distance SAT query — so the development is reusable:
instantiating the framework on a new CSS code amounts to supplying the parity-check matrices, their kernel
bases (computed offline), and the chosen distance bound, and renaming. We close the section by reporting
the resource envelope outside Lean for the [[144, 12, 12]] BB code.

5.1     The Steane Code
The [[7, 1, 3]] Steane code is the simplest non-trivial case study. It is a CSS code with HX = HZ , both equal
to the parity-check matrix of the [7, 4, 3] binary Hamming code; consequently dX = dZ and the distance
argument is carried out once.
                                                                           
                                                    1 0 0 1 0 1 1
                                      Hx = Hz = 0 1 0 1 1 0 1
                                                    0 0 1 0 1 1 1
    The matrix is entered directly as a Mathlib Matrix for human readability:


                                                       17
    def steane_mat’ : Matrix (Fin 3) (Fin 7) (ZMod 2) :=
      !![1, 0, 0, 1, 0, 1, 1;
        0, 1, 0, 1, 1, 0, 1;
        0, 0, 1, 0, 1, 1, 1]

   All subsequent operations happen on the BitVec-flattened form (Section 4.1). An external Python script
computes the hexadecimal flattening (0x1d2d69 for the Steane matrix) and we discharge the equivalence to
the Matrix form by Lean evaluation of the verified flatten_matrix function.

    def steane_mat : BitVec (3 * 7) :=
      0x1d2d69
    lemma steane_mat_correct : steane_mat = flatten_matrix steane_mat’ := by decide

   The kernel basis is computed by the same script and entered alongside its hexadecimal flattening.

    def steane_ker’ : Matrix (Fin 4) (Fin 7) (ZMod 2) :=
     !![1, 1, 0, 1, 0, 0, 0;
     0, 1, 1, 0, 1, 0, 0;
     1, 0, 1, 0, 0, 1, 0;
     1, 1, 1, 0, 0, 0, 1;]
    def steane_ker : BitVec (4 * 7) :=
      0x8e94b0b
    lemma steane_ker_correct : steane_ker = flatten_matrix steane_ker’ := by decide

    Lemma 4.1 demands a rank lower bound on both the parity-check matrix and the supplied kernel. For
the Steane code both matrices have full row rank, so the witness submatrix is the matrix itself and the rank
bound reduces to row-independence. We discharge independence via the SAT route of Section 4.3.1: rewrite
to the BitVec form, normalize to the shape bv_decide accepts, and let CaDiCaL verify that no nontrivial
F2 -combination of rows is zero.

    lemma steane_ind : LinearIndependent (ZMod 2) steane_mat’ := by
      rw [linear_indep_SAT_correct, ←steane_mat_correct, steane_mat]
      simp only [... long lemma list ...]
      bv_decide
    lemma steane_ker_ind : LinearIndependent (ZMod 2) steane_ker’ := by
      rw [linear_indep_SAT_correct, ←steane_ker_correct, steane_ker]
      simp only [... long lemma list ...]
      bv_decide

   Linear independence then yields the rank bound used in Lemma 4.1.

    lemma steane_mat_rank : 3 ≤ steane_mat’.rank := by
      apply Matrix.rank_le_of_submatrix_independent _ id (strictMono_id)
      rw [Matrix.submatrix_id_id]
      apply steane_ind

    lemma steane_ker_rank : 4 ≤ steane_ker’.rank := by
      apply Matrix.rank_le_of_submatrix_independent _ id (strictMono_id)
      rw [Matrix.submatrix_id_id]
      apply steane_ker_ind

   The two orthogonality conditions from Section 4.3.2 are the CSS dual-containment (HX ’s rows mutually
orthogonal — here against themselves) and the parity-check-vs-kernel orthogonality from Lemma 4.1. Both
expand to fully-concrete F2 dot products with no free variables, so SAT is unnecessary; simp on the BitVec
unfoldings suffices.

    lemma steane_orth : steane_mat’.mutually_orth_rows steane_mat’ := by
      rw [←mutually_orth_correct, ←steane_mat_correct, steane_mat]


                                                    18
       simp [bitvec_mutually_orth, mutually_orth_sat_aux,
       BitVec.row, BitVec.dot_product, dot_product_aux]

      lemma steane_mat_ker_orth : steane_mat’.mutually_orth_rows steane_ker’ := by
        rw [←mutually_orth_correct, ←steane_mat_correct, ←steane_ker_correct, steane_mat,
          steane_ker]
        simp [bitvec_mutually_orth, mutually_orth_sat_aux,
        BitVec.row, BitVec.dot_product, dot_product_aux]

    The core distance lemma is the SAT query proper: every error vector under the weight bound either
fails commutation with the kernel basis (i.e. lies in the row space) or is the zero error. We rewrite into the
location-indexed BitVec form and dispatch bv_decide.

      set_option maxHeartbeats 0 in
      lemma steane_dist : lt_dist_sat (flatten_matrix steane_mat’) (flatten_matrix steane_ker’) 2 3
        := by
        rw [←steane_mat_correct, ←steane_ker_correct, steane_mat, steane_ker]
        simp only [... long lemma list ...]
        bv_decide (timeout := 999)

    With rank bounds and orthogonality in place, Lemma 4.1 certifies that the externally-supplied basis is in
fact a basis of ker H.

      lemma steane_ker_mat_correct : steane_ker’.is_ker_for steane_mat’ := by
        apply Matrix.is_ker_for_of_rank_sum_mutually_orth _ _ steane_mat_rank steane_ker_rank (by
          norm_num) steane_mat_ker_orth

   The final step assembles the CSS code from its stabilizer generators and applies the verified SAT-translation
soundness theorem to lift the BSM-level UNSAT result to a quantum-theoretic distance bound on steane_css.

      theorem steane_dist_3 : 3 ≤ steane_css.toBSM.distance (by norm_num) := by
        apply bitvec_sat_translation_correct steane_css steane_ker’ steane_ker_mat_correct
          steane_ker’ steane_ker_mat_correct (by norm_num) _ _
        all_goals rw [steane_css, CSS_pair.of_matrices]
        all_goals exact steane_dist



5.2     Beyond Steane
Golay [[23, 1, 7]]. The [[23, 1, 7]] Golay code is another weakly self-dual CSS code (HX = HZ ), so its Lean
development is, mechanically, a rename of the Steane case study: regenerate the kernel and hexadecimal
flattening with the Python script, swap every “Steane” identifier for “Golay,” and the proofs go through
unchanged. The script and the Lean file together are under 110 lines.

Bivariate Bicycle [[90, 8, 10]]. The [[90, 8, 10]] BB code is the first case study with two genuinely different
parity-check matrices (HX ̸= HZ ). Two distance queries are needed, one for dX and one for dZ . The
parity-check matrices also have 4 dependent rows each, so the rank-bound step from Section 4.3.1 cannot
collapse to row-independence as in the Steane case; instead, the Python preprocessor selects an independent
row subset to feed into the SAT-based independence checker. Every preprocessor output is re-checked inside
Lean, so although the preprocessing happens outside the kernel, the resulting distance certificate remains
end-to-end. The main proof file is just under 200 lines. We autogenerate similar proofs for BB codes of size
18, 30, 36, 54, 60, 72, and 108 with the same format using a Python script.

[[144, 12, 12]] outside Lean. The 144-qubit BB instance pushes Lean’s certificate-replay budget beyond
what we can verify in the kernel. Under the location-indexed encoding with symmetry breaking of Section 4.1,
however, an external call to the SMT solver cvc5 dispatches this goal in minutes. We report this number to



                                                      19
show that the SAT encoding itself scales, and we view kernel-side replay at this size as the next concrete
engineering target (cf. Section 6.3).

Template summary. The three Lean case studies share a common skeleton: matrix entry, BitVec-flattening
equivalence, kernel basis entry, rank/independence via SAT, mutual orthogonality, distance SAT query, and
the final lift through bitvec_sat_translation_correct. Adding a new CSS code requires only its parity-check
matrices and a Python preprocessor invocation. We provide a python script that generates a Lean file
verifying the distance of a CSS code given only a NumPy description of the code stabilizers, demonstrating
the flexibility of this template.


6     Discussion and Conclusion
We presented Lean-QEC, a Lean 4 framework that combines interactive theorem proving with SAT-based
computation to deliver end-to-end, machine-checked distance certificates for practical CSS and Bivariate
Bicycle codes. The library contributes a reusable stabilizer-code stack, a verified reduction from code distance
to Boolean satisfiability, two scalability techniques (BitVec flattening and location-indexed error encoding),
and case studies covering the Steane, Golay, and a family of Bivariate Bicycle codes up to [[90, 8, 10]] inside
the kernel and the [[144, 12, 12]] instance outside it.
   The result narrows the gap that has separated the testing-only and solver-only options for QEC verification.
Every step from the quantum-theoretic definition of distance, through the binary symplectic representation,
through the BitVec encoding, to the final SAT certificate is connected by a Lean-checked theorem. Either the
kernel accepts the artifact or it does not; no informal mathematical glue sits in between.

6.1    Methodological Takeaways
The build process surfaced two design lessons that we expect to transfer to future quantum formalizations.

Representation bridges are first-class objects. The binary symplectic representation is the obvious
algebraic bridge between the quantum-theoretic stabilizer code and the matrix-level SAT query. The non-
obvious step is that this bridge must itself be a formalized object, not an informal correspondence, if the
resulting certificate is to be end-to-end. We further bridged the BSR to a BitVec representation tuned for
the solver. Each bridge is one Lean theorem and, once written, is invisible at the call site; without it, every
downstream lemma would carry an unverified soundness gap.

Verified linear algebra is the missing piece. The pipeline still admits one externally computed input:
a kernel basis for each parity-check matrix. We discharge its correctness via a rank/orthogonality argument,
but the kernel itself is supplied as a definition rather than computed. A verified Gaussian-elimination
implementation in Lean would let the framework take parity-check matrices alone as input. More broadly,
the absence of efficient verified algebraic computation is the consistent friction point in this development;
closing it would benefit many Lean formalizations beyond QEC.

6.2    Related Work
Quantum verification in proof assistants. The SQIR development [14] and CoqQ [32] formalize quantum
circuits and circuit optimizations in Rocq, and Peng et al. [23] verify end-to-end correctness of algorithms
such as Shor’s. QHLProver [19] formalizes quantum Hoare logic. On the Lean side, Lean-QuantumInfo [22]
formalizes finite-dimensional quantum-information primitives but does not specialize to qubit systems or QEC;
we build on the same Mathlib foundations but specialize to the qubit space and develop the stabilizer-code
stack.




                                                      20
Verification of QEC. The 9-qubit Shor-code verification of [11] closes the trust loop on a single small code
but enumerates Pauli errors explicitly and does not scale beyond it. Other verified-QEC efforts [15, 31] sit
outside ITPs and target program-level properties rather than code-distance certification. To our knowledge,
Lean-QEC is the first development that combines a kernel-checked stabilizer stack with a solver-backed
distance pipeline that scales to industrial code sizes.

Solver-assisted ITP. The strategy of reducing a hard subgoal to SAT, dispatching it to an external solver,
and reconstructing the certificate inside the kernel is well established in classical verification. Our contribution
to this idiom is the verified reduction from a quantum-theoretic distance statement to a SAT formula, the
BitVec-flattened encoding that makes the formula tractable to instantiate, and the location-indexed variable
scheme that makes the formula tractable to solve.
    Concurrent work by Jain [16] also explores formalization of quantum error-correcting codes in Lean but
focuses on the toric code family.

6.3    Limitations and Future Work
Solver scaling. The SAT pipeline scales by orders of magnitude over hand-written ITP distance proofs —
our 144-qubit instance handles roughly 240 candidate errors — but it is not unbounded. Codes substantially
larger than the BB family (BB360 and beyond) push the SAT query itself out of reach. Decomposition
strategies and specialized solvers for linear codes are natural directions for extending the envelope.

Broader code families. The development targets CSS codes, with BB as the headline family. Extending
to general non-CSS stabilizer codes is mostly a matter of dropping the X/Z split and reusing the full BSR
pipeline; subsystem codes and codes from the broader stabilizer formalism require more substantial additions.
Note that surface and color codes are themselves CSS and should fit the existing framework directly.

Verified kernel computation. The kernel basis for each parity-check matrix is currently produced by an
external Python script and certified inside Lean. A verified row-reduction routine would close this remaining
preprocessor step. Doing so cleanly is the most concrete piece of follow-on engineering implied by this work.

Integration with quantum-circuit verification. The QEC layer is one component of the verified
quantum-computation stack. Connecting it to verified circuit compilers such as SQIR would yield an
integrated, end-to-end pipeline from algorithm specification to fault-tolerant physical implementation.


7     Acknowledgements and Code Availability
We thank Junyi Liu for many useful discussions. We thank our AI assistant Aristotle [3] for its contributions
to the repository. YL and XW are partially supported by the U.S. National Science Foundation grant
CCF-1942837 (CAREER), CCF-2330974, and a Sloan Research Fellowship.
    The library may be found at https://github.com/VerifiedQC/Lean-QEC. The verified BB codes are
located within the library at LeanQEC/Stabilizer/Examples/BB.


References
 [1] Suppressing quantum errors by scaling a surface code logical qubit. Nature, 614(7949):676–681, 2023.

 [2] Quantum error correction below the surface code threshold. Nature, 638(8052):920–926, 2025.
 [3] Tudor Achim, Alex Best, Alberto Bietti, Kevin Der, Mathïs Fédérico, Sergei Gukov, Daniel Halpern-
     Leistner, Kirsten Henningsgard, Yury Kudryashov, Alexander Meiburg, et al. Aristotle: Imo-level
     automated theorem proving. arXiv preprint arXiv:2510.01346, 2025.
 [4] Jeremy Avigad and Patrick Massot. Mathematics in lean, 2020.


                                                        21
 [5] Dominic W Berry, Graeme Ahokas, Richard Cleve, and Barry C Sanders. Efficient quantum algorithms
     for simulating sparse hamiltonians. Communications in Mathematical Physics, 270(2):359–371, 2007.
 [6] Armin Biere, Tobias Faller, Katalin Fazekas, Mathias Fleury, Nils Froleyks, and Florian Pollitt. Cadical
     2.0. In International Conference on Computer Aided Verification, pages 133–152. Springer, 2024.

 [7] Sergey Bravyi, Andrew W. Cross, Jay M. Gambetta, Dmitri Maslov, Patrick Rall, and Theodore J.
     Yoder. High-threshold and low-overhead fault-tolerant quantum memory. Nature, 627:778–782, 2024.
 [8] Kevin Buzzard and Richard Taylor. FLT, 2025.
 [9] Luís Cruz-Filipe, Marijn JH Heule, Warren A Hunt Jr, Matt Kaufmann, and Peter Schneider-Kamp.
     Efficient certified rat verification. In International Conference on Automated Deduction, pages 220–236.
     Springer, 2017.
[10] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language. In
     CADE-28, volume 12699 of LNCS, pages 625–635. Springer, 2021.
[11] Qiuyi Feng. Formal verification of quantum stabiliser codes by stabiliser formalism.

[12] Daniel Gottesman. Surviving as a quantum computer in a classical world. 2024.
[13] Aram W Harrow, Avinatan Hassidim, and Seth Lloyd. Quantum algorithm for linear systems of equations.
     Physical review letters, 103(15):150502, 2009.
[14] Kesha Hietala, Robert Rand, Shih-Han Hung, Xiaodi Wu, and Michael Hicks. A verified optimizer for
     quantum circuits. Proceedings of the ACM on Programming Languages, 5(POPL):1–29, 2021.
[15] Qifan Huang, Li Zhou, Wang Fang, Mengyu Zhao, and Mingsheng Ying. Efficient formal verification of
     quantum error correcting programs. Proceedings of the ACM on Programming Languages, 9(PLDI):1068–
     1093, 2025.
[16] Stavan Jain. QEClean. https://github.com/Stavan-Jain/QECLean, 2026.

[17] Upendra Kapshikar and Srijita Kundu. On the hardness of the minimum distance problem of quantum
     codes. IEEE Transactions on Information Theory, 69(10):6293–6302, October 2023.
[18] Alex Kontorovich and Terence Tao. Prime Number Theorem and More, January 2024.
[19] Junyi Liu, Bohua Zhan, Shuling Zhu, Shenggang Ying, and Mingsheng Ying. Formal verification of
     quantum algorithms using quantum Hoare logic. In CAV 2019, volume 11562 of LNCS, pages 187–207.
     Springer, 2019.
[20] Sam McArdle, Suguru Endo, Alán Aspuru-Guzik, Simon C Benjamin, and Xiao Yuan. Quantum
     computational chemistry. Reviews of Modern Physics, 92(1):015003, 2020.
[21] Alex Meiburg. Quantum information in lean. https://github.com/Timeroot/Lean-QuantumInfo,
     2024.
[22] Alex Meiburg, Leonardo A Lessa, and Rodolfo R Soldati. A formalization of the generalized quantum
     stein’s lemma in lean. arXiv preprint arXiv:2510.08672, 2025.
[23] Yuxiang Peng, Kesha Hietala, Runzhou Tao, Liyi Li, Robert Rand, Michael Hicks, and Xiaodi Wu.
     A formally certified end-to-end implementation of shor’s factorization algorithm. Proceedings of the
     National Academy of Sciences, 120(21):e2218775120, 2023.
[24] Lukas Postler, Friederike Butt, Ivan Pogorelov, Christian D Marciniak, Sascha Heußen, Rainer Blatt,
     Philipp Schindler, Manuel Rispler, Markus Müller, and Thomas Monz. Demonstration of fault-tolerant
     steane quantum error correction. PRX Quantum, 5(3):030326, 2024.

[25] John Preskill. Quantum computing in the nisq era and beyond. Quantum, 2:79, August 2018.


                                                     22
[26] Peter W Shor. Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum
     computer. SIAM review, 41(2):303–332, 1999.
[27] The mathlib Community. The Lean Mathematical Library. In Proceedings of the 9th ACM SIGPLAN
     International Conference on Certified Programs and Proofs, CPP 2020, New Orleans, LA, USA, January
     2020. ACM.

[28] Felix Tripier, Woo Chang Chung, Jacob Young, Safwan Alam, Bryce Bjork, Aharon Brodutch, Finn Lasse
     Buessen, Nolan J. Coble, Thomas Dellaert, Dmitri Maslov, Martin Roetteler, Edwin Tham, Mark Webster,
     Min Ye, John Gamble, Andrii Maksymov, J. P. Marceaux, and Nicolas Delfosse. Fault-tolerant quantum
     computing with trapped ions: The walking cat architecture, 2026.
[29] Alexander Vardy. The intractability of computing the minimum distance of a code. IEEE Transactions
     on Information Theory, 43(6):1757–1766, 2002.
[30] Mark Webster, Abraham Jacob, and Oscar Higgott. Distance-finding algorithms for quantum codes and
     circuits, 2026.
[31] Anbang Wu, Gushu Li, Hezi Zhang, Gian Giacomo Guerreschi, Yuan Xie, and Yufei Ding. Qecv:
     Quantum error correction verification. arXiv preprint arXiv:2111.13728, 2021.
[32] Li Zhou, Gilles Barthe, Pierre-Yves Strub, Junyi Liu, and Mingsheng Ying. Coqq: Foundational
     verification of quantum programs. Proceedings of the ACM on Programming Languages, 7(POPL):833–
     865, 2023.




                                                   23
