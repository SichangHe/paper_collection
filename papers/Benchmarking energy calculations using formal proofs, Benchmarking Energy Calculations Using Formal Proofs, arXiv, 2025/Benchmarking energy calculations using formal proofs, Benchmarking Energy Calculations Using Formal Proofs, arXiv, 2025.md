                                                                                                                                                                      1




                                                              Benchmarking Energy Calculations Using Formal Proofs
                                                                    Ejike D. Ugwuanyi1 , Colin T. Jones1 , John Velkey1 , and Tyler R. Josephson1,2,*
arXiv:2505.09095v2 [cond-mat.stat-mech] 18 Aug 2025




                                                                       1 Department of Chemical, Biochemical, and Environmental Engineering,

                                                                            University of Maryland, Baltimore County, Baltimore, MD, USA
                                                                             2 Department of Computer Science and Electrical Engineering,

                                                                            University of Maryland, Baltimore County, Baltimore, MD, USA
                                                                                      * Corresponding author, email: tjo@umbc.edu




                                                                                                       May 15, 2025


                                                                                                          Abstract

                                                            Traditional approaches for validating molecular simulations rely on making software open source and
                                                            transparent, incorporating unit testing, and generally employing human oversight. We propose an ap-
                                                            proach that eliminates software errors using formal logic, providing proofs of correctness. We use the
                                                            Lean theorem prover and programming language to create a rigorous, mathematically verified framework
                                                            for computing molecular interaction energies. We demonstrate this in LeanLJ, a package of functions,
                                                            proofs, and code execution software that implements Lennard-Jones energy calculations in periodic
                                                            boundaries. We introduce a strategy that uses polymorphic functions and type classes to bridge formal
                                                            proofs (about idealized Real numbers) and executable programs (over floating point numbers). Exe-
                                                            cution of LeanLJ matches the current gold standard NIST benchmarks, while providing even stronger
                                                            guarantees, given LeanLJ’s grounding in formal mathematics. This approach can be extended to for-
                                                            mally verified molecular simulations in particular and formally verified scientific computing software,
                                                            in general.

                                                      Keywords: Formal verification, Lean 4, molecular simulations, functional programming.



                                                                                                     1.   Introduction

                                                      Molecular simulations constitute an essential computational tool for understanding atomic-scale phenom-
                                                      ena, playing a critical role in predicting the physicochemical properties underlying fields such as materials
                                                      science, chemistry, and biophysics [1]. For instance, accurate simulations enable the study of molecular
                                                      interactions that dictate gas adsorption behaviours in porous materials [2] [3], influence solvation dynamics
                                                      in chemical solutions [4], and affect catalytic reactions on material surfaces [5]. Accurate modelling of
                                                      particle interactions lies at the core of molecular simulations [6] . Among the most fundamental and ex-
                                                      tensively used models are the Lennard-Jones potential, describing van der Waals interactions, and Coulomb
                                                      potentials, capturing electrostatic forces. The Lennard-Jones potential, specifically, finds significant applica-
                                                      tion in representing non-bonded interactions in chemically relevant systems such as simple fluids [7], noble
                                                                                                              2


gas clusters [8], hydrocarbon fluids [9], and molecular adsorption phenomena in zeolites or metal-organic
frameworks (MOFs) [10] [11]. It also describes the interaction between a pair of neutral atoms or molecules
based on their distance [12] [13] [14], and efficiently captures the balance between attractive and repul-
sive forces [15] [16]. Coulomb interactions are particularly critical for describing electrolyte solutions [17],
protein-ligand binding affinities [18], and charged colloidal systems [19] [18].


To accurately approximate infinite molecular systems from computationally manageable finite-sized sim-
ulations, periodic boundary conditions (PBC) are conventionally employed [20] [21]. In chemical simula-
tions, PBC enables the study of bulk-phase properties without boundary effects, such as predicting phase
behaviours in liquid water [22], ionic solutions [23], or polymer melts [24]. Furthermore, the minimum
image convention ensures that computational resources are efficiently utilized by considering only the near-
est periodic images in calculations [25], which is particularly important in simulations of dense chemical
environments like ionic liquids or liquid crystal phases.


Software tools like LAMMPS and Gromacs [26][27][28] allow users to simulate the dynamics of large
molecular systems. However, the sheer complexity of these software packages and the systems they intend
to model presents challenges in making simulations transparent, reproducible, useable by others and extensi-
ble (TRUE) [29]. For example, the SAMPL Challenges (Statistical Assessment of the Modelling of Proteins
and Ligands) [30] and the Industrial Fluid Properties Simulation Challenges [31][32] task computational
researchers to predict the solvation or binding free energies of small molecules or the thermophysical prop-
erties of fluids. Each year, researchers submit highly variable answers, reflecting differences in modelling
choices by the researchers (e.g. force fields, simulation conditions, free-energy extrapolation strategies,
etc.), as well as more hidden, subtle differences amongst software packages (e.g. default settings for man-
aging Lennard-Jones cut-off and settings for Ewald summation). Projects such as the Molecular Simulation
Design Framework (MoSDeF) [33] [29][34] and the Molecular Sciences Software Institute (MolSSI) [35]
address these issues by providing reproducible workflows for molecular simulation setup, and by teaching
and promoting best practices in software development [36]. Simulation software can also be validated by
comparing to benchmarks, such as those on the National Institute of Standards and Technology (NIST)
Standard Reference Simulation Website (SRSW) [37].


We propose an alternative paradigm for improving reliability of molecular simulations. To illustrate, con-
sider the taxonomy of programming errors in Table 1. The simplest are syntax errors: these are addressed
immediately because the code cannot compile, the editor highlights the mistake, and the programmer fixes
it. Runtime errors occur during code execution, and may arise when users run the program under condi-
tions not anticipated by the software developers. Nonetheless, runtime errors typically provide a helpful
error message pointing toward the source of the issue. The deepest issues are semantic errors in the mean-
ing of the software: Python would not complain about misinterpreting a scientific principle or incorrectly
transcribing math into code – it is simply not designed for that. Floating-point and round-off errors create
numerical inaccuracies, since computers do not operate with infinite mathematical precision. These are ad-
dressed by judicious choices of simulation settings and algorithm choices, and by checking conditions like
energy conservation after simulation completion [38].
                                                                                                            3


 Category of Error Example                              Intervention                          Lean
 Syntax                 Not closing parentheses         Editor                                Editor
 Runtime                Accessing element in list       Run program, program gives error      Editor
                        that doesn’t exist              message
 Semantic               Missing a minus sign,           Human inspection of the code;         Editor
                        transposing tensor indices      test-driven development; observing
                                                        anomalous behaviour
 Floating-point/        Subtracting small values        Modifying simulation methods,         –
 Round-off              from large values,              using double precision floats
                        ill-conditioned matrices

Table 1: Errors in scientific computing software, and typical interventions. Our goal is to develop an ap-
proach to address syntax, runtime, and semantic errors in Lean at the “editor” stage, before code is compiled.



In this work, we propose a strategy for catching syntax, runtime, and semantic errors at the “editor” stage,
namely, before the code is compiled. Our approach stems from the formal methods community in computer
science, which seeks to prove when software is correct by construction before it is run (also known as static
program analysis), unlike traditional testing, which checks for errors by running a program with different
inputs. This approach is handy in areas where even small errors can have significant consequences, such
as hardware design and critical software systems. A prominent example is the Pentium FDIV bug in Intel
processors in the early 1990s, the subject of a multi-million dollar recall stemming from a few misplaced
bits in chip software [39]. Now, formal verification approaches prove the correctness of such arithmetic
operations in manufactured chips [40]. Our approach most closely resembles that of Selsam, et al., who
explored how formal methods can be applied to machine learning systems in Certigrad [41] (Figure 1). By
proving the correctness of each step mathematically, this approach exposes errors that might otherwise slip
through traditional empirical testing. They highlight the ability of theorem provers like Lean to eliminate
entire classes of high-level errors that arise in complex software systems by enforcing correctness through
formal reasoning. They demonstrate their approach by building a variational auto-encoder in Lean, proving
properties about their implementation of stochastic gradient descent.


Most prior work on formal methods has focused on floating point operations [42]. In molecular simulations,
these are typically insignificant, but they can lead to issues in certain settings, such as when programs are
run with less precision to increase speed, or under extreme conditions. Tran and Wang [43], explored using
interval arithmetic to model the propagation of these uncertainties in molecular dynamics simulations. Our
work sets aside the imprecision of floating-point arithmetic, and instead focuses on verifying higher-level
logic and mathematics. Incorporating interval arithmetic into our approach would in principle be possible,
but these tools are currently in development [44].


Lean 4 is a theorem prover and functional programming language designed to write and verify mathematical
proofs, as well as write formally-verified software [45]. Unlike traditional programming languages used for
scientific computing (C, FORTRAN, Python, etc.), Lean provides a formally verified framework in which
proofs of correctness can be explicitly constructed and checked [46]. We previously used Lean to formalize
                                                                                                          4



                             Standard approach: test code empirically
                                  Debug
                                                                      Code that
                        Program                     Test
                                                                     passes tests
                           Formal approach: verify code mathematically
                                            Debug
                                                                               Code with
                Specify             Program                 Prove
                                                                              correct math

                                Hybrid method: use tests and proofs
                                            Debug
                                                                                        Code with
      Specify             Program                   Test              Prove
                                                                                       correct math

Figure 1: Comparison of code correctness approaches (adapted from [41]): the standard test-debug cycle,
formal verification using proofs, and a hybrid method combining tests and formal proofs, that we adopt here.


chemical physics [47]. Lean is also being used to formalize theories in high-energy physics [48]. We also
recognize Tomáš Skřivan’s ongoing SciLean project, which is working out methods for automated differen-
tiation and efficient, array-based computations in Lean [49].


In our work [47], we showed how theories in science can be rigorously encoded using the Lean theorem
prover, proving the correctness of the derivations, grounding them in the foundations of mathematics. We
formalized derivations of the Langmuir and BET adsorption models, meticulously defining assumptions and
derivations to ensure mathematical rigour. That work was limited to proofs in Lean – we extend that now to
executable programs with formally-verified properties.


In this paper, we first present a familiar, informal description of Lennard-Jones energy calculations of pe-
riodic fluids (Section 3). We then highlight the proof components (especially definitions and theorems) for
the formal implementation in Lean (Section 4). Section 5 describes how we implement these energy calcu-
lations in Lean, which requires novel approaches using functional programming, type polymorphism, and
monads. Section 6 compares our calculations with the results from the NIST SRSW benchmarks [37].



                                               2.    Methods

We implemented this using Lean version 4.16.0-rc2, Mathlib 4 at commit e1a3d4c, and Visual Studio Code
version 1.96. The source code is available in LeanLJ Repository.
                                                                                                                    5


                     3.   Informal Description of the Molecular Simulation System

The Lennard-Jones system is modelled as a collection of N particles confined within a cubic simulation
box of side length L. The position of each particle is represented as a vector in a three-dimensional space,
ri = (xi , yi , zi ), where i = 1, 2, . . . , N. The interaction between particles is governed by the Lennard-Jones
potential:                                                "          12           6 #
                                                               σ              σ
                                       VLJ (ri j ) = 4ε                     −                                     (1)
                                                               ri j           ri j

where ri j is the distance between particles i and j, ε represents the depth of the potential well, and σ is the
characteristic length scale.


