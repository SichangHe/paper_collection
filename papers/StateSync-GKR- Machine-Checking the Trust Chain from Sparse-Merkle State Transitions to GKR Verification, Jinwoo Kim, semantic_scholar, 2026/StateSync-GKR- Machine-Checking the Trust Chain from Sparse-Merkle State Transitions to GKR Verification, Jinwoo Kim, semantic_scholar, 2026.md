                                                 StateSync-GKR: Machine-Checking the Trust Chain from
                                                  Sparse-Merkle State Transitions to GKR Verification
                                                                                       Preprint, compiled October 6, 2026

                                                                                                  Jinwook Kim1,2
                                                                                            (for the Oraclizer Core Team)
                                                                                       1 Oraclizer Labs, Inc., Delaware, USA
                                                                                        2 Oraclizer Labs Korea, Seoul, Korea
                                                                                                 jay@oraclizer.io

                                                                                                    Abstract
arXiv:2610.05335v1 [cs.CR] 4 Oct 2026




                                                 GKR soundness bounds false output claims about arithmetic circuits, but an application also needs assurance
                                                 that its circuit encodes the intended state transition. We machine-check this connection for sparse-Merkle
                                                 membership, non-membership, and update in Isabelle/HOL. A compiler model relates circuit acceptance to
                                                 transition validity in both directions. A reusable protocol model assembles layer reduction, wiring-predicate
                                                 extensions, and imported sumcheck soundness into a bound on an explicit chain event. Their composition
                                                 transfers semantic invalidity to that bound, with the witness fixed before the challenge experiment. Concrete
                                                 interpretations and premise activations expose vacuous assumption sets that a clean build alone would miss. A
                                                 further development constructs the exact degree-four KoalaBear extension, lifts the base-field circuit objects,
                                                 and establishes the assembly bound with denominator 𝑝 4 under its stated challenge assumptions. An executable
                                                 Rust prover accompanies the model. Creusot/Why3 contracts provide a partial implementation connection,
                                                 and a conditional theorem relates successful verifier traces to the model event under an undischarged value-
                                                 correspondence premise. Neither the transcript’s online challenge distribution nor a multi-round Fiat–Shamir
                                                 reduction is established. The contribution is the composition, within one proof assistant, of compiler cor-
                                                 rectness with a GKR assembly model, together with an explicit account of the remaining implementation and
                                                 cryptographic obligations.

                                        Keywords GKR protocol · sumcheck · interactive proofs · formal verification · Isabelle/HOL · sparse Merkle tree · circuit
                                        compiler · Rust · refinement

                                        1   Introduction
                                        Problem. Proof systems of the GKR family [9, 18, 20] verify computations expressed as layered arithmetic circuits. Their
                                        soundness guarantee is precise but narrow: if the circuit’s output claim is false, the verifier accepts with probability bounded
                                        by a small quantity over the challenge field. An application that deploys such a verifier, however, does not want to know that
                                        a circuit evaluated to zero. It wants to know that a state transition it cares about—here, an operation on a sparse Merkle tree
                                        that carries financial state—is valid. That gap is bridged, in deployed systems, by a circuit compiler: a piece of software that
                                        translates transition semantics into gates and wiring. The soundness theorem says nothing about this compiler. If the compiler
                                        emits a circuit whose acceptance condition fails to coincide with the intended semantics, the verifier faithfully checks the wrong
                                        statement, and every downstream consumer of its acceptance inherits an unfounded belief.

                                        Gap. The formal-methods literature has begun to mechanize the probabilistic heart of these protocols. The sumcheck proto-
                                        col [13], the recursive engine inside GKR, has a machine-checked soundness and completeness development in Isabelle/HOL,
                                        registered in the Archive of Formal Proofs [8, 7], and a Lean 4 formalization effort covers sumcheck at the level of interactive oracle
                                        reductions [19]. These developments deliberately stop before the GKR layer-reduction chain, its wiring-predicate extensions, and
                                        a composition with an application compiler. To the best of our knowledge, no prior mechanized development spans that model
                                        chain (section 12 surveys the adjacent work). Connecting such a model to an implementation is a further, distinct obligation; this
                                        paper supplies only the partial refinement stated in section 9.

                                        Approach. We mechanize the model chain for a concrete workload in Isabelle/HOL 2025-2 and organize its core in two sessions
                                        along the line that separates the reusable from the specific, with a further four-session chain on top that carries the result to the
                                        field the implementation actually uses. The general session formalizes layered circuits, multilinear extensions, the layer-reduction
                                        identity, the per-layer sumcheck instances (with per-round soundness imported from the AFP entry), the chain-event soundness
                                        bound of the assembled protocol model, the equivalence of a derived closed-form wiring oracle with its defining table form, and
                                        a batching-preservation theorem. The specialized session formalizes sparse-Merkle transition semantics, the circuit compiler at
                                        the level of an explicit constraint model, the equivalence of circuit acceptance with transition validity, the composition theorem,
StateSync-GKR: Mechanized Trust Chain                                                                                               2

and concrete instances over the production field that witness every assumption set. The development accompanies an executable
Rust prover stack; a separate, explicitly partial refinement layer connects the code to the model and declares exactly where
machine-checked correspondence ends and stated trust begins.

Contributions.    The paper makes six contributions.
1. Mechanized compiler correctness for sparse-Merkle transitions. A formal semantics of sparse-Merkle membership, non-
   membership, and update over three-state leaves, and a machine-checked equivalence—in both directions, with a canonical
   witness—between acceptance of the compiled layered circuit and transition validity (Theorem A), together with an injectivity
   lemma for the leaf pre-image encoding that reduces leaf-hash collisions to collisions of the underlying sponge.
2. A machine-checked GKR protocol assembly model. A formalization of layer reduction, wiring-predicate multilinear
   extensions, and the sumcheck chain, with per-round soundness imported from the AFP sumcheck entry and an explicit bound
   on the model chain event proved by induction over the layer chain (Theorem B), parametric in a per-layer degree-bound
   function. The implementation-facing per-variable degree-four form is recovered as a statement-level corollary; it is not
   activation-witnessed by the current polynomial instance. A separate four-session chain then transfers the assembly bound from
   the KoalaBear base field to the exact degree-four extension the implementation draws challenges from, proving the tower’s field
   structure and cardinality, lifting polynomials, multilinear extensions, circuits, and false outputs along the base-field embedding,
   and fixing the bound’s denominator at 𝑝 4 . The two “degree four” are different objects and are kept apart throughout: one is a
   per-variable degree bound inside the sumcheck, the other is the degree of the field extension.
3. A model-level composition theorem. A single mechanized statement (Theorem C) transfers semantic invalidity, through
   the compiled circuit, to the bounded GKR chain event. This closes the semantics-to-protocol composition inside the model.
   Connecting a running verifier’s transcript acceptance to that event remains an explicit partial-refinement obligation rather than
   part of Theorem C.
4. Batching preservation and concrete nonvacuity. A generic batching-preservation theorem (Theorem D), and a nonvacuity
   discipline with teeth: every locale assumption set is witnessed by a registered concrete instance over the production field, and
   the paper reports how this discipline caught two vacuously true headline theorems that had survived a clean build.
5. A conditional refinement of the shipped verifier’s acceptance. A theorem relating a successful acceptance trace of the
   verifier that ships in the artifact to the reduction-chain event of Theorem B. The relation between the running values and the
   model objects is carried as an explicit, deliberately load-bearing premise, stated in the theory and not discharged against the
   compiled program; the undischarged value relation and the probabilistic nature of the soundness statement limit its executable
   interpretation. Its force is confined to that implication and its stated premise.
6. An artifact with an explicit refinement boundary. An executable Rust prover stack on pinned Plonky3 building blocks,
   connected to the Isabelle model by Creusot contracts under a declared trust surface; the checked obligations, tool walls, trusted
   items, and black-box assumptions are enumerated without rounding them up to whole-program verification.

Result boundary. Four boundaries frame everything that follows. First, the probabilistic statements bound an explicitly defined
event in an interactive public-coin model. The implication from the running verifier’s transcript checks to that event has a
mechanized conditional form, but its value-correspondence premise is stated rather than discharged, and Fiat–Shamir remains
outside the model entirely. Second, the composition theorem itself uses one finite field, while the executable stack evaluates the
circuit over the base field and derives challenges in a degree-four extension. The lift to the exact extension field is mechanized,
so the bound’s 𝑝 4 denominator is no longer an unmechanized step; what is not mechanized is that the implementation’s transcript
yields challenges distributed as the lifted statement assumes. Third, the implementation refinement is partial: we report the
checked obligations, the trust surface, and the tool walls. Fourth, this paper makes no performance claim; the depth-independent
layer count is a recorded structural observation, not a benchmark comparison.
Section 2 makes the trust gap precise. Section 3 introduces the system. Sections 4 to 7 present the four stages of the chain,
section 8 the batching theorem and the nonvacuity discipline, section 9 the relationship to the implementation, section 10 the
artifact, section 11 the trust boundary, section 12 related work, and section 13 concludes.

2   The State-to-GKR Trust Gap
Consider a system in which acceptance of a proof is the trigger for a downstream effect: a state root is finalized, a synchronization
is committed, an asset changes hands. The deployment stack for a GKR-based verifier in such a system has four stages, and each
stage has a distinct correctness question.
1. Transition semantics. What does it mean for the claimed state transition to be valid? This must be a mathematical definition,
   or nothing downstream can be proved about it.
