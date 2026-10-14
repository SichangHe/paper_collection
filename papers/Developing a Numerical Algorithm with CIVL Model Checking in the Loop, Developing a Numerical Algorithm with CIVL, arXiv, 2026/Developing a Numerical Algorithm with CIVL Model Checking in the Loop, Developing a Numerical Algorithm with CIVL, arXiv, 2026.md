                                                  © 2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including
                                            reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any
                                                                                                        copyrighted component of this work in other works.



                                                Developing a Numerical Algorithm with CIVL
                                                        Model Checking in the Loop
                                                          Youngjun Lee                                                  Anshu Dubey                                                 Jan Hückelheim
                                               Argonne National Laboratory                         RIKEN Center for Computational Science                                  Argonne National Laboratory
                                                  Lemont, Illinois, USA                                        Kobe, Japan                                                    Lemont, Illinois, USA
                                                      leey@anl.gov                                         anshu.dubey@riken.jp                                               jhueckelheim@anl.gov



                                            Abstract—Verifying a numerical algorithm in a large scientific                           that surface only for certain inputs or process distributions can
                                         simulation framework is challenging: the framework is too big                               easily slip through. Formal verification, by contrast, promises
arXiv:2609.31964v1 [cs.LO] 25 Sep 2026




                                         to model-check, and the unit tests exercise only sampled inputs.                            exhaustive guarantees, but modern simulation codes are usu-
                                         We report a case study in which we developed a new cloud-
                                         in-cell (CIC) deposition algorithm for Flash-X, a large-scale                               ally surrounded by large, layered frameworks, making it hard
                                         multiphysics simulation framework, keeping the CIVL model                                   to verify an entire application stack in place.
                                         checker in the development loop. Rather than verify the algo-                                  CIVL (Concurrency Intermediate Verification Language) [1]
                                         rithm within Flash-X’s hefty infrastructure, we extract only the                            is a verification framework that combines model checking with
                                         interfaces that the algorithm needs into a small, self-contained C                          symbolic execution, in which inputs are taken as symbolic
                                         model, which abstracts away implementation details of the Flash-
                                         X infrastructure that are unrelated to the new algorithm. The                               values and the feasibility of each execution path, together
                                         new algorithm is then built and checked within this C model. The                            with the assertions placed by the developer, is discharged to
                                         CIVL model checker enables verification of the required physical                            SMT (Satisfiability Modulo Theories) solvers. CIVL provides
                                         properties of the CIC deposition algorithm using symbolic values                            front ends for several concurrency models, including MPI,
                                         for the particle positions. It proves two physical properties—mass                          OpenMP, and CUDA, lowering them to a single intermediate
                                         conservation and the deposition location—for the continuum
                                         of admissible positions in the simulation domain. CIVL also                                 language, and it detects deadlocks, data races, illegal memory
                                         verifies the algorithm’s memory safety and freedom from MPI                                 access, and violations of contracts written by developers.
                                         deadlocks and data race conditions over all rank distributions                              Crucially for numerical code, it can model numerical floating-
                                         within specified bounds. Writing the verifying properties first                             point computations symbolically as real numbers, enabling
                                         and continuously checking them at each stage of the bottom-up                               reasoning over a continuum of input space rather than a single
                                         prototyping workflow turned CIVL into a design guardrail that
                                         greatly increased confidence in the extended algorithm. During                              sampled value. While this model precludes the analysis of
                                         our case study, CIVL surfaced a concurrency defect in the                                   floating-point errors, it is a practical approach to reason about
                                         algorithm that our random-seed-based tests failed to exercise.                              the correctness of parallel algorithms, which are often not
                                         This paper shows our workflow, with the goal of helping readers                             expected to be bitwise exact, for example due to the non-
                                         understand its benefits, cost, and tradeoffs compared with testing.                         associativity of floating-point summation. This design choice
                                            Index Terms—CIVL, Model checking, Formal verification,                                   has allowed CIVL to be applied to production-grade numerical
                                         Particle-in-Cell, Scientific computing, High performance comput-                            frameworks such as PETSc [2].
                                         ing                                                                                            There is a substantial body of work applying formal meth-
                                                                                                                                     ods to message-passing software, mostly concentrated on the
                                                                      I. I NTRODUCTION                                               parallel-communication layer [3]. Dynamic verifiers such as
                                            Numerical simulation software is notoriously difficult to get                            ISP [4] replay a program under carefully chosen schedules
                                         right. A scientific simulation code combines two error-prone                                to expose deadlocks and mismatched communications. MPI-
                                         concerns at once. The numerical algorithm relies on floating-                               SV [5] pairs symbolic execution with model checking to rea-
                                         point operations over a discretized domain, where a subtle bug                              son about MPI programs over symbolic data. Most of this work
                                         in calculating an index, a weight, or a boundary case silently                              focuses on verifying a parallel program already established,
                                         degrades the solution rather than crashing. Also, the paral-                                and the property under test is either communication safety or
                                         lel algorithm distributes the execution over many processes                                 equivalence to a reference serial implementation.
                                         whose interleavings, message orderings, and certain floating-                                  This paper is a case study in using the model checker
                                         point operations such as summation depend on the process                                    as a design-time instrument, not only as a post-hoc verifier.
                                         counts, schedules, and system-specific or nondeterministic                                  We develop a new particle deposition algorithm intended for
                                         effects. Conventional test suites address both concerns only by                             Flash-X, a large multiphysics simulation framework, keeping
                                         sampling: a test fixes concrete inputs and observes a handful                               CIVL in the development loop from the outset. We build
                                         of executions so that it can cover neither the continuum of                                 and verify the algorithm in a compact, self-contained model
                                         admissible numerical inputs nor the combinatorial space of                                  that abstracts the surrounding frameworks of Flash-X. We use
                                         parallel schedules and process counts. Consequently, defects                                CIVL not only to certify a finished implementation, but to
