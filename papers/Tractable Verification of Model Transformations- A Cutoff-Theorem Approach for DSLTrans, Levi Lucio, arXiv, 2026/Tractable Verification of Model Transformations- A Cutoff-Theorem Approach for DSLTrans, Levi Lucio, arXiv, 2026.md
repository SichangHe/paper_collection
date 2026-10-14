                                                    Tractable Verification of Model Transformations:
                                                       A Cutoff-Theorem Approach for DSLTrans
                                                                                   Levi Lúcio
                                                                       Airbus Defense and Space, Germany
                                                                            levi.lucio@airbus.com


                                                                                        Abstract
arXiv:2604.18792v2 [cs.SE] 23 Apr 2026




                                                  Model transformations are central to Model-Driven Engineering (MDE), yet their formal
                                              verification has long been hindered by the undecidability of general-purpose transformation
                                              languages. DSLTrans was designed as a Turing-incomplete transformation language, in-
                                              tentionally trading expressiveness for verifiability. Despite this design philosophy, previous
                                              verification attempts based on path condition enumeration suffered from exponential blow-
                                              up and failed to scale to realistic transformations.
                                                  This paper presents a practically tractable verification workflow for DSLTrans trans-
                                              formations and explains the formal conditions under which that workflow is complete. The
                                              workflow rests on three mutually reinforcing contributions: (i) a Cutoff Theorem that makes
                                              bounded model checking complete for a precise fragment of DSLTrans and positive exis-
                                              tence/traceability properties, reducing verification from an infinite search space to a finite,
                                              computable bound; (ii) a suite of composable, soundness-preserving optimizations—per-class
                                              bounds, fragment-based verification with CEGAR, and trace-aware dependency analysis—
                                              that substantially reduce the SMT encoding size; and (iii) an implementation backed by Z3
                                              and validated on a concrete corpus of realistic model transformations drawn from the ATL
                                              Zoo and related community benchmarks.
                                                  We evaluate the approach on a corpus of 29 concrete transformations with 899 prop-
                                              erties, spanning compiler lowering, schema translation, behavioral modeling, graph map-
                                              ping, and synthetic stress tests. Of these, 552 properties are proved, 345 produce con-
                                              crete counterexamples—a number that includes intentional negative tests and boundary
                                              properties that mark known non-guarantees of the current transformations, not only un-
                                              intended bugs—and only 2 remain undecided within the timeout budget. For properties
                                              that exceed the tractability budget, we introduce a tractability-driven property refinement
                                              technique—precondition specialization, postcondition decomposition, and transformation
                                              instrumentation—that achieves up to 112× speedup while eliminating spurious counterex-
                                              amples. The approach is supported by a web-based IDE for authoring transformations and
                                              properties, and by a concrete execution engine for runtime validation.

                                         Keywords: Model transformation; Formal verification; DSLTrans; SMT solving; Bounded
                                         model checking; Cutoff theorem.


                                         1    Introduction
                                         Model-Driven Engineering (MDE) relies on model transformations as first-class artifacts that
                                         translate models conforming to one metamodel into models conforming to another [6, 7]. As
                                         transformations become more complex and are deployed in safety-critical domains such as
                                         aerospace, automotive, and medical systems, the need for formal guarantees about their cor-
                                         rectness grows correspondingly [8, 2].
                                             Unfortunately, the formal verification of model transformations is inherently difficult. Most
                                         widely used transformation languages—such as ATL [10], QVT [11], and Epsilon [12]—are
                                         Turing-complete, meaning that verification of arbitrary properties is undecidable in general.

                                                                                            1
Even for restricted property classes, the combinatorial explosion of possible input models ren-
ders exhaustive verification intractable for practical transformations.
   DSLTrans was designed from the outset to address this tension [1]. It is a Turing-incomplete
out-place model transformation language that deliberately sacrifices expressiveness—forbidding
unbounded recursion, in-place updates, and negative application conditions—in exchange for
amenability to formal analysis. The language enforces a layered execution model with mono-
tonic semantics: rules only add structure to the target model, never remove or modify existing
elements.

1.1   Previous Verification Attempts
Early verification approaches for DSLTrans were based on symbolic path condition enumera-
tion [2, 3, 5]. The idea was to enumerate all possible execution paths through the transformation—
each path condition representing a distinct combination of rule firings—and then check each path
against the property being verified. While theoretically sound, this approach suffered from a
fundamental scalability problem: the number of path conditions grows exponentially with the
number of rules and match patterns, reaching millions or billions for transformations with more
than a handful of rules.
    Several optimization techniques were proposed to mitigate this explosion, including path
condition subsumption and merging [4]. Despite these efforts, the approach could not be ap-
plied to transformations of realistic size. Benchmark transformations with 15–20 rules and 10+
properties routinely exceeded memory limits or required hours of computation, rendering the
approach impractical for the iterative development workflows that engineers require.

What is new in this paper relative to that prior line of work. The first author of the
present paper was also a co-author of the original DSLTrans verification approach [2] and of its
symbolic-execution successor [3, 4], and we want to be explicit about what is and is not inherited
from that work. The earlier line of work fixed a Turing-incomplete language design and a sound
path-condition enumeration semantics, and developed optimizations (subsumption, merging)
that addressed scalability within the path-condition paradigm. Crucially, no cutoff theorem
was proposed, conjectured, or actively pursued in that prior work—the question of whether
a small-model property could be derived from the structure of an F-LNR transformation was
simply not on the agenda. In hindsight, the path-condition approach could only have scaled to
realistic transformations through extreme compression of path conditions, an avenue that the
literature did not find. The contributions in the present paper—the F-LNR/G-BPP fragment
characterization, the cutoff theorem with its three concrete bound formulas, the per-class fixed-
point bound, the trace-aware soundness lemma, the SMT-direct encoding, and the composability
theorem—are therefore genuinely new with respect to the earlier DSLTrans line, and represent
a different verification architecture rather than an incremental optimization of the previous one.

1.2   Contributions of This Paper
This paper presents a fundamentally different verification strategy that makes formal property
checking of DSLTrans transformations practically tractable. Rather than enumerating paths, we
encode the transformation semantics directly into an SMT formula and leverage the Z3 solver [9]
for bounded model checking. The key insight is the Cutoff Theorem: for the fragment of
DSLTrans we consider and for positive existence/traceability properties, every property violation
has a bounded witness whose size depends only on the static characteristics of the transformation
and property, not on the input model. This transforms bounded model checking from a heuristic
into a complete verification method for the stated fragment.
    The primary contribution is a practically tractable verification workflow for DSLTrans; the



                                                2
cutoff theorem provides the formal basis for when bounded checking is complete, and the opti-
mization suite makes completeness practically reachable.
   Our contributions are:

  1. A tractable verification workflow: We implement a Python-based prover using Z3 that
     verifies properties of concrete DSLTrans transformations via automatic attribute abstrac-
     tion and SMT-based bounded model checking. We evaluate it on a corpus of 29 concrete
     transformations with 899 properties and show that verification workloads remain tractable
     in practice.

  2. The Cutoff Theorem for F-LNR × G-BPP: We prove that for the Local, Non-
     Recursive fragment of DSLTrans (F-LNR) and the class of Bounded Positive Pattern
     properties (G-BPP), every violation has a small counterexample. We derive three al-
     ternative bounds (Kcoarse , Ksharp , Ktight ) and prove their soundness. This theorem is the
     formal justification for when bounded checking is complete.

  3. Composable, soundness-preserving optimizations: We develop per-class bounds
     via fixed-point analysis, minimal fragment selection with CEGAR refinement, trace-and-
     attribute-aware dependency pruning, and equisatisfiable SMT encodings. These compose
     safely and reduce verification time by factors of 10–1000× on our benchmarks.

  4. A web-based IDE: We provide a browser-based development environment for authoring
     transformations, defining properties, executing transformations concretely, and running
     formal verification—supporting an interactive, test-driven development workflow. The
     deployed instance is publicly available online [15].

  5. Methodological insights: We report on the iterative co-evolution of mathematical the-
     ory and implementation, and on the test-driven methodology for defining properties and
     constructing transformations.

1.3   Paper Organization
The remainder of the paper is organized as follows:

   • Section 2 introduces the running UML-to-Java example.

   • Section 3 defines the DSLTrans fragment and the property fragment for which the results
     apply.

   • Section 4 presents the cutoff theorem and its claim boundary.

   • Section 5 develops the soundness-preserving optimization stack.

   • Section 6 describes the prover architecture, implementation, and empirical evaluation.

   • Section 7 explains why the resulting verification problem is tractable in practice.

   • Section 8, Section 9, and Section 10 discuss methodology, related work, and threats to
     validity.

   • Section 11 concludes.




                                               3
2     Running Example: UML to Java
To ground the discussion, we use as running example a transformation from UML class dia-
grams to Java Abstract Syntax Trees (ASTs). This transformation is a standard benchmark in
the model transformation community, frequently used to evaluate transformation languages and
verification approaches [13]. Our version is substantive: it comprises 6 layers, 22 rules, and 29
properties, covering package mapping, classifier-to-compilation-unit creation, member genera-
tion (fields, methods, constructors), accessor synthesis (getters/setters), inter-type relationships
(extends, implements, imports), and boilerplate generation (toString, equals, hashCode).
    We chose this example because it exercises every aspect of the verification method: (i)
layered structure: six layers with backward links across layers test the dependency-depth anal-
ysis; (ii) trace-link richness: most properties require trace links connecting source and target
elements, exercising trace-aware relevance pruning; (iii) type polymorphism: the metamodel con-
tains abstract classes with multiple concrete subtypes, stressing per-class bound analysis and
inheritance flattening; (iv) structural complexity: accessor and boilerplate rules produce multiple
target elements per match, leading to nontrivial cutoff bounds; and (v) community familiarity:
UML-to-Java variants appear across the ATL Zoo, TTC benchmarks, and related literature,
providing external comparability.

2.1    DSLTrans at a Glance
Before presenting the example, we briefly outline the key constructs of DSLTrans to help the
reader parse the listings and diagrams that follow. A complete formalization appears in Section 3.
    A DSLTrans specification is a single .dslt file containing metamodel, transformation, and
property declarations. A metamodel declares the typed classes, attributes, and associations of
a modeling language. A transformation maps a source metamodel to a target metamodel via
an ordered sequence of layers, each containing one or more rules. Each rule has three blocks:
(i) a match block, which specifies a pattern of source elements to find—elements prefixed any
are universally quantified, and direct associations constrain structural adjacency; (ii) an apply
block, which specifies target elements and links to create when the match succeeds, optionally
binding target attributes from matched source attributes; and (iii) an optional backward block,
whose concrete syntax uses <--trace--> to denote backward links (i.e., dependencies on traces
produced by earlier layers). A property is a precondition–postcondition pair: for every match
of the precondition pattern in the source model, a corresponding postcondition pattern must
exist in the target model. Postconditions may include trace links to assert that specific target
elements were produced from specific source elements.
    DSLTrans also has a graphical syntax, rendered by the web-based IDE (Figure 1). In the
graphical view, each rule is shown as a node-and-link diagram with match elements above and ap-
ply elements below, while backward links are drawn as vertical connectors linking apply elements
to previously created target elements. The textual listings in this paper are the authoritative
specification; the graphical views provide a complementary visual overview of rule structure.

2.2    Source and Target Metamodels
The source metamodel captures a simplified but representative subset of UML class diagrams:

                          Listing 1: Source UML metamodel (excerpt)
 1    metamodel UMLConcrete {
 2        enum ClassKind { Entity , Service , ValueObject }
 3        class Model { name : String }
 4        class Package { name : String }
 5        abstract class Classifier { name : String }
 6        class Class extends Classifier {


                                                 4
 7             isAbstract : Bool
 8             isFinal : Bool
 9             priority : Int
10             layerTag : String
11             kind : ClassKind
12        }
13        class Interface extends Classifier { }
14        class Enumeration extends Classifier { }
15        class DataType extends Classifier { }
16        class PrimitiveType extends DataType { }
17        abstract class Feature {
18            name : String
19            visibility : String
20            isStatic : Bool
21        }
22        class Property extends Feature {
23            isDerived : Bool
24            isReadOnly : Bool
25            lower : Int
26            upper : Int
27        }
28        class Operation extends Feature {
29            isAbstract : Bool
30            isQuery : Bool
31        }
32        // ... associations : packagedElement , ownedAttribute ,
33        //     ownedOperation , type , generalization , etc .
34   }

    The metamodel includes 22 classes with attributes ranging over strings, booleans, integers,
and enumerations, connected by associations representing ownership (packages contain classi-
fiers, classifiers own features), typing (properties have types), and inter-classifier relationships
(generalization, interface realization, dependency).
    The target metamodel represents a Java AST:

                        Listing 2: Target Java AST metamodel (excerpt)
 1   metamodel JavaASTConcrete {
 2       class CompilationUnit { fileName : String }
 3       class P ac ka geD ec la rat io n { name : String }
 4       class ClassDeclaration extends TypeDeclaration {
 5           isAbstract : Bool
 6           isFinal : Bool
 7           priority : Int
 8           layerTag : String
 9           kind : ClassKind
10       }
11       class I n t e r f a c e D ec l a r at i o n extends TypeDeclaration { }
12       class EnumDeclaration extends TypeDeclaration { }
13       class FieldDeclaration extends BodyDeclaration { }
14       class Meth odDeclar ation extends BodyDeclaration {
15           isAbstract : Bool
16       }
17       class C o n s t r u c t o r D e c l a r a t i o n extends BodyDeclaration { }
18       // ... TypeReference , Annotation , etc .
19   }




                                                 5
