                                                          A Machine-Verified Proof of a Quantum-Optimization Conjecture

                                                                                                      Uri Kol
                                                                               Center of Mathematical Sciences and Applications,
                                                                           Harvard University, Cambridge, Massachusetts 02138, USA

                                                                                                Maor Ben-Shahar
                                                            MIT Center for Theoretical Physics - a Leinweber Institute, Cambridge, MA 02139, USA

                                                                                       Kfir Sulimany∗ and Dirk Englund
                                                 Research Laboratory of Electronics, Massachusetts Institute of Technology, Cambridge, Massachusetts 02139, USA
                                                                                             (Dated: June 30, 2026)
                                                          We report a machine-verified resolution of a problem open for over a decade in quantum
                                                        optimization: the Farhi, Goldstone and Gutmann (FGG) conjecture [1] that depth-p Quantum
arXiv:2606.29687v1 [quant-ph] 29 Jun 2026




                                                        Approximate Optimization Algorithm (QAOA) on the ring of disagrees attains approximation ratio
                                                        (2p + 1)/(2p + 2) exactly. We found the proof using a large language model, Claude Fable 5,
                                                        and verified its correctness end-to-end by the Lean 4 proof assistant. Our methodology includes
                                                        several ingredients: building on a substantial Lean library of quantum information, we formalized
                                                        the QAOA components and the known parts of the problem, and reduced the conjecture to a single
                                                        open mathematical statement. The model was then handed the library and our agentic toolkit, and
                                                        tasked with closing that gap by constructing a proof in Lean. The resulting process is a feedback loop
                                                        between the model’s natural-language reasoning and Lean’s mechanical verification, which converged
                                                        to a machine-verified proof. Human verification is required only for the structural scaffolding - that
                                                        the formal statement faithfully encodes the intended claim - while the proof itself is supplied by the
                                                        model and certified mechanically by Lean. The proof is nevertheless striking - the model uncovered
                                                        a hidden dynamical symmetry of the problem and exploited it, borrowing tools and machinery from
                                                        an adjacent field to turn a hard existence problem into an explicit construction. This work paves
                                                        the way for resolving open conjectures in quantum information science and beyond.


                                                              INTRODUCTION                                   statement expresses the intended claim. The semantic
                                                                                                             gap, however, is confined to the comparatively compact
                                               Large language models are beginning to contribute             statement of the theorem and its definitions, which is
                                            directly to scientific reasoning: they can propose               the only place where human verification is required. The
                                            calculations, identify patterns, generate code, and search       proof connecting hypotheses to conclusion is delegated in
                                            for proofs. Their speed makes it possible to explore             full to the machine.
                                            arguments that would be costly to examine one by one.               This generate-then-certify paradigm has recently
                                            For mathematically precise problems the generation of            produced a wave of machine-generated results
                                            an argument can be separated from its certification.             across mathematics:          olympiad geometry [4],
                                            A model may propose a proof, while an independent                silver-medal olympiad problem solving in Lean [5],
                                            program checks whether every step follows from explicitly        and algorithmic discovery [6]. These build on advances
                                            stated assumptions.                                              in autoformalization [7] and language-model theorem
                                               Such verification is essential because large language         proving [8–10], including agentic Lean provers that
                                            models can hallucinate: they may invent facts or                 extend to the physical sciences [11].
                                            lemmas, overlook exceptional cases, or introduce subtly             We apply this paradigm to a long-standing open
                                            invalid inferences while producing fluent and persuasive         problem in quantum optimization, which dates to
                                            explanations. The danger is especially acute in long             the original analysis of the Quantum Approximate
                                            mathematical arguments, where one incorrect step can             Optimization Algorithm (QAOA) by Farhi, Goldstone,
                                            invalidate everything that follows and may be difficult to       and Gutmann (FGG). They identified a particularly
                                            identify by inspection. Readability, confidence, and even        clean benchmark known as the ring of disagrees
                                            agreement among several models are no substitutes for            [1].    In this problem, n binary spins are placed
                                            deterministic verification.                                      around a ring, and the objective is to maximize the
                                               Formal proof systems such as Lean 4 [2, 3] can be used        number of neighboring pairs that point in opposite
                                            as a tool for verification of AI proposed theorems. With         directions.    In optimization language, this is the
                                            such formal systems a proof that is accepted (namely,            MaxCut problem on a cycle; in physics language,
                                            compiles cleanly) establishes that its conclusion follows        it is a one-dimensional antiferromagnetic Ising model
                                            from its hypotheses and any of the axioms that are               with periodic boundary conditions. When n is even,
                                            assumed. What Lean does not establish is that the formal         the optimum is the alternating spin configuration, in
                                                                                                                                         2