Periodic boundary conditions (PBCs) are applied to simulate an infinite system as shown in the equation for
particle coordinates in the x, y, and z axes, respectively (Figure 2).
                                                                               x 
                                                                                  i
                                          xi_wrapped = xi − L · round                                             (2)
                                                                       L
                                                                      y 
                                                                        i
                                          yi_wrapped = yi − L · round                                             (3)
                                                                       L
                                                                      z 
                                                                        i
                                          zi_wrapped = zi − L · round                                             (4)
                                                                       L
Because the LJ particles are in a system with PBCs, the distance between two particles is not the Euclidean
distance, but the minimum image distance, the shortest pairwise distance considering the periodicity of the
box as given in the equation below.
                s                2                 2                 2
                                  ∆x                    ∆y                    ∆z
         ri j =   ∆x − L · round      + ∆y − L · round      + ∆z − L · round                                      (5)
                                  L                     L                     L
To improve computational efficiency, a cut-off radius rc is introduced. Interactions are considered only for
particle pairs that satisfy ri j ≤ rc , with contributions beyond this radius set to zero. This truncation neglects a
relatively minor contribution to the potential energy, depending on the cut-off radius rc as shown in Figure 3.
                                                    
                                                    V (r), r ≤ r
                                                      LJ          c
                                            V (r) =                                                               (6)
                                                    0,     r > rc
                                                                                                            h                  i
                                                                                                                σ 12
                                                                                                                         6
The Lennard Jones potential function is defined in part: When r ≤ rc , the potential is calculated as 4ε        r    − σr       ,
which captures both short-range repulsion and long-range attraction. For r > rc , the potential is set to zero,
reflecting the computational practice of truncating interactions beyond the cut-off to save resources. In ad-
dition, the inclusion of a cut-off distance makes the function practical for large-scale molecular systems.


The total internal energy Upair is calculated by summing the energies of the pairs of particles interacting.
                                                                                                         6




           (a) Periodic boundary conditions.                          (b) Minimum image convention.

Figure 2: (a) Periodic boundary conditions: Particles outside the central cubic simulation box are wrapped
back into it. Arrows represent the wrapping process along the directions. (b) Minimum image convention:
Particles interact with the nearest periodic image, ensuring the shortest distance is used in calculations.
The Euclidean distance (blue) is not used; the minimum image distance (black) is used instead, which is
equivalent to the minimum image distance between wrapped particles.




                       Figure 3: The Lennard-Jones potential, truncated at the cut-off.

This is given by the following equation, where V (ri j ) is the simulated pair potential:

                                           N   N
                                  Upair = ∑ ∑ V (ri j ),     where ri j ≤ rc .                          (7)
                                          i=1 j=i+1
                                                                                                                                       7


The neglected part of the Lennard-Jones potential can be approximately included by incorporating a “Long-
Range Correction” (LRC), also known as “tail corrections". This incorporates the ensemble-averaged energy
contribution of the particles beyond the cut-off radius, in a manner that only depends on the density of the
system and does not require pairwise distance calculations [25]. The LRC is given by:

                                                      1     ∞       Z
                                                ULRC = 4πρ    r2V (r)dr                                                             (8)
                                                      2    rc

where ρ is the density
                  of the system,  rc is the cut-off radius, and V (r) is the pairwise energy function.
                    σ 12
                              
                           σ 6
When V (r) = 4ε r        − r    , this integrates to:

                                           1     ∞     Z
                                     ULRC = 4πρ    r2VLJ (r)dr                                                                      (9)
                                           2    rc

                                                                      
                                             1               σ 12  σ 6
                                                  Z ∞
                                                       2
                                            = 4πρ     r 4ε       −         dr                                                    (10)
                                             2     rc        r      r

                                                            σ 12 σ 6
                                                                       
                                             8περ
                                            = 3                  −                                                               (11)
                                              rc            9rc6   3

                                      4.    Formally Defining the Mathematics



           Recursion over N molecules Recursion over N*(N-1)/2 pairs    Recursion for sum

                     Wrap                                                                                     Compare           P
                                        Calculate                            Sum to           Compute
  N particle       molecules                            Calculate           get total                        result with        A
                                        pairwise                                             long-range
  positions        into box             distances
                                                        LJ energy            energy                             NIST            S
                                                                                             correction
                                                                                                              standard          S

 Programming                                                                                                 Testing
 Proving                                                                                                       N       Cell    Match
                                       Proofs about                                                         Particles Length   NIST?
                  Proofs about                                                              Derivation of
                                         minimum        Proofs about                                          30       8.0      ✔
                    periodic                                                                 long-range
                                          image          LJ potential
                   boundaries                                                                correction       200      8.0      ✔
                                         distance
                                                                                                              400     10.0      ✔
                                 Proofs that recursion terminates                                             800     10.0      ✔



Figure 4: Workflow of the Lennard-Jones energy calculation using LeanLJ. The process involves recursive
programming, formal proofs, and comparison to NIST benchmarks.

The previous section was an informal description of these concepts; now, we turn to a formal description,
expressed as Lean code. Lean provides a structured framework to rigorously define the components of our
system and prove their properties. Figure 4 illustrates our code and the means by which it is verified. In this
section and the next, we describe the components of the system. We start by illustrating Lean’s capabilities
as a theorem prover.
                                                                                                              8


                                            4.1.      Introduction to Lean syntax

Here are a few examples to illustrate the syntax of Lean 4. Lean’s basic objects include types, tactics, def-
initions, and theorems; we do not introduce any custom types or tactics in this work, so we will focus on
definitions and theorems. A definition has the following basic structure1 :

 def name_of_object (p1 : parameter1) . . . : type_of_object := the_def_of_the_object


A theorem (or equivalently, a lemma) has the following basic structure:

 theorem name_of_theorem (p1 : parameter1) . . . (a1 : assumption1) . . . :
     thing_to_be_proved := by
   proof


Lean’s rich type system enables theorems to be stated and proved; while the user writes code, Lean effec-
tively checks the types of the objects in the code for consistency. Type-checking a theorem object amounts
to validating whether it is true. As the user writes the steps in a theorem’s proof, Lean provides a concise
overview of the current proof goal, as well as the current state of the assumptions and parameters. This
information is presented in the “Lean Infoview’ in VS Code, in what is known as a tactic state, which is
organized as follows:

 p1 : parameter1
 ...
 a1 : assumption1
 ⊢ current_state_of_goal


To learn more about Lean, we highly recommend the textbooks “Mechanics of Proof" by Heather Macbeth
[50] and “Functional Programming in Lean" by David Christiansen [46].



                                               4.2.    Lennard Jones Potential

We can write the Lennard-Jones potential energy function in multiple ways. In every case, we aim to for-
mally define Eq. 6, using a function that takes four parameters (ε, σ , r, and rc ) and returns the energy
between a pair of particles.


The first version of this is lj. In this version, all parameters are type R, for the Real numbers. Lean requires
this definition to be prefaced with the noncomputable keyword. Lean tries to generate executable bytecode
for its functions, but this is not possible, in general for the Real numbers. noncomputable signals to Lean
that this definition is only for Lean to reason about in proofs. We intend to execute other versions of this
function – see functions lj_Float and lj_p for computable LJ functions in Section 5.
  1 This overview is inspired by the presentation in [48].
                                                                                                           9




 noncomputable def lj (r r_c ε σ : R) : R :=
   if r ≤ r_c then
     4 * ε * ((σ / r) ^ 12 - (σ / r) ^ 6)
   else
     0


While lj may be a natural way to write Eq. 6, alternative formulations are typically used for efficient
molecular simulations. For instance, r−3 can be computed first, which is then squared to obtain r−6 , which
can be squared again to obtain r−12 . Our function lj_Real reflects this idea, using intermediate variables
like r6 and r12. Because lj_Real is also a function of Real numbers, it is also noncomputable.


 noncomputable def lj_Real (r r_c ε σ            : R) : R :=
   if r ≤ r_c then
     let r3 := (σ / r) ^ (3 : Nat)
     let r6 := r3 * r3
     let r12 := r6 * r6
     4 * ε * (r12 - r6)
   else
     0


Lean allows us to formally prove the equivalence of these two forms, as shown in the theorem lj_eq,
allowing us to use either representations confidently. This capability enables not only correctness, but also
flexibility in implementing the most efficient forms for simulation. Keep in mind that we do not address
floating-point or round-off errors; this guarantee holds only for idealized functions over Real numbers,
which have infinite precision. If a more-efficient version of a function is mathematically equivalent (over
Reals) to a base case, but leads to more round-off errors, that would not be detected in our formulation. A
more efficient version that is not mathematically equivalent (e.g. it invokes an approximation) would be
shown to be distinct by this approach.


 theorem lj_eq (r r_c ε σ : R) : lj_Real r r_c ε σ = lj r r_c ε σ := by
   unfold lj_Real
   unfold lj
   simp
   ring_nf


The theorem lj_eq formally proves that lj_Real r r_c ε σ = lj r r_c ε σ . This illustrates the
syntax of Lean functions: unlike Python, which uses parentheses to denote function application (e.g.,
lj_Real(r, r_c, epsilon, sigma)), Lean uses simple whitespace. In the expression lj_Real r r_c
ε σ , each argument is applied to the function from left to right, separated by spaces. Thus, lj_Real r
                                                                                                               10


r_c ε σ represents “apply the function lj_Real to these four arguments.” This compact syntax is helpful
in mathematical reasoning, where function application is so pervasive.


We can also prove various mathematical properties of our LJ function. Theorem cutoff_behaviour states
that for any r > rc , the value of the Lennard-Jones potential is zero. (The way to read this theorem, is “for
Real numbers ε, σ , r, and rc , assuming r > rc , this function evaluates to zero”). This reflects the practice of
truncating the potential beyond the cut-off distance.

 theorem cutoff_behaviour (ε σ r r_c : R) (h : r > r_c) :
     lj_Real ε σ r r_c = 0 := by
   unfold lj_Real
   simp [if_neg (not_le_of_gt h)]

                                                                                                h                i
                                                                                                    σ 12   σ 6
                                                                                                            
Theorem ljp_eq_le establishes that, in 0 < r ≤ rc , the Lennard-Jones potential is 4ε               r    − r      .
Lean can use logical operators like ∀ (for all) for defining properties of functions.

 theorem ljp_eq_le {r_c ε σ : R} : ∀ r ∈ {r | r > 0 ∧ r ≤ r_c},
     lj_Real r r_c ε σ = 4 * ε * ((σ / r)^12 - (σ / r)^6) := by
   intro r hr
   have h_r_le_rc : r ≤ r_c := hr.2
   unfold lj_Real
   rw [if_pos h_r_le_rc]
   ring


We also prove the continuity of the function in this range, in Theorem ljp_continuous_closed_domain
(for brevity, we just state the theorem here; the full proof is on GitHub). Continuity is essential in molecu-
lar dynamics simulations because forces are evaluated on the basis of energy gradients, and discontinuities
can introduce artificial forces, destabilizing numerical integration [7]. Importantly, we do not, indeed we
cannot, prove that this function is continuous for the whole domain of r; the LJ function diverges at r = 0
and undergoes a step change at r = rc . Researchers have implemented alternative truncation methods for
the LJ function, such as the truncated and shifted LJ function or the linear force shift function, which would
be continuous for all 0 < r [51]. These properties could be formalized in Lean, but in this work, we have
focused on the simple LJ function.


 theorem lj_p_continuous_closed_domain (r_c ε σ : R) :
     ContinuousOn (fun r => if r ≤ r_c then 4 * ε * (((σ / r) ^ 6) ^ 2 - (σ / r) ^ 6)
     else 0) {r | 0 < r ∧ r ≤ r_c} := by
                                                                                                                                  11


                                                  4.3.    Periodic Boundaries