2.3     Transformation Rules
The transformation is organized into 6 layers, each handling a distinct phase of the translation:

     1. Layer 1 (CreatePackages): Maps each UML Package to a Java PackageDeclaration.

     2. Layer 2 (CreateCompilationUnitsAndTopTypes): For each packaged classifier (Class,
        Interface, Enumeration), creates a CompilationUnit containing the appropriate TypeDeclaration.
        Uses backward links to connect the compilation unit’s package reference to the PackageDeclaration
        created in Layer 1.

     3. Layer 3 (CreateOwnedMembers): Generates FieldDeclarations from Property el-
        ements, MethodDeclarations from Operation elements, and ConstructorDeclarations
        from Class elements.

     4. Layer 4 (CompleteSignaturesAndAccessors): Creates method parameters, return
        types, constructor parameters, and accessor methods (getters, setters, add/remove for
        collections).

     5. Layer 5 (CreateInterTypeRelations): Handles generalization (extends), interface re-
        alization (implements), dependencies (imports), and property type imports.

     6. Layer 6 (AddCommentsAndUtilityMembers): Generates Javadoc comments and
        utility methods (equals, hashCode, toString).

     A representative rule is shown in Listing 3.

             Listing 3: Example rule: mapping a packaged class to a compilation unit
 1    rule C l a s s 2 C o m p i l a t i o n U n i t {
 2        match {
 3               any pkg : Package
 4               any cls : Class
 5               direct pe : packagedElement -- pkg . cls
 6        }
 7        apply {
 8               pkgDecl : Pac ka ge Dec la ra tio n
 9               cu : CompilationUnit { fileName = cls . name }
10               classDecl : ClassDeclaration {
11                       name = cls . name ,
12                       visibility = " public " ,
13                       isAbstract = cls . isAbstract ,
14                       isFinal = cls . isFinal
15               }
16               outP : package -- cu . pkgDecl
17               outT : types -- cu . classDecl
18        }
19        backward {
20               pkgDecl <-- trace - - pkg
21        }
22    }

    This rule demonstrates several key DSLTrans features: (i) match elements with type con-
straints and direct associations; (ii) apply elements with attribute bindings; (iii) backward links
that connect a target element (pkgDecl) to a previously-created element via a trace link from a
source element (pkg).




                                                    6
2.4    Properties
Properties express correctness requirements as precondition-postcondition pairs. A typical prop-
erty states:

          Listing 4: Property: every UML package maps to a Java package declaration
 1    property P a c k a g e H a s P a c k a g e D e c l a r a t i o n
 2      " Every UML package maps to a Java package declaration . "
 3    {
 4         precondition {
 5             any pkg : Package
 6         }
 7         postcondition {
 8             pkgDecl : Pac ka ge Dec la ra tio n
 9             pkgDecl <-- trace - - pkg
10         }
11    }

    The semantics is: for every match of the precondition pattern in the source model, there must
exist a match of the postcondition pattern in the target model. The trace link <–trace– asserts
that the target element was produced from the source element by some rule. Properties can
reference multiple source and target elements, include direct associations, and impose attribute
constraints.




Figure 1: UML-to-Java running example in the web IDE. The transformation view exposes the
layered DSLTrans rules and the corresponding graphical rule structures used throughout the
paper.

     More complex properties involve multiple elements and associations. For example:

                Listing 5: Property: class-owned property yields an owned field
 1    property O w n e d P r o p e r t y H a s O w n e d F i e l d
 2      " Each class - owned UML property yields an owned Java field . "


                                               7
 3    {
 4          precondition {
 5              any cls : Class
 6              any prop : Property
 7              direct owned : ownedAttribute -- cls . prop
 8          }
 9          postcondition {
10              classDecl : ClassDeclaration
11              field : FieldDeclaration
12              classDecl <-- trace - - cls
13              field <-- trace - - prop
14              outB : bodyDeclarations -- classDecl . field
15          }
16    }

    This property involves two source elements connected by an association, and requires two
target elements with a trace link to each source element and a target-side association between
them. Note that the postcondition footprint is bounded and purely structural—a characteristic
we will exploit in Section 4.


3     The DSLTrans Fragment for Verification
We now formalize the fragment of DSLTrans and the class of properties for which our verification
approach is complete.

3.1       Foundational Definitions
Definition 3.1 (Typed Graph / Model). A typed graph over a metamodel M M = (C, A) (where
C is a set of classes and A is a set of associations) is a tuple M = (V, τ, E, α) where:

     • V is a finite set of vertices (elements),

     • τ : V → C assigns a type (class) to each vertex,

     • E ⊆ V × A × V is a set of labeled edges (links); we write (v, a, w) ∈ E for an edge from v
       to w with association label a ∈ A,

     • α assigns attribute values to vertices.

The size of the model is |M | = |V |.

Definition 3.2 (DSLTrans Rule). A rule R = (Match, Apply, Backward ) consists of:

     • A match pattern Match: a typed graph fragment to be found in the source model. The
       match arity ar (R) = |VMatch | is the number of match elements.

     • An apply pattern Apply: a typed graph fragment to be created in the target model upon
       a successful firing. Apply elements may have attribute bindings derived from matched
       source elements.

     • A set of backward links Backward ⊆ VApply ×VMatch (written with <--trace--> in concrete
       syntax): each pair (va , vm ) declares that the apply element va must be connected to an
       existing target element that was previously created from the source element bound to vm ,
       as recorded by trace links from earlier layers.




                                                   8
Definition 3.3 (DSLTrans Transformation). A transformation T = (L1 , L2 , . . . , Ln ) is an or-
dered sequence of layers. Each layer Li contains a finite set of rules {Ri,1 , . . . , Ri,ki }. Execution
proceeds layer by layer. The output of layer i is visible to backward links of rules in layers j > i,
but not to rules in the same layer. Within a layer, rules execute independently and cannot
interfere with each other.

Definition 3.4 (Rule Firing). A rule R ∈ Li fires on a source model M with accumulated
target state T̂<i (the target model produced by layers 1, . . . , i−1) when both of the following
conditions hold:

   1. Source match. There exists an injective, type-compatible function µ : VMatch → VM that
      respects all structural (association) constraints in Match and satisfies all attribute guards.

   2. Backward resolution. For each backward link (va , vm ) ∈ Backward , there exists a
      unique target element t ∈ VT̂<i such that τ (t) is compatible with τ (va ) and the trace
      record of T̂<i contains a link from the source element µ(vm ) to t.

When R fires, its apply pattern is instantiated: fresh target elements are created for each
va ∈/ dom(Backward ), backward-linked apply elements are bound to their resolved targets,
attribute bindings are evaluated, and trace links from source elements to newly created target
elements are recorded.

Notation. We write Fires(R, M, T̂<i ) for the set of valid firing bindings of rule R ∈ Li on
source model M with target state T̂<i , i.e., the pairs (µ, ρ) satisfying conditions 1 and 2 above,
where ρ maps backward-linked apply elements to their resolved targets. When backward links
are absent (Backward = ∅), a firing reduces to a source-side match, and we write Matches(R, M )
for the set of injective functions µ satisfying condition 1. We write MtTypes(R) := {τ (v) | v ∈
VMatch } ⊆ C for the set of source class types that appear on vertices of R’s match pattern.

3.2    The F-LNR Fragment
Our verification approach targets the Local, Non-Recursive (F-LNR) fragment of DSLTrans.

Definition 3.5 (F-LNR Fragment). A transformation T belongs to the F-LNR fragment if it
satisfies:

R1 (No indirect links): Only direct associations are allowed in match patterns. Indirect links
    (transitive closure) are excluded.

R2 (Bounded match size): There exists m ∈ N such that ar (R) ≤ m for all rules R ∈ T .

R3 (Layered execution): Rules are organized into ordered layers, and backward links point
    only to earlier layers. This is a structural property of DSLTrans and is guaranteed by
    construction.

R4 (Acyclic backward dependencies): The dependency graph induced by backward links
    is acyclic. Since backward links always reference earlier layers, this follows from R3.

R5 (Finite attribute domains): All attributes have finite domains: Bool, bounded-range
    Int, finite-vocabulary String, or Enum.

R6 (Monotonicity): Rules only add elements, links, and trace links to the target model; they
    never delete or modify existing elements. This is implicit in DSLTrans semantics.

   The rationale for each restriction is as follows:


                                                   9
   • R1 ensures that rule matching is purely local, avoiding the need to compute transitive
     closures that could create unbounded dependencies.

   • R2 bounds the “blast radius” of any single rule match, ensuring that adding one rule to
     the witness model adds at most m elements.

   • R5 ensures that the attribute space is finite, making SMT encoding decidable without
     resorting to undecidable string or arithmetic theories.

   • R6 (monotonicity) is the cornerstone of the cutoff argument: because rules only add struc-
     ture, reducing the source model can only reduce the target model, preserving violations of
     positive properties.

3.3   Properties and the G-BPP Fragment
Definition 3.6 (DSLTrans Property). A property P = (Pre, Post, Trace) consists of:

   • A precondition pattern Pre: a typed graph fragment over the source metamodel.

   • A postcondition pattern Post: a typed graph fragment over the target metamodel.

   • A set of trace constraints Trace ⊆ VPost × VPre : each pair (vt , vs ) asserts that the target
     element matching vt was produced from the source element matching vs , as recorded by a
     trace link.

A transformation T satisfies P on source model M , written T (M ) |= P , if and only if: for every
injective, type-compatible match µpre : VPre → VM that respects the structural constraints of
Pre, there exists an injective, type-compatible match µpost : VPost → VT (M ) that respects the
structural constraints of Post and satisfies every trace constraint—i.e., for each (vt , vs ) ∈ Trace,
the trace record of T (M ) contains a link from µpre (vs ) to µpost (vt ). We write T (M ) ̸|= P when
some precondition match has no corresponding postcondition witness.

   The cutoff theorem (Section 4) applies to the following restricted fragment of properties.

Definition 3.7 (G-BPP Property Fragment). A property P = (Pre, Post, Trace) belongs to
the Bounded Positive Pattern (G-BPP) fragment if:

P1 (Bounded pattern size): There exists p ∈ N such that |VPre | ≤ p and |VPost | ≤ p.

P2 (No indirect links): No transitive-closure associations in Pre or Post.

P3 (Local trace requirements): Trace constraints relate only elements explicitly named in
    Pre and Post. The property cannot assert “some unknown source element produced this
    target.”

P4 (Positive existence/traceability semantics): Satisfaction is monotone with respect to
    adding target structure. The property requires the existence of a bounded postcondition
    witness for each precondition match; it does not express global absence, uniqueness, or
    exclusivity constraints.

    The key insight is that G-BPP properties have a bounded “footprint”: the postcondition
witness involves at most p target elements, p source elements, and finitely many local trace and
structural links. This bounded footprint is what makes the cutoff argument possible.




                                                 10
3.4    Concrete Execution versus Proof-Time Abstraction
In practice, transformations are written with unrestricted attribute domains (arbitrary strings,
unbounded integers) for realistic execution, whereas Condition R5 requires finite domains for
the proof. We therefore formalize an attribute abstraction from concrete attribute valuations to
finite proof-time valuations.

Definition 3.8 (Attribute Abstraction). An attribute abstraction is an attribute-only abstrac-
tion consisting of a family of total functions on source and target attribute valuations. For each
source class C and target class D, let

                    αSC : Valconc
                             C    → Valabs
                                       C        and     αTD : Valconc
                                                                 D    → Valabs
                                                                           D ,

where Valconc
          C    and Valabs
                       C (respectively ValD
                                           conc
                                                and Valabs
                                                        D ) are the concrete and abstract attribute-
valuation spaces for that class. These functions lift pointwise to models by leaving vertices, edges,
types, rules, layers, and trace structure unchanged, and replacing only attribute valuations by
their abstract images. The abstraction must satisfy:

    1. Attribute-only scope: the structural part of the specification is preserved (classes, as-
       sociations, rules, layers, and trace structure unchanged).

    2. Abstract attribute domains are finite.

    3. Rule compatibility is preserved: for the abstracted attributes, rule applicability depends
       only on distinctions preserved by the abstraction.

    4. Property observables are preserved: attributes referenced by the property remain distin-
       guishable.

Lemma 3.9 (Claim Boundary). A proof on the abstract specification is absolute for the abstract
model family. It lifts to the concrete transformation only for correctness claims whose truth is
preserved by (αS , αT ).

Proof sketch. The abstract specification preserves all structural and control-flow distinctions
(by conditions 1, 3 of Definition 3.8), so any proof on it is exact for the abstract model family.
Lifting to the concrete transformation requires only that the claim not distinguish concrete
valuations that collapse to the same abstract valuation, which holds when condition 4 (observable
preservation) covers the claim’s referenced attributes.

    In practice, structural and traceability properties transfer directly, while exact attribute-
value properties transfer only if the abstraction preserves the relevant distinctions.


4     The Cutoff Theorem
The cutoff theorem is the mathematical foundation of our verification approach. It establishes
that for F-LNR transformations and G-BPP properties, if a property violation exists for any
input model (of any size), then a violation exists for a small input model whose size is bounded
by a computable constant K.