2. Circuit compilation. The transition is compiled to a layered arithmetic circuit. The correctness question: does the circuit’s
   acceptance condition hold exactly when the transition is valid? An unsound compiler admits invalid transitions; an incomplete
   one rejects valid transitions, which for a system whose liveness depends on proof issuance is equally fatal.
StateSync-GKR: Mechanized Trust Chain                                                                                               3

3. Protocol execution. The prover and verifier run the GKR protocol over the compiled circuit. The correctness question is the
   classical soundness bound: if the output claim is false, acceptance is improbable.
4. Acceptance consumption. A consumer treats verifier acceptance as evidence that the transition is valid. This step is sound
   only if stages 1–3 compose: the probability bound from stage 3 must transfer, through the compiler equivalence of stage 2, to
   the semantics of stage 1.

The gap is that in deployed practice stage 3 alone has a theorem behind it—proved on paper, about an idealized protocol, for an
arbitrary circuit. (A growing research line supplies stage-2 theorems for specific systems, surveyed in section 12; what it does not
supply is their composition with stage 3 in one mechanized system.) The compiler of stage 2 is trusted software. The composition
of stage 4 is an informal argument. Even at stage 3, what runs is an implementation whose correspondence to the idealized
protocol is asserted rather than established. Each unproved step is a place where acceptance can detach from meaning without
any test failing: a compiler that drops a constraint still produces circuits, proofs, and acceptances—for a strictly weaker statement
than intended.
There is also a subtler failure mode, internal to the formalization itself, that this development met in practice: a mechanized
theorem whose assumption set is unsatisfiable is vacuously true, and the proof assistant will not volunteer this. A trust chain
assembled from vacuous links type-checks and builds. Section 8 describes how we make nonvacuity a checked property rather
than a hope, and what that check caught.
This paper’s thesis is that a claim of semantic force for GKR acceptance needs an explicit composition from transition semantics
through circuit compilation to the protocol model. The remainder constructs and instantiates that composition, carries it to the
exact field the implementation uses, and relates the shipped verifier acceptance to it under a stated premise, leaving what is left
of those two bridges visible as named obligations rather than as silence.

3   StateSync-GKR Overview
StateSync-GKR is a Rust GKR prover stack with a machine-checked Isabelle/HOL model and an explicitly partial, machine-
checked refinement layer toward the code, specialized for sparse-Merkle state transitions. The name deserves an immediate
disambiguation: StateSync here names the flagship workload—verifying transitions of a state tree in a bidirectional state-
synchronization system—and has nothing to do with the node snapshot or bootstrap mechanisms that some blockchain stacks call
“state sync.” The system has two layers, and the two-layer structure is deliberate.

The reusable core. The general layer is a GKR and sumcheck engine that is independent of the workload: a layered-circuit
intermediate representation with a three-kind gate set (linear, product, cube), a self-implemented multilinear sumcheck, the
GKR layer-reduction chain with two-point claim carrying, Fiat–Shamir transcript handling delegated to the underlying library’s
challenger, and a batching execution mode that prepares a circuit once and runs independent proving jobs against it. The engine
is built directly on five pinned crates of the Plonky3 toolkit [15] (field interfaces, the KoalaBear field, challenger, Poseidon2, and
symmetric primitives); the proof-system layers of that toolkit are not used. The cube gate is native because the production hash’s
S-box is 𝑥 3 ; keeping it a first-class gate kind keeps layer degree low without gate stacking.

The flagship specialization. The specialized layer compiles sparse-Merkle transition verification to the circuit IR: a fixed-depth
sparse Merkle tree over sequentially assigned keys, three-state leaves, Poseidon2 [10] as the in-circuit hash, an injective leaf pre-
image encoding, and a residual constraint encoding whose acceptance condition is “every output wire is zero.” The compilation
is data-parallel across tree levels, which is what makes the layer count depth-independent (section 5).

The mechanized development. The Isabelle/HOL development mirrors the two layers as two core sessions, with a four-session
chain above them (fig. 1). The session GKR_Protocol owns the general layer: circuits, multilinear extensions, sumcheck instances
built on the AFP entry [8], the assembly soundness bound, the wiring-oracle equivalence, batching, and the conditional refinement
from the shipped verifier’s acceptance trace to the assembly’s chain event. The session SMT_Circuit_Compiler_Correctness
owns the specialization: transition semantics, the compiler constraint model, the acceptance equivalence, the composition theorem,
and the concrete instances over the production field (KoalaBear, 𝑝 = 231 − 224 + 1). On top of it, four sessions in a linear chain
build the exact degree-four extension of that field and carry the assembly bound to it. Twenty theories across six registered
sessions build without sorry or oops, and no theory sits outside the registered sessions. The naming is tool-neutral by policy:
the sessions carry the names of their mathematical content, not of the product or the toolkit. (In session and fact names, SMT
abbreviates sparse Merkle tree, not satisfiability modulo theories.)

The implementation and its connection. The Rust workspace implements the same two layers as separate crates with an
enforced dependency direction: the sumcheck and protocol crates cannot depend on the compiler crate, so workload assumptions
cannot leak into the reusable engine. The connection between code and model is an explicit refinement layer (section 9):
Creusot [4] contracts anchor code clauses to model clauses for the compiler, the sumcheck engine, the protocol assembly, and
StateSync-GKR: Mechanized Trust Chain                                                                                                   4

                                                  AFP: Sumcheck_Protocol

GKR_Protocol — general layer (workload-agnostic)

                           Layered_Circuit        Multilinear_Extension          Sumcheck_Instance

                              Wiring_MLE       GKR_Assembly       Layer_Representative          GKR_Batching

                   Verifier_Acceptance_Refinement

                                                                                    imports

                            SMT_Semantics        Compiler_Model          Compiler_Correctness          Leaf_Fold

                             Composition        KoalaBear_Field          Compiler_Instance       Composition_Instance

                             SMT_Circuit_Compiler_Correctness — sparse-Merkle specialization, concrete instances

                                                                    imports

                      KoalaBear_Ext4_Nonsquare         KoalaBear_Ext4_Field          KoalaBear_Ext4_Lift           KoalaBear_Ext4_GKR

                                           four sessions — exact degree-four extension field, in the order shown

Figure 1: The session architecture. The general session depends on the AFP sumcheck entry and knows nothing about sparse
Merkle trees; the specialized session imports it and adds the semantics, the compiler model, the composition, and the concrete
instances; four sessions above it build the exact degree-four extension field and carry the assembly bound to it. Theory-to-session
placement is finalized against the released artifact.


the hash interface, under a declared trust surface. The refinement is partial—we state its exact coverage and its tool-imposed
ceiling—and nothing in this paper’s headline claims depends on pretending otherwise.

What is verified, and what is not. Verified, at the model level: compiler correctness, the GKR chain-event soundness bound,
their composition, batching preservation, leaf-encoding injectivity, wiring-oracle equivalence, and the satisfiability of every
assumption set by concrete production-field instances. Checked, at the implementation level: the machine-checked portion of
the refinement contracts, plus the test, format, and lint gates of the artifact. Also verified, at the model level: the transfer of the
assembly bound to the exact degree-four extension field, and the conditional refinement from the shipped verifier’s acceptance
trace to the chain event. Not claimed: whole-program verification of the Rust code, an unconditional executable acceptance-to-
event bridge, the distribution of the implementation’s derived challenges, verification of the underlying library primitives, security
of Fiat–Shamir, zero-knowledge, knowledge soundness, performance superiority, or downstream settlement and deployment.
Section 11 states the full boundary.

    KoalaBear instances (nonvacuity)                               AFP Sumcheck_Protocol (imported)


          Transition semantics compile      Layered circuit      prove           GKR protocol                      Bounded model
              smt_valid                    residual encoding              layer reduction + sumcheck                 chain event


                Theorem A: acceptance ←→ smt_valid                                    Theorem B: false-output event bound


                                         Theorem C: semantic invalidity =⇒ bounded model event

Figure 2: The mechanized model chain. Theorem A binds circuit acceptance to transition semantics; Theorem B bounds the GKR
model’s bad-chain event for a false output claim; Theorem C transfers semantic invalidity to that bound. The running-verifier
bridge is a separate conditional theorem with an undischarged value-correspondence premise, not part of these three. Concrete
KoalaBear instances witness every assumption set.
StateSync-GKR: Mechanized Trust Chain                                                                                                 5

4     Sparse-Merkle Transition Semantics
The first link of the chain is a mathematical definition of what the system is allowed to believe when it believes a transition. This
section fixes the state structure and the validity predicate; everything later either preserves this predicate or bounds the probability
of pretending to.

4.1   Trees, Keys, and Leaves

The state is a sparse Merkle tree of fixed depth 𝑑; the intended deployment instantiates 𝑑 = 24 as a genesis parameter, with larger
depths available by versioned re-instantiation instead of in-place migration. Keys are sequentially assigned asset identifiers, so
the populated key space is a dense prefix; non-membership queries concern the sparse remainder and, through the tombstone state
below, retired slots inside the prefix.
A leaf is in one of three states: empty (never populated), occupied with a payload, or tombstone (populated, then retired). The
three-state design is load-bearing for non-membership: retiring an asset must not make its slot indistinguishable from a never-used
slot, or historical uniqueness arguments collapse. In the formal model the leaf state is a datatype with the three constructors, and
the encoding tags them with field elements 0, 1, 2 respectively.

