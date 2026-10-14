                                                    Fixed-Point Scaffolding in the Clef Programming Language
                                             Our Theoretical Grounding for Type-Preserving Compilation and Proof Inference
                                                                                 Houston Haynes
                                                                        SpeakEZ Technologies, Asheville, NC
                                                                            hhaynes2@alumni.unca.edu
                                                                                        May 2026


                                                                                        Abstract
                                                  For fans of Gabriel’s “Worse is Better” it may be ironic that C++, by way of MLIR,
                                              serves as the scaffold for compiling an ML-family language whose correctness properties are
                                              structural. A crucial intersection in our Composer compiler initiates its lowering with a fixed-
arXiv:2606.02854v2 [cs.PL] 16 Jun 2026




                                              point combinator that preserves the dimensional, grade, escape, and numeric-representation
                                              structure from the Program Semantic Graph. And the MLIR that’s witnessed from the
                                              PSG is no passive host. Its use of static single assignment, attribute system and dialects
                                              carry that structure materially. We show that our compiler middle end uses categorical
                                              construction for lowering code with companion verification to that strata: a functor from
                                              the compilation poset to a target category, subject to the compositionality equation. The
                                              grounding of our approach comes from three sources, each on its own algebraic object:
                                              Ohori’s machine-code proof theory grounds the compilation axis, parametricity grounds the
                                              content at the base, and adjoint mode logic grounds the traversal between our verification
                                              tiers. To extend the thesis we introduce compact-closed negative and fractional types, and
                                              show the type machinery can be carried with preserved structure and realized through
                                              tooling MLIR provides. More broadly, the same fixed-point primitive that preserves types
                                              through compilation also supplies proof terms that can continue to be exercised in MLIR to
                                              verify its integrity as lowering proceeds through the pipeline. We argue that this foundation
                                              is a unique additional point anticipated by our framework that includes dimensional types,
                                              Tarau’s groupoid, and cellular sheaves. Throughout, the formalism is instrumented as an
                                              internal scaffold: the abstractions support the compiler’s mechanics, where a developer is
                                              never required to reach for category theory in order to rely on the guarantees the compiler
                                              provides.


                                         1    For Better And For Worse
                                         Richard Gabriel’s 1989 essay, which includes a famous section titled “Worse is Better” [8],
                                         makes a claim about software adoption that has resonated through generations of programming
                                         language design. His assertion is straightforward: a system that prioritizes delivery over formal
                                         concerns spreads, and a system that insists on correctness first arrives late and adoption suffers.
                                         C spread that first case, and C++ spread by adapting C’s frame, as Bjarne Stroustrup brought
                                         object-oriented tooling to C instead of building a “cleaner” language, which, in his own words,
                                         would have yielded an unimportant cult language. That framing is both era and technology-
                                         dependent, but the message still impacts software design narratives today.
                                             The ML-family of languages descend from LISP, Gabriel’s original subject. Clef places its
                                         emphasis as a concurrent programming language with syntax firmly in that tradition. It aspires
                                         to provide efficient determinism with heterogeneous processor targeting, and in so doing faces
                                         Gabriel’s assertion directly. As a matter of practicality we take Stroustrup’s decision and ride
                                         the ubiquitous vehicle, C++ by way of MLIR [23]. As has emerged in the software community
                                         since Gabriel’s time, the most common division point on approaches to computer engineering
                                         is the one his essay named: the formalism of the “MIT School” and its pursuit of “the right
                                         thing,” versus the “worse is better” pragmatism of Bell Labs in New Jersey, where Stroustrup
                                         built C++. We will sometimes refer to the Fidelity Framework as having “New Jersey wheels


                                                                                             1
under an MIT frame.” As we show in this paper, that metaphor is more than just a clumsy
attempt at humor.
    The Composer middle end lowers a Clef program through MLIR dialect refinements, and
that is driven by a fixed-point combinator. It appears as fix in the Composer API surface and
is detailed as a Y-combinator in our design notes, and it is the same object: the structure that
ties our nanopass pipeline together. The claim of this paper is that this combinator is not a
convenience of the implementation.
    We make four assertions. First, we exhibit the verification pipeline as one categorical
construction and identify the fixed-point combinator as the traversal of its compilation axis,
grounded by Ohori’s machine-code proof theory. Second, we identify the traversal of a second
axis, the movement between what we refer to as verification tiers, and ground it in adjoint
mode logic. Third, we provide an introduction to a compact-closed negative and fractional type
and show how they can be represented in MLIR. Fourth, we argue that this grounding is the
distinct point anticipated by our earlier work, and we position it against the other candidates
those early design theories had considered.


2    One construction with three faces
The compilation pipeline is an ordered sequence of stages, to the elaborated Program Semantic
Graph, then MLIR, then the binary. Each stage carries a bundle of annotations, and each
lowering pass translates the bundle from one stage to the next. The property the pipeline
depends on is that translating in two steps agrees with translating in one. Writing F for the
assignment of a bundle to each stage and D for the translation along an edge, the discipline is
the compositionality equation,

                             D(s0 ≤ s1 ) ; D(s1 ≤ s2 ) = D(s0 ≤ s2 ),

and a consistent assignment of one bundle value to every stage that respects every edge is a
global section. This is the defining equation of a functor from a finite poset to a target category,
and it is also, exactly, what an engineer means when they insist that lowering a property through
an intermediate dialect must agree with lowering it directly.
    We have shown in earlier work [11–14] that this same construction appears in three places
that may seem unrelated. The dimensional type system [19, 20] is the case where the base
poset is the compilation pipeline and the bundles are vectors of integer exponents, with the
translations being group homomorphisms and the compositionality enforced by our nanopass
infrastructure [30]. Tarau’s bijective encodings [31] are the degenerate case where the base is
a single point and the entire content is in the target, a connected groupoid of types linked by
isomorphisms through a common Root; the framework’s use of Zn as the canonical carrier for
                                                ∼