We follow the formulation in Allen and Tildesley [7] in defining functions for wrapping molecules accord-
ing to periodic boundary conditions (PBCs) and calculating the minimum image distance. The periodic
boundary function wraps a position from anywhere in space into the bounds of the simulation box. This
function pbc takes in a one-dimensional position and box length and outputs a new position (all have type
R).


    noncomputable def pbc_Real (pos boxLength : R) : R :=
      pos - boxLength * round (pos / boxLength)


We formally proved that the wrapped displacement produced by the periodic boundary condition function
lies within the interval [−L/2, L/2] for any Real coordinate p and positive box length L. This ensures that
particles always interact with the nearest periodic image, which is a key assumption in molecular dynamics
simulations. The proof was constructed in Lean by expressing the wrapped position as L · δ , where δ =
p           p                                   1                            L
L − round L , and rigorously showing that |δ | ≤ 2 , hence |pbc_Real(p, L)| ≤ 2 .



    theorem abs_pbc_le (p L : R) (hL : 0 < L) : |pbc_Real p L| ≤ L / 2 := by
      dsimp [pbc_Real]
      let δ := (p / L) - round (p / L)
      have h_eq : p - L * round (p / L) = L * δ := by
        rw [mul_sub]
        field_simp [hL.ne’]
      rw [h_eq, abs_mul, abs_of_pos hL]
      have hδ : |δ | ≤ 1 / 2 := abs_diff_round_le_half (p / L)
      trans L * (1 / 2)
      · exact mul_le_mul_of_nonneg_left hδ hL.le
      · field_simp




                                              4.4.    Minimum Image Distance

In defining the minimum image distance, we found it more convenient to first define the squared minimum
image distance, and then take the square root of that to obtain the minimum image distance. The box
length boxLength and positions posA and posB are vectors in RN (with N = 3) where each component
corresponds to a coordinate in the respective dimension. This is specified using a vector type Fin 3 → R.
2   The function iterates over each of the three dimension and computes a displacement, which is adjusted
using the periodic boundary function pbc_Real. The adjusted displacements are squared and summed over
   2 Lean can handle particularly rich mathematics through its use of dependent types – types that depend on a value. Vector is an

example of this – it is a subtype of List that depends on a value, the length of the list, which in our case, is 3. This is one way in
which Lean avoids runtime errors; before the code compiles, Lean can ensure that a function taking a vector of length N will always
receive a vector of length N.
                                                                                                         12


all dimensions. In our squaredminImageDistance_Real function, the decide tactic is employed in each
invocation of the vectors posB and posA, to prove to Lean that elements 0, 1, and 2 are in scope.


 noncomputable def squaredminImageDistance_Real (posA posB : Fin 3 → R) (boxLength :
     Fin 3 → R) : R :=
   let dx := pbc_Real (posB (0: Fin 3) - posA (0: Fin 3)) (boxLength (0: Fin 3))
   let dy := pbc_Real (posB (1: Fin 3) - posA (1: Fin 3)) (boxLength (1: Fin 3))
   let dz := pbc_Real (posB (2: Fin 3) - posA (2: Fin 3)) (boxLength (2: Fin 3))
   dx^2 + dy^2 + dz^2


We can prove a neat property of how the periodic boundaries interact with the minimum image distance –
that the minimum image distance between arbitrary points in space is equivalent to the minimum image
distance between those points, after being wrapped into the simulation box. This is stated in theorem
squaredminImageDistance_theorem, which requires an inline invoking a λ function to iterate over the
box dimensions (for brevity, the proof steps are omitted here, but available on GitHub). This only holds for
non-zero box lengths.


 theorem squaredminImageDistance_theorem (boxLength posA posB : Fin 3 → R)
     (hL : ∀ i, boxLength i ̸= 0) squaredminImageDistance_Real boxLength posA posB =
     squaredminImageDistance_Real boxLength (λ i => pbc_Real (posA i) (boxLength i))
     (λ i => pbc_Real (posB i) (box_length i)) := by
     ...


Finally, the function minImageDistance_Real calls the squaredminImageDistance function, and takes
the square root to obtain the minimum image distance.

 noncomputable def minImageDistance_Real (posA posB boxLength : Fin 3 → R) : R :=
   (squaredminImageDistance_Real posA posB boxLength).sqrt


We can also prove that computed distances between particles are guaranteed to be non-negative in all ap-
plications of the minimum image convention; this can be useful when non-negativity is invoked in proofs
about energy calculations.


 theorem minImageDistance_real_nonneg ( posA posB boxLength : Fin 3 → R) :
     0 ≤ minImageDistance_Real posA posB boxLength := by
   unfold minImageDistance_real
   apply Real.sqrt_nonneg


We also proved that the minimum image distance between a particle and itself is always zero (theorem
                                                                                                             13


minImageDistance_self).

 theorem minImageDistance_real_self (pos boxLength : Fin 3 → R) :
     minImageDistance_Real pos pos boxLength = 0 := by
   unfold minImageDistance_Real squaredminImageDistance_Real
   have h0 : pbc_Real (pos (0: Fin 3) - pos (0: Fin 3)) (boxLength (0: Fin 3)) = 0 := by
     simp [pbc_Real, sub_self, zero_div, round_zero, mul_zero, sub_zero]
   have h1 : pbc_Real (pos (1: Fin 3) - pos (1: Fin 3)) (boxLength (1: Fin 3)) = 0 := by
     simp [pbc_Real, sub_self, zero_div, round_zero, mul_zero, sub_zero]
   have h2 : pbc_Real (pos (2: Fin 3) - pos (2: Fin 3)) (boxLength (2: Fin 3)) = 0 := by
     simp [pbc_Real, sub_self, zero_div, round_zero, mul_zero, sub_zero]
   rw [h0, h1, h2]
   simp


While the above formulations of pbc_Real and minImageDistance_Real lead to valid computations and
proofs, we are somewhat dissatisfied with the semantics. The pbc_Real function operates on particle
positions (i.e. xi ), wrapping them inside the box from outside. When this function is applied in the
minImageDistance function, it is being applied to a difference between particle positions (i.e. x j − xi ).
Lean does not complain, because in both cases, these are just real numbers, and everything checks out, but
a displacement is nonetheless not the same thing as a position. There may be a way to make this even more
rigorous, by defining a custom type for positions and restricting the pbc_Real function to only operate on
such a type, but we kept our approach simpler for now.



                                       4.5.   Long-Range Corrections

The long-range correction, given in Eq. 8, is computed using the function U_LRC, which depends on ρ, ε,
σ , and rc.

 noncomputable def U_LRC_Real (ρ ε σ rc : R) : R :=
   (8 * π * ρ * ε) * ((1/9) * (σ ^ 12 / rc ^ 9) - (1/3) * (σ ^ 6 / rc ^ 3))

                                                                                                       R
We can prove that this function follows from the integral definition of ULRC , Eq. 9. The integral         (r :
R) in Set.Ioi rc is interpreted using measure theory, and refers to an integral over the set Set.Ioi rc,
which is the open interval (rc , ∞). We state the theorem here and omit the proof for brevity, the full proof is
available on GitHub.

 theorem long_range_correction_equality (hr : 0 < rc) (ρ ε σ : R) :
                  (r : R) in Set.Ioi rc, 4*ε * (r^2 * (((σ / r)^12) - ((σ / r)^6))) =
               R
     (2*π*ρ) *
     U_LRC ρ ε σ rc π := by
     ...
                                                                                                         14


                                               5.   Code Execution

Combining formal proofs with numerical computation is central to this work. In this section, we elaborate
on three aspects of programming in Lean. Subsection 5.1 introduces the function for energy summation;
in Lean, this must be recursive instead of based on traditional for loops. Subsection 5.2 highlights our
approach for bridging computations and proofs using polymorphic functions. Subsection 5.3 describes
Lean’s approach to input and output.

                                        5.1.    Functional Programming

Traditional molecular simulation software is implemented using imperative programming languages (like C
and FORTRAN), but Lean is a functional programming language (like Haskell). Imperative programs are
about “doing” (following a step-by-step procedure), while functional programs are about “being” (defining
what a function is, which in Lean, ultimately enables proofs about it). Imperative programming is suscep-
tible to “side effects” that are avoided in functional programming, reducing security risks and improving
rigour. Functional programming avoids mutable data types; rather than updating (mutating) existing vari-
ables, such as assigning x=x+1, when new things must be computed, new variables are assigned. Lean 4
does support some imperative design patterns, but to get guarantees that come from proofs, writing code in
a functional style is generally preferred.


One of the most stark differences (and most relevant for molecular simulations) between imperative and
functional programming is the use of for- and while-loops. Pairwise energy calculations typically first loop
over particles i from 1 to N, then over particles j from i + 1 to N [7, 51]. This “double for loop” can be
expressed in Lean as follows:

 -- Imperative style, double for loop
 def total_energy_loop (positions : List (Fin 3 → Float)) (boxLength : Fin 3 → Float)
     (cutoff ε σ : Float) : Float :=
   Id.run do
     let mut energy := 0.0
     for i in [0 : positions.length] do
       for j in [i+1 : positions.length] do
         let r := minImageDistance positions[i]! positions[j]! boxLength
         let e := lj_Float r cutoff ε σ
         energy := energy + e
     return energy


Lean sets up for loops using the keywords Id.run, do, and for, and uses mut to denote energy as a mutable
variable. To be clear, Lean isn’t actually running imperative code; do notation is “syntax sugar” for purely
functional code, which is guaranteed to be free of side effects. Lean 4’s “functional but in-place” paradigm
for memory management makes it quite efficient compared to other functional programming languages [52].
Lean converts the above for loops into recursive functions. In the following function we illustrate, making
the recursion explicit:
                                                                                                                15




 -- Recursive style
 def total_energy_recursive (positions : List (Fin 3 → Float))
     (boxLength : Fin 3 → Float) (cutoff ε σ : Float) : Float :=
   let numAtoms := positions.length
   let rec energy : Nat → Nat → Float → Float
     | 0, _, acc => acc
     | i+1, 0, acc => energy i (i - 1) acc
     | i+1, j+1, acc =>
       let r := minImageDistance positions[i]! positions[j]! boxLength
       let e := lj_Float r cutoff ε σ
       energy (i+1) j (acc + e)
   energy numAtoms (numAtoms - 1) 0.0


Here, a recursive function energy is defined locally, as well an accumulation variable acc. In the central
function call, energy (i+1) j (acc + lj_Float r r_c ε σ ), energy adds one LJ energy contribu-
tion to the value of acc, using particle indices i + 1 and j to obtain the distance r. The remaining conditions
handle increments on the edge cases.
    However, we found neither of these functions to be particularly amenable to proofs. We are particularly
looking for a proof that the total number of pairs in the system is N ∗ (N − 1)/2. To do so, we defined a
helper function that generates the pairs. Our function pairs returns a list of pairs of atom indexes (e.g.
[(0,1), (0,2), (1,2)] when n = 3).

  -- Helper function to generate pairs
 def pairs (n : Nat) : List (Nat × Nat) :=
   (List.range n).flatMap fun i =>
     (List.range’ (i + 1) (n - (i + 1))).map fun j => (i, j)