guide the algorithm’s design by defining correctness properties
before the code exists, and re-establishing them at each stage
of bottom-up prototyping. We report the detailed workflow that
we applied, a concurrency defect exposed by this workflow,
and the costs of CIVL model checking in this process.

                      II. BACKGROUND
A. Flash-X
   Flash-X [6] is a composable, multiphysics simulation code
used in a wide range of scientific domains, enabling users to
construct simulations by combining available physics units in
Flash-X. Most of the physics solvers in Flash-X are based on       Fig. 1. A close look at uneven cloud deposition at a fine-coarse boundary,
the Eulerian method, which assumes a block-structured Adap-        caused by the reverse-guard-cell-fill-based method
tive Mesh Refinement (AMR) grid; however, some physics
units are based on the Lagrangian method. The two differ
in how they represent matter: Eulerian methods discretize it       B. Particle-in-Cell Algorithm
as field values on a mesh or grid, while Lagrangian meth-             In a particle-in-cell (PIC) method, Lagrangian particles
ods represent it as moving parcels at continuous positions         move through the Eulerian grid, and the two representations
anywhere in space, such as particles, free of a grid. This         are coupled in each simulation time step: grid quantities
coexistence poses a challenge in ensuring physical consistency     are mapped through interpolation, and particle quantities are
between the two different pictures of physics modeling. For        deposited back onto the grid. A common deposition scheme
example, if a simulation is configured to solve the dynamics       is the cloud-in-cell (CIC) method [7], where each particle is
of free particles on the AMR grid, the physical quantities         considered a cloud of finite extent, and its quantities are dis-
carried by the particles (e.g., mass, charge) should update        tributed across the surrounding cells with weights proportional
the corresponding physical quantities in the grid (e.g., mass      to overlap. Therefore, particle deposition is performed on a
density, charge density) to be consistent with the other physics   small, multidimensional stencil, rather than on a single cell.
solvers.                                                           This paper concerns the CIC deposition scheme in Flash-X.
   The AMR grid in Flash-X is organized as a forest of                When a particle sits near a block boundary, its CIC stencil
blocks: the domain is decomposed into logically Cartesian          straddles multiple blocks, so its block-local deposition con-
blocks, each of which holds a fixed number of interior cells       tributes to its guard cell regions. Unlike other stencil-based
surrounded by a halo of guard cells. The guard cells hold          algorithms in Flash-X, where guard cell data is acted upon as
copies of data owned by neighboring blocks, so the stencil-        temporary copies of neighbor data and then discarded, CIC
based physics solvers can be performed block-locally, without      deposition writes into the guard cells; those updates carry
communicating with blocks that different MPI processors may        the deposited quantity that belongs to neighboring blocks and
own. Flash-X assumes octree-based AMR, where a block is            must be folded back into their interior cells. In the classical
recursively bisected in every dimension into 2d child blocks       scheme used by FLASH [8], a predecessor of Flash-X, the
when a finer resolution is needed. Flash-X’s Grid unit handles     particle deposits a CIC stencil on its block, then applies a
refinement and derefinement (coarsening) of blocks, along          so-called reverse guard cell fill process to transfer guard cell
with the data prolongation and restriction between levels, dur-    data back into interior cells in the neighboring blocks. This
ing the simulation runtime; hence, the number of blocks and        works; however, reverse guard cell fill poses two issues. One is
their topology are undefined before the simulation. Flash-X’s      that the operation is global and communication-heavy, which
physics units apply their numerical algorithm in one block         makes it inefficient. However, it is the second issue that is
of the AMR grid, considering a block as the finest data-           a greater concern. When a particle is located on a finer cell
abstraction unit provided by Flash-X’s Grid infrastructure.        adjacent to a coarser cell, the CIC mapping gets asymmetric,
   This infrastructure is the core idea of making Flash-X a        as demonstrated in Figure 1. This is because on the fine