which every neighboring pair disagrees. A depth-p                  literature uses a cost operator, related to the
QAOA circuit prepares a quantum state by alternating               Hamiltonian, whose spectrum is [Emin , Emax ], by
p evolutions generated by the Ising cost Hamiltonian               C = (Emax −HC )/2, so C is maximal at the ground state,
with p evolutions generated by a transverse-field mixing           where Cmax = 21 (Emax − Emin ). The approximation ratio
Hamiltonian. The approximation ratio rp is the cost                compares the achieved cost to this optimum,
expectation value in the QAOA state, normalized by the                               ⟨C⟩    Emax − ⟨HC ⟩
true optimum. The optimal approximation ratio rp∗ is                        rp =          =              =: 1 − εres
                                                                                                                 p ,                    (3)
                                                                                     Cmax   Emax − Emin
the largest expected fraction obtainable by varying the
2p evolution angles. FGG conjectured that, for even n in           so rp = 1 at the ground state, and the normalized residual
the regime 2p + 2 ≤ n,                                             energy εres
                                                                            p is the shortfall. The object of interest is the
                                                                   optimum over angles
                                2p + 1
                        rp∗ =          .                     (1)
                                2p + 2                                                      rp∗ = max rp (γ, β).                        (4)
                                                                                                  γ,β
Settling this conjecture would pin the exact expressive             The benchmark we focus on is the ring of disagrees,
power of depth-p QAOA on this model: what the                      MaxCut on the cycle graph, with cost and mixer
quantum circuit can achieve when its parameters are
                                                                                      n
chosen optimally, namely an optimal performance                                       X                                  X
                                                                             HC =           σjz σj+1
                                                                                                 z
                                                                                                        ,         B=            σjx .   (5)
guarantee. Such guarantees are the canonical figure of
                                                                                      j=1                                  j
merit for optimization algorithms, and in particular
for QAOA on MaxCut [12]. Beyond its theoretical                    Its spectrum is [−n, n], and C = (n − HC )/2
interest, QAOA and related combinatorial-optimization              counts disagreeing edges. We take n even, so the
protocols are now executed on programmable quantum                 antiferromagnetic ground state is unfrustrated and
hardware, including superconducting processors [13]                Cmax = n.
and neutral-atom Rydberg arrays [14–16];                  the
one-dimensional antiferromagnetic Ising ring studied
here is itself natively realized on such arrays [17, 18].                  Exact decomposition and the open gap
   In this work,           we combine human-guided
autoformalization, custom Lean infrastructure, and                   FGG predicted rp∗ on this benchmark from numerics
the large language model Claude Fable 5 to obtain a                and proved the case p = 1. Wang et al. [20] extended
machine-verified proof of the FGG conjecture (1). We               the proof to p = 2 by an exact fermionic analysis. Mbeng,
formalized the optimization problem, constructed the               Fazio, and Santoro [21] derived an exact decomposition
definitions and supporting library required by the prover,         formula of the residual energy for any p in terms of
and isolated the open gap as a single formal statement.            independent momentum modes, which we summarize
Claude Fable 5 generated the decisive argument, which              here since the open gap in the proof lies there.
Lean 4 accepts with the standard classical axioms used               The ring is effectively a free-fermion model [22].
in Mathlib [3]. The result is therefore an independently           A Jordan-Wigner transformation [23] maps it to
certified proof, not one resting on trust in either the            non-interacting spinless fermions, and translational
model-generated output or an informal derivation. The              invariance block-diagonalizes the dynamics into p
complete Lean development is publicly available [19],              decoupled momentum modes at
and for completeness we also present the proof itself                                        ℓπ
below.                                                                               kℓ =       ,           ℓ = 1, . . . , p.           (6)
                                                                                            p+1
                                                                   On each mode the Anderson pseudospin [24] reduces
     QAOA AND THE RING OF DISAGREES                                the (k, −k) fermion pair to a single spin- 21 with Pauli
                                                                   operators τk = (τkx , τky , τkz ). In this representation, the
          The algorithm and the benchmark                          mixer and cost operators act, mode by mode, as two
                                                                   competing Zeeman fields,
   The QAOA [1] is a hybrid quantum-classical ansatz                           (k)
                                                                             HC = −2 b̂k · τk ,               B (k) = 2 ẑ · τk ,
for combinatorial optimization. A classical cost function                                                                               (7)
is encoded in a Hamiltonian HC which, together with                                    b̂k = (− sin k, 0, cos k),
a mixing operator B, is used to construct the depth-p
                                                                   the mixer along ẑ and the cost along the cost axis b̂k .