4.1    Theorem Statement and Proof Sketch
Theorem 4.1 (Cutoff Theorem for F-LNR × G-BPP). Let T ∈ F-LNR be a transformation and
let P = (Pre, Post, Trace) ∈ G-BPP be a property—with precondition pattern Pre, postcondition
pattern Post, and trace constraints Trace as in Definition 3.7. Let:

    • c = number of source classes relevant to P (reachable in the dependency graph),

                                                 11
   • m = maximum match size over relevant rules,

   • p = maximum pattern size of P (i.e., max(|VPre |, |VPost |)),

   • d = depth of the backward dependency graph (set d′ = max(d, 1)),

   • a = effective association arity for transitive well-formedness closure, i.e., the maximum
     number of additional elements forced by the least mandatory-association closure of any
     retained element,

   • r = total number of relevant rules for P .

Although Definition 3.7(P1) is stated with an existentially quantified bound, we instantiate p
as the exact value max(|VPre |, |VPost |) for the given P —the minimal natural number satisfying
P1—and the cutoff formulas below use this p (not a strictly larger surrogate). Define the cutoff
bound K = min(Kcoarse , Ksharp , Ktight ) where:

                           Kcoarse = c · (m + p) · d′ · (a + 1)                               (1)
                                                        ′
                            Ksharp = p · (1 + m · r) · d · (a + 1)                            (2)
                            Ktight = p · (1 + (m − 1) · r · d) · (a + 1)                      (3)

If there exists a model M such that T (M ) ̸|= P , then there exists a model M ′ with |M ′ | ≤ K
such that T (M ′ ) ̸|= P .

Proof sketch. Because the property is local (bounded pattern of size p) and the rules are local
(bounded match of size m, no transitive closure), any property violation is caused by a small
cluster of elements. Starting from an arbitrary counterexample M , we construct a bounded
witness submodel M ′ in four stages.

  1. Violation witness. Since T (M ) ̸|= P , there exists an injective, type-compatible match
     µpre : VPre → VM of the precondition pattern in M with no corresponding postcondition
     witness. Define Support 0 = µpre (VPre ), with |Support 0 | ≤ p (since µpre is injective).

  2. Bounded rule participation. Iteratively expand the support to include match elements
     of relevant rules that fire on the current support. Each rule match adds at most m − 1
     new elements (since it must share at least one element with the existing support to be
     connected). After d layers of backward dependency traversal, the support stabilizes at
     Support d with:
                                  |Support d | ≤ p · (1 + (m − 1) · r · d)              (4)
     Informally, this is a sound over-approximation: we start from at most p seed elements, and
     across at most d dependency layers we conservatively allow participation from any of the
     r relevant rules at each layer, each contributing at most m − 1 fresh connected elements.
     This yields the conservative multiplier 1 + (m − 1)rd on the initial p elements.

  3. Association closure. To maintain well-formedness, add the least mandatory-association
     closure of the support. By definition of a, each retained element forces at most a additional
     elements under this transitive closure, so:

                              |Closure(Support d )| ≤ |Support d | · (a + 1)                  (5)

  4. Witness preservation via monotonicity. Let M ′ be the submodel of M induced by
     Closure(Support d ). The logical shape of the argument is: (a) the property requires the
     existence of a postcondition witness (positive existence, P4); (b) target growth is monotone
     in source size—adding source elements can only produce more target structure, never less

                                                12
      (R6); (c) therefore, removing irrelevant source structure from M to obtain M ′ can only
      shrink the target model, and cannot create the missing postcondition witness.
      Formally, we show T (M ′ ) ⊆ T (M ) as graphs by induction on layers. Consider layer
      Li and suppose the target states agree up to this point: T̂<i      ′   ⊆ T̂<i . For any firing
      (µ, ρ) ∈ Fires(R, M , T̂<i ): (i) the source match µ maps into M ′ ⊆ M , so µ is also a valid
                            ′   ′

      source match in M ; (ii) each backward resolution ρ(va ) = t requires a trace link from µ(vm )
      to t in T̂<i
                ′ , and since T̂ ′ ⊆ T̂ , the same trace link exists in T̂ , so backward resolution
                                <i     <i                                 <i
      succeeds in M as well. Thus every firing in the smaller execution is also a firing in the
      larger one, target elements and trace links produced by M ′ are a subset of those produced
      by M , and the inductive step holds. Since the postcondition witness was absent from the
      larger T (M ), it remains absent from the smaller T (M ′ ), and the violation persists.

    Each of Kcoarse , Ksharp , and Ktight is obtained by a different sound over-approximation of
stage 2. The bound Ktight uses the connected-component argument (m − 1 new elements per
step), Ksharp conservatively replaces m − 1 by m, and Kcoarse further replaces r with c · m/p.
After stage 3, each bound is multiplied by (a + 1), so all three soundly bound |M ′ |; therefore
|M ′ | ≤ K = min(Kcoarse , Ksharp , Ktight ). Appendix B details each derivation.

Where the argument breaks. The monotone witness-preservation argument above relies
critically on three properties of the F-LNR fragment. The argument would fail if:

   • Negative application conditions (NACs) were allowed: a rule conditioned on the
     absence of an element could fire in M ′ but not in M , breaking the subset relationship
     T (M ′ ) ⊆ T (M ).

   • Deletion or update semantics were present: in the larger model M , a rule might delete
     a target element; shrinking to M ′ could cause that rule not to fire, allowing the element
     to survive in T (M ′ ) and potentially completing a postcondition witness that did not exist
     in T (M ).

   • Transitive or nonlocal matching were used: rule matches could then depend on arbi-
     trarily long chains of elements, making the bounded support construction invalid.

   • Properties required global absence or uniqueness: a property such as “there is no
     element of type T ” is anti-monotone—shrinking the source reduces what the transforma-
     tion can build, so a violation present in T (M ) can disappear in T (M ′ ) when the smaller
     input simply produces fewer T -instances. The same holds for uniqueness or exclusivity
     constraints. In all these cases the small-model witness construction does not apply, because
     shrinking the model makes the property easier, not harder, to satisfy.

4.2   Significance
The cutoff theorem transforms bounded model checking from a heuristic (“we checked up to size
k and found nothing”) into a complete verification method (“we checked up to the theorem-valid
bound K and can therefore guarantee the property holds for all models of any size”). The bound
K is a computable constant that depends only on the static characteristics of (T, P )—it has no
dependence on the size of any particular input model.

4.3   Claim Boundary
To help the reader calibrate the scope of the result, we state explicitly what is and is not
established by the cutoff theorem.



                                                13
What is proved: Completeness of bounded verification for the F-LNR fragment (Definition 3.5)
   and G-BPP properties (Definition 3.7). If a property violation exists for any input model,
   it can be found within the computable bound K.

What is not claimed: The theorem does not cover arbitrary DSLTrans transformations (e.g.,
   those with indirect links or unbounded recursion), negative or global properties (absence,
   uniqueness, exclusivity), or unrestricted attribute domains. Properties outside G-BPP—
   such as those requiring global absence of a pattern or counting constraints—require sepa-
   rate justification.

What lifts to the concrete setting: When verification uses an abstracted proof specifica-
   tion (Section 3.4), a proof result is absolute for the abstract model family. It transfers to
   the concrete transformation only for claims whose truth is preserved by the attribute ab-
   straction map (Lemma 3.9). Structural and traceability properties transfer directly; exact
   attribute-value claims transfer only if the abstraction preserves the relevant distinctions.


5     Soundness-Preserving Optimizations
While the cutoff theorem guarantees a finite search space, the raw global bound K computed
from the theorem formulas alone can be very large—hundreds or even thousands for complex
properties. However, raw K is a poor predictor of actual verification difficulty: the optimizations
below interact to reduce the effective search space by orders of magnitude (e.g., from a raw
K = 735 to an effective per-class bound of 6; see Table 3). What matters for tractability is the
optimized bound vector, not the raw cutoff. We develop a suite of optimizations that reduce
this effective search space while preserving the soundness and completeness of the verification.
Crucially, these optimizations compose safely: each independently preserves the verification
guarantee, and their combination maintains it.

SMT encoding strategy. All optimizations in this section operate on top of a common encod-
ing that discharges the bounded verification problem to an off-the-shelf SMT solver. Following
the strategy outlined in Section 1, our prover targets the Z3 SMT solver [9] as its backend, and
we use “Z3” and “the SMT solver” interchangeably in what follows. Given a transformation T ,
a bound K, and a property P = (Pre, Post), the prover asks the solver to decide

                            Φ = Φworld ∧ Φrules ∧ Φpre ∧ ¬Φpost ,                              (6)

where Φworld encodes a well-formed source model of size ≤ K, Φrules encodes the full firing
semantics of every rule—source match satisfaction, backward link resolution against trace links
from earlier layers, and target element creation (Definition 3.4), Φpre asserts that the precon-
dition pattern is matched, and Φpost encodes the existence of a postcondition witness including
its target elements, target-side links, attribute constraints, and the required trace links back to
the chosen precondition elements. Thus ¬Φpost asserts that no such witness exists. If the solver
returns unsat, no violation exists within the bound—and by the cutoff theorem the property
holds for all input models. If it returns sat, the satisfying assignment encodes a concrete coun-
terexample. The full construction of each sub-formula is given in Appendix A; the optimizations
below reduce the size of Φ while preserving this equivalence.

5.1   Fragment-Based Verification
Rather than encoding the entire transformation, we verify each property against a fragment
F ⊆ T containing only the rules relevant to that property. This reduces both the number of
SMT variables and the cutoff bound K (since r and d are computed on the fragment).


                                                14
Lemma 5.1 (Monotonic Fragment Soundness). Let F ⊆ T be a subset of layers. For any source
model M , if F (M ) |= P , then T (M ) |= P .
Proof sketch. By R6 (monotonicity), F (M ) ⊆ T (M ) as graphs: every element, link, and trace
created by F is also present in T (M ). Since P is a positive existence property (P4), if a
postcondition witness exists in F (M ), the same witness exists in T (M ).

   This means that if the SMT solver proves P holds (unsat) on the fragment, the result is
absolute for the full transformation. A violated result on the fragment, however, might be
spurious: rules in T \ F might produce the missing postcondition structure.

5.2   CEGAR Refinement
We handle spurious counterexamples via Counterexample-Guided Abstraction Refinement (CE-
GAR) [17].
Lemma 5.2 (Witness Completeness via CEGAR). Let M be a counterexample such that F (M ) ̸|=
P . If for all rules R ∈ T \ F , no firing is possible—i.e., Matches(R, M ) = ∅ (no valid source
match exists)—then T (M ) ̸|= P .
Proof sketch. An omitted rule can contribute target structure only by firing on M , which requires
at minimum a valid source match (Definition 3.4, condition 1). If no omitted rule has a source
match, no omitted rule fires, so T (M ) and F (M ) produce identical target structure, and the
violation on F (M ) persists in T (M ).

    If any omitted rule does match, its layer is added to the fragment and verification is retried.
The implementation realises this idea as a progressive, counterexample-driven refinement loop
rather than an immediate jump to the full rule set: (i) try the minimal fragment (fewest layers
covering the property’s postcondition types and trace requirements); (ii) on violated, enter a
CEGAR loop that, at each iteration, inspects the concrete counterexample M and adds back
only those omitted relevant rules whose match pattern is satisfiable on the source side of M
(Lemma 5.2’s match witness). The cutoff K is recomputed for the enlarged fragment and, if it
remains within the configured per-property budget, verification is retried; (iii) only if this loop
reaches the full set of relevant rules (the baseline fragment) without resolving the verdict, or if
the refined cutoff exceeds the budget, the prover falls back to the baseline fragment as a final
attempt. This preserves Lemma 5.2’s witness-completeness guarantee while keeping the SMT
bound small for the typical case in which the violation is explained by a few additional rules
rather than the entire transformation.

5.3   Per-Class Bound Reduction
The global bound K allocates the same number of potential elements for every class, wasting
capacity on classes barely touched by the property. We derive per-class bounds through a
sequence of lemmas.
Lemma 5.3 (Witness Restriction). For F-LNR × G-BPP, the source side of any counterexample
can be reduced to only the precondition witness elements plus the least mandatory-association
closure required for well-formedness.
Proof sketch. The violation is triggered by the bounded precondition witness (G-BPP). By F-
LNR locality, only source elements in the witness or forced by mandatory associations participate
in rule matches relevant to the violation. Removing all other source elements can only eliminate
unrelated rule firings; by monotonicity (R6), the violation persists.

Corollary 5.4 (Source Seed Sufficiency). The source-side per-class bounds satisfy: KSbase = pS
(the number of precondition elements of class S), extended by mandatory association closure.

                                                15
Proof sketch. Immediate from Lemma 5.3: the base count for each source class S is exactly pS
(the precondition witness elements of that class), with additional instances arising only from
mandatory-association closure.
Lemma 5.5 (Target Production Bound). Given source bounds KS for each source class S
(for example, the source-side bounds obtained from Corollary 5.4 after mandatory closure), the
number of target elements of class C is bounded by:
                                               X
                              KCbase = pC +         NR · mC (R)                            (7)
                                             R∈Relevant

Here KCbase means the base bound for target class C: it counts the target instances of class C that
may be needed before adding any further target elements forced only by target-side mandatory-
association closure. The term pC is the number of postcondition elements of class C that the
property witness may require directly. The summation then adds the extra class-C target in-
stances that relevant transformation rules may produce:
   • for each relevant rule R, NR bounds how many times R may fire on the bounded source
     witness;
   • mC (R) is how many apply elements of class C a single firing of R can create;
   • therefore NR · mC (R) bounds the total number of class-C target elements contributed by
     rule R.