every annotation, with a round trip encA : A −  → Zn and decA ◦encA = idA , is a Root in precisely
Tarau’s sense. Cellular sheaves over finite posets [2] are the general case, where the base may
be any finite poset, including a hypergraph’s membership relation, and where a theorem makes
the discipline cheap to enforce: to verify a global section it suffices to check the structure-map
equations on the edges of the Hasse diagram, because transitivity propagates the rest. This is
both computationally efficient and logically rigorous.
    That last theorem is the reason the verification checks each lowering edge and not every
pair of stages, and it is a categorical fact and not simply engineering expediency. The cellular-
sheaf framing also supplies a diagnosis we will use later: when local consistency fails to extend
to a global section, the failure is a measurable obstruction, and a hypergraph serves to carry
obstruction classes that a one-dimensional graph cannot represent, which is why hyperedges are
load-bearing. For the rest of this paper the single fact to carry forward is that the pipeline is
one functor with the compositionality equation, and that everything the framework verifies is
a global section of some instance of that construction.

                                                 2
3    The compilation sheaf and its tiers
The verification architecture is this construction specialized so that the bundles are obligations
and the global section is the verification record. The base poset is held fixed, the compilation
pipeline, and what changes from one tier of verification to the next is only the category the
bundles live in. That single move, fixed base and refining stalks, is what lets a graduated
verification stack be one structure and not four layered mechanisms.

         Tier   Fragment        Decision   proce-    Bundle category         Trusted base
                                dure
         1      Zn equality     abelian-group uni-   finitely   generated    Z3
                                fication, polyno-    abelian groups
                                mial
         2      QF LIA,         Z3, NP               QF LIA models           Z3
                QF BV
         3      restricted      Z3 with library      distributions on lat-   Z3
                probabilistic   lemmas               tice cosets
         4      pRHL            type checker with    memory pairs with       Z3 and Rocq
                                Rocq library         relational judgments    kernel

    The tiers form an inclusion chain [14], Zn ⊂ QF LIA ⊂ FOL ⊂ pRHL, and the trusted base
has a factor that is salient here: Z3 alone is trusted through Tier 3, and Rocq’s kernel enters
only at Tier 4, so a deployment that needs safety-critical arithmetic and range proofs accepts a
smaller base than one that needs the relational, probabilistic proofs of Tier 4. The exponents
at Tier 1 are integers; whether the same decidability would carry to the rational exponents that
more advanced negative and fractional type forms introduce is a question a companion paper
takes up [15].
    The verification that witnesses a global section is not a second traversal of the program. The
compilation is a nanopass process, and the verification rides it as a distinct component, meeting
the compute-graph structuring at a clean seam. The reading is precise in program-verification
terms. At design time the obligation is a weakest precondition, computed backward through
the constraint chain so the language server can report proof status as the engineer types. At
each lowering edge the same obligation is re-checked, the consequence rule confirming that the
precondition the higher dialect established implies the one the lower dialect requires. Crucially,
that re-check is a safety net for passes whose preservation is not yet established by construction.
When a pass silently dropped an annotation, the global section would otherwise break invisibly,
and the re-check catches it. We will see in the next section that a pass which is a certified
proof transformation needs no such net, and that is where the fixed-point combinator earns its
grounding.
    From that, a further reading carries forward. When a tier’s analysis returns a bound it
cannot tighten, the cellular-sheaf framing takes the conservative finding as an uncharacterized
obstruction in that tier’s bundle category, and the resolution is to refine the category. In
compiler machinery terms, it means moving up one tier where a library lemma would supply
a missing witness. That movement up the tier axis is the subject of Section 5, and it is the
second traversal the scaffold provides. While we’re still in design for the scope and range of
these lemmas that fit this case, we’re encouraged to find formalism that supports what will be
a level of automation to keep the resolution out of direct view of the developer.


4    A compilation-axis traversal
The Composer middle end applies a sequence of nanopass transformations, each accepting the
Program Semantic Graph in one dialect and returning it in a more refined one, and the recursion

                                                 3
over that sequence is tied by a fixed-point combinator. The question this paper answers about
it is the one a compiler engineer would ask: why should the dimensional, grade, escape, and
representation structure that the front end established still be intact after the combinator has
driven the program through a dozen dialect refinements? The answer is that each pass carries a
proof transformation and that proof transformations compose without losing what they carry.
     The numeric-representation structure is the concrete case to hold in view, because it is
the one a backend engineer can confirm by reading the lowered MLIR. The elaborator fixes a
value’s representation, a posit, an IEEE 754 float, or a fixed-point form, from the range its
dimensional type admits and the arithmetic the target supports, and records that choice as
codata on the Program Semantic Graph beside the dimension, the grade, and the escape class.
A lowering pass that does not touch representation leaves the annotation as it found it, and the
pass that selects the target form reads the choice the front end computed, so memory footprint
and allocation follow from a representation the type checker already saw. The scaffold keeps
the annotation live to the point of use, and that is why the representation the front end selected
is the representation the target uses.
     This is visible in the implemented middle end. The width-inference coeffect, computed
during design-time analysis, holds the range; the lowering reads it and fixes the integer repre-
sentation accordingly, and a node whose range the analysis cannot observe is not guessed but
reported, the error asking the source for an annotation:
  // Alex middle end. narrowType pulls the design-time width-inference coeffect and
  // fixes the representation of an open integer type from the inferred range.
  let narrowType (coeffects: TransferCoeffects) (nodeId: NodeId) (ty: MLIRType) :
      MLIRType =
      match coeffects.WidthInference with
      | None →ty                                            // no inference result;
          pass through
      | Some result →
          match ty with
          | TInt (IntWidth 0) →                             // representation not yet
               fixed
              match Map.tryFind (NodeId.value nodeId) result.NodeWidths with
              | Some inferred →TInt (IntWidth inferred.Bits) // fixed from the
                  inferred range
              | None →failwith "error FPGA0001: range unobservable; the source must
                  annotate the width"
          | _ → ty // concrete integers pass through; struct fields are narrowed
              field by field (elided)

    The pattern generalizes. The structural decisions are made during design-time analysis and