4.2   Hashing and the Leaf Encoding

In-circuit hashing is Poseidon2 throughout. Internal nodes hash by truncated permutation: the children’s digests are concatenated
and one permutation is applied, of which the first lanes form the parent digest. Leaves are hashed by a rate-8 sponge over an
explicit pre-image encoding, leaf_fold: the encoded leaf payload is laid out as [tag, len, payload verbatim, 0-padding] into a
fixed width that is a multiple of the sponge rate.
The two-mode design (compression for nodes, sponge for leaves) follows the standard discipline that a compression function
alone is not collision-resistant on variable-length inputs; the leaf pre-image encoding is what makes the leaf hash safe to treat as
a binding commitment. That claim has a precise combinatorial core, which we prove:
Lemma 4.1 (Leaf-fold injectivity). For encodings 𝑒 1 , 𝑒 2 with lengths in {1, . . . , max}, assume that the natural-number embedding
is injective on {0, . . . , max}: of_nat(𝑎) = of_nat(𝑏) implies 𝑎 = 𝑏 for 𝑎, 𝑏 ≤ max. If leaf_fold(𝑒 1 ) = leaf_fold(𝑒 2 ), then
𝑒 1 = 𝑒 2 . Consequently, a collision of the leaf hash ℎleaf = sponge ◦ leaf_fold on distinct in-bound encodings yields a collision
of the sponge on distinct pre-images.

The proof runs through the length lane: len is embedded by of_nat, and the stated injectivity premise forces equal lengths, then
equal verbatim segments, then equal tags. A sufficient condition over a field is max < char(F); the weaker-looking condition
max < |F| would be insufficient over extension fields. KoalaBear is prime, so max ≪ char(F) discharges the premise. Empty
and tombstone leaves are not special cases outside the fold: their encodings are the one-lane vectors [0] and [2], respectively,
and therefore lie in the same in-bound domain. The development also supplies a toy collision for a deliberately weak sponge,
demonstrating that the theorem is a reduction rather than a cryptographic hardness proof.
The lemma’s role in the architecture is worth making explicit. Theorem A below is a deterministic equivalence in which the hash
functions are abstract locale parameters; collision resistance does not appear in its statement. Where collision resistance matters is
one level up, when a consumer wants the root to bind a unique state; theorem 4.1 is the mechanized link that reduces that question,
for leaves, to the collision resistance of the sponge construction (and from there, by the standard sponge argument outside this
development, to the underlying permutation). Keeping the reduction separate from the equivalence keeps each statement exactly
as strong as its proof.

4.3   Operations and Validity

Three operations are formalized: membership (a key holds an occupied leaf with a claimed payload under the claimed root),
non-membership (a key’s leaf is empty or tombstone under the claimed root), and update (the tree moves from a pre-root to a
post-root by changing one leaf, with both path recomputations correct). The validity predicate smt_valid(op, 𝑟, 𝑟 ′ , 𝑤) takes
the operation, the claimed roots, and a witness 𝑤 containing the leaf data and the authentication path; it holds when the path
recomputation from the leaf through the key’s bit path reproduces the claimed root(s) and the leaf state matches the operation’s
requirement. The formal definitions transcribe the implementation’s semantics module clause by clause; the refinement layer
(section 9) is what turns that transcription discipline into checked anchors.

5     Circuit Compilation and Semantic Preservation
The compiler is where meaning is most easily lost, so it is where the verification effort begins. This section describes the circuit
model, the compilation scheme, and the equivalence theorem.
StateSync-GKR: Mechanized Trust Chain                                                                                                  6

5.1   Layered Circuits with a Three-Kind Gate Set

A circuit is a list of layers; a layer is a list of gates plus a constants vector and a width parameter 𝑠 (the layer holds 2𝑠 wires). A
gate is a record (kind, out, in1 , in2 , 𝑐) with kind ∈ {Lin, Mul, Pow3} and coefficient 𝑐; unary kinds obey the convention in2 = in1 ,
which the model’s well-formedness predicate enforces exactly as the implementation’s validator does. Layer evaluation initializes
the layer’s wires with its constants and then accumulates, for each gate, 𝑐 · 𝑔(𝑣(in1 ), 𝑣(in2 )) onto wire out, where 𝑔 is the kind’s
semantics. Two modeling decisions here were forced by fidelity to the implementation rather than by proof convenience. Gates
form a list, not a set: the implementation accumulates with +=, so a duplicated gate contributes twice, and a set-based model
would prove theorems about a different machine. And accumulation is additive with per-gate coefficients, which is what makes
the residual encoding below natural.
Acceptance is a zero test: circuit_accept holds when every wire of the output layer evaluates to zero.

5.2   The Residual Encoding

The compiler emits, for a transition claim, a circuit whose output wires are residuals: quantities that are zero exactly when a
constraint holds. The constraint families are:

• Hash-chain constraints: the leaf sponge chain and the 𝑑-stage compression chain up the authentication path, with the key’s bits
  selecting sibling order through multiplexers built from Mul gates;
• Booleanity residuals 𝑏(𝑏 − 1) for each key bit 𝑏;
• Tag residuals, e.g. tag(tag − 2) forcing a non-membership leaf’s tag into {0, 2} (empty or tombstone);
• Boundary residuals equating the recomputed root(s) with the public claimed root(s) and binding the claimed value digest.

Because the tree levels are data-parallel—every level runs the same hash template over different wires—the compiled circuit’s
layer schedule is determined by the hash’s round structure rather than by the authentication-path depth. The artifact’s preserved
development measurements report 118 layers for the Poseidon2 instantiation across 𝑑 ∈ {24, 28, 32}; increasing depth changes
layer width in those measurements, not layer count. This is a recorded structural observation, not a new measurement at the
release or a current test-suite assertion. The regular wiring also supports the succinct oracle of section 6.

5.3   Theorem A: Acceptance Equals Validity

The compiler model is a deep embedding at the level of meaning blocks: the emitted constraint families above, composed exactly
as the implementation composes them, with the hash sub-circuits abstracted behind the same interface as the semantics’ hash
functions. The division of labor is deliberate and worth stating: the model fixes the constraint families and their composition; the
concrete layer schedule (including the depth-independent layer count of section 5) is produced by the implementation’s builder,
recorded in development measurements, and related to the model through the R1 correspondence of section 9 rather than by the
theorems of this section. The equivalence is proved in both directions, over a verifier model verifier_accept that conjoins the
public-side checks the running verifier performs (public-input well-formedness, claimed-root echo, witness length) with circuit
acceptance.
Theorem 5.1 (Compiler soundness; mechanized as theorem_A_soundness). If verifier_accept holds for the compiled
circuit of (op, 𝑟, 𝑟 ′ ) with witness 𝑤, then smt_valid(op, 𝑟, 𝑟 ′ , canon(op, 𝑤)).
Theorem 5.2 (Compiler completeness; mechanized as theorem_A_completeness). If smt_valid(op, 𝑟, 𝑟 ′ , 𝑤), then the com-
piled circuit accepts the canonical witness encoding of 𝑤.
Corollary 5.3 (Packaged equivalence; mechanized as theorem_A_compilation_soundness). verifier_accept for the
compiled circuit holds for some witness iff ∃𝑤. smt_valid(op, 𝑟, 𝑟 ′ , 𝑤).

Two features of the statements repay attention. The soundness direction produces a canonical witness: for membership, the
leaf is canonicalized to the occupied state with the bound value, since the circuit binds the leaf through the value digest and
the leaf-content question is exactly the collision question that theorem 4.1 reduces to the permutation. This keeps the theorem
free of cryptographic assumptions while conceding nothing the circuit actually enforces. And the equivalence is packaged in the
existential form (∃𝑤) that the composition theorem consumes, so the composition in section 7 is an application, not a re-proof.
Completeness deserves its parity of esteem. For a system whose downstream effects trigger on proof issuance, a compiler that
rejects valid transitions is a liveness failure with the same operational cost as a soundness failure has in the other direction; proving
both directions is what earns the word “equivalence.”
StateSync-GKR: Mechanized Trust Chain                                                                                                  7

6     Machine-Checked GKR Protocol
The protocol layer receives a layered circuit and must deliver a probability bound. This section presents the formalization in the
order of its dependency structure: the layer identity, the per-round soundness import, and the chain-event induction that yields the
assembly bound.

Formal setting. The soundness statements are made against an arbitrary prover strategy: nothing is assumed about how
the prover’s messages arise, and the probability is over the verifier’s public-coin challenges alone, drawn uniformly and
independently—the mechanized statements, following the imported AFP development, phrase this as the uniform probability
mass function over challenge tuples. The model verifier receives the transition claim, the public values, and the full input
vector (the encoded witness); no succinctness in the witness is claimed, and the succinctness of section 6.4 concerns the circuit
description. What the theorems bound is an explicitly defined chain event, introduced in section 6.3; the connection between the
running verifier’s checks and this model event is a refinement-layer obligation, stated as such where it arises.

6.1   Multilinear Extensions and the Layer Identity