The firing bound NR is estimated by
                                                            n (R)
                                               Y
                                   NR ≤                   KS S                                 (8)
                                          S∈MtTypes(R)

which bounds the number of possible rule firings. Here MtTypes(R) is the set of source classes
used in the match of rule R, and nS (R) is the number of match elements of class S in R.
Intuitively, for each source class used by R, we multiply by the number of available bounded
choices for that class, once for each match position of that class. For example, if R matches two
elements of class A and one of class B, then NR ≤ KA      2 K . This explicitly covers properties
                                                              B
whose postcondition witness requires several target elements produced by multiple firings of the
same rule on different bounded source bindings.
Proof sketch. Target elements of class C arise from postcondition requirements (pC ) or from rule
                                                        n (R)
firings. Rule R can fire at most NR ≤ S∈MtTypes(R) KS S       times (one firing per injective bind-
                                        Q
ing over bounded source counts), each creating at most mC (R) elements of class C. Summing
over all relevant rules gives the stated bound.
Theorem 5.6 (Per-Class Bound Theorem). A counterexample exists with each class count ≤
KC , where the per-class bounds KC are given by the least fixed point of source seeds, source
mandatory closure, target production bounds, target mandatory closure, and a global cap at K.
Proof sketch. The preceding lemmas enumerate every source of per-class demand: source seeds,
mandatory closure, and target production. Starting from seed counts and iterating these obliga-
tions produces a monotone sequence of per-class bounds, capped at K, that stabilizes at a least
fixed point. Any minimal witness respects each obligation, so its per-class counts are bounded
componentwise by this fixed point. See Appendix B.5 for the full argument.
    The practical impact is substantial. As a concrete instance, consider the UML-to-Java
property PropertyHasField—“every UML Property traces to a Java FieldDeclaration”—
whose full derivation is carried out in Appendix B.4. The theorem’s global bound is K = 78,
but per-class analysis determines that only 1 Property slot and 1 Class slot are needed on the
source side, reducing the effective search space from 78 uniform slots to a handful of per-class
slots.

                                                16
5.4   Trace-Aware Dependency Pruning
The cutoff parameters r (relevant rules) and d (dependency depth) critically affect the bound
K. A naive computation includes every rule that can produce any target element of the required
type. We refine this using trace and attribute awareness.
    In what follows it is convenient to think of a relevance mode as any concrete procedure that,
given a property and a rule set, returns values for r and d. The prover ships with three such
modes—legacy, trace-aware, and trace-and-attribute-aware—introduced in the paragraphs below.
We write rmode and dmode for the values returned by an arbitrary such mode and Kmode for the
bound the Cutoff Theorem then yields from them; stronger modes prune more aggressively and
so produce smaller (tighter) values. The next lemma states the soundness condition that every
such mode must satisfy.

Lemma 5.7 (Soundness of a Relevance Mode). Fix a property φ, and let rtrue and dtrue denote,
respectively, the minimal relevant-rule count and minimal dependency depth that suffice for the
Cutoff Theorem’s witness construction. If a relevance mode returns values rmode and dmode with

                               rtrue ≤ rmode   and   dtrue ≤ dmode ,

then the resulting bound Kmode also satisfies the conditions of the Cutoff Theorem; that is, Kmode
is a sound (possibly looser) witness bound.

Proof sketch. Each cutoff formula is monotone in r and d: replacing the minimal values rtrue , dtrue
by any over-approximations rmode , dmode can only enlarge the resulting bound, so Kmode ≥ Ktrue .
Any witness fitting under Ktrue therefore also fits under Kmode ; soundness is preserved, though
tightness may be lost.

    The three modes mentioned above instantiate this scheme, ranging from a coarse baseline to
the refinement actually used in the theory.

Legacy baseline. The coarsest safe approximation is legacy relevance: if the property requires
a target element of type T , then every rule that can produce an element of type T is considered
relevant. This is sound because it certainly includes every rule that might participate in a
witness, but it is often very imprecise: many such rules produce the right target type for the
wrong source provenance.

Trace-aware refinement. The key observation is that a postcondition trace requirement
does not ask merely for “some target element of type T ”; it asks for a target element of type T
that was produced from the appropriate source element. Thus, if the property contains a trace
requirement from a source type S to a target type T , a witness can only use rules that match
an S-typed source element and create a fresh T -typed target element. This replaces the coarse
question
                                 “which rules can create T ?”
by the more informative question

                           “which rules can create T traced from S?”

and therefore prunes away rules that have the right target type but the wrong provenance.
     The same idea applies recursively to dependencies created by backward links. If a later rule
needs an existing target element of type T traced from a match element of type S, then only ear-
lier rules that can produce that same (S, T ) trace pair need to appear in the dependency closure.
Consequently, trace-aware relevance and dependency depth remain sound over-approximations,
but are typically much smaller than the legacy ones.


                                                17
Implementation refinement. The prover also implements a further trace-and-attribute-aware
pruning mode, which discards trace-compatible rules whose attribute bindings are incompati-
ble with the property’s attribute requirements. This is useful in practice, but the theoretical
development in this section only requires the trace-aware refinement above.
    For UML-to-Java, trace-aware mode reduces r from 10+ to 2–3 for many properties, shrinking
K by factors of 3–5×.

5.5   Equisatisfiable SMT Encoding
Lemma 5.8 (Factored Postcondition Equivalence). If the postcondition graph has independent
connected components C1 , . . . , Ck , the monolithic existential quantification is equivalent to the
factored formula:
                                              k
                                              ^
                                  Φfactored =   (∃⃗e ∈ Ci : links(⃗e))                            (9)
                                       i=1
reducing the SMT search space from O(N | ) to O(|P | · N max |Ci | ), where N is the total number
                                      |P

of target slots and |P | abbreviates the number of postcondition elements |VPost |.
Proof sketch. Independent components share no existential variables, so the existential quanti-
fiers distribute across the conjunction: satisfying the full postcondition is equivalent to satisfy-
ing each component separately. In the overall SMT formula of Appendix A, this factored form
rewrites the ¬Φpost component while leaving Φworld , Φrules , and Φpre unchanged. The complex-
ity improvement follows because the solver solves one subproblem per component, dominated
by the largest.
   Additional equisatisfiable optimizations include:
   • Property slicing: Remove classes and associations not referenced by the property or its
     relevant rules.
   • Metamodel slicing: Remove unreachable metamodel elements.
   • Attribute domain reduction: Collapse unused attribute domains to singletons.

5.6   Composability
Theorem 5.9 (Composability of Optimizations). Any finite composition of the above optimiza-
tions, in any order, preserves the soundness and completeness of the verification.
Proof sketch. We reason by preservation invariants on the current transformed verification prob-
lem. Each optimization belongs to one of three classes. First, witness-preserving refinements
shrink the searched rule/model space but preserve the existence of a cutoff-valid witness when-
ever one exists for the current problem; this includes the bound refinements and trace-aware
dependency pruning, and fragment selection once paired with its CEGAR repair condition. Sec-
ond, equisatisfiable rewrites transform the SMT formula while preserving its SAT/unsatstatus;
this includes factored postconditions and the slicing/domain-reduction rewrites. Third, exact
refinement steps such as CEGAR may reject a spurious fragment counterexample, but only by
restoring omitted structure and re-running verification, so they preserve final verdict correctness.
    These invariants are closed under composition. Composing witness-preserving refinements
yields another witness-preserving refinement, because a witness surviving the later refinement
also survives the earlier safe over-approximation chain. Composing equisatisfiable rewrites yields
another equisatisfiable rewrite by transitivity of logical equivalence. Interleaving exact refine-
ment steps with either class cannot invalidate the established invariant, because each refinement
step re-establishes a sound current problem before verification continues. Therefore, after any
finite sequence and any ordering of the optimizations, the final verification problem still has the
same holds/violatedanswer as the original theorem-complete procedure.

                                                 18
6     The DSLTrans Prover
We now describe the architecture, implementation, and empirical evaluation of the prover. The
implementation, the web-based IDE, the corpus of transformations and properties used in the
evaluation, and the supporting evaluation artifacts are all distributed together as a public com-
panion repository [16].

6.1    Architecture
The prover consists of three main components:

    1. Parser and model layer: Parses .dslt specification files into an in-memory AST, sup-
       porting metamodels with inheritance, associations with multiplicities, transformation rules
       with all F-LNR constructs, and properties with preconditions, postconditions, and back-
       ward links.

    2. Cutoff analysis: Implements fragment validation, relevant rule computation with legacy/trace-
       aware/attribute-aware modes, cutoff bound computation (Kcoarse , Ksharp , Ktight ), per-class
       bound fixed-point analysis, and minimal/baseline fragment construction.

    3. SMT-direct verifier: Encodes the bounded verification problem as a single Z3 formula
       using three sub-encoders:

         • Model encoder: Creates bounded source and target worlds with per-class slots,
           existence variables, association matrices, and attribute variables with finite domains.
         • Rule encoder: Encodes rule firing semantics—for each injective match binding, a
           firing variable implies source match satisfaction, backward link resolution, and target
           element creation with “at most one creator” constraints.
         • Property encoder: Encodes the violation condition Pre ∧ ¬Post, using factored
           postconditions and optional incremental checking.

    Supporting components include:

    • Concrete execution engine: Executes transformations on concrete XMI/Ecore models
      for testing and cross-validation.

    • Abstraction pipeline: Automatically synthesizes proof specifications from concrete spec-
      ifications.

    • Inheritance flattening: When properties use abstract types, generates concrete-class
      variants for verification and lifts counterexamples back.

    The abstraction pipeline is automated and property-directed. It scans rule where clauses, rule
guards, apply bindings, and property constraints to identify attribute observables, then finite-
izes only the attribute domains while preserving the structural transformation and property
vocabulary. It also propagates domains through direct attribute-copy bindings, so the resulting
proof specification is synthesized generically from the given transformation and properties.
    Operationally, the prover validates each synthesized abstraction before using it for proof: for
every rule guard and match-element where clause, it checks that the abstract domains preserve
the same Boolean control-flow distinctions as the concrete domains for the supported predicate
fragment used by the prover. The resulting proof specification is then re-checked against the
verifiable fragment conditions before SMT solving. In the web IDE, this enables fully automatic
proof attempts via abstraction before SMT verification.



                                                19
The concrete-to-proof pipeline. The end-to-end verification workflow proceeds in four
steps:

  1. Author a concrete specification: The transformation is written with unrestricted at-
     tribute domains (arbitrary strings, unbounded integers) for realistic execution and testing.

  2. Synthesize a proof specification: The abstraction pipeline automatically derives a
     proof-oriented specification with finite attribute domains, preserving structural and control-
     flow distinctions.

  3. Verify properties: The prover runs bounded model checking on the proof specification,
     using the cutoff theorem and the optimization stack.

  4. Interpret results: Proof results are absolute for the abstract model family and transfer
     to the concrete transformation for claims whose truth is preserved by the abstraction
     (Lemma 3.9).


                                          .dslt Specification
                                      transformation + properties




                                       Parser & Model Layer




   Concrete Executor                    Abstraction Pipeline
   XMI/Ecore execution                 concrete-to-proof synthesis




                                           Cutoff Analysis
                                      relevance, K, per-class bounds




                                        SMT-Direct Verifier                  Inheritance Flattening
                                      model/rule/property encoders            concrete-class expansion




                                         Verification Result
                                  holds / violated / counterexample

                                                                                    data artifact

                                                                                   core component

                                                                                 support component



Figure 2: Architecture of the DSLTrans prover. Solid arrows show the main verification pipeline
from concrete specification through proof-specification synthesis to SMT checking; dashed arrows
show supporting service interactions.

6.2    The Web-Based IDE
The prover is integrated into a web-based development environment (DSLTrans Browser Studio)
built with React and Vite. The IDE supports:

   • Textual editing: Full-featured editor for .dslt specifications with syntax awareness.


                                                   20
   • Visual rendering: Graphical views of metamodels, transformation rules, and property
     patterns using Konva.

   • Concrete execution: Run transformations on XMI input models and inspect outputs.

   • Formal verification: Run SMT-direct verification with streaming per-property progress,
     displaying results (holds/violated/unknown), timing, and counterexample informa-
     tion.

   • Automatic abstraction: For non-fragment specifications, the IDE automatically syn-
     thesizes a proof specification and runs verification on it.

   The backend bridges to the Python prover via a Node.js server that spawns Python processes,
enabling real-time streaming of verification results to the browser.




      (a) Model-loading and context panel          (b) Concrete execution      (c) Proof mode
                                                           result                   result
Figure 3: The DSLTrans Browser Studio workflow for the UML-to-Java example. The IDE
supports loading source models, executing the transformation concretely, and running SMT-
based verification from the same environment.

