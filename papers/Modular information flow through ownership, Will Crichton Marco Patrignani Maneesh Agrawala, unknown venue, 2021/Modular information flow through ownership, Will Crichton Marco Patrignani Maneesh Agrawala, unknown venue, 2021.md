                                                   Modular Information Flow through Ownership
                                                          Will Crichton                                    Marco Patrignani                         Maneesh Agrawala
                                                       Stanford University                                University of Trento                        Pat Hanrahan
                                                          Stanford, USA                                       Trento, Italy                           Stanford University
                                                    wcrichto@cs.stanford.edu                            marco.patrignani@unitn.it                        Stanford, USA
                                         Abstract                                                                        1. Applicable to common language features: the lan-
                                         Statically analyzing information flow, or how data influences                      guage being analyzed should support widely used features
                                         other data within a program, is a challenging task in impera-                      like pointers and in-place mutation.
                                         tive languages. Analyzing pointers and mutations requires                       2. Zero configuration to run on existing code: the ana-
                                         access to a program’s complete source. However, programs                           lyzer must integrate with an existing language and exist-
arXiv:2111.13662v2 [cs.PL] 15 Mar 2022




                                         often use pre-compiled dependencies where only type sig-                           ing unannotated programs. It must not require users to
                                         natures are available. We demonstrate that ownership types                         adopt a new language designed for information flow.
                                         can be used to soundly and precisely analyze information                        3. No dynamic analysis: to reduce integration challenges
                                         flow through function calls given only their type signature.                       and costs, the analyzer must be purely static — no modifi-
                                         From this insight, we built Flowistry, a system for analyzing                      cations to runtimes or binaries are needed.
                                         information flow in Rust, an ownership-based language. We                       4. Modular over dependencies: programs may not have
                                         prove the system’s soundness as a form of noninterference                          source available for dependencies. The analyzer must have
                                         using the Oxide formal model of Rust. Then we empirically                          reasonable precision without whole-program analysis.
                                         evaluate the precision of Flowistry, showing that modular
                                         flows are identical to whole-program flows in 94% of cases                         As a case study on the challenges imposed by these re-
                                         drawn from large Rust codebases. We illustrate the applica-                     quirements, consider analyzing the information that flows
                                         bility of Flowistry by using it to implement prototypes of a                    to the return value in this C++ function:
                                         program slicer and an information flow control system.
                                                                                                                         1   // Copy elements 0 to max into a new vector
                                         CCS Concepts: • Software and its engineering → Auto-                            2   vector<int> copy_to(vector<int>& v, size_t max) {
                                         mated static analysis.                                                          3     vector<int> v2; size_t i = 0;
                                         Keywords: information flow, ownership types, rust                               4     for (auto x(v.begin()); x != v.end(); ++x) {
                                                                                                                         5       if (i == max) { break; }
                                         ACM Reference Format:                                                           6       v2.push_back(*x); ++i;
                                         Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Han-                 7     }
                                         rahan. 2022. Modular Information Flow through Ownership. In                     8     return v2;
                                         Proceedings of the 43rd ACM SIGPLAN International Conference on                 9   }
                                         Programming Language Design and Implementation (PLDI ’22), June
                                         13–17, 2022, San Diego, CA, USA. ACM, New York, NY, USA, 17 pages.
                                         https://doi.org/10.1145/3519939.3523445                                         Here, a key flow is that v2 is influenced by v: (1) push_back
                                                                                                                         mutates v2 with *x as input, and (2) x points to data within
                                                                                                                         v. But how could an analyzer statically deduce these facts?
                                         1    Introduction                                                               For C++, the answer is by looking at function implementa-
                                         Information flow describes how data influences other data                       tions. The implementation of push_back mutates v2, and the
                                         within a program. Information flow has applications to secu-                    implementation of begin returns a pointer to data in v.
                                         rity, such as information flow control [31], and to developer                      However, analyzing such implementations violates our
                                         tools, such as program slicing [37]. Our goal is to build a                     fourth requirement, since these functions may only have
                                         practical system for analyzing information flow, meaning:                       their type signature available. In C++, given only a function’s
                                                                                                                         type signature, not much can be inferred about its behavior,
                                         PLDI ’22, June 13–17, 2022, San Diego, CA, USA                                  since the type system does not contain information relevant
                                         © 2022 Copyright held by the owner/author(s). Publication rights licensed       to pointer analysis.
                                         to ACM.                                                                            Our key insight is that ownership types can be leveraged to
                                         This is the author’s version of the work. It is posted here for your personal   modularly analyze pointers and mutation using only a func-
                                         use. Not for redistribution. The definitive Version of Record was published     tion’s type signature. Ownership has emerged from several
                                         in Proceedings of the 43rd ACM SIGPLAN International Conference on Pro-
                                         gramming Language Design and Implementation (PLDI ’22), June 13–17, 2022,       intersecting lines of research on linear logic [16], class-based
                                         San Diego, CA, USA, https://doi.org/10.1145/3519939.3523445.                    alias management [8], and region-based memory manage-
                                                                                                                         ment [18]. The fundamental law of ownership is that data
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                      Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


cannot be simultaneously aliased and mutated. Ownership-            5. We demonstrate the utility of Flowistry by using it to
based type systems enforce this law by tracking which enti-            prototype a program slicer and an IFC checker (Section 6).
ties own which data, allowing ownership to be transferred              We conclude by presenting related work (Section 7) and
between entities, and flagging ownership violations like mu-        discussing future directions for Flowistry (Section 8). Due
tating immutably-borrowed data.                                     to space constraints, we omit many formal details, all auxil-
   Today, the most popular ownership-based language is Rust.        iary lemmas, and all proofs. The interested reader can find
Consider the information flows in this Rust implementation          them in Appendix A. Flowistry and our applications of it
of copy_to:                                                         are publicly available, open-source, MIT-licensed projects at
1   fn copy_to(v: &Vec<i32>, max: usize) -> Vec<i32> {              https://github.com/willcrichton/flowistry.
2     let mut v2 = Vec::new();
3     for (i, x) in v.iter().enumerate() {                          2   Analysis
4       if i == max { break; }                                      Inspired by the dependency calculus of Abadi et al. [1], our
5       v2.push(*x);                                                analysis represents information flow as a set of dependen-
6     }                                                             cies for each variable in a given function. The analysis is
7     return v2;                                                    flow-sensitive, computing a different dependency set at each
8   }                                                               program location, and field-sensitive, distinguishing between
                                                                    dependencies for fields of a data structure.
Focus on the two methods push and iter. For a Vec<i32>,                While the analysis is implemented in and for Rust, our
these methods have the following type signatures:                   goal here is to provide a description of it that is both concise
1   fn push(&mut self, value: i32);                                 (for clarity of communication) and precise (for amenability
2   fn iter<'a>(&'a self) -> Iter<'a, i32>;                         to proof). We therefore base our description on Oxide [38], a
To determine that push mutates v2, we leverage mutability           formal model of Rust. At a high level, Oxide provides three
modifiers. All references in Rust are either immutable (i.e. the    ingredients:
type is &T) or mutable (the type is &mut T). Therefore iter         1. A syntax of Rust-like programs with expressions 𝑒 and
does not mutate v because it takes &self as input (excepting           types 𝜏.
interior mutability, discussed in Section 4.3), while push may      2. A type-checker, expressed with the judgment Σ; Δ; Γ ⊢ 𝑒 :
mutate v2 because it takes &mut self as input.                         𝜏 ⇒ Γ ′ using the contexts Γ for types and lifetimes, Δ for
   To determine that x points to v, we leverage lifetimes. All         type variables, and Σ for global functions.