productive, modular, multiphysics simulation framework, but        side the guard cell is only half the size of the coarse cell.
also makes it difficult to verify the algorithms formally. The     During reverse guard cell fill, a prolongation step is applied
Grid unit and its guard-cell exchanges are written in ap-          on the coarse side, and the deposition occurs on an area that
proximately 150k lines of Fortran code with intricate parallel     is 2d times as big as the original deposition, where d is the
communication, so verifying a new algorithm in place would         dimension of the grid. This changes the shape of the deposited
mean exploring every code path in the entire stack. Crucially,     cloud and can introduce spurious forces.
however, checking the physical correctness of an algorithm            To avoid the spurious forces, we developed an alternative
does not require verifying the internal implementation of          deposition scheme based on virtual particles [9] that replaces
Flash-X’s Grid unit—it requires only that the algorithm uses       the reverse guard cell fill with virtual particle migration. When
the Grid unit’s APIs correctly.                                    a particle’s CIC stencil straddles the guard cell regions, we
emit one virtual particle per neighboring block the stencil                                                    Block 5       Block 6
touches, each of which carries the depositing quantity and                                                               3
a position expressed in its destination block’s frame. Virtual
particles are then migrated to the MPI ranks that own their des-                                                                           4
tination blocks. After the migration, every particle—including                                                 Block 3       Block 4
real and virtual particles—can be deposited entirely locally
in its owning block, and any deposition in the guard cell
region is discarded. Once the deposition is done, the virtual                                                                          2
                                                                              Block 2
particles are destroyed. The new algorithm also has the virtue                                             1
of completely eliminating the additional communication step
required for reverse guard cell fill. At every timestep, there
is a necessary communication step to migrate the particles to
their new destination as a result of their physical displacement
during evolution. We create and populate virtual particles prior
to this migration so that one communication step serves both
goals—getting the particles to the right place and ensuring
                                                                              Block 0                          Block 1
correct deposition at processor boundaries.
   In the generation of virtual particles, two families of edge
                                                                     Fig. 2. An example AMR grid with periodic boundary conditions for all axes,
cases must be handled:                                               with four particles. Each particle’s CIC stencils are highlighted in each color.
  1) Domain boundary condition: when a virtual parti-                All blocks have 4 × 4 cells, but have two different refinement levels.
     cle is generated at a domain boundary, the boundary
     conditions are resolved at generation time—a periodic
                                                                     q (e.g., mass or charge), of which D deposits q’s density, ρk ,
     edge shifts the deposit position by the domain width,
                                                                     in cell k, whose center is ck and volume is ∆Vk . Then,
     a reflecting edge mirrors it about the boundary, and an
                                                                                            X
     outflow edge drops the out-of-domain virtual particle.                                      ρk ∆Vk = q,                    (1)
  2) Fine-coarse interface: when a virtual particle is gener-
     ated at an interface between blocks at different refine-                                  Xk
                                                                                                ck ρk ∆Vk = q p.                                 (2)
     ment levels, the physical size of its CIC stencil must
                                                                                                k
     be consistent across the interface—it is resolved at the
     coarsest refinement level that the CIC stencil touches. If      Equation (1) ensures conservation: the deposited quantity
     a real particle sits in a coarser block, the virtual particle   integrated over the grid equals the quantity carried by the
     sent to a finer neighbor is spread over 2d finer cells (e.g.,   particle, so the operations in D neither create nor destroy the
     Figure 2, Particle 1); if the real particle sits in a finer     physical quantity. Equation (2) checks the deposition location:
     block, its stencil is coarsened to the neighbor’s level         the first moment (e.g., center of mass) of the deposited field
     (e.g., Figure 2, Particle 2).                                   equals the particle’s position, so the deposited quantity lands
                                                                     in the correct location. The two conditions are independent
In Figure 2, for example, the CIC stencils of four particles are
                                                                     of each other—e.g., if the quantity is conserved over Ω but
illustrated in an AMR grid with periodic boundary conditions.
                                                                     deposited in the wrong place—thus, Equation (2) is what
Particle 1 is placed in a block boundary that jumps the
                                                                     catches a misplaced stencil, a wrong destination block, or an
refinement level. Three virtual particles are generated and
                                                                     incorrect refinement resolution, none of which Equation (1)
transferred to Blocks 1, 2, and 3. The virtual particle in Block
                                                                     alone would detect.
3 needs to be deposited into four cells instead of one, as
                                                                        Both identities should hold for every admissible position
the real particle’s and the virtual particle’s refinement levels
                                                                     p ∈ Ω 1 , and under every possible grid configuration that
differ. Particle 2 shares a similar circumstance, but the virtual
                                                                     algorithm D should handle. However, the admissible positions,
particle’s refinement level is coarser. In this case, the real
                                                                     p, form a continuum, and the possible AMR geometry layered
particle’s stencil is extended to match the stencil size from
                                                                     on top of it leads to a large number of corner cases that are
the coarser block. Particle 3 lies in a block interior, and its
                                                                     difficult to exhaustively explore with a conventional test suite.
stencil is entirely within one block; thus, no virtual particle is
                                                                     Additional complications arise because the usual Flash-X test
generated—the common case. Particle 4’s stencil spills to the
                                                                     mechanism compares against previously validated baselines,
domain’s periodic boundary; so, its virtual particle is generated
                                                                     but this test practice does not help for algorithmic changes
in Block 2.
                                                                     that intentionally change the solution, for example to increase
   Regardless of the AMR geometric complications, a correct          fidelity, as is the case here. This is what makes the algorithm a