6.3   Experimental Setup
All experiments were run on a single machine with an Intel Core i7-12700H (14 cores), 32 GB
RAM, running Windows 10. The prover is implemented in Python 3.12 with Z3 4.13 as the SMT
backend. Each property is verified independently with a wall-clock timeout of 600 s (10 min);
properties exceeding this budget are reported as unknown. The dependency mode is trace-and-
attribute-aware (Section 5.4), and per-class bounds (Theorem 5.6) are enabled. All timings are
single-run wall-clock measurements, not averaged. For concrete transformations, proof specifica-
tions are synthesized automatically from the concrete specification via the abstraction pipeline
(Section 3.4) and regenerated for each run.




                                              21
                    Table 1: Concrete UML-to-Java verification results (excerpt).
 Property                                                                   Kbase      Kmin      Time (s)      Result
 PackageHasPackageDeclaration                                                     2         2           0.03   holds
 OwnedPropertyHasOwnedField                                                      73         4          29.78   holds
 ClassHasConstructor                                                              7         7           0.15   holds
 DependencyYieldsImport                                                          58         5          10.13   violated
 OperationParameterHasOwnedParameter                                             58         5           0.51   violated
 ClassMappedToInterfaceDeclaration_ShouldFail                                    30         3           0.03   violated
 MultiValuedPropertyHasArrayFieldType                                           405         5         100.51   holds
 MultiValuedPropertyHasAddHelper                                                735         6         370.99   holds



     Three properties in the table are violated: ClassMappedToInterfaceDeclaration_ShouldFail
is a negative test, intentionally expected to fail—its counterexample acts as a regression check for
a known non-guarantee. The other two (DependencyYieldsImport and OperationParameterHas-
OwnedParameter) are boundary properties: semantically meaningful correctness claims that are
stronger than what the current transformation rules guarantee. Their counterexamples docu-
ment the boundary of the proven correctness envelope and guide future strengthening of the
transformation (see Section 6.4).
     Table 2 summarizes the full corpus results. The 29 concrete transformations are organized
into primary benchmarks (individually listed), a graph-mapping suite of seven structurally sim-
ilar transforms, and synthetic/stress benchmarks. The three transformations grouped as “K-
boundary witnesses” in the synthetic block are the specs used for the empirical cutoff-bound
validation experiment described in Appendix C; their per-class bounds are exercised at K−3
through K+3 to corroborate that the theorem-derived bound is sufficient and that no single per-
class slot can be removed without changing the verdict, while leaving open whether a strictly
smaller theoretical bound might also be sound.

Table 2: Verification results across the full concrete benchmark corpus. The graph-mapping suite
contains seven structurally similar transformations sharing a common rule template; individual
suite entries appear in Appendix D.
 Transformation                                    Rules       Layers   Props    Holds      Viol.      Unk.    Max (s)
 Primary benchmark suites
 ATLCompiler                                           55           9      20          15         5        0       4.45
 BibTeX2DocBook                                        11           3      33          28         5        0       0.36
 BPMN2Petri                                            12           3       5           5         0        0      17.64
 Class2Relational                                      18           6      29          23         6        0       1.22
 Ecore2JsonSchema                                       5           3      20          15         5        0       3.89
 FSM2PetriNet                                           3           3      10           5         5        0       2.70
 KM32OWL                                                6           3      20          15         5        0       3.92
 OCLCompiler                                           29           6      40          32         6        2      70.00
 Persons                                                9           3       9           8         1        0       1.86
 PNML2NUPN                                              5           3      20          15         5        0       3.81
 SimplePDL2Tina                                         6           3      20          15         5        0       3.85
 Statechart2Flow                                        3           3      20          10        10        0       0.12
 Tree2Graph                                             2           2       6           3         3        0       1.52
 UML2Java                                              22           6      29          23         6        0     472.43
 University2ITSystem                                    8           5      21          16         5        0       2.34
 UseCase2Activity                                       3           3      12           8         4        0       0.04
 Graph-mapping suite (7 transforms, 3 rules / 3 layers each)
   Aggregate                                            21         —      140          77        63        0       4.11
 Synthetic and stress benchmarks
 K-boundary witnesses (3)                              —           —        8           4         4        0       0.77
 Scalability                                           67          14      17          15         2        0       3.73
 Stress (2)                                           278          —      400         200       200        0      83.83
 Total (29 transforms)                                                    899         552       345        2




                                                         22
6.4   Interpreting the Results
Three verdicts appear in the results, and their interpretation differs:
holds: The property is proved within the theorem-backed bound K. By the cutoff theorem,
    this is a complete guarantee: the property holds for all input models of any size.
violated: The SMT solver found a concrete counterexample—a specific source model and the
    resulting target model that violates the property. This is useful both as a bug report and
    as a boundary witness documenting a non-guarantee of the current transformation.
unknown: The solver did not terminate within the timeout budget. This is an implementation
   limitation, not a refutation of the theoretical framework: the property may well hold or
   fail, but the current solver budget was insufficient to decide it.
    Properties in the corpus fall into three categories. Ordinary properties express expected
structural invariants (e.g., “every UML package maps to a Java package declaration”). Negative
tests, marked by a dedicated naming suffix indicating that failure is expected, are intentionally
expected to be violated; their counterexamples serve as regression checks for known non-
guarantees. Boundary properties are semantically meaningful but stronger than the current
transformation contract—they mark behaviors that the transformation does not yet guarantee
and document the boundary of the proven correctness envelope.
    The concrete corpus demonstrates breadth across transformation sizes, domains, and struc-
tural patterns:
   • Standard benchmarks: Class2Relational and UML2Java are community-standard ex-
     amples [13, 14].
   • Compiler and compiler-like suites: ATLCompiler (55 rules, the largest non-stress
     transformation) and OCLCompiler exercise deep rule hierarchies and complex type struc-
     tures.
   • Behavioral transformations: UseCase2Activity, Statechart2Flow, FSM2PetriNet, BPMN2Petri,
     and SimplePDL2Tina cover process and state-machine mappings.
   • Schema and ontology transformations: Ecore2JsonSchema, KM32OWL, PNML2NUPN,
     and BibTeX2DocBook cover metamodel translation and document generation.
   • Graph-mapping family: Seven structurally similar transforms (Component2Deployment,
     ER2Relational, Family2SocialNetwork, FeatureModel2Configuration, Mindmap2Graph, Or-
     ganization2AccessControl, Workflow2PetriNet) share a common rule template, providing
     breadth across domains while testing the prover’s consistency on a homogeneous pattern.
   • Stress benchmarks: Scalability (67 rules, 14 layers), mega-stress (78 rules, 100 proper-
     ties), and ultra-stress (200 rules, 300 properties) test the prover under extreme workloads.
    The mixed outcomes are a feature, not a limitation: 552 properties are proved, 345 are falsi-
fied with concrete counterexamples (many intentionally through negative tests that are expected
to fail), and only 2 remain undecided. This shows that the method both proves nontrivial prop-
erties, detects real non-guarantees, and honestly reports its practical limits under current solver
budgets.

Sensitivity to abstraction. Because verification operates on the abstracted proof specifi-
cation (Section 3.4), changes to the abstraction policy can alter cutoff sizes, SMT encodings,
and timings. However, such changes do not invalidate the proof framework itself—they merely
change the practical workload. Results must therefore be regenerated when the abstraction
policy changes, and the timings reported here reflect the current abstraction settings.

                                                23
7     Why Is This Tractable?
The tractability of our approach is not a single insight but rather the result of four mutually
reinforcing factors. We discuss each in turn.

7.1    Monotone Semantics of DSLTrans
The monotone (additive-only) semantics of DSLTrans is the mathematical foundation that en-
ables every other optimization. Without monotonicity:

    • The cutoff theorem would not hold: a rule that deletes elements could invalidate postcon-
      dition witnesses in ways that depend on the global model size.

    • Fragment-based verification would be unsound: adding rules could remove previously-
      satisfied postconditions.

    • Per-class bounds would be invalid: the witness-restriction lemma relies on the fact that
      restricting the source model can only shrink the target model.

    The absence of negative application conditions (NACs) is equally critical: NACs would make
rule firing depend on the absence of elements, breaking the monotone relationship between source
and target model sizes.

7.2    Leveraging Z3’s Scalability
The move from path condition enumeration [2, 3, 4] to direct SMT encoding fundamentally
changes the verification architecture. Instead of the prover managing combinatorial explosion,
we delegate it to Z3, which brings decades of engineering in:

    • SAT solver heuristics (DPLL, CDCL, restart strategies),

    • Theory solvers (finite domains, bit-vectors, arrays),

    • Incremental solving and lemma learning,

    • Formula simplification and preprocessing.

    The key insight is that the SMT encoding is structurally regular : source and target worlds
are arrays of bounded slots, rule firings are conjunctions of local constraints, and postconditions
are bounded existential queries. This structure is well-suited to Z3’s decision procedures.

7.3    The Cutoff Theorem
The cutoff theorem converts an infinite verification problem (“for all models of any size”) into
a finite one (“for all models up to size K”). However, the raw bound K from the theorem
formulas is rarely the bottleneck in practice: per-class analysis, fragment selection, and trace-
aware pruning interact to replace a single large K with a vector of small, tightly fitted per-class
bounds. As Table 3 illustrates, raw bounds in the hundreds or thousands routinely collapse
to effective bounds in single digits. It is this optimized bound vector, not the raw cutoff, that
determines whether the SMT solver can decide the query in tractable time.




                                                24
7.4   Iterative Co-Evolution of Theory and Implementation
A distinctive aspect of this work is the tight feedback loop between mathematical theory and
implementation. Several optimizations that began as ad-hoc code-level improvements were later
generalized into the theory, and vice versa:

   • Per-class bounds: Originally a heuristic “slot allocation” trick, later formalized into the
     Per-Class Bound Theorem with the witness-restriction and target-production lemmas.

   • Trace-aware relevance: Originally a code-level filter (“only include rules that produce
     the right trace”), later formalized as a safe over-approximation lemma and integrated into
     the cutoff bound computation.

   • Factored postconditions: Originally an engineering optimization, later proved to be an
     equisatisfiable encoding with the Factored Postcondition Equivalence lemma.

   • Lazy target-world closure: Target well-formedness constraints (mandatory associa-
     tions on the target side) were initially encoded eagerly, creating enormous formulas. A
     lazy CEGAR-style refinement—defer closure constraints until the solver produces a model
     violating them—was found to be exact and substantially faster. This was later justified by
     the observation that closure constraints are equisatisfiable under the monotone fragment.

    This iterative process was greatly accelerated by AI-assisted development, which enabled
rapid prototyping of both mathematical proofs and code implementations. The speed of itera-
tion allowed mathematics to serve as an “abstract reasoning language” for guiding code develop-
ment: lemma statements encode architectural decisions, and proofs encode the justification for
optimizations.

7.5   Optimization Impact
To illustrate the cumulative effect of the optimization stack, Table 3 compares baseline and
optimized cutoff bounds for representative UML-to-Java properties. The baseline bound Kbase
uses the cutoff theorem alone (the tightest of the three formulas); the optimized bound Kmin
applies per-class analysis, trace-aware dependency pruning, and fragment selection.

Table 3: Effect of the optimization stack on selected UML-to-Java properties. Kbase is the
theorem-only bound; Kmin is the bound after per-class analysis, trace-aware pruning, and frag-
ment selection.
 Property                                                               Kbase   Kmin    Result
 PackageHasPackageDeclaration                                               2       2   holds
 ClassHasConstructor                                                        7       7   holds
 OwnedPropertyHasOwnedField                                                73       4   holds
 DependencyYieldsImport                                                    58       5   violated
 MultiValuedPropertyHasArrayFieldType                                     405       5   holds
 MultiValuedPropertyHasAddHelper                                          735       6   holds


    For simple properties (e.g., PackageHasPackageDeclaration), the baseline bound is already
small and the optimizations have little effect. For structurally complex properties, the reductions
are substantial: MultiValuedPropertyHasAddHelper drops from K = 735 to K = 6, a 122×
reduction in the bound and a corresponding reduction in SMT formula size. Without per-class
analysis, this property would be intractable; with it, verification completes in under 7 minutes.




                                                25
8     Working Practices and a Tentative Methodology
8.1    Toward Test-Driven Property Engineering
We do not claim a validated methodology: the case studies in this paper are too few, and
the workflow we followed was iterative and informal rather than prescriptive. What follows is
therefore a tentative methodology, distilled retrospectively from the practices that proved useful
while developing the transformations and property suites in our case studies. We expect it to
evolve as the prover is applied at larger scale.
   In this spirit, the recurring practices we found most useful were:

    1. Define expected structural invariants: What relationships should the transformation
       preserve? Write these as G-BPP properties.

    2. Write negative tests: Define properties that should be violated—expressing unin-
       tended mappings. These serve as regression tests for the transformation’s specificity.

    3. Iterate: If a holds property yields violated, either the transformation has a bug or the
       property is incorrectly specified. If an intentionally failing negative test yields holds, the
       transformation is too permissive.

    4. Refine property witnesses: When the SMT solver times out, analyze whether the
       postcondition pattern can be decomposed (factored postconditions) or whether the pre-
       condition is unnecessarily broad.

    In practice, we found a third category useful in addition to invariants and negative tests:
boundary properties. These are semantically meaningful, often desirable properties that are
stronger than the current transformation contract. They are not arbitrary falsehoods like neg-
ative tests; rather, they mark behaviors that the transformation does not yet guarantee, either
because the current rules are intentionally permissive, because the property had to be weakened
to match implemented behavior, or because further instrumentation/refinement of the trans-
formation would be needed to make the property provable. Keeping such properties in the
suite helps document the boundary of correctness of the current transformation, guides future
strengthening of the rules, and makes the prover useful not only for confirmation but also for
property-driven construction and refinement of transformations.
    Sub-second verification times for most properties made this style of interactive exploration
feasible in our case studies; whether the same workflow scales to larger transformation suites
remains to be evaluated.