We prove the length of this list is N ∗ (N − 1)/2 in pairs_length_eq in a long proof that uses mathematical
induction (full proof available on LeanLJ GitHub). In the absence of test data, such a proof could provide
confidence that the implementation is correct. We anticipate that such proofs would be useful for validating
energy calculations over molecules with complex exclusion rules (like excluding adjacent up to 1-4 interac-
tions in molecules), and higher-order interactions, like 3-body potentials.

 theorem pairs_length_eq (n : Nat) : (pairs n).length = n * (n - 1) / 2 := by


We use pairs in total_energy_pairs, a function that uses a simpler version of the recursive style to
accomplish this summation. This uses foldl, a function from functional programming that recursively ap-
plies a function to all elements of a list and accumulates the result, “folding” them together from the left.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      16


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="w0PVX34BPDtylG0k1mC5WXsMb0I=">AAAB9HicbVDLSgNBEOz1GeMr6tHLYBDiJeyKRPEU9OIxgnlAsoTeyWwyZPbhzGwwLPkOLx4U8erHePNvnCR70MSChqKqm+4uLxZcadv+tlZW19Y3NnNb+e2d3b39wsFhQ0WJpKxOIxHJloeKCR6yuuZasFYsGQaeYE1veDv1myMmFY/CBz2OmRtgP+Q+p6iN5PqlJ3JNOijiAZ51C0W7bM9AlomTkSJkqHULX51eRJOAhZoKVKrt2LF2U5SaU8Em+U6iWIx0iH3WNjTEgCk3nR09IadG6RE/kqZCTWbq74kUA6XGgWc6A9QDtehNxf+8dqL9KzflYZxoFtL5Ij8RREdkmgDpccmoFmNDkEpubiV0gBKpNjnlTQjO4svLpHFedirlyv1FsXqTxZGDYziBEjhwCVW4gxrUgcIjPMMrvFkj68V6tz7mrStWNnMEf2B9/gAngZES</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      f (x : ↵)

                                     f (x : R)
                                     <latexit sha1_base64="MnlaUSNxjsl/vfQKzgCTFpmsqwY=">AAAB+nicbVDLSgMxFL3js9bXVJdugkWomzIjUsVV0Y3LKvYBbSmZNNOGZjJDklHL2E9x40IRt36JO//GTDsLbT0QOJxzL/fkeBFnSjvOt7W0vLK6tp7byG9ube/s2oW9hgpjSWidhDyULQ8rypmgdc00p61IUhx4nDa90VXqN++pVCwUd3oc0W6AB4L5jGBtpJ5d8EuP6AJ1AqyHnpfcTo57dtEpO1OgReJmpAgZaj37q9MPSRxQoQnHSrVdJ9LdBEvNCKeTfCdWNMJkhAe0bajAAVXdZBp9go6M0kd+KM0TGk3V3xsJDpQaB56ZTCOqeS8V//PasfbPuwkTUaypILNDfsyRDlHaA+ozSYnmY0MwkcxkRWSIJSbatJU3JbjzX14kjZOyWylXbk6L1cusjhwcwCGUwIUzqMI11KAOBB7gGV7hzXqyXqx362M2umRlO/vwB9bnD9k8kx0=</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <latexit sha1_base64="FMepnFhpv4t1lx4dlbEQFn3MkXk=">AAAB/HicbVDLSsNAFJ34rPUV7dLNYBHqpiQiVVwVBXFZwT6gDWUynbRDJ5MwcyMNof6KGxeKuPVD3Pk3Th8LbT1w4XDOvdx7jx8LrsFxvq2V1bX1jc3cVn57Z3dv3z44bOgoUZTVaSQi1fKJZoJLVgcOgrVixUjoC9b0hzcTv/nIlOaRfIA0Zl5I+pIHnBIwUtcuBKURvsIdYCPIbkVEYHzatYtO2ZkCLxN3TopojlrX/ur0IpqETAIVROu268TgZUQBp4KN851Es5jQIemztqGShEx72fT4MT4xSg8HkTIlAU/V3xMZCbVOQ990hgQGetGbiP957QSCSy/jMk6ASTpbFCQCQ4QnSeAeV4yCSA0hVHFzK6YDoggFk1fehOAuvrxMGmdlt1Ku3J8Xq9fzOHLoCB2jEnLRBaqiO1RDdURRip7RK3qznqwX6936mLWuWPOZAvoD6/MHrXCULA==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    f (x : Float)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Proofs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Execution
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="1n+DhQXc4F++BP4QKN7vkNq9pF4=">AAAB9HicbVDLSgNBEOyNrxhfUY9eBoPgKeyKRI9BLx4jmAckS5idzCZDZnfWmd5gWPIdXjwo4tWP8ebfOHkcNLGgoajqprsrSKQw6LrfTm5tfWNzK79d2Nnd2z8oHh41jEo143WmpNKtgBouRczrKFDyVqI5jQLJm8Hwduo3R1wboeIHHCfcj2g/FqFgFK3kd5A/YVbTSoVm0i2W3LI7A1kl3oKUYIFat/jV6SmWRjxGJqkxbc9N0M+oRsEknxQ6qeEJZUPa521LYxpx42ezoyfkzCo9EiptK0YyU39PZDQyZhwFtjOiODDL3lT8z2unGF77mYiTFHnM5ovCVBJUZJoA6QnNGcqxJZRpYW8lbEA1ZWhzKtgQvOWXV0njouxVypX7y1L1ZhFHHk7gFM7Bgyuowh3UoA4MHuEZXuHNGTkvzrvzMW/NOYuZY/gD5/MHgdKSmQ==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         <latexit sha1_base64="NuuhMtfBYCg8TWNSEduYPC4bMZI=">AAAB+XicbVDLSgNBEJz1GeNr1aOXwSB4Crsi0WNQBI8RzAOSJcxOOsmQ2QczvSFhyZ948aCIV//Em3/jbLIHTSxoKKq66e7yYyk0Os63tba+sbm1Xdgp7u7tHxzaR8cNHSWKQ51HMlItn2mQIoQ6CpTQihWwwJfQ9Ed3md8cg9IiCp9wGoMXsEEo+oIzNFLXtjsIE0zvJ8CTTJl17ZJTduagq8TNSYnkqHXtr04v4kkAIXLJtG67ToxeyhQKLmFW7CQaYsZHbABtQ0MWgPbS+eUzem6UHu1HylSIdK7+nkhZoPU08E1nwHCol71M/M9rJ9i/8VIRxglCyBeL+omkGNEsBtoTCjjKqSGMK2FupXzIFONowiqaENzll1dJ47LsVsqVx6tS9TaPo0BOyRm5IC65JlXyQGqkTjgZk2fySt6s1Hqx3q2PReualc+ckD+wPn8AV42UIw==</latexit>




Figure 5: How polymorphic functions link proofs (over idealized Real numbers) with execution (over float-
ing point numbers). The polymorphic function f is defined for x with generic type α; proofs about f can be
written when x is Real, and computations with f can be executed when x is a float.



 -- Total energy function using pairs
  def total_energy_pairs (positions : List (Fin 3 → Float))
     (boxLength : Fin 3 → Float) (cutoff ε σ : Float) : Float :=
   let n := positions.length
   let indexPairs := pairs n
   indexPairs.foldl (fun acc (i, j) =>
     let r := minImageDistance_Float positions[i]! positions[j]! boxLength
     acc + lj_Float r cutoff ε σ
   ) 0.0


Lean automatically checks functions for termination, which is quite important for recursive functions, lest
they get trapped in an infinite loop. These are verified formally using tactics that operate behind-the-scenes;
only in more complicated cases, in which Lean cannot infer termination automatically, will the user be
prompted to write a termination proof. Likewise, Lean also ensures that array indexing is safe, preventing all
runtime errors associated with accessing out-of-bounds indices. In developing this code, we found execution
and comparing to the NIST tests was valuable for developing the logic of the loops and the recursion, as it
enabled quick feedback. Our code also incorporates tail recursion to facilitate efficient execution [46].

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               5.2.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            Polymorphism

In Lean, we can define functions specifically for Real numbers (R), which allows us to prove mathematical
properties, or for floating-point numbers (Float), which enables efficient numerical computation. However,
these separate implementations create a trade-off: the Real version is non-computable, meaning it cannot be
executed in actual simulations, while the Float version is not suitable for formal proofs, as floating-point
arithmetic lacks the necessary mathematical structure (in the typical standard for floating point addition,
IEEE 754, 0.1 + 0.2 ̸= 0.3). To bridge this gap, polymorphic functions are used, allowing the same def-
inition to work for multiple types (Fig. 5). By introducing a generic type α that can subsume both Real
and Float, we ensure that our function can operate on both Reals (R) for proofs and floats (Float) for
computations.
                                                                                                             17


            def pbc (position boxLength : α)
                [HSub α α α] [HMul α α α] [HDiv α α α] [HasRound α] : α :=
                position - boxLength * (HasRound.pround (position / boxLength))


                                     Typeclasses                      Instances
                                                                  Subtract(ℝ,ℝ)
                             HSub: type α “has subtraction”
                                                                  Subtract(Float,Float)

                                                                  Multiply(ℝ,ℝ)
                           HMul: type α “has multiplication”
                                                                  Multiply(Float,Float)

                                                                  Divide(ℝ,ℝ)
                                  HDiv: type α “has division”
                                                                  Divide(Float,Float)

                                                                  Round(ℝ,ℝ)
                              HasRound: type α “has round”
                                                                  Round(Float,Float)


Figure 6: Explanation of the polymorphic pbc function. The function is defined over a generic type α, and
the required operations—subtraction, multiplication, division, and rounding—are expressed through type
classes: HSub, HMul, HDiv, and HasRound. Each type class specifies that the type α must support a given
operation. For example, HSub α α α means α must support subtraction with two α inputs returning an
α result. Concrete instances, such as Float and R, implement these type classes to enable polymorphic
behaviour. This allows pbc to work with different numeric types, as long as they satisfy the required opera-
tions.


To illustrate, consider the function pbc (Fig. 6), which wraps a particle’s position into the simulation box us-
ing periodic boundary conditions. Section 4 showed pbc_Real, which operates on position and box length
with type R; pbc operates on position and box length with generic type α. We tell Lean more about what
α can be, using type classes and instances. Specially, pbc is defined for any type α that “knows how to”
subtract, multiply, divide, and round. These capabilities are provided through the type classes HSub, HMul,
HDiv, and HasRound. For example, the type class HSub [α α α] requires that there exists a definition of
subtraction between two members of α that would output a third member of α. HSub, HMul, and HDiv are
all defined in Mathlib; for rounding, we defined a custom type class, since Mathlib did not already define
that connection. This approach allows our definition of pbc to be used in two very different ways: with Real
numbers for formal proofs, and with floating-point numbers for actual simulations.


Prefacing each function with a long list of instances is rather cumbersome. We can group all of these in-
stances together into a single type class, RealLike, named thus because it is “like” Real numbers. RealLike
is ultimately compatible with Floats, but it doesn’t have all the properties of the Real numbers (after all, it
cannot use functions we did not attach to the type class). The RealLike type class captures the essential
features of types that behave like real numbers, making it easier to write numeric code that works across
different types such as Float or Int. It includes basic operations like addition, subtraction, multiplication,
division, negation, and exponentiation with natural numbers that appear in our equations (1, 3, 9, etc.). It
also provides comparisons (≤, <) that return Bool, along with constants like zero and one, and ways to
convert from natural and integer literals. In addition, RealLike extends two smaller type classes—HasSqrt
for square roots (used in distance calculations) and HasRound for rounding (used in periodic boundaries)
so that any type marked as RealLike is also expected to support those operations. This setup allows us to
                                                                                                         18