recorded as coeffects on the graph, and the lowering patterns pull those decisions and write
them into the operations they produce without recomputing them. This is a coeffect discipline
in the sense of Petricek, Orchard, and Mycroft [27], where a coeffect is what a computation
requires from its context: the requirement is settled during analysis, and a navigational pass
over the immutable graph, in the manner of Huet’s zipper [16], witnesses it and elides to MLIR
accordingly, so there is no second analysis at lowering time. Escape placement travels the same
way. The escape-analysis coeffect classifies a value, and the allocation pattern reads that class
and produces no heap allocation for a stack-scoped value and a static allocation for one that
escapes:
  // Alex middle end. pAllocValue pulls the design-time escape class and elides the
  // allocation the analysis already determined.
  let pAllocValue (nodeId: NodeId) (ssa: SSA) (ty: MLIRType) : PSGParser<MLIROp> =
      parser {
          let! state = getUserState


                                                4
          let escapeKind = getEscapeKindOrDefault nodeId state.Coeffects.
              EscapeAnalysis
          match escapeKind with
          | StackScoped →
              return! pUndef ssa ty                        // stack-scoped: no heap
                  allocation
          | EscapesViaReturn | EscapesViaClosure _ | EscapesViaByRef →
              let count, elemType = extractMemRefShape ty
              return! pAllocStatic ssa count elemType None // escapes: allocate
      }

    In both passes the MLIR layer carries a structure it did not establish. The dimensional,
grade, escape, and representation decisions belong to the Program Semantic Graph and are
settled during design-time analysis, and the lowering transports them and elides the operation
they imply. MLIR is structure-carrying here.
    The fixed point is a real object in the middle end: the combinator that ties the recursive
descent through the program. A nanopass that witnesses a scope-bearing node, a lambda, a
control-flow construct, a match, receives the combinator itself and calls it on the nested scope, so
the recursion closes over the program’s own structure. That descent is available because MLIR’s
static single assignment form is functional programming in Appel’s sense [1]: its regions keep
the program’s scope nesting as first-class structure in the IR. This reading has a formal lineage,
running from Kelsey’s correspondence between continuation-passing style and SSA [18] through
Appel to a result stated at the MLIR level, where Bhat, Peduri, and Grosser optimize functional
programs in SSA over MLIR’s own regions [4]. The combinator can recurse into a lambda or a
control-flow scope because, in this IR, the scope is still there to recurse into.
  type Nanopass =
      { Name: string
        Witness: WitnessContext →SemanticNode →WitnessOutput }

  // The recursion is tied over the program’s nested structure.
  let rec lazyCombinator : Lazy<WitnessContext →SemanticNode →WitnessOutput> =
      lazy (fun ctx node →
          let rec tryWitnesses = function
              | [] → WitnessOutput.skip
              | np :: rest →
                  match np.Witness ctx node with
                  | o when o.Result = TRSkip →tryWitnesses rest
                  | o →o
          tryWitnesses allNanopasses.Value)
  and allNanopasses : Lazy<Nanopass list> =
      lazy ( leafRegistry.Nanopasses @                     // literal, arithmetic,
          memory, binding (platform witnesses elided)
             [ LambdaWitness.createNanopass (fun () →lazyCombinator.Value)
               ControlFlowWitness.createNanopass (fun () →lazyCombinator.Value)
               MatchWitness.createNanopass    (fun () →lazyCombinator.Value) ] )

    The MLIR-to-MLIR structural passes that refine the witnessed result run in the pass driver
applyPasses as a composition of functions of the shape MLIROp list -> MLIROp list, the
shape of declarationCollectionPass. The driver composes the declaration pass today and
names the dialect lowerings that may emerge, including DCont and Inet passes, as its planned
direction. Each step is a proof transformer that preserves the bundle the stage carries, so the
recursion that composes them preserves it too, and that reading is what lets the sequence grow
without a separate re-check on every edge.
    The dimensional, grade, escape, and representation decisions are settled in the Program


                                                 5
Semantic Graph during elaboration and the coeffect analyses that follow. A lowering pass
works against decisions already made: where the pass is a proof transformer the structure
crosses its edge by construction, and where it is not yet certified the entailment is handed to
the SMT dialect for the per-edge re-check of Section 3 to discharge. For the by-construction
case to compose, lowering passes must chain without losing what they carry, and that is Ohori’s
claim about proof transformers.
    Ohori develops a sequent calculus for intuitionistic propositional logic whose inference rules
are read backward as machine instructions [25], so that a proof is a code block and a sequent
specifies the code that computes a value from a machine state. The calculus has four judgment
forms,

 ∆ ⊢c A    (code block),      ⊢v A      (value),         ⊢e ∆    (environment),            ⊢A   (top level),

an axiom that returns the top of the machine state, and a generic instruction that is a left rule
read in reverse,
                                                   ∆2 ⊢ A
      (taut) A · ∆ ⊢c A,           (Rule-I)               ,     where I takes the state ∆1 to ∆2 .
                                                   ∆1 ⊢ A
The cut rule is restricted to the top level, between a code-block proof and a machine-state proof,
and the elimination of one cut is one step of execution. It runs the first instruction, advances
the state, and shortens the code:
                              C1 (∆1 ⊢c A)
                    E(⊢e ∆)
                                 ∆ ⊢c A                   E ′ (⊢e ∆1 )    C1 (∆1 ⊢c A)
                                                   =⇒                                  .
                              ⊢A                                         ⊢A
Two of Ohori’s results carry weight for us. The calculus enjoys cut elimination, and its prov-
ability is equivalent to that of natural deduction, the typed lambda calculus with products and
sums. From the equivalence Ohori extracts compilation and decompilation as proof transfor-
mations between the two systems, type-preserving by construction:

           ∆ ⊢c A in S ⇐⇒ ∆ ⊢ A in N,                {proofs in S} ∼
                                                                   = {typed code blocks}.

The object of use to us in this context is Ohori’s proof transformer, a partial proof with a hole
on the major-premise path, which composes by substitution into the hole:
                                                   C1 [ ] : ∆1 ⇒ ∆2 C2 : ∆2 ⊢c A
                    C[ ] : ∆2 =⇒ ∆1 ,                                            .
                                                             C1 [C2 ] : ∆1 ⊢c A