8.2    Tractability-Driven Property Design
When a property exceeds the tractability budget, several strategies are available:
    • Precondition strengthening: Adding attribute guards to the precondition narrows the
      match space.

    • Precondition specialization: Replacing abstract/supertype match elements with con-
      crete subtypes reduces per-class slot allocation. The conjunction of specialized variants
      logically implies the original property.

    • Postcondition decomposition: Splitting a monolithic postcondition into independent
      components enables factored encoding.

    • Intrusive markers: For properties involving polymorphic types (e.g., “a setter signature
      exists”), adding marker classes to the target metamodel can disambiguate the postcondition
      pattern.

                                                 26
   • Property splitting: Complex properties can be decomposed into simpler sub-properties
     whose conjunction implies the original.

Case study: BPMN2Petri bipartite refinement. An initial bipartite-graph diagnostic
property for the BPMN-to-Petri-Net transformation used the abstract type FlowNode in both
precondition endpoints. Because FlowNode has 10+ concrete subtypes, the per-class analysis
allocated slots for every subtype, yielding K=90, bound =37, and a proof time of 383.75 s. Worse,
the polymorphic typing allowed the solver to construct a spurious counterexample in which
the same flow node could be matched by multiple mapping rules (which produce Places and
Transitions), reporting violated for a property that should hold.
    By specializing the precondition to representative concrete pairs (StartEvent → EndEvent
and StartEvent → ExclusiveGateway—the pairs where both endpoints map to Places), the
refined positive properties BipartiteCheck_StartEnd and BipartiteCheck_StartGateway are
each verified in 3.4 s at bound =17, a 112× speedup. The result also changes from violated
to holds: the SequenceFlow_PlaceToPlace rule correctly inserts a silent transition, preserving
bipartiteness. The specialization thus simultaneously improves tractability, eliminates a spurious
counterexample, and justifies renaming the refined checks so they are no longer marked as
intentionally failing tests.

Case study: UML2Java setter and adder properties. In the UML-to-Java transforma-
tion, the property PropertyHasGetter was intractable (> 30 min) because the postcondition
pattern—“there exists a method that is a getter for this property”—matched multiple rule out-
puts indistinguishably. Adding a SetterSignature marker class to the target metamodel and a
corresponding link in the setter-producing rule let the postcondition unambiguously identify the
intended getter method, reducing proof time from > 30 min to ≈ 10 s. Similarly, the composite
property MultiValuedPropertyHasAddRemoveHelpers was split into independent HasAddHelper
and HasRemoveHelper sub-properties, each with its own marker.
    Table 4 summarizes the property refinement techniques applied across the concrete bench-
mark corpus and their impact on verification times.

Table 4: Tractability engineering results. “Before” and “After” report proof time and verdict for
each original/refined property pair.
Suite        Property               Technique                 Before (s)   After (s)   Before     After
BPMN2Petri   Bipartite refinement   Precondition                  383.75        3.41   violated   holds
                                    specialization
UML2Java     PropertyHasGetter      Intrusive marker              >1800         10.2 unknown holds
UML2Java     WritableProperty-      Precondition                  >1800          9.8 unknown holds
             HasSetter              strengthening
UML2Java     AddRemoveHelpers       Postcondition                 >1800         12.1   unknown    holds
                                    decomposition + markers
OCLCompiler BuiltInNotHasInvoke     Precondition                    >70         >70    unknown    unknown
                                    strengthening
                                    (attempted)


    The BPMN2Petri bipartite refinement is notable because it both improved the result (elim-
inating a spurious counterexample caused by polymorphic type ambiguity) and achieved a
112× speedup; the refined properties were consequently renamed as positive checks. The
UML2Java properties demonstrate three complementary techniques—intrusive markers, precon-
dition strengthening, and postcondition decomposition—that together moved three previously-
intractable properties from unknown to holds. The OCLCompiler boundary properties remain
intractable due to the deep expression-layer type hierarchy; they mark the current tractability
boundary of the approach.



                                                 27
8.3   AI-Assisted Construction
AI tools played a significant role in this work:

    • Transformation authoring: AI was used to translate ATL Zoo transformations into
      DSLTrans syntax, with manual review for semantic fidelity.

    • Property generation: AI proposed initial property suites based on transformation struc-
      ture, which were then refined through iterative verification.

    • Mathematical development: AI assisted in formulating and refining theorem state-
      ments, proof sketches, and the identification of necessary lemmas.

    • Implementation: The prover code was developed iteratively with AI assistance, enabling
      rapid exploration of encoding strategies and optimization techniques.

    The key insight is that AI substantially accelerates the iteration speed of the theory-implementation
feedback loop described in Section 7.4. Mathematical reasoning in this context becomes an ab-
stract language for directing implementation: lemma statements encode architectural decisions,
and proofs encode the justification for optimizations.
    We are aware that AI-assisted theorem statements and AI-assisted prover code lower the
cost of producing plausible artifacts but do not by themselves guarantee their correctness. Ev-
ery theorem statement, lemma, and proof sketch in this paper was reviewed by the author, and
the prover was cross-checked empirically through the K-boundary validation experiment of Ap-
pendix C and through concrete-vs-symbolic agreement on the corpus. We nevertheless regard
these checks as complementary to, not a substitute for, the mechanized proof of the cutoff theo-
rem and the systematic mutation testing of the prover that we list as future work in Section 11;
AI-assisted development is precisely a reason to take those mechanization steps seriously rather
than to defer them.


9     Related Work
We organize related work along three axes: techniques for verifying model transformations
(Section 9.1), cutoff results in parameterized verification (Section 9.2), and SMT-based bounded
verification (Section 9.3). The positioning of DSLTrans among model transformation languages,
already sketched in the introduction, is revisited briefly in Section 9.4 from the perspective of
verifiability.

9.1   Verification of Model Transformations
The verification of model transformations has been studied extensively. Rahim and Whittle [25]
provide a survey of the field that gives broader context to the four lines of work below. We
categorize the most directly relevant approaches by their underlying verification technique.
    Theorem proving. Calegari et al. [22] and Poernomo [23] encode transformation properties
in interactive theorem provers (Coq, Isabelle). While these approaches offer the strongest guar-
antees, they require significant manual proof effort and do not scale to realistic transformations
without substantial domain-specific automation. Habel and Pennemann [32] establish founda-
tional results for verifying graph-transformation systems against nested conditions via weakest
preconditions; the resulting proof obligations are typically discharged by resolution-style theorem
proving rather than SMT, with completeness inherited from the discharger.
    Operational-semantics-based approaches. Troya and Vallecillo [24] give a rewriting-
logic semantics for ATL in Maude, which enables analysis via Maude’s reachability and model-
checking machinery. This recasts ATL verification as a general-purpose model-checking problem
and inherits its scalability profile; it provides no domain-specific completeness argument.

                                                   28
    Constraint solving and model finders. A line of work encodes transformation con-
tracts as constraint-satisfaction problems and discharges them with model finders. Anastasakis
et al. [29] translate UML class diagrams and transformation rules into Alloy/SAT. Cabot et
al. [8] verify declarative model-to-model transformations through invariants checked by con-
straint solvers (UMLtoCSP/EMFtoCSP). Büttner et al. [26] translate ATL transformations into
transformation models verified by model finders. Gogolla et al. [27] extend the USE tool with
filmstrip models for dynamic-property validation. These approaches are the closest neighbors of
our SMT encoding: they share the bounded-search engine, but in all of them the search bound
is user-supplied and there is no completeness theorem tying the bound to the transformation’s
structure. Our cutoff theorem mechanically derives a per-class bound from the transformation
and proves it sufficient for the F-LNR/G-BPP fragment.
    Static analysis for ATL. Cuadrado, Guerra, and de Lara [30] perform static analysis of
ATL transformations (AnATLyzer) to detect type errors, rule conflicts, and unreachable code.
AnATLyzer addresses well-formedness rather than contract-style correctness, but it is the closest
practical neighbor in the ATL ecosystem and complements rather than competes with the present
work.
    DSLTrans and related symbolic-execution work. The original DSLTrans verification
approach [2, 3, 4, 5] used symbolic enumeration of path conditions, with completeness arguments
specific to the language but tractability limited by the number of enumerated paths. Oakes’
thesis [5] also consolidated the theoretical development of this line of work and described sup-
porting tooling for execution and verification. Selim et al. [31] apply a closely related symbolic
approach to industrial automotive transformations, encoding ATL transformations as transfor-
mation models verified against OCL contracts. Our work replaces path-condition enumeration
with SMT-based bounded model checking backed by a cutoff theorem on the per-class slot count,
making verification tractable for transformations that were previously out of reach.

9.2   Cutoff Results in Verification
Cutoff arguments have a long history in parameterized verification. Emerson and Namjoshi [18]
established early cutoff results for symmetric ring topologies. Kaiser et al. [19] extended cutoff
detection to programs with dynamic thread creation. The current state of the art across commu-
nication primitives, system models, and proof techniques is surveyed by Bloem et al. [33]. Our
cutoff theorem differs from this body of work in that it is specific to model transformations and
exploits structural properties of DSLTrans (layered execution, monotone semantics, bounded
match patterns) rather than process symmetry.

9.3   SMT-Based Verification
Bounded model checking via SAT was introduced by Biere et al. [20] for hardware and extended
to software via SMT by Clarke et al. [21]; D’Silva, Kroening, and Weissenbacher [34] survey
the resulting body of techniques. Bounded SAT/SMT encodings have been applied to model
transformations through the model-finder approaches discussed in Section 9.1. The contribution
of the present paper is to combine such an SMT encoding with a domain-specific cutoff theorem
that turns the bounded check into a complete proof for the F-LNR/G-BPP fragment; we are
not aware of a prior result that pairs these two ingredients in this way.

9.4   Model Transformation Languages
The deliberate Turing-incompleteness of DSLTrans [1] is the language-design choice that makes
the cutoff theorem of this paper possible. Mainstream transformation languages—ATL [10],
QVT-R [11], Epsilon [12], Henshin [28]—obtain greater expressiveness through helpers, impera-
tive blocks, bidirectionality, recursion, or in-place updates with negative application conditions.


                                                29
Those features are valuable in practice but obstruct the structural arguments (layered execu-
tion, monotone semantics, bounded match patterns) on which our completeness result rests.
The positive results of this paper should therefore be read as showing what becomes provable
when expressiveness is constrained in this specific way, rather than as a critique of the more
expressive languages.


10    Threats to Validity
We discuss the main threats to the validity of our results along the standard internal/external/-
construct dimensions.
    Internal validity. The cutoff theorem is stated and proved at the paper level; it is not
mechanized in a proof assistant. An error in the theorem or its implementation could therefore
make the prover unsound or incomplete without being detected by the tooling. We mitigate
this through two complementary checks: (i) empirical validation of the cutoff bound by re-
verifying twelve representative properties under uniform K ± 1, K ± 2, K ± 3 shifts, per-class
selective −1 perturbations, and concrete witness execution at base − 1/base/base + 1 support
levels (Appendix C); and (ii) cross-validation of symbolic results against the concrete execution
engine described in Section 6 on representative XMI/Ecore inputs. A mechanized proof of the
cutoff theorem and systematic mutation testing of the prover remain future work (Section 11).
    External validity. The corpus consists of translations of existing transformations into
DSLTrans, primarily from the ATL Zoo. The F-LNR fragment excludes important transforma-
tion patterns (recursion, NACs, in-place updates), limiting applicability to out-place structural
mappings. We also did not perform a head-to-head empirical comparison with neighboring tools
such as Alloy-based encodings [29], USE/EMFtoCSP [8, 27], or AnATLyzer [30]: each of these
tools targets a different language and a different property class, and there is no shared input
format on which the same property could be discharged by all of them under comparable as-
sumptions. A faithful comparison would require non-trivial benchmark co-design and is left to
future work; the related-work discussion (Section 9) is therefore positional rather than empirical.
    Construct validity. The G-BPP property fragment covers positive existence and trace-
ability properties. Global absence, uniqueness, and non-monotone properties require separate
justification.


11    Conclusion and Future Work
This paper establishes a complete bounded-verification result for a precise fragment of DSLTrans
(F-LNR transformations with G-BPP properties), builds a practical prover architecture around
it, and evaluates it on a concrete corpus of 29 transformations with 899 properties spanning
compiler lowering, schema translation, behavioral modeling, graph mapping, and synthetic stress
tests. The approach rests on three pillars: the monotone semantics of DSLTrans that enables the
cutoff theorem; the practical power of Z3 as the verification backend; and a suite of composable,
soundness-preserving optimizations that reduce the verification problem to sizes the solver can
handle.
    The empirical results are encouraging: of 899 properties, 552 are proved, 345 are falsified
with concrete counterexamples, and only 2 remain undecided within the timeout budget. The
method detects both genuine invariants and real non-guarantees, and tractability-driven prop-
erty refinement extends its reach to initially intractable cases. Where previous path-condition
enumeration timed out on transformations with 15–20 rules, the workflow presented here settles
the full corpus—including transformations with up to 55 rules and stress benchmarks with 200
rules and 300 properties—with complete guarantees for decided properties.
    Future work includes:



                                                30
   • Mechanized proof : Formalizing the cutoff theorem in a proof assistant (Coq or Lean)
     to eliminate residual trust assumptions.

   • Mutation testing of the prover: Injecting mutants into the encoder and checking that
     intended-failure properties are detected, to corroborate the soundness of the implementa-
     tion.

   • Extended property classes: Developing cutoff arguments for absence and uniqueness
     properties under restricted conditions.

   • Fragment extensions: Carefully extending the F-LNR fragment with limited forms of
     NACs or bounded recursion while preserving verifiability.

   • Industrial validation: Applying the approach to safety-critical industrial transforma-
     tions.