QAOA state
                                                                   Since the modes are independent, the residual energy
  |γ, β⟩ = e−iβp B e−iγp HC · · · e−iβ1 B e−iγ1 HC |+⟩⊗n ,   (2)   splits into a sum over them [21],

with the 2p angles (γ, β) chosen to minimize ⟨HC ⟩. The                             1        1 X
                                                                            εres
                                                                             p =        +            εk ,  εk ≥ 0,     (8)
standard terminology in the combinatorial-optimization                            2p + 2 2p + 2
                                                                                                             k
                                                                                                                       3

and each per-mode residual is a single-qubit geometric         present formalization - together with parts of the agentic
quantity,                                                      autoformalization toolkit [30].
                                                                  In order for the model to be able to state the
           εk = 1 − b̂k · mk = 21 ∥mk − b̂k ∥2 ,         (9)   conjectured theorem, we extended this library with the
                                                               further terms and definitions it required. The inherited
where mk = ⟨τk ⟩ is the pseudospin’s magnetization. In         formalization already supplied the basic quantum
the QAOA state mk is its initial value ẑ, acted on by the     mechanical objects - bras, kets, density operators, tensor
p layers, an alternating product of SO(3) rotations about      products, and inner products - so our additions were
ẑ (mixer) and b̂k (cost),                                     the machinery specific to QAOA, such as the mixing
                    1
                                                               Hamiltonians and the depth-p state ansatz. We have
                                                               also formalized the known components of the problem
                   Y                            
            mk =           Rẑ (4βℓ ) Rb̂k (4γℓ ) ẑ.   (10)
                     ℓ=p
                                                               - the definition of the Ising chain, including its exact
                                                               decomposition into decoupled momentum modes and the
εk is therefore the misalignment between mk and its cost       supporting machinery (Jordan-Wigner transformation
axis b̂k , vanishing exactly when the layers steer the mode    and Anderson’s pseudospin) - using various tools,
onto that axis, mk = b̂k .                                     including our agentic toolkit for autoformalization [30].
    Each εk ≥ 0, so (8) gives εres
                               p ≥ 1/(2p + 2) [25], that is       The gap (11) was then given to Claude Fable 5,
  ∗                                                            with the same toolkit [30], and it was tasked with
rp ≤ (2p + 1)/(2p + 2). FGG conjectured that this bound
is saturated.                                                  closing the theorem by constructing a proof in Lean.
                                                               The LLM made natural language proof plans in the
Conjecture 1. (FGG [1]). For the ring of disagrees             process and attempted to formalize them, thus obtaining
with n even and 2p + 2 ≤ n, the optimal depth-p QAOA           compiler feedback on its proof attempts. This workflow
approximation ratio is exactly rp∗ = (2p + 1)/(2p + 2).        is described in Fig. 1: the loop takes a formalized
                                                               open statement as its input and carries it through to
  By (8) the bound is saturated exactly when there exist
                                                               a machine-checked proof. Many such statements can
angles that simultaneously drive every mode onto its cost
                                                               be posed; here it is the existence statement (11) of the
axis,
                                                               FGG conjecture. Although Lean compilation was the
                ∃ γ, β : ∀k, εk (γ, β) = 0,             (11)   final verification tool for the LLM, it also used python
                                                               for numerical checks before investing proof efforts in any
and this simultaneous-steering problem is the gap in the       conjectured construction, in order to make sure that its
literature. Each condition εk = 0 pins a unit Bloch            theorem statements were not obviously false.
vector to a target axis - that is two real constraints,           The conjecture is encoded by the Lean theorem
so the p modes give 2p equations in the 2p angles - a          residualEnergy isLeast [19], which states that
square system. Equal counts would force a solution if          1/(2p + 2) is the least attainable residual energy -
the equations were linear, but they are transcendental in      equivalently, that the optimal approximation ratio
the angles through the SO(3) rotations of (10), and a          equals (2p + 1)/(2p + 2):
square transcendental system may have no real solution,
                                                               theorem residualEnergy_isLeast {N P : N}
one, or many. Mbeng, Fazio, and Santoro confirmed
                                                                   (hN_even : 2 | N) (hP : 2 * P + 2 ≤ N) :
saturation numerically to p = 128 and gave an explicit
                                                                   IsLeast {e | ∃ γ β : Fin P → R,
schedule only for 2p ≥ n; analytic variational protocols
                                                                       residualEnergy (ringQAOA N) γ β = e}
for transverse-field Ising chains were given by Ho and
                                                                     (1 / (2 * P + 2))