references in Rust are annotated with a lifetime, either ex-        3. An interpreter, expressed by a small-step operational se-
plicitly (such as 'a) or implicitly. Shared lifetimes indicate         mantics with the judgment Σ ⊢ (𝜎; 𝑒) → (𝜎 ′; 𝑒 ′) using 𝜎
aliasing: because &self in iter has lifetime 'a, and because           for a runtime stack.
the returned Iter structure shares that lifetime, then we can          We extend this model by assuming that each expression
determine that Iter may contain pointers to self.                   in a program is automatically labeled with a unique loca-
   Inspired by this insight, we built Flowistry, a system for       tion ℓ. Then for a given expression 𝑒, our analysis computes
analyzing information flow in the safe subset of Rust pro-          the set of dependencies 𝜅 ::= {ℓ }. Because expressions have
grams. Flowistry satisfies our four design criteria: (1) Rust       effects on persistent memory, we further compute a depen-
supports pointers and mutation, (2) Flowistry does not re-          dency context Θ ::= {𝑝 ↦→ 𝜅} from memory locations 𝑝 to
quire any change to the Rust language or to Rust programs,          dependencies 𝜅. The computation of information flow is in-
(3) Flowistry is a purely static analysis, and (4) Flowistry        tertwined with type-checking, represented as a modified
uses ownership types to analyze function calls without need-        type-checking judgment (additions highlighted in red):
ing their definition. This paper presents a theoretical and
empirical investigation into Flowistry in five parts:                               Σ; Δ; Γ; Θ ⊢ 𝑒 ℓ : 𝜏 • 𝜅 ⇒ Γ ′; Θ′
1. We provide a precise description of how Flowistry com-           This judgment is read as, “with type contexts Σ, Δ, Γ and
   putes information flow by embedding its definition within        dependency context Θ, 𝑒 at location ℓ has type 𝜏 and depen-
   Oxide [38], a formal model of Rust (Section 2).                  dencies 𝜅, producing a new dependency context Θ′.”
2. We prove the soundness of our information flow analysis             Oxide is a large language — describing every feature, judg-
   as a form of noninterference (Section 3).                        ment, and inference rule would exceed our space constraints.
3. We describe the implementation of Flowistry that bridges         Instead, in this section we focus on a few key rules that
   the theory of Oxide to the practicalities of Rust (Section 4).   demonstrate the novel aspects of our system. We first lay
4. We evaluate the precision of the modular analysis on a           the foundations for dealing with variables and mutation
   dataset of large Rust codebases, finding that modular flows      (Section 2.1), and then describe how we modularly analyze
   are identical to whole-program flows in 94% of cases, and        references (Section 2.2) and function calls (Section 2.3). The
   are on average 7% larger in the remaining cases (Section 5).     remaining rules can be found in Appendix A.1.
Modular Information Flow through Ownership                                                           PLDI ’22, June 13–17, 2022, San Diego, CA, USA


2.1     Variables and mutation                                             a root variable 𝑥. Second, Θ1 [𝜋 ↦→ 𝜅 1 ] means “set 𝜋 to 𝜅 1 in
The core of Oxide is an imperative calculus with constants                 Θ1 ”. So this rule specifies that when checking 𝑒 2 , all places
and variables. The abstract syntax for these features is below:            within 𝑥 are initialized to the dependencies 𝜅 1 of 𝑒 1 .
                                                                              Next, the assignment expression rule is defined as updat-
                        Variable 𝑥         Number 𝑛                        ing all the conflicts of a place 𝜋:
                   Path 𝑞 ::= 𝜀 | 𝑛.𝑞
                                                                             T-Assign
                  Place 𝜋 ::= 𝑥 .𝑞                                                        Σ; Δ; Γ; Θ ⊢ 𝑒 : 𝜏 si • 𝜅 ⇒ Γ1 ; Θ1
             Constant 𝑐 ::= () | 𝑛 | true | false                             Γ1 (𝜋) = 𝜏  sx
                                                                                               (𝜏 sx = 𝜏 sd ∨ Δ; Γ1 ⊢uniq 𝜋 ⇒ { uniq 𝜋 })
          Base Type 𝜏 b ::= unit | u32 | bool                                                  Δ; Γ1 ⊢ 𝜏 si ≲ 𝜏 sx ⇒ Γ ′
                                                                                       Θ2 = Θ1 [update-conflicts (Θ1, 𝜋, 𝜅)]
         Sized Type 𝜏 si ::= 𝜏 b | (𝜏1si, . . . , 𝜏𝑛si ) | . . .
           Expression 𝑒 ::= 𝑐 | 𝜋 | let 𝑥 : 𝜏𝑎si = 𝑒 1 ; 𝑒 2 |                   Σ; Δ; Γ; Θ ⊢ 𝜋 := 𝑒 : unit • ∅ ⇒ Γ ′ [𝜋 ↦→ 𝜏 si ] ▷ 𝜋; Θ2

                                 𝜋 := 𝑒 | 𝑒 1 ; 𝑒 2 | . . .                   If you conceptualize a type as a tree and a path as a node
                                                                           in that tree, then a node’s conflicts are its ancestors and
   Constants are Oxide’s atomic values and also the base-
                                                                           descendants (but not siblings). Semantically, conflicts are the
case for information flow. A constant’s dependency is simply
                                                                           set of places whose value change if a given place is mutated.
itself, expressed through the T-u32 rule:
                                                                           Recall from the previous example that 𝑡 .1 conflicts with 𝑡
                 T-u32                                                     and 𝑡 .1, but not 𝑡 .0. Formally, we say two places are disjoint
                                                                           (#) or conflict (⊓) when:
                 Σ; Δ; Γ; Θ ⊢ 𝑛 ℓ : u32 • {ℓ } ⇒ Γ; Θ                                          def
                                                                            𝑥 1 .𝑞 1 # 𝑥 2 .𝑞 2 = 𝑥 1 ≠ 𝑥 2 ∨ (   (𝑞 1 is not a prefix of 𝑞 2 ) ∧
   Variables and mutation are introduced through let-bindings                                                     (𝑞 2 is not a prefix of 𝑞 1 ))
and assignment expressions, respectively. For example, this
                                                                                               def
(location-annotated) program mutates a field of a tuple:                            𝜋1 ⊓ 𝜋2 = ¬(𝜋1 # 𝜋2 )
             let 𝑡 : (u32, u32) = (1ℓ1 , 2ℓ2 ); 𝑡 .1 := 3ℓ3                   Then to update a place’s conflicts in Θ, we define the meta-
   Here, 𝑡 is a variable and 𝑡 .1 is a place, or a description of          function update-conflicts to add 𝜅 to all conflicting places 𝑝 ′.
a specific region in memory. For information flow, the key                 (Note that this rule is actually defined over place expressions
idea is that let-bindings introduce a set of places into Θ, and            𝑝, which are explained in the next subsection.)
then assignment expressions change a place’s dependencies                                                            def
within Θ. In the above example, after binding 𝑡, then Θ is:                           update-conflicts (Θ, 𝑝, 𝜅) =
                                                                                           ∀𝑝 ′ ↦→ 𝜅𝑝 ′ ∈ Θcfl . 𝑝 ′ ↦→ 𝜅𝑝 ′ ∪ 𝜅
                       Θ = {𝑡, 𝑡 .0, 𝑡 .1 ↦→ {ℓ1, ℓ2 }}
                                                                                           where Θcfl = {𝑝 ′ ↦→ 𝜅𝑝 ′ ∈ Θ | 𝑝 ⊓ 𝑝 ′ }
After checking “𝑡 .1 := 3”, then ℓ3 is added to Θ(𝑡) and
Θ(𝑡 .1), but not Θ(𝑡 .0). This is because the values of 𝑡 and                Finally, the rule for reading places is simply to look up the
𝑡 .1 have changed, but the value of 𝑡 .0 has not. Formally, the            place’s dependencies in Θ:
let-binding rule is:
                                                                           T-Move
T-Let                                                                      Δ; Γ ⊢uniq 𝜋 ⇒ { uniq 𝜋 }          Γ(𝜋) = 𝜏 si     noncopyableΣ 𝜏 si
             Σ; Δ; Γ; Θ ⊢ 𝑒 1 : 𝜏1si • 𝜅 1 ⇒ Γ1 ; Θ1
                                                                                     Σ; Δ; Γ; Θ ⊢ 𝜋 : 𝜏 si • Θ(𝜋) ⇒ Γ [𝜋 ↦→ 𝜏 si ]; Θ
                                                                                                                                    †
Γ; Δ1 ⊢ 𝜏1 ≲ 𝜏𝑎si ⇒ Γ1′
          si
                               Θ1′ = Θ1 [∀𝜋 = 𝜋 □ [𝑥] . 𝜋 ↦→ 𝜅 1 ]
Σ; Δ; gc-loans(Γ1 , 𝑥 : 𝜏𝑎 ); Θ1′ ⊢ 𝑒 2 : 𝜏2si • 𝜅 2 ⇒ Γ2, 𝑥 : 𝜏 sd ; Θ2
                 ′       si
                                                                           2.2     References
      Σ; Δ; Γ; Θ ⊢ let 𝑥 : 𝜏𝑎si = 𝑒 1 ; 𝑒 2 : 𝜏2si • 𝜅 2 ⇒ Γ2 ; Θ2
                                                                           Beyond concrete places in memory, Oxide also contains ref-
   Again, this rule (and many others) contain aspects of Oxide             erences that point to places. As in Rust, these references
that are not essential for understanding information flow                  have both a lifetime (called a “provenance”) and a mutability
such as the subtyping judgment 𝜏1 ≲ 𝜏2 or the metafunction                 qualifier (called an “ownership qualifier”). Their syntax is:
gc-loans. For brevity we will not cover these aspects here,
                                                                                  Concrete Provenance 𝑟           Abstract Provenance 𝜚
and instead refer the interested reader to Weiss et al. [38]. We
have deemphasized (in grey) the judgments which are not                          Place Expression 𝑝 ::= 𝑥 | ∗𝑝 | 𝑝.𝑛
important to understanding our information flow additions.                             Provenance 𝜌 ::= 𝜚 | 𝑟
   The key concept is the formula Θ1 [∀𝜋 = 𝜋 □ [𝑥] . 𝜋 ↦→ 𝜅 1 ].
                                                                           Ownership Qualifier 𝜔 ::= shrd | uniq
This introduces two shorthands: first, 𝜋 □ [𝑥] means “a place
𝜋 with root variable 𝑥 in a context 𝜋 □ ”, used to decompose a                        Sized Type 𝜏 si ::= . . . | &𝜌 𝜔 𝜏 xi
place. In T-Let, the update to Θ1 happens for all places with                           Expression 𝑒 ::= . . . | &𝑟 𝜔 𝑝 | 𝑝 := 𝑒 | letprov ⟨𝑟 ⟩ 𝑒
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                           Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


   Provenances are created via a letprov expression, and                 4. Checking “&𝑟 3 uniq (∗𝑦).1” gets the loan set for (∗𝑦).1,
references are created via a borrow expression &𝑟 𝜔 𝑝 that                  which is:
has an initial concrete provenance 𝑟 (abstract provenances
                                                                         {uniq𝑝.1 | uniq 𝑝 ∈ Γ(𝑟 2 )}∪{uniq (∗𝑦).1} = {uniq𝑥 .1, uniq (∗𝑦).1}
are just used for types of function parameters). References
are used in conjunction with place expressions 𝑝 that are                   That is, the loans for 𝑟 2 are looked up in Γ (to get {𝑥 }),
places whose paths contain dereferences. For example, this                  and then the additional projection _.1 is added on-top of
program creates, reborrows, and mutates a reference:                        each loan (to get {𝑥 .1}).
                                                                         5. Then Γ(𝑟 4 ) = Γ(𝑟 3 ) because 𝑟 3 :> 𝑟 4 .
           letprov ⟨𝑟 1, 𝑟 2, 𝑟 3, 𝑟 4 ⟩
                                                                         6. Finally, the loan set for ∗𝑧 is:
           let 𝑥 : (u32, u32) = (0, 0);
                                                                                 Γ(𝑟 4 ) ∪ {uniq (∗𝑧)} = {uniq𝑥 .1, uniq (∗𝑦).1, uniq (∗𝑧)}
           let 𝑦 : &𝑟 2 uniq (u32, u32) = &𝑟 1 uniq 𝑥;
                                                                            Applying this concept to the T-AssignDeref rule, we
           let 𝑧 : &𝑟 4 uniq u32 = &𝑟 3 uniq (∗𝑦).1;
                                                                         compute information flow for reference-mutation as: when
           ∗𝑧 := 1ℓ                                                      mutating 𝑝 with loans {𝑙 }, add 𝜅𝑒 to all the conflicts for every
Consider the information flow induced by ∗𝑧 := 1ℓ . We need              loan uniq𝑝 ′ ∈ {𝑙 }.
to compute all places that 𝑧 could point-to, in this case 𝑥 .1,
so ℓ can be added to the conflicts of 𝑥 .1. Essentially, we must         2.3     Function calls
perform a pointer analysis [33].                                         Finally, we examine how to modularly compute information
   The key idea is that Oxide already does a pointer analysis!           flow through function calls, starting with syntax:
Performing one is an essential task in ensuring ownership-                                       Type Var 𝛼   Frame Var 𝜑
safety. All we have to do is extract the relevant information
with Oxide’s existing judgments. This is represented by the                 Expression 𝑒 ::= . . . | 𝑓 ⟨Φ, 𝜌, 𝜏⟩(𝜋)
information flow extension to the reference-mutation rule:                Global Entry 𝜀 ::= fn 𝑓 ⟨𝜑, 𝜚, 𝛼, 𝜚 1 : 𝜚 2 ⟩(𝑥 : 𝜏𝑎si ) → 𝜏𝑟si { 𝑒 }
    T-AssignDeref                                                         Global Env. Σ ::= • | Σ, 𝜀
    Σ; Δ; Γ; Θ ⊢ 𝑒 : 𝜏𝑛si • 𝜅 ⇒ Γ1 ; Θ1      Δ; Γ1 ⊢uniq 𝑝 : 𝜏𝑜si
                                                                            Oxide functions are parameterized by frame variables 𝜑
        Δ; Γ1 ⊢uniq 𝑝 ⇒ {𝑙 }        Δ; Γ1 ⊢ 𝜏𝑛 ≲ 𝜏𝑜si ⇒ Γ ′
                                             si
                                                                         (for closures), abstract provenances 𝜚 (for provenance poly-
     Θ2 = Θ1 [∀ 𝜔 𝑝 ′ ∈ {𝑙 } . update-conflicts (Θ1, 𝑝 ′, 𝜅)]            morphism), and type variables 𝛼 (for type polymorphism).
          Σ; Δ; Γ; Θ ⊢ 𝑝 := 𝑒 : unit • ∅ ⇒ Γ ′ ▷ 𝑝; Θ2                   Unlike Oxide, we restrict to functions with one argument
   Here, the important concept is Oxide’s ownership safety               for simplicity in the formalism. Calling a function 𝑓 requires
                                                                         an argument 𝜋 and any type-level parameters Φ, 𝜌 and 𝜏.
judgment: Δ; Γ ⊢𝜔 𝑝 ⇒ {𝑙 }, read as “in the contexts Δ and Γ,
                                                                            The key question is: without inspecting its definition, what
𝑝 can be used 𝜔-ly and points to a loan in {𝑙 }.” A loan 𝑙 ::= 𝜔 𝑝       is the most precise assumption we can make about a func-
is a place expression with an ownership-qualifier. In Oxide,             tion’s information flow while still being sound? By “precise”
this judgment is used to ensure that a place is used safely at a         we mean “if the analysis says there is a flow, then the flow
given level of mutability. For instance, in the example at the           actually exists”, and by “sound” we mean “if a flow actually
top of this column, if ∗𝑧 := 1 was replaced with 𝑥 .1 := 1, then         exists, then the analysis says that flow exists.” For example
this would violate ownership-safety because 𝑥 is already                 consider this program:
borrowed by 𝑦 and 𝑧.
   In the example as written, the ownership-safety judgment                    fn f⟨𝜚 1, 𝜚 2 ⟩(𝑥 : (&𝜚 1 uniq u32, &𝜚 2 shrd u32)){ ??? }
for ∗𝑧 would compute the loan set:                                             let 𝑥 : u32 = 1ℓ1 ; let 𝑦 : u32 = 2ℓ2 ;
               {𝑙 } = {   uniq
                                 (∗𝑧),   uniq
                                                (∗𝑦).1,   uniq
                                                                 𝑥 .1}         letprov ⟨𝑟 1, 𝑟 2 ⟩ let 𝑡 : (&𝑟 1 uniq u32, &𝑟 2 shrd u32)
                                                                                   = (&𝑟 1 uniq 𝑥, &𝑟 2 shrd 𝑦);
Note that 𝑥 .1 is in the loan set of ∗𝑧. That suggests the loan
set can be used as a pointer analysis. The complete details                    f⟨𝑟 1, 𝑟 2 ⟩(𝑡)
of computing the loan set can be found in Weiss et al. [38,                  First, what can f (𝑡) mutate? Any data behind a shared ref-
p. 12], but the summary for this example is:                             erence is immutable, so only ∗𝑡 .0 could possibly be mutated,
1. Checking the borrow expression “&𝑟 1 uniq 𝑥” gets the loan            not ∗𝑡 .1. More generally, the argument’s transitive mutable
   set for 𝑥, which is just {uniq𝑥 }, and so sets Γ(𝑟 1 ) = {uniq𝑥 }.    references must be assumed to be mutated.
2. Checking the assignment “𝑦 = &𝑟 1 uniq 𝑥” requires that                   Second, what are the inputs to the mutation of ∗𝑡 .0? This
   &𝑟 1 uniq (u32, u32) is a subtype of &𝑟 2 uniq (u32, u32), which      could theoretically be any possible value in the input, so both
   requires that 𝑟 1 “outlives” 𝑟 2 , denoted 𝑟 1 :> 𝑟 2 .               ∗𝑡 .0 and ∗𝑡 .1. More generally, every transitively readable place
3. The constraint 𝑟 1 :> 𝑟 2 adds Γ(𝑟 1 ) to Γ(𝑟 2 ), so Γ(𝑟 2 ) =       from the argument must be assumed to be to be an input to
   {uniq𝑥 }.                                                             the mutation. So in this example, a modular analysis of the
Modular Information Flow through Ownership                                                                  PLDI ’22, June 13–17, 2022, San Diego, CA, USA


information flow from calling cp would add {ℓ1, ℓ2 } to Θ(𝑥)                        execution contexts, if the dependencies are equal between
but not Θ(𝑦).                                                                       contexts, then the program will execute with the same ob-
   To formalize these concepts, we first need to describe                           servable behavior in both cases. For our analysis, we focus
the transitive references of a place. The 𝜔-refs(𝑝, 𝜏) meta-                        just on values produced by the program, instead of other
function computes a place expression for every reference                            behaviors like termination or timing.
accessible from 𝑝. If 𝜔 = uniq then this just includes unique                         To formally define noninterference within Oxide, we first
references, otherwise it includes unique and shared ones.                           need to explore Oxide’s operational semantics. Oxide pro-
          𝜔-refs(𝑝, 𝜏 b ) = ∅                                                       grams are executed in the context of a stack of frames that
                                                                                    map variables to values:
𝜔-refs(𝑝, (𝜏1si, . . . , 𝜏𝑛si )) = 𝑖 𝜔-refs(𝑝.𝑖, 𝜏𝑖si )
                                  Ð
                                                                                                             Stack 𝜎 ::= • | 𝜎 ♮ 𝜍
                                    {∗𝑝} ∪ 𝜔-refs(∗𝑝, 𝜏 xi )       if 𝜔 ≲ 𝜔 ′
                                  (
  𝜔-refs(𝑝, &𝜌 𝜔 𝜏 ) =  ′ xi                                                                        Stack Frame 𝜍 ::= • | 𝜍, 𝑥 ↦→ 𝑣
                                    ∅                              otherwise
                                                                                       For example, in the empty stack •, the expression “let 𝑥 :
   Here, 𝜔 ≲ 𝜔 ′ means “a loan at 𝜔 can be used as a loan                           u32 = 1; 𝑥 := 2” would first add 𝑥 ↦→ 1 to the stack. Then
at 𝜔 ′”, defined as uniq shrd and 𝜔 ≲ 𝜔 ′ otherwise. Then                           executing 𝑥 := 2 would update 𝜎 (𝑥) = 2. More generally,
𝜔-loans(𝑝, 𝜏, Δ, Γ) can be defined as the set of concrete places                    we use the shorthand 𝜎 (𝑝) to mean “reduce 𝑝 to a concrete
accessible from those transitive references:                                        location 𝜋, then look up the value of 𝜋 in 𝜎.”
 𝜔-loans(𝑝, 𝜏, Δ, Γ) =
                            def                                                        The key ingredient for noninterference is the equivalence
                                                                                    of dependencies between stacks. That is, for two stacks 𝜎1
                                             where Δ; Γ ⊢𝜔 𝑝 1 ⇒ {𝑙 }
       Ø
                {𝑝 2 | 𝜔 𝑝 2 ∈ {𝑙 }}                                                and 𝜎2 and a set of dependencies 𝜅 in a context Θ, we say
     𝑝 1 ∈𝜔-refs(𝑝,𝜏)                                                               those stacks are the same up to 𝜅 if all 𝑝 with Θ(𝑝) ⊆ 𝜅 are
                                                                                    the same between stacks. Formally, the dependencies of 𝜅
  Finally, the function application rule can be revised to                          and equivalence of heaps are defined as:
include information flow as follows:
                                                                                                            def
T-App                                                                                        deps(Θ, 𝜅) = {𝑝 | 𝑝 ↦→ 𝜅𝑝 ∈ Θ ∧ 𝜅𝑝 ⊆ 𝜅}
             Σ; Δ; Γ ⊢ Φ        Δ; Γ ⊢ 𝜌              Σ; Δ; Γ ⊢ 𝜏 si                                        def
                                                                                                𝜎1 ∼𝑃 𝜎2 = ∀𝑝 ∈ 𝑃 . 𝜎1 (𝑝) = 𝜎2 (𝑝)
         Σ(𝑓 ) = fn 𝑓 ⟨𝜑, 𝜚, 𝛼, 𝜚 1 : 𝜚 2 ⟩(𝑥 : 𝜏𝑎si ) → 𝜏𝑟si { 𝑒 }
                                                                                                            def
          Σ; Δ; Γ; Θ ⊢ 𝜋 : 𝜏𝑎si [ Φ/𝜑 ] [ 𝜌/𝜚 ] [𝜏 si/𝛼 ] • 𝜅 ⇒ Γ1 ; Θ                          𝜎1 ∼𝜅Θ 𝜎2 = 𝜎1 ∼deps(Θ,𝜅) 𝜎2
                     Δ; Γ1 ⊢ 𝜚Ð2 [ 𝜌/𝜚 ] :> 𝜚 1 [ 𝜌/𝜚 ] ⇒ Γ2                          Then we define noninterference as follows:
                𝜅 arg = 𝜅 ∪ 𝑝 ∈shrd-loans(𝜋,𝜏𝑎si,Δ,Γ2 ) Θ(𝑝)
                                                                                    Theorem 3.1 (Noninterference). Let 𝑒 such that:
               Θ   ′
                       = Θ[∀𝑝 ∈ uniq-loans(𝜋, 𝜏𝑎si, Δ, Γ2 ) .                                       Σ; •; Γ; Θ ⊢ 𝑒 : 𝜏 • 𝜅 ⇒ Γ ′; Θ′
                            update-conflicts Θ, 𝑝, 𝜅 arg ]
                                                             
                                                                                    For 𝑖 ∈ {1, 2}, let 𝜎𝑖 such that:
Σ; Δ; Γ; Θ ⊢ 𝑓 ⟨Φ, 𝜌, 𝜏 si ⟩(𝜋) : 𝜏𝑟si [Φ/𝜑 ] [ 𝜌/𝜚 ] [𝜏 si/𝛼 ] • 𝜅 arg ⇒ Γ2 ; Θ′              Σ ⊢ 𝜎𝑖 : Γ     and    Σ ⊢ (𝜎𝑖 ; 𝑒) →
                                                                                                                                   ∗
                                                                                                                                  − (𝜎𝑖′; 𝑣𝑖 )
    The collective dependencies of the input 𝜋 are collected                        Then:
into 𝜅 arg , and then every unique reference is updated with
                                                                                      (a) 𝜎1 ∼𝜅Θ 𝜎2 =⇒ 𝑣 1 = 𝑣 2
𝜅 arg . Additionally, the function’s return value is assumed to
                                                                                      (b) ∀𝑝 ↦→ 𝜅𝑝 ∈ Θ′ . 𝜎1 ∼𝜅Θ𝑝 𝜎2 =⇒ 𝜎1′ (𝑝) = 𝜎2′ (𝑝)
be influenced by any input, and so has dependencies 𝜅 arg .
    Note that this rule does not depend on the body 𝑒 of the                           This theorem states that given a well-typed expression
function 𝑓 , only its type signature in Σ. This is the key to                       𝑒 and corresponding stacks 𝜎𝑖 , then its output 𝑣𝑖 should be
the modular approximation. Additionally, it means that this                         equal if the expression’s dependencies 𝜅 are initially equal.
analysis can trivially handle higher-order functions. If 𝑓                          Moreover, for any place expression 𝑝, if its dependencies in
were a parameter to the function being analyzed, then no                            the output context Θ′ are initially equal then the stack value
control-flow analysis is needed to guess its definition.                            will be the same after execution.
                                                                                       Note that the context Δ is required to be empty because an
3    Soundness                                                                      expression 𝑒 can only evaluate if it does not contain abstract
   To characterize the correctness of our analysis, we seek                         type or provenance variables. The judgment Σ ⊢ 𝜎𝑖 : Γ
to prove its soundness: if a true information flow exists in a                      means “the stack 𝜎𝑖 is well-typed under Σ and Γ”. That is, for
program, then the analysis computes that flow. The standard                         all places 𝜋 in Γ, then 𝜋 ∈ 𝜎 and 𝜎 (𝜋) has type Γ(𝜋).
soundness theorem for information flow systems is nonin-                               The proof of Theorem 3.1, found in Appendix A.2, guar-
terference [17]. At a high level, noninterference states that                       antees that we can soundly compute information flow for
for a given program and its dependencies, and for any two                           Oxide programs.
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                         Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


                                                                    start
                                                  b0
                                                   _1 = &’1 (*h)                             _1: Θ(*h) ∪ {b0[0]}
                                                   _2 = &’2 k                                _2: Θ(k) ∪ {b0[1]}
                                                   _3 = contains_key(_1, _2)                 _3: Θ(_1) ∪ Θ(_2) ∪ {b0[3]}
       1   fn get_count(                                       b1
       2     h: &mut HashMap<String, u32>,                    _4 = not _3         _4: Θ(_3) ∪ {b1[0]}
       3     k: String                                        switch _4
       4   ) -> u32 {                            b2         true             false
       5     if !h.contains_key(&k) {             insert(h, k, 0)           *h: Θ(*h) ∪ Θ(k) ∪ Θ(_4) ∪ {b1[1], b2[0]}
       6       h.insert(k, 0); 0
                                                       b6                    b3
       7     } else {
       8       *h.get(&k).unwrap()                     return 0              _5 = &’3 (*h)    _5: Θ(*h) ∪ {b3[0]}
                                                                             _6 = &’4 k       _6: Θ(k) ∪ {b3[1]}
       9     }                                                               _7 = get(_5, _6) _7: Θ(_5) ∪ Θ(_6) ∪ {b3[2]}
      10   }
                                                                             b4
                                                                              _8 = unwrap(_7)         _8: Θ(_7) ∪ {b4[0]}

                                                                                  b5
                                                                                  _9 = (*_8)      _9: Θ(_8) ∪ {b5[0]}
                                                                                  return _9

Figure 1. Example of how Flowistry computes information flow. On the left is a Rust function get_count that finds a value
in a hash map for a given key, and inserts 0 if none exists. On the right get_count is lowered into Rust’s MIR control-flow
graph, annotated with information flow. Each rectangle is a basic block, named at the top. Arrows indicate control flow (panics
omitted). Beside each instruction is the result of the information flow analysis, which maps place expressions to locations in
the CFG (akin to Θ in Section 2). For example, the insert function call adds dependencies to *h because it is assumed to be
mutated, since it is a mutable reference. Additionally, the switch instructions and _4 variable are added as dependencies to h
because the call to insert is control-dependent on the switch.

4      Implementation                                                 of instructions (basic blocks) which terminate in instructions
Our formal model provides a sound theoretical basis for               that can jump to other blocks, like a branch or function call.
analyzing information flow in Oxide. However, Rust is a               Figure 1 shows an example CFG and its information flow.
more complex language than Oxide, and the Rust compiler                  To implement the modular information flow analysis for
uses many intermediate representations beyond its surface             MIR, we reused standard static analysis techniques for CFGs,
syntax. Therefore in this section, we describe the key details        i.e., a flow-sensitive, forward dataflow analysis pass where:
of how our system, Flowistry, bridges theory to practice.             • At each instruction, we maintain a mapping from place
Specifically:                                                            expressions to a set of locations in the CFG on which the
1. Rust computes lifetime-related information on a control-              place is dependent, comparable to Θ in Section 2.
   flow graph (CFG) program representation, not the high-             • A transfer function updates Θ for each instruction, e.g.
   level AST. So we translate our analysis to work for CFGs              𝑝 := 𝑒 follows the same rules as in T-AssignDeref by
   (Section 4.1).                                                        adding the dependencies of 𝑒 to all conflicts of aliases of 𝑝.
2. Rust does not compute the loan set for lifetimes directly          • The input Θin to a basic block is the join of each   Ô of the
   like in Oxide. So we must reconstruct the loan sets given             output Θ𝑖out for each incoming edge, i.e. Θin = 𝑖 Θ𝑖out .
   the information exported by Rust (Section 4.2).                       The join operation is key-wise set union, or more precisely:
3. Rust contains escape hatches for ownership-unsafe code                              def
                                                                            Θ1 ∨ Θ2 = {𝑥 ↦→ Θ1 (𝑥) ∪ Θ2 (𝑥) | 𝑥 ∈ Θ1 ∨ 𝑥 ∈ Θ2 }
   that cannot be analyzed using our analysis. So we describe
   the situations in which our analysis is unsound for Rust           • We iterate this analysis to a fixpoint, which we are guar-
   programs (Section 4.3).                                              anteed to reach because ⟨Θ, ∨⟩ forms a join-semilattice.
                                                                        To handle indirect information flows via control flow, such
4.1        Analyzing control-flow graphs                              as the dependence of h on contains_key in Figure 1, we
The Rust compiler lowers programs into a “mid-level repre-            compute the control-dependence between instructions. We
sentation”, or MIR, that represents programs as a control-flow        define control-dependence following Ferrante et al. [15]: an
graph. Essentially, expressions are flattened into sequences          instruction 𝑋 is control-dependent on 𝑌 if there exists a
Modular Information Flow through Ownership                                               PLDI ’22, June 13–17, 2022, San Diego, CA, USA


directed path 𝑃 from 𝑋 to 𝑌 such that any 𝑍 in 𝑃 is post-          5     Evaluation
dominated by 𝑌 , and 𝑋 is not post-dominated by 𝑌 . An             Section 3 established that our analysis is sound. The next
instruction 𝑋 is post-dominated by 𝑌 if 𝑌 is on every path         question is whether it is precise: how many spurious flows
from 𝑋 to a return node. We compute control-dependencies           are included by our analysis? We evaluate two directions:
by generating the post-dominator tree and frontier of the
CFG using the algorithms of Cooper et al. [9] and Cytron           1. What if the analysis had more information? If we could
et al. [11], respectively.                                            analyze the definitions of called functions, how much
   Besides a return, the only other control-flow path out of          more precise are whole-program flows vs. modular flows?
a function in Rust is a panic. For example, each function          2. What if the analysis had less information? If Rust’s type
call in Figure 1 actually has an implicit edge to a panic node        system was more like C++, i.e. lacking ownership, then
(not depicted). Unlike exceptions in other languages, panics          how much less precise do the modular flows become?
are designed to indicate unrecoverable failure. Therefore we       To answer these questions, we created three modifications
exclude panics from our control-dependence analysis.               to Flowistry:
                                                                   • Whole-program: the analysis recursively analyzes infor-
4.2   Computing loan sets from lifetimes                             mation flow within the definitions of called functions. For
                                                                     example, if calling a function f(&mut x, y) where f does
To verify ownership-safety (perform “borrow-checking”),              not actually modify x, then the Whole-program analysis
the Rust compiler does not explicitly build the loan sets of         will not register a flow from y to x.
lifetimes (or provenances in Oxide terminology). The bor-          • Mut-blind: the analysis does not distinguish between
row checking algorithm performs a sort of flow-sensitive             mutable and immutable references. For example, if calling
dataflow analysis that determines the range of code during           a function f(&x), then the analysis assumes that x can be
which a lifetime is valid, and then checks for conflicts e.g. in     modified.
overlapping lifetimes (see the non-lexical lifetimes RFC [24]).    • Ref-blind: the analysis does not use lifetimes to reason
   However, Rust’s borrow checker relies on the same funda-          about references, and rather assumes all references of the
mental language feature as Oxide to verify ownership-safety:         same type can alias. For example, if a function takes as
outlives-constraints. For a given Rust function, Rust can out-       input f(x: &mut i32, y: &mut i32) then x and y are as-
put the set of outlives-constraints between all lifetimes in the     sumed to be aliases.
function. These lifetimes are generated in the same manner
as in Oxide, such as from inferred subtyping requirements             The Whole-program modification represents the most
or user-provided outlives-constraints. Then given these con-       precise information flow analysis we can feasibly implement.
straints, we compute loan sets via a process similar to the        The Mut-blind and Ref-blind modifications represent an
ownership-safety judgment described in Section 2.2. In short,      ablation of the precision provided by ownership types. Each
for all instances of borrow expressions &𝑟 𝜔 𝑝 in the MIR          modification can be combined with the others, representing
program, we initialize Γ(𝑟 ) = {𝑝}. Then we propagate loans        23 = 8 possible conditions for evaluation.
via Γ(𝑟 ) = 𝑟 ′ :>𝑟 Γ(𝑟 ′) until Γ reaches a fixpoint.
            Ð                                                         To better understand Whole-program, say we are ana-
                                                                   lyzing the information flow for an expression f(&mut x, y)
                                                                   where f is defined as f(a, b) { (*a).1 = b; }. After analyz-
4.3   Handling ownership-unsafe code                               ing the definition of f, we translate flows to parameters of f
Rust has a concept of raw pointers whose behavior is com-          into flows on arguments of the call to f. So the flow b → (*a
parable to pointers in C. For a type T, an immutable ref-          ).1 is translated into y → x.1. Additionally, if the definition
erence has type &T, while an immutable raw pointer has             of f is not available, then we fall back to the modular analy-
type *const T. Raw pointers are not subject to ownership           sis. Importantly, due to the architecture of the Rust compiler,
restrictions, and they can only be used in blocks of code de-      the only available definitions are those within the package
marcated as unsafe. They are primarily used to interoperate        being analyzed. Therefore even with Whole-program, we
with other languages like C, and to implement primitives           cannot recurse into e.g. the standard library.
that cannot be proved as ownership-safe via Rust’s rules.             With these three modifications, we compare the number of
   Our pointer and mutation analysis fundamentally relies          flows computed from a dataset of Rust projects (Section 5.1)
on ownership-safety for soundness. We do not try to ana-           to quantitatively (Section 5.2) and qualitatively (Section 5.3)
lyze information flowing directly through unsafe code, as it       evaluate the precision of our analysis.
would be subject to the same difficulties of C++ in Section 1.
While this limits the applicability of our analysis, empirical     5.1   Dataset
studies have shown that most Rust code does not (directly)         To empirically compare these modifications, we curated a
use unsafe blocks [2, 14]. We further discuss the impact and       dataset of Rust packages (or “crates”) to analyze. We had two
potential mitigations of this limitation in Section 8.             selection criteria:
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                       Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


              Project          Crate  Purpose                         LOC # Vars # Funcs Avg. Instrs/Func
              rayon                   Data parallelism library      15,524 10,607           1,079                  16.6
              Rocket        core/lib Web backend framework 10,688 12,040                      741                  25.5
              rustls        rustls    TLS implementation            16,866 23,407             868                  42.4
              sccache                 Distributed build cache       23,202 23,987             643                  62.1
              nalgebra                Numerics library              31,951 35,886           1,785                  26.7
              image                   Image processing library      20,722 39,077           1,096                  56.8
              hyper                   HTTP server                   15,082 44,900             790                  82.9
              rg3d                    3D game engine                54,426 59,590           3,448                  25.7
              rav1e                   Video encoder                 50,294 76,749             931                 115.4
              RustPython    vm        Python interpreter            47,927 97,637           3,315                  51.0
                                                          Total: 286,682 435,979           14,696
Table 1. Dataset of crates used to evaluate information flow precision, ordered in increasing number of variables analyzed. Each
project often contains many crates, so a sub-crate is specified where applicable, and the root crate is analyzed otherwise. Metrics
displayed are LOC (lines of code), number of variables, number of functions, and the average number of MIR instructions per
function (size of CFG).



1. To mitigate the single-crate limitation of Whole-program,                               y-linear                                          y-log
                                                                                                                                106
   we preferred large crates so as to see a greater impact from             4 · 105

   the Whole-program modification. We only considered




                                                                                                             Count, log scale
                                                                            3 · 105
   crates with over 10,000 lines of code as measured by the                                                                     104
                                                                    Count


   cloc utility [12].                                                       2 · 105
2. To control for code styles specific to individual applica-                                                                   102
                                                                            1 · 105
   tions, we wanted crates from a wide range of domains.
                                                                                 0
                                                                                      0   10−2   100   102                            0   10−2   100   102
                                                                             % difference in dependency set size, log scale (with zero)
   After a manual review of large crates in the Rust ecosys-
tem, we selected 10 crates, shown in Table 1. We built each
crate with as many feature flags enabled as would work on           Figure 2. Distribution in differences of dependency set size
our Ubuntu 16.04 machine. Details like the specific flags and       between Whole-program and Modular analyses. The x-
commit hashes can be found in Appendix A.3.                         axis is a log-scale with 0 added for comparison. Most sets
   For each crate, we ran the information flow analysis on          are the same, so 0 dominates (left). A log-scale (right) shows
every function in the crate, repeated under each of the 8           the tail more clearly.
conditions. Within a function, for each local variable 𝑥, we
compute the size of Θ(𝑥) at the exit of the CFG — in terms of       5.2        Quantitative results
program slicing, we compute the size of the variable’s back-
                                                                    We observed no meaningful patterns from the interaction
ward slice at the function’s return instructions. The resulting
                                                                    of modifications — for example, in a linear regression of
dataset then has four independent variables (crate, function,
                                                                    the interaction of Mut-blind and Ref-blind against the
condition, variable name) and one dependent variable (size
                                                                    size of the dependency set, each condition is individually
of dependency set) for a total of 3,487,832 data points.
                                                                    statistically significant (𝑝 < 0.001) while their interaction is
   Our main goal in this evaluation is to analyze precision,
                                                                    not (𝑝 = 0.337). So to simplify our presentation, we focus only
not performance. Our baseline implementation is reasonably
                                                                    on four conditions: three for each modification individually
optimized — the median per-function execution time was
                                                                    active with the rest disabled, and one for all modifications
370.24𝜇s. But Whole-program is designed to be as precise as
                                                                    disabled, referred to as Modular.
possible, so its naive recursion is sometimes extremely slow.
For example, when analyzing the GameEngine::render func-            5.2.1 Whole-program. For Whole-program, we com-
tion of the rg3d crate (with thousands of functions in its call     pare against Modular to answer our first evaluation ques-
graph), the modular analysis takes 0.13s while the recursive        tion: how much more precise is a whole-program analysis
analysis takes 23.18s, a 178× slowdown. Future work could           than a modular one? To quantify precision, we compare the
compare our modular analysis to whole-program analyses              percentage increase in size of dependency sets for a given
across the precision/performance spectrum, such as in the           variable between two conditions. For instance, if Whole-
extensive literature on context-sensitivity [33].                   program computes |Θ(𝑥)| = 2 and Modular computes
Modular Information Flow through Ownership                                                        PLDI ’22, June 13–17, 2022, San Diego, CA, USA


                               Mut-blind - Modular                           the kind of code that leads to such differences. For each
           Modular - Whole-program                Ref-blind - Modular        condition, we manually inspected a sample of cases with
                                                                             non-zero differences vs. Modular.
        10,000

                                                                             5.3.1 Modularity. One common source of imprecision in
Count




         5,000                                                               modular flows is when functions take a mutable reference
                                                                             as input for the purposes of passing the mutable permission
                                                                             off to an element of the input.
            0
                  10−2 100   102       10−2 100   102         10−2 100 102    1   fn crop<I: GenericImageView>(
                        % increase in dependency set size, log scale
                                                                              2     image: &mut I, x: u32, y: u32,
                                                                              3     width: u32, height: u32
Figure 3. Distribution in differences between Modular and                     4   ) -> SubImage<&mut I> {
each alternative condition, with zeros excluded to highlight                  5     let (x, y, width, height) =
the shape of each distribution. Mut-blind and Ref-blind                       6       crop_dimms(image, x, y, width, height);
both reduce the precision more often and more severely than                   7     SubImage::new(image, x, y, width, height)
Modular does vs. Whole-program.                                               8   }
                                                                                For example, the function crop from the image crate re-
|Θ(𝑥)| = 5 for some 𝑥, then the difference is (5 − 2)/2 =                    turns a mutable view on an image. No data is mutated,
1.5 = 150%.                                                                  only the mutable permission is passed from whole image to
   Figure 2 shows a histogram of the differences between                     sub-image. However, a modular analysis on the image input
Whole-program and Modular for all variables. In 94% of                       would assume that image is mutated by crop.
all cases, the Whole-program and Modular conditions                             Another common case is when a value only depends on
produce the same result and hence have a difference of 0.                    a subset of a function’s inputs. The modular approximation
In the remaining 6% of cases with a non-zero difference,                     assumes all inputs are relevant to all possible mutations, but
visually enhanced with a log-scale in Figure 2-right, the                    this is naturally not always the case.
metric follows a right-tailed log-normal distribution. We can                 1   fn solve_lower_triangular_with_diag_mut<R2,C2,S2>(
summarize the log-normal by computing its median, which                       2     &self, b: &mut Matrix<N, R2, C2, S2>, diag: N,
is 7%. This means that within the 6% of non-zero cases, the                   3   ) -> bool {
median difference is an increase in size by 7%. Thus, the                     4     if diag.is_zero() { return false; }
modular approximation does not significantly increase the                     5     // logic mutating b...
size of dependency sets in the vast majority of cases.                        6     true
5.2.2 Mut-blind and Ref-blind. Next, we address our                           7   }
second evaluation question: how much less precise is an anal-                  For example, this function from nalgebra returns a boolean
ysis with weaker assumptions about the program than the                      whose value solely depends on the argument diag. However,
Modular analysis? For this question, we compare the size                     a modular analysis of a call to this function would assume
of dependency sets between the Mut-blind and Ref-blind                       that self and b is relevant to the return value as well.
conditions versus Modular. Figure 3 shows the correspond-
ing histograms of differences, with the Whole-program vs.                    5.3.2 Mutability. The reason Mut-blind is less precise
Modular histogram included for comparison.                                   than Modular is quite simple — many functions take im-
   First, the Mut-blind and Ref-blind modifications reduce                   mutable references as inputs, and so many more mutations
the precision of the analysis more often and with a greater                  have to be assumed.
magnitude than Modular does vs. Whole-program. 39%                            1   fn read_until<R, F>(io: &mut R, func: F)
of Mut-blind cases and 17% of Ref-blind cases have a non-                     2     -> io::Result<Vec<u8>>
zero difference. Of those cases, the median difference in size                3     where R: Read, F: Fn(&[u8]) -> bool
is 50% for Mut-blind and 56% for Ref-blind.                                   4   {
   Therefore, the information from ownership types is valu-                   5     let mut buf = vec![0; 8192]; let mut pos = 0;
able in increasing the precision of our information flow anal-                6     loop {
ysis. Dependency sets are often larger without access to                      7       let n = io.read(&mut buf[pos..])?; pos += n;
information about mutability or lifetimes.                                    8       if func(&buf[..pos]) { break; }
5.3        Qualitative results                                                9       // ...
                                                                             10     }
The statistics convey a sense of how often each condition                    11   }
influences precision. But it is equally valuable to understand
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                                 Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


                           hyper                    image                nalgebra                    rav1e                  rayon

                4000


                2000


                  0
                       10−2      100   102       10−2   100    102      10−2     100   102        10−2   100   102       10−2   100   102
        Count




                               rg3d                Rocket                  rustls                 RustPython               sccache

                4000


                2000


                  0
                        10−2     100   102       10−2    100    102     10−2     100   102        10−2   100   102       10−2   100   102

                                                   % increase in dependency set size, log scale


            Figure 4. Distribution of non-zero differences between Modular and Mut-blind, broken down by crate.

  For instance, this function from hyper repeatedly calls an                   5.4.1 Are the results due to only a few crates? If dif-
input function func with segments of an input buffer. With-                    ferences between techniques only arose in a small number
out a control-flow analysis, it is impossible to know what                     of situations that happen to be in our dataset, then our tech-
functions read_until will be called with. And so Mut-blind                     nique would not be as generally applicable. To determine
must always assume that func could mutate buf. However,                        the variation between crates, we generated a histogram of
Modular can rely on the immutability of shared references                      non-zero differences for the Modular vs. Mut-blind com-
and deduce that func could not mutate buf.                                     parison, broken down by crate in Figure 4.
                                                                                  As expected, the larger code bases (e.g. rav1e and Rust-
5.3.3 Lifetimes. Without lifetimes, our analysis has to                        Python) have more non-zero differences than smaller code-
make more conservative assumptions about objects that                          bases — in general the correlation between non-zero dif-
could possibly alias. We observed many cases in the Ref-                       ferences and total number of variables analyzed is strong,
blind condition where two references shared different life-                    𝑅 2 = 0.79. However variation also exists for crates with
times but the same type, and so had to be classified as aliases.               roughly the same number of variables like image and hyper.
1    fn link_child_with_parent_component(                                      Mut-blind reduces precision for variables in hyper more
2       parent: &mut FbxComponent,                                             often than image. A qualitative inspection of the respective
3       child: &mut FbxComponent,                                              codebases suggests this may be because hyper simply makes
4       child_handle: Handle<FbxComponent>,                                    greater use of immutable references in its API.
 5   ) { match parent {                                                           These findings suggest that the impact of ownership types
6       FbxComponent::Model(model) => {                                        and the modular approximation likely do vary with code
 7        model.geoms.push(child_handle),                                      style, but a broader trend is still observable across all code.
 8      },
 9      // ..
                                                                               5.4.2 Would Whole-program be more precise with
10   }}
                                                                               access to dependencies? A limitation of our whole-program
  For example, the link_child_with_parent_component                            analysis is our inability to access function definitions out-
function in rg3d takes mutable references to a parent and                      side the current crate. Without this limitation, it may be
child. These references are guaranteed not to alias by the                     that the Modular analysis would be significantly worse
rules of ownership, but a naive pointer analysis must assume                   than Whole-program. So for each variable analyzed by
they could, so modifying parent could modify child.                            Whole-program, we additionally computed whether the
                                                                               information flow for that variable involved a function call
5.4    Threats to validity                                                     across a crate boundary.
Finally, we address the issue: how meaningful are the results                     Overall 96% of cases reached at least one crate boundary,
above? How likely would they generalize to arbitrary code                      suggesting that this limitation does occur quite often in prac-
rather than just our selected dataset? We discuss a few threats                tice. However, the impact of the limitation is less clear. Of the
to validity below.                                                             96% of cases that hit a crate boundary, 6.6% had a non-zero
Modular Information Flow through Ownership                                                            PLDI ’22, June 13–17, 2022, San Diego, CA, USA




 (a) A program slicer integrated into VSCode. Above, the user selects
 a slicing criterion like the variable f. Then the slicer highlights
 the criterion in green, and fades out lines that are not part of the        (b) An IFC checker. Above, the ifc_traits library exports a Secure
 backward slice on f. For example, write_all mutates the file so it          for users to mark sensitive data, like Password, and insecure oper-
 is in the slice, while metadata reads the file so it is not in the slice.   ations like insecure_print. Below, a compiler plugin invoked on
 Below, the user can manipulate aspects of a program such as com-            the program checks for information flows from data with a type im-
 menting out code related to timing. The user computes a forward             plementing Secure to insecure operations. Here insecure_print
 slice on start, adds this slice to their selection (in blue), then tells    is conditionally executed based on a read from PASSWORD, so this
 the IDE to comments out all lines in the selection.                         flow is flagged.

                                Figure 5. Two applications of information flow built using Flowistry.

difference between Modular and Whole-program. Of the                          6    Applications
4% that did not hit a crate boundary, 0.6% had a non-zero                     We have demonstrated that ownership can be leveraged to
difference. One would expect that Whole-program would                         build an information flow analysis that is static, modular,
be the most precise when the whole program is available (no                   sound, and precise. Our hope is that this analysis can serve
boundary), but instead it was much closer to Modular.                         as a building block for future static analyses. To bootstrap
   Ultimately it is not clear how much more precise Whole-                    this future, we have used Flowistry to implement prototypes
program would be given access to all a crate’s dependencies,                  of a program slicer and an IFC checker, shown in Figure 5.
but it would not necessarily be a significant improvement                        The program slicer in Figure 5a is a VSCode extension
over the benchmark presented.                                                 that fades out all lines of code that are not relevant to the
                                                                              user’s selection, i.e. not part of the modular slice. Rather
5.4.3 Is ownership actually important for precision?                          than present a slice of the entire program like in prior slicing
The finding that Ref-blind only makes a difference in 17%                     tools, we can use Flowistry’s modular analysis to present
of cases may seem surprisingly small. For instance, Shapiro                   lightweight slices of just within a given function. Users can
and Horwitz [32] found in a empirical study of slices on                      apply the slicer for comprehension tasks such as reducing
C programs that “using a pointer analysis with an average                     the scope of a bug, or for refactoring tasks such as removing
points-to set size twice as large as a more precise pointer                   an aspect of a program like timing or logging.
analysis led to an increase of about 70% in the size of [slices].”               The IFC checker in Figure 5b is a Rust library and compiler
   A limitation of our ablation is that the analyzed programs                 plugin. It provides the user a library with the traits Secure
were written to satisfy Rust’s ownership safety rules. Dis-                   and Insecure to indicate the relative security of data types
abling lifetimes does not change the structure of the pro-                    and operations. Then the compiler plugin uses Flowistry to
grams to become more C-like — Rust generally encourages a                     determine whether information flows from Insecure vari-
code style with fewer aliases to avoid dealing with lifetimes.                ables to Secure variables. Users can apply the IFC checker
A fairer comparison would be to implement an application                      to catch sensitive data leaks in an application. This proto-
idiomatically in both Rust and Rust-but-without-feature-X,                    type is purely intraprocedural, but future work could build
but such an evaluation is not practical. It is therefore likely               an interprocedural analysis by using Flowistry’s output as
that our results understate the true impact of ownership                      procedure summaries in a larger information flow graph.
types on precision given this limitation.
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                     Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


7    Related Work                                                  [20] use Rust’s ownership-based guarantees to implement
Our work draws on three core concepts: information flow,           more aggressive program optimizations.
modular static analysis, and ownership types.                         Closer to our domain, Balasubramanian et al. [5] imple-
                                                                   mented a prototype IFC system for Rust by lowering pro-
   Information flow. Information flow has been histori-            grams to LLVM and verifying them with SMACK [28], al-
cally studied in the context of security, such as ensuring         though their system is hard to contrast with ours given the
low-security users of a program cannot infer anything about        high-level description in their paper. Njor and Gústafsson
its high-security internals. Security-focused information flow     [26] implemented a static taint analysis for Rust, although it
analyses have been developed for Java [25], Javascript [4],        is not field-sensitive, alias-sensitive, or modular.
OCaml [27], Haskell [34], and many other languages.
   Each analysis satisfies some, but not all, of our require-      8    Discussion
ments from Section 1. For instance, the JFlow [25] and Flow-
                                                                   Looking forward, two interesting avenues for future work on
Caml [27] languages required adding features to the base
                                                                   Flowistry are improving its precision and addressing sound-
language, violating our second requirement. Some meth-
                                                                   ness in unsafe code. For instance, the lifetime-based pointer
ods like that of Austin and Flanagan [4] for Javascript rely
                                                                   analysis is sound but imprecise in some respects. Lifetimes
on dynamic analysis, violating our third requirement. And
                                                                   often lose information about part-whole relationships. Con-
Haskell only supports effects like mutation through monads,
                                                                   sider the function that returns a mutable pointer to a specific
violating our first requirement.
                                                                   index in a vector:
   Nonetheless, we draw significant inspiration from mech-
anisms in prior work. Our analysis resembles the slicing           1   fn get_mut<'a>(&'a mut self, i: usize)
calculus of Abadi et al. [1]. The use of lifetimes for modular     2     -> Option<&'a mut T>;
analysis of functions is comparable to security annotations        These lifetimes indicate only that the return value points to
in Flow-Caml [27]. The CFG analysis draws on techniques            something in the input vector. The expressions v.get_mut(i)
used in program slicers, such as the LLVM dg slicer [7].           and v.get_mut(i + 1) are considered aliases even though
                                                                   they are not. Future work could integrate Flowistry with
   Modular static analysis. The key technique to making
                                                                   verification tools like Prusti [3] to use abstract interpretation
static analysis modular (or “compositional” or “separate”) is
                                                                   for a more precise pointer analysis in such cases.
symbolically summarizing a function’s behavior, so that the
                                                                      Additionally, Rust has many libraries built on unsafe code
summary can be used without the function’s implementa-
                                                                   that can lose annotations essential to information flow, such
tion. Starting from Rountev et al. [29] and Cousot and Cousot
                                                                   as interior mutability. For example, shared-memory concur-
[10], one approach has been to design a system of “procedure
                                                                   rency in Rust looks like this:
summaries” understood by the static analyzer and distinct
from the language being analyzed. This approach has been           1   let n: Arc<Mutex<i32>> = Arc::new(Mutex::new(0));
widely applied for static analysis of null pointer derefer-        2   let n2: Arc<Mutex<i32>> = Arc::clone(&n);
ences [40], pointer aliases [13], data dependencies [35], and      3   *n2.lock().unwrap() = 1;
other properties.                                                  Arc::clone does not share a lifetime between its input and
   Another approach, like ours, is to leverage the language’s      output, so a lifetime-based pointer analysis therefore cannot
type system to summarize behavior. Tang and Jouvelot [36]          deduce that n2 is an alias of n, and Flowistry would not rec-
showed that an effect system could be used for a modular           ognize that the mutation on line 3 affects n. Future work can
control-flow analysis. Later work in Haskell used its powerful     explore how unsafe libraries could be annotated with the
type system and monadic effects to embed many forms of             necessary metadata needed to analyze information flow, sim-
information flow control into the language [6, 23, 30, 34].        ilar to how RustBelt [21] identifies the pre/post-conditions
   Ownership types. Rust and Oxide’s conceptions of own-           needed to ensure type safety within unsafe code.
ership derive from Clarke et al. [8] and Grossman et al. [18].        Overall, we are excited by the possibilities created by hav-
For instance, the Cyclone language of Grossman et al. uses         ing a practical information flow analysis that can run today
regions to restrict where a pointer can point-to, and uses         on any Rust program. Many exciting systems for tasks like
region variables to express relationships between regions in       debugging [22], example generation [19], and program re-
a function’s input and output types. A lifetime is similar in      pair [39] rely on information flow in some form, and we hope
that it annotates the types of pointers, but differs in how it     that Flowistry can support the development of these tools.
is analyzed.
   Recent works have demonstrated innovative applications          Acknowledgments
of Rust’s type system for modular program analysis. As-            This work was partially supported by the Italian Ministry
trauskas et al. [3] embed Rust programs into a separation          of Education through funding for the Rita Levi Montalcini
logic to verify pre/post conditions about functions. Jung et al.   grant (call of 2019).
Modular Information Flow through Ownership                                                      PLDI ’22, June 13–17, 2022, San Diego, CA, USA


A     Appendix                                                       A.2.1    Lemmas.
This appendix contains three major sections. First, in Appen-        Lemma A.1 (Mutating a place also mutates its conflicts).
dix A.1 we include information flow inference rules beyond           Let:
those presented in Section 2 for the remaining features of Ox-                  □ [𝑥], 𝜎 where 𝜎 ⊢ 𝜋 □ × 𝑥 ⇓ V
                                                                     • 𝜋mut = 𝜋mut
ide. Second, in Appendix A.2 we provide a complete proof of                                            mut
                                                                     • 𝑣 be a value and 𝜎 ′ = 𝜎 [𝑥 ↦→ V [𝑣]]
the noninterference theorem in Section 3, along with associ-
                                                                     • 𝜋any ∈ 𝜎
ated lemmas. Finally, in Appendix A.3 we provide additional
details necessary to replicate the evaluation.                       Then 𝜎 (𝜋any ) ≠ 𝜎 ′ (𝜋 any ) =⇒ 𝜋mut ⊓ 𝜋any .
                                                                     Proof.
A.1   Additional rules
                                                                     1. Assume 𝜎 (𝜋 any ) ≠ 𝜎 ′ (𝜋any ). Want to show 𝜋mut ⊓ 𝜋any .
In Figure 6, we provide the remaining information flow rules
                                                                     2. Because only 𝑥 is assigned, then 𝜋 any = 𝜋any    □ [𝑥].
for the expression forms not covered in Section 2. T-Tuple,
T-Seq, T-LetProv are relatively straightforward, so we focus         3. Assume for sake of contradiction that 𝜋mut # 𝜋any . Let 𝑞
on the remaining three rules.                                           be the shared path and 𝑛 mut, 𝑛 any be the split, i.e. 𝜋mut =
     First, T-Borrow: a borrow is unique in that its runtime            𝑥 .𝑞.𝑛 mut .𝑞 mut and 𝜋any = 𝑥 .𝑞.𝑛 any .𝑞 any .
value is a place, i.e. ptr 𝜋. A borrow &𝜋 will always have           4. By ER-Projection, then
value ptr 𝜋, so it has no dependencies. But the borrow is a               𝜎 ⊢ 𝑥 .𝑞.𝑛 mut ⇓ V [(𝑣 0, . . . , 𝑣𝑛any , . . . , □𝑛mut , . . . , 𝑣𝑛 )]
reborrow, i.e. of the form &∗𝑝, then we need to include the
dependencies of all places that 𝑝 could point-to. Therefore          5. 𝑣𝑛any = 𝜎 (𝑥 .𝑞.𝑛 any ) by induction on the derivation of V.
we include Θ(𝑝 ′) for each loan 𝑝 ′ in the loan set of 𝑝.            6. Therefore 𝜎 ′ (𝑥 .𝑞.𝑛 mut ) = 𝑣𝑛any = 𝜎 (𝑥 .𝑞.𝑛 mut ).
     Next, T-Copy shows a read from an arbitrary place expres-       7. This is a contradiction with 𝜎 (𝜋any ) ≠ 𝜎 ′ (𝜋 any ), therefore
sion 𝑝. Unlike T-Move, we have to account for 𝑝 referring               𝜋mut ⊓ 𝜋 any .
to many possible memory locations. Again this is captured                                                                             □
by the ownership-safety judgment ⊢shrd 𝑝 ⇒ {𝑙 }. Therefore
the dependencies of 𝑝 are the dependencies of any possibly           Lemma A.2 (A place expression’s loan set contains the place
read place, i.e. 𝜋 ′ Θ(𝜋 ′).
                  Ð                                                  it points-to at runtime.). Let:
     Finally, T-Branch shows how to handle conditional exe-          • 𝜎, Σ, Γ where Σ ⊢ 𝜎 : Γ
cution. The 𝜅 is simple, as the value of an if-expression could      • 𝑝 mut where •; Γ ⊢uniq 𝑝 mut ⇒ {𝑙 } and 𝜎 ⊢ 𝑝 mut ⇓ 𝜋mut
depend on either branch, 𝜅 2 ∪ 𝜅 3 , along with the condition,       • 𝑝 any where 𝜎 ⊢ 𝑝 any ⇓ 𝜋any
𝜅 1 . The more complex aspect is handling effects in Θ. The          Then 𝜋any ⊓ 𝜋 mut =⇒ ∃ uniq 𝑝 loan ∈ {𝑙 } . 𝑝 any ⊓ 𝑝 loan
core idea is that if a place 𝑝 could be mutated in either 𝑒 2 or
𝑒 3 , then that place has a control dependency on 𝑒 1 , and 𝜅 1      Proof. Proof by induction on the derivation of
should be part of the dependencies of 𝑝.                             •; Γ ⊢uniq 𝑝 mut ⇒ {𝑙 }
     To encode this idea, we introduce two new metafunctions.         (a) O-SafePlace:
First, Θ1 ⋓ Θ3 represents the union distributed over like              1. If 𝑝 any ≠ 𝜋 any then ∃𝑟 . 𝜋 any ∈ Γ(𝑟 ). But the first premise
entries:                                                                  of O-SafePlace, it must be the case that 𝜋any # 𝜋mut , a
             def                                                          contradiction. Therefore 𝑝 any = 𝜋any .
    Θ2 ⋓ Θ3 = {𝑝 ↦→ Θ2 (𝑝) ∪ Θ3 (𝑝) | 𝑝 ∈ Θ2 ∨ 𝑝 ∈ Θ3 }
                                                                       2. Then by the conclusion of O-SafePlace,
Next, we represent “could be mutated in 𝑒 2 or 𝑒 3 ” via Θ′ \ Θ1 ,        {𝑙 } = { uniq 𝜋 mut }. Then the theorem holds for 𝑝 loan =
similarly distributed over like entries:                                  𝜋mut .
           def
  Θ′ \ Θ1 = {𝑝 ↦→ Θ′ (𝑝) \ Θ1 (𝑝)                                     (b) O-Deref:
                                                                       1. Let 𝑝 mut = 𝑝 mut
                                                                                         □ [∗𝜋 ] and Γ(𝜋 ) = &𝑟 uniq 𝜏.
                                                                                                 ptr          ptr
                   | (𝑝 ∈ Θ′ ∨ 𝑝 ∈ Θ1 ) ∧ Θ′ (𝑝) \ Θ1 (𝑝) ≠ ∅}
                                                                       2. By extension of Lemma E.6 [2019, p. 47],
Then the rule says: after independently computing the con-
                                                                                   ∃ uniq 𝑝𝑖 ∈ Γ(𝑟 ) . 𝜎 ⊢ 𝑝 mut
                                                                                                             □
                                                                                                                 [𝑝𝑖 ] ⇓ 𝜋mut
texts Θ2 and Θ3 , compute a unioned context Θ′. Then for all
places 𝑝 that had new dependencies generated in 𝑒 2 or 𝑒 3 , i.e.     3. By the inductive hypothesis on
𝑝 ∈ Θ′ \ Θ1 , add 𝜅 1 to the dependencies of 𝑝.
                                                                                        •; Γ ⊢uniq 𝑝 mut
                                                                                                     □
                                                                                                         [𝑝𝑖 ] ⇒ {uniq 𝑝𝑖′ }
A.2   Proofs                                                             then:
The proof of non-interference relies on a few key lemmas                             ∃ uniq 𝑝 loan ∈ {uniq𝑝𝑖′ } . 𝑝 any ⊓ 𝑝 loan
about the semantics of Oxide. We start by defining and prov-
ing these lemmas (Appendix A.2.1), and then proceed to                 4. Because {uniq 𝑝𝑖′ } ⊆ {𝑙 }, then the theorem holds.
prove noninterference (Appendix A.2.2).                               (c) O-DerefAbs: does not apply since Δ = •.
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                                           Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


    T-Tuple                                                                                   T-Seq
                                         : 𝜏𝑖si • 𝜅𝑖 ⇒ Γ𝑖 ; Θ𝑖
            ∀𝑖 . Σ; Δ; Γ𝑖−1 ; Θ𝑖−1 ⊢ 𝑒ˆ𝑖 Ð                                                           Σ; Δ; Γ; Θ ⊢ 𝑒 1 : 𝜏1si • _ ⇒ Γ1 ; Θ1
                           𝜅 = {ℓ } ∪ 𝑖 𝜅𝑖                                                    Σ; Δ; gc-loans(Γ1 ); Θ1 ⊢ 𝑒 2 : 𝜏2si • 𝜅 2 ⇒ Γ2 ; Θ2
    Σ; Δ; Γ0 ; Θ0 ⊢ (𝑒ˆ1, . . . , 𝑒ˆ𝑛 )ℓ : (𝜏1si, . . . , 𝜏𝑛si ) • 𝜅 ⇒ Γ𝑛 ; Θ𝑛                      Σ; Δ; Γ; Θ ⊢ 𝑒 1 ; 𝑒 2 : 𝜏2si • 𝜅 2 ⇒ Γ; Θ2

                                                                                      T-Borrow
         T-LetProv                                                                                 Γ(𝑟 ) = ∅          Δ; Γ ⊢𝜔 𝑝Ð⇒ {𝑙 }
                                          si
         Σ; Δ; Γ, 𝑟 ↦→ ∅; Θ ⊢ 𝑒 : 𝜏 • 𝜅 ⇒ Γ , 𝑟 ↦→ {𝑙 }; Θ
                                                         ′                 ′                Δ; Γ ⊢𝜔 𝑝 : 𝜏 xi        𝜅 = {ℓ } ∪ 𝜔 𝑝 ′ ∈ {𝑙 } Θ(𝑝 ′)
             Σ; Δ; Γ; Θ ⊢ letprov ⟨𝑟 ⟩ 𝑒 : 𝜏 si • 𝜅 ⇒ Γ ′; Θ′                          Σ; Δ; Γ; Θ ⊢ (&𝑟 𝜔 𝑝)ℓ : &𝑟 𝜔 𝜏 xi • 𝜅 ⇒ Γ [𝑟 ↦→ {𝑙 }]; Θ

                                                               T-Branch
                                                                  Σ; Δ; Γ; Θ ⊢ 𝑒 1 : bool • 𝜅 1 ⇒ Γ1 ; Θ1        Σ; Δ; Γ1 ; Θ1 ⊢ 𝑒 2 : 𝜏2si • 𝜅 2 ⇒ Γ2 ; Θ2
                                                                                                  si
 T-Copy                                                                    Σ; Δ; Γ1 ; Θ1 ⊢ 𝑒 3 : 𝜏3 • 𝜅 3 ⇒ Γ3 ; Θ3        𝜏 si = 𝜏2si ∨ 𝜏 si = 𝜏3si
 Δ; Γ ⊢shrd 𝑝 ⇒ {𝑙 }    Δ; Γ ⊢shrd 𝑝 : 𝜏 si                                                si      si
                                                                                 Δ; Γ2 ⊢ 𝜏2 ≲ 𝜏 ⇒ Γ2      ′
                                                                                                                 Δ; Γ3 ⊢ 𝜏3si ≲ 𝜏 si ⇒ Γ3′
              si
                     𝜅 = 𝜔 𝑝 ′ ∈ {𝑙 } Θ(𝑝 ′)                    Γ2 ⋓ Γ3 = Γ          Θ2 ⋓ Θ3 = Θ           Θ = Θ′ [∀𝑝 ∈ Θ′ \ Θ1 . 𝑝 ↦→ Θ′ (𝑝) ∪ 𝜅 1 ]
                        Ð                                        ′     ′     ′                        ′     ′′
  copyableΣ𝜏
       Σ; Δ; Γ; Θ ⊢ 𝑝 : 𝜏 si • 𝜅 ⇒ Γ; Θ                                    Σ; Δ; Γ; Θ ⊢ if 𝑒 1 { 𝑒 2 } else { 𝑒 3 } : 𝜏 si • 𝜅 1 ∪ 𝜅 2 ∪ 𝜅 3 ⇒ Γ ′; Θ′′

                                                Figure 6. Additional information flow inference rules.

                                                                                 □      6. Hence, all mutated places in 𝜎 ′ are projections of a 𝑝 loan .
                                                                                           Therefore 𝜎 ′ [∀𝑝 loan ∈ uniq-loans(𝜋arg, 𝜏 si, •, Γ) . 𝑝 loan ↦→
Lemma A.3 (A function only mutates unique references in                                    𝜎 (𝑝 loan )] reverts all possible mutations, and 𝜎 = 𝜎 ′′.
its argument). Let:                                                                                                                                        □
• Γ, 𝜋arg, 𝜎 where Γ(𝜋arg ) = 𝜏 si and Σ ⊢ 𝜎 : Γ
                               ∗                                              Lemma A.4 (A function’s effects are only influenced by its
• 𝑓 where Σ ⊢ (𝜎; 𝑓 (𝜋 arg )) →− (𝜎 ′; _)                                     argument.). Let:
• 𝜎 ′′ = 𝜎 ′ [∀𝑝 loan ∈ uniq-loans(𝜋arg, 𝜏 si, •, Γ) . 𝑝 loan ↦→ 𝜎 (𝑝 loan )]
                                                                                 • Γ, 𝜋, 𝜎𝑖 where Γ(𝜋 arg ) = 𝜏 si and 𝑖 ∈ {1, 2} and Σ ⊢ 𝜎𝑖 : Γ
Then 𝜎 = 𝜎 ′′.                                                                                                    ∗
                                                                                 • 𝑓 where Σ ⊢ (𝜎𝑖 ; 𝑓 (𝜋 arg )) →
                                                                                                                 − (𝜎𝑖′; 𝑣𝑖 )
Proof.                                                                           • 𝑃 = {𝜋arg } ∪ shrd-loans(𝜋arg, 𝜏 si, •, Γ)
1. Let:                                                                         𝜎1 ∼𝑃 𝜎2 =⇒ 𝜎1′ ∼𝑃 𝜎2′ ∧ 𝑣 1 = 𝑣 2

       Σ(𝑓 ) = fn 𝑓 ⟨𝜑, 𝜚, 𝛼, 𝜚 1 : 𝜚 2 ⟩(𝑥 : 𝜏𝑎si ) → 𝜏𝑟si { 𝑒 }                       Proof.
                                                                                                                                                              ∗
                                                                                        1. As with the proof for Lemma A.3, have (𝜎𝑖 , 𝑓 (𝜋 arg )) →         −
2. By E-App, E-EvalCtx, and E-Framed:                                                      (𝜎𝑖′; 𝑣𝑖 ).
        Σ ⊢(𝜎; 𝑓 (𝜋)) → (𝜎 ♮ 𝑥 ↦→ 𝜎 (𝜋); framed 𝑒) →
                                                   −
                                                                      ∗                 2. By inspection of the operational semantics, the only rule
                                                                                           that could read 𝜎 is E-Copy via the premise (𝜎read ; 𝑝 read ) →
             (𝜎 ′ ♮ 𝜍; framed 𝑣) → (𝜎 ′; 𝑣)                                                (𝜎read ; 𝑣) where 𝜎read ⊢ 𝑝 read ⇓ 𝜋 read ↦→ 𝑣.
3. By inspection of the operational semantics, the only rule                            3. As with the proof for Lemma A.3, the only possible value
   that could modify 𝜎 (as apart from 𝜍) is E-Assign. Assume                               of 𝑝 read = 𝑝 □ [𝑝 loan ] where 𝑝 loan ∈ shrd-loans(𝜋 arg, 𝜏 si, •, Γ).
   that 𝑝 mut := 𝑒 ′ is executed under stack 𝜎mut ♮ 𝜍 during                            4. Because 𝑝 loan ∈ 𝑃 and 𝜎1 ∼𝑃 𝜎2 then 𝜎1 (𝑝 loan ) = 𝜎2 (𝑝 loan ).
   𝑓 (𝜋arg ) where 𝜎mut ⊢ 𝑝 mut ⇓ 𝜋mut .                                                5. Similarly because 𝜋 arg ∈ 𝑃 then 𝜎1 (𝜋arg ) = 𝜎2 (𝜋arg ).
4. By inspection of the operational semantics, the only way                             6. Therefore every readable input for 𝑓 is equal, and for the
   to create a pointer is E-Borrow on a place 𝑝. The only                                  same function body 𝑒, the evaluation should result in the
   places in 𝜎mut that are accessible from 𝑒 are                                           same effects on 𝜎 and same output 𝑣. Hence, 𝜎1′ ∼𝑃 𝜎2′ and
   shrd-loans(𝜋 arg, 𝜏 si, •, Γ), so it must be that 𝑝 mut = 𝑝 □ [𝑝 loan ]                 𝑣1 = 𝑣2.
   and 𝑝 loan ∈ shrd-loans(𝜋arg, 𝜏 si, •, Γ).                                                                                                                 □
5. Because 𝑒 is well-typed under 𝑥 : 𝜏𝑎si , then any shared
   references in 𝑥 cannot be mutated: T-AssignDeref re-                                 A.2.2     Noninterference.
   quires ⊢uniq 𝑝 mut ⇒ {𝑙 }, which by O-Deref requires that
                                                                                        Theorem A.5 (Noninterference). Let 𝑒 such that
   the reference under 𝑝 mut has type &𝑟 uniq 𝜏. Therefore
   𝑝 loan ∈ uniq-loans(𝜋arg, 𝜏 si, •, Γ).                                                                  Σ; •; Γ; Θ ⊢ 𝑒 : 𝜏 • 𝜅 ⇒ Γ ′; Θ′
Modular Information Flow through Ownership                                                                   PLDI ’22, June 13–17, 2022, San Diego, CA, USA


For 𝑖 ∈ {1, 2}, let 𝜎𝑖 such that                                                       6. By IH (a) for 𝑒 1 , if 𝜎1 ∼𝜅Θ1 𝜎2 then 𝑣 1𝑒1 = 𝑣 2𝑒1 .
             Σ ⊢ 𝜎𝑖 : Γ      and      Σ ⊢ (𝜎𝑖 ; 𝑒) →
                                                     ∗
                                                   − (𝜎𝑖′; 𝑣𝑖 )                        7. Because 𝜎1 ∼𝜅Θ2 𝜎2 and 𝜅 1 ⊆ 𝜅 2 by (3), then 𝜎1 ∼𝜅Θ1 𝜎2 and
                                                                                          𝑣 1𝑒1 = 𝑣 2𝑒1 .
                                                                                       8. Therefore 𝜎1𝑥 (𝜋) = 𝜎2𝑥 (𝜋).
Then:
  (a) 𝜎1 ∼𝜅Θ 𝜎2 =⇒ 𝑣 1 = 𝑣 2
  (b) ∀𝑝 ↦→ 𝜅𝑝 ∈ Θ′ . 𝜎1 ∼𝜅Θ𝑝 𝜎2 =⇒ 𝜎1′ (𝑝) = 𝜎2′ (𝑝)                                • T-Assign: 𝑒 = “𝜋mut := 𝑒”. Because 𝑣𝑖 = () then (a) is
                                                                                       trivial, so we focus on (b):
Proof. Proof by induction over the derivation of 𝑒 : 𝜏.                                ∀𝜋any ↦→ 𝜅 any ∈ Θ1′ . 𝜎1 ∼𝜅Θany 𝜎2 =⇒ 𝜎1′ (𝜋any ) = 𝜎2′ (𝜋any )
• T-u32: 𝑒 = 𝑛 ℓ where 𝜅 = {ℓ }. (a) is trivial because 𝑛 always                                                            ∗
  evaluates to 𝑛, and (b) is trivial because 𝑛 has no effects.                         1. By E-EvalCtx, Σ ⊢ (𝜎𝑖 ; 𝑒) →      − (𝜎𝑖𝑒 ; 𝑣𝑖𝑒 ). By IH (b) on 𝑒,
                                                                                          then 𝜎1𝑒 (𝜋any ) = 𝜎2𝑒 (𝜋any ).
• T-Move: 𝑒 = 𝜋 where 𝜅 = Θ(𝜋). (b) is trivial because 𝜋                               2. By E-Assign, Σ ⊢ (𝜎𝑖𝑒 ; 𝜋mut := 𝑣𝑖𝑒 )
  has no effects, so we focus on (a): 𝜎1 ∼Θ    𝜎 =⇒ 𝑣 1 = 𝑣 2
                                          Θ(𝜋 ) 2                                         → (𝜎𝑖𝑒 [𝑥 ↦→ V𝑖 [𝑣𝑖𝑒 ]]; ()) where 𝜋mut = 𝜋mut        □ [𝑥] and

  1. By the definition of equivalence of stacks, Θ(𝜋) ⊆                                   𝜎𝑖 ⊢ 𝜋mut ⇓ V𝑖 .
                                                                                           𝑒

     Θ(𝜋) =⇒ 𝜎1 (𝜋) = 𝜎2 (𝜋).                                                          3. By Lemma A.1, if 𝜎𝑖𝑒 (𝜋any ) ≠ 𝜎𝑖′ (𝜋any ) then 𝜋 any ⊓ 𝜋mut .
  2. By E-Move, 𝑣𝑖 = 𝜎𝑖 (𝜋).                                                           4. By T-Assign, because 𝜋any ⊓ 𝜋mut then
  3. Therefore 𝑣 1 = 𝑣 2 .                                                                Θ1′ (𝜋 any ) = Θ1 (𝜋 any ) ∪ 𝜅𝑒 .
                                                                                       5. Because 𝜅𝑒 ⊆ Θ1′ (𝜋any ), then 𝜎1 ∼𝜅Θ𝑒 𝜎2 .
• T-Copy: the proof is the same as for T-Move.
                                                                                       6. By IH (a) on 𝑒, then 𝑣 1𝑒 = 𝑣 2𝑒 .
• T-Seq: 𝑒 = 𝑒 1 ; 𝑒 2 where 𝜅 = 𝜅 2 .                                                 7. Therefore 𝜎1′ (𝜋any ) = 𝜎2′ (𝜋any ).
   (a) 𝜎1 ∼𝜅Θ2 𝜎2 =⇒ 𝑣 1 = 𝑣 2
    1. By E-EvalCtx, Σ ⊢ (𝜎𝑖 ; 𝑒 1 ) →
                                             ∗
                                     − (𝜎𝑖𝑒1 ; 𝑣𝑖𝑒1 ).                               • T-AssignDeref: 𝑒 = “𝑝 mut := 𝑒”. Like T-Assign, we focus
                                                               ∗                       on (b): ∀𝜋any ↦→ 𝜅 any ∈ Θ1′ . 𝜎1 ∼𝜅Θany 𝜎2 =⇒ 𝜎1′ (𝜋any ) =
    2. By E-Seq, Σ ⊢ (𝜎𝑖𝑒1 ; (𝑣𝑖𝑒1 ; 𝑒 2 )) → (𝜎𝑖𝑒1 ; 𝑒 2 ) →
                                                            − (𝜎𝑖𝑒2 ; 𝑣𝑖𝑒2 ).          𝜎2′ (𝜋any )
       WTS 𝑣 1 = 𝑣 2 .
             𝑒2    𝑒2
                                                                                       1. By E-EvalCtx and E-Assign,
    3. By the IH for 𝑒 2 , 𝑣 1𝑒2 = 𝑣 2𝑒2 if 𝜎1𝑒1 ∼𝜅Θ21 𝜎2𝑒1 .                              Σ ⊢ (𝜎𝑖 ; 𝑝 mut := 𝑒) →
                                                                                                                    ∗
                                                                                                                   − (𝜎𝑖𝑒 [𝑥𝑖 ↦→ V𝑖 [𝑣𝑖𝑒 ]]; ())
    4. Let 𝜋 ↦→ 𝜅𝜋 ∈ Θ1 . WTS 𝜅𝜋 ⊆ 𝜅 2 =⇒ 𝜎1𝑒1 (𝜋) =                                       where 𝜎𝑖 ⊢ 𝑝 mut ⇓ V𝑖 × 𝜋mut,𝑖
                                                                                                      𝑒                     □      [𝑥𝑖 ].
       𝜎2𝑒1 (𝜋).                                                                       2. By IH (b) on 𝑒, 𝜎1 (𝜋any ) = 𝜎2 (𝜋any ).
                                                                                                                𝑒              𝑒

    5. By the IH for 𝑒 1 , 𝜎1𝑒1 (𝜋) = 𝜎2𝑒1 (𝜋) if 𝜎1 ∼𝜅Θ𝜋 𝜎2 .                         3. By Lemma A.1, only consider the case where 𝜋mut,𝑖 ⊓ 𝜋any .
    6. Let 𝜋 ′ ↦→ 𝜅𝜋 ′ ∈ Θ1 such that 𝜅𝜋 ′ ⊆ 𝜅𝜋 . WTS 𝜎1 (𝜋 ′) =                       4. By Lemma A.2, because 𝜋mut,𝑖 ⊓ 𝜋any then
       𝜎2 (𝜋 ′).                                                                           ∃ uniq 𝑝 loan ∈ {𝑙 } . 𝜋 any ⊓ 𝑝 loan .
    7. By assumption, because 𝜅𝜋 ⊆ 𝜅 2 ∧ 𝜅𝜋 ′ ⊆ 𝜅𝜋 , then                              5. By T-AssignDeref, then 𝜅 ⊆ Θ1′ (𝜋 any ), and 𝑣 1𝑒 = 𝑣 2𝑒 ,
       𝜅𝜋 ′ ⊆ 𝜅2 .                                                                         and 𝜎1′ (𝜋any ) = 𝜎2′ (𝜋any ) as in the proof for T-Assign.
    8. By assumption, 𝜎1 (𝜋 ′) = 𝜎2 (𝜋 ′).
   (b) ∀𝜋 ↦→ 𝜅𝜋 ∈ Θ2 . 𝜎1 ∼𝜅Θ𝜋 𝜎2 =⇒ 𝜎1′ (𝜋) = 𝜎2′ (𝜋)                               • T-App: 𝑒 = “𝑓 (𝜋arg )” where 𝜅 = 𝜅 arg .
                                                                                        (a) 𝜎1 ∼𝜅Θarg 𝜎2 =⇒ 𝑣 1 = 𝑣 2
    1. By the IH for 𝑒 2 , 𝜎1′ (𝜋) = 𝜎2′ (𝜋) if 𝜎1𝑒1 ∼𝜅Θ𝜋1 𝜎2𝑒1 .
                                                                                         1. Let 𝑝 ∈ {𝜋arg } ∪ shrd-loans(𝜋arg, 𝜏𝑎si, •, Γ2 ).
    2. The proof that 𝜎1𝑒1 ∼𝜅Θ𝜋1 𝜎2𝑒1 follows similarly as above.                           By Lemma A.4, if 𝜎1 (𝑝) = 𝜎2 (𝑝), then 𝑣 1 = 𝑣 2 .
• T-Let: 𝑒 = “let 𝑥 : 𝜏𝑎si = 𝑒 1 ; 𝑒 2 ”. The proof of (b) follows                       2. By T-App, Θ(𝑝) ⊆ 𝜅 arg . Therefore 𝜎1 (𝑝) = 𝜎2 (𝑝) and
  from the proof for T-Seq. We focus on (a): 𝜎1 ∼𝜅Θ2 𝜎2 =⇒                                  hence 𝑣 1 = 𝑣 2 .
  𝑣1 = 𝑣2                                                                               (b) ∀𝜋any ↦→ 𝜅 any ∈ Θ2 . 𝜎1 ∼𝜅Θany 𝜎2 =⇒ 𝜎1′ (𝜋any ) =
  1. By E-EvalCtx, E-Let, E-EvalCtx, E-Shift:                                               𝜎2′ (𝜋any )
     Σ ⊢ (𝜎𝑖 ; let 𝑥 : 𝜏𝑎si = 𝑒 1 ; 𝑒 2 ) →
                                          − (𝜎𝑖𝑒1 ; let 𝑥 : 𝜏𝑎si = 𝑣𝑒𝑖 1 ; 𝑒 2 ) →
                                          ∗
                                                                                         1. By Lemma A.3 and Lemma A.1, if 𝜎𝑖 (𝜋any ) ≠ 𝜎𝑖′ (𝜋any )
                                      ∗                                                     then: ∃𝑝 loan ∈ uniq-loans(𝜋arg, 𝜏 si, •, Γ2 ) . (𝜎𝑖 ⊢ 𝑝 loan ⇓
      (𝜎𝑖𝑒1 , 𝑥 ↦→ 𝑣𝑒𝑖 1 ; shift 𝑒 2 ) →
                                       −
                                                                                            𝜋loan,𝑖 ) ∧ 𝜋any ⊓ 𝜋loan,𝑖 .
      (𝜎𝑖′, 𝑥 ↦→ _; shift 𝑣𝑖𝑒2 ) → (𝜎𝑖′; 𝑣𝑖𝑒2 ).
                                                                   Θ′                    2. By T-App, then 𝜅 arg ⊆ 𝜅 any .
  2. Let 𝜎𝑖𝑥 = 𝜎𝑖𝑒1 , 𝑥 ↦→ 𝑣𝑖𝑒1 . By IH (a) for 𝑒 2 , if 𝜎1𝑥 ∼𝜅21 𝜎2𝑥 then               3. By Lemma A.4, then 𝜎1′ (𝜋any ) = 𝜎2′ (𝜋any ).
     𝑣 1𝑒2 = 𝑣 2𝑒2 .
  3. Let 𝜋 such that Θ1′ (𝜋) ⊆ 𝜅 2 . WTS 𝜎1𝑥 (𝜋) = 𝜎2𝑥 (𝜋).
  4. If Θ1′ (𝜋) ⊆ Θ(𝜋), then 𝜎1𝑥 (𝜋) = 𝜎2𝑥 (𝜋) is true by as-
     sumption.
  5. Otherwise must be 𝜋 = 𝜋 □ [𝑥] and 𝜅𝑞 ⊆ Θ1′ (𝜋).                                                                                                     □
PLDI ’22, June 13–17, 2022, San Diego, CA, USA                                 Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan


                    Project           Crate       Commit                                                  Features
                    rayon                         c571f8ffb4f74c8c09b4e1e6d9979b71b4414d07                all
                    Rocket            core/lib    8d4d01106e2e10b08100805d40bfa19a7357e900                none
                    rustls            rustls      cdf1dada21a537e141d0c6dde9c5685bb43fbc0e                all
                    sccache                       3f318a8675e4c3de4f5e8ab2d086189f2ae5f5cf                none
                    nalgebra                      984bb1a63943aa68b6f26ff4a6acf8f68b833b70                rand, arbitrary, sparse,
                                                                                                          debug, io, libm
                image                     e916e9dda5f4253f6cc4557b0fe5fa3876ac18e5 none
                hyper                     ed2fdb7b6a2963cea7577df05ddc41c56fee7246 full
                rg3d                      ca7b85f2b30e45b82caee0591ee1abf65bb3eb00 all
                rav1e                     1b6643324752785e7cd6ad0b19257f3c3a9b2c6a none
                RustPython vm             9143e51b7524a5084d5ed230b1f2f5b0610ac58b compiler
Table 2. Build configuration for each package used in the evaluation. Crate is the sub-directory of the crate used for evaluation.
Commit is the point in the project’s Git history used. Features is the flags passed to cargo, where none means “no feature flags”
and all means --all-features.


A.3    Evaluation details                                                      [8] David G. Clarke, John M. Potter, and James Noble. 1998. Ownership
                                                                                   Types for Flexible Alias Protection. In Proceedings of the 13th ACM SIG-
Table 2 provides the build configurations needed to precisely
reproduce the codebases used in Section 5. We also provide a
                                                                                   PLAN Conference on Object-Oriented Programming, Systems, Languages,
                                                                                   and Applications (Vancouver, British Columbia, Canada) (OOPSLA ’98).
Zenodo artifact containing a Docker image that can exactly                         Association for Computing Machinery, New York, NY, USA, 48–64.
reproduce the results in Section 5: https://zenodo.org/record/                     https://doi.org/10.1145/286936.286947
6327882                                                                        [9] Keith D Cooper, Timothy J Harvey, and Ken Kennedy. 2001. A simple,
                                                                                   fast dominance algorithm. Software Practice & Experience 4, 1-10 (2001),
                                                                                   1–8.
References                                                                    [10] Patrick Cousot and Radhia Cousot. 2002. Modular Static Program
 [1] Martín Abadi, Anindya Banerjee, Nevin Heintze, and Jon G. Riecke.             Analysis. In Proceedings of the 11th International Conference on Compiler
     1999. A Core Calculus of Dependency. In Proceedings of the 26th ACM           Construction (CC ’02). Springer-Verlag, Berlin, Heidelberg, 159–178.
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages          [11] R. Cytron, J. Ferrante, B. K. Rosen, M. N. Wegman, and F. K. Zadeck.
     (San Antonio, Texas, USA) (POPL ’99). Association for Computing               1989. An Efficient Method of Computing Static Single Assignment
     Machinery, New York, NY, USA, 147–160. https://doi.org/10.1145/               Form. In Proceedings of the 16th ACM SIGPLAN-SIGACT Symposium on
     292540.292555                                                                 Principles of Programming Languages (Austin, Texas, USA) (POPL ’89).
 [2] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller,          Association for Computing Machinery, New York, NY, USA, 25–35.
     and Alexander J. Summers. 2020. How Do Programmers Use Unsafe                 https://doi.org/10.1145/75277.75280
     Rust? Proc. ACM Program. Lang. 4, OOPSLA, Article 136 (nov 2020),        [12] Al Danial. 2021. cloc: Count Lines of Code. https://github.com/
     27 pages. https://doi.org/10.1145/3428204                                     AlDanial/cloc
 [3] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J.       [13] Isil Dillig, Thomas Dillig, Alex Aiken, and Mooly Sagiv. 2011. Precise
     Summers. 2019. Leveraging Rust Types for Modular Specification and            and Compact Modular Procedure Summaries for Heap Manipulating
     Verification. Proc. ACM Program. Lang. 3, OOPSLA, Article 147 (oct            Programs. In Proceedings of the 32nd ACM SIGPLAN Conference on Pro-
     2019), 30 pages. https://doi.org/10.1145/3360573                              gramming Language Design and Implementation (San Jose, California,
 [4] Thomas H. Austin and Cormac Flanagan. 2009. Efficient Purely-                 USA) (PLDI ’11). Association for Computing Machinery, New York,
     Dynamic Information Flow Analysis. In Proceedings of the ACM SIG-             NY, USA, 567–577. https://doi.org/10.1145/1993498.1993565
     PLAN Fourth Workshop on Programming Languages and Analysis for           [14] Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust
     Security (Dublin, Ireland) (PLAS ’09). Association for Computing Ma-          Used Safely by Software Developers?. In Proceedings of the ACM/IEEE
     chinery, New York, NY, USA, 113–124. https://doi.org/10.1145/1554339.         42nd International Conference on Software Engineering (Seoul, South
     1554353                                                                       Korea) (ICSE ’20). Association for Computing Machinery, New York,
 [5] Abhiram Balasubramanian, Marek S. Baranowski, Anton Burtsev, Au-              NY, USA, 246–257. https://doi.org/10.1145/3377811.3380413
     rojit Panda, Zvonimir Rakamarić, and Leonid Ryzhyk. 2017. System         [15] Jeanne Ferrante, Karl J. Ottenstein, and Joe D. Warren. 1987. The
     Programming in Rust: Beyond Safety. In Proceedings of the 16th Work-          Program Dependence Graph and Its Use in Optimization. ACM Trans.
     shop on Hot Topics in Operating Systems (Whistler, BC, Canada) (Ho-           Program. Lang. Syst. 9, 3 (jul 1987), 319–349. https://doi.org/10.1145/
     tOS ’17). Association for Computing Machinery, New York, NY, USA,             24039.24041
     156–161. https://doi.org/10.1145/3102980.3103006                         [16] Jean-Yves Girard. 1987. Linear logic. Theoretical Computer Science 50,
 [6] Pablo Buiras, Dimitrios Vytiniotis, and Alejandro Russo. 2015. HLIO:          1 (1987), 1–101. https://doi.org/10.1016/0304-3975(87)90045-4
     Mixing Static and Dynamic Typing for Information-Flow Control            [17] J. A. Goguen and J. Meseguer. 1982. Security Policies and Security
     in Haskell. In Proceedings of the 20th ACM SIGPLAN International              Models. In 1982 IEEE Symposium on Security and Privacy. IEEE. https:
     Conference on Functional Programming (Vancouver, BC, Canada) (ICFP            //doi.org/10.1109/sp.1982.10014
     2015). Association for Computing Machinery, New York, NY, USA,           [18] Dan Grossman, Greg Morrisett, Trevor Jim, Michael Hicks, Yanling
     289–301. https://doi.org/10.1145/2784731.2784758                              Wang, and James Cheney. 2002. Region-Based Memory Management
 [7] Marek Chalupa. 2016. Slicing of LLVM bitcode. Master’s thesis. Masaryk        in Cyclone. In Proceedings of the ACM SIGPLAN 2002 Conference on
     University.