This is the compilation-axis traversal stated in the appropriate vocabulary. A lowering pass
realized as a proof transformer satisfies the compositionality equation of Section 2 by construc-
tion, because the composite transformer is type-preserving by the substitution rule above, so
the bundle it carries crosses that edge of the compilation poset with nothing to re-check. The
fixed-point combinator that the compilation pipeline runs is the operational form of this com-
position: it ties the sequence of transformers into one, and cut elimination is the normalization
that makes the composition coherent. Where a particular pass has not yet been certified as a
transformer, the build-time re-check of Section 3 is the net beneath it. Where it has, the net is
unnecessary, and the verification cost on that edge falls to zero.
    Two properties that the triangle of Section 2 did not carry come with this grounding.
One is completeness, in the bijection between proofs and typed code, which says that the
proof structure of low-level code is intrinsic and exhaustive within the propositional fragment.
The other is bidirectionality. Compilation is the transformation from natural deduction to the
sequent system, and decompilation is its reverse, recovering the logical structure faithfully, which
is the constructive method behind checking that a binary realizes the section it is supposed to.

                                                     6
5       The mode-shift traversal between tiers
The compilation axis is one axis of the construction; terraced verification crosses another. A
claim that begins as a dimensional equality and is closed by a probabilistic bound has touched
at least three of our tiers described in Section 3. We understood from early on that the path
between them would not be a “free move” so to speak. Our design is to make the crossings
first-class, the cross-tier proof composes the way the within-tier proof composes, and the verifier
would use the existing solver path to discharge each crossing as part of its surrounding obligation.
This is the second axis the construction needs, and the framework’s mode-shift discipline will
supply the typed object that traverses it. The vocabulary is from adjoint logic [10]1 , with the
shift operators as typed coercions between modes in a preorder, with the exponentials derived
from them:
                      ↑km A (m ≥ k),      ↓mk A,     !A =↓↑ A,       ?A =↑↓ A.
Specialized to our verification tiers, a shift ↑2,3 at a graph node would mark a transition from
Tier 2 to Tier 3 and carry the obligation that the structure present at the source tier admits
the refinement claimed at the target. The shifts compose by the laws of the adjoint logic, so
consecutive lifts compose and a round trip cancels,

                                   ↑2,3 ; ↑3,4 =↑2,4 ,       ↓3,2 ; ↑2,3 = id,

and the discharge would reuse the existing solver path, since a shift extends the source-tier
constraint with the obligation that justifies it and Z3 can discharge the conjunction in one
query, returning a verdict or an unsatisfiable core that localizes the failure to the transition.
This gives the conservative finding of Section 3 an operational meaning at this point: when
a lower tier cannot tighten a bound, the framework performs the shift ↑k,k+1 that refines the
bundle category to the one where a future library lemma would supply the witness.
    The two traversals are the same kind of object on different axes. Along the compilation
axis the structure maps are Ohori’s proof transformers, composing by substitution. Along the
verification-strength axis they are the mode shifts, composing by the adjoint laws. A global proof
therefore assembles from local, composable pieces, and the finite-poset theorem of Section 2 says
that checking the local pieces suffices. That is what makes the scaffold automatable.


6       Parametricity at the base
The two traversals move structure through the pipeline and across the tiers, but they say nothing
about where the content of the lowest tier comes from, and that content is free, because it is a
benefit it receives without design-time burden. The mechanism is parametricity, in the sense of
Reynolds and Wadler [29, 32]. A type read as a relation forces every well-typed term to respect
it, so a theorem about the term follows from its type, and because the abstraction theorem holds
for every well-typed term it is established once and instantiated per type. Wadler’s archetype
and its dimensional instance are

        g : ∀α.[α] → [α] =⇒ map f ◦ g = g ◦ map f,               mul : ∀d1 d2 . R⟨d1 ⟩ → R⟨d2 ⟩ → R⟨d1 d2 ⟩ ,

and the persistence of a dimension through a lowering pass L that does not inspect it is the
commutation dim ◦L = dim, which is the same free theorem.
   Curry–Howard, as in Section 4, identifies two objects: the program is the proof and the
type is the proposition. Parametricity keeps three objects apart: the type as a relation, the
program as the subject, and the proof as the abstraction theorem. The free theorem for a term
M of type τ is that M is related to itself, (M, M ) ∈ [[τ ]], and its proof is the meta-theorem
    1
    The specific uniform-mode-connective formulation is credited to recent work by A. Hăvărneanu; the load-
bearing weight in this paper rests on its published antecedents [26, 28], pending that work’s published venue.


                                                         7
                                             verification-strength axis:
                                             mode shifts ↑ / ↓




                          PSG                                 compilation axis:
                          node                                proof transformers




                                             joint-constraint axis:
                                             hyperedges


Figure 1: Three axes meet at a node. The compilation and verification-strength axes are the
two traversals this paper grounds, proof transformers along the one and mode shifts along the
other. The joint-constraint axis is the hypergraph structure that carries application factors.


and not M . So a program written with the Clef language is a program whose type entails
theorems, and the proof of each theorem is a separate object, the abstraction theorem at what
we refer to as Tier 1 and a solver witness at Tier 2. Our framework’s claim that a substantial
portion of automated verification is a compilation byproduct lives at this intersection, with the
lowering pipeline carrying the type-level structure and verification discharging the obligations
that operate on it.
    Parametricity does its work in the abelian fragment, where the annotation is a value in
a finitely generated abelian group and its preservation under a parametric map is forced. A
dimensional equality da = db +dc is on the free side. An inequality a ≤ x ≤ b, a statement about
a distribution, and a relation between two runs are past it, because parametricity is silent about
which specific values the variables take, and those are the obligations of Tiers 2 and beyond.
Naming this boundary is what lets us make use of the free component where it is available and
discharge where it is not.


7    Representing negative and fractional types
The dimensional types of our Native Type Universe already live in an abelian group: a value
carries an exponent over its base units, and inverses are ordinary, where a rate is the reciprocal
of a duration. We introduce negative and fractional types which lift that inverse structure from
the units up to the type itself. This may seem like a foreign concept but the theory is well
established [6, 17], and our design is shaped to take advantage of both where they are needed.
A fractional type is a demand: where a value of type T is something supplied, a value of its
reciprocal type stands for a T that is owed, and the two cancel when the demand is met. A
negative type is a value that runs in reverse, the counterpart that cancels its positive partner.
They are appropriate wherever a computation has a direction to undo or a demand to discharge,
and they would be substantial because the type system could then carry that reversal or demand
as structure checked before the graph runs, the basis for a compute graph whose integrity is
settled in advance. Where those conditions arise is a companion paper we’ve authored to further
develop; this section asks something more direct and narrow.
    Can such a type survive lowering? A dimension or a grade rides through as an attribute,
