                                                 Machine-Checked Certificates for the Geometric Half
                                                      of the Minimum Kochen–Specker Bound
                                                                     Shayaan Siddique            Ibrahim Mian
                                                                          Millennium Research
                                                                 {shayaan,ibby}@millenniumresearch.ai
                                                          shayaansiddique02@gmail.com, ibrahimnmian@gmail.com


                                                                                      Abstract
                                                  The best known lower bound for the minimum Kochen–Specker vector system in R3 —
                                              24 vectors—rests on a computational proof whose combinatorial half emits DRAT proofs
                                              but whose geometric half does not: the non-embeddability of thousands of candidate
                                              graphs is established by Z3’s nonlinear real arithmetic, which produces no checkable proof
arXiv:2607.26413v1 [cs.LO] 29 Jul 2026




                                              objects. We close this gap for the proof’s blocking database. We introduce exact rational
                                              case-tree certificates of real non-embeddability, whose splits are polynomial factorizations
                                              and rational sum-of-squares decompositions and whose leaves are discharged by injectivity,
                                              ideal-membership, or Positivstellensatz-shaped positivity arguments, and we certify all
                                              291 source lines (180 distinct graphs) of the published pipeline’s order-10–13 blocking
                                              lists. Certificates are replayed by two independent checkers that share no code with the
                                              generator: a pure-Python replay over exact fractions, and a total checker implemented and
                                              proved sound in Lean 4. The soundness theorem—acceptance implies that no injective-on-
                                              rays, orthogonality-respecting assignment of nonzero real vectors realizes the graph—is
                                              kernel-checked with axiom closure {propext, Classical.choice, Quot.sound}, and a
                                              gcd-free rational arithmetic layer makes the entire verdict computation kernel-reducible,
                                              so each per-graph non-embeddability result is a closed kernel theorem proved by decide.
                                              The formalization surfaced findings about the published pipeline, including a load-bearing
                                              injectivity side condition in its embeddability notion, hidden WLOG case obligations
                                              invisible to Z3-based workflows, and an unreproducible candidate count that we resolve
                                              against the published artifacts. All certificates, checkers, and proofs are available and
                                              replayable from a single build.


                                         1    Introduction
                                         A Kochen–Specker (KS) vector system in R3 is a finite set of nonzero vectors, pairwise distinct
                                         as rays, that admits no {0, 1}-coloring in which every orthogonal pair contains at most one 1
                                         and every orthogonal triad contains exactly one 1. Such systems witness the Kochen–Specker
                                         theorem [9], a cornerstone of quantum foundations ruling out noncontextual hidden-variable
                                         models, and the size of the smallest such system is a long-standing open problem: the best
                                         construction has 31 vectors, and the best lower bound, established computationally by Li et
                                         al. [12] and Kirchweger et al. [8], is 24.
                                              The published lower-bound proof has two halves. The combinatorial half is an isomorph-
                                         free SAT enumeration of candidate graphs up to order 23; its unsatisfiability results emit
                                         DRAT proofs checkable by drat-trim [15]. The geometric half must show that every enumer-
                                         ated candidate graph is non-embeddable in R3 —that no assignment of nonzero, pairwise-ray-
                                         distinct vectors realizes its edges as orthogonalities. This half is established by Z3’s nonlinear
                                         real arithmetic solver [4], which produces no proof objects: the trust chain for the geometric
                                         half of the bound terminates in an unverified decision procedure for a ∃R-hard theory. The


                                                                                           1
asymmetry is stark. One half of a flagship computational result in quantum foundations is
independently checkable; the other must be taken on faith.