References
 [1] B. Barroca, L. Lúcio, V. Amaral, R. Félix, and V. Sousa. DSLTrans: A Turing incomplete
     transformation language. In Proc. SLE, pages 296–305. Springer, 2011.

 [2] L. Lúcio, B. Barroca, and V. Amaral. A technique for automatic validation of model
     transformations. In Proc. MODELS, volume 6394 of LNCS, pages 136–150. Springer, 2010.

 [3] B. J. Oakes, J. Troya, L. Lúcio, and M. Wimmer. Fully verifying transformation contracts
     for declarative ATL. In 2015 ACM/IEEE 18th International Conference on Model Driven
     Engineering Languages and Systems (MODELS), pages 256–265. IEEE, 2015.

 [4] B. J. Oakes, J. Troya, L. Lúcio, and M. Wimmer. Full contract verification for ATL using
     symbolic execution. Software & Systems Modeling, 17(3):815–849, 2018.

 [5] B. J. Oakes. A Symbolic Execution-Based Approach to Model Transformation Verification
     Using Structural Contracts. PhD thesis, McGill University, 2018. https://escholarship.
     mcgill.ca/concern/theses/37720g196.

 [6] S. Sendall and W. Kozaczynski. Model transformation: The heart and soul of model-driven
     software development. IEEE Software, 20(5):42–45, 2003.

 [7] K. Czarnecki and S. Helsen. Feature-based survey of model transformation approaches.
     IBM Systems Journal, 45(3):621–645, 2006.

 [8] J. Cabot, R. Clarisó, E. Guerra, and J. de Lara. Verification and validation of declara-
     tive model-to-model transformations through invariants. Journal of Systems and Software,
     83(2):283–302, 2010.

 [9] L. de Moura and N. Bjørner. Z3: An efficient SMT solver. In Proc. TACAS, pages 337–340.
     Springer, 2008.

[10] F. Jouault, F. Allilaire, J. Bézivin, and I. Kurtev. ATL: A model transformation tool.
     Science of Computer Programming, 72(1-2):31–39, 2008.

[11] Object Management Group. Meta Object Facility (MOF) 2.0 Query/View/Transformation
     Specification, Version 1.3. OMG Document formal/16-06-03, 2016.

[12] D. S. Kolovos, R. F. Paige, and F. A. C. Polack. The Epsilon transformation language. In
     Proc. ICMT, pages 46–60. Springer, 2008.


                                             31
[13] Eclipse Foundation.   ATL transformation zoo.           https://www.eclipse.org/atl/
     atlTransformations/, 2024.

[14] Transformation Tool Contest (TTC). https://www.transformation-tool-contest.eu/,
     2024.

[15] L. Lúcio. DSLTrans Verification web application. Deployed browser-based environ-
     ment for authoring, executing, and verifying DSLTrans transformations. https://
     dsltrans-verification.onrender.com/, 2026.

[16] L. Lúcio. DSLTrans Verification: companion repository. Public monorepo containing the
     prover, the web-based IDE, the transformation and property corpus, and the evaluation
     artifacts for this paper. https://github.com/levilucio/dsltrans-verification, 2026.

[17] E. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. Counterexample-guided abstraction
     refinement for symbolic model checking. Journal of the ACM, 50(5):752–794, 2003.

[18] E. A. Emerson and K. S. Namjoshi. Reasoning about rings. In Proc. POPL, pages 85–94.
     ACM, 1995.

[19] A. Kaiser, D. Kroening, and T. Wahl. Dynamic cutoff detection in parameterized concurrent
     programs. In Proc. CAV, pages 645–659. Springer, 2010.

[20] A. Biere, A. Cimatti, E. M. Clarke, and Y. Zhu. Symbolic model checking without BDDs.
     In Proc. TACAS, pages 193–207. Springer, 1999.

[21] E. Clarke, D. Kroening, and F. Lerda. A tool for checking ANSI-C programs. In Proc.
     TACAS, pages 168–176. Springer, 2004.

[22] D. Calegari, C. Luna, N. Szasz, and Á. Tasistro. A type-theoretic framework for certified
     model transformations. In Proc. ICFEM, pages 112–127. Springer, 2011.

[23] I. Poernomo. Proofs-as-model-transformations. In Proc. ICMT, pages 214–228. Springer,
     2008.

[24] J. Troya and A. Vallecillo. A rewriting logic semantics for ATL. Journal of Object Tech-
     nology, 10:1–29, 2011.

[25] L. A. Rahim and J. Whittle. A survey of approaches for verifying model transformations.
     Software & Systems Modeling, 14(2):1003–1028, 2015.

[26] F. Büttner, M. Egea, J. Cabot, and M. Gogolla. Verification of ATL transformations using
     transformation models and model finders. In Proc. ICFEM, pages 198–213. Springer, 2012.

[27] M. Gogolla, L. Hamann, F. Hilken, M. Kuhlmann, and R. B. France. From application
     models to filmstrip models: An approach to automatic validation of model dynamics. In
     Proc. Modellierung 2014, volume 225 of LNI, pages 273–288. Gesellschaft für Informatik,
     2014.

[28] T. Arendt, E. Biermann, S. Jurack, C. Krause, and G. Taentzer. Henshin: Advanced
     concepts and tools for in-place EMF model transformations. In Proc. MODELS, pages
     121–135. Springer, 2010.

[29] K. Anastasakis, B. Bordbar, and J. M. Küster. Analysis of model transformations via
     Alloy. In Proc. 4th Workshop on Model-Driven Engineering, Verification and Validation
     (MoDeVVa), pages 47–56, 2007.



                                             32
[30] J. Sánchez Cuadrado, E. Guerra, and J. de Lara. Static analysis of model transformations.
     IEEE Transactions on Software Engineering, 43(9):868–897, 2017.

[31] G. M. K. Selim, F. Büttner, J. R. Cordy, J. Dingel, and S. Wang. Automated verification
     of model transformations in the automotive industry. In Proc. MODELS, volume 8107 of
     LNCS, pages 690–706. Springer, 2013.

[32] A. Habel and K.-H. Pennemann. Correctness of high-level transformation systems relative
     to nested conditions. Mathematical Structures in Computer Science, 19(2):245–296, 2009.

[33] R. Bloem, S. Jacobs, A. Khalimov, I. Konnov, S. Rubin, H. Veith, and J. Widder. Decid-
     ability of Parameterized Verification. Synthesis Lectures on Distributed Computing Theory.
     Morgan & Claypool, 2015.

[34] V. D’Silva, D. Kroening, and G. Weissenbacher. A survey of automated techniques for
     formal software verification. IEEE Transactions on Computer-Aided Design of Integrated
     Circuits and Systems, 27(7):1165–1178, 2008.




                                              33
A     SMT Encoding for DSLTrans
This appendix describes the SMT encoding used by the prover to translate the bounded verifi-
cation problem into a Z3 formula.

A.1     Source and Target Worlds
For each class C in the source metamodel, the encoder allocates KC slots, each guarded by a
Boolean variable exists C,i (for 1 ≤ i ≤ KC ). For each association A : C1 → C2 , a Boolean
matrix link A [i][j] (with 1 ≤ i ≤ KC1 , 1 ≤ j ≤ KC2 ) represents whether the link exists. Links
can only exist between existing elements:

                                   link A [i][j] =⇒ exists C1 ,i ∧ exists C2 ,j                                     (10)

    For each attribute attr of class C with finite domain D, an integer variable attr C,i is con-
strained to D. When C does not exist, attributes take a default value.
    Multiplicity constraints from the metamodel are encoded as cardinality constraints over link
rows/columns.

A.2     Rule Firing Encoding
For each rule R with match elements m1 : S1 , . . . , mn : Sn , the encoder iterates over all injective
bindings β = (i1 , . . . , in ) with ik ∈ {1, . . . , KSk } and ij ̸= ik when Sj = Sk . For each binding, a
Boolean variable fires R,β is defined:
                     ^                             ^
      fires R,β ⇐⇒        exists Sk ,ik ∧                    link Al,r [il ][ir ] ∧ guards R,β ∧ backward R,β       (11)
                      k                     (l,r)∈Links(R)

    where guards R,β encodes attribute constraints (Definition 3.4, condition 1) and backward R,β
encodes backward link resolution against trace links from earlier layers (Definition 3.4, condi-
tion 2).
    For each fresh apply element of class T in rule R, a choice variable selects which target slot
receives the element, with an “at most one creator” constraint ensuring no slot is claimed by
multiple rule firings.

A.3     Trace Encoding
Traces are encoded implicitly through the rule firing structure. When rule R fires with match
binding β and creates target element t in slot j, the trace link (Sk , ik ) → (T, j) is recorded.
Backward link resolution in later layers queries these trace links to identify previously-created
target elements.

A.4     Property Violation Encoding
The property P = (Pre, Post) is encoded as a satisfiability query:

                Φ=          Φworld          ∧      Φrules        ∧         Φpre           ∧        ¬Φpost           (12)
                            | {z }                 | {z }                  |{z}                    | {z }
                     well-formed models         rule semantics       precondition holds       postcondition fails

    Here Φpost requires a full postcondition witness: the chosen target elements exist, all required
target-side links hold, any postcondition attribute constraints are satisfied, and every declared
property trace link connects each postcondition element to the corresponding precondition el-
ement. If Z3 returns unsat, no violation exists (the property holds). If Z3 returns sat, the



                                                             34
satisfying assignment encodes a counterexample: a specific source model and the resulting target
model that violates the property.
    The postcondition encoding uses the factored form when the postcondition graph has inde-
pendent components, and falls back to monolithic encoding otherwise. For incremental check-
ing, each precondition binding is checked separately with early termination on the first violation
found.


B     Cutoff Bound Derivations
B.1     Derivation of Ktight
    1. Initial support. The violation starts with a match of the precondition pattern. The
       precondition has at most p elements, so |Support 0 | ≤ p. These are the “seed” elements.

    2. Backward dependency chains. To construct the minimal witness, we must ensure that
       the target elements required by the property are actually created. If a rule Ri requires
       a target element t via a backward link, we trace backward to the specific rule Ri−1 that
       created t and include the source elements that Ri−1 matched. This forms a backward
       dependency chain. In the worst case, satisfying the property may require tracing through
       all r relevant rules, so there are at most r chains per seed element.

    3. Chain depth. Because the transformation layers form a strict ordering (R3), the back-
       ward dependency graph is a DAG. The maximum length of any chain is the depth d of
       this DAG.

    4. Cost per step (connected-component argument). At each step backward in a chain,
       we add the match elements of one rule. A relevant rule matches at most m elements.
       Because the chain is connected—the rule must share at least one element with the existing
       support—each step adds at most m − 1 new elements. When m = 1, the matched element
       is already in the support, contributing 0 new elements; thus (m − 1) correctly bounds the
       additions.

    5. Total additions. Starting with p seeds, tracing at most r chains per seed, each of depth
       at most d, each step adding at most (m − 1) elements:

                                       additions ≤ p · r · d · (m − 1)

      The p multiplier is conservative: each seed element might independently require its own
      full set of r chains.

    6. Support size.

                       |Support d | ≤ p + p · r · (m − 1) · d = p · (1 + (m − 1) · r · d)

    7. Association closure. To ensure the extracted elements form a well-formed model, we
       include the least transitive mandatory-association closure required by the metamodel (e.g.,
       containment parents and any mandatory ancestors they in turn force). By definition of a,
       each retained element forces at most a additional elements under this closure, so:

                                |Closure(Support d )| ≤ |Support d | · (a + 1)

    8. Final formula.
                                 Ktight = p · (1 + (m − 1) · r · d) · (a + 1)


                                                   35
B.2    Derivation of Ksharp
Ksharp is a slightly looser but structurally simpler bound, derived with more conservative ap-
proximations.

  1. Initial support. As before, |Support 0 | ≤ p.
  2. Rule expansion without connected-component optimization. Instead of tracking
     that each rule match shares at least one element with the existing support (m − 1 new
     elements), we conservatively assume each match may add up to m elements.
  3. Support size. Tracing backward through d layers, with up to r relevant rules per seed
     element:
                       |Support d | ≤ p + p · r · m · d = p · (1 + m · r · d)

  4. Factoring out d′ . Define d′ = max(d, 1). Since 1 ≤ d′ , we can safely over-approximate
     the constant 1 as d′ :
                      p · (1 + m · r · d) ≤ p · (d′ + m · r · d′ ) = p · (1 + m · r) · d′
      This factoring also handles the edge case d = 0 (a single-layer transformation with no
      backward dependencies), where Ksharp correctly reduces to p · (1 + m · r) · (a + 1).
  5. Association closure and final formula.
                                  Ksharp = p · (1 + m · r) · d′ · (a + 1)

Linear vs. exponential growth. A natural concern is whether the support might grow
exponentially with depth. It does not: the witness construction is selective—at each chain
step we add only the elements needed to justify one backward dependency, not all possible rule
matches. The contribution of rule expansion is therefore additive in chain length (d), yielding
linear growth in the term p·r·d·(m−1) rather than multiplicative growth such as (1+r(m−1))d .
While exponential behavior can appear in the SMT solver’s search (as a function of the final
bound K), the theorem-side increase in K itself is linear in d.