uncontroversially. A negative or fractional type is the harder case, and an SSA world that is at


                                                8
bottom C++ is exactly where a skeptic expects the abstraction to give out. If the scaffolding
carries it there, it carries the easy cases by inclusion. This section introduces the representation
and shows MLIR scaffolding preserves it.

7.1   Carried type-level structure
A negative or fractional type is not a new primitive SSA value. It is type-level dual structure
on the existing value flow. The additive and multiplicative dualities and their unit and counit
are
         T ⊕ (−T ) ∼= 0,     T ⊗ T −1 ∼
                                      = 1,    ηA : I → A ⊗ A∗ ,       εA : A∗ ⊗ A → I,
and the compact-closed promotion is governed by “the snake identities” from the original papers,
which are the coherence the structure must satisfy:

              (εA ⊗ idA ) ◦ (idA ⊗ ηA ) = idA ,         (idA∗ ⊗ εA ) ◦ (ηA ⊗ idA∗ ) = idA∗ .

Within Clef Compiler Services, a design extension within the Baker elaboration mechanism
would recognize the η and ε source constructs and we envision hyperedges in the Program
Semantic Graph that connect a positive value with its negative-typed adjoint, or a fractional
value with its multiplicative unification site, and the pairing is carried as codata through the
graph. As the program lowers, the pairing appears as MLIR attributes that inform program
structure. So at the MLIR level the type is the pairing structure carried alongside the operations.
Any potential annihilation ε would be a type function: the cancellation is type-level structure
carried through elaboration, and its operational realization is deferred.
    What makes the pairing sound is that the framework withholds the two structural rules
whose presence would let a value be silently shared or dropped [9],
                              Γ, A, A ⊢ B                                  Γ⊢B
             (contraction)                absent,          (weakening)             absent.
                               Γ, A ⊢ B                                   Γ, A ⊢ B
With no silent duplication and no silent erasure, every dependency the dual pairing introduces is
explicit at the type level, so it cannot hide at design-time, providing a “pit of success” protection
for cases where the types are required. Where a program turns on a value flowing back or a
demand being met, the type carries that constraint: it holds the value to its pairing and refuses
the copy or drop that would break it if it was left to attribute-based description.

          Clef source:       PSG hyperedge:       MLIR attributes      realization       target:
        η / ε constructs     pairing as codata    on the op graph         path        pairing intact


Figure 2: A compact-closed dual carried as type-level pairing from source to target. The pairing
lives as codata in the PSG and as MLIR attributes through lowering; the realization path is
a choice the discipline makes, and the fixed-point scaffolding preserves the pairing whichever
path is selected.

    The design we envision draws on the machinery MLIR already provides. The two natural
flavors are interaction-net-style realization for the negative case and constraint-based realization
for the fractional case, each with candidate dialects in the existing ecosystem [21, 22]. The
compact-closed adjoint is type-level structure carried as PSG codata, the η and ε pairing; the
interaction-net layer would be an operational carrier for that pairing and not the categorical
ε itself. The reverse direction the negative type names is reconstructed from the type-level
pairing, not by running the net backward, so negative types carry reversibility that interaction
nets may eliminate via annihilation at build time. For the purposes of this paper the relevant
level is above the choice: the type-level pairing carried as codata in the PSG, and the attributes
that carry it through lowering, are the structure the fixed-point scaffolding preserves whichever
realization the companion settles on.

                                                    9
7.2   Preservation is the point
The Composer’s fixed-point combinator sequences the lowering passes, each pass is a proof
transformation that preserves the carried pairing by construction, and the transformers compose
by the substitution rule of Section 4. A pass realized this way satisfies the compositionality
equation by construction, so the dual pairing crosses that edge as a preserved bundle value
with no separate check, and where a pass is not yet certified the per-edge re-check re-discharges
the preservation at that edge through Z3. Either way the pairing survives from the Program
Semantic Graph through every MLIR level to the target. This is the type-preservation claim
made good on the most constrained type the framework carries.
    The net beneath an uncertified pass is a structural pass of the shape Composer already
uses, MLIROp list -> MLIROp list, the shape of declarationCollectionPass, which walks
the operation tree and validates a global property. A pass certified as a proof transformer needs
none of this on its edge, since it preserves the pairing by construction. The check is the safety
net for the passes that are not yet certified, which is the same structure-and-content discipline
the entire pipeline runs on.
    The concept an engineer can take away is that a negative or fractional type is carried as a
preserved type-level pairing, and that our design that includes a fixed-point scaffold is the reason
the pairing remains intact at every meaningful stage of the lowering. This paper introduces
that base concept, including the representation and its preservation, through MLIR. The type
discipline itself, what the dualities are, the inference rules, and the application domains, is the
subject of the companion treatment [15].


8     A fourth point proposed
Our earlier “triangle” framing of dimensional types, Tarau’s groupoid, and cellular sheaves
postulates a close by anticipating a fourth point of one of two shapes, either a concept that ties
the three together conceptually “from above” or an application that needs all three at once. For
this paper the choice of one mental model versus the other is not material. As an application, the
compilation pipeline draws on the three together: the dimensional annotations are the bundle
content, Tarau’s Zn encoding is the canonical carrier, and the cellular-sheaf compositionality
is the global-section discipline that the per-edge verification and the fix combinator realize.
We believe our work identifies what the three share when the base is a compilation order, the
composition of proof transformations with cut elimination behind it, and supplies the traversals
that turn the construction into a working scaffold. It adds the two properties the triangle did
not carry, completeness and bidirectionality.
    The grounding has three contributors, each on its own object. Parametricity grounds the