Modular Information Flow through Ownership                                                                PLDI ’22, June 13–17, 2022, San Diego, CA, USA


     Programming Language Design and Implementation (Berlin, Germany)                (Toulouse, France) (ESEC/FSE-7). Springer-Verlag, Berlin, Heidelberg,
     (PLDI ’02). Association for Computing Machinery, New York, NY, USA,             235–252.
     282–293. https://doi.org/10.1145/512529.512563                             [30] Alejandro Russo, Koen Claessen, and John Hughes. 2008. A Library for
[19] Andrew Head, Elena L. Glassman, Björn Hartmann, and Marti A.                    Light-Weight Information-Flow Security in Haskell. In Proceedings of
     Hearst. 2018. Interactive Extraction of Examples from Existing Code.            the First ACM SIGPLAN Symposium on Haskell (Victoria, BC, Canada)
     In Proceedings of the 2018 CHI Conference on Human Factors in Com-              (Haskell ’08). Association for Computing Machinery, New York, NY,
     puting Systems. Association for Computing Machinery, New York, NY,              USA, 13–24. https://doi.org/10.1145/1411286.1411289
     USA, 1–12. https://doi.org/10.1145/3173574.3173659                         [31] A. Sabelfeld and A.C. Myers. 2003. Language-based information-flow