Contributions. We close this gap for the blocking database on which the published pipeline
leans, and we lay verified groundwork for the full bound. Specifically:

 1. Certificate format (Section 3). We introduce exact rational case-tree certificates of real
    non-embeddability. A certificate WLOG-normalizes an anchor triad or edge, replays a
    propagation schedule that expresses all vertex vectors in few parameters, and presents
    a case tree whose splits are polynomial factorizations and rational sum-of-squares (SOS)
    decompositions, with leaves discharged by injectivity collisions, nonzero-obligation col-
    lapse, ideal membership with explicit cofactors, or a Positivstellensatz-shaped positivity
    argument. Every inference is checkable by exact Q-arithmetic; no numerical tolerance
    appears anywhere in the trust path.

 2. Complete coverage of the blocking database (Section 5). We certify all 291 source lines (180
    distinct graphs) of PhysicsCheck’s order-10/11/12 minimal-non-embeddable blocking lists
    together with the seven order-13 Uijlen–Westerbaan minimal graphs needed for the final
    candidates, replacing every Z3 verdict the database rests on.

 3. Dual independent replay and a kernel-checked soundness theorem (Section 4). Certifi-
    cates are validated by two checkers that share no code with the generator: a pure-
    Python replay over exact fraction arithmetic, and a total checker Cert.check imple-
    mented in the Lean 4 proof assistant [5]. We prove Cert.check_sound: acceptance im-
    plies that no injective-on-rays, orthogonality-respecting assignment of nonzero R3 vec-
    tors realizes the certified graph. The development is sorry-free, with an axiom clo-
    sure of {propext, Classical.choice, Quot.sound} (no native reduction, no custom ax-
    ioms) enforced by a build-time axiom gate. A gcd-free rational layer (KRat) and fuel-
    structural recursion make the verdict computation kernel-reducible, so each per-graph
    non-embeddability corollary is a closed kernel theorem proved by decide in roughly half
    a second.

 4. Findings about the published pipeline (Section 6). Formalization forced precision the
    original workflow did not: we show that pairwise ray-distinctness is load-bearing in the
    published embeddability notion (several database graphs are non-embeddable only for
    injectivity reasons); that the orthoplane parametrization hides WLOG case obligations
    invisible to Z3-based pipelines; that a noncolorability optimization treated as a lemma is
    empirical and not load-bearing; and that the published count of final order-23 candidates
    (41) is not reproducible from the published artifacts under the documented filter—the
    correct count is 43, which we resolve exactly against pinned artifact hashes.

 5. Adversarial validation (Section 5). 115 certificate mutations—dropped branches, tam-
    pered coefficients, incomplete case splits, malformed monomials—are rejected by both
    checkers in continuous integration, on the same code paths that accept the genuine cer-
    tificates.

   Everything in this paper replays from a single build: the Python suite requires only a
Python ≥ 3.9 interpreter, and the Lean development builds with a pinned toolchain and
pinned Mathlib against #guard-checked certificate transcriptions.

Scope. This paper verifies the geometric half for the blocking database: the graphs whose
non-embeddability the published enumeration consults at every order, plus the order-13 graphs


                                               2
           Component                  Basis in published proof   Status here
      T1   CNF encoding correctness   hand proof in paper        analyzed (Section 6)
      T2   minimality WLOGs           hand proofs                lemma inventory (Section 4)
      T3   canonicity pruning         trusted solver code        route fixed (Section 7)
      T4   SAT unsatisfiability       DRAT via drat-trim         streaming plan (Section 7)
      T5   non-embeddability          Z3 NRA, no proof objects   closed for blocking DB

Table 1: Trust surface of the published lower-bound pipeline. This paper closes T5 for the
blocking database (bold); Section 7 addresses the remainder.


that discharge 42 of the 44 final candidates by verified subgraph containment. It does not yet
compose a verified end-to-end bound ≥ 24 theorem; Section 7 lays out the remaining layers—
encoding correctness, verified canonicity, and streaming LRAT replay at terabyte scale—and
the design decisions each one forces.


2     Background and Trust Surface
2.1    The minimum Kochen–Specker problem
Fix nonzero vectors v1 , . . . , vn ∈ R3 , pairwise distinct as rays. Their orthogonality graph
orthGraph has a vertex per vector and an edge per orthogonal pair. A 010-coloring assigns
{0, 1} to vertices so that adjacent vertices are not both 1 and every triangle receives exactly
one 1; a KS system is a vector system whose orthogonality graph admits no 010-coloring. The
minimum KS problem asks for the least n admitting such a system. Uijlen and Westerbaan
[14] established n ≥ 22; Li et al. [12] and Kirchweger et al. [8] independently raised the bound
to n ≥ 24 using SAT-driven enumeration, and 31 remains the best upper bound [2].
    The enumeration strategy is common to both proofs: generate, up to isomorphism, all KS
candidate graphs of order ≤ 23—graphs that are squarefree, 010-noncolorable after symmetry
and minimality pruning—and show that none embeds in R3 as an orthogonality graph of
distinct rays. If no candidate embeds, no KS system of that order exists.

2.2    Trust surface of the published proof
Table 1 summarizes the trust basis of each component of the Li–Bright–Ganesh pipeline
(PhysicsCheck), from our source audit. The SAT half (T4) is the strongest link: unsatisfiability
results carry DRAT proofs, albeit checked by an unverified C checker. The encoding (T1),
minimality arguments (T2), and canonicity pruning (T3) rest on hand proofs and trusted
solver internals. The headline gap is T5: non-embeddability of candidates is decided by
Z3’s nonlinear real arithmetic, plus a Python forced-assignment routine and blocking lists of
minimal non-embeddable subgraphs—themselves Z3-derived. No component of T5 emits a
proof object.