content of the bundles, the abelian fragment, once for all well-typed terms. Ohori’s completeness
grounds the structure of the compilation-axis maps. The adjoint shifts ground the traversal
of the verification-strength axis. None of the three makes a Clef program a proof, and the
structure-and-content line is held throughout:
                                                                                      
           fourth point =        Param
                                 | {z }   ,         S ≡  N
                                                    | {z }         , ↑ / ↓ shift laws   .
                                                                     |      {z      }
                              bundle content   compilation-axis structure   tier-axis traversal

One hypothesis we’ve considered was several sheaves over the one base at once, a functional-
correctness sheaf with an access-discipline sheaf [3] and a symmetry sheaf [24], which is a
horizontal extension. Our companion work on negative and fractional types which follows
this paper [15] raises two further candidates as additional dimensions of the cell complex, a
verification-strength dimension and a duality dimension. These are compatible with what we
argue here, as we see the additional-dimension candidates and the “from above” grounding are
among those our triangle considers, and they may emerge as facets off the same figure.


                                                  10
9    New Jersey wheels under an MIT frame
Gabriel’s worse-is-better is a thesis about winning by spread, and that is not our primary goal.
The “wheels” supplied by MLIR is a significant body of work, and our frame uses it to reach a
variety of hardware targets. So by extension this nods to Stroustrup’s position, and applies it
to the goal Gabriel, at the time, lamented. The mundane MLIR substrate, which is C++ and
which won the way C won, carries the exotic and provable cargo: in our case, a compact-closed
dual that can ride dialects the MLIR ecosystem already provides, and the fixed-point scaffolding
we’ve built keeps it intact along the way. Of course we are not alone in bringing “the right thing”
onto this vehicle. The presence of an SMT dialect and of first-class verification dialects in the
MLIR ecosystem [7] shows the substrate already hosting correctness machinery, and the framing
we take is one MLIR’s own researchers reach for: Fehr and colleagues observe that base MLIR
is syntax-focused and supplies operation meaning through dialects, and Bhat and colleagues
mechanize rewriting directly over the nested regions our combinator descends [5]. That MLIR
is amenable to such treatment is the point, since it carries structure that proofs can ride. We
hold one boundary: this work formalizes operation behavior on the IR, which is adjacent to and
not the same as the type-level structure our Program Semantic Graph establishes, and none of
it is yet a complete semantics of the MLIR mechanism. The move is a recognized direction and
not our lone venture.
     The precise version of the metaphor is narrower than the irony might suggest. MLIR is
a constraint on C++, a disciplined use of it, and the structure it carries is what a front end
might provide. Its functional properties are there for utility, as the static single assignment
form is functional in Appel’s sense, while MLIR itself is structure-carrying without being a
direct expression of formalism itself. The structural work is primarily in our Program Semantic
Graph, settled during design-time analysis, and the MLIR carries principled expression because
it descends from that graph. What the substrate supplies is the capacity to carry the program’s
nesting, an attribute system that holds the annotations, and where verification is called for, the
SMT dialect discharges it to confirm the integrity holds.
     The grounding is also the answer to a critique the architecture might invite, that its higher
tiers are an over-built apparatus compensating for a type system that cannot carry value. The
answer is on our architecture’s own terms. The higher-tier machinery is the minimum the
content demands, because the free-theorem boundary of Section 6 forbids distributional and
relational facts being free of any type discipline, and the structure beneath that machinery is
grounded, by parametricity at the base, by the machine-code proof theory on the compilation
axis, and by the adjoint logic on the tier axis. Irreducible content-discharge riding on a grounded
structure is necessity. The way the architecture arrived here is corroborating: the verification
seam and the hypergraph were built under engineering pressure, and the sheaf and Tarau
structure were noted after. This progression revealed a principled structure; engineering pressure
and parametricity, the sheaf compositionality and two proof-theoretic groundings all land on
independently, characterized by necessity.
     What this paper has shown is that the fixed-point combinator in the Composer middle end
is the operational form of Ohori’s machine-code proof theory along the compilation axis, and
that the mode-shift discipline along the verification axis is the operational form of adjoint mode
logic. Parametricity grounds the content at the base; the cellular-sheaf compositionality the
framework already enforces joins them. The implementation work aims to be concrete and
bounded: certifying particular passes as proof transformations, lifting mode shifts to first-class
objects, and bringing the dialect realizations to maturity. What the developer interacts with
is the Clef language and design-time tooling, and the categorical structure underneath them is
the reason those interfaces are sound.
     And so by extension this paper takes a third position to Gabriel’s thesis: to use the substrate
that ‘won’ to carry verifiable structure. We propose a design for the compact-closed dual to


                                                11
the target as the hardest case the framework owns at this point. The type discipline behind it,
its inference rules, and its application reach are the subject of the companion treatment [15],
which carries our framework further.


A     From Clef source to MLIR
These three examples provide a proposed trace of the compilation-axis traversal of Section 4,
from Clef source to the MLIR the middle end produces. The middle end does not generate
MLIR from source text. Its zipper traversal witnesses the codata and coeffects on the Program
Semantic Graph, and that context guides the elision to MLIR. Clef is written in ML-family
syntax, and the MLIR is shown in the form the Composer serializer prints. The first two
examples show structure surviving into the result. The third shows a structural fact becoming
a proof obligation that the SMT dialect can discharge, which is what the abstract intends by
proof terms exercised in MLIR.

A.1    A dimensional function and the MLIR it lowers to
Consider a Clef function that computes kinetic energy:
  let kinetic (m: float<kg>) (v: float<m/s>) : float<joule> =
      0.5 * m * v * v

    The dimensional inference of the companion dimensional type system [11] resolves the return
as joule, since kg · (m/s)2 = kg · m2 · s−2 . The target is fixed by a quotation supplied through
the Fidelity.Platform component, which is type-carrying in the information sense and guides
the lowering toward a concrete target, an LLVM triple for the CPU case here, where the
representation selection settles on IEEE 754 double. Both the dimension and the representation
are decided in the Program Semantic Graph, before lowering. The dimension is consumed
there; it is not a value at the MLIR level, and no dimensional attribute rides on the resulting
operations. What the fixed-point combinator drives to the target is the arithmetic in the selected
representation:
  func.func @kinetic(%arg0: f64, %arg1: f64) →f64 {
    %v0 = arith.constant 0.500000 : f64
    %v1 = arith.mulf %v0, %arg0 : f64
    %v2 = arith.mulf %v1, %arg1 : f64
    %v3 = arith.mulf %v2, %arg1 : f64
    func.return %v3 : f64
  }

    Every operation is the output of a proof transformer in the sense of Section 4, and the