Hsieh [26]. The complementary regime 2p + 2 ≤ n,
where the p momenta (6) are the relevant modes [27],           Its proof combines two theorems:              the lower
is the one their schedule leaves open and the regime of        bound - εres  p    ≥    1/(2p   +  2)   for   all  angles
the conjecture; there they inferred existence from the         (residualEnergy lower bound) - and attainability
parameter count, which is not a proof [21, 28]. Supplying      - the explicit angle construction attaining the optimal
that existence proof is what closes the gap.                   value (residualEnergy attained).         Both are fully
                                                               formalized and checked by the kernel rather than
                                                               assumed. We have checked that these three theorems,
           MACHINE-PROVED RESULT                               together with residualEnergy, ringQAOA, and all
                                                               the definitions they depend on, faithfully encode the
   To supply that proof, we built on a Lean formalization      conjecture. The statement and its definitions were fixed
of quantum information that we developed in our parallel       before the model saw the gap, and the model never
work on machine-verified quantum cryptography [29]             changed them. The proof was filled by Claude Fable 5
- which provided the quantum-mechanical definitions            and it compiles cleanly with only the classical axiom set
and supporting mathematical theorems that underlie the         used in Mathlib.
                                                                                                                                             4

                                                  compiler diagnostics:

                                              type errors & open goals




  Input            Natural-language   formalize           Lean 4          compile        Lean 4 compiler          accept     Machine-checked
 problem              proof plan                       formalization                        & kernel                             proof


                 numerical   checks                                                     Verifier (Lean 4)


                       Python
                     unit-testing
                                               LLM (Claude Fable 5)


FIG. 1. The autoformalization feedback loop. The input is a formalized statement, here the open conjecture on the
optimal performance of depth-p QAOA on the Ising ring, handed to the system to prove. The LLM (Claude Fable 5 in our
case) drafts a proof strategy in natural language, validating its candidate statements with lightweight Python numerical checks
as part of the planning process. The Python checks are internal to the model and never reach Lean. Only a plan that passes
these internal checks is formalized as Lean 4 code. The Lean compiler and kernel - the external verifier - then check the attempt
and return diagnostics, namely type errors and the remaining proof goals, which the model uses to revise the plan. The cycle
repeats until Lean accepts the proof, yielding a terminal machine-checked certificate.


                       THE PROOF                                       under Ad(U )(v̂ · τk ) = U (v̂ · τk )U † = (Rv̂) · τk . Two
                                                                       SU(2) elements carry the per-mode evolution - the
  With a faithful formalization of the theorem and a                   depth-p propagator Uk and a fixed frame rotation Wk ,
machine certification provided by Lean, the validity                           1
                                                                                              z                                        y
of the proof is independent of whether any human
                                                                               Y
                                                                        Uk =         e−2iβℓ τk e−2iγℓ b̂k ·τk ,        Wk = e−ik τk /2 , (12)
understands it. Nevertheless, the proof is striking in its                     ℓ=p
own right, and we describe it below.
  By the decomposition (8) the problem is whether some                 whose adjoint actions on ẑ furnish the magnetization and
choice of the 2p angles makes every per-mode residual                  the cost axis,
vanish. The proof rests on a bridge to another problem:
each momentum mode’s propagator is a Quantum Signal                              mk = Ad(Uk ) ẑ,                 b̂k = Ad(Wk† ) ẑ.       (13)
Processing (QSP) sequence, which turns the steering
                                                                       With both now SU(2) objects, this lift is the entry point
condition into a condition on a single polynomial.
                                                                       into QSP - the theory of SU(2)-valued sequences built
                                                                       from alternating generators.
                                                                          Dynamical symmetry. SU(2) is not a symmetry of
                  A symmetry principle
                                                                       the Hamiltonian but a dynamical symmetry. The cost
                                                                       Hamiltonian singles out b̂k , so SO(3) does not commute
   The proof relies on a symmetry of the per-mode                      with HC . What holds instead is that the mixer and
dynamics that is not manifest in the original formulation              cost generators lie in a closed three-dimensional algebra,
of the problem.                                                        span{τkx , τky , τkz } ∼
                                                                                              = su(2), confining the dynamics to
   The SO(3) symmetry. By the per-mode reduction,                      SU(2). That the dynamical Lie algebra (DLA) is this