B.3    Derivation of Kcoarse
Kcoarse replaces the per-rule counting with a class-based approximation, avoiding dependence
on r entirely.

  1. Initial support. As before, |Support 0 | ≤ p.
  2. Rule contribution via class counting. Rather than tracking individual rules and their
     chain structure, observe that each relevant rule match involves at most m source elements
     drawn from c distinct source classes. In the worst case, every combination of seed elements
     with rule matches contributes new elements, bounded by the product c · m. Adding the p
     seed elements:
                                |Support d | ≤ c · m + p ≤ c · (m + p)
      This replaces the p · (1 + m · r) factor with c · (m + p), which is tighter when c is small
      relative to p · r.
  3. Depth and association closure.
                                    Kcoarse = c · (m + p) · d′ · (a + 1)

    Kcoarse tends to dominate (i.e., be the minimum) when the number of relevant source classes
c is small, even if r (the number of relevant rules) is large.

                                                  36
B.4    Worked Example: PropertyHasField
To illustrate how the bounds are computed in practice, we trace through the PropertyHasField
property of the UML-to-Java transformation. This property states: “Every UML Property
traces to a Java FieldDeclaration.” The property has a single precondition element (any
prop : Property) and a single postcondition element (field : FieldDeclaration) linked
by a trace constraint.

Parameters. The cutoff analysis (with trace-aware dependency mode) determines:

   • p = 1: max(|VPre |, |VPost |) = max(1, 1) = 1.

   • m = 3: the largest relevant rule matches 3 source elements.

   • r = 8: eight rules are relevant (they produce FieldDeclaration elements with the correct
     trace type, including rules for static, read-only, collection, and primitive-type properties).

   • d = 1: backward dependency depth is 1 (single-step backward dependency; d′ = max(d, 1) =
     1).

   • a = 5: transitive mandatory-association closure adds up to 5 additional forced elements
     per retained element in the UML metamodel.

   • c = 5: five source classes are reachable in the dependency graph.

Bound computation.

             Kcoarse = c · (m + p) · d′ · (a + 1) = 5 · (3 + 1) · 1 · 6 = 120
              Ksharp = p · (1 + m · r) · d′ · (a + 1) = 1 · (1 + 3 · 8) · 1 · 6 = 150
              Ktight = p · (1 + (m − 1) · r · d) · (a + 1) = 1 · (1 + 2 · 8 · 1) · 6 = 102

   The final bound is K = min(120, 150, 102) = 102. Here Ktight wins because the connected-
component argument (m − 1 = 2 instead of m = 3) yields a tighter inner term than Ksharp , and
Kcoarse benefits from having fewer relevant classes (c = 5) but is still larger.

Per-class reduction. The global bound K = 102 would allocate 102 slots for every class.
Per-class analysis (Theorem 5.6) determines much tighter bounds. On the source side:

   • KProperty = 2 (one seed from the precondition, plus one additional from rule expansion).

   • KClass = 1, KPackage = 1 (mandatory closure from Property).

   • All other source classes: KC ≤ 1.

On the target side, the dominant class is FieldDeclaration with KC = 25 (driven by rule firing
counts over the bounded source). The effective per-class bound is maxC KC = 25, reducing the
search space from 102 uniform slots to 25 slots for the dominant class and far fewer for most
others.

B.5    Fixed-Point Argument for Per-Class Bounds
This subsection expands the proof idea behind Theorem 5.6. The goal is to justify why the
iterative per-class computation yields a sound upper bound for every class in a minimal witness.




                                                  37
Step 1: Seed the source-side counts. By Lemma 5.3, every counterexample may be re-
duced to a source witness consisting only of the precondition match plus the least mandatory-
association closure needed for well-formedness. Therefore the initial information is given compo-
nentwise by BS0 = pS : for each source class S, any witness needs at most the precondition-selected
instances of that class before closure is applied.

Step 2: Propagate mandatory closure. Mandatory associations induce implications of
the form “if class A occurs, enough instances of class B must also occur.” Applying all such
implications to the current source-side counts yields a larger source bound vector. Because
each propagation step only increases counts and every count is globally capped by K, repeated
propagation stabilizes after finitely many steps.

Step 3: Bound target production from bounded source counts. Once the source-side
counts are bounded, Lemma 5.5 yields a bound for each target class C:
                                           X
                          KCbase = pC +           NR · mC (R),
                                             R∈Relevant

where the per-rule firing count NR is itself bounded by the current source counts via the product
formula of Lemma 5.5:
                                                          n (R)
                                                Y
                                  NR ≤                 KS S ,
                                          S∈MtTypes(R)

with MtTypes(R) the source classes appearing in the match of rule R and nS (R) the number of
match elements of class S in R. The key point is that a rule can create target instances only when
one of its source-side matches fires, and—through this product—the number of possible such
firings is already bounded by the current source counts. Thus target-side growth is determined
entirely by the bounded source witness and the finite relevant-rule set.

Step 4: Propagate mandatory closure on the target side. The same well-formedness
argument applies to target classes: if a target class instance is present, mandatory associations
may force additional target-side instances. Repeatedly applying these obligations again yields a
monotone increasing sequence, still capped by K.

Step 5: Iterate to a fixed point. Collecting the source seeds, source closure, target produc-
tion, and target closure steps defines an update operator on vectors of class counts. This operator
is monotone: increasing any class bound cannot decrease any other bound, because rule-firing
counts and multiplicity obligations are themselves monotone in the input counts. Starting from
the initial vector B 0 and iterating the operator therefore yields an increasing sequence

                                    B0 ≤ B1 ≤ B2 ≤ · · · ≤ K

that must stabilize after finitely many steps, since every component ranges over the finite set
{0, 1, . . . , K}.

Step 6: Why the fixed point bounds every witness. Every minimal counterexample
witness must satisfy all four generating obligations above: its source counts are bounded by
the seed plus closure (Steps 1–2), its target counts are bounded by rule production (Step 3)
plus target closure (Step 4), and each of these obligations is captured by the update operator.
Since the fixed point is the least vector satisfying all obligations simultaneously, the per-class
counts of any minimal witness are bounded componentwise by the fixed point. This completes
the argument.


                                                38
C     Empirical Validation of the Cutoff Bound
The cutoff theorem of Section 4 predicts that, for any property in the F-LNR/G-BPP fragment,
verification at the theorem-derived per-class bound K is sound and complete: a property that
yields holds at K holds in all models, and a counterexample at K lifts to a concrete witness.
This appendix reports an empirical experiment that exercises this prediction directly. Its purpose
is twofold: (i) to provide independent evidence that the implementation actually realizes the
bound the theorem requires, and (ii) to corroborate that the bound is tight in the sense that
uniformly weakening it by one slot per class causes the prover to lose the witness.

Experimental design. For twelve representative properties drawn from eight DSLTrans spec-
ifications (covering the three K-boundary witnesses introduced in Table 2 plus selected properties
from FSM2PetriNet, Class2Relational, BPMN2Petri, Persons, Attributes, and Ecore2JsonSchema),
the experiment proceeds in three phases:

    1. Uniform sweep. The theorem-derived per-class source/target bounds are computed,
       then each bound is uniformly shifted by an offset δ ∈ {−3, −2, −1, 0, +1, +2, +3} and
       the property is re-verified at every offset. Negative properties (intentionally violated)
       are expected to yield holds for δ < 0 and violated for δ ≥ 0; positive properties are
       expected to remain holds throughout.

    2. Per-class selective −1 perturbation. Starting from the base bounds, every individual
       source and target class is decremented by one in isolation; the cutoff theorem predicts that
       some single per-class decrement must change the result for negative properties (identifying
       the class on which the bound is binding) and that no single decrement can change the
       result for positive properties.

    3. Concrete witness validation. For seven of the twelve properties (those whose synthetic
       input families could be enumerated mechanically), concrete XMI inputs at support levels
       base − 1, base, and base + 1 are executed through the concrete transformation engine and
       the resulting target models are inspected directly for the predicted property outcome.

Results. Table 5 summarizes the outcome. All twelve properties match the theorem-predicted
behavior in the uniform sweep, all twelve identify at least one binding per-class slot in the selec-
tive perturbation phase consistent with the witness structure, and all seven properties subjected
to concrete validation match the predicted outcome at every support level. The dominant cut-
off formula column reports which of the four bound formulas Kcoarse , Ksharp , Ksharp2 , Ktight
from Appendix B is binding for the property; in 10 of 12 cases Ktight is the unique minimum,
exercising the strongest of the derived bounds.




                                                39
Table 5: Empirical validation of the cutoff bound. holds/violated columns under Uniform
sweep indicate whether the result matches the theorem-predicted pattern at all seven offsets
K−3 . . . K+3; Selective −1 indicates whether at least one per-class decrement changed the re-
sult in the predicted direction (negative properties only); Concrete indicates whether all three
concrete support-level executions matched the predicted outcome (a dash means concrete wit-
nesses were not enumerated for this property).
Spec               Property                          Base K Dominant        Uniform Sel. −1 Conc.

FSM2PetriNet     SMHasTwoNets_ShouldFail                  4 tight              ✓       ✓       ✓
FSM2PetriNet     StateHasTwoPlaces_ShouldFail            12 tight              ✓       ✓       —
                 Diag_AbstractClass
Class2Relational NoDirectTable_ShouldFail               215 tight              ✓       ✓       —
                 Diag_DataType                              coarse/sharp/
Class2Relational BecomesTable_ShouldFail                  2 tight              ✓       ✓       —
                                                            coarse/sharp/
BPMN2Petri         StartEventHasTwoPlaces                 2 tight              ✓       ✓       ✓
Persons            SonBecomesMan                         18 tight              ✓      n/a      ✓
Attributes         HighPriorityItemRecorded               2 tight              ✓      n/a      —
Ecore2JsonSchema   AttributeHasRef_ShouldFail             8 sharp/tight        ✓       ✓       —
Deep
Dependency         DeepLeafMapsToTwoTD_ShouldFail       325 tight              ✓       ✓       ✓
TargetTight
Bound              SourceHasTwoTB_ShouldFail              8 tight              ✓       ✓       ✓
TargetTight
Bound              SourceHasTwoTD_ShouldFail              8 tight              ✓       ✓       ✓
TargetTight
Bound              SourceHasTwoTF_ShouldFail              8 tight              ✓       ✓       ✓

Total: 12 properties, 8 specs                                                12/12   10/10    7/7


   The “n/a” entries in the Selective −1 column correspond to positive properties (holds at
base): for these, no single per-class decrement is expected to change the outcome, and indeed
none did. The two cases with dominant formula coarse/sharp/tight are properties where
multiple bound formulas agree at the minimum, so the experiment cannot distinguish which is
binding; this is recorded as a dominant-formula tie rather than as a separate result.

Reproducibility and full per-property breakdown. The experiment is driven by a ded-
icated K-boundary experiment driver in the companion repository [16], which computes the
per-class bounds, performs the uniform sweep and selective perturbations symbolically through
the SMT backend, and feeds the concrete witnesses through the same concrete execution engine
described in Section 6. The complete per-property breakdown—including every offset’s solver
time, every per-class perturbation, every concrete input, and the formula values Kcoarse , Ksharp ,
Ksharp2 , Ktight for every property—is published as a markdown report inside the same reposi-
tory, under docs/evaluation/k_boundary_expanded_results.md. Re-running the experiment
regenerates that document end-to-end.


D      Benchmark Corpus Details
Table 6 summarizes the provenance, size, and domain of each transformation in the evaluation
corpus.




                                                40
  Table 6: Transformation corpus provenance and metrics (29 transforms, 899 properties).
Transformation              Source               Rules   Layers   Props   Domain
Primary benchmark suites
ATLCompiler                 ATL Zoo                 55        9      20   Compiler
BibTeX2DocBook              ATL Zoo                 11        3      33   Bibliography
BPMN2Petri                  ATL Zoo                 12        3       5   Process
Class2Relational            ATL Zoo / TTC           18        6      29   Database
Ecore2JsonSchema            Community                5        3      20   Schema
FSM2PetriNet                ATL Zoo                  3        3      10   Behavioral
KM32OWL                     Community                6        3      20   Ontology
OCLCompiler                 ATL Zoo                 29        6      40   Compiler
Persons                     DSLTrans                 9        3       9   Social
PNML2NUPN                   Community                5        3      20   Petri nets
SimplePDL2Tina              ATL Zoo                  6        3      20   Process
Statechart2Flow             ATL Zoo                  3        3      20   Behavioral
Tree2Graph                  DSLTrans                 2        2       6   Graph
UML2Java                    Custom                  22        6      29   Software
University2ITSystem         DSLTrans                 8        5      21   Enterprise
UseCase2Activity            ATL Zoo                  3        3      12   Behavioral
Graph-mapping suite (common template)
Component2Deploy.         ATL Zoo                    3        3      20   Graph
ER2Relational             ATL Zoo                    3        3      20   Graph
Family2Social             ATL Zoo                    3        3      20   Graph
FeatureModel2Conf.        ATL Zoo                    3        3      20   Graph
Mindmap2Graph             ATL Zoo                    3        3      20   Graph
Org2AccessControl         ATL Zoo                    3        3      20   Graph
Workflow2PetriNet         ATL Zoo                    3        3      20   Graph
Synthetic and stress benchmarks
Attributes                   DSLTrans                1        1       3   K-boundary
DeepDependency               DSLTrans                4        4       2   K-boundary
TargetTightBound.            DSLTrans                3        1       3   K-boundary
Scalability                  Synthetic              67       14      17   Stress
MegaStress                   Synthetic              78        3     100   Stress
UltraStress                  Synthetic             200        3     300   Stress




                                            41