double precision the operations carry is the representation the front end selected, not a choice
remade during lowering. This is the structure-carrying reading of Section 9 in one function: the
structural decision is the graph’s, and witnessing into MLIR via our “Alex” middle end realizes
it.

A.2    An escape class decides the allocation
Consider a function that accumulates into a local:
  let sumScaled (xs: Span<float<m>>) : float<m> =
      let mutable acc = 0.0<m>
      for x in xs do acc ←acc + x
      acc


                                               12
   The escape-analysis coeffect detailed in Section 4 classifies acc. Because acc is read out as
a value and the cell itself does not leave the frame, the classification is stack-scoped, and the
witness elides it to a stack slot:
  func.func @sumScaled(%arg0: memref<?xf64>) →f64 {
    %v0 = arith.constant 0.000000 : f64
    // acc: a stack slot
    %v1 = memref.alloca() : memref<1xf64>
    %v2 = arith.constant 0 : index
    memref.store %v0, %v1[%v2] : memref<1xf64>
    // fold over %arg0 accumulates into %v1
    %v3 = memref.load %v1[%v2] : memref<1xf64>
    func.return %v3 : f64
  }

    The allocation op is the coeffect’s “decision”. Had acc escaped, by being returned by
reference or captured in a closure that outlives the call, the same site would be witnessed as
a heap memref.alloc. The witness pulls the class and elides accordingly, and the fixed-point
traversal carries it to the target intact.

A.3    A width obligation, extracted to the SMT dialect
In our FPGA pathway, integer widths are not declared but inferred. The interval analysis
records a range for each value, and the width follows from the range; the analysis is decidable
and runs to a fixed point before lowering. Consider the phase counter of an LED controller,
advanced once per step and reduced modulo the cycle length:
  // cycleSteps = 1024
  let nextPhase = (state.Phase + 1) % cycleSteps

    The analysis records Phase in the interval [0, 1023], which is eleven bits. The witness widens
to twelve bits for the increment and the modulus, then narrows the result back to eleven:
  %pe = arith.extsi %p : i11 to i12 // state.Phase, inferred 11-bit
  %one = arith.constant 1 : i12
  %inc = comb.add %pe, %one : i12
  %mod = arith.constant 1024 : i12
  %wrap = comb.mods %inc, %mod : i12 // (Phase + 1) mod 1024
  %next = arith.trunci %wrap : i12 to i11 // narrow back to eleven bits

    The truncation is sound only if %wrap is always representable in eleven bits. Today the
interval analysis establishes this structurally, and the FPGA0001 diagnostic fires when a range
cannot be resolved. The fact the analysis computed, %wrap in [0, 1023], is a proof obligation,
and it is a bitvector case: a Tier 2 obligation in the QF BV fragment, the fragment that carries
word-width reasoning. The SMT dialect upstreamed into MLIR gives the obligation a home
in the IR. A proposed lowering would state the soundness of the narrowing as a query whose
negation the solver attempts to satisfy:
  %verdict = smt.solver() : () →i1 {
    %p = smt.declare_fun "phase" : !smt.bv<12> // state.Phase, widened
    %k1024 = smt.bv.constant #smt.bv<1024> : !smt.bv<12>
    %k1 = smt.bv.constant #smt.bv<1> : !smt.bv<12>
    %k2048 = smt.bv.constant #smt.bv<2048> : !smt.bv<12> // 2^11, the i11 ceiling

    %bound = smt.bv.cmp ult %p, %k1024 : !smt.bv<12> // the inferred range fact
    smt.assert %bound


                                               13
      %inc = smt.bv.add %p, %k1 : !smt.bv<12>
      %wrap = smt.bv.urem %inc, %k1024 : !smt.bv<12> // (Phase + 1) mod 1024
      %over = smt.bv.cmp uge %wrap, %k2048 : !smt.bv<12> // narrowing to i11 would
          lose a bit
      smt.assert %over // seek a counterexample

      %r = smt.check
            sat { %f = arith.constant 0 : i1 smt.yield %f : i1 } // a counterexample
                exists
            unknown { %u = arith.constant 0 : i1 smt.yield %u : i1 }
            unsat { %t = arith.constant 1 : i1 smt.yield %t : i1 } // none: narrowing
                certified
            →i1
      smt.yield %r : i1
  }

    The unsat verdict is the witness that no eleven-bit overflow exists under the inferred range,
and the truncation stands. This is the build-time re-check at one lowering edge, made concrete:
the design-time analysis proposes the range, and the obligation that the lowering preserves it is
discharged as a bitvector query the solver decides. The width inference and the truncation are
in the middle end today. The SMT-dialect obligation is a proposed addition, and the dialect
that would carry it is already part of MLIR.


References
 [1] A. W. Appel. SSA is functional programming. ACM SIGPLAN Notices, 33(4):17–20, 1998.
     DOI: 10.1145/278283.278285.

 [2] A. Ayzenberg, T. Gebhart, G. Magai, and G. Solomadin. Sheaf theory: from deep geometry
     to deep learning. arXiv preprint arXiv:2502.15476, 2025.

 [3] A. Beckmann and A. Setzer. Access Hoare logic. arXiv preprint arXiv:2511.01754, 2025.

 [4] S. Bhat, A. Peduri, and T. Grosser. Lambda the ultimate SSA: optimizing func-
     tional programs in SSA. In Proceedings of the 2022 IEEE/ACM International Sym-
     posium on Code Generation and Optimization (CGO), pages 168–178, 2022. DOI:
     10.1109/CGO53902.2022.9741279.

 [5] S. Bhat, A. Keizer, C. Hughes, A. Goens, and T. Grosser. Verifying peephole rewriting in
     SSA compiler IRs. In 15th International Conference on Interactive Theorem Proving (ITP
     2024), LIPIcs 309, Article 9. Schloss Dagstuhl, 2024. DOI: 10.4230/LIPIcs.ITP.2024.9.

 [6] C.-H. Chen and A. Sabry. A computational interpretation of compact closed categories: re-
     versible programming with negative and fractional types. Proceedings of the ACM on Pro-
     gramming Languages, 5(POPL), Article 9 (January 2021), 29 pages. DOI: 10.1145/3434290.

 [7] M. Fehr, Y. Fan, H. Pompougnac, J. Regehr, and T. Grosser. First-class verification dialects
     for MLIR. Proceedings of the ACM on Programming Languages, 9(PLDI), Article 206, 2025.

 [8] R. P. Gabriel. Lisp: good news, bad news, how to win big, 1991. Contains the section
     “Worse is Better”.

 [9] J.-Y. Girard. Linear logic. Theoretical Computer Science, 50(1):1–101, 1987. DOI:
     10.1016/0304-3975(87)90045-4.


                                               14