the p layers act not on the full 2n -dimensional state                 small is exceptional: for a generic QAOA instance the
but on a single Bloch vector mk per mode, rotated by                   DLA fills a substantial part of su(2n ), and the evolution
the alternating product of SO(3) elements (10). The                    explores exponentially many directions. Here it collapses
reachable per-mode dynamics is that of the rotation                    because the model is free - Jordan-Wigner maps HC
group on a three-vector, rather than the generic,                      and B to quadratic operators, whose bilinears close into
exponentially large QAOA evolution.                                    so(2n), and translational invariance diagonalizes that
   Lifting to SU(2). Rotations of a Bloch vector                       algebra   into su(2) blocks. The entire DLA is thus
are the adjoint action of the double cover                                                                               n
                                                                       L
                                                                          k su(2) k , of dimension O(p) rather than O(4 ). The
SU(2):     with τk as the spin- 12 generators, each                    DLA viewpoint on variational circuits is due to Larocca
Rn̂ (θ) ∈ SO(3) is the image of e−i(θ/2)n̂·τk ∈ SU(2)                  et al. [31] and, for free-fermionic circuits, Matos et al.
                                                                                                                          5

[32]; the dynamical Lie algebras of translation-invariant        Unitarity imposes |A|2 + |B|2 = 1 on the unit circle, and
free-fermion chains have since been fully classified [33].       parity G(1/z) = τkz G(z)τkz makes the diagonal even and
Because the dynamics preserve this block structure, the          the off-diagonal odd under the antipodal map z → 1/z.
problem reduces to independent single-qubit rotations,           Defining w := z 2 , A = z −L R(w) and B = z −L T (w), we
which is what makes a single-qubit theory like QSP the           then have
right tool.
                                                                                |R(w)|2 + |T (w)|2 = 1,
                                                                                                                       (21)
                                                                    wL R(1/w) = R(w),         wL T (1/w) = −T (w),
                       The keystone
                                                                 with R palindromic and T antipalindromic. We call a
   Consider the dot product b̂k · mk of the cost axis and        pair (R, T ) carrying this parity a class-L pair.
the magnetization, both SU(2) adjoint images of ẑ. Since
the adjoint action preserves dot products, defining the                          The steering condition
lifted propagator
                  G(k) := Wk Uk ∈ SU(2)                   (14)     By the keystone (15), the steering condition (11)
                                                                 becomes a clean statement about a single polynomial,
gives b̂k · mk = ẑ · Ad(G)ẑ. Since the ẑ-component
of Ad(G)ẑ equals |G11 |2 − |G21 |2 = 1 − 2|G21 |2 by the         εk = 0 ∀k ⇐⇒ T vanishes at p nodes wℓ = eikℓ , (22)
SU(2) structure, the per-mode residual collapses to a
single off-diagonal entry,                                       reducing simultaneous steering to a polynomial
                                                                 interpolation: optimality holds if and only if such
              εk = 1 − b̂k · mk = 2 |G21 (k)|2 .          (15)   a polynomial can be constructed.
Thus εk = 0 if and only if G(k) is diagonal: the steering
condition (11) therefore becomes the demand that G21                          Determining the polynomial
vanish at the p physical momentum modes.
                                                                    As a class-L entry, T has a rigid analytic structure -
                  G as a QSP sequence                            a polynomial of degree ≤ L in w, its only singularity a
                                                                 pole of order L at w = ∞ - so it is fixed by its zeros up
                                                                 to a constant.
   Since the cost axis is a frame rotation of ẑ, each cost
                                                                    The zeros fix the form. The steering condition is now
layer can be written as
                                                                 T (wℓ ) = 0 at the p nodes, and the class symmetry
                                           z
               e−2iγℓ b̂k ·τk = Wk† e−2iγℓ τk Wk .        (16)   supplies the rest. Antipalindromy wL T (1/w) = −T (w)
                                                                 forces a root at w = 1 (since T (1) = −T (1)) and
via b̂k · τk = Wk† τkz Wk . Using that τkz Wk τkz = Wk† one      drags each node’s mirror w̄ℓ = wM −ℓ as a root, so
can then bring the lifted propagator to the form                 {wℓ } ∪ {w̄ℓ } ∪ {1} is exactly the M := 2p + 2 roots of
                                1                                unity except −1 - the mode k = π, whose cost and mixer
                                Y           z
              G = (−1)p Wk            eiψj τk Wk ,               axes are antiparallel and which is therefore unsteerable.
                                                
                                                          (17)
                               j=2p                              Up to scale we therefore have
with                                                                                                          wM − 1
                                                                  T (w) = c (wL − wL−1 + · · · + w − 1) = c          . (23)
                    ψ2ℓ−1 = −(2γℓ + π2 ),                                                                      w+1
                                                          (18)
                      ψ2ℓ = −(2βℓ + π2 ),                          Unitarity fixes the scale. The scale is set at the
                                                                 unsteerable point: palindromy with L odd forces