[20] Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2019.                security. IEEE Journal on Selected Areas in Communications 21, 1 (2003),
     Stacked Borrows: An Aliasing Model for Rust. Proc. ACM Program.                 5–19. https://doi.org/10.1109/JSAC.2002.806121
     Lang. 4, POPL, Article 41 (dec 2019), 32 pages. https://doi.org/10.1145/   [32] Marc Shapiro and Susan Horwitz. 1997. The Effects of the Precision of
     3371109                                                                         Pointer Analysis. In Proceedings of the 4th International Symposium on
[21] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer.           Static Analysis (SAS ’97). Springer-Verlag, Berlin, Heidelberg, 16–34.
     2017. RustBelt: Securing the Foundations of the Rust Programming           [33] Yannis Smaragdakis and George Balatsouras. 2015. Pointer analysis.
     Language. Proc. ACM Program. Lang. 2, POPL, Article 66 (dec 2017),              Foundations and Trends in Programming Languages 2, 1 (2015), 1–69.
     34 pages. https://doi.org/10.1145/3158154                                  [34] Deian Stefan, Alejandro Russo, John C. Mitchell, and David Maz-
[22] Amy J. Ko and Brad A. Myers. 2004. Designing the Whyline: A De-                 ières. 2011. Flexible Dynamic Information Flow Control in Haskell.
     bugging Interface for Asking Questions about Program Behavior. In               In Proceedings of the 4th ACM Symposium on Haskell (Tokyo, Japan)
     Proceedings of the SIGCHI Conference on Human Factors in Computing              (Haskell ’11). Association for Computing Machinery, New York, NY,
     Systems (Vienna, Austria) (CHI ’04). Association for Computing Ma-              USA, 95–106. https://doi.org/10.1145/2034675.2034688
     chinery, New York, NY, USA, 151–158. https://doi.org/10.1145/985692.       [35] Hao Tang, Xiaoyin Wang, Lingming Zhang, Bing Xie, Lu Zhang, and
     985712                                                                          Hong Mei. 2015. Summary-Based Context-Sensitive Data-Dependence