write clean, reusable, and type-safe numeric functions without tying them to one specific number type.


We note that this type class approach admits a small possibility of error that Lean will not catch. The
RealLike type class manually links certain Real-typed and Float-typed functions, and mistakes in RealLike
won’t be flagged by Lean. For example, a subtle error in which one rounding function rounded 0.5 down
while another rounded 0.5 up would not be detected by Lean. In fact, egregious errors linking a square root
and a cube root are also technically possible, so human oversight remains necessary with this approach.
Essentially, the RealLike type class defines which Real and Float functions are semantically equivalent,
and the human is responsible for ensuring correct semantics. The Lean community is developing more
systematic solutions, such as the ComputableReal project led by Alex Meiburg, which provides a more
principled, computable representation of real numbers that integrates cleanly with existing numeric type
classes [53].


 class RealLike (α : Type) extends HasRound α, HasSqrt α where
   add : α → α → α
   sub : α → α → α
   mul : α → α → α
   div : α → α → α
   neg : α → α
   pow : α → Nat → α
   le : α → α → Bool
   lt : α → α → Bool
   zero : α
   one : α
   ofNat : Nat → α
   ofInt : Int → α


For some more examples, we provide the implementations for the Lennard-Jones potential in three forms:
the polymorphic version (α), the Real number version (R), and the floating-point version (Float).


 -- Polymorphic version: Works for both R and Float
 def lj_p {α : Type} [RealLike α] (r r_c ε σ : α) : α :=
     if r ≤ r_c then
       let r3 := (σ / r) ^ (3 : Nat)
       let r6 := r3 * r3
       let r12 := r6 * r6
       4 * ε * (r12 - r6)
     else
       0
                                                                                                         19




 -- Real number version: Allows formal proofs but cannot compute
 noncomputable def lj_Real (r r_c ε σ : R) : R :=
     if r ≤ r_c then
       let r3 := (σ / r) ^ (3 : Nat)
       let r6 := r3 * r3
       let r12 := r6 * r6
       4 * ε * (r12 - r6)
     else
       0



 -- Floating-point version: Can compute but lacks proof capabilities
 def lj_Float (r r_c ε σ : Float) : Float :=
     if r ≤ r_c then
       let r3 := (σ / r) ^ (3 : Nat)
       let r6 := r3 * r3
       let r12 := r6 * r6
       4 * ε * (r12 - r6)
     else
       0


Ultimately, we use RealLike to define polymorphic versions of all executable functions in the overall
execution flow (Fig. 4) and connect them to their Real counterparts. The polymorphic version (with type
RealLike) of each function is that which is ultimately executed; the Real version or the polymorphic version
is used in the proofs.

                                      5.3.   Input and Output in Lean

Most of Lean is developed in terms of pure functions, whose behaviour can be guaranteed because the
argument types limit the domain of the function inputs. By chaining pure functions with pure functions
through-and-through, Lean guarantees there are no side effects. But input/output (IO) operations cannot
have the same guarantees. For instance, if one writes a molecular configuration file to disk, then reads it
back in, one cannot guarantee that some other process modified it in the meantime.


But to be a useful programming language, Lean must nonetheless have IO. Lean separates this cleanly from
its pure functions and math libraries, implementing it in the IO monad. This essentially serves as a bridge
between the messy, “outside” world and the safe, pure functions inside Lean (Figure 7).


Monads are used to handle many kinds of computation patterns in a clean and consistent way, such as op-
tional values, errors, and non-determinism. For example, the Option monad handles missing values, the
Except monad deals with errors without crashing, and the List monad allows multiple possible results
from a single computation. They are central in functional programming, but are encountered less often in
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            20


imperative languages; the interested reader can learn more here [46].



              “Outside world”                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    “Pure mathematics”
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Inputs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Lean objects
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 lj30.csv                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      positions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  <latexit sha1_base64="2dUhXUtZ2n70Sl71LDIc9HSOiW0=">AAAB+3icbVBNS8NAEN3Ur1q/Yj16CRbBU0lEqseiF48V7Ae0oWy2m3bpZjfsTqQl5K948aCIV/+IN/+NmzYHbX0w8Hhvhpl5QcyZBtf9tkobm1vbO+Xdyt7+weGRfVztaJkoQttEcql6AdaUM0HbwIDTXqwojgJOu8H0Lve7T1RpJsUjzGPqR3gsWMgIBiMN7eoA6AwA0lhqlks6G9o1t+4u4KwTryA1VKA1tL8GI0mSiAogHGvd99wY/BQrYITTrDJINI0xmeIx7RsqcES1ny5uz5xzo4ycUCpTApyF+nsixZHW8ygwnRGGiV71cvE/r59AeOOnTMQJUEGWi8KEOyCdPAhnxBQlwOeGYKLM78QhE6wwARNXxYTgrb68TjqXda9Rbzxc1Zq3RRxldIrO0AXy0DVqonvUQm1E0Aw9o1f0ZmXWi/VufSxbS1Yxc4L+wPr8AWCylVM=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <latexit sha1_base64="LekwvoWi4tfXgblD/GmqC2b3pLw=">AAAB+nicbVDLTsMwEHTKq5RXCkcuFhUSpygBVDhWcOFYJPqQ2qhyXKc1dZzI3hSq0E/hwgGEuPIl3Pgb3McBWkZaaTSzq92dIBFcg+t+W7mV1bX1jfxmYWt7Z3fPLu7XdZwqymo0FrFqBkQzwSWrAQfBmoliJAoEawSD64nfGDKleSzvYJQwPyI9yUNOCRipYxfbwB4BIBP3Z65D9XDcsUuu406Bl4k3JyU0R7Vjf7W7MU0jJoEKonXLcxPwM6KAU8HGhXaqWULogPRYy1BJIqb9bHr6GB8bpYvDWJmSgKfq74mMRFqPosB0RgT6etGbiP95rRTCSz/jMkmBSTpbFKYCQ4wnOeAuV4yCGBlCqOLmVkz7RBEKJq2CCcFbfHmZ1E8dr+yUb89Llat5HHl0iI7QCfLQBaqgG1RFNUTRA3pGr+jNerJerHfrY9aas+YzB+gPrM8fW7eUFA==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                <latexit sha1_base64="tdy5cBUx22e49sInllEMc7AaEZY=">AAAB7XicbVDLSgNBEOyNrxhfUY9eBoPgKeyKRI9BLx4jmAckS5idzCZj5rHMzAphyT948aCIV//Hm3/jJNmDJhY0FFXddHdFCWfG+v63V1hb39jcKm6Xdnb39g/Kh0cto1JNaJMornQnwoZyJmnTMstpJ9EUi4jTdjS+nfntJ6oNU/LBThIaCjyULGYEWye1eoYNBe6XK37VnwOtkiAnFcjR6Je/egNFUkGlJRwb0w38xIYZ1pYRTqelXmpogskYD2nXUYkFNWE2v3aKzpwyQLHSrqRFc/X3RIaFMRMRuU6B7cgsezPxP6+b2vg6zJhMUkslWSyKU46sQrPX0YBpSiyfOIKJZu5WREZYY2JdQCUXQrD88ippXVSDWrV2f1mp3+RxFOEETuEcAriCOtxBA5pA4BGe4RXePOW9eO/ex6K14OUzx/AH3ucPn/GPLg==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  pbc
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  <latexit sha1_base64="fKUGid2XFy+9zxmgR67ePGQuZQg=">AAAB83icbVBNS8NAEN3Ur1q/qh69BIvgqSQi1WPRi8cK9gOaUDbbabt0s1l2J2IJ/RtePCji1T/jzX/jts1BWx8MPN6bYWZepAQ36HnfTmFtfWNzq7hd2tnd2z8oHx61TJJqBk2WiER3ImpAcAlN5CigozTQOBLQjsa3M7/9CNrwRD7gREEY06HkA84oWikIEJ4QMVMRm/bKFa/qzeGuEj8nFZKj0St/Bf2EpTFIZIIa0/U9hWFGNXImYFoKUgOKsjEdQtdSSWMwYTa/eeqeWaXvDhJtS6I7V39PZDQ2ZhJHtjOmODLL3kz8z+umOLgOMy5ViiDZYtEgFS4m7iwAt881MBQTSyjT3N7qshHVlKGNqWRD8JdfXiWti6pfq9buLyv1mzyOIjkhp+Sc+OSK1MkdaZAmYUSRZ/JK3pzUeXHenY9Fa8HJZ47JHzifP8zYkjM=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ✏                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="w9hvxVEtH0CwHtdl/UDboK03PwY=">AAAB73icbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseiF48V7Ae0oWy2k3bpZhN3N0IJ/RNePCji1b/jzX/jts1BWx8MPN6bYWZekAiujet+O4W19Y3NreJ2aWd3b/+gfHjU0nGqGDZZLGLVCahGwSU2DTcCO4lCGgUC28H4dua3n1BpHssHM0nQj+hQ8pAzaqzU6WGiuYhlv1xxq+4cZJV4OalAjka//NUbxCyNUBomqNZdz02Mn1FlOBM4LfVSjQllYzrErqWSRqj9bH7vlJxZZUDCWNmShszV3xMZjbSeRIHtjKgZ6WVvJv7ndVMTXvsZl0lqULLFojAVxMRk9jwZcIXMiIkllClubyVsRBVlxkZUsiF4yy+vktZF1atVa/eXlfpNHkcRTuAUzsGDK6jDHTSgCQwEPMMrvDmPzovz7nwsWgtOPnMMf+B8/gBQY5Ar</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <latexit sha1_base64="WgmSAyBUwbvUKw4R6MMAjrlGhoQ=">AAACAnicbVDLSsNAFJ3UV62vqCtxEyyCq5KIVJdFXeiugn1AG8pkemOHTiZh5kYsobjxV9y4UMStX+HOv3H6WGjrgYHDOfdy5p4gEVyj635buYXFpeWV/GphbX1jc8ve3qnrOFUMaiwWsWoGVIPgEmrIUUAzUUCjQEAj6F+M/MY9KM1jeYuDBPyI3kkeckbRSB17r43wgIhZxOW18eDSZFLJYNixi27JHcOZJ96UFMkU1Y791e7GLI1AIhNU65bnJuhnVCFnAoaFdqohoaxvQlqGShqB9rPxCUPn0ChdJ4yVeRKdsfp7I6OR1oMoMJMRxZ6e9Ubif14rxfDMz7hMUgTJJkFhKhyMnVEfTpcrYCgGhlCmuPmrw3pUUYamtYIpwZs9eZ7Uj0teuVS+OSlWzqd15Mk+OSBHxCOnpEKuSJXUCCOP5Jm8kjfryXqx3q2PyWjOmu7skj+wPn8ASF+YAw==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          minImageDistance
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   L
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   <latexit sha1_base64="BkZirS3xLJHdCVdDDlMDKbxoLwk=">AAAB6HicbVA9SwNBEJ2LXzF+RS1tFoNgFe5EomXQxsIiAfMByRH2NnPJmr29Y3dPCCG/wMZCEVt/kp3/xk1yhSY+GHi8N8PMvCARXBvX/XZya+sbm1v57cLO7t7+QfHwqKnjVDFssFjEqh1QjYJLbBhuBLYThTQKBLaC0e3Mbz2h0jyWD2acoB/RgeQhZ9RYqX7fK5bcsjsHWSVeRkqQodYrfnX7MUsjlIYJqnXHcxPjT6gynAmcFrqpxoSyER1gx1JJI9T+ZH7olJxZpU/CWNmShszV3xMTGmk9jgLbGVEz1MveTPzP66QmvPYnXCapQckWi8JUEBOT2dekzxUyI8aWUKa4vZWwIVWUGZtNwYbgLb+8SpoXZa9SrtQvS9WbLI48nMApnIMHV1CFO6hBAxggPMMrvDmPzovz7nwsWnNONnMMf+B8/gCnG4zb</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       lj
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       <latexit sha1_base64="Bpl5vN91iatWgjcS2cEaeNWeURk=">AAAB8nicbVBNS8NAEJ34WetX1aOXxSJ4KolI9Vj04rGC/YA2lM12067dbMLuRCyhP8OLB0W8+mu8+W/ctjlo64OBx3szzMwLEikMuu63s7K6tr6xWdgqbu/s7u2XDg6bJk414w0Wy1i3A2q4FIo3UKDk7URzGgWSt4LRzdRvPXJtRKzucZxwP6IDJULBKFqp00X+hIiZfJj0SmW34s5AlomXkzLkqPdKX91+zNKIK2SSGtPx3AT9jGoUTPJJsZsanlA2ogPesVTRiBs/m508IadW6ZMw1rYUkpn6eyKjkTHjKLCdEcWhWfSm4n9eJ8Xwys+ESlLkis0XhakkGJPp/6QvNGcox5ZQpoW9lbAh1ZShTaloQ/AWX14mzfOKV61U7y7Ktes8jgIcwwmcgQeXUINbqEMDGMTwDK/w5qDz4rw7H/PWFSefOYI/cD5/ABMrkco=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   rc
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   <latexit sha1_base64="RSfXl0II+4HruVnZJLbm5qVQ0E4=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseiF48V7Qe0oWy2m3bpZhN2J0IJ/QlePCji1V/kzX/jts1BWx8MPN6bYWZekEhh0HW/ncLa+sbmVnG7tLO7t39QPjxqmTjVjDdZLGPdCajhUijeRIGSdxLNaRRI3g7GtzO//cS1EbF6xEnC/YgOlQgFo2ilB91n/XLFrbpzkFXi5aQCORr98ldvELM04gqZpMZ0PTdBP6MaBZN8WuqlhieUjemQdy1VNOLGz+anTsmZVQYkjLUthWSu/p7IaGTMJApsZ0RxZJa9mfif100xvPYzoZIUuWKLRWEqCcZk9jcZCM0ZyokllGlhbyVsRDVlaNMp2RC85ZdXSeui6tWqtfvLSv0mj6MIJ3AK5+DBFdThDhrQBAZDeIZXeHOk8+K8Ox+L1oKTzxzDHzifP1Hmjdc=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  IO Monad
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 U LRC
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <latexit sha1_base64="m6wy928VY0iOuuyEu84KBzeGdII=">AAAB+HicbVBNS8NAEN3Ur1o/GvXoJVgETyURqR6LvXjwUMW0hSaEzXbTLt1swu5ErKG/xIsHRbz6U7z5b9y2OWj1wcDjvRlm5oUpZwps+8sorayurW+UNytb2zu7VXNvv6OSTBLqkoQnshdiRTkT1AUGnPZSSXEcctoNx62Z372nUrFE3MEkpX6Mh4JFjGDQUmBWPaAPAJC7XnB925oGZs2u23NYf4lTkBoq0A7MT2+QkCymAgjHSvUdOwU/xxIY4XRa8TJFU0zGeEj7mgocU+Xn88On1rFWBlaUSF0CrLn6cyLHsVKTONSdMYaRWvZm4n9eP4Pows+ZSDOggiwWRRm3ILFmKVgDJikBPtEEE8n0rRYZYYkJ6KwqOgRn+eW/pHNadxr1xs1ZrXlZxFFGh+gInSAHnaMmukJt5CKCMvSEXtCr8Wg8G2/G+6K1ZBQzB+gXjI9v37WTPg==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Outputs
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            total energy
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            <latexit sha1_base64="QR3dfHEO9ewMZLvhoNoQnw9sQno=">AAAB/3icbVA9SwNBEN3zM8avqGBjcxgEq3AnEi2DNpYRzAckIext5pIle7vH7pwYzhT+FRsLRWz9G3b+GzfJFZr4YODx3gwz84JYcIOe9+0sLa+srq3nNvKbW9s7u4W9/bpRiWZQY0oo3QyoAcEl1JCjgGasgUaBgEYwvJ74jXvQhit5h6MYOhHtSx5yRtFK3cJhG+EBEVNUSEW7CxJ0fzTuFopeyZvCXSR+RookQ7Vb+Gr3FEsikMgENablezF2UqqRMwHjfDsxEFM2pH1oWSppBKaTTu8fuydW6bmh0rYkulP190RKI2NGUWA7I4oDM+9NxP+8VoLhZSflMk4QJJstChPhonInYbg9roGhGFlCmeb2VpcNqKYMbWR5G4I///IiqZ+V/HKpfHterFxlceTIETkmp8QnF6RCbkiV1Agjj+SZvJI358l5cd6dj1nrkpPNHJA/cD5/AF1klvw=</latexit>




                totalEnergy
                <latexit sha1_base64="vqnWDazMwTuuQ/NBRdhNbknlMYs=">AAAB/XicbVBNS8NAEN3Ur1q/4sfNS7AInkoiUj0WRfBYwX5AG8pmO22XbjZhdyLWUPwrXjwo4tX/4c1/47bNQVsfDDzem2FmXhALrtF1v63c0vLK6lp+vbCxubW9Y+/u1XWUKAY1FolINQOqQXAJNeQooBkroGEgoBEMryZ+4x6U5pG8w1EMfkj7kvc4o2ikjn3QRnhAxBQjpOJaguqPxh276JbcKZxF4mWkSDJUO/ZXuxuxJASJTFCtW54bo59ShZwJGBfaiYaYsiHtQ8tQSUPQfjq9fuwcG6Xr9CJlSqIzVX9PpDTUehQGpjOkONDz3kT8z2sl2LvwUy7jBEGy2aJeIhyMnEkUTpcrYChGhlCmuLnVYQOqKEMTWMGE4M2/vEjqpyWvXCrfnhUrl1kceXJIjsgJ8cg5qZAbUiU1wsgjeSav5M16sl6sd+tj1pqzspl98gfW5w+1fZYN</latexit>