[10] A. Hăvărneanu. Classical SNAX: An adjoint classical logic with uniform mode connectives.
     X post @aramh, May 10, 2026. https://x.com/aramh/status/2053868427375231352.

[11] H. Haynes. Dimensional Type Systems and Deterministic Memory Management: Design-
     Time Semantic Preservation in Native Compilation. arXiv preprint arXiv:2603.16437, 2026.

[12] H. Haynes. The Program Hypergraph: Multi-Way Relational Structure for Geometric Alge-
     bra, Spatial Compute, and Physics-Aware Compilation. arXiv preprint arXiv:2603.17627,
     2026.

[13] H. Haynes. Adaptive Domain Models: Bayesian Evolution, Warm Rotation, and Principled
     Training for Geometric and Neuromorphic AI. arXiv preprint arXiv:2603.18104, 2026.

[14] H. Haynes. Decidable By Construction: Design-Time Verification for Trustworthy AI. arXiv
     preprint arXiv:2603.25414, 2026.

[15] H. Haynes. Negative and Fractional Types in the Fidelity Framework. arXiv preprint
     arXiv:2606.04352, 2026.

[16] G. Huet. The zipper. Journal of Functional Programming, 7(5):549–554, 1997. DOI:
     10.1017/S0956796897002864.

[17] R. P. James and A. Sabry. Information Effects. In Proceedings of the 39th ACM SIGPLAN-
     SIGACT Symposium on Principles of Programming Languages (POPL ’12), pages 73–84.
     ACM, 2012. DOI: 10.1145/2103656.2103667.

[18] R. A. Kelsey. A correspondence between continuation passing style and static single as-
     signment form. In Papers from the 1995 ACM SIGPLAN Workshop on Intermediate Rep-
     resentations (IR ’95), pages 13–22. ACM, 1995. DOI: 10.1145/202529.202532.

[19] A. Kennedy. Programming Languages and Dimensions. Technical Report 391, University
     of Cambridge Computer Laboratory, 1996.

[20] A. Kennedy. Types for Units-of-Measure: Theory and Practice. In Central European Func-
     tional Programming School (CEFP 2009), LNCS 6299, pages 268–305. Springer, 2009. DOI:
     10.1007/978-3-642-17685-2 8.

[21] Y. Lafont. Interaction nets. In Proceedings of the 17th ACM SIGPLAN-SIGACT Sympo-
     sium on Principles of Programming Languages (POPL ’90), pages 95–108. ACM, 1990.
     DOI: 10.1145/96709.96718.

[22] Y. Lafont. Interaction combinators. Information and Computation, 137(1):69–101, 1997.
     DOI: 10.1006/inco.1997.2643.

[23] C. Lattner, M. Amini, U. Bondhugula, A. Cohen, A. Davis, J. Pienaar, R. Rid-
     dle, T. Shpeisman, N. Vasilache, and O. Zinenko. MLIR: scaling compiler infrastruc-
     ture for domain-specific computation. In Proceedings of the 2021 IEEE/ACM Interna-
     tional Symposium on Code Generation and Optimization (CGO), pages 2–14, 2021. DOI:
     10.1109/CGO51591.2021.9370308.

[24] A. Mehta and J. Hsu. Symmetry Hoare logic. arXiv preprint arXiv:2509.00587, 2025.

[25] A. Ohori. A proof theory for machine code. ACM Transactions on Programming Lan-
     guages and Systems, 29(6), Article 36, 2007. Preliminary form, FLOPS 1999. DOI:
     10.1145/1286821.1286827.



                                              15
[26] J. Paykin and S. Zdancewic. The Linearity Monad. In Proceedings of the 10th ACM SIG-
     PLAN International Symposium on Haskell (Haskell 2017), Oxford, UK, September 7–8,
     2017. DOI: 10.1145/3156695.3122965.

[27] T. Petricek, D. Orchard, and A. Mycroft. Coeffects: a calculus of context-dependent compu-
     tation. In Proceedings of the 19th ACM SIGPLAN International Conference on Functional
     Programming (ICFP ’14), pages 123–135. ACM, 2014. DOI: 10.1145/2628136.2628160.

[28] F. Pfenning. A logical foundation for session-based concurrent computation (adjoint logic),
     2015.

[29] J. C. Reynolds. Types, abstraction and parametric polymorphism. In Information Process-
     ing 83, pages 513–523. North-Holland, 1983.

[30] D. Sarkar, O. Waddell, and R. K. Dybvig. A nanopass infrastructure for compiler educa-
     tion. In Proceedings of the 9th ACM SIGPLAN International Conference on Functional
     Programming (ICFP ’04), pages 201–212. ACM, 2004. DOI: 10.1145/1016850.1016878.

[31] P. Tarau. Isomorphic Data Encodings in Haskell and their Generalization to Hylomor-
     phisms on Hereditarily Finite Data Types. arXiv preprint arXiv:0808.2953, 2008.

[32] P. Wadler. Theorems for free! In Proceedings of the Fourth International Conference on
     Functional Programming Languages and Computer Architecture (FPCA ’89), pages 347–
     359. ACM, 1989. DOI: 10.1145/99370.99404.




                                              16