[23] Peng Li and S. Zdancewic. 2006. Encoding information flow in Haskell.           Analysis in Presence of Callbacks. In Proceedings of the 42nd Annual
     In 19th IEEE Computer Security Foundations Workshop (CSFW’06). 12               ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
     pp.–16. https://doi.org/10.1109/CSFW.2006.13                                    guages (Mumbai, India) (POPL ’15). Association for Computing Ma-
[24] Niko Matsakis. 2017. Non-lexical lifetimes. https://rust-lang.github.           chinery, New York, NY, USA, 83–95. https://doi.org/10.1145/2676726.
     io/rfcs/2094-nll.html                                                           2676997
[25] Andrew C. Myers. 1999. JFlow: Practical Mostly-Static Information          [36] Yan Mei Tang and Pierre Jouvelot. 1994. Separate abstract interpreta-
     Flow Control. In Proceedings of the 26th ACM SIGPLAN-SIGACT Sym-                tion for control-flow analysis. In Lecture Notes in Computer Science.
     posium on Principles of Programming Languages (San Antonio, Texas,              Springer Berlin Heidelberg, 224–243. https://doi.org/10.1007/3-540-
     USA) (POPL ’99). Association for Computing Machinery, New York,                 57887-0_98
     NY, USA, 228–241. https://doi.org/10.1145/292540.292561                    [37] Mark Weiser. 1981. Program Slicing. In Proceedings of the 5th Interna-