deposition must satisfy two physical conditions. Let D denote        natural target for model checking: rather than sample particles’
the full pipeline under test—virtual particle generation, inter-
rank migration, and fine-coarse resolution—and let a particle          1 Strictly speaking, Equation (2) holds in the domain interior, away from the
at position p in the simulation domain Ω carry a scalar quantity     boundaries where a boundary condition intentionally relocates the quantity.
positions, we treat them as symbolic real values and let CIVL       approach to a modular verification of other parts of Flash-X,
prove both conditions by exhaustively exploring all possible        for example by using a spec-stub approach as in [2].
branches and message interleavings within bounds.
                                                                    B. Symbolic Driver
                         III. M ETHOD                                  Listing 1 shows the CIVL driver, symbolically checking
   Our goal is to verify the deposition algorithm before it         the correctness of the target algorithm. It declares the particle
is ported into Flash-X, to isolate the algorithm under test         position as a symbolic real input, $input, constrains it to the
from Flash-X’s infrastructure. The Flash-X framework is too         domain with $assume, runs the full pipeline, and checks the
large to model-check, and the algorithm to test does not            conservation and deposition location with $assert. Since
exist inside it; thus, we reproduce only what the algorithm         CIVL interprets the double type as real numbers, this single
needs, i.e., APIs required to be called by the algorithm. We        run establishes physical identities Equations (1) and (2) for
apply two levels of abstraction to achieve this: a physical         the entire continuum of physical domain positions, not the
abstraction replaces Flash-X with a small, self-contained C         finitely many sets of positions that a regular test may handle.
model of the deposition pipeline, D, and a logical abstraction      The grid topology and the MPI rank counts, by contrast, are
replaces the Grid infrastructure that the model calls with a        concretized and intentionally small. Axiomatizing the AMR
simplified grid model. A CIVL driver then runs the model with       grid topology leads to rapid growth in model checking time
a symbolic particle position and asserts two physical identities    and requires further optimizations to work within a feasible
of Equations (1) and (2) over the entire space of admissible        timeframe, and is left to future work.
positions.                                                             The driver deposits a single particle, which is sufficient
   Despite Flash-X being written in Fortran, we chose C as          for the physical identities we are testing. Both Equations (1)
the language for the abstraction layers, as CIVL’s support for      and (2) are additive across particles, so proving them for one
C is more mature. Because CIVL has Fortran support [10],            particle at a symbolic position establishes them for any super-
we plan to migrate our approach to Fortran in future work to        position of particles by linearity. However, the single particle
allow easier re-use across Flash-X components.                      case does not exercise the algorithm’s behavior that scales with
                                                                    the particle count. For example, whether a buffer size that is
A. Abstraction Layers                                               correct for one particle stays correct for many particle cases, or
   We develop the algorithm as standalone C code that models        the order in which many particle contributions accumulate in
the full pipeline of D—particle data structures, virtual particle   a single cell. However, these aspects can be tested reasonably
generations, collective MPI migration, and block-local particle     well with our conventional test suites.
deposit—outside of Flash-X. The CIC method implemented in
the C model reflects the full logic and algorithm, so it enables    C. Model Checking in the Loop
us and CIVL to focus on the physical algorithm and its correct-        The abstraction layers and the symbolic model check-
ness without exploring the surrounding framework. Because           ing driver with the correctness properties described in
the target application, Flash-X, runs on distributed nodes, the     Sections III-A and III-B are used not only as a post-
C model uses the same collective MPI communications.                implementation verifier, but also as a tool in the development
   The only Flash-X infrastructure the algorithm depends on         process. We first write the correctness properties that the target
is the grid, which it reaches through a small public API: find      algorithm must adhere to, so that “correct” is defined before
the block containing a physical position, query the block’s         the algorithm code exists, similar to test-driven development.
metadata (e.g., refinement level or owning process), and iterate    Conventional test suites can also coexist alongside it. Still, the
over the block’s data. We implement only that subset of Grid        CIVL driver provides two additional correctness checks that
APIs in about 400 lines of C code that reproduces Flash-X           test suites cannot: CIVL proves the correctness properties over
Grid unit’s observable behavior. Although each of the APIs          the continuous space, and it checks the model defects such
in the simplified grid has a fully functioning implementation,      as out-of-bounds access, invalid pointers, and MPI deadlocks
none of them has the production machinery, such as Morton-          and race conditions. The algorithm is then developed to satisfy
curve indexing or distribution lookup; they only contain a          them, with the properties as formal contracts that CIVL checks
simplified algorithm that needs to be carried out to check the      at every iteration of development. It proves whether the current
CIC algorithm. For example, finding a corresponding block’s         version is correct on the predefined properties, or returns a
ID with a given physical coordinate is required for building the    counterexample that fails.
CIC algorithm, as the block ID is used for dereferencing the           We applied this process to build and design the CIC
data array to be updated by the algorithm. Leaving the block        algorithm for Flash-X. We first established the CIVL driver
ID as a symbolic representation cannot supply the concrete          in Listing 1, then created the simplified grid as an abstraction
value for an array index, so an actual implementation is            layer. To develop the complete algorithm, we proceeded in four
needed.                                                             stages of increasing complexity: a uniform, single-level one-
   This approach allows verification of the algorithm in isola-     dimensional grid on one rank; then cross-rank in the same grid;