2.3    Why proof objects are hard here
The non-embeddability statements live in the existential theory of the reals: a graph embeds iff
a system of quadratic orthogonality equations, non-vanishing constraints, and ray-distinctness
disequalities has a real solution. Z3 decides such systems, but its NRA engine is a complex
decision procedure whose runs are not reconstructible as checkable objects. Worse, several
obstructions in this database are real-geometric: the orthogonality variety is nonempty over C,
and non-embeddability holds only because every real point collapses a pair of rays. Complex
ideal membership (a Gröbner-basis certificate alone) is provably insufficient for these graphs;


                                                3
any complete certificate format must speak about real positivity. Our format does so through
rational SOS splits and a Positivstellensatz-shaped positivity leaf (Section 3), while keeping
every check inside exact Q-arithmetic—the checkers never factor, never search, and never call
a CAS.


3     Case-Tree Certificates of Real Non-Embeddability
A certificate for a graph G is a self-contained object—anchor, propagation schedule, parameter
list, and case tree—replayed by a checker that performs only exact rational arithmetic on
structured polynomials (monomial lists over Q, mirroring the Lean MPoly normal form). The
generator may be clever; the checkers stay dumb, total, and exact.

3.1    Embedding notion
Formalization begins by fixing what “embeddable” means, and here the published pipeline
holds a surprise (Finding 1): PhysicsCheck’s Z3 encoding asserts pairwise ray-distinctness
for all vertex pairs, not merely adjacent ones, making injectivity part of embeddability. Our
verified statement therefore builds it in.
Definition 3.1 (Realization). A realization of a graph G on vertices 1, . . . , n is a map v 7→
vv ∈ R3 such that (i) vv ̸= 0 for all v; (ii) dot(vi , vj ) = 0 for every edge {i, j}; and (iii) for
all v ̸= w, vv and vw are distinct as rays. G is non-embeddable if it has no realization.

3.2    WLOG normalization and the propagation schedule
The rotation group acts transitively on ordered orthonormal triads, and on ordered orthonor-
mal pairs; per-vertex scaling is free. A certificate opens by anchoring either an orthogonal
triangle (a, b, c) 7→ (e1 , e2 , e3 ) or, for triangle-free graphs, an edge (a, b) 7→ (e1 , e2 ). It then
replays a schedule of two step forms:

    • cross(v, u, w): assign vv := vu × vw where v is adjacent to both assigned vertices
      u ̸= w. Soundness is the orthocomplement lemma (w ⊥ u, w ⊥ v, u ∦ v imply w ∥ u×v),
      and the side condition vu ×vw ̸= 0 becomes a recorded obligation polynomial ∥vu ×vw ∥2 ,
      justified by ray-distinctness of u and w.

    • plane(v, u, axis): parametrize vv := sv p + tv q with p = vu × eaxis and q = vu × p,
      introducing fresh parameters sv , tv and obligations ∥p∥2 and s2v + t2v .

    The orthoplane parametrization conceals a case the informal argument never surfaces: the
spanning pair (p, q) degenerates when the parent vector is parallel to the chosen basis vector.
That branch must be discharged by injectivity against an anchor vertex, which is why edge-
anchored certificates restrict plane axes to anchor-owned axes (e1 , e2 , never e3 )—the sound
discharge is otherwise unavailable (Finding 2).
    After the schedule, every vertex vector is a polynomial in the parameters; the pool con-
sists of one orthogonality polynomial dot(vi , vj ) per induced edge, shrunk by inline linear
elimination steps whose provenance the checker re-derives (each substitution names the pool
polynomial it comes from), typically leaving at most two residual polynomials.

3.3    The case tree
Internal nodes split the current branch; leaves close it. Splits take two forms: a factorization
            Q
split on p = k fk (in an integral domain, a vanishing product forces some factor to vanish—
the checker verifies the product identity by expansion), and an SOS split on p = k ck m2k
                                                                                       P


                                                   4
  SPLIT[FACTOR] on -s2^6 s6 t6^2 - s2^4 s6^3 - 2 s2^4 s6 t2^2 t6^2
    [s6 = 0] LEAF COLLIDE (1,3)    rays of vertices 1,3 coincide
    [s2 = 0] LEAF OBLIG basis[2,e1]    vertex 2 parallel to anchor
    [s2^2 t6^2 + s6^2 + 2 t2^2 t6^2 = 0]
              SOS => all summands 0 => LEAF COLLIDE (1,3)


Figure 1: Certificate for order-10 graph #1 (verbatim). The factorization split is verified
by expanding the product; the SOS split by expanding k ck m2k ; both leaves are injectivity
                                                      P

contradictions.