Figure 7: The IO Monad as a bridge that links the verified, pure functions in Lean with the messy real world,
where data and simulation inputs reside. The CSV parser uses the IO Monad to read the particle coordinates
from lj30.csv into the Lean object positions.

To import the configuration files from the NIST SRSW, we first saved them as comma-separated values
(CSV) files. We adapted the CSV reader and used it to parse each configuration. In addition, users are asked
to manually enter simulation parameters such as the cut-off radius, σ , ε, and the length of the box through
the terminal. These user inputs and file reads are examples of interaction with the “outside world,” and
are handled explicitly in Lean using the IO monad. This makes it clear which parts of the program remain
exposed to sources of error – our setup does not provide guarantees against sources of error on the “outside”
of IO; if an incorrect value for σ were input, Lean would not catch it. This would be a form of semantic
error (Table 1) that our current implementation does not avoid.


Proofs in Lean only provide guarantees about pure functions; errors in the I/O layer cannot be validated in
this manner. This is why we advocate for both proofs and tests (Fig. 1). For instance, while developing
this application, our first approach for reading the configuration failed to read all atoms, leading to incorrect
energy calculations. Our proofs do not catch bugs like these, but the tests do.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  6.   Results

To evaluate our implementation, we compare the pairwise interaction energy (Upair ) and long-range correc-
tion (LRC) values computed using our Lean code with the NIST Standard Reference Simulation Website
(SRSW) benchmark values [37] for LJ particles in a cubic box (Table 2). The results show exact agreement
for all four systems, within the number of digits provided by NIST.
                                                                                                           21


Table 2: Comparison of LRC and Upair energy calculations from NIST SRSW [37] and LeanLJ for various
particle counts. Energies are reported in scientific notation (reduced units), with one more digit than NIST.

            Particles     Upair (Lean)      Upair (NIST)         LRC (Lean)       LRC (NIST)
               30       −1.67903E+01        −1.6790E+01       −5.45166E−01        −5.4517E−01
              200       −6.90004E+02        −6.9000E+02       −2.42296E+01       −2.42296E+01
              400       −1.14666E+03        −1.1467E+03       −4.96222E+01        −4.9622E+01
              800       −4.35154E+03        −4.3515E+03       −1.98488E+02        −1.9849E+02


                                       7.   Discussion and Outlook

In this study, we developed pairwise energy calculations in Lean and compared our results with the values
provided by the NIST SRSW benchmark. Our calculations agree to machine precision with the NIST
reference values. To be clear, our confidence in our system does not stem from its agreement with the
NIST benchmark, rather from the theorems we have proved in Lean that certify that the functions in LeanLJ
have those specified mathematical properties. For instance, the pbc function guarantees that all wrapped
particles lie in the interval [−L/2, L/2], and the derivation of the function computing long-range corrections
is validated mathematically. We assert that LeanLJ is a more reliable benchmark than the NIST SRSW, at
least for the components of the benchmark we have addressed. LeanLJ could be validated even further by
adding to the list of proved theorems about current functions.
We consider it helpful to reflect on the remaining sources of uncertainty in our code – considering what we
have verified, what could still be wrong? First, we are trusting in the axioms of mathematics, as expressed
in Lean’s core; errors here might compromise Mathlib, on which we depend. Second, our approach to poly-
morphism exposes us to mistakes in our RealLike type class, as we described in Section 5.2; Lean does not
check to ensure that RealLike links the correct Float- and Real-type functions. Third, when we developed
both polymorphic and floating-point versions of the same function for illustration purposes; we sometimes
mistakenly called the floating-point version in execution instead of the polymorphic version. In this case,
proofs for that function are not technically connected to the execution – since Lean does not require our
polymorphic code design, it does not flag such mistakes (these could be eliminated by not defining Float
and RealLike versions of the same functions). Fourth, we are still exposed to errors in input/output (Section
5.3), and in defining system-specific parameters, such as the force field parameters; these are mitigated by
the testing, but do not prevent a user from inputting incorrect parameters for calculations outside the scope
of the NIST benchmarks. A fifth source would be vulnerabilities in the broader operating system in which
the code is executed. Nonetheless, traditional molecular simulation have far more possibilities for errors,
such that many of these concerns are not considered in typical conversations about software correctness.


More broadly, this work demonstrates how Lean can provide a new paradigm for computational molecu-
lar simulations, where the results and the entire computational process are provably correct. Logical steps
to build on this framework include implementing support for triclinic simulation boxes, Ewald summation
for Coulomb interactions, neighbour lists to improve computational efficiency, and of course, integrating
Newtons equations of motion to evolve particle trajectories. Some of these are matters of implementation
                                                                                                              22


(triclinic cells), but others will involve grappling yet-unresolved questions of how to handle various approx-
imations in a formal environment, such as how to precisely describe the conditions under which neighbour
lists can be trusted.