[26] Emil Jørgensen Njor and Hilmar Gústafsson. 2021. Static Taint Analysis          tional Conference on Software Engineering (San Diego, California, USA)
     in Rust. Master’s thesis. Aalborg University.                                   (ICSE ’81). IEEE Press, 439–449.
[27] François Pottier and Vincent Simonet. 2003. Information Flow Infer-        [38] Aaron Weiss, Olek Gierczak, Daniel Patterson, and Amal Ahmed. 2019.
     ence for ML. ACM Trans. Program. Lang. Syst. 25, 1 (jan 2003), 117–158.         Oxide: The Essence of Rust. arXiv:arXiv:1903.00982v3
     https://doi.org/10.1145/596980.596983                                      [39] Ming Wen, Junjie Chen, Rongxin Wu, Dan Hao, and Shing-Chi Che-
[28] Zvonimir Rakamaric and Michael Emmi. 2014. SMACK: Decoupling                    ung. 2018. Context-Aware Patch Generation for Better Automated
     Source Language Details from Verifier Implementations. In Proceedings           Program Repair. In Proceedings of the 40th International Conference
     of the 26th International Conference on Computer Aided Verification             on Software Engineering (Gothenburg, Sweden) (ICSE ’18). Associa-
     (CAV) (Lecture Notes in Computer Science, Vol. 8559), Armin Biere and           tion for Computing Machinery, New York, NY, USA, 1–11. https:
     Roderick Bloem (Eds.). Springer, 106–113. https://doi.org/10.1007/978-          //doi.org/10.1145/3180155.3180233
     3-319-08867-9_7                                                            [40] Greta Yorsh, Eran Yahav, and Satish Chandra. 2008. Generating Pre-
[29] Atanas Rountev, Barbara G. Ryder, and William Landi. 1999. Data-Flow            cise and Concise Procedure Summaries. In Proceedings of the 35th
     Analysis of Program Fragments. In Proceedings of the 7th European               Annual ACM SIGPLAN-SIGACT Symposium on Principles of Program-
     Software Engineering Conference Held Jointly with the 7th ACM SIG-              ming Languages (San Francisco, California, USA) (POPL ’08). Asso-
     SOFT International Symposium on Foundations of Software Engineering             ciation for Computing Machinery, New York, NY, USA, 221–234.
                                                                                     https://doi.org/10.1145/1328438.1328467