tion, while implicitly assuming correctness of the underlying       then two-dimensions; and finally multi-level AMR. Because
grid data structure. Future work could consider extending this      all stages share the same correctness properties encoded in the
     Listing 1. A CIVL driver for the deposition pipeline: a symbolic particle                                  Abstraction Layers
     position ($input), constrained by $assume, checked with $assert for
     Equations (1) and (2).
                                                                                              refine            Write correctness
 1    $input double pos[MDIM]; // symbolic particle position
 2
                                                                                                           properties as a CIVL driver
 3    int main(int argc, char **argv) {
 4      MPI_Init(&argc, &argv);
 5                                                                                                            Implement / extend the
 6        // Initialize a fixed AMR grid                                                                  algorithm for the current stage
 7        // Refinement topology is determined by refine_* args
 8        grid_initStaticAMR(MPI_COMM_WORLD, nb, lo, hi, bc_lo, bc_hi,
 9           refine_levels, refine_coords, n_refine);
10
11        // Constrain the symbolic position to the domain, p ∈ Ω.
12        double p[MDIM];
                                                                                                       failed     CIVL Model
13        for (int a = 0; a < NDIM; ++a) {                                                                         Checking
14          $assume(pos[a] >= lo[a] && pos[a] <= hi[a]);
15          p[a] = pos[a];
16        }                                                                                                                proved
17                                                                                                                                     no:
18        // Initialize one unit-mass particle
19        particle_t r = make_real(p, /*mass=*/1.0);                                                                Algorithm       next stage
20        // Run the full pipeline under test, D                                                                    complete?
21        int n_reals = rank_owns(p) ? 1 : 0;
22        particles_deposit(&r, n_reals);
23                                                                                                                         yes
24        // Equation (1): total deposited mass == input mass
25        $assert(deposited_mass() == 1.0);                                                                Port to the main application
26
27        // Equation (2): first moment == p, interior only
28        double mom[MDIM];                                                      Fig. 3. CIVL-in-the-loop development: each development stage is proved
29        deposited_moment(mom);
30        for (int a = 0; a < NDIM; ++a)
                                                                                 through CIVL.
31          if (interior(p, a))
32            $assert(mom[a] == p[a]);
33
34        grid_finalize();
35        MPI_Finalize();                                                        location, Equation (2), holds for all positions in the interior
36    }                                                                          of the grid. In the same runs, CIVL establishes memory
                                                                                 safety (e.g., out-of-bounds or invalid pointer dereference) and
                                                                                 freedom from MPI deadlocks and data races, over all particle
     CIVL driver, we re-apply CIVL with the same specification                   placements at each rank count. We developed the algorithm
     at every stage, extending the algorithm incrementally from a                pipeline from the simplest case, a 1D uniform grid with one
     foundation that has already been proved in the previous stage.              MPI rank, progressively extended to 2D AMR with multiple
     This workflow helped isolate the counterexample found by                    ranks, and CIVL verified the correctness at each stage. We
     CIVL as an implication of the added code in the current stage.              verified the pipeline on two AMR configurations: two-level
        Figure 3 represents the flowchart described in this section:             and three-level, both in 1D and 2D with multiple MPI ranks.
     establish the correctness properties and build the abstraction              Runtime and scaling for these CIVL model checks are reported
     layers, then develop the algorithm with CIVL in the loop in                 in Section V.
     each stage. CIVL’s check failure usually locates the incorrect-                CIVL model checking also exposed a defect in the pipeline
     ness of the algorithm in the current stage, but rarely indicates            that our conventional tests had not triggered. A rank that owns
     that the correctness property should be updated/refined. In                 no real particles can still receive virtual particles if neighboring
     our case, for example, the deposition location identity, Equa-              ranks have real particles near the block boundaries. The receive
     tion (2), does not hold near the domain boundary under non-                 buffer was sized based on each rank’s local real particle counts
     outflow conditions, as the deposited quantity is intentionally              with a max_total < 1 clamp, so the receive buffer would
     relocated. We found this during the development process and                 have only one slot if there is no real particle in the rank.
     updated our CIVL driver to constrain the deposition location                One slot is enough to receive one virtual particle; however,
     check only when the particle is placed away from the domain                 receiving two or more virtual particles is a reachable state,
     boundary.                                                                   as the neighboring ranks can have many real particles that
        The value of the loop is the confidence at each stage of the             spill virtual particles. This is also a reachable state in our
     development. It proves correctness properties and searches for              CIVL driver, even though it has only one particle in the
     model defects over the whole input space, helping developers                simulation domain. If a particle generates multiple virtuals,
     design and extend the algorithm stage by stage.                             then each of them is transferred to the destination blocks, and
                                                                                 they can be co-located in the same rank. A rank that owns
                      IV. R ESULTS AND D ISCUSSION                               multiple blocks may require more than one particle slot for
        Following the workflow of Section III-C, we designed and                 the receive buffer, even though it has no real particle. Our
     developed the CIC particle deposition pipeline on the simpli-               test suites did not capture this corner case, as they initialize
     fied grid. CIVL proves the conservation, Equation (1), for all              about a hundred random particles with a random seed, so
     particle positions in the grid domain, Ω, and the deposition                every rank owned at least one real particle and the empty-
    Listing 2. The fix CIVL prompted: size the receive buffer from the global                                    TABLE I
    particle count, so a rank with no local reals is not under-allocated (V = max                   CIVL STATS ON TWO - LEVEL AMR GRID
    virtuals per real).
                                                                                     Config   Time (s)   States States saved Transitions Prover calls Mem (GB)