For a layer of width 2𝑠 , the layer’s value vector 𝑉𝑖 and the wiring predicates of each gate kind are extended to multilinear
polynomials over F in the standard way (the unique multilinear polynomial agreeing with the function on the Boolean cube,
expressed as an equality-kernel weighted sum). The reduction of one layer’s claims to the next rests on an algebraic identity.
Claims are carried as (point, coefficient) pairs {(𝑧 𝑘 , 𝑐 𝑘 )} whose asserted combined value seeds the layer’s sumcheck target; for
such claims against layer 𝑖, the integrand over the next layer’s values
                       ∑︁ h                                                                                             i
          𝑃𝑖 (𝑥, 𝑦) =            f 𝑘 , 𝑥) 𝑉𝑖+1 (𝑥) 𝛽(𝑦) + mul(𝑧
                            𝑐 𝑘 lin(𝑧                                                           𝑘 , 𝑥) 𝑉𝑖+1 (𝑥) 3 𝛽(𝑦)
                                                               g 𝑘 , 𝑥, 𝑦) 𝑉𝑖+1 (𝑥) 𝑉𝑖+1 (𝑦) + pow3(𝑧
                         𝑘

satisfies                                       ∑︁                          ∑︁                              
                                                              𝑃𝑖 (𝑥, 𝑦) =        𝑐 𝑘 𝑉𝑖 (𝑧 𝑘 ) − c
                                                                                                  onst(𝑧 𝑘 ) ,
                                          ( 𝑥,𝑦) ∈ {0,1} 2𝑠                 𝑘
                                      Í
where 𝛽 is the standard lifting with 𝑦 𝛽(𝑦) = 1 and c
                                                     onst extends the layer’s constants vector. The identity is proved from the
Boolean-point agreement and sum-linearity of multilinear extensions, and it is the completeness half of the layer step: an honest
prover’s claims survive the reduction.

6.2   Per-Round Soundness by Import

Each layer runs a sumcheck over 𝑃𝑖 in 2𝑠 variables. We do not re-prove sumcheck soundness. The general session’s locale for
the layer sumcheck is built on the AFP entry for the sumcheck protocol [8], whose inductive soundness theorem bounds, for an
𝑛-variable instance with per-variable degree bound 𝑑 ∗ , the probability that the verifier accepts a false sum by 𝑛 · 𝑑 ∗ /|F|. Our
proof obligation is the instance correspondence: exhibiting the layer integrand as an object of the AFP development’s polynomial
type with the right variable count, degree bounds, and evaluation behavior—kept minimal so that every connecting assumption is
dischargeable at the concrete instances (a point section 8 returns to, since exactly this obligation is where a vacuity defect hid).
Making the degree obligation dischargeable required one genuine generalization. The chain-level statements are parametric in
a per-layer degree-bound function db(𝑠) in place of a single constant: the AFP-shipped concrete polynomial instance measures
total degree, under which the hypercube-faithful representative of the integrand has degree growing with 𝑠 (the mechanized
representative satisfies deg ≤ 2𝑠), while the implementation’s per-variable view works with the constant 4. Both are recovered
from the same theorems—the degree-four reading as a corollary by specializing db, the total-degree reading by instantiating
db(𝑠) = 2𝑠 with the mechanized representative—so the formal statement serves the implementation and the available formal
instance without privileging either. The nonvacuity status of the two readings differs, and we state it rather than blur it: the
registered activation instances discharge the degree premises via the total-degree representative, while the degree-four reading
is a statement-level specialization documenting the implementation-facing form of the bound—no polynomial instance for the
per-variable measure is registered, and table 1 marks the corollary accordingly.

6.3   Two-Point Carry and the Chain Event

After a layer’s sumcheck, the verifier holds evaluation claims about the next layer’s polynomial at two points (𝑥 ∗ , 𝑦 ∗ ); the protocol
carries them as the claim list [(𝑥 ∗ , 1), (𝑦 ∗ , 𝑟)] with a fresh challenge 𝑟 combining them. The final layer carries no recursion: the
input layer’s claim is checked by the verifier directly against the multilinear extension of the input vector, which the model verifier
holds in the clear (Formal setting above).
Soundness of the whole chain is proved over an explicitly defined chain event Bad𝑖 in the model, defined by recursion over the
remaining layers:                                                                    
                                      Bad𝑖 = AFPAccept𝑖 ∨ carry𝑖 false ∧ Bad𝑖+1 ,
StateSync-GKR: Mechanized Trust Chain                                                                                             8

where AFPAccept𝑖 is the imported sumcheck development’s acceptance event for layer 𝑖’s true integrand and carry𝑖 false says the
two carried evaluations disagree with the next layer’s true polynomial. At the last layer, the continuation disjunct is absent and
only the sumcheck acceptance event remains. The running verifier separately checks the final input multilinear evaluations; the
acceptance refinement uses those checks to exclude a false final carry. Under its stated value relation, an accepted running trace
implies this model event (sections 9 and 11). The small probability bound applies when the claimed output table differs from the
true output; its leading term accounts for collisions in the random output seeding.
Theorem 6.1 (Assembly soundness; mechanized as gkr_assembly_soundness). For a well-formed layer chain with widths
2𝑠𝑖 and a degree-bound function db admissible for the layer representatives, if the output claim is false, the probability (over the
verifier’s challenges, drawn uniformly from F) of the chain event is at most
                                                            Í                  
                                                    𝑠out + 𝑖 2𝑠𝑖 · db(𝑠𝑖 ) + 1
                                                                                 ,
                                                                 |F|
where the leading term accounts for the output-claim seeding and the per-layer terms combine the imported sumcheck bound with
the two-point carry loss.
Corollary 6.2 (Degree-four specialization). With db = 𝜆𝑠. 4, the bound specializes to the constant-degree form matching the
implementation’s per-variable round degree.

This corollary is a statement-level specialization (section 6): its premises are not discharged by the registered total-degree
instances, and it carries no activation witness of its own.
The proof is an induction over the layer chain with a union bound, assembled from the imported per-round theorem, a probability-
splitting toolkit over challenge tuples, and the multilinear agreement bound for the output seeding. The field is a theorem
parameter. Registered interpretations instantiate the GKR locale both at the KoalaBear base field and at its exact degree-four
extension. The latter establishes the assembly bound over a field of cardinality 𝑝 4 . Reading that denominator as a security bound
for the running verifier additionally requires the stated challenge-distribution and code-correspondence hypotheses, including an
applicable Fiat–Shamir reduction; the field construction does not supply them.

6.4   A Succinct Wiring Oracle, with Its Own Theorem

A verifier that must read the full gate list of each layer forfeits succinctness. Because the compilation is data-parallel, each
layer’s wiring decomposes into a few arithmetic-progression families plus a sparse residue, and the implementation derives a
closed-form oracle that evaluates the wiring extension from that decomposition. The equivalence of the derived oracle with the
defining table form is itself a mechanized lemma: if the family expansion plus residue reproduces the layer’s gate multiset exactly,
then the derived and table extensions are the same polynomial. The multiset hypothesis is precisely what the artifact’s repartition
tests (exact multiset-equality checks of the family expansion against the gate list) pin down, and the lemma localizes trust: the
derivation algorithm itself needs no verification, since any output passing the multiset check is correct by the lemma, and the
implementation falls back to the table form otherwise. One dependency remains on the Rust side of the boundary and is declared
as such: the runtime check-and-fallback logic that licenses the derived oracle is implementation code under the partial refinement
of section 9, and the table-form fallback does not depend on it.

7     Model-Level Composition
The two halves meet in a locale that merges the compiler model with the protocol model, identifying the circuit’s field with the
challenge field. The composition theorem transfers semantic invalidity to the protocol model’s bounded chain event. It does not
itself identify that event with the running verifier’s acceptance predicate.
Theorem 7.1 (Model composition soundness; mechanized as theorem_C_composition). In the merged locale, for a transition
claim (op, 𝑟, 𝑟 ′ ) whose compiled circuit forms a well-formed layer chain: if the public-side checks pass and no witness makes the
transition valid, then the probability of the chain event for the compiled circuit with the zero-output claim is at most
                                                             Í                   
                                                     𝑟 out + 𝑖 2𝑠𝑖 · db(𝑠𝑖 ) + 1
                                                                                   ,
                                                                  |F|
where 𝑟 out is the width in bits (the base-two logarithm of the wire count) of the residual output layer, namely
length(descs(kind_of(op))). The layer therefore has 2𝑟out wires. This is the compiled-chain counterpart of the logarith-
mic output-width term 𝑠out in theorem 6.1. The theorem bounds the model event under semantic invalidity; obtaining an
acceptance-implies-validity statement for the executable verifier additionally requires the transcript-to-event refinement described
in sections 9 and 11.

The proof composes the contrapositive of theorem 5.1 (no valid witness forces the true output off the zero table) with theorem 6.1;
the packaging of theorem 5.3 is what lets the composition consume the compiler equivalence without re-opening it. Two
StateSync-GKR: Mechanized Trust Chain                                                                                                 9

hypotheses stay explicit instead of being absorbed: the chain well-formedness of the compiled circuit is an instantiation obligation
discharged at concrete stacks (it is structural, about fan-in ranges and width agreement, and the concrete instances discharge it),
and semantic invalidity is the absence of any valid witness. The theorem bounds the resulting model event and deliberately makes
no knowledge-extraction claim.
This is the paper’s central model statement in its exact strength. The deterministic compiler equivalence and the probabilistic GKR
assembly are composed in one proof assistant, so the gap inside the model no longer contains an informal semantics-to-circuit step.
The remaining gap is narrower but material: the running transcript must refine the model chain event, and the base/extension-field
split must refine the model’s single-field instantiation. Both remain visible in section 11.

8     Batching and Concrete Nonvacuity
8.1   Batching Preservation

The deployment workload proves the same circuit shape repeatedly, so the execution mode that matters is: compile once, prepare
once, then run many independent proving jobs. The batching theorem says this mode changes nothing semantically.
Theorem 8.1 (Batching preservation; mechanized in GKR_Batching). With batch_prove = map prove over an operation list
(the model’s batch prover is literally this map; compilation caching is an implementation-level optimization whose meaning-
invariance is part of the refinement obligation) and batch_verify the conjunction of individual verifications, batch verification
of batch proofs is equivalent to individual verification of individual proofs, preserving each operation’s accept/reject outcome.

The theorem is generic in the prove and verify functions, so the implementation’s prepared-batch scheduler re-instantiates it
without re-proof. Its nonvacuity instance runs a two-job batch with one accepting and one rejecting member. The theorem’s
content is the preservation contract for the batching interface: it pins the semantics the scheduler must refine, and the claim that the
shared-preparation path realizes this semantics belongs to the refinement layer, deliberately not absorbed into the theorem. The
scope is exact: this covers independent-job batching with shared preparation. Cryptographic proof aggregation and cross-proof
amortization are different mechanisms and are not claimed.

8.2   Nonvacuity as a Checked Property

A mechanized theorem quantified over a locale is a conditional statement: if the assumption set is satisfiable, the theorem has
content. The proof assistant checks the implication, never the satisfiability. This development treats satisfiability as a first-class
proof obligation—every locale must be witnessed by a concrete instance registered in the build, and every headline theorem must
be accompanied by an activation instance that actually fires its premises—and the discipline earned its cost during the audit.
Two defects illustrate. First, a clean build with zero sorry contained a compiler-model assumption set that was unsatisfiable:
the specification equations force both specification-vector lengths to be powers of two, yet the two lengths provably satisfy
lenro < lenup < 2 lenro , and no two distinct powers of two fit strictly within a factor of two—so no model satisfied the assumptions,
and both compiler-side headline theorems were vacuously true. The repair (padding the specification vectors to the evaluator’s
power-of-two width, matching what the implementation’s builder actually emits) survived every downstream proof unchanged;
nothing but the instance construction would have found the defect, since no build signal distinguishes a vacuous theorem from a
contentful one. Second, the degree obligation of the sumcheck import was stated with a single constant bound over all widths,
which no pair of representative and constant could discharge against the AFP-shipped total-degree instance; the generalization
to a width-dependent bound function (section 6) was forced by the requirement that the premises be dischargeable, and the
mechanized 2𝑠-degree representative is what discharges them.
The registered compiler and composition activations use a depth-one toy hash stack over the production base field KoalaBear:
they witness satisfiable assumption sets and fire the compiler equivalence and composition premises without purporting to verify
the full Poseidon2 implementation. The batching activation runs one accepting and one rejecting job. Separately, the GKR locale
is interpreted over the exact degree-four extension field. These are distinct evidence classes. An instance file that is written but
not registered in a session has verified nothing; registering three such files surfaced latent proof defects that their existence had
concealed. The development’s completion criterion combines a green build, no admitted proof, registered interpretations, fired
premises, and rendered disclosure.

9     Relationship to the Rust Implementation
The model-level results of sections 4 to 7 are about mathematical objects. The artifact ships code. This section states, exactly,
how the two are connected—what is machine-checked, what is declared, and where the current tooling stops. The refinement
discipline follows one rule throughout: a contract clause exists only if it has a clause-level anchor in the model, so the contracts
can over-approximate trust but never over-claim correspondence.
StateSync-GKR: Mechanized Trust Chain                                                                                                10

9.1   Structure of the Refinement

The refinement layer consists of Creusot [4] contracts (checked via Why3 [6] and SMT solvers) over four obligation families,
mirroring the theorem structure: R1 anchors the compiler crate to the circuit-acceptance definitions of Theorem A; R2 anchors
the sumcheck engine and layer reduction to Theorem B’s chain, including a contract mirroring the AFP protocol’s round-step
law on the oracle interface; R3 anchors the composition facade to the merged locale; R4 confirms that the hash-gadget interface
matches the model’s hash-function usage—interface correspondence only, with no claim about hash values, whose computation is
the underlying library’s. Two trait-level contracts (an oracle view with a binding law, and an index-domain precondition mirroring
the model’s layer-indexing domain) were added as verification-only annotations under a frozen-interface discipline: they compile
only for the verifier, change no production semantics, and were the sole such extensions admitted.
R2 subsequently tightened in a way worth stating precisely, because it changes what the tool sees rather than what the code does.
The sumcheck and per-layer verifier bodies had been opted out of translation whole; each opt-out was narrowed to the single
foreign-field equality that forced it. Round counting, degree checks, rejection paths, transcript order, carry construction, and
the final claim are now ordinary translated code rather than trusted text. The bodies themselves are unchanged, so the program
identity is unchanged; what moved is the size of the declared trust surface.

                                                 R1–R4 Creusot contracts
                 Isabelle/HOL model                                                       Rust workspace
                                                 clause-by-clause anchors
                Theorems A–D, lemmas                                         compiler · sumcheck · protocol · batching
                                                 machine-checked portion


            37 reported development probes                           black boxes: p3-field · p3-challenger · p3-poseidon2
            (not a packaged public test suite)                          · p3-symmetric · p3-koala-bear · Rust/LLVM · OS




                          declared R1–R4 trust surface: trusted annotations classified per obligation
                                      · 1 tool-artifact axiom · 3 uninterpreted symbols

Figure 3: The explicit partial-refinement boundary. Contracts anchor code clauses to model clauses; the declared trust surface
and the library black boxes are stated, not hidden.


9.2   The Verifier-Acceptance Refinement

The contracts of the previous subsection connect code clauses to model clauses one clause at a time. A separate result connects an
entire successful run. In the general session, the verifier that ships in the artifact is given a trace type recording what it observed—
the public-input binding, the request guard, the zero-output check, the protocol result, and the final input-MLE comparisons—and
a theorem proves that a trace the verifier accepts inhabits the reduction-chain event of theorem 6.1.
The theorem is conditional, and the condition is the point of it. It carries a named relation between the running values and the
model objects as an explicit premise: a hypothesis stating that the trace’s field elements, layer data, and claims are the model’s,
under the intended reading. That premise is not discharged against the compiled program; discharging it is exactly the value-level
correspondence the contract layer reaches only in part. We therefore describe the result as a refinement that is mechanized in its
implication and conditional in its hypothesis, and the theory says so in its own preamble rather than leaving a reader to infer it.
The direction of the theorem matters. The model chain event does not contain the running verifier’s public-input and request
guards. A separate non-claim lemma assumes that event and shows rejection of a trace whose public-input binding guard is false;
it does not construct an instance of the bad event or establish its converse. The forward theorem remains conditional on the value
relation, and the chain-event bound remains probabilistic. Those are the reasons it does not constitute unconditional executable
acceptance-implies-validity. The theory’s shipped-body predicate names a source correspondence, not production readiness.

9.3   The Machine-Checked Portion and the Trust Surface

The machine-checked portion covers structural, typing, arithmetic, indexing, and domain clauses across the four families. We do
not turn this heterogeneous set into a headline percentage: the source contracts and committed replay records expose the proof
dispositions, and a ratio would depend on how clauses are split. The R1–R4 trust surface is classified as follows:

• trusted annotations classified per obligation, of which the only claim-bearing ones sit at the declared black-box boundary
  (foreign field-element equality/cloning, the hash-gadget interface, one encoding-determinism graph); every other in-scope
  annotation is a translation opt-out carrying no specification. A raw current-tree attribute count is not used because later
  integration code contains additional annotations outside R1–R4;
StateSync-GKR: Mechanized Trust Chain                                                                                                11

• 1 logic axiom, of a tool-artifact class: foreign_zero_wf, asserting well-formedness of the foreign field type’s zero element—
  the activation of an axiom the tool itself emits behind a false guard;
• 3 uninterpreted logic symbols for the abstract hash functions, carrying no claims;
• a small set of extern_spec declarations, each a standard-library fact or claim-free.

At the revision this paper describes, the committed replay inventory contains 331 proof.json files. A recursive census over
their proof trees finds 2421 discharged leaves and 179 open ones. The sumcheck set (34 files) has no open node. The current
verification-owner set (20 files) has two, both type-invariant leaves bound to the source and task types, which carry no claim
and are named as open in the artifact’s scope record; the set includes the acceptance-trace integration. The remaining 177 open
nodes lie across the broader compiler, primitives, and protocol inventories. Those nodes are the partial-refinement and tool-wall
dispositions described above; file or node counts are not used as a coverage denominator. The obligation ledger, not a percentage,
determines which code-to-model claims the paper owns.
The development journal records 37 falsification probes: deliberate distortions of contract clauses in isolated builds, each reported
as rejected by the checker. It also records two review passes independent of the authoring passes. These are historical development
checks, not a formal external security audit or a probe suite distributed with the public package. The public artifact provides the
contract sources and committed replay metadata, which expose the declared proof dispositions. Production tests, lint, format, and
the frozen-interface check supply separate evidence.

9.4   The Tool Ceiling, Stated Honestly

The unchecked remainder is not a backlog of unfinished proofs; it is a measured boundary of the current toolchain, established
by attempting each blocked obligation through code adjustment, tool upgrade, and contract restructuring, and failing through all
three. The wall classes: monolithic verification conditions for vectors of foreign elements that no available solver splits; hard
translation errors where comparison traits demand a deep model that foreign types cannot be given; specification gaps for iterator
adapters that surface as hard errors; and constructor-as-function references the translator rejects. Rewriting the core to evade the
walls was considered and declined—the production code stays idiomatic, and verification pressure does not get to deform a frozen
interface. The blocked value-level clauses are covered by documentation contracts—contract text anchored to the same model
clauses but not machine-checked, counted inside the declared trust surface above rather than toward the machine-checked portion.
We state the resulting claim precisely: the artifact carries a fully mechanized model and a partial, machine-checked refinement
with an explicit boundary—and no whole-program verification claim.

10    Artifact and Reproducibility
Contents. The artifact comprises (i) the Isabelle/HOL development: six registered sessions, twenty theories, building on
Isabelle2025-2 with the AFP sumcheck entry as the sole AFP dependency; (ii) the Rust workspace: compiler, sumcheck,
protocol-assembly, and batching crates over five pinned Plonky3 crates, with the workspace dependency graph enforcing that the
general crates cannot see the specialization; (iii) the refinement layer: Creusot contract sources and replay artifacts; and (iv) the
test suite, including the repartition tests referenced by section 6, the differential cross-checks of the in-circuit hash against the
library’s native computation, and deterministic proof-byte regression.

Verification.   The headline check is a clean build of every registered session:

                      isabelle build -c -d /path/to/afp/thys -d formal/isabelle SESSION

for each of GKR_Protocol, SMT_Circuit_Compiler_Correctness, and the four extension-field sessions, with zero sorry
and oops across all twenty theories, and the session documents building to PDF. Because a theory that no session registers is
never checked at all, the artifact’s gate also requires that every theory file belongs to the ROOT of its own session; a build that is
green while a theory sits outside it is the failure mode this guards against. At the revision this paper describes, a fresh isolated
build of all six sessions, the full Rust workspace release suite (194 passed, 0 failed, 2 intentionally ignored), format and lint gates,
and byte-exact deterministic proof digests were re-verified. The two ignored tests are an intentional golden-vector generator and
a manual cold/warm prepared-material metric that requires an external path; neither is a correctness test silently skipped.
The Creusot/Why3 R1–R4 campaign reached the declared partial-refinement dispositions recorded during development. The
released source retains the contracts and committed replay metadata; the detailed historical falsification and internal-review
journal is not part of the public archive. Counts from that journal are reported as development evidence, without implying that
readers can reproduce those isolated probes directly from the published package or that the whole current program was verified.

Coordinates. The software is available at https://github.com/Oraclizer/statesync-gkr.   This paper is
bound to the verified signed tag v1.1.0, commit 1b8d2f829792172b347dedbfde969016c2c05789, archived as
StateSync-GKR: Mechanized Trust Chain                                                                                                12

doi:10.5281/zenodo.23136385. The immutable GitHub Release carries the exact source tar archive, fixed proof, public in-
puts, manifests, and checksums. Its two base-session document PDFs are snapshots from 2026-08-29; the tagged theory files are
the source for subsequent extension-field and acceptance results.

11    Limitations and Trust Boundary
Each boundary below is stated once, here, in its exact form; the results above are meant to be read with this section in view.

Model-level probability. The soundness statements (theorems 6.1 and 7.1) are about the model verifier, in an interactive
public-coin model with challenges drawn uniformly from the field, matching the imported AFP development. The Fiat–Shamir
transformation [5] that makes the running protocol non-interactive is outside the formal model. An implementation-facing security
claim would require an applicable multi-round reduction with explicit assumptions and quantitative loss. Round-by-round or
state-restoration soundness can support such a reduction, but neither is established here or required by every possible reduction.
No such reduction is part of this development, and we make no security claim about the non-interactive protocol. The implication
from the running verifier’s transcript checks to the model’s chain event now has a mechanized conditional form (section 9), whose
value-correspondence premise is stated in the theory and not discharged against the compiled program; below that premise the
boundary is still the contract surface, machine-checked where it reaches and declared where it does not.

Single-field composition versus extension-field execution. The composition locale uses one finite field for circuit values and
verifier challenges. The executable stack uses KoalaBear for circuit values and a degree-four extension for challenges. Two
of the three steps that separated the model from that execution are now mechanized. The extension is constructed as an exact
quadratic tower with its field instance and cardinality 𝑝 4 , and the base-field embedding, polynomial and multilinear-extension
preservation, circuit, well-formedness, and false-output lifting are proved along it, so the assembly bound holds over the exact
field the implementation uses and its denominator is exactly 𝑝 4 .
The third step is not mechanized and is the sharpest remaining boundary of this paper. The lifted statement assumes challenges
distributed as uniform extension elements. What we prove about that assumption is one implication in the convenient direction:
four independent uniform base-field coefficients push forward to a uniform extension element. Whether the implementation’s
transcript-derived samples satisfy the hypothesis of that pushforward is a question about the challenger and the Fiat–Shamir
construction, not about the field, and it is outside this development. Until it is settled, the 𝑝 4 denominator is a statement about the
model over the exact field, and the implementation-facing reading of it rests on an assumption we name rather than discharge.

Online sampling and input binding. A uniform coefficient tuple for one challenge does not establish that the full challenge
sequence remains fresh and uniform conditioned on prior messages. The executable uses one evolving Poseidon2 duplex whose
permutation is also used by other hashing operations; transferring the model bound requires an argument for its exact message
schedule and the adversary’s adaptive queries. Moreover, theorem 7.1 fixes the witness outside the challenge probability space,
whereas the executable does not directly absorb the witness-derived input vector before drawing challenges. A transfer must
therefore account for adaptive input selection or establish an adequate binding condition. The verifier recomputes a Poseidon2
accumulator chain and checks two final input multilinear evaluations, so the input vector is not freely selectable. This observation
is a missing argument, not a demonstrated false acceptance.

Library primitives. The underlying library’s field interfaces, KoalaBear arithmetic, challenger, and Poseidon2 with its
symmetric-primitive interface, together with the Rust compiler, LLVM, and operating system, are black boxes. R4 checks
interface conformance to the model’s hash usage; it does not verify hash computation.

Partial refinement. The refinement is partial with a stated ceiling (section 9). No whole-program verification of the Rust
implementation is claimed. The trust surface is enumerated; the claim-bearing portion is confined to the declared black-box
boundary.

Scope of the semantics. The mechanized semantics covers the three sparse-Merkle operations over three-state leaves at a fixed
genesis depth. This is a specialization by design, and the general session is workload-agnostic; arbitrary state-transition languages
are out of scope, and no claim is made beyond the formalized operations.

Completeness scope. Completeness is mechanized for the compiler (theorem 5.2, with theorem 5.1 making the equivalence)
and at the layer-identity level, where the honest prover’s claims survive each reduction (section 6). An assembled end-to-
end completeness theorem for the full protocol run is not part of this development; the deployment’s liveness rests on the
implementation’s tests.

Succinctness scope. The derived wiring oracle avoids materializing the full gate table when its repartition check succeeds. The
model verifier used in the soundness statement still holds the full input vector, so this paper does not establish an end-to-end
sublinear verifier for the private witness.
StateSync-GKR: Mechanized Trust Chain                                                                                         13

No zero knowledge, no knowledge soundness. The core protocol provides no zero-knowledge property, and none is claimed;
external wrapping layers that add it are outside this paper’s scope and outside its verification boundary. Theorem 7.1 reasons
from the absence of any valid witness to a bounded model event. Even after the executable acceptance bridge is supplied, the
corresponding semantic conclusion is existential and provides no extractor.

Downstream consumption. Everything after verifier acceptance—settlement, cross-system finality, deployment operations—is
out of scope. Even before that boundary, the executable acceptance-to-model-event bridge remains partial. The paper therefore
establishes a model-level composition and a bounded code connection, not a production-readiness claim for a larger system.

No performance claims. This paper reports no benchmark results and asserts no performance superiority. Systems-level
measurement under controlled conditions is separate work.

12    Related Work
The GKR lineage. The protocol originates with Goldwasser, Kalai, and Rothblum [9]; Thaler [18] gives time-optimal provers
for regular wiring, the regime targeted by our compilation, and Libra [20] achieves linear-time proving in general. The sumcheck
engine descends from Lund, Fortnow, Karloff, and Nisan [13], with polynomial identity bounds supplied by Schwartz [16].
This development proposes no new protocol design; it machine-checks the model transcription, wiring identities, and compiler
composition.

Mechanized proof-system theory. The AFP sumcheck entry [8] and its accompanying analysis [7] provide our direct per-
round foundation. Their discussion of downstream sumcheck-based protocols motivates the GKR layer assembly developed
here. ArkLib [19] formalizes interactive oracle reductions and sumcheck in Lean 4. Bailey and Miller [3] mechanize linear-PCP
SNARK soundness in Lean under the algebraic group model. These provide protocol-level results in their respective settings; the
compiler-to-GKR composition and conditional Rust connection are the objects studied here.

Verified implementations and verified encodings. Almeida et al. [1] connect EasyCrypt security proofs for MPC-in-the-Head
zero knowledge to verified executable code. That result provides a stronger executable connection in a different protocol family
than the partial bridge claimed here. A second line checks deployed proof-system encodings against execution semantics: the
S-two AIR in Lean [2], SP1 Hypercube instruction constraints against the RISC-V Sail specification [17], Jolt lookup semantics in
ACL2 [11], extraction of Plonky3 constraint systems into Lean [14], and refinement-type certification of Coda reimplementations
of Circom circuits [12]. Theorem A occupies that semantics-to-constraint axis. Our additional object is a GKR assembly model
in the same proof assistant, consumed by Theorem C. The executable prover remains separate evidence connected through the
conditional and partial refinement; this comparison does not establish absence of all other mechanized GKR developments.

Implementation refinement. Creusot [4] and Why3 [6] supply the contract toolchain used against the Rust source. The
contribution on this axis is the explicit account of checked clauses, undischarged obligations, trust surface, and measured tool
limits for this artifact, rather than a claim that contract verification of proof-system code has no precedent.

13    Conclusion
A GKR verifier’s acceptance begins as a claim about a circuit. This paper machine-checks the model-level route from sparse-
Merkle transition semantics to the bounded bad-chain event of a GKR assembly: a compiler equivalence in both directions, a chain
soundness bound built on the AFP sumcheck entry, and a composition theorem that transfers semantic invalidity to that bound.
It does not claim that the executable route is closed, but two of the gaps it once listed have narrowed to named hypotheses. The
bound now holds over the exact extension field the implementation uses, leaving the distribution of the derived challenges as the
residual assumption; and the shipped verifier’s acceptance is related to the model event by a theorem whose value-correspondence
premise is stated rather than discharged. Fiat–Shamir and the remaining code correspondence stay in the stated trust boundary in
full. The development’s working disciplines remain part of the contribution: concrete activation exposed two vacuous headline
results hidden by a green build, the session split keeps the GKR model reusable, every theory is registered so that none escapes
the build, and the partial refinement makes the residual code assumptions auditable rather than implicit.
The general session is deliberately infrastructure: a machine-checked GKR assembly model that other workloads can specialize
by supplying their own compiler correctness theorem and inheriting the composition pattern. On the specialized side, the same
pattern can extend to richer transition semantics. The released artifact accompanies the paper, and its purpose is to let readers
distinguish the checked mathematical chain, the partially checked implementation bridge, and the unverified cryptographic and
operational boundaries.
StateSync-GKR: Mechanized Trust Chain                                                                                               14

Acknowledgments
We thank Bernhard Müller for his independent review of the verifier’s challenge-generation assumptions and the implementation-
facing interpretation of the extension-field soundness bound. His analysis clarified the distinction between the mechanized
field/model results and the remaining multi-round Fiat–Shamir and input-binding arguments, and informed the corresponding
claim corrections. Responsibility for the implementation and the remaining security arguments rests with the authors.

Artifact availability. The Isabelle sessions, Rust workspace, refinement contract sources, committed replay metadata, and
release verification scripts are publicly available at the signed v1.1.0 source revision, archived as doi:10.5281/zenodo.23136385.
Instructions for exact Release-asset verification are in REPRODUCING.md. The source is dual-licensed under MIT or Apache-2.0;
the software DOI identifies the artifact, not a journal publication of this paper.

A    Theorem Inventory

Table 1:         Mechanized results,      headline and supporting.    Session G = GKR_Protocol,           S =
SMT_Circuit_Compiler_Correctness, X = the four-session extension-field chain. Fact names are those of the devel-
opment; the full inventory accompanies the artifact.
 Result                        Mechanized fact                          Session   Statement (informal)
 Theorem A (soundness)         theorem_A_soundness                         S      acceptance ⇒ validity, canonical witness
 Theorem A (completeness)      theorem_A_completeness                      S      validity ⇒ acceptance, canonical path data
 Theorem A (packaged)          theorem_A_compilation_soundness             S      acceptance ↔ ∃𝑤. validity
 Theorem B (chain bound)       gkr_assembly_soundness                      G      theorem 6.1
 Theorem B (chain event)       gkr_chain_bad_bound                         G      per-chain union bound
 Theorem B (per-var. degree-   corollary of theorem 6.1                    G      db = 𝜆𝑠. 4; statement-level, not activation-
 4)                                                                               witnessed
 Theorem C                     theorem_C_composition                       S      theorem 7.1
 Theorem D                     theorem_D_batching_correctness              G      batch ↔ individual outcomes
 Leaf-fold injectivity         Leaf_Fold lemmas                            S      theorem 4.1 + collision reduction
 Wiring-oracle equivalence     Wiring_MLE lemmas                           G      derived = table extension
 Degree representative         Layer_Representative                        G      representative with deg ≤ 2𝑠
 Activation (compiler)         instance_theorem_A_activation               S      Theorem A fired on concrete round trip
 Activation (composition)      instance_theorem_C_activation               S      Theorem C premises fired concretely
 Verifier acceptance           verifier_acceptance_implies_                G      accepted trace inhabits the chain event
                               gkr_chain_bad
 Verifier        acceptance    production_verifier_acceptance_             G      same, for the shipped body; value relation is a
 (shipped)                     refines_gkr_chain_bad                              premise
 Converse non-claim            gkr_chain_bad_does_not_imply_               G      public-input guard failure forces rejection under an
                               public_input_acceptance                            assumed chain event
 Extension-field transfer      gkr_assembly_soundness_ext4                 X      theorem 6.1 over the exact degree-four extension
 Exact denominator             ext4_denominator_exact                      X      bound denominator is exactly 𝑝 4
 Coefficient pushforward       uniform_coeff_tuple_pushforward             X      four uniform base coefficients ⇒ uniform element



B    Assumption Ledger
• Fixed depth 𝑑: a genesis parameter of the instance; larger depths by re-instantiation.
• Abstract hashes: ℎleaf , ℎnode are locale parameters in Theorem A (deterministic equivalence; no collision assumption in its
  statement). Collision resistance enters only in the system-level reading of root binding, via theorem 4.1’s reduction.
• Interactive public-coin model: challenges uniform over F; Fiat–Shamir out of model.
• Field: statements are parametric in one finite field, and the registered nonvacuity instances of Theorems A and C are at the base
  field. The lift of the assembly bound to the exact degree-four extension is mechanized, so the extension-field cardinality is no
  longer an unmechanized step in the model; the implementation-facing reading additionally assumes that the derived challenges
  are distributed as the lifted statement requires.
• Challenge distribution: the extension-field statement assumes uniform extension elements. The mechanized pushforward
  supplies one direction only, from a jointly uniform tuple of four base-field coefficients. Freshness and conditional uniformity
  across the online challenge sequence, and the multi-round Fiat–Shamir transfer for the executable, are additional assumptions
  or arguments rather than consequences of the field construction.
StateSync-GKR: Mechanized Trust Chain                                                                                                   15

• Input binding: Theorem C fixes the witness before the challenge experiment. Applying it to adaptively selected witness-derived
  inputs requires a separate binding or security argument; the executable’s recomputed hash chain and final input checks must be
  included in that argument.
• Value correspondence: the verifier-acceptance refinement carries an explicit relation between the running trace’s values and
  the model objects as a premise. It is stated in the theory and not discharged against the compiled program.
• Degree admissibility: a representative of each layer integrand within db; discharged by the mechanized 2𝑠 representative (total
  degree). The degree-4 (per-variable) reading is a statement-level specialization with no registered instance (section 6).
• Chain well-formedness: fan-in ranges and width agreement of the compiled chain; an instantiation obligation, discharged at the
  concrete instances.
• Leaf length embedding: of_nat must be injective on {0, . . . , max}; max < char(F) suffices and is trivial at the prime production
  field. A cardinality-only premise would be insufficient over extension fields.
• Node-hash collision resistance: the system-level root-binding reading additionally assumes collision resistance of the truncated-
  permutation node hash; unlike the leaf side (theorem 4.1), no mechanized reduction is provided for it.
• Batching cache: theorem 8.1 is stated for the literal map; the meaning-invariance of the implementation’s shared compilation
  cache is a refinement-layer obligation.
• Library black boxes: p3-field, p3-koala-bear, p3-challenger, p3-poseidon2, p3-symmetric, Rust/LLVM, OS.

C    Compiler Correspondence Map

             Table 2: Model-to-implementation correspondence at the module level. Contract families per section 9.
       Model object                Implementation site   Refinement family                   Checked content
       Transition semantics        semantics module      R1                                  validity clauses, path recomputation
       Circuit model, acceptance   compiler crate        R1                                  gate/layer structure, residual emission
       Leaf encoding               hashing module        R1                                  fold layout, width, domain
       Sumcheck engine             sumcheck crate        R2                                  round structure, oracle laws, evaluation
       Layer reduction, carry      protocol crate        R2                                  claim threading, two-point carry
       Composition facade          facade module         R3                                  public-side checks, operation keying
       Hash-gadget interface       gadget trait          R4                                  interface conformance (no value claims)
       Batching                    batching crate        (re-instantiation of theorem 8.1)   order preservation, outcome equality



D     Assurance Summary
The development used clean session builds, registered assumption witnesses and premise activations, rendered disclosure checks,
and clause-level refinement accounting. Concrete activation exposed the two vacuity defects described in section 8.2. The historical
development journal records assumption-removal checks, 37 contract falsification probes, and internal reviews independent of the
authoring passes; that journal is not distributed with the public archive. The public package exposes the mechanized statements,
contract sources, committed replay metadata, tests, and exact release verifier. The reported Isabelle build and Rust test results are
also visible in the repository’s hosted CI. These evidence classes establish the stated model and partial-refinement results without
constituting a formal external security audit.

E    Verification Commands

    Check                      Command
    General session            isabelle build -c -d /path/to/afp/thys -d formal/isabelle GKR_Protocol
    Specialized session        isabelle build -c -d /path/to/afp/thys -d formal/isabelle
                               SMT_Circuit_Compiler_Correctness
    Extension-field chain      isabelle build -c -d /path/to/afp/thys -d formal/isabelle KoalaBear_Ext4_GKR
                               (builds the three sessions below it)
    Registration check         every theory file appears in the ROOT of its own session
    Session documents          isabelle build -o document=pdf -d /path/to/afp/thys -d formal/isabelle SESSION
    Rust tests                 cargo test –workspace –release –locked
    Lint / format              cargo clippy –workspace –all-targets –locked – -D warnings; cargo fmt –all –check
    Refinement inventory       Inspect committed verif/**/proof.json; selective replay requires the corresponding
                               Creusot/Why3 toolchain
StateSync-GKR: Mechanized Trust Chain                                                                                              16

F    Nonvacuity and Falsification Evidence

Table 3: Operation coverage at the tagged v1.1.0 source revision. The universal theorem and the concrete activation examples are
different evidence classes.
    Operation                Mechanized coverage                                Executable evidence
    Membership               Theorem A via the concrete compiler interpreta-    membership_theorem_a; end-to-end round trip
                             tion; positive round-trip activation
    Non-membership           Theorem A via the same interpretation; semantic    non_membership_theorem_a; genuine and adversar-
                             negative example rejects an occupied leaf          ial non-membership tests
    Update                   Theorem A via the update stack; Theorem C acti-    update_theorem_a; end-to-end round trip and mis-
                             vation on a concrete semantically invalid update   match rejection


• Instance witnesses: production-field formalization; compiler-model interpretation with a concrete membership round trip;
  merged-locale instance firing all composition premises on a concrete invalid update; two-job mixed-outcome batching instance;
  leaf-fold toy carrier with an explicit out-of-bound collision pair.
• Vacuity defects found and discharged: unsatisfiable specification-vector lengths (padding repair, downstream proofs unchanged);
  undischargeable constant degree bound (generalized to width-dependent bound; 2𝑠 representative mechanized).
• Falsification probes (refinement layer): 37 deliberate contract distortions in isolated builds, each rejected by the checker; zero
  vacuous active contracts found.
• Removal tests: redundant-assumption removal validated by clean rebuild; theorem- and premise-level mutation checks are part
  of the release re-audit protocol.

G     Claim-to-Source Map
Every claim in the abstract and introduction maps to a mechanized object: compiler equivalence → theorem_A_* (the-
orems 5.1 to 5.3); GKR chain-event soundness → gkr_assembly_soundness (theorem 6.1); model composition →
theorem_C_composition (theorem 7.1); batching → theorem_D_batching_correctness (theorem 8.1); leaf-encoding
injectivity → leaf_fold_inj (theorem 4.1); wiring-oracle equivalence → derived_mle_eq_table; nonvacuity → registered
instances and activations (table 1); partial refinement → contract families R1–R4 with the declared trust surface (section 9);
verifier-acceptance refinement → production_verifier_acceptance_refines_gkr_chain_bad with its stated value-
correspondence premise and its mechanized converse non-claim; extension-field transfer → gkr_assembly_soundness_ext4
and ext4_denominator_exact, with the challenge distribution assumed rather than proved. The contribution is the explicit
GKR model assembly and its composition with compiler correctness, extending the cited sumcheck formalization; it does not
assert a protocol-design innovation or an unconditional verified implementation.

References
 [1] José Bacelar Almeida, Manuel Barbosa, Karim Eldefrawy, Stéphane Graham-Lengrand, Hugo Pacheco, and Vitor Pereira.
     Machine-checked ZKP for NP relations: Formally verified security proofs and implementations of MPC-in-the-Head. In
     ACM Conference on Computer and Communications Security (CCS), 2021. ePrint 2021/1149.
 [2] Jeremy Avigad, Anat Ganor, Lior Goldberg, David Levit, Ohad Nir, Yoav Seginer, and Alon Titelman. Formal verification
     of the S-two AIR. arXiv:2606.04311, 2026.
 [3] Bolton Bailey and Andrew Miller. Formalizing soundness proofs of linear PCP SNARKs. In 33rd USENIX Security
     Symposium, 2024. ePrint 2023/656.
 [4] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. Creusot: A foundry for the deductive verification of Rust
     programs. In Formal Methods and Software Engineering (ICFEM), volume 13478 of LNCS, pages 90–105, 2022.
 [5] Amos Fiat and Adi Shamir. How to prove yourself: Practical solutions to identification and signature problems. In Advances
     in Cryptology – CRYPTO ’86, volume 263 of LNCS, pages 186–194, 1987.
 [6] Jean-Christophe Filliâtre and Andrei Paskevich. Why3 — where programs meet provers. In Programming Languages and
     Systems (ESOP), volume 7792 of LNCS, pages 125–128, 2013.
 [7] Azucena Garvía Bosshard, Jonathan Bootle, and Christoph Sprenger. Formal verification of the Sumcheck protocol. In 37th
     IEEE Computer Security Foundations Symposium (CSF), pages 605–619, 2024. arXiv:2402.06093.
 [8] Azucena Garvía Bosshard, Christoph Sprenger, and Jonathan Bootle. The Sumcheck protocol. Archive of Formal Proofs,
     2024. https://isa-afp.org/entries/Sumcheck_Protocol.html, formal proof development, February 2024.
StateSync-GKR: Mechanized Trust Chain                                                                                           17

 [9] Shafi Goldwasser, Yael Tauman Kalai, and Guy N. Rothblum. Delegating computation: Interactive proofs for Muggles.
     Journal of the ACM, 62(4):27:1–27:64, 2015. Preliminary version in STOC 2008, pp. 113–122.
[10] Lorenzo Grassi, Dmitry Khovratovich, and Markus Schofnegger. Poseidon2: A faster version of the Poseidon hash function.
     In Progress in Cryptology – AFRICACRYPT 2023, volume 14064 of LNCS, pages 177–203, 2023.
[11] Carl Kwan, Quang Dao, and Justin Thaler. Verifying Jolt zkVM lookup semantics. In Financial Cryptography and Data
     Security (FC), pages 163–179, 2026. ePrint 2024/1841.
[12] Junrui Liu, Ian Kretz, Hanzhi Liu, Bryan Tan, Jonathan Wang, Yi Sun, Luke Pearson, Anders Miltner, Işıl Dillig, and
     Yu Feng. Certifying zero-knowledge circuits with refinement types. In IEEE Symposium on Security and Privacy (S&P),
     2024. ePrint 2023/547.
[13] Carsten Lund, Lance Fortnow, Howard Karloff, and Noam Nisan. Algebraic methods for interactive proof systems. Journal
     of the ACM, 39(4):859–868, 1992.
[14] Nethermind Security. CertiPlonk: Extracting and formally verifying constraint systems from Plonky3 in Lean. https:
     //github.com/NethermindEth/CertiPlonk, 2025. Accessed 2026-08.
[15] Plonky3 contributors. Plonky3: A toolkit for polynomial IOPs. https://github.com/Plonky3/Plonky3, 2026. Rust
     library; accessed 2026-08.
[16] Jacob T. Schwartz. Fast probabilistic algorithms for verification of polynomial identities. Journal of the ACM, 27(4):701–717,
     1980.
[17] Succinct Labs and Nethermind Security. sp1-lean: Formal verification of the SP1 Hypercube zkVM in Lean. https:
     //github.com/succinctlabs/sp1-lean, 2026. Accessed 2026-08.
[18] Justin Thaler. Time-optimal interactive proofs for circuit evaluation. In Advances in Cryptology – CRYPTO 2013, volume
     8043 of LNCS, pages 71–89, 2013.
[19] Verified zkEVM project. ArkLib: Formally verified arguments of knowledge in Lean. https://github.com/
     Verified-zkEVM/ArkLib, 2026. Lean 4 development; accessed 2026-08.
[20] Tiancheng Xie, Jiaheng Zhang, Yupeng Zhang, Charalampos Papamanthou, and Dawn Song. Libra: Succinct zero-
     knowledge proofs with optimal prover computation. In Advances in Cryptology – CRYPTO 2019, volume 11694 of LNCS,
     pages 733–764, 2019.