with ck ∈ Q>0 (over a formally real field, a vanishing sum of squares forces every summand
to vanish). SOS witnesses are found offline by exact Gram-matrix LDLT decomposition over
an explicit monomial basis, but the certificate records only (ck , mk ) and the checker verifies
the identity by expansion; the discovery procedure is not trusted. Leaves are:

   • collide(i, j): the replayed vectors of distinct vertices i, j are provably parallel on
     this branch, contradicting ray-distinctness;

   • oblig: an obligation polynomial (or a designated basis component of an anchor-adjacent
     vector) is identically zero on this branch, contradicting its justification;

   • ideal and one: explicit cofactors q1 , . . . , qm with i qi pi = g over the residual pool
                                                                  P

     {p1 , . . . , pm }, where g is an obligation polynomial or a pair-injectivity polynomial ∥vi ×
     vj ∥2 (ideal), or i qi pi = 1 (one: the pool has no common zero over any field);
                            P


   • positiv: cofactors qr , vertex pairs (i1 , j1 ), . . . , (im , jm ), and an SOS list (ck , hk ) with
     the polynomial identity
                                 m
                                 Y                     X              X
                                     ∥vil × vjl ∥2 +       ck h2k =       qr · p r ,                 (1)
                                 l=1                   k              r

      verified by expansion. At a real point of the branch the right side vanishes while the
      left is strictly positive—each pair factor is positive by injectivity and the SOS term is
      nonnegative—a contradiction.

     The positiv leaf is the Positivstellensatz-shaped generalization of ideal, and it is not
a luxury: some branch varieties are real-nonempty, but every real point collapses a varying
vertex pair, so no single collision or ideal argument closes the branch.
     Finally, a certificate may carry a restrict_to field naming an induced subgraph H ⊆ G
actually certified; subgraph monotonicity (a realization of G restricts to one of any subgraph,
induced or not) lifts non-embeddability to G. This is needed because the published order-
11/12 blocking lists contain graphs consisting of a non-embeddable core plus isolated vertices,
and—in its general, non-induced form—it is exactly the lemma that lets seven order-13 cer-
tificates discharge 42 of the 44 final candidates (Section 5).

3.4   A complete example
Figure 1 shows a certificate for the first order-10 graph in the database, verbatim from the
human-readable rendering. The tree is three levels deep and closes every branch by injectivity.




                                                   5
    /-- A real realization of the graph carried by certificate ‘c‘:
        nonzero vectors for the vertices ‘1..c.n‘, orthogonal along every
        edge, pairwise distinct as rays. -/
    structure Realization (c : Cert) where
      vec      : Nat → Vec3 R
      nonzero : ∀ v, 1 ≤ v → v ≤ c.n → vec v ̸= ⟨0, 0, 0⟩
      orth     : ∀ e ∈ c.edges, dot (vec e.1) (vec e.2) = 0
      distinct : ∀ v w, 1 ≤ v → v ≤ c.n → 1 ≤ w → w ≤ c.n → v ̸= w →
                   ¬ SameRay (vec v) (vec w)

    /-- Soundness: checker acceptance refutes every realization. -/
    theorem check_sound (c : Cert) (h : check c = true)
        (x : Realization c) : False


Figure 2: The verified statement.        check_sound is sorry-free with axiom closure
{propext, Classical.choice, Quot.sound}.


3.5    Schema and normative deserialization
Certificates ship as JSON (schema_version = 1) with fully structured polynomials: a mono-
mial is a rational coefficient with positive denominator and a duplicate-free, exponent-positive
variable list. Well-formedness is normative and enforced at ingestion by both checkers; the
adversarial suite includes a duplicated-variable monomial that normalizes to the correct poly-
nomial, so only syntactic rejection distinguishes it (Section 5). The replay checkers share no
code and no parsing with the generator.


4     A Kernel-Checked Soundness Theorem in Lean 4
The Lean development (toolchain v4.32.0, pinned Mathlib) implements the checker as a total
reflective function Cert.check over the same normal-form polynomial arithmetic the schema
prescribes, and proves it sound against the semantic embedding notion of Theorem 3.1.

4.1    The soundness theorem
Figure 2 gives the statement. The proof factors through an interpretation invariant for the
schedule replay (orthocomplement representatives for cross steps; well-posed 2 × 2 solves for
plane steps), an elimination replay that consumes exactly what the checker verifies syntac-
tically, and a descent through all eight node kinds of the case tree. The real-geometry layer
supplies the seven lemmas the tree walk consumes: transitivity of the O(3) action on anchored
triads and edges, per-vertex scaling, the orthocomplement lemma, injectivity of the cross prod-
uct on distinct rays, plane-basis spanning with its parallel branch, SOS-zero over formally real
fields, and factor-zero in integral domains; the leaf extensions add evaluation of ideal identities
(evaluation is a ring homomorphism) and the positivity argument for Equation (1). The full
lemma inventory, including the combinatorial-layer lemmas (squarefreeness of orthogonality
graphs, noncolorability of KS graphs, vertex deletion, subgraph monotonicity), is maintained
in the repository with the invariant that any change to certificate semantics lands only after
its justifying lemma is inventoried.
     Discipline is enforced mechanically. A build-time axiom gate audits the axiom closure