1     int particles_maxPoolSize(int n_reals) {
2    - int max_total = n_reals * grid_getNumProcs() * (1 + V);                       1D × 1    10.34    16,008    25,276    21,627            547        1.13
3    + int global = n_reals;                                                         1D × 2    12.72    27,411    43,264    41,644            526        3.40
4    + MPI_Allreduce(&n_reals, &global, 1, MPI_INT, MPI_SUM, comm);                  1D × 3    17.85    39,063    61,621    61,654            540        3.31
5    + int max_total = global * (1 + V);
                                                                                     2D × 1 1,063.35 915,753 1,481,838 1,108,136           34,434        4.50
6       if (max_total < 1) max_total = 1;
                                                                                     2D × 2 1,713.58 1,176,850 1,891,732 1,540,286         33,213        5.82
7       return max_total;
8     }

                                                                                                                 TABLE II
                                                                                                   CIVL STATS ON THREE - LEVEL AMR GRID
    rank case was never reached. The CIVL driver, by contrast,
    exercises one particle over all positions and reaches this corner                Config   Time (s)   States States saved Transitions Prover calls Mem (GB)

    case, returning a concrete counterexample. The defect would                      1D × 1    11.53    25,073    39,852    33,238            756        1.12
                                                                                     1D × 2    16.41    40,631    64,146    59,940            741        3.31
    corrupt memory silently instead of crashing. The subsequent                      1D × 3    23.28    57,320    90,530    88,347            724        3.24
    communication step appends each received particle to the                         2D × 1 1,909.89 1,771,007 2,871,930 2,121,203         53,978        3.54
                                                                                     2D × 2 2,978.64 2,190,454 3,519,344 2,786,977         52,089        6.48
    local pool without a bounds check, so an under-allocated pool
    is an out-of-bounds heap write. Consequently, the resulting
    symptom would be a silent wrong deposition rather than an
    abort. CIVL reports it deterministically as an out-of-bounds                    transitions, and prover calls grow by roughly 50–60× in
    violation, without needing the fault to occur at runtime. We                    the two-level AMR grid, as the symbolic particle position
    sized the buffer from the global particle count to fix this defect,             explored a larger stencil on more cells/blocks. The runtime
    as represented in Listing 2.                                                    grows faster, roughly 100×, which indicates the individual
       In summary, the CIVL-in-the-loop procedure demonstrated                      solver queries also become harder. We observed that two-
    its benefits in the practical example: developing the CIC                       dimensional configurations require a slightly longer timeout
    deposition algorithm for Flash-X. It acted as a guardrail for                   for the SMT solver in CIVL. Refinement depth compounds
    a bottom-up prototyping strategy and also surfaced an algo-                     the cost of CIVL model checking. For 2D configurations, the
    rithmic defect. These guarantees, however, hold only for the                    three-level AMR grid nearly doubles the runtime and states
    bounded model we check; the grid configuration that the CIVL                    compared to the two-level grid, whereas it requires about a
    verifies is fixed in the driver (e.g., grid_initStaticAMR                       40– 50% states increase and about 10–30% more runtime in
    call in Listing 1), so it checks only one AMR topology at                       1D configurations. On the other hand, we found that extending
    a time. In a real case in Flash-X simulation, the AMR grid                      the number of MPI ranks is comparatively moderate, under 2×
    progressively refines and derefines blocks during runtime,                      across the rank counts we tested.
    so the algorithm should be tested on a large number of                             The runtime cost of 1D and 2D runs decides where CIVL
    possible AMR grid configurations. We used a finite number of                    sits in the development loop. The 1D runs are fast enough
    grid configurations for our CIVL driver, and its runtime and                    to wait on after an edit, similar to compilation and unit test
    scalability will be discussed in Section V.                                     runs, and we used them that way throughout development.
                                                                                    The 2D runs, however, are too expensive to run after every
                       V. C OSTS AND L IMITATIONS                                   small code edit, so we occasionally launched them on major
       Tables I and II report the cost of the CIVL runs we used, for                code changes. Consequently, most iteration in the workflow
    the two- and three-level AMR grids, respectively. The Config                    of Section III-C happens in 1D, with the 2D configurations
    column describes the grid dimensionality and the number of                      serving as a checkpoint at the end of each stage.
    MPI ranks. For instance, 2D × 2 denotes a 2D grid, and its                         As shown in the CIVL runtime tables, even a single-rank
    blocks are distributed over two MPI ranks. Time and Mem are                     2D AMR configuration is already expensive, and this is the
    wall-clock time and peak memory used during CIVL model                          main reason to fix the grid topology in the driver rather
    checking. States is the number of distinct program states CIVL                  than expressing the grid abstraction unit in symbolic repre-
    explored: the size of the reachable state space it searched;                    sentations. Expressing the AMR grid topology with symbolic
    States saved is the number of states it stored during the depth-                values or verifying the algorithm for three spatial dimensions
    first search for backtracking and revisit detection. Transitions                is therefore left for future work.
    represents the number of state-to-state execution steps, and                       The guarantees we obtain are relative to the fidelity of the
    Prover calls is the number of queries dispatched to the external                abstractions we used, which is an important limitation of this
    SMT solver.                                                                     approach. We verified the algorithm on a self-contained ab-
       The tables show a steep cost of grid dimensionality. In                      stracted model, rather than on the target application, Flash-X.
    one dimension, every configuration completes in about twenty                    Therefore, transferring the resulting algorithm to Flash-X rests
    seconds with several hundred prover calls, which is cheap                       on two assumptions. First, the simplified grid must reliably
    enough to run within development iterations. However, it                        reproduce the observable behavior of the Flash-X Grid APIs
    is far more expensive in two-dimensional cases. The states,                     that the algorithm calls. We limit this exposure by modeling