Nonetheless, we believe that Lean can be used (in principle) to implement molecular simulation software
with all the features of the established packages used in daily practice. The user interface would not need to
be more complex; the proofs and theorems would all be handled in the back-end. Furthermore, this could
be integrated with software frameworks like MoSDeF [54] [33], that generate input files for multiple sim-
ulation engines. This would help address reproducibility and rigour at the “outside world” layer (Fig. 7)
in which the force field parameters, molecular specifications, and configuration are defined. This would
also enable rigorous evaluation of traditional software using Lean software as a benchmark; MoSDeF could
create inputs for both verified Lean software as well as for LAMMPS, and deviations between the respective
outputs may signal a bug in LAMMPS.


In our previous work, we showed Lean’s broader utility for formalizing derivations in science as math
proofs [47], digitizing key results in absorption theory, thermodynamics, and kinematics. Joseph Tooby-
Smith is also developing derivations in the high-energy physics field [48, 55]. These early works showcase
Lean’s rigour and versatility for building a library (or libraries) of formally-verified results in diverse areas
of science, facilitating rigorous verification of scientific ideas in different disciplines. In the long term,
we envision Lean being used to formalize not just interaction potentials or particle dynamics, but the very
foundations of statistical mechanics itself. The mathematics of ensemble theory, such as definitions of the
microcanonical (NVE) and canonical (NVT) ensembles and proofs about their properties, could be stated
precisely, and then directly linked to formally verified simulation code. For instance, we imagine proving
that a molecular dynamics simulation routine satisfies the conservation laws of the NVE ensemble, in the
limit of infinitesimal time steps, and verifying the detailed balance condition of Monte Carlo moves.
LeanLJ demonstrates how executable scientific computing software can be tied to such proofs, using poly-
morphic functions. We believe this approach is quite general for reasoning about idealized Real-valued
functions in scientific theories, while linking these to floating-point executions in scientific computing soft-
ware. Certigrad’s [41] approach is also worth considering; this verifies the high-level mathematics in Lean,
and then links high-level functions to unverified, but efficient, linear algebra libraries written in C. Compared
to our approach, Certigrad’s “bridge” between verified math and executable math consequently happens at
a higher level; our polymorphic functions build this bridge at the level of individual math operators (e.g.
addition, division) and constants (e.g. π).


Scientific computing benchmarks are typically based on human oversight and software best practices [36];
formal Lean verification offers an even more rigorous alternative, allowing rigorous mathematical proofs
that the implemented software is correct. This shift from empirical validation to formal proof introduces
a new level of confidence in molecular simulations, setting the stage for more reliable and mathematically
sound scientific computing.
                                                                                                       23


                                              Conclusion

This work demonstrates how formal methods can complement molecular simulations by providing proven
guarantees about the properties of the molecular simulation system. While still in its early stages, this
approach opens a path toward mathematically-verified simulations.


                                          Acknowledgements

The authors thank the members of the Lean Zulip for helpful discussions, especially Tomáš Skřivan for
his insights into polymorphic functions. This material is based on work supported by the National Science
Foundation (NSF) CAREER Award #2236769.


                                        Declaration of Interest

The authors declare no competing financial or personal interests that could influence the work reported in
this paper.


                                           Data Availability

All code, proofs, and benchmark files are on the ATOMS Lab Github.


                                                ORCID

Ejike D. Ugwuanyi https://orcid.org/0009-0006-4335-5428
Colin T. Jones https://orcid.org/0009-0007-9013-8036
John Velkey https://orcid.org/0000-0001-5156-7451
Tyler R. Josephson https://orcid.org/0000-0002-0100-0227

                                              References
 [1] Hugo A. L. Filipe and Luís M. S. Loura. Molecular Dynamics Simulations: Advances and Applica-
     tions. Molecules, 27(7):2105, March 2022. URL: https://www.mdpi.com/1420-3049/27/7/2105,
     doi:10.3390/molecules27072105.
 [2] Lei Sun, Li Yang, Ya-Dong Zhang, Qi Shi, Rui-Feng Lu, and Wei-Qiao Deng. Accurate van der Waals
     force field for gas adsorption in porous materials. Journal of Computational Chemistry, 38(23):1991–
     1999, September 2017. URL: https://onlinelibrary.wiley.com/doi/10.1002/jcc.24832,
     doi:10.1002/jcc.24832.
 [3] Lei Sun and Weiqiao Deng. Progress and Prospect of Theoretical Simulation of Microporous Materials.
     Acta Chimica Sinica, 73(6):579, 2015. URL: http://sioc-journal.cn/Jwk_hxxb/CN/abstract/
     abstract344992.shtml, doi:10.6023/A15030192.
 [4] Alan E. Mark and Wilfred F. Van Gunsteren. Decomposition of the Free Energy of a Sys-
     tem in Terms of Specific Interactions. Journal of Molecular Biology, 240(2):167–176, July
     1994. URL: https://linkinghub.elsevier.com/retrieve/pii/S0022283684714306, doi:
     10.1006/jmbi.1994.1430.
 [5] Raphael S. Alvim. Material Surfaces and Interfaces: Characterization, Molecular Adsorption and
     Heterogeneous Catalysis by Computational Simulation. Revista Virtual de Química, 15(2):262–
     282, 2023. URL: https://rvq.sbq.org.br/audiencia_pdf.asp?aid2=1571&nomeArquivo=
     v15n2a07.pdf, doi:10.21577/1984-6835.20220124.
                                                                                                       24


 [6] Andrew R Leach. Molecular Modelling: Principles and Applications. Prentice Hall, 2nd edition,
     2001.
 [7] Michael Patrick Allen and Dominic J. Tildesley. Computer simulation of liquids. Oxford University
     Press, Oxford, 2nd ed edition, 2017.
 [8] Loup Verlet. Computer "Experiments" on Classical Fluids. I. Thermodynamical Properties of Lennard-
     Jones Molecules. Physical Review, 159(1):98–103, July 1967. URL: https://link.aps.org/doi/
     10.1103/PhysRev.159.98, doi:10.1103/PhysRev.159.98.
 [9] Joshua T. Horton, Simon Boothroyd, Pavan Kumar Behara, David L. Mobley, and Daniel J. Cole. A
     transferable double exponential potential for condensed phase simulations of small molecules. Digital
     Discovery, 2(4):1178–1187, 2023. URL: https://xlink.rsc.org/?DOI=D3DD00070B, doi:10.
     1039/D3DD00070B.
[10] Jiapu Zhang. A Brief Review on Results and Computational Algorithms for Minimizing the Lennard-
     Jones Potential, December 2010. arXiv:1101.0039 [physics]. URL: http://arxiv.org/abs/1101.
     0039, doi:10.48550/arXiv.1101.0039.
[11] Junwen Wang and Shengfeng Cheng. Integrated Lennard-Jones Potential between a Sphere and a
     Thin Rod, May 2024. arXiv:2405.03944 [cond-mat]. URL: http://arxiv.org/abs/2405.03944,
     doi:10.48550/arXiv.2405.03944.
[12] Peter Schwerdtfeger, Antony Burrows, and Odile R. Smits. The Lennard Jones Potential Revisited –
     Analytical Expressions for Vibrational Effects in Cubic and Hexagonal Close-Packed Lattices. The
     Journal of Physical Chemistry A, 125(14):3037–3057, April 2021. arXiv:2012.05413 [cond-mat].
     URL: http://arxiv.org/abs/2012.05413, doi:10.1021/acs.jpca.1c00012.
[13] Xipeng Wang, Simón Ramírez-Hinestrosa, Jure Dobnikar, and Daan Frenkel. The Lennard-Jones
     potential: when (not) to use it. Physical Chemistry Chemical Physics, 22(19):10624–10633, May
     2020. Publisher: The Royal Society of Chemistry. URL: https://pubs.rsc.org/en/content/
     articlelanding/2020/cp/c9cp05445f, doi:10.1039/C9CP05445F.
[14] A. Rahman. Correlations in the Motion of Atoms in Liquid Argon. Physical Review, 136(2A):A405–
     A411, October 1964. URL: https://link.aps.org/doi/10.1103/PhysRev.136.A405, doi:10.
     1103/PhysRev.136.A405.
[15] Chenyang Sun, Yaning Zhang, Chaofeng Hou, and Wei Ge. A new correlation model for predicting the
     melting and boiling temperatures of the Lennard-Jones systems. Physica Scripta, 98(1):015702, Jan-
     uary 2023. URL: https://iopscience.iop.org/article/10.1088/1402-4896/aca443, doi:
     10.1088/1402-4896/aca443.
[16] J.J. Nicolas, K.E. Gubbins, W.B. Streett, and D.J. Tildesley. Equation of state for the Lennard-Jones
     fluid. Molecular Physics, 37(5):1429–1454, May 1979. URL: https://www.tandfonline.com/
     doi/full/10.1080/00268977900101051, doi:10.1080/00268977900101051.
[17] W. Ronald Fawcett. Electrolyte Solutions. In Liquids, Solutions, and Interfaces. Oxford University
     Press, July 2004. URL: https://academic.oup.com/book/40724/chapter/348485529, doi:
     10.1093/oso/9780195094329.003.0007.
[18] H L Wen, E Allahyarov, C N Likos, R Blaak, J Dzubiella, A Jusufi, N Hoffmann, and
     H M Harreis. Charged colloids, polyelectrolytes and biomolecules viewed as strongly coupled
     Coulomb systems. Journal of Physics A: Mathematical and General, 36(22):5827–5834, June
     2003. URL: https://iopscience.iop.org/article/10.1088/0305-4470/36/22/301, doi:
     10.1088/0305-4470/36/22/301.
[19] David S. Dean, Jure Dobnikar, Ali Naji, and Rudolf Podgornik, editors. Electrostatics of Soft
     and Disordered Matter. Jenny Stanford Publishing, 0 edition, May 2014. URL: https://www.
     taylorfrancis.com/books/9789814411868, doi:10.1201/b15597.
[20] Jerry Z. Yang and Xiantao Li. Comparative study of boundary conditions for molecular dynamics
     simulations of solids at low temperature. Physical Review B, 73(22):224111, June 2006. URL: https:
     //link.aps.org/doi/10.1103/PhysRevB.73.224111, doi:10.1103/PhysRevB.73.224111.
                                                                                                         25


[21] Luke Mizzi, Daphne Attard, Ruben Gatt, Krzysztof K. Dudek, Brian Ellul, and Joseph N.
     Grima. Implementation of periodic boundary conditions for loading of mechanical metamate-
     rials and other complex geometric microstructures using finite element analysis. Engineering
     with Computers, 37(3):1765–1779, July 2021. URL: https://link.springer.com/10.1007/
     s00366-019-00910-1, doi:10.1007/s00366-019-00910-1.
[22] Etienne Palos, Ethan F. Bull-Vulpe, Xuanyu Zhu, Henry Agnew, Shreya Gupta, Suman
     Saha, and Francesco Paesani.       Current Status of the MB-pol Data-Driven Many-Body Po-
     tential for Predictive Simulations of Water Across Different Phases, September 2024. URL:
     https://chemrxiv.org/engage/chemrxiv/article-details/66f98ca451558a15ef84353d,
     doi:10.26434/chemrxiv-2024-9r9gn-v2.
[23] John W Lawson and Justin B Haskins. Atomistic Simulations of Ionic Liquid and Polymer Elec-
     trolytes: From Bulk Phases to Interfacial Behavior. ECS Meeting Abstracts, MA2017-01(22):1147–
     1147, April 2017. URL: https://iopscience.iop.org/article/10.1149/MA2017-01/22/
     1147, doi:10.1149/MA2017-01/22/1147.