which is identified as a standard QSP sequence [34,              R(−1) = 0, so |R(−1)|2 +|T (−1)|2 = 1 gives |T (−1)| = 1,
35] [36] - an alternating product of the signal Wk and           and since T (−1) = −cM ,
k-independent diagonal phases.
   Now define the signal variable z := eik/2 . In the                                     1     1
                                                                                     c=     =        .                 (24)
eigenbasis of τky the frame rotation is linear in z ±1                                    M   2p + 2
       Wk = z E+ + z −1 E− ,        E± = 21 (I ∓ τky ),   (19)   The FGG value 1/(2p + 2) thus emerges as the
                                                                 normalization of the unique node polynomial, fixed by
with E± the spectral projectors of τky . G is therefore an
                                                                 unitarity at the one mode that cannot be steered - a
SU(2)-valued Laurent polynomial of degree L := 2p + 1.
                                                                 structural explanation of a constant previously seen only
We can parametrize it as
                                                                 in numerics. As a consistency check, |T | ≤ 1 on the unit
                        A −B ∗                                 circle, since | sin( M
                                                                                      2 θ)| ≤ M | cos(θ/2)| for M even, with
                  G=              .               (20)
                         B A∗                                    equality only at θ = π.
                                                                                                                             6

            The complementary polynomial                                                 CONCLUSION


   To complete T to a class-L pair we need a palindromic                We have completed the proof of the FGG conjecture for
partner R with |R|2 + |T |2 = 1 on the unit circle.                  the ring of disagrees: for n even and 2p + 2 ≤ n, depth-p
Since |R(w)|2 = 1 − |T |2 ≥ 0, the Fejér–Riesz theorem              QAOA attains an approximation ratio (2p + 1)/(2p + 2)
[37, 38] guarantees a spectral square root R, palindromic            exactly. The proof is machine-verified in Lean 4.
because 1 − |T |2 is invariant under w 7→ 1/w, so the                   The proof the model produced has a clear physical
complementary polynomial exists and (R, T ) is a certified           structure.      It reduces the problem through the
class-L SU(2) pair. The freedom in this square root                  free-fermion symmetry to one SU(2) system per mode
- the p antipodal pairs - yields a 2p multiplicity of                and recognizes that system as a QSP sequence. This
admissible R, hence 2p optimal angle sets, a degeneracy              route is new to the problem: none of the papers on the
that is a consequence of the dynamical symmetry and                  conjecture [1, 20, 21, 25, 28] use QSP, the QSP “grand
was observed numerically in [21].                                    unification” [40] does not list QAOA, and the nearest
                                                                     result, that transverse-field Ising dynamics are QSP
                                                                     sequences [41], was not aimed at QAOA optimization.
                     The inverse map                                 The construction is not special to this model: the
                                                                     keystone (15) follows from the per-mode SU(2) structure
  To recover angles one maps (R, T ) back to a QSP                   alone, so any translation-invariant free-fermion [42, 43]
sequence.                                                            QAOA whose per-mode dynamics close into su(2) reduces
                                                                     to an analogous single-polynomial QSP steering problem.
  Haah’s factorization. Haah’s theorem [39] factors any
SU(2)-valued Laurent polynomial of degree L uniquely                    We believe the method extends well beyond this
and constructively,                                                  problem. Within quantum information science, natural
                                                                     targets include conjectures in quantum computation [44],
                       L
                       Y                                             the security analysis of quantum communication [45], and
              G = E0       (zPj + z −1 Qj ),                         secure computation [46]. More broadly, any well-posed
                       j=1                                   (25)    problem across mathematics, the physical sciences,
    Qj = I − Pj ,     Pj rank-one,      E0 ∈ SU(2),                  computer science, and engineering, once formalized, can
                                                                     be tackled in the same fashion using an interactive
an explicit degree-lowering peel, so the primitives can be           theorem prover such as Lean.
computed.                                                               Formal problems are a natural first domain for such
  Parity fixes the projectors. Our extra parity                      autonomous discovery precisely because they are closed :
G(1/z) = τkz G(z)τkz forces Qj = τkz Pj τkz , whose only             the kernel is a complete, deterministic, in-loop oracle,
solutions are equatorial,                                            independent of the model that generates the argument,
                                                                     so the knowledge the model must get right reduces to
            Pj = 21 (I + cos φj τkx + sin φj τky ),          (26)    the finite axioms and definitions fixed in the statement -
                                                                     a bounded “world model” a human audits once, within