only the small subset of well-defined public APIs in simplified     design guardrail. At each stage of development, the algorithm
algorithms/implementations, rather than reimplementing the          was extended from the foundation already proven through
full functionality the Flash-X Grid unit provides. Second, the      CIVL, and CIVL surfaced the concurrency defect that our con-
algorithm is checked in C, but the target application is written    ventional test suites failed to exercise. The computational cost
in Fortran. Reconstructing the properties in the ported code        for the CIVL model checking is modest in one-dimensional
is required to close the gap, and it is on our roadmap. Even        cases, but considerably more expensive in two-dimensional
before that port, however, verifying the model pays off: it pins    cases. The abstraction layers developed during the workflow
the design of the algorithm and verifies that it is correct on an   are reusable components for future Flash-X development, so
AMR grid. Thus, porting the abstraction layers and algorithm        the model-checking-in-the-loop procedure can be applied to
to Fortran begins from a design that has already proved correct,    other new physics solver development.
eventually simplifying the algorithm integration to Flash-X.           Yet, several directions remain to strengthen the workflow.
   It is worth noting that establishing and building the abstrac-   First, the CIVL driver fixes the AMR grid topology and
tion layers is a small one-time cost. The simplified grid model     checks only one AMR configuration at a time. Expressing
that we used as an abstraction layer is about 400 lines of C        the topology itself with symbolic values would enable CIVL
code, and the CIVL driver adds about 150 lines of code. More        to verify the target algorithm over all admissible grid con-
importantly, most of the effort is reusable. The grid abstraction   figurations; however, as Section V shows, this multiplies an
reproduces most of the Flash-X Grid API that any Flash-X            already non-trivial state space search, which makes it imprac-
physics unit calls, so it is a reusable component and testbed       tical. Additional abstractions and state-reduction techniques
for a new Flash-X physics solver, bringing CIVL into the            are required. Second, we plan to port the abstraction layers
design and development workflow. Developing another physics         and the current algorithm implementation to Fortran, the main
solver in Flash-X would reuse the same grid model and the           language of Flash-X. We used C to leverage the most mature
same workflow, rewriting only the algorithm’s pipeline and its      support from CIVL, but as reported in [10], CIVL already
correctness properties. Therefore, the cost of developing the       has Fortran support. As we port our C abstraction layers to
abstraction layers is amortized not only across the stages of       Fortran, we expect to improve and expand CIVL’s Fortran ca-
one algorithm but across future algorithms as well.                 pability, which we hope will help the community in verifying
   Keeping the grid abstraction aligned with Flash-X, however,      Fortran code. Additionally, the Fortran abstraction layer will
is a continuing obligation rather than a one-time cost. Nothing     be more proximate to Flash-X, and we will eventually port the
automatically checks and verifies the observable behaviors          algorithm to Flash-X.
of the simplified grid model, since the model and Flash-X
are separate codebases. We consider this an acceptable trade-                              ACKNOWLEDGMENT
off to make model checking feasible, since the maintenance            This material is based upon work supported by the U.S.
cost follows the handful of Grid APIs needed for physics            National Science Foundation under Award Number CCF-
algorithms under test, not 150k lines of code from the Flash-X      2446130, and by the U.S. Department of Energy, Office of
Grid unit implementation.                                           Science, Advanced Scientific Computing Research (ASCR)
           VI. C ONCLUSION AND F UTURE W ORK                        Program, under Award Number DE-SC0025953.
                                                                       This report was prepared as an account of work sponsored by an
   We presented a case study on developing a new numerical          agency of the United States Government. Neither the United States