[24] James P. Andrews and Estela Blaisten-Barojas. Workflow for investigating thermodynamic, struc-
     tural and energy properties of condensed polymer systems from Molecular Dynamics, 2022. Version
     Number: 1. URL: https://arxiv.org/abs/2203.02819, doi:10.48550/ARXIV.2203.02819.
[25] W. W. Wood and F. R. Parker. Monte Carlo Equation of State of Molecules Interacting with the
     Lennard-Jones Potential. I. A Supercritical Isotherm at about Twice the Critical Temperature. The
     Journal of Chemical Physics, 27(3):720–733, September 1957. URL: https://pubs.aip.org/
     jcp/article/27/3/720/204747/Monte-Carlo-Equation-of-State-of-Molecules, doi:10.
     1063/1.1743822.
[26] Steve Plimpton. Fast Parallel Algorithms for Short-Range Molecular Dynamics. Journal of Computa-
     tional Physics, 117(1):1–19, March 1995. URL: https://linkinghub.elsevier.com/retrieve/
     pii/S002199918571039X, doi:10.1006/jcph.1995.1039.
[27] Mark James Abraham, Teemu Murtola, Roland Schulz, Szilárd Páll, Jeremy C. Smith, Berk
     Hess, and Erik Lindahl.       GROMACS: High performance molecular simulations through
     multi-level parallelism from laptops to supercomputers. SoftwareX, 1-2:19–25, September
     2015. URL: https://linkinghub.elsevier.com/retrieve/pii/S2352711015000059, doi:
     10.1016/j.softx.2015.06.001.
[28] David Van Der Spoel, Erik Lindahl, Berk Hess, Gerrit Groenhof, Alan E. Mark, and Herman J. C.
     Berendsen. GROMACS: Fast, flexible, and free. Journal of Computational Chemistry, 26(16):1701–
     1718, December 2005. URL: https://onlinelibrary.wiley.com/doi/10.1002/jcc.20291,
     doi:10.1002/jcc.20291.
[29] Matthew W. Thompson, Justin B. Gilmer, Ray A. Matsumoto, Co D. Quach, Parashara Shamaprasad,
     Alexander H. Yang, Christopher R. Iacovella, Clare McCabe, and Peter T. Cummings. Towards molec-
     ular simulations that are transparent, reproducible, usable by others, and extensible (TRUE). Molecular
     Physics, 118(9-10):e1742938, June 2020. URL: https://www.tandfonline.com/doi/full/10.
     1080/00268976.2020.1742938, doi:10.1080/00268976.2020.1742938.
[30] Anthony Nicholls, David L. Mobley, J. Peter Guthrie, John D. Chodera, Christopher I. Bayly,
     Matthew D. Cooper, and Vijay S. Pande. Predicting Small-Molecule Solvation Free Energies: An
     Informal Blind Test for Computational Chemistry. Journal of Medicinal Chemistry, 51(4):769–
     779, February 2008. URL: https://pubs.acs.org/doi/10.1021/jm070549%2B, doi:10.1021/
     jm070549+.
[31] Daniel G. Friend, David J. Frurip, Joseph W. Magee, and James D. Olson. Establishing bench-
     marks for the first industrial fluids simulation challenge. Fluid Phase Equilibria, 217(1):11–15,
     March 2004. URL: https://linkinghub.elsevier.com/retrieve/pii/S0378381203003571,
     doi:10.1016/S0378-3812(03)00357-1.
[32] Fiona Case, Anne Chaka, Daniel G Friend, David Frurip, Joseph Golab, Russell Johnson,
     Jonathan Moore, Raymond D Mountain, James Olson, Martin Schiller, and Joey Storer. The
     first industrial fluid properties simulation challenge. Fluid Phase Equilibria, 217(1):1–10, March
     2004. URL: https://linkinghub.elsevier.com/retrieve/pii/S0378381203002085, doi:
     10.1016/S0378-3812(03)00208-5.
                                                                                                         26


[33] Nicholas C. Craven, Ramanish Singh, Co D. Quach, Justin B. Gilmer, Brad Crawford, Eliseo Marin-
     Rimoldi, Ryan Smith, Ryan DeFever, Maxim S. Dyukov, Jenny W. Fothergill, Chris Jones, Timothy C.
     Moore, Brandon L. Butler, Joshua A. Anderson, Christopher R. Iacovella, Eric Jankowski, Edward J.
     Maginn, Jeffrey J. Potoff, Sharon C. Glotzer, Peter T. Cummings, Clare McCabe, and J. Ilja Siepmann.
     Achieving Reproducibility and Replicability of Molecular Dynamics and Monte Carlo Simulations
     Using the Molecular Simulation Design Framework (MoSDeF). Journal of Chemical & Engineer-
     ing Data, 70(6):2178–2199, June 2025. URL: https://pubs.acs.org/doi/10.1021/acs.jced.
     5c00010, doi:10.1021/acs.jced.5c00010.
[34] Brad Crawford, Umesh Timalsina, Co D. Quach, Nicholas C. Craven, Justin B. Gilmer, Clare McCabe,
     Peter T. Cummings, and Jeffrey J. Potoff. MoSDeF-GOMC: Python Software for the Creation of
     Scientific Workflows for the Monte Carlo Simulation Engine GOMC. Journal of Chemical Information
     and Modeling, 63(4):1218–1228, February 2023. URL: https://pubs.acs.org/doi/10.1021/
     acs.jcim.2c01498, doi:10.1021/acs.jcim.2c01498.
[35] Jessica A. Nash, Mohammad Mostafanejad, T. Daniel Crawford, and Ashley Ringer McDonald.
     MolSSI Education: Empowering the Next Generation of Computational Molecular Scientists. Com-
     puting in Science & Engineering, 24(3):72–76, May 2022. URL: https://ieeexplore.ieee.org/
     document/9882989/, doi:10.1109/MCSE.2022.3165607.
[36] Matthew W. Thompson, Justin B. Gilmer, Ray A. Matsumoto, Co D. Quach, Parashara Shamaprasad,
     Alexander H. Yang, Christopher R. Iacovella, Clare McCabe, and Peter T. Cummings. Towards molec-
     ular simulations that are transparent, reproducible, usable by others, and extensible (TRUE). Molecular
     Physics, 118(9-10):e1742938, June 2020. URL: https://www.tandfonline.com/doi/full/10.
     1080/00268976.2020.1742938, doi:10.1080/00268976.2020.1742938.
[37] Vincent K. Shen, Daniel W. Siderius, William P. Krekelberg, and Harold W. Hatch, editors. NIST
     Standard Reference Simulation Website. Number 173 in NIST Standard Reference Database. National
     Institute of Standards and Technology, Gaithersburg, MD, 20899, 2017. URL: https://doi.org/
     10.18434/T4M88Q.
[38] Pascal T. Merz and Michael R. Shirts. Testing for physical validity in molecular simulations. PLOS
     ONE, 13(9):e0202764, September 2018. URL: https://dx.plos.org/10.1371/journal.pone.
     0202764, doi:10.1371/journal.pone.0202764.
[39] D. Price. Pentium FDIV flaw-lessons learned. IEEE Micro, 15(2):86–88, April 1995. URL: https:
     //ieeexplore.ieee.org/document/372360/, doi:10.1109/40.372360.
[40] R. Kaivola and N. Narasimhan. Formal Verification of the Pentium® 4 Floating-Point Multiplier. In
     Proceedings of the conference on Design, automation and test in Europe, DATE ’02, page 20, USA,
     March 2002. IEEE Computer Society.
[41] Daniel Selsam, Percy Liang, and David L. Dill. Developing Bug-Free Machine Learning Systems With
     Formal Mathematics. In Proceedings of the 34th International Conference on Machine Learning, pages
     3047–3056. PMLR, July 2017. ISSN: 2640-3498. URL: https://proceedings.mlr.press/v70/
     selsam17a.html.
[42] John Harrison. Floating-Point Verification Using Theorem Proving. In Marco Bernardo and Alessan-
     dro Cimatti, editors, Formal Methods for Hardware Verification, volume 3965, pages 211–242.
     Springer Berlin Heidelberg, Berlin, Heidelberg, 2006. Series Title: Lecture Notes in Computer Sci-
     ence. URL: http://link.springer.com/10.1007/11757283_8, doi:10.1007/11757283_8.
[43] Anh V. Tran and Yan Wang. Reliable Molecular Dynamics: Uncertainty quantification using interval
     analysis in molecular dynamics simulation. Computational Materials Science, 127:141–160, February
     2017. URL: https://linkinghub.elsevier.com/retrieve/pii/S0927025616305171, doi:
     10.1016/j.commatsci.2016.10.021.
[44] Geoffrey Irving. Conservative Interval Arithmetic in Lean, March 2025. original-date: 2024-05-
     26T10:00:08Z. URL: https://github.com/girving/interval.
[45] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Lan-
     guage. In Automated Deduction – CADE 28, volume 12699, pages 625–635, Cham, 2021. Springer
     International Publishing. URL: https://lean-lang.org/papers/lean4.pdf, doi:10.1007/
     978-3-030-79876-5_37.
                                                                                                    27


[46] David Thrane Christiansen. Functional Programming in Lean. Leanprover Community, 2023. URL:
     https://leanprover.github.io/functional_programming_in_lean/.
[47] Maxwell P. Bobbin, Samiha Sharlin, Parivash Feyzishendi, An Hong Dang, Catherine M. Wraback,
     and Tyler R. Josephson. Formalizing chemical physics using the Lean theorem prover. Digital Dis-
     covery, 3(2):264–280, 2024. URL: https://xlink.rsc.org/?DOI=D3DD00077J, doi:10.1039/
     D3DD00077J.
[48] Joseph Tooby-Smith. HepLean: Digitalising high energy physics, May 2024. arXiv:2405.08863 [hep-
     ph]. URL: http://arxiv.org/abs/2405.08863, doi:10.48550/arXiv.2405.08863.
[49] Tomáš Skřivan. lecopivo/SciLean, April 2025. original-date: 2021-09-27T21:50:10Z. URL: https:
     //github.com/lecopivo/SciLean.
[50] Heather Macbeth. The Mechanics of Proof.        2022.   URL: https://hrmacbeth.github.io/
     math2001/index.html.
[51] Daan Frenkel and Berend Smit. Understanding molecular simulation: from algorithms to applications.
     Number 1 in Computational science series. Academic Press, San Diego, 2nd ed edition, 2002.
[52] Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer. The
     Lean Theorem Prover (System Description). In Amy P. Felty and Aart Middeldorp, editors, Automated
     Deduction - CADE-25, pages 378–388, Cham, 2015. Springer International Publishing. doi:10.
     1007/978-3-319-21401-6_26.
[53] Alex Meiburg and Johan Commelin. ComputableReal: A Lean library for computable real numbers,
     2025. URL: https://github.com/Timeroot/ComputableReal.
[54] Andrew Z. Summers, Justin B. Gilmer, Christopher R. Iacovella, Peter T. Cummings, and Clare
     MCabe. MoSDeF, a Python Framework Enabling Large-Scale Computational Screening of Soft Mat-
     ter: Application to Chemistry-Property Relationships in Lubricating Monolayer Films. Journal of
     Chemical Theory and Computation, 16(3):1779–1793, March 2020. URL: https://pubs.acs.org/
     doi/10.1021/acs.jctc.9b01183, doi:10.1021/acs.jctc.9b01183.
[55] Joseph Tooby-Smith. Formalization of physics index notation in Lean 4, November 2024.
     arXiv:2411.07667 [cs]. URL: http://arxiv.org/abs/2411.07667, doi:10.48550/arXiv.
     2411.07667.