a one-parameter family, one phase φj per primitive, with             which a hallucinated step cannot survive compilation and
E0 diagonal.                                                         is discarded rather than propagated.
   From primitives to angles. Each equatorial primitive
is the fixed signal Wk dressed by a diagonal phase
            z
D(t) := eitτk ,                                                                    ACKNOWLEDGMENTS

 zPφ +z −1 Qφ = D(tφ ) Wk D(−tφ ),             tφ = φ2 + π4 , (27)     We would like to thank Edward Farhi for insightful
                                                                     conversations that motivated this work. We thank
so the product (25) takes exactly the shape                          Kunal Marwaha for his comments on the draft and for a
of the QSP circuit (17), with internal phases                        conversation on our independently derived results.
ψj = tφj+1 − tφj = 12 (φj+1 − φj ).           Composing                K.S. acknowledges support from the European Union’s
with the affine relations of (17) gives the dictionary to            Horizon Europe research and innovation programme
the QAOA angles,                                                     under the Marie Sklodowska-Curie grant agreement
                                                                     No. 101202109. The research of M.B.S. is supported by
    γℓ = − 14 (φ2ℓ − φ2ℓ−1 ) − π4 ,                                  the Knut and Alice Wallenberg Foundation, Grant KAW
    βℓ = − 14 (φ2ℓ+1 − φ2ℓ ) − π4 ,     ℓ = 1, . . . , p.    (28)    2023.0490.
                                                                       Note added.      - During the preparation of the
The map is affine and explicitly invertible, completing              manuscript we became aware of an independent work on
the proof that optimal angles exist.                                 the same optimization problem [47].
                                                                                                                              7

         CODE AND DATA AVAILABILITY                             [20] Z. Wang, S. Hadfield, Z. Jiang, and E. G. Rieffel, Phys.
                                                                     Rev. A 97, 022304 (2018), arXiv:1706.02998 [quant-ph].
                                                                [21] G. B. Mbeng, R. Fazio, and G. E. Santoro, Optimal
  The complete Lean library, the formalized known                    quantum control with digitized Quantum Annealing
components, and Fable 5’s proof are available in the                 (2019), arXiv:1911.12259 [quant-ph].
repository [19].                                                [22] E. Lieb, T. Schultz, and D. Mattis, Ann. Phys. 16, 407
                                                                     (1961).
                                                                [23] P. Jordan and E. Wigner, Z. Phys. 47, 631 (1928).
                                                                [24] P. W. Anderson, Phys. Rev. 112, 1900 (1958).
                                                                [25] G. B. Mbeng, R. Fazio, and G. Santoro, Quantum
  ∗
     Corresponding author; Kfir@mit.edu                              Annealing: a journey through Digitalization, Control,
 [1] E. Farhi, J. Goldstone, and S. Gutmann, A Quantum               and hybrid Quantum Variational schemes (2019),
     Approximate        Optimization     Algorithm    (2014),        arXiv:1906.08948 [quant-ph].
     arXiv:1411.4028 [quant-ph].                                [26] W. W. Ho and T. H. Hsieh, SciPost Phys. 6, 029 (2019).
 [2] L. de Moura and S. Ullrich, in International Conference    [27] E. Farhi, D. Gamarnik, and S. Gutmann, The Quantum
     on Automated Deduction (Springer, 2021) pp. 625–643.            Approximate Optimization Algorithm Needs to See the
 [3] The mathlib Community, in Proceedings of the 9th                Whole Graph: A Typical Case (2020), arXiv:2004.09002
     ACM SIGPLAN International Conference on Certified               [quant-ph].
     Programs and Proofs (2020).                                [28] S. Bravyi, A. Kliesch, R. Koenig, and E. Tang, Phys. Rev.
 [4] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong,              Lett. 125, 260505 (2020), arXiv:1910.08980 [quant-ph].
     Nature 625, 476 (2024).                                    [29] M. Ben Shahar, J. Morag, D. Englund, and K. Sulimany
 [5] T. Hubert et al., Nature 651, 607 (2025).                       (2026), in preparation.
 [6] B. Romera-Paredes et al., Nature 625, 468 (2024).          [30] LeanScriber: an agentic toolkit for Lean 4 formalization,
 [7] Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats,               https://github.com/urikol/leanscriber (2026).
     M. Jamnik, and C. Szegedy, in Advances in Neural           [31] M. Larocca, P. Czarnik, K. Sharma, G. Muraleedharan,
     Information Processing Systems (NeurIPS) (2022)                 P. J. Coles, and M. Cerezo, Quantum 6, 824 (2022),
     arXiv:2205.12615.                                               arXiv:2105.14377 [quant-ph].
 [8] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song,        [32] G. Matos, C. N. Self, Z. Papić, K. Meichanetzidis, and
     S. Yu, S. Godil, R. Prenger, and A. Anandkumar,                 H. Dreyer, Quantum 7, 966 (2023), arXiv:2206.06400
     in Advances in Neural Information Processing Systems            [quant-ph].
     (NeurIPS), Datasets and Benchmarks Track (2023)            [33] R. Wiersema, E. Kökcü, A. F. Kemper, and B. N.
     arXiv:2306.15626.                                               Bakalov, npj Quantum Information 10, 110 (2024).
 [9] Z. Z. Ren et al., DeepSeek-Prover-V2: Advancing Formal     [34] G. H. Low and I. L. Chuang, Phys. Rev. Lett. 118,
     Mathematical Reasoning via Reinforcement Learning               010501 (2017), arXiv:1606.02685 [quant-ph].
     for Subgoal Decomposition (2025), arXiv:2504.21801         [35] A. Gilyén, Y. Su, G. H. Low, and N. Wiebe, in
     [cs.CL].                                                        51st Annual ACM SIGACT Symposium on Theory of