algorithm (the CIC deposition scheme based on the virtual par-      Government nor any agency thereof, nor any of their employees,
ticle concept) for Flash-X, keeping the CIVL model checker          makes any warranty, express or implied, or assumes any legal liability
in the loop. Instead of verifying the algorithm inside Flash-X’s    or responsibility for the accuracy, completeness, or usefulness of any
large infrastructure, which is impractical to model-check, we       information, apparatus, product, or process disclosed, or represents
introduced abstraction layers that reproduce a small subset of      that its use would not infringe privately owned rights. Reference
the Flash-X framework with minimal implementation. On top           herein to any specific commercial product, process, or service by trade
of the abstraction layers, the target algorithm is implemented      name, trademark, manufacturer, or otherwise does not necessarily
as a small, self-contained C program, enabling the CIVL             constitute or imply its endorsement, recommendation, or favoring by
model checker to exercise the required physical properties          the United States Government or any agency thereof. The views and
with symbolic values. Treating the particle position as a           opinions of authors expressed herein do not necessarily state or reflect
symbolic real value, CIVL proved mass conservation and the          those of the United States Government or any agency thereof.
first moment of the deposited field over the continuum of
particle positions in the simulation domain. Additionally, it                                  R EFERENCES
checked memory safety and absence of MPI deadlocks and
                                                                     [1] S. F. Siegel, M. Zheng, Z. Luo, T. K. Zirkel, A. V. Marianiello,
race conditions across the multiple-rank distribution we tested.         J. G. Edenhofner, M. B. Dwyer, and M. S. Rogers, “CIVL:
   The core of the methodology is writing the correctness                the concurrency intermediate verification language,” in Proceedings
properties in CIVL before the algorithm and continuously                 of the International Conference for High Performance Computing,
                                                                         Networking, Storage and Analysis. New York, NY, USA: Association
checking them at every stage of a bottom-up prototyping                  for Computing Machinery, 2015, pp. 1–12. [Online]. Available:
workflow. This turned CIVL from a post-hoc verifier into a               https://doi.org/10.1145/2807591.2807635
 [2] V. Dhavala, J. Hückelheim, P. D. Hovland, and S. F. Siegel,
     “Verifying PETSc vector components using CIVL,” in Computer Aided
     Verification. Cham, Switzerland: Springer Nature, 2025, pp. 148–161.
     [Online]. Available: https://doi.org/10.1007/978-3-031-98668-0 7
 [3] G. Gopalakrishnan, R. M. Kirby, S. Siegel, R. Thakur, W. Gropp,
     E. Lusk, B. R. De Supinski, M. Schulz, and G. Bronevetsky,
     “Formal analysis of MPI-based parallel programs,” Communications
     of the ACM, vol. 54, no. 12, pp. 82–91, 2011. [Online]. Available:
     https://doi.org/10.1145/2043174.2043194
 [4] S. S. Vakkalanka, S. Sharma, G. Gopalakrishnan, and R. M. Kirby,
     “ISP: a tool for model checking MPI programs,” in Proceedings of the
     13th ACM SIGPLAN Symposium on Principles and Practice of Parallel
     Programming, ser. PPoPP ’08. New York, NY, USA: Association
     for Computing Machinery, 2008, p. 285–286. [Online]. Available:
     https://doi.org/10.1145/1345206.1345258
 [5] Z. Chen, H. Yu, X. Fu, and J. Wang, “MPI-SV: a symbolic
     verifier for MPI programs,” in Proceedings of the ACM/IEEE
     42nd International Conference on Software Engineering: Companion
     Proceedings, ser. ICSE ’20. New York, NY, USA: Association
     for Computing Machinery, 2020, p. 93–96. [Online]. Available:
     https://doi.org/10.1145/3377812.3382144
 [6] A. Dubey, K. Weide, J. O’Neal, A. Dhruv, S. Couch, J. A. Harris,
     T. Klosterman, R. Jain, J. Rudi, B. Messer et al., “Flash-X, a
     multiphysics simulation software instrument,” SoftwareX, vol. 19, p.
     101168, 2022. [Online]. Available: https://doi.org/10.1016/j.softx.2022.
     101168
 [7] R. W. Hockney and J. W. Eastwood, Computer Simulation Using
     Particles. Boca Raton, FL, USA: CRC Press, 1988. [Online].
     Available: https://doi.org/10.1201/9780367806934
 [8] B. Fryxell, K. Olson, P. Ricker, F. X. Timmes, M. Zingale, D. Lamb,
     P. MacNeice, R. Rosner, J. Truran, and H. Tufo, “FLASH: An adaptive
     mesh hydrodynamics code for modeling astrophysical thermonuclear
     flashes,” The Astrophysical Journal Supplement Series, vol. 131, no. 1,
     pp. 273–334, 2000. [Online]. Available: https://doi.org/10.1086/317361
 [9] A. Dubey and A. Dhruv, “Adding new capability in existing scientific
     application with LLM assistance,” arXiv:2511.00087 [cs.SE], 2025.
     [Online]. Available: https://doi.org/10.48550/arXiv.2511.00087
[10] W. Wu, J. Hückelheim, P. D. Hovland, and S. F. Siegel, “Verifying
     Fortran programs with CIVL,” in Tools and Algorithms for the
     Construction and Analysis of Systems: 28th International Conference,
     TACAS 2022, Held as Part of the European Joint Conferences on
     Theory and Practice of Software, ETAPS 2022, Munich, Germany,
     April 2–7, 2022, Proceedings, Part I. Berlin, Heidelberg: Springer-
     Verlag, 2022, p. 106–124. [Online]. Available: https://doi.org/10.1007/
     978-3-030-99524-9 6