of every declaration (no axioms beyond {propext, Classical.choice, Quot.sound}, no native
reduction), synchronizes the sorry set against a manifest in both directions—the manifest



                                                6
      order                            source lines   distinct   certified   replay   kernel thms
      10                                         2          2        2/2       ✓             2/2
      11                                        16         16      16/16       ✓           16/16
      12                                       266        155    266/266       ✓         155/155
      13 (Uijlen–Westerbaan minimal)             7          7        7/7       ✓             7/7
      total                                    291        180    291/291       ✓         180/180

Table 2: Certification coverage of the PhysicsCheck blocking database and the order-13 Uijlen–
Westerbaan minimal graphs. “Source lines” counts lines of the published graph lists; duplicate
lines share their graph’s theorem, with the line–graph binding verified by replay.


is empty—and confines Mathlib imports to the real-geometry subtree; the combinatorial and
checker layers build against core and Batteries only.

4.2    Kernel-reducible verdicts
A soundness theorem transfers no trust to a graph until the hypothesis check c = true is
itself established inside the trusted kernel. Initially this was only possible by compiled evalu-
ation (#guard), for two structural reasons: core Rat normalizes through Nat.gcd, which does
not reduce feasibly in the kernel, and the checker’s well-founded recursions do not unfold
definitionally.
    We closed the gap without native_decide and without changing semantics. The KRat
 layer provides gcd-free, normalization-free fractions: integer numerator/denominator pairs
carrying a den ̸= 0 invariant maintained by the operations, with zero-testing by numerator,
equality by cross-multiplication, and sign via num · den. The polynomial merge and the tree
walk were rewritten in fuel-structural form with evaluation-preserving (append) and rejecting
(false) fallbacks respectively, so every semantics lemma holds at every fuel value and fuel
exhaustion can only refuse a certificate—never accept one. The whole verdict computation is
then kernel-reducible, and each per-graph corollary is a closed kernel theorem:

    theorem c10_0_nonembeddable : /- no Realization of graph #0 -/ := by decide

    Kernel evaluation costs ≈ 0.5 s per order-≤ 12 verdict and ≈ 1.8 s per order-13 verdict on
a laptop (Table 3); the escalation threshold budgeted in the phase plan (60 s per certificate)
was never approached. Each generated theorem pins its graph to an explicit colex edge list by
#guard, independently re-verified against the PhysicsCheck source files by the Python replay,
so the binding between a source line and its theorem is itself checked, not asserted. Certificate
transcription into Lean is deterministic and diff-checked in CI, and the coverage table in the
repository README is regenerated from the compiled Lean environment, not from the JSON.


5     Results
5.1    Coverage
Table 2 summarizes coverage: every distinct graph in the blocking database carries a closed
kernel non-embeddability theorem, and every source line is bound to its theorem. The order-
10 trees are at most three levels deep and fully human-readable; deeper trees at orders 11–13
exercise edge anchors, induced-subgraph restriction, and the ideal and positivity leaves. The
seven order-13 certificates were produced in 18 seconds of generator time, a consequence of
the format’s maturity by that phase.



                                                 7
      shard                                certificates   marginal user time   per certificate
      order-10 shard                                 2                 0.9 s         ≈ 0.45 s
      order-12 shard                                20                10.0 s         ≈ 0.50 s
      order-13 shard (Uijlen–Westerbaan)             7                12.4 s          ≈ 1.8 s

Table 3: Marginal kernel cost of decide verdicts (laptop-class arm64, Lean 4.32.0). Marginal
user CPU time over an imports-only baseline; wall time is dominated by ≈ 76 s of olean
loading.


    The order-13 row does real work for the full bound. Replaying the published pipeline’s
candidate artifacts (Finding 5), the final order-22/23 candidate set has 44 members after
the pipeline’s own ≤ 12-subgraph filter—and none of them contains any of our 173 certified
order-≤ 12 graphs, so containment against the existing database discharges nothing. But
exactly 42 of the 44 contain one of seven order-13 Uijlen–Westerbaan minimal non-embeddable
graphs, so certifying those seven discharges 42 candidates via the verified general (non-induced)
subgraph-monotonicity lemma. The remaining two candidates are recorded machine-readably
as unresolved obligations—never faked, appearing as explicit hypotheses in any composed
statement until closed—with direct certification in progress.

5.2   Kernel timings
Table 3 reports kernel-evaluation costs. Extrapolated total kernel and elaboration cost for
all 173 order-≤ 12 certificates is roughly 90 s of CPU; the full ten-shard build completes in
minutes under parallel contention. Kernel-checking the geometric half of this database is, in
short, cheap enough to run in CI on every commit—which it does.

5.3   Adversarial validation
Checker code that has only ever seen valid certificates is untested where it matters. The adver-
sarial suite mutates genuine certificates in 115 ways—dropping a branch of a split, tampering
with an SOS coefficient, truncating a factorization, removing a leaf justification, injecting a
duplicated-variable monomial that normalizes correctly, corrupting cofactors of an ideal iden-
tity, breaking the edge-list binding—and requires both checkers to reject every mutant. The
Lean side runs the mutations through the same Cert.check code path used by the kernel
theorems (via a replay executable), giving CI-demonstrated adversarial parity between the
two checkers: 115/115 rejected by both.


6     What Formalization Revealed About the Published Pipeline
A recurring theme of verified re-examinations of computational proofs is that the formalization
pays for itself in findings. Ours is no exception. Throughout, the governing rule was soundness
over coverage: whenever a proof needed a hypothesis the checker did not verify syntactically,
the resolution was to strengthen the checker or report a finding—never to weaken a check or
paper over a discrepancy.

Finding 1 (Injectivity is load-bearing). PhysicsCheck’s Z3 encoding asserts cross(vj , vi ) ̸= 0
for all pairs i ̸= j, making pairwise ray-distinctness part of its embeddability notion. This is
not cosmetic: several database graphs have orthogonality systems with real solutions, every
one of which collapses some (varying) vertex pair. Those graphs are non-embeddable only
for injectivity reasons. Any verified statement must therefore build injectivity into the em-
bedding definition—ours does (Realization.distinct)—and any complete certificate format


                                                8
must reason about injectivity loci, not just the orthogonality ideal, which is what forced the
positiv leaf of Section 3.
Finding 2 (Hidden WLOG case obligations). The orthoplane parametrization conceals a
degenerate branch—parent vector parallel to the chosen basis vector—that must be discharged
by injectivity against an anchor vertex, and the edge-anchor variant is sound only because
plane axes are restricted to anchor-owned axes. Z3-based pipelines never surface such case
obligations; a checker with a soundness theorem cannot avoid them.
Finding 3 (The half-ones optimization is empirical, not a lemma). The pipeline’s noncol-
orability encoding blocks only colorings with 1 ≤ |ones| ≤ ⌈n/2⌉. Our verification plan ini-
tially treated the underlying claim as a load-bearing unverified lemma; the audit overturned
this premise. The paper itself justifies the restriction empirically, and it is not load-bearing
for the bound: dropping blocking clauses only enlarges the candidate set, and the direction
the verified chain needs—a noncolorable graph satisfies every blocking clause—is trivial and
proved sorry-free. The stronger counting statement remains open (the natural injection proof
provably fails on a girth-5 edge-count obstruction) and is recorded as a proof-free conjecture,
relevant only to completeness claims, not soundness. Two secondary paper-versus-code dis-
crepancies are documented for the encoding-correctness layer: an off-by-one in the blocking
range (paper text < ⌈n/2⌉, code ≤ ⌈n/2⌉) and the never-blocked empty coloring (benign
only because the triangle constraint forces a triangle). Relatedly, one documented minimality
constraint is commented out in the generator source, so the encoding-correctness target must
match the constraint set as shipped, not as described.
Finding 4 (Dataset accounting). The order-12 blocking file has 266 lines, not the previously
reported 265 (the file lacks a trailing newline), of which only 155 are distinct edge sets; 33
order-12 and 2 order-11 entries are disconnected, consisting of an order-10/11 non-embeddable
core plus isolated vertices. The blocking lists are raw enumeration output, not a deduplicated
minimal set. This is why certificates carry induced-subgraph restriction, and why per-line
bindings are verified rather than assumed.
Finding 5 (The published final-candidate count is not reproducible). The published sources
disagree about the final order-22/23 candidates: the paper’s text reports one order-22 and
41 order-23 candidates surviving the ≤ 12-subgraph filter, a figure caption implies only two
candidates lack minimal unembeddable subgraphs, and the published artifact’s log for that
step has exactly two lines. We settled the question against the artifacts, with SHA-256 hashes
pinned: decoding the published exhaust files yields 88,282 distinct order-22 candidates and
5,160,001 distinct order-23 candidates; replicating the pipeline’s own filter semantics exactly
(non-induced monomorphism against its 17 minimal graphs) leaves 1 survivor at order 22
and 43 pairwise non-isomorphic survivors at order 23—not 41. Classifying the 43 against the
located Uijlen–Westerbaan minimal-unembeddable list (933 graphs) reconciles the sources:
exactly 41 contain an order-13 Uijlen–Westerbaan minimal graph (seven distinct patterns
suffice), and the two that do not are precisely the pair in the published log—so the caption’s
“only two” is correct with reference class “known minimal unembeddable graphs,” while the
“41” is not reproducible from the artifact under the documented filter. None of this threatens
the bound; it does mean the verified chain must carry 44 final candidates, not 42, and it is
exactly the kind of discrepancy that replayable proof objects exist to eliminate.
    Two further findings are internal to the checkers and illustrate the discipline: substitution
semantics were made unconditional (total-exponent stripping) rather than relying on a well-
formedness invariant the Lean checker never verified, and monomial well-formedness was made
normative at deserialization in both checkers after the adversarial suite exposed a mutant
distinguishable only syntactically.

                                               9
7    Toward a Fully Verified Bound
The verified architecture has four layers, composing to “no KS system on ≤ 23 vectors,” hence
the bound 24: L1 (real geometry to combinatorics: vector systems, orthogonality graphs,
squarefreeness, noncolorability, minimality WLOGs), L2 (combinatorics to CNF: encoding-
correctness theorems for the generator’s constraint set as shipped), L3 (CNF exhaustiveness:
verified replay of the enumeration’s unsatisfiability results together with a proved-sound canon-
icity predicate), and L4 (candidate non-embeddability: this paper). L4 is closed for the block-
ing database and, via the order-13 certificates, for 42 of the 44 final candidates; the L1 lemmas
consumed so far are proved.
    Two design decisions dominate the remainder. For L3 canonicity, trusting the solver’s
symmetry-breaking code is not acceptable, and the published proof format resolves the choice
favorably: its CAS-derived clauses carry permutation witnesses for both the orderly-generation
blocking and the minimal-non-embeddable-subgraph blocking. Verifying a blocked candidate
then means applying the recorded permutation and checking a lexicographic comparison, or
checking a subgraph embedding against a certified non-embeddable graph—both squarely
within the verified toolkit of Section 4. An alternative route, re-running the enumeration
with VeriPB dominance-based proof logging bridged into Lean [6, 13], is cleaner but costs
compute; it remains the fallback if witness regeneration proves brittle.
    For L3 unsatisfiability, scale forbids kernel-level replay: the published DRAT/LRAT ma-
terial runs to 6.1 TiB through order 22 and 40.3 TiB at order 23. The plan is a verified
streaming LRAT checker—Lean-proved sound, compiled, constant-memory, in the tradition
of verified SAT proof checking [3, 11]—composed with the Lean-side statement, with only
per-cube summary artifacts entering the kernel.
    The staging is deliberately tiered: first a fully self-contained re-derived bound at small
orders (a verified ≥ 22, matching [14], with verified canonicity and the complete lemma
inventory), then replay through order 23 for a fully verified ≥ 24, contingent on the published
cube certificates or re-runs and a cluster budget. The composed theorem will carry the two
unresolved order-23 candidates as explicit hypotheses until their direct certificates land; under
the repository’s invariants, an unresolved graph is reported as unresolved, never absorbed.


8    Related Work
The minimum KS problem. The bound ≥ 18 of Arends et al. [1] introduced the graph-
theoretic minimality arguments (squarefreeness, WLOG constraints) the modern pipelines
inherit; Uijlen and Westerbaan [14] reached ≥ 22 and published the minimal non-embeddable
graph lists we reuse at order 13; Li et al. [12] and Kirchweger et al. [8] independently reached ≥
24 with SAT-plus-computer-algebra pipelines. Our work audits and complements the former’s
published pipeline and artifacts; nothing here diminishes those results—the point is to make
them independently checkable.

Verified SAT-based mathematics. Machine-checked replay of SAT-derived mathemati-
cal results is by now a tradition, from the Boolean Pythagorean triples proof onward, resting
on verified DRAT and LRAT checkers [3, 11] and, recently, on pseudo-Boolean proof logging
with dominance reasoning [6] bridged into proof assistants [13], whose encoding-correctness
pattern our L2 instantiates on a problem with a fifty-year pedigree. The distinctive difficulty
here is that SAT proofs cover only half the argument; the other half lives in ∃R.

Certificates for real-algebraic reasoning. Sum-of-squares and Positivstellensatz certifi-
cates for real infeasibility are classical in verified optimization and formal proof, and formally


                                               10
real fields provide exactly the leverage our SOS splits use. Our contribution on this axis is a
certificate format tuned to orthogonality systems—WLOG anchoring, schedule replay, injec-
tivity obligations, and a positivity leaf over products of pair-injectivity polynomials—small
enough for a total checker with a kernel-checked soundness proof and kernel-reducible verdicts.
On the satisfiable side of ∃R search, recent work attacks realizability with numerical-symbolic
methods [10]; our certificates target the unsatisfiable side with replayable objects, adjacent
but not overlapping.

KS formalizations. An existing Lean development proves the Kochen–Specker paradox
itself via one explicit vector gadget [7]—the existence direction. To our knowledge, no prior
machine-checked certificate exists for the geometric half of any KS lower bound.


9    Conclusion
The geometric half of the minimum Kochen–Specker bound no longer needs to be taken
on faith for the graphs the published proof consults at every step: all 291 source lines of the
blocking database now carry exact rational case-tree certificates, replayed by two independent
checkers and backed by closed Lean kernel theorems under a minimal axiom closure, at a cost
of about half a second of kernel time per graph. The exercise also demonstrated, once more,
why proof objects matter beyond replication: building a checker one must prove sound surfaced
a load-bearing injectivity condition, hidden WLOG branches, an optimization misclassified
as a lemma, and an unreproducible headline count—none visible to a workflow that trusts its
solvers.
    The path to a fully verified ≥ 24 is scoped and, we believe, unblocked: witness-based
canonicity checking matches the published proof format, streaming LRAT replay addresses
the terabyte-scale SAT material, and 42 of the 44 final candidates are already discharged by
verified subgraph containment. The remaining two candidates are tracked as explicit, machine-
readable obligations—which is, in the end, the entire method: never a verdict without an
object, never an object without a checker, never a checker without a proof.

Artifact availability. Certificates, both checkers, the Lean development, the adversarial
suite, and the artifact-provenance records (including SHA-256 pins for Finding 5) are available
at https://github.com/shayaansiddique06/kscert under the Apache 2.0 license, with a
pinned toolchain and a single-command build for each component.

Acknowledgments. We thank the authors of PhysicsCheck for publishing their pipeline
and proof artifacts, without which this audit-and-certify effort would not have been possible.
The development was carried out with assistance from Claude (Anthropic).


References
 [1] Felix Arends, Joël Ouaknine, and Charles W. Wampler. On searching for small Kochen–Specker
     vector systems. Graph-Theoretic Concepts in Computer Science (WG), pages 23–34, 2011.

 [2] John H. Conway and Simon Kochen. A 31-vector Kochen–Specker system, 1993. Reported in A.
     Peres, Quantum Theory: Concepts and Methods, Kluwer, 1993.

 [3] Luís Cruz-Filipe, Marijn J. H. Heule, Warren A. Hunt, Matt Kaufmann, and Peter Schneider-
     Kamp. Efficient certified RAT verification. In Automated Deduction (CADE), volume 10395 of
     LNCS, pages 220–236, 2017.




                                              11
 [4] Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In Tools and Algorithms
     for the Construction and Analysis of Systems (TACAS), volume 4963 of LNCS, pages 337–340,
     2008.

 [5] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language.
     In Automated Deduction (CADE), volume 12699 of LNCS, pages 625–635, 2021.

 [6] Stephan Gocht and Jakob Nordström. Certifying parity reasoning efficiently using pseudo-Boolean
     proofs. In Proceedings of the AAAI Conference on Artificial Intelligence, 2021. VeriPB proof
     system; dominance-based proof logging.

 [7] Anand Gupta. A Lean 4 formalization of the Kochen–Specker paradox. https://github.com/
     guptbot/free_will_lean, 2025.

 [8] Markus Kirchweger, Tomáš Peitl, and Stefan Szeider. Co-Certificate learning with SAT modulo
     symmetries. In Proceedings of the 32nd International Joint Conference on Artificial Intelligence
     (IJCAI), 2023.

 [9] Simon Kochen and Ernst P. Specker. The problem of hidden variables in quantum mechanics.
     Journal of Mathematics and Mechanics, 17(1):59–87, 1967.

[10] Andrew Krapivin, Benjamin Przybocki, and Marijn J. H. Heule. Toward satisfiability modulo
     realizability. arXiv preprint, arXiv:2607.02958, 2026. To appear in CICM, 2026.

[11] Peter Lammich. Efficient verified (UN)SAT certificate checking. Journal of Automated Reasoning,
     volume 64, pages 513–532, 2020.

[12] Zhengyu Li, Curtis Bright, and Vijay Ganesh. A SAT solver and computer algebra attack on the
     minimum Kochen–Specker problem. arXiv preprint, arXiv:2306.13319, 2024. Artifact repository:
     github.com/BrianLi009/PhysicsCheck.

[13] Stefan Szeider. PBLean:     Pseudo-Boolean proof certificates for Lean 4. arXiv preprint,
     arXiv:2602.08692, 2026.

[14] Sander Uijlen and Bas Westerbaan. A Kochen–Specker system has at least 22 vectors. New Gen-
     eration Computing, 34:3–23, 2016.

[15] Nathan Wetzler, Marijn J. H. Heule, and Warren A. Hunt. DRAT-trim: Efficient checking and
     trimming using expressive clausal proofs. In Theory and Applications of Satisfiability Testing
     (SAT), volume 8561 of LNCS, pages 422–429, 2014.




                                                 12