[10] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu,             Computing (2018) arXiv:1806.01838 [quant-ph].
     M. Jamnik, T. Lacroix, Y. Wu, and G. Lample, in            [36] G. H. Low, T. J. Yoder, and I. L. Chuang, Phys. Rev. X
     International Conference on Learning Representations            6, 041067 (2016).
     (ICLR) (2023) arXiv:2210.12283.                            [37] L. Fejér, J. Reine Angew. Math. 146, 53 (1916).
[11] B.    Breen,      M.   Del    Tredici,   J. McCarran,      [38] F. Riesz, J. Reine Angew. Math. 146, 83 (1916).
     J. Aspuru Mijares, W. W. Yin, K. Sulimany, J. M.           [39] J. Haah, Quantum 3, 190 (2019).
     Taylor, F. H. L. Koppens, and D. Englund, Ax-Prover:       [40] J. M. Martyn, Z. M. Rossi, A. K. Tan, and I. L. Chuang,
     A Deep Reasoning Agentic Framework for Theorem                  PRX Quantum 2, 040203 (2021), arXiv:2105.02859
     Proving in Mathematics and Quantum Physics (2025),              [quant-ph].
     arXiv:2510.12787 [cs.AI].                                  [41] V. M. Bastidas, S. Zeytinoğlu, Z. M. Rossi, I. L. Chuang,
[12] J. Wurtz and P. Love, Phys. Rev. A 103, 042612 (2021).          and W. J. Munro, Phys. Rev. B 109, 014306 (2024).
[13] M. P. Harrigan et al., Nature Physics 17, 332 (2021).      [42] A. Chapman and S. T. Flammia, Quantum 4, 278 (2020).
[14] H. Pichler, S.-T. Wang, L. Zhou, S. Choi, and              [43] A. Chapman, S. J. Elman, and R. L. Mann, A Unified
     M. D. Lukin, Quantum Optimization for Maximum                   Graph-Theoretic Framework for Free-Fermion Solvability
     Independent Set Using Rydberg Atom Arrays (2018),               (2023), arXiv:2305.15625.
     arXiv:1808.10816 [quant-ph].                               [44] J. Preskill, Quantum 2, 79 (2018).
[15] S. Ebadi et al., Science 376, 1209 (2022).                 [45] S. Pirandola, U. L. Andersen, L. Banchi, M. Berta,
[16] M.-T. Nguyen et al., PRX Quantum 4, 010316 (2023).              D. Bunandar, R. Colbeck, D. Englund, T. Gehring,
[17] H. Bernien et al., Nature 551, 579 (2017).                      C. Lupo, C. Ottaviani, J. Pereira, M. Razavi, J. S. Shaari,
[18] A. Keesling et al., Nature 568, 207 (2019).                     M. Tomamichel, V. C. Usenko, G. Vallone, P. Villoresi,
[19] U. Kol, M. Ben-Shahar, K. Sulimany, and D. Englund,             and P. Wallden, Adv. Opt. Photon. 12, 1012 (2020).
     QuantumOptimization: a Lean 4 / Mathlib library of         [46] K. Sulimany, S. K. Vadlamani, R. Hamerly, P. Iyengar,
     machine-verified quantum-optimization results, https:           and D. Englund, Phys. Rev. X 15, 041056 (2025).
     //github.com/urikol/QuantumOptimization (2026).            [47] K. Marwaha (2026), to appear.
